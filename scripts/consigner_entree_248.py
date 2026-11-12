#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree_248.py — LE DÉPÔT KIT TERRAIN REÇU : l'Entrée 248 au
journal de travail et la Task 155 au worklog.

L'annonce (le développeur, 12/11/2026) : « dossier kit terrain avec preuves
déposé dans /test du drive » — les deux premiers runs du paquet AUTO :
kit-1 shani (ALEKPC, refus T0.silicium encore) et kit-3 loupe (Windows 11,
VERT SUR PIÈCES, le treizième run terrain).

Append-only : les fins VÉRIFIÉES avant écriture, les rejeus REFUSÉS. Le
rapport de recoupement (26/26 VERT, sha256 7168ca81…) et les TROIS preuves
de run contrôlés AVANT toute écriture — la consignation ne peut pas
précéder ses preuves.
"""

import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")

PREUVES = REPO / "preuves-depot-auto-terrain"
RAPPORT = PREUVES / "recoupement-depot-kit-terrain.txt"
RAPPORT_SHA = ("7168ca81077b60cc81a1ea488317a40718ba20d98890b16159ffa3cc26f"
               "64d38")
VERDICT = (PREUVES / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_"
           "pc-windows_kit-1-shani_preuves-shani_VERDICT-run-shani.txt")
JOURNAL_RUN = (PREUVES / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_"
               "pc-windows_kit-1-shani_preuves-shani_scenario-shani-journal"
               ".log")
TEMOIN_LOUPE = (PREUVES / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_"
                "pc-windows_kit-3-terrain-tiers-loupe_loupe-kit-13_preuves-"
                "loupe_temoin-loupe.txt")

ENTREE248 = """

## Entrée 248 — LE DÉPÔT KIT TERRAIN REÇU : LES DEUX PREMIERS RUNS DU PAQUET AUTO (les runs du 12/11/2026, 13:36 heure locale du développeur — l'annonce « dossier kit terrain avec preuves déposé dans /test du drive ») — le kit-1 shani REFUSÉ ENCORE (ALEKPC, l'ÉCHEC NOMMÉ T0.silicium, le même silicium sans SHA-NI — le verdict octet pour octet celui du geste A) et le kit-3 loupe VÉCU VERT SUR PIÈCES (Windows 11, le treizième run terrain, le premier du paquet AUTO — la pièce de l'ère scellée c1115105… jugée par sa propre application chez son utilisateur)

