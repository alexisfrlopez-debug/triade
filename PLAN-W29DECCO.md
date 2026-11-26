# PLAN GELÉ — W29DECCO (décodage contraint client-side : éditer + ajouter, le gate d'abord)

> Vague 29, prompt 1 (dépôt du 27/11/2026, instructions.txt « Analyse — TRIADE v0.33.0 »
> §10 Prompt 1 — suggestions A1/A2/C11 de l'évaluation). Le levier unique qui convertirait
> 9/18 et 5/18 en ≥15–17/18 : le décodage contraint CÔTÉ CLIENT (xgrammar sur modèle
> ouvert 7–14B). Le présent plan gèle l'atelier AVANT toute mesure.

## Geste
1. LE MODÈLE OUVERT CHOISI (identifiant ET empreinte consignés au choix, la lettre du
   prompt) : **Qwen2.5-Coder-7B-Instruct** (Qwen/Qwen2.5-Coder-7B-Instruct, Hugging Face).
   L'empreinte consignée : celle du `tokenizer.json` + `config.json` téléchargés au présent
   atelier (les octets mêmes, sha256 — le choix nominal du plan ; AUCUN poids téléchargé,
   AUCUN chiffre de campagne fabriqué). Le bac ne porte PAS le compute du run (4 Gio de
   RAM, 2 vCPU, aucun GPU — la limite STRUCTURELLE nommée, le geste compute appartient au
   poste réel, la doctrine W28RLVR reconduite).
2. LE DÉCODEUR CONTRAIT CÔTÉ CLIENT : **xgrammar** (version pip + sha256 de la roue
   consignés). La grammaire compilée depuis le SCHÉMA FERMÉ D264/OPT-16 ÉTENDU à
   l'opération ajouter :
   - éditer (D264 étendu, W28OPT16 reconduit) : {"op": "substituer", "dst": <id du bloc>,
     "offset": <index de ligne dans la plage>, "src": "<ligne nouvelle>"} ;
   - ajouter (le squelette + dictionnaire du juge D264, scripts/vague19/expandeur_add.py
     sha256 9fc325e2… INTACT — JUGE-MODIFIÉ serait le refus) : l'objet pointeur-seul du
     domaine fermé (op ∈ {mov, add, sub, xor, and, or, cmp, test, jcc, call, ret}, offset
     borné, dst/src du dictionnaire typé).
   La grammaire est compilée sur le vocabulaire du modèle choisi (TokenizerInfo) ; les
   tokens du schéma étendu sont couverts ou l'écart nommé.
3. LA SONDE DE GATE SUR LE NOUVEL ENDPOINT, AVANT TOUTE CAMPAGNE : la violation ordonnée
   (op hors enum — « SUBVERSION-HORS-ENUM » ; offset hors bornes — 999999) doit être
   REFUSÉE AU DÉCODAGE, pas seulement au validateur. La mesure : le masque de bits de
   tokens appliqué par la grammaire compilée (accept ou refuse le token suivant) — la
   violation REFUSÉE AU MASQUE est le verdict VERT du décodeur client ; un décodeur qui
   laisse passer est refusé nommément. La sonde rejouée : verdict bit-identique.
4. LES CIBLES NOUVELLES (sans re-tirage des existantes — CIB-EDIT-OPT16 et CIB-ADD-STRUC
   inchangées au registre) : éditer ≥17/18 vertes à ≤150 tokens natifs médians PAR
   CHANGEMENT VALIDÉ ; ajouter ≥15/18 à ≤3000 tokens (CIB-ADD-STRUC INCHANGÉE — la cible
   de l'atelier la porte telle quelle). Graine 20261117 reconduite, ordre des 18 tâches
   jamais re-tiré, boucle ≤3 tours, le budget usage natif (le compte est le LOG).
   PRÉ-ENREGISTRÉ AU PRÉSENT PLAN : ces cibles ne seront mesurées QUE par la campagne au
   modèle ouvert — le bac n'en mesurera AUCUNE (aucun chiffre fabriqué).
5. LA CAMPAGNE (le geste compute) : le modèle ouvert en génération CONTRAINTE par la
   grammaire du point 2, les deux opérations mesurées côte à côte (médiane par tentative,
   faisabilité vertes/n, coût par changement validé, refus par classe). AU BAC : la
   campagne est EN ATTENTE du geste compute au poste réel (MODÈLE-ABSENT nommé — 4 Gio /
   2 vCPU / aucun GPU) ; le harnais complet (schéma, grammaire, expandeur, juge, boucle
   de réparation, journal) est LIVRÉ et rejouable.
6. LES CONTRÔLES NÉGATIFS DU CLIENT (exécutables au bac, sans le modèle) : l'octet muté
   du diff REFUSÉ ; l'offset hors plage REFUSÉ ; la clé hors schéma REFUSÉE ; l'op hors
   enum REFUSÉE AU MASQUE (le point 3). Chaque refus nommé par classe.

## Critères d'acceptation
- Le juge expandeur_add.py recoupé INTACT avant/après (9fc325e2…) ; sceau_I verifier
  14/14 avant et après.
- La sonde de gate rejouée bit-identique (deux passes) ; le verdict du décodeur consigné
  tel quel ; l'état de campagne (EN ATTENTE du geste compute) nommé sans maquillage.
- CIBLES.md : les cibles nouvelles pré-enregistrées par le présent plan, la ligne
  CIB-ADD-STRUC DEMEURE EN ATTENTE (aucun re-tirage) ; le registre des attentes inchangé.
- Aucun chiffre fabriqué : tout verdict publié sort d'une mesure vécue au bac ou porte
  l'étiquette EN ATTENTE.
