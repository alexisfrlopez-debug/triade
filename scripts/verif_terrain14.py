#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verif_terrain14 — vérification indépendante du livrable D68 (terrain.14).

Deux volets :
  A. STATIQUE — le fichier livré supervis-terrain14.exe relu de zéro :
     identité (md5/sha256/taille), génération terrain14 (L00/S00/
     VERSIONINFO/FileVersion/ProductVersion), porte R10 27/27 recalculée,
     sites patchés (handler -> relais, relais 6 instructions + chaîne,
     mov r13d 4, leas repointées, bloc de noms réordonné), 4 branches
     intactes vers 0x6113, xref du bloc de noms = 5 sites aux cibles
     réordonnées, périmètre intouché (--fail T2×2+PUT, gabarits T3 sans
     --fail, démo 73c064fb, proxy, annexe, correctif sup-34, chaîne S33
     originale encore présente), prologue http-10.
  B. ÉMULATION (unicorn) — le chemin T3-échec exécuté instruction par
     instruction depuis .jeton_ko (0x6113), journal et fichiers stubés :
     E1 [0x3B50]=26 : 2 appels journal exacts — « S33 T3 jeton KO code= »
        (21 o, mode 1, valeur 26) puis « S36 T3 VERDICT KO » (mode 0) —
        PUIS 4 suppressions sup-36 dans l'ordre req/meta/session/rep,
        AUCUNE sur terrain_jeton.json, arrêt propre à .fin (0x627B) ;
     E2 [0x3B50]=7 : idem avec code=7 (discrimination réseau).
