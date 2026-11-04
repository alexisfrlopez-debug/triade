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