**Le dépôt et sa lecture.** Le /test re-listé : 579 entrées (496 [geste A] + 8 [MULTIMACHINES, E246] + 75 [AUTO, E247]), aucune créée après 12:38:20Z — aucun autre dépôt. Le geste du développeur vit DANS le dossier AUTO livré : LA VAGUE 2 — l'arbre machine entier (55 entrées : pc-windows/ · telephone-arm/ · qemu-wsl2/ + COMMENCER-ICI.bat) retéléversé 13:37:44-13:38:20 locale AVEC les TROIS preuves de run. La provenance nommée par la métadonnée même : le livreur du labo ne pose JAMAIS modifiedTime (le code lu — upload_create/upload_update), l'outil du développeur, lui, PRÉSERVE les mtimes (l'arbre extrait porte 13:35:21-22 locale, les preuves portent leurs heures de run) — les deux voix ne se confondent pas.

**Le kit-1 shani (ALEKPC, 13:36:01 locale).** Le journal porte l'heure au contenu ET le mtime Drive la porte à la métadonnée (12:36:01.993Z = 13:36:01 locale) — la pièce datée par DEUX voix indépendantes. QUATRE lignes : ALEKPC · AMD64 · Windows · Python 3.14.3 — LE RUN TERRAIN, puis T0, T1, T0.silicium — le format n° 2 (D206) encore. Le constat CPUID identique au journal ET au verdict : « GenuineIntel » · famille 6 · modèle 142 · pas 12 · SHA-NI ABSENT (CPUID feuille 7, EBX bit 29 = 0). Le VERDICT est OCTET POUR OCTET celui du geste A ; le journal ne diffère du geste A QUE par l'heure (11:26:54 → 13:36:01) — UN RUN NEUF, LE MÊME REFUS : CE silicium n'exécute pas sha256rnds2, la mesure avant/après n'y existe pas, le kit ne peut pas inventer le silicium — il a refusé de mesurer EXACTEMENT comme conçu (D206 tenue une deuxième fois : QUI a exécuté — ALEKPC nommée à l'ouverture ; QUOI a refusé — T0.silicium, le constat au journal ET au verdict).

**Le kit-3 loupe (Windows 11, 13:36:32 locale — 31 s après le kit-1 : les DEUX runs séquentiels, une minute à eux deux).** L'env : Windows 11 · Python 64 bits · AMD64 (le même que les runs 11 et 12). LE SCELLÉ ASSERTÉ au T0 : loupe.exe 127488 o, sha256 c111510535767a40… == LA PIÈCE LIVRÉE. T0→T7+S0 TOUT VERT : l'arène (l'ombre byte-à-byte, l'IAT résolue par le scénario-chargeur : 37 feuilles), la session (poignée 0x2d4, le VRAI CreateFileW), la double lecture (les 384 octets IDENTIQUES), LE PANNEAU (md5 5fc07b786150… · sha256 == hashlib — la pièce de l'ère jugée par sa propre application sur son ombre), les lignes, la recherche (le motif à 577 == bytes.find), L'ÉDITION à l'octet (0x00 → 0x4D SEUL, la taille CONSTANTE, le VRAI WriteFile), LES REJETS nommés (-2 ABSENT · -5 ENTRÉE · -3 HORS-BORNES · -1 FIN), la pièce relue INCHANGÉE (T7). LA SONDE DE L'ENTRÉE 205 vécue : P1 LE TROU et P4 LA GÉOMÉTRIE dev.2 ENTIÈRE REFUSÉS par le VRAI chargeur (GetLastError 193, NTSTATUS 0xc000007b) — L'AXE EST NOMMÉ, les copies %TEMP% mortes, loupe.exe INTACT ; sonde-214 : la liaison nommée au témoin. Le témoin == celui du douzième run (les MÊMES pièces, E222) ne différant QUE par les adresses ASLR et la poignée de session — le gabarit intangible. LE VERDICT DU TÉMOIN : « LE RUN DE LOUPE : VERT SUR PIÈCES — l'application née de TRIADE a vécu chez son utilisateur : la session, le panneau, les lignes, la recherche, l'édition à l'octet, les rejets nommés ».

**Le recoupement (scripts/recouper_depot_kit_terrain.py — le rapport 26/26 VERT, sha256 7168ca81…, preuves-depot-auto-terrain/).** LA CHAÎNE : les 40 pièces du zip == l'arbre déposé au /test, OCTET POUR OCTET (40/40 md5 VERT) ; le zip du /test == celui du bac (051fd9adfbb0…) ; scenario-shani.py == le correctif n° 2 livré (d9def0b4…, 33 925 o) ; moteur-shani.bin == l'empreinte du témoin (761ab194…) ; proxy-image.bin == LE SCELLÉ (0782d7e2…) ; loupe.exe == LE SCELLÉ (c1115105…) ; scenario-loupe.py == la vague 0.1.1-dev.1 (77872b71…). LA CHRONOLOGIE datée aux métadonnées Drive : le zip livré 12:32:32Z → l'extraction 13:35:21-22 locale → le kit-1 13:36:01 → le kit-3 13:36:32 → le dépôt 13:37:44-13:38:20 — aucune inversion. UNE ÉTIQUETTE HONNÊTE : test_appel.exe (kit-2) — le téléchargement REFUSÉ par l'antivirus Drive (HTTP 403 « malware or spam », un faux positif connu des exe de mesure de timing) ; l'empreinte des MÉTADONNÉES (md5 64e7f8e762a8…) == la copie du zip — la pièce au /test demeure l'octet pour octet la livrée, rien à deviner.

**Frontières.** Kit-2-dudect NON couru (aucune preuve dudect au dépôt — ni témoin ni csv) ; le téléphone-arm et les voies QEMU non courus — AUCUN geste obligatoire ; LA VITRINE demeure à la main du développeur (le [suite] du témoin le dit : temoin-vitrine.bat à double-cliquer, les fenêtres à fermer SOI-MÊME — un témoin automatisé ne témoignerait de rien) ; le refus T0.silicium n'écrit QUE le VERDICT et le journal (le témoin complet et le moteur-exécuté naissent après le franchissement du silicium — le LISEZMOI le dit, les pièces le confirment : la ligne « signature du geste » n'existe pas pour un refus, rien à signer) ; D205 demeure consacrée au laboratoire, jamais scellée ; les journaux bruts (*.log) demeurent au coffre /test, leurs contenus cités mot pour mot. La main demeure au développeur : les kits restants du paquet AUTO à courir ou non, le geste B SHA-NI réel (une machine à SHA-NI), la campagne de comparaison D204, la cérémonie d'ère, le séquestre D183, la réplication.
"""

WORKLOG = """

Task ID: 155
Agent: Z.ai (agent principal)
Task: LA RÉCEPTION DU DÉPÔT KIT TERRAIN (l'annonce du développeur du
12/11/2026 : « dossier kit terrain avec preuves déposé dans /test du
drive ») — le rapatriement des preuves du paquet AUTO, le recoupement
26/26 VERT (la chaîne close, la chronologie datée aux métadonnées Drive,
les deux runs auto-portants), la consignation de l'Entrée 248.

Work Log:
- LE SONDAGE : le /test re-listé (579 entrées = 496 [geste A] + 8
  [MULTIMACHINES] + 75 [AUTO], aucune entrée créée après 12:38:20Z) ; le
  dépôt = LA VAGUE 2 dans le dossier AUTO livré : l'arbre machine (55
  entrées aux mtimes PRÉSERVÉS — l'extraction 13:35:21-22 locale) + LES
  TROIS preuves de run (le livreur du labo ne pose JAMAIS modifiedTime —
  le code lu ; l'outil du développeur nommé par la métadonnée même).
- LE RAPATRIEMENT : 21 pièces au md5 VERT (scripts/
  rapatrier_depot_kit_terrain.py, preuves-depot-auto-terrain/) ;
  test_appel.exe REFUSÉ par l'antivirus Drive (HTTP 403) — l'empreinte
  des MÉTADONNÉES recoupée à la place (== la copie du zip), l'étiquette
  honnête.
- LE KIT-1 SHANI (ALEKPC, 13:36:01 locale) : l'heure au journal == le
  mtime Drive (deux voix) ; le même refus T0.silicium (SHA-NI ABSENT,
  CPUID feuille 7 EBX bit 29 = 0) ; le VERDICT == celui du geste A
  OCTET POUR OCTET, le journal ne diffère QUE par l'heure ; D206 tenue
  une deuxième fois (QUI, QUOI).
- LE KIT-3 LOUPE (Windows 11, 13:36:32 locale, 31 s après le kit-1) : LE
  SCELLÉ c1115105… asserté au T0 ; T0→T7+S0 TOUT VERT (l'arène, la
  session, la double lecture, LE PANNEAU == hashlib, les lignes, la
  recherche, l'édition à l'octet 0x00 → 0x4D, les rejets nommés, la
  pièce relue INCHANGÉE) ; LA SONDE 205 (P1/P4 refusés par le VRAI
  chargeur : GetLastError 193, NTSTATUS 0xc000007b — l'axe nommé) ; le
  treizième run terrain, le témoin == celui du 12e aux adresses ASLR
  près ; « VERT SUR PIÈCES — l'application née de TRIADE a vécu chez
  son utilisateur ».
- LE RECOUPEMENT (scripts/recouper_depot_kit_terrain.py, rapport 26/26
  VERT sha256 7168ca81…) : LA CHAÎNE (40/40 pièces du zip == l'arbre du
  /test, les CINQ scellés exacts), LA CHRONOLOGIE (livraison 12:32:32Z →
  extraction → runs → dépôt, aucune inversion), LES FRONTIÈRES (kit-2
  non couru, la vitrine à la main, le refus n'écrit que ses deux pièces,
  rien maquillé).
- LA CONSIGNATION : l'Entrée 248 au journal, la présente tâche au
  worklog, le commit, le push GitHub, le miroir Drive et le kit
  Cérémonie tenus par le hook post-commit.
- SUITE : au développeur — les kits restants du paquet AUTO à courir ou
  non (kit-2 sur les siliciums Windows, le constat au téléphone, les
  voies QEMU sous WSL2 — aucun geste obligatoire), le geste B SHA-NI
  réel, la campagne de comparaison D204, la cérémonie d'ère, le
  séquestre D183, la réplication.
"""


# --- L'APPEND VÉRIFIÉ (la fin attendue de chaque pièce) ---------------------------

def append_verifie(chemin: pathlib.Path, fin_attendue: str, bloc: str,
                   nom: str, marqueur_doublon: str) -> None:
    texte = chemin.read_text(encoding="utf-8")
    if marqueur_doublon in texte:
        print(f"[consigner] {nom} : {marqueur_doublon} déjà présent — "
              "append sauté (déjà tenu)")
        return
    if not texte.rstrip("\n").endswith(fin_attendue.rstrip("\n")):
        sys.exit(f"[consigner] {nom} : la fin attendue n'est pas la "
                 "dernière section — append refusé")
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(bloc)
    print(f"[consigner] {nom} : appendé ({len(bloc)} o)")


def main() -> int:
    # 0. LES PREUVES AVANT LE TEXTE
    if not RAPPORT.exists():
        sys.exit("[consigner] le rapport de recoupement est absent — refus")
    sha = hashlib.sha256(RAPPORT.read_bytes()).hexdigest()
    if sha != RAPPORT_SHA:
        sys.exit(f"[consigner] le rapport diverge ({sha[:12]}… != "
                 f"{RAPPORT_SHA[:12]}…) — refus")
    texte_rapport = RAPPORT.read_text(encoding="utf-8")
    if "BILAN : 26/26 VERT" not in texte_rapport:
        sys.exit("[consigner] le rapport n'est pas 26/26 VERT — refus")
    print(f"[consigner] le rapport de recoupement recoupé ({sha[:12]}…, "
          f"{RAPPORT.stat().st_size} o, 26/26 VERT)")
    for p in (VERDICT, JOURNAL_RUN, TEMOIN_LOUPE):
        if not p.exists():
            sys.exit(f"[consigner] la preuve de run est absente : {p}")
    j = JOURNAL_RUN.read_text(encoding="utf-8")
    if "ALEKPC · AMD64 · Windows · Python 3.14.3" not in j \
            or "13:36:01" not in j or "T0.silicium" not in j:
        sys.exit("[consigner] le journal du kit-1 est incohérent — refus")
    t = TEMOIN_LOUPE.read_text(encoding="utf-8")
    if "VERT SUR PIÈCES" not in t or "c111510535767a40" not in t:
        sys.exit("[consigner] le témoin du kit-3 est incohérent — refus")
    print("[consigner] les TROIS preuves de run présentes et cohérentes "
          "(kit-1 refus T0.silicium ALEKPC 13:36:01, kit-3 VERT SUR PIÈCES "
          "scellé c1115105…)")

    # 1. L'Entrée 248 au JOURNAL DE TRAVAIL (append-only)
    fin_journal = "le séquestre D183, la réplication."
    append_verifie(REPO / "docs" / "JOURNAL_TRAVAIL.md", fin_journal,
                   ENTREE248, "JOURNAL_TRAVAIL.md (+Entrée 248)",
                   "## Entrée 248 — LE DÉPÔT KIT TERRAIN REÇU")

    # 2. LA TASK 155 AU WORKLOG (append-only)
    fin_worklog = "le séquestre D183, la réplication."
    append_verifie(REPO / "worklog.md", fin_worklog, WORKLOG,
                   "worklog.md (+Task 155)", "Task ID: 155")
    print("[consigner] LES DEUX CONSIGNATIONS TENUES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
