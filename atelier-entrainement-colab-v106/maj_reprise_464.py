#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE REPRISE PORTÉ À L'ÉTAT 464 (dépôt + coffre) : le nouvel état présent
inséré en tête de la pile des états (APRÈS L'ENTRÉE 464 — le repli du
plan § 7 acté, la v1064 au /livrables), les états 463/462/461/457 demeurant
en dessous. Au coffre : la pièce relue, le nouveau contenu téléversé
(PATCH au même ID), le recop byte-byte."""
import hashlib
import json
import pathlib
import time
import urllib.parse
import urllib.request

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build

SA_PATH = "/home/z/my-project/upload/physichong-4b3b7222b48c.json"
TOKENS_FOLDER = "1EMxwHKkkfKROjFsHhu4vpKZpgqW-rgZL"
COFFRE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
DEPOT = pathlib.Path("/home/z/my-project/depot/REPRISE_PROJET.md")

ÉTAT_464 = (
    "**L'ÉTAT PRÉSENT AU 28/11/2026 (APRÈS L'ENTRÉE 464 — LE TROISIÈME REFUS "
    "NOMMÉ, LE REPLI DU PLAN § 7 ACTÉ : LA v1064 AU /livrables)** : le troisième "
    "run du maître (la v1063, processus CUDA-vierge — la cane VERTE, "
    "l'allocateur né sous expandable_segments, l'autocast fp16 MORDU : le "
    "tampon refusé de 456,00 MiB = le [12 615 × 18 944] fp16, LA MOITIÉ EXACTE "
    "du pied fp32 du terrain.12) tint L'ÉPOQUE 1 ENTIÈRE (17/17, le monstre au "
    "pas 1 compris — les pics décroissants 9.24/8.39/7.98/7.62 aux pas "
    "4/8/12/16) puis refusa à LA SECONDE VISITE du monstre (le pas 18, "
    "l'époque 2 : LE PERSISTANT ADAMW [2 × 40 370 176 × 4 o ≈ 0,31 Gio, né au "
    "premier pas d'optimiseur] + les gradients accumulés + la fragmentation "
    "[1,16 Gio réservés-non-alloués, 253,81 MiB libres] mangeant la marge — le "
    "pic 13.58 Gio ; l'écart du budget du terrain.12 — l'état de l'optimiseur "
    "aux époques 2-3 non compté — l'écart du labo seul, NOMMÉ : le monstre "
    "tient sur un bassin vierge, PAS à la marche du plan). LE REPLI NOMMÉ DU "
    "PLAN § 7 ACTÉ AU LABO : l'exclusion de ajouter-v3-i26111705-t1 SEUL (le "
    "nommé ; t3/t2 [12 021/12 019] tenus à leur 1re visite, jamais nommés par "
    "la mesure), le corpus FICHIER byte-byte (sha 39614077… inchangé — "
    "l'exclusion vit à la cellule 5, PAR NOM, fail-closed "
    "EXCLUSION-NOMMÉE-DIVERGENTE), LA MARCHE 48 pas / 12 pas d'optimiseur "
    "EXACTS (l'horloge identique au 51-pas, prouvé au bac — la passe "
    "repli-0 : le repli, l'ordre, la marche, l'horloge, les totaux "
    "P 70 050 · C 16 584), l'ordre des longs d'abord parmi les retenus. "
    "LE KIT v1063 (ONZE pièces, les TROIS amendements au manifeste — "
    "sha 992f9e6b…, id 161NOiJc…) + LE NOTEBOOK v1064 (TROIS cellules "
    "touchées : le titre, le pin, LA CELLULE 5 ; SIX épreuves VERT — "
    "sha f0b8c7ef…, id 1lQpCDTY…) AU /livrables ; la copie aveugle "
    "(9e78d13d…, l'invariant des TROIS constantes asserté) au dépôt ; la "
    "v1063-VIVANTE et le kit v1062 archivés au lot "
    "livrables_supersedes_20261128_terrain13 (1XzXcpDo…). LA SUITE : LE "
    "MAÎTRE REDÉMARRE LA SESSION (la cane exige le processus vierge, le cache "
    "du modèle demeure) PUIS rouvre la v1064 au /livrables et « Tout "
    "exécuter » (le journal portera LE REPLI : 16 exemples retenus, "
    "48 pas / 12 pas d'optimiseur) ; si le terrain refuse t3/t2 à leur "
    "2e/3e visite, le repli élargi reviendra AU LABO avec le pic mesuré — "
    "jamais au bord ; la comparaison pré/post AU LABO (la ligne de base 105 : "
    "17/18 · 14/18 · 64/128) ; LA VALIDATION du maître ; PUIS la feuille de "
    "route de l'Entrée 461 dans l'ordre (les packs v0.34.x, le repo "
    "HuggingFace aleksickx, le fine-tuning v107). "
)

# ── 1 · le dépôt : l'état 464 inséré en tête de la pile ──
actuel = DEPOT.read_text(encoding="utf-8")
ancre = "**L'ÉTAT PRÉSENT AU 28/11/2026 (APRÈS L'ENTRÉE 463"
if actuel.count(ancre) != 1:
    raise SystemExit(f"ANCRE-DIVERGENTE : {actuel.count(ancre)} occurrence(s) de l'état 463")
nouveau = actuel.replace(ancre, ÉTAT_464 + ancre, 1)
if nouveau.count("L'ÉTAT PRÉSENT") != actuel.count("L'ÉTAT PRÉSENT") + 1:
    raise SystemExit("INSERTION-ROMPUE : la pile des états n'a pas grandi de 1")
DEPOT.write_text(nouveau, encoding="utf-8")
nb_etats = nouveau.count("L'ÉTAT PRÉSENT")
print(f"[dépôt] le REPRISE porté à l'état 464 ({len(nouveau.encode('utf-8'))} o) — "
      f"la pile : {nb_etats} états")

# ── 2 · le coffre : la pièce relue, recoupée au dépôt AVANT, puis PATCH ──
creds_ro = service_account.Credentials.from_service_account_file(
    SA_PATH, scopes=["https://www.googleapis.com/auth/drive.readonly"])
creds_ro.refresh(Request())
drive_ro = build("drive", "v3", credentials=creds_ro)
relais = json.loads(drive_ro.files().get_media(
    fileId=drive_ro.files().list(
        q=f"'{TOKENS_FOLDER}' in parents and name = 'oauth_token_relais.json' and trashed = false",
        fields="files(id)", pageSize=1).execute()["files"][0]["id"]).execute().decode("utf-8"))
data = urllib.parse.urlencode({
    "client_id": relais["client_id"], "client_secret": relais["client_secret"],
    "refresh_token": relais["refresh_token"], "grant_type": "refresh_token"}).encode()
with urllib.request.urlopen(urllib.request.Request(
        "https://oauth2.googleapis.com/token", data=data), timeout=30) as r:
    TOK = json.loads(r.read().decode())["access_token"]

def api(url, method="GET", octets=None, mime="application/json"):
    req = urllib.request.Request(url, data=octets, method=method,
                                 headers={"Authorization": f"Bearer {TOK}",
                                          "Content-Type": mime})
    with urllib.request.urlopen(req, timeout=1800) as r:
        lu = r.read()
        return json.loads(lu.decode()) if lu else {}

rep = api("https://www.googleapis.com/drive/v3/files?q=" + urllib.parse.quote(
    f"'{COFFRE}' in parents and name = 'REPRISE_PROJET.md' and trashed = false")
    + "&fields=files(id,modifiedTime)")
if len(rep.get("files", [])) != 1:
    raise SystemExit(f"REPRISE-ABSENT au coffre : {rep}")
fid = rep["files"][0]["id"]
print(f"[coffre] le REPRISE du coffre : id {fid} — modifié {rep['files'][0]['modifiedTime']}")

au_coffre = urllib.request.urlopen(urllib.request.Request(
    f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media",
    headers={"Authorization": f"Bearer {TOK}"}), timeout=300).read()
if hashlib.sha256(au_coffre).hexdigest() != hashlib.sha256(actuel.encode("utf-8")).hexdigest():
    raise SystemExit("RECOP-ROUGE : le REPRISE du coffre diverge du dépôt AVANT la mise à jour")
print("[coffre] le REPRISE du coffre recoupé au dépôt AVANT — VERT")

frontieres = "tr464r3pr1s3"
corps = ("--" + frontieres + "\r\n"
         "Content-Type: application/json; charset=UTF-8\r\n\r\n"
         + json.dumps({"name": "REPRISE_PROJET.md"}) + "\r\n"
         + "--" + frontieres + "\r\n"
         "Content-Type: text/markdown\r\n\r\n").encode("utf-8")
corps += nouveau.encode("utf-8") + ("\r\n--" + frontieres + "--\r\n").encode("utf-8")
api(f"https://www.googleapis.com/upload/drive/v3/files/{fid}?uploadType=multipart",
    method="PATCH", octets=corps, mime=f"multipart/related; boundary={frontieres}")
time.sleep(3)
relu = urllib.request.urlopen(urllib.request.Request(
    f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media",
    headers={"Authorization": f"Bearer {TOK}"}), timeout=300).read()
if hashlib.sha256(relu).hexdigest() != hashlib.sha256(nouveau.encode("utf-8")).hexdigest():
    raise SystemExit("RECOP-ROUGE : le REPRISE relu du coffre diverge !")
print(f"[coffre] le REPRISE du coffre PATCHÉ à l'état 464 ({len(relu)} o) — RECOP VERT")
