# ÉTAT DE RÉFÉRENCE — VAGUE 17 (exécution du plan W17R0GEL)

> Geste du 24/11/2026, APRÈS le commit de gel `8853bcf` (les six plans et leur table
> d'empreintes). Chaque ligne ci-dessous a été vérifiée ce jour, à la source, avec son
> empreinte recoupée. Aucun secret n'a été ouvert : le dossier `/Tokens` n'est cité qu'en
> noms.

## 1. Les trois bords

| Bord | État vérifié | Preuve |
|---|---|---|
| Dépôt local | clone public de `alexisfrlopez-debug/triade` ; tête **8853bcf** (le gel de la vague 17) sur `main` ; aucune autre branche de travail | `git rev-parse HEAD`, `git status --porcelain` vide |
| Miroir GitHub | `refs/heads/main` = **a75b0c5** (Entrée 397) | `git ls-remote` ; **le miroir est en retard d'un commit** (le gel) : le push est impossible ce jour — Service GitHub absent, blocage nommé |
| Coffre Drive | racine : `rapport-release-v0234-20261123.txt` (23/11 19:52), `REPRISE_PROJET.md` et `OU-TROUVER-LES-LIVRABLES.md` (23/11 11:47), `TRIADE_complet_v0.23.3.zip` (22/11 23:44), `empreintes_livrables_v0.23.3.txt`, `rapport_verification_v0.23.3.txt`, `coffre_fort.bin`, `LISEZMOI-PHRASE-CONTROLE.txt`, dossiers `livrables`, `test`, `ARCHIVE`, `instructions`, `Tokens`, `TRIADE-sauvegarde-git`, `Cérémonie` | listings horodatés `gdrive list` |
| Zenodo | protocole **v0.23.4** = record 24480415 (3 fichiers) ; corpus **v2.1** = 24479882 (9 fichiers) ; kit **v1.0.0** = 24457515 (1 fichier) ; corpus v1 = 24457525 (7 fichiers) | API `records/*` + résolution `doi.org` |

## 2. Matrice état → emplacement → pièce → empreinte

| Objet | État confirmé | Emplacement | Pièce / empreinte |
|---|---|---|---|
| Édition du protocole | **v0.23.4** (corrective) | Zenodo 24480415 ; Drive `/livrables` | `TRIADE_complet_v0.23.4.zip` 8 565 449 o md5 **c94748f8…** ; `TRIADE_soumission_v0.23.3.zip` 300 682 o md5 **60e1fac7…** ; `TRIADE_presentation_v0.23.3.zip` 2 223 923 o md5 **f8e6ad0a…** |
| Concept du protocole | résout sur v0.23.4 | doi.org | `10.5281/zenodo.24367343` → `zenodo.org/records/24480415` |
| Les cinq pièces | identiques à v0.23.3, **recomptées ce jour** | dépôt `scripts/vague15/pack-v233/` | manuscrit `a2835461…`, spécification `06171f7f…`, Livre `59305398…`, preuves `69a0b4c3…`, présentation `0b5e843b…` — **5/5 == la table consignée** |
| Corpus d'entraînement | **v2.1** | Zenodo 24479882 ; dépôt `depot-zenodo-corpus-v21/` | 9 fichiers ; `MANIFESTE.json` md5 **21fa7a73…** recoupé au bord anonyme (octet à octet) ; `train/dev/test` sha256 == manifeste publié ; 127/24/19 lignes, splits 14/2/2 contrats, 48 paires DPO, graine 20261126 |
| Concept du corpus | résout sur v2.1 | doi.org | `10.5281/zenodo.24457524` |
| Kit développeur | **v1.0.0** (immuable) | Zenodo 24457515 | 1 fichier ; concept 24457514 |
| Corpus v1 | **v1** (immuable) | Zenodo 24457525 | 7 fichiers |
| Sceau-I | **14 arbres, 14 manifestes déposés, 14 VERTS** | dépôt `v06/sceau-I/` | vérifié avant et après le gel ; le compte vient du manifeste vivant (`ARBRES` + `manifestes/`), jamais d'un rapport |
| Garde de sécurité | D223/D236 actives (séquestre 5/3), D81 historique | dépôt `docs/DECISIONS.md` | à re-vérifier par l'atelier W17R1D81 |

## 3. Divergences nommées (avec leur statut)

**Dv1 — La racine du coffre n'offre pas la version courante.** Elle porte
`TRIADE_complet_v0.23.3.zip` et `empreintes_livrables_v0.23.3.txt` alors que la version
courante est v0.23.4, présente au `/livrables`. Statut : confirmé. Conséquence : un
lecteur du coffre qui prend la racine travaille sur l'avant-dernière version.

**Dv2 — `REPRISE_PROJET.md` du coffre en retard.** Copie Drive du 23/11 11:47 (état
Entrée 393, rédaction vague 14) contre celle du dépôt, portée à l'Entrée 397 au commit
a75b0c5. Statut : confirmé.

**Dv3 — `OU-TROUVER-LES-LIVRABLES.md` du coffre en retard.** Copie du 23/11 11:47 contre
la Mise à jour 397 du dépôt. Statut : confirmé.

**Dv4 — Trois compteurs de version confondus.** `docs/PROTOCOLE_TRIADE.md` s'annonce
« PROTOCOLE TRIADE v0.15.0 — Spécification technique » et « Source de travail faisant
autorité pour la v0.15.0 », alors que la pièce publiée est
`Protocole_TRIADE_v0.15.8_Specification.pdf` et que l'édition porte v0.23.4. Ce sont
trois compteurs distincts : **document** (v0.15.8), **édition/release** (v0.23.4),
**corpus** (v2.1). Le corps du Markdown a bien été patché jusqu'à v0.15.8 (D236, onze
remplacements ancrés) ; c'est l'EN-TÊTE qui est resté à v0.15.0. Statut : confirmé ;
correction proposée : porter l'en-tête et la ligne « Version : » à v0.15.8, sans toucher
au corps ni au verbatim historique (geste éditorial, hors release).

