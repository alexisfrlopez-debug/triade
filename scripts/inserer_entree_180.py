#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_180.py — LA CONSIGNATION DU GESTE « LE PREMIER RUN TERRAIN
(f) RECROPÉ : ROUGE T1.la-résolution NOMMÉ — L'ERRATUM n° 6 DU KIT réparé à
la source, le kit corrigé ré-déposé au coffre /test » : JOURNAL_TRAVAIL
+Entrée 180 (ordre 179<180<marqueur, rejeu REFUSÉ), worklog +Task ID 98.
Tout ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit.

La datation : la présente porte le 06/11 au soir (le geste du développeur
« preuves déposées dans le dossier /test du drive » reçu le 06/11 — le run :
2026-11-06 16:17:51)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 180 — LE PREMIER RUN TERRAIN (f) REÇU ET RECROPÉ (« preuves déposées dans le dossier /test du drive ») : ROUGE `T1.la-résolution` NOMMÉ ; L'ERRATUM n° 6 du kit (la base de l'artefact aux lecteurs de SSN au lieu de la base ntdll) NOMMÉ SUR PIÈCES ET RÉPARÉ À LA SOURCE ; le kit corrigé ré-déposé au coffre /test — le second geste du développeur attendu (06/11 au soir)

**Le geste du développeur reçu, rapatrié, recoupé — l'échec est honnête, la faute est au labo.** LE RAPATRIEMENT (scripts/rapatrier_preuves_m9f.py — le modèle rapatrier_preuves_m7d.py, D99 : zéro mélange, dossier dédié download/preuves-run-m9f/, lecture seule) : les TROIS pièces du run téléchargées, md5 contrôlés PAR PIÈCE contre les métadonnées Drive (temoin-m9f.txt 1 444 o, md5 81ff1a30… ; scenario-m9f-journal.log 106 o, md5 4f5972a0… ; VERDICT-run-m9f.txt 1 809 o, md5 8e141128…) ; les DEUX pièces conditionnelles (ligne-recue.txt, journal-emissions.txt) NON DÉPOSÉES — le constat nommé : elles naissent à T4/T6, le run est mort à T1, leur absence est UNE PREUVE DE COHÉRENCE, jamais un manque. LE RECOUP (scripts/recouper_preuves_m9f.py — 25/25 PASS sur pièces croisées, D138/D145/D148, le juge est le code : constantes lues PAR AST dans la source, l'artefact re-haché, la cause RECONSTITUÉE depuis les octets du dépôt) : LE RUN ROUGE CONSTATÉ COHÉRENT — le témoin porte les SEIZE contrôles T0 tranchés [ok] AUX NOMS EXACTS DE LA SOURCE dans l'ordre du code (l'empreinte d8928934… ASSERTÉE avant tout geste, l'octet de l'erratum n° 5 relu DANS L'IMAGE, les slots scellés, les fixtures transport, le DNS, L'EMPREINTE ÉPINGLÉE 045d0758…) ; le journal porte « T0 VERT » puis LA LIGNE DU REFUS AU TEXTE EXACT DE LA SOURCE (« le miroir Python refuse « NtCreateFile » : répertoire export absent » — le code -3 de lire_ssn_python) et MEURT LÀ (deux lignes) ; le verdict porte « VERDICT : ROUGE — 1 échec(s) nommé(s) : T1.la-résolution » + le conseil honnête + le témoin embarqué == LA PIÈCE LIGNE POUR LIGNE + l'horodatage unique (2026-11-06 16:17:51 partout). LE TERRAIN EST LAVÉ : le VRAI ntdll localisé (base 0x7ffc01790000, C:\\WINDOWS\\System32\\ntdll.dll) et haché (sha256 36b1a62e4bf6bf7d68458fff6e8a33b39f6527ec6a46e55ecdd12cde83894c8d — la pièce d'analyse de l'avenir), l'artefact relu INTACT (sha256 d8928934… re-calculé au geste même == la carte génération 10), le scénario DU KIT == la source du dépôt OCTET POUR OCTET (38 465 o — le développeur a exécuté LE scénario du labo, sans modification) ; L'ENVIRONNEMENT consigné : Windows 10.0 build 19045 (10 22H2), Python 3.14.6 AMD64, la cible résolue 104.16.123.96 — le kit visait Windows 11 : la maison NOMME l'écart, le scénario ne l'interdit pas, si afd.sys diverge le refus sera NOMMÉ.

