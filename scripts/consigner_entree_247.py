#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree_247.py — L'ÉDITION AUTOMATISÉE DU PAQUET MULTIMACHINES :
l'Entrée 247 au journal de travail et la Task 154 au worklog.

La commande (le développeur, 12/11/2026) : « je vois qu'il y a dans le kit
des choses à compiler. je veux que l'utilisation soit la plus simple
possible, en automatisant au maximum ».

Append-only : les fins VÉRIFIÉES avant écriture, les rejeus REFUSÉS. Le
paquet AUTO (sha256 814312a5…), les preuves d'épreuve (voie 1 M7D VERT,
voie 2 shani émulé VERT, constat-arm VERT) et la note d'épreuve contrôlés
AVANT toute écriture — la consignation ne peut pas précéder ses preuves.
"""

import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")

PAQUET = REPO / "download" / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO.zip"
PAQUET_SHA = ("814312a5546d1476213948757943d8d33f4f94fe274d464b2bf17d059"
              "2a5562e")
PREUVES = [
    REPO / "scripts/kits_mesure_v150/preuves-edition-auto-labo/"
    "NOTE-D-EPREUVE.txt",
    REPO / "scripts/kits_mesure_v150/preuves-edition-auto-labo/"
    "voie1-m7d/VERDICT-run-m7d.txt",
    REPO / "scripts/kits_mesure_v150/preuves-edition-auto-labo/"
    "voie2-shani-emule/VERDICT-run-shani.txt",
    REPO / "scripts/kits_mesure_v150/preuves-edition-auto-labo/"
    "constat-arm-hote/constat-arm-verdict.txt",
    REPO / "scripts/kits_mesure_v150/preuves-edition-auto-labo/"
    "kit2-recompile/journal-dudect-1794486215.csv",
]

ENTREE247 = """

## Entrée 247 — L'ÉDITION AUTOMATISÉE DU PAQUET MULTIMACHINES : UN SEUL GESTE PAR KIT, LE DOUBLE-CLIC (la commande du développeur du 12/11/2026 : « je vois qu'il y a dans le kit des choses à compiler. je veux que l'utilisation soit la plus simple possible, en automatisant au maximum ») — TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO.zip (3 497 291 o, sha256 814312a5…) : LES HUIT LANCEURS NÉS (le menu COMMENCER-ICI.bat, les trois LANCER-KIT-*.bat, les trois .sh) ET LA LETTRE A-LIRE-AUTOMATISATION.txt, les pièces et les CINQ scellés du premier paquet INTACTS (l'Entrée 246 demeure, l'append-only tenu) (12/11, le deuxième geste de la journée)

**La commande et la réponse.** Le premier paquet (efff812b…) demandait au développeur d'ouvrir une invite, de taper les compilations à la main (cl /O2, gcc -O2 -lm), d'orchestre les étapes de chaque protocole. L'édition AUTOMATISÉE fait TOUS ces gestes : chaque kit vit par SON lanceur, le LISEZMOI de chaque kit porte la mention (six retouches, l'histoire jamais réécrite), la carte maîtresse porte le bandeau. Le menu COMMENCER-ICI.bat ouvre tout le paquet — y compris les deux voies QEMU qui partent seules par WSL2 s'il vit (wslpath, wsl.exe détecté, le refus nommé sinon).

