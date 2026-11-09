#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventaire exhaustif des appels indirects de loupe.exe dev.7 : chaque
call/jmp [rip+disp] est classé — NOUVELLE IAT (0x3100-0x3248), VIEILLES
PLAGES VIDÉES (0x2400-0x2510, 0x2818-0x2830), ou AILLEURS.

La retouche dev.7 devait repointer les 63 sites. Le scénario n'exécute
que les fonctions scellées (fichier) — les sites du chemin VITRINE ne
sont couverts par AUCUN test. Un site resté sur une vieille plage vide
appelle NULL : 0xC0000005 sans témoin WER, la fenêtre jamais née.
"""
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import capstone.x86_const as xc

EXE = "/home/z/my-project/run8/loupe.exe"
d = open(EXE, "rb").read()
e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
coff = e_lfanew + 4
machine, nsec, tds, ps, ns, optsz, chars = struct.unpack_from("<HHIIIHH", d, coff)
opt = coff + 20
sec_off = opt + optsz
sections = []
for i in range(nsec):
    s = sec_off + 40 * i
    nom = d[s:s + 8].rstrip(b"\0").decode("ascii", "replace")
    vs = struct.unpack_from("<I", d, s + 8)[0]
    va = struct.unpack_from("<I", d, s + 12)[0]
    ptr = struct.unpack_from("<I", d, s + 20)[0]
    raw = struct.unpack_from("<I", d, s + 16)[0]
    sections.append((nom, va, vs, ptr, raw))

# la carte IAT : slot → fonction
imp_rva = struct.unpack_from("<I", d, opt + 112 + 8)[0]


def r2o(rva):
    for (nom, va, vs, ptr, raw) in sections:
        if va <= rva < va + max(vs, raw):
            return ptr + (rva - va)
    return None


carte_iat = {}
off = r2o(imp_rva)
i = 0
while True:
    oft, tds, fwd, namerva, ft = struct.unpack_from("<IIIII", d, off + 20 * i)
    if oft == 0 and namerva == 0 and ft == 0:
        break
    o = r2o(ft)
    n = 0
    while True:
        v = struct.unpack_from("<Q", d, o + 8 * n)[0]
        if v == 0:
            break
        no = r2o(v)
        fin = d.find(b"\0", no + 2)
        carte_iat[ft + 8 * n] = d[no + 2:fin].decode("ascii", "replace")
        n += 1
    i += 1

NOUVELLE_IAT = (0x3100, 0x3248)
VIEILLES = [(0x2400, 0x2510), (0x2818, 0x2830)]

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

total = {"nouvelle": 0, "vieille": 0, "ailleurs": 0}
sites_vieilles = []
sites_ailleurs = []

for (nom, va, vs, ptr, raw) in sections:
    if not (va in (0x1000, 0x4000)):  # .text et .text2 seulement
        continue
    code = d[ptr:ptr + raw]
    # on balaie en suivant les instructions depuis des points de sync connus :
    # démarrage à chaque frontière de 16 octets serait bruité ; on utilise le
    # désassembleur en flux continu depuis le début de section (les nops
    # d'alignement 0x90 se désassemblent proprement, le flux reste synchrone)
    for ins in md.disasm(code, va):
        if ins.mnemonic in ("call", "jmp") and ins.operands:
            op = ins.operands[0]
            if op.type == xc.X86_OP_MEM and op.mem.base == xc.X86_REG_RIP:
                cible = ins.address + ins.size + op.mem.disp
                if NOUVELLE_IAT[0] <= cible < NOUVELLE_IAT[1]:
                    total["nouvelle"] += 1
                elif any(a <= cible < b for (a, b) in VIEILLES):
                    total["vieille"] += 1
                    q = struct.unpack_from("<Q", d, r2o(cible))[0] if r2o(cible) else -1
                    sites_vieilles.append((ins.address, ins.mnemonic, cible, q))
                else:
                    total["ailleurs"] += 1
                    q = struct.unpack_from("<Q", d, r2o(cible))[0] if r2o(cible) else -1
                    sites_ailleurs.append((ins.address, ins.mnemonic, cible, q))

print(f"sites d'appel indirects : {total['nouvelle']} → NOUVELLE IAT (0x3100) · "
      f"{total['vieille']} → VIEILLES PLAGES VIDÉES !! · {total['ailleurs']} → ailleurs")
print()
if sites_vieilles:
    print("=== LES SITES ENCORE SUR LES VIEILLES PLAGES (le défaut nommé ?) ===")
    for (adr, mn, cible, q) in sites_vieilles:
        print(f"  {adr:#06x}  {mn} [{cible:#06x}]  (contenu du slot : {q:#x})")
if sites_ailleurs:
    print("=== LES SITES AILLEURS (à vérifier) ===")
    for (adr, mn, cible, q) in sites_ailleurs[:30]:
        nomf = carte_iat.get(cible, "?")
        print(f"  {adr:#06x}  {mn} [{cible:#06x}] = {nomf} (contenu : {q:#x})")
