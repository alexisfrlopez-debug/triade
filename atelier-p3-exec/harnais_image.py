#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HARNAIS PAR BLOC v2 — L'IMAGE ENTIÈRE À SA VRAIE BASE (P3, 25/11/2026).

Conforme au plan gelé atelier-p3-exec/PLAN-HARNAIS-IMAGE.txt
(sha256 5cc5da3985838fc2905ab131ba22f3f1b28b23f6193a82ce43daecd77da31da6) :
  H1 image à B = 0x140000000 (L.IMAGE_BASE) ;
  H2 moitié code [B+0x1000,B+0x2000)∪[B+0x4000,B+0xA000) pré-remplie du
     motif de stub « xor eax,eax ; ret », chaque bloc écrit à B+son RVA ;
  H3 les quatre IAT de la carte (kernel32 0x20B0, ws2_32 0x2300,
     secur32 0x2A00, M5 0x2E30) pointent au stub B+0x20000 ; la moitié
     données [B+0x2000,B+0x4000) reste à zéro (lecture froide) ;
  H4 convention d'arguments de v1 reconduite à l'identique ;
  H5 mêmes vecteurs (atelier-w20-orac), type rejet exclu, msx64 puis sysv.

AUCUN fichier scellé n'est modifié : les notations sont assemblées en mémoire
par les builders du dépôt, exactement comme au build.
"""
import importlib.util
import json
import pathlib
import struct
import sys

R = pathlib.Path(__file__).resolve().parents[1]
ENTREE = R / "atelier-w20-orac"
SORTIE = R / "atelier-p3-exec"

B = 0x140000000                  # L.IMAGE_BASE (m3/layout.py:62)
PAGE_STUB = B + 0x20000          # page de stubs IAT (H3)
MOTIF = b"\x31\xc0\xc3" + b"\x90" * 13   # xor eax,eax ; ret — le stub de v1

# Les quatre IAT déclarées de la carte (H3) — [premier slot, dernier slot]
IATS = [
    (0x20B0, 0x2108, "kernel32"),   # R_IAT (m3/layout.py:162), jusqu'à l'INT 0x2110
    (0x2300, 0x2360, "ws2_32"),     # R_IAT_WS2 (m3/layout.py:172), 13 entrées
    (0x2A00, 0x2A30, "secur32"),    # R_IAT_SEC32 (m4/layout.py:408), 7 slots
    (0x2E30, 0x2E30, "m5"),         # R_IAT_M5 (m5/layout.py:177), 1 slot
]


def _charger_m5():
    sys.path.insert(0, str(R / "m5"))
    sp = importlib.util.spec_from_file_location("b5", str(R / "m5/build_m5.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def assembler_tous(m, ks):
    """Assemble chaque bloc de la carte à son RVA (H1) — en mémoire uniquement."""
    octets_par_bloc = {}
    refuses = []
    for bid, rva in sorted(m.RVA_PAR_BLOC.items()):
        try:
            octets, _ = m.assembler_bloc(ks, m._chemin_notation_bid(bid), rva, rva + 0x2000)
            octets_par_bloc[bid] = (rva, octets)
        except Exception as e:
            refuses.append((bid, str(e)[:120]))
    return octets_par_bloc, refuses


def _motif(taille):
    n = (taille + 15) // 16
    return (MOTIF * n)[:taille]


def _exec(octets_par_bloc, rva, entree, abi, calendrier):
    """Une émulation : l'image entière, le bloc à B+rva (H4 = convention v1)."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                                   UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_RDI,
                                   UC_X86_REG_RSI, UC_X86_REG_RSP)
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    # H1/H2 : l'image — moitié code en motif de stub, moitié données à zéro
    uc.mem_map(B + 0x1000, 0x1000)
    uc.mem_map(B + 0x2000, 0x2000)
    uc.mem_map(B + 0x4000, 0x6000)
    uc.mem_write(B + 0x1000, _motif(0x1000))
    uc.mem_write(B + 0x4000, _motif(0x6000))
    # H2 : chaque bloc de la carte à son RVA
    for _bid, (brva, octets) in octets_par_bloc.items():
        uc.mem_write(B + brva, octets)
    # H3 : chaque slot d'IAT pointe au stub
    for lo, hi, _nom in IATS:
        for a in range(lo, hi + 1, 8):
            uc.mem_write(B + a, struct.pack("<Q", PAGE_STUB))
    # H3 : la page de stub
    uc.mem_map(PAGE_STUB, 0x1000)
    uc.mem_write(PAGE_STUB, MOTIF * 256)
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
    octets_par_bloc, refuses = assembler_tous(m, ks)
    if refuses:
        print(f"[harnais] ATTENTION : {len(refuses)} blocs non assemblables (zones à stub) :")
        for bid, msg in refuses:
            print(f"  {bid}: {msg}")
    SORTIE.mkdir(exist_ok=True)

    detail = {}
    for f in sorted(ENTREE.glob("vecteurs-*.json")):
        d = json.loads(f.read_text())
        bid = d["id"]
        rva = m.RVA_PAR_BLOC[bid]
        vecteurs = []
        for v in d["vecteurs"]:
            if v.get("type") == "rejet":
                continue
            statut, motif, abi_ok = "FAULT", "", None
            for abi in ("msx64", "sysv"):
                try:
                    _exec(octets_par_bloc, rva, v["entree"], abi, calendrier)
                    statut, abi_ok = "OK", abi
                    break
                except Exception as e:
                    motif = f"{abi}:{type(e).__name__}:{str(e).split('(')[0]}"
            vecteurs.append({"exigence": v.get("exigence", "?"), "statut": statut,
                             "abi": abi_ok, "motif": motif if statut == "FAULT" else ""})
        detail[bid] = {"rva": rva, "vecteurs": vecteurs}

    # le compte est écrit BRUT ; la recomposition se fait par l'agrégateur
    (SORTIE / "resultat-image.json").write_text(
        json.dumps(detail, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(1 for b in detail.values() for v in b["vecteurs"] if v["statut"] == "OK")
    tot = sum(len(b["vecteurs"]) for b in detail.values())
    print(f"[harnais-v2] resultat-image.json écrit — brute {ok}/{tot} "
          f"(recomposition fail-closed par aggregateur_image.py)")


if __name__ == "__main__":
    mesurer()
