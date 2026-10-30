#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""migration_cf3_gui.py — le GUI DE CÉRÉMONIE DE MIGRATION CF2 → CF3 (D127).

POURQUOI CE MODULE EXISTE. La preuve terrain de la serrure CF3 est acquise
(D125 : 120 PASS sur Windows) : la spec § 12 (v06/I/CF3/README.md) dit
« l'outillage migrer sera livré avec la preuve terrain » — le voici. La
migration du coffre RÉEL est une CÉRÉMONIE en quatre actes, et le terrain
l'a exigé une première fois (D122, règle systématique) : tout module livré
pour un acte du maître porte (1) une INTERFACE GRAPHIQUE, (2) une BOÎTE
NOIRE locale horodatée, (3) un bouton « Envoyer le rapport… » — le
transport reste la main de l'humain, AUCUN réseau (le trio D113/D122).

LES QUATRE ACTES (spec § 12), guidés par les trois onglets :
  1 · MIGRER      — CF2 déverrouillé une dernière fois (porte D120
                    honorée), base re-scellée sous CF3 schéma identique
                    (RIEN À TRADUIRE), re-lecture à froid du scellage ;
                    le conteneur CF2 reste INTACT.
  2 · VÉRIFIER    — le verdict à froid de CF3 (sentinelle complète +
                    checksum 8 hex pour la CARTE du sachet) : l'humain
                    recoupe AVANT toute destruction.
  3 · DÉTRUIRE    — la destruction EXPLICITE du conteneur CF2 (quatrième
                    acte, --oui-je-comprends) ; les fragments CF2 et leurs
                    copies hors-ligne restent la RELÈVE HISTORIQUE.

CE QUE LE GUI FAIT :
  1. DIAGNOSTIC D'ENVIRONNEMENT AVANT TOUT ACTE — OS, Python, interpréteur,
     pile du dépôt (argon2-cffi / PyNaCl / cryptography, version ou ABSENT
     nommé) et EMPREINTES md5 des modules (coffre_cf3.py, coffre_cf2.py,
     coffre_fort.py, ce GUI) : un rapport qui me parvient dit EXACTEMENT
     quelle génération de code a tourné.
  2. TROIS ONDETS, RELAIS SOUS-PROCESSUS — le GUI ne réimplémente RIEN : il
     lance les vérités vivantes (v06/coffre_cf3.py migrer / verifier /
     detruire-cf2) et leur sortie coule ci-dessous. La PHRASE passe par
     STDIN (--phrase-stdin), JAMAIS en ligne de commande (invisible des
     journaux de processus), jamais affichée, jamais dans un rapport ;
     l'onglet 1 la fait taper DEUX fois (un scellé sous une phrase
     typée ne s'ouvrirait plus sous la phrase pensée).
  3. BOÎTE NOIRE (journal de vol horodaté, v06/migration-cf3-journal.log,
     gitignorée) + VERDICT croisé : code de sortie ET marque attendue dans
     le flux (un enfant menteux qui affiche VERT mais sort 1 est ROUGE).
  4. « Envoyer le rapport… » (D113/D122) : entête d'environnement + journal
     d'écran + journal de vol → Enregistrer sous .txt + presse-papiers +
     dossier ouvert. AUCUN réseau, AUCUN secret.
  5. DISPOSITION EN GRILLE (D132) : dans chaque onglet, l'étiquette vit
     AU-DESSUS de son champ, et le bouton « Parcourir… » vit sur la MÊME
     LIGNE que le champ qu'il remplit (le terrain avait les boutons
     empilés en colonne à droite, hors de leurs champs) ; la confirmation
     de phrase est étiquetée, les boutons d'acte prennent la pleine
     largeur, et TOUT champ de chemin porte son bouton (migrer, vérifier,
     détruire).

ENCODAGE : les enfants sont lancés avec PYTHONIOENCODING=utf-8 et lus en
UTF-8 remplacé — les accents des verdicts survivent au cp850 de Windows.

FLUX (D124) : les enfants sont lancés « python -u », stdout NON tamponné,
et PYTHONUNBUFFERED ambiant est NEUTRALISÉ — le drapeau VISIBLE décide
seul. La boîte noire horodate l'ÉMISSION réelle des lignes et survit à un
crash brutal de ce qu'elle observe (leçon du rapport terrain 30/10 12:13 :
22 s collapsées sur un horodatage, et un crash emporterait les lignes qui
le nomment).

EMPLACEMENT : ce GUI vit dans v06/ (dépôt complet OU kit du Drive) et
attend coffre_cf3.py À CÔTÉ de lui ; --v06 CHEMIN le pointe ailleurs
(échec NOMMÉ si introuvable, jamais un repli silencieux).

POSTURE : la migration part d'un coffre CF2 VIVANT — si le vôtre est
encore CF1, passez d'abord par le GUI de cérémonie (onglet CF2, migrer).
La cérémonie du sceau (re-cérémonie D126) est INDÉPENDANTE : le sceau
signe l'intention, la migration déplace le coffre — l'ordre voulu par le
maître (« a puis b ») recommande la signature d'abord, mais la migration
ne refuse pas pendant la fenêtre de re-cérémonie.

Modes : (aucun) → fenêtre ; --selftest → batterie headless (le GUI se
prouve lui-même : boîte noire vivante, relais réel d'une migration
complète de laboratoire, verdict croisé, rapport sans secret).
"""

import argparse
import datetime
import hashlib
import os
import platform
import queue
import subprocess
import sys
import threading
import traceback

# --- confort console Windows (accents français) ---------------------------
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


VERSION_GUI = "migration-CF3-GUI v1.1 (D132)"
# v1.1 = D132 : disposition en GRILLE — chaque bouton « Parcourir… » vit
#        sur la MÊME ligne que son champ (le terrain avait les boutons
#        empilés en colonne à droite, hors de leurs champs), confirmation
#        de phrase étiquetée, boutons d'acte pleine largeur, Parcourir sur
#        tous les champs de chemin. v1.0 = D127.

NOM_JOURNAL_VOL = "migration-cf3-journal.log"

# Marques de verdict dans le flux (le GUI croise code de sortie ET marque —
# un enfant menteux est ROUGE, un enfant muet est SANS VERDICT)
MARQUE_MIGRER = "VERDICT : VERT"
MARQUE_VERIFIER = "VERDICT : VERT"
MARQUE_DETRUIRE = "DÉTRUIT"


# ===========================================================================
# SECTION 0 — D113/D122 : L'ENREGISTREUR DE VOL (boîte noire). Tout ce que
# le GUI dit, fait, et chaque crash atterrit dans un journal LOCAL horodaté,
# à côté du fichier lui-même. AUCUN réseau ; aucune donnée secrète (la
# phrase ne figure JAMAIS ici : elle passe par stdin, invisible des
# journaux, et les sorties des enfants ne l'échoient pas).
# ===========================================================================

CHEMIN_JOURNAL_VOL = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), NOM_JOURNAL_VOL)


class Enregistreur:
    """Boîte noire locale : append horodaté, une ligne = un fait. Un échec
    d'écriture (disque en lecture seule) ne gêne JAMAIS la cérémonie."""

    def __init__(self, chemin):
        self.chemin = chemin
        self.fichier = None
        try:
            self.fichier = open(chemin, "a", encoding="utf-8", buffering=1)
        except OSError:
            pass

    def ligne(self, texte, genre="info"):
        if not self.fichier:
            return
        horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.fichier.write(f"[{horodatage}] [{genre:<8}] {texte}\n")
        except OSError:
            pass

    def traceback(self):
        """Le traceback COMPLET de l'exception en cours, ligne par ligne."""
        for ligne in traceback.format_exc().splitlines():
            self.ligne(ligne, "crash")

    def entete(self, racine=None):
        self.ligne("=" * 72, "entete")
        self.ligne(f"DEMARRAGE {VERSION_GUI}", "entete")
        self.ligne(f"python {sys.version.split()[0]} — "
                   f"{platform.platform()} — argv : {' '.join(sys.argv)!r}",
                   "entete")
        if racine is not None:
            try:
                self.ligne(
                    f"Tk {racine.tk.call('info', 'patchlevel')} — écran "
                    f"{racine.winfo_screenwidth()}x"
                    f"{racine.winfo_screenheight()}", "entete")
            except Exception:
                pass
        self.ligne(f"dossier v06 : {CHEMIN_V06}", "entete")


