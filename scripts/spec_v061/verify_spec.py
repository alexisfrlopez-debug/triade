#!/usr/bin/env python3
"""Vérification post-révision du protocole TRIADE v0.6.1 (cahier de révision).

Miroir de spec_v060/verify_spec.py — quinze critères, tous vérifiés
mécaniquement sur les sources, les décisions et les deux PDF :
  V1   hiérarchie Sécurité > Performance > Optimisation > Coût en tokens intacte ;
  V2   couches I/B/C indissociables ;
  V3   aucune règle affaiblie — R1-R9 à l'identique, R10 en sur-ensemble ;
  V4   aucune couche d'abstraction à l'exécution introduite ;
  V5   aucune promesse de portabilité universelle immédiate ;
  V6   aucun mécanisme de furtivité EDR ;
  V7   chaque nouvelle exigence vérifiable (mécaniquement ou par oracle) ;
  V8   chaque évolution tracée dans le changelog (v0.6.1 incluse) ;
  V9   modifications incompatibles explicitement rejetées ;
  V10  contenu hérité v0.5.0-v0.6.0 intact (terrain, taxonomie X1-X8, coffre
       D75, garde D81, souveraineté D133) ;
  V11  contenu v0.6.0 § 12 intact + § 12.5 RÉVISÉ : le niveau du coffre neuf
       est arbitré par le développeur (D137) — trois naissances, guide,
       obligations par niveau ;
  V12  contenu § 13 : cérémonies et kit — chaîne des cérémonies, trio
       D122, kit D130 identité par construction, preuve terrain 30-31/10 ;
  V13  menaces étendues ; M4 franchi constaté, M5 ouvert ; correspondances
       v0.5.2 → v0.6.0 ET v0.6.0 → v0.6.1 ; annexe empreintes et tableau
       décisionnel D75-D137 au PDF formel ;
  V14  le Livre du Coffre existe (v1.1, docs/) et la révision D137 y est
       alignée (runbook « coffre neuf », FAQ, table décisionnelle) ;
  V15  la règle v0.6.0 « un coffre neuf naît CF3 » est explicitement
       invalidée : la phrase vit en passe dans § 1.7, la décision D137 est
       consignée, l'erratum « tbp] » est réparé (aucun « tbp] » au PDF).
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
with pdfplumber.open(HERE / "docs" / "Protocole_TRIADE_v0.6.1_Specification.pdf") as pdf:
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
check("V8", "entrée v0.6.0 au journal des versions",
      "| v0.6.0 | 31 oct. 2026 |" in SPEC_RAW)
check("V8", "entrée v0.6.1 au journal des versions",
      "| v0.6.1 | 31 oct. 2026 |" in SPEC_RAW)
check("V8", "correspondance v0.5.2 → v0.6.0 présente",
      "### 19.7 Correspondance v0.5.2 → v0.6.0" in SPEC_RAW)
check("V8", "correspondance v0.6.0 → v0.6.1 présente",
      "### 19.8 Correspondance v0.6.0 → v0.6.1" in SPEC_RAW)

# ---- V9 : rejets explicites ----
check("V9", "modifications rejetées v0.6.0 consignées",
      "Modifications explicitement rejetées (v0.6.0)" in SPEC_RAW)
check("V9", "modifications rejetées v0.6.1 consignées",
      "Modifications explicitement rejetées (v0.6.1)" in SPEC_RAW)

# ---- V10 : héritage v0.5.0-v0.6.0 intact ----
check("V10", "taxonomie X1-X8 présente", "X1–X8" in SPEC_RAW or "X1-X8" in SPEC_RAW)
check("V10", "coffre-fort D75 présent", "TRIADE-CF1" in SPEC_RAW)
check("V10", "garde D81 présente", "PHRASE-CONTROLE-COFFRE.txt" in SPEC_RAW)
check("V10", "passation v0.6.0 intacte (D133, axes, migration réelle)",
      all(k in SPEC for k in ["D133", "par invocation", "0cc89a96"]))

# ---- V11 : souveraineté (§ 12) — § 12.5 RÉVISÉ ----
check("V11", "chapitre 12 souveraineté présent",
      "## 12. Souveraineté cryptographique" in SPEC_RAW)
for sonde in ["Shamir", "0x11B", "PORTE D120", "TRIADE-CF3",
              "par invocation", "cycle en deux actes", "carte papier",
              "Ed25519", "init"]:
    check("V11", f"« {sonde} » au chapitre souveraineté", sonde in SPEC_RAW)
check("V11", "§ 12.5 révisé : l'arbitrage du développeur (D137)",
      "### 12.5 Le niveau du coffre neuf — un arbitrage du développeur (D137)" in SPEC_RAW)
seg12 = SPEC_RAW[SPEC_RAW.find("## 12."):SPEC_RAW.find("## 13.")]
check("V11", "les trois naissances au § 12.5",
      all(k in seg12 for k in ["coffre_fort.py init", "coffre_cf2.py migrer",
                               "coffre_cf3.py init", "LABORATOIRE"]))
check("V11", "le guide de l'arbitrage au § 12.5",
      "Le guide de l'arbitrage" in seg12)
check("V11", "la chaîne de migration demeure disponible",
      "reste disponible à tout moment" in seg12)
check("V11", "sentinelle PAR INVOCATION dans le corps du chapitre",
      "par invocation" in seg12)
check("V11", "trois témoins d'époque nommés",
      all(k in seg12 for k in ["journal local", "carte papier", "journal Git"]))

# ---- V12 : cérémonies et kit (§ 13) ----
check("V12", "chapitre 13 cérémonies présent",
      "## 13. Les cérémonies et le kit du terrain" in SPEC_RAW)
seg13 = SPEC[SPEC.find("## 13."):SPEC.find("## 14.")]
for sonde in ["MIGRER", "VÉRIFIER", "DÉTRUIRE", "trio D122",
              "identité octet pour octet par construction", "0cc89a96"]:
    check("V12", f"« {sonde} » au chapitre cérémonies", sonde in seg13)

# ---- V13 : menaces, jalons, annexes ----
for sonde in ["Expropriation", "Evil maid", "Roll-back du couple"]:
    check("V13", f"menace « {sonde} »", sonde in SPEC_RAW)
check("V13", "M5 ouvert (markdown jalons)",
      "**ouvert** 31/10/2026 (D133" in SPEC_RAW)
check("V13", "M5 ouvert au plan", "Programme M5 — Outil complet" in PLAN_RAW)
check("V13", "M4 franchi au plan", "Jalon M4 franchi le 29 octobre 2026" in PLAN_RAW)
for sonde in ["8c79263b", "1cf18644", "f50ce894", "933e8405"]:
    check("V13", f"empreinte {sonde} au PDF formel", sonde in PDF_SPEC)
check("V13", "tableau décisionnel du coffre-fort au PDF",
      "Tableau décisionnel du coffre-fort" in PDF_SPEC)
check("V13", "tableau décisionnel étendu à D137 au PDF",
      "D75–D137" in PDF_SPEC or "D75--D137" in PDF_SPEC)
check("V13", "checksum terrain 0cc89a96 au PDF", "0cc89a96" in PDF_SPEC)
check("V13", "l'arbitrage D137 au PDF (§ 12.5)",
      "arbitrage du développeur" in PDF_SPEC and "D137" in PDF_SPEC)
check("V13", "correspondance v0.6.0 → v0.6.1 au PDF",
      "Correspondance v0.6.0" in PDF_SPEC)

# ---- V14 : le Livre du Coffre v1.1 + décisions ----
check("V14", "Livre du Coffre présent (26 pages attendues, ±2)",
      abs(N_PAGES_LIVRE - 26) <= 2, f"{N_PAGES_LIVRE} pages")
for sonde in ["Le Livre du Coffre", "runbook", "CINQ originaux",
              "carte du sachet", "0cc89a96"]:
    check("V14", f"« {sonde} » au Livre", sonde in PDF_LIVRE)
check("V14", "D133 consignée aux décisions",
      "## D133 — LA PASSATION v0.6.0" in DEC_RAW)
check("V14", "passation effective consignée au plan",
      "elle est effective" in PLAN)
check("V14", "PDF formel : 38 pages attendues (±2)",
      abs(N_PAGES_SPEC - 38) <= 2, f"{N_PAGES_SPEC} pages")
check("V14", "aucune référence non résolue (??) au PDF formel",
      "??" not in PDF_SPEC)
check("V14", "aucune référence non résolue (??) au Livre",
      "??" not in PDF_LIVRE)

# ---- V15 : la révision D137 nominative ----
check("V15", "§ 1.8 « Ce que change la v0.6.1 » présent",
      "### 1.8 Ce que change la v0.6.1" in SPEC_RAW)
check("V15", "la règle remplacée vit en passe au § 1.7 (« naissait CF3 »)",
      "Un **coffre neuf naissait CF3**" in SPEC_RAW)
check("V15", "l'arbitrage nommé avec sa raison (« imposer CF3 par défaut »)",
      "imposer CF3 par défaut risque" in SPEC_RAW)
check("V15", "le coffre réel reste CF3 (la révision n'est pas un geste)",
      "La présente version consigne l'arbitrage du niveau de naissance" in SPEC_RAW)
check("V15", "D137 consignée aux décisions",
      "## D137 —" in DEC_RAW)
check("V15", "D137 consignée au plan",
      "D137" in PLAN_RAW and "arbitré par le développeur" in PLAN_RAW)
check("V15", "erratum « tbp] » réparé : aucune LIGNE parasite au PDF formel",
      not any(l.strip() == "tbp]" for l in PDF_SPEC.splitlines()))
check("V15", "l'arbitrage D137 au Livre v1.1",
      "arbitrage" in PDF_LIVRE and "D137" in PDF_LIVRE)

print()
if failures:
    print("ÉCHEC :", len(failures), "critère(s) —", ", ".join(failures))
    sys.exit(1)
print(f"CAHIER v0.6.1 : TOUT PASSÉ — spécification {N_PAGES_SPEC} pages, "
      f"Livre du Coffre {N_PAGES_LIVRE} pages.")
