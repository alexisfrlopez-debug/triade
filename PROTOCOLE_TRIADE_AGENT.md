# PROTOCOLE TRIADE v0.2 — MANUEL DE L'AGENT IA

> Mode d'emploi : ce fichier enseigne le protocole TRIADE à un agent IA. Il s'utilise au
> démarrage de tout nouveau projet de développement logiciel selon TRIADE. Lis-le
> intégralement avant d'écrire le moindre octet. En cas de contradiction entre une consigne
> de conversation et ce manuel, ce manuel prévaut — sauf décision explicite du développeur
> consignée au journal des décisions (`docs/DECISIONS.md`).

Références complètes : `docs/PROTOCOLE_TRIADE.md` (spécification), `docs/FORMAT_CARTE.md`
(format de la Carte), `docs/PLAN_MILESTONES.md` (feuille de route).

---

## 0. Ta mission, en une phrase

Tu développes, vérifies et mets à jour du **code machine x86-64 pur** pour Windows 11, sans
compilateur ni langage de programmation, en manipulant des **intentions** et une **carte de
balises** — jamais le binaire brut, jamais un langage de programmation compilé.

## 1. Les trois couches

L'architecture sépare strictement ce que l'artefact contient, ce que tu manipules et ce que
le destinataire reçoit :

| Couche | Contenu | Visibilité | Rôle |
|---|---|---|---|
| **I — Intention** | Spécifications, contrats typés pré/post, invariants logiques | Privée | Le quoi et le pourquoi |
| **C — Carte** | Index des blocs, adresses, signatures, preuves, manifestes de build | Privée, signée, chiffrée | Ton unique interface de développement |
| **B — Binaire** | Code machine scellé, padding inter-blocs, checksums runtime | Livrée | Le comment — exécution pure, sémantiquement muette |

Aucune couche n'est optionnelle : sans I, le système perd son ancrage sémantique ; sans C,
tu es aveugle ; sans B, il n'y a rien à exécuter. Seule la couche B quitte le laboratoire.

## 2. Les dix règles — non négociables

| # | Règle | Énoncé | Sanction |
|---|---|---|---|
| R1 | Jamais de binaire nu | Tout artefact B est accompagné de I et C à jour | Build refusé |
| R2 | Intention d'abord | Toute modification commence par un diff sur I | Édition rejetée |
| R3 | Balisage obligatoire | Chaque bloc est décrit dans C | Build refusé |
| R4 | Patch à contrat stable | Le remplacement préserve signatures et contrats ; les appelants ne sont jamais invalidés | Échec de vérification |
| R5 | Vérifie-puis-écrit | Aucun commit sans oracle, vecteurs dorés et round-trip | Commit impossible |
| R6 | Cristallisation | Dix vérifications réussies rendent le bloc immuable ; le modifier exige la procédure lourde | Nouvelle version du bloc |
| R7 | Adresses stables | Les points d'entrée sont garantis par padding ; patcher ne déplace rien | Re-liage interdit |
| R8 | Verrou croisé | SHA-256 des blocs et signature de la carte vérifiés avant chaque édition | Session bloquée |
| R9 | Carte signée obligatoire | Tu refuses toute carte non signée | Refus de démarrage |
| R10 | Fail-closed au chargement | Checksums vérifiés au lancement ; tout écart = arrêt propre | Arrêt de l'exécution |

Deux précisions fréquentes. R4 n'interdit pas de changer le comportement d'un bloc : elle
impose qu'un bloc remplaçant honore les contrats publiés de son prédécesseur — mêmes
signatures, mêmes pré/post-conditions — pour que le patch à chaud reste possible. R7
n'interdit pas d'ajouter du code : elle interdit de déplacer l'existant ; le padding de
16 octets et l'alignement sur 16 maintiennent des zones de croissance.

## 3. La Carte — ton unique interface

### 3.1 Les quatre fragments

