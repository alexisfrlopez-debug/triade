#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE DÉPÔT DE LA SESSION — la cérémonie du run 9 et de la vague dev.10.

Sur le coffre Drive (/test, racine 1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0) :
  A. ARCHIVER LE RUN 9 → /archives-preuves/preuves-run-loupe-dev9/
     [VERDICT-run-loupe-dev9.txt + temoin-loupe.txt + temoin-vitrine.txt]
  B. VIDER le dossier du run (/kit-loupe/preuves-loupe → corbeille : les
     preuves sont archivées, le dossier du kit demeure comme loupe-kit-8)
  C. VERSIONNER LA VAGUE dev.9 → /archives-livraisons/vagues-m10/
     [kit-loupe-dev.9.zip + LISEZMOI-loupe-dev.9.txt — md5 recoupés]
  D. DÉPOSER LA VAGUE dev.10 à la racine : kit-loupe.zip (remplacé) +
     loupe-kit-10/ (dossier neuf, quatre pièces) + LISEZMOI-loupe.txt
  E. RÉ-ARMER LE RÉCEPTACLE /preuves-loupe/ [LISEZMOI-preuves.txt]
  F. METTRE À JOUR LES DEUX INDEX d'archives (livraisons + preuves)
Chaque geste recoupe son md5 APRÈS le dépôt (D138/D145/D148).
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, "/home/z/my-project/scripts")
from drive_api import _get, obtenir_token  # noqa: E402
import urllib.request  # noqa: E402

TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
RUN9 = "/home/z/my-project/run9"
DEV10 = "/home/z/my-project/build-dev10"
FOLDER_MIME = "application/vnd.google-apps.folder"
TOK = obtenir_token()


def api_get(path, params):
    import urllib.parse
    url = ("https://www.googleapis.com/drive/v3" + path + "?" +
           urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOK}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def upload_conteneur(nom, parent):
    """Crée un dossier Drive, retourne son id."""
    import urllib.request as ur
    meta = json.dumps({"name": nom, "mimeType": FOLDER_MIME,
                       "parents": [parent]}).encode()
    req = ur.Request("https://www.googleapis.com/drive/v3/files",
                     data=meta, method="POST",
                     headers={"Authorization": f"Bearer {TOK}",
                              "Content-Type": "application/json"})
    with ur.urlopen(req) as r:
        return json.load(r)["id"]


def liste_dossier(fid):
    rep = api_get("/files/", {
        "q": f"'{fid}' in parents and trashed = false",
        "fields": "files(id, name, mimeType, md5Checksum, size)",
        "pageSize": 200})
    return rep.get("files", [])


