# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 11, L'INSTRUCTION o5apue194 : LA PROSE DOMINANTE DE L'OPÉRATION ÉDITER — LE GABARIT VERSIONNÉ, LE LOCALISER HIÉRARCHIQUE, L'AJOUT PAR SQUELETTE

> Pré-enregistré AVANT toute mesure (l'empreinte sha256 consignée à
> EMPREINTES-PLANS-VAGUE11.txt, commitée AVANT la première donnée — la
> graine 20261117 reconduite, l'ordre jamais re-tiré).

## 1. LE CONSTAT (la motivation mesurée)

Éditer-F2 : 1 146 tokens totaux dont LA PROSE DOMINE (866 cl100k sur 1 146 —
la consigne en langue naturelle) ; le matériau déjà réduit (239). LE LEVIER
NOMMÉ par la vague 10 : la prose. Les trois opérations mesurées : ÉDITER
(1 146), LOCALISER (1 103), AJOUTER (3 674 opérationnel).

## 2. LE GABARIT VERSIONNÉ (l'éditer-T2)

LA CONSIGNE EN LANGUE NATURELLE REMPLACÉE par un gabarit versionné : (1) LE
CORPS DU GABARIT (la grammaire du format hunk, l'exemple complet, les
règles d'ancre — la prose actuelle) vit UNE FOIS par session, identifié
TPL-EDIT-v1 + son sha256 GRAVÉ AU PROMPT (la garde) ; (2) CHAQUE opération
porte SEULEMENT : l'ID du gabarit, l'empreinte, LES PARAMÈTRES LITTÉRAUX
(bloc, ligne, l'ancienne ligne, la nouvelle ligne — le diff lui-même) ;
(3) L'EXPANSION CÔTÉ CLIENT : le client recoupe l'empreinte du gabarit
(fail-closed — GABARIT-DIVERGENT si la session diverge), applique les hunks,
round-trip ; (4) LE REFUS NOMMÉ HORS-FORMAT : toute réponse hors grammaire
du gabarit = refus au premier nom. La fenêtre ±12 lignes et l'empreinte
sha256 de la notation DEMEURENT (aucun contrôle retiré).

## 3. LE LOCALISER HIÉRARCHIQUE (le localiser-H)

L'INDEX GROSSIER : les IDs + les empreintes COURTES (8 hex) de tous les
blocs — UN document compact par session (l'empreinte sha256 en garde) ;
L'ENTRÉE FINE : le pointeur seul (l'ID + l'empreinte complète) après choix
de l'entrée. La réponse : le pointeur littéral (le record 52). Le contrôle :
l'expansion côté client recoupée (le même oracle que le pointeur seul —
POINTEUR-INCONNU, HORS-FORMAT, EXPANSION-DIVERGENTE re-roulés).

## 4. L'AJOUT PAR SQUELETTE (l'ajouter-S)

LE SQUELETTE DÉTERMINISTE DÉRIVÉ DE LA COUCHE I : le cadre ABI (le
prologue/épilogue aux non-volatils sauvés, le shadow space), les types, la
signature — générés par le client depuis la spec I du bloc ; L'AGENT NE
REMPLIT QUE LA LOGIQUE (le corps entre les balises du squelette) ; le
client assemble le squelette + la logique, round-trip, oracle régénéré. La
mesure rapporte la décomposition squelette/logique/prose.

## 5. LA MESURE (le protocole, gelé)

n=18 PAR OPÉRATION (éditer : AVANT F2 re-mesuré à la même graine PUIS T2 ;
localiser : P puis H ; ajouter : H3 le record PUIS S) ; LA MÊME GRAINE
20261117, l'ordre jamais re-tiré ; le tokenizer natif LU du champ usage
(chaque appel journalisé) + cl100k PARALLÈLE ; LA DÉCOMPOSITION
matériau/prose/réponse consignée séparément ; la re-tokenisation
indépendante à ±1. LA VÉRIFICATION : 18/18 verts exigés (les refus nommés
consignés — jamais re-tirés) ; zéro divergence comportementale ; round-trip
100 % ; LES QUATRE REFUS DU POINTEUR re-roulés ; la garde sha256 de la
fenêtre conservée ; l'oracle régénéré ; AUCUN contrôle retiré.

## 6. LA VÉRIFICATION APRÈS MODIFICATION (la lettre de l'instruction)

Re-tokenisation indépendante à écart ≤1 ; zéro divergence sémantique
(l'oracle vert sur tous les vecteurs) ; les quatre refus du pointeur
re-roulés verts ; le contrôle négatif de dépendance hors fenêtre (une
définition référencée hors ±12 lignes mutée → refus nommé ou expansion) ;
les budgets publiés avec n et graine ; journal OPT + décision.
