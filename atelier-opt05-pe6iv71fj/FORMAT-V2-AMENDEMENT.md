# AMENDEMENT HUNK-v2 — NÉ DES REFUS NOMMÉS DE LA PREMIÈRE PASSE (consigné avant la re-mesure)

## Le constat (la première passe, les pièces au journal)

La première passe du mode HUNK (la grammaire v1 du plan gelé) a vécu
18 appels « editer-A » (VERT : 18/18 round-trip) puis les premiers
appels « editer-H ». LES REFUS NOMMÉS ONT ATTRAPÉ — et le motif est
L'AMBIGUÏTÉ DE LA SPÉCIFICATION, pas l'incapacité du modèle :

1. **« le hunk 1 annonce 1 hunks, il y en a 11 »** (HORS-FORMAT) — le
   gabarit v1 écrivait « @@ hunk 1/<n> » SANS DIRE que <n> est LE
   TOTAL : le modèle a lu « 1/1 » littéralement et numéroté
   « @@ hunk 2/1 », « @@ hunk 3/1 »… — ses hunks étaient sémantiquement
   JUSTES (la pièce au garde-brut : l'ancre exacte, le retrait exact,
   l'ajout exact — loupe-12 : cmp rdx, 0x100 → cmp rdx, 0xff et
   l'étiquette de spec R1 → R2, exactement la tâche gelée) ;
2. **« la ligne « cmp r9, 32 » n'est pas à l'ancre »** (CONTEXTE-
   DIVERGENT) — la sémantique v1 de l'ancre (« une ligne qui précède
   le changement ») n'était pas DITE : le modèle a naturellement pris
   LA LIGNE CHANGÉE ELLE-MÊME comme ancre (base: la ligne, - la
   ligne, + la nouvelle) — sémantiquement propre, grammaticalement
   refusé ;
3. **« la dernière ligne n'est pas FIN-HUNKS »** — le modèle a clos
   d'une phrase de politesse (la classe connue des complétions).

LA LEÇON (la même que B1 à OPT-04 : le point de défaillance n'est pas
le hunk mais LA SPECIFICATION du format) : une grammaire sans exemple
complet et sans sémantique d'ancre explicite fabrique des refus qui
ne mesurent PAS le coût du format, ils mesurent l'ambiguïté de la
spécification.

## L'AMENDEMENT (gelé avant la re-mesure — la grammaire v2)

```
@@ hunk <k>          (k = le rang du hunk, 1, 2, 3… en ordre)
base: <UNE ligne exacte du texte courant — le PREMIER point du changement>
- <une ligne retirée à partir de l'ancre>   [0..m lignes]
+ <une ligne insérée au même point>         [1..p lignes]
…
FIN-HUNKS
```

LA SÉMANTIQUE DE L'ANCRE (explicite, v2) : l'ancre est la ligne OÙ LE
CHANGEMENT SE PRODUIT. Si le hunk porte des lignes « - », la première
d'entre elles EST l'ancre elle-même (la ligne remplacée — le modèle
la répète, la confrontation l'exige) et les retraits suivent dans
l'ordre À PARTIR DE L'ANCRE. Si le hunk ne porte AUCUNE ligne « - »,
l'ancre est la ligne APRÈS laquelle l'insertion se fait. Le client :
(1) cherche l'ancre dans le texte courant — absente : **HUNK-INCONNU** ;
(2) confronte les « - » au texte à partir de l'ancre — tout écart :
**CONTEXTE-DIVERGENT** ; (3) applique, reconstruit, round-trip — tout
écart : **ROUND-TRIP-DIVERGENT** ; (4) la grammaire : **HORS-FORMAT**.
Les QUATRE REFUS NOMMÉS demeurent, fail-closed, le premier l'emporte.

LE GABARIT AU PROMPT porte désormais UN EXEMPLE COMPLET (l'exemple
enseigne ce que la règle seule ne dit pas — la leçon de la passe 1).

## LA DISCIPLINE DE MESURE (inchangée par l'amendement)

La re-mesure vit aux tâches « -H2 » (les 18 appels « editer-H2 » puis
« ajouter-H2 », la même graine 20261117, le même ordre, le même
instrument, n=18 par cellule). LA PREMIÈRE PASSE DEMEURE AU JOURNAL
tel quel (les refus nommés, les pièces brutes) : elle est le record de
l'ambiguïté, jamais effacée. Le rapport rapportera les DEUX : la
passe v1 (le taux de refus nommés, l'ambiguïté sourcée) et la passe
v2 (la mesure du format amendé). AUCUNE valeur de la passe v1
re-qualifiée : les refus étaient VERTUS (le client a refusé ce qu'il
devait refuser selon la grammaire v1).


## LE SECOND AMENDEMENT (consigné avant la re-mesure des cellules ajouter)

LA PREMIÈRE PASSE « ajouter-A » (10 appels vécus avant l'arrêt) : les
notations générées ne s'assemblent PAS (0/10 au round-trip) — LE MOTIF
NOMMÉ : le modèle écrit du NASM (global/extern/section .text/labels à
deux-points/appels symboliques) — la prose des conventions
n'enseigne PAS le format de notation du domaine. LES PIÈCES au
garde-brut (les réponses verbatim). LA LEÇON (la même que B1→B2 à
OPT-02) : le point de défaillance n'est pas l'opération d'ajout, c'est
LE FORMAT que la prose seule n'enseigne pas — L'EXEMPLE L'ENSEIGNE.

LE GABARIT AMENDÉ (v2) porte L'EXEMPLE DU FORMAT : la notation réelle
de loupe-13 (le bloc canonique du domaine, 60 lignes, lue du fichier
même) insérée au prompt comme « L'EXEMPLE DU FORMAT DE NOTATION » —
la carte du domaine porte cet exemple à toute opération d'ajout (le
format vit dans le contexte de travail de l'agent, il n'est pas
re-déduit de la prose à chaque unité). Les cellules re-mesurées :
« ajouter-A2 » et « ajouter-H2 » (la même graine, le même ordre,
n=18). La première passe demeure AU JOURNAL (le record de l'écart, les
pièces verbatim, jamais effacée).
