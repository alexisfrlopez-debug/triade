#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v200.py — LE LINTER INTER-PIÈCES de l'édition v0.20.0 (D218
reconduit, ÉTENDU à la vague 9 : les en-têtes, les DOI, les comptes, les
RATIOS RECALCULÉS depuis les pièces brutes, les probabilités, les
empreintes sha-256 des cinq pièces).

Fail-closed : toute divergence d'une valeur partagée entre les CINQ
pièces du pack v0.20.0 REFUSE le build. Usage :
  python3 linter_v200.py                 # le contrôle intégral
  python3 linter_v200.py --negatif       # le contrôle négatif (la valeur
                                         # mutée REFUSÉE au premier nom)
"""
import hashlib
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/z/my-project/depot")
V9 = REPO / "scripts" / "vague9"
PIECES = {
    "manuscrit": REPO / "edition-v0200" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v156" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v15" / "final.pdf",
    "preuves": V9 / "TRIADE_preuves_et_calculs_v0.20.0.pdf",
    "presentation": V9 / "TRIADE_presentation_20261120_v200.pdf",
}
EMPREINTES = V9 / "empreintes_livrables_v0.20.0.txt"


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


# ---- les médianes RECALCULÉES depuis les pièces brutes ----------------------
def mesurer_tokens():
    """Les médianes de la campagne vague 9, RECALCULÉES du JSONL brut
    (les DOUBLONS du journal cassé : la PREMIÈRE occurrence fait foi —
    la règle de l'extraction consignée, extraire_vague9.py)."""
    vus, bruts = set(), []
    for ligne in (REPO / "atelier-tokens-uagz3fby7" /
                  "resultats_vague9.jsonl").read_text().splitlines():
        r = json.loads(ligne)
        if r["tache"] in vus:
            continue
        vus.add(r["tache"])
        bruts.append(r)
    par_mode = {}
    for r in bruts:
        par_mode.setdefault(r["mode"], []).append(
            (r["prompt_tokens"], r["completion_tokens"]))
    out = {}
    for mode, rs in par_mode.items():
        totaux = sorted(p + c for p, c in rs)
        reps = sorted(c for _, c in rs)
        out[mode] = {"total": statistics.median(totaux),
                     "reponse": statistics.median(reps), "n": len(rs)}
    # le compte des verts lu de l'extraction consignée
    ext = json.load(open(REPO / "atelier-tokens-uagz3fby7" /
                         "extraire_vague9.json"))
    for mode, d in ext["cellules"].items():
        out[mode]["verts"] = d["verts"]
        out[mode]["mediane_consignee"] = d["total"]["mediane"]
        out[mode]["reponse_consignee"] = d["reponse"]["mediane"]
    return out


def mesurer_m4():
    """Les médianes M4 de la vague 9, RECALCULÉES des JSON bruts."""
    base = REPO / "atelier-cout-boucle-cq01qv1za" / "preuves"

    def lire(prefixe):
        vals = []
        for i in range(1, 10):
            f = base / f"{prefixe}-run{i}.json"
            if not f.exists():
                continue
            d = json.load(open(f))
            for cle in ("duree_s", "secondes", "duration_s", "total_s"):
                if cle in d:
                    vals.append(d[cle])
                    break
        return vals
    return {k: lire(p) for k, p in
            [("avant", "m4-avant"), ("froid", "m4-froid"),
             ("chaud", "m4-chaud"), ("C", "c")]}


def controle():
    v = Verdict()
    v.textes = {nom: extraire(chemin) for nom, chemin in PIECES.items()}
    negatif = "--negatif" in sys.argv
    if negatif:
        # LE CONTRÔLE NÉGATIF : la médiane localiser mutée à la présentation
        v.textes["presentation"] = v.textes["presentation"].replace(
            "1 103", "1 277", 1)
        print("LE CONTRÔLE NÉGATIF VÉCU : la médiane localiser mutée "
              "1 103 → 1 277 à la présentation — le refus attendu :\n")

    # ---- les versions croisées (les EN-TÊTES, étendu v200) ------------------
    v.exige("manuscrit", ["Academic edition v0.20.0"],
            "le manuscrit v0.20.0")
    v.exige("specification", ["v0.15.6"], "la spécification v0.15.6")
    v.exige("livre", ["v1.5"], "le Livre du Coffre v1.5")
    v.exige("presentation", ["v0.20.0"], "la présentation v0.20.0")
    v.exige("manuscrit", ["v0.15.6"], "la référence courante à la spec")
    v.exige("livre", ["v0.15.6"], "le Livre à la spec courante")
    v.exige("preuves", ["v0.20.0"], "les preuves v0.20.0")

    # ---- les DOI réconciliés -------------------------------------------------
    for piece in ("manuscrit", "preuves", "presentation"):
        v.exige(piece, ["10.5281/zenodo.24367343"],
                f"le concept DOI partout ({piece})")
    v.exige("manuscrit", ["24382460"], "le DOI de version courant nommé")
    v.interdit("presentation", "10.5281/zenodo.24367344",
               "le DOI v0.19.0 plus cité comme référence (présentation)")

    # ---- la probabilité du tirage ---------------------------------------------
    v.exige("manuscrit", ["one-in-sixteen"], "le tirage à 1/16 (manuscrit)")
    v.interdit("manuscrit", "one-in-eight", "le 1/8 périmé (manuscrit)")

    # ---- H5 : deux verdicts distincts -----------------------------------------
    v.exige("manuscrit", ["H5-D204", "H5-amended"],
            "H5 en deux verdicts distincts et datés")
    v.exige("presentation", ["H5-D204", "H5-amendée-OPT04"],
            "H5 en deux verdicts distincts (présentation)")

    # ---- les canons M4 re-mesurés à la vague 9 (RECALCULÉS des JSON) ---------
    m4 = mesurer_m4()
    med = {k: statistics.median(x) for k, x in m4.items() if x}
    v.cond(abs(med["avant"] - 39.3) < 0.05 and len(m4["avant"]) == 5,
           "M4 avant RECALCULÉE des JSON bruts (médiane 39,3, n=5)",
           f"médiane {med.get('avant')}, n={len(m4['avant'])}")
    v.cond(abs(med["chaud"] - 6.9) < 0.05 and len(m4["chaud"]) == 5,
           "M4 chaud RECALCULÉE des JSON bruts (médiane 6,9, n=5)",
           f"médiane {med.get('chaud')}, n={len(m4['chaud'])}")
    v.cond(abs(med["C"] - 2.1) < 0.05 and len(m4["C"]) == 5,
           "le bras C RECALCULÉ des JSON bruts (médiane 2,1, n=5)",
           f"médiane {med.get('C')}, n={len(m4['C'])}")
    v.cond(any(abs(x - 29.7) < 0.05 for x in m4["chaud"]),
           "l'audit 1/10 vécu au run chaud (29,7 s)")
    v.exige("preuves", ["39.3", "6.8", "6.9", "2.1"],
            "les médianes M4 (preuves, le tableau de bord)")
    v.exige("presentation", ["39,3", "3,4"],
            "les médianes M4 (présentation)")

    # ---- la sûreté mémoire au plancher (bk79jvzbm) ----------------------------
    v.exige("preuves", ["2098", "2006", "95.6", "92"],
            "la sûreté mémoire 2 006/2 098, 92 nommés (preuves)")
    v.exige("manuscrit", ["2,006", "2,098", "95.6"],
            "la sûreté mémoire (manuscrit, anglais)")
    v.exige("presentation", ["2 006", "2 098", "95,6"],
            "la sûreté mémoire (présentation)")

    # ---- la mutation : le sweep et le score ajusté vague 9 --------------------
    v.exige("preuves", ["30 scénarios", "ÉQUIVALENTS-PAR-SWEEP"],
            "la preuve par sweep (preuves)")
    v.exige("presentation", ["30 scénarios", "ÉQUIVALENTS-PAR-SWEEP"],
            "la preuve par sweep (présentation)")
    v.exige("preuves", ["811/817", "99,3"],
            "le score ajusté 811/817 = 99,3 % (preuves)")
    v.exige("presentation", ["811/817", "99,3"],
            "le score ajusté (présentation)")
    v.exige("manuscrit", ["811/817"], "le score ajusté (manuscrit)")
    v.exige("preuves", ["811/832"], "la batterie brute 811/832 (preuves)")
    v.exige("presentation", ["811/832"],
            "le brut À CÔTÉ de l'ajusté, jamais fusionné (présentation)")

    # ---- le temps constant : la non-interférence statique ---------------------
    v.exige("manuscrit", ["non-interference"],
            "la non-interférence statique (manuscrit)")
    v.exige("preuves", ["NON-INTERFÉRENCE"],
            "la non-interférence statique (preuves)")
    v.exige("presentation", ["non-interférence"],
            "la non-interférence statique (présentation)")

    # ---- CF3 mécanisé ---------------------------------------------------------
    for piece in ("manuscrit", "preuves", "presentation"):
        v.exige(piece, ["14/14"],
                f"CF3 mécanisé 14/14 obligations ({piece})")

    # ---- la boucle de vérification (bkobf06nu) --------------------------------
    v.exige("preuves", ["CERTIFICAT-DIVERGENT"],
            "les falsifications du certificat refusées nommément (preuves)")
    v.exige("presentation", ["CERTIFICAT-DIVERGENT"],
            "les falsifications refusées nommément (présentation)")
    v.exige("preuves", ["DIVERGENCE=0"],
            "le double moteur divergence 0 (preuves)")
    v.exige("presentation", ["DIVERGENCE=0"],
            "le double moteur divergence 0 (présentation)")

    # ---- les deux couloirs (0205wxg5q) -----------------------------------------
    v.exige("preuves", ["3928", "115292", "0.03"],
            "le couloir A : 3 928 contre 115 292, le ratio 0,03× (preuves)")
    v.exige("presentation", ["3 928", "115 292", "0,03", "31,2"],
            "le couloir A (présentation)")
    v.exige("manuscrit", ["0.03", "31.2"],
            "le couloir A (manuscrit, anglais)")

    # ---- les tokens (uagz3fby7) : RECALCULÉS du JSONL brut ---------------------
    toks = mesurer_tokens()
    v.cond(toks["editer-H2"]["total"] == 2452 and
           toks["editer-H2"]["verts"] == 18 and
           toks["editer-H2"]["n"] == 18,
           "éditer-H2 RECALCULÉ du JSONL brut (médiane 2 452, 18/18)",
           f"médiane {toks['editer-H2']['total']}, "
           f"{toks['editer-H2']['verts']}/{toks['editer-H2']['n']}")
    v.cond(toks["localiser-P"]["total"] == 1103 and
           toks["localiser-P"]["verts"] == 18,
           "localiser-P RECALCULÉ du JSONL brut (médiane 1 103, 18/18)",
           f"médiane {toks['localiser-P']['total']}")
    v.cond(toks["ajouter-H3"]["verts"] == 0,
           "l'ajout par hunks refusé pour la troisième fois (0/18)")
    v.cond(toks["composer-G"]["verts"] == 3,
           "composer-G à 3/18 (H4 falsifiée)")
    v.exige("preuves", ["2452", "1103", "968", "323"],
            "les médianes tokens et le compilateur d'oracle (preuves)")
    v.exige("presentation", ["2 452", "1 103", "968", "323"],
            "les médianes tokens et le compilateur (présentation)")

    # ---- LES RATIOS AU PLANCHER RECALCULÉS (h0mq0s2m6, la méthode nommée) ------
    planchers = {"editer-H2": 18, "localiser-P": 29,
                 "ajouter-H3": 1684, "composer-G": 1684}
    attendus = {"editer-H2": 136.2, "localiser-P": 38.0,
                "ajouter-H3": 4.1, "composer-G": 2.9}
    for mode, plancher in planchers.items():
        ratio = toks[mode]["total"] / plancher
        v.cond(abs(ratio - attendus[mode]) < 0.05,
               f"le ratio au plancher {mode} RECALCULÉ "
               f"({attendus[mode]:.1f}× = médiane ÷ plancher "
               f"{plancher} cl100k)",
               f"recalculé {ratio:.1f}×")
    v.exige("preuves", ["136.2", "38.0", "4.1", "2.9"],
            "les quatre ratios au plancher (preuves, le tableau)")
    v.exige("presentation", ["136,2", "38,0", "4,1", "2,9"],
            "les quatre ratios au plancher (présentation)")
    v.exige("manuscrit", ["136.2"], "les ratios au plancher (manuscrit)")

    # ---- la section distance-au-plancher du manuscrit --------------------------
    v.exige("manuscrit", ["Distance to the floor"],
            "la section « distance au plancher » (manuscrit)")

    # ---- la gouvernance vécue (reconduite) --------------------------------------
    v.exige("specification", ["D223", "VÉCUE"],
            "la cérémonie vécue (spec)")
    v.exige("livre", ["VÉCUE le 19 novembre 2026"], "le runbook VÉCU (livre)")
    v.interdit("livre", "demeure PRIVÉ", "le dépôt privé périmé (livre)")
    v.interdit("specification", "demeure PRIVÉ tant que la",
               "le dépôt privé périmé (spec)")
    v.exige("specification", ["D75-D228"],
            "le titre de l'annexe B à la plage réelle")
    v.exige("livre", ["quatorze arbres"], "quatorze arbres (livre)")
    v.exige("manuscrit", ["D1-D228"], "la plage de décisions D1-D228")

    # ---- LES EMPREINTES SHA-256 DES CINQ PIÈCES (la consigne de l'instruction) --
    emp = {n: sha(p) for n, p in
           [("manuscrit", PIECES["manuscrit"]),
            ("specification", PIECES["specification"]),
            ("livre", PIECES["livre"]),
            ("preuves", PIECES["preuves"]),
            ("presentation", PIECES["presentation"])]}
    for piece in ("manuscrit", "specification", "livre", "preuves"):
        v.cond(emp[piece] in v.textes["presentation"],
               f"l'empreinte sha-256 de la pièce {piece} GRAVÉE à la "
               f"présentation",
               "l'empreinte recalculée absente du texte")
    for piece in ("manuscrit", "specification", "livre"):
        v.cond(emp[piece] in v.textes["preuves"],
               f"l'empreinte sha-256 de la pièce {piece} gravée au document "
               f"de preuves",
               "l'empreinte recalculée absente du texte")
    if EMPREINTES.exists():
        txt_emp = EMPREINTES.read_text(encoding="utf-8")
        toutes = all(emp[n] in txt_emp for n in emp)
        v.cond(toutes,
               "le manifeste empreintes_livrables_v0.20.0.txt porte les "
               "CINQ empreintes",
               "au moins une empreinte absente du manifeste")
    else:
        v.cond(False, "le manifeste des empreintes",
               "empreintes_livrables_v0.20.0.txt absent — lancez "
               "assemble_pack_v200.py d'abord")

    print()
    if v.rouges:
        print(f"LE LINTER v200 : {v.verts} VERT, {len(v.rouges)} ROUGE — "
              f"le build est REFUSÉ")
        return 1
    print(f"LE LINTER v200 : {v.verts} VERT, 0 ROUGE — le build est admis")
    return 0


if __name__ == "__main__":
    raise SystemExit(controle())