"""

import hashlib
import pathlib
import struct
import sys

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

REPO = pathlib.Path("/home/z/my-project/triade")
EXE13 = REPO / "terrain/livraison/superviseur-terrain13.exe"
EXE14 = REPO / "terrain/livraison/superviseur-terrain14.exe"
DEMO9 = REPO / "demo/demo.exe"

MD5_14 = "1958cbfb9afb3345c2381c0dc2e135f4"
SHA_14 = "f71d81edfa32bf8042185e52818fa4e6ed7109d5894fc7b17612fa1eb10526d9"
MD5_DEMO9 = "73c064fbaf4610a167bc6434dee400e4"

data = EXE14.read_bytes()
base13 = EXE13.read_bytes()
ok = 0


def check(cond, lab):
    global ok
    if not cond:
        print(f"ECHEC : {lab}")
        sys.exit(1)
    ok += 1


# ---------------------------------------------------------------- identité
check(len(data) == 62464, "taille")
check(hashlib.md5(data).hexdigest() == MD5_14, "md5")
check(hashlib.sha256(data).hexdigest() == SHA_14, "sha256")

pe = pefile.PE(data=data, fast_load=True)
BASE = pe.OPTIONAL_HEADER.ImageBase


def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.SizeOfRawData:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None


off = lambda r: rva2off(r)  # noqa: E731
md = Cs(CS_ARCH_X86, CS_MODE_64)

# ---------------------------------------------------------------- génération
check(bytes(data[off(0x2ADA) - 8:off(0x2ADA) + 1]) == b"terrain14", "L00 terrain14")
check(bytes(data[off(0x4366) - 8:off(0x4366) + 1]) == b"terrain14", "S00 terrain14")
check(struct.unpack_from("<H", data, 0x5CD4)[0] == 14
      and struct.unpack_from("<H", data, 0x5CDC)[0] == 14, "VERSIONINFO 14")
check(data[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] == "0.5.14",
      "FileVersion 0.5.14")
check(data[0x5EC0:0x5ECE].decode("utf-16-le") == "rrain14", "ProductVersion terrain14")

# ---------------------------------------------------------------- porte R10
R10_TABLE_RVA = 0x2450
toff = off(R10_TABLE_RVA)
k = 0
while struct.unpack_from("<IIQ", data, toff + 16 * k)[0] != 0:
    rva, ln, sm = struct.unpack_from("<IIQ", data, toff + 16 * k)
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    check(s == sm, f"R10[{k}] verte")
    k += 1
check(k == 27, "27 entrées R10")

# ---------------------------------------------------------------- sites patchés
# handler : jmp 0x628A + 20 NOP
ins = list(md.disasm(bytes(data[off(0x6113):off(0x6113) + 5]), 0x6113))
check(len(ins) == 1 and ins[0].mnemonic == "jmp"
      and ins[0].op_str == "0x628a", "handler = jmp 0x628a")
check(bytes(data[off(0x6118):off(0x6113) + 25]) == b"\x90" * 20, "20 NOP derrière")

# relais : 6 instructions exactes
ins = list(md.disasm(bytes(data[off(0x628A):off(0x628A) + 32]), 0x628A))
attendu = ["lea rcx, [rip + 0x19]", "mov edx, 0x15", "mov r8b, 1",
           "mov r9d, dword ptr [rip - 0x2750]", "call 0x5000", "jmp 0x615c"]
check([f"{i.mnemonic} {i.op_str}" for i in ins] == attendu, "relais 6 instructions")
check(bytes(data[off(0x62AA):off(0x62AA) + 22]) == b"S33 T3 jeton KO code=\x00",
      "chaîne S33 @0x62AA")
# cohérence des disp du relais
check(0x6291 + 0x19 == 0x62AA, "lea relais -> chaîne")
check(0x62A0 - 0x2750 == 0x3B50, "mov r9d -> code de sortie")

# nettoyage : 4 fichiers
ins = list(md.disasm(bytes(data[off(0x617D):off(0x617D) + 6]), 0x617D))
check(f"{ins[0].mnemonic} {ins[0].op_str}" == "mov r13d, 4", "mov r13d, 4")

# leas repointées + bloc de noms
for site, cible in ((0x5EFC, 0x635A), (0x5F83, 0x6323), (0x5FF8, 0x6335)):
    disp = struct.unpack_from("<i", data, off(site) + 3)[0]
    check(site + 7 + disp == cible, f"lea @{site:#x} -> {cible:#x}")
noms = []
cur = 0x6313
for _ in range(5):
    o = off(cur)
    fin = data.index(b"\x00", o)
    noms.append(bytes(data[o:fin]).decode())
    cur += (fin - o) + 1
check(noms == ["terrain_req.txt", "terrain_meta.json", "terrain_session.txt",
               "terrain_rep.json", "terrain_jeton.json"], "ordre des noms")
check(cur == 0x636D, "fin de bloc 0x636D")

# 4 branches intactes vers 0x6113
for site, hexs in {0x5EBB: "0f8452020000", 0x5EF6: "0f8517020000",
                   0x5F16: "0f84f7010000", 0x5F58: "0f84b5010000"}.items():
    check(bytes(data[off(site):off(site) + 6]) == bytes.fromhex(hexs),
          f"branche @{site:#x} intacte")

# ------------------------------------------------- périmètre intouché
check(data.count(b"--fail") == 3, "--fail ×3 (T2×2 + PUT)")
for mot in (b"-s --fail --max-time 20 -o terrain_page_http.txt",
            b"-s --fail --max-time 20 -o terrain_page_https.txt",
            b"-s --fail --max-time 120 -o NUL -X PUT"):
    check(data.count(mot) == 1, f"mot T2/PUT unique : {mot[:30]}…")
GAB_JETON_13 = (b"curl.exe -s" + b" " * 8 +
                b"--max-time 30 -o terrain_jeton.json "
                b"--data @terrain_req.txt \x08\x00")
check(data.count(GAB_JETON_13) == 1, "GABARIT_JETON sans --fail intact")
demo9 = DEMO9.read_bytes()
check(hashlib.md5(demo9).hexdigest() == MD5_DEMO9, "demo.9 source")
check(bytes(data[0x6410:0x6410 + 0x4000]) == demo9, "démo embarquée")
check(bytes(data[0x585F:0x585F + 32]) == MD5_DEMO9.encode(), "S04C")
check(data[0xA410:0xF010] == base13[0xA410:0xF010], "proxy inchangé")
check(data[0xF010:] == base13[0xF010:], "annexe jetons inchangée")
check(data[0x6400:0x6410] == base13[0x6400:0x6410], "en-tête kit inchangé")
check(bytes(data[off(0x5D1E):off(0x5D1E) + 4]) == bytes.fromhex("4883ec28"),
      "correctif sup-34")
for s in (b'"access_token":"', b"S33 T3 jeton OAuth ECHEC",
          b"S36 T3 VERDICT KO", b"S31 T3 jetons absents"):
    check(data.count(s) == 1, f"étiquette présente : {s[:25]}…")
check(bytes(data[off(0x612C):off(0x612C) + 25]) == bytes(base13[off(0x612C):off(0x612C) + 25]),
      ".session_ko inchangé")
check(b"https://oauth2.googleapis.com/token" in data, "URL token")
off_pro = 0xA410 + 0x2C00 + (0x5580 - 0x4000)
pro = [f"{i.mnemonic} {i.op_str}".rstrip()
       for i in md.disasm(bytes(data[off_pro:off_pro + 0x40]), 0x140005580)]
check(pro[5] == "mov r10, 0xfffffffffffff000" and pro[11] == "sub rsp, 0x7100",
      "prologue http-10 (probing)")
print(f"[A] STATIQUE : {ok} contrôles VERTS")

# =============================================================================
# B. ÉMULATION — chemin T3-échec depuis .jeton_ko
# =============================================================================
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX,  # noqa: E402
                               UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9)


def emuler(code_sortie):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    # mapper toutes les sections (raw + remplissage zéro jusqu'à vsize)
    for s in pe.sections:
        debut = (BASE + s.VirtualAddress) & ~0xFFF
        fin = (BASE + s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData) + 0xFFF) & ~0xFFF
        uc.mem_map(debut, fin - debut)
        if s.SizeOfRawData:
            uc.mem_write(BASE + s.VirtualAddress,
                         bytes(data[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]))
    # pile
    uc.mem_map(BASE + 0x200000, 0x10000)
    uc.reg_write(UC_X86_REG_RSP, BASE + 0x210000 - 0x100)
    # stubs : journal (rva 0x5000) et sup-36 fichiers (rva 0x4e00)
    STUB = b"\xb8\x01\x00\x00\x00\xc3"          # mov eax, 1 ; ret
    uc.mem_write(BASE + 0x5000, STUB)
    uc.mem_write(BASE + 0x4E00, STUB)
    # code de sortie curl
    uc.mem_write(BASE + 0x3B50, struct.pack("<I", code_sortie))

    appels = {"journal": [], "sup36": []}

    def hook(uc_, addr, taille, user):
        rva = addr - BASE
        if rva == 0x627B:                       # .fin atteint
            uc_.emu_stop()
            return
        if rva == 0x5000:
            rcx = uc_.reg_read(UC_X86_REG_RCX)
            txt = bytes(uc_.mem_read(rcx, 24))
            appels["journal"].append((rcx - BASE,
                                      uc_.reg_read(UC_X86_REG_RDX),
                                      uc_.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF,
                                      uc_.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF,
                                      txt))
        elif rva == 0x4E00:
            rcx = uc_.reg_read(UC_X86_REG_RCX)
            nom = b""
            a = rcx
            while True:
                c = bytes(uc_.mem_read(a, 1))
                if c == b"\x00":
                    break
                nom += c
                a += 1
            appels["sup36"].append((uc_.reg_read(UC_X86_REG_RDX), nom.decode()))

    uc.hook_add(UC_HOOK_CODE, hook)
    uc.emu_start(BASE + 0x6113, BASE + 0x627B, count=200000)
    return appels


for code_test in (26, 7):
    appels = emuler(code_test)
    check(len(appels["journal"]) == 2, f"[code={code_test}] 2 lignes journal")
    rva_txt, lon, mode, val, brut = appels["journal"][0]
    check(rva_txt == 0x62AA, f"[code={code_test}] ligne 1 -> chaîne 0x62AA")
    check(brut[:21] == b"S33 T3 jeton KO code=", f"[code={code_test}] texte ligne 1")
    check(lon == 21, f"[code={code_test}] edx=21")
    check(mode == 1, f"[code={code_test}] mode 1")
    check(val == code_test, f"[code={code_test}] valeur journalisée = {code_test}")
    rva_txt2, lon2, mode2, _, brut2 = appels["journal"][1]
    check(brut2[:17] == b"S36 T3 VERDICT KO", f"[code={code_test}] ligne 2 = S36 KO")
    check(mode2 == 0 and lon2 == 17, f"[code={code_test}] ligne 2 mode 0")
    check(len(appels["sup36"]) == 4, f"[code={code_test}] 4 suppressions")
    noms_sup = [n for op, n in appels["sup36"]]
    check(all(op == 2 for op, _ in appels["sup36"]), f"[code={code_test}] op=2 (supprimer)")
    check(noms_sup == ["terrain_req.txt", "terrain_meta.json",
                       "terrain_session.txt", "terrain_rep.json"],
          f"[code={code_test}] ordre suppressions {noms_sup}")
    check("terrain_jeton.json" not in noms_sup,
          f"[code={code_test}] terrain_jeton.json SURVIT")
    print(f"[B] code={code_test} : journal « S33 T3 jeton KO code={code_test} » "
          f"+ S36 KO + 4 suppressions, jeton.json survit — VERT")

print(f"\n[verif] TOUT VERT : {ok} contrôles statiques + 2 émulations complètes")
print(f"  md5    {hashlib.md5(data).hexdigest()}")
print(f"  sha256 {hashlib.sha256(data).hexdigest()}")
