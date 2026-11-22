#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification des TROIS BORDS — v0.23.3 (le patron v232 adapté) :
1. dépôt local (la tête, le sceau, les empreintes locales des packs)
2. GitHub (ls-remote anonyme == la tête)
3. coffre Drive (worklog, OU-TROUVER, REPRISE, bundle, packs v0.23.3 — md5)
4. Zenodo (record 24450872 publié, les trois md5, le concept sur v0.23.3)
"""
import hashlib, json, subprocess, sys, requests

DEPOT = "/home/z/my-project/depot"
MIRROR_FOLDER = "1ZzvJjLlGyVW4YKnXWdAgZO0IjFETKOZY"   # TRIADE-sauvegarde-git
COFFRE_ROOT = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
LIVRABLES = "1wF0p0g-OPdnL7fgnNsJb6D1rXhtyHqIZ"
CONCEPT = 24367343
VERSION_RECORD = 24450872

sys.path.insert(0, "/home/z/my-project/scripts")

def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

ok, fail = [], []

def check(label, cond, detail=""):
    (ok if cond else fail).append((label, detail))
    print(("VERT  " if cond else "ROUGE ") + label + (f"  [{detail}]" if detail else ""))

# ---- 1. le dépôt
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=DEPOT, capture_output=True, text=True).stdout.strip()
print(f"[bord 1] tête locale : {head[:12]}")
packs = {
    "TRIADE_soumission_v0.23.3.zip": "60e1fac77b601fd423c457f71be3d282",
    "TRIADE_presentation_v0.23.3.zip": "f8e6ad0ac0bf09c009ea6b11d01c3242",
    "TRIADE_complet_v0.23.3.zip": "dea007203a998b3aa2602b5d4816c4f2",
}
import os
for name, md5 in packs.items():
    p = os.path.join(DEPOT, name)
    if os.path.exists(p):
        check(f"dépôt {name}", md5_of(p) == md5, md5_of(p)[:10])
    else:
        p2 = os.path.join(DEPOT, "depot-zenodo-v0233", name)
        check(f"dépôt {name}", os.path.exists(p2) and md5_of(p2) == md5)

# ---- 2. GitHub (ls-remote anonyme)
remote_head = subprocess.run(["git", "ls-remote", "https://github.com/alexisfrlopez-debug/triade.git", "HEAD"],
                             capture_output=True, text=True).stdout.split()[0]
check("GitHub == dépôt", remote_head == head, remote_head[:12])

# ---- 3. le coffre Drive (SA en lecture)
from relais_service_account import get_sa_token
tok = get_sa_token()
H = {"Authorization": f"Bearer {tok}"}

def find_files(folder, names):
    out = {}
    params = {"q": f"'{folder}' in parents and trashed=false",
              "fields": "nextPageToken,files(id,name,size,mimeType,md5Checksum,modifiedTime)", "pageSize": 200}
    token = None
    while True:
        if token:
            params["pageToken"] = token
        r = requests.get("https://www.googleapis.com/drive/v3/files", headers=H, params=params, timeout=60)
        for f in r.json().get("files", []):
            if f["name"] in names:
                out[f["name"]] = f
        token = r.json().get("nextPageToken")
        if not token:
            break
    return out

# 3a. le miroir : worklog, OU-TROUVER, REPRISE == md5 locaux
import os
for local, remote_names in [
    ("worklog.md", ["worklog.md"]),
    ("OU-TROUVER-LES-LIVRABLES.md", ["OU-TROUVER-LES-LIVRABLES.md"]),
    ("REPRISE_PROJET.md", ["REPRISE_PROJET.md"]),
]:
    lmd5 = md5_of(os.path.join(DEPOT, local))
    f = find_files(MIRROR_FOLDER, remote_names).get(local)
    check(f"miroir Drive {local}", bool(f) and f.get("md5Checksum") == lmd5,
          f"{f.get('md5Checksum','')[:10] if f else 'ABSENT'} vs {lmd5[:10]}")

# le bundle : la tête dans le bundle == la tête locale (md5 du bundle régénéré)
bundle_local = subprocess.run(["git", "bundle", "create", "/tmp/verif-bundle", "--all"],
                              cwd=DEPOT, capture_output=True)
bmd5 = md5_of("/tmp/verif-bundle")
f = find_files(MIRROR_FOLDER, ["triade-history.bundle"]).get("triade-history.bundle")
check("miroir Drive triade-history.bundle", bool(f) and f.get("md5Checksum") == bmd5,
      f"{f.get('md5Checksum','')[:10] if f else 'ABSENT'} vs {bmd5[:10]}")

# 3b. le /livrables : les trois packs aux md5
liv = find_files(LIVRABLES, list(packs.keys()))
for name, md5 in packs.items():
    f = liv.get(name)
    check(f"coffre /livrables {name}", bool(f) and f.get("md5Checksum") == md5,
          f.get("md5Checksum", "")[:10] if f else "ABSENT")

# 3c. la racine du coffre : rapport + manifeste == md5 locaux
rac = find_files(COFFRE_ROOT, ["rapport_verification_v0.23.3.txt", "empreintes_livrables_v0.23.3.txt",
                               "REPRISE_PROJET.md", "OU-TROUVER-LES-LIVRABLES.md", "TRIADE_complet_v0.23.3.zip"])
for local, remote in [("rapport_verification_v0.23.3.txt", "rapport_verification_v0.23.3.txt"),
                      ("empreintes_livrables_v0.23.3.txt", "empreintes_livrables_v0.23.3.txt"),
                      ("REPRISE_PROJET.md", "REPRISE_PROJET.md"),
                      ("OU-TROUVER-LES-LIVRABLES.md", "OU-TROUVER-LES-LIVRABLES.md")]:
    lmd5 = None
    for cand in [os.path.join(DEPOT, local), os.path.join(DEPOT, "scripts", "vague15", local)]:
        if os.path.exists(cand):
            lmd5 = md5_of(cand)
    f = rac.get(remote)
    check(f"coffre racine {remote}", bool(f) and lmd5 and f.get("md5Checksum") == lmd5,
          f"{f.get('md5Checksum','')[:10] if f else 'ABSENT'} vs {str(lmd5)[:10] if lmd5 else 'n/a local'}")
f = rac.get("TRIADE_complet_v0.23.3.zip")
check("coffre racine TRIADE_complet_v0.23.3.zip", bool(f) and f.get("md5Checksum") == packs["TRIADE_complet_v0.23.3.zip"],
      f.get("md5Checksum", "")[:10] if f else "ABSENT")

# 3d. le /instructions DEMEURÉ VIDE
instr = requests.get("https://www.googleapis.com/drive/v3/files", headers=H, params={
    "q": f"'1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6' in parents and trashed=false", "fields": "files(id,name)"}, timeout=60)
check("coffre /instructions VIDE", len(instr.json().get("files", [])) == 0,
      f"{len(instr.json().get('files', []))} fichiers")

# ---- 4. Zenodo (bord anonyme)
r = requests.get(f"https://zenodo.org/api/records/{VERSION_RECORD}", timeout=60)
d = r.json()
check(f"Zenodo {VERSION_RECORD} PUBLIÉ", r.ok and d.get("state") == "done", d.get("state", "?"))
zf = {f["key"]: f for f in d.get("files", [])}
for name, md5 in packs.items():
    f = zf.get(name)
    check(f"Zenodo {name}", bool(f) and f.get("checksum") == f"md5:{md5}",
          str(f.get("checksum", ""))[:19] if f else "ABSENT")
# le concept résout sur v0.23.3
c = requests.get(f"https://zenodo.org/api/records/{CONCEPT}", timeout=60).json()
check("concept résout sur v0.23.3", c.get("doi") == f"10.5281/zenodo.{VERSION_RECORD}", c.get("doi", "?"))

print()
print(f"BILAN : {len(ok)} VERT, {len(fail)} ROUGE")
if fail:
    for label, detail in fail:
        print(f"  ROUGE : {label} [{detail}]")
    sys.exit(1)
print("LES TROIS BORDS VERTS — le dépôt, le GitHub, le coffre et Zenodo à la même tête.")
