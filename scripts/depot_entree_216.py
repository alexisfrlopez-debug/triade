#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE DÉPÔT DE LA SESSION 216 — le run 10 recoupé, la vague dev.12.

LE DIXIÈME RUN (kit dev.11) : T0 → T7 TOUT VERT POUR LA TROISIÈME FOIS,
LA VITRINE VIVANTE LA PREMIÈRE FOIS (0 et 0) — MAIS la cascade 205
mourut à son premier geste ([FREE-SANS-TYPE] : FreeLibrary SANS
argtypes, le HMODULE 64 bits ne passe pas la conversion int 32 bits —
ArgumentError, qui n'est PAS un OSError) et LA LIAISON ne courut jamais.
LA BALISE N'EST PAS SCELLÉE (le critère publié exige le scénario
ENTIER) ; LA RETOUCHE dev.12 EST NÉE (genere_kit_dev12.py).

Sur le coffre Drive (/test, racine 1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0) :
  A. ARCHIVER LE RUN 10 → archives-preuves/preuves-run-loupe-dev11/
     [VERDICT-run-loupe-dev11.txt + les DEUX témoins — les octets
     rapatriés et recoupés du dossier du run kit-loupe/]
  B. NETTOYER LE DOSSIER DU RUN : kit-loupe/ → corbeille (les témoins
     sont archivés ; les QUATRE pièces du kit == loupe-kit-11/, octet
     pour octet, recoupées par md5 AVANT le geste — D99 : un dossier
     neuf par run, l'ancien meurt archivé)
  C. VERSIONNER LA VAGUE dev.11 → archives-livraisons/vagues-m10/
     [kit-loupe-dev.11.zip + LISEZMOI-loupe-dev.11.txt — copies Drive
     des fichiers de la racine, md5 recoupés APRÈS — l'archive devient
     COMPLÈTE dev.1 → dev.11]
  D. DÉPOSER LA VAGUE dev.12 à la racine : kit-loupe.zip (remplacé) +
     LISEZMOI-loupe.txt (remplacé) + loupe-kit-12/ (dossier neuf, les
     QUATRE pièces)
  E. PURGER LES DOUBLONS DE LA RACINE — [CORBEILLE-VIDE] NOMMÉ : la
     corbeille de l'Entrée 215 envoyait PATCH au CORPS VIDE ({}) —
     RIEN ne fut jamais corbeillé, les remplacés DEMEURÈRENT : DEUX
     kit-loupe.zip (dev.10 + dev.11) et DEUX LISEZMOI-loupe.txt à la
     racine, DEUX LISEZMOI-preuves.txt au réceptacle. LA RETOUCHE : le
     corps porte {"trashed": true} — et le dépôt VÉRIFIE L'ÉTAT FINAL
     (EXACTEMENT UN de chaque nom, tous dev.12).
  F. RÉ-ARMER LE RÉCEPTACLE /preuves-loupe/ [LISEZMOI-preuves.txt —
     l'histoire dev.12 : la vitrine DÉJÀ VÉCUE, la dette = le scénario
     ENTIER]
  G. METTRE À JOUR LES DEUX INDEX d'archives (livraisons + preuves).
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
RUN11 = "/home/z/my-project/upload/run-dev11"   # les octets recoupés du run 10
FOLDER_MIME = "application/vnd.google-apps.folder"
TOK = obtenir_token()


def md5(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


MD5_ZIP12 = md5(f"{DEV12}/kit-loupe.zip")
MD5_LIV12 = md5(f"{DEV12}/LISEZMOI-KIT-LOUPE.md")
MD5_SC12 = md5(f"{DEV12}/scenario-loupe.py")
MD5_BAT12 = md5(f"{DEV12}/temoin-vitrine.bat")
MD5_EXE12 = md5(f"{DEV12}/loupe.exe")
MD5_TEMOIN_LOUPE = md5(f"{RUN11}/temoin-loupe.txt")
MD5_TEMOIN_VITRINE = md5(f"{RUN11}/temoin-vitrine.txt")
SHA_EXE = hashlib.sha256(open(f"{DEV12}/loupe.exe", "rb").read()).hexdigest()

MD5_ZIP_V10 = "4b5e3931"   # la vague dev.10 (doublon de la racine)
MD5_ZIP_V11 = "a92ddcc8"   # la vague dev.11 (doublon de la racine)
MD5_LIV_V10 = "8908377d"
MD5_LIV_V11 = "e9b8c6ab"
MD5_SC_V11 = "f2766d6c964cf147a893574f5537c190"
MD5_BAT_V11 = "2236af792a9bc85387aba8c016f0cc27"
MD5_EXE_V8 = "074881be634119c2c3f6babeaeef9684"


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
    """LA RETOUCHE [CORBEILLE-VIDE] : le corps porte trashed=true —
    l'Entrée 215 envoyait un corps VIDE, rien n'était corbeillé."""
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
    """Corbeille TOUS les homonymes (les doublons nommés), puis dépose."""
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


# ═══════════════════ 0. LE VERDICT DU RUN 10 (le texte avant le dépôt) ═
VERDICT = f"""VERDICT DU DIXIÈME RUN TERRAIN — kit dev.11 (l'Entrée 216, recoupé sur pièces)
================================================================================
L'ENVIRONNEMENT : Windows 11 (10.0.26300.9818) · Python 64 bits · AMD64.
LE KIT COURU : la vague dev.11 — les QUATRE pièces recoupées pièce à
pièce contre le dépôt : loupe.exe md5 {MD5_EXE_V8[:8]}…, scenario-loupe.py
md5 {MD5_SC_V11[:8]}…, temoin-vitrine.bat md5 {MD5_BAT_V11[:8]}…,
LISEZMOI md5 {MD5_LIV_V11[:8]}… — le dossier du run (kit-loupe/) porte
LE MÊME kit, octet pour octet, AVEC ses preuves.
LA PIÈCE : loupe.exe 0.1.0-dev.8 — 127 488 o, sha256 {SHA_EXE[:16]}… —
l'empreinte ASSERTÉE au T0, la pièce relue INCHANGÉE au T7 ;
temoin-fichier.bin (né du témoin vitrine) == loupe.exe, octet pour
octet (md5 {MD5_EXE_V8[:8]}…) — LA PIÈCE EST ACQUITTÉE DE TOUTE CHARGE.

LE TÉMOIN (temoin-loupe.txt) : T0 → T7 TOUT VERT POUR LA TROISIÈME
FOIS — [T0] l'empreinte assertée, LE CONTRÔLE D54 ÉTENDU [les QUATRE
plages FirstThunk marchées au compte exact 10 · 18 · 6 · 3 ET LES
QUATRE OFT marchés au pas DWORD du chargeur, chaque entrée == le
préremplissage de son slot], les adresses scellées, l'IAT résolue ;
[T1] la session sur L'OMBRE byte-à-byte ; [T2] la double lecture, LE
PANNEAU [la pièce jugée par sa propre application : sha256 ==
hashlib == l'asserté] ; [T3] les lignes au format composé ; [T4] la
recherche == bytes.find ; [T5] LA BOUCLE D'ÉDITION ENTIÈRE [l'octet 0
mûté 0x00 → 0x4D SEUL, la taille CONSTANTE, la marque levée, la
session close] ; [T6] LES QUATRE REJETS NOMMÉS [-2 ABSENT · -5 ENTRÉE ·
-3 HORS-BORNES · -1 FIN] ; [T7] la clôture, l'artefact relu INCHANGÉ.
PUIS [S0] LA CASCADE 205 MOURUT À SON PREMIER GESTE : « ÉCHEC NOMMÉ
[EXCEPTION] : ArgumentError('argument 1: OverflowError: int too long to
convert') » — [FREE-SANS-TYPE] : le k32.FreeLibrary(base) de la leçon
du run 9 fut appelé SANS argtypes avec le HMODULE 64 bits rendu par le
restype c_void_p du T0 — ctypes convertit l'argument nu en int 32
bits, le handle ne tient pas ; ET l'ArgumentError n'est PAS un OSError
: l'essai isolé ne tenait que pour OSError — la cascade mourut à P0,
ET LA LIAISON (la sonde de l'Entrée 214) NE COURUT JAMAIS.

LE TÉMOIN VITRINE (temoin-vitrine.txt) : **LA VITRINE A VÉCU LA
PREMIÈRE FOIS** — [1/4] la vitrine vide : code de sortie 0 ; [2/4] la
vitrine avec fichier (temoin-fichier.bin) : code de sortie 0 ; [3/4]
AUCUN rapport WER ; [4/4] le journal d'événements ne porte que de
vieux LiveKernelEvent (1001, watchdog — 30/10, 02/11, 03/11) : AUCUNE
mort de loupe.exe. APRÈS SIX MORTS, **L'APPLICATION NÉE DE TRIADE A
VÉCU CHEZ SON UTILISATEUR** — le cœur du grandeur nature (D171) est
VÉCU.

LE VERDICT : LA VITRINE VIVANTE (0 et 0) ET LE CONTRAT T0 → T7 TOUT
VERT — MAIS le scénario n'est pas ENTIER (S0 morte, LA LIAISON jamais
courue) : LE CRITÈRE PUBLIÉ (le scénario ENTIER ET la vitrine vivante)
N'EST PAS TENU — **LA BALISE `loupe 0.1.0` N'EST PAS SCELLÉE sur ce
run**. LE SEPTIÈME DÉFAUT EST NOMMÉ : [FREE-SANS-TYPE] — LE DÉFAUT DU
KIT, PAS DE LA PIÈCE (la pièce est acquittée : le défaut vit dans le
scénario Python du kit ; la vitrine vivante prouve la liaison MIEUX
que toute sonde — la fenêtre n'eût pas vécu d'un import non résolu).
LA RETOUCHE : kit dev.12 (l'Entrée 216) — FreeLibrary.argtypes =
[c_void_p] posé au T0 (le POINTEUR passe, aux DEUX sondes d'un seul
geste), l'essai de la cascade 205 élargi à TOUTE classe d'exception
(l'ArgumentError n'est pas un OSError), la sonde de liaison blindée de
même (aucune exception de sonde ne tue le run) ; la pièce n'a pas
bougé d'un octet (sha256 {SHA_EXE[:16]}…, la carte demeure génération
16).
LE GESTE SUIVANT : le run du kit dev.12 — dossier loupe-kit-12/ au
coffre, python scenario-loupe.py (T0 → S0 → LA LIAISON), la vitrine
par son témoin (les deux codes, le [4/4]) ; si le vert TIENT ENTIER :
**LA BALISE `loupe 0.1.0` SCELLÉE — LE JALON M10**.
"""
open(f"{DEV12}/VERDICT-run-loupe-dev11.txt", "w", encoding="utf-8",
     newline="\n").write(VERDICT)
MD5_VERDICT = md5(f"{DEV12}/VERDICT-run-loupe-dev11.txt")
print(f"[0] le verdict du run 10 : {len(VERDICT)} octets, md5 {MD5_VERDICT[:8]}…")

# ═══════════════════ A. LE RUN 10 ARCHIVÉ ═════════════════════════════
print("A. LE RUN 10 ARCHIVÉ → archives-preuves/preuves-run-loupe-dev11/")
archives_preuves = trouve(TEST, "archives-preuves")
assert archives_preuves and archives_preuves["mimeType"] == FOLDER_MIME
run11 = trouve(archives_preuves["id"], "preuves-run-loupe-dev11")
if not run11:
    id_run11 = upload_conteneur("preuves-run-loupe-dev11", archives_preuves["id"])
    print("    dossier preuves-run-loupe-dev11/ créé")
else:
    id_run11 = run11["id"]
for piece, attendu in (("temoin-loupe.txt", MD5_TEMOIN_LOUPE),
                       ("temoin-vitrine.txt", MD5_TEMOIN_VITRINE)):
    if not trouve(id_run11, piece):
        upload(f"{RUN11}/{piece}", id_run11, piece)
    recoupe(id_run11, piece, attendu)
if not trouve(id_run11, "VERDICT-run-loupe-dev11.txt"):
    upload(f"{DEV12}/VERDICT-run-loupe-dev11.txt", id_run11,
           "VERDICT-run-loupe-dev11.txt")
recoupe(id_run11, "VERDICT-run-loupe-dev11.txt", MD5_VERDICT)
assert sans_doublon(id_run11) == 3
print("    le run 10 archivé : VERDICT + les DEUX témoins, sans doublon")

# ═══════════════════ B. LE DOSSIER DU RUN NETTOYÉ (D99) ═══════════════
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
# les QUATRE pièces du kit du run == la vague dev.11 du dépôt, octet pour
# octet (recoup AVANT le geste) ; temoin-fichier.bin == loupe.exe
for piece, attendu in (("loupe.exe", MD5_EXE_V8), ("scenario-loupe.py", MD5_SC_V11),
                       ("temoin-vitrine.bat", MD5_BAT_V11),
                       ("temoin-fichier.bin", MD5_EXE_V8)):
    assert pieces_run[piece].get("md5Checksum", "").startswith(attendu[:8]), \
        f"la pièce {piece} du run diverge de la vague dev.11"
print("    les QUATRE pièces + temoin-fichier.bin == la vague dev.11, "
      "les DEUX témoins archivés — le dossier peut mourir")
corbeille(kit_run["id"])
assert not trouve(TEST, "kit-loupe"), "kit-loupe/ demeure !"
print("    kit-loupe/ → corbeille (les preuves vivent aux archives)")

# ═══════════════════ C. LA VAGUE dev.11 VERSIONNÉE ════════════════════
print("C. LA VAGUE dev.11 VERSIONNÉE → vagues-m10/ (courue au run 10)")
archives_liv = trouve(TEST, "archives-livraisons")
assert archives_liv
vagues = trouve(archives_liv["id"], "vagues-m10")
assert vagues
zips11 = [f for f in trouve_tous(TEST, "kit-loupe.zip")
          if (f.get("md5Checksum") or "").startswith(MD5_ZIP_V11)]
livs11 = [f for f in trouve_tous(TEST, "LISEZMOI-loupe.txt")
          if (f.get("md5Checksum") or "").startswith(MD5_LIV_V11)]
assert len(zips11) == 1 and len(livs11) == 1, \
    f"la vague dev.11 à la racine : {len(zips11)} zip, {len(livs11)} LISEZMOI"
if not trouve(vagues["id"], "kit-loupe-dev.11.zip"):
    copie_drive(zips11[0], vagues["id"], "kit-loupe-dev.11.zip")
if not trouve(vagues["id"], "LISEZMOI-loupe-dev.11.txt"):
    copie_drive(livs11[0], vagues["id"], "LISEZMOI-loupe-dev.11.txt")
recoupe(vagues["id"], "kit-loupe-dev.11.zip", MD5_ZIP_V11)
recoupe(vagues["id"], "LISEZMOI-loupe-dev.11.txt", MD5_LIV_V11)
print("    vagues-m10 COMPLÈTE dev.1 → dev.11")

# ═══════════════════ D. LA VAGUE dev.12 DÉPOSÉE ═══════════════════════
print("D. LA VAGUE dev.12 DÉPOSÉE à la racine du /test")
remplace_fichier(f"{DEV12}/kit-loupe.zip", TEST, "kit-loupe.zip")
recoupe(TEST, "kit-loupe.zip", MD5_ZIP12)

kit12 = trouve(TEST, "loupe-kit-12")
if not kit12:
    upload_conteneur("loupe-kit-12", TEST)
    print("    dossier loupe-kit-12/ créé")
kit12 = trouve(TEST, "loupe-kit-12")
for piece, attendu in (("LISEZMOI-KIT-LOUPE.md", MD5_LIV12),
                       ("loupe.exe", MD5_EXE12),
                       ("scenario-loupe.py", MD5_SC12),
                       ("temoin-vitrine.bat", MD5_BAT12)):
    if not trouve(kit12["id"], piece):
        upload(f"{DEV12}/{piece}", kit12["id"], piece)
    recoupe(kit12["id"], piece, attendu)
assert sans_doublon(kit12["id"]) == 4
print("    loupe-kit-12/ aux QUATRE pièces, sans doublon")

remplace_fichier(f"{DEV12}/LISEZMOI-KIT-LOUPE.md", TEST, "LISEZMOI-loupe.txt")
recoupe(TEST, "LISEZMOI-loupe.txt", MD5_LIV12)

# ═══════════════════ E. LES DOUBLONS DE LA RACINE PURGÉS ══════════════
print("E. LES DOUBLONS DE LA RACINE PURGÉS ([CORBEILLE-VIDE] réparé)")
restants_zip = [f for f in liste_tout(TEST)
                if f["name"] == "kit-loupe.zip"
                and not (f.get("md5Checksum") or "").startswith(MD5_ZIP12[:8])]
restants_liv = [f for f in liste_tout(TEST)
                if f["name"] == "LISEZMOI-loupe.txt"
                and not (f.get("md5Checksum") or "").startswith(MD5_LIV12[:8])]
for f in restants_zip + restants_liv:
    corbeille(f["id"])
    print(f"    doublon {f['name']} (md5 {f.get('md5Checksum','-')[:8]}…) → corbeille")
n_racine = sans_doublon(TEST)
print(f"    la racine du /test : {n_racine} entrées, AUCUN doublon de nom")

# ═══════════════════ F. LE RÉCEPTACLE RÉ-ARMÉ ═════════════════════════
print("F. LE RÉCEPTACLE RÉ-ARMÉ (preuves-loupe/)")
receptacle = trouve(TEST, "preuves-loupe")
assert receptacle
remplace_fichier(f"{DEV12}/LISEZMOI-preuves-NEUF.txt",
                 receptacle["id"], "LISEZMOI-preuves.txt")
recoupe(receptacle["id"], "LISEZMOI-preuves.txt",
        md5(f"{DEV12}/LISEZMOI-preuves-NEUF.txt"))
assert sans_doublon(receptacle["id"]) == 1
print("    LISEZMOI-preuves.txt — l'histoire dev.12, unique")

# ═══════════════════ G. LES DEUX INDEX MIS À JOUR ═════════════════════
print("G. LES DEUX INDEX MIS À JOUR")
idx_liv_path = f"{DEV12}/idx-livraisons.txt"
idx_pre_path = f"{DEV12}/idx-preuves.txt"
telecharge(trouve(archives_liv["id"], "LISEZMOI-archives-livraisons.txt")["id"],
           idx_liv_path)
telecharge(trouve(archives_preuves["id"], "LISEZMOI-archives-preuves.txt")["id"],
           idx_pre_path)

with open(idx_liv_path, "a", encoding="utf-8") as f:
    f.write(f"""
--- la vague loupe dev.11 VERSIONNÉE après son run (l'Entrée 216 : le
    dixième run la courut — T0 → T7 TOUT VERT POUR LA TROISIÈME FOIS,
    LA VITRINE VIVANTE LA PREMIÈRE FOIS [0 et 0], MAIS la cascade 205
    mourut à son premier geste : [FREE-SANS-TYPE] — FreeLibrary SANS
    argtypes, le HMODULE 64 bits du restype c_void_p ne passe pas la
    conversion int 32 bits, ArgumentError('argument 1: OverflowError:
    int too long to convert') — et l'ArgumentError n'est PAS un
    OSError : l'essai isolé ne tenait que pour OSError, LA LIAISON ne
    courut jamais) : kit-loupe-dev.11.zip md5 {MD5_ZIP_V11[:8]}… +
    LISEZMOI-loupe-dev.11.txt md5 {MD5_LIV_V11[:8]}… → vagues-m10/ EN
    PIÈCES VERSIONNÉES — l'archive COMPLÈTE dev.1 → dev.11.

--- la vague courante (racine de /test) : loupe dev.12 — LA VAGUE DE
    [FREE-SANS-TYPE], LA RETOUCHE DU KIT SEUL (kit-loupe.zip md5
    {MD5_ZIP12[:8]}… + LISEZMOI-loupe.txt md5 {MD5_LIV12[:8]}… +
    loupe-kit-12/ aux QUATRE pièces : loupe.exe 0.1.0-dev.8 INTACTE,
    127 488 o, md5 {MD5_EXE12[:8]}…, sha256 {SHA_EXE[:16]}… — la carte
    génération 16 demeure ; LA RETOUCHE : FreeLibrary.argtypes =
    [c_void_p] posé au T0 — le POINTEUR passe, aux DEUX sondes d'un
    seul geste ; l'essai de la cascade 205 élargi à TOUTE classe
    d'exception ; la sonde de liaison blindée : AUCUNE exception de
    sonde ne tue le run) — livrée le 10/11/2026, déposée par le labo
    en la forme canonique kit-loupe.zip + LISEZMOI ET en la forme
    dossier loupe-kit-12/ prête à courir ; ET LE COFFRE PURGÉ de ses
    doublons ([CORBEILLE-VIDE] nommé : la corbeille de l'Entrée 215
    envoyait PATCH au corps vide — RIEN n'était corbeillé, DEUX
    kit-loupe.zip et DEUX LISEZMOI-loupe.txt demeuraient à la racine :
    le corps porte désormais trashed=true et le dépôt VÉRIFIE
    l'unicité de chaque nom) ; la balise `loupe 0.1.0` attend le vert
    ENTIER : LE JALON M10.
""")

with open(idx_pre_path, "a", encoding="utf-8") as f:
    f.write(f"""
--- le DIXIÈME RUN archivé : preuves-run-loupe-dev11/ (l'Entrée 216,
    recoupé sur pièces) — LE RUN HISTORIQUE : T0 → T7 TOUT VERT POUR
    LA TROISIÈME FOIS ET **LA VITRINE VIVANTE LA PREMIÈRE FOIS** (0 et
    0, les deux fenêtres vécues, Alt+F4 chacune, aucun WER, le [4/4]
    ne portant que de vieux LiveKernelEvent) — L'APPLICATION NÉE DE
    TRIADE A VÉCU CHEZ SON UTILISATEUR ; MAIS la cascade 205 mourut à
    son premier geste : [FREE-SANS-TYPE] (ArgumentError, int too long
    to convert — le HMODULE 64 bits au FreeLibrary SANS argtypes, et
    l'ArgumentError n'est pas un OSError), LA LIAISON ne courut
    jamais : la balise n'est PAS scellée sur ce run ; le dossier du
    run (kit-loupe/) archivé puis corbeillé (D99) — VERDICT-run-loupe-
    dev11.txt md5 {MD5_VERDICT[:8]}… + temoin-loupe.txt md5
    {MD5_TEMOIN_LOUPE[:8]}… + temoin-vitrine.txt md5
    {MD5_TEMOIN_VITRINE[:8]}… ; LA PIÈCE ACQUITTÉE (loupe.exe relu
    inchangé, temoin-fichier.bin == la pièce) ; le onzième run est LE
    GESTE SUIVANT, sur la vague dev.12.
""")

remplace_fichier(idx_liv_path, archives_liv["id"],
                 "LISEZMOI-archives-livraisons.txt")
remplace_fichier(idx_pre_path, archives_preuves["id"],
                 "LISEZMOI-archives-preuves.txt")
print("    les deux index reversés")

# ═══════════════════ L'ÉTAT FINAL RECONTRÉ ════════════════════════════
print("\nL'ÉTAT FINAL RECONTRÉ :")
sans_doublon(TEST)
racine = {f["name"]: f for f in liste_tout(TEST)}
assert racine["kit-loupe.zip"]["md5Checksum"].startswith(MD5_ZIP12[:8])
assert racine["LISEZMOI-loupe.txt"]["md5Checksum"].startswith(MD5_LIV12[:8])
for n in ("loupe-kit-12", "preuves-loupe", "archives-livraisons",
          "archives-preuves", "loupe-kit-11", "loupe-kit-10"):
    assert n in racine, f"{n} absent de la racine"
assert "kit-loupe" not in racine, "le dossier du run demeure"
print("  ✓ kit-loupe.zip == dev.12, LISEZMOI-loupe.txt == dev.12, uniques")
print("  ✓ loupe-kit-12/ neuf, loupe-kit-10/ et loupe-kit-11/ demeurés (D99)")
print("  ✓ kit-loupe/ (le dossier du run) archivé puis corbeillé")
print("\nLE DÉPÔT EST COMPLET — le coffre porte la vague dev.12")
print("le geste du terrain : loupe-kit-12/, python scenario-loupe.py,")
print("temoin-vitrine.bat, preuves-loupe/ ENTIER au coffre")
print("— si le vert TIENT ENTIER : LA BALISE loupe 0.1.0 SCELLÉE, LE JALON M10")
