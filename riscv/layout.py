"""layout.py — Plan d'adressage de la lignée du jalon M7 (riscv/, D149).

Le jalon M7 vit dans riscv/ (convention de dossiers D149-(5)) ; m7/ demeure
l'échelle d'auto-hébergement D34 (emprunt de nommage consigné — le programme
ne le défait pas). Source unique de vérité partagée par build_m7.py,
outils/auteur.py et la carte du jalon ; la notation référence ces constantes
et le builder vérifie la concordance. Série d'identifiants propre à la
lignée (f7xxxx — les séries sont nommées PAR CARTE : unix/ porte f6xxxx,
aucune adresse n'est héritée, même si le plan MIRE le plan unix : les DEUX
lignées partagent la MÊME géométrie de démonstration — seul le demi-octet
ISA de l'image change, fiche § 3).

L'ELF64 DURCI du jalon (fiche de profil § 3) : ET_DYN (PIE), e_entry RELATIF
à la base (RVA 0x1140), adresses de liaison = RVA (vaddr 0x0) — le code est
indifférent à la base : tout accès données vit en [ancre + déplacement] où
l'ancre est POSÉE par une paire auipc+addi (le portage RV64 du lea rip
lié-temps soustrait — l'instruction auipc lit pc, la paire soustrait le
lien-temps) ; TROIS segments PT_LOAD R/RX/RW (W^X vérifié depuis les phdr
par le build) ; PT_GNU_STACK (0x6474E551) à drapeaux RW SANS X (exigé NX
par le psABI RISC-V) ; offsets == vaddr par segment, p_align 0x1000 :
  - segment 1 PT_LOAD R  : vaddr 0x0, filesz = memsz = 0x1000 — en-têtes
    (ehdr 64 o + 4 phdr 224 o), table ERRNOS, HEXCHARS, messages ;
  - segment 2 PT_LOAD RX : vaddr 0x1000, filesz = memsz = 0x1000 — les
    quatre blocs, réserves ebreak ;
  - segment 3 PT_LOAD RW : vaddr 0x2000, filesz 0, memsz 0x1000 — .bss
    pur (tampon), zéro octet fichier ;
  - PT_GNU_STACK : drapeaux 6 (RW), align 0x10.

MOITIÉ ISA (fiche § 1/§ 3) : e_machine = 0xF3 (EM_RISCV), e_flags = 0 (ni
RVC ni float-abi), instructions TOUTES à 4 octets alignés 4 (SANS extension
C — un encodage 2 o est un refus de build, garde anti-C au oracle) ;
padding intra-slot : NOP canonique addi x0, x0, 0 (0x00000013) ; réserves
d'inaccessibilité : ebreak (0x00100073) — l'équivalent exact du rôle
int3/ud2 des profils x86-64 (garde défensive, fail-closed).

Table ERRNOS (fiche § 4 — le contrat d'erreurs des syscalls, miroir de la
table HRESULTS du primaire, MÊME contrat que M6) : à R_ERRNOS, [nombre u32]
puis des entrées {errno u32, verdict u32}. Échelle des verdicts : 0 = succès
(a0 dans [0, 4095], constaté PAR PLAGE par l'appelant — jamais par table) ;
1 = échec nommé ; 6 = VERDICT_FATAL. TOUTE entrée est motivée par le
contrat d'un bloc : sr-04 déclare EBADF (9) — la table grandira par
révision quand le corpus du chantier (b) déclare d'autres errno attendus.

TABLE DE SYSCALLS ASM-GENERIC (fiche § 4 — la garde du jalon : les numéros
NE SONT PAS ceux de x86-64, un bloc qui porterait write=1 est un REFUS
NOMMÉ au build, la parité est SÉMANTIQUE jamais lexicale).

Discipline D28/D33 : slots multiples de 64, alignés 16, padding
inter-blocs >= 16, réserves ebreak pour la croissance.

ANCRES (fiche § 7 — adresses stables R7 par profil) : s1 = base de
chargement (posée par la paire auipc+addi de sr-04 @ ANCRE_BASE, non-volatil
psABI, traversant — le portage de rbx) ; s2 = base + 0x2000 (la fenêtre
.bss, posée par la seconde paire — les charges/émissions RV64 n'atteignent
que ±2047 o, le tampon vit au-delà : l'ancre le porte). t1 = registre de
travail interne du projet (fiche § 2 — le portage de R10/R11) : il porte le
a0 brut à travers sr-02/sr-03.
"""

