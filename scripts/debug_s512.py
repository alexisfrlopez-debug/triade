#!/usr/bin/env python3
"""debug_s512.py — Harnais de diagnostic SHA-512 sceau (miroir debug hachoir).

Exécute init -> comprimer(bloc connu) sous Unicorn et compare H[8] après
chaque étape contre les valeurs attendues. Pour le message VIDE : la
compression unique produit directement le digest final cf83e135… — le
premier H divergent localise la ronde fausse.
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RDI, UC_X86_REG_RSP,
                               UC_X86_REG_RSI, UC_X86_REG_RDX)

sys.path.insert(0, "/home/z/my-project/triade/m7")
import layout as L

IMG = open("/home/z/my-project/triade/m7/sceau", "rb").read() if len(sys.argv) < 2 \
    else open(sys.argv[1], "rb").read()

BASE = L.IMAGE_BASE
PILE = 0x7ffe0000
CTX = BASE + 0x4000          # .bss


def lancer():
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    uc.mem_map(BASE, 0x4000)
    uc.mem_map(PILE, 0x2000)
    uc.mem_map(BASE + 0x4000, 0x12000)
    uc.mem_write(BASE, IMG)
    return uc


SENT = 0xfeedfacefeedface


def _pile(uc):
    uc.reg_write(UC_X86_REG_RSP, PILE + 0x1000 - 8)
    uc.mem_write(PILE + 0x1000 - 8, struct.pack("<Q", SENT))


def h(uc):
    return list(struct.unpack_from("<8Q", uc.mem_read(CTX, 64)))


def run_init(uc):
    uc.reg_write(UC_X86_REG_RDI, CTX)
    _pile(uc)
    uc.emu_start(BASE + L.A_INIT, SENT, count=200)


def run_comprimer(uc):
    uc.reg_write(UC_X86_REG_RDI, CTX)
    _pile(uc)
    uc.emu_start(BASE + L.A_COMPRIMER, SENT, count=200000)


# --- étape 1 : init ---------------------------------------------------------
uc = lancer()
run_init(uc)
attendu_init = [0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b,
                0xa54ff53a5f1d36f1, 0x510e527fade682d1, 0x9b05688c2b3e6c1f,
                0x1f83d9abfb41bd6b, 0x5be0cd19137e2179]
ok = h(uc) == attendu_init
print(f"[1] init : H == constantes FIPS : {'OK' if ok else 'FAUX'}")
if not ok:
    for i, (a, b) in enumerate(zip(h(uc), attendu_init)):
        if a != b:
            print(f"    H[{i}] = {a:#018x} attendu {b:#018x}")
    sys.exit(1)

# --- étape 2 : comprimer le bloc du message vide ----------------------------
# bloc : 0x80 puis 111 zéros puis longueur 128 bits BE (0) → digest cf83e135…
bloc = bytes([0x80]) + bytes(111) + struct.pack(">QQ", 0, 0)
uc.mem_write(CTX + L.CTX_TAMPON, bloc)
uc.mem_write(CTX + L.CTX_TAMPON + 128, b"\xcc" * 16)   # sentinèle (pas lu)
run_comprimer(uc)
attendu_final = [int.from_bytes(bytes.fromhex(x), "big") for x in (
    "cf83e1357eefb8bd", "f1542850d66d8007", "d620e4050b5715dc",
    "83f4a921d36ce9ce", "47d0d13c5d85f2b0", "ff8318d2877eec2f",
    "63b931bd47417a81", "a538327af927da3e")]
obtenu = h(uc)
print(f"[2] comprimer(bloc vide) : H == digest SHA-512(vide) : "
      f"{'OK' if obtenu == attendu_final else 'FAUX'}")
for i, (a, b) in enumerate(zip(obtenu, attendu_final)):
    marque = "  " if a == b else "≠ "
    print(f"    {marque}H[{i}] = {a:#018x}  attendu {b:#018x}")

# --- étape 2bis : débogage ronde par ronde (a..h après 1re ronde) ----------
# Recalcul Python de la première ronde sur le bloc vide :
K = L.K512
W = list(struct.unpack("<16Q", bloc))
for i in range(16, 80):
    s0 = ((W[i-15] >> 1) | (W[i-15] << 63)) ^ ((W[i-15] >> 8) | (W[i-15] << 56)) ^ (W[i-15] >> 7)
    s1 = ((W[i-2] >> 19) | (W[i-2] << 45)) ^ ((W[i-2] >> 61) | (W[i-2] << 3)) ^ (W[i-2] >> 6)
    W.append((W[i-16] + s0 + W[i-7] + s1) & 0xFFFFFFFFFFFFFFFF)
a, b_, c, d, e, f, g, hh = attendu_init
S1 = (((e >> 14) | (e << 50)) ^ ((e >> 18) | (e << 46)) ^ ((e >> 41) | (e << 23)))
ch = (e & f) ^ ((~e) & g)
t1 = (hh + S1 + ch + K[0] + W[0]) & 0xFFFFFFFFFFFFFFFF
S0 = (((a >> 28) | (a << 36)) ^ ((a >> 34) | (a << 30)) ^ ((a >> 39) | (a << 25)))
maj = (a & b_) ^ (a & c) ^ (b_ & c)
t2 = (S0 + maj) & 0xFFFFFFFFFFFFFFFF
print(f"[3] référence ronde 1 : T1={t1:#x} T2={t2:#x} "
      f"a'={(t1+t2)&0xFFFFFFFFFFFFFFFF:#x} e'={(d+t1)&0xFFFFFFFFFFFFFFFF:#x}")
