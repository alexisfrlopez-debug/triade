#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le LISEZMOI-KIT-LOUPE.md du kit dev.10 + l'assemblage du dossier et
du zip (build-dev10/loupe-kit-10/ + build-dev10/kit-loupe.zip)."""
import os
import zipfile

DST = "/home/z/my-project/build-dev10"
SHA_V8 = "054de960c31425d022f6900f27e59bdd82a120b0b3fe543a67e778867e9c7a69"

LISEZMOI = f"""# KIT TERRAIN M10-(e) — LE RUN DE LOUPE, LE GRANDE NATURE (win)

> Le test grandeur nature (TGN, D171) : coder une application ENTIÈREMENT
> avec TRIADE. La couche I a posé les 18 spécifications ; quatre chantiers
> ont noté-mesuré-prouvé chaque bloc (157 contrôles verts aux trois
> graines) ; la cérémonie d'ère a ouvert le build (le garde à QUATORZE
> arbres verts — Entrée 201) ; le build est NÉ et a vécu NEUF RUNS
> terrain. **LE NEUVIÈME RUN : T0 → T7 TOUT VERT POUR LA SECONDE FOIS —
> ET LA SIXIÈME MORT DE LA VITRINE NOMMÉE, PAR LE SYSTÈME PUIS PAR LE
> LABO** (**loupe.exe 0.1.0-dev.8**, 127 488 o, sha256
> `{SHA_V8}`, la carte génération 16 — Entrées 202 → … → 211 → 213 →
> **214**) : [T0] le contrôle D54 vécu vert [les QUATRE plages FirstThunk
> au compte exact 10 · 18 · 6 · 3] ; [T1]→[T5] le contrat tenu [la
> session, la double lecture, LE PANNEAU, les lignes, la recherche, la
> boucle d'édition] ; [T6] LES QUATRE REJETS NOMMÉS pour la seconde
> fois [-2 ABSENT · -5 ENTRÉE · -3 HORS-BORNES · -1 FIN] ; [T7]
> l'artefact relu INCHANGÉ ; PUIS DEUX FAITS DEMEURENT : **[S0]
> [PERMISSION-SONDE]** — la sonde réparée de l'Entrée 213 VÉCUT
> (l'AttributeError de ctypes est morte) mais mourut sur SON PROPRE
> NETTOYAGE : `PermissionError(13)` — un module LoadLibraryEx-é est
> CHARGÉ, il se LIBÈRE (FreeLibrary) avant de se supprimer — la cascade
> ne joua pas ; ET **LA VITRINE MORTE LA SIXIÈME FOIS — MAIS NOMMÉE PAR
> LE JOURNAL D'ÉVÉNEMENTS [4/4]** : BEX64, module fautif « unknown »,
> 0xC0000005, exécution sur mémoire non exécutable — le témoin portant
> du dev.9 FIT SON OFFICE. **LE LABO A NOMMÉ LA CAUSE SUR LES OCTETS DE
> LA PIÈCE : [OFT-QWORD]** — les QUATRE tableaux OriginalFirstThunk
> étaient écrits à PAS DE QWORD (RVA + quatre octets de zéro) au lieu
> du PAS DE DWORD du format PE : le VRAI chargeur lit OFT[1] = 0,
> CROIT chaque liste terminée, résout UNE fonction par DLL — les 33
> autres slots IAT gardent leur valeur fichier (les RVA des noms) — le
> SECOND appel de l'entrée (GetCommandLineW, slot 0x3108) SAUTE à
> l'adresse absolue 0x2A53 : page non mappée, aucun module — LA MORT
> NOMMÉE. **LA CÉCITÉ DES VERTS EXPLIQUÉE** : le scénario-chargeur pose
> les 37 feuilles À LA MAIN (il ne lit jamais l'OFT), le simulateur
> branche des relais, la sonde 205 cartographie DONT_RESOLVE (le
> drapeau qui SAUTE la résolution des imports), le contrôle D54 marchait
> la FirstThunk — JAMAIS l'OFT. **LA RETOUCHE DE L'ENTRÉE 214** : les
> QUATRE OFT COMPACTÉS AU PAS DE DWORD [10 · 18 · 6 · 3 + terminateurs],
> EN PLACE — les pointeurs de descripteurs inchangés, la table de noms
> inchangée, le .text/.text2/.data/les en-têtes OCTET-IDENTIQUES, les
> adresses scellées INTACTES, la taille CONSTANTE 127 488 o — 89 octets
> modifiés en tout, le qword version porté à dev.8 ; **ET LES LEÇONS
> INSTITUTIONNALISÉES AU KIT dev.10** : le scénario MARCHE LUI-MÊME LES
> QUATRE OFT au pas DWORD du chargeur [chaque entrée == le
> préremplissage de son slot — [OFT-QWORD] ne passera plus jamais], LA
> SONDE 205 RÉPARÉE DE SON PROPRE NETTOYAGE [FreeLibrary avant
> suppression, chaque essai dans son try : la cascade ne meurt jamais
> sur son propre geste], ET LA NOUVELLE SONDE DE LIAISON [une copie
> chargée SANS DONT_RESOLVE, l'entrée neutralisée d'un octet ret, les
> 37 slots RELUS : le VRAI chargeur doit y avoir posé LES ADRESSES DES
> FONCTIONS — la pièce LIÉE, la vitrine LIBRE DE VIVRE].

## 1. Ce que ce kit contient

```
loupe-kit-10/
├── loupe.exe          l'ARTEFACT 0.1.0-dev.8 (127 488 o, sha256
│                      054de960… — LA RETOUCHE DE L'ENTRÉE 214 : les
│                      QUATRE OFT compactés au pas DWORD du chargeur —
│                      [OFT-QWORD] nommé au run 9, la sixième mort
│                      reçut SA retouche ; le .text/.text2/.data
│                      octet-identiques au dev.7, les adresses scellées
│                      INTACTES, la taille CONSTANTE ; lecture seule
│                      pour le run ; la carte privée ne voyage JAMAIS
│                      avec l'artefact, R1) ;
├── scenario-loupe.py  LE SCÉNARIO dev.10 (python SEUL : ctypes,
│                      hashlib, os, platform, struct, sys, tempfile —
│                      les constantes FIGÉES au laboratoire depuis le
│                      plan du dépôt, recoupées à l'assemblage) :
│                      LE CONTRÔLE D54 ÉTENDU [les quatre plages
│                      marchées au compte exact — ET LES QUATRE OFT
│                      MARCHÉS AU PAS DWORD DU CHARGEUR, chaque entrée
│                      == le préremplissage de son slot] ; LA SONDE S0
│                      RÉPARÉE DE SON NETTOYAGE [FreeLibrary avant
│                      suppression — le PermissionError(13) du run 9
│                      ne passera plus — et chaque essai dans son try :
│                      la cascade ne meurt jamais sur son propre
│                      geste] ; LA NOUVELLE SONDE DE LIAISON [une
│                      copie chargée SANS DONT_RESOLVE, l'entrée
│                      neutralisée d'un octet ret, les 37 slots RELUS :
│                      le VRAI chargeur doit y avoir posé les ADRESSES
│                      DES FONCTIONS] ; VERSION_TXT DÉRIVÉ de
│                      VERSION_R10 ; le texte T0 nomme la carte à sa
│                      GÉNÉRATION RÉELLE [16 — la régénération est
│                      dette au labo, l'Entrée 211] ;
├── temoin-vitrine.bat LE TÉMOIN VITRINE dev.10 — PORTANT : les quatre
│                      temps [1/4] la vitrine vide, [2/4] la vitrine
│                      avec fichier, [3/4] les rapports WER éventuels,
│                      **[4/4] LE JOURNAL D'ÉVÉNEMENTS — wevtutil
│                      consigne les trois derniers Application Error
│                      (1000/1001) : LE MODULE FAUTIF ET LE DÉCALAGE
│                      DE L'EXCEPTION NOMMÉS PAR LE SYSTÈME** — la
│                      sixième mort fut ainsi nommée ; si la septième
│                      vient, elle sera nommée de la même façon ;
└── LISEZMOI-KIT-LOUPE.md  le présent document.
```

## 2. Le geste (quatre temps)

1. **Extraire** le kit COMPLET dans un NOUVEAU dossier (ne jamais
   mélanger les runs — D99 ; si le dossier d'un run ancien existe
   déjà — celui de dev.1 à dev.9 par exemple — créez-en un NEUF,
   `loupe-kit-10b/` si besoin : l'artefact refusé ne se réutilise pas).
   Sur votre Windows 11 : `loupe-kit-10/`.
2. **Lancer le scénario** : `python scenario-loupe.py` (ou
   `py`/`python3` — **un Python 64 bits est requis**). Aucun paquet à
   installer, aucun droit particulier, aucun réseau. Le run dure
   quelques secondes et dit tout à l'écran ; chaque constat est tranché
   binaire, le verdict se rend POST-MORTEM. Les boîtes bloquantes du
   chargeur sont COUPÉES par le mode d'erreur du scénario — un refus
   éventuel est nommé AU TÉMOIN (GetLastError + NTSTATUS consignés) ;
   ET LES CASCADES DIAGNOSTIQUES se jouent toutes seules cette fois —
   la 205 réparée ET la liaison de l'Entrée 214 : laissez-les finir, le
   témoin part au coffre QUEL QUE SOIT le verdict.
3. **Vivre la vitrine** (le cœur du grandeur nature) — **LA VITRINE SE
   VIT PAR SON TÉMOIN** : double-cliquez `temoin-vitrine.bat` — LA
   PREMIÈRE fenêtre s'ouvre VIDE (la barre d'état porte l'usage,
   `loupe <fichier>`, et l'ascenseur) : fermez-la par Alt+F4 ; LA SECONDE
   s'ouvre avec la copie `temoin-fichier.bin` : l'entête des colonnes,
   les lignes hexa, le miroir ASCII, **le panneau d'empreintes** (md5 +
   sha256 du fichier entier — la barre du bas), la cellule active
   inversée : fermez-la par Alt+F4. Les DEUX codes de sortie sont
   capturés au témoin (`preuves-loupe/temoin-vitrine.txt`) — **0 et 0
   sont attendus : la vitrine dev.8 est née pour VIVRE** (six morts
   déjà — les cinq premières ont nommé leur défaut ou acquitté la
   pièce, LA SIXIÈME A NOMMÉ LE SIEN : [OFT-QWORD] — la retouche est
   portée, la liaison sera VÉCUE par la sonde avant même la fenêtre :
   **si la septième mort vient, LE JOURNAL D'ÉVÉNEMENTS [4/4] LA
   NOMMERA** — module fautif, décalage de l'exception).
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
  aucun point d'entrée exécuté], **LE CONTRÔLE D54 ÉTENDU** [l'habillage
  d'import MARCHE : les QUATRE plages au compte exact, les séparateurs
  NULL, les slots préremplis — **ET LES QUATRE OFT MARCHÉS AU PAS DWORD
  DU CHARGEUR, chaque entrée == le préremplissage de son slot** — VERT
  au neuvième run pour la FirstThunk, l'OFT y est désormais], les
  adresses scellées, l'IAT résolue aux slots du plan ;
- **T1 → T7 LE CONTRAT ENTIÈREMENT VÉCU** (la première fois au
  huitième run, tenu au neuvième) : la session sur L'OMBRE byte-à-byte,
  la double lecture, LE PANNEAU [la pièce jugée par sa propre
  application : le sha256 du témoin == hashlib], les lignes au format
  composé, la recherche == bytes.find, LA BOUCLE D'ÉDITION [l'octet
  mûté SEUL, la taille constante, la marque levée, la session close],
  LES QUATRE REJETS NOMMÉS [-2 ABSENT, -5 ENTRÉE, -3 HORS-BORNES, -1
  FIN — l'offrande de la session double est L'OMBRE, jamais la pièce],
  la clôture [l'artefact relu INCHANGÉ] ;
- **S0 LA CASCADE 205 (RÉPARÉE DE SON PROPRE NETTOYAGE)** : les axes de
  dev.2 reconstitués UN À UN sur des COPIES TEMPORAIRES nées et mortes
  dans %TEMP% (loupe.exe n'est JAMAIS écrit) : **le VRAI chargeur
  Windows NOMME l'axe fautif** — le témoin consigne chaque verdict
  VERTE/REFUS + GetLastError + NTSTATUS, et le module chargé est
  LIBÉRÉ avant sa suppression — la cascade ne meurt JAMAIS sur son
  propre geste ;
- **LA LIAISON (LA SONDE DE L'ENTRÉE 214)** : une copie chargée SANS
  DONT_RESOLVE — l'entrée de la copie neutralisée d'un seul octet ret
  (la fenêtre n'y est jamais lancée) — LES 37 SLOTS RELUS : le VRAI
  chargeur doit y avoir posé **LES ADRESSES DES FONCTIONS** — la
  sixième mort [OFT-QWORD] était invisible à toute la machinerie
  précédente ; désormais **la liaison est VÉCUE AU TÉMOIN avant même
  que la fenêtre ne s'ouvre**.

## 4. Les frontières nommées (l'honnêteté du terrain)

- Le scénario NE LANCE PAS la vitrine (aucun point d'entrée exécuté) :
  les blocs sont appelés à leurs adresses scellées, la main du kit sur
  la pédale — la vitrine se vit PAR SON TÉMOIN (temoin-vitrine.bat),
  puis à la main si le cœur vous en dit ;
- le scénario n'écrit JAMAIS loupe.exe (lecture seule, relu à la
  clôture) ; L'OMBRE (temoin-session.bin) est une copie née et morte AU
  RUN, jamais l'original ; LES SONDES écrivent leurs copies de
  diagnostic dans %TEMP% uniquement, et les EFFACENT ; la carte privée
  ne voyage pas (R1) ;
- les blocs d'empreintes appellent la famille sha du SCELLÉ M9 aux
  adresses d'origine (R7) — le panneau sha256 de l'application EST le
  sha256 prouvé au jalon M9 ;
- si un dossier `preuves-loupe/` existe déjà d'un run ancien, NE LE
  MÉLANGEZ PAS (D99) : un dossier neuf par run.

## 5. Après le run

Le labo recoupe sur pièces (D138/D145/D148) : le témoin relu, LE
TÉMOIN VITRINE REQUIS (avec son [4/4] — le journal d'événements), les
constats croisés contre le dépôt, les empreintes recalculées. **ET SI
LE VERT TIENT — le scénario ENTIER (T0 → S0 → LA LIAISON, le contrôle
D54 ÉTENDU en tête, LA CASCADE RÉPARÉE) ET LA VITRINE VIVANTE (les deux
codes à 0) : LA BALISE `loupe 0.1.0` SCELLÉE sur run terrain recoupé —
LE JALON M10, la méthode TRIADE entière prouvée par la CRÉATION : de
l'intention (la couche I) à l'octet vécu chez son utilisateur.**
"""

open(os.path.join(DST, "LISEZMOI-KIT-LOUPE.md"), "w",
     encoding="utf-8").write(LISEZMOI)
print("LISEZMOI-KIT-LOUPE.md dev.10 : ÉCRIT")

# --- l'assemblage ------------------------------------------------------------
kit = os.path.join(DST, "loupe-kit-10")
os.makedirs(kit, exist_ok=True)
for piece in ("loupe.exe", "scenario-loupe.py", "temoin-vitrine.bat",
              "LISEZMOI-KIT-LOUPE.md"):
    import shutil
    shutil.copy2(os.path.join(DST, piece), os.path.join(kit, piece))
print("loupe-kit-10/ : les QUATRE pièces assemblées")

zipchemin = os.path.join(DST, "kit-loupe.zip")
with zipfile.ZipFile(zipchemin, "w", zipfile.ZIP_DEFLATED) as z:
    for piece in ("LISEZMOI-KIT-LOUPE.md", "loupe.exe", "scenario-loupe.py",
                  "temoin-vitrine.bat"):
        z.write(os.path.join(kit, piece), arcname=piece)
import hashlib
h = hashlib.md5(open(zipchemin, "rb").read()).hexdigest()
print(f"kit-loupe.zip : ÉCRIT (md5 {h})")
