#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree_246.py — LE PAQUET MULTIMACHINES CONSACRÉ : l'Entrée 246
au journal de travail (la commande du développeur du 12/11/2026 : « un zip
avec les kits terrain que je peux exécuter sur mes machines — téléphone ARM,
PC Windows 10 et 11, QEMU ou autre si besoin sur Windows ») et la Task 153
au worklog.

Append-only : les fins VÉRIFIÉES avant écriture, les rejeus REFUSÉS. Le paquet
(sha256 efff812b…), les autotests du correctif n° 1 du kit-dudect et les
preuves d'émulation contrôlés AVANT toute écriture — la consignation ne peut
pas précéder ses preuves.
"""

import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")

PAQUET = REPO / "download" / "TRIADE_kits_terrain_v0150_MULTIMACHINES.zip"
PAQUET_SHA = ("efff812b7b2eceb84dde76d3ce82996def3661b8d415523dabec"
              "4a0f98b3a76b")
PREUVES_EMULATION = [
    REPO / "scripts/kits_mesure_v150/qemu_emulation/"
    "preuves-shani-emulation-labo/temoin-shani.txt",
    REPO / "scripts/kits_mesure_v150/qemu_emulation/"
    "preuves-shani-emulation-labo/VERDICT-run-shani.txt",
]

# --- LES TEXTES -------------------------------------------------------------------

ENTREE246 = """

## Entrée 246 — LE PAQUET MULTIMACHINES LIVRÉ : la commande du développeur du 12/11/2026 (« faire un zip avec les kits terrain que je peux exécuter sur mes machines — téléphone ARM, PC Windows 10 et 11, QEMU ou autre si besoin sur Windows ») — TRIADE_kits_terrain_v0150_MULTIMACHINES.zip (3 478 725 o, sha256 efff812b…) : LES SIX KITS RÉUNIS ET ÉPROUVÉS (les trois machines Windows nommées, le téléphone, les deux voies QEMU), LE CORRECTIF n° 1 DU KIT-DUDECT PORTÉ (deux défauts latents de compilation Windows découverts à la cross-compilation, guéris à la source, le backend POSIX re-éprouvé VERT après le geste), LE KIT-CONSTAT-ARM NÉ (le troisième silicium, l'esprit D206 au téléphone — kit NOUVEAU, hors périmètre scellé v0.15.0), LA VOIE QEMU-SHANI ÉPROUVÉE AU LABORATOIRE (VERT code 0 sous qemu-x86_64 -cpu max — le rapport 0,19× consigné TEL QUEL : l'ARTEFACT TCG, jamais une vérité de silicium), LE KIT-3 COMPLÉTÉ (le coffre /test n'en portait que deux pièces sur quatre — les sources du dépôt ont complété, loupe.exe recoupé c1115105… EXACT) (12/11, la session de la préparation)

**La commande et la carte.** Le développeur nomma ses machines : le téléphone ARM, les PC Windows 10 et 11, QEMU ou autre si besoin sur Windows. Le paquet répond par UNE CARTE (LISEZMOI-MULTIMACHINES.txt) : kit-1-shani (le correctif n° 2 tel que livré — geste A déjà vécu et recoupé, Entrée 245), kit-2-dudect (LA mesure à vivre sur les siliciums Windows), kit-3-terrain-tiers-loupe (à vivre de préférence sur la machine Windows 11 — la machine tierce qui n'a JAMAIS servi au développement, la question même du kit), kit-constat-arm (le téléphone), et les DEUX voies QEMU sous WSL2 (le kit-m7d REJOUÉ — reproduction, la réserve D149 DEMEURE ; le kit-shani SOUS ÉMULATION — la chaîne sans le refus, la mesure N'Y EXISTE PAS).

