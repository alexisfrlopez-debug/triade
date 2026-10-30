#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""autotest_cf3_gui.py — le PUPITRE D'AUTOTEST CF3 (D122).

POURQUOI CE MODULE EXISTE. Le terrain s'apprête à prouver la serrure CF3
(docs/I/CF3/README.md, D121). Un autotest en ligne de commande rend son
verdict à l'écran, puis le verdict S'ÉVANOUIT : si quelque chose se passe
mal sur la machine du développeur (pile pip absente, encodage Windows,
version périmée du module), je ne reçois RIEN à analyser. La demande du
terrain (D122) est désormais une RÈGLE SYSTÉMATIQUE : tout module livré
pour être testé porte (1) une INTERFACE GRAPHIQUE, (2) une BOÎTE NOIRE
locale (journal de vol horodaté), (3) un bouton « Envoyer le rapport… »
qui prépare un fichier .txt complet — le transport reste la main de
l'humain (glisser le fichier dans la conversation), AUCUN réseau (le
trio D113, généralisé par décision D122).

CE QUE LE PUPITRE FAIT :

  1. DIAGNOSTIC D'ENVIRONNEMENT AVANT TOUT TEST — l'écran affiche : OS,
     Python, interpréteur, pile du dépôt (argon2-cffi / PyNaCl /
     cryptography, version ou ABSENT nommé), et les EMPREINTES md5 des
     modules CF3 présents (coffre_cf3.py, coffre_cf2.py,
     test_coffre_cf3.py, ce pupitre). Un rapport qui me parvient me dit
     donc EXACTEMENT quelle génération de code a tourné — le diagnostic
     « pas à jour » devient une lecture, plus une devinette.
  2. DEUX BOUTONS D'ESSAI, relais sous-processus (le pupitre ne réimplémente
     RIEN, il lance les vérités vivantes) :
       - « Autotest CF3 embarqué » → python v06/coffre_cf3.py autotest
         (28 contrôles, ~3 s, temporaires, AUCUN coffre réel touché) ;
       - « Suite de falsifiabilité CF3 » → python v06/test_coffre_cf3.py
         (92 contrôles, ~10-30 s selon machine).
     La sortie coule ligne à ligne dans le journal (écran + boîte noire),
     le verdict final est compté DEPUIS LE FLUX (PASS / ÉCHEC) et croisé
     avec le code de sortie — un mensonge d'un des deux serait visible.
  3. BOÎTE NOIRE : chaque ligne affichée, chaque dialogue posé/résolu et
     CHAQUE crash de rappel tkinter atterrissent dans
     v06/autotest-cf3-journal.log (local, horodaté, aucun réseau). Un
     échec d'écriture ne gêne JAMAIS les essais : la boîte noire est un
     témoin, pas une dépendance.
  4. « Envoyer le rapport… » (D113) : entête d'environnement complet +
     journal d'écran + journal de vol → Enregistrer sous .txt +
     presse-papiers + ouvrir le dossier. Le fichier se glisse dans la
     conversation — c'est le transport humain, hors-ligne.

ENCODEAGE : les enfants sont lancés avec PYTHONIOENCODING=utf-8 et lus en
UTF-8 remplacé — les « É » des verdicts survivent au cp850 de Windows.

FLUX (D124) : les enfants sont lancés « python -u », stdout NON tamponné,
et PYTHONUNBUFFERED ambiant est NEUTRALISÉ — le drapeau VISIBLE décide
seul. Pourquoi : pipé, le stdout d'un enfant Python se tamponne par BLOCS
— la boîte noire horodate l'ARRIVÉE des lignes, pas leur émission (le
rapport terrain du 30/10 12:13 en portait la trace : 22 secondes de
suite collapsées sur un seul horodatage, 12:13:31). Pire : un enfant qui
meurt BRUTALEMENT (crash natif, mémoire fautive) emporte son tampon —
les DERNIÈRES lignes, celles qui précèdent le crash et disent son nom,
ne parviendraient JAMAIS au journal. Avec -u chaque écriture est
immédiate : le journal de vol devient fidèle ET survivant au crash de
ce qu'il observe. Nota : le défaut était INVISIBLE au laboratoire
(variable PYTHONUNBUFFERED ambiante qui tamponnait tout en vert) — seul
le terrain l'a montré : le pupitre ne laisse plus l'ambiance décider.
Le drapeau est du PUPITRE, pas des vérités vivantes — coffre_cf3.py,
test_coffre_cf3.py et coffre_cf2.py ne changent pas d'un octet, leurs
verdicts restent acquis.

