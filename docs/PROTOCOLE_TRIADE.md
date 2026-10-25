# PROTOCOLE TRIADE v0.3 — Spécification technique

> Source de travail faisant autorité pour la v0.3. Le PDF
> `docs/Protocole_TRIADE_v0.2_Specification.pdf` demeure l'archive formelle de la version
> précédente ; la génération du PDF v0.3 interviendra à la stabilisation de la version
> (`scripts/triade_v02_spec.py` sert de modèle).

- Version : v0.3 — universalité par profils de cible, suite cryptographique paramétrable, export de continuité
- Date : 25 octobre 2026
- Couches : I/B/C · Profil primaire : x86-64 / Windows 11 / PE32+

---

## 1. Vision et objectifs

Le développement logiciel est entré dans l'ère agent-first : une part croissante du code est
écrite, relue et modifiée par des modèles de langage plutôt que par des humains. Cette
bascule remet en question une hypothèse centrale de nos outils — que le code source est
optimisé pour la lecture humaine. Compilateurs, systèmes de build et langages ont été conçus
autour de cette hypothèse ; si le lecteur principal devient une machine, l'empilement
complet mérite un réexamen systématique plutôt qu'une révision marginale.

TRIADE est la réponse disciplinée à ce réexamen. Plutôt que de supprimer les langages — une
impossibilité de principe, puisqu'un modèle de langage manipule des symboles textuels et que
tout format binaire rendu lisible par un agent constitue de facto un langage —, TRIADE
déplace le langage vers une fine couche de spécification maintenue par l'agent, tandis que
l'artefact livré est du code machine natif pur. Le compilateur disparaît du pipeline de
production : il n'existe plus aucune couche de traduction entre ce que l'agent écrit et les
octets exécutés. Ce que l'agent écrit est ce qui s'exécute — et rien d'autre.

Le nom encode l'architecture : trois couches indissociables — Intention (I), Binaire (B),
Carte (C) — unies par un verrou croisé cryptographique. La couche I contient le quoi et le
pourquoi : contrats typés, pré et post-conditions, invariants. La couche B contient le
comment : des octets scellés, versionnés, à adresses stables. La couche C — la
formalisation du système de balises décrit au départ du projet — est l'index naviguable qui
lie les deux et sert d'unique interface de développement à l'agent.

### 1.1 Fonction objectif hiérarchisée

**Sécurité > Performance > Optimisation > Coût en tokens** — arbitrage lexicographique : un
objectif n'est jamais sacrifié au profit d'un objectif de rang inférieur.

| Objectif | Signification concrète | Métrique de validation |
|---|---|---|
| Sécurité | Sûreté mémoire validée par oracle, intégrité carte ↔ binaire, durcissement au chargement | 0 corruption détectée par l'oracle ; tout échec de verrou bloque la session |
| Performance | 100 % code machine natif, zéro abstraction intermédiaire entre l'écriture et l'exécution | Comparaison par bloc scellé face à une référence compilée (clang -O2 ou équivalent du profil) |
| Optimisation | Descente à l'ISA sur les hot paths identifiés par profilage | Gain mesuré et journalisé pour chaque bloc optimisé |
| Coût en tokens | Édition ciblée via la carte, jamais de lecture intégrale du binaire | Budgets par type d'édition (chapitre 9) |

### 1.2 Périmètre et non-objectifs

Trois non-objectifs posés d'emblée. Premièrement, TRIADE ne prétend pas remplacer les
langages dans l'industrie : c'est une architecture de laboratoire, conçue pour être validée
sur une application réelle complète. Deuxièmement, la furtivité face aux EDR n'est pas
recherchée : l'outil cible est un utilitaire de pentest destiné à des tests autorisés en
environnement de laboratoire, et les API du système sont appelées via les interfaces
standards du profil. Troisièmement, l'universalité revendiquée par la v0.3 est structurelle
mais progressive : chaque profil de cible doit être instancié et validé (jalons M6 et M7)
avant d'être déclaré supporté — le protocole ne promet pas la portabilité, il la vérifie.

## 2. Journal des décisions (D1–D16)

Chaque décision structurante est consignée avec ses alternatives rejetées et sa
justification rattachée à la fonction objectif — voir `docs/DECISIONS.md` pour le journal
complet (D1–D10 issues de la v0.2 ; D11–D13 issues de l'infrastructure de sauvegarde ;
D14–D16 issues de la v0.3, dont deux amendent des décisions antérieures). Toute révision
future du protocole doit soit respecter ces décisions, soit expliciter précisément ce qui
les invalide. Cette discipline évite la dérive progressive qui transforme un protocole
propre en accumulation d'exceptions incohérentes.

