#!/usr/bin/env python3
"""signer_temoin.py — la signature Ed25519 du témoin natif (au CI :
la clé privée au SECRET, jamais au dépôt)."""
import json, os, sys
from nacl.signing import SigningKey
corps = json.loads(open(sys.argv[1], encoding="utf-8").read())
cle_hex = os.environ.get("NATIF_SIGNING_KEY")
if not cle_hex:
    raise SystemExit("SECRET-ABSENT : NATIF_SIGNING_KEY (la clé du CI) "
                     "n'est pas dans l'environnement — le témoin ne sera "
                     "jamais signé sans elle")
sk = SigningKey(bytes.fromhex(cle_hex))
temoin = {**corps, "cle_publique": sk.verify_key.encode().hex()}
temoin["signature"] = sk.sign(json.dumps(
    {k: v for k, v in temoin.items() if k != "signature"},
    sort_keys=True).encode()).signature.hex()
open(sys.argv[2], "w", encoding="utf-8").write(json.dumps(temoin, indent=1))
print(f"[natif] le témoin signé → {sys.argv[2]}")