# La résolution du dossier v06 doit exister AVANT l'entête de la boîte
# noire (elle y est consignée) — échec NOMMÉ, jamais un repli silencieux.
def _resoudre_v06(chemin_argument):
    if chemin_argument:
        candidat = os.path.abspath(chemin_argument)
        if not os.path.isdir(candidat):
            raise SystemExit(
                f"[migration-CF3-GUI] ÉCHEC — le dossier v06 indiqué "
                f"n'existe pas : {candidat}")
        return candidat
    return os.path.dirname(os.path.abspath(__file__))


CHEMIN_V06 = _resoudre_v06(None)

RACINE_DEPOT = os.path.dirname(CHEMIN_V06)
CONTENEUR_CF2_DEFAUT = os.path.join(RACINE_DEPOT, ".keys", "coffre_cf2.bin")
CONTENEUR_CF3_DEFAUT = os.path.join(RACINE_DEPOT, ".keys", "coffre_cf3.bin")

ENREGISTREUR = Enregistreur(CHEMIN_JOURNAL_VOL)


# ===========================================================================
# SECTION A — diagnostic d'environnement (D122) : pile pip + empreintes.
# Ce que le RAPPORT emporte, pour que le diagnostic distant soit une
# lecture : quelle machine, quel Python, quelle pile, quelle GÉNÉRATION
# du code (md5).
# ===========================================================================

PILE_PIP = (("argon2-cffi", "argon2"), ("PyNaCl", "nacl"),
            ("cryptography", "cryptography"))


def _version_paquet(nom_pip):
    """Version du paquet pip par les métadonnées (importlib) — None si le
    paquet n'est pas installé (un état NOMMÉ, pas un crash)."""
    try:
        from importlib import metadata as _meta
        return _meta.version(nom_pip)
    except Exception:
        return None


def pile_pip():
    return [(nom, _version_paquet(nom)) for nom, _ in PILE_PIP]


def pile_complete():
    return all(v is not None for _, v in pile_pip())


MODULES_EMPREINTES = ("coffre_cf3.py", "coffre_cf2.py", "coffre_fort.py",
                      "migration_cf3_gui.py")


def empreintes_modules():
    """[(nom, md5 ou None)] des modules de la cérémonie, dossier v06 (et
    racine du dépôt pour coffre_fort.py) — None = absent (nommé)."""
    empreintes = []
    for nom in MODULES_EMPREINTES:
        chemin = (os.path.join(RACINE_DEPOT, nom)
                  if nom == "coffre_fort.py"
                  else os.path.join(CHEMIN_V06, nom))
        if os.path.isfile(chemin):
            try:
                with open(chemin, "rb") as f:
                    empreintes.append((nom, hashlib.md5(f.read()).hexdigest()))
            except OSError:
                empreintes.append((nom, None))
        else:
            empreintes.append((nom, None))
    return empreintes


def texte_pile():
    morceaux = [f"{nom} {v if v else 'ABSENT'}" for nom, v in pile_pip()]
    return " · ".join(morceaux) + ("  [pile COMPLÈTE]" if pile_complete()
                                   else "  [pile INCOMPLÈTE]")


def chemin_cible(nom):
    return os.path.join(CHEMIN_V06, nom)


def constituer_rapport_complet(texte_ecran):
    """Le rapport D113/D122, au niveau MODULE (prouvable headless) :
    entête d'environnement + empreintes + journal d'écran + boîte noire.
    AUCUN secret : la phrase ne vit nulle part ici (stdin, jamais échoée)."""
    lignes = [
        "RAPPORT DE CÉRÉMONIE DE MIGRATION CF3 — " + VERSION_GUI,
        "généré le "
        + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        f"python {sys.version.split()[0]} — {platform.platform()}",
        f"interpréteur : {sys.executable}",
        f"dossier v06 : {CHEMIN_V06}",
        f"pile du dépôt : {texte_pile()}",
        "empreintes md5 des modules :",
    ]
    for nom, empreinte in empreintes_modules():
        lignes.append(f"  {nom} : "
                      f"{empreinte if empreinte else 'ABSENT'}")
    lignes += [
        f"boîte noire : {CHEMIN_JOURNAL_VOL}",
        "=" * 72,
        "JOURNAL D'ÉCRAN (ce que la fenêtre a affiché) :",
        (texte_ecran or "(vide)").rstrip() or "(vide)",
        "=" * 72,
        "JOURNAL DE VOL (boîte noire, horodatée) :",
    ]
    try:
        with open(CHEMIN_JOURNAL_VOL, "r", encoding="utf-8") as f:
            brut = f.read().splitlines()
        if len(brut) > 3000:   # garde-fou : le récent suffit
            lignes.append(f"… ({len(brut) - 3000} lignes plus "
                          "anciennes tronquées)")
            brut = brut[-3000:]
        lignes.extend(brut)
    except OSError as exc:
        lignes.append(f"(boîte noire illisible : {exc})")
    return "\n".join(lignes)


# ===========================================================================
# SECTION B — le relais sous-processus. Le GUI ne réimplémente RIEN : il
# lance les vérités vivantes (coffre_cf3.py migrer / verifier /
# detruire-cf2) et laisse leur sortie couler. La PHRASE (migrer, verifier)
# passe par STDIN : jamais en ligne de commande (les listes de processus
# la liraient), jamais affichée, jamais consignée. Le fil ouvrier NE
# TOUCHE JAMAIS tkinter (discipline maison D118) : il dépose ses lignes
# dans une file, le fil tkinter les pompe.
# ===========================================================================

