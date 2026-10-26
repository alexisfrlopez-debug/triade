#!/usr/bin/env python3
"""debug_ah.py — Diagnostique la chaîne SHA-256 d'hachoir bloc par bloc."""
import sys

sys.path.insert(0, "/home/z/my-project/triade/m6")
import layout as L
import build_ah as B

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RAX, UC_X86_REG_RDI,
                               UC_X86_REG_RSI, UC_X86_REG_RDX, UC_X86_REG_RBX,
                               UC_X86_REG_RBP, UC_X86_REG_R12, UC_X86_REG_R13,
                               UC_X86_REG_R14, UC_X86_REG_R15)

IMG = B.composer_elf({bid: code for bid, code in
                      {b[0]: None for b in L.BLOCS_AH}.items()} if False else None) \
    if False else None

# assembler et composer proprement
blocs, _, code, _ = B.assembler_tout()
img = B.composer_elf(code)

BASE = L.IMAGE_BASE
CTX = BASE + 0x3000          # .bss mappé manuellement
PILE = 0x7fff0000
SENT = 0xdeadbeefdeadbeef

uc = Uc(UC_ARCH_X86, UC_MODE_64)
uc.mem_map(BASE, 0x15000)             # image RX + .bss RW (fin 0x14300)
uc.mem_map(PILE, 0x10000)
uc.mem_write(BASE, img)

CTX_RVA = 0x3000
ctx = BASE + CTX_RVA

def appeler(rva, rdi=0, rsi=0, rdx=0):
    for reg, val in ((UC_X86_REG_RDI, rdi), (UC_X86_REG_RSI, rsi),
                     (UC_X86_REG_RDX, rdx)):
        uc.reg_write(reg, val)
    uc.reg_write(UC_X86_REG_RSP, PILE + 0x8000 - 8)
    uc.mem_write(PILE + 0x8000 - 8, SENT.to_bytes(8, "little"))
    for reg in (UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_R12,
                UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15):
        uc.reg_write(reg, 0x5a5a5a5a5a5a5a5a)
    from unicorn import UcError
    try:
        uc.emu_start(BASE + rva, SENT, count=5_000_000)   # stop À la sentinelle
    except UcError as e:
        from unicorn.x86_const import UC_X86_REG_RIP
        rip = uc.reg_read(UC_X86_REG_RIP)
        print(f"CRASH {e} rip={rip:#x} (RVA {rip - BASE:#x})")
        try:
            print("octets:", uc.mem_read(rip, 8).hex())
        except UcError:
            print("rip hors mémoire mappée")
        raise
    return uc.reg_read(UC_X86_REG_RAX)

def dump_ctx(label):
    brut = bytes(uc.mem_read(ctx, 112))
    h = [int.from_bytes(brut[4 * i:4 * i + 4], "little") for i in range(8)]
    print(f"{label}: H = " + " ".join(f"{x:08x}" for x in h))
    print(f"{'':{len(label)}}  remplissage={int.from_bytes(brut[96:100], 'little')} "
          f"total={int.from_bytes(brut[104:112], 'little')}")
    return h

# --- test 1 : init + compression du bloc de bourrage de l'entrée vide ---
appeler(L.A_INIT, ctx)
h0 = dump_ctx("après init")

# bloc manuel : 0x80 + zéros + longueur 0 (vide)
bloc = bytes([0x80]) + b"\x00" * 55 + (0).to_bytes(8, "big")
uc.mem_write(ctx + 32, bloc)
uc.mem_write(ctx + 96, (64).to_bytes(4, "little"))
appeler(L.A_COMPRIMER, ctx)
h1 = dump_ctx("après compression (vide attendu e3b0c442 98fc1c14 9afbf4c8 "
              "996fb924 27ae41e4 649b934c a495991b 7852b855)")

# --- test 2 : compression du bloc "abc"+bourrage (FIPS § B1 intermédiaire ?) ---
appeler(L.A_INIT, ctx)
bloc_abc = b"abc" + bytes([0x80]) + b"\x00" * 52 + (24).to_bytes(8, "big")
uc.mem_write(ctx + 32, bloc_abc)
uc.mem_write(ctx + 96, (64).to_bytes(4, "little"))
appeler(L.A_COMPRIMER, ctx)
dump_ctx("après compression abc (attendu ba7816bf 8f01cfea 414140de "
         "5dae2223 b00361a3 96177a9c b410ff61 f20015ad)")
