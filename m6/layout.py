"""layout.py — Plan d'adressage de la lignée auto-hôte (D34, profil x86-64-linux-elf64).

Source unique de vérité partagée par build_ah.py, outils/auteur.py et la
carte. Toute adresse de l'artefact `hachoir` dérive d'ici ; la notation
référence ces constantes et le builder vérifie la concordance.

PREMIER ARTEFACT DU PROFIL LINUX (D34 — anticipation restreinte sur M6,
les critères de sortie M6 complets restent soumis à M2-M5). Aucun héritage
d'adresse : la lignée win11-pe (io/libc/tcp @ 0x1040+) reste la propriété
du profil x86-64-win11-pe — les deux profils ne partagent QUE la couche I
et la méthode, par conception (M6 : diff nul sur I, adresses propres).

ELF64 ET_EXEC minimal, écrit à la main :
  - segment 1 PT_LOAD R+X : offset 0 → vaddr 0x400000, filesz = memsz
    = 0x3000 — en-têtes (ehdr 64 o + 2 phdr 56 o), réserve int3, code,
    rodata ; RVA == offset fichier (identité, pas de translation) ;
  - segment 2 PT_LOAD RW : offset 0x3000 (filesz 0) → vaddr 0x403000,
    memsz 0x11300 — .bss pur (zéro au chargement par le noyau) ;
  - aucune table de sections (le noyau ne lit que les phdr — e_shnum 0) ;
  - entrée @ 0x1680 (ah-09, point d'entrée ELF).

DISCIPLINE D28/D33 : slots multiples de 64, alignés 16, padding
inter-blocs >= 16, réserve int3 (0xCC) pour la croissance.

Contexte SHA-256 (ah-04..07, 112 o) : H[8] u32 @ +0, tampon[64] @ +32,
remplissage u32 @ +96, réservé @ +100, total u64 @ +104.
"""

# --- Image et segments --------------------------------------------------------

IMAGE_BASE = 0x400000
RX_RVA = 0x0                    # segment R+X : RVA == offset fichier
RX_TAILLE = 0x3000              # en-têtes + code + rodata
RW_RVA = 0x3000                 # segment RW : .bss pur (filesz 0)
RW_VADDR = IMAGE_BASE + RW_RVA  # 0x403000
RW_TAILLE = 0x11300             # contexte + digest + ligne + tampon 64 Kio
TAILLE_FICHIER = RX_TAILLE      # le segment RW n'occupe aucun octet fichier

TAILLE_PAGE = 0x1000

# --- Zones de code (RVA, dans le segment R+X) ---------------------------------

SYS_RVA = 0x1000                # ah-01..03 : interface noyau
SHA_RVA = 0x1100                # ah-04..07 : famille SHA-256
HEX_RVA = 0x1600                # ah-08
APP_RVA = 0x1680                # ah-09 : point d'entrée
RODATA_RVA = 0x2000             # données pures

# Blocs : (id carte, spec, fichier notation, rva, slot)
BLOCS_AH = [
    ("d40001", "ah-01:R1", "ah-01-ecrire", 0x1000, 0x40),
    ("d40002", "ah-02:R1", "ah-02-lire", 0x1040, 0x40),
    ("d40003", "ah-03:R1", "ah-03-sortir", 0x1080, 0x40),
    ("d40004", "ah-04:R1", "ah-04-initialiser", 0x1100, 0x100),
    ("d40005", "ah-05:R1", "ah-05-comprimer", 0x1200, 0x200),
    ("d40006", "ah-06:R1", "ah-06-absorber", 0x1400, 0x100),
    ("d40007", "ah-07:R1", "ah-07-finaliser", 0x1500, 0x100),
    ("d40008", "ah-08:R1", "ah-08-hex", 0x1600, 0x80),
    ("d40009", "ah-09:R1", "ah-09-principal", 0x1680, 0x200),
]

ENTREE = APP_RVA                # e_entry = 0x401680

NOMS_BLOCS = {
    "d40001": "ah-ecrire", "d40002": "ah-lire", "d40003": "ah-sortir",
    "d40004": "ah-initialiser", "d40005": "ah-comprimer",
    "d40006": "ah-absorber", "d40007": "ah-finaliser", "d40008": "ah-hex",
    "d40009": "ah-principal",
}

# Adresses de blocs (appels directs — I1 des specs)
A_ECRITE = 0x1000
A_LIRE = 0x1040
A_SORTIR = 0x1080
A_INIT = 0x1100
A_COMPRIMER = 0x1200
A_ABSORBER = 0x1400
A_FINALISER = 0x1500
A_HEX = 0x1600
A_PRINCIPAL = 0x1680

# --- .rodata : données pures (RVA) ---------------------------------------------

R_K = 0x2000                    # K[64] u32 — constantes FIPS 180-4 § 4.2.2
R_HEXCHARS = 0x2100             # "0123456789abcdef" (16 o)
R_MSG_USAGE = 0x2120            # "usage: hachoir <fichier>\n"
R_MSG_OUVERTURE = 0x2140        # "hachoir: ouverture impossible\n"
R_MSG_LECTURE = 0x2160          # "hachoir: erreur de lecture\n"
R_MSG_ECRITURE = 0x2180         # "hachoir: erreur d'ecriture\n"

# Constantes FIPS 180-4 § 4.2.2 (dérivées des racines cubiques des 64
# premiers nombres premiers — le builder écrit la table à R_K, la spec
# ah-05 la référence ; l'oracle vérifie l'empreinte de la table).
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
    0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
    0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
    0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
    0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]
HEXCHARS = b"0123456789abcdef"
MSG_USAGE = b"usage: hachoir <fichier>\n"
MSG_OUVERTURE = b"hachoir: ouverture impossible\n"
MSG_LECTURE = b"hachoir: erreur de lecture\n"
MSG_ECRITURE = b"hachoir: erreur d'ecriture\n"

# --- .bss : état de l'artefact (RVA, segment RW) -------------------------------

R_CTX = 0x3000                  # contexte SHA-256 (112 o)
CTX_TAILLE = 112
R_DIGEST = 0x3080               # digest binaire (32 o)
R_LIGNE = 0x30C0                # ligne de sortie (0x1200 o)
LIGNE_TAILLE = 0x1200
R_TAMPON = 0x4300               # tampon de lecture (64 Kio)
TAMPON_TAILLE = 0x10000

# Décalages dans le contexte (contrats ah-04..07)
CTX_H = 0                       # H[8] u32
CTX_TAMPON = 32                 # tampon[64]
CTX_REMPLISSAGE = 96            # u32 — octets valides du tampon
CTX_RESERVE = 100               # u32 — alignement
CTX_TOTAL = 104                 # u64 — octets absorbés cumulés

# --- Versions (R10 : monotonie, par lignée auto-hôte) ---------------------------

VERSION_DEV1 = "0.7.0-dev.1"    # hachoir, échelon 1 de l'échelle (D34)
VERSION_U64_DEV1 = 0x00070001
VERSION_U64_MIN = 0x00070000

PROFIL = "x86-64-linux-elf64"
