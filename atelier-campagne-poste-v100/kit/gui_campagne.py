#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gui_campagne.py — LA GUI du kit de campagne au poste réel (v100).

Le patron des GUI du projet (ceremonie_gui.py D87 : tkinter, stdlib seule,
zéro pip) : la fenêtre ne fait QUE lancer le moteur (moteur_campagne.py) et
suivre son journal en direct — LE MOTEUR PORTE TOUT LE POIDS DU GESTE (la
leçon des pousseur/cockpit vécus : la fenêtre suit les patrons éprouvés,
jamais la logique).

LES CINQ BOUTONS (l'ordre du plan gelé) :
  1. Vérifier le kit   — le manifeste recoupé byte-byte au chargement ;
  2. Le gate           — la sonde du décodeur client (GATE-VERT requis) ;
  3. Le canari         — la violation ordonnée refusée au décodage ;
  4. LA CAMPAGNE       — éditer 18 + ajouter 18 + la seconde famille ;
  5. Le zip de preuves — le retour au coffre /test.

Le mode (B llama.cpp / A transformers), l'endpoint, nprobs et le chemin du
modèle se règlent au panneau — le LISEZMOI porte les commandes exactes du
serving.
"""
from __future__ import annotations

import os
import pathlib
import queue
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk

ICI = pathlib.Path(__file__).resolve().parent
MOTEUR = ICI / "moteur_campagne.py"

for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class GUI:
    def __init__(self, racine: tk.Tk):
        self.racine = racine
        racine.title("TRIADE — campagne au poste réel (kit v100) · GUI 1 clic")
        racine.geometry("980x720")
        self.file = queue.Queue()
        self.proc = None
        self._bâtir()
        racine.after(200, self._pomper)

    # ------------------------------------------------------------------ vue
    def _bâtir(self):
        cadre = ttk.Frame(self.racine, padding=8)
        cadre.pack(fill=tk.BOTH, expand=True)

        entete = ("TRIADE — LA CAMPAGNE AU POSTE RÉEL (kit v100)\n"
                  "les plans gelés PLAN-W29DECCO.md + PLAN-W29FAMILLE.md : aucune cible "
                  "re-tirée, aucune graine re-tirée, aucun chiffre fabriqué\n"
                  "le modèle choisi : Qwen/Qwen2.5-Coder-7B-Instruct (les empreintes au "
                  "manifeste) — le décodage contraint CÔTÉ CLIENT (llguidance)")
        ttk.Label(cadre, text=entete, justify=tk.LEFT,
                  font=("TkDefaultFont", 9, "bold")).grid(row=0, column=0,
                                                          columnspan=4, sticky="w", pady=(0, 6))

        # -- le panneau de réglage -------------------------------------------
        reg = ttk.LabelFrame(cadre, text="Le serving du modèle (le LISEZMOI porte les commandes exactes)", padding=6)
        reg.grid(row=1, column=0, columnspan=4, sticky="we", pady=(0, 6))
        ttk.Label(reg, text="Mode :").grid(row=0, column=0, sticky="w")
        self.mode = tk.StringVar(value="B")
        ttk.Radiobutton(reg, text="B — llama.cpp (le bord natif /completion)",
                        variable=self.mode, value="B").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(reg, text="A — transformers (in-process, le masque aux logits entiers)",
                        variable=self.mode, value="A").grid(row=1, column=1, sticky="w")
        ttk.Label(reg, text="L'endpoint :").grid(row=0, column=2, sticky="e")
        self.url = tk.StringVar(value="http://127.0.0.1:8080")
        ttk.Entry(reg, textvariable=self.url, width=28).grid(row=0, column=3, sticky="we", padx=4)
        ttk.Label(reg, text="top-n :").grid(row=1, column=2, sticky="e")
        self.nprobs = tk.StringVar(value="64")
        ttk.Entry(reg, textvariable=self.nprobs, width=8).grid(row=1, column=3, sticky="w", padx=4)
        ttk.Label(reg, text="Le chemin du modèle (MODE-A seul) :").grid(row=2, column=0, columnspan=2, sticky="w")
        self.modele = tk.StringVar(value="")
        ttk.Entry(reg, textvariable=self.modele, width=52).grid(row=2, column=2, columnspan=2, sticky="we", padx=4)
        reg.columnconfigure(3, weight=1)

        # -- les boutons ------------------------------------------------------
        actions = ttk.LabelFrame(cadre, text="Les étapes (l'ordre du plan — chaque bouton attend la fin du précédent)", padding=6)
        actions.grid(row=2, column=0, columnspan=4, sticky="we", pady=(0, 6))
        self.boutons = {}
        for i, (nom, texte) in enumerate([
                ("verifier-kit", "1 · Vérifier le kit (le manifeste)"),
                ("gate", "2 · Le gate (la sonde du décodeur)"),
                ("canari", "3 · Le canari (la violation refusée)"),
                ("campagne", "4 · LA CAMPAGNE (éditer + ajouter + la famille)"),
                ("zip", "5 · Le zip de preuves")]):
            b = ttk.Button(actions, text=texte,
                           command=lambda n=nom: self.lancer(n))
            b.grid(row=0, column=i, sticky="we", padx=3)
            actions.columnconfigure(i, weight=1)
            self.boutons[nom] = b

        # -- le journal -------------------------------------------------------
        journal = ttk.LabelFrame(cadre, text="Le journal du moteur (en direct)", padding=6)
        journal.grid(row=3, column=0, columnspan=4, sticky="nsew", pady=(0, 4))
        self.zone = scrolledtext.ScrolledText(journal, height=24, state="disabled",
                                              font=("Courier New", 9))
        self.zone.pack(fill=tk.BOTH, expand=True)

        # -- la barre d'état --------------------------------------------------
        self.etat = tk.StringVar(value="PRÊT — l'étape 1 d'abord (le manifeste)")
        ttk.Label(cadre, textvariable=self.etat, relief="sunken",
                  anchor="w").grid(row=4, column=0, columnspan=4, sticky="we")
        cadre.rowconfigure(3, weight=1)
        cadre.columnconfigure(0, weight=1)

    def _log(self, texte: str):
        self.zone.configure(state="normal")
        self.zone.insert(tk.END, texte + "\n")
        self.zone.see(tk.END)
        self.zone.configure(state="disabled")

    def _pomper(self):
        try:
            while True:
                ligne = self.file.get_nowait()
                self._log(ligne)
                if ligne.startswith("[ÉTAT]"):
                    self.etat.set(ligne[7:].strip())
        except queue.Empty:
            pass
        self.racine.after(200, self._pomper)

    # ------------------------------------------------------------- lancement
    def _arguments(self, nom: str) -> list:
        a = [sys.executable, "-X", "utf8", str(MOTEUR)]
        if nom == "verifier-kit":
            a.append("--verifier-kit")
        elif nom == "gate":
            a.append("--gate")
        elif nom == "canari":
            a += ["--canari", "--mode", self.mode.get()]
        elif nom == "campagne":
            a += ["--campagne", "--mode", self.mode.get()]
        elif nom == "zip":
            a.append("--zip")
        if self.mode.get() == "B" and nom in ("canari", "campagne"):
            a += ["--url", self.url.get().strip(), "--nprobs", self.nprobs.get().strip()]
        if self.mode.get() == "A" and nom in ("canari", "campagne"):
            a += ["--modele", self.modele.get().strip()]
        return a

    def lancer(self, nom: str):
        if self.proc and self.proc.poll() is None:
            self._log("[GUI] une étape court déjà — attends sa fin.")
            return
        self._log(f"\n[GUI] === L'ÉTAPE : {nom} "
                  f"({' '.join(self._arguments(nom)[3:])}) ===")
        self.proc = subprocess.Popen(
            self._arguments(nom), cwd=str(ICI), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            encoding="utf-8", errors="replace", bufsize=1)

        def suivre():
            for ligne in self.proc.stdout:
                self.file.put(ligne.rstrip("\n"))
            code = self.proc.wait()
            self.file.put(f"[ÉTAT] {'VERT' if code == 0 else 'ROUGE'} — {nom} "
                          f"(code {code})")

        threading.Thread(target=suivre, daemon=True).start()


def main():
    racine = tk.Tk()
    GUI(racine)
    racine.mainloop()


if __name__ == "__main__":
    main()
