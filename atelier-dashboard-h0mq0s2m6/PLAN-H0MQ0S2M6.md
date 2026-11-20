# PLAN — LA VAGUE 9, L'INSTRUCTION h0mq0s2m6 : LE TABLEAU DE BORD DES QUATRE AXES ET LA COHÉRENCE DU PACK v0.20.0

> L'instruction de cohérence : AUCUNE valeur mesurée modifiée, AUCUNE
> règle affaiblie, AUCUN artefact scellé touché. Le tableau de bord est
> GÉNÉRÉ depuis les pièces brutes (les CSV des ateliers, les journaux
> vivants) — jamais tapé à la main ; il RECALCULE chaque ratio et
> REFUSE toute divergence (fail-closed au build).

## 1. LE TABLEAU DE BORD DES QUATRE AXES (généré)

L'ORDRE LEXICOGRAPHIQUE EXPLICITE — Sécurité, Performance,
Optimisation, Coût en tokens — AUCUNE compensation entre rangs (la
fonction objectif du protocole § 8, portée au tableau). POUR CHAQUE
AXE : la valeur mesurée courante (la source citée : le CSV, le
journal), le PLANCHER IRRÉDUCTIBLE et sa MÉTHODE DE CALCUL (nommée),
le RATIO D'OVERHEAD (mesuré ÷ plancher, la convention de périmètre
AVANT toute comparaison), la CIBLE, et le STATUT de CHAQUE RÉSIDU
NOMMÉ.

LES SOURCES (les pièces brutes, lues par le script) :
  - SÉCURITÉ : surete_memoire.csv (v110 + l'extension v200 : les
    2 098 accès, les classes, les non-résolus déchargés), la batterie
    de mutation (le brut 811/832 [814/832 si les tuables meurent],
    l'ajusté équivalents-exclus, les 21 survivants et leur statut), le
    fuzzing (la couverture par bloc d'entrée non fiable, les crashs,
    les canaris), le temps constant (le hash de trace, la preuve
    statique de non-interférence), la preuve CF3 (le statut mécanisé),
    la garde du sceau (14/14) ;
  - PERFORMANCE : la mesure M4 (l'avant, le froid, le chaud, le bras
    C, le ratio de régime, n et les IQR — les JSON du runner), le
    couloir A (la parité SSE2 par bloc : instructions/après ÷
    instructions/gcc-O2, le verdict par bloc), le couloir B (les
    chemins ISA : le gain avant/après par chemin, SHA-NI compris —
    OPT-01) ;
  - OPTIMISATION : le journal OPT-NN (OPT-01..OPT-08 : chaque gain
    mesuré, ses conditions) ;
  - COÛT EN TOKENS : les journaux de campagne (localiser-P, éditer-H2,
    ajouter-H3, composer-G : médianes et distributions), les ratios au
    plancher (mesuré ÷ diff réel tokenisé, la méthode cl100k_base
    nommée), les tokens d'oracle supprimés par le compilateur.

L'OUTIL : tableau_bord_v200.py — LIT les pièces, RECALCULE chaque
ratio, ÉCRIT le tableau (le format : un fichier par axe + le
récapitulatif), REFUSE toute divergence entre le tableau et les
sources (le linter étendu le re-vérifie au build). LE PLANCHER par
axe, NOMMÉ avec sa méthode : sécurité — zéro non-résolu / cent pour
cent des tuables tués (le dénominateur ajusté) ; performance — le
bras C à travail égal (la référence compilée) ; optimisation — le gain
mesuré par levier fondé sur hot path (le plancher est le JOURNAL,
jamais une cible flottante) ; coût — la longueur tokenisée du diff
réel (le plancher de description minimale).

## 2. LA SECTION « DISTANCE AU PLANCHER » DU MANUSCRIT

Une section NOUVELLE du manuscrit v0.20.0 : les ratios par axe, ce qui
les compose (la décomposition par sous-indicateur), LA CONVENTION DE
PÉRIMÈTRE OBLIGATOIRE avant toute comparaison (ce qui est compté : le
matériau, la prose, la réponse — jamais fusionnés ; le périmètre des
blocs ; la machine ; la graine), et la lecture lexicographique (aucune
compensation : un gain de rang inférieur ne rachète JAMAIS un recul de
rang supérieur).

## 3. L'UNIFICATION PAR MACROS (les étiquettes, les dates, les plages,
les comptes)

