#!/usr/bin/env python3
"""test_migration_cf3_gui.py — D127 : la falsifiabilité du GUI de cérémonie
de migration CF2 → CF3 (v06/migration_cf3_gui.py).

Une garde qui ne rejette rien ne garde rien (leçon M3). Le GUI ne
réimplémente RIEN (relais sous-processus des vérités vivantes) — sa suite
prouve donc le CANAL, pas la serrure (prouvée par v06/test_coffre_cf3.py
et v06/test_migration_cf3.py) :

  X1  import headless (aucune fenêtre créée) + selftest embarqué vert ;
      preuve structurelle AST : tk.Tk() ne vit QUE dans demarrer_gui
  X2  cohérence des attributs (régression D109, la méthode maison) : AST —
      tout self.<attr> lu est défini, aucune référence morte
  X3  le relais sous-processus : une CÉRÉMONIE COMPLÈTE de laboratoire
      (CF1 → CF2 par les vérités vivantes, puis migrer relayé avec la
      phrase par STDIN) rend code 0 + « VERDICT : VERT » dans le flux ;
      la COMMANDE porte -u (D124 : la boîte noire horodate l'émission,
      un crash n'emporte plus les dernières lignes) mais JAMAIS la
      phrase ; l'enfant témoin avoue PYTHONIOENCODING=utf-8 (cp850) et
      la CLASSE FileIO de son stdout (non tamponné — falsifié des deux
      côtés)
  X4  le verdict est CROISÉ flux/code : un enfant menteur qui imprime
      « VERDICT : VERT » mais sort 1 est ROUGE ; un enfant muet (code 0
      sans marque) est SANS VERDICT — état nommé, jamais un vert mou
  X5  le rapport : emporte l'entête, l'empreinte md5 de coffre_cf3, le
      journal d'écran et la boîte noire ; AUCUN chemin de coffre réel,
      la phrase N'Y FIGURE JAMAIS ; troncature à 3000 lignes (garde-fou)
  X6  la boîte noire est un TÉMOIN, pas une dépendance : chemin
      impossible → l'écriture est silencieuse, la cérémonie continue
  L   les lanceurs lancer_migration_cf3.bat/.sh : le .sh EXÉCUTÉ (deux
      postures : dossier v06/ d'abord, copie plate ensuite, refus nommé
      sans cible) ; le .bat par CONTENU (Windows ne court pas ici, la
      preuve structurelle est la seule possible et elle est dite)

Usage : python3 v06/test_migration_cf3_gui.py   (~40-90 s : deux
cérémonies complètes relayées, Argon2id à chaque dérivation)
"""

import ast
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)
import v06.migration_cf3_gui as G                      # noqa: E402

RESULTATS = []


def _verifie(temoin: str, condition: bool, detail: str = "") -> None:
    RESULTATS.append((temoin, bool(condition)))
    marque = "PASS" if condition else "ÉCHEC"
    print(f"[test-GUI-migration] {temoin} : {marque}"
          + (f" — {detail}" if detail and not condition else ""))


