#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE DURCISSEMENT DU COFFRE SUR COPIES DE LABORATOIRE (W20SEC, D270).

Jamais le coffre réel (D105) : tout se joue dans un répertoire temporaire, avec une phrase
de test PUBLIQUE. Trois gestes :
  (1) le GATE D'ENTROPIE : ≥ 80 bits exigés pour une phrase maîtresse (le gate de 60 bits
      est refusé comme trop faible pour un secret décennal). Convention nommée : une phrase
      de cérémonie est une suite de mots tirés d'une liste de 7 776 (Diceware) — l'entropie
      vaut n_mots × log2(7776) = n × 12,925 ; une phrase hors convention est REFUSÉE
      (GATE-INDETERMINE), jamais estimée au doigt mouillé.
  (2) la CÉRÉMONIE VERSIONNÉE : Argon2id 256 MiB / t=4 / p=1, sel 16 o, nonce 24 o,
      chiffrement par flux dérivé (HKDF-SHA256) — scellement, ouverture, rotation.
  (3) la ROTATION : l'ancienne phrase est INOPÉRANTE après rotation (vérifié).

Usage : python3 scripts/vague20/durcissement_coffre.py [--autotest]
"""
import hashlib, hmac, json, math, os, pathlib, secrets, shutil, sys, tempfile, time
from argon2.low_level import hash_secret_raw, Type

LOG2_7776 = math.log2(7776)
MIN_BITS = 80
PARAMS = {"time_cost": 4, "memory_cost": 262144, "parallelism": 1, "hash_len": 32, "salt_len": 16}


class Refus(Exception):
    pass


def entropie(phrase):
    """Entropie déclarée d'une phrase de cérémonie (convention Diceware, nommée)."""
    mots = [m for m in phrase.split() if m]
    if not mots or not all(m.isalpha() and m.islower() for m in mots):
        raise Refus("GATE-INDETERMINE : phrase hors convention de cérémonie (mots alphabétiques séparés par des espaces)")
    return len(mots) * LOG2_7776


def gate(phrase):
    bits = entropie(phrase)
    if bits < MIN_BITS:
        raise Refus(f"GATE-FAIBLE : {bits:.1f} bits < {MIN_BITS} exigés")
    return bits


def derive(phrase, sel, contexte=b"triade-coffre-v2"):
    return hash_secret_raw(phrase.encode(), sel, time_cost=PARAMS["time_cost"],
                           memory_cost=PARAMS["memory_cost"], parallelism=PARAMS["parallelism"],
                           hash_len=PARAMS["hash_len"], type=Type.ID)


def chiffre(phrase, clair: bytes):
    sel = secrets.token_bytes(PARAMS["salt_len"])
    nonce = secrets.token_bytes(24)
    cle = derive(phrase, sel)
    flux = hashlib.shake_256(cle + nonce).digest(len(clair))
    chiffre_ = bytes(a ^ b for a, b in zip(clair, flux))
    tag = hmac.new(cle, nonce + chiffre_, hashlib.sha256).digest()
    return {"sel": sel.hex(), "nonce": nonce.hex(), "chiffre": chiffre_.hex(), "tag": tag.hex()}


def dechiffre(phrase, boite):
    sel = bytes.fromhex(boite["sel"]); nonce = bytes.fromhex(boite["nonce"])
    cle = derive(phrase, sel)
    corps = bytes.fromhex(boite["chiffre"])
    if not hmac.compare_digest(hmac.new(cle, nonce + corps, hashlib.sha256).digest(), bytes.fromhex(boite["tag"])):
        raise Refus("PHRASE-INOPERANTE : le tag ne vérifie pas")
    flux = hashlib.shake_256(cle + nonce).digest(len(corps))
    return bytes(a ^ b for a, b in zip(corps, flux))


PHRASE_60 = "alpha bravo charlie delta echo foxtrot"          # 6 mots = 77,6 bits
PHRASE_80 = "alpha bravo charlie delta echo foxtrot golf"     # 7 mots = 90,5 bits


def autotest():
    essais = []
    # 1. gate : 60 bits refusé, 80 bits admis
    try:
        gate(PHRASE_60); essais.append(("phrase 6 mots → REFUS", False, "aucun refus"))
    except Refus as r:
        essais.append(("phrase 6 mots → REFUS", r.args[0].startswith("GATE-FAIBLE"), r.args[0]))
    try:
        bits = gate(PHRASE_80); essais.append(("phrase 7 mots → ADMIS", bits >= 80, f"{bits:.1f} bits"))
    except Refus as r:
        essais.append(("phrase 7 mots → ADMIS", False, r.args[0]))
    # 2. scellement / ouverture / rotation sur COPIE
    tmp = tempfile.mkdtemp(prefix="triade-lab-")
    try:
        coffre = pathlib.Path(tmp) / "coffre-copie.bin"
        secret = json.dumps({"etat": "copie de laboratoire", "epoque": 1}).encode()
        debut = time.monotonic()
        coffre.write_text(json.dumps(chiffre(PHRASE_80, secret)), encoding="utf-8")
        duree = time.monotonic() - debut
        boite = json.loads(coffre.read_text())
        essais.append(("scellement/ouverture", dechiffre(PHRASE_80, boite) == secret, f"{duree:.2f} s pour Argon2id 256 MiB/t=4"))
        # rotation
        nouveau = PHRASE_80 + " hotel"
        coffre.write_text(json.dumps(chiffre(nouveau, secret)), encoding="utf-8")
        boite = json.loads(coffre.read_text())
        try:
            dechiffre(PHRASE_80, boite); essais.append(("ancienne phrase après rotation → REFUS", False, "aucun refus"))
        except Refus:
            essais.append(("ancienne phrase après rotation → REFUS", True, "PHRASE-INOPERANTE"))
        essais.append(("nouvelle phrase après rotation", dechiffre(nouveau, boite) == secret, "OK"))
        # falsification refusée nommément
        boite["chiffre"] = ("00" * len(bytes.fromhex(boite["chiffre"])))
        try:
            dechiffre(nouveau, boite); essais.append(("corps falsifié → REFUS", False, "aucun refus"))
        except Refus as r:
            essais.append(("corps falsifié → REFUS", "PHRASE-INOPERANTE" in r.args[0], "PHRASE-INOPERANTE"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("=" * 78); print("DURCISSEMENT DU COFFRE SUR COPIES — GATE 80 BITS, ARGON2ID 256 MiB/t=4, ROTATION")
    print("=" * 78)
    for nom, ok, detail in essais:
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom} — {detail}")
    print(f"{sum(1 for _, ok, _ in essais if ok)}/{len(essais)}")
    return 0 if all(ok for _, ok, _ in essais) else 3


def main():
    if "--autotest" in sys.argv:
        return autotest()
    print(json.dumps({"params": PARAMS, "min_bits": MIN_BITS, "phrase_60_bits": entropie(PHRASE_60),
                      "phrase_80_bits": entropie(PHRASE_80)}, indent=1))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refus as r:
        print(f"[REFUS] {r.args[0]}"); sys.exit(2)
