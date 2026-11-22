# LE GUIDE D'AGENT INDÉPENDANT DU MODÈLE (zd316de39, la vague 15)
*Utilisable par n'importe quel LLM capable — la sonde de capacité AVANT
l'investissement (un modèle trop faible échouera à l'ajouter : conseil
fail-closed, pas gatekeeping — le finding 0/64 du 1.5B fait foi).*

## LES 11 RÈGLES
1. LE POINTEUR SEUL : le contrat d'accès vit à un pointeur — JAMAIS un
   chemin en clair ; SES 4 REFUS (le pointeur nul, hors zone, la taille,
   l'alignement) sont NOMMÉS au refus.
2. UNE INSTRUCTION PAR LIGNE — jamais d'expansion multiple, jamais
   d'opérande mémoire double (un accès mémoire par instruction au plus).
3. LES TROUS TYPÉS : registre / offset / cible LBL-CST — les IDs du
   dictionnaire du bloc, JAMAIS un symbole en clair.
4. LA GRAMMAIRE DES REFUS NOMMÉS : chaque refus porte sa classe
   (HORS-FORMAT, ID-INCONNU, EXPANSION-DIVERGENTE, FORME-INVALIDE) —
   réparer LA CAUSE NOMMÉE, le reste demeure octet pour octet.
5. L'IAT S'APPELLE EN CALL : « call CST-004 » — jamais un IAT en
   opérande cmp.
6. LA SOURCE ÉTROITE : movzx rax, ecx (32 bits ou moins).
7. LES CONSTANTES PAR LE DICTIONNAIRE : « mov reg, CST-001 » — jamais
   WM_PAINT en clair.
8. L'ÉTIQUETTE INTERNE : « LBL-001 : » en MAJUSCULES, à la ligne seule —
   la cible de saut « je LBL-001 ».
9. LE BUDGET : localiser 627 hiérarchique / éditer 674 TPL-EDIT-v1 /
   ajouter 2 200 squelette — les opérandes NON ARRONDIS publiés au
   MANIFESTE du kit.
10. LA BOUCLE EN 7 ÉTAPES : observer le fragment → lire le dictionnaire
    → émettre la notation → LIRE LE VERDICT DU JUGE → si refus : LE DIFF
    (la ligne fautive, la cause nommée) → réparer LA CAUSE SEULE →
    re-soumettre (le budget TROIS).
11. JAMAIS JOUER LE JUGE : la notation mutée d'un octet est ATTRAPÉE
    (la batterie de mutation) — le gain du juge est PERDU, pas gagné.

## LA DÉGRADATION GRÂCIEUSE NOMMÉE
response_format absent au CLI → LA GRAMMAIRE AU PROMPT + les validateurs
(les quatre interdits v3) — JAMAIS un juge affaibli (le constat
TPL-ADD-v4 reconduit : la v4 courait sans response_format, les juges
INTACTS).

## LA SONDE DE CAPACITÉ (AVANT investissement)
1. LA DÉRIVATION DES 128 CONSTANTES depuis les définitions mathématiques
   seules (le protocole peap6ws09) — zéro divergence exigée ;
2. LE SMOKE TEST DE NOTATION (un bloc simple au validateur) ;
3. LA FRONTIÈRE NOMMÉE : le modèle qui échoue la dérivation échouera à
   AJOUTER — le conseil fail-closed, JAMAIS le gatekeeping.

## LE BENCH PRÉ-ENREGISTRÉ EMBARQUÉ
LES 18 TÂCHES locate/edit/add (les blocs du dépôt, les graines
consignées 20261117, l'ordre JAMAIS re-tiré), les juges INTACTS (la
chaîne v2 + les validateurs v3), LE SCHÉMA JSONL append-only (tache,
essai, verdict, tokens natifs, wall), les budgets et périmètres
ÉTIQUETÉS ; LE GEL DE L'EMPREINTE du plan AVANT toute mesure (la ladder
vpcr7mh3t — le plan headline du gym).
