# KIT TERRAIN M7-(d) — L'UNIVERSALITÉ REJOUÉE (riscv64) : la parité des TROIS profils + le patch fence.i sur la machine du développeur

> Préparé au laboratoire le 05/11/2026 (chantier M7-(d), le dernier du jalon).
> **Deux artefacts et un instrument** : `corpus` est LE SCELLÉ **0.8.0-rc.1**
> du jalon M7 — la troisième instanciation de la même couche I
> (`riscv64-linux-elf64`, 12 288 o, sha256
> `ec343b4e8bebf21c8b29a6da1a5eb022fb7b8e4b50ce95c5906734ef0b043799`) ;
> `demo` est le DÉMONSTRATEUR INVITÉ du chantier M7-(c) (f72001, l'image du
> corpus + le démonstrateur patch, 12 288 o, sha256
> `e57fc74be2ea67ab4c05351d0b5e0b93b6147ec34f2fb7aabbfd1ab7f141cde9`) —
> l'INSTRUMENT du jalon, pas un artefact de la lignée (pas de carte).
> `qemu-riscv64` est l'INSTRUMENT D'EXÉCUTION, un binaire STATIQUE embarqué
> (aucun paquet à installer, aucun droit root, aucun réseau).
>
> **La réserve instrumentale D149 est NOMMÉE dans chaque verdict** : sous
> qemu-riscv64, l'ISA est exécutée par TCG — le noyau et les syscalls sont
> RÉELS de l'hôte, mais l'exécution demeure une ÉMULATION DE PROCESSUS,
> jamais déguisée en exécution native (aucune fer RISC-V n'existe ici).
>
> La démonstration de laboratoire est VERTE sur pièces (M7-(b)/(c) : Entrées
> 152/153) : le rituel de parité 6/6, la parité § 8.3 PAR EXÉCUTION sur les
> TROIS profils, la bascule fence.i pendant le trafic (1 200 usages,
> transcription byte-exact 15 425 o), le rollback, les refus nommés 1-4, le
> DEP falsifié (SIGSEGV, 4 290 o exacts), zéro régression. **Le présent kit
> demande à la machine du développeur de REJOUER le geste** — le run terrain
> VERT sur pièces pose la finale `0.8.0` : le jalon M7 franchi, chaque profil
> déclaré supporté a franchi ses critères — l'universalité DÉMONTRÉE.

## 1. Ce que ce kit contient

```
m7-kit/
├── corpus            le SCELLÉ 0.8.0-rc.1 du jalon M7 — les DOUZE blocs du
│                     patrimoine + corpus-13 (les MÊMES fichiers canoniques
│                     unix/I/ que l'instance Linux — la parité § 8.3) ;
│                     ET_DYN/PIE EM_RISCV, 3 segments R/RX/RW, PT_GNU_STACK
│                     sans X ; le moteur de patch tcp-07 EMBARQUÉ @0x1A40 ;
│                     sha256 ec343b4e… (lecture seule pour le run)
├── demo              le DÉMONSTRATEUR INVITÉ f72001 — l'image du corpus +
│                     le démonstrateur patch à 0x2000 dans la réserve RX ;
│                     sha256 e57fc74b… (lecture seule pour le run)
├── qemu-riscv64      l'INSTRUMENT — binaire STATIQUE (qemu-user 10.0.13,
│                     Debian) : md5 consigné au témoin du run ; le scénario
│                     accepte aussi $QEMU_RISCV64 ou le PATH de la machine
│                     (la version et le md5 sont alors consignés de même)
├── scenario-m7d.py   LE SCÉNARIO (python3 SEUL — aucun paquet à installer) :
│                     constantes FIGÉES au laboratoire depuis le plan du
│                     dépôt, sha256 assertés au démarrage (un kit corrompu
│                     est un refus nommé AVANT tout geste)
└── LISEZMOI-KIT-M7D.md  le présent document
```

## 2. Le geste (trois temps)

1. **Extraire** le zip COMPLET dans un NOUVEAU dossier (ne jamais mélanger
   les runs — D99). Sur WSL2 par exemple `~/run-m7d/`. Si le bit exécutable
   de l'instrument s'est perdu au transfert (certaines extractions zip ne
   restaurent pas les permissions), le scénario le rétablit — le geste est
   nommé au journal ; les DEUX artefacts, eux, ne sont jamais modifiés
   (ils s'exécutent PAR qemu, jamais par le noyau).
2. **Lancer** : `python3 scenario-m7d.py` — depuis le dossier extrait (le
   `corpus`, le `demo` et le `qemu-riscv64` doivent être à côté). Aucun
   réseau, aucun droit root, aucune écriture hors de `./preuves-m7/`. Le
   run dure environ une minute (une vingtaine d'exécutions qemu) et dit
   tout à l'écran ; chaque constat est tranché binaire (PASS/ÉCHEC nommé),
   le verdict se rend POST-MORTEM.
3. **Renvoyer** le dossier `preuves-m7/` ENTIER au coffre
   `/test/preuves-m7/` (dossier Drive « Triade » → « test ») : les trois
   pièces naissent toutes seules —
   - `temoin-m7d.txt` — l'environnement de la machine (uname, python, le
     noyau hôte, la version ET le md5 de l'instrument qemu, les empreintes
     des artefacts relues AVANT le run) ;
   - `scenario-m7d-journal.log` — le run entier, constat par constat ;
   - `VERDICT-run-m7d.txt` — le verdict post-mortem (chaque constat, les
     frontières nommées, la réserve D149).

## 3. Ce que le scénario démontre (les temps du run)

- **T0 LE TÉMOIN** : les empreintes des DEUX artefacts ASSERTÉES avant tout
  geste (un kit corrompu est un refus nommé, jamais un run muet) ; la
  version et le md5 de l'instrument consignés (la réserve D149 NOMMÉE).
- **T1 LE RITUEL DE PARITÉ** : le scellé exécuté TROIS FOIS sous qemu —
  exactement les DEUX lignes au code 0 (« TRIADE M1 : minilibc 21/21 OK »
  puis « corpus : autotest 21 vecteurs ») — LE MÊME verdict que les
  instances Windows et Linux : la parité § 8.3 sur la machine du
  développeur ; puis TROIS bases forcées du CHARGEUR (-R 1G / -R 4G /
  -B 0x100000000 -R 2G) : la sortie IDENTIQUE (l'indifférence à la base se
  démontre par les bases forcées, jamais par un ASLR émulé — D155).
- **T2 LE PATCH fence.i PENDANT LE TRAFIC** (le critère M5-(c)/M6-(d) sur
  la TROISIÈME ISA) : le démonstrateur invité —
  - **(a) le trafic en session** : 1 200 usages de l'ENTRÉE du journal ;
    le moteur APPLIQUÉ entre les usages 399 et 400, le RETOUR ARRIÈRE
    entre 799 et 800 — la boucle CONTINUE, le journal COHÉRENT : le flux
    OCTET POUR OCTET l'attendu (800 lignes v1, 400 lignes v2 marquées
    « j2: », aucune déchirée, aucune perdue, aucun mélange) ; la séquence
    scratch+fence.i : mprotect RW → copie → fence rw,rw → LA BASCULE UN
    mot → fence.i → RX (le bit X RETENU pendant l'écriture — D39) ;
  - **(b) les refus nommés 1/2/3/4 EXERCÉS** — le mode invalide, l'état
    divergent, l'absent et la somme par mutation IN-GUEST de la table
    d'intégrité R10 (restaurée après chacun) : INCLUS dans la
    transcription attendue (le démonstrateur les exerce LUI-MÊME) ;
  - **(c) LE DEP FALSIFIÉ** (0x7→0x3) : le mutant du démonstrateur, un run
    séparé — l'exécution FAUTE au retour du premier mprotect (page sans
    X, le fetch suivant) : SIGSEGV, les 400 lignes v1 EXACTES (4 290 o,
    zéro silence) ;
  - **(d) LA FALSIFICATION DU DÉMONSTRATEUR** (l'instrument est
    soupçonnable — D154) : un octet d'opcode corrompu par instruction,
    jusqu'à la déviation ; si TOUTES passaient silencieusement, l'oracle
    serait VACUE et refuserait ;
  - **(e) L'INDIFFÉRENCE À LA BASE** : les TROIS bases forcées du chargeur
    — la transcription identique à toute base.
- **T3 ZÉRO RÉGRESSION** : les DEUX fichiers relus — pas un octet bougé
  (le patch est un fait de la session INVITÉE, jamais du fichier) ; le
  rituel du scellé REJOUÉ : exactement ses deux lignes au code 0.

## 4. Les frontières nommées (l'honnêteté du terrain)

- **Le code 5 (le service refuse) est STRUCTUREL sous qemu-user** : l'hôte
  accorde RWX sur les mappings privés — le refus EACCES du noyau réel
  (démontré au terrain M6-(d) côté Linux natif) n'est PAS productible ici ;
  la branche fail-closed VIT dans tcp-07 (bltz → refus 5). La politique de
  mapping de l'HÔTE est consignée au témoin par le noyau qui parle (uname).
- **La concurrence réelle est HORS périmètre** (fiche profil § 5) : le
  corpus M7 est MONO-FIL — la bascule pendant le trafic se démontre EN
  SESSION, entre deux usages ; le verrou tournant amoswap.d vit dans le
  bloc, sa preuve sous concurrence appartient au profil Linux (M6-(d),
  démontrée terrain).
- **Le demo n'est PAS un artefact de la lignée** : pas de carte, l'image
  du corpus + le démonstrateur — l'INSTRUMENT du chantier (modèle
  unix/demo_patch.py) ; LE scellé du jalon est `corpus`.
- **qemu-riscv64 est une ÉMULATION DE PROCESSUS** (TCG) : le noyau et les
  syscalls sont réels de l'hôte, l'ISA est traduite — jamais une fer
  RISC-V (la réserve instrumentale D149, nommée dans chaque verdict).

## 5. Après le run

- Si le verdict est **VERT** : renvoyer `preuves-m7/` au coffre
  `/test/preuves-m7/` — le laboratoire recoupe les pièces (D138/D145/D148 :
  verdict sur pièces, post-mortem — témoin ↔ journal ↔ verdict recoupés
  ENTRE EUX) et, si elles établissent le critère, `--sceller-final` pose la
  **finale 0.8.0** : le jalon M7 franchi — l'universalité DÉMONTRÉE, chaque
  profil déclaré supporté a franchi ses critères.
- Si un constat dit **ÉCHEC NOMMÉ** : renvoyer `preuves-m7/` TEL QUEL — la
  ligne nomme le défaut ; un échec honnête vaut plus qu'un vert muet
  (l'ordre lexicographique de la maison : la vérité d'abord).

*Le laboratoire a déjà rejoué CE kit exact (extraction vierge + run) :
VERT — le kit déposé au coffre est le kit prouvé au labo (D153).*
