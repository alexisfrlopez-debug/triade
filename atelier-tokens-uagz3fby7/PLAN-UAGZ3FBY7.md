# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 9, L'INSTRUCTION uagz3fby7 : LA RÉDUCTION DU COÛT EN TOKENS AU-DELÀ D'OPT-05 (le compilateur d'oracle, la bibliothèque de gabarits, la carte compacte, les ratios au plancher)

> Pré-enregistré AVANT toute mesure (la règle D204/D211 reconduite : le
> présent plan, son empreinte sha256 consignée au journal, PRÉCÈDE la
> première donnée). Aucun contrôle retiré, aucun round-trip supprimé,
> aucune vérification affaiblie. Les SCELLES INTACTES par construction :
> la campagne est LECTURE SEULE sur les artefacts (empreintes vérifiées
> avant/après, la liste du runner M4).

## 1. LES HYPOTHÈSES (falsifiables, pré-enregistrées)

H1 — L'ÉDITION PAR HUNKS (OPT-05, la grammaire v2) : le gain mesuré à la
vague 8 (éditer-H2 total −34,3 %, réponse −97,7 %, 17/18) est REPRODUCTIBLE
à la même graine à ±5 % près sur la médiane ; attente directionnelle
confirmée.

H2 — L'AJOUT PAR HUNKS : la grammaire v2 REFUSÉE en l'état pour l'ajout
(ajouter-H2 0/18 HORS-FORMAT, le re-dump du contexte) — l'hypothèse
NOUVELLE : la cause nommée (le format de notation non enseigné par
l'exemple AU MOMENT du hunk) se traite par le GABARIT PORTANT (point 3) ;
SI l'ajout par hunks re-mesuré (ajouter-H3 : la notation d'exemple AU
PROMPT + les hunks) demeure sous 12/18, l'ajout par hunks est REJETÉ EN
L'ÉTAT pour la deuxième fois — consigné tel quel, l'ajout complet
(ajouter-A2) demeure la voie.

H3 — LE COMPILATEUR D'ORACLE : l'oracle de référence généré PAR SCRIPT
depuis le gabarit structuré de la couche I (pre/post/inv/échecs/vecteurs)
— SANS AUCUN token LLM — est CONFORME à l'oracle écrit à la main (la
confrontation aux vecteurs : zéro divergence) ; les tokens d'oracle
supprimés par unité = la longueur tokenisée (tokenizer natif) du code
d'oracle qui aurait dû être ÉMIS par l'agent — mesurée, jamais estimée.

