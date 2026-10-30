#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_autotest_cf3_gui.py — D122 : la falsifiabilité du PUPITRE
d'autotest CF3.

Une garde qui ne rejette rien ne garde rien (leçon M3). Le pupitre
(v06/autotest_cf3_gui.py) est un HABIT relais : ce qui doit être prouvé,
c'est son contrôleur — ce qu'il lance, ce qu'il compte, ce qu'il refuse,
ce que son rapport emporte. Cette suite l'attaque :

  X1  import headless (aucune fenêtre créée) + selftest embarqué vert ;
  X2  cohérence des attributs (régression D109, la méthode maison) : AST —
      tout self.X lu dans les classes Journal/Application (imbriquées
      dans demarrer_gui) existe (assigné ou méthode), et demarrer_gui
      ne référence que du réel — le bogue original appelait app.mainloop()
      alors que le Tk vit dans app.racine ;
  X3  le relais sous-processus : l'autotest embarqué rend « 28 PASS /
      0 ÉCHEC » COMPTÉ DEPUIS LE FLUX, la suite complète rend
      « 90 PASS / 0 ÉCHEC », une cible absente est un refus NOMMÉ, et
      l'enfant reçoit PYTHONIOENCODING=utf-8 (les accents des verdicts
      survivent au cp850 de Windows — prouvé par un enfant témoin qui
      imprime son environnement) ;
  X4  le verdict est CROISÉ flux/code : un enfant menteur qui imprime
      « 28 PASS / 0 ÉCHEC » mais sort 1 est ROUGE (la composition
      code==0 ET échecs==0 est testée telle quelle) ; le compteur garde
      le DERNIER verdict, tolère ECHEC sans accent, rend None sans
      verdict ;
  X5  le rapport : emporte l'entête, l'empreinte md5 de coffre_cf3, le
      journal d'écran témoin ET la boîte noire ; ne contient AUCUN
      chemin de coffre réel (ni .keys ni coffre_fort.bin — le pupitre
      n'y touche jamais, la preuve est dans son rapport) ; la
      troncature à 3000 lignes vit (garde-fou du récent suffit) ;
  X6  la posture : suite_disponible() est VRAI en dossier v06/ (dépôt)
      et FAUX en copie plate (refus nommé AVANT lancement) ; _resoudre_v06
      refuse un chemin inexistant (SystemExit nommé) et accepte un
      dossier réel ;
  X7  la boîte noire est un TÉMOIN, pas une dépendance : chemin
      impossible → Enregistreur muet, AUCUNE exception ;
  X8  posture KIT en sous-processus : un kit minimal (copie PLATE :
      pupitre + coffre_cf3.py + coffre_cf2.py) rend selftest 18 PASS ;
      un kit v06/ complet (avec __init__.py) rend AUSSI la suite
      disponible — les DEUX postures du terrain ;
  L   les lanceurs : lancer_autotest_cf3.sh EXÉCUTÉ dans les deux
      postures (dépôt : v06/ d'abord ; kit plat : repli sur la copie
      à côté) + refus nommé sans cible ; lancer_autotest_cf3.bat
      prouvé par CONTENU (replis + pause — Windows ne court pas ici,
      la preuve structurelle est la seule possible et elle est dite).

AUCUN coffre réel n'est touché : tout vit en temporaires. Le dépôt réel
n'est pas modifié (les lanceurs sont exécutés en LECTURE, leur échec ne
réécrit rien).
"""

import ast
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)
from v06 import autotest_cf3_gui as P                      # noqa: E402

V06 = os.path.dirname(os.path.abspath(P.__file__))
EMPLACEMENT_LANCEURS = RACINE

RESULTATS = []


def _verifie(temoin: str, condition: bool, detail: str = "") -> None:
    RESULTATS.append((temoin, bool(condition)))
    print(f"[test-pupitre] {temoin} : {'PASS' if condition else 'ECHEC'}"
          + (f" — {detail}" if detail and not condition else ""))


def _md5(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def _copier(source: str, cible: str) -> None:
    shutil.copyfile(source, cible)


# ---------------------------------------------------------------------------
# X1 — import headless + selftest embarqué vert
# ---------------------------------------------------------------------------

def x1_import_headless():
    # l'import a déjà eu lieu en tête de module SANS créer de fenêtre :
    # tkinter est importé PROTÉGÉ (drapeau), et le tk.Tk() ne vit QUE
    # dans demarrer_gui — preuve structurelle par AST
    _verifie("x1-import-headless-avec-drapeau",
             hasattr(P, "VERSION_PUPITRE") and P.TKINTER_DISPONIBLE)
    with open(os.path.abspath(P.__file__), "r", encoding="utf-8") as f:
        arbre = ast.parse(f.read())

    def dans_demarrer_gui(noeud):
        for parent in ast.walk(arbre):
            if isinstance(parent, ast.FunctionDef) \
                    and parent.name == "demarrer_gui" \
                    and noeud in ast.walk(parent):
                return True
        return False

    appels_tk = [n for n in ast.walk(arbre)
                 if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Attribute)
                 and n.func.attr == "Tk"]
    _verifie("x1-tk-ne-vit-que-dans-demarrer-gui",
             appels_tk and all(dans_demarrer_gui(n) for n in appels_tk))
    ok = P.selftest()
    _verifie("x1-selftest-embarque-vert", ok)


# ---------------------------------------------------------------------------
# X2 — cohérence des attributs (AST, régression D109)
# ---------------------------------------------------------------------------

def x2_coherence_attributs():
    with open(os.path.abspath(P.__file__), "r", encoding="utf-8") as f:
        arbre = ast.parse(f.read())

    classes = {n.name: n for n in ast.walk(arbre)
               if isinstance(n, ast.ClassDef)
               and n.name in ("Journal", "Application")}

    def attributs_definis(classe):
        definis = set()
        for noeud in ast.walk(classe):
            if isinstance(noeud, ast.FunctionDef):
                definis.add(noeud.name)
            if isinstance(noeud, ast.Assign):
                for cible in noeud.targets:
                    if (isinstance(cible, ast.Attribute)
                            and isinstance(cible.value, ast.Name)
                            and cible.value.id == "self"):
                        definis.add(cible.attr)
        return definis

    def attributs_lus(classe):
        lus = set()
        for noeud in ast.walk(classe):
            if isinstance(noeud, ast.Attribute) \
                    and isinstance(noeud.value, ast.Name) \
                    and noeud.value.id == "self":
                lus.add(noeud.attr)
        return lus

    for nom, classe in classes.items():
        manquants = attributs_lus(classe) - attributs_definis(classe)
        _verifie(f"x2-attributs-coherents-{nom.lower()}",
                 not manquants, f"manquants : {sorted(manquants)}")

    # demarrer_gui ne référence que du réel : aucun app.<attr> hors
    # attributs de la classe Application (le bogue D109 était
    # app.mainloop())
    definis_app = attributs_definis(classes["Application"])
    references_app = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Attribute) \
                and isinstance(noeud.value, ast.Name) \
                and noeud.value.id == "app":
            references_app.add(noeud.attr)
    _verifie("x2-demarrer-gui-ne-reference-que-du-reel",
             not (references_app - definis_app),
             f"références mortes : {sorted(references_app - definis_app)}")


# ---------------------------------------------------------------------------
# X3 — le relais sous-processus
# ---------------------------------------------------------------------------

def x3_relais_sous_processus():
    # l'autotest embarqué, avec SON argument, compté DU FLUX
    relais = P.RelaisEssais()
    lignes = relais.lancer(P.chemin_cible("coffre_cf3.py"), ["autotest"])
    _verifie("x3-relais-autotest-code-0", relais.code == 0)
    _verifie("x3-relais-autotest-28-pass-du-flux",
             P.compter_verdict(lignes) == (28, 0))

    # la suite complète, par le MÊME relais (le bouton du pupitre)
    relais_suite = P.RelaisEssais()
    lignes_suite = relais_suite.lancer(P.chemin_cible("test_coffre_cf3.py"))
    _verifie("x3-relais-suite-code-0", relais_suite.code == 0)
    _verifie("x3-relais-suite-90-pass-du-flux",
             P.compter_verdict(lignes_suite) == (90, 0))

    # cible absente : refus NOMMÉ (aucune ligne, code None)
    relais_fantome = P.RelaisEssais()
    lignes_fantome = relais_fantome.lancer(
        os.path.join(V06, "module-fantome.py"))
    _verifie("x3-relais-cible-absente-refus-nomme",
             lignes_fantome == [] and relais_fantome.code is None
             and "introuvable" in str(relais_fantome.erreur))

    # PYTHONIOENCODING=utf-8 passé à l'enfant : un témoin l'imprime
    bac = tempfile.mkdtemp(prefix="pupitre-x3-")
    try:
        temoin = os.path.join(bac, "temoin_env.py")
        with open(temoin, "w", encoding="utf-8") as f:
            f.write("import os\n"
                    "print('ENV=' + "
                    "str(os.environ.get('PYTHONIOENCODING')))\n")
        relais_env = P.RelaisEssais()
        lignes_env = relais_env.lancer(temoin)
        _verifie("x3-enfant-recoit-pythonioencoding-utf8",
                 any("ENV=utf-8" in ligne for ligne in lignes_env))
    finally:
        shutil.rmtree(bac, ignore_errors=True)


# ---------------------------------------------------------------------------
# X4 — le verdict est CROISÉ flux / code de sortie
# ---------------------------------------------------------------------------

def _enfant(bac: str, nom: str, corps: str) -> str:
    chemin = os.path.join(bac, nom)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(corps)
    return chemin


def x4_verdict_croise():
    bac = tempfile.mkdtemp(prefix="pupitre-x4-")
    try:
        # menteur : imprime 28 PASS / 0 ÉCHEC mais sort 1 → la COMPOSITION
        # du pupitre (code == 0 ET échecs == 0) rend ROUGE
        menteur = _enfant(bac, "menteur.py",
                          "print('[x] 28 PASS / 0 ÉCHEC')\n"
                          "raise SystemExit(1)\n")
        relais = P.RelaisEssais()
        lignes = relais.lancer(menteur)
        passes, echecs = P.compter_verdict(lignes)
        vert = (relais.code == 0 and echecs == 0)
        _verifie("x4-enfant-menteur-code-1-rouge",
                 passes == 28 and not vert)

        # avouant : 3 PASS / 2 ECHEC (sans accent) et sort 1 → ROUGE
        avouant = _enfant(bac, "avouant.py",
                          "print('[x] 3 PASS / 2 ECHEC')\n"
                          "raise SystemExit(1)\n")
        relais2 = P.RelaisEssais()
        lignes2 = relais2.lancer(avouant)
        comptes = P.compter_verdict(lignes2)
        _verifie("x4-enfant-avouant-echec-sans-accent-rouge",
                 comptes == (3, 2)
                 and not (relais2.code == 0 and comptes[1] == 0))

        # muet : aucun verdict → None (état NOMMÉ côté pupitre)
        muet = _enfant(bac, "muet.py", "print('je ne verdict pas')\n")
        relais3 = P.RelaisEssais()
        lignes3 = relais3.lancer(muet)
        _verifie("x4-enfant-muet-sans-verdict-none",
                 P.compter_verdict(lignes3) is None)
    finally:
        shutil.rmtree(bac, ignore_errors=True)

    # le compteur : le DERNIER verdict gagne
    _verifie("x4-compteur-dernier-verdict",
             P.compter_verdict(["[x] 1 PASS / 0 ÉCHEC",
                                "[x] 5 PASS / 2 ÉCHEC"]) == (5, 2))


# ---------------------------------------------------------------------------
# X5 — le rapport : tout emporté, rien de réel touché
# ---------------------------------------------------------------------------

def x5_rapport():
    import secrets
    temoin_ecran = "temoin-ecran-" + secrets.token_hex(8)
    rapport = P.constituer_rapport_complet(temoin_ecran)

    with open(P.chemin_cible("coffre_cf3.py"), "rb") as f:
        md5_cf3 = hashlib.md5(f.read()).hexdigest()
    _verifie("x5-rapport-emporte-version-et-sections",
             "RAPPORT D'AUTOTEST CF3" in rapport
             and P.VERSION_PUPITRE in rapport
             and "JOURNAL D'ÉCRAN" in rapport
             and "JOURNAL DE VOL" in rapport)
    _verifie("x5-rapport-emporte-empreinte-coffre-cf3", md5_cf3 in rapport)
    _verifie("x5-rapport-emporte-temoin-ecran", temoin_ecran in rapport)
    _verifie("x5-rapport-emporte-boite-noire",
             "autotest-cf3-journal.log" in rapport)

    # le pupitre ne touche JAMAIS les coffres réels : son rapport ne
    # porte NI chemin .keys NI conteneur réel
    _verifie("x5-rapport-sans-chemin-de-coffre-reel",
             ".keys" not in rapport and "coffre_fort.bin" not in rapport)

    # la troncature à 3000 lignes vit : boîte noire factice de 3100
    # lignes → le rapport le DIT (garde-fou : le récent suffit)
    bac = tempfile.mkdtemp(prefix="pupitre-x5-")
    try:
        faux_journal = os.path.join(bac, "faux-journal.log")
        with open(faux_journal, "w", encoding="utf-8") as f:
            for i in range(3100):
                f.write(f"ligne factice {i}\n")
        chemin_reel = P.CHEMIN_JOURNAL_VOL
        P.CHEMIN_JOURNAL_VOL = faux_journal
        try:
            rapport_tronque = P.constituer_rapport_complet("écran")
        finally:
            P.CHEMIN_JOURNAL_VOL = chemin_reel   # restauration immédiate
        _verifie("x5-rapport-tronque-apres-3000-lignes",
                 "tronquées" in rapport_tronque
                 and "ligne factice 3099" in rapport_tronque
                 and "ligne factice 0\n" not in rapport_tronque)
    finally:
        shutil.rmtree(bac, ignore_errors=True)


# ---------------------------------------------------------------------------
# X6 — la posture (dépôt / kit v06 / copie plate) et _resoudre_v06
# ---------------------------------------------------------------------------

def x6_posture():
    # ici (dépôt complet) : suite disponible
    _verifie("x6-posture-depot-suite-disponible", P.suite_disponible())

    # copie plate : PAS de __init__.py → refus nommé AVANT lancement
    bac = tempfile.mkdtemp(prefix="pupitre-x6-")
    try:
        for nom in ("autotest_cf3_gui.py", "coffre_cf3.py", "coffre_cf2.py"):
            _copier(P.chemin_cible(nom), os.path.join(bac, nom))
        chemin_reel = P.CHEMIN_V06
        P.CHEMIN_V06 = bac
        try:
            plat = P.suite_disponible()
        finally:
            P.CHEMIN_V06 = chemin_reel   # restauration immédiate
        _verifie("x6-posture-copie-plate-suite-refusee", not plat)

        # copie plate AVEC dossier v06/ complet (kit du Drive) : suite
        # disponible — les DEUX postures du kit, tranchées par la garde
        kit = os.path.join(bac, "kit", "v06")
        os.makedirs(kit)
        for nom in ("autotest_cf3_gui.py", "coffre_cf3.py",
                    "coffre_cf2.py", "test_coffre_cf3.py", "__init__.py"):
            source = P.chemin_cible(nom)
            if os.path.isfile(source):
                _copier(source, os.path.join(kit, nom))
        P.CHEMIN_V06 = kit
        try:
            kit_v06 = P.suite_disponible()
        finally:
            P.CHEMIN_V06 = chemin_reel
        _verifie("x6-posture-kit-v06-suite-disponible", kit_v06)

        # _resoudre_v06 : chemin inexistant → SystemExit NOMMÉ ;
        # chemin réel → abspath
        try:
            P._resoudre_v06(os.path.join(bac, "nimporte", "quoi"))
            refuse = False
        except SystemExit as exc:
            refuse = "n'existe pas" in str(exc)
        _verifie("x6-resoudre-v06-refuse-chemin-fantome", refuse)
        _verifie("x6-resoudre-v06-accepte-dossier-reel",
                 P._resoudre_v06(bac) == os.path.abspath(bac))
    finally:
        shutil.rmtree(bac, ignore_errors=True)


# ---------------------------------------------------------------------------
# X7 — la boîte noire : un témoin, pas une dépendance
# ---------------------------------------------------------------------------

def x7_boite_noire():
    # chemin impossible : Enregistreur MUET, aucune exception
    chemin_impossible = os.path.join(
        tempfile.gettempdir(), "dossier-qui-nexiste-pas-d122", "journal.log")
    enregistreur = P.Enregistreur(chemin_impossible)
    try:
        enregistreur.ligne("ceci ne doit pas lever", "info")
        enregistreur.traceback()
        muet = True
    except Exception:
        muet = False
    _verifie("x7-boite-noire-chemin-impossible-muet", muet
             and enregistreur.fichier is None)

    # chemin réel : écrit et restitue, horodaté
    bac = tempfile.mkdtemp(prefix="pupitre-x7-")
    try:
        chemin = os.path.join(bac, "journal.log")
        enregistreur2 = P.Enregistreur(chemin)
        enregistreur2.ligne("fait-temoin-d122", "info")
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
        _verifie("x7-boite-noire-ecrit-horodate",
                 "fait-temoin-d122" in contenu
                 and "[" in contenu and "]" in contenu)
    finally:
        shutil.rmtree(bac, ignore_errors=True)


# ---------------------------------------------------------------------------
# X8 — posture KIT en sous-processus (le terrain sans le dépôt)
# ---------------------------------------------------------------------------

def x8_posture_kit_sous_processus():
    bac = tempfile.mkdtemp(prefix="pupitre-x8-")
    try:
        # kit PLAT : pupitre + coffre_cf3 + coffre_cf2 à côté d'un lanceur
        plat = os.path.join(bac, "kit-plat")
        os.makedirs(plat)
        for nom in ("autotest_cf3_gui.py", "coffre_cf3.py", "coffre_cf2.py"):
            _copier(P.chemin_cible(nom), os.path.join(plat, nom))
        sortie = subprocess.run(
            [sys.executable, "autotest_cf3_gui.py", "--selftest"],
            cwd=plat, capture_output=True, text=True, timeout=180,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        _verifie("x8-kit-plat-selftest-vert",
                 sortie.returncode == 0
                 and "18 PASS / 0 ÉCHEC" in sortie.stdout,
                 sortie.stdout[-300:] if sortie.returncode else "")

        # kit v06/ complet : la suite de falsifiabilité CF3 tourne DEPUIS
        # le kit (from v06 import … — c'est la posture du Drive)
        kit = os.path.join(bac, "kit-drive", "v06")
        os.makedirs(kit)
        for nom in ("autotest_cf3_gui.py", "coffre_cf3.py", "coffre_cf2.py",
                    "test_coffre_cf3.py", "__init__.py"):
            source = P.chemin_cible(nom)
            if os.path.isfile(source):
                _copier(source, os.path.join(kit, nom))
        sortie2 = subprocess.run(
            [sys.executable, "autotest_cf3_gui.py", "--selftest"],
            cwd=kit, capture_output=True, text=True, timeout=180,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        _verifie("x8-kit-v06-selftest-vert",
                 sortie2.returncode == 0
                 and "18 PASS / 0 ÉCHEC" in sortie2.stdout)
        sortie3 = subprocess.run(
            [sys.executable, "test_coffre_cf3.py"],
            cwd=kit, capture_output=True, text=True, timeout=300,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        _verifie("x8-kit-v06-suite-cf3-90-pass",
                 sortie3.returncode == 0
                 and "90 PASS / 0 ÉCHEC" in sortie3.stdout)
    finally:
        shutil.rmtree(bac, ignore_errors=True)


# ---------------------------------------------------------------------------
# L — les lanceurs (D122 : mêmes conventions que lancer_ceremonie D118)
# ---------------------------------------------------------------------------

def l_lanceurs():
    lanceur_sh = os.path.join(EMPLACEMENT_LANCEURS, "lancer_autotest_cf3.sh")
    lanceur_bat = os.path.join(EMPLACEMENT_LANCEURS, "lancer_autotest_cf3.bat")
    _verifie("l-lanceurs-present-au-depot",
             os.path.isfile(lanceur_sh) and os.path.isfile(lanceur_bat))

    # L1 — posture dépôt : le lanceur trouve v06/autotest_cf3_gui.py
    if os.path.isfile(lanceur_sh) and os.name == "posix":
        sortie = subprocess.run(
            ["sh", lanceur_sh, "--selftest"],
            cwd=EMPLACEMENT_LANCEURS, capture_output=True, text=True,
            timeout=240,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        _verifie("l1-lanceur-sh-depot-selftest-vert",
                 sortie.returncode == 0
                 and "18 PASS / 0 ÉCHEC" in sortie.stdout)

        # L2 — posture kit PLAT : repli sur la copie à côté du lanceur
        bac = tempfile.mkdtemp(prefix="pupitre-l2-")
        try:
            _copier(lanceur_sh, os.path.join(bac, "lancer_autotest_cf3.sh"))
            for nom in ("autotest_cf3_gui.py", "coffre_cf3.py",
                        "coffre_cf2.py"):
                _copier(P.chemin_cible(nom), os.path.join(bac, nom))
            sortie2 = subprocess.run(
                ["sh", os.path.join(bac, "lancer_autotest_cf3.sh"),
                 "--selftest"],
                cwd=bac, capture_output=True, text=True, timeout=240,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            _verifie("l2-lanceur-sh-kit-plat-repli-vert",
                     sortie2.returncode == 0
                     and "18 PASS / 0 ÉCHEC" in sortie2.stdout)

            # L3 — sans cible : refus NOMMÉ, code 1
            vide = tempfile.mkdtemp(prefix="pupitre-l3-")
            try:
                _copier(lanceur_sh,
                        os.path.join(vide, "lancer_autotest_cf3.sh"))
                sortie3 = subprocess.run(
                    ["sh", os.path.join(vide, "lancer_autotest_cf3.sh")],
                    cwd=vide, capture_output=True, text=True, timeout=60)
                _verifie("l3-lanceur-sh-sans-cible-refus-nomme",
                         sortie3.returncode == 1
                         and "introuvable" in sortie3.stdout)
            finally:
                shutil.rmtree(vide, ignore_errors=True)
        finally:
            shutil.rmtree(bac, ignore_errors=True)

    # L4 — le .bat par CONTENU (Windows ne court pas ici) : l'ordre de
    # recherche v06\ d'abord puis repli, et la pause sur échec
    if os.path.isfile(lanceur_bat):
        with open(lanceur_bat, "r", encoding="utf-8", errors="replace") as f:
            contenu = f.read()
        _verifie("l4-lanceur-bat-structure-preuve-par-contenu",
                 "v06\\autotest_cf3_gui.py" in contenu
                 and "autotest_cf3_gui.py" in contenu
                 and "pause" in contenu.lower())


# ---------------------------------------------------------------------------

def main() -> int:
    print("[test-pupitre] falsifiabilité D122 — le pupitre d'autotest CF3")
    groupes = [x1_import_headless, x2_coherence_attributs,
               x3_relais_sous_processus, x4_verdict_croise, x5_rapport,
               x6_posture, x7_boite_noire, x8_posture_kit_sous_processus,
               l_lanceurs]
    for groupe in groupes:
        print(f"\n[test-pupitre] --- {groupe.__name__} ---")
        groupe()
    echecs = [temoin for temoin, ok in RESULTATS if not ok]
    print(f"\n[test-pupitre] {len(RESULTATS) - len(echecs)} PASS / "
          f"{len(echecs)} ÉCHEC")
    if echecs:
        for temoin in echecs:
            print(f"[test-pupitre] ÉCHEC : {temoin}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
