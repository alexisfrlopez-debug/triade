#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zips_v0194.py — les DEUX zips de dépôt Zenodo v0.19.4 (la nouvelle
version du record 10.5281/zenodo.24367344), en miroir de la structure v0.19.0
(assembler_zips_v0190.py : soumission 5 entrées + complet porté en avant).

Les tableaux sont GÉNÉRÉS des données brutes (journal_tokens.jsonl, les
preuves m4-*.json / c-run*.json) — jamais tapés ; les valeurs générées sont
CONFRONTÉES aux nombres consignés (le RAPPORT-cq01qv1za fait foi — un écart
est un REFUS)."""
import csv
import hashlib
import io
import json
import math
import pathlib
import statistics
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
ATELIER = REPO / "atelier-cout-boucle-cq01qv1za"
ATELIER_5EY7 = REPO / "atelier-cf3-5ey7gmjra"
V7 = REPO / "scripts/vague7"
PACK = V7 / "pack-v194"
OUT = REPO / "depot-zenodo-v0194"
OUT.mkdir(exist_ok=True)

OLD_SUB = zipfile.ZipFile(REPO / "TRIADE_soumission_v0.19.0.zip")
OLD_CMP = zipfile.ZipFile(REPO / "TRIADE_complet_v0.19.0.zip")


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def quartile(vals, p):
    k = (len(vals) - 1) * p
    f, c = math.floor(k), math.ceil(k)
    return vals[f] + (vals[c] - vals[f]) * (k - f)


def dist(vals):
    v = sorted(vals)
    return (statistics.median(v), quartile(v, .25), quartile(v, .75), v[0], v[-1])


# =============================================================== les vérifications
# (1) le plan gelé — sha256 recoupé au consigné
plan = (ATELIER / "PLAN-cq01qv1za-COUT.md").read_bytes()
assert sha256(plan).startswith("cb5d1943"), "le plan diverge du consigné"
# (2) les empreintes du pack — 5/5 recoupées
attendues = {}
for ligne in (PACK / "empreintes_livrables_v0.19.4.txt").read_text(encoding="utf-8").splitlines():
    parts = ligne.split()
    if len(parts) == 3 and parts[1].replace(",", "").isdigit():
        attendues[parts[0]] = (int(parts[1].replace(",", "")), parts[2])
for nom, (taille, sha) in attendues.items():
    p = next(s / nom for s in PACK.iterdir() if (s / nom).exists())
    assert sha256(p.read_bytes()) == sha and p.stat().st_size == taille, f"empreinte divergente : {nom}"
# (3) les scellés des runs M4 INTACTS
for f in sorted((ATELIER / "preuves").glob("*.json")):
    j = json.loads(f.read_text(encoding="utf-8"))
    assert j.get("scelles_intacts", True) is True, f"un scellé rompu : {f.name}"

# =============================================================== les tableaux v0.19.4
old_tableaux = OLD_SUB.read("tableaux_donnees_v0.19.0.csv").decode("utf-8")

# --- section OPT-04 : le pointeur seul (générée du journal des tokens)
entrees = [json.loads(l) for l in (ATELIER / "journal_tokens.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
A = [e for e in entrees if "-A-" in e["tache"]]
P = [e for e in entrees if "-P-" in e["tache"]]
assert len(A) == 18 and len(P) == 18, f"campaine incomplète : A={len(A)} P={len(P)}"

section = "\n\n===== opt04_le_pointeur_seul (générée du journal_tokens.jsonl — 36 appels réels, glm-4-plus, la graine 20261117, 100 % log-api) =====\n"
section += "appel,format,prompt_tokens,completion_tokens,total_tokens\n"
for e in A:
    section += f"{e['tache']},A,{e['prompt_tokens']},{e['completion_tokens']},{e['total_tokens']}\n"
for e in P:
    section += f"{e['tache']},P,{e['prompt_tokens']},{e['completion_tokens']},{e['total_tokens']}\n"
section += "\n===== opt04_les_distributions (natif lu du champ usage, jamais tapé — l'affichage .0f de l'instrument extraire_pointeur.py reconduit) =====\n"
section += "configuration,n,mediane,q1,q3,min,max\n"
for nom, sous in [("A l'actuel — total", [e["total_tokens"] for e in A]),
                  ("P pointeur seul — total", [e["total_tokens"] for e in P]),
                  ("A — réponse seule", [e["completion_tokens"] for e in A]),
                  ("P — réponse seule", [e["completion_tokens"] for e in P])]:
    m, q1, q3, lo, hi = dist(sous)
    section += f"{nom},{len(sous)},{m:.0f},{q1:.0f},{q3:.0f},{lo},{hi}\n"

# CONFRONTATION aux consignés (RAPPORT-cq01qv1za-POINTEUR.txt fait foi —
# l'affichage .0f de l'instrument, la méthode pct reprise TELLE QUELLE)
def aff(v):
    return f"{v:.0f}"
m, q1, q3, lo, hi = dist([e["total_tokens"] for e in A])
assert (aff(m), aff(q1), aff(q3), lo, hi) == ("1714", "1150", "2474", 721, 5204), (m, q1, q3, lo, hi)
m, q1, q3, lo, hi = dist([e["total_tokens"] for e in P])
assert (aff(m), aff(q1), aff(q3), lo, hi) == ("1103", "821", "1498", 610, 2840), (m, q1, q3, lo, hi)
assert aff(statistics.median([e["completion_tokens"] for e in A])) == "770"
assert aff(statistics.median([e["completion_tokens"] for e in P])) == "52"

# --- section M4 : la pile adoptée (générée des preuves m4-*.json / c-run*.json)
preuves = ATELIER / "preuves"
avant = [json.loads((preuves / f"m4-avant-run{i}.json").read_text())["total_s"] for i in range(1, 6)]
froid = [json.loads((preuves / "m4-froid-run1.json").read_text())["total_s"]]
chaud_tous = [json.loads((preuves / f"m4-chaud-run{i}.json").read_text())["total_s"] for i in range(1, 6)]
chaud_audit = [t for t in chaud_tous if t > 20]          # le CHAUD 4 porta l'audit (29,4 s)
chaud_regime = [t for t in chaud_tous if t <= 20]
audit_dedie = [json.loads((preuves / "m4-audit-run1.json").read_text())["total_s"]]
bras_c = [json.loads((preuves / f"c-run{i}.json").read_text())["total_s"] for i in range(1, 6)]
assert len(chaud_audit) == 1 and len(chaud_regime) == 4, (chaud_audit, chaud_regime)

section += "\n===== m4_la_pile_adoptee (générée des preuves m4-*.json et c-run*.json — la même liste fixe, chronomètre monotone, CE bac 2 cœurs) =====\n"
section += "configuration,run,total_s\n"
for i, t in enumerate(avant, 1):
    section += f"AVANT v180,{i},{t}\n"
section += f"FROID semis v182,1,{froid[0]}\n"
for i, t in enumerate(chaud_tous, 1):
    section += f"CHAUD v182,{i},{t}\n"
section += f"AUDIT dédié v182,1,{audit_dedie[0]}\n"
for i, t in enumerate(bras_c, 1):
    section += f"BRAS C,{i},{t}\n"
section += "\n===== m4_les_distributions (les médianes ; le CHAUD 4 exclu du régime ET NOMMÉ — il porta l'audit automatique) =====\n"
section += "configuration,n,mediane,q1,q3,min,max\n"
for nom, sous in [("AVANT (v180)", avant), ("CHAUD régime v182", chaud_regime),
                  ("CHAUD dont audit (le run 4)", chaud_audit), ("AUDIT dédié v182", audit_dedie),
                  ("BRAS C", bras_c)]:
    m, q1, q3, lo, hi = dist(sous)
    section += f"{nom},{len(sous)},{m:.1f},{q1:.1f},{q3:.1f},{lo:.1f},{hi:.1f}\n"
section += f"FROID (semis v182),1,{froid[0]:.1f},{froid[0]:.1f},{froid[0]:.1f},{froid[0]:.1f},{froid[0]:.1f}\n"

# CONFRONTATION aux consignés (RAPPORT-cq01qv1za-M4.txt fait foi)
assert f"{statistics.median(avant):.1f}" == "39.7" and f"{statistics.median(bras_c):.1f}" == "2.2"
assert f"{statistics.median(chaud_regime):.1f}" == "6.8" and f"{audit_dedie[0]:.1f}" == "39.1"
assert f"{chaud_audit[0]:.1f}" == "29.4" and f"{froid[0]:.1f}" == "6.7"

tableaux = (old_tableaux + section).encode("utf-8")

# =============================================================== les empreintes v0.19.4
manuscrit = (PACK / "1-manuscrit" / "TRIADE_manuscrit_v0.19.4.pdf").read_bytes()
old_empr = OLD_SUB.read("empreintes_livrables.txt").decode("utf-8")
sealed = [l for l in old_empr.splitlines() if "loupe.exe" in l or "proxy.exe" in l]
empreintes = "LIVRABLES v0.19.4\n\n"
empreintes += f"{sha256(manuscrit)}  TRIADE_manuscrit_v0.19.4.pdf (le manuscrit v0.19.4 — H5 tenue, le pointeur seul au RQ2)\n"
for l in sealed:
    empreintes += l + "\n"
for nom, (taille, sha) in attendues.items():
    if nom != "TRIADE_manuscrit_v0.19.4.pdf":
        empreintes += f"{sha}  {nom} ({taille} o)\n"
pack_zip = (V7 / "TRIADE_presentation_v0.19.4_20261120.zip").read_bytes()
empreintes += f"{sha256(pack_zip)}  TRIADE_presentation_v0.19.4_20261120.zip (le pack des cinq documents, relu pièce à pièce)\n"
empreintes += "\n(depôt soumission : les sha256 des cinq pièces ci-dessus ; le complet porte en outre\n"
empreintes += "les sources, les preuves et les modèles — chaque pièce gravée au zip même.)\n"
empreintes = empreintes.encode("utf-8")

# =============================================================== la soumission
readme = """TRIADE — ÉDITION ACADÉMIQUE v0.19.4 — ARCHIVE DE SOUMISSION
============================================================

