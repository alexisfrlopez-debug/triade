# OÙ TROUVER LES LIVRABLES — TRIADE

*Mise à jour : 13/11/2026 (Entrée 259 — le run kit-2 relevé : le run N'A
PAS VÉCU, LA LIGNE 55 DU LANCEUR nommée sur pièces, l'édition corrective
attend le mot du développeur). Ce fichier vit à la racine du coffre Drive, au
miroir `TRIADE-sauvegarde-git/` et au bac de la session — il est tenu par
`scripts/drive_sync.py` (ROOT_PUSH).*

## La réponse courte — les livrables récents ( Entrées 251-259 )

| Livrable | Bac de la session | Coffre /test | Miroir git |
| --- | --- | --- | --- |
| Kit-2 CORRECTIF2 (zip, sha256 0e930b80…) | oui | **oui (dépôté le 13/11)** | download/ |
| GUI kit-2 v1 (triade_gui.py, 06112518…) | oui | — | download/TRIADE_gui_kit2_v1/ |
| Kit Android v1 — le test en 1 clic (APK 313b60aa…, paquet b45999a0…) | oui | oui (dépôté le 13/11) | download/TRIADE_kit_android_v1/ |
| **LE RUN ANDROID VÉCU VERT** (VERDICT + zip 4 692 o, 12/11 21:45 UTC) | preuves-run-kit-android-v1/ | **oui (le dépôt du développeur, TEL QUEL)** | download/preuves-run-kit-android-v1/ |
| **Kit-2 en EXE 1-CLIC** (exe 9d2ccc91…, paquet fb7a8389…, sources) | oui | **oui (dépôté le 13/11)** | download/TRIADE_kit2_exe_1clic_v1/ |
| **LE RUN KIT-2 RELEVÉ — PAS VÉCU** (zip 2 722 o, md5 9e697c37…, 12/11 22:15 UTC — la ligne 55 du lanceur nommée, LISEZMOI-RUN-KIT2 9d2a6349…) | preuves-run-kit2-dudect-v1/ | **oui (le dépôt du développeur, TEL QUEL)** | download/preuves-run-kit2-dudect-v1/ |

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

## L'état (Entrée 259) — ce qui reste au développeur

1. **LA MESURE KIT-2 (le test Windows) — TOUJOURS JAMAIS ENCORE COURUE** :
   le run du 12/11 au soir (l'exe 1-clic vécu, la chaîne complète) est MORT
   à LA LIGNE 55 du lanceur (`|t| > 5` : le pipe et le chevron nus dans un
   echo — cmd.exe abandonne). **NE RE-COUREZ PAS l'exe en l'état** : il
   mourra à la même ligne, à chaque fois. **DITES LE MOT** (« fais la
   correction ») : l'édition corrective naît (la 55 + la 218 échappées,
   les écarts de source 334/307), le paquet re-livré, l'exe re-généré —
   puis re-courir (double-clic, dépôt, témoin signé). La lecture vit à
   `LISEZMOI-RUN-KIT2.txt` (download/preuves-run-kit2-dudect-v1/).
2. Le GUI Termux (`TRIADE_gui_kit2_v1/triade_gui.py`) demeure l'instrument
   complet pour la voie manuelle (téléphone ou PC).
3. La signature à la main du verdict Android (le constat vécu VERT,
   Entrée 257) et du futur témoin kit-2 — D189 : rapporter tel quel.
4. Les gestes ouverts : le geste B SHA-NI réel, la campagne D204, la
   cérémonie d'ère, le séquestre D183, la réplication.

*Le détail complet vit au journal de travail (`docs/JOURNAL_TRAVAIL.md`,
Entrées 251-259) et au worklog (`worklog.md`, Tasks 158-166).*
