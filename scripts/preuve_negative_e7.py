#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""preuve_negative_e7.py — LE CONTRÔLE NÉGATIF DU CONTRÔLE PERMANENT
erratum n° 7 : les TROIS portes de l'assembleur (assembler_kit_m9f.py)
confrontées à LA SOURCE PRÉ-RÉPARATION (la pointe git 35706ef — celle du
kit 7d5380ce… que le développeur a exécutée, celle du run mort au
TypeError ligne 593) : CHAQUE porte doit REFUSER, SON refus NOMMÉ — puis
les TROIS portes contre la source RÉPARÉE : AUCUNE ne refuse.

Le modèle du geste : la preuve négative de l'erratum n° 6 (corriger_
kit_m9f.py — « contrôle négatif PROUVÉ sur la source pré-réparation :
3 sites, 0 à ntdll_base → REFUS »). Une garde qui n'a jamais refusé le
coupable n'est pas une garde.

Usage : python3 scripts/preuve_negative_e7.py
Code de sortie : 0 = les TROIS refus ET le passage (la garde est réelle) ;
2 = la garde est muette ou aveugle — ARRÊTER."""

import ast
import pathlib
import subprocess
import sys
import tempfile

REPO = pathlib.Path("/home/z/my-project/triade")
POINTE_PRE = "35706ef"
sys.path.insert(0, str(REPO / "scripts"))
import assembler_kit_m9f as asm  # noqa: E402

REUSSITES, ECHECS = [], []


def controle(nom, ok, detail=""):
    if ok:
        REUSSITES.append(nom)
        print(f"  [ok] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append(nom)
        print(f"  [ÉCHEC] {nom}" + (f" — {detail}" if detail else ""))


def main():
    print("=== LA PREUVE NÉGATIVE DU CONTRÔLE PERMANENT erratum n° 7 ===\n")

    r = subprocess.run(
        ["git", "-C", str(REPO), "show",
         f"{POINTE_PRE}:tls13/terrain/scenario-m9f.py"],
        capture_output=True, check=True)
    pre = pathlib.Path(tempfile.mkdtemp()) / "scenario-pre-e7.py"
    pre.write_bytes(r.stdout)
    arbre_pre = ast.parse(pre.read_text(encoding="utf-8"))
    arbre_repare = ast.parse(
        (REPO / "tls13" / "terrain" / "scenario-m9f.py")
        .read_text(encoding="utf-8"))

    print(f"A — LA SOURCE PRÉ-RÉPARATION (la pointe git {POINTE_PRE}, "
          f"{len(r.stdout)} o)")
    v1 = asm._porte_e7_1_raw(arbre_pre)
    controle("porte 1 refuse (le TypeError du run)",
             v1 is not None and v1[0] == "ERRATUM-7 porte 1"
             and "ligne 593" in v1[1],
             f"« {v1[1][:96]}… »" if v1 else "la porte est muette")
    v2 = asm._porte_e7_2_ouvrir(arbre_pre)
    controle("porte 2 refuse (r9 = la TAILLE aux DEUX sites)",
             v2 is not None and v2[0] == "ERRATUM-7 porte 2",
             f"« {v2[1][:96]}… »" if v2 else "la porte est muette")
    v3 = asm._porte_e7_3_echelle(pre)
    controle("porte 3 refuse (l'échelle NULLE du run)",
             v3 is not None and v3[0] == "ERRATUM-7 porte 3",
             f"« {v3[1][:96]}… »" if v3 else "la porte est muette")

    print("\nB — LA SOURCE RÉPARÉE (les portes demeurent ouvertes au kit "
          "sain)")
    controle("porte 1 passe", asm._porte_e7_1_raw(arbre_repare) is None,
             "AUCUNE écriture `.raw[...]`")
    controle("porte 2 passe", asm._porte_e7_2_ouvrir(arbre_repare) is None,
             "les DEUX sites OUVRIR portent ctypes.addressof(kit…)")
    controle("porte 3 passe",
             asm._porte_e7_3_echelle(
                 REPO / "tls13" / "terrain" / "scenario-m9f.py") is None,
             "l'échelle == les vecteurs officiels du dépôt")

    print(f"\n=== BILAN : {len(REUSSITES)} VERT"
          + (f", {len(ECHECS)} ÉCHEC(S) — la garde est muette ou aveugle, "
             "ARRÊTER" if ECHECS else " — LA GARDE EST RÉELLE : elle a "
             "refusé le coupable, elle passe le kit sain") + " ===")
    return 0 if not ECHECS else 2


if __name__ == "__main__":
    sys.exit(main())
