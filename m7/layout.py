"""layout.py — Plan d'adressage de la lignée sceau (m7, D34 échelon 2).

Source unique de vérité partagée par build_sceau.py, outils/auteur.py et la
carte. Toute adresse de l'artefact `sceau` dérive d'ici ; la notation
référence ces constantes et le builder vérifie la concordance.

ÉCHELON 2 DE D34 : VÉRIFICATION NATIVE — le hachage (hachoir, échelon 1) et
désormais la SIGNATURE (Ed25519, RFC 8032) vérifiés par des blocs TRIADE.
`sceau` vérifie les signatures des cartes du projet en code machine nu :
SHA-512 + arithmétique f25519 + edwards25519 projective, écrits à la main.
Mode diagnostic : `sceau --hacher <fichier>` (ligne sha512sum — l'agent gagne
un hacheur SHA-512 natif, complément du hachoir SHA-256).

HÉRITAGE OCTET-IDENTIQUE m6 (même profil x86-64-linux-elf64, réutilisation
aux MÊMES adresses — les déplacements RIP et sauts internes des notations
ah-01/03/08 l'exigent) :
  - d40001 ah-01-ecrire @ 0x1000 (slot 0x40) ;
  - d40003 ah-03-sortir @ 0x1080 (slot 0x40) ;
  - d40008 ah-08-hex    @ 0x1600 (slot 0x80) — son lea [rip] vise
    R_HEXCHARS @ 0x2100 : l'image sceau DOIT poser "0123456789abcdef"
    à CETTE adresse (garde-fou du builder).
  ah-02-lire (d40002) n'est PAS embarqué : le principal lit par read direct
  (I1 de sa spec, miroir de ah-09) — héritage non embarqué, empreintes
  re-vérifiées par le verrou croisé.

Domaine NOUVEAU `av` (authentification-vérifiée) : 17 blocs.
  av-01..04 : SHA-512 (init, comprimer, absorber, finaliser) ;
  av-05..11 : corps f25519, radix 2^51, 5 membres u64 (charger, propager,
              add, sub, mul, freeze, exp) ;
  av-12..15 : edwards25519 projective (add unifiée — le neutre est (0:1:1),
              courbe complète, Z nul impossible ; mul scalaire double-and-add
              512 bits ; decompresser ; egal projective) ;
  av-16..17 : vérification RFC 8032 (v-verifier sans E/S) et principal (CLI).

ELF64 ET_EXEC minimal, écrit à la main (miroir hachoir) :
  - segment 1 PT_LOAD R+X : offset 0 → vaddr 0x400000, filesz = memsz
    = 0x4000 — en-têtes, réserve int3, code, rodata ; RVA == offset ;
  - segment 2 PT_LOAD RW : offset 0x4000 (filesz 0) → vaddr 0x404000,
    memsz 0x12000 — .bss pur ;
  - aucune table de sections ; entrée @ 0x2920 (av-17).

DISCIPLINE D28/D33 : slots multiples de 64, alignés 16, padding
inter-blocs >= 16, réserve int3 pour la croissance (dev.2+ : f25519,
courbe, vérification).

Contexte SHA-512 (av-01..04, 256 o) : H[8] u64 @ +0, tampon[128] @ +64,
remplissage u32 @ +192, total u64 @ +200.

Représentation f25519 « limbs » : 5 u64 little-endian @ +0..+39, radix 2^51,
membres < 2^52 ; valeur ≡ x mod p. Points projectifs : X, Y, Z (3×40 o
consécutifs). Scalars : octets little-endian (S : 32 o zéro-étendus à 64 ;
h : 64 o).
"""

# --- Image et segments --------------------------------------------------------

IMAGE_BASE = 0x400000
RX_RVA = 0x0                    # segment R+X : RVA == offset fichier
RX_TAILLE = 0x4000              # en-têtes + code + rodata
RW_RVA = 0x4000                 # segment RW : .bss pur (filesz 0)
RW_VADDR = IMAGE_BASE + RW_RVA  # 0x404000
RW_TAILLE = 0x12000             # contextes + zones courbe + tampon 64 Kio
TAILLE_FICHIER = RX_TAILLE

