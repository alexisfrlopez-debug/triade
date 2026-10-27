#!/usr/bin/env python3
"""carte_terrain.py — Couche C du jalon terrain : carte lignée terrain, génération 5.

Même format que les cartes M0/M1/démo (docs/FORMAT_CARTE.md) — quatre
fragments chiffrés XChaCha20-Poly1305, clés dérivées de la phrase maîtresse
par Argon2id puis HKDF, empreinte racine SHA-256, signature Ed25519 :

  - GÉNÉRATION 5 : les clés de fragments dérivent d'un contexte propre au
    terrain ; la même phrase maîtresse protège toutes les lignées — la
    génération 5 indexe l'ensemble des blocs embarqués dans superviseur.exe
    (io M0, libc M1, tcp-06 M2, win démo, sup terrain) ;
  - CLÉS PROJET : les secrets vivent dans triade/.keys/ (D27), partagés ;
  - MULTI-ARTEFACTS : la carte terrain vérifie les héritages R7 contre
    hello.exe, selftest.exe, echo.exe et demo.exe en plus de superviseur.exe.

Les secrets ne sont jamais committés (chmod 600, .gitignore). La phrase
maîtresse doit vivre dans le coffre du développeur.
"""

from __future__ import annotations

import hashlib
import os
import secrets

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from nacl.bindings import (
    crypto_aead_xchacha20poly1305_ietf_decrypt,
    crypto_aead_xchacha20poly1305_ietf_encrypt,
)

# --- Constantes du projet (terrain, D48) --------------------------------------

_ICI = os.path.dirname(os.path.abspath(__file__))
_RACINE = os.path.dirname(_ICI)
KEYS_DIR = os.path.join(_RACINE, ".keys")
CARTE_DIR = os.path.join(_ICI, "carte")

FRAGMENTS = ("frag-loc", "frag-con", "frag-prf", "frag-bld")
GENERATION = 5

# Sel Argon2id propre à la génération 5 (public par conception — la phrase
# maîtresse est le secret ; le sel fixe garantit la dérivation reproductible).
ARGON2_SALT = hashlib.sha256(b"TRIADE-TERRAIN-carte-argon2id-v1").digest()  # 32 o

# Listes blanches D15 (FORMAT_CARTE § 3.1) — vérifiées au chargement.
BLANCHE_HACHAGE = {
    "sha256", "sha384", "sha512", "sha3-256", "sha3-512",
    "blake2b-256", "blake2b-512", "blake3",
}
BLANCHE_SIGNATURE = {"ed25519", "ed448", "ecdsa-p256-rfc6979", "ecdsa-p384-rfc6979"}
BLANCHE_CHIFFREMENT = {"xchacha20poly1305", "chacha20poly1305", "aes-256-gcm"}

ALGO_HACHAGE = "sha256"
ALGO_SIGNATURE = "ed25519"
ALGO_CHIFFREMENT = "xchacha20poly1305"
PROFILS = "x86-64-win11-pe"


class ErreurCarte(Exception):
    """Tout échec de chiffrement, de signature ou de vérification (fail-closed)."""


# --- Secrets : chargement (partagés avec M0/M1, D27) --------------------------

def _ecrire_secret(chemin: str, donnees: bytes, note: str) -> None:
    with open(chemin, "wb") as f:
        f.write(donnees)
    os.chmod(chemin, 0o600)
    print(f"[cles] {note} : {os.path.basename(chemin)} (chmod 600, hors depôt)")


def charger_secrets(interactif: bool = True) -> tuple[bytes, bytes]:
    """Retourne (phrase_maîtresse, graine_ed25519) — jamais générés ici si absents."""
    os.makedirs(KEYS_DIR, exist_ok=True)
    os.chmod(KEYS_DIR, 0o700)
    chemin_phrase = os.path.join(KEYS_DIR, "passphrase.txt")
    chemin_graine = os.path.join(KEYS_DIR, "ed25519.seed")
    if not os.path.exists(chemin_phrase) or not os.path.exists(chemin_graine):
        sys_path = os.path.join(_RACINE, "m0")
        import sys
        if sys_path not in sys.path:
            sys.path.insert(0, sys_path)
        import carte_m0
        carte_m0.charger_secrets(interactif=interactif)
    with open(chemin_phrase, "rb") as f:
        phrase = f.read().strip()
    with open(chemin_graine, "rb") as f:
        graine = f.read().strip()
    return phrase, graine


# --- Dérivation de clés ------------------------------------------------------

def cle_maitresse(phrase: bytes) -> bytes:
    """Argon2id : 64 Mio, 3 itérations, parallélisme 1 (planchers FORMAT_CARTE § 3.1)."""
    return hash_secret_raw(
        secret=phrase, salt=ARGON2_SALT,
        time_cost=3, memory_cost=65536, parallelism=1,
        hash_len=32, type=Type.ID,
    )


def cle_fragment(maitre: bytes, nom_fragment: str) -> bytes:
    """HKDF-SHA256 avec contexte distinct par fragment et par génération."""
    hkdf = HKDF(
        algorithm=hashes.SHA256(), length=32,
        salt=b"TRIADE-carte-TERRAIN",
        info=f"frag={nom_fragment};gen={GENERATION}".encode("ascii"),
    )
    return hkdf.derive(maitre)


