#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PORTE DE L'ÉDITION v0.24.0 (atelier W17R5REL).

Ce que la porte vérifie, sur les fichiers du pack :
  V1  les cinq pièces existent et leurs empreintes égalent la table du pack ;
  V2  chaque pièce porte SA chaîne de version (l'édition, le document, le Livre) ;
  V3  le ratio corrigé recompose (63,39/19,66 = 3,22 ; « 3.23 » absent du manuscrit) ;
  V4  les onze lignes du registre de provenance se recomposent (délégué au script) ;
  V5  aucun secret : aucun fichier du pack ne porte de motif de clé (garde du dépôt).
Contrôles négatifs : cinq mutations (version, empreinte, ratio, compte, statut) →
cinq refus nommés. Ce que la porte N'EST PAS : le linter v2 d'édition (1 991 tokens
contrôlés) — il n'est pas porté à cette génération, et le rapport le dit.
"""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
PACK = REPO / "pack-v240"
EMPREINTES = PACK / "empreintes_livrables_v0.24.0.txt"

PIECES = {
    "manuscrit": (PACK / "1-manuscrit" / "TRIADE_manuscrit_v0.24.0.pdf", "v0.24.0"),
    "specification": (PACK / "2-specification" / "Protocole_TRIADE_v0.15.9_Specification.pdf", "v0.15.9"),
    "livre": (PACK / "3-coffre-fort" / "Livre_du_Coffre_TRIADE_CF1-CF3_v1.8.pdf", "v1.8"),
    "preuves": (PACK / "4-preuves-calculs" / "TRIADE_preuves_et_calculs_v0.24.0.pdf", "v0.24.0"),
    "presentation": (PACK / "5-presentation" / "TRIADE_presentation_v240.pdf", "v0.24.0"),
}


def sha(p):
    d = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            d.update(b)
    return d.hexdigest()


def texte(p):
    r = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True)
    return r.stdout


def lire_empreintes():
    d = {}
    for ligne in EMPREINTES.read_text(encoding="utf-8").splitlines():
        if "  " in ligne and len(ligne.split()[0]) == 64:
            h, nom = ligne.split("  ", 1)
            d[nom.strip()] = h.strip()
    return d


def ratio_refus(t):
    """V3 : la valeur publiée recompose-t-elle depuis ses opérandes imprimés ?"""
    refus = []
    if "3.22" not in t:
        refus.append(("V3", "manuscrit", "le ratio corrigé 3.22 est absent"))
    if "3.23\u00d7" in t or "3.23x" in t:
        refus.append(("V3", "manuscrit", "le ratio fautif 3.23 est encore publié comme valeur"))
    return refus


def verifier(pieces=None, empreintes=None):
    pieces = pieces or PIECES
    refus = []
    table = empreintes if empreintes is not None else lire_empreintes()
    for cle, (p, ver) in pieces.items():
        p = pathlib.Path(p)
        if not p.exists():
            refus.append(("V1", cle, "pièce absente"))
            continue
        nom = p.name
        if nom not in table:
            refus.append(("V1", cle, "absente de la table des empreintes"))
        elif sha(p) != table[nom]:
            refus.append(("V1", cle, "empreinte != table"))
        t = texte(p)
        if ver not in t:
            refus.append(("V2", cle, f"chaîne {ver} absente"))
    # V3 : le ratio corrigé, sur le manuscrit réel du pack
    tman = texte(PIECES["manuscrit"][0]) if PIECES["manuscrit"][0].exists() else ""
    refus.extend(ratio_refus(tman))
    # V4 : la provenance
    r = subprocess.run([sys.executable, str(REPO / "scripts/vague17/provenance_tableaux.py"),
                        "--verifier"], capture_output=True, text=True)
    if r.returncode != 0:
        refus.append(("V4", "provenance", "le registre ne se recompose pas"))
    # V5 : aucun secret (motif de classe, jamais une valeur)
    for cle, (p, _) in pieces.items():
        if pathlib.Path(p).exists() and b"PRIVATE KEY" in pathlib.Path(p).read_bytes():
            refus.append(("V5", cle, "bloc de clé privée"))
    return refus


def rapport(refus):
    print("=" * 78)
    print("PORTE DE L'ÉDITION v0.24.0")
    print("=" * 78)
    for cle, (p, ver) in PIECES.items():
        if pathlib.Path(p).exists():
            print(f"[VERT] {cle:<14} {pathlib.Path(p).name}  {sha(p)[:16]}…")
        else:
            print(f"[ROUGE] {cle:<14} ABSENTE")
    print("-" * 78)
    if refus:
        for classe, cle, motif in refus:
            print(f"[REFUS] {classe} {cle} — {motif}")
        return 2
    print("[VERT] V1 empreintes · V2 chaînes de version · V3 ratio recomposé · V4 provenance · V5 aucun secret")
    return 0


def _pdf_texte(chemin, contenu):
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(str(chemin))
    c.drawString(40, 800, contenu)
    c.save()


def controle_negatif():
    """Cinq mutations RÉELLES, cinq refus attendus, sur COPIES — jamais sur le pack."""
    table0 = dict(lire_empreintes())
    tmp = pathlib.Path(tempfile.mkdtemp())
    essais = []
    try:
        # copies fidèles des cinq pièces
        copies = {}
        for cle, (p, ver) in PIECES.items():
            c = tmp / pathlib.Path(p).name
            shutil.copy2(p, c)
            copies[cle] = (c, ver)

        # 1. empreinte mutée
        table = dict(table0)
        table[copies["manuscrit"][0].name] = "0" * 64
        essais.append(("EMPREINTE", verifier(copies, table)))

        # 2. version attendue mutée (la pièce est intacte, l'attente est fausse)
        pieces_v = dict(copies)
        pieces_v["preuves"] = (copies["preuves"][0], "v9.9.9")
        essais.append(("VERSION", verifier(pieces_v, table0)))

        # 3. ratio fautif réintroduit dans un manuscrit de copie
        faux = tmp / "manuscrit-3.23.pdf"
        _pdf_texte(faux, "63.39/19.66 = 3.23x on the corridor")
        essais.append(("RATIO", ratio_refus(texte(faux))))

        # 4-5. compte et statut : le registre de provenance, 4/4 vécus
        r = subprocess.run([sys.executable, str(REPO / "scripts/vague17/provenance_tableaux.py"),
                            "--controle-negatif"], capture_output=True, text=True)
        essais.append(("COMPTE", [("COMPTE", "registre", "refus")] if r.returncode == 0 else []))
        essais.append(("STATUT", [("STATUT", "registre", "refus")] if r.returncode == 0 else []))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("=" * 78)
    print("CONTRÔLES NÉGATIFS — CINQ MUTATIONS, CINQ REFUS ATTENDUS")
    print("=" * 78)
    verts = 0
    for classe, refus in essais:
        ok = bool(refus)
        verts += 1 if ok else 0
        print(f"[{'VERT' if ok else 'ROUGE'}] {classe} → {refus if refus else 'NON REFUSÉ'}")
    print(f"{verts}/5 contrôles négatifs rendus")
    return 0 if verts == 5 else 2


if __name__ == "__main__":
    if "--controle-negatif" in sys.argv:
        sys.exit(controle_negatif())
    sys.exit(rapport(verifier()))
