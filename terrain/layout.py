"""layout.py — Plan d'adressage du jalon terrain TRIADE (profil x86-64-win11-pe).

Source unique de vérité partagée par build_terrain.py, outils/auteur.py et
oracle_terrain.py. Toute adresse de superviseur.exe dérive d'ici.

LE SUPERVISEUR TERRAIN (D48) : un exe GUI qui exécute tous les tests du
projet en un clic (T1 démo M2, T2 proxy M3, T3 envoi Drive) et téléverse
son journal horodaté dans le dossier test du Drive par relais curl.exe.

HÉRITAGE (R7 — jamais déplacé, octets identiques aux artefacts scellés) :
  - io M0 @ 0x1040/0x1080 et libc M1 @ 0x1100-0x12FF (hello/selftest) ;
  - tcp-06 spawn @ 0x4300 (echo.exe) — win-04 scellé l'appelle ;
  - lignée démo : win-03 boucle @0x15C0, win-04 procédure @0x1640,
    win-06 autotest @0x1AC0, win-05 miroir @0x5000 (demo.exe 0.3.0-demo.9) ;
  - IAT kernel32#1 @0x20B0 (11 slots, ordre figé), IAT user32 @0x2800
    (14 slots), gdi32 @0x2980, kernel32#2 @0x2E80 — inchangées ;
  - table R10 @0x2450, ancre @0x2620, version @0x2628, fixtures win-06
    @0x2630-0x265A — adresses figées par win-06 scellé ;
  - chaînes scellées par win-04 : TXT_BOUTON @0x2A1E, CLASSE_EDIT @0x2A3A,
    CLASSE_BOUTON @0x2A44, CHAINE_VIDE @0x2A52, L03 @0x2F35, LKO_EDIT
    @0x2F55, LKO_BOUTON @0x2F80, LKO_SPAWN @0x2FA3, L4C @0x2FDD, L4D
    @0x2FEE — la pose UTF-16/ASCII est CONTRAINTE de retomber dessus ;
  - état .data hérité : hwnds @0x3860+, journal @0x3888+ (handle, BUF_CONV,
    BUF_CHEMIN, SCRATCH_ECRIT), BUF_MIROIR @0x3A50 (win-05 scellé).

NOUVEAUTÉS TERRAIN (génération 5, f6xxxx) :
  - sup-01 @0x1400 (entrée : horodatage AVANT fenêtre), sup-02 @0x1440
    (fenêtre « TRIADE superviseur terrain », classe TRIADE_superviseur) ;
  - sup-21 horodatage @0x1C40 slot 0x100 (TAMPON_NOM terrain_YYYYMMDD_
    HHMMSS.txt — chiffres par division inline, deux sous-routines locales) ;
  - sup-22 balayeur @0x1D40 slot 0xC0 (étiquette -> valeur, pur) ;
  - sup-11 journal @0x1E00 (contrat win-11:R1, nom dynamique — le relais
    queue de win-05 scellé jmp 0x1E00 tombe sur ce bloc : R4) ;
  - sup-09 scénario @0x4C00 (l'appelant scellé de win-04 : même slot que
    win-09 démo — exécutables distincts, plans distincts, discipline
    identique), sup-31 lanceur @0x5200, sup-36 fichiers @0x4E00 (lecture/
    écriture/suppression préfixées du répertoire — DIR_LONG posé en cache,
    un seul propriétaire du calcul), T1/T2/T3 @0x5400/0x5800/0x5E00 ;
  - ZONES DONNÉES SUP en .text2 (RX, lisible) : 0x4340-0x4BFF (lignes S,
    fixtures, étiquettes, URLs, gabarits curl) et 0x6000-0x63FF (INT/hints
    kernel32#3 + user32#2, noms de fichiers, cmdlines curl complètes) —
    l'espace .rdata est épuisé par l'héritage ; la table R10 couvre CES
    zones (intégrité des données posées, D48) ;
  - IAT kernel32#3 @0x2300 (9 slots : CreateProcessA, CreatePipe,
    WaitForSingleObject, GetExitCodeProcess, TerminateProcess,
    GetLocalTime, DeleteFileA, PeekNamedPipe, Sleep) et user32#2 @0x2360
    (FindWindowW, FindWindowExW, SendMessageTimeoutW) — l'ancienne zone
    ws2_32, libérée (le superviseur n'a pas de sockets : le réseau vit
    dans les processus testés et dans curl.exe) ;
  - état terrain .data : TAMPON_COMPO @0x3100 (1 888 o — composition
    sup-35 + source d'écriture sup-36 + tampon de vérification kit sup-37,
    D70 : la région .data [0x3000, 0x3860) était vide et sans référence ;
    l'ancienne zone 0x3EA0 n'offrait que 352 o avant la frontière .text2,
    la commande session réelle en fait 484 — le run terrain.15 est mort
    d'une violation d'écriture à 0x4000), puis TAMPON_NOM @0x3AD0 (32),
    TAMPON_AFF @0x3AF0 (32), ETAT_SUP @0x3B10 (96 : handles, tuyaux, pid,
    codes), TAMPON_JETON @0x3B70 (480), TAMPON_CMD @0x3D50 (672) — la
    section .data se termine à 0x4000 pile.
"""

import importlib.util
import os

# Le plan M2 se charge sous un nom distinct (les fichiers s'appellent tous
# layout.py — l'import classique serait ambigu).
_CHEMIN_M2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "m2", "layout.py")
_spec = importlib.util.spec_from_file_location("layout_m2", _CHEMIN_M2)
L2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L2)   # noqa: E402 — plan M2 (héritage)

# La lignée démo se charge pareil : les blocs réutilisés d4xxxx (win-03/04/
# 05/06, octet-identiques à demo.exe 0.3.0-demo.9) n'existent pas dans le
# plan M2 — leurs noms vivent dans demo/layout.py, qui fusionne déjà M2.
_CHEMIN_DEMO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "demo", "layout.py")
_spec_demo = importlib.util.spec_from_file_location("layout_demo", _CHEMIN_DEMO)
LD = importlib.util.module_from_spec(_spec_demo)
_spec_demo.loader.exec_module(LD)   # noqa: E402 — plan démo (héritage win)

# --- Image et sections ------------------------------------------------------------

IMAGE_BASE = L2.IMAGE_BASE                # 0x140000000
TEXT_RVA, RDATA_RVA, DATA_RVA = L2.TEXT_RVA, L2.RDATA_RVA, L2.DATA_RVA
TEXT2_RVA = L2.TEXT2_RVA                  # 0x4000
FILE_ALIGN, SECT_ALIGN = L2.FILE_ALIGN, L2.SECT_ALIGN
TEXT_VSIZE = L2.TEXT_VSIZE                # 0x1000 (io + libc + coquille)
RDATA_VSIZE = L2.RDATA_VSIZE              # 0x1000 (structures + chaînes scellées)
DATA_VSIZE = L2.DATA_VSIZE                # 0x1000 (0x3000-0x3FFF, brut dès 0x3800)
TEXT2_VSIZE = 0x4000                      # 0x4000-0x7FFF (tcp-06 + zones données + sup + kit
                                          #  + T4 @0x7200, terrain.17 — la section s'étend
                                          #  jusqu'à la borne alignée AVANT .rsrc @0x8000)
SIZE_OF_IMAGE = 0x14000                  # aligné SectionAlignment (.blob compris, terrain.17)
# Offsets fichier TERRAIN.2 : six sections -> 568 o d'en-têtes, la première
# section brute recule à 0x400 (les RVA ne bougent PAS — seuls les plans
# M2/démo gardent les anciennes valeurs scellées).
TEXT_FILE, RDATA_FILE, DATA_FILE = 0x400, 0x1400, 0x2400
TEXT2_FILE = 0x2E00
DATA_RAW = L2.DATA_RAW                    # 0xA00 (données committées dès 0x3800)

# --- Sections .rsrc et .blob (D49 — kit embarqué + habillage ressources) ----

