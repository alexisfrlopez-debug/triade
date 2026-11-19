#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zips_v0195.py — les DEUX zips de dépôt Zenodo v0.19.5 (la
nouvelle version du concept 10.5281/zenodo.24367343), en miroir de la
structure v0.19.4 (soumission 5 entrées + complet porté en avant).

Les tableaux sont GÉNÉRÉS des données brutes de l'atelier 1c4sokpii et
du registre — jamais tapés ; les valeurs générées sont CONFRONTÉES aux
nombres consignés (le RAPPORT-1C4SOKPII fait foi — un écart est un
REFUS)."""
import csv
import hashlib
import io
import pathlib
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V7 = REPO / "scripts" / "vague7"
PACK = V7 / "pack-v195"
ATELIER = REPO / "atelier-plan-final-1c4sokpii"
REPL = REPO / "scripts" / "replication_v150"
LED = REPO / "scripts/campagne_d204/reception-357"
OUT = REPO / "depot-zenodo-v0195"
OUT.mkdir(exist_ok=True)

OLD_SUB = zipfile.ZipFile(REPO / "TRIADE_soumission_v0.19.4.zip")
OLD_CMP = zipfile.ZipFile(REPO / "TRIADE_complet_v0.19.4.zip")


def sha256_file(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def lignes_csv(p):
    with open(p, encoding="utf-8-sig") as f:
        return [l for l in csv.DictReader(
            (x for x in f if not x.startswith("#")))]


# =============================================================== les vérifications
# (1) les empreintes du pack — 5/5 recoupées
attendues = {}
for ligne in (PACK / "empreintes_livrables_v0.19.5.txt").read_text(
        encoding="utf-8").splitlines():
    parts = ligne.split()
    if len(parts) == 3 and parts[1].replace(",", "").isdigit():
        attendues[parts[0]] = (int(parts[1].replace(",", "")), parts[2])
assert len(attendues) == 5, "le pack ne porte pas ses cinq pièces"
for nom, (taille, sha) in attendues.items():
    p = next(s / nom for s in PACK.iterdir() if (s / nom).exists())
    assert sha256_file(p) == sha and p.stat().st_size == taille, \
        f"empreinte divergente : {nom}"
print("[V] les empreintes du pack v0.19.5 : 5/5 recoupées")

# (2) la batterie — les valeurs générées contre les consignées
batt = lignes_csv(ATELIER / "rejeu_fautes.csv")
glob = next(r for r in batt if r["domaine"] == "global")
assert (int(glob["tues"]), int(glob["total"])) == (811, 832), "tues/total"
assert float(glob["taux"]) == 97.5, "taux"
assert int(glob["vivants"]) == 21, "vivants"
print("[V] la batterie : 811/832 (97,5 %), le reste de 21 — générés == consignés")

# (3) le triage — 56 survivants triés, chacun sa classe
tri = lignes_csv(ATELIER / "triage_survivants.csv")
assert len(tri) == 56, f"le triage porte {len(tri)} lignes (attendu 56)"
classes = {r["classe"] for r in tri}
print(f"[V] le triage : {len(tri)} survivants triés, classes {sorted(classes)}")

# (4) le reste nommé — 21, chacun sa cause
reste = lignes_csv(ATELIER / "reste_nomme.csv")
assert len(reste) == 21, f"le reste porte {len(reste)} lignes (attendu 21)"

# (5) le registre — N = 7 unités aux deux bras, recompté
liv = lignes_csv(LED / "livraisons.csv")
unites = {}
for r in liv:
    u, bras = r.get("unite") or r.get("tache"), r.get("bras")
    unites.setdefault(u, set()).add(bras)
deux_bras = sorted(u for u, b in unites.items() if len(b) >= 2)
assert len(deux_bras) == 7, f"N = {len(deux_bras)} (attendu 7) : {deux_bras}"
print(f"[V] le registre : N = {len(deux_bras)} unités aux deux bras — {deux_bras}")

# (6) le plan D210 pré-enregistré — jamais re-tiré
plan_sha = sha256_file(REPO / "scripts/campagne_d204/PLAN-D210.md") \
    if (REPO / "scripts/campagne_d204/PLAN-D210.md").is_file() else None
print(f"[i] le plan D210 pré-enregistré : sha256 {str(plan_sha)[:16]}… "
      "(jamais re-tiré — la graine 20261111 consignée)")

# =============================================================== les tableaux
def section(titre, chemin):
    return (f"===== {titre} =====\n" + chemin.read_text(encoding="utf-8-sig")
            .rstrip() + "\n\n")


tableaux = (
    "LES DONNÉES DE L'ÉDITION v0.19.5 (la clôture de la vague 7 — "
    "l'instruction 1c4sokpii)\n"
    "chaque valeur GÉNÉRÉE des registres bruts, jamais tapée ; les valeurs\n"
    "confrontées aux consignés (le RAPPORT-1C4SOKPII fait foi)\n\n"
    + section("batterie_injection_k4 (le rejeu aux mêmes tirages — le global "
              "et par domaine)", ATELIER / "rejeu_fautes.csv")
    + section("triage_56_survivants (chacun noté au niveau instruction)",
              ATELIER / "triage_survivants.csv")
    + section("reste_21_nomme (chacun sa cause, treize familles)",
              ATELIER / "reste_nomme.csv")
    + section("registre_livraisons (le comptage N = 7 lu du registre)",
              LED / "livraisons.csv")
    + section("grille_tx (les définitions opérationnelles D189/D203)",
              REPL / "grille_tx.csv")
    + section("codage_annotateur_1 (les 11 défauts codés F/L, sur pièces)",
              REPL / "codage_annotateur1.csv"))
(OUT / "tableaux_donnees_v0.19.5.csv").write_text(tableaux, encoding="utf-8")
print(f"[V] tableaux_donnees_v0.19.5.csv "
      f"[{len(tableaux.encode()):,} o] — six sections générées")

# =============================================================== l'empreinte
emp = ["LIVRABLES v0.19.5", ""]
emp.append(f"{sha256_file(REPO / 'edition-v0195/main.pdf')}  "
           "TRIADE_manuscrit_v0.19.5.pdf (le manuscrit v0.19.5 — la clôture "
           "de la vague 7, la gouvernance portée à l'état vécu)")
emp.append("c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1  "
           "loupe.exe 0.1.1 (la pièce scellée)")
emp.append("446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d  "
           "proxy.exe 1.0.0 (le scellé M9)")
emp.append(f"{attendues['Protocole_TRIADE_v0.15.4_Specification.pdf'][1]}  "
           "Protocole_TRIADE_v0.15.4_Specification.pdf (963257 o)")
emp.append(f"{attendues['Livre_du_Coffre_TRIADE_CF1-CF3_v1.3.pdf'][1]}  "
           "Livre_du_Coffre_TRIADE_CF1-CF3_v1.3.pdf (930968 o)")
emp.append(f"{attendues['TRIADE_preuves_et_calculs_v0.19.5.pdf'][1]}  "
           "TRIADE_preuves_et_calculs_v0.19.5.pdf (107425 o)")
emp.append(f"{attendues['TRIADE_presentation_20261120_v195.pdf'][1]}  "
           "TRIADE_presentation_20261120_v195.pdf (80377 o)")
emp.append(f"{sha256_file(V7 / 'TRIADE_presentation_v0.19.5_20261120.zip')}  "
           "TRIADE_presentation_v0.19.5_20261120.zip (le pack des cinq "
           "documents, relu pièce à pièce)")
emp.append("")
emp.append("(dépôt soumission : les sha256 des cinq pièces ci-dessus ; le "
           "complet porte en outre\nles sources, les preuves et les modèles "
           "— chaque pièce gravée au zip même.)")
(OUT / "empreintes_livrables.txt").write_text("\n".join(emp) + "\n",
                                              encoding="utf-8")
print("[V] empreintes_livrables.txt gravé")

# =============================================================== le README
readme = """TRIADE — ÉDITION ACADÉMIQUE v0.19.5 — ARCHIVE DE SOUMISSION
============================================================

