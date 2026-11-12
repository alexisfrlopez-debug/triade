#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""monter_edition_mise_a_jour.py — L'ÉDITION MISE À JOUR DU PAQUET
MULTIMACHINES (le 12/11/2026, troisième geste de la journée — la commande
du développeur : « fais un kit mis à jour avec ce qu'il reste à faire ou
des corrections si nécessaires, ou éventuellement rajouter des tests si tu
trouve ça pertinent »).

Le principe : le paquet AUTOMATISÉ (sha256 814312a5…, l'Entrée 247) est la
SOURCE DE VÉRITÉ — extraction intégrale, puis :
  — DEUX LISEZMOI retouchés PAR INSERTION (l'histoire jamais réécrite ;
    la ligne « 1. » du protocole dudect, amputée par l'édition AUTO, est
    RÉPARÉE — la correction est nommée dans la lettre) ;
  — DEUX lanceurs .bat remplacés (le menu COMMENCER-ICI enrichi du
    diagnostic, du vérificateur et de la feuille de route ; le lanceur
    kit-2 corrigé : l'écart nommé si l'épreuve d'appel manque, le refus
    nommé si le binaire manque, la validation de N durcie) ;
  — QUATRE pièces neuves (CE-QUI-RESTE-A-FAIRE.txt, DIAGNOSTIC-MACHINE.bat,
    diagnostic_machine.py, VERIFIER-PAQUET.bat) ;
  — PUIS le manifeste : EMPREINTES-PAQUET.txt (44 pièces) et
    verifier_paquet.py (le manifeste gravé, 45 pièces — tout sauf lui-même,
    voyez l'honnêteté du cercle dans son en-tête).

L'ÉPREUVE SUR EXTRACTION VIERGE (D153 — le paquet déposé est le paquet
prouvé) : le vérificateur 45/45 VERT, l'ANTI-TEST (un exe retiré et un
octet muté sur une COPIE : l'écart NOMMÉ attendu — l'épreuve que le test
attrape l'antivirus, l'événement du coffre Drive du 12/11), le diagnostic
vécu sur l'hôte Linux x86-64 du labo (le CPUID par stub recoupé à la
seconde voix /proc/cpuinfo), la voie 1 M7D REVÉCUE par son lanceur, le
kit-2 recompilé gcc (l'épreuve d'appel FIPS + l'autotest), le diff
éprouvé/livéré (les 36 pièces intactes attendues octet pour octet, les 4
fichiers d' édition seuls divergents), les CINQ scellés, les .bat CRLF
intégral et ASCII pur. La note d'épreuve jointe : preuves-edition-maj-labo/.
"""

import hashlib
import pathlib
import shutil
import subprocess
import sys
import zipfile

REPO = pathlib.Path("/home/z/my-project/triade")
KIT150 = REPO / "scripts" / "kits_mesure_v150"
ICI = KIT150 / "edition_mise_a_jour"
SOURCES = ICI / "sources"
PAQUET = ICI / "paquet"
PREUVES = ICI / "preuves-edition-maj-labo"

ZIP_AUTO = REPO / "download" / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO.zip"
ZIP_AUTO_SHA = ("814312a5546d1476213948757943d8d33f4f94fe274d464b2bf17d059"
                "2a5562e")
ZIP_MAJ = REPO / "download" / "TRIADE_kits_terrain_v0150_MULTIMACHINES-MISE-A-JOUR.zip"

# --- les textes d'insertion (l'append-only par insertion) ---------------------

BANDEAU_MULTI = """L'ÉDITION MISE À JOUR (le 12/11, troisième geste — la commande : « fais un
kit mis à jour avec ce qu'il reste à faire ou des corrections si
nécessaires, ou éventuellement rajouter des tests si tu trouve ça
pertinent ») : LA FEUILLE DE ROUTE CE-QUI-RESTE-A-FAIRE.txt (l'état exact
du projet au 12/11 soir — le kit-2 dudect JAMAIS ENCORE COURU, le
constat-arm au téléphone, les voies QEMU, le geste B, D204), DEUX TESTS
NEUFS (DIAGNOSTIC-MACHINE.bat : quels kits vivent sur CETTE machine, le
silicium lu par CPUID ; VERIFIER-PAQUET.bat : les 45 pièces de l'extraction
recoupées contre le manifeste du laboratoire — il attrape l'antivirus qui
retirerait un exe, l'événement du coffre Drive du 12/11), et LES CORRECTIONS
nommées (le lanceur du kit-2 : l'écart nommé si l'épreuve d'appel manque,
le refus nommé si le binaire manque, la validation de N durcie ; la ligne
« 1. » du protocole dudect réparée ; le menu enrichi). Les pièces du paquet
AUTOMATISÉ demeurent OCTET POUR OCTET sauf ces quatre fichiers d'édition.
"""

MENTION_DUDECT_ANCIENNE = """  Aucun Python requis. Le protocole ci-dessous demeure la référence.
 (extraire_cibles_v150.py, les
     cibles/ déjà extraites, dudect_v150.c, ce LISEZMOI).
"""

MENTION_DUDECT_NEUVE = """  Aucun Python requis. Le protocole ci-dessous demeure la référence.

  L'ÉDITION MISE À JOUR (le 12/11, troisième geste) corrige le LANCEUR :
  si l'épreuve d'appel (test_appel) manque à l'extraction — l'antivirus
  peut retirer les exe de mesure, le coffre Drive l'a vécu le 12/11 même —
  l'écart est désormais NOMMÉ à l'écran et au témoin (l'édition AUTOMATISÉE
  la sautait en silence) ; si le binaire de mesure manque : REFUS NOMMÉ
  (plus jamais un code 9009 nu) ; la validation de N ne peut plus exécuter
  aucun texte saisi. Et la présente réparation : la ligne « 1. » du
  protocole ci-dessous, amputée par l'insertion de la mention AUTOMATISÉE,
  est remise (la relecture sur pièces, encore). VERIFIER-PAQUET.bat, à la
  racine du paquet, recoupe les 45 pièces de votre extraction AVANT tout
  geste ; DIAGNOSTIC-MACHINE.bat dit quels kits vivent sur votre machine.

  1. Les pièces du kit : extraire_cibles_v150.py, les cibles/ déjà
     extraites, dudect_v150.c, ce LISEZMOI.
"""


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ok(msg: str) -> None:
    print("[montage] " + msg)


def refus(msg: str) -> None:
    sys.exit("[montage] REFUS : " + msg)


# --- 1. LA SOURCE DE VÉRITÉ RECoupÉE -----------------------------------------

def extraire_auto():
    if not ZIP_AUTO.exists():
        refus("le paquet AUTO est absent : %s" % ZIP_AUTO)
    if sha(ZIP_AUTO) != ZIP_AUTO_SHA:
        refus("le paquet AUTO diverge de son empreinte consignée")
    ok("le paquet AUTO recoupé (%s…, %d o)" % (ZIP_AUTO_SHA[:12],
                                                ZIP_AUTO.stat().st_size))
    if PAQUET.exists():
        shutil.rmtree(PAQUET)
    PAQUET.mkdir(parents=True)
    with zipfile.ZipFile(ZIP_AUTO) as z:
        z.extractall(PAQUET)
    n = sum(1 for p in PAQUET.rglob("*") if p.is_file())
    if n != 40:
        refus("l'extraction AUTO ne porte pas 40 pièces (%d)" % n)
    ok("l'extraction AUTO : 40 pièces")


# --- 2. LES RETOUCHES PAR INSERTION ------------------------------------------

def retoucher_lisezmoi():
    # (a) la carte maîtresse : le bandeau de l'édition, inséré SOUS le titre
    multi = PAQUET / "LISEZMOI-MULTIMACHINES.txt"
    texte = multi.read_text(encoding="utf-8")
    if "L'ÉDITION MISE À JOUR" in texte:
        refus("LISEZMOI-MULTIMACHINES : le bandeau existe déjà (rejeu ?)")
    lignes = texte.split("\n")
    # lignes[0] = titre, lignes[1] = =====, lignes[2] = vide
    if not lignes[1].startswith("====") or lignes[2].strip() != "":
        refus("LISEZMOI-MULTIMACHINES : la tête du texte ne correspond pas")
    lignes.insert(3, BANDEAU_MULTI)
    multi.write_text("\n".join(lignes), encoding="utf-8")
    ok("LISEZMOI-MULTIMACHINES : le bandeau MISE À JOUR inséré (%d lignes)"
       % len(BANDEAU_MULTI.split("\n")))

    # (b) le LISEZMOI-dudect : la ligne « 1. » réparée + la mention
    dud = PAQUET / "pc-windows" / "kit-2-dudect" / "LISEZMOI-dudect.txt"
    texte = dud.read_text(encoding="utf-8")
    if "L'ÉDITION MISE À JOUR" in texte:
        refus("LISEZMOI-dudect : la mention existe déjà (rejeu ?)")
    if MENTION_DUDECT_ANCIENNE not in texte:
        refus("LISEZMOI-dudect : la ligne amputée attendue est introuvable")
    texte = texte.replace(MENTION_DUDECT_ANCIENNE, MENTION_DUDECT_NEUVE)
    dud.write_text(texte, encoding="utf-8")
    ok("LISEZMOI-dudect : la ligne « 1. » réparée + la mention insérée")


# --- 3. LES LANCEURS REMPLACÉS ET LES PIÈCES NEUVES --------------------------

def poser_les_pieces():
    # les .bat : conversion LF -> CRLF (la forme canonique de cmd.exe),
    # ASCII pur exigé
    remplacements = {
        SOURCES / "COMMENCER-ICI.bat":
            PAQUET / "COMMENCER-ICI.bat",
        SOURCES / "LANCER-KIT-2-DUDECT.bat":
            PAQUET / "pc-windows" / "kit-2-dudect" / "LANCER-KIT-2-DUDECT.bat",
        SOURCES / "DIAGNOSTIC-MACHINE.bat":
            PAQUET / "DIAGNOSTIC-MACHINE.bat",
        SOURCES / "VERIFIER-PAQUET.bat":
            PAQUET / "VERIFIER-PAQUET.bat",
    }
    for src, dst in remplacements.items():
        brut = src.read_bytes()
        try:
            brut.decode("ascii")
        except UnicodeDecodeError as e:
            refus("%s : de l'ASCII pur est exigé (%s)" % (src.name, e))
        if b"\r\n" in brut:
            refus("%s : la source doit vivre en LF (la conversion est ici)"
                  % src.name)
        dst.write_bytes(brut.replace(b"\n", b"\r\n"))
        ok("%s : posé (%d o, CRLF, ASCII pur)" % (dst.name, dst.stat().st_size))

    # les .txt / .py : copie telle quelle (UTF-8, LF — la forme des
    # LISEZMOI livrés)
    for src, dst in [
        (SOURCES / "CE-QUI-RESTE-A-FAIRE.txt", PAQUET / "CE-QUI-RESTE-A-FAIRE.txt"),
        (SOURCES / "diagnostic_machine.py", PAQUET / "diagnostic_machine.py"),
    ]:
        shutil.copyfile(src, dst)
        ok("%s : posé (%d o)" % (dst.name, dst.stat().st_size))


# --- 4. LE MANIFESTE ----------------------------------------------------------

def generer_manifeste():
    pieces = sorted(
        str(p.relative_to(PAQUET)).replace("\\", "/")
        for p in PAQUET.rglob("*") if p.is_file())
    attendu = 44
    if len(pieces) != attendu:
        refus("le montage porte %d pièces, %d attendues avant manifeste"
              % (len(pieces), attendu))

    empreintes = {p: sha(PAQUET / p) for p in pieces}

    # (a) EMPREINTES-PAQUET.txt : les 44, la voix lisible à la main
    lignes = [
        "EMPREINTES-PAQUET.txt — LES %d PIÈCES DU PAQUET MISE À JOUR"
        % len(pieces),
        "(12/11/2026, l'édition MISE À JOUR — la feuille de route vit dans"
        " CE-QUI-RESTE-A-FAIRE.txt)",
        "=" * 78,
        "",
        "Généré au LABORATOIRE depuis le montage même du paquet : chaque",
        "pièce telle qu'elle vit dans le zip livré (les .bat en CRLF, leur",
        "forme canonique). Les CINQ pièces scellées y sont : loupe.exe,",
        "proxy-image.bin (l'image étendue), moteur-shani.bin, corpus et",
        "demo du kit M7D.",
        "",
        "L'HONNÊTETÉ DU PRESENT FICHIER : il couvre les %d pièces — tout"
        % len(pieces),
        "sauf lui-même et le vérificateur verifier_paquet.py : un fichier",
        "ne peut pas sceller sa propre empreinte sans cercle. Les",
        "empreintes du présent fichier et du vérificateur sont rendues par",
        "le sha256 du zip ENTIER, consigné à l'Entrée 249 du journal de",
        "travail et au coffre /test.",
        "",
        "sha256                                                            pièce",
        "-" * 64 + "  " + "-" * 30,
    ]
    for p in pieces:
        lignes.append("%s  %s" % (empreintes[p], p))
    lignes += [
        "",
        "LA VOIX AUTOMATIQUE : double-cliquez VERIFIER-PAQUET.bat (ou",
        "python verifier_paquet.py) — les 45 pièces sont recoupées sans",
        "aucun geste, chaque écart est nommé.",
    ]
    (PAQUET / "EMPREINTES-PAQUET.txt").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8")
    ok("EMPREINTES-PAQUET.txt : %d empreintes" % len(pieces))

    # (b) verifier_paquet.py : le manifeste gravé (45 = 44 + EMPREINTES)
    empreintes["EMPREINTES-PAQUET.txt"] = sha(PAQUET / "EMPREINTES-PAQUET.txt")
    gabarit = (SOURCES / "verifier_paquet.gabarit.py").read_text(
        encoding="utf-8")
    if "__MANIFESTE__" not in gabarit:
        refus("le gabarit du vérificateur ne porte pas sa marque")
    manifeste = " {\n" + "\n".join(
        "    %r: %r," % (k, empreintes[k]) for k in sorted(empreintes)
    ) + "\n}"
    manifeste = manifeste.replace("\\\\", "\\")
    texte = gabarit.replace("__MANIFESTE__", manifeste)
    texte = texte.replace("__EDITION__", "12/11/2026, troisième geste")
    (PAQUET / "verifier_paquet.py").write_text(texte, encoding="utf-8")
    ok("verifier_paquet.py : le manifeste gravé (%d pièces)"
       % len(empreintes))

    # la py_compile du vérificateur et du diagnostic (aucune pièce livrée
    # qui ne compile pas) — le __pycache__ né du contrôle est DÉTRUIT :
    # il n'est PAS une pièce du paquet
    for nom in ("verifier_paquet.py", "diagnostic_machine.py"):
        r = subprocess.run([sys.executable, "-m", "py_compile",
                            str(PAQUET / nom)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            refus("%s ne compile pas : %s" % (nom, r.stderr))
    shutil.rmtree(PAQUET / "__pycache__", ignore_errors=True)
    ok("les deux .py livrés compilent (py_compile, le cache détruit)")


# --- 5. LES CONTRÔLES DE FORME ------------------------------------------------

def controler_la_forme():
    nb = sum(1 for p in PAQUET.rglob("*") if p.is_file())
    if nb != 46:
        refus("le montage porte %d pièces, 46 attendues" % nb)
    for p in PAQUET.rglob("*.bat"):
        brut = p.read_bytes()
        try:
            brut.decode("ascii")
        except UnicodeDecodeError:
            refus("%s : de l'ASCII pur est exigé" % p)
        if b"\r\n" not in brut:
            refus("%s : le CRLF est exigé" % p)
        if brut.replace(b"\r\n", b"").find(b"\n") >= 0:
            refus("%s : un LF solitaire vit dans le fichier" % p)
    ok("la forme : 46 pièces, les .bat TOUS CRLF intégral et ASCII pur")

    # les cinq scellés, nommément
    scelles = {
        "pc-windows/kit-1-shani/moteur-shani.bin":
            "761ab194d88d527c653111a41324b0bb3e9247b1c56ba8dc9fedeeccbe04bcec",
        "pc-windows/kit-2-dudect/cibles/proxy-image.bin":
            "0782d7e20d0bd4a268e6ec7ed0dc1453a0f42d7e72b784c2acc9ed423a885dff",
        "pc-windows/kit-3-terrain-tiers-loupe/loupe-kit-13/loupe.exe":
            "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1",
        "qemu-wsl2/kit-m7d/corpus":
            "ec343b4e8bebf21c8b29a6da1a5eb022fb7b8e4b50ce95c5906734ef0b043799",
        "qemu-wsl2/kit-m7d/demo":
            "e57fc74be2ea67ab4c05351d0b5e0b93b6147ec34f2fb7aabbfd1ab7f141cde9",
    }
    for piece, attendu in scelles.items():
        if sha(PAQUET / piece) != attendu:
            refus("le scellé a bougé : %s" % piece)
    ok("les CINQ scellés recoupés INTACTS")


# --- 6. L'ASSEMBLAGE ----------------------------------------------------------

def assembler():
    if ZIP_MAJ.exists():
        ZIP_MAJ.unlink()
    pieces = sorted(p for p in PAQUET.rglob("*") if p.is_file())
    with zipfile.ZipFile(ZIP_MAJ, "w", zipfile.ZIP_DEFLATED) as z:
        for p in pieces:
            nom = str(p.relative_to(PAQUET)).replace("\\", "/")
            mode = 0o755 if nom.endswith(".sh") else 0o644
            info = zipfile.ZipInfo(nom, date_time=(2026, 11, 12, 14, 0, 0))
            info.external_attr = (mode | 0o100000) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())
    taille = ZIP_MAJ.stat().st_size
    ok("LE ZIP ASSEMBLÉ : %s (%d o, sha256 %s…)"
       % (ZIP_MAJ.name, taille, sha(ZIP_MAJ)[:12]))
    return taille


# --- 7. L'ÉPREUVE SUR EXTRACTION VIERGE (D153) --------------------------------

def epreuve_sur_extraction_vierge():
    extrait = pathlib.Path("/tmp/epreuve-maj")
    if extrait.exists():
        shutil.rmtree(extrait)
    extrait.mkdir(parents=True)
    with zipfile.ZipFile(ZIP_MAJ) as z:
        z.extractall(extrait)
    ok("l'extraction vierge : %d pièces" % sum(
        1 for p in extrait.rglob("*") if p.is_file()))

    journal = []

    def consigner(titre, rc, sortie):
        journal.append("### %s — code %d\n\n```\n%s\n```\n"
                       % (titre, rc, sortie.strip()[-4000:]))

    # (a) LE VÉRIFICATEUR : 45/45 VERT attendu
    r = subprocess.run([sys.executable, "verifier_paquet.py"],
                       cwd=extrait, capture_output=True, text=True)
    consigner("LE VÉRIFICATEUR (python3 verifier_paquet.py)", r.returncode,
              r.stdout + r.stderr)
    if r.returncode != 0 or "45/45" not in r.stdout:
        refus("le vérificateur n'est pas 45/45 VERT (code %d)" % r.returncode)
    ok("l'épreuve (a) : le VÉRIFICATEUR 45/45 VERT, code 0")

    # (b) L'ANTI-TEST : l'exe retiré + l'octet muté sur une COPIE — les
    # écarts NOMMÉS attendus (l'épreuve que le test attrape l'antivirus)
    copie = pathlib.Path("/tmp/epreuve-maj-anti")
    if copie.exists():
        shutil.rmtree(copie)
    shutil.copytree(extrait, copie)
    (copie / "pc-windows" / "kit-2-dudect" / "test_appel.exe").unlink()
    piece = copie / "pc-windows" / "kit-1-shani" / "moteur-shani.bin"
    brut = bytearray(piece.read_bytes())
    brut[0] ^= 0x01
    piece.write_bytes(bytes(brut))
    r = subprocess.run([sys.executable, "verifier_paquet.py"],
                       cwd=copie, capture_output=True, text=True)
    consigner("L'ANTI-TEST (test_appel.exe RETIRÉ + moteur-shani.bin MUTÉ "
              "sur une COPIE)", r.returncode, r.stdout + r.stderr)
    if r.returncode != 1:
        refus("l'anti-test : le code 1 était attendu (code %d)" % r.returncode)
    if "test_appel.exe" not in r.stdout or "ABSENTE" not in r.stdout:
        refus("l'anti-test : l'exe retiré n'est pas nommé")
    if "moteur-shani.bin" not in r.stdout or "DIVERGENTE" not in r.stdout:
        refus("l'anti-test : la pièce mutée n'est pas nommée")
    shutil.rmtree(copie)
    ok("l'épreuve (b) : l'ANTI-TEST rend les DEUX écarts nommés, code 1")

    # (c) LE DIAGNOSTIC sur l'hôte Linux x86-64 du labo (le CPUID par stub
    # recoupé à la seconde voix /proc/cpuinfo)
    r = subprocess.run([sys.executable, "diagnostic_machine.py"],
                       cwd=extrait, capture_output=True, text=True)
    consigner("LE DIAGNOSTIC (python3 diagnostic_machine.py, hôte labo)",
              r.returncode, r.stdout + r.stderr)
    if r.returncode != 0:
        refus("le diagnostic n'a pas vécu (code %d)" % r.returncode)
    for attendu in ("[machine]", "[silicium]", "2e voix", "VERDICT"):
        if attendu not in r.stdout:
            refus("le diagnostic ne rend pas %r" % attendu)
    ok("l'épreuve (c) : le DIAGNOSTIC vécu sur l'hôte labo "
       "(la double voix CPUID/cpuinfo rendue)")

    # (d) LA VOIE 1 M7D revécue par son lanceur (le qemu embarqué)
    r = subprocess.run(["bash", "lancer-voie1-m7d.sh"],
                       cwd=extrait / "qemu-wsl2", capture_output=True,
                       text=True, timeout=600)
    consigner("LA VOIE 1 M7D (bash lancer-voie1-m7d.sh, extraction vierge)",
              r.returncode, r.stdout + r.stderr)
    if r.returncode != 0 or "16 PASS" not in (r.stdout + r.stderr):
        refus("la voie 1 M7D n'est pas VERT 16 PASS (code %d)" % r.returncode)
    ok("l'épreuve (d) : LA VOIE 1 M7D revécue VERT (16 PASS, code 0)")

    # (e) LE KIT-2 recompilé depuis la source de l'extrait : l'épreuve
    # d'appel FIPS + l'autotest du mesureur
    kit2 = extrait / "pc-windows" / "kit-2-dudect"
    run = kit2 / "run-epreuve"
    run.mkdir()
    r1 = subprocess.run(["gcc", "-O2", "-o",
                         str(run / "test_appel"), "test_appel.c"],
                        cwd=kit2, capture_output=True, text=True)
    r2 = subprocess.run(["gcc", "-O2", "-o",
                         str(run / "dudect_v150"), "dudect_v150.c", "-lm"],
                        cwd=kit2, capture_output=True, text=True)
    if r1.returncode != 0 or r2.returncode != 0:
        consigner("LE KIT-2 (gcc -O2)", 1, r1.stderr + r2.stderr)
        refus("la recompilation gcc du kit-2 a échoué")
    ra = subprocess.run([str(run / "test_appel"), "cibles/proxy-image.bin"],
                        cwd=kit2, capture_output=True, text=True)
    rb = subprocess.run([str(run / "dudect_v150"), "--autotest"],
                        cwd=kit2, capture_output=True, text=True)
    consigner("LE KIT-2 RECOMPILÉ (gcc -O2 : test_appel FIPS + "
              "dudect --autotest)", ra.returncode + rb.returncode,
              ra.stdout + ra.stderr + "\n" + rb.stdout + rb.stderr)
    if ra.returncode != 0 or "EXACT" not in ra.stdout:
        refus("l'épreuve d'appel FIPS du kit-2 n'est pas VERT")
    if rb.returncode != 0:
        refus("l'autotest dudect du kit-2 n'est pas VERT (code %d)"
              % rb.returncode)
    ok("l'épreuve (e) : le KIT-2 recompilé gcc — FIPS EXACT, autotest VERT")

    # (f) LE DIFF éprouvé/livré : les 36 pièces AUTO intactes octet pour
    # octet, les 4 fichiers d'édition seuls divergents
    auto = pathlib.Path("/tmp/epreuve-maj-auto")
    if auto.exists():
        shutil.rmtree(auto)
    auto.mkdir(parents=True)
    with zipfile.ZipFile(ZIP_AUTO) as z:
        z.extractall(auto)
    modifiees = {
        "COMMENCER-ICI.bat", "LISEZMOI-MULTIMACHINES.txt",
        "pc-windows/kit-2-dudect/LANCER-KIT-2-DUDECT.bat",
        "pc-windows/kit-2-dudect/LISEZMOI-dudect.txt",
    }
    divergentes = []
    for p in auto.rglob("*"):
        if not p.is_file():
            continue
        nom = str(p.relative_to(auto)).replace("\\", "/")
        if p.read_bytes() != (PAQUET / nom).read_bytes():
            divergentes.append(nom)
    if set(divergentes) != modifiees:
        refus("le diff éprouvé/livré est inattendu : %s" % divergentes)
    ok("l'épreuve (f) : LE DIFF — 36/40 pièces AUTO identiques octet pour"
       " octet, les 4 fichiers d'édition seuls divergents (nommés)")

    # (g) LA NOTE D'ÉPREUVE
    if PREUVES.exists():
        shutil.rmtree(PREUVES)
    PREUVES.mkdir(parents=True)
    horodatage = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                                capture_output=True, text=True).stdout.strip()
    note = [
        "NOTE D'ÉPREUVE — L'ÉDITION MISE À JOUR DU PAQUET MULTIMACHINES",
        "(l'épreuve sur extraction vierge, D153 — %s ; la commande : « fais"
        % horodatage,
        "un kit mis à jour avec ce qu'il reste à faire ou des corrections si",
        "nécessaires, ou éventuellement rajouter des tests si tu trouve ça",
        "pertinent »)",
        "",
        "Le zip éprouvé : TRIADE_kits_terrain_v0150_MULTIMACHINES-"
        "MISE-A-JOUR.zip",
        "(%d o, sha256 %s…) — EXTRACTION VIERGE dans /tmp/epreuve-maj avant"
        % (ZIP_MAJ.stat().st_size, sha(ZIP_MAJ)),
        "toute épreuve ; la source de vérité : le paquet AUTO 814312a5…"
        " recoupé",
        "avant le montage ; les CINQ scellés recoupés INTACTS au montage.",
        "",
        "LES SIX ÉPREUVES :",
        "  (a) LE VÉRIFICATEUR 45/45 pièces VERTES, code 0 — le manifeste"
        " gravé",
        "      recoupe l'extraction entière (y compris EMPREINTES-PAQUET.txt"
        " et",
        "      les exe : l'attrapage antivirus est le dessein même du test) ;",
        "  (b) L'ANTI-TEST : sur une COPIE, test_appel.exe RETIRÉ et un",
        "      octet de moteur-shani.bin MUTÉ — le vérificateur rend les",
        "      DEUX écarts NOMMÉS (ABSENTE / DIVERGENTE), code 1 — le test",
        "      attrape bien ce qu'il prétend attraper ;",
        "  (c) LE DIAGNOSTIC vécu sur l'hôte Linux x86-64 du labo : la",
        "      machine nommée, le CPUID lu par le stub (fabricant, famille,",
        "      modèle, pas, SHA-NI) RECoupÉ à la seconde voix /proc/cpuinfo,",
        "      le verdict rendu (hôte non-Windows : l'honnêteté le dit) ;",
        "  (d) LA VOIE 1 M7D REVÉCUE par son lanceur sur l'extraction :",
        "      16 PASS / 0 ÉCHEC, VERT, code 0, les preuves nées seules ;",
        "  (e) LE KIT-2 RECOMPILÉ depuis la source de l'extrait (gcc -O2) :",
        "      l'épreuve d'appel FIPS « abc » EXACT, mutation K DIVERGE,",
        "      restauration EXACT ; dudect_v150 --autotest VERT code 0 ;",
        "  (f) LE DIFF éprouvé/livré : les 36 pièces du paquet AUTO restées",
        "      OCTET POUR OCTET identiques, les 4 fichiers d'édition seuls",
        "      divergents (COMMENCER-ICI.bat, LISEZMOI-MULTIMACHINES.txt,",
        "      le lanceur et le LISEZMOI du kit-2) — les .sh, les scénarios,",
        "      les scellés et les sources C : INTACTS.",
        "",
        "LA FORME (constatée au montage, avant l'assemblage) : 46 pièces au",
        "total, les .bat TOUS CRLF intégral et ASCII pur (assertion au",
        "montage), les .sh exécutables (mode 755 posé au zip), les CINQ",
        "scellés recoupés INTACTS.",
        "",
        "L'HONNÊTETÉ : le labo n'a AUCUN Windows — les .bat neufs et",
        "corrigés y sont éprouvés par leurs commandes (certutil, findstr,",
        "for /f, where, powershell — toutes standard de Windows 10/11) et",
        "par la relecture, JAMAIS par l'exécution ; le premier double-clic",
        "se vit chez le développeur (si un écran nomme un défaut, le .txt",
        "renvoyé tel quel, D122). Les épreuves (c)-(e) vécurent sur l'hôte",
        "Linux x86-64 du laboratoire — leurs sorties intégrales vivent",
        "ci-dessous.",
        "",
    ]
    (PREUVES / "NOTE-D-EPREUVE.txt").write_text(
        "\n".join(note) + "\n\n" + "\n".join(journal), encoding="utf-8")
    ok("la note d'épreuve : %s" % (PREUVES / "NOTE-D-EPREUVE.txt"))
    # les preuves brutes des épreuves (d) et (e) au dépôt aussi
    for nom, dossier in [
        ("voie1-m7d", extrait / "qemu-wsl2" / "kit-m7d" / "preuves-m7"),
    ]:
        if dossier.is_dir():
            dst = PREUVES / nom
            shutil.copytree(dossier, dst)
            ok("les preuves de l'épreuve copiées : %s" % nom)


def main():
    extraire_auto()
    retoucher_lisezmoi()
    poser_les_pieces()
    generer_manifeste()
    controler_la_forme()
    assembler()
    epreuve_sur_extraction_vierge()
    print()
    ok("L'ÉDITION MISE À JOUR EST MONTÉE ET ÉPROUVÉE :")
    ok("  le zip    : %s" % ZIP_MAJ)
    ok("  la taille : %d o" % ZIP_MAJ.stat().st_size)
    ok("  le sha256 : %s" % sha(ZIP_MAJ))
    ok("  les preuves : %s" % PREUVES)
    return 0


if __name__ == "__main__":
    sys.exit(main())
