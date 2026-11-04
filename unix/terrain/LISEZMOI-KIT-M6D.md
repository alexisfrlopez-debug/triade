# KIT TERRAIN M6-(d) — LE PATCH EN PRODUCTION (Linux) : la bascule du journal pendant le trafic

> Préparé au laboratoire le 05/11/2026 (chantier M6-(d) — le critère M5-(c)
> refermé sur le profil Linux, D149-(4)). L'artefact est LE scellé
> **0.7.0-rc.1** du jalon M6 (carte génération 1, le fait de carte du
> chantier M6-(c)) : `corpus`, 12 288 octets,
> sha256 `dd14195c9da5e9b990e8f9b141eedd6574bb8ecc793ffdd5b67edb71b81ddff7`.
> La démonstration de laboratoire est VERTE sur pièces
> (`unix/demo_patch.py` — la même exécutée PAR la suite de conformité) :
> la boucle d'écriture basculée ENTRE DEUX usages (1 200 lignes, le moteur
> appliqué entre les usages 400 et 401, le retour arrière entre 800 et
> 801), le journal cohérent OCTET POUR OCTET, la bascule sous concurrence
> réelle (le qword d'atomicité posé pendant qu'un fil ouvrier journalise —
> 5 300+ lignes entières, les deux formats constatés dans SON trafic), le
> rollback, la zéro régression. **Le présent kit demande à la machine
> Linux du développeur de rejouer le geste** : l'exécution réelle sur UN
> AUTRE noyau que celui du laboratoire (WSL2 recommandé — D149 : noyau
> Linux complet sur la machine Windows 11, aucun outil nouveau) — le run
> terrain VERT sur pièces pose la finale `0.7.0` (le jalon M6 franchi).

## 1. Ce que ce kit contient

```
m6-kit/
├── corpus                l'artefact scellé 0.7.0-rc.1 du jalon M6 —
│                         l'instance SysV du corpus paritaire : les DOUZE
│                         blocs du patrimoine M0-M5 + le principal
│                         corpus-13 ; ET_DYN/PIE, 3 segments R/RX/RW,
│                         PT_GNU_STACK sans X (le durcissement M6-(a)) ;
│                         le moteur de patch tcp-07 EMBARQUÉ @0x1A40, son
│                         remplaçant au staging (le journal v2, marque
│                         « j2: ») et la porte d'intégrité R10 @0x540 ;
│                         sha256 dd14195c9da5e9b990e8f9b141eedd6574bb8ecc793ffdd5b67edb71b81ddff7
│                         md5    ad385c370cf64e8e50e1b46eff05783d
│                         12 288 octets — le fichier est en LECTURE
│                         SEULE pour le run : le patch vit dans des
│                         cartographies mémoire PRIVÉES du processus, le
│                         fichier ne bouge JAMAIS d'un octet (le scénario
│                         le re-prouve après le run)
├── scenario-m6d.py       LE SCÉNARIO (python3 + ctypes SEULEMENT — aucun
│                         paquet à installer) : la cartouche d'appel est
│                         PRÉ-ASSEMBLÉE au laboratoire (octets embarqués,
│                         sha256 asserté au démarrage — un kit corrompu
│                         est un refus nommé AVANT tout geste)
└── LISEZMOI-KIT-M6D.md   le présent document
```

## 2. Le geste (trois temps)

1. **Extraire** le zip COMPLET dans un NOUVEAU dossier (ne jamais
   mélanger les runs — D99). Sur WSL2 : dans le dossier de votre choix,
   par exemple `~/run-m6d/`. Si le bit exécutable du `corpus` s'est perdu
   au transfert, le scénario le rétablit (le geste est nommé au journal).
2. **Lancer** : `python3 scenario-m6d.py` — depuis le dossier extrait
   (le `corpus` doit être à côté). Aucun réseau, aucun droit root,
   aucune écriture hors de `./preuves-m6/`. Le run dure quelques
   secondes et dit tout à l'écran ; chaque constat est tranché binaire
   (PASS/ÉCHEC nommé), le verdict se rend POST-MORTEM.
