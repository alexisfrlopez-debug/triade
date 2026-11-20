#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cg_gouverne.py — LES GESTES DE GOUVERNANCE DU BRAS C+G (les étapes de
la liste fixe M4) : --garde (la vérification des SIX intentions signées),
--cristallisation (la chaîne re-vérifiée), --kit (le gabarit assemblé —
le geste du terrain attend le maître)."""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-cg-3a91o5whb"


def cle_pub():
    pem = (ICI / "cle_session_lab.pub").read_bytes()
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    return load_pem_public_key(pem)


def garde() -> int:
    """(g1) LA GARDE DES INTENTIONS : chaque signature vérifiée contre
    le sha256 de la spec — LE REFUS NOMMÉ si une seule diverge."""
    pub = cle_pub().public_bytes(serialization.Encoding.Raw,
                                 serialization.PublicFormat.Raw)
    cle = Ed25519PublicKey.from_public_bytes(pub)
    verts, codes = 0, 0
    for f in sorted((ICI / "intentions").glob("*.json")):
        d = json.loads(f.read_text())
        try:
            cle.verify(bytes.fromhex(d["signature_ed25519"]),
                       d["sha256_spec"].encode())
            verts += 1
        except Exception:
            codes += 1
            print(f"[REFUS] l'intention {d['unite']} : signature DIVERGENTE")
    print(f"[garde] les intentions signées : {verts} VERT, {codes} refus")
    return 0 if codes == 0 else 2


def cristallisation() -> int:
    """(g2) LA CHAÎNE re-vérifiée : chaque empreinte d'unité recalculée,
    la signature finale vérifiée."""
    pub = cle_pub().public_bytes(serialization.Encoding.Raw,
                                 serialization.PublicFormat.Raw)
    cle = Ed25519PublicKey.from_public_bytes(pub)
    ch = json.loads((ICI / "cristallisation" / "chaine.json").read_text())
    ok = 0
    for u in ch["chaine"]:
        attendu = hashlib.sha256((u["precedente"] + u["sha256_source"] +
                                  u["sha256_dll"]).encode()).hexdigest()
        if attendu == u["empreinte_unite"]:
            ok += 1
    try:
        cle.verify(bytes.fromhex(ch["signature_ed25519"]),
                   ch["empreinte_finale"].encode())
        sig_ok = True
    except Exception:
        sig_ok = False
    print(f"[cristallisation] {ok}/{len(ch['chaine'])} empreintes "
          f"recoupées ; la signature finale "
          f"{'VÉRIFIÉE' if sig_ok else 'REFUSÉE'}")
    return 0 if ok == len(ch["chaine"]) and sig_ok else 2


def kit() -> int:
    """(g4) LE GABARIT DE KIT assemblé : le déploiement terrain (le
    geste du maître attendu — jamais simulé)."""
    kit = ICI / "kit-cg"
    kit.mkdir(exist_ok=True)
    for f in sorted(ICI.glob("*-cg.dll")):
        (kit / f.name).write_bytes(f.read_bytes())
    for f in sorted((ICI / "intentions").glob("*.json")):
        (kit / f.name).write_text(f.read_text(), encoding="utf-8")
    (kit / "LISEZMOI-KIT-CG.txt").write_text(
        "LE KIT C+G — les pièces gcc-O2 gouvernées (les intentions signées,\n"
        "la chaîne de cristallisation) — le geste du TERRAIN attend le\n"
        "maître : le kit 1-clic de campagne vit à son gabarit, jamais\n"
        "simulé ici (l'écart nommé).\n", encoding="utf-8")
    print(f"[kit] {len(list(kit.iterdir()))} pièces au gabarit "
          f"(le terrain au geste du maître)")
    return 0


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--garde":
        sys.exit(garde())
    if arg == "--cristallisation":
        sys.exit(cristallisation())
    if arg == "--kit":
        sys.exit(kit())
    print("usage: cg_gouverne.py --garde|--cristallisation|--kit")
    sys.exit(1)
