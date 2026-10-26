"""layout.py — Plan d'adressage du jalon démo TRIADE (profil x86-64-win11-pe).

Source unique de vérité partagée par build_demo.py, outils/auteur.py et
oracle_demo.py. Toute adresse de demo.exe dérive d'ici.

HÉRITAGE M2 (R7 — jamais déplacé) : les blocs scellés embarqués vivent à leurs
adresses historiques, octets identiques à echo.exe 0.3.0-rc.2 :
  - io M0 @ 0x1040/0x1080, libc M1 @ 0x1100-0x12FF ;
  - tcp-01..09 + tcp-11 en .text2 @ 0x4000-0x4BFF, écho cible @ 0x4600,
    croissance @ 0x4680 (int3 dans l'image), staging echo-01:R2 @ 0x23D0 ;
  - l'IAT kernel32 @ 0x20B0 (trois premiers slots GSH/WF/EP, ordre M0) et
    l'IAT ws2_32 @ 0x2300 (correctif D35 : FT = slots appelés) sont FIGÉS :
    des octets de code scellé y pointent ;
  - état serveur .data : stdout 0x3800, stdin 0x3808, listen 0x3810, quit
    0x3818, etat_patch 0x3820, entree_sauvee 0x3828, CS 0x3830 ;
  - la table R10 @ 0x2450 garde son entrée 0 = staging (lue par tcp-07).

NOUVEAUTÉS DÉMO (génération 4, d4xxxx) :
  - neuf blocs win-01..win-09 en .text @ 0x1400-0x1FBF (les slots libres de
    echo.exe : libc-05/06/07, libc-09 et tcp-12 n'y sont PAS embarqués) ;
    le point d'entrée devient win-01 @ 0x1400, sous-système WINDOWS_GUI (2) ;
  - imports étendus : user32.dll ×14 (FT 0x2800) et gdi32.dll ×1 (FT 0x2970),
    kernel32 +GetModuleHandleW (slot 0x2100), ws2_32 +connect (slot 0x2350) ;
    le marché des descripteurs s'étend en place (k32 0x2030, ws2 0x2044,
    user32 0x2058, gdi32 0x206C, terminateur 0x2080), ce qui déménage les
    données pures gênantes (nom kernel32, hints GSH/WF/EP -> 0x21F0-0x2216,
    noms dll -> 0x2218/0x2225, hints nouveaux GMH/connect -> 0x22A0/0x22B3) :
    aucun octet de code ne référence ces données (relocations documentées,
    sans effet R7) ;
  - l'état GUI vit en .data @ 0x3860+ (hwnd principal/journal/bouton,
    drapeaux worker et serveur) ;
  - chaînes UTF-16 statiques (classe, titre, libellés, journal 16 lignes) en
    fin de .rdata @ 0x29B0+, fixtures ASCII win-06 @ 0x2620, phrases
    d'échange @ 0x26E8 ; les chaînes tcp-09 ("echo ", CRLF, "fin connexion")
    restent à leurs adresses scellées.
"""

import importlib.util
import os
import sys

_CHEMIN_M2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "m2", "layout.py")
_spec = importlib.util.spec_from_file_location("layout_m2", _CHEMIN_M2)
L2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L2)   # noqa: E402 — plan M2 (héritage)

# --- Image et sections (identiques à echo.exe, D28/D33) ------------------------

IMAGE_BASE = L2.IMAGE_BASE
TEXT_RVA, RDATA_RVA, DATA_RVA = L2.TEXT_RVA, L2.RDATA_RVA, L2.DATA_RVA
TEXT2_RVA = L2.TEXT2_RVA
FILE_ALIGN, SECT_ALIGN = L2.FILE_ALIGN, L2.SECT_ALIGN
TEXT_VSIZE, RDATA_VSIZE, DATA_VSIZE, TEXT2_VSIZE = (L2.TEXT_VSIZE, L2.RDATA_VSIZE,
                                                    L2.DATA_VSIZE, L2.TEXT2_VSIZE)
SIZE_OF_IMAGE = L2.SIZE_OF_IMAGE
TEXT_FILE, RDATA_FILE, DATA_FILE, TEXT2_FILE = (L2.TEXT_FILE, L2.RDATA_FILE,
                                                L2.DATA_FILE, L2.TEXT2_FILE)
DATA_RAW = L2.DATA_RAW
TAILLE_FICHIER = L2.TAILLE_FICHIER
DLL_CHARACTERISTICS = L2.DLL_CHARACTERISTICS

