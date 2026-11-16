#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""egalite_traces_v180.py — LA VÉRIFICATION D'ÉGALITÉ EXACTE DES TRACES
(l'instruction gfylb610p, la vague 5) : « §3.5 et Table 6 rapportent
"all |t| = 0" pour le dudect d'émulation (N=60/classe). Sur des traces
d'instructions identiques, la variance est nulle et le t de Welch est
indéfini (nan), pas zéro : la formulation actuelle est un artefact. »

LA VÉRIFICATION DEMANDÉE : « script qui rejoue les 6 cibles, vérifie
l'égalité exacte des traces (pas un t-test), confirme le compte
1 238 959 pour x25519, et refuse toute réapparition de "|t| = 0" dans
le manuscrit ».

LA MÉTHODE — l'égalité EXACTE, pas un test statistique : pour chacune
des 6 cibles de temps_constant_v110.py (graine 20261111, N=60/classe,
LES MÊMES protocoles), les comptages d'instructions des DEUX classes
(secret fixe contre secret aléatoire) doivent être BIT-IDENTIQUES :
un SEUL compte distinct sur les 120 mesures — variance nulle, t de
Welch INDÉFINI (0/0), jamais « |t| = 0 ». Le compte x25519 doit être
EXACTEMENT 1 238 959.

Sortie : livraison-vague5/p7-egalite-traces.txt (+ CSV)
Code retour : 0 = égalité exacte partout ; 2 = refus nommé.
"""
from __future__ import annotations

import csv
import importlib.util
import pathlib
import random
import sys

REPO = pathlib.Path("/tmp/triade-gh")
SORTIE = pathlib.Path("/home/z/my-project/livraison-vague5")
SORTIE.mkdir(parents=True, exist_ok=True)

GRAINE = 20261111
N = 60                    # répétitions par classe (le protocole v110)
X25519_ATTENDU = 1_238_959  # le compte consigné au manuscrit


def charger_module(nom: str, chemin: pathlib.Path):
    sys.path.insert(0, str(chemin.parent))
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def verdict_egalite(nom: str, fixe: list[int], alea: list[int]) -> dict:
    """L'égalité EXACTE : un seul compte distinct sur les 120 mesures."""
    tous = fixe + alea
    distincts = sorted(set(tous))
    egalite = (len(distincts) == 1)
    return {"cible": nom, "n_fixe": len(fixe), "n_alea": len(alea),
            "comptes_distincts": len(distincts),
            "compte_unique": distincts[0] if egalite else None,
            "min": min(tous), "max": max(tous),
            "egalite_exacte": egalite}


def campagne() -> tuple[list[dict], bool]:
    rng = random.Random(GRAINE)
    resultats: list[dict] = []
    ok_global = True

    hsha = charger_module("h_sha_eq", REPO / "tls13" / "harnais_sha.py")

    # --- SHA-256 (tls13-01..04) : le message fixe contre aléatoire -------
    emul = hsha.Emulation()
    fixe_secret = bytes.fromhex("ab") * 55
    compte_fixe = []
    for _ in range(N):
        hsha.hacher(emul, fixe_secret, compter=True)
        compte_fixe.append(emul.compteur)
    compte_alea = []
    for _ in range(N):
        hsha.hacher(emul, bytes(rng.randrange(256) for _ in range(55)),
                    compter=True)
        compte_alea.append(emul.compteur)
    r = verdict_egalite("tls13-01..04 (sha-256)", compte_fixe, compte_alea)
    resultats.append(r); ok_global &= r["egalite_exacte"]

    # --- HMAC (tls13-05) : la clé fixe contre aléatoire -------------------
    # LA FAUTE v110 NOMMÉE : hmac_sha était appelée SANS compter=True — le
    # compteur jamais activé, les 120 mesures lisaient 0 : le « t = 0 » de
    # v0.11.0 était VIDE sur cette cible (l'artefact dénoncé par la vague 5)
    hhkdf = charger_module("h_hkdf_eq", REPO / "tls13" / "harnais_hkdf.py")
    emul_h = hhkdf.Emulation()
    compte_fixe, compte_alea = [], []
    for _ in range(N):
        hhkdf.hmac_sha(emul_h, b"\x0b" * 32, b"message", compter=True)
        compte_fixe.append(emul_h.compteur)
    for _ in range(N):
        hhkdf.hmac_sha(emul_h, bytes(rng.randrange(256) for _ in range(32)),
                       b"message", compter=True)
        compte_alea.append(emul_h.compteur)
    r = verdict_egalite("tls13-05 (hmac-sha256, la clé)", compte_fixe, compte_alea)
    resultats.append(r); ok_global &= r["egalite_exacte"]

    # --- HKDF (tls13-06) : l'IKM fixe contre aléatoire --------------------
    # (v110 passait « 32 » en 4e position = compter=32, VÉRIDIQUE par accident —
    #  ici l'activation EXPLICITE, le même compte attendu)
    emul_h2 = hhkdf.Emulation()
    compte_fixe, compte_alea = [], []
    for _ in range(N):
        hhkdf.hkdf_extraire(emul_h2, b"\x0b" * 22, b"\x00" * 22, compter=True)
        compte_fixe.append(emul_h2.compteur)
    for _ in range(N):
        hhkdf.hkdf_extraire(emul_h2, b"\x0b" * 22,
                            bytes(rng.randrange(256) for _ in range(22)),
                            compter=True)
        compte_alea.append(emul_h2.compteur)
    r = verdict_egalite("tls13-06 (hkdf-extract, l'IKM)", compte_fixe, compte_alea)
    resultats.append(r); ok_global &= r["egalite_exacte"]

    # --- x25519 (tls13-13/14) : la clé privée fixe contre aléatoire -------
    hx = charger_module("h_x25519_eq", REPO / "tls13" / "harnais_x25519.py")
    emul_x = hx.Emulation()
    privee_fixe = bytes.fromhex(
        "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
    compte_fixe, compte_alea = [], []
    for _ in range(N):
        hx.cle_publique(emul_x, privee_fixe, compter=True)
        compte_fixe.append(emul_x.compteur if hasattr(emul_x, "compteur") else 0)
    for _ in range(N):
        hx.cle_publique(emul_x, bytes(rng.randrange(256) for _ in range(32)),
                        compter=True)
        compte_alea.append(emul_x.compteur if hasattr(emul_x, "compteur") else 0)
    r = verdict_egalite("tls13-13/14 (x25519, la clé privée)",
                        compte_fixe, compte_alea)
    r["x25519_confirme"] = (r["compte_unique"] == X25519_ATTENDU)
    ok_global &= r["egalite_exacte"] and r["x25519_confirme"]
    resultats.append(r)

    # --- AES-GCM (tls13-15..19) : la clé fixe contre aléatoire ------------
    ha = charger_module("h_aead_eq", REPO / "tls13" / "harnais_aead.py")
    emul_a = ha.Emulation()
    cle_fixe = bytes(range(16))
    nonce = bytes(range(12))
    compte_fixe, compte_alea = [], []
    for _ in range(N):
        ha.sceller(emul_a, cle_fixe, nonce, b"secret constant " * 4, b"",
                   compter=True)
        compte_fixe.append(emul_a.compteur)
    for _ in range(N):
        ha.sceller(emul_a, bytes(rng.randrange(256) for _ in range(16)), nonce,
                   b"secret constant " * 4, b"", compter=True)
        compte_alea.append(emul_a.compteur)
    # LA FAUTE v110 NOMMÉE : sceller était appelée SANS compter=True — le
    # « t = 0 » de v0.11.0 était VIDE sur cette cible aussi
    r = verdict_egalite("tls13-15..19 (aes-gcm, la clé)", compte_fixe, compte_alea)
    resultats.append(r); ok_global &= r["egalite_exacte"]

    # --- LOUPE-06 (md5) : le contenu du fichier ---------------------------
    hn = charger_module("h_noyau_eq", REPO / "loupe" / "harnais_noyau.py")
    os_v = hn.OSVirtuel()
    contenu_fixe = b"A" * 1000
    contenu_alea = bytes(rng.randrange(256) for _ in range(1000))
    os_v.declarer("fixe.bin", hn.FichierVirtuel(contenu=contenu_fixe))
    os_v.declarer("alea.bin", hn.FichierVirtuel(contenu=contenu_alea))
    emul_n = hn.Emulation(os_v)
    emul_n.poser_heritages((REPO / "tls13" / "proxy.exe").read_bytes(),
                           (REPO / "m1" / "selftest.exe").read_bytes())

    def md5_du_fichier(nom):
        emul_n.uc.mem_write(hn.ADRESSE_CHEMIN,
                            nom.encode("utf-16-le") + b"\x00\x00")
        emul_n.appeler(hn.L.LOUPE01_VA, {"rcx": hn.ADRESSE_CHEMIN})
        emul_n.appeler(hn.L.LOUPE06_VA,
                       {"rcx": 0, "rdx": 1000, "r8": hn.ADRESSE_SORTIE16})
        emul_n.appeler(hn.L.LOUPE03_VA, {})

    from unicorn import UC_HOOK_CODE
    compteur = {"n": 0}
    actif = {"on": False}

    def croch(uc, adresse, taille, donnees):
        if actif["on"]:
            compteur["n"] += 1

    emul_n.uc.hook_add(UC_HOOK_CODE, croch)

    def mesurer(nom):
        compteur["n"] = 0
        actif["on"] = True
        md5_du_fichier(nom)
        actif["on"] = False
        return compteur["n"]

    compte_fixe = [mesurer("fixe.bin") for _ in range(N)]
    compte_alea = [mesurer("alea.bin") for _ in range(N)]
    r = verdict_egalite("loupe-06 (md5, le contenu)", compte_fixe, compte_alea)
    resultats.append(r); ok_global &= r["egalite_exacte"]

    return resultats, ok_global


def main() -> int:
    print("=== L'ÉGALITÉ EXACTE DES TRACES — les 6 cibles du dudect "
          "d'émulation (N=60/classe, graine 20261111) ===")
    resultats, ok = campagne()
    lignes = []
    for r in resultats:
        ligne = (f"{r['cible']:<38s} comptes distincts "
                 f"{r['comptes_distincts']:<3d} "
                 f"[min {r['min']} .. max {r['max']}] "
                 f"→ {'ÉGALITÉ EXACTE' if r['egalite_exacte'] else 'DIVERGENCE'}")
        if "x25519_confirme" in r:
            ligne += (f" — le compte unique {r['compte_unique']:,} "
                      f"{'==' if r['x25519_confirme'] else '≠'} "
                      f"1 238 959 attendu".replace(",", " "))
        print(ligne)
        lignes.append(ligne)

    rapport = [
        "L'ÉGALITÉ EXACTE DES TRACES D'INSTRUCTIONS — LA VÉRIFICATION "
        "DE LA VAGUE 5 (l'instruction gfylb610p)",
        f"  (les 6 cibles de temps_constant_v110.py rejouées : N={N} par "
        f"classe, graine {GRAINE}, les MÊMES protocoles)",
        "",
    ] + lignes + [
        "",
        "LA FORMULATION CORRECTE (qui remplace « all |t| = 0 ») : sur des",
        "traces d'instructions bit-identiques entre classes secret-fixe et",
        "secret-aléatoire, la variance est NULLE et le t de Welch est",
        "INDÉFINI (0/0), pas zéro : l'égalité est EXACTE, vérifiée comme",
        "telle — jamais un test statistique de puissance. N=60 est un",
        "contrôle structurel exact ; le temps réel matériel est l'affaire",
        "du kit dudect (mesuré à part).",
        "",
        ("VERDICT : VERT — égalité exacte sur les 6 cibles, le compte "
         "x25519 confirmé" if ok else
         "VERDICT : ROUGE — une divergence nommée, le refus s'impose"),
    ]
    (SORTIE / "p7-egalite-traces.txt").write_text(
        "\n".join(rapport), encoding="utf-8")
    with open(SORTIE / "p7-egalite-traces.csv", "w", newline="",
              encoding="utf-8") as f:
        champs = ["cible", "n_fixe", "n_alea", "comptes_distincts",
                  "compte_unique", "min", "max", "egalite_exacte",
                  "x25519_confirme"]
        w = csv.DictWriter(f, fieldnames=champs, extrasaction="ignore")
        w.writeheader()
        w.writerows(resultats)
    print("\n".join(rapport[-2:]))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