# terrain.17 : T4 @0x7200 pousse .rsrc hors de .text2 — TOUTE VA de section
# doit rester ALIGNÉE sur SectionAlignment (0x1000) : le premier jet la posait
# à 0x7800, pefile ajustait à 0x7000 et le répertoire des ressources devenait
# illisible (le chargeur Windows exigerait la même discipline — attrapé par
# pefile AVANT l'écriture, fail-closed du build). .rsrc -> 0x8000, .blob -> 0x9000.
RSRC_RVA = 0x8000                         # VERSIONINFO + manifeste (RT_MANIFEST)
RSRC_VSIZE = 0x800                       # arbre ressources + VS_VERSIONINFO + XML
RSRC_FILE = 0x6E00                        # terrain.17 : suit .text2 crue allongée (0x2E00+0x4000)
BLOB_RVA = 0x9000                         # kit embarqué : lecture seule
BLOB_VSIZE = 0xAF10                      # en-tête + demo + proxy M4 (28 160 o) + slot annexe
BLOB_FILE = 0x7600                        # terrain.17 : 0x6E00 + 0x800 (.rsrc)
TAILLE_FICHIER = 0x12600                  # 0x7600 + 0xB000 (blob arrondi 0x200)

DLL_CHARACTERISTICS = L2.DLL_CHARACTERISTICS   # DYNAMICBASE | HEVA | NX
SUBSYSTEM_GUI = 2                         # WINDOWS_GUI

VERSION_TERRAIN1 = "0.5.0-terrain.1"      # première génération de la lignée terrain
VERSION_U64_TERRAIN1 = 0x00050101         # monotonie : au-dessus de proxy 0.4.0
VERSION_TERRAIN2 = "0.5.0-terrain.2"      # kit embarqué (D49) : 1 seul exe
VERSION_U64_TERRAIN2 = 0x00050102
VERSION_TERRAIN3 = "0.5.0-terrain.3"      # correction chargeur (D50)
VERSION_U64_TERRAIN3 = 0x00050103
VERSION_TERRAIN4 = "0.5.0-terrain.4"      # T4 tunnel M4 + kit proxy 0.5.0-dev.2 (D96)
VERSION_U64_TERRAIN4 = 0x00050104         # monotonie : génération M4 du superviseur
VERSION_TERRAIN5 = "0.5.0-terrain.5"      # T4 diagnostic : témoin page A + ligne S47 (D99)
VERSION_U64_TERRAIN5 = 0x00050105         # le même test, l'évidence préservée (17-D)
VERSION_TERRAIN6 = "0.5.0-terrain.6"      # T4 honnêteté : timeout d'événements silencieux (D100)
VERSION_U64_TERRAIN6 = 0x00050106         # le même test, la charte § 3 protégée (17-E)
VERSION_TERRAIN7 = "0.5.0-terrain.7"      # prévol intégré : orphelins + amont (D101)
VERSION_U64_TERRAIN7 = 0x00050107         # ÉTAPES 0/0 BIS du protocole automatiques (17-F)
VERSION_TERRAIN8 = "0.5.0-terrain.8"      # kit proxy M4 D102 : tls-07 scan PAR TYPE (17-G)
VERSION_U64_TERRAIN8 = 0x00050108         # le clair ENFIN relayé — reclassement Schannel
VERSION_U64_MIN = 0x00050000              # plancher de la lignée terrain

# --- En-têtes PE : règle du chargeur RÉEL (D50) -------------------------------------
# En-têtes réels : DOS 64 + PE 24 + opt 240 + 6 × sections 40 = 568 o (0x238).
# Le chargeur Windows exige que SizeOfHeaders COUVRE toute la table des
# sections et soit aligné sur FILE_ALIGN : 0x238 -> 0x400. Le terrain.2
# écrivait L.FILE_ALIGN (0x200) — valeur qui ne coïncidait avec la bonne
# que pour QUATRE sections ou moins (cas de tous les artefacts scellés
# précédents : 0x1E8 réels -> 0x200) : avec six sections, la table débordait
# des en-têtes déclarés et Windows refusait de lancer superviseur.exe
# (« il ne se passe rien » au double-clic, constat développeur 27/10).
SIZE_HEADERS = 0x400
assert 64 + 4 + 20 + 240 + 6 * 40 <= SIZE_HEADERS, "table des sections hors SizeOfHeaders"
assert SIZE_HEADERS % FILE_ALIGN == 0, "SizeOfHeaders non aligné FILE_ALIGN"
assert SIZE_HEADERS <= TEXT_FILE, "SizeOfHeaders déborde sur la première section brute"

# --- Blocs embarqués dans superviseur.exe (couche C, génération 5) ----------------
# a1xxxx = M0 ; b2xxxx = M1 ; c3xxxx = M2 ; d4xxxx = démo ; f6xxxx = terrain.
# Tous les slots multiples de 64 (D8), alignés 16, padding inter-blocs >= 16.

BLOCS_TERRAIN = [
    # héritage M0/M1 (octets identiques à hello.exe / selftest.exe)
    ("a10002", "hello-02:R1", 0x1040, 0x40, "M0", 1),
    ("a10003", "hello-03:R1", 0x1080, 0x40, "M0", 1),
    ("b20001", "libc-01:R1", 0x1100, 0x80, "M1", 1),
    ("b20002", "libc-02:R1", 0x1180, 0x80, "M1", 1),
    ("b20003", "libc-03:R1", 0x1200, 0x80, "M1", 1),
    ("b20004", "libc-04:R1", 0x1280, 0x80, "M1", 1),
    # héritage lignée démo + M2 (octets identiques à demo.exe 0.3.0-demo.9 / echo.exe)
    ("d40003", "win-03:R1", 0x15C0, 0x80, "demo.9", 1),
    ("d40004", "win-04:R4", 0x1640, 0x380, "demo.9", 1),
    ("d40006", "win-06:R1", 0x1AC0, 0x180, "demo.9", 1),
    ("f60021", "sup-21:R1", 0x1C40, 0x100, "terrain.1", 1),  # horodatage
    ("f60022", "sup-22:R1", 0x1D40, 0xC0, "terrain.1", 1),   # balayeur
    ("c30006", "tcp-06:R1", 0x4300, 0x40, "M2", 1),
    ("d40005", "win-05:R3", 0x5000, 0x200, "demo.9", 1),
    # génération terrain (D48)
    ("f60001", "sup-01:R1", 0x1400, 0x40, "terrain.1", 1),   # principal — entrée
    ("f60002", "sup-02:R1", 0x1440, 0x180, "terrain.1", 1),  # fenêtre
    ("f60011", "sup-11:R1", 0x1E00, 0x200, "terrain.1", 1),  # journal horodaté
    ("f60009", "sup-09:R4", 0x4C00, 0x200, "terrain.18", 1), # scénario (R3 D96 ; R4 D101 : prévol avant extraction)
    ("f60031", "sup-31:R1", 0x5200, 0x1C0, "terrain.1", 1),  # lanceur
    ("f60036", "sup-36:R1", 0x4E00, 0x1C0, "terrain.1", 1),  # fichiers (D48)
    ("f60033", "sup-33:R1", 0x5400, 0x3C0, "terrain.1", 1),  # T1 démo
    ("f60034", "sup-34:R1", 0x5800, 0x5C0, "terrain.1", 1),  # T2 proxy
    ("f60035", "sup-35:R1", 0x5E00, 0x4C0, "terrain.1", 1),  # T3 envoi Drive
    ("f60037", "sup-37:R1", 0x6600, 0x400, "terrain.2", 1),  # kit embarqué (D49)
    ("f60038", "sup-38:R2", 0x7200, 0x800, "terrain.17", 1), # test T4 — tunnel M4 (D96)
                                            # R2 (D99) : .temoin/.exitline — la zone s'étend
                                            # à 0x800 (0x7800-0x7FFF était libre), la table
                                            # R10 garde SES 28 entrées (l'entrée T4 couvre
                                            # désormais 0x7200-0x7FFF — taille 0x800)
    ("f60039", "sup-39:R1", 0x4B40, 0xC0, "terrain.18", 1),  # prévol — orphelins + amont
                                            # (D101) ZONE-RÉSIDENT dans la queue de la zone
                                            # données sup 1 (0x4B40-0x4BFF, après FIN_SUP_1
                                            # + marge 16) : code couvert par l'ENTRÉE DE
                                            # ZONE R10 — la table est PLEINE depuis
                                            # terrain.17 (28 entrées, miroir D95/D96/D99 :
                                            # tout bloc neuf vit sous une couverture
                                            # EXISTANTE, jamais comme entrée neuve)
]
ENTREE = 0x1400    # AddressOfEntryPoint = sup-01

