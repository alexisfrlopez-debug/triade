#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agregateur_materiel.py — L'AGRÉGATEUR MATÉRIEL FAIL-CLOSED (gzxvze3py,
la vague 15) : UN RUN MANQUANT = REFUS (exit 2), JAMAIS un verdict
partiel. Les protocoles PRÉ-ENREGISTRÉS (les trois pièces) ; les runs
appartiennent au développeur — le laboratoire prépare et vérifie, ne
simule JAMAIS.
Usage : agregateur_materiel.py dudect <temoins.json>    (n≥10 par
N∈{60,200,400}, ≥2 machines, l'empreinte CPU + l'état de fréquence)
       agregateur_materiel.py loupe <temoins.json>       (T0→T7+S0 +
       la vitrine [4/4])"""
from __future__ import annotations

import json
import pathlib
import sys

PROTOCOLES = {
    "dudect": {"runs_attendus": 2 * 3 * 10,  # 2 machines × 3 tailles × n≥10
               "pieces": ["l'empreinte CPU par machine",
                          "l'état de fréquence consigné",
                          "l'affinité de cœur fixe",
                          "L'INVESTIGATION DES PICS tls13-02/tls13-13 à "
                          "N=200 pré-enregistrée : bruit d'horloge / "
                          "interruption cœur partagé / gap réel — LE "
                          "CRITÈRE DE MÉDIANE TRANCHE, aucune cause "
                          "élue d'avance"],
               "revendication_interdite": "« constant time proven » "
                                          "JAMAIS — le scope est "
                                          "L'ÉCHANTILLON, la machine, "
                                          "les runs"},
    "loupe": {"runs_attendus": 4 + 1 + 4,   # T0-T7 + S0 + la vitrine 4/4
              "pieces": ["T0→T7+S0 intégral", "la vitrine [4/4] deux "
                         "codes 0", "les empreintes avant/après "
                         "INCHANGÉES"],
              "revendication_interdite": "aucune pièce scellée ne bouge"},
    "fence": {"runs_attendus": 5,           # C1-C5 sur RV64
              "pieces": ["la carte RV64 physique", "la bascule vue par "
                         "le cœur (C1)", "l'invalidation prouvée au "
                         "témoin (C2)", "la cohérence du plan (C3)",
                         "le scellé au silicium (C4)", "zéro régression "
                         "(C5)"],
              "revendication_interdite": "aucune"},
}


def aggreger(protocole: str, chemin: pathlib.Path) -> int:
    spec = PROTOCOLES[protocole]
    if not chemin.exists():
        print(f"[AGRÉGATEUR] REFUS (exit 2) — le fichier des témoins "
              f"{chemin} ABSENT : un run manquant = refus, JAMAIS un "
              "verdict partiel")
        return 2
    temoins = [json.loads(l) for l in chemin.read_text(
        encoding="utf-8").splitlines() if l.strip()]
    machines = {t.get("machine", "?") for t in temoins}
    n = len(temoins)
    print(f"le protocole {protocole} : {n} témoins, {len(machines)} "
          f"machine(s) — attendus {spec['runs_attendus']} pièces "
          f"({len(machines)} machine(s) ≥ 2 exigées au dudect)")
    ok = n >= spec["runs_attendus"] and (protocole != "dudect"
                                         or len(machines) >= 2)
    for piece in spec["pieces"]:
        present = any(piece[:20] in json.dumps(t, ensure_ascii=False)
                      for t in temoins)
        print(f"  {piece[:70]} : {'présent' if present else 'ABSENT — le refus nommé'}")
        ok = ok and present
    if not ok:
        print("[AGRÉGATEUR] REFUS (exit 2) — jamais un verdict partiel ; "
              "la revendication interdite demeure : "
              + spec["revendication_interdite"])
        return 2
    print("[AGRÉGATEUR] VERT — les témoins signés recoupés avant tout "
          "mouvement de la table des statuts")
    return 0


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in PROTOCOLES:
        print(__doc__)
        return 2
    return aggreger(sys.argv[1], pathlib.Path(sys.argv[2]))


if __name__ == "__main__":
    sys.exit(main())
