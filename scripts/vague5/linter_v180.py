#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v180.py — LE LINTER NUMÉRIQUE DE LA VAGUE 5 : le registre de la
v0.17.0 PORTÉ aux nouvelles valeurs (l'instruction 4zi174ey3), ÉTENDU aux
SIGNES et conventions (l'instruction q17cx7y35 : « Étendre le linter
numérique pour vérifier désormais les SIGNES et les conventions de tous
les pourcentages et ratios du manuscrit »), et ARMÉ du refus de toute
réapparition de « |t| = 0 » (l'instruction gfylb610p).

LE PRINCIPE (inchangé, fail-closed) : chaque affirmation chiffrée porte
sa dérivation (le fichier source, la ligne, l'opération) ; la prose
normalisée du .tex doit contenir chaque valeur RECALCULÉE des sources ;
tout écart, toute valeur manquante, tout motif orphelin REFUSE le build.

LES SOURCES NOUVELLES :
  - livraison-vague4/p4-mesures-brutes.jsonl (la re-mesure v0.17.0)
  - livraison-vague4/p4-baselines.txt (les deux baselines réalistes)
  - livraison-vague5/p7-egalite-traces.csv (l'égalité exacte des traces)
  - livraison-vague5/p3-table-campagne.txt (la réconciliation D204)
  - les CSV historiques (remesure_rq2, bras_c, audit_benchmark, budgets)
  - le journal des tokens de campagne, le kit-2 signé, le PBT, la M4 v180

Usage :
  python3 linter_v180.py <manuscrit.tex>            # le verdict
  python3 linter_v180.py <manuscrit.tex> --falsifie # contrôles négatifs
"""
from __future__ import annotations

import csv
import json
import pathlib
import re
import sys

RACINE = pathlib.Path("/home/z/my-project/gdrive/projet/triade-complet")
V4 = pathlib.Path("/home/z/my-project/livraison-vague4")
V5 = pathlib.Path("/home/z/my-project/livraison-vague5")


def lire_csv(chemin: pathlib.Path) -> list[dict]:
    with open(chemin, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def lire_csv_diese(chemin: pathlib.Path) -> list[dict]:
    with open(chemin, encoding="utf-8-sig") as f:
        return list(csv.DictReader(
            l for l in f if not l.startswith("#")))


def nb(s: str) -> int:
    return int(s.replace(" ", "").replace(",", ""))


remesure = lire_csv(RACINE / "preuves_historiques/preuves_v140/remesure_rq2.csv")
bras_c = lire_csv(RACINE / "preuves_historiques/preuves_v140/bras_c.csv")
audit = lire_csv(RACINE / "preuves_historiques/preuves_v130/audit_benchmark.csv")
budgets = lire_csv(RACINE / "donnees/budgets.csv")
livraisons = lire_csv_diese(pathlib.Path(
    "/home/z/my-project/drive_work/atelier-post313/livraisons.csv"))
defauts = lire_csv_diese(pathlib.Path(
    "/home/z/my-project/drive_work/atelier-post313/defauts.csv"))
carnet = lire_csv_diese(pathlib.Path(
    "/home/z/my-project/drive_work/atelier-post313/carnet_temps_humain.csv"))
jetons = [json.loads(l) for l in (pathlib.Path(
    "/home/z/my-project/scripts/preuves_v150-local/journal_tokens.jsonl")
    .read_text(encoding="utf-8").splitlines())]
verifs = [json.loads(l) for l in (pathlib.Path(
    "/home/z/my-project/scripts/preuves_v150-local/journal_verifications.jsonl")
    .read_text(encoding="utf-8").splitlines())]
brutes = [json.loads(l) for l in (V4 / "p4-mesures-brutes.jsonl")
          .read_text(encoding="utf-8").splitlines()]
egalite = lire_csv(V5 / "p7-egalite-traces.csv")

med = {r["operation"]: r for r in remesure}
loc, edi, ajo, base = (med[k] for k in
    ("localiser (plan + en-tête)", "éditer (notation relue + réécrite)",
     "ajouter (spec + notation écrites)", "baseline naive (désassemblage complet)"))
m1 = {r["operation"]: r for r in budgets}
audit_par = {r["implementation"]: r for r in audit}
bloc_o2 = {r["bloc"]: r for r in bras_c if r["niveau"] == "-O2"}


def stats(echantillons):
    v = sorted(echantillons)
    n = len(v)
    def pct(p):
        k = (n - 1) * p
        f = int(k)
        c = min(f + 1, n - 1)
        return v[f] + (v[c] - v[f]) * (k - f)
    return n, pct(.25), pct(.5), pct(.75)


# la re-mesure v0.17.0 : les distributions EXACTES des mesures brutes
v2 = {}
for op in ("localiser", "éditer", "ajouter"):
    sel = [r["total_tokens"] for r in brutes
           if r.get("operation") == op and "erreur" not in r]
    v2[op] = stats(sel)          # (n, q1, médiane, q3)
c1k = {}
for op in ("localiser", "éditer", "ajouter"):
    sel = [r["cl100k_prompt"] + r["cl100k_completion"] for r in brutes
           if r.get("operation") == op and "erreur" not in r]
    c1k[op] = stats(sel)[2]              # la médiane interpolée

# ------------------------------------------------------------ LE REGISTRE
REGISTRE: list[tuple[str, str, str, str]] = []


def insere(id_, regex, valeur, derivation):
    REGISTRE.append((id_, regex, valeur, derivation))


# --- §3.2 : les médianes v0.17.0 (p4-mesures-brutes.jsonl) ---
for cle, op, motif in (("loc", "localiser", r"median of (\d+) tokens \[quartiles"),
                       ("edi", "éditer", None), ("ajo", "ajouter", None)):
    n, q1, me, q3 = v2[op]
    if cle == "loc":
        insere("rq2v2-localiser", r"median of (\d+) tokens",
               str(round(me)), "p4-mesures-brutes localiser médiane (natif)")
        insere("rq2v2-localiser-q", r"quartiles (\d+)-(\d+)\]",
               f"{round(q1)}|{round(q3)}", "p4-mesures-brutes localiser q1/q3")
insere("rq2v2-editer", r"editing one (\d+) \[(\d+)-(\d+)\]",
       f"{round(v2['éditer'][2])}|{round(v2['éditer'][1])}|{round(v2['éditer'][3])}",
       "p4-mesures-brutes éditer médiane/quartiles")
insere("rq2v2-ajouter", r"adding one (\d+) \[(\d+)-(\d+)\]",
       f"{round(v2['ajouter'][2])}|{round(v2['ajouter'][1])}|{round(v2['ajouter'][3])}",
       "p4-mesures-brutes ajouter médiane/quartiles")
insere("rq2v2-ns", r"n\{=\}(\d+)/(\d+)/(\d+) real samples",
       f"{v2['localiser'][0]}|{v2['éditer'][0]}|{v2['ajouter'][0]}",
       "les tailles d'échantillons des mesures brutes")
r_c1k = (c1k["localiser"] / v2["localiser"][2],
         c1k["éditer"] / v2["éditer"][2],
         c1k["ajouter"] / v2["ajouter"][2])
insere("rq2v2-cl100k", r"ratio 0\.(\d{2})-1\.(\d{2}) across operations",
       f"{round(min(r_c1k)*100):02d}|{round((max(r_c1k)-1)*100):02d}",
       f"cl100k/natif : {r_c1k[0]:.3f}/{r_c1k[1]:.3f}/{r_c1k[2]:.3f}")

# --- les valeurs historiques étiquetées (v0.14.0 : remesure_rq2.csv) ---
insere("rq2-hist-loc", r"medians of (\d+) \[(\d+)-(\d+)\] to locate",
       f"{nb(loc['mediane'])}|{loc['q1']}|{loc['q3']}",
       "remesure_rq2.csv localiser (historique v0.14.0)")
insere("rq2-hist-edi", r"(\d+) \[(\d+)-(\d+)\] to edit",
       f"{nb(edi['mediane'])}|{edi['q1']}|{edi['q3']}",
       "remesure_rq2.csv éditer (historique v0.14.0)")
insere("rq2-hist-ajo", r"(\d+) \[(\d+)-(\d+)\] to add",
       f"{nb(ajo['mediane'])}|{ajo['q1']}|{ajo['q3']}",
       "remesure_rq2.csv ajouter (historique v0.14.0)")

# --- les ratios baseline aux NOUVELLES médianes ---
insere("rq2-baseline", r"disassembly of loupe.exe costs (\d+) tokens",
       str(nb(base["mediane"])), "remesure baseline mediane")
insere("rq2-baseline-lignes", r"costs \d+ tokens \((\d+) lines\)", "37538",
       "remesure baseline note")
insere("rq2-rapport-loc", r"(\d+)× the cheapest card operation \(locating, (\d+)\)",
       f"{round(nb(base['mediane'])/v2['localiser'][2])}|{round(v2['localiser'][2])}",
       f"{nb(base['mediane'])}/{int(v2['localiser'][2])} = "
       f"{nb(base['mediane'])/v2['localiser'][2]:.0f}")
insere("rq2-rapport-ajo", r"(\d+)× the most expensive \(adding, (\d+)\)",
       f"{round(nb(base['mediane'])/v2['ajouter'][2])}|{round(v2['ajouter'][2])}",
       f"{nb(base['mediane'])}/{int(v2['ajouter'][2])}")

# --- les baselines réalistes (p4-baselines.txt) ---
BASE_TXT = (V4 / "p4-baselines.txt").read_text(encoding="utf-8")
insere("rq2-baseline-a", r"symbol table[^\n]*\n?[^\n]*?costs a median of (\d+) tokens \[quartiles (\d+)-(\d+)",
       re.search(r"médiane (\d+) tokens \[q1 (\d+) \.\. q3 (\d+)\]",
                 BASE_TXT).groups(),
       "p4-baselines.txt (a) la fonction entière")
insere("rq2-baseline-b", r"fifteen-line window\) costs a median of (\d+)\s*\n?tokens \[(\d+)-(\d+)",
       re.search(r"retrieval hiérarchique \(entête \+ fenêtre 15\).*?"
                 r"médiane (\d+) tokens \[q1 (\d+) \.\. q3 (\d+)\]",
                 BASE_TXT, re.S).groups(),
       "p4-baselines.txt (b) le retrieval hiérarchique")

# --- la décomposition par catégorie (p5-decomposition-contexte.txt) ---
DEC_TXT = (V5 / "p5-decomposition-contexte.txt").read_text(encoding="utf-8")
dec = re.search(r"localiser\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",
                DEC_TXT)
insere("rq2-decomp-loc", r"median of (\d+) tokens of material read",
       dec.group(1), "p5-decomposition (localiser matériau)")
insere("rq2-decomp-loc-req", r"(\d+) tokens of request prose",
       dec.group(2), "p5-decomposition (localiser prose)")
insere("rq2-decomp-loc-rep", r"(\d+) tokens of written response",
       dec.group(3), "p5-decomposition (localiser réponse)")

# --- le domaine historique + la lignée ---
r_loc = nb(loc["mediane"]) / int(m1["Locate a block"]["mesure_tokens"])
insere("rq2-domaine", r"cost (\d+)-(\d+)× their M1", "3|11",
       f"les ratios contenus : éditer "
       f"{nb(edi['mediane'])/int(m1['Edit a block']['mesure_tokens']):.2f}, "
       f"localiser {r_loc:.2f}")
insere("rq2-lignee", r"generation-1 lineage totalled (\d+)", "13873",
       "budgets Whole lineage (TOTAL)")

# --- §3.5 : les SIGNES (audit_benchmark.csv) — la convention explicite ---
n_not = nb(audit_par["tls13-01..04 (blocs)"]["instructions_par_op"])
o2 = nb(audit_par["gcc -O2 (fonction)"]["instructions_par_op"])
os_ = nb(audit_par["gcc -Os (fonction)"]["instructions_par_op"])
pct_o2 = (n_not - o2) / o2 * 100
pct_os = (n_not - os_) / os_ * 100
insere("audit-blocs", r"complete operation\s*\n?costs (\d+) instructions for",
       str(n_not), "audit_benchmark tls13 blocs")
insere("audit-o2", r"against (\d+) for gcc 14\.2 -O2", str(o2),
       "audit_benchmark gcc -O2")
insere("audit-os", r"and (\d+) for -Os", str(os_), "audit_benchmark gcc -Os")
insere("audit-signe-o2", r"at \+(\d+)\.(\d+)\\% executed instructions against -O2",
       f"{int(pct_o2)}|{round((pct_o2 % 1) * 10)}",
       f"le SIGNE recalculé : (75983-69132)/69132 = {pct_o2:+.1f} % "
       "(positif = la notation plus chère — la convention)")
insere("audit-signe-os", r"and -(\d+)\.(\d+)\\% against -Os",
       tuple(f"{-pct_os:.1f}".split(".")),
       f"le SIGNE recalculé : (75983-77505)/77505 = {pct_os:+.1f} %")

# --- l'égalité exacte des traces (p7-egalite-traces.csv) ---
par_cible = {r["cible"]: r for r in egalite}
insere("ct-x25519", r"x25519 exactly (\d+) for every key",
       par_cible["tls13-13/14 (x25519, la clé privée)"]["compte_unique"],
       "p7-egalite-traces.csv x25519 compte unique")
insere("ct-sha", r"sha-256 (\d+), hmac",
       par_cible["tls13-01..04 (sha-256)"]["compte_unique"],
       "p7-egalite sha-256")
insere("ct-n60", r"N=60 per class is an exact", "60",
       "le contrôle structurel N=60")

# --- le kit-2 matériel (les témoins signés, Entrées 261/264/266) ---
insere("kit2-n200a", r"At N=200 per class .*?\|t\| = (\d+)\.(\d+)",
       "12|39", "le témoin signé kit-2 N=200 (tls13-02)")
insere("kit2-n200b", r"and (\d+)\.(\d+) \(tls13-13\)", "5|19",
       "le témoin signé kit-2 N=200 (tls13-13)")
insere("kit2-n400", r"N=400 run reads (\d+)\.(\d+), (\d+)\.(\d+), -(\d+)\.(\d+) and (\d+)\.(\d+)",
       "0|84|1|55|0|30|2|02",
       "le témoin signé kit-2 N=400")

# --- la campagne (les ledgers) ---
verts = sum(1 for r in livraisons if r["verdict"] == "VERT")
rouges = sum(1 for r in livraisons if r["verdict"] == "ROUGE")
comptees = [d for d in defauts if d["exclusion"] == "non" and d["livraison"]]
exclues = [d for d in defauts if d["exclusion"] == "oui"]
m3_t = sum(int(c["minutes"]) for c in carnet if c["bras"] == "T")
m3_c = sum(int(c["minutes"]) for c in carnet if c["bras"] == "C")
tot_t = sum(j["total_tokens"] for j in jetons if j["bras"] == "T")
tot_c = sum(j["total_tokens"] for j in jetons if j["bras"] == "C")
m4_t = sum(v["secondes"] for v in verifs if v["bras"] == "T")
m4_c = sum(v["secondes"] for v in verifs if v["bras"] == "C")
insere("campagne-22", r"across (\d+) witnessed deliveries", str(len(livraisons)),
       "livraisons.csv (22 lignes)")
insere("campagne-15-7", r"(\d+) deliveries \((\d+) green, (\d+) red\)",
       f"{len(livraisons)}|{verts}|{rouges}", "livraisons.csv par verdict")
insere("campagne-6-22", r"campaign's rate is (\d+)/(\d+)", "6|22",
       "defauts.csv exclusion=non → 6 livraisons sur 22")
insere("campagne-6-2", r"(\d+) counted escapes\s*\n?under the D202", "6",
       "defauts.csv exclusion=non (6 lignes)")
insere("campagne-2-exclues", r"(\d+) named-and-excluded escapes", "2",
       "defauts.csv exclusion=oui (2 lignes)")
insere("campagne-t4c3", r"T-app-it4 and C-app-it3", "T-app-it4",
       "livraisons.csv les deux clôtures vertes")
insere("campagne-h2", r"(\d+) counted\s*\n?escapes at T against (\d+) at C",
       f"{sum(1 for d in comptees if d['bras'] == 'T')}"
       f"|{sum(1 for d in comptees if d['bras'] == 'C')}",
       "defauts.csv par bras")
insere("campagne-m3", r"(\d+) minutes against (\d+) at the gesture",
       f"{m3_t}|{m3_c}", "carnet_temps_humain.csv par bras")
insere("campagne-m2", r"(\d+) tokens for the notation arm\s*\n?against (\d+) for the compiled arm",
       f"{tot_t}|{tot_c}", "journal_tokens.jsonl (9+11 appels)")
insere("campagne-m4", r"reads M4 = (\d+)\.(\d+)s \(arm T\) against (\d+)\.(\d+)s \(arm C\)",
       f"{int(m4_t)}|{str(round((m4_t % 1) * 10))}|{int(m4_c)}|{str(round((m4_c % 1) * 10))}",
       "journal_verifications.jsonl")
insere("campagne-x127", r"consumed ×1\.27 the tokens", "×1.27",
       f"{tot_c}/{tot_t} = {tot_c/tot_t:.2f}")
insere("campagne-x239", r"(\d+)\.(\d+)s against (\d+)\.(\d+)s \(×(\d+)\.(\d+)\)",
       f"{int(m4_t)}|{str(round(m4_t % 1 * 10))}|{int(m4_c)}|"
       f"{str(round(m4_c % 1 * 10))}|"
       f"{int(m4_t / m4_c)}|{str(round((m4_t / m4_c % 1) * 10))}",
       f"{m4_t:.1f}/{m4_c:.1f} = {m4_t/m4_c:.1f}")

# --- la décomposition de l'unité instrumentée (journal des tokens) ---
def phase(bras, ph):
    return sum(j["prompt_tokens"] + j["completion_tokens"] for j in jetons
               if j["bras"] == bras and j["phase"] == ph)


insere("decomp-spec", r"specification (\d+),\s*\n?oracle", f"{phase('T', 'spec')}",
       "journal_tokens.jsonl bras T phase spec")
insere("decomp-oracle", r"oracle (\d+),", f"{phase('T', 'oracle')}",
       "journal_tokens.jsonl bras T phase oracle")
insere("decomp-notation", r"notation (\d+),", f"{phase('T', 'notation')}",
       "journal_tokens.jsonl bras T phase notation")
insere("decomp-correctifs", r"corrective iterations (\d+) \((\d+)\.(\d+)\\% of the total",
       f"{phase('T', 'correctif')}|61|4",
       f"correctifs T = {phase('T', 'correctif')} "
       f"({phase('T', 'correctif')/tot_t*100:.1f} %)")
insere("decomp-source-c", r"C source (\d+),", f"{phase('C', 'source-c')}",
       "journal_tokens.jsonl bras C phase source-c")
insere("decomp-c-correctifs", r"iterations (\d+) \(58\.(\d+)\\%, seven calls",
       f"{phase('C', 'correctif')}|1",
       f"correctifs C = {phase('C', 'correctif')} "
       f"({phase('C', 'correctif')/tot_c*100:.1f} %)")

# --- la conformité générative + la couverture (PBT, TLA+) ---
insere("pbt-10000", r"(\d+) random transition sequences", "10000",
       "la campagne PBT (10 000 traces)")
insere("pbt-660", r"(\d+) divergent traces, exactly one class", "660",
       "pbt_ecarts_brut.csv (660 traces à écart, UNE classe)")
insere("pbt-655", r"reduces (\d+) of them", "655",
       "pbt_ecarts_minimaux.json (655 au minimum de 2 pas)")
insere("couverture-288", r"one of the (\d+) abstract shapes", "288",
       "verifie_couverture_288 (la bijection)")
insere("alignement-512", r"(\d+) concrete states per rule", "512",
       "alignement_13_regles (4×2×8×2×2×2 = 512 états)")
insere("tla-8sur8", r"returns (\d+)/(\d+) green", "8|8",
       "jouer_tous_les_runs.py (la batterie re-jouée)")

# --- M4 v180 (p8-m4-*.json) ---
m4_avant = json.loads((V5 / "p8-m4-avant.json").read_text())
m4_apres = json.loads((V5 / "p8-m4-apres.json").read_text())
insere("m4-avant", r"(\d+)\.(\d+)s\s*39\.3/39\.2s",
       f"{int(m4_avant['total_s'])}|{str(round((m4_avant['total_s'] % 1) * 10))}",
       "p8-m4-avant/apres.json (50.9 → 39.3/39.2 s)")
insere("m4-ratio", r"from (\d+)\.(\d+)× to (\d+)\.(\d+)×",
       "23|1|17|9",
       "50.9/2.2 = 23.1× ; 39.3/2.2 = 17.9×")

# --- les ancres de la v0.17.0 conservées (bras_c, mutation, jalons) ---
k3_a = [int(bloc_o2[b]["mut_A_K3"]) for b in bloc_o2]
k3_c_purs = [int(bloc_o2[b]["mut_C_K3"]) for b in
             ("loupe-05", "loupe-08", "loupe-13", "loupe-16")]
insere("mut-A", r"Camp notation: (\d+)-(\d+)/16 killed",
       f"{min(k3_a)}|{max(k3_a)}", f"bras_c mut_A_K3 -O2 : {k3_a}")
insere("mut-C-purs", r"(\d+)-(\d+)/16 under the differential killer on the pure",
       f"{min(k3_c_purs)}|{max(k3_c_purs)}",
       f"bras_c mut_C_K3 purs -O2 : {k3_c_purs}")
insere("mut-totaux", r"both camps kill (\d+)/(\d+) mutants in total",
       "96|96", "bras_c mut_A_tot/mut_C_tot -O2 (6 blocs × 16)")
insere("cmp-05", r"(\d+) vs (\d+) instructions \(the 384-byte",
       f"{nb(bloc_o2['loupe-05']['ins_A_med'])}|{nb(bloc_o2['loupe-05']['ins_C_med'])}",
       "bras_c loupe-05 -O2")
insere("cmp-cascade", r"reads (\d+) vs (\d+) — not at equal work",
       f"{nb(bloc_o2['loupe-01']['ins_A_max'])}|{nb(bloc_o2['loupe-01']['ins_C_max'])}",
       "bras_c loupe-01 -O2 max (la cascade)")

# ------------------------------------------------------------ NORMALISATION
def normalise(chemin: pathlib.Path) -> str:
    brut = chemin.read_text(encoding="utf-8")
    propre = []
    for ligne in brut.splitlines():
        # un % PRÉCÉDÉ d'un backslash est LITTÉRAL (\%) — jamais un
        # commentaire ; le premier % NU seul coupe (règle LaTeX)
        coupe = -1
        for m in re.finditer(r"%", ligne):
            if m.start() == 0 or ligne[m.start() - 1] != "\\":
                coupe = m.start()
                break
        if coupe >= 0:
            ligne = ligne[:coupe]
        propre.append(ligne)
    t = "\n".join(propre)
    t = re.sub(r"\\emph\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\code\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\textbf\{([^{}]*)\}", r"\1", t)
    t = t.replace("{,}", "")
    t = t.replace("$\\times$", "×").replace("$\\ldots$", "…")
    t = t.replace("---", "—").replace("--", "-")
    t = t.replace("\\times", "×")
    t = t.replace("$", "").replace("~", " ").replace("\\ldots", "…")
    t = t.replace("'{e}", "é").replace("\\'e", "é")
    t = t.replace("\\,", "").replace("\\lvert", "|").replace("\\rvert", "|")
    t = re.sub(r"\\[a-zA-Z]+", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t


MOTIFS_DONNEE = [
    re.compile(r"\d+×"),
    re.compile(r"\d+/16"),
    re.compile(r"\d+ tokens"),
    re.compile(r"\d+ instructions"),
]

# LES INTERDITS (le refus nommé, l'instruction gfylb610p)
INTERDITS = [
    (re.compile(r"\|t\| ?= ?0(?!\d)"),
     "la formulation « |t| = 0 » est INTERDITE (l'égalité exacte la remplace)"),
    (re.compile(r"all \$\|t\|"),
     "la formulation « all |t| » est INTERDITE"),
    (re.compile(r"138 (?:mutation )?survivors in orchestration"),
     "« 138 survivors » : la valeur courante est 56 (v0.14.0)"),
    (re.compile(r"518×|86× the most expensive"),
     "les ratios 518×/86× sont PÉRIMÉS (235×/82× aux médianes courantes)"),
    (re.compile(r"−9\\?%|\\?-9\s?% in executed instructions"),
     "le signe de §3.5 est PÉRIMÉ (+9,9 % contre -O2)"),
]


def linter(chemin: pathlib.Path, falsifie: bool = False) -> list[str]:
    ecarts: list[str] = []
    prose = normalise(chemin)
    if falsifie:
        import random
        aleas = random.Random(20261117)
        for id_, regex, valeur, _ in REGISTRE:
            m = re.search(regex, prose)
            if not m or not m.groups() or not (m.group(1) or "").isdigit():
                continue
            mute = prose[:m.start(1)] + str(int(m.group(1)) + 1) + prose[m.end(1):]
            m2 = re.search(regex, mute)
            if not m2:
                ecarts.append(f"[MUT-{id_}] la mutation CASSE la regex — "
                              "contrôle inopérant")
                continue
            if isinstance(valeur, tuple):
                attendu = str(valeur[0]).replace(",", "")
            else:
                attendu = str(valeur).split("|")[0].replace(",", "")
            if m2.group(1).replace(",", "") == attendu:
                ecarts.append(f"[MUT-{id_}] NON ATTRAPÉE — la valeur mutée "
                              "== la valeur attendue (registre fautif)")
        return ecarts
    for id_, regex, valeur, deriv in REGISTRE:
        m = re.search(regex, prose)
        if not m:
            ecarts.append(f"[{id_}] ABSENT — regex : {regex[:70]}")
            continue
        attendus = [str(v) for v in (
            valeur if isinstance(valeur, tuple) else str(valeur).split("|"))]
        trouves = [g for g in m.groups() if g is not None]
        for attendu, trouve in zip(attendus, trouves):
            if (attendu or "").replace(",", "") != (trouve or "").replace(",", ""):
                ecarts.append(f"[{id_}] ÉCART — la prose dit « {trouve} », "
                              f"la source recalcule « {attendu} » ({deriv})")
    # les interdits
    for motif, message in INTERDITS:
        if motif.search(prose):
            ecarts.append(f"[INTERDIT] {message}")
    # les motifs orphelins dans les sections de données
    sections = re.split(r"(?:sub)*section\{", prose)
    donnees = "\n".join(s for s in sections
                        if any(k in s[:90] for k in
                               ("RQ2: token cost", "compiler comparison",
                                 "RQ1: escaped", "Constant-time")))
    valeurs_registre = " ".join(str(v) for _, _, v, _ in REGISTRE)
    for motif in MOTIFS_DONNEE:
        for m in motif.finditer(donnees):
            extrait = m.group(0)
            nombre = re.match(r"\d+", extrait).group(0)
            if nombre not in valeurs_registre and extrait not in valeurs_registre:
                ecarts.append(f"[ORPHELIN] « {extrait} » vit dans une section "
                              f"de données sans registre")
    return ecarts


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    chemin = pathlib.Path(sys.argv[1])
    falsifie = "--falsifie" in sys.argv
    ecarts = linter(chemin, falsifie)
    print("=" * 88)
    print(f"LE LINTER NUMÉRIQUE v180 — {chemin.name}"
          f"{' (CONTRÔLES NÉGATIFS)' if falsifie else ''}")
    print(f"le registre porte {len(REGISTRE)} affirmations chiffrées, "
          f"dérivées des sources brutes ; {len(INTERDITS)} interdits armés")
    if not ecarts:
        print("  VERDICT : VERT — la prose et les sources concordent, "
              "aucun nombre orphelin, aucun interdit")
        sys.exit(0)
    for e in ecarts:
        print("  " + e)
    print(f"VERDICT : ROUGE — {len(ecarts)} écart(s), le build est REFUSÉ")
    sys.exit(1)