NOMS_BLOCS = dict(LD.NOMS_BLOCS) | {   # LD fusionne déjà L2 (M2 ⊂ démo)
    "f60001": "sup-principal", "f60002": "sup-fenetre", "f60009": "sup-scenario",
    "f60011": "sup-journal", "f60021": "sup-horodatage", "f60022": "sup-balaye",
    "f60031": "sup-lanceur", "f60033": "sup-test-demo", "f60034": "sup-test-proxy",
    "f60035": "sup-test-envoi", "f60036": "sup-fichiers", "f60037": "sup-kit",
    "f60038": "sup-test-tunnel", "f60039": "sup-prevol",
}

# --- .text2 : zones ----------------------------------------------------------------

ZONE_THR = (0x4300, 0x433F)          # tcp-06
ZONE_DATA_SUP = (0x4340, 0x4BFF)     # lignes S + fixtures + étiquettes + URLs (RX)
                                     # terrain.18 (D101) : le PRÉVOL f60039 vit dans la
                                     # queue de zone (0x4B40-0x4BFF) — code RX couvert
                                     # par l'entrée DE ZONE R10 (table PLEINE D95/D96)
ZONE_PREVOL = (0x4B40, 0x4BFF)       # sup-39 — orphelins + réseau amont (D101)
PREVOL = 0x4B40                      # entrée publique : sup-09:R4 l'appelle AVANT
                                     # l'extraction (un proxy.exe orphelin VERROUILLE
                                     # le fichier à extraire et tient le port 25000)
ZONE_SCENARIO = (0x4C00, 0x4DFF)     # sup-09
ZONE_FICHIERS = (0x4E00, 0x4FBF)     # sup-36 (lecture/écriture/suppression)
ZONE_MIROIR = (0x5000, 0x51FF)       # win-05 scellé
ZONE_LANCEUR = (0x5200, 0x53BF)      # sup-31 (0x1C0)
ZONE_T1 = (0x5400, 0x57BF)           # sup-33
ZONE_T2 = (0x5800, 0x5DBF)           # sup-34 (0x5C0)
ZONE_T3 = (0x5E00, 0x62BF)           # sup-35 (0x4C0)
ZONE_KIT = (0x6600, 0x69FF)          # sup-37 — .extraire @0x6600, .nettoyage @0x6800 (D49)
ZONE_DATA_SUP_3 = (0x6A00, 0x71FF)   # lignes S04-S07 + md5 + T4 (fixtures + ps1,
                                     #  terrain.17 : 0x400 -> 0xC00, la zone suit le kit)
ZONE_T4 = (0x7200, 0x7FFF)           # sup-38 test T4 — tunnel TLS M4 (terrain.17 ;
                                     #  terrain.17-D : étendue à 0x800 — le diagnostic
                                     #  .temoin/.exitline vit dans le même slot, la
                                     #  section .text2 s'arrête là avant .rsrc @0x8000)
EXTRACTION = 0x6600                  # entrée publique de sup-37 (D49)
NETTOYAGE = 0x6800                   # HISTORIQUE : le mode 1 (nettoyage) est
                                     # dispatché à l'entrée unique 0x6600

# --- Entrées de win-05 scellé (miroir écran + fichier, D37 — mêmes adresses
# que la démo : le bloc est embarqué octet-identique, ses points d'entrée
# vivent dans SON slot 0x5000-0x51FF) -----------------------------------------

JOURNAL_TRACE = 0x5000      # entrée trace de win-05 (4 args ASCII, prologue
                            # à l'instruction 0 — verrou pile-alignee)
JOURNAL_GUI = 0x5100        # entrée scénario (utf16, nchars) : force mode 2 (shim
                            # en fin de slot, saute au début du bloc)
ZONE_DATA_SUP_2 = (0x6300, 0x65FF)   # INT/hints k32#3 + u32#2 + noms + cmdlines

# --- .rdata : structures PE ---------------------------------------------------------
# Le TABLEAU des descripteurs (contigu, terminé par zéros — le chargeur
# parcourt une suite, pas une liste chaînée) vit @0x2380 : six descripteurs
# + terme = 140 o tiennent entre l'IAT user32#2 (fin 0x2380) et la table R10
# (0x2450). L'ancrage démo @0x2030 est IMPOSSIBLE ici : 7 descripteurs
# (160 o) chevaucheraient l'IAT kernel32#1 scellée @0x20B0 (défaut latent
# du plan initial corrigé avant la notation — D48).
R_DESC_IMPORT = 0x2380      # descripteur kernel32#1 (FT figée 0x20B0)
R_DESC_USER32 = 0x2394
R_DESC_GDI32 = 0x23A8
R_DESC_K32B = 0x23BC        # kernel32#2 (héritage démo, D36)
R_DESC_K32C = 0x23D0        # kernel32#3 (terrain, D48)
R_DESC_U32B = 0x23E4        # user32#2 (terrain, D48)
R_DESC_TERM = 0x23F8        # terminateur (6 descripteurs + terme = 140 o)
R_IAT = 0x20B0              # IAT kernel32#1 — SCELLÉE (R7), 11 slots, ordre figé
R_INT_KERNEL32 = 0x2110     # INT kernel32#1 (12 qwords)
R_HN_GSH, R_HN_WF, R_HN_EP = 0x21F4, 0x2203, 0x220F    # hints M0 (héritage démo)
R_HN_CT = 0x2170            # hints kernel32 M2 (héritage démo)
R_HN_VP = 0x217F
R_HN_ICS = 0x2190
R_HN_ECS = 0x21AC
R_HN_LCS = 0x21C3
R_HN_RF = 0x21DA
R_HN_CH = 0x21E5
R_HN_GMH = 0x22A0            # hint GetModuleHandleW (héritage démo)
R_NOM_DLL = 0x2220          # kernel32.dll (héritage démo)
R_HN_GMFA = 0x2704           # hint k32#2 GetModuleFileNameA (héritage démo)
R_HN_CFA = 0x22C0            # hint k32#2 CreateFileA (interstice, héritage démo)
R_HN_FFB = 0x22DD            # hint k32#2 FlushFileBuffers
R_HN_GLE = 0x22CE            # hint k32#2 GetLastError
R_IAT_K32C = 0x2300         # IAT kernel32#3 — 9 slots + terme (D48, zone ws2 libérée)
R_IAT_U32B = 0x2360         # IAT user32#2 — 3 slots + terme (D48)
R_INT_K32B = 0x2720         # INT kernel32#2 (5 qwords — héritage démo)
R_RELOC = 0x2760            # BASERELOC minimal (12 o, entrées ABSOLUTE)
R_INT_USER32 = 0x2780       # INT user32 (15 qwords)
R_IAT_USER32 = 0x2800       # IAT user32 — SCELLÉE (R7), 14 slots
R_HN_USER32 = 0x2880        # hints user32 (14 entrées)
R_INT_GDI32 = 0x2970        # INT gdi32 (2 qwords, héritage démo)
R_IAT_GDI32 = 0x2980        # IAT gdi32 (1 slot)
R_HN_GDI32 = 0x2990         # hint GetStockObject
R_NOM_USER32 = 0x29A8       # "user32.dll\0"
R_NOM_GDI32 = 0x29B3        # "gdi32.dll\0"
R_UTF16 = 0x29C0            # chaînes UTF-16 (pose contrainte, voir ci-dessous)
R_ASCII = 0x2EA8            # chaînes ASCII de trace (pose contrainte)
R_IAT_K32B = 0x2E80         # IAT kernel32#2 — SCELLÉE (héritage démo, 4 slots)

