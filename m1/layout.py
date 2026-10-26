"""layout.py — Plan d'adressage du projet TRIADE, jalon M1 (profil x86-64-win11-pe).

Source unique de vérité partagée par build_m1.py, outils/auteur.py et
oracle_differentiel.py. Toute adresse du binaire selftest.exe dérive d'ici ;
la notation référence ces constantes et le builder vérifie la concordance.

HÉRITAGE M0 (R7 — jamais déplacé) :
  - blocs scellés io-01 write @ 0x1040 et io-02 exit @ 0x1080, octets identiques
    à hello.exe (réutilisation inter-artefacts, premier terrain de R7) ;
  - descripteurs d'import, hint/names, INT, IAT et BASERELOC aux RVA exactes de
    M0 (0x2030…0x20DB) : les déplacements RIP des blocs scellés l'exigent.

ZONES (.text, RVA 0x1000-0x1FFF) :
  zone io    0x1000-0x10FF : 0x1000 réservé (emplacement hello-main en M0, libre
                             dans les binaires ultérieurs), write, exit, 0x10C0
                             réservé io-03+ ;
  zone libc  0x1100-0x17FF : six blocs M1 puis réserve pour libc-08+ (memset y
                             entre en dev.2 sans rien déplacer — démonstration R7) ;
  zone app   0x1800-0x1FFF : blocs propres au binaire (autotest = point d'entrée).

Données (.rdata 0x2000) : structures PE héritées, puis vecteurs dorés et
messages du selftest. Arène (.data 0x3000) : curseur 8 octets puis, alignée
sur 64, la zone d'allocation (contractuelle pour align ∈ [1, 64] puissance de 2).
"""

# --- Image et sections --------------------------------------------------------

IMAGE_BASE = 0x140000000
TEXT_RVA, RDATA_RVA, DATA_RVA = 0x1000, 0x2000, 0x3000
FILE_ALIGN, SECT_ALIGN = 0x200, 0x1000
TEXT_VSIZE = 0x1000          # 0x1000-0x1FFF (zones io + libc + app)
RDATA_VSIZE = 0x1000         # 0x2000-0x2FFF
DATA_VSIZE = 0x1000          # 0x3000-0x3FFF
SIZE_OF_IMAGE = 0x4000
TEXT_FILE, RDATA_FILE, DATA_FILE = 0x200, 0x1200, 0x2200   # pointeurs fichiers
DATA_RAW = 0x200             # .data committée (curseur), queue BSS virtuelle
TAILLE_FICHIER = 0x2400      # 0x2200 + 0x200

DLL_CHARACTERISTICS = 0x0040 | 0x0020 | 0x0100   # DYNAMICBASE | HEVA | NX

VERSION_DEV1 = "0.2.0-dev.1"   # six blocs libc + autotest 18/18
VERSION_DEV2 = "0.2.0-dev.2"   # + memset, autotest 21/21
VERSION_RC1 = "0.2.0-rc.1"     # cristallisation (10 vérifications) + conformité verte
VERSION_FINALE = "0.2.0"        # validation terrain constatée (D32) — balise immuable § 9

# --- Blocs (couche C) ---------------------------------------------------------
# (id carte, spec, rva slot, taille slot, scellé-dès, phase d'entrée)
# a1xxxx = génération M0 ; b2xxxx = génération M1 (D28).

BLOCS_IO = [
    ("a10002", "hello-02:R1", 0x1040, 0x40, "M0", 1),   # write, réutilisé tel quel
    ("a10003", "hello-03:R1", 0x1080, 0x40, "M0", 1),   # exit, réutilisé tel quel
]

BLOCS_LIBC = [
    ("b20001", "libc-01:R1", 0x1100, 0x80, "M1-dev.1", 1),   # memcpy
    ("b20002", "libc-02:R1", 0x1180, 0x80, "M1-dev.1", 1),   # memcmp
    ("b20003", "libc-03:R1", 0x1200, 0x80, "M1-dev.1", 1),   # strlen
    ("b20004", "libc-04:R1", 0x1280, 0x80, "M1-dev.1", 1),   # itoa
    ("b20005", "libc-05:R1", 0x1300, 0x80, "M1-dev.1", 1),   # zone_alloc
    ("b20006", "libc-06:R1", 0x1380, 0x40, "M1-dev.1", 1),   # zone_reset
    ("b20007", "libc-07:R1", 0x13C0, 0x80, "M1-dev.2", 2),   # memset (démonstration R7)
]

