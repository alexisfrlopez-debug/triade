"""layout.py — Plan d'adressage de la lignée du jalon M6 (unix/, D149).

Le jalon M6 vit dans unix/ (convention de dossiers D149-(5)) ; m6/ demeure
l'échelle d'auto-hébergement D34 (emprunt de nommage consigné — le programme
ne le défait pas). Source unique de vérité partagée par build_m6.py,
outils/auteur.py et la carte du jalon ; la notation référence ces constantes
et le builder vérifie la concordance. Série d'identifiants propre à la lignée
(f6xxxx — les séries sont nommées PAR CARTE : la démo et le hachoir partagent
d4, le jalon prend f6, aucune adresse n'est héritée de la lignée auto-hôte).

L'ELF64 DURCI du jalon (fiche de profil § 3, chantier M6-(a) — le
durcissement) : ET_DYN (PIE — l'image se charge à une base aléatoire, ASLR
noyau), e_entry RELATIF à la base (RVA 0x1140), adresses de liaison = RVA
(vaddr 0x0) — le code est indifférent à la base : tous les accès données
vivent en [rip + disp] ou [base + RVA], jamais en lien-temps absolu ;
TROIS segments PT_LOAD R/RX/RW (aucun inscriptible exécutable — W^X vérifié
depuis les phdr par le build) ; PT_GNU_STACK (0x6474E551) à drapeaux RW
SANS X (NX explicite) ; offsets == vaddr par segment, p_align 0x1000 :
  - segment 1 PT_LOAD R  : vaddr 0x0, filesz = memsz = 0x1000 — en-têtes
    (ehdr 64 o + 4 phdr 224 o), table ERRNOS, HEXCHARS, messages ;
  - segment 2 PT_LOAD RX : vaddr 0x1000, filesz = memsz = 0x1000 — les
    quatre blocs, réserves int3 ;
  - segment 3 PT_LOAD RW : vaddr 0x2000, filesz 0, memsz 0x1000 — .bss
    pur (tampon), zéro octet fichier ;
  - PT_GNU_STACK : drapeaux 6 (RW), align 0x10.

Table ERRNOS (fiche § 4 — le contrat d'erreurs des syscalls, miroir de la
table HRESULTS du primaire) : à R_ERRNOS, [nombre u32] puis des entrées
{errno u32, verdict u32}. Échelle des verdicts : 0 = succès (RAX dans
[0, 4095], constaté PAR PLAGE par l'appelant — jamais par table) ;
1 = échec nommé (l'errno est attendu et déclaré : le bloc suit son contrat
d'échec, jamais un crash) ; 6 = VERDICT_FATAL (errno inattendu : arrêt
propre nommé, fail-closed). TOUTE entrée est motivée par le contrat d'un
bloc (comme les numéros de syscall en I1) : au chantier (a), la sonde
su-04 déclare EBADF (9) — la table grandira par révision quand le corpus
du chantier (b) déclare d'autres errno attendus.

Discipline D28/D33 : slots multiples de 64, alignés 16, padding
inter-blocs >= 16, réserves int3 (0xCC) pour la croissance.
"""

# --- Image et segments (ELF64 durci, ET_DYN/PIE) --------------------------------

PROFIL = "x86-64-linux-elf64"

SEG_R_RVA = 0x0                   # segment R : en-têtes + tables + messages
SEG_R_TAILLE = 0x1000
SEG_RX_RVA = 0x1000               # segment RX : les quatre blocs
SEG_RX_TAILLE = 0x1000
SEG_RW_RVA = 0x2000               # segment RW : .bss pur (filesz 0)
SEG_RW_TAILLE = 0x1000            # memsz — le tampon
TAILLE_FICHIER = 0x2000           # le segment RW n'occupe aucun octet fichier

TAILLE_PAGE = 0x1000
PT_GNU_STACK = 0x6474E551         # NX : drapeaux RW (6), jamais X

# --- Blocs : (id carte, spec, fichier notation, rva, slot) ----------------------

BLOCS_SU = [
    ("f60001", "su-01:R1", "su-01-ecrire",    0x1000, 0x40),
    ("f60002", "su-02:R1", "su-02-hex64",     0x1040, 0x80),
    ("f60003", "su-03:R1", "su-03-verdict",   0x10C0, 0x80),
    ("f60004", "su-04:R1", "su-04-principal", 0x1140, 0x280),
]

ENTREE = 0x1140                   # e_entry = RVA (ET_DYN : relatif à la base)

NOMS_BLOCS = {
    "f60001": "su-ecrire", "f60002": "su-hex64",
    "f60003": "su-verdict", "f60004": "su-principal",
}

# Adresses de blocs (appels directs — I2 des specs)
A_ECRIRE = 0x1000
A_HEX64 = 0x1040
A_VERDICT = 0x10C0
A_PRINCIPAL = 0x1140

