"""layout.py — Plan d'adressage du jalon démo TRIADE (profil x86-64-win11-pe).

Source unique de vérité partagée par build_demo.py, outils/auteur.py et
oracle_demo.py. Toute adresse de demo.exe dérive d'ici.

DÉMO.2 (D36 — trace terrain) : la génération demo.1 s'ouvrait FENÊTRE VIDE
sur le terrain réel : le gestionnaire WM_SIZE lisait RECT.top ([rsp+0x24],
toujours 0) comme largeur — contrôles invisibles (largeur -16). La spec
exigeait déjà w-16 : divergence notation/spec attrapée à l'exécution
terrain, invisible à l'oracle R1 (shim MoveWindow sans invariant).
Demo.2 corrige (win-04:R2 lit RECT.right), ajoute le journal FICHIER
(win-11:R1 — demo_journal.txt à côté de l'exe, GetLastError tracé) et
durcit l'oracle (coquille GUI exécutée, géométrie MoveWindow vérifiée,
falsification anti-régression de l'octet RECT).

DÉMO.3 (D37 — écran vivant + preuves d'exécution) : la capture terrain de
demo.2 (26/10/2026 20:56, fenêtre maximisée) montre un écran VIDE au
démarrage : les traces L00/L02/L01 appelaient win-11 EN DIRECT (fichier
seul — la spec win-02:R2 l'exigeait : « jumeau silencieux »), et l'edit est
créé avec un texte initial vide — la vitrine paraissait morte alors que le
fichier prouvait le contraire. ET le bouton « TOUT DÉMARRER » n'est pas
rendu — alors que notation, octets et oracle sont corrects (styles,
positions, cibles vérifiés par audit) : preuves d'exécution requises.
Demo.3 : win-05:R3 devient le point de passage UNIVERSEL (miroir écran
PUIS fichier, deux entrées — scénario inchangé @0x19C0, trace 4 args
@0x19C8) ; win-02:R3/win-04:R3 re-ciblent leurs traces (JOURNAL_TRACE) ;
WM_SIZE journalise les retours BOOL des MoveWindow (L4C/L4D — le bouton
sera jugé par ses retours réels au prochain run terrain).

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

NOUVEAUTÉS DÉMO (génération 4, d4xxxx) — REPORTEES DEMO.2 (win-09 déménage
en .text2, win-11 nouveau, R_VERSION 0x2610→0x2628 : la table R10 passe à
29 entrées ; R_ANCRE 0x2620 inchangé, l'ancre de win-06 reste stable) :
  - .text @ 0x1400-0x1FFF : win-01 0x1400, win-02:R3 0x1440 (slot 0x180),
    win-03 0x15C0, win-04:R3 0x1640 (slot 0x380), win-06 0x1AC0, win-07
    0x1C40, win-08 0x1D00, win-11:R1 journal-fichier 0x1E00 (slot 0x200) ;
    le slot 0x19C0-0x1ABF (win-05 R1/R2) est LIBRE depuis demo.3 ;
  - .text2 ÉTENDUE (D37) : 0x4000-0x53FF (VSIZE 0x1400, image 0x6000,
    fichier 0x4000) : héritage tcp inchangé, win-10 0x4980, win-09 0x4C00,
    win-05:R3 0x5000 (slot 0x200 — déménagé de .text : le code miroir
    universel (252 o) ne tenait ni dans son slot historique 256 o, ni dans
    la zone libre 0x4700-0x47FF ; 0x5000 est hors des pages VirtualProtect
    du patch 0x4000-0x4FFF) ; le slot .text 0x19C0-0x1ABF est LIBRE ;
  - imports kernel32#2 (descripteur 0x2080 — l'ancien terminateur, le marché
    s'étend en place ; terminateur 0x2094) : GetModuleFileNameA, CreateFileA,
    FlushFileBuffers, GetLastError — INT @ 0x2720, FT (slots appelés, D35)
    @ 0x2E80, hints dans les interstices libres 0x22C0/0x2704 ; l'IAT
    kernel32 historique 0x20B0 reste INTACTE (R7) ;
  - l'état GUI vit en .data @ 0x3860+ (hwnd principal/journal/bouton,
    drapeaux worker et serveur) ; win-11 ajoute handle 0x3888, tampon de
    conversion 0x3890 (128 o), tampon chemin 0x3910 (304 o), scratch
    écriture 0x3A40 ;
  - chaînes UTF-16 statiques (classe, titre, libellés, journal 16 lignes) en
    fin de .rdata @ 0x29B0+, chaînes ASCII de trace (L00/L01/L02/L03/LKO_*,
    nom du fichier) @ 0x2EA8+, fixtures ASCII win-06 @ 0x2630, phrases
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
# D37 — extension .text2 : win-05:R3 (337 o puis 252 o restructuré) ne tient
# ni dans son slot .text historique (0x19C0-0x1ABF, 256 o) ni dans la zone
# libre 0x4700-0x47FF : .text2 passe à 0x1400 (image 0x6000, fichier 0x4000).
# win-05 vit à 0x5000 — hors de l'étendue VirtualProtect du patch (pages
# 0x4000-0x4FFF, ETENDUE_PROTECT 0x700) : le moteur de patch ne l'atteint pas.
TEXT_VSIZE, RDATA_VSIZE, DATA_VSIZE = (L2.TEXT_VSIZE, L2.RDATA_VSIZE,
                                       L2.DATA_VSIZE)
TEXT2_VSIZE = 0x1400                     # 0x4000-0x53FF (héritage + win-05:R3)
SIZE_OF_IMAGE = 0x6000                   # aligné SectionAlignment (0x5400 -> 0x6000)
TEXT_FILE, RDATA_FILE, DATA_FILE, TEXT2_FILE = (L2.TEXT_FILE, L2.RDATA_FILE,
                                                L2.DATA_FILE, L2.TEXT2_FILE)
DATA_RAW = L2.DATA_RAW
TAILLE_FICHIER = 0x4000                   # 0x2C00 + 0x1400
DLL_CHARACTERISTICS = L2.DLL_CHARACTERISTICS

VERSION_DEMO1 = "0.3.0-demo.1"     # première génération de la lignée démo
VERSION_DEMO2 = "0.3.0-demo.2"     # D36 : correctif WM_SIZE + journal fichier
VERSION_U64_DEMO2 = 0x00030102     # monotonie : au-dessus de demo.1
VERSION_DEMO3 = "0.3.0-demo.3"     # D37 : miroir écran universel + L4C/L4D
VERSION_U64_DEMO3 = 0x00030103     # monotonie : au-dessus de demo.2
VERSION_DEMO4 = "0.3.0-demo.4"     # D38 : w/h WM_SIZE en r14d/r15d callee-saved (bouton invisible demo.3 : r10d/r11d volatiles relus après l'appel)
VERSION_U64_DEMO4 = 0x00030104     # monotonie : au-dessus de demo.3
VERSION_DEMO5 = "0.3.0-demo.5"     # D39 : héritage tcp-07:R2 (echo 0.3.0-rc.3) —
                                   # phases d'écriture en PAGE_EXECUTE_READWRITE :
                                   # le défaut R1 (PAGE_READWRITE, sans execute)
                                   # tuait le processus au 1er VirtualProtect (DEP)
VERSION_U64_DEMO5 = 0x00030105     # monotonie : au-dessus de demo.4
VERSION_DEMO6 = "0.3.0-demo.6"     # D40 : instrumentation mécanique — le journal
                                   # terrain demo.5 gèle ENCORE après J_LIBC_OK
                                   # malgré le correctif DEP : 3 sondes de trace
                                   # encadrent la frontière mécanique (win-09:R2)
VERSION_U64_DEMO6 = 0x00030106     # monotonie : au-dessus de demo.5
VERSION_DEMO7 = "0.3.0-demo.7"     # D41 : héritage tcp-07:R3 (echo 0.3.0-rc.4) —
                                   # .protger réserve 0x28 avant l'appel IAT
                                   # (zone d'accueil ABI msx64 : le défaut démo.6
                                   # faisait sauter le ret vers rdx=0x700 — sondes
                                   # CONSERVÉES pour la lecture terrain du correctif)
VERSION_U64_DEMO7 = 0x00030107     # monotonie : au-dessus de demo.6
VERSION_DEMO8 = "0.3.0-demo.8"     # D42 : win-09:R3 initialise R_CS en tête de
                                   # scénario (le devoir de tcp-12, non embarqué :
                                   # tcp-11 exige P5 une CS initialisée — le défaut
                                   # démo.7 tuait le processus au premier échange,
                                   # EnterCriticalSection sur CS vierge) ; sondes
                                   # bilatérales S1/S2 (win-08:R2) + 4/5 (win-10:R2)
VERSION_U64_DEMO8 = 0x00030108     # monotonie : au-dessus de demo.7
VERSION_U64_MIN = 0x00030000       # plancher de la porte R10 (hérité M2)

SUBSYSTEM_GUI = 2                  # WINDOWS_GUI (tcp-12 était CONSOLE)

# --- Blocs de la lignée démo (couche C, génération 4) ---------------------------
# d4xxxx = démo. Tous les slots multiples de 64 (D8), alignés 16, padding >= 16.

BLOCS_WIN = [
    ("d40001", "win-01:R1", 0x1400, 0x40, "demo.3", 1),    # principal — point d'entrée
    ("d40002", "win-02:R3", 0x1440, 0x180, "demo.3", 1),   # fenêtre (classe + création + trace miroir)
    ("d40003", "win-03:R1", 0x15C0, 0x80, "demo.3", 1),    # boucle de messages
    ("d40004", "win-04:R4", 0x1640, 0x380, "demo.4", 1),   # procédure (RECT corrigé + miroir + L4C/L4D + D38 : w/h en callee-saved)
    ("d40005", "win-05:R3", 0x5000, 0x200, "demo.3", 1),   # miroir universel écran + fichier (.text2 étendue 0x1400 — D37 : le code R3 ne tient ni dans le slot .text 0x19C0-0x1ABF (LIBRE depuis), ni dans 0x4700-0x47FF)
    ("d40006", "win-06:R1", 0x1AC0, 0x180, "demo.3", 1),   # autotest (porte R10 + libc)
    ("d40007", "win-07:R1", 0x1C40, 0xC0, "demo.3", 1),    # client TCP
    ("d40008", "win-08:R2", 0x1D00, 0x100, "demo.8", 1),   # serveur d'acceptation — D42 : sondes S1/S2 (accept/spawn)
    ("d40011", "win-11:R1", 0x1E00, 0x200, "demo.3", 1),   # journal fichier (inchangé, D36)
    ("d40010", "win-10:R2", 0x4980, 0x180, "demo.8", 1),   # échange vérifié — D42 : sondes 4/5 (send/recv complets)
    ("d40009", "win-09:R3", 0x4C00, 0x3C0, "demo.8", 1),   # scénario complet — D40 : sondes mécanique ; D42 : init R_CS (devoir tcp-12)
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
R_DESC_GDI32 = 0x206C       #   user32, gdi32 — contigu)
R_DESC_K32B = 0x2080        # descripteur kernel32#2 (D36 : imports du journal
                            #   fichier — l'ancien terminateur, marché en place)
R_DESC_TERM = 0x2094        # terminateur (déménagé de 0x2080)
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
R_VERSION = 0x2628          # qword version (R10, monotonie) — déplacé de
                            # 0x2610 : la table R10 (29 entrées) finit à 0x2620
R_ANCRE = 0x2620            # ancre de base (PI, D33) — suit la table, INCHANGÉ
                            # en demo.2 (la constante de win-06 reste stable)
R_FIXTURES = 0x2630         # fixtures ASCII win-06 (45 o)
R_MSG_CRLF = 0x2665         # "\r\n" — chaîne tcp-09 scellée (adresse figée)
R_MSG_ECHO = 0x2668         # "echo " — chaîne tcp-09 scellée
R_MSG_FIN = 0x26D8          # "fin connexion" — chaîne tcp-09 scellée
R_PHRASE = 0x26E8           # "salut triade\r\n" (14 o, échange réseau)
R_PHRASE_MAJ = 0x26F6       # "SALUT TRIADE\r\n" (14 o, attendu v2)
R_RELOC = 0x2760            # BASERELOC minimal (12 o)
R_HN_K32B_CFA = 0x22C0      # hint CreateFileA (interstice libre 0x22C0-0x2300)
R_HN_K32B_GLE = 0x22CE      # hint GetLastError
R_HN_K32B_FFB = 0x22DD      # hint FlushFileBuffers
R_HN_K32B_GMFA = 0x2704      # hint GetModuleFileNameA (interstice 0x2704-0x2760)
R_INT_K32B = 0x2720          # INT kernel32#2 (5 qwords : 4 + terme)
R_IAT_K32B = 0x2E80          # IAT kernel32#2 (FT = slots appelés, D35) — 4+1
R_ASCII = 0x2EA8             # chaînes ASCII de trace (pose séquentielle)
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
    "GetModuleFileNameA": 0x2E80, "CreateFileA": 0x2E88,
    "FlushFileBuffers": 0x2E90, "GetLastError": 0x2E98,
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
KERNEL32B_IMPORTS = ["GetModuleFileNameA", "CreateFileA",
                     "FlushFileBuffers", "GetLastError"]   # descripteur #2 (D36)
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

# --- État win-11 (journal fichier, D36) ------------------------------------------

R_JOURNAL_HANDLE = 0x3888   # handle du fichier : 0 = jamais ouvert, -1 = échec
BUF_CONV = 0x3890           # tampon de composition (128 o : ligne + CRLF)
BUF_CHEMIN = 0x3910         # chemin complet du journal (304 o, MAX_PATH+marge)
SCRATCH_ECRIT = 0x3A40      # qword écrit (WriteFile lpNumberOfBytesWritten)

# --- État win-05:R3 (miroir écran, D37) ------------------------------------------

BUF_MIROIR = 0x3A50         # tampon UTF-16 du miroir écran (128 o) — ligne
                            # la plus longue : 43 o texte + 11 chiffres +
                            # CRLF + NUL = 57 chars = 114 o ≤ 128
JOURNAL_TRACE = 0x5000      # entrée trace de win-05 (4 args ASCII, prologue
                            # à l'instruction 0 — verrou pile-alignee)
JOURNAL_GUI = 0x5100        # entrée scénario (utf16, nchars) : force mode 2 (shim
                            # en fin de slot, saute au début du bloc)

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
assert FIN_UTF16 <= R_IAT_K32B, "zone UTF-16 déborde sur l'IAT kernel32#2"

# Chaînes ASCII de trace (win-02/04 → win-11) : pose séquentielle serrée
# derrière l'IAT kernel32#2. Chaque entrée : nom -> (adresse, octets).
# Le NUL n'est posé que pour NOM_FICHIER (memcpy 17 o) ; les lignes L* sont
# pilotées par leur longueur (mode 0/1 de win-11), pas de terminaison.
_SEQ_ASCII = [
    ("L00", b"L00 demarrage demonstration 0.3.0-demo.8"),
    ("L01", b"L01 fenetre principale creee"),
    ("LKO_GUI", b"LKO creation fenetre impossible gle="),
    ("L02", b"L02 controles crees (journal, bouton)"),
    ("L03", b"L03 clic : lancement du scenario"),
    ("LKO_EDIT", b"LKO creation du journal (EDIT) echouee gle="),
    ("LKO_BOUTON", b"LKO creation du bouton echouee gle="),
    ("LKO_SPAWN", b"LKO lancement thread scenario echoue gle="),
    ("NOM_FICHIER", b"demo_journal.txt\x00"),
    ("L4C", b"L4C move journal="),
    ("L4D", b"L4D move bouton="),
]
CHAINES_ASCII = {}
_cur = R_ASCII
for _nom, _octets in _SEQ_ASCII:
    CHAINES_ASCII[_nom] = (_cur, _octets, len(_octets))
    _cur += len(_octets)
assert _cur <= RDATA_RVA + RDATA_VSIZE, "zone ASCII trace debordante"
LONGUEURS_ASCII = {n: len(o) for n, (_a, o, _l) in CHAINES_ASCII.items()}

ECHO_ENTREE = L2.ECHO_ENTREE            # 0x4600 — cible du patch (héritage)
ECHO_CROISSANCE = L2.ECHO_CROISSANCE    # 0x4680 — zone de croissance

# --- Sondes de trace (D40/D42 — instrumentation TEMPORAIRE) -----------------------
# Chaînes ASCII posées dans les zones libres de .rdata (jamais lues par le
# chargeur : hors INT/IAT/hints/reloc). Les zones UTF-16 (14 o restants) et
# ASCII (2 o restants) sont PLEINES depuis D40 — d'où les interstices, puis
# la zone libre M2 0x266E-0x26D8 (chaînes de tcp-10/tcp-12 NON posées dans
# la démo : leurs utilisateurs ne sont pas embarqués). Adresses fixes,
# longueurs pilotées par edx (mode 0 win-05).
R_SONDE_1 = 0x2748   # interstice INT kernel32#2 (fin 0x2748) → reloc 0x2760
R_SONDE_2 = 0x276C   # interstice reloc (fin 0x276C) → INT user32 0x2780
R_SONDE_3 = 0x22F1   # interstice hint FlushFileBuffers (hn = 2+18 o, fin 0x22F1) → IAT ws2 0x2300
R_SONDE_S1 = 0x266E  # zone libre M2 (fin "echo " 0x266E → "fin connexion" 0x26D8)
R_SONDE_S2 = 0x267A  # suite de la même zone libre
R_SONDE_4 = 0x268B   # suite de la même zone libre
R_SONDE_5 = 0x269B   # suite de la même zone libre
CHAINES_SONDES = {
    "SONDE_1": (R_SONDE_1, b"sonde1 avant echo", 17),   # avant le 1er appel écho (D40)
    "SONDE_2": (R_SONDE_2, b"sonde2 patch pose", 17),   # après tcp-07 mode 0 = 0 (D40)
    "SONDE_3": (R_SONDE_3, b"sonde3 v2 ok", 12),        # après memcmp v2 (écho patché, D40)
    "SONDE_S1": (R_SONDE_S1, b"S1 accept ok", 12),      # serveur : accept retourné (D42, win-08:R2)
    "SONDE_S2": (R_SONDE_S2, b"S2 fil echo lance", 17),  # serveur : fil tcp-09 lancé (D42, win-08:R2)
    "SONDE_4": (R_SONDE_4, b"sonde4 envoye ok", 16),    # client : émission complète (D42, win-10:R2)
    "SONDE_5": (R_SONDE_5, b"sonde5 recu ok", 14),      # client : réception complète (D42, win-10:R2)
}

# --- Jetons de retour d'émulation (oracle, hors binaire) ------------------------

SENTINELLE_RETOUR = L2.SENTINELLE_RETOUR

NOMS_BLOCS = dict(L2.NOMS_BLOCS) | {
    "d40001": "win-principal", "d40002": "win-fenetre", "d40003": "win-boucle",
    "d40004": "win-procedure", "d40005": "win-journal", "d40006": "win-autotest",
    "d40007": "win-client", "d40008": "win-serveur", "d40009": "win-scenario",
    "d40010": "win-echange", "d40011": "win-journal-fichier",
}