**Le correctif n° 1 du kit-dudect (le défaut que seul le terrain pouvait révéler, révélé par la préparation elle-même).** À la cross-compilation Windows du mesureur : rand_s n'est déclaré par NI MSVC NI mingw-w64 sans _CRT_RAND_S posé AVANT stdlib.h — les instructions de compilation du LISEZMOI (cl /O2, gcc -O2) eussent échoué chez le développeur AU PREMIER GESTE ; et test_appel.c n'avait QUE le backend mmap POSIX (il ne compilait AUCUNEMENT sous Windows). DEUX défauts latents que l'autotest POSIX du laboratoire ne pouvait pas toucher — la classe exacte du correctif kit-shani (un défaut que SEUL le monde cible révèle). LE GESTE : _CRT_RAND_S posé à la source, le backend _WIN32 (VirtualAlloc/VirtualProtect) ajouté à test_appel.c, le correctif DATÉ ET NOMMÉ dans les deux en-têtes ; LE RE-ÉPREUVE après le geste (gcc -O2, le même sandbox) : test_appel VERT code 0 (FIPS abc EXACT, mutation K DIVERGE, restauration EXACT), dudect_v150 --autotest VERT code 0 (les quatre cibles recoupées, le t de Welch calculé — le mécanisme seul, AUCUN statut terrain). Les exe précompilés (dudect_v150.exe 1f1d8c96…, test_appel.exe f8b8e06e…, gcc 14-win32 mingw-w64, PE32+ x86-64, imports KERNEL32+msvcrt uniquement — rand_s résolu par mingw en pointeur RtlGenRandom chargé à l'exécution) : éprouvés à la compilation et par le backend POSIX du même source, NON EXÉCUTÉS au laboratoire (aucun Windows au labo ; wine installé au bac REFUSÉ par le noyau — ptrace signal 31) — l'étiquette honnête au LISEZMOI : le premier run se vit chez le développeur, la source est la vérité.

**Le kit-constat-arm (le chaînon qui manquait).** Les pièces scellées v0.15.0 sont toutes x86-64 Windows — le téléphone ne peut RIEN exécuter d'elles : le kit NOUVEAU (scripts/kits_mesure_v150/kit_constat_arm/, HORS périmètre scellé, étiqueté comme tel) CONSTATE au lieu de maquiller : la machine nommée à l'ouverture (D206 vécu au terrain ALEKPC), le silicium lu par ses propres canaux (/proc/cpuinfo : les cœurs par implémenter/part, la famille cryptographique ARMv8 aux Features — aes, pmull, sha1, sha2, sha512, sha3, sm3, sm4 ; getprop : le modèle, le SoC, l'Android), LE REFUS DES PIÈCES x86-64 NOMMÉ AVEC LEURS EMPREINTES, et le lecteur Python éprouvé au FIPS 180-4 « abc » (sha256 et sha512 EXACTS — un LECTEUR, jamais une mesure de temps : aucun protocole pré-enregistré n'existe pour ce silicium, aucun chiffre fabriqué ; si FEAT_SHA256 vit au téléphone, le constat le DIT et dit AUSSI que c'est une AUTRE famille d'instructions que la SHA-NI x86). La mécanique éprouvée au labo sur hôte x86-64 : VERT code 0, le script constatant honnêtement « ceci n'est pas un téléphone ARM » sans faillir — tout lecteur manquant est un constat nommé, jamais un crash muet. Le geste optionnel M7D-sur-Termux nommé COMME POSSIBILITÉ (aucun Android au labo — jamais une promesse).

