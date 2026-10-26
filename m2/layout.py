"""layout.py — Plan d'adressage du projet TRIADE, jalon M2 (profil x86-64-win11-pe).

Source unique de vérité partagée par build_m2.py, outils/auteur.py et
oracle_m2.py. Toute adresse du binaire echo.exe dérive d'ici ; la notation
référence ces constantes et le builder vérifie la concordance.

HÉRITAGE M0/M1 (R7 — jamais déplacé) :
  - blocs scellés io @ 0x1040/0x1080 et libc @ 0x1100-0x13FF, octets identiques
    à hello.exe / selftest.exe — leurs déplacements RIP vers l'IAT (0x20B0+) et
    le curseur d'arène (0x3000) sont cuits dans les octets : ces RVA sont
    immuables, dans TOUT artefact qui les embarque ;
  - par conséquent .text couvre exactement 0x1000-0x1FFF, .rdata démarre à
    0x2000 (descripteur kernel32 @ 0x2030, IAT kernel32 @ 0x20B0 — les trois
    premiers slots GSH/WF/EP dans l'ordre M0), .data démarre à 0x3000
    (curseur @ 0x3000, arène @ 0x3040).

EXTENSION M2 (quatrième section, D33) :
  - ".text2" RX @ 0x4000-0x4FFF : zones net (0x4000), thr (0x4300), tramp
    (0x4400), echo (0x4600 — bloc cible + zone de croissance 0x4680), srv
    (0x4800) ; le COFF autorise quatre sections max (manuel § 7.2) ;
  - l'INT kernel32 déménage (l'ensemble d'imports passe de 3 à 10 entrées, il
    ne tient plus entre 0x2090 et l'IAT figée) — donnée pure, aucun octet de
    code ne la référence : relocation documentée, sans effet R7 ;
  - ws2_32.dll rejoint les imports (D7 : IAT, dix entrées) ;
  - l'état serveur vit en .data @ 0x3800+ (stdout, stdin, socket, drapeaux,
    entrée sauvegardée, section critique) — la zone 0x3000-0x37FF (curseur +
    arène) reste à l'identique.

PATCH À CHAUD (§ 7.4, jalon M2) :
  - le bloc echo-01 (cible) @ 0x4600 : entrée alignée 16 — 8 premiers octets
    remplaçables par E9 rel32 + NOP×3, un qword aligné unique, écriture
    atomique ;
  - la zone de croissance @ 0x4680 (128 o) reste int3 dans l'image : le bloc
    de remplacement (echo-01:R2, majuscules) vit en .rdata (staging) et n'est
    copié dans la croissance QU'AU RUNTIME par tcp-07 (VirtualProtect +
    memcpy scellé + bascule) — le code des sections .text/.text2 est
    byte-identique entre dev.1 et dev.2 (démonstration R7) ;
  - rollback : l'entrée originale (qword sauvegardé en .data à l'application)
    est réécrite par la même écriture alignée unique.
"""

import importlib.util
import os
import sys

# Le plan M1 se charge sous un nom distinct ("layout_m1") : les deux fichiers
# s'appellent layout.py — l'import classique serait circulaire.
_CHEMIN_M1 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "m1", "layout.py")
_spec = importlib.util.spec_from_file_location("layout_m1", _CHEMIN_M1)
L1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L1)   # noqa: E402 — plan M1 (héritage)

# --- Image et sections --------------------------------------------------------

IMAGE_BASE = L1.IMAGE_BASE                # 0x140000000
TEXT_RVA, RDATA_RVA, DATA_RVA = L1.TEXT_RVA, L1.RDATA_RVA, L1.DATA_RVA
TEXT2_RVA = 0x4000
FILE_ALIGN, SECT_ALIGN = L1.FILE_ALIGN, L1.SECT_ALIGN
TEXT_VSIZE = L1.TEXT_VSIZE                # 0x1000 (io + libc + app)
RDATA_VSIZE = L1.RDATA_VSIZE              # 0x1000
DATA_VSIZE = L1.DATA_VSIZE                # 0x1000
TEXT2_VSIZE = 0x1000                      # 0x4000-0x4FFF (net + thr + tramp + echo + srv)
SIZE_OF_IMAGE = 0x5000
TEXT_FILE, RDATA_FILE, DATA_FILE = L1.TEXT_FILE, L1.RDATA_FILE, L1.DATA_FILE   # 0x200/0x1200/0x2200
TEXT2_FILE = 0x2C00
DATA_RAW = 0xA00                          # .data committée : curseur+arène+état serveur (0x3800+)
TAILLE_FICHIER = 0x3C00                   # 0x2C00 + 0x1000

