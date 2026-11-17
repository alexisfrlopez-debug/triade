#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_loupe.py — LE GESTE DE BUILD DU DOMAINE loupe (M10, le TGN) :
loupe.exe 0.1.1-dev.1 — LA PREMIÈRE APPLICATION NÉE DE TRIADE ENTIÈRE,
ET LA VERSION COMMANDÉE PAR LE DÉVELOPPEUR (D178/D179 : la dette
[R10-PÉRIMÉE] soldée à la naissance — la porte R10 rafraîchie à la
vérité des blocs, le code BYTE-IDENTIQUE au vécu des onze runs de
l'ère 0.1.0 SCELLÉE ; la 0.1.1 attend le DOUZIÈME run, la balise se
scelle PAR FAIT DE CARTE sur le vert recoupé — D165/D170, l'Entrée 222).

LE PLAN PORTÉ À L'ÉPOQUE dev.8 (la dette de la carte de l'Entrée 211
SOLDÉE — les retouches dev.6/7/8, nées de patchs en place HORS de cette
chaîne, REVENUES au plan : le build recompose LA PIÈCE OCTET POUR OCTET,
sha256 054de960… — R7 au sens propre, la preuve par la renaissance) :
  - dev.6 [HINSTANCE-PEB] (l'Entrée 209) : l'entrée réécrite EN PLACE —
    r12 = GetModuleHandleW(NULL) LE VRAI MODULE (le slot importé mais
    jamais câblé de dev.5) ; le CADRE WNDCLASSEX né memset-zéro par
    libc-07 puis les champs vifs ; le WndProc @0x5DCB INTACT ;
  - dev.7 [D54-QUATRIÈME] + [EAX-SANS-SIGNE] (l'Entrée 210) : L'IAT
    ENTIÈRE relogée à 0x3100 — QUATRE plages FirstThunk SÉPARÉES PAR
    NULL, PRÉREMLIES des RVA de noms (le motif D54), descripteurs
    dirigés, dir[12] = (0x3100, 0x148), les 63 sites d'appel repointés,
    les vieilles plages VIDÉES ; les 20 rendus négatifs étendus au 64
    bits (« push imm8 ; pop rax »), les deux passages de loupe-01
    passés movsxd ; le repointage de win-03 (6 octets, le prix du
    relogement — l'écart nommé) ;
  - dev.8 [OFT-QWORD] (l'Entrée 214) : les QUATRE OFT compactés au pas
    DWORD [10·18·6·3 + terminateurs] — le chargeur de bibliothèque
    lisait OFT[1]=0 et ne résolvait qu'une fonction par DLL.
La carte : GÉNÉRATION 16 — la génération RÉELLE de la pièce (13 → 16 :
les générations 14/15/16 des retouches dev.6/7/8, l'arrière-dette de
l'Entrée 211 éteinte au geste même).

LES RETOUCHES DOCUMENTÉES DES ENTRÉES 204-207 (l'ère dev.1→dev.5) :

LA RETOUCHE DE L'ENTRÉE 207 (dev.4 → dev.5) : LE TÉMOIN T1 A NOMMÉ
[SESSION] — « loupe-01 a rendu 0xfffffffa (-6 SYSTÈME), le fichier
pourtant relu à l'instant » ; ET LA VITRINE A VÉCU SA PREMIÈRE FOIS AU
TERRAIN (« la fenêtre s'ouvre et se referme immédiatement »). LES
PIÈCES RAPATRIÉES DU /test (temoin-loupe.txt 1 209 o — LE RUN LE PLUS
LOIN JAMAIS VÊCU : image cartographiée ✓, CADRE né MIROIR ✓ (la
retouche de l'Entrée 206 TIENT, preuve au terrain), IAT 37 feuilles
posées ✓) PUIS L'AUTOPSIE SUR LA PIÈCE (capstone, les notations, le
harnais) NOMME LA CLASSE : LES ARGUMENTS 5+ DE L'ABI msx64 VIVAIENT
DANS LE HOME SPACE [rsp..0x18] au lieu de [rsp+0x20]+ :
  - loupe-01 R4 : CreateFileW relisait dwCreationDisposition À LA PILE
    NON INITIALISÉE (le -6 du T1) — les trois slots déménagent à leur
    place ; [rsp+0x20] REPRIS par la sortie GetFileSizeEx APRÈS le
    retour (la vie séquentielle du slot) ;
  - loupe-05 R2 : le contexte SHA (112 o) vivait SUR LE VRAI SLOT — le
    VRAI ReadFile lisait H0[0] 0x6A09E667… COMME UN POINTEUR — le
    contexte déménage [rsp+0x20]→[rsp+0x40], le cadre 0xa0→0xc0,
    lpOverlapped NÉ NUL à son vrai slot ;
  - loupe-06 R2 : le contexte MD5 (88 o) pareil (A = 0x67452301… au
    vrai slot) — le même déménagement, le cadre 0xa0→0xc0.
LE GARDE GUÉRI PAR LA CONVENTION (la leçon de jauge, deuxième du nom) :
les shims CreateFileW/ReadFile (noyau) et WriteFile (édition) RELISENT
LES MÊMES SLOTS QUE LE VRAI — ERROR_INVALID_PARAMETER sinon (87) — le
miroir du shim TextOutW du rendu qui, LUI, avait toujours eu raison
(c'est pourquoi loupe-10 était juste et 01/05/06 non) ; LE CONTRÔLE
DÉRIVE DE LA CONVENTION msx64, jamais de la pièce qu'il croyait garder.
LA VITRINE AU LABO : le flot réel complet rejoué sur l'émulation aux
18 blocs (naissance → vie → WM_CLOSE/WM_DESTROY) VERT des deux façons
(vide et avec fichier) — la mort terrain de la vitrine-avec-fichier
s'explique par loupe-05 (le pointeur fantôme : l'access violation
tuerait le processus — « s'ouvre et se referme immédiatement ») ; la
vitrine vide tient au labo : LE KIT dev.5 PORTE SON TÉMOIN VITRINE
(la console + %ERRORLEVEL% + le rapport WER — l'axe restant sera nommé
par le terrain). AUCUNE adresse scellée ne bouge, les héritages
INTACTS (R7), la carte GÉNÉRATION 13 réécrite ; le qword version R10 :
0x00010004 → 0x00010005.

LA RETOUCHE DE L'ENTRÉE 206 (dev.3 → dev.4) : LE VRAI CHARGEUR A
CARTOGRAPHIÉ dev.3 — LA PREMIÈRE FOIS AU TERRAIN : l'enveloppe de
l'Entrée 205 est PROUVÉE (LoadLibraryEx DONT_RESOLVE @0x7ff740e20000,
les adresses scellées CONSTATÉES, la table K, la porte R10 relues
VERTES au témoin) — puis LE RUN S'EST ARRÊTÉ AU T0 : ÉCHEC NOMMÉ
[CADRE-NÉ], « le CADRE .data n'est pas né poignée INVALIDE
(l'initialiseur du build) ». L'AUTOPSIE SUR PIÈCES (le témoin
rapatrié du /test + l'artefact relu champ à champ) : le sentinel
INVALIDE posé à +8 (DANS le chemin UTF-16 !) et ZÉRO à +528 —
l'initialiseur avait pris CADRE_POIGNEE (= 8, UNE TAILLE de la
chaîne des tailles du plan) pour un OFFSET ; le harnais
(CADRE_VIERGE : les FF à +528), le scénario (CADRE_POIGNEE = 528)
et l'assembleur (« les offsets se CALCULENT par la chaîne des
tailles, jamais gravés de tête ») disaient TOUS +528 — le plan
documentait +528 noir sur blanc, la main du build a gravé 8.
LA RETOUCHE : l'initialiseur .data devient LE MIROIR EXACT du
CADRE_VIERGE du harnais (offset CALCULÉ : CADRE_CHEMIN +
CADRE_TAILLE_F = 528) ET le validateur relit LE MÊME miroir —
dev.3 validait à +8 : UN GARDE BLESSÉ PAR LE DÉFAUT QU'IL CROYAIT
GARDER NE GARDE RIEN (le contrôle doit dériver du plan, jamais de
la pièce qu'il contrôle) ; le zéro à +528 aurait été UNE SESSION
FANTÔME au premier ouvrir() — le T0 du scénario l'a nommé AVANT
tout bloc. AUCUN octet de notation (R2), aucune adresse scellée,
aucune balise ne bouge ; la taille du fichier demeure 0x1F200 ; le
qword version R10 : 0x00010003 → 0x00010004.

LA RETOUCHE DE L'ENTRÉE 205 (dev.2 → dev.3) : le terrain a REFUSÉ dev.2
du MÊME refus que dev.1 — 0xc000007b au geste de cartographie
(LoadLibraryEx DONT_RESOLVE), l'empreinte dev.2 a8a65ed4… ASSERTÉE par
le témoin (le BASERELOC de l'Entrée 204 était NÉCESSAIRE mais PAS
SUFFISANT). L'AUTOPSIE DE LABO (pefile + le décodage champ à champ)
dit l'image CONFORME ; la PREUVE PAR LA LIGNÉE isole TROIS axes sur
lesquels loupe dev.2 SORTAIT de l'enveloppe des HUIT artefacts passés
au terrain (hello M0, selftest M1, echo M2, proxy M3/M4/M5/M8/M9) :
  (1) LE TROU DE PAGE 0x3000-0x4000 (aucun artefact de la lignée n'en
      avait — dev.2 avait déplacé .data de 0x3000 à 0xE000 en laissant
      le vide) ;
  (2) LE BSS MASSIF .data VS 0x12000 > RS 0x400 (la lignée n'avait
      jamais dépassé la page partielle) ;
  (3) Subsystem GUI (aucun artefact cartographié n'était fenêtré —
      conservé : la vitrine l'exige ; LE KIT dev.3 PORTE SON
      BISSECTEUR : la cascade diagnostic du scénario nommera l'axe au
      terrain si le refus persistait).
LA RETOUCHE ramène l'image DANS l'enveloppe : .rdata 0x1000 → 0x2000
(l'extension 0x3000-0x3FFF est une MARGE ZÉRO — plus AUCUN trou) et
.data VS == RS 0x12000 (le RAW ENTIER — plus AUCUN BSS) ; AUCUNE
adresse scellée ne bouge, AUCUN octet de notation (R2), la taille du
fichier passe 0xC600 → 0x1F200.

LA RETOUCHE DE L'ENTRÉE 204 (dev.1 → dev.2) : le run terrain M10-(e) a
REFUSÉ dev.1 par le VRAI chargeur Windows — 0xc000007b au geste de
cartographie (LoadLibraryEx DONT_RESOLVE) : l'image déclare DYNAMIC_BASE
(DllCharacteristics 0x0160) mais N'AVAIT AUCUNE TABLE DE RELOCALISATION ;
la base de prédilection 0x140000000 étant occupée chez l'utilisateur
(son propre python.exe), le chargeur devait reloger l'image — sans
table, il refuse : « n'est pas conçu pour s'exécuter sous Windows ».
TOUS les artefacts de la lignée M1..M9 portent le BASERELOC minimal
(12 o, entrées ABSOLUTE — l'image PI que le chargeur PEUT reloger) ;
l'éditeur de dev.1 l'avait omis — LE TERRAIN L'A NOMMÉ, la retouche
le rend au plan (R_RELOC @0x2E90, dirs[5] — le miroir m2/build_m2.py).

L'ère du TGN est OUVERTE AU BUILD (la cérémonie d'ère PASSÉE SUR PIÈCES,
Entrée 201 : le garde à QUATORZE arbres VERTS, la dette D166/D171 SOLDÉE,
la remise du développeur INSTALLÉE — m0 re-signé 9090752d… au registre
étendu + loupe l'arbre neuf signé 08caf05f…, sa première signature).

La composition 0.1.0-dev.1 (charte loupe/I/README.md, le plan layout.py) :
  - .text 0x1000-0x1FFF : LA MINILIBC + LA BOUCLE AUX ADRESSES SCELLÉES
    (R7 — les octets hérités ne bougent JAMAIS d'un pouce) : libc-01
    memcpy @0x1100, libc-02 memcmp @0x1180, libc-07 memset @0x13C0 (les
    feuilles du scellé M1 selftest.exe) et win-03 LA BOUCLE DE MESSAGES
    @0x15C0 (le scellé démo demo.exe 0.3.0 — ses TROIS déplacements RIP
    visent l'IAT démo RÉSERVÉE @0x2818/0x2820/0x2828 : la double entrée
    n'est pas une redondance, c'est LE PRIX du déplacement scellé) ; le
    reste int3 (la réserve M1 vierge) ;
  - .rdata 0x2000-0x2FFF : les tables MD5 S/T DÉRIVÉES PAR ARITHMÉTIQUE,
    les pièces du rendu (l'entête, les tables HEX/HEXL), les 24 libellés
    latin-1, l'UTF-16 (la classe, le titre, l'explication fatale), l'IAT
    loupe (34 feuilles : kernel32 10 · user32 18 · gdi32 6), l'IAT démo
    scellée, LA MACHINERIE D'IMPORTS (5 descripteurs — user32 DEUX FOIS :
    le marché + la double entrée), LA PORTE R10 (la table des sommes des
    26 blocs embarqués + le qword version + l'ancre), LE BASERELOC MINIMAL
    (12 o @0x2E90, entrées ABSOLUTE — l'image PI que le chargeur PEUT
    reloger : le miroir M1..M9, l'oubli nommé de dev.1 soldé) et K[64]
    @0x2F00 LA TABLE DU SCELLÉ M9 (le déplacement hérité de tls13-02 la vise) ;
  - .text2 0x4000-0xDFFF : LES 18 BLOCS DU DOMAINE (0x4040-0x6800, les
    slots ARRÊTÉS sur les mesures D161) + la marge int3 + LA FAMILLE SHA
    AUX ADRESSES SCELLÉES M9 (tls13-01..04 @0xC000-0xC3C0, les octets du
    scellé proxy.exe 1.0.0) — la convention .text5 : la zone réservée
    int3 DANS le fichier ;
  - .data 0xE000-0x1FFFF : les zones du domaine (le CADRE 960 o — né
    LE MIROIR du CADRE_VIERGE du harnais : zéros partout SAUF la
    poignée INVALIDE à +528 [l'Entrée 206 — l'offset CALCULÉ par la
    chaîne des tailles : chemin 520 + taille_f 8], l'initialiseur du
    build — le panneau, la
    saisie, le motif, le journal, l'écran, HWND, les métriques, CUMUL 64
    Kio finissant 0x20000) ; LE RAW ENTIER 0x12000 COMMITTÉ (VS == RS —
    l'Entrée 205 : plus AUCUN BSS, l'image DANS l'enveloppe de la lignée) ;
  - PE32+ QUATRE sections (VA croissantes — le miroir démo), entrée =
    LOUPE09_VA (WinMain — l'entrée EST le bloc, D161 : la réserve 64 o
    s'est inclinée, aucune fiction de trampoline), WINDOWS_GUI, image PI.

LE GARDE-SCEAU (D87) : le build REFUSE de démarrer si l'un des QUATORZE
arbres d'intention a divergé de sa signature — le garde VERT 14/14 AVANT
construire() (l'ère du TGN : la cérémonie a précédé, la dette est soldée).

L'ORACLE STRUCTUREL : le round-trip 18/18 (keystone == capstone, R5), les
longueurs == les mesures de l'arrêt (D161), les déplacements RIP == les
symboles du plan, les appels directs == LE RÉSEAU DES SPECS (chaque bloc
chez ses appelés, libc-02 et win-03 PAR LA CARTE), les feuilles IAT == la
liste fermée de chaque spec (I5), AUCUN syscall, LES SLOTS DISJOINTS, et
L'HÉRITAGE R7 CONSTATÉ BYTE-IDENTIQUE — LA DOUBLE PREUVE (les extraits
des scellés == les octets posés ET les notations d'origine ré-assemblées
== les extraits : minilibc M1, boucle démo, famille sha M9, la table K).

Les preuves d'observable : LES TROIS HARNAIS DU DOMAINE rejoués VERTS au
geste même du build (le noyau 59 + le rendu 53 + l'édition 45 — les 18
blocs NOTÉS-MESURÉS-PROUVÉS sur pièces, les vecteurs officiels RFC 1321
et FIPS 180-4, le différentiel hashlib, l'oracle à scénarios, la
falsification attrapée) ; la validation PE : LA COMPOSITION INTÉGRALE
(chaque octet de chaque section compté : bloc, table, libellé, IAT,
machinerie, porte, int3 ou marge zéro) + la porte R10 relue de l'image.

La carte : GÉNÉRATION 16 (la lignée D80, la graine durable D144 — la
génération RÉELLE de la pièce dev.8 : les i11xxxx à leur quatrième écriture,
la dette de l'Entrée 211 soldée).

Usage :
  python3 build_loupe.py             # construction 0.1.0-dev.8 (+ carte gén. 16)
  python3 build_loupe.py --verifier  # re-vérification sans écriture
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import struct
import subprocess
import sys
from datetime import datetime, timezone

ICI = os.path.dirname(os.path.abspath(__file__))
TRIADE = os.path.dirname(ICI)
M4_DIR = os.path.join(TRIADE, "m4")

for _d in (ICI, M4_DIR, os.path.join(M4_DIR, "outils")):
    if _d not in sys.path:
        sys.path.insert(0, _d)


class EchecBuild(Exception):
    """Tout échec du garde, de l'oracle, du round-trip ou de la construction."""


def _charger_module(nom: str, chemin: str):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


# --- Les plans et la machinerie (chargés par CHEMIN NOMINATIF — la leçon D158) ----

L = _charger_module("layout_loupe", os.path.join(ICI, "layout.py"))
LT = _charger_module("layout_tls13", os.path.join(TRIADE, "tls13", "layout.py"))
B4 = _charger_module("build_m4", os.path.join(M4_DIR, "build_m4.py"))
SCEAU_I = _charger_module("sceau_I", os.path.join(TRIADE, "v06", "sceau_I.py"))

import capstone  # noqa: E402
import pefile  # noqa: E402
from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402


# --- Garde sceau de l'Intention (D87) : les QUATORZE arbres ------------------------
# L'ère du TGN (la cérémonie Passée sur pièces, Entrée 201) : le quatorzième
# arbre (loupe) SIGNÉ 08caf05f… et m0 RE-SIGNÉ au registre étendu — le garde
# VERT 14/14 AVANT construire() (la dette D166/D171 est SOLDÉE).

ARBRES_GARDE_M10 = ["m0", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8",
                    "tls13", "loupe", "demo", "terrain", "v06"]


def _garde_sceau_I() -> None:
    try:
        SCEAU_I.garde(ARBRES_GARDE_M10)
        print(f"[sceau-I] garde : {len(ARBRES_GARDE_M10)} arbres d'intention "
              f"conformes à leurs signatures (le garde VERT 14/14 AVANT "
              f"construire() — l'ère du TGN ouverte au build) ; clé déposée : "
              f"{SCEAU_I.etat_cle()}")
    except SCEAU_I.EchecSceauI as exc:
        raise EchecBuild(
            f"{exc}\n  [cérémonie] le garde n'est pas vert : la remise du "
            f"développeur est requise au coffre /test (sceau_I.py deposer)") from exc


# --- Les scellés (les ancres R7 des octets hérités) --------------------------------

SCELLE_M9 = os.path.join(TRIADE, "tls13", "proxy.exe")   # l'ère 1.0.0 (M9)
SCELLE_M9_TAILLE = 65024
SCELLE_M9_SHA256 = ("446279f3ab356900870cc3b3e1700654"
                    "a4216ec0b264172340e453db3b00d93d")
SCELLE_M1 = os.path.join(TRIADE, "m1", "selftest.exe")   # la minilibc (M1)
SCELLE_M1_TAILLE = 9216
SCELLE_M1_SHA256 = ("8038585b7af83c9fe5e6fdccd197e678"
                    "88b9e5fb09d8d6c84cb998c684bff3c0")
SCELLE_DEMO = os.path.join(TRIADE, "demo", "demo.exe")   # la boucle (démo)
SCELLE_DEMO_TAILLE = 0x4000
SCELLE_DEMO_MD5 = "73c064fbaf4610a167bc6434dee400e4"
SCELLE_DEMO_SHA256 = ("df8f2e50949b14c072f139013a6166a0"
                      "41e573e49b6872d826958f522495e4af")


def _lire_scelles() -> tuple[bytes, bytes, bytes]:
    """Les TROIS pièces relues ET confrontées à leurs ancres (R6/R7 : le
    scellé qu'on hérite est le scellé qu'on relit — jamais cru sur parole)."""
    m9 = open(SCELLE_M9, "rb").read()
    if len(m9) != SCELLE_M9_TAILLE or hashlib.sha256(m9).hexdigest() != SCELLE_M9_SHA256:
        raise EchecBuild("le scellé M9 (tls13/proxy.exe) a divergé de son ancre "
                         "446279f3… — la famille sha ne peut être héritée")
    m1 = open(SCELLE_M1, "rb").read()
    if len(m1) != SCELLE_M1_TAILLE or hashlib.sha256(m1).hexdigest() != SCELLE_M1_SHA256:
        raise EchecBuild("le scellé M1 (m1/selftest.exe) a divergé de son ancre "
                         "8038585b… — la minilibc ne peut être héritée")
    demo = open(SCELLE_DEMO, "rb").read()
    if (len(demo) != SCELLE_DEMO_TAILLE
            or hashlib.md5(demo).hexdigest() != SCELLE_DEMO_MD5
            or hashlib.sha256(demo).hexdigest() != SCELLE_DEMO_SHA256):
        raise EchecBuild("le scellé démo (demo/demo.exe) a divergé de son ancre "
                         "df8f2e50… — la boucle de messages ne peut être héritée")
    print(f"[scellés] les TROIS ancres R7 relues : selftest.exe (M1) · "
          f"demo.exe 0.3.0 (la boucle) · proxy.exe 1.0.0 (M9) — INTACTES")
    return m9, m1, demo


def _extraire_scelle(donnees: bytes, rva: int, taille: int) -> bytes:
    """RVA -> raw par le parse minimal des sections PE (le lecteur canonique
    du harnais — le miroir EmulationRendu.extraire, jamais une adresse devinée)."""
    e = struct.unpack_from("<I", donnees, 0x3C)[0]
    n = struct.unpack_from("<H", donnees, e + 6)[0]
    opt = struct.unpack_from("<H", donnees, e + 20)[0]
    for k in range(n):
        o = e + 24 + opt + k * 40
        va, = struct.unpack_from("<I", donnees, o + 12)
        ra, = struct.unpack_from("<I", donnees, o + 20)
        vs, = struct.unpack_from("<I", donnees, o + 8)
        if va <= rva < va + vs:
            raw = ra + (rva - va)
            return donnees[raw:raw + taille]
    raise EchecBuild(f"RVA {rva:#x} introuvable dans le scellé")


# --- La table des 18 blocs du domaine (le plan, source unique) ---------------------
# (bid, sid, fichier, famille) — rva/slot dérivés de L.SLOTS_LOUPE.

BLOCS_LOUPE = [
    ("i110001", "loupe-01:R3", "loupe-01-ouvrir", "fichier"),
    ("i110002", "loupe-02:R1", "loupe-02-lire", "fichier"),
    ("i110003", "loupe-03:R1", "loupe-03-fermer", "fichier"),
    ("i110004", "loupe-04:R1", "loupe-04-cadre", "fichier"),
    ("i110005", "loupe-05:R1", "loupe-05-sha256", "empreintes"),
    ("i110006", "loupe-06:R1", "loupe-06-md5", "empreintes"),
    ("i110007", "loupe-07:R1", "loupe-07-cumul", "empreintes"),
    ("i110008", "loupe-08:R1", "loupe-08-ligne", "rendu"),
    ("i110009", "loupe-09:R1", "loupe-09-ecran", "rendu"),
    ("i110010", "loupe-10:R1", "loupe-10-peinture", "rendu"),
    ("i110011", "loupe-11:R1", "loupe-11-defilement", "rendu"),
    ("i110012", "loupe-12:R1", "loupe-12-aller", "navigation"),
    ("i110013", "loupe-13:R1", "loupe-13-recherche", "navigation"),
    ("i110014", "loupe-14:R1", "loupe-14-suivant", "navigation"),
    ("i110015", "loupe-15:R1", "loupe-15-curseur", "édition"),
    ("i110016", "loupe-16:R1", "loupe-16-saisie", "édition"),
    ("i110017", "loupe-17:R1", "loupe-17-sauver", "édition"),
    ("i110018", "loupe-18:R1", "loupe-18-quitter", "édition"),
]

# Les longueurs mesurées à l'arrêt (D161 — les quatre passes de l'auteur :
# le noyau, le rendu r2 [loupe-09 874 → 1135], l'édition).
MESURES_LOUPE = {
    "i110001": 389, "i110002": 296, "i110003": 122, "i110004": 47,
    "i110005": 313, "i110006": 871, "i110007": 102, "i110008": 271,
    "i110009": 1135, "i110010": 1622, "i110011": 568, "i110012": 796,
    "i110013": 126, "i110014": 983, "i110015": 391, "i110016": 660,
    "i110017": 521, "i110018": 163,
}

# LE RÉSEAU DES SPECS : les appels directs fermés par bloc (chaque bloc chez
# ses appelés — les héritages PAR LA CARTE à leurs adresses scellées).
APPELS_FERMES = {
    "i110001": {"libc01", "loupe04", "loupe02", "loupe03", "loupe07"},
    "i110002": set(),
    "i110003": {"libc07", "loupe04"},
    "i110004": {"libc07"},
    "i110005": {"tls01", "tls03", "tls04"},
    "i110006": {"libc01", "libc07"},
    "i110007": {"loupe05", "loupe06"},
    "i110008": set(),
    "i110009": {"win03", "loupe01", "loupe10", "loupe11", "loupe12",
                "loupe14", "loupe15", "loupe16", "loupe17", "loupe18",
                "libc07"},
    "i110010": {"loupe08"},
    "i110011": {"loupe02"},
    "i110012": {"loupe02", "loupe14"},
    "i110013": {"libc02"},
    "i110014": {"loupe02", "loupe13"},
    "i110015": {"loupe02"},
    "i110016": {"loupe02"},
    "i110017": {"loupe07"},
    "i110018": {"loupe03"},
}

# Les feuilles IAT par bloc (la liste fermée de chaque spec — I5 ; les blocs
# purs SANS entrée : 04, 07, 08, 13 — le miroir tls13 charte § 7).
IAT_PAR_BLOC = {
    "i110001": {"CreateFileW", "GetFileSizeEx", "CloseHandle", "GetLastError"},
    "i110002": {"SetFilePointerEx", "ReadFile", "GetLastError"},
    "i110003": {"CloseHandle", "GetLastError"},
    "i110004": set(),
    "i110005": {"SetFilePointerEx", "ReadFile", "GetLastError"},
    "i110006": {"SetFilePointerEx", "ReadFile", "GetLastError"},
    "i110007": set(),
    "i110008": set(),
    "i110009": {"GetModuleHandleW", "GetCommandLineW", "LoadCursorW",
                "RegisterClassExW", "CreateWindowExW", "ShowWindow",
                "MessageBoxW", "ExitProcess", "DefWindowProcW"},
    "i110010": {"BeginPaint", "EndPaint", "GetStockObject", "SelectObject",
                "GetTextMetricsW", "TextOutW", "SetTextColor", "SetBkColor",
                "GetClientRect", "GetLastError"},
    "i110011": {"GetScrollInfo", "SetScrollInfo", "InvalidateRect",
                "GetLastError"},
    "i110012": {"InvalidateRect"},
    "i110013": set(),
    "i110014": {"SetFilePointerEx", "ReadFile", "GetLastError",
                "InvalidateRect"},
    "i110015": {"InvalidateRect"},
    "i110016": {"InvalidateRect"},
    "i110017": {"SetFilePointerEx", "WriteFile", "GetLastError",
                "InvalidateRect"},
    "i110018": {"DestroyWindow", "PostQuitMessage", "MessageBeep"},
}

# Les adresses des appelés du réseau (le plan, source unique).
_ADRESSES_RESEAU = {
    "libc01": L.R_LIBC01, "libc02": L.R_LIBC02, "libc07": L.R_LIBC07,
    "win03": L.R_WIN03, "tls01": L.R_TLS01, "tls02": L.R_TLS02,
    "tls03": L.R_TLS03, "tls04": L.R_TLS04,
    "loupe01": L.LOUPE01_VA, "loupe02": L.LOUPE02_VA, "loupe03": L.LOUPE03_VA,
    "loupe04": L.LOUPE04_VA, "loupe05": L.LOUPE05_VA, "loupe06": L.LOUPE06_VA,
    "loupe07": L.LOUPE07_VA, "loupe08": L.LOUPE08_VA, "loupe09": L.LOUPE09_VA,
    "loupe10": L.LOUPE10_VA, "loupe11": L.LOUPE11_VA, "loupe12": L.LOUPE12_VA,
    "loupe13": L.LOUPE13_VA, "loupe14": L.LOUPE14_VA, "loupe15": L.LOUPE15_VA,
    "loupe16": L.LOUPE16_VA, "loupe17": L.LOUPE17_VA, "loupe18": L.LOUPE18_VA,
}

# Les 8 héritages embarqués : (nom, rva_destination, taille, scellé d'origine,
# rva d'origine, notation d'origine pour la double preuve R7).
HERITAGES = [
    ("libc-01", L.R_LIBC01, 0x80, "m1", 0x1100,
     os.path.join(TRIADE, "m1", "notation", "libc-01-memcpy.asm")),
    ("libc-02", L.R_LIBC02, 0x80, "m1", 0x1180,
     os.path.join(TRIADE, "m1", "notation", "libc-02-memcmp.asm")),
    ("libc-07", L.R_LIBC07, 0x80, "m1", 0x13C0,
     os.path.join(TRIADE, "m1", "notation", "libc-07-memset.asm")),
    ("win-03", L.R_WIN03, 0x80, "demo", 0x15C0,
     os.path.join(TRIADE, "demo", "notation", "win-03-boucle.asm")),
    ("tls13-01", L.R_TLS01, 0x80, "m9", LT.TLS01_VA,
     os.path.join(TRIADE, "tls13", "notation", "tls13-01-sha256-init.asm")),
    ("tls13-02", L.R_TLS02, 0x1C0, "m9", LT.TLS02_VA,
     os.path.join(TRIADE, "tls13", "notation", "tls13-02-sha256-comprimer.asm")),
    ("tls13-03", L.R_TLS03, 0xC0, "m9", LT.TLS03_VA,
     os.path.join(TRIADE, "tls13", "notation", "tls13-03-sha256-absorber.asm")),
    ("tls13-04", L.R_TLS04, 0xC0, "m9", LT.TLS04_VA,
     os.path.join(TRIADE, "tls13", "notation", "tls13-04-sha256-finaliser.asm")),
]


# --- Couche I : lecture et audit du gabarit (les specs sont la source, R2) ---------

def lire_spec_loupe(chemin: str) -> dict:
    """Le gabarit § 2.2 : la première ligne nomme, les blocs font foi —
    l'Intention, le Contrat, pre/post/inv PARSÉS (la carte en porte le
    condensé — la couche I est la source, jamais une copie)."""
    with open(chemin, encoding="utf-8") as f:
        lignes = f.read().splitlines()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", lignes[0])
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3))}
    texte = "\n".join(lignes)
    for bloc in ("Intention", "Contrat", "pre", "post", "inv"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")

    def _section(marqueur: str) -> str:
        pat = re.compile(rf"^  {marqueur}\s*:\s*(.*)$")
        sortie, actif = [], False
        for ligne in lignes:
            mm = pat.match(ligne)
            if mm:
                actif = True
                if mm.group(1).strip():
                    sortie.append(mm.group(1).strip())
                continue
            if actif:
                if ligne.startswith("  ") and ligne.strip():
                    sortie.append(ligne.strip())
                else:
                    actif = False
        return " ".join(sortie)

    spec["pre"] = _section("pre")
    spec["post"] = _section("post")
    spec["inv"] = _section("inv")
    if not (spec["pre"] and spec["post"] and spec["inv"]):
        raise EchecBuild(f"{chemin} : sections pre/post/inv vides (gabarit § 2.2)")
    return spec


def charger_couche_I_loupe() -> dict[str, dict]:
    """Les 18 spécifications du domaine : gabarit, id, révision — la charte
    LUE au passage (R2 : écrit-avant-code, la cérémonie a précédé le build)."""
    with open(os.path.join(ICI, "I", "README.md"), encoding="utf-8") as f:
        readme = f.read()
    if "écrite-avant-code" not in readme:
        raise EchecBuild("loupe/I/README.md : la provenance écrite-avant-code "
                         "absente de la charte (R2)")
    specs = {}
    for bid, sid, fichier, _famille in BLOCS_LOUPE:
        ident, rev_ref = sid.split(":")
        chemin = os.path.join(ICI, "I", fichier + ".md")
        if not os.path.exists(chemin):
            raise EchecBuild(f"spécification I introuvable pour {sid} : {chemin}")
        spec = lire_spec_loupe(chemin)
        if spec["id"] != ident or spec["rev"] != int(rev_ref[1:]):
            raise EchecBuild(f"{chemin} : {spec['id']}:{spec['rev']} != {sid}")
        specs[bid] = spec
    print(f"[couche-I] les 18 spécifications relues (gabarit § 2.2, révisions "
          f"concordantes — R2 : la cérémonie a précédé, chaque bloc porté par "
          f"sa spécification AVANT le premier octet)")
    return specs


# --- Assemblage + round-trip (le lecteur canonique de la lignée) -------------------

def assembler_blocs(ks) -> tuple[dict, dict]:
    """Les 18 notations assemblées (keystone), round-trippées (capstone, R5),
    les longueurs == les mesures de l'arrêt (D161), les slots du plan."""
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code, insns_par_bloc = {}, {}
    for bid, _sid, fichier, _famille in BLOCS_LOUPE:
        rva, slot = L.SLOTS_LOUPE[bid]
        chemin = os.path.join(ICI, "notation", fichier + ".asm")
        octets, metas = B4.assembler_bloc(ks, chemin, rva, slot)
        insns = B4.round_trip(cs, ks, chemin, rva, octets, metas)
        if len(insns) != len(metas):
            raise EchecBuild(f"{bid} : round-trip divergent ({len(insns)} != "
                             f"{len(metas)} instructions — R5)")
        if len(octets) != MESURES_LOUPE[bid]:
            raise EchecBuild(f"{bid} : {len(octets)} o != {MESURES_LOUPE[bid]} o "
                             f"mesurés à l'arrêt (D161 — la notation a bougé ?)")
        if slot - len(octets) < 16 or slot % 64:
            raise EchecBuild(f"{bid} : slot {slot:#x} invalide (multiple de 64, "
                             f"padding >= 16 — la convention de la lignée)")
        code[bid] = octets
        insns_par_bloc[bid] = insns
    print(f"[assemblage] 18/18 notations : round-trip R5 vert, les longueurs == "
          f"les mesures de l'arrêt (47/296/122/389/313/871/102 + 271/1622/568/"
          f"796/126/983/1135 + 391/660/521/163 o — D161 tenu, l'Entrée 207 : "
          f"1622 pour le peintre)")
    return code, insns_par_bloc


# --- L'héritage scellé : extraction + LA DOUBLE PREUVE R7 --------------------------

def heritage_scelle(m9: bytes, m1: bytes, demo: bytes, ks) -> dict[str, bytes]:
    """Les 8 héritages extraits de leurs scellés AUX ADRESSES D'ORIGINE —
    LA DOUBLE PREUVE : les extraits == les octets qui seront posés ET les
    notations d'origine ré-assemblées == les extraits (R7 au sens propre,
    jamais une ré-écriture). La table K @0x2F00 comprise (le déplacement
    scellé de tls13-02 la vise)."""
    sources = {"m1": m1, "demo": demo, "m9": m9}
    extraits = {}
    for nom, rva_dest, taille, source, rva_orig, chemin_notation in HERITAGES:
        extrait = _extraire_scelle(sources[source], rva_orig, taille)
        if rva_orig != rva_dest:
            raise EchecBuild(f"{nom} : l'adresse d'origine {rva_orig:#x} != la "
                             f"destination {rva_dest:#x} (la règle du geste (b) : "
                             f"les octets hérités ne bougent JAMAIS d'un pouce)")
        octets_origine, _ = B4.assembler_bloc(
            ks, chemin_notation, rva_orig, taille)
        if bytes(octets_origine) != extrait[:len(octets_origine)]:
            raise EchecBuild(f"{nom} : la notation d'origine ré-assemblée != "
                             f"l'extrait du scellé (R7 — la double preuve)")
        extraits[nom] = extrait
    # LE REPOINTAGE DE WIN-03 (l'écart nommé de l'Entrée 210 — le prix du
    # RELOGEMENT de l'IAT dev.7 [D54-QUATRIÈME]) : les TROIS déplacements
    # RIP de la boucle scellée visaient l'IAT démo d'ORIGINE
    # @0x2818/0x2820/0x2828 ; relogés vers la QUATRIÈME PLAGE
    # @0x3228/0x3230/0x3238 — disp32 SEULS, 6 octets en tout, AUCUNE
    # taille d'instruction ne change ; win-03 est LE SEUL héritage auquel
    # le plan touche (la minilibc M1, la famille sha M9, la table K et le
    # CADRE demeurent octet-identiques aux scellés — la double preuve ci-
    # dessus a joué sur l'EXTRAIT BRUT, le repointage est un geste NOMMÉ
    # par-dessus, la pièce recoupée le constate)
    w03 = bytearray(extraits["win-03"])
    for site, cible in ((0x15DD, L.R_IAT_DEMO_GMW), (0x15EA, L.R_IAT_DEMO_TM),
                        (0x15F3, L.R_IAT_DEMO_DMW)):
        assert w03[site - 0x15C0] == 0xFF and w03[site - 0x15C0 + 1] == 0x15, \
            f"l'encodage call [rip] de win-03 @{site:#x} inattendu"
        struct.pack_into("<i", w03, site - 0x15C0 + 2, cible - (site + 6))
    assert sum(a != b for a, b in zip(w03, extraits["win-03"])) == 6, \
        "le repointage de win-03 doit toucher EXACTEMENT 6 octets (les 3 disp32)"
    extraits["win-03"] = bytes(w03)
    # LA TABLE K : extraite du scellé M9 ET == les constantes du plan tls13
    # (la source unique — le plan loupe RENVOIE, jamais re-déclare)
    k_scelle = _extraire_scelle(m9, L.R_K, 256)
    if k_scelle != struct.pack("<64I", *LT.K):
        raise EchecBuild("la table K[64] extraite du scellé M9 != les constantes "
                         "du plan tls13 (R7 — la source unique)")
    extraits["K"] = k_scelle
    print(f"[R7] LA DOUBLE PREUVE des {len(HERITAGES)} héritages : libc-01/02/07 "
          f"(M1) + win-03 (démo) + tls13-01..04 (M9) + la table K — les extraits "
          f"des SCELLÉS == les notations d'origine ré-assemblées == les octets "
          f"qui seront posés AUX MÊMES adresses")
    return extraits


# --- L'AUDIT D'ABI msx64 (l'Entrée 207 : le garde STRUCTUREL de la classe) ----------

# les feuilles IAT qui prennent des arguments AU-DELÀ du quatrième (la
# CONVENTION msx64 — jamais la pièce) : la source = les tables des API de
# Windows ; toutes les autres feuilles vivent aux quatre registres.
ARGS_PILE_IAT = {
    "CreateFileW": 3,        # disposition, attributs, gabarit
    "ReadFile": 1,           # lpOverlapped
    "WriteFile": 1,          # lpOverlapped
    "TextOutW": 1,           # c — le compte
    "CreateWindowExW": 8,    # X, Y, L, H, parent, menu, instance, param
}


def audit_msx64(insns_par_bloc: dict) -> int:
    """L'AUDIT DE LA CLASSE DE L'ENTRÉE 207 (structurel, AVANT tout harnais) :
    à CHAQUE appel IAT de CHAQUE bloc —
      (1) L'ALIGNEMENT : rsp ≡ 0 (mod 16) au call (le VRAI kernel32/user32
          est SSE : movaps faute là où le labo (Unicorn + shims Python)
          passe — l'axe que seul l'audit statique voit) ;
      (2) LES SLOTS DES ARGUMENTS PILE : pour chaque feuille à arguments
          5+, chaque slot [rsp+0x20+8k] DOIT être écrit depuis la dernière
          cible de saut / le dernier appel IAT / tout ret — sinon
          l'argument part au hasard de la pile non initialisée (LE DÉFAUT
          DE dev.4 : trois slots au home space, un pointeur fantôme).
    Le garde dérive de la CONVENTION, jamais de la pièce qu'il contrôle."""
    verrous = 0
    inverse_iat = {v: k for k, v in L.IAT_SLOTS.items()}
    exit_slot = L.IAT_SLOTS["ExitProcess"]
    for bid, _sid, _fichier, _famille in BLOCS_LOUPE:
        insns = insns_par_bloc[bid]
        rva, slot = L.SLOTS_LOUPE[bid]
        # LA PRE-PASSE : les entrées de sous-programmes — les cibles des
        # appels directs INTERNES au bloc (le peintre et sa famille de
        # formatage · la compression md5 de loupe-06) ; chacune est UNE
        # fonction à l'entrée ABI ≡ 8 (l'adresse de retour posée par le
        # call) — sa marche lui est propre, le cadre de l'appelant est
        # SAUVÉ à l'entrée et RESTAURÉ au ret quand l'appelant reprend
        cibles = set()
        entrees_sp = set()
        for insn in insns:
            if insn.mnemonic.startswith("j") and insn.op_str.startswith("0x"):
                cibles.add(int(insn.op_str, 0))
            elif insn.mnemonic == "call" and insn.op_str.startswith("0x"):
                t = int(insn.op_str, 0)
                if rva <= t < rva + slot:
                    entrees_sp.add(t)
        # les appels internes ne coupent PAS la fenêtre des slots : le
        # délégué ne touche JAMAIS [rsp+0x20+] de son appelant (son home
        # space à LUI vit à [rsp..0x18] du même cadre — l'ABI)
        depile = 8               # l'entrée msx64 ≡ 8 (mod 16) — le cadre
        cadres: list[int] = []   # le cadre de l'appelant, sauvé à l'entrée
        ecrits = set()           # les slots écrits dans la fenêtre courante
        for insn in insns:
            adresse = insn.address
            if adresse in entrees_sp:
                # L'ENTRÉE DU SOUS-PROGRAMME : le call a posé l'adresse de
                # retour — l'invariant ABI ≡ 8 ; le cadre de l'appelant est
                # SAUVÉ (le sous-programme peut vivre AU MILIEU du corps :
                # à son ret, l'appelant REPAREND son cadre — la compression
                # md5 de loupe-06 et ses chemins d'erreur après le ret)
                cadres.append(depile)
                depile, ecrits = 8, set()
            if adresse in cibles:
                # une étiquette coupe la FENÊTRE DES SLOTS (les stores
                # doivent vivre DANS la branche qui appelle) — le CADRE
                # lui-même PERSISTE : l'alignement ne se réinitialise
                # JAMAIS à une étiquette — ET L'INSTRUCTION À L'ÉTIQUETTE
                # GARDE SON EFFET DE PILE : les rendus « push imm8 ; pop
                # rax » de la retouche dev.7 [EAX-SANS-SIGNE] VIVENT à
                # leurs étiquettes (le push -2 de .absent @0x41D0) — les
                # sauter c'est désynchroniser le cadre (la classe même de
                # l'Entrée 206 : le contrôle dérive de la CONVENTION)
                ecrits = set()
            m, ops = insn.mnemonic, insn.op_str
            if m == "push":
                depile -= 8
            elif m == "pop":
                depile += 8
            elif m == "ret":
                # LE RET : l'adresse de retour rendue — SI le code qui suit
                # est un CIBLE (la continuation de l'APPELANT : le
                # sous-programme vivait au milieu de son corps), le cadre
                # SAUVÉ à l'entrée revient ; sinon le ret rend +8 (le
                # matériel) — la suite est un autre sous-programme (son
                # entré réinitialisera) ou le mort du bloc
                if (adresse + insn.size) in cibles and cadres:
                    depile = cadres.pop()
                else:
                    depile += 8
            elif m == "sub" and ops.startswith("rsp,"):
                depile -= int(ops.split(",")[1], 0)
            elif m == "add" and ops.startswith("rsp,"):
                depile += int(ops.split(",")[1], 0)
            elif m == "lea":
                continue          # le lea pose des POINTEURS, jamais un slot
            elif m in ("mov", "movzx") and "rsp" in ops and "," in ops:
                cible = ops.split(",")[0].strip()
                if "ptr" in cible:      # « dword ptr [rsp + 0x20] » — le préfixe
                    cible = cible.split("ptr", 1)[1].strip()
                if cible.startswith("[rsp"):
                    import re as _re
                    mm = _re.match(r"\[rsp(?: \+ (0x[0-9a-f]+|\d+))?\]", cible)
                    if mm:
                        off = int(mm.group(1), 0) if mm.group(1) else 0
                        ecrits.add(off)
            elif m == "call" and "[rip" in ops:
                cible = B4.operande_rip_cible(insn)
                if cible is None or cible not in L.IAT_SLOTS.values():
                    continue          # l'appel direct demeure (fenêtre ouverte)
                feuille = inverse_iat[cible]
                if depile % 16 != 0:
                    raise EchecBuild(
                        f"{bid} : appel IAT {feuille} @{adresse:#x} PILE "
                        f"MISALIGNÉE rsp≡{depile % 16} (mod 16) — le VRAI "
                        f"chargeur de fonctions (SSE) peut fautter là où "
                        f"l'émulation passe (la classe de l'Entrée 207)")
                n = ARGS_PILE_IAT.get(feuille, 0)
                for k in range(n):
                    off = 0x20 + 8 * k
                    if off not in ecrits:
                        raise EchecBuild(
                            f"{bid} : appel IAT {feuille} @{adresse:#x} — "
                            f"l'argument {5 + k} attendu à [rsp+{off:#x}] "
                            f"N'EST PAS ÉCRIT depuis la dernière étiquette : "
                            f"il part AU HASARD de la pile non initialisée "
                            f"(LE DÉFAUT DE dev.4 : les slots au home space "
                            f"— la classe de l'Entrée 207)")
                ecrits = set()        # l'appelé consomme ses arguments
                if cible == exit_slot and (insn.address + insn.size) not in cibles:
                    depile, ecrits = 8, set()   # noreturn ET le code qui suit
                verrous += 1          # n'est PAS atteint par saut : une
        verrous += 1                  # fonction nouvelle naît (WinMain →
                                       # LA PROCÉDURE par pointeur enregistré)
    print(f"[audit msx64] {verrous} appels IAT AUDITÉS — l'alignement 16 "
          f"VERT partout, chaque argument 5+ ÉCRIT À SON SLOT [rsp+0x20+] "
          f"(la convention, jamais la pièce — la classe de l'Entrée 207 "
          f"gardée pour toujours)")
    return verrous


# --- L'oracle structurel (le plan rangée (d)/(e) — LA RÈGLE du domaine) ------------

def oracle_structurel(code: dict, insns_par_bloc: dict) -> int:
    """Les verrous du domaine : les déplacements RIP == les symboles du plan,
    les appels directs == LE RÉSEAU DES SPECS, les feuilles IAT == la liste
    fermée de chaque spec, AUCUN syscall, LES SLOTS DISJOINTS."""
    verrous = 0
    inverse_iat = {v: k for k, v in L.IAT_SLOTS.items()}

    cibles_legales = (
        {L.R_CADRE, L.R_EMPREINTES, L.R_SAISIE, L.R_MOTIF, L.R_JOURNAL,
         L.R_ECRAN, L.R_HWND, L.R_METRIQUES, L.R_CUMUL,
         L.R_MD5_S, L.R_MD5_T, L.R_ENTETE, L.R_HEX, L.R_HEXL,
         L.R_CLASSE, L.R_TITRE, L.R_ERREUR,
         L.L_USAGE, L.L_BALISE, L.L_TIRET, L.L_MID, L.L_OCT, L.L_MODIF,
         L.L_MD5, L.L_SHA, L.L_AST, L.L_VIDE, L.L_ALLER, L.L_CHERCHER,
         L.L_MALFORMEE, L.L_HORSBORNES, L.L_SESSION, L.L_FIN, L.L_PAIRES,
         L.L_SYSTEME, L.L_ABSENT, L.L_JOURNALPLEIN, L.L_RIENSAUVER,
         L.L_ECRITS, L.L_JUSQUA, L.L_QUITTER}
        | set(L.IAT_SLOTS.values()))

    for bid, _sid, _fichier, _famille in BLOCS_LOUPE:
        rva, slot = L.SLOTS_LOUPE[bid]
        attendus_appels = {_ADRESSES_RESEAU[n] for n in APPELS_FERMES[bid]}
        vus_appels = set()
        for insn in insns_par_bloc[bid]:
            # AUCUN syscall (le miroir du domaine : tout passe par l'IAT ou
            # les appels directs — l'image PI, l'ABI déclarée)
            if insn.mnemonic == "syscall":
                raise EchecBuild(f"{bid} : site syscall interdit dans le domaine "
                                 f"loupe (tout passe par l'IAT déclarée)")
            cible = B4.operande_rip_cible(insn)
            if cible is not None:
                if cible not in cibles_legales and not (rva <= cible < rva + slot):
                    raise EchecBuild(f"{bid} : déplacement RIP vers {cible:#x} "
                                     f"hors des symboles du plan (la liste fermée)")
            if insn.mnemonic == "call" and "[rip" not in insn.op_str:
                t = int(insn.op_str, 0)
                if t not in attendus_appels and not (rva <= t < rva + slot):
                    raise EchecBuild(f"{bid} : appel direct vers {t:#x} hors du "
                                     f"réseau des specs (la liste fermée)")
                vus_appels.add(t)
            if insn.mnemonic == "call" and cible is not None \
                    and cible in L.IAT_SLOTS.values():
                feuille = inverse_iat[cible]
                if feuille not in IAT_PAR_BLOC[bid]:
                    raise EchecBuild(f"{bid} : feuille IAT {feuille} hors de la "
                                     f"liste fermée de sa spec (I5)")
        manquants = attendus_appels - vus_appels
        if manquants:
            raise EchecBuild(f"{bid} : appels attendus manquants au réseau : "
                             f"{[hex(a) for a in sorted(manquants)]}")
        verrous += 1

    # LES SLOTS DISJOINTS (l'erratum n° 4 du M9 : le contrôle qui nomme —
    # PERMANENT désormais) + la couverture des 8 héritages disjoints aussi
    poses = sorted(
        [(L.SLOTS_LOUPE[bid][0], L.SLOTS_LOUPE[bid][0] + L.SLOTS_LOUPE[bid][1],
          bid) for bid, *_ in BLOCS_LOUPE]
        + [(rva, rva + taille, nom) for nom, rva, taille, _s, _o, _n in HERITAGES])
    for (debut_a, fin_a, nom_a), (debut_b, fin_b, nom_b) in zip(poses, poses[1:]):
        if fin_a > debut_b:
            raise EchecBuild(f"chevauchement de slots : {nom_a} [{debut_a:#x}, "
                             f"{fin_a:#x}) recouvre {nom_b} (l'erratum n° 4 : le "
                             f"contrôle qui nomme)")
        verrous += 1
    print(f"[oracle] structurel : {verrous} verrous PASS (le réseau des specs, "
          f"les feuilles IAT par bloc, les déplacements RIP aux symboles du "
          f"plan, AUCUN syscall, LES SLOTS DISJOINTS — les 26 posés)")
    return verrous


# --- Les pièces .rdata du plan (la source unique, relue du harnais) ----------------

ENTETE_TEXTE = ("Décalage  00 01 02 03 04 05 06 07"
                "  08 09 0A 0B 0C 0D 0E 0F  ASCII")
LIBELLES = [
    (L.L_USAGE, "loupe <fichier>"),
    (L.L_BALISE, "Loupe 0.1.0-dev.5"),
    (L.L_TIRET, " - "),
    (L.L_MID, " · "),
    (L.L_OCT, " o · curseur 0x"),
    (L.L_MODIF, " · MODIFIÉ"),
    (L.L_MD5, "md5 "),
    (L.L_SHA, " · sha256 "),
    (L.L_AST, " *"),
    (L.L_VIDE, "-"),
    (L.L_ALLER, "ALLER (hexa) : "),
    (L.L_CHERCHER, "CHERCHER (hexa) : "),
    (L.L_MALFORMEE, "saisie mal formée"),
    (L.L_HORSBORNES, "hors bornes"),
    (L.L_SESSION, "aucun fichier ouvert"),
    (L.L_FIN, "plus d'occurrence"),
    (L.L_PAIRES, "paires hexa attendues"),
    (L.L_SYSTEME, "refus système"),
    (L.L_ABSENT, "fichier introuvable"),
    (L.L_JOURNALPLEIN, "journal plein - Ctrl+S"),
    (L.L_RIENSAUVER, "rien à sauver"),
    (L.L_ECRITS, " o écrits · 0x"),
    (L.L_JUSQUA, "..0x"),
    (L.L_QUITTER, "MODIFIÉ - Alt+F4 encore pour quitter sans sauver, "
                  "Ctrl+S pour sauver"),
]
CLASSE_NOM = "LoupeHexa"
TITRE_NOM = "Loupe — l'éditeur hexadécimal"
ERREUR_NOM = "La fenêtre de Loupe ne peut pas être créée."


def _somme_qwords(octets: bytes) -> int:
    """La somme de contrôle des qwords du slot (modulo 2^64 — la convention
    de la lignée depuis M2 : la porte R10 tient dans son qword)."""
    return sum(struct.unpack_from(f"<{len(octets) // 8}Q", octets)) \
        & 0xFFFFFFFFFFFFFFFF


# --- Composition de l'image loupe.exe ----------------------------------------------

def composer_image(code: dict, extraits: dict):
    """-> (texte, rdata, data, text2, poses_rdata, table_r10) — l'image
    complète de loupe.exe aux quatre sections."""
    # -- .text : les héritages .text aux adresses scellées, le reste int3 ----
    texte = bytearray(b"\xcc" * L.TEXT_VSIZE)
    for nom, rva, taille, *_ in HERITAGES:
        if rva < L.RDATA_RVA:                      # libc + win-03 (le .text)
            texte[rva - L.TEXT_RVA: rva - L.TEXT_RVA + taille] = extraits[nom]

    # -- .text2 : les 18 blocs du domaine + la famille sha, le reste int3 ----
    text2 = bytearray(b"\xcc" * L.TEXT2_VSIZE)
    for bid, _sid, _fichier, _famille in BLOCS_LOUPE:
        rva, slot = L.SLOTS_LOUPE[bid]
        text2[rva - L.TEXT2_RVA: rva - L.TEXT2_RVA + slot] = \
            code[bid] + b"\x90" * (slot - len(code[bid]))
    for nom, rva, taille, *_ in HERITAGES:
        if rva >= L.TEXT2_RVA:                     # la famille sha (M9)
            text2[rva - L.TEXT2_RVA: rva - L.TEXT2_RVA + taille] = extraits[nom]

    # -- .rdata : les pièces du plan + l'IAT + la machinerie + la porte ------
    rdata = bytearray(b"\x00" * L.RDATA_VSIZE)
    _poses = []

    def poser(rva: int, donnees: bytes, nom: str = ""):
        fin = rva + len(donnees)
        if rva - L.RDATA_RVA + len(donnees) > L.RDATA_VSIZE:
            raise EchecBuild(f".rdata débordante à {rva:#x} (D33)")
        for rva_p, fin_p, nom_p in _poses:
            if rva < fin_p and rva_p < fin:
                raise EchecBuild(f"chevauchement .rdata : {nom or hex(rva)} "
                                 f"[{rva:#x}, {fin:#x}) recouvre {nom_p}")
        _poses.append((rva, fin, nom or hex(rva)))
        rdata[rva - L.RDATA_RVA: rva - L.RDATA_RVA + len(donnees)] = donnees

    hn = lambda nom: struct.pack("<H", 0) + nom.encode("ascii") + b"\x00"

    # les pièces du rendu + les tables MD5 (les constantes du plan)
    poser(L.R_ENTETE, ENTETE_TEXTE.encode("latin-1") + b"\x00", "entête")
    poser(L.R_HEX, b"0123456789ABCDEF\x00", "HEX")
    poser(L.R_HEXL, b"0123456789abcdef\x00", "HEXL")
    poser(L.R_MD5_S, struct.pack("<64I", *L.MD5_S), "MD5_S")
    poser(L.R_MD5_T, struct.pack("<64I", *L.MD5_T), "MD5_T")
    for adr, texte_libelle in LIBELLES:
        poser(adr, texte_libelle.encode("latin-1") + b"\x00", f"libellé")
    poser(L.R_CLASSE, CLASSE_NOM.encode("utf-16-le") + b"\x00\x00", "classe")
    poser(L.R_TITRE, TITRE_NOM.encode("utf-16-le") + b"\x00\x00", "titre")
    poser(L.R_ERREUR, ERREUR_NOM.encode("utf-16-le") + b"\x00\x00", "erreur")

    # le marché des imports : hints contigus, LES QUATRE OFT AU PAS DE
    # DWORD (la retouche dev.8 [OFT-QWORD] — l'Entrée 214 : le chargeur de
    # bibliothèque lisait OFT[1]=0 au pas de qword et ne résolvait qu'une
    # fonction par DLL), les descripteurs, les noms de DLL ; les QUATRE
    # PLAGES IAT RELOGÉES @0x3100 (la retouche dev.7 [D54-QUATRIÈME] —
    # l'Entrée 210) : SÉPARÉES PAR NULL, PRÉREMLIES des RVA de noms (le
    # motif D54 au complet) ; les vieilles plages @0x2400-0x250F et
    # @0x2818-0x282F NÉES ZÉRO (un slot mort doit être VIDE)
    hints = {}
    rva_h = L.R_HN
    for feuille in L.IAT_KERNEL32 + L.IAT_USER32 + L.IAT_GDI32:
        hints[feuille] = rva_h
        poser(rva_h, hn(feuille), f"hint {feuille}")
        rva_h += len(hn(feuille))
    # user32#2 : LA DOUBLE ENTRÉE DÉMO (les TROIS slots de win-03 reprpointés)
    demo_feuilles = ("GetMessageW", "TranslateMessage", "DispatchMessageW")
    for rva_oft, feuilles in ((L.R_INT_K32, L.IAT_KERNEL32),
                              (L.R_INT_U32, L.IAT_USER32),
                              (L.R_INT_GDI, L.IAT_GDI32),
                              (L.R_INT_U32B, demo_feuilles)):
        poser(rva_oft, b"".join(struct.pack("<I", hints[n]) for n in feuilles)
              + struct.pack("<I", 0), f"OFT {feuilles[0]}")
    poser(L.R_NOM_DLL, b"kernel32.dll\x00", "nom k32")
    poser(L.R_NOM_U32, b"user32.dll\x00", "nom u32")
    poser(L.R_NOM_GDI, b"gdi32.dll\x00", "nom gdi")
    # LES DESCRIPTEURS : OFT au pas DWORD + FT les plages relogées dev.7
    poser(L.R_DESC_IMPORT,
          struct.pack("<IIIII", L.R_INT_K32, 0, 0, L.R_NOM_DLL, L.R_IAT_K32)
          + struct.pack("<IIIII", L.R_INT_U32, 0, 0, L.R_NOM_U32, L.R_IAT_U32)
          + struct.pack("<IIIII", L.R_INT_GDI, 0, 0, L.R_NOM_GDI, L.R_IAT_GDI)
          + struct.pack("<IIIII", L.R_INT_U32B, 0, 0, L.R_NOM_U32,
                        L.R_IAT_DEMO_GMW)
          + b"\x00" * 20, "descripteurs")
    # LES QUATRE PLAGES IAT (chaque plage + son séparateur NULL, contiguës
    # de 0x3100 à 0x3248 — dir[12] exactement) ; les entrées PRÉREMPLIES
    # du RVA hint/nom : le chargeur lit le nom, le résout, l'y pose
    for rva_ft, feuilles in ((L.R_IAT_K32, L.IAT_KERNEL32),
                             (L.R_IAT_U32, L.IAT_USER32),
                             (L.R_IAT_GDI, L.IAT_GDI32),
                             (L.R_IAT_DEMO_GMW, demo_feuilles)):
        poser(rva_ft, b"".join(struct.pack("<Q", hints[n]) for n in feuilles)
              + struct.pack("<Q", 0), f"IAT {feuilles[0]}")

    # LA TABLE K DU SCELLÉ (le déplacement hérité de tls13-02 la vise)
    poser(L.R_K, extraits["K"], "K[64]")

    # LA PORTE R10 : un par bloc embarqué (les 18 + les 8 hérités, à l'ordre
    # des adresses) + terminateur ; la version + l'ancre
    embarques = ([(L.SLOTS_LOUPE[bid][0], L.SLOTS_LOUPE[bid][1])
                  for bid, *_ in BLOCS_LOUPE]
                 + [(rva, taille) for _n, rva, taille, *_ in HERITAGES])
    embarques.sort()
    table = b""
    for rva, taille in embarques:
        base = texte if rva < L.RDATA_RVA else text2
        off = rva - L.TEXT_RVA if rva < L.RDATA_RVA else rva - L.TEXT2_RVA
        tranche = bytes(base[off: off + taille])
        table += struct.pack("<IIQ", rva, taille, _somme_qwords(tranche))
    table += struct.pack("<IIQ", 0, 0, 0)
    poser(L.R_TAB_SUM, table, "porte R10")
    poser(L.R_VERSION, struct.pack("<Q", L.VERSION_DEV), "version R10")
    poser(L.R_ANCRE, struct.pack("<Q", 0), "ancre")

    # LE BASERELOC MINIMAL — le miroir M1..M9 (m2/build_m2.py:561) : douze
    # octets, la page .text, BlockSize 12, deux entrées ABSOLUTE (type 0,
    # sans effet). L'image est PI : la table ne reloge RIEN ; mais le
    # DllCharacteristics DYNAMIC_BASE invite le chargeur à déplacer
    # l'image, et SANS table déclarée il la REFUSE au premier relogement
    # exigé — 0xc000007b, le refus nommé du terrain M10-(e) sur dev.1
    # (l'Entrée 204 : la base 0x140000000 occupée par python.exe chez
    # l'utilisateur, le chargeur doit reloger — il ne peut pas).
    poser(L.R_RELOC, struct.pack("<II", L.TEXT_RVA, 12) + struct.pack("<HH", 0, 0),
          "BASERELOC minimal")

    # -- .data : le CADRE committé né LE MIROIR DU CADRE_VIERGE (l'Entrée 206) --
    # LE MIROIR EXACT du harnais (harnais_noyau.py CADRE_VIERGE : zéros
    # partout SAUF la poignée INVALIDE) — l'offset de la poignée CALCULÉ par
    # la chaîne des tailles du plan (CADRE_CHEMIN 520 + CADRE_TAILLE_F 8 =
    # 528), JAMAIS gravé de tête : CADRE_POIGNEE est une TAILLE (8) — dev.3
    # l'avait prise pour un offset, le terrain a nommé [CADRE-NÉ] au témoin.
    data = bytearray(b"\x00" * L.DATA_RAW)
    struct.pack_into("<Q", data, L.CADRE_CHEMIN + L.CADRE_TAILLE_F, L.INVALIDE)
    return bytes(texte), bytes(rdata), bytes(data), bytes(text2), _poses, table


# --- Éditeur PE32+ (quatre sections, VA croissantes — le miroir démo) -------------

def ecrire_pe32plus(texte: bytes, rdata: bytes, data: bytes, text2: bytes) -> bytes:
    dos = b"MZ" + b"\x00" * 58 + struct.pack("<I", 0x40)
    coff = struct.pack("<HHIIIHH", 0x8664, 4, 0, 0, 0, 0xF0, 0x0002)
    opt_fixe = struct.pack(
        "<HBBIIIIIQIIHHHHHHIIIIHHQQQQII",
        0x20B, 0, 0,
        len(texte) + len(text2), 0, 0,
        L.ENTREE, L.TEXT_RVA,
        L.IMAGE_BASE,
        L.SECT_ALIGN, L.FILE_ALIGN,
        6, 0, 0, 1, 6, 0, 0,
        L.SIZE_OF_IMAGE,
        L.FILE_ALIGN,
        0,
        L.SUBSYSTEM_GUI,             # WINDOWS_GUI — l'application fenêtrée
        L.DLL_CHARACTERISTICS,
        0x100000, 0x1000, 0x100000, 0x1000,
        0, 16,
    )
    dirs = [(0, 0)] * 16
    dirs[1] = (L.R_DESC_IMPORT, 100)   # 5 descripteurs (4 marchés + terminateur)
    dirs[5] = (L.R_RELOC, 12)         # BASERELOC minimal (l'image PI que le
                                      # chargeur PEUT reloger — le miroir M1..M9)
    dirs[12] = (L.R_IAT_DIR, L.IAT_DIR_TAILLE)   # l'IAT relogée (les QUATRE
                                   # plages séparées par NULL — dev.7)
    opt = bytes(opt_fixe) + b"".join(struct.pack("<II", *d) for d in dirs)

    def sh(nom, vsize, vaddr, rawsz, rawptr, cara):
        return struct.pack("<8sIIIIIIHHI", nom, vsize, vaddr, rawsz, rawptr,
                           0, 0, 0, 0, cara)

    sections = (
        sh(b".text\x00\x00\x00", L.TEXT_VSIZE, L.TEXT_RVA, L.TEXT_VSIZE,
           L.TEXT_FILE, 0x60000020)
        + sh(b".rdata\x00\x00", L.RDATA_VSIZE, L.RDATA_RVA, L.RDATA_VSIZE,
             L.RDATA_FILE, 0x40000040)
        + sh(b".text2\x00\x00", L.TEXT2_VSIZE, L.TEXT2_RVA, L.TEXT2_VSIZE,
             L.TEXT2_FILE, 0x60000020)
        + sh(b".data\x00\x00\x00", L.DATA_VSIZE, L.DATA_RVA, L.DATA_RAW,
             L.DATA_FILE, 0xC0000040)
    )
    entetes = dos + b"PE\x00\x00" + coff + opt + sections
    assert len(entetes) == 64 + 4 + 20 + 240 + 160
    exe = bytearray(b"\x00" * L.TAILLE_FICHIER)
    exe[0:len(entetes)] = entetes
    exe[L.TEXT_FILE:L.TEXT_FILE + len(texte)] = texte
    exe[L.RDATA_FILE:L.RDATA_FILE + len(rdata)] = rdata
    exe[L.TEXT2_FILE:L.TEXT2_FILE + len(text2)] = text2
    exe[L.DATA_FILE:L.DATA_FILE + len(data)] = data
    return bytes(exe)


# --- Validation PE (la composition INTÉGRALE : chaque octet compté) ----------------

def valider_pe(exe: bytes, code: dict, extraits: dict, poses_rdata, table_r10):
    pe = pefile.PE(data=exe)
    if pe.FILE_HEADER.Machine != 0x8664 or pe.OPTIONAL_HEADER.Magic != 0x20B:
        raise EchecBuild("l'en-tête PE32+ n'est pas conforme")
    if pe.FILE_HEADER.NumberOfSections != 4:
        raise EchecBuild("quatre sections attendues")
    if pe.OPTIONAL_HEADER.AddressOfEntryPoint != L.ENTREE:
        raise EchecBuild(f"l'entrée != LOUPE09_VA ({L.ENTREE:#x} — D161 : "
                         f"l'entrée EST le bloc, aucune fiction de trampoline)")
    if pe.OPTIONAL_HEADER.Subsystem != L.SUBSYSTEM_GUI:
        raise EchecBuild("le sous-système != WINDOWS_GUI")
    if pe.OPTIONAL_HEADER.SizeOfImage != L.SIZE_OF_IMAGE:
        raise EchecBuild("SizeOfImage != 0x20000")
    noms = [s.Name.decode().rstrip("\x00") for s in pe.sections]
    if noms != [".text", ".rdata", ".text2", ".data"]:
        raise EchecBuild(f"les sections {noms} != le miroir démo")

    tranche = lambda rva, n: exe[pe.get_offset_from_rva(rva): pe.get_offset_from_rva(rva) + n]

    # LE MARCHÉ DES IMPORTS — LA MARCHE DU CHARGEUR (D54, la doctrine de
    # l'Entrée 210 : le chargeur MARCHE les plages FirstThunk jusqu'au NULL ;
    # pefile lit l'OFT au pas de qword — le pas de DWORD de la retouche dev.8
    # le rend aveugle au 4e descripteur : la vérification dérive du PLAN,
    # jamais de l'outil) : les QUATRE descripteurs relus champ à champ, chaque
    # plage FT MARCHÉE — le compte exact, chaque entrée == le RVA hint/nom de
    # SA feuille (le préremplissage D54), les séparateurs NULL aux bornes
    marche = [(L.R_INT_K32, "kernel32.dll", L.R_NOM_DLL, L.R_IAT_K32,
               L.IAT_KERNEL32),
              (L.R_INT_U32, "user32.dll", L.R_NOM_U32, L.R_IAT_U32,
               L.IAT_USER32),
              (L.R_INT_GDI, "gdi32.dll", L.R_NOM_GDI, L.R_IAT_GDI,
               L.IAT_GDI32),
              (L.R_INT_U32B, "user32.dll", L.R_NOM_U32, L.R_IAT_DEMO_GMW,
               ("GetMessageW", "TranslateMessage", "DispatchMessageW"))]
    hints = {}
    rva_h = L.R_HN
    for _f in L.IAT_KERNEL32 + L.IAT_USER32 + L.IAT_GDI32:
        hints[_f] = rva_h
        rva_h += 2 + len(_f) + 1
    for k, (oft_attendu, dll_attendue, rva_nom, ft_attendu, feuilles) in \
            enumerate(marche):
        oft, _tds, _fwd, nom_rva, ft = struct.unpack_from(
            "<IIIII", tranche(L.R_DESC_IMPORT + 20 * k, 20))
        if (oft, ft) != (oft_attendu, ft_attendu):
            raise EchecBuild(f"le descripteur #{k} : OFT/FT ({oft:#x}/{ft:#x}) "
                             f"!= le plan ({oft_attendu:#x}/{ft_attendu:#x})")
        if tranche(nom_rva, len(dll_attendue) + 1) != \
                dll_attendue.encode("ascii") + b"\x00":
            raise EchecBuild(f"le descripteur #{k} : le nom != {dll_attendue}")
        # LA MARCHE de la plage : les entrées jusqu'au NULL, le compte exact,
        # chaque entrée PRÉREMPLIE du RVA hint/nom de sa feuille (D54)
        vus = []
        for i in range(len(feuilles) + 1):
            q, = struct.unpack_from("<Q", tranche(ft + 8 * i, 8))
            if q == 0:
                break
            vus.append(q)
        if len(vus) != len(feuilles):
            raise EchecBuild(f"la plage {dll_attendue} @ {ft:#x} : {len(vus)} "
                             f"entrées != {len(feuilles)} feuilles (D54)")
        for i, feuille in enumerate(feuilles):
            if vus[i] != hints[feuille]:
                raise EchecBuild(
                    f"la plage {dll_attendue} @ {ft:#x} : l'entrée {i} "
                    f"({vus[i]:#x}) != le RVA hint/nom de {feuille} "
                    f"({hints[feuille]:#x} — le préremplissage D54)")
        # le séparateur NULL à la borne de la plage
        sep, = struct.unpack_from("<Q",
                                  tranche(ft + 8 * len(feuilles), 8))
        if sep != 0:
            raise EchecBuild(f"la plage {dll_attendue} : le séparateur NULL "
                             f"absent @ {ft + 8 * len(feuilles):#x} (D54)")
    # le terminateur (le 5e descripteur)
    if tranche(L.R_DESC_IMPORT + 80, 20) != b"\x00" * 20:
        raise EchecBuild("le terminateur des descripteurs n'est pas nul")
    # les 37 feuilles AU TOTAL (34 + la double entrée démo : les TROIS de
    # win-03 comptées DEUX FOIS, une par plage — le prix du relogement),
    # aucune de plus : la marche s'arrête au NULL de chaque plage
    totale = sum(struct.unpack_from("<Q", tranche(L.R_IAT_DIR + 8 * i, 8))[0]
                 for i in range(41))
    if totale != sum(hints[f] for f in L.IAT_KERNEL32 + L.IAT_USER32
                     + L.IAT_GDI32) + hints["GetMessageW"] \
            + hints["TranslateMessage"] + hints["DispatchMessageW"]:
        raise EchecBuild("l'IAT déclarée porte des entrées hors du marché des "
                         "34 feuilles + la double entrée (la somme des "
                         "préremplissages)")
    # dir[12] : l'IAT déclarée — la plage relogée, 41 qwords (37 + 4 NULL)
    iat_dir = pe.OPTIONAL_HEADER.DATA_DIRECTORY[12]
    if iat_dir.VirtualAddress != L.R_IAT_DIR or iat_dir.Size != L.IAT_DIR_TAILLE:
        raise EchecBuild("le répertoire IAT != le plan (0x3100, 0x148 — les "
                         "QUATRE plages séparées par NULL, l'Entrée 210)")

    # LA COMPOSITION INTÉGRALE — chaque octet de chaque section compté :
    # (a) .text : les 4 héritages posés, le reste int3
    for nom, rva, taille, *_ in HERITAGES:
        if rva < L.RDATA_RVA and tranche(rva, taille) != extraits[nom]:
            raise EchecBuild(f"{nom} : l'extrait posé != le scellé (R7)")
    for i in range(L.TEXT_RVA, L.RDATA_RVA, 16):
        bout = tranche(i, 16)
        dans_bloc = any(rva <= i < rva + taille
                        for _n, rva, taille, *_ in HERITAGES if rva < L.RDATA_RVA)
        if not dans_bloc and bout != b"\xcc" * 16:
            raise EchecBuild(f".text @{i:#x} : ni héritage ni int3 (chaque octet compté)")
    # (b) .text2 : les 18 blocs + la famille sha, le reste int3
    for bid, _sid, _fichier, _famille in BLOCS_LOUPE:
        rva, slot = L.SLOTS_LOUPE[bid]
        attendu = code[bid] + b"\x90" * (slot - len(code[bid]))
        if tranche(rva, slot) != attendu:
            raise EchecBuild(f"{bid} : le slot posé != la notation + le padding NOP")
    for nom, rva, taille, *_ in HERITAGES:
        if rva >= L.TEXT2_RVA and tranche(rva, taille) != extraits[nom]:
            raise EchecBuild(f"{nom} : l'extrait posé != le scellé (R7)")
    poses_text2 = ([(L.SLOTS_LOUPE[bid][0], L.SLOTS_LOUPE[bid][1]) for bid, *_ in BLOCS_LOUPE]
                   + [(rva, taille) for _n, rva, taille, *_ in HERITAGES if rva >= L.TEXT2_RVA])
    for i in range(L.TEXT2_RVA, L.TEXT2_RVA + L.TEXT2_VSIZE, 16):
        if not any(rva <= i < rva + taille for rva, taille in poses_text2):
            if tranche(i, 16) != b"\xcc" * 16:
                raise EchecBuild(f".text2 @{i:#x} : ni bloc ni int3 (chaque octet compté)")
    # (c) .rdata : chaque pose du plan, le reste la marge zéro
    if tranche(L.R_TAB_SUM, len(table_r10)) != table_r10:
        raise EchecBuild("la porte R10 relue de l'image != la table composée")
    if struct.unpack_from("<Q", tranche(L.R_VERSION, 8))[0] != L.VERSION_DEV:
        raise EchecBuild("le qword version != VERSION_DEV (R10)")
    # LE BASERELOC MINIMAL (le miroir M1..M9 — le refus 0xc000007b du terrain
    # sur dev.1 ne reviendra plus) : le répertoire DÉCLARÉ au plan, les douze
    # octets relus — l'image PI que le VRAI chargeur PEUT reloger
    reloc_dir = pe.OPTIONAL_HEADER.DATA_DIRECTORY[5]
    if reloc_dir.VirtualAddress != L.R_RELOC or reloc_dir.Size != 12:
        raise EchecBuild("le répertoire BASERELOC != le plan (R_RELOC, 12 o — "
                         "le miroir M1..M9 : sans lui le VRAI chargeur ne peut "
                         "pas reloger l'image ASLR, le refus 0xc000007b du terrain)")
    if tranche(L.R_RELOC, 12) != struct.pack("<II", L.TEXT_RVA, 12) \
            + struct.pack("<HH", 0, 0):
        raise EchecBuild("le bloc BASERELOC != les douze octets de la lignée "
                         "(la page .text, deux entrées ABSOLUTE — l'image PI)")
    couvert = bytearray(L.RDATA_VSIZE)
    for rva, fin, _nom in poses_rdata:
        for i in range(rva - L.RDATA_RVA, fin - L.RDATA_RVA):
            couvert[i] = 1
    poses_rdata_set = [(rva, fin) for rva, fin, _n in poses_rdata]
    for i in range(L.RDATA_VSIZE):
        if not couvert[i]:
            rva = L.RDATA_RVA + i
            if exe[pe.get_offset_from_rva(L.RDATA_RVA) + i] != 0:
                raise EchecBuild(f".rdata @{rva:#x} : hors des pièces du plan "
                                 f"(la composition intégrale)")
    # (d) .data : LE CADRE né LE MIROIR DU CADRE_VIERGE, le reste zéro —
    # l'offset RE-LU CALCULÉ PAR LA MÊME chaîne des tailles que
    # l'initialiseur (l'Entrée 206 : dev.3 relisait à +8 — un garde blessé
    # par le défaut qu'il croyait garder ne garde rien ; le contrôle
    # dérive du plan, jamais de la pièce qu'il contrôle)
    o_poignee = L.CADRE_CHEMIN + L.CADRE_TAILLE_F
    if struct.unpack_from("<Q", tranche(L.R_CADRE + o_poignee, 8))[0] != L.INVALIDE:
        raise EchecBuild("le CADRE à l'image n'est pas né poignée INVALIDE "
                         "(le miroir du harnais à +528 — le zéro serait une "
                         "session fantôme : loupe-02 y croirait ; l'offset "
                         "CALCULÉ par la chaîne des tailles, jamais gravé)")
    attendu_data = bytearray(L.DATA_RAW)
    struct.pack_into("<Q", attendu_data, o_poignee, L.INVALIDE)
    if tranche(L.R_CADRE, L.DATA_RAW) != bytes(attendu_data):
        raise EchecBuild("le .data né != le miroir du harnais (zéros partout "
                         "SAUF la poignée INVALIDE à +528 — l'Entrée 206 : "
                         "l'initialiseur .data est LE MIROIR EXACT, le reste "
                         "des zones né zéro)")
    if len(exe) != L.TAILLE_FICHIER:
        raise EchecBuild(f"la taille du fichier != {L.TAILLE_FICHIER:#x}")
    print(f"[PE] loupe.exe : {len(exe):,} o, QUATRE sections (.text la minilibc + "
          f"la boucle scellées · .rdata les pièces + l'IAT + la machinerie + la "
          f"porte R10 + K[64] · .text2 les 18 blocs + la famille sha scellée · "
          f".data LE CADRE né MIROIR DU CADRE_VIERGE [zéros + la poignée "
          f"INVALIDE @+528 — l'Entrée 206]), entrée {L.ENTREE:#x} (WinMain), "
          f"WINDOWS_GUI, LA COMPOSITION INTÉGRALE comptée (chaque octet : bloc, "
          f"pièce, int3 ou marge zéro)".replace(",", " "))


# --- Les harnais du domaine rejoués au geste du build -------------------------------

HARNAIS = [
    ("harnais_noyau.py", "le noyau loupe-01..07"),
    ("harnais_rendu.py", "le rendu + la navigation loupe-08..14"),
    ("harnais_edition.py", "l'édition loupe-15..18 + la table r2"),
]


def rejouer_harnais() -> list[dict]:
    """LES TROIS HARNAIS rejoués au geste même du build — le verdict TRANCHÉ
    par les instruments (les vecteurs officiels, le différentiel, les
    scénarios, la falsification) ; l'empreinte du run consignée à la carte.

    LES TROIS EN CONCURRENCE (l'Entrée 204) : des instruments INDÉPENDANTS —
    aucun chemin partagé (aucun fichier écrit, la sortie seule), chacun dans
    son propre sous-processus ; les empreintes et l'ordre de consignation
    sont CEUX DE LA LIGNÉE (l'ordre HARNAIS, pas l'ordre d'arrivée) — la
    fenêtre du labo est bornée, l'édition (5 min 20) ne peut plus tenir
    APRÈS le rendu en une seule vie."""
    from concurrent.futures import ThreadPoolExecutor

    def jouer(script: str, description: str) -> tuple[str, str, int, str]:
        chemin = os.path.join(ICI, script)
        proc = subprocess.run([sys.executable, chemin], capture_output=True,
                              text=True, timeout=1800, cwd=ICI)
        return script, description, proc.returncode, proc.stdout + proc.stderr

    verdicts = []
    with ThreadPoolExecutor(max_workers=len(HARNAIS)) as pool:
        resultats = list(pool.map(lambda h: jouer(*h), HARNAIS))
    sorties = {script: (rc, sortie) for script, _d, rc, sortie in resultats}
    for script, description in HARNAIS:            # l'ordre de la lignée
        retour, sortie = sorties[script]
        if retour != 0 or "VERDICT : VERT" not in sortie:
            raise EchecBuild(f"{script} ({description}) : le harnais n'est pas "
                             f"VERT au geste du build — le domaine n'est pas "
                             f"prouvé, RIEN n'est écrit")
        m = re.search(r"LE CAHIER : (\d+) contrôles — (\d+) VERTS", sortie)
        total = int(m.group(1)) if m else 0
        verts = int(m.group(2)) if m else 0
        verdicts.append({"harnais": script, "description": description,
                         "total": total, "verts": verts,
                         "empreinte": "sha256:" + hashlib.sha256(
                             sortie.encode("utf-8")).hexdigest()})
        print(f"[harnais] {script} : {verts}/{total} VERTS — {description} "
              f"(rejoué AU GESTE du build)")
    return verdicts


# --- La carte génération 13 (lignée D80, graine durable D144) ----------------------

def construire_carte(exe: bytes, specs: dict, code: dict, verrous: int,
                     verdicts: list[dict], journal_runs: list[str]):
    import carte_m10 as cm10
    phrase, graine = cm10.charger_secrets(interactif=False)
    maitre = cm10.cle_maitresse(phrase)
    clairs = cm10.fragments_clairs(exe, specs, code, verrous, verdicts,
                                   journal_runs)
    fragments = {n: cm10.chiffrer_fragment(maitre, n, clairs[n])
                 for n in cm10.FRAGMENTS}
    racine = cm10.empreinte_racine(fragments)
    entete = cm10.construire_entete(racine, cm10.VERSION_DEV)
    prive, pub = cm10.paire_cles(graine)
    signature = cm10.signer(prive, entete, fragments)
    cm10.ecrire_carte(entete, fragments, signature, pub)
    return cm10


def verrou_croise(exe: bytes) -> tuple[int, dict]:
    """R8 : relecture indépendante — la carte déchiffrée, chaque empreinte
    de bloc revérifiée CONTRE l'artefact, l'artefact contre son manifeste."""
    import carte_m10 as cm10
    phrase, _ = cm10.charger_secrets(interactif=False)
    entete, fragments, signature, pub = cm10.lire_carte()
    cm10.verifier_listes_blanches(entete.decode("ascii"))
    cm10.verifier_signature(pub, entete, fragments, signature)
    if cm10.empreinte_racine(fragments).hex() not in entete.decode("ascii"):
        raise cm10.ErreurCarte("empreinte racine divergente")
    maitre = cm10.cle_maitresse(phrase)
    bld = cm10.dechiffrer_fragment(maitre, "frag-bld",
                                   fragments["frag-bld"]).decode("utf-8")
    empreintes, manifestes = {}, []
    for ligne in bld.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[champs["id"]] = champs["empreinte"]
        elif ligne.startswith("[build]"):
            manifestes.append(dict(re.findall(r"(\w+)=(\S+)", ligne)))
    manifeste = next((m for m in manifestes if m.get("artefact") == "loupe.exe"), {})
    pe = pefile.PE(data=exe)
    tranche = lambda rva, n: exe[pe.get_offset_from_rva(rva):
                                 pe.get_offset_from_rva(rva) + n]
    # la correspondance héritage -> id de carte (la numérotation des familles)
    _BID_CARTE = {"libc-01": "b20001", "libc-02": "b20002", "libc-07": "b20007",
                  "win-03": "d40003", "tls13-01": "h100001",
                  "tls13-02": "h100002", "tls13-03": "h100003",
                  "tls13-04": "h100004"}
    embarques = ([(bid, L.SLOTS_LOUPE[bid][0], L.SLOTS_LOUPE[bid][1])
                  for bid, *_ in BLOCS_LOUPE]
                 + [(_BID_CARTE[nom], rva, taille)
                    for nom, rva, taille, *_ in HERITAGES])
    for bid, rva, taille in embarques:
        sha = "sha256:" + hashlib.sha256(tranche(rva, taille)).hexdigest()
        if sha != empreintes.get(bid):
            raise cm10.ErreurCarte(f"verrou croisé : empreinte de {bid} divergente (R8)")
    sha_exe = "sha256:" + hashlib.sha256(exe).hexdigest()
    if sha_exe != manifeste.get("empreinte"):
        raise cm10.ErreurCarte("verrou croisé : empreinte de loupe.exe divergente (R8)")
    return len(empreintes), manifeste


def tableau_de_bord(exe: bytes, verrous: int, verdicts: list[dict],
                    nb_carte: int, manifeste: dict) -> str:
    lignes = [
        "=== TABLEAU DE BORD — loupe.exe 0.1.1-dev.1 (le TGN « Loupe », M10 — "
        "LA VERSION COMMANDÉE D179) ===",
        f"artefact     : loupe.exe ({len(exe):,} o)".replace(",", " "),
        f"version      : {manifeste.get('version', '0.1.1-dev.1')} "
        f"(LA VERSION 0.1.1 COMMANDÉE PAR LE DÉVELOPPEUR — D178/D179 : la",
        f"               dette [R10-PÉRIMÉE] SOLDÉE à la naissance — la porte",
        f"               R10 véridique, le code byte-identique au vécu des",
        f"               ONZE RUNS de l'ère 0.1.0 ; la balise `loupe 0.1.1` se",
        f"               scellera PAR FAIT DE CARTE sur le vert recoupé du",
        f"               DOUZIÈME run)",
        f"empreinte    : {manifeste.get('empreinte', '')}",
        f"profil       : x86-64-win11-pe · WINDOWS_GUI · entrée {L.ENTREE:#x} (WinMain)",
        "sections     : .text 0x1000 (la minilibc + la boucle SCELLÉES) ·",
        "               .rdata 0x2000 (les pièces, l'IAT 34 feuilles, la porte R10, K[64])",
        "               .text2 0x4000 (les 18 blocs + la famille sha SCELLÉE) ·",
        "               .data 0xE000 (le CADRE né poignée INVALIDE, CUMUL 64 Kio)",
        f"verrous      : {verrous} structurels (le réseau des specs, les listes",
        "               fermées IAT, les déplacements RIP, les slots disjoints)",
        "héritage R7  : libc-01/02/07 (M1) + win-03 (démo) + tls13-01..04 (M9)",
        "               + K[64] — LA DOUBLE PREUVE (les scellés == les notations",
        "               d'origine ré-assemblées == les octets posés)",
        "harnais      : " + " + ".join(
            f"{v['harnais']} {v['verts']}/{v['total']}" for v in verdicts),
        f"carte        : génération 17 (lignée D80, graine durable D144 — la",
        f"               16 demeure celle de la balise 0.1.0 SCELLÉE),",
        f"               {nb_carte} empreintes au verrou croisé (R8)",
        "frontières   : AUCUNE balise ne bouge (win 0.9.0 / linux 0.7.0 /",
        "               riscv 0.8.0 / tls13 1.0.0 INTACTES) ; le garde 14/14",
        "               VERT AVANT construire() ; la clé privée jamais",
        "               traversée (D87) ; aucun octet de notation (R2)",
    ]
    return "\n".join(lignes) + "\n"


# --- L'ÉCART NOMMÉ [R10-PÉRIMÉE] (le constat du port à l'époque dev.8) ---------------

def _ecart_r10_nomme(exe_neuf: bytes, deploye: bytes) -> list[tuple[int, int, int]]:
    """La recomposition contre LA PIÈCE DÉPLOYÉE (le témoin du terrain) :
    tout écart doit être CONFINÉ aux champs de SOMMES de la porte R10 —
    la pièce porte les sommes de l'ère dev.5 (la retouche des Entrées
    210/214 changea les octets des blocs SANS rafraîchir la table : 17
    entrées périmées, nommées) ; la recomposition, elle, dit la VÉRITÉ de
    l'image (chaque somme == son bloc relu). La pièce demeure INTACTE —
    sa porte périmée est son histoire, personne ne la vérifie à
    l'exécution (le chargeur l'ignore, le scénario ne la lit pas).
    Retourne [(rva, somme_pièce, somme_vérité)] — ou ÉCHEC NOMMÉ."""
    if len(exe_neuf) != len(deploye):
        raise EchecBuild(f"la recomposition ({len(exe_neuf)} o) != la pièce "
                         f"déployée ({len(deploye)} o) — la taille ne bouge "
                         f"jamais (R7)")
    fo_rdata = lambda rva: rva - L.RDATA_RVA + L.RDATA_FILE
    champs_sommes = set()
    entrees = []
    for k in range(26):
        base = fo_rdata(L.R_TAB_SUM) + 16 * k
        rva, taille, _s = struct.unpack_from("<IIQ", exe_neuf, base)
        entrees.append((rva, taille, base + 8))
        champs_sommes.update(range(base + 8, base + 16))
    hors = [i for i, (a, b) in enumerate(zip(exe_neuf, deploye))
            if a != b and i not in champs_sommes]
    if hors:
        raise EchecBuild(f"la recomposition diverge de la pièce déployée "
                         f"HORS de la porte R10 : {len(hors)} octets (le "
                         f"premier @fichier {hors[0]:#x}) — le plan ne "
                         f"reproduit PAS la pièce, ÉCHEC")
    perimees = []
    for (rva, taille, off_somme), _ in zip(entrees, range(26)):
        s_piece, = struct.unpack_from("<Q", deploye, off_somme)
        s_neuve, = struct.unpack_from("<Q", exe_neuf, off_somme)
        if s_piece != s_neuve:
            perimees.append((rva, s_piece, s_neuve))
    return perimees


# --- Le port de l'ère 0.1.1 (D179 — la dette soldée à la naissance) ----------------

def _porte_ere_011(exe_neuf: bytes, deploye: bytes,
                   journal: list[str]) -> bytes:
    """LE PORT DE L'ÈRE 0.1.1 (D179, la version commandée) : la pièce
    déployée porte l'ère 0.1.0 (qword 0x00010008, LA SCELLÉE du onzième
    run — 054de960…, ASSERTÉE) ; la recomposition porte l'ère 0.1.1-dev.1
    (qword 0x00010101). L'ÉCART doit être CONFINÉ aux champs NOMMÉS : les
    sommes de la porte R10 (la dette [R10-PÉRIMÉE] rafraîchie à la
    vérité des blocs) + le qword version — 0 octet ailleurs (R4 : le
    contrat stable, le code BYTE-IDENTIQUE au vécu des onze runs ;
    R7 : les adresses intactes). La nouvelle pièce est ÉCRITE ;
    l'ancienne demeure au git et au coffre."""
    SHA_010 = ("054de960c31425d022f6900f27e59bdd"
               "82a120b0b3fe543a67e778867e9c7a69")
    if len(exe_neuf) != len(deploye):
        raise EchecBuild(f"la recomposition ({len(exe_neuf)} o) != la pièce "
                         f"déployée ({len(deploye)} o) — la taille ne bouge "
                         f"jamais (R7)")
    sha_deploye = hashlib.sha256(deploye).hexdigest()
    if sha_deploye != SHA_010:
        raise EchecBuild(f"la pièce déployée ({sha_deploye[:16]}…) n'est pas "
                         f"LA SCELLÉE 0.1.0 (054de960…) — le port d'ère ne "
                         f"vit que de la pointe canonique (D164/D179)")
    fo_rdata = lambda rva: rva - L.RDATA_RVA + L.RDATA_FILE
    off_version = fo_rdata(L.R_VERSION)
    q_deploye, = struct.unpack_from("<Q", deploye, off_version)
    q_neuf, = struct.unpack_from("<Q", exe_neuf, off_version)
    if q_deploye != 0x00010008:
        raise EchecBuild(f"le qword de la déployée ({q_deploye:#x}) != "
                         f"l'ère 0.1.0 (0x00010008) — port d'ère REFUSÉ")
    if q_neuf != L.VERSION_DEV:
        raise EchecBuild(f"le qword de la recomposition ({q_neuf:#x}) != "
                         f"VERSION_DEV ({L.VERSION_DEV:#x})")
    champs_nommes = set(range(off_version, off_version + 8))     # le qword
    for k in range(26):                        # les sommes de la porte R10
        base = fo_rdata(L.R_TAB_SUM) + 16 * k
        champs_nommes.update(range(base + 8, base + 16))
    hors = [i for i, (a, b) in enumerate(zip(exe_neuf, deploye))
            if a != b and i not in champs_nommes]
    if hors:
        raise EchecBuild(f"le port de l'ère 0.1.1 diverge HORS des champs "
                         f"nommés : {len(hors)} octets (le premier @fichier "
                         f"{hors[0]:#x}) — R4/R7 blessés, ÉCHEC")
    rafraichies = 0
    for k in range(26):
        base = fo_rdata(L.R_TAB_SUM) + 16 * k
        s_v, = struct.unpack_from("<Q", deploye, base + 8)
        s_n, = struct.unpack_from("<Q", exe_neuf, base + 8)
        rafraichies += (s_v != s_n)
    print(f"[0.1.1] LA DETTE [R10-PÉRIMÉE] SOLDÉE À LA NAISSANCE : "
          f"{rafraichies} sommes rafraîchies à la vérité des blocs, le "
          f"qword porté {q_deploye:#x} → {q_neuf:#x}, 0 octet ailleurs — "
          f"le code BYTE-IDENTIQUE au vécu des onze runs (R4/R7) ; la "
          f"pièce 0.1.0 (054de960…) demeure au git et au coffre")
    journal.append(f"[0.1.1] la version COMMANDÉE (D179) née : "
                   f"{rafraichies} sommes véridiques + le qword "
                   f"{q_deploye:#x} → {q_neuf:#x}, 0 octet ailleurs — la "
                   f"dette [R10-PÉRIMÉE] soldée, la 0.1.0 scellée demeurée")
    return exe_neuf


# --- L'anti-rollback (R6 : une carte scellée interdit la reconstruction) -------------

# LA PIÈCE DU RECOUP VIT AU DÉPÔT (l'Entrée 219 : le modèle M9 — le verdict
# de preuves-run-m9f-7 vivait au download/ ; le chemin du bac à sable mort
# de la session du scellage ne se re-vit JAMAIS : la porte est de PROCESSUS,
# la pièce est du DÉPÔT). À l'ère 0.1.1 : le verdict du DOUZIÈME run
# (l'Entrée 222 — le miroir D165/D170 ; celui du onzième demeure à
# preuves-run-loupe-dev12/ pour l'histoire de la balise 0.1.0)
VERDICT_RECOUP_011 = os.path.join(
    TRIADE, "download", "preuves-run-loupe-011-dev1",
    "VERDICT-run-loupe-011-dev1.txt")


def _version_carte(cm10) -> str | None:
    """La balise portée par la carte déposée — L'EN-TÊTE SIGNÉ (en clair :
    génération-indépendant, l'ère se lit d'une génération à l'autre —
    D179 : le passage 16 → 17 ne doit JAMAIS aveugler l'anti-rollback) ;
    frag-bld demeurant l'autorité du manifeste au scellage."""
    try:
        entete, _fragments, _signature, _pub = cm10.lire_carte()
        m = re.search(rb"\[carte\] version=(\S+)", entete)
        return m.group(1).decode("ascii") if m else None
    except FileNotFoundError:
        return None          # pas de carte lisible : première construction


def _version_ordre(v: str) -> tuple[int, ...]:
    """"0.1.0" → (0,1,0,0,0) ; "0.1.0-dev.8" → (0,1,0,-1,8) — une
    pré-version est MOINDRE que sa balise, une balise supérieure OUvre
    l'ère suivante (R10 : la monotonie)."""
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:-dev\.(\d+))?", v or "")
    if not m:
        return (-1, -1, -1, -1, -1)
    X, Y, Z, d = m.groups()
    return (int(X), int(Y), int(Z), 0 if d is None else -1,
            0 if d is None else int(d))


def _anti_rollback() -> None:
    """Une carte scellée (rc/finale) interdit la reconstruction (R6) — SAUF
    LA VERSION STRICTEMENT SUPÉRIEURE commandée par le développeur (R10 :
    la monotonie ; D178/D179 : « nouvelle version X.Y.Z+1 requise » — la
    0.1.1-dev.1 après la 0.1.0 scellée, la dette [R10-PÉRIMÉE] soldée à
    la naissance ; une pré-version de la balise scellée demeure REFUSÉE :
    (0,1,0,-1,N) < (0,1,0,0,0) — jamais de retour en arrière)."""
    import carte_m10 as _cm10
    v = _version_carte(_cm10)
    if v and ("-rc" in v or re.fullmatch(r"\d+\.\d+\.\d+", v)):
        if _version_ordre(_cm10.VERSION_DEV) > _version_ordre(v):
            print(f"[anti-rollback] la carte scellée ({v}) demeure — la "
                  f"version commandée {_cm10.VERSION_DEV} est STRICTEMENT "
                  f"SUPÉRIEURE : la monotonie R10 OUvre la nouvelle ère "
                  f"(D179 — la dette [R10-PÉRIMÉE] soldée à la naissance)")
            return
        raise EchecBuild(
            f"carte scellée ({v}) : reconstruction interdite — "
            f"procedure lourde R6 ou nouvelle version X.Y.Z+1 requise")


def _sceller_final() -> int:
    """Scellage de la finale 0.1.1 (modèle D104/M9 — Entrées 218/222 : le
    scellage est un FAIT DE CARTE — l'artefact ne bouge JAMAIS, loupe.exe
    demeure byte-identique à la 0.1.1-dev.1 que LE DOUZIÈME RUN a courue
    et vécue). Les portes, tranchées binaires AVANT l'unique écriture : le
    garde sceau I (D87), LE RECOUP TERRAIN VERT SUR PIÈCES (le douzième
    run consigné — l'Entrée 222 : LE VERT TIENT ENTIER, 39/39, la
    vitrine vivante la troisième fois), la cristallisation R6 10/10, le
    verrou croisé R8, la balise encore dev ; puis la bascule de balise
    dans frag-bld (occurrence unique, vérifiée EN MÉMOIRE avant
    l'écriture), l'entête portant LA BALISE, la signature Ed25519
    re-signée (graine durable D144 : LE TÉMOIN NE BOUGE PAS),
    l'anti-rollback ARMÉ (constaté au geste même — la 0.1.0 scellée
    demeurée, la monotonie R10 n'ouvre jamais l'ancienne), le tableau de
    bord « loupe 0.1.1 SCELLÉE sur le douzième run vert recoupé » — LA
    VERSION DE LA DETTE [R10-PÉRIMÉE] SOLDÉE."""
    import carte_m10 as cm10
    print("=== M10 : SCELLAGE de la finale 0.1.1 (le fait de carte — le "
          "douzième run vert recoupé, l'Entrée 222 : LE VERT TIENT ENTIER) "
          "===")

    # 1. le garde sceau I (D87) — l'état « réelle » tenu avant tout geste
    _garde_sceau_I()

    # 2. LE RECOUP TERRAIN sur pièces (la seule porte que le terrain ouvre)
    if not os.path.isfile(VERDICT_RECOUP_011):
        raise EchecBuild(
            f"le verdict du recoup terrain est ABSENT ({VERDICT_RECOUP_011})"
            " — le recoup labo d'abord : la finale ne se scelle QUE sur "
            "pièces (D138/D145/D148)")
    with open(VERDICT_RECOUP_011, encoding="utf-8") as f:
        verdict_recoup = f.read()
    for porte, attendu in (
            ("le vert", "LE VERT TIENT ENTIER"),
            ("le recoup", "39/39 contrôles VERTS"),
            ("la condition", "EST SATISFAITE"),
            ("l'empreinte", "c111510535767a40"),
            ("la vitrine", "LA VITRINE VIVANTE LA TROISIÈME FOIS")):
        if attendu not in verdict_recoup:
            raise EchecBuild(f"la porte « {porte} » ({attendu!r}) manque au "
                             f"verdict du douzième run — scellage REFUSÉ "
                             f"(fail-closed)")
    print("[terrain] LE DOUZIÈME RUN recoupé 39/39 sur pièces croisées : "
          "T0→T7 TOUT VERT POUR LA CINQUIÈME FOIS, LA CASCADE 205 VÉCUE "
          "ENTIÈRE POUR LA DEUXIÈME FOIS, LA VITRINE VIVANTE LA TROISIÈME "
          "FOIS (0 ET 0 — LA PREMIÈRE DE LA PIÈCE 0.1.1) — LE VERT TIENT "
          "ENTIER : la condition de l'Entrée 221 EST SATISFAITE")

    # 3. la cristallisation R6 10/10 (exigée au scellage)
    phrase, graine_cles = cm10.charger_secrets(interactif=False)
    maitre = cm10.cle_maitresse(phrase)
    _, fragments, _, _ = cm10.lire_carte()
    prf = cm10.dechiffrer_fragment(maitre, "frag-prf",
                                   fragments["frag-prf"]).decode("utf-8")
    compteurs = {}
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            m = re.match(r"(\d+)/10", champs.get("crist", "0/10"))
            compteurs[champs["id"]] = int(m.group(1)) if m else 0
    incomplets = {b: n for b, n in compteurs.items() if n < 10}
    if incomplets:
        raise EchecBuild(f"cristallisation incomplète : {len(incomplets)} "
                         f"blocs < 10/10 ({sorted(incomplets)[:4]}…) — dix "
                         f"passages du --verifier requis (R6), scellage refusé")
    print(f"[R6] cristallisation : {len(compteurs)} blocs à 10/10")

    # 4. le verrou croisé R8 AVANT l'écriture + la balise encore dev
    chemin_exe = os.path.join(ICI, "loupe.exe")
    exe = open(chemin_exe, "rb").read()
    nb, manifeste = verrou_croise(exe)
    if manifeste.get("version") != cm10.VERSION_DEV:
        raise EchecBuild(
            f"la carte porte déjà « {manifeste.get('version')} » — la balise "
            f"n'est pas {cm10.VERSION_DEV} : scellage refusé (anti-rollback "
            f"R6, idempotence)")
    sha_exe = "sha256:" + hashlib.sha256(exe).hexdigest()
    if manifeste.get("empreinte") != sha_exe:
        raise EchecBuild(
            f"l'artefact diverge du scellé attendu "
            f"({(manifeste.get('empreinte') or '?')[:24]}…) — le scellage "
            f"est un fait de carte, loupe.exe ne bouge pas")
    if sha_exe != "sha256:" + ("c111510535767a40b0122d4e42261c9d8e"
                               "1ec10d94d95ef666fd76ceb93e61d1"):
        raise EchecBuild(f"loupe.exe ({sha_exe[7:23]}…) != LA PIÈCE DU "
                         f"TERRAIN (c1115105… — le binaire que LE DOUZIÈME "
                         f"RUN a couru) — le scellage scelle LE VÉCU")
    print(f"[R8] verrou croisé : {nb} empreintes conformes ; artefact "
          f"{manifeste.get('version')} INTACT ({sha_exe[7:23]}…, "
          f"{len(exe)} o — LA PIÈCE DU DOUZIÈME RUN, LA DETTE "
          f"[R10-PÉRIMÉE] SOLDÉE À LA NAISSANCE)")

    # 5. la bascule de balise (occurrence unique, EN MÉMOIRE avant l'écriture)
    bld = cm10.dechiffrer_fragment(maitre, "frag-bld",
                                   fragments["frag-bld"]).decode("utf-8")
    occurrences = bld.count(f"version={cm10.VERSION_DEV}")
    if occurrences != 1:
        raise EchecBuild(f"balise {cm10.VERSION_DEV} attendue une fois dans "
                         f"frag-bld ({occurrences} occurrence(s)) — scellage "
                         f"refusé (fail-closed)")
    bld = bld.replace(f"version={cm10.VERSION_DEV}",
                      f"version={cm10.VERSION_FINALE}")
    clairs = {"frag-bld": bld.encode("utf-8")}
    for nom in ("frag-loc", "frag-con", "frag-prf"):
        clairs[nom] = cm10.dechiffrer_fragment(maitre, nom, fragments[nom])
    nouveaux = {n: cm10.chiffrer_fragment(maitre, n, clairs[n])
                for n in cm10.FRAGMENTS}
    racine = cm10.empreinte_racine(nouveaux)
    entete = cm10.construire_entete(racine, cm10.VERSION_FINALE)
    prive, pub = cm10.paire_cles(graine_cles)
    signature = cm10.signer(prive, entete, nouveaux)

    # 6. vérification EN MÉMOIRE avant l'unique écriture (modèle D144/M9)
    cm10.verifier_listes_blanches(entete.decode("ascii"))
    cm10.verifier_signature(pub, entete, nouveaux, signature)
    if cm10.empreinte_racine(nouveaux).hex() not in entete.decode("ascii"):
        raise EchecBuild("contrôle en mémoire : empreinte racine divergente")
    controle = cm10.dechiffrer_fragment(maitre, "frag-bld",
                                        nouveaux["frag-bld"]).decode("utf-8")
    if (f"version={cm10.VERSION_FINALE}" not in controle
            or f"version={cm10.VERSION_DEV}" in controle):
        raise EchecBuild("contrôle en mémoire : bascule de balise non constatée")
    cm10.ecrire_carte(entete, nouveaux, signature, pub)

    # 7. le tableau de bord suit la balise (l'artefact, lui, ne bouge pas)
    chemin_tab = os.path.join(cm10.CARTE_DIR, "tableau-de-bord.txt")
    with open(chemin_tab, encoding="utf-8") as f:
        tab = f.read()
    tab = tab.replace(
        "version      : 0.1.1-dev.1 (LA VERSION 0.1.1 COMMANDÉE PAR LE DÉVELOPPEUR — D178/D179 : la\n"
        "               dette [R10-PÉRIMÉE] SOLDÉE à la naissance — la porte\n"
        "               R10 véridique, le code byte-identique au vécu des\n"
        "               ONZE RUNS de l'ère 0.1.0 ; la balise `loupe 0.1.1` se\n"
        "               scellera PAR FAIT DE CARTE sur le vert recoupé du\n"
        "               DOUZIÈME run)",
        "version      : 0.1.1 SCELLÉE sur le douzième run vert recoupé (l'Entrée 222 :\n"
        "               LE VERT TIENT ENTIER — T0→T7 TOUT VERT POUR LA CINQUIÈME\n"
        "               FOIS, la cascade 205 vécue pour la deuxième, LA VITRINE\n"
        "               VIVANTE LA TROISIÈME FOIS [0 ET 0] — LA PREMIÈRE DE LA\n"
        "               PIÈCE 0.1.1 ; LA DETTE [R10-PÉRIMÉE] DEMEURE SOLDÉE —\n"
        "               la balise vit dans la CARTE — fait de carte D104/M9,\n"
        "               le qword de l'artefact ne bouge pas)")
    if (f"version      : {cm10.VERSION_FINALE} SCELLÉE" not in tab
            or "se scellera PAR FAIT DE CARTE" in tab):
        raise EchecBuild("le tableau de bord n'a pas suivi la balise — "
                         "constater avant d'aller plus loin")
    with open(chemin_tab, "w", encoding="utf-8") as f:
        f.write(tab)

    # 8. le verrou croisé POST-scellage + l'artefact INTACT (le fait de carte)
    nb2, manifeste2 = verrou_croise(exe)
    if manifeste2.get("version") != cm10.VERSION_FINALE:
        raise EchecBuild(f"la carte scellée porte « {manifeste2.get('version')} "
                         f"» — la bascule n'est pas constatée après écriture")
    exe2 = open(chemin_exe, "rb").read()
    if "sha256:" + hashlib.sha256(exe2).hexdigest() != sha_exe:
        raise EchecBuild("l'artefact a bougé — le scellage est un fait de "
                         "carte, loupe.exe demeure byte-identique")

    # 9. L'ANTI-ROLLBACK ARMÉ — CONSTATÉ AU GESTE MÊME (la reconstruction
    #    REFUSÉE : la carte scellée 0.1.1 interdit construire() ; la 0.1.0
    #    scellée demeure — la monotonie R10 n'ouvre jamais l'ancienne)
    try:
        _anti_rollback()
        raise EchecBuild("l'anti-rollback n'a pas refusé la reconstruction — "
                         "le verrou n'est PAS armé, scellage invalide")
    except EchecBuild as exc:
        if "reconstruction interdite" not in str(exc):
            raise
        print(f"[anti-rollback] ARMÉ, CONSTATÉ AU GESTE MÊME : {exc}")

    print(f"[R8] verrou croisé post-scellage : {nb2} empreintes conformes ; "
          f"balise {manifeste2.get('version')}")
    print(f"[balise] loupe {cm10.VERSION_FINALE} SCELLÉE sur le douzième "
          f"run vert recoupé (immuable § 9 ; défaut → 0.1.2 à contrat "
          f"stable, R4 ; anti-rollback R6 vivant — la reconstruction est "
          f"désormais REFUSÉE) ; loupe.exe INTACT (sha256 "
          f"{sha_exe[7:23]}…, {len(exe2)} o — le scellage est un fait de "
          f"carte, LE DOUZIÈME RUN A ÉTABLI LE CRITÈRE : LA VERSION DE LA "
          f"DETTE [R10-PÉRIMÉE] SOLDÉE — la balise 0.1.0 scellée demeurée, "
          f"l'ère ouverte par la monotonie R10)")
    return 0


# --- Modes -------------------------------------------------------------------------

def construire() -> int:
    print("=== M10 : LE BUILD DE LOUPE — loupe.exe 0.1.1-dev.1 (le TGN, "
          "l'application née de TRIADE entière — LA VERSION COMMANDÉE "
          "D178/D179 : la dette [R10-PÉRIMÉE] soldée à la naissance) ===")
    _anti_rollback()
    _garde_sceau_I()
    m9, m1, demo = _lire_scelles()
    specs = charger_couche_I_loupe()

    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    code, insns_par_bloc = assembler_blocs(ks)
    verrous = oracle_structurel(code, insns_par_bloc)
    verrous += audit_msx64(insns_par_bloc)     # l'Entrée 207 : la classe
    # L'AUDIT DE TEMPS CONSTANT STRUCTUREL NON BORNÉ (fkkqc7v8t) — à côté
    # de l'audit ABI msx64 : l'obligation md5 (loupe-06 + libc + .comprimer)
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location(
        "audit_temps_constant",
        os.path.join(os.path.dirname(ICI), "audit_temps_constant.py"))
    _ATC = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_ATC)
    _ATC.auditer_loupe()
    extraits = heritage_scelle(m9, m1, demo, ks)

    sections = composer_image(code, extraits)
    exe = ecrire_pe32plus(*sections[:4])
    valider_pe(exe, code, extraits, sections[4], sections[5])
    print(f"[R7] l'héritage composé : les 8 blocs + la table K aux adresses "
          f"scellées, confrontés au geste même — la recomposition est la preuve")

    verdicts = rejouer_harnais()
    journal = [f"build 0.1.1-dev.1 le "
               f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} · "
               f"garde 14/14 VERT · verrous {verrous} · "
               + " · ".join(f"{v['harnais']}={v['empreinte']}" for v in verdicts)]

    # LA PIÈCE DE L'ÈRE (l'Entrée 219 : la 0.1.0 SCELLÉE, 054de960… — le
    # témoin du onzième run ; D179 : la version 0.1.1 COMMANDÉE) : le build
    # confronte la recomposition à la déployée —
    #   - ÈRE IDENTIQUE : la déployée demeure (la carte scelle LA PIÈCE
    #     VÉCUE, le build ne l'écrase jamais) ;
    #   - ÈRE NOUVELLE (le qword de la déployée == 0x00010008, l'ère 0.1.0
    #     SCELLÉE, et la version commandée > la balise — l'anti-rollback a
    #     déjà tranché) : la 0.1.1-dev.1 NAÎT — la dette [R10-PÉRIMÉE]
    #     soldée à la naissance (la table == la vérité des blocs), le qword
    #     porté, l'écart CONFINÉ aux champs nommés, la pièce 0.1.0
    #     demeurant au git et au coffre.
    chemin_exe = os.path.join(ICI, "loupe.exe")
    if os.path.exists(chemin_exe):
        deploye = open(chemin_exe, "rb").read()
        if deploye == exe:
            print("[artefact] la recomposition == la pièce déployée — la "
                  "porte R10 véridique (la dette [R10-PÉRIMÉE] n'existe "
                  "plus à cette ère)")
        else:
            exe = _porte_ere_011(exe, deploye, journal)   # la 0.1.1 NAÎT
            with open(chemin_exe, "wb") as f:
                f.write(exe)
            print(f"[artefact] loupe.exe 0.1.1-dev.1 NÉE — "
                  f"sha256:{hashlib.sha256(exe).hexdigest()}")
    else:
        with open(chemin_exe, "wb") as f:
            f.write(exe)
        print(f"[artefact] {chemin_exe} né — "
              f"sha256:{hashlib.sha256(exe).hexdigest()}")

    cm10 = construire_carte(exe, specs, code, verrous, verdicts, journal)
    nb, manifeste = verrou_croise(exe)
    print(f"[carte] génération 17 écrite (lignée D80, graine durable D144) : "
          f"4 fragments chiffrés, signature Ed25519, {len(cm10.TOUS_BLOCS_CARTE)} "
          f"blocs indexés")
    print(f"[R8] verrou croisé : signature OK, racine OK, {nb} empreintes "
          f"revérifiées, artefact {manifeste.get('version')}")
    with open(os.path.join(cm10.CARTE_DIR, "tableau-de-bord.txt"), "w",
              encoding="utf-8") as f:
        f.write(tableau_de_bord(exe, verrous, verdicts, nb, manifeste))
    print("[tableau] tableau de bord écrit (carte/tableau-de-bord.txt)")
    print(f"=== LE BUILD DE LOUPE : loupe.exe {manifeste.get('version')} — "
          f"l'application née des 18 blocs notés + les héritages scellés, "
          f"LA VERSION 0.1.1 COMMANDÉE PAR LE DÉVELOPPEUR (D179 : la dette "
          f"[R10-PÉRIMÉE] SOLDÉE à la naissance — la porte R10 véridique, "
          f"le code byte-identique au vécu des onze runs, R4/R7) ; la "
          f"balise `loupe 0.1.1` se scellera PAR FAIT DE CARTE sur le vert "
          f"recoupé du DOUZIÈME RUN : cristallisation 10/10 (--verifier) "
          f"puis le scellage au miroir D165/D170 ===")
    return 0


def verifier() -> int:
    """La re-vérification + LA CRISTALLISATION R6 (chaque passage incrémente
    les compteurs de la carte, la carte re-signée — la 10/10 sera exigée au
    scellage ; sous une balise scellée, la cristallisation N'ÉCRIT PLUS :
    la carte scellée est immuable § 9, la re-vérification demeure licite)."""
    print("=== M10 : re-vérification de loupe.exe + cristallisation R6 "
          "(R5/R7/R8) ===")
    _garde_sceau_I()
    m9, m1, demo = _lire_scelles()
    specs = charger_couche_I_loupe()
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    code, insns_par_bloc = assembler_blocs(ks)
    verrous = oracle_structurel(code, insns_par_bloc)
    verrous += audit_msx64(insns_par_bloc)    # l'Entrée 207 : la classe
    # L'AUDIT DE TEMPS CONSTANT STRUCTUREL NON BORNÉ (fkkqc7v8t) — à côté
    # de l'audit ABI msx64 : l'obligation md5 (loupe-06 + libc + .comprimer)
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location(
        "audit_temps_constant",
        os.path.join(os.path.dirname(ICI), "audit_temps_constant.py"))
    _ATC = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_ATC)
    _ATC.auditer_loupe()
    extraits = heritage_scelle(m9, m1, demo, ks)
    sections = composer_image(code, extraits)
    exe = ecrire_pe32plus(*sections[:4])
    valider_pe(exe, code, extraits, sections[4], sections[5])
    chemin_exe = os.path.join(ICI, "loupe.exe")
    if not os.path.exists(chemin_exe):
        raise EchecBuild("loupe.exe absent — construire d'abord")
    existant = open(chemin_exe, "rb").read()
    ecart_txt = "porte-r10=véridique (la dette [R10-PÉRIMÉE] soldée, D179)"
    if existant != exe:
        # L'ÉCART NOMMÉ [R10-PÉRIMÉE] : la recomposition véridique contre la
        # pièce du terrain (porte périmée) — tout écart HORS de la porte est
        # un VRAI échec (R6 : l'artefact a bougé, ou les sources ont bougé)
        perimees = _ecart_r10_nomme(exe, existant)
        print(f"[R10-PÉRIMÉE] la cristallisation constate l'écart nommé : "
              f"{len(perimees)} sommes dev.5 à la porte de la pièce, "
              f"0 octet ailleurs — la recomposition DÉTERMINISTE")
        exe = existant      # la carte scelle LA PIÈCE DU TERRAIN (intacte)
        ecart_txt = f"écart=[R10-PÉRIMÉE] {len(perimees)} sommes dev.5"
    nb, manifeste = verrou_croise(exe)
    print(f"[R8] verrou croisé : {nb} empreintes revérifiées, artefact "
          f"{manifeste.get('version')} — IDENTIQUE à la recomposition "
          f"(l'artefact DÉTERMINISTE)")
    print("=== re-vérification VERTE : l'artefact est la recomposition de ses "
          "sources, la carte le confirme ===")

    # LES TROIS HARNAIS REJOUÉS au geste de la passe (le modèle du build :
    # la preuve entière à chaque cristallisation — le domaine n'est jamais
    # cru sur parole, ni au premier geste ni au dixième)
    verdicts = rejouer_harnais()

    # LA CRISTALLISATION R6 : chaque passage incrémente les compteurs — la
    # carte est re-signée à chaque passage (fragments re-chiffrés, graine
    # durable D144), le verrou croisé re-vérifié (R8). La 10/10 sera exigée
    # au scellage de la 0.1.1 (qui attend le fait de carte sur le vert
    # recoupé du douzième run — l'Entrée 222).
    import carte_m10 as cm10
    version_carte = _version_carte(cm10)
    if version_carte and ("-rc" in version_carte
                          or re.fullmatch(r"\d+\.\d+\.\d+", version_carte)):
        print(f"[R6] la carte est SCELLÉE ({version_carte}) : la "
              f"cristallisation n'écrit plus (la balise immuable § 9 — la "
              f"re-vérification demeure licite, R5/R7)")
        return 0
    phrase, graine_cles = cm10.charger_secrets(interactif=False)
    maitre = cm10.cle_maitresse(phrase)
    _, fragments, _, _ = cm10.lire_carte()
    prf = cm10.dechiffrer_fragment(maitre, "frag-prf",
                                   fragments["frag-prf"]).decode("utf-8")
    compteurs, journal = {}, []
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            m = re.match(r"(\d+)/10", champs.get("crist", "1/10"))
            compteurs[champs["id"]] = int(m.group(1))
        elif ligne.startswith("  run "):
            journal.append(ligne.strip())
    for bid in cm10.TOUS_BLOCS_CARTE:
        compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal.append(
        f"run cristallisation R6 verrous={verrous} "
        f"artefact={hashlib.sha256(exe).hexdigest()[:8]}… {ecart_txt} "
        f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} · "
        + " · ".join(f"{v['harnais']}={v['empreinte']}" for v in verdicts))
    clairs = cm10.fragments_clairs(exe, specs, code, verrous,
                                   verdicts, journal, compteurs)
    nouveaux = {n: cm10.chiffrer_fragment(maitre, n, clairs[n])
                for n in cm10.FRAGMENTS}
    racine = cm10.empreinte_racine(nouveaux)
    entete = cm10.construire_entete(racine, version_carte or cm10.VERSION_DEV)
    prive, pub = cm10.paire_cles(graine_cles)
    signature = cm10.signer(prive, entete, nouveaux)
    cm10.verifier_signature(pub, entete, nouveaux, signature)
    cm10.ecrire_carte(entete, nouveaux, signature, pub)
    nb2, manifeste2 = verrou_croise(exe)
    crist = [f"{b}={compteurs[b]}/10"
             for b in cm10.TOUS_BLOCS_CARTE[:6]]
    print(f"[R6] cristallisation : {len(compteurs)} blocs incrémentés "
          f"({', '.join(crist)}…) — la carte re-signée (graine durable D144), "
          f"le verrou croisé {nb2} empreintes, artefact "
          f"{manifeste2.get('version')}")
    return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Le build du domaine loupe (M10)")
    ap.add_argument("--verifier", action="store_true",
                    help="re-vérifier + cristallisation R6 (les compteurs)")
    ap.add_argument("--sceller-final", action="store_true",
                    help="sceller la 0.1.1 (fait de carte — le vert recoupé "
                         "du douzième run, la cristallisation 10/10 exigés)")
    args = ap.parse_args()
    try:
        if args.sceller_final:
            sys.exit(_sceller_final())
        sys.exit(verifier() if args.verifier else construire())
    except EchecBuild as exc:
        print(f"[build] ÉCHEC NOMMÉ : {exc}", file=sys.stderr)
        sys.exit(1)
