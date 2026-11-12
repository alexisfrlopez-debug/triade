#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/experience_semantique_shani.py — L'ÉPREUVE EMPIRIQUE DES SÉMANTIQUES
SHA-NI (le paquet 6/6, l'instruction lfh49a1xf) : AVANT d'écrire la notation
de la variante, les sémantiques EXACTES de sha256rnds2 / sha256msg1 /
sha256msg2 sont ÉPINGLÉES PAR LE CODE sur le CPU SHA-NI natif du laboratoire
— chaque hypothèse confrontée à la référence FIPS 180-4 calculée en Python
pur (le juge est le code, jamais la documentation lue sur parole).

Les hypothèses testées (l'espace est nommé, chaque branche tranchée par
l'exécution) :
  RNDS2 — l'opérande implicite : RAX[31:0] et RAX[63:32] portent-ils les
          sommes (W[t]+K[t], W[t+1]+K[t+1]) ? (contre : la paire K seule) ;
          l'ordre des opérandes : dst = (C,D,G,H), src = (A,B,E,F), le
          résultat ABEF_{t+2} ÉCRIT dst, src devient de fait CDGH_{t+2}
          (contre : l'ordre inverse) ;
  MSG1  — dst += s0([dst[1], dst[2], dst[3], src[0]]) (l'argument sigma0 par
          la fenêtre glissante d'un dword — contre : src pris entier) ;
  MSG2  — dst += s1([src[2], src[3], dst[0], dst[1]]) (l'argument sigma1
          chevauchant les groupes — contre : les autres fenêtres) ;
  PUIS   — la compression ENTIÈRE (16 mots préchargés, 48 étendus, 64 tours)
          confrontée aux vecteurs FIPS 180-4 § 6.3.1 sur le chemin natif.

LA MÉTHODE : keystone assemble l'hypothèse (jamais un octet gravé de tête),
mmap exécutable la reçoit, l'appel se fait par ctypes — l'instrument est le
labo, la référence est hashlib/FIPS en Python pur. Aucune pièce scellée
n'est touchée (l'épreuve vit en mémoire anonyme).

Usage : python3 scripts/experience_semantique_shani.py
"""

from __future__ import annotations

import ctypes
import hashlib
import mmap
import os
import struct
import sys

from keystone import Ks, KS_ARCH_X86, KS_MODE_64

KS = Ks(KS_ARCH_X86, KS_MODE_64)
MASK32 = 0xFFFFFFFF


# --- la référence FIPS en Python pur (le juge) -------------------------------------

def ror(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK32


def s0(x: int) -> int:          # sigma0 du calendrier (FIPS § 6.2.2)
    return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)


def s1(x: int) -> int:          # sigma1 du calendrier
    return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)


def S1(x: int) -> int:          # Sigma1 des tours
    return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)


def S0(x: int) -> int:          # Sigma0 des tours
    return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)


def ch(e, f, g):
    return (e & f) ^ (~e & g)


def maj(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


def calendrier(bloc: bytes) -> list[int]:
    """W[0..63] depuis un bloc de 64 o (gros-boutiste), FIPS § 6.2.2."""
    w = list(struct.unpack(">16I", bloc))
    for t in range(16, 64):
        w.append((w[t - 16] + s0(w[t - 15]) + w[t - 7] + s1(w[t - 2])) & MASK32)
    return w


def deux_tours(etat: list[int], w: list[int], k: list[int], t: int):
    """(A..H) → (A..H) après les tours t et t+1 (la référence rnds2)."""
    a, b, c, d, e, f, g, h = etat
    for i in (t, t + 1):
        t1 = (h + S1(e) + ch(e, f, g) + k[i] + w[i]) & MASK32
        t2 = (S0(a) + maj(a, b, c)) & MASK32
        h, g, f, e, d, c, b, a = g, f, e, (d + t1) & MASK32, c, b, a, (t1 + t2) & MASK32
    return [a, b, c, d, e, f, g, h]


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


# --- l'exécuteur natif (mmap exécutable + ctypes) ----------------------------------

class Natif:
    """Une page exécutable : keystone assemble, mmap reçoit, ctypes appelle.
    L'appelé est appelé en SysV (rdi = le pointeur de la zone d'échange)."""

    def __init__(self):
        self.taille = 0x20000
        self.mem = mmap.mmap(-1, self.taille,
                             prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
        self.base = ctypes.addressof(ctypes.c_char.from_buffer(self.mem))
        self.curseur = 0
        self.fn = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p)

    def poser(self, asm: str) -> int:
        """Assemble à l'adresse courante (alignée 16), rend l'adresse."""
        while self.curseur % 16:
            self.curseur += 1
        adr = self.base + self.curseur
        code, _ = KS.asm(asm, adr)
        octets = bytes(code)
        self.mem[self.curseur:self.curseur + len(octets)] = octets
        self.curseur += len(octets)
        return adr

    def appeler(self, adr: int, zone: bytearray) -> None:
        ctypes.cast(adr, self.fn)(ctypes.addressof(
            (ctypes.c_char * len(zone)).from_buffer(zone)))


def u32s(b: bytes) -> list[int]:
    return list(struct.unpack("<4I", b))


def pack_u32s(xs: list[int]) -> bytes:
    return struct.pack("<4I", *[x & MASK32 for x in xs])


# --- l'épreuve 1 : sha256rnds2 ------------------------------------------------------

def epreuve_rnds2(natif: Natif) -> dict:
    """Deux ordres d'opérandes × deux contenus d'implicite — quatre
    hypothèses, une seule doit rendre le nouvel ABEF du Python pur."""
    etat0 = [0x11223344, 0x55667788, 0x99aabbcc, 0xddeeff00,
             0x01020304, 0x05060708, 0x090a0b0c, 0x0d0e0f10]
    w0, w1 = 0xdeadbeef, 0xcafebabe
    ref = deux_tours(etat0, [w0, w1] + [0] * 62, K, 0)
    ref_abef2 = ref[0:2] + ref[4:6]        # (A2, B2, E2, F2)
    ref_cdgh2 = ref[2:4] + ref[6:8]        # (C2, D2, G2, H2)

    resultats = {}
    for nom_ordre, asm_rnds in (
            ("dst=CDGH,src=ABEF", "sha256rnds2 xmm1, xmm0"),
            ("dst=ABEF,src=CDGH", "sha256rnds2 xmm0, xmm1")):
        for nom_implicite, charge in (
                ("rax=(W+K,W+K)", "mov rax, [rdi + 32]"),
                ("rax=(K,K)", "mov rax, [rdi + 40]")):
            asm = f"""
movdqu xmm0, [rdi]
movdqu xmm1, [rdi + 16]
{charge}
{asm_rnds}
movdqu [rdi + 64], xmm0
movdqu [rdi + 80], xmm1
ret
"""
            adr = natif.poser(asm)
            zone = bytearray(128)
            zone[0:16] = pack_u32s([etat0[0], etat0[1], etat0[4], etat0[5]])
            zone[16:32] = pack_u32s([etat0[2], etat0[3], etat0[6], etat0[7]])
            zone[32:40] = struct.pack("<Q", ((w0 + K[0]) & MASK32)
                                      | (((w1 + K[1]) & MASK32) << 32))
            zone[40:48] = struct.pack("<Q", K[0] | (K[1] << 32))
            natif.appeler(adr, zone)
            xmm0_out, xmm1_out = u32s(zone[64:80]), u32s(zone[80:96])
            resultats[(nom_ordre, nom_implicite)] = {
                "xmm0": xmm0_out, "xmm1": xmm1_out,
                "xmm0_est_abef2": xmm0_out == ref_abef2,
                "xmm1_est_abef2": xmm1_out == ref_abef2,
                "xmm0_est_cdgh2": xmm0_out == ref_cdgh2,
                "xmm1_est_cdgh2": xmm1_out == ref_cdgh2,
            }
    return {"reference": {"abef2": ref_abef2, "cdgh2": ref_cdgh2},
            "hypotheses": resultats}


# --- l'épreuve 2 : sha256msg1 -------------------------------------------------------

def epreuve_msg1(natif: Natif) -> dict:
    x = [0x01010101, 0x02020202, 0x03030303, 0x04040404]
    y = [0x0a0a0a0a, 0x0b0b0b0b, 0x0c0c0c0c, 0x0d0d0d0d]
    adr = natif.poser("""
movdqu xmm0, [rdi]
movdqu xmm1, [rdi + 16]
sha256msg1 xmm0, xmm1
movdqu [rdi + 32], xmm0
ret
""")
    zone = bytearray(64)
    zone[0:16] = pack_u32s(x)
    zone[16:32] = pack_u32s(y)
    natif.appeler(adr, zone)
    out = u32s(zone[32:48])
    hypotheses = {
        "fenetre[x1,x2,x3,y0]": [ (x[i] + s0([x[1], x[2], x[3], y[0]][i])) & MASK32
                                  for i in range(4)],
        "src_entier": [(x[i] + s0(y[i])) & MASK32 for i in range(4)],
    }
    return {"sortie": out, "hypotheses": {n: (h, h == out)
                                          for n, h in hypotheses.items()}}


# --- l'épreuve 3 : sha256msg2 -------------------------------------------------------

def epreuve_msg2(natif: Natif) -> dict:
    x = [0x11111111, 0x12121212, 0x13131313, 0x14141414]   # partiel (W[i-7..i-4] déjà ajouté)
    y = [0x21212121, 0x22222222, 0x23232323, 0x24242424]   # W[i-4..i-1]
    adr = natif.poser("""
movdqu xmm0, [rdi]
movdqu xmm1, [rdi + 16]
sha256msg2 xmm0, xmm1
movdqu [rdi + 32], xmm0
ret
""")
    zone = bytearray(64)
    zone[0:16] = pack_u32s(x)
    zone[16:32] = pack_u32s(y)
    natif.appeler(adr, zone)
    out = u32s(zone[32:48])
    hyp = {
        "fenetre[y2,y3,x0,x1]": [(x[i] + s1([y[2], y[3], x[0], x[1]][i])) & MASK32
                                 for i in range(4)],
        "fenetre[y1,y2,y3,x0]": [(x[i] + s1([y[1], y[2], y[3], x[0]][i])) & MASK32
                                 for i in range(4)],
        "fenetre[y3,x0,x1,x2]": [(x[i] + s1([y[3], x[0], x[1], x[2]][i])) & MASK32
                                 for i in range(4)],
    }
    return {"sortie": out, "hypotheses": {n: (h, h == out) for n, h in hyp.items()}}


def main() -> int:
    print("=== scripts/experience_semantique_shani.py — LES SÉMANTIQUES ÉPINGLÉES "
          "PAR LE CODE ===")
    natif = Natif()
    print(f"page exécutable : {natif.base:#x} ({natif.taille} o)")

    print("\n--- ÉPREUVE 1 : sha256rnds2 (quatre hypothèses) ---")
    r1 = epreuve_rnds2(natif)
    for (ordre, implicite), res in r1["hypotheses"].items():
        marques = [k for k in ("xmm0_est_abef2", "xmm1_est_abef2",
                               "xmm0_est_cdgh2", "xmm1_est_cdgh2") if res[k]]
        print(f"  {ordre:20} {implicite:16} → xmm0={res['xmm0']} "
              f"xmm1={res['xmm1']} {marques or 'aucun match'}")
    print(f"  référence ABEF2={r1['reference']['abef2']} "
          f"CDGH2={r1['reference']['cdgh2']}")

    print("\n--- ÉPREUVE 2 : sha256msg1 ---")
    r2 = epreuve_msg1(natif)
    print(f"  sortie = {r2['sortie']}")
    for n, (h, ok) in r2["hypotheses"].items():
        print(f"  {n:24} {'MATCH' if ok else 'non'} {h}")

    print("\n--- ÉPREUVE 3 : sha256msg2 ---")
    r3 = epreuve_msg2(natif)
    print(f"  sortie = {r3['sortie']}")
    for n, (h, ok) in r3["hypotheses"].items():
        print(f"  {n:24} {'MATCH' if ok else 'non'} {h}")

    gagnant = None
    for (ordre, implicite), res in r1["hypotheses"].items():
        if res["xmm1_est_abef2"] and res["xmm0_est_cdgh2"]:
            gagnant = ("dst=CDGH reçoit ABEF2 ; src=ABEF demeure (=CDGH2)",
                       ordre, implicite)
        if res["xmm0_est_abef2"] and res["xmm1_est_cdgh2"]:
            gagnant = ("dst=ABEF reçoit ABEF2 ; src=CDGH demeure", ordre, implicite)
    print(f"\nVERDICT RNDS2 : {gagnant}")
    m1 = [n for n, (h, ok) in r2["hypotheses"].items() if ok]
    m2 = [n for n, (h, ok) in r3["hypotheses"].items() if ok]
    print(f"VERDICT MSG1  : {m1}")
    print(f"VERDICT MSG2  : {m2}")
    if gagnant and m1 and m2:
        print("VERDICT : LES SÉMANTIQUES SONT ÉPINGLÉES — la notation peut naître")
        return 0
    print("VERDICT : ÉCHEC — hypothèses à élargir")
    return 1


if __name__ == "__main__":
    sys.exit(main())
