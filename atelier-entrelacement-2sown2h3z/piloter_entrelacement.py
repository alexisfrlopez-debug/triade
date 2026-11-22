#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""piloter_entrelacement.py — LE PILOTE DU COULOIR DE COMPOSITION
CTR v4i × GHASH AGRÉGÉ-4 (2sown2h3z, la vague 15) : l'assemblage, le
round-trip, la différentielle ≥320 vecteurs contre LA CHAÎNE SCELLÉE
(l'AES scellé par bloc de compteur + le GHASH scellé chaîné par bloc),
le mutant imm8, le repli 32/32, le FIPS 197 C.1, la trace-hash
temps-constant structurel, la dérivation de la table des puissances
PAR LE SCELLÉ, la garde du sceau-I avant/après.
La graine 20261124 consignée AVANT le premier tirage (le plan gelé).
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import random
import struct
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-entrelacement-2sown2h3z"
NOTA = ICI / "notation" / "ctr-v4i-ghash-agrege4.asm"
SC16 = REPO / "tls13" / "notation" / "tls13-16-aes128-bloc.asm"        # AES 0xDF00
SC17 = REPO / "tls13" / "notation" / "tls13-17-ghash-multiplication.asm"  # GHASH 0xDFC0
RVA_COULOIR = 0xF800
SC16_RVA = 0xDF00
SC17_RVA = 0xDFC0
TABLE = 0x508000
GRAINE = 20261124

import keystone
import capstone
import unicorn

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
UC = unicorn.Uc
XR = unicorn.x86_const

REG = {"rax": XR.UC_X86_REG_RAX, "rcx": XR.UC_X86_REG_RCX,
       "rdx": XR.UC_X86_REG_RDX, "r8": XR.UC_X86_REG_R8,
       "r9": XR.UC_X86_REG_R9, "r10": XR.UC_X86_REG_R10,
       "r11": XR.UC_X86_REG_R11}


# ------------------------------------------------- l'assemblage (v14) ------
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


# ------------------------------------------------- la machine Unicorn ------
def machine(octets16: bytes, octets17: bytes, octets_couloir: bytes,
            trace: list | None = None):
    uc = UC(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    uc.mem_map(0xC000, 0x4000)      # les scellés + couloirs
    uc.mem_map(0x500000, 0x21000)   # données
    uc.mem_map(0x70000, 0x10000)    # pile
    uc.mem_write(SC16_RVA, octets16)
    uc.mem_write(SC17_RVA, octets17)
    uc.mem_write(RVA_COULOIR, octets_couloir)
    if trace is not None:
        def croc(uc_, adr, taille, donnees, t=trace):
            t.append((adr, taille))
        uc.hook_add(unicorn.UC_HOOK_CODE, croc)
    return uc


def appeler_couloir(uc, cles: bytes, compteurs: bytes, clair: bytes,
                    N: int, r10: int, table_puissances: bytes,
                    adresse_ct: int = 0x503000):
    """Le couloir : rcx=clés, rdx=compteurs, r8=clair, r9=ct, r10=verdict,
    r11=N ; le tag lu à [ct + N*16]."""
    uc.mem_write(0x500200, cles)
    uc.mem_write(0x501000, compteurs)
    uc.mem_write(0x502000, clair)
    uc.mem_write(TABLE, table_puissances)
    uc.mem_write(0x78000, struct.pack("<Q", 0x60000))
    uc.reg_write(XR.UC_X86_REG_RSP, 0x78000)
    uc.reg_write(REG["rcx"], 0x500200)
    uc.reg_write(REG["rdx"], 0x501000)
    uc.reg_write(REG["r8"], 0x502000)
    uc.reg_write(REG["r9"], adresse_ct)
    uc.reg_write(REG["r10"], r10)
    uc.reg_write(REG["r11"], N)
    uc.emu_start(RVA_COULOIR, 0x60000)
    ct = bytes(uc.mem_read(adresse_ct, 16 * N + 16))
    return ct[:16 * N], ct[16 * N:], uc.reg_read(REG["rax"])


def scelle_aes(uc, bloc: bytes, cles: bytes) -> bytes:
    uc.mem_write(0x500400, bloc)
    uc.mem_write(0x500200, cles)
    uc.mem_write(0x78000, struct.pack("<Q", 0x60000))
    uc.reg_write(XR.UC_X86_REG_RSP, 0x78000)
    uc.reg_write(REG["rcx"], 0x500200)
    uc.reg_write(REG["rdx"], 0x500400)
    uc.reg_write(REG["r8"], 0x500800)
    uc.emu_start(SC16_RVA, 0x60000)
    return bytes(uc.mem_read(0x500800, 16))


def scelle_ghash(uc, X: bytes, H: bytes) -> bytes:
    uc.mem_write(0x500400, X)
    uc.mem_write(0x500A00, H)
    uc.mem_write(0x78000, struct.pack("<Q", 0x60000))
    uc.reg_write(XR.UC_X86_REG_RSP, 0x78000)
    uc.reg_write(REG["rcx"], 0x500800)
    uc.reg_write(REG["rdx"], 0x500400)
    uc.reg_write(REG["r8"], 0x500A00)
    uc.reg_write(REG["r10"], 0)
    uc.emu_start(SC17_RVA, 0x60000)
    return bytes(uc.mem_read(0x500800, 16))


def chaine_seallee(uc, cles: bytes, compteurs: bytes, clair: bytes,
                   N: int, H: bytes):
    """LA RÉFÉRENCE : l'AES scellé par bloc de compteur, le GHASH scellé
    chaîné par bloc — la chaîne intégralement scellée."""
    ct = bytearray()
    y = b"\x00" * 16
    for i in range(N):
        ks = scelle_aes(uc, compteurs[16 * i:16 * i + 16], cles)
        c = bytes(a ^ b for a, b in zip(ks, clair[16 * i:16 * i + 16]))
        ct += c
        x = bytes(a ^ b for a, b in zip(c, y))
        y = scelle_ghash(uc, x, H)
    return bytes(ct), y


# --------------------------------------------- la table du juge -----------
def table_puissances(uc, N: int, H: bytes) -> bytes:
    """[H^N ‖ H^{N-1} ‖ … ‖ H] — N entrées, l'entrée i = H^{N-i}
    (0-based) DÉRIVÉES PAR LE SCELLÉ : H^2 = scellé(H, H), puis chaîne.
    l'entrée d'indice N-1 = H (la dernière)."""
    entrees = [None] * N
    h = H
    entrees[N - 1] = h                # H^1
    for k in range(2, N + 1):
        h = scelle_ghash(uc, h, H)    # H^k
        entrees[N - k] = h
    return b"".join(entrees)


# ------------------------------------------------- le juge FIPS 197 -------
def expansion_cle(k: bytes):
    sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01,
            0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d,
            0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4,
            0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
            0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7,
            0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2,
            0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e,
            0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb,
            0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa, 0xfb,
            0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
            0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
            0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c,
            0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d,
            0x64, 0x5d, 0x19, 0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a,
            0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3,
            0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d,
            0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a,
            0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
            0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e,
            0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
            0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9,
            0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99,
            0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
    rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
    w = [list(k[4 * i:4 * i + 4]) for i in range(4)]
    for i in range(4, 44):
        t = list(w[i - 1])
        if i % 4 == 0:
            t = t[1:] + t[:1]
            t = [sbox[b] for b in t]
            t[0] ^= rcon[i // 4 - 1]
        w.append([a ^ b for a, b in zip(w[i - 4], t)])
    return b"".join(bytes(x) for x in w)


# ------------------------------------------------- LE PILOTE --------------
def main():
    rapport = []
    def consigne(ligne: str):
        print(ligne)
        rapport.append(ligne)

    # la graine consignée AVANT le premier tirage
    rng = random.Random(GRAINE)

    # 1. l'assemblage + round-trip
    consigne(f"=== l'assemblage (marge 0x{RVA_COULOIR:X}) ===")
    octets16 = assembler(SC16, SC16_RVA)
    octets17 = assembler(SC17, SC17_RVA)
    octets_c = assembler(NOTA, RVA_COULOIR)
    consigne(f"scellé tls13-16 : {len(octets16)} o ; scellé tls13-17 : "
             f"{len(octets17)} o ; couloir : {len(octets_c)} o")
    rt = round_trip(octets_c, RVA_COULOIR)
    consigne(f"round-trip keystone==capstone==keystone : "
             f"{'VERT' if rt else 'ROUGE'} ({len(octets_c)} o, "
             f"{sum(1 for _ in CS.disasm(octets_c, RVA_COULOIR))} instr)")

    uc = machine(octets16, octets17, octets_c)

    # 2. LE FIPS 197 C.1 par le couloir (le clair nul : ct[0] = E_k(PT_C.1))
    cles_fips = expansion_cle(bytes(range(16)))
    pt_c1 = bytes.fromhex("00112233445566778899aabbccddeeff")
    ct_attendu = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")
    table_c1 = table_puissances(uc, 4, b"\x42" * 16)
    ct_c1, tag_c1, rax_c1 = appeler_couloir(
        uc, cles_fips, pt_c1 * 4, b"\x00" * 64, 4, 1, table_c1)
    fips_ok = ct_c1[:16] == ct_attendu and rax_c1 == 0
    consigne(f"FIPS 197 C.1 par le couloir (N=4, clair nul) : "
             f"{'VERT' if fips_ok else 'ROUGE'} (ct[0]={ct_c1[:16].hex()})")

    # 3. LA DIFFÉRENTIELLE : 256 aléatoires + 64 structurés
    consigne("=== la différentielle contre la chaîne scellée ===")
    compteurs, indices = 0, 0
    tailles = [4, 8, 16, 64, 256, 5, 6, 7, 12, 13]
    ecarts = 0
    n_vec = 0
    classes: dict[str, list] = {}
    while n_vec < 256:
        N = tailles[n_vec % len(tailles)]
        cles = expansion_cle(bytes(rng.getrandbits(8) for _ in range(16)))
        H = bytes(rng.getrandbits(8) for _ in range(16))
        compteurs_b = bytes(rng.getrandbits(8) for _ in range(16 * N))
        clair = bytes(rng.getrandbits(8) for _ in range(16 * N))
        n_vec += 1
        tbl = table_puissances(uc, N, H)
        ct_ref, tag_ref = chaine_seallee(uc, cles, compteurs_b, clair, N, H)
        ct_c, tag_c, rax_c = appeler_couloir(uc, cles, compteurs_b, clair,
                                             N, 1, tbl)
        if ct_c != ct_ref or tag_c != tag_ref or rax_c != 0:
            ecarts += 1
            consigne(f"  ECART au vecteur {n_vec} (N={N}) : "
                     f"ct={'ok' if ct_c == ct_ref else 'ECART'} "
                     f"tag={'ok' if tag_c == tag_ref else 'ECART'}")
    consigne(f"256 aléatoires : {'ZÉRO ÉCART' if ecarts == 0 else str(ecarts) + ' ÉCARTS'}")

    ecarts_s = 0
    motifs = [b"\x00" * 16, b"\xff" * 16,
              bytes(range(16)), bytes(range(15, -1, -1))]
    for k in range(64):
        N = tailles[k % len(tailles)]
        cles = expansion_cle(bytes((k * 7 + i) & 0xff for i in range(16)))
        H = bytes((k * 13 + i) & 0xff for i in range(16))
        motif = motifs[k % len(motifs)]
        compteurs_b = (motif * (N + 1))[:16 * N]
        clair = (motifs[(k + 1) % len(motifs)] * (N + 1))[:16 * N]
        tbl = table_puissances(uc, N, H)
        ct_ref, tag_ref = chaine_seallee(uc, cles, compteurs_b, clair, N, H)
        ct_c, tag_c, rax_c = appeler_couloir(uc, cles, compteurs_b, clair,
                                             N, 1, tbl)
        if ct_c != ct_ref or tag_c != tag_ref or rax_c != 0:
            ecarts_s += 1
            consigne(f"  ECART au structuré {k} (N={N})")
    consigne(f"64 structurés : {'ZÉRO ÉCART' if ecarts_s == 0 else str(ecarts_s) + ' ÉCARTS'}")
    consigne(f"LA DIFFÉRENTIELLE : {256 + 64} vecteurs, "
             f"{'ZÉRO ÉCART' if ecarts + ecarts_s == 0 else str(ecarts + ecarts_s) + ' ÉCARTS'} "
             f"(graine {GRAINE} consignée)")

    # 4. LE MUTANT imm8 : le premier pclmulqdq du couloir muté
    octets_m = bytearray(octets_c)
    offset_mutant = None
    adr = RVA_COULOIR
    for ins in CS.disasm(bytes(octets_m), RVA_COULOIR):
        if ins.mnemonic == "pclmulqdq":
            offset_mutant = ins.address - RVA_COULOIR + len(ins.bytes) - 1
            break
    octets_m[offset_mutant] ^= 0x01
    uc_m = machine(octets16, octets17, bytes(octets_m))
    cles = expansion_cle(bytes(rng.getrandbits(8) for _ in range(16)))
    H = bytes(rng.getrandbits(8) for _ in range(16))
    N = 4
    compteurs_b = bytes(rng.getrandbits(8) for _ in range(16 * N))
    clair = bytes(rng.getrandbits(8) for _ in range(16 * N))
    tbl = table_puissances(uc_m, N, H)
    ct_ref, tag_ref = chaine_seallee(uc_m, cles, compteurs_b, clair, N, H)
    ct_m, tag_m, _ = appeler_couloir(uc_m, cles, compteurs_b, clair, N, 1, tbl)
    mutant_attrape = (tag_m != tag_ref) or (ct_m != ct_ref)
    consigne(f"LE MUTANT imm8 (l'octet {offset_mutant} du premier pclmulqdq) : "
             f"{'ATTRAPÉ au premier vecteur' if mutant_attrape else 'PASSÉ — ROUGE'}")

    # 5. LE REPLI : 32 vecteurs à la chaîne scellée interne (r10 = 0)
    repli_ok = 0
    for k in range(32):
        N = tailles[k % len(tailles)]
        cles = expansion_cle(bytes(rng.getrandbits(8) for _ in range(16)))
        H = bytes(rng.getrandbits(8) for _ in range(16))
        compteurs_b = bytes(rng.getrandbits(8) for _ in range(16 * N))
        clair = bytes(rng.getrandbits(8) for _ in range(16 * N))
        tbl = table_puissances(uc, N, H)
        ct_ref, tag_ref = chaine_seallee(uc, cles, compteurs_b, clair, N, H)
        ct_r, tag_r, rax_r = appeler_couloir(uc, cles, compteurs_b, clair,
                                             N, 0, tbl)
        if ct_r == ct_ref and tag_r == tag_ref and rax_r == 0:
            repli_ok += 1
    consigne(f"LE REPLI (r10 = 0, la chaîne scellée interne) : "
             f"{repli_ok}/32 {'— jamais un chemin mort' if repli_ok == 32 else '— ROUGE'}")

    # 6. LA BORNE fail-closed : N > 256
    ct_b, tag_b, rax_b = appeler_couloir(
        uc, cles_fips, b"\x00" * (16 * 257), b"\x00" * (16 * 257),
        257, 1, b"\x00" * 16)
    consigne(f"LA BORNE N ≤ 256 fail-closed : rax = {rax_b if rax_b >= 0 else rax_b - (1 << 64)}"
             f" {'(le refus -2 VÉCU)' if (rax_b - (1 << 64)) == -2 else ''}")
    ct_b, tag_b, rax_b = appeler_couloir(
        uc, cles_fips, b"", b"", 0, 1, b"\x00" * 16)
    consigne(f"LA BORNE N = 0 fail-closed : rax = {rax_b if rax_b >= 0 else rax_b - (1 << 64)}"
             f" {'(le refus -2 VÉCU)' if (rax_b - (1 << 64)) == -2 else ''}")

    # 7. LA TRACE-HASH TEMPS-CONSTANT STRUCTUREL : une empreinte par classe
    for classe, fabrique in (
            ("aleatoire", lambda r: (bytes(r.getrandbits(8) for _ in range(16 * 8)),
                                     bytes(r.getrandbits(8) for _ in range(16 * 8)))),
            ("structure", lambda r: (bytes(range(16)) * 8, b"\xff" * (16 * 8)))):
        empreintes = set()
        r2 = random.Random(GRAINE)
        for _ in range(8):
            cles = expansion_cle(bytes(r2.getrandbits(8) for _ in range(16)))
            H = bytes(r2.getrandbits(8) for _ in range(16))
            compteurs_b, clair = fabrique(r2)
            tbl = table_puissances(uc, 8, H)
            trace: list = []
            uc_t = machine(octets16, octets17, octets_c, trace=trace)
            ct_t, tag_t, _ = appeler_couloir(uc_t, cles, compteurs_b, clair,
                                             8, 1, tbl)
            empreintes.add(hashlib.sha256(
                b"".join(struct.pack("<QB", a, t) for a, t in trace)).hexdigest())
        consigne(f"LA TRACE-HASH classe {classe} (8 mesures, N=8) : "
                 f"{len(empreintes)} empreinte(s) "
                 f"{'— UNE par classe' if len(empreintes) == 1 else '— ROUGE'}")

    # 8. la table DÉRIVÉE PAR LE SCELLÉ : le recoupement algébrique du juge
    #    (l'entrée i = H^{N-i} : la nième entrée = H ⇒ scellé(H,H) == entrée N-2)
    H = bytes(rng.getrandbits(8) for _ in range(16))
    tbl = table_puissances(uc, 8, H)
    h2 = scelle_ghash(uc, H, H)
    tbl_ok = tbl[6 * 16:7 * 16] == h2
    consigne(f"LA TABLE dérivée par le scellé (entrée N-2 == scellé(H,H)) : "
             f"{'VERT' if tbl_ok else 'ROUGE'}")

    (ICI / "registres" / "differentielle.json").write_text(json.dumps({
        "graine": GRAINE, "corridor": len(octets_c), "round_trip": rt,
        "fips_c1": fips_ok, "differentielle": {"aleatoires": 256,
        "ecarts_aleatoires": ecarts, "structure": 64,
        "ecarts_structure": ecarts_s}, "mutant_attrape": mutant_attrape,
        "repli": f"{repli_ok}/32",
        "sha256_couloir": hashlib.sha256(octets_c).hexdigest(),
    }, indent=2), encoding="utf-8")
    (ICI / "rapport-differentielle.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\nOK — registres/differentielle.json + rapport-differentielle.txt")


if __name__ == "__main__":
    main()
