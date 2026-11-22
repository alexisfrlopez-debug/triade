#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesurer_ghash_agrege.py — LE PILOTE DU COULOIR GHASH AGRÉGÉ QUATRE BLOCS
(h1mz2sr8s, la vague 14) : round-trip, différentielle contre le scellé
chaîné, mutant, repli, la table des puissances DÉRIVÉE par le juge, la
mesure native RDTSCP (GH400 : 25 appels × 4 = 100 multiplications), la
trace-hash temps-constant, la garde du sceau-I avant/après.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import random
import struct
import subprocess
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-ghash-agrege-h1mz2sr8s"
NOTA = ICI / "notation" / "ghash-pclmulqdq-agrege4.asm"
SC17 = REPO / "tls13" / "notation" / "tls13-17-ghash-multiplication.asm"
RVA_COULOIR = 0xF300
SC17_RVA = 0xDFC0
GRAINE = 20261123

import keystone
import capstone
import unicorn

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


# ------------------------------------------------- le juge GHASH (v13) -----
def ghash_juge(NX: int, NY: int) -> int:
    def rev128(v):
        r = 0
        for i in range(128):
            r |= ((v >> (127 - i)) & 1) << i
        return r

    def clmul(a, b):
        r = 0
        while b:
            if b & 1:
                r ^= a
            b >>= 1
            a <<= 1
        return r

    def polymod(t):
        while t.bit_length() > 128:
            k = t.bit_length() - 129
            t ^= ((1 << 128) | 0x87) << k
        return t

    return rev128(polymod(clmul(rev128(NX), rev128(NY))))


def v128(x: int) -> bytes:
    return struct.pack("<QQ", x & 0xFFFFFFFFFFFFFFFF,
                       (x >> 64) & 0xFFFFFFFFFFFFFFFF)


def de128(b: bytes) -> int:
    lo, hi = struct.unpack("<QQ", b)
    return (hi << 64) | lo


# ------------------------------------------------- l'assemblage ------------
def assembler(fichier: pathlib.Path, rva: int):
    lignes = [l.split(";")[0] for l in fichier.read_text(
        encoding="utf-8").splitlines()]
    etiquettes: dict[str, int] = {}
    corps_list = []
    for _ in range(4):
        adr = rva
        corps_list = []
        for l in lignes:
            l = l.strip()
            if not l:
                continue
            if l.endswith(":") and l.startswith("."):
                etiquettes[l[:-1]] = adr
                continue
            corps = l
            for e, a in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
                corps = corps.replace(e, hex(a))
            corps_list.append(corps)
            try:
                c, _ = KS.asm(corps, adr)
                adr += len(bytes(c))
            except Exception:
                adr += 6
    octets = b""
    for corps in corps_list:
        for e, a in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
            corps = corps.replace(e, hex(a))
        c, _ = KS.asm(corps, rva + len(octets))
        octets += bytes(c)
    return octets


def round_trip(octets: bytes, rva: int) -> bool:
    reins = b""
    for ins in CS.disasm(octets, rva):
        c, _ = KS.asm(f"{ins.mnemonic} {ins.op_str}", ins.address)
        reins += bytes(c)
    return reins == octets


# ------------------------------------------------- le banc Unicorn ---------
REG = {"rax": unicorn.x86_const.UC_X86_REG_RAX, "rcx": unicorn.x86_const.UC_X86_REG_RCX,
       "rdx": unicorn.x86_const.UC_X86_REG_RDX, "r8": unicorn.x86_const.UC_X86_REG_R8,
       "r9": unicorn.x86_const.UC_X86_REG_R9, "r10": unicorn.x86_const.UC_X86_REG_R10}


def executer(octets17: bytes, octets_ag: bytes, X: bytes, table: bytes,
             H: bytes, r10: int) -> tuple[bytes, int]:
    """Le couloir agrégé à 0xF300, le scellé chaîné à 0xDFC0 (r10 porte
    le verdict du couloir ; le scellé appelé avec r10=0 — son contrat)."""
    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    uc.mem_map(0xC000, 0x4000)
    uc.mem_map(0x500000, 0x21000)
    uc.mem_map(0x70000, 0x10000)
    uc.mem_write(SC17_RVA, octets17)
    uc.mem_write(RVA_COULOIR, octets_ag)
    uc.mem_write(0x500400, X)
    uc.mem_write(0x500600, table)
    uc.mem_write(0x500A00, H)
    uc.mem_write(0x78000, struct.pack("<Q", 0x60000))
    uc.reg_write(unicorn.x86_const.UC_X86_REG_RSP, 0x78000)
    uc.reg_write(REG["rcx"], 0x500800)
    uc.reg_write(REG["rdx"], 0x500400)
    uc.reg_write(REG["r8"], 0x500600)
    uc.reg_write(REG["r9"], 0x500A00)
    uc.reg_write(REG["r10"], r10)
    uc.emu_start(RVA_COULOIR, 0x60000)
    z = uc.mem_read(0x500800, 16)
    return bytes(z), uc.reg_read(REG["rax"])


