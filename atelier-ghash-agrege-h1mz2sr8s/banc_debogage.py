#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE BANC DE DÉBOGAGE — l'assemblage, le round-trip et l'exécution Unicorn
du GHASH AGRÉGÉ avant le pilote complet : le couloir à 0xF300, le scellé à
0xDFC0, la table des puissances tordues dérivée par le juge, la
différentielle contre QUATRE chaînés, le repli, le mutant. Pièce de travail
de la méthode itérative (assemble, round-trip, rig, débloque)."""
import pathlib
import random
import sys

import capstone
import keystone
import unicorn

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = pathlib.Path(__file__).resolve().parent
KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

RVA_AGG = 0xF300
SC17 = 0xDFC0


def charger_module(nom, chemin):
    import importlib.util
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


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


# le juge + twist (recopiés du pilote v13 / de la dérivation)
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


def ghash_juge(NX, NY):
    return rev128(polymod(clmul(rev128(NX), rev128(NY))))


M64 = (1 << 64) - 1
M128 = (1 << 128) - 1
CONST_C = (0xC200000000000000 << 64) | 1


def twist(v):
    carry = v >> 127
    lo, hi = v & M64, (v >> 64) & M64
    w = ((lo << 1) & M64) | (((hi << 1) & M64) << 64)
    w |= ((lo >> 63) & 1) << 64
    if carry:
        w ^= CONST_C
    return w & M128


def table_tordue(NH):
    P1 = NH
    P2 = ghash_juge(NH, NH)
    P3 = ghash_juge(P2, NH)
    P4 = ghash_juge(P3, NH)
    return b"".join(twist(P).to_bytes(16, "big") for P in (P1, P2, P3, P4))


def appeler_msx64(uc, fn, rcx_v, rdx_v, r8_v, r9_v, r10_v):
    uc.mem_write(0x700100, b"\xC3")
    uc.mem_write(0x708000, (0x700100).to_bytes(8, "little"))
    uc.reg_write(unicorn.x86_const.UC_X86_REG_RSP, 0x708000)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_RCX, rcx_v)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_RDX, rdx_v)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_R8, r8_v)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_R9, r9_v)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_R10, r10_v)
    uc.emu_start(fn, 0x700100)
    return uc.reg_read(unicorn.x86_const.UC_X86_REG_RAX)


def chaine_s17(uc, Xs, H):
    """QUATRE chaînés au scellé : Y = 0 ; Y = S17(Y ⊕ X_i, H). Le tampon
    0x500C00 (JAMAIS 0x500400 — l'aire X reste intacte pour le contrôle)."""
    Y = bytes(16)
    for Xi in Xs:
        tmp = bytes(a ^ b for a, b in zip(Y, Xi))
        uc.mem_write(0x500C00, tmp)
        uc.mem_write(0x500600, H)
        appeler_msx64(uc, SC17, 0x500800, 0x500C00, 0x500600, 0, 0)
        Y = bytes(uc.mem_read(0x500800, 16))
    return Y


def main():
    for d in ("m4", "m3", "m2", "m1", "tls13", "loupe"):
        p = str(REPO / d)
        if p not in sys.path:
            sys.path.insert(0, p)
    B4 = charger_module("b4_ghash", REPO / "m4" / "build_m4.py")
    lay = charger_module("lay_ghash", REPO / "tls13" / "layout.py")
    o_s17, _ = B4.assembler_bloc(KS, str(REPO / "tls13" / "notation" /
                                "tls13-17-ghash-multiplication.asm"),
                                *lay.SLOTS_TLS13["h100017"])
    o_agg = assembler(ICI / "notation" / "ghash-pclmulqdq-agrege4.asm", RVA_AGG)
    print(f"octets agrégé : {len(o_agg)} · scellé : {len(o_s17)}")
    print(f"round-trip agrégé : {round_trip(o_agg, RVA_AGG)}")

    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    uc.mem_map(0xC000, 0x4000)
    uc.mem_map(0x700000, 0x10000)
    uc.mem_map(0x500000, 0x21000)
    uc.mem_write(RVA_AGG, o_agg)
    uc.mem_write(SC17, o_s17)
    uc.ctl_remove_cache(0xC000, 0x10000)

    rng = random.Random(20261121)
    ok = 0
    for i in range(40):
        Xs = [bytes(rng.getrandbits(8) for _ in range(16)) for _ in range(4)]
        H = bytes(rng.getrandbits(8) for _ in range(16))
        NH = int.from_bytes(H, "big")
        table = table_tordue(NH)
        uc.mem_write(0x500400, b"".join(Xs))
        uc.mem_write(0x500A00, table)
        uc.mem_write(0x500800, b"\xAA" * 16)
        rax = appeler_msx64(uc, RVA_AGG, 0x500800, 0x500400, 0x500A00,
                            0x500A00, 1)
        Z = bytes(uc.mem_read(0x500800, 16))
        intact = bytes(uc.mem_read(0x500400, 64)) == b"".join(Xs)
        ref = chaine_s17(uc, Xs, H)
        ok += (Z == ref and rax == 0 and intact)
    print(f"différentielle (agrége vs 4 chaînés + rax + X intacts) : {ok}/40")

    # le repli : r10 = 0
    okr = 0
    for _ in range(16):
        Xs = [bytes(rng.getrandbits(8) for _ in range(16)) for _ in range(4)]
        H = bytes(rng.getrandbits(8) for _ in range(16))
        table = table_tordue(int.from_bytes(H, "big"))
        uc.mem_write(0x500400, b"".join(Xs))
        uc.mem_write(0x500A00, table)
        uc.mem_write(0x500800, b"\xAA" * 16)
        rax = appeler_msx64(uc, RVA_AGG, 0x500800, 0x500400, 0x500A00,
                            0x500A00, 0)
        Z = bytes(uc.mem_read(0x500800, 16))
        ref = chaine_s17(uc, Xs, H)
        okr += (Z == ref and rax == 0)
    print(f"repli (r10=0, untwist + 4 chaînés) : {okr}/16")

    # le mutant : l'imm8 du premier pclmulqdq muté
    mut = bytearray(o_agg)
    trouve = None
    for ins in CS.disasm(bytes(mut), RVA_AGG):
        if ins.mnemonic == "pclmulqdq":
            trouve = ins.address - RVA_AGG + ins.size - 1
            break
    assert trouve is not None
    mut[trouve] ^= 0x01
    uc.mem_write(0x501000, bytes(mut))
    uc.ctl_remove_cache(0x501000, 0x502000)
    Xs = [bytes(rng.getrandbits(8) for _ in range(16)) for _ in range(4)]
    H = bytes(rng.getrandbits(8) for _ in range(16))
    table = table_tordue(int.from_bytes(H, "big"))
    uc.mem_write(0x500400, b"".join(Xs))
    uc.mem_write(0x500A00, table)
    appeler_msx64(uc, 0x501000, 0x500800, 0x500400, 0x500A00, 0x500A00, 1)
    Zm = bytes(uc.mem_read(0x500800, 16))
    ref = chaine_s17(uc, Xs, H)
    print(f"mutant (imm8 pclmulqdq#1 muté) : "
          f"{'ATTRAPÉ au premier vecteur' if Zm != ref else 'PAS ATTRAPÉ (rouge!)'}")


if __name__ == "__main__":
    main()
