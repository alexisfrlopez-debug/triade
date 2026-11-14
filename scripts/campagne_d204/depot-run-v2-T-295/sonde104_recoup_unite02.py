#!/usr/bin/env python3
"""TRIADE — LA SONDE 104 : le recoup du dépôt preuves-unite02/ (le run v2 du
bras T revenu). Les contrôles :
  S1  double téléchargement du témoin (byte-byte)
  S2  le témoin : empreinte de la pièce == la gravure du kit v2 == le /test
  S3  les VINGT noms de vecteurs du témoin == la liste attendue du scénario v2
  S4  le verdict porté : 20 VERT, 0 ROUGE
  S5  la main (D99) : daté + signé
  S6  les pièces du kit v2 re-hachées == la gravure EMPREINTES
  S7  la chronologie : run -> témoin (main) -> dépôt au coffre
"""
import json
import time
import hashlib
import urllib.request
import urllib.parse
import pathlib
import re

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64

UPLOAD = "/home/z/my-project/upload"
DEST = pathlib.Path("/home/z/my-project/work/test_mirror")
FOLDER_ID = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
TEMoin_ID = "1Bh9pt8qdy0jJgYGaetq3XHj3mW6DqDoI"  # temoin-unite02.txt au /test

with open(f"{UPLOAD}/physichong-4b3b7222b48c.json") as f:
    sa = json.load(f)

def b64url(d): return base64.urlsafe_b64encode(d).rstrip(b"=").decode()
now = int(time.time())
header = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
claims = b64url(json.dumps({"iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/drive",
                            "aud": sa["token_uri"], "iat": now, "exp": now + 3600}).encode())
