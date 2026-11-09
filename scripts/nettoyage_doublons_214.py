#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le nettoyage des doublons — la corbeille du dépôt initial envoyait un
corps vide ({} au lieu de {"trashed": true}) : les ANCIENS fichiers
demeuraient. Ici : chaque ancien est réellement mis à la corbeille,
recoupé par son id."""
import json
import sys
import urllib.request

sys.path.insert(0, "/home/z/my-project/scripts")
from drive_api import obtenir_token  # noqa: E402

TOK = obtenir_token()

# les ANCIENS fichiers à mettre à la corbeille (ids du manifeste run 9)
ANCIENS = [
    ("1QOdsTmRGe8AA8LChAivNQupN6WWEQcDS", "kit-loupe.zip racine (dev.9)"),
    ("1LOMnQMWu1_CpRZ3gyR4qPGBVYvI3Vxcs", "LISEZMOI-loupe.txt racine (dev.9)"),
    ("1Q28-cq5TVuaVNGMroT3EkuuN-DrCkF_A", "preuves-loupe/LISEZMOI-preuves.txt (dev.9)"),
    ("1LW5UyFaSPDziI1gMVhn5WmnPVLt3fW9s", "index livraisons (ancien)"),
    ("1WK5OOuMOFFoUj3PevftZo3pHIFKQx7zu", "index preuves (ancien)"),
    # le dossier preuves-loupe DANS kit-loupe (les preuves sont archivées
    # en preuves-run-loupe-dev9/) — id retrouvé ci-dessous
]

import urllib.parse


def liste(fid, nom=None):
    q = f"'{fid}' in parents and trashed = false"
    if nom:
        q += f" and name = '{nom}'"
    url = ("https://www.googleapis.com/drive/v3/files/?" +
           urllib.parse.urlencode({"q": q, "fields": "files(id,name)",
                                   "pageSize": 50}))
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOK}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r).get("files", [])


TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
kit_loupe = liste(TEST, "kit-loupe")[0]
preuves_kit = liste(kit_loupe["id"], "preuves-loupe")
for p in preuves_kit:
    ANCIENS.append((p["id"], "kit-loupe/preuves-loupe (archivé en dev9)"))


def corbeille_vraie(fid):
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{fid}",
        method="PATCH", data=json.dumps({"trashed": True}).encode(),
        headers={"Authorization": f"Bearer {TOK}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r).get("trashed") is True


for fid, nom in ANCIENS:
    ok = corbeille_vraie(fid)
    print(f"  {'✓' if ok else '✗'} corbeille : {nom}")

# vérification finale : plus AUCUN doublon à la racine
racine = {}
for f in liste(TEST):
    racine.setdefault(f["name"], []).append(f)
doublons = {n: len(v) for n, v in racine.items() if len(v) > 1}
print("DOUBLONS RACINE :", doublons or "AUCUN")
dans_kit = [f["name"] for f in liste(kit_loupe["id"])]
print("KIT-LOUPE :", dans_kit)
