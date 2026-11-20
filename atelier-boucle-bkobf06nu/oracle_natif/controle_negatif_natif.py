#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_negatif_natif.py — LE CONTRÔLE NÉGATIF du régime oracle natif :
un SHIM DE LANCEUR MUTÉ (l'artefact falsifié d'un octet) est attrapé À LA
PREMIÈRE LIGNE de vérification du runner — l'EMPREINTE-DIVERGENTE nommée,
AVANT toute exécution (fail-closed). Vécu au labo sur le MÉCANISME (la
chaîne de vérification du runner), la pièce au rapport."""
from __future__ import annotations

import hashlib
import pathlib
import tempfile

REPO = pathlib.Path("/home/z/my-project/depot")
LOUPE = REPO / "loupe" / "loupe.exe"
ATTENDU = "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1"


def verification_du_runner(chemin: pathlib.Path, attendu: str) -> str:
    """LA PREMIÈRE LIGNE du runner : le hash AVANT toute exécution."""
    h = hashlib.sha256(chemin.read_bytes()).hexdigest()
    if h != attendu:
        return f"EMPREINTE-DIVERGENTE : attendu {attendu[:16]}… rendu {h[:16]}…"
    return "VERT"


def main():
    rapport = []
    # (a) la pièce SANE : VERT
    rapport.append(f"(a) la pièce saine : {verification_du_runner(LOUPE, ATTENDU)}")
    # (b) le shim muté : UN octet changé — attrapé à la première ligne
    octets = bytearray(LOUPE.read_bytes())
    octets[0x151a] ^= 0xFF          # la première ligne de code mutée d'un octet
    with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as f:
        f.write(octets)
        mut = pathlib.Path(f.name)
    refus = verification_du_runner(mut, ATTENDU)
    rapport.append(f"(b) le shim muté (un octet à 0x151a) : {refus}")
    ok = refus.startswith("EMPREINTE-DIVERGENTE")
    if ok:
        verdict = ("VERT — le lanceur muté REFUSÉ à la première ligne, "
                   "AVANT toute exécution (fail-closed)")
    else:
        verdict = "ROUGE — le contrôle négatif a ÉCHOUÉ"
    rapport.append(f"LE VERDICT : {verdict}")
    mut.unlink()
    print("\n".join(rapport))
    (REPO / "atelier-boucle-bkobf06nu" / "oracle_natif" /
     "controle-negatif.txt").write_text("\n".join(rapport) + "\n",
                                         encoding="utf-8")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
