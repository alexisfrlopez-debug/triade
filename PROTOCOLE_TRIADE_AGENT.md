# PROTOCOLE TRIADE v0.3 — MANUEL DE L'AGENT IA

> Mode d'emploi : ce fichier enseigne le protocole TRIADE à un agent IA. Il s'utilise au
> démarrage de tout nouveau projet de développement logiciel selon TRIADE. Lis-le
> intégralement avant d'écrire le moindre octet. En cas de contradiction entre une consigne
> de conversation et ce manuel, ce manuel prévaut — sauf décision explicite du développeur
> consignée au journal des décisions (`docs/DECISIONS.md`).

Références complètes : `docs/PROTOCOLE_TRIADE.md` (spécification), `docs/FORMAT_CARTE.md`
(format de la Carte), `docs/PLAN_MILESTONES.md` (feuille de route).

---

## 0. Ta mission, en une phrase

Tu développes, vérifies et mets à jour du **code machine natif pur** — pour le **profil de
cible** du projet, par défaut x86-64 / Windows 11 —, sans compilateur ni langage de
programmation, en manipulant des **intentions** et une **carte de balises** — jamais le
binaire brut, jamais un langage compilé. Le protocole est universel : tout ce qui dépend
de la plateforme est défini par un profil de cible, jamais codé en dur dans ta façon de
travailler.

## 1. Les trois couches

L'architecture sépare strictement ce que l'artefact contient, ce que tu manipules et ce que
le destinataire reçoit :

| Couche | Contenu | Visibilité | Rôle |
|---|---|---|---|
| **I — Intention** | Spécifications, contrats typés pré/post, invariants logiques | Privée | Le quoi et le pourquoi — **indépendante de la cible** |
| **C — Carte** | Index des blocs, profils, adresses, signatures, preuves, manifestes | Privée, signée, chiffrée | Ton unique interface de développement |
| **B — Binaire** | Code machine scellé, padding inter-blocs, checksums runtime | Livrée | Le comment — exécution pure, **un binaire par profil** |

Aucune couche n'est optionnelle : sans I, le système perd son ancrage sémantique ; sans C,
tu es aveugle ; sans B, il n'y a rien à exécuter. Seule la couche B quitte le laboratoire.
Un même contrat de I est instancié par autant de blocs machine que de profils supportés :
l'intention s'écrit une fois, les octets existent par plateforme.

## 2. Profils de cible — l'universalité

Le cœur du protocole (règles, boucle, vérification) est indépendant de la cible. Chaque
plateforme est un **profil** — identifiant `<isa>-<os>-<format>` — qui définit sept
éléments obligatoires :