Cinq décisions engagent l'architecture entière. **D1** : l'oracle éphémère est le pivot du
compromis entre le « 100 % code machine » exigé pour l'artefact et la sûreté d'exécution ;
l'implémentation de référence ne sort jamais du laboratoire, ce qui préserve performance et
pureté du livrable tout en attrapant les corruptions mémoire avant scellage. **D2** :
keystone + capstone forment le couple d'assemblage et de désassemblage ; la nuance capitale
est que cette notation n'est pas un compilateur — aucune optimisation ni réécriture ne
s'intercale entre ce que l'agent écrit et les octets produits (principe WYSIWYG). **D5** :
le verrou croisé répond à la menace d'empoisonnement de carte — falsifier les métadonnées
ferait travailler l'agent sur des informations fausses et pourrait lui faire introduire une
porte dérobée en croyant respecter les contrats ; **D15** le rend paramétrable : les
algorithmes deviennent des choix consignés dans l'en-tête de la carte, dans les limites d'une
liste blanche. **D7** : les syscalls directs exigeraient une table de numéros par build de
Windows — une carte cachée supplémentaire, fragile — pour un gain relevant de la furtivité,
hors périmètre. **D14** : l'universalité est réalisée par des profils de cible vérifiables,
et non par une couche d'abstraction logicielle qui trahirait la fonction objectif
Performance.

## 3. Architecture TRIADE

L'architecture repose sur une séparation stricte entre ce que l'artefact contient, ce que
l'agent manipule et ce que le destinataire reçoit. Le diff d'intention descend de I vers C,
le verrou croisé relie C et B dans les deux sens, et la couche B seule quitte le
laboratoire. Aucune couche n'est optionnelle : privé de I, le système perd son ancrage
sémantique ; privé de C, l'agent devient aveugle ; privé de B, il n'y a plus rien à exécuter.

### 3.1 Les trois couches

| Couche | Contenu | Visibilité | Rôle |
|---|---|---|---|
| I | Spécifications, contrats typés pré/post, invariants logiques | Privée | Compression de l'intention — le quoi et le pourquoi |
| C | Index des blocs, adresses, signatures, preuves, manifestes de build | Privée, signée, chiffrée | Unique interface de développement de l'agent |
| B | Code machine scellé, padding inter-blocs, checksums runtime | Livrée | Le comment — exécution pure, sémantiquement muette |

Depuis la v0.3, la séparation des couches croise une seconde dimension : la cible. La
couche I est **indépendante de la cible** — un contrat s'écrit une fois, ses types abstraits
(`usize`, alignements) étant paramétrés par le profil. La couche B est **par profil** :
chaque plateforme visée possède son jeu d'octets scellés. La couche C indexe l'ensemble :
chaque entrée porte son profil, et frag-bld organise les empreintes par profil. Un même
contrat I est ainsi instancié par autant de blocs machine que de profils supportés —
c'est la condition de possibilité de la portabilité sans duplication de l'intention.

Le flux de travail découle de cette séparation : pour toute évolution, l'agent produit
d'abord un diff sur la couche I ; il localise les blocs concernés au travers de la carte,
sans jamais scanner le binaire ; il régénère les seuls blocs impactés — pour le ou les
profils visés —, les fait vérifier par l'oracle, puis commite l'ensemble de façon atomique :
patch du binaire, mise à jour de la carte et scellage ne font qu'un.

### 3.2 Invariants structurels

Quatre invariants non négociables, vérifiés à chaque cycle de build — leur violation est un
refus de build : B n'est jamais nu (R1) ; les adresses exposées sont stables (R7, par
profil) ; la signature couvre la carte entière (R9) ; B est auto-vérifiant au chargement
(R10).

## 4. La carte (couche C)

La carte est le cœur opérationnel du protocole : c'est elle qui rend le binaire navigable
pour l'agent, qui porte les preuves et qui concentre la valeur intellectuelle du projet.
Elle est compacte (coût en tokens), intègre (verrou croisé) et résiliente face à la
compromission (sharding et chiffrement).

Depuis la v0.3, la carte est **autodescriptive** : un en-tête normalisé consigne la version
du protocole, la suite cryptographique retenue — `algo_hachage` (SHA-256 par défaut),
`algo_signature` (Ed25519 par défaut), `algo_chiffrement` (XChaCha20-Poly1305 par défaut),
chacun modifiable par le développeur dans les limites d'une liste blanche (D15) — et la
liste des profils de cible actifs. Les empreintes portées par frag-bld sont préfixées par
leur algorithme (`sha256:ab12…`) : n'importe quel agent, présent ou futur, sait vérifier le
verrou croisé sans connaissance extérieure à la carte. La spécification détaillée —
fragments, en-tête, format d'entrée, verrou croisé, export de continuité, migration
cryptographique — fait l'objet de `docs/FORMAT_CARTE.md`.

