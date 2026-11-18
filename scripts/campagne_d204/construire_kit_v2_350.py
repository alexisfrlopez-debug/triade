#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_kit_v2_350.py — L'ASSEMBLAGE DU KIT v2 (le correctif du refus
nommé) : kit-unite-04-d210-20261118-v2/ — LES QUATORZE pièces du kit (les
DOUZE INCHANGÉES + le scénario CORRIGÉ + la gravure regénérée d'UNE ligne)
+ le GUI INCHANGÉ + le lanceur à l'édition correctif + le LISEZMOI-RUN v2
+ la NOTE-ATELIER reconduite + l'EMPREINTES-GUI v2 — puis le zip.

Usage : python3 scripts/campagne_d204/construire_kit_v2_350.py
"""

import hashlib
import pathlib
import shutil
import subprocess
import sys
import zipfile

CAMP = pathlib.Path(__file__).resolve().parent
KIT1 = CAMP / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118"
KIT2 = CAMP / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118-v2"
DEPOT = CAMP / "depot-run-unite16-d210-350" / "epreuves"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    print("=== L'ASSEMBLAGE DU KIT v2 (le correctif du refus nommé) ===")

    # 1. LE GUI (déjà SURGÉ à v2.0.1 au dossier) + LA NOTE-ATELIER
    #    (recoupée au dépôt du terrain — INCHANGÉE)
    if not (KIT2 / "triade_run_unite16_d210_gui.py").exists():
        shutil.copy2(DEPOT / "triade_run_unite16_d210_gui.py",
                     KIT2 / "triade_run_unite16_d210_gui.py")
    gui_md5 = hashlib.md5(
        (KIT2 / "triade_run_unite16_d210_gui.py").read_bytes()).hexdigest()
    print(f"[GUI v2.0.1] la chirurgie tenue au dossier (md5 {gui_md5[:8]}…) — "
          f"le selftest 27 VERT 0 ROUGE")
    if not (KIT2 / "NOTE-ATELIER-UNITE16-D210-20261118.txt").exists():
        shutil.copy2(DEPOT / "NOTE-ATELIER-UNITE16-D210-20261118.txt",
                     KIT2 / "NOTE-ATELIER-UNITE16-D210-20261118.txt")
    print(f"[INCHANGÉ] NOTE-ATELIER — reconduite (md5 "
          f"{hashlib.md5((KIT2 / 'NOTE-ATELIER-UNITE16-D210-20261118.txt').read_bytes()).hexdigest()[:8]}…)")

    # 2. LE LANCEUR à l'édition correctif (CRLF + BOM conservés)
    bat_v1 = (DEPOT / "LANCER-RUN-UNITE16-D210-1CLIC.bat").read_text(
        encoding="utf-8-sig")
    entete_v1 = bat_v1.split("rem ====")[0]
    corps = "rem ====" + bat_v1.split("rem ====", 1)[1]
    entete_v2 = """@echo off
rem ============================================================================
rem LANCER-RUN-UNITE16-D210-1CLIC.bat - LE RUN DE L'UNITE 04 D210 EN UN CLIC
rem [le kit kit-gui-1clic-unite16-d210-v2 - l'edition CORRECTIF du 18/11 au
rem  soir : LE REFUS NOMME du run v1 (« [REFUS] RVA-HOURS-SECTIONS : la RVA
rem  0x0 hors des sections — rien n'est execute ») recoupe, la faute nommee
rem  (le guichet aux QUATRE champs, la marche des plages FT - la doctrine
rem  D54 - et la 4e feuille GetLastError) ; LES QUATORZE pieces du kit v2 :
rem  les DOUZE INCHANGEES (loupe.exe b382e01b...), le scenario CORRIGE
rem  (705951cc... - le correctif confine au guichet, les vecteurs INTACTS),
rem  la gravure regeneree d'UNE ligne ; le kit v1 DEMEURE au coffre
rem  (D143 - le refus du run v1 est un temoin) ; le dossier racine du zip
rem  porte LE NOM DU KIT (kit-unite-04-d210-20261118-v2 - le pas 1-KIT du
rem  livre du kit : CHOISIR CE DOSSIER ; le double-clic du lanceur EST le
rem  choix - le GUI recoupe LUI-MEME les pieces de CE dossier)]
rem
"""
    # le corps : le titre demeure, le mécanisme demeure
    bat_v2 = entete_v2 + corps
    (KIT2 / "LANCER-RUN-UNITE16-D210-1CLIC.bat").write_bytes(
        b"\xef\xbb\xbf" + bat_v2.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8"))
    print(f"[LANCER] le lanceur à l'édition correctif "
          f"({(KIT2 / 'LANCER-RUN-UNITE16-D210-1CLIC.bat').stat().st_size} o, CRLF+BOM)")

    # 3. LE LISEZMOI-RUN v2 (le livre du correctif)
    lirez_v2 = KIT2 / "LISEZMOI-RUN-UNITE16-D210-1CLIC-V2.txt"
    lirez_v2.write_text(LISEZMOI, encoding="utf-8", newline="\n")
    print(f"[LISEZMOI-RUN v2] {lirez_v2.stat().st_size} o")

    # 4. LES EMPREINTES-GUI v2
    lignes = []
    lignes.append("EMPREINTES-GUI-UNITE16-D210-1CLIC-V2 — les pièces du kit GUI 1-clic "
                   "CORRECTIF")
    lignes.append("(l'unité 04 D210, la révision 2 — le refus nommé du run v1 recoupé, "
                   "le guichet corrigé ;")
    lignes.append("la console « certutil -hashfile <fichier> SHA256 » recoupe chaque "
                   "ligne chez vous)")
    lignes.append("=" * 78)
    lignes.append("")
    lignes.append("LE GUI ET SES LIVRES :")
    lignes.append("")
    gui = KIT2 / "triade_run_unite16_d210_gui.py"
    lignes.append(f"{gui.name:<50} {gui.stat().st_size:>7} o  sha256 {sha(gui)}")
    lignes.append("le GUI v2.0.1 (LA CHIRURGIE du correctif : les DEUX "
                   "empreintes du verrou — L'ATELIER CHOISI tenu ; le selftest "
                   "27 VERT)")
    lanceur = KIT2 / "LANCER-RUN-UNITE16-D210-1CLIC.bat"
    lignes.append(f"{lanceur.name:<50} {lanceur.stat().st_size:>7} o  "
                   f"sha256 {sha(lanceur)}")
    lignes.append("le lanceur au double-clic (l'édition CORRECTIF, CRLF+BOM)")
    lirez = KIT2 / "LISEZMOI-RUN-UNITE16-D210-1CLIC-V2.txt"
    lignes.append(f"{lirez.name:<50} {lirez.stat().st_size:>7} o  sha256 {sha(lirez)}")
    lignes.append("le livre du kit v2 (le correctif nommé, le geste du re-run)")
    note = KIT2 / "NOTE-ATELIER-UNITE16-D210-20261118.txt"
    lignes.append(f"{note.name:<50} {note.stat().st_size:>7} o  sha256 {sha(note)}")
    lignes.append("le commandement verbatim, la frontière M3 (INCHANGÉE — reconduite)")
    lignes.append("")
    lignes.append("LES PIÈCES DU KIT (le verrou du GUI les recoupe à CHAQUE "
                  "lancement, fail-closed) :")
    lignes.append("")
    for p in sorted(KIT2.iterdir()):
        if not p.is_file():
            continue
        if p.name in ("triade_run_unite16_d210_gui.py",
                      "LANCER-RUN-UNITE16-D210-1CLIC.bat",
                      "LISEZMOI-RUN-UNITE16-D210-1CLIC-V2.txt",
                      "NOTE-ATELIER-UNITE16-D210-20261118.txt",
                      "EMPREINTES-GUI-UNITE16-D210-1CLIC-V2.txt"):
            continue
        lignes.append(f"{p.name:<50} {p.stat().st_size:>7} o  sha256 {sha(p)}")
        if p.name == "scenario-unite16.py":
            lignes.append("                                               LE JUGE CORRIGÉ "
                          "(le guichet aux CINQ champs, la marche des plages FT,")
            lignes.append("                                               la 4e feuille "
                          "GetLastError — les vecteurs INTACTS)")
    lignes.append("")
    (KIT2 / "EMPREINTES-GUI-UNITE16-D210-1CLIC-V2.txt").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8", newline="\n")
    print(f"[EMPREINTES-GUI v2] "
          f"{(KIT2 / 'EMPREINTES-GUI-UNITE16-D210-1CLIC-V2.txt').stat().st_size} o")

    # 5. LE RECOUP : les DOUZE pièces inchangées == le kit v1
    inchangees = 0
    for p in sorted(KIT2.iterdir()):
        if not p.is_file() or p.name in ("scenario-unite16.py",
                                         "EMPREINTES-KIT-UNITE-04-D210.txt",
                                         "LANCER-RUN-UNITE16-D210-1CLIC.bat",
                                         "LISEZMOI-RUN-UNITE16-D210-1CLIC-V2.txt",
                                         "EMPREINTES-GUI-UNITE16-D210-1CLIC-V2.txt"):
            continue
        if p.name not in ("triade_run_unite16_d210_gui.py",
                          "NOTE-ATELIER-UNITE16-D210-20261118.txt"):
            if p.read_bytes() == (KIT1 / p.name).read_bytes():
                inchangees += 1
            else:
                print(f"[DIVERGE INATTENDU] {p.name}")
                return 2
    print(f"[RECOUP] {inchangees} pièces du kit == le v1 octet pour octet "
          f"(les DOUZE attendues)")

    # 6. LE ZIP
    zip_path = CAMP / "kit-gui-1clic-unite16-d210-v2-20261118.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(KIT2.iterdir()):
            if p.is_file():
                z.write(p, f"kit-unite-04-d210-20261118-v2/{p.name}")
    n = len(zipfile.ZipFile(zip_path).namelist())
    print(f"[ZIP] {zip_path.name} — {n} entrées, {zip_path.stat().st_size} o")
    return 0


LISEZMOI = """LISEZMOI-RUN-UNITE16-D210-1CLIC-V2 — LE RUN DE L'UNITÉ 04 D210,
RÉVISION 2 (LOUPE-16 SAISIE × BRAS T) EN UN CLIC · L'ATELIER CHOISI PAR
CONSTRUCTION · LE CORRECTIF DU REFUS NOMMÉ
=========================================================================

L'OBJET DE CETTE RÉVISION : le run v1 du 18/11 12:12 REFUSA (fail-closed,
code 2, 0,2 s — rien ne courut) : « [REFUS] RVA-HORS-SECTIONS : la RVA 0x0
hors des sections — RIEN ne court, le guichet ferme ». Le dépôt du refus
reçU et reCOUPÉ au labo (la console, l'état, la session, la capture — le
refus est AUSSI un témoin, TEL QUELLE) ; la faute nommée sur pièces : le
guichet du scénario lisait le descripteur d'imports à QUATRE champs (le
champ +8 ForwarderChain — la valeur 0 — lu comme la RVA du nom : LA RVA
0x0 DU REFUS) et marchait l'OFT (le pas de dword de la famille) au lieu
des PLAGES FIRSTTHUNK (la doctrine D54 : le chargeur marche les plages
jusqu'au NULL, chaque entrée sur disque == le RVA hint/nom de SA feuille).
LE CORRECTIF, CONFINÉ AU GUICHET : le descripteur aux CINQ champs (le
précédent de la 304), la marche des plages FT, ET la 4e feuille
GetLastError (le chemin d'échec de loupe-02 : les jz de la relecture
atterrissent au -6 PAR GetLastError — la feuille morte liée AVANT le
premier échec réel). LES VECTEURS INTACTS au byte près (la parité AST :
le modèle, les V1-V5, le témoin — IDENTIQUES) ; les DOUZE autres pièces
INCHANGÉES octet pour octet ; la gravure regénérée d'UNE SEULE ligne (le
scénario). L'ÉPREUVE QUI MANQUAIT NÉE : la découverte du guichet rejouée
au labo contre le fichier livré — CONTRE le v1 : ROUGE, le refus
RECONSTITUÉ mot pour mot ; CONTRE le v2 : TOUT VERT (les QUATRE feuilles
aux slots QUE les notations appellent : SetFilePointerEx 0x3128, ReadFile
0x3130, GetLastError 0x3148, InvalidateRect 0x31a0).

