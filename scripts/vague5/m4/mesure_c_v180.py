#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesure_c_v180.py — LA LISTE FIXE DU BRAS C, chronométrée sur cette
machine (le ratio M4 honnête exige les DEUX bras sur la MÊME machine —
la chaîne croisée TRIXIE re-extraite des .deb SANS ROOT, les versions
EXACTES de la campagne : gcc-mingw-w64 14.2.0-19+27+b1, binutils
2.44-3+12+b1, mingw-w64 12.0.0-5).
"""
import pathlib
import subprocess
import time

REPO = pathlib.Path("/tmp/triade-gh")
GCC = "/tmp/mingw-try/root/usr/bin/x86_64-w64-mingw32-gcc-posix"
U01C = REPO / "scripts" / "campagne_d204" / "unite-01-C"
U02C = REPO / "scripts" / "campagne_d204" / "unite-02-C"

ETAPES = [
    ("build-gcc-O2-loupe-01",
     f"cd {U01C} && {GCC} -O2 -shared -o epreuves/loupe-01-c.dll "
     f"source/loupe-01-c.c source/loupe-01-c.def", None),
    ("suite-tests-c-hash",
     f"cd {U01C} && python3 epreuve_hash_posix.py", None),
    ("suite-tests-c-contrat",
     f"cd {U01C}/epreuves && gcc -O2 -o epreuve_posix epreuve_posix.c "
     f"-I. && ./epreuve_posix > observe.txt && python3 compare_epreuve.py",
     None),
    ("controles-binaires-loupe-01",
     f"cd {U01C} && python3 epreuves/controles_binaires.py", None),
    ("build-gcc-O2-loupe-02",
     f"cd {REPO} && {GCC} -O2 -shared -o "
     f"scripts/campagne_d204/unite-02-C/epreuves/loupe-02-c.dll "
     f"scripts/campagne_d204/unite-02-C/source/loupe-02-c.c "
     f"scripts/campagne_d204/unite-02-C/source/loupe-02-c.def", None),
    ("epreuve-contrat-posix-loupe-02",
     f"cd {U02C}/epreuves && gcc -O2 -I. -o epreuve_posix "
     f"epreuve_posix.c && ./epreuve_posix > sortie-epreuve.txt && "
     f"python3 compare_epreuve.py", None),
    ("controles-binaires-loupe-02",
     f"cd {REPO} && python3 scripts/campagne_d204/unite-02-C/epreuves/"
     f"controles_binaires.py", None),
]

total = 0.0
code = 0
for nom, cmd, _ in ETAPES:
    t0 = time.monotonic()
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                       timeout=600)
    dt = time.monotonic() - t0
    total += dt
    code |= r.returncode
    print(f"  [{nom:<32}] {dt:7.3f} s  code {r.returncode}")
print(f"=== TOTAL C : {total:.1f} s ; code {code}")
