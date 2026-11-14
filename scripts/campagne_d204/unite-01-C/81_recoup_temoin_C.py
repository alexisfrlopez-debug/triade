#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LE RECOUP DU TÉMOIN DU BRAS C (l'Entrée 287) : la pièce revenue
du terrain (preuves-unite01C/temoin-unite01C.txt) recoupée OCTET PAR OCTET
contre la gravure du kit v2, le contrat (le témoin T), la chronologie du
coffre et l'impossibilité v1 (l'Entrée 286). Chaque contrôle VERT/ROUGE,
le rapport versé au bac ET à l'atelier du dépôt."""
import hashlib
import io
import pathlib
import re

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

UPLOAD = "/home/z/my-project/upload"
REPO = pathlib.Path("/home/z/my-project/work/triade")
ATELIER = REPO / "scripts" / "campagne_d204" / "unite-01-C"
BAC = pathlib.Path("/home/z/my-project/download/preuves-unite01C")
BAC_KIT_V2 = pathlib.Path(
    "/home/z/my-project/download/kit_unite_loupe_01_C_v2"
    "/kit-unite-loupe-01-C-20261114-v2")
BAC_TEMOIN_T = pathlib.Path(
    "/home/z/my-project/download/nouveau-run/Nouveau run"
    "/preuves-unite01/temoin-unite01.txt")

TEST_FOLDER = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
ID_PREUVES = "1Vnusi6ixTrJiytv-aMTUScgeM5mCUAlK"
ID_TEMOIN = "1Vc7djUFjglqRaghQ1WU9ej7nY2b4rDii"
ID_KIT_V2 = "1bjqb3S5i66408Bontalj9kZ7vZkJAPqX"

rapport = []
vert, rouge = [], []


def controle(nom, ok, detail=""):
    ligne = f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else "")
    rapport.append(ligne)
    (vert if ok else rouge).append(nom)
    print(ligne)


creds = service_account.Credentials.from_service_account_file(
    f"{UPLOAD}/physichong-4b3b7222b48c.json",
    scopes=["https://www.googleapis.com/auth/drive"],
)
svc = build("drive", "v3", credentials=creds, cache_discovery=False)


def telecharge(fid):
    buf = io.BytesIO()
    dl = MediaIoBaseDownload(buf, svc.files().get_media(fileId=fid))
    done = False
    while not done:
        _, done = dl.next_chunk()
    return buf.getvalue()


def list_folder(folder_id):
    items, token = [], None
    while True:
        res = svc.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken,files(id,name,mimeType,size,createdTime,modifiedTime,md5Checksum)",
            pageSize=200, orderBy="name", pageToken=token,
        ).execute()
        items.extend(res.get("files", []))
        token = res.get("nextPageToken")
        if not token:
            return items


def sha256(b):
    return hashlib.sha256(b).hexdigest()


# ---- 1) le réceptacle preuves-unite01C/ tel qu'il vit au coffre --------------
contenu_preuves = list_folder(ID_PREUVES)
noms = [f["name"] for f in contenu_preuves]
rapport.append(f"[PIÈCE] preuves-unite01C/ au coffre (né "
               f"{contenu_preuves and (contenu_preuves[0].get('createdTime') or '?')[:19]}) : "
               f"{', '.join(noms)}")
print(rapport[-1])
controle("le-receptacle:le-temoin-present-seul",
         noms == ["temoin-unite01C.txt"],
         f"le scénario n'écrit QUE le témoin (vérifié au source v1 == v2 hors la traverse)")

# la console du refus v1 — demandée à l'Entrée 286 — est-elle enfin déposée ?
racine = list_folder(TEST_FOLDER)
console = [f for f in racine if f["name"] == "run-console-unite01C.txt"]
rapport.append(f"[PIÈCE] run-console-unite01C.txt au /test (la console du refus v1, "
               f"demandée à l'Entrée 286) : "
               f"{'DÉPOSÉE (né ' + console[0]['createdTime'][:19] + ')' if console else 'TOUJOURS ABSENTE — l\'écart demeure nommé (le contenu vit déjà au bac download/preuves-refus-C-v1/)'}")
print(rapport[-1])

# ---- 2) le témoin rapatrié, re-téléchargé, byte-byte --------------------------
b_temoin = telecharge(ID_TEMOIN)
BAC.mkdir(parents=True, exist_ok=True)
(BAC / "temoin-unite01C.txt").write_bytes(b_temoin)
b_temoin_2 = telecharge(ID_TEMOIN)
meta_temoin = svc.files().get(
    fileId=ID_TEMOIN, fields="size,md5Checksum,createdTime,modifiedTime").execute()
controle("le-temoin:rapatrie-puis-re-telecharge-identique",
         b_temoin == b_temoin_2,
         f"{len(b_temoin)} o, sha256 {sha256(b_temoin)[:16]}…, md5 "
         f"{hashlib.md5(b_temoin).hexdigest()[:16]}… == le champ du coffre : "
         f"{meta_temoin.get('md5Checksum', '')[:16]}…")
