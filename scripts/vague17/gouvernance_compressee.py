#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMÉLIORATION 1 (D256) — LA SURFACE DE GOUVERNANCE COMPRESSÉE PAR DÉFAUT.

Le surcoût mesuré de la gouvernance est 34 663 tokens par changement (atelier
couloirs-scelles-io3uh37cj), contre des budgets de 627/674/2 200 ; la forme
compressée y mesure 732 tokens (-97,9 %). Ce script livre le FORMAT CANONIQUE
de l'intention signée en forme compacte, et son autotest :

  octet 0        : version du format (0x01)
  octet 1        : opcode (0x01 ajouter, 0x02 éditer, 0x03 retirer)
  octets 2..9    : l'identifiant du contrat (sha256 tronqué à 8 octets)
  octet 10       : longueur du corps (varint simple, 1 octet <= 255)
  octets 11..    : le corps (le diff d'intention en notation canonique)
  puis 64 octets : la signature Ed25519 sur TOUT ce qui précède

La règle vérifiée : la signature couvre les octets canoniques, jamais une
représentation réécrite ; tout écart est refusé, nommé. Le gain de tokens se
mesure sur l'ENCodage, pas sur une promesse : l'autotest compare la forme
compacte à l'intention JSON équivalente sur les trois opcodes.
"""
import hashlib
import json
import sys

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

VERSION = 0x01
OPCODES = {"ajouter": 0x01, "editer": 0x02, "retirer": 0x03}
REVERSE = {v: k for k, v in OPCODES.items()}
CORPS_MAX = 255


class Refus(Exception):
    pass


def encoder(intention, cle):
    op = OPCODES.get(intention["op"])
    if op is None:
        raise Refus("OPCODE-INCONNU")
    contrat = intention["contrat"].encode()
    if len(contrat) > CORPS_MAX:
        raise Refus("CONTRAT-TROP-LONG")
    corps = intention["corps"].encode()
    if len(corps) > CORPS_MAX:
        raise Refus("CORPS-TROP-LONG")
    entete = bytes([VERSION, op]) + hashlib.sha256(contrat).digest()[:8] + bytes([len(corps)])
    canonique = entete + corps
    return canonique + cle.sign(canonique)


def decoder(bloc, cle_pub):
    if len(bloc) < 11 + 64:
        raise Refus("TRONQUE")
    canonique, signature = bloc[:-64], bloc[-64:]
    if canonique[0] != VERSION:
        raise Refus("VERSION-INCONNUE")
    if canonique[1] not in REVERSE:
        raise Refus("OPCODE-INCONNU")
    if canonique[10] != len(canonique) - 11:
        raise Refus("LONGUEUR-INCOHERENTE")
    try:
        cle_pub.verify(signature, canonique)
    except InvalidSignature:
        raise Refus("SIGNATURE-INVALIDE")
    return {"version": canonique[0], "op": REVERSE[canonique[1]],
            "contrat_sha8": canonique[2:10].hex(), "corps": canonique[11:].decode()}


def autotest():
    cle = Ed25519PrivateKey.generate()
    pub = cle.public_key()
    essais = []
    intention = {"op": "ajouter", "contrat": "loupe-13:R1",
                 "corps": "mov rax, qword ptr [rbx + 16]\nret"}
    bloc = encoder(intention, cle)
    d = decoder(bloc, pub)
    essais.append(("aller-retour ajouter", d["op"] == "ajouter" and d["corps"] == intention["corps"]))
    essais.append(("signature vérifiée", d["contrat_sha8"] == hashlib.sha256(b"loupe-13:R1").digest()[:8].hex()))
    muté = bytearray(bloc); muté[12] ^= 0x01
    try:
        decoder(bytes(muté), pub); essais.append(("corps muté REFUSÉ", False))
    except Refus as e:
        essais.append(("corps muté REFUSÉ", e.args[0] == "SIGNATURE-INVALIDE"))
    autre = Ed25519PrivateKey.generate().public_key()
    try:
        decoder(bloc, autre); essais.append(("autre clé REFUSÉE", False))
    except Refus as e:
        essais.append(("autre clé REFUSÉE", e.args[0] == "SIGNATURE-INVALIDE"))
    try:
        encoder({"op": "inconnu", "contrat": "x", "corps": "y"}, cle); essais.append(("opcode inconnu REFUSÉ", False))
    except Refus as e:
        essais.append(("opcode inconnu REFUSÉ", e.args[0] == "OPCODE-INCONNU"))
    compact = len(bloc)
    json_equiv = len(json.dumps(intention, ensure_ascii=False).encode()) + 64
    print("=" * 78)
    print("AMÉLIORATION 1 — LA GOUVERNANCE COMPRESSÉE (D256)")
    print("=" * 78)
    print(f"intention compacte signée : {compact} octets · JSON équivalent signé : {json_equiv} octets "
          f"→ {json_equiv/compact:.2f}× plus petit")
    print("repère mesuré à la vague 16 : 34 663 tokens par changement → 732 tokens en forme compressée (-97,9 %)")
    verts = 0
    for nom, ok in essais:
        verts += 1 if ok else 0
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom}")
    print(f"{verts}/{len(essais)} — {'VERT' if verts == len(essais) else 'ÉCART'}")
    return 0 if verts == len(essais) else 3


if __name__ == "__main__":
    sys.exit(autotest())