BLOC_AUTOTEST = ("b20008", "libc-08:R1", 0x1800, 0x800)     # zone app, point d'entrée

# Bloc M0 non embarqué dans selftest.exe (reste indexé par la carte projet) :
BLOC_M0_NON_EMBARQUE = ("a10001", "hello-01:R1")             # hello.exe @ 0x1000

ENTREE = BLOC_AUTOTEST[2]    # AddressOfEntryPoint = 0x1800

NOMS_BLOCS = {
    "a10001": "hello-main", "a10002": "write", "a10003": "exit",
    "b20001": "memcpy", "b20002": "memcmp", "b20003": "strlen",
    "b20004": "itoa", "b20005": "zone_alloc", "b20006": "zone_reset",
    "b20007": "memset", "b20008": "autotest",
}

# --- .rdata : structures PE héritées M0 (positions immuables) ------------------

R_MSG_LIBRE = 0x2000         # 0x2000-0x202F : libre (48 o, héritage zone message)
R_DESC_IMPORT = 0x2030       # descripteur kernel32 + terminateur (40 o)
R_NOM_DLL = 0x2058           # "kernel32.dll\0"
R_HN_GSH, R_HN_WF, R_HN_EP = 0x2066, 0x2076, 0x2082
R_INT = 0x2090               # OriginalFirstThunk (4 qwords)
R_IAT = 0x20B0               # FirstThunk / IAT : [0] GSH [1] WF [2] EP  — SCELLÉ
R_RELOC = 0x20D0             # bloc de relocalisation minimal (12 o)

IAT_SLOTS = {
    "GetStdHandle": R_IAT + 0 * 8,
    "WriteFile": R_IAT + 1 * 8,
    "ExitProcess": R_IAT + 2 * 8,
}
DLL_IMPORTS = ["GetStdHandle", "WriteFile", "ExitProcess"]

# --- .rdata : vecteurs dorés et messages du selftest --------------------------

R_SA = 0x2000      # "TRIADE\0"          memcmp A
R_SB = 0x2008      # "TRIADE\0"          memcmp B (exemplaire distinct, égal)
R_SC = 0x2010      # "TRIADF\0"          memcmp C (supérieur)
R_SD = 0x2018      # "TRI\0"             memcmp D (préfixe)

R_MOTIF16 = 0x20E0      # 0x00..0x0F          memcpy/memset
R_SENT16 = 0x20F0       # 0xAA × 16          sentinelle dst
R_MOTIF33 = 0x2100      # motif fixe 33 o     memcpy
R_ZERO16 = 0x2130       # 0x00 × 16          memset attendu
R_FF33 = 0x2140         # 0xFF × 33          memset attendu
R_S_VIDE = 0x2168       # "\0"               strlen
R_S_TRIADE = 0x2170     # "TRIADE\0"         strlen
R_S_33 = 0x2178         # 33 lettres + NUL   strlen
R_I0 = 0x21A0           # "0\0"              itoa attendu
R_IMAX = 0x21A8         # "4294967295\0"     itoa attendu
R_I123 = 0x21B8         # "1234567890\0"     itoa attendu
R_I7 = 0x21C8           # "7\0"              itoa attendu
R_PREFIXE = 0x21D0      # "TRIADE M1 : minilibc " (21 o)
R_SLASH = 0x21F0        # "/"
R_OK = 0x21F8           # " OK\r\n"
R_KO = 0x2200           # " KO\r\n"

MOTIF33 = bytes((i * 37 + 11) & 0xFF for i in range(33))
S_33 = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg"
PREFIXE = b"TRIADE M1 : minilibc "

NB_TESTS_DEV1 = 18        # zone 4 + memcmp 4 + memcpy 3 + strlen 3 + itoa 4
NB_TESTS_DEV2 = 21        # + memset 3

# --- .data : allocateur par zone ----------------------------------------------

R_CURSEUR = 0x3000        # qword : offset de allocation suivant (init 0)
ARENE_BASE = 0x3040       # alignée 64 (contractuel : align ∈ [1,64] puissance de 2)
ARENE_TAILLE = 0x7C0      # 1 984 o ; l'arène finit à 0x3800

# --- Jetons de retour d'émulation (oracle, hors binaire) ----------------------

SENTINELLE_RETOUR = 0xDEADBEEFCAFE   # adresse factice de retour (unicorn)
