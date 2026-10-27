#!/usr/bin/env python3
"""D65 (suite 2) — Preuve de bout en bout de la chaîne T3 depuis le bac.

Même chaîne que le superviseur (D48, sup-35) :
  refresh_token → access_token → session resumable → PUT fichier témoin
  dans le dossier test Drive.

Dépose « preuve-jeton-vivant-depuis-le-bac-YYYYMMDD.txt » — fichier
autodocumenté, sans aucun secret. Sa présence dans le dossier test prouve :
jeton vivant + chaîne de dépôt fonctionnelle + dossier accessible → l'échec
S33 sur la machine du développeur est de nature RÉSEAU locale.

Élucide aussi le 4e champ de l'annexe (long. 35) découvert par
test_jeton_oauth.py (forme seulement, jamais le contenu).
"""
import hashlib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

UPLOAD = "/home/z/my-project/upload/terrain_jetons.bin"
URL_TOKEN = "https://oauth2.googleapis.com/token"
URL_SESSION = ("https://www.googleapis.com/upload/drive/v3/files"
               "?uploadType=resumable")
DOSSIER_TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"


def http(req, timeout=60):
    """Retourne (status, corps, en_tetes) sans lever sur les erreurs HTTP."""
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)


# --- 0) annexe : structure + mystère du 4e champ ---------------------------
data = open(UPLOAD, "rb").read()
champs = [c for c in data.split(b"\x00") if c]
cid, secret, refresh = champs[0], champs[1], champs[2]
print(f"[0] annexe : {len(champs)} champs, longueurs {[len(c) for c in champs]}")
if len(champs) >= 4:
    f4 = champs[3]
    print(f"    champ 4 (long. {len(f4)}) : "
          f"{'DOUBLON exact du secret' if f4 == secret else 'différent du secret'}, "
          f"préfixe GOCSPX (forme secret client) : "
          f"{'OUI' if f4.startswith(b'GOCSPX') else 'NON'}, "
          f"préfixe 1// (forme refresh) : "
          f"{'OUI' if f4.startswith(b'1//') else 'NON'}")

# --- 1) jeton OAuth ---------------------------------------------------------
corps = urllib.parse.urlencode({
    "client_id": cid.decode(),
    "client_secret": secret.decode(),
    "refresh_token": refresh.decode(),
    "grant_type": "refresh_token",
}).encode()
code, resp, _ = http(urllib.request.Request(
    URL_TOKEN, data=corps,
    headers={"Content-Type": "application/x-www-form-urlencoded"}))
j = json.loads(resp)
if code != 200 or "access_token" not in j:
    print(f"[1] jeton REFUSÉ HTTP {code} : {j.get('error')} — arrêt.")
    sys.exit(1)
jeton = j["access_token"]
print(f"[1] jeton OAuth : HTTP {code}, access_token {len(jeton)} car., "
      f"scope = {j.get('scope', '(absent)')}")

# --- 2) session resumable ---------------------------------------------------
now = datetime.now(ZoneInfo("Europe/Paris"))
nom_fichier = f"preuve-jeton-vivant-depuis-le-bac-{now:%Y%m%d-%H%M}.txt"
meta = json.dumps({"name": nom_fichier, "parents": [DOSSIER_TEST]}).encode()
code, resp, hdrs = http(urllib.request.Request(
    URL_SESSION, data=meta, method="POST", headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jeton}",
        "X-Upload-Content-Type": "text/plain",
    }))
if code not in (200, 201):
    print(f"[2] session REFUSÉE HTTP {code} : {resp[:300].decode('utf-8', 'replace')}")
    sys.exit(2)
location = hdrs.get("Location") or hdrs.get("location")
if not location:
    print(f"[2] session HTTP {code} mais PAS de Location — en-têtes : {list(hdrs)}")
    sys.exit(2)
print(f"[2] session upload ouverte (HTTP {code}, Location "
      f"{len(location)} car. — host {urllib.parse.urlparse(location).netloc})")

# --- 3) PUT du fichier témoin ----------------------------------------------
contenu = f"""PREUVE DE VIE DU JETON — générée depuis le bac de test, pas depuis votre machine
Date (Paris) : {now:%Y-%m-%d %H:%M}

Ce fichier a été déposé avec la MÊME annexe de jetons (terrain_jetons.bin)
et la MÊME chaîne d'envoi que le superviseur terrain (jeton OAuth → session
resumable → dépôt).

Sa présence dans ce dossier prouve trois choses :
  1. le refresh_token de l'annexe est VIVANT (Google a répondu 200) ;
  2. la chaîne de dépôt Drive complète fonctionne (session + PUT + dossier) ;
  3. l'échec S33 « jeton OAuth ÉCHEC » sur votre machine est donc de nature
     RÉSEAU LOCALE (DNS, pare-feu, fichier hosts, TLS, proxy…) et non un
     problème d'identifiants.

→ Si terrain.13 échoue encore en S33 : suivez le LISEZMOI-terrain13,
  section « SI LE JSON N'APPARAÎT TOUJOURS PAS » (le test curl -v montrera
  précisément l'étape réseau qui casse : résolution DNS, connexion, TLS…).

Ce fichier ne contient aucun secret. Vous pouvez le supprimer après lecture.
""".encode("utf-8")
code, resp, _ = http(urllib.request.Request(
    location, data=contenu, method="PUT",
    headers={"Content-Type": "text/plain; charset=utf-8",
             "Content-Length": str(len(contenu))}))
print(f"[3] PUT fichier témoin : HTTP {code} "
      f"({len(contenu)} octets, « {nom_fichier} »)")
if code not in (200, 201):
    print(f"    corps : {resp[:300].decode('utf-8', 'replace')}")
    sys.exit(3)
try:
    jr = json.loads(resp)
    print(f"    id Drive du fichier : {jr.get('id', '(absent)')} — "
          f"parents acceptés : {jr.get('parents', '(non renvoyé)')}")
except Exception:
    pass
print("\nVERDICT : chaîne T3 COMPLETE validée depuis le bac. "
      "L'annexe + le dossier + l'API sont bons ; seule la machine du "
      "développeur reste en cause pour S33 (réseau local).")
