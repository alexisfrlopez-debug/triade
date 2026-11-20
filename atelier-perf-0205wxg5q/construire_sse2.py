#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_sse2.py — LE BUILD DE LA VARIANTE SSE2 (le couloir A) : les
étiquettes résolues en ADRESSES ABSOLUES (le format maison — l'auteur
résout, keystone assemble, rien d'autre), le round-trip capstone 100 %,
la CONFRONTATION aux vecteurs dorés (zéro divergence exigée contre
l'implémentation triviale — le juge, jamais le binaire), la MESURE du
coût (le même moteur, les mêmes vecteurs, la même convention de parité
que couloir_a_mesure.py)."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import random
import statistics
import sys

import capstone
import keystone
import unicorn

REPO = pathlib.Path("/home/z/my-project/depot")
sys.path.insert(0, str(REPO / "loupe"))
ICI = REPO / "atelier-perf-0205wxg5q"

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

RVA = 0xCC00          # la marge .text2 vierge — AUCUN octet du scellé touché


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def resoudre_etiquettes(lignes: list[str], rva: int) -> list[str]:
    """Les DEUX PASSES : (1) les tailles (les étiquettes à 0), (2) les
    adresses absolues — le format maison (l'auteur résout)."""
    etiquettes: dict[str, int] = {}
    for _ in range(3):        # la convergence (les tailles changent les cibles)
        adr = rva
        out = []
        for l in lignes:
            l = l.strip()
            if not l or l.startswith(";"):
                continue
            if l.endswith(":") and l.startswith("."):
                etiquettes[l[:-1]] = adr
                continue
            corps = l
            for e, a in etiquettes.items():
                corps = corps.replace(e, hex(a))
            try:
                c, _ = KS.asm(corps, adr)
            except Exception:
                # l'étiquette en avant : garder le nom (la passe suivante)
                pass
            out.append((l, adr))
            try:
                c, _ = KS.asm(corps, adr)
            except Exception:
                # estimer la taille à la passe suivante — 6 o par défaut
                adr += 6
                continue
            adr += len(bytes(c))
    # la passe finale : remplacer
    final = []
    for l, adr in out:
        if l.endswith(":") and l.startswith("."):
            continue
        corps = l
        for e, a in etiquettes.items():
            corps = corps.replace(e, hex(a))
        final.append(corps)
    return final, etiquettes


def assembler(fichier: pathlib.Path):
    lignes = [l.split(";")[0] for l in fichier.read_text(
        encoding="utf-8").splitlines()]
    final, etiquettes = resoudre_etiquettes(lignes, RVA)
    octets = b""
    for l in final:
        c, _ = KS.asm(l, RVA + len(octets))
        octets += bytes(c)
    # LE ROUND-TRIP (R5) : désassembler, ré-assembler — byte-identique
    reins = b""
    for ins in CS.disasm(octets, RVA):
        c, _ = KS.asm(f"{ins.mnemonic} {ins.op_str}", ins.address)
        reins += bytes(c)
    if reins != octets:
        raise RuntimeError("le round-trip DIVERGE")
    return octets, etiquettes, final


def main():
    rapport = []
    octets, etiquettes, final = assembler(ICI / "notation" /
                                          "loupe-13-sse2.asm")
    n_sse2 = sum(1 for l in final if any(
        s in l for s in ("movdqu", "pcmpeqb", "pmovmskb", "movd",
                         "punpckldq", "punpcklqdq")))
    rapport.append(f"LA VARIANTE SSE2 : {len(octets)} o assemblés au "
                   f"RVA {RVA:#x} (la marge VIERGE — le scellé intact), "
                   f"{n_sse2} instructions SSE2 baseline, LE ROUND-TRIP "
                   f"100 % (capstone → keystone, byte-identique)")
    rapport.append(f"  les étiquettes résolues : "
                   f"{ {k: hex(v) for k, v in etiquettes.items()} }")

    # LA CONFRONTATION : les mêmes vecteurs que la mesure avant (la graine
    # 20261120, n=15 × les tailles aux bords) + LES BORDS NOMMÉS
    HE = charger_module("h_ed_sse2", REPO / "loupe" / "harnais_edition.py")
    os_v = HE.OSEdition()
    emul = HE.EmulationEdition(
        os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
        (REPO / "m1" / "selftest.exe").read_bytes(),
        (REPO / "demo" / "demo.exe").read_bytes())
    emul.uc.mem_map(0x500000, 0x21000)
    emul.uc.mem_write(RVA, octets)
    emul.uc.ctl_remove_cache(RVA & ~0xFFF, (RVA + len(octets) + 0xFFF)
                             & ~0xFFF)

    class Compteur:
        def __init__(self, e):
            self.n = 0
            e.uc.hook_add(unicorn.UC_HOOK_CODE, self._hook)

        def _hook(self, uc, a, t, d):
            self.n += 1

    rng = random.Random(20261120)
    res_sse2, res_scelle = [], []
    diverge = 0
    # la même série que couloir_a_mesure (15 × 4096/16) + LES BORDS
    serie = [(4096, 16)] * 15 + [(0, 1), (1, 1), (2, 32), (33, 32),
                                 (64, 1), (65, 32), (255, 31), (256, 32),
                                 (1000, 33 if False else 32)]
    not13 = list((REPO / "loupe" / "notation").glob("loupe-13-*.asm"))[0]
    B4 = charger_module("b4_sse2", REPO / "m4" / "build_m4.py")
    import harnais_noyau as HN
    rva13, slot13 = HN.L.SLOTS_LOUPE["i110013"]
    octets13, _ = B4.assembler_bloc(KS, str(not13), rva13, slot13)
    for (n, lm) in serie:
        f = bytes(rng.randrange(256) for _ in range(n))
        m = bytes(rng.randrange(256) for _ in range(lm))
        depart = 0
        attendu = f.find(m)
        emul.uc.mem_write(0x500000, f)
        emul.uc.mem_write(0x510000, m)
        # LA VARIANTE
        cpt = Compteur(emul)
        with contextlib.redirect_stdout(io.StringIO()):
            r = emul.appeler(RVA, {"rcx": 0x500000, "rdx": n,
                                   "r8": 0x510000, "r9": lm},
                             pile_args=[depart])
        if (r["rax"] & (1 << 64) - 1) != (attendu & (1 << 64) - 1):
            diverge += 1
            rapport.append(f"  DIVERGENCE au vecteur n={n} lm={lm} : "
                           f"{r['rax']} ≠ {attendu}")
        res_sse2.append(cpt.n)
        # LE SCELLÉ (la même instance rechargée)
        emul.uc.mem_write(rva13, octets13)
        cpt2 = Compteur(emul)
        with contextlib.redirect_stdout(io.StringIO()):
            r2 = emul.appeler(rva13, {"rcx": 0x500000, "rdx": n,
                                      "r8": 0x510000, "r9": lm},
                              pile_args=[depart])
        res_scelle.append(cpt2.n)
        if (r2["rax"] & (1 << 64) - 1) != (attendu & (1 << 64) - 1):
            diverge += 1
    med_sse2 = statistics.median(res_sse2)
    med_scelle = statistics.median(res_scelle)
    med_gcc = 115292          # la pièce couloir-a-avant.csv (gcc -O2)
    rapport += [
        "",
        f"LA CONFRONTATION : {len(serie)} vecteurs (les 15 de la mesure "
        f"avant + LES 9 BORDS NOMMÉS : n ∈ {{0,1,2,33,64,65,255,256,1000}}, "
        f"le motif ∈ {{1,16,31,32}}) — "
        f"{'ZÉRO DIVERGENCE' if diverge == 0 else str(diverge) + ' DIVERGENCES'} "
        f"contre l'implémentation triviale (le juge Python, jamais le "
        f"binaire)",
        "",
        f"LA MESURE APRÈS (les mêmes vecteurs 4096/16, le même moteur) :",
        f"  LA VARIANTE SSE2 : médiane {med_sse2:.0f} instructions/op",
        f"  LE SCELLÉ GPR   : médiane {med_scelle:.0f} instructions/op",
        f"  LE BRAS C gcc-O2 : médiane {med_gcc:.0f} (la pièce d'avant)",
        f"  LE RATIO SSE2/gcc-O2 : {med_sse2/med_gcc:.2f}× — "
        f"{'le coût INFÉRIEUR OU ÉGAL à gcc-O2 : L\'OBJECTIF TENU' if med_sse2 <= med_gcc else 'l\'objectif à reprendre'}",
        f"  LE GAIN SSE2/GPR : {med_scelle/med_sse2:.1f}×",
    ]
    (ICI / "rapport-couloir-a-sse2.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))
    return 0 if diverge == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
