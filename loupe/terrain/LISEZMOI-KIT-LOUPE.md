# KIT TERRAIN M10-(e) — LE RUN DE LOUPE, LE GRANDEUR NATURE (win)

> Le test grandeur nature (TGN, D171) : coder une application ENTIÈREMENT
> avec TRIADE. La couche I a posé les 18 spécifications ; quatre chantiers
> ont noté-mesuré-prouvé chaque bloc (157 contrôles verts aux trois
> graines) ; la cérémonie d'ère a ouvert le build (le garde à QUATORZE
> arbres verts, la dette soldée — Entrée 201) ; le build est NÉ et a vécu
> SEPT RUNS terrain (**loupe.exe 0.1.0-dev.7**, 127 488 o, sha256
> `388d468067cbf054…4d9bbc`, la carte génération 15 —
> Entrées 202 → … → 209 → **210** : le run du kit dev.7 a tenu **T0 → T5
> TOUT VERT** — la sauvegarde de l'Entrée 209 PROUVÉE au terrain, la
> boucle d'édition ENTIÈRE vivante — puis le témoin a nommé DEUX DÉFAUTS
> D'UN MÊME GESTE : **[EAX-SANS-SIGNE] AU KIT** — T6 lisait « 0xfffffffe
> != -2 ABSENT » : la pièce rendait ses codes d'échec par `mov eax,
> imm32` — EAX seul, les 32 bits hauts de RAX à zéro — et le contrat
> publié du scénario [c_int64] lit le qword ENTIER : la pièce disait -2,
> le kit entendait 4294967294 ; ET **[D54-QUATRIÈME] À LA PIÈCE** — la
> vitrine demeurait MORTE : 0xC0000005 sur LES DEUX fenêtres, AUCUN
> rapport WER, alors que l'autopsie avait tout vérifié — l'entrée [le fil
> GetModuleHandleW CÂBLÉ, r12 le vrai module aux deux appels], le WndProc
> @0x5DCB, la boucle démo, les 63 appels indirects TOUS couverts, la
> table d'imports PARFAITE, les chaînes larges, l'alignement, les gardes
> de session, le CADRE_VIERGE — **LE DIFFÉRENTIEL A NOMMÉ** : la lignée
> prouvée [demo.exe 0.3.0, le scellé M2 dont la fenêtre VÉCUT au terrain]
> termine CHAQUE plage FirstThunk par un slot NULL ; le build posait les
> QUATRE plages CONTIGUËS — et le chargeur du terrain (Windows 11 build
> 26300, le CHEMIN FirstThunk de la leçon D97) MARCHE chaque plage
> jusqu'au premier NULL : la marche de kernel32 déborde chez les noms
> user32, RegisterClassExW résout à NULL, **et l'entrée APPELLE LE NUL**
> — 0xC0000005 sans dialogue, avant même la première fenêtre ;
> QUATRIÈME manifestation de la dérive de dépôt [D54, D68, D98, et
> celle-ci]. LA RETOUCHE DE L'ENTRÉE 210 EST DOUBLE : la pièce **dev.7**
> [l'IAT ENTIÈRE relogée à 0x3100 — région née zéro — QUATRE plages
> SÉPARÉES PAR NULL et PRÉREMLIES des RVA de noms, le motif D54 au
> complet ; les descripteurs dirigés, dir[12] mis à jour, les 63 sites
> d'appel repointés, les vieilles plages VIDÉES ; les 20 rendus négatifs
> étendus au 64 bits par « push imm8 ; pop rax » et les deux passages de
> loupe-01 passés movsxd ; la taille DEMEURE 127 488 o, AUCUNE adresse
> scellée ne bouge — R7 tenue : le WndProc, la famille sha M9, la
> minilibc, la table K[64], le CADRE, octets inchangés ; le qword version
> 0x00010007] ET le kit **dev.8** [la leçon institutionnalisée : le
> scénario VÉRIFIE LUI-MÊME l'habillage d'import — chaque plage marchée
> au compte exact, les séparateurs NULL, les slots préremplis — la
> quatrième manifestation ne passera PLUS jamais un run ; l'affichage T0
> de la version rendu DYNAMIQUE — le littéral périmé nommé]. Il reste LE
> GESTE QUI NE PEUT ÊTRE FAIT QU'ICI : la vitrine VIVANTE — les DEUX
> codes de sortie à 0, l'application sous les yeux de son utilisateur —
> ET LA VITRINE SE VIT PAR SON TÉMOIN (temoin-vitrine.bat : une mort
> sans témoin ne recoupe pas, l'Entrée 208).

## 1. Ce que ce kit contient

```
loupe-kit-8/
├── loupe.exe          l'ARTEFACT 0.1.0-dev.7 (127 488 o, sha256
│                      388d4680… — LA RETOUCHE DE L'ENTRÉE 210 :
│                      [D54-QUATRIÈME] chassé — l'IAT relogée à 0x3100,
│                      QUATRE plages SÉPARÉES PAR NULL, préremplies du
│                      motif D54 [le chargeur du terrain marche le
│                      chemin FirstThunk : des plages contiguës
│                      tuaient la vitrine avant l'entrée, 0xC0000005
│                      sans dialogue] ; ET [EAX-SANS-SIGNE] étendu —
│                      chaque rendu négatif au 64 bits, le contrat
│                      c_int64 lu exact ; lecture seule pour le run ;
│                      la carte privée ne voyage JAMAIS avec l'artefact,
│                      R1) ;
├── scenario-loupe.py  LE SCÉNARIO dev.8 (python SEUL : ctypes, hashlib,
│                      os, platform, struct, sys, tempfile — les
│                      constantes FIGÉES au laboratoire depuis le plan
│                      du dépôt, recoupées à l'assemblage — un kit
│                      corrompu est un refus nommé AVANT tout geste ;
│                      L'ENTRÉE 210 : LE CONTRÔLE D54 NEUF — le
│                      scénario MARCHE lui-même les quatre plages
│                      FirstThunk au compte exact [10 · 18 · 6 · 3],
│                      constate les séparateurs NULL et les slots
│                      préremplis : l'habillage d'import fait partie de
│                      la surface de test, la leçon D97 ENTRE AU
│                      SCÉNARIO ; la session naît sur temoin-session.bin,
│                      L'OMBRE byte-à-byte de la pièce — le chargeur
│                      tient loupe.exe, jamais on n'écrit sur une
│                      section vivante) ;
├── temoin-vitrine.bat LE TÉMOIN VITRINE (l'Entrée 207 : la vitrine a
│                      vécu sa première mort SANS témoin — ce run
│                      console capture LES DEUX codes de sortie et le
│                      rapport WER éventuel ; l'Entrée 210 : la vitrine
│                      dev.7 doit VIVRE — 0 et 0 attendus au témoin) ;
└── LISEZMOI-KIT-LOUPE.md  le présent document.
```

## 2. Le geste (quatre temps)

1. **Extraire** le kit COMPLET dans un NOUVEAU dossier (ne jamais
   mélanger les runs — D99 ; si le dossier d'un run ancien existe
   déjà — celui de dev.1 à dev.7 par exemple — créez-en un NEUF,
   `loupe-kit-8b/` si besoin : l'artefact refusé ne se réutilise pas).
   Sur votre Windows 11 : `loupe-kit-8/`.
2. **Lancer le scénario** : `python scenario-loupe.py` (ou
   `py`/`python3` — **un Python 64 bits est requis**). Aucun paquet à
   installer, aucun droit particulier, aucun réseau. Le run dure
   quelques secondes et dit tout à l'écran ; chaque constat est tranché
   binaire, le verdict se rend POST-MORTEM. Les boîtes bloquantes du
   chargeur sont COUPÉES par le mode d'erreur du scénario — un refus
   éventuel est nommé AU TÉMOIN (GetLastError + NTSTATUS consignés) ;
   ET LA CASCADE DIAGNOSTIQUE se joue toute seule (voir S0 ci-dessous) :
   laissez-la finir, le témoin part au coffre QUEL QUE SOIT le verdict.
3. **Vivre la vitrine** (le cœur du grandeur nature) — **LA VITRINE SE
   VIT PAR SON TÉMOIN** : double-cliquez `temoin-vitrine.bat` — LA
   PREMIÈRE fenêtre s'ouvre VIDE (la barre d'état porte l'usage,
   `loupe <fichier>`, et l'ascenseur) : fermez-la par Alt+F4 ; LA SECONDE
   s'ouvre avec la copie `temoin-fichier.bin` : l'entête des colonnes,
   les lignes hexa, le miroir ASCII, **le panneau d'empreintes** (md5 +
   sha256 du fichier entier — la barre du bas), la cellule active
   inversée : fermez-la par Alt+F4. Les DEUX codes de sortie sont
   capturés au témoin (`preuves-loupe/temoin-vitrine.txt`) — **0 et 0
   sont attendus à l'Entrée 210 : la vitrine dev.7 est née pour VIVRE**
   (si un code nommait encore une mort, le témoin le consigne et le
   rapport WER s'il existe — une mort sans témoin ne recoupe pas).
   **PUIS, si le cœur vous en dit, vivez la vitrine à la main** :
   ouvrez un VRAI fichier **depuis la ligne de commande** :
   `loupe.exe monfichier.bin` (ou glissez-déposez un fichier sur
   l'icône). Les gestes :
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
   témoin naît tout seul (`temoin-loupe.txt`), LE TÉMOIN VITRINE est
   REQUIS (`temoin-vitrine.txt`) ; ajoutez-y les captures éventuelles de
   la vitrine (PNG/JPG, nommées `capture-*.png`).

## 3. Ce que le scénario démontre (les temps du run)

- **T0 LE TÉMOIN** : l'empreinte de l'artefact ASSERTÉE avant tout
  geste ; l'image cartographiée (LoadLibraryEx DONT_RESOLVE — le
  scénario est LE CHARGEUR, aucun point d'entrée exécuté) ; les
  adresses scellées CONSTATÉES UN PAR UN (la minilibc M1
  @0x1100/0x1180/0x13C0, la boucle démo @0x15C0, la famille sha M9
  @0xC000+, LA TABLE K[64] @0x2F00 de FIPS 180-4, le qword version R10
  @0x2E80 [0x00010007 — dev.7], le CADRE né poignée INVALIDE) ; LE
  BASERELOC MINIMAL DÉCLARÉ (dirs[5] — la leçon de l'Entrée 204) ;
  **L'HABILLAGE D'IMPORT VÉRIFIÉ (le contrôle D54 de l'Entrée 210 : les
  QUATRE plages FirstThunk marchées au compte exact [10 · 18 · 6 · 3],
  les séparateurs NULL constatés, les slots préremplis — le motif D54
  ENTIER, la leçon D97 au scénario)** ; l'IAT RÉSOLUE par le scénario
  (37 feuilles aux QUATRE plages du plan — VirtualProtect le temps de
  la pose).
- **T1 LA SESSION** : loupe-01 à son adresse scellée — le VRAI fichier
  ouvert par l'application (CreateFileW par l'IAT résolue), le cadre
  relu champ à champ — sur **L'OMBRE BYTE-À-BYTE DE LA PIÈCE**
  (`temoin-session.bin`, la copie née et morte au run : l'Entrée 208).
- **T2 LA DOUBLE LECTURE** : loupe-02 la fenêtre au tampon == le
  fichier lu par Python (les DEUX lecteurs indépendants) ; loupe-07 le
  panneau (md5 + sha256 du fichier ENTIER par fenêtres glissantes) ==
  hashlib — **ET LA PIÈCE DE L'ÈRE JUGÉE PAR SA PROPRE APPLICATION SUR
  SON OMBRE : loupe-07 rend le sha256 asserté de la pièce**.
- **T3 LES LIGNES** : loupe-08 la ligne == le format composé en Python
  pur ; la ligne finale incomplète garde le FORMAT.
- **T4 LA RECHERCHE** : loupe-13 (le memcmp SCELLÉ M1 à l'œuvre) ==
  bytes.find sur les octets vrais.
- **T5 L'ÉDITION** : la boucle ENTIÈRE sur une copie — ouvrir, la
  saisie « 4d » (l'attente consommée par l'engagement), Ctrl+S
  (l'écriture À L'OCTET par le VRAI WriteFile — **le contrat publié de
  loupe-17 : 0 = OK, le compte des octets part à la barre d'état —
  PROUVÉ AU TERRAIN par le run dev.7, l'Entrée 209**) ; le fichier
  revérifié : EXACTEMENT l'octet changé, la taille CONSTANTE, la marque
  levée.
- **T6 LES REJETS** : l'échec NOMMÉ — le motif absent → -1 FIN ; le
  chemin qui ne désigne rien → -2 ABSENT (**le contrat c_int64 ENFIN
  tenu des deux mains : la pièce étend ses rendus au 64 bits, le kit
  lit le qword entier — [EAX-SANS-SIGNE] chassé, l'Entrée 210**) ; la
  session double → -5 (l'offrande est L'OMBRE rouvrable, jamais la
  pièce sous le chargeur) ; le décalage hors bornes → -3 (un refus
  vaut plus qu'un vert muet).
- **T7 LA CLÔTURE** : loupe-03 le cadre re-vierge, idempotent ;
  l'artefact relu INCHANGÉ (le run ne touche pas la pièce).
- **S0 LA SONDE (l'Entrée 205 — LA CASCADE DIAGNOSTIQUE)** : après le
  run (ou à l'échec de la cartographie), le scénario reconstitue UN À
  UN les axes par lesquels dev.2 sortait de l'enveloppe de la lignée —
  sur des COPIES TEMPORAIRES nées et mortes dans %TEMP% (loupe.exe
  n'est JAMAIS écrit) : **le VRAI chargeur Windows NOMME l'axe fautif**
  — le témoin consigne chaque verdict VERTE/REFUS + GetLastError +
  NTSTATUS.

## 4. Les frontières nommées (l'honnêteté du terrain)

- Le scénario NE LANCE PAS la vitrine (aucun point d'entrée exécuté) :
  les blocs sont appelés à leurs adresses scellées, la main du kit sur
  la pédale — la vitrine se vit PAR SON TÉMOIN (temoin-vitrine.bat),
  puis à la main si le cœur vous en dit ;
- le scénario n'écrit JAMAIS loupe.exe (lecture seule, relu à la
  clôture) ; L'OMBRE (temoin-session.bin) est une copie née et morte AU
  RUN, jamais l'original ; LA SONDE écrit ses copies de diagnostic
  dans %TEMP% uniquement, et les EFFACE ; la carte privée ne voyage pas
  (R1) ;
- les blocs d'empreintes appellent la famille sha du SCELLÉ M9 aux
  adresses d'origine (R7) — le panneau sha256 de l'application EST le
  sha256 prouvé au jalon M9 ;
- si un dossier `preuves-loupe/` existe déjà d'un run ancien, NE LE
  MÉLANGEZ PAS (D99) : un dossier neuf par run.

## 5. Après le run

Le labo recoupe sur pièces (D138/D145/D148) : le témoin relu, LE
TÉMOIN VITRINE REQUIS, les constats croisés contre le dépôt, les
empreintes recalculées. **ET SI LE VERT TIENT — le scénario ENTIER
(T0 → S0, le contrôle D54 en tête) ET LA VITRINE VIVANTE (les deux
codes à 0) : LA BALISE `loupe 0.1.0` SCELLÉE sur run terrain recoupé —
LE JALON M10, la méthode TRIADE entière prouvée par la CRÉATION : de
l'intention (la couche I) à l'octet vécu chez son utilisateur.**