**La voie qemu-shani (l'épreuve du laboratoire, la pièce jointe).** Le kit-shani exact (le n° 2 livré, d9def0b4…) exécuté sous qemu-x86_64 10.0.13 -cpu max sur l'hôte Linux du labo : VERDICT VERT, code 0 — le constat CPUID « AuthenticAMD » famille 6 modèle 6 (le CPU virtuel de qemu), les trois lecteurs EXACTS, l'adversaire K tranché, la mesure consignée, la pièce relue intacte — ET LE RAPPORT 0,19× (l'avant scalaire 2 136 cyc, l'après SHA-NI émulé 11 014 cyc) : LE TCG TRADUIT CHAQUE sha256rnds2 EN DES DIZAINES D'OPÉRATIONS HÔTES — le rapport émulé est un ARTEFACT DE TRADUCTION, consigné TEL QUEL au témoin du labo (preuves-shani-emulation-labo/, jointes au paquet ET déposées au coffre) : aucun chiffre maquillé, aucun statut fabriqué. LA FRONTIÈRE au LISEZMOI-qemu.txt : cette voie exerce LA CHAÎNE (le refus ne peut plus exister — qemu présente SHA-NI), elle ne MESURE pas ; la mesure avant/après n'a de sens que sur le VRAI silicium (le geste B demeure).

**Le kit-3 complété et le M7D embarqué.** Le coffre /test/loupe-kit-13 ne portait que DEUX pièces sur QUATRE (loupe.exe et le LISEZMOI — le scénario et le témoin vitrine manquaient au dossier, vivotant au dépôt git) : les sources du dépôt (loupe/terrain/) ont complété — scenario-loupe.py 0.1.1-dev.1 (131d0135…, les constantes FIGÉES qui assertent loupe.exe c1115105…) et temoin-vitrine.bat (6745d46f…). loupe.exe rapatrié du coffre et recoupé : c11151053576… == LE SCELLÉ, EXACT. Le kit-m7d extrait du zip du coffre (85f7b4bf…) avec ses scellés recoupés à l'extraction : corpus ec343b4e… MATCH, demo e57fc74b… MATCH, le qemu-riscv64 STATIQUE embarqué (14 821 328 o) — le kit AUTONOME, aucun paquet à installer.

**L'assemblage et l'épreuve bout-en-bout.** scripts/assembler_paquet_multimachines.py : 32 pièces, CINQ scellés recoupés À L'ASSEMBLAGE (loupe.exe, proxy-image ×2, corpus, demo — un kit corrompu est un refus nommé AVANT l'empaquetage), le zip 3 478 725 o sha256 efff812b7b2eceb84dde76d3ce82996def3661b8d415523dabec4a0f98b3a76b. L'ÉPREUVE sur extraction vierge (/tmp, jamais les sources) : testzip INTÈGRE ; constat-arm.py VERT code 0 ; la source dudect RECOMPILÉE depuis l'extrait gcc -O2, --autotest VERT code 0 (les cibles recoupées par le mesureur lui-même) ; LE KIT M7D COMPLET REJOUÉ depuis l'extrait : 16 PASS / 0 ÉCHEC, VERDICT VERT, code 0 (la bascule fence.i sous qemu, les refus nommés, le DEP falsifié, la falsification du démonstrateur, l'indifférence à la base, zéro régression — la réserve D149 NOMMÉE au témoin) — LE PAQUET DÉPOSÉ EST LE PAQUET PROUVÉ (D153, la discipline tenue).

**La livraison.** Le zip au bac download/ (D197) ; le dépôt au coffre /test (scripts/deposer_paquet_multimachines.py) : le dossier TRIADE_kits_terrain_v0150_MULTIMACHINES/ — la lettre, le zip, les quatre preuves d'émulation — 6/6 pièces md5 MATCH au re-listing intégral.

**Frontières.** Aucune pièce scellée touchée (le garde 14/14 le constatera au geste) ; le rapport 0,19× consigné TEL QUEL (l'artefact TCG nommé, jamais déguisé) ; les exe Windows NON exécutés au labo — l'étiquette honnête, le premier run au développeur ; le kit-constat-arm étiqueté HORS périmètre scellé ; les consignations antérieures non réécrites (append-only) ; aucun chiffre fabriqué — tout nombre est LU d'une pièce, d'un témoin ou d'une épreuve vécue ; la main demeure au développeur (LE ZIP EST À LUI : kit-2-dudect sur les siliciums Windows, kit-3 sur la machine tierce Windows 11, le constat au téléphone, les deux voies QEMU sous WSL2 si besoin — aucun geste obligatoire ; le geste B SHA-NI réel ; la campagne de comparaison D204 ; la cérémonie d'ère ; le séquestre D183 ; la réplication).
"""

WORKLOG = """

Task ID: 153
Agent: Z.ai (agent principal)
Task: LE PAQUET MULTIMACHINES (la commande du développeur du 12/11/2026 :
« un zip avec les kits terrain que je peux exécuter sur mes machines —
téléphone ARM, PC Windows 10 et 11, QEMU ou autre si besoin sur
Windows ») — le correctif n° 1 du kit-dudect (les défauts latents de
compilation Windows, guéris à la source), le kit-constat-arm NÉ, la
voie qemu-shani épreuvée, le kit-3 complété, l'assemblage aux CINQ
scellés recoupés, l'épreuve bout-en-bout, la livraison au bac et au
coffre.

Work Log:
- LE CORRECTIF n° 1 DU KIT-DUDECT : à la cross-compilation Windows,
  rand_s non déclaré (ni MSVC ni mingw-w64 sans _CRT_RAND_S) et
  test_appel.c POSIX-seul (mmap) — DEUX défauts latents que l'autotest
  POSIX ne pouvait pas toucher ; _CRT_RAND_S posé à la source, le
  backend _WIN32 ajouté, le re-épreuve VERT (test_appel code 0 ;
  dudect --autotest code 0) ; LES EXE précompilés (gcc 14-win32
  mingw-w64, PE32+ x86-64, imports KERNEL32+msvcrt) — NON exécutés au
  labo (wine refusé par le bac, ptrace), l'étiquette honnête au
  LISEZMOI.
