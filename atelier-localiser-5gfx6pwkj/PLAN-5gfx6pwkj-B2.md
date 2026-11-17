# PLAN PRÉ-ENREGISTRÉ B2 — LE MODE MINIMAL AMENDÉ (la seconde passe de 5gfx6pwkj)
## Quatre champs LITTÉRAUX, aucun calcul — la carte fait l'arithmétique

**LA FALSIFICATION DE LA PASSE 1** (RAPPORT-5gfx6pwkj-PASSE1.txt, consigné
tel quel — l'instruction l'exigeait) : le mode B exigeait de la réponse la
PLAGE CALCULÉE [slot, slot+taille) — le modèle A CALCULÉ ET S'EST TROMPÉ :
12 plages fausses sur 18 (l'addition hexadécimale tête : 0x4440+0x180 rendu
0x45a0 ; 0x4240+0x140 rendu 0x4360 ; 0x5c00+0x480 rendu 0x6600…) et 6 noms
hors forme (la description du bloc recopiée au lieu du nom) — **18/18
divergences, la règle zéro-divergence FALSIFIÉE** ; le gain directionnel
TENU (le total −41,0 %, la réponse −96,8 % : 792 → 25 tokens) ; la
confrontation aux octets réels VERTE 18/18 (les plages attendues
vérifiées contre loupe.exe — le code réel au slot, le padding NOP, aucun
int3 instruction).

**LA LEÇON** (le mécanisme nommé) : le point de défaillance n'est pas le
format minimal — c'est L'ARITHMÉTIQUE demandée à la réponse. Un champ
calculé (la fin du slot) est un champ faussé ; la carte existe PRÉCISÉMENT
pour faire cette vérification — qu'elle fasse aussi le calcul.

## LE MODE B2 (le gabarit gelé — la réponse porte QUATRE CHAMPS LITTÉRAUX)

```
L'OPÉRATION LOCALISER DE LA CARTE TRIADE (le mode minimal — la réponse tient
en une ligne, la carte confronte la réponse aux octets réels).

BLOC DE LA CARTE (entête lu du fichier même) :
{ENTÊTE}

REQUÊTE : localise le bloc ci-dessus dans la carte et réponds AU FORMAT
MINIMAL, une seule ligne exactement :
IDENTIFIANT · NOM · SLOT · TAILLE
— IDENTIFIANT : l'identifiant de bloc de la carte (la forme iNNNNNN de
l'entête) ;
— NOM : le nom du bloc (le premier champ de la première ligne de
l'entête, la forme loupe-NN-mot) ;
— SLOT : l'adresse RVA du slot, telle que la deuxième ligne de l'entête
la porte (la forme 0x…) ;
— TAILLE : la taille du slot en octets, le nombre tel que l'entête le
porte.
AUCUN CALCUL — recopie les quatre champs tels quels ; la carte fait le
reste. Rien d'autre.
```

LA DIFFÉRENCE B1 → B2 : la réponse ne porte QUE des champs LITTÉRALEMENT
présents dans l'entête (l'identifiant, le nom, le slot, la taille) — la
PLAGE [slot, slot+taille) est CALCULÉE PAR LA CARTE (la vérification
d'adresse demeure : la plage calculée confrontée à la vérité-terrain ET aux
octets réels de loupe.exe — le contrôle 5.3 de la passe 1, inchangé).

## LE PLAN DE MESURE (le même cadre, la passe 2)

- Les MÊMES 18 blocs, LA MÊME GRAINE 20261117 (le même ordre), le MÊME
  instrument (compter_tokens — le natif lu du champ usage, journal et garde
  brute à l'atelier), n=18 (≥15) ;
- Le mode A N'EST PAS RE-MESURÉ : la passe A de la campagne initiale fait
  foi (les mêmes blocs, la même graine, le même instrument — l'appariement
  A/B2 est l'appariement A/B1) ;
- Le gabarit B2 ci-dessus GELÉ (aucun champ calculé) ;
- LES DISTRIBUTIONS : n, médiane, q1, q3, min, max — le total natif, la
  réponse seule, le cl100k parallèle.

## LES RÈGLES DE VERDICT (pré-enregistrées, falsifiables)

- **ZÉRO DIVERGENCE exigé** : la réponse doit être UNE ligne
  `iNNNNNN · loupe-NN-mot · 0x… · N` avec les QUATRE champs EXACTS (l'id,
  le nom, le slot, la taille de la vérité-terrain) — la plage calculée par
  la carte doit tomber aux octets réels (le contrôle 5.3 vert, déjà vécu) ;
  une réponse non parsable est une divergence (fail-closed) ;
- **LE GAIN** : 1 − médiane(total B2)/médiane(total A), lu des logs bruts ;
- **L'ATTENTE** (falsifiable) : la réponse B2 ≈ 30 tokens (quatre champs
  contre trois — un peu plus longue que B1), le total ≈ le total B1 —
  l'attente : −38 à −45 % contre A, SANS divergence cette fois ;
- **SI B2 diverge encore** : le résultat consigné tel quel — la conclusion
  serait que le format une-ligne lui-même est en cause (la discipline de
  forme du modèle), et le mode minimal REJETÉ en l'état (la règle d'arrêt
  D207 : un mode qui exige une re-vérification systématique coûte plus
  qu'il n'économise).

## LA CONSIGNATION

- **D212** : le présent plan B2, empreinte consignée AVANT la mesure (la
  falsification de la passe 1 citée, l'amendement nommé) ;
- **OPT-02** (le journal canonique) : LA CAMPAGNE ENTIÈRE — la passe 1
  falsifiée ET la passe 2, le format D205 (la mesure avant, le gain mesuré,
  le vérificateur) ;
- l'atelier : les journaux des deux passes AU MÊME fichier (l'ordre
  chronologique fait foi), les rapports des deux passes.
