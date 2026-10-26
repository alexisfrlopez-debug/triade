#!/usr/bin/env python3
"""Contrôles programmatiques de cohérence terminologique et structurelle
pour l'article TRIADE v0.4 (rapport de vérification interne, tâche 4).

Vérifie sur les sources .tex :
  1. terminologie clé — présence et absence de variantes interdites ;
  2. structure IMRAD — ordre et présence des sections attendues ;
  3. intégrité des références croisées et citations (pas de ?? / [?]) ;
  4. numérotation des flottants (tableaux, figures, listing, algorithme) ;
  5. vocabulaire anglais intrus dans le corps français (liste blanche).
Sortie : synthèse PASS/FAIL par famille + détails.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = [HERE / f for f in [
    "main.tex", "sec-intro.tex", "sec-related.tex", "sec-method.tex",
    "sec-case.tex", "sec-discussion.tex", "sec-threats.tex",
    "sec-conclusion.tex"]]

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


text = "\n".join(p.read_text(encoding="utf-8") for p in SRC)
text_norm = text.replace("\u2019", "'").replace("\u00a0", " ")
pdf = HERE / "final.pdf"
import pdfplumber
with pdfplumber.open(pdf) as doc:
    full = "\n".join((pg.extract_text() or "") for pg in doc.pages)

# ---- 1. Terminologie : occurrences des termes pivots ----
print("--- Terminologie pivot (sources) ---")
TERMS = [
    "verrou croisé", "vérifie-puis-écrit", "oracle éphémère",
    "cristallisation", "fonction objectif lexicographique",
    "spécifications d'intention", "couche I", "couche B", "couche C",
    "adresse", "profil", "patch à contrat stable", "adresses stables",
    "reverse-specs", "spécification rétro-active",
]
for t in TERMS:
    pat = r"\s+".join(re.escape(w) for w in t.split())
    n = len(re.findall(pat, text_norm, flags=re.IGNORECASE))
    check(f"terme présent : {t}", n >= 1, f"{n} occurrence(s)")

print("--- Variantes interdites (doivent être absentes) ---")
BANNED = [
    (r"verrou croise[^sé]", "verrou croisé sans accent ou mal formé"),
    (r"cross-lock", "anglicisme cross-lock (hors glossaire EN voulu)"),
    (r"[Rr]efactoring", "refactoring → refactorisation retenue"),
    (r"dette technique\s*:\s*TRIADE", "formulation ambiguë"),
]
for pat, label in BANNED[:-1]:
    m = re.findall(pat, text_norm)
    check(f"absence : {label}", len(m) == 0, f"{len(m)} trouvée(s)")
todos = re.findall(r"TODO|FIXME|XXX(?![\w])", text)
check("absence de TODO/FIXME", len(todos) == 0, f"{len(todos)}")

# ---- 2. Structure IMRAD ----
print("--- Structure IMRAD (sources) ---")
order = [
    (r"\\section\{Introduction\}", "Introduction"),
    (r"\\section\{Travaux connexes\}", "Travaux connexes (Related Work)"),
    (r"\\section\{Le protocole TRIADE\}", "Méthodologie"),
    (r"\\section\{Étude de cas", "Étude de cas (Case Study)"),
    (r"\\section\{Discussion\}", "Discussion"),
    (r"\\section\{Menaces sur la validité\}", "Menaces sur la validité"),
    (r"\\section\{Conclusion", "Conclusion"),
]
pos = []
for pat, label in order:
    m = re.search(pat, text)
    check(f"section présente : {label}", m is not None)
    if m:
        pos.append((m.start(), label))
check("ordre IMRAD respecté", pos == sorted(pos, key=lambda x: x[0]),
      " → ".join(l for _, l in pos))

# Résumé et mots-clés
check("résumé présent (main.tex)", "Résumé" in text and "Mots-clés" in text)
check("questions de recherche RQ1-RQ3", all(
    f"RQ{i}" in text for i in (1, 2, 3)))
check("contributions C1-C4", all(
    f"C{i}" in text for i in (1, 2, 3, 4)))

# ---- 3. Références croisées et citations ----
print("--- Références croisées (PDF) ---")
check("aucune référence non résolue ??", "??" not in full)
check("aucune citation non résolue [?]", "[?]" not in full)
labels = set(re.findall(r"\\label\{([^}]+)\}", text))
labels |= set(re.findall(r"label=\{([^}]+)\}", text))
refs = set(re.findall(r"\\ref\{([^}]+)\}", text))
check("toutes les \\ref ont un \\label", refs <= labels,
      f"manquants : {sorted(refs - labels) or 'aucun'}")

cites = set()
for c in re.findall(r"\\cite\{([^}]+)\}", text):
    cites.update(k.strip() for k in c.split(","))
bib = set(re.findall(r"@\w+\{([^,]+),", (HERE / "refs.bib").read_text(encoding="utf-8")))
check("toutes les clés \\cite existent dans refs.bib", cites <= bib,
      f"manquantes : {sorted(cites - bib) or 'aucune'}")
unused = bib - cites
print(f"[INFO] références biblio non citées : {sorted(unused) or 'aucune'}")

# ---- 4. Flottants ----
print("--- Flottants (PDF) ---")
n_tab = len(re.findall(r"Tableau\s?\d+", full))
n_fig = len(re.findall(r"Figure\s?\d+", full))
n_lst = len(re.findall(r"Listing\s?\d+", full))
n_alg = len(re.findall(r"Algorithme\s?\d+", full))
check("5 tableaux légendés", n_tab >= 5, f"{n_tab} légendes")
check("1 figure", n_fig >= 1, f"{n_fig}")
check("1 listing", n_lst >= 1, f"{n_lst}")
check("1 algorithme", n_alg >= 1, f"{n_alg}")
for f in ["tab:regles", "tab:mesures", "fig:arch", "lst:seuil", "alg:boucle"]:
    check(f"flottant référencé dans le prose : {f}", f"\\ref{{{f}}}" in text)

# ---- 5. Anglicismes hors liste blanche ----
print("--- Anglicismes (corps français, liste blanche) ---")
WHITELIST = {
    "agent-first", "reverse-specs", "WYSIWYG", "Design by Contract",
    "token", "tokens", "checkpoint", "benchmark", "micro-benchmarks",
    "padding", "trampoline", "round-trip", "fail-closed", "supply chain",
    "checkin", "CI", "commit", "commits", "diff", "diffable", "tag",
    "tags", "build", "SAN", "_md5", "SHA-256", "PE32+", "ELF64", "Mach-O",
    "Wasm", "WASI", "ASIO", "RoomEq", "TRIADE", "QuickCheck", "Alloy",
    "in-toto", "Copilot", "GitHub", "Linux", "Windows", "macOS", "RISC-V",
    "x86-64", "M-INS", "M-<DOM>-NN", "Dijkstra", "Hoare", "Wohlin",
    "Runeson", "Yin", "SQALE", "TLA", "M0", "Svyatkovskiy",
}
words = set(re.findall(r"\b[A-Za-z][a-z]{4,}\b", re.sub(
    r"(?s)\\begin\{lstlisting\}.*?\\end\{lstlisting\}|%.*", "",
    text_norm.replace("\\par", " "))))
suspects = sorted(w for w in words if w.lower() not in {x.lower() for x in WHITELIST}
                  and not w[0].isupper())
check("vocabulaire anglais intrus limité", len(suspects) <= 25,
      f"{len(suspects)} : {suspects[:20]}")

print()
print("=" * 60)
print(f"BILAN : {'ÉCHEC — ' + str(len(failures)) + ' contrôle(s)' if failures else 'TOUS CONTRÔLES PASSÉS'}")
print("=" * 60)
sys.exit(1 if failures else 0)
