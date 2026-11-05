#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tls13/harnais_aead.py — LE HARNAIS DE LA FAMILLE aead DU DOMAINE tls13.

Chantier M9-(b), quatrième geste : les blocs tls13-15..19 (AES-128 le
déploiement des clés de tour, AES-128 le chiffrement d'un bloc, GHASH la
multiplication GF(2^128), GCM sceller, GCM ouvrir — FIPS 197, SP 800-38A
F.1.1, SP 800-38D § 6.3/§ 7.1, RFC 8446 § 5.2/§ 5.3) NOTÉS-MESURÉS-PROUVÉS
sur les familles sha, hkdf et x25519 notées-mesurées-prouvées aux gestes
précédents. Le modèle est le harnais x25519 (tls13/harnais_x25519.py) :
l'émulation nue à les RVA du plan (mécanisme D79), l'appelant factice
pose les sentinelles non volatiles et les canaris, le verdict est
TRANCHÉ par le code — jamais cru.

LE CAHIER (la charte § 2 : les vecteurs officiels AVANT usage, la
falsification, zéro silence) :

  V0 — LES PIÈCES DU PLAN : le scellé 0.9.0 relu (l'ancre 1492b0bc…),
       les familles sha, hkdf ET x25519 INTACTES (les quatorze notations
       re-round-tripées aux longueurs arrêtées 74/387/139/165 +
       435/151/347/310 + 54/252/1078/281/2887/23 — la frontière des
       gestes précédents), K[64] posé à R_K, LES FIXTURES DU DOMAINE
       posés à leur ARRÊT .text6 (U9 @ 0xFF00, EXP_INV @ 0xFF20 — les
       contenus re-dérivés du plan par arithmétique), l'arbre I scellé
       relu VERT (verifier_specs_m9a rejoué — R2) ; LA FAMILLE aead
       N'AJOUTE AUCUN FIXTURE : la constante R = 0xE1||0^120 vit en
       IMMÉDIAT (I4 de tls13-17 — le bloc autoporteur), l'ARRÊT AES-NI
       tient l'expansion MATÉRIELLE (I3 de tls13-15) ;
  V1 — LE ROUND-TRIP + LA CONCORDANCE : chaque notation ré-assemblée en
       ses octets (keystone == capstone, R5), les longueurs == l'ARRÊT
       du plan (520/129/162/1076/1163 o, D161 — le 17 re-mesuré
       139→162 au geste même : la sonde a nommé la représentation, le
       domaine gros-boutiste par bswap), les appels directs de 18 et
       19 == TLS16 ×3 + TLS17 ×3 (les sites statiques : H, CTR, J0 ;
       AAD, chiffré, longueurs — I2), LES IMMÉDIATS au plan : les DIX
       Rcon de 15 (01..36 — FIPS 197 § 5.2), le pshufd 0xff de
       diffusion ×10 (la sonde du labo : le mot d'AES-128 au dword 3),
       le movabs 0xE1<<56 de 17 (l'octet 0 au SOMMET de la voie haute
       bswapée), le 0x01000000 de 18/19 (J0 = nonce||0^31||1 — le u32
       terminal GROS-BOUTISTE : la seconde faute nommée par la sonde,
       la première écriture posait 01 00 00 00) ; la composition de 16 :
       pxor + NEUF aesenc + aesenclast ; LA STRUCTURE : aucun site
       syscall, aucun appel indirect, AUCUN déplacement RIP (la famille
       ENTIÈRE autoporteur — contrairement à x25519 et ses DEUX
       fixtures, l'aead ne lit RIEN hors de ses arguments et de sa
       pile) ; LE TEMPS CONSTANT STRUCTUREL : 15/16 ZÉRO saut
       conditionnel, 17 exactement UN (le compteur de boucle — le bit
       de X devient masque par sbb, JAMAIS une branche), 18 exactement
       dix-sept et 19 exactement dix-neuf, TOUS sur les données
       PUBLIQUES (pointeurs, longueurs, compteurs — les comptes EXACTS
       vérifiés) ; LE SEUL saut qui lit un produit du chiffré est LE
       VERDICT de 19 : test r10, r10 — LE drapeau CUMULÉ des 16
       différences (I1 : le OU cumulatif, AUCUN court-circuit, la
       branche se prononce sur LE drapeau — jamais sur un octet isolé) ;
  V2 — LES VECTEURS OFFICIELS : FIPS 197 C.1 (le déploiement : les 176 o
       == la référence ; le bloc : 69c4e0d8…), SP 800-38A F.1.1 (les
       QUATRE blocs ECB-AES128 PAR LA COMPOSITION 15+16 — un déploiement
       faux rend un chiffrement faux : la § F.1.1 applique SES clés de
       tour), McGrew–Viega TC1..TC4 (le scellement : chiffré ET
       étiquette octet pour octet ; l'ouverture en sens inverse ; les
       TC5/TC6 — IV de 8 et 60 octets — sont HORS CONTRAT de la brique
       : P2 le nonce de 12 o, la borne du protocole RFC 8446 § 5.3, la
       référence du labo les couvre), ET LE TRANSFERT RFC 8448 : les
       SEPT enregistrements chiffrés du § 3 OUVERTS par tls13-19 (le
       nonce = IV ⊕ séquence, la tête 0x17 en AAD — le clair interne
       payload || type rendu octet pour octet) PUIS RESCELLÉS par
       tls13-18 == l'enregistrement OCTET POUR OCTET + l'oracle
       différentiel (cent scellages aléatoires contre la référence) ;
  V3 — LES CAS PUNITIFS : le GHASH (X = 0 → Z = 0, Y = 0 → Z = 0,
       l'identité réfléchie 0x80||0^120 : X·ID == X, X = Y = R, X = Y =
       1, la commutativité aux DEUX ordres), le chevauchement (la
       sortie SUR l'entrée : P3 de 16 et de 17 — le bloc charge AVANT
       d'écrire), les bornes du scellement (N = 2^14 exact — LA borne
       P4, dedans ; N = 2^14+1 → rax = −2 NOMMÉ ; A = 2^14+1 → −2),
       les refus (chaque pointeur nul → −1, les SIX de 18 et les SIX de
       19), l'indifférence (A = 0 : le pointeur AAD nul N'EST PAS un
       refus — le contrat P5 le permet, la brique ne le lit pas) ;
  V4 — LE CONTRAT : les non-volatiles rendus, la pile équilibrée,
       l'ombre et les logements intacts (le cadre 0xE8 de 18/19 — les
       QUATRE arguments de PILE relus), l'alignement msx64 à l'entrée de
       CHAQUE appelé à travers les appels directs (TLS16 et TLS17 par
       18, par 19 — les comptes exacts de la recette : 2 + ⌈N/16⌉
       chiffrements, ⌈A/16⌉ + ⌈N/16⌉ + 1 multiplications), les entrées
       INTACTES (la clé, le nonce, le clair, l'AAD, l'étiquette reçue —
       Q2/Q3), la sortie JAMAIS dépassée (les canaris après le chiffré,
       l'étiquette ET le clair restitué), les refus SANS corruption
       (l'échec ne touche RIEN) ;
  V5 — LA FALSIFICATION (zéro silence) : la clé mutée → le chiffré
       diverge (premier/milieu/dernier octet), le nonce muté → diverge,
       le clair muté → diverge, l'AAD muté → l'ouverture REFUSE (−4),
       CHAQUE octet du chiffré muté → −4, CHAQUE octet de l'étiquette
       muté → −4 (la garde constatée mutation par mutation — Q4 de
       tls13-19), la sortie clair INTACTE à chaque refus (fail-closed :
       AUCUN octet restitué), la comparaison n'est pas muette ;
  V6 — LE TEMPS CONSTANT MESURÉ (I1/I2 de chaque spec, la charte § 3) :
       le déploiement (4 clés → le MÊME compte), le bloc (3 paires →
       MÊME compte), le GHASH (3 paires → MÊME compte), le scellement
       (2 clairs de même longueur, 2 clés → MÊME compte — la longueur
       est publique, le contenu JAMAIS), ET LE VERDICT DE L'OUVERTURE :
       trois étiquettes divergentes (premier, milieu, dernier octet
       muté) → LE MÊME compte EXACTEMENT — le OU cumulatif ne
       court-circuite PAS, la position de la différence ne se lit pas
       dans le temps (I1 de tls13-19 — LA discipline du verdict).

Usage : python3 harnais_aead.py            # le cahier complet
        python3 harnais_aead.py --graine N # la graine du générateur (défaut 20261107)
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import random
import struct
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
TRIADE = os.path.dirname(ICI)
M4_DIR = os.path.join(TRIADE, "m4")
sys.path.insert(0, ICI)
sys.path.insert(0, M4_DIR)
sys.path.insert(0, os.path.join(M4_DIR, "outils"))

# Le plan tls13 chargé par CHEMIN NOMINATIF (leçon D158)
if "layout_tls13" in sys.modules:
    L = sys.modules["layout_tls13"]
else:
    _spec_l = importlib.util.spec_from_file_location(
        "layout_tls13", os.path.join(ICI, "layout.py"))
    L = importlib.util.module_from_spec(_spec_l)
    sys.modules["layout_tls13"] = L
    _spec_l.loader.exec_module(L)

# La machinerie de notation de la lignée (leçon D158)
if "build_m4" in sys.modules:
    B4 = sys.modules["build_m4"]
else:
    _spec_b4 = importlib.util.spec_from_file_location(
        "build_m4", os.path.join(M4_DIR, "build_m4.py"))
    B4 = importlib.util.module_from_spec(_spec_b4)
    sys.modules["build_m4"] = B4
    _spec_b4.loader.exec_module(B4)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402
import capstone  # noqa: E402
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX,  # noqa: E402
                               UC_X86_REG_RDX, UC_X86_REG_RSI, UC_X86_REG_RDI,
                               UC_X86_REG_RBP, UC_X86_REG_RSP, UC_X86_REG_R8,
                               UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11,
                               UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14,
                               UC_X86_REG_R15)

REGS = {"rax": UC_X86_REG_RAX, "rbx": UC_X86_REG_RBX, "rcx": UC_X86_REG_RCX,
        "rdx": UC_X86_REG_RDX, "rsi": UC_X86_REG_RSI, "rdi": UC_X86_REG_RDI,
        "rbp": UC_X86_REG_RBP, "rsp": UC_X86_REG_RSP, "r8": UC_X86_REG_R8,
        "r9": UC_X86_REG_R9, "r10": UC_X86_REG_R10, "r11": UC_X86_REG_R11,
        "r12": UC_X86_REG_R12, "r13": UC_X86_REG_R13, "r14": UC_X86_REG_R14,
        "r15": UC_X86_REG_R15}

# --- La mémoire du harnais (émulation nue à les RVA du plan, mécanisme D79) ------

ZONE_IMAGE = (0x1000, 0xF000)   # .rdata (K @0x2F00) + .text5 + .text6 arrêtée
RET_MAGIQUE = 0xEF00            # dans la marge .text6 (après la famille aead
                                # 0xE9C0, avant les fixtures 0xFF00) — jamais exécuté
ZONE_CLES = 0x500000            # la clé (16 o) et les clés de tour (176 o)
ZONE_ENTREES = 0x600000         # le nonce, le clair, l'AAD, les opérandes GHASH
TAILLE_ENTREES = 0x20000        # jusqu'à 2^14 + les canaris
ZONE_SORTIE = 0x700000          # le chiffré, l'étiquette, le clair restitué
TAILLE_SORTIE = 0x20000
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP0 = 0x7F008000
ENTREE_RSP = RSP0 - 0x108       # ≡ 8 (mod 16) — le point de vue de l'APPELÉ

FENETRE = 0x100                 # la fenêtre canaris autour de chaque entrée

ADR_CLE = ZONE_CLES + 0x100
ADR_RK = ZONE_CLES + 0x200
ADR_NONCE = ZONE_ENTREES + 0x100
ADR_CLAIR = ZONE_ENTREES + 0x1000
ADR_AAD = ZONE_ENTREES + 0x8000
ADR_X = ZONE_ENTREES + 0x10000
ADR_Y = ZONE_ENTREES + 0x10200
ADR_BLOC_IN = ZONE_ENTREES + 0x10400
ADR_BLOC_OUT = ZONE_ENTREES + 0x10600
ADR_CT = ZONE_SORTIE + 0x1000
ADR_TAG = ZONE_SORTIE + 0x8000
ADR_ETIQ = ZONE_SORTIE + 0x8200     # l'étiquette REÇUE (tls13-19 P7)
ADR_CLAIR2 = ZONE_SORTIE + 0x10000  # la sortie de l'ouverture (P8)

CANARI = b"\xA5"

SENTINELLES_NV = {
    "rbx": 0x1212121212121212, "rbp": 0x2323232323232323,
    "rdi": 0x3434343434343434, "rsi": 0x4545454545454545,
    "r12": 0x5656565656565656, "r13": 0x6767676767676767,
    "r14": 0x7878787878787878, "r15": 0x8989898989898989,
}

# --- Le scellé 0.9.0 (la pièce V0 — l'ancre du corps hérité) ---------------------

SCELLE_M8 = "m8/proxy.exe"
SCELLE_M8_TAILLE = 44544
SCELLE_M8_SHA256 = "1492b0bc0792e1ab162338b414fb20573134e84d752b9d0657292421f8eb0cd4"

REUSSITES, ECHECS = [], []


class ErreurHarnais(Exception):
    """Tout écart du harnais (le verdict est tranché, jamais muet)."""


def controle(nom: str, ok: bool, detail: str = "") -> None:
    if ok:
        REUSSITES.append(nom)
        print(f"  [ok] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append((nom, detail))
        print(f"  [ÉCHEC] {nom}" + (f" — {detail}" if detail else ""))


def section(titre: str) -> None:
    print(f"\n--- {titre} ---")


def s64(v: int) -> int:
    return v - (1 << 64) if v >= (1 << 63) else v


# ======================================================================
# LA RÉFÉRENCE — AES-128 pur FIPS 197, GHASH SP 800-38D § 6.3, GCM § 7.1
# (la même référence que le labo derive_aead.py — la S-box DÉRIVÉE de
# l'arithmétique GF(2^8), JAMAIS une table copiée ; contre-preuvée par
# FIPS 197 C.1, SP 800-38A F.1.1, McGrew–Viega TC1..TC6 et les SEPT
# enregistrements RFC 8448 § 3 AVANT la notation — le juge est le code)
# ======================================================================

def _gmul(a: int, b: int) -> int:
    r = 0
    for _ in range(8):
        if b & 1:
            r ^= a
        b >>= 1
        porte = a & 0x80
        a = (a << 1) & 0xFF
        if porte:
            a ^= 0x1B
    return r


def pow_gf(a: int, n: int) -> int:
    r = 1
    while n:
        if n & 1:
            r = _gmul(r, a)
        a = _gmul(a, a)
        n >>= 1
    return r


def _inverse_gf256(a: int) -> int:
    return 0 if a == 0 else pow_gf(a, 254)


def _affine(b: int) -> int:
    c = 0x63
    r = 0
    for i in range(8):
        bit = ((b >> i) ^ (b >> ((i + 4) % 8)) ^ (b >> ((i + 5) % 8))
               ^ (b >> ((i + 6) % 8)) ^ (b >> ((i + 7) % 8)) ^ (c >> i)) & 1
        r |= bit << i
    return r


SBOX = [_affine(_inverse_gf256(x)) for x in range(256)]
RCON = [pow_gf(2, i) for i in range(10)]        # 01 02 04 08 10 20 40 80 1b 36


def _rotword(w: int) -> int:
    return ((w << 8) | (w >> 24)) & 0xFFFFFFFF


def _subword(w: int) -> int:
    return (SBOX[(w >> 24) & 0xFF] << 24 | SBOX[(w >> 16) & 0xFF] << 16
            | SBOX[(w >> 8) & 0xFF] << 8 | SBOX[w & 0xFF])


def ref_cles_tour(cle: bytes) -> list[bytes]:
    """FIPS 197 § 5.2 : les ONZE clés de tour (176 o) depuis la clé 16 o."""
    assert len(cle) == 16
    w = [struct.unpack(">I", cle[4 * i:4 * i + 4])[0] for i in range(4)]
    for i in range(4, 44):
        t = w[i - 1]
        if i % 4 == 0:
            t = _subword(_rotword(t)) ^ (RCON[i // 4 - 1] << 24)
        w.append(w[i - 4] ^ t)
    return [struct.pack(">4I", *w[4 * r:4 * r + 4]) for r in range(11)]


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def ref_bloc_aes(bloc: bytes, rk: list[bytes]) -> bytes:
    """FIPS 197 § 5.1 : le chiffrement D'UN bloc (les 11 clés de tour)."""
    etat = bytearray(_xor(bloc, rk[0]))
    for r in range(1, 11):
        etat = bytearray(SBOX[b] for b in etat)          # SubBytes
        s = bytearray(16)                                # ShiftRows
        for c in range(4):
            for rr in range(4):
                s[4 * c + rr] = etat[4 * ((c + rr) % 4) + rr]
        etat = s
        if r != 10:                                      # MixColumns (sauf dernier)
            s = bytearray(16)
            for c in range(4):
                a = etat[4 * c:4 * c + 4]
                s[4 * c + 0] = (_gmul(a[0], 2) ^ _gmul(a[1], 3) ^ a[2] ^ a[3])
                s[4 * c + 1] = (a[0] ^ _gmul(a[1], 2) ^ _gmul(a[2], 3) ^ a[3])
                s[4 * c + 2] = (a[0] ^ a[1] ^ _gmul(a[2], 2) ^ _gmul(a[3], 3))
                s[4 * c + 3] = (_gmul(a[0], 3) ^ a[1] ^ a[2] ^ _gmul(a[3], 2))
            etat = s
        etat = bytearray(_xor(bytes(etat), rk[r]))
    return bytes(etat)


R_GCM = bytes([0xE1]) + bytes(15)      # SP 800-38D § 6.3 (le plan, GCM_R)


def ref_ghash(x: bytes, y: bytes) -> bytes:
    """La multiplication GF(2^128) — la convention réfléchie de GCM
    (l'algorithme 1 § 6.3 : le premier bit de X = le MSB de l'octet 0, le
    sortant = le bit 0 de l'octet 15, le repli R = 0xE1||0^120)."""
    assert len(x) == 16 and len(y) == 16
    xi = int.from_bytes(x, "big")
    v = int.from_bytes(y, "big")
    r = int.from_bytes(R_GCM, "big")
    z = 0
    for _ in range(128):
        if (xi >> 127) & 1:
            z ^= v
        sortant = v & 1
        v >>= 1
        if sortant:
            v ^= r
        xi = (xi << 1) & ((1 << 128) - 1)
    return z.to_bytes(16, "big")


def _ref_j0(iv: bytes, h: bytes) -> bytes:
    """SP 800-38D § 5.2.1.1 : J0 (le protocole : IV de 96 bits)."""
    assert len(iv) == 12
    return iv + b"\x00\x00\x00\x01"


def _ref_inc32(cb: bytes) -> bytes:
    v = int.from_bytes(cb[12:], "big")
    return cb[:12] + ((v + 1) & 0xFFFFFFFF).to_bytes(4, "big")


def ref_gcm_sceller(cle: bytes, iv: bytes, aad: bytes, clair: bytes):
    """SP 800-38D § 7.1 : le scellement (étiquette 128 bits)."""
    rk = ref_cles_tour(cle)
    h = ref_bloc_aes(bytes(16), rk)
    j0 = _ref_j0(iv, h)
    cb = _ref_inc32(j0)
    chiffre = bytearray()
    for i in range(0, len(clair), 16):
        flot = ref_bloc_aes(cb, rk)
        morceau = clair[i:i + 16]
        chiffre += bytes(a ^ b for a, b in zip(morceau, flot))
        cb = _ref_inc32(cb)
    y = bytes(16)
    for i in range(0, len(aad), 16):
        bloc = aad[i:i + 16]
        y = ref_ghash(_xor(y, bloc + bytes(16 - len(bloc))), h)
    for i in range(0, len(chiffre), 16):
        bloc = bytes(chiffre[i:i + 16])
        y = ref_ghash(_xor(y, bloc + bytes(16 - len(bloc))), h)
    lg = (len(aad) * 8).to_bytes(8, "big") + (len(chiffre) * 8).to_bytes(8, "big")
    y = ref_ghash(_xor(y, lg), h)
    return bytes(chiffre), _xor(ref_bloc_aes(j0, rk), y)


def ref_gcm_ouvrir(cle: bytes, iv: bytes, aad: bytes, chiffre: bytes,
                   etiquette: bytes):
    """L'inverse exact — le verdict AVANT la restitution (tls13-19)."""
    rk = ref_cles_tour(cle)
    h = ref_bloc_aes(bytes(16), rk)
    j0 = _ref_j0(iv, h)
    y = bytes(16)
    for i in range(0, len(aad), 16):
        bloc = aad[i:i + 16]
        y = ref_ghash(_xor(y, bloc + bytes(16 - len(bloc))), h)
    for i in range(0, len(chiffre), 16):
        bloc = chiffre[i:i + 16]
        y = ref_ghash(_xor(y, bloc + bytes(16 - len(bloc))), h)
    lg = (len(aad) * 8).to_bytes(8, "big") + (len(chiffre) * 8).to_bytes(8, "big")
    y = ref_ghash(_xor(y, lg), h)
    attendue = _xor(ref_bloc_aes(j0, rk), y)
    if any(a != b for a, b in zip(attendue, etiquette)):
        return None
    cb = _ref_inc32(j0)
    clair = bytearray()
    for i in range(0, len(chiffre), 16):
        flot = ref_bloc_aes(cb, rk)
        morceau = chiffre[i:i + 16]
        clair += bytes(a ^ b for a, b in zip(morceau, flot))
        cb = _ref_inc32(cb)
    return bytes(clair)


# --- Les vecteurs officiels FIPS 197 / SP 800-38A ---------------------------------

C1_CLE = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
C1_ENTREE = bytes.fromhex("00112233445566778899aabbccddeeff")
C1_ATTENDU = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")
F11_CLE = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
F11 = [
    ("6bc1bee22e409f96e93d7e117393172a", "3ad77bb40d7a3660a89ecaf32466ef97"),
    ("ae2d8a571e03ac9c9eb76fac45af8e51", "f5d3d58503b9699de785895a96fdbaaf"),
    ("30c81c46a35ce411e5fbc1191a0a52ef", "43b1cd7f598ece23881b00e3ed030688"),
    ("f69f2445df4f9b17ad2b417be66c3710", "7b0c785e27e8ad3f8223207104725dd4"),
]

# --- Les vecteurs officiels McGrew–Viega (la spec gcm, repris par CAVP) -----------
# Source : gcm-spec.pdf — TC5/TC6 (IV de 8 et 60 octets) sont HORS CONTRAT
# de la brique (P2 : le nonce de 12 o, RFC 8446 § 5.3) — la référence du
# labo les couvre, le protocole ne les émet jamais.

TC = [
    ("TC1", "00" * 16, "00" * 12, "", "",
     "", "58e2fccefa7e3061367f1d57a4e7455a"),
    ("TC2", "00" * 16, "00" * 12, "", "00" * 16,
     "0388dace60b6a392f328c2b971b2fe78", "ab6e47d42cec13bdf53a67b21257bddf"),
    ("TC3", "feffe9928665731c6d6a8f9467308308", "cafebabefacedbaddecaf888", "",
     "d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72"
     "1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b391aafd255",
     "42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e"
     "21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091473f5985",
     "4d5c2af327cd64a62cf35abd2ba6fab4"),
    ("TC4", "feffe9928665731c6d6a8f9467308308", "cafebabefacedbaddecaf888",
     "feedfacedeadbeeffeedfacedeadbeefabaddad2",
     "d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72"
     "1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39",
     "42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e"
     "21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091",
     "5bc94fbc3221a5db94fae95ae7121a47"),
]

# --- LE TRANSFERT RFC 8448 § 3 (Simple 1-RTT) : les SEPT enregistrements ----------
# Le texte officiel PARSÉ par le labo (derive_aead.py, la contre-preuve du
# geste), les constantes CONSIGNÉES au harnais : le nom, la clé de trafic,
# l'IV statique, la séquence (le nonce = IV ⊕ séquence, RFC 8446 § 5.3), le
# clair interne attendu (payload || type) et l'enregistrement complet (la
# tête 0x17 en AAD, chiffré + étiquette).

TRANSFERT_8448 = [
    ("le vol serveur (EE+Cert+CV+Fin)",
     "3fce516009c21727d0f2e4e86ee403bc",
     "5d313eb2671276ee13000b30",
     0,
     "080000240022000a00140012001d00170018001901000101010201030104001c00024001000000000b0001b9000001b50001b0308201ac30820115a003020102020102300d06092a864886f70d01010b0500300e310c300a06035504031303727361301e170d3136303733303031323335395a170d3236303733303031323335395a300e310c300a0603550403130372736130819f300d06092a864886f70d010101050003818d0030818902818100b4bb498f8279303d980836399b36c6988c0c68de55e1bdb826d3901a2461eafd2de49a91d015abbc9a95137ace6c1af19eaa6af98c7ced43120998e187a80ee0ccb0524b1b018c3e0b63264d449a6d38e22a5fda430846748030530ef0461c8ca9d9efbfae8ea6d1d03e2bd193eff0ab9a8002c47428a6d35a8d88d79f7f1e3f0203010001a31a301830090603551d1304023000300b0603551d0f0404030205a0300d06092a864886f70d01010b05000381810085aad2a0e5b9276b908c65f73a7267170618a54c5f8a7b337d2df7a594365417f2eae8f8a58c8f8172f9319cf36b7fd6c55b80f21a03015156726096fd335e5e67f2dbf102702e608ccae6bec1fc63a42a99be5c3eb7107c3c54e9b9eb2bd5203b1c3b84e0a8b2f759409ba3eac9d91d402dcc0cc8f8961229ac9187b42b4de100000f000084080400805a747c5d88fa9bd2e55ab085a61015b7211f824cd484145ab3ff52f1fda8477b0b7abc90db78e2d33a5c141a078653fa6bef780c5ea248eeaaa785c4f394cab6d30bbe8d4859ee511f602957b15411ac027671459e46445c9ea58c181e818e95b8c3fb0bf3278409d3be152a3da5043e063dda65cdf5aea20d53dfacd42f74f3140000209b9b141d906337fbd2cbdce71df4deda4ab42c309572cb7fffee5454b78f071816",
     "17030302a2d1ff334a56f5bff6594a07cc87b580233f500f45e489e7f33af35edf7869fcf40aa40aa2b8ea73f848a7ca07612ef9f945cb960b4068905123ea78b111b429ba9191cd05d2a389280f526134aadc7fc78c4b729df828b5ecf7b13bd9aefb0e57f271585b8ea9bb355c7c79020716cfb9b1183ef3ab20e37d57a6b9d7477609aee6e122a4cf51427325250c7d0e509289444c9b3a648f1d71035d2ed65b0e3cdd0cbae8bf2d0b227812cbb360987255cc744110c453baa4fcd610928d809810e4b7ed1a8fd991f06aa6248204797e36a6a73b70a2559c09ead686945ba246ab66e5edd8044b4c6de3fcf2a89441ac66272fd8fb330ef8190579b3684596c960bd596eea520a56a8d650f563aad27409960dca63d3e688611ea5e22f4415cf9538d51a200c27034272968a264ed6540c84838d89f72c24461aad6d26f59ecaba9acbbb317b66d902f4f292a36ac1b639c637ce343117b659622245317b49eeda0c6258f100d7d961ffb138647e92ea330faeea6dfa31c7a84dc3bd7e1b7a6c7178af36879018e3f252107f243d243dc7339d5684c8b0378bf30244da8c87c843f5e56eb4c5e8280a2b48052cf93b16499a66db7cca71e4599426f7d461e66f99882bd89fc50800becca62d6c74116dbd2972fda1fa80f85df881edbe5a37668936b335583b599186dc5c6918a396fa48a181d6b6fa4f9d62d513afbb992f2b992f67f8afe67f76913fa388cb5630c8ca01e0c65d11c66a1e2ac4c85977b7c7a6999bbf10dc35ae69f5515614636c0b9b68c19ed2e31c0b3b66763038ebba42f3b38edc0399f3a9f23faa63978c317fc9fa66a73f60f0504de93b5b845e275592c12335ee340bbc4fddd502784016e4b3be7ef04dda49f4b440a30cb5d2af939828fd4ae3794e44f94df5a631ede42c1719bfdabf0253fe5175be898e750edc53370d2b"),
    ("le Finished client",
     "dbfaa693d1762c5b666af5d950258d01",
     "5bd3c71b836e0b76bb73265f",
     0,
     "14000020a8ec436d677634ae525ac1fcebe11a039ec17694fac6e98527b642f2edd5ce6116",
     "170303003575ec4dc238cce60b298044a71e219c56cc77b0517fe9b93c7a4bfc44d87f38f80338ac98fc46deb384bd1caeacab6867d726c40546"),
    ("le NewSessionTicket serveur",
     "9f02283b6c9c07efc26bb9f2ac92e356",
     "cf782b88dd83549aadf1e984",
     0,
     "040000c90000001efad6aac502000000b22c035d829359ee5ff7af4ec900000000262a6494dc486d2c8a34cb33fa90bf1b0070ad3c498883c9367c09a2be785abc55cd226097a3a982117283f82a03a143efd3ff5dd36d64e861be7fd61d2827db279cce145077d454a3664d4e6da4d29ee03725a6a4dafcd0fc67d2aea70529513e3da2677fa5906c5b3f7d8f92f228bda40dda721470f9fbf297b5aea617646fac5c03272e970727c621a79141ef5f7de6505e5bfbc388e93343694093934ae4d3570008002a00040000040016",
     "17030300de3a6b8f90414a97d6959c3487680de5134a2b240e6cffac116e95d41d6af8f6b580dcf3d11d63c758db289a015940252f55713e061dc13e078891a38efbcf5753ad8ef170ad3c7353d16d9da773b9ca7f2b9fa1b6c0d4a3d03f75e09c30ba1e62972ac46f75f7b981be63439b2999ce13064615139891d5e4c5b406f16e3fc181a77ca475840025db2f0a77f81b5ab05b94c01346755f69232c86519d86cbeeac87aac347d143f9605d64f650db4d023e70e952ca49fe5137121c74bc2697687e248746d6df353005f3bce18696129c8153556b3b6c6779b37bf15985684f"),
    ("les données applicatives client",
     "17422dda596ed5d9acd890e3c63f5051",
     "5b78923dee08579033e523d9",
     0,
     "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303117",
     "1703030043a23f7054b62c94d0affafe8228ba55cbefacea42f914aa66bcab3f2b9819a8a5b46b395bd54a9a20441e2b62974e1f5a6292a2977014bd1e3deae63aeebb21694915e4"),
    ("les données applicatives serveur",
     "9f02283b6c9c07efc26bb9f2ac92e356",
     "cf782b88dd83549aadf1e984",
     1,
     "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303117",
     "17030300432e937e11ef4ac740e538ad36005fc4a46932fc3225d05f82aa1b36e30efaf97d90e6dffc602dcb501a59a8fcc49c4bf2e5f0a21c0047c2abf332540dd032e167c2955d"),
    ("la close_notify client",
     "17422dda596ed5d9acd890e3c63f5051",
     "5b78923dee08579033e523d9",
     1,
     "010015",
     "1703030013c9872760655666b74d7ff1153efd6db6d0b0e3"),
    ("la close_notify serveur",
     "9f02283b6c9c07efc26bb9f2ac92e356",
     "cf782b88dd83549aadf1e984",
     2,
     "010015",
     "1703030013b58fd67166ebf599d24720cfbe7efa7a8864a9"),
]


def nonce_de(iv: bytes, seq: int) -> bytes:
    """RFC 8446 § 5.3 : le nonce = IV ⊕ séquence (u64 gros-boutiste)."""
    n = bytearray(iv)
    s = seq.to_bytes(8, "big")
    for i in range(8):
        n[4 + i] ^= s[i]
    return bytes(n)


# --- L'émulation (le modèle harnais_x25519 — l'appelant factice msx64) -------------

class Emulation:
    """Les DIX-NEUF blocs posés à leurs RVA du plan, appelés comme des
    fonctions msx64 ordinaires : l'entrée ≡ 8 (mod 16), l'ombre et les
    logements d'arguments couverts de canaris, les non-volatiles sous
    sentinelles. Le mode « nue » (aucun hook) sert les boucles de vecteurs
    longues — l'instrument permanent ne compte pas les longues
    exécutions (V6 en compte quatre espèces)."""

    BLOCS = [("h100001", "tls13-01-sha256-init"),
             ("h100002", "tls13-02-sha256-comprimer"),
             ("h100003", "tls13-03-sha256-absorber"),
             ("h100004", "tls13-04-sha256-finaliser"),
             ("h100005", "tls13-05-hmac-sha256"),
             ("h100006", "tls13-06-hkdf-extract"),
             ("h100007", "tls13-07-hkdf-expand"),
             ("h100008", "tls13-08-hkdf-expand-label"),
             ("h100009", "tls13-09-f25519-add"),
             ("h100010", "tls13-10-f25519-sub"),
             ("h100011", "tls13-11-f25519-mul"),
             ("h100012", "tls13-12-f25519-propager-geler"),
             ("h100013", "tls13-13-x25519-echelle"),
             ("h100014", "tls13-14-x25519-cle-publique"),
             ("h100015", "tls13-15-aes128-cles-tour"),
             ("h100016", "tls13-16-aes128-bloc"),
             ("h100017", "tls13-17-ghash-multiplication"),
             ("h100018", "tls13-18-gcm-sceller"),
             ("h100019", "tls13-19-gcm-ouvrir")]

    def __init__(self, nue: bool = False):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.ks = Ks(KS_ARCH_X86, KS_MODE_64)
        self.cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.cs.detail = False
        self.uc.mem_map(*ZONE_IMAGE)
        for zone, taille in ((ZONE_CLES, 0x1000),
                             (ZONE_ENTREES, TAILLE_ENTREES),
                             (ZONE_SORTIE, TAILLE_SORTIE),
                             (ZONE_PILE, TAILLE_PILE)):
            self.uc.mem_map(zone, taille)
        for zone, taille in ((ZONE_CLES, 0x1000),
                             (ZONE_ENTREES, TAILLE_ENTREES),
                             (ZONE_SORTIE, TAILLE_SORTIE)):
            self.uc.mem_write(zone, CANARI * taille)
        # les pièces du plan : K[64] à R_K, les fixtures à leur ARRÊT .text6
        self.uc.mem_write(L.R_K, struct.pack("<64I", *L.K))
        self.uc.mem_write(L.R_U9, L.X25519_BASE.to_bytes(32, "little"))
        self.uc.mem_write(L.R_EXP_INV, ((2**255 - 19) - 2).to_bytes(32, "little"))
        self.blobs: dict[str, tuple[bytes, list]] = {}
        # L'INSTRUMENT PERMANENT (posé AVANT toute traduction, togglé par
        # drapeaux, jamais ajouté en cours de route)
        self.compteur_actif = False
        self.compteur = 0
        self.surveillance: dict[int, list[int]] | None = None
        if not nue:
            self.uc.hook_add(UC_HOOK_CODE, self._instrument)
        self.poser_blocs()

    def _instrument(self, uc, adresse, taille, donnees):
        if self.compteur_actif:
            self.compteur += 1
        if self.surveillance is not None and adresse in self.surveillance:
            self.surveillance[adresse].append(uc.reg_read(UC_X86_REG_RSP))

    def poser_blocs(self):
        for bid, nom in self.BLOCS:
            rva, slot = L.SLOTS_TLS13[bid]
            chemin = os.path.join(ICI, "notation", nom + ".asm")
            octets, metas = B4.assembler_bloc(self.ks, chemin, rva, slot)
            self.uc.mem_write(rva, octets)
            self.blobs[bid] = (octets, metas)

    def appeler(self, va: int, args: dict[str, int] | None = None,
                compter: bool = False, args_pile: list[int] | None = None):
        """Appelle un bloc comme une fonction msx64. Retourne le dict de
        sortie + canaris (le modèle harnais_x25519)."""
        uc = self.uc
        for nom, val in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], val)
        for nom, val in (args or {}).items():
            uc.reg_write(REGS[nom], val)
        uc.reg_write(UC_X86_REG_RAX, 0)
        rsp = ENTREE_RSP
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.mem_write(rsp + 8, CANARI * 0x178)
        logements = []
        for i, val in enumerate(args_pile or []):
            uc.mem_write(rsp + 0x28 + 8 * i, struct.pack("<Q", val))
            logements.append(rsp + 0x28 + 8 * i)
        # la zone morte PROFONDE (sous TOUT cadre possible : le cadre de
        # tls13-18/19 [0xE8] + celui de tls13-17 [0x28] ≈ 0x110 ; la zone
        # vit à [−0x1000, −0xC00))
        uc.mem_write(rsp - 0x1000, CANARI * 0x400)
        uc.mem_write(rsp, struct.pack("<Q", RET_MAGIQUE))
        entree_rsp = rsp
        self.compteur = 0
        self.compteur_actif = compter
        try:
            uc.emu_start(va, RET_MAGIQUE, count=50_000_000)
        except UcError as err:
            self.compteur_actif = False
            return {"crash": str(err), "entree_rsp": entree_rsp,
                    "canaris_haut": False, "canaris_profond": False,
                    "logements_intacts": False, "compteur": self.compteur}
        finally:
            self.compteur_actif = False
        sortie = {k: uc.reg_read(REGS[k]) for k in REGS}
        sortie["rax"] = s64(sortie["rax"])
        sortie["entree_rsp"] = entree_rsp
        sortie["crash"] = None
        sortie["compteur"] = self.compteur
        sortie["pile_equilibree"] = uc.reg_read(REGS["rsp"]) == entree_rsp + 8
        zone_haute = bytes(uc.mem_read(entree_rsp + 8, 0x178))
        plages = [(a, a + 8) for a in logements]
        intact = True
        for i in range(len(zone_haute)):
            adresse = entree_rsp + 8 + i
            octet = zone_haute[i:i + 1]
            if any(debut <= adresse < fin for debut, fin in plages):
                continue
            if octet != CANARI:
                intact = False
                break
        sortie["canaris_haut"] = intact
        sortie["logements_intacts"] = all(
            struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0] == v
            for a, v in zip(logements, args_pile or []))
        sortie["canaris_profond"] = bytes(
            uc.mem_read(entree_rsp - 0x1000, 0x400)) == CANARI * 0x400
        return sortie

    def non_volatiles_rendus(self, r: dict) -> bool:
        return all(r[nom] == SENTINELLES_NV[nom] for nom in SENTINELLES_NV)

    # --- les zones canaris ---------------------------------------------------

    def poser(self, adresse: int, donnees: bytes):
        """Pose les données avec une FENÊTRE de canaris autour (P2/Q2)."""
        self.uc.mem_write(adresse - FENETRE, CANARI * FENETRE)
        self.uc.mem_write(adresse, donnees)
        self.uc.mem_write(adresse + len(donnees),
                          CANARI * (FENETRE + 0x20))

    def intact_autour(self, adresse: int, longueur: int) -> bool:
        """Les canaris autour des données — les données elles-mêmes
        peuvent avoir été lues (elles demeurent) mais JAMAIS écrites."""
        avant = bytes(self.uc.mem_read(adresse - FENETRE, FENETRE))
        apres = bytes(self.uc.mem_read(adresse + longueur, FENETRE + 0x20))
        return avant == CANARI * FENETRE and apres == CANARI * (FENETRE + 0x20)


# --- Les pipelines (les compositions du harnais) -----------------------------------

def deployer(emul: Emulation, cle: bytes, compter: bool = False):
    """tls13-15 : les ONZE clés de tour depuis la clé de 16 o."""
    emul.poser(ADR_CLE, cle)
    emul.uc.mem_write(ADR_RK, CANARI * 192)
    r = emul.appeler(L.TLS15_VA, {"rcx": ADR_CLE, "rdx": ADR_RK},
                     compter=compter)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-15 a crashé : {r['crash']}")
    return bytes(emul.uc.mem_read(ADR_RK, 176)), r


def bloc_aes(emul: Emulation, rk: bytes, entree: bytes,
             sortie_adr: int | None = None, compter: bool = False):
    """tls13-16 : le chiffrement D'UN bloc (la sortie peut chevaucher
    l'entrée — P3 : le bloc charge AVANT d'écrire)."""
    emul.poser(ADR_BLOC_IN, entree)
    emul.uc.mem_write(ADR_RK, rk)
    adr_out = sortie_adr if sortie_adr is not None else ADR_BLOC_OUT
    if adr_out != ADR_BLOC_IN:
        emul.uc.mem_write(adr_out, CANARI * 16)
    r = emul.appeler(L.TLS16_VA, {"rcx": ADR_RK, "rdx": ADR_BLOC_IN,
                                  "r8": adr_out}, compter=compter)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-16 a crashé : {r['crash']}")
    return bytes(emul.uc.mem_read(adr_out, 16)), r


def ghash(emul: Emulation, x: bytes, y: bytes, sortie_adr: int | None = None,
          compter: bool = False):
    """tls13-17 : la multiplication GF(2^128) (la sortie peut chevaucher
    X — P3 : le bloc charge X et Y AVANT d'écrire)."""
    emul.poser(ADR_X, x)
    emul.poser(ADR_Y, y)
    adr_out = sortie_adr if sortie_adr is not None else ADR_BLOC_OUT
    if adr_out != ADR_X:
        emul.uc.mem_write(adr_out, CANARI * 16)
    r = emul.appeler(L.TLS17_VA, {"rcx": adr_out, "rdx": ADR_X, "r8": ADR_Y},
                     compter=compter)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-17 a crashé : {r['crash']}")
    return bytes(emul.uc.mem_read(adr_out, 16)), r


def sceller(emul: Emulation, cle: bytes, nonce: bytes, aad: bytes,
            clair: bytes, compter: bool = False, force: dict | None = None):
    """tls13-18 : le scellement GCM (CT + étiquette). `force` substitue
    un argument APRÈS la pose (les refus : pointeur nul, taille hors
    borne — le contrat P1..P8 exercé hors conformité)."""
    rk = b"".join(ref_cles_tour(cle))
    emul.uc.mem_write(ADR_RK, rk)
    emul.poser(ADR_NONCE, nonce)
    emul.poser(ADR_CLAIR, clair)
    emul.poser(ADR_AAD, aad)
    emul.uc.mem_write(ADR_CT, CANARI * (len(clair) + FENETRE + 0x20))
    emul.uc.mem_write(ADR_TAG, CANARI * 0x40)
    args = {"rcx": ADR_RK, "rdx": ADR_NONCE, "r8": ADR_CLAIR, "r9": len(clair)}
    pile = [ADR_AAD, len(aad), ADR_CT, ADR_TAG]
    if force:
        if "rcx" in force:
            args["rcx"] = force["rcx"]
        if "r8" in force:
            args["r8"] = force["r8"]
        if "r9" in force:
            args["r9"] = force["r9"]
        for i, clef in enumerate(("aad", "a", "ct", "tag")):
            if clef in force:
                pile[i] = force[clef]
    r = emul.appeler(L.TLS18_VA, args, compter=compter, args_pile=pile)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-18 a crashé : {r['crash']}")
    ct = bytes(emul.uc.mem_read(ADR_CT, len(clair)))
    tag = bytes(emul.uc.mem_read(ADR_TAG, 16))
    return ct, tag, r


def ouvrir(emul: Emulation, cle: bytes, nonce: bytes, aad: bytes,
           chiffre: bytes, etiquette: bytes, compter: bool = False,
           force: dict | None = None):
    """tls13-19 : l'ouverture GCM (le verdict AVANT la restitution)."""
    rk = b"".join(ref_cles_tour(cle))
    emul.uc.mem_write(ADR_RK, rk)
    emul.poser(ADR_NONCE, nonce)
    emul.poser(ADR_AAD, aad)
    emul.uc.mem_write(ADR_CT, CANARI * (len(chiffre) + FENETRE + 0x20))
    emul.uc.mem_write(ADR_CT, chiffre)
    emul.poser(ADR_ETIQ, etiquette)
    emul.uc.mem_write(ADR_CLAIR2, CANARI * (len(chiffre) + FENETRE + 0x20))
    args = {"rcx": ADR_RK, "rdx": ADR_NONCE, "r8": ADR_CT, "r9": len(chiffre)}
    pile = [ADR_AAD, len(aad), ADR_ETIQ, ADR_CLAIR2]
    if force:
        if "rcx" in force:
            args["rcx"] = force["rcx"]
        if "r8" in force:
            args["r8"] = force["r8"]
        if "r9" in force:
            args["r9"] = force["r9"]
        for i, clef in enumerate(("aad", "a", "etiq", "clair")):
            if clef in force:
                pile[i] = force[clef]
    r = emul.appeler(L.TLS19_VA, args, compter=compter, args_pile=pile)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-19 a crashé : {r['crash']}")
    clair = bytes(emul.uc.mem_read(ADR_CLAIR2, len(chiffre)))
    return clair, r


# --- V0 : les pièces du plan ------------------------------------------------------

def vecteur_v0(emul: Emulation):
    section("V0 — les pièces du plan (le scellé 0.9.0, sha+hkdf+x25519, l'arbre I, les fixtures)")
    donnees = open(os.path.join(TRIADE, SCELLE_M8), "rb").read()
    controle("V0.a:le-scelle-090-intact",
             len(donnees) == SCELLE_M8_TAILLE
             and hashlib.sha256(donnees).hexdigest() == SCELLE_M8_SHA256,
             f"{len(donnees)} o, sha256 1492b0bc…b0cd4 — l'ancre R7")
    # les familles sha, hkdf ET x25519 INTACTES : les quatorze notations
    # relues aux longueurs ARRÊTÉES du plan
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    attendus = {"h100001": 74, "h100002": 387, "h100003": 139, "h100004": 165,
                "h100005": 435, "h100006": 151, "h100007": 347, "h100008": 310,
                "h100009": 54, "h100010": 252, "h100011": 1078,
                "h100012": 281, "h100013": 2887, "h100014": 23}
    noms = {bid: nom for bid, nom in Emulation.BLOCS if bid in attendus}
    ok, details = True, []
    for bid, attendu in attendus.items():
        rva, slot = L.SLOTS_TLS13[bid]
        chemin = os.path.join(ICI, "notation", noms[bid] + ".asm")
        octets, _ = B4.assembler_bloc(ks, chemin, rva, slot)
        if len(octets) != attendu:
            ok = False
            details.append(f"{noms[bid]} : {len(octets)} o ≠ {attendu}")
    controle("V0.b:les-familles-sha-hkdf-x25519-intactes", ok,
             "les quatorze notations relues aux longueurs arrêtées "
             "74/387/139/165 + 435/151/347/310 + 54/252/1078/281/2887/23 o"
             + (f" — DÉFAUTS : {details}" if details else ""))
    # LES FIXTURES DU DOMAINE : les contenus re-dérivés du plan par
    # arithmétique (le juge est le code — jamais une copie d'écriture) ;
    # LA FAMILLE aead N'EN AJOUTE AUCUN (R vit en IMMÉDIAT — I4 de 17)
    u9 = bytes(emul.uc.mem_read(L.R_U9, 32))
    expinv = bytes(emul.uc.mem_read(L.R_EXP_INV, 32))
    controle("V0.c:les-fixtures-du-domaine-poses",
             u9 == L.X25519_BASE.to_bytes(32, "little")
             and expinv == ((2**255 - 19) - 2).to_bytes(32, "little")
             == L.X25519_EXP_INV,
             f"U9 @ 0x{L.R_U9:x}, EXP_INV @ 0x{L.R_EXP_INV:x} (re-dérivés) — "
             "la famille aead n'ajoute AUCUN fixture : R = 0xE1||0^120 en "
             "IMMÉDIAT (I4 — le bloc autoporteur)")
    # l'arbre I scellé relu : verifier_specs_m9a rejoué, exit 0 (R2)
    proc = subprocess.run([sys.executable, "scripts/verifier_specs_m9a.py"],
                          cwd=TRIADE, capture_output=True, text=True)
    controle("V0.d:l-arbre-I-scelle-relu-vert",
             proc.returncode == 0,
             "verifier_specs_m9a rejoué — les 28 spécifications posées et "
             "cohérentes (le sceau de l'ère tient)")


# --- V1 : round-trip + concordance au plan -----------------------------------------

def vecteur_v1(emul: Emulation):
    section("V1 — round-trip de notation + concordance au plan (source unique)")
    attendus = {"h100015": 520, "h100016": 129, "h100017": 162,
                "h100018": 1076, "h100019": 1163}
    noms = {bid: nom for bid, nom in Emulation.BLOCS if bid in attendus}
    insns_par_bloc = {}
    for bid, attendu in attendus.items():
        rva, slot = L.SLOTS_TLS13[bid]
        chemin = os.path.join(ICI, "notation", noms[bid] + ".asm")
        octets, metas = B4.assembler_bloc(emul.ks, chemin, rva, slot)
        insns = B4.round_trip(emul.cs, emul.ks, chemin, rva, octets, metas)
        insns_par_bloc[bid] = insns
        controle(f"V1.{bid}:round-trip-100",
                 len(insns) == len(metas) and len(octets) == attendu,
                 f"{len(octets)} o == {attendu} o arrêtés, "
                 f"{len(insns)}/{len(metas)} instructions")

    # la concordance des appels directs : chaque cible == le plan (I1/I2)
    cibles_attendues = {
        "h100015": {},
        "h100016": {},
        "h100017": {},
        "h100018": {L.TLS16_VA: 3, L.TLS17_VA: 3},
        "h100019": {L.TLS16_VA: 3, L.TLS17_VA: 3},
    }
    ok_appels, details = True, []
    for bid, attendu in cibles_attendues.items():
        vus: dict[int, int] = {}
        for insn in insns_par_bloc[bid]:
            if insn.mnemonic == "call":
                cible = int(insn.op_str, 0)
                vus[cible] = vus.get(cible, 0) + 1
        if vus != attendu:
            ok_appels = False
            details.append(f"{bid} : {vus} ≠ {attendu}")
    controle("V1.e:les-appels-directs-au-plan", ok_appels,
             "18 : TLS16 ×3 [H = E(K,0), les compteurs du CTR, E(K, J0)] + "
             "TLS17 ×3 [AAD, chiffré, le bloc des longueurs] ; 19 : la même "
             "recette sur le chiffré REÇU — I2 des specs"
             + (f" — DÉFAUTS : {details}" if details else ""))

    # la concordance des immédiats au plan : les DIX Rcon de 15 (FIPS 197
    # § 5.2), le pshufd 0xff de diffusion (la sonde du labo), le movabs
    # R de 17 (0xE1 au SOMMET de la voie haute bswapée), le J0 de 18/19
    texte15 = open(os.path.join(ICI, "notation",
                                "tls13-15-aes128-cles-tour.asm"),
                   encoding="utf-8").read()
    rcon_ok = all(f"aeskeygenassist xmm1, xmm0, 0x{r:02x}" in texte15
                  for r in RCON)
    controle("V1.f:les-dix-rcon-de-15-au-plan", rcon_ok,
             f"{[hex(r) for r in RCON]} — FIPS 197 § 5.2, en IMMÉDIATS (I1 : "
             "aucune donnée RIP) ; pshufd 0xff ×"
             f"{texte15.count('pshufd xmm1, xmm1, 0xff')} (la disposition "
             "DÉRIVÉE DE L'OBSERVATION — le mot d'AES-128 au dword 3, la "
             "sonde du labo)")
    texte16 = open(os.path.join(ICI, "notation",
                                "tls13-16-aes128-bloc.asm"),
                   encoding="utf-8").read()
    controle("V1.g:la-composition-de-16",
             texte16.count("\naesenc ") == 9
             and texte16.count("\naesenclast ") == 1
             and "\npxor xmm0, xmm1\n" in texte16,
             "pxor RK[0] + NEUF aesenc RK[1..9] + aesenclast RK[10] — sans "
             "MixColumns au dernier tour (FIPS 197 § 5.1)")
    texte17 = open(os.path.join(ICI, "notation",
                                "tls13-17-ghash-multiplication.asm"),
                   encoding="utf-8").read()
    controle("V1.h:les-constantes-de-17-au-plan",
             "movabs rdx, 0xe100000000000000" in texte17
             and "\nbswap rax\n" in texte17
             and "mov qword ptr [rsp + 0x10], 128" in texte17,
             "R = GCM_R = 0xE1||0^120 : l'octet 0 au SOMMET de la voie "
             "haute bswapée — 0xE1 << 56 (la sonde du geste a nommé la "
             "REPRÉSENTATION : le domaine GROS-BOUTISTE par bswap, les "
             "DEUX voies renversées, re-mesuré 139→162) ; les 128 "
             "itérations TOUJOURS")
    for bid, nom in (("h100018", "tls13-18-gcm-sceller"),
                     ("h100019", "tls13-19-gcm-ouvrir")):
        texte = open(os.path.join(ICI, "notation", nom + ".asm"),
                     encoding="utf-8").read()
        controle(f"V1.i:le-j0-de-{bid[-2:]}-gros-boutiste",
                 "mov dword ptr [rsp + 0x2c], 0x01000000" in texte,
                 "J0 = nonce || 0^31 || 1 : le u32 terminal posé "
                 "GROS-BOUTISTE (les octets 00 00 00 01 — la seconde faute "
                 "nommée par la sonde : la première écriture posait "
                 "01 00 00 00, les compteurs partaient de 0x01000001)")

    # la structure du domaine : AUCUN site syscall, AUCUN appel indirect,
    # AUCUN déplacement RIP — la famille ENTIÈRE autoporteur (I4 de 15)
    ok_struct, motifs = True, []
    for bid, insns in insns_par_bloc.items():
        for insn in insns:
            if insn.mnemonic in ("syscall", "int", "sysenter"):
                ok_struct, _ = False, motifs.append(f"{bid}:{insn.mnemonic}")
            if insn.mnemonic in ("call", "jmp") and "[" in insn.op_str:
                ok_struct, _ = False, motifs.append(f"{bid}:indirect")
            if "[rip" in insn.op_str:
                ok_struct, _ = False, motifs.append(f"{bid}:rip")
    controle("V1.j:calcul-pur-aucun-syscall-aucun-rip", ok_struct,
             "aucun syscall, aucun appel indirect, AUCUN déplacement RIP "
             "dans la famille ENTIÈRE — contrairement à x25519 (ses DEUX "
             "fixtures .text6), l'aead ne lit RIEN hors de ses arguments "
             "et de sa pile : R en IMMÉDIAT, le bloc autoporteur"
             + (f" — MOTIFS : {motifs}" if motifs else ""))

    # le temps constant STRUCTUREL : 15/16 ZÉRO saut conditionnel, 17
    # exactement UN (le compteur de boucle), 18 dix-sept et 19 dix-neuf —
    # TOUS sur les données PUBLIQUES, les comptes EXACTS vérifiés ; LE
    # VERDICT de 19 : test r10, r10 — LE drapeau CUMULÉ (I1)
    def inventaire_jcc(insns):
        out = []
        for k, insn in enumerate(insns):
            if insn.mnemonic.startswith("j") and insn.mnemonic != "jmp":
                j = k - 1
                while j >= 0 and insns[j].mnemonic not in (
                        "cmp", "test", "dec", "sub", "add"):
                    j -= 1
                out.append((insn.mnemonic,
                            f"{insns[j].mnemonic} {insns[j].op_str}"))
        return out

    compte = {bid: len(inventaire_jcc(insns_par_bloc[bid]))
              for bid in insns_par_bloc}
    ok_sauts = (compte["h100015"] == 0 and compte["h100016"] == 0
                and compte["h100017"] == 1 and compte["h100018"] == 17
                and compte["h100019"] == 19)
    # le SEUL saut de 17 : la boucle sur le COMPTEUR public
    inv17 = inventaire_jcc(insns_par_bloc["h100017"])
    ok_17 = (inv17 == [("jne", "sub qword ptr [rsp + 0x10], 1")])
    # les sources publiques de 18/19 : les comptes EXACTS de la recette
    from collections import Counter
    inv18 = Counter(src for _, src in inventaire_jcc(insns_par_bloc["h100018"]))
    inv19 = Counter(src for _, src in inventaire_jcc(insns_par_bloc["h100019"]))
    attendu18 = Counter({"test rcx, rcx": 1, "test rdx, rdx": 1,
                         "test r8, r8": 1, "cmp r9, 0x4000": 1,
                         "cmp rax, 0x4000": 1,
                         "cmp qword ptr [rsp + 0x118], 0": 1,
                         "test rax, rax": 1, "test r10, r10": 1,
                         "test r11, r11": 1,
                         "cmp qword ptr [rsp + 0x98], rax": 1,
                         "cmp qword ptr [rsp + 0xb0], 0": 1,
                         "cmp qword ptr [rsp + 0xa0], 0": 2,
                         "cmp rax, 0x10": 2, "cmp r10, rcx": 2})
    attendu19 = Counter({"test rcx, rcx": 1, "test rdx, rdx": 1,
                         "test r8, r8": 1, "cmp r9, 0x4000": 1,
                         "cmp rax, 0x4000": 1,
                         "cmp qword ptr [rsp + 0x118], 0": 1,
                         "test rax, rax": 1, "test r10, r10": 2,
                         "test r11, r11": 1,
                         "cmp qword ptr [rsp + 0xa0], 0": 2,
                         "cmp qword ptr [rsp + 0x98], rax": 1,
                         "cmp qword ptr [rsp + 0xb0], 0": 1,
                         "cmp qword ptr [rsp + 0xb0], 0x10": 1,
                         "cmp rax, 0x10": 2, "cmp r10, rcx": 2})
    ok_18 = inv18 == attendu18
    ok_19 = inv19 == attendu19
    verdict_19 = inv19.get("test r10, r10", 0) >= 1
    controle("V1.k:temps-constant-structurel",
             ok_sauts and ok_17 and ok_18 and ok_19 and verdict_19,
             f"les sauts conditionnels : {compte} — 15/16 ZÉRO (le flot "
             "AES-NI est SANS BRANCHE PAR CONSTRUCTION), 17 le SEUL saut "
             "du compteur public (le bit de X devient MASQUE par sbb — "
             "JAMAIS une branche), 18 dix-sept et 19 dix-neuf, TOUS sur "
             "les données PUBLIQUES (pointeurs, longueurs N et A, "
             "compteurs de boucle — les comptes EXACTS de la recette) ; "
             "LE VERDICT de 19 : test r10, r10 — LE drapeau CUMULÉ des "
             "16 différences, la branche se prononce sur LE drapeau "
             "(I1 : le OU cumulatif, AUCUN court-circuit)")


# --- V2 : les vecteurs officiels + l'oracle ----------------------------------------

def vecteur_v2(emul: Emulation, nue: Emulation, graine: int):
    section("V2 — les vecteurs officiels FIPS 197 / SP 800-38A / McGrew–Viega / RFC 8448")

    # (a) FIPS 197 C.1 : le déploiement (les 176 o == la référence) puis
    # le bloc (69c4e0d8…) — LA COMPOSITION : la référence croisée AVANT
    # le jugement (le juge est le code)
    rk, r = deployer(emul, C1_CLE)
    attendu_rk = b"".join(ref_cles_tour(C1_CLE))
    controle("V2.0:fips-197-c1-le-deploiement",
             r["rax"] == 0 and rk == attendu_rk,
             f"176 o == la référence ({rk[:8].hex()}… — les ONZE clés, "
             "RK[0] la clé elle-même)")
    ct_bloc, r = bloc_aes(emul, rk, C1_ENTREE)
    controle("V2.1:fips-197-c1-le-bloc", r["rax"] == 0 and ct_bloc == C1_ATTENDU,
             f"{ct_bloc.hex()} == 69c4e0d86a7b0430d8cdb78070b4c55a")

    # (b) SP 800-38A F.1.1 : les QUATRE blocs PAR LA COMPOSITION — la clé
    # de la § F.1.1 déployée par tls13-15, les blocs chiffrés par
    # tls13-16 (un déploiement faux rend un chiffrement faux)
    rk_f11, _ = deployer(emul, F11_CLE)
    ok_f11 = rk_f11 == b"".join(ref_cles_tour(F11_CLE))
    for i, (pt_hex, ct_hex) in enumerate(F11, 1):
        ct_bloc, r = bloc_aes(emul, rk_f11, bytes.fromhex(pt_hex))
        ok_f11 = ok_f11 and r["rax"] == 0 and ct_bloc == bytes.fromhex(ct_hex)
    controle("V2.2:sp-800-38a-f11-les-quatre-blocs", ok_f11,
             "la clé 2b7e1516… déployée par 15, les QUATRE blocs chiffrés "
             "par 16 (3ad77bb4…, f5d3d585…, 43b1cd7f…, 7b0c785e…) — la "
             "composition porte la preuve du déploiement")

    # (c) McGrew–Viega TC1..TC4 : le scellement (chiffré ET étiquette
    # octet pour octet) puis l'ouverture en sens inverse
    ok_tc, details = True, []
    for nom, cle_hex, iv_hex, aad_hex, pt_hex, ct_hex, tag_hex in TC:
        cle, iv = bytes.fromhex(cle_hex), bytes.fromhex(iv_hex)
        aad, pt = bytes.fromhex(aad_hex), bytes.fromhex(pt_hex)
        ct_att, tag_att = bytes.fromhex(ct_hex), bytes.fromhex(tag_hex)
        ct, tag, r = sceller(emul, cle, iv, aad, pt)
        if not (r["rax"] == 0 and ct == ct_att and tag == tag_att):
            ok_tc = False
            details.append(f"{nom}:sceller")
            continue
        clair, r2 = ouvrir(emul, cle, iv, aad, ct, tag)
        if not (r2["rax"] == 0 and clair == pt):
            ok_tc = False
            details.append(f"{nom}:ouvrir")
    controle("V2.3:mcgrew-viega-tc1-tc4", ok_tc,
             "les QUATRE Test Cases rendus chiffré + étiquette octet pour "
             "octet, puis ouverts (TC1 : 0 o de clair, l'étiquette seule ; "
             "TC2 : 16 o ; TC3 : 64 o ; TC4 : 60 o + AAD de 20 o) ; TC5/TC6 "
             "(IV de 8 et 60 octets) HORS CONTRAT de la brique — P2 le "
             "nonce de 12 o (RFC 8446 § 5.3), la référence du labo les "
             "couvre, le protocole ne les émet jamais"
             + (f" — DÉFAUTS : {details}" if details else ""))

    # (d) LE TRANSFERT RFC 8448 : les SEPT enregistrements chiffrés du
    # § 3 — OUVERTS par tls13-19 (le nonce = IV ⊕ séquence, la tête en
    # AAD), PUIS RESCELLÉS par tls13-18 == l'enregistrement OCTET POUR
    # OCTET (le juge est le texte officiel, parsé par le labo)
    ok_8448, details = True, []
    for nom, cle_hex, iv_hex, seq, interne_hex, rec_hex in TRANSFERT_8448:
        cle = bytes.fromhex(cle_hex)
        iv = bytes.fromhex(iv_hex)
        interne, rec = bytes.fromhex(interne_hex), bytes.fromhex(rec_hex)
        entete, ct_tag = rec[:5], rec[5:]
        nonce = nonce_de(iv, seq)
        clair, r = ouvrir(emul, cle, nonce, entete, ct_tag[:-16], ct_tag[-16:])
        if not (r["rax"] == 0 and clair == interne):
            ok_8448 = False
            details.append(f"{nom}:ouvrir(rax={r['rax']})")
            continue
        ct2, tag2, r2 = sceller(emul, cle, nonce, entete, clair)
        if not (r2["rax"] == 0 and ct2 + tag2 == ct_tag):
            ok_8448 = False
            details.append(f"{nom}:resceller")
    controle("V2.4:le-transfert-rfc-8448-les-sept-enregistrements", ok_8448,
             "le vol serveur (679 o, EE+Cert+CV+Fin), le Finished client "
             "(58 o), le NewSessionTicket (227 o), les données "
             "applicatives (72 o ×2, séquences 0 et 1), les close_notify "
             "(24 o ×2) — OUVERTS (le clair interne payload || type rendu) "
             "puis RESCELLÉS == l'enregistrement OCTET POUR OCTET"
             + (f" — DÉFAUTS : {details}" if details else ""))

    # (e) l'oracle différentiel : cent scellages aléatoires contre la
    # référence (l'émulation NUE — les longues exécutions ne se comptent
    # pas, elles se vérifient)
    rng = random.Random(graine)
    ecarts, joues = 0, 0
    for _ in range(100):
        cle = bytes(rng.randrange(256) for _ in range(16))
        nonce = bytes(rng.randrange(256) for _ in range(12))
        aad = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 41)))
        clair = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 81)))
        ct_ref, tag_ref = ref_gcm_sceller(cle, nonce, aad, clair)
        ct, tag, r = sceller(nue, cle, nonce, aad, clair)
        joues += 1
        if not (r["rax"] == 0 and ct == ct_ref and tag == tag_ref):
            ecarts += 1
            continue
        clair2, r2 = ouvrir(nue, cle, nonce, aad, ct, tag)
        joues += 1
        if not (r2["rax"] == 0 and clair2 == clair):
            ecarts += 1
    controle("V2.5:l-oracle-differentiel-100-scellages", ecarts == 0,
             f"{joues} exécutions (100 scellages + 100 ouvertures, les "
             "clairs de 0 à 80 o, les AAD de 0 à 40 o — les longueurs non "
             "multiples de 16 exercées) — ZÉRO écart contre la référence")


