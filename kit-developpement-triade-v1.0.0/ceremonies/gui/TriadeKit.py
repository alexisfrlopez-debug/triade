#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
 TRIADE KIT v1.0 - Kit de developpement complet Git / Google Drive / Zenodo
================================================================================
 GUI 1-clic autonome pour les ceremonies de la triade :

   initialisation  - nouveau projet : git init, dossier Drive, depot Zenodo
   verification    - controle des trois piliers (jetons, depots, reseau)
   rotation        - renouvellement des jetons (dossier Drive public ou local)
   synchronisation - Git commit + push, archive du projet sur Drive
   passage public  - Git public, Drive partage, publication Zenodo (DOI)
   cycle complet   - tout l'enchainement en un seul clic

 Aucune dependance externe : Python 3.8+ standard uniquement.
 Les jetons restent en local dans config/triade.json ; ils ne sont envoyes
 qu'aux API officielles (GitHub, Google, Zenodo) et jamais journalises.

 Lancement :
   Windows : double-clic sur LANCEUR-WINDOWS.bat
   macOS   : double-clic sur LANCEUR-MAC.command
   Linux   : ./LANCEUR-LINUX.sh
   Manuel  : python3 TriadeKit.py            (interface graphique)
             python3 TriadeKit.py --demo     (demonstration, sans jeton)
             python3 TriadeKit.py --cli cycle-complet
             python3 TriadeKit.py --selftest
================================================================================
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
import zipfile
from datetime import datetime
from pathlib import Path
from queue import Empty, Queue

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext, ttk
    TK_DISPONIBLE = True
except Exception:
    TK_DISPONIBLE = False

VERSION = "1.0.0"
RACINE = Path(__file__).resolve().parent
DOSSIER_CONFIG = RACINE / "config"
FICHIER_CONFIG = DOSSIER_CONFIG / "triade.json"
DOSSIER_JOURNAL = RACINE / "journal"
DOSSIER_ARCHIVES = RACINE / "archives"
DOSSIER_JETONS_IMPORTES = RACINE / "jetons-importes"


# =============================================================================
# HTTP - client minimal, stdlib uniquement
# =============================================================================

class ReponseHTTP:
    """Reponse simple : code HTTP + corps texte (+ decodage JSON tolerant)."""

    def __init__(self, statut, texte):
        self.statut = statut
        self.texte = texte

    def json(self):
        try:
            return json.loads(self.texte)
        except ValueError:
            return {}


