#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES PREUVES SYMBOLIQUES HORS BAC (W20SEC b) — REFUS NOMMÉ, AUCUN VERDICT FABRIQUÉ.

Tamarin (CF3-v3) et le port ProVerif exigent des binaires absents de ce bac et une mémoire
> 4 GiB pour les lemmes L1/L2 (le mur constaté au v3). Le script CONSTATE l'absence, refuse
le run avec son motif, et imprime la commande exacte du poste réel — y compris la
décomposition en lemmes auxiliaires que l'évaluation demande (induction sur l'époque,
connaissance attaquant restreinte).

Usage : python3 scripts/vague20/preuves_symboliques.py
"""
import json, pathlib, shutil, sys

R = pathlib.Path(__file__).resolve().parents[2]
MIN_MEMOIRE_GIO = 4


def memoire_gio():
    for ligne in pathlib.Path("/proc/meminfo").read_text().splitlines():
        if ligne.startswith("MemTotal"):
            return round(int(ligne.split()[1]) / 1024 / 1024, 1)
    return 0.0


def outils():
    return {o: (shutil.which(o) or None) for o in ("tamarin-prover", "proverif", "maude")}


def main():
    presence = outils()
    absents = [o for o, p in presence.items() if not p]
    mem = memoire_gio()
    doc = {"outils": presence, "memoire_gio": mem, "minimum_gio": MIN_MEMOIRE_GIO,
           "verdict": None, "motifs": [],
           "commandes_poste_reel": {
               "tamarin": "tamarin-prover --prove --partial-evaluation cf3-v3.spthy",
               "tamarin_negatif": "tamarin-prover --prove cf3-v3-defaut.spthy   # le contre-exemple attendu",
               "proverif": "proverif CF3-v3.pv",
               "note": "décomposition en lemmes auxiliaires : induction sur l'époque (PhraseVivante), "
                       "connaissance d'attaquant restreinte aux relations hors K ; six écarts de "
                       "sémantique ProVerif nommés au fichier .pv"}}
    if absents:
        doc["motifs"].append(f"TOOL-ABSENT : {', '.join(absents)}")
    if mem < MIN_MEMOIRE_GIO:
        doc["motifs"].append(f"MEMOIRE-INSUFFISANTE : {mem} Gio < {MIN_MEMOIRE_GIO}")
    doc["verdict"] = "REFUS" if doc["motifs"] else "A-EXECUTER"
    print(json.dumps(doc, ensure_ascii=False, indent=1))
    print(f"[preuves-symboliques] {doc['verdict']} — " + (" ; ".join(doc["motifs"]) if doc["motifs"] else "outils et mémoire présents"))
    return 2 if doc["verdict"] == "REFUS" else 0


if __name__ == "__main__":
    sys.exit(main())