## 5. Règles du protocole v0.3

R1 à R7 proviennent de la v0.1 ; R8 à R10 de la v0.2. La v0.3 n'ajoute aucune règle : elle
précise deux d'entre elles — preuve que le noyau normatif était déjà universel — et
s'appuie sur les décisions D14 à D16 pour les mécanismes. Les règles sont peu nombreuses,
vérifiables mécaniquement et sanctionnées par des effets concrets — refus de build, refus
de commit ou blocage de session — plutôt que par des recommandations.

| # | Règle | Énoncé | Violation et sanction |
|---|---|---|---|
| R1 | Jamais de binaire nu | Tout artefact B est accompagné de I et C à jour | Build refusé |
| R2 | Intention d'abord | Toute modification commence par un diff sur I | Édition rejetée par la boucle |
| R3 | Balisage obligatoire | Chaque bloc est décrit dans C | Build refusé |
| R4 | Patch à contrat stable | Le remplacement préserve signature et contrats ; les appelants ne sont jamais invalidés | Échec de vérification |
| R5 | Vérifie-puis-écrit | Aucun commit sans oracle, vecteurs dorés et round-trip | Commit impossible |
| R6 | Cristallisation | Dix vérifications réussies rendent le bloc immuable ; le modifier exige la procédure lourde | Nouvelle version du bloc |
| R7 | Adresses stables | Les points d'entrée sont garantis par padding ; patcher ne déplace rien | Re-liage forcé — interdit |
| R8 | Verrou croisé | Empreintes des blocs et signature de la carte vérifiés avant chaque édition | Session bloquée |
| R9 | Carte signée obligatoire | L'agent refuse toute carte non signée | Refus de démarrage |
| R10 | Fail-closed au chargement | Checksums vérifiés au lancement ; écart = arrêt propre | Arrêt de l'exécution |

Trois précisions. R4 signifie qu'un bloc remplaçant honore les contrats publiés de son
prédécesseur — mêmes signatures, mêmes pré et post-conditions, mêmes invariants visibles —
condition de possibilité du patch à chaud. R7 s'entend **par profil** : les adresses sont
stables au sein du binaire de chaque profil ; rien n'impose qu'elles coïncident entre
profils. R1, précisée par D16, interdit de livrer la carte **avec l'artefact** ou à des
tiers — elle n'interdit pas au développeur de détenir, sauvegarder et transférer son propre
état de développement : c'est précisément l'objet de l'export de continuité (§ 8.4).

## 6. Boucle de mise à jour

La boucle de mise à jour est le battement de cœur du protocole : c'est la seule voie par
laquelle le logiciel évolue. Elle se déroule en sept étapes réparties en deux phases —
l'édition, puis la validation et le commit — séparées par un point de non-retour : rien
n'est écrit dans le binaire avant que l'oracle n'ait rendu son verdict.

| N | Étape | Entrées | Sorties | Règles |
|---|---|---|---|---|
| 1 | Diff d'intention | Requête de changement, couche I | Diff minimal sur I | R2 |
| 2 | Localisation | frag-loc | Liste des blocs impactés | R3 |
| 3 | Verrou croisé | frag-bld, binaire | Verdict go / no-go | R8, R9 |
| 4 | Régénération ciblée | frag-con, notation du bloc | Octets candidats | R4, R7 |
| 5 | Vérification | Candidats, oracle, vecteurs dorés | Verdict, journal | R5 |
| 6 | Commit atomique | Verdict favorable | Patch B, carte à jour, scellage | R1 |
| 7 | Cristallisation | Compteur de vérifications | Bloc immuable | R6 |

### 6.1 Patch à chaud — exemple du profil primaire