class HTTP:
    TIMEOUT = 30

    @classmethod
    def requete(cls, methode, url, jeton=None, corps=None, entetes=None,
                params=None, timeout=None):
        """Effectue une requete HTTP. corps : dict (JSON) ou bytes (binaire).
        Retourne toujours une ReponseHTTP (statut 0 = echec reseau)."""
        timeout = timeout or cls.TIMEOUT
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        tete = dict(entetes or {})
        tete.setdefault("User-Agent", "TriadeKit/" + VERSION)
        tete.setdefault("Accept", "application/json")
        if jeton:
            tete["Authorization"] = "Bearer " + jeton
        donnees = None
        if corps is not None:
            if isinstance(corps, (bytes, bytearray)):
                donnees = bytes(corps)
                tete.setdefault("Content-Type", "application/octet-stream")
            else:
                donnees = json.dumps(corps).encode("utf-8")
                tete.setdefault("Content-Type", "application/json")
        requete = urllib.request.Request(url, data=donnees,
                                         method=methode.upper(), headers=tete)
        try:
            with urllib.request.urlopen(requete, timeout=timeout) as r:
                return ReponseHTTP(r.status, r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            return ReponseHTTP(e.code, e.read().decode("utf-8", "replace"))
        except Exception as e:
            return ReponseHTTP(0, "%s: %s" % (type(e).__name__, e))


# =============================================================================
# Configuration
# =============================================================================

CONFIG_DEFAUT = {
    "projet": {"nom": "projet-triade", "dossier_local": ""},
    "git": {"depot": "", "jeton": "", "branche": "main"},
    "drive": {
        "jeton_acces": "", "jeton_actualisation": "",
        "client_id": "", "client_secret": "",
        "dossier_projet": "",
        "dossier_jetons": "",
    },
    "zenodo": {
        "jeton": "", "depot_id": "", "environnement": "sandbox",
        "metadata": {"titre": "", "auteur": "", "description": "",
                     "licence": "CC-BY-4.0"},
    },
    "preferences": {"simulation": False, "confirmation_public": True},
}


def fusion(base, perso):
    sortie = dict(base)
    for cle, valeur in perso.items():
        if isinstance(valeur, dict) and isinstance(sortie.get(cle), dict):
            sortie[cle] = fusion(sortie[cle], valeur)
        else:
            sortie[cle] = valeur
    return sortie


class Config:

    @staticmethod
    def charger(creer=True):
        if not FICHIER_CONFIG.exists():
            if creer:
                DOSSIER_CONFIG.mkdir(parents=True, exist_ok=True)
                FICHIER_CONFIG.write_text(
                    json.dumps(CONFIG_DEFAUT, indent=2, ensure_ascii=False),
                    encoding="utf-8")
            return json.loads(json.dumps(CONFIG_DEFAUT))
        try:
            donnees = json.loads(FICHIER_CONFIG.read_text(encoding="utf-8"))
        except ValueError:
            donnees = {}
        return fusion(CONFIG_DEFAUT, donnees)

    @staticmethod
    def sauvegarder(cfg):
        DOSSIER_CONFIG.mkdir(parents=True, exist_ok=True)
        temporaire = FICHIER_CONFIG.with_suffix(".tmp")
        temporaire.write_text(
            json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
        temporaire.replace(FICHIER_CONFIG)

    @staticmethod
    def sauvegarde_securite():
        """Archive la configuration courante avant une rotation."""
        if not FICHIER_CONFIG.exists():
            return None
        horodatage = datetime.now().strftime("%Y%m%d-%H%M%S")
        destination = DOSSIER_CONFIG / ("triade.avant-rotation-%s.json"
                                        % horodatage)
        destination.write_text(FICHIER_CONFIG.read_text(encoding="utf-8"),
                               encoding="utf-8")
        return destination


def masquer(jeton):
    if not jeton:
        return "(vide)"
    if len(jeton) > 10:
        return jeton[:4] + "..." + jeton[-2:]
    return "****"


def obtenir(cfg, chemin, defaut=""):
    d = cfg
    for part in chemin[:-1]:
        d = d.setdefault(part, {})
    return d.get(chemin[-1], defaut)


def definir(cfg, chemin, valeur):
    d = cfg
    for part in chemin[:-1]:
        d = d.setdefault(part, {})
    d[chemin[-1]] = valeur


def slug(texte):
    s = re.sub(r"[^a-z0-9]+", "-", (texte or "projet").lower()).strip("-")
    return s or "projet"


# =============================================================================
# Journal de ceremonie
# =============================================================================

class Journal:
    """Journal horodate : affiche les lignes (GUI ou console), les ecrit dans
    journal/, et trace chaque ceremonie dans journal/historique.jsonl."""

    def __init__(self, nom_ceremonie, sortie=None, avancement=None):
        DOSSIER_JOURNAL.mkdir(parents=True, exist_ok=True)
        horodatage = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        self.nom = nom_ceremonie
        self.fichier = DOSSIER_JOURNAL / ("%s-%s.log"
                                          % (horodatage, slug(nom_ceremonie)))
        self.sortie = sortie or (lambda niveau, message:
                                 print("%s [%s] %s" % (
                                     datetime.now().strftime("%H:%M:%S"),
                                     niveau.strip(), message)))
        self.avancement_cb = avancement
        self._debut = time.time()
        self._ouvert = False

    def ecrire(self, niveau, message):
        horodatage = datetime.now().strftime("%H:%M:%S")
        if not self._ouvert:
            self._ouvert = True
            try:
                with self.fichier.open("a", encoding="utf-8") as f:
                    f.write("TRIADE KIT %s - ceremonie : %s - %s\n"
                            % (VERSION, self.nom,
                               datetime.now().isoformat(timespec="seconds")))
            except OSError:
                pass
        ligne = "%s  %-6s %s" % (horodatage, niveau, message)
        try:
            with self.fichier.open("a", encoding="utf-8") as f:
                f.write(ligne + "\n")
        except OSError:
            pass
        self.sortie(niveau, message)

    def info(self, m):
        self.ecrire("INFO", m)

    def ok(self, m):
        self.ecrire(" OK ", m)

    def erreur(self, m):
        self.ecrire("ERREUR", m)

    def titre(self, m):
        self.ecrire("=====", m)

    def etape(self, m):
        self.ecrire("ETAPE", m)

    def avancement(self, i, n):
        if self.avancement_cb:
            self.avancement_cb(i, n)

    def clore(self, identifiant, succes):
        duree = time.time() - self._debut
        self.ecrire("FIN", "ceremonie '%s' terminee en %.1f s - %s"
                    % (identifiant, duree, "SUCCES" if succes else "ECHEC"))
        entree = {"date": datetime.now().isoformat(timespec="seconds"),
                  "ceremonie": identifiant, "succes": succes,
                  "duree_s": round(duree, 1)}
        try:
            with (DOSSIER_JOURNAL / "historique.jsonl").open("a",
                                                             encoding="utf-8") as f:
                f.write(json.dumps(entree, ensure_ascii=False) + "\n")
        except OSError:
            pass


# =============================================================================
# Piliers : un par plateforme
# =============================================================================

class ErreurPilier(Exception):
    pass


class Pilier:
    nom = "?"
    cle = "?"

    def __init__(self, cfg_globale, journal):
        self.global_cfg = cfg_globale
        self.cfg = cfg_globale[self.cle]
        self.j = journal

    def verifier(self):
        """Retourne (etat, detail) ; etat in ok / partiel / invalide /
        absent / erreur."""
        raise NotImplementedError

    def valider_jeton(self, jeton):
        raise NotImplementedError


class PilierGit(Pilier):
    nom = "Git"
    cle = "git"

    def analyser_depot(self):
        depot = (self.cfg.get("depot") or "").strip()
        m = re.match(
            r"^(?:https?://)?(?:www\.)?github\.com/([^/\s]+)/([^/\s]+?)"
            r"(?:\.git)?/?$", depot)
        return (m.group(1), m.group(2)) if m else None

    def _dossier(self):
        return Path(self.global_cfg["projet"].get("dossier_local")
                    or str(RACINE))

    def _git(self, dossier, *arguments):
        r = subprocess.run(["git", "-C", str(dossier)] + list(arguments),
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=300)
        if r.returncode != 0:
            raise ErreurPilier("git %s : %s" % (
                " ".join(arguments), (r.stderr or r.stdout).strip()[:250]))
        return (r.stdout or "").strip()

    def verifier(self):
        jeton = (self.cfg.get("jeton") or "").strip()
        if not jeton:
            return ("absent", "aucun jeton configure")
        r = HTTP.requete("GET", "https://api.github.com/user", jeton=jeton)
        if r.statut == 200:
            login = r.json().get("login", "?")
            depot = self.analyser_depot()
            if not depot:
                return ("ok", "jeton valide (compte %s), depot non configure"
                        % login)
            o, rp = depot
            r2 = HTTP.requete("GET", "https://api.github.com/repos/%s/%s"
                              % (o, rp), jeton=jeton)
            if r2.statut == 200:
                return ("ok", "jeton valide (%s), depot %s/%s (%s)"
                        % (login, o, rp,
                           "prive" if r2.json().get("private") else "public"))
            if r2.statut == 404:
                return ("partiel", "jeton valide mais depot %s/%s introuvable"
                        % (o, rp))
            return ("partiel", "jeton valide, depot injoignable (HTTP %s)"
                    % r2.statut)
        if r.statut in (401, 403):
            return ("invalide", "jeton refuse par GitHub (HTTP %s)"
                    % r.statut)
        return ("erreur", "GitHub injoignable : %s" % r.texte[:120])

    def valider_jeton(self, jeton):
        return HTTP.requete("GET", "https://api.github.com/user",
                            jeton=jeton).statut == 200

    def _assurer_identite(self, dossier):
        try:
            self._git(dossier, "config", "user.name")
        except ErreurPilier:
            self._git(dossier, "config", "user.name", "Triade Kit")
            self._git(dossier, "config", "user.email", "triade-kit@localhost")

    def initialiser(self, dry=False):
        if not shutil.which("git"):
            raise ErreurPilier("git n'est pas installe (https://git-scm.com)")
        depot = self.analyser_depot()
        if not depot:
            raise ErreurPilier(
                "renseignez l'URL du depot GitHub dans la configuration")
        o, rp = depot
        branche = self.cfg.get("branche") or "main"
        dossier = self._dossier()
        if dry:
            self.j.ok("Git (simulation) : init, .gitignore, premier commit "
                      "et push vers %s/%s" % (o, rp))
            return
        dossier.mkdir(parents=True, exist_ok=True)
        if not (dossier / ".git").exists():
            try:
                self._git(dossier, "init", "-b", branche)
            except ErreurPilier:
                self._git(dossier, "init")
        gi = dossier / ".gitignore"
        if not gi.exists():
            gi.write_text("journal/\narchives/\njetons-importes/\nconfig/\n"
                          "__pycache__/\n", encoding="utf-8")
        md = dossier / "README.md"
        if not md.exists():
            md.write_text("# %s\n\nProjet gere avec le Triade Kit "
                          "(Git / Drive / Zenodo).\n"
                          % self.global_cfg["projet"].get("nom"),
                          encoding="utf-8")
        self._assurer_identite(dossier)
        self._git(dossier, "add", "-A")
        if self._git(dossier, "status", "--porcelain"):
            self._git(dossier, "commit", "-m", "Initialisation Triade Kit")
        else:
            self.j.info("Git : rien a valider")
        distant = self._git(dossier, "remote")
        url_propre = "https://github.com/%s/%s.git" % (o, rp)
        if "origin" in distant.split():
            self._git(dossier, "remote", "set-url", "origin", url_propre)
        else:
            self._git(dossier, "remote", "add", "origin", url_propre)
        jeton = (self.cfg.get("jeton") or "").strip()
        if jeton:
            self._git(dossier, "push",
                      "https://oauth2:%s@github.com/%s/%s.git"
                      % (jeton, o, rp), branche)
        else:
            self._git(dossier, "push", "-u", "origin", branche)
        self.j.ok("Git : depot local initialise et pousse vers %s/%s"
                  % (o, rp))

    def synchroniser(self, dry=False):
        if not shutil.which("git"):
            raise ErreurPilier("git n'est pas installe (https://git-scm.com)")
        depot = self.analyser_depot()
        if not depot:
            raise ErreurPilier("depot Git non configure ou non GitHub "
                               "(voir Configuration)")
        o, rp = depot
        branche = self.cfg.get("branche") or "main"
        dossier = self._dossier()
        if not (dossier / ".git").exists():
            raise ErreurPilier(
                "aucun depot git local dans %s - lancez d'abord la ceremonie "
                "Initialisation" % dossier)
        if dry:
            self.j.ok("Git (simulation) : add -A, commit si necessaire, "
                      "push vers %s/%s (branche %s)" % (o, rp, branche))
            return
        self._assurer_identite(dossier)
        self._git(dossier, "add", "-A")
        if self._git(dossier, "status", "--porcelain"):
            self._git(dossier, "commit", "-m",
                      "Synchronisation Triade Kit - %s"
                      % datetime.now().strftime("%Y-%m-%d %H:%M"))
        else:
            self.j.info("Git : rien a valider (arbre de travail propre)")
        jeton = (self.cfg.get("jeton") or "").strip()
        if jeton:
            self._git(dossier, "push",
                      "https://oauth2:%s@github.com/%s/%s.git"
                      % (jeton, o, rp), branche)
        else:
            self._git(dossier, "push", "origin", branche)
        self.j.ok("Git : pousse vers %s/%s (branche %s)" % (o, rp, branche))

    def rendre_public(self, dry=False):
        depot = self.analyser_depot()
        if not depot:
            raise ErreurPilier("depot Git non configure")
        o, rp = depot
        if dry:
            self.j.ok("Git (simulation) : le depot %s/%s serait rendu public"
                      % (o, rp))
            return
        jeton = (self.cfg.get("jeton") or "").strip()
        r = HTTP.requete("GET", "https://api.github.com/repos/%s/%s"
                         % (o, rp), jeton=jeton)
        if r.statut == 200 and not r.json().get("private"):
            self.j.info("Git : le depot est deja public")
            return
        r = HTTP.requete("PATCH", "https://api.github.com/repos/%s/%s"
                         % (o, rp), jeton=jeton, corps={"private": False})
        if r.statut == 200:
            self.j.ok("Git : depot %s/%s rendu public" % (o, rp))
            return
        raise ErreurPilier("impossible de rendre le depot public (HTTP %s) "
                           ": %s" % (r.statut, r.texte[:200]))


class PilierDrive(Pilier):
    nom = "Drive"
    cle = "drive"
    URL_API = "https://www.googleapis.com/drive/v3"

    def acces(self):
        return (self.cfg.get("jeton_acces") or "").strip()

    def actualiser_jeton(self):
        """Echange le jeton d'actualisation contre un jeton d'acces neuf."""
        donnees = {
            "client_id": (self.cfg.get("client_id") or "").strip(),
            "client_secret": (self.cfg.get("client_secret") or "").strip(),
            "refresh_token":
                (self.cfg.get("jeton_actualisation") or "").strip(),
            "grant_type": "refresh_token",
        }
        if not all(donnees.values()):
            return False
        r = HTTP.requete("POST", "https://oauth2.googleapis.com/token",
                         corps=donnees)
        if r.statut == 200 and r.json().get("access_token"):
            self.cfg["jeton_acces"] = r.json()["access_token"]
            Config.sauvegarder(self.global_cfg)
            self.j.ok("Drive : jeton d'acces actualise automatiquement")
            return True
        return False

    def verifier(self):
        if not self.acces() and not self.actualiser_jeton():
            return ("absent", "aucun jeton d'acces configure")
        r = HTTP.requete("GET", self.URL_API + "/about", jeton=self.acces(),
                         params={"fields": "user"})
        if r.statut == 200:
            u = r.json().get("user", {}).get("emailAddress", "?")
            return ("ok", "jeton valide (%s)" % u)
        if r.statut in (401, 403) and self.actualiser_jeton():
            r = HTTP.requete("GET", self.URL_API + "/about",
                             jeton=self.acces(), params={"fields": "user"})
            if r.statut == 200:
                return ("ok", "jeton rafraichi puis valide")
        if r.statut in (401, 403):
            return ("invalide", "jeton refuse par Google (HTTP %s)"
                    % r.statut)
        return ("erreur", "Google injoignable : %s" % r.texte[:120])

    def valider_jeton(self, jeton):
        return HTTP.requete("GET", self.URL_API + "/about", jeton=jeton,
                            params={"fields": "user"}).statut == 200

    def creer_dossier(self, nom, dry=False):
        if dry:
            self.j.ok("Drive (simulation) : le dossier '%s' serait cree"
                      % nom)
            return None
        r = HTTP.requete("POST", self.URL_API + "/files", jeton=self.acces(),
                         corps={"name": nom,
                                "mimeType":
                                    "application/vnd.google-apps.folder"},
                         params={"supportsAllDrives": "true"})
        if r.statut not in (200, 201):
            raise ErreurPilier("creation du dossier Drive impossible "
                               "(HTTP %s) : %s" % (r.statut, r.texte[:200]))
        identifiant = r.json().get("id")
        self.j.ok("Drive : dossier '%s' cree (%s)" % (nom, identifiant))
        return identifiant

    def televerser(self, chemin, dossier_id, dry=False):
        chemin = Path(chemin)
        if dry:
            self.j.ok("Drive (simulation) : %s serait televerse dans %s"
                      % (chemin.name, dossier_id or "(dossier par defaut)"))
            return None
        frontiere = "triadeKitFrontiere123456"
        metadonnees = json.dumps({"name": chemin.name,
                                  "parents": [dossier_id]})
        entete = ("--%s\r\nContent-Type: application/json; charset=UTF-8"
                  "\r\n\r\n%s\r\n--%s\r\nContent-Type: "
                  "application/octet-stream\r\n\r\n"
                  % (frontiere, metadonnees, frontiere)).encode("utf-8")
        corps = (entete + chemin.read_bytes()
                 + ("\r\n--%s--" % frontiere).encode("utf-8"))
        r = HTTP.requete("POST",
                         "https://www.googleapis.com/upload/drive/v3/files",
                         jeton=self.acces(), corps=corps,
                         entetes={"Content-Type":
                                  "multipart/related; boundary=%s"
                                  % frontiere},
                         params={"uploadType": "multipart",
                                 "supportsAllDrives": "true"})
        if r.statut in (200, 201):
            identifiant = r.json().get("id")
            self.j.ok("Drive : %s televerse (%s)"
                      % (chemin.name, identifiant))
            return identifiant
        raise ErreurPilier("televersement Drive impossible (HTTP %s) : %s"
                           % (r.statut, r.texte[:200]))

    def partager(self, fichier_id, dry=False):
        if dry:
            self.j.ok("Drive (simulation) : %s serait partage en lecture "
                      "publique" % fichier_id)
            return
        r = HTTP.requete("POST", "%s/files/%s/permissions"
                         % (self.URL_API, fichier_id), jeton=self.acces(),
                         corps={"role": "reader", "type": "anyone"},
                         params={"supportsAllDrives": "true"})
        if r.statut in (200, 201):
            self.j.ok("Drive : partage en lecture publique accorde")
            return
        raise ErreurPilier("partage Drive impossible (HTTP %s) : %s"
                           % (r.statut, r.texte[:200]))

    def recuperer_dossier_public(self, dossier_id):
        """Recupere les petits fichiers texte d'un dossier Drive public,
        sans jeton (best effort)."""
        r = HTTP.requete("GET",
                         "https://drive.google.com/drive/folders/%s"
                         % dossier_id, timeout=20)
        if r.statut != 200:
            raise ErreurPilier("dossier Drive injoignable (HTTP %s) - est-il "
                               "partage en 'toute personne disposant du "
                               "lien' ?" % r.statut)
        # identifiants des fichiers du dossier
        ids = [i for i in dict.fromkeys(re.findall(
            r'data-id="([A-Za-z0-9_-]{20,})"', r.texte))
            if i != dossier_id]
        if not ids:
            raise ErreurPilier("aucun fichier detecte dans la page du "
                               "dossier (dossier prive ou page de connexion)")
        # noms : chaque ligne du dossier porte un data-id suivi d'un
        # aria-label commencant par le nom du fichier
        noms = {}
        segments = re.split(r'data-id="([A-Za-z0-9_-]{20,})"', r.texte)
        for k in range(1, len(segments) - 1, 2):
            identifiant = segments[k]
            if identifiant == dossier_id or identifiant in noms:
                continue
            m = re.search(r'aria-label="([^"]{1,150})"',
                          segments[k + 1][:3000])
            if m:
                premier = (m.group(1).replace("&amp;", "&")
                           .replace("&#39;", "'").split(" ")[0])
                if "." in premier and not premier.startswith("."):
                    noms[identifiant] = premier
        entrees = [(i, noms.get(i, "fichier-%s.txt" % i[:8])) for i in ids]
        sorties = []
        for identifiant, nom in entrees[:20]:
            ru = HTTP.requete(
                "GET", "https://drive.usercontent.google.com/download",
                params={"id": identifiant, "export": "download"}, timeout=30)
            if ru.statut != 200:
                continue
            texte = ru.texte
            if "Virus scan warning" in texte[:4000]:
                m1 = re.search(r'name="confirm"\s+value="([^"]+)"', texte)
                m2 = re.search(r'name="uuid"\s+value="([^"]+)"', texte)
                parametres = {"id": identifiant, "export": "download"}
                if m1:
                    parametres["confirm"] = m1.group(1)
                if m2:
                    parametres["uuid"] = m2.group(1)
                ru = HTTP.requete(
                    "GET", "https://drive.usercontent.google.com/download",
                    params=parametres, timeout=30)
                if ru.statut != 200:
                    continue
                texte = ru.texte
            if (len(texte) > 100000
                    or "<html" in texte[:300].lower()):
                continue
            sorties.append((nom, texte.strip()))
        if not sorties:
            raise ErreurPilier("fichiers presents mais non recuperables "
                               "automatiquement - telechargez-les puis "
                               "utilisez 'Rotation : importer un dossier'")
        return sorties


class PilierZenodo(Pilier):
    nom = "Zenodo"
    cle = "zenodo"
    BASES = {"sandbox": "https://sandbox.zenodo.org/api",
             "production": "https://zenodo.org/api"}

    @property
    def base(self):
        return self.BASES.get(self.cfg.get("environnement"),
                              self.BASES["sandbox"])

    def _jeton(self):
        return (self.cfg.get("jeton") or "").strip()

    def _tester(self, base, jeton=None):
        candidat = jeton if jeton is not None else self._jeton()
        return HTTP.requete("GET", base + "/deposit/depositions",
                            params={"access_token": candidat, "size": 1},
                            timeout=20).statut == 200

    def _basculer(self, autre, jeton=None):
        """Valide le jeton sur l'environnement 'autre' et, si accepté,
        retient cet environnement dans la configuration."""
        if self._tester(self.BASES[autre], jeton):
            self.cfg["environnement"] = autre
            Config.sauvegarder(self.global_cfg)
            self.j.info("Zenodo : environnement bascule sur '%s' (le jeton "
                        "y est valide)" % autre)
            return True
        return False

    def _autre_environnement(self):
        return ("production"
                if self.cfg.get("environnement") == "sandbox"
                else "sandbox")

    def verifier(self):
        if not self._jeton():
            return ("absent", "aucun jeton configure")
        if self._tester(self.base):
            return ("ok", "jeton valide (environnement %s)"
                    % self.cfg.get("environnement"))
        if self._basculer(self._autre_environnement()):
            return ("ok", "jeton valide (environnement %s)"
                    % self.cfg.get("environnement"))
        return ("invalide", "jeton refuse par Zenodo (sandbox et "
                "production)")

    def valider_jeton(self, jeton):
        if self._tester(self.base, jeton):
            return True
        return self._basculer(self._autre_environnement(), jeton)

    def _corps_metadata(self):
        m = self.cfg.get("metadata", {})
        return {"metadata": {
            "title": (m.get("titre")
                      or self.global_cfg["projet"].get("nom")
                      or "Depot Triade Kit"),
            "upload_type": "software",
            "creators": [{"name": m.get("auteur") or "Anonyme"}],
            "description": (m.get("description")
                            or "Depot cree par le Triade Kit."),
            "license": m.get("licence") or "CC-BY-4.0",
        }}

    def creer_depot(self, dry=False):
        if dry:
            self.j.ok("Zenodo (simulation) : creation d'un depot brouillon "
                      "simulee")
            return None
        r = HTTP.requete("POST", self.base + "/deposit/depositions",
                         jeton=self._jeton(),
                         corps=self._corps_metadata())
        if r.statut != 201:
            raise ErreurPilier("creation du depot Zenodo impossible "
                               "(HTTP %s) : %s" % (r.statut, r.texte[:200]))
        identifiant = str(r.json().get("id"))
        self.cfg["depot_id"] = identifiant
        Config.sauvegarder(self.global_cfg)
        self.j.ok("Zenodo : depot brouillon n°%s cree (%s)"
                  % (identifiant, self.cfg.get("environnement")))
        return identifiant

    def preparer_version(self, dry=False):
        """Retourne (id_brouillon, url_bucket) : depot neuf ou nouvelle
        version du depot existant."""
        if dry:
            self.j.ok("Zenodo (simulation) : nouvelle version du depot "
                      "preparee (simulee)")
            return "0000", "https://simulation/bucket"
        identifiant = (self.cfg.get("depot_id") or "").strip()
        if not identifiant:
            r = HTTP.requete("POST", self.base + "/deposit/depositions",
                             jeton=self._jeton(),
                             corps=self._corps_metadata())
            if r.statut != 201:
                raise ErreurPilier("creation du depot Zenodo impossible "
                                   "(HTTP %s) : %s"
                                   % (r.statut, r.texte[:200]))
            donnees = r.json()
            self.cfg["depot_id"] = str(donnees.get("id"))
            Config.sauvegarder(self.global_cfg)
            bucket = donnees.get("links", {}).get("bucket")
            self.j.ok("Zenodo : nouveau depot n°%s cree"
                      % donnees.get("id"))
        else:
            r = HTTP.requete(
                "POST", "%s/deposit/depositions/%s/actions/newversion"
                % (self.base, identifiant), jeton=self._jeton())
            if r.statut != 201:
                raise ErreurPilier("nouvelle version Zenodo impossible "
                                   "(HTTP %s) : %s"
                                   % (r.statut, r.texte[:200]))
            url_brouillon = r.json().get("links", {}).get("latest_draft", "")
            if not url_brouillon:
                raise ErreurPilier("Zenodo n'a pas renvoye de brouillon")
            r2 = HTTP.requete("GET", url_brouillon, jeton=self._jeton())
            if r2.statut != 200:
                raise ErreurPilier("lecture du brouillon Zenodo impossible "
                                   "(HTTP %s)" % r2.statut)
            donnees = r2.json()
            bucket = donnees.get("links", {}).get("bucket")
            self.j.ok("Zenodo : brouillon de version n°%s pret"
                      % donnees.get("id"))
        if not bucket:
            raise ErreurPilier("bucket Zenodo introuvable")
        return str(donnees["id"]), bucket

    def televerser(self, bucket, chemin, dry=False):
        chemin = Path(chemin)
        if dry:
            self.j.ok("Zenodo (simulation) : %s serait televerse"
                      % chemin.name)
            return
        r = HTTP.requete("PUT", bucket + "/" + urllib.parse.quote(chemin.name),
                         jeton=self._jeton(), corps=chemin.read_bytes(),
                         params={"access_token": self._jeton()},
                         timeout=120)
        if r.statut not in (200, 201):
            raise ErreurPilier("televersement Zenodo impossible (HTTP %s) "
                               ": %s" % (r.statut, r.texte[:200]))
        self.j.ok("Zenodo : %s televerse" % chemin.name)

    def publier(self, identifiant, dry=False):
        if dry:
            self.j.ok("Zenodo (simulation) : publication simulee - DOI "
                      "10.5281/zenodo.000000")
            return "10.5281/zenodo.000000 (simulation)"
        r = HTTP.requete(
            "POST", "%s/deposit/depositions/%s/actions/publish"
            % (self.base, identifiant), jeton=self._jeton())
        if r.statut != 202:
            raise ErreurPilier("publication Zenodo impossible (HTTP %s) : %s"
                               % (r.statut, r.texte[:200]))
        donnees = r.json()
        doi = donnees.get("doi") or donnees.get("links", {}).get("doi", "")
        self.j.ok("Zenodo : PUBLIE - DOI %s" % doi)
        return doi


# =============================================================================
# Piliers de demonstration (aucun reseau, aucune ecriture)
# =============================================================================

class DemoPilier(Pilier):
    def verifier(self):
        time.sleep(0.25)
        return ("ok", "mode demonstration : pilier operationnel")

    def valider_jeton(self, jeton):
        return True


class DemoPilierGit(DemoPilier):
    nom = "Git"
    cle = "git"

    def initialiser(self, dry=False):
        time.sleep(0.2)
        self.j.ok("Git (demo) : depot local initialise et pousse (simule)")

    def synchroniser(self, dry=False):
        time.sleep(0.3)
        self.j.ok("Git (demo) : add, commit et push simules")

    def rendre_public(self, dry=False):
        time.sleep(0.2)
        self.j.ok("Git (demo) : depot rendu public (simule)")


class DemoPilierDrive(DemoPilier):
    nom = "Drive"
    cle = "drive"

    def creer_dossier(self, nom, dry=False):
        time.sleep(0.2)
        self.j.ok("Drive (demo) : dossier '%s' cree (simule)" % nom)
        return "dossier-demo"

    def televerser(self, chemin, dossier_id, dry=False):
        time.sleep(0.3)
        self.j.ok("Drive (demo) : %s televerse (simule)"
                  % Path(chemin).name)
        return "fichier-demo"

    def partager(self, fichier_id, dry=False):
        time.sleep(0.2)
        self.j.ok("Drive (demo) : partage en lecture publique (simule)")


class DemoPilierZenodo(DemoPilier):
    nom = "Zenodo"
    cle = "zenodo"

    def creer_depot(self, dry=False):
        time.sleep(0.2)
        self.j.ok("Zenodo (demo) : depot brouillon cree (simule)")
        return "12345"

    def preparer_version(self, dry=False):
        time.sleep(0.3)
        self.j.ok("Zenodo (demo) : nouvelle version preparee (simulee)")
        return "12345", "https://demo/bucket"

    def televerser(self, bucket, chemin, dry=False):
        time.sleep(0.3)
        self.j.ok("Zenodo (demo) : %s televerse (simule)"
                  % Path(chemin).name)

    def publier(self, identifiant, dry=False):
        time.sleep(0.3)
        self.j.ok("Zenodo (demo) : publication simulee")
        return "10.5281/zenodo.000000 (demo)"


def construire_piliers(config, journal, demo=False):
    classes = ((DemoPilierGit, DemoPilierDrive, DemoPilierZenodo) if demo
               else (PilierGit, PilierDrive, PilierZenodo))
    return {c.cle: c(config, journal) for c in classes}


# =============================================================================
# Aides aux jetons
# =============================================================================

def extraire_jetons(texte):
    """Extrait les champs de jeton d'un fichier : JSON, lignes 'cle: valeur',
    ou jeton brut seul sur une ligne."""
    sorties = {}
    if not texte:
        return sorties
    t = texte.strip()
    correspondances = {
        "jeton": ("jeton", "token", "access_token", "jeton_acces",
                  "pat", "ghp"),
        "jeton_actualisation": ("jeton_actualisation", "refresh_token"),
        "client_id": ("client_id",),
        "client_secret": ("client_secret",),
    }
    try:
        donnees = json.loads(t)
        if isinstance(donnees, dict):
            candidats = [donnees]
            for valeur in donnees.values():
                if isinstance(valeur, dict):
                    candidats.append(valeur)
            for bloc in candidats:
                for champ, cles in correspondances.items():
                    if champ in sorties:
                        continue
                    for cle in cles:
                        if bloc.get(cle):
                            sorties[champ] = str(bloc[cle]).strip()
                            break
            if sorties:
                return sorties
    except ValueError:
        pass
    for ligne in t.splitlines():
        if ":" in ligne:
            cle, valeur = ligne.split(":", 1)
            cle = (cle.strip().strip('"').strip("'").lower()
                   .replace(" ", "_"))
            valeur = valeur.strip().strip('"').strip("'").rstrip(",")
            if not valeur or len(valeur) > 400:
                continue
            if cle in ("jeton", "token", "access_token", "jeton_acces"):
                sorties["jeton"] = valeur
            elif cle in ("refresh_token", "jeton_actualisation"):
                sorties["jeton_actualisation"] = valeur
            elif cle == "client_id":
                sorties["client_id"] = valeur
            elif cle == "client_secret":
                sorties["client_secret"] = valeur
    if (not sorties and t and len(t) < 4096 and "\n" not in t
            and not t.startswith("{") and not t.startswith("[")):
        sorties["jeton"] = t
    return sorties


def construire_archive(cfg, journal, simulation=False):
    """Cree l'archive zip du projet (jetons, config, journal et .git exclus).
    Retourne (chemin, nombre_de_fichiers)."""
    DOSSIER_ARCHIVES.mkdir(parents=True, exist_ok=True)
    horodatage = datetime.now().strftime("%Y%m%d-%H%M%S")
    nom = "%s-%s.zip" % (slug(cfg["projet"].get("nom", "projet")), horodatage)
    chemin = DOSSIER_ARCHIVES / nom
    source = Path(cfg["projet"].get("dossier_local") or str(RACINE))
    exclus = {"journal", "archives", "jetons-importes", "config", ".git",
              "__pycache__"}
    if simulation:
        journal.info("(simulation) l'archive %s serait creee a partir de %s "
                     "(jetons et configuration exclus)" % (nom, source))
        return chemin, 0
    total = 0
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(source.rglob("*")):
            relatif = f.relative_to(source)
            if any(m in exclus for m in relatif.parts):
                continue
            if f.is_file():
                z.write(f, relatif.as_posix())
                total += 1
    journal.ok("archive %s creee (%d fichiers - jetons et configuration "
               "exclus)" % (chemin.name, total))
    return chemin, total


# =============================================================================
# Ceremonies
# =============================================================================

class Ceremonie:
    nom = "?"
    nom_id = "?"
    description = ""

    def __init__(self, config, journal, demo=False, simulation=False):
        self.cfg = config
        self.j = journal
        self.demo = demo
        self.simulation = simulation
        self.piliers = construire_piliers(config, journal, demo)
        self.rapport = {"ceremonie": self.nom, "succes": False,
                        "etapes": [], "erreurs": [], "liens": {},
                        "debut": datetime.now().isoformat(
                            timespec="seconds")}
        self.total = 1

    def etape(self, i, titre):
        self.j.etape("[%d/%d] %s" % (i, self.total, titre))
        self.j.avancement(i, self.total)
        self.rapport["etapes"].append(titre)

    def _erreur(self, message):
        self.j.erreur(message)
        self.rapport["erreurs"].append(message)

    def finaliser(self, succes):
        self.rapport["succes"] = succes
        self.rapport["fin"] = datetime.now().isoformat(timespec="seconds")
        self.rapport["fichier_journal"] = str(self.j.fichier)
        self.j.clore(self.nom_id, succes)
        chemin = DOSSIER_JOURNAL / ("%s-%s.rapport.json"
                                     % (self.j.fichier.stem, self.nom_id))
        try:
            chemin.write_text(json.dumps(self.rapport, indent=2,
                                         ensure_ascii=False),
                              encoding="utf-8")
        except OSError:
            pass
        return self.rapport

    def executer(self):
        raise NotImplementedError


class VerificationCeremonie(Ceremonie):
    nom = "Verification"
    nom_id = "verification"
    description = "Controle des trois piliers : jetons, depots, reseau."

    def executer(self):
        self.j.titre("Ceremonie de verification - %s"
                     % datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.total = 3
        etats = {}
        for i, cle in enumerate(("git", "drive", "zenodo"), 1):
            pilier = self.piliers[cle]
            self.etape(i, "Pilier %s" % pilier.nom)
            try:
                etat, detail = pilier.verifier()
                etats[cle] = etat
                if etat == "ok":
                    self.j.ok("%s : %s" % (pilier.nom, detail))
                elif etat in ("invalide", "erreur"):
                    self._erreur("%s : %s" % (pilier.nom, detail))
                else:
                    self.j.info("%s : %s" % (pilier.nom, detail))
            except Exception as e:
                etats[cle] = "erreur"
                self._erreur("%s : exception %s" % (pilier.nom, e))
        self.rapport["etats"] = etats
        succes = all(e == "ok" for e in etats.values())
        self.j.titre("Verdict : " + (
            "les trois piliers sont operationnels" if succes
            else "au moins un pilier exige une attention (Rotation "
                 "conseillee)"))
        return self.finaliser(succes)


class RotationCeremonie(Ceremonie):
    nom = "Rotation des jetons"
    nom_id = "rotation"
    description = ("Renouvelle les jetons : dossier Drive public, dossier "
                   "local ou saisie manuelle, avec validation avant "
                   "application.")
    INDICES_NOM = {
        "git": ("git", "github", "ghp", "gh_"),
        "drive": ("drive", "gdrive", "google", "gcloud", "oauth"),
        "zenodo": ("zenodo", "zdt"),
    }
    INDICES_CONTENU = {
        "git": ("github", "ghp_", "github_pat"),
        "drive": ("googleapis", "googleusercontent", "gserviceaccount",
                  "google"),
        "zenodo": ("zenodo",),
    }

    def executer(self, dossier_jetons=None):
        self.j.titre("Ceremonie de rotation des jetons - %s"
                     % datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.total = 5
        # 1. sauvegarde de securite
        self.etape(1, "Sauvegarde de securite de la configuration")
        if self.demo:
            self.j.ok("(demo) configuration fictive archivee")
        else:
            sauvegarde = Config.sauvegarde_securite()
            if sauvegarde:
                self.j.ok("configuration archivee : %s" % sauvegarde)
            else:
                self.j.info("aucune configuration preexistante a archiver")
        # 2. collecte
        self.etape(2, "Collecte des nouveaux jetons")
        fichiers = self.collecter(dossier_jetons)
        if not fichiers:
            self._erreur("aucun jeton trouve - telechargez les fichiers de "
                         "jetons puis utilisez 'Rotation : importer un "
                         "dossier', ou collez-les dans la Configuration")
            return self.finaliser(False)
        # 3. analyse / affectation
        self.etape(3, "Analyse et affectation des jetons")
        affectations = self.affecter(fichiers)
        if not affectations:
            self._erreur("impossible de deviner l'appartenance des fichiers "
                         "- nommez-les jeton-git.txt, jeton-drive.txt, "
                         "jeton-zenodo.txt et relancez")
            return self.finaliser(False)
        for pilier, donnees in sorted(affectations.items()):
            self.j.info("%s <- %s" % (
                pilier, ", ".join("%s=%s" % (c, masquer(v))
                                  for c, v in sorted(donnees.items()))))
        # 4. validation
        self.etape(4, "Validation des jetons aupres des plateformes")
        if self.demo or self.simulation:
            self.j.ok("validation simulee : les jetons sont acceptes "
                      "(demo/simulation)")
        else:
            for pilier, donnees in list(affectations.items()):
                p = self.piliers[pilier]
                if not donnees.get("jeton"):
                    self.j.info("%s : champs auxiliaires seulement (pas de "
                                "jeton principal)" % p.nom)
                    continue
                if p.valider_jeton(donnees["jeton"]):
                    self.j.ok("%s : jeton valide par la plateforme" % p.nom)
                else:
                    self._erreur("%s : jeton refuse - il ne sera PAS applique"
                                 % p.nom)
                    del affectations[pilier]
            if not affectations:
                return self.finaliser(False)
        # 5. application atomique
        self.etape(5, "Application de la nouvelle configuration")
        if self.demo or self.simulation:
            self.j.ok("(demo/simulation) la configuration serait mise a "
                      "jour avec %d jeton(s)" % len(affectations))
        else:
            appliques = []
            for pilier, donnees in affectations.items():
                section = self.cfg[pilier]
                if pilier == "drive":
                    for cle in ("jeton", "jeton_actualisation", "client_id",
                                "client_secret"):
                        if donnees.get(cle):
                            cle_cfg = ("jeton_acces" if cle == "jeton"
                                       else cle)
                            section[cle_cfg] = donnees[cle]
                elif donnees.get("jeton"):
                    section["jeton"] = donnees["jeton"]
                appliques.append(pilier)
            if appliques:
                Config.sauvegarder(self.cfg)
                self.j.ok("configuration mise a jour (%s)"
                          % ", ".join(appliques))
        self.j.titre("Verdict : rotation terminee (%d pilier(s) concerne(s))"
                     % len(affectations))
        return self.finaliser(bool(affectations))

    def collecter(self, dossier=None):
        if self.demo:
            return [("jeton-git.txt", "ghp_demo0000000000"),
                    ("jeton-drive.txt", "ya29.demo"),
                    ("jeton-zenodo.txt", "0123456789abcdef0123456789abcdef")]
        if dossier:
            p = Path(dossier)
            fichiers = []
            for f in sorted(p.rglob("*")):
                if (f.is_file() and f.suffix.lower() in (
                        ".txt", ".json", ".token", ".conf", ".ini", "")
                        and f.stat().st_size < 100000):
                    try:
                        fichiers.append(
                            (f.name,
                             f.read_text(encoding="utf-8",
                                         errors="replace").strip()))
                    except OSError:
                        pass
            self.j.info("%d fichier(s) lu(s) dans %s" % (len(fichiers), p))
            return fichiers
        dossier_drive = (self.cfg["drive"].get("dossier_jetons")
                         or "").strip()
        if dossier_drive:
            self.j.info("tentative de recuperation depuis le dossier Drive "
                        "des jetons (%s)" % dossier_drive)
            try:
                fichiers = self.piliers["drive"].recuperer_dossier_public(
                    dossier_drive)
                self.j.ok("%d fichier(s) recupere(s) depuis Drive"
                          % len(fichiers))
                DOSSIER_JETONS_IMPORTES.mkdir(parents=True, exist_ok=True)
                for nom, contenu in fichiers:
                    chemin = DOSSIER_JETONS_IMPORTES / slug(nom or "jeton")
                    chemin.write_text(contenu, encoding="utf-8")
                return fichiers
            except Exception as e:
                self.j.info("recuperation automatique impossible (%s) - "
                            "import manuel necessaire" % str(e)[:120])
        return []

    def affecter(self, fichiers):
        par_pilier = {}
        for nom, contenu in fichiers:
            pilier = self.deviner(nom, contenu)
            if not pilier:
                continue
            champs = self._nettoyer(extraire_jetons(contenu))
            if not champs:
                continue
            par_pilier.setdefault(pilier, []).append((nom, champs))
        affectations = {p: self._fusionner(l) for p, l in par_pilier.items()}
        # heuristiques : jeton brut non affecte -> Zenodo (hexa 32 ou
        # jeton alphanumerique de 48 a 64 caracteres, format Zenodo actuel)
        if "zenodo" not in affectations:
            for nom, contenu in fichiers:
                if self.deviner(nom, contenu):
                    continue
                champs = self._nettoyer(extraire_jetons(contenu))
                candidat = champs.get("jeton", "")
                if candidat and (re.fullmatch(r"[0-9a-f]{32}", candidat)
                                 or re.fullmatch(r"[0-9A-Za-z]{48,64}",
                                                 candidat)):
                    affectations["zenodo"] = champs
                    self.j.info("heuristique : fichier %s affecte a Zenodo "
                                "(jeton de %d caracteres)"
                                % (nom, len(candidat)))
                    break
        return affectations

    @staticmethod
    def _fusionner(liste):
        """Fusionne les champs extraits de plusieurs fichiers d'un meme
        pilier, avec priorite aux valeurs OAuth (client_id d'application,
        client_secret GOCSPX)."""
        fusion = {}
        for _, champs in liste:
            for cle, valeur in champs.items():
                if cle not in fusion:
                    fusion[cle] = valeur
                elif (cle == "client_id"
                        and valeur.endswith(".apps.googleusercontent.com")
                        and not fusion[cle].endswith(
                            ".apps.googleusercontent.com")):
                    fusion[cle] = valeur
                elif (cle == "client_secret"
                        and valeur.startswith("GOCSPX")
                        and not fusion[cle].startswith("GOCSPX")):
                    fusion[cle] = valeur
        return fusion

    @staticmethod
    def _nettoyer(champs):
        """Elimine les valeurs qui ressemblent a des noms de fichiers ou
        sont trop courtes (manifestes, listes...). Les jetons gcloud
        commencent par '1//' : le separateur '/' n'est donc pas filtre."""
        sorties = {}
        for cle, valeur in champs.items():
            v = (valeur or "").strip()
            if not v or len(v) < 8:
                continue
            if (v.endswith((".txt", ".json", ".md", ".token", ".docx",
                            ".pdf"))
                    or " " in v):
                continue
            sorties[cle] = v
        return sorties

    def deviner(self, nom, contenu):
        n = (nom or "").lower()
        for pilier, indices in self.INDICES_NOM.items():
            if any(i in n for i in indices):
                return pilier
        c = (contenu or "")[:4000].lower()
        for pilier, indices in self.INDICES_CONTENU.items():
            if any(i in c for i in indices):
                return pilier
        return None


class SynchronisationCeremonie(Ceremonie):
    nom = "Synchronisation"
    nom_id = "synchronisation"
    description = ("Git commit + push, puis archive du projet "
                   "televersee sur Google Drive.")

    def executer(self):
        self.j.titre("Ceremonie de synchronisation - %s"
                     % datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.total = 3
        self.etape(1, "Synchronisation Git (commit + push)")
        try:
            self.piliers["git"].synchroniser(
                dry=self.simulation or self.demo)
        except ErreurPilier as e:
            self._erreur("Git : %s" % e)
            return self.finaliser(False)
        self.etape(2, "Construction de l'archive projet")
        try:
            archive, _ = construire_archive(
                self.cfg, self.j, simulation=self.simulation or self.demo)
        except Exception as e:
            self._erreur("archive : %s" % e)
            return self.finaliser(False)
        self.etape(3, "Televersement sur Google Drive")
        dossier_id = (self.cfg["drive"].get("dossier_projet")
                      or "").strip()
        if not dossier_id and not self.demo:
            self.j.info("aucun dossier Drive configure - televersement "
                        "ignore (renseignez-le dans la configuration)")
        else:
            try:
                identifiant = self.piliers["drive"].televerser(
                    archive, dossier_id, dry=self.simulation or self.demo)
                if identifiant:
                    self.rapport["liens"]["drive_fichier"] = str(identifiant)
            except ErreurPilier as e:
                self._erreur("Drive : %s" % e)
                return self.finaliser(False)
        self.j.titre("Verdict : synchronisation terminee")
        return self.finaliser(True)


class PassagePublicCeremonie(Ceremonie):
    nom = "Passage public"
    nom_id = "passage-public"
    description = ("Depot GitHub rendu public, dossier Drive partage en "
                   "lecture, nouvelle version Zenodo publiee (DOI).")

    def executer(self):
        self.j.titre("Ceremonie du passage public - %s"
                     % datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.total = 4
        self.etape(1, "Controle prealable des trois piliers")
        if self.demo or self.simulation:
            self.j.info("(demo/simulation) controle prealable simule : OK")
        else:
            for cle in ("git", "drive", "zenodo"):
                etat, detail = self.piliers[cle].verifier()
                if etat != "ok":
                    self._erreur("%s : %s - executez d'abord la ceremonie "
                                 "Rotation" % (self.piliers[cle].nom, detail))
                    return self.finaliser(False)
                self.j.info("%s : %s" % (self.piliers[cle].nom, detail))
        self.etape(2, "Ouverture publique du depot Git")
        try:
            self.piliers["git"].rendre_public(dry=self.simulation
                                              or self.demo)
            self.rapport["liens"]["github"] = (self.cfg["git"].get("depot")
                                               or "").strip()
        except ErreurPilier as e:
            self._erreur("Git : %s" % e)
            return self.finaliser(False)
        self.etape(3, "Partage du dossier Drive en lecture publique")
        dossier_id = (self.cfg["drive"].get("dossier_projet")
                      or "").strip()
        try:
            if dossier_id or self.demo:
                self.piliers["drive"].partager(
                    dossier_id, dry=self.simulation or self.demo)
                if dossier_id:
                    self.rapport["liens"]["drive_dossier"] = dossier_id
            else:
                self.j.info("aucun dossier Drive configure - partage ignore")
        except ErreurPilier as e:
            self._erreur("Drive : %s" % e)
            return self.finaliser(False)
        self.etape(4, "Publication Zenodo (nouvelle version + DOI)")
        try:
            archive, _ = construire_archive(
                self.cfg, self.j, simulation=self.simulation or self.demo)
            identifiant, bucket = self.piliers["zenodo"].preparer_version(
                dry=self.simulation or self.demo)
            self.piliers["zenodo"].televerser(
                bucket, archive, dry=self.simulation or self.demo)
            doi = self.piliers["zenodo"].publier(
                identifiant, dry=self.simulation or self.demo)
            self.rapport["liens"]["zenodo_doi"] = str(doi)
        except ErreurPilier as e:
            self._erreur("Zenodo : %s" % e)
            return self.finaliser(False)
        if (not self.simulation and not self.demo
                and self.cfg["zenodo"].get("environnement") != "production"):
            self.j.info("NB : environnement Zenodo = sandbox ; passez a "
                        "'production' dans la configuration pour un DOI "
                        "definitif")
        self.j.titre("Verdict : passage public accompli - le projet est "
                     "en ligne")
        return self.finaliser(True)


class CycleCompletCeremonie(Ceremonie):
    nom = "Cycle complet autonome"
    nom_id = "cycle-complet"
    description = ("Verification -> rotation automatique si necessaire -> "
                   "synchronisation -> passage public. Un seul clic.")

    def executer(self):
        self.j.titre("CYCLE COMPLET AUTONOME - %s"
                     % datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.total = 6
        self.etape(1, "Phase 1/3 : verification des piliers")
        verification = VerificationCeremonie(
            self.cfg, self.j, demo=self.demo, simulation=self.simulation)
        rapport_verif = verification.executer()
        self.rapport["etats"] = rapport_verif.get("etats", {})
        besoin_rotation = any(
            e in ("invalide", "absent")
            for e in self.rapport["etats"].values())
        rotation_effectuee = False
        if besoin_rotation:
            self.etape(2, "Jetons manquants ou perimes : rotation "
                          "automatique")
            rotation = RotationCeremonie(
                self.cfg, self.j, demo=self.demo, simulation=self.simulation)
            if not rotation.executer()["succes"]:
                self._erreur("rotation automatique impossible : completez "
                             "les jetons (Configuration ou import d'un "
                             "dossier) puis relancez")
                return self.finaliser(False)
            rotation_effectuee = True
        else:
            self.etape(2, "Jetons a jour : rotation inutile")
        if rotation_effectuee and not self.demo and not self.simulation:
            self.etape(3, "Phase 2/3 : re-verification apres rotation")
            etats = {}
            for cle in ("git", "drive", "zenodo"):
                etat, detail = self.piliers[cle].verifier()
                etats[cle] = etat
                (self.j.ok if etat == "ok" else self.j.info)(
                    "%s : %s" % (self.piliers[cle].nom, detail))
            if not all(e == "ok" for e in etats.values()):
                self._erreur("des piliers restent indisponibles - arret "
                             "avant toute ecriture")
                return self.finaliser(False)
        else:
            self.etape(3, "Phase 2/3 : piliers deja verifies")
        self.etape(4, "Phase 3/3a : synchronisation Git + Drive")
        if not SynchronisationCeremonie(
                self.cfg, self.j, demo=self.demo,
                simulation=self.simulation).executer()["succes"]:
            self._erreur("synchronisation echouee - le passage public est "
                         "reporte (prudence)")
            return self.finaliser(False)
        self.etape(5, "Phase 3/3b : passage public (Git public + Drive "
                      "partage + DOI Zenodo)")
        rapport_public = PassagePublicCeremonie(
            self.cfg, self.j, demo=self.demo,
            simulation=self.simulation).executer()
        self.rapport["liens"].update(rapport_public.get("liens", {}))
        if not rapport_public["succes"]:
            self._erreur("passage public incomplet - consultez le journal")
            return self.finaliser(False)
        self.etape(6, "Rapport final")
        for cle, valeur in sorted(self.rapport["liens"].items()):
            self.j.info("lien %s : %s" % (cle, valeur))
        self.j.titre("Verdict : cycle complet accompli - la triade est a "
                     "jour et publique")
        return self.finaliser(True)


class InitialisationCeremonie(Ceremonie):
    nom = "Initialisation"
    nom_id = "initialisation"
    description = ("Nouveau projet triade : git init + premier commit + "
                   "push, dossier Drive, depot Zenodo en brouillon, "
                   "premiere synchronisation.")

    def executer(self):
        self.j.titre("Ceremonie d'initialisation - %s"
                     % datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.total = 4
        self.etape(1, "Depot Git local + premier commit + push")
        try:
            self.piliers["git"].initialiser(dry=self.simulation or self.demo)
        except ErreurPilier as e:
            self._erreur("Git : %s" % e)
            return self.finaliser(False)
        self.etape(2, "Dossier Drive du projet")
        dossier_id = (self.cfg["drive"].get("dossier_projet")
                      or "").strip()
        try:
            if dossier_id:
                self.j.info("dossier Drive existant conserve : %s"
                            % dossier_id)
            else:
                identifiant = self.piliers["drive"].creer_dossier(
                    self.cfg["projet"].get("nom", "projet-triade"),
                    dry=self.simulation or self.demo)
                if (identifiant and not self.simulation and not self.demo):
                    self.cfg["drive"]["dossier_projet"] = identifiant
                    Config.sauvegarder(self.cfg)
                self.j.ok("dossier Drive pret : %s"
                          % (identifiant or dossier_id or "existant"))
        except ErreurPilier as e:
            self._erreur("Drive : %s" % e)
            return self.finaliser(False)
        self.etape(3, "Depot Zenodo (brouillon)")
        try:
            if (self.cfg["zenodo"].get("depot_id") or "").strip():
                self.j.info("depot Zenodo existant : n°%s"
                            % self.cfg["zenodo"]["depot_id"])
            else:
                self.piliers["zenodo"].creer_depot(
                    dry=self.simulation or self.demo)
        except ErreurPilier as e:
            self._erreur("Zenodo : %s" % e)
            return self.finaliser(False)
        self.etape(4, "Premiere synchronisation")
        if not SynchronisationCeremonie(
                self.cfg, self.j, demo=self.demo,
                simulation=self.simulation).executer()["succes"]:
            self._erreur("premiere synchronisation echouee")
            return self.finaliser(False)
        self.j.titre("Verdict : projet triade initialise "
                     "(Git + Drive + Zenodo)")
        return self.finaliser(True)


FABRIQUE = {
    "initialisation": InitialisationCeremonie,
    "verification": VerificationCeremonie,
    "rotation": RotationCeremonie,
    "synchronisation": SynchronisationCeremonie,
    "passage-public": PassagePublicCeremonie,
    "cycle-complet": CycleCompletCeremonie,
}


# =============================================================================
# Interface graphique 1-clic
# =============================================================================

COULEURS = {
    "fond": "#0d1117", "panneau": "#161b22", "bord": "#30363d",
    "texte": "#e6edf3", "gris": "#8b949e",
    "vert": "#238636", "vert_clair": "#3fb950",
    "rouge": "#da3633", "rouge_clair": "#f85149",
    "jaune": "#d29922", "bleu": "#1f6feb", "bleu_clair": "#58a6ff",
}

CEREMONIES = [
    ("initialisation", "Initialisation",
     "Nouveau projet : git init, dossier Drive, depot Zenodo"),
    ("verification", "Verification",
     "Controle des trois piliers et des jetons"),
    ("rotation", "Rotation",
     "Import des nouveaux jetons (Drive public ou dossier local)"),
    ("synchronisation", "Synchronisation",
     "Git commit + push, archive sur Drive"),
    ("passage-public", "Passage public",
     "Git public, Drive partage, DOI Zenodo"),
]

ETATS_LED = {"ok": "#3fb950", "partiel": "#d29922", "invalide": "#f85149",
             "absent": "#8b949e", "erreur": "#f85149"}

TEXTE_AIDE = """TRIADE KIT - Aide rapide

PRINCIPE
  Trois piliers (Git, Google Drive, Zenodo) sont pilotes par des
  ceremonies. Le grand bouton vert execute le cycle complet :
  verification -> rotation si necessaire -> synchronisation ->
  passage public. Un seul clic.

LES CEREMONIES
  Initialisation    Prepare un nouveau projet : depot git local +
                    premier commit + push, dossier Drive, depot Zenodo
                    en brouillon, premiere synchronisation.
  Verification      Controle les jetons et la connectivite de chaque
                    pilier (voyants en haut a droite).
  Rotation          Importe les nouveaux jetons depuis le dossier Drive
                    public des jetons, ou un dossier local, les valide
                    un par un, puis met a jour la configuration
                    (l'ancienne est archivee dans config/).
  Synchronisation   Git commit + push ; archive du projet televersee
                    sur Drive (jetons et configuration exclus).
  Passage public    Depot GitHub rendu public, dossier Drive partage
                    en lecture, nouvelle version Zenodo publiee (DOI
                    definitif en environnement production).

OU TROUVER LES JETONS
  Git     https://github.com/settings/tokens (portee "repo")
  Drive   jeton OAuth d'acces (+ optionnel refresh token, client_id,
          client_secret)
  Zenodo  https://zenodo.org/account/settings/applications/
  Astuce : nommez vos fichiers jeton-git.txt, jeton-drive.txt,
  jeton-zenodo.txt pour que la rotation les reconnaisse.

MODES
  Reel           Actions effectives sur vos depots.
  Simulation     Tout est journalise, rien n'est ecrit (case a cocher).
  Demonstration  Ceremonies simulees, aucun jeton requis (bouton Demo).

SECURITE
  Les jetons restent dans config/triade.json sur votre machine. Ils ne
  sont jamais journalises (masques) ni inclus dans les archives. Zenodo
  cible la sandbox par defaut ; passez la configuration sur
  "production" pour un DOI definitif.

LIGNE DE COMMANDE
  python3 TriadeKit.py --cli verification
  python3 TriadeKit.py --cli rotation --dossier-jetons ~/Telechargements
  python3 TriadeKit.py --cli cycle-complet --simulation
  python3 TriadeKit.py --selftest
"""


if TK_DISPONIBLE:

    class Interface(tk.Tk):

        def __init__(self, demo=False):
            super().__init__()
            self.title("Triade Kit %s - Git / Google Drive / Zenodo"
                       % VERSION)
            self.configure(bg=COULEURS["fond"])
            self.geometry("1020x700")
            self.minsize(880, 620)
            self.demo = demo
            self.cfg = Config.charger()
            self.file = Queue()
            self.occupe = False
            self.boutons = []
            self._construire()
            self.after(150, self._consommer_file)
            self.after(400, self.verifier_piliers)
            self.after(900, self._premiere_fois)
            self.protocol("WM_DELETE_WINDOW", self._fermer)

        # ---------------- construction de la fenetre ----------------

        def _construire(self):
            self.bandeau_demo = tk.Label(
                self, text="MODE DEMONSTRATION - aucune action reelle, "
                           "aucun jeton requis",
                bg=COULEURS["jaune"], fg="#1b1f24",
                font=("Helvetica", 10, "bold"), pady=4)
            self.entete = tk.Frame(self, bg=COULEURS["fond"])
            self.entete.pack(fill="x", padx=16, pady=(12, 2))
            tk.Label(self.entete, text="TRIADE KIT",
                     font=("Helvetica", 20, "bold"),
                     fg=COULEURS["texte"],
                     bg=COULEURS["fond"]).pack(side="left")
            tk.Label(self.entete,
                     text="v%s  -  Git / Google Drive / Zenodo" % VERSION,
                     font=("Helvetica", 10), fg=COULEURS["gris"],
                     bg=COULEURS["fond"]).pack(side="left", padx=10,
                                               pady=(12, 0))
            cadre_leds = tk.Frame(self.entete, bg=COULEURS["fond"])
            cadre_leds.pack(side="right")
            self.leds = {}
            for nom in ("GIT", "DRIVE", "ZENODO"):
                led = tk.Label(cadre_leds, text="%s  -" % nom,
                               font=("Helvetica", 10, "bold"),
                               fg=COULEURS["gris"], bg=COULEURS["fond"])
                led.pack(side="left", padx=8)
                self.leds[nom] = led
            if self.demo:
                self.bandeau_demo.pack(fill="x", before=self.entete)

            zone_cycle = tk.Frame(self, bg=COULEURS["fond"])
            zone_cycle.pack(fill="x", padx=16, pady=10)
            self.bouton_cycle = tk.Button(
                zone_cycle, text="LANCER LE CYCLE COMPLET AUTONOME",
                command=lambda: self.demarrer("cycle-complet"),
                bg=COULEURS["vert"], fg="white",
                activebackground=COULEURS["vert_clair"],
                activeforeground="white",
                font=("Helvetica", 14, "bold"), relief="flat", bd=0,
                pady=12, cursor="hand2")
            self.bouton_cycle.pack(fill="x")
            self.boutons.append(self.bouton_cycle)
            tk.Label(zone_cycle, bg=COULEURS["fond"],
                     fg=COULEURS["gris"],
                     text="verification -> rotation si necessaire -> "
                          "synchronisation -> passage public - un seul "
                          "clic, rien a installer d'autre",
                     font=("Helvetica", 9)).pack(pady=(5, 0))

            grille = tk.Frame(self, bg=COULEURS["fond"])
            grille.pack(fill="x", padx=16, pady=(2, 8))
            for col, (identifiant, nom, _) in enumerate(CEREMONIES):
                bouton = tk.Button(
                    grille, text=nom,
                    command=lambda i=identifiant: self.demarrer(i),
                    bg=COULEURS["panneau"], fg=COULEURS["texte"],
                    activebackground=COULEURS["bord"],
                    activeforeground=COULEURS["texte"],
                    disabledforeground=COULEURS["gris"],
                    font=("Helvetica", 10, "bold"), relief="solid", bd=1,
                    padx=8, pady=12, cursor="hand2",
                    highlightbackground=COULEURS["bord"])
                bouton.grid(row=0, column=col, sticky="nsew", padx=3)
                grille.columnconfigure(col, weight=1)
                self.boutons.append(bouton)

            barre = tk.Frame(self, bg=COULEURS["panneau"])
            barre.pack(fill="x", padx=16, pady=4)
            self.var_simulation = tk.BooleanVar(
                value=bool(self.cfg["preferences"].get("simulation")))
            tk.Checkbutton(
                barre, text="Mode simulation (aucune ecriture)",
                variable=self.var_simulation,
                command=self._bascule_simulation,
                bg=COULEURS["panneau"], fg=COULEURS["texte"],
                selectcolor=COULEURS["fond"],
                activebackground=COULEURS["panneau"],
                activeforeground=COULEURS["texte"]).pack(
                    side="left", padx=8, pady=6)
            for texte, commande in (
                    ("Configuration...", self.ouvrir_configuration),
                    ("Rotation : importer un dossier...",
                     lambda: self.demarrer("rotation", dossier=True)),
                    ("Demo", self._activer_demo),
                    ("Aide", self.afficher_aide),
                    ("Journal", self._ouvrir_journal)):
                tk.Button(barre, text=texte, command=commande,
                          bg=COULEURS["panneau"], fg=COULEURS["bleu_clair"],
                          activebackground=COULEURS["bord"],
                          activeforeground=COULEURS["bleu_clair"],
                          disabledforeground=COULEURS["gris"],
                          relief="flat", cursor="hand2",
                          font=("Helvetica", 10)).pack(side="left",
                                                       padx=4, pady=6)

            zone_journal = tk.Frame(self, bg=COULEURS["fond"])
            zone_journal.pack(fill="both", expand=True, padx=16, pady=(2, 4))
            self.zone = scrolledtext.ScrolledText(
                zone_journal, bg=COULEURS["panneau"],
                fg=COULEURS["texte"], insertbackground=COULEURS["texte"],
                relief="flat", font=("Courier New", 10), state="normal")
            self.zone.pack(fill="both", expand=True)
            for etiquette, couleur in (
                    (" OK ", COULEURS["vert_clair"]),
                    ("ERREUR", COULEURS["rouge_clair"]),
                    ("ETAPE", COULEURS["bleu_clair"]),
                    ("INFO", COULEURS["texte"]),
                    ("=====", COULEURS["jaune"]),
                    ("FIN", COULEURS["gris"])):
                self.zone.tag_configure(etiquette, foreground=couleur)
            self.zone.insert("end", "Triade Kit %s - journal de ceremonie\n"
                             % VERSION, "=====")
            self.zone.insert("end", "Le cycle complet autonome s'execute "
                             "en un clic. Modes : reel, simulation "
                             "(case a cocher), demonstration (bouton "
                             "Demo).\n\n", "INFO")

            bas = tk.Frame(self, bg=COULEURS["panneau"])
            bas.pack(fill="x", padx=16, pady=(0, 10))
            self.progression = ttk.Progressbar(bas, mode="determinate",
                                               maximum=100)
            self.progression.pack(side="left", fill="x", expand=True,
                                  pady=8)
            self.etiquette_etat = tk.Label(
                bas, text="Pret.", bg=COULEURS["panneau"],
                fg=COULEURS["gris"], width=42, anchor="w")
            self.etiquette_etat.pack(side="left", padx=8)

        # ---------------- communication threads -> GUI ----------------

        def _sortie(self, niveau, message):
            self.file.put(("ligne", niveau, message))

        def _avancement(self, i, n):
            self.file.put(("avancement", i, n))

        def _consommer_file(self):
            while True:
                try:
                    element = self.file.get_nowait()
                except Empty:
                    break
                if element[0] == "ligne":
                    _, niveau, message = element
                    horodatage = datetime.now().strftime("%H:%M:%S")
                    self.zone.insert("end", "%s  %-6s %s\n"
                                     % (horodatage, niveau, message),
                                     niveau)
                    self.zone.see("end")
                elif element[0] == "avancement":
                    _, i, n = element
                    self.progression.config(value=100.0 * i / max(n, 1))
                elif element[0] == "led":
                    _, cle, etat = element
                    if cle.upper() in self.leds:
                        self.leds[cle.upper()].config(
                            fg=ETATS_LED.get(etat, COULEURS["gris"]))
                elif element[0] == "fin":
                    _, identifiant, rapport = element
                    self._terminer(identifiant, rapport)
            self.after(150, self._consommer_file)

        # ---------------- lancement des ceremonies ----------------

        def demarrer(self, identifiant, dossier=False):
            if self.occupe:
                return
            if identifiant == "rotation" and dossier:
                dossier_choisi = filedialog.askdirectory(
                    title="Dossier contenant les nouveaux jetons")
                if not dossier_choisi:
                    return
                self._lancer(identifiant, dossier_jetons=dossier_choisi)
                return
            if (identifiant in ("passage-public", "cycle-complet")
                    and not self.demo
                    and not self.var_simulation.get()
                    and self.cfg["preferences"].get("confirmation_public",
                                                    True)):
                if not messagebox.askyesno(
                        "Confirmation - passage public",
                        "Le passage public est definitif :\n\n"
                        "  - le depot GitHub devient visible publiquement\n"
                        "  - le dossier Drive sera partage en lecture\n"
                        "  - un DOI Zenodo sera publie (irreversible)\n\n"
                        "Poursuivre le passage public ?",
                        icon="warning", default="no"):
                    return
            self._lancer(identifiant)

        def _lancer(self, identifiant, dossier_jetons=None):
            self.occupe = True
            for b in self.boutons:
                b.config(state="disabled")
            self.etiquette_etat.config(
                text="Ceremonie en cours : %s" % identifiant)
            self.progression.config(value=0)
            journal = Journal(identifiant, sortie=self._sortie,
                              avancement=self._avancement)
            simulation = self.var_simulation.get()
            demo = self.demo
            cfg = self.cfg

            def travail():
                try:
                    ceremonie = FABRIQUE[identifiant](
                        cfg, journal, demo=demo, simulation=simulation)
                    if identifiant == "rotation" and dossier_jetons:
                        rapport = ceremonie.executer(
                            dossier_jetons=dossier_jetons)
                    else:
                        rapport = ceremonie.executer()
                except Exception as e:
                    journal.erreur("exception inattendue : %s" % e)
                    traceback.print_exc()
                    rapport = {"succes": False}
                self.file.put(("fin", identifiant, rapport))

            threading.Thread(target=travail, daemon=True).start()

        def _terminer(self, identifiant, rapport):
            self.occupe = False
            for b in self.boutons:
                b.config(state="normal")
            succes = rapport.get("succes")
            self.etiquette_etat.config(
                text=("Termine : succes" if succes
                      else "Termine : echec (voir journal)"))
            if succes:
                self.progression.config(value=100)
            self.verifier_piliers()
            if not succes:
                messagebox.showerror(
                    "Triade Kit",
                    "La ceremonie '%s' s'est terminee en echec.\n"
                    "Consultez le journal pour les details." % identifiant)
                return
            liens = rapport.get("liens") or {}
            doi = liens.get("zenodo_doi", "")
            if (identifiant in ("passage-public", "cycle-complet") and doi
                    and "simul" not in doi and "demo" not in doi.lower()):
                if messagebox.askyesno(
                        "Triade Kit",
                        "Passage public accompli.\n\nDOI Zenodo : %s\n\n"
                        "Ouvrir la page du DOI ?" % doi):
                    webbrowser.open("https://doi.org/%s" % doi)

        # ---------------- voyants / preferences ----------------

        def verifier_piliers(self):
            def travail():
                piliers = construire_piliers(
                    self.cfg, Journal("voyants", sortie=lambda n, m: None),
                    demo=self.demo)
                for cle in ("git", "drive", "zenodo"):
                    try:
                        etat, _ = piliers[cle].verifier()
                    except Exception:
                        etat = "erreur"
                    self.file.put(("led", cle, etat))
            threading.Thread(target=travail, daemon=True).start()

        def _bascule_simulation(self):
            self.cfg["preferences"]["simulation"] = bool(
                self.var_simulation.get())
            Config.sauvegarder(self.cfg)
            self._sortie("INFO", "mode simulation : %s"
                         % ("active" if self.var_simulation.get()
                            else "desactive"))

        def _activer_demo(self):
            if self.demo:
                return
            self.demo = True
            self.bandeau_demo.pack(fill="x", before=self.entete)
            self._sortie("INFO", "mode demonstration active - les "
                          "ceremonies suivantes seront simulees")
            self.verifier_piliers()

        def _premiere_fois(self):
            if self.demo:
                return
            if any([(self.cfg["git"].get("jeton") or "").strip(),
                    (self.cfg["drive"].get("jeton_acces") or "").strip(),
                    (self.cfg["zenodo"].get("jeton") or "").strip()]):
                return
            choix = messagebox.askyesnocancel(
                "Bienvenue dans le Triade Kit",
                "Aucun jeton n'est encore configure.\n\n"
                "Voulez-vous essayer le kit en mode demonstration ?\n\n"
                "Oui : demonstration immediate (aucun jeton)\n"
                "Non : ouvrir la configuration pour coller vos jetons\n"
                "Annuler : continuer tel quel")
            if choix is True:
                self._activer_demo()
            elif choix is False:
                self.ouvrir_configuration()

        # ---------------- fenetres secondaires ----------------

        def ouvrir_configuration(self):
            fenetre = tk.Toplevel(self)
            fenetre.title("Configuration de la triade")
            fenetre.configure(bg=COULEURS["fond"])
            fenetre.geometry("700x640")
            fenetre.transient(self)
            fenetre.grab_set()
            champs = []

            def section(titre):
                tk.Label(fenetre, text=titre, font=("Helvetica", 11,
                                                    "bold"),
                         fg=COULEURS["bleu_clair"], bg=COULEURS["fond"]
                         ).pack(anchor="w", padx=14, pady=(10, 2))

            def ajouter(libelle, chemin, masque=False):
                ligne = tk.Frame(fenetre, bg=COULEURS["fond"])
                ligne.pack(fill="x", padx=14, pady=2)
                tk.Label(ligne, text=libelle, width=30, anchor="w",
                         bg=COULEURS["fond"],
                         fg=COULEURS["gris"]).pack(side="left")
                var = tk.StringVar(value=str(obtenir(self.cfg, chemin)))
                entree = tk.Entry(ligne, textvariable=var,
                                  bg=COULEURS["panneau"],
                                  fg=COULEURS["texte"],
                                  insertbackground=COULEURS["texte"],
                                  relief="solid", bd=1,
                                  show=("\u2022" if masque else ""))
                entree.pack(side="left", fill="x", expand=True)
                champs.append((chemin, var))

            section("Projet")
            ajouter("Nom du projet", ("projet", "nom"))
            ajouter("Dossier local (vide = dossier du kit)",
                    ("projet", "dossier_local"))
            section("Git (GitHub)")
            ajouter("URL du depot GitHub", ("git", "depot"))
            ajouter("Jeton (Personal Access Token)",
                    ("git", "jeton"), masque=True)
            ajouter("Branche", ("git", "branche"))
            section("Google Drive")
            ajouter("Jeton d'acces", ("drive", "jeton_acces"),
                    masque=True)
            ajouter("Jeton d'actualisation (option)",
                    ("drive", "jeton_actualisation"), masque=True)
            ajouter("Client ID (option)", ("drive", "client_id"))
            ajouter("Client secret (option)", ("drive", "client_secret"),
                    masque=True)
            ajouter("ID du dossier projet", ("drive", "dossier_projet"))
            ajouter("ID du dossier des jetons", ("drive", "dossier_jetons"))
            section("Zenodo")
            ajouter("Jeton", ("zenodo", "jeton"), masque=True)
            ajouter("ID du depot", ("zenodo", "depot_id"))
            ligne_env = tk.Frame(fenetre, bg=COULEURS["fond"])
            ligne_env.pack(fill="x", padx=14, pady=2)
            tk.Label(ligne_env, text="Environnement", width=30, anchor="w",
                     bg=COULEURS["fond"],
                     fg=COULEURS["gris"]).pack(side="left")
            var_env = tk.StringVar(
                value=str(self.cfg["zenodo"].get("environnement",
                                                 "sandbox")))
            ttk.Combobox(ligne_env, textvariable=var_env, width=18,
                         values=("sandbox", "production"),
                         state="readonly").pack(side="left")
            ajouter("Titre du depot", ("zenodo", "metadata", "titre"))
            ajouter("Auteur", ("zenodo", "metadata", "auteur"))
            ajouter("Description", ("zenodo", "metadata", "description"))
            ajouter("Licence", ("zenodo", "metadata", "licence"))

            pied = tk.Frame(fenetre, bg=COULEURS["fond"])
            pied.pack(fill="x", padx=14, pady=12)
            tk.Label(pied, text="Les jetons restent en local "
                     "(config/triade.json), jamais journalises.",
                     fg=COULEURS["gris"], bg=COULEURS["fond"]).pack(
                         side="left")

            def enregistrer():
                for chemin, var in champs:
                    definir(self.cfg, chemin, var.get().strip())
                self.cfg["zenodo"]["environnement"] = var_env.get()
                Config.sauvegarder(self.cfg)
                fenetre.destroy()
                self.verifier_piliers()
                self._sortie("INFO", "configuration enregistree")
                messagebox.showinfo("Triade Kit",
                                    "Configuration enregistree.")

            tk.Button(pied, text="Enregistrer", command=enregistrer,
                      bg=COULEURS["vert"], fg="white", relief="flat",
                      font=("Helvetica", 10, "bold"), padx=14,
                      cursor="hand2").pack(side="right", padx=4)
            tk.Button(pied, text="Annuler",
                      command=fenetre.destroy,
                      bg=COULEURS["panneau"],
                      fg=COULEURS["texte"], relief="flat",
                      cursor="hand2").pack(side="right", padx=4)
            tk.Button(pied, text="Ouvrir le dossier Drive des jetons",
                      command=lambda: webbrowser.open(
                          "https://drive.google.com/drive/folders/%s"
                          % (self.cfg["drive"].get("dossier_jetons")
                             or "")),
                      bg=COULEURS["panneau"],
                      fg=COULEURS["bleu_clair"], relief="flat",
                      cursor="hand2").pack(side="right", padx=4)

        def afficher_aide(self):
            fenetre = tk.Toplevel(self)
            fenetre.title("Aide du Triade Kit")
            fenetre.configure(bg=COULEURS["fond"])
            fenetre.geometry("720x560")
            fenetre.transient(self)
            zone = scrolledtext.ScrolledText(
                fenetre, bg=COULEURS["panneau"], fg=COULEURS["texte"],
                relief="flat", font=("Courier New", 10))
            zone.pack(fill="both", expand=True)
            zone.insert("1.0", TEXTE_AIDE)
            zone.config(state="disabled")

        def _ouvrir_journal(self):
            DOSSIER_JOURNAL.mkdir(parents=True, exist_ok=True)
            chemin = str(DOSSIER_JOURNAL)
            try:
                if sys.platform.startswith("win"):
                    os.startfile(chemin)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", chemin])
                else:
                    subprocess.Popen(["xdg-open", chemin])
            except Exception:
                self._sortie("INFO", "journal : %s" % chemin)

        def _fermer(self):
            if self.occupe:
                if not messagebox.askyesno(
                        "Triade Kit",
                        "Une ceremonie est en cours. Quitter quand meme ?"):
                    return
            self.destroy()


# =============================================================================
# Ligne de commande / auto-diagnostic
# =============================================================================

def mode_cli(args):
    cfg = Config.charger()
    identifiant = args.cli
    if identifiant not in FABRIQUE:
        print("Ceremonies disponibles : " + ", ".join(FABRIQUE))
        return 2
    simulation = bool(args.simulation
                      or cfg["preferences"].get("simulation"))
    journal = Journal(identifiant)
    ceremonie = FABRIQUE[identifiant](cfg, journal, demo=args.demo,
                                      simulation=simulation)
    kwargs = {}
    if identifiant == "rotation" and args.dossier_jetons:
        kwargs["dossier_jetons"] = args.dossier_jetons
    rapport = ceremonie.executer(**kwargs)
    liens = rapport.get("liens") or {}
    if liens:
        print("\nLiens :")
        for cle, valeur in sorted(liens.items()):
            print("  %s : %s" % (cle, valeur))
    return 0 if rapport.get("succes") else 1


def auto_diagnostic():
    print("Triade Kit %s - auto-diagnostic" % VERSION)
    print("-" * 60)
    resultats = []

    def verifier(nom, ok, detail="", bloquant=True):
        resultats.append((nom, ok, bloquant))
        print("  [%s] %-38s %s" % ("OK" if ok else "!!", nom,
                                   ("- " + detail) if detail else ""))

    verifier("Version de Python", sys.version_info >= (3, 8),
             sys.version.split()[0])
    verifier("git installe", bool(shutil.which("git")),
             shutil.which("git") or "installez git")
    if TK_DISPONIBLE:
        verifier("tkinter (interface graphique)", True, "disponible")
    else:
        verifier("tkinter (interface graphique)", False,
                 "absent - le mode --cli reste utilisable",
                 bloquant=False)
    try:
        cfg = Config.charger()
        verifier("configuration chargeable", True, str(FICHIER_CONFIG))
        Config.sauvegarder(cfg)
        verifier("configuration inscriptible", True)
    except Exception as e:
        verifier("configuration chargeable", False, str(e)[:70])
    r = HTTP.requete("GET", "https://api.github.com", timeout=10)
    verifier("reseau (api.github.com)", r.statut > 0,
             ("HTTP %s" % r.statut) if r.statut else
             "aucun acces - verifiez la connexion", bloquant=False)
    journal = Journal("auto-diagnostic")
    cycle = CycleCompletCeremonie(cfg, journal, demo=True, simulation=True)
    rapport = cycle.executer()
    verifier("cycle complet en mode demo/simulation",
             rapport.get("succes") is True)
    print("-" * 60)
    ok_global = (all(ok for _, ok, bloquant in resultats if bloquant)
                 and rapport.get("succes"))
    print("Auto-diagnostic : %s" % (
        "TOUT EST OPERATIONNEL" if ok_global
        else "des points exigent votre attention (voir ci-dessus)"))
    return 0 if ok_global else 1


def main():
    analyseur = argparse.ArgumentParser(
        prog="TriadeKit",
        description="Kit triade Git / Google Drive / Zenodo - GUI 1-clic "
                    "autonome pour les ceremonies.")
    analyseur.add_argument(
        "--demo", action="store_true",
        help="mode demonstration : ceremonies simulees, aucun jeton requis")
    analyseur.add_argument(
        "--cli", metavar="CEREMONIE",
        help="execute une ceremonie sans interface : %s"
             % ", ".join(FABRIQUE))
    analyseur.add_argument(
        "--simulation", action="store_true",
        help="force le mode simulation (aucune ecriture reelle)")
    analyseur.add_argument(
        "--dossier-jetons", metavar="DOSSIER",
        help="rotation : dossier local contenant les nouveaux jetons")
    analyseur.add_argument("--selftest", action="store_true",
                           help="auto-diagnostic complet du kit")
    analyseur.add_argument("--version", action="version",
                           version="TriadeKit " + VERSION)
    args = analyseur.parse_args()
    if args.selftest:
        return auto_diagnostic()
    if args.cli:
        return mode_cli(args)
    if not TK_DISPONIBLE:
        print("Interface graphique indisponible (tkinter absent).")
        print("Exemples en ligne de commande :")
        print("  python3 TriadeKit.py --cli verification")
        print("  python3 TriadeKit.py --demo --cli cycle-complet")
        return 1
    try:
        app = Interface(demo=args.demo)
    except Exception as e:
        print("Interface graphique indisponible (%s)." % e)
        print("Exemples en ligne de commande :")
        print("  python3 TriadeKit.py --cli verification")
        print("  python3 TriadeKit.py --demo --cli cycle-complet")
        return 1
    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