1. l'ISA et la largeur de ses types (`usize`, alignements, boutisme) ;
2. l'ABI d'appel (registres de passage, volatilité, shadow space ou zone rouge) ;
3. le format d'exécutable et les protections à honorer (DEP/NX, ASLR/PIE, CFI/CFG) ;
4. l'interface système autorisée (IAT, syscalls, libc de la cible) ;
5. le mécanisme de patch à chaud natif (bascule atomique, invalidation du cache
   d'instructions) ;
6. le moteur de notation et son vérificateur de round-trip ;
7. la granularité des blocs et le padding des adresses stables.

Profils spécifiés à ce jour : `x86-64-win11-pe` (primaire — détaillé en § 7),
`x86-64-linux-elf64` (M6), `riscv64-linux-elf64` (M7) ; `aarch64-macos-macho` et
`wasm32-wasi` réservés. Travailler sur un profil nouveau exige sa fiche complète : les
sept éléments ci-dessus, écrits et vérifiés — jamais d'instanciation approximative. En cas
de doute sur un élément de profil, bloque et demande la fiche : un profil incomplet est un
refus de build, exactement comme une carte manquante.

## 3. Les dix règles — non négociables

| # | Règle | Énoncé | Sanction |
|---|---|---|---|
| R1 | Jamais de binaire nu | Tout artefact B est accompagné de I et C à jour | Build refusé |
| R2 | Intention d'abord | Toute modification commence par un diff sur I | Édition rejetée |
| R3 | Balisage obligatoire | Chaque bloc est décrit dans C | Build refusé |
| R4 | Patch à contrat stable | Le remplacement préserve signatures et contrats ; les appelants ne sont jamais invalidés | Échec de vérification |
| R5 | Vérifie-puis-écrit | Aucun commit sans oracle, vecteurs dorés et round-trip | Commit impossible |
| R6 | Cristallisation | Dix vérifications réussies rendent le bloc immuable ; le modifier exige la procédure lourde | Nouvelle version du bloc |
| R7 | Adresses stables | Les points d'entrée sont garantis par padding ; patcher ne déplace rien | Re-liage interdit |
| R8 | Verrou croisé | Empreintes des blocs et signature de la carte vérifiés avant chaque édition | Session bloquée |
| R9 | Carte signée obligatoire | Tu refuses toute carte non signée | Refus de démarrage |
| R10 | Fail-closed au chargement | Checksums vérifiés au lancement ; tout écart = arrêt propre | Arrêt de l'exécution |

Trois précisions fréquentes. R4 n'interdit pas de changer le comportement d'un bloc : elle
impose qu'un bloc remplaçant honore les contrats publiés de son prédécesseur — mêmes
signatures, mêmes pré/post-conditions — pour que le patch à chaud reste possible. R7
s'entend **par profil** : les adresses sont stables au sein du binaire de chaque profil.
R1, précisée par D16, interdit de livrer la carte **avec l'artefact ou à des tiers** — elle
ne t'interdit pas de produire, à la demande du développeur, un **export de continuité**
chiffré et signé (§ 6).

## 4. La Carte — ton unique interface

### 4.1 En-tête normalisé — lire la carte avant tout

Toute carte commence par un en-tête signé qui la rend autodescriptive :

```
[carte] version=0.3
  algo_hachage     : sha256
  algo_signature   : ed25519
  algo_chiffrement : xchacha20poly1305
  profils          : x86-64-win11-pe, x86-64-linux-elf64
  empreinte_racine : sha256:9f3c…e21a
```

Tu vérifies le verrou croisé **avec les algorithmes de l'en-tête**, jamais avec des
algorithmes supposés. La suite cryptographique est choisie par le développeur (défauts :
SHA-256, Ed25519, XChaCha20-Poly1305) dans des listes blanches — voir § 4.4.

### 4.2 Les quatre fragments

| Fragment | Contenu | Usage |
|---|---|---|
| `frag-loc` | Identifiants, profils, adresses, tailles, états, dépendances | Localisation — le plus lu, chargeable seul |
| `frag-con` | Signatures, pré/post-conditions, invariants, conventions d'appel | Contrats — lus à chaque édition |
| `frag-prf` | Vecteurs dorés hachés, compteurs de cristallisation, seuils | Preuves — volumineux, rarement lu en entier |
| `frag-bld` | Empreintes des blocs par profil, manifestes de build, registre des variantes | Verrou croisé et traçage — ne quitte jamais le poste |

Chaque fragment est chiffré séparément (AEAD de l'en-tête, clés HKDF dérivées d'Argon2id).
Un compromis partiel n'est jamais une perte totale.

### 4.3 Format d'entrée de bloc

Syntaxe ASCII, ligne par ligne. Première ligne = localisation (budget 40 tokens) ; entrée
complète (budget 200 tokens) :

```
[bloc] id=b7f3a9 cible=x86-64-win11-pe addr=0x4012A0 size=212 v=4 etat=scelle
  sig     : (ptr u8, usize) -> usize
  pre     : ptr != 0 && len <= MAX_LEN
  post    : ret <= len
  regs    : rbx, r12-r15 sauvegardes ; conv: msx64
  inv     : r8 aligne 16 dans la boucle
  deps    : [a31c2 memcpy] [ext AVX2]
  preuves : memsafe:ok bornes:ok term:ok
  tests   : 12400 cas ; ref=oracle_v9 ; crist=10/10
```

Cycle de vie : `brouillon` → `verifie` → `scelle` → `cristallise` (immuable, dix
vérifications) — ou `deprecie`. Un bloc cristallisé n'est plus jamais rechargé : seule son
empreinte est contrôlée. Le modifier exige justification sur I, double oracle, création
d'un nouveau bloc.

### 4.4 Suite cryptographique — paramétrable (D15)

Le développeur peut modifier les trois algorithmes, dans les limites des listes blanches :

| Paramètre | Défaut | Liste blanche |
|---|---|---|
| `algo_hachage` | sha256 | sha256, sha384, sha512, sha3-256, sha3-512, blake2b-256, blake2b-512, blake3 |
| `algo_signature` | ed25519 | ed25519, ed448, ecdsa-p256-rfc6979, ecdsa-p384-rfc6979 |
| `algo_chiffrement` | xchacha20poly1305 | xchacha20poly1305, chacha20poly1305, aes-256-gcm |

Exigences communes : hachage au moins 128 bits et résistant aux collisions ; signatures
déterministes ou hedged ; chiffrement authentifié (AEAD). Hors liste blanche = refus au
chargement — MD5 et SHA-1 sont irrecevables, la volonté du développeur s'exerce entre
algorithmes conformes, jamais contre la fonction objectif. Les empreintes sont préfixées
(`sha256:ab12…`). Un changement en cours de projet est un **re-cryptage** : opération
complète, atomique, journalisée, avec archivage de l'ancienne carte (voir
`docs/FORMAT_CARTE.md` § 9) — jamais un basculement silencieux.

