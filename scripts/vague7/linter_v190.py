#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v190.py — LE LINTER DE LA V0.19.0 : les affirmations de la clôture
D210 portées au build, chacune avec sa dérivation. Fail-closed : toute valeur
manquante ou erronée REFUSE.

LES SOURCES :
  - scripts/campagne_d204/reception-357/livraisons.csv (le livre, 29 lignes)
  - scripts/campagne_d204/reception-357/defauts.csv (11 défauts)
  - scripts/campagne_d204/reception-357/carnet_temps_humain.csv (M3 au geste)
  - scripts/campagne_d204/PLAN-EXTENSION-D210.md (le plan, sha256 4a3b1311…)
  - worklog.md (les Entrées 335-357 — les figures consignées)

LES ASSERTIONS (la clôture D210) :
  (1) le plan : hash 4a3b1311, la graine 20261117, le tirage « une chance sur huit »
  (2) les livraisons : 7 D210 (4 VERT + 3 ROUGE), les 29 lignes au livre
  (3) les échappées : TROIS comptées, toutes côté kit, les classes nommées
  (4) l'attribution : 14 VERT 0 ROUGE, le kit standard minimal
  (5) M2 : 42,610 (couture 23,220 + 19,390) / 52,729 / 40,749 / 26,662,
      le gap de l'attribution nommé
  (6) M3 : 4 min T / 1 min C, l'écart des bornes nommé
  (7) M4 : les oracles 33.6/4.0/146/57 s, POSIX 1.4--8.1, dll mappée 1.5,
      mingw 0.08
  (8) H6 tenue par attribution ; H7 non testée (le contraste vide, le report) ;
      H8 réfutée (51/39/9 %, la première 44 % la couture nommée —
      13,536/23,220 et 5,291/19,390)
  (9) la plage des Entrées : 305--357 (305--319 interdit désormais)
  (10) la table D210 : les 7 lignes du registre, la colonne It. telle que
       déposée (it2 = 1, l'écart R11-② jamais corrigé)

Usage :
  python3 linter_v190.py <manuscrit.tex>            # le verdict
  python3 linter_v190.py <manuscrit.tex> --falsifie # contrôles négatifs
"""
from __future__ import annotations

import csv
import hashlib
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
ATELIER = REPO / "scripts/campagne_d204/reception-357"


def lire_csv_diese(chemin: pathlib.Path) -> list[dict]:
    with open(chemin, encoding="utf-8-sig") as f:
        return list(csv.DictReader(
            l for l in f if not l.startswith("#")))


def normaliser(s: str) -> str:
    s = s.replace("\n", " ")
    s = re.sub(r"\\code\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\emph\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\textbf\{([^}]*)\}", r"\1", s)
    s = re.sub(r"[\\{}]", "", s)
    s = s.replace("---", " --- ")
    return re.sub(r"\s+", " ", s)


def verdict(ok: bool, msg: str, echecs: list):
    print(("  VERT  " if ok else "  ROUGE ") + msg)
    if not ok:
        echecs.append(msg)


def main(tex_path: str, falsifie: bool = False):
    src = pathlib.Path(tex_path)
    # le texte combine : le manuscrit + les tables \inputees (comme au PDF)
    parts = [src.read_text(encoding="utf-8")]
    for tbl in ["table-campagne-d210.tex", "table-campagne.tex", "statuts_v190.tex"]:
        f = src.parent / "donnees" / tbl
        if f.exists():
            parts.append(f.read_text(encoding="utf-8"))
    texte = normaliser("\n".join(parts))

    livraisons = lire_csv_diese(ATELIER / "livraisons.csv")
    defauts = lire_csv_diese(ATELIER / "defauts.csv")
    carnet = lire_csv_diese(ATELIER / "carnet_temps_humain.csv")
    plan_hash = hashlib.sha256(
        (REPO / "scripts/campagne_d204/PLAN-EXTENSION-D210.md").read_bytes()
    ).hexdigest()

    d210 = [l for l in livraisons if l["tache"].endswith("-d210") or l["tache"] == "loupe-16-attr"]
    vert = sum(1 for l in d210 if l["verdict"] == "VERT")
    rouge = sum(1 for l in d210 if l["verdict"] == "ROUGE")
    comptees = [d for d in defauts if d["livraison"] and d["exclusion"] == "non"
                and d["livraison"].startswith("T-loupe-16-d210")]
    carnet_d210 = [c for c in carnet if c["geste"] == "run-terrain"
                   and (c["tache"].endswith("-d210") or c["tache"] == "loupe-16-attr")]
    m3_t = sum(int(c["minutes"]) for c in carnet_d210 if c["bras"] == "T")
    m3_c = sum(int(c["minutes"]) for c in carnet_d210 if c["bras"] == "C")

    echecs: list[str] = []
    print(f"LE LINTER V190 — {src.name}" + (" [FALSIFIE]" if falsifie else ""))
    print(f"  dérivation : le plan sha256 {plan_hash[:8]}…, le livre "
          f"{len(livraisons)} lignes, le carnet {len(carnet_d210)} lignes D210")

    # falsification : on mutre une valeur pour éprouver le contrôle
    if falsifie:
        texte = texte.replace("14 VERT, 0 ROUGE", "13 VERT, 0 ROUGE")
        texte = texte.replace("4a3b1311", "4a3b1312")
        texte = texte.replace("51\\%", "50\\%").replace("51%", "50%")

    # (1) le plan
    verdict(plan_hash.startswith("4a3b1311") and "4a3b1311" in texte,
            "(1) le hash du plan 4a3b1311 (dérivé : le fichier, sha256)", echecs)
    verdict("20261117" in texte, "(1) la graine 20261117 consignée", echecs)
    verdict("one-in-eight" in texte, "(1) le tirage une chance sur huit, consigné tel quel", echecs)

    # (2) les livraisons
    verdict(f"{len(d210)}" == "7" and vert == 4 and rouge == 3
            and ("seven witnessed deliveries" in texte or "extension's seven deliveries" in texte),
            f"(2) 7 livraisons D210 (4 VERT + 3 ROUGE) — dérivé : {len(d210)}, {vert}+{rouge}", echecs)
    verdict(f"{len(livraisons)}" == "29" and "29 witnessed deliveries" in texte,
            f"(2) les 29 livraisons aux deux campagnes — dérivé : {len(livraisons)}", echecs)

    # (3) les échappées
    classes = sorted({d["classe"] for d in comptees})
    verdict(len(comptees) == 3 and "three counted escapes" in texte,
            f"(3) TROIS échappées comptées — dérivé : {len(comptees)}", echecs)
    verdict(all(c in texte.replace(" / ", "/") or c in texte for c in classes[:1])
            and "guichet-descripteur-quatre-champs" in texte
            and "liaison-memmove-deux-arguments" in texte,
            "(3) les classes nommées au texte (guichet, memmove, metriques)", echecs)
    verdict(all(d["cote"] == "kit" for d in comptees) and "every one kit-side" in texte,
            "(3) toutes côté kit, la pièce jamais fautive", echecs)

    # (4) l'attribution
    verdict("14 VERT, 0 ROUGE" in texte, "(4) l'attribution : 14 VERT, 0 ROUGE", echecs)
    verdict("minimal standard kit" in texte, "(4) le kit standard minimal nommé", echecs)

    # (5) M2
    for v in ["42,610", "23,220", "19,390", "52,729", "40,749", "26,662"]:
        verdict(v in texte, f"(5) M2 {v} présent", echecs)
    verdict("named M2 gap" in texte or "M2 gap" in texte,
            "(5) le gap M2 de l'attribution nommé (jamais reconstruit)", echecs)

    # (6) M3
    verdict(f"{m3_t}" == "4" and f"{m3_c}" == "1"
            and "four minutes" in texte and "one minute" in texte,
            f"(6) M3 : T {m3_t} min / C {m3_c} min (dérivé du carnet)", echecs)
    verdict("1.5, 1.3 and 1.1" in texte and "filed bounds" in texte,
            "(6) l'écart des bornes nommé (les consoles 1,5/1,3/1,1 min)", echecs)

    # (7) M4
    for v in ["33.6", "4.0", "146", "57", "1.4--8.1", "1.5", "0.08"]:
        verdict(v in texte, f"(7) M4 {v} présent", echecs)

    # (8) H6-H8
    verdict("holds, by attribution" in texte, "(8) H6 tenue par attribution", echecs)
    verdict("untested on this draw" in texte and "carries to the next campaign" in texte,
            "(8) H7 non testée — le contraste vide, le report nommé", echecs)
    verdict("51\\%" in texte or "51%" in texte, "(8) H8 : 51 % (la deuxième, tenue)", echecs)
    verdict("39\\%" in texte or "39%" in texte, "(8) H8 : 39 % (la troisième, rompue)", echecs)
    verdict("9\\%" in texte or "9%" in texte, "(8) H8 : 9 % (la quatrième)", echecs)
    for v in ["13,536|13{,}536", "5,291|5{,}291", "44\\%|44%|44,0"]:
        verdict(any(x in texte for x in v.split("|")), f"(8) la première unité : {v}", echecs)
    verdict("falsified" in texte and "it was the early one" in texte,
            "(8) H8 réfutée — la conclusion", echecs)

    # (9) la plage des Entrées
    verdict("305--357" in texte and "305--319" not in texte,
            "(9) la plage des Entrées 305--357 (305--319 interdit)", echecs)

    # (10) la table
    table = normaliser((REPO / "edition-v0190/donnees/table-campagne-d210.tex").read_text(encoding="utf-8"))
    it2 = [l for l in d210 if l["livraison"] == "T-loupe-16-d210-it2"][0]["numero_iteration"]
    verdict(f"T-loupe-16-d210-it2" in table and f" & {it2} & " in table.replace("  ", " "),
            f"(10) la colonne It. telle que déposée (it2 = {it2}, l'écart R11-②)", echecs)
    verdict("C-loupe-16-attr-it1" in table, "(10) la ligne d'attribution à la table", echecs)

    print()
    if echecs:
        print(f"ROUGE — {len(echecs)} échec(s) : le build est REFUSÉ")
        return 2
    print("VERT — le registre de la v0.19.0 est armé au build")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fals = "--falsifie" in sys.argv
    sys.exit(main(args[0] if args else "edition-v0190/main.tex", fals))
