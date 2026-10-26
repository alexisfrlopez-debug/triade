# Rapport de vérification interne — Article TRIADE v0.4 (édition académique)

> **Objet** : vérification du manuscrit `scripts/article_v04/` (sources LaTeX)
> et du PDF `docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf` avant
> empaquetage, conformément à la tâche 4 de la demande du développeur
> (évaluation externe du PDF de démonstration v0.3).
> **Date** : 26 octobre 2026. **Vérificateur** : agent Z.ai (GLM), chaîne de
> vérification scriptée + inspection visuelle assistée.
> **Statut du document vérifié** : v0.4 = édition académique du protocole —
> restructuration IMRAD, formalisation, travaux connexes, menaces sur la
> validité ; le noyau normatif (couches, règles, boucle) est inchangé depuis
> la spécification v0.3.

---

## 1. Conformité structurelle (IMRAD / standards ICSE-FSE)

| Exigence | Statut | Détail |
|---|---|---|
| Résumé (abstract) 150–250 mots | ✅ | 246 mots, pleine largeur sous le bloc titre |
| Mots-clés | ✅ | 6 mots-clés, style ACM |
| Introduction avec contributions explicites | ✅ | C1 formalisation, C2 étude de cas, C3 reverse-specs, C4 auto-évaluation critique |
| Travaux connexes (Related Work) avec positionnement | ✅ | 4 sous-sections (dette technique, DbC, AISE, positionnement) + tableau comparatif (Tableau 1) |
| Méthodologie formalisée | ✅ | 7 définitions/invariants numérotés, 5 équations, système de transitions, algorithme 1 |
| Étude de cas avec questions de recherche et design déclaré | ✅ | RQ1–RQ3 ; design monocasal cité Yin et Runeson-Höst ; instrumentation décrite |
| Discussion séparée des résultats | ✅ | §5, distincte de §4 |
| Menaces sur la validité (Wohlin et al.) | ✅ | 5 sous-sections dont l'écart conceptuel source/native en §6.5 |
| Conclusion avec perspectives | ✅ | réplication / réalisation M0–M7 / instrumentation |
| Références numériques complètes et toutes citées | ✅ | 29 entrées, zéro non citée, zéro `[?]` |
| Ordre IMRAD | ✅ | vérifié programmatiquement (positions croissantes) |
| Flottants légendés et référencés dans le prose | ✅ | 5 tableaux, 1 figure, 1 listing, 1 algorithme — chacun référencé |
| Signaletique française cohérente | ✅ | « Tableau », « Algorithme », « Listing », « Figure » (renommés en préambule) |
| Métadonnées PDF (titre, auteurs, sujet, mots-clés) | ✅ | posées à la fusion (`merge_cover.py`) |
| Aucune marque de processus (IA, versions internes, brouillon) | ✅ | la mention « édition académique v0.4 » est une donnée de contenu (numérotation de la série), pas une marque de génération |

**Écarts assumés** : (a) le document est rédigé en français — langue de la
série documentaire du projet ; les équivalents académiques anglais sont
donnés aux premières occurrences (dette technique, conception par contrat,
vérifie-puis-écrit…) ; (b) la couverture sombre de série (Template 03
académique) précède le corps — un article soumis l'omettrait, un document
de collection la conserve ; (c) les artefacts ne sont pas publiés
(dépôts privés), l'availability est déclarée honnêtement en note
d'affiliation.

## 2. Audit des affirmations du document original (v0.3 démonstration)

Chaque affirmation notable du PDF v0.3 a été reprise, sourcée ou nuancée.
Aucune n'a été conservée à l'identique si elle excédait sa preuve.