TAILLE_PAGE = 0x1000

# --- Zones de code (RVA, dans le segment R+X) ---------------------------------

SYS_RVA = 0x1000                # héritage ah-01/03 (d40001, d40003)
SHA_RVA = 0x1100                # av-01..04 : famille SHA-512
HEX_RVA = 0x1600                # héritage ah-08 (d40008)
ABS_RVA = 0x1680                # av-03/04 : absorber, finaliser
CORPS_RVA = 0x1880              # av-05..11 : f25519
COURBE_RVA = 0x2120             # av-12..15 : edwards25519 projective
APP_RVA = 0x2720                # av-16/17 : vérification, principal
RODATA_RVA = 0x3000             # données pures

# Blocs embarqués : (id carte, spec, fichier notation, rva, slot)
# Héritages m6 octet-identiques (d40001/03/08 — specs ah-* inchangées) ;
# av-* : domaine nouveau, id d50001+.
BLOCS_SCEAU = [
    ("d40001", "ah-01:R1", "ah-01-ecrire", 0x1000, 0x40),
    ("d40003", "ah-03:R1", "ah-03-sortir", 0x1080, 0x40),
    ("d50001", "av-01:R1", "av-01-s512-init", 0x1100, 0x100),
    ("d50002", "av-02:R2", "av-02-s512-comprimer", 0x1200, 0x400),
    ("d40008", "ah-08:R1", "ah-08-hex", 0x1600, 0x80),
    ("d50003", "av-03:R1", "av-03-s512-absorber", 0x1680, 0x100),
    ("d50004", "av-04:R1", "av-04-s512-finaliser", 0x1780, 0x100),
    ("d50005", "av-05:R1", "av-05-f-charger", 0x1880, 0x100),
    ("d50006", "av-06:R1", "av-06-f-propager", 0x1980, 0x80),
    ("d50007", "av-07:R1", "av-07-f-add", 0x1a00, 0x80),
    ("d50008", "av-08:R1", "av-08-f-sub", 0x1a80, 0x80),
    ("d50009", "av-09:R1", "av-09-f-mul", 0x1b00, 0x400),
    ("d50010", "av-10:R1", "av-10-f-freeze", 0x1f00, 0x80),
    ("d50011", "av-11:R1", "av-11-f-exp", 0x1f80, 0x180),
    ("d50012", "av-12:R1", "av-12-p-add", 0x2120, 0x200),
    ("d50013", "av-13:R1", "av-13-p-mul", 0x2320, 0x100),
    ("d50014", "av-14:R1", "av-14-p-decompresser", 0x2420, 0x200),
    ("d50015", "av-15:R1", "av-15-p-egal", 0x2620, 0x100),
    ("d50016", "av-16:R1", "av-16-v-verifier", 0x2720, 0x200),
    ("d50017", "av-17:R1", "av-17-principal", 0x2920, 0x280),
]

# Phase de notation (dev.1 : SHA-512 + principal mode hacher ; les specs
# av-05..16 sont POSÉES (couche I complète, R2 écrite-avant-code) mais leur
# notation est en chantier — dev.2 et suivants).
NOTES_DEV1 = {"d40001", "d40003", "d40008",
              "d50001", "d50002", "d50003", "d50004", "d50017"}

ENTREE = 0x2920                 # e_entry = av-17-principal

NOMS_BLOCS = {
    "d40001": "ah-ecrire", "d40003": "ah-sortir", "d40008": "ah-hex",
    "d50001": "av-s512-init", "d50002": "av-s512-comprimer",
    "d50003": "av-s512-absorber", "d50004": "av-s512-finaliser",
    "d50005": "av-f-charger", "d50006": "av-f-propager", "d50007": "av-f-add",
    "d50008": "av-f-sub", "d50009": "av-f-mul", "d50010": "av-f-freeze",
    "d50011": "av-f-exp", "d50012": "av-p-add", "d50013": "av-p-mul",
    "d50014": "av-p-decompresser", "d50015": "av-p-egal",
    "d50016": "av-v-verifier", "d50017": "av-principal",
}