DLL_CHARACTERISTICS = L1.DLL_CHARACTERISTICS   # DYNAMICBASE | HEVA | NX

VERSION_DEV1 = "0.3.0-dev.1"   # serveur + patch mécanique, staging vide
VERSION_DEV2 = "0.3.0-dev.2"   # boucle § 5 : echo-01:R2 (majuscules) en staging
VERSION_RC1 = "0.3.0-rc.1"     # cristallisation + conformité 1-7 verte
VERSION_FINALE = "0.3.0"       # validation terrain constatée — balise immuable § 9

VERSION_U64_DEV1 = 0x00030001  # R10 : monotonie de version (anti-rollback)
VERSION_U64_DEV2 = 0x00030002
VERSION_U64_MIN = 0x00030000   # plancher accepté par la porte R10

# --- Blocs embarqués dans echo.exe (couche C, génération 2) --------------------
# a1xxxx = M0 ; b2xxxx = M1 ; c3xxxx = M2 (D33). Tous les slots sont multiples
# de 64 (D8), alignés 16, padding inter-blocs >= 16.

BLOCS_IO = L1.BLOCS_IO                     # a10002 write, a10003 exit (octets M0)
BLOCS_LIBC_EMBARQUES = [                   # libc réutilisée, octets selftest.exe
    ("b20001", "libc-01:R1", 0x1100, 0x80, "M1", 1),   # memcpy (tcp-07, tcp-11)
    ("b20002", "libc-02:R1", 0x1180, 0x80, "M1", 1),   # memcmp (tcp-10)
    ("b20003", "libc-03:R1", 0x1200, 0x80, "M1", 1),   # strlen (tcp-11)
    ("b20004", "libc-04:R1", 0x1280, 0x80, "M1", 1),   # itoa (tcp-11)
]
# libc-05/06/07 restent scellés dans selftest.exe — aucun appelant dans echo.exe.

BLOC_LIBC09 = ("c30012", "libc-09:R1", 0x1440, 0x80)   # zone_alloc_ts, NON embarqué
# (indexé par la carte génération 2 ; vérifié par l'oracle contre la notation)

BLOCS_TCP = [
    ("c30001", "tcp-01:R1", 0x4000, 0x100, "M2-dev.1", 1),  # init serveur (WSA+socket+bind+listen)
    ("c30002", "tcp-02:R1", 0x4100, 0x40, "M2-dev.1", 1),   # accept
    ("c30003", "tcp-03:R1", 0x4140, 0x40, "M2-dev.1", 1),   # recv
    ("c30004", "tcp-04:R1", 0x4180, 0x40, "M2-dev.1", 1),   # send
    ("c30005", "tcp-05:R1", 0x41C0, 0x40, "M2-dev.1", 1),   # close (closesocket)
    ("c30006", "tcp-06:R1", 0x4300, 0x40, "M2-dev.1", 1),   # spawn (CreateThread)
    ("c30007", "tcp-07:R1", 0x4400, 0x200, "M2-dev.1", 1),  # moteur de patch (bascule echo)
    ("c30008", "tcp-08:R1", 0x4600, 0x40, "M2-dev.1", 1),   # echo v1 identité — CIBLE du patch
    ("c30009", "tcp-09:R1", 0x4800, 0x180, "M2-dev.1", 1),  # thread connexion
    ("c30010", "tcp-10:R1", 0x4980, 0x180, "M2-dev.1", 1),  # thread console
    ("c30011", "tcp-11:R1", 0x4B00, 0x100, "M2-dev.1", 1),  # ligne de journal
    ("c30013", "tcp-12:R1", 0x1800, 0x800, "M2-dev.1", 1),  # main — point d'entrée
]
BLOC_ECHO_V2 = ("c30014", "tcp-08:R2", 0x4680, 0x80)     # remplaçant (staging) — dev.2