Contenu (cinq fichiers) :
  1. README.txt                      — le présent guide ;
  2. TRIADE_manuscrit_v0.19.4.pdf    — le manuscrit : LE COÛT DE LA BOUCLE
     SOUS R11 (l'instruction cq01qv1za, la vague 7 quatrième — le plan
     pré-enregistré sha256 cb5d1943… gelé AVANT toute mesure) : LE POINTEUR
     SEUL adopté au localiser (OPT-04 : −35,7 % au total, −93,3 % à la
     réponse, zéro divergence 18/18, l'expansion client à quatre refus
     nommés), LA PILE MÉMO V2 + DOUBLE MOTEUR (la clé fichier + config
     émulateur + graine, le compteur chaîné au cœur signé, l'audit 1 run
     sur 10 vécu — l'identité champ à champ 0 écart ; QEMU-user au volume,
     Unicorn à l'échantillon consigné : DIVERGENCE 0 sur 2 041 opérations),
     LE RATIO 17,9× → 3,0× : H5 DEVIENT TENUE (l'énoncé explicite de
     l'instruction du maître — la falsification D204 demeurant consignée
     comme mesurée et datée), la réconciliation D214 nommée sur pièces (la
     variance inter-bac) ; le dépôt GitHub PUBLIC (D220) et le DOI vivant
     portés au statut exact ;
  3. empreintes_livrables.txt        — les sha256 de chaque pièce du dépôt,
     la pièce scellée loupe.exe 0.1.1 et le scellé proxy.exe 1.0.0 compris
     (le registre fait foi) ;
  4. rapport_verification_v0.19.4.txt — la vérification V1--V10 sur pièces
     (le linter v194 16/16 re-roulé, les empreintes du pack 5/5 recoupées,
     les tableaux GÉNÉRÉS des données brutes et confrontés aux consignés,
     la falsification prouvée, les écarts nommés) ;
  5. tableaux_donnees_v0.19.4.csv    — les données : le round-trip
     instrumenté RQ2, les tables de campagne D204/D210 (portées de la
     v0.19.0), le carnet M3 au geste, LA CAMPAGNE OPT-04 (les 36 appels
     réels du journal des tokens, les distributions natives) et LES MESURES
     M4 de la pile adoptée (les 17 runs aux preuves, les distributions par
     configuration) — chaque valeur GÉNÉRÉE des registres bruts, jamais
     tapée.

Cette version v0.19.4 succède à la v0.19.0 du même concept DOI : elle porte
l'édition courante à la date du 19/11/2026 (la vague 7 : le kit de séquestre
D219, le passage public D220, l'écart CF3 fermé D221, le coût de la boucle
D222). AUCUNE valeur mesurée des éditions scellées antérieures n'est
modifiée — la v0.19.4 est additive.

