# Couche I — v0.6.0 axe 2 : le coffre CF2 et l'interrupteur d'homme mort (D86)

Spécification écrite **avant** tout code (R2, provenance `écrite-avant-code`).
Elle instancie la décision D86 (interrupteur d'homme mort du coffre, Shamir,
destruction des fragments) et complète la hiérarchie des gardes établie par
D87 : (1) phrase de lignée — chiffre les enveloppes de carte ; (2) graine
Ed25519 en ligne — signe les cartes (les FAITS) ; (3) clé I hors-ligne —
signe l'intention (la VOLONTÉ). Le présent axe arme une **quatrième garde** :
la **clave** du coffre — une clé maîtresse **jamais stockée entière**, qui ne
vit que reconstituée en RAM le temps d'un déverrouillage.

Ce que CF2 établit : l'adversaire qui s'empare du dépôt (cartes et artefacts,
couche C) pendant que la machine vit perd le coffre **dans le même mouvement**
— la sentinelle brûle les fragments à la lecture non blanchie, le conteneur
devient indéchiffrable (Shamir sous le seuil : sécurité **informationnelle**,
pas computationnelle). Le code volé reste inexploitable : les enveloppes de
carte sont mortes avec le coffre. La contrepartie — une fausse alerte est une
perte auto-infligée — est arbitrée par le double seuil (§ 6) et appartient au
développeur (§ 12).

## 1. Périmètre

Sous le sceau : le conteneur **TRIADE-CF2** (format § 3), le découpage
**Shamir** (§ 2), les **fragments** (format § 4), les **gardes** (§ 5), la
**sentinelle** (§ 6), la **destruction** (§ 7), l'outil et la discipline RAM
(§ 8), la restauration (§ 10). Hors périmètre D106 : le moteur Windows réel
d'audit d'accès (SACL/ETW — **exigence consignée** § 9, même posture que
l'axe 1 D85 : l'infrastructure du bac à sable ne peut pas la satisfaire et le
dit) ; la migration du coffre RÉEL du développeur (cérémonie § 12, livrée par
`download/LISEZMOI-coffre-CF2.txt` — le bac à sable ne touchera JAMAIS le
conteneur ni les phrases réels).

L'adversaire modélisé (borne consignée, D86) : processus tiers aux privilèges
**utilisateur** — l'agent d'audit de l'employeur, un outil concurrent. PAS un
attaquant admin/noyau qui gèle la machine (édition froide) : une sentinelle
userland peut être tuée avant d'agir. La garantie honnête : la sentinelle
brûle **tant qu'elle vit** ; la fenêtre détection→destruction est mesurée et
consignée (§ 11).

## 2. Le secret maître et Shamir (normatif)

- **M** : 32 octets issus du CSPRNG (`os.urandom`). M n'est JAMAIS écrit
  entier — nulle part, jamais, ni journal, ni temporaire, ni variable
  persistante. M ne vit que reconstitué en RAM, le temps d'un déverrouillage,
  puis effacé au mieux de Python (§ 8).
- **Champ** : GF(2^8), polynôme générateur **0x11B** (le polynôme d'AES —
  le plus éprouvé de la littérature). Addition = XOR. Évaluation de f(x) par
  Horner ; interpolation de Lagrange en x = 0.
- **Découpage** : pour CHACUN des 32 octets de M, un polynôme distinct
  f(X) = s + a₁X + … + a_{T−1}X^{T−1} dont les T−1 coefficients sont **des
  octets frais du CSPRNG** (jamais réutilisés d'un octet à l'autre — la
  corrélation entre polynômes serait une fuite). Le fragment j porte le
  vecteur [f_j(b₀) … f_j(b₃₁)] : 32 octets, aucun coefficient, aucune
  matière prédictive sur M seul.
