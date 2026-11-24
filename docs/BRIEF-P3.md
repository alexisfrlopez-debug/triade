# LOT P3 — les harnais par bloc (confié à Claude, 24/11/2026)

## Ce que c'est
TRIADE écrit la notation d'assemblage directement, et vérifie par un **oracle** (émulation
différentielle Unicorn) ce que le binaire scellé fait. 320 vecteurs ont été produits, dont 235
sont exécutables ; au contexte **générique**, 95 seulement s'exécutent : 27 blocs fautent en
`UC_ERR_READ_UNMAPPED` / `UC_ERR_FETCH_UNMAPPED`, parce que le harnais ne leur fournit pas le
contexte que leur spécification d'intention (couche I) nomme — entrées d'IAT citées
(`kernel32!X`, `ws2_32!Y`), globales `.data`/`.rdata`, arguments de pile.

## L'objectif (pré-enregistré, non re-tirable)
Passer de **95/235** à **≥ 200/235** vecteurs exécutés, en synthétisant un harnais **par bloc**
depuis la carte et la spécification I. Si la cible est manquée, publier le manque et la cause par
bloc — jamais re-tirer la cible.

## Le lot tourne tel quel
    cd lot-p3
    python3 scripts/vague23/harnais_par_bloc.py

Il doit afficher exactement : `95/235 vecteurs exécutés (avant 95, delta +0) · blocs sans
exécution 27`. C'est le point de départ vérifié. Dépendance : `unicorn` 2.1.4 (`pip install
unicorn==2.1.4` s'il manque).

## Les contraintes, non négociables
1. **Ne jamais modifier** `m*/notation/`, les binaires scellés ni `pack-v310/`. Le harnais vit en
   copie de laboratoire ; R4/R7 du protocole interdisent de déplacer une adresse scellée.
2. **Pré-enregistrer** : écrire le sha256 du plan de harnais AVANT toute mesure, dans un fichier
   daté du lot.
3. **Agrégateur fail-closed** : un bloc non mesuré n'est pas un bloc vert ; un compte se recompose
   des fichiers, jamais à la main.
4. **Aucun chiffre inventé, aucune cible re-tirée, aucun contrôle retiré.**
5. Les blocs déjà verts doivent reproduire leurs résultats ligne pour ligne (régression = refus).

## Ce qu'il faut rendre
- Un tableau par bloc : identifiant, vecteurs, exécutés, fautes, cause nommée.
- Les comptes recomposés (total, exécutés, blocs fautifs) et le delta contre 95.
- Les sha256 des fichiers produits, et la liste des commandes exactes.
- Un court rapport (10-20 lignes) qui dit ce qui a marché, ce qui reste, et pourquoi.
Poste tout dans le fil sous le message de brief et mentionne `@[Spark](agent_k7k2ajpvcvet)`.

## Honnêteté attendue
Si 200 n'est pas atteint, dis-le et donne la cause par bloc. Si un harnais synthétisé casse une
hypothèse du profil (par exemple une adresse d'IAT hors de la plage du bac), refuse nommément au
lieu d'adapter en silence.
