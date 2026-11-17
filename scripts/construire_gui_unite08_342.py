#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_gui_unite08_342.py — LA CONSTRUCTION DU GUI 1-CLIC DE
L'UNITÉ 02 D210 (loupe-08 ligne × bras T — l'Entrée 342, la suite ①
annoncée à la 341 : le GUI 1-clic de l'unité au commandement, le
précédent de la 337) :

  1. LE KIT REÇU : les QUATORZE pièces du kit-unite-02-d210-20261118 du
     bac unite-08-T-d210/ copiées byte-byte au dossier GUI
     TRIADE_gui_unite08_d210_v1/, chaque sha256 recoupé AVANT (la
     gravure du kit fait foi) et APRÈS (INTACT) ;
  2. LE GUI SOURCE : triade_run_unite08_d210_gui.py — le source v2 du
     précédent 339 (la logique B-E INCHANGÉE — un seul fichier tkinter)
     porté à l'unité loupe-08 par la chirurgie NOMMÉE : l'en-tête
     (docstring) et LA SECTION A (les constantes du kit) REMPLACÉS, les
     références unitaires (console, DEPOT, zip, selftest, onglets)
     transposées unite02 → unite08, CHAQUE remplacement compté et
     affirmé (un assert par geste) ;
  3. LE LANCEUR : LANCER-RUN-UNITE08-D210-1CLIC.bat (CRLF, ASCII — le
     précédent 337) ;
  4. LE LIVRE : LISEZMOI-RUN-UNITE08-D210-1CLIC.txt.

