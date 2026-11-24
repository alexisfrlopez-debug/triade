#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATELIER W17R4PER — LA PROVENANCE DES TABLEAUX, DEPUIS LES SOURCES CANONIQUES.

Objet : rendre chaque nombre du dossier traçable à sa source canonique, et refuser
tout nombre qui ne s'y recompose pas. Les sources canoniques sont les JSONL et JSON
COMMITTÉS (campagnes TPL-ADD v2 à v5, gabarits, corpus v2.1, mesures GHASH agrégé) —
jamais un rapport, jamais une valeur retapée à la main.

Trois invariants tenus par le code :
  1. chaque ligne du registre porte la SOURCE (chemin + sha256), la grandeur, l'unité,
     n, la distribution (médiane) et le STATUT (mesuré / émulé / documenté / en attente) ;
  2. tout ratio est recalculé depuis ses OPÉRANDES NON ARRONDIS (règle D244) ;
  3. les quatre grandeurs (a) contrainte d'artefact, (b) performance d'exécution,
     (c) coût d'édition/validation, (d) sûreté et couverture ne sont NI additionnées
     NI comparées entre elles — le registre les étiquette séparément.

Usage :
  python3 scripts/vague17/provenance_tableaux.py --ecrire
  python3 scripts/vague17/provenance_tableaux.py --verifier
  python3 scripts/vague17/provenance_tableaux.py --controle-negatif