Le patch à chaud — modifier un logiciel en cours d'exécution — est l'un des deux objectifs
fondateurs du projet avec la performance. Le mécanisme exact est **spécifié par chaque
profil de cible** (taille minimale de bascule atomique, procédure d'invalidation du cache
d'instructions) ; ce paragraphe décrit l'instanciation du profil primaire x86-64. La
méthode contourne la cohérence du cache d'instructions et l'atomicité de la bascule en
n'écrivant jamais un bloc pendant qu'il s'exécute : le nouveau bloc est d'abord écrit dans
une zone de croissance libre ; ensuite, et seulement ensuite, un trampoline de 12 à 16
octets est installé à l'ancien point d'entrée et basculé par une écriture alignée unique,
atomique pour le processeur.

```
; trampoline de bascule atomique (aligné sur 16 octets)
; forme courte : saut relatif 32 bits
  E9 xx xx xx xx                ; jmp rel32 -> nouveau bloc
; forme longue : saut absolu 64 bits
  48 B8 xx xx xx xx xx xx xx xx ; mov rax, addr_new
  FF E0                         ; jmp rax
```

L'ancien trampoline est conservé : le rollback copy-on-write de l'étape 5 consiste à
rebasculer vers lui, et la carte référence les deux versions tant que la nouvelle n'a pas
atteint son seuil de cristallisation. Les adresses stables garantissent qu'aucun appelant
ne référence l'intérieur d'un bloc : seuls les points d'entrée — promis par R7 — sont
susceptibles d'être trampolinés, et la table de ces points est close et vérifiée par le
verrou croisé. Le critère de sortie du jalon M2 est précisément ce scénario : remplacer le
bloc d'écho d'un serveur TCP pendant qu'il traite des connexions, sans interruption de
service et avec rollback démontré.

## 7. Stratégie de vérification

Supprimer le compilateur, c'est perdre les filets de sécurité qu'il tendait gratuitement :
vérification de types, initialisation, analyse de flot. La stratégie de vérification
reconstruit une confiance équivalente — voire supérieure — sans réintroduire de couche de
traduction dans l'artefact. Elle repose sur trois piliers.

**L'oracle éphémère** : implémentation de référence de chaque bloc — triviale,
volontairement lente, écrite dans un langage sûr et dérivant directement de la couche I. Il
est généré au début de chaque session, utilisé pour des tests différentiels par propriétés,
puis détruit : jamais livré, jamais archivé dans la carte ; seuls ses vecteurs de test
dorés — hachés — y survivent. Le protocole de test est différentiel : l'oracle et le bloc
machine reçoivent des entrées aléatoires contraintes par les pré-conditions du contrat, et
leurs sorties sont comparées octet par octet. Volume de référence : douze mille cas par
bloc critique. Trois propriétés rendent l'oracle fiable : il dérive de I et non de B (il ne
peut pas hériter d'un bug du code machine) ; il est régénéré à chaque session (jamais en
désaccord avec les contrats courants) ; sa régénération coûte moins que le diagnostic d'une
corruption découverte après scellage. Par ailleurs, l'oracle étant dérivé de I — couche
indépendante de la cible — le **même** oracle valide les blocs de tous les profils : la
portabilité ne divise pas le coût de vérification, elle le mutualise.

**Le round-trip de notation** : chaque bloc assemblé par le moteur de notation du profil
est désassemblé par le vérificateur correspondant, et les instructions obtenues sont
comparées à la notation d'origine. Tout désaccord — une instruction, un opérande, une
taille d'encodage — est un échec de build. Ce contrôle à coût quasi nul attrape la classe
d'erreurs la plus insidieuse : l'écart silencieux entre ce que l'agent croit avoir écrit et
les octets réellement produits.

**La cristallisation** ferme la boucle économique : plus un bloc fait ses preuves, moins il
coûte à vérifier, ce qui libère le budget pour les blocs jeunes et les zones actives. La
chaîne de confiance du scellage résume le parcours d'une preuve : verdict de l'oracle →
vecteurs dorés hachés dans frag-prf → empreinte du bloc dans frag-bld → signature de la
carte entière → immuabilité à dix vérifications.

## 8. Sécurité et anti-rétro-ingénierie

La question qui a motivé la v0.2 — détenir la cartographie uniquement côté développeur
pour coder en binaire pur et freiner la rétro-ingénierie — reçoit ici sa réponse
systématique. Le principe directeur est la séparation de deux budgets souvent confondus :
l'obfuscation, qui protège la propriété intellectuelle (le comment), et le durcissement,
qui protège l'exécution (le où ça casse). La carte privée relève du premier ; la sûreté
mémoire, les contrats et le fuzzing relèvent du second. Conformément au principe de
Kerckhoffs, la sécurité du système ne repose jamais sur le secret de la carte : elle
survivrait à sa divulgation.

### 8.1 Modèle de menace

