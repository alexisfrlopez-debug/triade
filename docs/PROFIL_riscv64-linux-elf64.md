# FICHE DE PROFIL — `riscv64-linux-elf64` (jalon M7, universalité inter-ISA)

> Profil de cible au sens de la spécification § 16 : les sept éléments plus le huitième
> livrable v0.4.0, chacun constatable. Fondations : D14 (universalité), D149 (ouverture
> du programme M6/M7 — M7 s'exécute APRÈS M6, l'ordre isole chaque variable : le
> mécanisme des profils d'abord, l'indépendance de l'ISA ensuite). Cette fiche est
> **écrite dès l'ouverture** pour que le jalon M6 n'emprunte rien d'impensé, mais ses
> chantiers ne démarrent qu'au bouclage de M6 — les constats labo ci-dessous sont
> datés du 04/11/2026 et seront re-vérifiés au chantier (a).

**Identifiant** : `riscv64-linux-elf64` · **ISA** : RISC-V 64 bits (RV64IMA +
Zifencei, sans extension C — voir § 1) · **OS** : Linux (noyau ≥ 5.x, page 4 Kio) ·
**Format** : ELF64 petit-boutiste · **Statut** : spécifié, jalon M7 ouvert le
04/11/2026 (D149), exécution différée derrière M6.

---

## 1. ISA et types

- **Cible** : RV64IMA + **Zifencei** (l'extension `fence.i`, requise par le patch à
  chaud § 5) — **SANS extension C** : toutes les instructions du profil font
  **4 octets, alignement 4**. Le choix est délibéré et assumé : l'absence
  d'instructions compressées rend la granularité des blocs et la bascule de patch
  **uniformes** (le psABI autorise un cœur RV64GC à exécuter du RV64IMA —
  sous-ensemble strict) ; l'encodage variable 2/4 o de l'extension C est un coût
  de complexité que le jalon refuse (fonction objectif : la sécurité d'abord).
- Largeur native 64 bits ; `usize`/pointeurs 8 octets ; petit-boutiste ; alignements
  naturels (dont l'alignement 4 des instructions, gardé par le layout).
- Arithmétique entière (M : mul/div 64 bits) ; flottants hors corpus M7.

## 2. ABI d'appel — psABI RISC-V (LP64, soft-float)

| Convention | Règle | Le piège documenté |
|---|---|---|
| Arguments | a0–a7 (x10–x17), puis la pile, de gauche à droite | troisième convention du projet : ni msx64 ni SysV |
| Retour | a0 (a0:a1 pour 128 bits) | — |
| **Zone rouge** | **AUCUNE** — stocker sous sp sans allocation est interdit | **le piège inverse de SysV x86-64** (§ 16.2) : l'agent venant du profil M6 doit RÉAPPRENDRE l'interdit msx64 — frag-con porte la convention effective de chaque bloc |
| Volatils | t0–t6 (x5–x7, x28–x31), a0–a7 | — |
| Non volatils | s0–s11 (x8, x9, x18–x27), ra traité par la convention de sauvegarde | — |
| Registres dédiés | zero = x0, ra = x1, sp = x2, gp = x3, tp = x4 | — |
| Alignement | sp multiple de 16 au point d'appel | identique aux deux profils x86-64 |

Registre de travail interne du projet : **t1** (volatil) — le portage de la convention
R10/R11 des profils x86-64 ; la table de correspondance vit dans frag-con.

## 3. Format d'exécutable — ELF64 durci

- Magie `\x7fELF`, EI_CLASS 2, EI_DATA 1, EI_VERSION 1 ; **e_machine = `0xF3`**
  (EM_RISCV) ; **e_flags = 0** (ni RVC ni float-abi — cohérent avec § 1).
- **ET_DYN (PIE)** à base aléatoire, e_entry relatif ; trois segments R/RX/RW ;
  **PT_GNU_STACK** RW sans X — exigé par le psABI (NX) ; W^X vérifié depuis les phdr.
- Le writer ELF64 durci du jalon M6 (fiche `x86-64-linux-elf64` § 3) est repris :
  seule change la moitié ISA de l'en-tête (e_machine, e_flags, e_entry) — le
  mécanisme des en-têtes écrits à la main est déjà prouvé.

## 4. Interface système — syscalls directs (table asm-generic)

- Instruction `ecall` ; a7 = numéro, a0–a5 les arguments, a0 le retour ; échec =
  a0 ∈ [−4095, −1] avec −errno — même contrat fail-closed ERRNOS que M6
  (succès exact, continuations nommées, VERDICT_FATAL).
- **Les numéros NE SONT PAS ceux de x86-64** : Linux RISC-V suit la table
  asm-generic — table du jalon : `read` = 63, `write` = 64, `close` = 57,
  `openat` = 56, `brk` = 214, `mmap` = 222, `mprotect` = 226, `exit` = 93,
  `exit_group` = 94 — numéros autorisés PAR BLOC, tout numéro non motivé est un
  refus de build.
- L'écart de table est un garde du jalon : un bloc RISC-V qui porterait un numéro
  x86-64 (write = 1) est un refus nommé — la parité est SÉMANTIQUE (les mêmes
  intentions), jamais lexicale (pas les mêmes numéros).

## 5. Patch à chaud — bascule par registre scratch + `fence.i`

- **Pas de trampoline relatif 5 octets** : à taille d'instruction fixe, la bascule
  charge l'adresse cible dans un registre scratch puis saute — séquence de référence
  du profil : (1) `mprotect` la page du bloc RW ; (2) écrire le nouveau bloc ;
  (3) `fence rw, rw` (barrière mémoire, écritures visibles) ; (4) écrire la bascule
  (l'entrée de la table de saut ou l'instruction de branchement) — **écriture
  alignée 4 o ou 8 o, atomique sur RV64** ; (5) **`fence.i`** — invalidation du
  cache d'instructions du cœur courant ; (6) `mprotect` RX ; (7) saut via le
  scratch (`jalr x0, 0(t1)`). L'ancienne cible est conservée : le rollback
  rebascule vers elle (le modèle du manuel § 7.5).
- **Portée de `fence.i` : le cœur courant** — la séquence multi-cœur (IPI +
  synchronisation) est HORS périmètre du jalon : le corpus M7 est mono-fil, la
  frontière est nommée ici pour ne jamais être lue comme une généralité.
- Le registre scratch de la bascule : **t1** (§ 2), jamais un registre d'argument.

## 6. Moteur de notation et round-trip — LE chantier propre à M7

- **Constat labo (04/11/2026)** : keystone 0.9.2 **ne porte pas l'architecture
  RISC-V** (`KS_ARCH_RISCV` absent du module Python) ; capstone 5.0.7 **désassemble
  RV64** (constaté : `addi` décodé depuis ses octets). L'assemblage n'a donc AUCUN
  moteur en l'état — c'est un livrable du jalon, pas une surprise.
- **Livrable (a) du jalon** : l'**assembleur RV64IMA+Zifencei maison du dépôt**
  (recommandé — l'encodage est régulier : six formats R/I/S/B/U/J, 4 o, champs fixes ;
  dans la lignée « à la main » du projet, sans dépendance nouvelle) — OU un moteur
  tiers s'il passe la même porte : round-trip **capstone comme juge unique**
  (assemble → désassemble → ré-assemble, tout écart d'instruction, d'opérande ou
  de taille = échec de build), corpus d'instructions du profil exigé à 100 %.
- Le vérificateur de round-trip (le juge) existe déjà : capstone 5.0.7 constaté.

## 7. Granularité des blocs et adresses stables

- Slots alignés 4 octets ; padding intra-slot : **NOP canonique `addi x0, x0, 0`
  (0x00000013)** ; réserves d'inaccessibilité : **`ebreak` (0x00100073)** —
  l'équivalent exact du rôle `int3`/`ud2` des profils x86-64 (garde défensive,
  fail-closed).
- Adresses stables R7 **par profil** ; le layout du jalon (`riscv/layout.py`,
  convention D149) reprend le modèle D8 ; la correspondance bloc ↔ slot vit dans
  frag-loc de la carte du jalon.

## 8. Politique anti-rollback et vérification au chargement (R10 décliné)

- Porte R10 identique au profil M6 (checksums des blocs scellés au lancement,
  R_VERSION ≥ plancher, conformité environnement, arrêt propre fail-closed) —
  l'image est ELF64, le mécanisme est le même, seuls les octets changent.
- Balise du jalon M7 = **0.8.0** (rc.1 → finale après validation) ; LICENSE
  anti-rollback amendé à chaque scellage, modèle D147.
- Contrôle D146 adapté : exécution full-ELF à la base réelle **sur l'exécuteur du
  jalon** (§ 10) avant tout scellage rc/final.

## 9. Suite de conformité (spec § 8.2) — déclinée

| # | Élément | Contrôle sur l'artefact du jalon |
|---|---|---|
| 1 | ISA et types | magie ELF64 LE, e_machine 0xF3, e_flags 0 ; instructions toutes à 4 o (refus d'un encodage 2 o = garde anti-C) |
| 2 | ABI d'appel | appels/retours conformes psABI ; AUCUNE zone rouge (frag-con) ; alignement sp 16 |
| 3 | Format | ET_DYN, trois segments R/RX/RW, PT_GNU_STACK sans X, W^X |
| 4 | Interface système | numéros asm-generic autorisés PAR BLOC (garde anti-table-x86) ; contrat ERRNOS |
| 5 | Patch à chaud | séquence scratch + `fence.i` DÉMONTRÉE en exécution, écriture alignée atomique, rollback vivant |
| 6 | Notation | round-trip 100 % sur le corpus (assembleur maison + capstone juge) |
| 7 | Granularité et padding | adresses stables après patch (R7), NOP/ebreak constatés |

## 10. Exécution et terrain — la réserve instrumentale nommée

- **Constat labo (04/11/2026)** : aucun binaire `qemu-riscv64` dans le bac à sable —
  l'installation (qemu-user statique) est le prérequis du chantier (a), re-vérifié
  avant usage.
- **L'exécuteur du jalon : qemu-riscv64 (émulation de processus, TCG)** — le noyau
  Linux et les syscalls sont RÉELS (qemu-user traduit les instructions et relaie les
  appels au noyau hôte) ; l'ISA est exécutée par l'émulateur, **pas par une fer
  RISC-V** : cette limite est une **réserve instrumentale nommée** (D149), consignée
  dans chaque verdict — le protocole ne la déguise jamais en exécution native.
- Le terrain du jalon (machine du développeur) exécute le même artefact sous
  qemu-riscv64 (WSL2/VM Linux) — la parité inter-ISA se prouve par le MÊME oracle
  vert sur les TROIS profils et par le verrou croisé multi-profils (spec § 18-M7) ;
  l'export de continuité multi-profils de bout en bout (§ 6 du manuel : déchiffrer,
  vérifier signature, verrou croisé, régénérer l'oracle, reprendre) clôt le jalon.
