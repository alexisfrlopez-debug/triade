# FICHE DE PROFIL — `x86-64-linux-elf64` (jalon M6, universalité inter-OS)

> Profil de cible au sens de la spécification § 16 : les sept éléments constitutifs
> plus le huitième livrable v0.4.0 (politique anti-rollback et de vérification au
> chargement), chacun **constatable** — jamais déclaré. Fondations : D14 (universalité),
> D34 (échelle d'auto-hébergement — le hachoir `m6/` et le sceau `m7/` vivent déjà sur
> ce profil), D149 (ouverture du programme M6/M7). La fiche distingue l'**ACQUIS**
> (prouvé au labo par la lignée auto-hôte) de l'**À PRODUIRE PAR LE JALON** — le jalon
> M6 porte la parité du patrimoine des jalons Windows (M0–M5) sur ce profil, pas la
> re-création de la chaîne.

**Identifiant** : `x86-64-linux-elf64` · **ISA** : x86-64 (AMD64) · **OS** : Linux
(noyau ≥ 5.x, page 4 Kio) · **Format** : ELF64 petit-boutiste · **Statut** : vivant à
l'état auto-hôte (échelons 1 et 2 de D34) ; jalon M6 ouvert le 04/11/2026 (D149).

---

## 1. ISA et types

| Propriété | Valeur | Constat |
|---|---|---|
| Largeur native | 64 bits ; `usize`/pointeurs = 8 octets | hachoir `m6/` (D34), identique au primaire |
| Boutisme | petit-boutiste (EI_DATA = 1) | `m6/build_ah.py` `e_ident` |
| Alignements | naturels : 1/2/4/8/16 octets ; qword aligné 8 | héritage m0–m5 inchangé |
| Arithmétique | entière, complément à deux ; flottants hors corpus M6 | couche I du corpus (minilibc) |
| Page mémoire | 4 096 octets (0x1000) — frontière de `mprotect` | noyau Linux |

## 2. ABI d'appel — System V AMD64

| Convention | Règle | Différence avec le primaire msx64 |
|---|---|---|
| Arguments | RDI, RSI, RDX, RCX, R8, R9 puis la pile — **de gauche à droite** | ordre ET registres différents (RCX RDX R8 R9, droite à gauche) |
| Retour | RAX (RDX:RAX pour 128 bits) | identique |
| **Zone rouge** | **128 octets sous RSP, permise aux fonctions feuilles** | **le piège inverse de msx64** (spec § 16.2) : ce qui était interdit redevient permis |
| Shadow space | **aucun** | l'inverse du primaire (32 o obligatoires) |
| Volatils | RAX, RCX, RDX, RSI, RDI, R8–R11 | RSI/RDI deviennent volatils (non volatils en msx64) |
| Non volatils | RBX, RBP, R12–R15 (+ RSP) | identiques |
| XMM | XMM0–XMM15 **tous volatils** | msx64 préserve XMM6–XMM15 |
| Alignement | RSP multiple de 16 au point d'appel (≡ 8 mod 16 à l'entrée du bloc) | identique en pratique |
| Nettoyage pile | par l'appelant | identique |

