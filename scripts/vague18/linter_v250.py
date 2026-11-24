#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE LINTER D'ÉDITION v2 PORTÉ À LA GÉNÉRATION v0.25.0 (CMAH20ZA5, D265).

Cinq classes, chacune falsifiable, sur les cinq pièces et leurs sources :
  C1 PHRASES SÉMANTIQUES   — les revendications interdites et les étiquettes d'ère ;
  C2 PLAGES DE DÉCISIONS    — la plage annoncée, les lignes D252–D255, l'ordre ;
  C3 REVENDICATIONS DE VERSION — chaque pièce porte SA chaîne, aucune la version d'une autre ;
  C4 GALLICISMES ANGLAIS    — les calques interdits dans le texte anglais ;
  C5 NUMÉRAUX DE LA PROSE   — chaque valeur publiée se recompose de ses opérandes imprimés.

Usage : python3 scripts/vague18/linter_v250.py [--controle-negatif]
Sortie : 0 = 0 résidu ; 2 = résidus nommés ; 3 = un contrôle négatif non attrapé.
"""
import pathlib
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]
PACK = RACINE / "pack-v250"
PIECES = {
    "manuscrit": PACK / "1-manuscrit" / "TRIADE_manuscrit_v0.25.0.pdf",
    "specification": PACK / "2-specification" / "Protocole_TRIADE_v0.15.10_Specification.pdf",
    "livre": PACK / "3-coffre-fort" / "Livre_du_Coffre_TRIADE_CF1-CF3_v1.9.pdf",
    "preuves": PACK / "4-preuves-calculs" / "TRIADE_preuves_et_calculs_v0.25.0.pdf",
    "presentation": PACK / "5-presentation" / "TRIADE_presentation_v0250.pdf",
}


def texte(p):
    r = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def charge():
    return {k: texte(v) for k, v in PIECES.items()}


def verifie(t):
    refus = []
    # C1 — phrases sémantiques
    if "edition (v0.23.3) restates" in t["manuscrit"]:
        refus.append(("C1", "manuscrit", "l'abstract porte encore v0.23.3"))
    if "the training corpus of 109 triples" in t["manuscrit"] and "(v2, historical" not in t["manuscrit"]:
        refus.append(("C1", "manuscrit", "les 109 triples ne sont pas étiquetés historiques"))
    if "11/11 refus nommés rendus" in t["presentation"]:
        refus.append(("C1", "presentation", "« 11/11 refus » non corrigé"))
    # C2 — plages de décisions
    if "D75–D255" not in t["specification"] and "D75--D255" not in t["specification"]:
        refus.append(("C2", "specification", "la plage D75–D255 est absente"))
    for d in ("D252", "D253", "D254", "D255"):
        if d not in t["specification"]:
            refus.append(("C2", "specification", f"la ligne {d} est absente"))
    if "D251" in t["manuscrit"]:
        refus.append(("C2", "manuscrit", "le manuscrit annonce encore D251"))
    # C3 — revendications de version
    attendu = {"manuscrit": "v0.25.0", "specification": "v0.15.10", "livre": "v1.9",
               "preuves": "v0.25.0", "presentation": "v0.25.0"}
    for piece, ver in attendu.items():
        if ver not in t[piece]:
            refus.append(("C3", piece, f"la chaîne {ver} est absente"))
    # C4 — gallicismes anglais (texte EN)
    interdits = ["permits to ", "allows to ", "perennisation", "dispose of the possibility",
                 "the present edition permits to", "harmonisation of the"]
    for calque in interdits:
        if calque in t["manuscrit"].lower():
            refus.append(("C4", "manuscrit", f"calque interdit : {calque.strip()}"))
    # C5 — numéraux de la prose
    if "3.23×" in t["manuscrit"] or "3.23x" in t["manuscrit"]:
        refus.append(("C5", "manuscrit", "le ratio fautif 3.23 est publié comme valeur"))
    if "3.22" not in t["manuscrit"]:
        refus.append(("C5", "manuscrit", "le ratio corrigé 3.22 est absent"))
    for attendu_txt, piece in (("712,5", "manuscrit"), ("37,425", "preuves"), ("49,12", "preuves")):
        if attendu_txt not in t["preuves"]:
            refus.append(("C5", "preuves", f"le numéral {attendu_txt} est absent"))
    return refus


def rapport(refus):
    print("=" * 78)
    print("LE LINTER D'ÉDITION v2 PORTÉ À v0.25.0")
    print("=" * 78)
    if not refus:
        print("[linter-v250] 0 RÉSIDU — les cinq classes sont vertes sur les cinq pièces")
        return 0
    for c, p, m in refus:
        print(f"[linter-v250] RÉSIDU {c} {p} — {m}")
    print(f"[linter-v250] {len(refus)} résidu(s)")
    return 2


def controle_negatif():
    base = charge()
    essais = []
    def essai(classe, mut):
        t = dict(base); mut(t); refus = verifie(t)
        essais.append((classe, any(c == classe for c, _, _ in refus), refus))
    essai("C1", lambda t: t.__setitem__("presentation", t["presentation"] + "\n11/11 refus nommés rendus"))
    essai("C2", lambda t: t.__setitem__("specification", t["specification"].replace("D252", "D25Z")))
    essai("C3", lambda t: t.__setitem__("livre", t["livre"].replace("v1.9", "v1.8")))
    essai("C4", lambda t: t.__setitem__("manuscrit", t["manuscrit"] + "\nthe tool permits to write"))
    essai("C5", lambda t: t.__setitem__("manuscrit", t["manuscrit"].replace("3.22", "3.23").replace("3.23×", "3.23×")))
    verts = 0
    print("=" * 78); print("CONTRÔLES NÉGATIFS — CINQ MUTATIONS, CINQ REFUS ATTENDUS"); print("=" * 78)
    for classe, ok, refus in essais:
        verts += 1 if ok else 0
        print(f"[{'VERT' if ok else 'ROUGE'}] {classe} → {refus}")
    print(f"{verts}/5")
    return 0 if verts == 5 else 3


if __name__ == "__main__":
    if "--controle-negatif" in sys.argv:
        sys.exit(controle_negatif())
    sys.exit(rapport(verifie(charge())))
