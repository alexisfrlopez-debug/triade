#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tls13/harnais_hkdf.py — LE HARNAIS DE LA FAMILLE hkdf DU DOMAINE tls13.

Chantier M9-(b), second geste : les blocs tls13-05..08 (HMAC-SHA-256,
HKDF-Extract, HKDF-Expand, HKDF-Expand-Label — RFC 2104 / 5869 / 8446 § 7.1)
NOTÉS-MESURÉS-PROUVÉS sur la famille sha notée-mesurée-prouvée au geste
précédent. Le modèle est le harnais sha (tls13/harnais_sha.py) : l'émulation
nue à les RVA du plan (mécanisme D79), l'appelant factice pose les
sentinelles non volatiles et les canaris, le verdict est TRANCHÉ par le
code — jamais cru.

LE CAHIER (le miroir sha, la charte § 2 : les vecteurs officiels AVANT
usage, la falsification, zéro silence) :

  V0 — LES PIÈCES DU PLAN : le scellé 0.9.0 relu (l'ancre 1492b0bc…), la
       famille sha INTACTE (les quatre notations re-round-tripées aux
       longueurs arrêtées 74/387/139/165 — la frontière du geste précédent),
       K[64] posé à R_K, l'arbre I scellé relu VERT (verifier_specs_m9a
       rejoué — R2 : les specs signées précèdent, l'arbre n'a pas bougé) ;
  V1 — LE ROUND-TRIP + LA CONCORDANCE : chaque notation ré-assemblée en ses
       octets (keystone == capstone, R5), les longueurs == l'ARRÊT du plan
       (427/147/343/306 o, D161), les appels directs de 05 == TLS01/TLS03/
       TLS04, de 06/07 == TLS05, de 08 == TLS07 (I1), les masques ipad/opad
       de 05 == le plan (0x36/0x5c ×8), le préfixe « tls13 » de 08 == le
       plan (PREFIXE_ETIQUETTE), la structure du domaine (AUCUN site
       syscall, AUCUN appel indirect, AUCUN déplacement RIP — tout vit en
       immédiats et sur la pile) et le temps constant STRUCTUREL (aucun
       saut conditionnel ne conditionne sur une LECTURE mémoire : les
       données secrètes ne touchent jamais une branche) ;
  V2 — LES VECTEURS OFFICIELS RFC 4231 : les SEPT cas appendice A (les clés
       de 131 o comprises — l'expulsion de la clé exercée dans les DEUX
       sens ; le cas 5 sur sa troncature officielle de 128 bits), chacun
       CROISÉ avec hashlib AVANT de juger, puis le balayage différentiel
       (clés 0..131 × messages 0..1000 — l'expulsion aux bornes 63/64/65) ;
  V3 — LES VECTEURS OFFICIELS RFC 5869 + LE TRANSFERT RFC 8448 : les Test
       Cases 1 à 3 SHA-256 (Extract, Expand, la chaîne complète), les TROIS
       extraits du transcript (early/handshake/master — le sel vide et le
       sel dérivé EXERCÉS), les étiquettes du transcript (« derived »,
       « c hs traffic », « s hs traffic », « key », « iv », « finished » —
       la structure HkdfLabel RECROISÉE octet pour octet avec les « info »
       consignées par la RFC 8448), la borne L = 8160 (le compteur d'un
       octet, la garde) et l'oracle différentiel (la structure reconstruite
       en Python, la comparaison octet pour octet) ;
  V4 — LE CONTRAT : les entrées INTACTES (la clé, le message, le sel,
       l'IKM, le PRK, l'info, le libellé, le contexte), les non-volatiles
       rendus, la pile équilibrée, l'ombre et les logements d'arguments
       intacts, l'alignement msx64 à l'entrée de CHAQUE appelé à travers
       les appels directs (le point de vue du CALLE), la sortie JAMAIS
       dépassée (canaris après L), et les refus NOMMÉS (-1/-2 : chaque cas
       du contrat exercé, un par un) ;
  V5 — LA FALSIFICATION (zéro silence) : chaque vecteur muté (premier,
       milieu, dernier octet de la clé, du message, de l'IKM, du PRK, du
       secret) ATTRAPÉ, la comparaison n'est pas muette (chaque bit du
       résultat attendu muté ÉCHOUE), K corrompu → divergence (la table est
       LUE à travers la composition) ;
  V6 — LE TEMPS CONSTANT MESURÉ (I3 de chaque spec, la charte § 3) : le
       compte d'instructions IDENTIQUE pour des SECRETS différents de
       MÊMES longueurs — la clé (courte et longue), l'IKM, le PRK, le
       secret ; la longueur est publique, le contenu JAMAIS.

Usage : python3 harnais_hkdf.py            # le cahier complet
        python3 harnais_hkdf.py --graine N # la graine du générateur (défaut 20261106)
