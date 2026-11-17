#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
triade_run_unite02_d210_gui.py — TRIADE · LE RUN DE L'UNITÉ 01 D210
(LOUPE-02 LIRE × BRAS T) EN UN CLIC · GUI v2.0.0 · LE JUGE RÉPARÉ
=========================================================================
L'ÉDITION v2 DU 18/11/2026 AU SOIR — LA CORRECTION COMMANDÉE (D202 :
les défauts nommés AVANT correction — la cause fut nommée à la 338) :
le terrain courut le kit v1 le 17/11 (18 VERT, 2 ROUGE) ; LE RECOUP-338
prouva LA PIÈCE CORRECTE (l'oracle du bloc : 22 VERT, 0 ROUGE) et LA
CAUSE AU JUGE livré — le scénario v1 (b3e896f7…) posait R_JOURNAL =
0xE4E0, SOIXANTE-QUATRE octets au-dessus de la vérité du layout
(0xE4A0, D161) : le juge lisait son journal TROP HAUT, la pièce n'y
écrivait JAMAIS, les DEUX vecteurs V2 du recouvrement échouaient ; le
rejeu forensique (la seule constante greffée au labo) REPRODUISIT le
verdict terrain — la faute au juge, JAMAIS à la pièce (le précédent
295). CE kit porte LE JUGE v2 RÉPARÉ (302fa3a1…, R_JOURNAL = 0xE4A0)
— le même qu'aux archives du bac 295 depuis l'Entrée 295 de D204, la
seule constante remise à la vérité du layout ; LA PIÈCE loupe.exe et
les QUATORZE autres pièces du kit INCHANGÉES octet pour octet (D143 :
le kit v1 demeure au coffre, INTACT). Le re-run NE CONSOMME PAS
d'itération : T-loupe-02-d210-it1 attend CE juge réparé.
UN SEUL FICHIER PYTHON, ZÉRO LIGNE DE COMMANDE (si ce n'est le lancer) —
le GUI AUTONOME qui conduit, D'UN SEUL CLIC, LE GESTE TERRAIN de la
première unité de la campagne D210 (le LISEZMOI-KIT-UNITE-01-D210 du kit
fait foi ; l'ordre de jeu : 1·KIT → 2·RUN → 3·TÉMOIN) :

    TOUT LANCER — LE VERROU des QUINZE pièces du kit + les DEUX
    gravures (fail-closed : une divergence, RIEN ne court), LA PREUVE
    T0 (le scénario scellé voit les pièces — le correctif gravé du
    18/11 : le kit du 17/11 portait l'EMPREINTES « nom en tête », le
    scénario D204 scellé parse « sha256 en tête » — le run aurait
    REFUSÉ à T0 ; le kit GUI porte EMPREINTES-PIECES-RUN.txt au format
    parsé, la preuve recoupée à CHAQUE lancement), LE RUN au
    scenario-unite02.py v2 (SA console, écrite AU FIL DE L'EAU,
    UTF-8 des deux côtés du tuyau — PYTHONIOENCODING posé par le GUI),
    les verdicts RECOPIÉS des lignes de console (jamais recalculés),
    le chrono M4 du run (mesuré, jamais une analyse), LA COLLECTE (la
    console COPIÉE au réceptacle preuves-unite02/, le DEPOT-d210.txt
    assemblé), et LE GUIDE DE RENVOI — dater et signer le témoin DE
    VOTRE MAIN (D99), renvoyer le dossier ENTIER au coffre /test.

    l'assemblage du zip preuves-unite02-d210-<UTC>.zip EXIGE le témoin
    DATÉ ET SIGNÉ (D99 tenu par construction) et refuse au-delà de la
    cap M1 (TROIS livraisons par bloc, la règle § 7 du plan D204).

LE CORRECTIF T0 (le 18/11/2026, nommé au LISEZMOI du kit GUI) : le kit
kit-unite-01-d210-20261117 tel que livré portait
EMPREINTES-KIT-UNITE-01-D210.txt au format « nom  taille o  sha256 » —
le scénario scellé (ce kit v2 : le juge 302fa3a1… réparé à la 339 —
le LECTEUR de D204 inchangé) lit « sha256  nom » :
lire_empreintes() y voyait ZÉRO pièce, T0 aurait REFUSÉ (« aucune
EMPREINTES*.txt au kit — rien ne court »). La preuve vécue au labo :
l'extraction AST de lire_empreintes du scénario LIVRÉ, exécutée sur le
kit du 17/11 → 0 pièce ; sur le kit GUI (EMPREINTES-PIECES-RUN.txt au
format parsé, les QUINZE pièces gravées) → 15 pièces, loupe.exe
cf251c12… recoupé. L'EMPREINTES-KIT d'origine demeure INTACT à ses
côtés (D143 : rien n'est jamais détruit) ; le verrou du GUI recoupe
LES DEUX gravures à chaque lancement.

CE QUE CE GUI NE FERA JAMAIS (les frontières, tenues par construction) :
    — DATER ni SIGNER le témoin (votre main, toujours — D99) ; le
      témoin naît DU SCÉNARIO, le GUI le lit et le RECOPIE, il ne
      touche JAMAIS à ses octets ;
    — DÉPOSER au coffre (il OUVRIRA le /test au navigateur, il
      n'écrit JAMAIS au Drive) ;
    — FABRIQUER un chiffre (les verdicts sont RECOPIÉS des lignes de
      console ; le compte VERT/ROUGE est un recomptage des lignes
      couchées, jamais une réévaluation) ;
    — TOUCHER les pièces scellées (le scénario, loupe.exe, les
      témoins : LUS ; le scénario lui-même recoupe loupe.exe AVANT de
      courir — le moindre écart = [T0] REFUS, RIEN ne court) ;
    — RENOMMER ni ÉDITER les pièces du réceptacle (temoin-unite02.txt,
      les consoles : COPIÉES, jamais retouchées) ;
    — DÉPASSER la cap M1 (TROIS livraisons par bloc — l'assemblage du
      zip refuse au-delà, le refus est NOMMÉ).

Lancement :
    double-cliquez LANCER-RUN-UNITE02-D210-1CLIC.bat  (le kit complet), ou :
    python triade_run_unite02_d210_gui.py [--selftest]
"""

import ast
import datetime as dt
import hashlib
import json
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import time

# ===========================================================================
# SECTION A — LES CONSTANTES DU KIT
# ===========================================================================

VERSION = "2.0.0"
EDITION = ("l'édition v2 du 18/11/2026 — LE JUGE RÉPARÉ (la correction "
           "de la 339 : scenario-unite02.py v2 302fa3a1…, R_JOURNAL = "
           "0xE4A0 — la vérité du layout ; la cause des deux rouge du "
           "terrain nommée à la 338, la pièce INCHANGÉE ; le kit v1 "
           "demeure au coffre — D143)")

GUI_DIR = pathlib.Path(__file__).resolve().parent
FICHIER_ETAT = GUI_DIR / "etat-run-unite02-d210.json"
DOSSIER_LOGS = GUI_DIR / "TRIADE_logs"

# le coffre — le dossier /test du Drive « Triade »
COFFRE_TEST_URL = ("https://drive.google.com/drive/folders/"
                   "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0")

NOM_RUN = "l'unité 01 D210 (loupe-02 lire × bras T)"

# LES PIÈCES DU KIT — sha256 gravées (EMPREINTES-KIT-UNITE-01-D210.txt,
# la confrontation à chaque lancement, fail-closed : une divergence, RIEN
# ne court). LES QUINZE pièces du kit (le juge v2 de la 339 à la place du
# v1 fautif, les QUATORZE autres INCHANGÉES du 17/11) + les DEUX gravures
# (l'EMPREINTES-KIT d'origine INCHANGÉ + la gravure v2 au format parsé).
PIECES = [
    ("GRAINE-D210.txt",
     "c62a304f1df0d88882e03edecc8a9498e60bc6db293010775a9238eedcdc6673",
     "la graine D217 (consignée AVANT le premier appel, jamais re-tirée)"),
    ("LANCEUR-UNITE-02-T.bat",
     "7cbc677da0a58f543e6c18891fe84fa3b6087181755c9a58aa99cf3975e701da",
     "la console officielle du kit (le run SA console, INTACT — CA6)"),
    ("LISEZMOI-KIT-UNITE-01-D210.txt",
     "026e4c7f1afc1bd219497e37b36d9ea0b43e4b8bcbe05e91ab5ceb629e7c8874",
     "le livre du kit (l'ordre de jeu du terrain)"),
    ("NOTE-REPRISE-ATELIER.txt",
     "8ef08d47bb7966ceb55305c35f3a14e20d33a7111b703eff4ab5c3630780a159",
     "la note de reprise (la perte du bac nommée)"),
    ("brouillon-loupe-02-lire.asm",
     "5e4bae81be55216384b717c30da0e60faf8cde0f705ad46a1ff1fcae3f4ae4e0",
     "le brouillon it5 du bras T (la notation consignée)"),
    ("journal-tokens-d210.jsonl",
     "2559ecd7fd606a5c17505a46d6e05e90c12324603755659f649ab57f7b6af34f",
     "le journal des tokens (100 % log-api, la couture nommée)"),
    ("loupe.exe",
     "cf251c12d580b72997f3e37e2f723aefd1abaa90b3965a834ecb5e1718507fdc",
     "LA PIÈCE de campagne (le slot loupe-02 RVA 0x4240 porte la "
     "notation D210, 300 o cristallisés — c8ec754e…)"),
    ("notation-loupe-02-lire.asm",
     "32524f31631ce2f1e68203a7dce4a8c0cfe2a15c468f9a69e0f3e056f109f325",
     "la notation D210 (le texte de la pièce au slot)"),
    ("scenario-unite02.py",
     "302fa3a1ce0a9a883079a72732f2f48e25fd540d003b3132a233ab0f3c9a8185",
     "LE JUGE v2 RÉPARÉ D204 (R_JOURNAL = 0xE4A0, la vérité du layout "
     "D161 — la v1 b3e896f7… portait 0xE4E0 : la cause des deux rouge "
     "nommée à la 338, la faute au juge JAMAIS à la pièce ; le chargeur "
     "DONT_RESOLVE, le lecteur INCHANGÉ)"),
    ("source-loupe-02-C.c",
     "02cbbba0bfaaaf6bd7136f62149aa38a948f90f8eef9b79e17de8b4baed4fa21",
     "le source du bras C (gcc -O2 PROPRE, la pièce livrée à l'épreuve)"),
    ("temoin-1.bin",
     "df7e70e5021544f4834bbee64a9e3789febc4be81470df629cad6ddb03320a5c",
     "le témoin 1 octet (V1)"),
    ("temoin-384.bin",
     "3396717b98b4859b20ec0d673dcf168314834fc170fbc6b877f4eb32461d68c6",
     "le témoin 384 octets (V1/V2/V3/V5)"),
    ("temoin-3f.bin",
     "c5fc1f28e471059d56a892ba82df1e215f5263aafd8c43fdb0e76e110d1d5ca3",
     "le témoin 3 × 64 Kio + 1 (V1/V2)"),
    ("tests-loupe-02-C.md",
     "d3e2cab9b8a711ef5cdc587741c4376e0a81e81f786552d69138e6139cf88e73",
     "la suite de tests du bras C (N/B/R + la falsification)"),
    ("vide.bin",
     "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
     "le vide — 0 octet (V1 : l'ouverture sans fenêtre)"),
    ("EMPREINTES-KIT-UNITE-01-D210.txt",
     "ca4177a79f861d8aadcfe2259f3249dabdedcd4229486b504e2777283a1fe498",
     "la gravure d'ORIGINE du kit 17/11 (nom en tête — le format "
     "humain, INCHANGÉ)"),
    ("EMPREINTES-PIECES-RUN.txt",
     "cb2a8b0f370ed0dc8f80bedd9f9c558d383f7804948cbd77475ee4011d0aaa46",
     "la gravure du kit v2 (sha256 en tête — le format du scénario "
     "scellé, les QUINZE pièces, la ligne du juge v2 302fa3a1…)"),
]

# le scénario, le réceptacle, le témoin — LES NOMS DU SCÉNARIO SCELLÉ
NOM_SCENARIO = "scenario-unite02.py"
RECEPTACLE = "preuves-unite02"
NOM_TEMOIN = "temoin-unite02.txt"

# LA CAP M1 (le plan D204, § 7) : TROIS livraisons par bloc
CAP_LIVRAISONS_BLOC = 3

# le motif des verdicts de console (RECOPIÉS, jamais recalculés)
MOTIF_VERDICT = re.compile(r"^\[(VERT|ROUGE)\]\s*(.*)$")

# les lignes de refus du scénario (fail-closed au moindre)
MOTIF_REFUS = re.compile(r"\[(T\d|REFUS|témoin)\]\s*REFUS|\[T0\]\s*REFUS")

# LA LIGNE DE CARNET M3 prescrite pour cette unité (au geste, à la main)
LIGNE_CARNET_M3 = (
    "T-loupe-02-d210-it1 ; le run terrain de l'unité 01 D210 ; la date "
    "du geste ; le temps humain arrondi à la minute (toute interruption "
    "> 5 min ferme la ligne et en ouvre une autre)")

# LA LIGNE DE LIVRAISON M1 prescrite (livraisons.csv du plan D204)
LIGNE_LIVRAISON_M1 = (
    "livraison,bras,tache,numero_iteration,date_kit,date_run,verdict,recoup"
    "  →  <n>,T,loupe-02-d210,it1,20261117,<date du run>,"
    "<le verdict recopié de la console>,<le recoup du labo au retour>")

# LA RÈGLE D202 (les défauts nommés AVANT correction)
LIGNE_DEFAUTS_M1 = (
    "livraison,bras,tache,classe,mecanisme,cote,piece_appui,exclusion,"
    "raison_exclusion  →  un défaut vu au run se NOMME ici AVANT toute "
    "correction (classe + mécanisme + pièce à l'appui)")

# M4 — le chrono des commandes (le labo mesura, consigné au RAPPORT) :
M4_LABO = ("le labo mesura (17/11, RAPPORT-UNITE-D210-01) : build 0,5 s ; "
           "oracle V1-V5 33,6 s. Le chrono du terrain se mesure au geste "
           "présent (le GUI couche début/fin/durée à la console du run).")


class ErreurRun(RuntimeError):
    """Un refus nommé du GUI (fail-closed) — jamais silencieux."""


# ===========================================================================
# SECTION B — LA LOGIQUE DU RUN (testable sans tkinter : --selftest)
# ===========================================================================

def maintenant_local():
    return dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def horodatage_dossier():
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def horodatage_zip():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_fichier(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


# --- le verrou : les pièces du kit, sha256 par sha256 -----------------------

def verifier_pieces(racine):
    """Recoupe LES PIÈCES du kit. Retour une liste de dicts
    {piece, attendu, calcule, vert, message} — fail-closed."""
    resultats = []
    for rel, attendu, role in PIECES:
        p = racine / rel
        if not p.exists():
            resultats.append({"piece": rel, "attendu": attendu,
                              "calcule": None, "vert": False,
                              "message": "PIÈCE ABSENTE du kit — " + role})
            continue
        calcule = sha256_fichier(p)
        vert = calcule == attendu
        message = role
        if not vert:
            message = ("sha256 DIVERGENT — " + role +
                       " ; ne modifiez RIEN, consignez l'écart, le run "
                       "ne part pas.")
        resultats.append({"piece": rel, "attendu": attendu,
                          "calcule": calcule, "vert": vert,
                          "message": message})
    return resultats


# --- LA PREUVE T0 : le scénario scellé voit les pièces -----------------------

def extraire_lire_empreintes(racine):
    """Extrait lire_empreintes() DU FICHIER LIVRÉ (AST — l'épreuve exécute
    LE CODE LIVRÉ, pas sa copie, la leçon de l'Entrée 286). Retour None
    si le scénario est absent ou illisible."""
    p = racine / NOM_SCENARIO
    if not p.exists():
        return None
    try:
        arbre = ast.parse(p.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError):
        return None
    gardes = [n for n in ast.walk(arbre)
              if isinstance(n, ast.FunctionDef) and n.name == "lire_empreintes"]
    if not gardes:
        return None
    module = ast.Module(body=gardes, type_ignores=[])
    return compile(module, str(p), "exec")


def voir_pieces_du_scenario(racine):
    """LA PREUVE T0 : exécute lire_empreintes EXTRAIT du scénario livré
    sur le dossier du kit. Retour (n_pieces, vert, message). Sur le kit
    du 17/11 seul, n pièces = 0 → le run REFUSAIT ; avec la gravure du
    correctif (EMPREINTES-PIECES-RUN.txt), n = 15."""
    code = extraire_lire_empreintes(racine)
    if code is None:
        return 0, False, ("le scénario " + NOM_SCENARIO + " est ABSENT ou "
                          "illisible — le verrou seul nomme déjà l'écart")
    ns = {"os": os, "ICI": str(racine)}
    try:
        exec(code, ns)
        vues = ns["lire_empreintes"]()
    except Exception as e:  # jamais un crash silencieux
        return 0, False, ("l'exécution de lire_empreintes a échoué : "
                          + type(e).__name__ + " — " + str(e))
    if "loupe.exe" not in vues:
        return len(vues), False, (f"le scénario voit {len(vues)} pièce(s) "
                                  "mais PAS loupe.exe — le run REFUSERAIT "
                                  "à T0 ; la gravure EMPREINTES-PIECES-RUN "
                                  "manque ou diverge.")
    vert = len(vues) >= 15
    if vert:
        return len(vues), True, (f"le scénario scellé voit {len(vues)} "
                                 "pièces (loupe.exe recoupé "
                                 + vues["loupe.exe"][:8] + "…) — T0 "
                                 "passera (la gravure du correctif T0)")
    return len(vues), False, (f"le scénario ne voit que {len(vues)} "
                              "pièce(s) — la gravure EMPREINTES-PIECES-RUN "
                              "est amputée ; le run REFUSERAIT à T0.")


# --- le run (le geste § 2 : la console du scénario, INTACTE) -----------------

def extraire_verdicts(texte):
    """Extrait les lignes de verdict RECOPIÉES de la console — jamais
    recalculées. Retour [(vert_bool, texte)]."""
    verdicts = []
    for ligne in texte.splitlines():
        m = MOTIF_VERDICT.match(ligne.strip())
        if m:
            verdicts.append((m.group(1) == "VERT", m.group(2).strip()))
    return verdicts


def compter_verdicts(texte):
    """Le compte VERT/ROUGE des lignes de console — un RECOMPTE des
    lignes couchées, jamais une réévaluation."""
    v = extraire_verdicts(texte)
    return sum(1 for vert, _ in v if vert), sum(1 for vert, _ in v if not vert)


def conduire_run(racine, rediger, argv=None, delai_ligne=0.01):
    """Coure LE SCÉNARIO (SA console, écrite AU FIL DE L'EAU — chaque
    ligne couchée et flushée à mesure : un crash laisse la console
    VIVANTE à son dernier souffle), stdout+stderr, UTF-8 des deux côtés
    (PYTHONIOENCODING posé par le GUI — la leçon d'encodage du kit 01),
    les verdicts RECOPIÉS, le fail-closed au moindre [T0] REFUS.
    Retour le contexte du run (dict).

    argv : par défaut [python, scenario-unite02.py] au dossier du kit ;
    l'épreuve du labo peut passer un scénario substitué (étiqueté LABO,
    D122 : le bac n'a aucun Windows — jamais maquillé en run terrain).
    """
    console = racine / ("run-console-unite02-d210-" + horodatage_dossier()
                        + ".txt")
    if argv is None:
        argv = [sys.executable, NOM_SCENARIO]
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    debut = dt.datetime.now()
    refus = []
    verdicts = []
    ligne_témoin = ""
    code = None
    with open(console, "w", encoding="utf-8") as f_console:
        def coucher(ligne):
            f_console.write(ligne + "\n")
            f_console.flush()

        coucher("LE RUN DE " + NOM_RUN.upper() + " — début le "
                + debut.strftime("%d/%m/%Y %H:%M:%S"))
        coucher("l'argv exact : " + " ".join(str(a) for a in argv))
        coucher("=" * 60)
        try:
            proc = subprocess.Popen(
                [str(a) for a in argv], cwd=str(racine),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                env=env)
            for brut in proc.stdout:
                ligne = brut.decode("utf-8", "replace").rstrip("\r\n")
                coucher(ligne)
                rediger("[run] " + ligne)
                m = MOTIF_VERDICT.match(ligne.strip())
                if m:
                    verdicts.append((m.group(1) == "VERT",
                                     m.group(2).strip()))
                if "REFUS" in ligne:
                    refus.append(ligne)
                if ligne.startswith("[témoin]"):
                    ligne_témoin = ligne
                time.sleep(delai_ligne)
            code = proc.wait(timeout=1800)
        except Exception as e:
            coucher("[ÉCART NOMMÉ] le run a échoué : "
                    + type(e).__name__ + " — " + str(e))
            rediger("[GUI] " + "[ÉCART NOMMÉ] le run a échoué : "
                    + type(e).__name__)
        fin = dt.datetime.now()
        coucher("=" * 60)
        coucher("la durée : " + str(round((fin - debut).total_seconds(), 1))
                + " s — fin le " + fin.strftime("%d/%m/%Y %H:%M:%S"))
        coucher("le code retour : " + str(code))
    texte_console = console.read_text(encoding="utf-8")
    n_vert, n_rouge = compter_verdicts(texte_console)
    if refus:
        raise ErreurRun(("LE SCÉNARIO A REFUSÉ (fail-closed) : « "
                         + refus[0] + " » — ARRÊTEZ, ne modifiez AUCUN "
                         "fichier, ne relancez PAS : la console vit à "
                         + console.name + " — le dépôt d'un refus est "
                         "aussi un témoin, renvoyez-la TELLE QUELLE."))
    if code is None or code not in (0, 1):
        # code 2 = le refus nommé du scénario ; autre = la chute — la
        # console demeure, renvoyée TELLE QUELLE (jamais un silence).
        raise ErreurRun("le run s'est fermé au code " + str(code)
                        + " — la console vit à " + console.name
                        + ", renvoyez-la TELLE QUELLE (le code 1 = "
                        "un verdict ROUGE nommé, le code 2 = un refus).")
    return {"console": str(console), "argv": [str(a) for a in argv],
            "debut": debut.strftime("%d/%m/%Y %H:%M:%S"),
            "fin": fin.strftime("%d/%m/%Y %H:%M:%S"),
            "duree_s": round((fin - debut).total_seconds(), 1),
            "code": code, "n_vert": n_vert, "n_rouge": n_rouge,
            "verdicts": verdicts, "ligne_témoin": ligne_témoin,
            "rouge_ok": code == 0}


# --- le témoin (le geste § 3 : D99 — la main du terrain) ----------------------

def lire_temoin(racine):
    """Lit le témoin né du scénario (LECTURE SEULE — le GUI ne touche
    JAMAIS à ses octets). Retour (texte, chemin) ou (None, None)."""
    p = racine / RECEPTACLE / NOM_TEMOIN
    if not p.exists():
        return None, None
    return p.read_text(encoding="utf-8", errors="replace"), p


def temoin_est_signe(texte):
    """D99 tenu par construction : le témoin est « signé » quand les
    lignes « Daté le : » et « Signé    : » du témoin né du scénario
    portent une main (pas les blancs d'origine)."""
    if not texte:
        return False
    date_ok = signature_ok = False
    for ligne in texte.splitlines():
        s = ligne.strip()
        if s.startswith("Daté le :"):
            reste = s[len("Daté le :"):].strip()
            date_ok = bool(reste) and set(reste) - {"_"} != set()
        elif s.startswith("Signé") and ":" in s:
            reste = s.split(":", 1)[1].strip()
            signature_ok = bool(reste) and set(reste) - {"_", "."} != set()
    return date_ok and signature_ok


# --- la collecte (le DEPOT, la console au réceptacle) -------------------------

def collecter(racine, contexte, rediger):
    """Assemble LA COLLECTE : la console COPIÉE au réceptacle (la pièce
    du kit LANCEUR laissait la console au-dedans du kit ; le réceptacle
    du renvoi porte la console ET le DEPOT — les pièces nées du scénario
    JAMAIS retouchées) et le DEPOT-d210-unite02.txt (chaque pièce du
    réceptacle + les pièces du kit au run, sha256)."""
    receptacle = racine / RECEPTACLE
    if not receptacle.is_dir():
        raise ErreurRun("le réceptacle " + RECEPTACLE + "/ est ABSENT — "
                        "le scénario n'a pas fini son geste (le témoin "
                        "n'est pas né) ; la console vit au kit, "
                        "renvoyez-la TELLE QUELLE.")
    console = pathlib.Path(contexte["console"])
    copie = receptacle / console.name
    if not copie.exists():
        shutil.copyfile(console, copie)
        rediger("[collecte] la console COPIÉE au réceptacle : "
                + copie.name)
    else:
        rediger("[collecte] la console y était déjà : " + copie.name)
    pieces = []
    for p in sorted(receptacle.iterdir()):
        if p.is_file():
            pieces.append((p.name, p.stat().st_size, sha256_fichier(p)))
    pieces_kit = []
    for nom in ("loupe.exe", "temoin-1.bin", "temoin-384.bin",
                "temoin-3f.bin", "vide.bin", NOM_SCENARIO,
                "EMPREINTES-PIECES-RUN.txt"):
        p = racine / nom
        if p.exists():
            pieces_kit.append((nom, p.stat().st_size, sha256_fichier(p)))
    lignes = [
        "DEPOT-d210-unite02.txt — le dépôt des preuves du run terrain",
        "assemblé par le GUI le " + maintenant_local()
        + " (les relevés machine ; la signature est ailleurs — D99)",
        "=" * 60,
        "le kit : " + str(racine),
        "la machine : " + contexte.get("machine", "(non consignée)"),
        "le run : " + str(contexte.get("n_vert", "?")) + " VERT, "
        + str(contexte.get("n_rouge", "?")) + " ROUGE (RECOPIÉS des "
        "lignes de console, jamais recalculés)",
        "le chrono M4 du run : début " + str(contexte.get("debut"))
        + " · fin " + str(contexte.get("fin")) + " · durée "
        + str(contexte.get("duree_s")) + " s",
        M4_LABO,
        "",
        "LES PIÈCES DU RÉCEPTACLE " + RECEPTACLE + "/ (nom, taille, "
        "sha256) :",
    ]
    for nom, taille, sha in pieces:
        lignes.append("  " + nom + "  " + str(taille) + " o  " + sha)
    lignes.append("")
    lignes.append("LES PIÈCES DU KIT AU RUN (recoupées au verrou, "
                  "l'empreinte FAIT FOI) :")
    for nom, taille, sha in pieces_kit:
        lignes.append("  " + nom + "  " + str(taille) + " o  " + sha)
    lignes.append("")
    lignes.append("LA CAP M1 (le plan D204, § 7) : TROIS livraisons par "
                  "bloc — le GUI compte " + str(contexte.get("livraisons",
                  0)) + " assemblage(s) vécu(s).")
    lignes.append("")
    lignes.append("LE GESTE QUI RESTE À LA MAIN (jamais automatisé, "
                  "D99) : dater et SIGNER " + NOM_TEMOIN + " DE VOTRE "
                  "MAIN, renvoyer le dossier " + RECEPTACLE + "/ ENTIER "
                  "au coffre /test (le GUI l'assemble en zip — l'exigence "
                  "de la signature est tenue par construction).")
    depot = receptacle / "DEPOT-d210-unite02.txt"
    depot.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    rediger("[collecte] " + depot.name + " né au réceptacle ("
            + str(len(pieces)) + " pièces)")
    return depot, pieces


# --- l'assemblage du zip (le renvoi : le dossier ENTIER) ----------------------

def assembler_zip(racine, livraisons_deja=0):
    """Le geste du renvoi : preuves-unite02-d210-<UTC>Z.zip — le
    réceptacle ENTIER (le témoin DATÉ ET SIGNÉ exigé — D99), la cap M1
    tenue (TROIS par bloc, le refus NOMMÉ). Retour (chemin_zip,
    n_livraisons_apres)."""
    receptacle = racine / RECEPTACLE
    temoin = receptacle / NOM_TEMOIN
    if not temoin.exists():
        raise ErreurRun("le témoin " + NOM_TEMOIN + " est ABSENT du "
                        "réceptacle — le zip ne s'assemble pas sans lui : "
                        "le run doit d'abord finir (TOUT LANCER).")
    texte, _ = lire_temoin(racine)
    if not temoin_est_signe(texte):
        raise ErreurRun("le témoin " + NOM_TEMOIN + " n'est pas DATÉ ET "
                        "SIGNÉ — le zip ne s'assemble pas sans votre "
                        "main (D99) : ouvrez-le (l'onglet 3·TÉMOIN), "
                        " complétez « Daté le : » et « Signé    : », "
                        "enregistrez, puis réessayez.")
    if livraisons_deja >= CAP_LIVRAISONS_BLOC:
        raise ErreurRun("LA CAP M1 (le plan D204, § 7) : TROIS "
                        "livraisons par bloc — " + str(livraisons_deja)
                        + " assemblages déjà vécus pour l'unité "
                        "loupe-02-d210, le refus est NOMMÉ : le "
                        "quatrième zip ne s'assemble pas (le livre "
                        "décide ce qui compte, D202).")
    nom_zip = "preuves-unite02-d210-" + horodatage_zip() + ".zip"
    chemin_zip = racine / nom_zip
    import zipfile
    with zipfile.ZipFile(chemin_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(receptacle.iterdir()):
            if p.is_file() and p.name != nom_zip:
                z.write(p, RECEPTACLE + "/" + p.name)
    return chemin_zip, livraisons_deja + 1


# --- l'état du GUI (la reprise d'une session interrompue) ---------------------

def charger_etat():
    try:
        return json.loads(FICHIER_ETAT.read_text(encoding="utf-8"))
    except Exception:
        return {}


def sauver_etat(etat):
    # default=str : le contexte porte des chemins (la console) — json
    # les sauve en chaînes (la leçon du correctif collecte v1.0.1 du
    # GUI v160, jamais revécue ici).
    try:
        FICHIER_ETAT.write_text(
            json.dumps(etat, ensure_ascii=False, indent=1, default=str),
            encoding="utf-8")
    except Exception:
        pass


def norme_contexte(etat):
    """Les chemins sauvés en chaînes reprennent leur type ; les champs
    manquants portent leurs défauts NOMMÉS (jamais un crash)."""
    if not isinstance(etat, dict):
        etat = {}
    contexte = etat.get("contexte") or {}
    if isinstance(contexte.get("console"), str):
        contexte["console"] = str(contexte["console"])
    etat.setdefault("etapes", {})
    etat.setdefault("livraisons", 0)
    etat.setdefault("contexte", contexte)
    return etat


def recompleter_contexte(etat, racine):
    """LA RECONSTITUTION (la leçon du correctif collecte v1.0.1) : un
    état perdu ou amputé se RECOMPLÈTE des PIÈCES NÉES — la console la
    plus récente, le témoin du réceptacle — RECOPIÉES, jamais
    réinventées, chaque reconstitution porte sa source."""
    contexte = etat.get("contexte") or {}
    source = []
    if not contexte.get("console"):
        consoles = sorted(racine.glob("run-console-unite02-d210-*.txt"))
        if consoles:
            console = consoles[-1]
            texte = console.read_text(encoding="utf-8", errors="replace")
            n_vert, n_rouge = compter_verdicts(texte)
            contexte.update(
                {"console": str(console), "n_vert": n_vert,
                 "n_rouge": n_rouge,
                 "verdicts": extraire_verdicts(texte),
                 "source": "la console " + console.name
                 + " relue au réceptacle du kit (reconstitué au "
                 "démarrage — la leçon du correctif collecte)"})
            source.append("console")
    texte, chemin = lire_temoin(racine)
    if texte and not contexte.get("temoin"):
        contexte["temoin"] = str(chemin)
        contexte["temoin_signe"] = temoin_est_signe(texte)
        source.append("témoin")
    if not contexte.get("machine"):
        contexte["machine"] = (platform.node() + " · " + platform.system()
                               + " " + platform.release() + " · "
                               + platform.machine() + " · Python "
                               + platform.python_version()
                               + (" (reconstitué au démarrage)" if source
                                  else ""))
    etat["contexte"] = contexte
    if source:
        etat["reconstitue"] = ("recomplété de : " + ", ".join(source))
    return etat


# --- LE SELFTEST — la logique éprouvée au labo, sans fenêtre -----------------

def selftest():
    """L'épreuve du labo (D122 : le bac n'a aucun Windows — la logique
    seule s'éprouve ici ; le run Windows se vit au terrain)."""
    notes = []

    def note(nom, ok, detail=""):
        notes.append((nom, bool(ok), detail))
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom}"
              + (f" — {detail}" if detail else ""))

    import tempfile
    racine = GUI_DIR
    # T1 — les gravures du GUI : LES PIÈCES attendues existent au kit
    note("T1:le-kit-porte-les-pieces-du-verrou",
         all((racine / rel).exists() for rel, _, _ in PIECES),
         "les " + str(len(PIECES)) + " pièces du verrou présentes")

    # T2 — le verrou : les pièces intactes recoupées
    resultats = verifier_pieces(racine)
    verts = sum(1 for r in resultats if r["vert"])
    note("T2:le-verrou-recoupe-les-pieces", verts == len(PIECES),
         f"{verts}/{len(PIECES)} pièces VERT")

    # T3 — fail-closed : une pièce divergente refuse (copie au bac)
    with tempfile.TemporaryDirectory() as tmp:
        kit2 = pathlib.Path(tmp)
        for rel, _, _ in PIECES:
            cible = kit2 / rel
            if cible.suffix == ".bin" or rel == "loupe.exe":
                shutil.copyfile(racine / rel, cible)
            else:
                shutil.copyfile(racine / rel, cible)
        donne = kit2 / "temoin-384.bin"
        brut = bytearray(donne.read_bytes())
        brut[7] ^= 0xFF
        donne.write_bytes(bytes(brut))
        r = [x for x in verifier_pieces(kit2)
             if x["piece"] == "temoin-384.bin"][0]
        note("T3:le-verrou-refuse-la-piece-divergente",
             not r["vert"] and "DIVERGENT" in r["message"],
             "le message nomme la divergence (fail-closed)")

        # T4 — fail-closed : une pièce absente refuse
        (kit2 / "notation-loupe-02-lire.asm").unlink()
        r = [x for x in verifier_pieces(kit2)
             if x["piece"] == "notation-loupe-02-lire.asm"][0]
        note("T4:le-verrou-refuse-la-piece-absente",
             not r["vert"] and "ABSENTE" in r["message"],
             "le message nomme l'absence")

    # T5 — LA PREUVE T0 : le scénario scellé voit les pièces du kit GUI
    n, vert, message = voir_pieces_du_scenario(racine)
    note("T5:le-scenario-scelle-voit-les-pieces", vert and n >= 15,
         f"{n} pièces vues — {message}")
    # la preuve du défaut d'origine : sans la gravure du correctif,
    # le scénario voit ZÉRO pièce (le kit du 17/11 tel que livré)
    with tempfile.TemporaryDirectory() as tmp:
        kit3 = pathlib.Path(tmp)
        for f in racine.iterdir():
            if f.is_file() and f.name != "EMPREINTES-PIECES-RUN.txt":
                shutil.copyfile(f, kit3 / f.name)
        n0, vert0, _ = voir_pieces_du_scenario(kit3)
        note("T5b:le-defaut-d-origine-nomme", n0 == 0 and not vert0,
             "sans EMPREINTES-PIECES-RUN, le scénario voit 0 pièce — "
             "le kit du 17/11 aurait REFUSÉ à T0 (le défaut nommé)")

    # T6 — les verdicts RECOPIÉS : le parseur des lignes de console
    console_echantillon = (
        "[VERT] T0:la-piece-recoupee-a-l-empeinte-gravee — loupe.exe "
        "sha256 cf251c12d580b729… == la gravure du kit\n"
        "[VERT] V1:temoin-1.bin-la-fenetre-nee-a-l-ouverture — …\n"
        "[ROUGE] V2:les-bords-de-fenetre — l'écart nommé\n"
        "[témoin] preuves-unite02/temoin-unite02.txt — 21 VERT, 1 ROUGE\n"
        "=== LE RUN DE L'UNITÉ 2 FINI ===\n")
    n_vert, n_rouge = compter_verdicts(console_echantillon)
    note("T6:les-verdicts-recopies", n_vert == 2 and n_rouge == 1,
         f"{n_vert} VERT, {n_rouge} ROUGE recopiés des lignes")

    # T7 — la détection de la main : le témoin signé
    temoin_blanc = ("TÉMOIN DU RUN DE L'UNITÉ 2\n"
                    "Daté le : ____________________\n"
                    "Signé    : ____________________\n")
    temoin_signe = ("TÉMOIN DU RUN DE L'UNITÉ 2\n"
                    "Daté le : 18/11/2026\n"
                    "Signé    : Alexis Lopez\n")
    note("T7:la-main-detectee",
         not temoin_est_signe(temoin_blanc)
         and temoin_est_signe(temoin_signe),
         "les blancs refusés, la main admise (D99)")

    # T8 — la collecte : le DEPOT né au réceptacle simulé
    with tempfile.TemporaryDirectory() as tmp:
        kit4 = pathlib.Path(tmp)
        receptacle = kit4 / RECEPTACLE
        receptacle.mkdir()
        (receptacle / NOM_TEMOIN).write_text(temoin_signe,
                                             encoding="utf-8")
        console = kit4 / "run-console-unite02-d210-20261118-000000.txt"
        console.write_text(console_echantillon, encoding="utf-8")
        contexte = {"console": str(console), "n_vert": 2, "n_rouge": 1,
                    "debut": "18/11/2026 10:00:00",
                    "fin": "18/11/2026 10:00:34", "duree_s": 34.1,
                    "machine": "la-machine-du-bac · Linux · Python 3",
                    "livraisons": 0}
        depot, pieces = collecter(kit4, contexte, lambda _s: None)
        texte_depot = depot.read_text(encoding="utf-8")
        note("T8:la-collecte-nee",
             depot.exists() and len(pieces) == 2
             and "sha256" in texte_depot
             and (receptacle / console.name).exists(),
             "le DEPOT né (témoin + console), la console COPIÉE au "
             "réceptacle, " + str(len(pieces)) + " pièces")

        # T9 — le zip : le témoin signé exigé (D99), la cap M1 tenue
        (receptacle / NOM_TEMOIN).write_text(temoin_blanc,
                                             encoding="utf-8")
        try:
            assembler_zip(kit4)
            ok9a = False
        except ErreurRun as e:
            ok9a = "D99" in str(e)
        note("T9a:le-zip-exige-la-main", ok9a,
             "le témoin aux blancs refuse l'assemblage (le refus nomme "
             "D99 — votre main, jamais le GUI)")
        (receptacle / NOM_TEMOIN).write_text(temoin_signe,
                                             encoding="utf-8")
        chemin_zip, n_liv = assembler_zip(kit4, livraisons_deja=2)
        import zipfile
        with zipfile.ZipFile(chemin_zip) as z:
            noms = z.namelist()
        note("T9c:le-zip-assemble-le-receptacle-entier",
             n_liv == 3 and all(n.startswith(RECEPTACLE + "/")
                                for n in noms) and len(noms) >= 2,
             f"{len(noms)} pièces au zip, la livraison comptée "
             f"{n_liv}/3")
        try:
            assembler_zip(kit4, livraisons_deja=3)
            ok9d = False
        except ErreurRun as e:
            ok9d = "CAP M1" in str(e)
        note("T9d:la-cap-m1-tenue", ok9d,
             "le quatrième assemblage refuse (TROIS par bloc, nommé)")

    # T10 — l'état : le va-et-vient json (default=str), la reprise
    etat = {"etapes": {"verrou": True, "run": True},
            "livraisons": 1,
            "contexte": {"console": str(racine / "x.txt"),
                         "n_vert": 22, "machine": "la machine"}}
    with tempfile.TemporaryDirectory() as tmp:
        global FICHIER_ETAT
        ancien = FICHIER_ETAT
        FICHIER_ETAT = pathlib.Path(tmp) / "etat.json"
        sauver_etat(etat)
        relu = norme_contexte(charger_etat())
        note("T10:l-etat-va-et-vient",
             relu["etapes"]["run"] is True and relu["livraisons"] == 1
             and relu["contexte"]["n_vert"] == 22,
             "l'état sauvegardé puis relu rend ses gestes")
        FICHIER_ETAT = ancien

    # T11 — la reconstitution : l'état perdu se recomplète des pièces
    with tempfile.TemporaryDirectory() as tmp:
        kit5 = pathlib.Path(tmp)
        receptacle = kit5 / RECEPTACLE
        receptacle.mkdir()
        (receptacle / NOM_TEMOIN).write_text(temoin_signe,
                                             encoding="utf-8")
        console = kit5 / "run-console-unite02-d210-20261118-010101.txt"
        console.write_text(console_echantillon, encoding="utf-8")
        etat_vide = norme_contexte({})
        etat_vide = recompleter_contexte(etat_vide, kit5)
        ctx = etat_vide["contexte"]
        note("T11:l-etat-perdu-reconstitue",
             ctx.get("n_vert") == 2 and ctx.get("n_rouge") == 1
             and ctx.get("temoin_signe") is True
             and "reconstitué" in ctx.get("source", ""),
             "la console et le témoin relus, la source nommée")

    # T12 — le refus de code : la console d'un refus demeure (fail-closed)
    with tempfile.TemporaryDirectory() as tmp:
        kit6 = pathlib.Path(tmp)
        refuseur = kit6 / "refuseur.py"
        refuseur.write_text(
            "print('[T0] REFUS : aucune EMPREINTES*.txt au kit — rien "
            "ne court', flush=True)\nimport sys; sys.exit(2)\n",
            encoding="utf-8")
        try:
            conduire_run(kit6, lambda _s: None,
                         argv=[sys.executable, "refuseur.py"],
                         delai_ligne=0)
            ok12 = False
        except ErreurRun as e:
            ok12 = "A REFUSÉ" in str(e)
        consoles = sorted(kit6.glob("run-console-unite02-d210-*.txt"))
        note("T12:le-refus-nomme-et-la-console-demanuree",
             ok12 and consoles and
             "REFUS" in consoles[-1].read_text(encoding="utf-8"),
             "le refus nommé (code 2), la console vivante couchée")

    verts = sum(1 for _, ok, _ in notes if ok)
    print(f"\nSELFTEST : {verts} VERT, {len(notes) - verts} ROUGE "
          f"sur {len(notes)} contrôles")
    return 0 if verts == len(notes) else 1


# ===========================================================================
# SECTION C — LA GUI (tkinter, import PROTÉGÉ : --selftest reste sans fenêtre)
# ===========================================================================

def demarrer(fumee=False):
    """Bâtit la fenêtre. fumee=True : le mode ÉPREUVE VISUELLE du
    labo (D122) — la fenêtre est bâtie au fil principal SANS mainloop,
    l'application vit à FENETRE_FUMEE (le serveur X virtuel l'inspecte,
    la détruit) ; le terrain ne le voit JAMAIS (le .bat l'appelle sans
    argument)."""
    import queue
    import threading
    import tkinter as tk
    from tkinter import messagebox, scrolledtext, ttk

    STYLE_TITRE = ("TRIADE — le run de " + NOM_RUN + " en un clic")
    LARGEUR = 1180

    class JournalSession:
        """Le journal de session (TRIADE_logs/session-*.txt) — chaque
        geste y vit, renvoyé TEL QUEL si un écran nomme un défaut."""

        def __init__(self):
            DOSSIER_LOGS.mkdir(exist_ok=True)
            self.chemin = DOSSIER_LOGS / ("session-" + horodatage_dossier()
                                          + ".txt")
            self._fh = open(self.chemin, "w", encoding="utf-8")

        def ecrire(self, texte):
            horodatée = dt.datetime.now().strftime("%H:%M:%S") + "  " + texte
            print(horodatée, file=self._fh, flush=True)

    journal = JournalSession()

    class FileAffichage:
        """Le fil des instruments passe par une file (tkinter n'est pas
        thread-safe — JAMAIS un appel tkinter hors le fil principal).
        La file est POMPÉE au fil principal par l'Application
        (pomper_etendu) : elle seule connaît les genres d'affichage."""

        def __init__(self, app):
            self.app = app
            self.queue = queue.Queue()

        def partir(self, fonction, args=()):
            threading.Thread(target=self._fil, args=(fonction, args),
                             daemon=True).start()

        def _fil(self, fonction, args):
            try:
                fonction(*args)
            except ErreurRun as e:
                self.queue.put(("refus", str(e)))
            except Exception as e:
                self.queue.put(("refus", "[ÉCART NOMMÉ] le GUI a chuté : "
                                          + type(e).__name__ + " — " + str(e)
                                          + " ; le journal de session vit à "
                                          + str(DOSSIER_LOGS) + " — renvoyez-le "
                                          "TEL QUEL (D122)"))
            self.queue.put(("fin", None))

    class Application:
        def __init__(self):
            self.racine = tk.Tk()
            self.racine.title(STYLE_TITRE)
            self.file = FileAffichage(self)
            self.etat = norme_contexte(recompleter_contexte(
                charger_etat(), GUI_DIR))
            if self.etat.get("reconstitue"):
                journal.ecrire("[reprise] l'état recomplété : "
                               + self.etat["reconstitue"])
            self.occupe_flag = False
            self.verrou_vert = False
            self._construire()
            self.racine.after(80, self.pomper_etendu)
            self.racine.after(200, self._demarrage_verrou)
            if self.etat["etapes"].get("run") and self.etat["contexte"].get(
                    "console"):
                self.racine.after(400, self._reprise_affichage)
            else:
                # le premier regard : la zone témoin NOMME son attente
                # (jamais une zone muette — la leçon de la fumée Xvfb)
                self.racine.after(400, self._charger_le_temoin)

        # ------------------------------------------------- la construction
        def _construire(self):
            self.racine.geometry("1180x800")
            bandeau = ttk.Frame(self.racine, padding=6)
            bandeau.pack(fill="x")
            # LES BOUTONS D'ABORD à droite (leçon de la fumée Xvfb : le
            # titre long les chassait hors cadre — jamais un bouton
            # invisible au premier regard)
            self.bouton_tout = ttk.Button(
                bandeau, text="TOUT LANCER — le run",
                command=self.tout_lancer, state="disabled")
            self.bouton_tout.pack(side="right")
            self.bouton_rejouer = ttk.Button(
                bandeau, text="REJOUER", command=self.rejouer,
                state="disabled")
            self.bouton_rejouer.pack(side="right", padx=4)
            self.bouton_zip = ttk.Button(
                bandeau, text="ASSEMBLER le zip",
                command=self.assembler_le_zip, state="disabled")
            self.bouton_zip.pack(side="right", padx=4)
            titre = ttk.Label(bandeau,
                              text=("TRIADE — l'unité 01 D210 "
                                    "(loupe-02 lire × bras T)"),
                              font=("TkDefaultFont", 13, "bold"))
            titre.pack(side="left")
            edition = ttk.Label(bandeau,
                                text="GUI v" + VERSION + " — " + EDITION,
                                foreground="#555", wraplength=1100)
            edition.pack(side="left", padx=10, fill="x", expand=True)

            self.statut = tk.StringVar(value="le verrou se recoupe…")
            barre = ttk.Frame(self.racine, padding=(8, 0))
            barre.pack(fill="x")
            ttk.Label(barre, textvariable=self.statut,
                      foreground="#333", wraplength=880).pack(side="left")
            self.etiquette_livraisons = ttk.Label(
                barre, text="", foreground="#555")
            self.etiquette_livraisons.pack(side="right")
            self._rafraichir_livraisons()

            self.carnet = ttk.Notebook(self.racine)
            self.carnet.pack(fill="both", expand=True, padx=8, pady=6)

            # --- 1·VERROU ---
            self.page_verrou = ttk.Frame(self.carnet, padding=8)
            self.carnet.add(self.page_verrou, text="1·VERROU — le kit")
            entete = ttk.Label(
                self.page_verrou,
                text=("LES PIÈCES DU KIT recoupées sha256 par sha256 "
                      "(fail-closed : une divergence, RIEN ne court) — "
                      "l'EMPREINTES-KIT d'origine du 17/11 ET la gravure "
                      "du correctif T0 (EMPREINTES-PIECES-RUN.txt, le "
                      "format que le scénario scellé parse)."),
                wraplength=1080)
            entete.pack(fill="x")
            self.cadre_pieces = ttk.Frame(self.page_verrou)
            self.cadre_pieces.pack(fill="both", expand=True)
            self.lignes_pieces = []
            for i, (rel, _, role) in enumerate(PIECES):
                etiquette = ttk.Label(self.cadre_pieces, text=rel,
                                      font=("TkFixedFont", 9))
                etiquette.grid(row=i, column=0, sticky="w")
                valeur = ttk.Label(self.cadre_pieces, text="…",
                                   font=("TkFixedFont", 9))
                valeur.grid(row=i, column=1, sticky="w", padx=10)
                rolel = ttk.Label(self.cadre_pieces, text=role,
                                 foreground="#555", wraplength=520)
                rolel.grid(row=i, column=2, sticky="w")
                self.lignes_pieces.append((etiquette, valeur))
            self.etiquette_preuve_t0 = ttk.Label(
                self.page_verrou, text="LA PREUVE T0 : …", wraplength=1080,
                foreground="#333")
            self.etiquette_preuve_t0.pack(fill="x", pady=(8, 0))

            # --- 2·RUN ---
            self.page_run = ttk.Frame(self.carnet, padding=8)
            self.carnet.add(self.page_run, text="2·RUN — la console")
            ttk.Label(
                self.page_run,
                text=("LA CONSOLE DU SCÉNARIO (capture complète, écrite "
                      "AU FIL DE L'EAU à run-console-unite02-d210-*.txt — "
                      "UTF-8 des deux côtés, PYTHONIOENCODING posé) ; "
                      "les verdicts RECOPIÉS des lignes, jamais "
                      "recalculés :"), wraplength=1080).pack(fill="x")
            self.console = scrolledtext.ScrolledText(
                self.page_run, height=24, font=("TkFixedFont", 9))
            self.console.pack(fill="both", expand=True)
            self.etiquette_verdicts = ttk.Label(
                self.page_run, text="les verdicts recopiés : (aucun)",
                wraplength=1080)
            self.etiquette_verdicts.pack(fill="x")

            # --- 3·TÉMOIN ---
            self.page_temoin = ttk.Frame(self.carnet, padding=8)
            self.carnet.add(self.page_temoin,
                            text="3·TÉMOIN — D99, votre main")
            ttk.Label(
                self.page_temoin,
                text=("LE VERROU D99 : le GUI ne signe JAMAIS. Le témoin "
                      "naît DU SCÉNARIO (temoin-unite02.txt au réceptacle "
                      "preuves-unite02/) ; dater et signer DE VOTRE MAIN "
                      "(bloc-notes), puis renvoyer le dossier ENTIER au "
                      "coffre /test — le GUI OUVRIRA le coffre au "
                      "navigateur, il n'écrit JAMAIS au Drive."),
                wraplength=1080).pack(fill="x")
            boutons_temoin = ttk.Frame(self.page_temoin)
            boutons_temoin.pack(fill="x", pady=6)
            ttk.Button(boutons_temoin, text="OUVRIR le témoin au "
                        "bloc-notes",
                        command=lambda: self.ouvrir_au_systeme(
                            GUI_DIR / RECEPTACLE / NOM_TEMOIN)).pack(
                                side="left")
            ttk.Button(boutons_temoin, text="OUVRIR le dossier des preuves",
                       command=lambda: self.ouvrir_au_systeme(
                           GUI_DIR / RECEPTACLE)).pack(side="left", padx=6)
            ttk.Button(boutons_temoin, text="OUVRIR le coffre /test au "
                       "navigateur",
                       command=self.ouvrir_coffre).pack(side="left", padx=6)
            self.texte_temoin = scrolledtext.ScrolledText(
                self.page_temoin, height=20, font=("TkFixedFont", 9))
            self.texte_temoin.pack(fill="both", expand=True)

            # --- 4·LIVRE ---
            self.page_livre = ttk.Frame(self.carnet, padding=8)
            self.carnet.add(self.page_livre,
                            text="4·LIVRE — M1, M3, M4 au geste")
            for titre, texte in (
                    ("LA LIGNE DE CARNET M3 (AU GESTE, à votre main — "
                      "jamais automatisée)", LIGNE_CARNET_M3),
                    ("LA LIGNE DE LIVRAISON M1 (livraisons.csv, à votre "
                      "main)", LIGNE_LIVRAISON_M1),
                    ("LA RÈGLE D202 (defauts.csv — les défauts nommés "
                      "AVANT correction)", LIGNE_DEFAUTS_M1),
                    ("LE CHRONO M4 (mesuré au geste ; la référence du "
                      "labo consignée)", M4_LABO)):
                ttk.Label(self.page_livre, text=titre,
                          font=("TkDefaultFont", 10, "bold")).pack(
                              fill="x", pady=(8, 0))
                ttk.Label(self.page_livre, text=texte, wraplength=1080,
                          foreground="#333").pack(fill="x")
            self.etiquette_cap = ttk.Label(
                self.page_livre, text="", wraplength=1080)
            self.etiquette_cap.pack(fill="x", pady=(8, 0))
            self._rafraichir_cap()

            # --- 5·JOURNAL ---
            self.page_journal = ttk.Frame(self.carnet, padding=8)
            self.carnet.add(self.page_journal, text="5·JOURNAL — session")
            self.texte_journal = scrolledtext.ScrolledText(
                self.page_journal, height=26, font=("TkFixedFont", 9))
            self.texte_journal.pack(fill="both", expand=True)

        # ---------------------------------------------------- les affichages
        def console_insert(self, texte):
            self.console.insert("end", texte + "\n")
            self.console.see("end")
            journal.ecrire(texte)

        def journal_insert(self, texte):
            self.texte_journal.insert("end", texte + "\n")
            self.texte_journal.see("end")

        def etape_statut(self, cle, etat_txt, detail=""):
            self.statut.set(cle + " : " + etat_txt
                            + ((" — " + detail) if detail else ""))
            journal.ecrire("[" + cle + "] " + etat_txt
                           + ((" — " + detail) if detail else ""))
            self.journal_insert("[" + maintenant_local() + "] "
                                 + cle + " : " + etat_txt
                                 + ((" — " + detail) if detail else ""))

        def verdict_ajouter(self, ligne_verdict):
            actuel = self.etiquette_verdicts.cget("text")
            if actuel.startswith("les verdicts recopiés : (aucun)"):
                actuel = "les verdicts recopiés :"
            self.etiquette_verdicts.config(
                text=actuel + "\n  " + ligne_verdict, wraplength=880)

        def occupe(self, flag):
            self.occupe_flag = flag
            self._rafraichir_boutons()

        def _rafraichir_boutons(self):
            pret = (not self.occupe_flag) and self.verrou_vert
            self.bouton_tout.config(state="normal" if pret else "disabled")
            self.bouton_rejouer.config(
                state="normal" if pret else "disabled")
            pret_zip = (not self.occupe_flag) and bool(
                self.etat["etapes"].get("run"))
            self.bouton_zip.config(
                state="normal" if pret_zip else "disabled")

        def refus_nomme(self, message):
            self.occupe(False)
            self.etape_statut("REFUS NOMMÉ", "le GUI s'arrête", "")
            self.console_insert("[REFUS NOMMÉ] " + message)
            journal.ecrire("[REFUS NOMMÉ] " + message)
            messagebox.showerror(
                "TRIADE — le refus nommé", message)

        def _rafraichir_livraisons(self):
            n = self.etat.get("livraisons", 0)
            self.etiquette_livraisons.config(
                text="livraisons M1 assemblées par ce GUI : "
                + str(n) + "/" + str(CAP_LIVRAISONS_BLOC))

        def _rafraichir_cap(self):
            self.etiquette_cap.config(
                text="LA CAP M1 (§ 7) : TROIS livraisons par bloc, DOUZE "
                "par application — le GUI compte "
                + str(self.etat.get("livraisons", 0))
                + " assemblage(s) ; le refus au-delà est NOMMÉ. Le "
                "rejouage d'une unité verte n'est PAS une livraison "
                "(§ 7) — le livre décide ce qui compte (D202).")

        # ---------------------------------------------------- les gestes
        def ouvrir_au_systeme(self, chemin):
            chemin = pathlib.Path(chemin)
            if not chemin.exists():
                messagebox.showinfo(
                    "TRIADE", "la pièce n'existe pas encore : "
                    + str(chemin) + " (le geste qui la naît doit d'abord "
                    "courir)")
                return
            try:
                if sys.platform == "win32":
                    os.startfile(str(chemin))  # noqa: S321 (le geste GUI)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", str(chemin)])
                else:
                    subprocess.Popen(["xdg-open", str(chemin)])
            except Exception as e:
                messagebox.showinfo(
                    "TRIADE", "l'ouverture a échoué ("
                    + type(e).__name__ + ") — la pièce vit à "
                    + str(chemin))

        def ouvrir_coffre(self):
            try:
                import webbrowser
                webbrowser.open(COFFRE_TEST_URL)
                journal.ecrire("[coffre] le /test ouvert au navigateur "
                               "(le GUI n'écrit JAMAIS au Drive)")
            except Exception as e:
                messagebox.showinfo(
                    "TRIADE", "le navigateur a refusé ("
                    + type(e).__name__ + ") — le coffre vit à "
                    + COFFRE_TEST_URL)

        def _demarrage_verrou(self):
            self.file.partir(self._verifier_le_verrou)

        def _verifier_le_verrou(self):
            resultats = verifier_pieces(GUI_DIR)
            verts = 0
            for (rel, _, _), r in zip(PIECES, resultats):
                idx = [p for p, _, _ in PIECES].index(rel)
                etiquette, valeur = self.lignes_pieces[idx]
                couleur = "#0a7d32" if r["vert"] else "#b00020"
                self.file.queue.put((
                    "etape", ("verrou:" + rel,
                              "VERT" if r["vert"] else "ROUGE",
                              r["message"])))
                # l'affichage de la ligne (par la file, fil principal)
                self.file.queue.put((
                    "ligne_verrou", (idx, couleur, r["calcule"])))
                verts += 1 if r["vert"] else 0
            n, vert_t0, message = voir_pieces_du_scenario(GUI_DIR)
            self.file.queue.put(("preuve_t0", (n, vert_t0, message)))
            self.verrou_vert = all(r["vert"] for r in resultats) and vert_t0
            if self.verrou_vert:
                self.file.queue.put((
                    "etape", ("verrou", "VERT",
                              f"{verts}/{len(PIECES)} pièces + la preuve T0 "
                              f"({n} pièces vues par le scénario scellé)")))
                self.file.queue.put(("verrou_vert", None))
            else:
                self.file.queue.put((
                    "etape", ("verrou", "ROUGE",
                              "une divergence — RIEN ne court "
                              "(fail-closed) ; ne modifiez RIEN, "
                              "renvoyez le journal de session TEL QUE "
                              "QUEL")))

        def _geste_run(self, argv=None):
            contexte = conduire_run(GUI_DIR, lambda s: self.file.queue.put(
                ("ligne", s)), argv=argv)
            self.etat["etapes"]["run"] = True
            self.etat["contexte"] = contexte
            sauver_etat(self.etat)
            self.file.queue.put(("etape", ("run", "FINI",
                                          str(contexte["n_vert"])
                                          + " VERT, "
                                          + str(contexte["n_rouge"])
                                          + " ROUGE recopiés (code "
                                          + str(contexte["code"]) + ")")))
            self.file.queue.put(("apres_run", contexte))

        def _geste_collecte(self, contexte):
            depot, pieces = collecter(GUI_DIR, contexte,
                                      lambda s: self.file.queue.put(
                                          ("ligne", s)))
            self.etat["etapes"]["collecte"] = True
            self.etat["contexte"] = contexte
            sauver_etat(self.etat)
            self.file.queue.put(("apres_collecte", (depot, pieces)))

        def tout_lancer(self):
            if self.occupe_flag:
                return
            if not getattr(self, "verrou_vert", False):
                messagebox.showinfo(
                    "TRIADE", "le verrou n'est pas VERT — le GUI refuse "
                    "de lancer (fail-closed)")
                return
            self.occupe(True)
            self.console.delete("1.0", "end")
            self.etape_statut("TOUT LANCER", "parti",
                              "le verrou → le run → la collecte → le témoin")
            self.console_insert("=== TOUT LANCER — " + maintenant_local()
                                + " : le verrou recoupé, le run part, la "
                                "collecte suivra, le témoin est à VOTRE "
                                "MAIN (D99) ===")

            def travail():
                self._geste_run()
                self._geste_collecte(self.etat["contexte"])

            self.file.partir(travail)

        def rejouer(self):
            if self.occupe_flag:
                return
            if not getattr(self, "verrou_vert", False):
                messagebox.showinfo(
                    "TRIADE", "le verrou n'est pas VERT — le GUI refuse "
                    "de lancer (fail-closed)")
                return
            self.occupe(True)
            self.etape_statut("REJOUAGE", "parti",
                              "le rejeu diagnostic — le rejouage d'une "
                              "unité verte n'est PAS une livraison (§ 7)")
            self.file.partir(self._geste_run)

        def assembler_le_zip(self):
            if self.occupe_flag:
                return
            try:
                chemin_zip, n = assembler_zip(
                    GUI_DIR, livraisons_deja=self.etat.get("livraisons", 0))
            except ErreurRun as e:
                self.refus_nomme(str(e))
                return
            self.etat["livraisons"] = n
            sauver_etat(self.etat)
            self.etape_statut("RENVOI", "le zip assemblé",
                              chemin_zip.name + " — la livraison comptée "
                              + str(n) + "/" + str(CAP_LIVRAISONS_BLOC))
            self._rafraichir_livraisons()
            self._rafraichir_cap()
            messagebox.showinfo(
                "TRIADE — le zip de renvoi assemblé",
                "le zip vit au kit :\n\n  " + chemin_zip.name
                + "\n\nrenvoyez-le au coffre /test (l'onglet 3·TÉMOIN "
                "ouvre le coffre au navigateur — le GUI n'écrit JAMAIS "
                "au Drive).\n\nLa cap M1 : TROIS livraisons par bloc — "
                "comptées : " + str(n) + ".")

        # ---------------------------------------------- les retours du fil
        def _apres_run(self, contexte):
            self.etiquette_verdicts.config(
                text="les verdicts recopiés : "
                + str(contexte["n_vert"]) + " VERT, "
                + str(contexte["n_rouge"]) + " ROUGE (RECOPIÉS des "
                "lignes de console, jamais recalculés)")
            for vert, texte in contexte.get("verdicts", []):
                self.verdict_ajouter(("[VERT] " if vert else "[ROUGE] ")
                                     + texte)
            if contexte.get("n_rouge"):
                self.statut.set("le run FINI — "
                                + str(contexte["n_vert"]) + " VERT, "
                                + str(contexte["n_rouge"]) + " ROUGE : "
                                "LES DÉFAUTS SE NOMMENT AVANT CORRECTION "
                                "(D202) — le renvoi du dossier ENTIER "
                                "demeure (l'onglet 3·TÉMOIN)")
            self._charger_le_temoin()

        def _apres_collecte(self, depot, pieces):
            self.etape_statut("COLLECTE", "née",
                              depot.name + " au réceptacle ("
                              + str(len(pieces)) + " pièces)")
            self._charger_le_temoin()
            self._rafraichir_boutons()

        def _charger_le_temoin(self):
            texte, chemin = lire_temoin(GUI_DIR)
            self.texte_temoin.delete("1.0", "end")
            if texte is None:
                self.texte_temoin.insert(
                    "end", "(le témoin n'est pas encore né — le run "
                    "doit d'abord finir : TOUT LANCER)")
                return
            self.texte_temoin.insert("end", texte)
            signe = temoin_est_signe(texte)
            self.etape_statut(
                "TÉMOIN", "né" + (" et DATÉ-SIGNÉ de votre main"
                                  if signe else " — PAS ENCORE daté-signé "
                                  "(votre main, D99)"),
                str(chemin))
            self._rafraichir_boutons()

        def _reprise_affichage(self):
            """La reprise : la console du run précédent affichée de """
            """nouveau (RELUE, jamais réinventée), le témoin rechargé."""
            console = self.etat["contexte"].get("console")
            if console and pathlib.Path(console).exists():
                self.console.insert(
                    "end", pathlib.Path(console).read_text(
                        encoding="utf-8", errors="replace") + "\n")
                self.console.see("end")
                ctx = self.etat["contexte"]
                self.etiquette_verdicts.config(
                    text="les verdicts recopiés : " + str(ctx.get("n_vert"))
                    + " VERT, " + str(ctx.get("n_rouge"))
                    + " ROUGE (RECOPIÉS, la reprise relit la console)")
            self._charger_le_temoin()
            journal.ecrire("[reprise] la console du run précédent "
                           "affichée de nouveau")

        # ------------------------------------------------------- le fil des
        # événements de la file (étendus : ligne_verrou, preuve_t0, …)
        def pomper_etendu(self):
            traite = False
            try:
                while True:
                    genre, charge = self.file.queue.get_nowait()
                    if genre == "ligne":
                        self.console_insert(charge)
                    elif genre == "etape":
                        self.etape_statut(*charge)
                    elif genre == "verdict":
                        self.verdict_ajouter(charge)
                    elif genre == "refus":
                        self.refus_nomme(charge)
                    elif genre == "ligne_verrou":
                        idx, couleur, calcule = charge
                        etiquette, valeur = self.lignes_pieces[idx]
                        if calcule:
                            texte_ligne = ("sha256 " + calcule[:20] + "…")
                        else:
                            texte_ligne = "PIÈCE ABSENTE"
                        valeur.config(text=texte_ligne, foreground=couleur)
                    elif genre == "preuve_t0":
                        n, vert_t0, message = charge
                        self.etiquette_preuve_t0.config(
                            text=("LA PREUVE T0 : " + message
                                  + (" — VERT" if vert_t0 else " — ROUGE")),
                            foreground=("#0a7d32" if vert_t0 else "#b00020"))
                    elif genre == "verrou_vert":
                        self.verrou_vert = True
                        self._rafraichir_boutons()
                        self.etape_statut(
                            "VERROU", "VERT",
                            "le kit recoupé — TOUT LANCER attend votre clic")
                    elif genre == "apres_run":
                        self.occupe(False)
                        self._apres_run(charge)
                    elif genre == "apres_collecte":
                        self.occupe(False)
                        self._apres_collecte(*charge)
                    elif genre == "fin":
                        self.occupe(False)
                    traite = True
            except queue.Empty:
                pass
            self.racine.after(80, self.pomper_etendu)

    app = Application()
    journal.ecrire("[GUI] la fenêtre née — v" + VERSION + ", " + EDITION)
    journal.ecrire("[GUI] le kit : " + str(GUI_DIR))
    if fumee:
        global FENETRE_FUMEE
        FENETRE_FUMEE = app
        return app
    app.racine.mainloop()
    journal.ecrire("[GUI] la fenêtre fermée")
    journal._fh.close()
    return 0


FENETRE_FUMEE = None


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(demarrer())
