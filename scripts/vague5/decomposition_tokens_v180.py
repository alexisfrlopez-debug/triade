#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""decomposition_tokens_v180.py — LA DÉCOMPOSITION DES 53 158 / 67 475
TOKENS PAR CATÉGORIE (l'instruction 2l40ie6qn, point 3 : « décomposer les
53 158 vs 67 475 tokens de l'unité instrumentée par catégorie (lecture
contexte, écriture, raisonnement, itérations de compilation/débogage)
depuis les logs d'usage, et rapporter la décomposition dans §3.2 »).

LES CATÉGORIES (lues du journal, rien tapé) :
  — LECTURE DE CONTEXTE  : prompt_tokens (ce que l'agent lit)
  — ÉCRITURE             : completion_tokens (ce que l'agent rend)
  — ITÉRATIONS CORRECTIVES (compilation/débogage) : la phase « correctif »
  — RAISONNEMENT         : la ligne du log NE SÉPARE PAS les tokens de
    raisonnement de la complétion (l'API les compte ensemble) — le GAP est
    NOMMÉ, jamais estimé (le ×1,08 est interdit là où un log existe).
"""
import json
import pathlib

J = pathlib.Path(
    "/home/z/my-project/scripts/preuves_v150-local/journal_tokens.jsonl")
lignes = [json.loads(l) for l in J.read_text(encoding="utf-8").splitlines()]

PHASES = ["spec", "oracle", "notation", "source-c", "tests-c", "correctif"]


def agg(bras):
    par_phase = {p: {"appels": 0, "prompt": 0, "completion": 0}
                 for p in PHASES}
    for j in lignes:
        if j["bras"] != bras:
            continue
        p = par_phase[j["phase"]]
        p["appels"] += 1
        p["prompt"] += j["prompt_tokens"]
        p["completion"] += j["completion_tokens"]
    return par_phase


out = []
for bras in ("T", "C"):
    par = agg(bras)
    tot_prompt = sum(p["prompt"] for p in par.values())
    tot_compl = sum(p["completion"] for p in par.values())
    tot = tot_prompt + tot_compl
    corr = par["correctif"]
    out.append((bras, par, tot_prompt, tot_compl, tot, corr))

lignes_rapport = [
    "LA DÉCOMPOSITION DES TOKENS DE L'UNITÉ INSTRUMENTÉE (loupe-01, les",
    "DEUX bras — lue du journal d'usage, 20 appels, rien tapé à la main)",
    "(la vague 5, l'instruction 2l40ie6qn, point 3)",
    "=" * 88,
    f"{'catégorie':<34}{'bras T':>12}{'bras C':>12}{'part T':>9}{'part C':>9}",
    "-" * 88,
]
par_t, par_c = out[0][1], out[1][1]
tot_t, tot_c = out[0][4], out[1][4]
etiquettes = {"spec": "spécification (contrat lu/écrit)",
              "oracle": "oracle (dérivé du contrat)",
              "notation": "notation (écrite à la main)",
              "source-c": "source C (écrit)",
              "tests-c": "suite de tests C",
              "correctif": "ITÉRATIONS CORRECTIVES"}
for p in PHASES:
    vt = par_t[p]["prompt"] + par_t[p]["completion"]
    vc = par_c[p]["prompt"] + par_c[p]["completion"]
    if vt == 0 and vc == 0:
        continue
    lignes_rapport.append(
        f"{etiquettes[p]:<34}{vt:>12,}{vc:>12,}"
        f"{vt/tot_t*100:>8.1f}%{vc/tot_c*100:>8.1f}%".replace(",", " "))
lignes_rapport += [
    "-" * 88,
    f"{'LECTURE DE CONTEXTE (prompts)':<34}{out[0][2]:>12,}"
    f"{out[1][2]:>12,}{out[0][2]/tot_t*100:>8.1f}%"
    f"{out[1][2]/tot_c*100:>8.1f}%".replace(",", " "),
    f"{'ÉCRITURE (complétions)':<34}{out[0][3]:>12,}{out[1][3]:>12,}"
    f"{out[0][3]/tot_t*100:>8.1f}%{out[1][3]/tot_c*100:>8.1f}%".replace(",", " "),
    f"{'— dont ITÉRATIONS CORRECTIVES':<34}"
    f"{out[0][5]['prompt']+out[0][5]['completion']:>12,}"
    f"{out[1][5]['prompt']+out[1][5]['completion']:>12,}"
    f"{(out[0][5]['prompt']+out[0][5]['completion'])/tot_t*100:>8.1f}%"
    f"{(out[1][5]['prompt']+out[1][5]['completion'])/tot_c*100:>8.1f}%".replace(",", " "),
    f"{'   (appels correctifs)':<34}{out[0][5]['appels']:>12}"
    f"{out[1][5]['appels']:>12}",
    "-" * 88,
    f"{'TOTAL':<34}{tot_t:>12,}{tot_c:>12,}".replace(",", " "),
    "",
    "LE RAISONNEMENT : le GAP NOMMÉ — l'API compte le raisonnement DANS la",
    "complétion (jamais séparé au log) ; l'estimation ×1,08 est INTERDITE",
    "là où un log existe (la règle M2 du plan D204) : la catégorie",
    "« raisonnement » n'est PAS reconstruite.",
    "",
    "LA LECTURE : le CHEMIN CHAUD est le même aux deux bras — la spirale",
    "corrective (61,4 % de T, 58,1 % de C — l'Entrée 317 le nomma la",
    "première) ; la spécification et l'oracle coûtent PLUS au bras C",
    "(5 605/4 423 contre 5 313/3 752 : le contrat lu deux fois, l'oracle",
    "réécrit pour la suite standard) ; la notation T (11 480) contre le",
    "source C (14 660) : le C est PLUS LONG À ÉCRIRE que la notation — la",
    "première contre-intuition de H3.",
]
S = pathlib.Path("/home/z/my-project/livraison-vague5")
(S / "p9-decomposition-tokens.txt").write_text(
    "\n".join(lignes_rapport), encoding="utf-8")
print("\n".join(lignes_rapport))
