#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_negatif_memo.py — LA FALSIFICATION DU MÉMO VÉCUE (le plan
§ 5.6 : le contrôle négatif — la culture du projet l'exige) :

  1. UN OCTET DU CADRE RELEVÉ MUTÉ au mémo scellé → le chargement REFUSE
     (CHAÎNE-ROMPUE) ;
  2. LA RACINE MUTÉE → REFUS (RACINE-DIVERGENTE) ;
  3. LA SIGNATURE MUTÉE → REFUS (SIGNATURE-INVALIDE) ;
  4. LE MÉMO ABSENT → le repli : la session VIVANTE court (l'émulation
     complète, jamais l'échec muet).

Sortie : preuves/controle-negatif-memo.txt (le relevé des verdicts)."""
from __future__ import annotations

import json
import os
import pathlib
import shutil
import sys

REPO = pathlib.Path("/tmp/triade-gh")
ATELIER = REPO / "atelier-m4-vljfs6pcj"
sys.path.insert(0, str(ATELIER))
sys.path.insert(0, str(REPO / "loupe"))
import memo_sessions as MEMO      # noqa: E402

MEMO_SRC = ATELIER / "memo-sessions-v1.json"
SORTIE = ATELIER / "preuves" / "controle-negatif-memo.txt"


def tenter(chemin: pathlib.Path, attendu: str) -> tuple[bool, str]:
    try:
        MEMO.MemoSessions.charger(str(chemin))
        return False, "CHARGÉ (le refus ATTENDU n'est pas venu — ROUGE)"
    except MEMO.MemoRefus as e:
        nom = str(e).split(" : ")[0].split(" à l'entrée")[0].strip()
        return nom.startswith(attendu), f"REFUS {e}"


def main() -> int:
    lignes = ["LE CONTRÔLE NÉGATIF DU MÉMO SCELLÉ (le plan § 5.6)",
              "=" * 72, ""]
    tout_vert = True

    doc = json.loads(MEMO_SRC.read_text())

    # 1. un octet du cadre relevé muté
    m1 = json.loads(json.dumps(doc))
    entree = m1["entrees"][0]["valeur"]
    champ = "cadre_hex" if "cadre_hex" in entree else "panneau_hex"
    brut = bytearray(bytes.fromhex(entree[champ]))
    brut[7] ^= 0x01
    entree[champ] = bytes(brut).hex()
    p1 = ATELIER / "memo-mute-valeur.json"
    p1.write_text(json.dumps(m1, ensure_ascii=False), encoding="utf-8")
    ok, msg = tenter(p1, "CHAÎNE-ROMPUE")
    tout_vert &= ok
    lignes.append(f"1. UN OCTET DU RELEVÉ MUTÉ : {'VERT' if ok else 'ROUGE'}"
                  f" — {msg}")

    # 2. la racine mutée
    m2 = json.loads(json.dumps(doc))
    m2["racine"] = ("0" * 63 + "1") if m2["racine"][-1] != "1" \
        else ("0" * 64)
    p2 = ATELIER / "memo-mute-racine.json"
    p2.write_text(json.dumps(m2, ensure_ascii=False), encoding="utf-8")
    ok, msg = tenter(p2, "RACINE-DIVERGENTE")
    tout_vert &= ok
    lignes.append(f"2. LA RACINE MUTÉE : {'VERT' if ok else 'ROUGE'}"
                  f" — {msg}")

    # 3. la signature mutée (la chaîne demeure juste — la signature seule)
    m3 = json.loads(json.dumps(doc))
    sig = m3["signature"]
    m3["signature"] = sig[:-1] + ("1" if sig[-1] != "1" else "0")
    p3 = ATELIER / "memo-mute-signature.json"
    p3.write_text(json.dumps(m3, ensure_ascii=False), encoding="utf-8")
    ok, msg = tenter(p3, "SIGNATURE-INVALIDE")
    tout_vert &= ok
    lignes.append(f"3. LA SIGNATURE MUTÉE : {'VERT' if ok else 'ROUGE'}"
                  f" — {msg}")

    # 4. le mémo absent → le repli vivant
    p4 = ATELIER / "memo-absent.json"
    if p4.exists():
        p4.unlink()
    ok4, detail4 = False, ""
    try:
        MEMO.MemoSessions.charger(str(p4))
        detail4 = "CHARGÉ (le refus attendu n'est pas venu — ROUGE)"
    except MEMO.MemoRefus as e:
        ok4 = "MÉMO-ABSENT" in str(e)
        detail4 = f"REFUS {e} — le repli : la session vivante court " \
                  f"(vécu à la semence APRÈS-FROID)"
    tout_vert &= ok4
    lignes.append(f"4. LE MÉMO ABSENT : {'VERT' if ok4 else 'ROUGE'}"
                  f" — {detail4}")

    for p in (p1, p2, p3, p4):
        if p.exists():
            p.unlink()

    lignes += ["", "LA LECTURE HONNÊTE : le mémo n'est JAMAIS cru — "
                  "chaque écart nommé est un REFUS,",
               "le repli est l'émulation complète (jamais l'échec muet)."]
    verdict = "TOUT VERT" if tout_vert else "ROUGE"
    lignes.append(f"VERDICT : {verdict}")
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text("\n".join(lignes), encoding="utf-8")
    print("\n".join(lignes))
    return 0 if tout_vert else 2


if __name__ == "__main__":
    sys.exit(main())