IAT_SLOTS = {
    # kernel32#1 — inchangé (héritage M0/M2/démo, R7)
    "GetStdHandle": 0x20B0, "WriteFile": 0x20B8, "ExitProcess": 0x20C0,
    "CreateThread": 0x20C8, "VirtualProtect": 0x20D0,
    "InitializeCriticalSection": 0x20D8, "EnterCriticalSection": 0x20E0,
    "LeaveCriticalSection": 0x20E8, "ReadFile": 0x20F0, "CloseHandle": 0x20F8,
    "GetModuleHandleW": 0x2100,
    # user32 — inchangé (héritage démo, R7)
    "RegisterClassExW": 0x2800, "CreateWindowExW": 0x2808,
    "DefWindowProcW": 0x2810, "GetMessageW": 0x2818,
    "TranslateMessage": 0x2820, "DispatchMessageW": 0x2828,
    "PostQuitMessage": 0x2830, "DestroyWindow": 0x2838,
    "SendMessageW": 0x2840, "LoadCursorW": 0x2848,
    "EnableWindow": 0x2850, "MoveWindow": 0x2858, "GetClientRect": 0x2860,
    "MessageBoxW": 0x2868,
    # gdi32 — inchangé
    "GetStockObject": 0x2980,
    # kernel32#2 — inchangé (héritage démo, D36)
    "GetModuleFileNameA": 0x2E80, "CreateFileA": 0x2E88,
    "FlushFileBuffers": 0x2E90, "GetLastError": 0x2E98,
    # kernel32#3 — NOUVEAU (terrain, D48 ; l'ancienne IAT ws2_32 est libérée :
    # le superviseur n'a pas de sockets — le réseau vit dans les processus
    # testés et dans curl.exe)
    "CreateProcessA": 0x2300, "CreatePipe": 0x2308,
    "WaitForSingleObject": 0x2310, "GetExitCodeProcess": 0x2318,
    "TerminateProcess": 0x2320, "GetLocalTime": 0x2328,
    "DeleteFileA": 0x2330, "PeekNamedPipe": 0x2338, "Sleep": 0x2340,
    # user32#2 — NOUVEAU (terrain, D48)
    "FindWindowW": 0x2360, "FindWindowExW": 0x2368,
    "SendMessageTimeoutW": 0x2370,
}
KERNEL32_IMPORTS = L2.KERNEL32_IMPORTS + ["GetModuleHandleW"]      # 11 (figé)
KERNEL32B_IMPORTS = ["GetModuleFileNameA", "CreateFileA",
                     "FlushFileBuffers", "GetLastError"]           # 4 (figé)
KERNEL32C_IMPORTS = ["CreateProcessA", "CreatePipe", "WaitForSingleObject",
                     "GetExitCodeProcess", "TerminateProcess", "GetLocalTime",
                     "DeleteFileA", "PeekNamedPipe", "Sleep"]      # 9 (D48)
USER32_IMPORTS = ["RegisterClassExW", "CreateWindowExW", "DefWindowProcW",
                  "GetMessageW", "TranslateMessage", "DispatchMessageW",
                  "PostQuitMessage", "DestroyWindow", "SendMessageW",
                  "LoadCursorW", "EnableWindow", "MoveWindow", "GetClientRect",
                  "MessageBoxW"]                                    # 14 (figé)
USER32B_IMPORTS = ["FindWindowW", "FindWindowExW", "SendMessageTimeoutW"]   # 3
GDI32_IMPORTS = ["GetStockObject"]

# --- .rdata : table R10 (win-06 scellé lit @0x2450, ancre @0x2620, version @0x2628)

R_TAB_SUM = 0x2450          # 21 blocs + 2 zones données + terminateur = 24 entrées
R_ANCRE = 0x2620            # ancre de base (PI, D33)
R_VERSION = 0x2628          # qword version (R10, monotonie)
R_FIX_MEMCPY = 0x2630       # fixtures win-06 scellé (adresses figées)
R_FIX_MEMCMP_A = 0x2640
R_FIX_STRLEN = 0x264C
R_FIX_ITOA = 0x265A

FIXTURE_MEMCPY = b"TRIADE-M2-DEMO!!"
FIXTURE_MEMCMP_A = b"aaa\x00abc\x00aab\x00"
FIXTURE_STRLEN = b"porte-libc-ok\x00"
FIXTURE_ITOA = b"25000\x00"

# --- .rdata : chaînes UTF-16 (pose CONTRAINTE — win-04 scellé lit à ces adresses)
# Le titre fait 26 caractères + NUL pour que TXT_BOUTON retombe À L'OCTET
# 0x2A1E (adresse scellée par win-04) : contrainte de pose documentée (D48).

_SEQ_UTF16 = [
    ("CLASSE", "TRIADE_superviseur"),        # 0x29C0 (18 ch + NUL = 38 o)
    ("TITRE", "TRIADE superviseur terrain"),  # 0x29E6 (26 ch + NUL = 54 o + 2 pad)
    ("TXT_BOUTON", "TOUT DÉMARRER"),          # 0x2A1E — SCELLÉ par win-04
    ("CLASSE_EDIT", "EDIT"),                  # 0x2A3A — SCELLÉ par win-04
    ("CLASSE_BOUTON", "BUTTON"),              # 0x2A44 — SCELLÉ par win-04
    ("CHAINE_VIDE", ""),                      # 0x2A52 — SCELLÉ par win-04
    ("MSG_ECHEC_GUI", "création de fenêtre impossible"),
    ("CLASSE_DEMO", "TRIADE_demo"),           # cible FindWindowW de sup-33
]

CHAINES_UTF16 = {}
_cur = R_UTF16
for _nom, _texte in _SEQ_UTF16:
    if _nom == "TXT_BOUTON":
        _cur = 0x2A1E      # pad de 2 o après TITRE (26 ch) — contrainte scellée
    if _nom == "TXT_BOUTON":
        assert _cur == 0x2A1E, f"pose UTF-16 : TXT_BOUTON à 0x{_cur:x} != 0x2A1E (scellé)"
    if _nom == "CLASSE_EDIT":
        assert _cur == 0x2A3A, f"CLASSE_EDIT à 0x{_cur:x} != 0x2A3A (scellé)"
    if _nom == "CLASSE_BOUTON":
        assert _cur == 0x2A44, f"CLASSE_BOUTON à 0x{_cur:x} != 0x2A44 (scellé)"
    if _nom == "CHAINE_VIDE":
        assert _cur == 0x2A52, f"CHAINE_VIDE à 0x{_cur:x} != 0x2A52 (scellé)"
    CHAINES_UTF16[_nom] = (_cur, _texte, len(_texte))
    _cur += 2 * (len(_texte) + 1)
FIN_UTF16 = _cur
assert FIN_UTF16 <= 0x2E80, "zone UTF-16 déborde sur l'IAT kernel32#2"

# --- .rdata : chaînes ASCII de trace (pose CONTRAINTE — adresses scellées win-04)

# La fenêtre 0x2EA8-0x3000 est SCELLÉE par win-04 (L02 @0x2F10, L03, LKO_*,
# L4C, L4D — adresses ET longueurs figées dans le bloc) : la pose commence
# par 104 o de remplissage pour retomber PILE sur L02 @0x2F10, puis les
# chaînes scellées contiguës. Défaut latent du plan initial corrigé avant
# la notation : L00 terrain (49 o) décalait la séquence d'un cran et LKO_GUI
# écrasait L02 @0x2F10 (D48).
_SEQ_ASCII = [
    ("PAD_L02", b"\x00" * 104),                                       # 0x2EA8 (ancre scellée L02)
    ("L02", b"L02 controles crees (journal, bouton)"),               # 0x2F10 — SCELLÉ (37 o)
    ("L03", b"L03 clic : lancement du scenario"),                    # 0x2F35 — SCELLÉ
    ("LKO_EDIT", b"LKO creation du journal (EDIT) echouee gle="),    # 0x2F55 — SCELLÉ
    ("LKO_BOUTON", b"LKO creation du bouton echouee gle="),          # 0x2F80 — SCELLÉ
    ("LKO_SPAWN", b"LKO lancement thread scenario echoue gle="),     # 0x2FA3 — SCELLÉ
    ("PAD_L4C", b"\x00" * 17),                                       # 0x2FCC (alignement scellé)
    ("L4C", b"L4C move journal="),                                   # 0x2FDD — SCELLÉ
    ("L4D", b"L4D move bouton="),                                    # 0x2FEE — SCELLÉ
]

