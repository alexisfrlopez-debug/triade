#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REJOUER LES CINQ SONDES DU CONTRAT NOYAU (W28CORRIGE, la vérification de la
correction prompt : « rejouer les cinq sondes et les contrôles négatifs, verdicts
bit-identiques »). Les sondes sont celles que preuve-directe.txt consigne :
(1) E1 (poignée ~0) : retour -4 ; (2) la paire « 45 » : journal[0] = (0x22, 0x45) ;
(3) le compte : 1 ; (4) le curseur : 0x23 ; (5) la fenêtre au 0x22 : 0x45.
La pièce T (loupe.exe, b382e01b…) RECROPÉE INTACTE avant le rejeu."""
import importlib.util
import pathlib
import struct

ICI = pathlib.Path(__file__).resolve().parent
R = ICI.parent
EPR = R / "atelier-w28attr" / "epreuve_t_loupe16.py"

spec = importlib.util.spec_from_file_location("epr", str(EPR))
epr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(epr)   # PieceT / Session — la machinerie de l'atelier

import hashlib
LOUPE = R / "scripts/campagne_d204/unite-16-T-d210/piece/loupe.exe"
sha = hashlib.sha256(LOUPE.read_bytes()).hexdigest()
print(f"loupe.exe sha256 = {sha[:16]}… (l'attendu b382e01b… : "
      f"{'VERT' if sha.startswith('b382e01b') else 'ROUGE'})")

piece = epr.PieceT(LOUPE)

# (1) E1 — la poignée ~0 (hors session), le retour -4 exact (le refus sans session)
s = epr.Session(piece, bytes(63))
struct.pack_into("<Q", s.cadre, 528, (1 << 64) - 1)     # la poignée ~0 — hors session
r = s.frappe(0x30)
barre = bytes(s.saisie[12:12 + 80]).split(b"\x00")[0]
print(f"E1 (poignée ~0) : retour {r} — attendu -4 : {'VERT' if r == -4 else 'ROUGE'}"
      + (f" (la barre « {barre.decode(errors='replace')} »)" if barre else ""))

# (2)+(3)+(4)+(5) — la paire « 45 » au curseur 0x22
s = epr.Session(piece, bytes(63))
s.frappe(0x34)   # '4'
s.frappe(0x35)   # '5'
j = s.journal_lu()
n = s.lit(4096, 4, s.journal)
cur = s.lit(544, 8)
fen = s.cadre[568:568 + 384]
print(f"la paire « 45 » : journal[0] = {j[0] if j else None} — attendu (0x22, 0x45) : "
      f"{'VERT' if j and j[0] == (0x22, 0x45) else 'ROUGE'}")
print(f"le compte : {n} (attendu 1) : {'VERT' if n == 1 else 'ROUGE'}")
print(f"le curseur : {cur:#x} (attendu 0x23) : {'VERT' if cur == 0x23 else 'ROUGE'}")
print(f"la fenêtre au 0x22 : {fen[0x22]:#x} (attendu 0x45) : {'VERT' if fen[0x22] == 0x45 else 'ROUGE'}")