**L'erratum n° 6 — la faute au kit, jamais au terrain (la preuve de la garde encore : un échec honnête vaut plus qu'un vert muet).** LE CONSTAT SUR PIÈCES : T1 appelait `ssn_par_deux_lecteurs(base, …)` — `base` est la base de L'ARTEFACT cartographié à T0 (proxy.exe), PAS `ntdll_base` (localisé à T0 par GetModuleHandleW) ; or proxy.exe N'A PAS de répertoire export (data directory[0] == 0 — recalculé AU geste même depuis le dépôt), et le miroir Python lit le répertoire export du module qu'on lui donne : le refus -3 « répertoire export absent » était INÉVITABLE SUR TOUTE MACHINE Windows — le premier kit ne pouvait PAS franchir T1, aucune machine n'en était coupable. LES T2/T3/T5 passaient correctement `ntdll_base` à sys-04/05/06 (constaté : la confusion touchait les seuls TROIS sites de `ssn_par_deux_lecteurs`) ; l'artefact n'est PAS en cause (PE32+ valide, le motif de stub 4C 8B D1 B8 correct dans la source : c'est la BASE passée qui était fautive, jamais la machine du développeur). LA RÉPARATION À LA SOURCE (jamais un correctif local) : tls13/terrain/scenario-m9f.py — les TROIS sites de résolution (NtCreateFile, NtDeviceIoControlFile, NtClose) reçoivent désormais `ntdll_base`, le commentaire d'erratum consigné au site même ; LE CONTRÔLE PERMANENT : scripts/assembler_kit_m9f.py [2b] — l'AST EXIGE `ntdll_base` au premier argument DES TROIS lecteurs de SSN (REFUS nommé ERRATUM-6 sinon), CONTRÔLE NÉGATIF PROUVÉ sur la source pré-réparation (la pointe 20ab30f : 3 sites, 0 à ntdll_base → REFUS) — la faute ne peut plus dormir ; LA REJOUABILITÉ des pièces du recoup : E3/E5 lisent LA SOURCE À LA POINTE pré-réparation 20ab30f (l'histoire fait foi, le geste corrige l'arbre).

**Le kit corrigé réassemblé, éprouvé, ré-déposé — le coffre /test passe au second geste.** L'ASSEMBLAGE (scripts/assembler_kit_m9f.py rejoué) : l'artefact 1.0.0-dev.2 ASSERTÉ inchangé (65 024 o, sha256 d8928934…), les 26 constantes recoupées PAR AST == l'artefact/le plan/la sonde (l'octet 0x72 relu DANS L'IMAGE @0x10082), LE CONTRÔLE PERMANENT [2b] VERT, py_compile VERT, l'extraction vierge VERT — kit-m9f.zip 35 522 o, md5 7d5380ceb19420f62cd4481f14431284, sha256 85c75fc11ef8f1c4ff6527fb1515410970321fc28c0ca6155d926f6b198a0c83. LE COFFRE (scripts/corriger_kit_m9f.py — le modèle corriger_kit_m8d.py + cloturer_run_m8d.py, D143 : archivage par DÉPLACEMENT, jamais un jet) : kit-m9f.zip MIS À JOUR EN PLACE (upload_update — le contenu remplacé, le fichier même conservé, md5 7d5380ce… MATCH par relecture ; l'ancien scénario vit dans l'histoire git à la pointe 20ab30f) ; LISEZMOI-m9f.txt MIS À JOUR EN PLACE (md5 b1b91887… — l'erratum n° 6 consigné au document du kit, la note d'environnement Windows) ; LE PREMIER RUN ARCHIVÉ : les TROIS pièces DÉPLACÉES de preuves-m9f/ vers archives-preuves/preuves-run-m9f/ (md5 constatés après le geste) + VERDICT-recoup-labo-m9f.txt déposé AVEC elles (l'archive porte le jugement avec les pièces — modèle m8d/Entrée 155) ; preuves-m9f/ RÉ-ARMÉ (il ne porte plus que son LISEZMOI-preuves.txt — le réceptacle du second run) ; LES DEUX INDEX mis à jour (LISEZMOI-archives-preuves.txt : la section preuves-run-m9f ; LISEZMOI-archives-livraisons.txt : la note de correction) ; LA RACINE vérifiée (13 entrées, les résidents intacts).

**Détail.** FRONTIÈRES : le scellé 0.9.0 INTACT (m8/proxy.exe 1492b0bc… — non touché par le geste), l'ARTEFACT 1.0.0-dev.2 INTACT (sha256 d8928934… relu au recoup et à l'assemblage : l'erratum n° 6 touche LE SCÉNARIO DU KIT, jamais l'artefact), les arbres I INCHANGÉS (le scénario terrain est HORS du sceau), AUCUNE balise posée (la finale 1.0.0 attend le SECOND run terrain vert — le scellage sera un fait de carte, D104), la clé privée jamais traversée (D87). Livrables : scripts/rapatrier_preuves_m9f.py, scripts/recouper_preuves_m9f.py (la pièce rejouable : la pointe pré-réparation lue dans l'histoire) + download/preuves-run-m9f/VERDICT-recoup-labo-m9f.txt (ROUGE CONSTATÉ COHÉRENT 25/25), scripts/corriger_kit_m9f.py, scripts/maj_plan_m9k.py, tls13/terrain/scenario-m9f.py (l'erratum n° 6 réparé : `ntdll_base` aux trois lecteurs), scripts/assembler_kit_m9f.py (LE CONTRÔLE PERMANENT [2b]), tls13/terrain/LISEZMOI-KIT-M9F.md (l'erratum consigné), download/kit-m9f.zip (le kit corrigé, md5 7d5380ce…), l'ancien kit-m9f.zip (md5 a73fb526…) demeuré dans l'histoire git (pointe 20ab30f). Consignations : la présente Entrée 180 PAR SCRIPT, PLAN (maj_plan_m9k.py : la rangée (f) + l'État du programme), worklog +Task ID 98. SUITE : LE SECOND GESTE DU DÉVELOPPEUR — dézipper kit-m9f.zip (au coffre /test du Drive, la version CORRIGÉE md5 7d5380ce…), python scenario-m9f.py (Windows, réseau vivant, ~10 s) → renvoyer preuves-m9f/ ENTIER au coffre /test/preuves-m9f/ → le labo recoupe (D138/D145/D148) → si vert : LA FINALE 1.0.0 (fait de carte — D104) : le jalon M9 franchi — LA GRANDE ŒUVRE."""

TASK = """## Task ID 98 — LE PREMIER RUN TERRAIN (f) REÇU (« preuves déposées dans le dossier /test du drive ») ET RECROPÉ : ROUGE T1.la-résolution NOMMÉ, 25/25 sur pièces croisées ; L'ERRATUM n° 6 du kit (la base de l'artefact aux lecteurs de SSN au lieu de la base ntdll) NOMMÉ SUR PIÈCES ET RÉPARÉ À LA SOURCE ; LE KIT CORRIGÉ RÉ-DÉPOSÉ AU COFFRE /test — le second geste du développeur attendu (06/11 au soir)

- LE RAPATRIEMENT + LE RECOUP : rapatrier_preuves_m9f.py (les TROIS
  pièces md5 contrôlés par pièce ; les DEUX pièces T4/T6 absentes ==
  cohérentes avec la mort à T1) ; recouper_preuves_m9f.py — ROUGE
  CONSTATÉ COHÉRENT 25/25 (D138/D145/D148, le juge est le code : les
  SEIZE T0 aux noms exacts de la source, le refus T1 AU TEXTE EXACT, le
  témoin embarqué == la pièce LIGNE POUR LIGNE, l'horodatage unique
  16:17:51) ; LE TERRAIN LAVÉ : le VRAI ntdll localisé et haché
  (36b1a62e…), l'artefact relu INTACT (d8928934…), le scénario du kit ==
  la source du dépôt octet pour octet ; l'environnement consigné :
  Windows 10.0 build 19045 (10 22H2), Python 3.14.6 AMD64.
- L'ERRATUM n° 6 (LA FAUTE AU KIT, JAMAIS AU TERRAIN) : T1 passait
  `base` (l'ARTEFACT cartographié — proxy.exe N'A PAS de répertoire
  export, data directory[0] == 0 recalculé au geste même) aux lecteurs
  de SSN au lieu de `ntdll_base` : le refus -3 « répertoire export
  absent » était INÉVITABLE sur toute machine. RÉPARÉ À LA SOURCE : les
  TROIS sites de scenario-m9f.py reçoivent `ntdll_base` ; LE CONTRÔLE
  PERMANENT : assembler_kit_m9f.py [2b] — l'AST EXIGE `ntdll_base` aux
  trois lecteurs (contrôle négatif PROUVÉ sur la source pré-réparation :
  REFUS) ; la rejouabilité des pièces : E3/E5 du recoup lisent la
  source à la POINTE pré-réparation 20ab30f (l'histoire fait foi).
- LE KIT CORRIGÉ RÉ-DÉPOSÉ : réassemblé et rééprouvé (26 constantes PAR
  AST == l'artefact/le plan/la sonde, l'octet 0x72 relu DANS L'IMAGE,
  py_compile, extraction vierge VERT) — kit-m9f.zip 35 522 o, md5
  7d5380ce…, sha256 85c75fc1… ; corriger_kit_m9f.py : kit-m9f.zip MIS À
  JOUR EN PLACE au /test (md5 MATCH par relecture, rien jeté), le
  LISEZMOI porte l'erratum (md5 b1b91887…), LE PREMIER RUN archivé
  (les TROIS pièces → archives-preuves/preuves-run-m9f/ AVEC le
  VERDICT-recoup-labo — l'archive porte le jugement), preuves-m9f/
  ré-armé (son LISEZMOI seul), les DEUX index mis à jour, la racine
  vérifiée (13 entrées).
- FRONTIÈRES : le scellé 0.9.0 INTACT, l'ARTEFACT 1.0.0-dev.2 INTACT
  (l'erratum touche LE SCÉNARIO, jamais l'artefact), les arbres I
  inchangés, AUCUNE balise (la finale 1.0.0 attend le SECOND run vert,
  D104), la clé privée jamais traversée (D87) ; livrables :
  rapatrier_preuves_m9f.py, recouper_preuves_m9f.py +
  VERDICT-recoup-labo-m9f.txt, corriger_kit_m9f.py, maj_plan_m9k.py,
  scenario-m9f.py corrigé, assembler_kit_m9f.py [2b],
  LISEZMOI-KIT-M9F.md, kit-m9f.zip corrigé ; consignations : Entrée 180
  PAR SCRIPT, PLAN (maj_plan_m9k.py : la rangée (f) + l'État), worklog
  +Task ID 98.
- SUITE : LE SECOND GESTE DU DÉVELOPPEUR — dézipper kit-m9f.zip (la
  version CORRIGÉE md5 7d5380ce…), python scenario-m9f.py (~10 s,
  réseau vivant) → renvoyer preuves-m9f/ ENTIER au coffre → le labo
  recoupe → si vert : LA FINALE 1.0.0 (fait de carte) — le jalon M9
  franchi, LA GRANDE ŒUVRE.

Stage Summary:
- LE PREMIER RUN EST UN ÉCHEC HONNÊTE, ET LA FAUTE EST AU LABO : le
  verdict ROUGE T1.la-résolution est cohérent de bout en bout (25/25),
  le terrain est lavé (le VRAI ntdll haché, l'artefact intact, le
  scénario exécuté fidèlement) — la garde a refusé d'extraire un numéro
  d'un module sans exports : exactement ce qu'on lui demande.
- L'ERRATUM n° 6 EST RÉPARÉ À LA SOURCE avec un contrôle PERMANENT à
  l'assemblage (l'AST exige ntdll_base aux trois lecteurs — contrôle
  négatif prouvé) : la faute ne peut plus dormir.
- LE KIT CORRIGÉ EST AU COFFRE /test (md5 7d5380ce…) : le second geste
  du développeur est attendu — si vert : la finale 1.0.0, le jalon M9
  franchi — LA GRANDE ŒUVRE."""


def main():
    if not JOURNAL.exists():
        sys.exit("ÉCHEC : journal introuvable")
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 180" in journal:
        sys.exit("ÉCHEC : Entrée 180 déjà consignée (rejeu REFUSÉ)")
    if "## Entrée 179" not in journal:
        sys.exit("ÉCHEC : ancrage Entrée 179 introuvable")
    if MARQUEUR not in journal:
        sys.exit("ÉCHEC : marqueur introuvable")
    i179 = journal.index("## Entrée 179")
    im = journal.index(MARQUEUR)
    if not (i179 < im):
        sys.exit("ÉCHEC : l'ordre 179<marqueur est rompu")
    if "## Entrée 180" in journal[i179:im]:
        sys.exit("ÉCHEC : état inattendu entre 179 et le marqueur")
    # l'insertion APRÈS la SECTION 179 (la leçon de l'Entrée 175 :
    # TOUJOURS après la section, avant le marqueur)
    journal = journal[:im] + ENTREE + "\n\n" + journal[im:]
    JOURNAL.write_text(journal, encoding="utf-8")

    if not WORKLOG.exists():
        sys.exit("ÉCHEC : worklog introuvable")
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 98" in worklog:
        sys.exit("ÉCHEC : Task ID 98 déjà consigné (rejeu REFUSÉ)")
    if "## Task ID 97" not in worklog:
        sys.exit("ÉCHEC : ancrage Task ID 97 introuvable")
    worklog = worklog.rstrip("\n") + "\n\n" + TASK + "\n"
    WORKLOG.write_text(worklog, encoding="utf-8")

    print("[consignation] Entrée 180 déposée au journal "
          "(ordre 179<180<marqueur)")
    print("[consignation] Task ID 98 déposé au worklog")
    print("[consignation] la relecture fait foi :")
    j = JOURNAL.read_text(encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    assert j.index("## Entrée 179") < j.index("## Entrée 180") < j.index(MARQUEUR)
    assert "## Entrée 180" in j and "erratum n° 6" in j
    assert "7d5380ceb19420f62cd4481f14431284" in j
    assert "T1.la-résolution" in j and "ntdll_base" in j
    assert "## Task ID 98" in w and w.index("## Task ID 97") < w.index("## Task ID 98")
    print("[consignation] ORDRE et ANCRAGES constatés — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
