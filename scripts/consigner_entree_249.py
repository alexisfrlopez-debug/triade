#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree_249.py — L'ÉDITION MISE À JOUR DU PAQUET MULTIMACHINES :
l'Entrée 249 au journal de travail et la Task 156 au worklog.

La commande (le développeur, 12/11/2026) : « fais un kit mis à jour avec ce
qu'il reste à faire ou des corrections si nécessaires, ou éventuellement
rajouter des tests si tu trouve ça pertinent ».

Append-only : les fins VÉRIFIÉES avant écriture, les rejeus REFUSÉS. Le
paquet MISE À JOUR (sha256 4e7270d7…), la note d'épreuve et les preuves
voie-1 contrôlés AVANT toute écriture — la consignation ne peut pas
précéder ses preuves.
"""

import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")

PAQUET = REPO / "download" / "TRIADE_kits_terrain_v0150_MULTIMACHINES-MISE-A-JOUR.zip"
PAQUET_SHA = ("4e7270d774b731338da5f1c9e380071238bbb64596097f1afbcaa1c1e"
              "26f1dd3")
EDITION = REPO / "scripts" / "kits_mesure_v150" / "edition_mise_a_jour"
PREUVES = [
    EDITION / "preuves-edition-maj-labo" / "NOTE-D-EPREUVE.txt",
    EDITION / "preuves-edition-maj-labo" / "voie1-m7d" / "VERDICT-run-m7d.txt",
    EDITION / "paquet" / "CE-QUI-RESTE-A-FAIRE.txt",
    EDITION / "paquet" / "EMPREINTES-PAQUET.txt",
    EDITION / "paquet" / "verifier_paquet.py",
    EDITION / "paquet" / "diagnostic_machine.py",
]

ENTREE249 = """

## Entrée 249 — L'ÉDITION MISE À JOUR DU PAQUET MULTIMACHINES : LA FEUILLE DE ROUTE, DEUX TESTS NEUFS ET LES CORRECTIONS DE RELECTURE (la commande du développeur du 12/11/2026 : « fais un kit mis à jour avec ce qu'il reste à faire ou des corrections si nécessaires, ou éventuellement rajouter des tests si tu trouve ça pertinent ») — TRIADE_kits_terrain_v0150_MULTIMACHINES-MISE-A-JOUR.zip (3 519 581 o, sha256 4e7270d7…) : les 40 pièces du paquet AUTO reprises OCTET POUR OCTET sauf quatre fichiers d'édition, les CINQ scellés INTACTS, six pièces neuves (12/11, le troisième geste de la journée)

