# Couche I — lignée du jalon M6 (unix/, D149) : la sonde du durcissement

Quatre spécifications nouvelles, écrites avant la notation (R2, provenance
`écrite-avant-code`). Elles instancient le gabarit § 2.2 de la spécification
et étendent le registre figé du projet (m0/I/README.md, § 2.1) par le domaine
**`su`, réservé à la sonde du jalon M6** (chantier M6-(a) — le durcissement
format) : le premier artefact du jalon, dans `unix/` (convention de dossiers
D149-(5)). Le domaine `ah` reste celui de l'échelle d'auto-hébergement D34 ;
aucune adresse n'est héritée — les deux lignées ne partagent que la couche
de méthode (le chantier (b) portera la parité du patrimoine, pas la sonde).

| Spécification | Bloc machine (carte) | Rôle | Zone |
|---|---|---|---|
| su-01:R1 | f60001 | Écriture par appel système (sys_write) | sys @ 0x1000 |
| su-02:R1 | f60002 | Formatage hexadécimal u64 → 16 caractères | hex @ 0x1040 |
| su-03:R1 | f60003 | Verdict d'erreur syscall (table ERRNOS) | sys @ 0x10C0 |
| su-04:R1 | f60004 | Orchestration — point d'entrée ELF `sonde` | app @ 0x1140 |

L'artefact `sonde` est la démonstration exécutable du durcissement format
(le critère de sortie du chantier M6-(a)) : image **ET_DYN/PIE** chargée par
le noyau à une base aléatoire — la sonde calcule sa propre base à l'exécution
(`lea rip` sur le témoin `.rodata`, lien-temps soustrait) et l'émet en tête
de sortie ; **trois segments R/RX/RW** (W^X : aucun segment inscriptible
exécutable, vérifié depuis les phdr par le build) ; **PT_GNU_STACK sans X**
(NX explicite) ; **table ERRNOS** (le contrat d'erreurs des syscalls, miroir
de la table HRESULTS) exercée en exécution sur ses deux branches : une
sonde volontaire `write(-1, …)` rend -EBADF (errno nommé → verdict 1), une
sonde volontaire `write(1, 0x1, …)` rend -EFAULT (errno hors table →
VERDICT_FATAL 6 → arrêt propre, code de sortie 6).

L'ABI est SysV x86-64 (arguments rdi, rsi, rdx, rcx, r8, r9 ; zone rouge
permise aux feuilles — le piège miroir de msx64 documenté fiche § 2 ; r10/r11
registres de travail internes du projet, volatils) et l'interface noyau est
l'appel système direct Linux (nr dans rax, 4e argument en r10, rcx/r11
détruits par l'instruction, retour négatif = -errno) — chaque bloc sys le
spécifie intégralement : aucun octet de la chaîne n'est implicit.

La discipline des adresses suit D28/D33 : slots multiples de 64, alignés 16,
padding inter-blocs >= 16, réserves int3. Le verrou croisé R8 s'applique dès
le premier octet ; la carte de la lignée du jalon est une génération 1
propre (sel de dérivation distinct de l'échelle auto-hôte, clés projet
partagées D27). La série d'identifiants f6xxxx est nommée par la carte.
