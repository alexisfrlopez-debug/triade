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
04/11/2026 (D149) — **le chantier M7-(a) RÉALISÉ le 05/11/2026** (le moteur
de notation RV64 + la sonde aux oracles verts, Entrée 150, D155 ; balise
`0.8.0-dev.1` posée par le premier build du jalon) ; **le chantier M7-(b)
RÉALISÉ le 05/11/2026** (le corpus paritaire, Entrée 152, D156 ; balise
`0.8.0-dev.2` — la TROISIÈME instanciation de la même couche I, le diff nul
VERT, l'oracle qemu vert sur pièces) ; **le chantier M7-(c) RÉALISÉ le
05/11/2026** (le patch fence.i DÉMONTRÉ en exécution par le démonstrateur
invité, le verrou croisé multi-profils, Entrée 153, D157 ; balise
`0.8.0-rc.1` SCELLÉE) ; **le chantier M7-(d), LA PART LABORATOIRE RÉALISÉE
le 05/11/2026** (l'export de continuité MULTI-PROFILS vert de bout en bout
+ le kit terrain DÉPOSÉ au coffre /test avec l'instrument EMBARQUÉ + la
clôture D143 du run m6d, Entrée 154, D158) ; **LE RUN TERRAIN VERT SUR
PIÈCES + LE RECOUP LABORATOIRE VERT 29/29 SUR PIÈCES CROISÉES + LA FINALE
`0.8.0` SCELLÉE le 05/11/2026** (Entrée 155, D159 : le run du développeur
WSL2 — un autre noyau, l'instrument du kit, 16/16 PASS — le recoup le code
pour juge, l'attendu re-généré au geste même ; `--sceller-final` les gardes
vivantes constatées, l'artefact INTACT sha `ec343b4e…`) — **LE JALON M7
FRANCHI, l'universalité DÉMONTRÉE : chaque profil déclaré supporté a franchi
ses critères (win `0.6.0` / linux `0.7.0` / riscv `0.8.0`)**.

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

- **Constat labo (04/11/2026, re-vérifié au chantier M7-(a) le 05/11)** :
  keystone 0.9.2 **ne porte pas l'architecture RISC-V** (`KS_ARCH_RISCV`
  absent du module Python — re-constaté au geste même) ; capstone 5.0.7
  **désassemble RV64** (constaté : `addi` décodé depuis ses octets).
  L'assemblage n'a donc AUCUN moteur en l'état — c'est un livrable du
  jalon, pas une surprise.
- **ACQUIS (05/11/2026, chantier M7-(b), Entrée 152 — D156 : LA PORTE S'ÉTEND
  AVEC L'INSTRUMENT)** : l'extension A du profil est entrée au geste qui
  l'exigeait — `amoswap.w/d` (aq/rl nuls, le seul AMO du corpus : le verrou
  tournant de tcp-11, le portage du lock xchg) ; l'ISA AMO adresse [rs1]
  SANS déplacement (funct5 aux bits 31:27 — le champ imm12 n'existe pas dans
  ce format) : une demande de déplacement est un REFUS NOMMÉ, le déplacement
  vit dans la formation `addi` déclarée ; la porte est étendue AU MÊME GESTE
  aux DEUX directions : **AVANT 791 textes + INVERSE 1045 encodages légaux,
  100 %** — les autres AMO (amoadd…) et aq/rl armés vivent hors instrument,
  la frontière est nommée (la couverture se démontre, elle ne se décrète pas).
- **ACQUIS (05/11/2026, chantier M7-(a), Entrée 150)** : l'**assembleur
  RV64IMA+Zifencei maison du dépôt EST** — `riscv/outils/as_rv64.py`
  (six formats R/I/S/B/U/J, 4 o exactement, refus NOMMÉS fail-closed sur
  toute plage, tout décalage impair, tout mnémonique hors profil ; le jeu
  EXACT des pseudos du juge : mv, not, neg, negw, sext.w, seqz, snez,
  sgtz, sltz, beqz/bnez/bgez/bltz/bgtz/blez, j, jal implicite, jalr à
  1-2-3 opérandes, ret, nop, fence, fence.tso) — et sa preuve vit à
  `riscv/notation/porte_roundtrip.py` : **round-trip 100 % en DEUX
  directions** (783 textes du corpus du profil en AVANT + 1037 encodages
  légaux en INVERSE — le rendu INTÉGRAL du juge ré-assemble en ses
  octets : c'est la direction inverse qui attrape ce que l'auteur n'avait
  pas prévu), **capstone juge unique**. Quatre leçons attrapées par la
  porte au geste même (D155) : le pseudo `negw` manquant, le funct7 de
  SEPT bits des décalages W, la forme deux-opérandes mémoire de jalr, la
  frontière « unknown » du juge sur les champs fence vides.
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
- **L'ancre et sa limite (D254, atelier W17R3R10)** : même porte que M6 ; l'ancre
  d'exploitation serait la **chaîne de boot signée** (FIT/U-Boot) sur silicium —
  **EN ATTENTE** (exécution QEMU seulement au bac). Le plancher signé et l'époque de
  l'état local ne protègent ni d'un administrateur local ni d'une restauration
  cohérente du couple binaire + état.
- Balise du jalon M7 = **0.8.0** (rc.1 → finale après validation) ; LICENSE
  anti-rollback amendé à chaque scellage, modèle D147. La 0.8.0-dev.1
  (chantier (a)), la 0.8.0-dev.2 (chantier (b)) — des gestes de BUILD ;
  **la 0.8.0-rc.1 est SCELLÉE le 05/11/2026 (chantier M7-(c), Entrée 153 :
  le contrôle D146 adapté VERT [base réelle CONSTATÉE PAR TRACE
  0x555555556000 + 3 bases forcées distinctes] + le verrou croisé
  multi-profils AVANT l'édition + cristallisation 10/10 + conformité § 8.2
  7/7 [29 contrôles, la suite EXÉCUTANT la démonstration du patch] ; l'artefact
  INTACT sha ec343b4e… — le scellage est un fait de carte ; les TROIS gardes
  vivantes [re-scellage et reconstruction REFUSÉS, la re-vérification
  PRÉSERVE la balise]).**
- Contrôle D146 adapté : exécution full-ELF à la base réelle **sur l'exécuteur du
  jalon** (§ 10) avant tout scellage rc/final.

## 9. Suite de conformité (spec § 8.2) — déclinée

| # | Élément | Contrôle sur l'artefact du jalon |
|---|---|---|
| 1 | ISA et types | magie ELF64 LE, e_machine 0xF3, e_flags 0 ; instructions toutes à 4 o (refus d'un encodage 2 o = garde anti-C) |
| 2 | ABI d'appel | appels/retours conformes psABI ; AUCUNE zone rouge (frag-con) ; alignement sp 16 |
| 3 | Format | ET_DYN, trois segments R/RX/RW, PT_GNU_STACK sans X, W^X |
| 4 | Interface système | numéros asm-generic autorisés PAR BLOC (garde anti-table-x86) ; contrat ERRNOS |
| 5 | Patch à chaud | séquence scratch + `fence.i` DÉMONTRÉE en exécution, écriture alignée atomique, rollback vivant — **ACQUIS (05/11/2026, chantier M7-(c), Entrée 153 : le DÉMONSTRATEUR INVITÉ `riscv/demo` — la bascule pendant le trafic 1200 usages, apply/rollback ENTRE deux usages, transcription byte-exact 15 425 o, l'effet au geste même, les refus 1-4, le DEP SIGSEGV (4 290 o exacts), la falsification du démonstrateur, les bases forcées ; la correction tcp-07 D157 : `mv a2, t2` — le marshalling du prot oublié au port, nommé au premier apply, la pièce par QEMU_STRACE** |
| 6 | Notation | round-trip 100 % sur le corpus (assembleur maison + capstone juge) |
| 7 | Granularité et padding | adresses stables après patch (R7), NOP/ebreak constatés |

## 10. Exécution et terrain — la réserve instrumentale nommée

- **Constat labo (04/11/2026, LEVÉ au chantier M7-(a) le 05/11)** : aucun
  binaire `qemu-riscv64` dans le bac à sable — l'installation (qemu-user
  statique) était le prérequis du chantier (a) : **elle est FAITE et elle
  est une PROCÉDURE du dépôt** (`riscv/outils/installer_qemu.sh` :
  téléchargement + extraction locale du paquet Debian qemu-user SANS
  privilèges — le binaire est un instrument gitignoré sous `riscv/.tmp/`,
  la procédure est la pièce ; qemu-riscv64 10.0.13 statique, opérationnel,
  re-vérifié par le build avant tout usage).
- **L'exécuteur du jalon : qemu-riscv64 (émulation de processus, TCG)** — le noyau
  Linux et les syscalls sont RÉELS (qemu-user traduit les instructions et relaie les
  appels au noyau hôte) ; l'ISA est exécutée par l'émulateur, **pas par une fer
  RISC-V** : cette limite est une **réserve instrumentale nommée** (D149), consignée
  dans chaque verdict — le protocole ne la déguise jamais en exécution native.
- **Constat d'instrument NOMMÉ (05/11/2026, chantier M7-(a), D155)** : qemu
  10 ne randomise PAS l'image PIE invitée — la base par défaut est
  CONSTANTE (0x555555556000 au labo, CONSTATÉE sur 6 exécutions), et
  `-B` (guest_base) seul est SANS effet sur l'adresse d'image ET_DYN ;
  le levier du chargeur est `-R` (la fenêtre de réservation VA fixe où
  l'image vit) — **l'indifférence à la base se DÉMONTRÉE par bases
  forcées du CHARGEUR** (trois configurations VERTES à 0x2aaac000 /
  0xaaaac000 / 0x55556000 au geste même), jamais en feignant un ASLR
  émulé : la preuve ne dépend d'aucun aléa de l'instrument.
- Le terrain du jalon (machine du développeur) exécute le même artefact sous
  qemu-riscv64 (WSL2/VM Linux) — la parité inter-ISA se prouve par le MÊME oracle
  vert sur les TROIS profils et par le verrou croisé multi-profils (spec § 18-M7) ;
  l'export de continuité multi-profils de bout en bout (§ 6 du manuel : déchiffrer,
  vérifier signature, verrou croisé, régénérer l'oracle, reprendre) clôt le jalon.
- **ACQUIS (05/11/2026, chantier M7-(b), Entrée 152)** : l'oracle du CORPUS
  sous qemu — le rituel de parité 6/6 : les DEUX lignes octet pour octet
  (« TRIADE M1 : minilibc 21/21 OK\n » — LA PARITÉ § 8.3 PAR EXÉCUTION, le
  MÊME observable que l'instance Windows scellée et l'instance x86-64-linux,
  au terminateur du profil près) puis « corpus : autotest 21 vecteurs\n »,
  code 0 ; l'indifférence à la base par bases forcées du CHARGEUR (les trois
  configurations du chantier (a), VERTES sur le corpus) ; la falsification
  13 mutations 12/12 blocs rompus (zéro silence ; tcp-07 hors-chemin du
  rituel — son scénario complet est le chantier (c)).
- **ACQUIS (05/11/2026, chantier M7-(c), Entrée 153 — D157)** : LE JOURNAL DE
  L'EXÉCUTEUR EST UNE PIÈCE — QEMU_STRACE a nommé le marshalling oublié du
  port (`PROT_SEM` : un prot qui n'est dans AUCUN plan) ; le trace in_asm
  sert de TÉMOIN de la base réelle (le premier bloc traduit - e_entry) dans
  le contrôle D146 adapté (controle_base_reelle.py : base 0x555555556000 ×6,
  3 forçages distincts) ; les reproducers roulés à la main sont un marécage
  (l'isolement d'un défaut se mène SUR L'IMAGE DE LA FAMILLE — le builder) ;
  le mprotect invité fonctionne PARFAITEMENT sous qemu (RWX puis RX, D39
  tenu) — la réserve d'instrument qui aurait été nommée n'existait pas.
- **ACQUIS (05/11/2026, chantier M7-(d), Entrée 154 — D158)** : LE KIT
  TERRAIN DU JALON est ASSEMBLÉ, ÉPROUVÉ (extraction vierge + run au labo :
  VERT 16 PASS / 0 ÉCHEC — D153) et DÉPOSÉ au coffre /test (vague m7d :
  kit-m7d.zip + LISEZMOI) — il porte le SCELLÉ riscv/corpus (0.8.0-rc.1),
  le DÉMONSTRATEUR riscv/demo (f72001) et **l'INSTRUMENT EMBARQUÉ**
  qemu-riscv64 10.0.13 STATIQUE (md5 bae5a36f… consigné au TÉMOIN du run :
  aucun paquet, aucun réseau, aucun droit root — la réserve D149 NOMMÉE
  dans chaque verdict du scénario) ; le scénario PRÉ-ASSEMBLÉ rétablit le
  bit exécutable des images si l'extraction le perd (qemu-user L'EXIGE —
  « Exec format error » constaté, D158 : geste nommé, le chmod ne touche
  aucun octet de contenu) ; **L'EXPORT DE CONTINUITÉ MULTI-PROFILS** est
  VERT DE BOUT EN BOUT (riscv/export_continuite.py : conteneur TRIADE-EXP1
  chiffré + signé portant les couches I/B/C des TROIS profils — import
  AUTO-PORTANT aux cinq étapes § 8.2, la géométrie et les dérivations
  publiques AU MANIFESTE ; les rituels rejoués sur les octets TRANSPORTÉS) ;
  la clôture D143 du run m6d est FAITE au même geste (les pièces du run +
  le verdict du recoup labo à archives-preuves/preuves-run-m6d/) ; le run
  terrain du développeur (preuves-m7/) précède le scellage final 0.8.0.