Sortie : 0 conforme, 2 refus nommé (une valeur, un ratio, un compte ou un statut ne
se recompose pas depuis la source).
"""
import argparse
import hashlib
import json
import os
import statistics
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SORTIE = os.path.join(RACINE, "replication-v17", "provenance-v17.json")


def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def lignes_jsonl(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def _tokens_tentative(r):
    """Les tokens de la DERNIÈRE tentative, quel que soit le schéma de campagne."""
    if isinstance(r.get("journaux"), list) and r["journaux"]:
        j = r["journaux"][-1]
        return j.get("total_tokens", j.get("total"))
    if "total_tokens" in r:
        return r["total_tokens"]
    return None


def campagne(rel, mode=None):
    """n tâches, verts, et DEUX conventions de médiane, jamais confondues :
    (i) la médiane des tokens de la dernière tentative des tâches VERTES,
    (ii) la médiane des tokens de la dernière tentative des n tâches (refus compris).
    Le mode filtre une campagne qui porte plusieurs modes dans un même fichier.
    """
    rows = lignes_jsonl(os.path.join(RACINE, rel))
    if mode:
        rows = [r for r in rows if r.get("mode") == mode]
    verts = [r for r in rows if r.get("vert")]
    toks_verts = [t for t in (_tokens_tentative(r) for r in verts) if t is not None]
    toks_toutes = [t for t in (_tokens_tentative(r) for r in rows) if t is not None]
    return {
        "n": len(rows),
        "verts": len(verts),
        "mediane_tokens_verts": statistics.median(toks_verts) if toks_verts else None,
        "mediane_tokens_toutes_taches": statistics.median(toks_toutes) if toks_toutes else None,
        "source": rel,
    }


def corpus():
    base = os.path.join(RACINE, "depot-zenodo-corpus-v21")
    compte = {}
    for split in ("train", "dev", "test"):
        compte[split] = len(lignes_jsonl(os.path.join(base, split + ".jsonl")))
    dpo = len(lignes_jsonl(os.path.join(base, "dpo-paires.jsonl")))
    fichiers = sorted(f for f in os.listdir(base) if os.path.isfile(os.path.join(base, f)))
    return {
        "lignes": compte,
        "paires_dpo": dpo,
        "fichiers": len(fichiers),
        "source": "depot-zenodo-corpus-v21",
    }


def ghash():
    rel = "atelier-ghash-agrege-h1mz2sr8s/registres/ghash-agrege.json"
    d = json.load(open(os.path.join(RACINE, rel), encoding="utf-8"))
    m = d["mesures"]
    agrege = m["ghash-agrege"]["mediane"]
    scelle = m["ghash-scelle"]["mediane"]
    return {
        "agrege_cycles": agrege,
        "scelle_cycles": scelle,
        "ratio": scelle / agrege,
        "source": rel,
    }


def construire():
    """Le registre : une ligne par grandeur, sa source, son n, son statut."""
    reg = []
    grandes = {
        "tpl_v2": "(c) coût d'édition — TPL-ADD-v2",
        "tpl_v3_ajouter": "(c) coût d'édition — TPL-ADD-v3, mode ajouter",
        "tpl_v3_editer": "(c) coût d'édition — TPL-ADD-v3, mode éditer",
        "tpl_v4": "(c) coût d'édition — TPL-ADD-v4",
        "tpl_v5": "(c) coût d'édition — TPL-ADD-v5",
        "gabarits": "(c) coût d'édition — gabarits versionnés",
    }
    for cle, rel, mode in (
        ("tpl_v2", "atelier-ajouter-v2-pgodgk35l/resultats_v2.jsonl", None),
        ("tpl_v3_ajouter", "atelier-ajouter-v3-5nwnwoceo/resultats_v3.jsonl", "ajouter-v3"),
        ("tpl_v3_editer", "atelier-ajouter-v3-5nwnwoceo/resultats_v3.jsonl", "editer-v3"),
        ("tpl_v4", "atelier-ajouter-v4-842vqyy1k/resultats_v4.jsonl", None),
        ("tpl_v5", "atelier-ajouter-v5-yfkpml1j2/resultats_v5.jsonl", None),
    ):
        c = campagne(rel, mode)
        reg.append({
            "id": cle,
            "grandeur": grandes[cle],
            "unite": "tâches (n), greens, tokens/changement validé (deux conventions de médiane nommées)",
            "n": c["n"],
            "valeur": {"verts": c["verts"],
                       "mediane_tokens_verts": c["mediane_tokens_verts"],
                       "mediane_tokens_toutes_taches": c["mediane_tokens_toutes_taches"]},
            "statut": "mesuré (VM, glm-4-plus, graines consignées, 18 tâches — ordre jamais re-tiré)",
            "source": {"chemin": rel, "sha256": sha256(os.path.join(RACINE, rel))},
        })
    g = campagne("atelier-gabarits-o5apue194/resultats_gabarits.jsonl")
    reg.append({
        "id": "gabarits",
        "grandeur": grandes["gabarits"],
        "unite": "essais (n), verts",
        "n": g["n"],
        "valeur": {"verts": g["verts"]},
        "statut": "mesuré (VM, gabarits versionnés)",
        "source": {"chemin": g["source"], "sha256": sha256(os.path.join(RACINE, g["source"]))},
    })
    c = corpus()
    for split, n in c["lignes"].items():
        reg.append({
            "id": "corpus_" + split,
            "grandeur": "(d) sûreté et couverture — corpus v2.1, split " + split,
            "unite": "triples (lignes JSONL)",
            "n": n,
            "valeur": n,
            "statut": "mesuré (fichiers livrés, recomptés)",
            "source": {"chemin": "depot-zenodo-corpus-v21/%s.jsonl" % split,
                       "sha256": sha256(os.path.join(RACINE, "depot-zenodo-corpus-v21", split + ".jsonl"))},
        })
    reg.append({
        "id": "corpus_dpo",
        "grandeur": "(d) sûreté et couverture — paires DPO v2.1",
        "unite": "paires",
        "n": c["paires_dpo"],
        "valeur": c["paires_dpo"],
        "statut": "mesuré (fichier livré, recompté)",
        "source": {"chemin": "depot-zenodo-corpus-v21/dpo-paires.jsonl",
                   "sha256": sha256(os.path.join(RACINE, "depot-zenodo-corpus-v21", "dpo-paires.jsonl"))},
    })
    gh = ghash()
    reg.append({
        "id": "ghash_ratio",
        "grandeur": "(b) performance d'exécution — ratio GHASH agrégé / scellé",
        "unite": "× (cycles médians, opérandes non arrondis)",
        "n": None,
        "valeur": {"operandes": [gh["scelle_cycles"], gh["agrege_cycles"]],
                   "ratio_non_arrondi": gh["ratio"], "publie_2_dec": round(gh["ratio"], 2)},
        "statut": "mesuré (émulation Unicorn + natif, même machine ; pas de métal nu)",
        "source": {"chemin": gh["source"], "sha256": sha256(os.path.join(RACINE, gh["source"]))},
    })
    return {"version": "vague17", "registre": reg}


def verifier(reg, attendu):
    """Refuse toute ligne qui ne se recompose pas depuis sa source. Quatre classes."""
    refus = []
    par_id = {r["id"]: r for r in attendu.get("registre", [])}
    for r in reg.get("registre", []):
        a = par_id.get(r["id"])
        if a is None:
            refus.append(("SOURCE-INCONNUE", r["id"]))
            continue
        if r["valeur"] != a["valeur"]:
            classe = "VALEUR" if not isinstance(r["valeur"], dict) or "ratio_non_arrondi" not in r["valeur"] else "RATIO"
            refus.append((classe, r["id"]))
        if r.get("n") != a.get("n"):
            refus.append(("COMPTE", r["id"]))
        if r.get("statut") != a.get("statut"):
            refus.append(("STATUT", r["id"]))
        if r.get("source", {}).get("sha256") != a.get("source", {}).get("sha256"):
            refus.append(("EMPREINTE-SOURCE", r["id"]))
    return refus


def afficher(reg):
    print("=" * 100)
    print("REGISTRE DE PROVENANCE — VAGUE 17 (les sources canoniques, leurs empreintes, leurs statuts)")
    print("=" * 100)
    for r in reg["registre"]:
        print(f"{r['id']:<14} {r['grandeur']}")
        print(f"{'':<14} n={r['n']} valeur={r['valeur']}")
        print(f"{'':<14} statut : {r['statut']}")
        print(f"{'':<14} source : {r['source']['chemin']} sha256 {r['source']['sha256'][:16]}…")
    print("-" * 100)
    print(f"{len(reg['registre'])} lignes — aucune grandeur (a)-(d) n'est additionnée ni comparée à une autre")


def controle_negatif():
    """Quatre mutations, quatre refus attendus : valeur, ratio, compte, statut."""
    attendu = json.load(open(SORTIE, encoding="utf-8"))
    essais = []

    def mute(fn, classe):
        reg = json.loads(json.dumps(attendu))
        fn(reg["registre"])
        refus = verifier(reg, attendu)
        essais.append((classe, refus))

    mute(lambda r: next(x for x in r if x["id"] == "corpus_train").__setitem__("valeur", 128), "VALEUR")
    mute(lambda r: next(x for x in r if x["id"] == "ghash_ratio")["valeur"].__setitem__("ratio_non_arrondi", 50.0), "RATIO")
    mute(lambda r: next(x for x in r if x["id"] == "corpus_dpo").__setitem__("n", 49), "COMPTE")
    mute(lambda r: next(x for x in r if x["id"] == "tpl_v5").__setitem__("statut", "courant"), "STATUT")

    print("=" * 78)
    print("CONTRÔLES NÉGATIFS — QUATRE MUTATIONS, QUATRE REFUS ATTENDUS")
    print("=" * 78)
    verts = 0
    for classe, refus in essais:
        ok = any(c == classe for c, _ in refus) and len(refus) > 0
        verts += 1 if ok else 0
        print(f"[{'VERT' if ok else 'ROUGE'}] mutation de classe {classe} → refus : {refus}")
    print("-" * 78)
    print(f"{verts}/4 contrôles négatifs rendus")
    return 0 if verts == 4 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ecrire", action="store_true")
    ap.add_argument("--verifier", action="store_true")
    ap.add_argument("--controle-negatif", action="store_true")
    a = ap.parse_args()
    reg = construire()
    if a.ecrire:
        os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
        with open(SORTIE, "w", encoding="utf-8") as f:
            json.dump(reg, f, ensure_ascii=False, indent=1, sort_keys=True)
            f.write("\n")
        afficher(reg)
        print(f"écrit : {os.path.relpath(SORTIE, RACINE)}")
        return 0
    if a.verifier:
        if not os.path.exists(SORTIE):
            print("REFUS — registre attendu absent : lancer --ecrire d'abord")
            return 2
        attendu = json.load(open(SORTIE, encoding="utf-8"))
        refus = verifier(reg, attendu)
        afficher(reg)
        if refus:
            print("REFUS NOMMÉ :", refus)
            return 2
        print("CONFORME — chaque ligne se recompose depuis sa source canonique")
        return 0
    if a.controle_negatif:
        return controle_negatif()
    afficher(reg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
