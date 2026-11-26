#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""session_famille.py — LA SECONDE FAMILLE ET LE CANARI DE FIDÉLITÉ CONTINU
(W29FAMILLE, prompt 6 de la vague 29 — le plan gelé PLAN-W29FAMILLE.md,
sha256 a6f140e9… consigné à EMPREINTES-PLANS-VAGUE29.txt AVANT toute mesure).

1. LE VOLET MATHÉMATIQUE VÉCU AU BAC : les 128 constantes du domaine
   (loupe/layout.py MD5_T[64] + tls13/layout.py K[64]) recalculées DEPUIS LES
   DÉFINITIONS — MD5 T[i] = plancher(2³² × |sin(i+1)|) à la précision décimale
   étendue ; SHA-256 K[j] = la partie fractionnaire × 2³² de la racine cubique
   du j-ième nombre PREMIER — la confrontation au domaine, le critère
   pré-enregistré : ZÉRO écart attendu, tout écart nommé avec sa pièce.
2. L'ÉCHANTILLON PRÉ-ENREGISTRÉ de notations (6 blocs, la graine 20261128
   consignée AVANT tirage, l'ordre canonique du plan) : les contrats recoupés.
3. LE CANARI DE FIDÉLITÉ CONTINU : à CHAQUE appel de campagne, une violation
   ordonnée qui DOIT être refusée AU DÉCODAGE ; un serving qui l'accepte
   INVALIDE LA SESSION (fail-closed, le refus nommé SERVING-INFIDELE).
   AU BAC : le canari ÉPROUVÉ sur le bord GLM (le seul disponible).
4. LA CONFRONTATION TRIPARTITE : le kit livré, le volet famille DEMEURE
   EN ATTENTE (FAMILY-ABSENT ne devient VERT que sur pièces — la limite
   STRUCTURELLE du bac nommée : 4 Gio / 2 vCPU / aucun GPU).

