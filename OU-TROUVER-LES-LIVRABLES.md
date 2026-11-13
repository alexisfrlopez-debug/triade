# OÙ TROUVER LES LIVRABLES — TRIADE

*Mise à jour : 13/11/2026 (Entrées 261-269 — la réception du run kit-2 v2 :
LA MESURE A VÉCU ; le TÉMOIN DATÉ SIGNÉ reçu et recoupé : LA CHAÎNE DU
KIT-2 FERMÉE ; la suite approuvée OUTILLÉE : LE SECOND RUN À N=400 EN
1 CLIC ; LE SECOND TÉMOIN SIGNÉ (N=400) REÇU — la chaîne DOUBLEMENT
fermée ; LES TESTS CLOS ARCHIVÉS (44 entrées, le /test rendu à la
suite) ; LE TÉMOIN DU VERDICT ANDROID DÉPOSÉ pour signature ; le TÉMOIN ANDROID SIGNÉ REÇU — la chaîne constat-arm FERMÉE, Entrée 267 ; L'ARBITRAGE DE LA FAMILLE « [m » — Entrée 268 : les « étiquettes tronquées » étaient des artefacts de lecture, AUCUNE pièce fautive ; LES GESTES OUVERTS OUTILLÉS EN 1 CLIC — Entrée 269 : le paquet TRIADE_kits_1clic_gestes_ouverts_v1, chaque geste ouvert en un double-clic). Ce fichier
vit à la racine du coffre Drive, au miroir `TRIADE-sauvegarde-git/` et
au bac de la session — il est tenu par `scripts/drive_sync.py`
(ROOT_PUSH).*

## La réponse courte — les livrables récents ( Entrées 251-267 )

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
| **LE SECOND RUN OUTILLÉ — N=400 EN 1 CLIC (Entrée 265)** | TRIADE_kit2_second_run_N400_v1/ | oui (archivé à kits-terrain-v0150/ — le run est couru) | download/TRIADE_kit2_second_run_N400_v1/ |
| **LE SECOND TÉMOIN SIGNÉ — N=400, LA CHAÎNE DOUBLEMENT FERMÉE (Entrée 266)** | preuves-kit2-second-temoin-signe/ | **oui (le dossier du développeur, 13/11 10:38Z — les quatre \|t\| sous le seuil)** | download/preuves-kit2-second-temoin-signe/ |
| **LE TÉMOIN DU VERDICT ANDROID SIGNÉ — LA CHAÎNE DU CONSTAT-ARM FERMÉE (Entrée 267)** | temoin-android-signe/ | **oui (temoin-verdict-android/, QUATRE pièces — le signé du développeur, 13/11 11:14Z)** | download/temoin-android-signe/ |
| **LES GESTES OUVERTS EN 1 CLIC — le paquet des suites proposées (Entrée 269 : geste B, voies QEMU, campagne D204, séquestre D183, réplication — zip 878889c9…)** | TRIADE_kits_1clic_gestes_ouverts_v1/ | **oui (le zip + le LISEZMOI, md5 recoupés)** | download/TRIADE_kits_1clic_gestes_ouverts_v1/ |

## Les livrables v0.15.0 (à la racine du coffre)

- `TRIADE_complet_v0.15.0.zip`, `TRIADE_soumission_v0.15.0.zip`,
  `TRIADE_manuscrit_v0.15.0.pdf`, `empreintes_livrables_v0.15.0.txt`.
- Les kits terrain v0150 vécus : les itérations MULTIMACHINES →
  CORRECTIF → CORRECTIF2 et le kit CORRECTIF3 final vivent désormais aux
  archives du /test (`archives-livraisons/kits-terrain-v0150/`, Entrée
  266 — la salle et son LISEZMOI) ; le kit loupe-13 (campagne D204)
  demeure au /test.

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
JAMAIS conclure à une absence depuis le seul listing du compte de
service.*

*NOTE (Entrée 268) : une étiquette « tronquée » dans un texte ou une sortie ne se lit JAMAIS à l'œil — l'affichage du labo avale la séquence 5b 6d (« [m ») suivie d'une lettre (« achine] », « anifeste] », « utation K] » : trois artefacts, zéro pièce fautive, Entrées 260 et 268) : dump od ou comptage aveugle, toujours.

*NOTE (Entrée 267) : un listing de dossier peut RETARDER — la pièce
signée du 13/11 11:14Z ne parut au listing de son dossier que
~15 min plus tard, visible par la recherche par nom dès 11:19Z : on
CROISE les canaux (listing, recherche par nom, lecture directe de la
pièce) AVANT de conclure à une absence.*

## L'état (Entrée 268) — les chaînes kit-2 ET constat-arm fermées par la main, la famille des étiquettes arbitrée : AUCUNE pièce fautive

1. **LES DEUX TÉMOINS SIGNÉS du kit-2 SONT REÇUS** : N=200 (Entrée 264,
   le 13/11 09:04Z — « fait le 13/11/2026 / Alexis Lopez ») et N=400
   (Entrée 266, le 13/11 10:38Z — « fait le 13/11/2026 / Alexis LOPEZ »,
   85 s après le run). Au N=400 : tls13-02 |t|=0.84, tls13-13 |t|=1.55,
   tls13-16 |t|=-0.30, tls13-17 |t|=2.02 — LES QUATRE sous le seuil, les
   dépendances du premier run DISSIPÉES (la lecture honnête demeure :
   aucune divergence au seuil sur cet échantillon, cette machine — jamais
   « temps constant prouvé »). Les deux dossiers signés demeurent au /test
   — D99, jamais effacés.
2. **LES TESTS CLOS SONT ARCHIVÉS (Entrée 266)** : 44 entrées du /test
   déplacées aux salles d'archives (jamais jetées — D143) — 17 preuves et
   runs clos à `archives-preuves/`, 27 livraisons et outils à la salle
   nouvelle `archives-livraisons/kits-terrain-v0150/`. Le /test porte
   DÉSORMAIS 15 entrées vivantes : les deux témoins signés, la chaîne
   Android, le kit loupe-13, les registres de cérémonie, les salles — et
   le témoin du verdict android.
3. **LE TÉMOIN DU VERDICT ANDROID EST SIGNÉ ET RECOUPÉ (Entrée 267)** :
   la main du 13/11 11:14Z (« fait le 13/11/2026 / Alexis Lopez » — la
   même main que le premier témoin kit-2), le VERDICT joint ==
   l'original du run 12/11 octet pour octet, la date JAMAIS avant le
   run, la zone d'observations demeurée vide (D189 tel quel) — LA
   CHAÎNE DU CONSTAT-ARM FERMÉE, du téléphone au coffre. La portée
   D206 demeure : le constat ne mesure rien.
4. Les preuves formelles `preuves-constat-arm/` (le téléphone — l'APK
   demeure au /test) et les gestes ouverts : le geste B SHA-NI réel, la
   campagne D204 (le kit loupe-13 demeure au /test), la cérémonie d'ère,
   le séquestre D183, la réplication.

*Le détail complet vit au journal de travail (`docs/JOURNAL_TRAVAIL.md`,
Entrées 251-268) et au worklog (`worklog.md`, Tasks 158-175).*
