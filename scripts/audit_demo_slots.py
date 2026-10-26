#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Table d'imports réelle de demo.exe : slot FT -> fonction, par descripteur.

Vérifie que chaque slot appelé par win-04 (voir désassemblage) désigne bien
la fonction attendue — la classe de défaut D35 (slot désaligné) a déjà frappé
une fois ; le bouton invisible pourrait en être une récidive masquée.
"""
import struct

EXE = "/home/z/my-project/triade/demo/demo.exe"
data = open(EXE, "rb").read()
pe = struct.unpack_from("<I", data, 0x3C)[0]
nsec = struct.unpack_from("<H", data, pe + 6)[0]
opt = struct.unpack_from("<H", data, pe + 20)[0]
secs = []
for i in range(nsec):
    off = pe + 24 + opt + i * 40
    nom = data[off:off + 8].rstrip(b"\0").decode()
    vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", data, off + 8)
    secs.append((nom, vaddr, vsize, raddr, rsize))


def r2f(rva):
    for nom, vaddr, vsize, raddr, rsize in secs:
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return raddr + (rva - vaddr)
    return None


# répertoire imports (index 1 du data directory)
dd = pe + 24 + opt - 128 + 8  # data directories commencent après les 112 o fixes? non:
# optionnel: PE32+ : data directory à pe+24+112
ddoff = pe + 24 + 112
imp_rva, imp_taille = struct.unpack_from("<II", data, ddoff + 8)
print(f"imports : RVA 0x{imp_rva:x}, taille 0x{imp_taille:x}")

slots = {}
o = r2f(imp_rva)
n = 0
while True:
    oft, tds, fc, namerva, ft = struct.unpack_from("<IIIII", data, o + n * 20)
    if oft == 0 and ft == 0:
        break
    dll = data[r2f(namerva):].split(b"\0")[0].decode()
    print(f"\ndescripteur {dll} : OFT 0x{oft:x} FT 0x{ft:x}")
    # entrées thunk
    fo = r2f(oft if oft else ft)
    i = 0
    while True:
        thunk = struct.unpack_from("<Q", data, fo + i * 8)[0]
        if thunk == 0:
            break
        slot = ft + i * 8
        if thunk & (1 << 63):
            nomf = f"ordinal#{thunk & 0xFFFF}"
        else:
            hn = r2f(thunk & 0x7FFFFFFF)
            hint = struct.unpack_from("<H", data, hn)[0]
            nomf = data[hn + 2:].split(b"\0")[0].decode()
        slots[slot] = f"{dll}!{nomf}"
        if 0x2800 <= slot <= 0x2A00 or slot in (0x20F8, 0x2100):
            print(f"  slot 0x{slot:04x} = {dll}!{nomf} (hint {hint})")
        i += 1
    n += 1

print("\n=== slots appelés par win-04 (vérification) ===")
APPELES = {
    0x2100: "GetModuleHandleW", 0x2808: "CreateWindowExW",
    0x2E98: "GetLastError", 0x2980: "GetStockObject",
    0x2840: "SendMessageW", 0x2860: "GetClientRect",
    0x2858: "MoveWindow", 0x2850: "CloseHandle",
    0x2838: "DestroyWindow", 0x2830: "PostQuitMessage",
    0x2810: "DefWindowProcW", 0x2868: "MessageBoxW",
    0x20F8: "CloseHandle (kernel32)",
}
ok = True
for slot, attendu in sorted(APPELES.items()):
    reel = slots.get(slot, "— AUCUN —")
    marque = "OK " if reel.split("!")[-1] == attendu.split(" ")[0] else "*** DIVERGENT ***"
    if marque != "OK ":
        ok = False
    print(f"  0x{slot:04x} : attendu {attendu:28s} réel {reel:40s} {marque}")
print("\nVERDICT :", "slots conformes" if ok else "DIVERGENCE DÉTECTÉE")
