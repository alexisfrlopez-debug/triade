#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE DÉPÔT DE LA SESSION 217 — le onzième run recoupé, le jalon débloquent.

LE ONZIÈME RUN (kit dev.12) : T0 → T7 TOUT VERT POUR LA QUATRIÈME
FOIS, LA CASCADE 205 VÉCUE ENTIÈRE POUR LA PREMIÈRE FOIS, LA VITRINE
VIVANTE LA SECONDE FOIS (0 et 0) — ET LE HUITIÈME DÉFAUT NOMMÉ SUR
PIÈCES : [SONDE-EXE], le faux négatif STRUCTUREL de la sonde de
liaison (loupe.exe est un EXE : le bit DLL absent du COFF, et le
chargeur de bibliothèque ne résout JAMAIS les imports d'un module
exécutable — Microsoft Learn, LoadLibraryExA) ; LA LIAISON EST
PROUVÉE PAR LE VIVANT (la vitrine, deux runs, la même pièce).
LE RECOUP 39/39 VERT : LE VERT TIENT ENTIER — LA BALISE `loupe 0.1.0`
DÉBLOQUÉE ; le scellage (fait de carte, D104) est le chantier du
labo, la dette de la carte (l'Entrée 211) en est le préalable.

Sur le coffre Drive (/test, racine 1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0) :
  A. ARCHIVER LE RUN 11 → archives-preuves/preuves-run-loupe-dev12/
     [VERDICT-run-loupe-dev12.txt + les DEUX témoins — les octets
     rapatriés et recoupés du dossier du run kit-loupe/]
  B. NETTOYER LE DOSSIER DU RUN : kit-loupe/ → corbeille (les témoins
     sont archivés ; les QUATRE pièces == loupe-kit-12/ dev.12, octet
     pour octet, recoupées par md5 AVANT le geste — D99/D143)
  C. VERSIONNER LA VAGUE dev.12 → archives-livraisons/vagues-m10/
     [kit-loupe-dev.12.zip + LISEZMOI-loupe-dev.12.txt — copies Drive
     des fichiers de la racine, md5 recoupés APRÈS — l'archive devient
     COMPLÈTE dev.1 → dev.12 ; la vague demeurant AUSSI à la racine :
     c'est LA VAGUE DU SCELLEMENT, courue et validée]
  D. LA RACINE DEMEURE À LA VAGUE dev.12 (kit-loupe.zip + LISEZMOI-
     loupe.txt + loupe-kit-12/ — recoupés, sans doublon) : plus
     AUCUNE vague neuve n'est déposée — le jalon n'attend plus un
     run, il attend son fait de carte.
  E. RÉ-ARMER LE RÉCEPTACLE /preuves-loupe/ [LISEZMOI-preuves.txt —
     l'ère du JALON DÉBLOQUÉ : plus aucune pièce attendue, les
     captures demeurent bienvenues]
  F. METTRE À JOUR LES DEUX INDEX d'archives (livraisons + preuves).
Chaque geste recoupe son md5 APRÈS le dépôt (D138/D145/D148).
"""
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, "/home/z/my-project/triade/scripts")
from drive_api import obtenir_token  # noqa: E402

TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
DEV12 = "/home/z/my-project/build-dev12"
RUN12 = "/home/z/my-project/upload/run-dev12"   # les octets recoupés du run 11
FOLDER_MIME = "application/vnd.google-apps.folder"
TOK = obtenir_token()


def md5(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


MD5_ZIP12 = md5(f"{DEV12}/kit-loupe.zip")
MD5_LIV12 = md5(f"{DEV12}/LISEZMOI-KIT-LOUPE.md")
MD5_VERDICT = md5(f"{DEV12}/VERDICT-run-loupe-dev12.txt")
MD5_RECEPTACLE = md5(f"{DEV12}/LISEZMOI-preuves-JALON.txt")
MD5_TEMOIN_LOUPE = md5(f"{RUN12}/temoin-loupe.txt")
MD5_TEMOIN_VITRINE = md5(f"{RUN12}/temoin-vitrine.txt")

MD5_ZIP_V12 = "a3d9ea3c"   # la vague dev.12 à la racine (courue au run 11)
MD5_LIV_V12 = "8ec9553b"   # le LISEZMOI dev.12 à la racine
MD5_EXE_V8 = "074881be634119c2c3f6babeaeef9684"
MD5_SC_V12 = "7353e7342ff056eeb428f0d78445a7de"
MD5_BAT_V12 = "2d3bc31f54c7140de1d931be0d80fb93"


def api_get(path, params):
    import urllib.parse
    url = ("https://www.googleapis.com/drive/v3" + path + "?" +
           urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOK}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def liste_tout(fid):
    """Liste TOUTES les entrées (les doublons de nom ne se cachent pas)."""
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


def trouve(parent, nom):
    l = trouve_tous(parent, nom)
    return l[0] if l else None


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


def copie_drive(fichier, parent, nom):
    meta = json.dumps({"name": nom, "parents": [parent]}).encode()
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{fichier['id']}/copy",
        data=meta, method="POST",
        headers={"Authorization": f"Bearer {TOK}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)["id"]


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


# ═════════ A. LE RUN 11 ARCHIVÉ → preuves-run-loupe-dev12/ ═══════════════
print("A. LE RUN 11 ARCHIVÉ → archives-preuves/preuves-run-loupe-dev12/")
archives_preuves = trouve(TEST, "archives-preuves")
assert archives_preuves and archives_preuves["mimeType"] == FOLDER_MIME
run12 = trouve(archives_preuves["id"], "preuves-run-loupe-dev12")
if not run12:
    id_run12 = upload_conteneur("preuves-run-loupe-dev12", archives_preuves["id"])
    print("    dossier preuves-run-loupe-dev12/ créé")
else:
    id_run12 = run12["id"]
for piece, attendu in (("temoin-loupe.txt", MD5_TEMOIN_LOUPE),
                       ("temoin-vitrine.txt", MD5_TEMOIN_VITRINE)):
    if not trouve(id_run12, piece):
        upload(f"{RUN12}/{piece}", id_run12, piece)
    recoupe(id_run12, piece, attendu)
if not trouve(id_run12, "VERDICT-run-loupe-dev12.txt"):
    upload(f"{DEV12}/VERDICT-run-loupe-dev12.txt", id_run12,
           "VERDICT-run-loupe-dev12.txt")
recoupe(id_run12, "VERDICT-run-loupe-dev12.txt", MD5_VERDICT)
assert sans_doublon(id_run12) == 3
print("    le run 11 archivé : VERDICT + les DEUX témoins, sans doublon")

# ═════════ B. LE DOSSIER DU RUN NETTOYÉ (D99/D143) ═══════════════════════
print("B. LE DOSSIER DU RUN NETTOYÉ : kit-loupe/ → corbeille (archivé)")
kit_run = trouve(TEST, "kit-loupe")
assert kit_run, "le dossier du run kit-loupe/ est absent du /test"
pieces_run = {f["name"]: f for f in liste_tout(kit_run["id"])}
preuves_run = liste_tout(pieces_run["preuves-loupe"]["id"])
assert {f["name"] for f in preuves_run} == {"temoin-loupe.txt",
                                            "temoin-vitrine.txt"}
for f in preuves_run:
    assert f.get("md5Checksum", "").startswith(
        MD5_TEMOIN_LOUPE[:8] if f["name"] == "temoin-loupe.txt"
        else MD5_TEMOIN_VITRINE[:8]), f"le témoin {f['name']} diverge"
# les QUATRE pièces du kit du run == la vague dev.12 (loupe-kit-12/ et le
# dépôt), octet pour octet (recoup AVANT le geste) ; temoin-fichier.bin
# == loupe.exe (la copie que la seconde fenêtre ouvrit)
for piece, attendu in (("loupe.exe", MD5_EXE_V8), ("scenario-loupe.py", MD5_SC_V12),
                       ("temoin-vitrine.bat", MD5_BAT_V12),
                       ("temoin-fichier.bin", MD5_EXE_V8)):
    assert pieces_run[piece].get("md5Checksum", "").startswith(attendu[:8]), \
        f"la pièce {piece} du run diverge de la vague dev.12"
kit12 = {f["name"]: f for f in liste_tout(trouve(TEST, "loupe-kit-12")["id"])}
assert kit12["loupe.exe"]["md5Checksum"].startswith(MD5_EXE_V8[:8])
assert kit12["scenario-loupe.py"]["md5Checksum"].startswith(MD5_SC_V12[:8])
print("    les QUATRE pièces + temoin-fichier.bin == la vague dev.12, "
      "les DEUX témoins archivés — le dossier peut mourir")
corbeille(kit_run["id"])
assert not trouve(TEST, "kit-loupe"), "kit-loupe/ demeure !"
print("    kit-loupe/ → corbeille (les preuves vivent aux archives)")

# ═════════ C. LA VAGUE dev.12 VERSIONNÉE ═════════════════════════════════
print("C. LA VAGUE dev.12 VERSIONNÉE → vagues-m10/ (courue au run 11)")
archives_liv = trouve(TEST, "archives-livraisons")
assert archives_liv
vagues = trouve(archives_liv["id"], "vagues-m10")
assert vagues
zips12 = [f for f in trouve_tous(TEST, "kit-loupe.zip")
          if (f.get("md5Checksum") or "").startswith(MD5_ZIP_V12)]
livs12 = [f for f in trouve_tous(TEST, "LISEZMOI-loupe.txt")
          if (f.get("md5Checksum") or "").startswith(MD5_LIV_V12)]
assert len(zips12) == 1 and len(livs12) == 1, \
    f"la vague dev.12 à la racine : {len(zips12)} zip, {len(livs12)} LISEZMOI"
if not trouve(vagues["id"], "kit-loupe-dev.12.zip"):
    copie_drive(zips12[0], vagues["id"], "kit-loupe-dev.12.zip")
if not trouve(vagues["id"], "LISEZMOI-loupe-dev.12.txt"):
    copie_drive(livs12[0], vagues["id"], "LISEZMOI-loupe-dev.12.txt")
recoupe(vagues["id"], "kit-loupe-dev.12.zip", MD5_ZIP_V12)
recoupe(vagues["id"], "LISEZMOI-loupe-dev.12.txt", MD5_LIV_V12)
print("    vagues-m10 COMPLÈTE dev.1 → dev.12")

# ═════════ D. LA RACINE DEMEURE À LA VAGUE DU SCELLEMENT ═════════════════
print("D. LA RACINE DEMEURE À LA VAGUE dev.12 — LA VAGUE DU SCELLEMENT")
recoupe(TEST, "kit-loupe.zip", MD5_ZIP12)
recoupe(TEST, "LISEZMOI-loupe.txt", MD5_LIV12)
kit12d = trouve(TEST, "loupe-kit-12")
assert kit12d
for piece, attendu in (("LISEZMOI-KIT-LOUPE.md", MD5_LIV12),
                       ("loupe.exe", MD5_EXE_V8),
                       ("scenario-loupe.py", MD5_SC_V12),
                       ("temoin-vitrine.bat", MD5_BAT_V12)):
    recoupe(kit12d["id"], piece, attendu)
assert sans_doublon(kit12d["id"]) == 4
print("    kit-loupe.zip + LISEZMOI-loupe.txt + loupe-kit-12/ recoupés — "
      "plus AUCUNE vague neuve : le jalon n'attend plus un run")

# ═════════ E. LE RÉCEPTACLE RÉ-ARMÉ — L'ÈRE DU JALON DÉBLOQUÉ ════════════
print("E. LE RÉCEPTACLE RÉ-ARMÉ (preuves-loupe/ — l'ère du jalon débloquent)")
receptacle = trouve(TEST, "preuves-loupe")
assert receptacle
remplace_fichier(f"{DEV12}/LISEZMOI-preuves-JALON.txt",
                 receptacle["id"], "LISEZMOI-preuves.txt")
recoupe(receptacle["id"], "LISEZMOI-preuves.txt", MD5_RECEPTACLE)
assert sans_doublon(receptacle["id"]) == 1
print("    LISEZMOI-preuves.txt — le jalon débloquent, unique")

# ═════════ F. LES DEUX INDEX MIS À JOUR ══════════════════════════════════
print("F. LES DEUX INDEX MIS À JOUR")
idx_liv_path = f"{DEV12}/idx-livraisons-217.txt"
idx_pre_path = f"{DEV12}/idx-preuves-217.txt"
telecharge(trouve(archives_liv["id"], "LISEZMOI-archives-livraisons.txt")["id"],
           idx_liv_path)
telecharge(trouve(archives_preuves["id"], "LISEZMOI-archives-preuves.txt")["id"],
           idx_pre_path)

with open(idx_liv_path, "a", encoding="utf-8") as f:
    f.write(f"""
--- la vague loupe dev.12 VERSIONNÉE après son run (l'Entrée 217 : le
    onzième run la courut — LE RUN DU SCELLEMENT : T0 → T7 TOUT VERT
    POUR LA QUATRIÈME FOIS, LA CASCADE 205 VÉCUE ENTIÈRE POUR LA
    PREMIÈRE FOIS [P0..P4, les axes P1/P4 REFUSÉS par le chargeur —
    la dette du run 10 éteinte], LA VITRINE VIVANTE LA SECONDE FOIS
    [0 et 0, aucun WER], ET le huitième défaut nommé sur pièces :
    [SONDE-EXE] — le faux négatif STRUCTUREL de la sonde de liaison
    [loupe.exe est un EXE : le bit IMAGE_FILE_DLL absent du COFF, et
    le chargeur de bibliothèque ne résout JAMAIS les imports d'un
    module exécutable — Microsoft Learn, LoadLibraryExA] ; LA LIAISON
    EST PROUVÉE PAR LE VIVANT — la vitrine vécue DEUX FOIS, la même
    pièce 054de960…) : kit-loupe-dev.12.zip md5 {MD5_ZIP_V12}… +
    LISEZMOI-loupe-dev.12.txt md5 {MD5_LIV_V12}… → vagues-m10/ EN
    PIÈCES VERSIONNÉES — l'archive COMPLÈTE dev.1 → dev.12.

--- la vague courante (racine de /test) : loupe dev.12 DEMEURE — LA
    VAGUE DU SCELLEMENT (kit-loupe.zip md5 {MD5_ZIP_V12}… +
    LISEZMOI-loupe.txt md5 {MD5_LIV_V12}… + loupe-kit-12/ aux QUATRE
    pièces : loupe.exe 0.1.0-dev.8 INTACTE, 127 488 o, md5
    {MD5_EXE_V8[:8]}…, sha256 054de960…) : **LA BALISE `loupe 0.1.0`
    EST DÉBLOQUÉE SUR LE ONZIÈME RUN RECOUPÉ (39/39 VERT)** — plus
    AUCUNE vague neuve : le jalon n'attend plus un run, il attend son
    fait de carte (D104 : le scellage est un fait de carte, la dette
    de la carte [l'Entrée 211 : génération 16 à régénérer au labo]
    en est le préalable — LE JALON M10 au geste suivant du labo).
""")

with open(idx_pre_path, "a", encoding="utf-8") as f:
    f.write(f"""
--- le ONZIÈME RUN archivé : preuves-run-loupe-dev12/ (l'Entrée 217,
    recoupé 39/39 sur pièces croisées) — **LE RUN DU SCELLEMENT** :
    T0 → T7 TOUT VERT POUR LA QUATRIÈME FOIS, LA CASCADE 205 VÉCUE
    ENTIÈRE POUR LA PREMIÈRE FOIS [P0 la pièce identique VERTE · P1
    LE TROU REFUSÉ · P2 LE BSS VERTE · P3 LE CUI VERTE · P4 LA
    GÉOMÉTRIE REFUSÉE — GetLastError 193, NTSTATUS 0xc000007b : la
    dette du run 10 éteinte, la retouche [FREE-SANS-TYPE] portée],
    LA VITRINE VIVANTE LA SECONDE FOIS [0 et 0, aucun WER, le [4/4]
    ne portant que les vieux watchdog], ET LE HUITIÈME DÉFAUT NOMMÉ
    SUR PIÈCES : [SONDE-EXE] — le faux négatif STRUCTUREL de la
    sonde de liaison : loupe.exe est un EXE [le bit IMAGE_FILE_DLL
    absent, Characteristics 0x0002], le chargeur de bibliothèque ne
    résout JAMAIS les imports d'un module exécutable [« If the
    specified module is an executable module, static imports are not
    loaded; instead, the module is loaded as if
    DONT_RESOLVE_DLL_REFERENCES was specified » — Microsoft Learn,
    LoadLibraryExA] ; LA LIAISON PROUVÉE PAR LE VIVANT [la vitrine
    vécue DEUX FOIS, la même pièce — la sixième mort prouva que la
    fenêtre ne vit pas d'un import non résolu] — **LE VERT TIENT
    ENTIER : LA BALISE `loupe 0.1.0` DÉBLOQUÉE** ; le dossier du run
    (kit-loupe/) recoupé pièce à pièce puis corbeillé (D99) —
    VERDICT-run-loupe-dev12.txt md5 {MD5_VERDICT[:8]}… + temoin-loupe.txt
    md5 {MD5_TEMOIN_LOUPE[:8]}… + temoin-vitrine.txt md5
    {MD5_TEMOIN_VITRINE[:8]}… ; LA PIÈCE ACQUITTÉE (temoin-fichier.bin
    == loupe.exe, T7 la relut inchangée) ; le geste suivant est AU
    LABO : le scellage, fait de carte (D104) — LE JALON M10.
""")

remplace_fichier(idx_liv_path, archives_liv["id"],
                 "LISEZMOI-archives-livraisons.txt")
remplace_fichier(idx_pre_path, archives_preuves["id"],
                 "LISEZMOI-archives-preuves.txt")
print("    les deux index reversés")

# ═════════ L'ÉTAT FINAL RECONTRÉ ═════════════════════════════════════════
print("\nL'ÉTAT FINAL RECONTRÉ :")
n_racine = sans_doublon(TEST)
racine = {f["name"]: f for f in liste_tout(TEST)}
assert racine["kit-loupe.zip"]["md5Checksum"].startswith(MD5_ZIP12[:8])
assert racine["LISEZMOI-loupe.txt"]["md5Checksum"].startswith(MD5_LIV12[:8])
for n in ("loupe-kit-12", "preuves-loupe", "archives-livraisons",
          "archives-preuves", "loupe-kit-11", "loupe-kit-10"):
    assert n in racine, f"{n} absent de la racine"
assert "kit-loupe" not in racine, "le dossier du run demeure"
print(f"  ✓ la racine : {n_racine} entrées, AUCUN doublon — kit-loupe.zip =="
      " dev.12, la vague du scellement")
print("  ✓ loupe-kit-12/ recoupé aux QUATRE pièces ; kit-loupe/ corbeillé")
print("  ✓ preuves-run-loupe-dev12/ : VERDICT + les DEUX témoins, unique")
print("\nLE DÉPÔT EST COMPLET — le jalon est DÉBLOQUÉ sur le run recoupé ;")
print("le geste suivant est AU LABO : LE SCELLEMENT, fait de carte (D104)")
print("— la balise `loupe 0.1.0` SCELLÉE : LE JALON M10.")
