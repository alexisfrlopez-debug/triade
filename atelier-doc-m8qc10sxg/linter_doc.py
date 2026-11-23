#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_doc.py — m8qc10sxg LE GESTE SUIVANT : LE LINTER DOC.

TROIS CLASSES DE RÈGLES (chacune fail-closed, le refus NOMMÉ) :
  (1) LA PARITÉ NUMÉRIQUE EN/FR — le multiset des nombres de chaque
      fragment EN doit être ÉGAL à celui de son miroir FR (les tables
      numériques générées des canons : une divergence = un refus nommé) ;
  (2) L'IDENTITÉ DES IDENTIFICATEURS LITTÉRAUX — les constantes du
      protocole (les classes de refus, les IDs LBL/CST, les règles Rn,
      les décisions Dn, les gabarits TPL-EDIT-v1 / SQUELETTE-v2, les
      blocs loupe-XX) demeurent LITTÉRALES aux deux langues — un
      identifiant traduit ou absent = un refus nommé ;
  (3) LES BUDGETS — chaque fragment agent re-mesuré au tokenizer natif
      (cl100k_base) depuis le FICHIER ; un fragment hors budget est un
      refus nommé, jamais un budget silencieusement élargi.

LE CONTRÔLE NÉGATIF (la preuve que le linter porte) :
  linter_doc.py controle-negatif
  (a) une valeur numérique divergente plantée au miroir FR DOIT être
      attrapée ;
  (b) un identifiant traduit (HORS-FORMAT → OUT-OF-FORMAT) DOIT être
      attrapé.

Usage :
  linter_doc.py verifier [en_dir fr_dir]   (défaut : fragments/ fragments-fr/)
  linter_doc.py controle-negatif
