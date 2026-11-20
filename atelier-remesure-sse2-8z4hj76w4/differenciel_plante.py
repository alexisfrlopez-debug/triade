#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""differenciel_plante.py — LA DIFFÉRENTIELLE AUX OCCURRENCES PLANTÉES
(l'instruction 8z4hj76w4 : la re-mesure exige zéro divergence — la
confrontation vague 9 aux motifs aléatoires ABSENTS ne prouve pas la
DÉCOUVERTE d'une occurrence ; ici l'occurrence est PLANTÉE à chaque
alignement)."""
import contextlib
import importlib.util
import io
import pathlib
import random
import sys

import unicorn

REPO = pathlib.Path("/home/z/my-project/depot")
sys.path.insert(0, str(REPO / "loupe"))
ICI = REPO / "atelier-remesure-sse2-8z4hj76w4"
KS = None
import keystone  # noqa: E402
KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def assembler(fichier: pathlib.Path, rva: int):
    lignes = [l.split(";")[0] for l in fichier.read_text(
        encoding="utf-8").splitlines()]
    # résolution d'étiquettes maison (le format de construire_sse2)
    etiquettes = {}
    for _ in range(4):
        adr = rva
        out = []
        for l in lignes:
            l = l.strip()
            if not l:
                continue
            if l.endswith(":") and l.startswith("."):
                etiquettes[l[:-1]] = adr
                continue
            corps = l
            for e, a in etiquettes.items():
                corps = corps.replace(e, hex(a))
            out.append((corps, adr))
            try:
                c, _ = KS.asm(corps, adr)
                adr += len(bytes(c))
            except Exception:
                adr += 6
    octets = b""
    for corps, adr in out:
        for e, a in etiquettes.items():
            corps = corps.replace(e, hex(a))
        c, _ = KS.asm(corps, rva + len(octets))
        octets += bytes(c)
    return octets


def main():
    HE = charger_module("h_ed2", REPO / "loupe" / "harnais_edition.py")
    os_v = HE.OSEdition()
    emul = HE.EmulationEdition(
        os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
        (REPO / "m1" / "selftest.exe").read_bytes(),
        (REPO / "demo" / "demo.exe").read_bytes())
    emul.uc.mem_map(0x500000, 0x21000)
    RVA = 0xCC00
    octets = assembler(ICI / "notation" / "loupe-13-sse2.asm", RVA)
    emul.uc.mem_write(RVA, octets)
    emul.uc.ctl_remove_cache(RVA & ~0xFFF, (RVA + len(octets) + 0xFFF) & ~0xFFF)

    rng = random.Random(20261120)
    divergences = []
    n_tests = 0
    # (1) l'occurrence plantée à CHAQUE alignement p ∈ [0, 64)
    for p in range(0, 64):
        f = bytearray(rng.randrange(256) for _ in range(4096))
        m = bytes(rng.randrange(256) for _ in range(16))
        f[p:p + 16] = m
        f = bytes(f)
        attendu = f.find(m)
        emul.uc.mem_write(0x500000, f)
        emul.uc.mem_write(0x510000, m)
        with contextlib.redirect_stdout(io.StringIO()):
            r = emul.appeler(RVA, {"rcx": 0x500000, "rdx": len(f),
                                  "r8": 0x510000, "r9": len(m)},
                             pile_args=[0])
        n_tests += 1
        if (r["rax"] & (2**64 - 1)) != (attendu & (2**64 - 1)):
            divergences.append(("plante", p, r["rax"], attendu))
    # (2) 500 vecteurs aléatoires AVEC occurrence plantée à position
    #     aléatoire (la couverture statistique)
    for k in range(500):
        n = rng.choice([256, 1000, 4096])
        lm = rng.choice([1, 2, 5, 16, 31, 32])
        p = rng.randrange(max(1, n - lm)) if n > lm else 0
        f = bytearray(rng.randrange(256) for _ in range(n))
        m = bytes(rng.randrange(256) for _ in range(lm))
        f[p:p + lm] = m
        f = bytes(f)
        attendu = f.find(m)
        emul.uc.mem_write(0x500000, f)
        emul.uc.mem_write(0x510000, m)
        with contextlib.redirect_stdout(io.StringIO()):
            r = emul.appeler(RVA, {"rcx": 0x500000, "rdx": len(f),
                                  "r8": 0x510000, "r9": len(m)},
                             pile_args=[0])
        n_tests += 1
        if (r["rax"] & (2**64 - 1)) != (attendu & (2**64 - 1)):
            divergences.append(("stat", k, p, lm, r["rax"], attendu))
    print(f"LA DIFFÉRENTIELLE PLANTÉE : {n_tests} vecteurs "
          f"(64 alignements systématiques + 500 aléatoires)")
    if divergences:
        print(f"  {len(divergences)} DIVERGENCES — les premières :")
        for d in divergences[:12]:
            print("   ", d)
        return 2
    print("  ZÉRO DIVERGENCE — l'occurrence plantée est trouvée à tous "
          "les alignements")
    return 0


if __name__ == "__main__":
    sys.exit(main())
