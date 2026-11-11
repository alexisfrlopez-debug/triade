#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree_234.py — LA VAGUE 3 DES INSTRUCTIONS OUVERTE : six
fichiers reçus à /instructions (11/11 19:14-19:15 UTC), rapatriés et
recoupés md5 MATCH (rapatrier_instructions_v3.py), lus INTEGRALEMENT —
le contenu CITÉ à l'entrée qui ouvre l'exécution (la règle D197), le
programme lu en six paquets, l'ordre d'exécution fixé, l'environnement
vérifié (Java 21, réseau GitHub, SHA-NI natif, hypothesis). Entrée 234
+ worklog Task 140. Append-only : les fins VÉRIFIÉES avant écriture."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"


def append_verifie(chemin: pathlib.Path, fin_attendue: str, bloc: str,
                   nom: str, marqueur_doublon: str) -> None:
    texte = chemin.read_text(encoding="utf-8")
    if texte.count(fin_attendue) != 1:
        sys.exit(f"[consigner] {nom} : la fin attendue apparaît "
                 f"{texte.count(fin_attendue)} fois (attendu : 1) — "
                 f"append refusé")
    if not texte.rstrip("\n").endswith(fin_attendue.rstrip("\n")):
        sys.exit(f"[consigner] {nom} : la fin attendue n'est pas la "
                 f"dernière section — append refusé")
    if marqueur_doublon in texte:
        sys.exit(f"[consigner] {nom} : {marqueur_doublon} déjà présent — "
                 f"append refusé (doublon)")
    with chemin.open("a", encoding="utf-8") as f:
        f.write(bloc)
    print(f"[consigner] {nom} : appendé ({len(bloc)} caractères)")