| Menace | Acteur | Cible | Contre-mesure | Résiduel |
|---|---|---|---|---|
| Rétro-ingénierie de l'IP | Concurrent, pirate | Binaire livré | Carte privée ; binaire sémantiquement muet ; variantes par build | Temps acheté — s'érode avec les LLM de décompilation |
| Empoisonnement de carte | Attaquant supply-chain | Fragments | Signature (algo de l'en-tête) ; refus de carte non signée ; verrou croisé | Détecté — session bloquée (fail-closed) |
| Fuite de la carte | Initié, poste compromis | Fragments au repos | Chiffrement (algo de l'en-tête) ; sharding ; escrow | Perte partielle limitée à un fragment |
| Vol de l'export de continuité | Voleur, stockage cloud compromis | Conteneur exporté | Chiffrement intégral (phrase maîtresse + Argon2id) ; signature | Sans la phrase, indéchiffrable — aucune donnée en clair |
| Fuzzing boîte noire | Attaquant externe | Runtime | Contrats, oracle, tests par propriétés, fail-closed | Indépendant du secret de la carte |
| Redistribution frauduleuse | Pirate | Binaire livré | Empreintes par build — canary trap | Fuite traçable à son destinataire |
| Instrumentation dynamique | Analyste | Exécution | Anti-debug léger par mesure de temps | Assumé — l'obscurité n'est pas la sécurité |

La rétro-ingénierie est traitée comme un objectif d'économie, pas d'impossibilité : rendre
le coût de l'analyse supérieur à la valeur de ce qu'on obtient. Un binaire strippé, sans
structure ni symboles, dont chaque exemplaire diffère, coûte sensiblement plus cher à
analyser qu'un binaire compilé standard — mais les modèles de langage appliqués à la
décompilation progressent, et l'avantage doit être réévalué à chaque génération de modèles.

### 8.2 Empreintes par build

Puisque la régénération du code machine est quasi gratuite dans ce paradigme, chaque
livraison porte une variante unique sans coût marginal : réordonnancement des blocs scellés
indépendants, insertion de nops multioctets, choix parmi les encodages équivalents que
l'ISA offre pour une même instruction (`89 C0` / `8B C0` pour `mov eax, eax` — ni le sens
ni les effets ne changent, seule la signature binaire change). Le registre des variantes
est conservé dans frag-bld, côté développeur, par profil : toute fuite du binaire devient
traçable jusqu'à son destinataire.

### 8.3 Suite cryptographique et gestion des clés

Depuis la v0.3, la suite cryptographique est **paramétrable par le développeur** (D15) :
l'en-tête de la carte consigne `algo_hachage` (SHA-256 par défaut), `algo_signature`
(Ed25519 par défaut) et `algo_chiffrement` (XChaCha20-Poly1305 par défaut). La liberté
s'exerce dans une liste blanche d'algorithmes atteignant le seuil de sécurité du protocole
— au moins 128 bits de sécurité et résistance à la collision pour le hachage ; signatures
déterministes ou protégées par randomisation hedged pour la signature ; chiffrement
authentifié (AEAD) uniquement. Tout algorithme sous le seuil (MD5, SHA-1) est refusé : la
volonté du développeur s'exerce entre algorithmes conformes, jamais contre la fonction
objectif. Les motivations typiques d'un changement : conformité réglementaire (FIPS 140-3,
CNSA), résistance anticipée (migration vers SHA-3 ou BLAKE3), performance (BLAKE3 sur les
très gros blocs). Le changement en cours de projet est une migration complète, atomique et
journalisée — le re-cryptage : recalcul des empreintes, re-chiffrement des fragments,
re-signature de la carte, archivage de l'ancienne version (dépréciée, jamais détruite en
silence).

La phrase secrète maîtresse traverse Argon2id — mémoire d'au moins 64 Mio, au moins trois
itérations, parallélisme unitaire — pour produire la clé maîtresse ; les clés de chaque
fragment en sont dérivées par HKDF avec un contexte distinct par fragment et par
génération. Les sauvegardes suivent la règle 3-2-1 chiffrée, et l'escrow de la clé
maîtresse peut recourir à un partage de secret deux-sur-trois pour éliminer le point de
défaillance unique. La rotation des clés entraîne une re-signature complète de la carte —
opération atomique, journalisée, vérifiable après coup.

### 8.4 Export de continuité

La règle R1 interdit de livrer la carte avec l'artefact ; elle n'interdit pas au
développeur de détenir et transférer son propre état de développement. Sans mécanisme de
récupération, l'interdiction créerait un enfermement : le projet ne survivrait ni au
changement d'agent, ni au changement de poste. La v0.3 formalise donc l'**export de
continuité** : un conteneur unique, chiffré intégralement et signé, regroupant les couches
I, B et C complètes ainsi qu'un manifeste autodescriptif — version du protocole, suite
cryptographique, profils actifs, empreintes racine. Chiffré, l'export peut être stocké
n'importe où sans exposer la carte, ce qui satisfait la règle 3-2-1 ; signé, il est
vérifiable à l'import ; autodescriptif, il ne requiert aucune connaissance extérieure à
lui-même.

