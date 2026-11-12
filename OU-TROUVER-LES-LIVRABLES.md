# OÙ TROUVER LES LIVRABLES — TRIADE

*Mise à jour : 13/11/2026 (Entrée 256 — le kit android en APK, le test en
1 clic). Ce fichier vit à la racine du coffre Drive, au miroir
`TRIADE-sauvegarde-git/` et au bac de la session — il est tenu par
`scripts/drive_sync.py` (ROOT_PUSH).*

## La réponse courte — les livrables récents ( Entrées 251-256 )

| Livrable | Bac de la session | Coffre /test | Miroir git |
| --- | --- | --- | --- |
| Kit-2 CORRECTIF2 (zip, sha256 0e930b80…) | oui | **oui (dépôté le 13/11)** | download/ |
| Collecteur de preuves crash (zip, ea24dcdf…) | oui | — (vécu au /test : dossier kit-2-dudect) | download/ |
| Verdict crash kit-2 (LISEZMOI-VERDICT.txt, 3f4cdae0…) | oui | — | racine du dépôt |
| Diagnostic kit-2 (docx + pdf) | oui | — | download/ |
| Preuves du terrain (15 pièces, 8 + kit/7) | — | dossier kit-2-dudect (le dépôt du développeur, TEL QUEL) | preuves-crash-kit2/ |
| GUI kit-2 v1 (triade_gui.py, 06112518…) | oui | — | download/TRIADE_gui_kit2_v1/ |
| Kit Android v1 — le test en 1 clic (APK 313b60aa…, paquet b45999a0…, sources) | oui | **oui (dépôté le 13/11)** | download/TRIADE_kit_android_v1/ |

## Les livrables v0.15.0 (à la racine du coffre)

- `TRIADE_complet_v0.15.0.zip`, `TRIADE_soumission_v0.15.0.zip`,
  `TRIADE_manuscrit_v0.15.0.pdf`, `empreintes_livrables_v0.15.0.txt`.
- Les kits terrain v0150 vécus : dossiers `TRIADE_kits_terrain_v0150_*` du
  /test (MISE-A-JOUR, MISE-A-JOUR2, AUTO, CORRECTIF2-kit-shani,
  CORRECTIF2-kit-dudect, kit-2-dudect avec les preuves du run).

## Le miroir git — `TRIADE-sauvegarde-git/`

Le dépôt ENTIER (journal, worklog, tous les jalons, les livrables) +
`triade-history.bundle` (restauration à l'identique : `git clone
triade-history.bundle`) — synchronisé à chaque commit par
`scripts/drive_sync.py`, les anciens courants archivés versionnés dans
`archives-bundles/`.

## L'état (Entrée 256) — ce qui reste au développeur

1. **LA MESURE (le test du téléphone)** : le plus court geste = **l'APK**
   (download/TRIADE_kit_android_v1/ ou coffre /test) — l'installer, l'ouvrir :
   le test part tout seul, puis ENVOYER LE ZIP → Drive (Triade → test) ;
   le GUI Termux (`TRIADE_gui_kit2_v1/triade_gui.py`) demeure l'instrument
   complet si vous préférez la voie manuelle.
2. Les preuves formelles `preuves-constat-arm/` (le téléphone) — l'APK les
   produit à chaque run ; datez et signez le verdict de votre main.
3. Les gestes ouverts : le geste B SHA-NI réel, la campagne D204, la
   cérémonie d'ère, le séquestre D183, la réplication.

*Le détail complet vit au journal de travail (`docs/JOURNAL_TRAVAIL.md`,
Entrées 251-256) et au worklog (`worklog.md`, Tasks 158-163).*
