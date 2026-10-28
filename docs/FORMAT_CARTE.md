# FORMAT DE LA CARTE — Couche C, spécification détaillée

> Ce document détaille le format de la carte TRIADE : en-tête normalisé, fragments, format
> d'entrée de bloc, procédure du verrou croisé, cycle de vie, budgets, export de continuité
> et migration cryptographique. La carte est le cœur opérationnel du protocole : elle rend
> le binaire navigable pour l'agent, porte les preuves et concentre la valeur intellectuelle
> du projet. Mis à jour pour la v0.4.0 : champ de traçabilité `spec=` dans l'entrée de bloc
> (spécification § 4.2), norme de fragmentation, audit de traçabilité et tableau de bord.
> Mis à jour pour la v0.5.1 (D75) : § 11 — le coffre-fort des phrases maîtresses, conteneur
> chiffré TRIADE-CF1.

## 1. Contraintes de conception

Trois contraintes tirées de la fonction objectif structurent le format : **compacité**
(coût en tokens — chapitre 9 de la spécification), **intégrité** (verrou croisé D5) et
**résilience** face à la compromission (sharding et chiffrement D4). La v0.3 en ajoute une
quatrième : **autodescription** — la carte porte elle-même sa version, sa suite
cryptographique et ses profils actifs, de sorte qu'aucun agent n'ait besoin de connaissance
extérieure pour la vérifier (D15, D16). Chaque contrainte se traduit par un mécanisme
précis : syntaxe ASCII ligne-par-ligne à budgets serrés, signature de l'ensemble,
chiffrement séparé des fragments, en-tête normalisé.

## 2. Les quatre fragments

| Fragment | Contenu | Raison d'être de la séparation |
|---|---|---|
| `frag-loc` | Identifiants, profils, adresses, tailles, états, dépendances | Localisation : le plus lu, le moins sensible — peut être chargé seul |
| `frag-con` | Signatures, pré/post-conditions, invariants, conventions d'appel | Contrats : diffés à chaque changement (R2), lus à chaque édition |
| `frag-prf` | Vecteurs dorés hachés, compteurs de cristallisation, seuils | Preuves : volumineux, rarement lu en entier après cristallisation |
| `frag-bld` | Empreintes des blocs par profil, manifestes de build, registre des variantes | Verrou croisé et traçage (D5, D6) — ne quitte jamais le poste de développement |

Chaque fragment est chiffré avec sa propre clé dérivée de la clé maîtresse (AEAD selon
l'algorithme de l'en-tête, nonce aléatoire de 192 bits pour XChaCha20). Un compromis
partiel — la fuite d'un fragment isolé — n'est jamais une perte totale : les contrats sans
les adresses, ou les preuves sans les contrats, ne reconstituent pas la carte.

**Norme de fragmentation (v0.4.0, spécification § 12).** Aucune opération de la boucle de
mise à jour n'exige la lecture de plus d'un fragment ; aucune opération n'exige la lecture
intégrale du binaire — la carte est l'unique index, le balayage est interdit (localisation
par intention, spécification § 7). L'audit complet — carte entière déchiffrée — est une
opération exceptionnelle, non budgétée et journalisée.

## 3. Suite cryptographique — paramètres et en-tête

### 3.1 Paramètres modifiables (D15)

La suite cryptographique est paramétrable par le développeur et consignée dans l'en-tête
de la carte. Trois paramètres, chacun avec sa valeur par défaut et sa liste blanche :

| Paramètre | Défaut | Liste blanche | Exigences communes |
|---|---|---|---|
| `algo_hachage` | `sha256` | `sha256`, `sha384`, `sha512`, `sha3-256`, `sha3-512`, `blake2b-256`, `blake2b-512`, `blake3` | Au moins 128 bits de sécurité ; résistance à la collision |
| `algo_signature` | `ed25519` | `ed25519`, `ed448`, `ecdsa-p256-rfc6979`, `ecdsa-p384-rfc6979` | Signatures déterministes ou randomisation hedged |
| `algo_chiffrement` | `xchacha20poly1305` | `xchacha20poly1305`, `chacha20poly1305`, `aes-256-gcm` | Authentifié (AEAD) uniquement |

