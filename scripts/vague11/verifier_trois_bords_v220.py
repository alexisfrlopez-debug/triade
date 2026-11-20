#!/usr/bin/env python3
"""verifier_trois_bords_v220.py — LA VÉRIFICATION FINALE AUX TROIS BORDS
(la vague 11). (1) GitHub — anonyme : ls-remote main == la tête locale ;
(2) le coffre Drive — la racine (le pack + les deux archives + le rapport
+ l'OU-TROUVER à l'Entrée 381), le /test (treize pièces), le miroir
(worklog, OU-TROUVER, le bundle régénéré), LE /instructions DEMEURE VIDE ;
(3) Zenodo — anonyme : le concept 10.5281/zenodo.24367343 résout sur la
v0.22.0, les trois fichiers md5 égaux aux pièces locales. Les lectures au
compte de service (le bord froid) ; urllib seul."""
import hashlib
import json
import subprocess
import sys
import urllib.request

sys.path.insert(0, "/home/z/my-project/depot/scripts/vague11")
from drive_sa_v220 import liste  # noqa: E402

DEPOT = "/home/z/my-project/depot"
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
MIROIR = "1ZzvJjLlGyVW4YKnXWdAgZO0IjFETKOZY"
INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
CONCEPT = "24367343"

R = []  # résultats (label, ok)


def vert(label, ok):
    R.append((label, ok))
    print(f"  {'VERT' if ok else 'ROUGE'} {label}")
    return ok


