#!/usr/bin/env python3
"""carte_m5.py — Couche C du jalon M5 : carte projet, génération 7 (lignée D80).

Même format que les cartes M0-M4 (docs/FORMAT_CARTE.md) — quatre fragments
chiffrés XChaCha20-Poly1305, clés dérivées de la phrase maîtresse par
Argon2id puis HKDF, empreinte racine SHA-256, signature Ed25519 — avec les
spécificités M5 :

  - GÉNÉRATION 7 : les blocs g8xxxx (http-08:R3, http-10:R3, http-12:R3 —
    les révisions du relèvement https, D136) ; la numérotation suit les
    familles (a1 M0, b2 M1, c3 M2, d4 démo, e5 M3, f6 terrain, g7 M4,
    g8 M5) ; la génération 7 devient la carte COURANTE du projet et indexe
    l'ensemble des blocs des artefacts hello.exe, selftest.exe, echo.exe,
    proxy.exe 0.4.0 (génération 5, ancêtre cité), proxy.exe 0.5.1
    (génération 6, ancêtre cité — la lignée re-scellée D144) et
    proxy.exe 0.6.0-dev.1 ;
  - LIGNÉE D80 : la phrase maîtresse est celle du coffre (entrée
    lignee-D80, conteneur CF1 relève D75) — la même qui déchiffre m3
    génération 5, la carte m4 D104 ET la m4 0.5.1 re-scellée (D144) ;
  - GRAINE DURABLE (D144) : la graine Ed25519 est celle déposée au coffre
    (entrée TRIADE/graine-ed25519-cartes, octets bruts 32 o — pub
    e9cd8c549485…) ; c'est la graine qui a signé la carte m4 0.5.1
    re-scellée le 04/11 ; DÉSORMAIS toute génération de secret de carte
    est déposée au coffre DANS LE MÊME GESTE — le labo n'en crée plus
    jamais (la cause racine de l'orpheline du jalon v7, D140/D144) ;
  - charger_secrets est FAIL-CLOSED : si .keys/ est absent (labo recyclé,
    clone de bundle), AUCUN secret n'est généré — la relève se fait depuis
    le coffre (scripts/rapatrier_coffre_cf1.py ; phrase : entrée lignee-D80,
    graine : entrée graine-ed25519-cartes via obtenir --vers-fichier
    .keys/ed25519.seed, octets bruts, jamais d'hex, jamais de fin de ligne).

Les secrets ne sont jamais committés (chmod 600, .gitignore).
"""

from __future__ import annotations

import hashlib
import os

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from nacl.bindings import (
    crypto_aead_xchacha20poly1305_ietf_decrypt,
    crypto_aead_xchacha20poly1305_ietf_encrypt,
)

# --- Constantes du projet (M5) ----------------------------------------------

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS_DIR = os.path.join(_RACINE, ".keys")
CARTE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "carte")

FRAGMENTS = ("frag-loc", "frag-con", "frag-prf", "frag-bld")
GENERATION = 7

# Sel Argon2id propre à la génération 7 (public par conception — la phrase
# maîtresse est le secret ; le sel fixe garantit la dérivation reproductible).
ARGON2_SALT = hashlib.sha256(b"TRIADE-M5-carte-argon2id-v1").digest()  # 32 o

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

VERSION_DEV1 = "0.6.0-dev.1"


class ErreurCarte(Exception):
    """Tout échec de chiffrement, de signature ou de vérification (fail-closed)."""


# --- Secrets : chargement (lignée D80 + graine durable, D144) — FAIL-CLOSED ----

def charger_secrets(interactif: bool = True) -> tuple[bytes, bytes]:
    """Retourne (phrase_maîtresse, graine_ed25519) — JAMAIS générés ici.

    D144 : le laboratoire ne crée plus jamais de secret de carte. Si
    .keys/passphrase.txt ou .keys/ed25519.seed est absent, l'échec est
    NOMMÉ (cérémonie de relève depuis le coffre) — aucune délégation à
    carte_m0.charger_secrets, aucune génération éphémère (la cause racine
    de la carte orpheline du jalon v7 est ÉTEINTE à la source).
    """
    chemin_phrase = os.path.join(KEYS_DIR, "passphrase.txt")
    chemin_graine = os.path.join(KEYS_DIR, "ed25519.seed")
    manquants = [c for c in (chemin_phrase, chemin_graine) if not os.path.exists(c)]
    if manquants:
        raise ErreurCarte(
            "cérémonie requise (D144) : secrets de carte absents du laboratoire "
            f"({', '.join(os.path.basename(m) for m in manquants)}) — relève au "
            "coffre : phrase = entrée lignee-D80, graine = entrée "
            "graine-ed25519-cartes (obtenir --vers-fichier .keys/ed25519.seed, "
            "octets bruts 32 o, jamais d'hex, jamais de fin de ligne)")
    with open(chemin_phrase, "rb") as f:
        phrase = f.read().strip()
    with open(chemin_graine, "rb") as f:
        graine = f.read().strip()
    if len(phrase) < 16 or len(graine) != 32:
        raise ErreurCarte(
            f"secrets inattendus (phrase {len(phrase)} o, graine {len(graine)} o) — "
            "attendu : phrase >= 16 o, graine 32 o exactement (octets bruts)")
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
        salt=b"TRIADE-carte-M5",
        info=f"frag={nom_fragment};gen={GENERATION}".encode("ascii"),
    )
    return hkdf.derive(maitre)


def chiffrer_fragment(maitre: bytes, nom_fragment: str, clair: bytes) -> bytes:
    """XChaCha20-Poly1305, nonce aléatoire 192 bits, AAD = rôle du fragment."""
    cle = cle_fragment(maitre, nom_fragment)
    import secrets
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
        f"[carte] version={VERSION_DEV1} generation={GENERATION}",
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
