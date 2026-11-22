#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agregateur_h7.py — L'OUTILLAGE H7 GÉNÉRALISÉ ET L'AGRÉGATEUR
FAIL-CLOSED (ab2vh5c2m, la vague 15). LES LIVRAISONS APPARTIENNENT AU
DÉVELOPPEUR (le geste terrain) — le laboratoire sert la campagne,
l'agrégateur et LA TABLE DES STATUTS.
L'AGRÉGATEUR fail-closed : une livraison manquante = REFUS (exit 2,
JAMAIS un verdict partiel) ; les règles d'arrêt D207 éprouvées (au plus
TROIS livraisons par unité, fermeture au premier VERT sinon au plafond ;
< 10 strates complètes → H7 NON TESTÉE) ; LA RÈGLE DE JUGEMENT :
β̂_s par strate ; le t apparié t_{0,975;13} = 2,160 bilatéral ; LES
QUATRE MÉTRIQUES M1-M4 sans correction de multiplicité nommée.
Usage :
  agregateur_h7.py verif-tirage                (la re-exécution bit-identique)
  agregateur_h7.py statut <livraisons.jsonl>   (la table des statuts)
Le format des livraisons (une par ligne, append-only) :
  {"unite": "fermer-tour1", "essai": 1, "m1": …, "m2": …, "m3": …, "m4": …,
   "vert": true|false}
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
KIT = REPO / "atelier-preregistre-l4nnwqlld" / "kit-h7-stratifiee"
V14 = REPO / "atelier-validite-tcb7tpf9q"
TABLE = V14 / "TABLE-TIRAGE-H7.txt"
SHA_CANONIQUE = "2de7d488c89ea892f1612d8262d386ecfa35da0c2bcef6b9df2908831969d6ea"
PLAFOND = 3             # D207 : au plus TROIS livraisons par unité
STRATES_MIN = 10        # < 10 strates complètes → NON TESTÉE


def lire_table() -> list:
    unites = []
    for l in TABLE.read_text(encoding="utf-8").splitlines():
        if l.startswith("S") and "|" in l:
            f = l.split("|")
            unites.append({"strate": f[0], "famille": f[1],
                           "unite_t": f[2], "unite_c": f[4]})
    return unites


def verif_tirage() -> int:
    """LA RE-EXÉCUTION BIT-IDENTIQUE : le générateur à la graine 20261120
    doit redonner LA TABLE CANONIQUE — le sha affiché PAR LE GÉNÉRATEUR
    LUI-MÊME confronté à 2de7d488… ET les lignes officielles re-trouvées
    (la preuve de non-rétropédalage, la forme du kit)."""
    r = subprocess.run([sys.executable,
                        str(KIT / "generateur_randomisation.py"),
                        "--tirer"], capture_output=True, text=True,
                       timeout=120)
    sha_regen = ""
    for l in r.stdout.splitlines():
        if l.startswith("# sha256 de la table canonique : "):
            sha_regen = l.split(": ", 1)[1].strip()
    lignes_regen = [l for l in r.stdout.splitlines()
                    if l.startswith("S") and "|" in l]
    lignes_officielles = [l for l in TABLE.read_text(encoding="utf-8")
                          .splitlines() if l.startswith("S") and "|" in l]
    ok_sha = sha_regen == SHA_CANONIQUE
    ok_lignes = lignes_regen == lignes_officielles
    print(f"la re-exécution à la graine 20261120 : le sha du générateur "
          f"{sha_regen[:16]}… "
          f"{'== LA CANONIQUE 2de7d488…' if ok_sha else 'ROUGE — ÉCART'}")
    print(f"les 14 lignes de strates : "
          f"{'BIT-IDENTIQUES aux officielles' if ok_lignes else 'ROUGE — ÉCART'}")
    return 0 if (ok_sha and ok_lignes) else 2


def charger_livraisons(chemin: pathlib.Path) -> dict:
    par_unite: dict = {}
    for l in chemin.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        d = json.loads(l)
        par_unite.setdefault(d["unite"], []).append(d)
    for u in par_unite:
        par_unite[u].sort(key=lambda d: d.get("essai", 0))
    return par_unite


def statut_unite(livraisons: list) -> dict:
    """D207 : au plus TROIS livraisons ; fermeture au PREMIER vert sinon
    AU PLAFOND ; les livraisons au-delà du plafond REFUSÉES au nom."""
    if len(livraisons) > PLAFOND:
        return {"etat": "REFUS", "cause": f"{len(livraisons)} livraisons "
                f"> le plafond D207 de {PLAFOND}"}
    for d in livraisons:
        if d.get("vert"):
            return {"etat": "FERMÉE-VERT", "essais": d["essai"],
                    "m2": d.get("m2")}
    if len(livraisons) == PLAFOND:
        return {"etat": "FERMÉE-PLAFOND", "essais": PLAFOND}
    return {"etat": "OUVERTE", "essais": len(livraisons)}


def statut(livraisons_path: pathlib.Path) -> int:
    table = lire_table()
    liv = charger_livraisons(livraisons_path)
    refus, completes = [], 0
    for s in table:
        ut = statut_unite(liv.get(s["unite_t"], []))
        uc = statut_unite(liv.get(s["unite_c"], []))
        complete = ut["etat"].startswith("FERMÉE") and \
            uc["etat"].startswith("FERMÉE")
        completes += complete
        print(f"{s['strate']} ({s['famille']}) : T {ut['etat']} / "
              f"C {uc['etat']}" + ("  [COMPLÈTE]" if complete else ""))
        for st in (ut, uc):
            if st["etat"] == "REFUS":
                refus.append(f"{s['strate']} : {st['cause']}")
    if refus:
        print("\n[AGRÉGATEUR] REFUS (exit 2) — jamais un verdict partiel :")
        for l in refus:
            print("  " + l)
        return 2
    if completes < STRATES_MIN:
        print(f"\n[H7] NON TESTÉE — {completes} strates complètes < "
              f"{STRATES_MIN} (la règle fail-closed, AUCUN verdict partiel)")
        return 2
    print(f"\n[H7] {completes} strates complètes — LE JUGEMENT : β̂_s par "
          "strate (les QUATRE tours par strate aux journaux de campagne), "
          "le t apparié t_{0,975;13} = 2,160 bilatéral, les QUATRE "
          "métriques sans correction de multiplicité — LE GESTE "
          "DÉVELOPPEUR aux livraisons recoupées")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    if sys.argv[1] == "verif-tirage":
        return verif_tirage()
    if sys.argv[1] == "statut":
        if len(sys.argv) < 3:
            print("le fichier de livraisons attendu")
            return 2
        return statut(pathlib.Path(sys.argv[2]))
    return 2


if __name__ == "__main__":
    sys.exit(main())