L'EMPREINTES-GUI (la gravure du kit GUI) naît APRES les épreuves
(empreintes_gui_unite08_342.py — tout recalculé des octets finaux)."""
import hashlib
import pathlib
import py_compile
import shutil
import sys

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
BAC_KIT = (REPO / "scripts" / "campagne_d204" / "unite-08-T-d210"
           / "kit" / "kit-unite-02-d210-20261118")
BASE_V2 = (REPO / "download" / "TRIADE_gui_unite02_d210_v2"
           / "triade_run_unite02_d210_gui.py")
STAGING = pathlib.Path("/home/z/my-project/download"
                       "/TRIADE_gui_unite08_d210_v1")
GUI_PY = STAGING / "triade_run_unite08_d210_gui.py"
BAT = STAGING / "LANCER-RUN-UNITE08-D210-1CLIC.bat"
LISEZMOI = STAGING / "LISEZMOI-RUN-UNITE08-D210-1CLIC.txt"


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# 1· LE KIT REÇU — les QUATORZE pièces, recoupées avant/après
# ---------------------------------------------------------------------------
GRAVURE = "EMPREINTES-KIT-UNITE-02-D210.txt"


def recevoir_le_kit():
    grav = BAC_KIT / GRAVURE
    attendus = {}
    for ligne in grav.read_text(encoding="utf-8").splitlines():
        parts = ligne.strip().split(None, 2)
        if len(parts) >= 2 and len(parts[0]) == 64:
            attendus[parts[1]] = parts[0].lower()
    STAGING.mkdir(parents=True, exist_ok=True)
    for p in (STAGING / "etat-run-unite08-d210.json",
              STAGING / "TRIADE_logs"):
        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            p.unlink()
    pieces = sorted(p.name for p in BAC_KIT.iterdir() if p.is_file())
    assert len(pieces) == 14, f"le bac porte {len(pieces)} pièces, 14 attendues"
    verts = 0
    for nom in pieces:
        src, dst = BAC_KIT / nom, STAGING / nom
        avant = sha256f(src)
        if nom in attendus:
            assert avant == attendus[nom], f"{nom} : écart à la gravure"
        shutil.copyfile(src, dst)
        assert sha256f(dst) == avant, f"{nom} : la copie a muté"
        if nom in attendus:
            verts += 1
        print(f"[kit] {nom:<42} {avant[:12]}… "
              f"{'(gravé)' if nom in attendus else '(le livre)'}")
    print(f"[kit] {len(pieces)} pièces reçues, {verts}/13 recoupées à la "
          f"gravure — le kit INTACT")
    return sha256f(grav)


# ---------------------------------------------------------------------------
# 2· LE GUI SOURCE — la chirurgie nommée du v2 → loupe-08
# ---------------------------------------------------------------------------
DOCSTRING = '''"""
triade_run_unite08_d210_gui.py — TRIADE · LE RUN DE L'UNITÉ 02 D210
(LOUPE-08 LIGNE × BRAS T) EN UN CLIC · GUI v1.0.0
=========================================================================
L'ÉDITION v1 DU 18/11/2026 — LA DEUXIÈME UNITÉ DE LA CAMPAGNE D210 (la
suite ① annoncée à l'Entrée 341 : le GUI 1-clic de l'unité au
commandement, le précédent de la 337 ; loupe-08 ligne × bras T — la
séquence tirée de la graine D217, jamais re-tirée). Le kit
kit-unite-02-d210-20261118 né au labo à la Task 208 : LA PIÈCE
loupe.exe (127 488 o, 41660a30… — le slot loupe-08 RVA 0x49C0, 320 o,
porte la notation de campagne : 260 o cristallisés, sha256 4498b7fa…,
le différentiel au scellé CONFINÉ au slot [0x3bc0, 0x3d00) + la porte
R10, 9 plages 267 o), LE JUGE scenario-unite08.py D204 INCHANGÉ
(44384f5d…, la version corrigée — celle du kit-v2 de l'unité 4 : la
faute au juge nommée à la 338 ne se reproduit pas), LA GRAVURE
EMPREINTES-KIT-UNITE-02-D210.txt NÉE PARSÉE (« sha256  nom » — le
format que le scénario scellé lit : le défaut T0 de l'unité 01 [la
gravure « nom en tête », ZÉRO pièce vue] ne se reproduit pas non plus,
NOMMÉ PARCE QU'IL NE SE REPRODUIT PAS — D202 : les défauts se nomment,
l'absence de défaut aussi).
UN SEUL FICHIER PYTHON, ZÉRO LIGNE DE COMMANDE (si ce n'est le lancer) —
le GUI AUTONOME qui conduit, D'UN SEUL CLIC, LE GESTE TERRAIN de la
deuxième unité de la campagne D210 (le LISEZMOI-KIT-UNITE-02-D210 du kit
fait foi ; l'ordre de jeu : 1·KIT → 2·RUN → 3·TÉMOIN) :

    TOUT LANCER — LE VERROU des QUATORZE pièces du kit (fail-closed :
    une divergence, RIEN ne court), LA PREUVE T0 (le scénario scellé
    voit les TREIZE pièces de la gravure — loupe.exe recoupé à la
    gravure du kit), LE RUN au scenario-unite08.py (SA console, écrite
    AU FIL DE L'EAU, UTF-8 des deux côtés du tuyau — PYTHONIOENCODING
    posé par le GUI), les verdicts RECOPIÉS des lignes de console
    (jamais recalculés), le chrono M4 du run (mesuré, jamais une
    analyse), LA COLLECTE (la console COPIÉE au réceptacle
    preuves-unite08/, le DEPOT-d210-unite08.txt assemblé), et LE GUIDE
    DE RENVOI — dater et signer le témoin DE VOTRE MAIN (D99),
    renvoyer le dossier ENTIER au coffre /test.

    l'assemblage du zip preuves-unite08-d210-<UTC>.zip EXIGE le témoin
    DATÉ ET SIGNÉ (D99 tenu par construction) et refuse au-delà de la
    cap M1 (TROIS livraisons par bloc, la règle § 7 du plan D204).

LE JUGE DE CE KIT (l'attendu du run, recopié du contrat loupe-08:R1) :
T0 la pièce recoupée ; V1 le doré (la première ligne du proxy.exe
scellé + la ligne finale incomplète du témoin 3f) ; V2 le
différentiel (10 000 lignes == le modèle, la graine 20261115 — les
mêmes tirages au labo et au terrain) et EXACTEMENT 77 o (le poison
au-delà demeure — I2 : jamais un de plus) ; V3 les QUATRE rejets -5
(la sortie poison intacte) ; V4 la falsification (l'octet muté
diverge) — L'ATTENDU : 10 VERT, 0 ROUGE, code retour 0.

CE QUE CE GUI NE FERA JAMAIS (les frontières, tenues par construction) :
    — DATER ni SIGNER le témoin (votre main, toujours — D99) ; le
      témoin naît DU SCÉNARIO, le GUI le lit et le RECOPIE, il ne
      touche JAMAIS à ses octets ;
    — DÉPOSER au coffre (il OUVRIRA le /test au navigateur, il
      n'écrit JAMAIS au Drive) ;
    — FABRIQUER un chiffre (les verdicts sont RECOPIÉS des lignes de
      console ; le compte VERT/ROUGE est un recomptage des lignes
      couchées, jamais une réévaluation) ;
    — TOUCHER les pièces scellées (le scénario, loupe.exe, proxy.exe,
      les témoins : LUS ; le scénario lui-même recoupe loupe.exe AVANT
      de courir — le moindre écart = [T0] REFUS, RIEN ne court) ;
    — RENOMMER ni ÉDITER les pièces du réceptacle (temoin-unite08.txt,
      les consoles : COPIÉES, jamais retouchées) ;
    — DÉPASSER la cap M1 (TROIS livraisons par bloc — l'assemblage du
      zip refuse au-delà, le refus est NOMMÉ).

Lancement :
    double-cliquez LANCER-RUN-UNITE08-D210-1CLIC.bat  (le kit complet), ou :
    python triade_run_unite08_d210_gui.py [--selftest]
"""

'''

SECTION_A = '''VERSION = "1.0.0"
EDITION = ("l'édition v1 du 18/11/2026 — LA DEUXIÈME UNITÉ D210 "
           "(loupe-08 ligne × bras T, la séquence tirée de la graine "
           "D217 — jamais re-tirée ; le kit né au labo à l'Entrée 341, "
           "le juge scenario-unite08.py D204 INCHANGÉ 44384f5d… [la "
           "version corrigée], la gravure NÉE PARSÉE — le défaut T0 de "
           "l'unité 01 ne se reproduit pas)")

GUI_DIR = pathlib.Path(__file__).resolve().parent
FICHIER_ETAT = GUI_DIR / "etat-run-unite08-d210.json"
DOSSIER_LOGS = GUI_DIR / "TRIADE_logs"

# le coffre — le dossier /test du Drive « Triade »
COFFRE_TEST_URL = ("https://drive.google.com/drive/folders/"
                   "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0")

NOM_RUN = "l'unité 02 D210 (loupe-08 ligne × bras T)"

# LES PIÈCES DU KIT — sha256 gravées (EMPREINTES-KIT-UNITE-02-D210.txt,
# la gravure NÉE au format parsé « sha256  nom » — celui que le scénario
# scellé lit : le défaut T0 de l'unité 01 [gravure « nom en tête »,
# ZÉRO pièce vue] ne se reproduit pas ; la confrontation à chaque
# lancement, fail-closed : une divergence, RIEN ne court). LES
# QUATORZE pièces du kit (les DOUZE pièces + la gravure + le livre).
PIECES = [
    ("GRAINE-D210.txt",
     "c62a304f1df0d88882e03edecc8a9498e60bc6db293010775a9238eedcdc6673",
     "la graine D217 (consignée AVANT le premier appel, jamais re-tirée)"),
    ("LANCEUR-UNITE-08-T.bat",
     "acf950f0a155515cb6cbb4c24d37a47d908b8ab7819227981f9fa518620c957b",
     "la console officielle du kit (le run SA console, INTACT — CA6)"),
    ("LISEZMOI-KIT-UNITE-02-D210.txt",
     "a4686b324882fd0a8604ab6d7a5148f8206e63b293e9c76f256641a14da5ff24",
     "le livre du kit (l'ordre de jeu du terrain — CHOISIR CE DOSSIER)"),
    ("brouillon-loupe-08-ligne.asm",
     "663fd981192bf023c27ad68d92ef282711d4265b6ee3aac8effdda0b82a008c8",
     "le brouillon it8 du bras T (la notation consignée)"),
    ("journal-tokens-d210.jsonl",
     "0b5ddb07694ecc0cfd09919a2cdc8d62bdb5b9a0ee81db573fb87d9676fb5658",
     "le journal des tokens (100 % log-api, la couture nommée)"),
    ("garde-brut-d210.jsonl",
     "f8637fc4888137a025211f533db6ab599c9ad1bfa7343f564fba112e288295d1",
     "le garde-brut de la rig (le journal brut de la construction)"),
    ("loupe.exe",
     "41660a30752c378e27eacaeaa33ab9754a75d9d6b2c2837e1dfb0a9923555bb1",
     "LA PIÈCE de campagne (le slot loupe-08 RVA 0x49C0 porte la "
     "notation D210, 260 o cristallisés — 4498b7fa…)"),
    ("notation-loupe-08-ligne.asm",
     "bb4d72fbbfabf01d323eeb1793389602e7816c7d9ac60cfeb2328adbd4ad3240",
     "la notation D210 (le texte de la pièce au slot)"),
    ("proxy.exe",
     "446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d",
     "le scellé de l'ère (la première ligne du doré V1)"),
    ("scenario-unite08.py",
     "44384f5d4a5afbf5d17585ee73b0aeea56ba2fa76f1f4f82addf0903747a2d5a",
     "LE JUGE D204 INCHANGÉ (44384f5d…, la version corrigée — le "
     "lecteur « sha256  nom », le chargeur DONT_RESOLVE, la feuille "
     "pure)"),
    ("source-loupe-08-C.c",
     "f87bc5179bb8e9f8804d160b0bede8715f5224b5bf9c3003b188a1e790755a56",
     "le source du bras C (gcc -O2 PROPRE, la pièce livrée à l'épreuve)"),
    ("temoin-3f.bin",
     "c5fc1f28e471059d56a892ba82df1e215f5263aafd8c43fdb0e76e110d1d5ca3",
     "le témoin 3 × 64 Kio + 1 (V1 : la ligne finale incomplète)"),
    ("tests-loupe-08-C.md",
     "14ff38bd152cb7bcab3639a96bc7bbe3120dcdc6b952b3b3171f1ecd6820b297",
     "la suite de tests du bras C (N/B/R + la falsification)"),
    ("EMPREINTES-KIT-UNITE-02-D210.txt",
     "{sha_gravure}",
     "la gravure du kit (sha256 en tête — le format que le scénario "
     "scellé parse ; NÉE parsée : le défaut T0 de l'unité 01 ne se "
     "reproduit pas)"),
]

# le scénario, le réceptacle, le témoin — LES NOMS DU SCÉNARIO SCELLÉ
NOM_SCENARIO = "scenario-unite08.py"
RECEPTACLE = "preuves-unite08"
NOM_TEMOIN = "temoin-unite08.txt"

# LA CAP M1 (le plan D204, § 7) : TROIS livraisons par bloc
CAP_LIVRAISONS_BLOC = 3

# le motif des verdicts de console (RECOPIÉS, jamais recalculés)
MOTIF_VERDICT = re.compile(r"^\\[(VERT|ROUGE)\\]\\s*(.*)$")

# les lignes de refus du scénario (fail-closed au moindre)
MOTIF_REFUS = re.compile(r"\\[(T\\d|REFUS|témoin)\\]\\s*REFUS|\\[T0\\]\\s*REFUS")

# LA LIGNE DE CARNET M3 prescrite pour cette unité (au geste, à la main)
LIGNE_CARNET_M3 = (
    "T-loupe-08-d210-it1 ; le run terrain de l'unité 02 D210 ; la date "
    "du geste ; le temps humain arrondi à la minute (toute interruption "
    "> 5 min ferme la ligne et en ouvre une autre)")

# LA LIGNE DE LIVRAISON M1 prescrite (livraisons.csv du plan D204)
LIGNE_LIVRAISON_M1 = (
    "livraison,bras,tache,numero_iteration,date_kit,date_run,verdict,recoup"
    "  →  <n>,T,loupe-08-d210,it1,20261118,<date du run>,"
    "<le verdict recopié de la console>,<le recoup du labo au retour>")

# LA RÈGLE D202 (les défauts nommés AVANT correction)
LIGNE_DEFAUTS_M1 = (
    "livraison,bras,tache,classe,mecanisme,cote,piece_appui,exclusion,"
    "raison_exclusion  →  un défaut vu au run se NOMME ici AVANT toute "
    "correction (classe + mécanisme + pièce à l'appui)")

# M4 — le chrono des commandes (le labo mesura, consigné au RAPPORT) :
M4_LABO = ("le labo mesura (18/11, RAPPORT-UNITE-D210-02) : build 0,5 s ; "
           "oracle V1-V4 4,0 s ; l'épreuve POSIX 1,4 s. Le chrono du "
           "terrain se mesure au geste présent (le GUI couche "
           "début/fin/durée à la console du run).")


'''


def remplacer(src, ancien, nouveau, attendu):
    n = src.count(ancien)
    assert n == attendu, (
        f"le remplacement attendu {attendu}× trouvé {n}× : "
        f"{ancien[:70]!r}")
    return src.replace(ancien, nouveau)


def generer_le_gui(sha_gravure):
    src = BASE_V2.read_text(encoding="utf-8")

    # (a) l'en-tête : la docstring de l'édition, tout le reste inchangé
    idx = src.index("import ast\n")
    src = ("#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"
           + DOCSTRING + src[idx:])

    # (b) LA SECTION A : les constantes du kit loupe-08
    debut = src.index('VERSION = "2.0.0"')
    fin = src.index("class ErreurRun(RuntimeError):")
    src = (src[:debut]
           + SECTION_A.format(sha_gravure=sha_gravure)
           + src[fin:])

    # (c) LA PREUVE T0 — le seuil et les messages de la gravure du kit
    src = remplacer(
        src, "vert = len(vues) >= 15", "vert = len(vues) >= 13", 1)
    src = remplacer(
        src, '"à T0 ; la gravure EMPREINTES-PIECES-RUN "',
        '"à T0 ; la gravure EMPREINTES-KIT "', 1)
    src = remplacer(
        src, '"passera (la gravure du correctif T0)")',
        '"passera (la gravure du kit, née parsée)")', 1)
    src = remplacer(
        src, '"pièce(s) — la gravure EMPREINTES-PIECES-RUN "',
        '"pièce(s) — la gravure EMPREINTES-KIT "', 1)
    src = remplacer(
        src,
        "sur le dossier du kit. Retour (n_pieces, vert, message). Sur "
        "le kit\n    du 17/11 seul, n pièces = 0 → le run REFUSAIT ; "
        "avec la gravure du\n    correctif (EMPREINTES-PIECES-RUN.txt), "
        "n = 15.",
        "sur le dossier du kit. Retour (n_pieces, vert, message). Sans "
        "la\n    gravure EMPREINTES-KIT, n pièces = 0 → le run REFUSE ; "
        "avec la\n    gravure du kit (née parsée), n = 13.", 1)

    # (d) le run — la console du run et l'argv nommé
    src = remplacer(src, "run-console-unite02-d210-",
                    "run-console-unite08-d210-", 6)
    src = remplacer(src, "[python, scenario-unite02.py]",
                    "[python, scenario-unite08.py]", 1)

    # (e) la collecte — le DEPOT et les pièces du kit au run
    src = remplacer(
        src, "le DEPOT-d210-unite02.txt (chaque pièce du",
        "le DEPOT-d210-unite08.txt (chaque pièce du", 1)
    src = remplacer(
        src,
        'for nom in ("loupe.exe", "temoin-1.bin", "temoin-384.bin",\n'
        '                "temoin-3f.bin", "vide.bin", NOM_SCENARIO,\n'
        '                "EMPREINTES-PIECES-RUN.txt"):',
        'for nom in ("loupe.exe", "proxy.exe", "temoin-3f.bin", '
        'NOM_SCENARIO,\n'
        '                "LISEZMOI-KIT-UNITE-02-D210.txt",\n'
        '                "EMPREINTES-KIT-UNITE-02-D210.txt"):', 1)
    src = remplacer(
        src, '"DEPOT-d210-unite02.txt — le dépôt des preuves du run '
        'terrain",',
        '"DEPOT-d210-unite08.txt — le dépôt des preuves du run '
        'terrain",', 1)
    src = remplacer(
        src, 'depot = receptacle / "DEPOT-d210-unite02.txt"',
        'depot = receptacle / "DEPOT-d210-unite08.txt"', 1)

    # (f) le zip de renvoi — le nom et l'unité nommée au refus
    src = remplacer(src, "preuves-unite02-d210-<UTC>Z.zip",
                    "preuves-unite08-d210-<UTC>Z.zip", 1)
    src = remplacer(src, '"loupe-02-d210, le refus est NOMMÉ : le "',
                    '"loupe-08-d210, le refus est NOMMÉ : le "', 1)
    src = remplacer(src, 'nom_zip = "preuves-unite02-d210-"',
                    'nom_zip = "preuves-unite08-d210-"', 1)

    # (g) LE SELFTEST — les pièces de l'unité aux fixtures T3-T12
    src = remplacer(src, 'donne = kit2 / "temoin-384.bin"',
                    'donne = kit2 / "GRAINE-D210.txt"', 1)
    src = remplacer(src, 'if x["piece"] == "temoin-384.bin"][0]',
                    'if x["piece"] == "GRAINE-D210.txt"][0]', 1)
    src = remplacer(src, '(kit2 / "notation-loupe-02-lire.asm").unlink()',
                    '(kit2 / "notation-loupe-08-ligne.asm").unlink()', 1)
    src = remplacer(
        src, 'if x["piece"] == "notation-loupe-02-lire.asm"][0]',
        'if x["piece"] == "notation-loupe-08-ligne.asm"][0]', 1)
    src = remplacer(src, "vert and n >= 15,", "vert and n >= 13,", 1)
    src = remplacer(
        src, 'f.name != "EMPREINTES-PIECES-RUN.txt":',
        'f.name != "EMPREINTES-KIT-UNITE-02-D210.txt":', 1)
    src = remplacer(
        src,
        'note("T5b:le-defaut-d-origine-nomme", n0 == 0 and not vert0,\n'
        '             "sans EMPREINTES-PIECES-RUN, le scénario voit 0 '
        'pièce — "\n'
        '             "le kit du 17/11 aurait REFUSÉ à T0 (le défaut '
        'nommé)")',
        'note("T5b:le-refus-sans-gravure-nomme", n0 == 0 and not '
        'vert0,\n'
        '             "sans la gravure EMPREINTES-KIT, le scénario voit '
        '0 pièce — "\n'
        '             "le run REFUSERAIT à T0 (la fail-closed '
        'nommée)")', 1)
    src = remplacer(
        src,
        'console_echantillon = (\n'
        '        "[VERT] T0:la-piece-recoupee-a-l-empeinte-gravee — '
        'loupe.exe "\n'
        '        "sha256 cf251c12d580b729… == la gravure du kit\\n"\n'
        '        "[VERT] V1:temoin-1.bin-la-fenetre-nee-a-l-ouverture — '
        '…\\n"\n'
        '        "[ROUGE] V2:les-bords-de-fenetre — l\'écart nommé\\n"\n'
        '        "[témoin] preuves-unite02/temoin-unite02.txt — 21 VERT, '
        '1 ROUGE\\n"\n'
        '        "=== LE RUN DE L\'UNITÉ 2 FINI ===\\n")',
        'console_echantillon = (\n'
        '        "[VERT] T0:la-piece-recoupee-a-l-empeinte-gravee — '
        'loupe.exe "\n'
        '        "sha256 41660a30d580b729… == la gravure du kit\\n"\n'
        '        "[VERT] V1:le-dore-proxy-premiere-ligne — les 77 o == '
        'le "\n'
        '        "modèle\\n"\n'
        '        "[ROUGE] V2:le-differentiel-10-000-lignes — l\'écart '
        'nommé\\n"\n'
        '        "[témoin] preuves-unite08/temoin-unite08.txt — 9 VERT, '
        '1 ROUGE\\n"\n'
        '        "=== LE RUN DE L\'UNITÉ 4 FINI ===\\n")', 1)
    src = remplacer(src, "TÉMOIN DU RUN DE L'UNITÉ 2",
                    "TÉMOIN DU RUN DE L'UNITÉ 4", 2)

    # (h) LA FENÊTRE — le titre, l'entête du verrou, l'onglet témoin
    src = remplacer(
        src,
        'text=("TRIADE — l\'unité 01 D210 "\n'
        '                                    "(loupe-02 lire × bras T)"),',
        'text=("TRIADE — l\'unité 02 D210 "\n'
        '                                    "(loupe-08 ligne × '
        'bras T)"),', 1)
    src = remplacer(
        src,
        '"l\'EMPREINTES-KIT d\'origine du 17/11 ET la gravure "\n'
        '                      "du correctif T0 (EMPREINTES-PIECES-RUN.txt, '
        'le "\n'
        '                      "format que le scénario scellé parse)."),',
        '"la gravure EMPREINTES-KIT-UNITE-02-D210.txt (le "\n'
        '                      "format que le scénario scellé parse — NÉE '
        'parsée "\n'
        '                      "d\'origine : le défaut T0 de l\'unité 01 ne '
        'se "\n'
        '                      "reproduit pas)."),', 1)
    src = remplacer(
        src,
        '"naît DU SCÉNARIO (temoin-unite02.txt au réceptacle "\n'
        '                      "preuves-unite02/) ; dater et signer DE '
        'VOTRE MAIN "',
        '"naît DU SCÉNARIO (temoin-unite08.txt au réceptacle "\n'
        '                      "preuves-unite08/) ; dater et signer DE '
        'VOTRE MAIN "', 1)

    # (i) L'AUDIT FINAL — aucune référence de l'unité 01 ne demeure
    for interdit in ("unite02", "loupe-02", "EMPREINTES-PIECES-RUN",
                     "temoin-384", "temoin-1.bin", "vide.bin",
                     "NOTE-REPRISE", "UNITE-01", "LISEZMOI-KIT-UNITE-01",
                     "notation-loupe-02", "brouillon-loupe-02",
                     "source-loupe-02", "tests-loupe-02",
                     "LANCEUR-UNITE-02-T", "DEPOT-d210-unite02",
                     "l'unité 01 D210", "T-loupe-02-d210"):
        assert interdit not in src, f"référence interdite demeure : {interdit}"
    for exigence in ("scenario-unite08.py", "preuves-unite08",
                     "temoin-unite08.txt", "run-console-unite08-d210-",
                     "DEPOT-d210-unite08.txt", "preuves-unite08-d210-",
                     "etat-run-unite08-d210.json", "T-loupe-08-d210-it1",
                     "loupe-08-d210", "EMPREINTES-KIT-UNITE-02-D210.txt",
                     "proxy.exe", "notation-loupe-08-ligne.asm",
                     "GRAINE-D210.txt"):
        assert exigence in src, f"référence attendue absente : {exigence}"

    GUI_PY.write_text(src, encoding="utf-8", newline="\n")
    py_compile.compile(str(GUI_PY), doraise=True)
    print(f"[gui] {GUI_PY.name} né : {len(src.splitlines())} lignes, "
          f"{GUI_PY.stat().st_size} o — la chirurgie nommée "
          f"(l'en-tête + LA SECTION A + 26 remplacements affirmés)")
    return GUI_PY


# ---------------------------------------------------------------------------
# 3· LE LANCEUR — CRLF, ASCII (le précédent 337)
# ---------------------------------------------------------------------------
BAT_TEXT = r"""@echo off
rem ============================================================================
rem LANCER-RUN-UNITE08-D210-1CLIC.bat - LE RUN DE L'UNITE 02 D210 EN UN CLIC
rem [le kit kit-gui-1clic-unite08-d210 - l'edition v1 du 18/11/2026 : LA
rem  DEUXIEME UNITE de la campagne D210 (loupe-08 ligne x bras T, la
rem  sequence tiree de la graine D217 - jamais re-tiree ; le kit ne a la
rem  Task 208, le juge scenario-unite08.py D204 INCHANGE [44384f5d... la
rem  version corrigee], la gravure EMPREINTES-KIT-UNITE-02-D210.txt NEE
rem  PARSEE - sha256 en tete, le format que le scenario scelle lit : le
rem  defaut T0 de l'unite 01 ne se reproduit pas) ; le dossier racine du
rem  zip porte LE NOM DU KIT (kit-unite-02-d210-20261118 - le pas 1-KIT
rem  du livre du kit : CHOISIR CE DOSSIER ; le double-clic du lanceur EST
rem  le choix - le GUI recoupe LUI-MEME les pieces de CE dossier)]
rem
rem LE GESTE : DOUBLE-CLIQUEZ CE FICHIER SEUL. Le GUI ouvre sa fenetre,
rem recoupe LES QUATORZE pieces du kit (fail-closed), prouve que LE
rem SCENARIO SCELLE voit les pieces (LA PREUVE T0 - les TREIZE pieces de
rem la gravure, loupe.exe recoupe), et LE BOUTON VERT conduit tout : LE
rem RUN au scenario-unite08.py (SA console ecrite AU FIL DE L'EAU, UTF-8
rem des deux cotes du tuyau), les verdicts RECOPIES des lignes, le
rem chrono M4, LA COLLECTE (la console COPIEE au receptacle
rem preuves-unite08\, le DEPOT-d210-unite08.txt assemble) - puis le
rem temoin est a VOTRE MAIN (D99) : dater, signer au bloc-notes,
rem renvoyer le dossier ENTIER au coffre /test (le GUI l'assemble en
rem zip - l'exigence de la signature et la cap M1 sont tenues par
rem construction).
rem
rem CE QUE LE GUI EXIGE : Python 3 avec tkinter (l'installeur python.org
rem les livre ensemble - cochez "Add to PATH" et "tcl/tk and IDLE").
rem RIEN D'AUTRE : le scenario est pur ctypes de la stdlib, le kit
rem porte ses PIECES (loupe.exe, proxy.exe, le temoin 3f) - aucun outil
rem a installer au-dela de Python.
rem
rem CE QUE CE GUI NE FERA JAMAIS : dater ni signer un temoin (votre
rem main, toujours, D99) ; deposer au coffre (il OUVRIRA le /test au
rem navigateur, il n'ecrit JAMAIS au Drive) ; fabriquer un chiffre
rem (les verdicts sont RECOPIES des lignes de console) ; toucher les
rem pieces scellees (loupe.exe, le scenario, proxy.exe, les temoins :
rem LUS, le scenario lui-meme recoupe loupe.exe AVANT de courir) ;
rem renommer ni editer les pieces du receptacle.
rem
rem ETAPE 0, SEULEMENT SI UN CADRE "Windows a protege votre PC"
rem apparait au double-clic [la marque du web] : clic droit sur CE
rem fichier, Proprietes, cochez "Debloquer" en bas, OK - puis
rem double-cliquez encore. Ce fichier descend du coffre Drive : il
rem porte la marque, comme toute piece telechargee.
rem ============================================================================
setlocal EnableExtensions
title TRIADE - le run de l'unite 02 D210 (loupe-08 ligne x bras T) en un clic
cd /d "%~dp0"

set "PY="
py -3 -c "import sys" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys" >nul 2>&1 && set "PY=python"
if not defined PY python3 -c "import sys" >nul 2>&1 && set "PY=python3"
if not defined PY goto python_absent

%PY% -c "import tkinter" >nul 2>&1
if errorlevel 1 goto tkinter_absent

%PY% triade_run_unite08_d210_gui.py
set "RC=%errorlevel%"
if "%RC%"=="0" goto fin
echo.
echo [REFUS NOMME] le GUI s'est ferme avec le code %RC% - l'ecran du GUI
echo        nomme la cause ; le journal de session vit a TRIADE_logs\.
:fin
pause
exit /b %RC%

:python_absent
echo.
echo [REFUS NOMME] Python 3 est ABSENT - le GUI en exige un.
echo        https://www.python.org - cochez "Add to PATH".
pause
exit /b 2

:tkinter_absent
echo.
echo [REFUS NOMME] tkinter est ABSENT de ce Python - reinstallez Python
echo        depuis python.org en cochant "tcl/tk and IDLE" (livre avec
echo        l'installeur ; tkinter ne s'installe PAS par pip).
pause
exit /b 2
"""


def ecrire_le_bat():
    donnees = BAT_TEXT.replace("\n", "\r\n").encode("ascii")
    BAT.write_bytes(donnees)
    assert donnees.count(b"\r\n") > 50, "le bat aurait perdu ses CRLF"
    assert donnees.replace(b"\r\n", b"").count(b"\n") == 0
    print(f"[bat] {BAT.name} né : {BAT.stat().st_size} o, "
          f"{len(BAT_TEXT.splitlines())} lignes, CRLF conservés")


# ---------------------------------------------------------------------------
# 4· LE LIVRE — LISEZMOI-RUN-UNITE08-D210-1CLIC.txt
# ---------------------------------------------------------------------------
LISEZMOI_TEXT = '''LISEZMOI-RUN-UNITE08-D210-1CLIC — LE RUN DE L'UNITÉ 02 D210 EN UN CLIC
(l'édition v1 du 18/11/2026 — LA DEUXIÈME UNITÉ : loupe-08 ligne × bras T,
la séquence tirée de la graine D217, jamais re-tirée ; la suite ① annoncée
à l'Entrée 341 : le GUI 1-clic de l'unité au commandement, le précédent
de la 337)
================================================================================

L'OBJET : conduire LE GESTE TERRAIN de la deuxième unité de la campagne
D210 (loupe-08 ligne × bras T — le LISEZMOI-KIT-UNITE-02-D210 du kit fait
foi : l'ordre de jeu 1·KIT → 2·RUN → 3·TÉMOIN) SANS AUCUN CHOIX DE
DOSSIER : le kit VIT DANS CE DOSSIER (loupe.exe, le juge, proxy.exe, le
témoin 3f, les gravures), le GUI le recoupe LUI-MÊME à chaque lancement.
Le pas « 1·KIT — CHOISIR CE DOSSIER (kit-unite-02-d210-20261118) » du
livre du kit se vit AU DOUBLE-CLIC : le dossier racine du zip PORTE LE
NOM DU KIT — dézippez, vous voilà DANS le dossier daté, le lanceur y
attend votre clic.

LA PIÈCE DE CETTE UNITÉ (le RAPPORT-UNITE-D210-02 du labo fait foi) :
loupe.exe (127 488 o, sha256 41660a30…) — le build du plan où le slot
loupe-08 (RVA 0x49C0, 320 o) porte LA NOTATION DE CAMPAGNE : 260 o
cristallisés (4498b7fa…), le différentiel au scellé CONFINÉ au slot +
la porte R10 ; le contrat loupe-08:R1 : composer UNE ligne hexadécimale
de 77 o au tampon fixe — les 8 chiffres MAJUSCULES du décalage, 2
espaces, les seize groupes « HH » séparés d'un espace (l'espace médian
DOUBLÉ après le huitième), 2 espaces, le miroir ASCII de 16 (le point
hors 0x20..0x7E), le NUL — EXACTEMENT 77 o écrits, jamais un de plus ;
AUCUN débordement par construction, AUCUNE entrée IAT — la feuille
pure. LA CONSTRUCTION 100 % log-api (18 appels, 52 729 tokens, la
spirale corrective 51 % — H8 tenue), la cristallisation DIX rebuilds
consécutifs identiques, l'oracle au harnais 12 VERT 0 ROUGE, l'épreuve
POSIX du bras C 10 VERT 0 ROUGE (gcc -O2, la graine 20261115).

LE JUGE DE CE KIT : scenario-unite08.py (44384f5d… — LE SCÉNARIO D204
INCHANGÉ, la version corrigée : la faute au juge nommée à la 338 ne se
reproduit pas ici) ; LA GRAVURE EMPREINTES-KIT-UNITE-02-D210.txt NÉE
PARSÉE (« sha256  nom » — le format que le scénario scellé lit : le
défaut T0 de l'unité 01 [gravure « nom en tête », ZÉRO pièce vue, le
run aurait REFUSÉ] ne se reproduit pas non plus, NOMMÉ PARCE QU'IL NE
SE REPRODUIT PAS — D202 : les défauts se nomment, l'absence aussi).
LA PREUVE T0 : le GUI extrait lire_empreintes DU FICHIER LIVRÉ par AST
et l'exécute sur ce dossier AVANT tout lancement — « le scénario scellé
voit 13 pièces (loupe.exe recoupé 41660a30…) » s'affiche en vert ; le
moindre écart = le bouton reste gris, RIEN ne court.

LE GESTE : dézippez ce kit où vous voulez (Téléchargements, Bureau) —
kit-unite-02-d210-20261118/ — puis DOUBLE-CLIQUEZ
LANCER-RUN-UNITE08-D210-1CLIC.bat. La fenêtre s'ouvre sur LE VERROU
(l'étape 1 se recoupe seule) ; si un cadre « Windows a protégé votre
PC » apparaît : clic droit sur le .bat, Propriétés, cochez
« Débloquer », OK — la marque du web, comme toute pièce téléchargée
du coffre.

LA FENÊTRE — LES CINQ ONGLETS :
  1·VERROU   — LES QUATORZE pièces du kit recoupées sha256 par sha256
               (les DOUZE pièces + la gravure + le livre) + LA PREUVE
               T0 (le scénario scellé voit les TREIZE pièces de la
               gravure) ; une divergence, RIEN ne court (fail-closed) ;
  2·RUN      — LE BOUTON VERT « TOUT LANCER » : le scénario couru (SA
               console, écrite AU FIL DE L'EAU — chaque ligne couchée
               et flushée à mesure — un crash laisse la console
               VIVANTE), UTF-8 des deux côtés du tuyau
               (PYTHONIOENCODING posé par le GUI), la console sauvée
               à run-console-unite08-d210-<horodatage>.txt ; les
               verdicts RECOPIÉS des lignes [VERT]/[ROUGE] (jamais
               recalculés) ; le chrono M4 (début/fin/durée mesurés) ;
               REJOUER conduit le rejeu diagnostic (le rejouage d'une
               unité verte n'est PAS une livraison, § 7) ;
  3·TÉMOIN   — LE VERROU D99 : le GUI ne signe JAMAIS. Le témoin naît
               DU SCÉNARIO (preuves-unite08/temoin-unite08.txt, aux
               blancs « Daté le : » / « Signé    : ») ; ouvre-le au
               bloc-notes, DATE et SIGNE de votre main, puis
               ASSEMBLER LE ZIP : preuves-unite08-d210-<UTC>.zip (le
               réceptacle ENTIER + le DEPOT + la console) —
               l'assemblage EXIGE le témoin daté-signé (refus nommé
               sinon) et REFUSE au-delà de la cap M1 (TROIS
               livraisons par bloc, la règle § 7 du plan D204) ;
               renvoyez le zip au coffre /test (le bouton OUVRIR LE
               COFFRE y mène au navigateur — le GUI n'écrit JAMAIS au
               Drive) ;
  4·LIVRE    — les lignes AU GESTE : la ligne de carnet M3
               (T-loupe-08-d210-it1), la ligne de livraison M1
               (livraisons.csv), LA RÈGLE D202 (les défauts nommés
               AVANT correction, defauts.csv), le chrono M4 ; le livre
               se remplit À LA MAIN au bloc-notes, jamais ici ;
  5·JOURNAL  — le journal de la session (chaque geste y vit) ; si un
               écran nomme un défaut, renvoyez TRIADE_logs/ TEL QUEL.

L'ATTENDU DU RUN (le juge du kit, recopié du contrat) : les DIX
verdicts — T0 la pièce recoupée ; V1 le doré (la première ligne du
proxy.exe scellé + la ligne finale incomplète du témoin 3f) ; V2 le
différentiel (10 000 lignes == le modèle, la graine 20261115) et
EXACTEMENT 77 o ; V3 les QUATRE rejets -5 (la sortie poison intacte) ;
V4 la falsification (l'octet muté diverge) — 10 VERT, 0 ROUGE, code
retour 0.

UN RUN ROUGE (le scénario rend 1) : le run FINIT quand même — le témoin
naît, le dossier de preuves se renvoie ENTIER (le dépôt d'un run rouge
est AUSSI un témoin) et LES DÉFAUTS SE NOMMENT AVANT CORRECTION (D202).
Un REFUS (le code 2 — une pièce divergente, une empreinte absente) : le
GUI s'arrête et NOMME la cause — ARRÊTEZ, ne modifiez AUCUN fichier, la
console vivante se renvoie TELLE QUELLE.

CE QUE CE GUI NE FERA JAMAIS (les frontières, tenues par construction) :
  — DATER ni SIGNER un témoin : votre main, toujours (D99) ;
  — DÉPOSER au coffre : il OUVRIRA le /test au navigateur, il n'écrit
    JAMAIS au Drive ;
  — FABRIQUER un chiffre : les verdicts sont RECOPIÉS des lignes de
    console ; le compte VERT/ROUGE est un recomptage des lignes
    couchées, jamais une réévaluation ;
  — TOUCHER les pièces scellées : le scénario, loupe.exe, proxy.exe,
    les témoins LUS (le scénario lui-même recoupe loupe.exe AVANT de
    courir — le moindre écart = [T0] REFUS, RIEN ne court) ;
  — RENOMMER ni ÉDITER les pièces du réceptacle (le témoin, les
    consoles : COPIÉES, jamais retouchées) ;
  — DÉPASSER la cap M1 : TROIS livraisons par bloc — le quatrième zip
    refuse, le refus est NOMMÉ.

LA MÉMOIRE DU GUI : etat-run-unite08-d210.json (à côté du GUI) retient
les étapes vertes, le contexte du run (console, verdicts, chrono), les
livraisons assemblées — rouvrez le GUI, tout se retrouve (et si l'état
périt, il se RECOMPLÈTE des pièces nées : la console la plus récente,
le témoin — RELUS, jamais réinventés, la source nommée). TRIADE_logs/
conserve le journal de chaque session.

L'HONNÊTETÉ DE CETTE ÉDITION v1 (l'épreuve du labo, D122 — le labo n'a
AUCUN Windows : la fenêtre éprouvée au labo POSIX sous serveur X
virtuel, l'exécution Windows se vit AU TERRAIN) :
  — le selftest (python triade_run_unite08_d210_gui.py --selftest) :
    15 VERT, 0 ROUGE — le verrou (14/14), le fail-closed, LA PREUVE T0
    (13 pièces vues), les verdicts recopiés, la main détectée (D99),
    la collecte, le zip, la cap M1, l'état, la reconstitution ;
  — l'épreuve fonctionnelle : 9 VERT, 0 ROUGE — LA CHAÎNE RÉELLE du
    bouton vert conduite au bac POSIX (verrou, preuve T0, run,
    collecte, zip, cap) avec un scénario SUBSTITUÉ étiqueté LABO (le
    bac n'a aucun Windows — le substitué exécute les fonctions pures
    DU SCÉNARIO LIVRÉ extraites par AST et émet LA MÊME console,
    JAMAIS maquillé en run terrain) ;
  — l'épreuve visuelle sous serveur X virtuel : 7 VERT, 0 ROUGE — la
    fenêtre née, les CINQ onglets, les QUATORZE pièces rendues, le
    verrou VERT à l'écran, les accents rendus, le livre, le zip
    inactif sans run ;
  — l'épreuve du zip : les 18 entrées dézippées au bac, le juge du
    zip == le kit du labo byte-byte, le GUI DÉZIPPÉ conduit son propre
    selftest : 15 VERT, 0 ROUGE ;
  — le premier double-clic se vit chez vous : si un écran nomme un
    défaut, renvoyez le journal de session (TRIADE_logs/) TEL QUEL, le
    labo recoupe et corrige (D122).

LES EMPREINTES du kit vivent à EMPREINTES-GUI-UNITE08-D210-1CLIC.txt
(le GUI, le lanceur, le livre + les QUATORZE pièces du verrou recoupées)
— la console « certutil -hashfile <fichier> SHA256 » les recoupe chez
vous si vous le voulez.

LA SUITE : le run de l'unité À VOTRE GESTE (ce kit — T-loupe-08-d210-it1
demeure LA ligne de carnet : le kit livré le 18/11 n'a jamais couru,
aucune itération ne se consomme) ; après le run revenu et recoupé,
l'unité suivante selon la séquence tirée (loupe-13 le bras T d'abord) ;
la re-livraison d'attribution empirique se prépare au commandement.
'''


def ecrire_le_lisezmoi():
    LISEZMOI.write_text(LISEZMOI_TEXT, encoding="utf-8", newline="\n")
    print(f"[livre] {LISEZMOI.name} né : {LISEZMOI.stat().st_size} o, "
          f"{len(LISEZMOI_TEXT.splitlines())} lignes")


def main():
    print("=== LA CONSTRUCTION DU GUI 1-CLIC DE L'UNITÉ 02 D210 "
          "(loupe-08 ligne × bras T) ===")
    sha_gravure = recevoir_le_kit()
    generer_le_gui(sha_gravure)
    ecrire_le_bat()
    ecrire_le_lisezmoi()
    n = len([p for p in STAGING.iterdir() if p.is_file()])
    print(f"[état] le dossier du kit GUI : {n} fichiers "
          f"(14 pièces + le GUI + le lanceur + le livre — "
          f"l'EMPREINTES-GUI naît après les épreuves)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
