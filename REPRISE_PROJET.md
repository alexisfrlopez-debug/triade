# REPRISE DU PROJET TRIADE — Fichier d'instruction

> Objet : reprendre le projet TRIADE là où il s'est arrêté, le plus vite
> possible, sans relire l'historique. Ce fichier est auto-suffisant. Il
> s'adresse autant au développeur qu'à un agent IA chargé de continuer.
> REDESSINÉ à la vague 14 (22/11/2026, la demande du maître) : le système
> des VAGUES d'instructions, la restauration du bac, la chaîne de release.

## 1. Le projet en 30 secondes

TRIADE est un protocole où un agent IA écrit du CODE MACHINE NATIF PUR
(x86-64, RISC-V, TLS 1.3) à la main, guidé par des spécifications signées
(couche I) et une carte chiffrée (couche C) verrouillée aux octets (couche
B). Trois couches indissociables ; priorités lexicographiques
**Sécurité > Performance > Optimisation > Coût en tokens**. Le dossier
publie des ÉDITIONS académiques (manuscrit, spécification, Livre du
Coffre, preuves, présentation) au DOI Zenodo
**10.5281/zenodo.24367343** (concept ; v0.23.0 = record 24438614).

## 2. LE RYTHME : LES VAGUES D'INSTRUCTIONS (le cœur de la reprise)

Le maître dépose des instructions au dossier **`instructions`** du coffre
Drive (le lien « nouvelles instructions ici, à archiver après
exécution »). Chaque vague = 6 instructions environ (fichiers
`Qwen__AAAAMMJJ_<code>.txt`). La session d'une vague :

1. **RESTAURER LE BAC** (§ 3) ;
2. **GELER LES PLANS** : un `PLAN-<CODE>.md` par instruction + la table
   `EMPREINTES-PLANS-VAGUE<N>.txt` (sha256) — COMMIT AVANT TOUTE DONNÉE
   (la règle reconduite des vagues 8-13) ;
3. **EXÉCUTER** chaque atelier `atelier-<nom>-<code>/` (un commit par
   atelier, sceau 14/14 avant/après : `python3 v06/sceau_I.py verifier`) ;
