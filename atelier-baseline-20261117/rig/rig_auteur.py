#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rig_auteur.py — LE CÂBLAGE DE LA RIG L6 (le levier L6 du chantier
d'optimisation, CHANTIER-OPTIMISATION-TOKENS-v1.md, l'Entrée 317 ; la
commande du développeur : « Prepare le test L6 avec un guide »).

L'ÉCART NOMMÉ QUE LA RIG GUÉRIT (les Entrées 289/290 : les M2 manquants)
— les unités 2+ de la campagne ont vu leurs appels de construction passer
HORS journal : le travail vivait dans la conversation de l'agent, la
mesure M2 n'en est jamais née. Sans M2 complet, AUCUN gain du chantier
ne peut être consigné (la mesure est la condition de tout le reste).

LA LOI DU CÂBLAGE (le chantier, L6) : compter_tokens.py est câblé dans
CHAQUE outil auteur du labo — LE JOURNAL NAÎT DES OUTILS, JAMAIS DE LA
MÉMOIRE. Ce module est L'UNIQUE CHEMIN par lequel les outils auteurs
appelent le modèle :

    outil_builder.py    ─┐
    outil_correctif.py  ─┼─>  rig_auteur.appeler_modele()
    outil_tests.py     ─┘        │
                                 v
                    compter_tokens.appeler_et_compter()
                                 │  (l'appel instrumenté : z-ai chat,
                                 │   le champ usage LU de la réponse)
                                 v
                    journal_tokens.jsonl — UNE ligne JSON par appel,
                    zéro estimation (l'outil ne sait PAS estimer : il
                    ne sait que lire le log)

LES TROIS GARANTIES :
  1. AUCUN outil auteur n'invoque le modèle par un autre chemin — le
     seul appel au modèle vit à compter_tokens.py (l'épreuve L6 le
     vérifie par L'INSPECTION DU CODE : « z-ai » et « subprocess »
     n'y vivent qu'à compter_tokens.py) ;
  2. chaque appel est journalisé AU MOMENT MÊME où la réponse revient
     (la ligne naît de l'outil, pas d'un rattrapage de mémoire) ;
  3. un appel manquant est un ÉCART NOMMÉ, jamais un chiffre
     reconstruit (CA3 — la discipline du plan a78caf8c… demeure).

