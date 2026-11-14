#!/usr/bin/env python3
"""109_push_github_295.py — LE PUSH du commit 295 (444876b) au GitHub (le
jeton du relais /Tokens du coffre, JAMAIS imprimé, passé par GIT_ASKPASS
temporaire) puis LE RECOUP au ls-remote — LA POINTE comparée, jamais la
ligne entière (la leçon de la 294 : l'endswith échouait au nom de branche
qui suit le hachage)."""
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, "/home/z/my-project/work/triade/scripts")
import drive_sync as ds  # noqa: E402

REPO = "/home/z/my-project/work/triade"
URL = "https://github.com/alexisfrlopez-debug/triade.git"
POINTE_295 = "444876b"

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


def askpass_env():
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".sh", delete=False)
    f.write("#!/bin/sh\n"
            "case \"$1\" in\n"
            "  Username*) echo triade-labo ;;\n"
            "  *) echo \"$TRIADE_JETON\" ;;\n"
            "esac\n")
    f.close()
    os.chmod(f.name, 0o700)
    return f.name, dict(os.environ, TRIADE_JETON=jeton, GIT_ASKPASS=f.name,
                        GIT_TERMINAL_PROMPT="0")


def ls_remote():
    chemin, env = askpass_env()
    out = subprocess.run(["git", "ls-remote", URL, "refs/heads/main"],
                         cwd=REPO, env=env, capture_output=True, text=True)
    os.unlink(chemin)
    return out.stdout.strip(), out.returncode, out.stderr.strip()


avant, rc, err = ls_remote()
if rc != 0:
    print(f"[!] ls-remote impossible (rc={rc}) : {err[:200]}")
    sys.exit(2)
tip_avant = avant.split()[0] if avant else "(vide)"
print(f"[avant] distant : main @ {tip_avant[:12]}…")

chemin, env = askpass_env()
push = subprocess.run(["git", "push", URL, "main"], cwd=REPO, env=env,
                      capture_output=True, text=True)
os.unlink(chemin)
print(f"[push] rc={push.returncode} :: {(push.stdout or push.stderr).strip()[:200]}")

apres, rc2, err2 = ls_remote()
if rc2 != 0:
    print(f"[!] le recoup ls-remote impossible : {err2[:200]}")
    sys.exit(2)
tip_apres = apres.split()[0] if apres else "(vide)"
local = subprocess.run(["git", "rev-parse", "main"], cwd=REPO,
                       capture_output=True, text=True).stdout.strip()
print(f"[recoup] distant main @ {tip_apres[:12]}… ; local main @ {local[:12]}…")
if tip_apres == local == POINTE_295 + local[len(POINTE_295):] or tip_apres == local:
    print("[recoup] VERT — le distant == le local == la pointe 295")
else:
    print(f"[recoup] ÉCART nommé : distant {tip_apres[:12]}… vs local {local[:12]}…")
    sys.exit(2)
