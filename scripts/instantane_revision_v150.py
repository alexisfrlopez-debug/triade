#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""instantane_revision_v150.py — l'état AVANT/APRÈS de la révision
manuscrit+spécification (paquet 4 de la vague 3, instruction sollwnmae).

Mode d'emploi :
  python3 instantane_revision_v150.py avant|apres [fichier-rapport]

Consigne pour chaque mode : sha256 des artefacts scellés (loupe.exe,
proxy.exe, demo.exe, selftest.exe), des PDF livrés de l'édition
(docs/ + les zips + les main.pdf/final.pdf des chaînes), et de chaque
fichier source appelé à être révisé. Le rapport APRÈS est confronté au
rapport AVANT par le vérificateur (verifier_revision_v150.py)."""

import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")


def sha256(chemin: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


# Les pièces scellées (jamais touchées par la révision) — les
# empreintes CONSIGNÉES (empreintes.csv du manuscrit, D170/D178/D181)
# sont : loupe 0.1.1 c1115105…, proxy 1.0.0 (tls13, D170) 446279f3…
SCELLES = [
    REPO / "loupe" / "loupe.exe",
    REPO / "tls13" / "proxy.exe",
    REPO / "demo" / "demo.exe",
    REPO / "m1" / "selftest.exe",
]

# Les livrés de l'édition v0.15.0 (INTACTS — la révision vit aux sources)
LIVRES = [
    REPO / "docs" / "TRIADE_manuscrit_v0.15.0.pdf",
    REPO / "docs" / "Protocole_TRIADE_v0.15.0_Specification.pdf",
    REPO / "download" / "edition_v0150" / "TRIADE_soumission_v0.15.0.zip",
    REPO / "download" / "edition_v0150" / "TRIADE_complet_v0.15.0.zip",
    REPO / "download" / "edition_v0150" / "empreintes_livrables.txt",
    REPO / "scripts" / "manuscrit_v150" / "main.pdf",
    REPO / "scripts" / "spec_v150" / "main.pdf",
    REPO / "scripts" / "spec_v150" / "final.pdf",
]

# Les sources appelées à être révisées (le diff fera foi)
SOURCES = [
    REPO / "scripts" / "manuscrit_v150" / "main.tex",
    REPO / "scripts" / "spec_v150" / "sec-a.tex",
    REPO / "scripts" / "spec_v150" / "sec-d.tex",
    REPO / "scripts" / "statuts_preuves_v150.py",
    REPO / "scripts" / "replication_v150" / "grille_tx.csv",
    REPO / "scripts" / "replication_v150" / "LISEZMOI-replication.txt",
    REPO / "scripts" / "replication_v150" / "kohen_kappa_v150.py",
    REPO / "scripts" / "manuscrit_v150" / "donnees" / "statuts_v150.tex",
    REPO / "scripts" / "manuscrit_v150" / "donnees" / "tables_generees.tex",
    REPO / "scripts" / "manuscrit_v150" / "donnees" / "macros_v150.tex",
]


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "avant"
    sortie = pathlib.Path(
        sys.argv[2]
        if len(sys.argv) > 2
        else f"/tmp/instantane_revision_v150_{mode}.json"
    )
    etat = {"mode": mode, "scelles": {}, "livres": {}, "sources": {}}
    for c in SCELLES:
        etat["scelles"][str(c.relative_to(REPO))] = sha256(c)
    for c in LIVRES:
        etat["livres"][str(c.relative_to(REPO))] = sha256(c)
    for c in SOURCES:
        etat["sources"][str(c.relative_to(REPO))] = sha256(c)
    with open(sortie, "w", encoding="utf-8") as f:
        json.dump(etat, f, indent=2, ensure_ascii=False, sort_keys=True)
    print(f"[{mode}] {len(etat['scelles'])} scellés, "
          f"{len(etat['livres'])} livrés, {len(etat['sources'])} sources "
          f"—> {sortie}")


if __name__ == "__main__":
    main()
