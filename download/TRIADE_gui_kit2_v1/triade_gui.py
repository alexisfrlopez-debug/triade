#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — GUI kit-2 (dudect) · console autonome · v1.0.0
=========================================================================
Fichier UNIQUE, sans aucune dépendance (Python >= 3.8, stdlib uniquement).

But :
  1. Journaliser dès son lancement (environnement, architecture, montage,
     toolchain) dans TRIADE_logs/gui_<horodatage>.log
  2. Bouton « LANCER KIT-2 » : pré-diagnostic (ELF/noexec/CRLF), exécution
     avec capture complète stdout+stderr, code retour, durée.
  3. Bouton « ENVOYER LES LOGS AU DRIVE » : envoi vers /test du Drive
     TRIADE — rclone (automatique), compte de service (automatique),
     ou repli manuel assisté (zip + lien + partage Android).
  Ensuite, l'agent relève les logs depuis le Drive pour analyse
  (en particulier du crash au lancement de kit-2 sur téléphone).

Lancement :
    python3 triade_gui.py [--port 8420]
puis ouvrir l'URL affichée (le GUI tente de l'ouvrir seul).
"""

import base64
import configparser
import datetime as dt
import itertools
import json
import os
import platform
import re
import shlex
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import urllib.parse
import urllib.request
import webbrowser
import zipfile
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APP_NAME = "TRIADE GUI kit-2"
VERSION = "1.0.0"

SCRIPT_DIR = Path(__file__).resolve().parent
LOG_DIR = SCRIPT_DIR / "TRIADE_logs"
CONF_PATH = SCRIPT_DIR / "triade_gui.conf"

DRIVE_ROOT_URL = "https://drive.google.com/drive/folders/105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"

KIT_NAME_RE = re.compile(r"(triade|kit[\s_-]*2|dudect|kit[\s_-]*terrain)", re.I)

DEFAULTS = {
    "port": "8420",
    "bind": "0.0.0.0",
    "run_timeout": "600",
    "auto_send_after_run": "false",
    "copy_to_home_on_sdcard": "true",
    "kit2_dir": "",
    "kit2_cmd": "",
    "drive_remote": "triade",
    "drive_dest": "test/TRIADE_logs_gui",
    "drive_folder_id": "",
    "drive_folder_url": DRIVE_ROOT_URL,
    "drive_sa_file": "drive_sa.json",
}

CONF_TEMPLATE = """\
# triade_gui.conf — configuration du GUI kit-2 (facultatif)
# Tout est détecté automatiquement par défaut ; décommenter pour forcer.

[general]
# port = 8420
# bind = 0.0.0.0
# run_timeout = 600
# auto_send_after_run = false
# copy_to_home_on_sdcard = true

[kit2]
# dir = /data/data/com.termux/files/home/TRIADE_kits/TRIADE_kits_terrain_v0150_CORRECTIF2-kit-dudect
# cmd = bash run.sh

[drive]
# remote = triade
# dest = test/TRIADE_logs_gui
# folder_id = (ID du dossier /test, visible dans son URL ouverte dans le navigateur)
# folder_url = %s
# sa_file = drive_sa.json
""" % DRIVE_ROOT_URL


# --------------------------------------------------------------------------
# Petits utilitaires
# --------------------------------------------------------------------------

def now_iso():
    return dt.datetime.now().isoformat(timespec="seconds")


def sh(cmd, timeout=15, cwd=None):
    """Exécute une commande externe de façon sûre. Retour (rc, sortie_texte)."""
    try:
        p = subprocess.run(
            cmd, cwd=cwd, timeout=timeout, input=b"",
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        out = p.stdout.decode("utf-8", "replace").strip()
        return p.returncode, out
    except Exception as e:  # FileNotFoundError, TimeoutExpired, PermissionError...
        return -1, "%s: %s" % (type(e).__name__, e)


def which(name):
    return shutil.which(name) or ""


def human_bool(v):
    return str(v).strip().lower() in ("1", "true", "yes", "on")


def norm_machine(m):
    m = (m or "").lower()
    if m in ("x86_64", "amd64", "x64"):
        return "x86-64"
    if m in ("arm64", "aarch64"):
        return "aarch64"
    if m.startswith("arm"):
        return "arm"
    if m.startswith("riscv"):
        return "riscv64"
    return m or "?"


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


def elf_machine(p):
    """Lit l'en-tête ELF : retourne None si pas un ELF, sinon dict(class, machine)."""
    try:
        with open(p, "rb") as fh:
            h = fh.read(20)
    except Exception:
        return None
    if len(h) < 20 or h[:4] != b"\x7fELF":
        return None
    names = {0: "none", 2: "SPARC", 3: "x86", 8: "MIPS", 18: "PowerPC", 20: "PowerPC",
             22: "S390", 40: "ARM", 50: "ia-64", 62: "x86-64", 183: "aarch64", 243: "riscv64"}
    machine_code = h[18] | (h[19] << 8)  # LSB (Android/Linux le sont toujours)
    return {
        "class": "64" if h[4] == 2 else "32",
        "machine": names.get(machine_code, "0x%04x" % machine_code),
    }


# --------------------------------------------------------------------------
# Journal (fichier + taille en mémoire pour l'interface)
# --------------------------------------------------------------------------

class Logger:
    def __init__(self, log_dir):
        log_dir.mkdir(parents=True, exist_ok=True)
        self.path = log_dir / ("gui_%s.log" % time.strftime("%Y%m%d_%H%M%S"))
        self.lock = threading.Lock()
        self.tail = deque(maxlen=600)
        self._f = open(self.path, "a", buffering=1, encoding="utf-8")

    def _emit(self, line):
        with self.lock:
            self._f.write(line + "\n")
            self._f.flush()
            self.tail.append(line)

    def write(self, level, src, msg):
        msg = str(msg).replace("\r", "").rstrip("\n")
        for ln in (msg.split("\n") if msg else [""]):
            self._emit("[%s] [%-5s] [%-10s] %s" % (now_iso(), level, src, ln))

    def block(self, level, src, text):
        """Journalise un bloc multi-lignes (sortie de commande)."""
        text = (text or "").strip("\n")
        if not text:
            self.write(level, src, "(vide)")
            return
        for ln in text.splitlines():
            self.write(level, src, ln)

    def info(self, src, msg):
        self.write("INFO", src, msg)

    def ok(self, src, msg):
        self.write("OK", src, msg)

    def warn(self, src, msg):
        self.write("WARN", src, msg)

    def err(self, src, msg):
        self.write("ERR", src, msg)

    def out(self, line):
        self.write("OUT", "kit2", line)

    def section(self, title):
        bar = "=" * 72
        with self.lock:
            for ln in (bar, "SECTION — %s" % title, bar, ""):
                self._f.write(ln + "\n")
                self.tail.append(ln)
            self._f.flush()

    def snapshot(self):
        with self.lock:
            return list(self.tail)


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

