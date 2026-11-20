#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""taches_edition.py — LA LISTE GELÉE DES 18 TÂCHES D'ÉDITION (le plan
OPT-05 § 1.3, le type « LA CONSTANTE REVUE »). Généré AVANT TOUTE MESURE ;
l'empreinte sha256 du JSON produit est consignée au plan.

La règle (gelée au plan) : dans chaque bloc, LA PREMIÈRE instruction
portant un opérande immédiat de travail (cmp ou mov, destination un
registre autre que rsp/rbp — les tailles de cadre et les déplacements
mémoire EXCLUS) voit son immédiat révisé : imm > 0 → imm − 1 ;
imm = 0 → −1 (la révision de sentinelle). Le repli pour un bloc sans
tel immédiat : LE PREMIER « jz » devient « je » (l'alias — la classe
d'encodage équivalent du projet, zéro octet changé)."""
from __future__ import annotations

import hashlib
import json
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[1]
NOTATIONS = REPO / "loupe" / "notation"
VT = REPO / "atelier-localiser-5gfx6pwkj" / "verites-terrain.json"

IMM = re.compile(r"^(cmp|mov)\s+([a-z0-9]+),\s*(-?(?:0x[0-9a-f]+|\d+))\s*$")


def reviser_imm(valeur: str) -> str:
    """imm → imm − 1 ; 0 → -1 (la sentinelle). Garde la base (hex/déc)."""
    est_hex = valeur.lower().startswith("0x")
    n = int(valeur, 16 if est_hex else 10)
    n = n - 1 if n > 0 else -1
    return hex(n) if est_hex else str(n)


def tache_bloc(nom: str) -> dict:
    lignes = (NOTATIONS / f"{nom}.asm").read_text(encoding="utf-8").splitlines()
    type_tache = "constance-revue"
    for i, l in enumerate(lignes):
        l = l.strip()
        if l.startswith(";") or not l:
            continue
        m = IMM.match(l)
        if not m:
            continue
        op, reg, imm = m.group(1), m.group(2), m.group(3)
        if reg.startswith("rsp") or reg.startswith("rbp") or reg.startswith("esp") or reg.startswith("ebp"):
            continue
        nouvelle = f"{op} {reg}, {reviser_imm(imm)}"
        return {
            "bloc": nom,
            "type": type_tache,
            "ligne_index": i,
            "ancienne": l,
            "nouvelle": nouvelle,
            "consigne": (
                f"RÉVISION DE CONTRAT (loupe-XX:R2, la classe « la constante revue ») : "
                f"la ligne « {l} » est révisée en « {nouvelle} » — l'immédiat de travail "
                f"passe de {imm} à sa valeur révisée. AUCUNE autre ligne de code ne change "
                f"(les adresses, les étiquettes et les autres instructions demeurent OCTET "
                f"POUR OCTET ; les lignes de commentaire d'en-tête peuvent être mises à "
                f"jour pour porter la révision)."
            ),
        }
    # LE REPLI : l'alias jz → je
    for i, l in enumerate(lignes):
        l = l.strip()
        if l.startswith("jz "):
            return {
                "bloc": nom,
                "type": "alias-revu",
                "ligne_index": i,
                "ancienne": l,
                "nouvelle": "je " + l[3:],
                "consigne": (
                    f"RÉVISION DE NOTATION (la classe « l'encodage équivalent ») : la "
                    f"ligne « {l} » est révisée en « je {l[3:]} » — l'alias de mnémonique, "
                    f"zéro octet changé. AUCUNE autre ligne ne change."
                ),
            }
    raise SystemExit(f"[taches] AUCUNE ÉDITION TROUVÉE pour {nom}")


def main() -> int:
    vt = json.loads(VT.read_text(encoding="utf-8"))
    par_id = {b["id"]: b["nom"] for b in vt["blocs"]}
    taches = [tache_bloc(par_id[bid]) for bid in vt["ordre"]]
    for t in taches:
        t["consigne"] = t["consigne"].replace("loupe-XX:R2", f"{t['bloc']}:R2")
    sortie = pathlib.Path(__file__).resolve().parent / "taches-edition.json"
    sortie.write_text(json.dumps(taches, ensure_ascii=False, indent=1), encoding="utf-8")
    emp = hashlib.sha256(sortie.read_bytes()).hexdigest()
    print(f"18 tâches générées -> {sortie.name}")
    for t in taches:
        print(f"  {t['bloc']:22s} [{t['type']:15s}] {t['ancienne']}  ->  {t['nouvelle']}")
    print(f"sha256(taches-edition.json) = {emp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