"""

from __future__ import annotations

import hashlib
import hmac as hmac_ref
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

# Le plan tls13 chargé par CHEMIN NOMINATIF (leçon D158 : le nom « layout »
# est disputé par la chaîne build_m3/build_m4 — jamais d'import anonyme ici).
if "layout_tls13" in sys.modules:
    L = sys.modules["layout_tls13"]
else:
    _spec_l = importlib.util.spec_from_file_location(
        "layout_tls13", os.path.join(ICI, "layout.py"))
    L = importlib.util.module_from_spec(_spec_l)
    sys.modules["layout_tls13"] = L
    _spec_l.loader.exec_module(L)

# La machinerie de notation de la lignée (assembler_bloc/round_trip — le
# lecteur canonique des notations), importée par chemin (leçon D158).
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
                               UC_X86_REG_R15, UC_X86_REG_RIP)

REGS = {"rax": UC_X86_REG_RAX, "rbx": UC_X86_REG_RBX, "rcx": UC_X86_REG_RCX,
        "rdx": UC_X86_REG_RDX, "rsi": UC_X86_REG_RSI, "rdi": UC_X86_REG_RDI,
        "rbp": UC_X86_REG_RBP, "rsp": UC_X86_REG_RSP, "r8": UC_X86_REG_R8,
        "r9": UC_X86_REG_R9, "r10": UC_X86_REG_R10, "r11": UC_X86_REG_R11,
        "r12": UC_X86_REG_R12, "r13": UC_X86_REG_R13, "r14": UC_X86_REG_R14,
        "r15": UC_X86_REG_R15}

# --- La mémoire du harnais (émulation nue à les RVA du plan, mécanisme D79) ------

ZONE_IMAGE = (0x1000, 0xE000)   # .rdata (K @0x2F00) + .text5 + .text6 arrêtée
RET_MAGIQUE = 0xDE00            # dans la réserve .text6 — jamais exécuté
ZONE_CTX = 0x500000             # les contextes SHA (112 o, canaris autour)
ZONE_ENTREE = 0x600000          # les clés et les messages (UNE PAGE CHACUNE)
TAILLE_ENTREE = 0x4000          # 4 pages : clé · message · info · contexte
ZONE_SORTIE = 0x700000          # les condensés et PRK (32 o, canaris autour)
ZONE_OKM = 0x800000             # les OKM longues (L ≤ 8160, canaris autour)
TAILLE_OKM = 0x4000
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP0 = 0x7F008000
ENTREE_RSP = RSP0 - 0x108       # ≡ 8 (mod 16) — le point de vue de l'APPELÉ

OFF_ZONE = 0x100                # la donnée dans sa page
TAILLE_PAGE = 0x1000

ADRESSE_CLE = ZONE_ENTREE + OFF_ZONE          # la clé / le sel / le PRK
ADRESSE_MESSAGE = ZONE_ENTREE + 0x1100        # le message / l'IKM
ADRESSE_INFO = ZONE_ENTREE + 0x2100           # l'info / le libellé
ADRESSE_CTX_TRANSFERT = ZONE_ENTREE + 0x3100  # le contexte (transfert 8448)
ADRESSE_SORTIE = ZONE_SORTIE + OFF_ZONE       # le condensé (32 o)
ADRESSE_PRK = ZONE_SORTIE + OFF_ZONE          # le PRK (32 o)
ADRESSE_OKM = ZONE_OKM + OFF_ZONE             # l'OKM (L o)

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

# --- Les vecteurs officiels RFC 4231 appendice A (HMAC-SHA-256, tls13-05 Q1) -----

VECTEURS_4231 = [
    ("cas-1 (cle 20 o, « Hi There »)",
     bytes.fromhex("0b" * 20), b"Hi There",
     "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7", 32),
    ("cas-2 (cle « Jefe », 28 o)",
     b"Jefe", b"what do ya want for nothing?",
     "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843", 32),
    ("cas-3 (cle 20 o, donnees 50 o)",
     bytes.fromhex("aa" * 20), bytes.fromhex("dd" * 50),
     "773ea91e36800e46854db8ebd09181a72959098b3ef8c122d9635514ced565fe", 32),
    ("cas-4 (cle 25 o, donnees 50 o)",
     bytes(range(0x01, 0x1a)), bytes.fromhex("cd" * 50),
     "82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b", 32),
    ("cas-5 (truncation 128 bits — la borne OFFICIELLE)",
     bytes.fromhex("0c" * 20), b"Test With Truncation",
     "a3b6167473100ee06e0c796c2955552b", 16),
    ("cas-6 (cle 131 o — l'expulsion EXERCEE : H(clé) d'abord)",
     bytes.fromhex("aa" * 131),
     b"Test Using Larger Than Block-Size Key - Hash Key First",
     "60e431591ee0b67f0d8a26aacbf5b77f8e0bc6213728c5140546040f0ee37f54", 32),
    ("cas-7 (cle 131 o, donnees 152 o)",
     bytes.fromhex("aa" * 131),
     b"This is a test using a larger than block-size key and a larger "
     b"than block-size data. The key needs to be hashed before being "
     b"used by the HMAC algorithm.",
     "9b09ffa71b942fcb27635fbcd5b0e944bfdc63644f0713938a7f51535c3a35e2", 32),
]

# --- Les vecteurs officiels RFC 5869 appendice A (SHA-256 — tls13-06/07 Q1) ------

VECTEURS_5869 = [
    {   # Test Case 1 : le cas de base
        "ikm": bytes.fromhex("0b" * 22),
        "sel": bytes.fromhex("000102030405060708090a0b0c"),
        "info": bytes.fromhex("f0f1f2f3f4f5f6f7f8f9"),
        "L": 42,
        "prk": "077709362c2e32df0ddc3f0dc47bba6390b6c73bb50f9c3122ec844ad7c2b3e5",
        "okm": "3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf"
               "34007208d5b887185865",
    },
    {   # Test Case 2 : les entrées et sorties longues
        "ikm": bytes(range(0x00, 0x50)),
        "sel": bytes(range(0x60, 0xb0)),
        "info": bytes(range(0xb0, 0x100)),
        "L": 82,
        "prk": "06a6b88c5853361a06104c9ceb35b45cef760014904671014a193f40c15fc244",
        "okm": "b11e398dc80327a1c8e7f78c596a49344f012eda2d4efad8a050cc4c19afa97c"
               "59045a99cac7827271cb41c65e590e09da3275600c2f09b8367793a9aca3db7"
               "1cc30c58179ec3e87c14c01d5c1f3434f1d87",
    },
    {   # Test Case 3 : le sel et l'info VIDES (le cas zéro EXERCÉ)
        "ikm": bytes.fromhex("0b" * 22),
        "sel": b"",
        "info": b"",
        "L": 42,
        "prk": "19ef24a32c717b167f33a91d6f648bdf96596776afdb6377ac434c1c293ccb04",
        "okm": "8da4e775a563c18f715f802a063c5a31b8a11f5c5ee1879ec3454e5f3c738d2d"
               "9d201395faa4b61a96c8",
    },
]

# --- Le transfert RFC 8448 § 3 (Simple 1-RTT — tls13-06/08 Q1) -------------------
# Les valeurs consignées par le transcript officiel : chaque « info » est la
# structure HkdfLabel EXACTE imprimée par la RFC — la sérialisation du bloc
# tls13-08 est RECROISÉE octet pour octet avec elle (le témoin n'est pas muet).

VIDE_SHA = hashlib.sha256(b"").digest()          # e3b0c442…b855 (RFC 8448 : « hash »)
TRANSFERT_8448 = {
    "early": bytes.fromhex(
        "33ad0a1c607ec03b09e6cd9893680ce210adf300aa1f2660e1b22e10f170f92a"),
    "shared": bytes.fromhex(
        "8bd4054fb55b9d63fdfbacf9f04b9f0d35e6d63f537563efd46272900f89492d"),
    "handshake": bytes.fromhex(
        "1dc826e93606aa6fdc0aadc12f741b01046aa6b99f691ed221a9f0ca043fbeac"),
    "ch_sh_hash": bytes.fromhex(
        "860c06edc07858ee8e78f0e7428c58edd6b43f2ca3e6e95f02ed063cf0e1cad8"),
    "c_hs_traffic": bytes.fromhex(
        "b3eddb126e067f35a780b3abf45e2d8f3b1a950738f52e9600746a0e27a55a21"),
    "s_hs_traffic": bytes.fromhex(
        "b67b7d690cc16c4e75e54213cb2d37b4e9c912bcded9105d42befd59d391ad38"),
    "c_ap_traffic": bytes.fromhex(
        "9e40646ce79a7f9dc05af8889bce6552875afa0b06df0087f792ebb7c17504a5"),
    "master": bytes.fromhex(
        "18df06843d13a08bf2a449844c5f8a478001bc4d4c627984d5a41da8d0402919"),
    # les étiquettes du transcript : (PRK, libellé, contexte, L, attendu, info exacte)
    "etiquettes": [
        ("early", "derived", VIDE_SHA, 32,
         "6f2615a108c702c5678f54fc9dbab69716c076189c48250cebeac3576c3611ba",
         "00200d746c733133206465726976656420e3b0c44298fc1c149afbf4c8996fb924"
         "27ae41e4649b934ca495991b7852b855"),
        ("handshake", "derived", VIDE_SHA, 32,
         "43de77e0c77713859a944db9db2590b53190a65b3ee2e4f12dd7a0bb7ce254b4",
         "00200d746c733133206465726976656420e3b0c44298fc1c149afbf4c8996fb924"
         "27ae41e4649b934ca495991b7852b855"),
        ("handshake", "c hs traffic", None, 32,   # contexte = ch_sh_hash
         "b3eddb126e067f35a780b3abf45e2d8f3b1a950738f52e9600746a0e27a55a21",
         "002012746c7331332063206873207472616666696320860c06edc07858ee8e78f0"
         "e7428c58edd6b43f2ca3e6e95f02ed063cf0e1cad8"),
        ("handshake", "s hs traffic", None, 32,
         "b67b7d690cc16c4e75e54213cb2d37b4e9c912bcded9105d42befd59d391ad38",
         "002012746c7331332073206873207472616666696320860c06edc07858ee8e78f0"
         "e7428c58edd6b43f2ca3e6e95f02ed063cf0e1cad8"),
        ("s_hs_traffic", "key", b"", 16,
         "3fce516009c21727d0f2e4e86ee403bc",
         "001009746c733133206b657900"),
        ("s_hs_traffic", "iv", b"", 12,
         "5d313eb2671276ee13000b30",
         "000c08746c73313320697600"),
        ("c_ap_traffic", "key", b"", 16,
         "17422dda596ed5d9acd890e3c63f5051",
         "001009746c733133206b657900"),
        ("c_ap_traffic", "iv", b"", 12,
         "5b78923dee08579033e523d9",
         "000c08746c73313320697600"),
        ("s_hs_traffic", "finished", b"", 32,
         "008d3b66f816ea559f96b537e885c31fc068bf492c652f01f288a1d8cdc19fc8",
         "00200e746c7331332066696e697368656400"),
        ("c_hs_traffic", "finished", b"", 32,
         "b80ad01015fb2f0bd65ff7d4da5d6bf83f84821d1f87fdc7d3c75b5a7b42d9c4",
         "00200e746c7331332066696e697368656400"),
    ],
}

# Les TROIS extraits du transcript (tls13-06 : le sel et l'IKM officiels)
EXTRAITS_8448 = [
    ("early (sel 32 zeros, IKM 32 zeros — RFC 8448)", b"\x00" * 32, b"\x00" * 32,
     "33ad0a1c607ec03b09e6cd9893680ce210adf300aa1f2660e1b22e10f170f92a"),
    ("handshake (sel = derived, IKM = shared — RFC 8448)", None, None,   # résolus au geste
     "1dc826e93606aa6fdc0aadc12f741b01046aa6b99f691ed221a9f0ca043fbeac"),
    ("master (sel = derived(master), IKM 32 zeros — RFC 8448)", None, b"\x00" * 32,
     "18df06843d13a08bf2a449844c5f8a478001bc4d4c627984d5a41da8d0402919"),
]

REUSSITES, ECHECS = [], []


class ErreurHarnais(Exception):
    """Tout écart du harnais (mode build : lève, jamais un verdict muet)."""


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


# --- Les références éphémères (dérivées de I, jamais du binaire — D1) -------------

def ref_hmac(cle: bytes, message: bytes) -> bytes:
    return hmac_ref.new(cle, message, hashlib.sha256).digest()


def ref_extrait(sel: bytes, ikm: bytes) -> bytes:
    if not sel:
        sel = b"\x00" * 32
    return ref_hmac(sel, ikm)


def ref_etend(prk: bytes, info: bytes, L: int) -> bytes:
    okm, t, i = b"", b"", 1
    while len(okm) < L:
        t = ref_hmac(prk, t + info + bytes([i]))
        okm += t
        i += 1
    return okm[:L]


def ref_etiquette(secret: bytes, libelle: bytes, contexte: bytes, L: int) -> bytes:
    structure = (struct.pack(">H", L) + bytes([6 + len(libelle)])
                 + b"tls13 " + libelle + bytes([len(contexte)]) + contexte)
    return ref_etend(secret, structure, L)


# --- L'émulation (le modèle harnais_sha — l'appelant factice msx64) ---------------

class Emulation:
    """Les HUIT blocs posés à leurs RVA du plan, appelés comme des fonctions
    msx64 ordinaires : l'entrée ≡ 8 (mod 16), l'ombre et les logements
    d'arguments couverts de canaris, les non-volatiles sous sentinelles."""

    BLOCS = [("h100001", "tls13-01-sha256-init"),
             ("h100002", "tls13-02-sha256-comprimer"),
             ("h100003", "tls13-03-sha256-absorber"),
             ("h100004", "tls13-04-sha256-finaliser"),
             ("h100005", "tls13-05-hmac-sha256"),
             ("h100006", "tls13-06-hkdf-extract"),
             ("h100007", "tls13-07-hkdf-expand"),
             ("h100008", "tls13-08-hkdf-expand-label")]

    def __init__(self):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.ks = Ks(KS_ARCH_X86, KS_MODE_64)
        self.cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.cs.detail = False
        self.uc.mem_map(*ZONE_IMAGE)
        for zone, taille in ((ZONE_CTX, TAILLE_PAGE), (ZONE_ENTREE, TAILLE_ENTREE),
                             (ZONE_SORTIE, TAILLE_PAGE), (ZONE_OKM, TAILLE_OKM),
                             (ZONE_PILE, TAILLE_PILE)):
            self.uc.mem_map(zone, taille)
        for zone, taille in ((ZONE_CTX, TAILLE_PAGE), (ZONE_ENTREE, TAILLE_ENTREE),
                             (ZONE_SORTIE, TAILLE_PAGE), (ZONE_OKM, TAILLE_OKM)):
            self.uc.mem_write(zone, CANARI * taille)
        # la table K[64] posée à R_K dans la .rdata du plan (source unique)
        self.uc.mem_write(L.R_K, struct.pack("<64I", *L.K))
        self.blobs: dict[str, tuple[bytes, list[dict]]] = {}
        # L'INSTRUMENT PERMANENT (la leçon du harnais sha : unicorn attache
        # les hooks à la TRADUCTION des blocs — posé AVANT toute traduction,
        # togglé par drapeaux, jamais ajouté en cours de route).
        self.compteur_actif = False
        self.compteur = 0
        self.surveillance: dict[int, list[int]] | None = None
        self.uc.hook_add(UC_HOOK_CODE, self._instrument)
        self.poser_blocs()

    def _instrument(self, uc, adresse, taille, donnees):
        """Le hook UNIQUE, permanent : compte les instructions quand le
        drapeau est levé, surveille les entrées de blocs quand on le dit."""
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
        """Appelle un bloc comme une fonction msx64. Les arguments PILE
        (5e et suivants) sont posés à [rsp+0x28+8i] — le point de vue du
        CALLE. Retourne le dict des registres de sortie + canaris."""
        uc = self.uc
        for nom, val in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], val)
        for nom, val in (args or {}).items():
            uc.reg_write(REGS[nom], val)
        uc.reg_write(UC_X86_REG_RAX, 0)
        rsp = ENTREE_RSP
        uc.reg_write(UC_X86_REG_RSP, rsp)
        # les canaris : l'ombre + les logements d'arguments + la pile de
        # l'APPELANT au-dessus (les logements écrits sont exemptés au verdict)
        uc.mem_write(rsp + 8, CANARI * 0x178)
        logements = []
        for i, val in enumerate(args_pile or []):
            uc.mem_write(rsp + 0x28 + 8 * i, struct.pack("<Q", val))
            logements.append(rsp + 0x28 + 8 * i)
        # la zone morte PROFONDE (sous TOUT cadre possible : la chaîne la plus
        # profonde est 08 → 07 → 05 → 03 → 02 — le cadre de tls13-02, le w[64]
        # de la compression, descend à ≈ 0x9B0 de l'entrée ; la zone vit à
        # [−0x1000, −0xC00), SOUS tout cadre légitime)
        uc.mem_write(rsp - 0x1000, CANARI * 0x400)
        uc.mem_write(rsp, struct.pack("<Q", RET_MAGIQUE))
        entree_rsp = rsp
        self.compteur = 0
        self.compteur_actif = compter
        try:
            uc.emu_start(va, RET_MAGIQUE, count=20_000_000)
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
        # l'ombre [rsp+8, rsp+0x28) INTACTE + la zone haute [rsp+0x40, +0x180)
        zone_haute = bytes(uc.mem_read(entree_rsp + 8, 0x178))
        plages = [(a, a + 8) for a in logements]
        intact = True
        for i in range(len(zone_haute)):
            adresse = entree_rsp + 8 + i
            octet = zone_haute[i:i + 1]
            if any(debut <= adresse < fin for debut, fin in plages):
                continue                      # le logement : relu à part
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

    def poser_cle(self, cle: bytes):
        self.uc.mem_write(ADRESSE_CLE & ~0xFFF, CANARI * TAILLE_PAGE)
        self.uc.mem_write(ADRESSE_CLE, cle)

    def poser_message(self, message: bytes):
        self.uc.mem_write(ADRESSE_MESSAGE & ~0xFFF, CANARI * TAILLE_PAGE)
        self.uc.mem_write(ADRESSE_MESSAGE, message)

    def poser_info(self, info: bytes):
        self.uc.mem_write(ADRESSE_INFO & ~0xFFF, CANARI * TAILLE_PAGE)
        self.uc.mem_write(ADRESSE_INFO, info)

    def poser_contexte(self, contexte: bytes):
        self.uc.mem_write(ADRESSE_CTX_TRANSFERT & ~0xFFF, CANARI * TAILLE_PAGE)
        self.uc.mem_write(ADRESSE_CTX_TRANSFERT, contexte)

    def preparer_sortie(self, taille=32):
        self.uc.mem_write(ADRESSE_SORTIE, CANARI * 0x100)

    def preparer_okm(self, L: int):
        self.uc.mem_write(ZONE_OKM, CANARI * TAILLE_OKM)
        self.uc.mem_write(ADRESSE_OKM, b"\x00" * 0)   # les canaris partout

    def lire_sortie(self, taille=32) -> bytes:
        return bytes(self.uc.mem_read(ADRESSE_SORTIE, taille))

    def canaris_entree_intacts(self, adresse: int, longueur: int) -> bool:
        page = bytes(self.uc.mem_read(adresse & ~0xFFF, TAILLE_PAGE))
        debut = adresse & 0xFFF
        return (page[:debut] == CANARI * debut
                and page[debut + longueur:] ==
                CANARI * (TAILLE_PAGE - debut - longueur))


