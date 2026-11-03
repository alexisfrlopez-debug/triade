# Couche I — v0.6.0 axe 3 : le sceau de l'Intention (D87)

Spécification écrite **avant** tout code (R2, provenance `écrite-avant-code`).
Elle instancie la décision D87 (filigrane cryptographique de l'Intention) et
s'intègre à la hiérarchie des trois gardes : (1) phrase de lignée — chiffre
les enveloppes de carte, menace « vol du dépôt au repos » ; (2) graine
Ed25519 **en ligne** — signe les cartes, atteste les FAITS (les octets
scellés) ; (3) **clé I hors-ligne** — signe l'INTENTION, atteste la VOLONTÉ
(le droit de faire évoluer). La clé (3) est le seul des trois secrets que le
bac à sable de l'assistant ne verra **jamais** (discipline D30 « graine
jamais confiée », étendue du sceau de carte au sceau d'intention).

Ce que le sceau I établit : voler le binaire (couche B), le dépôt (B+C), et
même les clés du poste (phrase de lignée, graine de carte — scénario D76 déjà
vécu) ne permet **pas** de produire une évolution valide de l'intention :
l'oracle et le verrou croisé rejettent toute couche I non signée par la clé
physique du développeur. Le code volé ne peut pas évoluer.

## 1. Périmètre — les arbres signés

Un **arbre d'intention** est un répertoire `<lignée>/I/` du dépôt : ses
fichiers `.md` (registre figé + spécifications + README transverse). Onze
arbres vivent sous le sceau — les neuf lignées existantes à l'ouverture de
l'axe, PLUS l'arbre des axes eux-mêmes (`v06/I`) : la spécification qui
définit le sceau est la première couche I qu'il garde (un mécanisme de
garde qui s'exempte de lui-même serait une contrebande de niveau X2) ;
la table lie chaque arbre à son artefact et à sa balise de référence.
L'arbre `m5/I` — les trois révisions R3 du relèvement http→https,
écrites-avant-code (D136) — entre au sceau à la cérémonie 0.6.0 : le
périmètre ne grandit que signé (même modèle que l'entrée de CF3 à la
re-cérémonie D126).

| Arbre | Artefact | Balise de référence |
|---|---|---|
| `m0/I` | hello.exe | 0.1.0 (M0) |
| `m1/I` | minilibc (hello/selftest/echo) | 0.2.0 (M1, scellée) |
| `m2/I` | echo.exe + tcp | 0.3.0 (M2, scellée) |
| `m3/I` | proxy.exe | 0.4.0 (M3, scellée) |
| `m4/I` | proxy.exe (tunnel) | 0.5.0 (M4, scellée) |
| `m5/I` | proxy.exe (relèvement https) | 0.6.0 (M5, cérémonie 0.6.0 — D136) |
| `m6/I` | hachoir (lignée D34) | hachoir.1 |
| `m7/I` | sceau (lignée D34) | sceau.1 |
| `demo/I` | demo.exe | 0.3.0 (M2, scellée) |
| `terrain/I` | superviseur.exe | terrain.19/17-H (0.5.0-terrain.9) |
| `v06/I` | coffre CF2 + CF3 + sceau-I (transversal) | v0.6.0 axes 2-3-4 (D105/D106/D121) |

L'arbre `v06/I` porte les spécifications transversales du programme v0.6.0 :
ce README (axe 3, sceau de l'Intention — D87/D105) ET `CF2/README.md`
(axe 2, coffre CF2 et interrupteur d'homme mort — D86/D106) ET
`CF3/README.md` (axe 4, coffre CF3 : la serrure à triple scellement et le
cycle en deux actes — D121, entré à la re-cérémonie D126 avec l'erratum
§ 12 du README CF2) : la volonté d'évolution couvre le programme souverain
ENTIER, axes 2, 3 et 4 ensemble.

La balise est **informative dans le manifeste mais couverte par la
signature** : changer l'étiquette sans re-signer est un diff d'intention
rejeté comme tout autre. Hors périmètre D105 : les sources de la
spécification elle-même (`docs/`) — elles seront signées à leur propre
version quand PROTOCOLE_TRIADE passera à v0.6.0 (modèle par-version, même
mécanisme) ; les artefacts binaires, déjà couverts par le verrou croisé R8
des cartes (le sceau I ne duplique JAMAIS une preuve existante — défaut X2).

## 2. Le manifeste ordonné (source unique de l'empreinte)

Pour un arbre donné, le manifeste est le texte canonique suivant (UTF-8,
fins de ligne LF, ordre TOTAL : tri lexicographique du chemin relatif POSIX
— le tri est DÉTERMINISTE, indépendant du système de fichiers et de la
locale ; le même arbre produit le même manifeste sur toute machine) :

```
TRIADE-SCEAU-I v1
arbre: m4
artefact: proxy.exe
balise: 0.5.0
fichiers: 12
sha256:<64 hexdécimaux minuscules>  tls-01-nom-utf16.md
sha256:<64 hexdécimaux minuscules>  tls-02-verdicts.md
…
```

Règles :

1. **Tous les fichiers réguliers** de l'arbre sont listés (aujourd'hui tous
   `.md` ; tout fichier nouveau — quelle que soit son extension — entre au
   manifeste au prochain `preparer` : un ajout non signé est un diff
   d'intention, refusé comme une modification).
2. Chaque ligne fichier porte le SHA-256 du contenu **canonique LF** :
   toute paire `\r\n` est normalisée en `\n` avant condensé — la
   représentation du checkout (Windows `autocrlf` porte CRLF ; le dépôt
   git porte LF) n'est pas l'intention. D115 : la cérémonie de terrain
   D113 avait signé des empreintes CRLF, la vérification à froid sur un
   clone LF dénonçait les dix arbres CODE 10, signatures pourtant
   valides. Hexadécimal minuscule, **deux espaces** après le condensé
   (canon `sha256sum`-compatible en lecture humaine).
3. Répertoires vides, liens symboliques et fichiers spéciaux : **refus de
   préparation** (fail-closed — un arbre d'intention n'est pas un espace
   arbitraire ; un lien symbolique serait une échappée hors de l'arbre).
4. L'**empreinte d'arbre** est le SHA-256 du texte du manifeste ENTIER
   (l'en-tête compris) : elle couvre l'identité (arbre/artefact/balise), le
   décompte et chaque fichier. Aucun champ n'est hors signature.

## 3. La signature (Ed25519, RFC 8032)

- Algorithme : **Ed25519** (EdDSA sur Edwards25519, SHA-512) — cohérent avec
  le sceau de carte (D4 : Ed25519 auto-porté, X.509/PGP rejetés).
- La signature couvre le **message de 32 octets** `empreinte d'arbre` (le
  SHA-256 du manifeste). Le message signé est donc court et **imprimable sur
  papier** : la cérémonie hors-ligne manipule des charges utiles de quelques
  lignes hexadécimales, jamais le dépôt.
- Clé privée : graine de 32 octets (encodage hexadécimal minimal — pas de
  format conteneur, pas de métadonnées). Clé publique : 32 octets.
- Dépôt côté vérification : `cryptography` (déjà dépendance du projet) ;
  cérémonie hors-ligne : implémentation **pur Python standard seul** —
  aucune dépendance, aucun réseau, exécutable sur toute machine Python 3.8+
  y compris hors ligne (c'est le point : le script doit tourner SANS le bac
  à sable et SANS pip). Les deux implémentations sont croisées par les
  vecteurs RFC 8032 et par interopérabilité bidirectionnelle — la leçon
  D102 s'applique : deux implémentations d'accord entre elles ne prouvent
  rien contre la spécification ; **les vecteurs RFC sont le témoin
  byte-level**, chaque signature produite en cérémonie est vérifiée par les
  DEUX avant remise.

## 4. La cérémonie hors-ligne (ce que le bac à sable ne verra jamais)

Le script `v06/ceremonie_hors_ligne.py` est **autoporteur** (une copie
vivra dans `download/` pour exécution sans le dépôt). Trois modes :

1. `generer` — produit une graine Ed25519 depuis `os.urandom` (aucune autre
   source d'aléa), l'écrit dans `cle-I-privee.txt` (0600) avec mode d'emploi
   de garde (support papier : la graine est 64 caractères hexadécimaux),
   et `cle-publique-I.txt`. Aucun affichage de la graine n'est requis ; le
   fichier EST la remise.
2. `signer <a-signer.txt> <cle-I-privee.txt>` — lit les lignes
   `arbre balise empreinte` du fichier à signer (copié depuis le dépôt sur
   papier ou clef USB), signe chaque empreinte, écrit `signatures-I.txt`
   (`arbre balise signature`), VÉRIFIE chaque signature avec la clé publique
   correspondante avant écrire (une cérémonie qui rend une signature
   invérifiable est un échec nommé, exit ≠ 0).
3. `verifier <a-signer.txt> <signatures-I.txt> <cle-publique-I.txt>` —
   re-vérification autonome (l'outil du développeur pour auditer une remise
   avant de la confier au dépôt).

Flux air-gap : le dépôt produit `a-signer.txt` (une ligne par arbre) ; le
développeur le transporte hors ligne ; la clé et les signatures reviennent
au dépôt (`v06/sceau-I/`). Le dépôt ne voit JAMAIS la graine. L'horodatage
de première intention : la date du commit signé git (alternative D87 :
horodatage tiers rejeté).

## 5. Le dépôt porte la preuve (`v06/sceau-I/`)

```
v06/sceau-I/
  cle-publique-I.txt      # 64 hex — la clé publique DE LA GARDE COURANTE
  a-signer.txt            # la charge utile de la cérémonie courante
  manifestes/<arbre>.txt  # le manifeste canonique signé (transparence + audit)
  signatures/<arbre>.txt  # 128 hex — une signature par arbre
```

Rotation de clé : remplacer `cle-publique-I.txt` ET toutes les signatures
dans le MÊME commit (une clé publique sans signatures couvertes est un état
incohérent, refusé par `verifier`). La rotation consignée au journal de
travail — modèle des cérémonies de lignée existantes (§ 15.3).

## 6. La vérification (outil du dépôt : `v06/sceau_I.py`)

`python3 v06/sceau_I.py preparer|deposer|signer-test|verifier|etat` :

- **preparer** — reconstruit le manifeste de chaque arbre depuis le dépôt
  vivant, le compare à `manifestes/<arbre>.txt`, écrit `a-signer.txt`
  (empreintes courantes). Un arbre divergé de son manifeste signé est
  RAPPORTÉ nommément (divergence d'intention en attente de signature — c'est
  le signal du développeur : « quelqu'un a fait évoluer l'intention »).
- **deposer** — installe une remise de cérémonie (`signatures-I.txt`,
  éventuellement `--cle cle-publique-I.txt` pour la rotation réelle) :
  chaque signature est VÉRIFIÉE contre l'arbre vivant et la clé AVANT toute
  écriture (une remise invérifiable n'écrit RIEN — atomicité de cérémonie) ;
  une remise incomplète est refusée (la rotation couvre TOUS les arbres).
- **signer-test** — signe avec la clé de TEST du laboratoire (§ 8) : flux
  complet à vide, jamais présenté comme cérémonie réelle.
- **verifier** — la GARDIENNE : pour chaque arbre, recalcul du manifeste
  depuis l'arbre VIVANT, comparaison au manifeste déposé, re-hachage,
  vérification Ed25519 de la signature contre la clé publique déposée.
  **Codes de sortie nommés** : 0 = tout vert ; 10 = arbre divergé de son
  manifeste signé (diff d'intention non signé) ; 11 = signature invalide ;
  12 = dépôt incohérent (signature manquante, clé incohérente). Fail-closed
  intégral : toute anomalie de format est un refus, jamais un avertissement.
- **etat** — lecture seule : table des arbres, empreintes, état
  (signé/divergé), sans code d'échec (outil d'audit, pas garde).

## 7. Les gardes dans la chaîne (ce que le sceau I FERME)

1. **Chaîne de build** : `m4/build_m4.py` et `terrain/build_terrain.py`
   appellent la garde au plus tôt (après l'anti-rollback, avant tout
   assemblage) : un arbre d'intention divergé de sa signature **refuse le
   build** (exit nommé, message citant l'arbre et le fichier divergent).
   L'héritage M3 reste couvert par sa propre garde d'arbre (`m3/I` signé).
2. **Chemin de patch** : tout script qui modifie une couche I (révision de
   spécification, nouveau bloc) DOIT appeler la garde en sortie — le diff
   non signé est refusé. Les patchs BINAIRES historiques
   (`scripts/patch_terrain*.py`) ne touchent que la couche B : ils restent
   hors périmètre (le binaire est déjà la garde de la carte) ; la leçon
   D103 (un correctif qui ne vit pas dans la source ne survit pas à une
   reconstruction) s'applique : la garde vit dans la SOURCE des chaînes.
3. **Ce que la garde n'est pas** : elle ne protège pas contre un attaquant
   qui réécrit l'arbre ET le manifeste ET la signature ET la clé publique
   (cette menace est celle du vol de dépôt AVEC réécriture d'historique —
   elle appartient à la phrase de lignée et au dépôt git signé ; trois
   gardes, trois menaces, D87). Elle protège la seule chose qu'aucune autre
   garde ne protège : **l'évolution de l'intention sans la clé physique**.

## 8. La clé de TEST (phase laboratoire, honnêteté consignée)

Tant que le développeur n'a pas exécuté la cérémonie réelle, le dépôt porte
des signatures de **clé de TEST** — dérivée de façon DÉTERMINISTE d'une
constante PUBLIQUE du projet (une clé de test n'est un secret pour personne :
sa non-sécurité est CONSIGNÉE et visible — c'est la preuve permanente de
l'état laboratoire ; la dérivation publique garantit en outre que l'état
test survit à toute réinitialisation du bac à sable), étiquetée
`test` dans `v06/sceau-I/etat-cle.txt` (remplacement requis). La mécanique
est alors ENTIÈREMENT prouvée (falsification,
garde de build, refus de diff non signé) mais la souveraineté n'est PAS
encore armée : le bac à sable peut re-signer. L'état `test` est consigné
par `etat` et répété dans le tableau de bord ; la cérémonie réelle le
remplace (rotation § 5). Mentir sur cette phase serait le défaut X8
(affirmer une preuve non faite) — l'état est VISIBLE, toujours.

## 9. Critère de sortie D87 — correspondance

| Exigence D87 | Où elle vit |
|---|---|
| Cérémonie de génération hors-ligne documentée (script + mode d'emploi exécutable sans l'assistant) | `v06/ceremonie_hors_ligne.py` + `download/LISEZMOI-cle-I.txt` |
| Le dépôt vérifie la signature I de tous les jalons scellés | `v06/sceau_I.py verifier` — 10 arbres, gardes build_m4/build_terrain |
| Falsification d'un octet d'un `.md` de couche I rejetée | `v06/test_sceau_I.py` F2 — un octet par arbre, 10/10 |
| Un diff d'intention non signé refusé par le chemin de patch | `v06/test_sceau_I.py` F3 — ajout/modification/suppression, garde de build |

La falsifiabilité est la PREUVE : une garde qui ne rejette rien ne garde
rien (leçon M3). Toute mutation doit être attrapée, tout passage silencieux
est un échec de test — zéro tolérance.