# Adresses de blocs (appels directs — I1 des specs)
A_ECRITE = 0x1000               # ah-01 (héritage)
A_SORTIR = 0x1080               # ah-03 (héritage)
A_INIT = 0x1100                 # av-01
A_COMPRIMER = 0x1200            # av-02
A_HEX = 0x1600                  # ah-08 (héritage)
A_ABSORBER = 0x1680             # av-03
A_FINALISER = 0x1780            # av-04
A_F_CHARGER = 0x1880            # av-05
A_F_PROPAGER = 0x1980           # av-06
A_F_ADD = 0x1a00                # av-07
A_F_SUB = 0x1a80                # av-08
A_F_MUL = 0x1b00                # av-09
A_FREEZE = 0x1f00               # av-10
A_F_EXP = 0x1f80                # av-11
A_P_ADD = 0x2120                # av-12
A_P_MUL = 0x2320                # av-13
A_P_DECOMPRIMER = 0x2420        # av-14
A_P_EGAL = 0x2620               # av-15
A_VERIFIER = 0x2720             # av-16
A_PRINCIPAL = 0x2920            # av-17

# --- .rodata : données pures (RVA) ---------------------------------------------

R_HEXCHARS = 0x2100             # "0123456789abcdef" (16 o) — CIBLE du lea
                                # RIP de l'héritage ah-08 : INTANGIBLE
R_K512 = 0x3000                 # K[80] u64 — FIPS 180-4 § 4.2.3 (640 o)
R_D = 0x3280                    # d = -121665/121666 mod p, 5 limbs (40 o)
R_BX = 0x32c0                   # Bx en limbs (40 o)
R_BY = 0x3300                   # By en limbs (40 o)
R_SQRTM1 = 0x3340               # sqrt(-1) = 2^((p-1)/4), limbs (40 o)
R_EXP_INV = 0x3380              # p - 2, 32 o LE (exposant inversion)
R_EXP_SQRT = 0x33a0             # (p - 5) / 8, 32 o LE (exposant racine)
R_L = 0x33c0                    # L (ordre du groupe), 32 o LE
R_MSG_USAGE = 0x3400            # usage (2 modes)
R_MSG_OUVERTURE = 0x3460        # ouverture impossible
R_MSG_LECTURE = 0x3480          # erreur de lecture
R_MSG_ECRITURE = 0x34a0         # erreur d'ecriture
R_MSG_OK = 0x34c0               # verdict signature OK
R_MSG_KO = 0x34e0               # verdict signature KO
R_MSG_CHANTIER = 0x3500         # vérification en chantier (dev.1)

# Constantes FIPS 180-4 § 4.2.3 (80 u64, racines cubiques des 80 premiers
# premiers — le builder écrit la table à R_K512, la spec av-02 la référence).
K512 = [
    0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f,
    0xe9b5dba58189dbbc, 0x3956c25bf348b538, 0x59f111f1b605d019,
    0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242,
    0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
    0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235,
    0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3,
    0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65, 0x2de92c6f592b0275,
    0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
    0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f,
    0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725,
    0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc,
    0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
    0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6,
    0x92722c851482353b, 0xa2bfe8a14cf10364, 0xa81a664bbc423001,
    0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218,
    0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
    0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99,
    0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb,
    0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc,
    0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
    0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915,
    0xc67178f2e372532b, 0xca273eceea26619c, 0xd186b8c721c0c207,
    0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba,
    0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
    0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc,
    0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a,
    0x5fcb6fab3ad6faec, 0x6c44198c4a475817,
]

# --- Constantes f25519 / edwards25519 (calculées, vérifiées par le builder) ----

