#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesure_c_v182.py — LA LISTE FIXE DU BRAS C, chronométrée sur cette
machine, n exécutions (le plan § 4 : le ratio M4 honnête exige les DEUX
bras sur la MÊME machine — la chaîne croisée TRIXIE re-provisionnée aux
versions EXACTES de la campagne : gcc-mingw-w64 14.2.0-19+27+b1,
binutils 2.44-3+12+b1, mingw-w64 12.0.0-5, extraite des .deb SANS ROOT).
Sortie : preuves/c-run{N}.json."""
from __future__ import annotations

import json
import pathlib
import subprocess
import time

REPO = pathlib.Path("/tmp/triade-gh")
ATELIER = REPO / "atelier-cout-boucle-cq01qv1za"
SORTIE = ATELIER / "preuves"
GCC = "/tmp/mingw-try/root/usr/bin/x86_64-w64-mingw32-gcc-posix"
U01C = REPO / "scripts" / "campagne_d204" / "unite-01-C"
U02C = REPO / "scripts" / "campagne_d204" / "unite-02-C"

ETAPES = [
    ("build-gcc-O2-loupe-01",
     f"cd {U01C} && {GCC} -O2 -shared -o epreuves/loupe-01-c.dll "
     f"source/loupe-01-c.c source/loupe-01-c.def"),
    ("suite-tests-c-hash",
     f"cd {U01C} && python3 epreuve_hash_posix.py"),
    ("suite-tests-c-contrat",
     f"cd {U01C}/epreuves && gcc -O2 -o epreuve_posix epreuve_posix.c "
     f"-I. && ./epreuve_posix > observe.txt && python3 compare_epreuve.py"),
    ("controles-binaires-loupe-01",
     f"cd {U01C} && python3 epreuves/controles_binaires.py"),
    ("build-gcc-O2-loupe-02",
     f"cd {REPO} && {GCC} -O2 -shared -o "
     f"scripts/campagne_d204/unite-02-C/epreuves/loupe-02-c.dll "
     f"scripts/campagne_d204/unite-02-C/source/loupe-02-c.c "
     f"scripts/campagne_d204/unite-02-C/source/loupe-02-c.def"),
    ("epreuve-contrat-posix-loupe-02",
     f"cd {U02C}/epreuves && gcc -O2 -I. -o epreuve_posix "
     f"epreuve_posix.c && ./epreuve_posix > sortie-epreuve.txt && "
     f"python3 compare_epreuve.py"),
    ("controles-binaires-loupe-02",
     f"cd {REPO} && python3 scripts/campagne_d204/unite-02-C/epreuves/"
     f"controles_binaires.py"),
]


def une_execution(numero: int) -> int:
    mesures = []
    t_total = time.monotonic()
    code = 0
    print(f"=== BRAS C — exécution {numero} — la liste fixe, cette machine ===")
    for nom, cmd in ETAPES:
        t0 = time.monotonic()
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                           timeout=900)
        dt = time.monotonic() - t0
        code |= r.returncode
        mesures.append({"etape": nom, "secondes": round(dt, 3),
                        "code": r.returncode,
                        "console": (r.stdout + r.stderr)[-4000:]})
        print(f"  [{nom:<32}] {dt:7.3f} s  code {r.returncode}")
    total = time.monotonic() - t_total
    SORTIE.mkdir(parents=True, exist_ok=True)
    (SORTIE / f"c-run{numero}.json").write_text(
        json.dumps({"bras": "C", "run": numero, "total_s": round(total, 3),
                    "etapes": mesures, "code": code},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"=== TOTAL C run {numero} : {total:.1f} s ; code {code}")
    return 0 if code == 0 else 2


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    code = 0
    for i in range(1, n + 1):
        code |= une_execution(i)
    sys.exit(code)
