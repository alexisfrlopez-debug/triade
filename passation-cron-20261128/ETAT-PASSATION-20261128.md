# ÉTAT DE LA PASSATION — complément du 28/11 2026, ~15h45 (Paris)

**Rédigé depuis la session de passation** (distincte de la session TRIADE) à la demande du maître, après le constat suivant : le cron n° 553027 **ne peut pas être modifié à distance** (l'outil planifié refuse l'action `update` ; supprimer + recréer déplacerait la tâche vers la session qui la crée, donc vers un bac sans les fichiers TRIADE). Ce fichier complète `PASSATION-20261128.md`. Il ne touche NI au worklog NI à `REPRISE_PROJET.md` : la garde prescriptive (D262, liste blanche `SOURCES-PRESCRIPTIVES.txt`) verrouille ces registres par empreinte — les modifier depuis l'extérieur casserait la relance.

## 1. L'état du projet à l'instant présent (Entrée 463 du worklog, 13:48 UTC — la plus récente)

- **Le run du maître (v1062, graine 20261128) a été refusé au premier exemple encore** : EXEMPLE-LONG-OOM, 912,00 MiB refusés à `peft/tuners/lora/bnb.py:549` — le chemin fp32 de peft sur le MLP, plus l'allocateur né sans ses segments extensibles (noyau recyclé du matin, 1,64 Gio réservés-non-alloués).
- **Le geste correctif est fait et prouvé** (trois prongs : la cane fail-closed NOYAU-SALE, l'autocast fp16 du pas, l'hygiène `empty_cache` + pic mesuré ; preuve au bac en quatre passes — Δperte 0,0 exact, gradients ≈ 5e-03 relatif, cosinus 0,999998).
- **Livrés au /livrables** : LE KIT v1062 (`TRIADE_kit_entrainement_v1062.zip`, 2 134 909 o, id `1_P3hsysyE6fZGAdDP3caPk_OWXxHq66e`) et LE NOTEBOOK v1063 (`Entrainement-Colab-v1063-VIVANTE.ipynb`, 65 082 o, id `11G2fWojfoodPMpa8Zwor_VBMHlxShniN`). Les supersédées (v1062-VIVANTE, kit v1061) sont archivées au lot `livrables_supersedes_20261128_terrain12`.
- **LA PAROLE AU MAÎTRE (à faire au navigateur)** : REDÉMARRER LA SESSION D'ABORD (Exécution → Redémarrer la session — la cane refusera un noyau recyclé, c'est le dessein), PUIS rouvrir la **v1063** au /livrables et « Tout exécuter ». L'entraînement est DÉTERMINISTE (graine 20261128, ordre des longs d'abord) ; le journal vivant porte le pic à chaque pas.
- **SUITE prévue** : les vigies du jour (16h et 18h Paris) ; si le terrain refuse encore sur un processus CUDA-vierge, le repli (exclusion des monstres) revient au labo avec le pic mesuré ; PUIS la feuille de route de l'Entrée 461 (packs Zenodo v0.34.x, repo HuggingFace `aleksickx`, fine-tuning v107).

## 2. L'état de la passation elle-même

| Pièce | État |
|---|---|
| Kit de passation au coffre Drive (dossier `passation-cron-20261128`) | FAIT — PASSATION-20261128.md + CRON-TRIADE-553027-DEFINITION.json (recoupés) |
| Branche GitHub `passation-cron-20261128` (dépôt alexisfrlopez-debug/triade) | FAIT — les deux mêmes fichiers poussés, main intact |
| Registres au coffre (worklog, REPRISE_PROJET.md) | À JOUR à l'Entrée 463 (13:48–13:51 UTC) — tenus par la session TRIADE |
| Pièces du bac (`scripts/reprise_colab.sh`, `triade/` en zip) | **EN ATTENTE — seule la session TRIADE peut les sauver** |
| Modification du cron 553027 à distance | **IMPOSSIBLE** (update refusé ; delete+create = reroutage vers la session créatrice) |
| Jeton HuggingFace au /Tokens du coffre | à vérifier au moment de la sauvegarde (consigne incluse au texte à coller) |

