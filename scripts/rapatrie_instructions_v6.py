#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrie_instructions_v6.py — LA VAGUE 6 (les six Qwen__20261116_* du
/instructions, déposées le 16/11 à 22:02-22:03) : rapatriement + LECTURE
INTÉGRALE imprimée (aucune exécution avant la lecture complète — la
discipline), ET le recoup byte-byte de la livraison vague 5 au coffre (le
manuscrit, les deux archives, les deux rapports, les empreintes, les dix
instructions archivées) + l'état de TRIADE-sauvegarde-git (métadonnées).
Lecture par le compte de service (LECTURE SEULE — la voie désignée).
"""
import hashlib
import io
import os
import pathlib

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SA = "/home/z/my-project/upload/physichong-4b3b7222b48c.json"
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
ARCHIVE = "1qqfk-yMNg3E5s1HVVeEkhmFceeDuPtNb"
SAUVEGARDE_GIT = "1YwYXkoSFC9GnnTgCK0FRT0GO-3hSxMix"  # triade-history.bundle
WORKLOG_ID = "1IjBk84S81ioBMASehROG3UsdJkO6JEBY"      # worklog.md

DEST = "/home/z/my-project/instructions-recu"
RECOUP = pathlib.Path("/home/z/my-project/livraison-vague5/recoup-coffre")
RECOUP.mkdir(parents=True, exist_ok=True)

creds = service_account.Credentials.from_service_account_file(
    SA, scopes=["https://www.googleapis.com/auth/drive"])
drive = build("drive", "v3", credentials=creds, cache_discovery=False)


def lister(parent):
    page, items = None, []
    while True:
        resp = drive.files().list(
            q=f"'{parent}' in parents and trashed = false",
            pageSize=200,
            fields=("nextPageToken, files(id, name, mimeType, size, "
                    "md5Checksum, modifiedTime)"),
            pageToken=page).execute()
        items += resp.get("files", [])
        page = resp.get("nextPageToken")
        if not page:
            break
    return items


def telecharger(fid, chemin):
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    with io.FileIO(chemin, "wb") as fh:
        t = MediaIoBaseDownload(fh, drive.files().get_media(fileId=fid))
        fini = False
        while not fini:
            _, fini = t.next_chunk()


def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def md5(chemin):
    return hashlib.md5(pathlib.Path(chemin).read_bytes()).hexdigest()


# ------------------------------------------------ 1. LA VAGUE 6 AU /instructions
print("=" * 78)
print("1. LA VAGUE 6 — les fichiers du /instructions (lecture intégrale)")
print("=" * 78)
v6 = [it for it in lister(INSTRUCTIONS)
      if it.get("mimeType") != "application/vnd.google-apps.folder"]
print(f"{len(v6)} fichiers au /instructions :")
for it in sorted(v6, key=lambda x: x["name"]):
    print(f"  {it['name']}  ({it['size']} o, mod={it['modifiedTime']})")

for it in sorted(v6, key=lambda x: x["name"]):
    chemin = os.path.join(DEST, it["name"])
    telecharger(it["id"], chemin)
    local_md5 = md5(chemin)
    recoup = "RECROUPÉ" if local_md5 == it.get("md5Checksum") else "ÉCART (!)"
    print(f"\n----- {it['name']} ({it['size']} o, md5 {recoup}) -----")
    print(pathlib.Path(chemin).read_text(encoding="utf-8"))

# --------------------------------------- 2. RECOUP de la livraison vague 5 (racine)
print("=" * 78)
print("2. LE RECOUP BYTE-BYTE DE LA LIVRAISON VAGUE 5 (racine du coffre)")
print("=" * 78)
racine = {it["name"]: it for it in lister(RACINE)
          if it.get("mimeType") != "application/vnd.google-apps.folder"}
attendus = {
    "TRIADE_manuscrit_v0.18.0.pdf":
        "/home/z/my-project/livraison-vague5/edition-v180/"
        "TRIADE_manuscrit_v0.18.0.pdf",
    "TRIADE_soumission_v0.18.0.zip":
        "/home/z/my-project/livraison-vague5/archives/"
        "TRIADE_soumission_v0.18.0.zip",
    "TRIADE_complet_v0.18.0.zip":
        "/home/z/my-project/livraison-vague5/archives/"
        "TRIADE_complet_v0.18.0.zip",
    "rapport-execution-vague5.txt":
        "/home/z/my-project/livraison-vague5/rapport-execution-vague5.txt",
    "rapport_verification_v0.18.0.txt":
        "/home/z/my-project/livraison-vague5/archives/soumission/"
        "rapport_verification_v0.18.0.txt",
    "empreintes_livrables.txt":
        "/home/z/my-project/livraison-vague5/archives/soumission/"
        "empreintes_livrables.txt",
}
rouges = 0
for nom, local in attendus.items():
    if nom not in racine:
        print(f"  [ROUGE] {nom} ABSENT de la racine du coffre")
        rouges += 1
        continue
    distant = RECOUP / nom
    telecharger(racine[nom]["id"], str(distant))
    if sha256(distant) == sha256(local):
        print(f"  [VERT] {nom} — sha256 IDENTIQUE au local "
              f"({racine[nom]['size']} o)")
    else:
        print(f"  [ROUGE] {nom} — sha256 DIVERGE du local !")
        rouges += 1

# --------------------------------- 3. RECOUP des DIX instructions archivées
print("=" * 78)
print("3. LE RECOUP DES DIX INSTRUCTIONS ARCHIVÉES (/ARCHIVE/instructions_20261116)")
print("=" * 78)
archives = {it["name"]: it for it in lister(ARCHIVE)
            if it.get("mimeType") != "application/vnd.google-apps.folder"}
dix = [n for n in archives if n.startswith("Qwen_text_20261116_")]
for nom in sorted(dix):
    local = pathlib.Path(DEST) / nom
    if not local.exists():
        print(f"  [ROUGE] {nom} : copie locale ABSENTE (instructions-recu/)")
        rouges += 1
        continue
    if md5(local) == archives[nom].get("md5Checksum"):
        print(f"  [VERT] {nom} — md5 archivé == md5 rapatrié avant exécution")
    else:
        print(f"  [ROUGE] {nom} — md5 DIVERGE")
        rouges += 1
rap = "rapport-execution-vague5.txt"
if rap in archives:
    local_rap = pathlib.Path(
        "/home/z/my-project/livraison-vague5/rapport-execution-vague5.txt")
    dist = RECOUP / "ARCHIVE-rapport-execution-vague5.txt"
    telecharger(archives[rap]["id"], str(dist))
    if sha256(dist) == sha256(local_rap):
        print(f"  [VERT] le rapport d'exécution aux côtés des instructions — "
              f"sha256 IDENTIQUE au local")
    else:
        print(f"  [ROUGE] le rapport d'exécution aux archives DIVERGE du local")
        rouges += 1
print(f"  → {len(dix)} instructions Qwen_text_* archivées au total")

# ---------------------------------------------- 4. L'ÉTAT DE LA SAUVEGARDE GIT
print("=" * 78)
print("4. TRIADE-sauvegarde-git (métadonnées seulement)")
print("=" * 78)
for it in lister("1YwYXkoSFC9GnnTgCK0FRT0GO-3hSxMix"):
    print(f"  {it['name']}  ({it.get('size', '?')} o, "
          f"mod={it.get('modifiedTime', '?')})")
wl = drive.files().get(fileId=WORKLOG_ID,
                       fields="name, size, modifiedTime").execute()
print(f"  worklog.md  ({wl.get('size', '?')} o, mod={wl.get('modifiedTime')})")

print("=" * 78)
print(f"BILAN DU RECOUP : "
      f"{'TOUT VERT' if rouges == 0 else str(rouges) + ' ROUGE'}")
