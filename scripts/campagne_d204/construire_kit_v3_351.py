#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_kit_v3_351.py — L'ASSEMBLAGE DU KIT v3 (le correctif du crash
nommé) : kit-unite-04-d210-20261118-v3/ — LES QUATORZE pièces du kit (les
DOUZE INCHANGÉES + le scénario CORRIGÉ d'UN SEUL argument — la liaison
memmove au TROISIÈME argument, le compte 8 — + la gravure regénérée d'UNE
ligne) + le GUI v2.0.2 (LA CHIRURGIE sur les DEUX empreintes du verrou) +
le lanceur à l'édition correctif v3 + le LISEZMOI-RUN v3 + la NOTE-ATELIER
reconduite + l'EMPREINTES-GUI v3 — puis le zip.

Usage : python3 scripts/campagne_d204/construire_kit_v3_351.py
"""

import ast
import hashlib
import pathlib
import py_compile
import shutil
import subprocess
import sys
import zipfile

CAMP = pathlib.Path(__file__).resolve().parent
KIT1 = CAMP / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118"
KIT2 = CAMP / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118-v2"
KIT3 = CAMP / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118-v3"

LA_LIGNE_FAUTIVE = "        ctypes.memmove(adresse, struct.pack(\"<Q\", proc))\n"
LA_LIGNE_CORRIGEE = ("        ctypes.memmove(adresse, struct.pack(\"<Q\", proc), 8)\n")


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parite_ast(v2: str, v3: str) -> bool:
    """les vecteurs INTACTS : tout identique sauf lier_feuilles ; dans
    lier_feuilles, UNE SEULE ligne changée — la liaison memmove."""
    m2, m3 = ast.parse(v2), ast.parse(v3)

    def fonctions(module):
        return {n.name: n for n in module.body if isinstance(n, ast.FunctionDef)}

    f2, f3 = fonctions(m2), fonctions(m3)
    if set(f2) != set(f3):
        print("  [PARITÉ] les noms de fonctions divergent")
        return False
    for nom in f2:
        if nom == "lier_feuilles":
            continue
        if ast.dump(f2[nom]) != ast.dump(f3[nom]):
            print(f"  [PARITÉ] {nom} diverge — INTERDIT")
            return False
    # lier_feuilles : le segment source ligne à ligne — UNE seule ligne
    s2 = ast.get_source_segment(v2, f2["lier_feuilles"]).splitlines()
    s3 = ast.get_source_segment(v3, f3["lier_feuilles"]).splitlines()
    if len(s2) != len(s3):
        print(f"  [PARITÉ] lier_feuilles : {len(s2)} lignes contre {len(s3)}")
        return False
    diffs = [(i, a, b) for i, (a, b) in enumerate(zip(s2, s3)) if a != b]
    for i, a, b in diffs:
        print(f"  [PARITÉ] lier_feuilles ligne {i} : {a.strip()[:60]} → "
              f"{b.strip()[:60]}")
    return len(diffs) == 1 and "memmove" in diffs[0][1] and "memmove" in diffs[0][2]


def main() -> int:
    print("=== L'ASSEMBLAGE DU KIT v3 (le correctif du crash nommé) ===")

    # 0. le dossier v3 né des QUATORZE pièces du v2 (les DEUX livres de
    #    l'édition v2 partent — remplacés par leurs éditions v3)
    if KIT3.exists():
        shutil.rmtree(KIT3)
    KIT3.mkdir(parents=True)
    for p in sorted(KIT2.iterdir()):
        if p.is_file():
            shutil.copy2(p, KIT3 / p.name)
    for stale in ("LISEZMOI-RUN-UNITE16-D210-1CLIC-V2.txt",
                  "EMPREINTES-GUI-UNITE16-D210-1CLIC-V2.txt"):
        if (KIT3 / stale).exists():
            (KIT3 / stale).unlink()
    print(f"[KIT3] né du v2 — {len(list(KIT3.iterdir()))} fichiers "
          f"(les DEUX livres v2 partis, leurs éditions v3 suivent)")

    # 1. LE SCÉNARIO CORRIGÉ — UNE SEULE LIGNE, UN SEUL ARGUMENT
    source_v2 = (KIT2 / "scenario-unite16.py").read_text(encoding="utf-8")
    n_fautives = source_v2.count(LA_LIGNE_FAUTIVE)
    if n_fautives != 1:
        print(f"[ÉCHEC] la ligne fautive compte {n_fautives} occurrences — "
              f"le correctif refuse (il attend UNE)")
        return 2
    source_v3 = source_v2.replace(LA_LIGNE_FAUTIVE, LA_LIGNE_CORRIGEE)
    (KIT3 / "scenario-unite16.py").write_text(source_v3, encoding="utf-8",
                                              newline="")
    print(f"[SCÉNARIO] la ligne 269 corrigée : memmove(adresse, pack, 8) — "
          f"UN SEUL argument ajouté, {sha(KIT3 / 'scenario-unite16.py')[:8]}…")
    if not parite_ast(source_v2, source_v3):
        print("[ÉCHEC] la parité AST rompue")
        return 2

    # 2. LA GRAVURE regénérée d'UNE ligne (le scénario)
    gravure_v2 = (KIT2 / "EMPREINTES-KIT-UNITE-04-D210.txt").read_text(
        encoding="utf-8")
    lignes = gravure_v2.splitlines()
    # l'en-tête de révision (les lignes avant « (chaque pièce sha256 ») est
    # remplacé par celui de la RÉVISION 3 ; le corps ne change que la ligne
    # du scénario
    idx_corps = next(i for i, l in enumerate(lignes)
                     if l.startswith("(chaque pièce sha256"))
    entete_v3 = [
        "EMPREINTES — LE KIT DE L'UNITÉ 04 D210, RÉVISION 3 (loupe-16 saisie × bras",
        "T — le correctif du crash nommé : la liaison memmove au TROISIÈME argument",
        "(le compte 8, l'arité des DOUZE autres appels du fichier) ; LES TREIZE",
        "AUTRES PIÈCES INTACTES octet pour octet — la gravure regénérée d'UNE SEULE",
        "ligne, le scénario)",
    ]
    gravure_v3 = entete_v3 + lignes[idx_corps:]
    gravure_v3 = [f"{sha(KIT3 / 'scenario-unite16.py')}"
                  f"  scenario-unite16.py"
                  if l.endswith("  scenario-unite16.py") else l
                  for l in gravure_v3]
    (KIT3 / "EMPREINTES-KIT-UNITE-04-D210.txt").write_text(
        "\n".join(gravure_v3) + "\n", encoding="utf-8", newline="")
    grav_diff = sum(1 for a, b in zip(gravure_v2.splitlines(), gravure_v3)
                    if a != b)
    print(f"[GRAVURE] regénérée — {grav_diff} lignes changées (l'en-tête de "
          f"révision + la ligne du scénario), "
          f"{sha(KIT3 / 'EMPREINTES-KIT-UNITE-04-D210.txt')[:8]}…")

    # 3. LE GUI v2.0.2 — LA CHIRURGIE sur les DEUX empreintes du verrou
    gui_v2 = (KIT2 / "triade_run_unite16_d210_gui.py").read_text(
        encoding="utf-8")
    gui_v3 = gui_v2
    gui_v3 = gui_v3.replace(
        "EN UN CLIC · GUI v2.0.1 · L'ATELIER CHOISI",
        "EN UN CLIC · GUI v2.0.2 · L'ATELIER CHOISI")
    gui_v3 = gui_v3.replace(
        "LA RÉVISION 2.0.1 (le correctif du refus nommé — le run v1 du 18/11\n"
        "12:12 REFUSA fail-closed : « [REFUS] RVA-HOURS-SECTIONS : la RVA 0x0\n"
        "hors des sections — RIEN ne court, le guichet ferme », code 2, 0,2 s,\n"
        "AUCUN fichier modifié) : LA CHIRURGIE NOMMÉE sur les DEUX empreintes\n"
        "gravées du verrou — le scénario CORRIGÉ (le guichet aux CINQ champs,\n"
        "la marche des plages FT — la doctrine D54 — la 4e feuille GetLastError\n"
        "le chemin d'échec de loupe-02 ; les vecteurs INTACTS) et la gravure\n"
        "regénérée d'UNE ligne — LES DOUZE AUTRES PIÈCES INCHANGÉES. Le kit v1\n"
        "demeure au coffre (D143 — le refus du run v1 est un témoin).",
        "LA RÉVISION 2.0.2 (le correctif du crash nommé — le run v2 du 18/11\n"
        "14:09 tomba à la liaison : « TypeError: this function takes at least\n"
        "3 arguments (2 given) », code 1, 0,4 s, T0 VERT, AUCUN fichier\n"
        "modifié) : LA CHIRURGIE NOMMÉE sur les DEUX empreintes gravées du\n"
        "verrou — le scénario CORRIGÉ (la liaison memmove au TROISIÈME\n"
        "argument — le compte 8, l'arité des DOUZE autres appels du fichier ;\n"
        "les vecteurs INTACTS) et la gravure regénérée d'UNE ligne — LES DOUZE\n"
        "AUTRES PIÈCES INCHANGÉES. Les kits v1 et v2 demeurent au coffre\n"
        "(D143 — les dépôts des refus sont des témoins).")
    gui_v3 = gui_v3.replace('VERSION = "2.0.1"', 'VERSION = "2.0.2"')
    gui_v3 = gui_v3.replace(
        '"705951ccba0c25e895818392f21a629bd523d93b1f3709f36bc9b40258d73138"',
        f'"{sha(KIT3 / "scenario-unite16.py")}"')
    gui_v3 = gui_v3.replace(
        '"957f745c54ac6d61adfeac233566a717b72aab480ce6976ba1bc262e16728515"',
        f'"{sha(KIT3 / "EMPREINTES-KIT-UNITE-04-D210.txt")}"')
    gui_v3 = gui_v3.replace(
        '"LE JUGE CORRIGÉ (le guichet aux CINQ champs, la marche des plages "\n'
        '     "FT la doctrine D54, la 4e feuille GetLastError le chemin d\'échec "\n'
        '     "de loupe-02 — les vecteurs INTACTS, l\'épreuve du guichet née au "\n'
        '     "labo : la découverte rejouée contre le fichier livré, TOUT VERT)"),',
        '"LE JUGE CORRIGÉ (la liaison memmove au TROISIÈME argument — le "\n'
        '     "compte 8, l\'arité des DOUZE autres appels du fichier ; les "\n'
        '     "vecteurs INTACTS, l\'épreuve de la liaison née au labo : la "\n'
        '     "plomberie exécutée contre le fichier livré, TOUT VERT)"),')
    gui_v3 = gui_v3.replace(
        '"la gravure du kit RÉVISION 2 (regénérée d\'UNE ligne — le scénario "',
        '"la gravure du kit RÉVISION 3 (regénérée d\'UNE ligne — le scénario "')
    if gui_v3 == gui_v2:
        print("[ÉCHEC] la chirurgie du GUI ne prit aucun des greffons")
        return 2
    (KIT3 / "triade_run_unite16_d210_gui.py").write_text(
        gui_v3, encoding="utf-8", newline="")
    n_changements = sum(1 for a, b in zip(gui_v2.splitlines(),
                                           gui_v3.splitlines()) if a != b)
    print(f"[GUI v2.0.2] la chirurgie portée — {n_changements} lignes "
          f"changées (les DEUX empreintes, la version, l'en-tête)")

    # 4. LE LANCEUR à l'édition correctif v3 (CRLF + BOM conservés)
    bat_v2 = (KIT2 / "LANCER-RUN-UNITE16-D210-1CLIC.bat").read_text(
        encoding="utf-8-sig")
    corps = "rem ====" + bat_v2.split("rem ====", 1)[1]
    entete_v3 = """@echo off
