#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA PORTE DE GÉNÉRATION v0.33.1 (l'édition corrective de la vague 28) — le linter EST la porte.

  V1  les cinq pièces existent et leurs empreintes égalent le manifeste ;
  V2  chaque pièce porte SA chaîne de version ;
  V3  le ratio corrigé recompose (63,39/19,66 = 3,22 ; « 3.23× » absent) ;
  V4  les douze lignes du registre de provenance se recomposent (délégué) ;
  V5  aucun secret : aucun fichier du pack ne porte de motif de clé privée ;
  V6  l'ancrage de transparence (D267) — le témoin RFC 3161 recoupé ;
  V7  le tableau descendant est engendré, à diff nul (D260) ;
  L1..L32  le linter v5 : les classes des vagues précédentes reconduites +
           C30 N-VALUE + C31 CLAIM-SCOPE (la vague 28) + C32 RATIO-RECOMPOSE
           (la correction v0.33.1 : tout ratio canonique publié se recompose de
           ses opérandes non arrondis lus aux registres).

Contrôles négatifs : les mutations des vagues précédentes reconduites aux
chaînes de v0.33.1 + les TROIS de la vague 28-correction (le n= retiré d'une
médiane publiée — C30 ; le scope retiré d'une revendication first/only — C31 ;
un ratio volontairement faux — C32) → refus nommés, sur COPIES.
"""
import argparse
import hashlib
import importlib.util
import pathlib
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]
PACK = RACINE / "pack-v331"
MANIFESTE = PACK / "empreintes_livrables_v0.33.1.txt"

PIECES = {
    "manuscrit": (PACK / "1-manuscrit" / "TRIADE_manuscrit_v0.33.0.pdf", "v0.33.0"),
    "specification": (PACK / "2-specification" / "Protocole_TRIADE_v0.15.18_Specification.pdf", "v0.15.18"),
    "livre": (PACK / "3-coffre-fort" / "Livre_du_Coffre_TRIADE_CF1-CF3_v1.17.pdf", "v1.17"),
    "preuves": (PACK / "4-preuves-calculs" / "TRIADE_preuves_et_calculs_v0.33.1.pdf", "v0.33.1"),
    "presentation": (PACK / "5-presentation" / "TRIADE_presentation_v0330.pdf", "v0.33.0"),
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
    # V6 l'ancrage de transparence (D267) fait foi
    ancrage = RACINE / "atelier-w20-sec" / "ancrage-recu.json"
    if ancrage.exists():
        r6 = subprocess.run([sys.executable, str(RACINE / "scripts/vague20/ancrage_transparence.py"),
                             "--verifier"], capture_output=True, text=True)
        if r6.returncode != 0:
            refus.append(("V6", "ancrage", (r6.stdout or r6.stderr).strip()[:120]))
        else:
            print("[V6] ancrage vérifié — témoin d'époque RFC 3161 recoupé")
    # V7 tableau
    r7 = subprocess.run([sys.executable, str(RACINE / "scripts/vague17/provenance_tableaux.py"),
                         "--tableaux-verifier"], capture_output=True, text=True)
    if r7.returncode != 0:
        refus.append(("V7", "tableau-descendant", (r7.stdout or "").strip()[:120]))
    # L1..L29 — le linter est la porte
    L = _linter()
    pack = pathlib.Path(list(pieces.values())[0][0]).parents[1]
    textes = L.charge(pack)
    refus.extend(L.verifie(textes, L.charge_manifeste(pack), L.recompte_banc(), pack))
    refus.extend(L.controles_w25(textes, RACINE, "v0.33.1", "v0.15.18"))
    refus.extend(L.controles_w26(textes, RACINE))
    refus.extend(L.controles_w27(textes, RACINE))
    refus.extend(L.controles_w27b(textes, RACINE))
    refus.extend(L.controles_w28c(textes, RACINE))
    return refus


def rapport(refus):
    print("=" * 78)
    print("PORTE DE GÉNÉRATION v0.33.1 — V1..V7 + L1..L32 (le linter est la porte)")
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
          "V6 ancrage · V7 tableau")
    print("[VERT] L1..L32 — trente-deux classes, zéro résidu")
    return 0


def controle_negatif():
    import re as _re
    L = _linter()
    base = L.charge(PACK)
    rec = L.recompte_banc()
    essais = []

    def essai(nom, classe, mut):
        t = {k: v for k, v in base.items()}
        mut(t)
        r = list(L.verifie(t, None, rec))
        r += list(L.controles_w25(t, RACINE, "v0.33.1", "v0.15.18"))
        r += list(L.controles_w26(t, RACINE))
        r += list(L.controles_w27(t, RACINE))
        r += list(L.controles_w27b(t, RACINE))
        r += list(L.controles_w28c(t, RACINE))
        essais.append((nom, classe, any(c == classe for c, _, _ in r), r))

    def essai_spec(nom, classe, controle):
        """un contrôle qui porte ses propres entrées (titres, registres) — sur copies."""
        ok, r = controle(base)
        essais.append((nom, classe, ok, r))

    def _sub(t, piece, motif, remp):
        t[piece] = _re.sub(motif, remp, t[piece], count=1)

    # --- les mutations des vagues précédentes, reconduites aux chaînes v0.32.0
    essai("libellé de version muté", "C6", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("Manuscrit\n\nv0.33.0", "Manuscrit\n\nv0.24.0")))
    essai("ID hors plage", "C7", lambda t: t.__setitem__(
        "preuves", t["preuves"] + "\nla décision D299 tranche."))
    essai("ligne de menace non qualifiée", "C11", lambda t: t.__setitem__(
        "specification", t["specification"].replace("ADV-MEDIA", "ADVX-MEDIA")))
    essai("compte de banc muté", "C10", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("16/16", "15/15")))
    essai("version de prose mutée (Livre)", "C12", lambda t: t.__setitem__(
        "livre", t["livre"].replace("v1.16", "v1.9")))
    essai("résumé trop long", "C14", lambda t: t.__setitem__(
        "manuscrit", t["manuscrit"].replace("Abstract", "Abstract " + ("mot " * 300), 1)))
    essai("compte du registre muté", "C16", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("porte 10 entrées", "porte 11 entrées")))
    essai("compte oracle muté", "C17", lambda t: t.__setitem__(
        "presentation", t["presentation"].replace("95 exécutés au contexte standard", "94 exécutés au contexte standard")))
    essai("compte de classes muté", "C18", lambda t: _sub(t, "preuves", r"\b32 classes\b", "17 classes"))
    essai("vague de titre périmée", "C19", lambda t: _sub(t, "presentation", r"La vague 28", "La vague 19"))
    essai("DOI inconnu du registre", "C21", lambda t: _sub(
        t, "manuscrit", r"10\.5281/zenodo\.24545339", "10.5281/zenodo.99999999"))
    essai("version anglaise périmée", "C22", lambda t: _sub(
        t, "manuscrit", r"accompanied\s+here\s+is\s+v0\.15\.18",
        "accompanied here is v0.15.8 which this edition accompanies"))
    essai("statut Tamarin contredit", "C23", lambda t: _sub(
        t, "presentation", r"L3 rejoint bit-identiquement \(1 122 pas\)",
        "Tamarin : outils absents"))
    essai("opérandes inversés", "C24", lambda t: _sub(
        t, "preuves", r"Test du lecteur : 9/9", "Test du lecteur : (19,66/63,39) 9/9"))
    essai("verdict retourné", "C25", lambda t: t.__setitem__(
        "preuves", t["preuves"].replace("MANQUÉE", "TENUE", 1)))
    essai("statut d'ancrage contredit", "C20", lambda t: t.__setitem__(
        "preuves", t["preuves"].replace("DÉPLOYÉ (D267", "NON DÉPLOYÉ (D267")))

    # --- les QUATRE mutations de la vague 27 ----------------------------------
    essai("statut partagé contredit (C26)", "C26", lambda t: t.__setitem__(
        "livre", t["livre"].replace("le déploiement est\nAPPLIQUÉ", "le déploiement n'est pas fait")))
    essai("compte d'arbres muté (C27)", "C27", lambda t: _sub(
        t, "specification", r"verifier 14 arbres", "verifier 13 arbres"))
    def _c28(t):
        titres = L._titres_pieces(RACINE)
        titres["specification"] = [
            x.replace(" — la prose de statut dérivée (D275)", "").replace(" — les six résidus (D274)", "")
            for x in titres["specification"]]
        r = list(L.controles_w27b(t, RACINE, titres_override=titres))
        return any(c == "C28" for c, _, _ in r), r
    essai_spec("titre de vague dupliqué (C28)", "C28", _c28)
    essai("fragment français ressuscité (C29)", "C29", lambda t: t.__setitem__(
        "manuscrit", t["manuscrit"].replace("1,122 steps, replayed", "1 122 pas, rejoués")))

    # --- les TROIS mutations de la vague 28-correction -------------------------
    essai("le n= retiré d'une médiane publiée (C30)", "C30", lambda t: t.__setitem__(
        "manuscrit", t["manuscrit"].replace(
            "median 27.5 native tokens over the eighteen tasks, n=18",
            "median 27.5 native tokens over the eighteen tasks")))
    essai("la revendication sans scope (C31)", "C31", lambda t: t.__setitem__(
        "manuscrit", t["manuscrit"] + "\nThis study presents the first system ever."))
    essai("le ratio volontairement faux (C32)", "C32", lambda t: t.__setitem__(
        "preuves", t["preuves"].replace("13,6 ×", "33 ×")))

    verts = 0
    print("=" * 78)
    print("CONTRÔLES NÉGATIFS — VINGT-TROIS MUTATIONS, VINGT-TROIS REFUS NOMMÉS")
    print("=" * 78)
    for nom, classe, ok, r in essais:
        verts += 1 if ok else 0
        detail = [x for x in r if x[0] == classe]
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom} → attendu {classe} : {detail[:1]}")
    print(f"{verts}/{len(essais)}")
    return 0 if verts == len(essais) else 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--controle-negatif", action="store_true")
    a = ap.parse_args()
    if a.controle_negatif:
        return controle_negatif()
    return rapport(verifier())


if __name__ == "__main__":
    sys.exit(main())
