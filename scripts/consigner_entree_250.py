#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree_250.py — LE DÉPÔT « RUN AUTO SUR 2 ORDIS » CONSACRÉ :
l'Entrée 250 au journal de travail (l'annonce du développeur du 12/11/2026 :
« j'ai lancé le run auto sur 2 ords différents, j'ai tout mis dans /test du
drive ») et la Task 157 au worklog.

Append-only : les fins VÉRIFIÉES avant écriture, les rejeus REFUSÉS. Les
SIX preuves rapatriées (md5 contre le manifeste du sondage) et le rapport de
recoupement 35/35 VERT contrôlés AVANT toute écriture — la consignation ne
peut pas précéder ses preuves.
"""

import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")

SONDAGE = REPO / "scripts" / "kits_mesure_v150" / "edition_mise_a_jour" / "sondage_depots_2machines.json"
DEST = REPO / "preuves-depots-maj-2machines"
RAPPORT = DEST / "recoupement-depots-2machines.txt"
RAPPORT_SHA = ("586121136c3e56e182cff975196513dbea76af6de0077c0f5f"
               "a51cc35da9ec03")

PREUVES_RUN = [
    "pc-windows/kit-1-shani/preuves-shani/VERDICT-run-shani.txt",
    "pc-windows/kit-1-shani/preuves-shani/scenario-shani-journal.log",
    "pc-windows/kit-3-terrain-tiers-loupe/loupe-kit-13/preuves-loupe/temoin-loupe.txt",
    "qemu-wsl2/kit-m7d/preuves-m7/VERDICT-run-m7d.txt",
    "qemu-wsl2/kit-m7d/preuves-m7/scenario-m7d-journal.log",
    "qemu-wsl2/kit-m7d/preuves-m7/temoin-m7d.txt",
]

# --- LES TEXTES -------------------------------------------------------------------

ENTREE250 = """

## Entrée 250 — LE DÉPÔT « RUN AUTO SUR 2 ORDIS » REÇU : LE KIT-1 REFUSÉ UNE TROISIÈME FOIS, LE KIT-3 VERT AU QUATORZIÈME RUN, LA VOIE 1 M7D VERTE POUR LA PREMIÈRE FOIS HORS DU LABORATOIRE (l'annonce du développeur du 12/11/2026 : « j'ai lancé le run auto sur 2 ords différents, j'ai tout mis dans /test du drive ») — les dépôts /test/TRIADE_kits_terrain_v0150_MULTIMACHINES-MISE-A-JOUR et MISE-A-JOUR2, le recoupement 35/35 VERT (rapport sha256 586121136c3e…) (12/11, le quatrième geste de la journée)