Contenu (cinq fichiers) :
  1. README.txt                      — le présent guide ;
  2. TRIADE_manuscrit_v0.19.5.pdf    — le manuscrit : LA CLÔTURE DE LA VAGUE
     7 (l'instruction 1c4sokpii, la vague 7 cinquième et dernière) : LE
     CRITÈRE D'ÉCHANTILLON du plan D210 clos à N = 7 SANS NOUVEAU TIRAGE
     (sept unités aux deux bras lues du registre, l'amendement conditionnel
     jamais déclenché), LA BATTERIE D'INJECTION DE FAUTES (811/832 tués,
     97,5 % — 83,4 % → 93,3 % → 97,5 %, le reste de 21 nommé à treize
     familles de causes, AUCUN tueur affaibli : la console v0.14.0
     reproduite d'abord), L'INDÉPENDANCE INTER-FAMILLES au GAP NOMMÉ
     (jamais simulée : la confrontation math↔plan tenue, le local 1,5B
     récite 0/64 et copie à la correction, le bras C généré à 1984/2011),
     LE PAQUET D'ÉVALUATION (la reproduction en une commande, la grille
     codée, le protocole du second annotateur pré-enregistré κ ≥ 0,61, le
     calculateur autotesté 3/3) — ET LE STATUT DE GOUVERNANCE PORTÉ À
     L'ÉTAT VÉCU : la cérémonie D183 vécue le 19/11 (l'Entrée 365), la
     phrase commise tournée et l'ancienne refusée, le re-scan de tout
     l'historique trié (dix constats, aucun jeton réel commis), le dépôt
     GitHub PUBLIC (D220) et le DOI vivant portés au statut exact — les
     lignes « prepared and waiting » de la v0.19.4 étaient devenues
     stales à son scellage même, la présente les porte à l'état exact ;
  3. empreintes_livrables.txt        — les sha256 de chaque pièce du dépôt,
     la pièce scellée loupe.exe 0.1.1 et le scellé proxy.exe 1.0.0 compris
     (le registre fait foi) ;
  4. rapport_verification_v0.19.5.txt — la vérification V1--V10 sur pièces
     (le linter v195 29/29 re-roulé, les empreintes du pack 5/5 recoupées,
     les tableaux GÉNÉRÉS des données brutes et confrontés aux consignés,
     la gouvernance à l'état vécu, les écarts nommés) ;
  5. tableaux_donnees_v0.19.5.csv    — les données de la session : la
     batterie d'injection K4 (le global 811/832 et par domaine), le triage
     des 56 survivants au niveau instruction, le reste de 21 nommé à ses
     causes, le registre des livraisons (le comptage N = 7), la grille et
     le codage de l'annotateur 1 — chaque valeur GÉNÉRÉE des registres
     bruts, jamais tapée.

Cette version v0.19.5 succède à la v0.19.4 du même concept DOI : elle porte
l'édition courante à la date du 20/11/2026 (la vague 7 close — les cinq
instructions exécutées). AUCUNE valeur mesurée des éditions scellées
antérieures n'est modifiée — la v0.19.5 est additive.

