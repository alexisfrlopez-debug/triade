# Ce que le protocole garantit — et ce qu'il ne garantit pas (v1.1)

> Synthèse des décisions D253 (publication d'une bascule) et D254 (racine de
> confiance au chargement). Elle s'adresse au développeur qui doit dire, sans
> exagérer, ce que son artefact promet à son utilisateur.

## 1. La publication d'une bascule (patch à chaud)

- Un magasin mémoire simple n'est **atomique que jusqu'à huit octets naturels**.
  Douze ou seize octets alignés ne le sont pas.
- Seize octets ne se publient atomiquement que par un **unique `LOCK CMPXCHG16B`**,
  sous CPUID, dans un emplacement aligné sur seize.
- Recommandation : concevoir chaque trampoline comme **un mot de huit octets**
  (`E9 rel32` + trois `NOP`), aligné sur huit — la forme la plus simple qui soit
  atomique par construction.
- **L'atomicité du magasin ne protège pas un thread** dont le pointeur
  d'instruction tombe dans la plage remplacée : il peut décoder un mélange des
  deux flux. La publication exige donc un **rendez-vous de quiescence**
  (suspension et lecture de RIP sous Windows ; arrêt par signal / `ptrace` sous
  Linux), avec refus si un thread est immobilisé dans la plage.
- L'émulation ne valide pas la cohérence du cache d'instructions : la preuve
  concurrente se fait au métal nu, sur au moins deux machines.

## 2. La racine de confiance au chargement (R10)

Trois propriétés **distinctes**, jamais confondues :

| Propriété | Question | Mécanisme |
|---|---|---|
| Intégrité | les octets sont-ils ceux qui ont été scellés ? | checksums des blocs + empreinte du manifeste recomposée |
| Authenticité | le manifeste a-t-il été signé par la clé autorisée ? | signature Ed25519 vérifiée sous la clé épinglée **hors de l'artefact** |
| Fraîcheur | la version est-elle la plus récente admise, non révoquée ? | plancher de version signé + époque de l'état local |

**La garantie vaut ce que vaut l'ancre**, et l'ancre diffère par profil :
Authenticode vérifié par le système sous Windows ; IMA appraisal (clé du trousseau
noyau) ou signature de paquet sous Linux ; chaîne de boot signée sous RISC-V.

**Ce qui n'est pas garanti — à écrire noir sur blanc dans votre documentation :**
- si l'ancre est modifiable avec l'artefact (dépôt inscriptible, clé dans le
  binaire), R10 détecte la corruption et la falsification opportuniste, **pas un
  administrateur local** qui remplace ensemble binaire, clé et état ;
- la **restauration cohérente d'un couple binaire + état** (snapshot, VM) échappe
  à toute ancre locale : seuls des témoins **hors machine** la rendent visible
  (journal poussé, carte papier, journal de transparence) ;
- R10 est local et **hors ligne** : aucun appel réseau au chargement, la
  révocation d'une clé voyage avec la version suivante.

## 3. Les refus nommés (fail-closed)

Au chargement, l'arrêt précède toute exécution et chaque refus porte son nom :
carte absente, clé d'ancre absente, signature invalide, manifeste divergent,
version sous le plancher, état absent non déclaré, retour en arrière, tentative
réseau. **Aucun chemin dégradé n'existe.**

## 4. Rotation et révocation

La clé neuve est distribuée **hors bande** avec son identifiant (`kid`) et un
plancher d'époque ; une clé absente ou révoquée est un refus nommé, jamais une
récupération automatique. La rotation est un acte, pas une mise à jour silencieuse.