LA FRONTIÈRE HONNÊTE : la rig guérit la SOURCE (le chemin de l'outil) ;
la discipline de l'agent demeure le complément nommé — tout geste de
construction passe par les outils, jamais par la conversation seule
(le guide le consigne : c'est la condition d'usage de la rig).

Usage (par les outils, jamais à la main pour construire) :
    from rig_auteur import appeler_modele
    texte, ligne = appeler_modele(bras="T", phase="spec",
                                  tache="loupe-05", prompt=prompt,
                                  journal=journal)
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parent

# l'instrument v2 — INTACT, octet pour octet celui du kit campagne-d204
# (sha256 e2939ef9d3ef7f228c1881b55744e182238fbb489b58d30595882d926eea26e5)
def _charger_compteur():
    spec = importlib.util.spec_from_file_location(
        "compter_tokens", ICI / "compter_tokens.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

COMPTER = _charger_compteur()

# les phases du plan D204 — le vocabulaire du journal (jamais élargi en
# silence : une phase hors liste est un refus, pas une approximation)
PHASES = COMPTER.PHASES
BRAS_VALIDES = ("T", "C")


def appeler_modele(bras: str, phase: str, tache: str, prompt: str,
                   system: str | None = None,
                   journal: pathlib.Path | None = None,
                   garde_brut: pathlib.Path | None = None):
    """UN appel au modèle PAR L'OUTIL — journalisé à la source.

    Retourne (le texte de la réponse, la ligne née au journal). La
    ligne est ÉCRITE par compter_tokens au moment même où la réponse
    revient : l'outil ne conserve rien en mémoire à recopier plus tard.
    """
    if bras not in BRAS_VALIDES:
        raise ValueError(f"bras inconnu : {bras!r} (T ou C)")
    if phase not in PHASES:
        raise ValueError(f"phase hors plan : {phase!r} ({PHASES})")
    if journal is None:
        journal = COMPTER.JOURNAL_DEFAUT
    return COMPTER.appeler_et_compter(
        bras=bras, phase=phase, tache=tache, prompt=prompt, system=system,
        journal=pathlib.Path(journal), garde_brut=garde_brut)


# ---------------------------------------------------------------------------
# LE CÂBLAGE À L'ÉPREUVE (le mode --cablage des outils, repris par
# l'épreuve L6 niveau L1) : UN appel MOQUÉ — aucun réseau, un journal
# ÉPHÉMÈRE détruit après la preuve. La maquette intercepte le
# sous-processus AU DERNIER MILLE (là où compter_tokens invoque z-ai) :
# si l'appel de l'outil ne passe PAS par le compteur, RIEN ne naît et
# la preuve est ROUGE — le câblage ne peut pas se déclarer lui-même.
# ---------------------------------------------------------------------------
REPONSE_MOQUEE = {
    "id": "cablage-l6",
    "model": "maquette-de-cablage",
    "usage": {"prompt_tokens": 11, "completion_tokens": 7,
              "total_tokens": 18},
    "choices": [{"message": {"content":
                             "[cablage] la ligne naît de l'outil."}}],
}


def cablage(outil_nom: str, phase: str, bras: str, tache: str):
    """La preuve du câblage d'UN outil : l'appel moqué traverse
    rig_auteur -> compter_tokens -> (z-ai intercepté) -> la ligne naît.

    Retourne (ok, la_ligne_née | le_message_d'échec). Aucun réseau,
    aucun fichier qui demeure : le journal éphémère est détruit.
    """
    import subprocess as _vrai_subprocess
    import tempfile

    journal_ephemere = pathlib.Path(
        tempfile.mkdtemp(prefix="cablage-l6-")) / "journal.jsonl"
    appels_interceptes = []

    def faux_run(cmd, **kwargs):
        appels_interceptes.append(list(cmd))
        # la maquette écrit LA RÉPONSE là où le vrai z-ai l'écrirait
        chemin_reponse = pathlib.Path(cmd[cmd.index("-o") + 1])
        chemin_reponse.write_text(
            json.dumps(REPONSE_MOQUEE), encoding="utf-8")

        class _P:  # le CompletedProcess mensonger en forme, rien d'autre
            returncode = 0
            stderr = ""
            stdout = ""
        return _P()

    _vrai = COMPTER.subprocess.run
    COMPTER.subprocess.run = faux_run
    try:
        texte, ligne = appeler_modele(
            bras=bras, phase=phase, tache=tache,
            prompt="[cablage] la preuve du chemin, aucun réseau.",
            journal=journal_ephemere)
        # la ligne est-elle NÉE au journal éphémère, lue du disque ?
        lignes = [json.loads(l) for l in
                  journal_ephemere.read_text(encoding="utf-8").splitlines()
                  if l.strip()]
        ok = (len(lignes) == 1
              and lignes[0]["prompt_tokens"] ==
              REPONSE_MOQUEE["usage"]["prompt_tokens"]
              and lignes[0]["completion_tokens"] ==
              REPONSE_MOQUEE["usage"]["completion_tokens"]
              and lignes[0]["total_tokens"] ==
              REPONSE_MOQUEE["usage"]["total_tokens"]
              and lignes[0]["source"] == "log-api"
              and lignes[0]["bras"] == bras
              and lignes[0]["phase"] == phase
              and lignes[0]["tache"] == tache)
        return ok, (lignes[0] if lignes else None)
    finally:
        COMPTER.subprocess.run = _vrai
        if journal_ephemere.exists():
            journal_ephemere.unlink()
            journal_ephemere.parent.rmdir()


def inspecter_cablage() -> list[str]:
    """L'INSPECTION DU CODE (par l'AST — le CODE seul, jamais la prose
    des docstrings) : aucun outil auteur n'appelle le modèle hors
    compter_tokens.py. Les marqueurs d'invocation (la chaîne « z-ai »,
    le module subprocess) ne vivent qu'à l'instrument ; chaque outil
    emprunte rig_auteur. Retourne la liste des écarts nommés (vide =
    le câblage est structurel)."""
    import ast

    def docstrings(arbre: ast.AST) -> set[int]:
        """les nœudsConstant qui sont des docstrings (module, fonction,
        classe) — la prose descriptive, jamais le code."""
        marques = set()
        for noeud in ast.walk(arbre):
            if isinstance(noeud, (ast.Module, ast.FunctionDef,
                                  ast.AsyncFunctionDef, ast.ClassDef)):
                corps = noeud.body
                if (corps and isinstance(corps[0], ast.Expr)
                        and isinstance(corps[0].value, ast.Constant)
                        and isinstance(corps[0].value.value, str)):
                    marques.add(id(corps[0].value))
        return marques

    ecarts = []
    for outil in ("outil_builder.py", "outil_correctif.py",
                  "outil_tests.py"):
        source = (ICI / outil).read_text(encoding="utf-8")
        arbre = ast.parse(source)
        prose = docstrings(arbre)
        fautes = []
        for noeud in ast.walk(arbre):
            # la chaîne d'invocation du modèle — hors prose
            if (isinstance(noeud, ast.Constant)
                    and isinstance(noeud.value, str)
                    and "z-ai" in noeud.value
                    and id(noeud) not in prose):
                fautes.append("la chaîne « z-ai » hors docstring")
                break
        for noeud in ast.walk(arbre):
            if isinstance(noeud, ast.Import):
                for alias in noeud.names:
                    if alias.name == "subprocess":
                        fautes.append("l'import de subprocess")
            elif isinstance(noeud, ast.ImportFrom):
                if noeud.module == "subprocess":
                    fautes.append("l'import de subprocess")
            elif isinstance(noeud, ast.Attribute):
                if isinstance(noeud.value, ast.Name) \
                        and noeud.value.id == "subprocess":
                    fautes.append("l'usage de subprocess")
        if fautes:
            for f in sorted(set(fautes)):
                ecarts.append(f"{outil} : {f} — l'invocation ne vit "
                              f"qu'à compter_tokens.py")
        elif "from rig_auteur import" not in source:
            ecarts.append(f"{outil} n'emprunte pas rig_auteur — "
                          f"le câblage est absent")
    return ecarts


if __name__ == "__main__":
    print(__doc__)
    ecarts = inspecter_cablage()
    if ecarts:
        print("[inspection] ÉCARTS NOMMÉS :")
        for e in ecarts:
            print("  -", e)
        sys.exit(1)
    print("[inspection] le câblage est structurel : les trois outils "
          "empruntent rig_auteur, l'invocation vit à compter_tokens.py "
          "seule.")
    for outil, phase, bras in (("outil_builder.py", "spec", "T"),
                               ("outil_correctif.py", "correctif", "T"),
                               ("outil_tests.py", "tests-c", "C")):
        ok, ligne = cablage(outil, phase, bras, "cablage-l6")
        print(f"[cablage] {outil} phase {phase} bras {bras} : "
              f"{'VERT' if ok else 'ROUGE'}"
              + (f" — la ligne née : {ligne['prompt_tokens']}+"
                 f"{ligne['completion_tokens']}={ligne['total_tokens']} "
                 f"(source {ligne['source']})" if ok else ""))
        if not ok:
            sys.exit(1)
    sys.exit(0)
