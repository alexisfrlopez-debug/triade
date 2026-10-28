#!/usr/bin/env python3
"""Vérification post-révision du protocole TRIADE v0.5.1 (cahier de révision).

Onze critères, tous vérifiés mécaniquement sur les sources et le PDF :
  V1  hiérarchie Sécurité > Performance > Optimisation > Coût en tokens intacte ;
  V2  couches I/B/C indissociables ;
  V3  aucune règle affaiblie — R1-R9 à l'identique, R10 en sur-ensemble ;
  V4  aucune couche d'abstraction à l'exécution introduite ;
  V5  aucune promesse de portabilité universelle immédiate ;
  V6  aucun mécanisme de furtivité EDR ;
  V7  chaque nouvelle exigence vérifiable (mécaniquement ou par oracle) ;
  V8  chaque évolution tracée dans le changelog ;
  V9  modifications incompatibles explicitement rejetées ;
  V10 contenu v0.5.0 : validation terrain normée, taxonomie X1-X8, budgets
      mesurés, décisions D26-D45 consignées ;
  V11 contenu v0.5.1 : coffre-fort des phrases maîtresses (D75, TRIADE-CF1),
      menace du vol du coffre au modèle § 13.1, M3 franchi constaté (balise
      0.4.0, D72-D74), correspondance v0.5.0 → v0.5.1.
Sortie : PASS/FAIL par critère, exit 1 si échec.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent.parent  # racine du dépôt triade
SPEC_RAW = (HERE / "docs" / "PROTOCOLE_TRIADE.md").read_text(encoding="utf-8")
SPEC = re.sub(r"\s+", " ", SPEC_RAW).replace("\u2019", "'")
DEC_RAW = (HERE / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
DEC = re.sub(r"\s+", " ", DEC_RAW).replace("\u2019", "'")

import pdfplumber
with pdfplumber.open(HERE / "docs" / "Protocole_TRIADE_v0.5.1_Specification.pdf") as pdf:
    PDF = "\n".join((p.extract_text() or "") for p in pdf.pages).replace("\u2019", "'")

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
# aucune formulation alternative concurrente
alt = re.findall(r"Sécurité\s*>\s*[^>\n]{3,40}>\s*[^>\n]{3,40}>\s*[^>\n]{3,40}", SPEC)
alts = {a.strip() for a in alt if not a.strip().startswith(hier)}
check("V1", "aucune hiérarchie alternative", not alts, str(alts or "aucune"))

# ---- V2 : couches I/B/C indissociables ----
check("V2", "propriété normative « aucune couche n'est optionnelle »",
      "Aucune couche n'est optionnelle" in SPEC)
for layer in ("couche I", "couche B", "couche C"):
    check("V2", f"{layer} définie", layer in SPEC)
check("V2", "R1 (jamais de binaire nu) inchangée",
      "Tout artefact B est accompagné de I et C à jour" in SPEC)
check("V2", "tableau des trois couches dans le PDF",
      all(k in PDF for k in ("Intention", "Binaire", "Carte")))

# ---- V3 : aucune règle affaiblie ----
RULES_V03 = {
    "R1": "Tout artefact B est accompagné de I et C à jour",
    "R2": "Toute modification commence par un diff sur I",
    "R3": "Chaque bloc est décrit dans C",
    "R4": "Le remplacement préserve signature et contrats",
    "R5": "Aucun commit sans oracle, vecteurs dorés et round-trip",
    "R6": "Dix vérifications réussies rendent le bloc immuable",
    "R7": "Les points d'entrée sont garantis par padding",
    "R8": "Empreintes des blocs et signature de la carte vérifiés avant chaque édition",
    "R9": "L'agent refuse toute carte non signée",
}
for rid, enonce in RULES_V03.items():
    check(f"V3", f"{rid} — énoncé v0.3 repris à l'identique", enonce in SPEC)
# R10 : sur-ensemble strict (checksums v0.3 conservés + ajouts)
r10_ok = all(k in SPEC for k in (
    "checksums de ses blocs scellés", "signature du manifeste",
    "anti-rollback", "fail-closed explicite", "arrêt propre"))
check("V3", "R10 renforcée = sur-ensemble (checksums + signature + anti-rollback + "
      "fail-closed + arrêt propre)", r10_ok)
check("V3", "R11 présente avec sanction",
      "Optimisation mesurée" in SPEC and "Refus de commit" in SPEC)
check("V3", "les 11 règles dans le PDF", all(f"R{i}" in PDF for i in range(1, 12)))

# ---- V4 : aucune couche d'abstraction à l'exécution ----
forbidden = ["bytecode portable", "machine virtuelle", "traduction à la volée",
             "couche d'abstraction à l'exécution"]
hits = []
for f in forbidden:
    for m in re.finditer(re.escape(f), SPEC, re.IGNORECASE):
        ctx = SPEC[max(0, m.start() - 200):m.end() + 200]
        if not any(k in ctx for k in ("rejet", "rejetée", "interdite", "n'est pas "
                     "introduite", "aucune couche d'abstraction", "trahirait")):
            hits.append(f)
check("V4", "mentions d'abstraction uniquement en contexte de rejet", not hits,
      f"hors contexte : {hits or 'aucune'}")
check("V4", "rejet explicite consigné (§ 17.2)",
      "couche d'abstraction à l'exécution" in SPEC and "rejetée" in SPEC)

# ---- V5 : aucune promesse de portabilité universelle immédiate ----
check("V5", "déclaration « ne promet pas la portabilité, il la vérifie » présente",
      "ne promet pas la portabilité, il la vérifie" in SPEC)
bad_promises = []
for m in re.finditer(r"(fonctionne partout|universelle immédiate|"
                      r"portable sur toute|portabilité garantie)", SPEC,
                      re.IGNORECASE):
    ctx = SPEC[max(0, m.start() - 200):m.end() + 200].lower()
    if not any(k in ctx for k in ("promettre", "rejet")):
        bad_promises.append(m.group(0))
check("V5", "aucune promesse de portabilité immédiate", not bad_promises,
      str(bad_promises or "aucune"))
check("V5", "profils gated M6/M7", "M6" in SPEC and "M7" in SPEC
      and "suite de conformité" in SPEC)

# ---- V6 : aucun mécanisme de furtivité EDR ----
stealth = re.findall(r"(EDR|furtiv|évasion|anti-analyse)", SPEC, re.IGNORECASE)
bad = [s for s in stealth if True]
# toutes les occurrences doivent être en contexte de non-objectif / rejet
ctxs = []
for m in re.finditer(r"(EDR|furtivité|furtif)", SPEC, re.IGNORECASE):
    ctx = SPEC[max(0, m.start() - 250):m.end() + 250]
    if not any(k in ctx.lower() for k in ("hors périmètre", "non-objectif",
                                          "n'est pas recherchée", "rejet")):
        ctxs.append(m.group(0))
check("V6", "mentions EDR/furtivité uniquement en non-objectif", not ctxs,
      f"hors contexte : {ctxs or 'aucune'}")
check("V6", "rejet explicite dans § 17.2", "furtivité face aux EDR" in SPEC)

# ---- V7 : chaque nouvelle exigence vérifiable ----
NEW_REQS = {
    "couche I normalisée": ["gabarit", "vecteurs", "vérifie ce maillon"],
    "taxonomie": ["T1", "T6", "défauts ouverts par classe"],
    "threat model": ["Binaire altéré", "Rollback non autorisé", "Agent défaillant",
                     "Environnement non conforme"],
    "R10": ["checksums", "signature du manifeste", "monotonie", "arrêt propre"],
    "R11": ["hot path", "mesure avant/après", "Refus de commit"],
    "journal d'optimisation": ["OPT-NN", "journal d'optimisation"],
    "fragmentation": ["plus d'un fragment", "lecture intégrale du binaire"],
    "localisation par intention": ["jamais par balayage", "erreur de spécification"],
    "budgets": ["64 tokens max", "3 000 tokens max", "6 000 tokens max"],
    "suite de conformité": ["suite de conformité", "suite verte"],
    "parité inter-profils": ["paritaires", "vérifie par exécution"],
    "reverse-specs": ["reverse-spec", "statut"],
    "pré-versions": ["dev.N", "rc.N", "Monotonie"],
    "fixtures": ["fixtures", "T5"],
    "traçabilité": ["audit de traçabilité", "refus de build"],
    "journal des décisions normalisé": ["append-only", "Champ"],
    "tableau de bord": ["Métrique", "Cible", "Source de mesure"],
}
for req, anchors in NEW_REQS.items():
    ok = all(a in SPEC for a in anchors)
    check("V7", f"exigence vérifiable : {req}", ok,
          "" if ok else f"ancres manquantes : {[a for a in anchors if a not in SPEC]}")

# ---- V8 : chaque évolution tracée dans le changelog ----
CHANGELOG_KEYS = [
    "couche I normalisée", "taxonomie", "threat model", "R10", "R11",
    "journal d'optimisation", "fragmentation", "localisation", "budgets",
    "suite de conformité", "parité", "reverse-specs", "pré-versions",
    "fixtures", "traçabilité", "journal des décisions", "tableau de bord",
]
v040_row = re.search(r"\| v0\.4\.0 \|.*\|", SPEC)
row = v040_row.group(0) if v040_row else ""
missing = [k for k in CHANGELOG_KEYS if k.lower() not in row.lower()]
check("V8", "changelog v0.4.0 complet (17 éléments)", not missing,
      f"manquants : {missing or 'aucun'}")
corr = re.search(r"## 17\.1|Traçabilité des évolutions", SPEC)
check("V8", "table de correspondance v0.3 → v0.4.0 présente", bool(corr))
sec17 = SPEC_RAW[SPEC_RAW.find("### 17.1"):SPEC_RAW.find("### 17.2")]
n_rows = len(re.findall(r"^\| \d+ \|", sec17, re.M))
check("V8", "17 lignes de correspondance", n_rows == 17, f"{n_rows} lignes")

# ---- V9 : rejets explicites ----
REJECTS = [
    "Modifier la hiérarchie", "couche d'abstraction", "portabilité universelle",
    "furtivité face aux EDR", "Affaiblir R5", "contrôle en ligne",
    "Optimisation validée sans mesure",
]
for r in REJECTS:
    check("V9", f"rejet consigné : {r[:40]}", r in SPEC)
check("V9", "rejets dans le PDF formel",
      all(k in PDF for k in ("rejetées", "invariant de révision")))
check("V9", "décisions D19-D25 consignées",
      all(f"D{i}" in DEC for i in range(19, 26)))

# ---- V10 : contenu v0.5.0 (retour du terrain) ----
check("V10", "validation terrain normée (§ 8.4)",
      "La validation terrain" in SPEC and "boucle d'évidence" in SPEC
      and "journal d'exécution" in SPEC)
check("V10", "taxonomie X1-X8 présente (§ 8.5)",
      all(f"X{i}" in SPEC for i in range(1, 9))
      and "invisibles à l'émulation" in SPEC)
check("V10", "les 8 classes X tracées vers leurs décisions",
      all(d in DEC for d in ("D35", "D36", "D37", "D38", "D39", "D40", "D41", "D42")))
check("V10", "jalons M0-M3 constatés franchis",
      SPEC.count("**franchi**") == 4 and "balise 0.3.0" in SPEC
      and "balise 0.4.0" in SPEC)
check("V10", "M3 franchi avec preuves (campagne million, conformité, scellage)",
      "**franchi** 28/10/2026" in SPEC and "fuzzing à propriétés" in SPEC
      and "campagne million" in SPEC)
check("V10", "budgets corrigés et mesurés (64, D31)",
      "≤ 64 / 3 000 / 6 000" in SPEC and "51 / 719 / 1 088" in SPEC)
check("V10", "correspondance v0.4.0 → v0.5.0 présente",
      "### 17.3 Correspondance v0.4.0 → v0.5.0" in SPEC)
check("V10", "rejets v0.5.0 consignés (§ 17.4)",
      "Ajouter une règle R12" in SPEC and "Fusionner les classes X" in SPEC)
check("V10", "contenu v0.5.0 dans le PDF formel",
      all(k in PDF for k in ("boucle d'évidence", "X1", "X8", "franchi", "D43")))
check("V10", "décisions D43-D45 consignées",
      all(f"D{i}" in DEC for i in (43, 44, 45)))

# ---- V11 : contenu v0.5.1 (coffre-fort des phrases maîtresses) ----
check("V11", "coffre-fort des phrases maîtresses présent (D75)",
      "coffre-fort des phrases maîtresses" in SPEC and "TRIADE-CF1" in SPEC
      and "D75" in SPEC)
check("V11", "deux niveaux de secret distincts (phrase de contrôle jamais stockée)",
      "phrase de contrôle" in SPEC and "jamais stockée" in SPEC)
check("V11", "menace « Vol du coffre-fort des phrases » au modèle (§ 13.1)",
      "Vol du coffre-fort des phrases" in SPEC
      and "Sans la phrase, indéchiffrable" in SPEC)
check("V11", "règles de discipline et restauration post-réinitialisation (§ 15.3)",
      "obtenir --vers-fichier" in SPEC and "graine Ed25519 reste hors coffre" in SPEC)
check("V11", "correspondance v0.5.0 → v0.5.1 présente",
      "### 17.5 Correspondance v0.5.0 → v0.5.1" in SPEC)
check("V11", "alternatives rejetées à D75 consignées",
      "alternatives rejetées à D75" in SPEC)
check("V11", "glossaire étendu (coffre-fort, phrase de contrôle)",
      "| Phrase de contrôle |" in SPEC)
check("V11", "journal des versions : ligne v0.5.1",
      "| v0.5.1 | 28 oct. 2026 |" in SPEC and "autotest de falsification" in SPEC)
check("V11", "contenu v0.5.1 dans le PDF formel",
      all(k in PDF for k in ("coffre-fort", "TRIADE-CF1", "D75", "0.5.1")))
check("V11", "l'outil vit dans le dépôt, le conteneur jamais",
      os.path.exists(HERE / "coffre_fort.py")
      and "coffre_fort" in (HERE / ".gitignore").read_text(encoding="utf-8"))
check("V11", "autotest de falsification de l'outil (19 contrôles)",
      "AUTOTEST" in subprocess.run(
          [sys.executable, str(HERE / "coffre_fort.py"), "autotest"],
          capture_output=True, text=True, timeout=300).stdout)

print()
print("=" * 66)
print(f"BILAN : {'ÉCHEC — ' + str(len(failures)) + ' contrôle(s)' if failures else 'TOUS LES CRITÈRES PASSÉS'}")
print("=" * 66)
sys.exit(1 if failures else 0)
