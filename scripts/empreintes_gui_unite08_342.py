#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""empreintes_gui_unite08_342.py — L'EMPREINTES-GUI DE L'ÉDITION v1 de
l'unité 02 D210 (loupe-08 ligne × bras T — l'Entrée 342) : les sha256
recalculés des pièces FINALES du kit GUI (le GUI, le lanceur, le
livre + LES QUATORZE pièces du verrou), le format de l'édition v1 de
la 337 (deux espaces de séparation, lisible à certutil). Rien n'est
recopié : tout est recalculé depuis les octets — APRÈS les épreuves
(selftest 15 VERT, fonctionnelle 9 VERT, fumée Xvfb 7 VERT), les
octets finaux font foi."""
import hashlib
import pathlib

KIT = pathlib.Path("/home/z/my-project/download/"
                   "TRIADE_gui_unite08_d210_v1")
FICHIER = KIT / "EMPREINTES-GUI-UNITE08-D210-1CLIC.txt"


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


LIVRES = [
    ("triade_run_unite08_d210_gui.py",
     "le GUI v1 (un seul fichier, tkinter stdlib — la logique du "
     "précédent 339 INCHANGÉE, la SECTION A de l'unité loupe-08)"),
    ("LANCER-RUN-UNITE08-D210-1CLIC.bat",
     "le lanceur au double-clic (l'édition v1 nommée en tête, CRLF)"),
    ("LISEZMOI-RUN-UNITE08-D210-1CLIC.txt",
     "le livre du kit (l'édition v1 — la deuxième unité, l'attendu "
     "des DIX verdicts)"),
]

PIECES = [
    "GRAINE-D210.txt",
    "LANCEUR-UNITE-08-T.bat",
    "LISEZMOI-KIT-UNITE-02-D210.txt",
    "brouillon-loupe-08-ligne.asm",
    "journal-tokens-d210.jsonl",
    "garde-brut-d210.jsonl",
    "loupe.exe",
    "notation-loupe-08-ligne.asm",
    "proxy.exe",
    "scenario-unite08.py",
    "source-loupe-08-C.c",
    "temoin-3f.bin",
    "tests-loupe-08-C.md",
    "EMPREINTES-KIT-UNITE-02-D210.txt",
]

NOTES = {
    "loupe.exe": ("LA PIÈCE de campagne (le slot loupe-08 RVA 0x49C0 "
                  "porte la notation D210, 260 o cristallisés — "
                  "4498b7fa…)"),
    "scenario-unite08.py": ("LE JUGE D204 INCHANGÉ (44384f5d…, la "
                            "version corrigée — le lecteur « sha256  "
                            "nom », la feuille pure)"),
    "EMPREINTES-KIT-UNITE-02-D210.txt": (
        "la gravure du kit (née parsée — le défaut T0 de l'unité 01 "
        "ne se reproduit pas)"),
    "proxy.exe": "le scellé de l'ère (la première ligne du doré V1)",
}

lignes = [
    "EMPREINTES-GUI-UNITE08-D210-1CLIC — les pièces du kit GUI 1-clic",
    "(l'édition v1 du 18/11/2026 — LA DEUXIÈME UNITÉ D210 : loupe-08 "
    "ligne × bras T,",
    "la séquence tirée de la graine D217, jamais re-tirée ; le kit né "
    "au labo à l'Entrée 341 ;",
    "la console « certutil -hashfile <fichier> SHA256 » recoupe chaque "
    "ligne chez vous)",
    "======================================================================"
    "========",
    "",
    "LE GUI ET SES LIVRES :",
    "",
]
for nom, desc in LIVRES:
    p = KIT / nom
    lignes.append(f"{nom:<46} {p.stat().st_size:>7} o  "
                   f"sha256 {sha256f(p)}")
    lignes.append(f"{'':<46} {desc}")
lignes += ["",
           "LES PIÈCES DU KIT (le verrou du GUI les recoupe à CHAQUE "
           "lancement,",
           "fail-closed) — les QUATORZE du kit (les DOUZE pièces + la "
           "gravure +",
           "le livre) :",
           ""]
for nom in PIECES:
    p = KIT / nom
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
           "(18/11/2026, la session du GUI de l'unité 02 — l'Entrée 342 "
           "du worklog)",
           ""]

FICHIER.write_text("\n".join(lignes), encoding="utf-8", newline="\n")
h = sha256f(FICHIER)
print(f"[empreintes] {FICHIER.name} v1 né : "
      f"{FICHIER.stat().st_size} o, sha256 {h}")
print(f"[à reporter au zip] l'EMPREINTES-GUI vit au kit — "
      f"{len(LIVRES)} livres + {len(PIECES)} pièces listés "
      f"(17 + la gravure GUI elle-même)")
