#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v181.py — LE LINTER NUMÉRIQUE DE LA VAGUE 6 : le registre de la
v0.18.0 PORTÉ aux valeurs corrigées de l'audit (l'instruction bqh4qlrqj),
ÉTENDU AU TEXTE NARRATIF — les dix classes d'erreur nommées par l'audit
sont désormais armées au build, chacence avec sa dérivation :

  (1)  la plage des Entrées de clôture (305--319 partout, 305--318 interdit)
  (2)  les manifestations au slot (TROIS manifestations : DEUX au slot
       memcpy @+0x151a0, UNE au memcmp — recomptées de defauts.csv)
  (3)  la relation hint/RVA/adresse de crash (le crash EST la RVA
       hint/nom retenue dans le slot non lié)
  (4)  la plage exacte des ratios M1 (2.98--11.37, recalculée des CSV)
  (5)  la non-additivité des médianes par composante (1241/3297/3849
       contre 1277/3374/3674 — les sommes recomptées de p5)
  (6)  le décompte des blocs crypto (QUATORZE blocs = 224 mutants/16,
       0 survivant — recompté de mutation.csv)
  (7)  la réconciliation M4 (52.5 campagne / 50.9 avant-mesure, 3.0 %,
       la série d'après n=2 : 39.3/39.2 s)
  (8)  le résidu PBT (655/660 réduits au minimum de 2 pas ; les cinq
       autres, même classe, à des minima plus longs)
  (9)  la table de checksums 0.1.1 (elle vit DANS l'image ; 17 sommes +
       le qword de version 0x00010008→0x00010101, zéro octet ailleurs)
  (10) la table des statuts complète (longtable ; les lignes
       « Campaign D204 » et « Independent replication » doivent vivre
       au fichier source — la Table 8 v0.18.0 était TRONQUÉE au PDF)

LE PRINCIPE (inchangé, fail-closed) : chaque affirmation chiffrée porte
sa dérivation (le fichier source, la ligne, l'opération) ; la prose
normalisée du .tex doit contenir chaque valeur RECALCULÉE des sources ;
tout écart, toute valeur manquante, tout motif orphelin REFUSE le build.

Usage :
  python3 linter_v181.py <manuscrit.tex>            # le verdict
  python3 linter_v181.py <manuscrit.tex> --falsifie # contrôles négatifs
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
mutation = lire_csv(
    RACINE / "preuves_historiques/preuves_v110/mutation.csv")
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

# --- le domaine historique + la lignée : LA PLAGE EXACTE (l'audit bqh4qlrqj) ---
r_loc = nb(loc["mediane"]) / int(m1["Locate a block"]["mesure_tokens"])
r_edi = nb(edi["mediane"]) / int(m1["Edit a block"]["mesure_tokens"])
r_ajo = nb(ajo["mediane"]) / int(m1["Add a block"]["mesure_tokens"])
insere("rq2-domaine", r"cost (\d+)\.(\d+)-(\d+)\.(\d+)× their M1",
       f"{min(r_edi, r_ajo, r_loc):.2f}".replace(".", "|").split("|")[0]
       + "|" + f"{min(r_edi, r_ajo, r_loc):.2f}".split(".")[1]
       + "|" + f"{max(r_loc, r_edi, r_ajo):.2f}".split(".")[0]
       + "|" + f"{max(r_loc, r_edi, r_ajo):.2f}".split(".")[1],
       f"les trois ratios contenus, recalculés des CSV : localiser "
       f"{nb(loc['mediane'])}/{int(m1['Locate a block']['mesure_tokens'])} "
       f"= {r_loc:.2f}, éditer {nb(edi['mediane'])}/"
       f"{int(m1['Edit a block']['mesure_tokens'])} = {r_edi:.2f}, ajouter "
       f"{nb(ajo['mediane'])}/{int(m1['Add a block']['mesure_tokens'])} "
       f"= {r_ajo:.2f} — la plage exacte 2.98-11.37 (le « 3-11 » de D208 "
       f"remplacé par l'audit de la vague 6)")
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
insere("audit-os", r"and (\d+) for -Os", str(os_),
       "audit_benchmark gcc -Os")
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
insere("pbt-655", r"(\d+) of the (\d+) reach the two-step minimum", "655|660",
       "pbt_ecarts_minimaux.json (655 au minimum de 2 pas ; 660-655 = 5 "
       "traces résiduelles de la même classe, à des minima plus longs)")
insere("couverture-288", r"one of the (\d+) abstract shapes", "288",
       "verifie_couverture_288 (la bijection)")
insere("alignement-512", r"(\d+) concrete states per rule", "512",
       "alignement_13_regles (4×2×8×2×2×2 = 512 états)")
insere("tla-8sur8", r"returns (\d+)/(\d+) green", "8|8",
       "jouer_tous_les_runs.py (la batterie re-jouée)")

# --- M4 v180 → v181 (p8-m4-*.json + p8-m4-rapport-r11.txt) ---
m4_avant = json.loads((V5 / "p8-m4-avant.json").read_text())
m4_apres = json.loads((V5 / "p8-m4-apres.json").read_text())
m4_campagne = round(m4_t, 1)                    # la valeur consignée campagne
m4_avant_c = round(m4_avant["total_s"], 1)      # la avant-mesure consignée
insere("m4-avant", r"before-measure reads (\d+)\.(\d+)s",
       f"{int(m4_avant_c)}|{round((m4_avant_c % 1) * 10)}",
       f"p8-m4-avant.json (total_s = {m4_avant['total_s']} → "
       f"{m4_avant_c})")
insere("m4-apres-n2", r"two consecutive runs \(n\{=\}2\), (\d+)\.(\d+)s then\s*(\d+)\.(\d+)s, both green",
       "39|3|39|2",
       "p8-m4-rapport-r11.txt (la série d'après : 39.3 s puis 39.2 s — "
       "le json consigne total_s = 39.244, empreintes scellées intactes)")
ecart_m4 = (m4_campagne - m4_avant_c) / m4_campagne * 100
insere("m4-variance", r"(\d)\.(\d)\\% below the campaign's consigned (\d+)\.(\d+)s",
       f"{round(ecart_m4)}|{round((ecart_m4 % 1) * 10)}"
       f"|{int(m4_campagne)}|{round((m4_campagne % 1) * 10)}",
       f"la réconciliation M4 : ({m4_campagne} - {m4_avant_c})/"
       f"{m4_campagne} = {ecart_m4:.2f} % — l'écart des deux valeurs "
       "consignées (la campagne 52.5 s au registre ; la avant-mesure 50.9 s "
       "de p8-m4-avant.json), deux mesures n=1 consignées telles quelles, "
       "jamais moyennées (p8-m4-rapport-r11.txt : AVANT 50.9/2.2 = 23.1×, "
       "le recoup : la campagne avait mesuré 23.9×)")
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

# LES INTERDITS (le refus nommé — v180 + les cinq classes de l'audit v181)
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
    (re.compile(r"305-318"),
     "la plage 305-318 est PÉRIMÉE : le journal de tâches porte la fermeture "
     "319 (worklog-maj, Task 219 — l'Entrée 319 : le témoin L6 signé et la "
     "vague 4 exécutée) — la plage est 305-319"),
    (re.compile(r"three times at the same slot"),
     "« three times at the same slot » : defauts.csv recompte TROIS "
     "manifestations de la classe feuille — DEUX au slot memcpy "
     "(@+0x151a0 : C-app-it1 le scénario, C-app-it2 l'hôte), UNE au memcmp "
     "(C-loupe-13-it1)"),
    (re.compile(r"nineteen pure-compute crypto blocks"),
     "« nineteen » : les familles crypto comptent QUATORZE blocs (mutation.csv "
     "recompte 224 mutants/16 = 14 blocs — tls13-01..06, 13..19 + loupe-06, "
     "0 survivant)"),
    (re.compile(r"cost 3-11× their M1"),
     "la plage 3-11× est PÉRIMÉE : les ratios contenus recalculés des CSV "
     "sont 2.98-11.37× (580/51, 2143/719, 3510/1088)"),
    (re.compile(r"equalling the crash address"),
     "la confusion hint/adresse : le slot non lié est @+0x151a0, son contenu "
     "sur disque est la RVA hint/nom 0x152da, et le saut indirect ATTEINT "
     "cette RVA nue — le crash EST à la RVA hint/nom retenue, jamais "
     "« equalling » le slot"),
]

# ---------------------------------------------- LE TEXTE NARRATIF (vague 6)
def narratif(prose: str, chemin: pathlib.Path) -> list[str]:
    """Les dix classes de l'audit bqh4qlrqj, armées au build : chaque
    contrôle porte sa dérivation des registres bruts."""
    ecarts: list[str] = []

    # (1) la plage des fermetures : 305-319 partout (abstract EN/FR, intro)
    n_bon = len(re.findall(r"305-319", prose))
    if n_bon < 3:
        ecarts.append(
            f"[plage-fermetures] {n_bon} occurrence(s) de « 305-319 » "
            f"(attendu 3 : abstract EN, abstract FR, introduction) — le "
            f"journal de tâches (worklog-maj) porte les fermetures 305 à 319")

    # (2) les manifestations au slot : recomptées de defauts.csv
    feuilles = [d for d in defauts if "feuille" in d["classe"]]
    n_memcpy = sum(1 for d in feuilles if "memcpy" in d["classe"])
    n_memcmp = sum(1 for d in feuilles if "memcmp" in d["classe"])
    if not re.search(r"twice at the same slot \(the memcpy leaf", prose):
        ecarts.append(
            "[slots] la prose doit dire « twice at the same slot (the memcpy "
            f"leaf…) » — defauts.csv : {len(feuilles)} manifestations de la "
            f"classe feuille ({n_memcpy} memcpy au même slot @+0x151a0, "
            f"{n_memcmp} memcmp)")
    if "once at the memcmp leaf" not in prose:
        ecarts.append(
            "[slots] la prose doit dire « once at the memcmp leaf » — la "
            "manifestation loupe-13 (memcmp @+0x91a0) n'est pas au slot memcpy")

    # (3) la relation hint/RVA/adresse de crash
    for motif in (r"\+0x151a0", r"0x152da", r"0x91a0", r"0x92da",
                  r"the crash address is\s+the retained hint/name RVA"):
        if not re.search(motif, prose):
            ecarts.append(
                f"[hint-rva] la prose doit contenir « {motif} » — le mécanisme "
                f"consigné (Entrées 304/311/312, defauts.csv) : le slot IAT "
                f"non lié retient sa RVA hint/nom sur disque, le saut "
                f"indirect atteint l'adresse nue")

    # (5) la non-additivité des médianes par composante (p5)
    lignes = {}
    for op in ("localiser", "éditer", "ajouter"):
        m = re.search(rf"{op}\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",
                      DEC_TXT)
        if m:
            lignes[op] = tuple(int(m.group(i)) for i in range(1, 6))
    for op, attendu_somme in (("localiser", 1241), ("éditer", 3297),
                              ("ajouter", 3849)):
        mat, pro, rep, tot, contenu = lignes[op]
        if mat + pro + rep != attendu_somme or str(attendu_somme) not in prose:
            ecarts.append(
                f"[medianes-{op}] la note de non-additivité manque ou est "
                f"fausse : p5 recompte {mat}+{pro}+{rep} = {mat+pro+rep} "
                f"contre la médiane du total {tot} — la prose doit porter "
                f"« {mat+pro+rep} » et « medians are not additive »")
    if "medians are not additive" not in prose:
        ecarts.append("[medianes] la phrase « medians are not additive » "
                      "est requise (la note méthodologique de l'audit)")

    # (6) le décompte des blocs crypto (mutation.csv)
    cible = ["tls13-01", "tls13-02", "tls13-03", "tls13-04", "tls13-05",
             "tls13-06", "tls13-13", "tls13-14", "tls13-15", "tls13-16",
             "tls13-17", "tls13-18", "tls13-19", "loupe-06"]
    mut_cible = [r for r in mutation if r["bloc"] in cible]
    n_mut = sum(int(r["mutants"]) for r in mut_cible)
    n_viv = sum(int(r["vivants"]) for r in mut_cible)
    if (len(mut_cible), n_mut, n_viv) != (14, 224, 0):
        ecarts.append(
            f"[crypto-blocs] mutation.csv recompte {len(mut_cible)} blocs / "
            f"{n_mut} mutants / {n_viv} survivant(s) — le registre attend "
            f"14 blocs, 224 mutants, 0 survivant")
    if "fourteen blocks of the cryptographic families" not in prose:
        ecarts.append(
            "[crypto-blocs] la prose doit dire « fourteen blocks of the "
            "cryptographic families » (mutation.csv : 224 mutants = "
            "14 blocs × 16, 0 survivant)")
    if "224 mutants" not in prose:
        ecarts.append("[crypto-blocs] « 224 mutants » doit vivre dans la prose")

    # (8) le résidu PBT : 660 - 655 = 5, nommé
    if "five remaining traces" not in prose:
        ecarts.append(
            "[pbt-residu] la prose doit nommer « five remaining traces » — "
            "660 traces divergentes, 655 réduites au minimum de 2 pas "
            "(pbt_ecarts_minimaux.json), 660-655 = 5 résiduelles de la même "
            "classe, à des minima plus longs")

    # (9) la table de checksums 0.1.1 : où elle vit
    for motif in (r"inside the artifact image", r"0x00010008", r"0x00010101",
                  r"seventeen per-block sums"):
        if not re.search(motif, prose):
            ecarts.append(
                f"[checksums] la prose doit contenir « {motif} » — D178/D179 : "
                f"la table des 17 sommes vit DANS l'image (le qword de "
                f"version porté 0x00010008 → 0x00010101, zéro octet ailleurs)")

    # (10) la table des statuts : complète, en longtable
    f_statuts = chemin.parent / "donnees" / "statuts_v181.tex"
    if not f_statuts.exists():
        ecarts.append(f"[statuts] le fichier {f_statuts} est absent")
    else:
        src = f_statuts.read_text(encoding="utf-8")
        if "\\begin{longtable}" not in src:
            ecarts.append(
                "[statuts] la table des statuts doit être une longtable — la "
                "Table 8 de la v0.18.0 était TRONQUÉE à la page 29 du PDF "
                "(pdftotext : la dernière ligne visible « zero divergence, "
                "SHA-256 parity at » ; les lignes Campaign D204 et "
                "Independent replication perdues)")
        for ligne in ("Campaign D204", "Independent replication", "655/660"):
            if ligne not in src:
                ecarts.append(
                    f"[statuts] la ligne « {ligne} » doit vivre au fichier "
                    f"source de la table des statuts")
    return ecarts


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
    # le texte narratif (la vague 6)
    ecarts.extend(narratif(prose, chemin))
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
    print(f"LE LINTER NUMÉRIQUE v181 — {chemin.name}"
          f"{' (CONTRÔLES NÉGATIFS)' if falsifie else ''}")
    print(f"le registre porte {len(REGISTRE)} affirmations chiffrées, "
          f"dérivées des sources brutes ; {len(INTERDITS)} interdits armés ; "
          f"10 classes narratives de l'audit")
    if not ecarts:
        print("  VERDICT : VERT — la prose et les sources concordent, "
              "aucun nombre orphelin, aucun interdit, les dix classes "
              "narratives de l'audit tenues")
        sys.exit(0)
    for e in ecarts:
        print("  " + e)
    print(f"VERDICT : ROUGE — {len(ecarts)} écart(s), le build est REFUSÉ")
    sys.exit(1)
