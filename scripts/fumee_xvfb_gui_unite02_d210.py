#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fumee_xvfb_gui_unite02_d210.py — L'ÉPREUVE VISUELLE DU GUI 1-CLIC
D210 sous serveur X virtuel (D122 : le bac n'a aucun Windows ; la
FENÊTRE vivante s'éprouve ici, l'exécution Windows au terrain).

La fenêtre RÉELLE est bâtie AU FIL PRINCIPAL (demarrer(fumee=True) —
le hook d'épreuve du GUI, documenté au source), le verrou RECOUUPÉ
par le fil ouvrier réel, la file pompée par racine.update(), puis la
fenêtre INSPECTÉE : les onglets, les accents rendus, les boutons et
leurs états, la preuve T0, la géométrie.

Contrôles :
  V1  la fenêtre naît, le titre exact, la géométrie non triviale ;
  V2  les CINQ onglets présents, dans l'ordre (1·VERROU … 5·JOURNAL) ;
  V3  les 17 lignes de pièces rendues (chaque sha affiché) ;
  V4  le verrou VERT à l'écran : TOUT LANCER et REJOUER actifs,
      la preuve T0 affichée ;
  V5  les accents français rendus INTACTS (é, è, ç, …) ;
  V6  l'onglet 4·LIVRE porte la cap M1 et les lignes M3/M1/D202/M4 ;
  V7  le bouton zip inactif tant que le run n'a pas vécu (fail-sain).

Lancement : DISPLAY=:99 python3 fumee_xvfb_gui_unite02_d210.py
"""
import pathlib
import sys
import time

KIT = pathlib.Path("/home/z/my-project/download/"
                   "TRIADE_gui_unite02_d210_v1")
sys.path.insert(0, str(KIT))

PASSES, ECHECS = [], []


def verifie(nom, ok, detail=""):
    (PASSES if ok else ECHECS).append(nom)
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}"
          + (f" — {detail}" if detail else ""))


def tous_widgets(racine, classe=None):
    trouves, pile = [], list(racine.winfo_children())
    while pile:
        w = pile.pop()
        try:
            pile.extend(w.winfo_children())
        except Exception:
            pass
        try:
            if classe is None or w.winfo_class() == classe:
                trouves.append(w)
        except Exception:
            pass
    return trouves


def main():
    etat = KIT / "etat-run-unite02-d210.json"
    if etat.exists():
        etat.unlink()
    import triade_run_unite02_d210_gui as G

    print("[fumée Xvfb] la fenêtre du GUI 1-clic unite02 D210 — "
          "le verrou réel recoupé au fil ouvrier")
    app = G.demarrer(fumee=True)
    racine = app.racine

    # laisser le verrou (fil ouvrier) courir et la file pomper
    deadline = time.time() + 40
    while time.time() < deadline:
        racine.update()
        if getattr(app, "verrou_vert", False):
            break
        time.sleep(0.05)
    # le vidage : l'attribut peut tomber AVANT que la file (les
    # lignes de pièces, la preuve T0) soit pompée — on laisse la
    # pompe vider son monde (2 s d'horloge, au fil principal)
    for _ in range(40):
        racine.update()
        time.sleep(0.05)
    racine.update()

    verifie("V1:la-fenetre-nee",
            "TRIADE" in racine.title() and racine.winfo_width() > 600
            and racine.winfo_height() > 500,
            f"titre « {racine.title()[:60]}… », "
            f"{racine.winfo_width()}×{racine.winfo_height()}")

    carnets = [w for w in racine.winfo_children()
               if w.winfo_class() == "TNotebook"]
    onglets = []
    if carnets:
        carnet = carnets[0]
        onglets = [str(carnet.tab(w, "text")) for w in carnet.tabs()]
    verifie("V2:les-cinq-onglets",
            len(onglets) == 5 and onglets[0].startswith("1·VERROU")
            and "3·TÉMOIN" in onglets[2] and "5·JOURNAL" in onglets[4],
            " | ".join(onglets))

    etiquettes = [str(w.cget("text")) for w in tous_widgets(racine, "TLabel")]
    etiquettes += [str(w.cget("text")) for w in tous_widgets(racine, "Label")]
    shas = [t for t in etiquettes if t.startswith("sha256 ")]
    verifie("V3:les-17-pieces-rendues", len(shas) == 17,
            f"{len(shas)} sha affichés")

    boutons = [(str(b.cget("text")), b)
               for b in tous_widgets(racine, "TButton")]
    tout = [b for t, b in boutons if "TOUT LANCER" in t]
    rejouer = [b for t, b in boutons if "REJOUER" in t]
    zipb = [b for t, b in boutons if "ASSEMBLER" in t]
    preuve_t0 = [t for t in etiquettes if t.startswith("LA PREUVE T0")]
    verifie("V4:le-verrou-vert-a-l-ecran",
            bool(tout) and str(tout[0]["state"]) == "normal"
            and bool(rejouer) and str(rejouer[0]["state"]) == "normal"
            and bool(preuve_t0)
            and "scénario scellé voit 15 pièces" in preuve_t0[0],
            (preuve_t0[0][:80] + "…") if preuve_t0 else "aucune preuve T0")

    verifie("V5:les-accents-rendus",
            any("réceptacle" in t for t in etiquettes)
            and any("pièces" in t for t in etiquettes)
            and any("jamais recalculés" in t for t in etiquettes),
            "é/è/à rendus aux étiquettes (UTF-8 tenu)")

    verifie("V6:l-onglet-livre-porte-les-metriques",
            any("LA CAP M1" in t for t in etiquettes)
            and any("LA LIGNE DE CARNET M3" in t for t in etiquettes)
            and any("LA RÈGLE D202" in t for t in etiquettes)
            and any("LE CHRONO M4" in t for t in etiquettes),
            "M1, M3, M4 et D202 affichés au livre")

    verifie("V7:le-zip-inactif-sans-run",
            bool(zipb) and str(zipb[0]["state"]) == "disabled",
            "le bouton attend le run (fail-sain)")

    racine.destroy()
    print(f"\nFUMÉE VISUELLE : {len(PASSES)} VERT, {len(ECHECS)} ROUGE "
          f"sur {len(PASSES) + len(ECHECS)} contrôles")
    return 0 if not ECHECS else 1


if __name__ == "__main__":
    sys.exit(main())
