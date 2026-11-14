#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LE RECOUP DES PIÈCES NEUVES DU /test (l'annonce du développeur :
« j'ai déposé ce que tu m'as demandé ») :
  1. /run-console-unite01C.txt (racine, né 13:30:08, 5 040 o)
  2. /kit-unite-loupe-01-C-20261114-v2/run-console-unite01C.txt (né 13:31:58)
  3. /kit-unite-loupe-01-C-20261114-v2/preuves-unite01C/temoin-unite01C.txt
Chaque pièce : rapatriée DEUX FOIS, byte-byte identiques, sha256/md5 ;
le témoin du kit == le témoin du coffre (4cc0ee2b…) ; les consoles décodées
(BOM détectée) et confrontées : refus v1 (access violation, code 1) ou run
v2 (15 VERT) ? et la console racine == la pièce du chat (bac du refus) ?"""
import hashlib
import json
import pathlib

from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
BAC_REFUS = pathlib.Path("/home/z/my-project/download/preuves-refus-C-v1")
BAC_KIT_V2 = pathlib.Path(
    "/home/z/my-project/download/kit_unite_loupe_01_C_v2/kit-unite-loupe-01-C-20261114-v2")

PIECES = {
    "console-racine": ("1gkej-kqC3NCL_HH5ayfm9tKyCV0lpmHo",
                       BAC_REFUS / "run-console-unite01C-depot-test.txt"),
    "console-kit-v2": ("1h5jwZJFmK-Rk_FJQ7ncLwsplwUUSsAiB",
                       BAC_KIT_V2 / "run-console-unite01C.txt"),
    "temoin-kit-v2": ("1qxFPS-WiRx15s_2Bno4qtqyW7kd1TQir",
                      BAC_KIT_V2 / "preuves-unite01C" / "temoin-unite01C.txt"),
    "temoin-coffre": ("1Vc7djUFjglqRaghQ1WU9ej7nY2b4rDii", None),
}

creds = service_account.Credentials.from_service_account_file(
    f"{UPLOAD}/physichong-4b3b7222b48c.json",
    scopes=["https://www.googleapis.com/auth/drive"])
svc = build("drive", "v3", credentials=creds, cache_discovery=False)

def telecharger(fid):
    return svc.files().get_media(fileId=fid).execute()

rapport = []
contenus = {}
for nom, (fid, chemin_bac) in PIECES.items():
    a, b = telecharger(fid), telecharger(fid)   # rapatrié DEUX FOIS
    identique = a == b
    sha = hashlib.sha256(a).hexdigest()
    md5 = hashlib.md5(a).hexdigest()
    contenus[nom] = a
    vert = identique
    rapport.append(f"[{'VERT' if vert else 'ROUGE'}] {nom} : {len(a):,} o, "
                   f"sha256 {sha[:16]}…, md5 {md5[:12]}… — "
                   f"{'deux téléchargements IDENTIQUES' if identique else 'DIVERGENT !'}")
    if chemin_bac:
        chemin_bac.parent.mkdir(parents=True, exist_ok=True)
        chemin_bac.write_bytes(a)
        ok_bac = chemin_bac.read_bytes() == a
        rapport.append(f"[{'VERT' if ok_bac else 'ROUGE'}] {nom} : versé au bac {chemin_bac}")

# ---- le témoin du kit == le témoin du coffre ? --------------------------------
ok_t = contenus["temoin-kit-v2"] == contenus["temoin-coffre"]
rapport.append(f"[{'VERT' if ok_t else 'ROUGE'}] le témoin au kit v2 "
               f"{'==' if ok_t else '!='} le témoin du coffre /preuves-unite01C/"
               f" (sha256 {hashlib.sha256(contenus['temoin-kit-v2']).hexdigest()[:16]}…)")

# ---- les deux consoles entre elles ---------------------------------------------
ok_c = contenus["console-racine"] == contenus["console-kit-v2"]
rapport.append(f"[INFO] la console racine {'==' if ok_c else '!='} la console au kit v2 "
               f"(octet pour octet)")

# ---- la console racine vs la pièce du chat (bac du refus) ----------------------
piece_chat = (BAC_REFUS / "run-console-unite01C-recu-chat.txt").read_bytes()
ok_chat = contenus["console-racine"] == piece_chat
rapport.append(f"[{'VERT' if ok_chat else 'ÉCART'}] la console racine "
               f"{'==' if ok_chat else '!='} la pièce du chat consignée au bac "
               f"({len(piece_chat):,} o)")

# ---- décodage des consoles -----------------------------------------------------
def decoder(brut):
    if brut[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return brut.decode("utf-16"), "utf-16 (BOM)"
    for enc in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return brut.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return brut.decode("latin-1"), "latin-1 (repli)"

for nom in ("console-racine", "console-kit-v2"):
    texte, enc = decoder(contenus[nom])
    lignes = [l for l in texte.splitlines() if l.strip()]
    rapport.append(f"\n----- {nom} : décodée « {enc} », {len(lignes)} lignes vives -----")
    for l in lignes:
        rapport.append(f"  | {l}")

# ---- les marqueurs attendus -----------------------------------------------------
racine_txt = decoder(contenus["console-racine"])[0]
kit_txt = decoder(contenus["console-kit-v2"])[0]
def marqueurs(txt):
    return {
        "access-violation": "access violation" in txt.lower(),
        "code-1": "code 1" in txt.lower(),
        "15-vert": "15 VERT" in txt or "15 VERT" in txt.replace("  ", " "),
        "vert-total": "VERT" in txt and "ROUGE" not in txt.upper().replace("0 ROUGE", ""),
        "temoin-ne": "temoin" in txt.lower(),
        "adresse-exacte": "0x7ffa23900094" in txt.lower().replace("0x7FFA", "0x7ffa"),
        "base-0x7ff9b74d0000": "0x7ff9b74d0000" in txt.lower(),
    }
for nom, txt in (("console-racine", racine_txt), ("console-kit-v2", kit_txt)):
    m = marqueurs(txt)
    rapport.append(f"\n[marqueurs] {nom} : " + ", ".join(
        f"{k}={'OUI' if v else 'non'}" for k, v in m.items()))

print("\n".join(rapport))
pathlib.Path("/home/z/my-project/scripts/78_recoupe_depot.txt").write_text(
    "\n".join(rapport), encoding="utf-8")
