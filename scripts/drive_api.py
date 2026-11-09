#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Outil Drive API v3 pour le projet TRIADE.

Jetons : .gdrive/oauth_token_relais.json (refresh token, scope drive complet).
SECURITE : aucun jeton n'est jamais affiché ni journalisé. Usage :
  drive_api.py token                      -> rafraîchit/cache l'access token
  drive_api.py list <folder_id>           -> liste un dossier (nom, id, mime)
  drive_api.py mkdir <nom> <parent_id>    -> crée un dossier
  drive_api.py upload <fichier> <parent_id> [--name NOM]   -> téléverse un fichier
  drive_api.py upload_dir <dossier> <parent_id>            -> téléverse une arborescence
  drive_api.py download <file_id> <sortie> -> télécharge un fichier
  drive_api.py delete <file_id>           -> met à la corbeille
  drive_api.py search <nom>               -> cherche par nom dans tout le Drive
"""
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

RACINE = "/home/z/my-project"
GDRIVE = os.path.join(RACINE, ".gdrive")
CACHE = os.path.join(GDRIVE, "access_cache.json")
RELAIS = os.path.join(GDRIVE, "oauth_token_relais.json")
API = "https://www.googleapis.com/drive/v3"
UPLOAD = "https://www.googleapis.com/upload/drive/v3"


def _log(*a):
    print(*a, file=sys.stderr)


def obtenir_token():
    """Retourne un access_token valide (cache ou rafraîchissement)."""
    now = time.time()
    if os.path.exists(CACHE):
        try:
            c = json.load(open(CACHE))
            if c.get("expire_a", 0) - now > 120:
                return c["access_token"]
        except Exception:
            pass
    creds = json.load(open(RELAIS))
    donnees = urllib.parse.urlencode({
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "refresh_token": creds["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(creds["token_uri"], data=donnees,
                                 method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        rep = json.load(r)
    at = rep["access_token"]
    json.dump({"access_token": at, "expire_a": now + rep.get("expires_in", 3600)},
              open(CACHE, "w"))
    os.chmod(CACHE, 0o600)
    return at


def _auth():
    return {"Authorization": f"Bearer {obtenir_token()}"}


def _get(url, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=_auth())
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def cmd_token():
    t = obtenir_token()
    print(f"access_token OK ({len(t)} caractères, expire ~1 h)")


def cmd_list(folder_id):
    rep = _get(f"{API}/files/", {
        "q": f"'{folder_id}' in parents and trashed = false",
        "fields": "files(id, name, mimeType, size, md5Checksum)",
        "pageSize": 200,
    })
    for f in rep.get("files", []):
        taille = f.get("size", "-")
        print(f"{f['name']}\t{f['id']}\t{f['mimeType']}\t{taille}")


def cmd_mkdir(nom, parent_id):
    corps = {"name": nom, "mimeType": "application/vnd.google-apps.folder",
             "parents": [parent_id]}
    req = urllib.request.Request(
        f"{API}/files/", data=json.dumps(corps).encode(),
        headers={**_auth(), "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        rep = json.load(r)
    print(f"{rep['id']}")


def _upload_fichier(chemin, parent_id, nom=None):
    nom = nom or os.path.basename(chemin)
    meta = {"name": nom, "parents": [parent_id]}
    limite = 5 * 1024 * 1024  # multipart jusqu'à 5 Mio, resumable au-delà
    taille = os.path.getsize(chemin)
    if taille <= limite:
        delim = "xxTRIADExx"
        corps = (f"--{delim}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n"
                 f"{json.dumps(meta)}\r\n--{delim}\r\nContent-Type: application/octet-stream\r\n\r\n"
                 ).encode() + open(chemin, "rb").read() + f"\r\n--{delim}--\r\n".encode()
        req = urllib.request.Request(
            f"{UPLOAD}/files?uploadType=multipart", data=corps, method="POST",
            headers={**_auth(), "Content-Type": f"multipart/related; boundary={delim}"})
        with urllib.request.urlopen(req, timeout=300) as r:
            rep = json.load(r)
    else:
        req = urllib.request.Request(
            f"{UPLOAD}/files?uploadType=resumable",
            data=json.dumps(meta).encode(), method="POST",
            headers={**_auth(), "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            session_uri = r.headers["Location"]
        avec = 0
        reste = taille
        while reste > 0:
            bloc = min(8 * 1024 * 1024, reste)
            deb = avec
            fin = avec + bloc - 1
            req = urllib.request.Request(
                session_uri, data=open(chemin, "rb").read()[deb:fin + 1], method="PUT",
                headers={**_auth(),
                         "Content-Range": f"bytes {deb}-{fin}/{taille}"})
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    rep = json.load(r)
            except urllib.error.HTTPError as e:
                if e.code == 308:
                    avec = int(e.headers.get("Range", "bytes=0-0").split("-")[-1]) + 1
                    reste = taille - avec
                    continue
                raise
            reste = 0
    return rep["id"], taille


def cmd_upload(chemin, parent_id, nom=None):
    fid, taille = _upload_fichier(chemin, parent_id, nom)
    print(f"OK {nom or os.path.basename(chemin)} : {fid} ({taille} o)")


def cmd_upload_dir(dossier, parent_id):
    """Téléverse une arborescence locale vers parent_id, en créant les sous-dossiers."""
    total = 0
    for racine, dirs, fichiers in os.walk(dossier):
        rel = os.path.relpath(racine, dossier)
        cible = parent_id
        if rel != ".":
            parties = rel.split(os.sep)
            # vérifie/chaque niveau
            for p in parties:
                rep = _get(f"{API}/files/", {
                    "q": f"'{cible}' in parents and name = '{p}' and "
                         f"mimeType = 'application/vnd.google-apps.folder' "
                         f"and trashed = false",
                    "fields": "files(id, name)", "pageSize": 5})
                fs = rep.get("files", [])
                if fs:
                    cible = fs[0]["id"]
                else:
                    req = urllib.request.Request(
                        f"{API}/files/",
                        data=json.dumps({"name": p, "parents": [cible],
                                         "mimeType": "application/vnd.google-apps.folder"}).encode(),
                        headers={**_auth(), "Content-Type": "application/json"},
                        method="POST")
                    with urllib.request.urlopen(req, timeout=60) as r:
                        cible = json.load(r)["id"]
                    _log(f"  dossier créé : {p}")
        for f in sorted(fichiers):
            chemin = os.path.join(racine, f)
            fid, taille = _upload_fichier(chemin, cible)
            print(f"OK {os.path.relpath(chemin, dossier)} : {fid} ({taille} o)")
            total += 1
    print(f"--- {total} fichiers téléversés ---")


def cmd_download(file_id, sortie):
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media",
        headers=_auth())
    with urllib.request.urlopen(req, timeout=300) as r:
        donnees = r.read()
    open(sortie, "wb").write(donnees)
    print(f"OK {sortie} ({len(donnees)} o)")


def cmd_delete(file_id):
    req = urllib.request.Request(f"{API}/files/{file_id}", headers=_auth(),
                                 method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            pass
        print(f"OK corbeille : {file_id}")
    except urllib.error.HTTPError as e:
        if e.code == 204:
            print(f"OK corbeille : {file_id}")
        else:
            raise


def cmd_search(nom):
    rep = _get(f"{API}/files/", {
        "q": f"name contains '{nom}' and trashed = false",
        "fields": "files(id, name, mimeType, parents)", "pageSize": 50})
    for f in rep.get("files", []):
        print(f"{f['name']}\t{f['id']}\t{f['mimeType']}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "token":
        cmd_token()
    elif cmd == "list":
        cmd_list(sys.argv[2])
    elif cmd == "mkdir":
        cmd_mkdir(sys.argv[2], sys.argv[3])
    elif cmd == "upload":
        nom = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "--name" else (
            sys.argv[5] if len(sys.argv) > 5 else None)
        cmd_upload(sys.argv[2], sys.argv[3], nom)
    elif cmd == "upload_dir":
        cmd_upload_dir(sys.argv[2], sys.argv[3])
    elif cmd == "download":
        cmd_download(sys.argv[2], sys.argv[3])
    elif cmd == "delete":
        cmd_delete(sys.argv[2])
    elif cmd == "search":
        cmd_search(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
