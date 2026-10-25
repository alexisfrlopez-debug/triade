#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie les jetons d'authentification du projet TRIADE (dossier .gdrive/).

Teste : 1) l'échange refresh_token -> access_token OAuth Google Drive,
        2) l'accès API au dossier Drive de sauvegarde,
        3) le jeton GitHub (compte, validité).

Règle d'or : ce script n'affiche JAMAIS la valeur d'un secret,
uniquement des masques (préfixe + longueur) et des statuts.
"""

import json
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

GDRIVE = pathlib.Path(__file__).resolve().parents[1] / ".gdrive"
FOLDER_ID = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"


def mask(s: str) -> str:
    """Masque un secret : préfixe court + longueur."""
    return (s[:6] + "…[" + str(len(s)) + " car]") if s else "(vide)"


def http(url, data=None, headers=None):
    """GET/POST minimaliste, renvoie (statut, corps)."""
    req = urllib.request.Request(url, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def drive_test():
    print("== OAuth Google Drive ==")
    chemin = GDRIVE / "oauth_token_relais.json"
    if not chemin.exists():
        print("ABSENT :", chemin)
        return None
    tok = json.loads(chemin.read_text())
    data = urllib.parse.urlencode({
        "client_id": tok["client_id"],
        "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    st, body = http(tok["token_uri"], data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"})
    print("échange refresh_token -> access_token :", st)
    if st != 200:
        print("  corps :", body[:300].decode(errors="replace"))
        return None
    obj = json.loads(body)
    at = obj.get("access_token", "")
    print("  access_token :", mask(at), "| expire dans", obj.get("expires_in"), "s")
    q = urllib.parse.quote(f"'{FOLDER_ID}' in parents and trashed = false")
    st, body = http(
        f"https://www.googleapis.com/drive/v3/files?q={q}&pageSize=100"
        f"&fields=files(id,name,mimeType)",
        headers={"Authorization": "Bearer " + at})
    print("  listing du dossier de sauvegarde :", st)
    if st == 200:
        for f in json.loads(body).get("files", []):
            print("   -", f["name"], "|", f["mimeType"], "|", f["id"])
    else:
        print("  corps :", body[:300].decode(errors="replace"))
    return at


def github_test():
    print("== GitHub ==")
    chemin = GDRIVE / "token_git.txt"
    if not chemin.exists():
        print("ABSENT :", chemin)
        return
    raw = chemin.read_text(errors="replace")
    m = re.search(r"(gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})", raw)
    if not m:
        print("  aucun jeton GitHub reconnaissable ; taille fichier :", len(raw), "octets")
        return
    tok = m.group(1)
    print("  jeton détecté :", mask(tok))
    st, body = http("https://api.github.com/user",
                    headers={"Authorization": "Bearer " + tok,
                             "Accept": "application/vnd.github+json",
                             "User-Agent": "triade-check"})
    print("  API /user :", st)
    if st == 200:
        print("  compte :", json.loads(body).get("login"))
    else:
        print("  corps :", body[:300].decode(errors="replace"))


if __name__ == "__main__":
    drive_test()
    github_test()