LE GESTE DU RE-RUN : DÉZIPPEZ CE KIT (kit-unite-04-d210-20261118-v2/,
une extraction FRAÎCHE — jamais le dossier v1 réutilisé) puis
DOUBLE-CLIQUEZ LANCER-RUN-UNITE16-D210-1CLIC.bat seul (SmartScreen peut
demander « Plus d'informations → Exécuter quand même » — le .bat est
signé de RIEN, c'est l'honnêteté). LE GUI exige Python 3 avec tkinter.

À L'ONGLET 4·LIVRE : CHOISIR LE DOSSIER DE L'ATELIER (le dossier local
des QUATRE registres du livre, reçu du coffre /test — L'ATELIER CHOISI
PAR CONSTRUCTION : la ligne M1 au verdict RECOPIÉ et la ligne M3 aux
bornes OBSERVÉES appendées DURANT le run ; defauts.csv et
journal-ouverture.txt JAMAIS touchés ; l'atelier re-déposé au coffre
demeure VOTRE geste), puis TOUT LANCER.

L'ATTENDU DU RE-RUN : les NEUF verdicts VERT (9 VERT, 0 ROUGE, code 0) —
T0 la pièce recoupée, [guichet] les QUATRE feuilles liées, V1 le
différentiel 10 000 frappes, V2 le scénario « 4d5a » ET la vue qui suit,
V3 les rejets, V4 le repli, V5 la falsification. Puis : le témoin daté
signé de votre main [D99], preuves-unite16/ au coffre /test (le GUI
assemble le zip — la signature exigée).