## 5. La boucle de mise à jour — procédure obligatoire

La seule voie par laquelle le logiciel évolue. Sept étapes, un point de non-retour : rien
n'est écrit dans le binaire avant le verdict de l'oracle.

| N | Étape | Entrées | Sorties | Règles |
|---|---|---|---|---|
| 1 | Diff d'intention | Requête de changement, couche I | Diff minimal sur I | R2 |
| 2 | Localisation | frag-loc | Liste des blocs impactés | R3 |
| 3 | Verrou croisé | frag-bld, binaire | Verdict go / no-go | R8, R9 |
| 4 | Régénération ciblée | frag-con, notation du bloc | Octets candidats | R4, R7 |
| 5 | Vérification | Candidats, oracle, vecteurs dorés | Verdict, journal | R5 |
| 6 | Commit atomique | Verdict favorable | Patch B, carte à jour, scellage | R1 |
| 7 | Cristallisation | Compteur de vérifications | Bloc immuable | R6 |

Échec à l'étape 5 : rollback copy-on-write, la carte reste intacte. Une évolution peut
viser plusieurs profils : le diff I est unique, la régénération et la vérification se
répètent par profil — l'oracle, dérivé de I, est le même pour tous.

## 6. Vérification et sécurité — exigences obligatoires

Sépare deux budgets : l'**obfuscation** protège la propriété intellectuelle (carte privée,
binaire muet, variantes par build) ; le **durcissement** protège l'exécution (sûreté
mémoire, contrats, fuzzing, fail-closed). Conformément à Kerckhoffs, la sécurité du
système ne repose jamais sur le secret de la carte.

**L'oracle éphémère** : implémentation de référence triviale, lente, écrite dans un langage
sûr, dérivée de la couche I — jamais du binaire. Générée au début de chaque session,
détruite à la fin. Tests différentiels par propriétés : entrées aléatoires contraintes par
les pré-conditions, sorties comparées octet par octet — environ douze mille cas par bloc
critique. Le **round-trip de notation** : chaque bloc assemblé par le moteur du profil est
désassemblé et comparé exactement à la notation d'origine ; tout écart (instruction,
opérande, taille d'encodage) est un échec de build.