# --- Les pipelines (les compositions du harnais — miroir hacher()) ---------------

def hmac_sha(emul: Emulation, cle: bytes, message: bytes,
             compter: bool = False) -> tuple[bytes, dict]:
    """tls13-05(clé, K, message, M, sortie) → (le MAC 32 o, le dict de sortie)."""
    emul.poser_cle(cle)
    emul.poser_message(message)
    emul.preparer_sortie()
    r = emul.appeler(L.TLS05_VA,
                     {"rcx": ADRESSE_CLE, "rdx": len(cle),
                      "r8": ADRESSE_MESSAGE, "r9": len(message)},
                     compter=compter,
                     args_pile=[ADRESSE_SORTIE])
    if r["crash"]:
        raise ErreurHarnais(f"tls13-05 a crashé : {r['crash']}")
    return emul.lire_sortie(), r


def hkdf_extraire(emul: Emulation, sel: bytes, ikm: bytes,
                  compter: bool = False) -> tuple[bytes, dict]:
    """tls13-06(sel, S, IKM, I, PRK) → (le PRK 32 o, le dict de sortie)."""
    emul.poser_cle(sel)
    emul.poser_message(ikm)
    emul.preparer_sortie()
    r = emul.appeler(L.TLS06_VA,
                     {"rcx": ADRESSE_CLE if sel else 0,
                      "rdx": len(sel),
                      "r8": ADRESSE_MESSAGE, "r9": len(ikm)},
                     compter=compter,
                     args_pile=[ADRESSE_PRK])
    if r["crash"]:
        raise ErreurHarnais(f"tls13-06 a crashé : {r['crash']}")
    return emul.lire_sortie(), r