Tout algorithme hors liste blanche est refusé au chargement de la carte. La liste est un
seuil, pas une contrainte de goût : MD5, SHA-1 et toute fonction cassée ou sous-dimensionnée
sont irrecevables, car un affaiblissement choisi casserait le verrou croisé pour tous les
agents qui suivraient — contraire à la fonction objectif. L'ajout d'un algorithme à la
liste blanche relève de la gouvernance du protocole (révision de D15), jamais d'un choix
local de projet.

La dérivation de clés reste Argon2id (mémoire au moins 64 Mio, au moins 3 itérations,
parallélisme unitaire) — elle n'est pas paramétrable : ses paramètres de coût sont des
planchers, ajustables à la hausse par le développeur. Les clés de chaque fragment sont
dérivées de la clé maîtresse par HKDF, avec un contexte distinct par fragment et par
génération.

### 3.2 En-tête normalisé

L'en-tête est la première section de la carte, signée avec les fragments dont il fait
partie intégrante. Syntaxe identique au format d'entrée — ASCII, ligne par ligne :

```
[carte] version=0.4.0
  algo_hachage     : sha256
  algo_signature   : ed25519
  algo_chiffrement : xchacha20poly1305
  profils          : x86-64-win11-pe, x86-64-linux-elf64
  empreinte_racine : sha256:9f3c…e21a
```

| Champ | Signification |
|---|---|
| `version` | Version du protocole à laquelle la carte est conforme |
| `algo_hachage` | Algorithme des empreintes de blocs et de la racine (liste blanche D15) |
| `algo_signature` | Algorithme de signature de la carte (liste blanche D15) |
| `algo_chiffrement` | Algorithme AEAD du chiffrement des fragments (liste blanche D15) |
| `profils` | Liste des profils de cible actifs du projet (identifiants `<isa>-<os>-<format>`) |
| `empreinte_racine` | Empreinte de l'ensemble des fragments, au format préfixé |

Tout agent vérifie le verrou croisé **avec l'algorithme de l'en-tête**, jamais avec un
algorithme supposé : c'est la condition de l'autodescription. Les empreintes portées par
frag-bld sont toutes au format `<algo>:<hexadécimal>` — par exemple `sha256:ab12…` — si
bien qu'une migration future reste lisible par les outils présents.

## 4. Format d'entrée de bloc

Syntaxe volontairement ASCII et ligne-par-ligne : tokenisation non ambiguë, diff lisible,
aucun caractère Unicode exotique ne pouvant corromdre l'encodage en transit. Exemple de
référence (bloc utilisé tout au long de la spécification) :

```
[bloc] id=b7f3a9 spec=hex:R4 cible=x86-64-win11-pe addr=0x4012A0 size=212 v=4 etat=scelle
  sig     : (ptr u8, usize) -> usize
  pre     : ptr != 0 && len <= MAX_LEN
  post    : ret <= len
  regs    : rbx, r12-r15 sauvegardes ; conv: msx64
  inv     : r8 aligne 16 dans la boucle
  deps    : [a31c2 memcpy] [ext AVX2]
  preuves : memsafe:ok bornes:ok term:ok
  tests   : 12400 cas ; ref=oracle_v9 ; crist=10/10
```

### 4.1 Répartition des champs

- **Première ligne** — identifiant, spécification, profil, adresse, taille, version, état :
  c'est à elle seule l'entrée de localisation portée par `frag-loc`. C'est la seule partie
  lue pour situer un bloc. Budget : 64 tokens maximum (amendé par D31 : la mesure M1 a
  constaté 43 tokens sur le gabarit canonique v0.4.0 lui-même, tokenizer cl100k_base —
  la v0.4.0 prévoyait 40).
- **Lignes suivantes** — signature, pré/post-conditions, registres préservés, invariants,
  dépendances, preuves, tests : entrée détaillée portée par `frag-con` et `frag-prf`,
  chargée uniquement quand le bloc est effectivement édité. Budget de l'entrée complète :
  200 tokens maximum (D8).