rem ============================================================================
rem LANCER-RUN-UNITE16-D210-1CLIC.bat - LE RUN DE L'UNITE 04 D210 EN UN CLIC
rem [le kit kit-gui-1clic-unite16-d210-v3 - l'edition CORRECTIF 3 du 18/11 :
rem  LE CRASH NOMME du run v2 (« TypeError: this function takes at least
rem  3 arguments (2 given) » a la liaison memmove, code 1) recoupe, la faute
rem  nommee (la liaison a DEUX arguments - le compte 8 manquant, l'arite
rem  contraire des DOUZE autres appels du fichier) ; LES QUATORZE pieces du
rem  kit v3 : les DOUZE INCHANGEES (loupe.exe b382e01b...), le scenario
rem  CORRIGE d'UN SEUL argument, la gravure regeneree d'UNE ligne ; les kits
rem  v1 et v2 DEMEURENT au coffre (D143 - les depots des refus sont des
rem  temoins) ; le dossier racine du zip porte LE NOM DU KIT
rem  (kit-unite-04-d210-20261118-v3 - le pas 1-KIT du livre du kit :
rem  CHOISIR CE DOSSIER ; le double-clic du lanceur EST le choix - le GUI
rem  recoupe LUI-MEME les pieces de CE dossier)]
rem
"""
    bat_v3 = entete_v3 + corps
    (KIT3 / "LANCER-RUN-UNITE16-D210-1CLIC.bat").write_bytes(
        b"\xef\xbb\xbf" + bat_v3.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8"))
    print(f"[LANCER] le lanceur à l'édition correctif v3 "
          f"({(KIT3 / 'LANCER-RUN-UNITE16-D210-1CLIC.bat').stat().st_size} o, CRLF+BOM)")

    # 5. LE LISEZMOI-RUN v3 (le livre du correctif)
    lirez_v3 = KIT3 / "LISEZMOI-RUN-UNITE16-D210-1CLIC-V3.txt"
    lirez_v3.write_text(LISEZMOI, encoding="utf-8", newline="\n")
    print(f"[LISEZMOI-RUN v3] {lirez_v3.stat().st_size} o")

    # 6. LES EMPREINTES-GUI v3
    lignes_emp = []
    lignes_emp.append("EMPREINTES-GUI-UNITE16-D210-1CLIC-V3 — les pièces du kit "
                      "GUI 1-clic CORRECTIF")
    lignes_emp.append("(l'unité 04 D210, la révision 3 — le crash nommé du run "
                      "v2 recoupé, la liaison corrigée ;")
    lignes_emp.append("la console « certutil -hashfile <fichier> SHA256 » "
                      "recoupe chaque ligne chez vous)")
    lignes_emp.append("=" * 78)
    lignes_emp.append("")
    lignes_emp.append("LE GUI ET SES LIVRES :")
    lignes_emp.append("")
    gui = KIT3 / "triade_run_unite16_d210_gui.py"
    lignes_emp.append(f"{gui.name:<50} {gui.stat().st_size:>7} o  sha256 {sha(gui)}")
    lignes_emp.append("le GUI v2.0.2 (LA CHIRURGIE du correctif : les DEUX "
                      "empreintes du verrou — L'ATELIER CHOISI tenu ; le selftest "
                      "27 VERT)")
    lanceur = KIT3 / "LANCER-RUN-UNITE16-D210-1CLIC.bat"
    lignes_emp.append(f"{lanceur.name:<50} {lanceur.stat().st_size:>7} o  "
                      f"sha256 {sha(lanceur)}")
    lignes_emp.append("le lanceur au double-clic (l'édition CORRECTIF v3, CRLF+BOM)")
    lirez = KIT3 / "LISEZMOI-RUN-UNITE16-D210-1CLIC-V3.txt"
    lignes_emp.append(f"{lirez.name:<50} {lirez.stat().st_size:>7} o  sha256 {sha(lirez)}")
    lignes_emp.append("le livre du kit v3 (le correctif nommé, le geste du re-run)")
    note = KIT3 / "NOTE-ATELIER-UNITE16-D210-20261118.txt"
    lignes_emp.append(f"{note.name:<50} {note.stat().st_size:>7} o  sha256 {sha(note)}")
    lignes_emp.append("le commandement verbatim, la frontière M3 (INCHANGÉE — reconduite)")
    lignes_emp.append("")
    lignes_emp.append("LES PIÈCES DU KIT (le verrou du GUI les recoupe à CHAQUE "
                      "lancement, fail-closed) :")
    lignes_emp.append("")
    for p in sorted(KIT3.iterdir()):
        if not p.is_file():
            continue
        if p.name in ("triade_run_unite16_d210_gui.py",
                      "LANCER-RUN-UNITE16-D210-1CLIC.bat",
                      "LISEZMOI-RUN-UNITE16-D210-1CLIC-V3.txt",
                      "NOTE-ATELIER-UNITE16-D210-20261118.txt",
                      "EMPREINTES-GUI-UNITE16-D210-1CLIC-V3.txt"):
            continue
        lignes_emp.append(f"{p.name:<50} {p.stat().st_size:>7} o  sha256 {sha(p)}")
        if p.name == "scenario-unite16.py":
            lignes_emp.append("                                               LE JUGE CORRIGÉ "
                              "(la liaison memmove au TROISIÈME argument,")
            lignes_emp.append("                                               le compte 8 — "
                              "les vecteurs INTACTS)")
    lignes_emp.append("")
    (KIT3 / "EMPREINTES-GUI-UNITE16-D210-1CLIC-V3.txt").write_text(
        "\n".join(lignes_emp) + "\n", encoding="utf-8", newline="\n")
    print(f"[EMPREINTES-GUI v3] "
          f"{(KIT3 / 'EMPREINTES-GUI-UNITE16-D210-1CLIC-V3.txt').stat().st_size} o")

    # 7. LE RECOUP : les pièces inchangées == le kit v2 (et le v1 pour
    #    celles qui y vivent — la NOTE-ATELIER naquit au v2)
    inchangees = inchangees_v1 = 0
    presentes_v1 = 0
    for p in sorted(KIT3.iterdir()):
        if not p.is_file() or p.name in ("scenario-unite16.py",
                                         "EMPREINTES-KIT-UNITE-04-D210.txt",
                                         "LANCER-RUN-UNITE16-D210-1CLIC.bat",
                                         "LISEZMOI-RUN-UNITE16-D210-1CLIC-V3.txt",
                                         "EMPREINTES-GUI-UNITE16-D210-1CLIC-V3.txt",
                                         "triade_run_unite16_d210_gui.py"):
            continue
        if p.read_bytes() != (KIT2 / p.name).read_bytes():
            print(f"[DIVERGE INATTENDU] {p.name}")
            return 2
        inchangees += 1
        if (KIT1 / p.name).exists():
            presentes_v1 += 1
            if p.read_bytes() == (KIT1 / p.name).read_bytes():
                inchangees_v1 += 1
            else:
                print(f"[DIVERGE INATTENDU v1] {p.name}")
                return 2
    print(f"[RECOUP] {inchangees} pièces du kit == le v2 octet pour octet "
          f"(les TREIZE attendues : les DOUZE + la NOTE-ATELIER) ; "
          f"{inchangees_v1}/{presentes_v1} de celles-ci == le v1 aussi")

    # 8. PY_COMPILE + LE SELFTEST du GUI v2.0.2
    py_compile.compile(str(KIT3 / "scenario-unite16.py"), doraise=True)
    py_compile.compile(str(KIT3 / "triade_run_unite16_d210_gui.py"), doraise=True)
    print("[PY_COMPILE] le scénario et le GUI compilés PROPRE")
    r = subprocess.run([sys.executable, str(KIT3 / "triade_run_unite16_d210_gui.py"),
                        "--selftest"], capture_output=True, text=True,
                       cwd=str(KIT3), timeout=600)
    derniere = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "?"
    print(f"[SELFTEST] code {r.returncode} — {derniere}")
    if r.returncode != 0:
        return 2

    # 9. LE ZIP
    zip_path = CAMP / "kit-gui-1clic-unite16-d210-v3-20261118.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(KIT3.iterdir()):
            if p.is_file():
                z.write(p, f"kit-unite-04-d210-20261118-v3/{p.name}")
    n = len(zipfile.ZipFile(zip_path).namelist())
    print(f"[ZIP] {zip_path.name} — {n} entrées, {zip_path.stat().st_size} o")
    return 0


LISEZMOI = """LISEZMOI-RUN-UNITE16-D210-1CLIC-V3 — LE RUN DE L'UNITÉ 04 D210,
RÉVISION 3 (LOUPE-16 SAISIE × BRAS T) EN UN CLIC · L'ATELIER CHOISI PAR
CONSTRUCTION · LE CORRECTIF DU CRASH NOMMÉ
=========================================================================

