#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9p.py — LA CONSIGNATION DU PLAN au geste « LE TROISIÈME RUN
TERRAIN (f) REÇU : ROUGE T3.ouvrir NOMMÉ — MAIS LE RECOUP DU JALON VERT (le
ClientHello de LA MACHINE == la référence octet pour octet) ET LA RÉPARATION
DE L'ERRATUM n° 7 PROUVÉE ; le kit ACQUITTÉ, le run archivé AVEC le verdict
du recoup 26/26 — LA RELANCE EST LE GESTE SUIVANT » : la rangée (f) reçoit le
constat du troisième run, l'État du programme reçoit la phrase du geste (la
relance attendue). Rejeu REFUSÉ ; tout ancrage absent ou compté autrement
qu'UNE fois = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

# --- la rangée (f) : le constat du TROISIÈME run, AVANT la colonne du
# critère -------------------------------------------------------------------------

ANCIEN_RANGEE = ("LE TROISIÈME GESTE ATTENDU — si vert : la finale 1.0.0, le "
                 "jalon M9 franchi** | run terrain VERT sur pièces")

NOUVELLE_RANGEE = (
    "LE TROISIÈME GESTE ATTENDU — si vert : la finale 1.0.0, le jalon M9 "
    "franchi** ; **LE TROISIÈME RUN REÇU le 06/11/2026 au soir (Entrée 183, "
    "Task 101) : ROUGE T3.ouvrir NOMMÉ — MAIS LE RECOUP DU JALON VERT** (le "
    "run 18:49:34, SIX MINUTES après le dépôt du kit corrigé : T0/T1/T2 "
    "VERT, LA RÉPARATION DE L'ERRATUM n° 7 PROUVÉE [la clé publique attendue "
    "NON-NULLE 89d50a86…], **LE ClientHello COMPOSÉ PAR LA MACHINE == LA "
    "RÉFÉRENCE OCTET POUR OCTET — 119 o : LA PREUVE CRYPTOGRAPHIQUE DU "
    "JALON SUR LA MACHINE RÉELLE, les DEUX lecteurs d'accord tls13-14 == "
    "l'échelle Python** ; la mort NOMMÉE : sys-05 rend -6 à SON PREMIER "
    "APPEL RÉEL [l'émission du CH refusée — UNE SEULE émission tentée, la "
    "preuve en une ligne : la ligne « dernière émission » absente du "
    "témoin] → -7 LE TRANSPORT EN ÉCHEC, état 5 [le NTSTATUS vit dans rdx, "
    "la limite NOMMÉE de l'instrument] ; LE KIT ACQUITTÉ [INCHANGÉ "
    "90a1d022…], la frontière nommée d'avance [l'artefact contre le VRAI "
    "afd.sys — les mesures viennent de Windows 11, les runs ont lieu sur "
    "Windows 10 22H2] ; le run archivé → preuves-run-m9f-3/ AVEC le "
    "VERDICT-recoup-labo-m9f-3.txt [ROUGE CONSTATÉ COHÉRENT 26/26] ; LA "
    "RELANCE ATTENDUE — un réseau vivant distingue le passager du "
    "structurel ; si le -6 se répète à l'identique à l'émission du CH : la "
    "divergence afd.sys Win10 ↔ Win11 devient le suspect principal [une "
    "machine Windows 11, ou la sonde sys-05 au labo — le chantier futur "
    "nommé])** | run terrain VERT sur pièces")

# --- l'État du programme : la phrase du geste APRÈS celle de l'erratum n° 7 ------

ANCIEN_ETAT = ("LE TROISIÈME RUN ATTENDU — si vert : LA FINALE 1.0.0, LE "
               "JALON M9 — LA GRANDE ŒUVRE** Les chantiers M6-(a)")

NOUVEL_ETAT = ("LE TROISIÈME RUN ATTENDU — si vert : LA FINALE 1.0.0, LE "
               "JALON M9 — LA GRANDE ŒUVRE** **LE TROISIÈME RUN (f) REÇU ET "
               "RECROPÉ le 06/11/2026 au soir (Entrée 183, Task 101) : LE "
               "PLUS LOIN DU PROGRAMME — L'OFFRE DE LA MACHINE PARFAITE SUR "
               "PIÈCES, LE RECOUP DU JALON VERT** (le ClientHello composé "
               "par LES BLOCS SCELLÉS == la référence octet pour octet, "
               "119 o — les DEUX lecteurs d'accord [tls13-14 == l'échelle "
               "Python], LA PREUVE CRYPTOGRAPHIQUE DU JALON SUR LA MACHINE "
               "RÉELLE ; la réparation de l'erratum n° 7 PROUVÉE [la clé "
               "attendue NON-NULLE 89d50a86…, le segment du run 2 traversé "
               "vivant, la machine appelée au pointeur] ; la mort NOMMÉE à "
               "sys-05 : -6 à SON PREMIER APPEL RÉEL [l'émission du CH "
               "refusée, UNE SEULE émission tentée — la preuve en une "
               "ligne] → -7 LE TRANSPORT EN ÉCHEC, état 5 [le NTSTATUS vit "
               "dans rdx : la limite nommée de l'instrument] ; LE KIT "
               "ACQUITTÉ [INCHANGÉ 90a1d022…] et la frontière nommée "
               "d'avance [l'artefact contre le VRAI afd.sys : sys-05 "
               "n'avait JAMAIS couru sur le vrai noyau, le labo n'a que le "
               "modèle] ; le run archivé → preuves-run-m9f-3/ avec le "
               "verdict du recoup 26/26) ; LA RELANCE DU DÉVELOPPEUR EST LE "
               "GESTE SUIVANT — un réseau vivant distingue le passager du "
               "structurel ; si le -6 se répète à l'identique : la "
               "divergence afd.sys Windows 10 ↔ Windows 11 devient le "
               "suspect principal (une machine Windows 11, ou la sonde "
               "sys-05 au labo) — et si le vert tient : LA FINALE 1.0.0, "
               "LE JALON M9 — LA GRANDE ŒUVRE** Les chantiers M6-(a)")


def main():
    if not PLAN.exists():
        sys.exit("ÉCHEC : plan introuvable")
    plan = PLAN.read_text(encoding="utf-8")

    if "LE TROISIÈME RUN REÇU le 06/11/2026" in plan \
            or "LE TROISIÈME RUN (f) REÇU ET RECROPÉ" in plan:
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

    if "LE TROISIÈME RUN REÇU le 06/11/2026 au soir (Entrée 183" \
            not in plan:
        sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat du "
                 "troisième run après remplacement")
    if "LE TROISIÈME RUN (f) REÇU ET RECROPÉ le 06/11/2026" not in plan:
        sys.exit("ÉCHEC : l'État du programme ne porte pas la phrase du "
                 "troisième run après remplacement")
    PLAN.write_text(plan, encoding="utf-8")

    relu = PLAN.read_text(encoding="utf-8")
    if relu.count("LE TROISIÈME RUN REÇU le 06/11/2026") != 1 \
            or relu.count("LE TROISIÈME RUN (f) REÇU ET RECROPÉ") != 1:
        sys.exit("ÉCHEC : relecture — les phrases du geste ne sont pas "
                 "chacune UNIQUES")
    print("[plan] rangée (f) : le constat du troisième run déposé (le "
          "recoup du jalon VERT, la mort nommée à sys-05, la relance "
          "attendue)")
    print("[plan] État du programme : la phrase du geste déposée (le plus "
          "loin du programme — l'offre de la machine parfaite sur pièces)")
    print("[plan] la relecture fait foi : les DEUX ancrages remplacés, "
          "chacune UNIQUE — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