**La commande, la réponse en trois volets.** (1) CE QU'IL RESTE À FAIRE : CE-QUI-RESTE-A-FAIRE.txt — l'état daté au 12/11 soir : les kits VÉCUS (le kit-1 shani DEUX refus identiques T0.silicium sur ALEKPC — le geste A puis le rejeu du paquet AUTO, Entrées 245 et 248 : le rejeu n'y est plus requis ; le kit-3 loupe VERT SUR PIÈCES, le 13e run terrain, Windows 11, Entrée 248 — reste à la main le témoin vitrine, facultatif) ; les kits RESTANTS (LE KIT-2 DUDECT — LA SEULE MESURE JAMAIS ENCORE COURUE du paquet, vivable sur N'IMPORTE QUEL Windows x86-64 sans Python ni compilateur ; le kit-constat-arm au téléphone ; les deux voies QEMU sous WSL2) ; et LES GESTES DU PROJET (le geste B SHA-NI réel — une machine à SHA-NI ; la campagne D204 pré-enregistrée ; la cérémonie d'ère ; le séquestre D183 ; la réplication). (2) LES DEUX TESTS NEUFS : DIAGNOSTIC-MACHINE.bat + diagnostic_machine.py — la machine nommée (l'OS, l'arche, le CPU), le silicium lu par CPUID (LA MÊME lecture que le kit-1 au geste A : feuille 7, EBX bit 29 — le stub x86-64 aux deux conventions win64/sysv), recoupée sur Linux par la SECONDE VOIX /proc/cpuinfo, ce qui vit (Python et ses 64 bits, cl/gcc/clang, wsl.exe), LE VERDICT kits vivables sur CETTE machine (il sert aussi à choisir la machine du geste B) — le témoin diagnostic-machine.txt ; et VERIFIER-PAQUET.bat + verifier_paquet.py — le recoup sha256 des 45 pièces de l'extraction contre le MANIFESTE GRAVÉ, l'événement qui le motiva : le refus Drive HTTP 403 « malware or spam » de test_appel.exe le 12/11 même (Entrée 248) — l'antivirus LOCAL peut faire pareil À L'EXTRACTION, le vérificateur le NOMME avant tout run ; sans Python il recoupe au moins les CINQ scellés par certutil et le dit ; EMPREINTES-PAQUET.txt : les 44 empreintes, la voix lisible à la main — l'honnêteté du cercle : ni le présent fichier ni le vérificateur ne scellent leur propre empreinte, le sha256 du zip rend les deux (Entrée 249 même, le coffre /test). (3) LES CORRECTIONS DE RELECTURE : le lanceur LANCER-KIT-2-DUDECT.bat (a) si l'épreuve d'appel manque à l'extraction l'écart est désormais NOMMÉ à l'écran ET au témoin — l'édition AUTO la sautait en SILENCE ; (b) si le binaire de mesure manque : REFUS NOMMÉ, plus jamais un code 9009 nu ; (c) la validation de N par « for /f delims=0123456789 » NE PEUT PLUS EXÉCUTER aucun texte saisi (l'ancienne passait par un pipe « echo %N%|findstr ») ; la ligne « 1. Les pièces du kit » du LISEZMOI-dudect, amputée par l'insertion de la mention AUTOMATISÉE, RÉPARÉE (la relecture sur pièces, encore) ; le menu COMMENCER-ICI.bat enrichi (les choix D/V/6/7, l'état des kits vécus affiché, la feuille de route en tête) ; le bandeau de l'édition inséré au LISEZMOI-MULTIMACHINES.

**L'épreuve sur extraction vierge (D153 — le paquet déposé est le paquet prouvé ; preuves-edition-maj-labo/, la note d'épreuve jointe, les six épreuves vécues).** (a) LE VÉRIFICATEUR : 45/45 pièces VERTES, code 0 ; (b) L'ANTI-TEST — l'épreuve que le test attrape ce qu'il prétend attraper : sur une COPIE, test_appel.exe RETIRÉ et un octet de moteur-shani.bin MUTÉ, le vérificateur rend les DEUX écarts NOMMÉS (« ABSENTE » / « DIVERGENTE »), code 1, la copie détruite après constat ; (c) LE DIAGNOSTIC vécu sur l'hôte Linux x86-64 du laboratoire : le CPUID par stub rend « GenuineIntel » · famille 6 · modèle 173 · pas 1 · SHA-NI PRÉSENT — RECoupÉ par la seconde voix /proc/cpuinfo (vendor_id « GenuineIntel » et le flag sha_ni : les DEUX voix concordent, le silicium du labo est le PREMIER HÔTE DU PROJET à afficher SHA-NI), le verdict rend honnêtement « cette machine est LINUX » ; (d) LA VOIE 1 M7D REVÉCUE par son lanceur sur l'extraction : 16 PASS / 0 ÉCHEC, VERT, code 0, les preuves nées seules (copiées au dépôt) ; (e) LE KIT-2 RECOMPILÉ depuis la source de l'extrait (gcc -O2) : l'épreuve d'appel FIPS « abc » EXACT, mutation K DIVERGE, restauration EXACT, dudect_v150 --autotest VERT code 0 ; (f) LE DIFF éprouvé/livré : les 36 pièces du paquet AUTO restées OCTET POUR OCTET identiques, les QUATRE fichiers d'édition seuls divergents (nommés : le menu, la carte maîtresse, le lanceur et le LISEZMOI du kit-2) — les .sh, les scénarios, les sources C et les CINQ scellés INTACTS ; la forme : les .bat TOUS CRLF intégral et ASCII pur, les .sh exécutables, 46 pièces au total.

**Frontières.** Aucune pièce scellée touchée (le garde 14/14 le constatera au geste) ; les LISEZMOI retouchés PAR INSERTION (le bandeau, la mention — l'histoire jamais réécrite ; la ligne amputée réparée et DITE dans la mention même) ; aucun chiffre fabriqué — les références 5,84×/6,37×/0,19× restent consignées à leurs entrées d'origine, la feuille de route les cite sans en créer aucune, l'état « vécu » de chaque kit est daté à ses preuves (Entrées 245/248) ; le labo n'a AUCUN Windows — les .bat neufs et corrigés y sont éprouvés par leurs commandes (certutil, findstr, for /f, where, powershell — standard de Windows 10/11) et par la relecture, JAMAIS par l'exécution : le premier double-clic se vit chez le développeur, l'écran nommant un défaut renvoyé TEL QUEL (D122) ; ce qui reste à la main du développeur — la signature, l'état EFFECTIF du turbo, le témoin vitrine, le renvoi au coffre /test — est dit à l'écran de chaque lanceur et dans la lettre : JAMAIS maquillé. La main demeure au développeur : LE KIT-2 DUDECT à courir (aucun geste obligatoire), le constat-arm au téléphone, les voies QEMU, le diagnostic pour choisir la machine du geste B, la campagne de comparaison D204, la cérémonie d'ère, le séquestre D183, la réplication.
"""

WORKLOG = """

Task ID: 156
Agent: Z.ai (agent principal)
Task: L'ÉDITION MISE À JOUR DU PAQUET MULTIMACHINES (la commande du
développeur du 12/11/2026 : « fais un kit mis à jour avec ce qu'il reste à
faire ou des corrections si nécessaires, ou éventuellement rajouter des
tests si tu trouve ça pertinent ») — la feuille de route, deux tests neufs,
les corrections de relecture, l'assemblage aux scellés recoupés, l'épreuve
sur extraction vierge, la consignation et la livraison.

Work Log:
- LA FEUILLE DE ROUTE : CE-QUI-RESTE-A-FAIRE.txt — l'état daté au 12/11
  soir (kit-1 vécu par deux refus identiques, kit-3 vécu VERT au 13e run,
  LE KIT-2 JAMAIS COURU, le constat-arm, les voies QEMU, le geste B,
  D204, la cérémonie d'ère, le séquestre D183, la réplication).
- LES DEUX TESTS NEUFS : DIAGNOSTIC-MACHINE.bat + diagnostic_machine.py
  (le CPUID feuille 7 EBX bit 29 == la lecture du kit-1 au geste A, la
  double voix /proc/cpuinfo sous Linux, le verdict kits vivables, le
  témoin diagnostic-machine.txt) ; VERIFIER-PAQUET.bat + verifier_paquet.py
  (les 45 pièces contre le manifeste gravé — l'attrapage antivirus, motivé
  par le refus Drive 403 de test_appel.exe du 12/11 ; sans Python : les 5
  scellés par certutil) ; EMPREINTES-PAQUET.txt (les 44 empreintes
  lisibles, l'honnêteté du cercle).
- LES CORRECTIONS : le lanceur kit-2 (l'écart NOMMÉ si l'épreuve d'appel
  manque — l'édition AUTO la sautait en silence ; le REFUS NOMMÉ si le
  binaire manque ; la validation de N sans exécution), la ligne « 1. » du
  LISEZMOI-dudect réparée, le menu enrichi (D/V/6/7 + l'état des kits),
  le bandeau inséré à la carte maîtresse.
- L'ÉPREUVE SUR EXTRACTION VIERGE : (a) le vérificateur 45/45 VERT code 0 ;
  (b) l'ANTI-TEST — l'exe retiré + l'octet muté sur une COPIE : les DEUX
  écarts NOMMÉS, code 1 ; (c) le diagnostic vécu sur l'hôte labo — le
  CPUID GenuineIntel · famille 6 · modèle 173 · SHA-NI PRÉSENT == la
  seconde voix /proc/cpuinfo (le PREMIER hôte du projet à afficher
  SHA-NI) ; (d) la voie 1 M7D revécue 16 PASS/0 ÉCHEC VERT code 0 ; (e)
  le kit-2 recompilé gcc : FIPS abc EXACT, autotest VERT ; (f) le diff
  36/40 pièces AUTO octet pour octet identiques, les 4 fichiers
  d'édition seuls divergents ; CRLF/ASCII/scellés/46 pièces.
- L'ASSEMBLAGE : 46 pièces, les .bat en CRLF, les .sh exécutables —
  TRIADE_kits_terrain_v0150_MULTIMACHINES-MISE-A-JOUR.zip 3 519 581 o
  sha256 4e7270d7… ; les preuves d'épreuve au dépôt
  (scripts/kits_mesure_v150/edition_mise_a_jour/preuves-edition-maj-labo/
  + la note d'épreuve).
- LA CONSIGNATION : l'Entrée 249 au journal, la présente tâche au worklog,
  le commit, le push GitHub, le miroir Drive et le kit Cérémonie tenus par
  le hook post-commit ; la livraison au bac download/ et au coffre /test.
- SUITE : au développeur — LE KIT-2 DUDECT À COURIR (la seule mesure
  jamais encore vécue du paquet : un double-clic, aucun Python ni
  compilateur requis), le constat-arm au téléphone, les voies QEMU, le
  DIAGNOSTIC pour choisir la machine du geste B, la campagne D204, la
  cérémonie d'ère, le séquestre D183, la réplication.
"""


# --- L'APPEND VÉRIFIÉ (la fin attendue de chaque pièce) ------------------------

def append_verifie(chemin: pathlib.Path, fin_attendue: str, bloc: str,
                   nom: str, marqueur_doublon: str) -> None:
    texte = chemin.read_text(encoding="utf-8")
    if marqueur_doublon in texte:
        print(f"[consigner] {nom} : {marqueur_doublon} déjà présent — "
              "append sauté (déjà tenu)")
        return
    if not texte.rstrip("\n").endswith(fin_attendue.rstrip("\n")):
        sys.exit(f"[consigner] {nom} : la fin attendue n'est pas la "
                 f"dernière section — append refusé")
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(bloc)
    print(f"[consigner] {nom} : appendé ({len(bloc)} o)")


def main() -> int:
    # 0. LES PREUVES AVANT LE TEXTE
    if not PAQUET.exists():
        sys.exit("[consigner] le paquet MISE À JOUR est absent — refus")
    empreinte = hashlib.sha256(PAQUET.read_bytes()).hexdigest()
    if empreinte != PAQUET_SHA:
        sys.exit(f"[consigner] le paquet diverge ({empreinte[:12]}… != "
                 f"{PAQUET_SHA[:12]}…) — refus")
    print(f"[consigner] le paquet MISE À JOUR recoupé ({empreinte[:12]}…, "
          f"{PAQUET.stat().st_size} o)")
    for p in PREUVES:
        if not p.exists():
            sys.exit(f"[consigner] la preuve est absente : {p}")
    note = PREUVES[0].read_text(encoding="utf-8")
    for attendu in ("45/45", "ANTI-TEST", "16 PASS", "36 pièces",
                    "CRLF intégral"):
        if attendu not in note:
            sys.exit(f"[consigner] la note d'épreuve ne rend pas "
                     f"{attendu!r} — refus")
    v1 = PREUVES[1].read_text(encoding="utf-8")
    if "16 PASS" not in v1 or "VERT" not in v1:
        sys.exit("[consigner] le verdict M7D d'épreuve est incohérent — "
                 "refus")
    lettre = PREUVES[2].read_text(encoding="utf-8")
    for attendu in ("LE GRAND MANQUANT", "DIAGNOSTIC-MACHINE.bat",
                    "VERIFIER-PAQUET.bat", "LES CORRECTIONS DE CETTE ÉDITION"):
        if attendu not in lettre:
            sys.exit(f"[consigner] la feuille de route ne rend pas "
                     f"{attendu!r} — refus")
    print("[consigner] les preuves présentes et cohérentes (note 6 épreuves, "
          "M7D 16 PASS VERT, la feuille de route, le manifeste, les deux .py)")

    # 1. L'Entrée 249 au JOURNAL DE TRAVAIL (append-only)
    fin_journal = "le séquestre D183, la réplication."
    append_verifie(REPO / "docs" / "JOURNAL_TRAVAIL.md", fin_journal,
                   ENTREE249, "JOURNAL_TRAVAIL.md (+Entrée 249)",
                   "## Entrée 249 — L'ÉDITION MISE À JOUR DU PAQUET")

    # 2. LA TASK 156 AU WORKLOG (append-only) — la fin réelle porte un
    # retour à la ligne au milieu (« …le\n  séquestre D183, la réplication. »)
    fin_worklog = "séquestre D183, la réplication."
    append_verifie(REPO / "worklog.md", fin_worklog, WORKLOG,
                   "worklog.md (+Task 156)", "Task ID: 156")
    print("[consigner] LES DEUX CONSIGNATIONS TENUES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
