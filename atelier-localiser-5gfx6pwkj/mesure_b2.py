#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesure_b2.py — LA PASSE 2 de la campagne 5gfx6pwkj : le mode B2 (quatre
champs LITTÉRAUX, aucun calcul — le plan B2 gelé, sha256 0d98b0e1…, consigné
D212 AVANT la mesure).

Les mêmes 18 blocs, la même graine 20261117, le même instrument — le mode A
n'est pas re-mesuré (la passe A de la campagne initiale fait foi)."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time

ICI = pathlib.Path(__file__).resolve().parent
RIG = ICI.parent / "atelier-baseline-20261117" / "rig" / "compter_tokens.py"
journal = ICI / "journal_tokens.jsonl"
garde = ICI / "garde-brut.jsonl"
prompts = ICI / "garde-prompts"

GABARIT_B2 = (
    "L'OPÉRATION LOCALISER DE LA CARTE TRIADE (le mode minimal — la réponse tient\n"
    "en une ligne, la carte confronte la réponse aux octets réels).\n"
    "\n"
    "BLOC DE LA CARTE (entête lu du fichier même) :\n"
    "{entete}\n"
    "\n"
    "REQUÊTE : localise le bloc ci-dessus dans la carte et réponds AU FORMAT\n"
    "MINIMAL, une seule ligne exactement :\n"
    "IDENTIFIANT · NOM · SLOT · TAILLE\n"
    "— IDENTIFIANT : l'identifiant de bloc de la carte (la forme iNNNNNN de\n"
    "l'entête) ;\n"
    "— NOM : le nom du bloc (le premier champ de la première ligne de\n"
    "l'entête, la forme loupe-NN-mot) ;\n"
    "— SLOT : l'adresse RVA du slot, telle que la deuxième ligne de l'entête\n"
    "la porte (la forme 0x…) ;\n"
    "— TAILLE : la taille du slot en octets, le nombre tel que l'entête le\n"
    "porte.\n"
    "AUCUN CALCUL — recopie les quatre champs tels quels ; la carte fait le\n"
    "reste. Rien d'autre.\n"
)


def main() -> int:
    sys.path.insert(0, str(ICI))
    from mesure_localiser import verite_terrain
    blocs = {b["id"]: b for b in verite_terrain()}
    vt = json.loads((ICI / "verites-terrain.json").read_text(encoding="utf-8"))
    ordre = vt["ordre"]

    deja = set()
    for l in journal.read_text(encoding="utf-8").splitlines():
        if l.strip():
            deja.add(json.loads(l)["tache"])
    manquants = [bid for bid in ordre if f"localiser-B2-{bid}" not in deja]
    print(f"[B2] {len(manquants)} appel(s) à vivre (l'ordre de la graine)")

    for i, bid in enumerate(manquants):
        tache = f"localiser-B2-{bid}"
        pfile = prompts / f"{tache}.txt"
        pfile.write_text(GABARIT_B2.format(entete=blocs[bid]["entete"]),
                         encoding="utf-8")
        if i and i % 4 == 0:
            time.sleep(30)  # la leçon du 429 : l'espacement
        for essai in (1, 2, 3):
            if essai > 1:
                time.sleep(75)
            r = subprocess.run(
                ["python3", str(RIG), "--bras", "T", "--phase", "analyse",
                 "--tache", tache, "--prompt-file", str(pfile),
                 "--journal", str(journal), "--garde-brut", str(garde)],
                capture_output=True, text=True, timeout=600)
            if r.returncode == 0:
                ligne = [l for l in r.stderr.splitlines() if "tokens" in l]
                print(f"[{tache}] {ligne[-1] if ligne else 'OK'}")
                break
            print(f"[{tache}] (essai {essai}) ÉCHEC : "
                  f"{(r.stderr or r.stdout).strip().splitlines()[-1][:150]}")
        else:
            print(f"[{tache}] ÉCHEC DÉFINITIF — écart nommé")
            return 2
    n = sum(1 for l in journal.read_text(encoding="utf-8").splitlines()
            if l.strip())
    print(f"\n[B2] le journal porte {n} lignes (18 A + 18 B1 + 18 B2 attendues)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
