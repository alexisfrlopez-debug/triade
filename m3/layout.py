"""layout.py — Plan d'adressage du projet TRIADE, jalon M3 (profil x86-64-win11-pe).

Source unique de vérité partagée par build_m3.py, outils/auteur.py et
oracle_m3.py. Toute adresse du binaire proxy.exe dérive d'ici ; la notation
référence ces constantes et le builder vérifie la concordance.

HÉRITAGE M0/M1/M2 (R7 — jamais déplacé) :
  - blocs scellés io @ 0x1040/0x1080 et libc @ 0x1100-0x13FF, octets identiques
    à hello.exe / selftest.exe / echo.exe ;
  - blocs réseau M2 @ leurs RVA exacts : tcp-01 0x4000, tcp-02 0x4100,
    tcp-03 0x4140, tcp-04 0x4180, tcp-05 0x41C0, tcp-06 0x4300, tcp-11 0x4B00
    — octets identiques à echo.exe (l'IAT existante est inchangée) ;
  - .text couvre 0x1000-0x1FFF (http-12 au slot d'application 0x1800 — celui
    de tcp-12 dans echo.exe : exécutables distincts, plans distincts,
    discipline identique), .rdata démarre à 0x2000, .data à 0x3000.

EXTENSION M3 (D46, génération 4 — blocs e5xxxx) :
  - tcp-13 (connexion cliente résolue) occupe le trou libre net 0x4200-0x42FF
    (laissé par tcp-05 @ 0x41C0 dans echo.exe) ;
  - la zone http étend .text2 depuis 0x4C00 (libre après tcp-11 @ 0x4B00) :
    http-01 0x4C00, http-02 0x4C80, http-03 0x4D80, http-04 0x4E00,
    http-05 0x4EC0, http-06 0x4F40, http-07 0x5000, http-08 0x50C0,
    http-09 0x51C0, http-10 0x5280, http-11 0x5680 ;
  - .text2 couvre 0x4000-0x5FFF (vsize 0x2000) ; les slots 0x4400-0x4AFF
    (tramp+echo) et 0x4800-0x49FF (tcp-09/10) restent int3 dans l'image M3 :
    ces blocs ne sont pas embarqués (aucun appelant M3 — le patch à chaud
    revient au jalon M5) ;
  - l'IAT ws2_32 est ÉTENDUE de deux entrées appendues (D46) :
    getaddrinfo @ 0x2350, freeaddrinfo @ 0x2358 — les dix premiers slots
    0x2300-0x2348 sont inchangés (R7) ; l'INT ws2_32 (13 qwords désormais)
    et les hints déménagent en conséquence (données pures, aucun octet de
    code ne les référence — relocation documentée sans effet R7, miroir
    D33/D35) ;
  - état .data identique à M2 (stdout, stdin, écoute, drapeau, section
    critique) : les zones 0x3000-0x37FF (curseur+arène héritage) restent
    réservées.

CORRECTIF http-10:R2 (journal 36 / D47) : le relais du corps de requête est
borné par Content-Length et vit INLINE dans la session (boucles tcp-03/tcp-04
autorisées par I1 de http-10) — http-09 (pompe à fermeture délimitée) est
réservé aux pompes du tunnel CONNECT et au relais de réponse. La Q4 de la
spécification est clarifiée à R2 : la mention « http-09 cliente→amont » de R1
décrivait la discipline (émission intégrale, octet exact), pas l'appel —
mécaniquement impossible pour un corps borné (http-09 s'arrête à l'EOF du
client, qui attend la réponse sur la même connexion).
"""

import importlib.util
import os
import sys

# Le plan M2 se charge sous un nom distinct ("layout_m2") : les deux fichiers
# s'appellent layout.py — l'import classique serait circulaire.
_CHEMIN_M2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "m2", "layout.py")
_spec = importlib.util.spec_from_file_location("layout_m2", _CHEMIN_M2)
L2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L2)   # noqa: E402 — plan M2 (héritage)

# --- Image et sections --------------------------------------------------------