L'oracle est volontairement exclu du conteneur : éphémère par conception (D1), il est
régénéré depuis I à l'arrivée — l'export n'embarque ainsi aucun artefact empoisonnable
persistant, et sa surface d'attaque s'en trouve réduite d'autant. La procédure d'import,
exécutée par tout agent conforme TRIADE sur un poste ou un agent nouveau, comporte cinq
étapes : (1) déchiffrement par la phrase maîtresse — escrow deux-sur-trois si le contexte
est organisationnel ; (2) vérification de la signature, refus si invalide ; (3)
vérification du verrou croisé avec l'algorithme de l'en-tête ; (4) régénération de
l'oracle depuis I ; (5) reprise normale du développement — la boucle de mise à jour
s'applique à l'identique. Cette procédure garantit l'anti-enfermement : le développeur
peut changer d'agent à tout moment, sans perte et sans dépendance envers l'agent qui
l'a précédé.

## 9. Optimisation du coût en tokens

Le coût en tokens est le seul des quatre objectifs spécifique à l'ère agent-first. Il est
traité comme une contrainte d'ingénierie — budgets, mécanismes, instrumentation — toujours
subordonnée aux trois objectifs supérieurs : aucune économie de tokens ne justifie de
sauter une vérification. Le principe directeur : l'agent ne lit jamais le binaire en
entier ; la carte est son unique index, conçue pour être lue parcellairement (compacité du
format, chargement paresseux par fragment, cristallisation).

| Opération | Fragments et données lus | Budget |
|---|---|---|
| Localiser un bloc | frag-loc — une entrée | 40 tokens max |
| Éditer simplement un bloc | frag-loc + frag-con du bloc + notation du bloc | 3 000 tokens max |
| Ajouter un bloc | frag-loc + frag-con + seuils frag-prf | 6 000 tokens max |
| Audit complet (rare) | Carte entière déchiffrée | Non budgété — opération exceptionnelle |

Indicateurs de santé : précision de localisation (cible 95 % au jalon M0), coût moyen
d'une édition simple (cible 5 000 tokens), taux de régression post-patch (cible zéro,
rollback exclu). Le multi-profils n'altère pas ces budgets : l'entrée de localisation porte
le profil, et l'édition d'un bloc pour un nouveau profil relève du budget « ajouter ».

## 10. Profils de cible — universalité

La v0.2 fixait une cible unique — x86-64 / Windows 11 / PE32+ — et renvoyait la
portabilité à un objectif post-M5. La v0.3 généralise : le cœur du protocole — couches,
règles, boucle, vérification — est indépendant de la cible par construction, et tout ce qui
dépend de la cible est regroupé dans un **profil de cible**. L'universalité devient une
propriété structurelle : instancier une plateforme nouvelle revient à écrire un profil,
jamais à modifier le protocole.

Un profil définit obligatoirement sept éléments, qui font de l'extension une opération
vérifiable plutôt que déclarative : (1) l'ISA et la largeur de ses types — `usize`,
alignements, boutisme ; (2) l'ABI d'appel — registres de passage, volatilité, shadow space
ou zone rouge ; (3) le format d'exécutable et les protections à honorer — DEP/NX,
ASLR/PIE, CFI/CFG ; (4) l'interface système autorisée — IAT, syscalls, libc de la cible ;
(5) le mécanisme de patch à chaud natif — taille minimale de bascule atomique et procédure
d'invalidation du cache d'instructions ; (6) le moteur de notation et son vérificateur de
round-trip ; (7) la granularité des blocs et le padding garantissant les adresses stables
(R7).

| Profil | ISA | OS | Format | Interface | Statut |
|---|---|---|---|---|---|
| `x86-64-win11-pe` | x86-64 | Windows 11 | PE32+ | IAT (kernel32, ws2_32, Schannel) | Primaire — jalons M0-M5 |
| `x86-64-linux-elf64` | x86-64 | Linux | ELF64 | syscalls + libc | M6 — portabilité inter-OS |
| `riscv64-linux-elf64` | RISC-V 64 | Linux | ELF64 | syscalls + libc | M7 — portabilité inter-ISA |
| `aarch64-macos-macho` | AArch64 | macOS | Mach-O | libSystem | Réservé — hors feuille de route courante |
| `wasm32-wasi` | WebAssembly | WASI | module Wasm | WASI | Réservé — étude de niche |

L'identifiant d'un profil suit la convention `<isa>-<os>-<format>`. La correspondance des
couches est la suivante : la couche I est partagée par tous les profils du projet ; chaque
entrée de la carte porte son profil ; chaque profil possède son binaire, ses empreintes de
build et son registre de variantes dans frag-bld. « Sans compilateur » ne signifie pas «
sans système d'exploitation » — les interfaces sont appelées selon les conventions du
profil, comme tout binaire natif légitime.

