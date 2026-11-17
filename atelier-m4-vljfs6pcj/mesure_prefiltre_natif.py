#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesure_prefiltre_natif.py — LE PRÉ-FILTRE DIFFÉRENTIEL NATIF MESURÉ
D'ABORD (le plan § 4 : « le coût natif hashlib (md5+sha256) du témoin
196 609 o : n = 5, chronométré isolément ») — l'effet du levier (c) sur
le chemin critique crypto : l'attendu natif (~ms) contre l'émulation
(~10 s). Sortie : preuves/prefiltre-natif.json."""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import statistics
import sys
import time

REPO = pathlib.Path("/tmp/triade-gh")
sys.path.insert(0, str(REPO / "loupe"))
import harnais_noyau as HN          # noqa: E402

SORTIE = REPO / "atelier-m4-vljfs6pcj" / "preuves"


def main() -> int:
    temoins = HN.composer_temoins()
    contenu = temoins["temoin-3f.bin"]
    assert len(contenu) == 3 * 65536 + 1
    mesures = []
    for i in range(5):
        t0 = time.monotonic()
        attendu = hashlib.md5(contenu).digest() \
            + hashlib.sha256(contenu).digest()
        dt = time.monotonic() - t0
        mesures.append(round(dt, 6))
        print(f"  [natif md5+sha256 196 609 o] {dt*1000:.2f} ms")
    attendu_hex = attendu.hex()
    doc = {"mesure": "pré-filtre différentiel natif (md5+sha256 hashlib)",
           "entree": "temoin-3f.bin", "octets": len(contenu),
           "secondes": mesures,
           "mediane_ms": round(statistics.median(mesures) * 1000, 3),
           "panneau_attendu_16": attendu_hex[:16],
           "n": 5}
    SORTIE.mkdir(parents=True, exist_ok=True)
    (SORTIE / "prefiltre-natif.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"médiane : {doc['mediane_ms']} ms — contre ~10 s d'émulation "
          f"(le chemin critique) : le levier (c) vaut ~4 ordres de grandeur")
    return 0


if __name__ == "__main__":
    sys.exit(main())