def chiffrer_fragment(maitre: bytes, nom_fragment: str, clair: bytes) -> bytes:
    """XChaCha20-Poly1305, nonce aléatoire 192 bits, AAD = rôle du fragment."""
    cle = cle_fragment(maitre, nom_fragment)
    nonce = secrets.token_bytes(24)  # 192 bits
    ct = crypto_aead_xchacha20poly1305_ietf_encrypt(clair, nom_fragment.encode("ascii"), nonce, cle)
    return nonce + ct


def dechiffrer_fragment(maitre: bytes, nom_fragment: str, blob: bytes) -> bytes:
    if len(blob) < 24 + 16:
        raise ErreurCarte(f"{nom_fragment} : blob trop court")
    nonce, ct = blob[:24], blob[24:]
    try:
        return crypto_aead_xchacha20poly1305_ietf_decrypt(ct, nom_fragment.encode("ascii"), nonce, cle_fragment(maitre, nom_fragment))
    except Exception as exc:  # fail-closed : aucun contournement
        raise ErreurCarte(f"{nom_fragment} : dechiffrement impossible ({exc})") from exc


# --- Signature ---------------------------------------------------------------

def paire_cles(graine: bytes) -> tuple[Ed25519PrivateKey, bytes]:
    prive = Ed25519PrivateKey.from_private_bytes(graine)
    pub = prive.public_key().public_bytes_raw()
    return prive, pub


def signer(prive: Ed25519PrivateKey, entete: bytes, fragments: dict[str, bytes]) -> bytes:
    donnees = entete + b"".join(fragments[n] for n in FRAGMENTS)
    return prive.sign(donnees)


def verifier_signature(pub: bytes, entete: bytes, fragments: dict[str, bytes], signature: bytes) -> None:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    donnees = entete + b"".join(fragments[n] for n in FRAGMENTS)
    try:
        Ed25519PublicKey.from_public_bytes(pub).verify(signature, donnees)
    except Exception as exc:
        raise ErreurCarte(f"signature de carte invalide (R9) : {exc}") from exc


# --- En-tête normalisé -------------------------------------------------------

def construire_entete(racine: bytes) -> bytes:
    lignes = [
        "[carte] version=0.5.0-terrain.2 generation=5",
        f"  algo_hachage     : {ALGO_HACHAGE}",
        f"  algo_signature   : {ALGO_SIGNATURE}",
        f"  algo_chiffrement : {ALGO_CHIFFREMENT}",
        f"  profils          : {PROFILS}",
        f"  empreinte_racine : sha256:{racine.hex()}",
    ]
    return ("\n".join(lignes) + "\n").encode("ascii")


def verifier_listes_blanches(entete: str) -> None:
    champs = {}
    for ligne in entete.splitlines():
        if ":" in ligne and ligne.startswith("  "):
            cle, val = ligne.strip().split(":", 1)
            champs[cle.strip()] = val.strip()
    for cle, blanche in (
        ("algo_hachage", BLANCHE_HACHAGE),
        ("algo_signature", BLANCHE_SIGNATURE),
        ("algo_chiffrement", BLANCHE_CHIFFREMENT),
    ):
        if champs.get(cle) not in blanche:
            raise ErreurCarte(f"{cle}={champs.get(cle)!r} hors liste blanche D15")


def empreinte_racine(fragments: dict[str, bytes]) -> bytes:
    """SHA-256 de l'ensemble des fragments chiffrés, dans l'ordre canonique."""
    return hashlib.sha256(b"".join(fragments[n] for n in FRAGMENTS)).digest()


# --- Écriture / lecture des artefacts carte ----------------------------------

def ecrire_carte(entete: bytes, fragments: dict[str, bytes], signature: bytes, pub: bytes) -> None:
    os.makedirs(CARTE_DIR, exist_ok=True)
    with open(os.path.join(CARTE_DIR, "header.txt"), "wb") as f:
        f.write(entete)
    for nom in FRAGMENTS:
        with open(os.path.join(CARTE_DIR, f"{nom}.bin"), "wb") as f:
            f.write(fragments[nom])
    with open(os.path.join(CARTE_DIR, "carte.sig"), "wb") as f:
        f.write(signature)
    with open(os.path.join(CARTE_DIR, "cle-publique.ed25519"), "wb") as f:
        f.write(pub)


def lire_carte() -> tuple[bytes, dict[str, bytes], bytes, bytes]:
    with open(os.path.join(CARTE_DIR, "header.txt"), "rb") as f:
        entete = f.read()
    fragments = {}
    for nom in FRAGMENTS:
        with open(os.path.join(CARTE_DIR, f"{nom}.bin"), "rb") as f:
            fragments[nom] = f.read()
    with open(os.path.join(CARTE_DIR, "carte.sig"), "rb") as f:
        signature = f.read()
    with open(os.path.join(CARTE_DIR, "cle-publique.ed25519"), "rb") as f:
        pub = f.read()
    return entete, fragments, signature, pub
