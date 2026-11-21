#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""purger_d81_semantique.py — LA PURGE DES RÉSIDUS PRESCRIPTIFS D81 AU
PÉRIMÈTRE SÉMANTIQUE (0uug27teo, la vague 12).

LA CAUSE (l'erratum nommé) : la purge ou6wn6wlv (la vague 11) revendiquait
« zéro prescriptive » — EXACTE au périmètre du grep (le motif
« PHRASE-CONTROLE »), INEXACTE au périmètre sémantique : sept résidus
prescriptifs de la garde D81 vivaient encore au Livre v1.6 et à la spec
v0.15.7, sous les tournures « fichier-remise », « remise D81 », « le
fichier est la remise ». LA CAUSE RACINE : le motif du linter dérivait du
NOM DE FICHIER, pas de l'INTENTION de la garde (écrire la phrase au dépôt).

LA MÉTHODE : remplacements ancrés — REFUS si une ancre manque (la méthode
établie). Chaque résidu remplacé par LA GARDE ACTIVE D223 (le séquestre 5/3,
la reconstitution à froid de TROIS parts, la phrase en AUCUN dépôt, le refus
nommé de la réécriture). Les contextes historiques datés DEMEURENT annotés.

AUCUN coffre réel, aucune phrase réelle (D105) — du texte seul."""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
LIVRE = REPO / "scripts" / "livre_v16"
SPEC = REPO / "scripts" / "spec_v157"

R = []


def remplace(chemin: pathlib.Path, ancien: str, nouveau: str, nom: str):
    t = chemin.read_text(encoding="utf-8")
    if ancien not in t:
        print(f"ANCRE MANQUANTE ({chemin.name}) : {nom}")
        sys.exit(2)
    if t.count(ancien) != 1:
        print(f"ANCRE AMBIGUE {t.count(ancien)}x ({chemin.name}) : {nom}")
        sys.exit(2)
    chemin.write_text(t.replace(ancien, nouveau), encoding="utf-8")
    R.append(f"{chemin.name} : {nom}")


# ============ LE LIVRE v1.6 — LES CINQ RÉSIDUS =============================

# (1) Annexe C, dernière FAQ — « posez la phrase courante dans le
#     fichier-remise, commit, push — puis rejouez »
remplace(
    LIVRE / "sec-6.tex",
    "écrit ; posez la phrase courante dans le fichier-remise, commit, push — puis\n"
    "rejouez.",
    "écrit ; reconstituez à froid TROIS parts du séquestre courant (l'époque au\n"
    "manifeste), puis rejouez — la phrase ne vit en AUCUN dépôt, le refus nommé\n"
    "de la réécriture (D223).",
    "la dernière FAQ de l'annexe C : la prescription de remise remplacée par la garde D223")

# (2) §7.3 étape 1 — « Le fichier-remise D81 est à jour … le fichier AVANT tout »
remplace(
    LIVRE / "sec-4.tex",
    "\\item \\textbf{La phrase d'abord.} Le fichier-remise D81 est à jour (si vous venez de\n"
    "changer la phrase : le fichier AVANT tout — un premier \\code{migrer} refusé « phrase\n"
    "de contrôle divergente » est le fail-closed qui travaille, pas une panne).",
    "\\item \\textbf{La phrase d'abord.} Le séquestre 5/3 est à jour (si la phrase vient de\n"
    "changer : la reconstitution à froid de TROIS parts AVANT tout — un premier\n"
    "\\code{migrer} refusé « phrase de contrôle divergente » est le fail-closed qui\n"
    "travaille, pas une panne ; la phrase ne vit en AUCUN dépôt, D223).",
    "§7.3 étape 1 : le fichier-remise remplacé par le séquestre 5/3")

# (3) §9.2 ligne « phrase ERRONÉE » — « vérifiez le fichier-remise »
remplace(
    LIVRE / "sec-5.tex",
    "fichier-remise ; jamais de destruction, jamais d'écriture \\\\",
    "séquestre (la reconstitution à froid de TROIS parts, D223) ; jamais de\n"
    "destruction, jamais d'écriture \\\\",
    "§9.2 « phrase ERRONÉE » : le renvoi au fichier-remise remplacé par le séquestre")

# (4) Tableau 1, colonne CF1 — « le fichier-remise D81 » (la garde vivante)
remplace(
    LIVRE / "sec-1.tex",
    "La garde vivante & le fichier-remise D81 & les gardes + la sentinelle & le sachet",
    "La garde vivante & la phrase sous séquestre 5/3 (amendé D223) & les gardes + la "
    "sentinelle & le sachet",
    "Tableau 1 colonne CF1 : la garde vivante au séquestre")

# (5) Glossaire B, entrée « relève » — « et le fichier-remise D81 »
remplace(
    LIVRE / "sec-6.tex",
    "\\item[relève] Ce qui ressuscite le coffre si la machine meurt : le sachet (pièges,\n"
    "copies hors-ligne) et le fichier-remise D81.",
    "\\item[relève] Ce qui ressuscite le coffre si la machine meurt : le sachet (pièges,\n"
    "copies hors-ligne) — la phrase revient par la reconstitution à froid de TROIS\n"
    "parts du séquestre (amendé D223), jamais par un fichier de dépôt.",
    "le glossaire « relève » : le fichier de dépôt remplacé par le séquestre")

# ============ LA SPEC v0.15.7 — LES TROIS RÉSIDUS ===========================

# (6) Tableau 13 (§12.3) « Relève si la machine brûle », colonne CF1 —
#     « la phrase (D81 : le fichier est la remise) » ; l'ordre chronologique
#     des gardes rétabli (la phrase d'époque, l'amende D223 datée après)
remplace(
    SPEC / "sec-cf.tex",
    "Relève si la machine brûle & la phrase (D81 : le fichier est la remise) & T copies\n"
    "hors-ligne des fragments & le sachet : pièges d'époque + carte papier \\\\",
    "Relève si la machine brûle & la phrase — la garde d'époque D81 amendée le\n"
    "19 novembre 2026 : le séquestre 5/3, la reconstitution à froid de TROIS parts\n"
    "(D223) & T copies hors-ligne des fragments & le sachet : pièges d'époque + "
    "carte papier \\\\",
    "Tableau 13 « Relève » colonne CF1 : la prescription remplacée, l'ordre chronologique rétabli")

# (7) §14.3 « Contrepartie consignée » — « la phrase vit sur le stockage du
#     coffre Drive partagé par lien »
remplace(
    SPEC / "sec-d.tex",
    "hors coffre (D30). Contrepartie consignée : la\n"
    "phrase vit sur le stockage du coffre Drive partagé par lien — la confidentialité au\n"
    "repos repose sur le contrôle d'accès au dossier (restreindre le partage par lien :\n"
    "mitigation première) ; une phrase entrée dans l'historique git y demeure à vie, la\n"
    "rotation reste le remède — format normatif : FORMAT\\_CARTE § 11.",
    "hors coffre (D30). Contrepartie consignée (amendée D223) : la\n"
    "phrase ne vit en AUCUN dépôt — le séquestre 5/3 la porte (cinq parts Shamir à\n"
    "seuil trois, la reconstitution à froid quand la phrase sert) ; le résidu\n"
    "historique nommé : une phrase entrée dans l'historique git avant l'amende y\n"
    "demeure à vie, inopérante par la rotation (le refus nommé de la réécriture la\n"
    "garde) — format normatif : FORMAT\\_CARTE § 11.",
    "§14.3 la contrepartie : la phrase au Drive remplacée par le séquestre D223")

# (8) Tableau 16 (§13.6, la frontière des supports) « Dépôt git » —
#     « et la phrase de contrôle (D81 : le fichier est la remise…) »
remplace(
    SPEC / "sec-cf.tex",
    "le journal de travail — et la \\emph{phrase de contrôle} (D81 : le fichier est la\n"
    "remise ; la rotation reste le remède d'une exposition) & aucun conteneur de coffre",
    "le journal de travail — la phrase de contrôle n'y vit plus (amendée D223 : le\n"
    "séquestre 5/3 la porte, la reconstitution à froid de TROIS parts ; l'historique\n"
    "D81 du passé git demeure à vie, inopérant par la rotation) & aucun conteneur de "
    "coffre",
    "Tableau 16 « Dépôt git » : la phrase au dépôt remplacée par l'amende D223")

# (9) la table d'évolution v0.5.1/v0.5.2 (HISTORIQUE DATÉE — l'annotation
#     « amendé D223 » portée à la ligne de menace, l'ordre chronologique)
remplace(
    SPEC / "sec-d.tex",
    "dossier ; une phrase commise en git y demeure à vie, la rotation reste le remède &\n"
    "étendu (D81) \\\\",
    "dossier ; une phrase commise en git y demeure à vie, la rotation reste le remède &\n"
    "étendu (D81 ; amendé D223 — le séquestre 5/3, la phrase hors dépôt) \\\\",
    "la table d'évolution : la ligne de menace annotée amendé D223 (le contexte historique daté demeure)")

# ============ LES CORRECTIONS AU PASSAGE (nommées) ==========================

# (10) la couverture du Livre « Version 1.3 » → v1.6
remplace(
    LIVRE / "cover.html",
    '<div class="label">Document compl&eacute;mentaire &middot; Version 1.3</div>',
    '<div class="label">Document compl&eacute;mentaire &middot; Version 1.6</div>',
    "la couverture : Version 1.3 -> 1.6 (périmée)")

# (11) l'avant-propos « v1.3 / v0.15.2 » → v1.6 / v0.15.7
remplace(
    LIVRE / "sec-1.tex",
    "spécification (v1.3 : l'édition courante est la v0.15.2) : il ne crée aucune règle,",
    "spécification (v1.6 : l'édition courante est la v0.15.7) : il ne crée aucune règle,",
    "l'avant-propos : les versions courantes v1.6 / v0.15.7 (périmées)")

# (12) la phrase tronquée du §2.3 — la parenthèse jamais refermée
remplace(
    LIVRE / "sec-2.tex",
    "séquestre 5/3 ; la garde D81 est AMENDÉE (la phrase tournée, l'ancienne\n"
    "ACTIVE jusqu'au geste vécu.",
    "séquestre 5/3 ; la garde D81 est AMENDÉE (la phrase tournée, l'ancienne\n"
    "demeurant ACTIVE jusqu'au geste vécu de sa destruction).",
    "§2.3 : la phrase tronquée refermée (la parenthèse jamais refermée)")

# (13) le titre PDF du merge — v1.4 périmé → v1.6
remplace(
    LIVRE / "merge_cover.py",
    '"/Title": "Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.4)",',
    '"/Title": "Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.6)",',
    "le titre PDF du merge : v1.4 -> v1.6 (périmé)")

print(f"LA PURGE : {len(R)} remplacements ancrés vécus —")
for r in R:
    print("  -", r)
