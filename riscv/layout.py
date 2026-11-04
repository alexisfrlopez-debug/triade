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
