#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree_245.py — LA RÉCEPTION DU GESTE A CONSACRÉE : l'Entrée 245
au journal de travail (le refus auto-portant du terrain — le run du correctif
n° 2, 12/11 11:26 heure locale du développeur) et la Task 152 au worklog.

Append-only : les fins VÉRIFIÉES avant écriture, les rejeus REFUSÉS. Le
rapport de recoupement (21/21 VERT) et les pièces du geste A contrôlés
AVANT toute écriture — la consignation ne peut pas précéder ses preuves.
"""

import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")

RAPPORT = REPO / "preuves-run-shani" / "recoupement-geste-a.txt"
RAPPORT_SHA = ("32072b83944772fb2c32914fb4f70cd6de9b9ea003f5cba"
               "005f2724332e9ace5")
PIECES = [
    REPO / "preuves-run-shani" / ("TRIADE_kits_terrain_v0150_CORRECTIF2-"
                                  "kit-shani_kit-shani_preuves-shani_"
                                  "VERDICT-run-shani.txt"),
    REPO / "preuves-run-shani" / ("TRIADE_kits_terrain_v0150_CORRECTIF2-"
                                  "kit-shani_kit-shani_preuves-shani_"
                                  "scenario-shani-journal.log"),
]

# --- LES TEXTES -------------------------------------------------------------------

ENTREE245 = """

## Entrée 245 — LE GESTE A REÇU : LE REFUS AUTO-PORTANT DU TERRAIN (le run du correctif n° 2, 12/11 11:26 heure locale du développeur — l'annonce « kit shani avec preuves déposé dans /test du drive ») : LA PIÈCE DÉFINITIVE EXISTE — le silicium du développeur nommé par son CPUID dans SON propre verdict (machine ALEKPC · AMD64 · Windows · Python 3.14.3 ; « GenuineIntel » · famille 6 · modèle 142 · pas 12 · SHA-NI ABSENT — CPUID feuille 7, EBX bit 29 = 0), LA RÈGLE D206 CONFIRMÉE AU TERRAIN par le geste même qu'elle exigeait, LE RECOUPEMENT 21/21 VERT (la chaîne de garde close : le scénario exécuté EST l'octet-pour-octet le n° 2 livré d9def0b4… ; la chronologie datée aux métadonnées Drive — le kit livré 10:16 UTC, le run 10:26:54 UTC, le dépôt 10:28:10 UTC) — D205 DEMEURE CONSACRÉE AU LABORATOIRE, JAMAIS SCELLÉE ; le geste B (la mesure sur un silicium SHA-NI) demeure au développeur, AUCUN geste obligatoire (12/11, la session de réception)

**Le dépôt et le rapatriement.** L'annonce du développeur : « kit shani avec preuves déposé dans /test du drive ». Le /test re-listé : 496 entrées — L'ARITHMÉTIQUE EXACTE DE L'ATTENTE (478 à l'Entrée 244 avant sa livraison + l'arbre CORRECTIF2 livré [16 entrées : 11 pièces + 5 dossiers] + les DEUX pièces du geste A), aucune entrée de premier niveau créée après la livraison hors l'arbre attendu — AUCUN AUTRE DÉPÔT. Le rapatriement (lecture seule, scripts/rapatrier_preuves_shani.py) : les 25 fichiers « shani » vers preuves-run-shani/, dont les DEUX pièces nouvelles du geste A déposées par le développeur dans kit-shani/preuves-shani/ du dossier CORRECTIF2 — le VERDICT-run-shani.txt (588 o) et le scenario-shani-journal.log (325 o).

**La chronologie, datée aux métadonnées Drive.** Les pièces du kit (le scénario, le moteur) créées 10:16:08-10:16:12 UTC — LA LIVRAISON de l'Entrée 244, jamais re-téléversées ; les pièces du geste A créées 10:28:10.063Z (le verdict) et 10:28:10.227Z (le journal) — déposées ENSEMBLE, 164 ms d'écart. Le journal ouvre le run à 11:26:54 heure locale (10:26:54 UTC — l'écart d'une heure recoupant la locale Europe/Paris, comme au run de 10:02) : LE RUN PRÉCÈDE SON DÉPÔT DE 76 SECONDES. Le geste est cohérent de bout en bout : recevoir le correctif n° 2 (10:16), remplacer le scénario, exécuter (10:26:54), renvoyer les preuves (10:28:10).

