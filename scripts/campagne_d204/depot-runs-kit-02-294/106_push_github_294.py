#!/usr/bin/env python3
"""106_push_github_294.py — LE PUSH du commit 294 (97bb116) au GitHub (le
jeton du relais /Tokens du coffre, JAMAIS imprimé, passé par GIT_ASKPASS
temporaire) puis LE RECOUP au ls-remote."""
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
import urllib.parse
import base64

sys.path.insert(0, "/home/z/my-project/work/triade/scripts")
import drive_sync as ds  # noqa: E402

REPO = "/home/z/my-project/work/triade"
URL = "https://github.com/alexisfrlopez-debug/triade.git"

coffre = ds.list_folder(ds.DRIVE_ROOT_ID)
tokens_dir = coffre.get("Tokens") or sys.exit("[!] /Tokens introuvable")
tg = ds.list_folder(tokens_dir["id"]).get("token_git.txt") or \
    sys.exit("[!] token_git.txt introuvable au relais")
st, corps, _ = ds.api("GET", ds.API + f"/files/{tg['id']}?alt=media")
corps = corps.decode("utf-8", errors="replace")
m = re.search(r"(ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9_]+)", corps)
if not m:
    print("[!] pas de jeton lisible au relais /Tokens")
    sys.exit(2)
jeton = m.group(1)
print(f"[OK] jeton du relais lu (préfixe {jeton[:4]}…, jamais imprimé)")


def ls_remote():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".sh", delete=False) as f:
        f.write("#!/bin/sh\n"
                "case \"$1\" in\n"
                "  Username*) echo triade-labo ;;\n"
                "  *) echo \"$TRIADE_JETON\" ;;\n"
                "esac\n")
        chemin = f.name
    os.chmod(chemin, 0o700)
    env = dict(os.environ, TRIADE_JETON=jeton, GIT_ASKPASS=chemin,
               GIT_TERMINAL_PROMPT="0")
    out = subprocess.run(["git", "ls-remote", URL, "refs/heads/main"],
                         cwd=REPO, env=env, capture_output=True, text=True)
    os.unlink(chemin)
    return out.stdout.strip(), out.returncode, out.stderr.strip()


avant, rc, err = ls_remote()
if rc != 0:
    print(f"[!] ls-remote impossible (rc={rc}) : {err[:200]}")
    sys.exit(2)
print(f"[avant] distant : {avant[:60]}")

with tempfile.NamedTemporaryFile(mode="w", suffix=".sh", delete=False) as f:
    f.write("#!/bin/sh\n"
            "case \"$1\" in\n"
            "  Username*) echo triade-labo ;;\n"
            "  *) echo \"$TRIADE_JETON\" ;;\n"
            "esac\n")
    chemin = f.name
os.chmod(chemin, 0o700)
env = dict(os.environ, TRIADE_JETON=jeton, GIT_ASKPASS=chemin,
           GIT_TERMINAL_PROMPT="0")
push = subprocess.run(["git", "push", URL, "main"], cwd=REPO, env=env,
                      capture_output=True, text=True)
os.unlink(chemin)
print(f"[push] rc={push.returncode}")
for ligne in (push.stdout + push.stderr).splitlines():
    if jeton not in ligne:
        print(f"       {ligne[:160]}")
if push.returncode != 0:
    print("[!] LE PUSH A ÉCHOUÉ — écart à nommer")
    sys.exit(1)

apres, rc, err = ls_remote()
print(f"[après] distant : {apres[:60]}")
local = subprocess.run(["git", "rev-parse", "main"], cwd=REPO,
                       capture_output=True, text=True).stdout.strip()
print(f"[local] main    : {local}")
distant = apres.split()[0] if apres else ""
if distant == local:
    print("[RECOUP] le distant == le local : LE PUSH DU COMMIT 294 (97bb116) A VÉCU")
else:
    print("[!] ÉCART : le distant ≠ le local")
    sys.exit(1)
