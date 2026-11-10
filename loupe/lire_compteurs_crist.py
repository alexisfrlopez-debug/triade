#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lire_compteurs_crist.py — lecture seule des compteurs de cristallisation
R6 (les 26 blocs, dans frag-prf chiffré — le modèle des portes du scellage,
lignes 1575-1591 de build_loupe.py). Aucune écriture, aucune signature."""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))    # loupe/ (les .keys)

import carte_m10 as cm10  # noqa: E402

phrase, _graine = cm10.charger_secrets(interactif=False)
maitre = cm10.cle_maitresse(phrase)
_entete, fragments, _sig, _pub = cm10.lire_carte()
prf = cm10.dechiffrer_fragment(maitre, "frag-prf",
                               fragments["frag-prf"]).decode("utf-8")
compteurs = {}
for ligne in prf.splitlines():
    if ligne.startswith("[bloc]"):
        champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
        m = re.match(r"(\d+)/10", champs.get("crist", "0/10"))
        compteurs[champs["id"]] = int(m.group(1)) if m else 0
    elif ligne.startswith("  run "):
        derniere = ligne.strip()
incomplets = {b: n for b, n in compteurs.items() if n < 10}
print(f"[compteurs] {len(compteurs)} blocs — min {min(compteurs.values())}/10, "
      f"max {max(compteurs.values())}/10, incomplets {len(incomplets)}")
print(f"[compteurs] aperçu : "
      + ", ".join(f"{b}={compteurs[b]}/10"
                  for b in sorted(compteurs)[:6]) + "…")
print(f"[compteurs] dernier run carte : {derniere[:100]}…")
sys.exit(0)
