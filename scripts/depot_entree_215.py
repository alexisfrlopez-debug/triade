#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE DÉPÔT DE LA SESSION 215 — la vague dev.11 ([RET-NU] nommé avant le run).

Sur le coffre Drive (/test, racine 1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0) :
  A. VERSIONNER LA VAGUE dev.10 (jamais courue) → /archives-livraisons/
     vagues-m10/ [kit-loupe-dev.10.zip + LISEZMOI-loupe-dev.10.txt —
     copie Drive, md5 recoupés APRÈS] — l'archive est COMPLÈTE
     dev.1 → dev.10
  B. DÉPOSER LA VAGUE dev.11 à la racine : kit-loupe.zip (remplacé) +
     loupe-kit-11/ (dossier neuf, quatre pièces) + LISEZMOI-loupe.txt
  C. RÉ-ARMER LE RÉCEPTACLE /preuves-loupe/ [LISEZMOI-preuves.txt —
     l'histoire dev.11, [RET-NU] raconté]
  D. METTRE À JOUR LES DEUX INDEX d'archives (livraisons + preuves)
Chaque geste recoupe son md5 APRÈS le dépôt (D138/D145/D148).
La vague dev.10 n'a JAMAIS couru : aucun témoin ne l'attend aux
archives-preuves — seule sa vague est versionnée.
"""
import hashlib
import json
import os
import sys
import urllib.request

sys.path.insert(0, "/home/z/my-project/scripts")
from drive_api import obtenir_token  # noqa: E402

TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
DEV11 = "/home/z/my-project/build-dev11"
SRC = "/home/z/my-project/scripts"       # les pièces dev.10 recoupées
FOLDER_MIME = "application/vnd.google-apps.folder"
TOK = obtenir_token()

MD5_ZIP_V10_ATTENDU = "4b5e3931"          # la vague dev.10 à la racine
MD5_ZIP11 = hashlib.md5(open(f"{DEV11}/kit-loupe.zip", "rb").read()).hexdigest()
MD5_LIV11 = hashlib.md5(open(f"{DEV11}/LISEZMOI-KIT-LOUPE.md", "rb").read()).hexdigest()
MD5_EXE = hashlib.md5(open(f"{DEV11}/loupe.exe", "rb").read()).hexdigest()


def api_get(path, params):
    import urllib.parse
    url = ("https://www.googleapis.com/drive/v3" + path + "?" +
           urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOK}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def upload_conteneur(nom, parent):
    meta = json.dumps({"name": nom, "mimeType": FOLDER_MIME,
                       "parents": [parent]}).encode()
    req = urllib.request.Request("https://www.googleapis.com/drive/v3/files",
                                 data=meta, method="POST",
                                 headers={"Authorization": f"Bearer {TOK}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)["id"]


def liste_dossier(fid):
    return api_get("/files/", {
        "q": f"'{fid}' in parents and trashed = false",
        "fields": "files(id, name, mimeType, md5Checksum, size)",
        "pageSize": 200}).get("files", [])


def md5(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


def upload(chemin, parent, nom=None):
    import uuid
    nom = nom or os.path.basename(chemin)
    frontiere = uuid.uuid4().hex
    meta = json.dumps({"name": nom, "parents": [parent]})
    corps = open(chemin, "rb").read()
    payload = (f"--{frontiere}\r\n"
               f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
               f"{meta}\r\n"
               f"--{frontiere}\r\n"
               f"Content-Type: application/octet-stream\r\n\r\n").encode() \
        + corps + f"\r\n--{frontiere}--".encode()
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        data=payload, method="POST",
        headers={"Authorization": f"Bearer {TOK}",
                 "Content-Type": f"multipart/related; boundary={frontiere}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)["id"]


def corbeille(fid):
    import urllib.error
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{fid}",
        method="PATCH", data=b"{}",
        headers={"Authorization": f"Bearer {TOK}",
                 "Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
        return True
    except urllib.error.HTTPError as e:
        print(f"    corbeille ÉCHEC {e.code}")
        return False


def trouve(parent, nom):
    for f in liste_dossier(parent):
        if f["name"] == nom:
            return f
    return None


def remplace_fichier(chemin, parent, nom):
    ancien = trouve(parent, nom)
    if ancien:
        corbeille(ancien["id"])
        print(f"    ancien {nom} → corbeille")
    return upload(chemin, parent, nom)


def recoupe(parent, nom, attendu_md5):
    f = trouve(parent, nom)
    assert f and (f.get("md5Checksum") or "").startswith(attendu_md8(attendu_md5)), \
        f"RECOUP ÉCHOUÉ : {nom} (md5 {f and f.get('md5Checksum')} != {attendu_md5})"
    print(f"    ✓ {nom} md5 {attendu_md5[:8]}… recoupé")
    return f["id"]


def attendu_md8(md):
    """Le recoup compare les 8 premiers caractères."""
    return md[:8] if len(md) >= 8 else md


def copie_drive(fichier, parent, nom):
    meta = json.dumps({"name": nom, "parents": [parent]}).encode()
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{fichier['id']}/copy",
        data=meta, method="POST",
        headers={"Authorization": f"Bearer {TOK}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)["id"]


# ═══════════════════ 0. LE RÉCEPTACLE NEUF (le texte avant le dépôt) ═══
rz = open(f"{SRC}/receptacle-LISEZMOI-preuves.txt", encoding="utf-8").read()
assert rz.count("l'entrée neutralisée\nd'un octet ret") == 1, "ancre réceptacle"
rz = rz.replace(
    "LIAISON [une copie chargée SANS DONT_RESOLVE, l'entrée neutralisée\n"
    "d'un octet ret, les 37 slots RELUS : le VRAI chargeur doit y avoir\n"
    "posé les ADRESSES DES FONCTIONS — la liaison vécue au témoin AVANT\n"
    "MÊME LA FENÊTRE]",
    "LIAISON [une copie chargée SANS DONT_RESOLVE, l'entrée neutralisée\n"
    "de SIX OCTETS mov eax, 1 ; ret — [RET-NU] NOMMÉ AVANT LE RUN\n"
    "(l'Entrée 215 : un ret nu eût rendu le verdict ATTACH FAUX au\n"
    "chargeur qui appelle l'entrée en sémantique DllMain ET LIT SON\n"
    "RETOUR — REFUS FAUX, liaison perdue), les 37 slots RELUS : le\n"
    "VRAI chargeur doit y avoir posé les ADRESSES DES FONCTIONS — la\n"
    "liaison vécue au témoin AVANT MÊME LA FENÊTRE]")
assert rz.count("neutralisée d'un octet ret") == 0, "l'octet ret nu demeure"
rz = rz.replace("le kit dev.10 :", "le kit dev.11 ([RET-NU] retouché avant le\nrun — la vague dev.10 ne courut jamais) :")
rz = rz.replace("l'artefact attendu 0.1.0-dev.8, sha256\n054de960c31425d0… — LA RETOUCHÉE DE L'ENTRÉE 214",
                "l'artefact attendu 0.1.0-dev.8, sha256\n054de960c31425d0… — LA RETOUCHÉE DE L'ENTRÉE 214, INTACTE\nÀ L'ENTRÉE 215 (la vague dev.11 est UNE RETOUCHE DU KIT\nSEUL : la pièce n'a pas bougé d'un octet, la carte demeure\ngénération 16)")
rz = rz.replace("si le\ndossier d'un run dev.1 à dev.9 existe encore", "si le\ndossier d'un run dev.1 à dev.10 existe encore")
rz = rz.replace("(loupe-kit-10/ par exemple", "(loupe-kit-10/ par exemple —\nla vague dev.10 retouchée AVANT le run")
rz = rz.replace("le dossier\nloupe-kit-10/ du coffre Drive EST le kit lui-même", "le dossier\nloupe-kit-11/ du coffre Drive EST le kit lui-même")
rz = rz.replace("neuf runs, neuf leçons ; la sixième mort a nommé [OFT-QWORD] : la\nseptième, si elle vient, sera nommée PAR LE JOURNAL D'ÉVÉNEMENTS",
                "neuf runs, neuf leçons ; la sixième mort a nommé [OFT-QWORD] : la\nseptième, si elle vient, sera nommée PAR LE JOURNAL D'ÉVÉNEMENTS ;\nle défaut [RET-NU] fut nommé AVANT le dixième run — la liaison ne\npeut plus être perdue de fausse cause")
open(f"{DEV11}/LISEZMOI-preuves-NEUF.txt", "w", encoding="utf-8", newline="\n").write(rz)
print(f"[0] le réceptacle neuf : {len(rz)} octets — [RET-NU] raconté")

# ═══════════════════ A. LA VAGUE dev.10 VERSIONNÉE ═════════════════════
print("A. LA VAGUE dev.10 VERSIONNÉE → vagues-m10/ (jamais courue)")
archives_liv = trouve(TEST, "archives-livraisons")
assert archives_liv and archives_liv["mimeType"] == FOLDER_MIME
vagues = trouve(archives_liv["id"], "vagues-m10")
assert vagues
zip_v10 = trouve(TEST, "kit-loupe.zip")
assert zip_v10 and zip_v10["md5Checksum"].startswith(MD5_ZIP_V10_ATTENDU), \
    f"le zip racine n'est plus la vague dev.10 : {zip_v10 and zip_v10['md5Checksum']}"
liv_v10 = trouve(TEST, "LISEZMOI-loupe.txt")
assert liv_v10, "le LISEZMOI racine est absent"

if not trouve(vagues["id"], "kit-loupe-dev.10.zip"):
    copie_drive(zip_v10, vagues["id"], "kit-loupe-dev.10.zip")
if not trouve(vagues["id"], "LISEZMOI-loupe-dev.10.txt"):
    copie_drive(liv_v10, vagues["id"], "LISEZMOI-loupe-dev.10.txt")
recoupe(vagues["id"], "kit-loupe-dev.10.zip", zip_v10["md5Checksum"])
recoupe(vagues["id"], "LISEZMOI-loupe-dev.10.txt", liv_v10["md5Checksum"])
print("    vagues-m10 COMPLÈTE dev.1 → dev.10")

# ═══════════════════ B. LA VAGUE dev.11 DÉPOSÉE ════════════════════════
print("B. LA VAGUE dev.11 DÉPOSÉE à la racine du /test")
remplace_fichier(f"{DEV11}/kit-loupe.zip", TEST, "kit-loupe.zip")
recoupe(TEST, "kit-loupe.zip", MD5_ZIP11)

kit11 = trouve(TEST, "loupe-kit-11")
if not kit11:
    id_kit11 = upload_conteneur("loupe-kit-11", TEST)
    print("    dossier loupe-kit-11/ créé")
else:
    id_kit11 = kit11["id"]
for piece in ("LISEZMOI-KIT-LOUPE.md", "loupe.exe", "scenario-loupe.py",
              "temoin-vitrine.bat"):
    if not trouve(id_kit11, piece):
        upload(f"{DEV11}/{piece}", id_kit11, piece)
    recoupe(id_kit11, piece, md5(f"{DEV11}/{piece}"))

remplace_fichier(f"{DEV11}/LISEZMOI-KIT-LOUPE.md", TEST, "LISEZMOI-loupe.txt")
recoupe(TEST, "LISEZMOI-loupe.txt", MD5_LIV11)

# ═══════════════════ C. LE RÉCEPTACLE RÉ-ARMÉ ══════════════════════════
print("C. LE RÉCEPTACLE RÉ-ARMÉ (preuves-loupe/)")
receptacle = trouve(TEST, "preuves-loupe")
assert receptacle
remplace_fichier(f"{DEV11}/LISEZMOI-preuves-NEUF.txt",
                 receptacle["id"], "LISEZMOI-preuves.txt")
recoupe(receptacle["id"], "LISEZMOI-preuves.txt",
        md5(f"{DEV11}/LISEZMOI-preuves-NEUF.txt"))

# ═══════════════════ D. LES DEUX INDEX MIS À JOUR ══════════════════════
print("D. LES DEUX INDEX MIS À JOUR")
archives_preuves = trouve(TEST, "archives-preuves")
assert archives_preuves


def telecharge(fid, chemin):
    url = f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOK}"})
    with urllib.request.urlopen(req) as r:
        open(chemin, "wb").write(r.read())


idx_liv_path = f"{DEV11}/idx-livraisons.txt"
idx_pre_path = f"{DEV11}/idx-preuves.txt"
telecharge(trouve(archives_liv["id"], "LISEZMOI-archives-livraisons.txt")["id"],
           idx_liv_path)
telecharge(trouve(archives_preuves["id"], "LISEZMOI-archives-preuves.txt")["id"],
           idx_pre_path)

with open(idx_liv_path, "a", encoding="utf-8") as f:
    f.write(f"""
--- la vague loupe dev.10 versionnée SANS AVOIR COURU (l'Entrée 215 :
    l'audit de reprise nomma [RET-NU] À L'OCTET PRÈS dans le kit
    lui-même AVANT le run — la sonde de liaison neutralisait
    l'entrée de sa copie d'un seul octet ret ; or sans DONT_RESOLVE
    le VRAI chargeur appelle l'entrée en sémantique DllMain ET LIT
    SON RETOUR : un ret nu rend AL tel qu'il fut à l'appel —
    l'octet de poids faible de l'adresse d'entrée (RVA 0x5C00,
    base 64 Kio-alignée) = 0x00 → le chargeur eût cru
    l'initialisation ÉCHOUÉE : LoadLibraryExW NULL, « REFUS DU
    CHARGEUR » de fausse cause, les 37 slots jamais relus, LA
    LIAISON PERDUE au run de scellement) : kit-loupe.zip md5
    4b5e3931… + LISEZMOI-loupe.txt → vagues-m10/ EN PIÈCES
    VERSIONNÉES [kit-loupe-dev.10.zip + LISEZMOI-loupe-dev.10.txt]
    — l'archive COMPLÈTE dev.1 → dev.10.