class RelaisEssais:
    """Lance un acte en sous-processus, streame sa sortie ligne à ligne.

    usage (headless, comme le selftest) :
        relais = RelaisEssais()
        lignes = relais.lancer(chemin_script, ["migrer", …],
                               entree_stdin=phrase)
        lignes → liste des lignes émises ; relais.code → code de sortie ;
        relais.erreur → message d'échec nommé (lancement impossible) ;
        relais.commande → la commande effective (SANS la phrase — le -u
        s'y LIT, la preuve D124).

    usage (GUI) : lancer(chemin, arguments, emit=callback) — callback
    appelé depuis le FIL OUVRIER (il ne doit toucher ni tkinter ni le
    journal écran).
    """

    def __init__(self):
        self.code = None
        self.erreur = None
        self.commande = None

    def lancer(self, chemin_script, arguments=None, emit=None,
               entree_stdin=None):
        """Exécute [sys.executable, "-u", chemin_script] + arguments dans
        le dossier v06. entree_stdin (str) : écrit sur l'entrée standard
        puis ferme (la phrase passe par LÀ, pas par la ligne de commande).
        PYTHONIOENCODING=utf-8 : les accents des verdicts survivent au
        cp850 de Windows. « -u » (D124) : stdout NON tamponné — la boîte
        noire horodate l'émission réelle et un crash brutal de l'enfant
        ne peut plus emporter ses dernières lignes. PYTHONUNBUFFERED
        ambiant est retiré : le drapeau VISIBLE décide seul."""
        self.code, self.erreur = None, None
        if not os.path.isfile(chemin_script):
            self.erreur = (f"acte impossible : {chemin_script} introuvable "
                           "— le GUI vit dans v06/ (dépôt complet ou kit "
                           "du Drive) auprès de coffre_cf3.py")
            return []
        environnement = dict(os.environ)
        environnement["PYTHONIOENCODING"] = "utf-8"
        # D124 : le drapeau VISIBLE (-u dans la commande affichée au
        # rapport) décide seul — une variable ambiante ne peut ni le
        # remplacer ni le masquer.
        environnement.pop("PYTHONUNBUFFERED", None)
        commande = [sys.executable, "-u", chemin_script] + list(arguments
                                                                or [])
        self.commande = commande
        lignes = []
        try:
            processus = subprocess.Popen(
                commande,
                cwd=CHEMIN_V06, env=environnement,
                stdin=(subprocess.PIPE if entree_stdin is not None
                       else subprocess.DEVNULL),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                bufsize=1)
        except OSError as exc:
            self.erreur = f"acte impossible : lancement échoué — {exc}"
            return lignes
        if entree_stdin is not None:
            try:
                processus.stdin.write(entree_stdin)
                processus.stdin.close()
            except OSError:
                pass      # l'enfant est mort tôt : son code parlera
        for ligne in processus.stdout:
            ligne = ligne.rstrip("\n").rstrip("\r")
            lignes.append(ligne)
            if emit:
                try:
                    emit(ligne)
                except Exception:
                    pass   # un témoin d'écriture ne doit pas tuer l'acte
        processus.stdout.close()
        self.code = processus.wait()
        return lignes


# ===========================================================================
# SECTION C — la GUI. tkinter est importé au niveau module mais PROTÉGÉ
# (try/except, drapeau TKINTER_DISPONIBLE) : --selftest et la batterie
# externe restent utilisables sur une machine sans tkinter — l'aide
# d'installation exacte s'affiche alors en console, et AUCUNE fenêtre
# n'est créée à l'import (le tk.Tk() ne vit que dans demarrer_gui,
# preuve structurelle par la suite externe).
# ===========================================================================

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    TKINTER_DISPONIBLE, TKINTER_ERREUR = True, ""
except ImportError as _exc:
    TKINTER_DISPONIBLE, TKINTER_ERREUR = False, str(_exc)

COULEUR_ENCRE = "#1f2328"
COULEUR_VERTE = "#1a7f37"
COULEUR_ROUGE = "#cf222e"
POLICE_FIXE = ("TkFixedFont", 10)


def _message_tkinter_manquant():
    if sys.platform.startswith("linux"):
        aide = ("Linux : sudo apt install python3-tk   (Debian/Ubuntu) ; "
                "sudo dnf install python3-tkinter   (Fedora)")
    elif sys.platform == "darwin":
        aide = ("macOS : réinstallez Python depuis python.org (le Python "
                "système n'a pas toujours tkinter)")
    else:
        aide = "Windows : réinstallez Python depuis python.org (cochez tcl/tk)"
    return (f"tkinter est absent de ce Python — {aide}\n"
            f"(détail : {TKINTER_ERREUR})")


def phrases_coherentes(phrase, confirmation):
    """(ok, message) — l'onglet MIGRER fait taper la phrase DEUX fois : un
    scellé sous une phrase typée ne s'ouvrirait plus sous la phrase
    pensée (il n'y a pas de « phrase erronée » à la migration : tout ce
    qui est scellé sous la phrase tapée s'ouvre sous la phrase tapée)."""
    if not phrase:
        return False, "phrase VIDE — la migration exige la phrase du coffre"
    if phrase != confirmation:
        return False, ("les deux phrases DIVERGENT — recomposez (un scellé "
                       "sous une phrase typée ne s'ouvrirait plus sous la "
                       "phrase pensée)")
    return True, ""


class Journal:
    """Journal d'écran : trace textuelle des actes (la preuve reste aux
    vérités vivantes lancées — le journal est pour l'humain ET pour le
    rapport). Chaque ligne voit AUSSI la boîte noire."""

    def __init__(self, parent, application):
        self.app = application
        cadre = ttk.LabelFrame(parent, text="Journal de cérémonie")
        cadre.pack(side="bottom", fill="both", expand=True,
                   padx=10, pady=(4, 10))
        barre = ttk.Frame(cadre)
        barre.pack(side="top", fill="x", padx=6, pady=(2, 0))
        ttk.Button(barre, text="Envoyer le rapport…", width=20,
                   command=lambda: self.app.envoyer_rapport()
                   ).pack(side="right", padx=(6, 0))   # D122 : systématique
        ttk.Button(barre, text="Copier tout", width=12,
                   command=self.copier).pack(side="right", padx=(6, 0))
        ttk.Button(barre, text="Effacer", width=8,
                   command=self.effacer).pack(side="right")
        self.texte = tk.Text(cadre, height=12, wrap="word",
                             state="disabled", font=POLICE_FIXE,
                             background="#ffffff", relief="flat",
                             highlightthickness=1,
                             highlightbackground="#d0d7de")
        self.texte.pack(side="top", fill="both", expand=True,
                        padx=6, pady=4)
        for tag, couleur in (("titre", "#0969da"),
                             ("info", COULEUR_ENCRE),
                             ("vert", COULEUR_VERTE),
                             ("rouge", COULEUR_ROUGE)):
            self.texte.tag_configure(tag, foreground=couleur)
        self.texte.tag_configure("titre",
                                 font=(POLICE_FIXE[0], 10, "bold"))

    def ajoute(self, ligne, genre="info"):
        ENREGISTREUR.ligne(str(ligne), genre)
        self.texte.configure(state="normal")
        self.texte.insert("end", str(ligne) + "\n", genre)
        self.texte.see("end")
        self.texte.configure(state="disabled")

    def copier(self):
        self.app.racine.clipboard_clear()
        self.app.racine.clipboard_append(self.texte.get("1.0", "end"))
        ENREGISTREUR.ligne("journal d'écran copié (presse-papiers)", "info")

    def effacer(self):
        ENREGISTREUR.ligne("journal d'écran effacé (la boîte noire "
                           "garde tout)", "info")
        self.texte.configure(state="normal")
        self.texte.delete("1.0", "end")
        self.texte.configure(state="disabled")


def _champ(parent, etiquette, valeur="", dialogue=None, titre=None,
           largeur=48, ligne=0):
    """Une ligne de saisie ALIGNÉE (D132) : étiquette AU-DESSUS, puis le
    champ et son éventuel bouton « Parcourir… » sur la MÊME ligne de
    grille — le terrain a dénoncé des boutons empilés en colonne à
    droite de l'onglet, loin de leurs champs (retour 31/10 : « les
    boutons de recherche de fichiers ne sont pas alignés aux champs
    concernés »). Retourne la StringVar."""
    ttk.Label(parent, text=etiquette).grid(
        column=0, row=ligne, columnspan=2, sticky="w")
    variable = tk.StringVar(value=valeur)
    ttk.Entry(parent, textvariable=variable, width=largeur).grid(
        column=0, row=ligne + 1, sticky="ew", pady=(0, 8))
    if dialogue is not None:
        def parcourir():
            choix = dialogue(title=titre, parent=parent.winfo_toplevel())
            if choix:
                variable.set(choix)
        ttk.Button(parent, text="Parcourir…", width=11,
                   command=parcourir).grid(
            column=1, row=ligne + 1, sticky="e", padx=(6, 0),
            pady=(0, 8))
    return variable


