#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE DÉPÔT DE LA SESSION 221 — LA VAGUE 0.1.1-dev.1 (la version commandée).

L'ère 0.1.0 est refermée sur sa balise scellée (D178). Le développeur a
commandé « b et c » : la consolidation v0.9.0 de la spécification ET le
soldage de la dette [R10-PÉRIMÉE] à la version 0.1.1+ (D179). LA PIÈCE
0.1.1-dev.1 NAÎT DE LA RECOMPOSITION MÊME : les 17 sommes rafraîchies à
la vérité des blocs, le qword porté 0x00010101, 0 OCTET AILLEURS — le
code byte-identique au vécu des onze runs (R4/R7) ; la carte GÉNÉRATION
17. LE DOUZIÈME RUN est attendu : si le vert tient (le scénario ENTIER
T0 → S0 → LA LIAISON ET la vitrine vivante), LA BALISE `loupe 0.1.1`
SE SCELLERA sur run terrain recoupé (le miroir D165/D170).

Sur le coffre Drive (/test, racine 1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0) :
  A. VERSIONNER LA VAGUE 0.1.1-dev.1 → archives-livraisons/vagues-m10/
     [kit-loupe-0.1.1-dev.1.zip + LISEZMOI-loupe-0.1.1-dev.1.txt]
  B. LA RACINE PORTÉE À LA VAGUE 0.1.1-dev.1 [kit-loupe.zip +
     LISEZMOI-loupe.txt remplacés + loupe-kit-13/ aux QUATRE pièces]
  C. LE RÉCEPTACLE /preuves-loupe/ RÉ-ARMÉ [LISEZMOI-preuves.txt — le
     douzième run attend ses pièces]
  D. L'INDEX DES LIVRAISONS mis à jour [la vague 0.1.1-dev.1 racontée]
Chaque geste recoupe son md5 APRÈS le dépôt (D138/D145/D148) ; le
dépôt VÉRIFIE L'UNICITÉ de chaque nom (la leçon [CORBEILLE-VIDE])."""
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, "/home/z/my-project/triade/scripts")
from drive_api import obtenir_token  # noqa: E402

TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
KIT = "/home/z/my-project/build-011-dev1"
FOLDER_MIME = "application/vnd.google-apps.folder"
TOK = obtenir_token()