IMAGE_BASE = L2.IMAGE_BASE                # 0x140000000
TEXT_RVA, RDATA_RVA, DATA_RVA = L2.TEXT_RVA, L2.RDATA_RVA, L2.DATA_RVA
TEXT2_RVA = 0x4000
FILE_ALIGN, SECT_ALIGN = L2.FILE_ALIGN, L2.SECT_ALIGN
TEXT_VSIZE = L2.TEXT_VSIZE                # 0x1000 (io + libc + app)
RDATA_VSIZE = L2.RDATA_VSIZE              # 0x1000
DATA_VSIZE = L2.DATA_VSIZE                # 0x1000
TEXT2_VSIZE = 0x2000                      # 0x4000-0x5FFF (net + thr + srv + http)
SIZE_OF_IMAGE = 0x6000
TEXT_FILE, RDATA_FILE, DATA_FILE = L2.TEXT_FILE, L2.RDATA_FILE, L2.DATA_FILE   # 0x200/0x1200/0x2200
TEXT2_FILE = 0x2C00
DATA_RAW = 0xA00                          # .data committée : état serveur (0x3800+)
TAILLE_FICHIER = 0x4C00                   # 0x2C00 + 0x2000

DLL_CHARACTERISTICS = L2.DLL_CHARACTERISTICS   # DYNAMICBASE | HEVA | NX

VERSION_DEV1 = "0.4.0-dev.2"   # proxy complet : 13 blocs M3 + réutilisation R7 ;
                                 # dev.2 (D63) : http-10:R3 — probing de pile au
                                 # prologue (c00000fd terrain 21:38 corrigé)
VERSION_U64_DEV1 = 0x00040002  # R10 : monotonie de version (anti-rollback)
VERSION_U64_MIN = 0x00040000   # plancher accepté par la porte R10 (http-12:Q1)
VERSION_RC1 = "0.4.0-rc.1"    # cristallisation R6 10/10 + conformité § 8.2 verte
                               # (D74) — candidate à la validation terrain
VERSION_FINALE = "0.4.0"      # validation terrain consignée (T2 du superviseur,
                               # 6 verts consécutifs D64-D71, octets dd12b649
                               # inchangés) — balise immuable § 9 ; défaut →
                               # 0.4.1 à contrat stable (R4)

# --- Blocs embarqués dans proxy.exe (couche C, génération 4) --------------------
# a1xxxx = M0 ; b2xxxx = M1 ; c3xxxx = M2 ; e5xxxx = M3 (D46). Tous les slots
# sont multiples de 64 (D8), alignés 16, padding inter-blocs >= 16.

