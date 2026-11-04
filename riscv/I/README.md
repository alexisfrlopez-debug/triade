# Couche I — lignée du jalon M7 (riscv/, D149) : la sonde de la notation RV64

Quatre spécifications nouvelles au chantier M7-(a), écrites avant la
notation (R2, provenance `écrite-avant-code`). Elles instancient le
gabarit § 2.2 de la spécification et étendent le registre figé du projet
(m0/I/README.md, § 2.1) par le domaine **`sr`, réservé à la sonde du jalon
M7** (chantier M7-(a) — le moteur de notation RV64) : le premier artefact
du jalon, dans `riscv/` (convention de dossiers D149-(5)). Les domaines
`su` (jalon M6, unix/) et `sr` mirent la MÊME démonstration — la
géométrie du plan d'adressage est partagée : les deux lignées ne
diffèrent que par le demi-octet ISA de l'image (e_machine, e_flags,
instructions) — c'est le PROTOCOLE de l'universalité : l'intention
s'écrit une fois, les octets existent par plateforme.

| Spécification | Bloc machine (carte) | Rôle | Zone |
|---|---|---|---|
| sr-01:R1 | f70001 | Écriture par appel système (sys_write asm-generic) | sys @ 0x1000 |
| sr-02:R1 | f70002 | Formatage hexadécimal u64 → 16 caractères | hex @ 0x1040 |
| sr-03:R1 | f70003 | Verdict d'erreur syscall (table ERRNOS) | sys @ 0x10C0 |
| sr-04:R1 | f70004 | Orchestration — point d'entrée ELF `sonde` | app @ 0x1140 |

L'artefact `sonde` est la démonstration exécutable du chantier M7-(a) :
image **ET_DYN/PIE** chargée par l'exécuteur du jalon (qemu-riscv64 —
réserve instrumentale D149 NOMMÉE : l'ISA est exécutée par l'émulateur de
processus, le noyau et les syscalls sont RÉELS, le protocole ne déguise
jamais l'émulation en exécution native) ; la sonde calcule sa propre base
à l'exécution (la PAIRE auipc+addi — le portage RV64 du `lea rip`
lié-temps soustrait : auipc lit pc, addi soustrait le lien-temps) et
l'émet en tête de sortie ; **trois segments R/RX/RW** (W^X depuis les
phdr) ; **PT_GNU_STACK sans X** (NX — exigé par le psABI RISC-V) ;
**table ERRNOS** exercée en exécution sur ses deux branches : une sonde
volontaire `write(-1, …)` rend -EBADF (errno nommé → verdict 1), une
sonde volontaire `write(1, 0x1, …)` rend -EFAULT (errno hors table →
VERDICT_FATAL 6 → arrêt propre, code de sortie 6).

