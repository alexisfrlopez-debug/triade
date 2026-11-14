#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LE NETTOYAGE DU /test (la commande du développeur : « nettoie /test
en archivant tout ce qui n'est pas nécessaire pour la suite »).
L'unité loupe-01 est close aux deux bras (T : Entrée 284 ; C : Entrée 287),
l'ère pré-campagne (10-13/11) est consignée : TOUT descend à l'archive.
RIEN N'EST JETÉ — « les fragments ne sont jamais jetés » : chaque pièce est
DÉPLACÉE (addParents/removeParents — mêmes identifiants, mêmes octets, la
corbeille n'est jamais touchée).
  1. PRÉ-VOl : les 41 entrées racine classées à l'AVANCE — une inconnue ABORT.
  2. Le recoup du kit v2 AVANT le déplacement : 14/14 (les DIX pièces à la
     gravure EMPREINTES, la gravure et le zip au bac du miroir, les DEUX
     dépôts neufs d'hier 13:31).
  3. Les DEUX archives créées sous /archives-livraisons/.
  4. Les 31 DÉPLACEMENTS.
  5. Le recoup APRÈS : la racine re-listée (l'ensemble attendu EXACT), les
     archives re-listées, les pièces déplacées re-téléchargées byte-byte.
  6. LISEZMOI-NETTOYAGE-TEST-20261114.txt posé à la racine + la carte
     LISEZMOI-KITS-UNITES-D204.txt portée à jour."""
import base64
import hashlib
import json
import pathlib
import time
import urllib.parse
import urllib.request

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
WORK = pathlib.Path("/home/z/my-project/work")
TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
BAC_KIT_V2 = pathlib.Path(
    "/home/z/my-project/download/kit_unite_loupe_01_C_v2/kit-unite-loupe-01-C-20261114-v2")
API = "https://www.googleapis.com/drive/v3"
RELAI_ID = "1RKV_5dN1qtp_H7A_3kyPBOKIrrpIG8rP"

# ---- la classification des 41 entrées racine (à l'avance, nommée) -------------
GARDER_DOSSIERS = {"Nouveau run", "archives-livraisons", "archives-preuves"}
GARDER_FICHIERS = {
    "LISEZMOI-CORRECTIF-ENCODAGE.txt", "LISEZMOI-GUI-TOUS-RUNS.txt",
    "LISEZMOI-KITS-UNITES-D204.txt", "LISEZMOI-campagne-GUI.txt",
    "TRIADE-1CLIC-CAMPAGNE-D204-v3.bat",
    "TRIADE_gui_campagne_v1_CORRECTIF-encodage.zip",
    "TRIADE_gui_tous_runs_v1.zip",
}
VERS_UNITE01 = [  # → /archives-livraisons/unite-01-loupe-20261114/
    "kit-unite-loupe-01-T-20261114", "kit-unite-loupe-01-T-20261114-v2",
    "kit-unite-loupe-01-C-20261114", "kit-unite-loupe-01-C-20261114-v2",
    "preuves-unite01C", "run-console-unite01.txt",
]
VERS_CONSOLE_V2 = ["run-console-unite01C.txt"]  # → unite-01-loupe…/console-run-v2-recue-1330/
VERS_PRECAMPAGNE = [  # → /archives-livraisons/terrain-pre-campagne-20261110-13/
    "LISEZMOI-loupe.txt", "kit-loupe.zip", "loupe-kit-13",
    "LISEZMOI-KIT-ANDROID.txt", "TRIADE-kit-android-v1.apk",
    "TRIADE_kit_android_20261112T214507Z.zip", "temoin-verdict-android", "VERDICT.txt",
    "preuves-kit2-dudect-20261113T081451Z", "preuves-kit2-dudect-20261113T081451Z.zip",
    "preuves-kit2-dudect-20261113T103725Z", "preuves-m7d-voie1-20261113T155020Z",
    "temoin-shani-fermeture-20261114", "temoin-shani-reprise-20261114",
    "temoin-shani-signe-ecart-20261114", "temoin-shani.txt",
    "LISEZMOI-FICHIERS-1CLIC.txt", "fichiers-1clic",
    "LISEZMOI-RUNS-1CLIC.txt", "LISEZMOI-RUNS-RESTANTS.txt",
    "TRIADE_kit_runs_restants_v1.zip",
    "cle-publique-I.txt", "signatures-I.txt",
    "TRIADE_gui_campagne_v1.zip",
]
NOM_ARCH_U01 = "unite-01-loupe-20261114"
NOM_ARCH_PRE = "terrain-pre-campagne-20261110-13"
NOM_CONSOLE_V2 = "console-run-v2-recue-1330"

# ---- 0) le relais OAuth du coffre (écriture) ----------------------------------
svc_creds = service_account.Credentials.from_service_account_file(
    f"{UPLOAD}/physichong-4b3b7222b48c.json",
    scopes=["https://www.googleapis.com/auth/drive"])
svc = build("drive", "v3", credentials=svc_creds, cache_discovery=False)
with open(f"{UPLOAD}/physichong-4b3b7222b48c.json") as f:
    sa = json.load(f)

def b64url(d):
    return base64.urlsafe_b64encode(d).rstrip(b"=").decode()

now = int(time.time())
header = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
claims = b64url(json.dumps(
    {"iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/drive",
     "aud": sa["token_uri"], "iat": now, "exp": now + 3600}).encode())
si = f"{header}.{claims}".encode()
key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
jwt = f"{header}.{claims}.{b64url(key.sign(si, padding.PKCS1v15(), hashes.SHA256()))}"
req = urllib.request.Request(
    sa["token_uri"],
    data=urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt}).encode(), method="POST")
with urllib.request.urlopen(req, timeout=30) as r:
    token_sa = json.loads(r.read())["access_token"]
req = urllib.request.Request(f"{API}/files/{RELAI_ID}?alt=media",
    headers={"Authorization": f"Bearer {token_sa}"})
with urllib.request.urlopen(req, timeout=30) as r:
    relais = json.loads(r.read())
req = urllib.request.Request(
    relais["token_uri"],
    data=urllib.parse.urlencode({
        "client_id": relais["client_id"],
        "client_secret": relais["client_secret"],
        "refresh_token": relais["refresh_token"],
        "grant_type": "refresh_token"}).encode(), method="POST")
with urllib.request.urlopen(req, timeout=30) as r:
    ACCESS = json.loads(r.read())["access_token"]
print("[jeton] le relais OAuth du coffre est rafraîchi")

def api(url, data=None, method="GET", headers=None):
    h = {"Authorization": f"Bearer {ACCESS}"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    with urllib.request.urlopen(req, timeout=600) as r:
        corps = r.read()
        return json.loads(corps) if corps else {}

def list_children(fid):
    out, token = [], None
    while True:
        params = {"q": f"'{fid}' in parents and trashed = false",
                  "pageSize": "200",
                  "fields": "nextPageToken,files(id,name,mimeType,size)"}
        if token:
            params["pageToken"] = token
        obj = api(API + "/files?" + urllib.parse.urlencode(params))
        out += obj.get("files", [])
        token = obj.get("nextPageToken")
        if not token:
            return out

def retelecharger(fid):
    req = urllib.request.Request(f"{API}/files/{fid}?alt=media",
        headers={"Authorization": f"Bearer {ACCESS}"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.read()

def patch_media(fid, contenu):
    api(f"https://www.googleapis.com/upload/drive/v3/files/{fid}"
        f"?uploadType=media", data=contenu, method="PATCH",
        headers={"Content-Type": "application/octet-stream"})

def uploader(nom, contenu, parent):
    limite = "trk8c2f1a3"
    metadonnees = json.dumps({"name": nom, "parents": [parent]})
    corps = (f"--{limite}\r\n"
             "Content-Type: application/json; charset=UTF-8\r\n\r\n"
             f"{metadonnees}\r\n"
             f"--{limite}\r\n"
             "Content-Type: application/octet-stream\r\n\r\n").encode() \
        + contenu + f"\r\n--{limite}--".encode()
    res = api("https://www.googleapis.com/upload/drive/v3/files"
              "?uploadType=multipart&fields=id,name",
              data=corps, method="POST",
              headers={"Content-Type":
                       f"multipart/related; boundary={limite}"})
    return res["id"]

def deplacer(fid, cible):
    api(f"{API}/files/{fid}?addParents={cible}&removeParents={TEST_ID}",
        method="PATCH")

# ---- 1) PRÉ-VOL : la racine entière doit être classée --------------------------
racine = list_children(TEST_ID)
noms = {c["name"]: c for c in racine}
attendus = (GARDER_DOSSIERS | GARDER_FICHIERS | set(VERS_UNITE01)
            | set(VERS_CONSOLE_V2) | set(VERS_PRECAMPAGNE))
inconnus = set(noms) - attendus
manquants = attendus - set(noms)
assert not inconnus, f"ENTRÉES RACINE INCONNUES (abort, rien touché) : {inconnus}"
assert not manquants, f"ENTRÉES ATTENDUES ABSENTES : {manquants}"
print(f"[pré-vol] les {len(racine)} entrées racine sont TOUTES classées — "
      f"{len(GARDER_DOSSIERS)+len(GARDER_FICHIERS)} demeurent, "
      f"{len(VERS_UNITE01)}+{len(VERS_CONSOLE_V2)} vers l'archive unité-01, "
      f"{len(VERS_PRECAMPAGNE)} vers l'archive pré-campagne")

# ---- 2) le recoup du kit v2 AVANT le déplacement (14/14) ------------------------
kit = {c["name"]: c for c in list_children(noms["kit-unite-loupe-01-C-20261114-v2"]["id"])}
gravure = {}
for ligne in retelecharger(kit["EMPREINTES-KIT-UNITE-01-C.txt"]["id"]).decode("utf-8").splitlines():
    parties = ligne.split()
    if len(parties) == 2 and len(parties[0]) == 64:
        gravure[parties[1]] = parties[0]
assert len(gravure) == 10, f"la gravure porte {len(gravure)} pièces, 10 attendues"
verts_kit = 0
for nom, h in gravure.items():
    brut = retelecharger(kit[nom]["id"])
    ok = hashlib.sha256(brut).hexdigest() == h
    verts_kit += ok
    print(f"[{'VERT' if ok else 'ROUGE'}] kit-v2/{nom} == la gravure")
for nom, bac in [("EMPREINTES-KIT-UNITE-01-C.txt", "EMPREINTES-KIT-UNITE-01-C.txt"),
                 ("kit-unite-loupe-01-C-20261114-v2.zip", "kit-unite-loupe-01-C-20261114-v2.zip"),
                 ("run-console-unite01C.txt", "run-console-unite01C.txt")]:
    ok = retelecharger(kit[nom]["id"]) == (BAC_KIT_V2 / bac).read_bytes()
    verts_kit += ok
    print(f"[{'VERT' if ok else 'ROUGE'}] kit-v2/{nom} == le bac du miroir (byte-byte)")
temoin_kit = list_children(kit["preuves-unite01C"]["id"])[0]
ok = retelecharger(temoin_kit["id"]) == (BAC_KIT_V2 / "preuves-unite01C" / "temoin-unite01C.txt").read_bytes()
verts_kit += ok
print(f"[{'VERT' if ok else 'ROUGE'}] kit-v2/preuves-unite01C/temoin-unite01C.txt == le bac")
assert verts_kit == 14, f"le recoup pré-déplacement du kit v2 : {verts_kit}/14"
print(f"[recoup] le kit v2 AVANT déplacement : 14/14 VERT")

# ---- 3) les deux archives créées -------------------------------------------------
archives_livraisons = noms["archives-livraisons"]["id"]
def trouver_ou_creer(nom, parent):
    for c in list_children(parent):
        if c["name"] == nom:
            return c["id"], False
    res = api(API + "/files", data=json.dumps(
        {"name": nom, "mimeType": "application/vnd.google-apps.folder",
         "parents": [parent]}).encode(), method="POST",
        headers={"Content-Type": "application/json; charset=UTF-8"})
    return res["id"], True

arch_u01, neuf1 = trouver_ou_creer(NOM_ARCH_U01, archives_livraisons)
arch_pre, neuf2 = trouver_ou_creer(NOM_ARCH_PRE, archives_livraisons)
dossier_console, neuf3 = trouver_ou_creer(NOM_CONSOLE_V2, arch_u01)
print(f"[archives] {NOM_ARCH_U01} {'créé' if neuf1 else 'trouvé'}, "
      f"{NOM_ARCH_PRE} {'créé' if neuf2 else 'trouvé'}, "
      f"{NOM_CONSOLE_V2} {'créé' if neuf3 else 'trouvé'} — sous /archives-livraisons/")

# ---- 4) les 31 DÉPLACEMENTS ------------------------------------------------------
for nom in VERS_UNITE01:
    deplacer(noms[nom]["id"], arch_u01)
    print(f"[déplacé] {nom} → /archives-livraisons/{NOM_ARCH_U01}/")
for nom in VERS_CONSOLE_V2:
    deplacer(noms[nom]["id"], dossier_console)
    print(f"[déplacé] {nom} → /archives-livraisons/{NOM_ARCH_U01}/{NOM_CONSOLE_V2}/")
for nom in VERS_PRECAMPAGNE:
    deplacer(noms[nom]["id"], arch_pre)
    print(f"[déplacé] {nom} → /archives-livraisons/{NOM_ARCH_PRE}/")

# ---- 5) le recoup APRÈS -----------------------------------------------------------
racine_apres = {c["name"] for c in list_children(TEST_ID)}
attendu_apres = (GARDER_DOSSIERS | GARDER_FICHIERS
                 | {"LISEZMOI-NETTOYAGE-TEST-20261114.txt"})
trop = racine_apres - attendu_apres - {"LISEZMOI-NETTOYAGE-TEST-20261114.txt"}
assert not trop, f"la racine porte encore : {trop}"
u01_apres = {c["name"] for c in list_children(arch_u01)}
assert set(VERS_UNITE01) <= u01_apres and NOM_CONSOLE_V2 in u01_apres, u01_apres
pre_apres = {c["name"] for c in list_children(arch_pre)}
assert set(VERS_PRECAMPAGNE) <= pre_apres, pre_apres
print(f"[recoup] la racine ne porte plus que {len(racine_apres)-1} entrées + le "
      f"LISEZMOI à venir ; l'archive unité-01 porte {len(u01_apres)}, "
      f"l'archive pré-campagne {len(pre_apres)}")

noms_apres = {c["name"]: c for c in list_children(TEST_ID)}
u01_map = {c["name"]: c for c in list_children(arch_u01)}
console_map = {c["name"]: c for c in list_children(dossier_console)}
kit_archive = {c["name"]: c for c in list_children(u01_map["kit-unite-loupe-01-C-20261114-v2"]["id"])}
ok1 = retelecharger(console_map["run-console-unite01C.txt"]["id"]) == \
     (BAC_KIT_V2 / "run-console-unite01C.txt").read_bytes()
ok2 = retelecharger(kit_archive["loupe-01-c.dll"]["id"]) == \
     (BAC_KIT_V2 / "loupe-01-c.dll").read_bytes()
ok3 = retelecharger(list_children(u01_map["preuves-unite01C"]["id"])[0]["id"]) == \
     (BAC_KIT_V2 / "preuves-unite01C" / "temoin-unite01C.txt").read_bytes()
ok4 = retelecharger(u01_map["run-console-unite01.txt"]["id"]) == \
     pathlib.Path("/home/z/my-project/download/nouveau-run/run-console-unite01.txt").read_bytes() \
     if pathlib.Path("/home/z/my-project/download/nouveau-run/run-console-unite01.txt").exists() else None
print(f"[{'VERT' if ok1 else 'ROUGE'}] la console v2 re-téléchargée de l'archive : identique byte-byte")
print(f"[{'VERT' if ok2 else 'ROUGE'}] loupe-01-c.dll re-téléchargé de l'archive : identique byte-byte")
print(f"[{'VERT' if ok3 else 'ROUGE'}] le témoin C re-téléchargé de l'archive : identique byte-byte")
print(f"[{'VERT' if ok4 else 'ÉCART'}] la console du refus T re-téléchargée de l'archive"
      + ("" if ok4 else " (le bac local ne la porte pas — vérifiée à 283)"))
assert ok1 and ok2 and ok3

# ---- 6) le LISEZMOI-NETTOYAGE + la carte des kits --------------------------------
LISEZMOI = """LISEZMOI-NETTOYAGE-TEST — le 14/11/2026 (l'Entrée 288, la campagne D204)
« nettoie /test en archivant tout ce qui n'est pas nécessaire pour la suite » — la commande du développeur.

L'unité loupe-01 est CLOSE aux deux bras (T : Entrée 284 ; C : Entrée 287) ; l'ère pré-campagne (10-13/11) est consignée. Le /test est la zone de travail de la campagne : ce qui est clos descend à l'archive. RIEN N'EST JETÉ — « les fragments ne sont jamais jetés » : chaque pièce est DÉPLACÉE (mêmes identifiants, mêmes octets), jamais supprimée.

== ARCHIVÉ à /archives-livraisons/unite-01-loupe-20261114/ (l'unité close) ==
- kit-unite-loupe-01-T-20261114/       le kit T v1 (le refus T0 « CreateFileW » — Entrée 283)
- kit-unite-loupe-01-T-20261114-v2/    le kit T v2 (le run VERT 15/0 — Entrée 284)
- kit-unite-loupe-01-C-20261114/       le kit C v1 (le refus du scénario — Entrée 286 ; D143 : il demeure au coffre, l'archive est au coffre)
- kit-unite-loupe-01-C-20261114-v2/    le kit C v2 (le run VERT 15/0 — Entrée 287 ; avec la console du run et le témoin né au kit, déposés le 14/11 13:31)
- preuves-unite01C/                    le témoin C signé (recoupé 19 VERT — Entrée 287)
- run-console-unite01.txt              la console du refus T v1 (Entrée 283)
- console-run-v2-recue-1330/run-console-unite01C.txt   la console VERTE du run C v2, déposée à la racine le 14/11 13:30 (15 VERT 0 ROUGE — sha256 81011506fc797331…)

== ARCHIVÉ à /archives-livraisons/terrain-pre-campagne-20261110-13/ (l'ère consignée avant la campagne) ==
- la vitrine loupe (kit-loupe.zip, loupe-kit-13/, LISEZMOI-loupe.txt — 10/11)
- le kit android (TRIADE-kit-android-v1.apk, TRIADE_kit_android_20261112T214507Z.zip, temoin-verdict-android/, VERDICT.txt, LISEZMOI-KIT-ANDROID.txt — 12/11)
- les preuves kit2-dudect (2 dossiers + le zip — 13/11) et m7d-voie1 (13/11)
- les témoins shani (3 dossiers + temoin-shani.txt — 13/11)
- la distribution « runs restants » (TRIADE_kit_runs_restants_v1.zip, fichiers-1clic/, les trois LISEZMOI-RUNS/FICHIERS — 13/11)
- les clés du sceau-I (cle-publique-I.txt, signatures-I.txt)
- TRIADE_gui_campagne_v1.zip (le GUI v1 non corrigé — remplacé par la version CORRECTIF-encodage)

== DEMEURE au /test (la suite de la campagne) ==
- Nouveau run/   l'atelier 013520, le livre de la campagne (la ligne T ; la ligne C attend son retour)
- TRIADE-1CLIC-CAMPAGNE-D204-v3.bat + TRIADE_gui_campagne_v1_CORRECTIF-encodage.zip + LISEZMOI-campagne-GUI.txt + LISEZMOI-CORRECTIF-ENCODAGE.txt   le GUI de campagne, l'outil de chaque unité
- TRIADE_gui_tous_runs_v1.zip + LISEZMOI-GUI-TOUS-RUNS.txt   le GUI tous-runs (la réplication attend ses deux jeux d'annotations)
- LISEZMOI-KITS-UNITES-D204.txt   la carte des kits d'unités (portée à jour)
- archives-livraisons/, archives-preuves/

== ENCORE ATTENDUS (nommés à l'Entrée 287 — le dépôt du 14/11 13:30-13:31 a apporté la console VERTE du run v2 et le témoin du kit, pas les deux pièces ci-dessous) ==
1. run-console-unite01C.txt DU KIT C v1 — LA CONSOLE DU REFUS : le fichier né du Tee du lanceur, dans le dossier kit-unite-loupe-01-C-20261114\\ de votre machine (celui qui porte « access violation … 0x7FFA23900094 » et « code 1 »). Le dépôt reçu le 13:30 est la console du run v2 (VERTE) — une bonne pièce, consignée — mais ce n'est pas celle du refus. La pièce d'un refus n'est jamais jetée.
2. L'ATELIER DE L'UNITÉ C (onglets 4-7 du GUI : le carnet M3, la ligne livraisons.csv, les défauts, le chrono M4) — l'atelier du coffre ne porte encore que la ligne T.
Non bloquant : les deux jeux d'annotations pour la réplication ; la commande réelle des unités 13-14.

LA SUITE : LOUPE-02 LIRE, aux deux bras (la troisième unité du plan a78caf8c…).
"""

fid_lisezmoi = uploader("LISEZMOI-NETTOYAGE-TEST-20261114.txt",
                        LISEZMOI.encode("utf-8"), TEST_ID)
ok_l = retelecharger(fid_lisezmoi) == LISEZMOI.encode("utf-8")
print(f"[{'VERT' if ok_l else 'ROUGE'}] LISEZMOI-NETTOYAGE-TEST-20261114.txt "
      f"posé à la racine ({len(LISEZMOI.encode('utf-8')):,} o) — "
      f"{'identique au re-téléchargement' if ok_l else 'DIVERGE'}")

carte_id = noms_apres["LISEZMOI-KITS-UNITES-D204.txt"]["id"]
carte = retelecharger(carte_id).decode("utf-8")
NOTE = """

=== LE NETTOYAGE DU /test — le 14/11/2026 (l'Entrée 288) ===
L'unité loupe-01 est CLOSE aux deux bras (T : Entrée 284 ; C : Entrée 287). Ses QUATRE kits (T v1/v2, C v1/v2), preuves-unite01C/ et la console du refus T vivent désormais à /archives-livraisons/unite-01-loupe-20261114/ (DÉPLACÉS, jamais jetés — mêmes identifiants, mêmes octets ; D143 tenu : le kit C v1 demeure au coffre, l'archive est au coffre). La console VERTE du run C v2 (déposée le 14/11 13:30) : /archives-livraisons/unite-01-loupe-20261114/console-run-v2-recue-1330/. L'ère pré-campagne (10-13/11) : /archives-livraisons/terrain-pre-campagne-20261110-13/. Le détail : LISEZMOI-NETTOYAGE-TEST-20261114.txt à la racine du /test. LA CAMPAGNE CONTINUE : LOUPE-02 LIRE, aux deux bras.
"""
if "LE NETTOYAGE DU /test" not in carte:
    carte = carte.rstrip("\n") + "\n" + NOTE
patch_media(carte_id, carte.encode("utf-8"))
ok_c = retelecharger(carte_id).decode("utf-8") == carte
print(f"[{'VERT' if ok_c else 'ROUGE'}] la carte LISEZMOI-KITS-UNITES-D204.txt "
      f"portée à jour ({len(carte.encode('utf-8')):,} o)")

final = sorted(c["name"] for c in list_children(TEST_ID))
print("\n===== LA RACINE DU /test APRÈS LE NETTOYAGE =====")
for n in final:
    print(f"  {n}")
print("\nLE NETTOYAGE EST RECOUPÉ VERT — 31 déplacements, 0 suppression, "
      "le kit v2 14/14 avant, les pièces re-téléchargées après.")
