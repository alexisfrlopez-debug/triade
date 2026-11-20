#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cgp_recomposition.py — LA RECOMPOSITION DU PLAN DU BRAS C+G+ (3lmyfb2xa)
: le graphe de dépendances des sources RE-VÉRIFIÉ À CHAQUE LIVRAISON (le
plan § 2 : l'adaptation compilée du build-recomposition du bras T — le
bras T RECOMPOSE la pièce depuis le plan à chaque session ; le bras C+G+
RE-VÉRIFIE le graphe : chaque source, chaque dépendance d'inclusion, la
spec signée, l'outil, le corpus — L'ÉQUIVALENCE DOCUMENTÉE, jamais
confondue : la recomposition d'octets vit aux REBUILDS de cristallisation).

Le plan gelé : cgp-plan.json (consigné par cgp_construire.py AVANT toute
mesure). Chaque divergence : REFUS NOMMÉ (fail-closed).

Usage :
  python3 cgp_recomposition.py                # la vérification honnête
  python3 cgp_recomposition.py --falsifie    # le contrôle : un hash
                                             # muté dans la copie en
                                             # mémoire → REFUS attendu
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
PLAN = ICI / "cgp-plan.json"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def refus(nom: str, detail: str) -> int:
    print(f"[recomposition] REFUS {nom} : {detail}")
    return 2


def inclussions(src_texte: str) -> list[str]:
    return re.findall(r'^\s*#\s*include\s*[<"]([^>"]+)[>"]',
                      src_texte, re.M)


def main() -> int:
    falsifie = "--falsifie" in sys.argv[1:]
    if not PLAN.exists():
        return refus("PLAN-ABSENT", f"{PLAN} — construire d'abord")
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if falsifie:
        # LE CONTRÔLE : UNE dépendance mutée dans la copie en mémoire —
        # la vérification DOIT refuser (les originaux jamais touchés)
        plan["unites"][0]["sha256_source"] = \
            plan["unites"][0]["sha256_source"][:-2] + "ab"
        print("[recomposition] LA FALSIFICATION DEMANDÉE : le hash de la "
              "source de loupe-01 muté dans la copie en mémoire")

    print("=== LA RECOMPOSITION DU PLAN (C+G+) — le graphe de "
          "dépendances re-vérifié à la livraison ===")
    verts, refus_n = 0, 0

    # 1. LES SIX UNITÉS : la source, ses inclusions de dépôt résolues, la
    #    spec (les inclusions système portées par la chaîne d'outil gelée)
    for u in plan["unites"]:
        src = REPO / u["source"]
        if not src.exists():
            print(f"  ROUGE {u['unite']} : la source ABSENTE ({src})")
            refus_n += 1
            continue
        h_src = sha(src)
        deps_ok = 0
        for rel, attendu in u["deps"].items():
            p = REPO / rel
            if not p.exists() or sha(p) != attendu:
                print(f"  ROUGE {u['unite']} : la dépendance {rel} "
                      "ABSENTE ou DIVERGENTE de son empreinte gelée")
                refus_n += 1
                continue
            deps_ok += 1
        spec = REPO / u["spec"]
        ok = (h_src == u["sha256_source"]
              and spec.exists() and sha(spec) == u["sha256_spec"]
              and deps_ok == len(u["deps"]))
        verts += ok
        refus_n += not ok
        dll_ch = u["dll_chaine"]
        attendu_dll = ("ECHEC (l'état clos de la chaîne)"
                       if dll_ch == "ECHEC" else dll_ch[:12] + "…")
        print(f"  {'VERT' if ok else 'ROUGE'} {u['unite']} ({u['famille']}"
              f") : la source {h_src[:12]}… recoupée ; {deps_ok}/"
              f"{len(u['deps'])} dépendances d'inclusion de dépôt "
              f"recoupées ; {len(u.get('systeme', []))} inclusion(s) "
              f"système (portées par la chaîne d'outil gelée) ; la spec "
              f"signée {u['sha256_spec'][:12]}… recoupée ; le DLL de la "
              f"chaîne vague 10 : {attendu_dll}")

    # 2. LES HARNAIS D'ÉPREUVE (la campagne + les miens) — chaque fichier
    #    à SON empreinte gelée
    refus_h = 0
    for rel, attendu in plan["harnais"].items():
        p = REPO / rel
        ok = p.exists() and sha(p) == attendu
        verts += ok
        if not ok:
            refus_n += 1
            refus_h += 1
            print(f"  ROUGE harnais {rel} : ABSENT ou DIVERGENT")
    print(f"  {'VERT' if refus_h == 0 else 'ROUGE'} les harnais "
          f"d'épreuve : {len(plan['harnais'])} fichiers recoupés à leurs "
          f"empreintes gelées")

    # 3. LA CHAÎNE DE GOUVERNANCE (les artefacts vague 10 que le bras
    #    reçoit : l'outil cg_gouverne.py, la chaîne signée, la clé)
    refus_g = 0
    for rel, attendu in plan["gouvernance"].items():
        p = REPO / rel
        ok = p.exists() and sha(p) == attendu
        verts += ok
        if not ok:
            refus_n += 1
            refus_g += 1
            print(f"  ROUGE gouvernance {rel} : ABSENT ou DIVERGENT")
    ch = json.loads((REPO / "atelier-cg-3a91o5whb" / "cristallisation"
                     / "chaine.json").read_text(encoding="utf-8"))
    recoupees = 0
    for u in ch["chaine"]:
        if hashlib.sha256((u["precedente"] + u["sha256_source"]
                           + u["sha256_dll"]).encode()).hexdigest() \
                == u["empreinte_unite"]:
            recoupees += 1
    ok_chaine = recoupees == len(ch["chaine"])
    verts += ok_chaine
    if not ok_chaine:
        refus_n += 1
    print(f"  {'VERT' if ok_chaine else 'ROUGE'} la chaîne de "
          f"cristallisation vague 10 : {recoupees}/{len(ch['chaine'])} "
          f"empreintes d'unité recoupées (la signature vit à g2)")

    # 4. L'OUTIL (la chaîne mingw gelée + le gcc natif) et LE CORPUS
    refus_o = 0
    for rel, attendu in plan["outil"].items():
        p = pathlib.Path(rel)
        ok = p.exists() and sha(p) == attendu
        verts += ok
        if not ok:
            refus_n += 1
            refus_o += 1
            print(f"  ROUGE outil {rel} : ABSENT ou DIVERGENT")
    for rel, attendu in plan["corpus"].items():
        p = ICI / rel
        ok = p.exists() and sha(p) == attendu
        verts += ok
        if not ok:
            refus_n += 1
            refus_o += 1
            print(f"  ROUGE corpus {rel} : ABSENT ou DIVERGENT")
    print(f"  {'VERT' if refus_o == 0 else 'ROUGE'} l'outil (la chaîne "
          f"mingw {plan['outil_mingw_version']}, le gcc natif) et le "
          f"corpus ({len(plan['corpus'])} fichiers) recoupés")

    print(f"=== LA RECOMPOSITION : {verts} VERT, {refus_n} REFUS — "
          f"{'VERT' if refus_n == 0 else 'ROUGE (REFUS NOMMÉ)'} ===")
    return 0 if refus_n == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
