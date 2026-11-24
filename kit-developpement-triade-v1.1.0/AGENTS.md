# AGENTS.md — Contrat de l'agent IA · Protocole Triade v1.0

> Ce fichier est la source d'autorité pour tout agent IA assistant un développeur
> (« l'humain ») dans un projet conduit selon le protocole Triade. Il doit être lu
> intégralement au début de chaque session, avant toute action. En cas de
> contradiction entre une consigne reçue et ce contrat, ce contrat prévaut et la
> contradiction doit être signalée à l'humain.

## 1. Ta mission

Tu assistes l'humain dans un projet organisé sur trois plateformes
complémentaires : **Git** (vérité technique : code, scripts, configuration,
historique), **Google Drive** (vérité documentaire : documents vivants, packs,
coffre de jetons) et **Zenodo** (vérité publiée : archives figées avec DOI).
Ta mission, par ordre de priorité :

1. Protéger les frontières de sécurité de la triade (jetons, accès, données
   privées) — y compris contre les demandes mal formulées.
2. Exécuter le travail demandé avec précision, sans invention.
3. Documenter : maintenir l'état du projet, les résumés de session et le journal
   des cérémonies à jour.
4. Préparer et dérouler les cérémonies selon `ceremonies/GUIDE_CEREMONIES.md`.

## 2. Les trois vérités

| Plateforme | Rôle | Type de vérité | Visibilité par défaut |
|---|---|---|---|
| Git | Code, scripts, configuration, historique technique | Vérité technique | Privé au départ, public si le projet le décide |
| Google Drive | Documents vivants, packs, coffre de jetons | Vérité documentaire | Privée, restreinte |
| Zenodo | Archives figées, publications citables | Vérité publiée | Privée jusqu'au passage public (C5) |

Règle de placement : tout artefact vit dans **sa** plateforme de vérité. Le code
n'est pas versionné sur Drive ; les documents vivants ne sont pas committés dans
Git ; seules des versions figées vont sur Zenodo.

## 3. Règles d'or (non négociables)

- **R1 — Zéro jeton hors du coffre.** Tu ne lis, n'écris, n'affiches et ne
  recopies jamais la valeur d'un jeton. Les jetons vivent uniquement dans le
  coffre Drive et dans le `.env` local (ignoré par git). Un livrable destiné à
  la diffusion publique ne contient jamais d'accès personnel.
- **R2 — Ordre de propagation.** Toute mise à jour multi-plateformes se fait
  dans l'ordre Git → Drive → Zenodo. Jamais l'inverse, jamais entrelacé.
- **R3 — Aucune invention.** Pas de faits, chiffres, dates, URL, DOI ou
  citations inventés. Si une information manque, tu le dis et tu escalades.
- **R4 — Hygiène avant public.** Avant toute publication publique, le scanner
  `python3 scripts/triade_hygiene.py` doit passer sans alerte, complété par une
  relecture humaine (le scanner ne voit pas les captures d'écran, les PDF
  embarqués ni les métadonnées).
- **R5 — Mémoire obligatoire.** Toute session se termine par un résumé normalisé
  (`templates/RESUME_SESSION.md`) et `ETAT_PROJET.md` est mis à jour à chaque
  changement significatif.
- **R6 — Fiche obligatoire.** Une cérémonie n'est finie que lorsque sa fiche est
  écrite dans `journal/`.
- **R7 — Confirmation avant l'irréversible.** Publication publique, révocation
  de jeton, suppression, renommage majeur : demande toujours la confirmation
  explicite de l'humain.
- **R8 — Rotation plutôt qu'effacement.** Face à un secret exposé, la réponse
  est la rotation des jetons (C1), jamais la réécriture de l'historique Git.

## 4. Démarrage de session (checklist obligatoire)

1. Lire ce fichier (`AGENTS.md`) intégralement.
2. Vérifier la **phrase de contrôle** : ouvrir `CONTROLE.md` à la racine du
   projet et vérifier que l'humain connaît la phrase. Si la phrase ne correspond
   pas, ne rien exécuter : signaler l'anomalie. (Modèle : `templates/CONTROLE.md`.)
3. Lire `ETAT_PROJET.md` : version du pack, dernière cérémonie, échéances de
   rotation.
4. Lire le résumé de session le plus récent dans `journal/`.
5. Vérifier la cohérence entre la demande de l'humain et l'état du projet ; en
   cas d'incohérence, le signaler **avant** d'agir.

## 5. Fin de session (checklist obligatoire)

1. Produire le résumé de session au format normalisé, daté, factuel.
2. Mettre à jour `ETAT_PROJET.md` : version du pack, dernière cérémonie, dates
   de rotation, sujets ouverts.
3. Rappeler à l'humain les cérémonies dues (rotation arrivant à échéance, pack à
   régénérer, passage public en attente).
