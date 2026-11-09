# KIT TERRAIN M10-(e) — LE RUN DE LOUPE, LE GRANDEUR NATURE (win)

> Le test grandeur nature (TGN, D171) : coder une application ENTIÈREMENT
> avec TRIADE. La couche I a posé les 18 spécifications ; quatre chantiers
> ont noté-mesuré-prouvé chaque bloc (157 contrôles verts aux trois
> graines) ; la cérémonie d'ère a ouvert le build (le garde à QUATORZE
> arbres verts — Entrée 201) ; le build est NÉ et a vécu HUIT RUNS
> terrain. **LE HUITIÈME EST LE PLUS LOIN JAMAIS VÊCU : T0 → T7 TOUT
> VERT — LA PREMIÈRE FOIS** (**loupe.exe 0.1.0-dev.7**, 127 488 o,
> sha256 `388d468067cbf054…4d9bbc`, la carte génération 13 — Entrées
> 202 → … → 210 → 211 → **213**) : le contrôle D54 en tête [les QUATRE
> plages FirstThunk marchées au compte exact, les séparateurs NULL, les
> slots préremplis], la session sur L'OMBRE, la double lecture, LE
> PANNEAU [la pièce jugée par sa propre application], les lignes, la
> recherche, LA BOUCLE D'ÉDITION ENTIÈRE, **puis LES QUATRE REJETS DU
> T6 — TOUS VERTS POUR LA PREMIÈRE FOIS** [le chemin qui ne désigne
> rien → -2 ; la session double → -5 ; le décalage hors bornes → -3 ;
> le motif absent → -1 : **[EAX-SANS-SIGNE] ACQUITTÉ** — l'extension
> 64 bits de l'Entrée 210 rendue au terrain], la clôture T7 [l'artefact
> relu INCHANGÉ]. **LE CONTRAT FONCTIONNEL DE LOUPE EST PROUVÉ AU
> TERRAIN, ENTIÈREMENT — loupe-01 à loupe-17, les dix-huit
> spécifications de la couche I vécues par le VRAI Windows.**
> PUIS DEUX FAITS DEMEURENT : **[SONDE-PYTHON] À LA SONDE S0** — le
> scénario dev.8 appelait `ctypes.SetLastError` / `ctypes.GetLastError`
> qui N'EXISTENT PAS dans le module ctypes : la cascade diagnostique de
> l'Entrée 205 mourut sur place, ses sondes jamais jouées (le défaut
> était latent depuis l'origine de S0 — invisible tant que le run
> n'avait jamais atteint S0) ; ET **LA VITRINE MORTE POUR LA CINQUIÈME
> FOIS** : 0xC0000005 sur LES DEUX fenêtres, AUCUN rapport WER — la
> fenêtre jamais née. **LA PIÈCE EST ACQUITTÉE DE TOUTE CHARGE NOMMABLE
> AU LABO** (l'autopsie de l'Entrée 213, la plus complète jamais vécue :
> la table d'imports vérifiée DESCRIPTEUR PAR DESCRIPTEUR [OFT/FT/noms,
> plages séparées, terminateurs], le chemin d'entrée démonté
> INSTRUCTION PAR INSTRUCTION [la classe WNDCLASSEXW champ à champ, les
> 12 arguments de CreateWindowExW, chaque lea/call résolu], le WndProc,
> le peintre, la boucle, l'alignement de pile à chaque frontière, ZÉRO
> SSE dans l'image, ZÉRO pointeur absolu, les 63 sites d'appel
> recoupés, aucune écriture en page lecture-seule ; ET **LE SIMULATEUR
> DE VITRINE NÉ AU LABO** : la pièce exécutée sous émulation complète —
> l'entrée, la classe, la fenêtre, la boucle à messages, WM_SIZE AVEC
> SESSION, WM_PAINT LE PEINTRE LECTEUR, WM_VSCROLL — **LES DEUX
> VITRINES VÉCUES VERTES, SORTIE PROPRE ExitProcess(0)** : le défaut
> vit dans l'interaction avec le VRAI système, pas dans les octets que
> le labo peut lire). **LA NEUVIÈME VAGUE EST CELLE DU TÉMOIN
> PORTANT** : la pièce demeure dev.7 — l'ACQUITTÉE, aucune retouche
> aveugle (un défaut sans nom ne reçoit pas de correctif, la méthode) —
> ET LE KIT dev.9 porte TROIS GESTES : **la sonde S0 RÉPARÉE**
> (`k32.SetLastError` + `ctypes.get_last_error` + `use_last_error` :
> la cascade de l'Entrée 205 vivra ENFIN son terrain), **les littéraux
> périmés chassés** (l'en-tête du témoin et le message PORTE-R10
> disaient « dev.6 » : VERSION_TXT est désormais DÉRIVÉ de VERSION_R10,
> le littéral ne dérivera plus jamais), et **LE TÉMOIN VITRINE PORTANT
> [4/4]** : si la mort vient encore, **LE JOURNAL D'ÉVÉNEMENTS DE
> WINDOWS LA NOMMERA** — wevtutil consigne l'Application Error 1000 :
> le module fautif et le décalage de l'exception, la pièce du système
> que le témoin muet ne pouvait pas rendre.

## 1. Ce que ce kit contient

```
loupe-kit-9/
├── loupe.exe          l'ARTEFACT 0.1.0-dev.7 (127 488 o, sha256
│                      388d4680… — INCHANGÉ DEPUIS L'ENTRÉE 210 :
│                      l'ACQUITTÉE du huitième run — l'IAT relogée à
│                      0x3100 en QUATRE plages SÉPARÉES PAR NULL
│                      préremplies du motif D54, les rendus négatifs
│                      étendus au 64 bits [les QUATRE rejets du T6
│                      ONT VÉCU VERTS au terrain] ; lecture seule
│                      pour le run ; la carte privée ne voyage JAMAIS
│                      avec l'artefact, R1) ;
├── scenario-loupe.py  LE SCÉNARIO dev.9 (python SEUL : ctypes,
│                      hashlib, os, platform, struct, sys, tempfile —
│                      les constantes FIGÉES au laboratoire depuis le
│                      plan du dépôt, recoupées à l'assemblage) :
│                      LE CONTRÔLE D54 en tête [les quatre plages
│                      marchées au compte exact — VERT au huitième
│                      run] ; LA SONDE S0 RÉPARÉE [k32.SetLastError +
│                      ctypes.get_last_error sur un WinDLL né
│                      use_last_error=True : les cinq axes de dev.2
│                      reconstitués UN À UN vivront ENFIN leur
│                      terrain] ; VERSION_TXT DÉRIVÉ de VERSION_R10
│                      [l'en-tête du témoin ne portera plus jamais un
│                      littéral périmé] ; le texte T0 nomme la carte à
│                      sa GÉNÉRATION RÉELLE [13 — la régénération est
│                      dette au labo, l'Entrée 211] ;
├── temoin-vitrine.bat LE TÉMOIN VITRINE dev.9 — PORTANT : les quatre
│                      temps [1/4] la vitrine vide, [2/4] la vitrine
│                      avec fichier, [3/4] les rapports WER éventuels,
│                      **[4/4] LE JOURNAL D'ÉVÉNEMENTS — wevtutil
│                      consigne les trois derniers Application Error
│                      (1000/1001) : LE MODULE FAUTIF ET LE DÉCALAGE
│                      DE L'EXCEPTION NOMMÉS** — si la sixième mort
│                      vient, elle sera NOMMÉE PAR LE SYSTÈME ;
└── LISEZMOI-KIT-LOUPE.md  le présent document.
```

## 2. Le geste (quatre temps)

1. **Extraire** le kit COMPLET dans un NOUVEAU dossier (ne jamais
   mélanger les runs — D99 ; si le dossier d'un run ancien existe
   déjà — celui de dev.1 à dev.8 par exemple — créez-en un NEUF,
   `loupe-kit-9b/` si besoin : l'artefact refusé ne se réutilise pas).
   Sur votre Windows 11 : `loupe-kit-9/`.
2. **Lancer le scénario** : `python scenario-loupe.py` (ou
   `py`/`python3` — **un Python 64 bits est requis**). Aucun paquet à
   installer, aucun droit particulier, aucun réseau. Le run dure
   quelques secondes et dit tout à l'écran ; chaque constat est tranché
   binaire, le verdict se rend POST-MORTEM. Les boîtes bloquantes du
   chargeur sont COUPÉES par le mode d'erreur du scénario — un refus
   éventuel est nommé AU TÉMOIN (GetLastError + NTSTATUS consignés) ;
   ET LA CASCADE DIAGNOSTIQUE S0 se joue toute seule cette fois —
   réparée au dev.9 : laissez-la finir, le témoin part au coffre QUEL
   QUE SOIT le verdict.
3. **Vivre la vitrine** (le cœur du grandeur nature) — **LA VITRINE SE
   VIT PAR SON TÉMOIN** : double-cliquez `temoin-vitrine.bat` — LA
   PREMIÈRE fenêtre s'ouvre VIDE (la barre d'état porte l'usage,
   `loupe <fichier>`, et l'ascenseur) : fermez-la par Alt+F4 ; LA SECONDE
   s'ouvre avec la copie `temoin-fichier.bin` : l'entête des colonnes,
   les lignes hexa, le miroir ASCII, **le panneau d'empreintes** (md5 +
   sha256 du fichier entier — la barre du bas), la cellule active
   inversée : fermez-la par Alt+F4. Les DEUX codes de sortie sont
   capturés au témoin (`preuves-loupe/temoin-vitrine.txt`) — **0 et 0
   sont attendus : la vitrine dev.7 est née pour VIVRE** (cinq morts
   déjà — les quatre premières ont nommé leur défaut, la cinquième a
   ACQUITTÉ la pièce au labo : **si la sixième vient, LE JOURNAL
   D'ÉVÉNEMENTS [4/4] LA NOMMERA** — module fautif, décalage de
   l'exception).
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
   REQUIS (`temoin-vitrine.txt` — avec son [4/4]) ; ajoutez-y les
   captures éventuelles de la vitrine (PNG/JPG, nommées
   `capture-*.png`).

## 3. Ce que le scénario démontre (les temps du run)

- **T0 LE TÉMOIN** : l'empreinte ASSERTÉE (sha256/taille de la pièce),
  l'image cartographiée DONT_RESOLVE [le scénario est LE CHARGEUR,
  aucun point d'entrée exécuté], **LE CONTRÔLE D54** [l'habillage
  d'import MARCHE : les QUATRE plages au compte exact, les
  séparateurs NULL, les slots préremplis — VERT au huitième run], les
  adresses scellées, l'IAT résolue aux slots du plan ;
- **T1 → T7 LE CONTRAT ENTIÈREMENT VÉCU** (la première fois au
  huitième run) : la session sur L'OMBRE byte-à-byte, la double
  lecture, LE PANNEAU [la pièce jugée par sa propre application : le
  sha256 du témoin == hashlib], les lignes au format composé, la
  recherche == bytes.find, LA BOUCLE D'ÉDITION [l'octet mûté SEUL, la
  taille constante, la marque levée, la session close], LES QUATRE
  REJETS NOMMÉS [-2 ABSENT, -5 ENTRÉE, -3 HORS-BORNES, -1 FIN —
  l'offrande de la session double est L'OMBRE, jamais la pièce], la
  clôture [l'artefact relu INCHANGÉ] ;
- **S0 LA SONDE (l'Entrée 205 — LA CASCADE DIAGNOSTIQUE, RÉPARÉE au
  dev.9)** : après le run (ou à l'échec de la cartographie), le
  scénario reconstitue UN À UN les axes par lesquels dev.2 sortait de
  l'enveloppe de la lignée — sur des COPIES TEMPORAIRES nées et mortes
  dans %TEMP% (loupe.exe n'est JAMAIS écrit) : **le VRAI chargeur
  Windows NOMME l'axe fautif** — le témoin consigne chaque verdict
  VERTE/REFUS + GetLastError + NTSTATUS.

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
TÉMOIN VITRINE REQUIS (avec son [4/4] — le journal d'événements), les
constats croisés contre le dépôt, les empreintes recalculées. **ET SI
LE VERT TIENT — le scénario ENTIER (T0 → S0, le contrôle D54 en tête,
LA CASCADE RÉPARÉE) ET LA VITRINE VIVANTE (les deux codes à 0) : LA
BALISE `loupe 0.1.0` SCELLÉE sur run terrain recoupé — LE JALON M10,
la méthode TRIADE entière prouvée par la CRÉATION : de l'intention
(la couche I) à l'octet vécu chez son utilisateur.**
