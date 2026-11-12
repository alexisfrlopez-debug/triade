# OÙ TROUVER LES LIVRABLES — TRIADE

*Mise à jour : 13/11/2026 (Entrées 259-260 — le relevé du run kit-2 : la
ligne 55 du lanceur nommée sur pièces ; l'édition corrective CORRECTIF3 +
l'exe 1-clic v2). Ce fichier vit à la racine du coffre Drive, au miroir
`TRIADE-sauvegarde-git/` et au bac de la session — il est tenu par
`scripts/drive_sync.py` (ROOT_PUSH).*

## La réponse courte — les livrables récents ( Entrées 251-260 )

| Livrable | Bac de la session | Coffre /test | Miroir git |
| --- | --- | --- | --- |
| Kit-2 CORRECTIF2 (zip, sha256 0e930b80…) | oui | oui | download/ |
| GUI kit-2 v1 (triade_gui.py, 06112518…) | oui | — | download/TRIADE_gui_kit2_v1/ |
| Kit Android v1 — le test en 1 clic (APK 313b60aa…) | oui | oui | download/TRIADE_kit_android_v1/ |
| LE RUN ANDROID VÉCU VERT (VERDICT + zip, 12/11 21:45 UTC) | preuves-run-kit-android-v1/ | oui (le dépôt du développeur) | download/preuves-run-kit-android-v1/ |
| Exe 1-clic kit-2 v1 (9d2ccc91… — la pièce du premier run, Entrée 259) | oui | oui | download/TRIADE_kit2_exe_1clic_v1/ |
| Les preuves du run kit-2 v1 (console capturée, Entrée 259) | preuves-run-kit2-dudect-v1/ | oui (le dépôt du développeur) | download/preuves-run-kit2-dudect-v1/ |
| **Kit-2 CORRECTIF3 — L'ÉDITION CORRECTIVE** (zip c18b11c6…) | oui | **oui (dépôté le 13/11)** | download/ |
| **Exe 1-clic kit-2 v2 — LE GESTE LE PLUS COURT** (exe e6752c58…, paquet c2887ebd…) | oui | **oui (dépôté le 13/11)** | download/TRIADE_kit2_exe_1clic_v2/ |

## Les livrables v0.15.0 (à la racine du coffre)

- `TRIADE_complet_v0.15.0.zip`, `TRIADE_soumission_v0.15.0.zip`,
  `TRIADE_manuscrit_v0.15.0.pdf`, `empreintes_livrables_v0.15.0.txt`.
- Les kits terrain v0150 vécus : dossiers `TRIADE_kits_terrain_v0150_*` du
  /test (MISE-A-JOUR, MISE-A-JOUR2, AUTO, CORRECTIF2-kit-shani,
  CORRECTIF2-kit-dudect, CORRECTIF3-kit-dudect, kit-2-dudect avec les
  preuves du run).

## Le miroir git — `TRIADE-sauvegarde-git/`

Le dépôt ENTIER (journal, worklog, tous les jalons, les livrables) +
`triade-history.bundle` (restauration à l'identique : `git clone
triade-history.bundle`) — synchronisé à chaque commit par
`scripts/drive_sync.py`, les anciens courants archivés versionnés dans
`archives-bundles/`.

## L'état (Entrée 260) — ce qui reste au développeur

1. **LA MESURE KIT-2 (le test Windows — JAMAIS ENCORE COURUE)** : le plus
   court geste = **L'EXE 1-CLIC V2** (download/TRIADE_kit2_exe_1clic_v2/
   ou coffre /test) — le DOUBLE-CLIQUER : le test part seul (l'épreuve
   d'appel FIPS abc, puis LE RUN N=200 : la mesure prend des minutes), le
   zip des preuves naît sur le Bureau, l'explorateur et le coffre /test
   s'ouvrent — déposez le zip, complétez et signez le témoin. Si le
   navigateur refuse l'exe nu (faux positif « malware »), prenez le
   paquet `TRIADE_kit2_exe_1clic_v2.zip` (le porteur). La cause du run
   v1 est RÉPARÉE (la ligne 55 du lanceur, l'Entrée 259) : la v2 porte
   l'édition CORRECTIF3.
2. Le GUI Termux (`TRIADE_gui_kit2_v1/triade_gui.py`) demeure l'instrument
   complet pour la voie manuelle (téléphone ou PC).
3. La signature à la main du verdict Android (Entrée 257) et du futur
   témoin kit-2 — D189 : rapporter tel quel.
4. Les gestes ouverts : les preuves-constat-arm, le geste B SHA-NI réel,
   la campagne D204, la cérémonie d'ère, le séquestre D183, la
   réplication.

*Le détail complet vit au journal de travail (`docs/JOURNAL_TRAVAIL.md`,
Entrées 251-260) et au worklog (`worklog.md`, Tasks 158-167).*