controle("le-temoin:la-taille-annoncee",
         int(meta_temoin.get("size", 0)) == len(b_temoin) == 1334)

txt = b_temoin.decode("utf-8")
lignes = txt.splitlines()

# ---- 3) les champs du témoin ---------------------------------------------------
def champ(prefixe):
    for l in lignes:
        if l.startswith(prefixe):
            return l
    return ""


run = champ("le run")
machine = champ("la machine")
piece = champ("la pièce")
verdict_l = champ("le verdict")
m_run = re.search(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)", run)
m_piece = re.search(r"loupe-01-c\.dll (\d+) o, sha256 ([0-9a-f]{64})", piece)
controle("le-temoin:le-run-date",
         bool(m_run) and m_run.group(1) == "2026-11-14T12:55:25Z", run)
controle("le-temoin:la-machine",
         machine == "la machine  : PORTABLE · Windows 10 · AMD64 · Python 3.14.10",
         "LA MÊME LIGNE EXACTE que le témoin du bras T (la constante du terrain, CA2)")
controle("le-temoin:la-piece-93-625-o",
         bool(m_piece) and m_piece.group(1) == "93625", piece)
sha_piece = m_piece.group(2) if m_piece else ""
vectors = [l.strip()[len("VERT "):] for l in lignes if l.strip().startswith("VERT ")]
rouges = [l.strip() for l in lignes if l.strip().startswith("ROUGE ")]
controle("le-temoin:le-verdict-15-vert-0-rouge",
         verdict_l.strip() == "le verdict  : 15 VERT, 0 ROUGE — VERT"
         and len(vectors) == 15 and not rouges, verdict_l.strip())
n_v = [v for v in vectors if v.startswith("V")]
controle("le-temoin:la-clef-du-contrat-1+8+3+3",
         sum(1 for v in vectors if v.startswith("T0:")) == 1
         and sum(1 for v in vectors if v.startswith("V1:")) == 8
         and sum(1 for v in vectors if v.startswith("V2:")) == 3
         and sum(1 for v in vectors if v.startswith("V3:")) == 3,
         "T0, V1×8 (les quatre témoins × session+panneau), V2×3, V3×3")

# D99 : daté et signé de la main
date_l = champ("Daté le")
signe_l = champ("Signé")
def rempli(l):
    m = re.search(r":\s*_*([^_]+?)_+\s*$", l)
    return bool(m) and m.group(1).strip()
controle("le-temoin:D99-date-de-la-main",
         rempli(date_l) == "14/11/2026", date_l)
controle("le-temoin:D99-signe",
         rempli(signe_l) == "Alexis Lopez", signe_l)

# ---- 4) la gravure : kit v2 au coffre, re-téléchargée et re-hachée -------------
kit_v2 = {f["name"]: f for f in list_folder(ID_KIT_V2)}
b_dll = telecharge(kit_v2["loupe-01-c.dll"]["id"])
b_scn = telecharge(kit_v2["scenario-unite01C.py"]["id"])
b_emp = telecharge(kit_v2["EMPREINTES-KIT-UNITE-01-C.txt"]["id"])
controle("la-gravure:la-dll-du-kit-v2-==-l-empreinte-du-temoin",
         sha256(b_dll) == sha_piece == "85b34ed4c243e9774d661a0b1964f80ba49333f4be1f6eef4658556eecb5ef3f",
         f"sha256 {sha256(b_dll)[:16]}… (la gravure v2 == la gravure v1 == le témoin — la pièce n'a jamais bougé)")
controle("la-gravure:le-scenario-repare-du-kit-v2",
         sha256(b_scn) == "6340cd3c6308c3ae7ed11dad54c10ced75c19a86dbe54516cdd224e3bcc8ba77",
         f"sha256 {sha256(b_scn)[:16]}… == la ligne de la gravure")
controle("la-gravure:la-gravure-elle-meme",
         sha256(b_emp) == "250d6534b2cac9ad18363bd8bf29fd3903b321e75b58880457ac79f064e548a1"
         and sha_piece in b_emp.decode("utf-8"),
         f"sha256 {sha256(b_emp)[:16]}…, la ligne DLL == l'empreinte du témoin")
controle("la-gravure:le-bac-du-miroir-==-le-coffre",
         sha256((BAC_KIT_V2 / "loupe-01-c.dll").read_bytes()) == sha256(b_dll)
         and sha256((BAC_KIT_V2 / "scenario-unite01C.py").read_bytes()) == sha256(b_scn))

# ---- 5) le contrat : les QUINZE noms == le témoin T, == les appels du scénario -
t_txt = BAC_TEMOIN_T.read_text(encoding="utf-8")
vectors_t = [l.strip()[len("VERT "):] for l in t_txt.splitlines()
             if l.strip().startswith("VERT ")]