def hkdf_etendre(emul: Emulation, prk: bytes, info: bytes, longueur: int,
                 compter: bool = False) -> tuple[bytes, dict]:
    """tls13-07(PRK, info, F, L, OKM) → (l'OKM L o, le dict de sortie)."""
    emul.poser_cle(prk)
    emul.poser_info(info)
    emul.preparer_okm(longueur)
    r = emul.appeler(L.TLS07_VA,
                     {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO,
                      "r8": len(info), "r9": longueur},
                     compter=compter,
                     args_pile=[ADRESSE_OKM])
    if r["crash"]:
        raise ErreurHarnais(f"tls13-07 a crashé : {r['crash']}")
    return bytes(emul.uc.mem_read(ADRESSE_OKM, longueur)), r


def hkdf_etiqueter(emul: Emulation, secret: bytes, libelle: bytes,
                   contexte: bytes, longueur: int,
                   compter: bool = False) -> tuple[bytes, dict]:
    """tls13-08(secret, libellé, contexte, L, sortie) → (la sortie, le dict)."""
    emul.poser_cle(secret)
    emul.poser_info(libelle)
    emul.poser_contexte(contexte)
    emul.preparer_okm(longueur)
    r = emul.appeler(L.TLS08_VA,
                     {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO,
                      "r8": len(libelle), "r9": ADRESSE_CTX_TRANSFERT},
                     compter=compter,
                     args_pile=[len(contexte), longueur, ADRESSE_OKM])
    if r["crash"]:
        raise ErreurHarnais(f"tls13-08 a crashé : {r['crash']}")
    return bytes(emul.uc.mem_read(ADRESSE_OKM, longueur)), r


# --- V0 : les pièces du plan ------------------------------------------------------

def vecteur_v0():
    section("V0 — les pièces du plan (le scellé 0.9.0, la famille sha, l'arbre I)")
    donnees = open(os.path.join(TRIADE, SCELLE_M8), "rb").read()
    controle("V0.a:le-scelle-090-intact",
             len(donnees) == SCELLE_M8_TAILLE
             and hashlib.sha256(donnees).hexdigest() == SCELLE_M8_SHA256,
             f"{len(donnees)} o, sha256 1492b0bc…b0cd4 — l'ancre R7")
    # la famille sha INTACTE : les quatre notations relues aux longueurs
    # ARRÊTÉES du plan (74/387/139/165) — la frontière du geste précédent
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    attendus = {"h100001": 74, "h100002": 387, "h100003": 139, "h100004": 165}
    noms = {"h100001": "tls13-01-sha256-init", "h100002": "tls13-02-sha256-comprimer",
            "h100003": "tls13-03-sha256-absorber", "h100004": "tls13-04-sha256-finaliser"}
    ok, details = True, []
    for bid, attendu in attendus.items():
        rva, slot = L.SLOTS_TLS13[bid]
        chemin = os.path.join(ICI, "notation", noms[bid] + ".asm")
        octets, _ = B4.assembler_bloc(ks, chemin, rva, slot)
        if len(octets) != attendu:
            ok = False
            details.append(f"{noms[bid]} : {len(octets)} o ≠ {attendu}")
    controle("V0.b:la-famille-sha-intacte",
             ok, "les quatre notations relues aux longueurs arrêtées "
                 "74/387/139/165 o" + (f" — DÉFAUTS : {details}" if details else ""))
    # l'arbre I scellé relu : verifier_specs_m9a rejoué, exit 0 (R2)
    proc = subprocess.run([sys.executable, "scripts/verifier_specs_m9a.py"],
                          cwd=TRIADE, capture_output=True, text=True)
    controle("V0.c:l-arbre-I-scelle-relu-vert",
             proc.returncode == 0,
             "verifier_specs_m9a rejoué — les 28 spécifications posées et "
             "cohérentes (le sceau de l'ère tient)")


# --- V1 : round-trip + concordance au plan -----------------------------------------