### 10.1 Profil primaire : ABI Microsoft x64

| Convention | Règle |
|---|---|
| Passation des arguments | RCX, RDX, R8, R9, puis la pile — de droite à gauche |
| Valeur de retour | RAX (RDX pour une valeur de 128 bits) |
| Shadow space | 32 octets réservés par l'appelant avant chaque CALL |
| Registres volatils | RAX, RCX, RDX, R8 à R11 — détruits par l'appelé |
| Registres non volatils | RBX, RBP, RDI, RSI, R12 à R15 — préservés par l'appelé |
| Registres flottants | XMM0 à XMM5 volatils, XMM6 à XMM15 préservés |
| Alignement de pile | RSP multiple de 16 au point d'appel |
| Zone rouge | Aucune — contrairement à System V : stocker sous RSP sans allocation préalable est interdit |

L'absence de zone rouge est le piège classique pour qui vient de System V. La convention
interne du projet en tire les conséquences : R10 et R11 sont désignés registres de travail
internes — volatils selon l'ABI, donc jamais promis à un appelant ; aucune donnée vivante
ne séjourne entre RSP et RSP+32 au moment d'un appel ; tout bloc qui appelle une API
alloue son cadre avant d'y toucher. Ces règles internes sont portées par frag-con.

### 10.2 Format PE32+ minimal

L'exécutable est écrit à la main par l'agent, sans outil de liaison — preuve de maîtrise
du pipeline artefact exigée au jalon M0. Structure minimale : en-tête DOS et stub,
signature PE, en-tête COFF (machine 0x8664, quatre sections au maximum), en-tête optionnel
PE32+ (magic 0x20B, alignement de section 0x1000, caractéristiques DYNAMICBASE,
HIGH_ENTROPY_VA et NX_COMPAT activées), section `.text` en lecture-exécution, section
`.rdata` portant les imports et les relocations, table d'imports et table `.reloc` rendant
l'ASLR possible. Objectif de taille pour M0 : moins de 4 Kio.

### 10.3 Appels via IAT et protections du système

Les dépendances système du profil primaire se limitent à trois ensembles : kernel32 pour
les entrées-sorties, les threads et le tas ; ws2_32 pour le réseau à partir du jalon M2 ;
et Schannel via SSPI pour TLS au jalon M4. Les adresses ne sont jamais codées en dur :
chaque appel transite par la table d'imports, résolue par le chargeur — compatibilité
entre builds de Windows et ASLR respectés. Les protections du système sont honorées par
construction : DEP, puisque aucun code n'est jamais généré en pile ; ASLR, grâce aux
relocations ; Control Flow Guard, par la déclaration des cibles d'appel indirect valides.
L'objectif est assumé : un outil légitime par construction, dont la transparence
vis-à-vis du système est totale.

### 10.4 Différences entre profils — aperçu

| Élément | `x86-64-win11-pe` (primaire) | `x86-64-linux-elf64` (M6) | `riscv64-linux-elf64` (M7) |
|---|---|---|---|
| ABI | msx64 : RCX RDX R8 R9 ; shadow space 32 o. | SysV : RDI RSI RDX RCX R8 R9 ; zone rouge 128 o. | psABI RISC-V : a0-a7 |
| Format | PE32+ : DYNAMICBASE, HIGH_ENTROPY_VA, NX | ELF64 : PIE, RELRO, NX | ELF64 : PIE, RELRO, NX |
| Interface | IAT : kernel32, ws2_32, Schannel | syscalls + libc | syscalls + libc |
| Patch à chaud | trampoline 5/12 o., écriture alignée atomique | identique x86-64 | instructions de taille fixe : bascule par registre scratch + `fence.i` |
| Notation | keystone / capstone x86-64 | keystone / capstone x86-64 | keystone / capstone RISC-V |

Deux transitions méritent une vigilance documentée. Le passage Windows → Linux **inverse**
le piège de la zone rouge : ce qui était interdit sur msx64 (stocker sous RSP) redevient
permis sur SysV pour une fonction feuille — l'agent doit désapprendre le réflexe acquis sur
le profil primaire, et frag-con porte la convention effective de chaque bloc. Le passage
x86-64 → RISC-V change la nature du patch à chaud : sur une ISA à instructions de taille
fixe, il n'existe pas de trampoline relatif de 5 octets insérable n'importe où ; la bascule
passe par un registre scratch chargé de l'adresse cible, suivi d'une barrière
d'invalidation du cache d'instructions (`fence.i`) — le profil spécifie la séquence exacte
et son atomicité.

