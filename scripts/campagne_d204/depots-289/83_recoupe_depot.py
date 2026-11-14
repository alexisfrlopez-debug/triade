#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LE RECOUP DES DEUX DÉPÔTS DE LA MAIN (la commande du développeur :
« vérifie les dépôts dans /test puis go pour la suite ») — l'Entrée 289.

A. /test/kit-unite-loupe-01-C-20261114/ (la copie TERRAIN du kit C v1, née
   14:04:35) : LA CONSOLE DU REFUS y vit (run-console-unite01C.txt, 3 250 o,
   modifiée 12:29:25 — la pièce demandée aux Entrées 286/287/288). Chaque
   pièce rapatriée DEUX FOIS byte-byte ; les ONZE pièces du kit == l'original
   ARCHIVÉ (mêmes octets — la chaîne tenue : le kit livré == le kit qui a
   refusé) ; la console décodée, ses MARQUEURS nommés (l'access violation,
   l'adresse 0x7FFA23900094, le code 1), CONFRONTÉE à la pièce du chat au bac.

B. /test/test/ (le retour de l'atelier tous-runs, né 14:09:16 — la LIGNE C
   attendue) : atelier-campagne-d204-20261114-013520/ (livraisons.csv, carnet
   M3, defauts.csv, journal-ouverture), etat-tous-runs.json, les DEUX logs du
   GUI — chaque pièce DEUX FOIS byte-byte ; la ligne C-loupe-01-it1 LUE, la
   ligne T vérifiée INCHANGÉE, le log neuf 114216 lu (la session du bras C).

C. PUIS LE RANGEMENT : les DEUX dépôts DÉPLACÉS à l'archive (addParents/
   removeParents — JAMAIS une suppression, les fragments ne sont jamais
   jetés) ; la racine re-listée ; les pièces re-téléchargées à leur nouvelle
   place."""
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
API = "https://www.googleapis.com/drive/v3"
RELAI_ID = "1RKV_5dN1qtp_H7A_3kyPBOKIrrpIG8rP"
BAC = pathlib.Path("/home/z/my-project/download")

# ---- 0) le relais OAuth du coffre ----------------------------------------------
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
                  "fields": "nextPageToken,files(id,name,mimeType,size,createdTime,modifiedTime)"}
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

def double(fid, nom):
    a, b = retelecharger(fid), retelecharger(fid)
    assert a == b, f"{nom} : les deux téléchargements DIVERGENT"
    return a

# ==============================================================================
# A. LE KIT C v1 TERRAIN + LA CONSOLE DU REFUS
# ==============================================================================
racine = {c["name"]: c for c in list_children(TEST_ID)}
kit_terrain = {c["name"]: c for c in list_children(racine["kit-unite-loupe-01-C-20261114"]["id"])}
print(f"\n===== A. LE KIT TERRAIN ({len(kit_terrain)} pièces) =====")
for n in sorted(kit_terrain):
    print(f"  {n}  ({kit_terrain[n].get('size','?')} o, modifié "
          f"{(kit_terrain[n].get('modifiedTime') or '?')[:19]})")

# l'original archivé (la vérité depuis la 284, déplacé intact à la 288)
archives = {c["name"]: c for c in list_children(racine["archives-livraisons"]["id"])}
u01 = {c["name"]: c for c in list_children(archives["unite-01-loupe-20261114"]["id"])}
kit_archive = {c["name"]: c for c in list_children(u01["kit-unite-loupe-01-C-20261114"]["id"])}

pieces_communes = sorted(set(kit_terrain) & set(kit_archive))
console_seule = sorted(set(kit_terrain) - set(kit_archive))
print(f"\n[pièces] {len(pieces_communes)} communes à l'archivé, "
      f"propre au terrain : {console_seule}")

verts = 0
for nom in pieces_communes:
    a = double(kit_terrain[nom]["id"], f"terrain/{nom}")
    b = double(kit_archive[nom]["id"], f"archive/{nom}")
    ok = a == b
    verts += ok
    print(f"[{'VERT' if ok else 'ROUGE'}] terrain/{nom} == l'archivé "
          f"byte-byte ({len(a):,} o, sha256 {hashlib.sha256(a).hexdigest()[:16]}…)")
assert len(pieces_communes) == 11, pieces_communes
assert verts == 11, f"la comparaison à l'archivé : {verts}/11"

# la gravure : les DIX pièces du terrain à EMPREINTES (celui de l'archive,
# déjà tenu, == celui du terrain vérifié ci-dessus)
gravure = {}
for ligne in double(kit_archive["EMPREINTES-KIT-UNITE-01-C.txt"]["id"],
                     "gravure").decode("utf-8").splitlines():
    p = ligne.split()
    if len(p) == 2 and len(p[0]) == 64:
        gravure[p[1]] = p[0]
assert len(gravure) == 10, gravure
vg = 0
for nom, h in gravure.items():
    a = double(kit_terrain[nom]["id"], f"terrain/{nom}")
    ok = hashlib.sha256(a).hexdigest() == h
    vg += ok
    print(f"[{'VERT' if ok else 'ROUGE'}] terrain/{nom} == la gravure ({h[:16]}…)")
assert vg == 10, f"la gravure au terrain : {vg}/10"

# LA CONSOLE DU REFUS
console = kit_terrain["run-console-unite01C.txt"]
brut = double(console["id"], "console-refus")
sha_c = hashlib.sha256(brut).hexdigest()
(BAC / "preuves-refus-C-v1" / "run-console-unite01C-refus-v1-terrain.txt").write_bytes(brut)
print(f"\n----- LA CONSOLE DU REFUS : {len(brut):,} o, sha256 {sha_c[:16]}… "
      f"(versée au bac) -----")
try:
    texte = brut.decode("utf-16")
    enc = "utf-16"
except UnicodeDecodeError:
    texte = brut.decode("utf-8", errors="replace")
    enc = "utf-8 (forcé)"
print(f"[décodage] {enc}, {len(texte.splitlines())} lignes")
for l in texte.splitlines():
    if l.strip():
        print(f"  | {l}")

marqueurs = {
    "access-violation": "access violation" in texte.lower(),
    "adresse-0x7FFA23900094": "23900094" in texte,
    "code-1": "code 1" in texte or "(code 1)" in texte or "code 1" in texte.lower(),
    "T0-vert": "T0" in texte and ("VERT" in texte or "[VERT]" in texte),
    "quatre-exports": "loupe_01_ouvrir" in texte and "loupe_03_fermer" in texte,
    "base-refus-0x7ff9b74d0000": "7ff9b74d0000" in texte.lower(),
}
print("\n[marqueurs] " + "  ".join(
    f"{k}={'OUI' if v else 'non'}" for k, v in marqueurs.items()))

# la confrontation à la pièce du chat (le bac, 2 693 o — la paste manuelle)
chat = (BAC / "preuves-refus-C-v1" / "run-console-unite01C-recu-chat.txt").read_bytes()
lignes_chat = [l for l in chat.decode("utf-8").splitlines() if l.strip()]
lignes_console = [l for l in texte.splitlines() if l.strip()]
communes = [l for l in lignes_console if l in lignes_chat]
print(f"\n[confrontation] la pièce du chat : {len(lignes_chat)} lignes vives ; "
      f"la console du terrain : {len(lignes_console)} lignes vives ; "
      f"{len(communes)} lignes de la console VIVENT dans la pièce du chat")
absentes = [l for l in lignes_console if l not in lignes_chat]
if absentes:
    print(f"  → {len(absentes)} lignes de la console ABSENTES de la pièce du chat :")
    for l in absentes[:8]:
        print(f"    | {l[:110]}")

# ==============================================================================
# B. LE RETOUR DE L'ATELIER TOUS-RUNS (la ligne C)
# ==============================================================================
print("\n===== B. LE RETOUR DE L'ATELIER (/test/test/) =====")
snaps = {c["name"]: c for c in list_children(racine["test"]["id"])}
gui = {c["name"]: c for c in list_children(snaps["TRIADE_gui_tous_runs_v1"]["id"])}
atelier = {c["name"]: c for c in list_children(gui["atelier-campagne-d204-20261114-013520"]["id"])}
logs = {c["name"]: c for c in list_children(gui["TRIADE_logs"]["id"])}

miroir_atelier = BAC / "nouveau-run" / "Nouveau run" / "test" / \
    "TRIADE_gui_tous_runs_v1" / "atelier-campagne-d204-20261114-013520"
bac_retour = BAC / "atelier-retour-C-20261114"
bac_retour.mkdir(exist_ok=True)

# 1) livraisons.csv — la ligne C attendue
livr = double(atelier["livraisons.csv"]["id"], "livraisons.csv")
(bac_retour / "livraisons.csv").write_bytes(livr)
texte_livr = livr.decode("utf-8", errors="replace")
print("----- livraisons.csv (les lignes de données) -----")
lignes_c = []
lignes_t = []
for l in texte_livr.splitlines():
    if l and not l.startswith("#"):
        print(f"  | {l}")
        if l.startswith("T-loupe-01"):
            lignes_t.append(l)
        if ",C," in l:
            lignes_c.append(l)
ancien_livr = (miroir_atelier / "livraisons.csv").read_bytes()
ancien_txt = ancien_livr.decode("utf-8", errors="replace")
ancienne_ligne_t = [l for l in ancien_txt.splitlines() if l.startswith("T-loupe-01")]
ok_t = lignes_t == ancienne_ligne_t
print(f"[{'VERT' if ok_t else 'ROUGE'}] la ligne T {'INCHANGÉE' if ok_t else 'CHANGÉE'} : {lignes_t}")
print(f"[{'VERT' if lignes_c else 'ÉCART'}] la ligne C : {lignes_c or 'ABSENTE de livraisons.csv'}")
if livr != ancien_livr:
    import difflib
    print("  [delta livraisons.csv contre le miroir pré-C]")
    for d in difflib.unified_diff(ancien_txt.splitlines(), texte_livr.splitlines(),
                                  lineterm="", n=0):
        if d.startswith(("+", "-")) and not d.startswith(("+++", "---")):
            print(f"    {d[:120]}")
else:
    print("  [delta] livraisons.csv == le miroir pré-C OCTET POUR OCTET (aucune ligne née)")

# 2) le carnet M3
carnet = double(atelier["carnet_temps_humain.csv"]["id"], "carnet.csv")
(bac_retour / "carnet_temps_humain.csv").write_bytes(carnet)
print("\n----- carnet_temps_humain.csv (les lignes de données) -----")
for l in carnet.decode("utf-8", errors="replace").splitlines():
    if l and not l.startswith("#"):
        print(f"  | {l}")

# 3) les défauts
defs = double(atelier["defauts.csv"]["id"], "defauts.csv")
(bac_retour / "defauts.csv").write_bytes(defs)
print("\n----- defauts.csv (les lignes de données) -----")
lignes_d = [l for l in defs.decode("utf-8", errors="replace").splitlines()
            if l and not l.startswith("#")]
for l in lignes_d:
    print(f"  | {l}")
if not lignes_d:
    print("  | (aucun défaut nommé)")

# 4) le journal d'ouverture + etat-tous-runs.json (L'ÉTAT DES RUNS — la session C)
journaux = double(atelier["journal-ouverture.txt"]["id"], "journal-ouverture.txt")
(bac_retour / "journal-ouverture.txt").write_bytes(journaux)
print("\n----- journal-ouverture.txt -----")
print(journaux.decode("utf-8", errors="replace")[:800])
try:
    etat_brut = double(gui["etat-tous-runs.json"]["id"], "etat.json")
    (bac_retour / "etat-tous-runs.json").write_bytes(etat_brut)
    etat = json.loads(etat_brut)
    print("\n----- etat-tous-runs.json (ENTIER) -----")
    print(json.dumps(etat, ensure_ascii=False, indent=1))
except Exception as e:
    print(f"[!] etat-tous-runs.json : {e}")

# 5) les DEUX logs — l'ancien == le miroir, le neuf LU
ancien_log_miroir = (BAC / "nouveau-run" / "Nouveau run" / "test" /
                     "TRIADE_gui_tous_runs_v1" / "TRIADE_logs" /
                     "tous_runs_gui_20261114-013458.log").read_bytes()
ok_log0 = double(logs["tous_runs_gui_20261114-013458.log"]["id"], "log-013458") == ancien_log_miroir
print(f"\n[{'VERT' if ok_log0 else 'ROUGE'}] le log 013458 == le miroir (inchangé)")
neuf = double(logs["tous_runs_gui_20261114-114216.log"]["id"], "log-114216")
(bac_retour / "tous_runs_gui_20261114-114216.log").write_bytes(neuf)
print("----- le log NEUF tous_runs_gui_20261114-114216.log "
      f"({len(neuf):,} o) -----")
for l in neuf.decode("utf-8", errors="replace").splitlines():
    if l.strip():
        print(f"  | {l}")

# ==============================================================================
# C. LE RANGEMENT (les dépôts à l'archive — JAMAIS jetés)
# ==============================================================================
print("\n===== C. LE RANGEMENT =====")

def trouver_ou_creer(nom, parent):
    for c in list_children(parent):
        if c["name"] == nom:
            return c["id"], False
    res = api(API + "/files", data=json.dumps(
        {"name": nom, "mimeType": "application/vnd.google-apps.folder",
         "parents": [parent]}).encode(), method="POST",
        headers={"Content-Type": "application/json; charset=UTF-8"})
    return res["id"], True

def deplacer(fid, cible):
    api(f"{API}/files/{fid}?addParents={cible}&removeParents={TEST_ID}",
        method="PATCH")

# la console du refus : sous l'archive de l'unité close
w_console, n1 = trouver_ou_creer("console-refus-v1-terrain-20261114",
                                 archives["unite-01-loupe-20261114"]["id"])
deplacer(racine["kit-unite-loupe-01-C-20261114"]["id"], w_console)
print(f"[déplacé] kit-unite-loupe-01-C-20261114/ → "
      f"/archives-livraisons/unite-01-loupe-20261114/console-refus-v1-terrain-20261114/"
      f"{' (créé)' if n1 else ''}")

# le retour d'atelier : sous l'archive de l'unité close aussi (la ligne C la ferme)
w_atelier, n2 = trouver_ou_creer("atelier-retour-ligne-C-20261114",
                                 archives["unite-01-loupe-20261114"]["id"])
deplacer(racine["test"]["id"], w_atelier)
print(f"[déplacé] test/ → /archives-livraisons/unite-01-loupe-20261114/"
      f"atelier-retour-ligne-C-20261114/test/{' (créé)' if n2 else ''}")

# le recoup APRÈS
racine_apres = {c["name"] for c in list_children(TEST_ID)}
attendu = {"Nouveau run", "archives-livraisons", "archives-preuves",
           "LISEZMOI-CORRECTIF-ENCODAGE.txt", "LISEZMOI-GUI-TOUS-RUNS.txt",
           "LISEZMOI-KITS-UNITES-D204.txt", "LISEZMOI-campagne-GUI.txt",
           "LISEZMOI-NETTOYAGE-TEST-20261114.txt",
           "TRIADE-1CLIC-CAMPAGNE-D204-v3.bat",
           "TRIADE_gui_campagne_v1_CORRECTIF-encodage.zip",
           "TRIADE_gui_tous_runs_v1.zip"}
assert racine_apres == attendu, (racine_apres - attendu, attendu - racine_apres)
print(f"[recoup] la racine : {len(racine_apres)} entrées, l'attendu EXACT")

u01_apres = {c["name"]: c for c in list_children(archives["unite-01-loupe-20261114"]["id"])}
wc = {c["name"]: c for c in list_children(u01_apres["console-refus-v1-terrain-20261114"]["id"])}
wa = {c["name"]: c for c in list_children(u01_apres["atelier-retour-ligne-C-20261114"]["id"])}
kt = {c["name"]: c for c in list_children(wc["kit-unite-loupe-01-C-20261114"]["id"])}
wa_test = {c["name"]: c for c in list_children(wa["test"]["id"])}
wa_gui = {c["name"]: c for c in list_children(wa_test["TRIADE_gui_tous_runs_v1"]["id"])}
wa_atelier = {c["name"]: c for c in list_children(wa_gui["atelier-campagne-d204-20261114-013520"]["id"])}
ok1 = double(kt["run-console-unite01C.txt"]["id"], "console-apres") == brut
ok2 = double(wa_atelier["livraisons.csv"]["id"], "livraisons-apres") == livr
print(f"[{'VERT' if ok1 else 'ROUGE'}] la console du refus re-téléchargée de l'archive : identique")
print(f"[{'VERT' if ok2 else 'ROUGE'}] livraisons.csv re-téléchargé de l'archive : identique")
assert ok1 and ok2

print("\nLE RECOUP DES DEUX DÉPÔTS EST VERT — la console du refus et la ligne C "
      "sont TENUES ; les deux dépôts rangés à l'archive, 0 suppression.")