# --- Table ERRNOS (contrat d'erreurs des syscalls — source unique) --------------

ERRNOS = {
    9: 1,       # EBADF : descripteur invalide — échec nommé (déclaré par
                # su-04:E1 : la sonde du descripteur ; su-01 le constate)
}
VERDICT_FATAL = 6                # tout errno hors table : arrêt propre nommé

R_ERRNOS = 0x140                 # [nombre u32] + {errno u32, verdict u32}
R_HEXCHARS = 0x180               # HEXCHARS (16 o) — chiffres hexadécimaux minuscules
HEXCHARS = b"0123456789abcdef"

# --- .rodata : messages de la sonde (longueurs FIGÉES par le plan) ---------------

R_MSG_BASE = 0x1C0               # préfixe de la ligne 1 — ET témoin de base
MSG_BASE = b"sonde : base 0x"            # 15 o
L_MSG_BASE = 15

R_MSG_P1 = 0x1E0
MSG_P1 = b"sonde : write(-1) : rax 0x"   # 26 o — préfixe de la ligne sonde 1
L_MSG_P1 = 26

R_MSG_P2 = 0x200
MSG_P2 = b"sonde : write(0x1) : rax 0x"  # 27 o — préfixe de la ligne sonde 2
L_MSG_P2 = 27

R_MSG_VERD = 0x220
MSG_VERD = b" verdict 0x"                # 11 o — entre hex16(rax) et hex16(verdict)
L_MSG_VERD = 11

R_MSG_FIN = 0x240
MSG_FIN = b"\n"                          # 1 o — terminateur de ligne
L_MSG_FIN = 1

R_MSG_FATAL = 0x260
MSG_FATAL = b"sonde : VERDICT_FATAL (arret propre)\n"  # 37 o
L_MSG_FATAL = 37

# --- .bss : tampon de formatage (segment RW, .bss pur) ---------------------------

# Trois sous-zones (I3/I4 de su-04) : la mémoire traverse les appels et les
# syscalls — les registres volatils non (r8/r9 meurent dans su-02/su-03,
# r11 dans chaque syscall de su-01). Le verdict vit donc au tampon.
R_TAMPON = 0x2000                # +0 : hex16 du rax brut (16 o)
R_TAMPON_VERD = 0x2010           # +16 : hex16 du verdict (16 o)
R_TAMPON_NUM = 0x2020            # +32 : le verdict u32 (la valeur de retour)
TAMPON_TAILLE = 0x40             # +36..64 libres

# --- Versions (R10 : monotonie, lignée du jalon M6) ------------------------------

VERSION_DEV1 = "0.7.0-dev.1"     # premier build du jalon M6 (D149 : la
                                 # 0.7.0-dev.1 vient du premier build M6)
VERSION_U64_DEV1 = 0x00070001
VERSION_U64_MIN = 0x00070000     # plancher (la pointe 0.7.0-dev.1 est déjà
                                 # vivante : hachoir échelon 1 D34 et sonde)
VERSION_RC1 = "0.7.0-rc.1"      # chantier (c) — scellage avec contrôle D146
VERSION_FINALE = "0.7.0"        # chantier (d) — après run terrain vert


# ============================================================================
# LE CORPUS PARITAIRE (chantier M6-(b) — le diff nul sur la couche I)
# ============================================================================
"""Plan d'adressage de l'artefact `corpus` (balise 0.7.0-dev.2) — l'instance
SysV du corpus nominal de D149-(2) : les DOUZE blocs du patrimoine (révisions
de granularité R+1 de unix/I/, ancêtres scellés INTACTS dans m0/m1/m2) et le
principal propre au jalon (corpus-13, modèle ah-09). Le durcissement M6-(a)
est hérité tel quel : ET_DYN/PIE, e_entry RELATIF, TROIS segments R/RX/RW,
offsets == vaddr, PT_GNU_STACK RW sans X. Le code est indifférent à la base :
TOUT accès vit en relatif RIP (la sonde CONSTATAIT sa base — son sujet ;
le corpus n'en a pas besoin — le sien est le patrimoine).

  - segment 1 PT_LOAD R  : vaddr 0x0, 0x1000 — en-têtes (ehdr 64 + 4 phdr
    224), vecteurs dorés (mêmes CONTENUS que m1, aux adresses du corpus),
    chaînes du rituel, STAGING (le journal v2 assemblé POUR la croissance),
    table d'intégrité R10 ;
  - segment 2 PT_LOAD RX : vaddr 0x1000, 0x2000 — les treize blocs (zones
    io/libc/app, D28), la CROISSANCE (0x1D80, la cible du patch y dort en
    int3), réserves int3 ;
  - segment 3 PT_LOAD RW : vaddr 0x3000, filesz 0, memsz 0x1000 — .bss pur :
    curseur d'arène + arène (la MÊME géométrie que m1 : curseur à la base,
    arène alignée 64), le verrou tournant du journal (né déverrouillé —
    tcp-11:R2 P5), l'état du patch et l'entrée sauvée (tcp-07:R4) ;
  - PT_GNU_STACK : drapeaux 6 (RW), align 0x10.

La CIBLE du patch moteur (tcp-07:R4 P5) est l'ENTRÉE DU JOURNAL (tcp-11 @
0x1840) : la démonstration M5-(c) reportée (D149-(4)) basculera la ligne de
journal PENDANT le trafic au chantier (d) — le staging est le journal v2
(marqueur "j2: ") assemblé pour la croissance 0x1D80, embarqué dès dev.2
(le modèle m2 dev.2 : staging présent, la démonstration prête).

Série d'identifiants f61xxxx (f60xxxx demeure à la sonde — les séries sont
nommées PAR CARTE, la carte du corpus est une génération 1 propre).
"""

