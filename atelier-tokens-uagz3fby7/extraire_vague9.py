#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extraire_vague9.py — L'EXTRACTION DE LA CAMPAGNE (jamais tapée à la
main) : les distributions par cellule (n, médiane, q1, q3, min, max par
champ), les verdicts, ET LES RATIOS AU PLANCHER (H6 du PLAN-UAGZ3FBY7) :
le total mesuré ÷ la longueur tokenisée (cl100k_base, l'instrument
parallèle consigné depuis OPT-02) du diff réel — le plancher de
description minimale NOMMÉ avec sa méthode."""
from __future__ import annotations

import json
import pathlib
import statistics

import tiktoken

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-tokens-uagz3fby7"
V8 = REPO / "atelier-opt05-pe6iv71fj"

enc = tiktoken.get_encoding("cl100k_base")


def tokens_cl100k(texte: str) -> int:
    return len(enc.encode(texte))


def dedupe(chemin: pathlib.Path) -> list[dict]:
    """les DOUBLONS du journal cassé : la PREMIÈRE occurrence fait foi
    (l'horodatage le plus ancien)."""
    vus, out = set(), []
    for l in open(chemin, encoding="utf-8"):
        if not l.strip():
            continue
        r = json.loads(l)
        if r["tache"] in vus:
            continue
        vus.add(r["tache"])
        out.append(r)
    return out


def dist(vals: list) -> dict:
    if not vals:
        return {}
    q = statistics.quantiles(vals, n=4) if len(vals) >= 4 else \
        [vals[0], vals[0], vals[-1]]
    return {"n": len(vals), "mediane": statistics.median(vals),
            "q1": q[0], "q3": q[2], "min": min(vals), "max": max(vals)}


def main():
    res = dedupe(ICI / "resultats_vague9.jsonl")
    rapport = ["LA CAMPAGNE VAGUE 9 — L'EXTRACTION (les distributions "
               "complètes, jamais tapées)", ""]
    # les cellules
    cellules = {}
    for mode in ("editer-H2", "ajouter-H3", "composer-G", "localiser-P"):
        sub = [r for r in res if r["mode"] == mode]
        if not sub:
            continue
        verts = sum(1 for r in sub if ("OK" in r["verdict"] or
                                       "CONFORME" in r["verdict"]))
        cellules[mode] = {
            "total": dist([r["tokens"] for r in sub]),
            "prompt": dist([r["prompt_tokens"] for r in sub]),
            "reponse": dist([r["completion_tokens"] for r in sub]),
            "verts": verts, "n": len(sub),
        }
        d = cellules[mode]["total"]
        r = cellules[mode]["reponse"]
        rapport.append(
            f"  {mode}: n={len(sub)}, verts {verts}/{len(sub)} — total "
            f"médiane {d.get('mediane', 0):.0f} [q1 {d.get('q1', 0):.0f}, "
            f"q3 {d.get('q3', 0):.0f}], réponse médiane "
            f"{r.get('mediane', 0):.0f}")

    # LES RATIOS AU PLANCHER (H6) : le diff réel tokenisé (cl100k_base)
    # — éditer : les lignes changées des tâches gelées (la consigne
    #   l'écrit : ancienne → nouvelle — le diff minimal = la ligne
    #   retirée + la ligne posée)
    # — localiser : le pointeur (l'identifiant + l'empreinte) = le
    #   plancher LITTÉRAL de la réponse
    # — ajouter/composer : la notation du bloc (le matériau minimal que
    #   TOUTE réponse doit porter — le plancher HAUT : l'unité entière)
    taches = {t["bloc"]: t for t in json.loads(
        (V8 / "taches-edition.json").read_text(encoding="utf-8"))}
    vt = json.loads((REPO / "atelier-localiser-5gfx6pwkj" /
                     "verites-terrain.json").read_text(encoding="utf-8"))
    par_id = {b["id"]: b for b in vt["blocs"]}

    planchers = {}
    # éditer : le diff réel = « - ancienne » + « + nouvelle » par tâche
    diffs = []
    for r in res:
        if r["mode"] != "editer-H2":
            continue
        t = taches.get(r["bloc"])
        if not t:
            continue
        diffs.append(tokens_cl100k(f"- {t['ancienne']}\n+ {t['nouvelle']}\n"))
    if diffs:
        planchers["editer-H2"] = statistics.median(diffs)
    # localiser : le pointeur littéral
    ptrs = []
    for r in res:
        if r["mode"] != "localiser-P":
            continue
        bid = [k for k, v in par_id.items() if v["nom"] == r["bloc"]]
        if bid:
            ptrs.append(tokens_cl100k(
                f"{bid[0]} · sha256:{'0' * 64}"))
    if ptrs:
        planchers["localiser-P"] = statistics.median(ptrs)
    # ajouter/composer : le corps du bloc (le matériau de la réponse)
    for mode, gab in (("ajouter-H3", None), ("composer-G", None)):
        corps = []
        for r in res:
            if r["mode"] != mode:
                continue
            try:
                notation = (REPO / "loupe/notation" /
                            f"{r['bloc']}.asm").read_text(encoding="utf-8")
                corps.append(tokens_cl100k(notation))
            except FileNotFoundError:
                pass
        if corps:
            planchers[mode] = statistics.median(corps)

    rapport += ["", "LES RATIOS AU PLANCHER (le total mesuré ÷ le plancher",
                "de description minimale, la méthode cl100k_base — la "
                "convention de périmètre : le TOTAL (matériau + prose + "
                "réponse) rapporté, chaque champ consigné séparément) :"]
    for mode, p in planchers.items():
        if mode in cellules and p:
            m = cellules[mode]["total"]["mediane"]
            rapport.append(f"  {mode}: médiane {m:.0f} ÷ plancher {p:.0f} "
                           f"= {m / p:.2f}×")
    rapport += ["",
                "LA MÉTHODE DU PLANCHER (nommée) : éditer — la paire de "
                "lignes (retrait + pose) du diff réel, tokenisée ; "
                "localiser — le pointeur littéral (l'identifiant + "
                "l'empreinte) ; ajouter/composer — le corps du bloc (le "
                "matériau que TOUTE réponse doit porter : le plancher HAUT "
                "de l'unité entière) — la re-tokenisation indépendante à "
                "±1 token (la règle OPT-02 reconduite)."]
    (ICI / "extraire_vague9_rapport.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    (ICI / "extraire_vague9.json").write_text(json.dumps(
        {"cellules": cellules, "planchers": planchers}, indent=1,
        ensure_ascii=False), encoding="utf-8")
    print("\n".join(rapport))


if __name__ == "__main__":
    main()
