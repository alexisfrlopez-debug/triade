#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigne_entree_322.py — LE GESTE GIT DE LA SESSION 322 : l'Entrée 322
consignée au worklog (la reprise, le recoup TOUT VERT de la vague 5, les
DEUX failles de l'état livré fermées, la vague 6 reçue et lue intégralement,
le plan déclaré), les QUATRE scripts de session copiés, le commit
(l'identité établie du projet), le push GitHub (main), le bundle --all, et
LES DEUX à chaque push (la règle) : triade-history.bundle REMPLACÉ au slot
générique + le nom versionné triade-history-322-<pointe>.bundle, le worklog
REMPLACÉ — recoupés par re-téléchargement. Fail-closed : le worklog du
coffre RECROUPÉ au git AVANT toute écriture. Le jeton git vit dans
/tmp/git-credentials (600, hors du dépôt, jamais affiché) ; le relais OAuth
de tokens/ pour le coffre (jamais affiché).
"""
import hashlib
import io
import os
import pathlib
import shutil
import subprocess
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

MIROIR = "/tmp/triade-mirror.git"
TRAVAIL = "/tmp/triade-work"
DEPOT = "https://github.com/alexisfrlopez-debug/triade.git"
CRED = "/tmp/git-credentials"
AUTEUR = ("Alexis Lopez "
          "<alexisfrlopez-debug@users.noreply.github.com>")

JETON = "/home/z/my-project/tokens/oauth_token_relais.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
WORKLOG_ID = "1IjBk84S81ioBMASehROG3UsdJkO6JEBY"
BUNDLE_LOCAL = "/tmp/triade-history-322.bundle"

SCRIPTS = ("sonde_relais_ecriture.py", "rapatrie_instructions_v6.py",
           "cloture_vague5.py", "consigne_entree_322.py")

ENTREE_322 = """
## Task 222 — Entrée 322 : LA VAGUE 5 RECROUPÉE ET CLOSE (les deux failles
de l'état livré fermées), LA VAGUE 6 REÇUE ET LUE INTÉGRALEMENT — six
instructions en attente, le plan déclaré

Work Log:
- LA REPRISE : la session précédente s'était close au push 7146490 (les
  scripts du geste miroir) ; le résumé de reprise héritait d'un état EN
  RETARD sur le coffre (il croyait la livraison en attente) — LE COFFRE
  RACONTAIT AUTRE CHOSE. LE RECOUP BYTE-BYTE DE TOUTE LA VAGUE 5
  (rapatrie_instructions_v6.py, lecture seule SA) : le manuscrit v0.18.0
  (224 774 o), l'archive soumission (228 299 o), l'archive complète
  (376 593 o), le rapport d'exécution, le rapport de vérification, les
  empreintes — CHACUNE re-téléchargée, sha256 IDENTIQUE au local ; les DIX
  instructions archivées 10/10 md5 recoupées (les copies
  d'instructions-recu/), le rapport d'exécution aux côtés — TOUT VERT : la
  321 avait bien livré (le relais OAuth du /Tokens du 12/11 vivait encore
  le 17/11 — la sonde OAuth VERTE, scripts/sonde_relais_ecriture.py).
- LA PREMIÈRE FAILLE, FERMÉE : le rapport d'exécution livré citait les
  empreintes d'une GÉNÉRATION INTERMÉDIAIRE des archives (59567916…/
  629229ba… — le rapport rédigé 20:21:39, les zips rescellés 20:22:16, la
  preuve p10 finale 20:22:40 ; le commit a5be18a portait déjà les vraies) :
  la ligne CORRIGÉE vers les empreintes du scellage final (990d7cb6…/
  cab4d688…), le rapport REMPLACÉ à la racine ET aux côtés des instructions
  archivées (13 673 o), chacun RECROUPÉ byte-byte au re-téléchargement
  (scripts/cloture_vague5.py — les remplacements créent des révisions
  Drive, D143 tenu).
- LA SECONDE FAILLE, FERMÉE : RIEN au coffre ne consignait les empreintes
  réelles des deux zips livrés (l'empreinte racine couvre le manuscrit et
  les pièces, pas les zips) : la preuve p10 FINALE (le scellage des deux
  archives, les six pièces VERT, les trois gaps nommés du poste autonome,
  1 858 o) et les métadonnées Zenodo v0180 (1 835 o — le DOI s'insère au
  minting, jamais inventé) DÉPOSÉES à la racine, recoupées byte-byte.