CONF_SPEC = {
    # flat -> (section, option, type)
    "port": ("general", "port", str),
    "bind": ("general", "bind", str),
    "run_timeout": ("general", "run_timeout", str),
    "auto_send_after_run": ("general", "auto_send_after_run", bool),
    "copy_to_home_on_sdcard": ("general", "copy_to_home_on_sdcard", bool),
    "kit2_dir": ("kit2", "dir", str),
    "kit2_cmd": ("kit2", "cmd", str),
    "drive_remote": ("drive", "remote", str),
    "drive_dest": ("drive", "dest", str),
    "drive_folder_id": ("drive", "folder_id", str),
    "drive_folder_url": ("drive", "folder_url", str),
    "drive_sa_file": ("drive", "sa_file", str),
}


def load_conf(logger):
    cp = configparser.ConfigParser()
    if CONF_PATH.exists():
        try:
            cp.read(CONF_PATH, encoding="utf-8")
        except Exception as e:
            logger.warn("gui", "conf illisible (%s) — valeurs par défaut" % e)
    else:
        try:
            CONF_PATH.write_text(CONF_TEMPLATE, encoding="utf-8")
            logger.info("gui", "conf créée : %s (tout est optionnel)" % CONF_PATH.name)
        except Exception as e:
            logger.warn("gui", "conf non créable : %s" % e)

    conf = {}
    for flat, (sec, opt, kind) in CONF_SPEC.items():
        raw = cp.get(sec, opt) if cp.has_option(sec, opt) else DEFAULTS[flat]
        raw = str(raw).strip()
        conf[flat] = human_bool(raw) if kind is bool else raw
    return conf


# --------------------------------------------------------------------------
# Détection des kits + candidats de lancement
# --------------------------------------------------------------------------

def scan_roots():
    home = Path.home()
    cands = [
        SCRIPT_DIR, Path.cwd(), home, home / "TRIADE_kits",
        home / "storage" / "downloads", home / "storage" / "shared",
        home / "storage" / "download",
        Path("/sdcard/Download"), Path("/sdcard/Downloads"),
        Path("/storage/emulated/0/Download"), Path("/storage/emulated/0/Downloads"),
    ]
    seen, roots = set(), []
    for p in cands:
        try:
            if p.exists():
                rp = p.resolve()
                if rp not in seen:
                    seen.add(rp)
                    roots.append(p)
        except Exception:
            pass
    return roots


def scan_kits(logger, limit=15):
    """Retourne [{name, path, mtime, candidates, default_cmd}] triés par récence."""
    found = {}
    for root in scan_roots():
        is_storage = str(root.resolve()).startswith(("/storage/emulated", "/sdcard")) or "storage" in str(root)
        max_depth = 3 if is_storage else 2
        try:
            walked = 0
            for dirpath, dirnames, filenames in os.walk(str(root)):
                rel = os.path.relpath(dirpath, str(root))
                depth = 0 if rel == "." else rel.count(os.sep) + 1
                if depth >= max_depth:
                    dirnames[:] = []
                dirnames[:] = [d for d in dirnames
                               if not d.startswith(".")
                               and d not in ("Android", "proc", "sys", "dev", "cache", "node_modules")]
                walked += 1
                if walked > 2500:
                    break
                here = Path(dirpath)
                label_src = here.name or str(root)
                parent = here.parent.name if here.parent != here else ""
                if KIT_NAME_RE.search(label_src) or (parent and KIT_NAME_RE.search(parent)):
                    if "TRIADE_logs" in dirpath or str(LOG_DIR) == dirpath:
                        continue
                    if here in found:
                        continue
                    try:
                        if not any(here.iterdir()):
                            continue
                        found[here] = here.stat().st_mtime
                    except Exception:
                        pass
        except Exception:
            continue
        if len(found) >= 40:
            break

    # Déduplication hiérarchique : si un dossier détecté est l'ancêtre d'un
    # autre dossier détecté (ex. conteneur TRIADE_kits vs le kit réel),
    # on ne garde que le plus profond.
    for a in list(found):
        for b in found:
            if a != b and a in b.parents:
                found.pop(a, None)
                break

    kits = []
    for p, mtime in sorted(found.items(), key=lambda kv: -kv[1])[:limit]:
        cands = cmd_candidates(p)
        kits.append({
            "name": p.name,
            "path": str(p),
            "mtime": mtime,
            "candidates": cands,
            "default_cmd": (cands[0]["cmd"] if cands else "bash run.sh"),
        })
    return kits


def cmd_candidates(kit):
    """Classe les façons de lancer le kit, du plus au moins probable."""
    scored = {}

    def add(score, label, cmd):
        scored.setdefault(cmd, (score, label))

    files = {}
    try:
        for f in kit.iterdir():
            files[f.name.lower()] = f
    except Exception:
        pass

    for prio, name in enumerate(("run.sh", "run_kit2.sh", "run-kit2.sh", "run_dudect.sh",
                                 "launch.sh", "start.sh", "exec.sh")):
        if name in files:
            add(300 - prio, files[name].name, "bash %s" % files[name].name)

    for lname, f in files.items():
        if lname.endswith(".sh"):
            if re.search(r"(run|launch|start|exec|go)", lname):
                add(200, f.name, "bash %s" % f.name)
            elif re.search(r"(kit|dudect|build|make|go)", lname):
                add(150, f.name, "bash %s" % f.name)

    if "makefile" in files:
        add(180, "Makefile", "make")
    if "configure" in files and os.access(str(files["configure"]), os.X_OK):
        add(170, "configure+make", "./configure && make")
    if "configure.py" in files:
        add(140, "configure.py", "python3 configure.py")
    if "cmakelists.txt" in files:
        add(130, "cmake", "cmake . && make")

    try:
        depth2 = list(itertools.islice(kit.rglob("*"), 300))
    except Exception:
        depth2 = []
    for f in depth2:
        try:
            if not f.is_file():
                continue
            rel = f.relative_to(kit)
            if f.suffix.lower() in ("", ".bin", ".elf", ".out"):
                if os.access(str(f), os.X_OK) and re.search(r"(dudect|kit|test|run)", str(f).lower()):
                    add(160, str(rel), "./%s" % rel)
        except Exception:
            pass

    ordered = sorted(scored.items(), key=lambda kv: -kv[1][0])[:8]
    return [{"label": lbl, "cmd": cmd} for cmd, (sc, lbl) in ordered]


# --------------------------------------------------------------------------
# Pré-diagnostic avant lancement (c'est ici qu'on attrape le crash kit-2)
# --------------------------------------------------------------------------

def mount_opts_of(target):
    rc, out = sh(["mount"], timeout=10)
    if rc != 0 or not out:
        return None
    best = None
    for ln in out.splitlines():
        parts = ln.split()
        if len(parts) >= 4 and parts[1] == "on":
            mnt = parts[2].rstrip("/")
            opts = ""
            if "type" in parts:
                ti = parts.index("type")
                if ti + 2 < len(parts):
                    opts = parts[ti + 2]
            if not opts:
                opts = parts[-1]
            opts = opts.strip("()")
            if mnt and (str(target).startswith(mnt) or mnt == "/"):
                if best is None or len(mnt) > len(best[0]):
                    best = (mnt, opts)
    return best


