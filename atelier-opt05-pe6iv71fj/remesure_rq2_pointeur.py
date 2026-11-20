#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""remesure_rq2_pointeur.py — LA RE-MESURE RQ2 DE LOCALISER APRÈS ADOPTION
DU POINTEUR SEUL (le plan atelier-egalite-gq117wphb/PLAN-REMESURE-RQ2.md,
gelé) : le gabarit P de la campagne OPT-04 RECONDUIT OCTET POUR OCTET,
la même graine 20261117, le même ordre des 18 blocs, le tokenizer natif
lu du champ usage, n=18, la confrontation à chaque réponse (l'identifiant
exact, l'empreinte recopiée telle quelle — toute divergence NOMMÉE)."""
from __future__ import annotations

import json
import pathlib
import sys
import time

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
sys.path.insert(0, str(ICI))

from instrument_opt05 import appeler_et_compter  # noqa: E402

VT = REPO / "atelier-localiser-5gfx6pwkj" / "verites-terrain.json"

# LE GABARIT P — TEL QUE GELÉ À OPT-04 (cq01qv1za, copié octet pour octet)
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

    journal = ICI / "journal_tokens.jsonl"
    faits = set()
    if journal.exists():
        for l in journal.read_text(encoding="utf-8").splitlines():
            if l.strip():
                faits.add(json.loads(l)["tache"])
    resultats = ICI / "resultats_rq2.jsonl"

    manquants = [bid for bid in ordre if f"localiser-P-{bid}" not in faits]
    print(f"[RQ2-P] {len(manquants)} appel(s) à vivre (la graine {vt['graine']})", flush=True)
    for bid in manquants:
        b = par_id[bid]
        tache = f"localiser-P-{bid}"
        prompt = GABARIT_P.format(entete=entetes[b["nom"]],
                                  empreinte=b["notation_sha256"])
        try:
            texte, ligne = appeler_et_compter("T", "analyse", tache, prompt)
        except Exception as e:
            print(f"  ÉCHEC API {tache}: {e}", flush=True)
            time.sleep(20)
            continue
        # LA CONFRONTATION (aucun contrôle retiré) : l'identifiant exact,
        # l'empreinte recopiée telle quelle
        attendu = f"{bid} · sha256:{b['notation_sha256']}"
        conforme = texte.strip() == attendu
        verdict = "CONFORME" if conforme else f"DIVERGENCE: {texte.strip()[:70]!r}"
        with open(resultats, "a", encoding="utf-8") as f:
            f.write(json.dumps({"tache": tache, "bloc": b["nom"],
                                "verdict": verdict,
                                "total_tokens": ligne["total_tokens"],
                                "completion_tokens": ligne["completion_tokens"],
                                "sha256_echange": ligne["sha256_echange"]},
                               ensure_ascii=False) + "\n")
        print(f"  {tache}: {ligne['total_tokens']} tokens — {verdict[:80]}", flush=True)
        time.sleep(6)
    print("LA RE-MESURE RQ2 visitée.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
