#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA VAGUE 27 (édition v0.32.0) : la prose du manuscrit DÉRIVÉE des registres
— la même règle que D275 (la vague 25), reconduite : Data availability ←
DEPOTS.jsonl · Tamarin/ProVerif ← PREUVES-STATUTS.json · la spécification
accompagnée ← la pièce construite · les chaînes de version et la note de vague.
Chaque passe est VÉRIFIÉE par relecture du fichier écrit."""
import json, pathlib, re, sys

R = pathlib.Path(__file__).resolve().parents[2]
main = R / "edition-v0230" / "main.tex"
s = main.read_text(encoding="utf-8")

depots = [json.loads(l) for l in (R / "DEPOTS.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
preuves = json.loads((R / "PREUVES-STATUTS.json").read_text(encoding="utf-8"))
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
 f"for {VERS} respectively. This edition (v0.32.0) is \\emph{{not}}\n"
 "minted: the developer's deposit gesture is an explicit command, and until\n"
 "it is given the current snapshot has no version DOI of its own, which is\n"
 "why none is cited here. The two"
)
s = s[:i] + neuf + s[j:]

# ---------- 2. le statut Tamarin/ProVerif (dérivé du registre des preuves) ----------
vieux = ("The limits are named: the checker is an explicit-state explorer, and the symbolic\n"
         "side is a partial verdict --- tamarin-prover 1.12.0 + Maude 3.4 (installed at wave 14), model CF3-v3: VERIFIED (1,122 steps, 29.4 s),\n"
         "L1 incomplete at the 4 GiB memory wall and L2 incomplete at the memory wall (the named\n"
         "cause: proof-goal decomposition); the ProVerif port is delivered, run not executed;")
remp = ("The limits are named: the checker is an explicit-state explorer, and the symbolic\n"
        "side is a partial verdict --- tamarin-prover 1.12.0 + Maude 3.4 (installed at the\n"
        "laboratory at wave 27), model CF3-v3: L3 VERIFIED (1,122 steps, replayed\n"
        "bit-identically at wave 27), L1 and L2 incomplete at the 4 GiB memory wall; the\n"
        "wave-27 decomposition verifies two sub-lemmas natively (L1c, the three-held-leak\n"
        "bridge, 52 steps; L2a, the host-phrase chain, 7 steps), names the occurrence\n"
        "semantics of tamarin 1.12.0 that refuted the first L2b formulation (a tool\n"
        "semantic, not a protocol attack), and leaves the knowledge stage L1a and the\n"
        "full L1/L2 to the real-machine run kit; the ProVerif port is delivered, the\n"
        "prover absent from the laboratory (the named cause: every download route\n"
        "refused), its real-machine kit consigned at a logged fingerprint;")
assert vieux in s, "la prose Tamarin attendue est introuvable (le source a-t-il bougé ?)"
s = s.replace(vieux, remp)

# ---------- 3. la spécification accompagnée (la pièce construite) ----------
vieux_spec = "described in the protocol specification (the edition accompanied here is v0.15.16, which this edition accompanies;"
remp_spec = "described in the protocol specification (the edition accompanied here is v0.15.17, which this edition accompanies;"
assert vieux_spec in s, "la chaîne de spécification v0.15.16 est introuvable"
s = s.replace(vieux_spec, remp_spec)

# ---------- 4. les chaînes de version et la date ----------
for vieux, neuf in [
    ("pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent Governance (Academic Edition v0.31.0)}",
     "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent Governance (Academic Edition v0.32.0)}"),
    ("\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.31.0}",
     "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.32.0}"),
    ("\\date{24 November 2026 $\\cdot$ Academic edition v0.31.0}",
     "\\date{26 November 2026 $\\cdot$ Academic edition v0.32.0}"),
]:
    assert vieux in s, f"chaîne introuvable : {vieux[:60]}"
    s = s.replace(vieux, neuf)

# ---------- 5. la note de vague au changelog ----------
vieux_note = ("\\item v0.31.0 (24 Nov 2026) --- the present edition, the twenty-fourth wave: "
              "the targets, like the statuses, move into a registry (D276) --- one line per target with its exact "
              "subject, perimeter, pre-registered value, measurement and verdict, published in the proofs; the "
              "interleaved AES-GCM corridor is named what it is (measured at 1.26x EVP, no relative target of "
              "its own) while the 1.05x target belongs to the VAES corridor, which is not written; class C25 "
              "recomposes every published verdict from the registry. No measured value changed and no target re-aimed.\\end{itemize}")
remp_note = ("\\item v0.31.0 (24 Nov 2026) --- the twenty-fourth wave: the targets, like the statuses, move "
             "into a registry (D276) --- one line per target with its exact subject, perimeter, pre-registered "
             "value, measurement and verdict, published in the proofs; the interleaved AES-GCM corridor is "
             "named what it is (measured at 1.26x EVP, no relative target of its own) while the 1.05x target "
             "belongs to the VAES corridor, which is not written; class C25 recomposes every published verdict "
             "from the registry. No measured value changed and no target re-aimed.\n"
             "\\item v0.32.0 (26 Nov 2026) --- the present edition, the twenty-fifth wave: the pack's own "
             "review is answered at the source --- the D267 anchoring divergence between the five pieces is "
             "settled by deriving the single status from the append-only journal (class C26 recomposes every "
             "shared semantic status across all five pieces), the four editorial residues are closed (the "
             "fourteen signed trees of Table 12, the two wave-24 section titles distinguished, the French "
             "fragments of the English manuscript, the Book's chronology reordered; classes C27--C29), the "
             "targets registry gains its era table and every TENUE verdict cites its perimeter or carries the "
             "dated-historical label, the constrained-decoding campaign is delivered as a ready harness with "
             "the named SERVING-ABSENT refusal (the border accepts the schema field and does not apply it), "
             "the symbolic proofs advance natively (two sub-lemmas verified, the occurrence semantics of the "
             "checker named, the real-machine kit at a logged fingerprint), and the VAES corridor is written "
             "on its frozen notation and measured: the gate is green first (20/20 NIST vectors against the "
             "independent reference, the mutated variant refused at the first vector), the pre-registered "
             "1.05x target is MISSED at 5.66x EVP and published as missed, and the native oracle engine "
             "session runs the 235-vector corpus at 0.266 s median against its 10 s target. No measured value "
             "changed and no target re-aimed.\\end{itemize}")
assert vieux_note in s, "la note de vague v0.31.0 est introuvable"
s = s.replace(vieux_note, remp_note)

main.write_text(s, encoding="utf-8")

# ---------- la vérification par relecture ----------
s2 = main.read_text(encoding="utf-8")
verifs = [
    ("v0.32.0" in s2, "la version v0.32.0 portée"),
    ("the latest MINTED version is\nv0.31.0 (2026-11-26, version DOI 10.5281/zenodo.24545339)" in s2,
     "le dernier minté v0.31.0 (24545339)"),
    ("This edition (v0.32.0) is \\emph{not}\nminted" in s2, "la non-publication de v0.32.0 dite"),
    ("v0.15.17, which this edition accompanies" in s2, "la spécification accompagnée v0.15.17"),
    ("L1c, the three-held-leak\nbridge, 52 steps" in s2, "la décomposition L1c"),
    ("the twenty-fifth wave" in s2, "la note de vague vingt-cinquième"),
    ("26 November 2026" in s2, "la date du jour"),
]
ok = all(v for v, _ in verifs)
for v, nom in verifs:
    print(("VERT " if v else "ROUGE ") + nom)
sys.exit(0 if ok else 3)