def pre_run_diag(logger, kit, cmd):
    lg = logger
    lg.section("PRÉ-DIAGNOSTIC KIT-2 (avant lancement)")
    lg.info("diag", "cible : %s" % kit)
    lg.info("diag", "commande : %s" % cmd)

    u = platform.uname()
    host = norm_machine(u.machine)
    lg.info("diag", "hôte : %s | noyau %s %s | arch : %s" % (u.node, u.system, u.release, u.machine))

    rc, out = sh(["uname", "-a"], 8)
    if rc == 0:
        lg.info("diag", "uname -a : %s" % out)

    if which("getprop"):
        for k in ("ro.product.manufacturer", "ro.product.model", "ro.product.cpu.abi",
                  "ro.build.version.release"):
            rc, out = sh(["getprop", k], 6)
            lg.info("diag", "%s = %s" % (k, (out.strip() if rc == 0 else "?") or "?"))
    if which("getenforce"):
        rc, out = sh(["getenforce"], 6)
        lg.info("diag", "SELinux : %s" % (out.strip() or "?") if rc == 0 else "SELinux : ?")

    lg.info("diag", "PATH = %s" % os.environ.get("PATH", ""))
    for b in ("cc", "gcc", "clang", "make", "python3", "file", "openssl", "rclone"):
        lg.info("diag", "%-8s %s" % (b, which(b) or "absent"))

    rc, out = sh(["ls", "-la", str(kit)], 10)
    lg.block("INFO", "diag", out or "(ls indisponible)")

    mi = mount_opts_of(str(kit))
    if mi:
        lg.info("diag", "montage de %s : %s" % (mi[0] or "/", mi[1]))
        if "noexec" in mi[1]:
            lg.err("diag", "POINT CLE : montage NOEXEC — aucun binaire ne peut s'exécuter "
                            "depuis cet emplacement ; il faut copier le kit vers $HOME "
                            "(le GUI le fait si l'option est cochée).")
        if "ro" in [o.strip() for o in mi[1].split(",")]:
            lg.err("diag", "POINT CLE : montage en lecture seule (ro).")

    # Architecture des binaires ELF présents dans le kit
    elfs = []
    try:
        for f in itertools.islice(kit.rglob("*"), 400):
            if not f.is_file():
                continue
            try:
                if f.stat().st_size > 80 * 1024 * 1024:
                    continue
            except Exception:
                continue
            if f.suffix.lower() in (".sh", ".py", ".md", ".txt", ".log", ".json",
                                    ".conf", ".zip", ".c", ".h", ".o", ".a"):
                continue
            m = elf_machine(f)
            if m:
                elfs.append((f, m))
    except Exception:
        pass
    machines = set()
    for f, m in elfs[:20]:
        machines.add(m["machine"])
        lg.info("diag", "ELF %-9s class%s — %s" % (m["machine"], m["class"], f.name))
    if machines and host not in machines:
        lg.err("diag", "POINT CLE : ARCHITECTURE INCOMPATIBLE — binaires %s alors que "
                        "l'hôte est %s. Cause probable du crash au lancement."
                        % (", ".join(sorted(machines)), host))

    # Fins de ligne CRLF + shebang des scripts
    try:
        scripts = list(itertools.islice(kit.rglob("*.sh"), 25))
    except Exception:
        scripts = []
    for f in scripts:
        try:
            head = f.open("rb").read(600)
        except Exception:
            continue
        if b"\r\n" in head:
            lg.err("diag", "POINT CLE : CRLF (Windows) dans %s — sous Unix cela casse "
                            "shebang/parsing. Corriger : sed -i 's/\\r$//' %s" % (f.name, f.name))
        first = head.split(b"\n", 1)[0].decode("utf-8", "replace").strip()
        if first and not first.startswith("#!"):
            lg.warn("diag", "%s : pas de shebang (lancé via bash, toléré)" % f.name)
        elif first.startswith("#!"):
            lg.info("diag", "%s : shebang %r" % (f.name, first))

    return {"host": host, "elf_machines": sorted(machines)}


# --------------------------------------------------------------------------
# Copie éventuelle vers $HOME (SDCard souvent noexec)
# --------------------------------------------------------------------------

def ensure_runnable_location(logger, kit, copy_allowed):
    resolved = Path(os.path.realpath(str(kit)))
    if not str(resolved).startswith(("/storage/emulated", "/sdcard")):
        return kit
    if not copy_allowed:
        logger.warn("kit2", "le kit est sur stockage partagé (%s) — risque NOEXEC ; "
                            "copie vers $HOME non demandée." % resolved)
        return kit
    dest = Path.home() / "TRIADE_kits" / kit.name
    logger.info("kit2", "kit sur stockage partagé — copie vers %s" % dest)
    try:
        dest.mkdir(parents=True, exist_ok=True)
        n = 0
        for src in kit.rglob("*"):
            if src.is_file():
                target = dest / src.relative_to(kit)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(src), str(target))
                n += 1
        logger.ok("kit2", "copie terminée : %d fichiers -> %s" % (n, dest))
        return dest
    except Exception as e:
        logger.err("kit2", "copie impossible (%r) — run depuis l'emplacement d'origine" % e)
        return kit


# --------------------------------------------------------------------------
# Lancement de kit-2
# --------------------------------------------------------------------------