Le MOTEUR DE NOTATION du jalon vit à `outils/as_rv64.py` (l'assembleur
RV64IMA+Zifencei maison — fiche § 6 : keystone ne porte pas l'ISA) et sa
preuve à `notation/porte_roundtrip.py` (capstone JUGE UNIQUE, round-trip
100 % sur le corpus d'instructions du profil, DEUX directions : le
corpus de textes, et l'espace d'encodage légal tout entier). La notation
des blocs vit à `notation/` (générée par `outils/auteur.py` depuis les
brouillons étiquetés — l'arithmétique d'adresses de l'auteur : paires
d'ancres auipc+addi, décalages B/J relatifs documentés).

La discipline des adresses suit D28/D33 : slots multiples de 64, alignés
16, padding inter-blocs >= 16, réserves ebreak. Le verrou croisé R8
s'applique dès le premier octet ; la carte de la sonde est une génération
1 propre (QUATRIÈME sel de dérivation : m2, hachoir D34, jalon unix,
jalon riscv — clés projet partagées D27). La série d'identifiants f7xxxx
est nommée par la carte (f6xxxx demeure au jalon unix). Le jalon M7
instanciera la MÊME couche I que M6 en TROISIÈME (le corpus paritaire,
chantier M7-(b)) — les specs `su-*` de unix/I/ demeurent INTACTES.

## Le corpus paritaire (chantier M7-(b) — la TROISIÈME instanciation)

Le chantier M7-(b) ajoute l'instance RV64 du corpus nominal de D149-(2) :
les DOUZE blocs du patrimoine + le principal propre au jalon. L'instance
ne COPIE rien : elle **CHARGE les fichiers canoniques de `unix/I/`**
(empreintes mesurées par `diff_nul_corpus.py`, aucune copie nulle part —
la thèse du diff nul : l'intention vit dans I, pas dans les octets) ; la
notation est l'instance à elle (RV64 native, `riscv/notation/`), la
GÉOMÉTRIE est MIROIR du plan unix (D8 : les MÊMES RVA, les MÊMES
fixtures).

| Bloc | Spec (CANONIQUE, unix/I/) | Bloc machine | Rôle | Zone |
|---|---|---|---|---|
| hello-02:R2 | hello-02-ecrire-r2.md | f71001 | Interface — écriture | io @ 0x1000 |
| hello-03:R2 | hello-03-sortir-r2.md | f71002 | Interface — terminaison | io @ 0x1040 |
| libc-01:R2 | libc-01-memcpy-r2.md | f71003 | memcpy (pur) | libc @ 0x1080 |
| libc-02:R2 | libc-02-memcmp-r2.md | f71004 | memcmp (pur) | libc @ 0x10C0 |
| libc-03:R2 | libc-03-strlen-r2.md | f71005 | strlen (pur) | libc @ 0x1140 |
| libc-04:R3 | libc-04-itoa-r3.md | f71006 | itoa (pur) | libc @ 0x1180 |
| libc-05:R2 | libc-05-zone-alloc-r2.md | f71007 | zone-alloc (pur) | libc @ 0x1200 |
| libc-06:R2 | libc-06-zone-reset-r2.md | f71008 | zone-reset (pur) | libc @ 0x1280 |
| libc-07:R2 | libc-07-memset-r2.md | f71009 | memset (pur) | libc @ 0x12C0 |
| libc-08:R3 | libc-08-autotest-r3.md | f71010 | auto-test (21 vecteurs dorés) | app @ 0x1340 |
| tcp-11:R2 | tcp-11-journal-r2.md | f71011 | ligne de journal (verrou amoswap.d) | app @ 0x1840 |
| tcp-07:R4 | tcp-07-patch-r4.md | f71012 | moteur de patch (mprotect 226, fence.i) | app @ 0x1A40 |
| corpus-13:R1 | corpus-13-principal.md | f71013 | Orchestration — `_start` | app @ 0x1C40 |

L'artefact `corpus` (balise **0.8.0-dev.2**, 12 288 o, sha256
b34a7147…) hérite le durcissement de la sonde (ET_DYN/PIE, R/RX/RW,
PT_GNU_STACK sans X) et porte le patrimoine : le rituel de parité de
corpus-13 lance l'auto-test (la ligne « TRIADE M1 : minilibc 21/21 OK » —
LE MÊME observable que les instances Windows et x86-64-linux, § 8.3 PAR
EXÉCUTION), journalise le verdict par tcp-11 (le verrou tournant
amoswap.d — l'extension A du profil, le portage du lock xchg) et termine
au code du verdict par sortir. tcp-07 vit dans l'image avec son staging
(le journal v2 « j2: » assemblé POUR la croissance 0x1D80) et LA SÉQUENCE
du profil (fence rw,rw + fence.i + la bascule un mot jal — fiche § 5) ;
sa démonstration complète est le chantier M7-(c).

LA LEÇON imm12 du chantier (D156) vit ici : l'ancre .bss (s2) se pose AU
CENTRE de la zone (base + 0x3400), PAS à sa base — le verrou (0x3800) vu
de la base vivrait à +0x800 = 2048, hors imm12 de UN. Les fenêtres :
s1 = base (rodata), s2 = base+0x3400 (bss CENTRE), s3 = base+0x1840
(l'entrée du journal — la fenêtre PRIVÉE de tcp-07) ; les registres sont
DÉDIÉS PAR RÔLE (jamais recyclés), t1 n'est touché par AUCUN bloc.

La discipline des adresses suit D28/D33 (slots multiples de 64, alignés
16, padding ≥ 16, réserves ebreak). Le verrou croisé R8 s'applique dès
le premier octet ; la carte du corpus est une génération 1 propre
(SIXIÈME sel de dérivation : m2, hachoir D34, sonde unix, corpus unix,
sonde riscv, corpus riscv — clés projet partagées D27). La série
d'identifiants f71xxxx est nommée par la carte du corpus (f70xxxx demeure
à la sonde).
