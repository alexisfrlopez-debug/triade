#!/usr/bin/env python3
"""D65 (suite) — Pré-diagnostic OAuth : tester le refresh token de l'annexe
depuis le bac, AVANT le run terrain.13 du développeur.

Ne print AUCUN secret : uniquement longueurs, empreintes, formes (préfixes/
suffixes) et le verdict brut de Google (code erreur + description, sans secret).

Étapes :
  1. lit upload/terrain_jetons.bin (annexe D48, 248 o) ;
  2. vérifie la structure (3 champs NUL-séparés : cid / secret / refresh) ;
  3. vérifie que ces 248 octets sont embarqués À L'IDENTIQUE dans
     superviseur-terrain13.exe (sinon le test porte sur une annexe obsolète) ;
  4. POST https://oauth2.googleapis.com/token — corps identique à GABARIT_OAUTH
     (client_id / client_secret / refresh_token / grant_type=refresh_token) ;
  5. classe le verdict : VIVANT (access_token) / REFUSÉ (error=…).
"""
import hashlib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

UPLOAD = "/home/z/my-project/upload/terrain_jetons.bin"
EXE13 = "/home/z/my-project/download/superviseur-terrain13.exe"
URL_TOKEN = "https://oauth2.googleapis.com/token"

# --- 1-2) lecture et structure de l'annexe ---------------------------------
data = open(UPLOAD, "rb").read()
print(f"[1] annexe upload : {len(data)} octets, md5 {hashlib.md5(data).hexdigest()}")

champs = data.split(b"\x00")
champs = [c for c in champs if c]
print(f"[2] champs non vides : {len(champs)} — longueurs {[len(c) for c in champs]}")
if len(champs) < 3:
    print("    STRUCTURE INATTENDUE (moins de 3 champs) — abandon.")
    sys.exit(2)

cid, secret, refresh = champs[0], champs[1], champs[2]
formes = {
    "cid finit par .apps.googleusercontent.com": cid.endswith(b".apps.googleusercontent.com"),
    "refresh commence par '1//' (forme Google)": refresh.startswith(b"1//"),
    "secret long. 24-35 (forme Google)": 24 <= len(secret) <= 35,
}
for k, v in formes.items():
    print(f"    forme : {k} : {'OUI' if v else 'NON'}")

# --- 3) identité avec l'annexe embarquée dans terrain.13 -------------------
exe = open(EXE13, "rb").read()
off = exe.find(data)
if off >= 0:
    print(f"[3] annexe embarquée dans superviseur-terrain13.exe : IDENTIQUE @0x{off:X}")
    embarquee_identique = True
else:
    print("[3] annexe ABSENTE du terrain.13 — recherche des 3 champs séparément :")
    for nom, val in (("cid", cid), ("secret", secret), ("refresh", refresh)):
        o = exe.find(val)
        print(f"    {nom} : {'présent @0x%X' % o if o >= 0 else 'ABSENT'}")
    embarquee_identique = False

# --- 4) la requête OAuth (identique au GABARIT_JETON du superviseur) -------
corps = urllib.parse.urlencode({
    "client_id": cid.decode(),
    "client_secret": secret.decode(),
    "refresh_token": refresh.decode(),
    "grant_type": "refresh_token",
}).encode()
req = urllib.request.Request(
    URL_TOKEN, data=corps,
    headers={"Content-Type": "application/x-www-form-urlencoded"})
print(f"[4] POST {URL_TOKEN} ({len(corps)} octets de corps)…")
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        resp, code = r.read(), r.status
except urllib.error.HTTPError as e:
    resp, code = e.read(), e.code
except Exception as e:
    print(f"    RÉSEAU (depuis le bac) : {e}")
    sys.exit(3)

# --- 5) verdict (sans secret) ----------------------------------------------
try:
    j = json.loads(resp)
except Exception:
    print(f"    réponse non-JSON HTTP {code} ({len(resp)} o) — brut tronqué : {resp[:120]!r}")
    sys.exit(4)

if "access_token" in j:
    print(f"[5] VERDICT : JETON VIVANT (HTTP {code}) — access_token "
          f"{len(j['access_token'])} car., expires_in={j.get('expires_in')}s, "
          f"token_type={j.get('token_type')}")
    print("    → l'annexe est BONNE ; l'échec S33 sur la machine du développeur "
          "est de nature RÉSEAU (branche B des prédictions D65).")
elif "error" in j:
    print(f"[5] VERDICT : REFUSÉ (HTTP {code}) — error={j['error']}")
    desc = j.get("error_description", "")
    if desc:
        print(f"    description : {desc}")
    print("    → l'annexe est REFUSÉE par Google ; terrain.13 produira exactement "
          "ce message dans terrain_jeton.json (branche A' des prédictions D65).")
else:
    print(f"[5] réponse inattendue HTTP {code} — clés : {sorted(j.keys())}")
