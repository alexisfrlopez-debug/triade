#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livraison_vague5_relais.py — LA LIVRAISON DE LA VAGUE 5 AU COFFRE (relais
OAuth, la voie d'écriture) : le manuscrit v0.18.0, les DEUX archives, le
rapport d'exécution, le rapport de vérification, les empreintes — puis
L'ARCHIVAGE des DIX instructions /instructions → /ARCHIVE (après exécution,
10/10 md5 recoupés avant le déplacement, re-téléchargés et recoupés après).

Adapté de livraison_drive_v180.py (préparé en vague 5) : la voie d'écriture
est le relais OAuth (tokens/oauth_token_relais.json — jetons du /Tokens du
coffre, RÈGLE PERMANENTE du 16/11/2026). AUCUNE valeur de jeton affichée.

Discipline : recoup AVANT chaque geste, écriture, RELECTURE RECROUPÉE après
(téléchargement + md5). D143 : rien ne se jette — l'empreinte v0.17.0 de la
racine est RENOMMÉE empreintes_livrables_v0.17.0.txt avant de poser la
v0.18.0 au nom générique.
"""
import hashlib
import io
import json
import pathlib
import sys
import time

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

JETON = "/home/z/my-project/tokens/oauth_token_relais.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]

RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
DOSSIER_INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
ARCHIVE_INSTRUCTIONS = "1qqfk-yMNg3E5s1HVVeEkhmFceeDuPtNb"

V5 = pathlib.Path("/home/z/my-project/livraison-vague5")
RECUS = pathlib.Path("/home/z/my-project/instructions-recu")

ROUGES = 0


def coup(rouge: bool, message: str):
    global ROUGES
    if rouge:
        ROUGES += 1
    print(f"  [{'ROUGE' if rouge else 'VERT'}] {message}")


def md5_local(chemin: pathlib.Path) -> str:
    return hashlib.md5(chemin.read_bytes()).hexdigest()


def connexion():
    with open(JETON, encoding="utf-8-sig") as f:
        info = json.load(f)
    creds = Credentials(
        token=None,
        refresh_token=info["refresh_token"],
        token_uri=info.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=info["client_id"],
        client_secret=info["client_secret"],
        scopes=SCOPES,
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def lister(drive, parent):
    page, items = None, []
    while True:
        resp = drive.files().list(
            q=f"'{parent}' in parents and trashed = false",
            pageSize=200,
            fields="nextPageToken, files(id, name, mimeType, size, "
                   "modifiedTime, md5Checksum)",
            pageToken=page).execute()
        items += resp.get("files", [])
        page = resp.get("nextPageToken")
        if not page:
            break
    return items


def telecharger(drive, file_id) -> bytes:
    buf = io.BytesIO()
    d = MediaIoBaseDownload(buf, drive.files().get_media(fileId=file_id))
    fini = False
    while not fini:
        _, fini = d.next_chunk()
    return buf.getvalue()


def deposer(drive, chemin: pathlib.Path, parent: str, etiquette: str) -> str:
    """Crée ou REMPLACE (jamais de doublon) + relecture recoupée."""
    attendu = md5_local(chemin)
    existant = None
    for it in lister(drive, parent):
        if it["name"] == chemin.name and it.get("mimeType") != \
                "application/vnd.google-apps.folder":
            existant = it["id"]
            break
    media = MediaFileUpload(str(chemin), resumable=True)
    if existant:
        drive.files().update(fileId=existant, media_body=media).execute()
        print(f"  [remplacé] {chemin.name} ({chemin.stat().st_size} o)")
        fid = existant
    else:
        r = drive.files().create(
            body={"name": chemin.name, "parents": [parent]},
            media_body=media, fields="id").execute()
        print(f"  [livré] {chemin.name} → {etiquette} "
              f"({chemin.stat().st_size} o)")
        fid = r["id"]
    # la relecture recoupée
    contenu = telecharger(drive, fid)
    ok = hashlib.md5(contenu).hexdigest() == attendu
    coup(not ok, f"relecture {chemin.name} : md5 "
                 f"{'RECROUPÉ' if ok else 'DIVERGE (!)'}")
    return fid


def main():
    drive = connexion()

    # ------------------------------------------------------------ PHASE 0
    print("=== PHASE 0 : LES VÉRIFICATIONS PRÉALABLES (fail-closed) ===")
    # l'identité du dossier d'archivage (nom + parent)
    meta = drive.files().get(
        fileId=ARCHIVE_INSTRUCTIONS,
        fields="id, name, parents").execute()
    print(f"  dossier d'archivage : « {meta['name']} » "
          f"(parents={meta.get('parents', [])})")
    coup(meta["name"] != "instructions_20261116",
         "le dossier d'archivage porte le nom attendu "
         f"(« {meta['name']} »)")
    # les fichiers à livrer existent localement
    pieces = [
        (V5 / "edition-v180" / "TRIADE_manuscrit_v0.18.0.pdf", "le manuscrit"),
        (V5 / "archives" / "TRIADE_soumission_v0.18.0.zip",
         "l'archive soumission"),
        (V5 / "archives" / "TRIADE_complet_v0.18.0.zip",
         "l'archive complète"),
        (V5 / "rapport-execution-vague5.txt", "le rapport d'exécution"),
        (V5 / "archives" / "soumission" / "rapport_verification_v0.18.0.txt",
         "le rapport de vérification"),
        (V5 / "archives" / "soumission" / "empreintes_livrables.txt",
         "les empreintes v0.18.0"),
    ]
    for chemin, _ in pieces:
        coup(not chemin.exists(), f"{chemin.name} présent au bac "
                                  f"({chemin.stat().st_size if chemin.exists() else 0} o)")
    if ROUGES:
        print("=== PHASE 0 : REFUS (fail-closed) ===")
        return 1

    # ------------------------------------------------------- PHASE A : dépôts
    print("\n=== PHASE A : LES DÉPÔTS À LA RACINE DU COFFRE ===")
    for chemin, etiquette in pieces[:-1]:  # tout sauf les empreintes
        deposer(drive, chemin, RACINE, etiquette)

    # les empreintes : D143 — l'ancienne (v0.17.0) renommée, la neuve posée
    empreinte_v180 = pieces[-1][0]
    racine = lister(drive, RACINE)
    ancienne = next((it for it in racine
                     if it["name"] == "empreintes_livrables.txt"), None)
    if ancienne:
        contenu = telecharger(drive, ancienne["id"])
        texte = contenu.decode("utf-8", errors="replace")
        if "v0.18.0" in texte and \
                hashlib.md5(contenu).hexdigest() == md5_local(empreinte_v180):
            print("  [déjà là] empreintes_livrables.txt == v0.18.0")
        elif "v0.17.0" in texte:
            cible = "empreintes_livrables_v0.17.0.txt"
            deja = next((it for it in racine if it["name"] == cible), None)
            if deja:
                print(f"  [déjà là] {cible} — l'ancienne reste en place")
            else:
                drive.files().update(
                    fileId=ancienne["id"], body={"name": cible}).execute()
                apres = telecharger(drive, ancienne["id"])
                ok = hashlib.md5(apres).hexdigest() == \
                    hashlib.md5(contenu).hexdigest()
                coup(not ok, f"renommage {cible} : md5 "
                             f"{'RECROUPÉ' if ok else 'CHANGÉ (!)'}")
            deposer(drive, empreinte_v180, RACINE, "les empreintes v0.18.0")
        else:
            coup(True, "empreintes_livrables.txt racine : contenu "
                       "INATTENDU (ni v0.17.0 ni v0.18.0) — REFUS")
    else:
        deposer(drive, empreinte_v180, RACINE, "les empreintes v0.18.0")

    # ------------------------------------------- PHASE B : l'archivage des dix
    print("\n=== PHASE B : L'ARCHIVAGE DES DIX INSTRUCTIONS ===")
    fichiers = lister(drive, DOSSIER_INSTRUCTIONS)
    print(f"  {len(fichiers)} fichiers au /instructions")
    if len(fichiers) != 10:
        coup(True, "le /instructions ne porte pas exactement 10 fichiers")
    deplaces = 0
    for f in sorted(fichiers, key=lambda x: x["name"]):
        local = RECUS / f["name"]
        md5_drive = f.get("md5Checksum")
        md5_avant = md5_local(local) if local.exists() else None
        if not (md5_avant and md5_drive and md5_avant == md5_drive):
            coup(True, f"{f['name']} : md5 Drive {md5_drive} != local "
                       f"{md5_avant} — REFUS de déplacer")
            continue
        drive.files().update(
            fileId=f["id"], addParents=ARCHIVE_INSTRUCTIONS,
            removeParents=DOSSIER_INSTRUCTIONS).execute()
        apres = telecharger(drive, f["id"])
        ok = hashlib.md5(apres).hexdigest() == md5_drive
        deplaces += ok
        coup(not ok, f"{f['name']} archivé — md5 "
                     f"{'RECROUPÉ après déplacement' if ok else 'CHANGÉ (!)'}")
    coup(deplaces != len(fichiers),
         f"{deplaces}/{len(fichiers)} instructions archivées, md5 recoupés")

    # le rapport d'exécution aux côtés des instructions archivées
    print("\n=== PHASE C : LE RAPPORT AUX CÔTÉS DES INSTRUCTIONS ===")
    deposer(drive, V5 / "rapport-execution-vague5.txt",
            ARCHIVE_INSTRUCTIONS, "l'archive des instructions")

    # ------------------------------------------------- PHASE D : la relecture
    print("\n=== PHASE D : LA RELECTURE FINALE DU COFFRE ===")
    restants = lister(drive, DOSSIER_INSTRUCTIONS)
    coup(len(restants) != 0,
         f"le /instructions est vide ({len(restants)} fichier restant)")
    archive = lister(drive, ARCHIVE_INSTRUCTIONS)
    attendu_archive = 8 + 10 + 1  # le lot de 8 + les dix + le rapport
    coup(len(archive) != attendu_archive,
         f"l'archive des instructions porte {len(archive)} entrées "
         f"(attendu {attendu_archive})")
    noms_racine = {it["name"]: it for it in lister(drive, RACINE)}
    for nom in ("TRIADE_manuscrit_v0.18.0.pdf",
                "TRIADE_soumission_v0.18.0.zip",
                "TRIADE_complet_v0.18.0.zip",
                "rapport-execution-vague5.txt",
                "rapport_verification_v0.18.0.txt",
                "empreintes_livrables.txt",
                "empreintes_livrables_v0.17.0.txt"):
        coup(nom not in noms_racine, f"la racine porte {nom}")

    print(f"\n=== BILAN : {'TOUT VERT' if ROUGES == 0 else str(ROUGES) + ' ROUGE'} ===")
    return 0 if ROUGES == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
