#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification des TROIS BORDS — session Entrée 428 (le patron v426 adapté) :
1. dépôt local (la tête, l'atelier, le sceau-I)
2. GitHub (ls-remote == la tête)
3. coffre Drive : worklog/OU-TROUVER/REPRISE au miroir ET à la racine, bundle,
   l'atelier au miroir, LE DÉPÔT DES 43 PIÈCES du maître au /livrables
   intactes, /instructions vide.
Zenodo : hors périmètre de la session (la publication v0.31.0 attend la commande).
"""
import hashlib
import subprocess
import sys
import urllib.request

DEPOT = "/home/z/my-project/depot"
ATELIER = DEPOT + "/atelier-actions-syntheses-signees-20261125"
SILICIUMS = DEPOT + "/atelier-siliciums-commodite-v100/preuves-actions"
MIRROR_FOLDER = "1ZzvJjLlGyVW4YKnXWdAgZO0IjFETKOZY"   # TRIADE-sauvegarde-git
COFFRE_ROOT = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
LIVRABLES = "1wF0p0g-OPdnL7fgnNsJb6D1rXhtyHqIZ"   # (l'id exact du v426 — la typo fgur corrigée)
INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
DEPOT_CAMPAGNE = "preuves-actions-campagne-20261125"    # au /livrables

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
    import time
    out = {}
    token = None
    while True:
        params = {"q": f"'{folder}' in parents and trashed=false",
                  "fields": "nextPageToken,files(id,name,mimeType,md5Checksum,size)",
                  "pageSize": 200}
        if token:
            params["pageToken"] = token
        url = "https://www.googleapis.com/drive/v3/files?" + urllib.parse.urlencode(params)
        # reprise idempotente aux 404/500 passagers du bord Drive (3 essais)
        for essai in range(3):
            try:
                r = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60)
                obj = json.load(r)
                break
            except urllib.error.HTTPError as e:
                if essai == 2:
                    raise
                time.sleep(3 * (essai + 1))
        for f in obj.get("files", []):
            out[f["name"]] = f
        token = obj.get("nextPageToken")
        if not token:
            return out


import urllib.parse  # noqa: E402
import os  # noqa: E402

# ---- 1. le dépôt
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=DEPOT,
                      capture_output=True, text=True).stdout.strip()
print(f"[bord 1] tête locale : {head[:12]}")
check("dépôt propre (aucun modified)",
      subprocess.run(["git", "status", "--porcelain"], cwd=DEPOT,
                     capture_output=True, text=True).stdout.strip() == "")
for rel in ["recoup_actions_20261125.py", "EMPREINTES-ACTIONS-DEPOT.txt",
            "RAPPORT-ACTIONS-SYNTHESES-SIGNEES-20261125.txt",
            "temoins-signes/temoin-dudect-collab-N60.txt",
            "temoins-signes/temoin-dudect-collab-SYNTHESE.txt",
            "temoins-signes/temoin-dudect-arm-SYNTHESE.txt",
            "temoins-signes/temoin-dudect-apple-SYNTHESE.txt"]:
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
subprocess.run(["git", "bundle", "create", "/tmp/verif-bundle-428", "--all"],
               cwd=DEPOT, capture_output=True)
f = miroir.get("triade-history.bundle")
check("miroir triade-history.bundle",
      bool(f) and f.get("md5Checksum") == md5_of("/tmp/verif-bundle-428"),
      f"{f.get('md5Checksum','?')[:10] if f else 'ABSENT'} vs {md5_of('/tmp/verif-bundle-428')[:10]}")
# l'atelier au miroir
miroir_at = list_folder([f["id"] for f in miroir.values()
                         if f["name"] == "atelier-actions-syntheses-signees-20261125" and
                         f["mimeType"] == "application/vnd.google-apps.folder"][0])
for nom in ["recoup_actions_20261125.py", "EMPREINTES-ACTIONS-DEPOT.txt",
            "RAPPORT-ACTIONS-SYNTHESES-SIGNEES-20261125.txt"]:
    f = miroir_at.get(nom)
    check(f"miroir atelier {nom}",
          bool(f) and f.get("md5Checksum") == md5_of(os.path.join(ATELIER, nom)))

# ---- 3b. la racine du coffre : worklog, REPRISE, OU-TROUVER
racine = list_folder(COFFRE_ROOT)
for local in ["worklog.md", "REPRISE_PROJET.md", "OU-TROUVER-LES-LIVRABLES.md"]:
    lmd5 = md5_of(os.path.join(DEPOT, local))
    f = racine.get(local)
    check(f"coffre racine {local}", bool(f) and f.get("md5Checksum") == lmd5,
          f"{f.get('md5Checksum','?')[:10] if f else 'ABSENT'} vs {lmd5[:10]}")

# ---- 3c. le /livrables : LE DÉPÔT DES 43 PIÈCES DU MAÎTRE INTACT
# (les SIX signées comparées aux copies SIGNÉES de l'atelier — préfixe
#  intact + signature ; les autres, aux originaux committés)
SIGNES_SET = {
    ("kit-C-x86-serveur", "temoin-dudect-collab-N60.txt"),
    ("kit-C-x86-serveur", "temoin-dudect-collab-N200.txt"),
    ("kit-C-x86-serveur", "temoin-dudect-collab-N400.txt"),
    ("kit-C-x86-serveur", "temoin-dudect-collab-SYNTHESE.txt"),
    ("kit-D-arm64-serveur", "temoin-dudect-arm-SYNTHESE.txt"),
    ("kit-G-apple-silicon", "temoin-dudect-apple-SYNTHESE.txt"),
}
liv = list_folder(LIVRABLES)
camp = liv.get(DEPOT_CAMPAGNE)
check("coffre /livrables preuves-actions-campagne-20261125 (dossier)",
      bool(camp) and camp["mimeType"] == "application/vnd.google-apps.folder")
if camp:
    pa = list_folder(camp["id"])            # preuves-actions (le sous-dossier unique)
    pa_id = [f["id"] for f in pa.values()
             if f["mimeType"] == "application/vnd.google-apps.folder"][0]
    sous = {f["name"]: f["id"] for f in list_folder(pa_id).values()
            if f["mimeType"] == "application/vnd.google-apps.folder"}
    n_check, n_signees = 0, 0
    for kit in ["kit-C-x86-serveur", "kit-D-arm64-serveur",
                "kit-G-apple-silicon", "vague1-annulee-macos"]:
        drive_kit = list_folder(sous[kit])
        for p in sorted(os.listdir(os.path.join(SILICIUMS, kit))):
            local_path = os.path.join(SILICIUMS, kit, p)
            if (kit, p) in SIGNES_SET:
                local_path = os.path.join(ATELIER, "temoins-signes", p)
                n_signees += 1
            if not os.path.isfile(local_path):
                continue
            f = drive_kit.get(p)
            check(f"/livrables {kit}/{p}",
                  bool(f) and f.get("md5Checksum") == md5_of(local_path))
            n_check += 1
    check("/livrables le dépôt du maître == 43 pièces (dont 6 signées)",
          n_check == 43 and n_signees == 6, f"{n_check} pièces, {n_signees} signées")

# ---- 3d. le /instructions DEMEURÉ VIDE
instr = list_folder(INSTRUCTIONS)
check("coffre /instructions VIDE", len(instr) == 0, f"{len(instr)} fichiers")

print()
print(f"BILAN : {len(ok)} VERT, {len(fail)} ROUGE")
if fail:
    for label, detail in fail:
        print(f"  ROUGE {label} [{detail}]")
sys.exit(1 if fail else 0)
