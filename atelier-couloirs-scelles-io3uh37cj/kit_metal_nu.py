#!/usr/bin/env python3
"""kit_metal_nu.py — atelier IO3UH37CJ (la vague 16).

LE KIT DE MESURE MÉTAL NU (≥ 2 machines) — PRÉPARÉ, PAS EXÉCUTÉ AU LABORATOIRE.
La machine nue est le geste du développeur ; le laboratoire livre le protocole,
le manifeste et L'AGRÉGATEUR QUI REFUSE.

La règle : une machine manquante = REFUS (exit 2), JAMAIS un verdict partiel.
Un agrégateur qui rend un chiffre sur deux machines quand trois étaient
attendues est un mensonge de mesure — il refuse et il NOMME la pièce absente.
"""

import argparse
import json
import os
import sys

MACHINES_ATTENDUES = 2          # ≥ 2 machines : la borne du protocole
PIECES_PAR_MACHINE = ("couloir", "evp", "repli")   # les TROIS pièces par machine
COLONNES = ("c_fenetre", "c_appel", "c_octet_4096", "iqr")


def manifeste(nom_machine: str, sortie: str):
    """Le manifeste d'UNE machine — l'empreinte CPU, l'état de fréquence, le cœur épinglé."""
    import platform
    doc = {
        "schema": "TRIADE-METAL-NU-MANIFESTE-v1",
        "machine": nom_machine,
        "empreinte_cpu": {
            "processeur": platform.processor() or "(à consigner au poste)",
            "architecture": platform.machine(),
            "systeme": f"{platform.system()} {platform.release()}",
            "noyau": platform.version(),
            "drapeaux_requis": ["aes", "pclmulqdq", "rdtscp", "avx2"],
        },
        "etat_frequence": "(le gouverneur FIXED si possible — sinon l'état vécu NOMMÉ)",
        "coeur_epingle": "(taskset -c <coeur> — le même cœur aux deux machines)",
        "meme_entree": "le clair du rig (la graine 20261124 — JAMAIS retapée)",
        "pieces_attendues": list(PIECES_PAR_MACHINE),
        "note": "l'écart VM / métal nu est NOMMÉ, jamais maquillé — la VM partage le port "
                "pclmulqdq et l'unité AES avec l'hôte ; la mesure métal nu départage le partage",
    }
    with open(sortie, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"le manifeste {nom_machine} : {sortie}")
    return 0


def agreger(dossier: str, sortie: str = None):
    """L'agrégateur fail-closed : TOUTES les machines, TOUTES les pièces — sinon REFUS."""
    registres = {}
    for nom in sorted(os.listdir(dossier)) if os.path.isdir(dossier) else []:
        if nom.endswith(".json"):
            with open(os.path.join(dossier, nom), encoding="utf-8") as f:
                registres[nom[:-5]] = json.load(f)

    manquants = []
    if len(registres) < MACHINES_ATTENDUES:
        manquants.append(f"il faut ≥ {MACHINES_ATTENDUES} machines, "
                         f"{len(registres)} trouvée(s)")
    for machine, reg in registres.items():
        for piece in PIECES_PAR_MACHINE:
            if piece not in reg.get("pieces", {}):
                manquants.append(f"{machine} : la pièce « {piece} » manque")
        for col in COLONNES:
            for piece, val in reg.get("pieces", {}).items():
                if col not in val:
                    manquants.append(f"{machine}.{piece} : l'opérande « {col} » manque")

    print("=== L'AGRÉGATEUR MÉTAL NU (fail-closed) ===")
    print(f"  les machines trouvées : {len(registres)} ({', '.join(sorted(registres)) or 'aucune'})")
    if manquants:
        print("  LE VERDICT : REFUS (exit 2) — jamais un verdict partiel")
        for m in manquants:
            print(f"    - {m}")
        return 2

    print("  LES SIX COLONNES (machine × {{couloir, EVP, repli}}) aux opérandes non arrondis :")
    for machine in sorted(registres):
        for piece in PIECES_PAR_MACHINE:
            v = registres[machine]["pieces"][piece]
            print(f"    {machine:14s} {piece:8s} "
                  f"{v['c_fenetre']:>12} {v['c_appel']:>10} {v['c_octet_4096']:>10} "
                  f"IQR {v['iqr']:>8}")
    if sortie:
        with open(sortie, "w", encoding="utf-8") as f:
            json.dump({"schema": "TRIADE-METAL-NU-AGREGAT-v1", "machines": registres},
                      f, ensure_ascii=False, indent=2)
        print(f"  l'agrégat : {sortie}")
    print("  LE VERDICT : VERT — toutes les machines, toutes les pièces")
    return 0


def autotest():
    """Le contrôle négatif vécu : un jeu INCOMPLET doit REFUSER (exit 2)."""
    import tempfile
    print("=== L'AUTOTEST DE L'AGRÉGATEUR ===")
    avec = tempfile.mkdtemp()
    complet = {
        "machine-A": {"pieces": {p: {"c_fenetre": 1234.5, "c_appel": 12.34,
                                     "c_octet_4096": 0.7271, "iqr": 3.2}
                                 for p in PIECES_PAR_MACHINE}},
        "machine-B": {"pieces": {p: {"c_fenetre": 1301.9, "c_appel": 13.01,
                                     "c_octet_4096": 0.7646, "iqr": 3.9}
                                 for p in PIECES_PAR_MACHINE}},
    }
    for n, r in complet.items():
        with open(os.path.join(avec, n + ".json"), "w", encoding="utf-8") as f:
            json.dump(r, f)
    rc_complet = agreger(avec)

    incomplet = tempfile.mkdtemp()
    with open(os.path.join(incomplet, "machine-A.json"), "w", encoding="utf-8") as f:
        json.dump({"machine-A": {"pieces": {"couloir": {"c_fenetre": 1, "c_appel": 1,
                                                        "c_octet_4096": 1, "iqr": 1}}}}, f)
    rc_incomplet = agreger(incomplet)

    tests = [rc_complet == 0, rc_incomplet == 2]
    print(f"  [1] le jeu COMPLET (2 machines, 3 pièces)     : {'VERT' if rc_complet == 0 else 'ROUGE'}")
    print(f"  [2] le jeu INCOMPLET (une machine, une pièce) : "
          f"{'REFUSÉ exit 2' if rc_incomplet == 2 else 'ROUGE — il a rendu un verdict partiel'}")
    print(f"  {sum(1 for t in tests if t)}/{len(tests)} contrôles rendus")
    return 0 if all(tests) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifeste", metavar="NOM_MACHINE")
    ap.add_argument("--sortie", default=None)
    ap.add_argument("--agreger", metavar="DOSSIER")
    ap.add_argument("--autotest", action="store_true")
    args = ap.parse_args()
    if args.autotest:
        return autotest()
    if args.agreger:
        return agreger(args.agreger, args.sortie)
    if args.manifeste:
        return manifeste(args.manifeste, args.sortie or f"manifeste-{args.manifeste}.json")
    ap.error("--manifeste, --agreger ou --autotest requis")


if __name__ == "__main__":
    sys.exit(main())