- **Indices** : x_j ∈ {1 … N} tous distincts, non nuls. Bornes : 2 ≤ T ≤ N
  ≤ 255. Un seuil T = 1 est REFUSÉ (aucune distribution : la « garde » serait
  une clé unique — l'alternative rejetée par D86).
- **Reconstitution** : Lagrange sur T fragments VALIDES distincts (le choix
  canonique : les T plus petits x valides, dans l'ordre — déterminisme
  documenté). Toute reconstitution est VERIFIÉE contre le champ `verif` de
  l'en-tête (§ 3) AVANT toute interprétation du chiffretexte : un fragment
  faux ou corrompu est un refus NOMMÉ (§ 4), jamais un silence.
- **Sécurité** : sous T fragments, la sécurité est **informationnelle** —
  tout M' de 32 octets reste compatible avec les fragments présents, aucune
  hypothèse computationnelle. C'est la propriété qui fait de la destruction
  une mort, pas une révocation.

## 3. Format conteneur « TRIADE-CF2 » (normatif)

Même discipline que CF1 (§ 11.2) — autodescriptif, fail-closed, écriture
atomique. La différence est la CÉRÉMONIE de la clé : CF1 dérive d'une phrase
(Argon2id) ; CF2 dérive d'un secret maître réparti.

```
magic « TRIADE-CF2 » (10 o) · version u16 (1) ·
champs longueur-préfixée u16 : hachage (sha256), kdf (hkdf-sha256),
                               chiffrement (xchacha20poly1305),
                               date ISO-8601 UTC, shamir (« t=3/n=5 ») ·
sel HKDF 32 o (aléatoire à l'init) · nonce 24 o (aléatoire à CHAQUE écriture) ·
empreinte sha256 du chiffretexte 32 o ·
verif 16 o = sha256(HKDF(M, sel, info « cf2=verif »)) tronqué ·
chiffretexte : XChaCha20-Poly1305(JSON base, K, AAD = tout ce qui précède)
   avec K = HKDF-SHA256(M, sel = sel du conteneur, info « coffre=v2 », L=32)
```

La base déchiffrée est le MÊME JSON que CF1 (`{format, protocole, cree,
modifie, projets}` — la migration § 10 ne traduit rien). Dérivation à
contexte **distinct** de CF1 (`coffre=v2` vs `coffre=v1`) et des fragments de
carte : nul chevauchement de clé. `verif` est la VERIFICATION NOMMÉE de la
reconstitution : 16 o suffisants pour que la probabilité d'un faux M accepté
soit 2⁻¹²⁸ — et l'AEAD re-verrouille derrière. Toute anomalie de parsing,
d'algorithme (liste blanche de l'en-tête), d'empreinte, de `verif` ou de tag
AEAD est un refus terminal — rien n'est interprété (fail-closed). Écriture
atomique (tmp + `os.replace` + fsync, 0600, répertoire 0700).

## 4. Format fragment « TRIADE-CF2-FRAG » (normatif)

ASCII autodescriptif, transportable **sur papier** (l'exfiltration d'un
fragment est un vol physique — hors modèle) :

```
TRIADE-CF2-FRAG v1
coffre: <sel HKDF du conteneur, 64 hex — l'identité STABLE du coffre>
x: <indice, décimal>
seuil: t=3/n=5
fragment: <64 hex — 32 o>
tag: <16 hex — sha256("TRIADE-CF2-frag" || x || fragment) tronqué à 8 o>
```

Le fragment lie au **SEL du coffre** — identité stable par construction
(posé à l'init, inchangé d'écriture en écriture, rotation seulement au
re-chiffrement intégral) — et JAMAIS à l'empreinte de l'en-tête : le nonce
est frais à CHAQUE écriture, une liaison à l'en-tête invaliderait les
copies papier à chaque `ajouter`/`retirer` (faute dénoncée par le parcours
CLI complet — consignée D106). Le `tag` nomme le fragment fautif SANS le
divulguer (préimage résistante) : corruption, mélange de fragments d'un
autre coffre (sel divergent), collision d'indice — refus nommés à l'import
comme à la reconstitution. Le fragment n'est accepté dans une garde que si
tag ET sel du coffre sont verts (§ 10 — atomicité).

## 5. Les gardes

Une garde est un **répertoire distinct** portant UN fragment, mode 0700. En
production : gardes à **ACL distinctes** (répertoires frères à propriétaires
différents) et, autant que possible, **supports séparés** (une garde sur
clé USB détachable) — un seul processus compromis ne lit pas toutes les
gardes, un seul support perdu n'emporte pas le seuil. En laboratoire : N
répertoires frères distincts (la ACL est simulée par la séparation des
chemins — consigné, la vraie ACL est une affaire de déploiement Windows).
Configuration partagée outil/sentinelle : JSON (`gardes`, `couche_c`,
`liste_blanche`, `periode_sondage`, `journal`, `pv_dir` — § 6). Valeurs par
défaut du laboratoire : **N = 5, T = 3** (l'arbitrage PERTE vs
EXPROPRIATION appartient au développeur et sera consigné avec la
configuration retenue — D86 ; la valeur par défaut donne : brûler les 5
gardes machine = mort ; la RELÈVE exige **T copies hors-ligne** — TROIS à
seuil 3 : deux copies laisseraient le coffre mort, l'autotest le prouve
par restauration partielle refusée).

## 6. La sentinelle (normatif)

Un processus userland, long terme, qui SURVEILLE LA COUCHE C (répertoires de
cartes et artefacts listés dans la configuration — JAMAIS les gardes ni le
conteneur).

**Double seuil** (deux signaux INDÉPENDANTS, tous deux requis — la fausse
alerte est une perte auto-infligée) :
1. **processus hors liste blanche** — résolution par `/proc/<pid>/exe` et
   `/proc/<pid>/cmdline` (production Windows : image du processus, SACL) ;
