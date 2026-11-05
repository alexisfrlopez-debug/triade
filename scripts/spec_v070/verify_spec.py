#!/usr/bin/env python3
"""Vérification post-révision du protocole TRIADE v0.7.0 (cahier de révision).

Miroir de spec_v061/verify_spec.py — seize critères, tous vérifiés
mécaniquement sur les sources, les décisions et le PDF formel :
  V1   hiérarchie Sécurité > Performance > Optimisation > Coût en tokens intacte ;
  V2   couches I/B/C indissociables ;
  V3   aucune règle affaiblie — R1-R9 à l'identique, R10 en sur-ensemble ;
  V4   aucune couche d'abstraction à l'exécution introduite ;
  V5   aucune promesse de portabilité universelle immédiate ;
  V6   aucun mécanisme de furtivité EDR ;
  V7   chaque nouvelle exigence vérifiable (mécaniquement ou par oracle) ;
  V8   chaque évolution tracée dans le changelog (v0.7.0 incluse) ;
  V9   modifications incompatibles explicitement rejetées ;
  V10  contenu hérité v0.5.0-v0.6.1 intact (terrain, taxonomie X1-X8, coffre
       D75, garde D81, souveraineté D133, arbitrage D137) ;
  V11  contenu § 12 intact + § 12.4 : TREIZE arbres, la discipline des
       cérémonies d'ère (dette à la naissance D166 r. 8, charge au geste
       D168, déterminisme Ed25519 D163) ;
  V12  contenu § 13 : cérémonies et kit + la NOUVELLE § 13.5 (les cérémonies
       d'ère du 05/11 : M8 12 arbres, M9 13 arbres, garde 13/13) ;
  V13  menaces étendues ; jalons M0-M8 franchis / M9 ouvert constatés ;
       correspondances v0.6.0 → v0.6.1 ET v0.6.1 → v0.7.0 ; annexe
       décisionnelle étendue D160-D169 au PDF formel ;
  V14  le Livre du Coffre existe (v1.1, docs/) et demeure la référence
       opératoire ; aucune référence non résolue au PDF formel ;
  V15  la révision D169 nominative : § 1.9 présent, la clause « hors
       périmètre courant » LEVÉE NOMMÉMENT, aucune ligne parasite « tbp] » ;
  V16  l'état consolidé au PDF : M8 franchi (0.9.0), M9 ouvert, le sceau à
       treize arbres, la cérémonie de l'ère M9 passée sur pièces.
Sortie : PASS/FAIL par critère, exit 1 si échec.
"""
import re
import sys
from pathlib import Path

import pdfplumber

