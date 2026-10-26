#!/usr/bin/env python3
"""debug_s512_rondes.py — trace ronde par ronde de av-02 contre modèle Python.

Hook sur le « inc r15 » de la boucle .tour (3e occurrence d'inc r15 dans
av-02) : enregistre (a=rax, e=rsi) après chaque ronde ; le modèle Python
calculé indépendamment donne les valeurs attendues — la PREMIÈRE ronde
divergente localise le défaut (W, K, rotations, Ch/Maj ou chaînage).
"""
import struct
import sys

import capstone
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RDI, UC_X86_REG_RSI,
                               UC_X86_REG_RSP, UC_X86_REG_R15)

sys.path.insert(0, "/home/z/my-project/triade/m7")
import layout as L

IMG = open(sys.argv[1] if len(sys.argv) > 1
           else "/home/z/my-project/triade/m7/sceau", "rb").read()
BASE, PILE, CTX = L.IMAGE_BASE, 0x7ffe0000, L.IMAGE_BASE + 0x4000
SENT = 0xfeedfacefeedface

# --- adresse du « inc r15 » de .tour (3e occurrence dans le slot av-02) ------
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
code_slot = IMG[L.A_COMPRIMER:L.A_COMPRIMER + 0x400]
incs = [i.address for i in cs.disasm(code_slot, L.A_COMPRIMER)
        if i.mnemonic == "inc" and i.op_str == "r15"]
assert len(incs) == 3, f"attendu 3 inc r15, trouvé {len(incs)}"
AD_INC_TOUR = BASE + incs[2]
print(f"[harnais] inc r15 de .tour @ {AD_INC_TOUR:#x} (RVA {incs[2]:#x})")

# --- modèle Python complet (rondes par rondes) --------------------------------
K = L.K512
bloc = bytes([0x80]) + bytes(111) + struct.pack(">QQ", 0, 0)   # bloc du vide
W = list(struct.unpack("<16Q", bloc))
M = (1 << 64) - 1
for i in range(16, 80):
    x, y = W[i - 15], W[i - 2]
    s0 = ((x >> 1) | (x << 63)) ^ ((x >> 8) | (x << 56)) ^ (x >> 7)
    s1 = ((y >> 19) | (y << 45)) ^ ((y >> 61) | (y << 3)) ^ (y >> 6)
    W.append((W[i - 16] + s0 + W[i - 7] + s1) & M)
H0 = [0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b,
      0xa54ff53a5f1d36f1, 0x510e527fade682d1, 0x9b05688c2b3e6c1f,
      0x1f83d9abfb41bd6b, 0x5be0cd19137e2179]
a, b_, c, d, e, f, g, h = H0
attendus = []
for j in range(80):
    S1 = ((e >> 14) | (e << 50)) ^ ((e >> 18) | (e << 46)) ^ ((e >> 41) | (e << 23))
    ch = (e & f) ^ ((~e) & g)
    t1 = (h + S1 + ch + K[j] + W[j]) & M
    S0 = ((a >> 28) | (a << 36)) ^ ((a >> 34) | (a << 30)) ^ ((a >> 39) | (a << 25))
    maj = (a & b_) ^ (a & c) ^ (b_ & c)
    t2 = (S0 + maj) & M
    h, g, f = g, f, e
    e = (d + t1) & M
    d, c, b_ = c, b_, a
    a = (t1 + t2) & M
    attendus.append((a, e))

# --- exécution Unicorn avec trace ---------------------------------------------
uc = Uc(UC_ARCH_X86, UC_MODE_64)
uc.mem_map(BASE, 0x4000)
uc.mem_map(PILE, 0x2000)
uc.mem_map(BASE + 0x4000, 0x12000)
uc.mem_write(BASE, IMG)

uc.reg_write(UC_X86_REG_RDI, CTX)
uc.reg_write(UC_X86_REG_RSP, PILE + 0x1000 - 8)
uc.mem_write(PILE + 0x1000 - 8, struct.pack("<Q", SENT))
uc.emu_start(BASE + L.A_INIT, SENT, count=200)
uc.mem_write(CTX + L.CTX_TAMPON, bloc)

trace: list[tuple[int, int, int]] = []


def crochet(uc_, adresse, taille, donnees):
    trace.append((uc_.reg_read(UC_X86_REG_R15),
                  uc_.reg_read(UC_X86_REG_RAX),
                  uc_.reg_read(UC_X86_REG_RSI)))


uc.hook_add(UC_HOOK_CODE, crochet, begin=AD_INC_TOUR, end=AD_INC_TOUR)
uc.reg_write(UC_X86_REG_RDI, CTX)
uc.reg_write(UC_X86_REG_RSP, PILE + 0x1000 - 8)
uc.mem_write(PILE + 0x1000 - 8, struct.pack("<Q", SENT))
uc.emu_start(BASE + L.A_COMPRIMER, SENT, count=200000)

print(f"[harnais] {len(trace)} rondes tracées (attendu 80)")
if len(trace) != 80:
    print("    NB: la trace s'arrête tôt — boucle cassée ?")

# --- comparaison ---------------------------------------------------------------
def faute(n):
    for i, (r15, a, e) in enumerate(trace[:n]):
        ea, ee = attendus[i]
        if a != ea or e != ee:
            return i, (r15, a, e), (i, ea, ee)
    return None


res = faute(len(trace))
if res is None:
    print("[verdict] toutes les rondes tracées sont EXACTES — le défaut est "
          "après la boucle (chaînage final ?)")
else:
    i, (r15, a, e), (_, ea, ee) = res
    print(f"[verdict] PREMIÈRE ronde divergente : {i}")
    print(f"    ronde {i} : r15={r15} a={a:#x} e={e:#x}")
    print(f"    attendu   : a={ea:#x} e={ee:#x}")
    # diagnostic W : si la ronde 0 est déjà fausse, comparer W[0..15] et W[16]
    if i == 0:
        print("    la ronde 0 n'utilise que H0, K[0], W[0] et les rotations")
        print("    K[0] =", hex(K[0]), " W[0] =", hex(W[0]))