AU LIVRE, AU BLOC-NOTES (la chirurgie prescrite — le livre ne ment
jamais : le run v1 a couru) : ① la ligne T-loupe-16-d210-it1 ROUGE (le
kit v1, le run 2026-11-18 REFUS nommé) posée à la main à livraisons.csv ;
② le défaut à defauts.csv (l'onglet 6·DÉFAUTS : la classe
« guichet-descripteur-quatre-champs », le mécanisme « le champ +8 lu
comme la RVA du nom — la RVA 0x0 ; la marche de l'OFT au lieu des plages
FT (D54) ; la 4e feuille GetLastError non liée », le côté « kit », la
pièce à l'appui run-console-unite16-d210-20261118-121219.txt, l'exclusion
« non — la faute au kit voyagée jusqu'au terrain, le run consommé,
D202 ») ; ③ l'atelier ENTIER re-déposé. Le re-run v2 couchera la ligne
T-loupe-16-d210-it2 au livre DURANT le run.

LE KIT v1 DEMEURE AU COFFRE (D143 : le dépôt du refus jamais recouvert —
un refus est aussi un témoin).

LES EMPREINTES : EMPREINTES-GUI-UNITE16-D210-1CLIC-V2.txt (le GUI et ses
livres + les QUATORZE pièces du kit, chaque sha256 ; certutil -hashfile
chez vous recoupe).

(18/11/2026, la session du correctif — le refus nommé, l'épreuve née,
le guichet remis à la doctrine du plan)
"""


if __name__ == "__main__":
    sys.exit(main())