- LE KIT-CONSTAT-ARM : le téléphone nommé, le silicium lu par ses
  canaux (/proc/cpuinfo, getprop), le refus des pièces x86-64 nommé
  avec empreintes, le lecteur FIPS abc exact — kit NOUVEAU hors
  périmètre scellé, éprouvé au labo (VERT code 0 sur hôte x86-64, le
  constat « pas un téléphone ARM » honnête).
- LA VOIE QEMU-SHANI : le kit n° 2 exécuté sous qemu-x86_64 -cpu max —
  VERT code 0, rapport 0,19× = l'ARTEFACT TCG consigné tel quel (les
  preuves au paquet et au coffre) ; LE M7D embarqué (scellés corpus/
  demo MATCH à l'extraction du zip du coffre).
- LE KIT-3 COMPLÉTÉ : /test/loupe-kit-13 ne portait que 2 pièces sur 4
  — les sources du dépôt ont complété (scenario-loupe.py 0.1.1-dev.1,
  temoin-vitrine.bat) ; loupe.exe recoupé c1115105… EXACT.
- L'ASSEMBLAGE : 32 pièces, 5 scellés recoupés, le zip 3 478 725 o
  sha256 efff812b… ; L'ÉPREUVE sur extraction vierge : constat-arm
  VERT, dudect source recompilée VERT, M7D 16 PASS / 0 ÉCHEC VERT —
  le paquet déposé est le paquet prouvé (D153).
- LA LIVRAISON : le zip au bac download/ (D197), le dossier au coffre
  /test 6/6 pièces md5 MATCH (la lettre, le zip, les 4 preuves
  d'émulation).
- SUITE : au développeur — LE ZIP EST À LUI (kit-2-dudect sur les
  siliciums Windows, kit-3 sur la machine tierce, le constat au
  téléphone, les voies QEMU sous WSL2 — aucun geste obligatoire), le
  geste B SHA-NI réel, la campagne de comparaison D204, la cérémonie
  d'ère, le séquestre D183, la réplication.
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
    # 0. LES PREUVES AVANT LE TEXTE — le paquet et l'épreuve d'émulation
    if not PAQUET.exists():
        sys.exit("[consigner] le paquet est absent — refus "
                 "(la consignation ne précède pas ses preuves)")
    sha = hashlib.sha256(PAQUET.read_bytes()).hexdigest()
    if sha != PAQUET_SHA:
        sys.exit(f"[consigner] le paquet diverge ({sha[:12]}… != "
                 f"{PAQUET_SHA[:12]}…) — refus")
    print(f"[consigner] le paquet recoupé ({sha[:12]}…, "
          f"{PAQUET.stat().st_size} o)")
    for p in PREUVES_EMULATION:
        if not p.exists():
            sys.exit(f"[consigner] la preuve d'émulation est absente : {p.name}")
    t = PREUVES_EMULATION[0].read_text(encoding="utf-8")
    if "0.19" not in t or "AuthenticAMD" not in t:
        sys.exit("[consigner] le témoin d'émulation ne porte pas le rapport "
                 "0,19× / le CPU qemu — refus")
    print("[consigner] les preuves d'émulation présentes et cohérentes")

    # 1. L'Entrée 246 au JOURNAL DE TRAVAIL (append-only)
    fin_journal = "le séquestre D183 ; la réplication)."
    append_verifie(REPO / "docs" / "JOURNAL_TRAVAIL.md", fin_journal,
                   ENTREE246, "JOURNAL_TRAVAIL.md (+Entrée 246)",
                   "## Entrée 246 — LE PAQUET MULTIMACHINES LIVRÉ")

    # 2. LA TASK 153 AU WORKLOG (append-only)
    fin_worklog = "d'ère, le séquestre D183, la réplication."
    append_verifie(REPO / "worklog.md", fin_worklog, WORKLOG,
                   "worklog.md (+Task 153)", "Task ID: 153")
    print("[consigner] LES DEUX CONSIGNATIONS TENUES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