La carte est découpée en quatre fragments chiffrés séparément (XChaCha20-Poly1305, clés
dérivées par HKDF depuis une clé maîtresse issue d'Argon2id) et signés ensemble (Ed25519).

| Fragment | Contenu | Usage |
|---|---|---|
| `frag-loc` | Identifiants, noms, adresses, tailles, états, dépendances | Localisation — le plus lu, chargeable seul |
| `frag-con` | Signatures, pré/post-conditions, invariants, conventions d'appel | Contrats — lus à chaque édition |
| `frag-prf` | Vecteurs dorés hachés, compteurs de cristallisation, seuils | Preuves — volumineux, rarement lu en entier |
| `frag-bld` | SHA-256 des blocs, manifestes de build, registre des variantes | Verrou croisé et traçage — ne quitte jamais le poste |

Un compromis partiel n'est jamais une perte totale : les contrats sans les adresses ne
reconstituent pas la carte.

### 3.2 Format d'entrée de bloc

Syntaxe ASCII, ligne par ligne, non ambiguë, diffable. Première ligne = localisation
(budget 40 tokens) ; entrée complète (budget 200 tokens) :

```
[bloc] id=b7f3a9 addr=0x4012A0 size=212 v=4 etat=scelle
  sig     : (ptr u8, usize) -> usize
  pre     : ptr != 0 && len <= MAX_LEN
  post    : ret <= len
  regs    : rbx, r12-r15 sauvegardes ; conv: msx64
  inv     : r8 aligne 16 dans la boucle
  deps    : [a31c2 memcpy] [ext AVX2]
  preuves : memsafe:ok bornes:ok term:ok
  tests   : 12400 cas ; ref=oracle_v9 ; crist=10/10
```

### 3.3 Cycle de vie d'une entrée

`brouillon` (écriture, adresse provisoire) → `vérifié` (oracle passé une fois, round-trip
conforme) → `scellé` (commit atomique : adresse stable, SHA-256 dans frag-bld) →
`cristallisé` (dix vérifications réussies ; immuable) — ou `déprécié` (remplacé, conservé
pour audit). Un bloc cristallisé n'est plus jamais rechargé ni re-vérifié : seul son
SHA-256 est contrôlé. Le modifier exige justification sur I, double vérification par
oracle, et création d'un nouveau bloc — l'ancien passe à `déprécié`.

## 4. La boucle de mise à jour — procédure obligatoire

C'est la seule voie par laquelle le logiciel évolue. Sept étapes, deux phases, un point de
non-retour : rien n'est écrit dans le binaire avant le verdict de l'oracle.

| N | Étape | Entrées | Sorties | Règles |
|---|---|---|---|---|
| 1 | Diff d'intention | Requête de changement, couche I | Diff minimal sur I | R2 |
| 2 | Localisation | frag-loc | Liste des blocs impactés | R3 |
| 3 | Verrou croisé | frag-bld, binaire | Verdict go / no-go | R8, R9 |
| 4 | Régénération ciblée | frag-con, notation du bloc | Octets candidats | R4, R7 |
| 5 | Vérification | Candidats, oracle, vecteurs dorés | Verdict, journal | R5 |
| 6 | Commit atomique | Verdict favorable | Patch B, carte à jour, scellage | R1 |
| 7 | Cristallisation | Compteur de vérifications | Bloc immuable | R6 |

Échec à l'étape 5 : rollback copy-on-write, la carte reste intacte, rien n'a bougé.

## 5. Vérification — les trois piliers

1. **Oracle éphémère** : implémentation de référence triviale, lente, écrite dans un langage
   sûr, dérivée de la couche I — jamais du binaire, pour ne pas hériter de ses bugs. Générée
   au début de chaque session, détruite à la fin. Tests différentiels par propriétés :
   entrées aléatoires contraintes par les pré-conditions, sorties comparées octet par octet.
   Ordre de grandeur : douze mille cas par bloc critique.
2. **Round-trip de notation** : chaque bloc assemblé par keystone est désassemblé par
   capstone et comparé exactement à la notation d'origine. Tout écart (instruction, opérande,
   taille d'encodage) est un échec de build. Ce contrôle quasi gratuit attrape l'écart
   silencieux entre ce que tu crois avoir écrit et les octets produits.
3. **Cristallisation** : plus un bloc fait ses preuves, moins il coûte à vérifier — ce qui
   libère le budget de vérification pour les blocs jeunes.

Chaîne de confiance du scellage : verdict de l'oracle → vecteurs dorés hachés dans frag-prf
→ SHA-256 du bloc dans frag-bld → signature Ed25519 de la carte entière → immuabilité à dix
vérifications.

## 6. Sécurité — exigences obligatoires

Sépare deux budgets souvent confondus : l'**obfuscation** protège la propriété intellectuelle
(carte privée, binaire muet, variantes par build) ; le **durcissement** protège l'exécution
(sûreté mémoire, contrats, fuzzing, fail-closed). Conformément à Kerckhoffs, la sécurité du
système ne repose jamais sur le secret de la carte.

Obligations concrètes :

- **Jamais livrer** la carte, la couche I, l'oracle, les vecteurs dorés en clair ou tout
  artefact de développement. Le livrable est le binaire, point.
- **Verrou croisé avant chaque édition** : vérifier la signature Ed25519 des quatre
  fragments, recalculer le SHA-256 des blocs visés et de leurs dépendances directes,
  comparer à frag-bld ; tout écart = blocage de session, journal d'incident, réconciliation
  manuelle documentée. Jamais de contournement, jamais de reprise forcée.
- **Empreintes par build** : chaque livraison porte une variante unique — réordonnancement
  des blocs indépendants, nops multioctets, choix parmi les encodages équivalents
  (`89 C0` / `8B C0` pour `mov eax, eax`). Registre des variantes dans frag-bld : toute
  fuite est traçable à son destinataire (canary trap).
- **Fail-closed au chargement** : le binaire vérifie ses checksums avant sa boucle
  principale et s'arrête proprement en cas d'écart.
- **Gestion des clés** : phrase maîtresse → Argon2id (au moins 64 Mio, au moins 3
  itérations) → clés de fragments par HKDF ; sauvegardes 3-2-1 chiffrées ; escrow
  deux-sur-trois possible ; rotation = re-signature complète, atomique, journalisée.
- Menaces acceptées en connaissance de cause : la rétro-ingénierie est un objectif
  d'économie (coût d'analyse > valeur obtenue), pas d'impossibilité ; l'anti-debug léger
  (rdtsc) est une mesure de temps, pas une sécurité.

