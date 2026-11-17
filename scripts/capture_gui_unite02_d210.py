#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""capture_gui_unite02_d210.py — LA CAPTURE VISUELLE (l'épreuve visuelle
du LISEZMOI : les onglets capturés ET inspectés — les cadres, les
accents, aucun texte rogné). La fenêtre vive sous Xvfb, quatre onglets
capturés au pixel."""
import pathlib
import sys
import time

KIT = pathlib.Path("/home/z/my-project/download/"
                   "TRIADE_gui_unite02_d210_v1")
sys.path.insert(0, str(KIT))

SORTIE = pathlib.Path("/tmp/render")


def main():
    import triade_run_unite02_d210_gui as G
    from PIL import ImageGrab
    app = G.demarrer(fumee=True)
    racine = app.racine
    deadline = time.time() + 40
    while time.time() < deadline:
        racine.update()
        if getattr(app, "verrou_vert", False):
            break
        time.sleep(0.05)
    for _ in range(40):
        racine.update()
        time.sleep(0.05)
    carnets = [w for w in racine.winfo_children()
               if w.winfo_class() == "TNotebook"]
    carnet = carnets[0]
    for i, nom in enumerate(("verrou", "run", "temoin", "livre")):
        carnet.select(i)
        for _ in range(20):
            racine.update()
            time.sleep(0.03)
        im = ImageGrab.grab(xdisplay=":99")
        chemin = SORTIE / f"gui-d210-{nom}.png"
        im.save(chemin)
        print("capturé :", chemin, im.size)
    racine.destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