BLOCS_IO = L2.BLOCS_IO                     # a10002 write, a10003 exit (octets M0)
BLOCS_LIBC_EMBARQUES = L2.BLOCS_LIBC_EMBARQUES   # b20001-04 (octets selftest.exe)
BLOCS_TCP_EMBARQUES = [                    # octets echo.exe, RVA exacts (R7)
    ("c30001", "tcp-01:R1", 0x4000, 0x100, "M2", 1),   # init serveur
    ("c30002", "tcp-02:R1", 0x4100, 0x40, "M2", 1),    # accept
    ("c30003", "tcp-03:R1", 0x4140, 0x40, "M2", 1),    # recv
    ("c30004", "tcp-04:R1", 0x4180, 0x40, "M2", 1),    # send
    ("c30005", "tcp-05:R1", 0x41C0, 0x40, "M2", 1),    # close
    ("c30006", "tcp-06:R1", 0x4300, 0x40, "M2", 1),    # spawn (CreateThread)
    ("c30011", "tcp-11:R1", 0x4B00, 0x100, "M2", 1),   # ligne de journal
]
BLOCS_M3 = [
    ("e50001", "http-01:R1", 0x4C00, 0x80, "M3-dev.1", 1),   # itérateur CRLF
    ("e50002", "http-02:R1", 0x4C80, 0x200, "M3-dev.1", 1),  # ligne de requête
    ("e50003", "http-03:R1", 0x4E80, 0xC0, "M3-dev.1", 1),   # ligne d'en-tête
    ("e50004", "http-04:R1", 0x4F40, 0x140, "M3-dev.1", 1),  # recherche d'en-tête
    ("e50005", "http-05:R1", 0x5080, 0xC0, "M3-dev.1", 1),   # décimal borné
    ("e50006", "http-06:R2", 0x5140, 0xC0, "M3-dev.1", 1),   # fin de tête
    ("e50007", "http-07:R1", 0x5200, 0x180, "M3-dev.1", 1),  # autorité
    ("e50008", "http-08:R1", 0x5380, 0x140, "M3-dev.1", 1),  # cible
    ("e50009", "http-09:R1", 0x54C0, 0xC0, "M3-dev.1", 1),   # pompe
    ("e50010", "http-10:R2", 0x5580, 0x800, "M3-dev.1", 1),  # session proxy
    ("e50011", "http-11:R1", 0x5D80, 0x100, "M3-dev.1", 1),  # console
    ("e50012", "http-12:R1", 0x1800, 0x480, "M3-dev.1", 1),  # orchestrateur — entrée
    ("e50013", "tcp-13:R1", 0x4400, 0x1C0, "M3-dev.1", 1),   # connexion cliente
]
# ARRÊT étape b (mesure auteur) : la préfiguration D46 donnait http-02 0x100,
# http-04 0xC0, http-07/08 0xC0/0x100, http-10 0x400, tcp-13 0x100 @0x4200 —
# les notations réelles exigent 424/252/307/246/1746/402 o : la zone http est
# réarrêtée ci-dessus (mêmes règles D8 : multiples de 64, alignés 16, padding
# >= 16) et tcp-13 occupe 0x4400-0x45BF (zone tramp M2, INT3 dans proxy.exe
# — aucun patch à chaud à ce jalon ; le trou net 0x4200 reste int3). L'IAT
# gagne TROIS entrées appendues (getaddrinfo, freeaddrinfo, connect — la
# préfiguration oubliait connect, exigé par tcp-13:I1).
# tcp-07/08/09/10/12 et libc-05/06/07/09 restent indexés par la carte
# génération 3 (echo.exe) — aucun appelant dans proxy.exe.

ENTREE = 0x1800    # AddressOfEntryPoint = http-12 orchestrateur

NOMS_BLOCS = dict(L2.NOMS_BLOCS) | {
    "e50001": "http-ligne", "e50002": "http-requete", "e50003": "http-entete",
    "e50004": "http-chercher", "e50005": "http-nombre", "e50006": "http-tete",
    "e50007": "http-autorite", "e50008": "http-cible", "e50009": "http-pompe",
    "e50010": "http-session", "e50011": "http-console", "e50012": "http-main",
    "e50013": "tcp-connexion",
}

# --- .text2 : zones ------------------------------------------------------------

ZONE_NET = (0x4000, 0x42FF)      # tcp-01..05 (trou net 0x4200-0x42FF : int3)
ZONE_CLI = (0x4400, 0x45BF)     # tcp-13 (zone tramp M2 réaffectée — arrêt b)
ZONE_THR = (0x4300, 0x43FF)     # tcp-06
ZONE_RESERVEE_1 = (0x45C0, 0x4AFF)   # reste tramp+echo M2 : int3 dans l'image M3
ZONE_RESERVEE_2 = (0x4800, 0x49FF)   # tcp-09/10 M2 : int3 dans l'image M3
ZONE_SRV = (0x4B00, 0x4BFF)      # tcp-11
ZONE_HTTP = (0x4C00, 0x5E7F)     # http-01..http-11 (arrêt étape b : mesure
                            # auteur — http-02 424 o, http-07 307 o, http-10
                            # 1746 o, http-08 246 o, http-04 252 o ont dicté
                            # les slots ; la préfiguration D46 est réarrêtée,
                            # même discipline, même zone)

# --- .rdata : structures PE (héritage + extension M3) ---------------------------

