#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE DÉPÔT DE LA SESSION 222 — le douzième run recoupé, LA BALISE 0.1.1 SCELLÉE.

LE DOUZIÈME RUN (kit 0.1.1-dev.1) : T0 → T7 TOUT VERT POUR LA CINQUIÈME
FOIS, LA CASCADE 205 VÉCUE ENTIÈRE POUR LA DEUXIÈME FOIS, LA VITRINE
VIVANTE LA TROISIÈME FOIS (0 et 0 — LA PREMIÈRE DE LA PIÈCE 0.1.1) ;
LA DOCTRINE [SONDE-EXE] TENUE (D178) ; LE RÉSIDU DU PORT NOMMÉ
[T0-PÉRIMÉ] (le bandeau « génération 16 » du scénario porté — texte
d'ère dev.12, AUCUNE porte touchée). LE RECOUP 39/39 VERT : LE VERT
TIENT ENTIER. PUIS LE LABO : la cristallisation 26 blocs à 10/10 (les
huit passes — D178 règle 2), les portes --sceller-final adaptées au
verdict (le miroir D165/D170), LA BASCULE version=0.1.1-dev.1 → 0.1.1,
l'anti-rollback ARMÉ constaté au geste même — **LA BALISE `loupe 0.1.1`
SCELLÉE SUR LE DOUZIÈME RUN VERT RECOUPÉ : LA VERSION DE LA DETTE
[R10-PÉRIMÉE] SOLDÉE** (loupe.exe INTACT c1115105…, 127 488 o).

Sur le coffre Drive (/test, racine 1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0) :
  A. ARCHIVER LE RUN 12 → archives-preuves/preuves-run-loupe-011-dev1/
     [VERDICT-run-loupe-011-dev1.txt + les DEUX témoins — les octets
     rapatriés et recoupés du dossier du run kit-loupe/]
  B. NETTOYER LE DOSSIER DU RUN : kit-loupe/ → corbeille (les témoins
     archivés ; les QUATRE pièces == loupe-kit-13/ 0.1.1-dev.1, octet
     pour octet, recoupées par md5 AVANT le geste — D99/D143)
  C. LA RACINE DEMEURE À LA VAGUE 0.1.1-dev.1 — LA VAGUE DU SCELLEMENT
     (kit-loupe.zip + LISEZMOI-loupe.txt + loupe-kit-13/ — recoupés,
     sans doublon) ; la vague versionnée dès sa naissance (l'Entrée
     221) re-recoupée : vagues-m10/ COMPLÈTE dev.1 → dev.12 +
     0.1.1-dev.1.
  D. RÉ-ARMER LE RÉCEPTACLE /preuves-loupe/ [LISEZMOI-preuves.txt —
     l'ère de la BALISE SCELLÉE : plus aucune pièce attendue, les
     captures demeurent bienvenues]
  E. METTRE À JOUR LES DEUX INDEX d'archives (livraisons + preuves).
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
KIT = "/home/z/my-project/build-011-dev1"       # la zone de la vague 0.1.1-dev.1
RUN12 = "/home/z/my-project/upload/run-011-dev1"  # les octets recoupés du run 12
DEPOT = "/home/z/my-project/triade/download/preuves-run-loupe-011-dev1"
FOLDER_MIME = "application/vnd.google-apps.folder"
TOK = obtenir_token()


def md5(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


MD5_ZIP = md5(f"{KIT}/kit-loupe.zip")                      # dadfb48c…
MD5_LIV = md5(f"{KIT}/LISEZMOI-KIT-LOUPE.md")              # 70340163…
MD5_VERDICT = md5(f"{DEPOT}/VERDICT-run-loupe-011-dev1.txt")
MD5_TEMOIN_LOUPE = md5(f"{RUN12}/temoin-loupe.txt")        # 46db2210…
MD5_TEMOIN_VITRINE = md5(f"{RUN12}/temoin-vitrine.txt")    # d83ae8cb…
MD5_EXE = md5(f"{KIT}/loupe.exe")                          # 5fc07b78…
MD5_SC = md5(f"{KIT}/scenario-loupe.py")                   # 77872b71…
MD5_BAT = md5(f"{KIT}/temoin-vitrine.bat")                 # 2a3f22f4…

RECEPTACLE = """TRIADE — preuves-loupe : LE RÉCEPTACLE DE L'ÈRE SCELLÉE (la balise 0.1.1)
========================================================================
(LA BALISE `loupe 0.1.1` EST SCELLÉE SUR LE DOUZIÈME RUN VERT RECOUPÉ
— l'Entrée 222 : LE VERT TIENT ENTIER, 39/39 ; la cristallisation 26
blocs à 10/10 ; LA VERSION DE LA DETTE [R10-PÉRIMÉE] SOLDÉE — D179/D181.
loupe.exe 0.1.1 INTACTE : sha256 c111510535767a40…, 127 488 o, la
même pièce que LE DOUZIÈME RUN a courue et vécue ; la carte génération
17 porte la balise [version=0.1.1], l'anti-rollback ARMÉ — la 0.1.0
scellée [054de960…] demeure, la monotonie R10 n'ouvre jamais
l'ancienne ; le jalon M10 demeure FRANCHI depuis la 0.1.0 [onze runs,
onze leçons] — la 0.1.1 est LA VERSION DE LA DETTE SOLDÉE.)

PLUS AUCUNE PIÈCE N'EST ATTENDUE ICI : l'ère est scellée, le run du
scellage est archivé (preuves-run-loupe-011-dev1/ aux archives) :
  - temoin-loupe.txt     le témoin du scénario — ARCHIVÉ ;
  - temoin-vitrine.txt   le témoin vitrine — ARCHIVÉ ;
  - capture-*.png        les captures de la vitrine, toujours les
                         bienvenues ;
  - si un DÉFAUT est jamais nommé sur la 0.1.1 scellée : JAMAIS un
                         hot-fix (R4/R10) — la version 0.1.2+ sera
                         commandée par le développeur, née de la
                         recomposition, la dette payée à la naissance
                         (le miroir D179).
"""


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


# ═════════ A. LE RUN 12 ARCHIVÉ → preuves-run-loupe-011-dev1/ ════════════
print("A. LE RUN 12 ARCHIVÉ → archives-preuves/preuves-run-loupe-011-dev1/")
archives_preuves = trouve(TEST, "archives-preuves")
assert archives_preuves and archives_preuves["mimeType"] == FOLDER_MIME
run12 = trouve(archives_preuves["id"], "preuves-run-loupe-011-dev1")
if not run12:
    id_run12 = upload_conteneur("preuves-run-loupe-011-dev1",
                                archives_preuves["id"])
    print("    dossier preuves-run-loupe-011-dev1/ créé")
else:
    id_run12 = run12["id"]
for piece, attendu in (("temoin-loupe.txt", MD5_TEMOIN_LOUPE),
                       ("temoin-vitrine.txt", MD5_TEMOIN_VITRINE)):
    if not trouve(id_run12, piece):
        upload(f"{RUN12}/{piece}", id_run12, piece)
    recoupe(id_run12, piece, attendu)
if not trouve(id_run12, "VERDICT-run-loupe-011-dev1.txt"):
    upload(f"{DEPOT}/VERDICT-run-loupe-011-dev1.txt", id_run12,
           "VERDICT-run-loupe-011-dev1.txt")
recoupe(id_run12, "VERDICT-run-loupe-011-dev1.txt", MD5_VERDICT)
assert sans_doublon(id_run12) == 3
print("    le run 12 archivé : VERDICT + les DEUX témoins, sans doublon")

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
# les QUATRE pièces du kit du run == la vague 0.1.1-dev.1 (loupe-kit-13/
# et le dépôt), octet pour octet (recoup AVANT le geste) ; temoin-fichier.bin
# == loupe.exe (la copie que la seconde fenêtre ouvrit)
for piece, attendu in (("loupe.exe", MD5_EXE),
                       ("scenario-loupe.py", MD5_SC),
                       ("temoin-vitrine.bat", MD5_BAT),
                       ("temoin-fichier.bin", MD5_EXE)):
    assert pieces_run[piece].get("md5Checksum", "").startswith(attendu[:8]), \
        f"la pièce {piece} du run diverge de la vague 0.1.1-dev.1"
kit13 = {f["name"]: f for f in liste_tout(trouve(TEST, "loupe-kit-13")["id"])}
assert kit13["loupe.exe"]["md5Checksum"].startswith(MD5_EXE[:8])
assert kit13["scenario-loupe.py"]["md5Checksum"].startswith(MD5_SC[:8])
print("    les QUATRE pièces + temoin-fichier.bin == la vague 0.1.1-dev.1, "
      "les DEUX témoins archivés — le dossier peut mourir")
corbeille(kit_run["id"])
assert not trouve(TEST, "kit-loupe"), "kit-loupe/ demeure !"
print("    kit-loupe/ → corbeille (les preuves vivent aux archives)")

# ═════════ C. LA RACINE DEMEURE À LA VAGUE DU SCELLEMENT ═════════════════
print("C. LA RACINE DEMEURE À LA VAGUE 0.1.1-dev.1 — LA VAGUE DU SCELLEMENT")
recoupe(TEST, "kit-loupe.zip", MD5_ZIP)
recoupe(TEST, "LISEZMOI-loupe.txt", MD5_LIV)
kit13d = trouve(TEST, "loupe-kit-13")
assert kit13d
for piece, attendu in (("LISEZMOI-KIT-LOUPE.md", MD5_LIV),
                       ("loupe.exe", MD5_EXE),
                       ("scenario-loupe.py", MD5_SC),
                       ("temoin-vitrine.bat", MD5_BAT)):
    recoupe(kit13d["id"], piece, attendu)
assert sans_doublon(kit13d["id"]) == 4
# la vague versionnée dès sa naissance (l'Entrée 221) re-recoupée :
# vagues-m10/ COMPLÈTE dev.1 → dev.12 + 0.1.1-dev.1
archives_liv = trouve(TEST, "archives-livraisons")
assert archives_liv
vagues = trouve(archives_liv["id"], "vagues-m10")
assert vagues
recoupe(vagues["id"], "kit-loupe-0.1.1-dev.1.zip", MD5_ZIP)
recoupe(vagues["id"], "LISEZMOI-loupe-0.1.1-dev.1.txt", MD5_LIV)
print("    kit-loupe.zip + LISEZMOI-loupe.txt + loupe-kit-13/ recoupés ; "
      "vagues-m10/ COMPLÈTE dev.1 → dev.12 + 0.1.1-dev.1")

# ═════════ D. LE RÉCEPTACLE RÉ-ARMÉ — L'ÈRE SCELLÉE ══════════════════════
print("D. LE RÉCEPTACLE RÉ-ARMÉ (preuves-loupe/ — l'ère de la balise scellée)")
receptacle = trouve(TEST, "preuves-loupe")
assert receptacle
chemin_recep = f"{KIT}/LISEZMOI-preuves-SCELLEE.txt"
with open(chemin_recep, "w", encoding="utf-8", newline="\n") as f:
    f.write(RECEPTACLE)
MD5_RECEPTACLE = md5(chemin_recep)
remplace_fichier(chemin_recep, receptacle["id"], "LISEZMOI-preuves.txt")
recoupe(receptacle["id"], "LISEZMOI-preuves.txt", MD5_RECEPTACLE)
assert sans_doublon(receptacle["id"]) == 1
print("    LISEZMOI-preuves.txt — l'ère scellée, unique")

# ═════════ E. LES DEUX INDEX MIS À JOUR ══════════════════════════════════
print("E. LES DEUX INDEX MIS À JOUR")
idx_liv_path = f"{KIT}/idx-livraisons-222.txt"
idx_pre_path = f"{KIT}/idx-preuves-222.txt"
telecharge(trouve(archives_liv["id"], "LISEZMOI-archives-livraisons.txt")["id"],
           idx_liv_path)
telecharge(trouve(archives_preuves["id"], "LISEZMOI-archives-preuves.txt")["id"],
           idx_pre_path)

with open(idx_liv_path, "a", encoding="utf-8") as f:
    f.write(f"""
--- la vague loupe 0.1.1-dev.1 COURUE ET SCELLÉE (l'Entrée 222 : le
    douzième run la courut — LE RUN DU SCELLEMENT DE LA DETTE : T0 → T7
    TOUT VERT POUR LA CINQUIÈME FOIS, LA CASCADE 205 VÉCUE ENTIÈRE
    POUR LA DEUXIÈME FOIS, LA VITRINE VIVANTE LA TROISIÈME FOIS [0 et
    0 — LA PREMIÈRE DE LA PIÈCE 0.1.1, aucun WER], le recoup 39/39
    VERT — LE VERT TIENT ENTIER ; puis le labo : la cristallisation
    26 blocs à 10/10, les portes --sceller-final adaptées au verdict
    [le miroir D165/D170], LA BASCULE version=0.1.1-dev.1 → 0.1.1,
    l'anti-rollback ARMÉ) : **LA BALISE `loupe 0.1.1` SCELLÉE SUR LE
    DOUZIÈME RUN VERT RECOUPÉ — LA VERSION DE LA DETTE [R10-PÉRIMÉE]
    SOLDÉE** ; loupe.exe INTACTE c1115105…, 127 488 o ; la racine
    demeure à la vague du scellement (kit-loupe.zip md5 {MD5_ZIP[:8]}…
    + LISEZMOI-loupe.txt md5 {MD5_LIV[:8]}… + loupe-kit-13/ aux
    QUATRE pièces) ; vagues-m10/ demeure COMPLÈTE dev.1 → dev.12 +
    0.1.1-dev.1 — plus AUCUNE vague neuve : l'ère est scellée.
""")

with open(idx_pre_path, "a", encoding="utf-8") as f:
    f.write(f"""
--- le DOUZIÈME RUN archivé : preuves-run-loupe-011-dev1/ (l'Entrée
    222, recoupé 39/39 sur pièces croisées) — **LE RUN DU SCELLEMENT
    DE LA DETTE** : T0 → T7 TOUT VERT POUR LA CINQUIÈME FOIS, LA
    CASCADE 205 VÉCUE ENTIÈRE POUR LA DEUXIÈME FOIS [P0 la pièce
    identique VERTE · P1 LE TROU REFUSÉ · P2 LE BSS VERTE · P3 LE CUI
    VERTE · P4 LA GÉOMÉTRIE REFUSÉE — GetLastError 193, NTSTATUS
    0xc000007b], LA VITRINE VIVANTE LA TROISIÈME FOIS [0 et 0, aucun
    WER, le [4/4] ne portant que les vieux watchdog — LA PREMIÈRE DE
    LA PIÈCE 0.1.1 : le qword 0x00010101 lu sur la pièce, la dette
    soldée à la naissance], LA DOCTRINE [SONDE-EXE] TENUE (D178 : le
    faux négatif structurel — la liaison PROUVÉE PAR LE VIVANT) ET LE
    RÉSIDU DU PORT NOMMÉ [T0-PÉRIMÉ] (le bandeau « génération 16 » du
    scénario porté — texte d'ère dev.12, AUCUNE porte touchée) — **LE
    VERT TIENT ENTIER : LA BALISE `loupe 0.1.1` SCELLÉE PAR FAIT DE
    CARTE (la cristallisation 10/10, la bascule dans frag-bld,
    l'entête génération 17, la signature Ed25519 re-signée, l'anti-
    rollback ARMÉ — LA VERSION DE LA DETTE [R10-PÉRIMÉE] SOLDÉE)** ;
    le dossier du run (kit-loupe/) recoupé pièce à pièce puis
    corbeillé (D99) — VERDICT-run-loupe-011-dev1.txt md5
    {MD5_VERDICT[:8]}… + temoin-loupe.txt md5 {MD5_TEMOIN_LOUPE[:8]}…
    + temoin-vitrine.txt md5 {MD5_TEMOIN_VITRINE[:8]}… ; LA PIÈCE
    ACQUITTÉE (temoin-fichier.bin == loupe.exe, T7 la relut
    inchangée) ; la suite appartient au développeur : l'ère 0.1.1
    scellée, M10 demeure franchi depuis la 0.1.0.
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
assert racine["kit-loupe.zip"]["md5Checksum"].startswith(MD5_ZIP[:8])
assert racine["LISEZMOI-loupe.txt"]["md5Checksum"].startswith(MD5_LIV[:8])
for n in ("loupe-kit-13", "preuves-loupe", "archives-livraisons",
          "archives-preuves", "loupe-kit-12", "loupe-kit-11"):
    assert n in racine, f"{n} absent de la racine"
assert "kit-loupe" not in racine, "le dossier du run demeure"
print(f"  ✓ la racine : {n_racine} entrées, AUCUN doublon — kit-loupe.zip =="
      " 0.1.1-dev.1, la vague du scellement")
print("  ✓ loupe-kit-13/ recoupé aux QUATRE pièces ; kit-loupe/ corbeillé")
print("  ✓ preuves-run-loupe-011-dev1/ : VERDICT + les DEUX témoins, unique")
print("\nLE DÉPÔT EST COMPLET — LA BALISE `loupe 0.1.1` SCELLÉE sur le run")
print("recoupé : LA VERSION DE LA DETTE [R10-PÉRIMÉE] SOLDÉE.")