2. **lecture de CONTENU** — un descripteur ouvert en lecture sur un FICHIER
   de la couche C (une ouverture d'attribut — `stat`, listage de répertoire
   — n'est PAS un signal : elle n'ouvre pas de descripteur de fichier).

**Moteur de laboratoire** (Linux, non privilégié — l'utilisateur `z` du bac
à sable n'a pas CAP_SYS_ADMIN, `fanotify_init` rend EPERM : consigné, testé) :
- **inotify** (ctypes, autoporté) sur les répertoires de la couche C :
  `IN_OPEN|IN_ACCESS` sur FICHIER (les événements `IN_ISDIR` ne comptent
  pas) déclenchent UN BALAYAGE IMMÉDIAT — la latence de détection ne dépend
  pas de la période de sondage ;
- **balayage /proc** : à chaque événement (et périodiquement — robustesse),
  lecture de `/proc/*/fd/*` : tout descripteur pointant dans la couche C
  attribue la lecture à son pid ; résolution exe/cmdline ; BLANC → journal
  « blanchi » ; NON BLANC → **les deux seuils sont réunis → destruction (§ 7)** ;
- **lecture non attribuée** (le lecteur a refermé avant le balayage) :
  journalée, comptée, **PAS brûlée** — un seul signal, la discipline du
  double seuil prime sur l'activation ; la fenêtre résiduelle est consignée
  (§ 11).

**Moteur de production Windows** (exigence consignée, non codée — § 9) :
SACL « lecture » sur les répertoires de couche C + surveillance du journal
d'événements de sécurité (4663 « An attempt was made to access an object »),
ou ETW file-I/O ; même double seuil, même liste blanche.

**Liste blanche minimale** (D86) : les chaînes de build, les vérificateurs,
l'éditeur du développeur, la sentinelle elle-même. Mécanisme : motifs
regex sur le chemin d'image RÉSOLU **et** sur la ligne de commande complète —
un motif ne blanchit JAMAIS « tout python3 » : c'est la ligne de commande qui
distingue `build_m4.py` d'un `-c` jetable.

**Test de santé** : la sentinelle bat un heart-beat (horodatage + fragments
présents par garde) à chaque boucle ; `sante` vérifie la fraîcheur (une
sentinelle morte est un avertissement nominal, pas un décès du coffre —
la clé ne peut pas être lue par une sentinelle morte).

## 7. La destruction (normatif)

`bruler` — la MÊME routine pour la sentinelle et la commande manuelle
(source unique de vérité, chargée par chemin — motif sceau-I/D105) :

1. pour chaque garde, pour chaque fichier fragment présent : **trois passes**
   d'écrasement (octets aléatoires CSPRNG, puis 0xFF, puis 0x00), `fsync`
   après CHAQUE passe ;
2. troncature à zéro, `fsync`, renommage vers un nom aléatoire, `unlink`,
   `fsync` du répertoire ;
3. **procès-verbal** de destruction : date, déclencheur (pid, image, fichier
   lu — l'évidence nommée), fragments détruits (chemins, tailles, passes),
   version de la sentinelle — le développeur SAIT qu'il doit restaurer (§ 10) ;
4. le conteneur et les gardes vides restent sur place : c'est le PV qui dit
   la mort, la vérification (§ 8) qui la confirme — sous le seuil,
   indéchiffrable, preuve informationnelle § 2.

Sur SSD : un `TRIM` de la zone est la parade à l'usure cellulaire (fstrim
système, ou l'équivalent Windows `FSCTL_SET_ZERO_DATA` + TRIM au
déploiement) — consigné comme exigence de déploiement, non exécutable en
portable ; sur systèmes CoW (ZFS/btrfs, instantanés), l'écrasement
logique ne garantit pas la mort des copies physiques : la spec L'ÉCRIT
(§ 11) — le laboratoire est ext4/overlayfs, l'écrasement y est effectif.

## 8. L'outil et la discipline RAM

`v06/coffre_cf2.py` : `init` (conteneur + fragments, laboratoire),
`migrer` (CF1 → CF2, § 10), `statut` (en-tête seul, aucune clé),
`etat-fragments` (gardes présentes / seuil), `lister`, `obtenir`,
`ajouter`, `retirer`, `verifier` (intégrité complète, reconstitution
contrôlée), `restaurer` (§ 10), `bruler` (§ 7), `autotest` (autocontrôles,
répertoire temporaire, AUCUN coffre réel touché).

Chaque opération qui déverrouille : lit les fragments présents, retient les
T plus petits x valides, reconstitue M dans un `bytearray`, dérive K,
vérifie `verif` + AEAD, opère, re-chiffre (nonce frais) si écriture, puis
**efface M et K** (affectation à zéro du buffer, `del`) — au mieux de
Python : les `bytes` immuables interdisent la garantie native
(`SecureZeroMemory` au déploiement Windows) ; la limite est CONSIGNÉE, pas
niée (§ 11). Aucun M, K, fragment ou phrase n'entre jamais dans un journal,
un PV ou une sortie.

## 9. Le moteur Windows réel (exigence consignée)

Même posture que l'axe 1 (D85) : l'exigence est consignée, l'infrastructure
du bac à sable ne peut pas la satisfaire et le dit. Au déploiement :
SACL par fichier/répertoire de couche C (succès : lecture de données),
journal Sécurité 4663 avec image du processus, ou ETW (manifeste
FileIo/Read) ; la sentinelle Windows reprend EXACTEMENT le double seuil, la
liste blanche et la routine de destruction du laboratoire — seule la source
d'événements change. Latence cible : < 1 s (l'événement 4663 est poussé,
pas sondé).

