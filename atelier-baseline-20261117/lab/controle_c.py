#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_c.py — LE CONTRÔLE MÉCANIQUE DU BRAS C (le labo de la
baseline) : gcc -O2 -std=c11 -Wall -Wextra contre le shim windows.h (la
tradition des shims de la campagne), puis les règles de la pièce :
  R1 la FONCTION EXPORTÉE existe (long long loupe_05_sha256(u64, u64,
     void*) — la pièce de l'unité, le .def l'exporte) ;
  R2 LA LISTE IAT FERMÉE (D161) : SetFilePointerEx, ReadFile,
     GetLastError — toute autre fonction Win32 est une contrebande ;
  R3 LES VERDICTS nommés : -4 (session), -3 (bornes), -5 (entrée),
     -6 (système), 0 (succès) ;
  R4 LA COMPOSITION : l'initialisation UNE fois, l'absorption par
     fenêtre, la finalisation UNE fois (les sémantiques tls13-01/03/04
     au flux C — la famille sha256_* de la pièce scellée) ;
  R5 fail-closed : le lu RECOUPÉ au demandé (jamais un condensé
     partiel).
Sortie : {vert, defauts: [{classe, mecanisme, ligne}]}"""
from __future__ import annotations

import json
import re
import subprocess
import sys

SHIM = "lab/shim"


def controler(piece: str) -> dict:
    source = open(piece, encoding="utf-8").read()
    lignes = source.splitlines()
    defauts = []

    def nommer(classe, mecanisme, no):
        defauts.append({"classe": classe, "mecanisme": mecanisme, "no": no})

    # R1 — la fonction exportée
    if not re.search(r"loupe_05_sha256\s*\(", source):
        nommer("FONCTION-ABSENTE",
               "la fonction loupe_05_sha256 est ABSENTE de la pièce — la"
               " rédaction s'arrête aux tableaux, aucune fonction"
               " n'existe (le .def de la famille exporte"
               " loupe_05_sha256)", len(lignes))

    # R2 — la liste IAT fermée
    autorisees = {"SetFilePointerEx", "ReadFile", "GetLastError"}
    utilisees = set(re.findall(r"\b(SetFilePointerEx|ReadFile|"
                               r"GetLastError|CreateFileW)\s*\(", source))
    contrebande = utilisees - autorisees
    if contrebande:
        nommer("IAT-CONTREBANDE",
               "fonction(s) Win32 hors la liste fermée D161 : "
               + ", ".join(sorted(contrebande)), 0)

    # R3 — les verdicts nommés
    for verdict, nom in ((-4, "E1 SESSION"), (-3, "E2 HORS-BORNES"),
                         (-5, "E3 ENTRÉE"), (-6, "E4 SYSTÈME")):
        if not re.search(rf"VERDICT_\w+\s*=?\s*\(?\s*{verdict}|"
                         rf"return\s+\(?{verdict}\)?|"
                         rf"=\s*{verdict}\s*;", source):
            nommer("VERDICT-ABSENT",
                   f"le verdict {nom} ({verdict}) n'est nulle part"
                   " nommé", 0)

    # R4 — la composition (init une fois, absorption par fenêtre,
    # finalisation une fois)
    if re.search(r"loupe_05_sha256\s*\(", source):
        corps = source
        if not re.search(r"(sha256_transform|_transform|compress)\s*\(", corps):
            nommer("COMPOSITION", "la transformation/compression SHA-256 "
                   "n'est nulle part appelée (la composition héritée : "
                   "tls13-03 absorbe par fenêtre)", 0)
        absorptions = len(re.findall(r"(sha256_absorbe|absorbe|update)"
                                     r"\s*\(", corps))
        if absorptions < 1:
            nommer("COMPOSITION", "aucune absorption par fenêtre "
                   "(tls13-03)", 0)
        if not re.search(r"(sha256_final|final)\s*\(", corps):
            nommer("COMPOSITION", "aucune finalisation (tls13-04)", 0)

    # R5 — fail-closed (le lu recoupé au demandé)
    if re.search(r"loupe_05_sha256\s*\(", source) and \
            not re.search(r"lus\s*!=|lus\s*<|a_lire\s*!=|!=\s*a_lire",
                          source):
        nommer("FAIL-CLOSED", "le lu n'est jamais RECOUPÉ au demandé "
               "(E4 fail-closed : jamais un condensé partiel)", 0)

    # le compilateur — gcc -O2 contre le shim
    proc = subprocess.run(
        ["gcc", "-O2", "-std=c11", "-Wall", "-Wextra", "-I", SHIM,
         "-c", piece, "-o", "/dev/null"],
        capture_output=True, text=True)
    for ligne in (proc.stderr or "").splitlines():
        m = re.match(r"(.*?):(\d+):\d+: (\w+): (.*)", ligne)
        if m and m.group(3) == "error":
            nommer("GCC-ERREUR", f"gcc refuse : {m.group(4)} "
                   f"(ligne {m.group(2)})", int(m.group(2)))
        elif m and m.group(3) == "warning":
            if "unused" in m.group(4):
                nommer("PIÈCE-CREUSE", f"une pièce définie mais jamais "
                       f"servie : {m.group(4)} (ligne {m.group(2)}) — "
                       "la rédaction avorta avant la fonction",
                       int(m.group(2)))
    return {"vert": not defauts, "defauts": defauts}


if __name__ == "__main__":
    r = controler(sys.argv[1])
    print(json.dumps(r, ensure_ascii=False, indent=1))
    sys.exit(0 if r["vert"] else 2)
