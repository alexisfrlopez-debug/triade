#!/usr/bin/env python3
"""Scan de loupe.exe : chaque call/jmp [rip+X] -> RVA cible ; vérifie la couverture IAT.
Les sections exécutables : .text (RVA 0x1000, file 0x200, 0x1000) et .text2 (RVA 0x4000, file 0x3200, 0xA000)."""
import struct
from capstone import *

data = open('/home/z/my-project/loupe-kit-7/loupe.exe', 'rb').read()

# couverture IAT (déjà établie par autopsie_imports.py)
KERNEL32 = list(range(0x2400, 0x2450, 8))   # 10
USER32_1 = list(range(0x2450, 0x24E0, 8))   # 18
GDI32    = list(range(0x24E0, 0x2510, 8))   # 6
USER32_2 = list(range(0x2818, 0x2830, 8))   # 3 (double entrée démo)
COUVERT = set(KERNEL32 + USER32_1 + GDI32 + USER32_2)

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = False

def scan(rva_start, rva_end, file_off, label):
    print(f"===== {label} : appels indirects [rip+X] =====")
    code = data[file_off:file_off + (rva_end - rva_start)]
    trouve = []
    for i in md.disasm(code, rva_start):
        if i.mnemonic in ('call', 'jmp') and i.op_str.startswith('qword ptr [rip'):
            # calcule la cible
            disp = int(i.op_str.split('rip')[1].split(']')[0].replace(' ', ''), 16 if '0x' in i.op_str else 0)
            cible = i.address + i.size + disp
            couv = cible in COUVERT
            trouve.append((i.address, i.mnemonic, cible, couv))
            marque = "OK " if couv else "*** SLOT NON COUVERT ***"
            print(f"0x{i.address:x}: {i.mnemonic} [{hex(cible)}]  {marque}")
    return trouve

t1 = scan(0x1000, 0x2000, 0x200, ".text (minilibc M1 + boucle démo)")
t2 = scan(0x4000, 0xE000, 0x3200, ".text2 (les blocs loupe)")

total = t1 + t2
non_couverts = [t for t in total if not t[3]]
print(f"\n=== BILAN : {len(total)} appels indirects scannés, {len(non_couverts)} NON COUVERTS ===")
for a, m, c, _ in non_couverts:
    print(f"  0x{a:x}: {m} -> slot {hex(c)}")
