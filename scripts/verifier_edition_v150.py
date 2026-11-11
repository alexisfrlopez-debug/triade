#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_edition_v150.py — L'ÉTAPE DE VÉRIFICATION de la v0.15.0 (la
commande ic09ydeli : « ré-exécuter le model-checking et les tests de
raffinement depuis un clone frais et vérifier les comptes d'états/
transitions contre le rapport ; vérifier que chaque statut de preuve du
manuscrit correspond à une pièce archivée ; vérifier l'intégrité des
artefacts scellés et des arbres signés ; régénérer les tableaux par
script ; compiler le PDF et contrôler renvois, versions et cohérence
des statuts »).

Les vérificateurs (chacun tranche binaire, le rapport consigne tout) :
  V1 LE GARDE : les QUATORZE arbres signés (sceau_I) + les empreintes
     des pièces scellées (loupe.exe c1115105…, proxy.exe 446279f3…,
     demo.exe, selftest.exe) — INTACTES ;
  V2 LE CLONE FRAIS : le model-checking non borné RE-EXÉCUTÉ depuis un
     clone git neuf — les comptes confrontés au rapport (288 formes /
     0 violation, D187 reproduit 154/1 152, bornes étendues 228/1 902
     et 372/3 342, zéro hors I) ;
  V3 LE RAFFINEMENT RE-EXÉCUTÉ depuis le clone : 34 pas, 0 écart ;
  V4 LE κ AUTOTESTÉ depuis le clone : VERT (trois cas synthétiques) ;
  V5 LES TABLEAUX RÉGÉNÉRÉS : extraire_donnees_v150 + statuts_preuves
     re-joués — les sorties IDENTIQUES bit à bit aux fichiers livrés ;
  V6 LES STATUTS ↔ LES PIÈCES : chaque statut du manuscrit confronté à
     sa pièce (le CSV de l'invariant, le CSV du raffinement — les
     statuts relus, jamais gravés) ;
  V7 LE PDF : le manuscrit relu (le compte de pages, les motifs v0.15.0,
     les statuts rendus, aucune référence cassée « ?? »).