**Dv5 — Pas de table d'empreintes v0.23.4 dans le dépôt.** La racine ne porte que
`empreintes_livrables_v0.23.1.txt` ; les tables v0.23.2 et v0.23.3 vivent sous
`scripts/vague14/` et `scripts/vague15/` ; aucune table v0.23.4 n'existe, la release
correctice s'appuyant sur la reconduction byte-byte des cinq pièces v0.23.3. Statut :
confirmé ; conséquence : la porte A de l'assemblage v0.23.4 n'est pas re-jouable depuis
une table dédiée (même classe de défaut que `campagne-v5.log` nommé à l'Entrée 397).

**Dv6 — `MANIFESTE.json` du corpus : même contenu, octets différents.** Le fichier publié
(md5 21fa7a73…) et celui du dépôt (md5 ece632e8…) portent un contenu JSON **identique**
(comparé clé à clé) mais des octets différents. Statut : confirmé ; conséquence : les
empreintes ne sont pas reproductibles à l'octet près tant que la sérialisation n'est pas
épinglée.

**Dv7 — La « lignée du pack ».** Le zip `depot-zenodo-v0233/TRIADE_complet_v0.23.3.zip`
du clone a pour sha256 `8a256333…`, différent de celui de la lignée du coffre, à contenu
identique : c'est l'écart déjà nommé à l'Entrée 391 (les octets d'un zip varient selon la
lignée du bac). Statut : connu, non un défaut.

**Dv8 — Le pack v0.23.4 n'a qu'un fichier neuf.** Seul le complet est régénéré ; la
soumission et la présentation sont reconduites octet pour octet sous leur nom v0.23.3 (le
précédent v0.23.1). Statut : décision assumée, à ne pas lire comme un oubli.

## 4. Contradictions internes du dossier

- `REPRISE_PROJET.md` § 1 cite encore v0.23.3 comme version courante et D81 comme garde
  durable : ces phrases sont HISTORIQUES et contredisent l'état 397 et D223. Elles ne
  seront corrigées que par W17R1D81 (D81) et W17R5REL (versions), jamais dans ce prompt.
- Les prompts 00 et 05 décrivent eux-mêmes cette contradiction (« release corrective
  v0.23.4 et corpus v2.1, tandis que ses paragraphes permanents citent encore v0.23.3 ») :
  le constat est CONFIRMÉ sur pièces.

## 5. Numéro de la vague

Deux pièces indépendantes concordent : l'ARCHIVE du coffre s'arrête à
`instructions_vague16_20261123` (la vague 16 close le 23/11), et le `/instructions` porte
six fichiers déposés le 23/11 entre 23:10 et 23:12 UTC, après la release v0.23.4
(19:52). **Vague 17 confirmée** — et non présumée.

## 6. Décision de gel

Six plans gelés (`PLAN-W17R0GEL`, `W17R1D81`, `W17R2PAT`, `W17R3R10`, `W17R4PER`,
`W17R5REL`), table `EMPREINTES-PLANS-VAGUE17.txt` (six sha256), **commit `8853bcf`** —
posé avant la première collecte, la première mesure et tout atelier. Ordre d'exécution
gelé : 00 → 01 → 02 → 03 → 04 → 05.

## 7. Calendrier d'exécution proposé

1. **W17R1D81** — vérification et durcissement (linter à deux tests négatifs, erratum),
   court.
2. **W17R2PAT** — spécification de la bascule, kit falsifiable, statut matériel en
   attente, moyen.
3. **W17R3R10** — matrice menace/ancre, décision bornée, moyen.
4. **W17R4PER** — provenance des tableaux et paquet de réplication, long.
5. **W17R5REL** — conditionnel : `tectonic` absent ⇒ **pas d'édition possible ici** ; une
   corrective seulement si 01-04 changent des octets publiés ; sinon aucune publication,
   avec la raison écrite.
6. **Push GitHub** — bloqué jusqu'à l'ouverture du Service GitHub ; le miroir et le
   bundle seront recalés sur la tête réellement poussée.
