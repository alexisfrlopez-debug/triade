#!/usr/bin/env python3
"""verifier_trois_bords_v221.py — LA VÉRIFICATION FINALE AUX TROIS BORDS
(la vague 12, la release v0.22.1). (1) GitHub — anonyme : ls-remote main ==
la tête locale ; (2) le coffre Drive — la racine (le complet v0.22.1 + le
rapport de vérification v0.22.1 + le manifeste, ET les pièces v0.22.0
demeurées), le /test (dix-neuf pièces), le miroir (worklog, OU-TROUVER, le
bundle régénéré), LE /instructions DEMEURE VIDE ; (3) Zenodo — anonyme :
le concept 10.5281/zenodo.24367343 résout sur la v0.22.1, les trois
fichiers md5 égaux aux pièces locales (la soumission et la présentation
demeurées, le complet régénéré). Les lectures au compte de service (le
bord froid) ; urllib seul."""
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


def recup(url, essais=4, attente=15):
    for i in range(essais):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "triade-v221"})
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
    ("TRIADE_complet_v0.22.1.zip",
     f"{DEPOT}/depot-zenodo-v0221/TRIADE_complet_v0.22.1.zip"),
    ("rapport_verification_v0.22.1.txt",
     f"{DEPOT}/scripts/vague12/rapport_verification_v0.22.1.txt"),
    ("empreintes_livrables_v0.22.1.txt",
     f"{DEPOT}/scripts/vague12/empreintes_livrables_v0.22.1.txt"),
    # les pièces v0.22.0 DEMEURÉES à la racine
    ("TRIADE_presentation_v0.22.0.zip",
     f"{DEPOT}/TRIADE_presentation_v0.22.0.zip"),
    ("TRIADE_soumission_v0.22.0.zip",
     f"{DEPOT}/depot-zenodo-v0220/TRIADE_soumission_v0.22.0.zip"),
    ("rapport_verification_v0.22.0.txt",
     f"{DEPOT}/scripts/vague11/rapport_verification_v0.22.0.txt"),
]:
    ok = nom in rac and rac[nom].get("md5Checksum") == md5_de(chemin)
    vert(f"la racine : {nom} [{rac.get(nom, {}).get('size', '?')} o] "
         f"md5 recoupé", ok)
ok = "OU-TROUVER-LES-LIVRABLES.md" in rac and \
    rac["OU-TROUVER-LES-LIVRABLES.md"].get("md5Checksum") == \
    md5_de(f"{DEPOT}/OU-TROUVER-LES-LIVRABLES.md")
vert("la racine : OU-TROUVER à l'Entrée 382 (md5 recoupé)", ok)

tes = {x["name"]: x for x in liste(TEST)}
pieces = [
    ("rapport_verification_v0.22.1.txt",
     f"{DEPOT}/scripts/vague12/rapport_verification_v0.22.1.txt"),
    ("empreintes_livrables_v0.22.1.txt",
     f"{DEPOT}/scripts/vague12/empreintes_livrables_v0.22.1.txt"),
    ("rapport-recomposabilite.txt",
     f"{DEPOT}/atelier-recomposabilite-6kbfrpn7k/"
     f"rapport-recomposabilite.txt"),
    ("rapport-audit-ratios.txt",
     f"{DEPOT}/atelier-recomposabilite-6kbfrpn7k/rapport-audit-ratios.txt"),
    ("rapport-census.txt",
     f"{DEPOT}/atelier-recomposabilite-6kbfrpn7k/rapport-census.txt"),
    ("rapport-purge-semantique.txt",
     f"{DEPOT}/atelier-purge-0uug27teo/rapport-purge-semantique.txt"),
    ("rapport-verification-purge.txt",
     f"{DEPOT}/atelier-purge-0uug27teo/rapport-verification-purge.txt"),
    ("rapport-conformite.txt",
     f"{DEPOT}/atelier-conformite-alhmpl35u/rapport-conformite.txt"),
    ("rapport-generatif.txt",
     f"{DEPOT}/atelier-conformite-alhmpl35u/rapport-generatif.txt"),
    ("grille-reception-autotests.txt",
     f"{DEPOT}/atelier-conformite-alhmpl35u/"
     f"grille-reception-autotests.txt"),
    ("rapport-double-moteur.txt",
     f"{DEPOT}/atelier-double-moteur-14n3k8gd7/rapport-double-moteur.txt"),
    ("rapport-budget-risque.txt",
     f"{DEPOT}/atelier-double-moteur-14n3k8gd7/rapport-budget-risque.txt"),
    ("rapport-generalisateur.txt",
     f"{DEPOT}/atelier-double-moteur-14n3k8gd7/"
     f"rapport-generalisateur.txt"),
    ("rapport-menace-cache.txt",
     f"{DEPOT}/atelier-double-moteur-14n3k8gd7/rapport-menace-cache.txt"),
    ("rapport-ajouter-v2.txt",
     f"{DEPOT}/atelier-ajouter-v2-pgodgk35l/rapport-ajouter-v2.txt"),
    ("rapport-campagne-v2.txt",
     f"{DEPOT}/atelier-ajouter-v2-pgodgk35l/rapport-campagne-v2.txt"),
    ("rapport-marge-vierge.txt",
     f"{DEPOT}/atelier-marge-vierge-x705m50vl/rapport-marge-vierge.txt"),
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
assert st == 200, f"concept illisible : HTTP {st}"
c = json.loads(body)
vert(f"le concept 10.5281/zenodo.{CONCEPT} résout sur la v0.22.1 "
     f"(record {c['id']}, version {c['metadata']['version']})",
     c["metadata"]["version"] == "v0.22.1")
vert("le DOI de version minté au concept (l'URL vivante)",
     str(c["doi"]).endswith(str(c["id"])) and c["id"] != 24407701)
files_pub = {f["key"]: f["checksum"].split("md5:")[-1]
             for f in c.get("files", [])}
for nom, chemin in [
    ("TRIADE_soumission_v0.22.0.zip",
     f"{DEPOT}/depot-zenodo-v0220/TRIADE_soumission_v0.22.0.zip"),
    ("TRIADE_complet_v0.22.1.zip",
     f"{DEPOT}/depot-zenodo-v0221/TRIADE_complet_v0.22.1.zip"),
    ("TRIADE_presentation_v0.22.0.zip",
     f"{DEPOT}/TRIADE_presentation_v0.22.0.zip"),
]:
    vert(f"zenodo : {nom} md5 byte-byte",
         files_pub.get(nom) == md5_de(chemin))

nb = sum(1 for _, ok in R if ok)
print(f"\nLA VÉRIFICATION : {nb}/{len(R)} VERT, "
      f"{len(R) - nb} ROUGE")
sys.exit(0 if nb == len(R) else 1)