def md5_de(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def recup(url):
    req = urllib.request.Request(url, headers={"User-Agent": "triade-v220"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read()


print("== (1) LE GIT — le bord anonyme ==")
out = subprocess.run(["git", "ls-remote",
                      "https://github.com/alexisfrlopez-debug/triade.git",
                      "refs/heads/main"], capture_output=True, text=True,
                     cwd=DEPOT).stdout.strip().split()[0]
loc = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                     text=True, cwd=DEPOT).stdout.strip()
vert(f"GitHub main == {loc[:12]} (distant {out[:12]})", out == loc)

print("== (2) LE COFFRE DRIVE ==")
rac = {x["name"]: x for x in liste(RACINE)}
for nom, chemin in [
    ("TRIADE_presentation_v0.22.0.zip",
     f"{DEPOT}/TRIADE_presentation_v0.22.0.zip"),
    ("TRIADE_soumission_v0.22.0.zip",
     f"{DEPOT}/depot-zenodo-v0220/TRIADE_soumission_v0.22.0.zip"),
    ("TRIADE_complet_v0.22.0.zip",
     f"{DEPOT}/depot-zenodo-v0220/TRIADE_complet_v0.22.0.zip"),
    ("rapport_verification_v0.22.0.txt",
     f"{DEPOT}/scripts/vague11/rapport_verification_v0.22.0.txt"),
]:
    ok = nom in rac and rac[nom].get("md5Checksum") == md5_de(chemin)
    vert(f"la racine : {nom} [{rac.get(nom, {}).get('size', '?')} o] "
         f"md5 recoupé", ok)
ok = "OU-TROUVER-LES-LIVRABLES.md" in rac and \
    rac["OU-TROUVER-LES-LIVRABLES.md"].get("md5Checksum") == \
    md5_de(f"{DEPOT}/OU-TROUVER-LES-LIVRABLES.md")
vert("la racine : OU-TROUVER à l'Entrée 381 (md5 recoupé)", ok)

tes = {x["name"]: x for x in liste(TEST)}
pieces = [
    ("rapport_verification_v0.22.0.txt",
     f"{DEPOT}/scripts/vague11/rapport_verification_v0.22.0.txt"),
    ("empreintes_livrables_v0.22.0.txt",
     f"{DEPOT}/scripts/vague11/empreintes_livrables_v0.22.0.txt"),
    ("rapport-purge.txt",
     f"{DEPOT}/atelier-sequestre-ou6wn6wlv/rapport-purge.txt"),
    ("rapport-corridors.txt",
     f"{DEPOT}/atelier-corridors-fnvan0zes/rapport-corridors.txt"),
    ("rapport-temps-reel-corridors.txt",
     f"{DEPOT}/atelier-corridors-fnvan0zes/"
     f"rapport-temps-reel-corridors.txt"),
    ("rapport-porteuse.txt",
     f"{DEPOT}/atelier-porteuse-ahult8jgd/rapport-porteuse.txt"),
    ("rapport-gabarits.txt",
     f"{DEPOT}/atelier-gabarits-o5apue194/rapport-gabarits.txt"),
    ("rapport-coffre.txt",
     f"{DEPOT}/atelier-coffre-vr9n3s3l7/rapport-coffre.txt"),
    ("rapport-cgp-m4.txt",
     f"{DEPOT}/atelier-quatrebras-3lmyfb2xa/rapport-cgp-m4.txt"),
    ("rapport-preregistre.txt",
     f"{DEPOT}/atelier-preregistre-l4nnwqlld/rapport-preregistre.txt"),
    ("rapport-lifter.txt",
     f"{DEPOT}/atelier-lifter-hrbdfy6i4/rapport-lifter.txt"),
    ("rapport-plancher-natif.txt",
     f"{DEPOT}/atelier-medians-zho5vilpy/rapport-plancher-natif.txt"),
    ("rapport-recompte.txt",
     f"{DEPOT}/atelier-medians-zho5vilpy/rapport-recompte.txt"),
]
for nom, chemin in pieces:
    ok = nom in tes and tes[nom].get("md5Checksum") == md5_de(chemin)
    vert(f"le /test : {nom} md5 recoupé", ok)

mir = {x["name"]: x for x in liste(MIROIR)}
for nom, chemin in [
    ("worklog.md", f"{DEPOT}/worklog.md"),
    ("OU-TROUVER-LES-LIVRABLES.md", f"{DEPOT}/OU-TROUVER-LES-LIVRABLES.md"),
]:
    ok = nom in mir and mir[nom].get("md5Checksum") == md5_de(chemin)
    vert(f"le miroir : {nom} md5 recoupé", ok)
vert("le miroir : triade-history.bundle régénéré (présent)",
     "triade-history.bundle" in mir)
vert("le miroir : scripts/ présent (les outils committés — D97)",
     "scripts" in mir)

ins = liste(INSTRUCTIONS)
vert(f"le /instructions DEMEURE VIDE ({len(ins)} fichier)",
     len(ins) == 0)

print("== (3) LE ZENODO — le bord anonyme ==")
st, body = recup(f"https://zenodo.org/api/records/{CONCEPT}")
c = json.loads(body)
vert(f"le concept 10.5281/zenodo.{CONCEPT} résout sur la v0.22.0 "
     f"(record {c['id']}, version {c['metadata']['version']})",
     c["metadata"]["version"] == "v0.22.0")
vert("le DOI de version minté au concept (l'URL vivante)",
     str(c["doi"]).endswith(str(c["id"])) and c["id"] != 24397623)
files_pub = {f["key"]: f["checksum"].split("md5:")[-1]
             for f in c.get("files", [])}
for nom, chemin in [
    ("TRIADE_soumission_v0.22.0.zip",
     f"{DEPOT}/depot-zenodo-v0220/TRIADE_soumission_v0.22.0.zip"),
    ("TRIADE_complet_v0.22.0.zip",
     f"{DEPOT}/depot-zenodo-v0220/TRIADE_complet_v0.22.0.zip"),
    ("TRIADE_presentation_v0.22.0.zip",
     f"{DEPOT}/TRIADE_presentation_v0.22.0.zip"),
]:
    vert(f"zenodo : {nom} md5 byte-byte",
         files_pub.get(nom) == md5_de(chemin))

nb = sum(1 for _, ok in R if ok)
print(f"\nLA VÉRIFICATION : {nb}/{len(R)} VERT, "
      f"{len(R) - nb} ROUGE")
sys.exit(0 if nb == len(R) else 1)