**Le kit-2 (LE kit qui voulait une compilation).** LANCER-KIT-2-DUDECT.bat : il recoupe le sha256 de l'image scellée AVANT tout (certutil + findstr, 0782d7e2… attendu, refus nommé si divergence) ; il cherche un compilateur (cl / gcc / clang, where) — S'IL EN TROUVE UN il RECOMPILE le mesureur et l'épreuve d'appel depuis LA SOURCE (la source est la vérité, les binaires dans run\\, MSVC /D_CRT_SECURE_NO_WARNINGS pour les fopen dépréciés) et exécute VOTRE binaire, SINON les exe PRÉCOMPILÉS livrés courent ; SI LA COMPILATION LOCALE ÉCHOUE il BASCULE sur les précompilés avec l'écart NOMÉ au témoin (le refus complet du premier jet fut guéri à la relecture — la commande même était la simplicité maximale) ; l'épreuve d'appel est vécue (FIPS « abc » EXACT attendu, l'écart nommé sans arrêter le run) ; LE RUN : dudect_v150 cibles N, N = 200 par défaut (l'argument de la ligne de commande, validation numérique, minimum 60, garde contre un N aberrant) ; puis LE BROUILLON DE TÉMOIN écrit tout seul (date, OS par ver, CPU/cœurs/fréquence par powershell Get-CimInstance, le binaire et SON sha256 par certutil, le code de sortie, le journal csv le plus récent, la sortie console conservée) — l'état EFFECTIF du turbo et la SIGNATURE demeurent À LA MAIN du développeur (le mesureur ne peut pas lire le BIOS, le labo ne peut pas signer son geste : rien n'est maquillé). AUCUN Python requis pour ce kit.

**Les autres kits.** Kit-1 : le lanceur trouve Python (py/python/python3) et vit le scénario — RIEN À COMPILER (le moteur-shani.bin livré, son sha256 asserté par le scénario). Kit-3 : le RECOUP de loupe.exe contre le scellé (c1115105…) AVANT TOUT lancement — l'exigence du LISEZMOI-terrain-tiers automatisée —, le Python vérifié 64 BITS (struct.calcsize('P')), le scénario T0→T7+S0, le témoin vitrine nommé comme le double-clic à part qu'il EST (des fenêtres que VOUS fermez : un témoin automatisé ne témoignerait de rien). Le téléphone : lancer-kit-constat-arm.sh INSTALLE PYTHON TOUT SEUL par pkg s'il manque (l'unique étape manuelle du protocole, morte). Les voies QEMU : lancer-voie1-m7d.sh (le kit AUTONOME, le qemu statique embarqué, le lanceur ne demande que python3 — qu'il tente même d'installer si sudo vit sans mot de passe) et lancer-voie2-shani.sh (qemu-x86_64 trouvé, installé s'il peut, ou LA commande exacte rendue : sudo apt install qemu-user).

**L'épreuve sur extraction vierge (D153 — le paquet déposé est le paquet prouvé ; preuves-edition-auto-labo/, la note d'épreuve jointe).** Sur le premier assemblage (c73e0be4…) : LA VOIE 1 VÉCUE PAR SON LANCEUR — le run M7D complet, 16 PASS / 0 ÉCHEC, VERDICT VERT, code 0, preuves-m7/ nées seules ; LA VOIE 2 VÉCUE — le kit-shani sous qemu-x86_64 -cpu max (l'instrument réinstallé au labo par SA procédure riscv/outils/installer_qemu.sh), VERDICT VERT, code 0, LE RAPPORT 0,19× RENDU PAR LE RUN (le même artefact TCG que l'épreuve du matin, consigné tel quel) ; LE CONSTAT-ARM VÉCU sur l'hôte x86-64 — VERDICT VERT, le constat honnête « CECI N'EST PAS UN TÉLÉPHONE ARM » ; LE KIT-2 RECOMPILÉ depuis la source de l'extrait (gcc -O2) : test_appel FIPS abc EXACT / mutation K DIVERGE / restauration EXACT code 0, dudect --autotest code 0 (le journal du mesureur joint). L'extraction : testzip INTÈGRE, les .bat TOUS CRLF intégral et ASCII pur, les .sh exécutables, les CINQ scellés EXACTS.

**La relecture des .bat (le labo n'a AUCUN Windows — l'étiquette honnête de l'Entrée 246 demeure : les .bat y sont éprouvés par leurs commandes et la relecture, jamais par l'exécution) a attrapé et guéri DEUX défauts** : (1) le menu appelait les lanceurs par chemins RELATIFS — le dossier courant change après chaque kit, les appels suivants eussent fauté : les chemins absolus (%~dp0) posés ; (2) le kit-2 refusait tout run sur échec de compilation — le fallback précompilé posé (l'écart nommé au témoin, D189). LE DIFF de l'éprouvé au livré : 38/40 pièces OCTET POUR OCTET identiques — les deux .bat corrigés seuls divergent (des fichiers que le labo ne peut PAS exécuter ; tout ce qui FUT éprouvé — scellés, scénarios, lanceurs .sh — est identique au livré).

**Frontières.** Aucune pièce scellée touchée (le garde 14/14 le constatera au geste) ; les LISEZMOI retouchés par INSERTION de la mention du lanceur, l'histoire jamais réécrite ; les .bat livrés en CRLF (la forme canonique de cmd.exe — temoin-vitrine.bat compris, les sources du dépôt demeurant LF) ; aucun chiffre fabriqué (le 0,19× de la voie 2 fut RENDU PAR LE RUN d'épreuve, pas recopié) ; ce qui reste à la main du développeur — la signature, l'état EFFECTIF du turbo, le témoin vitrine, le renvoi au coffre /test — est dit À L'ÉCRAN de chaque lanceur et dans la lettre : JAMAIS maquillé ; le premier double-clic des .bat se vit chez le développeur (si un écran nomme un défaut, le .txt renvoyé tel quel, D122). La main demeure au développeur : LE ZIP AUTO EST À LUI (aucun geste obligatoire), le geste B SHA-NI réel, la campagne de comparaison D204, la cérémonie d'ère, le séquestre D183, la réplication.
"""

WORKLOG = """

Task ID: 154
Agent: Z.ai (agent principal)
Task: L'ÉDITION AUTOMATISÉE DU PAQUET MULTIMACHINES (la commande du
développeur du 12/11/2026 : « je vois qu'il y a dans le kit des choses à
compiler. je veux que l'utilisation soit la plus simple possible, en
automatisant au maximum ») — les HUIT lanceurs (menu + 3 .bat kits + 3
.sh), la lettre A-LIRE-AUTOMATISATION.txt, les six retouches de LISEZMOI,
l'assemblage aux CINQ scellés recoupés, l'épreuve sur extraction vierge,
la consignation et la livraison.