ENTREE_234 = """

## Entrée 234 — LA VAGUE 3 : SIX FICHIERS D'INSTRUCTION REÇUS, RECROPÉS, LUS ET CITÉS — l'exécution OUVERTE (la règle D197 tenue : lecture intégrale avant toute attribution, le contenu cité ci-dessous mot à mot), le programme lu en SIX paquets — les corrections du manuscrit, le reclassement des défauts Loupe, la preuve TLA+/Apalache et le property-based, la campagne de mutation étendue, le plan de comparaison pré-enregistré, le SHA-NI — l'ordre fixé, l'environnement vérifié (12/11, la session de la vague 3)

**La vague.** /instructions porte SIX fichiers nouveaux, déposés 11/11 19:14:53–19:15:13 UTC (créés 19:15:54–55 — le dépôt en lot) : Qwen__20261111_sollwnmae.txt (1 719 o, md5 72c1db35ecd2…), Qwen__20261111_xboh1kljq.txt (992 o, md5 6f7637d182df…), Qwen__20261111_6zqo2h60n.txt (1 488 o, md5 cae23bc6dd5b…), Qwen__20261111_n4kwcs3wa.txt (1 000 o, md5 ac1da1f21e62…), Qwen__20261111_54wni4hzh.txt (1 179 o, md5 305856a4cc3f…), Qwen__20261111_lfh49a1xf.txt (1 248 o, md5 a55d24226f5c…). Rapatriés par scripts/rapatrier_instructions_v3.py : les SIX md5 recoupés MATCH contre les métadonnées Drive, copies au dépôt instructions_20261111/ (le modèle des vagues 1 et 2). Les six instructions exécutées des vagues antérieures demeurent archivées hors de /instructions — le dossier ne porte que la vague 3.

**Le contenu cité (D197 — mot à mot).**

*sollwnmae* : « Parcours TRIADE_manuscrit_v0.15.0.pdf (source LaTeX), la spécification v0.15.0 et les CSV de preuves. Corrige sans toucher aux artefacts scellés ni aux arbres signés : 1) Reformule les pourcentages du benchmark sans ambiguïté : "la notation exécute +9,9 % d'instructions de plus que gcc -O2 (75 983 vs 69 132) et −2,0 % de moins que -Os (77 505)" ; aligne la spécification. 2) Remplace "4–11×" par les ratios réels des médianes RQ2 (≈3–11×), recalculés depuis remesure_rq2.csv. 3) Unifie le quantile à 1,86σ (valeur exacte 1,863) partout. 4) Purge les résidus d'édition : référence spec "v0.13.0" → v0.15.0 ; archives "v0.14.0" → v0.15.0 dans Data Availability ; supprime les phrases "budgets mesurés une seule fois / ère M1 seulement" contredites par D195 ; réécris la conclusion avec les médianes actuelles et 56 survivants (138 = historique v0.11.0, à mentionner comme tel) ; "D1–D197" → D1–D198. 5) Renomme la grille de réplication T1–T5/X1–X3 en classes distinctes (ex. F1–F5 terrain, L1–L3 laboratoire) pour lever la collision avec T1–T6/X1–X8, avec table de correspondance. Consigne chaque correction dans une nouvelle décision D199 (journal append-only, aucune entrée réécrite). Vérification : régénère toutes les tables par le script d'extraction ; recalcule chaque pourcentage depuis les CSV bruts ; recherche par motif les chaînes périmées ("v0.13.0", "v0.14.0", "4–11", "1,87", "138 survivants" hors contexte historique) et exige zéro occurrence injustifiée ; contrôle que les sha256 des artefacts scellés et des arbres signés sont identiques avant/après ; produis un rapport diff complet. »

*xboh1kljq* : « Reclasse les onze défauts nommés des runs Loupe (entrées 204–222 du journal, Table 4) en deux catégories : défaut de la pièce (code natif scellé) et défaut du kit/harnais (Python, scénario, sonde). Recalcule deux taux d'échappement : artefact natif seul, et ensemble livré kit+pièce, chacun avec son intervalle Clopper-Pearson 95 % exact et la réserve de non-indépendance. Mets à jour l'abstract, §2.3 (règle de comptage), §3.1, Table 4 (colonne catégorie) et Threats to validity. Le taux "code natif écrit par agent" doit être présenté comme la métrique primaire de RQ1, le taux ensemble comme métrique de livraison. Vérification : recompte indépendamment depuis les entrées du journal (pas depuis la table existante) ; recalcule les deux IC avec une seconde méthode (script séparé) et exige l'égalité à 10⁻³ ; contrôle la cohérence abstract↔résultats↔conclusion ; régénère les tables et archive le rapport de comptage avec son empreinte. »

*6zqo2h60n* : « Encode la sémantique opérationnelle du coffre CF3 (13 règles, état d'époque non borné) dans TLA+ et décharge l'invariant I (I1–I4) par Apalache (SMT, entiers non bornés) ; si l'outil est absent, installe-le et consigne la déviation levée. Ajoute un audit mécanique des 13 règles prouvant qu'elles ne lisent l'époque que via les prédicats {==1, ≥2} et l'opération successeur (analyse des gardes/actions, pas des témoins par translation). En parallèle, remplace le raffinement par scénarios par un test property-based modèle↔implémentation : génération de ≥10 000 traces aléatoires (graine consignée), vérification pas à pas, shrinking sur tout écart, couverture des 13 règles et des chemins d'échec mesurée. Ne change le statut "prouvé non borné" qu'après existence des artefacts de preuve ; sinon écris "argument inductif témoigné mécaniquement, preuve indépendante en attente". Le coffre réel n'est jamais ouvert : clones de test à phrases publiques marquées uniquement. Vérification : rejoue TLC/Apalache depuis un clone frais et exige la reproduction exacte des counts bornés D187 (154 états/1 152 transitions) comme contrôle de fidélité ; exige zéro contre-exemple ou un contre-exemple archivé et nommé ; rejoue les traces property-based à graine identique et vérifie la stabilité des verdicts ; consigne les empreintes des scripts, logs et preuves ; mets à jour la table des statuts uniquement depuis ces pièces. »

*n4kwcs3wa* : « Étends la campagne de mutation des 52 blocs scellés (copies de laboratoire uniquement) : ≥200 mutants par bloc avec graine consignée, incluant mutations multi-octets, substitutions d'opérateurs et de conditions, altérations d'offsets et de constantes ; applique les tueurs en ordre de coût (round-trip, structurel, différentiel, composition). Classe chaque survivant : mutant équivalent (preuve d'équivalence argumentée) ou chemin non couvert (nommer le chemin et le contrôle manquant). Rapporte les taux par domaine avec intervalles de confiance et compare à v0.11.0/v0.14.0 sans remplacer l'historique. Vérification : rejoue toute la campagne à graine identique et exige des verdicts bit-identiques ; contrôle sha256 avant/après de chaque artefact scellé et arbre signé (aucun ne bouge) ; recalcule les taux depuis le CSV brut produit ; exige que chaque survivant restant porte une classification et une pièce ; régénère les lignes de tables concernées par le générateur. »

*54wni4hzh* : « Rédige et verrouille (empreinte sha256 consignée AVANT toute mesure) un plan de comparaison pré-enregistré : même agent, même famille de tâches (les six blocs du bras C + une application complète de type Loupe), deux workflows — TRIADE notation scellée vs C+gcc standard avec le même kit terrain. Métriques : défauts échappés par livraison (règle de comptage pièce/kit séparée), tokens réels mesurés depuis les logs d'usage API (plus jamais ×1,08 quand un log existe), temps humain de cérémonie/revue, temps de calcul de vérification. Définis hypothèses H1–Hn, critères d'acceptation, taille d'échantillon et règle d'arrêt avant toute exécution. Prépare les kits et scripts de mesure ; n'exécute aucune mesure terrain (elle appartient au développeur) et ne fabrique aucun résultat. Vérification : contrôle que l'empreinte du plan est consignée et datée avant tout fichier de résultats ; fais un dry-run d'instrumentation sur un bloc de laboratoire pour prouver que les compteurs de tokens correspondent aux logs à l'unité près ; audite que le plan ne contient aucun chiffre de résultat ; consigne le tout au journal des décisions. »

*lfh49a1xf* : « Identifie d'abord le hot path par mesure : instrumente le hachage de fichiers volumineux dans le harnais Loupe et consigne la mesure avant toute optimisation (R11). Si le hot path est confirmé, crée une variante de profil sha256 utilisant SHA-NI, sélectionnée par dispatch CPUID avec repli scalaire sur les blocs scellés existants, contrat I inchangé (R4), adresses scellées intactes (R7), notation round-trip vérifiée. Prépare le kit de mesure terrain avant/après dans des conditions identiques (même machine, même entrée, condensé vérifié avant comptage, opérations complètes init+absorb+final — jamais un périmètre partiel). Aucun scellement : la cérémonie et le run terrain appartiennent au développeur ; l'arbre signé n'est pas touché sans cérémonie d'ère. Vérification : vecteurs dorés FIPS 180-4 verts sur les deux chemins (dispatch forcé dans les deux sens) ; égalité des condensés scalaire/SHA-NI sur corpus aléatoire ; round-trip 100 % ; contrôle structurel temps-constant sur le nouveau chemin ; sha256 des artefacts scellés existants identiques avant/après ; consigne l'entrée OPT-NN au journal d'optimisation avec mesures avant/après et refuse l'optimisation si le hot path n'est pas mesuré. »

**La numérotation.** L'instruction sollwnmae demande « une nouvelle décision D199 » — D199 EST DÉJÀ PRISE (la réparation de l'instrument du miroir, consignée ce jour même à la session de reprise) : les corrections seront consignées au prochain numéro LIBRE (D200 et suivants, dans l'ordre d'achèvement des paquets). La cible « D1–D198 » du manuscrit (écrite avant D199) sera portée à la valeur COURANTE au moment de la régénération — l'esprit de l'instruction : la plage nomme la vraie dernière décision.

**L'environnement vérifié (la recce avant l'engagement).** Java 21 PRÉSENT (OpenJDK 21.0.13 — TLA+ Tools et Apalache exécutables) ; le réseau joint les releases GitHub (TLA+ v1.8.0 et Apalache téléchargeables — la clause « si l'outil est absent, installe-le » de 6zqo2h60n est EXÉCUTABLE, la déviation « preuve indépendante absente » pourra être levée si les outils tournent) ; le CPU PORTE SHA-NI (lfh49a1xf testable nativement — le dispatch CPUID aura ses deux chemins réels sur cette machine) ; hypothesis INSTALLÉ (le property-based de 6zqo2h60n).

**L'ordre d'exécution (fixé, les dépendances lues).** (1) LE TLA+/APALACHE + PROPERTY-BASED (6zqo2h60n) D'ABORD — le paquet le plus incertain, et son issue décide le LANGAGE du statut (« prouvé non borné » vs « argument inductif témoigné mécaniquement, preuve indépendante en attente ») que la révision du manuscrit devra porter ; (2) LA CAMPAGNE DE MUTATION (n4kwcs3wa) — la plus lourde en calcul, ≥200 mutants × 52 blocs ; (3) LE RECOMPTE LOUPE (xboh1kljq) — depuis les entrées 204–222 du journal, indépendant des tableaux existants ; (4) LA RÉVISION MANUSCRIT+SPÉCIFICATION (sollwnmae) — intégrant les résultats de 2 et 3 et le langage du statut issu de 1 ; (5) LE PLAN PRÉ-ENREGISTRÉ (54wni4hzh) — empreinte consignée AVANT toute mesure ; (6) LE SHA-NI (lfh49a1xf) — mesure du hot path d'abord, l'optimisation refusée si le hot path n'est pas mesuré. Chaque paquet achevé porte SA consignation (entrée + décision + task) ; le sync aux jalons.

**Frontières (déclarées à l'ouverture, tenues à la clôture).** Aucun artefact scellé touché (loupe.exe c1115105…, proxy.exe 446279f3… — sha256 contrôlés avant/après de CHAQUE paquet) ; le coffre réel JAMAIS ouvert (clones de test à phrases publiques marquées uniquement, D87/D192) ; AUCUNE mesure terrain exécutée (54wni4hzh et le run SHA-NI de lfh49a1xf appartiennent au développeur) ; AUCUN chiffre fabriqué — ce qui n'est pas mesuré n'existe pas ; les consignations antérieures non réécrites (append-only).
"""