## 10. Restauration et migration

- **restaurer FICHIER…** : remise de copies hors-ligne dans les gardes.
  Chaque fragment importé est vérifié (tag § 4 + empreinte conteneur +
  indice non déjà présent) ; la remise est **ATOMIQUE** : toute anomalie et
  RIEN n'est écrit (motif D105 [11] — une remise partielle est un coffre
  menteur). Le PV de destruction archivé marque la relève.
- **migrer** : lit le conteneur CF1 (phrase de contrôle — la cérémonie du
  développeur, cf. `download/LISEZMOI-coffre-CF2.txt`), ré-encrypte la base
  sous M + Shamir, écrit conteneur + fragments, **laisse CF1 intact** : la
  destruction de l'ancien est un acte explicite du développeur après
  vérification. Le laboratoire prouve le flux sur un coffre CF1 de test.

## 11. Bornes honnêtes (consignées, aucune cachée)

1. **Fenêtre résiduelle** : une lecture de fichier < ~10 ms peut refermer
   avant attribution — journalée « non attribuée », non brûlée (double
   seuil). Une exfiltration RÉELLE (copie d'arbre, secondes) est garantie
   attrapée : c'est le scénario de sortie D86, testé avec latence bornée.
2. **Sentinelle tuable** : l'adversaire utilisateur peut tuer la sentinelle
   AVANT la destruction — hors garantie (borne D86 consignée) ; le
   heart-beat rend la mort VISIBLE.
3. **Zéroïsation Python** : au mieux de Python (§ 8) — la garantie native
   exige le déploiement Windows.
4. **CoW/instantanés** : § 7 — l'écrasement logique ne tue pas les copies
   physiques sur ZFS/btrfs ; ext4/overlayfs au laboratoire.
5. **Attribution par ligne de commande** : un motif trop large
   (« python3 ») blanchit l'adversaire — la liste blanche est MINIMALE et
   les motifs sont sur la ligne complète, testés par falsifiabilité.

## 12. Phase laboratoire / cérémonie réelle

Le laboratoire livre la mécanique COMPLÈTE (conteneur, Shamir, gardes,
sentinelle, destruction, restauration, migration) prouvée par
falsifiabilité (`v06/test_cf2.py`, § 13) sur des coffres de TEST — le
conteneur réel `.keys/coffre_fort.bin` et les phrases réelles ne sont
JAMAIS touchés (discipline D105 : aucune clé touchée). L'acte qui arme la
protection réelle appartient au développeur : `migrer` + copies hors-ligne
de 2 fragments + `sentinelle demarrer` — le flux pas à pas vit dans
`download/LISEZMOI-coffre-CF2.txt`.

## 13. Critères de sortie D86 → tests

| Critère D86 | Preuve (`test_cf2.py`) |
|---|---|
| Shamir : reconstitution, seuil, refus nommés | T1 (KAT + 1 000 vecteurs, interop exhaustive C(5,3)) |
| sous T : informationnellement mort | T2 (M′ arbitraire accepté par les fragments seuls — aucune discrimination) |
| conteneur : round-trip + fail-closed | T3 (en-tête, AEAD, verif, empreinte — refus nommés) |
| exfiltration simulée → fragments détruits, indéchiffrable | F1 (sentinelle en sous-processus, lecture non blanchie, PV + mort du coffre, restauration → vie : le cycle complet) |
| fausses alertes NULLES en essai nominal | T4 (opérations blanches — build/vérificateur simulés — journal « blanchi », zéro brûlage) |
| latence détection→destruction bornée | F1 (mesurée, assertée < borne consignée) |
| remise douteuse refusée sans écrire | F2 (atomicité, octet pour octet) |
| santé de la sentinelle | T5 (heart-beat frais, mort visible) |

La sortie honnête : tout échec est NOMMÉ (le fichier, l'octet, le fragment
fautif) — un verdict muet n'est pas une preuve (leçon M3).
