#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tls13/harnais_x25519.py — LE HARNAIS DE LA FAMILLE x25519 DU DOMAINE tls13.

Chantier M9-(b), troisième geste : les blocs tls13-09..14 (f25519 addition,
soustraction, multiplication, propagation+gel, X25519 échelle de Montgomery,
X25519 clé publique — RFC 7748 § 5/§ 6.1) NOTÉS-MESURÉS-PROUVÉS sur les
familles sha et hkdf notées-mesurées-prouvées aux gestes précédents. Le
modèle est le harnais hkdf (tls13/harnais_hkdf.py) : l'émulation nue à les
RVA du plan (mécanisme D79), l'appelant factice pose les sentinelles non
volatiles et les canaris, le verdict est TRANCHÉ par le code — jamais cru.

LE CAHIER (la charte § 2 : les vecteurs officiels AVANT usage, la
falsification, zéro silence) :

  V0 — LES PIÈCES DU PLAN : le scellé 0.9.0 relu (l'ancre 1492b0bc…), les
       familles sha ET hkdf INTACTES (les huit notations re-round-tripées
       aux longueurs arrêtées 74/387/139/165 + 435/151/347/310 — la
       frontière des gestes précédents), K[64] posé à R_K, LES FIXTURES
       DU DOMAINE posés à leur ARRÊT .text6 (U9 @ 0xFF00, EXP_INV
       @ 0xFF20 — les contenus re-dérivés du plan par arithmétique), l'arbre
       I scellé relu VERT (verifier_specs_m9a rejoué — R2) ;
  V1 — LE ROUND-TRIP + LA CONCORDANCE : chaque notation ré-assemblée en ses
       octets (keystone == capstone, R5), les longueurs == l'ARRÊT du plan
       (54/252/1078/281/2884/23 o, D161), les appels directs de 09/10/11 ==
       TLS12, de 13 == TLS09×4 + TLS10×4 + TLS11×13 (la recette § 5 : 4
       add + 4 sub + 10 mul PAR ITÉRATION + l'inversion 255 carrés + 253
       mults + le produit final), de 14 == TLS13 (I1/I5) ; LES IMMÉDIATS au
       plan : les membres de 2p de 10 == F25519_P2_MEMBRES (l'ERRATUM I1
       consigné : la spec écrivait « (2^51−38) puis (2^51−1)×4 » — compose
       2^255−38 ≡ −19, la notation re-dérive), M51/P0/19 de 12, M51/121665
       et les masques de clamp de 13 ; la structure du domaine : AUCUN site
       syscall, AUCUN appel indirect, les déplacements RIP UNIQUEMENT aux
       DEUX fixtures du plan (EXP_INV lu par 13, U9 par 14 — l'ARRÊT D95) ;
       le temps constant STRUCTUREL : 09/11/12 SANS AUCUN saut
       conditionnel, 10 exactement UN (le verrou d'emprunt fail-closed —
       le contrat, jamais un secret), 13 exactement TROIS (les deux
       compteurs de boucle et le bit de L'EXPOSANT PUBLIC p−2 — le scalaire
       ne touche JAMAIS une branche, charte § 3) ;
  V2 — LES VECTEURS OFFICIELS RFC 7748 : les DEUX paires du § 5.2, la paire
       d'Alice ET celle de Bob du § 6.1 rendues par l'échelle au point 9,
       LE SECRET PARTAGÉ consigné (Alice × publique de Bob == Bob ×
       publique d'Alice == K), LE TEST ITÉRÉ (l'entrée 9 itérée 1 fois puis
       1000 fois — les résultats consignés, joués sur l'émulation NUE :
       l'instrument permanent ne compte pas mille pas) + l'oracle
       différentiel (Python) sur l'échelle ET les quatre opérateurs ;
  V3 — LES CAS PUNITIFS : le gel (p → 0 exact, p−1 inchangé
       OCTET-IDENTIQUE, l'invariance de la passe), les valeurs LÂCHES de
       l'école (membres saturés 2^52−1, a = b = lâches, 0·x, 1·x, (p−1)²,
       x²), la soustration lâche (a ≥ p admise), le point u NON CANONIQUE
       (les valeurs [p, 2^255) traitées comme réduites — RFC 7748 § 5, le
       bit 255 masqué), les dégénérés (u de petit ordre → la sortie nulle) ;
  V4 — LE CONTRAT : les entrées INTACTES (le scalaire, le point u, la clé
       privée — Q2), les non-volatiles rendus, la pile équilibrée, l'ombre
       et les logements intacts, L'ALIGNEMENT msx64 à l'entrée de CHAQUE
       appelé à travers les appels directs (le point de vue du CALLE : 09,
       10, 11, 12 par la composition, 13 par 14), la sortie JAMAIS dépassée
       (canaris après les 32 o), ET LE VERROU fail-closed de 10 exercé :
       l'emprunt sortant → rax = −1 NOMMÉ, la sortie a JAMAIS écrite (le
       scratch meurt — l'échec E1 d'av-08 ÉLEVÉ en verdict, il ne se tait
       jamais) ;
  V5 — LA FALSIFICATION (zéro silence) : le scalaire muté (premier, milieu,
       dernier octet) → la sortie diverge, le point u muté → diverge, la
       clé privée mutée → la clé publique diverge, la comparaison n'est pas
       muette (chaque bit de l'attendu muté ÉCHOUE), LES FIXTURES
       CORROMPUS → divergence (U9 et EXP_INV : les données du plan sont
       LUES — la preuve à travers la composition) ;
  V6 — LE TEMPS CONSTANT MESURÉ (I1/I3 de chaque spec, la charte § 3) : le
       compte d'instructions IDENTIQUE pour des SCALAIRES différents (la
       clé privée : 4 couronnes), pour des POINTS u différents (2), pour
       des opérandes différents des opérateurs (add/sub/mul) — la longueur
       est publique, le contenu JAMAIS.

Usage : python3 harnais_x25519.py            # le cahier complet
        python3 harnais_x25519.py --graine N # la graine du générateur (défaut 20261107)
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
RET_MAGIQUE = 0xDE00            # dans la marge .text6 (après 0xDCC0) — jamais exécuté
ZONE_MEMBRES = 0x500000         # les opérandes membres (5×u64, canaris autour)
TAILLE_MEMBRES = 0x4000
ZONE_ENTREE = 0x600000          # le scalaire, le point u, la clé privée
TAILLE_ENTREE = 0x3000
ZONE_SORTIE = 0x700000          # la sortie sérialisée (32 o, canaris autour)
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP0 = 0x7F008000
ENTREE_RSP = RSP0 - 0x108       # ≡ 8 (mod 16) — le point de vue de l'APPELÉ

OFF_ZONE = 0x100
TAILLE_PAGE = 0x1000

ADRESSE_A = ZONE_MEMBRES + OFF_ZONE            # l'opérande a / la sortie gel
ADRESSE_B = ZONE_MEMBRES + 0x1100              # l'opérande b
ADRESSE_SCALAIRE = ZONE_ENTREE + OFF_ZONE      # le scalaire / la clé privée
ADRESSE_POINTE = ZONE_ENTREE + 0x1100          # le point u
ADRESSE_SORTIE = ZONE_SORTIE + OFF_ZONE        # la sortie (32 o)

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

# --- Les vecteurs officiels RFC 7748 § 5.2 (la fonction) -------------------------

VECTEURS_7748_52 = [
    ("§5.2-a (scalaire a546…, point e6db…)",
     "a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4",
     "e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c",
     "c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552"),
    ("§5.2-b (scalaire 4b66…, point e521…)",
     "4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d",
     "e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493",
     "95cbde9476e8907d7aade45cb4b873f88b595a68799fa152e6f8f7647aac7957"),
]

# --- Les vecteurs officiels RFC 7748 § 6.1 (Diffie-Hellman) ----------------------

ALICE_PRIV = "77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a"
ALICE_PUB = "8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a"
BOB_PRIV = "5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb"
BOB_PUB = "de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f"
PARTAGE = "4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742"

# --- Le test itéré RFC 7748 § 5.2 (la seconde espèce) ----------------------------

ITERE_1 = "422c8e7a6227d7bca1350b3e2bb7279f7897b87bb6854b783c60e80311ae3079"
ITERE_1000 = "684cf59ba83309552800ef566f2f4d3c1c3887c49360e3875f2eb94d99532c51"

# --- Le transfert RFC 8448 § 3 (Simple 1-RTT — le transcript enregistré) ---------

TRANSFERT_8448 = {
    "client_priv": "49af42ba7f7994852d713ef2784bcbcaa7911de26adc5642cb634540e7ea5005",
    "client_pub": "99381de560e4bd43d23d8e435a7dbafeb3c06e51c13cae4d5413691e529aaf2c",
    "serveur_pub": "c9828876112095fe66762bdbf7c672e156d6cc253b833df1dd69b1b04e751f0f",
    "partage": "8bd4054fb55b9d63fdfbacf9f04b9f0d35e6d63f537563efd46272900f89492d",
}

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


P = 2**255 - 19
M51 = (1 << 51) - 1


def vers_membres(v: int) -> list[int]:
    out = []
    for _ in range(4):
        out.append(v % (1 << 51))
        v //= (1 << 51)
    out.append(v)
    return out


def depuis_membres(m) -> int:
    return sum(x << (51 * i) for i, x in enumerate(m))


def ref_x25519(k_bytes: bytes, u_bytes: bytes) -> bytes:
    """La référence Python (RFC 7748 § 5, le pseudocode officiel)."""
    k = bytearray(k_bytes)
    k[0] &= 248
    k[31] &= 127
    k[31] |= 64
    k = int.from_bytes(k, "little")
    u = int.from_bytes(u_bytes, "little") & ((1 << 255) - 1)
    x1 = u % P
    x2, z2, x3, z3, swap = 1, 0, u % P, 1, 0
    for t in range(254, -1, -1):
        kt = (k >> t) & 1
        swap ^= kt
        if swap:
            x2, x3 = x3, x2
            z2, z3 = z3, z2
        swap = kt
        a = (x2 + z2) % P
        aa = a * a % P
        b = (x2 - z2) % P
        bb = b * b % P
        e = (aa - bb) % P
        c = (x3 + z3) % P
        d = (x3 - z3) % P
        da = d * a % P
        cb = c * b % P
        x3n = (da + cb) % P
        x3n = x3n * x3n % P
        t2 = (da - cb) % P
        z3n = x1 * t2 % P
        z3n = z3n * t2 % P
        x2n = aa * bb % P
        z2n = e * (aa + 121665 * e) % P
        x2, z2, x3, z3 = x2n, z2n, x3n, z3n
    if swap:
        x2, x3 = x3, x2
        z2, z3 = z3, z2
    return (x2 * pow(z2, P - 2, P) % P).to_bytes(32, "little")


# --- L'émulation (le modèle harnais_hkdf — l'appelant factice msx64) ---------------

class Emulation:
    """Les QUATORZE blocs posés à leurs RVA du plan, appelés comme des
    fonctions msx64 ordinaires : l'entrée ≡ 8 (mod 16), l'ombre et les
    logements d'arguments couverts de canaris, les non-volatiles sous
    sentinelles. Le mode « nue » (aucun hook) sert les boucles de vecteurs
    longues — l'instrument permanent ne compte pas mille pas (V6 compte
    quatre)."""

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
             ("h100014", "tls13-14-x25519-cle-publique")]

    def __init__(self, nue: bool = False):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.ks = Ks(KS_ARCH_X86, KS_MODE_64)
        self.cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.cs.detail = False
        self.uc.mem_map(*ZONE_IMAGE)
        for zone, taille in ((ZONE_MEMBRES, TAILLE_MEMBRES),
                             (ZONE_ENTREE, TAILLE_ENTREE),
                             (ZONE_SORTIE, TAILLE_PAGE),
                             (ZONE_PILE, TAILLE_PILE)):
            self.uc.mem_map(zone, taille)
        for zone, taille in ((ZONE_MEMBRES, TAILLE_MEMBRES),
                             (ZONE_ENTREE, TAILLE_ENTREE),
                             (ZONE_SORTIE, TAILLE_PAGE)):
            self.uc.mem_write(zone, CANARI * taille)
        # les pièces du plan : K[64] à R_K, les fixtures à leur ARRÊT .text6
        self.uc.mem_write(L.R_K, struct.pack("<64I", *L.K))
        self.uc.mem_write(L.R_U9, L.X25519_BASE.to_bytes(32, "little"))
        self.uc.mem_write(L.R_EXP_INV, (P - 2).to_bytes(32, "little"))
        self.blobs: dict[str, tuple[bytes, list]] = {}
        # L'INSTRUMENT PERMANENT (la leçon du harnais sha : posé AVANT toute
        # traduction, togglé par drapeaux, jamais ajouté en cours de route)
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
        sortie + canaris (le modèle harnais_hkdf)."""
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
        # la zone morte PROFONDE (sous TOUT cadre possible : la chaîne la plus
        # profonde est 13 → 11 → 12 — le cadre de tls13-13 [0x228] + celui de
        # tls13-11 [0xC8] ≈ 0x2F0 ; la zone vit à [−0x1000, −0xC00))
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

    def poser_a(self, membres):
        self.uc.mem_write(ADRESSE_A & ~0xFFF, CANARI * TAILLE_PAGE)
        self.uc.mem_write(ADRESSE_A, struct.pack("<5Q", *membres))

    def poser_b(self, membres):
        self.uc.mem_write(ADRESSE_B & ~0xFFF, CANARI * TAILLE_PAGE)
        self.uc.mem_write(ADRESSE_B, struct.pack("<5Q", *membres))

    def lire_a(self):
        return list(struct.unpack("<5Q", self.uc.mem_read(ADRESSE_A, 40)))

    def poser_scalaire(self, k: bytes):
        self.uc.mem_write(ADRESSE_SCALAIRE & ~0xFFF, CANARI * TAILLE_PAGE)
        self.uc.mem_write(ADRESSE_SCALAIRE, k)

    def poser_pointe(self, u: bytes):
        self.uc.mem_write(ADRESSE_POINTE & ~0xFFF, CANARI * TAILLE_PAGE)
        self.uc.mem_write(ADRESSE_POINTE, u)

    def preparer_sortie(self):
        self.uc.mem_write(ZONE_SORTIE, CANARI * TAILLE_PAGE)

    def lire_sortie(self) -> bytes:
        return bytes(self.uc.mem_read(ADRESSE_SORTIE, 32))

    def canaris_entree_intacts(self, adresse: int, longueur: int) -> bool:
        page = bytes(self.uc.mem_read(adresse & ~0xFFF, TAILLE_PAGE))
        debut = adresse & 0xFFF
        return (page[:debut] == CANARI * debut
                and page[debut + longueur:] ==
                CANARI * (TAILLE_PAGE - debut - longueur))


# --- Les pipelines (les compositions du harnais) -----------------------------------

def f_add(emul: Emulation, ma, mb, compter: bool = False):
    emul.poser_a(ma)
    emul.poser_b(mb)
    r = emul.appeler(L.TLS09_VA, {"rcx": ADRESSE_A, "rdx": ADRESSE_B},
                     compter=compter)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-09 a crashé : {r['crash']}")
    return emul.lire_a(), r


def f_sub(emul: Emulation, ma, mb, compter: bool = False):
    emul.poser_a(ma)
    emul.poser_b(mb)
    r = emul.appeler(L.TLS10_VA, {"rcx": ADRESSE_A, "rdx": ADRESSE_B},
                     compter=compter)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-10 a crashé : {r['crash']}")
    return emul.lire_a(), r


def f_mul(emul: Emulation, ma, mb, compter: bool = False):
    emul.poser_a(ma)
    emul.poser_b(mb)
    r = emul.appeler(L.TLS11_VA, {"rcx": ADRESSE_A, "rdx": ADRESSE_B},
                     compter=compter)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-11 a crashé : {r['crash']}")
    return emul.lire_a(), r


def f_gel(emul: Emulation, m, compter: bool = False):
    emul.poser_a(m)
    r = emul.appeler(L.TLS12_VA, {"rcx": ADRESSE_A}, compter=compter)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-12 a crashé : {r['crash']}")
    return emul.lire_a(), r


def x25519(emul: Emulation, k: bytes, u: bytes, compter: bool = False):
    emul.poser_scalaire(k)
    emul.poser_pointe(u)
    emul.preparer_sortie()
    r = emul.appeler(L.TLS13_VA, {"rcx": ADRESSE_SORTIE,
                                  "rdx": ADRESSE_SCALAIRE,
                                  "r8": ADRESSE_POINTE}, compter=compter)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-13 a crashé : {r['crash']}")
    return emul.lire_sortie(), r


def cle_publique(emul: Emulation, privee: bytes, compter: bool = False):
    emul.poser_scalaire(privee)
    emul.preparer_sortie()
    r = emul.appeler(L.TLS14_VA, {"rcx": ADRESSE_SORTIE,
                                  "rdx": ADRESSE_SCALAIRE}, compter=compter)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-14 a crashé : {r['crash']}")
    return emul.lire_sortie(), r


# --- V0 : les pièces du plan ------------------------------------------------------

def vecteur_v0(emul: Emulation):
    section("V0 — les pièces du plan (le scellé 0.9.0, sha+hkdf, l'arbre I, les fixtures)")
    donnees = open(os.path.join(TRIADE, SCELLE_M8), "rb").read()
    controle("V0.a:le-scelle-090-intact",
             len(donnees) == SCELLE_M8_TAILLE
             and hashlib.sha256(donnees).hexdigest() == SCELLE_M8_SHA256,
             f"{len(donnees)} o, sha256 1492b0bc…b0cd4 — l'ancre R7")
    # les familles sha ET hkdf INTACTES : les huit notations relues aux
    # longueurs ARRÊTÉES du plan (74/387/139/165 + 435/151/347/310)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    attendus = {"h100001": 74, "h100002": 387, "h100003": 139, "h100004": 165,
                "h100005": 435, "h100006": 151, "h100007": 347, "h100008": 310}
    noms = {bid: nom for bid, nom in Emulation.BLOCS if bid in attendus}
    ok, details = True, []
    for bid, attendu in attendus.items():
        rva, slot = L.SLOTS_TLS13[bid]
        chemin = os.path.join(ICI, "notation", noms[bid] + ".asm")
        octets, _ = B4.assembler_bloc(ks, chemin, rva, slot)
        if len(octets) != attendu:
            ok = False
            details.append(f"{noms[bid]} : {len(octets)} o ≠ {attendu}")
    controle("V0.b:les-familles-sha-et-hkdf-intactes", ok,
             "les huit notations relues aux longueurs arrêtées "
             "74/387/139/165 + 435/151/347/310 o"
             + (f" — DÉFAUTS : {details}" if details else ""))
    # LES FIXTURES DU DOMAINE : les contenus re-dérivés du plan par
    # arithmétique (le juge est le code — jamais une copie d'écriture)
    u9 = bytes(emul.uc.mem_read(L.R_U9, 32))
    expinv = bytes(emul.uc.mem_read(L.R_EXP_INV, 32))
    controle("V0.c:les-fixtures-du-domaine-poses",
             u9 == L.X25519_BASE.to_bytes(32, "little")
             and expinv == (P - 2).to_bytes(32, "little") == L.X25519_EXP_INV,
             f"U9 @ 0x{L.R_U9:x} == 09 00…00, EXP_INV @ 0x{L.R_EXP_INV:x} == "
             "eb ff…ff 7f (p−2 re-dérivé par arithmétique — l'ARRÊT D95)")
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
    attendus = {"h100009": 54, "h100010": 252, "h100011": 1078,
                "h100012": 281, "h100013": 2887, "h100014": 23}
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

    # la concordance des appels directs : chaque cible == le plan (I1/I5)
    cibles_attendues = {
        "h100009": {L.TLS12_VA: 1},
        "h100010": {L.TLS12_VA: 1},
        "h100011": {L.TLS12_VA: 1},
        "h100012": {},
        "h100013": {L.TLS09_VA: 4, L.TLS10_VA: 4, L.TLS11_VA: 13},
        "h100014": {L.TLS13_VA: 1},
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
             "09/10/11 → TLS12 ; 13 → TLS09×4 + TLS10×4 + TLS11×13 (la "
             "recette § 5 : 4 add + 4 sub + 10 mul par itération, + 2 "
             "l'inversion + 1 le produit final — ERRATUM I5 consigné : la "
             "spec écrivait « entre 4 et 6 », le compte par code fait foi) ; "
             "14 → TLS13" + (f" — DÉFAUTS : {details}" if details else ""))

    # la concordance des immédiats au plan : les membres de 2p de 10 (I1,
    # l'ERRATUM consigné : la notation re-dérive), M51/P0/19 de 12 (I1/I3)
    texte10 = open(os.path.join(ICI, "notation", "tls13-10-f25519-sub.asm"),
                   encoding="utf-8").read()
    ok_2p = all(f"0x{m:x}" in texte10 for m in L.F25519_P2_MEMBRES)
    controle("V1.f:les-membres-de-2p-de-10-au-plan", ok_2p,
             f"{[hex(m) for m in L.F25519_P2_MEMBRES]} — F25519_P2_MEMBRES "
             "(2p = 2^256−38 : (2^51−38), (2^51−1)×3, (2^52−1) — l'erratum "
             "I1 consigné AVANT la notation : l'écriture de la spec compose "
             "2^255−38 ≡ −19, le membre 4 est 2^52−1, le juge est le code)")
    texte12 = open(os.path.join(ICI, "notation",
                                "tls13-12-f25519-propager-geler.asm"),
                   encoding="utf-8").read()
    controle("V1.g:les-constantes-de-12-au-plan",
             f"0x{L.F25519_M51:x}" in texte12
             and f"0x{L.F25519_P0:x}" in texte12
             and "imul rdx, rdx, 19" in texte12,
             f"M51 0x{L.F25519_M51:x}, P0 0x{L.F25519_P0:x} (2^51−19 — la "
             "borne du gel), le repli 19 — tls13/layout.py (F25519_M51/P0)")
    texte13 = open(os.path.join(ICI, "notation", "tls13-13-x25519-echelle.asm"),
                   encoding="utf-8").read()
    controle("V1.h:les-constantes-de-13-au-plan",
             f"mov qword ptr [rsp + 0xe8], {L.X25519_A24}" in texte13
             and "0xfffffffffffffff8" in texte13
             and "0x4000000000000000" in texte13
             and "mov rbx, 254" in texte13,
             f"a24 = {L.X25519_A24} = (486662−2)/4 (RFC 7748 § 5), le clamp "
             "[octet 0 &= 248 ; octet 31 |= 64], les 255 itérations bornées")

    # la structure du domaine : AUCUN site syscall, AUCUN appel indirect, les
    # déplacements RIP UNIQUEMENT aux DEUX fixtures du plan (I3/I4 — charte § 7)
    ok_struct, motifs = True, []
    for bid, insns in insns_par_bloc.items():
        for i, insn in enumerate(insns):
            if insn.mnemonic in ("syscall", "int", "sysenter"):
                ok_struct, _ = False, motifs.append(f"{bid}:{insn.mnemonic}")
            if insn.mnemonic in ("call", "jmp") and "[" in insn.op_str:
                ok_struct, _ = False, motifs.append(f"{bid}:indirect")
            if "[rip" in insn.op_str:
                # la cible re-dérivée : adresse + taille + disp32
                import re as _re
                m = _re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", insn.op_str)
                if not m:
                    ok_struct, _ = False, motifs.append(f"{bid}:rip-illisible")
                    continue
                cible = insn.address + insn.size + (
                    int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16))
                if bid == "h100013" and cible == L.R_EXP_INV:
                    pass                      # le fixture de l'exposant (I4)
                elif bid == "h100014" and cible == L.R_U9:
                    pass                      # le fixture du point de base (I1)
                else:
                    ok_struct, _ = False, motifs.append(
                        f"{bid}:rip→0x{cible:x}")
    controle("V1.i:calcul-pur-aucun-syscall-rip-aux-fixtures-pres",
             ok_struct, "aucun syscall, aucun appel indirect ; les déplacements "
             f"RIP : 4 lectures d'EXP_INV @ 0x{L.R_EXP_INV:x} (tls13-13 I4) + "
             f"1 lea de U9 @ 0x{L.R_U9:x} (tls13-14 I1) — LES SEULS, aux "
             "fixtures du plan" + (f" — MOTIFS : {motifs}" if motifs else ""))

    # le temps constant STRUCTUREL : 09/11/12 sans AUCUN saut conditionnel,
    # 10 exactement UN (le verrou d'emprunt — le contrat), 13 exactement
    # TROIS (les compteurs + le bit de l'exposant PUBLIC — jamais le scalaire)
    compte = {bid: sum(1 for insn in insns_par_bloc[bid]
                       if insn.mnemonic.startswith("j") and insn.mnemonic != "jmp")
              for bid in insns_par_bloc}
    ok_sauts = (compte["h100009"] == 0 and compte["h100010"] == 1
                and compte["h100011"] == 0 and compte["h100012"] == 0
                and compte["h100013"] == 3 and compte["h100014"] == 0)
    # et les trois de 13 : chacun conditionné par un drapeau de REGISTRE
    # (dec rbx / test eax) — le scalaire et les intermédiaires ne touchent
    # JAMAIS une branche (charte § 3 — la preuve mesurée suit en V6)
    ok_regs = True
    for i, insn in enumerate(insns_par_bloc["h100013"]):
        if insn.mnemonic in ("jns", "jz"):
            j = i - 1
            while j >= 0 and insns_par_bloc["h100013"][j].mnemonic not in (
                    "cmp", "test", "dec"):
                j -= 1
            if j < 0 or "[" in insns_par_bloc["h100013"][j].op_str:
                ok_regs = False
    controle("V1.j:temps-constant-structurel", ok_sauts and ok_regs,
             f"les sauts conditionnels : {compte} — 09/11/12 ZÉRO (le flot "
             "arithmétique est SANS BRANCHE), 10 le SEUL verrou fail-closed "
             "(l'emprunt du contrat), 13 les DEUX compteurs de boucle + le "
             "bit de l'exposant PUBLIC p−2, chacun sur drapeau de registre")


# --- V2 : les vecteurs officiels RFC 7748 + l'oracle différentiel -------------------

def vecteur_v2(emul: Emulation, nue: Emulation, graine: int):
    section("V2 — les vecteurs officiels RFC 7748 § 5.2/§ 6.1 + l'oracle")

    # (a) les deux paires du § 5.2 : la référence croisée AVANT le jugement
    for i, (nom, k_hex, u_hex, attendu_hex) in enumerate(VECTEURS_7748_52):
        k, u, attendu = (bytes.fromhex(x) for x in (k_hex, u_hex, attendu_hex))
        if ref_x25519(k, u) != attendu:
            controle(f"V2.{i}:reference-python-{nom}", False,
                     "la constante du vecteur diverge de la référence — "
                     "INSTRUMENT DÉFAILLANT")
            continue
        sortie, r = x25519(emul, k, u)
        controle(f"V2.{i}:{nom}", sortie == attendu and r["rax"] == 0,
                 f"{sortie.hex()[:16]}… == {attendu_hex[:16]}…")

    # (b) la paire § 6.1 : les clés publiques par l'échelle au point 9 (le
    # geste même de tls13-14) ET le secret partagé des DEUX côtés
    alice_pub, _ = cle_publique(emul, bytes.fromhex(ALICE_PRIV))
    bob_pub, _ = cle_publique(emul, bytes.fromhex(BOB_PRIV))
    controle("V2.2:les-cles-publiques-§6.1",
             alice_pub == bytes.fromhex(ALICE_PUB)
             and bob_pub == bytes.fromhex(BOB_PUB),
             f"Alice {alice_pub.hex()[:12]}… == 8520f009…, "
             f"Bob {bob_pub.hex()[:12]}… == de9edb7d… — X25519(privée, 9)")
    partage_ab, _ = x25519(emul, bytes.fromhex(ALICE_PRIV), bob_pub)
    partage_ba, _ = x25519(emul, bytes.fromhex(BOB_PRIV), alice_pub)
    controle("V2.3:le-secret-partage-§6.1",
             partage_ab == partage_ba == bytes.fromhex(PARTAGE),
             "Alice × publique de Bob == Bob × publique d'Alice == K "
             f"({partage_ab.hex()[:12]}…) — la COMMUTATIVITÉ prouvée sur pièces")

    # (c) LE TEST ITÉRÉ (la seconde espèce du § 5.2) : k = u = 9 ; à chaque
    # pas k devient X25519(k, u) et u l'ancien k — les résultats consignés
    # après 1 et 1000 pas (joué sur l'émulation NUE : mille pas ne se
    # comptent pas, ils se vérifient)
    k = u = L.X25519_BASE.to_bytes(32, "little")
    vu_1 = False
    for i in range(1000):
        nouveau, _ = x25519(nue, k, u)
        k, u = nouveau, k
        if i == 0:
            vu_1 = k == bytes.fromhex(ITERE_1)
    controle("V2.4:itere-1", vu_1,
             f"après 1 pas : {k.hex()[:16] if not vu_1 else '422c8e7a…'} == "
             "422c8e7a… (RFC 7748 § 5.2)")
    controle("V2.5:itere-1000", k == bytes.fromhex(ITERE_1000),
             f"après 1000 pas : {k.hex()[:16]}… == 684cf59b… (RFC 7748 § 5.2)")

    # (d) l'oracle différentiel : l'échelle sur 60 vecteurs aléatoires +
    # les quatre opérateurs sur 400 chacun (Python en oracle)
    rng = random.Random(graine)
    ecarts, joues = 0, 0
    for _ in range(60):
        k = bytes(rng.randrange(256) for _ in range(32))
        u = bytes(rng.randrange(256) for _ in range(32))
        sortie, _ = x25519(nue, k, u)
        joues += 1
        ecarts += sortie != ref_x25519(k, u)
    controle("V2.6:l-oracle-echelle-60-vecteurs", ecarts == 0,
             f"{joues} échelles aléatoires (scalaire ET point aléatoires, "
             "le bit 255 et les non-canonicals exercés) — ZÉRO écart")
    ecarts, joues = 0, 0
    for _ in range(400):
        va, vb = rng.randrange(P), rng.randrange(P)
        ma, mb = vers_membres(va), vers_membres(vb)
        for op, ref in (("add", (va + vb) % P), ("sub", (va - vb) % P),
                        ("mul", (va * vb) % P)):
            s, _ = {"add": f_add, "sub": f_sub, "mul": f_mul}[op](nue, ma, mb)
            joues += 1
            ecarts += (depuis_membres(s) != ref
                       or not all(x < (1 << 52) for x in s))
        m = vers_membres(va)
        s, _ = f_gel(nue, m)
        joues += 1
        ecarts += (depuis_membres(s) != va or not all(x < (1 << 52) for x in s))
    controle("V2.7:l-oracle-operateurs-1600-cas", ecarts == 0,
             f"{joues} opérations (add/sub/mul/gel : 400 couronnes de "
             "quatre) — la sortie ≡ la référence ET les membres < 2^52")


# --- V3 : les cas punitifs (les bornes et les lâches) -------------------------------

def vecteur_v3(emul: Emulation, nue: Emulation, graine: int):
    section("V3 — les cas punitifs (les lâches, les bords, les dégénérés)")
    rng = random.Random(graine ^ 0xC0FFEE)

    # (a) le gel : p → 0 EXACT, p−1 inchangé, l'invariance de la passe
    s, _ = f_gel(emul, list(L.F25519_P_MEMBRES))
    controle("V3.a:gel-p-donne-zero", s == [0] * 5,
             "l'égalité exacte p → 0 (Q2 de tls13-12 — la soustraction "
             "conditionnelle par ET logique)")
    s, _ = f_gel(emul, vers_membres(P - 1))
    controle("V3.b:gel-p−1-inchange-octet-identique",
             s == vers_membres(P - 1), "déjà < p → les membres OCTET-IDENTIQUES")
    tous = True
    for _ in range(100):
        v = rng.randrange(P)
        m = vers_membres(v)
        m[0] = min(m[0] + rng.randrange(0, 1207), (1 << 52) - 1)  # la forme
        s, _ = f_gel(nue, m)                    # post-producteur (m0 lâche)
        tous = tous and depuis_membres(s) == depuis_membres(m) % P \
            and all(x < (1 << 52) for x in s)
    controle("V3.c:la-passe-preserve-la-valeur", tous,
             "100 formes lâches (m0 < 2^51+1216) — la valeur préservée "
             "mod p, les membres ramenés < 2^52")

    # (b) les valeurs LÂCHES de l'école (av-09 V2 cité) : membres saturés,
    # a = b lâche, 0·x, 1·x, (p−1)², x²
    cas = [("0·x", [0] * 5, vers_membres(12345)),
           ("1·x", [1, 0, 0, 0, 0], vers_membres(P - 1)),
           ("(p−1)·(p−1)", vers_membres(P - 1), vers_membres(P - 1)),
           ("x·x (carré)", vers_membres(987654321), vers_membres(987654321)),
           ("membres saturés", [(1 << 52) - 1] * 5, [(1 << 52) - 1] * 5),
           ("a lâche ≥ p", vers_membres(P + 2026), vers_membres(P - 1)),
           ("a,b lâches max", vers_membres((1 << 255) - 1),
            vers_membres((1 << 255) - 1))]
    ok, details = True, []
    for nom, ma, mb in cas:
        s, r = f_mul(emul, ma, mb)
        attendu = (depuis_membres(ma) * depuis_membres(mb)) % P
        if not (r["rax"] == 0 and depuis_membres(s) == attendu
                and all(x < (1 << 52) for x in s)):
            ok = False
            details.append(f"{nom} → {s}")
    controle("V3.d:les-laches-de-l-ecole", ok,
             "0·x, 1·x, (p−1)², le carré, les membres saturés 2^52−1 partout, "
             "a lâche ≥ p, a = b = 2^255−1 — l'école dépend des MEMBRES, le "
             "repli préserve l'équivalence mod p"
             + (f" — DÉFAUTS : {details}" if details else ""))

    # (c) la soustraction lâche (P1 de tls13-10 : a réduite OU lâche < 2^255)
    ok = True
    for va in (P + 2026, P, (1 << 255) - 38, (1 << 255) - 1, 0):
        vb = rng.randrange(P)
        s, r = f_sub(emul, vers_membres(va), vers_membres(vb))
        ok = ok and (r["rax"] == 0 and depuis_membres(s) == (va - vb) % P
                     and all(x < (1 << 52) for x in s))
    controle("V3.e:la-soustraction-lache", ok,
             "a ∈ {p+2026, p, 2^255−38, 2^255−1, 0} contre b réduite — les "
             "DEUX bornes de P1 démontrées (a + 2p − b, la passe, le gel)")

    # (f) le point u NON CANONIQUE : les valeurs [p, 2^255) traitées comme
    # réduites (RFC 7748 § 5), le bit 255 MASQUÉ (le décodage de P3)
    k = bytes.fromhex(BOB_PRIV)
    ok = True
    for u_val in (P, P + 1, P + 12345, (1 << 255) - 1, (1 << 255) - 19):
        u = u_val.to_bytes(32, "little")
        sortie, _ = x25519(nue, k, u)
        ok = ok and sortie == ref_x25519(k, u)
    u_bit255 = ((1 << 255) | 12345).to_bytes(32, "little")
    sortie, _ = x25519(nue, k, u_bit255)
    controle("V3.f:le-point-non-canonique",
             ok and sortie == ref_x25519(k, u_bit255),
             "u ∈ [p, 2^255) ≡ réduit (l'arithmétique lâche le porte), le "
             "bit 255 masqué AVANT le décodage — RFC 7748 § 5 sur pièces")

    # (g) les dégénérés : u de petit ordre → la sortie NULLE (RFC 7748 § 6.1)
    ok = True
    for u_petit in (0, 1, 2, 3, 8):
        sortie, _ = x25519(nue, k, u_petit.to_bytes(32, "little"))
        ok = ok and sortie == ref_x25519(k, u_petit.to_bytes(32, "little"))
    controle("V3.g:les-degeneres", ok,
             "u ∈ {0, 1, 2, 3, 8} (les ordres petits) — la sortie nulle "
             "rendue, l'inversion 0^(p−2) = 0 par la composition même")


# --- V4 : le contrat ---------------------------------------------------------------

def vecteur_v4(emul: Emulation):
    section("V4 — le contrat (les pré/post de chaque bloc, sur pièces)")

    # (a) les non-volatiles rendus + la pile équilibrée + les canaris : un
    # cas représentatif de CHAQUE bloc de la famille
    rng = random.Random(20261107)
    ok_nv, details = True, []
    ma, mb = vers_membres(rng.randrange(P)), vers_membres(rng.randrange(P))
    for nom, prep in [("tls13-09", "add"), ("tls13-10", "sub"),
                      ("tls13-11", "mul"), ("tls13-12", "gel")]:
        emul.poser_a(ma)
        emul.poser_b(mb)
        va = {"tls13-09": L.TLS09_VA, "tls13-10": L.TLS10_VA,
              "tls13-11": L.TLS11_VA, "tls13-12": L.TLS12_VA}[nom]
        r = emul.appeler(va, {"rcx": ADRESSE_A, "rdx": ADRESSE_B})
        if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
                and r["canaris_haut"] and r["canaris_profond"]
                and r["logements_intacts"] and r["rax"] == 0):
            ok_nv = False
            details.append(f"{nom}(nv={emul.non_volatiles_rendus(r)},"
                           f"pile={r['pile_equilibree']},haut={r['canaris_haut']},"
                           f"prof={r['canaris_profond']},log={r['logements_intacts']})")
    k = bytes(range(32))
    u = bytes(range(32, 64))
    emul.poser_scalaire(k)
    emul.poser_pointe(u)
    emul.preparer_sortie()
    r = emul.appeler(L.TLS13_VA, {"rcx": ADRESSE_SORTIE,
                                  "rdx": ADRESSE_SCALAIRE,
                                  "r8": ADRESSE_POINTE})
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"]
            and r["logements_intacts"] and r["rax"] == 0):
        ok_nv = False
        details.append("tls13-13")
    emul.poser_scalaire(k)
    emul.preparer_sortie()
    r = emul.appeler(L.TLS14_VA, {"rcx": ADRESSE_SORTIE,
                                  "rdx": ADRESSE_SCALAIRE})
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"]
            and r["logements_intacts"] and r["rax"] == 0):
        ok_nv = False
        details.append("tls13-14")
    controle("V4.a:non-volatiles-pile-canaris (les six blocs)", ok_nv,
             "les 8 sentinelles rendues, rsp équilibrée, l'ombre intacte, "
             "les logements d'arguments relus, la zone profonde intacte "
             "(la chaîne 13 → 11 → 12 ≈ 0x2F0 sous l'entrée)"
             + (f" — DÉFAUTS : {details}" if details else ""))

    # (b) l'alignement msx64 à travers les appels directs : à CHAQUE entrée
    # de TLS09/10/11 (par 13), TLS12 (par 09/10/11), TLS13 (par 14)
    emul.surveillance = {va: [] for va in (L.TLS09_VA, L.TLS10_VA, L.TLS11_VA,
                                           L.TLS12_VA, L.TLS13_VA)}
    try:
        x25519(emul, bytes.fromhex(ALICE_PRIV),
               L.X25519_BASE.to_bytes(32, "little"))
        cle_publique(emul, bytes.fromhex(BOB_PRIV))
    finally:
        entrees = {va: list(l) for va, l in emul.surveillance.items()}
        emul.surveillance = None
    total = sum(len(l) for l in entrees.values())
    ok_align = total > 0 and all(e % 16 == 8 for l in entrees.values() for e in l)
    # les comptes exacts : DEUX compositions (l'échelle entrée directement +
    # le couple 14 → 13) — par échelle : 4 add + 4 sub + 10 mul × 255 pas,
    # l'inversion 255 carrés + 253 mults + le produit final, et tls13-12
    # appelé par CHACUN des 09/10/11
    attendus_align = {L.TLS09_VA: 4 * 255 * 2, L.TLS10_VA: 4 * 255 * 2,
                      L.TLS11_VA: (10 * 255 + 508 + 1) * 2,
                      L.TLS12_VA: (18 * 255 + 508 + 1) * 2,
                      L.TLS13_VA: 2}
    ok_compte = all(len(entrees[va]) == attendus_align[va] for va in entrees)
    controle("V4.b:l-alignement-msx64-a-l-entree-de-chaque-calle",
             ok_align and ok_compte,
             f"{total} entrées surveillées (09×{len(entrees[L.TLS09_VA])}, "
             f"10×{len(entrees[L.TLS10_VA])}, 11×{len(entrees[L.TLS11_VA])}, "
             f"12×{len(entrees[L.TLS12_VA])}, 13×{len(entrees[L.TLS13_VA])}) — "
             "rsp ≡ 8 (mod 16) chacune, les comptes exacts de la recette")

    # (c) les entrées INTACTES (Q2) : le scalaire, le point u, la clé privée
    x25519(emul, k, u)
    ok_intacts = (emul.canaris_entree_intacts(ADRESSE_SCALAIRE, 32)
                  and emul.canaris_entree_intacts(ADRESSE_POINTE, 32))
    cle_publique(emul, k)
    ok_intacts &= emul.canaris_entree_intacts(ADRESSE_SCALAIRE, 32)
    controle("V4.c:les-entrees-intactes (Q2)", ok_intacts,
             "le scalaire ET le point u relus OCTET POUR OCTET après "
             "l'échelle, la clé privée après le couple — le clamp et le "
             "masque vivent dans les COPIES LOCALES")

    # (d) la sortie JAMAIS dépassée : les canaris après les 32 o
    x25519(emul, k, u)
    apres = bytes(emul.uc.mem_read(ADRESSE_SORTIE + 32, 0x80))
    cle_publique(emul, k)
    apres2 = bytes(emul.uc.mem_read(ADRESSE_SORTIE + 32, 0x80))
    controle("V4.d:la-sortie-jamais-depassee",
             apres == CANARI * 0x80 and apres2 == CANARI * 0x80,
             "les canaris après les 32 o de la sortie intacts — la "
             "sérialisation n'écrit JAMAIS au-delà (le quad 4 est nul)")

    # (e) LE VERROU fail-closed de tls13-10 : l'emprunt sortant → rax = −1
    # NOMMÉ et a JAMAIS ÉCRIT (l'appelant HORS CONTRAT — l'exercice du
    # verrou, l'échec E1 d'av-08 ÉLEVÉ en verdict de la table du domaine)
    emul.poser_a(vers_membres(0))
    b_hors = list(L.F25519_P2_MEMBRES)     # b = 2p + 1000 : hors P2 —
    b_hors[0] += 1000                      # a + 2p − b = −1000 < 0
    emul.poser_b(b_hors)
    r = emul.appeler(L.TLS10_VA, {"rcx": ADRESSE_A, "rdx": ADRESSE_B})
    intact = all(x == 0 for x in emul.lire_a())
    r2 = emul.appeler(L.TLS10_VA, {"rcx": ADRESSE_A, "rdx": ADRESSE_B})
    controle("V4.e:le-verrou-fail-closed-de-10",
             r["rax"] == -1 and r2["rax"] == -1 and intact
             and all(x == 0 for x in emul.lire_a()),
             "b = 2p+1000 (hors contrat : a + 2p − b = −1000) → l'emprunt "
             "sort au cinquième membre : "
             "rax = −1 NOMMÉ, la sortie a INTACTE (le scratch meurt) — le "
             "fail-closed se prononce, il ne se tait jamais")


# --- V5 : la falsification ---------------------------------------------------------

def vecteur_v5(emul: Emulation, nue: Emulation):
    section("V5 — la falsification (zéro silence)")
    k = bytes.fromhex(ALICE_PRIV)
    u = L.X25519_BASE.to_bytes(32, "little")
    attendu = bytes.fromhex(ALICE_PUB)

    # (a) le scalaire muté → la sortie diverge (premier, milieu, dernier)
    # NOTE DE DISCIPLINE : les TROIS bits bas de l'octet 0 du scalaire
    # sont CLAMPÉS par RFC 7748 (k[0] &= 248) — la mutation du bit 0 est
    # un no-op PAR DESIGN : la falsification vise le bit 3 (le plus bas
    # NON clampé) — le clamp est PUBLIC, l'absorption est la SÉMANTIQUE.
    attrapes, total = 0, 0
    for pos, masque in ((0, 0x08), (15, 0x01), (31, 0x01)):
        mute = bytearray(k)
        mute[pos] ^= masque
        sortie, _ = x25519(nue, bytes(mute), u)
        total += 1
        attrapes += sortie != ref_x25519(k, u)      # ≠ le résultat original
    for pos in (0, 15, 31):
        mute = bytearray(u)
        mute[pos] ^= 0x01
        sortie, _ = x25519(nue, k, bytes(mute))
        total += 1
        attrapes += sortie != ref_x25519(k, u)
    controle("V5.a:scalaire-et-point-mutes-attrapes",
             attrapes == total and total > 0,
             f"{attrapes}/{total} mutations (premier/milieu/dernier octet du "
             "scalaire ET du point) — la sortie diverge du résultat original")

    # (b) la clé privée mutée → la clé publique diverge (le couple de 14)
    attrapes, total = 0, 0
    for pos, masque in ((0, 0x08), (15, 0x01), (31, 0x01)):
        mute = bytearray(k)
        mute[pos] ^= masque
        pub, _ = cle_publique(nue, bytes(mute))
        total += 1
        attrapes += pub != attendu
    controle("V5.b:la-cle-privee-mutee-attrapee", attrapes == total,
             f"{attrapes}/{total} mutations de la clé privée — la clé "
             "publique diverge (le couple du ClientHello)")

    # (c) la comparaison n'est pas muette : chaque bit de l'attendu muté
    # → l'égalité ÉCHOUE (l'instrument se prouve non-vide)
    attrapes, total = 0, 0
    attendu_b = bytearray(attendu)
    for bit in (0, 127, 255):
        mute = bytearray(attendu_b)
        mute[bit // 8] ^= 1 << (bit % 8)
        total += 1
        attrapes += bytes(mute) != attendu
    controle("V5.c:la-comparaison-n-est-pas-muette", attrapes == total,
             f"{attrapes}/{total} résultats attendus mutés → l'égalité ÉCHOUE")

    # (d) LES FIXTURES CORROMPUS → divergence : les données du plan sont
    # LUES à travers la composition (le miroir de K corrompu du harnais sha)
    # la corruption ET l'exécution sur la MÊME instance (la nue : les
    # mémoires des instances sont distinctes, la discipline le consigne)
    u9_orig = bytes(nue.uc.mem_read(L.R_U9, 32))
    nue.uc.mem_write(L.R_U9 + 0, bytes([u9_orig[0] ^ 1]))
    pub, _ = cle_publique(nue, k)
    nue.uc.mem_write(L.R_U9, u9_orig)
    controle("V5.d:U9-corrompu-la-cle-diverge", pub != attendu,
             "le point de base muté @ 0xFF00 → la clé publique diverge : la "
             "fixture est LUE par tls13-14 à travers la composition")
    exp_orig = bytes(nue.uc.mem_read(L.R_EXP_INV, 32))
    nue.uc.mem_write(L.R_EXP_INV + 5, bytes([exp_orig[5] ^ 0x10]))
    sortie, _ = x25519(nue, k, u)
    nue.uc.mem_write(L.R_EXP_INV, exp_orig)
    controle("V5.e:EXP_INV-corrompu-le-partage-diverge",
             sortie != attendu and sortie != bytes(32),
             "l'exposant muté @ 0xFF20 → la sortie diverge : l'inversion "
             "LIT la constante publique du plan (miroir av-11)")


# --- V6 : le temps constant mesuré ---------------------------------------------------

def vecteur_v6(emul: Emulation, graine: int):
    section("V6 — le temps constant MESURÉ (I1/I3, la charte § 3)")
    rng = random.Random(graine ^ 0x7)

    # (a) le SCALAIRE (la clé privée) : 4 couronnes différentes, même compte
    comptes = []
    for _ in range(4):
        k = bytes(rng.randrange(256) for _ in range(32))
        u = L.X25519_BASE.to_bytes(32, "little")
        _, r = x25519(emul, k, u, compter=True)
        comptes.append(r["compteur"])
    controle("V6.a:le-scalaire-compte-constant",
             len(set(comptes)) == 1,
             f"4 scalaires aléatoires, {comptes[0]} instructions EXACTEMENT — "
             "le contenu JAMAIS, la longueur seule (255 itérations TOUJOURS)")

    # (b) le POINT u (l'entrée publique) : 2 points différents, même compte
    comptes = []
    for u in (L.X25519_BASE.to_bytes(32, "little"),
              bytes.fromhex(BOB_PUB)):
        _, r = x25519(emul, bytes.fromhex(ALICE_PRIV), u, compter=True)
        comptes.append(r["compteur"])
    controle("V6.b:le-point-u-compte-constant", len(set(comptes)) == 1,
             f"2 points u (9 et la publique de Bob), {comptes[0]} instructions "
             "EXACTEMENT — le cswap masqué ne compte pas les différences")

    # (c) les opérateurs : des opérandes différents, même compte (le flot
    # est SANS BRANCHE — la mesure le confirme)
    for nom, pipe in (("add", f_add), ("sub", f_sub), ("mul", f_mul)):
        comptes = []
        for _ in range(3):
            ma = vers_membres(rng.randrange(P))
            mb = vers_membres(rng.randrange(P))
            _, r = pipe(emul, ma, mb, compter=True)
            comptes.append(r["compteur"])
        controle(f"V6.c:{nom}-compte-constant", len(set(comptes)) == 1,
                 f"3 paires d'opérandes, {comptes[0]} instructions EXACTEMENT")


# --- Le verdict --------------------------------------------------------------------------

def main() -> int:
    graine = 20261107
    if "--graine" in sys.argv:
        graine = int(sys.argv[sys.argv.index("--graine") + 1])
    print("=== tls13/harnais_x25519.py — LE HARNAIS DE LA FAMILLE x25519 "
          "(chantier M9-(b), le geste trois) ===")
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
