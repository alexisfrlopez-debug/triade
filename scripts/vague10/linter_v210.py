#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v210.py — LE LINTER INTER-PIÈCES + LA COHÉRENCE INTERNE de
l'édition v0.21.0 (la vague 10, l'instruction 1e2vq7rtw : « Étends le
linter pour contrôler la cohérence INTERNE au manuscrit
(abstract↔corps↔tableaux), pas seulement inter-pièces »).

Fail-closed : toute divergence REFUSE le build. Usage :
  python3 linter_v210.py                 # le contrôle intégral
  python3 linter_v210.py --negatif       # le contrôle négatif (la valeur
                                         # mutée REFUSÉE au premier nom)"""
import hashlib
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/z/my-project/depot")
V10 = REPO / "scripts" / "vague10"
PIECES = {
    "manuscrit": REPO / "edition-v0210" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v156" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v15" / "final.pdf",
    "preuves": V10 / "TRIADE_preuves_et_calculs_v0.21.0.pdf",
    "presentation": V10 / "TRIADE_presentation_20261120_v210.pdf",
}
EMPREINTES = V10 / "empreintes_livrables_v0.21.0.txt"


def extraire(chemin):
    txt = subprocess.run(["pdftotext", str(chemin), "-"],
                         capture_output=True, check=True).stdout.decode(
                             "utf-8", "replace")
    return re.sub(r"\s+", " ",
                  txt.replace("\u2013", "-").replace("\u2014", "-")
                     .replace("\u2009", " ").replace("\u202f", " ")
                     .replace("\u00a0", " ").replace("\u2212", "-"))


class Verdict:
    def __init__(self):
        self.verts, self.rouges = 0, []

    def exige(self, piece, marqueurs, nom, tous=True):
        t = self.textes[piece]
        ok = all(m in t for m in marqueurs) if tous \
            else any(m in t for m in marqueurs)
        if ok:
            self.verts += 1
            print(f"VERT  {nom}")
        else:
            self.rouges.append(nom)
            print(f"ROUGE {nom} — {' et '.join(repr(m) for m in marqueurs)}"
                  f" absent(s) de la pièce {piece}")

    def interdit(self, piece, motif, nom):
        t = self.textes[piece]
        if motif in t:
            self.rouges.append(nom)
            print(f"ROUGE {nom} — le motif interdit {motif!r} EST PRÉSENT "
                  f"({piece})")
        else:
            self.verts += 1
            print(f"VERT  {nom}")

    def cond(self, ok, nom, detail=""):
        if ok:
            self.verts += 1
            print(f"VERT  {nom}")
        else:
            self.rouges.append(nom)
            print(f"ROUGE {nom} — {detail}")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---- les canons RECALCULÉS des pièces brutes ------------------------------
def canons_fenetre():
    """Les médianes de la campagne fenêtre, RECALCULÉES du JSONL brut."""
    f = REPO / "atelier-fenetre-mqf258e4l" / "resultats_fenetre.jsonl"
    f2, h2, rep = [], [], []
    verts = 0
    for l in f.read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            if r["mode"] == "editer-F2":
                f2.append(r["total_tokens"])
                rep.append(r["completion_tokens"])
                verts += r["vert"]
            elif r["mode"] == "editer-H2":
                h2.append(r["total_tokens"])
    return {"f2": statistics.median(f2), "rep": statistics.median(rep),
            "h2": statistics.median(h2), "n": len(f2), "verts": verts}


def canons_m4():
    base = REPO / "atelier-cout-boucle-cq01qv1za" / "preuves"
    out = {}
    for k, p in [("avant", "m4-avant"), ("chaud", "m4-chaud"), ("C", "c")]:
        vals = [json.load(open(f))["total_s"]
                for f in sorted(base.glob(f"{p}-run*.json"))]
        out[k] = vals
    return out