# --- Image et segments (ELF64 durci, ET_DYN/PIE, moitié ISA RISC-V) ---------------

PROFIL = "riscv64-linux-elf64"
E_MACHINE = 0xF3                   # EM_RISCV (fiche § 3)
E_FLAGS = 0                        # ni RVC ni float-abi (fiche § 1)

SEG_R_RVA = 0x0                   # segment R : en-têtes + tables + messages
SEG_R_TAILLE = 0x1000
SEG_RX_RVA = 0x1000               # segment RX : les quatre blocs
SEG_RX_TAILLE = 0x1000
SEG_RW_RVA = 0x2000               # segment RW : .bss pur (filesz 0)
SEG_RW_TAILLE = 0x1000            # memsz — le tampon
TAILLE_FICHIER = 0x2000           # le segment RW n'occupe aucun octet fichier

TAILLE_PAGE = 0x1000
PT_GNU_STACK = 0x6474E551         # NX : drapeaux RW (6), jamais X

NOP_CANONIQUE = 0x00000013        # addi x0, x0, 0 (fiche § 7)
EBREAK = 0x00100073               # réserve d'inaccessibilité (fiche § 7)

# --- Blocs : (id carte, spec, fichier notation, rva, slot) ------------------------

BLOCS_SR = [
    ("f70001", "sr-01:R1", "sr-01-ecrire",    0x1000, 0x40),
    ("f70002", "sr-02:R1", "sr-02-hex64",     0x1040, 0x80),
    ("f70003", "sr-03:R1", "sr-03-verdict",   0x10C0, 0x80),
    ("f70004", "sr-04:R1", "sr-04-principal", 0x1140, 0x280),
]

ENTREE = 0x1140                   # e_entry = RVA (ET_DYN : relatif à la base)

NOMS_BLOCS = {
    "f70001": "sr-ecrire", "f70002": "sr-hex64",
    "f70003": "sr-verdict", "f70004": "sr-principal",
}

# Adresses de blocs (appels directs jal — I2 des specs)
A_ECRIRE = 0x1000
A_HEX64 = 0x1040
A_VERDICT = 0x10C0
A_PRINCIPAL = 0x1140

# --- Ancres de base (paires auipc+addi de sr-04 — arithmétique vérifiée au build) -

ANCRE_BASE = 0x1140               # site de l'auipc posant s1 (1re instr. de sr-04)
CIBLE_BASE = 0x0                  # s1 = base + 0 (la base de chargement)
ANCRE_BSS = 0x1148                # site de l'auipc posant s2 (2e instr.)
CIBLE_BSS = 0x2000                # s2 = base + 0x2000 (la fenêtre .bss)

# --- Table ERRNOS (contrat d'erreurs des syscalls — source unique) ----------------

ERRNOS = {
    9: 1,       # EBADF : descripteur invalide — échec nommé (déclaré par
                # sr-04:E1 : la sonde du descripteur ; sr-01 le constate)
}
VERDICT_FATAL = 6                # tout errno hors table : arrêt propre nommé

R_ERRNOS = 0x140                 # [nombre u32] + {errno u32, verdict u32}
R_HEXCHARS = 0x180               # HEXCHARS (16 o) — chiffres hexadécimaux minuscules
HEXCHARS = b"0123456789abcdef"

# --- .rodata : messages de la sonde (longueurs FIGÉES par le plan) -----------------
# (adaptation assumée du plan unix : la ligne de preuve nomme a0, le registre
#  de retour psABI — rax était le registre du profil M6, a0 est celui du M7)

R_MSG_BASE = 0x1C0               # préfixe de la ligne 1 — ET témoin de base
MSG_BASE = b"sonde : base 0x"            # 15 o
L_MSG_BASE = 15

R_MSG_P1 = 0x1E0
MSG_P1 = b"sonde : write(-1) : a0 0x"    # 25 o — préfixe de la ligne sonde 1
L_MSG_P1 = 25

R_MSG_P2 = 0x200
MSG_P2 = b"sonde : write(0x1) : a0 0x"   # 26 o — préfixe de la ligne sonde 2
L_MSG_P2 = 26

R_MSG_VERD = 0x220
MSG_VERD = b" verdict 0x"                # 11 o — entre hex16(a0) et hex16(verdict)
L_MSG_VERD = 11