P25519 = 2**255 - 19
L25519 = 2**252 + 27742317777372353535851937790883648493
D25519 = (-121665 * pow(121666, P25519 - 2, P25519)) % P25519
BX25519 = 15112221349535400772501151409588531511454012693041857206046113283949847762202
BY25519 = 46316835694926478169428394003475163141307993866256225615783033603165251855960
SQRTM1 = pow(2, (P25519 - 1) // 4, P25519)

M51 = (1 << 51) - 1


def limbs(x: int) -> list[int]:
    """Décomposition radix 2^51 (5 u64) — utilisée par le builder pour
    écrire les fixtures et vérifier les constantes de la notation."""
    return [(x >> (51 * i)) & M51 for i in range(5)]


P_LIMBS = limbs(P25519)             # [0x7ffffffffffedc, 0x7ffffffffffff, ...]
DEUX_P_LIMBS = [(v * 2) for v in P_LIMBS]

HEXCHARS = b"0123456789abcdef"
MSG_USAGE = b"usage: sceau (--hacher <fichier> | <message> <signature> <cle-hex>)\n"
MSG_OUVERTURE = b"sceau: ouverture impossible\n"
MSG_LECTURE = b"sceau: erreur de lecture\n"
MSG_ECRITURE = b"sceau: erreur d'ecriture\n"
MSG_OK = b"TRIADE sceau : signature OK\n"
MSG_KO = b"TRIADE sceau : signature KO\n"
MSG_CHANTIER = b"TRIADE sceau : verification en chantier (0.8.0-dev.1)\n"

# --- .bss : état de l'artefact (RVA, segment RW) -------------------------------

R_CTX = 0x4000                  # contexte SHA-512 (256 o)
CTX_TAILLE = 256
R_DIGEST = 0x4100               # digest SHA-512 (64 o) — h de RFC 8032
R_CLE = 0x4140                  # clé publique A (32 o)
R_SIG = 0x4160                  # signature R'||S' (64 o)
R_SCALAIRE = 0x41a0             # S zéro-étendu (64 o)
R_LIGNE = 0x4200                # ligne de sortie (0x1200 o)
LIGNE_TAILLE = 0x1200
R_TRAVAIL = 0x5400              # zones de travail f25519 / points (0x800)
TRAVAIL_TAILLE = 0x800
R_TAMPON = 0x5c00               # tampon de lecture (64 Kio)
TAMPON_TAILLE = 0x10000

# Décalages dans le contexte SHA-512 (contrats av-01..04)
CTX_H = 0                       # H[8] u64
CTX_TAMPON = 64                 # tampon[128]
CTX_REMPLISSAGE = 192           # u32 — octets valides du tampon
CTX_TOTAL = 200                 # u64 — octets absorbés cumulés

# Zones de travail courbe (offsets depuis R_TRAVAIL — contrats av-12..16)
TRAV_P1 = 0x000                 # p-add : P1 (X,Y,Z = 120 o)
TRAV_P2 = 0x078                 # p-add : P2 (120 o)
TRAV_P3 = 0x0f0                 # p-add : P3 (120 o)
TRAV_A = 0x168                  # p-add : A,B,C,D,E,F,G,t* (14×40 = 560 o)
TRAV_Q = 0x400                  # p-mul : Q (120 o)
TRAV_T = 0x478                  # p-mul : T (120 o)
TRAV_PT_B = 0x4f0               # v-verifier : point B (120 o)
TRAV_Q1 = 0x568                 # v-verifier : Q1 = [S]B (120 o)
TRAV_Q2 = 0x5e0                 # v-verifier : Q2 = [h]A (120 o)
TRAV_Q3 = 0x658                 # v-verifier : Q3 = R' + [h]A (120 o)
TRAV_PA = 0x6d0                 # v-verifier : point A décompressé (120 o)
TRAV_PR = 0x748                 # v-verifier : point R' décompressé (120 o)

# --- Versions (R10 : monotonie, lignée auto-hôte) -------------------------------

VERSION_DEV1 = "0.8.0-dev.1"    # sceau, échelon 2 de l'échelle (D34)
VERSION_U64_DEV1 = 0x00080001
VERSION_U64_MIN = 0x00080000

PROFIL = "x86-64-linux-elf64"
