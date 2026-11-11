#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_edition_v110.py — le vérificateur de l'édition v0.11.0 (l'étape
de vérification obligatoire du deuxième fichier d'instruction, rejouable) :

  V1 (a) le rejeu intégral des harnais : le constat rejeu_complet.txt porte
      les verdicts VERTS des 10 harnais + le garde 14/14 (le rejeu vécu au
      geste) ; les empreintes des artefacts scellés byte pour byte ;
  V2 (c) les données : l'extraction v0.11.0 re-passée VERT (les six preuves
      EXIGÉES — le script refuse si une manque) ; les valeurs clés des
      preuves vivent dans le manuscrit ;
  V3 (d) la traçabilité : chaque exigence nouvelle de la couche I (le
      brouillon tls13-29) reliée à ses vecteurs ; l'audit de gouvernance
      VERT (D1..D186 append-only) ;
  V4 (e) les archives : le numéro v0.11.0 aux noms, la soumission compte
      cinq fichiers au plus (readme + manuscrit pdf), le complet porte
      l'intégralité (les six instruments + sorties + la spec CSPRNG + le
      corpus RFC 8446) ;
  V5 les formulation : le manuscrit v0.11.0 porte la section des preuves
      renforcées et les limites marquées non prouvées.

Usage : python3 scripts/verifier_edition_v110.py — code 0 = VERT.
"""
import hashlib
import pathlib
import re
import subprocess
import sys
import zipfile

import pdfplumber

REPO = pathlib.Path(__file__).resolve().parents[1]
LIV = REPO / "download" / "edition_v0110"
PREUVES = REPO / "scripts" / "preuves_v110"
ecarts = []


def verifie(cid, nom, ok, detail=""):
    print(f"[{cid}] {nom} : {'VERT' if ok else 'ÉCART'}"
          + (f" — {detail}" if detail else ""))
    if not ok:
        ecarts.append(f"{cid} {nom}")


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --- V1 : le constat du rejeu + les empreintes ---
rejeu = (PREUVES / "rejeu_complet.txt").read_text(encoding="utf-8")
n_verts = rejeu.count("VERDICT : VERT") + rejeu.count("verts · 0 échecs")
verifie("V1", "le constat porte les 10 harnais VERTS", n_verts >= 10,
        f"{n_verts} verdicts verts")
verifie("V1", "le garde du sceau 14/14 au constat", "14 arbres VERTS" in rejeu)
loupe = sha256(REPO / "loupe" / "loupe.exe")
proxy = sha256(REPO / "tls13" / "proxy.exe")
verifie("V1", "loupe.exe == la pièce scellée (c1115105…)",
        loupe == "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1")
verifie("V1", "proxy.exe == la pièce scellée (446279f3…)",
        proxy == "446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d")

# --- V2 : les données et preuves ---
ext = subprocess.run(["python3", "scripts/extraire_donnees_v110.py",
                      "--verifier"], cwd=REPO, capture_output=True, text=True)
verifie("V2", "l'extraction v0.11.0 VERT (les six preuves exigées)",
        ext.returncode == 0, ext.stdout.strip().splitlines()[-1]
        if ext.stdout.strip() else ext.stderr[:100])
mp = REPO / "docs" / "TRIADE_manuscrit_v0.11.0.pdf"
texte = ""
with pdfplumber.open(mp) as pdf:
    pages = len(pdf.pages)
    for p in pdf.pages:
        texte += (p.extract_text() or "") + "\n"
sans_espaces = re.sub(r"\s+", "", texte.lower())
verifie("V2", "le manuscrit v0.11.0 existe et se lit", pages >= 10,
        f"{pages} pages")
attendus = ["694/832", "83.4", "60.5", "15.3", "4,524", "69,132",
            "1,181", "zerodivergences", "1,238,959"]
absents = [a for a in attendus
           if re.sub(r"[\s,%]", "", a).lower() not in sans_espaces
           and re.sub(r"[\s%]", "", a).replace(",", ",").lower()
           not in sans_espaces]
verifie("V2", "les chiffres des six instruments vivent au manuscrit",
        not absents, f"absents : {absents or 'aucun'}")

# --- V3 : la traçabilité et la gouvernance ---
spec29 = (REPO / "tls13" / "notation" / "brouillons"
          / "tls13-29-source-csprng.md").read_text(encoding="utf-8")
verifie("V3", "la spec CSPRNG (brouillon) porte ses vecteurs",
        "RFC 8448" in spec29 and "RFC 7748" in spec29 and "KIT96" in spec29)
corpus = (REPO / "tls13" / "fixtures" / "rfc8446.py").read_text(encoding="utf-8")
verifie("V3", "le corpus RFC 8446 porte les sentinelles citées",
        "DOWNGRD" in corpus and "0x1301" in corpus and "0x001D" in corpus)
audit = subprocess.run(["python3", "scripts/audit_gouvernance_v100.py"],
                       cwd=REPO, capture_output=True, text=True)
verifie("V3", "l'audit de gouvernance VERT (D1..D186)", audit.returncode == 0)

# --- V4 : les archives ---
soum = LIV / "TRIADE_soumission_v0.11.0.zip"
comp = LIV / "TRIADE_complet_v0.11.0.zip"
if not soum.exists() or not comp.exists():
    verifie("V4", "les deux livrables existent", False)
else:
    zs = zipfile.ZipFile(soum)
    ns = zs.namelist()
    verifie("V4", "la soumission compte cinq fichiers au plus", len(ns) <= 5,
            f"{len(ns)}")
    verifie("V4", "la soumission porte readme et manuscrit pdf",
            "README.txt" in ns and any(n.endswith("v0.11.0.pdf") for n in ns))
    verifie("V4", "le numéro v0.11.0 aux noms des deux zips",
            "v0.11.0" in soum.name and "v0.11.0" in comp.name)
    zc = zipfile.ZipFile(comp)
    nc = zc.namelist()
    requis = ["README.txt", "manuscrit/main.tex",
              "instruments/mutation_v110.py", "instruments/fuzzage_v110.py",
              "instruments/surete_memoire_v110.py",
              "instruments/temps_constant_v110.py",
              "instruments/benchmarks_v110.py",
              "instruments/independance_v110.py",
              "instruments/sorties/mutation.csv",
              "spec-csprng/tls13-29-source-csprng.md",
              "corpus/rfc8446.py", "VERIFICATION_v0.11.0.txt"]
    manquants = [r for r in requis if r not in nc]
    verifie("V4", "le complet porte l'intégralité requise",
            not manquants, f"manquants : {manquants or 'aucun'} ({len(nc)})")

# --- V5 : la formulation et les limites ---
verifie("V5", "la section des preuves renforcées présente",
        "strengthenedevidence" in sans_espaces)
verifie("V5", "les limites marquées non prouvées",
        "notproven" in sans_espaces or "unmeasured" in sans_espaces,
        "le temps réel et les canaux auxiliaires marqués")

print()
if ecarts:
    print(f"VÉRIFICATEUR DE L'ÉDITION v0.11.0 : {len(ecarts)} ÉCART(S) — "
          + " ; ".join(ecarts))
    sys.exit(1)
print("VÉRIFICATEUR DE L'ÉDITION v0.11.0 : VERT — rejeu, preuves, "
      "traçabilité, archives et formulation tous constatés.")