R_MSG_FIN = 0x240
MSG_FIN = b"\n"                          # 1 o — terminateur de ligne
L_MSG_FIN = 1

R_MSG_FATAL = 0x260
MSG_FATAL = b"sonde : VERDICT_FATAL (arret propre)\n"  # 37 o
L_MSG_FATAL = 37

# --- .bss : tampon de formatage (segment RW, .bss pur, via l'ancre s2) ------------
# Trois sous-zones (I3/I4 de sr-04) : la mémoire traverse les appels et les
# syscalls — les registres volatils non (t0+ meurent dans sr-02/sr-03, a0
# à chaque ecall de sr-01). Le verdict vit donc au tampon. Les adresses
# sont RELATIVES À s2 (= base + 0x2000 — les charges RV64 n'ont que imm12).

R_TAMPON_REL = 0x0               # s2+0  : hex16 du a0 brut (16 o)
R_TAMPON_VERD_REL = 0x10         # s2+16 : hex16 du verdict (16 o)
R_TAMPON_NUM_REL = 0x20          # s2+32 : le verdict u32 (la valeur de retour)
TAMPON_TAILLE = 0x40             # +36..64 libres

# --- Syscalls du jalon (table asm-generic, fiche § 4 — garde anti-table-x86) ------

SYS_WRITE = 64                   # asm-generic (x86-64 : 1 — REFUSÉ au build)
SYS_EXIT_GROUP = 94              # asm-generic (x86-64 : 231 — REFUSÉ au build)
PROT_RX = 0x5                    # PROT_READ | PROT_EXEC (le patch, chantier (c))
PROT_RWX = 0x7                   # le bit exécution RETENU pendant l'écriture

# La table x86-64 REFUSÉE nommément (fiche § 4 : la parité est SÉMANTIQUE,
# jamais lexicale — un bloc RISC-V qui porterait un numéro x86-64 est un
# refus de build NOMMÉ) :
TABLE_X86_REFUSEE = {
    0: "read", 1: "write", 3: "close", 9: "mmap", 10: "mprotect",
    12: "brk", 60: "exit", 231: "exit_group",
}

# --- Versions (R10 : monotonie, lignée du jalon M7) --------------------------------

VERSION_DEV1 = "0.8.0-dev.1"     # premier build du jalon M7 (D149 : la
                                 # 0.8.0-dev.1 vient du premier build M7)
VERSION_U64_DEV1 = 0x00080001
VERSION_U64_MIN = 0x00080000     # plancher
VERSION_RC1 = "0.8.0-rc.1"      # chantier (c) — scellage avec contrôle D146 adapté
VERSION_FINALE = "0.8.0"        # chantier (d) — après run terrain vert

