#!/usr/bin/env python3
"""verifier_trois_bords_v230.py — LA VÉRIFICATION FINALE AUX TROIS BORDS
(la vague 13, la release v0.23.0). (1) GitHub — anonyme : ls-remote main ==
la tête locale ; (2) le coffre Drive — la racine (le complet v0.23.0 + le
rapport de vérification v0.23.0 + le manifeste des empreintes +
l'OU-TROUVER à l'Entrée 383), le /livrables (les TROIS packs v0.23.0, les
v0.22.1 supersédés), le /test (les huit pièces de session), le miroir
(worklog, OU-TROUVER, le bundle régénéré), l'ARCHIVE (les six instructions
de la vague 13), LE /instructions DEMEURE VIDE ; (3) Zenodo — anonyme : le
concept 10.5281/zenodo.24367343 résout sur la v0.23.0, les trois fichiers
md5 égaux aux pièces locales. Les lectures au compte de service (le bord
froid) ; urllib seul."""
import hashlib
import json
import subprocess
import sys
import time
import urllib.request

sys.path.insert(0, "/home/z/my-project/depot/scripts/vague11")
from drive_sa_v220 import liste  # noqa: E402

DEPOT = "/home/z/my-project/depot"
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
LIVRABLES = "1wF0p0g-OPdnL7fgnNsJb6D1rXhtyHqIZ"
MIROIR = "1ZzvJjLlGyVW4YKnXWdAgZO0IjFETKOZY"
INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
ARCHIVE = "1uJ5yU7ma5dYQM1GuWzm9Fx1I1U3Ywepr"
CONCEPT = "24367343"

R = []  # résultats (label, ok)


def vert(label, ok):
    R.append((label, ok))
    print(f"  {'VERT' if ok else 'ROUGE'} {label}")
    return ok


def md5_de(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def recup(url, essais=4, attente=15):
    for i in range(essais):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "triade-v230"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.read()
        except Exception as e:
            print(f"    [zenodo] tentative {i + 1}/{essais} : {e}")
            time.sleep(attente)
    return 0, b""


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
    ("TRIADE_complet_v0.23.0.zip",
     f"{DEPOT}/depot-zenodo-v0230/TRIADE_complet_v0.23.0.zip"),
    ("rapport_verification_v0.23.0.txt",
     f"{DEPOT}/rapport_verification_v0.23.0.txt"),
    ("empreintes_livrables_v0.23.0.txt",
     f"{DEPOT}/scripts/vague13/empreintes_livrables_v0.23.0.txt"),
]:
    ok = nom in rac and rac[nom].get("md5Checksum") == md5_de(chemin)
    vert(f"la racine : {nom} [{rac.get(nom, {}).get('size', '?')} o] "
         f"md5 recoupé", ok)
ok = "OU-TROUVER-LES-LIVRABLES.md" in rac and \
    rac["OU-TROUVER-LES-LIVRABLES.md"].get("md5Checksum") == \
    md5_de(f"{DEPOT}/OU-TROUVER-LES-LIVRABLES.md")
vert("la racine : OU-TROUVER à l'Entrée 383 (md5 recoupé)", ok)
vert("la racine : les pièces v0.22.1 supersédées (plus à la racine)",
     "rapport_verification_v0.22.1.txt" not in rac and
     "empreintes_livrables_v0.22.1.txt" not in rac)

liv = {x["name"]: x for x in liste(LIVRABLES)}
for nom, chemin in [
    ("TRIADE_soumission_v0.23.0.zip",
     f"{DEPOT}/depot-zenodo-v0230/TRIADE_soumission_v0.23.0.zip"),
    ("TRIADE_complet_v0.23.0.zip",
     f"{DEPOT}/depot-zenodo-v0230/TRIADE_complet_v0.23.0.zip"),
    ("TRIADE_presentation_v0.23.0.zip",
     f"{DEPOT}/TRIADE_presentation_v0.23.0.zip"),
]:
    ok = nom in liv and liv[nom].get("md5Checksum") == md5_de(chemin)
    vert(f"le /livrables : {nom} md5 recoupé", ok)
