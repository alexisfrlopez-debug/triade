#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9n.py — LA CONSIGNATION DU PLAN au geste « LA CONSOLE DU
DÉVELOPPEUR REÇUE : LE CRASH DU SECOND RUN NOMMÉ — L'ERRATUM n° 7 DU KIT
(TROIS FAUTES DANS LE SEGMENT PYTHON PUR), L'ACQUITTEMENT DE L'ENTRÉE 181
RENVERSÉ PAR LA PIÈCE ; LE KIT RÉPARÉ + LE CONTRÔLE PERMANENT, MIS À JOUR EN
PLACE AU COFFRE » : la rangée (f) reçoit le constat de l'erratum n° 7, l'État
du programme reçoit la phrase du geste (le TROISIÈME run attendu). Rejeu
REFUSÉ ; tout ancrage absent ou compté autrement qu'UNE fois = ÉCHEC NOMMÉ,
rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

# --- la rangée (f) : le constat de L'ERRATUM n° 7 APRÈS celui du second run
# interrompu, AVANT la colonne du critère ---------------------------------------

ANCIEN_RANGEE = ("LE RUN COMPLET ATTENDU** | run terrain VERT sur pièces")

NOUVELLE_RANGEE = (
    "LE RUN COMPLET ATTENDU** ; **LE CRASH DU SECOND RUN NOMMÉ SUR LA CONSOLE "
    "le 07/11/2026 (Entrée 182, Task 100) : L'ERRATUM n° 7 DU KIT — TROIS "
    "FAUTES DANS LE SEGMENT PYTHON PUR, l'acquittement « par élimination » de "
    "l'Entrée 181 RENVERSÉ PAR LA PIÈCE CONSOLE** (le TypeError ligne 593 "
    "`kit96.raw[:32] = alea` : `.raw` est une copie bytes IMMUABLE — le crash "
    "DÉTERMINISTE sur toute machine, le prompt revenu : ni console gelée ni "
    "mort inexpliquée ; la « clé publique attendue » imprimée NULLE 000…0 : "
    "x_3 né à 0 [le point à l'infini] et a24 = (p+1)//4 [la fausse courbe] — "
    "le recoup T3 eût été IMPOSSIBLE ; les DEUX sites OUVRIR passaient la "
    "TAILLE 96 en r9 où tls13-27 P2 É1 exige LE POINTEUR des 96 o : la "
    "machine eût lu à l'adresse 0x60 — la faute (3) devancée de quatre lignes "
    "par la faute (1), toutes deux dans le MÊME segment Python pur, aucune "
    "machine en vol) ; LA RÉPARATION À LA SOURCE (les 96 o posés EN UN GESTE "
    "par create_string_buffer ; r9 = ctypes.addressof(kit96|kit96_2) aux "
    "DEUX sites ; l'échelle == le pseudocode officiel RFC 7748 § 5 == la "
    "référence du dépôt) + LE CONTRÔLE PERMANENT aux TROIS portes à "
    "l'assemblage (preuve négative sur la pointe 35706ef : les TROIS refus "
    "nommés — la porte 1 NOMME la ligne 593) ; le kit corrigé md5 90a1d022… "
    "MIS À JOUR EN PLACE au /test, le second run archivé → archives-preuves/"
    "preuves-run-m9f-2/ AVEC la pièce console et le verdict du recoup "
    "(12/12) ; l'artefact INTACT (relu VERT au T0 du run mort lui-même), le "
    "terrain LAVÉ (les acquis de l'Entrée 181 demeurent : l'erratum n° 6 "
    "prouvé réparé, LE VRAI afd.sys franchi) ; LE TROISIÈME GESTE ATTENDU — "
    "si vert : la finale 1.0.0, le jalon M9 franchi** | run terrain VERT sur "
    "pièces")

# --- l'État du programme : la phrase du geste APRÈS celle du second run --------

ANCIEN_ETAT = ("LA GRANDE ŒUVRE** Les chantiers M6-(a)")

NOUVEL_ETAT = ("LA GRANDE ŒUVRE** **L'ERRATUM n° 7 DU KIT NOMMÉ ET RÉPARÉ le "
               "07/11/2026 (Entrée 182, Task 100) : le second run (06/11 "
               "16:56) est MORT d'un crash PYTHON DÉTERMINISTE nommé sur la "
               "console du développeur — l'acquittement « par élimination » "
               "de l'analyse du journal seul RENVERSÉ PAR LA PIÈCE CONSOLE** "
               "(TypeError ligne 593 `kit96.raw[:32] = alea` : `.raw` est une "
               "copie bytes IMMUABLE ; la « clé attendue » imprimée NULLE "
               "000…0 : x_3 né à 0, a24 = (p+1)//4 ; la TAILLE au lieu du "
               "POINTEUR aux DEUX sites OUVRIR — la machine eût lu à "
               "l'adresse 0x60) ; T0/T1/T2 VERT demeurent (le terrain LAVÉ, "
               "l'artefact INTACT relu au T0 du run mort lui-même, LE VRAI "
               "afd.sys franchi pour la première fois) ; la réparation À LA "
               "SOURCE + LE CONTRÔLE PERMANENT aux TROIS portes "
               "(assembler_kit_m9f.py [2c], preuve négative 6/6 sur la pointe "
               "35706ef : les TROIS refus nommés) ; le kit corrigé md5 "
               "90a1d022… EN PLACE au /test, le run 2 archivé AVEC la pièce "
               "console → archives-preuves/preuves-run-m9f-2/ ; LE TROISIÈME "
               "RUN ATTENDU — si vert : LA FINALE 1.0.0, LE JALON M9 — LA "
               "GRANDE ŒUVRE** Les chantiers M6-(a)")


def main():
    if not PLAN.exists():
        sys.exit("ÉCHEC : plan introuvable")
    plan = PLAN.read_text(encoding="utf-8")

    if "L'ERRATUM n° 7 DU KIT — TROIS" in plan \
            or "L'ERRATUM n° 7 DU KIT NOMMÉ ET RÉPARÉ" in plan:
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
    if "LE CRASH DU SECOND RUN NOMMÉ SUR LA CONSOLE le 07/11/2026" \
            not in plan:
        sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat de "
                 "l'erratum n° 7 après remplacement")
    if "L'ERRATUM n° 7 DU KIT NOMMÉ ET RÉPARÉ le 07/11/2026" not in plan:
        sys.exit("ÉCHEC : l'État du programme ne porte pas la phrase de "
                 "l'erratum n° 7 après remplacement")
    PLAN.write_text(plan, encoding="utf-8")

    relu = PLAN.read_text(encoding="utf-8")
    if relu.count("LE CRASH DU SECOND RUN NOMMÉ SUR LA CONSOLE") != 1 \
            or relu.count("L'ERRATUM n° 7 DU KIT NOMMÉ ET RÉPARÉ") != 1:
        sys.exit("ÉCHEC : relecture — les phrases du geste ne sont pas "
                 "chacune UNIQUES")
    print("[plan] rangée (f) : le constat de l'erratum n° 7 déposé (les "
          "TROIS fautes nommées, l'acquittement renversé, le kit corrigé "
          "en place)")
    print("[plan] État du programme : la phrase du geste déposée (le "
          "TROISIÈME run attendu — si vert : la finale 1.0.0)")
    print("[plan] la relecture fait foi : les DEUX ancrages remplacés, "
          "chacune UNIQUE — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
