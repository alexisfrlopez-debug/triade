#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cristallisation.py — m8qc10sxg LE GESTE SUIVANT : LES DIX REBUILDS
bit-identiques (le générateur déterministe — aucun timestamp, aucun
aléa, les entrées triées) + LE SCAN DE SECRETS des fragments au
contrôle négatif planté (un ghp_ planté DOIT être attrapé).

Sortie : registres/cristallisation.txt (les dix empreintes, le verdict
bit-identique, le scan vert, le négatif attrapé).
"""
from __future__ import annotations

import hashlib
import pathlib
import shutil
import subprocess
import sys
import tempfile

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parents[0]      # le dépôt (le parent de l'atelier)
ORDRE = ["AGENT-CORE", "QUICKSTART", "DEVELOPER_GUIDE", "TROUBLESHOOTING",
         "SECURITY", "REFERENCE", "DOC-LOC", "DOC-EDIT", "DOC-ADD",
         "DOC-REFUS", "DOC-CEREMONY", "DOC-FEEDBACK", "CAPABILITY_PROBE"]
SORTIES = ([f"fragments/{n}.md" for n in ORDRE]
           + [f"fragments-fr/{n}.md" for n in ORDRE]
           + ["MANIFESTE-fragments.txt", "registres/budgets-complet.json"])


def empreinte_arbre() -> str:
    lignes = []
    for rel in SORTIES:
        p = ICI / rel
        assert p.exists(), f"la sortie attendue manque : {rel}"
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        lignes.append(f"{h}  {rel}")
    arbre = hashlib.sha256("\n".join(lignes).encode()).hexdigest()
    return arbre, lignes


def main() -> int:
    rapport = ["LA CRISTALLISATION — m8qc10sxg (le geste suivant) : DIX "
               "REBUILDS bit-identiques", ""]
    empreintes = []
    for i in range(10):
        r = subprocess.run([sys.executable, "generer_fragments.py"],
                           cwd=ICI, capture_output=True, text=True)
        if r.returncode != 0:
            print("[cristallisation] REFUS : le générateur a échoué à la "
                  f"passe {i+1} : {r.stderr[:200]}")
            return 1
        arbre, _ = empreinte_arbre()
        empreintes.append(arbre)
        rapport.append(f"passe {i+1:2d} : {arbre}")
    identiques = len(set(empreintes)) == 1
    rapport.append("")
    if identiques:
        rapport.append("VERDICT : LES DIX PASSES BIT-IDENTIQUES "
                       f"({empreintes[0]}) — l'archive est déterministe")
    else:
        rapport.append("VERDICT : REFUS — les passes divergent "
                       "(l'archive n'est pas déterministe)")
        print("\n".join(rapport))
        return 1

    # LE SCAN DE SECRETS des 26 fragments + le MANIFESTE
    fichiers = [str(ICI / f"fragments/{n}.md") for n in ORDRE] + \
               [str(ICI / f"fragments-fr/{n}.md") for n in ORDRE] + \
               [str(ICI / "MANIFESTE-fragments.txt")]
    r = subprocess.run([sys.executable, str(REPO / "scan_secrets.py")]
                       + fichiers, capture_output=True, text=True)
    scan_vert = r.returncode == 0
    rapport.append(f"LE SCAN DE SECRETS (scan_secrets.py, 27 fichiers) : "
                   f"{'VERT' if scan_vert else 'REFUS — ' + r.stdout[:200]}")

    # LE CONTRÔLE NÉGATIF : un ghp_ planté DOIT être attrapé
    with tempfile.TemporaryDirectory(dir=ICI) as td:
        temoin = pathlib.Path(td) / "PLANTE.md"
        # la forme canonique du jeton : ghp_ + 36 caractères (le motif
        # de la garde — un jeton mal formé n'est pas un témoin)
        temoin.write_text("# témoin\nle jeton planté : ghp_"
                          "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789AB\n",
                          encoding="utf-8")
        r2 = subprocess.run([sys.executable, str(REPO / "scan_secrets.py"),
                             str(temoin)], capture_output=True, text=True)
        negatif_attrape = r2.returncode != 0 and "ghp_" in (
            r2.stdout + r2.stderr)
        rapport.append(f"LE CONTRÔLE NÉGATIF (un ghp_ planté au témoin) : "
                       f"{'ATTRAPÉ' if negatif_attrape else 'NON ATTRAPÉ — REFUS'}")

    (ICI / "registres" / "cristallisation.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))
    ok = identiques and scan_vert and negatif_attrape
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
