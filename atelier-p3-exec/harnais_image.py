#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HARNAIS PAR BLOC v4 — L'IMAGE SCELLÉE, LA SPÉCIFICATION, LA PILE DU PROBING (P3).

Plans gelés : PLAN-HARNAIS-IMAGE.txt (v2, 5cc5da39…), AMENDEMENT-V3.txt
(141192d2…), AMENDEMENT-V4.txt (empreinte dans EMPREINTES.txt) :
  H1   image à B = 0x140000000 (L.IMAGE_BASE) ;
  V3-1 sections du binaire scellé à leur RVA (LECTURE SEULE) ; le bloc
       mesuré écrit à B+son RVA depuis SA NOTATION ASSEMBLÉE ;
  V3-2 ExitProcess (0x20C0) → TERMINATEUR ; V4-2 GetCommandLineW (0x2E30)
       → stub sémantique rendant L"proxy.exe" à 0x630000 ;
  V4-1 pile [0x60000, 0x80000), rsp=0x78000 (le probing http-10 couvert) ;
  V4-3 image de contexte = l'exécutable nommé par EXE_PAR_BLOC ;
  V4-4 après la convention fixe de v1, seconde tentative à la convention
       TIRÉE DE LA SPÉCIFICATION (consignée par vecteur) ;
  H4/H5 convention d'arguments et vecteurs de v1, à l'identique.
"""
import importlib.util
import json
import pathlib
import struct
import sys

R = pathlib.Path(__file__).resolve().parents[1]
ENTREE = R / "atelier-w20-orac"
SORTIE = R / "atelier-p3-exec"
EXES = {"proxy": R / "m5/proxy.exe", "selftest": R / "m1/selftest.exe",
        "echo": R / "m2/echo.exe", "hello": R / "m0/hello.exe"}

B = 0x140000000
PAGE_STUB = B + 0x20000
TERMINATEUR = PAGE_STUB + 0x800
STUB_GCLW = PAGE_STUB + 0x900          # V4-2
LIGNE_CMD = 0x630000                   # V4-2 : L"proxy.exe"
MOTIF = b"\x31\xc0\xc3" + b"\x90" * 13
SLOT_EXIT = 0x20C0
SLOT_GCLW = 0x2E30                     # IAT M5 (m5/layout.py:177)

IATS = [
    (0x20B0, 0x2108, "kernel32"),
    (0x2300, 0x2360, "ws2_32"),
    (0x2A00, 0x2A30, "secur32"),
    (0x2E30, 0x2E30, "m5"),
]

# V4-4 : conventions d'arguments TIRÉES DE LA SPÉCIFICATION I (msx64 ;
# la variante sysv met les mêmes valeurs en rdi/rsi/rdx/rcx).
CONVENTIONS_SPEC = {
    "c30011": {"args": [0x500200, 8, 42, 0x500A00], "arg5": 4},      # tcp-11
    "e50002": {"args": [0x500200, 16, 0x503000, None]},               # http-02
    "e50004": {"args": [0x500200, 32, 0x500A00, 4], "arg5": 0x503000},  # http-04
    "e50006": {"args": [0x500200, 16, None, None]},                   # http-06
    "e50007": {"args": [0x500200, 16, 80, 0x503000]},                 # http-07
    "g70006": {"args": [0x620000, 0x500A00, 16, None]},               # tls-06
    "g70010": {"args": [0x10, None, None, None]},                     # http-10:R2
    "g80002": {"args": [0x10, None, None, None]},                     # http-10:R3
}


def _charger_m5():
    sys.path.insert(0, str(R / "m5"))
    sp = importlib.util.spec_from_file_location("b5", str(R / "m5/build_m5.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _sections_exe(chemin):
    import pefile
    data = chemin.read_bytes()
    pe = pefile.PE(data=data, fast_load=True)
    assert pe.OPTIONAL_HEADER.ImageBase == B
    sections = []
    for s in pe.sections:
        brut = data[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]
        sections.append((s.VirtualAddress, brut, s.Misc_VirtualSize))
    return sections


def _exe_du_bloc(m, bid):
    """V4-3 : l'exécutable de contexte — celui qui contient le bloc."""
    porteurs = [n for n in ("proxy", "selftest", "echo", "hello")
                if n in m.EXE_PAR_BLOC.get(bid, "")]
    for nom in porteurs:                      # proxy d'abord (le plus complet)
        return EXES[nom]
    return EXES["proxy"]