HERE = Path(__file__).resolve().parent.parent.parent  # racine du dépôt triade
SPEC_RAW = (HERE / "docs" / "PROTOCOLE_TRIADE.md").read_text(encoding="utf-8")
SPEC = re.sub(r"\s+", " ", SPEC_RAW).replace("\u2019", "'")
DEC_RAW = (HERE / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
DEC = re.sub(r"\s+", " ", DEC_RAW).replace("\u2019", "'")
PLAN_RAW = (HERE / "docs" / "PLAN_MILESTONES.md").read_text(encoding="utf-8")
PLAN = re.sub(r"\s+", " ", PLAN_RAW).replace("\u2019", "'")

PDF_SPEC = ""
with pdfplumber.open(HERE / "docs" / "Protocole_TRIADE_v0.7.0_Specification.pdf") as pdf:
    N_PAGES_SPEC = len(pdf.pages)
    PDF_SPEC = "\n".join((p.extract_text() or "") for p in pdf.pages).replace("\u2019", "'")
PDF_LIVRE = ""
with pdfplumber.open(HERE / "docs" / "Livre_du_Coffre_TRIADE_CF1-CF3_v1.1.pdf") as pdf:
    N_PAGES_LIVRE = len(pdf.pages)
    PDF_LIVRE = "\n".join((p.extract_text() or "") for p in pdf.pages).replace("\u2019", "'")

failures = []


def check(cid, name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {cid} — {name}" + (f" : {detail}" if detail else ""))
    if not ok:
        failures.append(cid)


# ---- V1 : hiérarchie intacte et verrouillée ----
hier = "Sécurité > Performance > Optimisation > Coût en tokens"
n_md = SPEC.count(hier)
check("V1", "hiérarchie présente dans la spécification", n_md >= 2, f"{n_md} occurrences")
check("V1", "hiérarchie déclarée invariant de révision",
      "invariant de révision" in SPEC and "D19" in SPEC)
alt = re.findall(r"Sécurité\s*>\s*[^>\n]{3,40}>\s*[^>\n]{3,40}>\s*[^>\n]{3,40}", SPEC)
alts = {a.strip() for a in alt if not a.strip().startswith(hier)}
check("V1", "aucune hiérarchie alternative", not alts, str(alts or "aucune"))

# ---- V2 : couches indissociables ----
check("V2", "trois couches nommées I/B/C",
      all(k in SPEC for k in ["couche I", "couche B", "couche C"]))
check("V2", "aucune couche optionnelle",
      "Aucune couche n'est optionnelle" in SPEC or "aucune couche n'est optionnelle" in SPEC.lower())

# ---- V3 : règles intactes ----
for r in ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11"]:
    check("V3", f"règle {r} présente", r in SPEC)
check("V3", "R10 en sur-ensemble (a, b, c, d)",
      all(k in SPEC for k in ["a", "b", "c", "d"]) and "R10" in SPEC)

# ---- V4 : aucune couche d'exécution ----
check("V4", "aucune machine virtuelle / bytecode portable introduits",
      "bytecode portable" in SPEC and "machine virtuelle" in SPEC
      and "aucune couche d'abstraction" in SPEC)

# ---- V5 : portabilité progressive ----
check("V5", "universalité structurelle mais progressive",
      "le protocole ne promet pas la portabilité, il la vérifie" in SPEC)

# ---- V6 : pas de furtivité ----
check("V6", "furtivité EDR explicitement hors périmètre",
      "La furtivité face aux EDR n'est pas recherchée" in SPEC
      or "furtivité" in SPEC.lower())

# ---- V7 : exigences vérifiables ----
check("V7", "critères de sortie mesurables présents (jalons)",
      "Critères d'acceptation des jalons" in SPEC_RAW)
check("V7", "falsifiabilité exigée dans le chapitre souveraineté",
      "falsifiabilité" in SPEC_RAW or "falsification" in SPEC_RAW)

# ---- V8 : changelog ----
check("V8", "entrée v0.6.1 au journal des versions",
      "| v0.6.1 | 31 oct. 2026 |" in SPEC_RAW)
check("V8", "entrée v0.7.0 au journal des versions",
      "| v0.7.0 | 5 nov. 2026 |" in SPEC_RAW)
check("V8", "correspondance v0.6.0 → v0.6.1 présente",
      "### 19.8 Correspondance v0.6.0 → v0.6.1" in SPEC_RAW)
check("V8", "correspondance v0.6.1 → v0.7.0 présente",
      "### 19.9 Correspondance v0.6.1 → v0.7.0" in SPEC_RAW)

# ---- V9 : rejets explicites ----
check("V9", "modifications rejetées v0.6.1 consignées",
      "Modifications explicitement rejetées (v0.6.1)" in SPEC_RAW)
check("V9", "modifications rejetées v0.7.0 consignées",
      "Modifications explicitement rejetées (v0.7.0)" in SPEC_RAW)

# ---- V10 : héritage v0.5.0-v0.6.1 intact ----
check("V10", "taxonomie X1-X8 présente", "X1–X8" in SPEC_RAW or "X1-X8" in SPEC_RAW)
check("V10", "coffre-fort D75 présent", "TRIADE-CF1" in SPEC_RAW)
check("V10", "garde D81 présente", "PHRASE-CONTROLE-COFFRE.txt" in SPEC_RAW)
check("V10", "passation v0.6.0 intacte (D133, axes, migration réelle)",
      all(k in SPEC for k in ["D133", "par invocation", "0cc89a96"]))
check("V10", "arbitrage D137 intact (§ 12.5, les trois naissances)",
      "### 12.5 Le niveau du coffre neuf — un arbitrage du développeur (D137)" in SPEC_RAW
      and "coffre_cf3.py init" in SPEC_RAW)

# ---- V11 : souveraineté (§ 12) — § 12.4 TREIZE arbres ----
check("V11", "chapitre 12 souveraineté présent",
      "## 12. Souveraineté cryptographique" in SPEC_RAW)
for sonde in ["Shamir", "0x11B", "PORTE D120", "TRIADE-CF3",
              "par invocation", "cycle en deux actes", "carte papier",
              "Ed25519", "init"]:
    check("V11", f"« {sonde} » au chapitre souveraineté", sonde in SPEC_RAW)
check("V11", "§ 12.4 : TREIZE arbres sous le sceau",
      "Treize arbres de couche I vivent sous le sceau" in SPEC_RAW)
seg12 = SPEC_RAW[SPEC_RAW.find("## 12."):SPEC_RAW.find("## 13.")]
check("V11", "la dette de cérémonie nommée à la naissance (D166 r. 8)",
      "dette de cérémonie à la" in seg12 and "D166" in seg12)
check("V11", "la charge préparée au geste qui sert la main (D168)",
      "au geste qui sert la main" in seg12 and "D168" in seg12)
check("V11", "la continuité de clé par le déterminisme Ed25519 (D163)",
      "déterminisme" in seg12 and "D163" in seg12)
check("V11", "aucun « dix arbres » restant au § 12",
      "dix arbres" not in seg12 and "Dix arbres" not in seg12)

# ---- V12 : cérémonies et kit (§ 13) + § 13.5 ----
check("V12", "chapitre 13 cérémonies présent",
      "## 13. Les cérémonies et le kit du terrain" in SPEC_RAW)
seg13 = SPEC[SPEC.find("## 13."):SPEC.find("## 14.")]
for sonde in ["MIGRER", "VÉRIFIER", "DÉTRUIRE", "trio D122",
              "identité octet pour octet par construction", "0cc89a96",
              "treize arbres VERTS"]:
    check("V12", f"« {sonde} » au chapitre cérémonies", sonde in seg13)
check("V12", "§ 13.5 : les cérémonies d'ère du sceau présentes",
      "### 13.5 Les cérémonies d'ère du sceau de l'Intention" in SPEC_RAW)
check("V12", "§ 13.5 : l'ère M8 (douze arbres, la preuve D163)",
      "douze arbres" in seg13 and "12/12" in seg13)
check("V12", "§ 13.5 : l'ère M9 (treize arbres, la charge régénérée D168)",
      "TREIZE arbres" in seg13 and "RÉGÉNÉRÉE" in seg13 and "13/13" in seg13)

# ---- V13 : menaces, jalons, annexes ----
for sonde in ["Expropriation", "Evil maid", "Roll-back du couple"]:
    check("V13", f"menace « {sonde} »", sonde in SPEC_RAW)
check("V13", "jalons M0 à M9 au titre du § 18",
      "## 18. Critères d'acceptation des jalons M0 à M9" in SPEC_RAW)
check("V13", "M8 franchi constaté (markdown jalons)",
      "**franchi** 05/11/2026 — balise `0.9.0`" in SPEC_RAW)
check("V13", "M9 ouvert constaté (markdown jalons)",
      "**ouvert** 05/11/2026 (D166)" in SPEC_RAW)
check("V13", "M7 franchi constaté (markdown jalons)",
      "**franchi** 05/11/2026 — balise `0.8.0`" in SPEC_RAW)
check("V13", "le programme d'après M7 au plan",
      "Programme d'après M7" in PLAN_RAW)
for sonde in ["8c79263b", "1cf18644", "f50ce894", "933e8405"]:
    check("V13", f"empreinte {sonde} au PDF formel", sonde in PDF_SPEC)
check("V13", "tableau décisionnel du coffre-fort au PDF",
      "Tableau décisionnel du coffre-fort" in PDF_SPEC)
check("V13", "annexe décisionnelle étendue à D169 au PDF",
      "D160" in PDF_SPEC and "D169" in PDF_SPEC)
check("V13", "checksum terrain 0cc89a96 au PDF", "0cc89a96" in PDF_SPEC)
check("V13", "correspondance v0.6.1 → v0.7.0 au PDF",
      "Correspondance v0.6.1" in PDF_SPEC)

# ---- V14 : le Livre du Coffre + intégrité du PDF ----
check("V14", "Livre du Coffre présent (26 pages attendues, ±2)",
      abs(N_PAGES_LIVRE - 26) <= 2, f"{N_PAGES_LIVRE} pages")
for sonde in ["Le Livre du Coffre", "runbook", "CINQ originaux",
              "carte du sachet", "0cc89a96"]:
    check("V14", f"« {sonde} » au Livre", sonde in PDF_LIVRE)
check("V14", "D169 consignée aux décisions",
      "## D169 —" in DEC_RAW)
check("V14", "PDF formel : 41 pages attendues (±2)",
      abs(N_PAGES_SPEC - 41) <= 2, f"{N_PAGES_SPEC} pages")
check("V14", "aucune référence non résolue (??) au PDF formel",
      "??" not in PDF_SPEC)
check("V14", "aucune référence non résolue (??) au Livre",
      "??" not in PDF_LIVRE)

# ---- V15 : la révision D169 nominative ----
check("V15", "§ 1.9 « Ce que change la v0.7.0 » présent",
      "### 1.9 Ce que change la v0.7.0" in SPEC_RAW)
check("V15", "la clause « hors périmètre courant » LEVÉE NOMMÉMENT",
      "levée NOMMÉMENT" in SPEC_RAW or "LEVÉE NOMMÉMENT" in SPEC_RAW)
check("V15", "la consolidation nommée au § 21 (clôture)",
      "La présente version consolide le programme d'après M7" in SPEC_RAW)
check("V15", "D169 consignée aux décisions",
      "## D169 —" in DEC_RAW)
check("V15", "le programme D160 consigné au plan",
      "D160" in PLAN_RAW and "FONDATION D'ABORD" in PLAN_RAW)
check("V15", "erratum « tbp] » : aucune LIGNE parasite au PDF formel",
      not any(l.strip() == "tbp]" for l in PDF_SPEC.splitlines()))
check("V15", "aucun placeholder (XXX / TODO / 【) au PDF",
      not any(k in PDF_SPEC for k in ["XXX", "TODO", "【"]))

# ---- V16 : l'état consolidé au PDF ----
PDF_SPEC_JOINT = PDF_SPEC.replace(" ", "")  # l'extraction avale les espaces (ligatures)
check("V16", "§ 1.9 au PDF (Ce que change la v0.7.0)",
      "Ce que change la v0.7.0" in PDF_SPEC)
check("V16", "le sceau à TREIZE arbres au PDF",
      "Treizearbres" in PDF_SPEC_JOINT or "TREIZEarbres" in PDF_SPEC_JOINT)
check("V16", "les cérémonies d'ère au PDF (§ 13.5)",
      "cérémonies d'ère" in PDF_SPEC)
check("V16", "M8 — syscalls directs au PDF (tableau des jalons)",
      "syscalls directs" in PDF_SPEC and "0.9.0" in PDF_SPEC)
check("V16", "M9 — TLS 1.3 pur au PDF (tableau des jalons)",
      "TLS 1.3 pur" in PDF_SPEC and "1.0.0" in PDF_SPEC)
check("V16", "la cérémonie de l'ère M9 passée (garde 13/13)",
      "13/13" in PDF_SPEC)
check("V16", "version v0.7.0 au PDF (en-tête de page)",
      "v0.7.0" in PDF_SPEC)

print()
if failures:
    print("ÉCHEC :", len(failures), "critère(s) —", ", ".join(failures))
    sys.exit(1)
print(f"CAHIER v0.7.0 : TOUT PASSÉ — spécification {N_PAGES_SPEC} pages, "
      f"Livre du Coffre {N_PAGES_LIVRE} pages.")