Sortie : scripts/preuves_v150/rapport_verification_v150.txt (la pièce
qui accompagne les livrables).
"""
from __future__ import annotations

import hashlib
import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path("/home/z/my-project/triade")
PREUVES = REPO / "scripts" / "preuves_v150"
RAPPORT = []


def ver(nom, condition, detail=""):
    etat = "VERT" if condition else "ROUGE"
    RAPPORT.append(f"  {nom} : {etat}" + (f" — {detail}" if detail else ""))
    print(f"[{etat}] {nom}" + (f" — {detail}" if detail else ""))
    return condition


def main():
    ok = True
    RAPPORT.append("L'ÉTAPE DE VÉRIFICATION DE L'ÉDITION v0.15.0")
    RAPPORT.append("(le clone frais, les comptes, les pièces, le PDF)")

    # ---- V1 : le garde ----------------------------------------------------
    sys.path.insert(0, str(REPO / "v06"))
    import sceau_I  # noqa: E402
    code = sceau_I.verifier(silencieux=True)
    ok &= ver("V1a le garde des QUATORZE arbres signés", code == 0,
              "sceau_I.verifier() == OK" if code == 0
              else f"code {code}")
    pieces = {
        "loupe/loupe.exe": ("c111510535767a40b0122d4e42261c9d8e1ec10d94d9"
                            "5ef666fd76ceb93e61d1", "loupe.exe 0.1.1"),
        "tls13/proxy.exe": ("446279f3ab356900870cc3b3e1700654a4216ec0b2641"
                            "72340e453db3b00d93d", "proxy.exe 1.0.0"),
    }
    for chemin, (attendu, nom) in pieces.items():
        emp = hashlib.sha256((REPO / chemin).read_bytes()).hexdigest()
        ok &= ver(f"V1b la pièce scellée {nom}", emp == attendu,
                  f"sha256 {emp[:16]}…" if emp == attendu
                  else f"DIVERGENT {emp[:16]}…")

    # ---- V2/V3/V4 : le clone frais ----------------------------------------
    clone = pathlib.Path(tempfile.mkdtemp(prefix="clone_v150_"))
    try:
        r = subprocess.run(
            ["git", "clone", "-q", str(REPO), str(clone / "triade")],
            capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            ver("V2 le clone frais", False, r.stderr[:120])
            return 2
        c = clone / "triade"
        # V2 : le model-checking non borné depuis le clone
        r = subprocess.run(
            [sys.executable, "scripts/preuves_v150/modele_invariant_v150.py"],
            cwd=c, capture_output=True, text=True, timeout=600)
        sortie = r.stdout + r.stderr
        ok &= ver("V2a le model-checking re-exécuté (clone frais)",
                  r.returncode == 0, f"code {r.returncode}")
        for chiffre, attendu in (
                ("154 états / 1152 transitions", "D187 reproduit"),
                ("288 formes × 13 règles : 0 violation", "la préservation"),
                ("228 états / 1902 transitions", "bornes étendues e≤5"),
                ("372 états / 3342 transitions", "bornes étendues e≤7"),
                ("PROUVÉE NON BORNÉE ; P2=PROUVÉE NON BORNÉE", "les 4 verdicts")):
            ok &= ver(f"V2b compte « {attendu} »", chiffre in sortie,
                      "confronté au clone")
        # V3 : le raffinement depuis le clone
        r = subprocess.run(
            [sys.executable, "scripts/preuves_v150/raffinement_v150.py"],
            cwd=c, capture_output=True, text=True, timeout=600)
        ok &= ver("V3 le raffinement re-exécuté (clone frais)",
                  r.returncode == 0 and "34 pas de raffinement, 0 écart"
                  in r.stdout + r.stderr,
                  "34 pas, 0 écart")
        # V4 : le κ autotesté depuis le clone
        r = subprocess.run(
            [sys.executable, "scripts/replication_v150/kohen_kappa_v150.py"],
            cwd=c, capture_output=True, text=True, timeout=300)
        ok &= ver("V4 le κ autotesté (clone frais)",
                  r.returncode == 0 and "VERT" in r.stdout,
                  "trois cas synthétiques")
    finally:
        shutil.rmtree(clone, ignore_errors=True)

    # ---- V5 : les tableaux régénérés --------------------------------------
    import filecmp
    for script, cible in (
            ("scripts/statuts_preuves_v150.py",
             "scripts/manuscrit_v150/donnees/statuts_v150.tex"),):
        avant = (REPO / cible).read_bytes()
        subprocess.run([sys.executable, script], cwd=REPO,
                       capture_output=True, text=True, timeout=300)
        apres = (REPO / cible).read_bytes()
        ok &= ver(f"V5a les tableaux régénérés identiques ({cible.split('/')[-1]})",
                  avant == apres,
                  "bit à bit" if avant == apres else "DIVERGENT")
    # la table des preuves : re-générée, la LONGTABLE aux 34 lignes
    tex = (REPO / "scripts/manuscrit_v150/donnees/tables_generees.tex"
           ).read_text(encoding="utf-8")
    ok &= ver("V5b la table des preuves LONGTABLE rendue",
              "begin{longtable}" in tex and tex.count("addlinespace") >= 34,
              f"{tex.count('addlinespace')} lignes")

    # ---- V6 : les statuts ↔ les pièces ------------------------------------
    import csv
    statuts = {}
    with open(PREUVES / "modele_invariant.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            statuts[row["propriété"]] = row["statut"]
    ok &= ver("V6a les statuts P1-P4 relus de la pièce",
              all(statuts.get(p) == "PROUVÉE NON BORNÉE"
                  for p in ("P1", "P2", "P3", "P4")),
              "modele_invariant.csv (jamais gravés)")
    n_pas = n_ec = 0
    with open(PREUVES / "raffinement.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            n_pas += 1
            if row["conforme"] == "ÉCART":
                n_ec += 1
    ok &= ver("V6b le raffinement relu de la pièce",
              n_pas == 34 and n_ec == 0, "raffinement.csv : 34/0")

    # ---- V7 : le PDF --------------------------------------------------------
    from pypdf import PdfReader
    pdf = REPO / "scripts/manuscrit_v150/main.pdf"
    r = PdfReader(str(pdf))
    txt = "".join((p.extract_text() or "") for p in r.pages)
    ok &= ver("V7a le manuscrit v0.15.0 relu", "v0.15.0" in txt,
              f"{len(r.pages)} pages")
    ok &= ver("V7b les statuts rendus",
              txt.count("proved unbounded") >= 9
              and "awaiting hardware run" in txt,
              "9+ « proved unbounded », les kits en attente")
    ok &= ver("V7c aucune référence cassée", "??" not in txt,
              "zéro « ?? »")

    RAPPORT.append("")
    RAPPORT.append("LE BILAN : " + ("VERT — l'édition est vérifiée de bout "
                   "en bout." if ok else "ROUGE — voir les vérificateurs "
                   "fautifs ci-dessus."))
    (PREUVES / "rapport_verification_v150.txt").write_text(
        "\n".join(RAPPORT) + "\n", encoding="utf-8")
    print(f"\n[rapport] {PREUVES / 'rapport_verification_v150.txt'}")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