- LA VAGUE 6 REÇUE : SIX nouvelles instructions au /instructions
  (Qwen__20261116_*, déposées 22:02:59-22:03:21 — DIX MINUTES après
  l'archivage des dix précédentes, pendant le push miroir de la 321) :
  rapatriées (6/6 md5 recoupés, instructions-recu/) et LUES INTÉGRALEMENT
  avant toute exécution — (1) 5gfx6pwkj le mode de réponse minimale de
  localiser (plan pré-enregistré hash-consigné, n>=15/mode, aucun contrôle
  retiré) ; (2) 89488hblm le renforcement CF3 (équivalence SMT non bornée
  garde-à-garde pour les 13 règles, le lemme O3 déchargé, la translation
  d'époque forall-delta) ; (3) bqh4qlrqj l'audit du manuscrit v0.18.0 (DIX
  incohérences nommées, le linter étendu au narratif) ; (4) fkkqc7v8t le
  temps constant structurel (analyse de flux d'information au build, la
  cause racine du renversement dudect N=200/400) ; (5) p39uklsca le plan
  d'extension D210 (n>=6 unités instrumentées, ordre randomisé, le test
  d'attribution empirique) ; (6) vljfs6pcj l'optimisation M4 (invalidation
  incrémentaire par empreinte, mémoïsation scellée, pré-filtre différentiel,
  n>=5). AUCUNE exécutée cette session — chacune est une session de mesure
  ou de preuve à elle seule ; l'exécution viendra UNE À UNE avec son étape
  de vérification (la discipline).
- LE PLAN DÉCLARÉ : bqh4qlrqj D'ABORD (l'audit borné aux données locales,
  la voie de la v0.19.0) ; puis les vagues de mesure (5gfx6pwkj, vljfs6pcj,
  fkkqc7v8t) et la vague de preuve (89488hblm) ; p39uklsca DEMANDE LE
  TERRAIN — n>=6 unités livrées de la main du développeur, le labo
  prescrira le plan et préparera les kits, les témoins restent à la main
  (D99), le livre au terrain.
(17/11, la session de la clôture et de la réception)
"""

MESSAGE = ("Entrée 322 : LA VAGUE 5 RECROUPÉE ET CLOSE — le rapport "
           "d'exécution corrigé aux empreintes du scellage final "
           "(990d7cb6…/cab4d688…) et remplacé aux deux emplacements, la "
           "preuve p10 finale + les métadonnées Zenodo déposées à la "
           "racine (les empreintes réelles des deux zips enfin consignées "
           "au coffre), la vague 6 reçue et lue intégralement (six "
           "instructions, aucune exécutée, le plan déclaré)")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[ROUGE] {' '.join(cmd[:4])}… : "
              f"{(r.stderr or r.stdout).strip()[:400]}")
        sys.exit(1)
    return r.stdout


def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def md5(chemin):
    h = hashlib.md5()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def charger_relais():
    with open(JETON, encoding="utf-8-sig") as f:
        info = json.load(f)
    return Credentials(
        token=None,
        refresh_token=info["refresh_token"],
        token_uri=info.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=info["client_id"],
        client_secret=info["client_secret"],
        scopes=SCOPES,
    )


import json  # noqa: E402

drive = build("drive", "v3", credentials=charger_relais(),
              cache_discovery=False)


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


def trouver_dossier(nom, parent):
    for it in lister(parent):
        if it["name"] == nom and it.get("mimeType") == (
                "application/vnd.google-apps.folder"):
            return it["id"]
    return None


def trouver_fichier(nom, parent):
    for it in lister(parent):
        if it["name"] == nom and it.get("mimeType") != (
                "application/vnd.google-apps.folder"):
            return it["id"]
    return None


def telecharger(fid, chemin):
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    with io.FileIO(chemin, "wb") as fh:
        t = MediaIoBaseDownload(fh, drive.files().get_media(fileId=fid))
        fini = False
        while not fini:
            _, fini = t.next_chunk()


def televerser(chemin, nom, parent):
    existant = trouver_fichier(nom, parent)
    media = MediaFileUpload(chemin, resumable=True)
    if existant:
        drive.files().update(fileId=existant, media_body=media).execute()
        print(f"  [remplacé] {nom} ({os.path.getsize(chemin)} o)")
        return existant
    cree = drive.files().create(
        body={"name": nom, "parents": [parent]},
        media_body=media, fields="id").execute()
    print(f"  [livré] {nom} ({os.path.getsize(chemin)} o)")
    return cree["id"]


# ---- 0) le recoup AVANT : le worklog du coffre == le worklog du git
print("=== 0. LE RECOUP AVANT : worklog coffre == worklog git ===")
wl_coffre = "/tmp/worklog-coffre-avant.md"
telecharger(WORKLOG_ID, wl_coffre)
if sha256(wl_coffre) != sha256(f"{TRAVAIL}/worklog.md"):
    print("[ROUGE] le worklog du coffre DIVERGE du git — ARRÊT (fail-closed)")
    sys.exit(2)
print("[VERT] le worklog du coffre == le worklog du git (sha256 identique)")

# ---- 1) l'Entrée 322 consignée (append-only)
with open(f"{TRAVAIL}/worklog.md", "a", encoding="utf-8") as f:
    f.write(ENTREE_322)
print(f"[VERT] l'Entrée 322 consignée au worklog "
      f"({os.path.getsize(f'{TRAVAIL}/worklog.md'):,} o)".replace(",", " "))

# ---- 2) les QUATRE scripts de session copiés
for script in SCRIPTS:
    shutil.copy(f"/home/z/my-project/scripts/{script}",
                f"{TRAVAIL}/scripts/{script}")
print("[VERT] les quatre scripts de session copiés (scripts/)")

# ---- 3) le commit (l'identité établie)
run(["git", "-C", TRAVAIL, "add", "worklog.md", "scripts/"])
run(["git", "-C", TRAVAIL, "-c", "user.name=Alexis Lopez",
     "-c", "user.email=alexisfrlopez-debug@users.noreply.github.com",
     "commit", "-m", MESSAGE])
pointe = run(["git", "-C", TRAVAIL, "rev-parse", "--short", "HEAD"]).strip()
print(f"[VERT] le commit de session : {pointe}")

# ---- 4) le push GitHub (main)
run(["git", "-C", TRAVAIL, "-c",
     f"credential.helper=store --file={CRED}",
     "push", DEPOT, "main:main"])
distant = run(["git", "-C", TRAVAIL, "-c",
               f"credential.helper=store --file={CRED}",
               "ls-remote", DEPOT, "refs/heads/main"]).strip()
local = run(["git", "-C", TRAVAIL, "rev-parse", "main"]).strip()
ok_push = distant == local
print(f"[{'VERT' if ok_push else 'ROUGE'}] le push GitHub : "
      f"main == {distant[:12]}… "
      f"({'identique' if ok_push else 'DIVERGE'})")
if not ok_push:
    sys.exit(1)

# ---- 5) le miroir mis à jour + le bundle --all
run(["git", "-C", MIROIR, "fetch", TRAVAIL,
     "refs/heads/main:refs/heads/main"])
if os.path.exists(BUNDLE_LOCAL):
    os.remove(BUNDLE_LOCAL)
run(["git", "-C", MIROIR, "bundle", "create", BUNDLE_LOCAL, "--all"])
print(f"[VERT] le bundle --all né : {BUNDLE_LOCAL} "
      f"({os.path.getsize(BUNDLE_LOCAL):,} o)".replace(",", " "))
for ligne in run(["git", "-C", MIROIR, "bundle", "list-heads",
                  BUNDLE_LOCAL]).strip().splitlines():
    print(f"  pointe du bundle : {ligne[:70]}")

# ---- 6) LES DEUX à chaque push : le bundle (slot générique + nom versionné)
#         et le worklog, au TRIADE-sauvegarde-git
print("=== LES DEUX À CHAQUE PUSH (TRIADE-sauvegarde-git) ===")
dossier = trouver_dossier("TRIADE-sauvegarde-git", RACINE)
if not dossier:
    print("[ROUGE] le dossier TRIADE-sauvegarde-git introuvable")
    sys.exit(1)
nom_versionne = f"triade-history-322-{pointe}.bundle"
fid_generique = televerser(BUNDLE_LOCAL, "triade-history.bundle", dossier)
fid_versionne = televerser(BUNDLE_LOCAL, nom_versionne, dossier)
fid_worklog = WORKLOG_ID
drive.files().update(
    fileId=fid_worklog,
    media_body=MediaFileUpload(f"{TRAVAIL}/worklog.md",
                               resumable=True)).execute()
print(f"  [remplacé] worklog.md "
      f"({os.path.getsize(f'{TRAVAIL}/worklog.md'):,} o)".replace(",", " "))

# ---- 7) les recoups par re-téléchargement
print("=== LES RECOUPS (re-téléchargement) ===")
rouges = 0
telecharger(fid_worklog, "/tmp/worklog-coffre-apres.md")
if sha256("/tmp/worklog-coffre-apres.md") == sha256(
        f"{TRAVAIL}/worklog.md"):
    print("[VERT] worklog.md — sha256 IDENTIQUE après dépôt")
else:
    print("[ROUGE] worklog.md — DIVERGE !")
    rouges += 1
for etiquette, fid in (("triade-history.bundle", fid_generique),
                       (nom_versionne, fid_versionne)):
    chemin = f"/tmp/recoup-{etiquette}"
    telecharger(fid, chemin)
    if md5(chemin) == md5(BUNDLE_LOCAL):
        print(f"[VERT] {etiquette} — md5 IDENTIQUE après dépôt "
              f"({os.path.getsize(chemin):,} o)".replace(",", " "))
    else:
        print(f"[ROUGE] {etiquette} — DIVERGE !")
        rouges += 1

print(f"=== BILAN DE LA CONSIGNATION : "
      f"{'TOUT VERT' if rouges == 0 else str(rouges) + ' ROUGE'} ===")
sys.exit(0 if rouges == 0 else 1)
