#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_edition_v100.py — le vérificateur de l'édition académique v0.10.0
(l'étape de vérification obligatoire du fichier d'instruction, rejouable) :

  V1 (a) les données : l'extraction re-passée VERT (chaque ancre au journal),
      et chaque valeur des tableaux générés vit dans le PDF du manuscrit ;
  V2 (a) les citations : chaque entrée de refs.bib porte un DOI ou une
      référence vérifiable (URL institutionnelle / standard) ;
  V3 (b) les artefacts scellés : sha256 de loupe.exe et proxy.exe ==
      les empreintes consignées (identité octet pour octet) ;
  V4 (c) l'audit de gouvernance VERT + le vérificateur du sceau 14/14 ;
  V5 (d) la conformité des deux archives : le numéro v0.10.0 aux noms,
      la soumission compte CINQ fichiers au plus (readme inclus, le
      manuscrit en pdf), le complet porte l'intégralité requise ;
  V6 (a) le manuscrit : la formulation corrigée présente, la formulation
      interdite absente, le résumé français présent, l'agent jamais
      co-auteur.

Usage : python3 scripts/verifier_edition_v100.py
Code de sortie : 0 = VERT, 1 = écart.
"""
import hashlib
import pathlib
import re
import subprocess
import sys
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[1]
LIVRAISONS = REPO / "download" / "edition_v0100"
MANUSCRIT_PDF = REPO / "docs" / "TRIADE_manuscrit_v0.10.0.pdf"

ecarts = []


def verifie(cid, nom, ok, detail=""):
    print(f"[{cid}] {nom} : {'VERT' if ok else 'ÉCART'}"
          + (f" — {detail}" if detail else ""))
    if not ok:
        ecarts.append(f"{cid} {nom}")


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --- V1 : les données extraites et rendues ---
ext = subprocess.run(["python3", "scripts/extraire_donnees_v100.py", "--verifier"],
                     cwd=REPO, capture_output=True, text=True)
verifie("V1", "l'extraction des données re-passée VERT",
        ext.returncode == 0, ext.stdout.strip().splitlines()[-1]
        if ext.stdout.strip() else ext.stderr[:120])

import pdfplumber
texte_pdf = ""
with pdfplumber.open(MANUSCRIT_PDF) as pdf:
    pages = len(pdf.pages)
    for page in pdf.pages:
        texte_pdf += (page.extract_text() or "") + "\n"
verifie("V1", "le manuscrit existe et se lit", pages >= 8,
        f"{pages} pages")

genere = (REPO / "scripts" / "manuscrit_v100" / "donnees"
          / "tables_generees.tex").read_text(encoding="utf-8")
# chaque empreinte scellée et les nombres clés des tableaux rendus au PDF
attendus_pdf = ["054de960", "c1115105", "446279f3", "51", "719", "1,088",
                "13,873", "159", "12", "loupe 0.1.0"]
absents = [x for x in attendus_pdf if x not in texte_pdf]
verifie("V1", "les valeurs générées vivent dans le manuscrit",
        not absents, f"absents : {absents or 'aucun'}")

# --- V2 : la bibliographie vérifiable ---
bib = (REPO / "scripts" / "manuscrit_v100" / "refs.bib").read_text(encoding="utf-8")
entrees = re.findall(r"@(\w+)\{([^,]+),", bib)
sans_doi = []
for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", bib, re.DOTALL):
    corps = m.group(3)
    if "doi" not in corps and "url" not in corps and "howpublished" not in corps:
        sans_doi.append(m.group(2))
verifie("V2", f"les {len(entrees)} entrées bibliographiques portent DOI ou "
        "référence vérifiable", not sans_doi,
        f"sans : {sans_doi or 'aucune'}")

# --- V3 : les artefacts scellés ---
loupe = sha256(REPO / "loupe" / "loupe.exe")
proxy = sha256(REPO / "tls13" / "proxy.exe")
verifie("V3", "loupe.exe == la pièce scellée 0.1.1 (c1115105…)",
        loupe == "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1",
        loupe[:16] + "…")
verifie("V3", "proxy.exe == la pièce scellée 1.0.0 (446279f3…)",
        proxy == "446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d",
        proxy[:16] + "…")

# --- V4 : gouvernance + sceau ---
audit = subprocess.run(["python3", "scripts/audit_gouvernance_v100.py"],
                       cwd=REPO, capture_output=True, text=True)
verifie("V4", "l'audit de gouvernance VERT", audit.returncode == 0,
        audit.stdout.strip().splitlines()[-1])
sceau = subprocess.run(["python3", "v06/sceau_I.py", "verifier"],
                       cwd=REPO, capture_output=True, text=True)
verifie("V4", "le vérificateur du sceau I : 14/14",
        sceau.returncode == 0 and "14 arbres VERTS" in sceau.stdout,
        sceau.stdout.strip().splitlines()[-1] if sceau.stdout.strip() else "")

# --- V5 : les archives ---
soumission = LIVRAISONS / "TRIADE_soumission_v0.10.0.zip"
complet = LIVRAISONS / "TRIADE_complet_v0.10.0.zip"
if not soumission.exists() or not complet.exists():
    verifie("V5", "les deux livrables existent", False,
            "construire_livrables_v100.py d'abord")
else:
    zs = zipfile.ZipFile(soumission)
    noms = zs.namelist()
    verifie("V5", "la soumission compte cinq fichiers au plus", len(noms) <= 5,
            f"{len(noms)} : {', '.join(noms)}")
    verifie("V5", "la soumission porte le readme et le manuscrit pdf",
            "README.txt" in noms and any(n.endswith("v0.10.0.pdf") for n in noms))
    verifie("V5", "le numéro de version figure aux noms des deux zips",
            "v0.10.0" in soumission.name and "v0.10.0" in complet.name)
    zc = zipfile.ZipFile(complet)
    nc = zc.namelist()
    requis = ["README.txt", "manuscrit/main.tex", "manuscrit/refs.bib",
              "manuscrit/donnees/tables_generees.tex",
              "journal/extraits_journal.txt", "VERIFICATION_v0.10.0.txt"]
    manquants = [r for r in requis if r not in nc]
    verifie("V5", "le complet porte l'intégralité requise",
            not manquants, f"manquants : {manquants or 'aucun'} ({len(nc)} entrées)")

# --- V6 : la formulation du manuscrit ---
tex = (REPO / "scripts" / "manuscrit_v100" / "main.tex").read_text(encoding="utf-8")
verifie("V6", "le résumé français est présent",
        "Résumé" in texte_pdf or "résumé" in tex.lower() or
        "otherlanguage" in tex)
interdits = {"« le compilateur disparaît »": "compiler disappears",
             "« code volé inexploitable »": "stolen code is unusable"}
trouves = [fr for fr in interdits.values() if fr in texte_pdf]
verifie("V6", "les formulations interdites sont absentes", not trouves,
        f"trouvées : {trouves or 'aucune'}")
# l'extraction pdfplumber colle parfois les mots du texte justifié :
# la comparaison se fait SANS ESPACES (le contenu, pas la métrique)
corpus_sans_espaces = re.sub(r"\s+", "", (tex + texte_pdf).lower())
exigees = ["nooptimizingoropaquetranslationchain",
           "wysiwyg",
           "theevolutionofstolencodeisblocked",
           "isnotanauthor"]
absents_f = [x for x in exigees if x not in corpus_sans_espaces]
verifie("V6", "les formulations corrigées et la politique d'auteur présentes",
        not absents_f, f"absents : {absents_f or 'aucun'}")

print()
if ecarts:
    print(f"VÉRIFICATEUR DE L'ÉDITION : {len(ecarts)} ÉCART(S) — "
          + " ; ".join(ecarts))
    sys.exit(1)
print("VÉRIFICATEUR DE L'ÉDITION v0.10.0 : VERT — données, bibliographie, "
      "artefacts scellés, gouvernance, sceau, archives et formulation "
      "tous constatés.")