## 3. Les deux voies pour terminer

**VOIE A (recommandée — aucune perte).** Le maître colle dans la session TRIADE le texte du § 4 de `PASSATION-20261128.md` (version étendue du 28/11 au soir, reproduite ci-dessous). Même si la session affiche « busy due to another request » : le message sera traité dès la fin du tour en cours du cron (les tours s'enchaînent toutes les 10 minutes) ; sinon réessayer dans la fenêtre libre entre deux déclenchements. La session TRIADE sauvegarde les pièces du bac, consigne l'Entrée « PASSATION » au worklog, met REPRISE_PROJET.md à jour, pousse et rafraîchit le miroir. Le maître confirme, puis la tâche 553027 est supprimée (depuis n'importe quelle session : outil planifié, action supprimer, jobId 553027).

**VOIE B (si écrire dans la session TRIADE s'avère impossible).** On accepte la perte des pièces du bac — elles sont reconstruisibles : le script `reprise_colab.sh` a déjà été reconstruit une fois après recyclage (Entrée 458 ; la méthode est documentée à `REPRISE_PROJET.md` § 3). Le maître fait supprimer la tâche 553027, puis la relance depuis une nouvelle session suit `PASSATION-20261128.md` § 6 : restauration du bac (jetons au /Tokens du coffre, clone depuis GitHub ou le bundle miroir), reconstruction du script, initialisation de `triade/`, création du cron (message VERBATIM du fichier de définition). Coût : la reconstruction du script et la perte de l'état `vm/` courant.

## 4. Le texte à coller dans la session TRIADE (voie A)

> SAUVEGARDE DE PASSATION (commande du maître, 28/11 au soir) — le cron « TRIADE — reprise autonome de l'entraînement Colab » sera arrêté depuis une autre session. AVANT cela :
> 1. Porte au coffre Drive, dans le dossier dédié « passation-cron-20261128 » (id 1aJJzgtfCz48-vMOSzw9mEyCMmRFwlH-_) : (a) `/home/z/my-project/scripts/reprise_colab.sh` — copie INTACTE (aucune retouche), recoupée par re-téléchargement ; (b) `/home/z/my-project/triade/` en l'état (`etat-reprise.log` + `vm/`) — zip « triade-bac-20261128.zip », recoupé par re-téléchargement.
> 2. Vérifie que le jeton HuggingFace (Hugginface.txt, compte aleksickx) est bien au /Tokens du coffre ; s'il n'y est pas, dépose-le là (JAMAIS au dépôt public).
> 3. Consigne l'état (commande du maître) : une Entrée « PASSATION » au worklog et la mise à jour de REPRISE_PROJET.md — l'état exact du projet (l'Entrée 463 ; le run à relancer par le maître sur la v1063 APRÈS redémarrage de session ; les vigies 16h/18h Paris), les pièces sauvées au point 1, la procédure de relance (PASSATION-20261128.md, au coffre et à la branche git passation-cron-20261128). Pousse le tout sur git main comme d'habitude et rafraîchis le miroir au coffre (worklog.md, REPRISE_PROJET.md, bundle TRIADE-sauvegarde-git).
> 4. Rapporte : la liste des pièces sauvées, leurs tailles, leurs ids Drive, le sha256 de reprise_colab.sh, et le sha du commit git.
> Ne modifie rien d'autre (ni le script, ni triade/vm/, ni le plan gelé). N'arrête PAS le cron toi-même : le maître le fera depuis l'autre session une fois ta sauvegarde confirmée.

## 5. Après la sauvegarde confirmée (les deux voies)

Arrêter la tâche : outil planifié, action supprimer, jobId **553027** — depuis n'importe quelle session du compte. La relance ultérieure : `PASSATION-20261128.md` § 6 (restauration du bac, pièces, cron, vérification). Les vigies du jour (16h, 18h Paris) sont à reprendre par la session qui relance, tant que le run du maître n'est pas terminé.
