#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reconfronter_opt05.py — RE-CONFRONTE les réponses conservées (garde-brut)
aux clients corrigés : les verdicts de resultats_opt05.jsonl sont RECALCULÉS
depuis les pièces brutes (les mesures de jetons au journal demeurent —
elles sont le LOG, jamais retouchées). Le recalcul ne change un verdict
que lorsque le défaut était CELUI DU CLIENT (l'extraction absente), jamais
lorsque la réponse divergeait : la pièce fait foi."""
from __future__ import annotations

import json
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from client_hunks import round_trip, extraire_notation  # noqa: E402
from client_hunks_v2 import traiter as traiter_v2, Refus  # noqa: E402

REPO = ICI.parent
GABARIT_BASE = (
    "push rbx\npush r12\npush r13\npush r14\npush r15\nsub rsp, 0x20\n"
    "; --- LE CORPS DU BLOC ICI ---\n"
    "add rsp, 0x20\npop r15\npop r14\npop r13\npop r12\npop rbx\nret\n"
)


def main() -> int:
    garde = {}
    for l in (ICI / "garde-brut.jsonl").read_text(encoding="utf-8").splitlines():
        if l.strip():
            g = json.loads(l)
            garde[g["tache"]] = g["reponse_api"]["choices"][0]["message"]["content"]
    resultats = [json.loads(l) for l in
                 (ICI / "resultats_opt05.jsonl").read_text(encoding="utf-8").splitlines()
                 if l.strip()]
    taches = {t["bloc"]: t for t in
              json.loads((ICI / "taches-edition.json").read_text(encoding="utf-8"))}
    changements = 0
    for r in resultats:
        tache = r["tache"]
        if tache not in garde:
            continue
        texte = garde[tache]
        mode = r["mode"]
        ancien = r["verdict"]
        try:
            if mode in ("editer-A", "ajouter-A", "ajouter-A2"):
                mat = extraire_notation(texte)
                ok, detail = round_trip(mat)
                nouveau = "ROUND-TRIP:OK" if ok else f"ROUND-TRIP-DIVERGENT:{detail[:80]}"
            elif mode in ("editer-H2", "ajouter-H2"):
                base = ((REPO / "loupe/notation" / f"{r['bloc']}.asm").read_text(
                    encoding="utf-8") if mode == "editer-H2" else GABARIT_BASE)
                _, detail = traiter_v2(base, texte)
                nouveau = f"APPLIQUE+ROUND-TRIP:OK ({detail[:40]})"
            else:
                continue
        except Refus as e:
            nouveau = f"REFUS {e.nom}: {e.detail[:80]}"
        except Exception as e:
            nouveau = f"ERREUR: {str(e)[:80]}"
        if nouveau != ancien:
            changements += 1
            print(f"{tache}: {ancien[:60]!r} -> {nouveau[:70]!r}")
            r["verdict"] = nouveau
            r["reconfronte"] = True
    (ICI / "resultats_opt05.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in resultats) + "\n",
        encoding="utf-8")
    print(f"{changements} verdict(s) re-confronté(s) — les pièces font foi")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