class Application:
    """Le GUI de cérémonie : environnement, trois actes relais, rapport."""

    def __init__(self, racine):
        self.racine = racine
        racine.title(f"TRIADE — cérémonie de migration CF2 → CF3 "
                     f"({VERSION_GUI})")
        racine.geometry("1000x720")
        racine.minsize(780, 560)
        self.file_messages = queue.Queue()
        self.acte_en_cours = False
        self.boutons_actes = []
        self._construire()
        racine.report_callback_exception = self._crash
        ENREGISTREUR.entete(racine)
        self.journal.ajoute(VERSION_GUI, "titre")
        self.journal.ajoute(
            "le GUI ne réimplémente rien : il lance les vérités vivantes "
            "(coffre_cf3.py migrer / verifier / detruire-cf2) et leur "
            "sortie coule ci-dessous. La phrase passe par stdin, jamais "
            "en ligne de commande, jamais ici.", "info")
        self.journal.ajoute(f"dossier v06 : {CHEMIN_V06}", "info")
        self.journal.ajoute(f"pile du dépôt : {texte_pile()}", "info")
        if not pile_complete():
            self.journal.ajoute(
                "pile INCOMPLÈTE — installez-la d'abord : "
                "pip install argon2-cffi pynacl cryptography "
                "(protocole terrain, LISEZMOI-coffre-CF3.txt § 1)",
                "rouge")
        absents = [nom for nom, empreinte in empreintes_modules()
                   if empreinte is None]
        requis_absents = [nom for nom in absents if nom != "coffre_fort.py"]
        if requis_absents:
            self.journal.ajoute(
                "modules REQUIS absents : " + ", ".join(requis_absents)
                + " — les actes correspondants seront des refus NOMMÉS",
                "rouge")
        if "coffre_fort.py" in absents:
            self.journal.ajoute(
                "coffre_fort.py absent du dossier parent — il ne sert qu'à "
                "la migration CF1 → CF2 (GUI de cérémonie) : la cérémonie "
                "CF2 → CF3 n'en a PAS besoin (état nommé, pas une panne)",
                "info")
        self.journal.ajoute(
            "POSTURE : la migration part d'un coffre CF2 VIVANT — si le "
            "vôtre est encore CF1, passez d'abord par le GUI de cérémonie "
            "(onglet CF2, migrer). La re-cérémonie du sceau (D126) est "
            "INDÉPENDANTE : le sceau signe l'intention, la migration "
            "déplace le coffre.", "info")
        self.racine.after(80, self._pomper)

    # --- construction -----------------------------------------------
    def _construire(self):
        bandeau = ttk.Frame(self.racine, padding=(10, 8))
        bandeau.pack(fill="x")
        ttk.Label(bandeau, text="Cérémonie de migration CF2 → CF3",
                  font=("TkDefaultFont", 14, "bold")).pack(side="left")
        ttk.Label(bandeau, text="   " + VERSION_GUI
                  ).pack(side="left", padx=(6, 0))

        # --- l'environnement, AVANT tout acte (D122)
        env = ttk.LabelFrame(self.racine,
                             text="Environnement (emporté par le rapport)",
                             padding=(10, 6))
        env.pack(fill="x", padx=10, pady=(6, 2))
        lignes_env = [
            f"python {sys.version.split()[0]} — {platform.platform()}",
            f"interpréteur : {sys.executable}",
            f"pile du dépôt : {texte_pile()}",
            "empreintes : "
            + " · ".join(f"{nom} {emp[:10] if emp else 'ABSENT'}"
                         for nom, emp in empreintes_modules()),
        ]
        for texte in lignes_env:
            ttk.Label(env, text=texte, font=POLICE_FIXE,
                      foreground=COULEUR_ENCRE).pack(anchor="w")
        if not pile_complete():
            ttk.Label(env, foreground=COULEUR_ROUGE, font=POLICE_FIXE,
                      text=("pile INCOMPLÈTE — pip install argon2-cffi "
                            "pynacl cryptography")).pack(anchor="w")

        carnets = ttk.Notebook(self.racine)
        carnets.pack(fill="both", expand=True, padx=10, pady=(6, 2))
        self.carnets = carnets   # la fumée Xvfb sélectionne les onglets

        # --- onglet 1 : MIGRER ---------------------------------------
        acte1 = ttk.Frame(carnets, padding=(10, 8))
        carnets.add(acte1, text="1 · Migrer (CF2 → CF3)")
        acte1.columnconfigure(0, weight=1)
        ttk.Label(acte1, text=(
            "Actes 1-3 de la cérémonie (spec § 12) : CF2 déverrouillé une "
            "dernière fois (porte D120 honorée), base re-scellée sous CF3 "
            "SCHÉMA IDENTIQUE (rien à traduire), re-lecture à froid du "
            "scellage. Le conteneur CF2 reste INTACT — sa destruction est "
            "l'onglet 3, après votre verdict."),
            wraplength=880, justify="left").grid(
                column=0, row=0, columnspan=2, sticky="w", pady=(0, 8))
        self.var_cf2 = _champ(
            acte1, "Conteneur CF2 (le coffre vivant)",
            CONTENEUR_CF2_DEFAUT,
            dialogue=filedialog.askopenfilename,
            titre="Choisir le conteneur CF2", ligne=1)
        self.var_gardes = _champ(
            acte1, "Racine des gardes CF2 (g1…gN — vide : la config CF2 "
                   "décide)", "",
            dialogue=filedialog.askdirectory,
            titre="Choisir la racine des gardes CF2", ligne=3)
        self.var_config = _champ(
            acte1, "Config CF2 explicite (vide : .keys/config_cf2.json si "
                   "elle vit, sinon synthèse nommée)", "",
            dialogue=filedialog.askopenfilename,
            titre="Choisir la config CF2", ligne=5)
        self.var_media = _champ(
            acte1, "MÉDIA du piège (la clef USB du sachet — REQUIS, la "
                   "machine ne le crée jamais)", "",
            dialogue=filedialog.askdirectory,
            titre="Choisir le média du piège", ligne=7)
        self.var_cf3 = _champ(
            acte1, "Conteneur CF3 (le coffre qui naît)",
            CONTENEUR_CF3_DEFAUT,
            dialogue=filedialog.asksaveasfilename,
            titre="Choisir l'emplacement du conteneur CF3", ligne=9)
        ttk.Separator(acte1, orient="horizontal").grid(
            column=0, row=11, columnspan=2, sticky="ew", pady=(0, 6))
        ttk.Label(acte1, text="Phrase du coffre (tapée DEUX fois — un "
                              "scellé sous une phrase typée ne s'ouvrirait "
                              "plus sous la phrase pensée) :").grid(
                                  column=0, row=12, columnspan=2,
                                  sticky="w")
        self.var_phrase = tk.StringVar(value="")
        ttk.Entry(acte1, textvariable=self.var_phrase, width=48,
                  show="•").grid(column=0, row=13, sticky="ew",
                                 pady=(0, 4))
        ttk.Label(acte1, text="Confirmation de la phrase :").grid(
            column=0, row=14, columnspan=2, sticky="w")
        self.var_phrase2 = tk.StringVar(value="")
        ttk.Entry(acte1, textvariable=self.var_phrase2, width=48,
                  show="•").grid(column=0, row=15, sticky="ew",
                                 pady=(0, 8))
        self.bouton_migrer = ttk.Button(
            acte1, text="MIGRER (actes 1-3 : porte, re-scellage, "
                        "re-lecture à froid)",
            command=self.acte_migrer)
        self.bouton_migrer.grid(column=0, row=16, columnspan=2,
                                sticky="ew", pady=(4, 0))
        self.boutons_actes.append(self.bouton_migrer)

        # --- onglet 2 : VÉRIFIER -------------------------------------
        acte2 = ttk.Frame(carnets, padding=(10, 8))
        carnets.add(acte2, text="2 · Vérifier (verdict à froid)")
        acte2.columnconfigure(0, weight=1)
        ttk.Label(acte2, text=(
            "Acte 3 de la cérémonie, par l'humain : sentinelle complète, "
            "verdict à froid, checksum de 8 hex à RECOUPER avec la CARTE "
            "du sachet AVANT toute destruction (spec § 9). Recommandé : "
            "re-exécutez-le le lendemain, machine froide."),
            wraplength=880, justify="left").grid(
                column=0, row=0, columnspan=2, sticky="w", pady=(0, 8))
        self.var_cf3_v = _champ(
            acte2, "Conteneur CF3", CONTENEUR_CF3_DEFAUT,
            dialogue=filedialog.askopenfilename,
            titre="Choisir le conteneur CF3", ligne=1)
        self.var_media_v = _champ(
            acte2, "MÉDIA du piège", "",
            dialogue=filedialog.askdirectory,
            titre="Choisir le média du piège", ligne=3)
        ttk.Label(acte2, text="Phrase du coffre :").grid(
            column=0, row=5, columnspan=2, sticky="w")
        self.var_phrase_v = tk.StringVar(value="")
        ttk.Entry(acte2, textvariable=self.var_phrase_v, width=48,
                  show="•").grid(column=0, row=6, sticky="ew",
                                 pady=(0, 8))
        self.bouton_verifier = ttk.Button(
            acte2, text="VÉRIFIER (verdict à froid)",
            command=self.acte_verifier)
        self.bouton_verifier.grid(column=0, row=7, columnspan=2,
                                  sticky="ew", pady=(4, 0))
        self.boutons_actes.append(self.bouton_verifier)

        # --- onglet 3 : DÉTRUIRE -------------------------------------
        acte3 = ttk.Frame(carnets, padding=(10, 8))
        carnets.add(acte3, text="3 · Détruire le conteneur CF2")
        acte3.columnconfigure(0, weight=1)
        ttk.Label(acte3, text=(
            "Acte 4 de la cérémonie, EXPLICITE (spec § 12.4) : destruction "
            "du conteneur CF2 SEUL — les fragments CF2 et leurs copies "
            "hors-ligne restent la RELÈVE HISTORIQUE (jamais touchés). "
            "Uniquement après un verdict à froid VERT recoupé avec la "
            "carte. Garde fail-closed : refus si le conteneur CF3 est "
            "absent (jamais l'ancien sans le neuf)."),
            wraplength=880, justify="left").grid(
                column=0, row=0, columnspan=2, sticky="w", pady=(0, 8))
        self.var_cf2_d = _champ(
            acte3, "Conteneur CF2 (à détruire)", CONTENEUR_CF2_DEFAUT,
            dialogue=filedialog.askopenfilename,
            titre="Choisir le conteneur CF2", ligne=1)
        self.var_cf3_d = _champ(
            acte3, "Conteneur CF3 (le survivant — garde)",
            CONTENEUR_CF3_DEFAUT,
            dialogue=filedialog.askopenfilename,
            titre="Choisir le conteneur CF3", ligne=3)
        self.var_oui = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            acte3, variable=self.var_oui,
            text="Je comprends : destruction EXPLICITE et irréversible du "
                 "conteneur CF2 ; fragments et copies hors-ligne INTACTS "
                 "(relève historique)").grid(
                     column=0, row=5, columnspan=2, sticky="w",
                     pady=(0, 8))
        self.bouton_detruire = ttk.Button(
            acte3, text="DÉTRUIRE le conteneur CF2 (acte 4)",
            command=self.acte_detruire)
        self.bouton_detruire.grid(column=0, row=6, columnspan=2,
                                  sticky="ew", pady=(4, 0))
        self.boutons_actes.append(self.bouton_detruire)

        barre = ttk.Frame(self.racine, padding=(10, 2))
        barre.pack(fill="x")
        self.barre_verdict = ttk.Label(
            barre, text="aucun acte lancé", anchor="e",
            font=(POLICE_FIXE[0], 10, "bold"))
        self.barre_verdict.pack(side="right")

        self.journal = Journal(self.racine, self)

    # --- actes (le fil tkinter décide, l'ouvrier transmet) ---------
    def _bloquer_actes(self, bloquer):
        etat = "disabled" if bloquer else "normal"
        for bouton in self.boutons_actes:
            bouton.configure(state=etat)

    def acte_migrer(self):
        phrase = self.var_phrase.get()
        ok, message = phrases_coherentes(phrase, self.var_phrase2.get())
        if not ok:
            self.journal.ajoute(f"ÉCHEC NOMMÉ — {message}", "rouge")
            ENREGISTREUR.ligne(f"migrer refusé : {message}", "refus")
            self.barre_verdict.configure(text="migrer : phrase invalide",
                                         foreground=COULEUR_ROUGE)
            return
        media = self.var_media.get().strip()
        if not media:
            self.journal.ajoute(
                "ÉCHEC NOMMÉ — le MÉDIA du piège est REQUIS (branchez la "
                "clef USB du sachet et désignez-la — la machine ne le "
                "crée jamais, spec § 4)", "rouge")
            ENREGISTREUR.ligne("migrer refusé : média absent", "refus")
            self.barre_verdict.configure(text="migrer : média requis",
                                         foreground=COULEUR_ROUGE)
            return
        arguments = ["migrer", "--conteneur-cf2", self.var_cf2.get().strip(),
                     "--piege-dir", media,
                     "--conteneur", self.var_cf3.get().strip(),
                     "--phrase-stdin"]
        if self.var_gardes.get().strip():
            arguments += ["--gardes", self.var_gardes.get().strip()]
        if self.var_config.get().strip():
            arguments += ["--config-cf2", self.var_config.get().strip()]
        self._lancer("coffre_cf3.py", arguments, "migration (actes 1-3)",
                     MARQUE_MIGRER, entree_stdin=phrase + "\n")

    def acte_verifier(self):
        media = self.var_media_v.get().strip()
        if not media:
            self.journal.ajoute(
                "ÉCHEC NOMMÉ — le MÉDIA du piège est REQUIS (branchez-le)",
                "rouge")
            return
        phrase = self.var_phrase_v.get()
        if not phrase:
            self.journal.ajoute("ÉCHEC NOMMÉ — phrase vide", "rouge")
            return
        arguments = ["verifier", "--piege-dir", media,
                     "--conteneur", self.var_cf3_v.get().strip(),
                     "--phrase-stdin"]
        self._lancer("coffre_cf3.py", arguments, "verdict à froid",
                     MARQUE_VERIFIER, entree_stdin=phrase + "\n")

    def acte_detruire(self):
        if not self.var_oui.get():
            self.journal.ajoute(
                "ÉCHEC NOMMÉ — la destruction est EXPLICITE : cochez "
                "« Je comprends » (spec § 12.4 ; fragments INTACTS)",
                "rouge")
            ENREGISTREUR.ligne("detruire-cf2 refusé : sans affirmation",
                               "refus")
            self.barre_verdict.configure(
                text="detruire-cf2 : affirmation requise",
                foreground=COULEUR_ROUGE)
            return
        arguments = ["detruire-cf2",
                     "--conteneur-cf2", self.var_cf2_d.get().strip(),
                     "--conteneur", self.var_cf3_d.get().strip(),
                     "--oui-je-comprends"]
        self._lancer("coffre_cf3.py", arguments,
                     "destruction du conteneur CF2 (acte 4)",
                     MARQUE_DETRUIRE)

    def _lancer(self, nom_script, arguments, nom_acte, marque,
                entree_stdin=None):
        if self.acte_en_cours:
            self.journal.ajoute("un acte court déjà — attendez son "
                                "verdict (les actes ne se mélangent pas)",
                                "rouge")
            return
        chemin = chemin_cible(nom_script)
        if not os.path.isfile(chemin):
            self.journal.ajoute(
                f"ÉCHEC NOMMÉ — {nom_script} introuvable : {chemin} "
                "(le GUI vit dans v06/ du dépôt complet ou du kit du "
                "Drive)", "rouge")
            ENREGISTREUR.ligne(f"acte refusé : {nom_script} introuvable",
                               "refus")
            self.barre_verdict.configure(
                text=f"{nom_acte} : IMPOSSIBLE (module absent)",
                foreground=COULEUR_ROUGE)
            return
        self.acte_en_cours = True
        self._bloquer_actes(True)
        self.barre_verdict.configure(text=f"{nom_acte} : en cours…",
                                     foreground=COULEUR_ENCRE)
        # la commande affichée ne porte JAMAIS la phrase (stdin, pas argv)
        commande_affichee = f"{sys.executable} -u {nom_script}"
        if arguments:
            commande_affichee += " " + " ".join(arguments)
        self.journal.ajoute(f"— {nom_acte} : lancement "
                            f"({commande_affichee}) —", "titre")
        ENREGISTREUR.ligne(f"acte lancé : {commande_affichee}", "essai")

        def emit(ligne):
            self.file_messages.put(("ligne", ligne))

        def ouvrier():
            relais = RelaisEssais()
            lignes = relais.lancer(chemin, arguments, emit=emit,
                                   entree_stdin=entree_stdin)
            self.file_messages.put(("fin", nom_acte, relais.code,
                                    relais.erreur, lignes, marque))

        threading.Thread(target=ouvrier, daemon=True).start()

    def _pomper(self):
        """Le fil tkinter SEUL touche le journal (discipline D118)."""
        try:
            while True:
                message = self.file_messages.get_nowait()
                if message[0] == "ligne":
                    genre = "info"
                    if "VERT" in message[1] or "PASS" in message[1]:
                        genre = "vert"
                    elif ("CHEC" in message[1] or "ECHEC" in message[1]
                          or "refus" in message[1].lower()
                          or "ABSENT" in message[1]):
                        genre = "rouge"
                    self.journal.ajoute(message[1], genre)
                elif message[0] == "fin":
                    _, nom_acte, code, erreur, lignes, marque = message
                    self._fin_acte(nom_acte, code, erreur, lignes, marque)
        except queue.Empty:
            pass
        self.racine.after(80, self._pomper)

    def _fin_acte(self, nom_acte, code, erreur, lignes, marque):
        self.acte_en_cours = False
        self._bloquer_actes(False)
        if erreur:
            self.journal.ajoute(f"ÉCHEC NOMMÉ — {erreur}", "rouge")
            self.barre_verdict.configure(
                text=f"{nom_acte} : IMPOSSIBLE", foreground=COULEUR_ROUGE)
            ENREGISTREUR.ligne(f"acte impossible : {erreur}", "refus")
            return
        marque_presente = any(marque in l for l in lignes)
        if code == 0 and not marque_presente:
            self.journal.ajoute(
                f"— {nom_acte} : code 0 SANS la marque attendue "
                f"« {marque} » dans le flux — état NOMMÉ, rapportez-le —",
                "rouge")
            self.barre_verdict.configure(
                text=f"{nom_acte} : SANS VERDICT (code {code})",
                foreground=COULEUR_ROUGE)
            ENREGISTREUR.ligne(
                f"acte sans marque : code {code}, marque absente", "essai")
            return
        vert = (code == 0 and marque_presente)
        couleur = COULEUR_VERTE if vert else COULEUR_ROUGE
        self.journal.ajoute(
            f"— VERDICT {nom_acte} : {'VERT' if vert else 'ROUGE'} "
            f"(code de sortie {code}, marque « {marque} » "
            f"{'vue' if marque_presente else 'ABSENTE'} dans le flux) —",
            "vert" if vert else "rouge")
        self.barre_verdict.configure(
            text=f"{nom_acte} : {'VERT' if vert else 'ROUGE'}",
            foreground=couleur)
        ENREGISTREUR.ligne(
            f"verdict {nom_acte} : {'VERT' if vert else 'ROUGE'} "
            f"(code {code})", "verdict")
        if vert and "migration" in nom_acte:
            self.journal.ajoute(
                "→ onglet 2 : verdict à froid (recoupez le checksum avec "
                "la CARTE du sachet), puis onglet 3 : destruction "
                "EXPLICITE du conteneur CF2 — à votre rythme, le CF2 "
                "reste intact jusqu'à votre geste.", "info")

    # --- rapport (D113, systématisé D122) ---------------------------
    def constituer_rapport(self):
        """Le rapport complet, UNE seule vérité au niveau module
        (constituer_rapport_complet — prouvée headless par le
        selftest) : la classe ne fournit que son journal d'écran."""
        return constituer_rapport_complet(
            self.journal.texte.get("1.0", "end"))

    def envoyer_rapport(self):
        """D113/D122 — le rapport part par la main de l'humain :
        fichier .txt + presse-papiers + dossier ouvert. AUCUN réseau ;
        AUCUN secret (la phrase ne figure nulle part : stdin, jamais
        échoée, jamais consignée)."""
        ENREGISTREUR.ligne("bouton « Envoyer le rapport » actionné",
                           "envoi")
        rapport = self.constituer_rapport()
        fenetre = tk.Toplevel(self.racine)
        fenetre.title("Envoyer le rapport de migration CF3 (D113/D122)")
        fenetre.geometry("880x560")
        fenetre.transient(self.racine)
        zone = ttk.Frame(fenetre, padding=8)
        zone.pack(fill="both", expand=True)
        barre = ttk.Frame(zone)
        barre.pack(fill="x", pady=(0, 4))

        def copier():
            self.racine.clipboard_clear()
            self.racine.clipboard_append(rapport)
            self.journal.ajoute("[GUI] rapport copié dans le "
                                "presse-papiers", "info")
            ENREGISTREUR.ligne("rapport copié dans le presse-papiers",
                               "envoi")

        def enregistrer():
            horodatage = datetime.datetime.now().strftime(
                "%Y%m%d-%H%M%S")
            bureau = os.path.join(os.path.expanduser("~"), "Desktop")
            chemin = filedialog.asksaveasfilename(
                parent=fenetre,
                title="Enregistrer le rapport de migration CF3",
                defaultextension=".txt",
                initialfile=f"rapport-migration-cf3-{horodatage}.txt",
                initialdir=bureau if os.path.isdir(bureau)
                else os.path.expanduser("~"),
                filetypes=[("Rapport", "*.txt"), ("Tout", "*.*")])
            if not chemin:
                return
            try:
                with open(chemin, "w", encoding="utf-8") as f:
                    f.write(rapport + "\n")
            except OSError as exc:
                self._dialogue("showerror", "Écriture impossible",
                               f"{chemin} :\n{exc}")
                return
            self.journal.ajoute(f"[GUI] rapport écrit : {chemin}", "info")
            ENREGISTREUR.ligne(f"rapport écrit : {chemin}", "envoi")
            self._dialogue(
                "showinfo", "Rapport écrit",
                f"Rapport écrit :\n  {chemin}\n\nPour l'envoyer à "
                "l'assistant : glissez ce fichier dans la conversation "
                "(ou collez le presse-papiers).")

        def ouvrir_dossier():
            dossier = (os.path.dirname(CHEMIN_JOURNAL_VOL)
                       or os.path.expanduser("~"))
            ENREGISTREUR.ligne(
                f"dossier de la boîte noire ouvert : {dossier}", "envoi")
            try:
                if sys.platform.startswith("win"):
                    os.startfile(dossier)   # noqa: S606
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", dossier])
                else:
                    subprocess.Popen(["xdg-open", dossier])
            except OSError as exc:
                self._dialogue("showwarning", "Ouverture impossible",
                               f"{dossier} :\n{exc}")

        ttk.Button(barre, text="Copier tout le rapport",
                   command=copier).pack(side="left")
        ttk.Button(barre, text="Enregistrer sous (.txt)…",
                   command=enregistrer).pack(side="left", padx=6)
        ttk.Button(barre, text="Ouvrir le dossier de la boîte noire",
                   command=ouvrir_dossier).pack(side="left")
        texte = tk.Text(zone, wrap="word", font=POLICE_FIXE)
        barre_d = ttk.Scrollbar(zone, orient="vertical",
                                command=texte.yview)
        texte.configure(yscrollcommand=barre_d.set)
        barre_d.pack(side="right", fill="y")
        texte.pack(side="left", fill="both", expand=True)
        texte.insert("1.0", rapport)
        texte.configure(state="disabled")
        ttk.Label(zone, wraplength=820, justify="left",
                  text=("AUCUN réseau — le rapport part par vos mains : "
                        "glissez le fichier .txt dans la conversation de "
                        "l'assistant. Il contient l'environnement, les "
                        "empreintes des modules, le journal d'écran et "
                        "la boîte noire : de quoi diagnostiquer à "
                        "distance. Aucun secret n'y figure — la phrase "
                        "ne quitte jamais votre machine.")
                  ).pack(fill="x", pady=(4, 0))

    def _dialogue(self, genre, titre, message, **options):
        """Toujours AU-DESSUS (parent) et consigné dans la boîte noire
        (D113 — les dialogues ne contiennent jamais un secret)."""
        ENREGISTREUR.ligne(f"dialogue « {titre} » posé", "dialogue")
        reponse = getattr(messagebox, genre)(titre, message,
                                             parent=self.racine,
                                             **options)
        ENREGISTREUR.ligne(f"dialogue « {titre} » → {reponse!r}",
                           "dialogue")
        return reponse

    def _crash(self, exc_type, valeur, tb):
        """D113 : un crash de rappel tkinter est un échec NOMMÉ à
        l'écran + le traceback complet dans la boîte noire."""
        ENREGISTREUR.traceback()
        self.journal.ajoute(
            f"CRASH du GUI — {exc_type.__name__} : {valeur} "
            "(traceback complet dans la boîte noire — envoyez le "
            "rapport)", "rouge")


