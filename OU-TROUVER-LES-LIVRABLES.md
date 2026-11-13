# OÙ TROUVER LES LIVRABLES — TRIADE

*Mise à jour : 13/11/2026 (Entrées 261-265 — la réception du run kit-2 v2 :
LA MESURE A VÉCU ; le TÉMOIN DATÉ SIGNÉ reçu et recoupé : LA CHAÎNE DU
KIT-2 FERMÉE ; la suite approuvée OUTILLÉE : LE SECOND RUN À N=400 EN
1 CLIC). Ce fichier vit à la racine du coffre Drive, au
miroir `TRIADE-sauvegarde-git/` et au bac de la session — il est tenu par
`scripts/drive_sync.py` (ROOT_PUSH).*

## La réponse courte — les livrables récents ( Entrées 251-265 )

| Livrable | Bac de la session | Coffre /test | Miroir git |
| --- | --- | --- | --- |
| Kit-2 CORRECTIF2 (zip, sha256 0e930b80…) | oui | oui | download/ |
| GUI kit-2 v1 (triade_gui.py, 06112518…) | oui | — | download/TRIADE_gui_kit2_v1/ |
| Kit Android v1 — le test en 1 clic (APK 313b60aa…) | oui | oui | download/TRIADE_kit_android_v1/ |
| LE RUN ANDROID VÉCU VERT (VERDICT + zip, 12/11 21:45 UTC) | preuves-run-kit-android-v1/ | oui (le dépôt du développeur) | download/preuves-run-kit-android-v1/ |
| Exe 1-clic kit-2 v1 (9d2ccc91… — la pièce du premier run, Entrée 259) | oui | oui | download/TRIADE_kit2_exe_1clic_v1/ |
| Les preuves du run kit-2 v1 (console capturée, Entrée 259) | preuves-run-kit2-dudect-v1/ | oui (le dépôt du développeur) | download/preuves-run-kit2-dudect-v1/ |
| Kit-2 CORRECTIF3 — l'édition corrective (zip c18b11c6…) | oui | oui (dépôté le 12/11, md5 recoupé — Entrée 263) | download/ |
| Exe 1-clic kit-2 v2 (exe e6752c58…, paquet c2887ebd…) | oui | oui (dépôté le 12/11, md5 recoupé — Entrée 263) | download/TRIADE_kit2_exe_1clic_v2/ |
| **LE RUN KIT-2 v2 — LA MESURE VÉCUE (zip 3111842a… + lecture, Entrée 261)** | preuves-run-kit2-dudect-v2/ | **oui (le dépôt du développeur + LISEZMOI-MESURE-VECUE.txt)** | download/preuves-run-kit2-dudect-v2/ |
| **LE TÉMOIN DU KIT-2 DATÉ SIGNÉ — LA CHAÎNE FERMÉE (Entrée 264)** | preuves-kit2-temoin-signe/ | **oui (le dossier du développeur, 13/11 09:04Z)** | download/preuves-kit2-temoin-signe/ |
| **LE SECOND RUN OUTILLÉ — N=400 EN 1 CLIC (Entrée 265)** | TRIADE_kit2_second_run_N400_v1/ | oui | download/TRIADE_kit2_second_run_N400_v1/ |

## Les livrables v0.15.0 (à la racine du coffre)

- `TRIADE_complet_v0.15.0.zip`, `TRIADE_soumission_v0.15.0.zip`,
  `TRIADE_manuscrit_v0.15.0.pdf`, `empreintes_livrables_v0.15.0.txt`.
- Les kits terrain v0150 vécus : dossiers `TRIADE_kits_terrain_v0150_*` du
  /test (MISE-A-JOUR, MISE-A-JOUR2, AUTO, CORRECTIF2-kit-shani,
  CORRECTIF2-kit-dudect, kit-2-dudect avec les preuves du crash).

## Le miroir git — `TRIADE-sauvegarde-git/`

Le dépôt ENTIER (journal, worklog, tous les jalons, les livrables) +
`triade-history.bundle` (restauration à l'identique : `git clone
triade-history.bundle`) — synchronisé à chaque commit par
`scripts/drive_sync.py`, les anciens courants archivés versionnés dans
`archives-bundles/`.

*NOTE (Entrée 263) : les fichiers à exe du coffre sont CACHÉS aux comptes
non propriétaires (la quarantaine malware de Drive les retire du listing du
compte de service — c'est pourquoi ils semblèrent absents à l'Entrée 261) :
le relais OAuth du coffre `Tokens/` est la vue de référence du coffre ;
JAMAIS conclure à une absence depuis le seul listing du compte de service.*

## L'état (Entrée 265) — la chaîne du kit-2 FERMÉE, le second run outillé, ce qui reste au développeur

1. **LE TÉMOIN DATÉ SIGNÉ du run kit-2 EST REÇU** (Entrée 264, le 13/11
   09:04Z) : « fait le 13/11/2026 / Alexis Lopez » sous les lignes, les
   cinq pièces de mesure jamais retouchées — LA CHAÎNE DU KIT-2 EST
   FERMÉE. Les champs demeurés vides (l'OS, le turbo EFFECTIF au BIOS, la
   fréquence réelle, les observations) sont consignés TELS QUELS — D189 :
   ils restent à votre main si vous souhaitez les compléter un jour, le
   témoin signé demeurant la pièce de référence.
2. **LE SECOND RUN KIT-2 EST OUTILLÉ EN 1 CLIC (Entrée 265)** : téléchargez
   `TRIADE_kit2_second-run_N400_v1.zip` au coffre /test, extrayez,
   double-cliquez `LANCER-SECOND-RUN-N400.bat` — il trouve l'exe v2 seul
   (Téléchargements ou Bureau s'il y vit), recoupe son sha256 (fail-closed,
   la v1 refusée nommée — la ligne 55) et le lance à N=400. Puis : déposez
   le zip des preuves au /test, datez et signez le témoin du second run.
   Il consoliderait tls13-13 (5.19, la limite n'est pas loin) et tls13-17
   (3.11) sans jamais effacer le premier témoin signé.
3. La signature à la main du verdict Android (Entrée 257) — D189 :
   rapporter tel quel.
4. Les preuves formelles `preuves-constat-arm/` (le téléphone) et les
   gestes ouverts : le geste B SHA-NI réel, la campagne D204, la
   cérémonie d'ère, le séquestre D183, la réplication.

*Le détail complet vit au journal de travail (`docs/JOURNAL_TRAVAIL.md`,
Entrées 251-265) et au worklog (`worklog.md`, Tasks 158-172).*
