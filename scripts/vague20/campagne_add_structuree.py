#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA CAMPAGNE ADD STRUCTURÉE, PRÉ-ENREGISTRÉE (W20ADD, D264).

Le client à décodage contraint (structured output) émet le pointeur SEUL ; l'expandeur
déterministe de la vague 19 (importé, jamais recopié) compile la notation ; le juge intact
tranche. HORS-FORMAT devient impossible PAR CONSTRUCTION côté client, et reste refusé côté
juge si le schéma est violé.

Aucun serving à structured output dans ce bac : la campagne part EN ATTENTE. L'instrument
rejoue ses fixtures (18 pointeurs honnêtes, 4 mutées), rejoue deux fois à graine consignée
(bit-identique) et consigne la voie d'entraînement (SFT/DPO/RLVR) sans run.

Usage : python3 scripts/vague20/campagne_add_structuree.py [--fixtures|--preregistrer|--statut]
"""
import hashlib, importlib.util, json, pathlib, sys

R = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = R / "atelier-w20-add"
GRAINE = 20261124


def _expandeur():
    spec = importlib.util.spec_from_file_location("expandeur_add", R / "scripts/vague19/expandeur_add.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def empreinte_juge():
    return hashlib.sha256((R / "scripts/vague19/expandeur_add.py").read_bytes()).hexdigest()


SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["op", "offset"],
    "properties": {
        "op": {"enum": ["mov", "add", "sub", "xor", "and", "or", "cmp", "test", "jcc", "call", "ret"]},
        "dst": {"type": "object"}, "src": {"type": "object"},
        "offset": {"type": "integer", "minimum": 0, "maximum": 65535},
    },
}

RLVR = {
    "corpus": "TRIADE-CORPUS-v2.1 (127/24/19 triples, 48 paires DPO, splits par groupe-de-contrat, TEST sans dorée)",
    "recompense": "verdict typé du juge : syntaxe → expansion → round-trip → oracle → mutation ; cumulative et stricte, anti-hacking",
    "etape": "SFT (démonstrations), DPO (paires du corpus), RLVR (récompense = juge, échelle de capacité held-out)",
    "interdit": "aucun juge affaibli ; aucune cible re-tirée ; aucune dorée au TEST",
}


def preregistrer():
    DOSSIER.mkdir(exist_ok=True)
    doc = {
        "objet": "campagne add structurée (décodage contraint par grammaire)",
        "cible": "≥ 15/18 verts à ≤ 3 000 tokens par changement validé",
        "mediane": ["sur les 18 tâches", "sur les seules vertes (deux conventions nommées)"],
        "graine": GRAINE,
        "tokenisation": "indépendante, écart exigé ≤ 1 token",
        "juge": {"fichier": "scripts/vague19/expandeur_add.py", "sha256": empreinte_juge(), "intact": True},
        "schema_client": SCHEMA,
        "reparation": "contre-exemple réinjecté, borné à 3 tours, conversions consignées par classe",
        "voie_entrainement": RLVR,
        "statut": "EN ATTENTE — aucun serving à structured output dans ce bac",
    }
    f = DOSSIER / "preregistrement.json"
    f.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[preregistre] {f.relative_to(R)} sha256 {hashlib.sha256(f.read_bytes()).hexdigest()}")
    return doc


def fixtures():
    m = _expandeur()
    honnetes, mutes = m.fixtures()
    verts = 0
    for p in honnetes:
        r = m.boucle_reparation(p, m.DICO)
        verts += 1 if r["verdict"] == "VERT" else 0
    refus = {}
    for classe, p in mutes.items():
        r = m.boucle_reparation(p, m.DICO)
        refus[classe] = (r["classes_converties"][0] if r["classes_converties"] else r["verdict"])
    # rejeu bit-identique
    import json as _j
    a = _j.dumps([m.boucle_reparation(p, m.DICO) for p in honnetes], sort_keys=True)
    b = _j.dumps([m.boucle_reparation(p, m.DICO) for p in honnetes], sort_keys=True)
    tokens = [m.compter_tokens(m.expanse(p, m.DICO)) for p in honnetes]
    tokens2 = [m.compter_tokens_independant(m.expanse(p, m.DICO)) for p in honnetes]
    ecart = max(abs(x - y) for x, y in zip(tokens, tokens2))
    print("=" * 78); print("CAMPAGNE ADD STRUCTURÉE — FIXTURES (aucun serving : EN ATTENTE)"); print("=" * 78)
    print(f"[fixtures] {verts}/18 verts · refus par classe {refus}")
    print(f"[fixtures] rejeu bit-identique : {'VERT' if a == b else 'ROUGE'}")
    print(f"[tokens] médiane {sorted(tokens)[len(tokens)//2]} · écart entre compteurs {ecart} (≤1 exigé)")
    ok = verts == 18 and set(refus.values()) == set(mutes) and a == b and ecart <= 1
    return 0 if ok else 3


if __name__ == "__main__":
    if "--fixtures" in sys.argv: sys.exit(fixtures())
    if "--preregistrer" in sys.argv: preregistrer(); sys.exit(0)
    d = preregistrer(); print("[statut] EN ATTENTE —", d["statut"]); sys.exit(0)