4. **ARCHIVER LES INSTRUCTIONS** : copie au dépôt
   `ARCHIVE/instructions_vague<N>_<AAAAMMJJ>/` (recoupée byte-byte), AU
   COFFRE le geste en deux étapes (retirer du `/instructions` PUIS ajouter
   au dossier ARCHIVE — l'appel combiné est refusé 403) ; le
   `/instructions` LAISSÉ VIDE ;
5. **LA RELEASE** (la commande du maître : « il faudra ensuite mettre à
   jour les miroirs et zenodo ») : l'édition ou la release corrective au
   concept Zenodo (§ 5), la livraison au coffre, les miroirs ;
6. **CONSIGNER** : l'Entrée au `worklog.md`, `OU-TROUVER-LES-LIVRABLES.md`,
   et LE PRÉSENT FICHIER mis à jour.

**L'ÉTAT PRÉSENT** : la vague 14 est CLOSE (Entrée 384, 22/11/2026) —
six ateliers exécutés, instructions archivées, la release v0.23.1 au
concept. **LA VAGUE 15 attend ses instructions au commandement du
maître.** La dernière vague close entièrement : six ateliers + release ;
détail au worklog (Entrée 383 = vague 13, 384 = vague 14).

## 3. RESTAURER LE BAC NEUF (le pas à pas éprouvé à la vague 14)

```
1. jetons du coffre Drive /Tokens → /home/z/my-project/work/tokens/
   (oauth_token_relais.json [OAuth compte propriétaire — le refresh token
   d'upload peut meurer : le SA physichong couvre la LECTURE], zenodo.txt,
   token_git.txt)
2. cp le SA + le client_secret vers depot/.gdrive/ (chmod 600) ;
   echo le jeton zenodo > /home/z/my-project/work/mirrors_zenodo.txt
3. le bundle : télécharger TRIADE-sauvegarde-git/triade-history.bundle
   (145 Mo) → git clone <bundle> /home/z/my-project/depot && cd depot
   && git remote set-url origin https://github.com/alexisfrlopez-debug/triade.git
4. cp git-hooks/pre-commit .git/hooks/ (la garde de secrets h66o54pjd)
5. LES OUTILS DU BAC : pip install z3-solver unicorn keystone-engine
   capstone tiktoken ; apt-get download maude libbdd0c2 libtecla1t64
   libsigsegv2 libgcc-14-dev cpp gcc → dpkg-deb -x <chacun> maude-root/ ;
   curl tamarin-prover 1.12.0 linux64-ubuntu.tar.gz → /tmp/tamarin-prover
   (PATH=maude-root/usr/bin, LD_LIBRARY_PATH=maude-root/usr/lib/...) ;
   mingw : apt-get download gcc-mingw-w64-x86-64-posix + -x86-64 +
   binutils-mingw-w64-x86-64 + mingw-w64-x86-64-dev + gcc-14-base →
   dpkg-deb -x <chacun> /home/z/my-project/work/mingw-debs/root/
6. python3 scripts/check_auth.py  (le test des jetons, sans les montrer)
```
tectonic et openssl sont déjà au bac. Vérifier : `git log --oneline -3`
(la tête == le miroir GitHub : ls-remote), `python3 v06/sceau_I.py
verifier` (14 arbres VERTS).

## 4. OÙ TOUT SE TROUVE

| Emplacement | Contenu |
|---|---|
| `/home/z/my-project/depot` | LA SOURCE DE VÉRITÉ : le dépôt git complet (l'historique par le bundle ; l'arborescence § 6) |
| Coffre Drive (dossier racine « Triade ») | le `/instructions` (les vagues en attente), `ARCHIVE/` (les instructions exécutées, les packs supersédés), `/livrables` (les packs courants), `/test` (les constats du développeur), `TRIADE-sauvegarde-git/` (LE MIROIR du dépôt + triade-history.bundle + worklog + OU-TROUVER + les ateliers), `/Tokens`, `coffre_fort.bin` + `PHRASE-CONTROLE-COFFRE.txt` (garde durable D81), le conteneur de continuité |
| GitHub `alexisfrlopez-debug/triade` | le miroir distant (push à chaque release, vérifié anonymement ls-remote) |
| Zenodo | le concept 10.5281/zenodo.24367343 (les versions : …24420007 = v0.22.1, 24438614 = v0.23.0, la v0.23.1 = la vague 14) |
| `/home/z/my-project/download/` | les livrables du bac (miroir des pièces terrain) |

**Les jetons NE SONT JAMAIS committés** (la garde pre-commit h66o54pjd :
empreintes + entropie ; § 8 de l'ancien fichier demeure).

## 5. LA CHAÎNE DE RELEASE (la voie éprouvée v13)

1. **L'édition** (quand la vague porte une génération) : edition-v0<N>M0/
   née de la précédente, macros régénérées des journaux vivants
   (`scripts/vague13/regenerer_macros_v230.py`), tectonic + weasyprint
   pour les cinq pièces, LE LINTER `scripts/vague12/linter_v230.py`
   (zéro rouge + contrôle négatif), les packs (soumission / présentation /
   complet) assemblés aux empreintes consignées ;
2. **LA PUBLICATION ZENODO** (patron `scripts/vague13/publier_zenodo_
   v0230.py`) : la voie newversion → bucket → métadonnées → PUBLISH,
   reprise idempotente aux 500, les md5 recoupés byte-byte au bord anonyme,
   le DOI de version minté ;
3. **LA LIVRAISON AU COFFRE** (patron `scripts/vague13/livrer_coffre_
   vague13.py`) : la racine, le /test, le /livrables, les supersédés au
   lot ARCHIVE — chaque pièce recoupée par re-téléchargement (le 308
   « Resume Incomplete » est LA réponse intermédiaire normale) ;
4. **LES MIROIRS** : `python3 scripts/drive_sync.py` (miroir + bundle),
   le push GitHub (jeton .gdrive/token_git.txt), la vérification
   `verifier_trois_bords_v230.py` (le patron) ;
5. **L'ARCHIVAGE DES INSTRUCTIONS** (§ 2 point 4) ; worklog + OU-TROUVER
   + le présent fichier mis à jour ; le commit final + push.

## 6. L'ARBRERESCEMENT du dépôt (l'essentiel)

```
depot/
├── worklog.md                      LE JOURNAL (fait foi pour le détail ;
│                                   la dernière Entrée = l'état)
├── OU-TROUVER-LES-LIVRABLES.md    la carte des livrables (maj chaque Entrée)
├── PLAN-*.md + EMPREINTES-PLANS-VAGUE*.txt   les plans gelés (une table par vague)
├── REPRISE_PROJET.md               CE FICHIER
├── docs/                           PROTOCOLE_TRIADE.md (la spec source de travail),
│                                   DECISIONS.md (D1-D251+), PLAN_MILESTONES.md,
│                                   les archives PDF (v0.2 → v0.15.8), le Livre
├── scripts/                        sync_backup.sh, drive_sync.py, build_pdf.sh,
│   ├── vague11/ vague12/ vague13/  les chaînes par vague (linter v230, patchers)
│   ├── spec_v158/ livre_v17/       les sources spec + Livre (tectonic/cover)
├── edition-v0230/                  L'ÉDITION courante (main.tex + donnees/)
├── depot-zenodo-v0230/             les packs v0.23.0 (soumission + complet)
├── atelier-*/                      LES ATELIERS par vague (un dossier par
│                                   instruction : rapport + outils + registres)
├── ARCHIVE/                        les instructions exécutées par vague
├── m0/ m1/ m2/ m3/ m4/ m5/ m6/ m7/ m8/ tls13/ riscv/ unix/ loupe/ demo/
│   terrain/ v06/                   les jalons scellés (SCEAU-I 14/14)
├── loupe/ tls13/                   les notation/ + I/ (le matériau TPL-ADD)
└── v06/sceau_I.py                  LA GARDE (verifier : 14 arbres VERTS)
```

## 7. Les règles qui ne se marchandent pas

- le plan gelé AVANT la donnée ; l'empreinte consignée ; le commit d'abord ;
- **aucun verdict fabriqué** : un échec mesuré est une pièce aussi
  précieuse qu'un vert (la trace consignée) ;
- **le verbatim historique demeure octet pour octet** : les corrections
  vivent en ERRATUM append-only à côté ;
- **aucun secret commité** (la garde h66o54pjd), le coffre réel jamais
  touché au laboratoire (D105), les scellés intacts (le sceau-I avant et
  après chaque geste) ;
- la sauvegarde systématique (sync_backup.sh) après chaque modification ;
- l'ordre des tâches JAMAIS re-tiré ; les graines consignées.

## 8. Le protocole de cette session de reprise (vague 14, pour mémoire)

La restauration du bac + les six plans gelés + les six ateliers (frontières
z3 58/58, Tamarin installé-amendé-falsifié-honnête, GHASH agrégé 41× le
scellé, H-CGP4 −89,4 % du régime, TPL-ADD-v4 7/18 avec deux conversions,
H7 tirée + état de l'art vérifié) + les corrections (a)-(i) aux sources +
l'archivage + la release v0.23.1 + le présent fichier. Les GAPS nommés à
l'Entrée 384 (la régénération des cinq pièces et le linter étendu PORTÉS À
LA PROCHAINE SESSION DE GÉNÉRATION — la priorité de la vague 15).
