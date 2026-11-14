#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA CONSIGNATION de l'Entrée 289 + Task 196 : LES DEUX DÉPÔTS DE
LA MAIN REÇUS ET RECOUPÉS (la commande du développeur : « vérifie les dépôts
dans /test puis go pour la suite ») — LA CONSOLE DU REFUS ENFIN DÉPOSÉE (la
pièce demandée depuis la 286 : 3 250 o, UTF-16, l'access violation à
L'ADRESSE EXACTE 0x7FFA23900094, la base 0x7ff9b74d0000, T0 VERT, les
QUATRE exports — le kit terrain == l'archivé OCTET POUR OCTET, 11/11 pièces
+ 10/10 gravure) ; LE RETOUR D'ATELIER lu honnêtement (la ligne C ABSENTE de
livraisons.csv — l'onglet 5 n'a pas été fait ; l'état des runs et le log
114216 consignent la session C) ; LES DEUX DÉPÔTS RANGÉS à l'archive
(déplacés, jamais jetés) ; LA SUITE : LOUPE-02 LIRE, aux deux bras."""
import pathlib
import shutil

REPO = pathlib.Path("/home/z/my-project/work/triade")
SCRIPTS = pathlib.Path("/home/z/my-project/scripts")
BAC = pathlib.Path("/home/z/my-project/download")

WORKLOG = """

Task ID: 196
Agent: Z.ai (agent principal — la session des dépôts de la main : la console du refus et le retour d'atelier)
Task: LA COMMANDE DU DÉVELOPPEUR (« vérifie les dépôts dans /test puis go pour la suite ») : LES DEUX dépôts reçus (14:04:35 le kit terrain du refus, 14:09:16 le retour d'atelier), recoupés byte-byte ; LA CONSOLE DU REFUS — la pièce demandée depuis l'Entrée 286 — ENFIN DÉPOSÉE ET TENUE ; L'ÉCART NOMMÉ : la ligne C de livraisons.csv demeure ABSENTE (le geste onglet 5 n'a pas été fait) ; LES DEUX dépôts rangés à l'archive (31+2 déplacements au total, 0 suppression) ; PUIS LA SUITE OUVERTE : LOUPE-02 LIRE, aux deux bras.

Work Log:
- LA SONDE (82) : la racine portait 13 entrées (l'attendu 288 = 11) — les DEUX dépôts de la main : /test/kit-unite-loupe-01-C-20261114/ (né 14:04:35, la copie TERRAIN du kit C v1 AVEC la console du refus) et /test/test/ (né 14:09:16, l'instantané du dossier test de la machine — le retour d'atelier) ; 153 pièces nées après le bornage (le LISEZMOI-NETTOYAGE, dernier geste 288) ; RIEN disparu.
- LE RECOUP DU KIT TERRAIN (83-A) : les DOUZE pièces listées ; les ONZE pièces du kit == l'original ARCHIVÉ (unite-01-loupe-20261114/kit-unite-loupe-01-C-20261114/) OCTET POUR OCTET (EMPREINTES dbc94a82…, LANCEUR 29bdae2f…, LISEZMOI b06f859b…, loupe-01-c.c 860ff1cf…, loupe-01-c.def c0c9b9f4…, loupe-01-c.dll 85b34ed4…, scenario-unite01C.py a21c5e19… — le v1 avec la faute —, les QUATRE témoins df7e70e5…/3396717b…/c5fc1f28…/e3b0c442…) et les DIX à la gravure EMPREINTES 10/10 — LE KIT QUI A REFUSÉ == LE KIT LIVRÉ, la chaîne tenue d'un bout à l'autre ; la seule pièce propre au terrain : run-console-unite01C.txt (3 250 o, modifiée 12:29:25 — l'heure du refus).
- LA CONSOLE DU REFUS (la pièce demandée aux 286/287/288) : 3 250 o, sha256 4e76630b765af50f…, UTF-16 BOM, 26 lignes — T0 VERT (la pièce 85b34ed4… == la gravure du kit), l'image cartographiée DONT_RESOLVE @ 0x7ff9b74d0000 (LA BASE DU REFUS), les QUATRE exports découverts, puis l'échec : l'enrobage RemoteException de PowerShell, la pile python EXACTE (ligne 214 nom_dll = lire_chaine(base, lire_u32(base, desc + 12)) ; ligne 126 lire_octets ; ligne 113 ctypes.memmove) et « OSError: exception: access violation reading 0x00007FFA23900094 » — L'ADRESSE EXACTE de l'autopsie 286 (0x6c430094 + la base 0x7ff9b74d0000), la faute au labo confirmée SUR LA PIÈCE ; versée au bac (download/preuves-refus-C-v1/run-console-unite01C-refus-v1-terrain.txt).
- LES DEUX ÉCARTS NOMMÉS de la console, honnêtes : ① le fichier NE PORTE PAS la ligne « === LE RUN… (code 1) === » — elle vivait au TERMINAL (l'écho du lanceur après le code 1), collée au chat à la 286 et consignée au bac : le fichier Tee est la sortie de python SEULE, la pièce officielle ; ② la pièce du chat (2 693 o, 36 lignes vives) contre le fichier (25 lignes vives) : 20 lignes communes, 5 lignes du fichier coupées par la largeur du chat, les 11 lignes du chat absentes du fichier = l'enrobage PowerShell + l'écho du lanceur — le fichier EST la vérité, l'écart consigné.
- LE RETOUR D'ATELIER (83-B, l'instantané test/ de la machine) : livraisons.csv (853 o) == LE MIROIR PRÉ-C OCTET POUR OCTET — LA LIGNE C (C-loupe-01-it1) DEMEURE ABSENTE : le geste de recoup de livraison (l'onglet 5 du GUI) n'a pas été fait pour le bras C ; le carnet M3 ne porte que la ligne T (cristallisation 85 min) ; defauts.csv vide ; l'état des runs etat-tous-runs.json (modifié 12:55:34 — L'HEURE DU RUN C) porte l'unité C-loupe-01 (kit = kit-unite-loupe-01-C-20261114-v2, dernier_run = preuves-unite01C) ; le log NEUF tous_runs_gui_20261114-114216.log (4 194 o, 11:42:16 → 14:07:58) consigne la session : le kit T recoupé, le run T consigné, le kit T relancé, « le coffre /test est ouvert au navigateur — le renvoi du dossier ENTIER appartient à votre main » ; le log 013458 == le miroir (inchangé) ; l'atelier visé par l'état est le 012347 (la copie imbriquée vide, la 285) — le livre 013520 n'a pas été touché par la session C. LA LIGNE C RESTE À LA MAIN DU DÉVELOPPEUR (onglet 5) — le labo ne fabrique JAMAIS une ligne de mesure.
- LE RANGEMENT (83-C, 84) : les DEUX dépôts DÉPLACÉS à l'archive (addParents/removeParents — JAMAIS une suppression, la corbeille jamais touchée) : kit-unite-loupe-01-C-20261114/ → /archives-livraisons/unite-01-loupe-20261114/console-refus-v1-terrain-20261114/ (la pièce d'un refus ne se jette jamais — D143) ; test/ → /archives-livraisons/unite-01-loupe-20261114/atelier-retour-ligne-C-20261114/ ; APRÈS : la racine re-listée == les ONZE entrées attendues EXACTEMENT ; la console du refus, loupe-01-c.dll (85b34ed4…), livraisons.csv et etat-tous-runs.json re-téléchargés DE l'archive == le bac byte-byte ; l'archive unite-01 porte 9 entrées.
- LA CONSIGNATION : la présente Entrée 289 + Task 196 ; la carte OU-TROUVER portée à 289 ; l'atelier depots-289/ au dépôt (la sonde 82, le recoup 83, la vérification 84, la console du refus et les pièces d'atelier au bac versées).
- SUITE : « go pour la suite » — LOUPE-02 LIRE, aux deux bras (la deuxième tâche contrôlée du plan a78caf8c…, la troisième unité) : le labo construit les kits (oracle écrit-avant-code, la notation T au slot i110002 0x4240/320, le source C gcc -O2), les éprouve au POSIX, les livre au /test.
"""

JOURNAL = """

