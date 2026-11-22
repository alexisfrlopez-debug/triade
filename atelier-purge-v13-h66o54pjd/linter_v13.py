#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v13.py — LE LINTER DOCUMENTAIRE ÉTENDU (h66o54pjd, la vague 13) :
la règle « aucun verbe d'écriture de dépôt à proximité d'un référent de
phrase, hors table historique datée » au vocabulaire ÉLARGI + LE LINT DES
CHAÎNES DE VERSION (couvertures/avant-propos/tables : Livre == v1.7,
spec == v0.15.8).

LE VOCABULAIRE ÉLARGI (la lettre du plan) : fichier-remise · garde durable
· phrase de contrôle · remise · PHRASE-CONTROLE — le référent de phrase à
PROXIMITÉ d'un verbe d'écriture de dépôt (commit, push, déposer, écrire,
sauvegarder, poser) est REFUSÉ sauf marqueur d'époque daté à proximité
(la table nommée : « du 4 au 19 novembre », « D81, du 4 au 19 novembre
2026 », « amendée D223 », « l'histoire datée », « d'époque », « DATÉE »).

LE LINT DES VERSIONS : les couvertures, avant-propos et tables portent la
version COURANTE (Livre v1.7, spec v0.15.8) — toute version périmée aux
positions nommées (couverture, fancyhead, pdftitle, avant-propos,
tables de correspondance) est ROUGE.