# Chaînes ASCII LIBRES (aucun lecteur scellé — sup-02/sup-33/sup-34
# nouveaux) : posées dans l'espace UTF-16 libéré par la disparition des
# lignes J_* de la démo (après CLASSE_DEMO, avant l'IAT kernel32#2).
R_ASCII_LIBRE = 0x2AAA
_SEQ_ASCII_LIBRE = [
    ("L00", b"L00 demarrage superviseur terrain 0.5.0-terrain17"),   # 49 o
    ("L01", b"L01 fenetre principale creee"),                        # 28 o
    ("LKO_GUI", b"LKO creation fenetre impossible gle="),            # 36 o
    ("NOM_DEMO", b"demo.exe\x00"),                                   # 9 o (cmdline T1)
    ("NOM_PROXY", b"proxy.exe\x00"),                                 # 10 o (cmdline T2)
    ("QUIT", b"quit\r\n"),                                           # 6 o (stdin proxy)
]
assert R_ASCII_LIBRE >= FIN_UTF16, "zone ASCII libre chevauche l'UTF-16"

CHAINES_ASCII = {}
_cur = R_ASCII
for _nom, _octets in _SEQ_ASCII:
    _attendu = {"L02": 0x2F10, "L03": 0x2F35, "LKO_EDIT": 0x2F55,
                "LKO_BOUTON": 0x2F80, "LKO_SPAWN": 0x2FA3,
                "L4C": 0x2FDD, "L4D": 0x2FEE}
    if _nom in _attendu:
        assert _cur == _attendu[_nom], \
            f"pose ASCII : {_nom} à 0x{_cur:x} != 0x{_attendu[_nom]:x} (scellé)"
    CHAINES_ASCII[_nom] = (_cur, _octets, len(_octets))
    _cur += len(_octets)
assert _cur <= 0x3000, "zone ASCII trace débordante"
_cur = R_ASCII_LIBRE
for _nom, _octets in _SEQ_ASCII_LIBRE:
    CHAINES_ASCII[_nom] = (_cur, _octets, len(_octets))
    _cur += len(_octets)
assert _cur <= R_IAT_K32B, "zone ASCII libre débordante sur l'IAT kernel32#2"
LONGUEURS_ASCII = {n: len(o) for n, (_a, o, _l) in CHAINES_ASCII.items()}

# --- .text2 zone données sup 1 : lignes S + fixtures + étiquettes + URLs (0x4340+)

_SEQ_SUP_1 = [
    # en-tête scénario
    ("S00", b"S00 superviseur terrain 0.5.0-terrain17"),
    ("S01_PREFIXE", b"S01 date "),
    ("S02A", b"S02 porte R10 : integrite VERTE"),
    ("S02B", b"S02 porte R10 : KO - arret"),
    ("S03A", b"S03 libc M1 scellee : 4/4 verts"),
    ("S03B", b"S03 libc : vecteur en echec"),
    # T1 — démo
    ("S10", b"S10 T1 demo 0.3.0 : lancement demo.exe"),
    ("S10B", b"S10 T1 demo.exe ABSENT"),
    ("S11A", b"S11 T1 fenetre demo detectee"),
    ("S11B", b"S11 T1 fenetre demo ABSENTE"),
    ("S12A", b"S12 T1 clic TOUT DEMARRER envoye"),
    ("S12B", b"S12 T1 clic timeout"),
    ("S13", b"S13 T1 demo.exe termine code="),
    ("S14", b"S14 T1 lignes journal demo="),
    ("S15A", b"S15 T1 verdict journal : conforme"),
    ("S15B", b"S15 T1 verdict journal : NON conforme"),
    ("S16A", b"S16 T1 VERDICT OK"),
    ("S16B", b"S16 T1 VERDICT KO"),
    # T2 — proxy
    ("S20", b"S20 T2 proxy 0.4.0-dev.1 : lancement"),
    ("S20B", b"S20 T2 proxy.exe ABSENT"),
    ("S21A", b"S21 T2 banniere proxy recue"),
    ("S21B", b"S21 T2 banniere ABSENTE"),
    ("S22A", b"S22 T2 curl http : code="),
    ("S22B", b"S22 T2 curl.exe ABSENT"),
    ("S23", b"S23 T2 page http octets="),
    ("S24", b"S24 T2 curl https : code="),
    ("S25", b"S25 T2 page https octets="),
    ("S26", b"S26 T2 journal proxy lignes="),
    ("S27A", b"S27 T2 verdict console : conforme"),
    ("S27B", b"S27 T2 verdict console : NON conforme"),
    ("S28A", b"S28 T2 VERDICT OK"),
    ("S28B", b"S28 T2 VERDICT KO"),
    # T3 — envoi Drive
    ("S30", b"S30 T3 envoi Drive : lecture jetons"),
    ("S31", b"S31 T3 jetons absents - envoi saute"),
    ("S32", b"S32 T3 requete OAuth composee"),
    ("S33A", b"S33 T3 jeton OAuth obtenu"),
    # D68 (terrain.14+) : l'échec jeton se journalise via le relais mode 1 —
    # « S33 T3 jeton KO code=NN » (NN = code de sortie curl, lu @0x3B50).
    # L'ancienne chaîne « jeton OAuth ECHEC » survit comme orpheline dans les
    # binaires de livraison (handler @0x6113 remplacé par jmp -> relais 0x628A).
    ("S33B", b"S33 T3 jeton KO code="),
    ("S34A", b"S34 T3 session upload ouverte"),
    ("S34B", b"S34 T3 session upload ECHEC"),
    ("S35A", b"S35 T3 journal televerse : OK"),
    ("S35B", b"S35 T3 televersement ECHEC"),
    ("S36A", b"S36 T3 VERDICT OK"),
    ("S36B", b"S36 T3 VERDICT KO"),
    # verdict final
    ("S90", b"S90 SUPERVISEUR : TOUT OK"),
    ("S91", b"S91 SUPERVISEUR : ECHEC (voir lignes KO)"),
    # fixtures d'événements (comparaisons memcmp exactes)
    ("FIX_BANNIERE", b"TRIADE M3 : proxy demarre (port 25000)\r\n"),
    ("FIX_EVT_HTTP", b"connexion entrante\r\nfin connexion\r\n"),
    ("FIX_EVT_HTTPS", b"connexion entrante\r\ntunnel\r\nfin connexion\r\n"),
    ("FIX_ARRET", b"arret\r\n"),
    ("FIX_FINAL_DEMO", "boucle § 5 complète - DÉMO OK\r\n".encode("cp1252")),
    # étiquettes du balayeur (sup-22)
    # D69 : Google répond en JSON INDENTÉ — "access_token": "ya29…" (un
    # espace après les deux-points ; preuve : le json du run terrain.14 et un
    # rafraîchissement frais du bac, byte-identiques). L'étiquette se termine
    # sur le guillemet OUVRANT de la valeur ; 16 o — même longueur que
    # l'ancienne forme compacte, l'immédiat r9d=0x10 du site d'appel reste
    # exact.
    ("ETIQ_TOKEN", b"access_token\": \""),
    ("ETIQ_LOCATION", b"Location: "),
    ("ETIQ_ID", b"\"id\""),
    # URLs et constantes Drive (voie drive_sync.py, D48)
    ("URL_TOKEN", b"https://oauth2.googleapis.com/token"),
    ("URL_UPLOAD", b"https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable"),
    ("DOSSIER_TEST", b"1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0\x00"),
    # gabarits de composition (formatteur à marqueurs de sup-35 : 0x01=cid,
    # 0x02=secret, 0x03=refresh, 0x04=nom du run, 0x05=id dossier, 0x06=chemin
    # du journal, 0x07=TAMPON_JETON, 0x08=uri des jetons — un seul formateur,
    # zéro découpe de gabarit, D48)
    ("GABARIT_OAUTH",
     b"client_id=\x01&client_secret=\x02&refresh_token=\x03&grant_type=refresh_token\x00"),
    ("GABARIT_META", b"{\"name\":\"\x04\",\"parents\":[\"\x05\"]}\x00"),
    # D65 : --fail retiré des 2 requêtes Google (une erreur HTTP doit ÉCRIRE
    # sa réponse — la preuve survit) ; 8 espaces, longueur 81 o inchangée.
    ("GABARIT_JETON",
     b"curl.exe -s        --max-time 30 -o terrain_jeton.json "
     b"--data @terrain_req.txt \x08\x00"),
    # D69 : HTTP/1.1 FORCÉE + -m 30 (forme courte) : en HTTP/2, curl -D
    # écrit les en-têtes en minuscules (location:) et l'étiquette
    # « Location: » raterait ; en HTTP/1.1 Google répond « Location: » (casse
    # classique — sonde bac D69, octet ~194 d'un dump ~846 o, sous la limite
    # de lecture 600 o). 6 espaces de bourrage, longueur 232 o inchangée.
    ("GABARIT_SESSION",
     b"curl.exe -s --http1.1 -m 30      -o NUL -D terrain_session.txt "
     b"-X POST -H \"Content-Type: application/json\" "
     b"-H \"Authorization: Bearer \x07\" "
     b"--data @terrain_meta.json "
     b"https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable\x00"),
    # D70 : le chemin du journal est un CHEMIN COMPLET Windows — il contient
    # le plus souvent un ESPACE (« My Drive », « Jean Dupont ») : sans
    # guillemets, curl lirait --data-binary @"C:\Users\Jean" et échouerait.
    # Guillemets ajoutés ; --max-time 120 → -m 120 (8 o libérés) : longueur
    # totale 67 o inchangée. Le PUT n'avait JAMAIS tourné en réel avant D70.
    ("GABARIT_PUT",
     b"curl.exe -s --fail -m 120 -o NUL -X PUT --data-binary @\"\x06\""
     + b" " * 7 + b"\x07\x00"),
]

