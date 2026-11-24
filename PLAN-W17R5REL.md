# PLAN GELÉ — W17R5REL (clôture, versionnement, release et synchronisation des trois bords)

> Instruction source : `/instructions/05_RELEASE_MIROIRS_ZENODO.md`. **Conditionnel** :
> l'exécution n'est autorisée que si les ateliers 01 à 04 ont produit des changements
> pertinents, si leurs plans et commits sont présents et si les contrôles passent. Aucun
> PUBLISH sans ces conditions ; aucun record réécrit ; aucun DOI de version réutilisé.

## Périmètre
### A. Pré-vol et versionnement
- Repartir de l'état vivant (Git, Drive, Zenodo) et résoudre les divergences consignées
  par W17R0GEL : release corrective v0.23.4 et corpus v2.1 contre les paragraphes
  permanents citant v0.23.3, v2 et D81.
- Décider : nouvelle édition / release corrective / aucune publication. Ne jamais
  réécrire une balise ou un record immuable ; ne pas minter une version vide ou
  simplement renommée.
- Utiliser le patron le plus récent réellement présent (`scripts/vague16/
  publier_zenodo_v0234.py`, `assembler_zips_v0234.py`, `linter_v233_residus.py`,
  `scripts/livrer_coffre_v232.py`, `scripts/drive_sync.py`), sans présumer qu'un numéro
  de script est encore le patron courant.
- Sceau-I avant génération et après, au nombre d'arbres du manifeste ; vérifier les cinq
  pièces et les empreintes enregistrées ; archiver rapport, manifeste et contrôles.

### B. Zenodo
- Garder séparés le concept du protocole (10.5281/zenodo.24367343), le kit développeur
  (…24457514) et le corpus (…24457524).
- Nouvelle version seulement si le contenu a changé : new version → bucket → dépôt →
  métadonnées → comparaison byte-byte → PUBLISH. Version publiée jamais remplacée.
- Avant PUBLISH : fichiers et métadonnées exacts, sommes recoupées par re-téléchargement,
  DOI résolvant. Un contrôle en échec ⇒ brouillon + blocage expliqué.
- Kit v1 et corpus v1 restent immuables si leur contenu n'a pas changé.

### C. Drive et GitHub
- Livrer au coffre aux emplacements racine, `/test`, `/livrables`, `ARCHIVE` selon les
  patrons ; re-télécharger et comparer les octets.
- Archivage en DEUX étapes séparées (retirer de `/instructions`, puis ajouter à ARCHIVE) ;
  une instruction non exécutée n'est pas déplacée ; `/instructions` n'est pas déclaré vide
  s'il reste des tâches pendantes.
- Miroir Drive + bundle, push GitHub, vérification des trois bords ; si GitHub pousse
  avant Drive, recaler le miroir sur la tête réellement poussée.

### D. Clôture
- `worklog.md`, `OU-TROUVER-LES-LIVRABLES.md`, `REPRISE_PROJET.md` : un état UNIQUE, daté,
  recoupé ; mentions d'anciennes versions étiquetées historiques ; aucune consigne active
  ne contredit D223. Rapports de release, empreintes, état de chaque bord.

## Fichiers touchés
`worklog.md`, `OU-TROUVER-LES-LIVRABLES.md`, `REPRISE_PROJET.md`, `RAPPORT-RELEASE-*.txt`,
`empreintes_livrables_v0.24.0.txt` (ou équivalent), `depot-zenodo-v0240/` (si édition),
`scripts/vague17/` (patrons), `ARCHIVE/instructions_vague17_<date>/`.

## Hypothèses
- H1 : `tectonic` est ABSENT de ce bac → une **édition** (régénération des cinq pièces) est
  impossible ici ; seules une release corrective de dépôt ou aucune publication sont
  atteignables, sauf installation de la chaîne.
- H2 : `weasyprint` et `pdftotext` sont présents, ce qui n'est pas suffisant pour le
  tectonic des pièces LaTeX.
- H3 : le push GitHub exige le Service GitHub (absent au gel) ou le jeton du coffre ; son
  absence est un blocage NOMMÉ, pas une étape sautée en silence.

## Critères d'acceptation
- Une seule version de départ, datée, prouvée par les octets.
- Si publication : md5 byte-byte avant PUBLISH, DOI de version minté, concept résolvant,
  trois bords vérifiés, records antérieurs intacts.
- Si aucune publication : décision écrite et datée, avec la raison (rien de pertinent,
  ou chaîne indisponible).
- `/instructions` : état exact (ce qui reste, pourquoi) — jamais un « vide » de
  complaisance.
- Sceau-I avant/après ; aucun secret lu, committé ou copié.

## Risques
- R1 : mint d'une version vide ou simplement renommée.
- R2 : réutilisation d'un DOI de version, remplacement d'un record publié.
- R3 : push GitHub avant Drive sans recalage du miroir.
- R4 : déclarer « complet » avec une étape autorisée en attente.

## Tests et preuves requis
- `git ls-remote` avant/après push ; comparaison des têtes et de l'univers d'objets.
- Re-téléchargement et comparaison d'empreintes de chaque pièce livrée.
- `curl` au bord public : état, version, fichiers, résolution des DOI.
- `python3 v06/sceau_I.py verifier`.

## Dépendances
W17R1D81, W17R2PAT, W17R3R10, W17R4PER closes (commits présents, contrôles verts).
Chaîne tectonic (édition) et Service GitHub (push) : en attente nommée si indisponibles.
