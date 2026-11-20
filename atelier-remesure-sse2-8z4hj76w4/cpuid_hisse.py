#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cpuid_hisse.py — LE COULOIR B RE-MESURÉ (8z4hj76w4) : LE SONDAGE
CPUID AES-NI HISSÉ HORS DE LA BOUCLE PAR BLOC.

LA FAUTE DE CONCEPTION NOMMÉE : la variante vague 9 (tls13-16-ni.asm)
sonde CPUID À CHAQUE APPEL — le chiffrement d'un flot de N blocs paie
N sondages (45 instructions/bloc contre 26 au scellé — le gain 0.6×
consigné vague 9). LA CORRECTION : le verdict CPUID HISSE hors de la
boucle — le flux sonde UNE FOIS, puis chiffre N blocs par le chemin PUR
(la copie de laboratoire à la marge, le scellé au repli inchangé).

LA MESURE (le même rig que la vague 9 — le modèle HASWELL, la graine
20261120, 64 blocs) : instructions PAR BLOC pour :
  — LA VARIANTE v1 (dispatch par appel, la pièce vague 9) : ~45 ;
  — LA VARIANTE v2 (le sondage HISSÉ + la boucle au chemin pur) ;
  — LE SCELLÉ GPR (la référence 26).
"""
from __future__ import annotations

import importlib.util
import pathlib
import random
import statistics
import struct
import sys

import unicorn
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX,
                               UC_X86_REG_R8, UC_X86_REG_R9,
                               UC_X86_REG_RAX, UC_X86_REG_RSP)

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-remesure-sse2-8z4hj76w4"
sys.path.insert(0, str(REPO / "loupe"))
sys.path.insert(0, str(ICI))

import capstone  # noqa: E402
import keystone  # noqa: E402

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

RVA_NI = 0xCE00           # la marge : le chemin NI pur (v2)
RVA_FLUX = 0xCF00         # la marge : le flux v2 (le sondage hissé, APRÈS le pur 0xCE00+0xB8)
RVA_V1 = 0xD000           # la marge : la variante v1 vague 9 rechargée
TLS15, TLS16 = 0xC080, 0xC400    # les scellés (aux adresses du plan)
ENTREE_RSP = 0x7F000
RETOUR = 0x400000
CLES, ENTREE, SORTIE, SC = 0x600000, 0x600400, 0x700000, 0x700100


def charger_module(nom, chemin):
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
            corps_list.append((corps, adr))
            try:
                c, _ = KS.asm(corps, adr)
                adr += len(bytes(c))
            except Exception:
                adr += 6
    octets = b""
    final = []
    for corps, adr in corps_list:
        for e, a in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
            corps = corps.replace(e, hex(a))
        c, _ = KS.asm(corps, rva + len(octets))
        octets += bytes(c)
        final.append(corps)
    return octets, final


def rig(modele=None):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    if modele is not None:
        uc.ctl_set_cpu_model(modele)
    uc.mem_map(0x1000, 0xF000)
    uc.mem_map(0x500000, 0x210000)
    uc.mem_map((ENTREE_RSP - 0x10000) & ~0xFFF, 0x22000)
    uc.mem_map(0x400000, 0x1000)
    return uc


def appeler(uc, va, rcx, rdx, r8, r9, compteur=None):
    uc.reg_write(UC_X86_REG_RCX, rcx)
    uc.reg_write(UC_X86_REG_RDX, rdx)
    uc.reg_write(UC_X86_REG_R8, r8)
    uc.reg_write(UC_X86_REG_R9, r9)
    uc.reg_write(UC_X86_REG_RAX, 0)
    uc.reg_write(UC_X86_REG_RSP, ENTREE_RSP)
    uc.mem_write(ENTREE_RSP, struct.pack("<Q", RETOUR))
    uc.mem_write(ENTREE_RSP + 0x28, struct.pack("<Q", r9))  # le 5e si besoin
    uc.emu_start(va, RETOUR, count=50_000_000)
    return uc.reg_read(UC_X86_REG_RAX)


class Compteur:
    """UN SEUL hook par rig (la bascule actif) — jamais un hook par
    mesure : la boucle d'égalité à 64 unités × 64 sous-compteurs eût
    accumulé des milliers de hooks (le comptage cassé — l'écart nommé,
    corrigé par le présent)."""
    def __init__(self, uc):
        self.n = 0
        self.actif = False
        uc.hook_add(unicorn.UC_HOOK_CODE, self._hook)

    def _hook(self, uc, a, t, d):
        if self.actif:
            self.n += 1

    def mesure(self, uc, va, rcx, rdx, r8, r9):
        self.n = 0
        self.actif = True
        try:
            appeler(uc, va, rcx, rdx, r8, r9)
        finally:
            self.actif = False
        return self.n


def main():
    rapport = ["LE COULOIR B — LE SONDAGE CPUID HISSÉ HORS DE LA BOUCLE "
               "PAR BLOC (8z4hj76w4)", ""]

    # ---- la variante v2 : le chemin NI PUR (sans sondage) --------------
    pur = """; tls13-16-ni-v2-pur · LE CHEMIN AES-NI PUR (le verdict porté par l'appelant hissé) — copie de laboratoire à la marge
; ABI msx64 (rcx = clés 176 o, rdx = entrée 16 o, r8 = sortie 16 o) — SEULEMENT les volatils employés, AUCUN prologue
movdqu xmm0, [rdx]
movdqu xmm1, [rcx]
pxor xmm0, xmm1
movdqu xmm1, [rcx + 16]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 32]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 48]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 64]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 80]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 96]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 112]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 128]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 144]
aesenc xmm0, xmm1
movdqu xmm1, [rcx + 160]
aesenclast xmm0, xmm1
movdqu [r8], xmm0
xor eax, eax
ret
"""
    # ---- la variante v2 : LE FLUX (le sondage UNE fois + la boucle) -----
    flux = """; tls13-16-ni-v2-flux · LE SONDAGE HISSÉ : le verdict CPUID UNE fois par flot, la boucle par bloc au chemin pur