def md5(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


def upload(chemin, parent, nom=None):
    """Téléverse (multipart) un fichier, retourne l'id."""
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
    """Supprime l'ancien (corbeille) et téléverse le neuf."""
    ancien = trouve(parent, nom)
    if ancien:
        corbeille(ancien["id"])
        print(f"    ancien {nom} → corbeille")
    return upload(chemin, parent, nom)


def recoupe(parent, nom, attendu_md5):
    f = trouve(parent, nom)
    assert f and f.get("md5Checksum") == attendu_md5, \
        f"RECOUP ÉCHOUÉ : {nom} (md5 {f and f.get('md5Checksum')} != {attendu_md5})"
    print(f"    ✓ {nom} md5 {attendu_md5[:8]}… recoupé")
    return f["id"]


# ═══════════════════════ A. L'ARCHIVE DU RUN 9 ═══════════════════════════
print("A. L'ARCHIVE DU RUN 9 → archives-preuves/preuves-run-loupe-dev9/")
archives_preuves = trouve(TEST, "archives-preuves")
assert archives_preuves and archives_preuves["mimeType"] == FOLDER_MIME
dossier_run9 = trouve(archives_preuves["id"], "preuves-run-loupe-dev9")
if not dossier_run9:
    dossier_run9 = {"id": upload_conteneur("preuves-run-loupe-dev9",
                                           archives_preuves["id"])}
    print("    dossier créé")
else:
    print("    dossier existant — les pièces s'y ajoutent")

for piece, src in (("VERDICT-run-loupe-dev9.txt",
                    f"{DEV10}/VERDICT-run-loupe-dev9.txt"),
                   ("temoin-loupe.txt", f"{RUN9}/preuves-loupe/temoin-loupe.txt"),
                   ("temoin-vitrine.txt",
                    f"{RUN9}/preuves-loupe/temoin-vitrine.txt")):
    if not trouve(dossier_run9["id"], piece):
        upload(src, dossier_run9["id"], piece)
    recoupe(dossier_run9["id"], piece, md5(src))

# ═══════════════════ B. LE DOSSIER DU RUN VIDÉ ═══════════════════════════
print("B. LE DOSSIER DU RUN VIDÉ (les preuves sont archivées)")
kit_loupe = trouve(TEST, "kit-loupe")
assert kit_loupe and kit_loupe["mimeType"] == FOLDER_MIME
preuves_dans_kit = trouve(kit_loupe["id"], "preuves-loupe")
if preuves_dans_kit:
    corbeille(preuves_dans_kit["id"])
    print("    /kit-loupe/preuves-loupe → corbeille (archivé en A)")
reste = [f["name"] for f in liste_dossier(kit_loupe["id"])]
print(f"    /kit-loupe demeure (le dossier du run, comme loupe-kit-8) : {reste}")

# ═══════════════════ C. LA VAGUE dev.9 VERSIONNÉE ════════════════════════
print("C. LA VAGUE dev.9 VERSIONNÉE → vagues-m10/")
archives_liv = trouve(TEST, "archives-livraisons")
assert archives_liv
vagues = trouve(archives_liv["id"], "vagues-m10")
assert vagues
zip_dev9 = trouve(TEST, "kit-loupe.zip")
assert zip_dev9 and zip_dev9["md5Checksum"].startswith("a7a6bb76"), \
    f"le zip racine n'est plus la vague dev.9 : {zip_dev9 and zip_dev9['md5Checksum']}"
lisezmoi_dev9 = trouve(TEST, "LISEZMOI-loupe.txt")
assert lisezmoi_dev9 and lisezmoi_dev9["md5Checksum"].startswith("44a36c85"), \
    f"le LISEZMOI racine n'est plus celui du dev.9 : {lisezmoi_dev9 and lisezmoi_dev9['md5Checksum']}"

def copie_drive(fichier, parent, nom):
    """Copie un fichier Drive existant vers un autre parent."""
    import urllib.request as ur
    meta = json.dumps({"name": nom, "parents": [parent]}).encode()
    req = ur.Request(
        f"https://www.googleapis.com/drive/v3/files/{fichier['id']}/copy",
        data=meta, method="POST",
        headers={"Authorization": f"Bearer {TOK}",
                 "Content-Type": "application/json"})
    with ur.urlopen(req) as r:
        return json.load(r)["id"]

if not trouve(vagues["id"], "kit-loupe-dev.9.zip"):
    copie_drive(zip_dev9, vagues["id"], "kit-loupe-dev.9.zip")
if not trouve(vagues["id"], "LISEZMOI-loupe-dev.9.txt"):
    copie_drive(lisezmoi_dev9, vagues["id"], "LISEZMOI-loupe-dev.9.txt")
recoupe(vagues["id"], "kit-loupe-dev.9.zip", zip_dev9["md5Checksum"])
recoupe(vagues["id"], "LISEZMOI-loupe-dev.9.txt", lisezmoi_dev9["md5Checksum"])
print("    vagues-m10 COMPLÈTE dev.1 → dev.9")

# ═══════════════════ D. LA VAGUE dev.10 DÉPOSÉE ══════════════════════════
print("D. LA VAGUE dev.10 DÉPOSÉE à la racine du /test")
remplace_fichier(f"{DEV10}/kit-loupe.zip", TEST, "kit-loupe.zip")
recoupe(TEST, "kit-loupe.zip", md5(f"{DEV10}/kit-loupe.zip"))

kit10 = trouve(TEST, "loupe-kit-10")
if not kit10:
    id_kit10 = upload_conteneur("loupe-kit-10", TEST)
    print("    dossier loupe-kit-10/ créé")
else:
    id_kit10 = kit10["id"]
for piece in ("LISEZMOI-KIT-LOUPE.md", "loupe.exe", "scenario-loupe.py",
              "temoin-vitrine.bat"):
    if not trouve(id_kit10, piece):
        upload(f"{DEV10}/loupe-kit-10/{piece}", id_kit10, piece)
    recoupe(id_kit10, piece, md5(f"{DEV10}/loupe-kit-10/{piece}"))

remplace_fichier(f"{DEV10}/LISEZMOI-KIT-LOUPE.md", TEST, "LISEZMOI-loupe.txt")
recoupe(TEST, "LISEZMOI-loupe.txt", md5(f"{DEV10}/LISEZMOI-KIT-LOUPE.md"))

# ═══════════════════ E. LE RÉCEPTACLE RÉ-ARMÉ ════════════════════════════
print("E. LE RÉCEPTACLE RÉ-ARMÉ (preuves-loupe/)")
receptacle = trouve(TEST, "preuves-loupe")
assert receptacle
remplace_fichier(f"{DEV10}/LISEZMOI-preuves-NEUF.txt",
                 receptacle["id"], "LISEZMOI-preuves.txt")
recoupe(receptacle["id"], "LISEZMOI-preuves.txt",
        md5(f"{DEV10}/LISEZMOI-preuves-NEUF.txt"))

# ═══════════════════ F. LES DEUX INDEX MIS À JOUR ════════════════════════
print("F. LES DEUX INDEX MIS À JOUR")
# télécharger, appending, reverser
def telecharge(fid, chemin):
    url = f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOK}"})
    with urllib.request.urlopen(req) as r:
        open(chemin, "wb").write(r.read())