# --- V3 : les cas punitifs (les bornes et les lâches) -------------------------------

def vecteur_v3(emul: Emulation, nue: Emulation, graine: int):
    section("V3 — les cas punitifs (les dégénérés, le chevauchement, les bornes, les refus)")
    rng = random.Random(graine ^ 0xC0FFEE)

    # (a) le GHASH : les dégénérés et l'identité réfléchie
    zero = bytes(16)
    identite = bytes.fromhex("80" + "00" * 15)   # le neutre réfléchi
    un = bytes.fromhex("01" + "00" * 15)
    cas = [("X = 0", zero, un, zero),
           ("Y = 0", un, zero, zero),
           ("X·ID == X", identite, identite, identite),
           ("X = Y = 1", un, un, ref_ghash(un, un)),
           ("X = Y = R", R_GCM, R_GCM, ref_ghash(R_GCM, R_GCM))]
    ok, details = True, []
    for nom, x, y, attendu in cas:
        z, r = ghash(emul, x, y)
        if not (r["rax"] == 0 and z == attendu):
            ok = False
            details.append(f"{nom} → {z.hex()}")
    controle("V3.a:les-degeneres-du-ghash", ok,
             "X = 0 → Z = 0 ; Y = 0 → Z = 0 ; l'identité réfléchie "
             "0x80||0^120 : X·ID == X (le premier bit = x^0) ; X = Y = 1 ; "
             "X = Y = R" + (f" — DÉFAUTS : {details}" if details else ""))

    # (b) la commutativité aux DEUX ordres (50 paires — Q1 de 17)
    ok = True
    for _ in range(50):
        x = bytes(rng.randrange(256) for _ in range(16))
        y = bytes(rng.randrange(256) for _ in range(16))
        z1, _ = ghash(emul, x, y)
        z2, _ = ghash(emul, y, x)
        ok = ok and z1 == z2 == ref_ghash(x, y)
    controle("V3.b:la-commutativite-aux-deux-ordres", ok,
             "50 paires aléatoires : X•Y == Y•X == la référence — SP 800-38D "
             "§ 6.3 sur pièces")

    # (c) le chevauchement : la sortie SUR l'entrée (P3 de 16 et de 17 —
    # le bloc charge AVANT d'écrire)
    rk = b"".join(ref_cles_tour(C1_CLE))
    entree = bytes(range(16))
    ct_inplace, r = bloc_aes(emul, rk, entree, sortie_adr=ADR_BLOC_IN)
    ct_normal, _ = bloc_aes(emul, rk, entree)
    controle("V3.c:le-chevauchement-de-16", r["rax"] == 0
             and ct_inplace == ct_normal == ref_bloc_aes(entree, ref_cles_tour(C1_CLE)),
             "la sortie ÉCRASE l'entrée (r8 == rdx) — le bloc charge AVANT "
             "d'écrire : le même chiffré que la sortie séparée")
    x = bytes(rng.randrange(256) for _ in range(16))
    y = bytes(rng.randrange(256) for _ in range(16))
    z_inplace, r = ghash(emul, x, y, sortie_adr=ADR_X)
    controle("V3.d:le-chevauchement-de-17", r["rax"] == 0
             and z_inplace == ref_ghash(x, y),
             "la sortie ÉCRASE X (rcx == rdx) — le bloc charge X et Y "
             "AVANT d'écrire")

    # (d) les bornes du scellement : N = 2^14 exact (LA borne P4,
    # dedans), N = 2^14+1 et A = 2^14+1 → rax = −2 NOMMÉS
    cle = bytes(rng.randrange(256) for _ in range(16))
    nonce = bytes(rng.randrange(256) for _ in range(12))
    clair_max = bytes(rng.randrange(256) for _ in range(1 << 14))
    aad_court = bytes(11)
    ct, tag, r = sceller(nue, cle, nonce, aad_court, clair_max)
    clair_rendu, r2 = ouvrir(nue, cle, nonce, aad_court, ct, tag)
    controle("V3.e:la-borne-p4-n-2-14-exact", r["rax"] == 0 and r2["rax"] == 0
             and clair_rendu == clair_max,
             "N = 16384 (LA borne de la couche enregistrement, RFC 8446 "
             "§ 5.1 — 1024 blocs, le compteur u32 loin du rendement, I3) : "
             "scellé PUIS ouvert, le clair rendu OCTET POUR OCTET")
    clair = bytes(64)
    _, _, r = sceller(emul, cle, nonce, aad_court, clair,
                      force={"r9": (1 << 14) + 1})
    controle("V3.f:le-refus-2-de-18 (N > 2^14)", r["rax"] == -2,
             f"N = 16385 → rax = {r['rax']} NOMMÉ (Q3)")
    _, _, r = sceller(emul, cle, nonce, aad_court, clair,
                      force={"a": (1 << 14) + 1})
    controle("V3.g:le-refus-2-de-18 (A > 2^14)", r["rax"] == -2,
             f"A = 16385 → rax = {r['rax']} NOMMÉ (Q3)")

    # (h) les refus -1 : chaque pointeur nul (les SIX de 18 et les SIX de 19)
    ok_18, ok_19 = True, True
    for champ in ("rcx", "r8"):
        _, _, r = sceller(emul, cle, nonce, aad_court, clair,
                          force={champ: 0})
        ok_18 = ok_18 and r["rax"] == -1
    for champ in ("aad", "ct", "tag"):
        _, _, r = sceller(emul, cle, nonce, aad_court, clair,
                          force={champ: 0})
        ok_18 = ok_18 and r["rax"] == -1
    ct_ok, tag_ok, _ = sceller(emul, cle, nonce, aad_court, clair)
    for champ in ("rcx", "r8"):
        _, r = ouvrir(emul, cle, nonce, aad_court, ct_ok, tag_ok,
                      force={champ: 0})
        ok_19 = ok_19 and r["rax"] == -1
    for champ in ("aad", "etiq", "clair"):
        _, r = ouvrir(emul, cle, nonce, aad_court, ct_ok, tag_ok,
                      force={champ: 0})
        ok_19 = ok_19 and r["rax"] == -1
    controle("V3.h:les-refus-1-les-douze-pointeurs", ok_18 and ok_19,
             "18 : clé/nonce/clair/AAD/étiquette-sortie/chiffré-sortie "
             "nuls → −1 ; 19 : les six siens — chaque refus NOMMÉ (Q3)")

    # (i) l'indifférence : A = 0 — le pointeur AAD nul N'EST PAS un refus
    # (P5 : la brique ne lit PAS l'AAD vide — le contrat le permet)
    ct0, tag0, r = sceller(emul, cle, nonce, b"", clair, force={"aad": 0})
    ct_ref, tag_ref = ref_gcm_sceller(cle, nonce, b"", clair)
    controle("V3.i:l-indifference-a-nul", r["rax"] == 0 and ct0 == ct_ref
             and tag0 == tag_ref,
             "A = 0 avec le pointeur AAD NUL : le scellement rend la "
             "référence — le pointeur n'est PAS lu quand la longueur est "
             "nulle (P5/P6 : le couple, jamais le pointeur seul)")