class Runner:
    def __init__(self, app):
        self.app = app
        self.lock = threading.Lock()
        self.state = {"state": "idle", "dir": None, "cmd": None, "exit": None,
                      "started": None, "ended": None, "duration": None,
                      "pid": None, "timeout": False, "error": None}

    def start(self, kit_dir, cmd, timeout, copy_home, auto_send):
        with self.lock:
            if self.state.get("state") == "running":
                return False, "un run est déjà en cours"
            self.state = {"state": "running", "dir": str(kit_dir), "cmd": cmd,
                          "exit": None, "started": now_iso(), "ended": None,
                          "duration": None, "pid": None, "timeout": False, "error": None}
        threading.Thread(target=self._work, args=(kit_dir, cmd, timeout, copy_home, auto_send),
                         daemon=True).start()
        return True, None

    def _work(self, kit_dir, cmd, timeout, copy_home, auto_send):
        lg = self.app.logger
        kit = Path(kit_dir)
        lg.section("LANCER KIT-2")
        lg.info("kit2", "kit : %s" % kit)
        lg.info("kit2", "commande demandée : %s" % cmd)
        lg.info("kit2", "timeout : %ss | copie $HOME : %s | auto-envoi : %s"
                % (timeout, copy_home, auto_send))

        eff = ensure_runnable_location(lg, kit, copy_home)
        if eff != kit:
            lg.info("kit2", "exécution depuis la copie : %s" % eff)
        pre_run_diag(lg, eff, cmd)

        lg.info("kit2", "DEBUT — %s (cwd=%s)" % (cmd, eff))
        t0 = time.time()
        try:
            proc = subprocess.Popen(
                cmd, shell=True, cwd=str(eff),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        except Exception as e:
            lg.err("kit2", "impossible de lancer : %r" % e)
            with self.lock:
                self.state.update(state="done", exit=None, error=str(e),
                                  ended=now_iso(), duration=round(time.time() - t0, 1))
            return

        with self.lock:
            self.state["pid"] = proc.pid
        lg.info("kit2", "PID %d — fusion stdout+stderr ci-dessous" % proc.pid)

        nlines = [0]

        def pump():
            try:
                for raw in iter(proc.stdout.readline, b""):
                    if nlines[0] >= 20000:
                        if nlines[0] == 20000:
                            lg.warn("kit2", "sortie tronquée à 20000 lignes")
                            nlines[0] += 1
                        continue
                    nlines[0] += 1
                    lg.out(raw.decode("utf-8", "replace").rstrip("\r\n"))
            except Exception as e:
                lg.err("kit2", "lecteur de sortie : %r" % e)

        reader = threading.Thread(target=pump, daemon=True)
        reader.start()

        timed_out = False
        try:
            rc = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            lg.err("kit2", "TIMEOUT après %ss — SIGKILL au groupe" % timeout)
            try:
                os.killpg(os.getpgid(proc.pid), 9)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
            rc = proc.wait()
        reader.join(timeout=5)
        duration = round(time.time() - t0, 1)

        lg.section("FIN KIT-2")
        verdict = "OK" if rc == 0 else "ECHEC"
        if timed_out:
            verdict = "TIMEOUT"
        lg.info("kit2", "code retour : %s (%s) | durée : %ss | lignes : %d"
                % (rc, verdict, duration, nlines[0]))
        if rc != 0:
            lg.err("kit2", ">>> kit-2 n'a pas terminé correctement. Le journal ci-dessus "
                            "est exactement ce qu'il faut envoyer via le bouton Drive. <<<")

        with self.lock:
            self.state.update(state="done", exit=rc, timeout=timed_out,
                              ended=now_iso(), duration=duration)

        if auto_send:
            lg.info("gui", "auto-envoi après run — lancement de l'envoi Drive")
            self.app.drive.send()


# --------------------------------------------------------------------------
# Envoi des logs vers le Drive (/test) — 3 stratégies
# --------------------------------------------------------------------------

class DriveSender:
    def __init__(self, app):
        self.app = app
        self.lock = threading.Lock()
        self.state = {"state": "idle", "mode": None, "detail": None, "zip": None}
        self.zips = []

    def send(self):
        with self.lock:
            if self.state.get("state") == "sending":
                return False
            self.state.update(state="sending", mode=None, detail=None, zip=None)
        threading.Thread(target=self._work, daemon=True).start()
        return True

    def _work(self):
        lg = self.app.logger
        conf = self.app.conf
        lg.section("ENVOI DRIVE (logs vers /test)")
        lg.info("drive", "dossier log : %s (%d fichiers)"
                % (LOG_DIR, len(list(LOG_DIR.glob('*.log')))))

        # --- Stratégie 1 : rclone -----------------------------------------
        rclone = which("rclone")
        if rclone:
            lg.info("drive", "rclone détecté : %s" % rclone)
            rc, out = sh([rclone, "listremotes"], 12)
            remotes = [l.strip().rstrip(":") for l in out.splitlines() if l.strip()] \
                if rc == 0 and out else []
            lg.info("drive", "remotes configurés : %s" % (remotes or "aucun"))
            target = None
            if remotes:
                pref = conf["drive_remote"]
                target = pref if pref in remotes else remotes[0]
            if target:
                dest = conf["drive_dest"]
                lg.info("drive", "rclone copy %s -> %s:%s" % (LOG_DIR, target, dest))
                rc, out = sh([rclone, "copy", str(LOG_DIR), "%s:%s" % (target, dest),
                              "-v", "--create-empty-src-dirs"], timeout=600)
                lg.block("INFO", "drive", out)
                if rc == 0:
                    lg.ok("drive", "ENVOI AUTOMATIQUE OK (rclone) -> %s:%s" % (target, dest))
                    with self.lock:
                        self.state.update(state="done", mode="rclone",
                                          detail="%s:%s" % (target, dest))
                    return
                lg.err("drive", "rclone a échoué (rc=%s) — stratégie suivante" % rc)
            else:
                lg.warn("drive", "rclone présent mais aucun remote — configurer : rclone config")
        else:
            lg.info("drive", "rclone absent — stratégie suivante")

        # --- Stratégie 2 : compte de service (drive_sa.json + folder_id) ---
        sa = SCRIPT_DIR / conf["drive_sa_file"]
        fid = (conf["drive_folder_id"] or "").strip()
        if sa.exists() and fid and not fid.startswith("("):
            lg.info("drive", "compte de service : %s | dossier : %s" % (sa.name, fid))
            ok, detail = self._sa_upload(sa, fid)
            if ok:
                lg.ok("drive", "ENVOI AUTOMATIQUE OK (API Drive) — %s" % detail)
                with self.lock:
                    self.state.update(state="done", mode="sa", detail=detail)
                return
            lg.err("drive", "envoi par compte de service échoué — repli manuel")
        else:
            lg.info("drive", "pas de couple drive_sa.json + folder_id — repli manuel")

        # --- Stratégie 3 : manuel assisté ---------------------------------
        zpath = self._make_zip()
        lg.warn("drive", "MODE MANUEL ASSISTE — aucune méthode automatique disponible.")
        lg.info("drive", "paquet prêt : %s" % zpath)
        lg.info("drive", "ouvrir le Drive (%s) puis déposer le .zip dans /test"
                % conf["drive_folder_url"])
        with self.lock:
            self.state.update(state="done", mode="manual", zip=str(zpath))

    def _make_zip(self):
        lg = self.app.logger
        ts = time.strftime("%Y%m%d_%H%M%S")
        host = (socket.gethostname() or "phone").split(".")[0][:16]
        zpath = SCRIPT_DIR / ("TRIADE_logs_gui_%s_%s.zip" % (host, ts))
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(LOG_DIR.glob("*.log")):
                zf.write(str(f), arcname=f.name)
            if CONF_PATH.exists():
                zf.write(str(CONF_PATH), arcname="triade_gui.conf")
        self.zips.append(zpath)
        # copie de commodité vers le stockage partagé (partage Android plus simple)
        try:
            dl = Path.home() / "storage" / "downloads"
            if dl.exists():
                shutil.copy2(str(zpath), str(dl / zpath.name))
                lg.info("drive", "copie du zip aussi disponible dans %s" % dl)
        except Exception:
            pass
        return zpath

    def _sa_upload(self, sa_path, folder_id):
        lg = self.app.logger
        try:
            sa = json.loads(sa_path.read_text(encoding="utf-8"))
        except Exception as e:
            lg.err("drive", "drive_sa.json illisible : %r" % e)
            return False, "sa illisible"
        if not which("openssl"):
            lg.err("drive", "openssl absent — signature JWT impossible")
            return False, "openssl absent"

        def b64u(b):
            return base64.urlsafe_b64encode(b).rstrip(b"=").decode()

        now = int(time.time())
        header = {"alg": "RS256", "typ": "JWT", "kid": sa.get("private_key_id", "")}
        claims = {"iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/drive",
                  "aud": "https://oauth2.googleapis.com/token", "iat": now, "exp": now + 3500}
        si = (b64u(json.dumps(header, separators=(",", ":")).encode())
              + "." + b64u(json.dumps(claims, separators=(",", ":")).encode())).encode()

        keytmp = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".pem", delete=False) as kf:
                kf.write(sa["private_key"].encode())
                keytmp = kf.name
            p = subprocess.run(["openssl", "dgst", "-sha256", "-sign", keytmp],
                               input=si, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if p.returncode != 0:
                lg.err("drive", "signature JWT échouée : %s"
                       % p.stderr.decode("utf-8", "replace").strip()[:200])
                return False, "signature JWT"
            jwt = si + b"." + b64u(p.stdout).encode()
            data = urllib.parse.urlencode({
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": jwt.decode(),
            }).encode()
            req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data,
                                         headers={"Content-Type": "application/x-www-form-urlencoded"})
            tok = json.loads(urllib.request.urlopen(req, timeout=30).read())["access_token"]
            lg.ok("drive", "jeton service account obtenu")

            sent, failed = [], []
            for f in sorted(LOG_DIR.glob("*.log")):
                boundary = "triiade%s" % os.urandom(8).hex()
                meta = json.dumps({"name": f.name, "parents": [folder_id]})
                body = (("--%s\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n%s\r\n"
                         % (boundary, meta)
                         + "--%s\r\nContent-Type: text/plain\r\n\r\n" % boundary).encode()
                        + f.read_bytes()
                        + ("\r\n--%s--\r\n" % boundary).encode())
                rq = urllib.request.Request(
                    "https://www.googleapis.com/upload/drive/v3/files"
                    "?uploadType=multipart&supportsAllDrives=true",
                    data=body,
                    headers={"Authorization": "Bearer " + tok,
                             "Content-Type": "multipart/related; boundary=%s" % boundary})
                try:
                    urllib.request.urlopen(rq, timeout=60).read()
                    sent.append(f.name)
                    lg.ok("drive", "envoyé : %s" % f.name)
                except Exception as e:
                    failed.append(f.name)
                    lg.err("drive", "échec %s : %r" % (f.name, e))
            if sent and not failed:
                return True, "%d fichiers -> dossier %s" % (len(sent), folder_id)
            return False, "%d envoyés, %d échecs" % (len(sent), len(failed))
        except Exception as e:
            lg.err("drive", "SA upload : %r" % e)
            return False, "exception"
        finally:
            if keytmp:
                try:
                    os.unlink(keytmp)
                except Exception:
                    pass

    def share(self, zpath_str):
        lg = self.app.logger
        lg.section("PARTAGE ANDROID")
        ts = which("termux-share")
        zpath = Path(zpath_str)
        if not zpath.exists():
            lg.err("partage", "fichier introuvable : %s" % zpath)
            return False, "introuvable"
        if ts:
            cmd = [ts, "-a", "send", str(zpath)]
        elif which("am"):
            cmd = ["am", "start", "-a", "android.intent.action.SEND", "-t", "application/zip",
                   "--eu", "android.intent.extra.STREAM", "file://" + str(zpath)]
        else:
            lg.warn("partage", "ni termux-share ni am disponible — utiliser l'application "
                               "Fichiers du téléphone, ou le lien de téléchargement.")
            return False, "aucun mécanisme"
        rc, out = sh(cmd, 40)
        lg.block("INFO", "partage", out)
        lg.info("partage", "rc=%s cmd=%s" % (rc, " ".join(cmd[:2])))
        return rc == 0, out


