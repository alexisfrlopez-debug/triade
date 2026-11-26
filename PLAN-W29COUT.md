# PLAN GELÉ — W29COUT (la lecture économique unifiée + le plancher de faisabilité)

> Vague 29, prompt 5 (dépôt du 27/11/2026, instructions.txt §10 Prompt 5 — suggestions
> A2/D14/D15 de l'évaluation). Aucune valeur mesurée existante n'est modifiée ; aucune
> cible re-tirée. Compléter CIBLES.md et le journal OPT de la lecture économique
> unifiée. Le présent plan gèle l'atelier AVANT toute mesure (la mesure ici est le
> RECALCUL depuis les journaux vivants — les sources canoniques).

## Geste
1. LA TABLE UNIFIÉE : pour chaque opération (localiser / éditer / ajouter) et chaque
   ère (M1 historique-datée, pointeur-seul, contenu-seul, ADOPTÉE, OPT-16, la voie
   structurée EN ATTENTE), publiée côte à côte depuis les journaux :
   - la médiane par tentative (les journaux usage : journal-opt16.jsonl pour OPT-16,
     les journaux des campagnes add/locate des ateliers précédents — les canons de la
     table des ères) ;
   - la FAISABILITÉ (vertes/n) ;
   - LE COÛT PAR CHANGEMENT VALIDÉ (somme des tokens de tous les tours et tentatives
     ÷ vertes — lu des journaux usage, JAMAIS une estimation) ;
   - le temps de vérification et le temps humain quand ils existent aux registres.
2. LE PLANCHER DE FAISABILITÉ PRÉ-ENREGISTRÉ (la cible NOUVELLE, jamais un re-tirage
   de CIB-EDIT-OPT16) : **CIB-EDIT-FAISAB ≥ 15/18** pour l'éditer structuré ; la cible
   de coût par changement validé **CIB-EDIT-AMORTI ≤ 150 tokens** — les deux lignes
   pré-enregistrées AU PRÉSENT PLAN, mesurées à la campagne future (EN ATTENTE du
   décodage contraint — le plan w29decco), AUCUN chiffre fabriqué au présent atelier
   (la faisabilité courante 9/18 et l'amorti 1 896 restent les mesures courantes
   publiées).
3. LES IC BOOTSTRAP 95 % sur les médianes token (B ≥ 10 000 rééchantillons, la graine
   20261128 consignée AVANT le tirage, l'algorithme : le rééchantillonnage des tâches
   du journal-opt16.jsonl à médiane recalculée) ; LES TESTS EXACTS sur les différences
   de faisabilité (le test exact de Fisher bilatéral : 9/18 vs 18/18 ; 5/18 vs 15/18
   attendu — la p-value publiée telle quelle avec sa statistique et ses effectifs).
4. LES n= PORTÉS à la portée de chaque médiane (C30 — la classe vérifie) ; chaque
   ratio RECALCULÉ depuis les opérandes non arrondis (le linter C32 refuse tout
   écart) ; les marges de non-infériorité nommées quand elles s'appliquent (aucune
   fabriquée).
5. LE REGISTRE DE PROVENANCE ÉTENDU : chaque grandeur de la table unifiée recomposée
   depuis sa source canonique (le fichier, la ligne, le champ — la chaîne de recomposition
   rejouable) ; les contrôles mutants refusés (une grandeur mutée à la source → la
   recomposition la refuse).
6. LE TEST DU LECTEUR étendu d'un cas par nouvelle grandeur (l'amorti, l'IC, la
   p-value : un lecteur recompose chacun depuis les opérandes imprimés).

## Critères d'acceptation
- Le rejeu bit-identique du script de calcul (deux passes, la graine consignée) ;
  la porte 32 classes zéro rouge ; le sceau-I 14/14.
- AUCUNE valeur historique réécrite (les ères datées demeurent — les errata
  append-only seuls vivent) ; le test du lecteur VERT par nouvelle grandeur.
- CIBLES.md complété des lignes nouvelles pré-enregistrées (CIB-EDIT-FAISAB,
  CIB-EDIT-AMORTI — EN ATTENTE de la campagne contrainte) ; la table des ères
  complétée de la lecture unifiée ; aucun re-tirage.
