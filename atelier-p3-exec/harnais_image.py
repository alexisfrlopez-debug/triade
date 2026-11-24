#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HARNAIS PAR BLOC v3 — L'IMAGE SCELLÉE POUR CONTEXTE, LA NOTATION POUR LE CODE (P3).

Plan gelé PLAN-HARNAIS-IMAGE.txt (sha256 5cc5da39…31da6) + AMENDEMENT-V3.txt
(sha256 141192d2…9e2356) :
  H1  image à B = 0x140000000 (L.IMAGE_BASE) ;
  V3-1 les sections du binaire scellé m5/proxy.exe sont chargées à leur RVA
      (LECTURE SEULE — le fichier n'est jamais ouvert en écriture) ;
      le bloc mesuré est écrit à B+son RVA depuis SA NOTATION ASSEMBLÉE
      (le moteur de v1/v2 demeure ; corrige la collision des slots partagés) ;
  V3-2 le slot kernel32 0x20C0 (ExitProcess) reçoit un TERMINATEUR
      (mov rax, 0x60000 ; jmp rax) — ExitProcess ne rend jamais la main,
      le ud2 défensif qui suit demeure inatteignable ; tous les autres
      slots des quatre IAT demeurent au stub retour zéro ;
  H4  convention d'arguments de v1 reconduite à l'identique ;
  H5  mêmes vecteurs (atelier-w20-orac), type rejet exclu, msx64 puis sysv.
"""
import importlib.util
import json
import pathlib
import struct
import sys

R = pathlib.Path(__file__).resolve().parents[1]
ENTREE = R / "atelier-w20-orac"
SORTIE = R / "atelier-p3-exec"
EXE_SCELLE = R / "m5/proxy.exe"       # lecture seule (V3-1)

B = 0x140000000                       # L.IMAGE_BASE
PAGE_STUB = B + 0x20000
TERMINATEUR = PAGE_STUB + 0x800       # V3-2
MOTIF = b"\x31\xc0\xc3" + b"\x90" * 13
SLOT_EXIT = 0x20C0                    # ExitProcess (ordre GSH/WF/EP figé)

IATS = [
    (0x20B0, 0x2108, "kernel32"),    # R_IAT (m3/layout.py:162)
    (0x2300, 0x2360, "ws2_32"),      # R_IAT_WS2
    (0x2A00, 0x2A30, "secur32"),     # R_IAT_SEC32 (m4/layout.py:408)
    (0x2E30, 0x2E30, "m5"),          # R_IAT_M5 (m5/layout.py:177)
]


def _charger_m5():
    sys.path.insert(0, str(R / "m5"))
    sp = importlib.util.spec_from_file_location("b5", str(R / "m5/build_m5.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _sections_exe():
    """Les sections du binaire scellé : [(rva, octets, taille_virtuelle)]."""
    import pefile
    data = EXE_SCELLE.read_bytes()
    pe = pefile.PE(data=data, fast_load=True)
    assert pe.OPTIONAL_HEADER.ImageBase == B
    sections = []
    for s in pe.sections:
        brut = data[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]
        virt = s.Misc_VirtualSize
        sections.append((s.VirtualAddress, brut, virt))
    return sections


def _terminateur():
    """mov rax, 0x60000 ; jmp rax — arrêt propre sur la sentinelle (V3-2)."""
    return b"\x48\xb8" + struct.pack("<Q", 0x60000) + b"\xff\xe0"


def _exec(sections, rva, octets_bloc, entree, abi, calendrier):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                                   UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_RDI,
                                   UC_X86_REG_RSI, UC_X86_REG_RSP)
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    # V3-1 : les sections du binaire scellé à leur RVA (une carte par section,
    # arrondie à la page ; le flanc virtuel au-delà du brut est à zéro)
    for va, brut, virt in sections:
        taille = max((virt + 0xFFF) & ~0xFFF, (len(brut) + 0xFFF) & ~0xFFF)
        uc.mem_map(B + va, taille)
        uc.mem_write(B + va, brut)
    # V3-1 : le bloc mesuré, depuis SA notation assemblée
    uc.mem_write(B + rva, octets_bloc)
    # H3/V3-2 : les quatre IAT — stub retour zéro, sauf ExitProcess terminateur
    uc.mem_map(PAGE_STUB, 0x1000)
    uc.mem_write(PAGE_STUB, MOTIF * 256)
    uc.mem_write(TERMINATEUR, _terminateur())
    for lo, hi, _nom in IATS:
        for a in range(lo, hi + 1, 8):
            cible = TERMINATEUR if a == SLOT_EXIT else PAGE_STUB
            uc.mem_write(B + a, struct.pack("<Q", cible))
    # H4 : la convention d'arguments de v1, à l'identique
    uc.mem_map(0x500000, 0x21000)
    uc.mem_map(0x70000, 0x10000)
    uc.mem_map(0x620000, 0x10000)
    uc.mem_write(0x500200, calendrier)
    uc.mem_write(0x500400, struct.pack("<QQQQ", *entree))
    uc.mem_write(0x500A00, struct.pack("<QQQQ", *entree)[:16])
    uc.mem_write(0x503000, b"\x00" * 16)
    uc.mem_write(0x78000, struct.pack("<Q", 0x60000) + b"\x00" * 64)
    uc.reg_write(UC_X86_REG_RSP, 0x78000)
    if abi == "msx64":
        uc.reg_write(UC_X86_REG_RCX, 0x500200)
        uc.reg_write(UC_X86_REG_RDX, 0x500400)
        uc.reg_write(UC_X86_REG_R8, 0x503000)
        uc.reg_write(UC_X86_REG_R9, 0x620000)
    else:
        uc.reg_write(UC_X86_REG_RDI, 0x500200)
        uc.reg_write(UC_X86_REG_RSI, 0x500400)
        uc.reg_write(UC_X86_REG_RDX, 0x503000)
    uc.reg_write(UC_X86_REG_R10, 0x620000)
    uc.emu_start(B + rva, 0x60000, timeout=2_000_000)


def mesurer():
    m = _charger_m5()
    ks = m.Ks(m.KS_ARCH_X86, m.KS_MODE_64)
    calendrier = (R / "atelier-oracles-8hguph5ee/registres/calendrier.bin").read_bytes()
    sections = _sections_exe()
    print(f"[harnais-v3] binaire scellé : {len(sections)} sections chargées "
          f"(lecture seule, sha256 enregistré par l'agrégateur)")
    import hashlib
    sha_exe = hashlib.sha256(EXE_SCELLE.read_bytes()).hexdigest()
    print(f"[harnais-v3] m5/proxy.exe sha256 {sha_exe[:16]}…")

    detail = {}
    for f in sorted(ENTREE.glob("vecteurs-*.json")):
        d = json.loads(f.read_text())
        bid = d["id"]
        rva = m.RVA_PAR_BLOC[bid]
        # le bloc mesuré est assemblé depuis sa notation (V3-1)
        octets_bloc, _ = m.assembler_bloc(ks, m._chemin_notation_bid(bid), rva, rva + 0x2000)
        vecteurs = []
        for v in d["vecteurs"]:
            if v.get("type") == "rejet":
                continue
            statut, motif, abi_ok = "FAULT", "", None
            for abi in ("msx64", "sysv"):
                try:
                    _exec(sections, rva, octets_bloc, v["entree"], abi, calendrier)
                    statut, abi_ok = "OK", abi
                    break
                except Exception as e:
                    motif = f"{abi}:{type(e).__name__}:{str(e).split('(')[0]}"
            vecteurs.append({"exigence": v.get("exigence", "?"), "statut": statut,
                             "abi": abi_ok, "motif": motif if statut == "FAULT" else ""})
        detail[bid] = {"rva": rva, "vecteurs": vecteurs}

    (SORTIE / "resultat-image.json").write_text(
        json.dumps({"sha_proxy_exe": sha_exe, "blocs": detail},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(1 for b in detail.values() for v in b["vecteurs"] if v["statut"] == "OK")
    tot = sum(len(b["vecteurs"]) for b in detail.values())
    print(f"[harnais-v3] resultat-image.json écrit — brute {ok}/{tot} "
          f"(recomposition fail-closed par agregateur_image.py)")


if __name__ == "__main__":
    mesurer()
