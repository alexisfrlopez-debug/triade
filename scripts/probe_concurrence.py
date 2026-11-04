#!/usr/bin/env python3
"""probe_concurrence.py — attrape la divergence intermittente de tcp-11 (instrument
temporaire du chantier M6-(c), jamais un livrable)."""
import os
import sys
import threading

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(ICI), "unix"))
import layout as L
import oracle_corpus as OC

cart = OC.Cartouche()
img = OC.Image(os.path.join(os.path.dirname(ICI), "unix", "corpus"), "prive")
NP = 300
echecs = []

def travailleur(marque, k):
    for i in range(NP):
        p = cart._libc.mmap(__import__("ctypes").c_void_p(0), 64,
                            3, 0x22, -1, 0)
        ligne = marque + str(i).encode() + b"\n"
        import ctypes
        ctypes.memmove(p, ligne + b"\0", len(ligne) + 1)
        r = cart.appeler(img.adr(L.A_JOURNAL), [p, len(ligne), 0xFFFFFFFF, p, 0])
        if r["rax"] != len(ligne):
            echecs.append((k, i, r["rax"], len(ligne), r["rsp"] == r["sommet"]))

for essai in range(60):
    echecs.clear()
    with OC.Capture() as cap:
        t1 = threading.Thread(target=travailleur, args=(b"AA ", 1))
        t2 = threading.Thread(target=travailleur, args=(b"BBB ", 2))
        t1.start(); t2.start(); t1.join(); t2.join()
        flux = cap.lire()
    if echecs:
        print(f"essai {essai}: DIVERGENCES = {echecs[:5]}")
    else:
        lignes = [l for l in flux.split(b"\n") if l]
        ok = len(lignes) == 2 * NP
        print(f"essai {essai}: vert ({len(lignes)} lignes entières{'' if ok else ' — FRAGMENTS'})")
