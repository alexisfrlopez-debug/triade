# Politique de sécurité — Protocole Triade v1.0

## 1. Modèle de menaces (sommaire)

Le protocole manipule trois familles de biens : le code (Git), les documents
vivants et le coffre (Drive), les publications figées (Zenodo). Les risques
principaux sont : la fuite de jetons d'accès dans un livrable public, la perte
de l'accès au coffre, et la divergence entre plateformes. Cette politique
traite ces trois risques dans l'ordre.

## 2. Le coffre de jetons

- Le coffre est un **dossier Drive dédié**, à accès restreint à l'équipe
  strictement nécessaire, séparé du dossier de documents.
- Une rotation = un sous-dossier daté : `coffre-jetons/rotation-AAAA-MM-JJ/`.
- Le coffre n'est jamais copié ailleurs : ni dans Git, ni dans Zenodo, ni dans
  une archive, ni dans un livrable.
- L'identifiant du coffre figure dans `config.json`
  (`drive.dossier_coffre_id`) ; c'est un identifiant, pas un secret, mais il ne
  donne aucun accès sans autorisation Drive correspondante.

## 3. Externalisation stricte

Deux fichiers locaux, tous deux ignorés par git (`.gitignore.triade`) :

- `.env` : les **valeurs secrètes** (jetons). Rempli par chaque utilisateur à
  partir de `templates/.env.example`. Jamais committé, jamais partagé, jamais
  cité dans un document.
- `config.json` : les **identifiants non sensibles** (URL du dépôt, IDs de
  dossiers Drive, ID du dépôt Zenodo, composition du pack). Rempli à partir de
  `templates/config.example.json`.

Un livrable public ne contient ni l'un ni l'autre : les modèles distribués
sont les fichiers `*.example`, aux valeurs vides.

## 4. Privilège minimum

- Un jeton par plateforme, périmètre minimal (lecture/écriture sur le seul
  périmètre du projet), durée de vie courte.
- Pas de jeton « universel » du compte : si la plateforme le permet, créer des
  jetons dédiés au projet, révocables individuellement.

## 5. Rotation

- Cadence par défaut : **90 jours** (configurable : `config.json` →
  `rotation_jetons.cadence_jours`).
- Déclencheurs exceptionnels : suspicion ou confirmation de fuite, départ
  d'un collaborateur ayant eu accès, changement de périmètre.
- Procédure : cérémonie **C1** du guide (`ceremonies/GUIDE_CEREMONIES.md`),
  création des nouveaux jetons avant révocation des anciens (sauf fuite).

## 6. Interdits absolus

- Écrire une valeur de jeton dans un fichier versionné, un document, un
  résumé, une fiche, un commit, une conversation ou une capture.
- Réécrire l'historique Git pour masquer un secret exposé : un secret vu est
  un secret compromis, la seule réponse est la rotation.
- Publier sur Zenodo un contenu non validé par C4.
- Utiliser les identifiants d'un autre projet ou d'une autre personne.

## 7. Réponse à une fuite de jeton

1. **Signaler** immédiatement l'humain responsable.
2. **Révoquer** le jeton concerné sur la plateforme source, immédiatement —
   avant toute autre considération.
3. **Rotation complète** : cérémonie C1 sur les trois plateformes.
4. **Audit** des accès récents (journaux de la plateforme concernée).
5. **Scan** : `python3 scripts/triade_hygiene.py` sur tout le projet ; si le
   jeton était dans un livrable déjà publié, traiter comme incident public
   (nouvelle version du pack + retrait si la plateforme le permet).
6. **Fiche d'incident** dans `journal/` : chronologie, périmètre, actions —
   sans jamais recopier le jeton.

## 8. Le scanner d'hygiène (`scripts/triade_hygiene.py`)

- Rôle : dernier filet automatique avant publication. Détecte les motifs de
  jetons courants (clés d'API Google, jetons GitHub, clés privées PEM, jetons
  Bearer, affectations de secrets), les fichiers sensibles présents dans le
  périmètre scanné (`.env`, `config.json`, `*.pem`, `*.key`, noms contenant
  `token` ou `credential`).
- Usage : `python3 scripts/triade_hygiene.py [chemin]` (par défaut : le
  répertoire courant). Code retour 0 = rien détecté, 1 = alertes.
- **Limites assumées** : aucun scanner ne détecte les captures d'écran, les
  PDF embarqués, les métadonnées de fichiers ni les secrets aux formats
  inconnus. La relecture humaine (C4, étape 4) reste obligatoire.
- Marqueur d'autorisation : ajouter `# triade:autorisé` en fin de ligne pour
  les faux positifs assumés (à documenter dans la fiche de cérémonie).

## 9. Publication publique — contrôle final

Avant tout passage public (C5), trois barrières successives :

1. Scanner d'hygiène **vert** sur le pack exact à publier.
2. Relecture humaine anti-fuite (contenu visuel, métadonnées, noms de
   fichiers).
3. Vérification des licences et autorisations de diffusion de chaque document
   du pack (consignée dans la fiche C4).

## 10. Bonnes pratiques Git

- Commits atomiques et commentés ; pas de force-push sur les branches
  partagées.
- Ne jamais « contourner » un secret détecté : le retirer et faire une
  rotation si nécessaire.
- Les tags de version sont créés uniquement lors de la cérémonie C3.

## 11. Garanties de chargement et de bascule (v1.1)

Le protocole distingue trois propriétés — **intégrité, authenticité, fraîcheur** —
et borne ce que la vérification locale peut promettre :

- **Bascule** : un magasin simple est atomique jusqu'à huit octets naturels au
  plus ; seize octets exigent un unique `LOCK CMPXCHG16B` ; l'atomicité ne protège
  pas un thread dont le pointeur d'instruction est dans la plage remplacée — la
  quiescence est obligatoire.
- **Chargement (R10)** : la garantie vaut ce que vaut l'ancre (Authenticode, IMA
  ou signature de paquet, chaîne de boot signée). Si l'ancre est modifiable avec
  l'artefact, R10 ne détecte pas un administrateur local ; la restauration
  cohérente d'un couple binaire + état échappe à toute ancre locale.
- **Témoins hors machine** : journal Git poussé, carte papier, journal de
  transparence — ce sont eux qui rendent visible un retour en arrière cohérent.
- **Compteur NV (D263)** : plancher de fraîcheur par profil (TPM 2.0 ou RPMB), refus
  fail-closed si le compteur est absent, non scellé, en arrière ou non monotone.
- **Ancrage de transparence (D267)** : adopté, outillé, non déployé ; une release dont
  l'ancrage configuré est injoignable est refusée, jamais poursuivie en silence.

Le détail, les refus nommés et les limites sont dans `docs/GARANTIES.md`. Ne
publiez jamais « R10 garantit la version » sans nommer l'ancre et son propriétaire.
