# Ce que le protocole garantit — et ce qu'il ne garantit pas (v1.3)

> Synthèse des décisions D253 (publication d'une bascule), D254 (racine de
> confiance au chargement), D263 (compteur NV) et D267 (ancrage de transparence). Elle s'adresse au développeur qui doit dire, sans
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

## 5. Le compteur NV comme plancher de fraîcheur (D263)

La fraîcheur ne peut pas reposer sur l'horloge ni sur un horodatage de fichier : un
administrateur les remet ensemble. Le **compteur NV monotone** — compteur NV TPM 2.0
lorsque le profil en dispose, compteur monotone RPMB (eMMC/UFS) sinon — est comparé au
plancher scellé dans le manifeste signé. Refus fail-closed nommés : compteur absent ou
illisible (`ANCRE-PERDUE`), aucun plancher scellé (`SCELAGE-NON-ENREGISTRE`), compteur
inférieur au plancher (`RETOUR-EN-ARRIERE`), incrément non monotone
(`INCREMENT-NON-MONOTONE`). **Limites** : l'effacement du TPM ou le remplacement du média
remet le compteur à zéro et exige une cérémonie de ré-enregistrement ; un TPM virtualisé
ne prouve rien du silicium ; le compteur prouve un plancher, pas l'identité de la version
fraîche.

## 6. L'ancrage de transparence des témoins d'époque (D267)

Un témoin d'époque (édition, empreinte de l'artefact, empreinte de l'état, date) peut être
ancré hors de la machine : entrée de journal de transparence (Rekor) ou horodatage qualifié
(RFC 3161). **Statut appliqué : la règle est adoptée et outillée, le déploiement n'est pas
fait** — un témoin non ancré reste marqué non ancré, jamais promu. Refus nommés :
`ANCRE-INDISPONIBLE` (ancrage configuré, service injoignable → release refusée),
`TEMOIN-SANS-ANCHE`, `ANCRE-INCOHERENTE`. **Delta au modèle de menace** : en ligne, au
geste de release seulement, l'ancre voit la restauration cohérente d'un couple binaire +
état — au prix d'une fuite d'empreintes et d'une dépendance à un tiers ; hors ligne, au
chargement, rien ne change (R10 ne fait aucun appel réseau). L'ancrage est une propriété
de **release**, jamais une condition de démarrage.
