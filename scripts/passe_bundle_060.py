#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_060.py — LA PASSATION DU BUNDLE D141 pour le jalon 0.6.0 :
  1. le bundle triade-history-060-07d392e.bundle est déposé au MIROIR
     (TRIADE-sauvegarde-git/ — l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-051-3375e9b.bundle est ARCHIVÉ VERSIONNÉ
     dans archives-bundles/ (JAMAIS supprimé ni écrasé — D141) ;
  3. la copie déposée par erreur au dossier /test du développeur est RETIRÉE
     (la même pièce, md5 recoupé, vit au miroir — D143 : /test reste la file
     de livraison de la vague courante, pas un dépôt d'bundles).
Chaque geste ASSERTÉ ; md5 recoupés AVANT tout déplacement."""

import hashlib
import importlib.util
import json
import os
import sys
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "ds", os.path.join(REPO, "scripts", "drive_sync.py"))
ds = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ds)

BUNDLE = "triade-history-060-07d392e.bundle"
ANCIEN = "triade-history-051-3375e9b.bundle"
FOLD = "application/vnd.google-apps.folder"

tok = ds.get_access_token()


def api(chemin, method="GET", json_body=None):
    # NOTE Drive : addParents/removeParents/trashed sont des PARAMÈTRES DE
    # REQUÊTE (dans le chemin), jamais des champs du corps — un PATCH avec
    # corps retourne 200 SRI rien déplacer (la leçon du run v7, D143)
    req = urllib.request.Request(
        "https://www.googleapis.com/" + chemin, method=method,
        headers={"Authorization": f"Bearer {tok}"},
        data=json.dumps(json_body).encode() if json_body is not None else None)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return {"erreur": e.code, "corps": e.read()[:150].decode("utf-8", "replace")}


def lister(parent):
    return api("drive/v3/files?q=" + urllib.request.quote(
        f"'{parent}' in parents and trashed=false") +
        "&fields=files(id,name,mimeType,md5Checksum)&pageSize=200").get("files", [])


# -- 0. l'état AVANT (assertions) -------------------------------------------------
coffre = lister(ds.DRIVE_ROOT_ID)
miroir = next((f for f in coffre if f["name"] == "TRIADE-sauvegarde-git"), None)
assert miroir, "miroir introuvable"
racine_m = lister(miroir["id"])
ancien = next((f for f in racine_m if f["name"] == ANCIEN), None)
assert ancien, f"l'ancien courant {ANCIEN} introuvable au miroir"
archives = next((f for f in racine_m if f["name"] == "archives-bundles"), None)
assert archives, "archives-bundles/ introuvable"
deja = next((f for f in racine_m if f["name"] == BUNDLE), None)
deja_arch = next((f for f in lister(archives["id"]) if f["name"] == BUNDLE), None)
print(f"[état] ancien courant : {ANCIEN} (md5 {ancien.get('md5Checksum', '')[:8]}…)")

# -- 1. dépôt du 060 au miroir ----------------------------------------------------
chemin_local = os.path.join(REPO, "bundles-060", BUNDLE)
with open(chemin_local, "rb") as f:
    md5_local = hashlib.md5(f.read()).hexdigest()
if deja or deja_arch:
    cible = deja or deja_arch
    assert cible.get("md5Checksum") == md5_local, \
        f"{BUNDLE} existe déjà avec un md5 divergent — ABANDON"
    print(f"[1] {BUNDLE} déjà présent au miroir (md5 MATCH) — idempotent")
else:
    # dépôt multipart (mêmo que drive_livraison) : métadonnées + octets
    limite = "====triade060"
    meta = json.dumps({"name": BUNDLE, "parents": [miroir["id"]]})
    with open(chemin_local, "rb") as f:
        octets = f.read()
    corps = (f"--{limite}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n"
             f"{meta}\r\n--{limite}\r\nContent-Type: application/octet-stream\r\n\r\n"
             ).encode() + octets + f"\r\n--{limite}--".encode()
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files"
        "?uploadType=multipart&fields=id,md5Checksum",
        data=corps, method="POST",
        headers={"Authorization": f"Bearer {tok}",
                 "Content-Type": f"multipart/related; boundary={limite}"})
    with urllib.request.urlopen(req) as r:
        depose = json.loads(r.read())
    assert depose["md5Checksum"] == md5_local, "md5 divergent après dépôt"
    print(f"[1] déposé au miroir : {BUNDLE} (md5 {md5_local[:8]}… MATCH)")

# -- 2. l'ancien 051 archivé VERSIONNÉ --------------------------------------------
deja_la = any(f["name"] == ANCIEN for f in lister(archives["id"]))
if deja_la:
    print(f"[2] {ANCIEN} déjà archivé — idempotent")
else:
    rep = api(f"drive/v3/files/{ancien['id']}"
              f"?addParents={archives['id']}&removeParents={miroir['id']}",
              "PATCH", {})
    assert "erreur" not in rep, f"échec du déplacement : {rep}"
    apres = lister(miroir["id"])
    assert not any(f["name"] == ANCIEN for f in apres), "l'ancien reste au miroir"
    assert any(f["name"] == ANCIEN for f in lister(archives["id"])), \
        "l'ancien n'est pas à l'archive"
    print(f"[2] archivé versionné : {ANCIEN} → archives-bundles/ "
          f"(la racine ne porte que le courant)")

# -- 3. la copie erronée de /test RETIRÉE (md5 recoupé AVANT) ----------------------
test = next((f for f in coffre if f["name"] == "test"), None)
if test:
    copie = next((f for f in lister(test["id"]) if f["name"] == BUNDLE), None)
    if copie:
        assert copie.get("md5Checksum") == md5_local, \
            "la copie /test diverge du local — retrait refusé"
        miroir_ok = any(f["name"] == BUNDLE and f.get("md5Checksum") == md5_local
                        for f in lister(miroir["id"])) or deja or deja_arch
        assert miroir_ok, "la pièce canonique n'est pas au miroir — retrait refusé"
        rep = api(f"drive/v3/files/{copie['id']}?trashed=true", "PATCH", {})
        assert "erreur" not in rep, f"échec du retrait : {rep}"
        print(f"[3] copie /test retirée (la canonique vit au miroir, md5 recoupé)")
    else:
        print("[3] aucune copie à retirer de /test")

# -- 4. l'état APRÈS (recoupement) -------------------------------------------------
final = lister(miroir["id"])
courants = sorted(f["name"] for f in final if f["name"].endswith(".bundle")
                  and f["name"].startswith("triade-history-0"))
archives_finales = sorted(f["name"] for f in lister(archives["id"]))
print(f"[état] courants au miroir : {courants}")
print(f"[état] archives-bundles/ : {archives_finales}")
assert BUNDLE in courants and ANCIEN not in courants, "état final divergent"
print("PASSATION D141 TERMINÉE")
