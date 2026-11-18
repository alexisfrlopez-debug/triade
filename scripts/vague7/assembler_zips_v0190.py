#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zips_v0190.py — les DEUX zips de dépôt Zenodo v0.19.0, en miroir
de la structure v0.18.0 (soumission 5 entrées + complet ~52 entrées)."""
import hashlib
import io
import pathlib
import zipfile

REPO = pathlib.Path("/home/z/my-project/work/repo-probe/triade")
WORK = pathlib.Path("/home/z/my-project/work")
OUT = WORK / "depot-zenodo"
OUT.mkdir(exist_ok=True)

OLD_SUB = zipfile.ZipFile(WORK / "TRIADE_soumission_v0.18.0.zip")
OLD_CMP = zipfile.ZipFile(WORK / "TRIADE_complet_v0.18.0.zip")


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- la soumission
manuscrit = (REPO / "edition-v0190/TRIADE_manuscrit_v0.19.0.pdf").read_bytes()
rapport = (REPO / "scripts/vague7/rapport_verification_v0.19.0.txt").read_bytes()

readme = """TRIADE — ÉDITION ACADÉMIQUE v0.19.0 — ARCHIVE DE SOUMISSION
============================================================

Contenu (cinq fichiers) :
  1. README.txt                      — le présent guide ;
  2. TRIADE_manuscrit_v0.19.0.pdf    — le manuscrit : LA CLÔTURE DE LA
     CAMPAGNE D210 (l'édition finale du cycle) — le PDF portant la
     clôture de l'extension D210, la lecture de l'attribution empirique
     et les lignes M3 : les QUATRE unités closes aux formats identiques
     (loupe-02 VERT, loupe-08 VERT, loupe-13 VERT, loupe-16 ROUGE à la
     cap — trois échappées comptées, toutes côté kit dans le juge
     partagé, la pièce jamais fautive), l'attribution tranchée sur
     pièces (la même pièce C re-livrée via un kit standard minimal :
     14 VERT 0 ROUGE — le flux compilé pur ne l'aurait pas produite),
     les verdicts H6--H8 explicites (H6 tenue par attribution ; H7 non
     testée — le tirage public ne donna aucun contraste, l'hypothèse
     reportée ; H8 réfutée — 51 %/39 %/9 %, une unité sur quatre
     au-dessus du seuil inscrit), les métriques M2/M3/M4 telles que
     consignées (la couture de la première unité nommée ; le gap M2 de
     l'attribution jamais reconstruit ; l'écart M3 des bornes du
     carnet — les lignes reçues telles quelles) ; AUCUNE valeur mesurée
     de la v0.18.1 scellée n'est modifiée — la v0.19.0 est purement
     additive (30 pages) ;
  3. empreintes_livrables.txt        — les sha256 de chaque pièce du
     dépôt, la pièce scellée loupe.exe 0.1.1 et le scellé proxy.exe
     compris (le registre fait foi) ;
  4. rapport_verification_v0.19.0.txt — la vérification V1--V10 sur
     pièces (la compilation, le linter 35/35, la falsification prouvée
     — trois mutations, trois refus —, la réconciliation 10/10, le
     contrôle géométrique, les écarts nommés) ;
  5. tableaux_donnees_v0.19.0.csv    — les données : le round-trip
     instrumenté RQ2 (les mesures brutes, le plan pré-enregistré), la
     table de campagne D204 (22 livraisons) et la table D210 née (7
     livraisons, générée du registre), le carnet M3 au geste.

Licence : Business Source License 1.1 avec Additional Use Grant
académique (peer review, artifact evaluation, réplication scientifique,
recherche non commerciale — la décision D209 ; Change Date 2030-10-28,
conversion GPLv3+).
""".encode("utf-8")

# tableaux : le CSV v0.18.0 (les mesures RQ2) + les sections D210
old_tableaux = OLD_SUB.read("tableaux_donnees_v0.18.0.csv").decode("utf-8")
import csv
led = REPO / "scripts/campagne_d204/reception-357"
liv = [l for l in csv.DictReader(
    (x for x in open(led / "livraisons.csv", encoding="utf-8-sig") if not x.startswith("#")))]
d210 = [l for l in liv if l["tache"].endswith("-d210") or l["tache"] == "loupe-16-attr"]
carn = [c for c in csv.DictReader(
    (x for x in open(led / "carnet_temps_humain.csv", encoding="utf-8-sig") if not x.startswith("#")))]
carnet_d210 = [c for c in carn if c["geste"] == "run-terrain" and (c["tache"].endswith("-d210") or c["tache"] == "loupe-16-attr")]

section = "\n\n===== campagne_d210_les_livraisons (générée du registre reception-357) =====\n"
section += "livraison,bras,tache,numero_iteration,date_kit,date_run,verdict,recoup\n"
for l in d210:
    section += ",".join([l["livraison"], l["bras"], l["tache"], l["numero_iteration"], l["date_kit"], l["date_run"], l["verdict"], l["recoup"]]) + "\n"
section += "\n===== campagne_d210_le_carnet_m3 (au geste, la frontière D99) =====\n"
section += "date,bras,tache,geste,debut,fin,minutes,notes\n"
for c in carnet_d210:
    section += ",".join([c["date"], c["bras"], c["tache"], c["geste"], c["debut"], c["fin"], c["minutes"], c["notes"]]) + "\n"
tableaux = (old_tableaux + section).encode("utf-8")

# empreintes (la pièce scellée + le scellé proxy — repris du v0.18.0, inchangés)
old_empr = OLD_SUB.read("empreintes_livrables.txt").decode("utf-8")
old_empr_lines = old_empr.splitlines()
sealed = [l for l in old_empr_lines if "loupe.exe" in l or "proxy.exe" in l]
empreintes = "LIVRABLES v0.19.0\n\n"
empreintes += f"{sha256(manuscrit)}  TRIADE_manuscrit_v0.19.0.pdf (le manuscrit, 30 pages — la clôture D210)\n"
for l in sealed:
    empreintes += l + "\n"
empreintes += "\n(depôt soumission : les sha256 des cinq pièces ci-dessus ; le complet porte en outre\n"
empreintes += "les sources, les preuves et les modèles — chaque pièce gravée au zip même.)\n"
empreintes = empreintes.encode("utf-8")

soumission = {
    "README.txt": readme,
    "TRIADE_manuscrit_v0.19.0.pdf": manuscrit,
    "empreintes_livrables.txt": empreintes,
    "rapport_verification_v0.19.0.txt": rapport,
    "tableaux_donnees_v0.19.0.csv": tableaux,
}
zp = OUT / "TRIADE_soumission_v0.19.0.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for n, b in soumission.items():
        z.writestr(n, b)
print(f"TRIADE_soumission_v0.19.0.zip: {zp.stat().st_size} o, sha256 {sha256(zp.read_bytes())[:16]}… — {len(soumission)} entrées")

# ---------------------------------------------------------------- le complet
complet: dict[str, bytes] = {}
complet["LICENSE"] = OLD_CMP.read("LICENSE")
# ledgers (l'état 357 : le livre 29 lignes, les défauts 11, le carnet 5 lignes D210)
for nom in ["livraisons.csv", "defauts.csv", "carnet_temps_humain.csv"]:
    complet[f"ledgers_d204_d210/{nom}"] = (led / nom).read_bytes()
# manuscrit
complet["manuscrit/TRIADE_manuscrit_v0.19.0.pdf"] = manuscrit
complet["manuscrit/main.tex"] = (REPO / "edition-v0190/main.tex").read_bytes()
complet["manuscrit/refs.bib"] = (REPO / "edition-v0190/refs.bib").read_bytes()
for nom in ["macros_v190.tex", "statuts_v190.tex", "table-campagne.tex",
            "table-campagne-d210.tex", "tables_generees_v180.tex"]:
    complet[f"manuscrit/donnees/{nom}"] = (REPO / f"edition-v0190/donnees/{nom}").read_bytes()
# preuves : les preuves scellées v180 (inchangées) + les preuves v190 nées
for n in OLD_CMP.namelist():
    if n.startswith("preuves_v180/"):
        complet[n] = OLD_CMP.read(n)
complet["preuves_v190/diff-annote-v190.txt"] = (REPO / "scripts/vague7/diff-annote-v190.txt").read_bytes()
complet["preuves_v190/p3-table-campagne-d210.csv"] = tableaux.split(b"===== campagne_d210_les_livraisons")[1].split(b"===== campagne_d210_le_carnet")[0].strip(b"\n") + b"\n"
complet["preuves_v190/rapport-reception-357.txt"] = (WORK / "RAPPORT-RECEPTION-CARNET-M3-D210-357-20261119.txt").read_bytes()
complet["preuves_v190/rapport-reception-355.txt"] = (WORK / "RAPPORT-355.txt").read_bytes()
# scripts : la chaîne v180 (les sources des preuves scellées) + la chaîne v190 née
for n in OLD_CMP.namelist():
    if n.startswith("scripts_v180/"):
        complet[n] = OLD_CMP.read(n)
for nom in ["reconciliation_campagne_d210.py", "linter_v190.py",
            "controle_geometrique_v190.py", "regenerer_macros_v190.py"]:
    complet[f"scripts_v190/{nom}"] = (REPO / f"scripts/vague7/{nom}").read_bytes()
complet["scripts_v190/diff-main-v181-v190.patch"] = (REPO / "scripts/vague7/diff-main-v181-v190.patch").read_bytes()
# tla inchangé
for n in OLD_CMP.namelist():
    if n.startswith("tla_v150/"):
        complet[n] = OLD_CMP.read(n)

zc = OUT / "TRIADE_complet_v0.19.0.zip"
with zipfile.ZipFile(zc, "w", zipfile.ZIP_DEFLATED) as z:
    for n, b in sorted(complet.items()):
        z.writestr(n, b)
print(f"TRIADE_complet_v0.19.0.zip: {zc.stat().st_size} o, sha256 {sha256(zc.read_bytes())[:16]}… — {len(complet)} entrées")

# manifeste des empreintes du complet
with open(OUT / "empreintes_complet_v0190.txt", "w") as f:
    for n, b in sorted(complet.items()):
        f.write(f"{sha256(b)}  {n}\n")
print("empreintes_complet_v0190.txt écrit")
