# PLAN GELÉ — W27RESID (résidus éditoriaux + extension du linter)

> Évaluation du pack — prompt 2 de la vague 27 (26/11/2026). Append-only ; aucune valeur
> mesurée modifiée ; aucun artefact scellé touché ; le verbatim historique demeure octet pour
> octet (les corrections vivent aux sources courantes, les colonnes historiques restent datées).

## Les quatre résidus, corrigés à la source
- (a) SPEC, Table 12 (le programme de souveraineté, état à la passation v0.6.0), axe 3 : la
  cellule d'« État » dit « treize arbres signés … — verifier 13 arbres VERTS » alors que le
  sceau de l'Intention porte QUATORZE arbres depuis D177 (loupe.1 le quatorzième) : porté à
  « quatorze arbres signés … verifier 14 arbres VERTS » ; la colonne historique DÉMEURE DATÉE
  (cérémonies d'ère M8 [12 arbres, D162/D163] et M9 [13 arbres, D166/D168] telles quelles).
  Source : scripts/spec_v158/sec-cf.tex → spec_v159 (v0.15.17).
- (b) SPEC, titres dupliqués §1.23/§1.24 : deux sous-sections « Ce que change la v0.15.16 »
  (labels nouveautes1514/nouveautes1515) → DISTINGUÉES : la première (D274, les six résidus de
  l'évaluation de v0.28.0) et la seconde (D275, la prose de statut dérivée des registres)
  portent chacune son objet dans le titre.
- (c) MANUSCRIT §4.1, fragments français dans le corps anglais : « installés à la vague 14 » →
  anglais ; « 1 122 pas, 29,4 s » → anglais (les valeurs inchangées, la virgule décimale à
  l'anglaise) ; « au mur mémoire 4 Gio » → anglais ; « run non exécuté » → anglais.
  Source : edition-v0230/main.tex.
- (d) LIVRE, table 13 (chronologie de la migration du coffre réel) RÉORDONNÉE : 30/10 soir
  (cérémonie CF1→CF2) → 30/10 20:03 (premier essai refusé) → 20:37 (relance, pile complète) →
  20:40 (MIGRER, époque 1, checksum 0cc89a96) → 20:41 (VÉRIFIER VERT) → 31/10 18:10
  (attachement, doublon dénoncé → D131) → 18:18 (rapport, question fragments) → 31/10 soir
  (fenêtre de migration, habit du GUI → D132) → à suivre. Les dates imprimées demeurent telles
  quelles ; seul l'ORDRE des rangées est rétabli (le rapport de boîte noire v1.1 du 30/10 20:41
  fait foi). Source : scripts/livre_v18/sec-5.tex → livre_v19.

## Les trois classes nouvelles
- C27 COUNT-TABLECELL : tout compte d'arbres/vecteurs en cellule de table est confronté au
  registre — quatorze arbres (le sceau-I fait foi), 320 produits / 235 exécutables (le harnais
  fait foi) ; toute cellule divergente est refusée nommément ; les colonnes historiques datées
  (dix, douze, treize arbres aux ères nommées) sont admises À LEUR ÉTIQUETTE d'époque.
- C28 TITLE-UNIQUE : aucun titre de section/sous-section dupliqué dans une pièce (le défaut
  §1.23/§1.24 ne peut plus renaître).
- C29 LANG-BODY : la langue du corps par pièce — le manuscrit anglais, les quatre pièces
  françaises ; un fragment de prose corps dans l'autre langue est refusé, les citations verbatim
  et les noms propres (refus nommés, décisions, outils) admis.

## Critères d'acceptation
- Porte complète zéro rouge (L1..L29 après W27RECON et le présent plan).
- Une mutation négative par nouvelle classe (C27, C28, C29), refusée nommément.
- Diff NUL sur les artefacts scellés et les valeurs mesurées (sceau-I 14/14, aucune empreinte
  d'arbre touchée).
- Consignation append-only.
