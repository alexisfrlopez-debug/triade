#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification des TROIS BORDS — session Entrée 426 (le patron v233 adapté) :
1. dépôt local (la tête, l'atelier, le sceau-I)
2. GitHub (ls-remote == la tête)
3. coffre Drive (worklog/OU-TROUVER/REPRISE au miroir ET à la racine, bundle,
   l'atelier au miroir, les pièces du /livrables intactes, /instructions vide)
Zenodo : hors périmètre de la session (la publication v0.31.0 attend la commande).
"""
import hashlib
import subprocess
import sys
import urllib.request

DEPOT = "/home/z/my-project/depot"
MIRROR_FOLDER = "1ZzvJjLlGyVW4YKnXWdAgZO0IjFETKOZY"   # TRIADE-sauvegarde-git
COFFRE_ROOT = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
LIVRABLES = "1wF0p0g-OPdnL7fgnNsJb6D1rXhtyHqIZ"
INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"

ok, fail = [], []


def check(label, cond, detail=""):
    (ok if cond else fail).append((label, detail))
    print(("VERT  " if cond else "ROUGE ") + label + (f"  [{detail}]" if detail else ""))


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sa_token():
    """Jeton SA en lecture (la même voie que le vérifieur v233)."""
    import google.oauth2.service_account as sa
    import google.auth.transport.requests
    creds = sa.Credentials.from_service_account_file(
        "/home/z/my-project/upload/physichong-4b3b7222b48c.json",
        scopes=["https://www.googleapis.com/auth/drive.readonly"])
    req = google.auth.transport.requests.Request()
    creds.refresh(req)
    return creds.token


H = {"Authorization": "Bearer " + sa_token()}


def list_folder(folder):
    import json
    out = {}
    token = None
    while True:
        params = {"q": f"'{folder}' in parents and trashed=false",
                  "fields": "nextPageToken,files(id,name,mimeType,md5Checksum,size)",
                  "pageSize": 200}
        if token:
            params["pageToken"] = token
        url = "https://www.googleapis.com/drive/v3/files?" + urllib.parse.urlencode(params)
        r = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60)
        obj = json.load(r)
        for f in obj.get("files", []):
            out[f["name"]] = f
        token = obj.get("nextPageToken")
        if not token:
            return out


def get_file(fid):
    import json
    url = f"https://www.googleapis.com/drive/v3/files/{fid}?fields=id,name,md5Checksum,size,modifiedTime"
    r = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60)
    return json.load(r)


import urllib.parse  # noqa: E402
import os  # noqa: E402

# ---- 1. le dépôt
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=DEPOT,
                      capture_output=True, text=True).stdout.strip()
print(f"[bord 1] tête locale : {head[:12]}")
check("dépôt propre (aucun modified)",
      subprocess.run(["git", "status", "--porcelain"], cwd=DEPOT,
                     capture_output=True, text=True).stdout.strip() == "")
ATELIER = os.path.join(DEPOT, "atelier-run-collab-20261125")
for rel in ["preuves-collab-20261125T114128Z.zip",
            "temoins-arm-signes/constat-arm-verdict.txt",
            "temoins-arm-signes/temoin-dudect-arm-SYNTHESE.txt"]:
    check(f"atelier {rel}", os.path.exists(os.path.join(ATELIER, rel)))
sceau = subprocess.run(["python3", "v06/sceau_I.py", "verifier"], cwd=DEPOT,
                       capture_output=True, text=True)
check("sceau-I 14 arbres VERTS", sceau.returncode == 0 and
      sceau.stdout.count("vert") == 14, sceau.stdout.strip().splitlines()[-1])

# ---- 2. GitHub (ls-remote anonyme)
remote = subprocess.run(["git", "ls-remote", "https://github.com/alexisfrlopez-debug/triade.git", "HEAD"],
                        capture_output=True, text=True).stdout.split()[0]
check("GitHub == dépôt", remote == head, remote[:12])

# ---- 3a. le miroir : worklog, OU-TROUVER, REPRISE == md5 locaux
miroir = list_folder(MIRROR_FOLDER)
for local in ["worklog.md", "OU-TROUVER-LES-LIVRABLES.md", "REPRISE_PROJET.md"]:
    lmd5 = md5_of(os.path.join(DEPOT, local))
    f = miroir.get(local)
    check(f"miroir {local}", bool(f) and f.get("md5Checksum") == lmd5,
          f"{f.get('md5Checksum','?')[:10] if f else 'ABSENT'} vs {lmd5[:10]}")
# le bundle : md5 du bundle régénéré == celui du miroir
subprocess.run(["git", "bundle", "create", "/tmp/verif-bundle-426b", "--all"],
               cwd=DEPOT, capture_output=True)
f = miroir.get("triade-history.bundle")
check("miroir triade-history.bundle",
      bool(f) and f.get("md5Checksum") == md5_of("/tmp/verif-bundle-426b"),
      f"{f.get('md5Checksum','?')[:10] if f else 'ABSENT'} vs {md5_of('/tmp/verif-bundle-426b')[:10]}")
# l'atelier au miroir
miroir_at = list_folder([f["id"] for f in miroir.values()
                         if f["name"] == "atelier-run-collab-20261125" and
                         f["mimeType"] == "application/vnd.google-apps.folder"][0])
for rel, nom in [("preuves-collab-20261125T114128Z.zip", "preuves-collab-20261125T114128Z.zip"),
                 ("RAPPORT-RUN-COLLAB-20261125.txt", "RAPPORT-RUN-COLLAB-20261125.txt"),
                 ("recoup_run_collab.py", "recoup_run_collab.py")]:
    f = miroir_at.get(nom)
    check(f"miroir atelier {nom}",
          bool(f) and f.get("md5Checksum") == md5_of(os.path.join(ATELIER, rel)))

# ---- 3b. la racine du coffre : les trois fichiers d'instruction + worklog
racine = list_folder(COFFRE_ROOT)
for local in ["worklog.md", "REPRISE_PROJET.md", "OU-TROUVER-LES-LIVRABLES.md"]:
    lmd5 = md5_of(os.path.join(DEPOT, local))
    f = racine.get(local)
    check(f"coffre racine {local}", bool(f) and f.get("md5Checksum") == lmd5,
          f"{f.get('md5Checksum','?')[:10] if f else 'ABSENT'} vs {lmd5[:10]}")

# ---- 3c. le /livrables : les trois pièces de la session INTACTES
liv = list_folder(LIVRABLES)
for nom, ref in [("preuves-collab-20261125T114128Z.zip", ATELIER + "/preuves-collab-20261125T114128Z.zip"),
                 ("constat-arm-verdict.txt", ATELIER + "/temoins-arm-signes/constat-arm-verdict.txt"),
                 ("temoin-dudect-arm-SYNTHESE.txt", ATELIER + "/temoins-arm-signes/temoin-dudect-arm-SYNTHESE.txt")]:
    f = liv.get(nom)
    check(f"coffre /livrables {nom}",
          bool(f) and f.get("md5Checksum") == md5_of(ref),
          f.get("md5Checksum", "?")[:10] if f else "ABSENT")

# ---- 3d. le /instructions DEMEURÉ VIDE
instr = list_folder(INSTRUCTIONS)
check("coffre /instructions VIDE", len(instr) == 0, f"{len(instr)} fichiers")

print()
print(f"BILAN : {len(ok)} VERT, {len(fail)} ROUGE")
if fail:
    for label, detail in fail:
        print(f"  ROUGE {label} [{detail}]")
sys.exit(1 if fail else 0)
