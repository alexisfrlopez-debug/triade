# PLAN GELÉ — W17R0GEL (reprise, état de référence et gel de la vague 17)

> Instruction source : `/instructions/00_REPRISE_ET_GEL.md` (coffre Drive, déposée le
> 23/11/2026 à 23:12 UTC). Gelé le 24/11/2026 AVANT toute collecte de données, toute
> mesure et tout atelier. Le présent plan et la table `EMPREINTES-PLANS-VAGUE17.txt`
> sont committés ensemble, et ce commit précède le premier geste de collecte.

## Périmètre
1. Vérifier l'état vivant aux trois bords : dépôt Git local, miroir GitHub
   (`alexisfrlopez-debug/triade`), coffre Drive (racine, `/livrables`, `/test`, `ARCHIVE`,
   `/instructions`, noms du dossier `/Tokens` seulement) et records Zenodo (protocole,
   kit développeur, corpus).
2. Établir la **matrice d'état** : pour chaque objet (version d'édition, corpus, kit,
   arbre scellé, garde de sécurité), quel état est CONFIRMÉ, à quel emplacement, par
   quelle pièce et quelle empreinte (sha256 local, md5 au bord anonyme).
3. Trancher la divergence de références documentaires : `docs/PROTOCOLE_TRIADE.md`
   s'annonce « source de travail faisant autorité pour la v0.15.0 », la série des PDF
   publiés va jusqu'à v0.15.8, et l'édition courante est v0.23.4. Déterminer la relation
   réelle (source de travail vs pièces générées vs archives historiques) et consigner
   toute divergence avant de proposer une correction.
4. Confirmer le numéro de vague à partir de l'ARCHIVE du coffre et de l'état vivant
   (ne pas présumer « 17 »).
5. Geler les six plans (00 à 05) et leur table d'empreintes, puis committer.

## Fichiers touchés
- `ETAT-REFERENCE-VAGUE17.md` (nouveau — la matrice ; **après** le commit de gel).
- `PLAN-W17R0GEL.md` … `PLAN-W17R5REL.md` (nouveaux, six plans).
- `EMPREINTES-PLANS-VAGUE17.txt` (nouveau, table sha256).
- Aucun document de protocole modifié dans ce prompt.

## Hypothèses
- H1 : la tête locale (clone public) est la tête du miroir GitHub ; à re-vérifier par
  `git ls-remote` au moment du geste.
- H2 : les cinq pièces de l'édition courante sont byte-identiques à celles de v0.23.3
  (constat de la release corrective v0.23.4) ; le corpus courant est v2.1.
- H3 : le nombre d'arbres scellés est celui déclaré par le manifeste vivant
  (`v06/sceau-I/manifestes`), jamais un compte recopié d'un rapport ancien.
- H4 : le dossier `/Tokens` est lisible en NOMS seulement ; aucune valeur n'est ouverte,
  affichée ni recopiée.
- H5 : le numéro de la prochaine vague se déduit de l'ARCHIVE (`instructions_vague*`) et
  du contenu de `/instructions` ; une divergence entre les deux est un fait à consigner.

## Critères d'acceptation
- Matrice complète, datée, chaque ligne portant emplacement + pièce + empreinte recoupée.
- Chaque contradiction nommée avec son statut : confirmée / close / historique.
- Les six plans et la table d'empreintes committés AVANT toute collecte ; le hash du
  commit de gel cité dans le rapport.
- Sceau-I vérifié au nombre d'arbres du manifeste vivant, avant et après le geste.
- Aucun secret lu, affiché ou committé ; aucun PUBLISH Zenodo dans ce prompt.

## Risques
- R1 : miroir GitHub ou Drive en retard sur la tête locale → la matrice doit dire lequel
  fait foi, sans réécrire l'histoire.
- R2 : record Zenodo non résolvable (erreur transitoire 500 constatée le 24/11 sur
  l'API) → re-tester au bord anonyme, consigner le statut réel, ne pas conclure.
- R3 : confusion v0.15.x / v0.23.x → traitée explicitement, jamais moyennée.
- R4 : lecture accidentelle de `/Tokens` ou du coffre réel → refus nommé, chemins seuls.

## Tests et preuves requis
- `git rev-parse HEAD`, `git status --porcelain`, `git ls-remote origin` (les trois têtes).
- `python3 v06/sceau_I.py verifier` (avant et après) + décompte des manifestes déposés.
- Listings Drive horodatés (racine, `/livrables`, `/test`, `ARCHIVE`, `/instructions`).
- `curl` au bord public : état, version, nombre de fichiers de chaque record ; résolution
  des DOI de concept chez doi.org.
- Recoupement d'au moins une empreinte par objet (sha256 local vs md5 publié).

## Dépendances
Aucune amont. Ce plan conditionne l'ouverture des ateliers 01 à 05 : **aucun atelier ne
commence avant confirmation du commit de gel**.