def demarrer_gui():
    """Point d'entrée fenêtre — retourne le code de sortie tkinter.
    Le tk.Tk() ne vit QUE ici (preuve structurelle : l'import du module
    ne crée jamais de fenêtre)."""
    if not TKINTER_DISPONIBLE:
        print(_message_tkinter_manquant(), file=sys.stderr)
        return 3
    racine = tk.Tk()
    Application(racine)
    racine.mainloop()
    return 0


# ===========================================================================
# SECTION D — selftest headless : le GUI se prouve lui-même.
# ===========================================================================

def selftest():
    """Batterie embarquée : boîte noire vivante, empreintes, relais
    SOUS-PROCESSUS réel d'une migration COMPLÈTE de laboratoire (CF1 →
    CF2 par les vérités vivantes, puis migrer/verifier/detruire-cf2
    relayés), verdict croisé (menteux / muet), phrase JAMAIS dans le
    rapport, refus nommés, AUCUNE voie réseau dans le source. True ssi
    tout passe."""
    import json
    import shutil
    import tempfile
    import time

    passes, echecs = [], []

    def controle(nom, ok, detail=""):
        (passes if ok else echecs).append(nom if ok else f"{nom} ({detail})")
        print(f"  {'PASS' if ok else 'ÉCHEC'} {nom}"
              + (f" — {detail}" if detail and not ok else ""))

    print(f"[selftest] {VERSION_GUI} — batterie headless (temporaire)")
    ENREGISTREUR.entete()

    # 1 — boîte noire vivante
    try:
        ENREGISTREUR.ligne("selftest : la boîte noire écrit-elle ?", "essai")
        with open(CHEMIN_JOURNAL_VOL, "r", encoding="utf-8") as f:
            controle("boîte noire vivante",
                     "selftest : la boîte noire écrit-elle ?" in f.read())
    except OSError as exc:
        controle("boîte noire vivante", False, str(exc))

    # 2 — empreintes nommées (coffre_fort.py est un état NOMMÉ, pas une
    #     panne : il ne sert qu'à CF1 → CF2 — la cérémonie CF2 → CF3
    #     n'en a pas besoin)
    empreintes = empreintes_modules()
    requis = {"coffre_cf3.py", "coffre_cf2.py", "migration_cf3_gui.py"}
    controle("empreintes : vérités requises présentes",
             all(e is not None for nom, e in empreintes if nom in requis),
             ", ".join(nom for nom, e in empreintes
                        if nom in requis and e is None) or "")

    # 3 — la cérémonie COMPLÈTE de laboratoire, relayée (relais réel).
    #     La fixture passe par la vérité vivante CF2 (cmd_init : coffre
    #     neuf — AUCUN besoin de coffre_fort.py, le kit PLAT se prouve
    #     aussi) ; une vérité absente est NOMMÉE, jamais un crash.
    bac = tempfile.mkdtemp(prefix="selftest-migr-cf3-")
    try:
        cf2_bin = os.path.join(bac, "coffre_cf2.bin")
        cf3_bin = os.path.join(bac, "coffre_cf3.bin")
        gardes = os.path.join(bac, "gardes")
        cfg = os.path.join(bac, "config_cf2.json")
        media = os.path.join(bac, "media-piege")
        os.makedirs(media)
        try:
            import coffre_cf2 as _cf2         # l'instance que coffre_cf3 relaye
            from types import SimpleNamespace
            _cf2.cmd_init(SimpleNamespace(
                fragments=5, seuil=3, conteneur=cf2_bin,
                racine_gardes=gardes, config=cfg,
                description_projet="selftest migration-CF3-GUI"))
            config = _cf2.lire_config(cfg)
            config["journal"] = os.path.join(bac, "journal-s.txt")
            config["heartbeat"] = os.path.join(bac, "heartbeat.txt")
            config["pv_dir"] = os.path.join(bac, "pv-cf2")
            _cf2.ecrire_config(cfg, config)
            with open(config["heartbeat"], "w", encoding="utf-8") as f:
                json.dump({"ts": time.time()}, f)
            prets, detail_prets = True, ""
        except (ImportError, RuntimeError) as exc:
            prets, detail_prets = False, str(exc)
        controle("vérités vivantes présentes (coffre_cf2 à côté du GUI)",
                 prets, detail_prets)

        lignes, l2 = [], []
        if prets:
            arguments = ["migrer", "--conteneur-cf2", cf2_bin,
                         "--config-cf2", cfg, "--piege-dir", media,
                         "--conteneur", cf3_bin, "--phrase-stdin"]
            relais = RelaisEssais()
            lignes = relais.lancer(chemin_cible("coffre_cf3.py"), arguments,
                                   entree_stdin="phrase-selftest-migr\n")
            controle("relais migrer : code 0", relais.code == 0,
                     f"code={relais.code}")
            controle("relais migrer : VERDICT VERT dans le flux",
                     any("VERDICT : VERT" in l for l in lignes))
            controle("relais migrer : la commande porte -u (D124)",
                     relais.commande is not None
                     and "-u" in relais.commande)
            controle("relais migrer : la phrase n'est PAS dans la commande",
                     relais.commande is not None
                     and all("phrase-selftest-migr" not in str(a)
                             for a in relais.commande))

            r2 = RelaisEssais()
            l2 = r2.lancer(chemin_cible("coffre_cf3.py"),
                           ["verifier", "--piege-dir", media,
                            "--conteneur", cf3_bin, "--phrase-stdin"],
                           entree_stdin="phrase-selftest-migr\n")
            controle("relais verifier : code 0 + VERT",
                     r2.code == 0 and any("VERDICT : VERT" in l for l in l2))

            r3 = RelaisEssais()
            l3 = r3.lancer(chemin_cible("coffre_cf3.py"),
                           ["detruire-cf2", "--conteneur-cf2", cf2_bin,
                            "--conteneur", cf3_bin, "--oui-je-comprends"])
            controle("relais detruire-cf2 : code 0 + DÉTRUIT",
                     r3.code == 0 and any("DÉTRUIT" in l for l in l3))
            controle("relais detruire-cf2 : le CF2 est bien mort",
                     not os.path.isfile(cf2_bin))

            # 6 — le rapport N'EMPORTE PAS la phrase : la preuve que le
            #     trio ne fuit pas son secret
            rapport = constituer_rapport_complet(
                "\n".join(lignes) + "\n" + "\n".join(l2))
            controle("rapport : entête + empreintes + boîte noire",
                     VERSION_GUI in rapport
                     and "empreintes md5" in rapport
                     and "JOURNAL DE VOL" in rapport)
            controle("rapport : la phrase n'y figure JAMAIS",
                     "phrase-selftest-migr" not in rapport)

        # 4 — verdict croisé : un enfant MENTEUR (affiche la marque,
        #     sort 1) est ROUGE ; un enfant MUET est SANS VERDICT
        menteur = os.path.join(bac, "menteur.py")
        with open(menteur, "w", encoding="utf-8") as f:
            f.write("print('[menteur] VERDICT : VERT — époque 1')\n"
                    "raise SystemExit(1)\n")
        r4 = RelaisEssais()
        l4 = r4.lancer(menteur)
        controle("verdict croisé : menteux détecté (code 1)",
                 r4.code == 1 and any("VERT" in l for l in l4))
        muet = os.path.join(bac, "muet.py")
        with open(muet, "w", encoding="utf-8") as f:
            f.write("print('(silence)')\n")
        r5 = RelaisEssais()
        l5 = r5.lancer(muet)
        controle("verdict croisé : muet détecté (pas de marque)",
                 r5.code == 0 and not any("VERDICT" in l for l in l5))

        # 5 — refus nommé : cible absente
        r6 = RelaisEssais()
        r6.lancer(os.path.join(bac, "introuvable.py"))
        controle("cible absente : refus NOMMÉ",
                 r6.erreur is not None and "introuvable" in r6.erreur)
    finally:
        shutil.rmtree(bac, ignore_errors=True)

    # 7 — aucune voie réseau dans le source (le transport est humain) :
    #     contrôle STRUCTUREL par AST (les importations réelles), pas par
    #     sous-chaîne — la chaîne de recherche se trouverait elle-même
    import ast
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        source = f.read()
    importations = set()
    for noeud in ast.walk(ast.parse(source)):
        if isinstance(noeud, ast.Import):
            importations.update(alias.name.split(".")[0]
                                for alias in noeud.names)
        elif isinstance(noeud, ast.ImportFrom) and noeud.module:
            importations.add(noeud.module.split(".")[0])
    controle("aucune voie réseau dans le source (AST)",
             not importations & {"socket", "urllib", "requests", "http",
                                 "ftplib", "smtplib", "telnetlib"},
             ", ".join(sorted(importations & {"socket", "urllib",
                                             "requests", "http"})))

    # 9 — disposition D132 : dans les onglets, le bouton « Parcourir… »
    #     vit SUR LA LIGNE de grille de SON champ (le terrain a dénoncé
    #     des boutons empilés en colonne à droite, loin de leurs champs
    #     — retour 31/10 : « les boutons de recherche de fichiers ne
    #     sont pas alignés aux champs concernés »). Preuve structurelle
    #     AST : dans _champ, le Entry et le Button partagent la MÊME
    #     ligne (row), dans des colonnes DISTINCTES — un retour au pack
    #     side="right" ferait échouer ce contrôle.
    def _mots_cles_grid(noeud, nom_widget):
        """Les mots-clés du .grid(...) attaché à ttk.<nom_widget>(...)."""
        for expression in ast.walk(noeud):
            if not (isinstance(expression, ast.Call)
                    and isinstance(expression.func, ast.Attribute)
                    and expression.func.attr == "grid"):
                continue
            constructeur = expression.func.value
            if (isinstance(constructeur, ast.Call)
                    and isinstance(constructeur.func, ast.Attribute)
                    and constructeur.func.attr == nom_widget
                    and constructeur.args
                    and isinstance(constructeur.args[0], ast.Name)):
                return {mot.arg: ast.dump(mot.value)
                        for mot in expression.keywords}
        return None

    arbre_source = ast.parse(source)
    fonction_champ = next(
        (n for n in ast.walk(arbre_source)
         if isinstance(n, ast.FunctionDef) and n.name == "_champ"), None)
    grille_entree = (_mots_cles_grid(fonction_champ, "Entry")
                     if fonction_champ else None)
    grille_bouton = (_mots_cles_grid(fonction_champ, "Button")
                     if fonction_champ else None)
    controle("disposition : champ et bouton « Parcourir… » sur la même "
             "ligne de grille (D132)",
             grille_entree is not None and grille_bouton is not None
             and grille_entree.get("row") == grille_bouton.get("row")
             and grille_entree.get("column") != grille_bouton.get("column"),
             f"Entry/grid={grille_entree!r} Button/grid={grille_bouton!r}")

    # 8 — phrases_coherentes : la confirmation de l'onglet MIGRER
    controle("phrases divergentes refusées nommément",
             phrases_coherentes("a", "b") == (False, "les deux phrases "
                                              "DIVERGENT — recomposez "
                                              "(un scellé sous une phrase "
                                              "typée ne s'ouvrirait plus "
                                              "sous la phrase pensée)"))
    controle("phrase vide refusée",
             phrases_coherentes("", "")[0] is False)

    total = len(passes) + len(echecs)
    print(f"[selftest] {len(passes)} PASS / {len(echecs)} ÉCHEC "
          f"sur {total} contrôles")
    return not echecs