def _exec(sections, rva, octets_bloc, entree, abi, calendrier, conv_spec=None):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                                   UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_RDI,
                                   UC_X86_REG_RSI, UC_X86_REG_RSP)
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    mapped = []                             # plages (debut, fin) mapées
    for va, brut, virt in sections:
        taille = max((virt + 0xFFF) & ~0xFFF, (len(brut) + 0xFFF) & ~0xFFF)
        uc.mem_map(B + va, taille)
        uc.mem_write(B + va, brut)
        mapped.append((B + va, B + va + taille))
    uc.mem_write(B + rva, octets_bloc)
    # les stubs + la ligne de commande (V4-2)
    uc.mem_map(PAGE_STUB, 0x1000)
    uc.mem_write(PAGE_STUB, MOTIF * 256)
    uc.mem_write(TERMINATEUR, b"\x48\xb8" + struct.pack("<Q", 0x60000) + b"\xff\xe0")
    uc.mem_write(STUB_GCLW, b"\x48\xb8" + struct.pack("<Q", LIGNE_CMD) + b"\xc3")
    uc.mem_map(0x630000, 0x1000)
    uc.mem_write(0x630000, "proxy.exe".encode("utf-16-le") + b"\x00\x00")
    # les IAT : patchées SI elles tombent dans une section mapée (V4-3 garde)
    def _dans_image(a):
        return any(lo <= B + a < hi for lo, hi in mapped)
    for lo, hi, _nom in IATS:
        for a in range(lo, hi + 1, 8):
            if not _dans_image(a):
                continue
            if a == SLOT_EXIT:
                cible = TERMINATEUR
            elif a == SLOT_GCLW:
                cible = STUB_GCLW
            else:
                cible = PAGE_STUB
            uc.mem_write(B + a, struct.pack("<Q", cible))
    # H4 (convention fixe v1) ; V4-1 : pile élargie au probing http-10
    uc.mem_map(0x500000, 0x21000)
    uc.mem_map(0x60000, 0x20000)
    uc.mem_map(0x620000, 0x10000)
    uc.mem_write(0x500200, calendrier)
    uc.mem_write(0x500400, struct.pack("<QQQQ", *entree))
    uc.mem_write(0x500A00, struct.pack("<QQQQ", *entree)[:16])
    uc.mem_write(0x503000, b"\x00" * 16)
    uc.mem_write(0x78000, struct.pack("<Q", 0x60000) + b"\x00" * 64)
    uc.reg_write(UC_X86_REG_RSP, 0x78000)
    if conv_spec is None:
        # la convention fixe de v1, à l'identique
        vals = [0x500200, 0x500400, 0x503000, 0x620000]
        arg5 = None
    else:
        vals = conv_spec["args"]
        arg5 = conv_spec.get("arg5")
    if arg5 is not None:
        uc.mem_write(0x78000 + 0x20, struct.pack("<Q", arg5))
    r1, r2, r3, r4 = vals
    if abi == "msx64":
        if r1 is not None: uc.reg_write(UC_X86_REG_RCX, r1)
        if r2 is not None: uc.reg_write(UC_X86_REG_RDX, r2)
        if r3 is not None: uc.reg_write(UC_X86_REG_R8, r3)
        if r4 is not None: uc.reg_write(UC_X86_REG_R9, r4)
    else:
        if r1 is not None: uc.reg_write(UC_X86_REG_RDI, r1)
        if r2 is not None: uc.reg_write(UC_X86_REG_RSI, r2)
        if r3 is not None: uc.reg_write(UC_X86_REG_RDX, r3)
        if r4 is not None: uc.reg_write(UC_X86_REG_RCX, r4)
    uc.reg_write(UC_X86_REG_R10, 0x620000)
    uc.emu_start(B + rva, 0x60000, timeout=2_000_000)


def mesurer():
    import hashlib
    m = _charger_m5()
    ks = m.Ks(m.KS_ARCH_X86, m.KS_MODE_64)
    calendrier = (R / "atelier-oracles-8hguph5ee/registres/calendrier.bin").read_bytes()

    sections_cache = {nom: _sections_exe(ch) for nom, ch in EXES.items()}
    sha_exes = {nom: hashlib.sha256(ch.read_bytes()).hexdigest()
                for nom, ch in EXES.items()}

    detail = {}
    for f in sorted(ENTREE.glob("vecteurs-*.json")):
        d = json.loads(f.read_text())
        bid = d["id"]
        rva = m.RVA_PAR_BLOC[bid]
        exe_ctx = _exe_du_bloc(m, bid)
        nom_exe = {v: k for k, v in EXES.items()}[exe_ctx]
        sections = sections_cache[nom_exe]
        octets_bloc, _ = m.assembler_bloc(ks, m._chemin_notation_bid(bid), rva, rva + 0x2000)
        conv = CONVENTIONS_SPEC.get(bid)
        vecteurs = []
        for v in d["vecteurs"]:
            if v.get("type") == "rejet":
                continue
            statut, motif, abi_ok, conv_ok = "FAULT", "", None, None
            # tentative 1 : convention fixe v1 ; tentative 2 : convention spec (V4-4)
            for cnom, c in (("v1", None), ("spec", conv)):
                if c is None and cnom == "spec":
                    continue
                for abi in ("msx64", "sysv"):
                    try:
                        _exec(sections, rva, octets_bloc, v["entree"], abi,
                              calendrier, c)
                        statut, abi_ok, conv_ok = "OK", abi, cnom
                        break
                    except Exception as e:
                        motif = f"{abi}/{cnom}:{type(e).__name__}:{str(e).split('(')[0]}"
                if statut == "OK":
                    break
            vecteurs.append({"exigence": v.get("exigence", "?"), "statut": statut,
                             "abi": abi_ok, "convention": conv_ok,
                             "motif": motif if statut == "FAULT" else ""})
        detail[bid] = {"rva": rva, "exe_contexte": nom_exe, "vecteurs": vecteurs}

    (SORTIE / "resultat-image.json").write_text(
        json.dumps({"sha_exes": sha_exes, "blocs": detail},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(1 for b in detail.values() for v in b["vecteurs"] if v["statut"] == "OK")
    tot = sum(len(b["vecteurs"]) for b in detail.values())
    print(f"[harnais-v4] resultat-image.json écrit — brute {ok}/{tot} "
          f"(recomposition fail-closed par agregateur_image.py)")


if __name__ == "__main__":
    mesurer()
