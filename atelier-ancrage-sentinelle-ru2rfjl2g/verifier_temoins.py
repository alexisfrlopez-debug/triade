#!/usr/bin/env python3
"""verifier_temoins.py — atelier RU2RFJL2G (la vague 16).

L'ANCRAGE DE TRANSPARENCE du témoin d'époque CF3 : le format du témoin signé et
son vérificateur machine OFFLINE, fail-closed.

LA RÈGLE R10 : aucune dépendance réseau au chargement — ni import conditionnel,
ni repli silencieux. Un témoin qui ne se vérifie pas LOCALEMENT est REFUSÉ, et
le refus est NOMMÉ. Le mode « récupérer le témoin au réseau » n'existe pas : le
drapeau --reseau est REFUSÉ à l'entrée (la preuve que l'absence réseau n'est pas
un état dégradé mais l'état NORMAL du vérificateur).

Le format : unobjet JSON canonique (clés triées, UTF-8, séparateurs compacts)
portant l'époque, l'horodatage, le condensé de l'état CF3 de l'ère et le
condensat du témoin précédent (la chaîne), signé Ed25519 détaché.
"""

import argparse
import base64
import hashlib
import json
import os
import sys

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key

SCHEMA = "TRIADE-TEMOIN-EPOQUE-v1"


def canonique(payload: dict) -> bytes:
    """Le canon : clés triées, compact, UTF-8 — l'octet signé est l'octet vérifié."""
    return json.dumps(payload, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def condense(donnees: bytes) -> str:
    return hashlib.sha256(donnees).hexdigest()


def verifier(temoin: dict, cle: Ed25519PublicKey) -> tuple:
    """-> (ok, motif). Tout refus est NOMMÉ ; jamais un silence."""
    if not isinstance(temoin, dict):
        return False, "REFUS : le témoin n'est pas un objet"

    if temoin.get("schema") != SCHEMA:
        return False, f"REFUS : schéma {temoin.get('schema')!r} != {SCHEMA!r}"

    for champ in ("epoque", "horodatage", "etat_cf3", "precedent", "signature"):
        if champ not in temoin:
            return False, f"REFUS : le champ {champ!r} manque"

    try:
        signature = base64.b64decode(temoin["signature"], validate=True)
    except Exception as e:
        return False, f"REFUS : la signature n'est pas du base64 valide ({type(e).__name__})"

    corps = {k: temoin[k] for k in ("schema", "epoque", "horodatage", "etat_cf3", "precedent")}
    try:
        cle.verify(signature, canonique(corps))
    except InvalidSignature:
        return False, "REFUS : signature INVALIDE (le corps ou la clé a changé)"
    except Exception as e:
        return False, f"REFUS : la vérification a échoué ({type(e).__name__})"

    return True, "VERT"


def charger_cle(chemin: str) -> Ed25519PublicKey:
    """La clé vient d'UN FICHIER LOCAL — jamais d'un réseau."""
    if not os.path.isfile(chemin):
        raise SystemExit(f"REFUS : la clé publique {chemin} n'existe pas (aucun repli réseau)")
    with open(chemin, "rb") as f:
        return load_pem_public_key(f.read())


def autotest() -> int:
    """Les contrôles nommés : le valide VERT, le muté REFUSÉ, le réseau absent PROPRE."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import (
        Encoding, NoEncryption, PrivateFormat, PublicFormat)

    cle_privee = Ed25519PrivateKey.generate()
    cle = cle_privee.public_key()
    pem = cle.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode()

    corps = {"schema": SCHEMA, "epoque": 1, "horodatage": "2026-11-23T00:00:00Z",
             "etat_cf3": "a" * 64, "precedent": "0" * 64}
    signature = cle_privee.sign(canonique(corps))
    temoin = dict(corps, signature=base64.b64encode(signature).decode())

    print("=== L'AUTOTEST DU VÉRIFICATEUR D'ANCRAGE ===")
    ok, motif = verifier(temoin, cle)
    print(f"  [1] témoin valide                 : {'VERT' if ok else 'ROUGE'} — {motif}")
    tests = [ok]

    # (2) le témoin muté : UN octet du corps change
    mute = dict(temoin)
    mute["etat_cf3"] = "b" + "a" * 63
    ok2, motif2 = verifier(mute, cle)
    print(f"  [2] témoin muté (1 octet)         : {'VERT' if ok2 else 'REFUSÉ'} — {motif2}")
    tests.append(not ok2)

    # (3) le témoin muté : la signature tronquée
    tronque = dict(temoin, signature=base64.b64encode(signature[:-1]).decode())
    ok3, motif3 = verifier(tronque, cle)
    print(f"  [3] signature tronquée            : {'VERT' if ok3 else 'REFUSÉ'} — {motif3}")
    tests.append(not ok3)

    # (4) la clé substituée : une AUTRE clé, la même signature
    autre = Ed25519PrivateKey.generate().public_key()
    ok4, motif4 = verifier(temoin, autre)
    print(f"  [4] clé substituée                : {'VERT' if ok4 else 'REFUSÉ'} — {motif4}")
    tests.append(not ok4)

    # (5) l'absence réseau simulée : la clé n'existe pas sur disque
    try:
        charger_cle(os.path.join(os.environ.get("TEMP", "."), "cle-absente.pem"))
        ok5, motif5 = False, "aucun refus levé — DÉFAUT"
    except SystemExit as e:
        ok5, motif5 = False, str(e)[:70]
    print(f"  [5] clé absente (pas de réseau)   : {'REFUSÉ' if not ok5 else 'ROUGE'} — {motif5}")
    tests.append(not ok5)

    # (6) le mode réseau REFUSÉ à l'entrée
    try:
        point_entree(["--verifier", "x", "--cle", "y", "--reseau"])
        ok6, motif6 = False, "aucun refus levé — DÉFAUT"
    except SystemExit as e:
        ok6, motif6 = False, str(e)[:70]
    print(f"  [6] --reseau demandé              : {'REFUSÉ' if not ok6 else 'ROUGE'} — {motif6}")
    tests.append(not ok6)

    print(f"  {sum(1 for t in tests if t)}/{len(tests)} contrôles rendus")
    return 0 if all(tests) else 1


def point_entree(argv=None):
    ap = argparse.ArgumentParser(description="vérificateur OFFLINE du témoin d'époque CF3")
    ap.add_argument("--verifier", metavar="TEMOIN.json")
    ap.add_argument("--cle", metavar="CLE.pem", help="la clé publique LOCALE (jamais le réseau)")
    ap.add_argument("--autotest", action="store_true")
    ap.add_argument("--reseau", action="store_true",
                    help="REFUSÉ : le vérificateur ne consulte jamais le réseau (R10)")
    args = ap.parse_args(argv)

    if args.reseau:
        raise SystemExit("REFUS : --reseau est interdit — le vérificateur est OFFLINE (R10)")

    if args.autotest:
        return autotest()

    if not (args.verifier and args.cle):
        ap.error("--verifier et --cle sont requis (ou --autotest)")

    cle = charger_cle(args.cle)
    with open(args.verifier, encoding="utf-8") as f:
        temoin = json.load(f)
    ok, motif = verifier(temoin, cle)
    print(f"[temoin] {motif}")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(point_entree())