def chaine_seallee(uc17: bytes, X: bytes, H: bytes) -> bytes:
    """La référence : QUATRE appels chaînés au scellé (l'ABI du scellé)."""
    import unicorn as u2
    uc = u2.Uc(u2.UC_ARCH_X86, u2.UC_MODE_64)
    uc.mem_map(0xC000, 0x4000)
    uc.mem_map(0x500000, 0x21000)
    uc.mem_map(0x70000, 0x10000)
    uc.mem_write(SC17_RVA, uc17)
    uc.mem_write(0x500A00, H)
    y = X[0:16]
    for k in range(4):
        uc.mem_write(0x500400, y)
        uc.mem_write(0x78000, struct.pack("<Q", 0x60000))
        uc.reg_write(u2.x86_const.UC_X86_REG_RSP, 0x78000)
        uc.reg_write(REG["rcx"], 0x500800)
        uc.reg_write(REG["rdx"], 0x500400)
        uc.reg_write(REG["r8"], 0x500A00)
        uc.reg_write(REG["r10"], 0)
        uc.emu_start(SC17_RVA, 0x60000)
        y = bytes(uc.mem_read(0x500800, 16))
        if k < 3:
            xk = X[16 * (k + 1):16 * (k + 2)]
            y = bytes(a ^ b for a, b in zip(y, xk))
    return y


# ------------------------------------------------- la table des puissances -
OCTETS17_G = None

def _sealed(X: int, Y: int) -> int:
    """Le scellé tls13-17 en Unicorn (le produit PAR BLOC du scellé)."""
    import unicorn as u2
    uc = u2.Uc(u2.UC_ARCH_X86, u2.UC_MODE_64)
    uc.mem_map(0xC000, 0x4000)
    uc.mem_map(0x500000, 0x21000)
    uc.mem_map(0x70000, 0x10000)
    uc.mem_write(SC17_RVA, OCTETS17_G)
    uc.mem_write(0x500400, v128(X))
    uc.mem_write(0x500A00, v128(Y))
    uc.mem_write(0x78000, struct.pack("<Q", 0x60000))
    uc.reg_write(u2.x86_const.UC_X86_REG_RSP, 0x78000)
    uc.reg_write(REG["rcx"], 0x500800)
    uc.reg_write(REG["rdx"], 0x500400)
    uc.reg_write(REG["r8"], 0x500A00)
    uc.reg_write(REG["r10"], 0)
    uc.emu_start(SC17_RVA, 0x60000)
    lo, hi = struct.unpack("<QQ", uc.mem_read(0x500800, 16))
    return (hi << 64) | lo


def puissances(H: int) -> bytes:
    """[H⁴ ‖ H³ ‖ H² ‖ H] DÉRIVÉES PAR LE SCELLÉ LUI-MÊME (trois appels
    chaînés du scellé sur H — l'associativité de la multiplication de
    corps : T_k = H⊗T_(k-1), jamais devinées, le domaine du scellé)."""
    h2 = _sealed(H, H)
    h3 = _sealed(h2, H)
    h4 = _sealed(h3, H)
    return v128(h4) + v128(h3) + v128(h2) + v128(H)


def trace_hash(octets17, octets_ag, classe: str) -> str:
    """L'empreinte de trace par classe (60 mesures — les VALEURS JAMAIS)."""
    empreintes = set()
    for i in range(60):
        if classe == "aleatoire":
            rng = random.Random(1000 + i)
            X = rng.getrandbits(512)
            H = rng.getrandbits(128)
        else:
            X = (i << 8) | 0xE1
            H = 0xE1 << 120
        table = puissances(H)
        uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
        uc.mem_map(0xC000, 0x4000)
        uc.mem_map(0x500000, 0x21000)
        uc.mem_map(0x70000, 0x10000)
        uc.mem_write(SC17_RVA, octets17)
        uc.mem_write(RVA_COULOIR, octets_ag)
        uc.mem_write(0x500400, X.to_bytes(64, "little"))
        uc.mem_write(0x500600, table)
        uc.mem_write(0x500A00, H.to_bytes(16, "little"))
        trace = []
        uc.hook_add(unicorn.UC_HOOK_CODE,
                    lambda u, a, t, _: trace.append((a, t)))
        uc.mem_write(0x78000, struct.pack("<Q", 0x60000))
        uc.reg_write(unicorn.x86_const.UC_X86_REG_RSP, 0x78000)
        uc.reg_write(REG["rcx"], 0x500800)
        uc.reg_write(REG["rdx"], 0x500400)
        uc.reg_write(REG["r8"], 0x500600)
        uc.reg_write(REG["r9"], 0x500A00)
        uc.reg_write(REG["r10"], 1)
        uc.emu_start(RVA_COULOIR, 0x60000)
        empreintes.add(hashlib.sha256(json.dumps(trace).encode()).hexdigest())
    return f"{len(empreintes)} empreinte(s) sur 60"


