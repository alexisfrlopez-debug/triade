#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_interpieces.py — LE LINTER INTER-PIÈCES (D218, l'instruction 376f15f18).

Fail-closed : toute divergence d'une valeur partagée entre les CINQ pièces du
pack REFUSE le build. Les valeurs partagées confrontées :
  — les tailles et empreintes des artefacts scellés (passeur.exe / passeur-c.dll) ;
  — les ratios (la plage RQ2 attribuée à l'ère Loupe contre M1 ; le canon M4 17,9×) ;
  — les versions croisées (manuscrit v0.19.1 ↔ spécification v0.15.1 ↔ Livre v1.2) ;
  — les QUATORZE arbres signés (D177) ;
  — le statut des outils formels (TLC / Apalache, 13 règles, 288 formes) ;
  — la visibilité du dépôt (GitHub PRIVÉ, à trancher avant soumission — D81).
Les motifs interdits : « sans compilateur ni langage de programmation »,
« 3–11× », l'attribution bras-à-bras de la plage RQ2, « 57,856 »/« 97,937 »,
« real-hardware timing remains unmeasured », « 305–318 ».

Usage :
  python3 linter_interpieces.py                 # le contrôle, exit 1 si ROUGE
  python3 linter_interpieces.py --autocontrole  # + les contrôles négatifs
                                                 # (mutation → attrapée, interdit
                                                 #  réintroduit → refusé)
"""
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
REPO = ICI.parent.parent

PIECES = {
    "manuscrit": REPO / "edition-v0191" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v151" / "final.pdf",
    "livre": REPO / "scripts" / "livre_v12" / "final.pdf",
    "preuves": ICI / "TRIADE_preuves_et_calculs_v0.19.1.pdf",
    "presentation": ICI / "TRIADE_presentation_20261120.pdf",
}


def extraire(chemin):
    txt = subprocess.run(["pdftotext", str(chemin), "-"], capture_output=True,
                         check=True).stdout.decode("utf-8", "replace")
    # normalise les tirets et les espaces (retours à la ligne du rendu compris)
    # — une valeur partagée ne doit jamais dépendre de la coupe des lignes
    import re
    return re.sub(r"\s+", " ",
                  txt.replace("\u2013", "-").replace("\u2014", "-")
                     .replace("\u2009", " ").replace("\u202f", " ")
                     .replace("\u00a0", " "))


class Verdict:
    def __init__(self):
        self.lignes = []
        self.rouges = 0

    def exige(self, piece, marqueurs, nom, tous=True):
        texte = PIECES_TXT[piece]
        if isinstance(marqueurs, str):
            marqueurs = [marqueurs]
        manquants = [m for m in marqueurs if m.replace("\u2013", "-") not in texte]
        ok = (not manquants) if tous else (len(manquants) < len(marqueurs))
        if ok:
            self.lignes.append(f"VERT   {nom} [{piece}]")
        else:
            self.rouges += 1
            self.lignes.append(f"ROUGE  {nom} [{piece}] — manquant : {manquants}")

    def interdit(self, piece, motif, nom):
        texte = PIECES_TXT[piece]
        if motif.replace("\u2013", "-") in texte:
            self.rouges += 1
            self.lignes.append(f"ROUGE  {nom} [{piece}] — le motif interdit EST PRÉSENT : « {motif} »")
        else:
            self.lignes.append(f"VERT   {nom} [{piece}] — le motif interdit est absent")


PIECES_TXT = {}


def hors_diff_annote(texte):
    """Le texte des preuves SANS la section 7 (le diff annoté) — cette section
    CITE par nature les motifs et valeurs qu'elle corrige (l'interdit vise
    l'énoncé qui affirme, jamais la pièce qui documente la correction)."""
    debut = texte.find("7. L'édition v0.19.1 : le diff annoté")
    fin = texte.find("8. Empreintes des pièces du pack")
    if debut == -1 or fin == -1 or fin <= debut:
        return texte  # structure inattendue : le texte ENTIER est confronté (fail-closed)
    return texte[:debut] + texte[fin:]


def sans_citations(texte):
    """Le texte sans les portées CITÉES entre guillemets « … » — la citation
    d'un motif interdit (à l'objet de la vérification ou de la correction)
    n'est pas l'assertion du motif. L'interdit vise l'énoncé nu."""
    import re
    return re.sub(r"«[^«»]*»", " ", texte, flags=re.S)


def controle(textes=None, verbeux=True):
    """Le contrôle lui-même. `textes` permet d'injecter des copies mutées
    (les contrôles négatifs)."""
    global PIECES_TXT
    injectes = textes is not None
    PIECES_TXT = textes if injectes else {n: extraire(p) for n, p in PIECES.items()}
    v = Verdict()

    # ---- 1. les tailles et empreintes des artefacts scellés ----
    v.exige("manuscrit", ["61,952"], "taille passeur.exe (61 952 o)")
    v.exige("manuscrit", ["4a7229e7418e8276"], "empreinte passeur.exe")
    v.exige("manuscrit", ["102,390"], "taille passeur-c.dll (102 390 o)")
    v.exige("manuscrit", ["fe4ddfc9842fb29b"], "empreinte passeur-c.dll")
    v.exige("preuves", ["4a7229e7418e8276"], "empreinte passeur.exe (la table des empreintes)")
    v.exige("preuves", ["fe4ddfc9842fb29b"], "empreinte passeur-c.dll (la table des empreintes)")
    v.exige("preuves", ["61952"], "taille passeur.exe au format verbatim (61952 o)")
    v.exige("preuves", ["102390"], "taille passeur-c.dll au format verbatim (102390 o)")
    v.exige("preuves", ["c1115105"], "loupe.exe 0.1.1 scellé (c1115105…)")
    v.interdit("manuscrit", "57,856", "l'ancienne taille v1 de passeur.exe")
    v.interdit("manuscrit", "97,937", "l'ancienne taille v1 de passeur-c.dll")
    # aux preuves : l'interdit vise le texte HORS diff annoté et HORS citations
    # (la section 7 cite les valeurs corrigées — c'est son office ; la table
    # d'empreintes, elle, exige les tailles réelles, vérifiées ci-dessus)
    base_preuves = PIECES_TXT["preuves"]
    PIECES_TXT["preuves"] = sans_citations(hors_diff_annote(base_preuves))
    v.interdit("preuves", "57,856", "l'ancienne taille v1 de passeur.exe (preuves, hors citations)")
    v.interdit("preuves", "97,937", "l'ancienne taille v1 de passeur-c.dll (preuves, hors citations)")

    # ---- 2. les ratios ----
    v.exige("manuscrit", ["2.98-11.37"], "la plage RQ2 exacte")
    v.exige("manuscrit", ["Loupe-era"], "l'attribution RQ2 : l'ère Loupe (manuscrit)")
    v.exige("manuscrit", ["M1 counterparts"], "l'attribution RQ2 : la baseline M1 (manuscrit)")
    v.exige("preuves", ["2,98-11,37"], "la plage RQ2 exacte (preuves)")
    v.exige("preuves", ["ère Loupe contre la baseline M1"], "l'attribution RQ2 (preuves)")
    v.exige("presentation", ["2,98-11,37"], "la plage RQ2 exacte (présentation)")
    v.exige("presentation", ["l'ère Loupe"], "l'attribution RQ2 : l'ère Loupe (présentation)")
    v.exige("presentation", ["baseline M1"], "l'attribution RQ2 : la baseline M1 (présentation)")
    v.interdit("manuscrit", "3-11", "la plage arrondie « 3-11× »")
    v.interdit("preuves", "3-11", "la plage arrondie « 3-11× » (preuves)")
    v.interdit("preuves", "l'écart mesuré entre les bras tient à la plage exacte 2,98",
               "l'attribution bras-à-bras de la plage RQ2 (preuves)")
    v.interdit("presentation", "2,98-11,37× le bras C",
               "l'attribution bras-à-bras de la plage RQ2 (présentation)")
    v.exige("manuscrit", ["17.9"], "le canon M4 17,9× (manuscrit)")
    v.exige("preuves", ["17,9"], "le canon M4 17,9× (preuves)")
    v.exige("presentation", ["17,9"], "le canon M4 17,9× (présentation)")
    v.exige("preuves", ["17,8"], "l'écart d'arrondi 17,8× NOMMÉ à côté de la pièce R11 verbatim (preuves)")
    v.exige("manuscrit", ["23.1"], "la base avant 23,1× (manuscrit)")

    # ---- 3. les versions croisées ----
    v.exige("manuscrit", ["v0.19.1"], "la version du manuscrit")
    v.exige("manuscrit", ["v0.15.1"], "la référence à la spécification courante")
    v.exige("specification", ["v0.15.1"], "la version de la spécification")
    v.exige("specification", ["v0.19.1", "cohérence"], "l'édition de cohérence nommée à la spec", tous=False)
    v.exige("livre", ["v1.2"], "la version du Livre")
    v.exige("livre", ["v0.15.1"], "la référence à la spécification courante (Livre)")
    v.exige("preuves", ["v0.19.1"], "la version des preuves")
    v.exige("preuves", ["v0.15.1"], "la référence à la spec courante (preuves)")
    v.exige("preuves", ["v1.2"], "la référence au Livre v1.2 (preuves)")
    v.exige("presentation", ["v0.19.1"], "la version du manuscrit (présentation)")
    v.exige("presentation", ["v0.15.1"], "la version de la spec (présentation)")
    v.exige("presentation", ["v1.2"], "la version du Livre (présentation)")

    # ---- 4. les QUATORZE arbres signés ----
    v.exige("specification", ["Quatorze arbres de couche"], "les quatorze arbres (spec §12.4)")
    v.exige("livre", ["QUATORZE arbres signés"], "les quatorze arbres (Livre ch. 4)")
    v.exige("manuscrit", ["fourteen signed"], "les quatorze arbres (manuscrit)")
    v.exige("preuves", ["QUATORZE arbres"], "les quatorze arbres (preuves, V8)")
    v.interdit("specification", "Treize arbres de couche", "le compte périmé « treize arbres » (spec)")
    v.interdit("livre", "neuf arbres", "le compte périmé « neuf arbres » (Livre)")

    # ---- 5. le statut des outils formels ----
    v.exige("manuscrit", ["TLC"], "l'outil TLC nommé (manuscrit)")
    v.exige("manuscrit", ["Apalache"], "l'outil Apalache nommé (manuscrit)")
    v.exige("preuves", ["TLC"], "l'outil TLC nommé (preuves)")
    v.exige("preuves", ["Apalache"], "l'outil Apalache nommé (preuves)")
    v.exige("preuves", ["288"], "la couverture 288 formes (preuves)")
    v.exige("presentation", ["Apalache"], "l'outil Apalache nommé (présentation)")
    v.exige("presentation", ["TLA+"], "le modèle TLA+ nommé (présentation)")
    v.exige("specification", ["Apalache"], "l'outil Apalache nommé (spec)")
    v.exige("specification", ["288 formes"], "la couverture 288 formes (spec)")

    # ---- 6. la visibilité du dépôt ----
    v.exige("presentation", ["PRIVÉ"], "la visibilité du dépôt : GitHub PRIVÉ (présentation)")
    v.exige("presentation", ["D81"], "la décision D81 citée à la ligne de visibilité")
    v.interdit("presentation", "GitHub public", "la visibilité publique avant D183")

    # ---- 7. les motifs interdits généraux ----
    for piece in PIECES:
        if piece == "preuves":
            # le diff annoté (section 7) et les citations « … » citent les motifs
            # corrigés — l'interdit s'applique au texte NU des preuves
            PIECES_TXT["preuves"] = sans_citations(hors_diff_annote(base_preuves))
            v.interdit(piece, "sans compilateur ni langage de programmation",
                       "la formulation requalifiée D182/D190 (hors citations et diff annoté)")
        else:
            v.interdit(piece, "sans compilateur ni langage de programmation",
                       "la formulation requalifiée D182/D190")
    PIECES_TXT["preuves"] = base_preuves
    v.interdit("manuscrit", "real-hardware timing remains unmeasured",
               "le timing matériel contredit par les runs signés du 13/11")
    v.interdit("manuscrit", "305-318", "la plage périmée des entrées de clôture")
    v.interdit("specification", "le douzième run attendu", "le douzième run est vécu et scellé (D181)")
    v.interdit("specification", "D75-D184", "le titre périmé de l'annexe décisionnelle")
    v.interdit("livre", "Empreintes md5 des modules", "la table d'empreintes est à sha-256 (D184/D187)")
    v.interdit("livre", "D75 à D133", "le sommaire des décisions périmé (la table va à D137)")

    if verbeux:
        for l in v.lignes:
            print(l)
    return v


def autocontrole():
    """LES CONTRÔLES NÉGATIFS — la falsification : chaque mutation d'une valeur
    partagée doit être ATTRAPÉE, chaque motif interdit réintroduit REFUSÉ."""
    base = {n: extraire(p) for n, p in PIECES.items()}
    cas = [
        ("une valeur partagée mutée (61,952 → 57,856)",
         "manuscrit", lambda t: t.replace("61,952", "57,856", 1)),
        ("le canon M4 muté (17,9 → 17,8 partout)",
         "manuscrit", lambda t: t.replace("17.9", "17.8")),
        ("l'empreinte scellée mutée (toutes occurrences)",
         "preuves", lambda t: t.replace("4a7229e7418e8276", "4a7229e7418e8277")),
        ("la version mutée (v0.15.1 → v0.13.0)",
         "manuscrit", lambda t: t.replace("v0.15.1", "v0.13.0", 1)),
        ("les quatorze arbres mutés (→ treize)",
         "specification", lambda t: t.replace("Quatorze arbres de couche", "Treize arbres de couche", 1)),
        ("un motif interdit réintroduit (« sans compilateur ni langage de programmation »)",
         "presentation", lambda t: t.replace(
             "sans aucune chaîne de traduction optimisante ni opaque",
             "sans compilateur ni langage de programmation", 1)),
        ("l'attribution RQ2 dévoyée (bras-à-bras)",
         "presentation", lambda t: t.replace(
             "se tient dans la plage 2,98-11,37× la baseline M1",
             "se tient dans la plage 2,98-11,37× le bras C", 1)),
    ]
    verts = 0
    for nom, piece, mutation in cas:
        textes = dict(base)
        textes[piece] = mutation(textes[piece])
        v = controle(textes, verbeux=False)
        if v.rouges > 0:
            print(f"AUTOCONTRÔLE VERT   {nom} → ATTRAPÉ ({v.rouges} rouge(s))")
            verts += 1
        else:
            print(f"AUTOCONTRÔLE ROUGE  {nom} → NON ATTRAPÉ — LE LINTER EST FAUX")
            return False
    # le contrôle positif : la version non mutée doit être TOUTE VERTE
    v = controle(base, verbeux=False)
    if v.rouges == 0:
        print(f"AUTOCONTRÔLE VERT   la version non mutée → TOUTE VERTE ({len(v.lignes)} assertions)")
        verts += 1
    else:
        print(f"AUTOCONTRÔLE ROUGE  la version non mutée porte {v.rouges} rouge(s) — corriger d'abord")
        return False
    print(f"AUTOCONTRÔLE : {verts}/{len(cas) + 1} VERT")
    return True


if __name__ == "__main__":
    print("LE LINTER INTER-PIÈCES (D218) — les cinq pièces confrontées, fail-closed")
    print(f"  manuscrit     : {PIECES['manuscrit']}")
    print(f"  spécification : {PIECES['specification']}")
    print(f"  livre         : {PIECES['livre']}")
    print(f"  preuves       : {PIECES['preuves']}")
    print(f"  présentation  : {PIECES['presentation']}")
    print()
    v = controle()
    print()
    print(f"BILAN : {len(v.lignes) - v.rouges}/{len(v.lignes)} assertions VERTES, "
          f"{v.rouges} ROUGE(S)")
    if v.rouges:
        print("LE BUILD EST REFUSÉ — toute divergence d'une valeur partagée refuse la livraison.")
        sys.exit(1)
    ok = True
    if "--autocontrole" in sys.argv:
        print()
        ok = autocontrole()
    if not ok:
        sys.exit(1)
    print("TOUT VERT — la livraison peut suivre.")