ENTREE = 0x1800    # AddressOfEntryPoint = tcp-12 main

NOMS_BLOCS = dict(L1.NOMS_BLOCS) | {
    "c30001": "tcp-init", "c30002": "tcp-accept", "c30003": "tcp-recv",
    "c30004": "tcp-send", "c30005": "tcp-close", "c30006": "tcp-spawn",
    "c30007": "tcp-patch", "c30008": "echo-v1", "c30009": "tcp-conn",
    "c30010": "tcp-console", "c30011": "tcp-journal", "c30012": "zone-alloc-ts",
    "c30013": "tcp-main", "c30014": "echo-v2",
}

# --- .text2 : zones et points remarquables ------------------------------------

ECHO_ENTREE = 0x4600        # entrée du bloc cible (alignée 16 — trampolinable, R7)
ECHO_CROISSANCE = 0x4680    # zone de croissance (128 o, int3 dans l'image)
ETENDUE_PROTECT = 0x700     # VirtualProtect : page 0x4000 -> fin de croissance 0x4700

# --- .rdata : structures PE (héritage + extension M2) --------------------------

R_DESC_IMPORT = 0x2030      # descripteur kernel32 (héritage M0/M1, FT figée 0x20B0)
R_DESC_WS2 = 0x2044         # descripteur ws2_32 (M2) — CONTIGU : le marche d'imports
                            # (kernel32, ws2_32, terminateur 0x2058) doit etre d'un seul
                            # tenant, le terminateur M1 a 0x2044 est demenage (D33)
R_NOM_DLL = 0x206C          # "kernel32.dll\0" (demenage de 0x2058, donnee pure)
R_HN_GSH, R_HN_WF, R_HN_EP = 0x2079, 0x2088, 0x2094   # hints herites demenages
                            # (donnee pure) — GSH deplacee de 0x2078 (collision
                            # NUL de 1 octet avec R_NOM_DLL, garde-fou journal 18)
R_NOM_WS2 = 0x20A4          # "ws2_32.dll\0" (M2)
R_IAT = 0x20B0              # IAT kernel32 — SCELLÉE : les 3 premiers slots sont
                            # cuits dans a10002/a10003 (R7), l'ordre GSH/WF/EP figé
R_INT_KERNEL32 = 0x2110     # INT kernel32 (11 qwords) — déménagée de 0x2090 (D33 :
                            # 10 entrées ne tiennent plus avant l'IAT figée ; donnée
                            # pure, aucun octet de code ne la référence)
R_HN_CT = 0x2170            # hints kernel32 nouveaux (M2)
R_HN_VP = 0x217F
R_HN_ICS = 0x2190
R_HN_ECS = 0x21AC
R_HN_LCS = 0x21C3
R_HN_RF = 0x21DA
R_HN_CH = 0x21E5
R_INT_WS2 = 0x2240          # INT ws2_32 (11 qwords)
R_IAT_WS2 = 0x22A0          # IAT ws2_32 (11 qwords)
R_HN_WS2 = 0x2310           # hints ws2_32 (10 entrées)
R_STAGING = 0x23D0          # staging du remplaçant echo-01:R2 (128 o ; int3 si absent)
R_TAB_SUM = 0x2450          # porte R10 : (rva u32, taille u32, somme u64)* + terme
R_VERSION = 0x2600          # qword version (R10, monotonie)
R_ANCRE = 0x2610            # ancre de calcul de base (position-indépendance, D33)
R_RELOC = 0x2760            # BASERELOC minimal (12 o, entrées ABSOLUTE — image sans
                            # adresse absolue, aucune relocalisation réelle nécessaire)

