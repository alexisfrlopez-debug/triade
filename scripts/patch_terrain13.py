#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.13 — LA PIÈCE GOOGLE ENFIN CAPTURE + ANTI-CONFUSION (D65, 28/10).

LE CONSTAT DU RUN 22:32 (terrain_20261027_223216.txt, déposé dans le dossier
test) : le développeur annonce « journaux envoyés, mais je n'ai pas le json
google dans le dossier ». DEUX causes, toutes deux de notre côté :

1. LE JSON NE POUVAIT PAS EXISTER. Le gabarit curl du jeton embarque
   « --fail » (curl : « Fail silently (no output at all) on server errors ») :
   quand Google répond par une erreur HTTP (400/401…), curl sort 22 ET N'ÉCRIT
   PAS LA RÉPONSE — terrain_jeton.json n'est jamais créé. Quand curl échoue au
   niveau réseau (DNS/TCP/TLS), il ne l'écrit pas non plus. Le LISEZMOI
   terrain.12 demandait une pièce que le binaire ne pouvait pas produire :
   promesse erronée, nos excuses au développeur.

2. LE RUN 22:32 A TOURNÉ SUR TERRAIN.11, PAS TERRAIN.12. Diff formel
   22:10 vs 22:32 : UNE ligne (la date). S00 dit « terrain11 » et S04C
   affiche cf72462d… = demo10-diagnostique (l'ancienne démo), pas 73c064fb…
   (la finale de terrain.12). Le terrain.12 n'a JAMAIS tourné — le développeur
   a double-cliqué l'ancien exe. Le LISEZMOI terrain.13 impose l'étape 0 :
   supprimer les anciens superviseur-terrain*.exe.

LE CORRECTIF (data-only, 14 octets utiles) :
  a. GABARIT_JETON : « --fail » → 7 espaces (longueur totale inchangée,
     aucun décalage, marqueur \\x08 intact) — si Google répond, même par un
     refus, terrain_jeton.json existera avec le message d'erreur exact ;
  b. GABARIT_SESSION : idem (la réponse d'erreur de la session atterrira
     dans terrain_session.txt le moment venu) ;
     VERDICTS INCHANGÉS : sans --fail, une erreur HTTP sort code=0, le
     balayeur cherche quand même « "access_token":" » / « Location: » et
     rend le MÊME verdict (ÉCHEC) — seule la preuve survit sur disque ;
  c. génération terrain12 → terrain13 (L00/S00), VERSIONINFO 0.5.13.0,
     FileVersion « 0.5.13 », ProductVersion « …terrain13 » ;
  d. somme R10[23] recalculée (couvre les deux gabarits + S00).

INTOUCHÉS PAR DESIGN (leurs --fail sont verdict-critiques) :
  - CMD_CURL_HTTP / CMD_CURL_HTTPS (T2 — T2 est VERT et stable 3 runs) ;
  - GABARIT_PUT (sans --fail, un 5xx de Google donnerait un faux S35 OK) ;
  - tout le code superviseur, la démo finale 73c064fb, le proxy 0.4.0-dev.2,
    l'annexe jetons, l'en-tête kit, la chaîne md5 S04C.
"""

import hashlib
import pathlib
import re
import struct
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
SRC = REPO / "terrain/livraison/superviseur-terrain12.exe"
DST = REPO / "terrain/livraison/superviseur-terrain13.exe"
DEMO9 = REPO / "demo/demo.exe"

MD5_TERRAIN12 = "ee9d1072861444cb91ccfe52788bf185"
MD5_DEMO9 = "73c064fbaf4610a167bc6434dee400e4"
MD5_DEMO9_B = MD5_DEMO9.encode()
MD5_S05C = b"dd12b64948e64153ff1dd7a66f367ff3"

R10_TABLE_RVA = 0x2450
OFF_DEMO = 0x6410            # offset fichier de BLOB_DEMO (rva 0x8010)
TAILLE_DEMO = 0x4000         # 16 384 o
OFF_MD5_DEMO = 0x585F        # chaîne md5 S04C (rva 0x6A5F)
OFF_MD5_PROXY = None         # chaîne md5 S05C — localisée par recherche
OFF_ENETE_KIT = (0x6400, 0x6410)
OFF_PROXY = 0xA410
OFF_ANNEXE = 0xF010

# gabarits T3 tels que posés par layout.py (_SEQ_SUP_1) — recherche exacte
GAB_JETON = (b"curl.exe -s --fail --max-time 30 -o terrain_jeton.json "
             b"--data @terrain_req.txt \x08\x00")
GAB_SESSION = (b"curl.exe -s --fail --max-time 30 -o NUL -D terrain_session.txt "
               b"-X POST -H \"Content-Type: application/json\" "
               b"-H \"Authorization: Bearer \x07\" --data @terrain_meta.json "
               b"https://www.googleapis.com/upload/drive/v3/files"
               b"?uploadType=resumable\x00")
GAB_JETON_APRES = (b"curl.exe -s" + b" " * 8 +
                   b"--max-time 30 -o terrain_jeton.json "
                   b"--data @terrain_req.txt \x08\x00")
GAB_SESSION_APRES = (b"curl.exe -s" + b" " * 8 +
                     b"--max-time 30 -o NUL -D terrain_session.txt "
                     b"-X POST -H \"Content-Type: application/json\" "
                     b"-H \"Authorization: Bearer \x07\" "
                     b"--data @terrain_meta.json "
                     b"https://www.googleapis.com/upload/drive/v3/files"
                     b"?uploadType=resumable\x00")
assert len(GAB_JETON_APRES) == len(GAB_JETON) == 81
assert len(GAB_SESSION_APRES) == len(GAB_SESSION) == 232

# gabarits T2 + PUT : hors périmètre, --fail VERDICT-CRITIQUE
MOT_T2_HTTP = b"-s --fail --max-time 20 -o terrain_page_http.txt"
MOT_T2_HTTPS = b"-s --fail --max-time 20 -o terrain_page_https.txt"
MOT_PUT = b"-s --fail --max-time 120 -o NUL -X PUT"

PREFIX = b"curl.exe -s "       # 12 octets avant « --fail »


def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return 0x400 + (rva - 0x1000)
    if 0x2000 <= rva < 0x3000:
        return 0x1400 + (rva - 0x2000)
    if 0x3000 <= rva < 0x4000:
        d = rva - 0x3000
        return 0x2400 + d if d < 0xA00 else None
    if 0x4000 <= rva < 0x6E00:
        return 0x2E00 + (rva - 0x4000)
    if 0x7000 <= rva < 0x7800:
        return 0x5C00 + (rva - 0x7000)
    if 0x8000 <= rva < 0x10D10:
        return 0x6400 + (rva - 0x8000)
    if 0x11000 <= rva < 0x11200:
        return 0xF200 + (rva - 0x11000)
    return None


def somme_zone(data, rva, ln):
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s


def lire_table(data):
    table_off = rva2off(R10_TABLE_RVA)
    entrees = []
    k = 0
    while True:
        rva, ln, sm = struct.unpack_from("<IIQ", data, table_off + 16 * k)
        if rva == 0:
            return entrees, k, table_off
        entrees.append((rva, ln, sm))
        k += 1
        if k > 60:
            raise ValueError("table R10 sans terminateur")


def unique(data, motif):
    hits = [m.start() for m in re.finditer(re.escape(motif), data)]
    if len(hits) != 1:
        raise ValueError(f"{len(hits)} occurrences de {motif[:40]!r}…")
    return hits[0]


def erreur(msg):
    print(f"ECHEC : {msg}")
    sys.exit(1)


# =============================================================================
# 1. GARDES-FOUS
# =============================================================================
base = bytearray(SRC.read_bytes())
if hashlib.md5(bytes(base)).hexdigest() != MD5_TERRAIN12:
    erreur("terrain.12 : md5 inattendu (source altérée ?)")

# gabarits T3 présents, exacts, uniques
off_gj = unique(bytes(base), GAB_JETON)
off_gs = unique(bytes(base), GAB_SESSION)
off_fail_gj = off_gj + len(PREFIX)          # début de « --fail »
off_fail_gs = off_gs + len(PREFIX)
if bytes(base[off_fail_gj:off_fail_gj + 7]) != b"--fail ":
    erreur("GABARIT_JETON : « --fail » pas à la position attendue")
if bytes(base[off_fail_gs:off_fail_gs + 7]) != b"--fail ":
    erreur("GABARIT_SESSION : « --fail » pas à la position attendue")
if base[off_gj - 1:off_gj] != b"\x00" or base[off_gs - 1:off_gs] != b"\x00":
    erreur("gabarits : NUL précédent absent (alignement de chaîne inattendu)")

# périmètre intouché : T2 ×2 + PUT, chacun unique, --fail présent
for mot in (MOT_T2_HTTP, MOT_T2_HTTPS, MOT_PUT):
    unique(bytes(base), mot)
if bytes(base).count(b"--fail") != 5:
    erreur(f"--fail : {bytes(base).count(b'--fail')} occurrences, 5 attendues")

# démo finale terrain.12 toujours embarquée + chaîne md5 S04C
demo9 = DEMO9.read_bytes()
if hashlib.md5(demo9).hexdigest() != MD5_DEMO9:
    erreur("demo/demo.exe : md5 inattendu")
if bytes(base[OFF_DEMO:OFF_DEMO + TAILLE_DEMO]) != demo9:
    erreur("la démo embarquée n'est plus demo.9 (terrain.12 altéré ?)")
if bytes(base[OFF_MD5_DEMO:OFF_MD5_DEMO + 32]) != MD5_DEMO9_B:
    erreur("chaîne md5 S04C : demo.9 introuvable")

# génération courante = 12 / terrain.12
OFF_L00 = rva2off(0x2ADA)
OFF_S00 = rva2off(0x4366)
if bytes(base[OFF_L00 - 8:OFF_L00 + 1]) != b"terrain12" or base[OFF_L00 + 1:OFF_L00 + 4] != b"L01":
    erreur("L00 : contexte inattendu")
if bytes(base[OFF_S00 - 8:OFF_S00 + 1]) != b"terrain12" or base[OFF_S00 + 1:OFF_S00 + 4] != b"S01":
    erreur("S00 : contexte inattendu")
for off_b in (0x5CD4, 0x5CDC):
    if struct.unpack_from("<H", base, off_b)[0] != 12:
        erreur(f"VERSIONINFO binaire @{off_b:#x} != 12")
if base[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] != "0.5.12":
    erreur("FileVersion inattendue")
if base[0x5EC0:0x5ECE].decode("utf-16-le") != "rrain12":
    erreur("ProductVersion (fin) inattendue")

# correctif ABI terrain.10 en place
if bytes(base[rva2off(0x5D1E):rva2off(0x5D1E) + 4]) != bytes.fromhex("4883ec28"):
    erreur("sup-34 .curl : correctif D62 absent")

# étiquettes de verdict T3 intactes (le code ne change pas)
for s in (b'"access_token":"', b"S33 T3 jeton OAuth ECHEC",
          b"S36 T3 VERDICT KO"):
    unique(bytes(base), s)
if b"https://oauth2.googleapis.com/token" not in bytes(base):
    erreur("URL_TOKEN absente (le champ \x08 du gabarit la reçoit du kit)")

# porte : 27 entrées vertes + couvreurs des zones touchées
entrees, idx_term, table_off = lire_table(base)
if idx_term != 27:
    erreur(f"table R10 : {idx_term} entrées, 27 attendues")
for k, (rva, ln, sm) in enumerate(entrees):
    if somme_zone(base, rva, ln) != sm:
        erreur(f"terrain.12 : R10[{k}] ROUGE avant patch")

def couvreurs(rva_z, ln_z):
    return {k for k, (rva, ln, sm) in enumerate(entrees)
            if not (rva + ln <= rva_z or rva_z + ln_z <= rva)}

def rva_depuis_off(off):
    # zone .text2 données : off = 0x2E00 + (rva - 0x4000)
    return 0x4000 + (off - 0x2E00)

zones = [("gabarit jeton (rva " + hex(rva_depuis_off(off_fail_gj)) + ")", off_fail_gj, 7),
         ("gabarit session (rva " + hex(rva_depuis_off(off_fail_gs)) + ")", off_fail_gs, 7),
         ("S00", OFF_S00, 2)]
for lab, off, ln in zones:
    cov = couvreurs(rva_depuis_off(off), ln)
    if cov != {23}:
        erreur(f"couvreurs de {lab} : {sorted(cov)} != [23]")
    print(f"[couv] {lab} couvert par R10{sorted(cov)}")

# =============================================================================
# 2. LE PATCH
# =============================================================================
img = bytearray(base)

# (a,b) les deux --fail T3 -> 7 espaces (longueur inchangée, zéro décalage)
img[off_fail_gj:off_fail_gj + 7] = b" " * 7
img[off_fail_gs:off_fail_gs + 7] = b" " * 7

# (c) génération : terrain12 -> terrain13
img[OFF_L00] = ord("3")
img[OFF_S00] = ord("3")

# (d) VERSIONINFO 0.5.13.0
struct.pack_into("<H", img, 0x5CD4, 13)
struct.pack_into("<H", img, 0x5CDC, 13)

# (e,f) FileVersion « 0.5.12 » -> « 0.5.13 », ProductVersion « rrain12 » -> « rrain13 »
img[0x5DC2:0x5DC4] = "3".encode("utf-16-le")
img[0x5ECC:0x5ECE] = "3".encode("utf-16-le")

# (g) somme R10[23] recalculée sur l'image finale
rva23, ln23, _ = entrees[23]
struct.pack_into("<Q", img, table_off + 16 * 23 + 8, somme_zone(img, rva23, ln23))

# =============================================================================
# 3. POST-VÉRIFICATIONS
# =============================================================================
# 3a. diff borné (2×7 --fail + L00 + S00 + 2×2 VERSIONINFO + 2×2 FV/PV + 8 somme)
autorisations = [
    (off_fail_gj, off_fail_gj + 7, "--fail jeton -> espaces"),
    (off_fail_gs, off_fail_gs + 7, "--fail session -> espaces"),
    (OFF_L00, OFF_L00 + 1, "L00"),
    (OFF_S00, OFF_S00 + 1, "S00"),
    (0x5CD4, 0x5CD6, "bin1"), (0x5CDC, 0x5CDE, "bin2"),
    (0x5DC2, 0x5DC4, "FV"), (0x5ECC, 0x5ECE, "PV"),
    (table_off + 16 * 23 + 8, table_off + 16 * 23 + 16, "somme R10[23]"),
]
diffs = [i for i in range(len(base)) if base[i] != img[i]]
hors = [i for i in diffs if not any(a <= i < b for a, b, _ in autorisations)]
if hors:
    erreur(f"{len(hors)} octets hors zones autorisées : {[hex(i) for i in hors[:8]]}")
print(f"[diff] {len(diffs)} octets modifiés, tous bornés "
      f"(2×7 --fail + 2 génération + 6 .rsrc + 8 somme)")

# 3b. porte ENTIÈRE verte
entrees_f, idx_term_f, _ = lire_table(img)
if idx_term_f != 27:
    erreur(f"table finale : {idx_term_f} entrées")
for k, (rva, ln, sm) in enumerate(entrees_f):
    if somme_zone(img, rva, ln) != sm:
        erreur(f"porte R10 ROUGE après patch à l'entrée [{k}]")
if struct.unpack_from("<IIQ", img, table_off + 16 * 27) != (0, 0, 0):
    erreur("le terminateur a bougé")
print("[porte] R10 : 27/27 entrées VERTES + terminateur intact")

# 3c. gabarits T3 patchés : espaces, marqueurs, NUL, longueur totale
if bytes(img[off_gj:off_gj + 81]) != GAB_JETON_APRES:
    erreur("GABARIT_JETON final inattendu")
if bytes(img[off_gs:off_gs + 232]) != GAB_SESSION_APRES:
    erreur("GABARIT_SESSION final inattendu")
if bytes(img).count(b"--fail") != 3:
    erreur(f"--fail finaux : {bytes(img).count(b'--fail')}, 3 attendus (T2×2 + PUT)")
print("[gab] jeton + session : --fail retiré, espaces in-place, marqueurs "
      "\\x08/\\x07 + NUL intacts, longueurs 81/232 inchangées")
print("      T2 ×2 + GABARIT_PUT : --fail CONSERVÉS (verdict-critiques)")

# 3d. le reste du binaire : octet pour octet identique
if img[OFF_ENETE_KIT[0]:OFF_ENETE_KIT[1]] != base[OFF_ENETE_KIT[0]:OFF_ENETE_KIT[1]]:
    erreur("l'en-tête kit (longueurs) a bougé")
if img[OFF_PROXY:OFF_ANNEXE] != base[OFF_PROXY:OFF_ANNEXE]:
    erreur("le proxy embarqué a bougé")
if img[OFF_ANNEXE:] != base[OFF_ANNEXE:]:
    erreur("l'annexe jetons a bougé")
if bytes(img[OFF_DEMO:OFF_DEMO + TAILLE_DEMO]) != demo9:
    erreur("la démo embarquée != demo.9")
if bytes(img[OFF_MD5_DEMO:OFF_MD5_DEMO + 32]) != MD5_DEMO9_B:
    erreur("chaîne md5 S04C modifiée")
if bytes(img[rva2off(0x5D1E):rva2off(0x5D1E) + 4]) != bytes.fromhex("4883ec28"):
    erreur("correctif sup-34 altéré")
print("[blob] kit/démo 73c064fb/proxy dd12b649/annexe/S04C/S05C/sup-34 : "
      "inchangés octet pour octet")

# 3e. identité
if bytes(img[OFF_L00 - 8:OFF_L00 + 1]) != b"terrain13" or bytes(img[OFF_S00 - 8:OFF_S00 + 1]) != b"terrain13":
    erreur("versions L00/S00 finales inattendues")
for off_b in (0x5CD4, 0x5CDC):
    if struct.unpack_from("<H", img, off_b)[0] != 13:
        erreur(f"VERSIONINFO finale inattendue @{off_b:#x}")
if img[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] != "0.5.13":
    erreur("FileVersion finale inattendue")
if img[0x5EC0:0x5ECE].decode("utf-16-le") != "rrain13":
    erreur("ProductVersion (fin) inattendue")
print("[ident] L00/S00 « terrain13 », VERSIONINFO 0.5.13.0, "
      "FileVersion « 0.5.13 », ProductVersion « …terrain13 »")

# 3f. prologue du proxy embarqué inchangé (probing D63, désassemblé)
try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    off_pro = OFF_PROXY + 0x2C00 + (0x5580 - 0x4000)
    code = bytes(img[off_pro:off_pro + 0x40])
    obtenu = [f"{i.mnemonic} {i.op_str}".rstrip() for i in md.disasm(code, 0x140005580)]
    attendu = [
        "push rbx", "push r12", "push r13", "push r14", "push r15",
        "mov r10, 0xfffffffffffff000",
        "mov rax, qword ptr [rsp + r10]",
        "sub r10, 0x1000",
        "cmp r10, -0x7000",
        "jge 0x140005590",
        "mov rax, qword ptr [rsp - 0x7100]",
        "sub rsp, 0x7100",
    ]
    if obtenu[:12] != attendu:
        erreur("prologue http-10 embarqué inattendu (proxy altéré ?)")
    print("[code] prologue http-10 embarqué intact : BOUCLE DE PROBING")
except ImportError:
    print("[code] capstone absent (FAIBLE)")

# 3g. empreintes + écriture
final = hashlib.md5(bytes(img)).hexdigest()
sha = hashlib.sha256(bytes(img)).hexdigest()
DST.write_bytes(bytes(img))
print(f"\n[patch] {DST} écrit ({len(img)} octets)")
print(f"  md5    {final}")
print(f"  sha256 {sha}")
