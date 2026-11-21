# PLAN GELÉ — PGODGK35L (la vague 12)
> TPL-ADD-v2 : le squelette déterministe dérivé de la couche I PLUS un dictionnaire de domaine versionné — combler le gap nommé de o5apue194 (ajouter-S 3/18 verts).
> Gelé AVANT toute mesure, graine 20261117 reconduite, ordre jamais re-tiré.

## Le mandat
Le gap nommé de o5apue194 : ajouter-S rend 3/18 verts, les 15 refus sont hors-format
(étiquettes inconnues, constantes du domaine hors portée). Construire TPL-ADD-v2 :
le squelette déterministe dérivé de la couche I (cadre ABI, shadow space, signature)
PLUS un dictionnaire de domaine versionné — les étiquettes et constantes admissibles du
bloc vivent comme IDs littéraux (LBL-xxx, CST-xxx) dans le matériau, l'agent émet des
IDs, le client expande et recoupe l'empreinte sha256 du dictionnaire (fail-closed :
ID-INCONNU, DICT-DIVERGENT, EXPANSION-DIVERGENTE, HORS-FORMAT nommés). Le sha256 du
gabarit et celui du dictionnaire sont gravés au prompt. AUCUN contrôle retiré : fenêtre
±12, empreinte de la notation, round-trip, juge du cadre demeurent.

Mesurer sur les 18 mêmes tâches au tokenizer natif (champ usage lu à chaque appel,
cl100k parallèle, re-tokenisation indépendante ≤1) : médiane, prose/matériau, verdicts,
faisabilité. Cible pré-enregistrée : faisabilité ≥15/18 verts, coût ≤1 500 natifs ; si
la cible n'est pas atteinte, le gap résiduel est nommé par classe de refus, jamais
re-tiré. Consigner OPT-xx au journal et D2xx append-only.

## Les gestes
1. Ce plan gelé AVANT toute mesure (graine 20261117, les 18 mêmes tâches que la vague 11,
   l'ordre jamais re-tiré).
2. Atelier atelier-ajouter-v2-pgodgk35l/ : le squelette TPL-ADD-v2 (cadre ABI msx64,
   shadow space, signature, épilogue), le dictionnaire de domaine versionné (les
   étiquettes LBL-xxx et constantes CST-xxx extraites des notations réelles du domaine),
   les empreintes sha256 du gabarit et du dictionnaire gravées au prompt.
3. Le client de campagne v2 : expansion des IDs, recoup de l'empreinte du dictionnaire,
   les quatre refus nommés (ID-INCONNU, DICT-DIVERGENT, EXPANSION-DIVERGENTE,
   HORS-FORMAT), la fenêtre ±12 et l'empreinte de la notation et le round-trip et le
   juge du cadre DEMEURENT.
4. La campagne : les 15 refus v1 re-roulés sur le client v2 (chaque refus nommé
   re-productible ou converti vert sur pièce), les 3 verts v1 re-roulés (round-trip
   exact octet pour octet, cadre ABI vérifié), la mesure au champ usage du CLI,
   re-tokenisation indépendante.

## La vérification après modifications
- les 15 refus de la campagne v1 re-roulés sur le client v2 → chaque refus nommé
  re-productible ou converti vert sur pièce ;
- les 3 verts v1 re-roulés → round-trip exact octet pour octet, cadre ABI vérifié ;
- contrôles négatifs plantés (ID inconnu, dictionnaire muté d'un octet, expansion
  divergente, ligne hors forme) → REFUS nommés aux quatre faces ;
- re-tokenisation indépendante écart max 0 (≤1 exigé) ;
- sceau 14/14 avant/après, aucune couche I touchée (le dictionnaire vit au client de
  campagne) ;
- les médianes publiées avec leurs valeurs non arrondies.

## Les refus
Aucun re-tirage ; aucun contrôle retiré ; la cible pré-enregistrée falsifiable ; le gap
résiduel nommé par classe de refus si la cible manque.