VERSION_DEMO1 = "0.3.0-demo.1"     # première génération de la lignée démo
VERSION_U64_DEMO1 = 0x00030101     # monotonie : au-dessus de la lignée echo
VERSION_U64_MIN = 0x00030000       # plancher de la porte R10 (hérité M2)

SUBSYSTEM_GUI = 2                  # WINDOWS_GUI (tcp-12 était CONSOLE)

# --- Blocs de la lignée démo (couche C, génération 4) ---------------------------
# d4xxxx = démo. Tous les slots multiples de 64 (D8), alignés 16, padding >= 16.

BLOCS_WIN = [
    ("d40001", "win-01:R1", 0x1400, 0x40, "demo.1", 1),    # principal — point d'entrée
    ("d40002", "win-02:R1", 0x1440, 0x140, "demo.1", 1),   # fenêtre (classe + création)
    ("d40003", "win-03:R1", 0x1580, 0x80, "demo.1", 1),    # boucle de messages
    ("d40004", "win-04:R1", 0x1600, 0x2C0, "demo.1", 1),   # procédure de fenêtre
    ("d40005", "win-05:R1", 0x18C0, 0x80, "demo.1", 1),    # journal graphique
    ("d40006", "win-06:R1", 0x1940, 0x180, "demo.1", 1),   # autotest (porte R10 + libc)
    ("d40007", "win-07:R1", 0x1AC0, 0xC0, "demo.1", 1),    # client TCP
    ("d40008", "win-08:R1", 0x1B80, 0x100, "demo.1", 1),   # serveur d'acceptation
    ("d40009", "win-09:R1", 0x1C80, 0x380, "demo.1", 1),   # scénario complet
    ("d40010", "win-10:R1", 0x4980, 0x180, "demo.1", 1),   # échange vérifié (slot tcp-10 libre)
]
ENTREE = 0x1400    # AddressOfEntryPoint = win-01

# Héritage embarqué octet-identique (vérifié contre hello.exe / selftest.exe /
# echo.exe 0.3.0-rc.2 à chaque construction — R7) :
#   a10002/a10003 (io M0), b20001-b20004 (libc M1),
#   c30001-c30009 (tcp-01..09), c30011 (tcp-11) — tcp-10 et tcp-12 NON embarqués
#   (console et point d'entrée console : remplacés par win-04/win-01).
#   c30014 (staging echo-01:R2) embarqué en .rdata @ 0x23D0 (donnée).

# --- .rdata : structures PE (héritage + extension démo) --------------------------

R_DESC_IMPORT = 0x2030      # descripteur kernel32 (FT figée 0x20B0)
R_DESC_WS2 = 0x2044         # descripteur ws2_32 (FT 0x2300 — correctif D35)
R_DESC_USER32 = 0x2058      # descripteur user32 (MARCHÉ ÉTENDU : k32, ws2,
R_DESC_GDI32 = 0x206C       #   user32, gdi32, terminateur 0x2080 — contigu)
R_DESC_TERM = 0x2080
R_HN_GSH, R_HN_WF, R_HN_EP = 0x21F4, 0x2203, 0x220F   # hints M0 déménagés
                            # (0x2079-0x20A0 -> zone 0x21F0, données pures :
                            # le marché s'étend en place, relocation documentée)
R_NOM_DLL = 0x2220          # "kernel32.dll\0" (déménagé de 0x206C)
R_NOM_WS2 = 0x222E          # "ws2_32.dll\0" (déménagé de 0x20A4)
R_IAT = 0x20B0              # IAT kernel32 SCELLÉE (11 slots : 10 M2 + GMH)
R_INT_KERNEL32 = 0x2110     # INT kernel32 (12 qwords : 11 + terme)
R_HN_CT = 0x2170            # hints kernel32 M2 (inchangés)
R_HN_VP = 0x217F
R_HN_ICS = 0x2190
R_HN_ECS = 0x21AC
R_HN_LCS = 0x21C3
R_HN_RF = 0x21DA
R_HN_CH = 0x21E5
R_HN_GMH = 0x22A0           # hint GetModuleHandleW (nouveau, zone 0x22A0 —
                            # l'ancienne pré-IAT ws2 morte de rc.1)
