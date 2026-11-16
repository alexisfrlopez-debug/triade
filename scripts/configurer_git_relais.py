#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""configurer_git_relais.py — Regénère le fichier d'identifiants git depuis
tokens/token_git.txt (la procédure établie du projet : 600, JAMAIS affiché,
JAMAIS committé — le fichier vit dans /tmp, hors du dépôt), puis vérifie
l'accès au dépôt GitHub par ls-remote (les pointes affichées, rien d'autre).
"""
import os
import subprocess
import sys

JETON_GIT = "/home/z/my-project/tokens/token_git.txt"
CRED = "/tmp/git-credentials"
DEPOT = "https://github.com/alexisfrlopez-debug/triade.git"


def main():
    with open(JETON_GIT, encoding="utf-8-sig") as f:
        jeton = f.read().strip()
    if not jeton:
        print("[ROUGE] le jeton git est vide")
        return 1
    with open(CRED, "w", encoding="utf-8") as f:
        f.write(f"https://alexisfrlopez-debug:{jeton}@github.com\n")
    os.chmod(CRED, 0o600)
    print(f"[VERT] {CRED} régénéré (600, hors du dépôt, valeur jamais affichée)")
    r = subprocess.run(
        ["git", "-c", f"credential.helper=store --file={CRED}",
         "ls-remote", DEPOT],
        capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print(f"[ROUGE] ls-remote : {r.stderr.strip()[:300]}")
        return 1
    print("[VERT] ls-remote : le dépôt répond — les pointes :")
    for ligne in r.stdout.strip().splitlines()[:12]:
        print(f"  {ligne}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
