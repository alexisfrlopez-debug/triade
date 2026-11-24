#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMÉLIORATION 2 (D257) — LA MESURE DE L'ÉCART JUGE / GRAMMAIRE.

Le juge d'une campagne accepte une complétion sur le CONTRAT ; la grammaire
publie ce que la notation doit être. Quand les deux divergent, une campagne
« contrainte » mesure un changement de RÈGLE, pas un gain de modèle.

Ce script rejoue la grammaire canonique TPL-ADD (l'instrument de l'atelier
campagne-v6, importé, jamais recopié) sur les complétions que le juge a
déclarées VERTES dans le corpus v2.1, et rend :
  - l'acceptation de la grammaire sur les verts du juge ;
  - les familles de refus (les motifs nommés, comptés) ;
  - le verdict : ÉCART si une seule verte est refusée par la grammaire.
Sortie : 0 = aligné (toutes les vertes acceptées), 3 = écart nommé (défaut de
campagne, pas de production), 2 = corpus ou instrument absent.
"""
import collections
import importlib.util
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]
INSTRUMENT = RACINE / "atelier-campagne-v6-0j7ywza2h" / "instrument_contraint.py"
CORPUS = RACINE / "depot-zenodo-corpus-v21"


def charge_grammaire():
    spec = importlib.util.spec_from_file_location("instrument_contraint", INSTRUMENT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def mesure():
    if not INSTRUMENT.exists() or not CORPUS.exists():
        print("[ecart] instrument ou corpus absent")
        return 2
    g = charge_grammaire()
    verts, acceptes, refus = 0, 0, collections.Counter()
    for split in ("train", "dev", "test"):
        for ligne in (CORPUS / (split + ".jsonl")).read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            r = json.loads(ligne)
            if str(r.get("verdict", "")).upper() != "VERT":
                continue
            rep = r.get("reponse") or ""
            if not rep.strip():
                continue
            verts += 1
            ok, motifs = g.valider_corps(rep)
            if ok:
                acceptes += 1
            else:
                refus[motifs[0][2].split(" : ")[0]] += 1
    print("=" * 78)
    print("L'ÉCART JUGE / GRAMMAIRE — LE CORPUS v2.1, LES COMPLÉTIONS DÉCLARÉES VERTES")
    print("=" * 78)
    print(f"vertes du juge : {verts} · acceptées par la grammaire : {acceptes} · refusées : {verts - acceptes}")
    for motif, n in refus.most_common():
        print(f"  {n:>3} × {motif}")
    if verts and acceptes == verts:
        print("[ecart] ALIGNÉ — la grammaire accepte tout ce que le juge déclare vert")
        return 0
    print("[ecart] ÉCART NOMMÉ — une campagne « contrainte » sans cette mesure mesurerait un changement de règle")
    return 3


if __name__ == "__main__":
    sys.exit(mesure())
