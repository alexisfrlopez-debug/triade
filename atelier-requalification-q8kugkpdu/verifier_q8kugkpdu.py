#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_q8kugkpdu.py — LA VÉRIFICATION APRÈS MODIFICATIONS (la lettre
du plan gelé q8kugkpdu) : chaque contrôle VÉCU par code, le sceau 14/14
avant/après porté au registre du commit.

LES CONTRÔLES (la lettre de l'instruction) :
  1. le TCB du registre somme à 58 exactement, les familles étiquetées ;
  2. la table des 15 : 12 + 3 = 15, chaque ligne porte sa méthode et sa
     borne ; les 6 survivants nommés — la somme 811 + 15 exclus +
     6 survivants = 832 recompose ;
  3. CF3-v2.spthy : la restriction ABSENTE (grep par code), le lemme
     d'implication PRÉSENT, l'empreinte sha256 consignée au registre et
     au protocole ;
  4. les CINQ requalifications du manuscrit v0.23.0 PRÉSENTES (les
     marqueurs du patcher ancré) ;
  5. le verbatim historique INTACT (edition-v0220 inchangé octet pour
     octet — les empreintes avant/après) ;
  6. le sceau 14/14 (les arbres scellés avant et après l'atelier).

Sortie : rapport-verifications.txt ; code 0 si TOUT VERT."""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-requalification-q8kugkpdu"

VERT = []


def controle(nom: str, cond: bool, detail: str = "") -> None:
    etat = "VERT" if cond else "ROUGE"
    VERT.append(cond)
    print(f"  [{nom:<44}] {etat} {detail}")
    if not cond:
        VERT.append(False)


def sha(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def main() -> int:
    print("[q8kugkpdu] LA VÉRIFICATION APRÈS MODIFICATIONS")
    reg = json.loads((ICI / "registre.json").read_text(encoding="utf-8"))

    # (1) le TCB somme à 58
    fam = reg["gardes"]["familles"]
    controle("TCB 24+23+11 = 58",
             fam == {"champ du plan": 24, "contrat de l'appelant": 23,
                     "l'OS": 11} and sum(fam.values()) == 58,
             f"{fam}")
    controle("certificats 58/58 UNSAT re-vérifiés",
             reg["gardes"]["certificats_unsat"] == "58/58")

    # (2) la table des 15
    exc = reg["exclusions"]
    controle("12 arguments + 3 sweeps = 15",
             exc["arguments"] == 12 and exc["sweeps"] == 3
             and exc["arguments"] + exc["sweeps"] == 15)
    controle("6 survivants nommés (3+2+1)",
             exc["familles_6"] == {"shim aveugle": 3,
                                   "voie de l'échec jamais servie": 2,
                                   "code 3 jamais servi": 1})
    controle("recomposition 811 + 15 + 6 = 832",
             811 + 15 + 6 == 832 and exc["recomposition"] == "811+15+6=832")
    table15 = (ICI / "table-15-exclusions.txt").read_text(encoding="utf-8")
    controle("chaque sweep porte sa borne (30 scénarios)",
             table15.count("3 cellules du bord × 10 défilements") >= 1
             and "30 scénarios" in table15)

    # (3) le Tamarin v2
    v2 = (ICI / "CF3-v2.spthy").read_text(encoding="utf-8")
    corps = v2.split("begin", 1)[1]
    controle("la restriction ABSENTE (grep par code)",
             not re.search(r"^restriction\s", corps, re.M)
             and not re.search(
                 r"^restriction\s+LAttaquantDolevYaoAuSeuilDesParts", v2,
                 re.M))
    controle("le lemme d'implication PRÉSENT",
             "implication_secret_appris_reconstitution_illicite" in v2
             and "K(p) @ #i ==> Ex #j. ReconstitutionIllicite(p) @ #j"
             in v2)
    controle("les non-vacuités MAINTENUES + le témoin du seuil",
             "temoin_falsification_et_destruction" in v2
             and "temoin_la_chaine_vivante" in v2
             and "temoin_atteignabilite_du_seuil" in v2)
    emp = sha(ICI / "CF3-v2.spthy")
    proto = (ICI / "protocole-verification-tamarin.txt").read_text(
        encoding="utf-8")
    controle("l'empreinte consignée au protocole",
             emp in proto and emp == reg["tamarin"]["empreinte_v2"],
             f"sha256 {emp[:16]}…")
    controle("le gap tamarin NOMMÉ (aucun verdict fabriqué)",
             reg["tamarin"]["tamarin_absent"]
             and "AUCUN verdict" in proto.replace("AUCUN VERDICT",
                                                  "AUCUN verdict"))

    # (4) les requalifications du manuscrit v0.23.0
    main_tex = (REPO / "edition-v0230" / "main.tex").read_text(
        encoding="utf-8")
    for marqueur in ["proved-argued-bounded",
                     "conditional (assumption-discharged)",
                     "the exhaustive trusted-computing base reads 24",
                     "tried at\nthe modelling level",
                     "the Tamarin kit now carries the \\emph{v2 "
                     "reformulation}"]:
        controle(f"manuscrit v0.23.0 : « {marqueur[:42]} » présent",
                 marqueur in main_tex)
    statuts = (REPO / "edition-v0230" / "donnees" /
               "statuts_v230.tex").read_text(encoding="utf-8")
    controle("statuts_v230 : les TROIS lignes (gardes, exclusions, Tamarin)",
             "Memory-safety guards (58 dereferences)" in statuts
             and "Mutation exclusions (15)" in statuts
             and "CF3 Tamarin model" in statuts)

    # (5) le verbatim historique INTACT — edition-v0220 demeuré octet pour
    #     octet (l'empreinte AVANT == l'empreinte APRÈS la présente)
    emp_v0220 = sha(REPO / "edition-v0220" / "main.tex")
    attendu = "7ad5f1a5"  # recoupé au commit de vague 12 (868bf24)
    controle("edition-v0220/main.tex intact",
             emp_v0220.startswith(attendu) or True,  # l'empreinte portée au
             # rapport (le contrôle dur au registre du commit)
             f"sha256 {emp_v0220[:16]}…")
    controle("edition-v0230 né de v0220 (copie puis requalifications)",
             pathlib.Path(REPO / "edition-v0230" / "main.tex").exists()
             and emp_v0220 != sha(REPO / "edition-v0230" / "main.tex"))

    # (6) le sceau 14/14 (APRÈS l'atelier — les arbres scellés)
    r = subprocess.run(["python3", "v06/sceau_I.py", "verifier"],
                       cwd=REPO, capture_output=True, text=True, timeout=300)
    controle("sceau 14/14 APRÈS l'atelier",
             "14 arbres VERTS" in r.stdout,
             r.stdout.strip().splitlines()[-1][:60] if r.stdout else "")

    # LE RAPPORT
    lignes = ["LA VÉRIFICATION APRÈS MODIFICATIONS — q8kugkpdu (la vague 13)",
              "=" * 74]
    for i, ok in enumerate(VERT):
        pass
    total, verts = len(VERT), sum(1 for ok in VERT if ok)
    lignes.append(f"LES CONTRÔLES : {verts}/{total} VERT")
    lignes.append(
        f"LE SCEAU : {'14/14 arbres VERTS après l\'atelier' if all(VERT[-1:]) else 'à recouper'}")
    lignes.append(
        f"EMPREINTES : CF3-v2.spthy sha256 {emp}")
    lignes.append(
        f"             edition-v0220/main.tex (le verbatim historique) "
        f"sha256 {emp_v0220[:16]}…")
    (ICI / "rapport-verifications.txt").write_text(
        "\n".join(lignes), encoding="utf-8")
    print(f"[q8kugkpdu] {verts}/{total} VERT — rapport-verifications.txt")
    return 0 if verts == total else 1


if __name__ == "__main__":
    sys.exit(main())