# --------------------------------------------------------------------------
# Application (état partagé)
# --------------------------------------------------------------------------

class App:
    def __init__(self, conf, logger):
        self.conf = conf
        self.logger = logger
        self.runner = Runner(self)
        self.drive = DriveSender(self)
        self.kits = []
        self.url = ""
        self.started = now_iso()

    def rescan(self):
        self.kits = scan_kits(self.logger)
        lg = self.logger
        if self.kits:
            lg.info("scan", "%d kit(s) détecté(s) :" % len(self.kits))
            for k in self.kits:
                lg.info("scan", "  - %s (%s) cmd par défaut : %s"
                        % (k["name"], k["path"], k["default_cmd"]))
        else:
            lg.warn("scan", "aucun kit détecté — placer le kit près du script, ou "
                            "renseigner kit2.dir dans triade_gui.conf")
        return self.kits

    def state_json(self):
        return {
            "version": VERSION,
            "now": now_iso(),
            "started": self.started,
            "session_log": str(self.logger.path),
            "log_dir": str(LOG_DIR),
            "tail": "\n".join(self.logger.snapshot()),
            "kits": self.kits,
            "conf": {
                "run_timeout": self.conf["run_timeout"],
                "auto_send_after_run": self.conf["auto_send_after_run"],
                "copy_to_home_on_sdcard": self.conf["copy_to_home_on_sdcard"],
                "kit2_dir": self.conf["kit2_dir"],
                "kit2_cmd": self.conf["kit2_cmd"],
                "drive_remote": self.conf["drive_remote"],
                "drive_dest": self.conf["drive_dest"],
                "drive_folder_url": self.conf["drive_folder_url"],
            },
            "run": dict(self.runner.state),
            "drive": dict(self.drive.state),
            "server": {"url": self.url},
        }


# --------------------------------------------------------------------------
# Serveur HTTP + interface
# --------------------------------------------------------------------------