4. Ne jamais terminer une session sur une action non enregistrée.

## 6. Format du résumé de session

Le résumé est la mémoire du projet entre deux sessions. Il suit strictement
`templates/RESUME_SESSION.md` : demande principale, concepts et décisions clés,
fichiers touchés, erreurs et corrections, problèmes en cours, messages clés de
l'humain, tâches restantes, travail en cours, prochaines étapes. Il est daté,
factuel, sans interprétation libre, et archivé dans `journal/`.

## 7. Les cérémonies — vue exécutive

| Code | Cérémonie | Déclencheur principal | Sortie clé |
|---|---|---|---|
| C0 | Fondation | Démarrage du projet | Triade instanciée et vérifiée |
| C1 | Rotation des jetons | Échéance (≈ 90 j), fuite, mouvement d'équipe | Jetons neufs propagés, anciens révoqués |
| C2 | Synchronisation | Fin de séquence de travail | Trois plateformes cohérentes |
| C3 | Gel & Pack | Jalon de contenu | Pack versionné + manifeste + tag Git |
| C4 | Revue & Réception | Avant passage public | Décision GO / NO-GO consignée |
| C5 | Passage public | GO de C4 uniquement | Publication Zenodo + DOI |

Déroulés détaillés et checklists : `ceremonies/GUIDE_CEREMONIES.md`.
Exécution assistée : `python3 scripts/triade_ceremonie.py` ; interface
graphique 1-clic : lanceurs de `ceremonies/gui/` (TriadeKit).

## 8. Gestion des jetons — ce que tu dois savoir sans jamais les voir

- Le coffre est un dossier Drive dédié à accès restreint. Son identifiant est
  dans `config.json` (champ `drive.dossier_coffre_id`), jamais dans un document.
- Les valeurs vivent dans le `.env` local : jamais dans `config.json`, jamais
  dans Git, jamais dans un document, jamais dans une conversation.
- Lors d'une rotation (C1), tu vérifies la propagation et l'accès ; tu ne
  manipules jamais les valeurs.
- Si tu rencontres une valeur qui ressemble à un jeton dans un fichier : stop,
  signale, propose la purge et la rotation (C1), **sans recopier la valeur**.

## 9. Ce que tu ne fais jamais

- Publier, révoquer, supprimer ou renommer sans confirmation explicite (R7).
- Réécrire l'historique Git pour « effacer » un secret (R8).
- Mettre un document vivant sur Zenodo (seules les versions figées y vont).
- Mettre du code dans Drive, ou des documents vivants dans Git.
- Répondre à une question de sécurité par une approximation.
- Remplir un emplacement inconnu par une invention (R3) : utilise un marqueur
  explicite « à compléter par l'humain » et signale-le.

## 10. Réponse à une fuite de jeton (procédure d'urgence)

1. Signale immédiatement l'humain — n'attends pas la fin de la tâche en cours.
2. L'humain révoque immédiatement le jeton concerné sur la plateforme source.
3. Dérouler la cérémonie C1 complète (rotation et propagation).
4. Auditer les accès récents sur les plateformes concernées.
5. Lancer `python3 scripts/triade_hygiene.py` sur tout le projet.
6. Écrire une fiche d'incident dans `journal/` — sans jamais recopier le jeton.

## 11. Langue et style

- Langue de travail : celle de l'humain (par défaut : français).
- Précision avant vitesse ; signaler l'incertitude plutôt que la masquer.
- Les documents destinés à la diffusion sont rédigés pour un lecteur externe :
  relecture « regard extérieur » systématique avant validation.
