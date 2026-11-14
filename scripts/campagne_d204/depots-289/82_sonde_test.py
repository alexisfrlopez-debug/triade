#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA SONDE du /test après la commande du développeur (« vérifie les
dépôts dans /test puis go pour la suite ») : l'arborescence entière sauvée, le
DIFF contre l'état 288 (la racine attendue à 12 entrées, nommée), et TOUT ce
qui est né après le dernier geste du labo (le LISEZMOI-NETTOYAGE posé à la
288) — les dépôts de la main nommés AVANT tout recoup."""
import pathlib
from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
TEST_FOLDER = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
OUT = pathlib.Path("/home/z/my-project/scripts/82_arborescence_test.txt")

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
            fields="nextPageToken,files(id,name,mimeType,size,createdTime,modifiedTime)",
            pageSize=200, orderBy="name", pageToken=token,
        ).execute()
        items.extend(res.get("files", []))
        token = res.get("nextPageToken")
        if not token:
            return items

lignes = []
recents = []
marqueur_nettoyage = None  # le bornage : le LISEZMOI-NETTOYAGE, dernier geste 288

def walk(folder_id, path):
    global marqueur_nettoyage
    for it in list_folder(folder_id):
        p = f"{path}/{it['name']}"
        ne = (it.get("createdTime") or "?")[:19]
        if it["name"] == "LISEZMOI-NETTOYAGE-TEST-20261114.txt" and not path:
            marqueur_nettoyage = ne
        if it["mimeType"] == "application/vnd.google-apps.folder":
            lignes.append(f"[DIR ] {p}  (né {ne})")
            walk(it["id"], p)
        else:
            size = int(it.get("size", 0) or 0)
            ligne = (f"[FILE] {p}  ({size} o, né {ne}, modifié "
                     f"{(it.get('modifiedTime') or '?')[:19]})  [id={it['id']}]")
            lignes.append(ligne)

root = svc.files().get(fileId=TEST_FOLDER, fields="id,name").execute()
lignes.append(f"[RACINE] {root['name']} (id {TEST_FOLDER})")
walk(TEST_FOLDER, "")
OUT.write_text("\n".join(lignes), encoding="utf-8")
print(f"[OK] {len(lignes)} lignes — arborescence sauvée : {OUT}")

# ---- la racine contre l'attendu 288 --------------------------------------------
ATTENDU_288 = {
    "Nouveau run", "archives-livraisons", "archives-preuves",
    "LISEZMOI-CORRECTIF-ENCODAGE.txt", "LISEZMOI-GUI-TOUS-RUNS.txt",
    "LISEZMOI-KITS-UNITES-D204.txt", "LISEZMOI-campagne-GUI.txt",
    "LISEZMOI-NETTOYAGE-TEST-20261114.txt",
    "TRIADE-1CLIC-CAMPAGNE-D204-v3.bat",
    "TRIADE_gui_campagne_v1_CORRECTIF-encodage.zip",
    "TRIADE_gui_tous_runs_v1.zip",
}
racine_noms = {c["name"] for c in list_folder(TEST_FOLDER)}
print(f"\n===== LA RACINE ({len(racine_noms)} entrées) =====")
for n in sorted(racine_noms):
    marque = "  [DEMANDE 288]" if n not in ATTENDU_288 else ""
    print(f"  {n}{marque}")
nouveaux_racine = racine_noms - ATTENDU_288
perdus_racine = ATTENDU_288 - racine_noms
print(f"  → NEUFS à la racine : {sorted(nouveaux_racine) or 'aucun'}")
print(f"  → DISPARUS : {sorted(perdus_racine) or 'aucun'}")

# ---- tout ce qui est né après le marqueur 288 -----------------------------------
bornage = (marqueur_nettoyage or "2026-11-14T13:31")[:16]
print(f"\n===== LE BORNAGE : le LISEZMOI-NETTOYAGE né {bornage} =====")
print("\n===== NÉS APRÈS le bornage (les dépôts de la main) =====")
compte = 0
for l in lignes:
    if l.startswith(("[DIR ", "[FILE]")):
        ne = l.split("né ")[1][:16] if "né " in l else ""
        if ne and ne > bornage:
            print(l)
            compte += 1
print(f"  → {compte} pièces neuves après le bornage")