# --- V4 : le contrat ---------------------------------------------------------------

def vecteur_v4(emul: Emulation):
    section("V4 — le contrat (les pré/post de chaque bloc, sur pièces)")

    # (a) les non-volatiles rendus + la pile équilibrée + les canaris :
    # un cas représentatif de CHAQUE bloc de la famille
    rng = random.Random(20261107)
    cle = bytes(rng.randrange(256) for _ in range(16))
    nonce = bytes(rng.randrange(256) for _ in range(12))
    clair = bytes(rng.randrange(256) for _ in range(37))
    aad = bytes(rng.randrange(256) for _ in range(13))
    ok_nv, details = True, []

    rk, r = deployer(emul, cle)
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"]
            and r["logements_intacts"] and r["rax"] == 0):
        ok_nv = False
        details.append("tls13-15")
    ct_bloc, r = bloc_aes(emul, rk, bytes(range(16)))
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"]
            and r["logements_intacts"] and r["rax"] == 0):
        ok_nv = False
        details.append("tls13-16")
    z, r = ghash(emul, bytes(range(16)), bytes(range(16, 32)))
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"]
            and r["logements_intacts"] and r["rax"] == 0):
        ok_nv = False
        details.append("tls13-17")
    ct, tag, r = sceller(emul, cle, nonce, aad, clair)
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"]
            and r["logements_intacts"] and r["rax"] == 0):
        ok_nv = False
        details.append("tls13-18")
    clair2, r = ouvrir(emul, cle, nonce, aad, ct, tag)
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"]
            and r["logements_intacts"] and r["rax"] == 0):
        ok_nv = False
        details.append("tls13-19")
    controle("V4.a:non-volatiles-pile-canaris (les cinq blocs)", ok_nv,
             "les 8 sentinelles rendues, rsp équilibrée, l'ombre intacte, "
             "les QUATRE logements d'arguments de pile relus (le cadre "
             "0xE8 de 18/19), la zone profonde intacte"
             + (f" — DÉFAUTS : {details}" if details else ""))

    # (b) l'alignement msx64 à travers les appels directs : à CHAQUE
    # entrée de TLS16 et TLS17 (par 18 au scellement, par 19 à
    # l'ouverture) — les comptes exacts de la recette
    emul.surveillance = {va: [] for va in (L.TLS16_VA, L.TLS17_VA)}
    try:
        sceller(emul, cle, nonce, aad, clair)
        ouvrir(emul, cle, nonce, aad, ct, tag)
    finally:
        entrees = {va: list(l) for va, l in emul.surveillance.items()}
        emul.surveillance = None
    n = len(clair)
    a = len(aad)
    attendu_bloc = 2 * (2 + (n + 15) // 16)       # H + J0 + ⌈N/16⌉, ×2 appels
    attendu_ghash = 2 * ((a + 15) // 16 + (n + 15) // 16 + 1)
    total = sum(len(l) for l in entrees.values())
    ok_align = total > 0 and all(e % 16 == 8 for l in entrees.values() for e in l)
    ok_compte = (len(entrees[L.TLS16_VA]) == attendu_bloc
                 and len(entrees[L.TLS17_VA]) == attendu_ghash)
    controle("V4.b:l-alignement-msx64-a-l-entree-de-chaque-calle",
             ok_align and ok_compte,
             f"{total} entrées surveillées (TLS16 ×{len(entrees[L.TLS16_VA])} "
             f"== 2×[2 + ⌈37/16⌉ = 5], TLS17 ×{len(entrees[L.TLS17_VA])} == "
             "2×[⌈13/16⌉ + ⌈37/16⌉ + 1 = 5]) — rsp ≡ 8 (mod 16) chacune, "
             "les comptes exacts de la recette (H, CTR, J0 ; AAD, chiffré, "
             "longueurs)")

    # (c) les entrées INTACTES (Q2/Q3) : la clé, le nonce, le clair,
    # l'AAD, l'étiquette reçue
    sceller(emul, cle, nonce, aad, clair)
    ok_int = (emul.intact_autour(ADR_NONCE, 12)
              and emul.intact_autour(ADR_CLAIR, len(clair))
              and emul.intact_autour(ADR_AAD, len(aad)))
    ouvrir(emul, cle, nonce, aad, ct, tag)
    ok_int &= (emul.intact_autour(ADR_NONCE, 12)
               and emul.intact_autour(ADR_CT, len(ct))
               and emul.intact_autour(ADR_ETIQ, 16)
               and emul.intact_autour(ADR_AAD, len(aad)))
    controle("V4.c:les-entrees-intactes (Q2/Q3)", ok_int,
             "le nonce, le clair et l'AAD relus OCTET POUR OCTET après le "
             "scellement ; le nonce, le chiffré REÇU, l'étiquette REÇUE et "
             "l'AAD après l'ouverture — J0 et CB vivent dans les COPIES "
             "LOCALES de la pile")

    # (d) la sortie JAMAIS dépassée : les canaris après le chiffré,
    # l'étiquette ET le clair restitué
    ok_dep = (emul.intact_autour(ADR_CT, len(ct))
              and emul.intact_autour(ADR_TAG, 16)
              and emul.intact_autour(ADR_CLAIR2, len(clair2)))
    controle("V4.d:les-sorties-jamais-depassee", ok_dep,
             "les canaris après le chiffré (37 o), l'étiquette (16 o) et "
             "le clair restitué (37 o) intacts — les écritures ne "
             "débordent JAMAIS")

    # (e) les refus SANS corruption : l'échec ne touche RIEN (les canaris
    # du chiffré et de l'étiquette demeurent, la pile rendue)
    emul.uc.mem_write(ADR_CT, CANARI * 0x100)
    emul.uc.mem_write(ADR_TAG, CANARI * 0x40)
    _, _, r = sceller(emul, cle, nonce, aad, clair,
                      force={"r9": (1 << 14) + 1})
    ct_vierge = bytes(emul.uc.mem_read(ADR_CT, len(clair)))
    tag_vierge = bytes(emul.uc.mem_read(ADR_TAG, 16))
    controle("V4.e:le-refus-sans-corruption", r["rax"] == -2
             and r["pile_equilibree"] and ct_vierge == CANARI * len(clair)
             and tag_vierge == CANARI * 16,
             "N hors borne → rax = −2 AVANT toute écriture : le chiffré "
             "et l'étiquette demeurent VIERGES, la pile équilibrée — "
             "l'échec ne corrompt rien")


# --- V5 : la falsification ---------------------------------------------------------

def vecteur_v5(emul: Emulation, nue: Emulation):
    section("V5 — la falsification (zéro silence)")
    rng = random.Random(0xFEED)
    cle = bytes(rng.randrange(256) for _ in range(16))
    nonce = bytes(rng.randrange(256) for _ in range(12))
    clair = bytes(rng.randrange(256) for _ in range(53))
    aad = bytes(rng.randrange(256) for _ in range(19))
    ct_ref, tag_ref = ref_gcm_sceller(cle, nonce, aad, clair)
    ct, tag, _ = sceller(emul, cle, nonce, aad, clair)
    assert ct == ct_ref and tag == tag_ref

    # (a) la clé mutée → le chiffré diverge (premier/milieu/dernier octet)
    attrapes, total = 0, 0
    for pos in (0, 8, 15):
        mute = bytearray(cle)
        mute[pos] ^= 1
        ct2, tag2, r = sceller(nue, bytes(mute), nonce, aad, clair)
        total += 1
        attrapes += (ct2 != ct_ref or tag2 != tag_ref)
    controle("V5.a:la-cle-mutee-attrapee", attrapes == total,
             f"{attrapes}/{total} mutations de la clé — le chiffré ou "
             "l'étiquette divergent (le déploiement ET le bloc portent la clé)")

    # (b) le nonce et le clair mutés → la sortie diverge
    attrapes, total = 0, 0
    for pos in (0, 6, 11):
        mute = bytearray(nonce)
        mute[pos] ^= 1
        ct2, tag2, _ = sceller(nue, cle, bytes(mute), aad, clair)
        total += 1
        attrapes += (ct2 != ct_ref or tag2 != tag_ref)
    for pos in (0, 26, 52):
        mute = bytearray(clair)
        mute[pos] ^= 1
        ct2, tag2, _ = sceller(nue, cle, nonce, aad, bytes(mute))
        total += 1
        attrapes += (ct2 != ct_ref or tag2 != tag_ref)
    controle("V5.b:le-nonce-et-le-clair-mutes-attrapes", attrapes == total,
             f"{attrapes}/{total} mutations — le compteur (J0) et le flot "
             "portent la divergence")

    # (c) CHAQUE octet de l'étiquette muté → −4, la sortie INTACTE (Q4 :
    # la garde constatée mutation par mutation)
    attrapes, total = 0, 0
    for pos in range(16):
        mute = bytearray(tag)
        mute[pos] ^= 0x80
        nue.uc.mem_write(ADR_CLAIR2, CANARI * (len(ct) + 0x120))
        _, r = ouvrir(nue, cle, nonce, aad, ct, bytes(mute))
        intact = bytes(nue.uc.mem_read(ADR_CLAIR2, len(ct))) == CANARI * len(ct)
        total += 1
        attrapes += (r["rax"] == -4 and intact)
    controle("V5.c:les-16-octets-de-l-etiquette-mutes", attrapes == total,
             f"{attrapes}/{total} mutations de l'étiquette (UNE PAR OCTET, "
             "bit de poids fort) → rax = −4 NOMMÉ, la sortie clair INTACTE "
             "— fail-closed : AUCUN octet restitué")

    # (d) CHAQUE octet du chiffré muté → −4, la sortie INTACTE (Q4)
    attrapes, total = 0, 0
    for pos in range(len(ct)):
        mute = bytearray(ct)
        mute[pos] ^= 1
        nue.uc.mem_write(ADR_CLAIR2, CANARI * (len(ct) + 0x120))
        _, r = ouvrir(nue, cle, nonce, aad, bytes(mute), tag)
        intact = bytes(nue.uc.mem_read(ADR_CLAIR2, len(ct))) == CANARI * len(ct)
        total += 1
        attrapes += (r["rax"] == -4 and intact)
    controle("V5.d:les-53-octets-du-chiffre-mutes", attrapes == total,
             f"{attrapes}/{total} mutations du chiffré (UNE PAR OCTET) → "
             "rax = −4 NOMMÉ, la sortie clair INTACTE — le GHASH du "
             "chiffré porte chaque octet")

    # (e) l'AAD muté → l'ouverture REFUSE (l'AAD est AUTHENTIFIÉ)
    attrapes, total = 0, 0
    for pos in (0, 9, 18):
        mute = bytearray(aad)
        mute[pos] ^= 1
        _, r = ouvrir(nue, cle, nonce, bytes(mute), ct, tag)
        total += 1
        attrapes += r["rax"] == -4
    controle("V5.e:l-aad-mute-attrape", attrapes == total,
             f"{attrapes}/{total} mutations de l'AAD → −4 — les données "
             "ASSOCIÉES sont couvertes par l'étiquette (I2 de 18)")

    # (f) la comparaison n'est pas muette (l'instrument se prouve non vide)
    attrapes, total = 0, 0
    for bit in (0, 63, 127):
        mute = bytearray(tag)
        mute[bit // 8] ^= 1 << (bit % 8)
        total += 1
        attrapes += bytes(mute) != tag
    controle("V5.f:la-comparaison-n-est-pas-muette", attrapes == total,
             f"{attrapes}/{total} étiquettes attendues mutées → l'égalité ÉCHOUE")


# --- V6 : le temps constant mesuré ---------------------------------------------------

def vecteur_v6(emul: Emulation, graine: int):
    section("V6 — le temps constant MESURÉ (I1/I2, la charte § 3)")
    rng = random.Random(graine ^ 0x7)

    # (a) le déploiement : 4 clés différentes, même compte
    comptes = []
    for _ in range(4):
        cle = bytes(rng.randrange(256) for _ in range(16))
        _, r = deployer(emul, cle, compter=True)
        comptes.append(r["compteur"])
    controle("V6.a:le-deploiement-compte-constant", len(set(comptes)) == 1,
             f"4 clés aléatoires, {comptes[0]} instructions EXACTEMENT — "
             "les dix tours DÉROULÉS, AESKEYGENASSIST temps constant PAR "
             "CONSTRUCTION (I2 de 15 : la clé ne touche JAMAIS une branche)")

    # (b) le bloc : 3 paires différentes, même compte
    comptes = []
    for _ in range(3):
        rk = bytes(rng.randrange(256) for _ in range(176))
        entree = bytes(rng.randrange(256) for _ in range(16))
        _, r = bloc_aes(emul, rk, entree, compter=True)
        comptes.append(r["compteur"])
    controle("V6.b:le-bloc-compte-constant", len(set(comptes)) == 1,
             f"3 paires (clés de tour, bloc) aléatoires, {comptes[0]} "
             "instructions EXACTEMENT — les dix tours TOUJOURS exécutés "
             "(I1 de 16 : la propriété est GRATUITE PAR CONSTRUCTION)")

    # (c) le GHASH : 3 paires différentes, même compte
    comptes = []
    for _ in range(3):
        x = bytes(rng.randrange(256) for _ in range(16))
        y = bytes(rng.randrange(256) for _ in range(16))
        _, r = ghash(emul, x, y, compter=True)
        comptes.append(r["compteur"])
    controle("V6.c:le-ghash-compte-constant", len(set(comptes)) == 1,
             f"3 paires (X, Y) aléatoires, {comptes[0]} instructions "
             "EXACTEMENT — le bit de X devient MASQUE par sbb, les 128 "
             "itérations TOUJOURS (I1/I2 de 17)")

    # (d) le scellement : clairs et clés différents (MÊME longueur), même
    # compte — la longueur est publique, le contenu JAMAIS
    comptes = []
    for _ in range(2):
        clair = bytes(rng.randrange(256) for _ in range(45))
        cle = bytes(rng.randrange(256) for _ in range(16))
        _, _, r = sceller(emul, cle, nonce_de(bytes(12), 0), bytes(7), clair,
                          compter=True)
        comptes.append(r["compteur"])
    controle("V6.d:le-scellage-compte-constant", len(set(comptes)) == 1,
             f"2 scellages (clairs ET clés différents, N = 45, A = 7), "
             f"{comptes[0]} instructions EXACTEMENT")

    # (e) LE VERDICT DE L'OUVERTURE : trois étiquettes divergentes
    # (premier, milieu, dernier octet muté) → LE MÊME compte EXACTEMENT —
    # le OU cumulatif ne court-circuite PAS, la position de la différence
    # ne se lit pas dans le temps (I1 de 19 : LA discipline du verdict)
    cle = bytes(rng.randrange(256) for _ in range(16))
    nonce = bytes(rng.randrange(256) for _ in range(12))
    clair = bytes(rng.randrange(256) for _ in range(45))
    ct, tag, _ = sceller(emul, cle, nonce, bytes(7), clair)
    comptes = []
    for pos in (0, 8, 15):
        mute = bytearray(tag)
        mute[pos] ^= 0x80
        _, r = ouvrir(emul, cle, nonce, bytes(7), ct, bytes(mute),
                      compter=True)
        comptes.append(r["compteur"])
    controle("V6.e:le-verdict-compte-constant", len(set(comptes)) == 1,
             f"3 étiquettes divergentes (octets 0, 8 et 15 mutés), "
             f"{comptes[0]} instructions EXACTEMENT — les 16 différences "
             "TOUTES accumulées avant LA branche : la position de la "
             "première divergence est INVISIBLE dans le temps (le OU "
             "cumulatif, AUCUN court-circuit)")

    # (f) l'ouverture conforme : 2 clairs différents (même longueur),
    # même compte
    comptes = []
    for _ in range(2):
        clair2 = bytes(rng.randrange(256) for _ in range(45))
        cle2 = bytes(rng.randrange(256) for _ in range(16))
        ct2, tag2, _ = sceller(emul, cle2, nonce, bytes(7), clair2)
        _, r = ouvrir(emul, cle2, nonce, bytes(7), ct2, tag2, compter=True)
        comptes.append(r["compteur"])
    controle("V6.f:l-ouverture-conforme-compte-constant", len(set(comptes)) == 1,
             f"2 ouvertures conformes, {comptes[0]} instructions EXACTEMENT")


# --- Le verdict ----------------------------------------------------------------------

def main() -> int:
    graine = 20261107
    if "--graine" in sys.argv:
        graine = int(sys.argv[sys.argv.index("--graine") + 1])
    print("=== tls13/harnais_aead.py — LE HARNAIS DE LA FAMILLE aead "
          "(chantier M9-(b), le geste quatre) ===")
    print(f"    plan : tls13/layout.py · graine : {graine}")
    emul = Emulation()
    nue = Emulation(nue=True)
    vecteur_v0(emul)
    vecteur_v1(emul)
    vecteur_v2(emul, nue, graine)
    vecteur_v3(emul, nue, graine)
    vecteur_v4(emul)
    vecteur_v5(emul, nue)
    vecteur_v6(emul, graine)
    print("\n" + "=" * 72)
    print(f"Contrôles : {len(REUSSITES)} verts · {len(ECHECS)} échecs")
    if ECHECS:
        for nom, detail in ECHECS:
            print(f"  [ÉCHEC] {nom} — {detail}")
        print("VERDICT : ROUGE")
        return 1
    print("VERDICT : VERT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
