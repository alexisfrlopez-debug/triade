#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fumee_xvfb_d129.py — FUMÉE Xvfb du PILIER DROIT (D129).

Fenêtre Tk RÉELLE (Xvfb), dépôt triade attaché (ce dépôt-ci), AUCUNE
action lancée — la fumée ne fait que LIRE l'arbre de widgets vivant et
basculer les onglets du cahier. Elle prouve LA promesse du terrain :

  « la liste des étapes soit affichée dans un encart à droite de
    l'écran qui soit visible quel que soit l'onglet affiché, idem pour
    le journal de cérémonie (en dessous de la liste des étapes) »

Contrôles :
  1. le pilier existe et se packe À DROITE (side=right), le corps
     défilant À GAUCHE (coordonnées réelles à l'écran) ;
  2. le FIL (cadre_fil) et le JOURNAL (journal.cadre) sont ENFANTS du
     pilier — le fil AU-DESSUS du journal (coordonnée y) ;
  3. NI le fil NI le journal ne descendent du CAHIER d'onglets (avant,
     le fil vivait DANS l'onglet « 1 · Sceau » : la fumée l'aurait vu
     disparaître aux onglets 2-4 — c'est le défaut que D129 tue) ;
  4. SUR CHAQUE onglet du cahier (select + rendu), le fil ET le journal
     restent affichés (winfo_ismapped) — la promesse, onglet par onglet ;
  5. la page ACCUEIL garde elle aussi le pilier (la colonne vit HORS
     des pages) ;
  6. le fil a été ÉVALUÉ (le titre porte le scénario, la ligne courante
     est écrite) : le pilier n'est pas un décor vide.

Lancement : xvfb-run -a python3 scripts/fumee_xvfb_d129.py
"""

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "v06"))

import tkinter as tk          # noqa: E402

PASSES, ECHECS = [], []


def verifie(nom, ok, detail=""):
    (PASSES if ok else ECHECS).append(nom)
    print(f"  {'PASS' if ok else 'ÉCHEC'} {nom}"
          + (f" — {detail}" if detail and not ok else ""))


def _ancetres(widget):
    """La chaîne des parents jusqu'à la racine Tk."""
    chaine, courant = [], widget
    while courant is not None:
        chaine.append(courant)
        courant = courant.master
    return chaine


def main():
    import ceremonie_gui as gui
    print(f"[fumée D129] pilier droit — dépôt {gui.RACINE_DEPOT}")
    app = gui.Application(profil="depot")     # ouvre DIRECTEMENT la cérémonie
    try:
        app.racine.update_idletasks()
        app.racine.update()

        # --- 1. le pilier est un cadre à DROITE du corps défilant --------
        colonne = getattr(app, "colonne_droite", None)
        verifie("pilier-existe", colonne is not None)
        if colonne is None:
            return fin()
        info = colonne.pack_info()
        verifie("pilier-packe-a-droite", info.get("side") == "right",
                str(info))
        canevas = app.zone_defilement
        app.racine.update()
        verifie("pilier-a-droite-du-corps",
                colonne.winfo_rootx() > canevas.winfo_rootx()
                + canevas.winfo_width(),
                f"colonne x={colonne.winfo_rootx()} vs canevas "
                f"x={canevas.winfo_rootx()}+{canevas.winfo_width()}")
        verifie("pilier-largeur-tenue",
                abs(colonne.winfo_width() - gui.LARGEUR_COLONNE_DROITE) <= 2,
                f"{colonne.winfo_width()} px")

        # --- 2. fil et journal vivent DANS le pilier, fil AU-DESSUS ------
        fil, journal = app.cadre_fil, app.journal.cadre
        verifie("fil-enfant-du-pilier", fil.master is colonne,
                fil.master.winfo_name())
        verifie("journal-enfant-du-pilier", journal.master is colonne,
                journal.master.winfo_name())
        app.racine.update()
        verifie("fil-au-dessus-du-journal",
                fil.winfo_rooty() < journal.winfo_rooty(),
                f"fil y={fil.winfo_rooty()} journal y={journal.winfo_rooty()}")

        # --- 3. ni l'un ni l'autre ne descend du cahier -------------------
        cahier = app.cahier_ceremonie
        anc_fil, anc_journal = _ancetres(fil), _ancetres(journal)
        verifie("fil-hors-du-cahier", cahier not in anc_fil)
        verifie("journal-hors-du-cahier", cahier not in anc_journal)
        verifie("fil-hors-des-pages", app.pages["ceremonie"] not in anc_fil
                and app.pages["accueil"] not in anc_fil)

        # --- 4. SUR CHAQUE onglet : fil ET journal restent affichés ------
        onglets = cahier.tabs()
        for i, ident in enumerate(onglets):
            cahier.select(i)
            app.racine.update()
            titre = cahier.tab(ident, "text").strip()
            visible = (fil.winfo_ismapped()
                       and app.journal.texte.winfo_ismapped())
            verifie(f"onglet-{i + 1}-garde-le-pilier[{titre[:26]}]",
                    visible,
                    f"fil={fil.winfo_ismapped()} "
                    f"journal={app.journal.texte.winfo_ismapped()}")

        # --- 5. la page ACCUEIL garde le pilier ---------------------------
        app.montrer("accueil")
        app.racine.update()
        verifie("accueil-garde-le-pilier",
                fil.winfo_ismapped() and app.journal.texte.winfo_ismapped())

        # --- 6. le fil VIT (évalué : titre scénario + ligne courante) ----
        app._choisir_scenario(gui.SCENARIO_GIT)     # lu, aucune action lancée
        app.montrer("ceremonie")
        app.racine.update()
        titre_fil = fil.cget("text")
        courant = app.label_fil_courant.cget("text")
        verifie("fil-evalue-titre-scenario",
                "scénario" in titre_fil and "repo git" in titre_fil,
                titre_fil)
        verifie("fil-evalue-ligne-courante-ecrite",
                bool(courant.strip()) and "aucun dépôt" not in courant,
                courant[:80])
        verifie("journal-vivant-autotest-ecrit",
                "autotest" in app.journal.texte.get("1.0", "end").lower())

        # la fenêtre s'est élargie du pilier (D116 : taille au contenu)
        verifie("fenetre-elargie-du-pilier",
                app.racine.winfo_width() >= gui.LARGEUR_COLONNE_DROITE
                + canevas.winfo_width(),
                f"fenêtre {app.racine.winfo_width()} = pilier "
                f"{gui.LARGEUR_COLONNE_DROITE} + corps "
                f"{canevas.winfo_width()}")
    finally:
        app.racine.destroy()
    return fin()


def fin():
    print(f"[fumée D129] {len(PASSES)} PASS / {len(ECHECS)} ÉCHEC")
    if ECHECS:
        for e in ECHECS:
            print(f"  ÉCHEC : {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
