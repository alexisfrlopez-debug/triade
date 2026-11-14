#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA SONDE de l'état des miroirs à l'ouverture de la session
(la question du développeur : « je ne sais pas où trouver la ligne C de
l'atelier ») — AVANT de consigner la réponse, le labo vérifie que la
passation 290 est TENUE (GitHub, le bundle D141, les trois textes du
miroir Drive) : aucune dette n'est laissée derrière, jamais."""
import hashlib
import json
import pathlib
import urllib.request

from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
WORK = pathlib.Path("/home/z/my-project/work")
REPO = WORK / "triade"
ROOT = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
API = "https://www.googleapis.com/drive/v3"

svc_creds = service_account.Credentials.from_service_account_file(
    f"{UPLOAD}/physichong-4b3b7222b48c.json",
    scopes=["https://www.googleapis.com/auth/drive"])
svc = build("drive", "v3", credentials=svc_creds, cache_discovery=False)


def list_children(fid):
    out, token = [], None
    while True:
        params = {"q": f"'{fid}' in parents and trashed = false",
                  "pageSize": "200",
                  "fields": "nextPageToken,files(id,name,mimeType,size)"}
        if token:
            params["pageToken"] = token
        obj = svc.files().list(**params).execute()
        out += obj.get("files", [])
        token = obj.get("nextPageToken")
        if not token:
            return out


def retelecharger(fid):
    return svc.files().get_media(fileId=fid).execute()


racine = {c["name"]: c for c in list_children(ROOT)}
miroir = racine["TRIADE-sauvegarde-git"]
n1 = {c["name"]: c for c in list_children(miroir["id"])}
docs = {c["name"]: c for c in list_children(n1["docs"]["id"])}

print("=== LE MIROIR DRIVE (TRIADE-sauvegarde-git) ===")
print("racine du miroir :", sorted(n1.keys()))

# 1) le bundle courant : attendu == l'état 290
sha_local_290 = hashlib.sha256(
    (WORK / "triade-history-290.bundle").read_bytes()).hexdigest()
distant_bundle = retelecharger(n1["triade-history.bundle"]["id"])
sha_distant = hashlib.sha256(distant_bundle).hexdigest()
ok_bundle = sha_distant == sha_local_290
print(f"[{'VERT' if ok_bundle else 'ROUGE'}] triade-history.bundle "
      f"({len(distant_bundle):,} o) == l'état 290 local "
      f"({sha_local_290[:16]}…)")

# 2) D141 : le courant 288-ad9d2f5 versé à archives-bundles/
archives = {c["name"]: c for c in list_children(n1["archives-bundles"]["id"])}
print(f"[{'VERT' if any(n.startswith('triade-history-288-') for n in archives) else 'ROUGE'}]"
      f" D141 : triade-history-288-ad9d2f5.bundle à archives-bundles/"
      f" ({len(archives)} bundles archivés)")
courants = [n for n in archives
            if n.startswith("triade-history-288-")
            or n.startswith("triade-history-290-")]
if courants:
    print("   les courants 288/290 présents :", courants)

# 3) les trois textes
FICHIERS = {
    "worklog.md": (n1["worklog.md"]["id"], REPO / "worklog.md"),
    "docs/JOURNAL_TRAVAIL.md": (docs["JOURNAL_TRAVAIL.md"]["id"],
                                REPO / "docs" / "JOURNAL_TRAVAIL.md"),
    "OU-TROUVER-LES-LIVRABLES.md": (n1["OU-TROUVER-LES-LIVRABLES.md"]["id"],
                                    REPO / "OU-TROUVER-LES-LIVRABLES.md"),
}
for nom, (fid, chemin) in FICHIERS.items():
    local = chemin.read_bytes()
    distant = retelecharger(fid)
    vert = distant == local
    print(f"[{'VERT' if vert else 'ROUGE'}] {nom} "
          f"({len(local):,} o local / {len(distant):,} o au miroir) — "
          f"{'identique' if vert else 'DIVERGE (la 290 peut ne pas être passée)'}")

# 4) le coffre /test — l'atelier attendu
test = {c["name"]: c for c in list_children(racine["test"]["id"])}
print("\n=== LE COFFRE /test ===")
print("racine /test :", sorted(test.keys()))
if "TRIADE_gui_tous_runs_v1" in test:
    gui = {c["name"]: c for c in list_children(test["TRIADE_gui_tous_runs_v1"]["id"])}
    ateliers = [n for n in gui if n.startswith("atelier-campagne-d204-")]
    print("ateliers au coffre :", ateliers)
    for nom in ateliers:
        pieces = {c["name"] for c in list_children(gui[nom]["id"])}
        liv = retelecharger(
            [c for c in list_children(gui[nom]["id"])
             if c["name"] == "livraisons.csv"][0]["id"]).decode("utf-8")
        lignes = [l for l in liv.splitlines()
                  if l and not l.startswith("#") and not l.startswith("livraison,")]
        print(f"  {nom} : {len(pieces)} pièces, "
              f"{len(lignes)} ligne(s) de livraison : {lignes}")

print("\n[sonde] l'état des miroirs est établi")