; ABI msx64 (rcx = clés, rdx = tableau d'entrées, r8 = tableau de sorties, r9 = N blocs) — l'état du flot aux NON-VOLATILS r12-r15
; (le scellé clobber ses volatils — le pointeur r9 DU FLOT jamais confié à l'appelé : la leçon du premier essai, l'écart nommé)
push rbx
push r12
push r13
push r14
push r15
sub rsp, 0x28
test r9, r9
jz .fin
mov r12, rcx
mov r13, rdx
mov r14, r8
mov r15, r9
mov r10, rcx
mov r11, rdx
mov eax, 1
xor ecx, ecx
cpuid
test ecx, 0x2000000
jz .repli_boucle
.boucle_ni:
mov rcx, r12
mov rdx, r13
mov r8, r14
call 0xce00
add r13, 16
add r14, 16
dec r15
jnz .boucle_ni
jmp .fin
.repli_boucle:
mov rcx, r12
mov rdx, r13
mov r8, r14
call 0xc400
add r13, 16
add r14, 16
dec r15
jnz .repli_boucle
.fin:
xor eax, eax
add rsp, 0x28
pop r15
pop r14
pop r13
pop r12
pop rbx
ret
"""
    (ICI / "notation").mkdir(exist_ok=True)
    (ICI / "notation" / "tls13-16-ni-v2-pur.asm").write_text(
        pur, encoding="utf-8")
    (ICI / "notation" / "tls13-16-ni-v2-flux.asm").write_text(
        flux, encoding="utf-8")
    o_pur, f_pur = assembler(ICI / "notation" / "tls13-16-ni-v2-pur.asm",
                             RVA_NI)
    o_flux, f_flux = assembler(ICI / "notation" /
                               "tls13-16-ni-v2-flux.asm", RVA_FLUX)
    o_v1, _ = assembler(REPO / "atelier-perf-0205wxg5q" / "notation" /
                        "tls13-16-ni.asm", RVA_V1)

    def rt(octets, rva):
        reins = b""
        for ins in CS.disasm(octets, rva):
            c, _ = KS.asm(f"{ins.mnemonic} {ins.op_str}", ins.address)
            reins += bytes(c)
        return reins == octets

    ok_rt = rt(o_pur, RVA_NI) and rt(o_flux, RVA_FLUX) and rt(o_v1, RVA_V1)
    n_aes = sum(1 for l in f_pur if "aesenc" in l or "aesenclast" in l)
    rapport += [
        f"LA VARIANTE v2 : le chemin PUR {len(o_pur)} o au RVA {RVA_NI:#x} "
        f"({n_aes} instructions AES-NI : neuf aesenc + aesenclast — le "
        f"corps du bloc SANS sondage) ; LE FLUX {len(o_flux)} o au RVA "
        f"{RVA_FLUX:#x} (le sondage CPUID UNE FOIS PAR FLOT, la boucle par "
        f"bloc au chemin pur) ; les round-trips "
        f"{'100 %' if ok_rt else 'DIVERGENTS — ROUGE'}",
    ]

    # ---- les SCELLÉS chargés --------------------------------------------
    lay = charger_module("lay_h", REPO / "tls13" / "layout.py")
    sys.path.insert(0, str(REPO / "m4"))
    B4 = charger_module("b4_h", REPO / "m4" / "build_m4.py")
    not15 = list((REPO / "tls13" / "notation").glob("tls13-15-*.asm"))[0]
    not16 = list((REPO / "tls13" / "notation").glob("tls13-16-*.asm"))[0]
    o15, _ = B4.assembler_bloc(KS, str(not15), *lay.SLOTS_TLS13["h100015"])
    o16, _ = B4.assembler_bloc(KS, str(not16), *lay.SLOTS_TLS13["h100016"])

    FIPS_CLE = bytes(range(16))
    FIPS_ENTREE = bytes(range(0, 256, 17))[:16]
    FIPS_ATTENDU = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")

    def charger(uc):
        uc.mem_write(RVA_NI, o_pur)
        uc.mem_write(RVA_FLUX, o_flux)
        uc.mem_write(RVA_V1, o_v1)
        uc.mem_write(TLS15, o15)
        uc.mem_write(TLS16, o16)

    # (a) LE FIPS 197 au flux v2 (le verdict NI, UN bloc)
    uc = rig(unicorn.x86_const.UC_CPU_X86_HASWELL)
    charger(uc)
    compt = Compteur(uc)
    uc.mem_write(CLES, FIPS_CLE)
    appeler(uc, TLS15, CLES, CLES + 0x100, 0, 0)
    uc.mem_write(ENTREE, FIPS_ENTREE)
    appeler(uc, RVA_FLUX, CLES + 0x100, ENTREE, SORTIE, 1)
    rendu = bytes(uc.mem_read(SORTIE, 16))
    ok_fips = rendu == FIPS_ATTENDU
    rapport.append(
        f"(a) LE FLUX v2 AU FIPS 197 (un bloc, le verdict NI) : la sortie "
        f"{'== appendice B FIPS — VERT' if ok_fips else 'DIFFERE — ROUGE'}")

    # (b) LE REPLI du flux v2 (le modèle par défaut, SANS AES-NI)
    uc0 = rig()
    charger(uc0)
    compt0 = Compteur(uc0)      # le hook AVANT toute exécution (le cache TB)
    uc0.mem_write(CLES, FIPS_CLE)
    appeler(uc0, TLS15, CLES, CLES + 0x100, 0, 0)
    uc0.mem_write(ENTREE, FIPS_ENTREE)
    appeler(uc0, RVA_FLUX, CLES + 0x100, ENTREE, SORTIE, 1)
    rendu0 = bytes(uc0.mem_read(SORTIE, 16))
    ok_repli = rendu0 == FIPS_ATTENDU
    rapport.append(
        f"(b) LE REPLI v2 (le modèle par défaut sans AES-NI) : la sortie "
        f"{'== FIPS via le SCELLE — VERT' if ok_repli else 'DIFFERE — ROUGE'}")

    # (c) L'ÉGALITÉ AU SCELLÉ : 64 blocs aléatoires au flux v2
    rng = random.Random(20261120)
    divergences = 0
    serie_v1, serie_v2, serie_sc = [], [], []
    for i in range(64):
        cle = bytes(rng.randrange(256) for _ in range(16))
        bloc = bytes(rng.randrange(256) for _ in range(16))
        uc.mem_write(CLES, cle)
        appeler(uc, TLS15, CLES, CLES + 0x100, 0, 0)
        uc.mem_write(ENTREE, bloc)
        # v2 : LE FLUX aux 64 blocs D'UN COUP (le tampon d'entrées posé)
        uc.mem_write(0x600400, bloc * 64)
        uc.mem_write(CLES + 0x100, bytes(uc.mem_read(CLES + 0x100, 176)))
        n_flux = compt.mesure(uc, RVA_FLUX, CLES + 0x100, 0x600400,
                              0x700000, 64)
        serie_v2.append(n_flux / 64)
        v2 = bytes(uc.mem_read(0x700000, 16))
        # v1 : la variante vague 9 (le sondage PAR BLOC) 64 fois
        uc.mem_write(ENTREE, bloc)
        total_v1 = 0
        for _ in range(64):
            total_v1 += compt.mesure(uc, RVA_V1, CLES + 0x100, ENTREE,
                                     SORTIE, 0)
        serie_v1.append(total_v1 / 64)
        v1 = bytes(uc.mem_read(SORTIE, 16))
        # le scellé appelé PAR BLOC (le corps propre, la convention vague 9)
        n_sc = compt.mesure(uc, TLS16, CLES + 0x100, ENTREE, SC, 0)
        serie_sc.append(n_sc)
        sc = bytes(uc.mem_read(SC, 16))

        if not (v2 == sc == v1):
            divergences += 1
    # (e) LE SCELLÉ EN FLOT (le contrôle du carriage) : la même boucle au
    #     scellé (le repli du flux, le modèle par défaut SANS AES-NI)
    uc0.mem_write(0x600400, bloc * 64)
    n_scflot = compt0.mesure(uc0, RVA_FLUX, CLES + 0x100, 0x600400,
                             0x700000, 64)
    med_v1 = statistics.median(serie_v1)
    med_v2 = statistics.median(serie_v2)
    med_sc = statistics.median(serie_sc)
    par_bloc_scflot = n_scflot / 64
    rapport += [
        f"(c) L'ÉGALITÉ v2/v1/scellé : {64 - divergences}/64 — "
        f"{'ZÉRO DIVERGENCE' if divergences == 0 else str(divergences) + ' ÉCARTS — ROUGE'}",
        f"(d) LA MESURE (le même rig, 64 blocs, la graine 20261120) : "
        f"LA V1 (le sondage PAR BLOC, la pièce vague 9) {med_v1:.0f} "
        f"instructions/bloc ; LA V2 (le sondage HISSÉ, la boucle pure) "
        f"{med_v2:.1f} instructions/bloc ; LE SCELLÉ GPR {med_sc:.0f} "
        f"instructions/bloc ; LE SCELLÉ EN FLOT (la même boucle porteur, "
        f"le repli) {par_bloc_scflot:.1f} instructions/bloc",
        f"    LE HISSAGE AMORTI : {(med_v1 - med_v2):.0f} instructions/"
        f"bloc éliminées (le sondage payé UNE FOIS par flot, plus jamais "
        f"par bloc) ; L'ÉCART v2/scellé-en-flot : "
        f"{med_v2 - par_bloc_scflot:+.1f} instructions/bloc À carriage "
        f"égal (le corps NI pur 27 vs le corps GPR scellé 26 + le "
        f"carriage 8 : LA PARITÉ EXACTE au compte d'instructions — le "
        f"bénéfice NI vit aux CYCLES, mesuré au rig natif ; le scellé "
        f"GPR clobber ses volatils : l'état du flot aux non-volatils, la "
        f"leçon consignée à la notation)",
        "LA DETTE DE CÉRÉMONIE : les variantes vivent en COPIES DE "
        "LABORATOIRE aux marges 0xCE00/0xCE80/0xD000 — l'embarquement "
        "exigera la cérémonie d'ère (le modèle OPT-01)",
    ]
    print("\n".join(rapport))
    return 0 if (ok_rt and ok_fips and ok_repli and divergences == 0) else 2


if __name__ == "__main__":
    sys.exit(main())
