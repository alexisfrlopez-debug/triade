#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""falsifie_d132_v10.py — l'autre côté de la preuve D132 : sur le code
v1.0 (git HEAD, AVANT le correctif de disposition), la MESURE de la
fumée doit voir le défaut du terrain — des boutons « Parcourir… »
empilés en colonne à droite, SANS champ aligné sur leur ligne.

PASS si le défaut v1.0 est observé (au moins un bouton sans Entry dont
le centre vertical partage le sien) ; ÉCHEC si le v1.0 se comportait
déjà comme le v1.1 (la fumée D132 ne falsifierait alors rien).

Lancement : DISPLAY=:99 python3 scripts/falsifie_d132_v10.py
"""

import importlib.util
import os
import subprocess
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOLERANCE = 3


def main():
    if not os.environ.get("DISPLAY"):
        print("[falsifie D132] ÉCHEC — aucune variable DISPLAY (Xvfb requis)")
        return 1
    bac = tempfile.mkdtemp(prefix="falsifie-d132-")
    chemin = os.path.join(bac, "migration_cf3_gui_v10.py")
    source = subprocess.run(
        ["git", "-C", RACINE, "show", "HEAD:v06/migration_cf3_gui.py"],
        capture_output=True, text=True, check=True).stdout
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(source)

    spec = importlib.util.spec_from_file_location(
        "migration_cf3_gui_v10", chemin)
    gui = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gui)

    import tkinter as tk
    from tkinter import ttk
    print(f"[falsifie D132] code v1.0 chargé : {gui.VERSION_GUI}")
    racine = tk.Tk()
    app = gui.Application(racine)
    try:
        racine.update_idletasks()
        racine.update()
        cahiers = [w for w in racine.winfo_children()
                   if isinstance(w, ttk.Notebook)][0]
        cahiers.select(0)
        racine.update()
        page = racine.nametowidget(cahiers.tabs()[0])

        def descendants(classe):
            trouves, pile = [], [page]
            while pile:
                w = pile.pop()
                for enfant in w.winfo_children():
                    if isinstance(enfant, classe):
                        trouves.append(enfant)
                    pile.append(enfant)
            return trouves

        entrees = descendants(ttk.Entry)
        boutons = [b for b in descendants(ttk.Button)
                   if (b.cget("text") or "") == "Parcourir…"]
        non_alignes = []
        for bouton in boutons:
            centre_b = bouton.winfo_y() + bouton.winfo_height() / 2
            if not any(abs(e.winfo_y() + e.winfo_height() / 2 - centre_b)
                       <= TOLERANCE for e in entrees):
                non_alignes.append(f"y={bouton.winfo_y()}")
        print(f"[falsifie D132] onglet Migrer : {len(boutons)} bouton(s) "
              f"« Parcourir… », {len(non_alignes)} SANS champ aligné "
              f"(le défaut du terrain)")
        ok = bool(boutons) and len(non_alignes) == len(boutons)
        print(f"[falsifie D132] {'PASS' if ok else 'ÉCHEC'} — le défaut "
              f"v1.0 {'est' if ok else 'n est PAS'} visible : la mesure "
              f"D132 falsifie bien les deux côtés")
        return 0 if ok else 1
    finally:
        racine.destroy()


if __name__ == "__main__":
    sys.exit(main())
