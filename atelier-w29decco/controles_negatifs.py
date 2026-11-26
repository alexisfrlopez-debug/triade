#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controles_negatifs.py — LES CONTRÔLES NÉGATIFS DU CLIENT (W29DECCO,
prompt 1 : « octet muté du diff refusé, offset hors plage refusé, clé hors
schéma refusée ») — éprouvés sur le validateur client OPT-16 reconduit
(l'import à l'identique, le juge D264 n'est jamais touché).

Chaque refus nommé par sa classe. La sortie : controles-verdict.json.
"""
import json
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "atelier-w28opt16"))
from campagne_opt16 import valider, expander, Refus, TACHES, NOTATIONS  # noqa: E402

ICI = pathlib.Path(__file__).resolve().parent


def empreinte(notation: str) -> str:
    import hashlib
    return hashlib.sha256(notation.encode("utf-8")).hexdigest()


def main():
    t = json.loads(TACHES.read_text(encoding="utf-8"))[0]     # la première tâche canonique
    notation = (NOTATIONS / f"{t['bloc']}.asm").read_text(encoding="utf-8")
    emp = empreinte(notation)
    n_lignes = len(notation.splitlines())

    verdicts = []

    # ---- 1. OCTET MUTÉ DU DIFF REFUSÉ ------------------------------------------------
    # la réponse honnête, un octet de la ligne src muté
    honnete = {"op": "substituer", "dst": t["bloc"], "offset": t["ligne_index"],
               "src": t["nouvelle"]}
    src_muté = t["nouvelle"][:2] + ("X" if t["nouvelle"][2:3] != "X" else "Y") + t["nouvelle"][3:]
    obj_mute = dict(honnete, src=src_muté)
    try:
        expander(t, obj_mute, notation)
        v = {"nom": "octet-mute-du-diff", "refuse": False, "classe": "(aucune — passe!)"}
    except Refus as r:
        v = {"nom": "octet-mute-du-diff", "refuse": True, "classe": r.nom,
             "detail": r.detail[:160]}
    verdicts.append(v)

    # la mutation qui casse l'assemblage : un mnémonique inconnu
    lignes = t["nouvelle"].split(" ", 1)
    src_casse = "zzzz9 " + (lignes[1] if len(lignes) > 1 else "0x0")
    try:
        expander(t, dict(honnete, src=src_casse), notation)
        v = {"nom": "ligne-non-assemblable", "refuse": False, "classe": "(aucune)"}
    except Refus as r:
        v = {"nom": "ligne-non-assemblable", "refuse": True, "classe": r.nom,
             "detail": r.detail[:160]}
    verdicts.append(v)

    # ---- 2. OFFSET HORS PLAGE REFUSÉ ----------------------------------------------------
    try:
        valider(json.dumps(dict(honnete, offset=n_lignes + 7)), t, notation, emp)
        v = {"nom": "offset-hors-plage", "refuse": False, "classe": "(aucune)"}
    except Refus as r:
        v = {"nom": "offset-hors-plage", "refuse": True, "classe": r.nom}
    verdicts.append(v)

    # ---- 3. CLÉ HORS SCHÉMA REFUSÉE -----------------------------------------------------
    obj_cle = dict(honnete)
    obj_cle["subversion"] = "1"
    try:
        valider(json.dumps(obj_cle), t, notation, emp)
        v = {"nom": "cle-hors-schema", "refuse": False, "classe": "(aucune)"}
    except Refus as r:
        v = {"nom": "cle-hors-schema", "refuse": True, "classe": r.nom}
    verdicts.append(v)

    # ---- 4. OP HORS ENUM (le validateur — le masque déjà prouvé au gate) ----------------
    try:
        valider(json.dumps(dict(honnete, op="SUBVERSION-HORS-ENUM")), t, notation, emp)
        v = {"nom": "op-hors-enum-validateur", "refuse": False, "classe": "(aucune)"}
    except Refus as r:
        v = {"nom": "op-hors-enum-validateur", "refuse": True, "classe": r.nom}
    verdicts.append(v)

    # ---- LE HONNÊTE Passe (contrôle positif) --------------------------------------------
    try:
        obj = valider(json.dumps(honnete), t, notation, emp)
        expander(t, obj, notation)
        positif = True
    except Refus as r:
        positif = False
        print(f"POSITIF REFUSÉ (!): {r.nom}: {r.detail[:120]}")

    out = {"controles": verdicts, "controle_positif": positif,
           "tous_refuses": all(v["refuse"] for v in verdicts)}
    (ICI / "controles-verdict.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for v in verdicts:
        print(f"  {v['nom']:26s} refuse={v['refuse']}  classe={v.get('classe')}")
    print(f"  positif honnête: {positif} — tous les négatifs refusés: {out['tous_refuses']}")


if __name__ == "__main__":
    main()