def main():
    parseur = argparse.ArgumentParser(
        description=f"GUI de cérémonie de migration CF2 → CF3 — {VERSION_GUI}")
    parseur.add_argument("--selftest", action="store_true",
                         help="batterie headless (le GUI se prouve lui-même)")
    parseur.add_argument("--v06", default=None,
                         help="dossier v06 alternatif (échec NOMMÉ si "
                              "introuvable)")
    arguments = parseur.parse_args()
    global CHEMIN_V06, RACINE_DEPOT, CONTENEUR_CF2_DEFAUT
    global CONTENEUR_CF3_DEFAUT, ENREGISTREUR, CHEMIN_JOURNAL_VOL
    if arguments.v06:
        CHEMIN_V06 = _resoudre_v06(arguments.v06)
        RACINE_DEPOT = os.path.dirname(CHEMIN_V06)
        CONTENEUR_CF2_DEFAUT = os.path.join(RACINE_DEPOT, ".keys",
                                            "coffre_cf2.bin")
        CONTENEUR_CF3_DEFAUT = os.path.join(RACINE_DEPOT, ".keys",
                                            "coffre_cf3.bin")
        CHEMIN_JOURNAL_VOL = os.path.join(CHEMIN_V06, NOM_JOURNAL_VOL)
        ENREGISTREUR = Enregistreur(CHEMIN_JOURNAL_VOL)
    if arguments.selftest:
        return 0 if selftest() else 1
    return demarrer_gui()


if __name__ == "__main__":
    sys.exit(main())