EMPLACEMENT : ce pupitre vit dans v06/ (dépôt complet OU kit du Drive —
le kit porte v06/ entier depuis D122) et attend coffre_cf3.py À CÔTÉ de
lui ; --v06 CHEMIN le pointe ailleurs (échec NOMMÉ si introuvable, jamais
un repli silencieux).

Modes : (aucun) → fenêtre ; --selftest → batterie headless (le pupitre
se prouve lui-même : boîte noire vivante, rapport complet, relais réel
28 PASS compté depuis le flux, refus nommés).
"""

import argparse
import datetime
import hashlib
import os
import platform
import queue
import re
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


VERSION_PUPITRE = "autotest-CF3-GUI v1.2 (D124)"

NOM_JOURNAL_VOL = "autotest-cf3-journal.log"


# ===========================================================================
# SECTION 0 — D113/D122 : L'ENREGISTREUR DE VOL (boîte noire). Tout ce que
# le pupitre dit, fait, et chaque crash atterrit dans un journal LOCAL
# horodaté, à côté du fichier lui-même. AUCUN réseau ; aucune donnée
# secrète (les essais vivent sur des coffres de laboratoire en temporaires
# — D105 ; la phrase d'autotest est publique, dans le source).
# ===========================================================================

CHEMIN_JOURNAL_VOL = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), NOM_JOURNAL_VOL)


class Enregistreur:
    """Boîte noire locale : append horodaté, une ligne = un fait. Un échec
    d'écriture (disque en lecture seule) ne gêne JAMAIS les essais."""

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
        self.ligne(f"DEMARRAGE {VERSION_PUPITRE}", "entete")
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
                f"[autotest-CF3-GUI] ÉCHEC — le dossier v06 indiqué "
                f"n'existe pas : {candidat}")
        return candidat
    return os.path.dirname(os.path.abspath(__file__))


CHEMIN_V06 = _resoudre_v06(None)

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
    paquet n'est pas installé. La version d'argon2 par attribute est
    DÉPRÉCIÉE : les métadonnées sont la voie stable."""
    try:
        from importlib import metadata as _meta
        return _meta.version(nom_pip)
    except Exception:
        return None


def pile_pip():
    """[(nom pip, version ou None)] — le None est un état NOMMÉ (absent),
    pas un crash : le pupitre doit s'ouvrir et le DIRE même sans pile."""
    return [(nom, _version_paquet(nom)) for nom, _ in PILE_PIP]


def pile_complete():
    return all(v is not None for _, v in pile_pip())


MODULES_EMPREINTES = ("coffre_cf3.py", "coffre_cf2.py",
                      "test_coffre_cf3.py", "autotest_cf3_gui.py")


def empreintes_modules():
    """[(nom, md5 ou None)] des modules CF3 du dossier v06 — None = absent
    (nommé). Le rapport distant saura quelle GÉNÉRATION a tourné."""
    empreintes = []
    for nom in MODULES_EMPREINTES:
        chemin = os.path.join(CHEMIN_V06, nom)
        if os.path.isfile(chemin):
            try:
                with open(chemin, "rb") as f:
                    empreintes.append((nom, hashlib.md5(f.read()).hexdigest()))
            except OSError:
                empreintes.append((nom, None))
        else:
            empreintes.append((nom, None))
    return empreintes