3. **Renvoyer** le dossier `preuves-m6/` ENTIER au coffre
   `/test/preuves-m6/` (dossier Drive « Triade » → « test ») : les trois
   pièces naissent toutes seules —
   - `temoin-m6d.txt` — l'environnement de la machine (uname, WSL,
     python, l'état ASLR du noyau, l'empreinte du corpus relu AVANT le
     run) ;
   - `scenario-m6d-journal.log` — le run entier, ligne à ligne ;
   - `VERDICT-run-m6d.txt` — le verdict post-mortem avec chaque constat.

## 3. Ce que le scénario démontre (les temps du run)

- **T0 LE TÉMOIN** : l'empreinte du corpus ASSERTÉE avant tout geste
  (sha256 dd14195c… — un kit corrompu est un refus nommé, jamais un run
  muet) ; l'environnement consigné.
- **T1 LE RITUEL** : `./corpus` exécuté TROIS FOIS par le noyau de la
  machine — l'ASLR choisit la base à chaque run (le développeur ne
  choisit pas, le laboratoire non plus : D146, la leçon du scellé
  0.6.0-rc.1 mort en terrain) — exactement les deux lignes nominales au
  code 0 à CHAQUE exécution ; si `setarch` est présent : un passage à
  base figée (ADDR_NO_RANDOMIZE), même sortie (le recoupement du
  mécanisme noyau).
- **T2 LE PATCH PENDANT LE TRAFIC** (LE critère M5-(c)) :
  - **(a) le trafic en session** : 1 200 usages de la boucle
    d'écriture ; le moteur APPLIQUÉ entre les usages 400 et 401, le
    RETOUR ARRIÈRE entre 800 et 801 — la boucle CONTINUE (jamais une
    interruption), le journal COHÉRENT : le flux OCTET POUR OCTET
    l'attendu (800 lignes v1, 400 lignes v2 marquées « j2: », aucune
    déchirée, aucune perdue, aucun mélange de formats) ;
  - **(b) la bascule sous CONCURRENCE RÉELLE** : un fil ouvrier
    journalise en boucle PENDANT que le fil conducteur applique le
    patch, journalise sous v2, revient, journalise sous v1, applique
    encore — la PREUVE DE VIE de l'ouvrier AVANT la bascule (des lignes
    déjà émises), puis chaque ligne de l'ouvrier ENTIÈRE au format v1
    OU v2 (jamais un mélange dans une même ligne — l'écriture alignée
    unique du qword, l'atomicité x86-64), aucun index perdu ni
    dupliqué, et les DEUX formats constatés dans le trafic de l'ouvrier
    (la bascule était VIVANTE pendant qu'il journalisait) ;
  - **(c) le retour à l'état image** : l'entrée du journal restaurée
    OCTET POUR OCTET, l'état v1, le verrou rendu, le remplaçant DORMANT
    dans la croissance (réactivable) ;
  - **(d) LE NOYAU DE LA MACHINE PARLE** : la cartographie PARTAGÉE en
    lecture seule (le descripteur du fichier ouvert en lecture seule) —
    `mprotect` EXIGE un descripteur inscriptible : le refus EACCES est
    le NOYAU du développeur qui refuse (le code 5 du contrat tcp-07,
    AVANT toute écriture) — aucune émulation, aucun shim : le run
    terrain parle au noyau réel.
- **T3 ZÉRO RÉGRESSION** : le FICHIER artefact n'a pas bougé d'un octet
  (sha256 re-relu après la démonstration) ; le rituel REJOUÉ rend
  exactement ses deux lignes au code 0.

## 4. Après le run

- Si le verdict est **VERT** : renvoyer `preuves-m6/` au coffre
  `/test/preuves-m6/` — le laboratoire recoupe les pièces (D138/D145/
  D148 : verdict sur pièces, post-mortem) et, si elles établissent le
  critère, `--sceller-final` pose la **finale 0.7.0** (le jalon M6
  franchi).
- Si un constat dit **ÉCHEC NOMMÉ** : renvoyer `preuves-m6/` TEL QUEL
  — la ligne nomme le défaut ; un échec honnête vaut plus qu'un vert
  muet (l'ordre lexicographique de la maison : la vérité d'abord).

*Le laboratoire a déjà rejoué CE kit exact (extraction vierge + run) :
VERT — le kit déposé au coffre est le kit prouvé au labo.*