### 4.2 Sémantique des champs

| Champ | Signification |
|---|---|
| `id` | Identifiant stable du bloc sur six hexadécimaux ; référencé par les dépendances d'autres blocs |
| `spec` | **Traçabilité v0.4.0 (spécification § 4.2)** : spécification I d'origine au format `<DOM>-<NN>:R` (identifiant + révision) ; une reverse-spec en attente porte son statut (`prête`/`validée`) |
| `cible` | Profil de cible du bloc (identifiant `<isa>-<os>-<format>`) ; un même contrat I peut être instancié sur plusieurs profils |
| `addr` | Adresse virtuelle du point d'entrée — stable une fois scellé (R7), au sein du binaire du profil |
| `size` | Taille en octets, padding inclus |
| `v` | Version du bloc ; une correction crée une nouvelle version, pas une réécriture |
| `etat` | `brouillon`, `verifie`, `scelle`, `cristallise`, `deprecie` (voir § 7) |
| `sig` | Signature typée de la fonction — la partie de I embarquée dans C |
| `pre` / `post` | Pré-conditions et post-conditions du contrat |
| `regs` | Registres non volatils sauvegardés ; convention d'appel effective du profil (`msx64`, `sysv`, `lp64r`…) |
| `inv` | Invariants internes maintenus pendant l'exécution du bloc |
| `deps` | Dépendances : autres blocs (par id) et extensions ou instructions ISA requises |
| `preuves` | Résultats des preuves : sûreté mémoire, bornes, terminaison |
| `tests` | Volume de tests différentiels, référence de l'oracle, compteur de cristallisation |

## 5. Verrou croisé — procédure

Exécutée avant chaque édition et avant chaque chargement. Tout échec interrompt la
session : jamais de contournement, jamais de reprise forcée.

1. Vérifier la signature de la carte — avec `algo_signature` de l'en-tête — sur les quatre
   fragments ; une carte non signée ou à signature invalide est refusée (R9).
2. Recalculer l'empreinte de chaque bloc scellé visé par l'édition — avec
   `algo_hachage` de l'en-tête — ainsi que de l'ensemble de ses dépendances directes.
3. Comparer les empreintes obtenues à celles portées par `frag-bld` (format préfixé) ;
   tout écart signifie que binaire et carte ont divergé.
4. En cas d'écart : blocage de la session, journal de l'incident, état conservé pour
   audit — la reprise passe obligatoirement par une réconciliation manuelle documentée.

Au chargement — côté exécution cette fois — le binaire vérifie ses propres checksums avant
d'entrer dans sa boucle principale : chaque bloc scellé porte une empreinte vérifiable, et
un écart déclenche un arrêt propre plutôt qu'une exécution de code potentiellement altéré
(R10). La protection est bilatérale : la carte authentifie le binaire pendant le
développement, et le binaire s'authentifie lui-même en production. Falsifier l'un des deux
côtés sans détection exige de compromettre simultanément la clé de signature et le binaire
livré.

## 6. Cycle de vie d'une entrée

| État | Signification | Transition |
|---|---|---|
| `brouillon` | Bloc en cours d'écriture, non vérifié, non adressé | Création par l'agent ; adresse provisoire |
| `verifie` | Oracle passé une fois, round-trip conforme | Après une session de vérification complète (R5) |
| `scelle` | Commité : adresse stable, empreinte dans frag-bld | Commit atomique (étape 6 de la boucle) |
| `cristallise` | Immuable : dix vérifications réussies consécutives | Seuil atteint (R6) ; modification = procédure lourde |
| `deprecie` | Remplacé par une version plus récente | Conservé pour l'audit et le traçage des variantes |

La cristallisation est le mécanisme d'économie structurelle : un bloc cristallisé n'est
plus jamais rechargé ni re-vérifié en session — seule son empreinte est contrôlée, ce qui
coûte une comparaison de chaîne courte. La modification d'un bloc cristallisé reste
possible mais relève d'une procédure délibérément lourde : justification sur la couche I,
double vérification par oracle, et création d'un nouveau bloc plutôt qu'une réécriture —
l'ancien passant à l'état déprécié. Cette asymétrie de coût est volontaire : elle rend
l'évolution des blocs mûrs rare et réfléchie, exactement comme un noyau de système
d'exploitation protège ses parties les plus éprouvées.