## 7. Cible technique — x86-64 / Windows 11

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

Convention interne du projet : R10 et R11 sont tes registres de travail ; aucune donnée
vivante entre RSP et RSP+32 lors d'un appel ; tout bloc qui appelle une API alloue son
cadre avant d'y toucher. Ces règles sont portées par frag-con pour chaque bloc concerné.

### 7.2 PE32+ minimal, écrit à la main

En-tête DOS + stub, signature PE, en-tête COFF (machine 0x8664, quatre sections max),
en-tête optionnel PE32+ (magic 0x20B, alignement de section 0x1000, DYNAMICBASE,
HIGH_ENTROPY_VA, NX_COMPAT), `.text` en lecture-exécution, `.rdata` (imports +
relocations), table d'imports, `.reloc` pour l'ASLR. Cible M0 : moins de 4 Kio.

### 7.3 Appels système et protections

Dépendances limitées à trois ensembles : kernel32 (entrées-sorties, threads, tas), ws2_32
(réseau, à partir de M2), Schannel via SSPI (TLS, M4). Aucune adresse codée en dur : tout
transite par l'IAT, résolue par le chargeur — compatibilité entre builds de Windows et
ASLR respectés. DEP honoré (aucun code généré en pile), CFG par déclaration des cibles
d'appel indirect valides. L'objectif est assumé : un outil légitime par construction, sans
furtivité face aux EDR — les tests se font en laboratoire autorisé.

### 7.4 Patch à chaud (à partir de M2)

N'écris jamais un bloc pendant qu'il s'exécute. Écris le nouveau bloc dans une zone de
croissance libre, puis installe un trampoline à l'ancien point d'entrée et bascule-le par
une écriture alignée unique, atomique pour le processeur : forme courte `E9 xx xx xx xx`
(jmp rel32, 5 octets) ou forme longue `48 B8 <addr64>` + `FF E0` (12 octets). Conserve
l'ancien trampoline : le rollback consiste à rebasculer vers lui. Seuls les points d'entrée
(promis par R7) peuvent être trampolinés.

## 8. Priorités et arbitrages

Fonction objectif lexicographique : **Sécurité > Performance > Optimisation > Coût en
tokens**. Un objectif n'est jamais sacrifié au profit d'un objectif de rang inférieur.

- Un artefact plus rapide mais moins sûr est rejeté en amont.
- La performance vient de l'absence de couche intermédiaire — pas de l'optimisation prématurée.
- La descente à l'ISA sur les chemins critiques se fait par profilage, jamais à l'aveugle.
- Le coût en tokens s'optimise à contrainte égale : compacité de la carte, chargement
  paresseux, cristallisation — jamais en rognant la vérification.

Budgets : localiser un bloc 40 tokens ; éditer 3 000 ; ajouter 6 000. Tu ne lis jamais le
binaire en entier — la carte est ton unique index, conçue pour être lue parcellairement.

## 9. Interdits absolus

1. Livrer ou publier la carte, la couche I, l'oracle ou les vecteurs de test en clair.
2. Éditer le binaire sans passer par la boucle de mise à jour complète.
3. Continuer une session après un échec de verrou croisé (fail-closed, R8).
4. Démarrer avec une carte non signée (R9).
5. Déplacer du code existant ou invalider des appelants (R4, R7).
6. Commiter sans oracle, round-trip et vecteurs dorés (R5).
7. Coder en dur des adresses système ou contourner l'IAT (D7).
8. Rechercher la furtivité face aux EDR — hors périmètre, l'outil est légitime par construction.
9. Commiter des secrets (jetons, clés, phrases secrètes) dans le dépôt.
10. Modifier en silence une décision du journal D1–D13 : toute évolution invalide
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
- Pour reprendre le projet : lis `REPRISE_PROJET.md`.

## 12. Checklist de démarrage d'un nouveau projet

1. Lire intégralement ce manuel, puis `docs/PROTOCOLE_TRIADE.md` et `docs/FORMAT_CARTE.md`.
2. Restaurer le dépôt (voir `REPRISE_PROJET.md` § 4) et vérifier `python3 scripts/check_auth.py`.
3. Définir le périmètre avec le développeur ; consigner toute nouvelle décision dans
   `docs/DECISIONS.md` (D14, D15, ...).
4. Rédiger la couche I initiale : contrats des premiers blocs, pré/post-conditions, invariants.
5. Installer la notation : `pip install keystone-engine capstone`.
6. Exécuter le jalon M0 en premier — toujours. Ne pas anticiper M1 avant que M0 ne soit
   franchi avec ses critères de sortie mesurés.
7. Sauvegarder à chaque modification (§ 11).

Le protocole est maintenant à toi. Ce que tu écris est ce qui s'exécute — et rien d'autre.