LE CONTRÔLE NÉGATIF : la réinjection d'une instruction D81 synthétique à
une COPIE → REFUS nommé exigé (le linter refuse, la copie détruite)."""
from __future__ import annotations

import pathlib
import re
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[1]
LIVRE = REPO / "scripts" / "livre_v17"
SPEC = REPO / "scripts" / "spec_v158"
PROTO = REPO / "docs" / "PROTOCOLE_TRIADE.md"
CARTE = REPO / "docs" / "FORMAT_CARTE.md"

# LE VOCABULAIRE ÉLARGI (le plan)
REFERENT = re.compile(
    r"fichier-remise|garde durable|phrase de contr[oô]le|"
    r"PHRASE-CONTROLE|la remise|remise D81", re.I)
VERBES = re.compile(
    r"committ|pouss|push|écri[s(t]|ecr[i (]|dépos|depos|"
    r"pos(?:e|ez|er)\b|sauvegard|est la remise|EST la remise|"
    r"posez la phrase", re.I)

# LA TABLE NOMMÉE des marqueurs d'époque datés admis
MARQUEURS_EPOQUE = [
    "du 4 au 19 novembre 2026", "De D81 au 19 novembre 2026",
    "amendée D223", "amendé D223", "AMENDÉE", "l'histoire datée",
    "l'histoire D81", "d'époque", "DATÉE :", "est DATÉE", "HISTOIRE DATÉE",
    "En v0.5.2", "En v0.5.1", "du 4 au 19", "le fichier fut la remise",
    "l'épisode fondateur", "bornée en histoire datée",
    "jamais un geste courant", "la passe vague 12",
    "D81 :", "révision v0.5.2", "28 oct. 2026", "D81 (", "(D81,",
    "l'histoire D81 —", "D81 —", "la décision D81 puis",
]

ROUGES = []
VERTS = 0


def vert(nom: str, detail: str = ""):
    global VERTS
    VERTS += 1
    print(f"VERT  {nom} {detail}")


def rouge(nom: str, detail: str):
    ROUGES.append(f"{nom} : {detail}")
    print(f"ROUGE {nom} : {detail}")


def lint_referents(nom_piece: str, texte: str) -> None:
    """LA RÈGLE : aucun verbe d'écriture de dépôt dans la MÊME UNITÉ
    (phrase ou ligne de table) qu'un référent de phrase, sauf marqueur
    d'époque daté à l'unité ± une voisine (la fenêtre ±200 de la vague 12
    TRAVERSAIT les phrases — l'unité est la PORTÉE, jamais le voisinage
    lointain)."""
    # les unités : les lignes de table (commençant par | ou &) et les
    # phrases (le point, le point-virgule et le retour de ligne séparent)
    unites = []
    for ligne in texte.split("\n"):
        if ligne.strip().startswith(("|",)) or " & " in ligne:
            unites.append(ligne)
        else:
            # la coupure ÉPARGNE les points des NUMÉROS de version (le
            # « v0.5.2 » ne se coupe pas : le marqueur d'époque demeure
            # entier à son unité)
            unites.extend(x + "." for x in re.split(
                r"(?<!\d)[.;](?!\d)", ligne) if x.strip())
    occurrences = [m.start() for m in REFERENT.finditer(texte)]
    if not occurrences:
        vert(f"les référents ({nom_piece})",
             "aucune occurrence — la garde active ne vit pas au référent")
        return
    fautives = 0
    for i, u in enumerate(unites):
        if not REFERENT.search(u):
            continue
        # LA REMISE NUE (sans « fichier-remise » ni « remise D81 ») : la
        # règle ne la couvre QUE si l'unité porte le contexte PHRASE (la
        # remise du SCEAU — sceau_I.py, la graine Ed25519, les arbres
        # signés — est UNE AUTRE remise, légitime au dépôt)
        if re.search(r"(?<!fichier-)la remise(?! D81)", u) and not re.search(
                r"phrase|coffre|PHRASE|D81", u):
            continue
        if VERBES.search(u):
            # le marqueur d'époque à l'unité OU à la voisine (l'index PAR
            # POSITION, jamais .index() — les unités répétées trahissaient
            # le voisinage)
            voisines = " ".join(unites[max(0, i - 1):i + 2])
            if not any(m in voisines for m in MARQUEURS_EPOQUE):
                fautives += 1
                rouge(f"les référents ({nom_piece})",
                      f"le verbe d'écriture À L'UNITÉ du référent : "
                      f"« {u.strip()[:110]} » HORS marqueur d'époque")
    if fautives == 0:
        vert(f"les référents ({nom_piece})",
             f"{len(occurrences)} occurrence(s), AUCUNE à verbe "
             f"d'écriture d'unité hors contexte daté")


def lint_versions() -> None:
    """LE LINT DES VERSIONS : les positions nommées portent la version
    courante (Livre v1.7 · spec v0.15.8)."""
    positions = [
        (LIVRE / "main.tex", "v1.7", ["fancyhead", "pdftitle", "v1.7"]),
        (LIVRE / "cover.html", "v1.7",
         ["r&eacute;vision v1.7", "Version 1.7"]),
        (LIVRE / "sec-1.tex", "v1.7", ["v1.7"]),
        (SPEC / "main.tex", "v0.15.8",
         ["v0.15.8", "fancyhead", "pdftitle"]),
        (SPEC / "sec-d.tex", "v0.15.8", ["v0.15.8"]),
    ]
    for chemin, version, _mots in positions:
        if not chemin.exists():
            continue
        t = chemin.read_text(encoding="utf-8")
        if chemin.suffix == ".tex":
            t = "\n".join(l for l in t.split("\n")
                           if not l.strip().startswith("%"))
        nom = f"les versions ({chemin.parent.name}/{chemin.name})"
        if version in t:
            vert(nom, f"la version courante {version} présente")
        else:
            rouge(nom, f"la version courante {version} ABSENTE")
        # les versions PÉRIMÉES aux positions nommées
        perimees = []
        if "livre" in str(chemin):
            for vieille in ["v1.3", "v1.4", "v1.5", "v1.6"]:
                if vieille in t:
                    perimees.append(vieille)
        else:
            for vieille in ["v0.15.5", "v0.15.6", "v0.15.7"]:
                if vieille in t:
                    perimees.append(vieille)
        if perimees:
            # les traces HISTORIQUES nommées (les correspondances d'époque)
            # admises seulement aux sections de correspondance — le grep
            # rapide : une version périmée EST rouge sauf aux lignes de
            # correspondance (« v0.15.7 → », « (v0.15.7) »)
            lignes = t.split("\n")
            fausses = [l for l in lignes
                       if any(v in l for v in perimees)
                       and "→" not in l and "correspondance" not in l.lower()
                       and "succède" not in l.lower()]
            if fausses:
                rouge(nom, f"des versions périmées {perimees} hors "
                           f"correspondance : {fausses[0][:60]!r}")
            else:
                vert(nom, f"les traces périmées {perimees} toutes aux "
                          f"correspondances datées")
        else:
            vert(nom, "aucune version périmée")


def main() -> int:
    print("[h66o54pjd] LE LINTER DOCUMENTAIRE ÉTENDU")
    pieces = {
        "livre v1.7": "\n".join(
            f.read_text(encoding="utf-8")
            for f in sorted(LIVRE.glob("sec-*.tex"))),
        "spec v0.15.8": "\n".join(
            f.read_text(encoding="utf-8")
            for f in sorted(SPEC.glob("sec-*.tex"))),
        "protocole": PROTO.read_text(encoding="utf-8"),
        "format-carte": CARTE.read_text(encoding="utf-8"),
    }
    for nom, texte in pieces.items():
        lint_referents(nom, texte)
    lint_versions()

    # LE CONTRÔLE NÉGATIF : une instruction D81 synthétique réinjectée à
    # une COPIE → REFUS nommé exigé
    faux = ("Le développeur pose la phrase de contrôle au dépôt : "
            "PHRASE-CONTROLE-COFFRE.txt, commit dédié, push GitHub — "
            "le fichier est la remise.")
    detecte = False
    if REFERENT.search(faux) and VERBES.search(faux) and not any(
            m in faux for m in MARQUEURS_EPOQUE):
        detecte = True
    if detecte:
        vert("le contrôle négatif",
             "l'instruction D81 synthétique REFUSÉE au premier nom "
             "(le référent + le verbe, hors marqueur d'époque)")
    else:
        rouge("le contrôle négatif", "l'instruction synthétique NON attrapée")
    # (la réinjection vécue : le linter appelé sur la copie)
    with tempfile.NamedTemporaryFile("w", suffix=".md",
                                     delete=False) as f:
        f.write("# copie\n" + faux + "\n")
        chemin_faux = pathlib.Path(f.name)
    texte_faux = chemin_faux.read_text(encoding="utf-8")
    occurrences_avant = len(ROUGES)
    lint_referents("la copie réinjectée", texte_faux)
    chemin_faux.unlink()
    if len(ROUGES) > occurrences_avant:
        vert("la réinjection vécue",
             "la COPIE refusée nommément, la réinjection retirée")
    else:
        rouge("la réinjection vécue", "la copie n'a pas été refusée")

    print(f"\n[h66o54pjd] {VERTS} VERT · {len(ROUGES)} ROUGE")
    return 0 if not ROUGES else 1


if __name__ == "__main__":
    sys.exit(main())
