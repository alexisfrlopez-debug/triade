# PLAN GELÉ — W29MOTEUR (moteur natif généralisé aux 52 blocs, l'ouverture de session, la racine de Merkle)

> Vague 29, prompt 2 (dépôt du 27/11/2026, instructions.txt §10 Prompt 2 — suggestions
> B5/B7 de l'évaluation). Généraliser le moteur natif de atelier-w28harnais (le lot
> unique, le compte en registres bruts, rax ET digeste lus par vecteur, la console
> différée en une passe) aux 52 blocs du manifeste et au corpus complet des 235
> vecteurs, PUIS au chemin critique d'ouverture de session (md5+sha256 du fichier
> témoin 196 Kio). Le présent plan gèle l'atelier AVANT toute donnée.

## Geste
1. LE CORPUS GÉNÉRALISÉ : les 50 blocs résolus du manifeste-52 (atelier-w19-oracle,
   les deux non-résolus c30012/c30014 exclus et nommés), le corpus des vecteurs
   atelier-w20-orac (320 produits — les 235 exécutables à la carte dérivée la référence
   W28HARNAIS), l'assemblage de chaque bloc DEPUIS SA NOTATION (R5, sha256 recoupé au
   manifeste — un écart refuse la session). La session : CHAQUE bloc dans son lot unique
   au moteur généralisé (mmap + appel), la console LIGNE-IDENTIQUE au moteur committé
   pour chaque bloc (l'équivalence prouvée ligne par ligne) ; un timeout n'est jamais
   un OK (le gate du RIP reconduit).
2. LA NOUVELLE LIGNE CIBLE — CIB-VOL-SESSION (pré-enregistrée AU PRÉSENT PLAN, jamais
   un re-tirage de CIB-VOL-REGIME qui demeure à 4,56×) : l'OUVERTURE DE SESSION — le
   md5+sha256 du FICHIER TÉMOIN temoin-3f.bin (196 609 octets, la génération FIXE
   graine 20261107 de loupe/harnais_noyau.py, le témoin du p8-m4 « 10,3 s ») par le
   moteur natif — cible **≤ 1 s** (la référence : ~10 s à l'émulateur jumeau, mesurée
   au présent bac dans la même session). Le chemin : les blocs scellés loupe-05-sha256
   et loupe-06-md5 (et leurs dépendances PAR LA CARTE : tls13-01/03/04, libc-01/07)
   assemblés depuis leurs notations, montés au moteur natif avec les feuilles kernel32
   du noyau (SetFilePointerEx/ReadFile/GetLastError) PORTÉES en amorces natives lisant
   le témoin — le code des blocs INCHANGÉ (les octets assemblés == l'empreinte du
   manifeste loupe, la carte est le montage, jamais la pièce ré-écrite). Les condensés
   recoupés À hashlib.md5/hashlib.sha256 (le juge croisé). Le temps : horloge monotone,
   n≥5 passes, la médiane publiée.
3. LA RACINE DE MERKLE : le digeste de trace complet par vecteur (rax ‖ digeste ‖ le
   corps ‖ le vecteur) engagé dans UN ARBRE DE MERKLE au scellage de la session — la
   racine CONSIGNÉE au registre de la session ; l'audit 1-sur-10 conservé et étendu
   (chaque vecteur audité confronté au jumeau champ par champ) DEVIENT vérifiable
   sélectivement à coût constant (la recomposition depuis les traces recoupée à la
   racine). SHA256 les feuilles ; la racine divergente → REFUS NOMMÉ.
4. LE RÉGIME PAR BLOC : le régime chaud ≤ 5× C par bloc contre le pilote nu (le même
   code de bloc appelé directement, gcc -O2, horloges internes symétriques, n≥9
   médianes) — la cible PRÉ-ENREGISTRÉE par le présent plan pour CHAQUE bloc du corpus,
   publiée par bloc (tenue/manquée, aucune agrégation maquillée). AUCUN contrôle retiré
   (le compte rax + digeste par vecteur conservé ; le mémo content-addressed reconduit).
5. LES CONTRÔLES NÉGATIFS : le shim muté attrapé au premier vecteur ; l'octet de carte
   muté → MISS du mémo content-addressed ; le voisinage amputé → FAULT nommé ; la racine
   de Merkle divergente → refus nommé.
6. LA GRAINE : 20261128 reconduite pour le tirage des vecteurs (celle de W28HARNAIS),
   consignée AVANT le tirage ; l'ordre des blocs/vecteurs JAMAIS re-tiré (l'ordre
   canonique du corpus w20-orac).

## Critères d'acceptation
- Rejeu bit-identique de la session complète (console jsonl byte-byte, deux passes).
- Audit 1-sur-10 à zéro écart au jumeau ; racine de Merkle recomposée depuis les traces
  et recoupée ; la racine mutée refusée nommément.
- Sceau_I 14/14 avant et après ; aucune empreinte de pièce scellée modifiée ; porte de
  génération 32 classes zéro rouge (la chaîne existante).
- Verdicts publiés TELS QUELS au registre CIBLES.md (la ligne nouvelle CIB-VOL-SESSION,
  JAMAIS de re-tirage de CIB-VOL-REGIME) ; le linter C32 vérifie chaque ratio publié
  (les opérandes non arrondis aux registres).
