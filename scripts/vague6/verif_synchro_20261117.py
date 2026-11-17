#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verif_synchro_20261117.py — Vérification LECTURE SEULE de la synchro
git ↔ Drive du coffre TRIADE (demande du développeur, 17/11/2026).

Discipline respectée :
  - compte de service physichong : LECTURE SEULE (lister, télécharger) ;
  - AUCUNE écriture au coffre, AUCUN déplacement, AUCUNE suppression ;
  - aucune VALEUR de jeton affichée — le /Tokens n'est listé qu'en
    métadonnées (noms, tailles, dates).
Vérifie :
  1. la racine du coffre et les dossiers clés (/instructions, /test,
     TRIADE-sauvegarde-git, archives-bundles, /Tokens) ;
  2. triade-history.bundle : téléchargé puis recoupé au md5 servi par
     Drive (le git bundle verify se fait après, côté shell) ;
  3. worklog.md : téléchargé puis recoupé au md5 Drive ;
  4. l'état du /instructions (vagues 5 et 6 — qu'y reste-t-il ?).
"""
import hashlib
import io
import os
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SA_KEY = "/home/z/my-project/upload/physichong-4b3b7222b48c.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]

RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
INSTRUCTIONS = None      # trouvé au listing de la racine
TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
SAUVEGARDE = "1ZzvJjLlGyVW4YKnXWdAgZO0IjFETKOZY"   # TRIADE-sauvegarde-git
ARCHIVES_BUNDLES = "1D2MJl2_1lQbDU6oUWjun6rLyS-RrKle9"
DOSSIER_TOKENS = "1EMxwHKkkfKROjFsHhu4vpKZpgqW-rgZL"
BUNDLE_ID = "1YwYXkoSFC9GnnTgCK0FRT0GO-3hSxMix"     # triade-history.bundle
WORKLOG_ID = "1IjBk84S81ioBMASehROG3UsdJkO6JEBY"    # worklog.md

DEST = "/tmp/verif_synchro"
ROUGES = 0


def coup(rouge, message):
    global ROUGES
    if rouge:
        ROUGES += 1
    print(f"  [{'ROUGE' if rouge else 'VERT'}] {message}")


def md5_local(chemin):
    h = hashlib.md5()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def lister(drive, dossier, titre, filtre=None):
    page, items = None, []
    while True:
        resp = drive.files().list(
            q=f"'{dossier}' in parents and trashed = false",
            pageSize=200,
            fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)",
            pageToken=page).execute()
        items += resp.get("files", [])
        page = resp.get("nextPageToken")
        if not page:
            break
    print(f"\n=== {titre} : {len(items)} éléments ===")
    for it in sorted(items, key=lambda x: x["name"]):
        if filtre and not filtre(it):
            continue
        t = it.get("mimeType", "")
        badge = "DOSSIER" if t == "application/vnd.google-apps.folder" else "fichier"
        print(f"  [{badge}] {it['name']}  "
              f"(size={it.get('size', '-')}, mod={it.get('modifiedTime', '-')})")
    return items


def telecharger(drive, file_id, chemin, attendu_md5, attendu_nom):
    meta = drive.files().get(fileId=file_id,
                             fields="name, size, md5Checksum, modifiedTime").execute()
    demande = drive.files().get_media(fileId=file_id)
    with io.FileIO(chemin, "wb") as fh:
        telechargeur = MediaIoBaseDownload(fh, demande)
        fini = False
        while not fini:
            _, fini = telechargeur.next_chunk()
    ok = md5_local(chemin) == (attendu_md5 or meta.get("md5Checksum"))
    coup(not ok,
         f"{attendu_nom} téléchargé : md5 local == md5 servi par Drive "
         f"({meta.get('md5Checksum', '')[:12]}…, "
         f"{int(meta.get('size', 0)):,} o, mod {meta.get('modifiedTime', '?')})"
         .replace(",", " "))
    return meta


def main():
    creds = service_account.Credentials.from_service_account_file(SA_KEY,
                                                                  scopes=SCOPES)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    os.makedirs(DEST, exist_ok=True)

    # ---- 1. la racine du coffre
    racine = lister(drive, RACINE, "RACINE DU COFFRE (TRIADE)")
    par_nom = {}
    for it in racine:
        par_nom[it["name"].strip().lower()] = it

    # ---- 2. /instructions (l'état des vagues 5 et 6)
    instr = par_nom.get("instructions")
    if instr:
        fichiers = lister(drive, instr["id"], "/instructions")
        noms = sorted(f["name"] for f in fichiers
                      if f.get("mimeType") != "application/vnd.google-apps.folder")
        v5 = [n for n in noms if n.startswith("Qwen_text_")]
        v6 = [n for n in noms if n.startswith("Qwen__20261116_")]
        archives = [f["name"] for f in fichiers
                    if f.get("mimeType") == "application/vnd.google-apps.folder"]
        print(f"\n  --> vague 5 restante au /instructions : {len(v5)} fichier(s)")
        for n in v5:
            print(f"        {n}")
        print(f"  --> vague 6 restante au /instructions : {len(v6)} fichier(s)")
        for n in v6:
            print(f"        {n}")
        print(f"  --> sous-dossiers : {archives}")
        if any(n.lower() == "qwen__20261116_bqh4qlrqj.txt" for n in noms):
            print("  --> bqh4qlrqj (exécutée, archivable) TOUJOURS au /instructions")
        else:
            print("  --> bqh4qlrqj (exécutée) ABSENTE du /instructions "
                  "(archivée par le développeur ?)")
    else:
        coup(True, "dossier /instructions INTROUVABLE à la racine")

    # ---- 3. TRIADE-sauvegarde-git + archives-bundles
    lister(drive, SAUVEGARDE, "TRIADE-sauvegarde-git")
    lister(drive, ARCHIVES_BUNDLES, "archives-bundles")

    # ---- 4. /Tokens : métadonnées SEULEMENT (aucune valeur)
    lister(drive, DOSSIER_TOKENS, "/Tokens (métadonnées seules — jamais affichées)")

    # ---- 5. /test (la campagne)
    lister(drive, TEST, "/test (campagne D204)")

    # ---- 6. le bundle + le worklog : téléchargés pour recoup
    print("\n=== TÉLÉCHARGEMENT DE RECROUP ===")
    telecharger(drive, BUNDLE_ID, os.path.join(DEST, "triade-history.bundle"),
                None, "triade-history.bundle")
    telecharger(drive, WORKLOG_ID, os.path.join(DEST, "worklog.md"),
                None, "worklog.md")

    print(f"\n=== BILAN LISTING/TÉLÉCHARGEMENT : "
          f"{'TOUT VERT' if ROUGES == 0 else str(ROUGES) + ' ROUGE'} ===")
    print(f"(fichiers posés dans {DEST} pour vérification git locale)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
