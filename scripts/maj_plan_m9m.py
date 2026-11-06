#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9m.py — LA CONSIGNATION DU PLAN au geste « LE SECOND RUN TERRAIN
(f) REÇU : LE JOURNAL SEUL, LE RUN INTERROMPU SANS VERDICT — T0/T1/T2 VERT
(la réparation de l'erratum n° 6 PROUVÉE sur la machine réelle, le VRAI
afd.sys franchi pour la première fois) ; le geste rendu au développeur » :
la rangée (f) reçoit le constat du second run interrompu, l'État du
programme reçoit la phrase du geste (le run complet attendu). Rejeu REFUSÉ ;
tout ancrage absent ou compté autrement qu'UNE fois = ÉCHEC NOMMÉ, rien
n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

# --- la rangée (f) : le constat du second run INTERROMPU, AVANT la colonne
# du critère ------------------------------------------------------------------------

ANCIEN_RANGEE = ("LE SECOND GESTE DU DÉVELOPPEUR ATTENDU — si vert : la "
                 "finale 1.0.0, le jalon M9 franchi** | run terrain VERT sur "
                 "pièces")

NOUVELLE_RANGEE = (
    "LE SECOND GESTE DU DÉVELOPPEUR ATTENDU — si vert : la finale 1.0.0, le "
    "jalon M9 franchi** ; **LE SECOND RUN REÇU le 06/11/2026 au soir (Entrée "
    "181, Task 99) : LE JOURNAL SEUL, LE RUN INTERROMPU SANS VERDICT — "
    "T0/T1/T2 VERT NOMMÉS** (16:56:09 : T1 VERT — LA RÉPARATION DE "
    "L'ERRATUM n° 6 PROUVÉE SUR LA MACHINE RÉELLE, le refus -3 ne s'est pas "
    "représenté, les DEUX lecteurs d'accord sur les TROIS SSN ; T2 VERT — "
    "LE VRAI afd.sys FRANCHI POUR LA PREMIÈRE FOIS : l'endpoint TCP vers "
    "www.cloudflare.com:443 ÉTABLI par sys-04 en TROIS appels NT, zéro "
    "ws2_32 : le plus loin du programme sur le terrain) ; LA MORT "
    "SILENCIEUSE entre T2 VERT et la ligne « T3 : OUVRIR » (journalée AVANT "
    "l'appel TLS27 — entre les deux : UN SEGMENT PYTHON PUR dont la "
    "première instruction est UN PRINT CONSOLE, AUCUN appel machine en vol ; "
    "le témoin/le verdict jamais nés : COHÉRENTS avec le dépôt ; le journal "
    "171 o natif CRLF == la ré-écriture EXACTE des trois lignes) ; LE KIT "
    "ACQUITTÉ PAR ÉLIMINATION (aucun octet du kit ne court dans la fenêtre "
    "de mort, le premier run avait traversé tous les prints jusqu'au "
    "verdict sur la MÊME console — kit du /test relu 7d5380ce…, artefact "
    "d8928934… INTACT, scénario == la source octet pour octet) ; LES "
    "CANDIDATS : la console gelée (QuickEdit — ÉCHAP REPREND le run là où "
    "il s'est tu) ou la mort du processus (RELANCER) — la pièce ne tranche "
    "pas, la console du développeur répond ; un « -7 LE TRANSPORT EN ÉCHEC » "
    "après reprise serait POSSIBLE ET HONNÊTE (la connexion muette depuis "
    "16:56 a pu être refermée) ; LE GESTE RENDU : reprendre ou relancer → "
    "preuves-m9f/ ENTIER au coffre → le recoup (D138/D145/D148) → si vert : "
    "la finale 1.0.0, le jalon M9 franchi — LE RUN COMPLET ATTENDU** | run "
    "terrain VERT sur pièces")

# --- l'État du programme : la phrase du geste APRÈS celle du premier run -------------

ANCIEN_ETAT = ("le jalon M9 franchi — LA GRANDE ŒUVRE** Les chantiers "
               "M6-(a)")