Règle interne du projet (portée) : R10 et R11 restent les registres de travail internes
— tous deux volatils en SysV comme en msx64. La **convention effective de chaque bloc
vit dans frag-con** (spec § 8.3-4) : la zone rouge, permise par l'ABI, reste interdite
à tout bloc qui appelle (elle est détruite par l'instruction `call`) — le réflexe msx64
est donc désappris sélectivement, jamais globalement.

## 3. Format d'exécutable — ELF64 durci

- **Magie** : `\x7fELF`, EI_CLASS = 2 (64 bits), EI_DATA = 1 (LSB), EI_VERSION = 1,
  EI_OSABI = 0 (SysV) — l'artefact est statique, sans `PT_INTERP`.
- **e_machine** = `0x3E` (EM_X86_64) ; e_version = 1.
- **ACQUIS (hachoir/sceau)** : ET_EXEC à base fixe, en-têtes écrits à la main
  (ehdr 64 o + 2 phdr 56 o, PT_LOAD RX avec RVA == offset fichier, PT_LOAD RW `.bss`
  pur) — `m6/build_ah.py` `composer_elf()`, artefact exécuté nativement au labo.
- **ACQUIS PAR LE CHANTIER M6-(a) (04/11/2026, `unix/` — la sonde, balise
  0.7.0-dev.1, D149/D150)** : le durcissement est DÉMONTRÉ en exécution —
  1. **ET_DYN (PIE)** — l'image se charge à une **base aléatoire** (ASLR
     noyau), `e_entry` relatif à la base (RVA 0x1140) ; **CONSTATÉ** : 6
     bases distinctes sur 6 exécutions (alignées 0x1000, >= 0x10000),
     recoupées sous `setarch -R` (ADDR_NO_RANDOMIZE : même base deux fois —
     la base vient du noyau, pas du programme) et par `readelf` indépendant ;
     la sonde calcule sa propre base (`lea rip` sur le témoin `.rodata`,
     lien-temps soustrait) et l'émet en tête de sortie ;
  2. **séparation R/RX/RW en trois segments** : table ERRNOS + HEXCHARS +
     messages dans un PT_LOAD R distinct, code RX, `.bss` pur RW (filesz 0) ;
  3. **PT_GNU_STACK** (`0x6474e551`) à drapeaux RW **sans X** — NX explicite ;
  4. pas de section exécutable inscriptible (W^X), **vérifié depuis les phdr
     par le build** (`unix/build_m6.py` `valider_elf()` relit son image).
- L'écart acquis → jalon est **nommé** : l'ELF minimal auto-hôte (ET_EXEC,
  base fixe) reste VALIDE pour sa lignée ; l'artefact du jalon exige l'ELF
  durci — la sonde `unix/` le porte, **le corpus du chantier (b) L'A HÉRITÉ
  (04/11/2026, Entrée 146 : `unix/corpus` 12 288 o, ET_DYN/PIE, 3 segments
  R/RX/RW, PT_GNU_STACK sans X — `readelf` recoupé)**.

## 4. Interface système — syscalls directs

