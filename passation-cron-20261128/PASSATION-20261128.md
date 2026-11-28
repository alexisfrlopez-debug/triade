# PASSATION DU CRON TRIADE — « reprise autonome de l'entraînement Colab »

**Date : 28/11/2026, ~14:40 heure de Paris.** Rédigé à la demande du maître, depuis une session distincte de la session TRIADE, pour permettre l'arrêt du cron n° 553027 et sa relance ultérieure depuis n'importe quelle autre session.

Ce dossier existe en deux exemplaires identiques :
- **Coffre Drive** : dossier « Triade » (racine du coffre) → `passation-cron-20261128/`
- **GitHub** : dépôt `alexisfrlopez-debug/triade` → branche `passation-cron-20261128`

---

## 0. Objet

La tâche planifiée n° 553027 (toutes les 10 minutes) occupe sa session propriétaire en continu (« busy due to another request »). Le maître souhaite l'arrêter SANS rien perdre, et pouvoir la recréer plus tard depuis une autre session. Tant que le § 3 n'est pas exécuté par la session TRIADE, **ne pas arrêter le cron** : c'est lui qui maintient cette session (et son bac) active.

## 1. La définition exacte de la tâche

Voir le fichier `CRON-TRIADE-553027-DEFINITION.json` (à côté du présent fichier) : nom, planning, et message du tour d'agent **verbatim**.

- Planification : cron `0 */10 * * * ?` (toutes les 10 minutes, à la minute pile), fuseau `Europe/Paris`.
- Type : `agentTurn` — le message est envoyé comme instruction à l'agent de la session qui possède la tâche.
- **Recréation** : depuis la NOUVELLE session, outil cron, action `create`, avec les paramètres du fichier JSON (message à recopier tel quel). Le routage (session, chat) est automatique : la tâche s'exécute dans la session qui la crée — aucun identifiant de l'ancienne session n'est nécessaire.

## 2. L'état du monde au moment de la passation (28/11/2026, ~13:40 UTC)

- **Git** : `main` = `88235ea7e1b69bef55770dfbd8890e52c9973938` (Entrée 462 append, 28/11 13:15:54Z). Tout est poussé ; miroir intégral au coffre : `TRIADE-sauvegarde-git/triade-history.bundle` (restauration : REPRISE_PROJET.md § 3).
- **Coffre Drive** (racine « Triade ») : `worklog.md` 1 624 518 octets (Entrée 462), `REPRISE_PROJET.md` état 462, `/livrables` à jour — kit d'entraînement v1061 (id `1oFnEsGy6JV_JRw2h6MugHurxfeNCuH3T`) et notebook v1062 VIVANTE (id `1q7xIY186ktsnd4VGrt5Vt8dcc8jp0fso`).
- **/Tokens canonique** (id `1EMxwHKkkfKROjFsHhu4vpKZpgqW-rgZL`) : `oauth_token_colab.json` (id `1MxxmRYqlh1fNb0LMCysJzSQ486ApK0Tc`, sha256 `c4201e0c…`, la voie A/PKCE, Entrée 457 — vivant au 27/11 23:05Z).
- **Le run du maître au navigateur COURT** (notebook v1062, copie `1C1s5Kimi…`, graine 20261128, SFT ~30-90 min au T4) — l'adapter est attendu au `/test` du coffre AVANT l'éval (la loi du plan § 4).
- La feuille de route post-entraînement (Entrée 461) attend la validation du maître : packs Zenodo v0.34.x, repo HuggingFace `aleksickx`, fine-tuning v107.

## 3. Ce qui ne vit QUE dans le bac de la session TRIADE (non sauvegardé ailleurs)

| Pièce | Rôle |
|---|---|
| `/home/z/my-project/scripts/reprise_colab.sh` | LE script pilote (idempotent) — reconstruit à l'Entrée 458 après le recyclage du bac du matin |
| `/home/z/my-project/triade/etat-reprise.log` | le journal que lit le cron à chaque déclenchement |
| `/home/z/my-project/triade/vm/` | l'état de la VM Colab |

Ces pièces DOIVENT être sauvées par la session TRIADE elle-même (§ 4) AVANT tout arrêt du cron. Si le bac de cette session est recyclé avant cela, le script sera à reconstruire depuis REPRISE_PROJET.md (cela a déjà été fait une fois à l'Entrée 458 — c'est possible mais coûteux).

## 4. L'instruction à coller UNE FOIS dans la session TRIADE

> SAUVEGARDE DE PASSATION (commande du maître, 28/11) — le cron « TRIADE — reprise autonome de l'entraînement Colab » sera arrêté depuis une autre session. AVANT cela, porte au coffre Drive, dans le dossier dédié « passation-cron-20261128 » (déjà créé à la racine du coffre), les pièces qui ne vivent qu'au bac :
> 1. `/home/z/my-project/scripts/reprise_colab.sh` — copie INTACTE (aucune retouche), recoupée par re-téléchargement.
> 2. `/home/z/my-project/triade/` en l'état (`etat-reprise.log` + `vm/`) — zip « triade-bac-20261128.zip », copie au même dossier Drive, recoupée.
> 3. Vérifie que le jeton HuggingFace (Hugginface.txt, compte aleksickx) est bien au /Tokens du coffre ; s'il n'y est pas, dépose-le là (JAMAIS au dépôt public).
> 4. Rapporte : la liste des pièces sauvées, leurs tailles, leurs ids Drive, et le sha256 de reprise_colab.sh.
> Ne modifie rien d'autre (ni le script, ni triade/vm/, ni les registres — aucune Entrée au worklog n'est requise pour ce geste, la passation vit au dossier dédié du coffre et à la branche git passation-cron-20261128). N'arrête PAS le cron toi-même : le maître le fera depuis l'autre session une fois ta sauvegarde confirmée.

## 5. Après confirmation de la sauvegarde : arrêter le cron

Depuis n'importe quelle session du compte : outil cron, action `delete`, `jobId` **553027**. (La session TRIADE peut aussi le faire elle-même si le maître le lui demande.)

## 6. Recréer la tâche plus tard (depuis une nouvelle session)

1. **Restaurer le bac** : REPRISE_PROJET.md § 3 (pas à pas éprouvé à la vague 14) — jetons depuis le /Tokens du coffre, clone depuis le bundle ou GitHub, outils du bac.
2. **Replacer les pièces de passation** : `reprise_colab.sh` → `/home/z/my-project/scripts/`, et l'état `triade/` (`etat-reprise.log` + `vm/`) depuis ce dossier Drive.
3. **Créer le cron** avec les paramètres du fichier `CRON-TRIADE-553027-DEFINITION.json` (message VERBATIM).
4. **Vérifier** : le premier déclenchement doit exécuter le script et rapporter les 15 dernières lignes de `etat-reprise.log`.

## 7. Sécurité (règles du projet, rappel)

- Le dépôt GitHub est **PUBLIC** : aucun jeton, aucun identifiant (garde pre-commit `h66o54pjd` : empreintes + entropie).
- Les jetons vivent au **/Tokens du coffre Drive** uniquement (le compte de service `physichong` couvre la lecture).
- **D'autres sessions Colab travaillent sur d'autres projets dans ce Drive** : ne rien renommer, écraser ni supprimer en dehors de ce dossier de passation.
- Le `/livrables` et les registres (worklog, REPRISE, OU-TROUVER) appartiennent à la session TRIADE : ne pas les modifier depuis l'extérieur.