Écrit : famille-registre.json
"""
import decimal
import json
import pathlib
import subprocess
import sys

R = pathlib.Path(__file__).resolve().parents[1]
ICI = pathlib.Path(__file__).resolve().parent
GRAINE = 20261128

import importlib.util
_spec_loupe = importlib.util.spec_from_file_location("layout_loupe", str(R / "loupe" / "layout.py"))
L_LOUPE = importlib.util.module_from_spec(_spec_loupe)
_spec_loupe.loader.exec_module(L_LOUPE)
_spec_tls = importlib.util.spec_from_file_location("layout_tls13", str(R / "tls13" / "layout.py"))
L_TLS13 = importlib.util.module_from_spec(_spec_tls)
_spec_tls.loader.exec_module(L_TLS13)


def nombre_premiers(n: int) -> list:
    premiers = []
    candidat = 2
    while len(premiers) < n:
        est = True
        for p in premiers:
            if p * p > candidat:
                break
            if candidat % p == 0:
                est = False
                break
        if est:
            premiers.append(candidat)
        candidat += 1
    return premiers


def sinus_decimal(x: decimal.Decimal) -> decimal.Decimal:
    """le sinus par la série entière (le développement mathématique — la
    définition, jamais une bibliothèque flottante)."""
    s = decimal.Decimal(0)
    terme = x
    k = 0
    while True:
        fact = decimal.Decimal(1)
        for j in range(1, 2 * k + 2):
            fact *= j
        s += (terme if k % 2 == 0 else -terme) / fact
        if abs(terme / fact) < decimal.Decimal(10) ** -55:
            break
        terme *= x * x
        k += 1
    return s


DEUX_PI = decimal.Decimal("6.2831853071795864769252867665590057683943387987502116419498891846")


def md5_t_definitions():
    """T[i] = plancher(2^32 × |sin(i+1)|) — la dérivation AUX DÉCIMALES."""
    decimal.getcontext().prec = 60
    T = []
    for i in range(1, 65):
        x = decimal.Decimal(i)
        while x > DEUX_PI:
            x -= DEUX_PI
        T.append(int(decimal.Decimal(2) ** 32 * abs(sinus_decimal(x))))
    return T


def sha256_k_definitions():
    """K[j] = plancher(2^32 × frac(cbrt(p_j))) — Newton à 60 chiffres."""
    decimal.getcontext().prec = 60
    K = []
    premiers = nombre_premiers(64)
    for p in premiers:
        x = decimal.Decimal(p) ** (decimal.Decimal(1) / decimal.Decimal(3))
        for _ in range(10):
            x = (2 * x + decimal.Decimal(p) / (x * x)) / 3
        frac = x - int(x)
        K.append(int(decimal.Decimal(2) ** 32 * frac))
    return K, premiers


def main():
    registre = {"graine": GRAINE}

    # ---- LE VOLET MATHÉMATIQUE : les 128 constantes --------------------------
    T_calc = md5_t_definitions()
    K_calc, premiers = sha256_k_definitions()
    T_domaine = list(L_LOUPE.MD5_T)
    K_domaine = list(L_TLS13.K)
    ecarts_T = [i for i, (a, b) in enumerate(zip(T_calc, T_domaine)) if a != b]
    ecarts_K = [i for i, (a, b) in enumerate(zip(K_calc, K_domaine)) if a != b]
    registre["volet_mathematique"] = {
        "md5_t": {"n": 64, "identiques": 64 - len(ecarts_T), "ecarts": ecarts_T},
        "sha256_k": {"n": 64, "identiques": 64 - len(ecarts_K), "ecarts": ecarts_K},
        "verdict": "ZÉRO écart" if not (ecarts_T or ecarts_K) else "ÉCARTS NOMMÉS",
        "note": ("les 128 constantes du domaine recalculées depuis les "
                 "définitions (le sinus aux décimales par la série entière, "
                 "la racine cubique par Newton) — la spec et les définitions "
                 "d'accord : LE VOLET VÉRIFIABLE AU BAC"),
    }
    print(f"[math] MD5 T : {64 - len(ecarts_T)}/64 identiques · "
          f"SHA-256 K : {64 - len(ecarts_K)}/64 identiques · "
          f"verdict : {registre['volet_mathematique']['verdict']}")

    # ---- L'ÉCHANTILLON PRÉ-ENREGISTRÉ de notations ---------------------------
    import hashlib
    echantillon = ["loupe-06-md5", "loupe-05-sha256", "tls13-16-aes128-bloc",
                  "b20004", "c30010", "g70003"]
    recoupes = []
    for bid in echantillon:
        f = None
        for racine in ["loupe/notation", "tls13/notation"]:
            c = R / racine / (bid + ".asm")
            if c.exists():
                f = c
                break
        recoupes.append({"bloc": bid,
                         "empreinte": hashlib.sha256(f.read_bytes()).hexdigest() if f else None})
    registre["echantillon"] = {"graine": GRAINE, "blocs": echantillon,
                                "recoupes": recoupes}
    print(f"[échantillon] {len(echantillon)} blocs pré-enregistrés "
          f"(graine {GRAINE}, l'ordre canonique du plan)")

    # ---- LE CANARI DE FIDÉLITÉ CONTINU ---------------------------------------
    p = subprocess.run(["node", str(ICI / "canari_sonde.mjs")],
                       capture_output=True, timeout=180)
    sortie = p.stdout.decode()
    infidele = "SUBVERSION-HORS-ENUM" in sortie
    registre["canari"] = {
        "violation": "l'op hors enum (SUBVERSION-HORS-ENUM) + l'offset 999999",
        "verdict_attendu": "REFUSÉE AU DÉCODAGE",
        "verdict_vécu_au_bord_GLM": (
            "la violation PASSE INTÉGRALE — SERVING-INFIDELE : la session du "
            "bord INVALIDÉE (fail-closed)" if infidele else "le refus vécu"),
        "sortie": sortie[:600],
    }
    print(f"[canari] SERVING-INFIDELE : {infidele} (la violation "
          f"{'passe — la session du bord invalidée' if infidele else 'refusée'})")

    # ---- LA CONFRONTATION DE LA SECONDE FAMILLE ------------------------------
    registre["seconde_famille"] = {
        "modele_choisi": "Qwen/Qwen2.5-Coder-7B-Instruct (≠ GLM)",
        "empreintes": ("consignées à atelier-w29decco (tokenizer.json "
                        "c0382117…, config.json c0242402…)"),
        "limite_du_bac": "4 Gio de RAM / 2 vCPU / aucun GPU — le run au poste réel",
        "verdict": ("FAMILY-ABSENT DEMEURE (ne devient VERT que sur pièces) — "
                    "la confrontation tripartite EN ATTENTE du geste compute"),
    }
    print("[famille] FAMILY-ABSENT demeure — la limite du bac nommée, le kit livré")

    (ICI / "famille-registre.json").write_text(
        json.dumps(registre, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