def _md5(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


# ---------------------------------------------------------------------------
# X1 — import headless + selftest embarqué vert
# ---------------------------------------------------------------------------

def x1_import_headless():
    # l'import a déjà eu lieu en tête de module SANS créer de fenêtre :
    # tkinter est importé PROTÉGÉ (drapeau), et le tk.Tk() ne vit QUE
    # dans demarrer_gui — preuve structurelle par AST
    _verifie("x1-import-headless-avec-drapeau",
             hasattr(G, "VERSION_GUI") and G.TKINTER_DISPONIBLE)
    with open(os.path.abspath(G.__file__), "r", encoding="utf-8") as f:
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
    ok = G.selftest()
    _verifie("x1-selftest-embarque-vert", ok)


# ---------------------------------------------------------------------------
# X2 — cohérence des attributs (AST, régression D109)
# ---------------------------------------------------------------------------

def x2_coherence_attributs():
    with open(os.path.abspath(G.__file__), "r", encoding="utf-8") as f:
        arbre = ast.parse(f.read())

    classes = {n.name: n for n in ast.walk(arbre)
               if isinstance(n, ast.ClassDef)
               and n.name in ("Journal", "Application", "Enregistreur",
                              "RelaisEssais")}

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
# X3 — le relais sous-processus : une cérémonie COMPLÈTE relayée
# ---------------------------------------------------------------------------

def _fabrique_cf2(bac: str, phrase: bytes):
    """Un coffre CF2 de laboratoire par les VÉRITÉS VIVANTES (CF1 → CF2),
    config à jour + heart-beat vivant (la porte D120 est armée au labo)."""
    import json as _json
    from v06 import coffre_cf2 as cf2
    cf1 = cf2._charger_cf1()
    import base64 as _b64
    cf1_bin = os.path.join(bac, "coffre_fort.bin")
    cf2_bin = os.path.join(bac, "coffre_cf2.bin")
    gardes = os.path.join(bac, "gardes")
    cfg = os.path.join(bac, "config_cf2.json")
    base = cf1.nouvelle_base()
    base["description"] = "test GUI migration D127"
    base["projets"]["projet"] = {"description": "", "entrees": [
        {"etiquette": "e", "description": "",
         "phrase_b64": _b64.b64encode(b"X").decode("ascii")}]}
    cf1.sauver(cf1_bin, base, phrase)
    cf2.migrer(cf1_bin, cf2_bin, gardes, 5, 3, phrase, cfg)
    config = cf2.lire_config(cfg)
    config["journal"] = os.path.join(bac, "journal-s.txt")
    config["heartbeat"] = os.path.join(bac, "heartbeat.txt")
    config["pv_dir"] = os.path.join(bac, "pv-cf2")
    cf2.ecrire_config(cfg, config)
    with open(config["heartbeat"], "w", encoding="utf-8") as f:
        _json.dump({"ts": time.time()}, f)
    return cf2_bin, cfg


def x3_relais_sous_processus():
    phrase = b"phrase-relais-x3-D127"
    bac = tempfile.mkdtemp(prefix="gui-migr-x3-")
    try:
        cf2_bin, cfg = _fabrique_cf2(bac, phrase)
        cf3_bin = os.path.join(bac, "coffre_cf3.bin")
        media = os.path.join(bac, "media-piege")
        os.makedirs(media)
        arguments = ["migrer", "--conteneur-cf2", cf2_bin,
                     "--config-cf2", cfg, "--piege-dir", media,
                     "--conteneur", cf3_bin, "--phrase-stdin"]
        relais = G.RelaisEssais()
        lignes = relais.lancer(G.chemin_cible("coffre_cf3.py"), arguments,
                               entree_stdin=phrase.decode() + "\n")
        _verifie("x3-relais-migrer-code-0", relais.code == 0,
                 f"code={relais.code}")
        _verifie("x3-relais-migrer-verdict-vert-du-flux",
                 any("VERDICT : VERT" in l for l in lignes))
        _verifie("x3-relais-commande-porte-u",
                 relais.commande is not None
                 and relais.commande[1] == "-u")
        _verifie("x3-relais-phrase-jamais-dans-la-commande",
                 relais.commande is not None
                 and all("phrase-relais-x3" not in str(a)
                         for a in relais.commande))

        # l'enfant témoin avoue PYTHONIOENCODING et la CLASSE de son
        # tampon stdout (FileIO = non tamponné : le drapeau -u court,
        # D124 — la boîte noire horodate l'ÉMISSION, un crash n'emporte
        # plus les lignes qui le nomment)
        temoin = os.path.join(bac, "temoin.py")
        with open(temoin, "w", encoding="utf-8") as f:
            f.write("import os, sys\n"
                    "print('ioencoding=' "
                    "+ os.environ.get('PYTHONIOENCODING', 'ABSENT'))\n"
                    "print('stdout=' + type(sys.stdout.buffer).__name__)\n")
        relais_t = G.RelaisEssais()
        lignes_t = relais_t.lancer(temoin)
        _verifie("x3-enfant-recoit-pythonioencoding-utf8",
                 any("ioencoding=utf-8" in l for l in lignes_t))
        _verifie("x3-enfant-flux-non-tamponne-u",
                 any("stdout=FileIO" in l for l in lignes_t),
                 "attendu FileIO (écrit immédiat) — reçu : "
                 + "; ".join(lignes_t))
        # falsifié de l'AUTRE côté : SANS -u (environ propre), le témoin
        # avoue BufferedWriter — le défaut D124 resterait visible
        environnement_propre = dict(os.environ)
        environnement_propre.pop("PYTHONUNBUFFERED", None)
        r = subprocess.run([sys.executable, temoin], capture_output=True,
                           text=True, env=environnement_propre,
                           cwd=bac, timeout=60)
        _verifie("x3-sans-u-le-tampon-revient (contrôle croisé)",
                 "stdout=BufferedWriter" in r.stdout, r.stdout.strip())

        # cible absente : refus NOMMÉ, jamais un crash
        relais_x = G.RelaisEssais()
        relais_x.lancer(os.path.join(bac, "introuvable.py"))
        _verifie("x3-relais-cible-absente-refus-nomme",
                 relais_x.erreur is not None
                 and "introuvable" in relais_x.erreur)
    finally:
        shutil.rmtree(bac, ignore_errors=True)


# ---------------------------------------------------------------------------
# X4 — le verdict est CROISÉ flux / code de sortie
# ---------------------------------------------------------------------------

def x4_verdict_croise():
    bac = tempfile.mkdtemp(prefix="gui-migr-x4-")
    try:
        # menteur : imprime la MARQUE mais sort 1 → la COMPOSITION du
        # GUI (code == 0 ET marque vue) rend ROUGE
        menteur = os.path.join(bac, "menteur.py")
        with open(menteur, "w", encoding="utf-8") as f:
            f.write("print('[CF3-migration] VERDICT : VERT — époque 1, "
                    "checksum deadbeef')\nraise SystemExit(1)\n")
        relais = G.RelaisEssais()
        lignes = relais.lancer(menteur)
        marque_vue = any(G.MARQUE_MIGRER in l for l in lignes)
        vert = (relais.code == 0 and marque_vue)
        _verifie("x4-enfant-menteur-code-1-rouge",
                 marque_vue and not vert)

        # muet : code 0 SANS la marque → SANS VERDICT (état nommé côté
        # GUI : « code 0 SANS la marque attendue — rapportez-le »)
        muet = os.path.join(bac, "muet.py")
        with open(muet, "w", encoding="utf-8") as f:
            f.write("print('(silence)')\n")
        relais2 = G.RelaisEssais()
        lignes2 = relais2.lancer(muet)
        marque2 = any(G.MARQUE_MIGRER in l for l in lignes2)
        _verifie("x4-enfant-muet-sans-marque-sans-verdict",
                 relais2.code == 0 and not marque2
                 and not (relais2.code == 0 and marque2))
    finally:
        shutil.rmtree(bac, ignore_errors=True)


# ---------------------------------------------------------------------------
# X5 — le rapport : tout emporté, la phrase JAMAIS
# ---------------------------------------------------------------------------

def x5_rapport():
    temoin_ecran = ("[CF3-migration] VERDICT : VERT — époque 1, "
                    "checksum abcd1234 (temoin-x5)")
    rapport = G.constituer_rapport_complet(temoin_ecran)

    md5_cf3 = _md5(G.chemin_cible("coffre_cf3.py"))
    _verifie("x5-rapport-emporte-version-et-sections",
             "RAPPORT DE CÉRÉMONIE DE MIGRATION CF3" in rapport
             and G.VERSION_GUI in rapport
             and "JOURNAL D'ÉCRAN" in rapport
             and "JOURNAL DE VOL" in rapport
             and temoin_ecran in rapport)
    _verifie("x5-rapport-emporte-l-empreinte-de-coffre_cf3",
             md5_cf3 in rapport)
    _verifie("x5-rapport-aucun-chemin-de-coffre-reel",
             ".keys/coffre_cf3.bin" not in rapport
             and ".keys/coffre_fort.bin" not in rapport)

    # troncature : une boîte factice de 3100 lignes → 3000 gardées
    ancien = G.CHEMIN_JOURNAL_VOL
    bac = tempfile.mkdtemp(prefix="gui-migr-x5-")
    try:
        factice = os.path.join(bac, "boite.log")
        with open(factice, "w", encoding="utf-8") as f:
            for i in range(3100):
                f.write(f"[2000-01-01 00:00:{i % 60:02d}] [info    ] "
                        f"ligne {i}\n")
        G.CHEMIN_JOURNAL_VOL = factice
        rapport2 = G.constituer_rapport_complet("écran témoin")
        _verifie("x5-troncature-3000-lignes",
                 "100 lignes plus anciennes tronquées" in rapport2
                 and "ligne 3099" in rapport2
                 and "ligne 0\n" not in rapport2)
    finally:
        G.CHEMIN_JOURNAL_VOL = ancien
        shutil.rmtree(bac, ignore_errors=True)


# ---------------------------------------------------------------------------
# X6 — la boîte noire est un TÉMOIN, pas une dépendance
# ---------------------------------------------------------------------------

def x6_boite_noire_temoin():
    bac = tempfile.mkdtemp(prefix="gui-migr-x6-")
    try:
        impossible = os.path.join(bac, "dossier-inexistant", "vol.log")
        enregistreur = G.Enregistreur(impossible)
        # silencieux : aucune exception, la ligne ne va nulle part
        enregistreur.ligne("ligne qui n'ira nulle part", "essai")
        _verifie("x6-boite-noire-impossible-silencieuse",
                 enregistreur.fichier is None
                 and not os.path.exists(impossible))
    finally:
        shutil.rmtree(bac, ignore_errors=True)


# ---------------------------------------------------------------------------
# L — les lanceurs (conventions D118 : v06/ d'abord, repli copie à côté,
# refus nommé sans cible ; le .bat par CONTENU — Windows ne court pas ici)
# ---------------------------------------------------------------------------

def l_lanceurs():
    bat = os.path.join(RACINE, "lancer_migration_cf3.bat")
    sh = os.path.join(RACINE, "lancer_migration_cf3.sh")
    with open(bat, "r", encoding="utf-8", errors="replace") as f:
        contenu_bat = f.read()
    _verifie("l-bat-ordre-v06-d-abord-puis-copie-plate",
             "v06\\migration_cf3_gui.py" in contenu_bat
             and "migration_cf3_gui.py" in contenu_bat
             and "introuvable" in contenu_bat)
    _verifie("l-bat-py-3-puis-python",
             'py -3 "%GUI%"' in contenu_bat
             and 'python "%GUI%"' in contenu_bat)

    bac = tempfile.mkdtemp(prefix="gui-migr-l-")
    try:
        # posture 1 : dossier v06/ (un kit minimal autour des vérités
        # vivantes — la posture du Drive)
        posture = os.path.join(bac, "posture-v06")
        kit = os.path.join(posture, "v06")
        os.makedirs(kit)
        for nom in ("migration_cf3_gui.py", "coffre_cf3.py",
                    "coffre_cf2.py", "__init__.py"):
            source = (os.path.join(RACINE, "v06", nom)
                      if nom != "__init__.py" or os.path.isfile(
                          os.path.join(RACINE, "v06", nom))
                      else None)
            if source and os.path.isfile(source):
                shutil.copy(source, os.path.join(kit, nom))
        shutil.copy(sh, os.path.join(posture, "lancer_migration_cf3.sh"))
        r = subprocess.run(["sh", "lancer_migration_cf3.sh", "--selftest"],
                           cwd=posture, capture_output=True, text=True,
                           timeout=600)
        _verifie("l-sh-posture-v06-selftest-vert",
                 r.returncode == 0 and "18 PASS / 0 ÉCHEC" in r.stdout,
                 r.stdout[-300:] + r.stderr[-200:])

        # posture 2 : copie PLATE — le selftest se prouve aussi (la
        # fixture passe par cmd_init, AUCUN besoin de coffre_fort.py)
        plat = os.path.join(bac, "posture-plate")
        os.makedirs(plat)
        for nom in ("migration_cf3_gui.py", "coffre_cf3.py",
                    "coffre_cf2.py"):
            shutil.copy(os.path.join(RACINE, "v06", nom),
                        os.path.join(plat, nom))
        shutil.copy(sh, os.path.join(plat, "lancer_migration_cf3.sh"))
        r2 = subprocess.run(["sh", "lancer_migration_cf3.sh", "--selftest"],
                            cwd=plat, capture_output=True, text=True,
                            timeout=600)
        _verifie("l-sh-posture-copie-plate-selftest-vert",
                 r2.returncode == 0
                 and "18 PASS / 0 ÉCHEC" in r2.stdout,
                 r2.stdout[-300:] + r2.stderr[-200:])

        # refus nommé : sans cible, le lanceur S'ARRÊTE en disant pourquoi
        vide = os.path.join(bac, "posture-vide")
        os.makedirs(vide)
        shutil.copy(sh, os.path.join(vide, "lancer_migration_cf3.sh"))
        r3 = subprocess.run(["sh", "lancer_migration_cf3.sh"],
                            cwd=vide, capture_output=True, text=True,
                            timeout=60)
        _verifie("l-sh-sans-cible-refus-nomme",
                 r3.returncode == 1
                 and "migration_cf3_gui.py introuvable" in r3.stderr
                 + r3.stdout)
    finally:
        shutil.rmtree(bac, ignore_errors=True)


# ---------------------------------------------------------------------------

def main() -> int:
    print("[test-GUI-migration] suite D127 du GUI de cérémonie de "
          "migration CF2 → CF3 (trio D122 : GUI + boîte noire + rapport)")
    for groupe in (x1_import_headless, x2_coherence_attributs,
                   x3_relais_sous_processus, x4_verdict_croise, x5_rapport,
                   x6_boite_noire_temoin, l_lanceurs):
        groupe()
    echecs = [t for t, ok in RESULTATS if not ok]
    print(f"\n[test-GUI-migration] {len(RESULTATS) - len(echecs)} PASS / "
          f"{len(echecs)} ÉCHEC")
    if echecs:
        for temoin in echecs:
            print(f"  ÉCHEC : {temoin}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
