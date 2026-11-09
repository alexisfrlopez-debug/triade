# KIT TERRAIN M10-(e) — LE RUN DE LOUPE, LE GRANDEUR NATURE (win)

> Le test grandeur nature (TGN, D171) : coder une application ENTIÈREMENT
> avec TRIADE. La couche I a posé les 18 spécifications ; quatre chantiers
> ont noté-mesuré-prouvé chaque bloc (157 contrôles verts aux trois
> graines) ; la cérémonie d'ère a ouvert le build (le garde à QUATORZE
> arbres verts, la dette soldée — Entrée 201) ; le build est NÉ
> (**loupe.exe 0.1.0-dev.4**, 127 488 o, sha256
> `1f2da2833b47265e9b956ee83a5cc246b68455f06f5b7bb03a69045f03503e03`,
> la carte génération 13, le verrou croisé 26/26 — Entrées 202 → 204 →
> 205 → 206 : le terrain a REFUSÉ dev.1 [0xc000007b : l'image ASLR sans
> table de relocalisation, l'oubli nommé du premier build] PUIS dev.2 DU
> MÊME REFUS [le BASERELOC rendu était NÉCESSAIRE mais PAS SUFFISANT —
> l'Entrée 205 a ramené l'image DANS l'enveloppe prouvée de la lignée
> ET PORTÉ LA CASCADE DIAGNOSTIQUE] ; LE RUN dev.3 A ÉTÉ LE PAS
> DÉCISIF : **LE VRAI CHARGEUR A CARTOGRAPHIÉ L'IMAGE** — la première
> fois au terrain, l'enveloppe PROUVÉE — puis le témoin a nommé
> **[CADRE-NÉ]** : le CADRE .data n'était pas né poignée INVALIDE,
> l'initialiseur du build avait pris la TAILLE CADRE_POIGNEE (8) pour
> un offset et posé le sentinel à +8 au lieu de +528 [la chaîne des
> tailles du plan] ; LA RETOUCHE DE L'ENTRÉE 206 fait de l'initialiseur
> .data LE MIROIR EXACT du CADRE_VIERGE du harnais [zéros partout SAUF
> la poignée INVALIDE à +528, l'offset CALCULÉ — jamais gravé de tête]
> ET le scénario relit désormais LE .data ENTIER contre le miroir). Il
> reste
> LE GESTE QUI NE PEUT ÊTRE FAIT QU'ICI : l'application vit chez son
> utilisateur — LE VRAI Windows 11, les VRAIS fichiers, la VRAIE vitrine.

## 1. Ce que ce kit contient

```
loupe-kit/
├── loupe.exe          l'ARTEFACT 0.1.0-dev.4 (127 488 o, sha256
│                      1f2da283… — lecture seule pour le run ; la carte
│                      privée ne voyage JAMAIS avec l'artefact, R1) ;
├── scenario-loupe.py  LE SCÉNARIO (python SEUL : ctypes, hashlib, os,
│                      platform, struct, sys, tempfile — les constantes
│                      FIGÉES au laboratoire depuis le plan du dépôt,
│                      recoupées à l'assemblage — un kit corrompu est un
│                      refus nommé AVANT tout geste) ;
└── LISEZMOI-KIT-LOUPE.md  le présent document.
```

## 2. Le geste (quatre temps)

1. **Extraire** le zip COMPLET dans un NOUVEAU dossier (ne jamais
   mélanger les runs — D99 ; si le dossier d'un run ancien existe
   déjà — celui de dev.1, de dev.2 ou de dev.3 par exemple — créez-en
   un NEUF, `loupe-kit-4/` par exemple : l'artefact refusé ne
   se réutilise pas). Sur votre Windows 11 : `loupe-kit/`.
2. **Lancer le scénario** : `python scenario-loupe.py` (ou
   `py`/`python3` — **un Python 64 bits est requis**). Aucun paquet à
   installer, aucun droit particulier, aucun réseau. Le run dure
   quelques secondes et dit tout à l'écran ; chaque constat est tranché
   binaire, le verdict se rend POST-MORTEM. NOTE DE L'ENTRÉE 205 : les
   boîtes bloquantes du chargeur (« python.exe — Image incorrecte »)
   sont COUPÉES par le mode d'erreur du scénario — un refus éventuel
   est nommé AU TÉMOIN (GetLastError + NTSTATUS consignés), jamais
   muré derrière un bouton OK ; ET LA CASCADE DIAGNOSTIQUE se joue
   toute seule (voir S0 ci-dessous) : laissez-la finir, le témoin
   part au coffre QUEL QUE SOIT le verdict.
3. **Vivre la vitrine** (le cœur du grandeur nature) :
   **double-cliquez `loupe.exe`** — la fenêtre s'ouvre, la barre
   d'état porte l'usage (`loupe <fichier>`) et l'ascenseur ; fermez-la
   (Alt+F4). Puis ouvrez un VRAI fichier **depuis la ligne de
   commande** : `loupe.exe monfichier.bin` (ou glissez-déposez un
   fichier sur l'icône). L'entête des colonnes, les lignes hexa, le
   miroir ASCII, **le panneau d'empreintes** (md5 + sha256 du fichier
   entier — la barre du bas), la cellule active inversée. Les gestes :
   la molette (3 lignes par cran), l'ascenseur, **F5** l'aller
   (l'adresse hexa à la barre), **F3** la recherche (les paires hexa à
   la barre, F3 encore : l'occurrence suivante), la **saisie hexa**
   (tapez deux chiffres sur une cellule — `4` puis `d` : l'octet est
   écrit au journal, la marque « MODIFIÉ » monte à la barre), **Ctrl+S**
   la sauvegarde (`N o écrits · 0x…..0x…` — chaque octet à son
   décalage), **Alt+F4 LE DOUBLE-GESTE** quand la marque est posée (le
   premier est refusé nommément, le second tranche). Une capture
   d'écran après ouverture d'un fichier de votre choix est la bienvenue
   au réceptacle.
4. **Renvoyer** le dossier `preuves-loupe/` ENTIER au coffre
   `/test/preuves-loupe/` (dossier Drive « Triade » → « test ») : le
   témoin naît tout seul (`temoin-loupe.txt`) ; ajoutez-y les captures
   éventuelles de la vitrine (PNG/JPG, nommées `capture-*.png`).

## 3. Ce que le scénario démontre (les temps du run)

- **T0 LE TÉMOIN** : l'empreinte de l'artefact ASSERTÉE avant tout
  geste ; l'image cartographiée (LoadLibraryEx DONT_RESOLVE — le
  scénario est LE CHARGEUR, aucun point d'entrée exécuté) ; les
  adresses scellées CONSTATÉES UN PAR UN (la minilibc M1
  @0x1100/0x1180/0x13C0, la boucle démo @0x15C0, la famille sha M9
  @0xC000+, LA TABLE K[64] @0x2F00 de FIPS 180-4, le qword version R10
  @0x2E80, le CADRE né poignée INVALIDE) ; **LE BASERELOC MINIMAL
  DÉCLARÉ (dirs[5] — la leçon de l'Entrée 204 : sans table, le VRAI
  chargeur refuse de reloger l'image ASLR, c'est le refus 0xc000007b
  que le terrain a nommé sur dev.1)** ; l'IAT RÉSOLUE par le
  scénario (34 feuilles + la double entrée démo — VirtualProtect le
  temps de la pose : ce que fait le chargeur réel à la liaison).
- **T1 LA SESSION** : loupe-01 à son adresse scellée — le VRAI fichier
  ouvert par l'application (CreateFileW par l'IAT résolue), le cadre
  relu champ à champ (la taille EXACTE, la poignée vivante).
- **T2 LA DOUBLE LECTURE** : loupe-02 la fenêtre au tampon == le
  fichier lu par Python (les DEUX lecteurs indépendants) ; loupe-07 le
  panneau (md5 + sha256 du fichier ENTIER par fenêtres glissantes) ==
  hashlib — **ET LA PIÈCE DE L'ÈRE JUGÉE PAR SA PROPRE APPLICATION :
  loupe-07 sur loupe.exe LUI-MÊME rend son sha256 asserté**.
- **T3 LES LIGNES** : loupe-08 la ligne == le format composé en Python
  pur (les DEUX lecteurs encore) ; la ligne finale incomplète garde le
  FORMAT (l'alignement des colonnes est un invariant).
- **T4 LA RECHERCHE** : loupe-13 (le memcmp SCELLÉ M1 à l'œuvre) ==
  bytes.find sur les octets vrais.
- **T5 L'ÉDITION** : la boucle ENTIÈRE sur une copie — ouvrir, la
  saisie « 4d » (l'attente consommée par l'engagement), Ctrl+S
  (l'écriture À L'OCTET par le VRAI WriteFile) ; le fichier revérifié :
  EXACTEMENT l'octet changé, la taille CONSTANTE, la marque levée.
- **T6 LES REJETS** : l'échec NOMMÉ — le motif absent → -1 FIN ; le
  chemin qui ne désigne rien → -2 ABSENT ; la session double → -5 ;
  le décalage hors bornes → -3 (un refus vaut plus qu'un vert muet).
- **T7 LA CLÔTURE** : loupe-03 le cadre re-vierge, idempotent ;
  l'artefact relu INCHANGÉ (le run ne touche pas la pièce).
- **S0 LA SONDE (l'Entrée 205 — LA CASCADE DIAGNOSTIQUE)** : après le
  run (ou à l'échec de la cartographie), le scénario reconstitue UN À
  UN les axes par lesquels dev.2 sortait de l'enveloppe de la
  lignée — P0 la copie identique (le contrôle), P1 LE TROU DE PAGE
  (.rdata 0x1000), P2 LE BSS MASSIF (.data RS 0x400), P3 LE
  SOUS-SYSTÈME CUI, P4 LA GÉOMÉTRIE dev.2 ENTIÈRE — sur des COPIES
  TEMPORAIRES nées et mortes dans %TEMP% (loupe.exe n'est JAMAIS
  écrit) : **le VRAI chargeur Windows NOMME l'axe fautif** — le
  témoin consigne chaque verdict VERTE/REFUS + GetLastError +
  NTSTATUS ; la leçon de l'Entrée 205 rentre au dépôt avec le run.

## 4. Les frontières nommées (l'honnêteté du terrain)

- Le scénario NE LANCE PAS la vitrine (aucun point d'entrée exécuté) :
  les blocs sont appelés à leurs adresses scellées, la main du kit sur
  la pédale — la vitrine se vit AUSSI, à côté, au double-clic ;
- le scénario n'écrit JAMAIS loupe.exe (lecture seule, relu à la
  clôture) ; LA SONDE de l'Entrée 205 écrit ses copies de diagnostic
  dans %TEMP% uniquement, et les EFFACE (loupe.exe n'est jamais
  touché) ; la carte privée ne voyage pas (R1) ;
- les blocs d'empreintes appellent la famille sha du SCELLÉ M9 aux
  adresses d'origine (R7 : jamais une copie ré-écrite) — le panneau
  sha256 de l'application EST le sha256 prouvé au jalon M9 ;
- si un dossier `preuves-loupe/` existe déjà d'un run ancien, NE LE
  MÉLANGEZ PAS (D99) : un dossier neuf par run.

## 5. Après le run

Le labo recoupe sur pièces (D138/D145/D148) : le témoin relu, les
constats croisés contre le dépôt, les empreintes recalculées. **ET SI
LE VERT TIENT : LA BALISE `loupe 0.1.0` SCELLÉE sur run terrain
recoupé — LE JALON M10, la méthode TRIADE entière prouvée par la
CRÉATION : de l'intention (la couche I) à l'octet vécu chez son
utilisateur.**
