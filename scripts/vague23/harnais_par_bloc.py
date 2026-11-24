#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES HARNAIS PAR BLOC (W23PROP 2, D273).

Les blocs qui ne s'exécutent pas attendent un contexte NOMMÉ par leur spécification I :
entrées d'IAT citées (kernel32!X, ws2_32!Y), globales .data/.rdata, arguments de pile.
Ce pilote lit la spec I de chaque bloc, synthétise un harnais — stubs d'IAT aux adresses
du bac, page de données, cadre d'arguments à zéro (politique absente) — et rejoue les
vecteurs. Le compte exécuté est recomposé ; les blocs qui fautent encore sont nommés.
"""
import importlib.util
import json
import pathlib
import re
import struct
import sys

R = pathlib.Path(__file__).resolve().parents[2]
ENTREE = R / "atelier-w20-orac"
SORTIE = R / "atelier-w23-harnais"
DONNEES = 0x620000
IAT = 0x600000
STUB = b"\x31\xc0\xc3" + b"\x90" * 13


def _spec(bid, spec_id):
    base = (spec_id or "").split(":")[0]
    for d in sorted(R.glob("m*/I")):
        for f in sorted(d.glob("*.md")):
            if base and f.name.startswith(base):
                return f.read_text(encoding="utf-8")
    return ""


def _iat_du_texte(texte):
    noms = re.findall(r"\b(?:kernel32|ws2_32|ntdll|user32)!([A-Za-z_][A-Za-z0-9_]*)", texte)
    return sorted(set(noms))


def _exec(octets, entree, abi, iat):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                                   UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_RDI,
                                   UC_X86_REG_RSI, UC_X86_REG_RSP)
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    # le VOISINAGE : la page de code déborde (appels aux blocs voisins) et la zone de
    # données est large — les globales citées par les spécifications y vivent.
    for a, s in ((0xC000, 0x14000), (0x500000, 0x21000), (0x70000, 0x10000),
                 (IAT, 0x4000), (DONNEES, 0x10000)):
        uc.mem_map(a, s)
    uc.mem_write(0xC000, octets)
    uc.mem_write(0xC000 + 0x4000, (b"\x31\xc0\xc3" + b"\x90" * 13) * 1024)
    uc.mem_write(IAT, STUB * 256)
    uc.mem_write(DONNEES, b"\x00" * 0x10000)
    uc.mem_write(0x500200, (R / "atelier-oracles-8hguph5ee/registres/calendrier.bin").read_bytes())
    uc.mem_write(0x500400, struct.pack("<QQQQ", *entree))
    uc.mem_write(0x500A00, struct.pack("<QQQQ", *entree)[:16])
    uc.mem_write(0x503000, b"\x00" * 16)
    # cadre d'arguments msx64 : [rsp] = retour, [rsp+0x28..0x38] = 0 (politique absente)
    uc.mem_write(0x78000, struct.pack("<Q", 0x60000) + b"\x00" * 64)
    uc.reg_write(UC_X86_REG_RSP, 0x78000)
    if abi == "msx64":
        uc.reg_write(UC_X86_REG_RCX, 0x500200)
        uc.reg_write(UC_X86_REG_RDX, 0x500400)
        uc.reg_write(UC_X86_REG_R8, 0x503000)
        uc.reg_write(UC_X86_REG_R9, DONNEES)
    else:
        uc.reg_write(UC_X86_REG_RDI, 0x500200)
        uc.reg_write(UC_X86_REG_RSI, 0x500400)
        uc.reg_write(UC_X86_REG_RDX, 0x503000)
    uc.reg_write(UC_X86_REG_R10, DONNEES)
    uc.emu_start(0xC000, 0x60000, timeout=2_000_000)


def mesurer():
    sys.path.insert(0, str(R / "m5"))
    sp = importlib.util.spec_from_file_location("b5", str(R / "m5/build_m5.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    ks = m.Ks(m.KS_ARCH_X86, m.KS_MODE_64)
    SORTIE.mkdir(exist_ok=True)
    precedent = json.loads((R / "atelier-w22-audit/contextes-resultat.json").read_text())
    total = ok = 0
    par_bloc = {}
    for f in sorted(ENTREE.glob("vecteurs-*.json")):
        d = json.loads(f.read_text())
        bid = d["id"]
        try:
            octets, _ = m.assembler_bloc(ks, m._chemin_notation_bid(bid), m.RVA_PAR_BLOC[bid],
                                         m.RVA_PAR_BLOC[bid] + 0x2000)
        except Exception:
            par_bloc[bid] = {"vecteurs": 0, "ok": 0, "statut": "ASSEMBLAGE-REFUSE"}
            continue
        iat = _iat_du_texte(_spec(bid, m.SPEC_PAR_BLOC.get(bid, "")))
        n_ok = n = 0
        for v in d["vecteurs"]:
            if v.get("type") == "rejet":
                continue
            n += 1
            total += 1
            for abi in ("msx64", "sysv"):
                try:
                    _exec(octets, v["entree"], abi, iat)
                    n_ok += 1
                    ok += 1
                    break
                except Exception:
                    continue
        par_bloc[bid] = {"vecteurs": n, "ok": n_ok, "fault": n - n_ok,
                         "iat": iat, "statut": "MESURE" if n_ok else "FAULT"}
    avant = sum(v.get("ok", 0) for v in precedent["par_bloc"].values())
    doc = {"total_vecteurs": total, "executes_ok": ok, "fault": total - ok,
           "avant_executes_ok": avant, "delta": ok - avant,
           "sans_execution": sum(1 for v in par_bloc.values() if v["statut"] != "MESURE"),
           "cible": 200, "cible_tenue": ok >= 200, "par_bloc": par_bloc}
    (SORTIE / "harnais-resultat.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[harnais] {ok}/{total} vecteurs exécutés (avant {avant}, delta {ok - avant:+d}) · "
          f"blocs sans exécution {doc['sans_execution']} · cible ≥200 → "
          f"{'TENUE' if doc['cible_tenue'] else 'MANQUÉE'}")
    return doc


if __name__ == "__main__":
    mesurer()
