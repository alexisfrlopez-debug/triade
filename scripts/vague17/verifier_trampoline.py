#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMÉLIORATION 3 (D258) — LE TRAMPOLINE DE HUIT OCTETS, VÉRIFIÉ AU BUILD.

La promesse « 12 à 16 octets atomiques par écriture alignée » est fausse
(D253) : un magasin naturel n'est atomique que jusqu'à huit octets. La règle
de build devient donc celle-ci, vérifiable sur les octets :

  OK    un mot de 8 octets au plus, commençant par E9 (jmp rel32) + NOP de
        remplissage, ALIGNÉ sur 8 — la forme courte ;
  OK    une forme absolue de 12 octets (48 B8 imm64 FF E0) UNIQUEMENT si la
        publication passe par LOCK CMPXCHG16B (CPUID présent) et que
        l'emplacement est aligné sur 16 ;
  REFUS tout autre cas, nommé.

Usage : `verifier(stub: bytes, adresse: int, cpuid_cmpxchg16b: bool)` ; le
script lance son autotest (7 cas) et rend 0 si les sept verdicts sont ceux
attendus.
"""
import sys


class Refus(Exception):
    pass


def verifier(stub: bytes, adresse: int, cpuid_cmpxchg16b: bool = False) -> str:
    if not stub:
        raise Refus("TRAMPOLINE-VIDE")
    if len(stub) <= 8:
        if stub[0] != 0xE9:
            raise Refus("FORME-INCONNUE")
        if any(o != 0x90 for o in stub[5:]):
            raise Refus("REMPLISSAGE-NON-NOP")
        if adresse % 8 != 0:
            raise Refus("NON-ALIGNE-8")
        return "MOT-8-OCTETS"
    if len(stub) == 12 and stub[:2] == b"\x48\xb8" and stub[10:] == b"\xff\xe0":
        if not cpuid_cmpxchg16b:
            raise Refus("FORME-ABSOLUE-SANS-CMPXCHG16B")
        if adresse % 16 != 0:
            raise Refus("NON-ALIGNE-16")
        return "FORME-ABSOLUE-CMPXCHG16B"
    raise Refus("LONGUEUR-NON-ATOMIQUE")


def autotest():
    nop = b"\x90" * 3
    court = b"\xe9\x10\x00\x00\x00" + nop            # 8 octets
    long_ = b"\x48\xb8" + b"\x11" * 8 + b"\xff\xe0"  # 12 octets
    cas = [
        ("mot de 8 octets aligné", court, 0x1000, False, "MOT-8-OCTETS"),
        ("mot de 8 octets non aligné", court, 0x1002, False, "NON-ALIGNE-8"),
        ("remplissage non NOP", b"\xe9\x10\x00\x00\x00\xcc\x90\x90", 0x1000, False, "REMPLISSAGE-NON-NOP"),
        ("12 octets au magasin simple", long_, 0x1000, False, "FORME-ABSOLUE-SANS-CMPXCHG16B"),
        ("12 octets CMPXCHG16B aligné 16", long_, 0x1000, True, "FORME-ABSOLUE-CMPXCHG16B"),
        ("12 octets CMPXCHG16B non aligné 16", long_, 0x1008, True, "NON-ALIGNE-16"),
        ("16 octets quelconques", b"\x90" * 16, 0x1000, True, "LONGUEUR-NON-ATOMIQUE"),
    ]
    verts = 0
    print("=" * 78)
    print("AMÉLIORATION 3 — LE TRAMPOLINE VÉRIFIÉ AU BUILD (D258)")
    print("=" * 78)
    for nom, stub, adr, cpuid, attendu in cas:
        try:
            rendu = verifier(stub, adr, cpuid)
        except Refus as e:
            rendu = e.args[0]
        ok = rendu == attendu
        verts += 1 if ok else 0
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom} → {rendu}")
    print(f"{verts}/{len(cas)}")
    return 0 if verts == len(cas) else 3


if __name__ == "__main__":
    sys.exit(autotest())