CHAINES_SUP = {}
_cur = ZONE_DATA_SUP[0]
for _nom, _octets in _SEQ_SUP_1:
    CHAINES_SUP[_nom] = (_cur, _octets, len(_octets))
    _cur += len(_octets)
assert _cur <= ZONE_DATA_SUP[1] + 1, f"zone données sup 1 débordante (fin 0x{_cur:x})"
FIN_SUP_1 = _cur
assert FIN_SUP_1 + 16 <= ZONE_PREVOL[0], "prévol : marge < 16 o après les chaînes zone 1"

# --- .text2 zone données sup 2 : noms de fichiers + cmdlines curl complètes (0x6000+)

_SEQ_SUP_2 = [
    ("NOM_JETONS", b"terrain_jetons.bin\x00"),
    # D68/D96 : les QUATRE temporaires du nettoyage T3 sont CONTIGUS —
    # terrain_jeton.json vit APRÈS rep (la réponse de Google SURVIT au run,
    # la preuve doit rester sur disque : jamais dans le chemin de la marche)
    ("NOM_REQ", b"terrain_req.txt\x00"),
    ("NOM_META", b"terrain_meta.json\x00"),
    ("NOM_SESSION", b"terrain_session.txt\x00"),
    ("NOM_REP", b"terrain_rep.json\x00"),
    ("NOM_JETON_JSON", b"terrain_jeton.json\x00"),
    ("NOM_PAGE_HTTP", b"terrain_page_http.txt\x00"),
    ("NOM_PAGE_HTTPS", b"terrain_page_https.txt\x00"),
    ("NOM_CURL", b"curl.exe\x00"),
    ("NOM_JOURNAL_DEMO", b"demo_journal.txt\x00"),
    ("CMD_CURL_HTTP",
     b"curl.exe -s --fail --max-time 20 -o terrain_page_http.txt "
     b"-x http://127.0.0.1:25000 http://neverssl.com/\x00"),
    ("CMD_CURL_HTTPS",
     b"curl.exe -s --fail --max-time 20 -o terrain_page_https.txt "
     b"-x http://127.0.0.1:25000 https://example.com/\x00"),
]

_cur = ZONE_DATA_SUP_2[0]
for _nom, _octets in _SEQ_SUP_2:
    CHAINES_SUP[_nom] = (_cur, _octets, len(_octets))
    _cur += len(_octets)
FIN_SUP_2 = _cur
assert FIN_SUP_2 <= ZONE_DATA_SUP_2[1] + 1, "zone données sup 2 débordante"

# --- .text2 zone données sup 3 : lignes du kit embarqué (D49, 0x6A00+) ---------
# Les md5 affichés sont les constantes du plan — le build ASSERT leur
# cohérence avec les artefacts scellés avant d'embarquer les octets.

MD5_DEMO_HEXA = b"73c064fbaf4610a167bc6434dee400e4"
# D63 (terrain.11+) : proxy re-scellé après le correctif de pile http-10:R3.
# D96 (terrain.17) : le kit embarque le proxy M4 scellé D95 — le tunnel TLS
# voyage dans le superviseur ; md5/sha256 assertés au build contre l'artefact.
# D102 (terrain.18/17-G) : le kit embarque le proxy M4 RECONSTRUIT — tls-07:R2
# scan PAR TYPE (Schannel reclasse [0]=STREAM_HEADER/[1]=DATA/[3]=EXTRA —
# l'anomalie 13 octets 17-C/17-F ÉTEINTE : le clair est enfin relayé).
MD5_PROXY_HEXA = b"2b6481a1e76fbd8e245cd03d883e36c7"
SHA256_PROXY_HEXA = b"b9264e0b6aef460f86c54ec0c4d38ebe90ca58b841fec7a09257e813ff6545cf"
LONGUEUR_DEMO = 16384                     # demo.exe 0.3.0 (M2 scellé)
LONGUEUR_PROXY = 28160                    # proxy.exe 0.5.0-dev.2 (M4 scellé D95)
LONGUEUR_ANNEXE = 248                     # terrain_jetons.bin (D48)

