# PLAN GELÉ — W27PREUV (preuves symboliques complètes — sécurité)

> Évaluation du pack — prompt 5 de la vague 27 (26/11/2026). INCOMPLETE demeure INCOMPLETE
> tant que la preuve n'est pas close ; aucun verdict fabriqué ; tout verdict dérivé de
> PREUVES-STATUTS.json, jamais tapé.

## Geste
1. DÉCOMPOSER LES LEMMES L1/L2 en sous-lemmes de connaissance bornée — la décomposition du but
   attaquant, les bornes d'évaluation partielle — pour franchir le mur 4 Gio : le modèle
   CF3-v3 porteur de sous-lemmes NOMMÉS, chacun vérifiable dans le budget, la décomposition
   consignée (chaque sous-lemme, sa borne, l'articulation vers L1/L2).
2. LE KIT DE RUN MACHINE RÉELLE à empreinte de modèle consignée : les commandes exactes, les
   budgets nommés, l'empreinte sha256 du modèle décomposé, l'attendu de sortie — le run se
   rejoue à empreinte identique.
3. EXÉCUTER LE PORT PROVERIF LIVRÉ (six requêtes actives, événements miroir, oracle de seuil)
   sur machine réelle ou budget mémoire suffisant : tentative d'installation au bac (le bac
   dispose de 4 Gio — le mur de Tamarin, pas celui de ProVerif) ; si le prouveur demeure
   absent : le kit prêt, le statut demeurant dérivé du registre (run NON exécuté).
4. TOUT VERDICT DÉRIVÉ DE PREUVES-STATUTS.json : le registre est mis à jour uniquement par un
   run vécu (empreinte du modèle recoupée avant/après), jamais par frappe.

## Critères d'acceptation
- Les sous-lemmes écrits, leurs bornes nommées ; l'empreinte du modèle décomposé consignée.
- Rejeu des runs à empreinte identique (si un run vit au bac : bit-identique au rejeu).
- CONTRÔLES NÉGATIFS : modèle muté → contre-exemple attendu (le juge doit le voir).
- Statut recomposé par C23/C26 depuis le registre ; consignation append-only.
- INCOMPLETE demeure INCOMPLETE tant que la preuve n'est pas close ; aucun verdict fabriqué.