CORPUS_PROFIL = "x86-64-linux-elf64"

# --- Segments du corpus ------------------------------------------------------------

CORPUS_SEG_R_RVA = 0x0
CORPUS_SEG_R_TAILLE = 0x1000
CORPUS_SEG_RX_RVA = 0x1000
CORPUS_SEG_RX_TAILLE = 0x2000          # treize blocs + croissance + réserves
CORPUS_SEG_RW_RVA = 0x3000
CORPUS_SEG_RW_TAILLE = 0x1000           # memsz — .bss pur (filesz 0)
CORPUS_TAILLE_FICHIER = 0x3000          # le segment RW n'occupe aucun octet fichier

CORPUS_ENTREE = 0x1C40                  # e_entry = RVA (corpus-13)

# --- Blocs du corpus : (id carte, spec, fichier notation, rva, slot) ---------------

BLOCS_CORPUS = [
    ("f61001", "hello-02:R2", "hello-02-ecrire-r2",   0x1000, 0x40),
    ("f61002", "hello-03:R2", "hello-03-sortir-r2",   0x1040, 0x40),
    ("f61003", "libc-01:R2",  "libc-01-memcpy-r2",    0x1080, 0x40),
    ("f61004", "libc-02:R2",  "libc-02-memcmp-r2",    0x10C0, 0x80),
    ("f61005", "libc-03:R2",  "libc-03-strlen-r2",    0x1140, 0x40),
    ("f61006", "libc-04:R3",  "libc-04-itoa-r3",      0x1180, 0x80),
    ("f61007", "libc-05:R2",  "libc-05-zone-alloc-r2", 0x1200, 0x80),
    ("f61008", "libc-06:R2",  "libc-06-zone-reset-r2", 0x1280, 0x40),
    ("f61009", "libc-07:R2",  "libc-07-memset-r2",    0x12C0, 0x80),
    ("f61010", "libc-08:R3",  "libc-08-autotest-r3",  0x1340, 0x500),
    ("f61011", "tcp-11:R2",   "tcp-11-journal-r2",    0x1840, 0x200),
    ("f61012", "tcp-07:R4",   "tcp-07-patch-r4",      0x1A40, 0x200),
    ("f61013", "corpus-13:R1", "corpus-13-principal", 0x1C40, 0x140),
]

# Le staging du remplaçant : le journal v2 (marqueur "j2: ") assemblé POUR
# l'adresse de croissance — PAS un bloc placé : ses octets vivent au staging
# (.rodata, segment R), la table d'intégrité le porte en première entrée.
BLOC_STAGING = ("f61991", "tcp-11:R2-v2", "tcp-11-journal-v2", 0x1D80, 0x280)

CORPUS_NOMS = {
    "f61001": "ecrire", "f61002": "sortir",
    "f61003": "memcpy", "f61004": "memcmp", "f61005": "strlen",
    "f61006": "itoa", "f61007": "zone_alloc", "f61008": "zone_reset",
    "f61009": "memset", "f61010": "autotest", "f61011": "journal",
    "f61012": "patch", "f61013": "principal",
}

# Adresses d'appel direct (I1 des specs — le builder vérifie la concordance)
A_ECRIRE_CORPUS = 0x1000
A_SORTIR = 0x1040
A_MEMCPY = 0x1080
A_MEMCMP = 0x10C0
A_STRLEN = 0x1140
A_ITOA = 0x1180
A_ZONE_ALLOC = 0x1200
A_ZONE_RESET = 0x1280
A_MEMSET = 0x12C0
A_AUTOTEST = 0x1340
A_JOURNAL = 0x1840            # la CIBLE du patch (tcp-07:R4 P5)
A_PATCH = 0x1A40
A_PRINCIPAL_CORPUS = 0x1C40
A_CROISSANCE = 0x1D80         # zone de croissance (le remplaçant y sera copié)
CROISSANCE_TAILLE = 0x280