def garde_sceau(quand: str) -> dict:
    sys.path.insert(0, str(REPO / "v06"))
    import sceau_I
    ok = sceau_I.verifier(silencieux=True) == 0   # 0 arbre en échec = 14/14 VERTS
    pieces = {n: hashlib.sha256((REPO / c).read_bytes()).hexdigest()[:16]
              for n, c in [("proxy.exe", "tls13/proxy.exe"),
                           ("loupe.exe", "loupe/loupe.exe")]}
    print(f"[garde du sceau {quand}] {'14/14 VERT' if ok else 'ROUGE'} ; "
          f"pièces {pieces}")
    return {"ok": ok, "pieces": pieces}


def main() -> int:
    print("=== LA MESURE DU COULOIR GHASH AGRÉGÉ QUATRE BLOCS (h1mz2sr8s) ===")
    garde_avant = garde_sceau("avant")
    octets17 = assembler(SC17, SC17_RVA)
    octets_ag = assembler(NOTA, RVA_COULOIR)
    globals()["OCTETS17_G"] = octets17
    print(f"[1] assemblage : scellé {len(octets17)} o, couloir "
          f"{len(octets_ag)} o ({RVA_COULOIR:#x})")
    rt = round_trip(octets_ag, RVA_COULOIR)
    print(f"[1] round-trip keystone==capstone==keystone : "
          f"{'VERT' if rt else 'ROUGE'}")

    # [2] LA DIFFÉRENTIELLE 0/320 : le couloir (r10=1) contre QUATRE appels
    #     chaînés au scellé (0xDFC0) — 256 aléatoires + 64 structurés
    rng = random.Random(GRAINE)
    ecarts = 0
    vecteurs = []
    for i in range(256):
        X = rng.getrandbits(512)
        H = rng.getrandbits(128)
        vecteurs.append((X, H))
    for i in range(64):
        X = (0xE1 << 504) | i
        H = (0xE1 << 120) | i
        vecteurs.append((X, H))
    for n, (X, H) in enumerate(vecteurs):
        xb = X.to_bytes(64, "little")
        hb = H.to_bytes(16, "little")
        table = puissances(H)
        z_ref = chaine_seallee(octets17, xb, hb)
        z, rax = executer(octets17, octets_ag, xb, table, hb, 1)
        if z != z_ref or rax != 0:
            ecarts += 1
            if ecarts == 1:
                print(f"  PREMIER ÉCART au vecteur {n} : {z.hex()} vs "
                      f"{z_ref.hex()}")
    print(f"[2] différentielle {320 - ecarts}/320 — "
          f"{'ZÉRO écart' if ecarts == 0 else str(ecarts) + ' ÉCARTS'}")

    # [3] LE MUTANT : l'imm8 du premier pclmulqdq muté — attrapé au premier
    octets_m = bytearray(octets_ag)
    pos = None
    for ins in CS.disasm(bytes(octets_m), RVA_COULOIR):
        if ins.mnemonic == "pclmulqdq":
            pos = ins.address - RVA_COULOIR + ins.size - 1
            break
    octets_m[pos] ^= 0x01
    X, H = vecteurs[0]
    xb, hb = X.to_bytes(64, "little"), H.to_bytes(16, "little")
    z_ref = chaine_seallee(octets17, xb, hb)
    try:
        z, _ = executer(octets17, bytes(octets_m), xb, puissances(H), hb, 1)
        mutant_attrape = (z != z_ref)
    except Exception:
        mutant_attrape = True
    print(f"[3] le mutant (imm8 du premier pclmulqdq) : "
          f"{'ATTRAPÉ au premier vecteur' if mutant_attrape else 'PASSE — ROUGE'}")

    # [4] LE REPLI : 32 vecteurs à r10=0 — identique au scellé chaîné
    ecart_repli = 0
    for n in range(32):
        X, H = vecteurs[n]
        xb, hb = X.to_bytes(64, "little"), H.to_bytes(16, "little")
        z_ref = chaine_seallee(octets17, xb, hb)
        z, _ = executer(octets17, octets_ag, xb, puissances(H), hb, 0)
        ecart_repli += int(z != z_ref)
    print(f"[4] le repli 32/32 : "
          f"{'jamais un chemin mort' if ecart_repli == 0 else 'ÉCARTS'}")

    # [5] LE TEMPS-CONSTANT STRUCTUREL (une empreinte par classe)
    e1 = trace_hash(octets17, octets_ag, "aleatoire")
    e2 = trace_hash(octets17, octets_ag, "structuree")
    print(f"[5] trace-hash : aléatoire {e1} · structurée {e2}")

    # [6] LA MESURE NATIVE RDTSCP (GH400 : 25 appels × 4 = 100 multiplications)
    #     + la composition GCM (CTR v4-inline entrelacé aux groupes de 4)
    rng2 = random.Random(GRAINE)
    X0 = rng2.getrandbits(512).to_bytes(64, "little")
    H0 = rng2.getrandbits(128)
    T0 = puissances(H0)
    hexa = ", ".join(f"0x{b:02x}" for b in octets17)
    hexa_ag = ", ".join(f"0x{b:02x}" for b in octets_ag)
    rig_c = RIG_C.format(s17=hexa, s17_taille=len(octets17),
                         ag=hexa_ag, ag_taille=len(octets_ag),
                         x=", ".join(f"0x{b:02x}" for b in X0),
                         t=", ".join(f"0x{b:02x}" for b in T0),
                         h=", ".join(f"0x{b:02x}" for b in H0.to_bytes(16, "little")))
    (ICI / "native").mkdir(exist_ok=True)
    (ICI / "native" / "rig_agrege.c").write_text(rig_c)
    r = subprocess.run(["gcc", "-O1", "-no-pie", "-msha", "-mssse3",
                        "-msse4.1", "-mpclmul", "-o",
                        str(ICI / "native" / "rig_agrege"),
                        str(ICI / "native" / "rig_agrege.c"), "-lcrypto"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("gcc:", r.stderr[:300])
        return 1
    rr = subprocess.run([str(ICI / "native" / "rig_agrege")],
                        capture_output=True, text=True, timeout=600)
    print("[6] la mesure native (RDTSCP, n=20, cœur épinglé) :")
    print(rr.stdout)
    garde_apres = garde_sceau("après")
    ok = (rt and ecarts == 0 and mutant_attrape and ecart_repli == 0
          and garde_avant["ok"] and garde_apres["ok"])
    print(f"[verdict] {'VERT' if ok else 'ROUGE'}")
    return 0 if ok else 1


RIG_C = """#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <sched.h>
#include <string.h>
#include <sys/mman.h>
static unsigned char S17[{s17_taille}] = {{ {s17} }};
static unsigned char AG[{ag_taille}] = {{ {ag} }};
static unsigned char Xb[64] = {{ {x} }};
static unsigned char Tb[64] = {{ {t} }};
static unsigned char Hb[16] = {{ {h} }};
#define S17_A 0xDFC0
#define AG_A 0xF300
__attribute__((naked)) static void appel_ag4(void) {{
    __asm__ volatile("movq $0x500800, %rcx; movq $0x500400, %rdx; movq $0x500600, %r8; movq $0x500A00, %r9; movq $1, %r10; movq $0xF300, %rax; jmpq *%rax");
}}
static uint64_t cyc[20];
int main(void) {{
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(1, &m);
    sched_setaffinity(0, sizeof(m), &m);
    mmap((void*)0xC000, 0x4000, 7, 0x32, -1, 0);
    mmap((void*)0x500000, 0x21000, 3, 0x32, -1, 0);
    mmap((void*)0x70000, 0x10000, 3, 0x32, -1, 0);
    memcpy((void*)S17_A, S17, {s17_taille});
    memcpy((void*)AG_A, AG, {ag_taille});
    memcpy((void*)0x500400, Xb, 64);
    memcpy((void*)0x500600, Tb, 64);
    memcpy((void*)0x500A00, Hb, 16);
    uint64_t t0, t1; uint32_t a, d;
    void (*volatile fp)(void) = appel_ag4; fp(); fp();
    for (int i = 0; i < 20; i++) {{
        __asm__ volatile("rdtscp" : "=a"(a), "=d"(d) :: "rcx");
        t0 = ((uint64_t)d << 32) | a;
        for (int k = 0; k < 25; k++) fp();
        __asm__ volatile("rdtscp" : "=a"(a), "=d"(d) :: "rcx");
        t1 = ((uint64_t)d << 32) | a;
        cyc[i] = t1 - t0;
    }}
    for (int i = 0; i < 20; i++) for (int j = i+1; j < 20; j++)
        if (cyc[j] < cyc[i]) {{ uint64_t t = cyc[i]; cyc[i] = cyc[j]; cyc[j] = t; }}
    printf("GH400 (100 mults) : mediane=%.1f iqr=%.1f -> %.2f c/mult (machine virtualisee)\\n",
           (double)(cyc[9]+cyc[10])/2.0,
           (double)(cyc[14]+cyc[15])/2.0-(double)(cyc[4]+cyc[5])/2.0,
           ((double)(cyc[9]+cyc[10])/2.0)/100.0);
    return 0;
}}
"""


if __name__ == "__main__":
    sys.exit(main())
