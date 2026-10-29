#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE D52 — construction de la sonde superviseur-zero.exe.

Principe : prendre les octets EXACTS de la livraison terrain.3 (md5
40b2f350...) et mettre a ZERO tout le contenu de la section .blob
(fichier 0x6400..0xF200). Le PE (en-tetes, .text, .rdata, .data, .text2,
.rsrc, imports) reste STRICTEMENT identique.

La chaine de demarrage ne lit jamais .blob (prouve par emulation
forensique D52h/D52i : aucun acces .blob avant la boucle de messages).
Cette sonde sert donc a discriminer sur le terrain :

  - si superviseur-zero.exe S'EXECUTE (fenetre) alors que
    superviseur-terrain3.exe crashe  -> le declencheur est le CONTENU
    de .blob (proxy.exe embarque + jetons) = interference antivirus
    (Defender a deja flagge proxy.exe en Wacatac.C!ml le 27/10 12:55) ;

  - si superviseur-zero.exe crashe aussi -> le declencheur est dans le
    reste de l'image ou l'environnement, .blob est innocent.
"""

import hashlib
import pathlib
import struct

SRC = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur.exe")
DST = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur-zero.exe")

data = bytearray(SRC.read_bytes())

# localiser .blob par la table des sections (verification d'independance)
e = struct.unpack_from("<I", data, 0x3C)[0]
coff = e + 4
_, nsec, _, _, _, opt_sz, _ = struct.unpack_from("<HHIIIHH", data, coff)
so = coff + 20 + opt_sz
blob = None
for i in range(nsec):
    o = so + 40 * i
    nom = bytes(data[o:o + 8]).rstrip(b"\x00").decode()
    vs, va, rs, ra = struct.unpack_from("<IIII", data, o + 8)
    if nom == ".blob":
        blob = (va, vs, ra, rs)
        break
assert blob, "section .blob introuvable"
va, vs, ra, rs = blob
print(f".blob : VA={va:#x} VS={vs:#x} RAW={ra:#x} RS={rs:#x}")
assert ra == 0x6400 and rs == 0x8E00, "layout .blob inattendu"

n = 0
for i in range(ra, ra + rs):
    if data[i] != 0:
        data[i] = 0
        n += 1
print(f"{n} octets non nuls mis a zero dans .blob")

DST.write_bytes(bytes(data))
md5 = hashlib.md5(bytes(data)).hexdigest()
src_md5 = hashlib.md5(SRC.read_bytes()).hexdigest()
print(f"source  : {SRC}  md5 {src_md5}")
print(f"sonde   : {DST}  md5 {md5}")
print(f"taille  : {len(data)} octets (identique)")

# controles : tout hors .blob doit etre identique
src = SRC.read_bytes()
diffs = [i for i in range(len(src))
         if src[i] != data[i] and not (ra <= i < ra + rs)]
print(f"octets modifies hors .blob : {len(diffs)} (attendu 0)")
assert not diffs

# l'image reste chargeable : re-audit minimal (SizeOfHeaders, entree, dirs)
opt = coff + 20
soh = struct.unpack_from("<I", data, opt + 60)[0]
fin_reelle = e + 4 + 20 + opt_sz + nsec * 40
assert soh >= fin_reelle, "SizeOfHeaders casse"
print(f"audit : SizeOfHeaders {soh:#x} >= fin table {fin_reelle:#x} OK")
print("sonde superviseur-zero.exe PRETE")
