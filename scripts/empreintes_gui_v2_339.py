#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""empreintes_gui_v2_339.py — L'EMPREINTES-GUI DE L'ÉDITION v2 (l'Entrée
339) : les sha256 recalculés des pièces FINALES du kit v2 (le GUI, le
lanceur, le livre, les DEUX correctifs + LES DIX-SEPT pièces du verrou),
le format de l'édition v1 (deux espaces de séparation, lisible à
certutil). Rien n'est recopié : tout est recalculé depuis les octets."""
import hashlib
import pathlib

V2 = pathlib.Path("/home/z/my-project/download/TRIADE_gui_unite02_d210_v2")
FICHIER = V2 / "EMPREINTES-GUI-UNITE02-D210-1CLIC.txt"


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


LIVRES = [
    ("triade_run_unite02_d210_gui.py",
     "le GUI v2 (un seul fichier, tkinter stdlib — LE JUGE RÉPARÉ)"),
    ("LANCER-RUN-UNITE02-D210-1CLIC.bat",
     "le lanceur au double-clic (l'édition v2 nommée en tête)"),
    ("LISEZMOI-RUN-UNITE02-D210-1CLIC.txt",
     "le livre du kit (l'édition v2 — la correction de la 339)"),
    ("CORRECTIF-T0-UNITE01-D210-20261118.txt",
     "le défaut T0 nommé sur pièces (INCHANGÉ — celui du kit v1)"),
    ("CORRECTIF-JUGE-V2-UNITE02-D210-20261118.txt",
     "le défaut du juge nommé à la 338, la réparation livrée"),
]

PIECES = [
    "GRAINE-D210.txt",
    "LANCEUR-UNITE-02-T.bat",
    "LISEZMOI-KIT-UNITE-01-D210.txt",
    "NOTE-REPRISE-ATELIER.txt",
    "brouillon-loupe-02-lire.asm",
    "journal-tokens-d210.jsonl",
    "loupe.exe",
    "notation-loupe-02-lire.asm",
    "scenario-unite02.py",
    "source-loupe-02-C.c",
    "temoin-1.bin",
    "temoin-384.bin",
    "temoin-3f.bin",
    "tests-loupe-02-C.md",
    "vide.bin",
    "EMPREINTES-KIT-UNITE-01-D210.txt",
    "EMPREINTES-PIECES-RUN.txt",
]

NOTES = {
    "scenario-unite02.py": "LE JUGE v2 RÉPARÉ (302fa3a1…, R_JOURNAL = "
                           "0xE4A0 — la vérité du layout)",
    "EMPREINTES-PIECES-RUN.txt": "la gravure v2 (la ligne du juge v2 "
                                 "gravée)",
}

lignes = [
    "EMPREINTES-GUI-UNITE02-D210-1CLIC — les pièces du kit GUI 1-clic",
    "(l'édition v2 du 18/11/2026 au soir — LE JUGE RÉPARÉ : la correction",
    "commandée à la 339, la cause nommée à la 338 ; la console « certutil",
    "-hashfile <fichier> SHA256 » recoupe chaque ligne chez vous)",
    "======================================================================"
    "========",
    "",
    "LE GUI ET SES LIVRES :",
    "",
]
for nom, desc in LIVRES:
    p = V2 / nom
    lignes.append(f"{nom:<46} {p.stat().st_size:>7} o  "
                   f"sha256 {sha256f(p)}")
    lignes.append(f"{'':<46} {desc}")
lignes += ["",
           "LES PIÈCES DU KIT (le verrou du GUI les recoupe à CHAQUE "
           "lancement,",
           "fail-closed) — les QUINZE du kit (le juge v2 à la place du "
           "v1",
           "fautif, les QUATORZE autres INCHANGÉES du 17/11) + les DEUX "
           "gravures :",
           ""]
for nom in PIECES:
    p = V2 / nom
    note = NOTES.get(nom)
    if note:
        lignes.append(f"{nom:<46} {p.stat().st_size:>7} o  "
                       f"sha256 {sha256f(p)}")
        lignes.append(f"{'':<46} {note}")
    else:
        lignes.append(f"{nom:<46} {p.stat().st_size:>7} o  "
                      f"sha256 {sha256f(p)}")
lignes += ["",
           "======================================================================"
           "========",
           "(18/11/2026 au soir, la session de la correction — l'Entrée 339 "
           "du worklog)",
           ""]

FICHIER.write_text("\n".join(lignes), encoding="utf-8", newline="\n")
h = sha256f(FICHIER)
print(f"[empreintes] {FICHIER.name} v2 né : "
      f"{FICHIER.stat().st_size} o, sha256 {h}")
print(f"[à reporter au zip] l'EMPREINTES-GUI vit au kit — "
      f"{len(LIVRES)} livres + {len(PIECES)} pièces listés")