regenerer_macros_v200.py — reconduit de la vague 8 : les comptes de
lignes des journaux (journal, worklog, décisions) LUS des fichiers,
la plage de décisions D1–D{dernière}, le DOI concept
10.5281/zenodo.24367343 et le DOI de version courant, les canons M4,
le compte d'arbres signés — GÉNÉRÉS, jamais tapés. Les CINQ pièces
portent les MÊMES macros (la spécification et le Livre du Coffre
compris — les étiquettes de version, les dates, les plages, les
comptes : la cohérence inter-pièces au build).

## 4. L'ALIGNEMENT À L'ÉTAT VÉCU (la spécification v0.15.6, le Livre
du Coffre v1.5)

PAR DÉCISION APPEND-ONLY (D224+ : les décisions de la vague 9),
SANS AFFAIBLIR AUCUNE RÈGLE : les comptes d'arbres (quatorze → le
compte réel si la vague 9 scelle de nouveaux arbres — SINON le compte
demeure, NOMMÉ tel quel), les titres d'annexes (l'annexe B à la plage
réelle D75–D{dernière}), les références de version périmées (v0.19.6 →
v0.20.0, v0.15.5 → v0.15.6, v1.4 → v1.5), la table des preuves (le
statut CF3 mécanisé, la non-interférence statique), la section
nouveautés (les gains de la vague : OPT-06..08, le certificat
incrémental, les deux couloirs, la sûreté mémoire à zéro non-résolu si
tenue). LES VERDICTS pré-enregistrés en DEUX LIGNES DISTINCTES quand
une règle a été amendée après falsification (H5-D204 réfutée ×23,9
mesurée / H5-amendée-OPT04 tenue ×3,0 — le modèle reconduit) ; LE
VERDICT BRUT à côté du verdict par attribution (H6 : 3 côté T / 0 côté
C brut, l'attribution kit-partagé à côté) ; LE CRITÈRE D'ÉCHANTILLON
réconcilié (les unités instrumentées vs livrées, N=7) ; LA PROBABILITÉ
DU TIRAGE à 1/16 (quatre tirages indépendants).

## 5. L'ABSTRACT (un seul paragraphe, l'état courant v0.20.0)

Réécrit en un seul paragraphe cohérent : la clôture des 30 000 traces
zéro divergence en premier, le gap 10 000 traces comme histoire datée,
l'état des quatre axes AU PLANCHER MESURÉ (les ratios de la section
distance-au-plancher), les canons de la vague 9. SANS accumulation de
couches d'édition (les couches v0.19.x fondues en l'état courant).

## 6. LE LINTER INTER-PIÈCES v200 (étendu)

linter_v200.py — reconduit de v196 (39 VERT) et ÉTENDU : les EN-TÊTES
(les étiquettes de version des cinq pièces croisées : v0.20.0 ↔
v0.15.6 ↔ v1.5), les DOI (le concept partout, les versions datées
nommées), les COMPTES (les plages de décisions, les comptes de lignes,
le compte d'arbres — les macros croisées aux journaux RÉELS), les
RATIOS (les ratios au plancher RECALCULÉS depuis les CSV bruts : le
tableau de bord confronté, TOUT écart un ROUGE), les PROBABILITÉS (le
1/16, le 1/8 interdit), les valeurs mesurées de la vague 9 (les canons
M4, les gains OPT, les scores mutation brut/ajusté côte à côte,
JAMAIS fusionnés), les interdits (les valeurs périmées, les
formulations stale). LE CONTRÔLE NÉGATIF : une divergence
volontairement injectée (une valeur mutée au tableau) REFUSÉE au
premier nom — la pièce au journal ; après retrait, le build admis.

## 7. LES RÈGLES DE VERDICT (fail-closed)

  - le linter étendu : ZÉRO divergence sur toutes les valeurs
    partagées ; un écart volontaire REFUSÉ puis RETIRÉ (le contrôle
    négatif vécu) ;
  - TOUTES les tables du manuscrit régénérées par le script
    d'extraction : AUCUN chiffre tapé à la main ;
  - la garde du sceau 14/14, les empreintes des artefacts scellés
    INTACTES, l'autotest du kit de séquestre vert ;
  - les verdicts pré-enregistrés ORIGINAUX demeurent lisibles et datés
    au journal append-only (jamais réécrits) ;
  - le tableau de bord RECALCULE chaque ratio depuis les CSV bruts et
    REFUSE toute divergence ;
  - le pack TRIADE_presentation_v0.20.0.zip : EXACTEMENT 5 documents
    PDF régénérés et cohérents (manuscrit, spécification, Livre du
    Coffre, preuves et calculs, présentation), les empreintes sha-256
    des cinq pièces consignées DANS la présentation et le document de
    preuves.
