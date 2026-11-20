#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extraire_fenetre.py — LA RE-DÉRIVATION de la campagne fenêtre depuis
les journaux bruts (le journal fait foi — la reprise idempotente : la
première exécution fut interrompue au milieu de la cellule F2 par une
faute de frappe locale ; les 18 appels H2 vivaient déjà au journal —
JAMAIS re-appelés, les verdicts re-dérivés des réponses conservées au
garde, la confrontation étant déterministe côté client)."""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
V8 = REPO / "atelier-opt05-pe6iv71fj"
sys.path.insert(0, str(V8))

from campagne_opt05 import charger as charger_v8  # noqa: E402
from client_hunks_v2 import traiter as traiter_v2, Refus  # noqa: E402

from campagne_fenetre import (gabarit_editer_fenetre, appliquer_f2,  # noqa
                               FENETRE_N)
import tiktoken  # noqa: E402

CL100K = tiktoken.get_encoding("cl100k_base")
JOURNAL = ICI / "journal_fenetre.jsonl"
GARDE = ICI / "garde-fenetre.jsonl"
PROMPTS = ICI / "garde-prompts"
RESULTATS = ICI / "resultats_fenetre.jsonl"


def main() -> int:
    vt, taches = charger_v8()
    par_id = {b["id"]: b for b in vt["blocs"]}
    journal = {json.loads(l)["tache"]: json.loads(l)
               for l in JOURNAL.read_text(encoding="utf-8").splitlines()
               if l.strip()}
    garde = {json.loads(l)["tache"]: json.loads(l)
             for l in GARDE.read_text(encoding="utf-8").splitlines()
             if l.strip()}

    lignes = []
    for tache, j in journal.items():
        if not tache.startswith("editer-"):
            continue
        mode, bid = tache.rsplit("-", 1)
        nom = par_id[bid]["nom"]
        notation = (REPO / "loupe" / "notation" /
                    f"{nom}.asm").read_text(encoding="utf-8")
        consigne = taches[nom]["consigne"]
        li = taches[nom]["ligne_index"]
        fenetre_texte = "\n".join(
            notation.split("\n")[max(0, li - FENETRE_N):li + FENETRE_N + 1])
        rep = garde[tache]["reponse_api"]["choices"][0]["message"]["content"]
        prompt = (PROMPTS / f"{tache}.txt").read_text(encoding="utf-8")
        try:
            if mode == "editer-H2":
                _, detail = traiter_v2(notation, rep)
                verdict = f"APPLIQUE+ROUND-TRIP:OK ({detail[:40]})"
            else:
                emp = hashlib.sha256(notation.encode("utf-8")).hexdigest()
                _, detail = appliquer_f2(notation, emp, rep)
                verdict = f"GARDE+APPLIQUE+ROUND-TRIP:OK ({detail[:40]})"
        except Refus as e:
            verdict = f"REFUS {e.nom}: {e.detail[:80]}"
        except Exception as e:
            verdict = f"ERREUR: {str(e)[:80]}"
        lignes.append({
            "tache": tache, "mode": mode, "bloc": nom, "verdict": verdict,
            "prompt_tokens": j["prompt_tokens"],
            "completion_tokens": j["completion_tokens"],
            "total_tokens": j["total_tokens"],
            "cl100k_prompt": len(CL100K.encode(prompt)),
            "cl100k_reponse": len(CL100K.encode(rep)),
            "retok_prompt": len(tiktoken.get_encoding("cl100k_base")
                                .encode_ordinary(prompt)),
            "retok_reponse": len(tiktoken.get_encoding("cl100k_base")
                                 .encode_ordinary(rep)),
            "materiau_fenetre_cl100k": (
                len(CL100K.encode(fenetre_texte)) if mode == "editer-F2"
                else len(CL100K.encode(notation))),
            "vert": verdict.startswith(("APPLIQUE", "GARDE")),
        })
    RESULTATS.write_text("\n".join(json.dumps(l, ensure_ascii=False)
                                    for l in lignes) + "\n",
                         encoding="utf-8")
    print(f"{len(lignes)} lignes re-dérivées au resultats_fenetre.jsonl")
    for l in sorted(lignes, key=lambda x: x["tache"]):
        print(f"  {l['tache']}: {l['total_tokens']} — {l['verdict'][:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