_SEQ_SUP_3 = [
    ("S04A", b"S04 demo.exe extrait, octets conformes"),
    ("S04B", b"S04B demo.exe : octets ECART - T1 saute"),
    ("S04C", b"S04C md5 demo.exe " + MD5_DEMO_HEXA),
    ("S04D", b"S04D extraction demo.exe : echec ecriture"),
    ("S05A", b"S05 proxy.exe extrait, octets conformes"),
    ("S05B", b"S05B proxy.exe : octets ECART - T2 et T4 sautent"),
    ("S05C", b"S05C md5 proxy.exe " + MD5_PROXY_HEXA),
    ("S05D", b"S05D extraction proxy.exe : echec ecriture"),
    ("S06A", b"S06 annexe jetons extraite - T3 actif"),
    ("S06B", b"S06 variante publique - annexe absente, T3 non applicable"),
    ("S06C", b"S06C annexe jetons : octets ECART"),
    ("S07A", b"S07 nettoyage kit effectue (demo, proxy, annexe)"),
    # T4 (terrain.17) : le client de la passerelle M4 — la forme absolue
    # « GET https://… HTTP/1.1 » n'existe dans AUCUN client standard (curl
    # envoie CONNECT) : powershell.exe + script TCP brut (FIX_PS1), lancé
    # par sup-31 MODE 0, chemin RELATIF (cwd forcé = répertoire de l'exe —
    # la leçon D36 des chemins relatifs travaille pour nous ici : aucun
    # guillemet à composer, aucun espace à craindre).
    ("NOM_PS1", b"terrain_m4.ps1\x00"),
    ("NOM_PAGE_M4A", b"page_m4a.txt\x00"),
    ("NOM_PAGE_M4B", b"page_m4b.txt\x00"),
    ("CMD_PS_M4A",
     b"powershell.exe -NoProfile -ExecutionPolicy Bypass -File "
     b"terrain_m4.ps1 example.com a\x00"),
    ("CMD_PS_M4B",
     b"powershell.exe -NoProfile -ExecutionPolicy Bypass -File "
     b"terrain_m4.ps1 self-signed.badssl.com b\x00"),
    # T4 — tunnel TLS M4 (terrain.17, D96 : le critère M4 « HTTPS en transit ;
    # échec propre sur certificat invalide » atterrit dans le run terrain)
    ("S40", b"S40 T4 tunnel M4 : script terrain_m4.ps1 pose"),
    ("S40B", b"S40B T4 script NON POSE - rien lance"),
    ("S41A", b"S41 T4 proxy 0.5.0-dev.2 : lancement"),
    ("S41B", b"S41 T4 proxy.exe ABSENT"),
    ("S42A", b"S42 T4 banniere proxy recue"),
    ("S42B", b"S42 T4 banniere ABSENTE"),
    ("S43A", b"S43 T4 powershell exemple : code="),
    ("S43B", b"S43 T4 powershell.exe ABSENT"),
    ("S44A", b"S44 T4 page exemple octets="),
    ("S45A", b"S45 T4 powershell badssl : code="),
    ("S46A", b"S46 T4 page badssl octets="),
    ("S49A", b"S49 T4 VERDICT OK (console conforme)"),
    ("S49B", b"S49 T4 VERDICT KO (console NON conforme)"),
    # fixtures T4 — CROISÉES au build contre les octets de l'artefact embarqué
    # (pefile RVA→offset : jamais deux sources de vérité)
    ("FIX_200", b"HTTP/1.1 200"),
    ("FIX_502_M4", b"HTTP/1.1 502 Certificat rejete\r\n\r\n"),
    ("FIX_EVT_M4A", b"connexion entrante\r\ntunnel chiffre etabli\r\nfin connexion\r\n"),
    ("FIX_EVT_M4B", b"connexion entrante\r\ncertificat rejete\r\nfin connexion\r\n"),
    ("FIX_PS1", b'param([string]$m,[string]$o)\r\ntry{\r\n$c=New-Object Net.Sockets.TcpClient(\'127.0.0.1\',25000)\r\n$c.ReceiveTimeout=30000\r\n$s=$c.GetStream()\r\n$r=[Text.Encoding]::ASCII.GetBytes("GET https://$m/ HTTP/1.1`r`nHost: $m`r`nConnection: close`r`n`r`n")\r\n$s.Write($r,0,$r.Length)\r\n$b=New-Object byte[] 65536\r\n$f=[IO.File]::Create("page_m4$o.txt")\r\nwhile(($n=$s.Read($b,0,65536)) -gt 0){$f.Write($b,0,$n)}\r\n$f.Close();$c.Close();exit 0\r\n}catch{exit 1}\r\n'),
    # terrain.17-D (D99) : le TÉMOIN de la page A (l'évidence qui manquait au
    # run 17-C — 13 octets livrés, contenu inconnu) + l'étiquette de la ligne
    # S47 (le code de sortie du proxy journalisé — exit 0 confirme le chemin
    # propre, tout autre code nomme le mode de mort)
    ("NOM_TEMOIN_A", b"temoin_m4a.txt\x00"),
    ("S47", b"S47 T4 exit proxy="),
    # terrain.18 (D101) : le PRÉVOL — les ÉTAPES 0/0 BIS du protocole LISEZMOI
    # deviennent AUTOMATIQUES (demande développeur 29/10 : « peux-tu intégrer la
    # commande taskkill et la verif curl dans le superviseur ? » — le réflexe
    # manuel constaté runs après runs depuis D98). (1) taskkill tue les orphelins
    # d'un run antérieur AVANT l'extraction (un proxy.exe survivant verrouille le
    # FICHIER proxy.exe à re-poser et tient le PORT 25000) ; codes lus au
    # LISEZMOI : 0 = orphelins tués, 128 = introuvables (état PROPRE), autre =
    # refus/échec. (2) curl sonde l'AMONT DIRECT (sans proxy, exemple.com) :
    # code 0 = réseau vivant, 6/7/28 = DNS/connexion/timeout — le run 17-D est
    # mort de l'amont, pas du code : cette preuve naît désormais DANS le
    # journal, AVANT les tests. Les DEUX codes ne touchent JAMAIS le verdict
    # (une évidence, pas un juge — miroir du témoin D99 : résultat ignoré).
    ("CMD_TASKKILL",
     b"taskkill.exe /f /IM proxy.exe /IM demo.exe\x00"),
    ("CMD_CURL_AMONT",
     b"curl.exe -s --max-time 20 -o NUL https://example.com/\x00"),
    ("S08", b"S08 orphelins proxy/demo : taskkill code="),
    ("S09", b"S09 reseau amont : curl code="),
]

_cur = ZONE_DATA_SUP_3[0]
for _nom, _octets in _SEQ_SUP_3:
    CHAINES_SUP[_nom] = (_cur, _octets, len(_octets))
    _cur += len(_octets)
FIN_SUP_3 = _cur
assert FIN_SUP_3 <= ZONE_DATA_SUP_3[1] + 1, "zone données sup 3 débordante"

# INT/hints des descripteurs #3 (kernel32#3, user32#2) vivent en fin de zone 2 :
# R_INT_K32C et R_INT_U32B + les hints correspondants.
R_INT_K32C = (FIN_SUP_2 + 0x10) & ~0xF       # INT kernel32#3 (10 qwords)
R_INT_U32B = R_INT_K32C + 0x50               # INT user32#2 (4 qwords)
R_HN_K32C = R_INT_U32B + 0x20                # hints k32#3 (9)
R_HN_U32B = R_HN_K32C + 0xA0                 # hints u32#2 (3)
assert R_HN_U32B + 0x40 <= ZONE_DATA_SUP_2[1] + 1, "INT/hints #3 débordants"

# --- .rdata : motif loader D54 (terrain.17-B — LEÇON MACHINE RÉELLE) -----------
# La machine cible (Windows 11 build 26300, Insider) résout kernel32#3 et
# user32#2 par le CHEMIN FirstThunk : les slots IAT du fichier doivent porter
# des pointeurs de hints VALABLES, et hints + INT vivent en .rdata NON
# exécutable (leçon terrain.4/terrain.5, D54). Le correctif vivait seulement
# dans l'arbre local du terrain.16 — jamais committé : la régénération D96
# l'a perdu, le run machine réelle l'a nommé (fenêtre jamais créée, journal
# jamais ouvert, processus mort avant l'entrée). Adresses FIXES = celles du
# terrain16, prouvées sur la machine ; la copie .text2 ci-dessus reste DONNÉE
# MORTE couverte par la table R10 (aucun octet couvert ne bouge).
R_INT_K32C_RDATA = 0x2B40      # INT kernel32#3 en .rdata (9 qwords + terme)
R_INT_U32B_RDATA = 0x2B90      # INT user32#2 en .rdata (3 qwords + terme)
HINTS_K32C_RDATA = {           # hints kernel32#3 — adresses terrain16
    "CreateProcessA": 0x2BB0, "CreatePipe": 0x2BC2,
    "WaitForSingleObject": 0x2BD0, "GetExitCodeProcess": 0x2BE6,
    "TerminateProcess": 0x2BFC, "GetLocalTime": 0x2C10,
    "DeleteFileA": 0x2C20, "PeekNamedPipe": 0x2C2E, "Sleep": 0x2C3E,
}
HINTS_U32B_RDATA = {           # hints user32#2 — adresses terrain16
    "FindWindowW": 0x2C46, "FindWindowExW": 0x2C54,
    "SendMessageTimeoutW": 0x2C64,
}
assert max(HINTS_U32B_RDATA.values()) + 24 <= 0x2C80, "hints .rdata débordants"

# --- Section .blob : kit embarqué (D49) ---------------------------------------------
# En-tête : u64 longueur démo, u64 longueur proxy (JAMAIS codées en dur dans
# le code — sup-37 les lit ici) ; les octets suivent ; l'emplacement annexe
# (u64 longueur + 248 o) est le SEUL point mutable de l'image : deux
# variantes, publiques (zéro) et livraison (annexe D48 intégrée).