NOUVEL_ETAT = ("le jalon M9 franchi — LA GRANDE ŒUVRE** **LE SECOND RUN (f) "
               "REÇU ET ANALYSÉ le 06/11/2026 au soir (Entrée 181, Task 99) "
               ": LE JOURNAL SEUL, LE RUN INTERROMPU SANS VERDICT — LE PLUS "
               "LOIN DU PROGRAMME SUR LE TERRAIN** (T0/T1/T2 VERT à "
               "16:56:09 : LA RÉPARATION DE L'ERRATUM n° 6 PROUVÉE SUR LA "
               "MACHINE RÉELLE [le kit corrigé 7d5380ce… exécuté, le refus "
               "-3 ne s'est pas représenté, les DEUX lecteurs d'accord sur "
               "les TROIS SSN] ; LE VRAI afd.sys FRANCHI POUR LA PREMIÈRE "
               "FOIS [l'endpoint TCP vers www.cloudflare.com:443 ÉTABLI par "
               "sys-04 en TROIS appels NT, zéro ws2_32]) ; LA MORT "
               "SILENCIEUSE entre T2 VERT et la ligne « T3 : OUVRIR » — une "
               "fenêtre PYTHON PUR (le print d'entête T3, os.urandom, "
               "l'échelle x25519, les rappels ctypes, les tampons) dont la "
               "première instruction est UN PRINT CONSOLE, AUCUN appel "
               "machine en vol ; le témoin/le verdict jamais nés "
               "[COHÉRENTS : _verdict() les écrit à la fin] ; le journal "
               "171 o natif CRLF == la ré-écriture EXACTE des trois lignes "
               "[reconstituée octet pour octet] ; l'horloge des pièces "
               "[mtime 16:56:09.463 == la seconde de T2, dépôt Drive "
               "16:56:34 : à 16:56:34 le run était déjà gelé ou mort] ; LE "
               "KIT ACQUITTÉ PAR ÉLIMINATION [la fenêtre ne porte AUCUN "
               "octet du kit, le premier run avait traversé tous les prints "
               "sur la MÊME console — kit relu 7d5380ce…, artefact "
               "d8928934… INTACT, scénario == la source] ; LES CANDIDATS "
               "NOMMÉS : la console gelée [QuickEdit — ÉCHAP reprend] ou la "
               "mort du processus [relancer] — le journal seul ne départage "
               "pas, la console du développeur répond ; LE GESTE RENDU : "
               "reprendre ou relancer → preuves-m9f/ ENTIER → le recoup → "
               "si vert : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE** "
               "Les chantiers M6-(a)")


def main():
    if not PLAN.exists():
        sys.exit("ÉCHEC : plan introuvable")
    plan = PLAN.read_text(encoding="utf-8")

    if "LE SECOND RUN REÇU le 06/11/2026" in plan \
            or "LE SECOND RUN (f) REÇU ET ANALYSÉ le 06/11/2026" in plan:
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
    if "LE SECOND RUN REÇU le 06/11/2026 au soir (Entrée 181, Task 99)" \
            not in plan:
        sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat du second "
                 "run après remplacement")
    if "LE SECOND RUN (f) REÇU ET ANALYSÉ le 06/11/2026 au soir" not in plan:
        sys.exit("ÉCHEC : l'État du programme ne porte pas la phrase du "
                 "second run après remplacement")
    PLAN.write_text(plan, encoding="utf-8")

    relu = PLAN.read_text(encoding="utf-8")
    if relu.count("LE SECOND RUN REÇU le 06/11/2026") != 1 \
            or relu.count("LE SECOND RUN (f) REÇU ET ANALYSÉ") != 1:
        sys.exit("ÉCHEC : relecture — les phrases du geste ne sont pas "
                 "chacune UNIQUES")
    print("[plan] rangée (f) : le constat du second run INTERROMPU déposé "
          "(T0/T1/T2 VERT nommés, la mort silencieuse nommée, le geste "
          "rendu)")
    print("[plan] État du programme : la phrase du geste déposée (le run "
          "complet attendu — si vert : la finale 1.0.0)")
    print("[plan] la relecture fait foi : les DEUX ancrages remplacés, "
          "chacune UNIQUE — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