TASK_140 = """

Task ID: 140
Agent: Z.ai (agent principal)
Task: LA VAGUE 3 DES INSTRUCTIONS — SIX paquets reçus à /instructions
(11/11 19:14-19:15 UTC), rapatriés md5 MATCH, lus intégralement et
CITÉS (D197), l'exécution OUVERTE : TLA+/Apalache + property-based,
campagne de mutation étendue, recompte Loupe, révision
manuscrit+spécification, plan de comparaison pré-enregistré, SHA-NI.

Work Log:
- LA VAGUE : six fichiers (992-1 719 o), /instructions ne porte qu'eux
  (les six instructions antérieures exécutées demeurent archivées) ;
  rapatrier_instructions_v3.py : les SIX md5 recoupés MATCH, copies au
  dépôt instructions_20261111/.
- LE CONTENU CITÉ (D197) : les six textes intégraux cités à l'Entrée
  234 — aucune attribution d'héritage, la lecture intégrale AVANT le
  programme.
- LA NUMÉROTATION : « nouvelle décision D199 » demandée par sollwnmae
  mais D199 est PRISE (l'instrument du miroir, ce jour) — les
  consignations de la vague prendront D200 et suivants.
- L'ENVIRONNEMENT : Java 21 (TLA+ exécutable), réseau GitHub joignable
  (TLC/Apalache téléchargeables), CPU SHA-NI natif, hypothesis installé.
- L'ORDRE : (1) TLA+/PBT — décide le langage du statut ; (2) mutation
  ≥200×52 ; (3) recompte Loupe depuis les entrées 204-222 ; (4) la
  révision manuscrit+spécification intégrant tout ; (5) le plan
  pré-enregistré (empreinte AVANT toute mesure) ; (6) SHA-NI (hot path
  mesuré d'abord, sinon refus).
- Frontières : artefacts scellés intouchés (sha256 avant/après par
  paquet), coffre réel jamais ouvert, aucune mesure terrain, aucun
  chiffre fabriqué, append-only.
- SUITE : l'exécution paquet par paquet, consignation à l'achèvement de
  chacun, sync aux jalons.
"""


def main() -> int:
    append_verifie(
        JOURNAL,
        "le dépôt en clair est un geste d'ACCÈS, pas une nouvelle livraison) ; "
        "aucun octet du PDF modifié (la copie est une copie, l'empreinte le "
        "prouve) ; aucune pièce scellée touchée ; les consignations "
        "antérieures non réécrites (append-only).",
        ENTREE_234, "JOURNAL_TRAVAIL.md", "Entrée 234")
    append_verifie(
        WORKLOG,
        "la réplication (l'annotateur, le\n  second domaine).",
        TASK_140, "worklog.md", "Task ID: 140")
    print("[consigner] Entrée 234 + Task 140 : CONSIGNÉES (la vague 3 ouverte)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