HTML_PAGE = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TRIADE — console kit-2</title>
<style>
:root{--bg:#0d1117;--card:#161b22;--line:#30363d;--txt:#c9d1d9;--dim:#8b949e;
--ok:#3fb950;--err:#f85149;--blue:#58a6ff;--green:#2ea043}
*{box-sizing:border-box}
body{margin:0;font:15px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
background:var(--bg);color:var(--txt)}
header{padding:14px 16px;border-bottom:1px solid var(--line)}
h1{font-size:18px;margin:0}
.sub{color:var(--dim);font-size:12px;margin-top:3px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.chip{font:11px/1.2 ui-monospace,monospace;color:var(--dim);border:1px solid var(--line);
border-radius:999px;padding:5px 10px;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.chip b{color:var(--txt)}
main{padding:14px;display:flex;flex-direction:column;gap:14px;max-width:760px;margin:0 auto;padding-bottom:70px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.card h2{font-size:13px;margin:0 0 10px;letter-spacing:.6px;text-transform:uppercase;color:var(--dim)}
label{display:block;font-size:12px;color:var(--dim);margin:10px 0 4px}
select,input{width:100%;font:13px/1.3 ui-monospace,monospace;background:#0b0f14;color:var(--txt);
border:1px solid var(--line);border-radius:8px;padding:10px}
.row{display:flex;gap:10px}.row>div{flex:1}
.chk{display:flex;align-items:center;gap:8px;margin:10px 0;font-size:13px}
.chk input{width:auto}
button.big{width:100%;margin-top:12px;padding:16px;font-size:17px;font-weight:700;
letter-spacing:.5px;border:0;border-radius:10px;color:#fff;cursor:pointer}
#btn-launch{background:var(--green)} #btn-launch:disabled{opacity:.45}
#btn-drive{background:#1f6feb} #btn-drive:disabled{opacity:.45}
button.sec{margin-top:8px;width:100%;padding:12px;font-size:14px;font-weight:600;
border:1px solid var(--line);border-radius:10px;background:#21262d;color:var(--txt);cursor:pointer;display:block;text-align:center}
.banner{margin-top:12px;padding:10px 12px;border-radius:8px;font-size:13px;display:none}
.banner.ok{display:block;background:#12261e;border:1px solid #1f4d33;color:var(--ok)}
.banner.err{display:block;background:#2d1517;border:1px solid #6e2a2e;color:var(--err)}
#console{margin-top:10px;background:#05070a;border:1px solid var(--line);border-radius:8px;
padding:10px;height:42vh;overflow:auto;font:12px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;
white-space:pre;color:#e6edf3}
a{color:var(--blue);text-decoration:none}
.muted{color:var(--dim);font-size:12px}
details{margin-top:8px}summary{cursor:pointer;color:var(--blue);font-size:13px}
.help{font-size:13px}
.help code{font:12px ui-monospace,monospace;background:#0b0f14;border:1px solid var(--line);
border-radius:4px;padding:1px 5px;word-break:break-all}
.led{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;background:var(--dim)}
.led.run{background:#d29922;animation:p 1s infinite alternate}
.led.ok{background:var(--ok)}.led.err{background:var(--err)}
@keyframes p{from{opacity:.35}to{opacity:1}}
code.zipname{font:12px ui-monospace,monospace;word-break:break-all;color:var(--txt);
background:#0b0f14;border:1px solid var(--line);border-radius:4px;padding:1px 5px}
</style></head><body>
<header>
 <h1>TRIADE — console kit-2 (dudect)</h1>
 <div class="sub">GUI autonome · journalisation dès le lancement · kits terrain v0.15.0</div>
 <div class="chips">
  <span class="chip" id="c-log">log: —</span>
  <span class="chip" id="c-run"><span class="led" id="led-run"></span>état: —</span>
  <span class="chip" id="c-exit">exit: —</span>
  <span class="chip" id="c-url">—</span>
 </div>
</header>
<main>
 <section class="card">
  <h2>1 · Lancer kit-2</h2>
  <label>Kit détecté (chemin le plus récent d'abord)</label>
  <select id="kit"></select>
  <label>Commande suggérée par le kit</label>
  <select id="cand"></select>
  <label>Commande à exécuter (modifiable librement)</label>
  <input id="cmd" placeholder="bash run.sh">
  <div class="row">
   <div><label>Timeout (s)</label><input id="to" type="number" value="600" min="10" max="3600"></div>
   <div><label>Options</label>
    <div class="chk" style="margin:0"><input type="checkbox" id="copyhome" checked><span>copier vers $HOME si SDCard</span></div>
    <div class="chk" style="margin:0"><input type="checkbox" id="autosend"><span>auto-envoi Drive après le run</span></div>
   </div>
  </div>
  <button class="big" id="btn-launch">LANCER KIT-2</button>
  <div class="banner" id="run-banner"></div>
 </section>
 <section class="card">
  <h2>2 · Console — journal en direct (dès le lancement du GUI)</h2>
  <div id="console">…</div>
  <div class="muted" style="margin-top:8px">
   <a href="/api/logfile">télécharger le log de session</a> · rafraîchissement 1,2 s
  </div>
 </section>
 <section class="card">
  <h2>3 · Envoyer les logs vers le Drive (/test)</h2>
  <div class="muted" id="drive-dest">destination : Drive TRIADE → /test/TRIADE_logs_gui</div>
  <button class="big" id="btn-drive">ENVOYER LES LOGS AU DRIVE</button>
  <div class="banner" id="drive-banner"></div>
  <div id="manual" style="display:none;margin-top:10px;font-size:13px">
   Paquet prêt : <span class="zipname" id="zipname"></span>
   <a class="sec" id="zipdl" href="#">télécharger le .zip</a>
   <button class="sec" id="btn-open">OUVRIR LE DOSSIER DU DRIVE (dépôt dans /test)</button>
   <button class="sec" id="btn-share">PARTAGER VIA ANDROID</button>
   <div class="muted" style="margin-top:8px">
    Glisser le .zip dans /test du Drive, puis prévenir l'agent :
    il relèvera les logs depuis le Drive pour analyser le crash.
   </div>
  </div>
 </section>
 <section class="card">
  <h2>4 · Aide / installation</h2>
  <details class="help"><summary>Installation sur le téléphone (Termux)</summary>
   <div style="margin-top:8px">
    1. <code>pkg install python</code><br>
    2. (optionnel, pour lire la SDCard) <code>termux-setup-storage</code><br>
    3. <code>python triade_gui.py</code><br>
    4. ouvrir l'URL affichée (le GUI tente de l'ouvrir seul).
    Fonctionne aussi sur PC/Linux et sous Pydroid.
   </div></details>
  <details class="help"><summary>Envoi 100% automatique (rclone ou compte de service)</summary>
   <div style="margin-top:8px">
    • rclone : <code>pkg install rclone</code> puis <code>rclone config</code>
    (remote <code>triade</code>, type <code>drive</code>, coller l'URL du dossier
    partagé). Le bouton envoie alors vers <code>triade:test/TRIADE_logs_gui</code>.<br>
    • Compte de service : déposer <code>drive_sa.json</code> à côté du script et
    renseigner <code>folder_id</code> dans <code>triade_gui.conf</code> (l'ID est
    dans l'URL de /test ouvert dans le navigateur).<br>
    • Sinon : repli manuel assisté (zip + lien + partage Android).
   </div></details>
  <details class="help"><summary>Ce que le GUI journalise</summary>
   <div style="margin-top:8px">
    Environnement au lancement (arch, Android, SELinux, toolchain), montage
    noexec, architecture ELF des binaires du kit, fins de ligne CRLF,
    stdout+stderr horodatés ligne à ligne, code retour et durée du run,
    chaque clic et chaque envoi. Tout atterrit dans <code>TRIADE_logs/</code>.
   </div></details>
 </section>
</main>
<script>
"use strict";
function $(id){return document.getElementById(id)}
var stick=true, lastState=null, lastKitJson="";
$("console").addEventListener("scroll",function(){
  var c=$("console");stick=c.scrollTop+c.clientHeight>=c.scrollHeight-40;});

function poll(){
  fetch("/api/state").then(function(r){return r.json()})
    .then(function(s){render(s)})
    .catch(function(){});
}

function render(s){
  lastState=s;
  $("c-log").textContent="log: "+String(s.session_log||"—").split("/").pop();
  $("c-exit").textContent="exit: "+((s.run&&s.run.exit===null||s.run.exit===undefined)?"—":s.run.exit);
  var rs=(s.run&&s.run.state)||"idle";
  var ledClass=rs==="running"?"run":(s.run.exit===0?"ok":(s.run.exit?"err":""));
  $("c-run").innerHTML='<span class="led '+ledClass+'"></span>état: '+rs;
  $("c-url").textContent=(s.server&&s.server.url)||"";
  var kj=JSON.stringify(s.kits||[]);
  if(kj!==lastKitJson){
    lastKitJson=kj;
    var sel=$("kit");sel.innerHTML="";
    (s.kits||[]).forEach(function(k){
      var o=document.createElement("option");
      o.value=k.path;o.textContent=k.name+" — "+k.path;sel.appendChild(o);});
    if(!(s.kits||[]).length){
      var o=document.createElement("option");
      o.value=(s.conf&&s.conf.kit2_dir)||"";
      o.textContent="aucun kit détecté"+(o.value?" — conf: "+o.value:" (déposer le kit près du script)");
      sel.appendChild(o);}
    onKitChange(true);
  }
  var c=$("console");c.textContent=s.tail||"(journal en attente…)";
  if(stick){c.scrollTop=c.scrollHeight;}
  $("btn-launch").disabled=(rs==="running");
  $("btn-drive").disabled=(s.drive&&s.drive.state==="sending");

  var rb=$("run-banner");
  if(rs==="done"&&s.run.exit!==null&&s.run.exit!==undefined){
    rb.style.display="block";
    if(s.run.exit===0){rb.className="banner ok";
      rb.textContent="RUN TERMINÉ (code 0) — logs prêts pour l'envoi.";}
    else{rb.className="banner err";
      rb.textContent="ÉCHEC DU RUN (code "+s.run.exit+(s.run.timeout?", TIMEOUT":"")+
        ") — détail dans la console ; envoyer les logs pour analyse.";}
  }else if(rs==="running"){rb.style.display="none";}

  var db=$("drive-banner"),man=$("manual");
  var ds=(s.drive&&s.drive.state)||"idle";
  if(ds==="done"){
    db.style.display="block";
    if(s.drive.mode==="rclone"||s.drive.mode==="sa"){
      db.className="banner ok";
      db.textContent="ENVOI AUTOMATIQUE OK ("+s.drive.mode+") → "+(s.drive.detail||"");
      man.style.display="none";
    }else{
      db.className="banner err";
      db.textContent="Mode manuel assisté : aucune méthode automatique configurée (voir aide).";
      man.style.display="block";
      if(s.drive.zip){
        $("zipname").textContent=String(s.drive.zip).split("/").pop();
        $("zipdl").href="/api/file?path="+encodeURIComponent(s.drive.zip);}
    }
  }else if(ds==="sending"){
    db.style.display="block";db.className="banner err";
    db.textContent="envoi en cours…";man.style.display="none";
  }else{db.style.display="none";man.style.display="none";}
  $("drive-dest").textContent="destination : Drive TRIADE → "+
    ((s.conf&&s.conf.drive_dest)||"test/TRIADE_logs_gui");
}

function onKitChange(force){
  var path=$("kit").value;
  fetch("/api/state").then(function(r){return r.json()}).then(function(s){
    var k=null;(s.kits||[]).forEach(function(x){if(x.path===path)k=x;});
    var cand=$("cand");cand.innerHTML="";
    if(k&&k.candidates&&k.candidates.length){
      k.candidates.forEach(function(cc){
        var o=document.createElement("option");
        o.value=cc.cmd;o.textContent=cc.label+" → "+cc.cmd;cand.appendChild(o);});
      $("cmd").value=k.default_cmd||k.candidates[0].cmd||"";
    }else{
      $("cmd").value=(s.conf&&s.conf.kit2_cmd)||"";
      var o=document.createElement("option");
      o.value="";o.textContent="—";cand.appendChild(o);}
  }).catch(function(){});
}

$("kit").addEventListener("change",function(){onKitChange();});
$("cand").addEventListener("change",function(){if(this.value){$("cmd").value=this.value;}});

$("btn-launch").addEventListener("click",function(){
  fetch("/api/launch",{method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      dir:$("kit").value||"",
      cmd:$("cmd").value||"",
      timeout:parseInt($("to").value,10)||600,
      copy_home:$("copyhome").checked,
      auto_send:$("autosend").checked})})
  .then(function(r){return r.json()})
  .then(function(j){
    if(!j.ok){var rb=$("run-banner");rb.style.display="block";
      rb.className="banner err";rb.textContent=j.error||"refusé";}
  }).catch(function(){});
});

$("btn-drive").addEventListener("click",function(){
  fetch("/api/drive",{method:"POST"})
    .then(function(r){return r.json()})
    .then(function(j){
      if(!j.ok){var db=$("drive-banner");db.style.display="block";
        db.className="banner err";db.textContent=j.error||"refusé";}}).catch(function(){});
});

$("btn-share").addEventListener("click",function(){
  var z=(lastState&&lastState.drive&&lastState.drive.zip)||"";
  fetch("/api/share",{method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({path:z})})
  .then(function(r){return r.json()}).catch(function(){});
});

$("btn-open").addEventListener("click",function(){
  var u=(lastState&&lastState.conf&&lastState.conf.drive_folder_url)||
        "https://drive.google.com/drive/folders/105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp";
  window.open(u,"_blank");
});

setInterval(poll,1200);poll();
</script></body></html>
"""


class Handler(BaseHTTPRequestHandler):
    server_version = "TRIADEgui/" + VERSION
    app = None  # injecté avant démarrage

    # --- helpers -------------------------------------------------------
    def _json(self, status, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _bytes(self, status, data, ctype, fname=None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        if fname:
            self.send_header("Content-Disposition",
                             "attachment; filename=%s" % urllib.parse.quote(fname))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _body_json(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(n) if n else b"{}"
            return json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            return {}

    def log_message(self, fmt, *args):
        try:
            line = fmt % args
            if "/api/state" in line:  # polling : pas de journal pour éviter le bruit
                return
            self.app.logger.write("INFO", "http", line)
        except Exception:
            pass

    # --- GET ----------------------------------------------------------
    def do_GET(self):
        try:
            app = self.app
            path = urllib.parse.urlparse(self.path).path
            if path == "/":
                self._bytes(200, HTML_PAGE.encode("utf-8"), "text/html; charset=utf-8")
            elif path == "/api/state":
                self._json(200, app.state_json())
            elif path == "/api/logfile":
                data = app.logger.path.read_bytes()
                self._bytes(200, data, "text/plain; charset=utf-8",
                            fname=app.logger.path.name)
            elif path == "/api/file":
                q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                p = (q.get("path") or [""])[0]
                hit = next((z for z in app.drive.zips if str(z) == p), None)
                if hit:
                    self._bytes(200, hit.read_bytes(), "application/zip", fname=hit.name)
                else:
                    self._json(404, {"ok": False, "error": "zip inconnu"})
            else:
                self._json(404, {"ok": False, "error": "route inconnue"})
        except Exception as e:
            self.app.logger.err("http", "GET %s : %r" % (self.path, e))
            try:
                self._json(500, {"ok": False, "error": str(e)})
            except Exception:
                pass

    # --- POST ---------------------------------------------------------
    def do_POST(self):
        try:
            app = self.app
            path = urllib.parse.urlparse(self.path).path
            app.logger.info("http", "POST %s" % path)
            if path == "/api/launch":
                body = self._body_json()
                d = str(body.get("dir") or "").strip()
                cmd = str(body.get("cmd") or "").strip()
                timeout = max(10, min(3600, int(body.get("timeout") or 600)))
                copy_home = bool(body.get("copy_home", True))
                auto_send = bool(body.get("auto_send", False))
                if not d:
                    self._json(400, {"ok": False, "error": "aucun kit sélectionné"})
                    return
                if not Path(d).exists():
                    self._json(400, {"ok": False, "error": "dossier introuvable : %s" % d})
                    return
                if not cmd:
                    self._json(400, {"ok": False, "error": "commande vide"})
                    return
                ok, err = app.runner.start(Path(d), cmd, timeout, copy_home, auto_send)
                self._json(202 if ok else 409, {"ok": ok, "error": err})
            elif path == "/api/drive":
                ok = app.drive.send()
                self._json(202 if ok else 409,
                           {"ok": ok, "error": None if ok else "envoi déjà en cours"})
            elif path == "/api/share":
                body = self._body_json()
                p = str(body.get("path") or "")
                hit = next((z for z in app.drive.zips if str(z) == p), None)
                if not hit:
                    self._json(404, {"ok": False, "error": "zip inconnu"})
                    return
                ok, out = app.drive.share(str(hit))
                self._json(200, {"ok": ok, "output": out})
            elif path == "/api/scan":
                app.rescan()
                self._json(200, {"ok": True, "n": len(app.kits)})
            else:
                self._json(404, {"ok": False, "error": "route inconnue"})
        except Exception as e:
            self.app.logger.err("http", "POST %s : %s" % (self.path, traceback.format_exc()[-400:]))
            try:
                self._json(500, {"ok": False, "error": str(e)})
            except Exception:
                pass


# --------------------------------------------------------------------------
# Environnement au lancement
# --------------------------------------------------------------------------

def env_diag(logger):
    lg = logger
    lg.section("DIAGNOSTIC ENVIRONNEMENT (au lancement du GUI)")
    u = platform.uname()
    lg.info("env", "hôte : %s | système : %s %s | arch : %s (norm : %s)"
            % (u.node, u.system, u.release, u.machine, norm_machine(u.machine)))
    lg.info("env", "python : %s" % sys.version.split()[0])
    lg.info("env", "répertoire du GUI : %s" % SCRIPT_DIR)
    lg.info("env", "TERMUX_VERSION = %s" % os.environ.get("TERMUX_VERSION", "(absent)"))

    rc, out = sh(["uname", "-a"], 8)
    if rc == 0 and out:
        lg.info("env", "uname -a : %s" % out)
    if which("getprop"):
        for k in ("ro.product.manufacturer", "ro.product.model",
                  "ro.product.cpu.abi", "ro.build.version.release"):
            rc, out = sh(["getprop", k], 6)
            lg.info("env", "%s = %s" % (k, (out.strip() if rc == 0 else "") or "?"))
    if which("getenforce"):
        rc, out = sh(["getenforce"], 6)
        lg.info("env", "SELinux : %s" % (out.strip() if rc == 0 else "?"))

    lg.info("env", "PATH = %s" % os.environ.get("PATH", ""))
    for b in ("cc", "gcc", "clang", "make", "python3", "file",
              "openssl", "rclone", "termux-share", "am"):
        lg.info("env", "%-12s %s" % (b, which(b) or "absent"))
    for p in (Path.home() / "storage" / "downloads",
              Path("/sdcard/Download"), Path("/storage/emulated/0/Download")):
        lg.info("env", "stockage %-38s %s" % (str(p), "OK" if p.exists() else "absent"))


def open_browser(url, logger):
    try:
        opened = webbrowser.open(url)
        logger.info("gui", "navigateur : %s" % ("ouvert" if opened else "échec"))
        if not opened and which("am"):
            rc, out = sh(["am", "start", "-a", "android.intent.action.VIEW", "-d", url], 15)
            logger.info("gui", "am start VIEW : rc=%s" % rc)
    except Exception as e:
        logger.warn("gui", "ouverture navigateur impossible : %r" % e)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    port = int(DEFAULTS["port"])
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--port" and i + 1 < len(args):
            try:
                port = int(args[i + 1])
            except ValueError:
                pass
            i += 2
        else:
            i += 1

    logger = Logger(LOG_DIR)
    logger.section("DEMARRAGE %s v%s" % (APP_NAME, VERSION))
    logger.info("gui", "script : %s" % Path(__file__))

    conf = load_conf(logger)
    if not any(a.startswith("--port") for a in args):
        try:
            port = int(conf["port"])
        except ValueError:
            port = int(DEFAULTS["port"])

    app = App(conf, logger)
    env_diag(logger)
    app.rescan()

    Handler.app = app
    bind = conf["bind"] or "0.0.0.0"
    httpd = None
    for attempt in range(6):
        try:
            httpd = ThreadingHTTPServer((bind, port + attempt), Handler)
            port = port + attempt
            break
        except OSError:
            continue
    if httpd is None:
        logger.err("gui", "impossible de binder un port (%s..%s)" % (port, port + 5))
        print("[TRIADE GUI] impossible d'ouvrir un port — voir %s" % logger.path)
        sys.exit(1)
    httpd.daemon_threads = True

    ip = lan_ip()
    app.url = "http://%s:%d" % (ip, port)
    logger.ok("gui", "serveur prêt : %s  (local : http://127.0.0.1:%d)" % (app.url, port))
    logger.info("gui", "log de session : %s" % logger.path)
    logger.info("gui", "arrêt : Ctrl-C")

    print("=" * 66)
    print("  %s v%s" % (APP_NAME, VERSION))
    print("  URL      : %s   (et http://127.0.0.1:%d)" % (app.url, port))
    print("  LOG      : %s" % logger.path)
    print("  Kits     : %d détecté(s)" % len(app.kits))
    print("=" * 66)

    threading.Timer(1.2, open_browser, args=(app.url, logger)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("gui", "arrêt demandé (Ctrl-C)")
    finally:
        try:
            httpd.server_close()
        except Exception:
            pass
        logger.section("ARRET DU GUI")
        logger.info("gui", "session de log close : %s" % logger.path)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        tb = traceback.format_exc()
        try:
            lg = Logger(LOG_DIR)
            lg.err("gui", "FATAL\n" + tb)
        except Exception:
            pass
        print(tb)
        sys.exit(1)