"""
from __future__ import annotations

import pathlib
import re
import shutil
import sys
import tempfile

import tiktoken

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parents[1]
EN_DEFAUT = ICI / "fragments"
FR_DEFAUT = ICI / "fragments-fr"
ORDRE = ["AGENT-CORE", "QUICKSTART", "DEVELOPER_GUIDE", "TROUBLESHOOTING",
         "SECURITY", "REFERENCE", "DOC-LOC", "DOC-EDIT", "DOC-ADD",
         "DOC-REFUS", "DOC-CEREMONY", "DOC-FEEDBACK", "CAPABILITY_PROBE"]

# LES IDENTIFICATEURS LITTÉRAUX (les constantes du protocole — jamais
# traduites) : les classes de refus, les IDs du dictionnaire, les règles,
# les décisions, les gabarits, les blocs du banc.
MOTIFS_ID = [
    r"\b(?:HORS-FORMAT|ID-INCONNU|EXPANSION-DIVERGENTE|FORME-INVALIDE"
    r"|HUNK-INCONNU|CONTEXTE-DIVERGENT|ROUND-TRIP-DIVERGENT"
    r"|POINTEUR-INCONNU|EMPREINTE-DIVERGENTE)\b",
    r"\b(?:LBL|CST)-\d{3}\b",
    r"\bR\d{1,2}\b",
    r"\bD\d{2,3}\b",
    r"\bTPL-EDIT-v1\b",
    r"\bSQUELETTE-v2\b",
    r"\bloupe-\d{2}-[a-z0-9]+\b",
    r"\bAIR-GAP\b",
    r"\bCC-BY(?:-\d)?",
    r"\bBSL\b",
    r"\bDOC-(?:LOC|EDIT|ADD|REFUS|CEREMONY|FEEDBACK)\b",
    r"\bCAPABILITY_PROBE\b",
]
ID_RE = re.compile("|".join(MOTIFS_ID), re.I)
NUM_RE = re.compile(r"\d+")


def nombres(texte: str) -> list:
    return sorted(NUM_RE.findall(texte))


def identifiants(texte: str) -> list:
    return sorted(m.group(0).upper() for m in ID_RE.finditer(texte))


def lire(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8")


def verifier_fragments(en_dir: pathlib.Path, fr_dir: pathlib.Path,
                       budget: bool = True) -> list:
    """LES TROIS CLASSES ; rend la liste des REFUS NOMMÉS (vide = vert)."""
    refus = []
    tok = tiktoken.get_encoding("cl100k_base")
    cibles = {}
    if budget and (ICI / "registres" / "budgets-complet.json").exists():
        cibles = {k: v for k, v in json_loads(
            ICI / "registres" / "budgets-complet.json").items()
            if "cible" in v}
    for nom in ORDRE:
        fen, ffr = en_dir / f"{nom}.md", fr_dir / f"{nom}.md"
        if not fen.exists() or not ffr.exists():
            refus.append(f"ABSENT : {nom}.md ne vit pas aux deux miroirs")
            continue
        ten, tfr = lire(fen), lire(ffr)
        # (1) la parité numérique
        if nombres(ten) != nombres(tfr):
            refus.append(f"PARITÉ NUMÉRIQUE : {nom} — EN {nombres(ten)} "
                         f"!= FR {nombres(tfr)}")
        # (2) l'identité des identificateurs
        if identifiants(ten) != identifiants(tfr):
            manq_en = sorted(set(identifiants(ten)) - set(identifiants(tfr)))
            manq_fr = sorted(set(identifiants(tfr)) - set(identifiants(ten)))
            refus.append(f"IDENTIFIANT : {nom} — les littéraux divergent "
                         f"(absents du FR : {manq_en} ; absents de l'EN : "
                         f"{manq_fr})")
        # (3) le budget (re-mesuré DEPUIS LE FICHIER)
        if nom in cibles:
            c = cibles[nom]["cible"]
            for lang, t, p in (("EN", ten, fen), ("FR", tfr, ffr)):
                n = len(tok.encode(t))
                if n > c:
                    refus.append(f"BUDGET : {nom} ({lang}) — {n} tokens "
                                 f"> la cible {c} (le fichier {p.name})")
    return refus


def json_loads(p: pathlib.Path):
    import json
    return json.loads(lire(p))


def cmd_verifier(argv: list) -> int:
    en_dir = pathlib.Path(argv[0]) if argv else EN_DEFAUT
    fr_dir = pathlib.Path(argv[1]) if len(argv) > 1 else FR_DEFAUT
    refus = verifier_fragments(en_dir, fr_dir)
    total = len(ORDRE)
    if refus:
        print(f"[linter_doc] REFUS — {len(refus)} rouge(s) sur "
              f"{total} canaux :")
        for r in refus:
            print("  — " + r)
        return 2
    print(f"[linter_doc] {total}/{total} canaux VERTS — la parité "
          "numérique, l'identité des littéraux, les budgets re-mesurés "
          "depuis les fichiers")
    return 0


def cmd_controle_negatif() -> int:
    """LES DEUX CONTRÔLES NÉGATIFS VÉCUS : la divergence numérique
    plantée, l'identifiant traduit — chacun DOIT être attrapé."""
    attrapes = []
    with tempfile.TemporaryDirectory(dir=ICI) as td:
        tdp = pathlib.Path(td)
        # (a) la valeur numérique divergente plantée au FR
        fr_a = tdp / "fr-a"
        shutil.copytree(FR_DEFAUT, fr_a)
        cible = fr_a / "DOC-LOC.md"
        t = lire(cible)
        assert "627" in t, "le témoin numérique 627 absent du DOC-LOC FR"
        cible.write_text(t.replace("627", "628", 1), encoding="utf-8")
        r = verifier_fragments(EN_DEFAUT, fr_a, budget=False)
        if r and any("PARITÉ NUMÉRIQUE : DOC-LOC" in x for x in r):
            attrapes.append("(a) la valeur numérique divergente plantée "
                            "(627 → 628 au DOC-LOC FR) : ATTRAPÉE — "
                            + next(x for x in r
                                   if x.startswith("PARITÉ NUMÉRIQUE"))[:90])
        else:
            print("[controle-negatif] REFUS DU CONTRÔLE : la divergence "
                  "numérique plantée N'A PAS ÉTÉ attrapée — le linter NE "
                  "PORTE PAS")
            return 1
        # (b) l'identifiant traduit (HORS-FORMAT → OUT-OF-FORMAT)
        fr_b = tdp / "fr-b"
        shutil.copytree(FR_DEFAUT, fr_b)
        cible = fr_b / "DOC-REFUS.md"
        t = lire(cible)
        assert "HORS-FORMAT" in t, "le témoin HORS-FORMAT absent du DOC-REFUS"
        cible.write_text(t.replace("HORS-FORMAT", "OUT-OF-FORMAT", 1),
                         encoding="utf-8")
        r = verifier_fragments(EN_DEFAUT, fr_b, budget=False)
        if r and any("IDENTIFIANT : DOC-REFUS" in x for x in r):
            attrapes.append("(b) l'identifiant traduit (HORS-FORMAT → "
                            "OUT-OF-FORMAT au DOC-REFUS FR) : ATTRAPÉ — "
                            + next(x for x in r
                                   if x.startswith("IDENTIFIANT"))[:90])
        else:
            print("[controle-negatif] REFUS DU CONTRÔLE : l'identifiant "
                  "traduit N'A PAS ÉTÉ attrapé — le linter NE PORTE PAS")
            return 1
    print("[controle-negatif] 2/2 ATTRAPÉS — le linter PORTE :")
    for a in attrapes:
        print("  — " + a)
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "controle-negatif":
        return cmd_controle_negatif()
    reste = sys.argv[1:]
    if reste and reste[0] == "verifier":
        reste = reste[1:]          # le mot de commande ne vit pas au chemin
    return cmd_verifier(reste)


if __name__ == "__main__":
    raise SystemExit(main())
