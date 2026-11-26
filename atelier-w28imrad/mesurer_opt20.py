#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OPT-20 — LE BUDGET TOKEN PAR VAGUE (W28IMRAD, prompt 7, geste 4) : le coût
token de la production de la vague 28 mesuré et pré-enregistré comme budget —
la méta-optimisation : le protocole s'optimise lui-même.

LA CONVENTION (nommée, honnête) : la vague PRODUIT des artefacts — les sept
plans gelés, les sept rapports d'atelier, la prose source ajoutée au manuscrit
(la restructuration IMRAD + les travaux connexes + la note de vague + la note
post-édition). Le COÛT TOKEN DE GÉNÉRATION mesuré = le compte de tokens de
cette production autoriée : (a) le compte CL100K (tiktoken, la convention
publiée depuis OPT-05) ; (b) LE COMPTE NATIF lu du bord (le champ usage de
l'appel qui porte le texte — la convention des OPT-14/16 : le compte est le
LOG, jamais une estimation). La cible BUDGET pré-enregistrée pour la vague
suivante : ≤ le compte natif de la présente (aucun chiffre fabriqué : le bord
rend le compte, la session le consigne).
"""
import json
import pathlib
import re
import subprocess
import sys

R = pathlib.Path(__file__).resolve().parents[1]
ICI = pathlib.Path(__file__).resolve().parent

FICHIERS = [
    # les sept plans gelés de la vague 28
    R / "PLAN-W28VAES.md", R / "PLAN-W28OPT16.md", R / "PLAN-W28HARNAIS.md",
    R / "PLAN-W28ATTR.md", R / "PLAN-W28TERRAIN.md", R / "PLAN-W28RLVR.md",
    R / "PLAN-W28IMRAD.md",
    # les sept rapports d'atelier
    R / "atelier-w28vaes/rapport.txt",
    R / "atelier-w28opt16/rapport.txt",
    R / "atelier-w28harnais/rapport.txt",
    R / "atelier-w28attr/rapport.txt",
    R / "atelier-w28terrain/rapport.txt",
    R / "atelier-w28rlvr/rapport.txt",
    R / "atelier-w28imrad/rapport.txt",
]
FICHIERS = [f for f in FICHIERS if f.exists()]


def cl100k(texte):
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(texte))


def natif(texte):
    """le compte natif : le TEXTE PORTÉ PAR L'APPEL — le champ usage du bord
    rend prompt_tokens (la convention OPT-14/16 : le compte est le LOG, jamais
    une estimation). La tranche EST le prompt."""
    r = subprocess.run(["z-ai", "chat", "--prompt", texte,
                        "--system", "renvoie uniquement le mot : compte",
                        "-o", str(ICI / "_opt20_out.json")],
                       capture_output=True, text=True, timeout=180)
    try:
        d = json.loads((ICI / "_opt20_out.json").read_text())
        u = d.get("usage") or {}
        prompt_tokens = int(u.get("prompt_tokens", 0))
        return prompt_tokens, d
    except Exception as e:
        return None, {"erreur": str(e) + " / " + (r.stderr or "")[:100]}


def main():
    corpus = []
    for f in FICHIERS:
        t = f.read_text(encoding="utf-8")
        corpus.append(f"### {f.name}\n{t}")
    texte = "\n\n".join(corpus)
    # la prose source AJOUTÉE au manuscrit (le diff de la restructuration) :
    # les ajouts identifiés au restructurer (l'en-tête + les trois paragraphes
    # de travaux connexes + la note post-édition v0.33.0 + la note de vague)
    manuscrit = (R / "edition-v0230" / "main.tex").read_text(encoding="utf-8")
    for marqueur_debut, marqueur_fin in [
        ("%  TRIADE — édition académique v0.33.0", "%  L'édition v0.32.0 est"),
        ("\\paragraph{Structured outputs and constrained decoding.}", "\\paragraph{Design by contract"),
        ("\\subsection{Post-edition note (v0.33.0):", "\\subsection{Post-edition note (v0.31.0)"),
        ("\\item v0.33.0 (26 Nov 2026) --- the present edition, the twenty-eighth wave:", "\\end{itemize}"),
        ("\\subsection{The four-arm decomposition and the pre-registered", "\n\\paragraph{Lexicographic"),
    ]:
        try:
            i = manuscrit.index(marqueur_debut)
            j = manuscrit.index(marqueur_fin, i) if marqueur_fin != "\n\\paragraph{Lexicographic" else i + 400
            corpus.append(f"### main.tex (extrait ajouté)\n{manuscrit[i:j]}")
        except ValueError:
            pass
    texte = "\n\n".join(corpus)

    n_cl = cl100k(texte)
    print(f"[opt20] la production autoriée de la vague 28 : {len(corpus)} pièces, "
          f"{len(texte)} caractères — CL100K : {n_cl} tokens")

    # le compte natif : le bord rend le champ usage — le texte porté par tranches
    # de 60 000 caractères (la limite du champ), le compte sommé, la convention
    # nommée (le prompt système minimal, le compte rendu du bord)
    total_natif = 0
    for k in range(0, len(texte), 60000):
        chunk = texte[k:k + 60000]
        pt, d = natif(chunk)
        if pt is None:
            print(f"[opt20] ROUGE : le bord n'a pas rendu le compte — {d}")
            sys.exit(2)
        total_natif += pt
    print(f"[opt20] le compte NATIF (le champ usage du bord, {len(texte)} caractères) : "
          f"{total_natif} tokens")

    doc = {"convention": "la production autoriée de la vague (plans + rapports + prose ajoutée au manuscrit)",
           "pieces": len(corpus), "caracteres": len(texte),
           "cl100k": n_cl, "natif_usage": total_natif,
           "budget_vague_suivante": f"≤ {total_natif} tokens natifs (la production de la vague 28)",
           "fichiers": [str(f.relative_to(R)) for f in FICHIERS]}
    (ICI / "opt20-resultat.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print("[opt20] opt20-resultat.json écrit — la cible posée pour la vague suivante")


if __name__ == "__main__":
    main()