**Verrou croisé avant chaque édition** : vérifier la signature (algorithme de l'en-tête)
sur les quatre fragments, recalculer les empreintes des blocs visés et de leurs dépendances
directes, comparer à frag-bld ; tout écart = blocage de session, journal d'incident,
réconciliation manuelle documentée. Jamais de contournement.

**Export de continuité (D16)** — la seule forme sous laquelle l'état protocole quitte le
poste de développement :

- Contenu : couches I, B (tous les profils), C, et un manifeste autodescriptif (version,
  suite cryptographique, profils, empreinte racine). L'oracle n'est **jamais** exporté.
- Sécurité : chiffré intégralement (AEAD de l'en-tête, clé dérivée de la phrase maîtresse
  par Argon2id) et signé. Produis-le exclusivement chiffré et signé, à la demande du
  développeur.
- **Procédure d'import** (nouveau poste ou nouvel agent), cinq étapes, chaque échec est
  terminal : (1) déchiffrer avec la phrase maîtresse ; (2) vérifier la signature — refus
  si invalide ; (3) vérifier le verrou croisé avec l'algorithme de l'en-tête ; (4)
  régénérer l'oracle depuis I ; (5) reprendre normalement.
- Ne jamais interpréter un export non signé, ni accepter un contenu dont les empreintes
  divergent du manifeste.

Autres obligations : **empreintes par build** (variante unique par livraison et par profil
— réordonnancement, nops, encodages équivalents) ; **fail-closed au chargement** (le
binaire vérifie ses checksums avant sa boucle principale) ; **gestion des clés** (phrase
maîtresse → Argon2id ≥ 64 Mio, ≥ 3 itérations → HKDF par fragment ; sauvegardes 3-2-1
chiffrées ; escrow deux-sur-trois possible).

## 7. Le profil primaire — x86-64 / Windows 11

Le projet courant s'exécute sur le profil primaire. Tout autre profil se spécifie par sa
fiche (spécification § 10.4) ; les exigences communes (§ 2) y rappellent ce qui doit y
figurer.

### 7.1 ABI Microsoft x64 (msx64)

| Convention | Règle |
|---|---|
| Arguments | RCX, RDX, R8, R9, puis la pile — de droite à gauche |
| Retour | RAX (RDX pour 128 bits) |
| Shadow space | 32 octets réservés par l'appelant avant chaque CALL |
| Volatils | RAX, RCX, RDX, R8 à R11 — détruits par l'appelé |
| Non volatils | RBX, RBP, RDI, RSI, R12 à R15 — préservés par l'appelé |
| Flottants | XMM0–XMM5 volatils ; XMM6–XMM15 préservés |
| Alignement | RSP multiple de 16 au point d'appel |
| Zone rouge | **Aucune** — stocker sous RSP sans allocation est interdit |

Convention interne : R10 et R11 sont tes registres de travail ; aucune donnée vivante
entre RSP et RSP+32 lors d'un appel ; tout bloc qui appelle une API alloue son cadre
avant d'y toucher.

### 7.2 PE32+ minimal, écrit à la main

En-tête DOS + stub, signature PE, COFF (0x8664, quatre sections max), PE32+ (magic
0x20B, alignement 0x1000, DYNAMICBASE, HIGH_ENTROPY_VA, NX_COMPAT), `.text` RX, `.rdata`
(imports + relocations), `.reloc` pour l'ASLR. Cible M0 : moins de 4 Kio.

### 7.3 Appels via IAT et protections

kernel32 (entrées-sorties, threads, tas), ws2_32 (réseau, M2+), Schannel/SSPI (TLS, M4).
Aucune adresse en dur : tout transite par l'IAT. DEP, ASLR et CFG honorés par
construction. L'objectif est assumé : un outil légitime par construction, sans furtivité
face aux EDR — les tests se font en laboratoire autorisé.

### 7.4 Patch à chaud (profil x86-64)

N'écris jamais un bloc pendant qu'il s'exécute. Écris le nouveau bloc dans une zone de
croissance libre, puis installe un trampoline à l'ancien point d'entrée et bascule-le par
une écriture alignée unique, atomique : forme courte `E9 xx xx xx xx` (jmp rel32) ou forme
longue `48 B8 <addr64>` + `FF E0` (12 octets). Conserve l'ancien trampoline : le rollback
consiste à rebasculer vers lui. Seuls les points d'entrée (R7) peuvent être trampolinés.

### 7.5 Autres profils — ce qui change

| Élément | `x86-64-linux-elf64` (M6) | `riscv64-linux-elf64` (M7) |
|---|---|---|
| ABI | SysV : RDI RSI RDX RCX R8 R9 ; **zone rouge 128 o.** (le piège inverse de msx64) | psABI : a0-a7 |
| Format | ELF64 (PIE, RELRO, NX), écrit à la main | ELF64 (PIE, RELRO, NX) |
| Interface | syscalls + libc | syscalls + libc |
| Patch à chaud | identique x86-64 (trampoline rel32/absolu) | instructions de taille fixe : registre scratch + `fence.i` |

Sur SysV, la zone rouge existe : une fonction feuille peut stocker sous RSP — désapprends
le réflexe msx64, et porte la convention effective dans frag-con. Sur RISC-V, pas de
trampoline de 5 octets : la bascule passe par un registre scratch et une barrière
d'invalidation du cache d'instructions ; la séquence exacte et son atomicité sont
spécifiées par la fiche du profil.

## 8. Priorités et arbitrages

Fonction objectif lexicographique : **Sécurité > Performance > Optimisation > Coût en
tokens**. Un objectif n'est jamais sacrifié au profit d'un objectif de rang inférieur.

- Un artefact plus rapide mais moins sûr est rejeté en amont.
- La performance vient de l'absence de couche intermédiaire — pas de l'optimisation
  prématurée. C'est aussi pourquoi l'universalité passe par des profils, jamais par un
  bytecode portable : une couche d'abstraction logicielle trahirait la fonction objectif.
- La descente à l'ISA sur les chemins critiques se fait par profilage, jamais à l'aveugle.
- Le coût en tokens s'optimise à contrainte égale : compacité de la carte, chargement
  paresseux, cristallisation — jamais en rognant la vérification.

Budgets : localiser un bloc 40 tokens ; éditer 3 000 ; ajouter 3 000–6 000 ; instancier
un profil nouveau pour un contrat existant 6 000 par bloc. Tu ne lis jamais le binaire en
entier — la carte est ton unique index.

## 9. Interdits absolus

1. Livrer ou publier **en clair** la carte, la couche I ou les vecteurs de test — avec
   l'artefact ou à des tiers. (L'export de continuité chiffré et signé est l'unique
   exception, réservée au développeur.)
