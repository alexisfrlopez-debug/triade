#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fumee_xvfb_d132.py — FUMÉE Xvfb de la DISPOSITION EN GRILLE du GUI de
migration CF2 → CF3 (D132, v06/migration_cf3_gui.py v1.1).

Fenêtre Tk RÉELLE (Xvfb), AUCUN acte lancé (le relais sous-processus est
prouvé par test_migration_cf3_gui.py X3). Elle prouve LA promesse du
terrain (31/10) :

  « l'interface n'est pas très claire, problèmes de disposition ; les
    boutons de recherche de fichiers ne sont pas alignés aux champs
    concernés »

L'ANCIEN défaut (v1.0) : les entrées étaient packées fill="x" PLEINE
LARGEUR, puis les boutons « Parcourir… » packés side="right" APRÈS — la
cavité restante les empilait en COLONNE à droite, SOUS les champs : un
bouton par ligne, mais AUCUN sur la ligne de son champ.

Contrôles (par onglet, géométrie RÉELLE winfo) :
  1. l'onglet est géré en GRILLE (pack_slaves vide — l'ancienne
     disposition vivait du pack) ;
  2. CHAQUE bouton « Parcourir… » est ALIGNÉ à un champ : son centre
     vertical est sur celui d'un Entry (± 3 px) — l'ancien défaut
     échouerait ici : les boutons vivaient sous les champs ;
  3. chaque bouton vit À DROITE de son champ (il ne le recouvre pas,
     il ne vit pas dessous) et DEUX boutons ne partagent jamais un même
     champ (bijection) ;
  4. le compte de boutons est le compte attendu (migrer 5, vérifier 2,
     détruire 2 — TOUT champ de chemin porte désormais son bouton) ;
  5. le bouton d'acte (MIGRER / VÉRIFIER / DÉTRUIRE) prend la PLEINE
     LARGEUR de l'onglet ;
  6. la confirmation de phrase est ÉTIQUETÉE (« Confirmation de la
     phrase : » — l'ancien deuxième champ muet portait à confusion).

Lancement : Xvfb :99 -screen 0 1280x1024x24 & DISPLAY=:99 \
python3 scripts/fumee_xvfb_d132.py
"""

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "v06"))

from tkinter import ttk       # noqa: E402

PASSES, ECHECS = [], []

LIBELLE_BOUTON = "Parcourir…"
TOLERANCE = 3          # pixels : centres verticaux champ/bouton

ATTENDUS = {           # onglet -> (boutons Parcourir…, libellé d'acte)
    0: (5, "MIGRER"),
    1: (2, "VÉRIFIER"),
    2: (2, "DÉTRUIRE"),
}


def verifie(nom, ok, detail=""):
    (PASSES if ok else ECHECS).append(nom)
    print(f"  {'PASS' if ok else 'ÉCHEC'} {nom}"
          + (f" — {detail}" if detail and not ok else ""))


def _descendants(page, classe):
    """Tous les widgets de `classe` sous `page`, récursivement."""
    trouves, pile = [], [page]
    while pile:
        w = pile.pop()
        for enfant in w.winfo_children():
            if isinstance(enfant, classe):
                trouves.append(enfant)
            pile.append(enfant)
    return trouves


def main():
    if not os.environ.get("DISPLAY"):
        print("[fumée D132] ÉCHEC — aucune variable DISPLAY (Xvfb requis)")
        return 1
    import tkinter as tk
    import migration_cf3_gui as gui
    print(f"[fumée D132] disposition en grille — {gui.VERSION_GUI}")
    racine = tk.Tk()
    app = gui.Application(racine)
    try:
        racine.update_idletasks()
        racine.update()
        verifie("cahier-de-trois-onglets",
                len(app.carnets.tabs()) == 3,
                f"{len(app.carnets.tabs())} onglet(s)")

        for indice, (attendus, libelle_acte) in ATTENDUS.items():
            app.carnets.select(indice)
            racine.update()
            page = racine.nametowidget(app.carnets.tabs()[indice])

            # --- 1. l'onglet vit en GRILLE, plus en pack --------------
            verifie(f"onglet-{indice + 1}-en-grille",
                    not page.pack_slaves() and page.grid_slaves(),
                    f"{len(page.pack_slaves())} pack(s), "
                    f"{len(page.grid_slaves())} grid(s)")

            # --- 2/3. chaque bouton ALIGNÉ à UN champ, à sa droite ---
            entrees = _descendants(page, ttk.Entry)
            boutons = [b for b in _descendants(page, ttk.Button)
                       if (b.cget("text") or "") == LIBELLE_BOUTON]
            details, vus = [], set()
            for bouton in boutons:
                centre_b = bouton.winfo_y() + bouton.winfo_height() / 2
                aligne = [
                    e for e in entrees
                    if abs(e.winfo_y() + e.winfo_height() / 2 - centre_b)
                    <= TOLERANCE]
                if not aligne:
                    details.append(f"bouton y={bouton.winfo_y()} sans champ")
                    continue
                champ = aligne[0]
                if id(champ) in vus:
                    details.append("deux boutons sur le même champ")
                vus.add(id(champ))
                if bouton.winfo_x() < champ.winfo_x() + champ.winfo_width():
                    details.append("bouton pas à droite de son champ")
            verifie(f"onglet-{indice + 1}-boutons-alignes-a-leur-champ",
                    boutons and not details,
                    "; ".join(details) or f"{len(boutons)} bouton(s)")

            # --- 4. le compte attendu ---------------------------------
            verifie(f"onglet-{indice + 1}-{attendus}-boutons-parcourir",
                    len(boutons) == attendus,
                    f"{len(boutons)} bouton(s), attendu {attendus}")

            # --- 5. le bouton d'acte prend la PLEINE LARGEUR -----------
            actes = [b for b in _descendants(page, ttk.Button)
                     if (b.cget("text") or "").startswith(libelle_acte)]
            verifie(f"onglet-{indice + 1}-acte-{libelle_acte.lower()}"
                    f"-pleine-largeur",
                    len(actes) == 1 and actes[0].winfo_width() >= 500,
                    f"{len(actes)} bouton(s) d'acte, largeur "
                    f"{actes[0].winfo_width() if actes else 0} px")

        # --- 6. la confirmation de phrase est étiquetée (onglet 1) ----
        app.carnets.select(0)
        racine.update()
        page1 = racine.nametowidget(app.carnets.tabs()[0])
        libelles = [e.cget("text") or "" for e in _descendants(page1,
                                                               ttk.Label)]
        verifie("confirmation-de-phrase-etiquetee",
                "Confirmation de la phrase :" in libelles)
    finally:
        racine.destroy()
    return fin()


def fin():
    print(f"[fumée D132] {len(PASSES)} PASS / {len(ECHECS)} ÉCHEC")
    if ECHECS:
        for e in ECHECS:
            print(f"  ÉCHEC : {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