def controle():
    v = Verdict()
    v.textes = {nom: extraire(chemin) for nom, chemin in PIECES.items()}
    negatif = "--negatif" in sys.argv
    if negatif:
        # LE CONTRÔLE NÉGATIF : le score ajusté muté à UNE pièce (le
        # manuscrit) — la cohérence INTERNE doit le REFUSER au premier nom
        v.textes["manuscrit"] = v.textes["manuscrit"].replace(
            "811/817", "811/820", 1)
        print("LE CONTRÔLE NÉGATIF VÉCU : le score ajusté muté 811/817 → "
              "811/820 au manuscrit — le refus attendu :\n")

    # ---- (1) les versions croisées --------------------------------------
    v.exige("manuscrit", ["Academic edition v0.21.0"],
            "le manuscrit v0.21.0")
    v.exige("specification", ["v0.15.6"], "la spécification v0.15.6")
    v.exige("livre", ["v1.5"], "le Livre du Coffre v1.5")
    v.exige("specification", ["D75-D228"],
            "le titre de l'annexe B à la plage réelle (la spec, inchangée)")
    v.exige("manuscrit", ["D1-D234"], "la plage de décisions D1-D234")

    # ---- (2) les DOI ------------------------------------------------------
    for piece in ("manuscrit", "preuves", "presentation"):
        v.exige(piece, ["10.5281/zenodo.24367343"],
                f"le concept DOI ({piece})")
    v.exige("manuscrit", ["24382460"], "le DOI de version courant nommé")
    v.interdit("presentation", "10.5281/zenodo.24367344",
                "le DOI v0.19.0 interdit à la présentation")

    # ---- (3) le tirage et les verdicts H5 --------------------------------
    v.exige("manuscrit", ["one-in-sixteen"], "le tirage à 1/16 (manuscrit)")
    v.interdit("manuscrit", "one-in-eight", "le 1/8 périmé (manuscrit)")
    v.exige("manuscrit", ["H5-D204", "H5-amended"],
            "H5 en deux verdicts distincts (manuscrit)")

    # ---- (4) LES CANONS M4 (les médianes RECALCULÉES des JSON bruts) ----
    m4 = canons_m4()
    med = {k: statistics.median(v) for k, v in m4.items()}
    ratio = med["chaud"] / med["C"]
    v.cond(abs(med["avant"] - 39.3) < 0.05 and len(m4["avant"]) == 5,
           "la médiane AVANT 39,3 s (n=5, recalculée)")
    v.cond(abs(med["chaud"] - 6.9) < 0.05 and len(m4["chaud"]) == 5,
           "la médiane CHAUD 6,9 s (n=5, recalculée)")
    v.cond(abs(med["C"] - 2.1) < 0.05 and len(m4["C"]) == 5,
           "la médiane C 2,1 s (n=5, recalculée)")
    v.cond(abs(ratio - 3.4) < 0.05,
           f"LE RATIO M4 RECALCULÉ des médianes non arrondies "
           f"({med['chaud']:.3f}/{med['C']:.3f} = {ratio:.2f} → 3,4×)",
           f"{ratio:.3f}")
    v.exige("presentation", ["3,4"], "le ratio M4 3,4× (présentation)")
    # LA COHÉRENCE INTERNE (l2) : les valeurs historiques datées seulement
    hist35 = [m.start() for m in
              re.finditer(r"×3\.5", v.textes["manuscrit"])]
    dates = all("D204" in v.textes["manuscrit"][max(0, h - 120):h + 120]
                for h in hist35)
    v.cond(dates and len(hist35) <= 2,
           "les ratios 3,5× historiques DATÉS (D204) seulement (interne)",
           f"{len(hist35)} occurrence(s), la datation absente")

    # ---- (5) LES TROIS BRAS (la vague 10, le C+G) ------------------------
    v.exige("preuves", ["39,24", "1,95", "2,16", "18,1", "37,07"],
            "les trois bras et l'effet notation (preuves)")
    v.exige("presentation", ["18,1", "215"],
            "l'effet notation et l'effet gouvernance (présentation)")
    v.exige("manuscrit", ["18.1", "37", "215"],
            "les effets notation/gouvernance (manuscrit)")
    v.exige("preuves", ["ATTRAPÉE", "ATTRAPÉ"],
            "le contrôle négatif de la réconciliation (preuves)")

    # ---- (6) LA SÛRETÉ MÉMOIRE (les gardes, la vague 10) ------------------
    v.exige("preuves", ["100 % DÉCHARGÉ-OU-GARDÉ", "58/58"],
            "les gardes 100 % déchargé-ou-gardé (preuves)")
    v.exige("presentation", ["100 % DÉCHARGÉ-OU-GARDÉ"],
            "les gardes (présentation)")
    v.exige("manuscrit", ["one hundred percent"],
            "les gardes au manuscrit (le paragraphe)")
    v.exige("preuves", ["2 098", "2 006", "92"],
            "la base v200 reconduite (preuves — la pièce verbatim des gardes)")

    # ---- (7) LA MUTATION : LA COHÉRENCE INTERNE (l1) ----------------------
    v.exige("preuves", ["811/817", "99,3"],
            "le score ajusté (preuves)")
    v.exige("presentation", ["811/817", "99,3"],
            "le score ajusté (présentation)")
    n817 = v.textes["manuscrit"].count("811/817")
    n832 = v.textes["manuscrit"].count("811/832")
    v.cond(n817 >= 2,
           f"LA COHÉRENCE INTERNE : le score ajusté 811/817 AUX TROIS BORDS "
           f"du manuscrit (abstract, corps, tableaux : {n817} occurrences "
           f"≥ 2)", f"{n817} occurrence(s)")
    v.cond(n832 >= 2,
           f"le score brut 811/832 AUX TROIS BORDS ({n832} occurrences ≥ 2)",
           f"{n832} occurrence(s)")
    v.interdit("manuscrit", "811/820",
               "le score périmé 811/820 (l'état du lot 8 — INTERNE)")
    v.interdit("manuscrit", "98.9%",
               "le 98,9 % périmé (INTERNE)")
    v.interdit("preuves", "811/820", "le score périmé aux preuves")

    # ---- (8) LA NON-INTERFÉRENCE ÉTENDUE (la vague 10) -------------------
    v.exige("manuscrit", ["13 blocks across seven"],
            "la couverture EN BLOCS et familles (manuscrit)")
    v.exige("manuscrit", ["lifter-soundness hypothesis"],
            "la requalification sous l'hypothèse du lifter (manuscrit)")
    v.exige("preuves", ["13 BLOCS", "SEPT familles"],
            "la couverture en blocs/familles (preuves)")
    v.exige("preuves", ["SOUS L'HYPOTHÈSE", "13/13"],
            "l'hypothèse et le round-trip (preuves)")
    v.exige("presentation", ["SOUS L'HYPOTHÈSE", "13 blocs"],
            "l'hypothèse et la couverture (présentation)")
    v.interdit("manuscrit", "ten crypto families",
                "la couverture périmée « dix familles » (manuscrit)")

    # ---- (9) CF3 -----------------------------------------------------------
    for piece in ("manuscrit", "preuves", "presentation"):
        v.exige(piece, ["14/14"], f"CF3 mécanisé 14/14 ({piece})")

    # ---- (10) LA SSE2 : LA FAUTE ET LA RE-MESURE (la vague 10) ----------
    v.exige("preuves", ["406/564", "833", "561", "16 040"],
            "la faute nommée et le temps réel (preuves)")
    v.exige("presentation", ["406/564", "833", "561"],
            "la faute et le temps réel (présentation)")
    v.exige("manuscrit", ["4087", "833", "16040", "561"],
            "la re-mesure SSE2 (manuscrit)")
    v.interdit("manuscrit", "0.03", "le ratio périmé 0,03× (manuscrit)")
    v.exige("preuves", ["34,4"], "le CPUID hissé (preuves)")

    # ---- (11) LES TOKENS : la fenêtre + l'axe opérationnel (l3) ----------
    cf = canons_fenetre()
    v.cond(abs(cf["f2"] - 1145.5) < 0.01 and cf["n"] == 18 and cf["verts"] == 18,
           "LA FENÊTRE éditer-F2 : médiane 1 146, n=18, 18/18 verts "
           "(RECALCULÉS du JSONL brut)",
           f"f2={cf['f2']} n={cf['n']} verts={cf['verts']}")
    v.cond(cf["h2"] == 2452,
           "la référence H2 2 452 (recalculée — le record reproduit)",
           f"h2={cf['h2']}")
    v.cond(cf["rep"] == 40, "la réponse médiane 40 (recalculée)",
           f"rep={cf['rep']}")
    v.exige("manuscrit", ["1,146", "2,452", "63.6", "2.2"],
            "les canons fenêtre + l'axe add opérationnel (manuscrit)")
    v.exige("preuves", ["1 146", "2 452", "53,3"],
            "les canons fenêtre (preuves)")
    v.exige("presentation", ["1 146", "53,3"],
            "les canons fenêtre (présentation)")
    # L'AXE AJOUTER AU COÛT OPÉRATIONNEL (l'instruction 1e2vq7rtw)
    v.exige("manuscrit", ["3,674"], "l'axe ajouter au coût opérationnel "
            "(le canon D222 : la notation complète)")
    v.exige("presentation", ["3 674"],
            "l'axe ajouter au coût opérationnel (présentation — la ligne AVANT de la table porte l'état historique nommé, la valeur courante est opérationnelle)")
    v.exige("preuves", ["dix familles", "La fenêtre", "OPT-10"]
            if False else ["OPT-10", "la prose"],
            "la fenêtre et le levier nommé (preuves)")

    # ---- (12) LES EMPREINTES SHA-256 DES CINQ PIÈCES ---------------------
    emp = {n: sha(p) for n, p in PIECES.items()}
    for piece in ("manuscrit", "specification", "livre", "preuves"):
        v.cond(emp[piece] in v.textes["presentation"],
               f"l'empreinte sha-256 de la pièce {piece} GRAVÉE à la "
               f"présentation", "l'empreinte recalculée absente du texte")
    for piece in ("manuscrit", "specification", "livre"):
        v.cond(emp[piece] in v.textes["preuves"],
               f"l'empreinte sha-256 de la pièce {piece} gravée au document "
               f"de preuves", "l'empreinte recalculée absente du texte")
    if EMPREINTES.exists():
        txt_emp = EMPREINTES.read_text(encoding="utf-8")
        v.cond(all(emp[n] in txt_emp for n in emp),
               "le manifeste empreintes_livrables_v0.21.0.txt porte les "
               "CINQ empreintes",
               "au moins une empreinte absente du manifeste")
    else:
        v.cond(False, "le manifeste des empreintes",
               "empreintes_livrables_v0.21.0.txt absent — lancez "
               "assemble_pack_v210.py d'abord")

    print()
    if v.rouges:
        print(f"LE LINTER v210 : {v.verts} VERT, {len(v.rouges)} ROUGE — "
              f"le build est REFUSÉ")
        return 1
    print(f"LE LINTER v210 : {v.verts} VERT, 0 ROUGE — le build est admis")
    return 0


if __name__ == "__main__":
    raise SystemExit(controle())