R_DESC_IMPORT = 0x2030      # descripteur kernel32 (héritage, FT figée 0x20B0)
R_DESC_WS2 = 0x2044         # descripteur ws2_32 (FT 0x2300, D35)
R_NOM_DLL = 0x206C          # "kernel32.dll\0"
R_HN_GSH, R_HN_WF, R_HN_EP = 0x2079, 0x2088, 0x2094
R_NOM_WS2 = 0x20A4          # "ws2_32.dll\0"
R_IAT = 0x20B0              # IAT kernel32 — SCELLÉE (R7), ordre GSH/WF/EP figé
R_INT_KERNEL32 = 0x2110     # INT kernel32 (11 qwords)
R_HN_CT = 0x2170
R_HN_VP = 0x217F
R_HN_ICS = 0x2190
R_HN_ECS = 0x21AC
R_HN_LCS = 0x21C3
R_HN_RF = 0x21DA
R_HN_CH = 0x21E5
R_INT_WS2 = 0x2240          # INT ws2_32 (14 qwords : 13 entrées + terminateur)
R_IAT_WS2 = 0x2300          # IAT ws2_32 — 10 premiers slots SCELLÉS (R7),
                            # TROIS entrées appendues (arrêt b) : getaddrinfo
                            # 0x2350, freeaddrinfo 0x2358, connect 0x2360 ;
                            # terminateur 0x2368
R_HN_WS2 = 0x2370           # hints ws2_32 (13 entrées, 145 o -> 0x2401)
                            # — la zone fixtures http démarre à 0x2410 (arrêt b)

IAT_SLOTS = {
    # kernel32 — inchangé (héritage M0/M2, R7)
    "GetStdHandle": 0x20B0, "WriteFile": 0x20B8, "ExitProcess": 0x20C0,
    "CreateThread": 0x20C8, "VirtualProtect": 0x20D0,
    "InitializeCriticalSection": 0x20D8, "EnterCriticalSection": 0x20E0,
    "LeaveCriticalSection": 0x20E8, "ReadFile": 0x20F0, "CloseHandle": 0x20F8,
    # ws2_32 — 10 premiers inchangés (R7), deux appendus (M3)
    "WSAStartup": 0x2300, "socket": 0x2308, "bind": 0x2310, "listen": 0x2318,
    "accept": 0x2320, "recv": 0x2328, "send": 0x2330, "closesocket": 0x2338,
    "WSAGetLastError": 0x2340, "WSACleanup": 0x2348,
    "getaddrinfo": 0x2350, "freeaddrinfo": 0x2358, "connect": 0x2360,
}
KERNEL32_IMPORTS = L2.KERNEL32_IMPORTS          # 10 entrées, ordre figé (R7)
WS2_IMPORTS = L2.WS2_IMPORTS + ["getaddrinfo", "freeaddrinfo", "connect"]  # 13

# --- .rdata : fixtures du domaine http (D46 — propriétaires uniques) ------------

R_TAB_METHODES = 0x2410     # http-02 : 8 entrées (ptr u64, len u64) + TERMINATEUR
                            # (len 0 — arrêt de marche de la notation) = 9*16 = 144
R_METHODES = 0x24A0         # chaînes "GET\0".."CONNECT\0" (47 o, NUL-terminées)
R_SLASH = 0x24D0            # http-08 : chaîne "/" + NUL (chemin par défaut)
R_TAB_REPONSES = 0x24E0     # http-10 : 7 entrées (ptr u64, len u64) — table des
                            # réponses (400/431/501/411/505/502/200-tunnel) ;
                            # fixture (unique propriété des textes), la notation
                            # référence les lignes directement (le build vérifie
                            # la concordance table <-> chaînes)
