# OÙ TROUVER LES LIVRABLES — TRIADE

*Mise à jour : 13/11/2026 (Entrée 261 — la réception du run kit-2 v2 : LA
MESURE A VÉCU). Ce fichier vit à la racine du coffre Drive, au miroir
`TRIADE-sauvegarde-git/` et au bac de la session — il est tenu par
`scripts/drive_sync.py` (ROOT_PUSH).*

## La réponse courte — les livrables récents ( Entrées 251-261 )

| Livrable | Bac de la session | Coffre /test | Miroir git |
| --- | --- | --- | --- |
| Kit-2 CORRECTIF2 (zip, sha256 0e930b80…) | oui | oui | download/ |
| GUI kit-2 v1 (triade_gui.py, 06112518…) | oui | — | download/TRIADE_gui_kit2_v1/ |
| Kit Android v1 — le test en 1 clic (APK 313b60aa…) | oui | oui | download/TRIADE_kit_android_v1/ |
| LE RUN ANDROID VÉCU VERT (VERDICT + zip, 12/11 21:45 UTC) | preuves-run-kit-android-v1/ | oui (le dépôt du développeur) | download/preuves-run-kit-android-v1/ |
| Exe 1-clic kit-2 v1 (9d2ccc91… — la pièce du premier run, Entrée 259) | oui | sources seules (l'exe refusé par Drive) | download/TRIADE_kit2_exe_1clic_v1/ |
| Les preuves du run kit-2 v1 (console capturée, Entrée 259) | preuves-run-kit2-dudect-v1/ | oui (le dépôt du développeur) | download/preuves-run-kit2-dudect-v1/ |
| Kit-2 CORRECTIF3 — l'édition corrective (zip c18b11c6…) | oui | sources seules (le zip refusé par Drive — écart nommé à l'Entrée 261) | download/ |
| Exe 1-clic kit-2 v2 (exe e6752c58…, paquet c2887ebd…) | oui | sources seules (l'exe refusé par Drive — écart nommé à l'Entrée 261) | download/TRIADE_kit2_exe_1clic_v2/ |
| **LE RUN KIT-2 v2 — LA MESURE VÉCUE (zip 3111842a… + lecture, Entrée 261)** | preuves-run-kit2-dudect-v2/ | **oui (le dépôt du développeur + LISEZMOI-MESURE-VECUE.txt)** | download/preuves-run-kit2-dudect-v2/ |

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

## L'état (Entrée 261) — ce qui reste au développeur

1. **LE TÉMOIN SIGNÉ du run kit-2** (le seul geste qui ferme la chaîne du
   kit-2) : complétez temoin-dudect-BROUILLON.txt (l'état EFFECTIF du
   turbo au BIOS, vos observations mêmes défavorables — D189), datez,
   signez, déposez-le au coffre /test. Le run v2 du 13/11 (08:14 UTC) est
   REÇU, recoupé et consigné (Entrée 261) : LA MESURE, jamais encore
   courue depuis v0.15.0, EST COURUE — tls13-02 |t|=12.39 et tls13-13
   |t|=5.19 > 5 (dépendances au seuil), tls13-16 |t|=0.94 et tls13-17
   |t|=3.11 <= 5.
2. Un second run kit-2 (optionnel) : l'exe v2 accepte N en argument (ex.
   « 400 », minimum 60) — il consoliderait tls13-13 (5.19, la limite
   n'est pas loin) sans jamais effacer le premier témoin.
3. La signature à la main du verdict Android (Entrée 257) — D189 :
   rapporter tel quel.
4. Les preuves formelles `preuves-constat-arm/` (le téléphone) et les
   gestes ouverts : le geste B SHA-NI réel, la campagne D204, la
   cérémonie d'ère, le séquestre D183, la réplication.

*Le détail complet vit au journal de travail (`docs/JOURNAL_TRAVAIL.md`,
Entrées 251-261) et au worklog (`worklog.md`, Tasks 158-168).*
