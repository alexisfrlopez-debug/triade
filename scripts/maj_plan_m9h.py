#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m9h.py — LA CONSIGNATION DU PLAN au geste « LA REPRISE : LE
CHANTIER M9-(e) OUVERT — LA CÉRÉMONIE DU BUILD 1.0.0 ARMÉE » : la rangée
(e) reçoit le statut OUVERT (le kit de cérémonie déposé et recoupé, le
build attend la remise du développeur). Un remplacement ASSERTÉ — tout
ancrage manquant ou déjà passé = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"

ANCIEN = ("le garde VERT 13/13 AVANT construire() ; l'artefact né déterministe "
          "(sha annoncé par la pièce de vérification par parties détachées) ; "
          "le verrou croisé à la nouvelle génération |")

NOUVEAU = (
    "le garde VERT 13/13 AVANT construire() ; l'artefact né déterministe "
    "(sha annoncé par la pièce de vérification par parties détachées) ; "
    "le verrou croisé à la nouvelle génération — **OUVERT le 06/11/2026 "
    "(Entrée 177, Task 95) : LE KIT DE CÉRÉMONIE DU BUILD 1.0.0 DÉPOSÉ ET "
    "RECOUPÉ** — la reprise a d'abord SOLDÉ la dette de consignation des "
    "Tasks 93/94 (l'ordre 174<175 du journal RESTAURÉ — le défaut de "
    "inserer_entree_175.py nommé —, l'Entrée 176 déposée depuis le worklog "
    "qui fait foi, l'État du programme + la rangée (d) complétés PAR "
    "SCRIPT) ; la remise fraîche PREPARER : 13 arbres, DEUX empreintes "
    "nouvelles — m8 sys.1 72aadd38… (la révision M9-(d) : README + les "
    "TROIS specs sys-04/05/06, 7 fichiers vivants contre 4 déposés) et "
    "tls13 tls13.1 42559862… (l'erratum n° 2 : README seul) —, les ONZE "
    "autres inchangées (Ed25519 déterministe : re-signer redonne les "
    "signatures déposées) ; LISEZMOI-ceremonie-build-1.0.0.txt ÉCRIT au "
    "kit (le modèle ere-M9 : POURQUOI, CE QUI A CHANGÉ, LA RÈGLE D'OR — "
    "JAMAIS « generer », la clé du 04/11 réutilisée 173fae9c… —, le "
    "PAS-À-PAS, CE QUE CELA DÉBLOQUE) ; maj_kit.py ÉTENDU (RACINE_KIT + "
    "NOTE_D130 réorientée) et REJOUÉ : 1 téléversé (le LISEZMOI), 2 mis "
    "à jour (MANIFESTE.txt + v06/sceau-I/a-signer.txt), 56 inchangés, "
    "59/59 VÉRIFIÉS ALLER-RETOUR md5 + le recoup indépendant (le "
    "a-signer du kit == le local, les DEUX empreintes présentes, le "
    "MANIFESTE orienté) ; LA CÉRÉMONIE DU DÉVELOPPEUR attend sa remise "
    "(signer a-signer.txt hors ligne avec la clé du 04/11, ramener "
    "signatures-I.txt + cle-publique-I.txt au /test du Drive) — le build "
    "suit le garde VERT 13/13 |")


def main():
    if not PLAN.exists():
        sys.exit("ÉCHEC : plan introuvable")
    plan = PLAN.read_text(encoding="utf-8")

    if plan.count(ANCIEN) != 1:
        sys.exit(f"ÉCHEC : l'ancre rangée (e) attendue UNE fois, "
                 f"trouvée {plan.count(ANCIEN)} fois")
    if "OUVERT le 06/11/2026 (Entrée 177, Task 95)" in plan:
        sys.exit("ÉCHEC : la rangée (e) déjà ouverte (rejeu REFUSÉ)")

    plan = plan.replace(ANCIEN, NOUVEAU, 1)

    if plan.count("OUVERT le 06/11/2026 (Entrée 177, Task 95)") != 1:
        sys.exit("ÉCHEC : le statut (e) absent ou dupliqué après "
                 "remplacement — rien n'est écrit")

    PLAN.write_text(plan, encoding="utf-8")
    print("[plan] rangée M9-(e) : OUVERT (Entrée 177, Task 95) — LE KIT DE "
          "CÉRÉMONIE DU BUILD 1.0.0 déposé et recoupé ; la cérémonie du "
          "développeur attend sa remise, le build suit le garde VERT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
