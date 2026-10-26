# Couche I — expérience d'auto-hébergement (D34, profil x86-64-linux-elf64)

Neuf spécifications nouvelles, écrites avant la notation (R2, provenance
`écrite-avant-code`). Elles instancient le gabarit § 2.2 de la spécification
v0.4.0 et étendent le registre figé du projet (m0/I/README.md, § 2.1) par le
domaine **`ah`, réservé à l'auto-hébergement de l'agent** (D34) — les blocs
que l'agent écrit pour son propre travail, sur son propre terrain d'exécution
(le bac à sable Linux). Aucun autre domaine n'est créé ; l'artefact est le
premier du profil `x86-64-linux-elf64` (anticipation restreinte sur M6, D34).

| Spécification | Bloc machine (carte) | Rôle | Zone |
|---|---|---|---|
| ah-01:R1 | d40001 | Écriture par appel système (sys_write) | sys @ 0x1000 |
| ah-02:R1 | d40002 | Lecture par appel système (sys_read) | sys @ 0x1040 |
| ah-03:R1 | d40003 | Terminaison par appel système (sys_exit) | sys @ 0x1080 |
| ah-04:R1 | d40004 | Initialisation du contexte SHA-256 (H0) | sha @ 0x1100 |
| ah-05:R1 | d40005 | Compression d'un bloc de 64 octets (FIPS § 6.2.2) | sha @ 0x1200 |
| ah-06:R1 | d40006 | Absorption tamponnée (invariance de découpage) | sha @ 0x1400 |
| ah-07:R1 | d40007 | Finalisation : bourrage + longueur + extraction | sha @ 0x1500 |
| ah-08:R1 | d40008 | Encodage hexadécimal 32 o → 64 caractères | hex @ 0x1600 |
| ah-09:R1 | d40009 | Orchestration — point d'entrée ELF `hachoir` | app @ 0x1680 |

L'artefact `hachoir` est un hacheur SHA-256 conforme FIPS 180-4 : il lit un
fichier, calcule l'empreinte et l'écrit sur stdout au format exact de
`sha256sum` (`<hex>  <chemin>\n`) — un remplaçant direct, vérifiable par diff.
L'ABI est SysV x86-64 (arguments rdi, rsi, rdx, rcx, r8, r9 ; zone rouge de
128 octets — le piège miroir de msx64 documenté § 8.3 de la spécification) et
l'interface noyau est l'interface d'appel Linux (nr dans rax, 4e argument en
**r10**, rcx/r11 détruits, retour négatif = -errno) — les blocs sys la
spécifient intégralement : aucun octet de la chaîne n'est implicit.

Contexte SHA-256 (état partagé ah-04→07, 112 octets, .bss @ RVA 0x3000) :
H[8] u32 @ +0 (ordre natif petit-boutiste), tampon[64] @ +32, remplissage
u32 @ +96 (octets valides du tampon), réservé u32 @ +100, total u64 @ +104
(octets absorbés cumulés).

La discipline des adresses suit D28/D33 : slots multiples de 64, alignés 16,
padding inter-blocs ≥ 16, réserve int3 pour la croissance. Le verrou croisé
R8 s'applique dès le premier octet ; la carte de la lignée auto-hôte est une
génération 1 propre (sel de dérivation distinct, clés projet partagées D27).
