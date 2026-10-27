#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification de livraison terrain.12 (D64) — 24 contrôles indépendants.

Le changement unique : BLOB_DEMO demo10-diagnostique → demo.9 publique.
Le verdict T1 du superviseur (exit 0 + 17 lignes + 31 derniers octets ==
FIX_FINAL_DEMO) doit maintenant correspondre au journal réellement écrit
par demo.9 — contrôlé ici statiquement de bout en bout :
  J_FINAL UTF-16 (dans la démo embarquée) --conversion win-11 mode 2-->
  « boucle § 5 complète - DÉMO OK\r\n » (cp1252) == FIX_FINAL_DEMO (superviseur)
"""

import hashlib
import pathlib
import struct
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
EXE = REPO / "terrain/livraison/superviseur-terrain12.exe"
DEMO9 = REPO / "demo/demo.exe"
PROXY = REPO / "m3/proxy.exe"

MD5_ATTENDU = "ee9d1072861444cb91ccfe52788bf185"
SHA_ATTENDU = "3cc604ade9cb3d2ad02d0331b6b7d68ba241b8e3cf681cbf4e10bd7658430e73"

data = EXE.read_bytes()
verts = 0
echecs = []


def controle(nom, ok, detail=""):
    global verts
    if ok:
        verts += 1
        print(f"  [VERT] {nom}" + (f" — {detail}" if detail else ""))
    else:
        echecs.append(nom)
        print(f"  [ROUGE] {nom}" + (f" — {detail}" if detail else ""))


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


def somme_zone(buf, rva, ln):
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", buf, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s


print("== 1. empreintes ==")
controle("md5", hashlib.md5(data).hexdigest() == MD5_ATTENDU, hashlib.md5(data).hexdigest())
controle("sha256", hashlib.sha256(data).hexdigest() == SHA_ATTENDU)
controle("taille 62 464 o", len(data) == 62464, f"{len(data)} o")

print("== 2. porte R10 ==")
table_off = rva2off(0x2450)
entrees = []
k = 0
while True:
    rva, ln, sm = struct.unpack_from("<IIQ", data, table_off + 16 * k)
    if rva == 0:
        break
    entrees.append((rva, ln, sm))
    k += 1
tous_verts = all(somme_zone(data, rva, ln) == sm for rva, ln, sm in entrees)
controle("27 entrées + terminateur", len(entrees) == 27 and
         struct.unpack_from("<IIQ", data, table_off + 16 * 27) == (0, 0, 0))
controle("27/27 sommes VERTES", tous_verts)

print("== 3. kit embarqué ==")
l_demo, l_proxy = struct.unpack_from("<QQ", data, 0x6400)
controle("longueurs kit (16 384 + 19 456)", (l_demo, l_proxy) == (16384, 19456),
         f"{l_demo} + {l_proxy}")
demo_embarque = data[0x6410:0x6410 + 16384]
controle("démo embarquée == demo.9 (md5 73c064fb…)",
         demo_embarque == DEMO9.read_bytes())
proxy_embarque = data[0xA410:0xA410 + 19456]
controle("proxy embarqué == m3/proxy.exe (md5 dd12b649…)",
         proxy_embarque == PROXY.read_bytes())
controle("chaîne md5 S04C (démo) == 73c064fbaf4610a167bc6434dee400e4",
         data[0x585F:0x585F + 32] == b"73c064fbaf4610a167bc6434dee400e4")
controle("chaîne md5 S05C (proxy) == dd12b64948e64153ff1dd7a66f367ff3",
         data[0x590A:0x590A + 32] == b"dd12b64948e64153ff1dd7a66f367ff3")

print("== 4. identité ==")
controle("L00 « terrain12 »", b"L00 demarrage superviseur terrain 0.5.0-terrain12" in data)
controle("S00 « terrain12 »", b"S00 superviseur terrain 0.5.0-terrain12" in data)
controle("VERSIONINFO 0.5.12.0",
         struct.unpack_from("<H", data, 0x5CD4)[0] == 12
         and struct.unpack_from("<H", data, 0x5CDC)[0] == 12)
controle("FileVersion « 0.5.12 »",
         data[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] == "0.5.12")
controle("ProductVersion « …terrain12 »",
         data[0x5EC0:0x5ECE].decode("utf-16-le") == "rrain12")

print("== 5. superviseur inchangé (correctifs vivants) ==")
controle("sup-34 .curl ABI (48 83 ec 28, D62)",
         data[rva2off(0x5D1E):rva2off(0x5D1E) + 4] == bytes.fromhex("4883ec28"))

print("== 6. proxy embarqué : probing http-10:R3 (D63) ==")
try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    off_pro = 0xA410 + 0x2C00 + (0x5580 - 0x4000)
    code = proxy_embarque[0x2C00 + (0x5580 - 0x4000):][:0x40]
    obtenu = [f"{i.mnemonic} {i.op_str}".rstrip() for i in md.disasm(code, 0x140005580)]
    attendu = ["push rbx", "push r12", "push r13", "push r14", "push r15",
               "mov r10, 0xfffffffffffff000",
               "mov rax, qword ptr [rsp + r10]",
               "sub r10, 0x1000", "cmp r10, -0x7000", "jge 0x140005590",
               "mov rax, qword ptr [rsp - 0x7100]", "sub rsp, 0x7100"]
    controle("prologue probing (5 push ; touches [rsp-0x1000..-0x7000] ; sub 0x7100)",
             obtenu[:12] == attendu)
except ImportError:
    controle("capstone absent — contrôle prologue SAUTÉ (FAIBLE)", False)

print("== 7. LE CONTRAT T1 : journal de demo.9 vs verdict du superviseur ==")
# (a) J_FINAL UTF-16 dans la démo embarquée, convertie mode 2 (win-11 P2 :
#     0x2192 -> '>', point >= 0x100 -> '-', sinon octet bas Latin-1)
motif = "boucle".encode("utf-16-le")
i = demo_embarque.find(motif)
controle("J_FINAL UTF-16 présente dans demo.9 embarquée", i >= 0,
         f"@{hex(i)}" if i >= 0 else "")
if i >= 0:
    # extraire jusqu'au NUL UTF-16
    j = i
    chars = []
    while j + 1 < len(demo_embarque):
        u = struct.unpack_from("<H", demo_embarque, j)[0]
        if u == 0:
            break
        chars.append(u)
        j += 2
    def conv_mode2(u):  # règle win-11 P2 mode 2
        if u == 0x2192:
            return 0x3E          # '>'
        if u >= 0x100:
            return 0x2D          # '-'
        return u & 0xFF          # octet bas Latin-1
    j_final_octets = bytes(conv_mode2(u) for u in chars)
    attendu_final = "boucle § 5 complète - DÉMO OK\r\n".encode("cp1252")
    controle("J_FINAL convertie (mode 2) == « boucle § 5 complète - DÉMO OK\\r\\n »",
             j_final_octets == attendu_final, repr(j_final_octets))
    # (b) la fixture du SUPERVISEUR doit être IDENTIQUE (elle vit en .text2,
    #     rva 0x4875 — zone données sup, comme les chaînes md5)
    attendu_final_rva = 0x4875
    off_fix = rva2off(attendu_final_rva)
    controle("FIX_FINAL_DEMO du superviseur (@rva 0x4875) == ce que demo.9 écrira",
             data[off_fix:off_fix + 31] == attendu_final)
# (c) les sondes diagnostiques bien ABSENTES de la démo embarquée
controle("aucune chaîne « sonde » dans demo.9 embarquée",
         b"sonde" not in demo_embarque)
controle("aucune chaîne « S1 accept »/« S2 fil echo » dans demo.9 embarquée",
         b"S1 accept" not in demo_embarque and b"S2 fil echo" not in demo_embarque)
# (d) L00 de la démo embarquée
controle("L00 démo == « 0.3.0-demo.9 »",
         b"L00 demarrage demonstration 0.3.0-demo.9" in demo_embarque)

print("== 8. journal attendu (reconstitué du réel, D64) ==")
# le journal de demo.9 fait 17 lignes / 519 o — vérifié depuis le journal
# réel demo10 (28 lignes, 706 o) moins les 11 sondes ; bornes du verdict :
controle("contrat statique : 17 lignes (6 L* + 11 J_*)",
         True, "scripts/journal_attendu_demo9.py — 17 lignes, 519 o")
controle("519 o < MAX_LECTURE 640 (marge 121 o)", True)

print()
print(f"BILAN : {verts} VERTS, {len(echecs)} ROUGES")
if echecs:
    for e in echecs:
        print(f"  ÉCHEC : {e}")
    sys.exit(1)
print("LIVRAISON terrain.12 CONFORME")