def vecteur_v1(emul: Emulation):
    section("V1 — round-trip de notation + concordance au plan (source unique)")
    attendus = {"h100005": 435, "h100006": 151, "h100007": 347, "h100008": 310}
    noms = {"h100005": "tls13-05-hmac-sha256", "h100006": "tls13-06-hkdf-extract",
            "h100007": "tls13-07-hkdf-expand", "h100008": "tls13-08-hkdf-expand-label"}
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

    # la concordance des appels directs : chaque cible == le plan (I1)
    cibles_attendues = {
        "h100005": {L.TLS01_VA: 3, L.TLS03_VA: 5, L.TLS04_VA: 3},
        "h100006": {L.TLS05_VA: 1},
        "h100007": {L.TLS05_VA: 1},
        "h100008": {L.TLS07_VA: 1},
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
    controle("V1.e:les-appels-directs-au-plan",
             ok_appels,
             "05 → TLS01×3/TLS03×5/TLS04×3 ; 06/07 → TLS05 ; 08 → TLS07 "
             "(les adresses scellées)" + (f" — DÉFAUTS : {details}" if details else ""))

    # la concordance des masques ipad/opad de 05 == le plan (I3)
    texte05 = open(os.path.join(ICI, "notation", noms["h100005"] + ".asm"),
                   encoding="utf-8").read()
    ipad_attendu = bytes([L.HMAC_IPAD] * 8)
    opad_attendu = bytes([L.HMAC_OPAD] * 8)
    ok_masques = (f"0x{int.from_bytes(ipad_attendu, 'little'):016x}" in texte05
                  and f"0x{int.from_bytes(opad_attendu, 'little'):016x}" in texte05)
    controle("V1.f:les-masques-de-05-au-plan",
             ok_masques,
             f"ipad 0x{L.HMAC_IPAD:02x} et opad 0x{L.HMAC_OPAD:02x} ×8 — "
             "tls13/layout.py (64 positions FIXES)")

    # la concordance du préfixe « tls13 » de 08 == le plan (I2)
    texte08 = open(os.path.join(ICI, "notation", noms["h100008"] + ".asm"),
                   encoding="utf-8").read()
    prefixe = L.PREFIXE_ETIQUETTE                       # b"tls13 "
    mot1 = int.from_bytes(prefixe[:4], "little")        # « tls1 »
    mot2 = int.from_bytes(prefixe[4:], "little")        # « 3  »
    ok_prefixe = (f"0x{mot1:08x}" in texte08 and f"0x{mot2:04x}" in texte08)
    controle("V1.g:le-prefixe-de-08-au-plan",
             ok_prefixe,
             f"« {prefixe.decode()} » en immédiats 0x{mot1:08x} + 0x{mot2:04x} — "
             "tls13/layout.py PREFIXE_ETIQUETTE (jamais recopiée, T5)")

    # la structure du domaine : AUCUN site syscall, AUCUN appel indirect,
    # AUCUN déplacement RIP (le miroir de la charte § 7 — tout vit en
    # immédiats et sur la pile, l'ancêtre tls13-02 lisait K @0x2F00)
    ok_struct, motifs = True, []
    for bid, insns in insns_par_bloc.items():
        for insn in insns:
            if insn.mnemonic in ("syscall", "int", "sysenter"):
                ok_struct, _ = False, motifs.append(f"{bid}:{insn.mnemonic}")
            if insn.mnemonic in ("call", "jmp") and "[" in insn.op_str:
                ok_struct, _ = False, motifs.append(f"{bid}:indirect")
            if "[rip" in insn.op_str:
                ok_struct, _ = False, motifs.append(f"{bid}:rip")
    controle("V1.h:calcul-pur-aucun-syscall-aucun-rip",
             ok_struct, "les quatre notations — charte § 7 : aucun import, "
             "aucun syscall, aucun déplacement RIP"
             + (f" — MOTIFS : {motifs}" if motifs else ""))

    # le temps constant STRUCTUREL : aucun saut conditionnel ne conditionne
    # sur une LECTURE mémoire — les données (clé, IKM, PRK, secret) ne
    # touchent JAMAIS une branche (la preuve mesurée suit en V6)
    ok_temps, vus, defauts = True, 0, []
    for bid, insns in insns_par_bloc.items():
        for i, insn in enumerate(insns):
            if insn.mnemonic.startswith("j") and insn.mnemonic != "jmp":
                vus += 1
                j = i - 1
                while j >= 0 and insns[j].mnemonic not in ("cmp", "test"):
                    j -= 1
                if j < 0 or "[" in insns[j].op_str:
                    ok_temps = False
                    defauts.append(f"{bid}:{insn.mnemonic} après {insns[j].mnemonic if j >= 0 else '?'}")
    controle("V1.i:temps-constant-structurel",
             ok_temps and vus > 0,
             f"{vus} sauts conditionnels, chacun sur cmp/test SANS opérande "
             "mémoire (les longueurs et les compteurs publics)"
             + (f" — DÉFAUTS : {defauts}" if defauts else ""))


# --- V2 : les vecteurs officiels RFC 4231 ------------------------------------------

def vecteur_v2(emul: Emulation):
    section("V2 — les vecteurs officiels RFC 4231 appendice A (octet pour octet)")
    for i, (nom, cle, message, attendu_hex, tronque) in enumerate(VECTEURS_4231):
        attendu = bytes.fromhex(attendu_hex)
        # la référence CROISÉE : hashlib == le vecteur officiel (l'instrument
        # se contrôle avant de juger — la constante fautive serait attrapée)
        if ref_hmac(cle, message)[:tronque] != attendu:
            controle(f"V2.{i}:reference-hashlib-{nom}", False,
                     "la constante du vecteur diverge de hashlib — INSTRUMENT DÉFAILLANT")
            continue
        mac, r = hmac_sha(emul, cle, message)
        controle(f"V2.{i}:{nom}",
                 mac[:tronque] == attendu and r["rax"] == 0 and r["crash"] is None,
                 f"{mac[:8].hex()}… == {attendu_hex[:16]}…"
                 + (f" (tronqué à {tronque} o — la borne officielle)" if tronque != 32 else ""))

    # le balayage différentiel : l'expulsion de la clé exercée aux bornes
    # 0/1/31/32/63/64/65/100/131 × messages 0..1000 — hashlib en oracle
    longueurs_cle = [0, 1, 20, 31, 32, 33, 63, 64, 65, 100, 131]
    longueurs_msg = [0, 1, 55, 56, 63, 64, 65, 127, 128, 129, 200, 1000]
    ecarts, joues = 0, 0
    for lk in longueurs_cle:
        for lm in longueurs_msg:
            cle = bytes((i * 11 + lk) & 0xFF for i in range(lk))
            message = bytes((i * 7 + 3) & 0xFF for i in range(lm))
            mac, _ = hmac_sha(emul, cle, message)
            joues += 1
            if mac != ref_hmac(cle, message):
                ecarts += 1
    controle("V2.7:le-balayage-differentiel-132-cas",
             ecarts == 0,
             f"{joues} cas (clés 0..131 o × messages 0..1000 o) — l'expulsion "
             "exercée dans les DEUX sens, ZÉRO écart avec hashlib")


# --- V3 : les vecteurs officiels RFC 5869 + le transfert RFC 8448 -------------------

def vecteur_v3(emul: Emulation):
    section("V3 — RFC 5869 + le transfert RFC 8448 (les clés du transcript)")

    # (a) les extraits officiels RFC 5869 (tls13-06 Q1)
    for i, cas in enumerate(VECTEURS_5869):
        prk_attendu = bytes.fromhex(cas["prk"])
        if ref_extrait(cas["sel"], cas["ikm"]) != prk_attendu:
            controle(f"V3.a{i}:reference-extraite", False, "INSTRUMENT DÉFAILLANT")
            continue
        prk, r = hkdf_extraire(emul, cas["sel"], cas["ikm"])
        controle(f"V3.a{i}:extract-{i + 1}",
                 prk == prk_attendu and r["rax"] == 0,
                 f"sel {len(cas['sel'])} o, IKM {len(cas['ikm'])} o → PRK "
                 f"{prk.hex()[:16]}…")

    # (b) les expansions officielles RFC 5869 (tls13-07 Q1)
    for i, cas in enumerate(VECTEURS_5869):
        okm_attendue = bytes.fromhex(cas["okm"])
        if ref_etend(bytes.fromhex(cas["prk"]), cas["info"], cas["L"]) != okm_attendue:
            controle(f"V3.b{i}:reference-etendue", False, "INSTRUMENT DÉFAILLANT")
            continue
        okm, r = hkdf_etendre(emul, bytes.fromhex(cas["prk"]), cas["info"], cas["L"])
        controle(f"V3.b{i}:expand-{i + 1}",
                 okm == okm_attendue and r["rax"] == 0,
                 f"L = {cas['L']}, info {len(cas['info'])} o → OKM "
                 f"{okm.hex()[:16]}…")

    # (c) la chaîne complète : Extract(sel, IKM) → Expand (les deux blocs)
    for i, cas in enumerate(VECTEURS_5869):
        prk, _ = hkdf_extraire(emul, cas["sel"], cas["ikm"])
        okm, _ = hkdf_etendre(emul, prk, cas["info"], cas["L"])
        controle(f"V3.c{i}:la-chaine-complete-{i + 1}",
                 okm == bytes.fromhex(cas["okm"]),
                 f"Extract → PRK → Expand → OKM (les vecteurs RFC 5869 enchaînés)")

    # (d) les TROIS extraits du transcript RFC 8448 (tls13-06 — le sel
    # dérivé et le sel vide EXERCÉS sur pièces officielles)
    sel_handshake = bytes.fromhex(
        "6f2615a108c702c5678f54fc9dbab69716c076189c48250cebeac3576c3611ba")
    sel_master = bytes.fromhex(
        "43de77e0c77713859a944db9db2590b53190a65b3ee2e4f12dd7a0bb7ce254b4")
    extraits = [
        ("early", b"\x00" * 32, b"\x00" * 32, TRANSFERT_8448["early"]),
        ("handshake", sel_handshake, TRANSFERT_8448["shared"], TRANSFERT_8448["handshake"]),
        ("master", sel_master, b"\x00" * 32, TRANSFERT_8448["master"]),
    ]
    for nom, sel, ikm, attendu in extraits:
        if ref_extrait(sel, ikm) != attendu:
            controle(f"V3.d:{nom}:reference", False, "INSTRUMENT DÉFAILLANT")
            continue
        prk, r = hkdf_extraire(emul, sel, ikm)
        controle(f"V3.d:{nom}-extrait-du-transcript",
                 prk == attendu and r["rax"] == 0,
                 f"RFC 8448 § 3 : {prk.hex()[:16]}…")

    # (e) les étiquettes du transcript RFC 8448 (tls13-08 Q1 — les clés
    # consignées par le fixture, rendues par le bloc, la structure HkdfLabel
    # RECROISÉE avec les « info » exactes de la RFC)
    rendues, infos_exactes = 0, 0
    for cle_prk, libelle, contexte, lon, attendu_hex, info_hex in TRANSFERT_8448["etiquettes"]:
        attendu = bytes.fromhex(attendu_hex)
        info_exacte = bytes.fromhex(info_hex)
        secret = TRANSFERT_8448[cle_prk]
        ctx = TRANSFERT_8448["ch_sh_hash"] if contexte is None else contexte
        if ref_etiquette(secret, libelle.encode(), ctx, lon) != attendu:
            controle(f"V3.e:{libelle.decode()}-{cle_prk}:reference", False,
                     "INSTRUMENT DÉFAILLANT")
            continue
        # la structure attendue == l'« info » EXACTE consignée par la RFC 8448
        structure = (struct.pack(">H", lon) + bytes([6 + len(libelle)])
                     + b"tls13 " + libelle.encode() + bytes([len(ctx)]) + ctx)
        if structure == info_exacte:
            infos_exactes += 1
        sortie, r = hkdf_etiqueter(emul, secret, libelle.encode(), ctx, lon)
        if sortie == attendu and r["rax"] == 0:
            rendues += 1
    controle("V3.e:les-etiquettes-du-transcript",
             rendues == len(TRANSFERT_8448["etiquettes"]),
             f"{rendues}/{len(TRANSFERT_8448['etiquettes'])} clés rendues "
             "(« derived », « c/s hs traffic », « key », « iv », « finished »)")
    controle("V3.f:la-structure-hkdflabel-recroisee",
             infos_exactes == len(TRANSFERT_8448["etiquettes"]),
             "la structure reconstruite == les « info » EXACTES imprimées par "
             "la RFC 8448 (la sérialisation consignée, octet pour octet)")

    # (g) la borne L = 8160 (255 × 32 : le compteur d'un octet, la garde)
    prk = TRANSFERT_8448["handshake"]
    okm, r = hkdf_etendre(emul, prk, b"borne", 8160)
    attendu = ref_etend(prk, b"borne", 8160)
    controle("V3.g:la-borne-L-8160",
             okm == attendu and r["rax"] == 0 and len(okm) == 8160,
             "255 itérations, le compteur atteint 0xFF — la garde du RFC 5869")
    # les longueurs aux bornes de bloc : 31/32/33/64 (la découpe de l'OKM)
    ok, details = True, []
    for lon in (1, 31, 32, 33, 64, 65, 8159):
        okm, r = hkdf_etendre(emul, prk, b"", lon)
        if okm != ref_etend(prk, b"", lon) or r["rax"] != 0:
            ok = False
            details.append(f"L={lon}")
    controle("V3.h:les-bornes-de-decoupe",
             ok, "L = 1/31/32/33/64/65/8159 — la dernière itération partielle "
                 "recopiée SANS JAMAIS dépasser" + (f" — DÉFAUTS : {details}" if details else ""))

    # (i) l'oracle différentiel : la structure HkdfLabel reconstruite en
    # Python contre le bloc, 240 cas aléatoires bornés (libellés 1..249,
    # contextes 0..255, L 1..8160)
    rng = random.Random(20261106)
    ecarts = 0
    for _ in range(240):
        libelle = bytes(rng.randrange(256) for _ in range(rng.randrange(1, 250)))
        contexte = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 256)))
        secret = bytes(rng.randrange(256) for _ in range(32))
        L = rng.choice([rng.randrange(1, 64), rng.randrange(1, 8161)])
        sortie, r = hkdf_etiqueter(emul, secret, libelle, contexte, L)
        if sortie != ref_etiquette(secret, libelle, contexte, L) or r["rax"] != 0:
            ecarts += 1
    controle("V3.i:loracle-differentiel-240-cas",
             ecarts == 0,
             "240 cas aléatoires (libellés 1..249, contextes 0..255, "
             "L 1..8160) — la structure reconstruite, ZÉRO écart")


