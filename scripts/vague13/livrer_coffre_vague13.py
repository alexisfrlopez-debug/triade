#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_coffre_vague13.py — LA LIVRAISON AU COFFRE (la vague 13, la
release v0.23.0) : LE COMPLET TRIADE_complet_v0.23.0.zip + LE RAPPORT DE
VÉRIFICATION v0.23.0 + LE MANIFESTE des empreintes à la RACINE — le
tout RECOUPÉ byte-byte par re-téléchargement ; LES PIÈCES DE SESSION au
/test (le rapport de vérification, le manifeste, les rapports des six
ateliers de la vague) recoupées ; LES TROIS PACKS v0.23.0 au /livrables
ET les packs v0.22.1 SUPERSEDÉS au lot ARCHIVE/supersede-packs-20261122
; LES RAPPORT+MANIFESTE v0.22.1 de la racine SUPERSEDÉS au lot
ARCHIVE/supersede-racine-vague13-20261122 ; L'ARCHIVAGE DES INSTRUCTIONS
au coffre en deux étapes (le retrait du /instructions PUIS l'ajout au
dossier ARCHIVE/instructions_vague13_20261122 — l'appel combiné refusé
pour les pièces du déposant, l'écart nommé aux vagues 10-12) ; LE
/instructions LAISSÉ VIDE, vérifié. Les écritures au RELAIS (le compte
de service demeure LECTEUR seul — D101), les lectures et le recoup au
SERVICE (le bord froid) — la voie du module drive_sa_v220.py."""
import hashlib
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, "/home/z/my-project/depot/scripts/vague11")
import drive_sa_v220 as DS  # noqa: E402
from drive_sa_v220 import trouve  # noqa: E402

REPO = pathlib.Path("/home/z/my-project/depot")
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
LIVRABLES = "1wF0p0g-OPdnL7fgnNsJb6D1rXhtyHqIZ"
INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
ARCHIVE = "1uJ5yU7ma5dYQM1GuWzm9Fx1I1U3Ywepr"
V13 = REPO / "scripts" / "vague13"


def televerse_robuste(chemin, parent, essais=5):
    """LE TÉLÉVERSEMENT REPRENABLE (le 308 « Resume Incomplete » est LA
    RÉPONSE INTERMÉDIAIRE NORMALE — LE RANGE du 308 LU, l'envoi repris à
    l'octet près, PUIS LE RECOUP byte-byte au compte de service)."""
    p = pathlib.Path(chemin)
    data = p.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    fid = trouve(p.name, parent)
    for i in range(essais):
        try:
            if fid:
                url = (f"{DS.UPLOAD}/files/{fid}?uploadType=media"
                       f"&supportsAllDrives=true")
                req = urllib.request.Request(
                    url, data=data, method="PATCH",
                    headers={**DS.hdr("relais"),
                             "Content-Type": "application/octet-stream"})
                with urllib.request.urlopen(req, timeout=900) as r:
                    assert r.status == 200, f"mise à jour : HTTP {r.status}"
                print(f"  [mis à jour] {p.name} [{len(data):,} o]")
            else:
                url = (f"{DS.UPLOAD}/files?uploadType=resumable"
                       f"&supportsAllDrives=true")
                meta = json.dumps({"name": p.name,
                                   "parents": [parent]}).encode()
                req = urllib.request.Request(
                    url, data=meta, method="POST",
                    headers={**DS.hdr("relais"),
                             "Content-Type": "application/json",
                             "X-Upload-Content-Length": str(len(data)),
                             "X-Upload-Content-Type":
                                 "application/octet-stream"})
                with urllib.request.urlopen(req, timeout=120) as r:
                    loc = r.headers["Location"]
                pos, chunk = 0, 4 * 1024 * 1024
                while pos < len(data):
                    bout = data[pos:pos + chunk]
                    fin = pos + len(bout) - 1
                    req = urllib.request.Request(
                        loc, data=bout, method="PUT",
                        headers={"Content-Range":
                                 f"bytes {pos}-{fin}/{len(data)}"})
                    try:
                        with urllib.request.urlopen(req,
                                                    timeout=900) as r:
                            if r.status in (200, 201):
                                fid = json.loads(r.read())["id"]
                    except urllib.error.HTTPError as e:
                        if e.code == 308:
                            plage = e.headers.get("Range", "")
                            if "-" in plage:
                                pos = int(plage.split("-")[1]) + 1
                                continue
                            raise
                        raise
                    pos = fin + 1
                print(f"  [téléversé] {p.name} [{len(data):,} o]")
            st, body = DS.api("GET", f"/files/{fid}",
                              {"alt": "media", "supportsAllDrives": "true"})
            if st != 200 or body != data:
                raise SystemExit(f"RECOUP ÉCHOUÉ : {p.name}")
            print(f"  VERT {p.name} recoupé byte-byte (md5 {md5[:8]}…)")
            return fid
        except urllib.error.HTTPError as e:
            if e.code in (308, 500, 502, 503, 504) and i + 1 < essais:
                print(f"  [reprise] {p.name} : HTTP {e.code} "
                      f"({i + 1}/{essais}) — la session relancée")
                time.sleep(10)
                continue
            raise
    raise SystemExit(f"ÉCHEC {p.name} après {essais} essais")


def deplacer(fid, nouveau_parent):
    """le déplacement au relais (l'ancien parent retiré)."""
    req = urllib.request.Request(
        f"{DS.API}/files/{fid}?addParents={nouveau_parent}"
        f"&removeParents="
        f"{RACINE if nouveau_parent != RACINE else LIVRABLES}"
        f"&supportsAllDrives=true",
        method="PATCH", data=b"{}",
        headers={**DS.hdr("relais"), "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        assert r.status in (200, 204), f"déplacement : HTTP {r.status}"


def creer_dossier(nom, parent):
    req = urllib.request.Request(
        f"{DS.API}/files?supportsAllDrives=true", method="POST",
        data=json.dumps({"name": nom,
                         "mimeType": "application/vnd.google-apps.folder",
                         "parents": [parent]}).encode(),
        headers={**DS.hdr("relais"), "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())["id"]


def id_dossier(nom, parent):
    st, body = DS.api(
        "GET", "/files",
        {"q": f"name = '{nom}' and '{parent}' in parents "
              "and trashed=false and mimeType="
              "'application/vnd.google-apps.folder'",
         "fields": "files(id,name)", "supportsAllDrives": "true",
         "includeItemsFromAllDrives": "true"})
    d = json.loads(body).get("files", [])
    return d[0]["id"] if d else None


# ---- (1) LA RACINE --------------------------------------------------------
print("[1] LA RACINE : le complet, le rapport, le manifeste")
RACINE_PIECES = [
    REPO / "depot-zenodo-v0230" / "TRIADE_complet_v0.23.0.zip",
    REPO / "rapport_verification_v0.23.0.txt",
    V13 / "empreintes_livrables_v0.23.0.txt",
]
for p in RACINE_PIECES:
    televerse_robuste(p, RACINE)

# les pièces v0.22.1 de la racine SUPERSEDÉES au lot
lot_racine = id_dossier("supersede-racine-vague13-20261122", ARCHIVE) \
    or creer_dossier("supersede-racine-vague13-20261122", ARCHIVE)
for nom in ("rapport_verification_v0.22.1.txt",
            "empreintes_livrables_v0.22.1.txt"):
    fid = trouve(nom, RACINE)
    if fid:
        deplacer(fid, lot_racine)
        print(f"  [supersédé racine → ARCHIVE] {nom}")

# ---- (2) LE /test ---------------------------------------------------------
print("[2] LE /test : les pièces de session de la vague 13")
TEST_PIECES = [
    REPO / "rapport_verification_v0.23.0.txt",
    V13 / "empreintes_livrables_v0.23.0.txt",
    REPO / "atelier-ghash-0g3400vql" / "rapport-ghash.txt",
    REPO / "atelier-requalification-q8kugkpdu" /
    "rapport-requalification.txt",
    REPO / "atelier-hcgp3-ay6zuzm8o" / "rapport-ventilation.txt",
    REPO / "atelier-ajouter-v3-5nwnwoceo" / "rapport-ajouter-v3.txt",
    REPO / "atelier-purge-v13-h66o54pjd" / "rapport-purge-v13.txt",
    REPO / "atelier-generation-v0230-ylrzmlbn8" / "rapport-generation.txt",
]
for p in TEST_PIECES:
    televerse_robuste(p, TEST)

# ---- (3) LE /livrables : les trois packs, les v0.22.1 supersédés ---------
print("[3] LE /livrables : les trois packs v0.23.0")
for p in (REPO / "depot-zenodo-v0230" / "TRIADE_soumission_v0.23.0.zip",
          REPO / "depot-zenodo-v0230" / "TRIADE_complet_v0.23.0.zip",
          REPO / "TRIADE_presentation_v0.23.0.zip"):
    televerse_robuste(p, LIVRABLES)

lot_packs = id_dossier("supersede-packs-20261122", ARCHIVE) \
    or creer_dossier("supersede-packs-20261122", ARCHIVE)
for nom in ("TRIADE_soumission_v0.22.1.zip",
            "TRIADE_complet_v0.22.1.zip",
            "TRIADE_presentation_v0.22.1.zip"):
    fid = trouve(nom, LIVRABLES)
    if fid:
        deplacer(fid, lot_packs)
        print(f"  [supersédé livrables → ARCHIVE] {nom}")

# ---- (4) L'ARCHIVAGE DES INSTRUCTIONS (le geste en deux étapes) ----------
print("[4] LES INSTRUCTIONS : le retrait du /instructions, l'archive au coffre")
dossier_arch = id_dossier("instructions_vague13_20261122", ARCHIVE) \
    or creer_dossier("instructions_vague13_20261122", ARCHIVE)
INSTRACTIONS = [
    ("17dmSLE17Do6iBK28-5Yj68ClW04AAmvM",
     "Qwen__20261121_0g3400vql.txt"),
    ("111SI2KO3AnN6e9itzfT4PdkR7_h87hQg",
     "Qwen__20261121_q8kugkpdu.txt"),
    ("18Dc5QnnK7lZu7dwAbXcIjI77rE2S7GtD",
     "Qwen__20261121_5nwnwoceo.txt"),
    ("15bY1-pQmzdDBuSRzhStbXR4Rru51NwTr",
     "Qwen__20261121_ay6zuzm8o.txt"),
    ("1xH3ELILigsL3_Do0podju5d8JfyE_kWZ",
     "Qwen__20261121_ylrzmlbn8.txt"),
    ("12XLoG71xan5JEe1PaBpci5OJ46l2V7-Z",
     "Qwen__20261121_h66o54pjd.txt"),
]
# (a) l'ajout au dossier ARCHIVE du coffre (les pièces du dépôt, recoupées)
for _, nom in INSTRACTIONS:
    televerse_robuste(REPO / "ARCHIVE" / "instructions_vague13_20261122" /
                      nom, dossier_arch)
# (b) le retrait du /instructions (la mise à la corbeille au relais)
for fid, nom in INSTRACTIONS:
    req = urllib.request.Request(
        f"{DS.API}/files/{fid}?supportsAllDrives=true",
        method="PATCH", data=json.dumps({"trashed": True}).encode(),
        headers={**DS.hdr("relais"), "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        assert r.status in (200, 204), f"retrait {nom} : HTTP {r.status}"
    print(f"  [retiré du /instructions] {nom}")

# ---- (5) LE /instructions DEMEURÉ VIDE ------------------------------------
st, body = DS.api(
    "GET", "/files",
    {"q": f"'{INSTRUCTIONS}' in parents and trashed=false",
     "fields": "files(id,name)", "supportsAllDrives": "true",
     "includeItemsFromAllDrives": "true", "pageSize": 50})
restants = json.loads(body).get("files", [])
print(f"[5] le /instructions : {len(restants)} fichier(s) restant(s)"
      + (f" — {restants}" if restants else " — VIDE, vérifié"))
if restants:
    raise SystemExit("LE /instructions N'EST PAS VIDE")
print("[livraison v13] TOUT VERT — la racine, le /test, le /livrables, "
      "l'archive des instructions, le /instructions vide")
