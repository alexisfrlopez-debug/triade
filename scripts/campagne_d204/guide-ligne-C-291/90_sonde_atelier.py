#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA SONDE de l'atelier au coffre : où vit le livre 013520,
quelles lignes porte livraisons.csv — LA LIGNE C (C-loupe-01-it1) est-elle
toujours absente ? (la question du développeur : « je ne sais pas où
trouver la ligne C de l'atelier »)."""
import pathlib

from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
ROOT = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"

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


def parcourir(fid, prefix="", profondeur=0):
    if profondeur > 4:
        return
    for c in list_children(fid):
        chemin = f"{prefix}/{c['name']}"
        if c["mimeType"] == "application/vnd.google-apps.folder":
            print(f"[DIR ] {chemin}")
            if c["name"].startswith("atelier-campagne-d204-"):
                pieces = {p["name"] for p in list_children(c["id"])}
                print(f"      └─ L'ATELIER : {sorted(pieces)}")
                for p in list_children(c["id"]):
                    if p["name"] == "livraisons.csv":
                        liv = svc.files().get_media(
                            fileId=p["id"]).execute().decode("utf-8")
                        lignes = [l for l in liv.splitlines()
                                  if l and not l.startswith("#")
                                  and not l.startswith("livraison,")]
                        print(f"      └─ livraisons.csv : "
                              f"{len(lignes)} ligne(s) :")
                        for l in lignes:
                            print(f"           {l}")
                        print(f"      └─ LA LIGNE C "
                              f"{'PRÉSENTE' if any(l.startswith('C-') for l in lignes) else 'ABSENTE (attendue à la main du développeur)'}")
            else:
                parcourir(c["id"], chemin, profondeur + 1)


racine = {c["name"]: c for c in list_children(ROOT)}
test = {c["name"]: c for c in list_children(racine["test"]["id"])}
print("=== /test/Nouveau run (l'arbre de l'atelier) ===")
parcourir(test["Nouveau run"]["id"], "/test/Nouveau run")
