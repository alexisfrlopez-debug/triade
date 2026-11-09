#!/usr/bin/env python3
"""Autopsie de loupe.exe dev.6 : table d'imports réelle vs slots appelés par le code."""
import struct, sys

data = open('/home/z/my-project/loupe-kit-7/loupe.exe', 'rb').read()

pe_off = struct.unpack_from('<I', data, 0x3C)[0]
opt = pe_off + 24
magic = struct.unpack_from('<H', data, opt)[0]
assert magic == 0x20b, "pas PE32+"
numdd = struct.unpack_from('<I', data, opt + 108)[0]
dd = opt + 112
names = ["EXPORT","IMPORT","RESOURCE","EXCEPTION","SECURITY","BASERELOC","DEBUG","ARCH","GLOBALPTR","TLS","LOAD_CONFIG","BOUND_IMPORT","IAT","DELAY_IMPORT","COM","RESERVED"]
dirs = {}
for i in range(16):
    rva, size = struct.unpack_from('<II', data, dd + i*8)
    dirs[names[i]] = (rva, size)
    if rva:
        print(f"dir[{i}] {names[i]}: RVA {hex(rva)} taille {hex(size)}")

# sections -> conversion RVA/off
secs = []
nsec = struct.unpack_from('<H', data, pe_off + 6)[0]
optsize = struct.unpack_from('<H', data, pe_off + 20)[0]
for i in range(nsec):
    s = opt + optsize + i*40
    nm = data[s:s+8].rstrip(b'\x00').decode()
    vsize, vaddr, rsize, raddr = struct.unpack_from('<IIII', data, s+8)
    secs.append((nm, vaddr, vsize, raddr, rsize))
    print(f"  {nm}: RVA {hex(vaddr)}+{hex(vsize)} file {hex(raddr)}+{hex(rsize)}")

def rva2off(rva):
    for nm, vaddr, vsize, raddr, rsize in secs:
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return raddr + (rva - vaddr)
    return None

def cstr(off):
    end = data.index(b'\x00', off)
    return data[off:end].decode('utf-8', 'replace')

def wstr(rva):
    off = rva2off(rva)
    out = []
    while True:
        w = struct.unpack_from('<H', data, off)[0]
        if w == 0: break
        out.append(chr(w)); off += 2
    return ''.join(out)

print("\n=== TABLE D'IMPORTS (ce que le VRAI chargeur Windows résoudra) ===")
imp_rva, imp_size = dirs["IMPORT"]
off = rva2off(imp_rva)
desc_i = 0
slots = {}   # slot RVA -> (dll, fonction)
while True:
    oft, tds, fwd, name_rva, first_thunk = struct.unpack_from('<IIIII', data, off + desc_i*20)
    if oft == 0 and first_thunk == 0:
        break
    dll = cstr(rva2off(name_rva))
    print(f"\n[{dll}]  FirstThunk(IAT) @{hex(first_thunk)}  OriginalFirstThunk @{hex(oft)}")
    thunk_rva = oft if oft else first_thunk
    t_off = rva2off(thunk_rva)
    iat_off = rva2off(first_thunk)
    j = 0
    while True:
        val = struct.unpack_from('<Q', data, t_off + j*8)[0]
        if val == 0: break
        slot_rva = first_thunk + j*8
        if val & (1 << 63):
            fn = f"ordinal#{val & 0xffff}"
        else:
            fn = cstr(rva2off(val + 2))
        slots[slot_rva] = (dll, fn)
        hint = struct.unpack_from('<H', data, rva2off(val))[0]
        print(f"  slot {hex(slot_rva)}: {fn} (hint {hint}, thunk file {hex(t_off+j*8)})")
        j += 1
    desc_i += 1

print(f"\n=== {len(slots)} feuilles au total ===")

# les slots que le CODE appelle (extraits du désassemblage d'entrée + fenêtres)
code_slots = {
    0x2400: "GetModuleHandleW (entrée, fix 209)",
    0x2408: "GetCommandLineW (entrée)",
    0x2410: "ExitProcess (entrée)",
    0x2450: "RegisterClassExW (entrée)",
    0x2458: "CreateWindowExW (entrée)",
    0x2460: "ShowWindow (entrée)",
    0x24C8: "LoadCursorW (entrée)",
}
print("\n=== RECROISEMENT : slot appelé par le code vs fonction réellement résolue ===")
for slot, usage in sorted(code_slots.items()):
    if slot in slots:
        dll, fn = slots[slot]
        mark = "OK " if usage.split()[0].lower() == fn.lower() else "*** MISMATCH ***"
        print(f"slot {hex(slot)} attendu={usage:45s} réel={dll}!{fn}  {mark}")
    else:
        print(f"slot {hex(slot)} attendu={usage:45s} *** SLOT HORS TABLE D'IMPORTS ***")

# chaînes de classe / titre
print("\n=== CHAÎNES ===")
print("classe  @0x2600:", repr(wstr(0x2600)))
print("titre   @0x2614:", repr(wstr(0x2614)))
# version
print("qword version @RVA 0x2E80:", hex(struct.unpack_from('<Q', data, rva2off(0x2E80))[0]))