**La machine 1 (ALEKPC · Windows 11 · Python 3.14.3 — le journal la nomme).** LE KIT-1 SHANI REFUSÉ UNE TROISIÈME FOIS (14:28:26 locale == le mtime Drive 13:28:26.522Z, deux voix indépendantes) : le même ÉCHEC NOMMÉ T0.silicium — « GenuineIntel » · famille 6 · modèle 142 · pas 12 · SHA-NI ABSENT, CPUID feuille 7 EBX bit 29 = 0 — et le VERDICT (md5 17fd82f7…) == celui du geste A (le /test CORRECTIF2, deux voix Drive) ET du dépôt AUTO (l'Entrée 248), OCTET POUR OCTET : TROIS refus au même byte ; le journal ne diffère du précédent QUE par l'heure (13:36:01 → 14:28:26 locale) ; D206 tenue une troisième fois (QUI a exécuté, QUOI a refusé) — le kit ne peut pas inventer le silicium, le refus EST le résultat. PUIS LE KIT-3 LOUPE, QUATORZE SECONDES PLUS TARD (14:28:40 locale), LE QUATORZIÈME RUN TERRAIN : le scellé c111510535767a40… asserté au T0 ; T0→T7+S0 TOUT VERT (l'arène, la session, la double lecture, LE PANNEAU md5 5fc07b786150… · sha256 == hashlib, les lignes, la recherche à 577 == bytes.find, l'édition à l'octet 0x00 → 0x4D SEUL, les rejets nommés -2/-5/-3/-1, la pièce relue INCHANGÉE) ; LA SONDE 205 : P1 LE TROU et P4 LA GÉOMÉTRIE refusés par le VRAI chargeur (GetLastError 193, NTSTATUS 0xc000007b — l'axe nommé) ; le témoin == celui du 13e run AUX ADRESSES ASLR ET À LA POIGNÉE PRÈS (38/38 lignes du gabarit) — VERT SUR PIÈCES : l'application née de TRIADE a vécu chez son utilisateur, une deuxième fois dans la journée.

**La machine 2 (Linux 6.18.58.1-microsoft-standard-WSL2 · glibc 2.43 · Python 3.14.4 — un hôte Windows par WSL2).** LA VOIE 1 M7D — LE KIT M7D REJOUÉ SOUS LE qemu-riscv64 EMBARQUÉ (md5 bae5a36f… == la pièce du paquet livré, l'instrument du kit, jamais un qemu de la machine) : 16 PASS / 0 ÉCHEC, VERDICT VERT (14:31:15 +0100 au témoin == les mtimes Drive 13:31:15-17Z) — et LES 16 LIGNES PASS == CELLES DU RUN DU LABORATOIRE (l'Entrée 249) OCTET POUR OCTET : l'universalité rejouée, le labo (noyau 5.10.134, Python 3.12.16) et le WSL2 du développeur rendent le MÊME verdict par le MÊME instrument ; les DEUX scellés assertés avant tout geste (corpus ec343b4e…, le scellé 0.8.0-rc.1 du jalon M7 ; demo e57fc74b…, le démonstrateur invité f72001) ; ZÉRO RÉGRESSION (le patch est un fait de la session INVITÉE, jamais du fichier) ; la réserve instrumentale D149 NOMMÉE au témoin (le TCG exécute l'ISA, le noyau et les syscalls sont réels de l'hôte — une émulation de processus, jamais déguisée en exécution native). LA PREMIÈRE FOIS HORS DU LABORATOIRE — la frontière honnête : l'identité Windows de l'hôte WSL2 n'est pas au témoin, la voix du développeur nomme les DEUX machines.

**Le recoupement sur pièces (scripts/recouper_depots_maj_2machines.py — chaque contrôle calculé depuis les pièces, aucun chiffre recopié ; le rapport preuves-depots-maj-2machines/recoupement-depots-2machines.txt sha256 586121136c3e…, 35/35 VERT).** LA CHAÎNE : les 46 pièces de CHACUN des deux dépôts == le paquet livré (l'Entrée 249) md5 PAR md5, les DEUX machines parties du MÊME paquet (0 divergence) ; LA CHRONOLOGIE : livraison 13:25Z → upload machine 1 13:26:57Z → kit-1 13:28:26Z → kit-3 13:28:40Z → M7D 13:31:17Z — les deux machines à l'œuvre en cinq minutes, AUCUNE inversion ; les mtimes 13:00:00.000Z exactes des pièces du paquet MISE-A-JOUR2 sont un ARTEFACT de l'outil d'upload du développeur — la chaîne tient par le CONTENU (md5), jamais par les mtimes. LES FRONTIÈRES : LE KIT-2 DUDECT TOUJOURS PAS COURU (aucun temoin-dudect-BROUILLON.txt ni journal-dudect-*.csv dans AUCUN dépôt — LA SEULE MESURE JAMAIS ENCORE VÉCUE du paquet) ; le DIAGNOSTIC-MACHINE (le témoin diagnostic-machine.txt), le constat-arm, la voie 2 QEMU (les preuves-shani-emulation-labo demeurent celles du LABO, md5 == le paquet) et le témoin vitrine : PAS VÉCUS — aucun geste obligatoire, rien maquillé.

**La consignation.** L'Entrée 250 au journal, la Task 157 au worklog, le commit, le push GitHub, le miroir Drive et le kit Cérémonie tenus par le hook post-commit ; les SIX preuves rapatriées au dépôt git (preuves-depots-maj-2machines/ — les .log bruts demeurent au coffre /test, leurs contenus cités mot pour mot au présent) ; le manifeste du sondage (sondage_depots_2machines.json, 49 + 49 pièces) et les trois scripts (sonder, rapatrier, recouper) au dépôt.

**Frontières.** Aucune pièce scellée touchée ; les dépôts du développeur JAMAIS modifiés (lecture et rapatriement seuls, jamais d'écriture au /test) ; les consignations antérieures non réécrites (append-only) ; aucun chiffre fabriqué — tout nombre est LU d'une pièce, d'un témoin ou d'une métadonnée Drive ; la main demeure au développeur : LE KIT-2 DUDECT à courir (le grand manquant — un double-clic, aucun Python ni compilateur requis, puis l'état EFFECTIF du turbo au BIOS et la signature), le DIAGNOSTIC-MACHINE pour choisir la machine du geste B SHA-NI réel, le constat-arm au téléphone, la voie 2 QEMU, le témoin vitrine, la campagne de comparaison D204, la cérémonie d'ère, le séquestre D183, la réplication.
"""

WORKLOG = """

Task ID: 157
Agent: Z.ai (agent principal)
Task: LE DÉPÔT « RUN AUTO SUR 2 ORDIS » REÇU ET RECOUPÉ (l'annonce du
développeur du 12/11/2026 : « j'ai lancé le run auto sur 2 ords
différents, j'ai tout mis dans /test du drive ») — le sondage des DEUX
dépôts (MISE-A-JOUR et MISE-A-JOUR2, 49 pièces chacun), le rapatriement
des SIX preuves de run (md5 vérifiés), le recoupement 35/35 VERT, la
consignation.

Work Log:
- LE SONDAGE (scripts/sonder_depots_maj_2machines.py, manifeste
  sondage_depots_2machines.json) : /test porte les DEUX dossiers —
  MISE-A-JOUR (machine 1, l'upload 13:26:57Z) et MISE-A-JOUR2 (machine
  2, les mtimes 13:00:00.000Z exactes = artefact de l'outil d'upload).
- LE RAPATRIEMENT (scripts/rapatrier_depots_maj_2machines.py) : les SIX
  preuves de run téléchargées, chaque md5 == la métadonnée Drive —
  machine 1 : VERDICT + journal du kit-1 (13:28:26Z), témoin du kit-3
  (13:28:40Z) ; machine 2 : VERDICT + journal + témoin de la voie 1 M7D
  (13:31:15-17Z).
- LE KIT-1 (machine 1 : ALEKPC · Windows 11 · Python 3.14.3) : REFUSÉ
  UNE TROISIÈME FOIS — le même ÉCHEC NOMMÉ T0.silicium (« GenuineIntel »
  · famille 6 · modèle 142 · pas 12 · SHA-NI ABSENT, CPUID feuille 7 EBX
  bit 29 = 0) ; le VERDICT md5 17fd82f7… == geste A == dépôt AUTO, TROIS
  refus au même byte ; le journal ne diffère QUE par l'heure (14:28:26
  locale == le mtime Drive) ; D206 tenue une 3e fois.
- LE KIT-3 (machine 1, 14 s après) : LE QUATORZIÈME RUN TERRAIN, VERT
  SUR PIÈCES — le scellé c1115105… asserté, T0→T7+S0 tout vert, la
  sonde 205 : P1 et P4 refusés par le VRAI chargeur (GetLastError 193,
  NTSTATUS 0xc000007b) ; le témoin == celui du 13e run aux adresses
  ASLR et à la poignée près (38/38 lignes du gabarit).
- LA VOIE 1 M7D (machine 2 : WSL2 6.18.58.1 · glibc 2.43 · Python
  3.14.4) : 16 PASS / 0 ÉCHEC VERT, LA PREMIÈRE FOIS HORS DU LABO —
  l'instrument == le qemu-riscv64 EMBARQUÉ du kit (md5 bae5a36f…), les
  16 lignes PASS == celles du run du labo OCTET POUR OCTET (l'universalité
  rejouée), les deux scellés assertés, ZÉRO RÉGRESSION, la réserve D149
  nommée au témoin.
- LE RECOUPEMENT (scripts/recouper_depots_maj_2machines.py, rapport
  sha256 586121136c3e…, 35/35 VERT) : LA CHAÎNE (les 46 pièces de chaque
  dépôt == le paquet livré md5 par md5, les deux machines parties du
  MÊME paquet), LA CHRONOLOGIE (livraison 13:25Z → kit-1 13:28:26Z →
  kit-3 13:28:40Z → M7D 13:31:17Z, aucune inversion), LES FRONTIÈRES (le
  kit-2 dudect TOUJOURS PAS COURU — la seule mesure jamais vécue ; le
  diagnostic, le constat-arm, la voie 2, la vitrine : pas vécus).
- LA CONSIGNATION : l'Entrée 250 au journal, la présente tâche au
  worklog, le commit, le push GitHub, le miroir Drive et le kit
  Cérémonie tenus par le hook post-commit ; les .log bruts demeurent au
  coffre /test, leurs contenus cités mot pour mot.
- SUITE : au développeur — LE KIT-2 DUDECT (le grand manquant : un
  double-clic, aucun Python ni compilateur requis), le DIAGNOSTIC pour
  choisir la machine du geste B, le constat-arm au téléphone, la voie 2
  QEMU, le témoin vitrine, la campagne D204, la cérémonie d'ère, le
  séquestre D183, la réplication.
"""


# --- L'APPEND VÉRIFIÉ (la fin attendue de chaque pièce) ----------------------------

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
    # 0. LES PREUVES AVANT LE TEXTE — le sondage, les six pièces, le rapport
    if not SONDAGE.exists():
        sys.exit("[consigner] le manifeste du sondage est absent — refus "
                 "(la consignation ne précède pas ses preuves)")
    manifeste = json.loads(SONDAGE.read_text(encoding="utf-8"))
    n1 = manifeste["MISE-A-JOUR"]["nb_pieces"]
    n2 = manifeste["MISE-A-JOUR2"]["nb_pieces"]
    if (n1, n2) != (49, 49):
        sys.exit(f"[consigner] le sondage ne porte pas 49+49 pièces ({n1}+{n2}) — refus")
    print(f"[consigner] le sondage recoupé ({n1} + {n2} pièces)")

    index_md5 = {}
    for depot, info in manifeste.items():
        for p in info["pieces"]:
            index_md5[(depot, p["chemin"].split("/", 1)[1])] = p["md5"]
    verifiees = 0
    for chemin_rel in PREUVES_RUN:
        p = None
        for depot in manifeste:
            cand = DEST / depot / chemin_rel
            if cand.exists():
                p = cand
                md5_calc = hashlib.md5(p.read_bytes()).hexdigest()
                if md5_calc != index_md5[(depot, chemin_rel)]:
                    sys.exit(f"[consigner] {depot}/{chemin_rel} : md5 diverge — refus")
                verifiees += 1
                break
        if p is None:
            sys.exit(f"[consigner] la preuve rapatriée est ABSENTE : {chemin_rel} — refus")
    if verifiees != 6:
        sys.exit(f"[consigner] {verifiees}/6 preuves vérifiées — refus")
    print("[consigner] les SIX preuves rapatriées, md5 tous == Drive")

    if not RAPPORT.exists():
        sys.exit("[consigner] le rapport de recoupement est absent — refus")
    sha = hashlib.sha256(RAPPORT.read_bytes()).hexdigest()
    if sha != RAPPORT_SHA:
        sys.exit(f"[consigner] le rapport diverge ({sha[:12]}… != "
                 f"{RAPPORT_SHA[:12]}…) — refus")
    if "BILAN : 35 VERT / 0 ROUGE" not in RAPPORT.read_text(encoding="utf-8"):
        sys.exit("[consigner] le rapport ne porte pas le bilan 35/35 VERT — refus")
    print(f"[consigner] le rapport de recoupement recoupé ({sha[:12]}…, 35/35 VERT)")

    # 1. L'Entrée 250 au JOURNAL DE TRAVAIL (append-only)
    fin_journal = ("le diagnostic pour choisir la machine du geste B, la campagne "
                   "de comparaison D204, la cérémonie d'ère, le séquestre D183, la réplication.")
    append_verifie(REPO / "docs" / "JOURNAL_TRAVAIL.md", fin_journal,
                   ENTREE250, "JOURNAL_TRAVAIL.md (+Entrée 250)",
                   "## Entrée 250 — LE DÉPÔT « RUN AUTO SUR 2 ORDIS » REÇU")

    # 2. LA TASK 157 AU WORKLOG (append-only)
    fin_worklog = ("voies QEMU, le\n"
                   "  DIAGNOSTIC pour choisir la machine du geste B, la campagne D204, la\n"
                   "  cérémonie d'ère, le séquestre D183, la réplication.")
    append_verifie(REPO / "worklog.md", fin_worklog, WORKLOG,
                   "worklog.md (+Task 157)", "Task ID: 157")
    print("[consigner] LES DEUX CONSIGNATIONS TENUES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
