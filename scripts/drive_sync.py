#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Synchronisation Google Drive.

Pousse une copie miroir du projet vers le dossier Drive de sauvegarde :
  - sous-dossier TRIADE-sauvegarde-git/ : tous les fichiers suivis
    par git (miroir lisible — renommé D122 : ce n'est PAS un kit de
    cérémonie, c'est la sauvegarde automatique du dépôt) ;
  - TRIADE/triade-history.bundle : bundle git complet (historique restaurable) ;
  - racine du dossier Drive : les deux fichiers d'instruction
    (REPRISE_PROJET.md, PROTOCOLE_TRIADE_AGENT.md).

Propriétés :
  - idempotent : les fichiers identiques (MD5 égal) ne sont pas retéléversés ;
  - prudent : ne supprime jamais rien côté Drive ;
  - sûr : les secrets de .gdrive/ ne sont jamais synchronisés (décision D12) ;
  - autonome : stdlib uniquement, aucun paquet externe requis.

Utilisation : python3 scripts/drive_sync.py [--quiet]
Code de sortie : 0 = succès, 1 = erreurs partielles, 2 = erreur fatale.
"""

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

REPO = pathlib.Path(__file__).resolve().parents[1]
GDRIVE = REPO / ".gdrive"
TOKEN_FILE = GDRIVE / "oauth_token_relais.json"
STATE_FILE = GDRIVE / "state.json"

DRIVE_ROOT_ID = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"   # dossier Drive « Triade »
PROJECT_FOLDER = "TRIADE-sauvegarde-git"   # D122 : renommé pour que
                                          # le miroir ne se confonde
                                          # plus avec le kit de cérémonie
BUNDLE_NAME = "triade-history.bundle"
ROOT_PUSH = ["REPRISE_PROJET.md", "PROTOCOLE_TRIADE_AGENT.md"]
FOLDER_MIME = "application/vnd.google-apps.folder"
API = "https://www.googleapis.com/drive/v3"
UPLOAD = "https://www.googleapis.com/upload/drive/v3"


class SyncError(RuntimeError):
    pass


# ---------------------------------------------------------------- jeton OAuth

def _http_raw(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)


def get_access_token(force=False):
    """Obtient un access_token (cache local dans .gdrive/state.json)."""
    now = time.time()
    if not force and STATE_FILE.exists():
        try:
            st = json.loads(STATE_FILE.read_text())
            if st.get("expires_at", 0) > now + 60:
                return st["access_token"]
        except Exception:
            pass
    if not TOKEN_FILE.exists():
        raise SyncError(f"jeton OAuth absent : {TOKEN_FILE}")
    tok = json.loads(TOKEN_FILE.read_text())
    data = urllib.parse.urlencode({
        "client_id": tok["client_id"],
        "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    st, body, _ = _http_raw(tok["token_uri"], data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded"})
    if st != 200:
        raise SyncError(f"rafraîchissement OAuth échoué (HTTP {st}) : {body[:200]!r}")
    obj = json.loads(body)
    try:
        STATE_FILE.write_text(json.dumps(
            {"access_token": obj["access_token"],
             "expires_at": now + int(obj.get("expires_in", 3600))}))
    except Exception:
        pass
    return obj["access_token"]


# ---------------------------------------------------------------- appels API

def api(method, url, body=None, retry=True):
    headers = {"Authorization": "Bearer " + get_access_token()}
    data = None
    if body is not None:
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        if e.code == 401 and retry:
            get_access_token(force=True)
            return api(method, url, body, retry=False)
        detail = e.read()[:200]
        raise SyncError(
            f"appel API {method} {url[:80]}… échoué (HTTP {e.code}) : {detail!r}")


def list_folder(folder_id):
    """Liste un dossier Drive -> {nom: métadonnées} (pagination incluse)."""
    out = {}
    token = None
    while True:
        params = {"q": f"'{folder_id}' in parents and trashed = false",
                  "pageSize": "200",
                  "fields": "nextPageToken,files(id,name,mimeType,md5Checksum)"}
        if token:
            params["pageToken"] = token
        st, body, _ = api("GET", API + "/files?" + urllib.parse.urlencode(params))
        if st != 200:
            raise SyncError(f"listing impossible ({st}) : {body[:200]!r}")
        obj = json.loads(body)
        for f in obj.get("files", []):
            out[f["name"]] = f
        token = obj.get("nextPageToken")
        if not token:
            return out


def create_folder(parent_id, name):
    st, body, _ = api("POST", API + "/files",
                      body={"name": name, "mimeType": FOLDER_MIME,
                            "parents": [parent_id]})
    if st not in (200, 201):
        raise SyncError(f"création du dossier '{name}' impossible ({st})")
    return json.loads(body)["id"]


def ensure_folder(parent_id, name, cache):
    key = (parent_id, name)
    if key not in cache:
        entries = list_folder(parent_id)
        found = [f for f in entries.values()
                 if f["mimeType"] == FOLDER_MIME and f["name"] == name]
        cache[key] = found[0]["id"] if found else create_folder(parent_id, name)
    return cache[key]


# ---------------------------------------------------------------- téléversement

def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def resumable_upload(init_url, metadata, path, init_method="POST"):
    """Téléversement résumable en une requête (taille quelconque).

    init_method : POST pour créer un fichier, PATCH pour mettre à jour
    (exigé par l'API Drive pour les fichiers existants).
    """
    size = path.stat().st_size
    st, body, headers = api(init_method, init_url, body=metadata)
    if st not in (200, 201):
        raise SyncError(f"initialisation upload impossible ({st}) : {body[:200]!r}")
    session_uri = headers.get("Location")
    if not session_uri:
        raise SyncError("session de téléversement sans URL")
    with open(path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(session_uri, data=data, method="PUT",
                                 headers={"Content-Length": str(size)})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status
    except urllib.error.HTTPError as e:
        raise SyncError(f"téléversement échoué ({e.code}) : {e.read()[:200]!r}")


def upload_create(parent_id, name, path):
    return resumable_upload(UPLOAD + "/files?uploadType=resumable",
                            {"name": name, "parents": [parent_id]}, path)


def upload_update(file_id, path):
    return resumable_upload(f"{UPLOAD}/files/{file_id}?uploadType=resumable",
                            {}, path, init_method="PATCH")


# ---------------------------------------------------------------- fichiers locaux

def git_tracked_files():
    """Fichiers suivis par git -> {chemin_relatif: chemin_absolu}."""
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO,
                             capture_output=True, check=True)
    except subprocess.CalledProcessError:
        return {}
    files = {}
    for rel in out.stdout.decode(errors="replace").split("\0"):
        if not rel:
            continue
        p = REPO / rel
        if p.is_file():
            files[rel] = p
    return files


def build_bundle(tmpdir):
    """Régénère le bundle git complet ; None si aucun commit."""
    probe = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                           capture_output=True)
    if probe.returncode != 0:
        return None
    bundle = pathlib.Path(tmpdir) / BUNDLE_NAME
    out = subprocess.run(["git", "bundle", "create", str(bundle), "--all"],
                         cwd=REPO, capture_output=True)
    if out.returncode != 0 or not bundle.exists():
        return None
    return bundle


# ---------------------------------------------------------------- synchro

def sync(quiet=False):
    def log(msg):
        if not quiet:
            print(msg)

    files = git_tracked_files()
    errors = []

    with tempfile.TemporaryDirectory(prefix="triade_sync_") as tmp:
        bundle = build_bundle(tmp)
        if bundle:
            files[BUNDLE_NAME] = bundle
        else:
            log("[Drive] avertissement : aucun commit, bundle non généré")

        cache = {}
        triade_id = ensure_folder(DRIVE_ROOT_ID, PROJECT_FOLDER, cache)

        # carte distante récursive sous TRIADE/
        remote = {}

        def walk_remote(fid, prefix):
            for f in list_folder(fid).values():
                if f["mimeType"] == FOLDER_MIME:
                    walk_remote(f["id"], prefix + f["name"] + "/")
                else:
                    remote[prefix + f["name"]] = f

        walk_remote(triade_id, "")

        uploaded = updated = skipped = 0
        for rel in sorted(files):
            path = files[rel]
            md5 = md5_of(path)
            r = remote.get(rel)
            if r and r.get("md5Checksum") == md5:
                skipped += 1
                continue
            parts = pathlib.PurePosixPath(rel).parts[:-1]
            parent = triade_id
            for part in parts:
                parent = ensure_folder(parent, part, cache)
            try:
                if r:
                    upload_update(r["id"], path)
                    updated += 1
                    log(f"[Drive] mis à jour : {rel}")
                else:
                    upload_create(parent, pathlib.PurePosixPath(rel).name, path)
                    uploaded += 1
                    log(f"[Drive] téléversé : {rel}")
            except SyncError as e:
                errors.append(f"{rel} : {e}")
                print(f"[Drive] ERREUR {rel} : {e}", file=sys.stderr)

        # fichiers d'instruction à la racine du dossier Drive
        root_entries = list_folder(DRIVE_ROOT_ID)
        for name in ROOT_PUSH:
            path = REPO / name
            if not path.is_file():
                continue
            r = root_entries.get(name)
            if r and r.get("mimeType") != FOLDER_MIME \
                    and r.get("md5Checksum") == md5_of(path):
                continue
            try:
                if r and r.get("mimeType") != FOLDER_MIME:
                    upload_update(r["id"], path)
                    log(f"[Drive] mis à jour (racine) : {name}")
                else:
                    upload_create(DRIVE_ROOT_ID, name, path)
                    log(f"[Drive] téléversé (racine) : {name}")
            except SyncError as e:
                errors.append(f"{name} : {e}")
                print(f"[Drive] ERREUR {name} : {e}", file=sys.stderr)

        log(f"[Drive] bilan : {uploaded} téléversés, {updated} mis à jour, "
            f"{skipped} inchangés, {len(errors)} erreurs")
    return 1 if errors else 0


def main():
    ap = argparse.ArgumentParser(
        description="Synchronisation Google Drive du projet TRIADE")
    ap.add_argument("--quiet", action="store_true",
                    help="mode silencieux (utilisé par le hook post-commit)")
    args = ap.parse_args()
    try:
        sys.exit(sync(quiet=args.quiet))
    except SyncError as e:
        print(f"[Drive] ERREUR FATALE : {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
