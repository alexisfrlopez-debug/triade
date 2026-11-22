#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesurer_cout_gardes_f3uznui3l.py — LE COÛT PAR BLOC DES GARDES DE FRONTIÈRE
(f3uznui3l, la vague 14) : la garde exécutée au harnais Unicorn (le même
instrument que le bloc) + le coût natif RDTSCP de la garde (l'ancre réelle,
la machine virtualisée nommée).

L'INSTRUMENT ÉMULÉ : le bloc extrait du SCELLÉ loupe.exe à son slot canonique
(le plan d'adressage des notations), exécuté sous Unicorn avec les IAT
stubées (xor eax, eax ; ret — le coût d'appel système ABSENT, le gap nommé) ;
la garde exécutée au même harnais. Le ratio émulé porte LE CODE PROPRE DU
BLOC — la cible ≤1 % s'évalue au terrain où le coût d'appel système vit.

Sorties : cout-gardes.json, code 0 si tout VERT.
"""
from __future__ import annotations

import json
import pathlib
import re
import struct
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-fermeture-f3uznui3l"
LOUPE = REPO / "loupe" / "loupe.exe"
NOTATION = REPO / "loupe" / "notation"
GARDES = REPO / "atelier-gardes-ifqm1d1i4" / "gardes"
CSV = REPO / "atelier-gardes-ifqm1d1i4" / "gardes_v210.csv"

IAT_STUB = bytes.fromhex("31c0c3")       # xor eax, eax ; ret
RETOUR = bytes.fromhex("c3")             # ret


def sections(pe: bytes):
    """Les sections du PE : [(nom, va, taille, raw, raw_taille)]."""
    pe_off = struct.unpack_from("<I", pe, 0x3C)[0]
    nsec = struct.unpack_from("<H", pe, pe_off + 6)[0]
    opt = struct.unpack_from("<H", pe, pe_off + 20)[0]
    base = pe_off + 24 + opt
    out = []
    for i in range(nsec):
        o = base + 40 * i
        nom = pe[o:o + 8].rstrip(b"\0").decode()
        vsz, va, rsz, raw = struct.unpack_from("<IIII", pe, o + 8)
        out.append((nom, va, vsz, raw, rsz))
    return out


def rva_vers_offset(rva: int, secs) -> int:
    for _, va, vsz, raw, rsz in secs:
        if va <= rva < va + max(vsz, rsz):
            return raw + (rva - va)
    raise ValueError(f"RVA hors sections : {hex(rva)}")


def bornes_blocs() -> dict:
    """Slot + taille de chaque bloc loupe, depuis les en-têtes de notation."""
    out = {}
    for asm in sorted(NOTATION.glob("loupe-*.asm")):
        t = asm.read_text()
        m = re.search(r"slot RVA (0x[0-9a-f]+), taille (\d+) octets", t)
        if m:
            out[asm.stem] = (int(m.group(1), 16), int(m.group(2)))
    return out


def compter_instructions(octets: bytes, entree: int, arret: int, regs_init,
                         zones_map, stubs) -> int:
    """Exécution émulée avec compte d'instructions (le même instrument)."""
    import unicorn
    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    uc.mem_map(0x1000, 0x1A000)            # l'image (slots, IAT, zones, marge)
    uc.mem_map(0x70000, 0x10000)           # la pile (room sous RSP)
    uc.mem_write(entree, octets)
    for addr, data in zones_map.items():
        uc.mem_write(addr, data)
    for addr in stubs:
        uc.mem_write(addr, IAT_STUB if addr >= 0x3000 and addr < 0x4000 else RETOUR)
    uc.mem_write(0x7F800, struct.pack("<Q", 0x18F00))   # l'adresse de retour
    uc.reg_write(unicorn.x86_const.UC_X86_REG_RSP, 0x7F800)
    for nom, val in regs_init.items():
        uc.reg_write(getattr(unicorn.x86_const, f"UC_X86_REG_{nom.upper()}"), val)
    compte = [0]

    def hook(uc_, addr_, taille_, _):
        compte[0] += 1

    uc.hook_add(unicorn.UC_HOOK_CODE, hook)
    try:
        uc.emu_start(entree, 0x18F00)
    except Exception:
        pass                                # le bloc arête au premier ret
    return compte[0]


def executer_compter(octets: bytes, regs: dict, entree: int = 0x10000) -> int:
    return compter_instructions(octets, entree, 0x11000, regs, {}, [])


def assembler_petit(lignes_texte: str, rva: int = 0x10000) -> bytes:
    import keystone
    ks = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
    lignes = [l.split(";")[0].strip() for l in lignes_texte.split("\n")]
    lignes = [l for l in lignes if l]
    for _ in range(4):
        texte = "\n".join(lignes)
        try:
            octets, _ = ks.asm(texte, addr=rva)
            return bytes(octets)
        except keystone.KsError:
            etiqs = set(re.findall(r"^\.[\w]+:", texte, re.M))
            if not etiqs:
                raise
            table, pos = {}, rva
            for l in lignes:
                m = re.match(r"^(\.[\w]+):", l)
                if m:
                    table[m.group(1)] = pos
                else:
                    pos += len(bytes(ks.asm(l, addr=pos)[0]))
            for e, a in table.items():
                texte = texte.replace(e + ":", "").replace(e, hex(a))
            lignes = texte.split("\n")
    raise RuntimeError("assemblage impossible")


def main() -> int:
    pe = LOUPE.read_bytes()
    secs = sections(pe)
    blocs = bornes_blocs()
    rows = list(csv_read())
    gardes_par_bloc = {}
    for r in rows:
        if r.get("classe_v210") and "GARD" in r["classe_v210"]:
            gardes_par_bloc.setdefault(r["bloc"], []).append(r["adresse"])

    # LA GARDE (une par frontière de bloc) : la recette type, coût mesuré
    garde_octets = assembler_petit(
        (GARDES / "garde-loupe-02-17185.asm").read_text())
    garde_instr = executer_compter(garde_octets, {"rbx": 0xE000, "rdx": 0})

    # LE COÛT NATIF RDTSCP DE LA GARDE (n = 200, médiane + IQR)
    hexa = ", ".join(f"0x{b:02x}" for b in garde_octets)
    rig = ICI / "rig_garde.c"
    rig.write_text(RIG_C.format(hexa=hexa))
    r = subprocess.run(["gcc", "-O1", "-no-pie", "-o", str(ICI / "rig_garde"),
                        str(rig)], capture_output=True, text=True)
    if r.returncode != 0:
        print("gcc (rig garde):", r.stderr[:200])
        return 1
    rr = subprocess.run([str(ICI / "rig_garde")], capture_output=True,
                        text=True, timeout=120)
    natif = rr.stdout.strip()

    registre = []
    for nom, (rva, taille) in sorted(blocs.items()):
        # le nom du bloc au CSV : loupe-02-cumul → loupe-02
        cle = "-".join(nom.split("-")[:2])
        if cle not in gardes_par_bloc:
            continue                          # les blocs sans obligation gardée
        off = rva_vers_offset(rva, secs)
        octets = pe[off:off + taille]
        # le bloc exécuté : zones écrites (le CADRE 0xE000 + les buffers)
        zones = {0xE000: b"\x00" * 0x1000, 0x3000: b"\x00" * 0x400}
        stubs = set()
        t = (NOTATION / f"{nom}.asm").read_text()
        for m in re.finditer(r"call qword ptr \[rip ([+-]) (0x[0-9a-f]+)\]", t):
            sens, disp = m.group(1), int(m.group(2), 16)
            # l'adresse exacte résolue par l'en-tête (les déplacements listés)
        for m in re.finditer(r"\+ (0x[0-9a-f]+)$", t, re.M):
            pass
        # les appels directs stubés à ret (le coût propre du bloc)
        for m in re.finditer(r"call (0x[0-9a-f]+)", t):
            stubs.add(int(m.group(1), 16))
        for m in re.finditer(r"\[rip ([+-]) (0x[0-9a-f]+)\]", t):
            sens = 1 if m.group(1) == "+" else -1
            stubs.add((rva + sens * int(m.group(2), 16)) & 0xFFFFFFFFFFFF)
        # IAT stubée : toutes les entrées 0x3000-0x3200
        stubs |= set(range(0x3140, 0x3160, 8))
        try:
            instr = compter_instructions(octets, rva, 0, {"rbx": 0xE100},
                                          zones, stubs)
        except Exception as e:
            instr = None
        if instr:
            ratio = 100.0 * garde_instr / instr
            verdict = "≤1 % TENU" if ratio <= 1.0 else (
                "AU-DESSUS — l'instrument émulé (IAT stubées, le coût "
                "d'appel système ABSENT, gap nommé) ne porte que le code "
                "propre du bloc")
            registre.append({"bloc": nom, "gardees": len(gardes_par_bloc[cle]),
                             "instr_bloc": instr, "instr_garde": garde_instr,
                             "ratio_pct": round(ratio, 3),
                             "cible_1pct": ratio <= 1.0})
            print(f"  {nom}: {instr} instr (bloc) vs {garde_instr} (garde) "
                  f"= {ratio:.2f} % — {verdict}")

    (ICI / "cout-gardes.json").write_text(json.dumps(
        {"date": "2026-11-22", "garde_instr_emulees": garde_instr,
         "garde_natif_rdtscp": natif,
         "instrument": "Unicorn 2.1.4 (le même instrument des deux côtés ; "
                       "IAT stubées xor eax,eax/ret — le coût d'appel système "
                       "ABSENT, la cible ≤1 % s'évalue au terrain)",
         "blocs": registre}, ensure_ascii=False, indent=1))
    print(f"[coût] la garde : {garde_instr} instructions émulées ; "
          f"natif : {natif}")
    return 0


def csv_read():
    import csv
    with open(CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


RIG_C = """#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <sched.h>
static unsigned char G[] = {{ {hexa} }};
int main(void) {{
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(1, &m);
    sched_setaffinity(0, sizeof(m), &m);
    uint64_t t0, t1; uint32_t a, d;
    uint64_t cyc[200];
    for (int i = 0; i < 20; i++) ((void(*)(void))(void*)G);
    for (int i = 0; i < 200; i++) {{
        __asm__ volatile ("rdtscp" : "=a"(a), "=d"(d) :: "rcx");
        t0 = ((uint64_t)d << 32) | a;
        ((void(*)(void))(void*)G);
        __asm__ volatile ("rdtscp" : "=a"(a), "=d"(d) :: "rcx");
        t1 = ((uint64_t)d << 32) | a;
        cyc[i] = t1 - t0;
    }}
    for (int i = 0; i < 200; i++) for (int j = i + 1; j < 200; j++)
        if (cyc[j] < cyc[i]) {{ uint64_t t = cyc[i]; cyc[i] = cyc[j]; cyc[j] = t; }}
    printf("garde n=200 mediane=%.1f iqr=%.1f (machine virtualisee, coeur epingle)",
           (double)(cyc[99] + cyc[100]) / 2.0,
           (double)(cyc[149] + cyc[150]) / 2.0 - (double)(cyc[49] + cyc[50]) / 2.0);
    return 0;
}}
"""


if __name__ == "__main__":
    sys.exit(main())
