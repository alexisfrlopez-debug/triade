#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9k.py — LA CONSIGNATION DU PLAN au geste « LE PREMIER RUN
TERRAIN (f) RECROPÉ : ROUGE T1.la-résolution NOMMÉ — L'ERRATUM n° 6 du kit
réparé à la source, le kit corrigé ré-déposé » : la rangée (f) reçoit le
constat du premier run + la correction, l'État du programme reçoit la
phrase du geste (le second geste du développeur attendu). Rejeu REFUSÉ ;
tout ancrage absent ou compté autrement qu'UNE fois = ÉCHEC NOMMÉ, rien
n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

# --- la rangée (f) : le constat du premier run + la correction, AVANT la
# colonne du critère -----------------------------------------------------------------

ANCIEN_RANGEE = ("le témoin « HTTP/1.1 200 OK » | run terrain VERT sur "
                 "pièces")

NOUVELLE_RANGEE = (
    "le témoin « HTTP/1.1 200 OK » ; **LE PREMIER RUN REÇU ET RECROPÉ le "
    "06/11/2026 au soir (Entrée 180, Task 98) : ROUGE `T1.la-résolution` "
    "NOMMÉ — L'ERRATUM n° 6 du kit (T1 passait la base de L'ARTEFACT aux "
    "lecteurs de SSN au lieu de `ntdll_base` : proxy.exe n'a PAS de "
    "répertoire export, le refus -3 « répertoire export absent » INÉVITABLE "
    "sur toute machine — LA FAUTE AU LABO, jamais au terrain) ; le terrain "
    "LAVÉ par le recoup 25/25 sur pièces croisées (D138/D145/D148 : le "
    "VRAI ntdll localisé et haché 36b1a62e…, l'artefact relu INTACT "
    "d8928934…, le scénario exécuté fidèlement octet pour octet, les "
    "SEIZE T0 verts) ; RÉPARÉ À LA SOURCE (les TROIS sites de résolution "
    "reçoivent `ntdll_base`) + LE CONTRÔLE PERMANENT à l'assemblage "
    "(assembler_kit_m9f.py [2b] : l'AST exige `ntdll_base` aux trois "
    "lecteurs — contrôle négatif PROUVÉ sur la source pré-réparation : "
    "REFUS) ; kit-m9f.zip MIS À JOUR EN PLACE au /test (md5 7d5380ce… "
    "MATCH relu, le LISEZMOI porte l'erratum) ; le run ROUGE archivé "
    "(preuves-run-m9f/ aux archives-preuves AVEC le VERDICT-recoup-labo — "
    "l'archive porte le jugement), preuves-m9f/ ré-armé ; NOTE "
    "d'environnement : le run a eu lieu sur Windows 10 22H2 build 19045 "
    "(le kit vise Windows 11 : si afd.sys diverge, le refus sera NOMMÉ) ; "
    "LE SECOND GESTE DU DÉVELOPPEUR ATTENDU — si vert : la finale 1.0.0, "
    "le jalon M9 franchi** | run terrain VERT sur pièces")

# --- l'État du programme : la phrase du geste APRÈS celle du kit déposé --------------

ANCIEN_ETAT = ("si vert : la finale 1.0.0, le jalon M9 franchi** Les "
               "chantiers M6-(a)")

NOUVEL_ETAT = ("si vert : la finale 1.0.0, le jalon M9 franchi** "
               "**LE PREMIER RUN (f) RECROPÉ le 06/11/2026 au soir (Entrée "
               "180, Task 98) : ROUGE T1.la-résolution NOMMÉ — L'ERRATUM "
               "n° 6 du kit** (T1 passait la base de L'ARTEFACT aux "
               "lecteurs de SSN au lieu de `ntdll_base` : proxy.exe sans "
               "répertoire export, le refus -3 « répertoire export absent » "
               "INÉVITABLE sur toute machine — la faute AU LABO, jamais au "
               "terrain ; le recoup 25/25 sur pièces croisées : le VRAI "
               "ntdll haché 36b1a62e…, l'artefact relu INTACT, le scénario "
               "exécuté fidèlement octet pour octet, les SEIZE T0 verts, "
               "Windows 10 22H2 build 19045 + Python 3.14.6 AMD64 "
               "consignés) ; RÉPARÉ à la source [les trois sites reçoivent "
               "`ntdll_base`] + le contrôle PERMANENT à l'assemblage [l'AST "
               "exige `ntdll_base` aux trois lecteurs — contrôle négatif "
               "PROUVÉ : la source pré-réparation est REFUSÉE] ; "
               "kit-m9f.zip MIS À JOUR EN PLACE au /test [md5 7d5380ce… "
               "MATCH relu, le LISEZMOI porte l'erratum] ; le run ROUGE "
               "archivé [preuves-run-m9f/ + le VERDICT-recoup-labo : "
               "l'archive porte le jugement], preuves-m9f/ ré-armé ; LE "
               "SECOND GESTE DU DÉVELOPPEUR ATTENDU — si vert : la finale "
               "1.0.0, le jalon M9 franchi — LA GRANDE ŒUVRE** Les "
               "chantiers M6-(a)")


def main():
    if not PLAN.exists():
        sys.exit("ÉCHEC : plan introuvable")
    plan = PLAN.read_text(encoding="utf-8")

    if "LE PREMIER RUN REÇU ET RECROPÉ le 06/11/2026" in plan \
            or "LE PREMIER RUN (f) RECROPÉ le 06/11/2026" in plan:
        sys.exit("ÉCHEC : la rangée (f)/l'État sont déjà à jour "
                 "(rejeu REFUSÉ)")
    if plan.count(ANCIEN_RANGEE) != 1:
        sys.exit(f"ÉCHEC : ancrage rangée (f) trouvé "
                 f"{plan.count(ANCIEN_RANGEE)} fois (attendu : 1)")
    if plan.count(ANCIEN_ETAT) != 1:
        sys.exit(f"ÉCHEC : ancrage État du programme trouvé "
                 f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")

    plan = plan.replace(ANCIEN_RANGEE, NOUVELLE_RANGEE, 1)
    plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)

    # la relecture fait foi : les DEUX remplacements constatés AVANT écriture
    if "LE PREMIER RUN REÇU ET RECROPÉ le 06/11/2026 au soir (Entrée 180, " \
            "Task 98)" not in plan:
        sys.exit("ÉCHEC : la rangée (f) n'a pas suivi (constat AVANT écriture)")
    if "LE PREMIER RUN (f) RECROPÉ le 06/11/2026 au soir (Entrée 180, " \
            "Task 98)" not in plan:
        sys.exit("ÉCHEC : l'État du programme n'a pas suivi (constat AVANT "
                 "écriture)")

    PLAN.write_text(plan, encoding="utf-8")
    print("[plan] la rangée (f) : LE PREMIER RUN RECROPÉ — ROUGE T1 nommé, "
          "l'erratum n° 6 réparé à la source, le kit corrigé ré-déposé, le "
          "second geste attendu")
    print("[plan] l'État du programme : la phrase du geste déposée après "
          "celle du kit déposé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
