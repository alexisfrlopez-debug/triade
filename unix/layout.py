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
