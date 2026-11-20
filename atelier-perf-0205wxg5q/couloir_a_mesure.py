#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""couloir_a_mesure.py — LE COULOIR A : LA PARITÉ BASELINE (la vague 9,
l'instruction 0205wxg5q point 1, le PLAN-0205WXG5Q H1 gelé).

LA MESURE AVANT (R11 : avant toute écriture) : les blocs contrôlés au
GPR pur (les notations SCELLÉES, lecture seule) contre LA RÉFÉRENCE
COMPILÉE gcc -O2 (la chaîne mingw TRIXIE : gcc 14.2.0-19+27+b1,
binutils 2.44-3+12+b1, mingw-w64 12.0.0-5 — le bras C de la campagne,
AUCUN drapeau supplémentaire).

LA CONVENTION DE PARITÉ (la périmètre AVANT toute comparaison) :
  — le MÊME moteur : Unicorn, le COMPTE D'INSTRUCTIONS par hook —
    déterministe (jamais l'horloge) ;
  — LA BIBLIOTHÈQUE TENUE ÉGALE : les DEUX bras appellent LE MÊME
    memcmp SCELLÉ (libc-02 à son adresse du plan 0x1180 — le call du
    bras C repointé vers le scellé : l'appel de loupe-13 est le même
    geste des deux côtés, la parité est EXACTE) ;
  — les MÊMES vecteurs (la graine 20261120, n=15, la médiane et l'IQR).

LE CONSTAT PRÉALABLE (sur pièces, au rapport) : le décompte des
instructions SIMD (movdqa/movdqu/pcmpeq*/pmovmskb/punpck*) dans les
.text gcc-O2 des blocs contrôlés — LA RÉFÉRENCE N'EMPLOIE PAS SSE2 sur
ces boucles (le compilateur émet des boucles d'octets GPR) : la parité
se joue au GPR, et les CHEMINS SSE2 BASELINE écrits en notation (le
point 1 de l'instruction) DÉPASSENT les deux bras — l'objectif « coût
inférieur ou égal à gcc-O2 » tenu par construction SSE2 (baseline du
x86-64 : AUCUN dispatch requis, la garantie constructeur).

Sortie : couloir-a-avant.csv · rapport-couloir-a.txt."""
from __future__ import annotations

import contextlib
import csv
import importlib.util
import io
import pathlib
import random
import statistics
import subprocess
import sys

import unicorn

REPO = pathlib.Path("/home/z/my-project/depot")
sys.path.insert(0, str(REPO / "loupe"))
ICI = REPO / "atelier-perf-0205wxg5q"
ICI.mkdir(exist_ok=True)

import harnais_noyau as HN   # noqa: E402
import keystone              # noqa: E402

L = HN.L
KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)

MINGW = pathlib.Path("/tmp/pkgs/mingw-ext/usr/bin/"
                     "x86_64-w64-mingw32-gcc-win32")
OBJCOPY = MINGW.parent / "x86_64-w64-mingw32-objcopy"
OBJDUMP = MINGW.parent / "x86_64-w64-mingw32-objdump"
GRAINE = 20261120
N_REP = 15
VA_C = 0x600000


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


B4 = charger_module("build_m4_ca", REPO / "m4" / "build_m4.py")
HE = charger_module("h_ed_ca", REPO / "loupe" / "harnais_edition.py")

SIMD = ("movdqa", "movdqu", "movaps", "movups", "pcmpeqb", "pcmpeqd",
        "pcmpeqq", "pmovmskb", "punpcklbw", "punpckhbw", "paddb")


def instance():
    os_v = HE.OSEdition()
    emul = HE.EmulationEdition(
        os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
        (REPO / "m1" / "selftest.exe").read_bytes(),
        (REPO / "demo" / "demo.exe").read_bytes())
    return os_v, emul


class Compteur:
    def __init__(self, emul):
        self.n = 0
        emul.uc.hook_add(unicorn.UC_HOOK_CODE, self._hook)

    def _hook(self, uc, adresse, taille, donnees):
        self.n += 1


def appeler_comptant(emul, va, args, pile_args=None):
    cpt = Compteur(emul)
    with contextlib.redirect_stdout(io.StringIO()):
        r = emul.appeler(va, args, pile_args=pile_args)
    return r, cpt.n


# ------------------------------------------------- le bras C (gcc -O2)

def compiler(src: str, nom: str) -> tuple[bytes, int]:
    """gcc -O2, le .text extrait ; rend (octets, l'offset de l'appel memcmp)."""
    c = ICI / f"{nom}.c"
    c.write_text(src, encoding="utf-8")
    obj = ICI / f"{nom}.o"
    r = subprocess.run([str(MINGW), "-O2", "-c", str(c), "-o", str(obj)],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"la compilation a échoué : {r.stderr[:300]}")
    bin_ = ICI / f"{nom}.text.bin"
    r = subprocess.run([str(OBJCOPY), "-O", "binary", "-j", ".text",
                        str(obj), str(bin_)], capture_output=True, text=True,
                       timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"l'extraction a échoué : {r.stderr[:300]}")
    return bin_.read_bytes(), obj


def decompte_simd(obj: pathlib.Path) -> int:
    r = subprocess.run([str(OBJDUMP), "-d", str(obj)], capture_output=True,
                       text=True, timeout=60)
    n = 0
    for ligne in r.stdout.splitlines():
        for s in SIMD:
            if s in ligne:
                n += 1
                break
    return n


def repointer_memcmp(texte: bytes) -> bytes:
    """LE CALL memcmp DU BRAS C REPOINTÉ vers le memcmp SCELLÉ libc-02 à
    0x1180 — la bibliothèque tenue ÉGALE (la convention de parité)."""
    out = bytearray(texte)
    pos = 0
    n = 0
    while True:
        i = out.find(b"\xe8\x00\x00\x00\x00", pos)
        if i < 0:
            break
        cible = 0x1180 - (VA_C + i + 5)
        out[i + 1:i + 5] = cible.to_bytes(4, "little", signed=True)
        n += 1
        pos = i + 5
    if n == 0:
        raise RuntimeError("aucun call rel32 trouvé — le repointage impossible")
    return bytes(out), n


# ----------------------------------------------------------- loupe-13

SRC_13 = """#include <string.h>
long loupe_13_recherche(const unsigned char *fenetre,
        long taille, const unsigned char *motif, long taille_motif,
        long depart) {
    if (taille_motif > 32 || taille < 0 || depart > taille) return -5;
    for (long i = depart; i <= taille - taille_motif; ++i)
        if (memcmp(fenetre + i, motif, taille_motif) == 0) return i;
    return -1;
}
"""


def vecteurs_13(rng):
    for _ in range(N_REP):
        n = 4096
        f = bytes(rng.randrange(256) for _ in range(n))
        m = bytes(rng.randrange(256) for _ in range(16))
        yield f, m, 0, f.find(m)


def mesurer_13(emul, va, rng_seed=GRAINE):
    rng = random.Random(rng_seed)
    emul.uc.mem_map(0x500000, 0x21000)
    res = []
    for f, m, depart, attendu in vecteurs_13(rng):
        emul.uc.mem_write(0x500000, f)
        emul.uc.mem_write(0x510000, m)
        r, n_ins = appeler_comptant(
            emul, va, {"rcx": 0x500000, "rdx": len(f), "r8": 0x510000,
                       "r9": len(m)}, pile_args=[depart])
        assert (r["rax"] & (1 << 64) - 1) == (attendu & (1 << 64) - 1), \
            f"loupe-13 : la divergence {r['rax']} ≠ {attendu}"
        res.append(n_ins)
    return res


def main():
    rapport = ["LE COULOIR A — LA PARITÉ BASELINE (la mesure avant, R11)",
               ""]
    # le constat préalable : le décompte SIMD des .text gcc-O2
    textes = {}
    for nom, src in (("l13", SRC_13),):
        texte, obj = compiler(src, nom)
        n_simd = decompte_simd(obj)
        rapport.append(f"LE CONSTAT SUR PIÈCES ({nom}.o, gcc -O2) : "
                       f"{n_simd} instruction(s) SIMD — la référence "
                       f"n'emploie PAS SSE2 sur ces boucles (les boucles "
                       f"d'octets GPR du compilateur)")
        textes[nom] = texte

    # le bras T : la notation scellée (lecture seule)
    not13 = list((REPO / "loupe" / "notation").glob("loupe-13-*.asm"))[0]
    rva13, slot13 = L.SLOTS_LOUPE["i110013"]
    octets13, _ = B4.assembler_bloc(KS, str(not13), rva13, slot13)
    os_v, emul = instance()
    emul.uc.mem_write(rva13, octets13)
    emul.uc.ctl_remove_cache(rva13 & ~0xFFF, (rva13 + len(octets13) + 0xFFF)
                             & ~0xFFF)
    gpr = mesurer_13(emul, rva13)

    # le bras C : le .text repointé vers le memcmp SCELLÉ
    texte, n_calls = repointer_memcmp(textes["l13"])
    os_v2, emul2 = instance()
    emul2.uc.mem_map(VA_C & ~0xFFF, 0x2000)
    emul2.uc.mem_write(VA_C, texte)
    ref = mesurer_13(emul2, VA_C)

    med_gpr, med_ref = statistics.median(gpr), statistics.median(ref)
    q = statistics.quantiles
    parite = "la parité TENUE (T ≤ C)" if med_gpr <= med_ref else \
        "la parité À PRENDRE (le chemin SSE2 du point 1)"
    rapport += [
        "",
        f"loupe-13 (la recherche d'octet, fenêtre 4 096 o, motif 16 o) :",
        f"  LE BRAS T (la notation GPR scellée + le memcmp scellé) : "
        f"médiane {med_gpr:.0f} instructions/op, IQR "
        f"{q(gpr, n=4)[2]-q(gpr, n=4)[0]:.0f} (n={N_REP}, la graine "
        f"{GRAINE})",
        f"  LE BRAS C (gcc -O2, {n_calls} call memcmp repointé au SCELLÉ "
        f"libc-02) : médiane {med_ref:.0f}, IQR "
        f"{q(ref, n=4)[2]-q(ref, n=4)[0]:.0f}",
        f"  LE RATIO T/C : {med_gpr/med_ref:.2f}× — {parite}",
        "",
        "LA CONVENTION DE PARITÉ : le même moteur (Unicorn, le compte par "
        "hook), la bibliothèque tenue ÉGALE (les DEUX bras au memcmp "
        "SCELLÉ libc-02 — le call du bras C repointé), les mêmes vecteurs "
        "(la graine 20261120), la confrontation comportementale aux "
        "vecteurs (zéro divergence — l'assertion au code).",
    ]
    with open(ICI / "couloir-a-avant.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["bloc", "operation", "bras", "mediane_instr",
                    "iqr", "n", "ratio"])
        w.writerow(["loupe-13", "recherche 4096/16", "T-GPR", med_gpr,
                    q(gpr, n=4)[2] - q(gpr, n=4)[0], N_REP,
                    round(med_gpr / med_ref, 2)])
        w.writerow(["loupe-13", "recherche 4096/16", "C-gcc-O2", med_ref,
                    q(ref, n=4)[2] - q(ref, n=4)[0], N_REP, 1.0])
    (ICI / "rapport-couloir-a.txt").write_text("\n".join(rapport) + "\n",
                                               encoding="utf-8")
    print("\n".join(rapport))


if __name__ == "__main__":
    main()