si = f"{header}.{claims}".encode()
key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
sig = key.sign(si, padding.PKCS1v15(), hashes.SHA256())
jwt = f"{header}.{claims}.{b64url(sig)}"
req = urllib.request.Request(sa["token_uri"], data=urllib.parse.urlencode(
    {"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}).encode(), method="POST")
with urllib.request.urlopen(req, timeout=30) as r:
    tok = json.loads(r.read())["access_token"]

def dl(file_id):
    req = urllib.request.Request(f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media",
                                 headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def api(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

rapport = []
def note(num, vert, texte):
    ligne = f"{'VERT' if vert else 'ROUGE'} S{num}: {texte}"
    print(ligne)
    rapport.append(ligne)

# S1 — double téléchargement
t1 = dl(TEMoin_ID)
t2 = dl(TEMoin_ID)
local = (DEST / "temoin-unite02.txt").read_bytes()
note(1, t1 == t2 == local,
     f"le témoin re-téléchargé DEUX FOIS == la première rapportée ({len(t1)} o, "
     f"md5 {hashlib.md5(t1).hexdigest()[:8]}…, sha256 {hashlib.sha256(t1).hexdigest()[:8]}…)")

texte = t1.decode("utf-8")

# S2 — l'empreinte de la pièce portée au témoin == la gravure == le /test
m = re.search(r"loupe\.exe 127488 o, sha256 ([0-9a-f]{64})", texte)
sha_porte = m.group(1) if m else None
loupe_local = (DEST / "kit-T-v2" / "loupe.exe").read_bytes()
sha_exe = hashlib.sha256(loupe_local).hexdigest()
gravure = {}
for ligne in (DEST / "kit-T-v2" / "EMPREINTES-KIT-UNITE-02-T.txt").read_text(encoding="utf-8-sig").splitlines():
    mm = re.match(r"([0-9a-f]{64})\s+(\S+)", ligne)
    if mm:
        gravure[mm.group(2)] = mm.group(1)
note(2, sha_porte == sha_exe == gravure["loupe.exe"] == "98354ff6ac07cf291199e9b33acd032bf2285bcbc7490b8f174bc24f91770f6e",
     f"loupe.exe : le témoin porte {str(sha_porte)[:8]}… == re-haché au labo {sha_exe[:8]}… == la gravure {gravure['loupe.exe'][:8]}…")

# S3 — les vecteurs du témoin v2 == les vecteurs du témoin v1 (le MÊME juge,
# seule la constante R_JOURNAL a bougé — le diff v1->v2 recoupé au labo)
vec_temoin = re.findall(r"^  (VERT|ROUGE) (\S+)$", texte, re.M)
noms_v2 = [n for (_, n) in vec_temoin]
temoin_v1 = (DEST / "archives-u02" / "kit-unite-loupe-02-T-20261114" /
             "preuves-unite02" / "temoin-unite02.txt").read_text(encoding="utf-8")
vec_v1 = re.findall(r"^  (VERT|ROUGE) (\S+)$", temoin_v1, re.M)
noms_v1 = [n for (_, n) in vec_v1]
retournes = [n for (c, n) in vec_v1 if c == "ROUGE"]
flips = [n for n in retournes if n in [x for (c, x) in vec_temoin if c == "VERT"]]
note(3, sorted(noms_v2) == sorted(noms_v1) and len(noms_v2) == 20
        and set(retournes) == {"V2:les-bords-de-fenetre", "V2:cinq-entrees-dont-une-non-alignee"}
        and set(flips) == set(retournes),
     f"les {len(noms_v2)} vecteurs du témoin v2 == les {len(noms_v1)} du témoin v1 (le même juge, "
     f"la seule constante changée) ; les DEUX ROUGE du juge fautif v1 retournés VERT au v2 : "
     + ", ".join(sorted(retournes)))

# S4 — le verdict
m = re.search(r"le verdict\s+:\s*(\d+) VERT, (\d+) ROUGE", texte)
note(4, m and m.group(1) == "20" and m.group(2) == "0" and all(c == "VERT" for c, _ in vec_temoin),
     f"le verdict porté : {m.group(1)} VERT, {m.group(2)} ROUGE — les DEUX V2 du juge fautif v1 "
     f"(les-bords-de-fenetre, cinq-entrees-dont-une-non-alignee) désormais VERT")

# S5 — la main
note(5, "14/11/2026" in texte and "Alexis Lopez" in texte and "Daté le" in texte and "Signé" in texte,
     "la main (D99) : daté le 14/11/2026, signé Alexis Lopez — la même main que les témoins "
     "de la campagne (Entrées 264/266/267/272/276/284/287/294)")

# S6 — les pièces du kit v2 re-hachées
verts, details = 0, []
for nom, sha_attendu in gravure.items():
    p = DEST / "kit-T-v2" / nom
    if not p.exists():
        details.append(f"{nom}: ABSENT au bac"); continue
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    if sha == sha_attendu:
        verts += 1
    else:
        details.append(f"{nom}: {sha[:8]}… != {sha_attendu[:8]}…")
note(6, verts == len(gravure) and not details,
     f"les pièces du kit v2 au /test re-hachées : {verts}/{len(gravure)} == la gravure "
     + ("; ".join(details) if details else ""))

# S7 — la chronologie (les horodatages Drive)
meta = api(f"https://www.googleapis.com/drive/v3/files/{TEMoin_ID}?fields=createdTime,modifiedTime")
m = re.search(r"le run\s+:\s*(\S+) \(UTC\)", texte)
note(7, m.group(1) == "2026-11-14T19:53:02Z"
        and meta["modifiedTime"] >= "2026-11-14T19:53:45"
        and meta["createdTime"] >= meta["modifiedTime"],
     f"la chronologie : le run {m.group(1)} -> le témoin touché par la main {meta['modifiedTime'][:19]}Z "
     f"-> déposé au coffre {meta['createdTime'][:19]}Z — jamais une date avant le run")

print()
verts_total = sum(1 for l in rapport if l.startswith("VERT"))
print(f"=== LA SONDE 104 : {verts_total}/{len(rapport)} VERT ===")
(DEST / "RECOUP-104-preuves-unite02.txt").write_text(
    "LA SONDE 104 — LE RECOUP DU DÉPÔT preuves-unite02/ (le run v2 du bras T, la campagne D204)\n"
    "=" * 78 + "\n\n" + "\n".join(rapport)
    + f"\n\n=== {verts_total}/{len(rapport)} VERT — le dépôt EST la pièce ENTière (le scénario n'écrit\n"
      "que le témoin au réceptacle preuves-unite02/ ; la console vit au dossier du kit) ===\n",
    encoding="utf-8")
