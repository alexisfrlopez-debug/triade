#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consigner l'Entrée 220 + le worklog Task 127 — PAR SCRIPT (la vérification
post-clôture : le jalon M10 franchi, les constats de la session, la passation
D13 du geste, la suite au développeur). Aucune décision nouvelle : la session
n'arbitre rien — le programme d'après M10 demeure au développeur (D178)."""

import os

R = "/home/z/my-project/triade"

ENTREE_220 = """## Entrée 220 — « continue » : LA VÉRIFICATION POST-CLÔTURE DU JALON M10 — L'ÉTAT CONSTATÉ VERT, LA PASSATION D13 PARACHÉVÉE, LA SUITE AU DÉVELOPPEUR (11/11)

**Le fait.** Le message du développeur « continue » ouvrit la présente session SUR LE JALON CLOS : l'Entrée 219 avait consigné la clôture complémentaire (D178 — M10 FRANCHI, la balise `loupe 0.1.0` SCELLÉE) et la passation D141 (a707a4f). La session ne rouvre RIEN : elle CONSTATE l'état, parachevait la règle D13 (le sync du dernier commit — le hook post-commit de a707a4f avait couru à 17:58:32, la fin de session put l'interrompre), et consigne.

**Les constats (l'état vérifié, pièce à pièce).** (1) LE DÉPÔT : l'arbre PROPRE à a707a4f, origin/main == la pointe (le push avait vécu) ; (2) LES CONSIGNATIONS : l'Entrée 218 (le scellage, la pointe canonique 66fa17c), l'Entrée 219 (la clôture complémentaire), D178, le PLAN clos (la rangée (e) + l'État du programme — M10 FRANCHI en tête), le worklog Task 125/126 — TOUT y vit ; (3) LA CHAÎNE SOUS LA BALISE : re-vérifiée VERTE à la clôture même (garde 14/14, 78 appels IAT audités, le verrou croisé 26/26, l'artefact DÉTERMINISTE — l'Entrée 219 la consigne) ; (4) LE COFFRE : la passation D141 vécue (le bundle courant triade-history-090-1162003.bundle au miroir, l'ancien 090-a541f4b archivé versionné, /test SANS copie de bundle).

**Le geste de la session (D13, idempotent).** `sync_backup.sh` : le PDF formel régénéré BYTE-STABLE (v0.8.4, sha256 e92689ab… — l'empreinte CONSIGNÉE n°38 au registre D134, la chaîne spec_v084, le contrôle BUILD-NON-DÉTERMINISTE tenu) ; le commit de librairie 6ef8f11 (le stamp rafraîchi + la ligne de build au journal + la rangée du registre — CINQ fichiers, AUCUN octet technique) ; le miroir Drive SYNCHRONISÉ (1650 fichiers, 0 téléversé requis, 0 erreur) ; le kit « Cérémonie » D130 DÉPLOYÉ ET VÉRIFIÉ (60/60 aller-retour md5, MANIFESTE.txt mis à jour) ; le push GitHub — **LES TROIS MIROIRS ALIGNÉS à 6ef8f11** (qui porte a707a4f, la clôture, la balise).

**Frontières.** La balise `loupe 0.1.0` SCELLÉE DEMEURE (l'anti-rollback vivant : construire REFUSÉ) ; loupe.exe INTACT (054de960… — le MÊME binaire que le onzième run) ; les balises sœurs INTACTES (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0) ; AUCUN arbre signé touché, AUCUNE règle modifiée, AUCUNE notation touchée (R2) ; les secrets au seul .keys/ (D12) ; la dette [R10-PÉRIMÉE] DEMEURE NOMMÉE (réparable à 0.1.1+, R4 — la commande au développeur).

**SUITE : LE PROGRAMME D'APRÈS M10 APPARTIENT AU DÉVELOPPEUR** (l'Entrée 219/D178 le posent ; la présente session n'arbitre rien — aucune décision nouvelle consommée) : (a) le projet fils COFFRE-FORT dégeler — D171/D135 amendée ; (b) la consolidation v0.9.0 de la spécification — le modèle D169/D176 (v0.8.4 s'arrête avant le onzième run : la rangée M10 du document attend la consolidation) ; (c) la dette [R10-PÉRIMÉE] — la table des 17 sommes rafraîchie à 0.1.1+, le jour où le développeur commande la version.

"""

WORKLOG_127 = """
---
Task ID: 127
Agent: Z.ai (agent principal)
Task: « continue » — LA VÉRIFICATION POST-CLÔTURE DU JALON M10 : l'état
constaté vert (le dépôt propre à a707a4f, GitHub aligné, les consignations
complètes, la chaîne sous la balise verte, le coffre passé à D141), la
passation D13 parachevée (le commit de librairie 6ef8f11 : PDF byte-stable
consigné n°38, miroir Drive 1650 fichiers 0 erreur, kit D130 60/60, push —
LES TROIS MIROIRS ALIGNÉS), la suite au développeur.

Work Log:
- LES CONSTATS : l'arbre propre à a707a4f == origin/main ; Entrées 218/219,
  D178, le PLAN clos, Tasks 125/126 — tout vit ; la chaîne re-vérifiée
  verte à la clôture (garde 14/14, verrou croisé 26/26, artefact
  déterministe) ; le bundle 090-1162003 au miroir, l'ancien archivé.
- LE GESTE (D13) : sync_backup.sh — le PDF v0.8.4 régénéré BYTE-STABLE
  (e92689ab…, consigné n°38), le commit 6ef8f11 (cinq fichiers de
  librairie, AUCUN octet technique), le miroir Drive 1650/0-erreur, le
  kit 60/60, le push : les TROIS miroirs à 6ef8f11.
- FRONTIÈRES : la balise loupe 0.1.0 scellée demeure, loupe.exe intact
  (054de960…), les balises sœurs intactes, aucune notation touchée, la
  dette [R10-PÉRIMÉE] demeurée nommée (0.1.1+, R4).
- SUITE : LE PROGRAMME D'APRÈS M10 APPARTIENT AU DÉVELOPPEUR — (a) le
  projet fils COFFRE-FORT dégeler (D171/D135 amendée), (b) la
  consolidation v0.9.0 de la spécification (le modèle D169/D176), (c) la
  dette [R10-PÉRIMÉE] à 0.1.1+ (R4, la commande au développeur).
"""


def main() -> int:
    # 1. JOURNAL_TRAVAIL.md — l'Entrée 220 AVANT le marqueur m5a
    chemin = os.path.join(R, "docs", "JOURNAL_TRAVAIL.md")
    texte = open(chemin, encoding="utf-8").read()
    marqueur = "<!-- m5a:journal-des-builds v1"
    idx = texte.index(marqueur)
    if "## Entrée 220" in texte:
        print("[journal] l'Entrée 220 y vit déjà")
    else:
        texte = texte[:idx] + ENTREE_220 + "\n" + texte[idx:]
        open(chemin, "w", encoding="utf-8").write(texte)
        print("[journal] l'Entrée 220 consignée")

    # 2. worklog.md — le Task ID 127 en fin
    chemin = os.path.join(R, "worklog.md")
    texte = open(chemin, encoding="utf-8").read()
    if "Task ID: 127" in texte:
        print("[worklog] le Task ID 127 y vit déjà")
    else:
        open(chemin, "a", encoding="utf-8").write(WORKLOG_127)
        print("[worklog] le Task ID 127 consigné")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