def _md5_si_present(nom):
    for nom_f, empreinte in empreintes_modules():
        if nom_f == nom:
            return empreinte
    return None


def texte_pile():
    """La pile en UNE ligne lisible (journal + rapport)."""
    morceaux = [f"{nom} {v if v else 'ABSENT'}" for nom, v in pile_pip()]
    return " · ".join(morceaux) + ("  [pile COMPLÈTE]" if pile_complete()
                                   else "  [pile INCOMPLÈTE]")


def chemin_cible(nom):
    """Chemin d'un module du dossier v06 — l'échec est nommé par l'appelant."""
    return os.path.join(CHEMIN_V06, nom)


def suite_disponible():
    """La suite COMPLÈTE (test_coffre_cf3.py) exige la posture « dossier
    v06/ » (dépôt complet ou kit du Drive) : elle s'importe par
    « from v06 import coffre_cf3 » — en copie PLATE (pupitre et modules
    posés à côté d'un lanceur, sans dossier v06/ ni __init__.py), seul
    l'autotest EMBARQUÉ (28 contrôles) a un sens. Le refus est NOMMÉ
    AVANT le lancement, jamais un crash d'import dans le journal."""
    return (os.path.isfile(os.path.join(CHEMIN_V06, "__init__.py"))
            and os.path.isfile(chemin_cible("test_coffre_cf3.py")))