R_HN_CONNECT = 0x22B3       # hint connect (nouveau)
R_INT_WS2 = 0x2240          # INT ws2_32 (12 qwords : 11 + terme)
R_IAT_WS2 = 0x2300          # IAT ws2_32 (FT = slots appelés, D35) — 11 slots
R_HN_WS2 = 0x2360           # hints ws2_32 hérités (10 entrées, fix rc.2)
R_STAGING = 0x23D0          # staging echo-01:R2 (128 o) — tcp-07 le vérifie
R_TAB_SUM = 0x2450          # porte R10 : entrée 0 = staging (figée, tcp-07)
R_VERSION = 0x2610          # qword version (R10, monotonie) — déplacé de
                            # 0x2600 : la table R10 (28 entrées) finit à 0x2610
R_ANCRE = 0x2620            # ancre de base (PI, D33) — suit la version
R_FIXTURES = 0x2630         # fixtures ASCII win-06 (45 o)
R_MSG_CRLF = 0x2665         # "\r\n" — chaîne tcp-09 scellée (adresse figée)
R_MSG_ECHO = 0x2668         # "echo " — chaîne tcp-09 scellée
R_MSG_FIN = 0x26D8          # "fin connexion" — chaîne tcp-09 scellée
R_PHRASE = 0x26E8           # "salut triade\r\n" (14 o, échange réseau)
R_PHRASE_MAJ = 0x26F6       # "SALUT TRIADE\r\n" (14 o, attendu v2)
R_RELOC = 0x2760            # BASERELOC minimal (12 o)
R_INT_USER32 = 0x2780       # INT user32 (15 qwords : 14 + terme)
R_IAT_USER32 = 0x2800       # IAT user32 (FT — 14 slots)
R_HN_USER32 = 0x2880        # hints user32 (14 entrées, ~222 o)
R_INT_GDI32 = 0x2970        # INT gdi32 (2 qwords)
R_IAT_GDI32 = 0x2980        # IAT gdi32 (FT — 1 slot)
R_HN_GDI32 = 0x2990         # hint GetStockObject
R_NOM_USER32 = 0x29A8       # "user32.dll\0"
R_NOM_GDI32 = 0x29B3        # "gdi32.dll\0"
R_UTF16 = 0x29C0            # chaînes UTF-16 (classe, titre, libellés, journal)

IAT_SLOTS = dict(L2.IAT_SLOTS) | {
    "GetModuleHandleW": 0x2100,
    "connect": 0x2350,
    "RegisterClassExW": 0x2800, "CreateWindowExW": 0x2808,
    "DefWindowProcW": 0x2810, "GetMessageW": 0x2818,
    "TranslateMessage": 0x2820, "DispatchMessageW": 0x2828,
    "PostQuitMessage": 0x2830, "DestroyWindow": 0x2838,
    "SendMessageW": 0x2840, "LoadCursorW": 0x2848,
    "EnableWindow": 0x2850, "MoveWindow": 0x2858,
    "GetClientRect": 0x2860, "MessageBoxW": 0x2868,
    "GetStockObject": 0x2980,
}
KERNEL32_IMPORTS = list(L2.KERNEL32_IMPORTS) + ["GetModuleHandleW"]
WS2_IMPORTS = list(L2.WS2_IMPORTS) + ["connect"]
USER32_IMPORTS = ["RegisterClassExW", "CreateWindowExW", "DefWindowProcW",
                  "GetMessageW", "TranslateMessage", "DispatchMessageW",
                  "PostQuitMessage", "DestroyWindow", "SendMessageW",
                  "LoadCursorW", "EnableWindow", "MoveWindow", "GetClientRect",
                  "MessageBoxW"]
GDI32_IMPORTS = ["GetStockObject"]

# --- .data : état GUI (au-delà de l'état serveur hérité) -------------------------

R_STDOUT, R_STDIN, R_LISTEN, R_QUIT = L2.R_STDOUT, L2.R_STDIN, L2.R_LISTEN, L2.R_QUIT
R_ETAT_PATCH, R_ENTREE_SAUVEE, R_CS = L2.R_ETAT_PATCH, L2.R_ENTREE_SAUVEE, L2.R_CS
R_CURSEUR, ARENE_BASE = L2.R_CURSEUR, L2.ARENE_BASE

