#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AGRÉGATEUR FAIL-CLOSED du harnais image (P3, plan gelé A1/A2/A3).

Recompose les comptes DEPUIS resultat-image.json (jamais à la main) et REFUSE :
  A1  un bloc absent du fichier, un total différent de 235 ;
  A2  toute régression contre le « avant » v1 (atelier-w23-harnais, 95) ;
  A3  la cible ≥ 200/235 (pré-enregistrée, non re-tirable) : manquée = publiée.

Écrit recomposition-image.json + tableau-image.txt ; sortie NON-ZÉRO si REFUS.
"""
import json
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parents[1]
ICI = R / "atelier-p3-exec"
AVANT = R / "atelier-w23-harnais/harnais-resultat.json"

CAUSES = {
    "Invalid memory read": "READ_UNMAPPED",
    "Invalid memory fetch": "FETCH_UNMAPPED",
    "Invalid memory write": "WRITE_UNMAPPED",
    "Invalid instruction": "INSTRUCTION_INVALIDE",
    "Timeout": "TIMEOUT",
}


def principal():
    refus = []
    detail = json.loads((ICI / "resultat-image.json").read_text())
    avant = json.loads(AVANT.read_text())

    # A1 — recomposition
    par_bloc = {}
    for bid, b in sorted(detail.items()):
        vec = b["vecteurs"]
        ok = sum(1 for v in vec if v["statut"] == "OK")
        fautes = [v for v in vec if v["statut"] != "OK"]
        causes = sorted({CAUSES.get(v["motif"].split(":")[-1], v["motif"].split(":")[-1])
                         for v in fautes})
        par_bloc[bid] = {
            "rva": b["rva"], "vecteurs": len(vec), "executes": ok,
            "fautes": len(vec) - ok,
            "causes": causes,
            "par_vecteur": [{"exigence": v["exigence"], "statut": v["statut"],
                             "abi": v["abi"], "motif": v["motif"]} for v in vec],
        }
    total = sum(v["vecteurs"] for v in par_bloc.values())
    ok = sum(v["executes"] for v in par_bloc.values())
    if total != 235:
        refus.append(f"A1: total recomposé {total} != 235")

    # A1 — le « avant » de v1 sert de référence par bloc (régression)
    avant_par_bloc = {bid: v.get("ok", 0) for bid, v in avant["par_bloc"].items()}
    regressions = []
    for bid, v in par_bloc.items():
        if v["executes"] < avant_par_bloc.get(bid, 0):
            regressions.append(f"{bid}: {avant_par_bloc[bid]} → {v['executes']}")
    if regressions:
        refus.append("A2: RÉGRESSION — " + "; ".join(regressions))

    delta = ok - 95
    cible_tenue = ok >= 200

    doc = {
        "total_vecteurs": total,
        "executes_ok": ok,
        "fault": total - ok,
        "avant_executes_ok": 95,
        "delta": delta,
        "sans_execution": sum(1 for v in par_bloc.values() if v["executes"] == 0),
        "partiels": sum(1 for v in par_bloc.values() if 0 < v["executes"] < v["vecteurs"]),
        "cible": 200,
        "cible_tenue": cible_tenue,
        "regressions": regressions,
        "refus": refus,
        "par_bloc": par_bloc,
    }
    (ICI / "recomposition-image.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")

    # le tableau par bloc (rendu exigé par le brief)
    lignes = [
        "# TABLEAU PAR BLOC — harnais image v2 (P3, 25/11/2026)",
        f"# recomposé depuis resultat-image.json · total {total} · exécutés {ok} "
        f"· fautes {total - ok} · delta contre 95 : {delta:+d}",
        f"# cible ≥ 200/235 : {'TENUE' if cible_tenue else 'MANQUÉE'}"
        f" · régressions : {len(regressions)}",
        "",
        f"{'bloc':8} {'rva':>7} {'vect':>4} {'exé':>4} {'faut':>4}  causes",
    ]
    for bid, v in par_bloc.items():
        causes = ",".join(v["causes"]) if v["causes"] else ("—" if v["fautes"] == 0 else "?")
        lignes.append(f"{bid:8} {hex(v['rva']):>7} {v['vecteurs']:>4} {v['executes']:>4} "
                      f"{v['fautes']:>4}  {causes}")
    lignes.append("")
    lignes.append(f"blocs sans aucune exécution : {doc['sans_execution']} · "
                  f"blocs partiels : {doc['partiels']}")
    (ICI / "tableau-image.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")

    print(f"[agrégateur] {ok}/{total} exécutés (avant 95, delta {delta:+d}) · "
          f"sans exécution {doc['sans_execution']} · partiels {doc['partiels']} · "
          f"cible ≥200 → {'TENUE' if cible_tenue else 'MANQUÉE'} · "
          f"régressions {len(regressions)}")
    if refus:
        print("[agrégateur] REFUS :")
        for r in refus:
            print("  " + r)
        return 1
    print("[agrégateur] AUCUN REFUS — comptes recomposés, pas de régression")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