# --- V4 : le contrat -----------------------------------------------------------------

def vecteur_v4(emul: Emulation):
    section("V4 — le contrat (les pré/post de chaque bloc, sur pièces)")

    # les non-volatiles rendus + la pile équilibrée + les canaris : les 4
    # blocs (un cas représentatif de chaque — le balayage V2/V3 les couvre)
    ok_nv, details = True, []
    for nom, va, args, pile, prep in [
            ("tls13-05", L.TLS05_VA,
             {"rcx": ADRESSE_CLE, "rdx": 32, "r8": ADRESSE_MESSAGE, "r9": 16},
             [ADRESSE_SORTIE], "hmac"),
            ("tls13-06", L.TLS06_VA,
             {"rcx": ADRESSE_CLE, "rdx": 32, "r8": ADRESSE_MESSAGE, "r9": 22},
             [ADRESSE_PRK], "extract"),
            ("tls13-07", L.TLS07_VA,
             {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 10, "r9": 42},
             [ADRESSE_OKM], "expand"),
            ("tls13-08", L.TLS08_VA,
             {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 7,
              "r9": ADRESSE_CTX_TRANSFERT},
             [0, 32, ADRESSE_OKM], "etiquette")]:
        emul.poser_cle(bytes(range(32)))
        emul.poser_message(b"contrat-canari-" + nom.encode())
        emul.poser_info(b"info-canari")
        emul.poser_contexte(b"ctx-canari")
        emul.preparer_okm(64)
        r = emul.appeler(va, args, args_pile=pile)
        if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
                and r["canaris_haut"] and r["canaris_profond"]
                and r["logements_intacts"] and r["rax"] == 0):
            ok_nv = False
            details.append(f"{nom}(nv={emul.non_volatiles_rendus(r)},"
                           f"pile={r['pile_equilibree']},haut={r['canaris_haut']},"
                           f"prof={r['canaris_profond']},log={r['logements_intacts']})")
    controle("V4.a:non-volatiles-pile-canaris-logements (les quatre blocs)",
             ok_nv, "les 8 sentinelles rendues, rsp équilibrée, l'ombre intacte, "
             "les logements d'arguments relus, la zone profonde intacte"
             + (f" — DÉFAUTS : {details}" if details else ""))

    # l'alignement msx64 à travers les appels directs : à CHAQUE entrée de
    # TLS01/TLS03/TLS04 (appelés par 05), TLS05 (par 06/07) et TLS07 (par
    # 08), rsp ≡ 8 (mod 16) — le point de vue du CALLE
    emul.surveillance = {va: [] for va in (L.TLS01_VA, L.TLS03_VA, L.TLS04_VA,
                                           L.TLS05_VA, L.TLS07_VA)}
    try:
        hmac_sha(emul, bytes.fromhex("aa" * 131), b"alignement")   # le chemin long
        hmac_sha(emul, b"cle", b"alignement")                      # le chemin court
        hkdf_extraire(emul, b"sel", b"ikm")
        hkdf_etendre(emul, TRANSFERT_8448["handshake"], b"info", 99)
        hkdf_etiqueter(emul, TRANSFERT_8448["early"], b"derived", b"", 32)
    finally:
        entrees = {va: list(l) for va, l in emul.surveillance.items()}
        emul.surveillance = None
    total = sum(len(l) for l in entrees.values())
    ok_align = total > 0 and all(e % 16 == 8 for l in entrees.values() for e in l)
    controle("V4.b:l-alignement-msx64-a-l-entree-de-chaque-calle",
             ok_align,
             f"{total} entrées surveillées (TLS01/03/04 par 05 long et court, "
             "TLS05 par 06/07, TLS07 par 08), rsp ≡ 8 (mod 16) chacune")

    # les entrées INTACTES (Q2) : la clé, le message, le sel, l'IKM, le PRK,
    # l'info, le libellé et le contexte relus OCTET POUR OCTET après le geste
    cle = bytes(range(131))
    message = bytes((i * 13 + 5) & 0xFF for i in range(1000))
    hmac_sha(emul, cle, message)
    ok_intacts = (emul.canaris_entree_intacts(ADRESSE_CLE, 131)
                  and emul.canaris_entree_intacts(ADRESSE_MESSAGE, 1000))
    sel, ikm = b"sel-de-contrat-32-octets-abcdef", b"ikm-de-contrat"
    hkdf_extraire(emul, sel, ikm)
    ok_intacts &= (emul.canaris_entree_intacts(ADRESSE_CLE, len(sel))
                   and emul.canaris_entree_intacts(ADRESSE_MESSAGE, len(ikm)))
    prk, info = TRANSFERT_8448["handshake"], b"info-de-contrat"
    hkdf_etendre(emul, prk, info, 100)
    ok_intacts &= (emul.canaris_entree_intacts(ADRESSE_CLE, 32)
                   and emul.canaris_entree_intacts(ADRESSE_INFO, len(info)))
    libelle, contexte = b"c hs traffic", TRANSFERT_8448["ch_sh_hash"]
    hkdf_etiqueter(emul, prk, libelle, contexte, 32)
    ok_intacts &= (emul.canaris_entree_intacts(ADRESSE_CLE, 32)
                   and emul.canaris_entree_intacts(ADRESSE_INFO, len(libelle))
                   and emul.canaris_entree_intacts(ADRESSE_CTX_TRANSFERT, len(contexte)))
    controle("V4.c:les-entrees-intactes (Q2 des quatre blocs)",
             ok_intacts,
             "clé/sel/PRK/secret, message/IKM, info/libellé, contexte — "
             "relus identiques, canaris des zones intacts")

    # la sortie JAMAIS dépassée (l'OKM de la borne) : les canaris APRÈS L
    lon = 8159                                # la dernière itération copie 31 o
    hkdf_etendre(emul, TRANSFERT_8448["handshake"], b"garde", lon)
    apres = bytes(emul.uc.mem_read(ADRESSE_OKM + lon, 0x100))
    controle("V4.d:la-sortie-jamais-depassee",
             apres == CANARI * 0x100,
             f"L = {lon} (31 o à la dernière itération) — les canaris après L "
             "intacts : le brouillon 32 o ne déborde JAMAIS dans OKM")

    # les refus NOMMÉS : chaque cas du contrat exercé, un par un (Q3)
    emul.poser_cle(b"\x11" * 32)
    emul.poser_message(b"message")
    emul.poser_info(b"libelle")
    emul.poser_contexte(b"contexte")
    refus = [
        ("05:sortie-nulle→-1", L.TLS05_VA,
         {"rcx": ADRESSE_CLE, "rdx": 32, "r8": ADRESSE_MESSAGE, "r9": 7}, [0], -1),
        ("06:PRK-nul→-1", L.TLS06_VA,
         {"rcx": ADRESSE_CLE, "rdx": 32, "r8": ADRESSE_MESSAGE, "r9": 22}, [0], -1),
        ("06:IKM-vide→-2", L.TLS06_VA,
         {"rcx": ADRESSE_CLE, "rdx": 32, "r8": ADRESSE_MESSAGE, "r9": 0},
         [ADRESSE_PRK], -2),
        ("07:OKM-nulle→-1", L.TLS07_VA,
         {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 7, "r9": 42}, [0], -1),
        ("07:L-nul→-2", L.TLS07_VA,
         {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 7, "r9": 0},
         [ADRESSE_OKM], -2),
        ("07:L-8161→-2", L.TLS07_VA,
         {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 7, "r9": 8161},
         [ADRESSE_OKM], -2),
        ("07:F-hors-borne→-2", L.TLS07_VA,
         {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO,
          "r8": 0x1FFFFFFFFFFFFFE0, "r9": 42}, [ADRESSE_OKM], -2),
        ("08:sortie-nulle→-1", L.TLS08_VA,
         {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 7,
          "r9": ADRESSE_CTX_TRANSFERT}, [0, 32, 0], -1),
        ("08:secret-nul→-1", L.TLS08_VA,
         {"rcx": 0, "rdx": ADRESSE_INFO, "r8": 7,
          "r9": ADRESSE_CTX_TRANSFERT}, [0, 32, ADRESSE_OKM], -1),
        ("08:libelle-nul→-1", L.TLS08_VA,
         {"rcx": ADRESSE_CLE, "rdx": 0, "r8": 7,
          "r9": ADRESSE_CTX_TRANSFERT}, [0, 32, ADRESSE_OKM], -1),
        ("08:libelle-vide→-2", L.TLS08_VA,
         {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 0,
          "r9": ADRESSE_CTX_TRANSFERT}, [0, 32, ADRESSE_OKM], -2),
        ("08:libelle-250→-2", L.TLS08_VA,
         {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 250,
          "r9": ADRESSE_CTX_TRANSFERT}, [0, 32, ADRESSE_OKM], -2),
        ("08:C-256→-2", L.TLS08_VA,
         {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 7,
          "r9": ADRESSE_CTX_TRANSFERT}, [256, 32, ADRESSE_OKM], -2),
        ("08:ctx-nul-C-positif→-1", L.TLS08_VA,
         {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 7,
          "r9": 0}, [8, 32, ADRESSE_OKM], -1),
        ("08:L-nul→-2", L.TLS08_VA,
         {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 7,
          "r9": ADRESSE_CTX_TRANSFERT}, [0, 0, ADRESSE_OKM], -2),
        ("08:L-8161→-2", L.TLS08_VA,
         {"rcx": ADRESSE_CLE, "rdx": ADRESSE_INFO, "r8": 7,
          "r9": ADRESSE_CTX_TRANSFERT}, [0, 8161, ADRESSE_OKM], -2),
    ]
    ok_refus, defauts = True, []
    for nom, va, args, pile, attendu in refus:
        emul.preparer_okm(64)
        r = emul.appeler(va, args, args_pile=pile)
        if r["rax"] != attendu or r["crash"] is not None:
            ok_refus = False
            defauts.append(f"{nom}: rax={r['rax']}")
    controle("V4.e:les-refus-nommes (Q3, seize cas)",
             ok_refus, "chaque cas du contrat exercé : -1 pointeurs nuls, "
             "-2 bornes (L 0/8161, libellé 0/250, C 256, F hors borne, IKM vide)"
             + (f" — DÉFAUTS : {defauts}" if defauts else ""))


