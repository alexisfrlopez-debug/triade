#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Déduplique les paragraphes insérés plusieurs fois (runs partiels du script de révision)."""

from pathlib import Path

DIR = Path("/home/z/my-project/triade/scripts/spec_v040")


def dedup(nom: str, debut_paragraphe: str, marqueur_fin: str):
    """Garde la 1re occurrence du bloc [debut_paragraphe .. marqueur_fin] et
    supprime les duplicates suivants (le bloc se termine par la ligne fin)."""
    p = DIR / nom
    s = p.read_text(encoding="utf-8")
    debut = s.find(debut_paragraphe)
    assert debut >= 0, f"{nom} : paragraphe introuvable"
    copies = []
    i = debut
    while True:
        fin = s.find(marqueur_fin, i)
        if fin < 0:
            break
        fin_ligne = s.find("\n", fin) + 1
        copies.append((i, fin_ligne))
        i = s.find(debut_paragraphe, fin_ligne)
        if i < 0:
            break
    assert copies, f"{nom} : aucune copie complète trouvée"
    # suppression de la fin vers le début (indices stables)
    for d, f in reversed(copies[1:]):
        s = s[:d] + s[f:]
    p.write_text(s, encoding="utf-8")
    print(f"[ok] {nom} : {len(copies)} copie(s) trouvée(s), {len(copies) - 1} supprimée(s)")


# sec-a : paragraphe vision v0.5.0 (se termine par « sur entrées non fiables. »)
dedup("sec-a.tex",
      "La v0.5.0 est la révision du retour du terrain. Les jalons M0 (chaîne artefact), M1",
      "renforcés\nsur entrées non fiables.")

# sec-c : complément pré-versions (se termine par « (§\ref{sec:terrain}). »)
dedup("sec-c.tex",
      "a depuis été vécu deux fois par le cœur natif",
      "(§\\ref{sec:terrain}).")

# vérifications d'unicité globale
verifs = {
    "sec-a.tex": ["La v0.5.0 est la révision du retour du terrain",
                  "\\subsection{Ce que change la v0.5.0}"],
    "sec-b.tex": ["\\subsection{La validation terrain",
                  "\\subsection{Taxonomie étendue"],
    "sec-c.tex": ["a depuis été vécu deux fois"],
    "sec-d.tex": ["\\subsection{Correspondance v0.4.0 $\\to$ v0.5.0}",
                  "D44 consigne la présente révision v0.5.0"],
    "main.tex": ["v0.5.0 — Manuscrit", "spécification v0.5.0", "TRIADE v0.5.0 — spécification"],
    "cover.html": ["Version 0.5.0"],
}
for nom, motifs in verifs.items():
    s = (DIR / nom).read_text(encoding="utf-8")
    for m in motifs:
        n = s.count(m)
        assert n == 1, f"{nom} : {n} × {m!r} (attendu 1)"
    print(f"[ok] {nom} : unicités vérifiées ({len(motifs)})")
print("\nDéduplication terminée — sources v0.5.0 propres.")