## 7. Budgets en tokens

| Opération | Données lues | Budget |
|---|---|---|
| Localiser un bloc | frag-loc — une entrée | 64 tokens max (D31) |
| Éditer simplement un bloc | frag-loc + frag-con du bloc + notation | 3 000 tokens max |
| Ajouter un bloc (profil existant) | frag-loc + frag-con + notation | 6 000 tokens max |
| Instancier un profil nouveau pour un contrat existant | I partagée + frag-con + notation du profil | 6 000 tokens max par bloc |
| Audit complet (rare) | Carte entière déchiffrée | Non budgété — opération exceptionnelle |

L'agent ne lit jamais le binaire en entier : la carte est son unique index, et elle est
conçue pour être lue parcellairement (compacité, chargement paresseux, cristallisation).
Le multi-profils n'alourdit pas la localisation : l'entrée de frag-loc porte le profil, et
l'instanciation d'un contrat sur un profil nouveau est budgété comme un ajout — la couche
I, elle, n'est jamais dupliquée.

## 8. Export de continuité (D16)

### 8.1 Contenu et sécurité

L'export de continuité est l'unique forme sous laquelle l'état protocole quitte le poste de
développement. C'est un conteneur unique regroupant :

- la **couche I** complète — contrats, pré/post-conditions, invariants ;
- la **couche B** — le binaire scellé de chaque profil actif ;
- la **couche C** — les quatre fragments et l'en-tête de la carte ;
- un **manifeste autodescriptif** : version du protocole, suite cryptographique (les trois
  algorithmes de l'en-tête), profils actifs, empreinte racine, date, liste des contrôles
  effectués à l'export.

Le conteneur est chiffré intégralement (AEAD de l'en-tête, clé dérivée de la phrase
maîtresse par Argon2id — les mêmes paramètres que la carte au repos) et signé
(`algo_signature`). Chiffré, il peut être stocké n'importe où — y compris un stockage
cloud — sans exposer la carte, ce qui satisfait la règle de sauvegarde 3-2-1 ; signé, il
est vérifiable à l'import ; autodescriptif, il ne requiert aucune connaissance extérieure
à lui-même.

L'oracle est volontairement exclu du conteneur : éphémère par conception (D1), il est
régénéré depuis I à l'arrivée. L'export n'embarque ainsi aucun artefact empoisonnable
persistant — un export falsifié est détecté par la signature, un export volé est
indéchiffrable sans la phrase maîtresse.

### 8.2 Procédure d'import — cinq étapes

Exécutée par tout agent conforme TRIADE sur un poste ou un agent nouveau :

1. **Déchiffrement** du conteneur par la phrase maîtresse (escrow deux-sur-trois si le
   contexte est organisationnel). Un échec de déchiffrement est terminal : rien n'est
   interprété.
2. **Vérification de la signature** du conteneur et de la carte qu'il contient. Un export
   non signé ou à signature invalide est refusé (R9) — sans exception, même si son
   contenu paraît sain.
3. **Vérification du verrou croisé** : recalcul des empreintes de B avec l'algorithme de
   l'en-tête, comparaison à frag-bld. Tout écart bloque la reprise (R8).
4. **Régénération de l'oracle** depuis la couche I — l'oracle n'est jamais importé.
5. **Reprise normale** : la boucle de mise à jour s'applique à l'identique.

Cette procédure garantit l'anti-enfermement : le développeur peut changer d'agent, de
poste ou de fournisseur à tout moment, sans perte et sans dépendance envers l'agent qui
l'a précédé. Elle garantit aussi la traçabilité : le manifeste conserve la date, la suite
cryptographique et les contrôles de l'export, ce qui l'inscrit dans la chaîne de confiance
du scellage.

### 8.3 Statut de l'interdiction de livraison

La règle R1, précisée par D16, s'entend ainsi : la carte, la couche I et les vecteurs de
test ne sont **jamais livrés avec l'artefact ni communiqués à des tiers**. L'export de
continuité est l'unique exception — réservé au développeur, exclusivement sous forme
chiffrée et signée. Un export en clair est une violation du protocole ; sa production,
son acceptation ou sa diffusion constituent des interdits absolus pour l'agent (voir le
manuel agent, § 9).