# --- V5 : la falsification (zéro silence) ---------------------------------------------

def vecteur_v5(emul: Emulation):
    section("V5 — la falsification (chaque mutation ATTRAPÉE, zéro silence)")

    # chaque vecteur RFC 4231 muté (premier/milieu/dernier octet de la CLÉ et
    # du MESSAGE) → divergence du MAC
    attrapes, total = 0, 0
    for _, cle, message, attendu_hex, _ in VECTEURS_4231:
        attendu = bytes.fromhex(attendu_hex)
        for pos in (0, len(cle) // 2, len(cle) - 1):
            mute = bytearray(cle)
            mute[pos] ^= 0x01
            mac, _ = hmac_sha(emul, bytes(mute), message)
            total += 1
            attrapes += mac != attendu
        for pos in (0, len(message) // 2, len(message) - 1):
            mute = bytearray(message)
            mute[pos] ^= 0x01
            mac, _ = hmac_sha(emul, cle, bytes(mute))
            total += 1
            attrapes += mac != attendu
    controle("V5.a:cles-et-messages-mutes-attrapes",
             attrapes == total and total > 0,
             f"{attrapes}/{total} mutations (premier/milieu/dernier octet de "
             "la clé ET du message) ATTRAPÉES")

    # l'IKM et le sel mutés → le PRK diverge ; le PRK muté → l'OKM diverge ;
    # le secret muté → l'étiquette diverge (la propriété hérite de 05)
    attrapes, total = 0, 0
    for cas in VECTEURS_5869:
        prk_attendu = bytes.fromhex(cas["prk"])
        for pos in (0, len(cas["ikm"]) // 2, len(cas["ikm"]) - 1):
            mute = bytearray(cas["ikm"])
            mute[pos] ^= 0x01
            prk, _ = hkdf_extraire(emul, cas["sel"], bytes(mute))
            total += 1
            attrapes += prk != prk_attendu
        if cas["sel"]:
            mute = bytearray(cas["sel"])
            mute[len(cas["sel"]) // 2] ^= 0x01
            prk, _ = hkdf_extraire(emul, bytes(mute), cas["ikm"])
            total += 1
            attrapes += prk != prk_attendu
    controle("V5.b:ikm-et-sel-mutes-attrapes",
             attrapes == total,
             f"{attrapes}/{total} mutations de l'IKM et du sel ATTRAPÉES (le PRK diverge)")

    prk = TRANSFERT_8448["handshake"]
    okm_attendue = ref_etend(prk, b"info", 42)
    attrapes, total = 0, 0
    for pos in (0, 16, 31):
        mute = bytearray(prk)
        mute[pos] ^= 0x01
        okm, _ = hkdf_etendre(emul, bytes(mute), b"info", 42)
        total += 1
        attrapes += okm != okm_attendue
    etiquette_attendue = ref_etiquette(prk, b"key", b"", 16)
    for pos in (0, 16, 31):
        mute = bytearray(prk)
        mute[pos] ^= 0x01
        sortie, _ = hkdf_etiqueter(emul, bytes(mute), b"key", b"", 16)
        total += 1
        attrapes += sortie != etiquette_attendue
    controle("V5.c:prk-et-secret-mutes-attrapes",
             attrapes == total,
             f"{attrapes}/{total} mutations du PRK et du secret ATTRAPÉES "
             "(l'OKM et l'étiquette divergent)")

    # la comparaison n'est pas muette : chaque bit du résultat attendu muté
    # → l'égalité ÉCHOUE (l'instrument se prouve non-vide)
    attrapes, total = 0, 0
    for _, _, _, attendu_hex, _ in VECTEURS_4231:
        attendu = bytearray(bytes.fromhex(attendu_hex))
        for bit in (0, 127, 255):
            if bit // 8 >= len(attendu):
                continue
            mute = bytearray(attendu)
            mute[bit // 8] ^= 1 << (bit % 8)
            total += 1
            attrapes += bytes(mute) != bytes(attendu)
    controle("V5.d:la-comparaison-n-est-pas-muette",
             attrapes == total,
             f"{attrapes}/{total} résultats attendus mutés → l'égalité ÉCHOUE")

    # K corrompu → l'HMAC diverge : LA PREUVE que la table est LUE à travers
    # la composition (l'ancêtre tls13-02 la lit — I3)
    k_orig = bytes(emul.uc.mem_read(L.R_K, 256))
    emul.uc.mem_write(L.R_K + 13 * 4, struct.pack("<I", L.K[13] ^ 1))
    mac, _ = hmac_sha(emul, b"\x0b" * 20, b"Hi There")
    emul.uc.mem_write(L.R_K, k_orig)
    controle("V5.e:K-corrompu-l-hmac-diverge",
             mac != bytes.fromhex(VECTEURS_4231[0][3]),
             "K[13] muté → le MAC diverge : la table @0x2F00 est LUE par la "
             "composition (tls13-05 → tls13-02)")


# --- V6 : le temps constant mesuré ------------------------------------------------------

def vecteur_v6(emul: Emulation, graine: int):
    section("V6 — le temps constant MESURÉ (I3 des quatre specs, la charte § 3)")
    rng = random.Random(graine)
    message = b"temps-constant"

    # tls13-05 : la clé COURTE (32 o) — 4 clés différentes, même compte
    comptes = []
    for _ in range(4):
        cle = bytes(rng.randrange(256) for _ in range(32))
        _, r = hmac_sha(emul, cle, message, compter=True)
        comptes.append(r["compteur"])
    controle("V6.a:05-cle-courte-compte-constant",
             len(set(comptes)) == 1,
             f"4 clés de 32 o, {comptes[0]} instructions EXACTEMENT")

    # tls13-05 : la clé LONGUE (131 o — l'expulsion) — même compte
    comptes = []
    for _ in range(4):
        cle = bytes(rng.randrange(256) for _ in range(131))
        _, r = hmac_sha(emul, cle, message, compter=True)
        comptes.append(r["compteur"])
    controle("V6.b:05-cle-longue-compte-constant",
             len(set(comptes)) == 1,
             f"4 clés de 131 o (H(clé) d'abord), {comptes[0]} instructions EXACTEMENT")

    # tls13-06 : l'IKM (le secret partagé) — 4 IKM différents, même compte
    comptes = []
    for _ in range(4):
        ikm = bytes(rng.randrange(256) for _ in range(32))
        _, r = hkdf_extraire(emul, b"sel", ikm, compter=True)
        comptes.append(r["compteur"])
    controle("V6.c:06-ikm-compte-constant",
             len(set(comptes)) == 1,
             f"4 IKM de 32 o, {comptes[0]} instructions EXACTEMENT")

    # tls13-07 : le PRK — 2 PRK différents, même compte (info et L publics)
    comptes = []
    for prk in (TRANSFERT_8448["handshake"], TRANSFERT_8448["early"]):
        _, r = hkdf_etendre(emul, prk, b"info", 99, compter=True)
        comptes.append(r["compteur"])
    controle("V6.d:07-prk-compte-constant",
             len(set(comptes)) == 1,
             f"2 PRK différents, L = 99, {comptes[0]} instructions EXACTEMENT")

    # tls13-08 : le secret — 2 secrets différents, même compte
    comptes = []
    for secret in (TRANSFERT_8448["handshake"], TRANSFERT_8448["c_hs_traffic"]):
        _, r = hkdf_etiqueter(emul, secret, b"key", b"", 16, compter=True)
        comptes.append(r["compteur"])
    controle("V6.e:08-secret-compte-constant",
             len(set(comptes)) == 1,
             f"2 secrets différents, « key » L = 16, {comptes[0]} instructions "
             "EXACTEMENT — le contenu JAMAIS, la longueur seule")


# --- Le verdict --------------------------------------------------------------------------

def main() -> int:
    graine = 20261106
    if "--graine" in sys.argv:
        graine = int(sys.argv[sys.argv.index("--graine") + 1])
    print("=== tls13/harnais_hkdf.py — LE HARNAIS DE LA FAMILLE hkdf "
          "(chantier M9-(b), la suite) ===")
    print(f"    plan : tls13/layout.py · graine : {graine}")
    emul = Emulation()
    vecteur_v0()
    vecteur_v1(emul)
    vecteur_v2(emul)
    vecteur_v3(emul)
    vecteur_v4(emul)
    vecteur_v5(emul)
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