| Affirmation (v0.3 démo) | Traitement v0.4 | Localisation |
|---|---|---|
| 42 modules cartographiés, 44 spécifications | repris, sourcé (Tableau 4) | §4.4 + nuance §6.1 (métrique proxy, instrument/objet partiellement confondus) |
| 437 tests contre 228, 0 avertissement | repris, sourcé (Tableau 4) | §4.4 + nuance §6.1 (aucune mesure de couverture de code collectée) |
| Parité fonctionnelle 14/14 familles | repris | §4.4 + nuance §6.1 (audit guidé par le README, pas une équivalence formelle) |
| Empreintes md5 identiques, reproductibles par des tiers | repris | §4.4 |
| « Zéro régression » | **reformulé** : zéro régression borné par l'étendue de la suite et de l'audit | §6.4 |
| L'oracle révèle des défauts invisibles (caractère hôte, verrouillage Windows) | repris (2 cas) | §4.3.3, §4.4 + nuance §6.2 (pas de condition témoin) |
| La gouvernance survit à la réinitialisation de l'environnement | repris (récit factuel) | §4.2 |
| La séquence v3.0.0→v3.0.2 « valide le mécanisme d'échec honnête » | repris **et borné** : événement unique, généralité non démontrée | §4.4 + §6.4 |
| 152× temps réel, zéro allocation sur 100 000 blocs | repris **et requalifié** : micro-benchmarks meilleur-cas sur infrastructure partagée 2 vCPU | §4.4 + §6.4 |
| Le refus D15 (fusion modules / natif machine) illustre la fonction objectif | repris comme illustration de la définition 3.3 | §3.2 + §4.2 |
| « Conversion systématique » de la classe « contrat non écrit » | **affaibli** : établi sur les trois comparatifs et l'extension ; sélection des comparatifs déclarée | §5.1 + §6.2 |
| Coût marginal faible du diagnostic D8 | repris, marqué qualitatif | §5.3 (« aucune mesure comparative du coût total n'a été tentée ») |
| L'anti-enfermement « n'est pas théorique » | repris (restauration sans perte) | §5.1 |
| Le titre v0.3 laissait entendre que « le protocole v0.3 [était] démontré » | **corrigé** : distinction explicite couche de gouvernance validée / cœur natif non validé | §6.5 (écart conceptuel) |
| Budgets tokens (40 / 3 000 / 6 000) présentés comme contraintes opérantes | **requalifiés** : cibles de conception, aucune mesure réelle | §3.4 + §6.5 |
| Cristallisation -dev.N, reverse-specs, partage de fixtures | repris comme enseignements entrés au journal | §5.4 |

Le changement de niveau de preuve le plus important porte sur le rapport
démonstration/protocole : la v0.3 pouvait laisser croire que la
démonstration RoomEq validait le programme « natif » du protocole ; la
v0.4 interdit cette lecture (§6.5) — la démonstration valide la
gouvernance, les jalons M0–M7 restent ouverts.

## 3. Cohérence terminologique

Contrôles programmatiques (`scripts/article_v04/verify_article.py`,
exécution : **44 PASS / 0 FAIL**) :

- **Termes pivots présents et stables** : verrou croisé (9), couche I/B/C,
  vérifie-puis-écrit (3), oracle éphémère, cristallisation (7), fonction
  objectif lexicographique (4), spécifications d'intention (4),
  adresses stables (4), reverse-specs (4), patch à contrat stable.
- **Variantes interdites absentes** : aucun « cross-lock » (l'équivalent
  anglais n'apparaît pas dans le corps), aucun « refactoring »
  (« refactorisation » retenue), aucun verrou « croise » sans accent.
- **Équivalents anglais donnés une fois** aux premières occurrences, puis
  français exclusif ; liste blanche d'anglicismes techniques assumés
  (commit, tag, diff, build, token, WYSIWYG, round-trip…) — 0 terme
  anglais intrus détecté hors liste blanche.
- **Notation mathématique uniforme** : $\mathcal{I},\mathcal{B},
  \mathcal{C},\mathcal{D}$ pour les couches (macros `\IB` etc.),
  $\kappa(S)$ pour la cohérence, $\mathcal{O}_{\mathcal{I}}$ pour
  l'oracle, $\succ_{\mathrm{lex}}$ pour l'ordre lexicographique —
  définies en §3 puis réutilisées à l'identique en §4–§6.
- **Numérotation** : Définitions/Invariants chaînés (3.1–3.4), équations
  (1)–(8), RQ1–RQ3, C1–C4 — aucune référence croisée non résolue.

## 4. Contrôles automatisés et inspection visuelle

| Contrôle | Résultat |
|---|---|
| `poster_validate.py check-tex` (8 fichiers sources) | 0 erreur, 0 avertissement |
| Compilation Tectonic (3 passes, via `pdf.py convert.latex`) | 0 erreur ; 0 overfull |
| Références croisées / citations (`??`, `[?]`) | 0 / 0 |
| Clés `\cite` ↔ `refs.bib` | 29/29 résolues, 0 non citée |
| `pdf_qa.py --skip-cover --formulas` | 11 contrôles passés, 0 erreur (avertissements : voir §5) |
| `pages.clean` | 0 page blanche |
| `font.check` | 0 glyphe manquant |
| Couverture : `check-html` + `cover_validate.js` | PASS après correction d'un écart texte-ligne (23,5 px → 42,5 px ≥ 1U) |
| Taille de page homogène | 12 pages A4 exactes (normalisation 0,5 pt à la fusion) |
| Inspection visuelle (VLM, 5 pages : couverture, titre, méthodologie, listing, bibliographie) | 5/5 sans défaut — accents, guillemets, colonnes, cadres, flottants |

## 5. Avertissements résiduels (justifiés)

1. **`pdf_qa` : « formula overflow » (11×)** — faux positif structurel : le
   vérificateur suppose une colonne unique ; la colonne droite d'une page
   bicolonne dépasse naturellement sa marge de contenu monocolonne. Vérifié
   géométriquement : aucun texte au-delà de la marge physique (la
   protrusion microtype ≤ 1,8 pt est une fonctionnalité typographique).
2. **`pdf_qa` : tiret cadratin en début de ligne (10×)** — règle CJK ;
   en typographie française, un tiret d'incise en début de ligne est
   licite. L'unique cas de la page 1 a été éliminé par reformulation.
3. **`pdf_qa` : « table not centered » (1×)** — tableau de colonne droite,
   centré dans sa colonne (faux positif bicolonne).
4. **6 lignes légèrement lâches** (badness 1 100–2 300, seuil de signalement
   1 000) — justification française en colonnes étroites avec jetons
   techniques insécables (`Path.GetInvalidFileNameChars()`…) ; impact
   visuel négligeable, inspecté et validé visuellement.
5. **3 avertissements `algorithm2e.sty` UTF-8** — octets non UTF-8 dans les
   commentaires du paquet lui-même, jamais composés dans le PDF.

## 6. Décision

Tous les contrôles bloquants sont au vert ; les affirmations du document
original sont sourcées, reformulées ou nuancées ; la terminologie et la
notation sont stables d'un bout à l'autre. **L'empaquetage est autorisé** :
copie du PDF final dans `docs/`, livrable `download/`, mise à jour de la
gouvernance (D18) et sauvegarde systématique (commit + Drive + GitHub).

La régénération de ce document est manuelle (hors D17, comme le PDF de
démonstration) : `scripts/article_v04/` contient l'intégralité des sources
(main.tex, sections, refs.bib, cover.html) et des scripts
(`merge_cover.py`, `verify_article.py`).
