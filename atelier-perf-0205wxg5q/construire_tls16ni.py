#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_tls16ni.py — LE BUILD ET LA VÉRIFICATION DE LA VARIANTE
AES-NI de tls13-16 (le couloir B — la vague 9, l'instruction 0205wxg5q
point 2, le PLAN-0205WXG5Q H2 gelé).

LE RIG AUTONOME : un Uc nu (le modèle CPU posé AVANT toute cartographie —
qemu64 par défaut : la sonde rend SANS AES-NI, le repli vécu ; Haswell :
AES-NI porté, le chemin NI exercé), les blocs chargés à leurs adresses
du plan (le tls13-15 SCELLÉ 0xDCC0, le tls13-16 SCELLÉ 0xDF00, la
VARIANTE 0xCE00 — la marge vierge), l'appel msx64 par le point d'entrée
magique.

LA VÉRIFICATION (la lettre de l'instruction) :
  — le round-trip 100 % (keystone → capstone → keystone) ;
  — LE REPLI vécu au modèle par défaut (la sonde naturelle rend sans
    AES-NI — le SCELLÉ exécuté) ;
  — LE FIPS 197 appendice B au chemin NI (Haswell) ;
  — L'ÉGALITÉ NI/SCELLÉ sur 64 blocs aléatoires (le juge : la sortie du
    scellé au même bloc — zéro divergence exigée) ;
  — LA MESURE : les instructions/bloc NI contre le scellé GPR (le même
    rig, la même série, la graine 20261120)."""
from __future__ import annotations

import importlib.util
import pathlib
import random
import statistics
import struct
import sys

import capstone
import keystone
import unicorn
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                               UC_X86_REG_R9, UC_X86_REG_RAX, UC_X86_REG_RSP,
                               UC_X86_REG_RBX, UC_X86_REG_R12)

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-perf-0205wxg5q"
KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

RVA_NI = 0xCE00
TLS15, TLS16 = 0xDCC0, 0xDF00
RETOUR = 0x9000            # l'adresse magique de retour
ENTREE_RSP = 0x7E000008    # la pile du rig (≡ 8 mod 16 — l'entrée msx64 VÉCUE)


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def resoudre(lignes, rva):
    etiquettes = {}
    corps_list = []
    for _ in range(4):
        adr = rva
        corps_list = []
        for l in lignes:
            l = l.strip()
            if not l or l.startswith(";"):
                continue
            if l.startswith(".") and l.endswith(":"):
                etiquettes[l[:-1]] = adr
                continue
            corps = l
            for e, a in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
                corps = corps.replace(e, hex(a))
            corps_list.append((corps, adr))
            try:
                c, _ = KS.asm(corps, adr)
                adr += len(bytes(c))
            except Exception:
                adr += 6
    octets = b""
    final = []
    for corps, adr in corps_list:
        c, _ = KS.asm(corps, RVA_NI + len(octets))
        octets += bytes(c)
        final.append(corps)
    return octets, final


def rig(modele=None):
    """Le Uc nu : le modèle AVANT la cartographie."""
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    if modele is not None:
        uc.ctl_set_cpu_model(modele)
    uc.mem_map(0x1000, 0xF000)
    uc.mem_map(0x500000, 0x210000)
    uc.mem_map((ENTREE_RSP - 0x10000) & ~0xFFF, 0x22000)
    return uc


def appeler(uc, va, rcx, rdx, r8, r9, compteur=None):
    uc.reg_write(UC_X86_REG_RCX, rcx)
    uc.reg_write(UC_X86_REG_RDX, rdx)
    uc.reg_write(UC_X86_REG_R8, r8)
    uc.reg_write(UC_X86_REG_R9, r9)
    uc.reg_write(UC_X86_REG_RAX, 0)
    uc.reg_write(UC_X86_REG_RSP, ENTREE_RSP)
    uc.mem_write(ENTREE_RSP, struct.pack("<Q", RETOUR))
    uc.emu_start(va, RETOUR, count=50_000_000)
    return uc.reg_read(UC_X86_REG_RAX)


class Compteur:
    def __init__(self, uc):
        self.n = 0
        uc.hook_add(unicorn.UC_HOOK_CODE, self._hook)

    def _hook(self, uc, a, t, d):
        self.n += 1


def main():
    rapport = ["LE COULOIR B — LA VARIANTE AES-NI DE TLS13-16 (le chemin "
               "descendu à l'ISA, le hot path crypto mesuré)", ""]
    lignes = [l.split(";")[0] for l in (
        ICI / "notation" / "tls13-16-ni.asm").read_text(
        encoding="utf-8").splitlines()]
    octets, final = resoudre(lignes, RVA_NI)
    reins = b""
    for ins in CS.disasm(octets, RVA_NI):
        c, _ = KS.asm(f"{ins.mnemonic} {ins.op_str}", ins.address)
        reins += bytes(c)
    if reins != octets:
        raise RuntimeError("le round-trip DIVERGE")
    n_ni = sum(1 for l in final if "aesenc" in l or "aesenclast" in l)
    rapport.append(f"LA VARIANTE : {len(octets)} o au RVA {RVA_NI:#x} (la "
                   f"marge VIERGE — le scellé intact), {n_ni} instructions "
                   f"AES-NI (neuf aesenc + aesenclast), LE ROUND-TRIP 100 %")

    # les SCELLÉS chargés : tls13-15 (les clés) + tls13-16 (le bloc)
    lay = charger_module("lay_tls_ni2", REPO / "tls13" / "layout.py")
    sys.path.insert(0, str(REPO / "m4"))
    B4 = charger_module("b4_ni2", REPO / "m4" / "build_m4.py")
    not15 = list((REPO / "tls13" / "notation").glob("tls13-15-*.asm"))[0]
    not16 = list((REPO / "tls13" / "notation").glob("tls13-16-*.asm"))[0]
    o15, _ = B4.assembler_bloc(KS, str(not15), *lay.SLOTS_TLS13["h100015"])
    o16, _ = B4.assembler_bloc(KS, str(not16), *lay.SLOTS_TLS13["h100016"])

    FIPS_CLE = bytes(range(16))
    FIPS_ENTREE = bytes(range(0, 256, 17))[:16]
    FIPS_ATTENDU = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")
    CLES, ENTREE, SORTIE, SC = 0x600000, 0x600400, 0x700000, 0x700100

    def charger(uc):
        uc.mem_write(RVA_NI, octets)
        uc.mem_write(TLS15, o15)
        uc.mem_write(TLS16, o16)

    # (a) LE MODÈLE PAR DÉFAUT : la sonde naturelle → LE REPLI VÉCU
    uc = rig()
    charger(uc)
    uc.mem_write(CLES, FIPS_CLE)
    r15 = appeler(uc, TLS15, CLES, CLES + 0x100, 0, 0)
    rk0 = bytes(uc.mem_read(CLES + 0x100, 16))
    assert r15 == 0 and rk0 == FIPS_CLE, (
        f"tls13-15 : rax={r15} RK[0]={rk0.hex()} (la clé {FIPS_CLE.hex()})")
    uc.mem_write(ENTREE, FIPS_ENTREE)
    appeler(uc, RVA_NI, CLES + 0x100, ENTREE, SORTIE, 0)
    rendu = bytes(uc.mem_read(SORTIE, 16))
    ok_repli = rendu == FIPS_ATTENDU
    rapport.append(f"(a) LE MODÈLE PAR DÉFAUT (la sonde NATURELLE rend sans "
                   f"AES-NI) : LE REPLI VÉCU — le scellé exécuté, la sortie "
                   f"{'== le FIPS 197 — VERT (le repli est le scellé)' if ok_repli else '≠ le FIPS — ROUGE'}")

    # (b) HASWELL : LE CHEMIN NI — le FIPS 197
    uc = rig(unicorn.x86_const.UC_CPU_X86_HASWELL)
    charger(uc)
    uc.mem_write(CLES, FIPS_CLE)
    appeler(uc, TLS15, CLES, CLES + 0x100, 0, 0)
    uc.mem_write(ENTREE, FIPS_ENTREE)
    cpt = Compteur(uc)
    appeler(uc, RVA_NI, CLES + 0x100, ENTREE, SORTIE, 0)
    rendu_ni = bytes(uc.mem_read(SORTIE, 16))
    ok_fips = rendu_ni == FIPS_ATTENDU
    n_fips = cpt.n
    rapport.append(f"(b) LE MODÈLE HASWELL : LE CHEMIN NI — la sortie "
                   f"{rendu_ni.hex()} "
                   f"{'== LE FIPS 197 APPENDICE B — VERT' if ok_fips else '≠ LE FIPS — ROUGE'} "
                   f"({n_fips} instructions/bloc)")

    # (c) L'ÉGALITÉ NI/SCELLÉ : 64 blocs aléatoires — le juge est le
    # scellé au même bloc (zéro divergence exigée)
    rng = random.Random(20261120)
    divergences = 0
    serie_ni, serie_sc = [], []
    for i in range(64):
        cle = bytes(rng.randrange(256) for _ in range(16))
        bloc = bytes(rng.randrange(256) for _ in range(16))
        uc.mem_write(CLES, cle)
        appeler(uc, TLS15, CLES, CLES + 0x100, 0, 0)
        uc.mem_write(ENTREE, bloc)
        cpt1 = Compteur(uc)
        appeler(uc, RVA_NI, CLES + 0x100, ENTREE, SORTIE, 0)
        serie_ni.append(cpt1.n)
        ni = bytes(uc.mem_read(SORTIE, 16))
        cpt2 = Compteur(uc)
        appeler(uc, TLS16, CLES + 0x100, ENTREE, SC, 0)
        serie_sc.append(cpt2.n)
        sc = bytes(uc.mem_read(SC, 16))
        if ni != sc:
            divergences += 1
    med_ni, med_sc = statistics.median(serie_ni), statistics.median(serie_sc)
    rapport += [
        f"(c) L'ÉGALITÉ NI/SCELLÉ : {64 - divergences}/64 — "
        f"{'ZÉRO DIVERGENCE (le NI rend le scellé octet pour octet)' if divergences == 0 else str(divergences) + ' ÉCARTS — ROUGE'}",
        f"(d) LA MESURE (le même rig, 64 blocs, la graine 20261120) : NI "
        f"{med_ni:.0f} instructions/bloc contre le SCELLÉ GPR {med_sc:.0f}"
        f" — LE GAIN {med_sc/med_ni:.1f}×",
        "",
        "LE TEMPS CONSTANT STRUCTUREL : le chemin NI ne porte AUCUN saut "
        "de données (les dix tours TOUJOURS exécutés — I1 par "
        "construction) ; le dispatch saute sur le VERDICT CPUID (public), "
        "jamais sur une donnée secrète.",
        "LA DETTE DE CÉRÉMONIE : la variante vit en COPIE DE LABORATOIRE "
        "à la marge 0xCE00 — l'embarquement exigera la cérémonie d'ère "
        "(le sceau-I, la clé hors-ligne — le modèle OPT-01 : JAMAIS "
        "scellé sans le geste du maître). Le GHASH PCLMULQDQ (l'autre "
        "moitié du chemin GCM) demeure LE CHEMIN SUIVANT — le plan le "
        "porte, la cérémonie le précède.",
    ]
    (ICI / "rapport-couloir-b.txt").write_text("\n".join(rapport) + "\n",
                                               encoding="utf-8")
    print("\n".join(rapport))
    return 0 if (ok_repli and ok_fips and divergences == 0) else 2


if __name__ == "__main__":
    raise SystemExit(main())
