#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gui_ceremonie.py — LA GUI de la cérémonie d'ère de couloir-vaes512.asm (v100).

Le patron des GUI du projet (ceremonie_gui.py D87 : tkinter, stdlib seule,
zéro pip) : la fenêtre ne fait QUE lancer le moteur (moteur_ceremonie.py) et
suivre son journal — LE MOTEUR PORTE TOUT LE POIDS DU GESTE.

LES QUATRE BOUTONS (le flux de la cérémonie) :
  1. Préparer la charge        — le manifeste recoupé, la charge écrite, a-emporter/ ;
  2. Guider la signature       — le pas-à-pas hors-ligne (la clé du maître, jamais au bac) ;
  3. Vérifier la signature     — chaque signature contre la charge + la clé publique I ;
  4. Installer le sceau d'ère  — ere-vaes512-sceau.txt + le zip de preuves.
"""
from __future__ import annotations

import pathlib
import queue
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk

ICI = pathlib.Path(__file__).resolve().parent
MOTEUR = ICI / "moteur_ceremonie.py"

for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class GUI:
    def __init__(self, racine: tk.Tk):
        self.racine = racine
        racine.title("TRIADE — la cérémonie d'ère de couloir-vaes512.asm (kit v100)")
        racine.geometry("940x640")
        self.file = queue.Queue()
        self.proc = None
        self._bâtir()
        racine.after(200, self._pomper)

    def _bâtir(self):
        cadre = ttk.Frame(self.racine, padding=8)
        cadre.pack(fill=tk.BOTH, expand=True)
        entete = ("TRIADE — LA CÉRÉMONIE D'ÈRE DE couloir-vaes512.asm (kit v100)\n"
                  "LA DETTE NOMMÉE À LA NAISSANCE (PLAN-W29VAES512) : l'ère n'est scellée\n"
                  "que par la clé hors-ligne du maître — le laboratoire ne signe JAMAIS\n"
                  "(D87/D183). La continuité de clé (D163) : l'ère se signe à la MÊME clé\n"
                  "que le sceau de l'Intention (la clé des 14 arbres).")
        ttk.Label(cadre, text=entete, justify=tk.LEFT,
                  font=("TkDefaultFont", 9, "bold")).grid(row=0, column=0, columnspan=4,
                                                          sticky="w", pady=(0, 6))
        actions = ttk.LabelFrame(cadre, text="Les étapes de la cérémonie", padding=6)
        actions.grid(row=1, column=0, columnspan=4, sticky="we", pady=(0, 6))
        self.boutons = {}
        for i, (nom, texte) in enumerate([
                ("preparer", "1 · Préparer la charge (le manifeste + a-emporter)"),
                ("guider", "2 · Guider la signature hors-ligne (la clé du maître)"),
                ("verifier", "3 · Vérifier la signature revenue"),
                ("installer", "4 · Installer le sceau d'ère")]):
            b = ttk.Button(actions, text=texte, command=lambda n=nom: self.lancer(n))
            b.grid(row=0, column=i, sticky="we", padx=3)
            actions.columnconfigure(i, weight=1)
            self.boutons[nom] = b
        journal = ttk.LabelFrame(cadre, text="Le journal du moteur", padding=6)
        journal.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=(0, 4))
        self.zone = scrolledtext.ScrolledText(journal, height=20, state="disabled",
                                              font=("Courier New", 9))
        self.zone.pack(fill=tk.BOTH, expand=True)
        self.etat = tk.StringVar(value="PRÊT — l'étape 1 d'abord (la charge)")
        ttk.Label(cadre, textvariable=self.etat, relief="sunken",
                  anchor="w").grid(row=3, column=0, columnspan=4, sticky="we")
        cadre.rowconfigure(2, weight=1)

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

    def _arguments(self, nom: str) -> list:
        if nom == "preparer":
            return [sys.executable, "-X", "utf8", str(MOTEUR), "--preparer"]
        if nom == "guider":
            return None            # le guide est LOCAL (aucun processus)
        if nom == "verifier":
            chemin = self._choisir_signatures()
            if chemin is None:
                return None
            return [sys.executable, "-X", "utf8", str(MOTEUR), "--verifier", str(chemin)]
        if nom == "installer":
            chemin = self._choisir_signatures()
            if chemin is None:
                return None
            return [sys.executable, "-X", "utf8", str(MOTEUR), "--installer", str(chemin)]
        return None

    def _choisir_signatures(self):
        chemin = filedialog.askopenfilename(
            title="Choisissez signatures-I.txt (rapporté de la machine hors-ligne)",
            initialdir=str(ICI), filetypes=[("signatures", "signatures-I.txt"), ("tous", "*")])
        return chemin or None

    def lancer(self, nom: str):
        if nom == "guider":
            self._log("\n[GUI] === LE GUIDE DE LA SIGNATURE HORS-LIGNE ===")
            for ligne in [
                    "1. Copiez le DOSSIER a-emporter/ (côté kit) vers la machine",
                    "   hors ligne (clef USB, papier) — la clé privée n'entre",
                    "   jamais au bac à sable de l'assistant.",
                    "2. À la machine hors ligne, re-vérifiez la notation :",
                    "   l'empreinte sha256 de couloir-vaes512.asm doit être",
                    "   a2c3a393… (celle de la charge) :",
                    "     python3 signeur_hors_ligne.py autotest",
                    "     certutil -hashfile couloir-vaes512.asm SHA256   (Windows)",
                    "3. Signez la charge À VOTRE CLÉ du sceau (la continuité D163) :",
                    "     python3 signeur_hors_ligne.py signer ere-vaes512-a-signer.txt cle-I-privee.txt",
                    "   (l'outil du dépôt v06/ceremonie_hors_ligne.py signe la MÊME",
                    "    charge telle quelle — la forme est la même).",
                    "4. Rapportez signatures-I.txt au kit, puis le bouton 3"]:
                self._log("[guide] " + ligne)
            self.etat.set("le guide affiché — la signature vit hors-ligne")
            return
        if self.proc and self.proc.poll() is None:
            self._log("[GUI] une étape court déjà — attends sa fin.")
            return
        args = self._arguments(nom)
        if args is None:
            return
        self._log(f"\n[GUI] === L'ÉTAPE : {nom} ===")
        self.proc = subprocess.Popen(args, cwd=str(ICI), text=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      encoding="utf-8", errors="replace", bufsize=1)

        def suivre():
            for ligne in self.proc.stdout:
                self.file.put(ligne.rstrip("\n"))
            code = self.proc.wait()
            self.file.put(f"[ÉTAT] {'VERT' if code == 0 else 'ROUGE'} — {nom} (code {code})")
        threading.Thread(target=suivre, daemon=True).start()


def main():
    racine = tk.Tk()
    GUI(racine)
    racine.mainloop()


if __name__ == "__main__":
    main()
