#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_modules_etendus.py — construit les modules étendus de l'atelier
5ey7gmjra par transformation des modules 89488hblm : chaque transformation est
UNE substitution documentée, le diff intégral gravé à DIFF-MODULES-ETENDUS.txt
(la consignation append-only l'exige)."""
import difflib
import pathlib

AT = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path("/home/z/my-project/depot/atelier-cf3-89488hblm")

TRANSFORMATIONS = [
    # (source, destination, [(ancien, nouveau, cause)])
    ("CF3Python.tla", "CF3PythonEtendu.tla", [
        ("--------------------------- MODULE CF3Python ---------------------------",
         "------------------------ MODULE CF3PythonEtendu ------------------------",
         "le nom du module"),
        (" * CF3Python — LA SÉMANTIQUE PYTHON DE CF3 EN TLA+ : la transcription\n * fidèle de modele_invariant_v150.py (l'instruction 89488hblm, point (a)).",
         " * CF3PythonEtendu — LA SÉMANTIQUE PYTHON DE CF3 ÉTENDUE EN TLA+ : la\n * transcription fidèle de modele_invariant_v153.py (l'instruction 5ey7gmjra\n * — le pendant Python de CF3Etendu.tla : la règle 4 étendue, les douze\n * autres la copie de la v0.15.0).",
         "l'en-tête de généalogie"),
        ("EXTENDS CF3\n", "EXTENDS CF3Etendu\n", "la base étendue"),
        ("\\* 4 : falsifie_conteneur — offert toujours ; EFFECTIF : piège intègre ET\n\\*     canonique (appliquer : if trap_ok and phase == \"canonique\")\nGP_FalsifieConteneur == trap_ok /\\ phase = \"canonique\"",
         "\\* 4 : falsifie_conteneur — L'EXTENSION 5ey7gmjra : offert toujours ;\n\\*     EFFECTIF : piège intègre SEUL (appliquer : if trap_ok — les DEUX\n\\*     phases, la session ouverte comprise : la sentinelle concrète)\nGP_FalsifieConteneur == trap_ok",
         "LA GARDE ÉTENDUE (l'instruction, point 1)"),
    ]),
    ("CF3Equiv.tla", "CF3EquivEtendu.tla", [
        ("--------------------------- MODULE CF3Equiv ---------------------------",
         "------------------------ MODULE CF3EquivEtendu ------------------------",
         "le nom du module"),
        (" * CF3Equiv — L'ÉQUIVALENCE TLA+ ↔ SÉMANTIQUE PYTHON, RÈGLE PAR RÈGLE,",
         " * CF3EquivEtendu — L'ÉQUIVALENCE TLA+ ÉTENDU ↔ SÉMANTIQUE PYTHON\n * ÉTENDUE, RÈGLE PAR RÈGLE (l'instruction 5ey7gmjra : la batterie\n * 89488hblm re-déchargée sur le modèle étendu — les 13 règles, la garde\n * de la règle 4 portant l'extension),",
         "l'en-tête"),
        ("EXTENDS CF3, CF3Python\n", "EXTENDS CF3Etendu, CF3PythonEtendu\n",
         "les bases étendues"),
        ("\\* la règle RÉELLE sur la copie R (zéro retranscription)\nCF3R == INSTANCE CF3 WITH",
         "\\* la règle RÉELLE sur la copie R (zéro retranscription — L'ÉTENDUE)\nCF3R == INSTANCE CF3Etendu WITH",
         "l'instance de la règle réelle étendue"),
        ("\\* la relation PYTHON sur la copie P\nCFP == INSTANCE CF3Python WITH",
         "\\* la relation PYTHON sur la copie P (l'étendue)\nCFP == INSTANCE CF3PythonEtendu WITH",
         "l'instance de la relation Python étendue"),
        ("GT_FalsifieConteneur == trap_ok /\\ phase = \"canonique\"",
         "\\* L'EXTENSION 5ey7gmjra : la garde TLA+ extraite de CF3Etendu.tla\nGT_FalsifieConteneur == trap_ok",
         "la garde extraite étendue"),
    ]),
    ("CF3Translation.tla", "CF3TranslationEtendu.tla", [
        ("------------------------ MODULE CF3Translation ------------------------",
         "--------------------- MODULE CF3TranslationEtendu ---------------------",
         "le nom du module"),
        (" * CF3Translation — LE LEMME DE TRANSLATION ∀δ DÉCHARGÉ MÉCANIQUEMENT\n * (l'instruction 89488hblm, point (c) : « formalise l'argument",
         " * CF3TranslationEtendu — LE LEMME DE TRANSLATION ∀δ SUR LE MODÈLE\n * ÉTENDU (l'instruction 5ey7gmjra, point 2 — le lemme 89488hblm re-déchargé\n * sur la garde étendue de la règle 4 : « formalise l'argument",
         "l'en-tête"),
        ("EXTENDS CF3, CF3Python\n", "EXTENDS CF3Etendu, CF3PythonEtendu\n",
         "les bases étendues"),
        ("CF3T == INSTANCE CF3 WITH", "CF3T == INSTANCE CF3Etendu WITH",
         "l'instance réelle étendue"),
        ("CFPyT == INSTANCE CF3Python WITH", "CFPyT == INSTANCE CF3PythonEtendu WITH",
         "l'instance Python étendue"),
    ]),
]

diffs = []
for src_nom, dst_nom, substitutions in TRANSFORMATIONS:
    texte = (SRC / src_nom).read_text(encoding="utf-8")
    journal = []
    for ancien, nouveau, cause in substitutions:
        if ancien not in texte:
            raise SystemExit(f"[ROUGE] substitution introuvable dans {src_nom}: {cause}")
        texte = texte.replace(ancien, nouveau, 1)
        journal.append(cause)
    (AT / dst_nom).write_text(texte, encoding="utf-8")
    diff = difflib.unified_diff(
        (SRC / src_nom).read_text(encoding="utf-8").splitlines(),
        texte.splitlines(),
        fromfile=f"atelier-cf3-89488hblm/{src_nom}",
        tofile=f"atelier-cf3-5ey7gmjra/{dst_nom}",
        lineterm="", n=2)
    diffs.append("\n".join(diff))
    print(f"[VERT] {dst_nom} — {len(substitutions)} substitutions : "
          + " ; ".join(journal))

(AT / "DIFF-MODULES-ETENDUS.txt").write_text(
    "\n\n".join(diffs) + "\n", encoding="utf-8")
print(f"[VERT] DIFF-MODULES-ETENDUS.txt gravé "
      f"({len(''.join(diffs).splitlines())} lignes de diff)")
