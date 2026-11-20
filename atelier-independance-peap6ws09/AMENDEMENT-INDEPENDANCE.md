# AMENDEMENT PRÉ-ENREGISTRÉ — LE PROTOCOLE D'INDÉPENDANCE INTER-FAMILLES (peap6ws09)

> L'instruction (Qwen_text_20261120_peap6ws09.txt, lue INTÉGRALEMENT, md5
> recoupé) : « Recadre le protocole d'indépendance inter-familles et
> affine l'analyse des survivants de mutation, au laboratoire uniquement,
> sans toucher aux artefacts scellés ni aux arbres signés, sans fabriquer
> aucun résultat. »

CET AMENDEMENT EST GELÉ AVANT TOUT RUN — son empreinte sera consignée à
la décision (D225) avant la première exécution.

## 1 · L'AMENDEMENT AU PROTOCOLE D'INDÉPENDANCE (gelé)

**L'ÉTAT PRÉCÉDENT (1c4sokpii, consigné)** : l'indépendance
inter-familles était sondée par LA RÉCITATION PURE — le second modèle
(famille distincte) récite les tables T[64] (MD5, RFC 1321) et K[64]
(SHA-256, FIPS 180-4) par morceaux de 16, sans indice des valeurs. LE
RÉSULTAT VÉCU : Qwen2.5-Coder-1.5B-Instruct récite 0/64 + 0/64 (répète
les ancêtres puis dérive), les rondes de correction copient (64/64 —
la copie, jamais l'indépendance). LE GAP NOMMÉ : la capacité du local
disponible (3 Go de RAM barrent le 7B).

**L'AMENDEMENT (ce qui change, gelé avant tout run)** : la récitation
pure est une SONDE DE MÉMORISATION, jamais un test d'indépendance — le
test d'indépendance devient LA DÉRIVATION OUTILLÉE :

- LE SECOND MODÈLE (famille distincte de l'agent de développement —
  GLM ici) ÉCRIT DU CODE qui dérive T[64] et K[64] depuis LES
  DÉFINITIONS MATHÉMATIQUES SEULES (RFC 1321 § 3.4 : T[i] =
  floor(2³² · |sin(i+1)|) ; FIPS 180-4 § 4.2.2 : K[i] = les 32
  premiers bits de la partie fractionnaire de la racine cubique du
  i-ème nombre premier) — LE PLAN (les tables du dépôt) N'EST JAMAIS
  AU PROMPT ;
- LE CODE ÉCRIT EST EXÉCUTÉ (l'exécution outillée : le script lance le
  code généré, aucun jugement sur la prose) ;
- LE JUGE DEMEURE LA CONFRONTATION MATHÉMATIQUE : les valeurs dérivées
  contre LES DÉFINITIONS (le harnais deriv_MD5_T / deriv_K_sha256 aux
  décimales exactes, Décamal) et contre LE PLAN (les tables du dépôt,
  la source unique) — zéro divergence attendue des deux côtés ;
- LA RÉCITATION PURE DEMEURE, rapportée comme sonde de mémorisation
  (le protocole documenté, jamais re-qualifiée rétroactivement).

**LES RÈGLES DE VERDICT (pré-enregistrées)** : (a) le code généré qui
ne s'exécute pas ou qui diverge des définitions = LE GAP NOMMÉ SUR
PIÈCES (le code généré est conservé verbatim, l'écart exact consigné —
jamais simulé, jamais corrigé silencieusement) ; (b) si le local
disponible tient un modèle plus grand (le 7B quantifié en RAM), le
tenter et consigner la configuration ; sinon NOMMER le plafond de
capacité (la RAM du bac) ; (c) la confrontation math↔plan est re-tenue
AVANT toute génération (zéro divergence exigée — elle fut verte à
1c4sokpii, elle est re-vérifiée).

## 2 · LE BRAS C ÉTENDU (gelé)

**L'ÉTAT PRÉCÉDENT** : le bras C (le contrat de couche I MOT POUR MOT
au prompt → le second modèle écrit le source C → gcc -O2 → l'épreuve
POSIX) fut vécu sur UN contrat (loupe-13 : 1984/2011, le bord Q2 nommé
— la plage restante trop courte rend −5 au lieu du −1 du contrat).

**L'EXTENSION (gelée)** : AU MOINS TROIS contrats de couche I, dont
loupe-13 (le reconduit) : + loupe-02 LIRE et loupe-16 SAISIE (les
contrats instrumentés de la campagne D210 — les classes différentes :
la fenêtre bornée au tampon, la saisie bornée aux touches). LE
PROFIL DE CAPACITÉ par contrat : les verts/rouges de l'épreuve (le
positif, les rejets, la différentielle 2 000 cas graine 20261115, le
juge bytes.find pour la recherche), les classes de bord nommées, chaque
gap nommé sur pièces. AUCUN résultat fabriqué : le source généré est
conservé verbatim, l'épreuve exécutée, l'écart exact consigné.

## 3 · LA CLASSIFICATION DES 21 SURVIVANTS (gelée)

**L'ÉTAT PRÉCÉDENT (1c4sokpii)** : les 56 survivants triés au niveau
instruction, 35 tués par la batterie d'injection K4, LE RESTE DE 21
nommé à treize familles de causes.

**LA CLASSIFICATION (gelée)** : les 21 restants classés en TROIS
catégories :
1. **ÉQUIVALENTS PROUVÉS** — preuve mécanique : le mutant produit le
   MÊME OBSERVABLE sur TOUT état servable (l'espace d'entrée du
   contrat) — la preuve par analyse du mutant contre le scénario
   (l'instruction morte par construction : le registre volatil jamais
   relu, le sentinel adjacent hors de l'espace servable, la convergence
   des gardes, la cible détournée retombant sur le même état) ;
2. **TUABLES RESTANTS** — le scénario qui les tuerait est nommé mais
   hors du harnais actuel ;
3. **LIMITES DU HARNAIS** — ce que l'émulation ne peut pas observer.

LE SCORE AJUSTÉ rapporté à côté du 811/832 brut : (811 + équivalents
prouvés) / (832 − équivalents prouvés) — les équivalents exclus du
dénominateur, LA FORMULE GELÉE ICI avant calcul. AUCUN tueur
affaibli : la batterie K4 re-visitée aux mêmes graines, la console
v0.14.0 (776/832) reproduite d'abord.

## 4 · LES PIÈCES ATTENDUES

- RAPPORT-AMENDEMENT-EXECUTION.txt (la dérivation outillée vécue, le
  modèle, la configuration, les résultats, les gaps nommés) ;
- les sources générés conservés verbatim (derivation_*.py, bras_c_*.c) ;
- la classification 21-survivants.csv (les trois catégories, la
  preuve mécanique par équivalent, le score ajusté à côté du brut) ;
- l'empreinte des artefacts scellés avant/après : INTACTES.

L'EMPREINTE DE CET AMENDEMENT : consignée au commit (gelé avant tout
run).