## 9. Migration cryptographique — le re-cryptage

Le changement d'un paramètre de la suite cryptographique en cours de projet est possible ;
c'est une opération de migration complète, dite **re-cryptage**, jamais un basculement
silencieux :

1. Justification consignée sur le journal des décisions du projet (conformité, résistance
   anticipée, performance).
2. Recalcul de toutes les empreintes des blocs scellés avec le nouvel algorithme ;
   réécriture de frag-bld au format préfixé.
3. Re-chiffrement des quatre fragments avec les nouvelles clés dérivées ; mise à jour de
   l'en-tête.
4. Re-signature complète de la carte ; régénération de l'empreinte racine.
5. Archivage de l'ancienne carte — dépréciée, jamais détruite : l'audit doit pouvoir
   remonter la chaîne des suites successives.
6. Un nouvel export de continuité est produit dès la migration achevée : la version
   chiffrée avec l'ancienne suite devient obsolète et doit être retirée des stockages.

L'opération est atomique — elle réussit entièrement ou laisse l'ancienne carte en place —
et journalisée. Le round-trip de vérification s'exécute immédiatement après : la première
édition suivant un re-cryptage vérifie l'intégralité des empreintes, pas seulement les
blocs visés.

## 10. Audit de traçabilité et tableau de bord (v0.4.0)

La **commande d'audit de traçabilité** parcourt la carte et vérifie les chaînes complètes
I ↔ C ↔ B ↔ tests (spécification § 4.2) : chaque entrée porte son champ `spec=<DOM>-<NN>:R` ;
chaque spécification référencée existe à la révision indiquée ; chaque bloc scellé a une
empreinte dans frag-bld ; chaque vecteur de frag-prf se rattache à une exigence numérotée
de la spécification. Trois propriétés attendues, dont la violation est un refus de build :
aucune spécification sans entrée de carte (hors reverse-specs en statut « prête », visibles
comme telles) ; aucun bloc scellé sans spécification référencée ; aucun vecteur orphelin.

Le même audit produit le **tableau de bord de conformité** (spécification § 15.2) :
métriques mesurables avec leurs cibles — spécifications à jour, chaînes complètes,
construction, tests, empreintes des données embarquées, défauts ouverts par classe de
taxonomie T1-T6, optimisations sans mesure, budgets tokens (une fois instrumentés, M1),
suite de conformité par profil actif, changements hors journal des décisions, balisage
correct des pré-versions. Le tableau est archivé avec la carte à chaque cristallisation :
la conformité s'inspecte a posteriori, elle ne se déclare pas.

## 11. Le coffre-fort des phrases maîtresses (D75)

### 11.1 Objet et modèle de secret

Le coffre-fort centralise **toutes les phrases maîtresses, par projet**, dans un conteneur
unique chiffré. Il ne remplace ni la carte ni l'export de continuité : il protège le
maillon que ni l'un ni l'autre ne couvrait — la phrase elle-même, jusque-là confiée à la
seule instruction de cérémonie (D27/D30) alors que quatre réinitialisations du poste de
développement en ont démontré la fragilité. Deux niveaux de secret, jamais confondus :

- la **phrase de contrôle** ouvre le coffre ; elle vit sous garde durable depuis D81 —
  sauvegardée dès production (init, rotation, changement) dans le dépôt
  (`PHRASE-CONTROLE-COFFRE.txt` au racine, phrase seule sur une ligne, lisible par
  `--phrase-fichier`) et au racine du coffre Drive, AVANT toute autre action de la
  session ; le fichier EST la remise — l'affichage unique de cérémonie (D27/D30) demeure
  possible mais n'est plus le canal de survie ;
