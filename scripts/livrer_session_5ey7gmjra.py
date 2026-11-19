#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_session_5ey7gmjra.py — LA LIVRAISON CHIRURGICALE de la session :
(1) les QUATRE rapports au /test du coffre (recoupés byte-byte au
re-téléchargement) ; (2) le pack TRIADE_presentation_v0.19.3_20261120.zip
à la RACINE du coffre (le motif des packs de présentation) ; (3)
l'instruction 5ey7gmjra ARCHIVÉE : /instructions → /ARCHIVE/
instructions_20261119/ (la règle du développeur : « archivées après
exécution ») — le geste Drive natif (add parent / remove parent), la
corbeille JAMAIS (D143)."""
import hashlib
import json
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

GDRIVE = pathlib.Path("/home/z/my-project/depot/.gdrive")
REPO = pathlib.Path("/home/z/my-project/depot")
ROOT_ID = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
API = "https://www.googleapis.com/drive/v3"


def access_token() -> str:
    tok = json.loads((GDRIVE / "oauth_token_relais.json").read_text())
    data = urllib.parse.urlencode({
        "client_id": tok["client_id"],
        "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"],
        "grant_type": "refresh_token"}).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token",
                                 data=data, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["access_token"]


def api(at, method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": f"Bearer {at}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)


def inventaire(at, fid):
    params = {"q": f"'{fid}' in parents and trashed = false",
              "fields": "nextPageToken, files(id, name, md5Checksum)",
              "pageSize": 200}
    out, token = {}, None
    while True:
        if token:
            params["pageToken"] = token
        st, body, _ = api(at, "GET",
                          f"{API}/files?{urllib.parse.urlencode(params)}")
        assert st == 200, (st, body[:200])
        j = json.loads(body)
        for f in j.get("files", []):
            out[f["name"]] = f
        token = j.get("nextPageToken")
        if not token:
            return out


def contenu(at, file_id):
    req = urllib.request.Request(f"{API}/files/{file_id}?alt=media",
                                 headers={"Authorization": f"Bearer {at}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def md5_de(p: pathlib.Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


at = access_token()
racine = inventaire(at, ROOT_ID)
test_id = racine["test"]["id"]
archive_id = racine["ARCHIVE"]["id"]
instructions_id = racine["instructions"]["id"]
test = inventaire(at, test_id)
archive = inventaire(at, archive_id)
instructions = inventaire(at, instructions_id)
bilan = []


def geste(nom, fn):
    try:
        detail = fn()
        bilan.append(("VERT", nom, detail))
        print(f"VERT  {nom} — {detail}")
    except Exception as e:  # noqa: BLE001
        bilan.append(("ROUGE", nom, str(e)[:200]))
        print(f"ROUGE {nom} — {str(e)[:200]}")


def resumable(at, init_url, metadata, chemin):
    size = chemin.stat().st_size
    st, body, headers = api(at, "PATCH" if "files/" in init_url else "POST",
                            init_url, body=metadata)
    assert st in (200, 201), (st, body[:200])
    session = headers.get("Location") or headers.get("location")
    req = urllib.request.Request(session, data=chemin.read_bytes(),
                                 method="PUT",
                                 headers={"Content-Length": str(size)})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())


# (1) les quatre rapports au /test — idempotents (md5 égal → rien)
PIECES_TEST = [
    ("rapport_verification_v0.19.3.txt",
     REPO / "scripts/vague7/rapport_verification_v0.19.3.txt"),
    ("RAPPORT-BATTERIE-5EY7GMJRA.txt",
     REPO / "atelier-cf3-5ey7gmjra/RAPPORT-BATTERIE-5EY7GMJRA.txt"),
    ("RAPPORT-CAMPAGNE-PBT-5EY7GMJRA.txt",
     REPO / "atelier-cf3-5ey7gmjra/RAPPORT-CAMPAGNE-PBT-5EY7GMJRA.txt"),
    ("RAPPORT-TRACES-HASH-V190.txt",
     REPO / "atelier-cf3-5ey7gmjra/RAPPORT-TRACES-HASH-V190.txt"),
]
for nom, chemin in PIECES_TEST:
    def g(nom=nom, chemin=chemin):
        if nom in test and test[nom].get("md5Checksum") == md5_de(chemin):
            return "DÉJÀ EN PLACE (md5 égal)"
        if nom in test:
            resumable(at, f"https://www.googleapis.com/upload/drive/v3/"
                          f"files/{test[nom]['id']}?uploadType=resumable",
                      {}, chemin)
        else:
            resumable(at, "https://www.googleapis.com/upload/drive/v3/files"
                          "?uploadType=resumable",
                      {"name": nom, "parents": [test_id]}, chemin)
        octets = contenu(at, inventaire(at, test_id)[nom]["id"])
        assert hashlib.md5(octets).hexdigest() == md5_de(chemin), "recoup échoue"
        return f"posé et recoupé byte-byte ({chemin.stat().st_size} o)"
    geste(f"le /test : {nom}", g)

# (2) le pack à la racine
def g_pack():
    chemin = REPO / "scripts/vague7/TRIADE_presentation_v0.19.3_20261120.zip"
    nom = chemin.name
    if nom in racine and racine[nom].get("md5Checksum") == md5_de(chemin):
        return "DÉJÀ EN PLACE (md5 égal)"
    if nom in racine:
        resumable(at, f"https://www.googleapis.com/upload/drive/v3/files/"
                      f"{racine[nom]['id']}?uploadType=resumable",
                  {}, chemin)
    else:
        resumable(at, "https://www.googleapis.com/upload/drive/v3/files"
                      "?uploadType=resumable",
                  {"name": nom, "parents": [ROOT_ID]}, chemin)
    octets = contenu(at, inventaire(at, ROOT_ID)[nom]["id"])
    assert hashlib.md5(octets).hexdigest() == md5_de(chemin), "recoup échoue"
    return f"posé à la racine et recoupé ({chemin.stat().st_size:,} o)" \
        .replace(",", " ")
geste("la racine : le pack v0.19.3", g_pack)

# (3) l'instruction archivée : /instructions → /ARCHIVE/instructions_20261119/
def g_archive():
    nom = "Qwen__20261118_5ey7gmjra.txt"
    if nom not in instructions:
        if nom in inventaire(at, inventaire(at, archive_id).get(
                "instructions_20261119", {}).get("id", "") if
                "instructions_20261119" in inventaire(at, archive_id)
                else ""):
            return "DÉJÀ ARCHIVÉE"
        raise RuntimeError("l'instruction introuvable au /instructions")
    fid = instructions[nom]["id"]
    dest = inventaire(at, archive_id)
    if "instructions_20261119" not in dest:
        st, body, _ = api(at, "POST", f"{API}/files",
                          {"name": "instructions_20261119",
                           "mimeType": "application/vnd.google-apps.folder",
                           "parents": [archive_id]})
        assert st == 200 or st == 201, (st, body[:200])
        dest = inventaire(at, archive_id)
    dest_id = dest["instructions_20261119"]["id"]
    # le geste Drive natif : ajouter le parent d'archive, retirer le parent
    # d'instructions — la corbeille JAMAIS (D143)
    st, body, _ = api(at, "GET", f"{API}/files/{fid}?fields=parents")
    parents = json.loads(body).get("parents", [])
    st, body, _ = api(at, "POST",
                      f"{API}/files/{fid}/parents"
                      f"?addParent={dest_id}", None)
    assert st in (200, 201), (st, body[:200])
    for p in parents:
        st, body, _ = api(at, "DELETE",
                          f"{API}/files/{fid}/parents"
                          f"?removeParent={p}")
        assert st in (200, 204), (st, body[:200])
    assert nom not in inventaire(at, instructions_id), "encore au /instructions"
    assert nom in inventaire(at, dest_id), "absente de l'archive"
    return "déplacée /instructions → /ARCHIVE/instructions_20261119/ " \
           "(la règle du développeur)"
geste("l'archivage de l'instruction 5ey7gmjra", g_archive)

verts = sum(1 for v, _, _ in bilan if v == "VERT")
print(f"\nBILAN DE LA LIVRAISON : {verts}/{len(bilan)} VERT")
sys.exit(0 if verts == len(bilan) else 1)
