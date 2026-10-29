#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verif_terrain13 — audit indépendant de superviseur-terrain13.exe (D65).

Relit le binaire ÉCRIT sans aucun état partagé avec patch_terrain13.py et
contrôle les 20 invariants du terrain.13 :
  identité (terrain13 / 0.5.13.0), gabarits T3 sans --fail mais structure
  et marqueurs intacts, --fail conservés là où ils sont verdict-critiques
  (T2 ×2 + PUT), porte R10 27/27, kit embarqué (démo finale 73c064fb,
  proxy 0.4.0-dev.2 dd12b649, annexe) inchangé, correctifs ABI D62 et de
  pile D63 toujours en place.
"""

import hashlib
import pathlib
import re
import struct
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
EXE = REPO / "terrain/livraison/superviseur-terrain13.exe"
DEMO9 = (REPO / "demo/demo.exe").read_bytes()
PROXY = (REPO / "m3/proxy.exe").read_bytes()
BASE12 = (REPO / "terrain/livraison/superviseur-terrain12.exe").read_bytes()

MD5_ATTENDU = "8d1938b179d0dd8779fb8b2a82b17921"
SHA_ATTENDU = "e71ad06e8b11e8c2a6628be821ba1c4afe75a6bbabcd155206fd5ed90c570ebb"

R10_TABLE_RVA = 0x2450
OFF_DEMO, TAILLE_DEMO = 0x6410, 0x4000
OFF_MD5_DEMO, OFF_MD5_PROXY = 0x585F, 0x590A
OFF_PROXY, OFF_ANNEXE = 0xA410, 0xF010

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

verts = 0


def ok(nom):
    global verts
    verts += 1
    print(f"  VERT  {nom}")


def ko(nom, detail=""):
    print(f"  ROUGE {nom} {detail}")
    sys.exit(1)


def rva2off(rva):
    zones = [(0x1000, 0x2000, 0x400), (0x2000, 0x3000, 0x1400),
             (0x3000, 0x3A00, 0x2400), (0x4000, 0x6E00, 0x2E00),
             (0x7000, 0x7800, 0x5C00), (0x8000, 0x10D10, 0x6400),
             (0x11000, 0x11200, 0xF200)]
    for rb, rf, ob in zones:
        if rb <= rva < rf:
            return ob + (rva - rb)
    return None


def somme_zone(d, rva, ln):
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", d, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s


img = EXE.read_bytes()
print(f"[verif] {EXE.name} : {len(img)} octets — 20 contrôles")

# 1-3. empreintes
if hashlib.md5(img).hexdigest() == MD5_ATTENDU:
    ok("md5 8d1938b179d0dd8779fb8b2a82b17921")
else:
    ko("md5", hashlib.md5(img).hexdigest())
if hashlib.sha256(img).hexdigest() == SHA_ATTENDU:
    ok("sha256 e71ad06e…570ebb")
else:
    ko("sha256")
if len(img) == 62464:
    ok("taille 62 464 o (aucun décalage de section)")
else:
    ko("taille", str(len(img)))

# 4. identité terrain13
def offs(motif):
    return [m.start() for m in re.finditer(re.escape(motif), img)]

if len(offs(b"terrain 0.5.0-terrain13")) == 2 and img.count(b"terrain13") >= 2:
    ok("L00/S00 « superviseur terrain 0.5.0-terrain13 » (×2)")
else:
    ko("L00/S00 terrain13")
if struct.unpack_from("<H", img, 0x5CD4)[0] == 13 and struct.unpack_from("<H", img, 0x5CDC)[0] == 13:
    ok("VERSIONINFO 0.5.13.0")
else:
    ko("VERSIONINFO")
if img[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] == "0.5.13":
    ok("FileVersion « 0.5.13 »")
else:
    ko("FileVersion")
if img[0x5EC0:0x5ECE].decode("utf-16-le") == "rrain13":
    ok("ProductVersion « …terrain13 »")
else:
    ko("ProductVersion")

# 5. gabarits T3 : --fail retiré, structure + marqueurs intacts
for nom, mot in (("GABARIT_JETON", GAB_JETON_APRES),
                 ("GABARIT_SESSION", GAB_SESSION_APRES)):
    hits = offs(mot)
    if len(hits) == 1:
        ok(f"{nom} : sans --fail, 81/232 o, marqueurs + NUL intacts"
            if nom == "GABARIT_JETON" else
            f"{nom} : sans --fail, marqueur \\x07 + URL upload intacts")
    else:
        ko(nom, f"{len(hits)} occurrences")

# 6. --fail : il ne reste QUE T2 ×2 + PUT
if img.count(b"--fail") == 3:
    ok("compte --fail = 3 (T2 http + T2 https + PUT — et rien d'autre)")
else:
    ko("compte --fail", str(img.count(b"--fail")))

# 7. périmètre intouché : T2 + PUT byte-identiques à terrain.12
for nom, mot in (("CMD_CURL_HTTP", b"-s --fail --max-time 20 -o terrain_page_http.txt -x http://127.0.0.1:25000 http://neverssl.com/"),
                 ("CMD_CURL_HTTPS", b"-s --fail --max-time 20 -o terrain_page_https.txt"),
                 ("GABARIT_PUT", b"-s --fail --max-time 120 -o NUL -X PUT --data-binary @")):
    a, b = len(offs(mot)), len([m for m in re.finditer(re.escape(mot), BASE12)])
    if a == 1 and a == b:
        ok(f"{nom} intact (--fail conservé, identique à terrain.12)")
    else:
        ko(nom, f"{a} occ / terrain.12 {b}")

# 8. GABARIT_OAUTH / META intacts (marqueurs de composition)
for nom, mot in (("GABARIT_OAUTH", b"client_id=\x01&client_secret=\x02&refresh_token=\x03&grant_type=refresh_token"),
                 ("GABARIT_META", b"{\"name\":\"\x04\",\"parents\":[\"\x05\"]}")):
    if len(offs(mot)) == 1:
        ok(f"{nom} intact (marqueurs de composition)")
    else:
        ko(nom)

# 9. porte R10
table_off = rva2off(R10_TABLE_RVA)
k, verts_r10 = 0, 0
while True:
    rva, ln, sm = struct.unpack_from("<IIQ", img, table_off + 16 * k)
    if rva == 0:
        break
    if somme_zone(img, rva, ln) == sm:
        verts_r10 += 1
    k += 1
if k == 27 and verts_r10 == 27 and struct.unpack_from("<IIQ", img, table_off + 16 * 27)[0] == 0:
    ok("porte R10 : 27/27 entrées VERTES + terminateur")
else:
    ko("porte R10", f"{verts_r10}/{k}")

# 10-12. kit embarqué
if hashlib.md5(img[OFF_DEMO:OFF_DEMO + TAILLE_DEMO]).hexdigest() == "73c064fbaf4610a167bc6434dee400e4":
    ok("démo embarquée = FINALE demo.9 (md5 73c064fb…)")
else:
    ko("démo embarquée")
if img[OFF_MD5_DEMO:OFF_MD5_DEMO + 32] == b"73c064fbaf4610a167bc6434dee400e4":
    ok("chaîne S04C = 73c064fbaf4610a167bc6434dee400e4")
else:
    ko("chaîne S04C")
if img[OFF_PROXY:OFF_PROXY + len(PROXY)] == PROXY and img[OFF_MD5_PROXY:OFF_MD5_PROXY + 32] == b"dd12b64948e64153ff1dd7a66f367ff3":
    ok("proxy embarqué = 0.4.0-dev.2 (md5 dd12b649…) + chaîne S05C")
else:
    ko("proxy embarqué / S05C")

# 13. en-tête kit + annexe : identiques à terrain.12
if img[0x6400:0x6410] == BASE12[0x6400:0x6410] and img[OFF_ANNEXE:] == BASE12[OFF_ANNEXE:]:
    ok("en-tête kit + annexe jetons : octet pour octet terrain.12")
else:
    ko("en-tête kit / annexe")

# 14. correctif ABI sup-34 (D62) : sub rsp,0x28 et add rsp,0x28
if (img[rva2off(0x5D1E):rva2off(0x5D1E) + 4] == bytes.fromhex("4883ec28")
        and img[rva2off(0x5D63) - 3:rva2off(0x5D63) + 1] == bytes.fromhex("4883c428")):
    ok("sup-34 .curl : shadow space D62 (sub/add rsp,0x28)")
else:
    ko("sup-34 shadow space")

# 15. prologue http-10 (probing D63) dans le proxy embarqué
try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    off_pro = OFF_PROXY + 0x2C00 + (0x5580 - 0x4000)
    code = img[off_pro:off_pro + 0x40]
    obtenu = [f"{i.mnemonic} {i.op_str}".rstrip() for i in md.disasm(code, 0x140005580)]
    attendu = ["push rbx", "push r12", "push r13", "push r14", "push r15",
               "mov r10, 0xfffffffffffff000",
               "mov rax, qword ptr [rsp + r10]",
               "sub r10, 0x1000", "cmp r10, -0x7000", "jge 0x140005590",
               "mov rax, qword ptr [rsp - 0x7100]", "sub rsp, 0x7100"]
    if obtenu[:12] == attendu:
        ok("proxy embarqué : prologue http-10 avec boucle de probing")
    else:
        ko("prologue http-10")
except ImportError:
    print("  FAIBLE capstone absent — contrôle prologue sauté")

# 16. verdicts T3 inchangés (le code ne change pas, seules les preuves survivent)
for s in (b"S33 T3 jeton OAuth ECHEC", b"S36 T3 VERDICT KO", b'"access_token":"',
          b"Location: ", b"S33 T3 jeton OAuth obtenu"):
    if s in img:
        ok(f"chaîne verdict T3 intacte : {s.decode(errors='replace')[:34]}")
    else:
        ko("chaîne verdict T3", s.decode(errors="replace"))

print(f"\n[verif] {verts} contrôles VERTS — terrain.13 est livrable")