**Le run et le verdict, reçus TEL QUELS.** Le journal, QUATRE lignes : « machine : ALEKPC · AMD64 · Windows · Python 3.14.3 — LE RUN TERRAIN » (LA MACHINE À L'OUVERTURE — l'exigence de D206) ; « T0 — le témoin : les empreintes et le silicium » ; « T1 — l'arène : l'allocation, la pose des pièces » (LA CLASSE DU CRASH DEMEURE MORTE) ; « T0.silicium — constat CPUID : « GenuineIntel » · famille 6 · modèle 142 · pas 12 · SHA-NI ABSENT ». Le verdict : ÉCHEC NOMMÉ — « T0.silicium : les extensions SHA sont présentes — CONSTAT : « GenuineIntel » · famille 6 · modèle 142 · pas 12 · SHA-NI ABSENT — CPUID feuille 7, EBX bit 29 = 0 : CE silicium n'exécute pas sha256rnds2, la mesure avant/après n'y existe pas ; le kit ne peut pas inventer le silicium » — LE VERDICT EST AUTO-PORTANT : QUI a exécuté (la machine, journalisée à l'ouverture) et QUOI a refusé (le constat CPUID complet, au journal ET au verdict). L'échec recoupe celui du 10:02 (le même geste T0.silicium, la même machine) et le NOMME désormais : fabricant, famille, modèle, pas. Aucun témoin n'est né (le run s'arrête avant T4 — la mesure n'existe pas sur ce silicium, le kit a refusé de mesurer exactement comme conçu).

**Le recoupement, 21/21 VERT** (scripts/recouper_geste_a_shani.py — le rapport à preuves-run-shani/recoupement-geste-a.txt, sha256 32072b839447…). QUATRE groupes. (A) LE DÉPÔT : le premier niveau du /test sans entrée tardive (29 entrées, aucune créée après la livraison), le recompte récursif 496 EXACT, les pièces du geste A postérieures à la livraison, les pièces du kit datant de la livraison. (B) LA CHAÎNE : le scénario du kit n° 2 au /test EST l'octet-pour-octet le scénario livré (d9def0b4…, 33 925 o — LE KIT EXÉCUTÉ FUT LE KIT LIVRÉ) ; moteur-shani.bin IDENTIQUE au n° 1, au kit du dépôt et à l'original du laboratoire (761ab194…, l'empreinte du témoin) ; la source, le manifeste, l'image et le LISEZMOI IDENTIQUES ; la plage scellée tls13-02 recoupée au manifeste (RVA 0xC080, 448 o, 2ce2517a…) ; le moteur exécuté de l'autotest == le moteur livré (LA PIÈCE RELUE INTACTE). (C) LE RUN : les quatre lignes du journal, le constat IDENTIQUE au journal et au verdict, la règle « un verdict d'échec se renvoie TEL QUEL », ET LA MUTATION DE FORMAT — le journal du geste A porte la ligne machine (le format du n° 2), celui du 10:02 (n° 1) n'en portait PAS : LE SCÉNARIO EXÉCUTÉ FUT LE N° 2, preuve par le format même. (D) L'AUTOTEST v2 : les quatre pièces du /test == les copies du laboratoire (download/preuves-run-shani-autotest-labo-v2/), le témoin cohérent (machine c-6af57fe2…, modèle 173, 819.8 → 128.6 cycles/compression = 6,37×, les empreintes du moteur et de l'image).

**Ce que cela statue.** L'arc du kit-shani terrain est COMPLET : le crash du scénario livré (l'extension de signe ctypes 0xFFFFFFFFD4991000), la guérison et l'échec muet (le correctif n° 1, 10:02 — D206 naît de ce mutisme), la guérison et l'ÉCHEC AUTO-PORTANT (le correctif n° 2, 11:26 — la règle D206 tenue au terrain par le geste même du développeur, la boucle fermée en trois actes). LA MESURE AVANT/APRÈS N'EXISTE PAS SUR LA MACHINE DU DÉVELOPPEUR — un fait de silicium, consigné ; les mesures du laboratoire demeurent ce qu'elles sont (D205 : 5,84× au protocole 8 Mio de l'instruction ; les autotests du kit : 6,37× et 6,38× à leur propre protocole — des statuts laboratoire, aucun généralisé). D205 EST ET DEMEURE CONSACRÉE AU LABORATOIRE, JAMAIS SCELLÉE — l'embarquement, s'il advient, exigera la cérémonie d'ère du développeur. Le geste B (exécuter le même kit sur tout silicium SHA-NI à sa main — Ice Lake et après chez Intel, Ryzen chez AMD) DEMEURE POSSIBLE, jamais exigé : le fait de silicium est consigné, l'arc est clos.

**Frontières.** Aucune pièce scellée touchée ; le verdict d'échec consigné TEL QUEL (la règle du kit — la ligne nomme le défaut) ; les consignations antérieures non réécrites (append-only — D206 et les Entrées 242-244 demeurent) ; les journaux bruts (*.log) vivent au coffre /test — la règle *.log du .gitignore les exclut du miroir git, leurs contenus cités ici mot pour mot, le /test fait foi ; aucun chiffre fabriqué — tout nombre est LU d'une pièce, d'un témoin ou d'une métadonnée ; la main demeure au développeur (le geste B — aucun obligatoire ; les trois autres kits EN ATTENTE ; la cérémonie d'ère ; la campagne D204 ; le séquestre D183 ; la réplication).
"""

WORKLOG = """

Task ID: 152
Agent: Z.ai (agent principal)
Task: LA RÉCEPTION DU GESTE A (l'annonce du développeur « kit shani avec
preuves déposé dans /test du drive ») — le rapatriement des preuves du
correctif n° 2, le recoupement 21/21 VERT (la chaîne de garde close, la
chronologie datée aux métadonnées Drive), la consignation de l'Entrée 245 :
le refus auto-portant du terrain — la règle D206 confirmée au terrain,
D205 demeurant consacrée au laboratoire, jamais scellée.

Work Log:
- LE RAPATRIEMENT : le /test re-listé (496 entrées = 478 + l'arbre n° 2
  [16] + le geste A [2], aucun autre dépôt — le premier niveau sans
  entrée tardive), les 25 fichiers shani rapatriés dont les DEUX pièces
  du geste A (le VERDICT 588 o, le journal 325 o).
- LE RECOUPEMENT (scripts/recouper_geste_a_shani.py, rapport à
  preuves-run-shani/recoupement-geste-a.txt, sha256 32072b83…) : 21/21
  VERT — LA CHAÎNE (le scénario exécuté == le n° 2 livré d9def0b4… ; le
  moteur, la source, les cibles et le LISEZMOI identiques au n° 1 et au
  dépôt ; la plage scellée tls13-02 recoupée au manifeste ; le moteur
  exécuté == le moteur livré), LA CHRONOLOGIE (le kit livré 10:16 UTC,
  le run 10:26:54 UTC — 11:26:54 heure locale, le dépôt 10:28:10 UTC,
  76 s après le run), LE RUN AUTO-PORTANT (la machine ALEKPC journalisée
  à l'ouverture, le constat CPUID « GenuineIntel » · famille 6 · modèle
  142 · pas 12 · SHA-NI ABSENT au journal ET au verdict, la mutation de
  format prouvant le scénario n° 2), L'AUTOTEST v2 == les copies du
  laboratoire (le témoin 6,37×).
- LA CONSIGNATION : l'Entrée 245 au journal de travail, la présente
  tâche au worklog, le commit, le push GitHub, le miroir Drive et le kit
  Cérémonie tenus par le hook post-commit.
- SUITE : au développeur — le geste B (aucun obligatoire), les trois
  autres kits EN ATTENTE, la campagne de comparaison D204, la cérémonie
  d'ère, le séquestre D183, la réplication.
"""


# --- L'APPEND VÉRIFIÉ (la fin attendue de chaque pièce) ----------------------------

def append_verifie(chemin: pathlib.Path, fin_attendue: str, bloc: str,
                   nom: str, marqueur_doublon: str) -> None:
    texte = chemin.read_text(encoding="utf-8")
    if marqueur_doublon in texte:
        sys.exit(f"[consigner] {nom} : {marqueur_doublon} déjà présent — "
                 "rejeu refusé (append-only)")
    if not texte.rstrip("\n").endswith(fin_attendue.rstrip("\n")):
        sys.exit(f"[consigner] {nom} : la fin attendue n'est pas la "
                 "dernière section — append refusé")
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(bloc)
    print(f"[consigner] {nom} : appendé ({len(bloc)} o)")


def main() -> int:
    # 0. LES PREUVES AVANT LE TEXTE — le rapport et les pièces du geste A
    if not RAPPORT.exists():
        sys.exit("[consigner] le rapport de recoupement est absent — "
                 "refus (la consignation ne précède pas ses preuves)")
    sha = hashlib.sha256(RAPPORT.read_bytes()).hexdigest()
    if sha != RAPPORT_SHA:
        sys.exit(f"[consigner] le rapport de recoupement diverge "
                 f"({sha[:12]}… != {RAPPORT_SHA[:12]}…) — refus")
    print(f"[consigner] le rapport 21/21 VERT recoupé ({sha[:12]}…)")
    for p in PIECES:
        if not p.exists():
            sys.exit(f"[consigner] la pièce du geste A est absente : {p.name}")
    print("[consigner] les deux pièces du geste A présentes")

    # 1. L'Entrée 245 au JOURNAL DE TRAVAIL (append-only)
    fin_journal = "le séquestre D183 ; la réplication)."
    append_verifie(REPO / "docs" / "JOURNAL_TRAVAIL.md", fin_journal,
                   ENTREE245, "JOURNAL_TRAVAIL.md (+Entrée 245)",
                   "## Entrée 245 — LE GESTE A REÇU")

    # 2. LA TASK 152 AU WORKLOG (append-only)
    fin_worklog = "le séquestre D183, la\n  réplication."
    append_verifie(REPO / "worklog.md", fin_worklog, WORKLOG,
                   "worklog.md (+Task 152)", "Task ID: 152")
    print("[consigner] LES DEUX CONSIGNATIONS TENUES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