## Entrée 289 — LES DEUX DÉPÔTS DE LA MAIN REÇUS ET RECOUPÉS : LA CONSOLE DU REFUS ENFIN DÉPOSÉE (L'ADRESSE EXACTE TENUE), LA LIGNE C DE L'ATELIER NOMMÉE ABSENTE, LES DEUX DÉPÔTS RANGÉS (l'annonce du développeur : « vérifie les dépôts dans /test puis go pour la suite »)

- LA SONDE (82) : la racine à 13 entrées — les DEUX dépôts de la main : /test/kit-unite-loupe-01-C-20261114/ (14:04:35, la copie TERRAIN du kit C v1 AVEC la console du refus) et /test/test/ (14:09:16, l'instantané du dossier test de la machine — le retour d'atelier) ; RIEN disparu des onze attendues.

- LE KIT TERRAIN (83-A) : les ONZE pièces du kit == l'original archivé OCTET POUR OCTET (la dll 85b34ed4…, le scénario v1 a21c5e19… — celui qui porte la faute —, la gravure 10/10) — LE KIT QUI A REFUSÉ == LE KIT LIVRÉ. LA CONSOLE DU REFUS (3 250 o, 4e76630b…, UTF-16, 26 lignes) : T0 VERT, l'image @ 0x7ff9b74d0000, les QUATRE exports, la pile python EXACTE (214 → 126 → 113) et « access violation reading 0x00007FFA23900094 » — L'ADRESSE EXACTE de l'autopsie 286, la faute au labo confirmée SUR LA PIÈCE ; versée au bac. DEUX écarts nommés, honnêtes : le fichier ne porte PAS la ligne « (code 1) » (elle vivait à l'écho du lanceur, au terminal, collée au chat à la 286) ; la pièce du chat (36 lignes vives) enveloppait le fichier (25 lignes vives, 20 communes) — le fichier Tee EST la vérité.

- LE RETOUR D'ATELIER (83-B) : livraisons.csv == LE MIROIR PRÉ-C OCTET POUR OCTET — LA LIGNE C (C-loupe-01-it1) DEMEURE ABSENTE (le geste onglet 5 n'a pas été fait) ; le carnet M3 : la ligne T seule ; defauts vide ; etat-tous-runs.json (modifié 12:55:34, l'heure du run C) porte l'unité C-loupe-01 (kit v2 → preuves-unite01C) ; le log NEUF 114216 consigne la session et l'ouverture du coffre au navigateur ; le log 013458 inchangé. LA LIGNE C RESTE À LA MAIN DU DÉVELOPPEUR — le labo ne fabrique jamais une ligne de mesure ; l'écart nommé, jamais maquillé.

- LE RANGEMENT (83-C, 84) : les DEUX dépôts DÉPLACÉS (jamais jetés) — le kit terrain à console-refus-v1-terrain-20261114/ (D143 : la pièce d'un refus ne se jette jamais), l'instantané à atelier-retour-ligne-C-20261114/, SOUS l'archive de l'unité close ; la racine == les ONZE attendues EXACTEMENT ; la console, la dll, livraisons.csv et l'état re-téléchargés de l'archive == le bac byte-byte.

- LA CONSIGNATION : l'Entrée 289 + Task 196 ; la carte OU-TROUVER portée à 289 ; l'atelier depots-289/ versé au dépôt. (14/11, la session des dépôts de la main — la console du refus attendue depuis la 286 EST LIVRÉE, la ligne C attend sa main)

- SUITE : LOUPE-02 LIRE, aux deux bras — la deuxième tâche contrôlée du plan a78caf8c… : le labo construit (l'oracle écrit-avant-code, la notation T, le source C), éprouve au POSIX et livre les DEUX kits au /test.
"""

ITEM_16 = """
16. **LES DEUX DÉPÔTS DE LA MAIN RECOUPÉS — LA CONSOLE DU REFUS TENUE, LA LIGNE C NOMMÉE ABSENTE (Entrée 289)** : le kit terrain du refus (14:04:35, 12 pièces — les ONZE du kit == l'archivé byte-byte, la gravure 10/10 : le kit qui a refusé == le kit livré) porte LA CONSOLE DU REFUS (3 250 o, 4e76630b…, UTF-16 : T0 VERT, l'image @ 0x7ff9b74d0000, les QUATRE exports, la pile 214→126→113, « access violation reading 0x00007FFA23900094 » — L'ADRESSE EXACTE de la 286 ; le fichier ne porte pas l'écho « (code 1) » du terminal, nommé) ; le retour d'atelier (14:09:16) : livraisons.csv == le miroir pré-C byte-byte — LA LIGNE C DEMEURE ABSENTE (l'onglet 5 n'a pas été fait, la ligne reste à la main du développeur), l'état des runs (12:55:34) et le log 114216 consignent la session C ; les DEUX dépôts RANGÉS à /archives-livraisons/unite-01-loupe-20261114/ (console-refus-v1-terrain-20261114/ et atelier-retour-ligne-C-20261114/ — déplacés, jamais jetés), la racine == les ONZE attendues ; LA SUITE : LOUPE-02 LIRE, aux deux bras.
"""

with open(REPO / "worklog.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(WORKLOG)
with open(REPO / "docs" / "JOURNAL_TRAVAIL.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(JOURNAL)

carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
txt = carte.read_text(encoding="utf-8")
txt = txt.replace("Entrées 251-288", "Entrées 251-289")
txt = txt.replace("Tasks 158-195", "Tasks 158-196")
if not txt.endswith("\n"):
    txt += "\n"
txt += ITEM_16
carte.write_text(txt, encoding="utf-8", newline="\n")
print("[consigné] worklog.md + docs/JOURNAL_TRAVAIL.md + la carte OU-TROUVER — "
      "l'Entrée 289 + Task 196")

# ---- l'atelier depots-289/ -------------------------------------------------------
dest = REPO / "scripts" / "campagne_d204" / "depots-289"
(dest / "epreuves").mkdir(parents=True, exist_ok=True)
for nom in ["82_sonde_test.py", "83_recoupe_depot.py", "84_verifie_rangement.py"]:
    shutil.copy2(SCRIPTS / nom, dest / nom)
    print(f"[atelier] {nom} versé")
shutil.copy2(SCRIPTS / "82_arborescence_test.txt", dest / "82_arborescence_test.txt")
bac_console = BAC / "preuves-refus-C-v1" / "run-console-unite01C-refus-v1-terrain.txt"
shutil.copy2(bac_console, dest / "epreuves" / "run-console-unite01C-refus-v1-terrain.txt")
for nom in ["livraisons.csv", "carnet_temps_humain.csv", "defauts.csv",
            "journal-ouverture.txt", "etat-tous-runs.json",
            "tous_runs_gui_20261114-114216.log"]:
    shutil.copy2(BAC / "atelier-retour-C-20261114" / nom,
                 dest / "epreuves" / nom)
print("[atelier] epreuves/ : la console du refus + les sept pièces d'atelier")