def md5(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


MD5_EXE = md5(f"{KIT}/loupe.exe")                  # 5fc07b78…
MD5_SC = md5(f"{KIT}/scenario-loupe.py")           # 77872b71…
MD5_BAT = md5(f"{KIT}/temoin-vitrine.bat")         # 2a3f22f4…
MD5_LIV = md5(f"{KIT}/LISEZMOI-KIT-LOUPE.md")      # 70340163…
MD5_ZIP = md5(f"{KIT}/kit-loupe.zip")              # dadfb48c…

# les attendus de la vague dev.12 (la racine AVANT le geste)
MD5_ZIP_V12 = "a3d9ea3c"
MD5_LIV_V12 = "8ec9553b"

RECEPTACLE = """TRIADE — preuves-loupe : LE RÉCEPTACLE DU DOUZIÈME RUN (l'ère 0.1.1)
========================================================================
(L'ÈRE 0.1.0 EST REFERMÉE : le onzième run recoupé 39/39 — LA BALISE
`loupe 0.1.0` SCELLÉE PAR FAIT DE CARTE [D178], loupe.exe 054de960…
INTACT — LE JALON M10 FRANCHI : la méthode TRIADE entière prouvée par
la CRÉATION, onze runs, onze leçons.)

LA PRÉSENTE VAGUE EST CELLE DE LA VERSION COMMANDÉE : 0.1.1-dev.1
(D178/D179 — le développeur a commandé le soldage de la dette
[R10-PÉRIMÉE] à la version 0.1.1+) : la pièce 0.1.0 scellée portait à
sa porte R10 les SOMMES DE L'ÈRE dev.5 [les retouches des Entrées
210/214 changèrent les octets des blocs sans rafraîchir la table —
dette nommée au scellage même, jamais un hot-fix d'un scellé] ; la
0.1.1 naît de LA RECOMPOSITION : LA DETTE SOLDÉE À LA NAISSANCE [les
17 sommes rafraîchies à la vérité des blocs — chaque somme == son
bloc relu, par construction], le qword version porté 0x00010008 →
0x00010101, 0 OCTET AILLEURS — le code BYTE-IDENTIQUE au vécu des
ONZE RUNS (R4 : le contrat stable ; R7 : les adresses intactes) ;
loupe.exe 0.1.1-dev.1, 127 488 o, sha256 c111510535767a40…, la carte
GÉNÉRATION 17 (la 16 demeure celle de la balise 0.1.0 scellée) ; la
pièce 0.1.0 (054de960…) demeure AU GIT ET AU COFFRE (loupe-kit-12).

LE DOUZIÈME RUN ATTEND SES PIÈCES ICI :
  - temoin-loupe.txt     LE TÉMOIN DU SCÉNARIO (il naît tout seul au
                         run : python scenario-loupe.py) — les temps
                         T0 → T7, la cascade S0, la liaison ;
  - temoin-vitrine.txt   LE TÉMOIN VITRINE REQUIS (temoin-vitrine.bat,
                         avec son [4/4] — le journal d'événements) ;
  - temoin-fichier.bin   la copie que la seconde fenêtre ouvrit (si le
                         cœur vous en dit) ;
  - capture-*.png        les captures de la vitrine, toujours les
                         bienvenues.

LE CRITÈRE (le même que le onzième — la pièce nouvelle à la place de
l'ancienne) : le scénario ENTIER (T0 → S0 → LA LIAISON) ET LA VITRINE
VIVANTE (les deux codes à 0) — SI LE VERT TIENT : LA BALISE `loupe
0.1.1` SCELLÉE sur run terrain recoupé, LA VERSION DE LA DETTE
SOLDÉE (le miroir D165/D170 : la porte est de processus).
"""

INDEX_AJOUT = """
--- la vague loupe 0.1.1-dev.1 VERSIONNÉE À SA NAISSANCE (l'Entrée
    221 : la version COMMANDÉE par le développeur — D179, le soldage
    de la dette [R10-PÉRIMÉE] à 0.1.1+ ; la pièce naît de la
    recomposition même — les 17 sommes rafraîchies à la vérité des
    blocs, le qword porté 0x00010101, 0 OCTET de code changé, le code
    BYTE-IDENTIQUE au vécu des onze runs ; la 0.1.0 [054de960…]
    SCELLÉE demeure au git et au coffre [loupe-kit-12 aux archives]) :
    kit-loupe-0.1.1-dev.1.zip md5 dadfb48c… + LISEZMOI-loupe-0.1.1-
    dev.1.txt md5 70340163… → vagues-m10/ — l'archive poursuit :
    dev.1 → dev.12 + 0.1.1-dev.1.

--- la vague courante (racine de /test) : loupe 0.1.1-dev.1 (kit-loupe.zip
    md5 dadfb48c… + LISEZMOI-loupe.txt md5 70340163… + loupe-kit-13/
    aux QUATRE pièces : loupe.exe 0.1.1-dev.1, 127 488 o, md5
    5fc07b78…, sha256 c1115105…, scenario 77872b71…, bat 2a3f22f4…,
    LISEZMOI 70340163…) : LE DOUZIÈME RUN ATTENDU — si le vert tient
    (le scénario ENTIER T0 → S0 → LA LIAISON + la vitrine vivante),
    LA BALISE `loupe 0.1.1` SCELLÉE sur run recoupé : LA VERSION DE LA
    DETTE SOLDÉE (D179, le miroir D165/D170).
"""


def api_get(path, params):
    import urllib.parse
    url = ("https://www.googleapis.com/drive/v3" + path + "?" +
           urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOK}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def liste_tout(fid):
    return api_get("/files/", {
        "q": f"'{fid}' in parents and trashed = false",
        "fields": "files(id, name, mimeType, md5Checksum, size)",
        "pageSize": 200}).get("files", [])


def upload_conteneur(nom, parent):
    meta = json.dumps({"name": nom, "mimeType": FOLDER_MIME,
                       "parents": [parent]}).encode()
    req = urllib.request.Request("https://www.googleapis.com/drive/v3/files",
                                 data=meta, method="POST",
                                 headers={"Authorization": f"Bearer {TOK}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)["id"]


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


def upload_texte(texte, parent, nom):
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8", newline="\n") as f:
        f.write(texte)
        chemin = f.name
    try:
        return upload(chemin, parent, nom)
    finally:
        os.remove(chemin)


def remplace_texte(texte, parent, nom):
    """Corbeille TOUS les homonymes (l'unicité est la loi), puis dépose."""
    for ancien in trouve_tous(parent, nom):
        corbeille(ancien["id"])
        print(f"    ancien {nom} (md5 {ancien.get('md5Checksum','-')[:8]}…) → corbeille")
    return upload_texte(texte, parent, nom)


def corbeille(fid):
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{fid}",
        method="PATCH",
        data=json.dumps({"trashed": True}).encode(),
        headers={"Authorization": f"Bearer {TOK}",
                 "Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
        return True
    except urllib.error.HTTPError as e:
        print(f"    corbeille ÉCHEC {e.code}")
        return False


def trouve_tous(parent, nom):
    return [f for f in liste_tout(parent) if f["name"] == nom]


def remplace_fichier(chemin, parent, nom):
    """Corbeille TOUS les homonymes (l'unicité est la loi), puis dépose."""
    for ancien in trouve_tous(parent, nom):
        corbeille(ancien["id"])
        print(f"    ancien {nom} (md5 {ancien.get('md5Checksum','-')[:8]}…) → corbeille")
    return upload(chemin, parent, nom)


def recoupe(parent, nom, attendu_md5):
    l = trouve_tous(parent, nom)
    assert len(l) == 1, f"RECOUP : {len(l)} « {nom} » (doublon !)"
    f = l[0]
    assert f and (f.get("md5Checksum") or "").startswith(attendu_md5[:8]), \
        f"RECOUP ÉCHOUÉ : {nom} (md5 {f and f.get('md5Checksum')} != {attendu_md5})"
    print(f"    ✓ {nom} md5 {attendu_md5[:8]}… recoupé (unique)")
    return f["id"]


def telecharge(fid, chemin):
    url = f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOK}"})
    with urllib.request.urlopen(req) as r:
        open(chemin, "wb").write(r.read())


def sans_doublon(parent):
    noms = [f["name"] for f in liste_tout(parent)]
    doubles = sorted({n for n in noms if noms.count(n) > 1})
    assert not doubles, f"DOUBLONS demeurent : {doubles}"
    return len(noms)


# ═════════ A. LA VAGUE 0.1.1-dev.1 VERSIONNÉE → vagues-m10/ ═══════════
print("A. LA VAGUE 0.1.1-dev.1 VERSIONNÉE → archives-livraisons/vagues-m10/")
archives = trouve_tous(TEST, "archives-livraisons")
assert archives and archives[0]["mimeType"] == FOLDER_MIME
vagues = trouve_tous(archives[0]["id"], "vagues-m10")
assert vagues and vagues[0]["mimeType"] == FOLDER_MIME
V = vagues[0]["id"]
for nom, attendu in (("kit-loupe-0.1.1-dev.1.zip", MD5_ZIP),
                     ("LISEZMOI-loupe-0.1.1-dev.1.txt", MD5_LIV)):
    if trouve_tous(V, nom):
        print(f"    {nom} y vit déjà — recoupé")
    else:
        upload(f"{KIT}/{'kit-loupe.zip' if nom.endswith('.zip') else 'LISEZMOI-KIT-LOUPE.md'}",
               V, nom)
        print(f"    {nom} déposé")
    recoupe(V, nom, attendu)
n_v = sans_doublon(V)
print(f"    vagues-m10/ : {n_v} entrées, AUCUN doublon — l'archive poursuit "
      f"(dev.1 → dev.12 + 0.1.1-dev.1)")

# ═════════ B. LA RACINE PORTÉE À LA VAGUE 0.1.1-dev.1 ═════════════════
print("B. LA RACINE PORTÉE À LA VAGUE 0.1.1-dev.1 (kit-loupe.zip + "
      "LISEZMOI-loupe.txt + loupe-kit-13/)")
zip_racine = trouve_tous(TEST, "kit-loupe.zip")
liv_racine = trouve_tous(TEST, "LISEZMOI-loupe.txt")
if (zip_racine and zip_racine[0].get("md5Checksum", "").startswith(MD5_ZIP[:8])
        and liv_racine and liv_racine[0].get("md5Checksum", "").startswith(MD5_LIV[:8])):
    print("    la racine porte DÉJÀ la vague 0.1.1-dev.1 — recoupée, le geste saute")
    recoupe(TEST, "kit-loupe.zip", MD5_ZIP)
    recoupe(TEST, "LISEZMOI-loupe.txt", MD5_LIV)
else:
    ancien_zip = zip_racine
    assert ancien_zip and ancien_zip[0].get("md5Checksum", "").startswith(MD5_ZIP_V12), \
        "le kit-loupe.zip de la racine n'est ni la vague dev.12 attendue ni la 0.1.1 !"
    ancien_liv = liv_racine
    assert ancien_liv and ancien_liv[0].get("md5Checksum", "").startswith(MD5_LIV_V12), \
        "le LISEZMOI-loupe.txt de la racine n'est ni la vague dev.12 attendue ni la 0.1.1 !"
    print(f"    la racine porte bien la vague dev.12 (zip {MD5_ZIP_V12}… + "
          f"lisez-moi {MD5_LIV_V12}…) — le passage se fait")
    remplace_fichier(f"{KIT}/kit-loupe.zip", TEST, "kit-loupe.zip")
    recoupe(TEST, "kit-loupe.zip", MD5_ZIP)
    remplace_fichier(f"{KIT}/LISEZMOI-KIT-LOUPE.md", TEST, "LISEZMOI-loupe.txt")
    recoupe(TEST, "LISEZMOI-loupe.txt", MD5_LIV)

k13 = trouve_tous(TEST, "loupe-kit-13")
if k13:
    print("    loupe-kit-13/ y vit déjà — les pièces recoupées")
    K13 = k13[0]["id"]
else:
    K13 = upload_conteneur("loupe-kit-13", TEST)
    print("    dossier loupe-kit-13/ créé")
for piece, attendu in (("loupe.exe", MD5_EXE), ("scenario-loupe.py", MD5_SC),
                       ("temoin-vitrine.bat", MD5_BAT),
                       ("LISEZMOI-KIT-LOUPE.md", MD5_LIV)):
    if trouve_tous(K13, piece):
        recoupe(K13, piece, attendu)
    else:
        upload(f"{KIT}/{piece}", K13, piece)
        recoupe(K13, piece, attendu)
sans_doublon(K13)

# ═════════ C. LE RÉCEPTACLE RÉ-ARMÉ ═══════════════════════════════════
print("C. LE RÉCEPTACLE /preuves-loupe/ RÉ-ARMÉ (le douzième run attendu)")
rec = trouve_tous(TEST, "preuves-loupe")
assert rec and rec[0]["mimeType"] == FOLDER_MIME
R = rec[0]["id"]
md5_rec = hashlib.md5(RECEPTACLE.encode("utf-8")).hexdigest()
deja = trouve_tous(R, "LISEZMOI-preuves.txt")
if (len(deja) == 1 and deja[0].get("md5Checksum", "").startswith(md5_rec[:8])):
    print("    le réceptacle porte DÉJÀ l'ère 0.1.1 — recoupé, le geste saute")
else:
    remplace_texte(RECEPTACLE, R, "LISEZMOI-preuves.txt")
    print(f"    LISEZMOI-preuves.txt md5 {md5_rec[:8]}… — l'ère 0.1.1 : le "
          f"réceptacle attend les pièces du DOUZIÈME run")
recoupe(R, "LISEZMOI-preuves.txt", md5_rec)

# ═════════ D. L'INDEX DES LIVRAISONS MIS À JOUR ═══════════════════════
print("D. L'INDEX DES LIVRAISONS mis à jour (la vague 0.1.1-dev.1 racontée)")
index = trouve_tous(archives[0]["id"], "LISEZMOI-archives-livraisons.txt")
assert index, "l'index des livraisons est introuvable"
md5_idx_attendu = None
if os.path.exists("/tmp/index-livraisons.txt"):
    md5_idx_attendu = hashlib.md5(
        (open("/tmp/index-livraisons.txt", encoding="utf-8").read()
         + INDEX_AJOUT).encode("utf-8")).hexdigest()
if (md5_idx_attendu and len(index) == 1
        and index[0].get("md5Checksum", "").startswith(md5_idx_attendu[:8])):
    print("    l'index porte DÉJÀ la vague 0.1.1-dev.1 — recoupé, le geste saute")
    recoupe(archives[0]["id"], "LISEZMOI-archives-livraisons.txt", md5_idx_attendu)
else:
    telecharge(index[0]["id"], "/tmp/index-livraisons.txt")
    avec = open("/tmp/index-livraisons.txt", encoding="utf-8").read() + INDEX_AJOUT
    remplace_texte(avec, archives[0]["id"], "LISEZMOI-archives-livraisons.txt")
    md5_idx = hashlib.md5(avec.encode("utf-8")).hexdigest()
    recoupe(archives[0]["id"], "LISEZMOI-archives-livraisons.txt", md5_idx)
    print(f"    l'index porte la vague 0.1.1-dev.1 (md5 {md5_idx[:8]}…)")

# ═════════ LE BILAN ═══════════════════════════════════════════════════
n_racine = sans_doublon(TEST)
print(f"\nLA VAGUE 0.1.1-dev.1 EST DÉPOSÉE : la racine porte {n_racine} "
      f"entrées, AUCUN doublon ; le réceptacle est ARMÉ (le douzième "
      f"run) ; l'archive vagues-m10/ poursuit (dev.1 → dev.12 + "
      f"0.1.1-dev.1) — chaque pièce recoupée par md5")