Licence : Business Source License 1.1 avec Additional Use Grant
académique (peer review, artifact evaluation, réplication scientifique,
recherche non commerciale — la décision D209 ; Change Date 2030-10-28,
conversion GPLv3).
"""
(OUT / "README.txt").write_text(readme, encoding="utf-8")

# =============================================================== la soumission
SOUMISSION = OUT / "TRIADE_soumission_v0.19.5.zip"
with zipfile.ZipFile(SOUMISSION, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(OUT / "README.txt", "README.txt")
    z.write(REPO / "edition-v0195" / "main.pdf",
            "TRIADE_manuscrit_v0.19.5.pdf")
    z.write(OUT / "empreintes_livrables.txt", "empreintes_livrables.txt")
    z.write(V7 / "rapport_verification_v0.19.5.txt",
            "rapport_verification_v0.19.5.txt")
    z.write(OUT / "tableaux_donnees_v0.19.5.csv",
            "tableaux_donnees_v0.19.5.csv")
print(f"[V] {SOUMISSION.name} [{SOUMISSION.stat().st_size:,} o, "
      f"{len(zipfile.ZipFile(SOUMISSION).namelist())} fichiers]")

# =============================================================== le complet
COMPLET = OUT / "TRIADE_complet_v0.19.5.zip"
with zipfile.ZipFile(COMPLET, "w", zipfile.ZIP_DEFLATED) as z:
    # (1) les chaînes du complet v0.19.4 portées en avant, le manuscrit
    # remplacé par l'édition courante v0.19.5
    for info in OLD_CMP.infolist():
        nom = info.filename
        if nom.startswith("manuscrit/"):
            continue  # remplacé par l'édition v0.19.5
        z.writestr(nom, OLD_CMP.read(nom))
    # (2) le manuscrit v0.19.5 (PDF + tex + données)
    z.write(REPO / "edition-v0195" / "main.pdf",
            "manuscrit/TRIADE_manuscrit_v0.19.5.pdf")
    z.write(REPO / "edition-v0195" / "main.tex", "manuscrit/main.tex")
    z.write(REPO / "edition-v0195" / "refs.bib", "manuscrit/refs.bib")
    for d in sorted((REPO / "edition-v0195" / "donnees").iterdir()):
        z.write(d, f"manuscrit/donnees/{d.name}")
    # (3) les preuves v0.19.5 nées : le PDF et les trois rapports verbatim
    z.write(V7 / "TRIADE_preuves_et_calculs_v0.19.5.pdf",
            "preuves_v195/TRIADE_preuves_et_calculs_v0.19.5.pdf")
    for src, dst in [("RAPPORT-1C4SOKPII.txt", "RAPPORT-1C4SOKPII.txt"),
                     ("RAPPORT-INDEPENDANCE-FAMILLES.txt",
                      "RAPPORT-INDEPENDANCE-FAMILLES.txt"),
                     ("rejeu_fautes_rapport.txt",
                      "RAPPORT-REJEU-FAUTES-1C4SOKPII.txt")]:
        z.write(ATELIER / src, f"preuves_v195/{dst}")
    # (4) l'atelier 1c4sokpii : les données et l'épreuve de reproduction
    for f in sorted(ATELIER.iterdir()):
        if f.is_file() and f.suffix in (".csv", ".py", ".sh", ".txt", ".c",
                                        ".json"):
            z.write(f, f"atelier_1c4sokpii/{f.name}")
    # (5) les scripts v195 nés (les instruments de l'édition)
    for f in sorted(V7.glob("*v195*")):
        if f.is_file():
            z.write(f, f"scripts_v195/{f.name}")
    z.write(V7 / "rapport_verification_v0.19.5.txt",
            "scripts_v195/rapport_verification_v0.19.5.txt")

noms = zipfile.ZipFile(COMPLET).namelist()
assert len(noms) >= 113, f"le complet ne porte que {len(noms)} entrées"
print(f"[V] {COMPLET.name} [{COMPLET.stat().st_size:,} o, "
      f"{len(noms)} fichiers]")

# =============================================================== la relecture
for Z in (SOUMISSION, COMPLET):
    with zipfile.ZipFile(Z) as z:
        for n in z.namelist():
            assert z.read(n), f"entrée vide : {n}"
print("[V] les DEUX zips relus : chaque entrée non vide")
print("LES DEUX ZIPS v0.19.5 ASSEMBLÉS — les vérifications vertes, "
      "les valeurs générées == les consignées.")