## 11. Feuille de route M0–M7

Huit jalons, chacun couvrant une capacité nouvelle et se terminant par des critères de
sortie mesurables — détail dans `docs/PLAN_MILESTONES.md`. Aucun jalon n'est franchi sans
que la carte soit signée, le verrou croisé vérifié et l'oracle passé. L'application cible —
un outil de pentest de type intercepteur MITM — est choisie comme stress test : réseau,
concurrence, parsing d'entrées non fiables et chiffrement, soit un large éventail de blocs
aux contrats très différents. Son usage est encadré : tests autorisés en environnement de
laboratoire, machine virtuelle isolée, autorité de certification de test installée
localement.

M0 est le jalon existentiel : il prouve que la chaîne notation, octets, exécutable,
exécution fonctionne de bout en bout sans compilateur. M2 est le jalon de vérité du
protocole : le patch à chaud sur code en cours d'exécution est la capacité qui a motivé
l'architecture de balises depuis la première discussion. M6 et M7, ajoutés par la v0.3,
valident l'universalité en isolant chaque variable : M6 change l'OS à ISA constante, M7
change d'ISA — ensemble, ils transforment la portabilité de promesse en propriété
démontrée.

## 12. Glossaire et journal des versions

| Terme | Définition |
|---|---|
| Carte | Couche C : index signé et chiffré liant intention et binaire, unique interface de développement de l'agent |
| Bloc | Unité de code machine de 32 à 512 instructions, une responsabilité, un point d'entrée stable |
| Scellage | Acte atomique d'engagement : écriture du bloc, mise à jour de la carte, inscription de l'empreinte |
| Cristallisation | Immuabilité d'un bloc après dix vérifications réussies ; modification dès lors soumise à procédure lourde |
| Oracle éphémère | Implémentation de référence triviale dérivée de la couche I, générée par session et détruite après usage |
| Verrou croisé | Contrôle bilatéral d'intégrité : empreintes des blocs dans la carte, signature de la carte, checksums au chargement |
| Contrat | Signature typée, pré et post-conditions et invariants publiés d'un bloc — la partie de I embarquée dans C |
| Fragment | Quart de carte chiffré séparément : localisation, contrats, preuves, builds |
| Profil de cible | Instanciation complète du protocole pour un couple ISA/OS : ABI, format, interface système, patch à chaud, notation, padding |
| Suite cryptographique | Paramètres de l'en-tête de carte — hachage, signature, chiffrement — choisis par le développeur dans une liste blanche |
| Re-cryptage | Migration atomique de la suite cryptographique : recalcul des empreintes, re-chiffrement, re-signature, archivage de l'ancienne carte |
| Export de continuité | Conteneur chiffré et signé regroupant I, B, C et un manifeste — seule forme de transfert de l'état de développement |
| Empreinte de build | Variante binaire unique par livraison et par profil, rendant toute fuite traçable |
| Vecteurs dorés | Jeu de tests de référence d'un bloc, conservé haché dans frag-prf |
| Notation | Représentation textuelle des instructions assemblées par le moteur du profil — un média, jamais un langage compilé |
| Round-trip | Contrôle de fidélité : assemblage puis désassemblage d'un bloc, comparaison exacte |

| Version | Date | Contenu |
|---|---|---|
| v0.1 | 25 oct. 2026 | Première ébauche : couches I/B/C, règles R1 à R7, boucle en sept étapes, feuille de route M0–M5 |
| v0.2 | 25 oct. 2026 | Décisions D1 à D10 ; sharding en quatre fragments chiffrés ; suite cryptographique (Ed25519, XChaCha20-Poly1305, Argon2id) ; règles R8 à R10 ; empreintes par build ; budgets en tokens ; spécification de la cible x86-64 / Windows 11 ; critères de sortie mesurables |
| v0.3 | 25 oct. 2026 | Universalité par profils de cible (D14, amende D10) ; suite cryptographique paramétrable — SHA-256 par défaut, liste blanche (D15, amende D5) ; export de continuité chiffré et signé (D16, précise R1) ; en-tête de carte normalisé ; jalons M6-M7 |

La présente version fige les arbitrages nécessaires au démarrage du jalon M0, qui s'effectue
sur le profil primaire. Les évolutions prévisibles — bloc optionnel de syscalls directs,
TLS 1.3 pur en blocs scellés, profils additionnels après M7 — sont volontairement hors du
périmètre courant afin que chaque addition s'appuie sur des résultats mesurés. La règle de
gouvernance reste celle du journal des décisions : toute évolution invalide explicitement
ce qu'elle remplace, et rien ne se change en silence.