2. Produire un export de continuité non chiffré ou non signé.
3. Reprendre un projet depuis un export sans avoir vérifié signature puis verrou croisé.
4. Éditer le binaire sans passer par la boucle de mise à jour complète.
5. Continuer une session après un échec de verrou croisé (fail-closed, R8).
6. Démarrer avec une carte non signée (R9) ou hors listes blanches cryptographiques.
7. Déplacer du code existant ou invalider des appelants (R4, R7).
8. Commiter sans oracle, round-trip et vecteurs dorés (R5).
9. Coder en dur des adresses système ou contourner l'interface du profil (IAT, syscalls).
10. Rechercher la furtivité face aux EDR — hors périmètre, l'outil est légitime par
    construction.
11. Commiter des secrets (jetons, clés, phrases secrètes) dans le dépôt.
12. Modifier en silence une décision du journal D1–D16 : toute évolution invalide
    explicitement ce qu'elle remplace.

## 10. Jalons — vue condensée

| Jalon | Objectif | Critère de sortie majeur |
|---|---|---|
| M0 | Prouver la chaîne artefact | hello.exe < 4 Kio sur Windows 11, round-trip 100 %, carte v0 signée |
| M1 | Blocs réutilisables | Mini-libc scellée, oracle 100 %, première cristallisation, adresses stables |
| M2 | Patch à chaud | Bascule du bloc écho en exécution, sans interruption, rollback démontré |
| M3 | Entrées non fiables | Un million de requêtes fuzzées sans crash ; proxy transparent pour curl |
| M4 | Tunnel chiffré | HTTPS en transit via Schannel ; échec propre sur certificat invalide |
| M5 | L'outil complet | Interception en VM isolée ; patch à chaud du journal ; empreintes par build |
| M6 | Portabilité inter-OS | Profil `x86-64-linux-elf64` : diff nul sur I, carte multi-profils, même oracle |
| M7 | Portabilité inter-ISA | Profil `riscv64-linux-elf64` : round-trip, patch `fence.i`, export multi-profils |

Détail complet, livrables et indicateurs : `docs/PLAN_MILESTONES.md`.

## 11. Infrastructure du projet — sauvegarde et continuité

Le projet vit dans un dépôt git (source de vérité), sauvegardé sur Google Drive et miroité
sur GitHub privé. Exigences qui te sont propres :

- **Après chaque modification** : `bash scripts/sync_backup.sh "description courte"` —
  commit, synchro Drive (fichiers + bundle d'historique), push GitHub. C'est la règle D13.
- Le dossier `.gdrive/` contient les jetons : tu ne le lis pas, ne le commites pas, ne le
  synchronises pas, ne l'affiches jamais.
- Le hook `post-commit` déclenche une synchro Drive à chaque commit ; s'il est absent,
  `sync_backup.sh` le réinstalle depuis `git-hooks/`.
- Après toute session, consigne ton travail dans le journal de travail du projet.
- Pour reprendre le projet : lis `REPRISE_PROJET.md` — ou, si le développeur te fournit un
  export de continuité, suis la procédure d'import du § 6.

## 12. Checklist de démarrage d'un nouveau projet

1. Lire intégralement ce manuel, puis `docs/PROTOCOLE_TRIADE.md` et `docs/FORMAT_CARTE.md`.
2. Restaurer l'état du projet : depuis le dépôt (`REPRISE_PROJET.md` § 4) ou depuis un
   export de continuité (procédure d'import, § 6). Vérifier
   `python3 scripts/check_auth.py` si l'infrastructure est utilisée.
3. Lire l'en-tête de la carte : version du protocole, suite cryptographique, profils
   actifs. Vérifier la signature et le verrou croisé avant toute opération.
4. Définir le périmètre avec le développeur ; consigner toute nouvelle décision dans
   `docs/DECISIONS.md` (D17, D18, ...).
5. Rédiger la couche I initiale : contrats des premiers blocs, pré/post-conditions,
   invariants — indépendants de la cible.
6. Installer la notation du profil (par défaut : `pip install keystone-engine capstone`).
7. Exécuter le jalon M0 en premier — toujours, sur le profil primaire. Ne pas anticiper
   M1 avant que M0 ne soit franchi avec ses critères de sortie mesurés.
8. Sauvegarder à chaque modification (§ 11).

Le protocole est maintenant à toi. Ce que tu écris est ce qui s'exécute — et rien d'autre.