--- la vague courante (racine de /test) : loupe dev.11 — LA VAGUE
    DE [RET-NU] NOMMÉ AVANT LE RUN (kit-loupe.zip md5
    {MD5_ZIP11[:8]}… + LISEZMOI-loupe.txt md5 {MD5_LIV11[:8]}… ;
    loupe.exe 0.1.0-dev.8 INTACTE (l'Entrée 214), 127 488 o, md5
    {MD5_EXE[:8]}…, sha256 054de960… — la carte génération 16
    demeure ; LA RETOUCHE DU KIT SEUL : la sonde de liaison
    neutralise désormais l'entrée de sa copie de SIX OCTETS mov
    eax, 1 ; ret — le verdict ATTACH VRAI PAR CONSTRUCTION, le
    DETACH indifférent ; le contrôle D54 étendu et la sonde 205
    réparée demeurent ; le témoin vitrine [4/4] demeure) — livrée
    le 10/11/2026, déposée par le labo en la forme canonique
    kit-loupe.zip + LISEZMOI ET en la forme dossier loupe-kit-11/
    prête à courir ; la balise `loupe 0.1.0` attend le vert
    recoupé : LE JALON M10.
""")

with open(idx_pre_path, "a", encoding="utf-8") as f:
    f.write("""
--- PAS de run archivé pour la vague dev.10 (l'Entrée 215 : elle ne
    courut JAMAIS — le défaut [RET-NU] fut nommé dans le KIT avant
    le geste du terrain ; la vague est versionnée aux
    archives-livraisons, les archives-preuves n'ont rien reçu :
    chaque témoin présent demeure le témoin du run 9 — le dixième
    run est LE GESTE SUIVANT, sur la vague dev.11).
""")

remplace_fichier(idx_liv_path, archives_liv["id"],
                 "LISEZMOI-archives-livraisons.txt")
remplace_fichier(idx_pre_path, archives_preuves["id"],
                 "LISEZMOI-archives-preuves.txt")
print("    les deux index reversés")

print("\nLE DÉPÔT EST COMPLET — le coffre porte la vague dev.11")
print("le geste du terrain : loupe-kit-11/, python scenario-loupe.py,")
print("temoin-vitrine.bat, preuves-loupe/ ENTIER au coffre")
