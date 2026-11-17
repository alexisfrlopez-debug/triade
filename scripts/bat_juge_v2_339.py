#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bat_juge_v2_339.py — l'en-tête du LANCER-RUN-UNITE02-D210-1CLIC.bat
porté à l'édition v2 (LE JUGE RÉPARÉ), les fins de ligne CRLF conservées
à l'octet près (le format .bat de Windows)."""
import pathlib

BAT = pathlib.Path(
    "/home/z/my-project/download/TRIADE_gui_unite02_d210_v2"
    "/LANCER-RUN-UNITE02-D210-1CLIC.bat")

ANCIEN_1 = (b"rem [le kit kit-gui-1clic-unite02-d210 - l'edition du "
            b"18/11/2026, le\r\n"
            b"rem  correctif T0 grave (EMPREINTES-PIECES-RUN.txt)]\r\n")
NOUVEAU_1 = (b"rem [le kit kit-gui-1clic-unite02-d210 - l'edition v2 du "
             b"18/11/2026 au\r\n"
             b"rem  soir : LE JUGE REPARE - la correction commandee a la "
             b"339, la cause\r\n"
             b"rem  nommee a la 338 (le scenario v1 portait R_JOURNAL = "
             b"0xE4E0,\r\n"
             b"rem  soixante-quatre octets au-dessus de la verite du "
             b"layout 0xE4A0 :\r\n"
             b"rem  la faute au juge, JAMAIS a la piece - le rejeu "
             b"forensique le\r\n"
             b"rem  prouva ; CE kit porte le juge v2 302fa3a1... a la "
             b"verite du\r\n"
             b"rem  layout ; la piece loupe.exe et les quatorze autres "
             b"INCHANGEES,\r\n"
             b"rem  D143) ; le correctif T0 demeure grave "
             b"(EMPREINTES-PIECES-RUN.txt)]\r\n")

ANCIEN_2 = (b"rem BOUTON VERT conduit tout : LE RUN au "
            b"scenario-unite02.py TEL QUEL\r\n"
            b"rem (SA console ecrite AU FIL DE L'EAU, UTF-8 des deux "
            b"cotes du\r\n")
NOUVEAU_2 = (b"rem BOUTON VERT conduit tout : LE RUN au "
             b"scenario-unite02.py v2 (LE\r\n"
             b"rem JUGE REPARE - SA console ecrite AU FIL DE L'EAU, "
             b"UTF-8 des deux\r\n")

b = BAT.read_bytes()
assert ANCIEN_1 in b, "l'en-tête v1 introuvable au bat"
assert ANCIEN_2 in b, "la ligne du run v1 introuvable au bat"
b = b.replace(ANCIEN_1, NOUVEAU_1, 1).replace(ANCIEN_2, NOUVEAU_2, 1)
assert b.count(b"\r\n") == 77 + 6, "le compte de lignes CRLF diverge"
BAT.write_bytes(b)
print(f"[bat] l'en-tête v2 posé ({len(b)} o, "
      f"{b.count(chr(13).encode() + chr(10).encode())} lignes CRLF)")