Work Log:
- LES LANCEURS : COMMENCER-ICI.bat (le menu, voies QEMU par WSL2/détection
  wsl.exe), LANCER-KIT-1-SHANI.bat (python trouvé, rien à compiler),
  LANCER-KIT-2-DUDECT.bat (recoup de l'image scellée, compilation
  AUTOMATIQUE cl/gcc/clang sinon les exe précompilés, FALLBACK précompilé
  sur échec avec écart nommé, épreuve d'appel, LE RUN N=200 par défaut,
  BROUILLON DE TÉMOIN auto : CPU/OS/binaire/sha256/csv), LANCER-KIT-3-
  LOUPE.bat (recoup loupe.exe AVANT tout, python 64 bits vérifié),
  lancer-kit-constat-arm.sh (python installé par pkg s'il manque),
  lancer-voie1-m7d.sh et lancer-voie2-shani.sh (qemu trouvé/installé/la
  commande exacte rendue).
- L'ÉPREUVE SUR EXTRACTION VIERGE : voie 1 M7D 16 PASS/0 ÉCHEC VERT code 0
  PAR LE LANCEUR ; voie 2 shani émulé VERT code 0, le rapport 0,19× RENDU
  PAR LE RUN ; constat-arm VERT (le constat honnête « pas un téléphone
  ARM ») ; kit-2 recompilé gcc VERT (FIPS exact, autotest code 0) ;
  testzip/CRLF/ASCII/bits/scellés. La RELECTURE des .bat (aucun Windows
  au labo) a guéri : les call relatifs du menu, le refus sur échec de
  compilation (fallback) ; le diff éprouvé/livré : 38/40 identiques, les
  deux .bat corrigés seuls divergent.
- L'ASSEMBLAGE : 40 pièces, 5 scellés recoupés, les .bat en CRLF, les .sh
  exécutables — TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO.zip
  3 497 291 o sha256 814312a5… ; les preuves d'épreuve au dépôt
  (scripts/kits_mesure_v150/preuves-edition-auto-labo/ + la note
  d'épreuve).
- LA CONSIGNATION : l'Entrée 247 au journal, la présente tâche au worklog,
  le commit, le push GitHub, le miroir Drive et le kit Cérémonie tenus par
  le hook post-commit ; la livraison au bac download/ et au coffre /test.
- SUITE : au développeur — LE ZIP AUTO EST À LUI (un double-clic par kit,
  aucun geste obligatoire ; si un écran nomme un défaut, le .txt renvoyé
  tel quel D122), le geste B SHA-NI réel, la campagne de comparaison D204,
  la cérémonie d'ère, le séquestre D183, la réplication.
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
    if not PAQUET.exists():
        sys.exit("[consigner] le paquet AUTO est absent — refus")
    sha = hashlib.sha256(PAQUET.read_bytes()).hexdigest()
    if sha != PAQUET_SHA:
        sys.exit(f"[consigner] le paquet diverge ({sha[:12]}… != "
                 f"{PAQUET_SHA[:12]}…) — refus")
    print(f"[consigner] le paquet AUTO recoupé ({sha[:12]}…, "
          f"{PAQUET.stat().st_size} o)")
    for p in PREUVES:
        if not p.exists():
            sys.exit(f"[consigner] la preuve d'épreuve est absente : {p}")
    v1 = (PREUVES[1]).read_text(encoding="utf-8")
    if "16 PASS" not in v1 or "VERT" not in v1:
        sys.exit("[consigner] le verdict M7D d'épreuve est incohérent — refus")
    v2 = (PREUVES[2]).read_text(encoding="utf-8")
    if "VERT" not in v2 or "0.19" not in (PREUVES[1].parent.parent /
                                          "voie2-shani-emule" /
                                          "temoin-shani.txt").read_text(
                                              encoding="utf-8"):
        sys.exit("[consigner] le verdict/temoin shani émulé d'épreuve est "
                 "incohérent — refus")
    print("[consigner] les preuves d'épreuve présentes et cohérentes "
          "(M7D 16 PASS VERT, shani émulé VERT 0,19×, constat-arm VERT)")

    # 1. L'Entrée 247 au JOURNAL DE TRAVAIL (append-only)
    fin_journal = "le séquestre D183 ; la réplication)."
    append_verifie(REPO / "docs" / "JOURNAL_TRAVAIL.md", fin_journal,
                   ENTREE247, "JOURNAL_TRAVAIL.md (+Entrée 247)",
                   "## Entrée 247 — L'ÉDITION AUTOMATISÉE DU PAQUET")

    # 2. LA TASK 154 AU WORKLOG (append-only)
    fin_worklog = "le séquestre D183, la réplication."
    append_verifie(REPO / "worklog.md", fin_worklog, WORKLOG,
                   "worklog.md (+Task 154)", "Task ID: 154")
    print("[consigner] LES DEUX CONSIGNATIONS TENUES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
