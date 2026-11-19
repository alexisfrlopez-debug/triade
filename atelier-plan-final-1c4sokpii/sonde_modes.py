#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonde_modes.py — LA SONDE des modes ALLER/CHERCHER (v2) : la BARRE est à
ECRAN+2000, 2 × 160 o en UTF-16-LE (la disposition I1 de loupe-09) ; le
commit arrive par WM_CHAR 0x0D (Enter génère le caractère), l'annulation par
0x1B. La sonde lit la barre de chaque scénario — une exploration, jamais une
mesure."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


HE = charger_module("h_edition_sonde", REPO / "loupe" / "harnais_edition.py")
HN = charger_module("h_noyau_sonde", REPO / "loupe" / "harnais_noyau.py")
LL = HN.L

BASE = [
    (0x770001, 5, 0, (440 << 16) | 640),      # WM_SIZE
    (0x770001, 0x0F, 0, 0),                   # WM_PAINT
]

CANDIDATS = {
    "la barre au repos": [],
    "ALLER-vide (F5, RETOUR)": [
        (0x770001, 0x100, 0x74, 0),           # WM_KEYDOWN F5 → le mode
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x102, 0x0D, 0),           # WM_CHAR RETOUR → commit VIDE
        (0x770001, 0x0F, 0, 0),
    ],
    "ALLER-hors-bornes (F5, FFFFFFFFFF, RETOUR)": [
        (0x770001, 0x100, 0x74, 0),           # F5
        (0x770001, 0x0F, 0, 0),
        *[(0x770001, 0x102, 0x46, 0)] * 8,    # 'F' × 8
        (0x770001, 0x102, 0x0D, 0),           # RETOUR → hors bornes
        (0x770001, 0x0F, 0, 0),
    ],
    "ALLER-saut (F5, a9, RETOUR)": [
        (0x770001, 0x100, 0x74, 0),
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x102, 0x61, 0),           # 'a'
        (0x770001, 0x102, 0x39, 0),           # '9'
        (0x770001, 0x102, 0x0D, 0),           # RETOUR → le saut 0xa9
        (0x770001, 0x0F, 0, 0),
    ],
    "ALLER-annulation (F5, a, ÉCHAP)": [
        (0x770001, 0x100, 0x74, 0),
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x102, 0x61, 0),
        (0x770001, 0x102, 0x1B, 0),           # ÉCHAP → l'annulation propre
        (0x770001, 0x0F, 0, 0),
    ],
    "CHERCHER (Ctrl+F 4D RETOUR, F3)": [
        (0x770001, 0x102, 0x06, 0),           # Ctrl+F (WM_CHAR 0x06)
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x102, 0x34, 0),           # '4'
        (0x770001, 0x102, 0x44, 0),           # 'D'
        (0x770001, 0x102, 0x0D, 0),           # RETOUR → le motif « 4D »
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x100, 0x72, 0),           # F3 → l'occurrence suivante
        (0x770001, 0x0F, 0, 0),
        (0x770001, 0x100, 0x72, 0),           # F3 encore
        (0x770001, 0x0F, 0, 0),
    ],
}


def barre(emul):
    brut = bytes(emul.uc.mem_read(LL.R_ECRAN + 2000, 320))
    return [brut[i * 160:(i + 1) * 160].decode("utf-16-le",
                                                errors="replace").rstrip("\x00")
            for i in range(2)]


def main():
    for nom, seq in CANDIDATS.items():
        os_v = HE.OSEdition()
        os_v.declarer("temoin-sonde.bin", HE.FichierEditable(contenu=bytes(
            (i * 7 + 3) % 256 for i in range(2000))))
        emul = HE.EmulationEdition(
            os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
            (REPO / "m1" / "selftest.exe").read_bytes(),
            (REPO / "demo" / "demo.exe").read_bytes())
        with contextlib.redirect_stdout(io.StringIO()):
            r = emul.appeler_winmain("loupe.exe temoin-sonde.bin",
                                     messages=BASE + seq)
        print(f"═══ {nom} ═══ exit={r.get('exit_code')} crash={r.get('crash')}")
        for ligne in barre(emul):
            if ligne.strip():
                print(f"   barre | {ligne}")
    print("la sonde finie")


if __name__ == "__main__":
    main()
