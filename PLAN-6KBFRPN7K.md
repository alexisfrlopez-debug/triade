# PLAN GELÉ — 6KBFRPN7K (la vague 12)
> Les trois corrections de recomposabilité dans les cinq pièces v0.22.0, le linter v220 étendu à la confrontation des ratios.
> Gelé AVANT toute modification. Toute donnée mesurée ou publiée suit ce plan ; tout écart au plan est nommé au rapport.

## Le mandat (l'instruction, résumée fidèle)
Trois corrections de recomposabilité — plus l'alignement du résumé — dans les cinq pièces v0.22.0 :

1. **Publier les canons NON ARRONDIS derrière chaque ratio dérivé**, dans les tables de preuves
   et du manuscrit :
   - le cache round-trip : 283,7 ms → 0,4 ms imprimé donne ×709,2 au lecteur, ×680,6 publié —
     publier la médiane après en ms à trois décimales ;
   - l'ajouter : 3 074 → 2 200 imprimé donne −28,4 %, −28,5 % publié — publier les médianes
     non arrondies ;
   - tout ratio dont le recalcul depuis les valeurs imprimées diverge de plus de 0,05 de la
     valeur publiée.
   Le linter v220 confronte désormais chaque ratio au recalcul depuis les canons non arrondis
   ET depuis les valeurs imprimées (tolérance d'arrondi nommée).

2. **Les tables de décomposition §4 du rapport C+G+** portent l'étiquette « médianes par
   poste — la somme des médianes n'est pas la médiane des sommes ; réconciliation par run au
   registre » (Σ imprimés C+G+ = 18,672 vs 18,678 ; T = 39,405 vs 39,393) ; la réconciliation
   20/20 par run demeure la preuve d'exactitude.

3. **Publier le census exact de la batterie 559 vecteurs** (compte par catégorie sommant à 559
   — la formule publiée 64+3·4·13·3·8·512 ne se recompose pas) dans rapport-corridors et §7
   du manuscrit.

4. **Aligner le résumé français du manuscrit sur l'abstract** : les formats ADOPTÉS sont
   1 053 (pointeur seul, request) / 674 (gabarit) / 2 200 (squelette) ; 1 103/3 374/3 674
   sont l'historique daté v0.17.0/v0.19.6. Étendre le linter aux étiquettes de statut :
   tout nombre marqué « adopté/courant » doit égaler le canon courant ; tout nombre
   historique doit porter sa date de périmètre.

## Les gestes (l'ordre)
1. Recenser les ratios et canons en cause depuis les sources (macros v220, générateurs de
   preuves/présentation, ateliers vague 11) — les valeurs non arrondies lues des JSONL/CSV
   bruts, jamais retapées.
2. Corrections ancrées (REFUS si une ancre manque) : manuscrit (résumé français, §7 census,
   ratios), preuves (tables C+G+ étiquetées, canons non arrondis aux tables), présentation
   v230 en conséquence.
3. Linter v220 → extension : classe « ratio » — chaque ratio publié confronté au recalcul
   depuis (a) les canons non arrondis, (b) les valeurs imprimées, à la tolérance d'arrondi
   nommée (0,05) ; classe « étiquette de statut » — le nombre marqué adopté/courant doit
   égaler le canon courant, l'historique doit être daté.
4. Contrôles négatifs plantés : un ratio faux (divergence > 0,05) et une étiquette « adopté »
   sur un nombre historique — TOUS DEUX REFUSÉS au premier nom.

## La vérification après modifications
- linter re-roulé sur les cinq pièces → zéro divergence ;
- contrôle négatif double refusé au premier nom ;
- recalcul indépendant de chaque ratio publié depuis les canons imprimés non arrondis →
  écart nul ;
- census 559 sommé par code depuis le générateur de vecteurs → 559 exact ;
- sceau 14/14 avant/après ;
- les verbatim des ateliers DEMEURENT octet pour octet (les corrections vivent au texte des
  preuves et au manuscrit, jamais aux rapports historiques).

## Les refus
Aucun chiffre fabriqué ; les canons lus des sources brutes ; le verbatim historique intact ;
la pièce corrigée, jamais le linter.
