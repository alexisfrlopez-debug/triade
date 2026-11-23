#!/usr/bin/env python3
"""generer_paires_dpo.py — atelier 0J7YWZA2H (la vague 16, l'achèvement).

LE SECOND LEVIER DE L'INSTRUCTION : la génération de paires DPO par rejection
sampling — « pour chaque contrat, échantillonne k complétions, apparie notation
VERTE vs REFUS au même contrat (récompense = le verdict du juge, JAMAIS la
similarité), scrub fail-closed, split par contrat étanche ».

La matière : le corpus v2.1 corrigé (les splits PAR GROUPE-DE-CONTRAT —
l'étanchéité par contrat est la condition de validité des paires : une paire ne
peut pas fuiter vers le TEST puisque le contrat entier vit dans UN split).
L'appariement : CHOSEN = une complétion VERTE du juge, REJECTED = une complétion
REFUS du juge, AU MÊME CONTRAT — la récompense est le VERDICT, jamais une
similarité. Les paires naissent du TRAIN SEUL (les paires DPO sont de
l'entraînement ; le TEST reste nu et les DEV/TEST ne fournissent AUCUNE paire).

LE CONTRÔLE ANTI-HACKING P2 : chaque paire porte ses deux empreintes sha256 ;
une notation MUTÉE à la récompense (un octet changé au chosen ou au rejected)
est REFUSÉE par la porte — la preuve au contrôle négatif, pas à l'intention.
"""

import argparse
import hashlib
import json
import os
import re
import sys

RE_CONTRAT = re.compile(r"^(loupe-\d+|tls13-\d+|sys-\d+)\s*·", re.MULTILINE)


def contrat_id(enreg):
    m = RE_CONTRAT.search(enreg.get("contrat", ""))
    if m:
        return m.group(1)
    m = re.match(r"^((?:loupe|tls13|sys)-\d+)", enreg.get("bloc", ""))
    return m.group(1) if m else None


def sha256_texte(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def charger_train(dataset):
    with open(os.path.join(dataset, "train.jsonl"), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def generer(dataset, limite_refus=None):
    """-> [paire] — CHOSEN vert, REJECTED refus, AU MÊME CONTRAT, du TRAIN seul."""
    enregistrements = charger_train(dataset)
    par_contrat = {}
    for e in enregistrements:
        c = contrat_id(e)
        if c is None:
            continue                                    # le canari : jamais une paire
        par_contrat.setdefault(c, []).append(e)

    paires = []
    for contrat in sorted(par_contrat):
        verts = [e for e in par_contrat[contrat] if e.get("verdict") == "VERT"]
        refus = [e for e in par_contrat[contrat] if e.get("verdict") == "REFUS"]
        if not verts or not refus:
            continue
        refuses = refus[:limite_refus] if limite_refus else refus
        for v in sorted(verts, key=lambda x: x["triple"]):
            for r in sorted(refuses, key=lambda x: x["triple"]):
                paires.append({
                    "contrat": contrat,
                    "triple_vert": v["triple"],
                    "triple_refus": r["triple"],
                    "verdict_choisi": "VERT",
                    "verdict_rejete": r.get("classe_de_refus", "REFUS"),
                    "prompt": v["contrat"],
                    "chosen": v["reponse"],
                    "rejected": r["reponse"],
                    "sha256_chosen": sha256_texte(v["reponse"]),
                    "sha256_rejected": sha256_texte(r["reponse"]),
                })
    return paires, par_contrat


def porte_p2(paires, dataset):
    """LE CONTRÔLE ANTI-HACKING : la récompense est le VERDICT DU JUGE, et les
    notations sont BYTE-IDENTIQUES aux pièces du corpus — une notation mutée à
    la récompense est REFUSÉE."""
    corpus = {}
    for e in charger_train(dataset):
        if e.get("reponse"):
            corpus[e["triple"]] = e
    refus_p2 = []
    for p in paires:
        v, r = corpus.get(p["triple_vert"]), corpus.get(p["triple_refus"])
        if v is None or r is None:
            refus_p2.append((p["triple_vert"], "absent du corpus"))
            continue
        if v.get("verdict") != "VERT":
            refus_p2.append((p["triple_vert"], "le choisi n'est pas VERTE au juge"))
        if r.get("verdict") != "REFUS":
            refus_p2.append((p["triple_refus"], "le rejeté n'est pas REFUS au juge"))
        if p["chosen"] != v["reponse"]:
            refus_p2.append((p["triple_vert"], "la notation choisie a été MUTÉE"))
        if p["rejected"] != r["reponse"]:
            refus_p2.append((p["triple_refus"], "la notation rejetée a été MUTÉE"))
        if p["contrat"] != contrat_id(v) or p["contrat"] != contrat_id(r):
            refus_p2.append((p["triple_vert"], "la paire est à cheval sur deux contrats"))
    return refus_p2


def ecrire(paires, chemin):
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        for p in paires:
            f.write(json.dumps(p, ensure_ascii=False, sort_keys=True) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--sortie", default=None)
    ap.add_argument("--limite-refus", type=int, default=None)
    ap.add_argument("--autotest", action="store_true")
    args = ap.parse_args()

    if args.autotest:
        print("=== L'AUTOTEST DE LA PORTE P2 (le contrôle anti-hacking) ===")
        paires, _ = generer(args.dataset)
        sains = not porte_p2(paires, args.dataset)
        print(f"  [1] les {len(paires)} paires saines à la porte      : "
              f"{'OUI' if sains else 'NON'}")
        mute = [dict(p) for p in paires[:3]]
        for p in mute:
            p["chosen"] = p["chosen"] + "\nmov rax, 1"      # LA NOTATION MUTÉE
        attrape = bool(porte_p2(mute, args.dataset))
        print(f"  [2] la notation MUTÉE à la récompense : "
              f"{'REFUSÉE' if attrape else 'PASSÉE — DÉFAUT GRAVE'}")
        return 0 if (sains and attrape) else 1

    if not args.sortie:
        ap.error("--sortie est requis (hors --autotest)")
    paires, par_contrat = generer(args.dataset, args.limite_refus)
    ecrire(paires, args.sortie)

    print("=== LA GÉNÉRATION DES PAIRES DPO (le TRAIN seul, par contrat) ===")
    print(f"  les contrats au TRAIN : {len(par_contrat)}")
    concernes = sorted({p['contrat'] for p in paires})
    print(f"  les contrats portant des paires : {len(concernes)} → {', '.join(concernes)}")
    print(f"  LES PAIRES : {len(paires)} (CHOSEN vert · REJECTED refus · même contrat)")
    refus_p2 = porte_p2(paires, args.dataset)
    print(f"  LA PORTE P2 : {len(refus_p2)} refus" + (f" — {refus_p2[:3]}" if refus_p2 else " (toutes les paires saines)"))
    print(f"  le fichier : {args.sortie} ({os.path.getsize(args.sortie)} octets)")
    return 0 if not refus_p2 else 3


if __name__ == "__main__":
    sys.exit(main())
