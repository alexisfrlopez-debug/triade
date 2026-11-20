#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""plancher_natif.py — LE PLANCHER ÉDITER RE-TOKENISÉ AU NATIF (zho5vilpy,
la correction (c) du PLAN-ZHO5VILPY.md) : la paire de lignes du diff réel
(« - ancienne / + nouvelle », la médiane 18 cl100k de la vague 9, le
plancher gelé du tableau de bord) MESURÉE AU CHAMP USAGE du CLI z-ai —
LE MÊME INSTRUMENT que la campagne (le compte est le LOG, jamais une
estimation). Le ratio au plancher rapporté NATIF/NATIF : le numérateur
674 (le gabarit TPL-EDIT-v1, la médiane du champ prompt de la campagne
gabarits) sur le plancher natif — la ligne cl100k historique demeure
DATÉE."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import statistics
import subprocess
import tempfile

ICI = pathlib.Path("/home/z/my-project/depot/atelier-medians-zho5vilpy")
PLANCHERS = ICI / "planchers_editer.json"
JOURNAL = ICI / "journal_plancher_natif.jsonl"
GARDE = ICI / "garde-plancher-natif.jsonl"


def horodatage() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def mesurer(prompt: str) -> dict:
    """LE PATRON D'APPEL (la campagne reconduite) : le CLI z-ai, le champ
    usage JOURNALISÉ — le compte natif du prompt tel que l'API le compte."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False,
                                     encoding="utf-8") as f:
        chemin = pathlib.Path(f.name)
    proc = subprocess.run(["z-ai", "chat", "--prompt", prompt,
                           "-o", str(chemin)],
                          capture_output=True, text=True, timeout=900)
    if proc.returncode != 0:
        chemin.unlink(missing_ok=True)
        raise RuntimeError(f"l'appel z-ai a échoué : {proc.stderr[:300]}")
    reponse = json.loads(chemin.read_text(encoding="utf-8"))
    with open(GARDE, "a", encoding="utf-8") as f:
        f.write(json.dumps({"horodatage": horodatage(), "phase":
                            "plancher-natif", "reponse_api": reponse},
                           ensure_ascii=False) + "\n")
    usage = reponse.get("usage") or {}
    ligne = {
        "horodatage": horodatage(), "phase": "plancher-natif",
        "id": reponse.get("id", ""), "modele": reponse.get("model", ""),
        "prompt_tokens": int(usage.get("prompt_tokens", 0)),
        "completion_tokens": int(usage.get("completion_tokens", 0)),
        "total_tokens": int(usage.get("total_tokens", 0)),
        "source": "log-api",
    }
    chemin.unlink(missing_ok=True)
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return ligne


def deja_faits() -> set:
    if not JOURNAL.exists():
        return set()
    faits = set()
    for l in JOURNAL.read_text(encoding="utf-8").splitlines():
        if l.strip():
            faits.add(json.loads(l)["bloc"])
    return faits


def main() -> int:
    planchers = json.loads(PLANCHERS.read_text(encoding="utf-8"))
    faits = deja_faits()
    for p in planchers:
        if p["bloc"] in faits:
            continue
        ligne = mesurer(p["planchier"] if False else p["plancher"])
        ligne["bloc"] = p["bloc"]
        ligne["cl100k"] = p["cl100k"]
        # la ligne complète ré-écrite (le journal porte le bloc)
        lignes = [json.loads(x) for x in
                  JOURNAL.read_text(encoding="utf-8").splitlines() if x.strip()]
        lignes[-1] = ligne
        JOURNAL.write_text("\n".join(json.dumps(x, ensure_ascii=False)
                                     for x in lignes) + "\n",
                           encoding="utf-8")
        print(f"  {p['bloc']}: natif {ligne['prompt_tokens']} "
              f"(cl100k {p['cl100k']})", flush=True)

    # ---- l'extraction ------------------------------------------------------
    res = [json.loads(l) for l in
           JOURNAL.read_text(encoding="utf-8").splitlines() if l.strip()]
    natifs = [r["prompt_tokens"] for r in res]
    cl = [r["cl100k"] for r in res]
    med_nat = statistics.median(natifs)
    med_cl = statistics.median(cl)
    # le numérateur : le gabarit TPL-EDIT-v1 (la médiane prompt de la
    # campagne gabarits o5apue194 — RECALCULÉE du JSONL brut)
    g = [json.loads(l) for l in
         (ICI.parent / "atelier-gabarits-o5apue194" /
          "resultats_gabarits.jsonl").read_text(encoding="utf-8").splitlines()
         if l.strip()]
    t2 = [r["prompt_tokens"] for r in g if r["mode"] == "editer-T2"]
    med_t2 = statistics.median(t2)
    rapport = [
        "LE PLANCHER ÉDITER AU NATIF (zho5vilpy, la correction (c))",
        "=" * 64,
        f"L'INSTRUMENT : le CLI z-ai, le champ usage LU ({len(res)} appels, "
        f"le journal journal_plancher_natif.jsonl — le compte est le LOG)",
        f"LE PLANCHER (la paire de lignes du diff réel, 18 mesures) :",
        f"  cl100k : {[v for _, v in sorted(zip([r['bloc'] for r in res], cl))]}",
        f"  natif  : {sorted(natifs)}",
        f"  LES MÉDIANES : cl100k {med_cl:.0f} (le plancher gelé de la "
        f"vague 9 REPRODUIT) ; NATIF {med_nat:.1f}",
        "",
        f"LE RATIO NATIF/NATIF : le numérateur {med_t2:.0f} (le gabarit "
        f"TPL-EDIT-v1, la médiane du champ prompt de la campagne gabarits, "
        f"RECALCULÉE du JSONL brut) ÷ le plancher natif {med_nat:.1f} = "
        f"{med_t2 / med_nat:.1f}×",
        f"LA LIGNE CL100K HISTORIQUE DEMEURE DATÉE : le ratio mixte 63,6× "
        f"de la v0.21.0 (le total 1 146 natif ÷ le plancher 18 cl100k — la "
        f"convention de périmètre de la vague 10, datée, jamais le courant)",
        "",
        f"LA CLÉ DU JOURNAL : sha256 "
        f"{hashlib.sha256(JOURNAL.read_bytes()).hexdigest()[:16]}…",
    ]
    (ICI / "rapport-plancher-natif.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