- les **phrases maîtresses** stockées, une par lignée de clés et par projet, déverrouillent
  les fragments de cartes (§ 3.1) — la graine Ed25519, elle, reste hors coffre (D30).

### 11.2 Format conteneur « TRIADE-CF1 »

```
magic « TRIADE-CF1 » (10 o) · version u16 (1) ·
champs longueur-préfixée u16 : hachage (sha256), kdf (argon2id(65536,3,1)),
                               chiffrement (xchacha20poly1305), date ISO-8601 UTC ·
sel Argon2id 32 o (aléatoire à l'init, rotation au changement de phrase) ·
nonce 24 o (aléatoire à CHAQUE écriture) ·
empreinte sha256 du chiffretexte 32 o ·
chiffretexte : XChaCha20-Poly1305(JSON base, clé dérivée, AAD = tout ce qui précède)
```

La base déchiffrée est un JSON `{format, protocole, cree, modifie, projets}` ; chaque
projet porte une description et des entrées `etiquette / description / cree / modifie /
phrase_b64`. Dérivation : Argon2id aux planchers de § 3.1 sur la phrase de contrôle et le
sel du conteneur, puis HKDF-SHA256 avec sel `TRIADE-coffre-fort` et info `coffre=v1` — un
contexte distinct des fragments de carte et de l'export de continuité, nul chevauchement
de clé. L'écriture est atomique (tmp + `os.replace` + `fsync`, 0600, répertoire 0700) ;
toute anomalie de parsing, d'algorithme (liste blanche de l'en-tête), d'empreinte ou de
tag AEAD est un refus terminal — rien n'est interprété (fail-closed).

### 11.3 Outil, commandes et discipline

L'outil vit dans le dépôt (`coffre_fort.py`, racine du projet) ; le conteneur
`.keys/coffre_fort.bin` vit hors dépôt (gitignore, jamais commité ni synchronisé en clair).
Commandes : `init` (génération éventuelle de la phrase de contrôle, 128 bits, modèle D27),
`statut` (en-tête clair seul), `ajouter` / `lister` / `obtenir` / `retirer` (par projet et
étiquette ; `obtenir --vers-fichier` restaure l'état opérationnel, chmod 600), `verifier`,
`changer-phrase` (rotation du sel), `exporter` / `importer` (conteneur chiffré — coffre
Drive du projet et coffre personnel du développeur, les deux copies), `autotest`.

Discipline consignée : (1) chaque cérémonie de clés alimente le coffre dans la même
session ; (2) l'`autotest` — falsifications d'un octet (chiffretexte, sel, nonce,
empreinte), mauvaise phrase, anti-écrasement, témoin sauvage de randomisation — doit passer
avant tout usage sur un poste neuf ; (3) l'export chiffré se téléverse au racine du coffre
Drive (copie projet) et se remet au coffre du développeur (copie personnelle) ; (4) toute
production d'une phrase de contrôle neuve est sauvegardée AVANT TOUTE AUTRE ACTION —
`PHRASE-CONTROLE-COFFRE.txt` au racine du dépôt (commit dédié, push GitHub, miroir Drive
par le hook) + copie au racine du coffre Drive, md5 vérifiés — le fichier est la remise
(D81) ; à chaque rotation il est remplacé et git conserve les phrases retirées du service ;
(5) après une réinitialisation : importer le conteneur, relire la phrase de contrôle
depuis `PHRASE-CONTROLE-COFFRE.txt` (dépôt, miroir ou racine du coffre Drive — D81), puis
`obtenir --vers-fichier .keys/passphrase.txt` — la lignée redevient opérationnelle sans
cérémonie de régénération (la signature des cartes reste attachée à sa graine, D30/D74).
Contrepartie consignée (D81) : la phrase vit sur le stockage du coffre Drive partagé par
lien — la confidentialité au repos repose sur le contrôle d'accès au dossier (restriction
du partage par lien : mitigation première) ; une phrase entrée dans l'historique git y
demeure à vie, la rotation reste le remède à toute exposition avérée.
