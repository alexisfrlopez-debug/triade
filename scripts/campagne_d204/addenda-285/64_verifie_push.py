#!/usr/bin/env python3
"""TRIADE — lire le relais /Tokens du coffre (SANS JAMAIS IMPRIMER le jeton)
et vérifier l'état du dépôt GitHub (le push de l'Entrée 284 a-t-il vécu ?)."""
import json
import pathlib
import urllib.request
from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
ROOT = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"

creds = service_account.Credentials.from_service_account_file(
    f"{UPLOAD}/physichong-4b3b7222b48c.json",
    scopes=["https://www.googleapis.com/auth/drive"],
)
svc = build("drive", "v3", credentials=creds, cache_discovery=False)

def list_folder(folder_id):
    items, token = [], None
    while True:
        res = svc.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken,files(id,name,mimeType,size,modifiedTime)",
            pageSize=100, pageToken=token,
        ).execute()
        items.extend(res.get("files", []))
        token = res.get("nextPageToken")
        if not token:
            return items

# trouver le dossier /Tokens puis le fichier jeton
tokens_dir = None
for it in list_folder(ROOT):
    if it["name"] == "Tokens" and it["mimeType"] == "application/vnd.google-apps.folder":
        tokens_dir = it["id"]
        break
if not tokens_dir:
    print("[!] dossier /Tokens introuvable")
    raise SystemExit(1)

candidats = list_folder(tokens_dir)
for it in candidats:
    print(f"[Tokens] {it['name']}  ({it.get('size','?')} o, modifié {(it.get('modifiedTime') or '?')[:19]})")

# le fichier jeton GIT (token_git.txt, 40 o — le ghp_)
import re
meilleur = None
for it in candidats:
    if it["mimeType"] == "application/vnd.google-apps.folder":
        continue
    if it["name"] == "token_git.txt":
        meilleur = it
        break
if not meilleur:
    print("[!] token_git.txt introuvable dans /Tokens")
    raise SystemExit(1)

req = svc.files().get_media(fileId=meilleur["id"]).execute()
corps = req.decode("utf-8", errors="replace")
m = re.search(r"(ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9_]+)", corps)
if not m:
    print(f"[!] pas de jeton lisible dans {meilleur['name']} (longueur {len(corps)})")
    raise SystemExit(1)
jeton = m.group(1)
print(f"[OK] jeton lu dans « {meilleur['name']} » (préfixe {jeton[:4]}…, jamais imprimé)")

# l'état du dépôt GitHub
req = urllib.request.Request(
    "https://api.github.com/repos/alexisfrlopez-debug/triade/commits?per_page=3",
    headers={"Authorization": f"Bearer {jeton}",
             "Accept": "application/vnd.github+json",
             "User-Agent": "triade-labo"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    for c in data:
        msg = c["commit"]["message"].split("\n")[0]
        print(f"[GitHub] {c['sha'][:9]} | {c['commit']['committer']['date']} | {msg[:120]}")
except Exception as e:
    print(f"[!] l'appel GitHub a échoué : {e}")