idx_liv_path = "/home/z/my-project/run9/idx-livraisons.txt"
idx_pre_path = "/home/z/my-project/run9/idx-preuves.txt"
telecharge(trouve(archives_liv["id"], "LISEZMOI-archives-livraisons.txt")["id"],
           idx_liv_path)
telecharge(trouve(archives_preuves["id"], "LISEZMOI-archives-preuves.txt")["id"],
           idx_pre_path)

MD5_ZIP10 = md5(f"{DEV10}/kit-loupe.zip")
MD5_LIV10 = md5(f"{DEV10}/LISEZMOI-KIT-LOUPE.md")
MD5_EXE10 = md5(f"{DEV10}/loupe.exe")

with open(idx_liv_path, "a", encoding="utf-8") as f:
    f.write(f"""
--- la vague loupe dev.9 archivée (consommée par le neuvième run,
    l'Entrée 214) : kit-loupe.zip md5 a7a6bb76… + LISEZMOI-loupe.txt
    md5 44a36c85… → vagues-m10/ EN PIÈCES VERSIONNÉES
    [kit-loupe-dev.9.zip + LISEZMOI-loupe-dev.9.txt] ; le terrain l'a
    vécue en kit-loupe/ : T0→T7 TOUT VERT pour la seconde fois, puis
    [PERMISSION-SONDE] au S0 et la vitrine morte pour la sixième
    fois — NOMMÉE par le journal d'événements [4/4] puis par le labo
    [OFT-QWORD] : la pièce retouchée dev.8.

--- la vague courante (racine de /test) : loupe dev.10 — LA VAGUE DE
    LA LIAISON VÉCUE (kit-loupe.zip md5 {MD5_ZIP10[:8]}… +
    LISEZMOI-loupe.txt md5 {MD5_LIV10[:8]}… ; loupe.exe 0.1.0-dev.8
    LA RETOUCHÉE DE L'ENTRÉE 214, 127 488 o, md5 {MD5_EXE10[:8]}…,
    sha256 054de960… — les QUATRE OFT compactés au pas DWORD du
    chargeur [OFT-QWORD] nommé au run 9, 89 octets en tout, le
    .text/.text2/.data octet-identiques, les adresses scellées
    intactes ; ET LE SCÉNARIO dev.10 : LE CONTRÔLE D54 ÉTENDU [les
    QUATRE OFT marchés au pas DWORD, chaque entrée == le
    préremplissage de son slot], LA SONDE 205 RÉPARÉE DE SON PROPRE
    NETTOYAGE [FreeLibrary avant suppression, chaque essai dans son
    try], ET LA NOUVELLE SONDE DE LIAISON [une copie chargée SANS
    DONT_RESOLVE, l'entrée neutralisée d'un octet ret, les 37 slots
    relus : le VRAI chargeur doit y avoir posé les ADRESSES DES
    FONCTIONS] ; ET LE TÉMOIN VITRINE dev.10 : [4/4] le journal
    d'événements demeure) — livrée le 10/11/2026, déposée par le
    labo en la forme canonique kit-loupe.zip + LISEZMOI ET en la
    forme dossier loupe-kit-10/ prête à courir ; la balise `loupe
    0.1.0` attend le vert recoupé : LE JALON M10.
""")