H4 — LA BIBLIOTHÈQUE DE GABARITS : une unité comparable composée PAR
HÉRITAGE SCELLÉ (la réponse ne porte que la spécification nouvelle + la
déclaration d'héritage aux entrées scellées) coûte MOINS que l'unité
écrite entière (ajouter-A2, médiane 5 079) — attente directionnelle
−40 à −70 % au total ; SI la mesure falsifie (le gabarit n'achète rien),
consigné tel quel.

H5 — LA CARTE COMPACTE : le total de localisation au POINTEUR SEUL
(OPT-04 adopté D222) est REPRODUCTIBLE (la re-mesure RQ2 vague 8 :
médiane 1 103, réponse 52) à ±5 % — la cellule localiser-P le re-mesure.

H6 — LES RATIOS AU PLANCHER : pour CHAQUE opération (localiser, éditer,
ajouter/composer) le ratio au plancher = tokens mesurés (médiane) ÷
longueur tokenisée du diff réel (le plancher de description minimale) ;
le plancher est NOMMÉ avec sa méthode : la longueur tokenisée (cl100k_base,
l'instrument parallèle consigné depuis OPT-02) du diff minimal qui
reproduit le changement — la convention de périmètre AVANT toute
comparaison (le matériau, la prose de prescription et la réponse comptés
séparément, JAMAIS fusionnés).

## 2. LES CELLULES (n=18 chacune, la graine 20261117, l'ordre par
shuffle déterministe — le même instrument que la vague 8 : le CLI z-ai,
le champ usage LU, chaque appel journalisé au journal_tokens.jsonl,
la garde brute verbatim au garde-brut.jsonl)

  éditer-H2   — reconduite (la référence reproductible de la vague 8) ;
  ajouter-H3  — la grammaire v2 + L'EXEMPLE DE NOTATION AU PROMPT au
                moment du hunk (l'amendement v3 de la cause nommée) ;
  composer-G  — l'unité comparable composée par héritage scellé (H4) :
                la tâche porte la spécification I nouvelle (le gabarit
                § 2 de la spec) + la carte des entrées scellées à
                hériter ; la réponse attendue : la DÉCLARATION
                d'héritage + la notation du SEUL code nouveau ;
  localiser-P — le pointeur seul (deux champs littéraux : l'identifiant
                + l'empreinte sha256 de la notation), l'expansion côté
                client aux QUATRE refus nommés (POINTEUR-INCONNU,
                EMPREINTE-DIVERGENTE, EXPANSION-DIVERGENTE, HORS-FORMAT).

LES TÂCHES : les 18 tâches « la constante revue » de la vague 8
(taches-edition.json, gelées sha256 1122251e…) reprises TELLES QUELLES
pour éditer-H2 ; les mêmes 18 blocs pour localiser-P ; les tâches
d'ajout de la vague 8 (la même graine) pour ajouter-H3 ; une unité
NOUVELLE comparable (le même gabarit de difficulté : un bloc de calcul
pur du domaine loupe) pour composer-G — la tâche gelée au présent plan.

## 3. LE COMPILATEUR D'ORACLE DÉTERMINISTE (H3)

L'OUTIL : compilateur_oracle.py — lit le gabarit structuré de la
couche I (loupe/I/*.md : identifiant, intention, contrat pre/post/inv,
cas d'échec, vecteurs dorés), GÉNÈRE l'oracle de référence Python
(l'implémentation triviale, lente, sûre — le juge) PAR SCRIPT. L'oracle
demeure DÉRIVÉ DE I, jamais de B ; RÉGÉNÉRÉ à chaque session (l'empreinte
consignée) ; la CONFRONTATION : l'oracle généré contre l'oracle écrit à
la main aux VECTEURS DORÉS de chaque bloc — zéro divergence exigée, tout
écart un refus nommé ORACLE-DIVERGENT. LA MESURE : les tokens supprimés
par unité = la réponse tokenisée (natif) du code d'oracle généré — ce
que l'agent n'émet plus.

## 4. LA BIBLIOTHÈQUE DE GABARITS PORTEURS DE PREUVES (H4)

L'INDEX : la carte du domaine porte l'index des blocs scellés
réutilisables et leurs contrats (l'identifiant, la signature, le slot,
l'empreinte — LUS du plan et de la carte, jamais retapés) ; la
COMPOSITION par héritage scellé (R7) : le nouveau bloc APPELLE les
entrées scellées À LEURS ADRESSES (le repli du modèle D222/OPT-01), il
ne les réécrit pas. LA MESURE : le coût unitaire avant (ajouter-A2) /
après (composer-G) ; LA PART DE LA SPIRALE CORRECTIVE : les appels de
reprise après divergence (le journal les porte) rapportés au total —
avant/après.

## 5. LES RÈGLES DE VERDICT PRÉ-ENREGISTRÉES (fail-closed)

  - ZÉRO DIVERGENCE sur la localisation et l'expansion (chaque réponse
    localise le bloc soumis ; l'expansion recouvre la notation EXACTE,
    octet pour octet — le round-trip du client vert 18/18 reconduit) ;
  - le round-trip 100 % sur TOUTE notation reconstruite (le client
    hunks : appliquer, reconstruire, confronter — les QUATRE refus nommés
    HUNK-INCONNU, CONTEXTE-DIVERGENT, ROUND-TRIP-DIVERGENT, HORS-FORMAT,
    le premier l'emporte) ;
  - les gains LUS des logs bruts par le script d'extraction (jamais
    tapés) ; les distributions COMPLÈTES (n, médiane, q1, q3, min, max
    par cellule et par champ : matériau, prose, réponse, total) ;
  - une re-tokenisation indépendante (cl100k_base) à ±1 token près des
    comptes natifs (la règle OPT-02 reconduite) ;
  - les EMPREINTES SCELLÉES intactes avant/après la campagne ;
  - AUCUNE graine supprimée, AUCUN vecteur réduit, AUCUNE vérification
    retirée ;
  - les ratios au plancher RECALCULÉS depuis les CSV bruts par le linter
    numérique (la tableau de bord refuse toute divergence).

## 6. LA CONSIGNATION

OPT-06 (le compilateur d'oracle + la bibliothèque de gabarits + la carte
compacte au plancher) au journal d'optimisation (le format D205) ; la
décision append-only D224 ; les cellules rejouées consignées au rapport
de l'atelier ; la présente empreinte au journal AVANT la première donnée.
