#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fumee_xvfb_d131.py — FUMÉE Xvfb du BOUTON D'ATTACHEMENT UNIQUE (D131).

Fenêtre Tk RÉELLE (Xvfb), dépôt triade attaché (ce dépôt-ci), AUCUNE
action lancée. Elle prouve LA promesse du terrain (31/10) :

  « sur la page de choix de scénario, il y a 2 boutons pour attacher
    un repo local qui font doublon »

Contrôles :
  1. l'accueil SANS scénario ne porte AUCUN bouton « Attacher le dépôt
     local… » (il naît du choix — D117 : le scénario est AVANT TOUT) ;
  2. scénario DOSSIER LOCAL : EXACTEMENT UN bouton sur l'accueil, et il
     vit DANS le panneau de scénario (cadre_scen_panels ancêtre) ;
  3. scénario REPO GIT : EXACTEMENT UN bouton d'attachement, à côté du
     bouton « Cloner en local… » (distinct) — toujours pas de doublon ;
  4. re-choix de scénario : le panneau se rebâtit, le bouton SURVIT et
     reste UNIQUE à chaque rebâtissage ;
  5. la régression tuée : quel que soit le scénario, le compte par page
     ne remonte JAMAIS à 2 (l'ancien doublon de la section « La
     cérémonie » de l'accueil est mort).

Lancement : DISPLAY=:99 python3 scripts/fumee_xvfb_d131.py
"""

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "v06"))

from tkinter import ttk       # noqa: E402

PASSES, ECHECS = [], []

LIBELLE = "Attacher le dépôt local…"


def verifie(nom, ok, detail=""):
    (PASSES if ok else ECHECS).append(nom)
    print(f"  {'PASS' if ok else 'ÉCHEC'} {nom}"
          + (f" — {detail}" if detail and not ok else ""))


def _boutons(page):
    """Tous les ttk.Button (texte, widget) d'une page, récursivement."""
    trouves = []
    pile = [page]
    while pile:
        w = pile.pop()
        for enfant in w.winfo_children():
            if isinstance(enfant, ttk.Button):
                trouves.append((enfant.cget("text") or "", enfant))
            pile.append(enfant)
    return trouves


def _ancetres(widget):
    """La chaîne des parents jusqu'à la racine Tk."""
    chaine, courant = [], widget
    while courant is not None:
        chaine.append(courant)
        courant = courant.master
    return chaine


def main():
    import ceremonie_gui as gui
    print(f"[fumée D131] bouton d'attachement unique — dépôt "
          f"{gui.RACINE_DEPOT}")
    app = gui.Application(profil="depot")
    try:
        app.racine.update_idletasks()
        app.racine.update()

        # --- 1. sans scénario : AUCUN bouton d'attachement ---------------
        app.montrer("accueil")
        app.racine.update()
        accueil = app.pages["accueil"]
        attaches = [w for t, w in _boutons(accueil) if t == LIBELLE]
        verifie("accueil-sans-scenario-zero-bouton", len(attaches) == 0,
                f"{len(attaches)} bouton(s) « {LIBELLE} »")

        # --- 2. dossier local : UN bouton, DANS le panneau de scénario ---
        app._choisir_scenario(gui.SCENARIO_DOSSIER)
        app.racine.update()
        attaches = [w for t, w in _boutons(accueil) if t == LIBELLE]
        verifie("accueil-dossier-local-un-seul-bouton", len(attaches) == 1,
                f"{len(attaches)} bouton(s) — le doublon du terrain "
                f"serait 2")
        if attaches:
            verifie("bouton-dans-le-panneau-de-scenario",
                    app.cadre_scen_panels in _ancetres(attaches[0]),
                    "le bouton doit vivre dans cadre_scen_panels")

        # --- 3. repo git : TOUJOURS UN, à côté du clonage (distinct) ------
        app._choisir_scenario(gui.SCENARIO_GIT)
        app.racine.update()
        boutons = _boutons(accueil)
        n_att = sum(1 for t, _ in boutons if t == LIBELLE)
        n_clone = sum(1 for t, _ in boutons if t == "Cloner en local…")
        verifie("accueil-repo-git-un-seul-bouton", n_att == 1,
                f"{n_att} bouton(s) d'attachement")
        verifie("clonage-present-et-distinct", n_clone == 1,
                f"{n_clone} bouton(s) « Cloner en local… »")

        # --- 4. re-choix : le panneau se rebâtit, le bouton reste UNIQUE -
        app._choisir_scenario(gui.SCENARIO_DOSSIER)
        app.racine.update()
        n = sum(1 for t, _ in _boutons(accueil) if t == LIBELLE)
        verifie("re-choix-le-bouton-survit-unique", n == 1,
                f"{n} bouton(s) après re-bâtissage du panneau")

        # --- 5. la régression tuée : JAMAIS deux, quel que soit le -------
        #        scénario (l'ancien doublon de « La cérémonie » est mort)
        for scenario in (gui.SCENARIO_DOSSIER, gui.SCENARIO_GIT):
            app._choisir_scenario(scenario)
            app.racine.update()
            n = sum(1 for t, _ in _boutons(accueil) if t == LIBELLE)
            verifie(f"jamais-deux-{scenario.replace(' ', '-')}", n <= 1,
                    f"{n} bouton(s) en scénario « {scenario} »")
    finally:
        app.racine.destroy()
    return fin()


def fin():
    print(f"[fumée D131] {len(PASSES)} PASS / {len(ECHECS)} ÉCHEC")
    if ECHECS:
        for e in ECHECS:
            print(f"  ÉCHEC : {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
