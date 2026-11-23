#!/usr/bin/env python3
"""surcout_gouvernance.py — atelier IO3UH37CJ (la vague 16).

LE SURCOÛT TOKEN DE GOUVERNANCE PAR CHANGEMENT (sceau, linter, cristallisation),
publié À CÔTÉ DES BUDGETS 627 / 674 / 2 200 — et la réduction mesurée quand la
surface de gouvernance lue par l'agent est COMPRESSÉE.

La question honnête : la gouvernance coûte-t-elle plus cher que le changement
qu'elle protège ? La réponse se mesure, elle ne se décrète pas.
"""

import argparse
import json
import os
import sys

try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")

    def tokens(texte: str) -> int:
        return len(_ENC.encode(texte, disallowed_special=()))
    METHODE = "tiktoken cl100k_base (le compte exact)"
except Exception:                                    # pragma: no cover
    def tokens(texte: str) -> int:
        return max(1, len(texte.encode("utf-8")) // 4)
    METHODE = "l'estimation octets/4 (tiktoken absent — l'écart nommé)"

# Les budgets de changement publiés (c/octet@4096 → tokens par changement)
BUDGETS = {"m4": 627, "m6": 674, "headline": 2200}

# La surface de gouvernance lue par l'agent à CHAQUE changement
PIECES = [
    ("v06/sceau_I.py", "le sceau de l'Intention (la gardienne des 14 arbres)"),
    ("scripts/vague14/linter_v232.py", "le linter v2 (les cinq classes + les négatifs)"),
    ("atelier-entrelacement-2sown2h3z/piloter_entrelacement.py", "la différentielle du couloir"),
    ("atelier-audit-splits-am9d6o2th/auditer_splits.py", "l'audit d'étanchéité des splits"),
]


def lire(chemin):
    try:
        with open(chemin, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def extraire_invariants(texte: str) -> str:
    """La forme COMPRESSÉE : les docstrings, les signatures et les constantes —
    la surface qu'un agent a réellement besoin de lire pour obéir."""
    sortie = []
    for ligne in texte.splitlines():
        s = ligne.strip()
        if s.startswith('"""') or s.startswith("#"):
            continue
        if s.startswith(("def ", "class ", "ARBRES", "CONSTANTE", "SHA256", "RVA_", "N_MIN",
                         "N_MAX", "PROPORTION", "GRAINE", "PIECES", "MEM_", "PAGE_")):
            sortie.append(s)
    return "\n".join(sortie)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default=".", help="la racine du dépôt")
    ap.add_argument("--registre", default=None)
    args = ap.parse_args()

    print("=== LE SURCOÛT TOKEN DE GOUVERNANCE PAR CHANGEMENT ===")
    print(f"  la méthode : {METHODE}")
    print(f"  les budgets de changement : {BUDGETS}")
    print()

    total, total_compact = 0, 0
    lignes = []
    for rel, role in PIECES:
        chemin = os.path.join(args.racine, rel)
        texte = lire(chemin)
        if texte is None:
            print(f"  {rel:52s} ABSENT (l'écart nommé)")
            continue
        t = tokens(texte)
        compact = extraire_invariants(texte)
        tc = tokens(compact)
        reduction = (1 - tc / t) * 100 if t else 0
        total += t
        total_compact += tc
        lignes.append((rel, role, t, tc, reduction))
        print(f"  {rel:52s} {t:6d} tokens   compact {tc:5d}  (-{reduction:4.1f} %)")
        print(f"    {role}")

    print()
    print(f"  LA SURFACE TOTALE     : {total:6d} tokens par changement")
    print(f"  LA FORME COMPRESSÉE   : {total_compact:6d} tokens  "
          f"(-{(1 - total_compact / total) * 100 if total else 0:.1f} %)")
    print()
    print("  LA LECTURE (le surcoût rapporté aux budgets) :")
    for nom, budget in BUDGETS.items():
        part = (total / budget * 100) if budget else 0
        print(f"    {nom:9s} budget {budget:5d} → la gouvernance en coûte {part:6.1f} % "
              f"{'(plus cher que le changement)' if part > 100 else ''}")
    print()
    print("  LA RÈGLE : la gouvernance se lit À CHAQUE changement — c'est pourquoi sa")
    print("  compression est une mesure de performance, pas un confort de lecture.")

    if args.registre:
        with open(args.registre, "w", encoding="utf-8") as f:
            json.dump({
                "schema": "TRIADE-SURCOUT-GOUVERNANCE-v1",
                "methode": METHODE, "budgets": BUDGETS,
                "pieces": [{"fichier": r, "role": ro, "tokens": t,
                            "tokens_compact": tc, "reduction_pct": round(red, 2)}
                           for r, ro, t, tc, red in lignes],
                "total": total, "total_compact": total_compact,
            }, f, ensure_ascii=False, indent=2)
        print(f"  le registre : {args.registre}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
