#!/usr/bin/env python3
"""carte_sceau.py — Carte de la lignée sceau (m7, D34 échelon 2) : génération 1 propre.

Adaptateur de carte_m2.py (même mécanique : Argon2id + HKDF + XChaCha20-Poly1305
+ Ed25519, mêmes listes blanches D15) avec les constantes de la lignée sceau :
sel Argon2id DISTINCT (D34 : « sel de dérivation distinct » par lignée),
contexte HKDF propre, génération 1 — mais CLÉS PROJET PARTAGÉES (D27 :
triade/.keys/, la signature Ed25519 est celle du projet ; une seule lignée
de secrets). Miroir de carte_ah.py (m6).
"""

from __future__ import annotations

import hashlib
import os
import sys

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_RACINE, "m2"))
import carte_m2 as base  # mécanique commune (D27/D15) — seul le sel diverge

ICI = os.path.dirname(os.path.abspath(__file__))
CARTE_DIR = os.path.join(ICI, "carte")

FRAGMENTS = base.FRAGMENTS          # frag-loc/con/prf/bld (FORMAT_CARTE § 3)
GENERATION = 1                      # génération 1 de la lignée sceau

# Sel Argon2id PROPRE à la lignée sceau (D34 : sel distinct — public par
# conception, la phrase maîtresse reste le secret ; le sel fixe garantit la
# dérivation reproductible de CETTE lignée indépendamment de m0-m6).
ARGON2_SALT = hashlib.sha256(b"TRIADE-M7-sceau-carte-argon2id-v1").digest()

PROFILS = "x86-64-linux-elf64"

ErreurCarte = base.ErreurCarte


def charger_secrets(interactif: bool = True) -> tuple[bytes, bytes]:
    """Clés projet partagées (D27) — délégué à la source commune."""
    return base.charger_secrets(interactif=interactif)


def cle_maitresse(phrase: bytes) -> bytes:
    """Argon2id aux planchers § 3.1, sel de la lignée sceau (distinct)."""
    from argon2.low_level import Type, hash_secret_raw
    return hash_secret_raw(
        secret=phrase, salt=ARGON2_SALT,
        time_cost=3, memory_cost=65536, parallelism=1,
        hash_len=32, type=Type.ID,
    )


def cle_fragment(maitre: bytes, nom_fragment: str) -> bytes:
    """HKDF-SHA256, contexte propre à la lignée sceau."""
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    hkdf = HKDF(
        algorithm=hashes.SHA256(), length=32,
        salt=b"TRIADE-carte-M7-sceau",
        info=f"frag={nom_fragment};gen={GENERATION}".encode("ascii"),
    )
    return hkdf.derive(maitre)


def chiffrer_fragment(maitre: bytes, nom_fragment: str, clair: bytes) -> bytes:
    cle = cle_fragment(maitre, nom_fragment)
    import secrets
    from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_encrypt
    nonce = secrets.token_bytes(24)
    ct = crypto_aead_xchacha20poly1305_ietf_encrypt(
        clair, nom_fragment.encode("ascii"), nonce, cle)
    return nonce + ct


def dechiffrer_fragment(maitre: bytes, nom_fragment: str, blob: bytes) -> bytes:
    if len(blob) < 24 + 16:
        raise ErreurCarte(f"{nom_fragment} : blob trop court")
    from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_decrypt
    nonce, ct = blob[:24], blob[24:]
    try:
        return crypto_aead_xchacha20poly1305_ietf_decrypt(
            ct, nom_fragment.encode("ascii"), nonce, cle_fragment(maitre, nom_fragment))
    except Exception as exc:
        raise ErreurCarte(f"{nom_fragment} : dechiffrement impossible ({exc})") from exc


def paire_cles(graine: bytes):
    return base.paire_cles(graine)


def signer(prive, entete: bytes, fragments: dict) -> bytes:
    return base.signer(prive, entete, fragments)


def verifier_signature(pub: bytes, entete: bytes, fragments: dict, signature: bytes) -> None:
    base.verifier_signature(pub, entete, fragments, signature)


def construire_entete(racine: bytes) -> bytes:
    lignes = [
        "[carte] version=0.4.0 generation=1",
        f"  algo_hachage     : {base.ALGO_HACHAGE}",
        f"  algo_signature   : {base.ALGO_SIGNATURE}",
        f"  algo_chiffrement : {base.ALGO_CHIFFREMENT}",
        f"  profils          : {PROFILS}",
        f"  empreinte_racine : sha256:{racine.hex()}",
    ]
    return ("\n".join(lignes) + "\n").encode("ascii")


def ecrire_carte(entete: bytes, fragments: dict, signature: bytes, pub: bytes) -> None:
    os.makedirs(CARTE_DIR, exist_ok=True)
    for nom in FRAGMENTS:
        with open(os.path.join(CARTE_DIR, nom + ".bin"), "wb") as f:
            f.write(fragments[nom])
    with open(os.path.join(CARTE_DIR, "entete.txt"), "wb") as f:
        f.write(entete)
    with open(os.path.join(CARTE_DIR, "signature.bin"), "wb") as f:
        f.write(signature)
    with open(os.path.join(CARTE_DIR, "cle-publique.txt"), "w", encoding="ascii") as f:
        f.write(pub.hex() + "\n")


def lire_carte() -> tuple[bytes, dict, bytes, bytes]:
    fragments = {}
    for nom in FRAGMENTS:
        chemin = os.path.join(CARTE_DIR, nom + ".bin")
        if not os.path.exists(chemin):
            raise ErreurCarte(f"fragment absent : {chemin}")
        with open(chemin, "rb") as f:
            fragments[nom] = f.read()
    for nom, fich in (("entete", "entete.txt"), ("signature", "signature.bin")):
        chemin = os.path.join(CARTE_DIR, fich)
        if not os.path.exists(chemin):
            raise ErreurCarte(f"{nom} absent : {chemin}")
    with open(os.path.join(CARTE_DIR, "entete.txt"), "rb") as f:
        entete = f.read()
    with open(os.path.join(CARTE_DIR, "signature.bin"), "rb") as f:
        signature = f.read()
    with open(os.path.join(CARTE_DIR, "cle-publique.txt"), encoding="ascii") as f:
        pub = bytes.fromhex(f.read().strip())
    return entete, fragments, signature, pub
