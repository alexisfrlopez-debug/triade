#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit l'annexe terrain_jetons.bin (D48, sup-35:P1) — TRIADE.

Format (contrat sup-35) : 4 champs ASCII NUL-terminés contigus, dans
l'ordre client_id, client_secret, refresh_token, token_uri — 480 octets
maximum au total. L'annexe est lue par superviseur.exe (test T3) pour
rafraîchir le jeton OAuth puis téléverser le journal du run dans le
dossier test du Drive, par la MÊME voie que drive_sync.py.

Sécurité (interdit 11) : les valeurs viennent de .gdrive/ (jamais dans
le dépôt) et l'annexe s'écrit DANS .gdrive/ (ignoré par git). Elle est
poussée au dossier test du Drive par le canal de livraison uniquement —
voir scripts/drive_livraison.py --dossier-test.
"""

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
GDRIVE = REPO / ".gdrive"
SOURCE = GDRIVE / "oauth_token_relais.json"
CIBLE = GDRIVE / "terrain_jetons.bin"
MAX_TOTAL = 480          # sup-35:P1
CHAMPS = ("client_id", "client_secret", "refresh_token", "token_uri")


def construire() -> bytes:
    with open(SOURCE, encoding="utf-8") as f:
        tok = json.load(f)
    annexe = b""
    for champ in CHAMPS:
        valeur = tok[champ].encode("ascii")
        if b"\x00" in valeur:
            raise SystemExit(f"[annexe] ERREUR : NUL interdit dans {champ}")
        annexe += valeur + b"\x00"
    if len(annexe) > MAX_TOTAL:
        raise SystemExit(f"[annexe] ERREUR : {len(annexe)} o > {MAX_TOTAL} o (sup-35:P1)")
    return annexe


def main() -> int:
    if not SOURCE.is_file():
        print(f"[annexe] ERREUR FATALE : {SOURCE} absent", file=sys.stderr)
        return 2
    annexe = construire()
    with open(CIBLE, "wb") as f:
        f.write(annexe)
    # Vérification de relecture : 4 champs NUL-terminés, total ≤ 480.
    with open(CIBLE, "rb") as f:
        relu = f.read()
    champs = relu.split(b"\x00")[:-1]
    assert relu == annexe and len(champs) == 4 and len(relu) <= MAX_TOTAL
    print(f"[annexe] {CIBLE.name} : {len(relu)} octets, 4 champs "
          f"({', '.join(f'{len(c)} o' for c in champs)}), "
          f"limite {MAX_TOTAL} o — round-trip OK")
    print("[annexe] RAPPEL : fichier de secret — jamais committé "
          "(interdit 11), livraison par --dossier-test uniquement")
    return 0


if __name__ == "__main__":
    sys.exit(main())
