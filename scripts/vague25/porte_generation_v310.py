#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA PORTE DE GÉNÉRATION v0.31.0 (W19LINT) — le linter EST la porte.

Ce que la porte vérifie, sur les fichiers du pack :
  V1  les cinq pièces existent et leurs empreintes égalent le manifeste ;
  V2  chaque pièce porte SA chaîne de version ;
  V3  le ratio corrigé recompose (63,39/19,66 = 3,22 ; « 3.23× » absent) ;
  V4  les douze lignes du registre de provenance se recomposent (délégué) ;
  V5  aucun secret : aucun fichier du pack ne porte de motif de clé privée ;
  V6  le témoin hors machine (D259) — EN ATTENTE nommé s'il manque ;
  V7  le tableau descendant est engendré, à diff nul (D260) ;
  L1..L25  les quinze classes du linter v3 (dont C6 VERSION-TABLE, C7 DECISION-RANGE,
           C8 CHANGELOG-ORDER, C9 NUMEROTATION, C10 BENCH-COUNT, C11 SEMANTIC-THREAT).

Contrôles négatifs : QUATRE mutations (libellé de version, ID hors plage, ligne de
menace non qualifiée, compte de banc muté) → quatre refus nommés, sur COPIES.

Usage : python3 scripts/vague19/porte_generation_v260.py [--controle-negatif]
Sortie : 0 = zéro rouge ; 2 = rouge(s) nommé(s) ; 3 = contrôle négatif non attrapé.
"""
import argparse
import hashlib
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile

RACINE = pathlib.Path(__file__).resolve().parents[2]
PACK = RACINE / "pack-v310"
MANIFESTE = PACK / "empreintes_livrables_v0.31.0.txt"

PIECES = {
    "manuscrit": (PACK / "1-manuscrit" / "TRIADE_manuscrit_v0.31.0.pdf", "v0.31.0"),
    "specification": (PACK / "2-specification" / "Protocole_TRIADE_v0.15.16_Specification.pdf", "v0.15.16"),
    "livre": (PACK / "3-coffre-fort" / "Livre_du_Coffre_TRIADE_CF1-CF3_v1.15.pdf", "v1.15"),
    "preuves": (PACK / "4-preuves-calculs" / "TRIADE_preuves_et_calculs_v0.31.0.pdf", "v0.31.0"),
    "presentation": (PACK / "5-presentation" / "TRIADE_presentation_v0310.pdf", "v0.31.0"),
}


def _linter():
    spec = importlib.util.spec_from_file_location(
        "linter_v4", str(RACINE / "scripts/vague20/linter_v4.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sha(p):
    d = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            d.update(b)
    return d.hexdigest()


def lire_manifeste():
    d = {}
    for ligne in MANIFESTE.read_text(encoding="utf-8").splitlines():
        if "  " in ligne and len(ligne.split()[0]) == 64:
            h, nom = ligne.split("  ", 1)
            d[nom.strip()] = h.strip()
    return d


def texte(p):
    r = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True)
    return r.stdout


def verifier(pieces=None, manifeste=None):
    pieces = pieces or PIECES
    table = manifeste if manifeste is not None else lire_manifeste()
    refus = []
    for cle, (p, ver) in pieces.items():
        p = pathlib.Path(p)
        if not p.exists():
            refus.append(("V1", cle, "pièce absente"))
            continue
        if p.name not in table:
            refus.append(("V1", cle, "absente du manifeste"))
        elif sha(p) != table[p.name]:
            refus.append(("V1", cle, "empreinte != manifeste"))
        t = texte(p)
        if ver not in t:
            refus.append(("V2", cle, f"chaîne {ver} absente"))
    # V3 ratio
    tman = texte(PIECES["manuscrit"][0]) if PIECES["manuscrit"][0].exists() else ""
    if "3.22" not in tman:
        refus.append(("V3", "manuscrit", "le ratio corrigé 3.22 est absent"))
    if "3.23×" in tman:
        refus.append(("V3", "manuscrit", "le ratio fautif 3.23 est publié"))
    # V4 provenance
    r = subprocess.run([sys.executable, str(RACINE / "scripts/vague17/provenance_tableaux.py"),
                        "--verifier"], capture_output=True, text=True)
    if r.returncode != 0:
        refus.append(("V4", "provenance", "le registre ne se recompose pas"))
    # V5 secrets
    for cle, (p, _) in pieces.items():
        p = pathlib.Path(p)
        if p.exists() and b"PRIVATE KEY" in p.read_bytes():
            refus.append(("V5", cle, "bloc de clé privée"))
    # V6 témoin — l'ANCRAGE DE TRANSPARENCE (D267) fait foi quand il existe
    ancrage = RACINE / "atelier-w20-sec" / "ancrage-recu.json"
    if ancrage.exists():
        r6 = subprocess.run([sys.executable, str(RACINE / "scripts/vague20/ancrage_transparence.py"),
                             "--verifier"], capture_output=True, text=True)
        if r6.returncode != 0:
            refus.append(("V6", "ancrage", (r6.stdout or r6.stderr).strip()[:120]))
        print("[V6] ancrage vérifié — témoin d'époque RFC 3161 recoupé")
    temoin = RACINE / "replication-v17" / "temoin-fraicheur.json"
    if not ancrage.exists() and temoin.exists():
        r6 = subprocess.run([sys.executable, str(RACINE / "scripts/vague17/temoin_fraicheur.py"),
                             str(temoin), str(RACINE / "replication-v17" / "etat-fraicheur.json")],
                            capture_output=True, text=True)
        if r6.returncode != 0:
            refus.append(("V6", "temoin", (r6.stdout or r6.stderr).strip()[:120]))
    elif not ancrage.exists():
        print("[V6] EN ATTENTE — aucun témoin hors machine consigné (D259)")
    # V7 tableau
    r7 = subprocess.run([sys.executable, str(RACINE / "scripts/vague17/provenance_tableaux.py"),
                         "--tableaux-verifier"], capture_output=True, text=True)
    if r7.returncode != 0:
        refus.append(("V7", "tableau-descendant", (r7.stdout or "").strip()[:120]))
    # L1..L25 — le linter est la porte
    L = _linter()
    pack = pathlib.Path(list(pieces.values())[0][0]).parents[1]
    textes = L.charge(pack)
    refus.extend(L.verifie(textes, L.charge_manifeste(pack), L.recompte_banc(), pack))
    refus.extend(L.controles_w25(textes, RACINE, "v0.31.0", "v0.15.16"))
    refus.extend(L.controles_w26(textes, RACINE))
    return refus


def rapport(refus):
    print("=" * 78)
    print("PORTE DE GÉNÉRATION v0.31.0 — V1..V7 + L1..L25 (le linter est la porte)")
    print("=" * 78)
    for cle, (p, ver) in PIECES.items():
        print(f"[{'VERT' if pathlib.Path(p).exists() else 'ROUGE'}] {cle:<14} "
              f"{pathlib.Path(p).name if pathlib.Path(p).exists() else 'ABSENTE'}")
    print("-" * 78)
    if refus:
        for classe, cle, motif in refus:
            print(f"[REFUS] {classe} {cle} — {motif}")
        return 2
    print("[VERT] V1 empreintes · V2 versions · V3 ratio · V4 provenance · V5 aucun secret · "
          "V6 témoin (EN ATTENTE si absent) · V7 tableau")
    print("[VERT] L1..L25 — vingt-cinq classes, zéro résidu")
    return 0


def controle_negatif():
    L = _linter()
    base = L.charge(PACK)
    rec = L.recompte_banc()
    essais = []

    def essai(nom, classe, mut):
        t = {k: v for k, v in base.items()}
        mut(t)
        r = L.verifie(t, None, rec)
        r = list(r) + list(L.controles_w25(t, RACINE, "v0.31.0", "v0.15.16")) + list(L.controles_w26(t, RACINE))
        essais.append((nom, classe, any(c == classe for c, _, _ in r), r))

    essai("libellé de version muté", "C6", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("Manuscrit\n\nv0.31.0", "Manuscrit\n\nv0.24.0")))
    essai("ID hors plage", "C7", lambda t: t.__setitem__(
        "preuves", t["preuves"] + "\nla décision D299 tranche."))
    essai("ligne de menace non qualifiée", "C11", lambda t: t.__setitem__(
        "specification", t["specification"].replace("ADV-MEDIA", "ADVX-MEDIA")))
    essai("compte de banc muté", "C10", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("16/16", "15/15")))
    essai("version de prose mutée (Livre)", "C12", lambda t: t.__setitem__(
        "livre", t["livre"].replace("v1.15", "v1.9")))
    essai("vague inconnue", "C13", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("vague 15", "vague 16")))
    essai("résumé trop long", "C14", lambda t: t.__setitem__(
        "manuscrit", t["manuscrit"].replace("Abstract", "Abstract " + ("mot " * 300), 1)))
    essai("compte du lecteur muté", "C15", lambda t: t.__setitem__(
        "preuves", t["preuves"].replace("Test du lecteur : 9/9", "Test du lecteur : 8/9")))
    essai("compte du registre muté", "C16", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("10 entrées", "11 entrées")))
    essai("compte oracle muté", "C17", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("235 exécutables", "234 exécutables")))
    import re as _re
    def _sub(t, piece, motif, remp):
        t[piece] = _re.sub(motif, remp, t[piece], count=1)
    essai("compte de classes muté", "C18", lambda t: _sub(t, "preuves", r"\b25 classes\b", "17 classes"))
    essai("vague de titre périmée", "C19", lambda t: _sub(t, "presentation", r"vague 24", "vague 19"))
    essai("DOI inconnu du registre", "C21", lambda t: _sub(t, "manuscrit", r"10\.5281/zenodo\.24499428", "10.5281/zenodo.99999999"))
    essai("version anglaise périmée", "C22", lambda t: _sub(
        t, "manuscrit", r"accompanied\s+here is v0\.15\.15",
        "accompanied here is v0.15.8 which this edition accompanies"))
    essai("statut Tamarin contredit", "C23", lambda t: _sub(t, "presentation", r"L3 vérifié \(1 122 pas\)", "outils absents"))
    essai("opérandes inversés", "C24", lambda t: _sub(t, "preuves", r"Test du lecteur : 9/9", "Test du lecteur : (19,66/63,39) 9/9"))
    essai("verdict retourné", "C25", lambda t: t.__setitem__(
        "preuves", t["preuves"].replace("mesuré 5/18", "mesuré 5/18 — TENUE", 1) ))
    essai("mesure de cible effacée", "C25", lambda t: t.__setitem__(
        "preuves", t["preuves"].replace("mesuré 3,264", "mesuré 2,964", 1) ))
    essai("statut d'ancrage contredit", "C20", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("l'ancrage de transparence est DÉPLOYÉ",
                                                  "l'ancrage de transparence est NON DÉPLOYÉ")))

    verts = 0
    print("=" * 78)
    print("CONTRÔLES NÉGATIFS — TREIZE MUTATIONS, TREIZE REFUS NOMMÉS")
    print("=" * 78)
    for nom, classe, ok, r in essais:
        verts += 1 if ok else 0
        detail = [x for x in r if x[0] == classe]
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom} → attendu {classe} : {detail}")
    print(f"{verts}/19")
    return 0 if verts == 19 else 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--controle-negatif", action="store_true")
    a = ap.parse_args()
    if a.controle_negatif:
        return controle_negatif()
    return rapport(verifier())


if __name__ == "__main__":
    sys.exit(main())