vert("le /livrables : les packs v0.22.1 supersédés au lot ARCHIVE",
     all(n not in liv for n in ("TRIADE_soumission_v0.22.1.zip",
                                "TRIADE_complet_v0.22.1.zip",
                                "TRIADE_presentation_v0.22.1.zip")))

tes = {x["name"]: x for x in liste(TEST)}
pieces = [
    ("rapport_verification_v0.23.0.txt",
     f"{DEPOT}/rapport_verification_v0.23.0.txt"),
    ("empreintes_livrables_v0.23.0.txt",
     f"{DEPOT}/scripts/vague13/empreintes_livrables_v0.23.0.txt"),
    ("rapport-ghash.txt",
     f"{DEPOT}/atelier-ghash-0g3400vql/rapport-ghash.txt"),
    ("rapport-requalification.txt",
     f"{DEPOT}/atelier-requalification-q8kugkpdu/"
     f"rapport-requalification.txt"),
    ("rapport-ventilation.txt",
     f"{DEPOT}/atelier-hcgp3-ay6zuzm8o/rapport-ventilation.txt"),
    ("rapport-ajouter-v3.txt",
     f"{DEPOT}/atelier-ajouter-v3-5nwnwoceo/rapport-ajouter-v3.txt"),
    ("rapport-purge-v13.txt",
     f"{DEPOT}/atelier-purge-v13-h66o54pjd/rapport-purge-v13.txt"),
    ("rapport-generation.txt",
     f"{DEPOT}/atelier-generation-v0230-ylrzmlbn8/rapport-generation.txt"),
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

# l'ARCHIVE : le lot des instructions de la vague 13 aux SIX
lots = {x["name"]: x["id"] for x in liste(ARCHIVE)
        if x["mimeType"] == "application/vnd.google-apps.folder"}
ok = "instructions_vague13_20261122" in lots and \
    len(liste(lots["instructions_vague13_20261122"])) == 6
vert("l'ARCHIVE : instructions_vague13_20261122 aux SIX pièces", ok)

ins = liste(INSTRUCTIONS)
vert(f"le /instructions DEMEURE VIDE ({len(ins)} fichier)",
     len(ins) == 0)

print("== (3) LE ZENODO — le bord anonyme ==")
st, body = recup(f"https://zenodo.org/api/records/{CONCEPT}")
assert st == 200, f"concept illisible : HTTP {st}"
c = json.loads(body)
vert(f"le concept 10.5281/zenodo.{CONCEPT} résout sur la v0.23.0 "
     f"(record {c['id']}, version {c['metadata']['version']})",
     c["metadata"]["version"] == "v0.23.0")
vert("le DOI de version minté au concept (l'URL vivante)",
     str(c["doi"]).endswith(str(c["id"])) and c["id"] == 24438614)
files_pub = {f["key"]: f["checksum"].split("md5:")[-1]
             for f in c.get("files", [])}
for nom, chemin in [
    ("TRIADE_soumission_v0.23.0.zip",
     f"{DEPOT}/depot-zenodo-v0230/TRIADE_soumission_v0.23.0.zip"),
    ("TRIADE_complet_v0.23.0.zip",
     f"{DEPOT}/depot-zenodo-v0230/TRIADE_complet_v0.23.0.zip"),
    ("TRIADE_presentation_v0.23.0.zip",
     f"{DEPOT}/TRIADE_presentation_v0.23.0.zip"),
]:
    vert(f"Zenodo : {nom} md5 recoupé au bord anonyme",
         files_pub.get(nom) == md5_de(chemin))

print()
verts = sum(1 for _, ok in R if ok)
print(f"LA VÉRIFICATION AUX TROIS BORDS : {verts}/{len(R)} VERT"
      + ("" if verts == len(R) else " — ROUGE !"))
sys.exit(0 if verts == len(R) else 1)
