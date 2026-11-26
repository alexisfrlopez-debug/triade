# PLAN-W28CORRIGE — SOLDER LES RÉSIDUS NUMÉRIQUES ET DE PÉRIMÈTRE DE LA VAGUE 28
## (la correction prompt de l'évaluation du pack v0.33.0 — instructions2.txt §10, dépôt du 26/11/2026 au /instructions ; exécutée par la présente reprise le 27/11/2026)

**LA SOURCE PRÉSCRIPTIVE** : l'évaluation « sans anesthésie » du pack TRIADE v0.33.0
(instructions2.txt au /instructions du coffre, 25 491 o), son §10 « Prompt de correction
pour l'agent ». Objectif : solder les résidus numériques et de périmètre de la vague 28,
SANS toucher aux artefacts scellés ni re-tirer aucune cible.

**LE PLAN GELÉ AVANT TOUTE DONNÉE** (les étapes, dans l'ordre, jamais re-tirées) :

1. **L'AUDIT** — confronter les empreintes d'abord ; lire intégralement
   atelier-w28harnais/rapport.txt, atelier-w28vaes/rapport.txt,
   atelier-w28opt16/rapport.txt et CIBLES.md ; pour chaque ratio publié dans les
   cinq pièces, recalculer depuis les opérandes non arrondis du rapport source
   (les registres : volumes-resultat.json, mesure-sched.txt, mesure-v3b.txt,
   resultats-opt16.json, journal-opt16.jsonl). Lister les écarts > 0,005 en
   valeur relative. Cas connus à traiter : 33× (46,6/1,9), 1 056× (46,6 ms /
   24,0 µs), 2,68× (1 082/409).
2. **LES CORRECTIONS À LA SOURCE** (rapport ou registre, jamais la prose seule),
   chacune avec ERRATUM append-only daté (l'ancienne valeur et la nouvelle) :
   - harnais : la valeur canonique du mur du committé est la MÉDIANE DE NEUF
     PASSES du registre (25,4 ms), pas la passe froide unique (46,6 ms) ; le
     ratio committé→généralisé se recompose des régimes du registre
     (1 056,04 / 77,49 = 13,6×) — l'ancienne ligne « 46,6 ms … 33× » devient
     « 25,4 ms (médiane de neuf passes ; la passe froide mesura 46,6 ms) …
     13,6× » ;
   - vaes : le ratio 2,68× se recompose de SA PROPRE passe (1 082 / 404 =
     2,6782, mesure-sched.txt) — l'opérande d'opposé imprimé à côté (409 ns,
     la passe du portage C) clarifié : chaque ratio porte les opérandes de sa
     passe ; la coquille « 2 47-2,68 » corrigée en « 2,47–2,68 » ;
   - CIBLES.md et docs/JOURNAL_OPTIMISATION.md : les lignes porteuses mises en
     cohérence (aucune cible re-tirée, aucun verdict retourné).
3. **LA DÉCOMPOSITION OPT-16** — depuis journal-opt16.jsonl : prompt 15 519 /
   réponse 1 542 (total 17 061, 39 appels, 18 tâches) ; publication de la
   seconde ligne « coût par changement validé, échecs amortis : 1 896 tokens
   natifs (17 061 ÷ 9 vertes, n=9/18) » au rapport de l'atelier, au registre
   (un fichier de décomposition dédié) et à la ligne CIB-EDIT-OPT16 de
   CIBLES.md — l'arbitrage tokens/faisabilité CONSIGNED (politique
   lexicographique : un gain token acheté par une perte de faisabilité est un
   arbitrage nommé, pas une tenue silencieuse).
4. **C30 N-VALUE ET C31 CLAIM-SCOPE RECONSTRUITS** — controles_w28c du linter
   v4 (append-only) : le code de la session morte fut perdu avec le bac (le
   complet v0.33.0 ne le porte pas) ; la reconstruction se calibre sur les
   mutations attendues de la porte v330 (le n= retiré de « median 27.5 native
   tokens over the eighteen tasks, n=18 » → refus C30 ; la revendication
   « This study presents the first system ever. » sans scope → refus C31) et
   ne produit AUCUN refus sur les cinq pièces v0.33.0.
5. **C32 RATIO-RECOMPOSE** — nouvelle classe du linter : TOUT ratio canonique
   publié (4,56×, 77×, 1 056×, 13,6×, 123×, 1,41×, 2,68×, 2,47×, 1,31×,
   1,07×, 2,89×, 24,5×, 3,22) se recompose de ses opérandes non arrondis lus
   aux registres ; son contrôle négatif : un ratio volontairement faux refuse.
6. **L'ÉDITION CORRECTIVE v0.33.1** — le patron v0.23.4 : les quatre pièces
   aux sources inchangées RECONDUITES byte-byte (manuscrit v0.33.0,
   spécification v0.15.18, Livre v1.17, présentation v0330) ; la pièce
   preuves RÉGÉNÉRÉE (elle lit les rapports corrigés verbatim) à v0.33.1 ;
   pack-v331/ ; la porte V1..V7 + L1..L32 zéro rouge, VINGT-TROIS mutations
   refusées (les vingt-deux reconduites + la mutation C32) ; le manifeste
   empreintes v0.33.1, le rapport de vérification, le LISEZMOI ; les trois
   packs assemblés (soumission / présentation / complet v0.33.1) ;
   depot-zenodo-v0331/.
7. **LA VÉRIFICATION** (avant tout commit de close, l'ordre du prompt) :
   la porte complète zéro rouge ; les cinq sondes de W28ATTR et les contrôles
   négatifs des ateliers rejoués bit-identiques ; sceau_I verifier 14/14 avant
   et après ; chaque ratio corrigé recalculé indépendamment du fichier source
   et confronté à la valeur imprimée ; git diff : aucun octet hors des zones
   autorisées (les rapports, les registres nommés, CIBLES.md, JOURNAL_OPT,
   le linter, la chaîne v331, le pack-v331) ; le /instructions du coffre
   laissé tel quel (les évaluations y demeurent : elles ne sont PAS consommées
   par la présente — la vague 29 aux sept prompts attend le geste du maître).
8. **LE DÉPÔT ET LA CONSIGNATION** — le set v0.33.1 au /livrables du coffre
   (au jeton relais, recoup byte-byte) ; le set v0.33.0 supersédé au lot
   ARCHIVE ; l'Entrée au worklog ; OU-TROUVER + REPRISE mis à jour ; le
   miroir resynchronisé, le push GitHub, les trois bords vérifiés.

**LES INTERDITS** (les règles qui ne se marchandent pas, reconduites) : aucun
artefact scellé touché (sceau-I 14/14 avant et après chaque geste) ; aucune
cible re-tirée ; aucun verdict fabriqué ; aucune valeur mesurée modifiée au-delà
des résidus nommés (l'erratum documente chaque correction, l'ancienne valeur
demeure lisible) ; aucun secret commis ni affiché ; l'ordre des étapes jamais
re-tiré.