- **Aucune IAT, aucune libc au jalon** : l'interface est l'appel système direct
  (`syscall`, 0x0F 0x05), registres : RAX = numéro, RDI RSI RDX **R10** R8 R9 les
  arguments (le 4e passe par R10 — RCX est détruit par l'instruction), RAX le retour,
  RCX/R11 clobbered.
- **Contrat d'erreurs** : RAX ∈ [0, 4095] = succès ; RAX ∈ [−4095, −1] = échec avec
  −errno — **fail-closed** : tout errno inattendu est un arrêt propre nommé (le modèle
  HRESULTS du primaire a son miroir : table ERRNOS du jalon, succès exact + continuations
  nommées + VERDICT_FATAL).
- **Numéros autorisés PAR BLOC** (le garde auto-hôte existant, `m6/build_ah.py` I1) —
  table du jalon : `read` = 0, `write` = 1, `mmap` = 9, `mprotect` = 10, `exit` = 60,
  `exit_group` = 231 — chaque numéro motivé par un bloc du corpus, tout numéro
  non motivé est un refus de build.
- Le couplage le plus riche du jalon : `mprotect` (rendre une plage de code
  accessible en écriture) — la contrepartie exacte de VirtualProtect au primaire.

## 5. Patch à chaud

- **Bascule** : identique x86-64 — trampoline court `E9 rel32` + trois `NOP`
  (**un mot de 8 octets aligné, publication atomique**) ou forme longue `48 B8 <addr64>`
  + `FF E0` (12 octets, publiée seulement par `LOCK CMPXCHG16B` dans un emplacement
  16 octets aligné) ; ancien trampoline conservé pour le rollback (manuel § 7.4
  inchangé). LA CORRECTION D253 : « écriture alignée unique atomique » ne vaut QUE
  jusqu'à 8 octets naturels (Intel SDM vol. 3 § 8.1.1).
- **Changement de protection** : `mprotect(10)` — adresse alignée page, drapeaux
  PROT_READ|PROT_EXEC ↔ +PROT_WRITE ; jamais une page laissée RWX après le geste.
- **Invalidation du cache d'instructions** — cohérence I/D matérielle sur x86-64
  (Intel SDM vol. 3 § 8.1.3) : aucune barrière n'est requise pour le cœur qui écrit ;
  `__builtin___clear_cache()` (Linux) / `FlushInstructionCache()` (Windows) sont
  appelés sans condition, par portabilité et pour la même raison qui les rend
  nécessaires ailleurs. Réserve nommée (D253) : pour du code CROSS-MODIFIANT — un
  autre cœur exécutant la zone — le SDM EXIGE une synchronisation explicite de l'autre
  processeur (protocole drapeau/sémaphore, IPI) ; TRIADE la fournit par le RENDEZ-VOUS
  de quiescence du § 7.1.1, jamais par l'atomicité seule. Écart documenté avec RISC-V
  (`fence.i` + synchronisation des harts, fiche `riscv64`).
- **ACQUIS PAR LE CHANTIER M6-(d) (05/11/2026, Entrée 148)** : la démonstration
  en exécution est LIVRÉE — `unix/demo_patch.py`, VERT sur pièces sur l'artefact
  scellé 0.7.0-rc.1 relu (sha dd14195c…, le fichier jamais touché : le patch
  vit en cartographie privée) : la boucle d'écriture basculée ENTRE DEUX
  USAGES (1 200 lignes, apply entre 400/401, rollback entre 800/801 — tcp-07:R4
  V5), le journal COHÉRENT octet pour octet (aucune ligne déchirée, aucun
  mélange de formats), la bascule sous CONCURRENCE RÉELLE (le qword posé
  pendant qu'un fil ouvrier journalise — 5 300+ lignes entières, les DEUX
  formats dans SON trafic, Q3), le retour à l'état image et la zéro
  régression ; la suite § 9 EXÉCUTE la démonstration à chaque passage
  (l'élément 5 est devenu un contrôle RÉEL) — le chantier M5-(c) reporté est
  REFERMÉ au labo ; le run terrain (kit m6d au coffre /test) juge le
  scellage final.

## 6. Moteur de notation et round-trip

- **ACQUIS** : keystone 0.9.2 (`KS_ARCH_X86`, `KS_MODE_64`) — **le même moteur que le
  profil primaire** (constat labo 04/11 : `mov rax, rdi` → `48 89 F8`) ; capstone 5.0.7
  (`CS_ARCH_X86`, `CS_MODE_64`) pour le désassemblage.
- **Round-trip** : le WYSIWYG octets du projet (keystone → octets → capstone → keystone,
  tout écart = échec de build) s'applique tel quel — la chaîne vit déjà à
  `m6/build_ah.py` étape 2.
- Le profil n'exige AUCUN moteur nouveau : c'est précisément la thèse de M6 à ISA
  constante (seuls l'ABI, le format et l'interface changent).

## 7. Granularité des blocs et adresses stables

- **ACQUIS** : le modèle D8 (slots, padding ≥ 16, NOP intra-slot, réserves `int3`,
  adresses stables R7) est instancié par `m6/layout.py` (RX 0x3000 + RW, zones
  réservées, chevauchement gardé).
- **ACQUIS PAR LE CHANTIER M6-(b) (04/11/2026, Entrée 146)** : le layout du
  corpus (`unix/layout.py`, balise 0.7.0-dev.2, convention de dossiers D149)
  reprend le modèle — slots et adresses stables **par profil** (spec § 3 R7) :
  13 blocs à slots stables (série f61xxxx), padding/réserves `int3`, la table
  de correspondance bloc ↔ slot vit au frag-loc de la carte génération 1
  (`unix/carte-corpus/`).

## 8. Politique anti-rollback et vérification au chargement (R10 décliné)

- **Porte R10** : au lancement — avant le chemin d'exécution — vérification des
  checksums des blocs scellés, monotonie de version (R_VERSION ≥ plancher),
  conformité minimale de l'environnement au profil ; tout écart = arrêt propre
  immédiat, fail-closed explicite (le modèle m5/m4 transposé : mêmes qwords de
  garde, image ELF).
- **Registre des versions acceptées** : LICENSE anti-rollback amendé à chaque scellage
  (modèle D147) ; plancher posé à `0.7.0-dev.1`, balise du jalon M6 = **`0.7.0` SCELLÉE**
  (rc.1 au chantier (c) ; la FINALE posée le 05/11/2026 sur run terrain WSL2 vert
  recoupé sur pièces — Entrée 149/D154).
- **ACQUIS PAR LE CHANTIER M6-(c) (05/11/2026, Entrée 147)** : le scellage
  `0.7.0-rc.1` est POSÉ avec le contrôle D146 adapté EXÉCUTÉ AU SCELLAGE
  même (modèle D147 — `unix/controle_base_reelle.py` : 6 bases noyau
  DISTINCTES constatées par témoin ptrace/maps, ADDR_NO_RANDOMIZE recoupé,
  le mutant « RVA nu » mort nommé — la classe exacte du crash e3) ; les
  gardes sont VIVANTES sur pièces (re-scellage REFUSÉ, reconstruction
  REFUSÉE, la balise scellée SURVIT à la re-vérification) ; l'artefact
  est INTACT (sha dd14195c… — le scellage est un fait de carte) ; le
  registre des versions acceptées vit au code (`BALISES_LIGNEE`, plancher
  `0.7.0-dev.1`).
- **ACQUIS PAR LE CHANTIER M6-(d), LA FINALE (05/11/2026, Entrée 149)** : la
  finale `0.7.0` est SCELLÉE sur le run terrain recoupé VERT — le kit m6d
  exécuté par la machine du développeur (WSL2, noyau
  `6.18.54.1-microsoft-standard-WSL2`, UN AUTRE noyau que celui du labo,
  ASLR complet `randomize_va_space=2` ; 16/16 constats PASS ; le recoup
  labo 22/22 sur pièces croisées — D154) : `--sceller-final` a exécuté la
  même chaîne que le rc (D146 adapté + cristallisation 10/10 + conformité
  7/7 — la suite exécutant la démonstration M5-(c)) au geste même, la
  bascule rc.1 → 0.7.0 dans frag-bld (occurrence unique assertée, le
  re-scellage vérifié en mémoire avant l'unique écriture), l'artefact
  INTACT (sha dd14195c… — le scellage est un fait de carte) ; les gardes
  VIVANTES constatées : re-scellage REFUSÉ, reconstruction REFUSÉE, la
  balise PRÉSERVÉE par la re-vérification.
- Le scellage du jalon (rc et finale) exécute le **contrôle D146 adapté** : aucune
  balise sans exécution **full-ELF à la base réelle** — au labo l'image PIE se charge
  par le noyau à une base aléatoire authentique : un pointeur nu ou un RVA mal
  relocalisé y meurt exactement comme sur le terrain (la leçon e3/D146 s'applique
  au profil Linux par construction, l'émulation à base fixe restant interdite comme
  témoin unique).

## 9. Suite de conformité (spec § 8.2) — déclinée

| # | Élément | Contrôle sur l'artefact du jalon |
|---|---|---|
| 1 | ISA et types | magie ELF64 LE, e_machine 0x3E ; sections RX décodables 64 bits sans reste ; qwords IAT→sans objet (syscalls) |
| 2 | ABI d'appel | appels et retours conformes SysV ; volatilité ; zone rouge absente des blocs appelants (frag-con) ; alignement 16 aux points d'appel |
| 3 | Format | ET_DYN constaté, trois segments R/RX/RW, PT_GNU_STACK sans X (NX), W^X vérifié depuis les phdr |
| 4 | Interface système | numéros de syscall autorisés PAR BLOC ; contrat d'erreurs ERRNOS (succès exact, continuations nommées, VERDICT_FATAL) |
| 5 | Patch à chaud | mprotect + trampoline + publication atomique d'un mot de 8 o. démontrés EN EXÉCUTION, rollback vivant |
| 6 | Notation | round-trip 100 % sur le corpus du jalon (keystone/capstone x86-64) |
| 7 | Granularité et padding | adresses stables après patch (R7), slots et réserves constatés |

La suite s'exécute à chaque cristallisation rc et finale (spec § 9) — modèle
`m5/conformite_profil.py`, portée à `unix/conformite_profil.py`. **ACQUIS PAR
LE CHANTIER M6-(c) (05/11/2026, Entrée 147) : la suite est LIVRÉE, EXÉCUTÉE
VERTE 7/7 (37 contrôles PASS, sortie `unix/conformite.txt`) au scellage
`0.7.0-rc.1` même — les SEPT éléments constatés depuis l'artefact relu,
jamais déclarés ; le diff nul y est REJOUÉ à chaque passage (une garde qui
vit, pas un souvenir du chantier (b)). ACQUIS PAR LE CHANTIER M6-(d)
(05/11/2026, Entrée 148) : l'élément 5 porte désormais LA BASCULE PENDANT LE
TRAFIC comme contrôle RÉEL — la suite exécute `unix/demo_patch.py` (V5, Q3,
cohérence octet pour octet, zéro régression) et exige son vert : le scellage
final re-prouvera le critère M5-(c) à chaque passage.**

## 10. Terrain — le constat qui resserre la frontière labo/terrain

Le bac à sable du labo **EST une machine Linux x86-64 réelle** : l'oracle
différentiel du jalon s'exécute NATIVEMENT (mmap RX + appel direct des blocs —
déjà le modèle auto-hôte, `m6/build_ah.py` étape 5), plus fort que l'émulation
full-PE du primaire. La validation terrain demeure exigée sur une machine
DISTINCTE du labo (D149 : WSL2 recommandé — noyau Linux complet sur la machine
Windows 11 du développeur — ou VM Linux isolée dans la lignée des runs e*) : c'est
la preuve de portabilité réelle (noyau, chargeur et libc éventuels différents),
les preuves rapportées au coffre `/test` par la boucle d'évidence (§ 8.4, D99).

**ACQUIS PAR LE CHANTIER M6-(d) (05/11/2026, Entrée 148) : le kit terrain
est LIVRÉ AU COFFRE** — `/test` vit à la vague m6d (kit-m6d.zip +
LISEZMOI-m6d.txt + preuves-m6/, la vague e4 consommée archivée D143) :
l'artefact scellé 0.7.0-rc.1 + le scénario AUTONOME (python3 + ctypes
seulement — la cartouche d'appel PRÉ-ASSEMBLÉE au labo, octets embarqués
sha256 assertés, relogée au terrain par UN fixup imm64 ; recoupée contre
l'instrument vivant de l'oracle octet pour octet) + le LISEZMOI ; le kit
EXACT est ÉPROUVÉ au labo PAR EXTRACTION VIERGE + RUN (16/16 constats
PASS — D153 : un livrable ne se dépose que s'il est vert à l'extraction,
jamais par confiance en sa construction). Le scénario rejoue le geste
complet sur la machine du développeur : le rituel ×3 à l'ASLR du noyau
(+ base figée si setarch), la bascule pendant le trafic (V5), la
concurrence réelle (Q3), le refus EACCES PAR LE NOYAU de la machine
(cartographie partagée lecture seule — aucun shim), la zéro régression
(sha re-relu + rituel rejoué) ; les pièces naissent dans preuves-m6/
(temoin + journal + VERDICT post-mortem). **ACQUIS (05/11/2026, Entrée 149) :
LE RUN EST VENU ET VERT — LA FINALE `0.7.0` SCELLÉE, LE JALON M6 FRANCHI.**
La machine du développeur (WSL2 — la recommandation D149 suivie ; le premier
geste, lancé sous Windows natif, était mort NOMMÉ AVANT T0 : `libc.so.6`
introuvable — le fail-closed tient hors terrain, D154 : LE TERRAIN D'UN KIT
FAIT PARTIE DE SON CONTRAT) a rendu son verdict **VERT 16/16** sur le noyau
`6.18.54.1-microsoft-standard-WSL2` — UN AUTRE noyau que celui du
laboratoire, l'ASLR complet constaté (`randomize_va_space=2`), le scellé
relu `dd14195c…` avant tout geste ; les trois pièces renvoyées au coffre
`/test/preuves-m6/`, le RECOUP labo VERT 22/22 sur pièces croisées
(`scripts/recouper_run_m6d.py` — D154 : le verdict du labo se rend sur
pièces croisées, jamais sur console), et la finale `0.7.0` scellée au geste
même — **la portabilité inter-OS est une propriété démontrée** : le MÊME
corpus, la MÊME couche I, deux systèmes d'exploitation, deux noyaux
constatés, le diff nul mesuré et rejoué.
