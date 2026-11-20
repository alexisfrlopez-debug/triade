#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""publier_zenodo_v0195.py — LE GESTE DU MAÎTRE : la publication du brouillon
v0.19.5 (24382460) du concept 10.5281/zenodo.24367343 — à la commande
explicite « mets a jour les miroirs ». La voie est vérifiée AVANT le geste
(l'état du brouillon, la version v0.19.5 aux métadonnées, les TROIS fichiers
recoupés md5 byte-byte aux pièces locales), le geste PUIS la vérification
fraîche (le DOI de version minté, le concept DOI résolvant sur la v0.19.5,
l'état done, la page anonyme)."""
import hashlib
import json
import sys
import urllib.error
import urllib.request

TOK = open("/home/z/my-project/keys/zenodo.txt").read().strip()
DRAFT = "https://zenodo.org/api/deposit/depositions/24382460"
CONCEPT = "10.5281/zenodo.24367343"

FICHIERS_LOCAUX = {
    "TRIADE_soumission_v0.19.5.zip":
        "/home/z/my-project/depot/TRIADE_soumission_v0.19.5.zip",
    "TRIADE_complet_v0.19.5.zip":
        "/home/z/my-project/depot/TRIADE_complet_v0.19.5.zip",
    "TRIADE_presentation_v0.19.5_20261120.zip":
        "/home/z/my-project/depot/scripts/vague7/"
        "TRIADE_presentation_v0.19.5_20261120.zip",
}


def api(method, url, body=None, avec_jeton=True):
    headers = {}
    if avec_jeton:
        headers["Authorization"] = f"Bearer {TOK}"
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method,
                                 headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def md5_de(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


# (1) LA VOIE VÉRIFIÉE AVANT LE GESTE
st, body = api("GET", DRAFT)
assert st == 200, f"brouillon illisible : HTTP {st}"
d = json.loads(body)
etat = d.get("state")
version = d.get("metadata", {}).get("version")
assert etat in ("unsubmitted", "draft"), f"état inattendu : {etat}"
assert version == "v0.19.5", f"version inattendue : {version}"
print(f"[1] le brouillon 24382460 : état {etat}, version {version}")
fichiers = {f["filename"]: f.get("checksum", "md5:").split("md5:")[-1]
            for f in d.get("files", [])}
assert len(fichiers) == 3, f"fichiers inattendus : {list(fichiers)}"
for nom, chemin in FICHIERS_LOCAUX.items():
    assert nom in fichiers, f"absent du brouillon : {nom}"
    assert fichiers[nom] == md5_de(chemin), f"md5 divergent : {nom}"
    print(f"    recoupé md5 byte-byte : {nom}")
print(f"[1] la voie est VÉRIFIÉE — les trois fichiers, la version, l'état")

# (2) LE GESTE — la publication au commandement du maître
st, body = api("POST", f"{DRAFT}/actions/publish")
if st >= 400:
    print(f"[2] PUBLICATION : HTTP {st}")
    print(body.decode(errors="replace")[:500])
    sys.exit(1)
d = json.loads(body)
doi, concept, etat = d.get("doi"), d.get("conceptdoi"), d.get("state")
print(f"[2] PUBLICATION : HTTP {st}")
print(f"    DOI de version : {doi}")
print(f"    concept DOI    : {concept}")
print(f"    état           : {etat}")
assert etat == "done", f"état inattendu après publication : {etat}"
assert concept == CONCEPT, f"concept inattendu : {concept}"
assert doi and doi.startswith("10.5281/zenodo."), f"DOI anormal : {doi}"

# (3) LA VÉRIFICATION FRAÎCHE — le bord public anonyme
import time
time.sleep(4)
rid = doi.split("zenodo.")[-1]
st, body = api("GET", f"https://zenodo.org/api/records/{rid}", avec_jeton=False)
assert st == 200, f"la page publique du record : HTTP {st}"
r = json.loads(body)
assert r.get("doi") == doi and r.get("conceptdoi") == CONCEPT, "DOI divergents"
assert r["metadata"].get("version") == "v0.19.5", "version divergente"
files_pub = {f["key"]: f["checksum"].split("md5:")[-1]
             for f in r.get("files", [])}
assert files_pub == fichiers, "fichiers divergents au bord public"
print(f"[3] le bord public anonyme : HTTP 200, la v0.19.5 vivante")
for nom, md5 in sorted(files_pub.items()):
    print(f"    - {nom} (md5 {md5[:8]}… recoupé égal)")
st, body = api("GET",
               "https://zenodo.org/api/records?q=concepts.recid:%22"
               f"{CONCEPT.split('zenodo.')[-1]}%22&all_versions=true&size=5",
               avec_jeton=False)
if st == 200:
    hits = json.loads(body).get("hits", {}).get("hits", [])
    versions = sorted((h["metadata"].get("version"), h["id"])
                      for h in hits)
    print(f"[3] le concept au bord public : "
          f"{[v for v, _ in versions]} — la tête = {versions[-1]}")
print("\nLE GESTE EST VÉCU — la v0.19.5 publiée, les trois bords verts.")