BLOB_LONGUEURS = BLOB_RVA               # 0x8000 : u64 longueur demo
BLOB_LONGUEUR_PROXY = BLOB_RVA + 8      # 0x8008 : u64 longueur proxy
BLOB_DEMO = BLOB_RVA + 0x10             # 0x8010 : demo.exe 16 384 o
BLOB_PROXY = BLOB_DEMO + LONGUEUR_DEMO  # 0xC010 : proxy.exe 19 456 o
SLOT_JETONS = BLOB_PROXY + LONGUEUR_PROXY   # 0x10C10 : u64 + 248 o
TAILLE_SLOT_JETONS = 8 + LONGUEUR_ANNEXE    # u64 longueur + annexe D48
ZONE_BLOB_INTEG = (BLOB_LONGUEURS, SLOT_JETONS - 1)   # couverte par la table R10
assert BLOB_RVA + BLOB_VSIZE == SLOT_JETONS + TAILLE_SLOT_JETONS, "plan .blob incohérent"
assert ZONE_BLOB_INTEG[1] < SLOT_JETONS, "l'emplacement annexe doit rester hors table R10"

TAILLE_MORCEAU_KIT = 512                 # relecture de vérification (sup-37 P→Q1)

LONGUEURS_ASCII.update({n: len(o) for n, (_a, o, _l) in CHAINES_SUP.items()})

# --- .data : état (héritage + terrain) ------------------------------------------------

R_STDOUT, R_STDIN, R_LISTEN, R_QUIT = L2.R_STDOUT, L2.R_STDIN, L2.R_LISTEN, L2.R_QUIT
R_ETAT_PATCH, R_ENTREE_SAUVEE, R_CS = L2.R_ETAT_PATCH, L2.R_ENTREE_SAUVEE, L2.R_CS
R_CURSEUR, ARENE_BASE = L2.R_CURSEUR, L2.ARENE_BASE

HWND_PRINCIPAL = 0x3860     # handle de la fenêtre principale (sup-02)
HWND_JOURNAL = 0x3868       # handle du contrôle EDIT journal (win-04 scellé)
HWND_BOUTON = 0x3870        # handle du bouton unique (win-04 scellé)
DRAPEAU_WORKER = 0x3878     # 0 = scénario non lancé, 1 = lancé (win-04 scellé)
DRAPEAU_SRV = 0x3880        # héritage — HÔTE DU HANDLE PROXY (HPROC_PROXY,
                            # D48 : le global HPROC est écrasé par chaque spawn
                            # de curl, le handle proxy doit survivre aux curls —
                            # win-08 seul lecteur démo n'est PAS embarqué terrain)

R_JOURNAL_HANDLE = 0x3888   # handle du fichier journal (sup-11)
BUF_CONV = 0x3890           # tampon de composition (128 o — win-11/sup-11)
BUF_CHEMIN = 0x3910         # chemin complet du journal (304 o — sup-11, lu par sup-35)
SCRATCH_ECRIT = 0x3A40      # qword écrit (WriteFile lpNumberOfBytesWritten)
BUF_MIROIR = 0x3A50         # tampon UTF-16 du miroir écran (128 o — win-05 scellé)

# état terrain (D48) — 0x3AD0-0x3FEF
TAMPON_NOM = 0x3AD0         # "terrain_YYYYMMDD_HHMMSS.txt\0" (28 o, sup-21)
TAMPON_AFF = 0x3AF0         # "S01 date YYYYMMDD_HHMMSS" (24 o, sup-21)
ETAT_SUP = 0x3B10           # 96 o : handles, tuyaux, pid, codes
HPROC = 0x3B10              # dernier processus lancé (sup-31)
PID = 0x3B18
TUYAU_IN_RD = 0x3B20        # stdin du proxy — extrémité enfant (fermée après spawn)
TUYAU_IN_WR = 0x3B28        # stdin du proxy — extrémité parent (écriture "quit")
TUYAU_OUT_RD = 0x3B30       # stdout du proxy — extrémité parent (lecture)
TUYAU_OUT_WR = 0x3B38       # stdout du proxy — extrémité enfant (fermée après spawn)
HWND_DEMO = 0x3B40          # fenêtre de la démo (sup-33)
HWND_BTN_DEMO = 0x3B48      # bouton de la démo (sup-33)
CODE_SORTIE = 0x3B50        # code de sortie du dernier processus attendu
LU = 0x3B58                 # octets lus (ReadFile/PeekNamedPipe)
DISPO = 0x3B60              # octets disponibles (PeekNamedPipe)
DIR_LONG = 0x3B68           # longueur du répertoire de l'exe (préfixe de
                            # BUF_CHEMIN, séparateur compris — posé en cache
                            # par sup-36, un seul propriétaire du calcul)
TAMPON_JETON = 0x3B70       # 480 o : access_token puis URL de session (cycle séquentiel)
TAMPON_CMD = 0x3D50         # 688 o : chemins (sup-36) + lectures — composition DÉCOUPLÉE (D70)
assert TAMPON_CMD + 688 == 0x4000, "TAMPON_CMD doit finir pile à 0x4000"

# --- D70 : le tampon de composition déménage hors de TAMPON_CMD ------------------
# L'ancienne convention (chemins à +0, composés à +ZONE_COMPO=+0x150) offrait
# 352 o à la composition — la commande session RÉELLE (230 littéraux + jeton
# 254 o constatés au run terrain.15) en fait 484 : la boucle .gab écrivait
# au-delà de 0x4000, première page de .text2 (RX, non inscriptible) — mort
# instantanée du superviseur, « fermé tout seul ». La région .data
# [0x3000, 0x3860) est vierge (aucune référence de code, hors table R10) :
# TAMPON_COMPO y offre 1 888 o, DÉCOUPLÉS des chemins/lectures — plus aucune
# contrainte de coexistence. Quatre sites référent la base (lea 4 octets
# chacun) : sup-35 @0x5E0E (composition .gab), sup-36 @0x4F5C (source
# WriteFile), sup-37 @0x68D2/@0x6902 (lecture + memcmp de la vérif kit).
TAMPON_COMPO = 0x3100       # composition + vérification kit (sup-35/36/37)
FIN_COMPO = 0x3860          # premier octet d'état (HWND_PRINCIPAL)
assert TAMPON_COMPO >= DATA_RVA + 0x100, "TAMPON_COMPO : marge de section"
assert FIN_COMPO - TAMPON_COMPO == 1888, "TAMPON_COMPO : 1 888 o attendus"
# pires cas constatés/possibles : session 230+254 = 484 ; PUT 58 + chemin
# 304 (BUF_CHEMIN) + 7 + URL 480 (TAMPON_JETON) = 849
assert FIN_COMPO - TAMPON_COMPO >= max(230 + 254, 58 + 304 + 7 + 480), \
    "TAMPON_COMPO : capacité insuffisante pour les pires cas"
# L'ancienne constante disparaît : la composition ne vit plus dans TAMPON_CMD.
ZONE_COMPO = None           # HISTORIQUE D48-D69 — remplacée par TAMPON_COMPO (D70)

# --- Jetons de retour d'émulation (oracle, hors binaire) ------------------------------

SENTINELLE_RETOUR = L2.SENTINELLE_RETOUR

# --- Constantes à propriétaire unique (charte terrain/I) ------------------------------

MAX_LIGNE_JOURNAL = 100     # sup-11 P4 (modes 0/1, BUF_CONV 128 o)
MAX_CHARS_UTF16 = 60        # sup-11 P4 (mode 2)
MAX_TAMPON_CMD = 688        # capacité TAMPON_CMD (sup-35 P3)
MAX_TAMPON_JETON = 480      # capacité TAMPON_JETON
MAX_LECTURE = 640           # lecture max en un appel (sup-36, marge TAMPON_CMD)
ATTENTE_FENETRE = 200       # sup-33 : 200 x 50 ms = 10 s (FindWindowW)
ATTENTE_MARQUEUR = 150      # sup-33 : 150 x 200 ms = 30 s (journal démo)
ATTENTE_BANNIERE = 300      # sup-34 : 300 x 50 ms = 15 s
ATTENTE_EVENEMENTS = 300    # sup-34 : 300 x 50 ms = 15 s
ATTENTE_ARRET = 200         # sup-34 : 200 x 50 ms = 10 s
ATTENTE_PREVOL = 30000      # sup-39 : sonde bornée — taskkill OU curl amont
                            # (curl --max-time 20 s'autolimite ; 259 = STILL_ACTIVE
                            # si le plafond tombe, l'évidence reste brute, zéro gel)