def constituer_rapport_complet(texte_ecran):
    """Le rapport D113/D122, au niveau MODULE (prouvable headless) :
    entête d'environnement + empreintes + journal d'écran + boîte noire.
    La classe GUI ne fait que passer son journal d'écran — le reste est
    UNE seule vérité, testée par le selftest sans fenêtre."""
    lignes = [
        "RAPPORT D'AUTOTEST CF3 — " + VERSION_PUPITRE,
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
# SECTION B — le relais sous-processus. Le pupitre ne réimplémente RIEN :
# il lance les vérités vivantes (coffre_cf3.py autotest, test_coffre_cf3.py)
# et laisse leur sortie couler. Le fil ouvrier NE TOUCHE JAMAIS tkinter
# (discipline maison D118) : il dépose ses lignes dans une file, le fil
# tkinter les pompe.
# ===========================================================================

_MOTIF_VERDICT = re.compile(r"(\d+)\s+PASS\s+/\s+(\d+)\s+[ÉE]CHEC")


def compter_verdict(lignes):
    """Compte PASS/ÉCHEC DEPUIS LE FLUX (la dernière ligne de verdict de
    l'enfant). None si l'enfant n'a rien verdicté — c'est un fait nommé,
    pas un zéro."""
    comptes = None
    for ligne in lignes:
        trouve = _MOTIF_VERDICT.search(ligne)
        if trouve:
            comptes = (int(trouve.group(1)), int(trouve.group(2)))
    return comptes


class RelaisEssais:
    """Lance un essai en sous-processus, streame sa sortie ligne à ligne.

    usage (headless, comme le selftest) :
        relais = RelaisEssais()
        lignes = relais.lancer(chemin_script)
        lignes → liste des lignes émises ; relais.code → code de sortie ;
        relais.erreur → message d'échec nommé (lancement impossible).

    usage (GUI) : lancer(chemin, emit=callback) — callback appelé depuis
    le FIL OUVRIER (il ne doit toucher ni tkinter ni le journal écran).
    """

    def __init__(self):
        self.code = None
        self.erreur = None

    def lancer(self, chemin_script, arguments=None, emit=None):
        """Exécute [sys.executable, "-u", chemin_script] + arguments dans
        le dossier v06. PYTHONIOENCODING=utf-8 : les accents des verdicts
        survivent au cp850 de Windows (l'enfant ne reconfigure pas
        lui-même). « -u » (D124) : stdout de l'enfant NON tamponné — la
        boîte noire horodate l'émission réelle et un crash brutal de
        l'enfant ne peut plus emporter ses dernières lignes dans un
        tampon mort. PYTHONUNBUFFERED ambiant est retiré : le drapeau
        visible décide seul (au laboratoire, cette variable ambiante
        rendait tout non tamponné — vert — et MASQUAIT le défaut que
        seul le terrain a montré).
        Le drapeau relève du pupitre : les vérités vivantes ne changent
        pas d'un octet."""
        self.code, self.erreur = None, None
        if not os.path.isfile(chemin_script):
            self.erreur = (f"essai impossible : {chemin_script} introuvable "
                           f"— le pupitre vit dans v06/ (dépôt complet ou "
                           "kit du Drive) auprès de coffre_cf3.py")
            return []
        environnement = dict(os.environ)
        environnement["PYTHONIOENCODING"] = "utf-8"
        # D124 : le drapeau VISIBLE (-u dans la commande affichée au
        # rapport) décide seul — une variable ambiante ne peut ni le
        # remplacer ni le masquer (au labo, PYTHONUNBUFFERED=1 ambiant
        # rendait tout vert et cachait le tampon que le terrain a vu).
        environnement.pop("PYTHONUNBUFFERED", None)
        commande = [sys.executable, "-u", chemin_script] + list(arguments or [])
        lignes = []
        try:
            processus = subprocess.Popen(
                commande,
                cwd=CHEMIN_V06, env=environnement,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                bufsize=1)
        except OSError as exc:
            self.erreur = f"essai impossible : lancement échoué — {exc}"
            return lignes
        for ligne in processus.stdout:
            ligne = ligne.rstrip("\n").rstrip("\r")
            lignes.append(ligne)
            if emit:
                try:
                    emit(ligne)
                except Exception:
                    pass   # un témoin d'écriture ne doit pas tuer l'essai
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


class Journal:
    """Journal d'écran : trace textuelle des essais (la preuve reste
    aux suites lancées — le journal est pour l'humain ET pour le
    rapport). Chaque ligne voit AUSSI la boîte noire."""

    def __init__(self, parent, application):
        self.app = application
        cadre = ttk.LabelFrame(parent, text="Journal des essais")
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


class Application:
    """Le pupitre : environnement, deux essais relais, rapport."""

    def __init__(self, racine):
        self.racine = racine
        racine.title(f"TRIADE — pupitre d'autotest CF3 ({VERSION_PUPITRE})")
        racine.geometry("980x680")
        racine.minsize(760, 520)
        self.file_messages = queue.Queue()
        self.essai_en_cours = False
        self._construire()
        racine.report_callback_exception = self._crash
        ENREGISTREUR.entete(racine)
        self.journal.ajoute(VERSION_PUPITRE, "titre")
        self.journal.ajoute(
            "le pupitre ne réimplémente rien : il lance les vérités "
            "vivantes (coffre_cf3.py autotest, test_coffre_cf3.py) et "
            "leur sortie coule ci-dessous.", "info")
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
        if absents:
            self.journal.ajoute(
                "modules CF3 absents du dossier v06 : "
                + ", ".join(absents)
                + " — les essais correspondants seront des refus NOMMÉS",
                "rouge")
        self.racine.after(80, self._pomper)

    # --- construction -----------------------------------------------
    def _construire(self):
        bandeau = ttk.Frame(self.racine, padding=(10, 8))
        bandeau.pack(fill="x")
        ttk.Label(bandeau, text="Pupitre d'autotest CF3",
                  font=("TkDefaultFont", 14, "bold")).pack(side="left")
        ttk.Label(bandeau, text="   " + VERSION_PUPITRE
                  ).pack(side="left", padx=(6, 0))

        # --- l'environnement, AVANT tout essai (D122 : le rapport
        # doit dire quelle machine, quelle pile, quelle GÉNÉRATION)
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
                      foreground=COULEUR_ENCRE
                      ).pack(anchor="w")
        if not pile_complete():
            ttk.Label(env, foreground=COULEUR_ROUGE, font=POLICE_FIXE,
                      text=("pile INCOMPLÈTE — pip install argon2-cffi "
                            "pynacl cryptography")).pack(anchor="w")

        actions = ttk.Frame(self.racine, padding=(10, 4))
        actions.pack(fill="x")
        self.bouton_autotest = ttk.Button(
            actions, text="Lancer l'autotest CF3 (embarqué, 28 contrôles)",
            command=self.lancer_autotest)
        self.bouton_autotest.pack(side="left")
        self.bouton_suite = ttk.Button(
            actions, text="Lancer la suite de falsifiabilité (92 contrôles)",
            command=self.lancer_suite)
        self.bouton_suite.pack(side="left", padx=(6, 0))
        self.barre_verdict = ttk.Label(
            actions, text="aucun essai lancé", anchor="e",
            font=(POLICE_FIXE[0], 10, "bold"))
        self.barre_verdict.pack(side="right")

        self.journal = Journal(self.racine, self)

    # --- essais (le fil tkinter décide, l'ouvrier transmet) ---------
    def _bloquer_essais(self, bloquer):
        etat = "disabled" if bloquer else "normal"
        self.bouton_autotest.configure(state=etat)
        self.bouton_suite.configure(state=etat)

    def lancer_autotest(self):
        self._lancer("coffre_cf3.py", ["autotest"],
                     "autotest embarqué")

    def lancer_suite(self):
        if not suite_disponible():
            self.journal.ajoute(
                "ÉCHEC NOMMÉ — la suite complète vit dans le dossier "
                "v06/ d'un dépôt complet ou du kit du Drive "
                "(__init__.py requis) ; en copie plate, seul "
                "l'autotest EMBARQUÉ (28 contrôles) est disponible — "
                "la posture est dite, pas devinée", "rouge")
            ENREGISTREUR.ligne("suite refusée : posture copie plate",
                               "refus")
            self.barre_verdict.configure(
                text="suite : posture insuffisante (copie plate)",
                foreground=COULEUR_ROUGE)
            return
        self._lancer("test_coffre_cf3.py", [],
                     "suite de falsifiabilité")

    def _lancer(self, nom_script, arguments, nom_essai):
        if self.essai_en_cours:
            self.journal.ajoute("un essai court déjà — attendez son "
                                "verdict (les essais ne se mélangent pas)",
                                "rouge")
            return
        chemin = chemin_cible(nom_script)
        if not os.path.isfile(chemin):
            self.journal.ajoute(
                f"ÉCHEC NOMMÉ — {nom_script} introuvable : {chemin} "
                "(le pupitre vit dans v06/ du dépôt complet ou du kit "
                "du Drive)", "rouge")
            ENREGISTREUR.ligne(f"essai refusé : {nom_script} introuvable",
                               "refus")
            self.barre_verdict.configure(
                text=f"{nom_essai} : IMPOSSIBLE (module absent)",
                foreground=COULEUR_ROUGE)
            return
        self.essai_en_cours = True
        self._bloquer_essais(True)
        self.barre_verdict.configure(text=f"{nom_essai} : en cours…",
                                     foreground=COULEUR_ENCRE)
        commande_affichee = f"{sys.executable} -u {nom_script}"
        if arguments:
            commande_affichee += " " + " ".join(arguments)
        self.journal.ajoute(f"— {nom_essai} : lancement "
                            f"({commande_affichee}) —", "titre")
        ENREGISTREUR.ligne(f"essai lancé : {commande_affichee}", "essai")

        def emit(ligne):
            self.file_messages.put(("ligne", ligne))

        def ouvrier():
            relais = RelaisEssais()
            lignes = relais.lancer(chemin, arguments, emit=emit)
            self.file_messages.put(("fin", nom_essai, relais.code,
                                    relais.erreur, lignes))

        threading.Thread(target=ouvrier, daemon=True).start()

    def _pomper(self):
        """Le fil tkinter SEUL touche le journal (discipline D118)."""
        try:
            while True:
                message = self.file_messages.get_nowait()
                if message[0] == "ligne":
                    genre = "info"
                    if "PASS" in message[1]:
                        genre = "vert"
                    elif "CHEC" in message[1]:
                        genre = "rouge"
                    self.journal.ajoute(message[1], genre)
                elif message[0] == "fin":
                    _, nom_essai, code, erreur, lignes = message
                    self._fin_essai(nom_essai, code, erreur, lignes)
        except queue.Empty:
            pass
        self.racine.after(80, self._pomper)

    def _fin_essai(self, nom_essai, code, erreur, lignes):
        self.essai_en_cours = False
        self._bloquer_essais(False)
        if erreur:
            self.journal.ajoute(f"ÉCHEC NOMMÉ — {erreur}", "rouge")
            self.barre_verdict.configure(
                text=f"{nom_essai} : IMPOSSIBLE",
                foreground=COULEUR_ROUGE)
            ENREGISTREUR.ligne(f"essai impossible : {erreur}", "refus")
            return
        comptes = compter_verdict(lignes)
        if comptes is None:
            self.journal.ajoute(
                f"— {nom_essai} : AUCUN verdict dans le flux "
                f"(code de sortie {code}) — état NOMMÉ, rapportez-le —",
                "rouge")
            self.barre_verdict.configure(
                text=f"{nom_essai} : SANS VERDICT (code {code})",
                foreground=COULEUR_ROUGE)
            ENREGISTREUR.ligne(
                f"essai sans verdict : code {code}", "essai")
            return
        passes, echecs = comptes
        vert = (code == 0 and echecs == 0)
        couleur = COULEUR_VERTE if vert else COULEUR_ROUGE
        self.journal.ajoute(
            f"— VERDICT {nom_essai} : {passes} PASS / {echecs} ÉCHEC "
            f"(code de sortie {code}, compté DEPUIS LE FLUX) —",
            "vert" if vert else "rouge")
        self.barre_verdict.configure(
            text=f"{nom_essai} : {'VERT' if vert else 'ROUGE'} "
                 f"— {passes} PASS / {echecs} ÉCHEC",
            foreground=couleur)
        ENREGISTREUR.ligne(
            f"verdict {nom_essai} : {passes} PASS / {echecs} ÉCHEC "
            f"(code {code})", "verdict")

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
        aucun secret (les essais vivent sur des coffres de laboratoire,
        phrase publique du source — D105)."""
        ENREGISTREUR.ligne("bouton « Envoyer le rapport » actionné",
                           "envoi")
        rapport = self.constituer_rapport()
        fenetre = tk.Toplevel(self.racine)
        fenetre.title("Envoyer le rapport d'autotest CF3 (D113/D122)")
        fenetre.geometry("880x560")
        fenetre.transient(self.racine)
        zone = ttk.Frame(fenetre, padding=8)
        zone.pack(fill="both", expand=True)
        barre = ttk.Frame(zone)
        barre.pack(fill="x", pady=(0, 4))

        def copier():
            self.racine.clipboard_clear()
            self.racine.clipboard_append(rapport)
            self.journal.ajoute("[pupitre] rapport copié dans le "
                                "presse-papiers", "info")
            ENREGISTREUR.ligne("rapport copié dans le presse-papiers",
                               "envoi")

        def enregistrer():
            horodatage = datetime.datetime.now().strftime(
                "%Y%m%d-%H%M%S")
            bureau = os.path.join(os.path.expanduser("~"), "Desktop")
            chemin = filedialog.asksaveasfilename(
                parent=fenetre,
                title="Enregistrer le rapport d'autotest CF3",
                defaultextension=".txt",
                initialfile=f"rapport-autotest-cf3-{horodatage}.txt",
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
            self.journal.ajoute(f"[pupitre] rapport écrit : {chemin}",
                                "info")
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
                        "distance. Aucun secret n'y figure.")
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
            f"CRASH du pupitre — {exc_type.__name__} : {valeur} "
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


# SECTION D — selftest headless : le pupitre se prouve lui-même.
# ===========================================================================

def selftest():
    """Batterie embarquée : boîte noire vivante, pile nommée, empreintes,
    relais SOUS-PROCESSUS réel (l'autotest embarqué doit rendre
    « 28 PASS / 0 ÉCHEC » compté DEPUIS LE FLUX), refus nommés, rapport
    complet, et AUCUNE voie réseau dans le source. True ssi tout passe."""
    import secrets
    passes, echecs = [], []

    def controle(nom, ok, detail=""):
        (passes if ok else echecs).append(nom)
        print(f"  {'PASS' if ok else 'ÉCHEC'} {nom}"
              + (f" — {detail}" if detail and not ok else ""))

    # D122 : la boîte noire écrit et restitue (le rapport aura du fond)
    marque = "selftest-boite-noire-" + secrets.token_hex(8)
    ENREGISTREUR.ligne(marque, "selftest")
    try:
        with open(CHEMIN_JOURNAL_VOL, "r", encoding="utf-8") as f:
            retrouve = marque in f.read()
    except OSError:
        retrouve = False
    controle("boite-noire-ecrit-et-restitue", retrouve)

    # la pile pip : trois états NOMMÉS (version ou ABSENT, jamais un crash)
    pile = pile_pip()
    controle("pile-pip-trois-etats-nommes",
             len(pile) == 3 and all(isinstance(v, str) or v is None
                                    for _, v in pile))
    texte = texte_pile()
    controle("pile-pip-texte-nomme-les-absents",
             ("ABSENT" in texte) == (not pile_complete())
             and ("COMPLÈTE" in texte) == pile_complete())

    # les empreintes : coffre_cf3 présent (le pupitre vit auprès de lui),
    # empreinte = md5 réel ; un fichier absent est NOMMÉ (None)
    controle("empreinte-coffre-cf3-presente",
             _md5_si_present("coffre_cf3.py") is not None)
    with open(chemin_cible("coffre_cf3.py"), "rb") as f:
        md5_reel = hashlib.md5(f.read()).hexdigest()
    controle("empreinte-coffre-cf3-exacte",
             _md5_si_present("coffre_cf3.py") == md5_reel)

    # la posture est DITE avant le fait, DANS LES DEUX sens : en dossier
    # v06/ (dépôt complet ou kit du Drive), la suite complète doit être
    # DISPONIBLE ; en copie plate, elle doit être REFUSÉE (le refus nommé
    # du bouton n'arrive qu'à un état réel) — la suite externe prouve les
    # deux postures par sous-processus
    if os.path.isfile(os.path.join(CHEMIN_V06, "__init__.py")):
        controle("posture-dossier-v06-suite-disponible",
                 suite_disponible())
    else:
        controle("posture-copie-plate-suite-refusee",
                 not suite_disponible())

    # le relais SOUS-PROCESSUS réel : l'autotest embarqué (avec SON
    # argument de sous-commande — le pupitre est un lanceur, pas un
    # réimplémenteur), compté DU FLUX
    relais = RelaisEssais()
    lignes = relais.lancer(chemin_cible("coffre_cf3.py"), ["autotest"])
    comptes = compter_verdict(lignes)
    controle("relais-autotest-code-0", relais.code == 0,
             f"code={relais.code}")
    controle("relais-autotest-28-pass-compte-du-flux",
             comptes == (28, 0), f"comptes={comptes}")

    # refus NOMMÉ : cible absente (jamais un repli silencieux)
    relais_fantome = RelaisEssais()
    lignes_fantome = relais_fantome.lancer(
        os.path.join(CHEMIN_V06, "module-fantome.py"))
    controle("relais-cible-absente-refus-nomme",
             lignes_fantome == [] and relais_fantome.code is None
             and "introuvable" in str(relais_fantome.erreur))

    # le compteur de verdict : compte la DERNIÈRE ligne de verdict,
    # tolère ÉCHEC et ECHEC, rend None sans verdict
    controle("compteur-dernier-verdict-gagne",
             compter_verdict(["[x] 1 PASS / 0 ÉCHEC",
                              "[x] 5 PASS / 2 ÉCHEC"]) == (5, 2))
    controle("compteur-tolerer-accent-facon-windows",
             compter_verdict(["[x] 3 PASS / 1 ECHEC"]) == (3, 1))
    controle("compteur-sans-verdict-rend-none",
             compter_verdict(["rien ici", "ni là"]) is None)

    # le rapport : LA fonction réelle (niveau module, sans fenêtre) doit
    # emporter l'entête, l'environnement, l'empreinte de coffre_cf3, le
    # journal d'écran témoin ET la boîte noire (la marque y vit déjà)
    temoin_ecran = "ligne-ecran-temoin-" + secrets.token_hex(8)
    rapport = constituer_rapport_complet(temoin_ecran)
    controle("rapport-entete-et-version",
             "RAPPORT D'AUTOTEST CF3" in rapport
             and VERSION_PUPITRE in rapport)
    controle("rapport-trois-sections",
             "JOURNAL D'ÉCRAN" in rapport
             and "JOURNAL DE VOL" in rapport
             and "empreintes md5" in rapport)
    controle("rapport-empreinte-coffre-cf3-emportee",
             md5_reel in rapport)
    controle("rapport-temoin-ecran-emporte", temoin_ecran in rapport)
    controle("rapport-boite-noire-emportee", marque in rapport)

    # AUCUNE voie réseau dans le source : audit AST des IMPORTS réels
    # (un contrôle par chaîne se dénoncerait LUI-MÊME — la preuve doit
    # regarder les imports, pas le texte ; falsifiable par le premier
    # « import socket » ajouté au fichier)
    import ast
    modules_interdits = {"socket", "urllib", "urllib.request",
                         "urllib.parse", "urllib.error", "requests",
                         "http", "http.client", "ftplib", "smtplib",
                         "telnetlib", "asyncio", "ssl"}
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        arbre = ast.parse(f.read())
    imports_trouves = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            imports_trouves.update(alias.name.split(".")[0]
                                   for alias in noeud.names)
        elif isinstance(noeud, ast.ImportFrom):
            if noeud.module:
                imports_trouves.add(noeud.module.split(".")[0])
    controle("source-sans-import-reseau",
             not (imports_trouves & modules_interdits),
             f"imports réseau : {sorted(imports_trouves & modules_interdits)}")

    print(f"[autotest-CF3-GUI] selftest : "
          f"{len(passes)} PASS / {len(echecs)} ÉCHEC")
    return not echecs


def main():
    parseur = argparse.ArgumentParser(
        description="TRIADE — pupitre d'autotest CF3 (D124, v1.2). Sans "
                    "argument : fenêtre (essais relais + rapport). --selftest : "
                    "batterie headless (aucune GUI requise). --v06 CHEMIN : "
                    "dossier qui porte coffre_cf3.py (défaut : à côté du "
                    "pupitre).")
    parseur.add_argument("--selftest", action="store_true",
                         help="batterie embarquée (aucune GUI requise)")
    parseur.add_argument("--v06", metavar="CHEMIN", default=None,
                         help="dossier v06 à utiliser (dépôt complet ou kit "
                              "du Drive) ; un chemin inexistant est un "
                              "échec nommé (code 2)")
    arguments = parseur.parse_args()
    if arguments.v06:
        try:
            global CHEMIN_V06
            CHEMIN_V06 = _resoudre_v06(arguments.v06)
        except SystemExit as exc:
            print(str(exc), file=sys.stderr)
            return 2
        ENREGISTREUR.ligne(f"dossier v06 imposé : {CHEMIN_V06}", "entete")
    if arguments.selftest:
        ok = selftest()
        return 0 if ok else 1
    return demarrer_gui()


if __name__ == "__main__":
    sys.exit(main())
