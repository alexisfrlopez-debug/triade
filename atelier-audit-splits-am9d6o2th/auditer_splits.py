#!/usr/bin/env python3
"""auditer_splits.py — atelier AM9D6O2TH (la vague 16).

L'audit d'étanchéité des splits du corpus d'entraînement.
L'UNITÉ est l'IDENTIFIANT DE CONTRAT (loupe-XX, tls13-XX, sys-XX), jamais
l'instance de tâche : deux campagnes (v3, v4) qui portent le même contrat
sont LE MÊME contrat pour l'étanchéité.

Déterministe, lecture seule : aucune écriture dans le dataset.
Code de sortie : 0 = étanche, 3 = fuite inter-splits constatée.
"""

import argparse
import json
import os
import re
import sys

RE_CONTRAT = re.compile(r"^(loupe-\d+|tls13-\d+|sys-\d+)\s*·", re.MULTILINE)
SPLITS = ("train", "dev", "test")


def contrat_id(enreg: dict):
    """L'identifiant de contrat, depuis le texte du contrat puis le champ bloc."""
    texte = enreg.get("contrat", "")
    m = RE_CONTRAT.search(texte)
    if m:
        return m.group(1)
    bloc = enreg.get("bloc", "")
    m = re.match(r"^((?:loupe|tls13|sys)-\d+)", bloc)
    return m.group(1) if m else None


def charger(dataset: str):
    """-> {split: [enregistrements]} — l'ordre du fichier est conservé."""
    corps = {}
    for split in SPLITS:
        chemin = os.path.join(dataset, f"{split}.jsonl")
        lignes = []
        with open(chemin, encoding="utf-8") as f:
            for ligne in f:
                if ligne.strip():
                    lignes.append(json.loads(ligne))
        corps[split] = lignes
    return corps


def analyser(corps):
    par_split = {}      # split -> {contrat: [triple]}
    sans_contrat = {}   # split -> [triple]
    for split, enregistrements in corps.items():
        table = {}
        vrac = []
        for e in enregistrements:
            cid = contrat_id(e)
            if cid is None:
                vrac.append(e.get("triple", "?"))
            else:
                table.setdefault(cid, []).append(e.get("triple", "?"))
        par_split[split] = table
        sans_contrat[split] = vrac
    return par_split, sans_contrat


def fuites(par_split):
    """Toute paire (split_a, split_b) partageant au moins un contrat."""
    constats = []
    for i, a in enumerate(SPLITS):
        for b in SPLITS[i + 1:]:
        # entraînement contre évaluation : la fuite qui compte
            communs = sorted(set(par_split[a]) & set(par_split[b]))
            if communs:
                constats.append({"a": a, "b": b, "contrats": communs,
                                 "n": len(communs)})
    return constats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="dataset")
    ap.add_argument("--sortie", default=None, help="registre JSON")
    args = ap.parse_args()

    corps = charger(args.dataset)
    par_split, sans_contrat = analyser(corps)
    constats = fuites(par_split)

    print("=== L'AUDIT D'ÉTANCHÉITÉ DES SPLITS (l'unité : l'identifiant de contrat) ===")
    total = 0
    for split in SPLITS:
        n = len(corps[split])
        total += n
        print(f"  {split.upper():5s} : {n:4d} lignes · {len(par_split[split]):3d} contrats distincts"
              + (f" · {len(sans_contrat[split])} sans contrat (le canari)" if sans_contrat[split] else ""))
    print(f"  TOTAL : {total} lignes")

    print("=== LA MATRICE DES CONTRATS PAR SPLIT ===")
    tous = sorted(set().union(*[set(par_split[s]) for s in SPLITS]))
    print(f"  {'contrat':10s} " + " ".join(f"{s.upper():>6s}" for s in SPLITS))
    partage = 0
    for cid in tous:
        rang = [len(par_split[s].get(cid, [])) for s in SPLITS]
        marque = ""
        if sum(1 for x in rang if x) > 1:
            marque = "   <-- PARTAGÉ"
            partage += 1
        print(f"  {cid:10s} " + " ".join(f"{x:6d}" for x in rang) + marque)

    print("=== LE VERDICT ===")
    if constats:
        print(f"  FUITE INTER-SPLITS : {partage} contrat(s) partagé(s)")
        for c in constats:
            print(f"    {c['a'].upper()} ∩ {c['b'].upper()} : {c['n']} contrat(s) → {', '.join(c['contrats'])}")
        code = 3
    else:
        print("  ÉTANCHE : aucun contrat partagé entre deux splits (v3 et v4 confondus)")
        code = 0

    if args.sortie:
        registre = {
            "schema": "TRIADE-AUDIT-SPLITS-v1",
            "unite": "l'identifiant de contrat (loupe-XX, tls13-XX, sys-XX)",
            "splits": {s: {"lignes": len(corps[s]),
                           "contrats": len(par_split[s]),
                           "sans_contrat": sans_contrat[s]} for s in SPLITS},
            "contrats_partages": constats,
            "verdict": "FUITE" if constats else "ETANCHE",
            "total_lignes": total,
        }
        with open(args.sortie, "w", encoding="utf-8") as f:
            json.dump(registre, f, ensure_ascii=False, indent=2)
        print(f"  registre : {args.sortie}")

    return code


if __name__ == "__main__":
    sys.exit(main())