# --- Segment R : vecteurs dorés (les MÊMES contenus que m1, plan du corpus) ---------

R_SA = 0x140                   # "TRIADE\0"  memcmp A
R_SB = 0x148                   # "TRIADE\0"  memcmp B (exemplaire distinct, égal)
R_SC = 0x150                   # "TRIADF\0"  memcmp C (supérieur)
R_SD = 0x158                   # "TRI\0"     memcmp D (préfixe)
R_MOTIF16 = 0x160              # 0x00..0x0F          memcpy/memset
R_SENT16 = 0x170               # 0xAA × 16          sentinelle dst
R_MOTIF33 = 0x180              # motif fixe 33 o     memcpy (fin 0x1A1)
R_ZERO16 = 0x1A8               # 0x00 × 16          memset attendu
R_FF33 = 0x1B8                 # 0xFF × 33          memset attendu (fin 0x1D9)
R_S_VIDE = 0x1E0               # "\0"               strlen
R_S_TRIADE = 0x1E8             # "TRIADE\0"         strlen
R_S_33 = 0x1F0                 # 33 lettres + NUL   strlen (fin 0x212)
R_I0 = 0x218                   # "0\0"              itoa attendu
R_IMAX = 0x220                 # "4294967295\0"     itoa attendu
R_I123 = 0x230                 # "1234567890\0"     itoa attendu
R_I7 = 0x240                   # "7\0"              itoa attendu
R_SLASH = 0x248                 # "/" — le séparateur N/21 de la ligne du patrimoine
R_PREFIXE_M1 = 0x250           # "TRIADE M1 : minilibc " (21 o — la ligne du patrimoine)
R_OK = 0x268                   # " OK\n"  (terminateur du profil Linux)
R_KO = 0x270                   # " KO\n"

CORPUS_PREFIXE_M1 = b"TRIADE M1 : minilibc "
CORPUS_MOTIF33 = bytes((i * 37 + 11) & 0xFF for i in range(33))
CORPUS_S_33 = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg"

# --- Segment R : chaînes du rituel (corpus-13) + marqueur v2 ------------------------

R_J_PREF = 0x280               # "corpus : autotest " (18 o — préfixe de la ligne de journal)
R_J_SUFF = 0x2A0               # " vecteurs\n" (10 o — suffixe)
R_J2_MARK = 0x2B0              # "j2: " (4 o — la marque du journal v2, le remplaçant)

CORPUS_J_PREF = b"corpus : autotest "
CORPUS_J_SUFF = b" vecteurs\n"
CORPUS_J2_MARK = b"j2: "

# --- Segment R : staging du remplaçant + table d'intégrité R10 ----------------------

R_STAGING_CORPUS = 0x300       # le journal v2 assemblé POUR 0x1D80 (taille au build)
STAGING_TAILLE_MAX = 0x280
R_TAB_SUM_CORPUS = 0x540       # porte R10 : (rva u32, taille u32, somme u64)* + terme
                               # première entrée = le staging (taille 0 = absent)

# --- Segment RW : .bss du corpus -----------------------------------------------------

R_CURSEUR_CORPUS = 0x3000      # qword : curseur d'arène (init 0 au chargement)
ARENE_BASE_CORPUS = 0x3040     # alignée 64 (contractuel : align ∈ [1,64] puissance de 2)
ARENE_TAILLE_CORPUS = 0x7C0    # 1 984 o — la MÊME géométrie que m1, l'arène finit à 0x3800
R_VERROU = 0x3800              # qword : verrou tournant du journal (né 0 = déverrouillé)
R_ETAT_PATCH_CORPUS = 0x3808   # qword : 0 = v1, 1 = v2 (tcp-07:R4 P4)
R_ENTREE_SAUVEE = 0x3810       # qword : les 8 octets originaux de l'entrée journal

# --- Syscalls du corpus (I1 par bloc — la table du jalon, fiche § 4) -----------------

SYS_WRITE = 1
SYS_MPROTECT = 10
SYS_EXIT_GROUP = 231
PROT_RX = 0x5                  # PROT_READ | PROT_EXEC
PROT_RWX = 0x7                 # PROT_READ | PROT_WRITE | PROT_EXEC (D39 : le bit
                               # exécution RETENU — jamais 0x3 pendant l'écriture de code)

# --- Versions du corpus (R10 : monotonie de la lignée) -------------------------------

VERSION_DEV2 = "0.7.0-dev.2"   # le corpus paritaire (chantier M6-(b))
VERSION_U64_DEV2 = 0x00070002
