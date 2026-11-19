#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_pointeur.py — LA CAMPAGNE cq01qv1za (le plan § 1.2, gelé) :
le mode A (l'avant — le format en vigueur, le gabarit de 5gfx6pwkj TEL
QUEL) contre le mode P (l'après — LE POINTEUR SEUL).

Les MÊMES 18 blocs, la MÊME graine 20261117, le MÊME ordre, le MÊME
instrument (la rig compter_tokens.py — le natif LU du champ usage).
L'espacement 429 : 30 s tous les 4 appels, 75 s à la reprise."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
RIG = REPO / "atelier-baseline-20261117" / "rig" / "compter_tokens.py"
VT = REPO / "atelier-localiser-5gfx6pwkj" / "verites-terrain.json"
journal = ICI / "journal_tokens.jsonl"
garde = ICI / "garde-brut.jsonl"
prompts = ICI / "garde-prompts"

# LE GABARIT A — TEL QUEL (la campagne 5gfx6pwkj, le format en vigueur)
GABARIT_A = (
    "L'OPÉRATION LOCALISER DE LA CARTE TRIADE (le format en vigueur — la réponse\n"
    "rend l'entête complet du bloc localisé).\n"
    "\n"
    "BLOC DE LA CARTE (entête lu du fichier même) :\n"
    "{entete}\n"
    "\n"
    "REQUÊTE : localise le bloc ci-dessus dans la carte et rends SON ENTÊTE\n"
    "COMPLET (toutes les lignes de l'entête du bloc localisé, le format en\n"
    "vigueur de l'opération) — rien d'autre.\n"
)

# LE GABARIT P — LE POINTEUR SEUL (le plan § 1.1, gelé) : le matériau
# porte l'entête ET l'empreinte de la notation (la carte la porte pour
# l'entrée — un champ LITTÉRAL, jamais calculé) ; la réponse tient en
# une ligne : l'identifiant et l'empreinte, recopiés tels quels.
GABARIT_P = (
    "L'OPÉRATION LOCALISER DE LA CARTE TRIADE (le mode pointeur seul — la\n"
    "réponse tient en une ligne, le client expande le pointeur auprès de la\n"
    "carte et confronte l'empreinte aux octets réels).\n"
    "\n"
    "BLOC DE LA CARTE (entête lu du fichier même) :\n"
    "{entete}\n"
    "Empreinte notation : sha256:{empreinte}\n"
    "\n"
    "REQUÊTE : localise le bloc ci-dessus dans la carte et réponds AU FORMAT\n"
    "POINTEUR SEUL, une seule ligne exactement :\n"
    "IDENTIFIANT · sha256:<empreinte>\n"
    "— IDENTIFIANT : l'identifiant de bloc de la carte (la forme iNNNNNN de\n"
    "l'entête) ;\n"
    "— <empreinte> : l'empreinte sha256 recopiée TELLE QUELLE de la ligne\n"
    "« Empreinte notation » ci-dessus (64 hexadécimaux, aucun calcul).\n"
    "Rien d'autre.\n"
)


def main() -> int:
    vt = json.loads(VT.read_text(encoding="utf-8"))
    ordre = vt["ordre"]
    par_id = {b["id"]: b for b in vt["blocs"]}
    entetes = {}
    for f in sorted((REPO / "loupe" / "notation").glob("loupe-*.asm")):
        lignes = []
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.startswith(";"):
                lignes.append(l)
            elif l.strip() == "":
                continue
            else:
                break
        entetes[f.stem] = "\n".join(lignes)

    deja = set()
    if journal.exists():
        for l in journal.read_text(encoding="utf-8").splitlines():
            if l.strip():
                deja.add(json.loads(l)["tache"])
    prompts.mkdir(exist_ok=True)

    appels = [("A", GABARIT_A), ("P", GABARIT_P)]
    for mode, gabarit in appels:
        manquants = [bid for bid in ordre
                     if f"localiser-{mode}-{bid}" not in deja]
        print(f"[{mode}] {len(manquants)} appel(s) à vivre "
              f"(l'ordre de la graine {vt['graine']})", flush=True)
        for i, bid in enumerate(manquants):
            b = par_id[bid]
            tache = f"localiser-{mode}-{bid}"
            if mode == "A":
                prompt = gabarit.format(entete=entetes[b["nom"]])
            else:
                prompt = gabarit.format(entete=entetes[b["nom"]],
                                        empreinte=b["notation_sha256"])
            pfile = prompts / f"{tache}.txt"
            pfile.write_text(prompt, encoding="utf-8")
            if i and i % 4 == 0:
                time.sleep(30)          # la leçon du 429 : l'espacement
            for essai in (1, 2, 3):
                if essai > 1:
                    time.sleep(75)
                r = subprocess.run(
                    ["python3", str(RIG), "--bras", "T", "--phase",
                     "analyse", "--tache", tache,
                     "--prompt-file", str(pfile),
                     "--journal", str(journal),
                     "--garde-brut", str(garde)],
                    capture_output=True, text=True, timeout=600)
                if r.returncode == 0:
                    ligne = [l for l in r.stderr.splitlines()
                             if "tokens" in l]
                    print(f"[{tache}] "
                          f"{ligne[-1] if ligne else 'OK'}", flush=True)
                    break
                print(f"[{tache}] (essai {essai}) ÉCHEC : "
                      f"{(r.stderr or r.stdout).strip().splitlines()[-1][:130]}",
                      flush=True)
            else:
                print(f"[{tache}] ÉCHEC DÉFINITIF — écart nommé", flush=True)
                return 2
    n = sum(1 for l in journal.read_text(encoding="utf-8").splitlines()
            if l.strip())
    print(f"\n[fin] le journal porte {n} lignes (18 A + 18 P attendues)",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
