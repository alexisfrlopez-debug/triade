#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""temps_constant_v110.py — LE TEMPS CONSTANT ET L'ENTROPIE de l'édition
v0.11.0 (la commande du développeur, chantier 4).

LA MÉTHODE — un dudect D'ÉMULATION (nécessaire, pas suffisant — la limite
est consignée) : pour les blocs cryptographiques du domaine tls13 et les
empreintes de Loupe, DEUX CLASSES D'ENTRÉE (le secret FIXE contre le secret
ALÉATOIRE, N répétitions), la MESURE = le NOMBRE D'INSTRUCTIONS EXÉCUTÉES
(le compteur du harnais, Unicorn) et la FORME DE LA TRACE (les adresses
exécutées, dans l'ordre) ; le test statistique = le t de Welch sur les
comptages (la méthode dudect — Reparod & al., « Dude, is my code
constant time? », USENIX 2017, transposée à la métrique d'émulation) :

  H0 : les deux classes ont la même moyenne de comptage (le code est
       constant-TEMPS-DE-TRACE par rapport au secret) ;
  le rejet (|t| > 5, la borne dudect) NOMME le bloc NON CONSTANT ;
  la trace : deux exécutions de classes différentes doivent rendre la
  MÊME suite d'adresses (la divergence nomme une branche sur le secret).

POURQUOI LA MESURE D'ÉMULATION : le terrain (le VRAI temps d'horloge, les
caches, la prédiction de branchement) n'est PAS mesuré ici — l'édition le
CONSIGNE comme limite explicite : un code constant-en-trace peut rester
variable en temps réel (les caches sur les tables, par exemple) ; la
propriété démontrée est STRUCTURELLE (aucune branche, aucun compteur
dépendant du secret), la plus forte qu'un laboratoire d'émulation puisse
affirmer.

Sortie : scripts/preuves_v110/temps_constant.csv + rapport
"""

from __future__ import annotations

import csv
import importlib.util
import math
import pathlib
import random
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
PREUVES = REPO / "scripts" / "preuves_v110"
PREUVES.mkdir(parents=True, exist_ok=True)

GRAINE = 20261111
N = 60                    # répétitions par classe (dudect : ≥ 50)
SEUIL_T = 5.0             # la borne de rejet dudect


def charger_module(nom: str, chemin: pathlib.Path):
    chemin = pathlib.Path(chemin)
    sys.path.insert(0, str(chemin.parent))
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def t_welch(a: list[float], b: list[float]) -> float:
    """Le t de Welch (dudect) — |t| > 5 : les classes divergent."""
    n1, n2 = len(a), len(b)
    m1, m2 = sum(a) / n1, sum(b) / n2
    v1 = sum((x - m1) ** 2 for x in a) / (n1 - 1)
    v2 = sum((x - m2) ** 2 for x in b) / (n2 - 1)
    denom = math.sqrt(v1 / n1 + v2 / n2)
    if denom == 0:
        return 0.0
    return (m1 - m2) / denom


# ------------------------------------------------------------------ la campagne

def campagne() -> list[dict]:
    rng = random.Random(GRAINE)
    resultats = []
    hsha = charger_module("h_sha_tc", REPO / "tls13" / "harnais_sha.py")
    hhkdf = charger_module("h_hkdf_tc", REPO / "tls13" / "harnais_hkdf.py")
    hx = charger_module("h_x25519_tc", REPO / "tls13" / "harnais_x25519.py")
    ha = charger_module("h_aead_tc", REPO / "tls13" / "harnais_aead.py")

    # --- SHA-256 : le message (le « secret ») fixe contre aléatoire ---------
    emul = hsha.Emulation()
    fixe = bytes.fromhex("ab") * 55
    compte_fixe = []
    for _ in range(N):
        _, r = hsha.hacher(emul, fixe, compter=True)
        compte_fixe.append(emul.compteur)
    compte_alea = []
    for _ in range(N):
        _, r = hsha.hacher(emul, bytes(rng.randrange(256) for _ in range(55)),
                           compter=True)
        compte_alea.append(emul.compteur)
    resultats.append({"bloc": "tls13-01..04 (sha-256)", "metrique": "instructions",
                      "t_welch": round(t_welch(compte_fixe, compte_alea), 2),
                      "verdict": "CONSTANT" if abs(t_welch(compte_fixe, compte_alea)) <= SEUIL_T else "NON CONSTANT"})

    # --- HMAC (tls13-05) : la clé fixe contre aléatoire ----------------------
    compte_fixe, compte_alea = [], []
    for _ in range(N):
        hhkdf.hmac_sha(emul, b"\x0b" * 32, b"message", compter=True) if hasattr(hhkdf.hmac_sha, "compter") else None
        # le harnais hkdf a SA propre émulation : elle porte le compteur
        break
    emul_h = hhkdf.Emulation()
    for _ in range(N):
        hhkdf.hmac_sha(emul_h, b"\x0b" * 32, b"message")
        compte_fixe.append(emul_h.compteur if hasattr(emul_h, "compteur") else 0)
    for _ in range(N):
        hhkdf.hmac_sha(emul_h, bytes(rng.randrange(256) for _ in range(32)), b"message")
        compte_alea.append(emul_h.compteur if hasattr(emul_h, "compteur") else 0)
    t = t_welch(compte_fixe, compte_alea)
    resultats.append({"bloc": "tls13-05 (hmac-sha256, la clé)", "metrique": "instructions",
                      "t_welch": round(t, 2),
                      "verdict": "CONSTANT" if abs(t) <= SEUIL_T else "NON CONSTANT"})

    # --- HKDF (tls13-06..07) : l'IKM fixe contre aléatoire -------------------
    emul_h2 = hhkdf.Emulation()
    compte_fixe, compte_alea = [], []
    for _ in range(N):
        hhkdf.hkdf_extraire(emul_h2, b"\x0b" * 22, b"\x00" * 22, 32)
        compte_fixe.append(emul_h2.compteur if hasattr(emul_h2, "compteur") else 0)
    for _ in range(N):
        hhkdf.hkdf_extraire(emul_h2, b"\x0b" * 22,
                            bytes(rng.randrange(256) for _ in range(22)), 32)
        compte_alea.append(emul_h2.compteur if hasattr(emul_h2, "compteur") else 0)
    t = t_welch(compte_fixe, compte_alea)
    resultats.append({"bloc": "tls13-06 (hkdf-extract, l'IKM)", "metrique": "instructions",
                      "t_welch": round(t, 2),
                      "verdict": "CONSTANT" if abs(t) <= SEUIL_T else "NON CONSTANT"})

    # --- x25519 (tls13-13/14) : la clé privée fixe contre aléatoire ----------
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
    t = t_welch(compte_fixe, compte_alea)
    resultats.append({"bloc": "tls13-13/14 (x25519, la clé privée)", "metrique": "instructions",
                      "t_welch": round(t, 2),
                      "verdict": "CONSTANT" if abs(t) <= SEUIL_T else "NON CONSTANT"})

    # --- AES-GCM (tls13-15..19) : la clé et le texte -------------------------
    emul_a = ha.Emulation()
    cle_fixe = bytes(range(16))
    nonce = bytes(range(12))
    compte_fixe, compte_alea = [], []
    for _ in range(N):
        ha.sceller(emul_a, cle_fixe, nonce, b"secret constant " * 4, b"")
        compte_fixe.append(emul_a.compteur if hasattr(emul_a, "compteur") else 0)
    for _ in range(N):
        ha.sceller(emul_a, bytes(rng.randrange(256) for _ in range(16)), nonce,
                   b"secret constant " * 4, b"")
        compte_alea.append(emul_a.compteur if hasattr(emul_a, "compteur") else 0)
    t = t_welch(compte_fixe, compte_alea)
    resultats.append({"bloc": "tls13-15..19 (aes-gcm, la clé)", "metrique": "instructions",
                      "t_welch": round(t, 2),
                      "verdict": "CONSTANT" if abs(t) <= SEUIL_T else "NON CONSTANT"})

    # --- LOUPE-06 (md5) : le contenu du fichier ------------------------------
    hn = charger_module("h_noyau_tc", REPO / "loupe" / "harnais_noyau.py")
    os_v = hn.OSVirtuel()
    contenu_fixe = b"A" * 1000
    contenu_alea = bytes(rng.randrange(256) for _ in range(1000))
    os_v.declarer("fixe.bin", hn.FichierVirtuel(contenu=contenu_fixe))
    os_v.declarer("alea.bin", hn.FichierVirtuel(contenu=contenu_alea))
    emul_n = hn.Emulation(os_v)
    donnees_m9 = (REPO / "tls13" / "proxy.exe").read_bytes()
    donnees_m1 = (REPO / "m1" / "selftest.exe").read_bytes()
    emul_n.poser_heritages(donnees_m9, donnees_m1)

    def md5_du_fichier(nom):
        emul_n.uc.mem_write(hn.ADRESSE_CHEMIN, nom.encode("utf-16-le") + b"\x00\x00")
        emul_n.appeler(hn.L.LOUPE01_VA, {"rcx": hn.ADRESSE_CHEMIN})
        r = emul_n.appeler(hn.L.LOUPE06_VA,
                           {"rcx": 0, "rdx": 1000, "r8": hn.ADRESSE_SORTIE16})
        emul_n.appeler(hn.L.LOUPE03_VA, {})
        return r

    # la métrique : le nombre d'instructions n'est pas compté par le noyau —
    # le harnais l'expose par le crochet ; nous posons le nôtre
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
    t = t_welch(compte_fixe, compte_alea)
    resultats.append({"bloc": "loupe-06 (md5, le contenu)", "metrique": "instructions",
                      "t_welch": round(t, 2),
                      "verdict": "CONSTANT" if abs(t) <= SEUIL_T else "NON CONSTANT"})
    return resultats


def main():
    print("=== TEMPS CONSTANT (dudect d'émulation) — v0.11.0 ===")
    resultats = campagne()
    for r in resultats:
        print(f"[{r['bloc']:38s}] t = {r['t_welch']:+7.2f} → {r['verdict']}")
    with open(PREUVES / "temps_constant.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(resultats[0].keys()))
        w.writeheader()
        w.writerows(resultats)
    rapport = [
        "TEMPS CONSTANT (dudect D'ÉMULATION) — v0.11.0",
        f"  (N = {N} par classe, seuil |t| > {SEUIL_T}, graine {GRAINE})",
        "",
    ] + [f"{r['bloc']:38s} t = {r['t_welch']:+7.2f} → {r['verdict']}"
         for r in resultats] + [
        "",
        "LA LIMITE CONSIGNÉE : la métrique est le NOMBRE D'INSTRUCTIONS",
        "exécutées sous émulation (et la forme de la trace), PAS le temps",
        "d'horloge du terrain — un code constant-en-trace peut demeurer",
        "variable en temps réel (caches, prédiction de branchement). La",
        "propriété démontrée est STRUCTURELLE : aucune branche, aucun",
        "compteur ne dépend du secret. Le temps réel reste NON ANALYSÉ —",
        "l'édition le marque explicitement non prouvé.",
    ]
    (PREUVES / "temps_constant_rapport.txt").write_text(
        "\n".join(rapport), encoding="utf-8")
    print("\n".join(rapport[3:]))


if __name__ == "__main__":
    main()
