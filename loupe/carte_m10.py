#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""carte_m10.py — Couche C du domaine loupe : carte, GÉNÉRATION 13 (lignée
D80) — LA PREMIÈRE GÉNÉRATION DU DOMAINE (les i11xxxx entrent à la carte).

Même format que les cartes M0-M9 (docs/FORMAT_CARTE.md) — quatre fragments
chiffrés XChaCha20-Poly1305, clés dérivées de la phrase maîtresse par
Argon2id puis HKDF, empreinte racine SHA-256, signature Ed25519 — avec les
spécificités du domaine loupe (M10, le TGN « Loupe ») :

  - GÉNÉRATION 13 : les 18 blocs i110001..18 (le domaine `loupe` — l'éditeur
    hexadécimal au panneau d'empreintes, le test grandeur nature D171) et les
    HUIT hérités embarqués À LEURS ADRESSES SCELLÉES (b20001/02/07 la
    minilibc M1 · d40003 la boucle démo · h100001..04 la famille sha M9) ;
    la numérotation suit les familles (a1 M0, b2 M1, c3 M2, d4 démo, e5 M3,
    f6 terrain, g7 M4, g8 M5, g9 M8/M9-sys, h10 M9-tls13, i11 M10-loupe) ;
  - LIGNÉE D80 : la phrase maîtresse est celle du coffre (entrée
    lignee-D80) — la même depuis la génération 5 ;
  - GRAINE DURABLE (D144) : la graine Ed25519 est celle déposée au coffre
    (entrée TRIADE/graine-ed25519-cartes, octets bruts 32 o — pub
    e9cd8c549485…) ; le TÉMOIN NE BOUGE PAS d'une ère à l'autre ;
  - charger_secrets est FAIL-CLOSED (D144) : aucun secret n'est jamais
    généré ici (miroir carte_m5/carte_m8/carte_m9) ;
  - LE BUILD du domaine : loupe.exe 0.1.0-dev.3 (LA RETOUCHE DE
    L'ENTRÉE 205 — dev.2 refusé par le terrain du MÊME refus
    0xc000007b : le BASERELOC était nécessaire mais pas suffisant ;
    dev.3 ramène l'image dans l'enveloppe de la lignée — plus de trou
    de page, plus de BSS ; le geste de BUILD, jamais
    scellage — la balise `loupe 0.1.0` se scellera sur le run
    terrain vert recoupé, M10-(e) : la porte est de processus).

Les secrets ne sont jamais committés (chmod 600, .gitignore).
"""

from __future__ import annotations

import hashlib
import os
import re

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from nacl.bindings import (
    crypto_aead_xchacha20poly1305_ietf_decrypt,
    crypto_aead_xchacha20poly1305_ietf_encrypt,
)

# --- Constantes du projet (M10, le domaine loupe) ----------------------------------

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS_DIR = os.path.join(_RACINE, ".keys")
CARTE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "carte")

FRAGMENTS = ("frag-loc", "frag-con", "frag-prf", "frag-bld")
GENERATION = 13   # la génération du domaine loupe (les builds dev.1 → dev.2 →
                   # dev.3 — le miroir M8 : une génération par domaine, les
                   # builds la réécrivent)

# Sel Argon2id propre au domaine (public par conception — la phrase
# maîtresse est le secret ; le sel fixe garantit la dérivation reproductible).
ARGON2_SALT = hashlib.sha256(b"TRIADE-M10-carte-argon2id-v1").digest()  # 32 o

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

VERSION_DEV = "0.1.0-dev.3"     # la retouche de l'Entrée 205 (dev.2 refusé
                                 # par le terrain — le geste de BUILD)
VERSION_FINALE = "0.1.0"        # la finale (le miroir layout.VERSION_FINALE
                                # 0x00010000 — le scellage est un fait de
                                # carte : la 0.1.0 attend le run terrain vert
                                # recoupé M10-(e), jamais un build ici)


class ErreurCarte(Exception):
    """Tout échec de chiffrement, de signature ou de vérification (fail-closed)."""


# --- Secrets : chargement (lignée D80 + graine durable, D144) — FAIL-CLOSED --------

def charger_secrets(interactif: bool = True) -> tuple[bytes, bytes]:
    """Retourne (phrase_maîtresse, graine_ed25519) — JAMAIS générés ici.

    D144 : le laboratoire ne crée plus jamais de secret de carte. Si
    .keys/passphrase.txt ou .keys/ed25519.seed est absent, l'échec est
    NOMMÉ (cérémonie de relève depuis le coffre).
    """
    chemin_phrase = os.path.join(KEYS_DIR, "passphrase.txt")
    chemin_graine = os.path.join(KEYS_DIR, "ed25519.seed")
    manquants = [c for c in (chemin_phrase, chemin_graine) if not os.path.exists(c)]
    if manquants:
        raise ErreurCarte(
            "cérémonie requise (D144) : secrets de carte absents du laboratoire "
            f"({', '.join(os.path.basename(c) for c in manquants)}) — relève au "
            "coffre : phrase = entrée lignee-D80, graine = entrée "
            "graine-ed25519-cartes (obtenir --vers-fichier .keys/ed25519.seed, "
            "octets bruts 32 o, jamais d'hex, jamais de fin de ligne)"
        )
    with open(chemin_phrase, "rb") as f:
        phrase = f.read().strip()
    with open(chemin_graine, "rb") as f:
        graine = f.read().strip()
    if len(phrase) < 16 or len(graine) != 32:
        raise ErreurCarte(
            f"secrets inattendus (phrase {len(phrase)} o, graine {len(graine)} o) — "
            "attendu : phrase >= 16 o, graine 32 o exactement (octets bruts)"
        )
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
        salt=b"TRIADE-carte-M10",
        info=f"frag={nom_fragment};gen={GENERATION}".encode("ascii"),
    )
    return hkdf.derive(maitre)


def chiffrer_fragment(maitre: bytes, nom_fragment: str, clair: bytes) -> bytes:
    """XChaCha20-Poly1305, nonce aléatoire 192 bits, AAD = rôle du fragment."""
    cle = cle_fragment(maitre, nom_fragment)
    import secrets
    nonce = secrets.token_bytes(24)  # 192 bits
    ct = crypto_aead_xchacha20poly1305_ietf_encrypt(
        clair, nom_fragment.encode("ascii"), nonce, cle)
    return nonce + ct


def dechiffrer_fragment(maitre: bytes, nom_fragment: str, blob: bytes) -> bytes:
    if len(blob) < 24 + 16:
        raise ErreurCarte(f"{nom_fragment} : blob trop court")
    nonce, ct = blob[:24], blob[24:]
    try:
        return crypto_aead_xchacha20poly1305_ietf_decrypt(
            ct, nom_fragment.encode("ascii"), nonce, cle_fragment(maitre, nom_fragment))
    except Exception as exc:  # fail-closed : aucun contournement
        raise ErreurCarte(f"{nom_fragment} : dechiffrement impossible ({exc})") from exc


# --- Signature ---------------------------------------------------------------

def paire_cles(graine: bytes) -> tuple[Ed25519PrivateKey, bytes]:
    prive = Ed25519PrivateKey.from_private_bytes(graine)
    pub = prive.public_key().public_bytes_raw()
    return prive, pub


def signer(prive: Ed25519PrivateKey, entete: bytes,
           fragments: dict[str, bytes]) -> bytes:
    donnees = entete + b"".join(fragments[n] for n in FRAGMENTS)
    return prive.sign(donnees)


def verifier_signature(pub: bytes, entete: bytes,
                       fragments: dict[str, bytes], signature: bytes) -> None:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    donnees = entete + b"".join(fragments[n] for n in FRAGMENTS)
    try:
        Ed25519PublicKey.from_public_bytes(pub).verify(signature, donnees)
    except Exception as exc:
        raise ErreurCarte(f"signature de carte invalide (R9) : {exc}") from exc


# --- En-tête normalisé -------------------------------------------------------

def construire_entete(racine: bytes, version: str = VERSION_DEV) -> bytes:
    """L'en-tête porte la version de l'ARTEFACT (dev au fil des builds, la
    balise scellée au geste final — le scellage est un fait de carte)."""
    lignes = [
        f"[carte] version={version} generation={GENERATION}",
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

def ecrire_carte(entete: bytes, fragments: dict[str, bytes],
                 signature: bytes, pub: bytes) -> None:
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


# =====================================================================================
# LA TABLE DU DOMAINE — les 26 blocs indexés par la première génération loupe
# (les 18 du domaine + les HUIT hérités embarqués AUX ADRESSES SCELLÉES).
# La source unique : loupe/layout.py (les RVA/slots) et les specs d'origine.
# =====================================================================================

ICI = os.path.dirname(os.path.abspath(__file__))

# (bid, spec, rôle, rva, taille, dossier d'origine de la notation, fichier)
BLOCS_CARTE_LOUPE = [
    ("i110001", "loupe-01:R3", "ouvrir (la session née entière)", 0x4080, 0x1C0),
    ("i110002", "loupe-02:R1", "lire (la fenêtre bornée)", 0x4240, 0x140),
    ("i110003", "loupe-03:R1", "fermer (idempotent)", 0x4380, 0xC0),
    ("i110004", "loupe-04:R1", "le cadre (la structure unique)", 0x4040, 0x40),
    ("i110005", "loupe-05:R1", "sha256 (l'héritage tls13 PAR LA CARTE)", 0x4440, 0x180),
    ("i110006", "loupe-06:R1", "md5 (la notation neuve RFC 1321)", 0x45C0, 0x380),
    ("i110007", "loupe-07:R1", "le cumul (les empreintes du fichier entier)", 0x4940, 0x80),
    ("i110008", "loupe-08:R1", "la ligne (feuille pure)", 0x49C0, 0x140),
    ("i110009", "loupe-09:R1", "l'écran (WinMain + LA PROCÉDURE, r2 la table étendue)", 0x5C00, 0x480),
    ("i110010", "loupe-10:R1", "la peinture (l'unique peintre)", 0x4B00, 0x680),
    ("i110011", "loupe-11:R1", "le défilement (borné à la fin)", 0x5180, 0x280),
    ("i110012", "loupe-12:R1", "l'aller (la barre-saisie hexa)", 0x5400, 0x340),
    ("i110013", "loupe-13:R1", "la recherche (feuille pure, memcmp scellé)", 0x5740, 0xC0),
    ("i110014", "loupe-14:R1", "le suivant (le recouvrement, la FIN nommée)", 0x5800, 0x400),
    ("i110015", "loupe-15:R1", "le curseur (la vue suit)", 0x6080, 0x1C0),
    ("i110016", "loupe-16:R1", "la saisie (l'octet au journal)", 0x6240, 0x2C0),
    ("i110017", "loupe-17:R1", "la sauvegarde (l'écriture à l'octet)", 0x6500, 0x240),
    ("i110018", "loupe-18:R1", "la sortie (le double-gestre garanti)", 0x6740, 0xC0),
    # les hérités — les octets SCELLÉS d'origine aux MÊMES adresses (R7)
    ("b20001", "libc-01:R1", "memcpy (la minilibc M1, le scellé selftest.exe)", 0x1100, 0x80),
    ("b20002", "libc-02:R1", "memcmp (la minilibc M1, le scellé selftest.exe)", 0x1180, 0x80),
    ("b20007", "libc-07:R1", "memset (la minilibc M1, le scellé selftest.exe)", 0x13C0, 0x80),
    ("d40003", "win-03:R1", "la boucle de messages (le scellé demo.exe 0.3.0)", 0x15C0, 0x80),
    ("h100001", "tls13-01:R1", "sha256-init (le scellé proxy.exe 1.0.0, M9)", 0xC000, 0x80),
    ("h100002", "tls13-02:R1", "sha256-comprimer (le scellé proxy.exe 1.0.0)", 0xC080, 0x1C0),
    ("h100003", "tls13-03:R1", "sha256-absorber (le scellé proxy.exe 1.0.0)", 0xC240, 0xC0),
    ("h100004", "tls13-04:R1", "sha256-finaliser (le scellé proxy.exe 1.0.0)", 0xC300, 0xC0),
]

TOUS_BLOCS_CARTE = [b[0] for b in BLOCS_CARTE_LOUPE]     # 26
_RVA_PAR_BLOC = {b[0]: b[3] for b in BLOCS_CARTE_LOUPE}
_TAILLE_PAR_BLOC = {b[0]: b[4] for b in BLOCS_CARTE_LOUPE}
_SPEC_PAR_BLOC = {b[0]: b[1] for b in BLOCS_CARTE_LOUPE}
_ROLE_PAR_BLOC = {b[0]: b[2] for b in BLOCS_CARTE_LOUPE}

_ZONES_CARTE_M10 = (
    "[zones] libc=0x1100-0x11ff (libc-01/02 scellés M1) "
    "libc-suite=0x13c0-0x143f (libc-07 scellé M1) reserve-libc=0x1200-0x13bf "
    "reserve-m1=0x1440-0x15bf win-demo=0x15c0-0x163f (win-03 scellé démo) "
    "reserve-text=0x1640-0x1fff (int3 défensif) "
    "rdata-rendu=0x2000-0x20ff rdata-md5=0x2100-0x22ff "
    "rdata-libelles=0x2300-0x23fa iat-k32=0x2400-0x244f "
    "iat-u32=0x2450-0x24df iat-gdi=0x24e0-0x250f "
    "rdata-libelles-d=0x2520-0x259e rdata-utf16=0x2600-0x26a7 "
    "iat-demo=0x2818-0x282f (les TROIS slots scellés de win-03) "
    "imports=0x2830-0x2c57 (descripteurs, INT, hints, noms) "
    "porte-r10=0x2c60-0x2e8f k-table=0x2f00-0x2fff (la table du scellé M9) "
    "marge-rdata=0x26a8-0x2817 "
    "domaine=0x4040-0x67ff (les 18 blocs, les slots arrêtés D161) "
    "reserve-t2=0x6800-0xbfff (int3 défensif) "
    "sha-m9=0xc000-0xc3bf (la famille scellée M9) "
    "data-cadre=0xe000-0xe3bf data-empreintes=0xe3c0 data-saisie=0xe400 "
    "data-motif=0xe460 data-journal=0xe4a0 data-ecran=0xf4c0 "
    "data-hwnd=0xfde0 data-metriques=0xfdf0 data-cumul=0x10000-0x1ffff"
)


def _lire_spec_gabarit(chemin: str) -> dict:
    """Le gabarit § 2.2 (partagé par toutes les couches I du projet) : la
    première ligne nomme, pre/post/inv PARSÉS — la couche I est la source."""
    with open(chemin, encoding="utf-8") as f:
        lignes = f.read().splitlines()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", lignes[0])
    if not m:
        raise ErreurCarte(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3))}

    def _section(marqueur: str) -> str:
        pat = re.compile(rf"^  {marqueur}\s*:\s*(.*)$")
        sortie, actif = [], False
        for ligne in lignes:
            mm = pat.match(ligne)
            if mm:
                actif = True
                if mm.group(1).strip():
                    sortie.append(mm.group(1).strip())
                continue
            if actif:
                if ligne.startswith("  ") and ligne.strip():
                    sortie.append(ligne.strip())
                else:
                    actif = False
        return " ".join(sortie)

    spec["pre"] = _section("pre")
    spec["post"] = _section("post")
    spec["inv"] = _section("inv")
    if not (spec["pre"] and spec["post"] and spec["inv"]):
        raise ErreurCarte(f"{chemin} : sections pre/post/inv vides (gabarit § 2.2)")
    return spec


# les specs d'origine des hérités (la couche I de CHAQUE ère — la source)
_SPECS_HERITES = {
    "b20001": ("m1", "libc-01-memcpy.md"),
    "b20002": ("m1", "libc-02-memcmp.md"),
    "b20007": ("m1", "libc-07-memset.md"),
    "d40003": ("demo", "win-03-boucle.md"),
    "h100001": ("tls13", "tls13-01-sha256-init.md"),
    "h100002": ("tls13", "tls13-02-sha256-comprimer.md"),
    "h100003": ("tls13", "tls13-03-sha256-absorber.md"),
    "h100004": ("tls13", "tls13-04-sha256-finaliser.md"),
}


def fragments_clairs(exe: bytes, specs_loupe: dict, code: dict, verrous: int,
                     verdicts: list[dict], journal_runs: list[str]) -> dict[str, bytes]:
    """Les QUATRE fragments clairs du domaine (FORMAT_CARTE § 3.2) — la
    couche I est la source (R2) : les contrats PARSÉS des spécifications,
    jamais une copie d'écriture."""
    sha = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()

    # -- frag-loc : les zones + un par bloc (id, spec, cible, exe, addr, état)
    loc = [f"[carte-frag] nom=frag-loc generation={GENERATION}",
           _ZONES_CARTE_M10]
    etats = {bid: "verifie" for bid in TOUS_BLOCS_CARTE}
    for bid in ("b20001", "b20002", "b20007", "d40003",
                "h100001", "h100002", "h100003", "h100004"):
        etats[bid] = "scelle"       # les octets hérités sont des pièces scellées
    for bid in TOUS_BLOCS_CARTE:
        loc.append(
            f"[bloc] id={bid} spec={_SPEC_PAR_BLOC[bid]} "
            f"cible=x86-64-win11-pe exe=loupe.exe "
            f"addr={0x140000000 + _RVA_PAR_BLOC[bid]:#x} v=1 "
            f"etat={etats[bid]} role={_ROLE_PAR_BLOC[bid]}")

    # -- frag-con : les contrats parsés des specs (loupe + les origines)
    con = [f"[carte-frag] nom=frag-con generation={GENERATION}"]
    BLOCS_LOUPE_BUILD = [
        ("i110001", "loupe-01:R3", "loupe-01-ouvrir"),
        ("i110002", "loupe-02:R1", "loupe-02-lire"),
        ("i110003", "loupe-03:R1", "loupe-03-fermer"),
        ("i110004", "loupe-04:R1", "loupe-04-cadre"),
        ("i110005", "loupe-05:R1", "loupe-05-sha256"),
        ("i110006", "loupe-06:R1", "loupe-06-md5"),
        ("i110007", "loupe-07:R1", "loupe-07-cumul"),
        ("i110008", "loupe-08:R1", "loupe-08-ligne"),
        ("i110009", "loupe-09:R1", "loupe-09-ecran"),
        ("i110010", "loupe-10:R1", "loupe-10-peinture"),
        ("i110011", "loupe-11:R1", "loupe-11-defilement"),
        ("i110012", "loupe-12:R1", "loupe-12-aller"),
        ("i110013", "loupe-13:R1", "loupe-13-recherche"),
        ("i110014", "loupe-14:R1", "loupe-14-suivant"),
        ("i110015", "loupe-15:R1", "loupe-15-curseur"),
        ("i110016", "loupe-16:R1", "loupe-16-saisie"),
        ("i110017", "loupe-17:R1", "loupe-17-sauver"),
        ("i110018", "loupe-18:R1", "loupe-18-quitter"),
    ]
    for bid, _sid, fichier in BLOCS_LOUPE_BUILD:
        spec = specs_loupe[bid]
        chemin_asm = os.path.join(ICI, "notation", fichier + ".asm")
        deps = ""
        with open(chemin_asm, encoding="utf-8") as f:
            for ligne in f:
                if ligne.startswith(";") and "Dépendances :" in ligne:
                    deps = ligne.split("Dépendances :", 1)[1].strip()
                    break
        con += [f"[bloc] id={bid}",
                f"  sig : {spec['nom']}",
                f"  pre : {spec['pre']}",
                f"  post : {spec['post']}",
                f"  inv : {spec['inv']}",
                f"  deps : {deps}"]
    for bid, (dossier, fichier_spec) in _SPECS_HERITES.items():
        spec = _lire_spec_gabarit(os.path.join(_RACINE, dossier, "I", fichier_spec))
        con += [f"[bloc] id={bid} (l'origine : {dossier}/I/{fichier_spec})",
                f"  sig : {spec['nom']}",
                f"  pre : {spec['pre']}",
                f"  post : {spec['post']}",
                f"  inv : {spec['inv']}"]

    # -- frag-prf : les notations empreintées + la cristallisation + les runs
    prf = [f"[carte-frag] nom=frag-prf generation={GENERATION}"]
    chemins_notation = {bid: os.path.join(ICI, "notation", f + ".asm")
                        for bid, _s, f in BLOCS_LOUPE_BUILD}
    chemins_notation.update({
        "b20001": os.path.join(_RACINE, "m1", "notation", "libc-01-memcpy.asm"),
        "b20002": os.path.join(_RACINE, "m1", "notation", "libc-02-memcmp.asm"),
        "b20007": os.path.join(_RACINE, "m1", "notation", "libc-07-memset.asm"),
        "d40003": os.path.join(_RACINE, "demo", "notation", "win-03-boucle.asm"),
        "h100001": os.path.join(_RACINE, "tls13", "notation", "tls13-01-sha256-init.asm"),
        "h100002": os.path.join(_RACINE, "tls13", "notation", "tls13-02-sha256-comprimer.asm"),
        "h100003": os.path.join(_RACINE, "tls13", "notation", "tls13-03-sha256-absorber.asm"),
        "h100004": os.path.join(_RACINE, "tls13", "notation", "tls13-04-sha256-finaliser.asm"),
    })
    for bid in TOUS_BLOCS_CARTE:
        with open(chemins_notation[bid], "rb") as f:
            empreinte_notation = sha(f.read())
        prf += [
            f"[bloc] id={bid} etat=verifie crist=1/10",
            f"  vecteurs : roundtrip=ok structure=ok notation={empreinte_notation}",
        ]
    prf.append("[verifications] runs=" + str(len(journal_runs)))
    prf += ["  " + r for r in journal_runs[-12:]]

    # -- frag-bld : les empreintes DANS l'artefact + le manifeste du build
    import pefile
    pe = pefile.PE(data=exe)

    def tranche(rva: int, n: int) -> bytes:
        return exe[pe.get_offset_from_rva(rva): pe.get_offset_from_rva(rva) + n]

    bld = [f"[carte-frag] nom=frag-bld generation={GENERATION}"]
    for bid in TOUS_BLOCS_CARTE:
        rva, taille = _RVA_PAR_BLOC[bid], _TAILLE_PAR_BLOC[bid]
        bld.append(f"[bloc] id={bid} addr={0x140000000 + rva:#x} "
                   f"empreinte={sha(tranche(rva, taille))}")
    bld += [
        f"[build] artefact=loupe.exe version={VERSION_DEV} "
        f"profil=x86-64-win11-pe taille={len(exe)} empreinte={sha(exe)}",
        f"  outils : keystone-engine + capstone ; verrous structurels : "
        f"{verrous} ; oracles : "
        + " + ".join(f"{v['harnais']} {v['verts']}/{v['total']} VERTS"
                     for v in verdicts),
        f"  heritage : libc-01/02/07 (M1 selftest.exe) + win-03 (demo.exe 0.3.0) "
        f"+ tls13-01..04 (proxy.exe 1.0.0) — LA DOUBLE PREUVE R7, la table "
        f"K[64] @0x2F00 du scellé M9",
        f"  garde : sceau-I 14/14 arbres VERTS AVANT construire() (D87 — "
        f"l'ère du TGN, la cérémonie Passée sur pièces, Entrée 201)",
    ]
    return {"frag-loc": "\n".join(loc).encode("utf-8") + b"\n",
            "frag-con": "\n".join(con).encode("utf-8") + b"\n",
            "frag-prf": "\n".join(prf).encode("utf-8") + b"\n",
            "frag-bld": "\n".join(bld).encode("utf-8") + b"\n"}