Licence : Business Source License 1.1 avec Additional Use Grant
académique (peer review, artifact evaluation, réplication scientifique,
recherche non commerciale — la décision D209 ; Change Date 2030-10-28,
conversion GPLv3).
""".encode("utf-8")

rapport = (V7 / "rapport_verification_v0.19.4.txt").read_bytes()

soumission = {
    "README.txt": readme,
    "TRIADE_manuscrit_v0.19.4.pdf": manuscrit,
    "empreintes_livrables.txt": empreintes,
    "rapport_verification_v0.19.4.txt": rapport,
    "tableaux_donnees_v0.19.4.csv": tableaux,
}
zp = OUT / "TRIADE_soumission_v0.19.4.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for n, b in soumission.items():
        z.writestr(n, b)
print(f"TRIADE_soumission_v0.19.4.zip : {zp.stat().st_size} o, sha256 {sha256(zp.read_bytes())[:16]}… — {len(soumission)} entrées")

# =============================================================== le complet
complet: dict[str, bytes] = {}
complet["LICENSE"] = OLD_CMP.read("LICENSE")
led = REPO / "scripts/campagne_d204/reception-357"
for nom in ["livraisons.csv", "defauts.csv", "carnet_temps_humain.csv"]:
    complet[f"ledgers_d204_d210/{nom}"] = (led / nom).read_bytes()
# manuscrit v0.19.4
complet["manuscrit/TRIADE_manuscrit_v0.19.4.pdf"] = manuscrit
complet["manuscrit/main.tex"] = (REPO / "edition-v0194/main.tex").read_bytes()
complet["manuscrit/refs.bib"] = (REPO / "edition-v0194/refs.bib").read_bytes()
for nom in ["macros_v190.tex", "statuts_v190.tex", "table-campagne.tex",
            "table-campagne-d210.tex", "tables_generees_v180.tex"]:
    complet[f"manuscrit/donnees/{nom}"] = (REPO / f"edition-v0194/donnees/{nom}").read_bytes()
# preuves : les scellées v180 + les v190 (portées du zip v0.19.0)
for n in OLD_CMP.namelist():
    if n.startswith("preuves_v180/") or n.startswith("preuves_v190/"):
        complet[n] = OLD_CMP.read(n)
# preuves_v193 : l'écart CF3 fermé (l'instruction 5ey7gmjra — jamais déposée avant)
for nom in ["RAPPORT-BATTERIE-5EY7GMJRA.txt", "RAPPORT-CAMPAGNE-PBT-5EY7GMJRA.txt",
            "RAPPORT-TRACES-HASH-V190.txt", "modele_invariant_rapport.txt"]:
    complet[f"preuves_v193/{nom}"] = (ATELIER_5EY7 / nom).read_bytes()
complet["preuves_v193/rapport_verification_v0.19.3.txt"] = (V7 / "rapport_verification_v0.19.3.txt").read_bytes()
# preuves_v194 : le coût de la boucle sous R11 (l'instruction cq01qv1za)
for nom in ["RAPPORT-cq01qv1za-M4.txt", "RAPPORT-cq01qv1za-POINTEUR.txt"]:
    complet[f"preuves_v194/{nom}"] = (ATELIER / nom).read_bytes()
complet["preuves_v194/controle-negatif-v2.txt"] = (ATELIER / "preuves" / "controle-negatif-v2.txt").read_bytes()
complet["preuves_v194/PLAN-cq01qv1za-COUT.md"] = plan
complet["preuves_v194/journal_tokens.jsonl"] = (ATELIER / "journal_tokens.jsonl").read_bytes()
complet["preuves_v194/memo-sessions-v2.json"] = (ATELIER / "memo-sessions-v2.json").read_bytes()
for f in sorted((ATELIER / "preuves").glob("*.json")):
    complet[f"preuves_v194/preuves/{f.name}"] = f.read_bytes()
complet["preuves_v194/empreintes_livrables_v0.19.4.txt"] = (PACK / "empreintes_livrables_v0.19.4.txt").read_bytes()
# scripts : la chaîne v180 + la chaîne v190 (portées) + la chaîne v194 née
for n in OLD_CMP.namelist():
    if n.startswith("scripts_v180/") or n.startswith("scripts_v190/") or n.startswith("tla_v150/"):
        complet[n] = OLD_CMP.read(n)
for nom in ["campagne_pointeur.py", "expansion_pointeur.py", "extraire_opt04.py",
            "extraire_pointeur.py", "memo_sessions_v2.py", "moteur_qemu.py",
            "outil_m4_v182.py", "mesure_c_v182.py", "oracle_unite01_v182.py",
            "oracle_unite02_v182.py", "linter_v194.py", "consigner_opt04.py",
            "generer_presentation_v194.py", "generer_preuves_v194.py",
            "assemble_pack_v194.py", "assembler_zips_v0194.py",
            "reconciliation_campagne_d210.py"]:
    complet[f"scripts_v194/{nom}"] = (V7 / nom).read_bytes() if (V7 / nom).exists() else (ATELIER / nom).read_bytes()
# les modules étendus CF3 (la preuve D221 au complet)
for nom in ["CF3Etendu.tla", "CF3EquivEtendu.tla", "CF3EtenduDebordant.tla",
            "CF3FideliteEtendu.tla", "CF3PlafondEtendu.tla"]:
    complet[f"tla_v153_etendu/{nom}"] = (ATELIER_5EY7 / nom).read_bytes()

zc = OUT / "TRIADE_complet_v0.19.4.zip"
with zipfile.ZipFile(zc, "w", zipfile.ZIP_DEFLATED) as z:
    for n, b in sorted(complet.items()):
        z.writestr(n, b)
print(f"TRIADE_complet_v0.19.4.zip : {zc.stat().st_size} o, sha256 {sha256(zc.read_bytes())[:16]}… — {len(complet)} entrées")

# le pack des cinq documents (le troisième fichier du dépôt)
zpk = OUT / "TRIADE_presentation_v0.19.4_20261120.zip"
zpk.write_bytes(pack_zip)
print(f"TRIADE_presentation_v0.19.4_20261120.zip : {zpk.stat().st_size} o, sha256 {sha256(pack_zip)[:16]}…")

# manifeste des empreintes du complet
with open(OUT / "empreintes_complet_v0194.txt", "w") as f:
    for n, b in sorted(complet.items()):
        f.write(f"{sha256(b)}  {n}\n")
print("empreintes_complet_v0194.txt écrit")
print("\nVERDICT : VERT — les zips v0.19.4 assemblés, chaque valeur confrontée aux consignés")