# ============================================================================
# LE CORPUS PARITAIRE RISC-V (chantier M7-(b) — la TROISIÈME instanciation
# de la même couche I : la TROISIÈME, D149-(7) — le diff nul par script)
# ============================================================================
"""Plan d'adressage de l'artefact `corpus` (balise 0.8.0-dev.2) — l'instance
RV64 du corpus nominal de D149-(2) : les DOUZE blocs du patrimoine (les
révisions R+1 de unix/I/, LES MÊMES FICHIERS CANONIQUES — aucune copie :
l'instance les CHARGE depuis unix/I/, empreintes mesurées par
diff_nul_corpus.py ; ancêtres scellés INTACTS dans m0/m1/m2) et le principal
propre au jalon (corpus-13, modèle ah-09). Le durcissement M7-(a) est hérité :
ET_DYN/PIE, e_entry RELATIF, TROIS segments R/RX/RW, offsets == vaddr,
PT_GNU_STACK RW sans X. GÉOMÉTRIE MIROIR du plan unix (D8) : les MÊMES RVA,
les MÊMES fixtures au même plan — seul le demi-octet ISA change.

  - segment 1 PT_LOAD R  : vaddr 0x0, 0x1000 — en-têtes (ehdr 64 + 4 phdr
    224), vecteurs dorés (les MÊMES contenus que m1/unix, aux adresses du
    corpus), chaînes du rituel, STAGING (le journal v2 assemblé POUR la
    croissance), table d'intégrité R10 ;
  - segment 2 PT_LOAD RX : vaddr 0x1000, 0x2000 — les treize blocs (zones
    io/libc/app, D28), la CROISSANCE (0x1D80, la cible du patch y dort en
    ebreak), réserves ebreak ;
  - segment 3 PT_LOAD RW : vaddr 0x3000, filesz 0, memsz 0x1000 — .bss pur :
    curseur d'arène + arène (la MÊME géométrie que m1/unix : curseur à la
    base, arène alignée 64), le verrou tournant du journal (né déverrouillé —
    tcp-11:R2 P5, amoswap.d du profil), l'état du patch et l'entrée sauvée
    (tcp-07:R4) ;
  - PT_GNU_STACK : drapeaux 6 (RW), align 0x10.

LA LEÇON imm12 DU CHANTIER (portée par le plan) : la fenêtre .bss ne peut
PAS vivre à la base de la zone — le verrou (0x3800) serait à +0x800 = 2048,
HORS imm12 de un (constaté au geste même : le premier as_rv64 sur
amoswap.d 0x800(s2) a rendu le REFUS NOMMÉ). L'ancre .bss se pose donc AU
CENTRE de la zone (0x3400) : le curseur vit à -0x400, l'arène à -0x3C0, le
verrou à +0x400 — tout déplacement dans ±2047. C'est la GÉNÉRALISATION du
modèle sr-04 : l'ancre est une FENÊTRE, sa place est un choix du plan, la
portée imm12 la contraint (chaque fenêtre déclarée en I3).

La CIBLE du patch moteur (tcp-07:R4 P5) est l'ENTRÉE DU JOURNAL (tcp-11 @
0x1840) — la démonstration M5-(c) (le chantier M7-(c)) basculera pendant le
trafic ; le staging est le journal v2 (marqueur « j2: ») assemblé pour la
croissance 0x1D80, embarqué dès dev.2. Le patch du profil suit la séquence
§ 5 de la fiche : mprotect RW → copie → fence rw, rw → la bascule (UN mot
aligné, jal — atomique) → fence.i → mprotect RX ; le verrou tournant est
amoswap.d (l'extension A du profil — le portage du lock xchg x86-64).

Série d'identifiants f71xxxx (f70xxxx demeure à la sonde — les séries sont
nommées PAR CARTE, la carte du corpus est une génération 1 propre, sel
distinct de la sonde).
"""

CORPUS_PROFIL = "riscv64-linux-elf64"

# --- Segments du corpus (géométrie miroir du plan unix) ----------------------------

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
    ("f71001", "hello-02:R2", "hello-02-ecrire-r2",   0x1000, 0x40),
    ("f71002", "hello-03:R2", "hello-03-sortir-r2",   0x1040, 0x40),
    ("f71003", "libc-01:R2",  "libc-01-memcpy-r2",    0x1080, 0x40),
    ("f71004", "libc-02:R2",  "libc-02-memcmp-r2",    0x10C0, 0x80),
    ("f71005", "libc-03:R2",  "libc-03-strlen-r2",    0x1140, 0x40),
    ("f71006", "libc-04:R3",  "libc-04-itoa-r3",      0x1180, 0x80),
    ("f71007", "libc-05:R2",  "libc-05-zone-alloc-r2", 0x1200, 0x80),
    ("f71008", "libc-06:R2",  "libc-06-zone-reset-r2", 0x1280, 0x40),
    ("f71009", "libc-07:R2",  "libc-07-memset-r2",    0x12C0, 0x80),
    ("f71010", "libc-08:R3",  "libc-08-autotest-r3",  0x1340, 0x500),
    ("f71011", "tcp-11:R2",   "tcp-11-journal-r2",    0x1840, 0x200),
    ("f71012", "tcp-07:R4",   "tcp-07-patch-r4",      0x1A40, 0x200),
    ("f71013", "corpus-13:R1", "corpus-13-principal", 0x1C40, 0x140),
]

# Le staging du remplaçant : le journal v2 (marqueur « j2: ») assemblé POUR
# l'adresse de croissance — PAS un bloc placé : ses octets vivent au staging
# (.rodata, segment R), la table d'intégrité le porte en première entrée.
BLOC_STAGING = ("f71991", "tcp-11:R2-v2", "tcp-11-journal-v2", 0x1D80, 0x280)