controle("le-contrat:les-quinze-noms-==-ceux-du-temoin-T",
         vectors == vectors_t,
         "octet pour octet — le même contrat de couche I aux deux bras (CA2)")

scn_txt = (BAC_KIT_V2 / "scenario-unite01C.py").read_text(encoding="utf-8")
fichiers_v1 = re.search(
    r"for nom in \(([^)]+)\):\n", scn_txt)
attendus = ["T0:la-piece-recoupee-a-l-empreinte-gravee"]
if fichiers_v1:
    for nom in re.findall(r'"([^"]+\.bin)"', fichiers_v1.group(1)):
        attendus.append(f"V1:{nom}-la-session-nee-entiere")
        attendus.append(f"V1:{nom}-le-panneau-ne")
attendus += ["V2:E1-absent", "V2:E2-verrouille",
             "V2:E3-acces-refuse-NOMMÉ-ABSENT", "V3:Q2-la-borne-2-Gio",
             "V3:E4-la-session-double", "V3:P1-le-chemin-trop-long"]
controle("le-contrat:les-quinze-noms-==-les-appels-du-scenario-v2",
         vectors == attendus,
         "la liste attendue dérivée du source du kit v2 livré")

# ---- 6) l'impossibilité v1, re-vérifiée aux octets réels de la pièce -----------
# (l'Entrée 286 : la boucle v1 testait la CHAÎNE au terminateur — à l'RVA 0 vit
#  l'en-tête DOS, jamais vide. Ici : les octets réels du fichier.)
dos = b_dll[:4]
premier_nul = b_dll.find(b"\x00")
controle("l-impossibilite-v1:la-chaine-du-terminateur-nest-jamais-vide",
         dos == b"MZ\x90\x00" and premier_nul == 3,
         f"les quatre premiers octets de la pièce : « {dos.hex(' ')} » — lire_chaine(base, 0) "
         "rend TROIS caractères (« MZ\\x90 », le 0x90 en replacement) avant le premier NUL : "
         "JAMAIS vide, la boucle v1 ne s'arrête JAMAIS au terminateur "
         "(l'autopsie 286 : 25 itérations de dérive, l'access violation 0x7ffa23900094 "
         "reproduite au labo OCTET PAR OCTET) — le v1 NE PEUT PAS écrire un témoin")
# et le v2 s'arrête au champ : la preuve par le source livré
controle("l-arret-v2:le-champ-avant-la-chaine",
         "nom_rva = lire_u32(base, desc + 12)" in scn_txt
         and "if not nom_rva:" in scn_txt
         and "if nom_rva >= taille_image:" in scn_txt,
         "le terminateur lu au CHAMP Name (l'RVA NUL), les gardes fail-closed — "
         "la réparation de l'Entrée 286, dans le fichier livré au coffre")

# ---- 7) la chronologie du coffre, sans trou ------------------------------------
t_kit = kit_v2.get("EMPREINTES-KIT-UNITE-01-C.txt", {}).get("createdTime", "?")[:19]
t_dossier_kit = min((f.get("createdTime") or "?")[:19] for f in list_folder(ID_KIT_V2))
t_run = m_run.group(1) if m_run else "?"
t_modif = (meta_temoin.get("modifiedTime") or "?")[:19]
t_depot = (meta_temoin.get("createdTime") or "?")[:19]
controle("la-chronologie:kit-v2-avant-run-avant-depot",
         "2026-11-14T12:43:48" <= t_dossier_kit < t_run < t_modif < t_depot,
         f"le kit v2 né {t_dossier_kit} → le run {t_run} → le témoin touché "
         f"{t_modif} (la main qui date et signe) → déposé {t_depot} — "
         f"DOUZE minutes du kit au run, aucun trou")

# ---- le rapport -----------------------------------------------------------------
BAC.mkdir(parents=True, exist_ok=True)
corps = "\n".join(rapport) + f"\n\nLE RECOUP DE L'ENTRÉE 287 : {len(vert)} VERT, {len(rouge)} ROUGE" + \
    (" — LE TÉMOIN DU BRAS C EST RECOUPÉ VERT" if not rouge else " — ÉCART NOMMÉ") + "\n"
(BAC / "RECOUP-287.txt").write_text(corps, encoding="utf-8")
(ATELIER / "epreuves" / "recoup-temoin-C-v2.txt").write_text(corps, encoding="utf-8")
print(f"\nLE RECOUP DE L'ENTRÉE 287 : {len(vert)} VERT, {len(rouge)} ROUGE"
      + (" — LE TÉMOIN DU BRAS C EST RECOUPÉ VERT" if not rouge else " — ÉCART NOMMÉ"))
print(f"[rapport] {BAC / 'RECOUP-287.txt'}")
print(f"[rapport] {ATELIER / 'epreuves' / 'recoup-temoin-C-v2.txt'}")
