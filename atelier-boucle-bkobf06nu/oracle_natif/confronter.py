#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""confronter.py — LA CONFRONTATION AU LABORATOIRE des témoins du régime
ORACLE NATIF (le troisième régime — jamais le terrain du développeur).

Le témoin signé (runner.ps1 → temoin-natif.json) confronté aux ATTENTES
du laboratoire : les oracles hashlib du panneau, les découpes Python des
fenêtres, la base SANE de la boucle WinMain. TOUT écart un refus nommé
TEMOIN-DIVERGENT. La signature vérifiée D'ABORD (la clé publique du CI
au dépôt — jamais crue, toujours recalculée)."""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parents[1]

# la clé publique du CI (au dépôt — remplacée à l'armement du runner par
# le maître ; la clé privée AU SECRET DU CI, jamais au dépôt)
CLE_PUBLIQUE_CI = None   # posée à l'armement (le geste du maître)


def verifier_signature(temoin: dict) -> None:
    if CLE_PUBLIQUE_CI is None:
        raise SystemExit("ARMEMENT-ABSENT : la clé publique du CI n'est "
                         "pas posée — le régime natif exige le geste du "
                         "maître (l'armement du runner), jamais deviné")
    import nacl.signing
    import nacl.exceptions
    corps = {k: v for k, v in temoin.items() if k != "signature"}
    vk = nacl.signing.VerifyKey(bytes.fromhex(CLE_PUBLIQUE_CI))
    try:
        vk.verify(json.dumps(corps, sort_keys=True).encode(),
                  bytes.fromhex(temoin["signature"]))
    except (nacl.exceptions.BadSignatureError, ValueError):
        raise SystemExit("SIGNATURE-INVALIDE : le témoin natif refusé")


def attendu_panneau(fichier: bytes) -> str:
    """L'ATTENDU hashlib du panneau (md5 ‖ sha256 du fichier entier)."""
    import hashlib as h
    return (h.md5(fichier).hexdigest() + h.sha256(fichier).hexdigest())


def confronter(chemin_temoign: pathlib.Path) -> int:
    temoin = json.loads(chemin_temoign.read_text(encoding="utf-8"))
    verifier_signature(temoin)
    print(f"[natif] le témoin signé VERT — {temoin.get('machine')} · "
          f"{temoin.get('windows')} · {temoin.get('horodatage')}")
    ecarts = 0
    for t in temoin.get("temoins", []):
        attendu = t.get("attendu")      # posé par le scénario consigné
        rendu = t.get("disque")
        if attendu is not None and rendu != attendu:
            print(f"ROUGE TEMOIN-DIVERGENT : {t['id']} — attendu "
                  f"{attendu[:16]}… rendu {str(rendu)[:16]}…")
            ecarts += 1
        else:
            print(f"VERT  {t['id']}")
    if ecarts:
        print(f"LA CONFRONTATION : {ecarts} écart(s) — le refus nommé "
              "TEMOIN-DIVERGENT")
        return 2
    print("LA CONFRONTATION : VERT — les octets scellés au vrai Windows "
          "rendent les attentes du laboratoire (le régime NATIF, jamais "
          "confondu avec le terrain)")
    return 0


if __name__ == "__main__":
    raise SystemExit(confronter(pathlib.Path(sys.argv[1])))