IAT_SLOTS = {
    # kernel32 — les trois premiers hérités M0 (ordre figé, R7)
    "GetStdHandle": 0x20B0, "WriteFile": 0x20B8, "ExitProcess": 0x20C0,
    "CreateThread": 0x20C8, "VirtualProtect": 0x20D0,
    "InitializeCriticalSection": 0x20D8, "EnterCriticalSection": 0x20E0,
    "LeaveCriticalSection": 0x20E8, "ReadFile": 0x20F0, "CloseHandle": 0x20F8,
    # ws2_32
    "WSAStartup": 0x2300, "socket": 0x2308, "bind": 0x2310, "listen": 0x2318,
    "accept": 0x2320, "recv": 0x2328, "send": 0x2330, "closesocket": 0x2338,
    "WSAGetLastError": 0x2340, "WSACleanup": 0x2348,
}
KERNEL32_IMPORTS = ["GetStdHandle", "WriteFile", "ExitProcess", "CreateThread",
                    "VirtualProtect", "InitializeCriticalSection",
                    "EnterCriticalSection", "LeaveCriticalSection", "ReadFile",
                    "CloseHandle"]
WS2_IMPORTS = ["WSAStartup", "socket", "bind", "listen", "accept", "recv",
               "send", "closesocket", "WSAGetLastError", "WSACleanup"]

# --- .rdata : chaînes du serveur (journal + commandes console) ------------------

# Longueurs = octets réels (LF compté) — l'erratum C1 (journal 18) a corrigé
# l'arithmétique « caractères + CR » qui oubliait le LF ; le garde-fou de
# chevauchement de build_m2.py (poser) garantit désormais le non-recouvrement.
R_MSG_BANNIERE = 0x2620     # "TRIADE M2 : serveur echo demarre (port 25000)\r\n" (47)
R_MSG_CONNEXION = 0x2650    # "connexion entrante\r\n" (20) — fin NUL à 0x2665
R_MSG_CRLF = 0x2665         # "\r\n" (2) — trou de 3 octets, accès octets (memcpy)
R_MSG_ECHO = 0x2668         # "echo " (5) — déplacée de 0x2664 (collision NUL, journal 18)
R_MSG_PATCH_OK = 0x2670     # "patch applique (majuscules)\r\n" (29)
R_MSG_RB_OK = 0x2690        # "retour arriere (identite)\r\n" (27)
R_MSG_INCONNU = 0x26B0      # "commande inconnue\r\n" (19)
R_MSG_REFUS = 0x26C4        # "commande refusee\r\n" (18)
R_MSG_FIN = 0x26D8          # "fin connexion\r\n" (15)
R_MSG_ARRET = 0x26E8        # "arret\r\n" (7)
R_MSG_ERREUR = 0x26F0       # "erreur reseau, arret\r\n" (22)
R_MSG_KO = 0x2708           # "TRIADE M2 : integrite KO, arret\r\n" (33)
R_CMD_PATCH = 0x2730        # "patch\r\n" (5+CR+LF = 7)
R_CMD_RB = 0x2738           # "rollback\r\n" (8+CR+LF = 10) — fin NUL à 0x2743
R_CMD_QUIT = 0x2748         # "quit\r\n" (4+CR+LF = 6) — déplacée de 0x2742 (collision NUL, journal 18)

BANNIERE = b"TRIADE M2 : serveur echo demarre (port 25000)\r\n"
PORT_ECOUTE = 25000         # 0x61A8 — stocké en ordre réseau dans sockaddr
AF_INET, SOCK_STREAM, IPPROTO_TCP = 2, 1, 6
SOMAXCONN_M2 = 8            # file d'attente d'acceptation

# --- .data : état du serveur (M2, au-delà de l'arène héritée) -------------------

R_CURSEUR = L1.R_CURSEUR    # 0x3000 (héritage libc-05/06)
ARENE_BASE = L1.ARENE_BASE  # 0x3040 (héritage)
ARENE_TAILLE = L1.ARENE_TAILLE

R_STDOUT = 0x3800           # handle stdout (cache par tcp-12 au démarrage)
R_STDIN = 0x3808            # handle stdin
R_LISTEN = 0x3810           # socket d'écoute
R_QUIT = 0x3818             # drapeau d'arrêt demandé (0/1)
R_ETAT_PATCH = 0x3820       # état du bloc echo : 0 = v1 identité, 1 = v2 majuscules
R_ENTREE_SAUVEE = 0x3828    # qword : 8 octets originaux de l'entrée echo (rollback)
R_CS = 0x3830               # CRITICAL_SECTION (40 o) — sérialise le journal

# --- Jetons de retour d'émulation (oracle, hors binaire) ------------------------

SENTINELLE_RETOUR = L1.SENTINELLE_RETOUR