MD5_TL9 = md5(f"{RUN9}/preuves-loupe/temoin-loupe.txt")
MD5_TV9 = md5(f"{RUN9}/preuves-loupe/temoin-vitrine.txt")
MD5_VERDICT = md5(f"{DEV10}/VERDICT-run-loupe-dev9.txt")

with open(idx_pre_path, "a", encoding="utf-8") as f:
    f.write(f"""
--- le run loupe dev.9 archivé (le neuvième run, l'Entrée 214) :
    T0→T7 TOUT VERT POUR LA SECONDE FOIS [le contrôle D54 vert, la
    boucle d'édition, LES QUATRE REJETS DU T6 : -2, -5, -3, -1, la
    clôture T7 : l'artefact relu inchangé] ; [S0] ÉCHEC NOMMÉ
    [PERMISSION-SONDE] : PermissionError(13) — la réparation dev.9
    vécut (l'AttributeError est morte) mais la cascade mourut sur
    SON PROPRE NETTOYAGE (un module chargé ne se supprime pas :
    FreeLibrary manquait) ; ET LA VITRINE MORTE ×2 0xC0000005 — LA
    SIXIÈME MORT — NOMMÉE PAR LE SYSTÈME [le témoin portant [4/4] :
    BEX64, module « unknown », P9=8 exécution sur mémoire non
    exécutable] PUIS PAR LE LABO [OFT-QWORD : les QUATRE OFT à pas
    de qword — le chargeur lisait OFT[1]=0, résolvait UNE fonction
    par DLL, laissait 33 slots à leur valeur fichier — le second
    appel de l'entrée sautait à 0x2A53 : LA MORT NOMMÉE] ; témoins
    temoin-loupe.txt 3 650 o md5 {MD5_TL9[:8]}… + temoin-vitrine.txt
    4 049 o md5 {MD5_TV9[:8]}… archivés à preuves-run-loupe-dev9/
    AVEC le verdict md5 {MD5_VERDICT[:8]}… [la retouche de l'Entrée
    214 : la pièce dev.8 (les OFT compactés, 89 octets) + le kit
    dev.10 — le contrôle D54 ÉTENDU, la sonde 205 réparée, LA SONDE
    DE LIAISON : la sixième mort ne passera plus jamais].
""")

remplace_fichier(idx_liv_path, archives_liv["id"],
                 "LISEZMOI-archives-livraisons.txt")
remplace_fichier(idx_pre_path, archives_preuves["id"],
                 "LISEZMOI-archives-preuves.txt")
print("    les deux index reversés")

print("\nLA CÉRÉMONIE DU DÉPÔT EST COMPLÈTE — le coffre porte la vague dev.10")
