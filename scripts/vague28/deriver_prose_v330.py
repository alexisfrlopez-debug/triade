#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA VAGUE 28 (édition v0.33.0) : la prose du manuscrit DÉRIVÉE des registres
— la règle D275 reconduite : Data availability ← DEPOTS.jsonl · la
spécification accompagnée ← la pièce construite · les chaînes de version.
Chaque passe est VÉRIFIÉE par relecture du fichier écrit."""
import json, pathlib, sys

R = pathlib.Path(__file__).resolve().parents[2]
main = R / "edition-v0230" / "main.tex"
s = main.read_text(encoding="utf-8")

depots = [json.loads(l) for l in (R / "DEPOTS.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
publies = [d for d in depots if d["statut"] == "publie"]
dernier = publies[0]
DOIS = ", ".join("10.5281/zenodo." + d["doi_version"].split(".")[-1] for d in publies)
VERS = ", ".join(d["version"] for d in publies)
assert dernier["version"] == "v0.31.0", "le registre doit nommer v0.31.0 comme dernière publiée"

# ---------- 1. Data availability (dérivé du registre des dépôts) ----------
i = s.index("\\paragraph{Data availability.}")
j = s.index("\n\\paragraph{", i + 10)
neuf = (
 "\\paragraph{Data availability.} All primary data is public in the project\n"
 "repository (append-only journal, decision log, evidence vault indexes,\n"
 "extraction script, generated tables) and in the versioned archival\n"
 "snapshots at the concept DOI \\doiConcept{} --- the latest MINTED version is\n"
 f"{dernier['version']} ({dernier['date']}, version DOI {dernier['doi_version']}).\n"
 "The deposits are recorded one line each in the deposit registry\n"
 "(\\code{DEPOTS.jsonl}) and this paragraph is derived from it: the dated\n"
 f"version DOIs are {DOIS}\n"
 f"for {VERS} respectively. This edition (v0.33.0) is \\emph{{not}}\n"
 "minted: the developer's deposit gesture is an explicit command, and until\n"
 "it is given the current snapshot has no version DOI of its own, which is\n"
 "why none is cited here. The two"
)
s = s[:i] + neuf + s[j:]

# ---------- 2. la spécification accompagnée (la pièce construite) ----------
vieux_spec = "described in the protocol specification (the edition accompanied here is v0.15.17, which this edition accompanies;"
remp_spec = "described in the protocol specification (the edition accompanied here is v0.15.18, which this edition accompanies;"
assert vieux_spec in s, "la chaîne de spécification v0.15.17 est introuvable"
s = s.replace(vieux_spec, remp_spec)

# ---------- 3. les chaînes de version et la date ----------
for vieux, neuf in [
    ("pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent Governance (Academic Edition v0.32.0)}",
     "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent Governance (Academic Edition v0.33.0)}"),
    ("\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.32.0}",
     "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.33.0}"),
    ("\\date{26 November 2026 $\\cdot$ Academic edition v0.32.0}",
     "\\date{26 November 2026 $\\cdot$ Academic edition v0.33.0}"),
]:
    assert vieux in s, f"chaîne introuvable : {vieux[:60]}"
    s = s.replace(vieux, neuf)

main.write_text(s, encoding="utf-8")

# ---------- la vérification par relecture ----------
s2 = main.read_text(encoding="utf-8")
verifs = [
    ("v0.33.0" in s2, "la version v0.33.0 portée"),
    ("the latest MINTED version is\nv0.31.0 (2026-11-26, version DOI 10.5281/zenodo.24545339)" in s2,
     "le dernier minté v0.31.0 (24545339)"),
    ("This edition (v0.33.0) is \\emph{not}\nminted" in s2, "la non-publication de v0.33.0 dite"),
    ("v0.15.18, which this edition accompanies" in s2, "la spécification accompagnée v0.15.18"),
    ("pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent Governance (Academic Edition v0.33.0)}" in s2,
     "le pdftitle v0.33.0"),
]
ok = True
for cond, nom in verifs:
    print(("  OK " if cond else "  ROUGE ") + nom)
    ok = ok and cond
if not ok:
    sys.exit(1)
print("[deriver-v330] la prose dérivée des registres — les cinq vérifications vertes")
