#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES CONTEXTES D'EXÉCUTION DES 50 BLOCS (W22AUDT b).

Constat de la vague 20 : 81 des 320 vecteurs s'exécutaient, 239 fautaient faute de contexte
(pas d'IAT, pas de fenêtre de registres, pas de pile gardée). Ici on fournit un contexte
STANDARD — IAT bouchonnée, deux ABI essayées (msx64 : rcx/rdx/r8 ; sysv : rdi/rsi/rdx), pile
avec sentinelle — et on rejoue les vecteurs. Le delta est consigné par bloc ; un bloc qui
faute encore reste FAULT (aucun résultat inventé).
"""
import importlib.util, json, pathlib, struct, sys

R = pathlib.Path(__file__).resolve().parents[2]
ENTREE = R / "atelier-w20-orac"
SORTIE = R / "atelier-w22-audit"
STUBS = 0x400000
STUB = b"\x31\xc0\xc3" + b"\x90" * 13


def _exec(octets, entree, abi):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,
                                   UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_RSP)
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    for a, s in ((0xC000, 0x4000), (0x500000, 0x21000), (0x70000, 0x10000), (STUBS, 0x2000)):
        uc.mem_map(a, s)
    uc.mem_write(0xC000, octets)
    uc.mem_write(STUBS, STUB * 256)
    cal = (R / "atelier-oracles-8hguph5ee/registres/calendrier.bin").read_bytes()
    uc.mem_write(0x500200, cal)
    uc.mem_write(0x500400, struct.pack("<QQQQ", *entree))
    uc.mem_write(0x500A00, struct.pack("<QQQQ", *entree)[:16])
    uc.mem_write(0x503000, b"\x00" * 16)
    uc.mem_write(0x78000, struct.pack("<Q", 0x60000))
    uc.reg_write(UC_X86_REG_RSP, 0x78000)
    if abi == "msx64":
        uc.reg_write(UC_X86_REG_RCX, 0x500200); uc.reg_write(UC_X86_REG_RDX, 0x500400)
        uc.reg_write(UC_X86_REG_R8, 0x503000); uc.reg_write(UC_X86_REG_R9, STUBS)
    else:
        uc.reg_write(UC_X86_REG_RDI, 0x500200); uc.reg_write(UC_X86_REG_RSI, 0x500400)
        uc.reg_write(UC_X86_REG_RDX, 0x503000)
    uc.emu_start(0xC000, 0x60000, timeout=2_000_000)


def mesurer():
    sys.path.insert(0, str(R / "m5"))
    sp = importlib.util.spec_from_file_location("b5", str(R / "m5/build_m5.py"))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    ks = m.Ks(m.KS_ARCH_X86, m.KS_MODE_64)
    SORTIE.mkdir(exist_ok=True)
    total = ok = 0
    par_bloc = {}
    for f in sorted(ENTREE.glob("vecteurs-*.json")):
        d = json.loads(f.read_text()); bid = d["id"]
        try:
            octets, _ = m.assembler_bloc(ks, m._chemin_notation_bid(bid), m.RVA_PAR_BLOC[bid],
                                         m.RVA_PAR_BLOC[bid] + 0x2000)
        except Exception:
            par_bloc[bid] = {"vecteurs": 0, "ok": 0, "statut": "ASSEMBLAGE-REFUSE"}
            continue
        n_ok = n = 0
        for v in d["vecteurs"]:
            if v.get("type") == "rejet":
                continue
            n += 1; total += 1
            for abi in ("msx64", "sysv"):
                try:
                    _exec(octets, v["entree"], abi); n_ok += 1; ok += 1
                    v["contexte"] = abi
                    break
                except Exception:
                    continue
        par_bloc[bid] = {"vecteurs": n, "ok": n_ok, "fault": n - n_ok,
                         "statut": "MESURE" if n_ok else "FAULT"}
    doc = {"total_vecteurs": total, "executes_ok": ok, "fault": total - ok,
           "par_bloc": par_bloc, "vague20_executes_ok": 81}
    (SORTIE / "contextes-resultat.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1),
                                                    encoding="utf-8")
    print(f"[contextes] {ok}/{total} vecteurs exécutés OK (vague 20 : 81) · delta +{ok - 81} · "
          f"blocs sans exécution : {sum(1 for v in par_bloc.values() if v['statut'] != 'MESURE')}")
    return doc


if __name__ == "__main__":
    mesurer()
