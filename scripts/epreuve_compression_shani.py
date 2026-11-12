#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/epreuve_compression_shani.py — L'ÉPREUVE ENTIÈRE DE LA COMPRESSION
SHA-NI À LA MAIN (la suite de experience_semantique_shani.py) : MA PROPRE
structure — pas un octet copié du compilateur, la structure DÉRIVÉE des
sémantiques épinglées — confrontée aux vecteurs FIPS 180-4 § 6.3.1 et à un
corpus aléatoire recoupé à hashlib.

LA STRUCTURE ÉPROUVÉE (celle que portera la notation shani-02) :
  - l'état en ping-pong xmm1/xmm2, la mise en page (F,E,B,A)/(H,G,D,C)
    épinglée par le compilateur-oracle puis RE-DÉRIVÉE ici à la main ;
  - le cur (W+K) TOUJOURS en xmm0 (l'opérande implicite de sha256rnds2) —
    les registres de groupes JAMAIS additionnés de K (pas de conflit
    brut/cur : le budget de 6 volatils + 2 sauvés tient) ;
  - les groupes A/B/C/D = xmm3..6, le grattoir = xmm7 (xmm6/7 sauvés sur
    la pile — le contrat msx64 honoré : XMM6-15 non volatils) ;
  - le cycle de quatre phases : msg1(oldest, next) AU MOMENT de la phase
    (le brut consommé juste après son cur), le W[t-7] par palignr sur une
    COPIE du plus récent, msg2 chaîné, les 16 phases DÉROULÉES (aucune
    rotation de registres — la notation est explicite) ;
  - le masque BE = [3,2,1,0,7,6,5,4,11,10,9,8,15,14,13,12] (chaque dword
    renversé) — DÉFINI ICI et jugé par les vecteurs.

Usage : python3 scripts/epreuve_compression_shani.py
"""

from __future__ import annotations

import ctypes
import hashlib
import mmap
import os
import random
import struct
import sys

from keystone import Ks, KS_ARCH_X86, KS_MODE_64

KS = Ks(KS_ARCH_X86, KS_MODE_64)
MASK32 = 0xFFFFFFFF

K = [int(h, 16) for h in """
428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967
27b70a85 2e1b2138 4d2c6dfc 53380d13 650a7354 766a0abb 81c2c92e 92722c85
a2bfe8a1 a81a664b c24b8b70 c76c51a3 d192e819 d6990624 f40e3585 106aa070
19a4c116 1e376c08 2748774c 34b0bcb5 391c0cb3 4ed8aa4a 5b9cca4f 682e6ff3
748f82ee 78a5636f 84c87814 8cc70208 90befffa a4506ceb bef9a3f7 c67178f2
""".split()]

H0 = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]

# Les vecteurs FIPS 180-4 § 6.3.1 (le doré — les messages EXACTS du standard)
VECTEURS_FIPS = [
    ("le vide", b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("« abc »", b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
    ("les 448 bits",
     b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
     "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
    ("les 896 bits",
     b"abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmno"
     b"ijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu",
     "cf5b16a778af8380036ce59e7b0492370b249b11e8f07a51afac45037afee9d1"),
]


def ror(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK32


def s0(x):
    return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)


def s1(x):
    return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)


def reference_compression(h: list, bloc: bytes) -> list:
    """H' = la compression FIPS d'un bloc (le juge Python pur)."""
    w = list(struct.unpack(">16I", bloc))
    for t in range(16, 64):
        w.append((w[t - 16] + s0(w[t - 15]) + w[t - 7] + s1(w[t - 2])) & MASK32)
    a, b, c, d, e, f, g, hh = h
    for t in range(64):
        t1 = (hh + (ror(e, 6) ^ ror(e, 11) ^ ror(e, 25))
              + ((e & f) ^ (~e & g)) + K[t] + w[t]) & MASK32
        t2 = ((ror(a, 2) ^ ror(a, 13) ^ ror(a, 22))
              + ((a & b) ^ (a & c) ^ (b & c))) & MASK32
        hh, g, f, e, d, c, b, a = g, f, e, (d + t1) & MASK32, c, b, a, (t1 + t2) & MASK32
    return [(x + y) & MASK32 for x, y in zip((a, b, c, d, e, f, g, hh), h)]


# --- LA COMPRESSION À LA MAIN (la structure de la future notation) ---------------

def asm_phases(kbase: int) -> str:
    """Les 16 phases déroulées. A=xmm3 B=xmm4 C=xmm5 D=xmm6, grattoir=xmm7,
    cur=xmm0, état ping-pong xmm1/xmm2 (rnds2 dst=ST1 puis dst=ST2).
    Phase g : cur = K[g] + groupe_g ; 2 rnds2 ; si g+4 ≤ 15 : le calendrier
    du groupe g+4 (msg1 sur le mourant, palignr-copie, paddd, msg2).
    Les adresses absolues précalculées (keystone n'additionne pas deux
    immédiats — l'arithmétique vit ici, une fois pour toutes)."""
    lignes = []
    for g in range(16):
        # les noms des registres de groupes par phase (cycle de 4)
        noms = ["A", "B", "C", "D"]
        vieux = noms[g % 4]          # le groupe g (le mourant de cette phase)
        suivant = noms[(g + 1) % 4]  # le groupe g+1
        deux = noms[(g + 2) % 4]     # le groupe g+2
        trois = noms[(g + 3) % 4]    # le groupe g+3 (le plus récent)
        reg = {"A": "xmm3", "B": "xmm4", "C": "xmm5", "D": "xmm6"}
        r_v, r_s, r_2, r_3 = reg[vieux], reg[suivant], reg[deux], reg[trois]
        lignes.append(f"; --- phase {g} (rounds {4*g}-{4*g+3}) ---")
        lignes.append(f"movdqa xmm0, [{hex(kbase + 16*g)}]")
        lignes.append(f"paddd xmm0, {r_v}")
        lignes.append("sha256rnds2 xmm1, xmm2")
        lignes.append("pshufd xmm0, xmm0, 0x0e")
        lignes.append("sha256rnds2 xmm2, xmm1")
        if g + 4 <= 15:
            lignes.append(f"sha256msg1 {r_v}, {r_s}")
            lignes.append(f"movdqa xmm7, {r_3}")
            lignes.append(f"palignr xmm7, {r_2}, 4")
            lignes.append(f"paddd {r_v}, xmm7")
            lignes.append(f"sha256msg2 {r_v}, {r_3}")
    return "\n".join(lignes)


ASM_COMPRESSION = """
; LE GABARIT DE LA COMPRESSION (epreuve native, appelee en SysV :
; rdi = le contexte (H[8] u32 LE), rsi = le bloc de 64 o)
push rbx
push rbp
push r12
push r13
push r14
push r15
push rdi
push rsi
sub rsp, 0x48
movdqa [rsp], xmm6
movdqa [rsp + 0x10], xmm7

; L'ETAT : la mise en page de travail (F,E,B,A)/(H,G,D,C)
movdqu xmm3, [rdi]
movdqu xmm1, [rdi + 16]
pshufd xmm4, xmm3, 0xb1
pshufd xmm5, xmm1, 0xb1
punpcklqdq xmm5, xmm4
movdqa xmm2, xmm5
pshufd xmm3, xmm3, 0x1b
pshufd xmm1, xmm1, 0x1b
punpcklqdq xmm1, xmm3
movdqa [rsp + 0x20], xmm2
movdqa [rsp + 0x30], xmm1

; LE BLOC : quatre groupes BE par le masque
movdqu xmm3, [rsi]
movdqu xmm4, [rsi + 16]
movdqu xmm5, [rsi + 32]
movdqu xmm6, [rsi + 48]
pshufb xmm3, [MASQUE]
pshufb xmm4, [MASQUE]
pshufb xmm5, [MASQUE]
pshufb xmm6, [MASQUE]

{__PHASES__}

; LA SORTIE : l'etat final + l'initial, remis en (A..H)
movdqa xmm0, [rsp + 0x20]
paddd xmm2, xmm0
movdqa xmm0, [rsp + 0x30]
paddd xmm1, xmm0
pshufd xmm0, xmm2, 0x1b
pshufd xmm2, xmm1, 0x1b
movdqa xmm1, xmm0
punpckhqdq xmm0, xmm2
punpcklqdq xmm1, xmm2
movdqu [rdi], xmm1
movdqu [rdi + 16], xmm0

movdqa xmm6, [rsp]
movdqa xmm7, [rsp + 0x10]
add rsp, 0x48
pop rsi
pop rdi
pop r15
pop r14
pop r13
pop r12
pop rbp
pop rbx
ret
"""


class Natif:
    def __init__(self):
        self.mem = mmap.mmap(-1, 0x20000,
                             prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
        self.base = ctypes.addressof(ctypes.c_char.from_buffer(self.mem))
        self.cur = 0
        self.fn = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)

    def poser(self, asm: str, symboles: dict | None = None) -> int:
        while self.cur % 16:
            self.cur += 1
        adr = self.base + self.cur
        # les commentaires retirés AVANT keystone (le miroir de
        # B4.assembler_bloc — keystone n'évalue jamais les lignes « ; »)
        corps = "\n".join(l.split(";")[0].strip()
                          for l in asm.split("\n"))
        corps = "\n".join(l for l in corps.split("\n") if l)
        code, _ = KS.asm(corps, adr)
        b = bytes(code)
        self.mem[self.cur:self.cur + len(b)] = b
        self.cur += len(b)
        return adr

    def zone(self, taille=0x1000):
        """Une zone de données 16-alignée dans la page."""
        while self.cur % 16:
            self.cur += 1
        adr = self.base + self.cur
        self.cur += taille
        return adr


def main() -> int:
    print("=== scripts/epreuve_compression_shani.py — LA COMPRESSION ENTIÈRE "
          "À LA MAIN ===")
    natif = Natif()

    # les données : K au plan, le masque BE
    kbase = natif.zone(0x100)
    natif.mem[kbase - natif.base:kbase - natif.base + 256] = \
        struct.pack("<64I", *K)
    masque = natif.zone(16)
    natif.mem[masque - natif.base:masque - natif.base + 16] = \
        bytes([3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12])

    asm = (ASM_COMPRESSION
           .replace("MASQUE", hex(masque))
           .replace("{__PHASES__}", asm_phases(kbase)))
    adr_comp = natif.poser(asm)
    print(f"la compression posée à {adr_comp:#x} "
          f"({natif.cur} octets utilisés)")

    def comprimer(h: list, bloc: bytes) -> list:
        zone = bytearray(0x200)
        struct.pack_into("<8I", zone, 0, *h)
        zone[32:96] = bloc
        ctypes.cast(adr_comp, natif.fn)(
            ctypes.addressof((ctypes.c_char * len(zone)).from_buffer(zone)),
            ctypes.addressof((ctypes.c_char * len(zone)).from_buffer(zone)) + 32)
        return list(struct.unpack_from("<8I", zone, 0))

    # 1. LA COMPRESSION SEULE contre le juge Python pur (100 blocs aléatoires)
    rng = random.Random(20261112)
    ok = True
    for i in range(100):
        h = [rng.getrandbits(32) for _ in range(8)]
        bloc = rng.randbytes(64)
        ref = reference_compression(h, bloc)
        eu = comprimer(h, bloc)
        if eu != ref:
            ok = False
            print(f"  ÉCHEC bloc {i}: H={h} attendu={ref} eu={eu}")
            break
    print(f"1. la compression contre le juge Python : "
          f"{'100/100 VERT' if ok else 'ÉCHEC'}")

    # 2. LE PIPELINE FIPS : padding + compression(s) — les vecteurs dorés
    def condense(message: bytes) -> bytes:
        h = list(H0)
        pad = message + b"\x80"
        pad += b"\x00" * ((56 - len(pad) % 64) % 64)
        pad += struct.pack(">Q", len(message) * 8)
        for i in range(0, len(pad), 64):
            h = comprimer(h, pad[i:i + 64])
        return struct.pack(">8I", *h)

    ok_fips = True
    for nom, message, attendu in VECTEURS_FIPS:
        eu = condense(message).hex()
        py = hashlib.sha256(message).hexdigest()
        bon = eu == attendu == py
        ok_fips &= bon
        print(f"2. FIPS {nom:12} : {'VERT' if bon else 'ÉCHEC'} "
              f"({eu[:16]}…)")
    ok_corpus = True
    for taille in (0, 1, 55, 56, 63, 64, 65, 127, 128, 129, 1000, 4096):
        message = rng.randbytes(taille)
        ok_corpus &= condense(message) == hashlib.sha256(message).digest()
    print(f"3. le corpus aléatoire aux bords (0..4096) : "
          f"{'VERT' if ok_corpus else 'ÉCHEC'}")

    if ok and ok_fips and ok_corpus:
        print("VERDICT : LA STRUCTURE À LA MAIN EST JUSTE — la notation "
              "shani-02 peut naître sur cette structure éprouvée")
        return 0
    print("VERDICT : ÉCHEC — la structure reprend")
    return 1


if __name__ == "__main__":
    sys.exit(main())
