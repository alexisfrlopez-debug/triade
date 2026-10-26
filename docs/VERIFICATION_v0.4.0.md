# Rapport de vérification — Protocole TRIADE v0.4.0

> **Objet** : vérification post-révision de la spécification v0.4.0 (tâche 4 du cahier
> des charges), avant sauvegarde finale. **Vérificateur** : `scripts/spec_v040/
> verify_spec.py` (contrôles mécaniques sur les sources markdown, le PDF formel et le
> journal des décisions) — **64 contrôles PASS / 0 FAIL**. **Date** : 26 octobre 2026.

## Les neuf critères du cahier

### V1 — Hiérarchie Sécurité > Performance > Optimisation > Coût en tokens respectée

**PASS.** La hiérarchie apparaît à l'identique (3 occurrences dans la spécification,
présente dans le PDF formel) et est désormais consignée comme **invariant de révision**
(D19) : aucune révision future ne peut la modifier sans invalider explicitement le
protocole entier. Aucune formulation alternative concurrente n'existe dans le document.
Le contrôle programmatique vérifie les deux.

### V2 — Les trois couches I/B/C restent indissociables

**PASS.** La propriété « aucune couche n'est optionnelle » est passée du statut de constat
(v0.3) à celui de propriété normative (§ 4) : livrer B sans I et C viole R1 ; contourner C
pour éditer B viole R3 et la boucle. Les définitions des trois couches, leurs rôles et le
tableau correspondant sont présents dans la source et le PDF.

### V3 — Aucune règle affaiblie, notamment R5, R8, R9 et R10

**PASS.** Les énoncés v0.3 de R1 à R9 sont repris **à l'identique** (vérifié chaîne par
chaîne). R10 est un **sur-ensemble strict** : les checksums au lancement (v0.3) sont
conservés, augmentés de la signature du manifeste, de l'anti-rollback par monotonie de
version, des contrôles de conformité environnementale et du fail-closed explicite — la
sanction passe de « arrêt de l'exécution » à « arrêt avant tout effet ». R11 s'ajoute sans
toucher aux existantes. Les onze règles figurent dans le PDF formel.

### V4 — Aucune couche d'abstraction à l'exécution introduite

**PASS.** Les mentions de « bytecode portable », « machine virtuelle » ou « couche
d'abstraction à l'exécution » n'apparaissent qu'en contexte de **rejet** (§ 1.2, § 8.3,
§ 17.2, alternatives rejetées de D14 et D22). La parité inter-profils s'obtient par
vérification à contrat constant, jamais par couche intermédiaire.

### V5 — Aucune promesse de portabilité universelle immédiate

**PASS.** La déclaration « le protocole ne promet pas la portabilité, il la vérifie » est
présente ; les seules occurrences de promesses de portabilité immédiate sont dans la table
des rejets (§ 17.2). Chaque profil reste gated : suite de conformité verte obligatoire,
critères M6/M7 inchangés et renforcis (conditions transverses).

### V6 — Aucun mécanisme de furtivité face aux EDR

**PASS.** Toutes les occurrences d'« EDR » et de « furtivité » sont en contexte de
non-objectif ou de rejet (§ 1.2, § 13.2, § 17.2). Aucun mécanisme d'évasion n'est ajouté ;
l'anti-rollback et les vérifications de R10 sont des mécanismes d'intégrité, pas de
furtivité — et restent strictement locaux.

### V7 — Chaque nouvelle exigence vérifiable mécaniquement ou par oracle

**PASS.** Les dix-sept nouvelles exigences ont chacune leurs ancrages de vérification dans
la spécification : gabarit I audité (traçabilité), taxonomie alimentant le tableau de bord,
menaces rattachées aux contre-mesures R10, R11 sanctionnée au commit, journal d'optimisation
consigné avant commit, fragmentation contrôlée par les budgets, localisation par intention
(interdition du balayage = vérifiable par instrumentation), suite de conformité exécutable,
parité vérifiée par exécution, pré-versions contrôlées par le registre des balises,
reverse-specs par statut visible, fixtures par unicité référencée, traçabilité par commande
d'audit (refus de build), journal des décisions par audit de gouvernance, tableau de bord
généré par l'audit.

### V8 — Chaque évolution tracée dans un changelog

**PASS.** La table de correspondance § 17.1 compte exactement 17 lignes (une par
évolution, avec situation v0.3, disposition v0.4.0 et décision), et la ligne v0.4.0 du
journal des versions cite chacune des évolutions, y compris fragmentation, localisation par
intention et budgets tokens.

### V9 — Modifications incompatibles explicitement rejetées et non appliquées

**PASS.** Sept rejets consignés (§ 17.2 + alternatives rejetées des décisions) :
modification de la hiérarchie, couche d'abstraction à l'exécution, promesse de portabilité
immédiate, furtivité EDR, affaiblissement de R5/R8/R9/R10, anti-rollback en ligne,
optimisation sans mesure. Les décisions D19 à D25 sont au format normalisé avec
alternatives rejetées.

## Contrôles complémentaires

| Contrôle | Résultat |
|---|---|
| `poster_validate.py check-tex` (5 sources LaTeX) | 0 erreur, 0 avertissement |
| Compilation Tectonic (2 passes) | 0 erreur ; 0 overfull après correctifs |
| `pdf_qa.py --skip-cover` | 11 contrôles passés, 0 erreur |
| `font.check` | 0 glyphe manquant |
| `pages.clean` | 0 page blanche |
| Couverture : `check-html` + `cover_validate.js` | PASS |
| Inspection visuelle (VLM, 3 pages) | 3/3 sans défaut |
| `build_pdf.sh` (D17/D25) | détection, idempotence et retour arrière testés OK |
| Sommaire | présent en page 2 du corps, numéros alignés, entrées cliquables |

Avertissements résiduels (8) : ponctuation française en début de ligne — tirets cadratins
des itemizes babel-français et incises, convention typographique correcte ; un séparateur
« · » sur la couverture. Aucun n'est un défaut.

## Décision

La révision v0.4.0 est conforme au cahier des charges sur les neuf critères. La
sauvegarde et l'alignement RoomEq (démonstration) sont autorisés.
