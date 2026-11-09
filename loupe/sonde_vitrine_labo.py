#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonde_vitrine_labo.py — LA VITRINE REJOUÉE AU LABO SUR LE FLOT RÉEL.

L'ÉMULATION COMPLÈTE : EmulationEdition (les 18 notations posées, l'IAT à
33 feuilles vivantes, le disque saisissable, la mort de la fenêtre).

LE FLOT RÉEL : la naissance (GETMINMAXINFO → NCCREATE → NCCALCSIZE →
CREATE → WINDOWPOS×2 → MOVE → SIZE → SHOWWINDOW → ACTIVATE×3 → SETFOCUS
→ ERASEBKGND → SETCURSOR → PAINT ×2) puis la vie (les flèches, la
molette, les scrolls) — LA VITRINE VIDE (double-clic) ET AVEC FICHIER.

À CHAQUE FAUTE : le tampon circulaire des 24 derniers appels des nôtres.
La sonde ne modifie RIEN : elle NOMME.
"""

import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
TRIADE = os.path.dirname(ICI)
sys.path.insert(0, ICI)

import harnais_edition as HE              # noqa: E402
import harnais_rendu as HR               # noqa: E402
import harnais_noyau as HN               # noqa: E402
import layout as L                       # noqa: E402
from unicorn import UC_HOOK_MEM_UNMAPPED  # noqa: E402
from unicorn.x86_const import UC_X86_REG_RIP  # noqa: E402

BLOCS = {
    0x1100: "libc-01 memcpy (M1 scellé)", 0x1180: "libc-02 memcmp (M1 scellé)",
    0x13C0: "libc-07 memset (M1 scellé)", 0x15C0: "win-03 boucle (démo scellé)",
    0xC000: "tls13-01 sha-init (M9 scellé)", 0xC080: "tls13-02 sha-comprimer",
    0xC240: "tls13-03 sha-absorber", 0xC300: "tls13-04 sha-finaliser",
    0x4040: "loupe-04 cadre", 0x4080: "loupe-01 ouvrir",
    0x4240: "loupe-02 lire", 0x4380: "loupe-03 fermer",
    0x4440: "loupe-05 sha256", 0x4700: "loupe-06 md5",
    0x4940: "loupe-07 cumul", 0x49C0: "loupe-08 ligne",
    0x4B00: "loupe-10 peinture", 0x5180: "loupe-11 défilement",
    0x5400: "loupe-14 suivant", 0x5800: "loupe-12 aller",
    0x5C00: "loupe-09 écran (WinMain)", 0x5DCB: "loupe-09 la procédure",
    0x6029: "loupe-09 .monter", 0x6046: "loupe-09 .message",
    0x6080: "loupe-15 curseur", 0x6240: "loupe-16 saisie",
    0x6500: "loupe-17 sauver", 0x6740: "loupe-18 quitter",
}


def nom_de(rip: int) -> str:
    for base, nom in sorted(BLOCS.items()):
        if base <= rip < base + 0x400:
            return f"{nom} @{rip:#x}"
    return f"@{rip:#x} (hors carte)"


FLOT_NAISSANCE = [
    (0x770001, 0x0024, 0, 0x710200),      # WM_GETMINMAXINFO
    (0x770001, 0x0081, 0, 0x710400),      # WM_NCCREATE
    (0x770001, 0x0083, 1, 0x710600),      # WM_NCCALCSIZE
    (0x770001, 0x0001, 0, 0x710800),      # WM_CREATE
    (0x770001, 0x0046, 0, 0x710A00),      # WM_WINDOWPOSCHANGING
    (0x770001, 0x0047, 0, 0x710A00),      # WM_WINDOWPOSCHANGED
    (0x770001, 0x0003, 0, 0x00F40028),    # WM_MOVE
    (0x770001, 0x0005, 0, (440 << 16) | 640),  # WM_SIZE
    (0x770001, 0x0018, 1, 0),             # WM_SHOWWINDOW
    (0x770001, 0x0006, 1, 0),             # WM_ACTIVATE
    (0x770001, 0x001C, 1, 0),             # WM_ACTIVATEAPP
    (0x770001, 0x0086, 0, 0),             # WM_NCACTIVATE
    (0x770001, 0x0007, 0, 0),             # WM_SETFOCUS
    (0x770001, 0x0014, 0, 0x710C00),      # WM_ERASEBKGND
    (0x770001, 0x0020, 0, 0x02040004),    # WM_SETCURSOR
    (0x770001, 0x000F, 0, 0),             # WM_PAINT
    (0x770001, 0x000F, 0, 0),             # WM_PAINT (repaint)
]
FLOT_VIE = [
    (0x770001, 0x0100, 0x28, 0),          # VK_RIGHT  → loupe-15
    (0x770001, 0x0100, 0x26, 0),          # VK_UP     → loupe-15
    (0x770001, 0x0100, 0x22, 0),          # VK_NEXT   → loupe-15
    (0x770001, 0x020A, 0xFF880000, 0),    # WM_MOUSEWHEEL → loupe-11
    (0x770001, 0x0115, 1, 0),             # WM_VSCROLL LINEDOWN → loupe-11
    (0x770001, 0x0115, 5, 0),             # WM_VSCROLL THUMBTRACK
    (0x770001, 0x0100, 0x74, 0),          # VK_F5     → loupe-12
    (0x770001, 0x0102, 0x31, 0),          # « 1 »     → loupe-12
    (0x770001, 0x0102, 0x0d, 0),          # retour    → commit
    (0x770001, 0x0100, 0x72, 0),          # VK_F3     → loupe-14
    (0x770001, 0x0010, 0, 0),             # WM_CLOSE  → loupe-18
    (0x770001, 0x0002, 0, 0),             # WM_DESTROY → loupe-18
]


def main() -> int:
    print("=== LA SONDE VITRINE : LE FLOT RÉEL SUR L'ÉMULATION COMPLÈTE "
          "(dev.4) ===")
    temoins = HN.composer_temoins()
    donnees_m9 = open(os.path.join(TRIADE, HN.SCELLE_M9), "rb").read()
    donnees_m1 = open(os.path.join(TRIADE, HN.SCELLE_M1), "rb").read()
    donnees_demo = open(os.path.join(TRIADE, "demo", "demo.exe"), "rb").read()
    os_v = HE.OSEdition()
    emul = HE.EmulationEdition(os_v, donnees_m9, donnees_m1, donnees_demo)

    piste: list[str] = []

    def nomme_crash(uc, acces, adresse, taille, valeur, eh):
        rip = uc.reg_read(UC_X86_REG_RIP)
        print(f"    !! FAUTE UC {acces} @{adresse:#x} taille {taille} — "
              f"rip {nom_de(rip)}")
        print("       LES 24 DERNIERS APPELS DES NÔTRES :")
        for ligne in piste[-24:]:
            print(f"         {ligne}")

    def trace(uc, adresse, taille, donnees):
        if 0x1000 <= adresse < 0x8000:
            piste.append(nom_de(adresse))
            if len(piste) > 600:
                del piste[:300]

    emul.uc.hook_add(UC_HOOK_MEM_UNMAPPED, nomme_crash)
    emul.uc.hook_add(HN.UC_HOOK_CODE, trace)

    def relance():
        emul.gui.reset()
        nonlocal os_v
        os_v = HE.OSEdition()
        emul.__init__(os_v, donnees_m9, donnees_m1, donnees_demo)
        emul.uc.hook_add(UC_HOOK_MEM_UNMAPPED, nomme_crash)
        emul.uc.hook_add(HN.UC_HOOK_CODE, trace)
        return emul.gui

    # --- 1. LA VITRINE VIDE SUR LE FLOT RÉEL ----------------------------------
    print("\n[1] LA VITRINE VIDE (double-clic) — LE FLOT RÉEL COMPLET")
    gui = relance()
    r = emul.appeler_winmain("loupe.exe", FLOT_NAISSANCE + FLOT_VIE)
    print(f"    WinMain : exit_code {r['exit_code']}, crash {r.get('crash')}, "
          f"pile {r.get('pile_equilibree')}")
    print(f"    GetMessageW {gui.compteurs['GetMessageW']} · Dispatch "
          f"{gui.compteurs['DispatchMessageW']} · DefWindowProc "
          f"{gui.appels_defproc} · BeginPaint {gui.compteurs['BeginPaint']} · "
          f"boîtes {len(gui.boites)} · fenêtre détruite "
          f"{getattr(gui, 'fenetre_detruite', '?')}")

    # --- 2. LA VITRINE AVEC FICHIER --------------------------------------------
    print("\n[2] LA VITRINE AVEC FICHIER — « loupe.exe temoin-384.bin »")
    gui = relance()
    os_v.declarer("temoin-384.bin", HE.FichierEditable(
        contenu=temoins["temoin-384.bin"]))
    r = emul.appeler_winmain("loupe.exe temoin-384.bin",
                             FLOT_NAISSANCE + FLOT_VIE)
    print(f"    WinMain : exit_code {r['exit_code']}, crash {r.get('crash')}, "
          f"pile {r.get('pile_equilibree')}")
    poignee = emul.u64(528)
    print(f"    la session : poignée {poignee:#x} "
          f"({'NÉE' if poignee not in (0, 0xFFFFFFFFFFFFFFFF) else 'MORTE'}), "
          f"taille {emul.u64(520)}")
    print(f"    CreateFileW {os_v.compteurs['CreateFileW']} · ReadFile "
          f"{os_v.compteurs['ReadFile']} · WriteFile "
          f"{os_v.compteurs['WriteFile']} · journal gle "
          f"{os_v.journal_gle[-3:]}")
    print("\n=== FIN DE LA SONDE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
