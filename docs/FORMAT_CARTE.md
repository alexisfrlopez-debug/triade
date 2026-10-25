# FORMAT DE LA CARTE — Couche C, spécification détaillée

> Ce document détaille le format de la carte TRIADE : fragments, format d'entrée de bloc,
> procédure du verrou croisé, cycle de vie et budgets. La carte est le cœur opérationnel du
> protocole : elle rend le binaire navigable pour l'agent, porte les preuves et concentre la
> valeur intellectuelle du projet.

## 1. Contraintes de conception

Trois contraintes tirées de la fonction objectif structurent le format : **compacité**
(coût en tokens — chapitre 9 de la spécification), **intégrité** (verrou croisé D5) et
**résilience** face à la compromission (sharding et chiffrement D4). Chaque contrainte se
traduit par un mécanisme précis : syntaxe ASCII ligne-par-ligne à budgets serrés,
signature Ed25519 de l'ensemble, chiffrement séparé des fragments.

## 2. Les quatre fragments

| Fragment | Contenu | Raison d'être de la séparation |
|---|---|---|
| `frag-loc` | Identifiants, noms, adresses, tailles, états, dépendances | Localisation : le plus lu, le moins sensible — peut être chargé seul |
| `frag-con` | Signatures, pré/post-conditions, invariants, conventions d'appel | Contrats : diffés à chaque changement (R2), lus à chaque édition |
| `frag-prf` | Vecteurs dorés hachés, compteurs de cristallisation, seuils | Preuves : volumineux, rarement lu en entier après cristallisation |
| `frag-bld` | SHA-256 des blocs, manifestes de build, registre des variantes | Verrou croisé et traçage (D5, D6) — ne quitte jamais le poste de développement |

Chaque fragment est chiffré avec sa propre clé dérivée de la clé maîtresse
(XChaCha20-Poly1305, nonce aléatoire de 192 bits). Un compromis partiel — la fuite d'un
fragment isolé — n'est jamais une perte totale : les contrats sans les adresses, ou les
preuves sans les contrats, ne reconstituent pas la carte.

## 3. Chaîne cryptographique

- **Dérivation** : phrase secrète maîtresse → Argon2id (mémoire au moins 64 Mio, au moins
  3 itérations, parallélisme unitaire) → clé maîtresse.
- **Clés de fragments** : dérivation HKDF depuis la clé maîtresse, avec un contexte
  distinct par fragment et par génération.
- **Chiffrement au repos** : XChaCha20-Poly1305 par fragment.
- **Signature** : Ed25519 calculée sur le concaténé des empreintes de chaque fragment —
  toute substitution d'un seul fragment invalide la signature globale (R9).
- **Escrow** : partage de secret deux-sur-trois possible pour la clé maîtresse ;
  sauvegardes 3-2-1 chiffrées ; rotation = re-signature complète atomique et journalisée.

## 4. Format d'entrée de bloc

Syntaxe volontairement ASCII et ligne-par-ligne : tokenisation non ambiguë, diff lisible,
aucun caractère Unicode exotique ne pouvant corrompre l'encodage en transit. Exemple de
référence (bloc utilisé tout au long de la spécification) :

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

### 4.1 Répartition des champs

- **Première ligne** — identifiant, adresse, taille, version, état : c'est à elle seule
  l'entrée de localisation portée par `frag-loc`. C'est la seule partie lue pour situer un
  bloc. Budget : 40 tokens maximum.
- **Lignes suivantes** — signature, pré/post-conditions, registres préservés, invariants,
  dépendances, preuves, tests : entrée détaillée portée par `frag-con` et `frag-prf`,
  chargée uniquement quand le bloc est effectivement édité. Budget de l'entrée complète :
  200 tokens maximum (D8).

### 4.2 Sémantique des champs

| Champ | Signification |
|---|---|
| `id` | Identifiant stable du bloc sur six hexadécimaux ; référencé par les dépendances d'autres blocs |
| `addr` | Adresse virtuelle du point d'entrée — stable une fois scellé (R7) |
| `size` | Taille en octets, padding inclus |
| `v` | Version du bloc ; une correction crée une nouvelle version, pas une réécriture |
| `etat` | `brouillon`, `verifie`, `scelle`, `cristallise`, `deprecie` (voir § 6) |
| `sig` | Signature typée de la fonction — la partie de I embarquée dans C |
| `pre` / `post` | Pré-conditions et post-conditions du contrat |
| `regs` | Registres non volatils sauvegardés ; convention d'appel (`msx64` sur la cible Windows) |
| `inv` | Invariants internes maintenus pendant l'exécution du bloc |
| `deps` | Dépendances : autres blocs (par id) et extensions CPU requises |
| `preuves` | Résultats des preuves : sûreté mémoire, bornes, terminaison |
| `tests` | Volume de tests différentiels, référence de l'oracle, compteur de cristallisation |

## 5. Verrou croisé — procédure

Exécutée avant chaque édition et avant chaque chargement. Tout échec interrompt la
session : jamais de contournement, jamais de reprise forcée.

1. Vérifier la signature Ed25519 de la carte sur les quatre fragments ; une carte non
   signée ou à signature invalide est refusée (R9).
2. Recalculer le SHA-256 de chaque bloc scellé visé par l'édition, ainsi que de l'ensemble
   de ses dépendances directes.
3. Comparer les empreintes obtenues à celles portées par `frag-bld` ; tout écart signifie
   que binaire et carte ont divergé.
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
| `scelle` | Commité : adresse stable, SHA-256 dans frag-bld | Commit atomique (étape 6 de la boucle) |
| `cristallise` | Immuable : dix vérifications réussies consécutives | Seuil atteint (R6) ; modification = procédure lourde |
| `deprecie` | Remplacé par une version plus récente | Conservé pour l'audit et le traçage des variantes |

La cristallisation est le mécanisme d'économie structurelle : un bloc cristallisé n'est
plus jamais rechargé ni re-vérifié en session — seul son SHA-256 est contrôlé, ce qui
coûte une comparaison de 64 caractères. La modification d'un bloc cristallisé reste
possible mais relève d'une procédure délibérément lourde : justification sur la couche I,
double vérification par oracle, et création d'un nouveau bloc plutôt qu'une réécriture —
l'ancien passant à l'état déprécié. Cette asymétrie de coût est volontaire : elle rend
l'évolution des blocs mûrs rare et réfléchie, exactement comme un noyau de système
d'exploitation protège ses parties les plus éprouvées.

## 7. Budgets en tokens

| Opération | Données lues | Budget |
|---|---|---|
| Localiser un bloc | frag-loc — une entrée | 40 tokens max |
| Éditer simplement un bloc | frag-loc + frag-con du bloc + notation | 3 000 tokens max |
| Ajouter un bloc | frag-loc + frag-con + seuils frag-prf | 6 000 tokens max |
| Audit complet (rare) | Carte entière déchiffrée | Non budgété — opération exceptionnelle |

L'agent ne lit jamais le binaire en entier : la carte est son unique index, et elle est
conçue pour être lue parcellairement (compacité, chargement paresseux, cristallisation).