R_TXT_400 = 0x2560          # "HTTP/1.1 400 Requete mal formee\r\n\r\n" (35)
R_TXT_431 = 0x2584          # "HTTP/1.1 431 Tete trop grande\r\n\r\n" (33)
R_TXT_501 = 0x25A8          # "HTTP/1.1 501 Non implemente\r\n\r\n" (31)
R_TXT_411 = 0x25C8          # "HTTP/1.1 411 Longueur requise\r\n\r\n" (33)
R_TXT_505 = 0x25EC          # "HTTP/1.1 505 Version non supportee\r\n\r\n" (38)
R_TXT_502 = 0x2614          # "HTTP/1.1 502 Passerelle inaccessible\r\n\r\n" (40)
R_TXT_TUNNEL = 0x2640       # "HTTP/1.1 200 Tunnel etabli\r\n\r\n" (30)
R_TAB_SUM = 0x2660          # porte R10 : (rva u32, taille u32, somme u64)* + terme
R_VERSION = 0x2820          # qword version (R10, monotonie — plancher 0x00040000)
R_ANCRE = 0x2830            # ancre de calcul de base (position-indépendance, D33)
R_RELOC = 0x2990            # BASERELOC minimal (12 o, entrées ABSOLUTE)

# Index des réponses dans R_TAB_REPONSES (http-10, unique propriétaire)
REP_400, REP_431, REP_501, REP_411, REP_505, REP_502, REP_TUNNEL = range(7)

# --- .rdata : chaînes (journal + commandes, discipline tcp-11/tcp-12) -----------

R_MSG_BANNIERE = 0x2840     # "TRIADE M3 : proxy demarre (port 25000)\r\n" (40)
R_MSG_CONNEXION = 0x2870    # "connexion entrante\r\n" (20) — journalisée par http-10
R_MSG_TUNNEL = 0x2890       # "tunnel\r\n" (8)
R_MSG_FIN = 0x28A0          # "fin connexion\r\n" (15)
R_MSG_ARRET = 0x28C0        # "arret\r\n" (7)
R_MSG_INCONNU = 0x28D0      # "commande inconnue\r\n" (19)
R_MSG_ERREUR = 0x28F0       # "erreur reseau, arret\r\n" (22)
R_MSG_KO = 0x2910           # "TRIADE M3 : integrite KO, arret\r\n" (33)
R_CMD_QUIT = 0x2940         # "quit\r\n" (6) — fixture http-11 (comparaison exacte)
R_NOM_HOST = 0x2950         # "Host\0" (4) — chercheur http-10
R_NOM_CL = 0x2960           # "Content-Length\0" (14) — chercheur http-10
R_NOM_TE = 0x2970           # "Transfer-Encoding\0" (17) — chercheur http-10

BANNIERE = b"TRIADE M3 : proxy demarre (port 25000)\r\n"
PORT_ECOUTE = 25000         # 0x61A8 — identique M2 (tcp-01 scellé)
AF_INET, SOCK_STREAM, IPPROTO_TCP = 2, 1, 6
SOMAXCONN_M2 = 8            # file d'attente d'acceptation (tcp-01 scellé)

# --- Constantes à propriétaire unique (charte m3/I, point 3) --------------------

MAX_TETE = 8192             # http-06 (RFC 7230 §3.1.1 : au moins 8000)
MAX_CIBLE = 2048            # http-02 (usage navigateur)
HOTE_MAX = 255              # tcp-13 (limite DNS)
TAILLE_TAMPON_SESSION = 16384   # http-10 : tampon d'accumulation (>= MAX_TETE+1)
TAILLE_TAMPON_REECRITURE = 12288  # http-10 : tampon de réécriture
TAILLE_TAMPON_POMPE = 4096  # http-10 : pompe amont (thread détaché du tunnel)

# --- .data : état du serveur (identique M2 — tcp-11 réutilisé) -------------------

R_CURSEUR = L2.R_CURSEUR    # 0x3000 (héritage libc-05/06 — réservé)
ARENE_BASE = L2.ARENE_BASE  # 0x3040 (héritage — réservé)
ARENE_TAILLE = L2.ARENE_TAILLE

R_STDOUT = 0x3800           # handle stdout (cache par http-12 au démarrage)
R_STDIN = 0x3808            # handle stdin
R_LISTEN = 0x3810           # socket d'écoute
R_QUIT = 0x3818             # drapeau d'arrêt demandé (0/1)
R_CS = 0x3830               # CRITICAL_SECTION (40 o) — sérialise le journal

# --- Jetons de retour d'émulation (oracle, hors binaire) ------------------------

SENTINELLE_RETOUR = L2.SENTINELLE_RETOUR
