#!/usr/bin/env python3
"""verifier_trois_bords_v210.py — LA VÉRIFICATION FINALE AUX TROIS BORDS.
(1) GitHub — anonyme : ls-remote main == la tête locale ;
(2) le coffre Drive — la racine (pack + deux archives + OU-TROUVER), le /test
    (six pièces), le miroir (worklog, OU-TROUVER, les deux outils, le bundle),
    le /instructions DEMEURE VIDE ;
(3) Zenodo — anonyme : le concept résout sur la v0.21.0, les trois fichiers
    md5 égaux aux pièces locales."""
import hashlib
import json
import subprocess
import sys

import requests

sys.path.insert(0, "/home/z/my-project/scripts")
from sa_auth_test import get_sa_token  # noqa: E402

DEPOT = "/home/z/my-project/depot"
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
MIROIR = "1ZzvJjLlGyVW4YKnXWdAgZO0IjFETKOZY"
INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"

R = []  # résultats (label, ok)


def vert(label, ok):
    R.append((label, ok))
    print(f"  {'VERT' if ok else 'ROUGE'} {label}")
    return ok


def md5_de(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


tok = get_sa_token()
H = {"Authorization": f"Bearer {tok}"}


def liste(parent):
    r = requests.get("https://www.googleapis.com/drive/v3/files",
                     params={"q": f"'{parent}' in parents and trashed=false",
                             "fields": "files(name,size,md5Checksum,modifiedTime)",
                             "pageSize": 200}, headers=H, timeout=30)
    r.raise_for_status()
    return {x["name"]: x for x in r.json().get("files", [])}


print("== (1) LE GIT — le bord anonyme ==")
out = subprocess.run(["git", "ls-remote",
                      "https://github.com/alexisfrlopez-debug/triade.git",
                      "refs/heads/main"], capture_output=True, text=True,
                     cwd=DEPOT).stdout.strip().split()[0]
loc = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                     text=True, cwd=DEPOT).stdout.strip()
vert(f"GitHub main == {loc[:12]} (distant {out[:12]})", out == loc)

print("== (2) LE COFFRE DRIVE ==")
rac = liste(RACINE)
for nom, chemin in [
    ("TRIADE_presentation_v0.21.0.zip",
     f"{DEPOT}/TRIADE_presentation_v0.21.0.zip"),
    ("TRIADE_soumission_v0.21.0.zip",
     f"{DEPOT}/depot-zenodo-v0210/TRIADE_soumission_v0.21.0.zip"),
    ("TRIADE_complet_v0.21.0.zip",
     f"{DEPOT}/depot-zenodo-v0210/TRIADE_complet_v0.21.0.zip"),
]:
    ok = nom in rac and rac[nom].get("md5Checksum") == md5_de(chemin)
    vert(f"la racine : {nom} [{rac[nom].get('size','?')} o] md5 recoupé", ok)
ok = "OU-TROUVER-LES-LIVRABLES.md" in rac and \
    rac["OU-TROUVER-LES-LIVRABLES.md"].get("md5Checksum") == \
    md5_de(f"{DEPOT}/OU-TROUVER-LES-LIVRABLES.md")
vert("la racine : OU-TROUVER à l'Entrée 380 (md5 recoupé)", ok)

tes = liste(TEST)
pieces = [
    ("rapport_verification_v0.21.0.txt",
     f"{DEPOT}/rapport_verification_v0.21.0.txt"),
    ("empreintes_livrables_v0.21.0.txt",
     f"{DEPOT}/scripts/vague10/empreintes_livrables_v0.21.0.txt"),
    ("rapport-cg-reconciliation.txt",
     f"{DEPOT}/atelier-cg-3a91o5whb/rapport-cg-reconciliation.txt"),
    ("rapport-temps-reel.txt",
     f"{DEPOT}/atelier-remesure-sse2-8z4hj76w4/rapport-temps-reel.txt"),
    ("rapport-fenetre.txt",
     f"{DEPOT}/atelier-fenetre-mqf258e4l/rapport-fenetre.txt"),
    ("rapport-non-interference-v210.txt",
     f"{DEPOT}/atelier-gardes-ifqm1d1i4/rapport-non-interference-v210.txt"),
]
for nom, chemin in pieces:
    ok = nom in tes and tes[nom].get("md5Checksum") == md5_de(chemin)
    vert(f"le /test : {nom} md5 recoupé", ok)

mir = liste(MIROIR)
for nom, chemin in [
    ("worklog.md", f"{DEPOT}/worklog.md"),
    ("OU-TROUVER-LES-LIVRABLES.md", f"{DEPOT}/OU-TROUVER-LES-LIVRABLES.md"),
    ("triade-history.bundle", None),
]:
    if nom == "triade-history.bundle":
        vert("le miroir : triade-history.bundle régénéré (présent)",
             nom in mir)
        continue
    ok = nom in mir and mir[nom].get("md5Checksum") == md5_de(chemin)
    vert(f"le miroir : {nom} md5 recoupé", ok)
# les deux outils committés au miroir (sous scripts/vague10/)
r = requests.get("https://www.googleapis.com/drive/v3/files",
                 params={"q": f"'{MIROIR}' in parents and "
                              "name='scripts'"},
                 headers=H, timeout=30)
ok = len(r.json().get("files", [])) == 1
vert("le miroir : scripts/ présent", ok)

ins = liste(INSTRUCTIONS)
vert(f"le /instructions DEMEURE VIDE ({len(ins)} fichier)", len(ins) == 0)

print("== (3) LE ZENODO — le bord anonyme ==")
r = requests.get("https://zenodo.org/api/records/24397623", timeout=30)
d = r.json()
vert("records/24397623 HTTP 200, la version " + d["metadata"]["version"],
     r.status_code == 200 and d["metadata"]["version"] == "v0.21.0")
files_pub = {f["key"]: f["checksum"].split("md5:")[-1]
             for f in d.get("files", [])}
ok = files_pub.get("TRIADE_soumission_v0.21.0.zip") == \
    md5_de(f"{DEPOT}/depot-zenodo-v0210/TRIADE_soumission_v0.21.0.zip")
vert("soumission md5 byte-byte", ok)
ok = files_pub.get("TRIADE_complet_v0.21.0.zip") == \
    md5_de(f"{DEPOT}/depot-zenodo-v0210/TRIADE_complet_v0.21.0.zip")
vert("complet md5 byte-byte", ok)
ok = files_pub.get("TRIADE_presentation_v0.21.0.zip") == \
    md5_de(f"{DEPOT}/TRIADE_presentation_v0.21.0.zip")
vert("présentation md5 byte-byte", ok)
r = requests.get("https://zenodo.org/api/records/24367343", timeout=30)
c = r.json()
vert(f"le concept résout sur la v0.21.0 "
     f"(record {c['id']}, version {c['metadata']['version']})",
     c["metadata"]["version"] == "v0.21.0" and str(c["id"]) == "24397623")

nb = sum(1 for _, ok in R if ok)
print(f"\nLA VÉRIFICATION : {nb}/{len(R)} VERT, "
      f"{len(R) - nb} ROUGE")
sys.exit(0 if nb == len(R) else 1)