HWND_PRINCIPAL = 0x3860     # handle de la fenêtre principale (win-02)
HWND_JOURNAL = 0x3868       # handle du contrôle EDIT journal (win-04)
HWND_BOUTON = 0x3870        # handle du bouton unique (win-04)
DRAPEAU_WORKER = 0x3878     # 0 = scénario non lancé, 1 = lancé (clic unique)
DRAPEAU_SRV = 0x3880        # 0 = inconnu, 1 = écoute prête, 2 = échec (win-08)

# --- Chaînes TCP héritées (adresses figées par tcp-09 scellé) -------------------

MSG_ECHO = b"echo "
MSG_CRLF = b"\r\n"
MSG_FIN = b"fin connexion\r\n"
PHRASE = b"salut triade\r\n"
PHRASE_MAJ = b"SALUT TRIADE\r\n"
FIXTURE_MEMCPY = b"TRIADE-M2-DEMO!!"          # 16 o @ 0x2630
FIXTURE_MEMCMP_A = b"aaa\x00abc\x00aab\x00"    # 12 o @ 0x2640
FIXTURE_STRLEN = b"porte-libc-ok\x00"          # 13 chars + NUL @ 0x264C
FIXTURE_ITOA = b"25000\x00"                    # 5 chars + NUL @ 0x265A

# --- Chaînes UTF-16 statiques (GUI + journal) : pose séquentielle @ 0x29B0 ------
# Chaque entrée : nom -> (adresse, texte, nchars). Le NUL final est posé mais
# non compté (win-05 affiche exactement nchars). Ordre = ordre de pose.

_SEQ_UTF16 = [
    ("CLASSE", "TRIADE_demo"),
    ("TITRE", "TRIADE M2 — démonstration complète"),
    ("TXT_BOUTON", "TOUT DÉMARRER"),
    ("CLASSE_EDIT", "EDIT"),
    ("CLASSE_BOUTON", "BUTTON"),
    ("CHAINE_VIDE", ""),
    ("MSG_ECHEC_GUI", "création de fenêtre impossible"),
    ("J_ENTETE", "TRIADE M2 — démonstration\r\n"),
    ("J_PROTO", "I → B → C, zéro compilateur\r\n"),
    ("J_PORTE_OK", "porte R10 : intégrité VERTE\r\n"),
    ("J_PORTE_KO", "porte R10 : KO — arrêt\r\n"),
    ("J_LIBC_OK", "libc M1 scellée : 4/4 verts\r\n"),
    ("J_LIBC_KO", "libc : vecteur en échec\r\n"),
    ("J_MEC_OK", "mécanique : v1→v2→v1 confirmés\r\n"),
    ("J_SRV_OK", "serveur : écoute 127.0.0.1:25000\r\n"),
    ("J_SRV_KO", "port 25000 occupé — fermez echo.exe\r\n"),
    ("J_CLI_OK", "client : connecté\r\n"),
    ("J_ECHO_OK", "écho réseau : aller-retour exact\r\n"),
    ("J_PROD_OK", "patch en production : MAJUSCULES\r\n"),
    ("J_RB_OK", "retour arrière : identité confirmée\r\n"),
    ("J_FINAL", "boucle § 5 complète — DÉMO OK\r\n"),
    ("J_RESEAU_KO", "réseau : échange en échec\r\n"),
    ("J_DEF_KO", "défaillance inattendue — arrêt\r\n"),
]

CHAINES_UTF16 = {}
_cur = R_UTF16
for _nom, _texte in _SEQ_UTF16:
    CHAINES_UTF16[_nom] = (_cur, _texte, len(_texte))
    _cur += 2 * (len(_texte) + 1)          # chars UTF-16 + NUL
FIN_UTF16 = _cur
assert FIN_UTF16 <= RDATA_RVA + RDATA_VSIZE, "zone UTF-16 débordante"

ECHO_ENTREE = L2.ECHO_ENTREE            # 0x4600 — cible du patch (héritage)
ECHO_CROISSANCE = L2.ECHO_CROISSANCE    # 0x4680 — zone de croissance

# --- Jetons de retour d'émulation (oracle, hors binaire) ------------------------

SENTINELLE_RETOUR = L2.SENTINELLE_RETOUR

NOMS_BLOCS = dict(L2.NOMS_BLOCS) | {
    "d40001": "win-principal", "d40002": "win-fenetre", "d40003": "win-boucle",
    "d40004": "win-procedure", "d40005": "win-journal", "d40006": "win-autotest",
    "d40007": "win-client", "d40008": "win-serveur", "d40009": "win-scenario",
    "d40010": "win-echange",
}