L'OBJET DE CETTE RÉVISION : le run v2 du 18/11 14:09 tomba à la liaison
(code 1, 0,4 s — T0 VERT, la pièce INTACTE, le guichet découvert, puis) :
« TypeError: this function takes at least 3 arguments (2 given) » à la
ligne 269, LA LIAISON memmove. Le dépôt du crash reçu et reCOUPÉ au labo
(la console, l'état, la session — le crash est AUSSI un témoin, TEL
QUELLE) ; la faute nommée sur pièces : la liaison appelait memmove à
DEUX arguments (dst, src) — le COMPTE manquait. Or CHAQUE autre appel
du fichier (les DOUZE : les memmove des zones, les memset, les poses du
cadre et du journal) porte SES TROIS arguments — la forme du correctif
était déjà là, dans le fichier même ; la ligne fautive était née du
correctif v2 (le bloc de liaison réécrit au guichet), et l'épreuve du
guichet — née le même jour — n'éprouvait que la DÉCOUVERTE : la
plomberie de la liaison n'avait jamais couru au labo. LE CORRECTIF,
D'UN SEUL ARGUMENT : memmove(adresse, struct.pack("<Q", proc), 8) — le
compte 8, l'arité de ses DOUZE frères. LES VECTEURS INTACTS au byte
près (la parité AST : tout identique sauf CE seul appel) ; les DOUZE
autres pièces INCHANGÉES octet pour octet ; la gravure regénérée d'UNE
SEULE ligne (le scénario). L'ÉPREUVE QUI MANQUAIT NÉE :
L'ÉPREUVE DE LA LIAISON — le bloc de liaison EXÉCUTÉ au labo contre
le fichier livré (les gestes Windows neutralisés au contexte seul, le
memmove et la relecture RÉELS) : CONTRE le v2 : ROUGE, le TypeError
RECONSTITUÉ mot pour mot ; CONTRE le v3 : TOUT VERT (les QUATRE
feuilles écrites, relues, l'égalité recoupée). Et l'AUDIT D'ARITÉ :
chaque memmove/memset/string_at du scénario porte son compte.

LE GESTE DU RE-RUN : DÉZIPPEZ CE KIT (kit-unite-04-d210-20261118-v3/,
une extraction FRAÎCHE — jamais le dossier v2 réutilisé) puis
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

AU LIVRE, AU BLOC-NOTS (la chirurgie prescrite — le livre ne ment
jamais : le run v2 a couru) : ① la ligne T-loupe-16-d210-it2 ROUGE (le
kit v2, le run 2026-11-18, le crash nommé, code 1) posée à la main à
livraisons.csv ; ② le défaut à defauts.csv (l'onglet 6·DÉFAUTS : la
classe « liaison-memmove-deux-arguments », le mécanisme « memmove
appelé à DEUX arguments (dst, src) — le compte 8 manquant, contraire à
l'arité des DOUZE autres appels du fichier ; la ligne née du correctif
v2, l'épreuve du guichet n'éprouvait que la découverte », le côté
« kit », la pièce à l'appui
run-console-unite16-d210-20261118-140903.txt, l'exclusion « non — la
faute au kit voyagée jusqu'au terrain, le run consommé, D202 ») ; ③
l'atelier ENTIER re-déposé. Le re-run v3 couchera la ligne
T-loupe-16-d210-it3 au livre DURANT le run.

LA CAP M1 (le plan D204, § 7) : TROIS livraisons par bloc — le v3 EST
la troisième de l'unité 04 (v1, v2, v3) : l'arrêt au premier vert
recoupé, la censure sans exclusion.

LES KITS v1 ET v2 DEMEURENT AU COFFRE (D143 : les dépôts des refus
jamais recouverts — un refus est aussi un témoin).

LES EMPREINTES : EMPREINTES-GUI-UNITE16-D210-1CLIC-V3.txt (le GUI et ses
livres + les QUATORZE pièces du kit, chaque sha256 ; certutil -hashfile
chez vous recoupe).

(18/11/2026, la session du correctif v3 — le crash nommé, l'épreuve de
la liaison née, la plomberie enfin éprouvée au labo)
"""


if __name__ == "__main__":
    sys.exit(main())
