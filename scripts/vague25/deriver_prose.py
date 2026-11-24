"""La vague 25 (D275) : la prose de statut se DÉRIVE des registres.
Data availability ← DEPOTS.jsonl · Tamarin/ProVerif ← PREUVES-STATUTS.json ·
titre de l'annexe B ← le contenu réel de la table. Chaque passe est VÉRIFIÉE
par relecture du fichier écrit (leçon de la vague 24 : un correctif non
vérifié n'est pas un correctif)."""
import json, pathlib, py_compile, re, sys

R = pathlib.Path(__file__).resolve().parents[2]
depots = [json.loads(l) for l in (R / "DEPOTS.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
preuves = json.loads((R / "PREUVES-STATUTS.json").read_text(encoding="utf-8"))
publies = [d for d in depots if d["statut"] == "publie"]
dernier = publies[0]
DOIS = ", ".join(d["doi_version"] for d in publies)
VERS = ", ".join(d["version"] for d in publies)

# ---------- 1. manuscrit : Data availability ----------
main = R / "edition-v0230/main.tex"
s = main.read_text(encoding="utf-8")
i = s.index("\\paragraph{Data availability.}")
j = s.index("\n\\paragraph{", i + 10)
neuf = (
 "\\paragraph{Data availability.} All primary data is public in the project\n"
 "repository (append-only journal, decision log, evidence vault indexes,\n"
 "extraction script, generated tables) and in the versioned archival\n"
 f"snapshots at the concept DOI \\doiConcept{{}} --- the latest MINTED version is\n"
 f"{dernier['version']} ({dernier['date']}, version DOI {dernier['doi_version']}).\n"
 "The deposits are recorded one line each in the deposit registry\n"
 "(\\code{DEPOTS.jsonl}) and this paragraph is derived from it: the dated\n"
 f"version DOIs are {DOIS}\n"
 f"for {VERS} respectively. This edition (v0.29.0) is \\emph{{not}}\n"
 "minted: the developer's deposit gesture is an explicit command, and until\n"
 "it is given the current snapshot has no version DOI of its own, which is\n"
 "why none is cited here. The two"
)
s = s[:i] + neuf + s[j:]

# ---------- 2. manuscrit : § 2.1 ----------
vieux = ("described in the protocol specification v0.15.8 (the D81 purge edition: the five-share "
         "threshold-three Shamir escrow is the active guard, the delivery instructions retired "
         "from the operational text), which this edition\naccompanies;")
SPECV = re.search(r"v0\.15\.\d+", (R / "scripts/spec_v158/main.tex").read_text(encoding="utf-8")).group(0)
remp = (f"described in the protocol specification (the edition accompanied here is {SPECV}, which this edition accompanies; "
        "v0.15.8 remains a \\emph{dated} reference, its D81 purge edition, whose five-share "
        "threshold-three Shamir escrow is the active guard and whose delivery instructions are "
        "retired from the operational text);")
s = s.replace(vieux, remp)
if "which this edition\naccompanies; we summarise" in s:
    s = s.replace("which this edition\naccompanies; we summarise", "we summarise")

# ---------- 3. manuscrit : statut Tamarin/ProVerif ----------
t = preuves["tamarin"]; pv = preuves["proverif"]
vieux_t = ("The limits are named: the checker is an explicit-state explorer\n"
           "(Tamarin/ProVerif absent from the laboratory --- the deviation is\n"
           "consigned);")
remp_t = (f"The limits are named: the checker is an explicit-state explorer, and the symbolic\n"
          f"side is a partial verdict --- {t['outil']}, model {t['modele']}: {t['verdicts']['L3']},\n"
          f"{t['verdicts']['L1'].split(' (')[0]} and L2 incomplete at the memory wall (the named\n"
          f"cause: proof-goal decomposition); the ProVerif port is delivered, {pv['statut'].lower()};")
s = s.replace(vieux_t, remp_t)
main.write_text(s, encoding="utf-8")

# ---------- vérification du manuscrit (grep de contrôle) ----------
controle = main.read_text(encoding="utf-8")
assert "which this edition\naccompanies" not in controle, "§2.1 non corrigé"
assert "Tamarin/ProVerif absent" not in controle, "statut Tamarin non corrigé"
assert "v0.29.0 at this writing" not in controle, "Data availability non corrigée"
assert "v0.15.8 (the D81 purge edition" not in controle, "référence §2.1 résiduelle"
print("[1-3] manuscrit : Data availability, §2.1, statut Tamarin — VÉRIFIÉS par relecture")

# ---------- 4. preuves : ordre canonique du ratio et statut de preuve ----------
gen = R / "scripts/vague24/generer_pieces_v290.py"
g = gen.read_text(encoding="utf-8")
g = g.replace("(19,66 / 63,39)", "(63,39 / 19,66)")
vieux_pres = '"Tamarin/ProVerif/Maude : outils absents, aucun verdict fabriqué."'
if vieux_pres in g:
    g = g.replace("import re\n", "import re\nimport json\n", 1)
    g = g.replace("R = pathlib.Path(__file__).resolve().parents[2]",
                  "R = pathlib.Path(__file__).resolve().parents[2]\n"
                  "PREUVES = json.loads((R / \"PREUVES-STATUTS.json\").read_text(encoding=\"utf-8\"))\n"
                  "STATUT_TAM = (\"Tamarin \" + PREUVES[\"tamarin\"][\"outil\"].split(\"(\")[0].strip()\n"
                  "              + \" : L3 vérifié (1 122 pas), L1/L2 incomplets au mur 4 Gio ; \"\n"
                  "              + \"ProVerif : port livré, run non exécuté.\")", 1)
    g = g.replace(vieux_pres, "STATUT_TAM")
gen.write_text(g, encoding="utf-8")
verif = gen.read_text(encoding="utf-8")
assert "(19,66 / 63,39)" not in verif, "ratio non corrigé"
assert "outils absents" not in verif, "présentation §9 non corrigée"
py_compile.compile(str(gen), doraise=True)   # leçon : un fichier qui ne s'importe plus n'est pas corrigé
print("[4] preuves/présentation : ordre canonique et statut de preuve — VÉRIFIÉS")

# ---------- 5. annexe B : le titre dérive de la table ----------
sec_d = R / "scripts/spec_v158/sec-d.tex"
d = sec_d.read_text(encoding="utf-8")
k = d.index("\\section{Tableau décisionnel du coffre-fort")
corps = d[k:]
ids = [int(x) for x in re.findall(r"\bD(\d{2,3})\b", corps)]
dmax = max(ids)
d = re.sub(r"\\section\{Tableau décisionnel du coffre-fort \(D75--D\d+\)\}",
           f"\\\\section{{Tableau décisionnel du coffre-fort (D75--D{dmax})}}", d, count=1)
sec_d.write_text(d, encoding="utf-8")
assert f"(D75--D{dmax})" in sec_d.read_text(encoding="utf-8")
print(f"[5] annexe B : titre dérivé = D75--D{dmax} (max réel de la table) — VÉRIFIÉ")