CORPUS_NOMS = {
    "f71001": "ecrire", "f71002": "sortir",
    "f71003": "memcpy", "f71004": "memcmp", "f71005": "strlen",
    "f71006": "itoa", "f71007": "zone_alloc", "f71008": "zone_reset",
    "f71009": "memset", "f71010": "autotest", "f71011": "journal",
    "f71012": "patch", "f71013": "principal",
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

# --- Ancres du corpus (paires auipc+addi — le modèle sr-04 généralisé) -------------
# LA LEÇON imm12 : l'ancre .bss se pose AU CENTRE de la zone (0x3400), la
# base (0x3000) mettrait le verrou (0x3800) à +0x800 = 2048 — hors plage de
# UN (le REFUS NOMMÉ d'as_rv64 au premier geste du chantier). Les fenêtres :

ANCRE_RODATA = 0x1C40         # site = 1re instr. de corpus-13
CIBLE_RODATA = 0x0            # s1 = base + 0 (les .rodata 0x140-0x580 : < 2047)

ANCRE_BSS_CORPUS = 0x1C48     # site = 3e instr. de corpus-13 (2e paire)
CIBLE_BSS_CORPUS = 0x3400     # s2 = base + 0x3400 (le CENTRE .bss — la leçon)

ANCRE_ENTREE = 0x1A54         # site = 6e instr. de tcp-07 (après le cadre
                               # addi/sd/sd et la validation du mode — la paire
                               # est AVANT le branchement apply/rollback)
CIBLE_ENTREE = 0x1840         # s3 = base + 0x1840 (l'entrée du journal ; la
                               # croissance 0x1D80 = s3 + 0x540, la page = s3
                               # & ~0xFFF — tout dans la portée imm12)

# --- Segment R : vecteurs dorés (les MÊMES contenus que m1/unix, plan du corpus) ----

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
R_SLASH = 0x248                # "/" — le séparateur N/21 de la ligne du patrimoine
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

# --- Segment RW : .bss du corpus (l'ancre s2 = base + 0x3400 — LA LEÇON imm12) ------

R_CURSEUR_CORPUS = 0x3000      # qword : curseur d'arène (init 0 au chargement)
ARENE_BASE_CORPUS = 0x3040     # alignée 64 (contractuel : align ∈ [1,64] puissance de 2)
ARENE_TAILLE_CORPUS = 0x7C0    # 1 984 o — la MÊME géométrie que m1/unix, l'arène finit à 0x3800
R_VERROU = 0x3800              # qword : verrou tournant du journal (né 0 = déverrouillé)
R_ETAT_PATCH_CORPUS = 0x3808   # qword : 0 = v1, 1 = v2 (tcp-07:R4 P4)
R_ENTREE_SAUVEE = 0x3810       # qword : le mot original de l'entrée journal (zéro-étendu)

# Déplacements relatifs à l'ancre s2 (base + 0x3400) — TOUS dans ±2047 :
CURSEUR_REL = R_CURSEUR_CORPUS - 0x3400          # -0x400
ARENE_REL = ARENE_BASE_CORPUS - 0x3400           # -0x3C0
VERROU_REL = R_VERROU - 0x3400                   # +0x400
ETAT_REL = R_ETAT_PATCH_CORPUS - 0x3400          # +0x408
ENTREE_SAUVEE_REL = R_ENTREE_SAUVEE - 0x3400     # +0x410
CROISSANCE_REL = A_CROISSANCE - 0x1840           # +0x540 (fenêtre s3, depuis l'entrée)

# --- Syscalls du corpus (I1 par bloc — la table asm-generic, fiche § 4 : la garde) --

SYS_MPROTECT = 226             # asm-generic (x86-64 : 10 — REFUSÉ au build ;
                               # déjà dans TABLE_X86_REFUSEE, la garde vit)
PROT_RX = 0x5                  # PROT_READ | PROT_EXEC (le patch, séquence § 5)
PROT_RWX = 0x7                 # le bit exécution RETENU pendant l'écriture (D39)

# --- Versions du corpus (R10 : monotonie de la lignée) -------------------------------

VERSION_DEV2 = "0.8.0-dev.2"   # le corpus paritaire (chantier M7-(b))
VERSION_U64_DEV2 = 0x00080002

# ============================================================================
# LE DÉMONSTRATEUR DU CHANTIER M7-(c) — la bascule pendant le trafic, RV64
# ============================================================================
"""Plan d'adressage de l'artefact `demo` (le démonstrateur du patch fence.i —
LE CHANTIER M7-(c) : la séquence scratch+fence.i DÉMONTRÉE en exécution sous
qemu, la bascule PENDANT le trafic). Le demo est UN INSTRUMENT du chantier :
il n'est PAS un artefact de la lignée (pas de carte propre — le modèle
unix/demo_patch.py, l'instrument du jalon M6) ; il réutilise LES MÊMES blocs
du corpus (la même notation, les mêmes slots, le même staging, la même table
R10, les mêmes fixtures — l'image ne diffère du corpus QUE par le
démonstrateur et ses chaînes) :

  - le DÉMONSTRATEUR `demo-patch` (f72001, e_entry 0x2000) vit dans la réserve
    RX (0x2000-0x2800 — la réserve ebreak du corpus y cède la place au
    démonstrateur, le reste demeure réserve) ; le corpus-13 (0x1C40) reste À
    SA PLACE dans l'image (inerte — personne ne l'appelle) ;
  - les CHAÎNES du démonstrateur (0x5A0-0xA20, segment R — des slots 0x40) ;
    le SCRATCH itoa (0x3900, .bss — s2+0x500, hors la zone du corpus qui
    finit à 0x3818) ;
  - LES TROIS FENÊTRES du démonstrateur (le modèle sr-04, la leçon imm12) :
    s1 = base+0 (rodata : les chaînes, la table R10), s2 = base+0x3400 (la
    fenêtre .bss CENTRALE — état/entrée_sauvée/verrou/scratch), s9 =
    base+0x1840 (la fenêtre d'INSPECTION de l'entrée du journal — l'entrée à
    +0, la croissance à +0x540). s3 demeure la fenêtre PRIVÉE de tcp-07
    (D156 : les registres sont dédiés par rôle — le démonstrateur ne touche
    JAMAIS s3) ; le démonstrateur est _start : AUCUN cadre, sp ≡ 0 mod 16
    à chaque jal, jamais touché entre les appels (toute sa vie dans les
    non volatils — s8 = i, s7 = le drapeau v2 (4 = la marque), s11/s5 = les
    sauvegardes de la table pour les refus).

LE SCÉNARIO (le modèle unix/demo_patch.py — la bascule pendant le trafic) :
  (a) LE TRAFIC EN SESSION : 1 200 usages de l'ENTRÉE du journal (0x1840 —
      la cible du patch) ; l'apply ENTRE les usages 399 et 400, le rollback
      entre 799 et 800 ; le verdict de CHAQUE usage est CONTRÔLÉ SUR PLACE
      (la longueur rendue == 8 + len(itoa(i)) + marque) ; l'effet constaté
      au geste même (l'entrée appelée rend « j2: verdict » sous v2, la ligne
      sans marque sous v1) ;
  (b) LE RETOUR À L'ÉTAT IMAGE : l'entrée revenue à l'octet près
      (== ENTREE_SAUVEE), le remplaçant DORMANT (la croissance porte le
      remplaçant, pas la réserve), le verrou rendu ;
  (c) LES REFUS NOMMÉS : mode invalide 1, états incohérents 4, staging
      absent 2 et somme divergente 3 — les DEUX derniers par mutation
      IN-GUEST de la table R10 (le démonstrateur ouvre la page R par
      mprotect — LE MÊME SERVICE que le bloc, le geste est nommé dans sa
      spec), restaurée après chacun ;
  (d) LA FRONTIÈRE NOMMÉE : code 5 (le service refuse) n'est pas
      productible sous qemu-user de façon naturelle (l'hôte accorde RWX sur
      mapping privé) — la branche vit fail-closed dans le bloc (bltz →
      refus5, constaté structurellement) ; la concurrence réelle est HORS
      périmètre (fiche § 5 : le corpus M7 est mono-fil — portée de fence.i :
      le cœur courant) ; le DEP falsifié (0x7→0x3) est une épreuve
      HOST-SIDE (le mutant du FICHIER, un run séparé — SIGSEGV attendu).
"""

# --- Le démonstrateur : bloc, entrée, fenêtres --------------------------------------

BLOC_DEMO = ("f72001", "demo-patch:R1", "demo-patch", 0x2000, 0x800)
DEMO_ENTREE = 0x2000              # e_entry = RVA (le démonstrateur EST _start)
DEMO_SCRATCH = 0x3900             # .bss (s2+0x500) — le tampon itoa du trafic
DEMO_SCRATCH_REL = 0x500          # … relativement à s2 (base+0x3400)

# Les fenêtres du démonstrateur (les paires auipc+addi — sites = 3 premières
# paires d'instructions ; s3 demeure à tcp-07 SEUL — D156, jamais recyclé)
ANCRE_D_RODATA = 0x2000          # s1 = base + 0 (les chaînes + la table R10)
CIBLE_D_RODATA = 0x0
ANCRE_D_BSS = 0x2008             # s2 = base + 0x3400 (la fenêtre CENTRALE)
CIBLE_D_BSS = 0x3400
ANCRE_D_ENTREE = 0x2010          # s9 = base + 0x1840 (l'INSPECTION : entrée
CIBLE_D_ENTREE = 0x1840          # à +0, croissance à +0x540)

# --- Les chaînes du démonstrateur (segment R, slots 0x40, 0x5A0-0xA20) --------------

R_D_TRAFIC = 0x580
D_TRAFIC = b"trafic "                              # 7 o — le préfixe du trafic
L_D_TRAFIC = 7
R_D_NL = 0x588
D_NL = b"\n"                                       # 1 o — le suffixe du trafic
L_D_NL = 1
R_D_VERDICT = 0x58C
D_VERDICT = b"verdict"                             # 7 o — la ligne de l'épreuve d'effet
L_D_VERDICT = 7
R_D_APPLY = 0x594
D_APPLY = b"demo: PASS apply 0 (usages 399/400)\n"
L_D_APPLY = 36
R_D_TRAMP = 0x5B8
D_TRAMP = b"demo: PASS trampoline (le mot a bascule)\n"
L_D_TRAMP = 41
R_D_EFFET = 0x5E4
D_EFFET = b"demo: PASS effet j2: verdict (v2 effectif)\n"
L_D_EFFET = 43
R_D_ROLLB = 0x610
D_ROLLB = b"demo: PASS rollback 0 (usages 799/800)\n"
L_D_ROLLB = 39
R_D_V1 = 0x638
D_V1 = b"demo: PASS v1-retour (verdict sans marque)\n"
L_D_V1 = 43
R_D_PTRAFIC = 0x664
D_PTRAFIC = b"demo: PASS trafic 1200 verdicts (800 v1 + 400 v2)\n"
L_D_PTRAFIC = 50
R_D_REST = 0x698
D_REST = b"demo: PASS restauration (entree a l'octet)\n"
L_D_REST = 43
R_D_DORM = 0x6C4
D_DORM = b"demo: PASS dormance (croissance habitee)\n"
L_D_DORM = 41
R_D_VERROU = 0x6F0
D_VERROU = b"demo: PASS verrou (rendu un-pour-un)\n"
L_D_VERROU = 37
R_D_REFMODE = 0x718
D_REFMODE = b"demo: PASS refus-mode 1\n"
L_D_REFMODE = 24
R_D_REFETAT = 0x730
D_REFETAT = b"demo: PASS refus-etat 4 (x2)\n"
L_D_REFETAT = 29
R_D_REFABS = 0x750
D_REFABS = b"demo: PASS refus-absent 2\n"
L_D_REFABS = 26
R_D_REFSOM = 0x76C
D_REFSOM = b"demo: PASS refus-somme 3\n"
L_D_REFSOM = 25
R_D_FIN = 0x788
D_FIN = b"demo: VERDICT VERT (fence.i demontre)\n"
L_D_FIN = 38
R_D_ECHEC = 0x7B0
D_ECHEC = b"demo: ECHEC\n"
L_D_ECHEC = 12
# LA LEÇON imm12 (D156) APPLIQUÉE AU DÉMONSTRATEUR : les chaînes vivent
# PACKÉES dans la zone libre 0x580-0x7BC — SOUS la portée de la fenêtre
# s1 = base+0 (le zone 0x5A0-0xA20 du premier jet dépassait imm12 de un
# geste : le REFUS NOMMÉ d'as_rv64 ; la zone libre après la table est
# 0x580-0x7FF, les messages ont été comptés pour y tenir — le plan paie
# la portée, jamais l'instrument).

# --- Les symboles du scénario (les cibles et fenêtres, vérifiés au build) -----------

A_JOURNAL_DEMO = 0x1840          # l'ENTRÉE du journal — la cible du patch
A_PATCH_DEMO = 0x1A40
SYS_MPROTECT_DEMO = 226          # asm-generic (10 : REFUSÉ nommément — la garde)
