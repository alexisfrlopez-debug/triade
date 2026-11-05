#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tls13/harnais_sha.py — LE HARNAIS DE LA FAMILLE sha DU DOMAINE tls13.

Chantier M9-(b), premier geste : les blocs tls13-01..04 (les miroirs win
msx64 des contrats ah-04..07 de M6) NOTÉS-MESURÉS-PROUVÉS. Le modèle est le
harnais M8 (m8/harnais_sys.py, D161) : l'émulation nue à les RVA du plan
(mécanisme D79), l'appelant factice pose les sentinelles non volatiles et
les canaris, le verdict est TRANCHÉ par le code — jamais cru.

LE CAHIER (le miroir M8-(b), la charte § 2 : les vecteurs officiels AVANT
usage, la falsification, zéro silence) :

  V0 — LES PIÈCES DU PLAN : le scellé 0.9.0 relu (l'ancre 1492b0bc…), la
       zone .rdata RVA 0x2F00-0x2FFF VIERGE sur pièces (la réserve M8 qui
       reçoit K[64]), les fixtures M8 intacts (la frontière tenue) ;
  V1 — LE ROUND-TRIP + LA CONCORDANCE : chaque notation ré-assemblée en ses
       octets (keystone == capstone, R5), les H0 de tls13-01 == le plan, le
       déplacement RIP de tls13-02 == R_K, les appels de 03/04 == TLS02_VA,
       les constantes DÉRIVÉES PAR ARITHMÉTIQUE (H0 : racines carrées, K :
       racines cubiques des premiers — le juge est le code), la structure
       du domaine (AUCUN site syscall, AUCUN appel indirect) et le temps
       constant STRUCTUREL de tls13-02 (aucune branche ne lit les données) ;
  V2 — LES VECTEURS OFFICIELS FIPS 180-4 : le vide (N=0), « a », « abc »,
       les DEUX messages longs NIST (448/896 bits — la borne .deux exercée)
       — le condensé OCTET POUR OCTET, la compression SEULE à découvert sur
       le bloc bourré de « abc », la référence hashlib CROISÉE ;
  V3 — L'INVARIANCE DE DÉCOUPAGE (Q2 de tls13-03) : le même message absorbé
       en un appel, octet par octet, par 3, par 63/64/65, par 7, par 13 ;
  V4 — LE CONTRAT : N=0 légal (rien ne bouge), le bloc d'entrée INTACT
       (Q2 de tls13-02), les données INTACTES (Q3 de tls13-03), les
       non-volatiles rendus, rax = 0 (Q3/Q4), l'alignement msx64 à l'entrée
       de l'appelé à travers l'appel direct (le point de vue du CALLE),
       l'ombre et la pile de l'appelant intacts, le contexte clos DÉTECTÉ ;
  V5 — LA FALSIFICATION (zéro silence) : chaque vecteur muté (premier,
       milieu, dernier bit du message) ATTRAPÉ, la comparaison n'est pas
       muette (chaque bit du condensé attendu muté ÉCHOUE), K corrompu →
       divergence (la table est LUE), H0 corrompu → divergence, le total
       corrompu → divergence (le bourrage en dépend) ;
  V6 — LE TEMPS CONSTANT MESURÉ (I3 de tls13-02) : le compte d'instructions
       IDENTIQUE pour des données arbitraires différentes — la compression
       seule et la pipeline entière.

Usage : python3 harnais_sha.py            # le cahier complet
        python3 harnais_sha.py --graine N # la graine du générateur (défaut 20261105)
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
import os
import random
import re
import struct
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
# lecteur canonique des notations, le même outil qui scella M4..M8), importée
# par chemin (leçon D158) — ses répertoires ouverts au sys.path AVANT exec.
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

ZONE_IMAGE = (0x1000, 0xE000)   # .rdata (K @0x2F00) + .text5 + .text6 préfigurée
RET_MAGIQUE = 0xDE00            # dans la réserve .text6 — jamais exécuté
ZONE_CTX = 0x500000             # les contextes SHA (112 o, canaris autour)
ZONE_ENTREE = 0x600000          # les messages (canaris autour)
ZONE_SORTIE = 0x700000          # les condensés (32 o, canaris autour)
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP0 = 0x7F008000
ENTREE_RSP = RSP0 - 0x108       # ≡ 8 (mod 16) — le point de vue de l'APPELÉ

OFF_CTX = 0x100                 # le contexte dans sa page
OFF_ENTREE = 0x100              # le message dans sa page
OFF_SORTIE = 0x100              # le condensé dans sa page
TAILLE_PAGE = 0x1000

ADRESSE_CTX = ZONE_CTX + OFF_CTX
ADRESSE_ENTREE = ZONE_ENTREE + OFF_ENTREE
ADRESSE_SORTIE = ZONE_SORTIE + OFF_SORTIE

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
SCELLE_M8_FIXTURE_NOM = b"NtWriteFile"          # @RVA 0x2EC0 (raw 0x22C0)
SCELLE_M8_FIXTURE_LIGNE = b"TRIADE M0 : Hello, Windows 11 !\r\n\x00"  # @0x2ED0

# --- Les vecteurs officiels FIPS 180-4 (la § citée par tls13-02 Q1 / tls13-04 I5) --

VECTEURS = [
    ("le vide (N=0 — P3 de tls13-03)", b"",
     "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("« a » (un octet — I5 de tls13-04)", b"a",
     "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"),
    ("« abc » (le message d'un bloc)", b"abc",
     "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
    ("448 bits (la borne .deux exercée)",
     b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
     "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
    ("896 bits (multi-blocs)",
     b"abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmno"
     b"ijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu",
     "cf5b16a778af8380036ce59e7b0492370b249b11e8f07a51afac45037afee9d1"),
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


# --- Les constantes DÉRIVÉES PAR ARITHMÉTIQUE (le juge est le code) --------------

def _premiers(n: int) -> list[int]:
    out: list[int] = []
    c = 2
    while len(out) < n:
        if all(c % p for p in out if p * p <= c):
            out.append(c)
        c += 1
    return out


def _icbrt(n: int) -> int:
    """Racine cubique entière exacte par Newton (convergence par le haut)."""
    if n < 8:
        return 1 if n < 8 else 2
    x = 1 << ((n.bit_length() + 2) // 3 + 1)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            return x
        x = y


def deriv_H0() -> list[int]:
    """FIPS 180-4 § 5.3.1 : parties fractionnaires des racines CARRÉES des
    8 premiers premiers — floor(sqrt(p)·2^32) = isqrt(p·2^64), mod 2^32."""
    return [math.isqrt(p << 64) & 0xFFFFFFFF for p in _premiers(8)]


def deriv_K() -> list[int]:
    """FIPS 180-4 § 4.2.2 : parties fractionnaires des racines CUBIQUES des
    64 premiers premiers — floor(cbrt(p)·2^32) = icbrt(p·2^96), mod 2^32."""
    return [_icbrt(p << 96) & 0xFFFFFFFF for p in _premiers(64)]


# --- L'émulation (le modèle m8/harnais_sys.py — l'appelant factice msx64) --------

class Emulation:
    """Les quatre blocs posés à leurs RVA du plan, appelés comme des
    fonctions msx64 ordinaires : l'entrée ≡ 8 (mod 16), l'ombre et la pile
    de l'appelant couvertes de canaris, les non-volatiles sous sentinelles."""

    def __init__(self):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.ks = Ks(KS_ARCH_X86, KS_MODE_64)
        self.cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.cs.detail = False
        self.uc.mem_map(*ZONE_IMAGE)
        self.uc.mem_map(ZONE_CTX, TAILLE_PAGE)
        self.uc.mem_map(ZONE_ENTREE, TAILLE_PAGE)
        self.uc.mem_map(ZONE_SORTIE, TAILLE_PAGE)
        self.uc.mem_map(ZONE_PILE, TAILLE_PILE)
        for zone in (ZONE_CTX, ZONE_ENTREE, ZONE_SORTIE):
            self.uc.mem_write(zone, CANARI * TAILLE_PAGE)
        # la table K[64] posée à R_K dans la .rdata du plan (source unique)
        self.uc.mem_write(L.R_K, struct.pack("<64I", *L.K))
        self.blobs: dict[str, tuple[bytes, list[dict]]] = {}
        # L'INSTRUMENT PERMANENT (la leçon du premier passage V4/V6 : unicorn
        # attache les hooks à la TRADUCTION des blocs — un bloc déjà exécuté
        # est en cache et ne déclenche JAMAIS un hook posé après coup ; le
        # comptage et la surveillance d'entrée vivent donc ICI, posés AVANT
        # toute traduction, togglés par drapeaux — jamais ajoutés en cours
        # de route, miroir de reposer_bloc/ctl_remove_cache du harnais M8).
        self.compteur_actif = False
        self.compteur = 0
        self.entrees_tls02: list[int] | None = None
        self.uc.hook_add(UC_HOOK_CODE, self._instrument)
        self.poser_blocs()

    def _instrument(self, uc, adresse, taille, donnees):
        """Le hook UNIQUE, permanent : compte les instructions quand le
        drapeau est levé, surveille les entrées de tls13-02 quand on le dit."""
        if self.compteur_actif:
            self.compteur += 1
        if self.entrees_tls02 is not None and adresse == L.TLS02_VA:
            self.entrees_tls02.append(uc.reg_read(UC_X86_REG_RSP))

    def poser_blocs(self):
        for bid, nom in [("h100001", "tls13-01-sha256-init"),
                         ("h100002", "tls13-02-sha256-comprimer"),
                         ("h100003", "tls13-03-sha256-absorber"),
                         ("h100004", "tls13-04-sha256-finaliser")]:
            rva, slot = L.SLOTS_TLS13[bid]
            chemin = os.path.join(ICI, "notation", nom + ".asm")
            octets, metas = B4.assembler_bloc(self.ks, chemin, rva, slot)
            self.uc.mem_write(rva, octets)
            self.blobs[bid] = (octets, metas)

    def appeler(self, va: int, args: dict[str, int] | None = None,
                compter: bool = False):
        """Appelle un bloc comme une fonction msx64. Retourne le dict des
        registres de sortie + canaris + compteur d'instructions (si demandé)."""
        uc = self.uc
        for nom, val in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], val)
        for nom, val in (args or {}).items():
            uc.reg_write(REGS[nom], val)
        uc.reg_write(UC_X86_REG_RAX, 0)
        rsp = ENTREE_RSP
        uc.reg_write(UC_X86_REG_RSP, rsp)
        # les canaris : l'ombre + les loges + la pile de l'APPELANT au-dessus
        uc.mem_write(rsp + 8, CANARI * 0x170)
        # la zone morte PROFONDE (sous tout cadre possible : max ≈ 0x220)
        uc.mem_write(rsp - 0x800, CANARI * 0x400)
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
                    "compteur": self.compteur}
        finally:
            self.compteur_actif = False
        sortie = {k: uc.reg_read(REGS[k]) for k in REGS}
        sortie["rax"] = s64(sortie["rax"])
        sortie["entree_rsp"] = entree_rsp
        sortie["crash"] = None
        sortie["compteur"] = self.compteur
        sortie["pile_equilibree"] = uc.reg_read(REGS["rsp"]) == entree_rsp + 8
        sortie["canaris_haut"] = bytes(
            uc.mem_read(entree_rsp + 8, 0x170)) == CANARI * 0x170
        sortie["canaris_profond"] = bytes(
            uc.mem_read(entree_rsp - 0x800, 0x400)) == CANARI * 0x400
        return sortie

    def non_volatiles_rendus(self, r: dict) -> bool:
        return all(r[nom] == SENTINELLES_NV[nom] for nom in SENTINELLES_NV)

    # --- les zones canaris ---------------------------------------------------

    def preparer_ctx(self):
        self.uc.mem_write(ADRESSE_CTX, CANARI * L.SHA_CTX)

    def preparer_sortie(self):
        self.uc.mem_write(ADRESSE_SORTIE, CANARI * L.SHA_TAILLE_CONDENSE)

    def poser_message(self, message: bytes):
        self.uc.mem_write(ADRESSE_ENTREE, CANARI * 0x400)
        self.uc.mem_write(ADRESSE_ENTREE, message)

    def lire_ctx(self) -> bytes:
        return bytes(self.uc.mem_read(ADRESSE_CTX, L.SHA_CTX))

    def lire_digest(self) -> bytes:
        return bytes(self.uc.mem_read(ADRESSE_SORTIE, L.SHA_TAILLE_CONDENSE))

    def canaris_ctx_intacts(self) -> bool:
        page = bytes(self.uc.mem_read(ZONE_CTX, TAILLE_PAGE))
        return (page[:OFF_CTX] == CANARI * OFF_CTX
                and page[OFF_CTX + L.SHA_CTX:] == CANARI * (TAILLE_PAGE - OFF_CTX - L.SHA_CTX))

    def canaris_sortie_intacts(self) -> bool:
        page = bytes(self.uc.mem_read(ZONE_SORTIE, TAILLE_PAGE))
        return (page[:OFF_SORTIE] == CANARI * OFF_SORTIE
                and page[OFF_SORTIE + 32:] == CANARI * (TAILLE_PAGE - OFF_SORTIE - 32))

    def canaris_entree_intacts(self, longueur: int) -> bool:
        page = bytes(self.uc.mem_read(ZONE_ENTREE, TAILLE_PAGE))
        return (page[:OFF_ENTREE] == CANARI * OFF_ENTREE
                and page[OFF_ENTREE + longueur:] ==
                CANARI * (TAILLE_PAGE - OFF_ENTREE - longueur))


# --- La pipeline : init → absorb → finalise (le découpage en argument) -----------

def hacher(emul: Emulation, message: bytes, decoupage: int | None = None,
           compter: bool = False) -> tuple[bytes, dict]:
    """Le pipeline complet ; decoupage=None → un seul appel absorb, sinon la
    taille des morceaux (le DERNIER morceau peut être court). Retourne
    (condensé, le dict de sortie du finaliser)."""
    emul.preparer_ctx()
    emul.preparer_sortie()
    emul.poser_message(message)
    r = emul.appeler(L.TLS01_VA, {"rcx": ADRESSE_CTX})
    if r["crash"]:
        raise ErreurHarnais(f"tls13-01 a crashé : {r['crash']}")
    if decoupage is None:
        parties = [(0, message)] if message else [(0, b"")]
    else:
        parties = [(i, message[i:i + decoupage])
                   for i in range(0, len(message), decoupage)] or [(0, b"")]
    total_instr = r["compteur"]
    for decalage, morceau in parties:
        r = emul.appeler(L.TLS03_VA, {"rcx": ADRESSE_CTX,
                                      "rdx": ADRESSE_ENTREE + decalage,
                                      "r8": len(morceau)}, compter=compter)
        total_instr += r["compteur"]
        if r["crash"]:
            raise ErreurHarnais(f"tls13-03 a crashé : {r['crash']}")
    r = emul.appeler(L.TLS04_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_SORTIE},
                     compter=compter)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-04 a crashé : {r['crash']}")
    total_instr += r["compteur"]
    r = dict(r)
    r["compteur"] = total_instr
    return emul.lire_digest(), r


# --- V0 : les pièces du plan ------------------------------------------------------

def vecteur_v0():
    section("V0 — les pièces du plan (le scellé 0.9.0 relu, la réserve .rdata)")
    donnees = open(os.path.join(TRIADE, SCELLE_M8), "rb").read()
    controle("V0.a:le-scelle-090-intact",
             len(donnees) == SCELLE_M8_TAILLE
             and hashlib.sha256(donnees).hexdigest() == SCELLE_M8_SHA256,
             f"{len(donnees)} o, sha256 1492b0bc…b0cd4 — l'ancre R7")
    # .rdata : RVA 0x2000, raw 0x1400 — la zone 0x2F00-0x2FFF (raw 0x2300)
    zone = donnees[0x2300:0x2400]
    controle("V0.b:la-reserve-0x2F00-vierge",
             zone == b"\x00" * 256,
             "256 octets nuls — K[64] y vivra (la réserve M8 exactement remplie)")
    nom = donnees[0x22C0:0x22C0 + len(SCELLE_M8_FIXTURE_NOM)]
    ligne = donnees[0x22D0:0x22D0 + len(SCELLE_M8_FIXTURE_LIGNE)]
    controle("V0.c:les-fixtures-M8-intacts",
             nom == SCELLE_M8_FIXTURE_NOM and ligne == SCELLE_M8_FIXTURE_LIGNE,
             "NtWriteFile @0x2EC0, la ligne M0 @0x2ED0 — la frontière tenue")


# --- V1 : round-trip + concordance au plan -----------------------------------------

def vecteur_v1(emul: Emulation):
    section("V1 — round-trip de notation + concordance au plan (source unique)")
    attendus = {"h100001": 74, "h100002": 387, "h100003": 139, "h100004": 165}
    noms = {"h100001": "tls13-01-sha256-init", "h100002": "tls13-02-sha256-comprimer",
            "h100003": "tls13-03-sha256-absorber", "h100004": "tls13-04-sha256-finaliser"}
    insns_par_bloc = {}
    for bid, attendu in attendus.items():
        rva, slot = L.SLOTS_TLS13[bid]
        chemin = os.path.join(ICI, "notation", noms[bid] + ".asm")
        octets, metas = B4.assembler_bloc(emul.ks, chemin, rva, slot)
        insns = B4.round_trip(emul.cs, emul.ks, chemin, rva, octets, metas)
        insns_par_bloc[bid] = insns
        controle(f"V1.{bid}:round-trip-100",
                 len(insns) == len(metas) and len(octets) == attendu,
                 f"{len(octets)} o == {attendu} o mesurés, "
                 f"{len(insns)}/{len(metas)} instructions")

    # la concordance des H0 : chaque immédiat de tls13-01 == le plan (Q1)
    texte01 = open(os.path.join(ICI, "notation", noms["h100001"] + ".asm"),
                   encoding="utf-8").read()
    h0_notation = [int(m, 16) for m in
                   re.findall(r"mov dword ptr \[rcx(?: \+ (?:0x[0-9a-f]+|\d+))?\], (0x[0-9a-f]+)",
                              texte01)]
    controle("V1.e:les-H0-de-tls13-01-au-plan",
             h0_notation == list(L.SHA_H0),
             "les HUIT constantes FIPS § 5.3.1 == tls13/layout.py")

    # la concordance du déplacement RIP : la cible de K == R_K (I3 de tls13-02)
    cibles_rip = [B4.operande_rip_cible(insn) for insn in insns_par_bloc["h100002"]]
    cibles_rip = [c for c in cibles_rip if c is not None]
    controle("V1.f:le-K-de-tls13-02-au-plan",
             cibles_rip == [L.R_K],
             f"le déplacement RIP cible 0x{L.R_K:x} (la réserve M8)")

    # la concordance des appels : les cibles == TLS02_VA (I1 de tls13-03/04)
    ok_appels = True
    nb_appels = 0
    for bid in ("h100003", "h100004"):
        for insn in insns_par_bloc[bid]:
            if insn.mnemonic == "call":
                nb_appels += 1
                ok_appels &= int(insn.op_str, 0) == L.TLS02_VA
    controle("V1.g:les-appels-directs-au-plan",
             ok_appels and nb_appels == 3,
             f"{nb_appels} appels à 0x{L.TLS02_VA:x} (l'adresse scellée — 03 : 1, 04 : 2)")

    # la DÉRIVATION PAR ARITHMÉTIQUE : H0 et K re-dérivés des premiers
    controle("V1.h:H0-derives-par-arithmetique",
             deriv_H0() == list(L.SHA_H0),
             "racines carrées des 8 premiers premiers, parties fractionnaires")
    controle("V1.i:K-derive-par-arithmetique",
             deriv_K() == list(L.K),
             "racines cubiques des 64 premiers premiers (icbrt entier, Newton)")

    # la structure du domaine : AUCUN site syscall, AUCUN appel indirect
    ok_struct, motifs = True, []
    for bid, insns in insns_par_bloc.items():
        for insn in insns:
            if insn.mnemonic in ("syscall", "int", "sysenter"):
                ok_struct, _ = False, motifs.append(f"{bid}:{insn.mnemonic}")
            if insn.mnemonic in ("call", "jmp") and "[rip" in insn.op_str:
                ok_struct, _ = False, motifs.append(f"{bid}:indirect")
    controle("V1.j:calcul-pur-aucun-syscall-aucun-indirect",
             ok_struct, "les quatre notations — charte § 7 (l'oracle structurel du build (e))")

    # le temps constant STRUCTUREL de tls13-02 : chaque saut conditionnel y
    # compare un COMPTEUR à une constante — aucune branche ne lit les données
    insns02 = insns_par_bloc["h100002"]
    ok_const, vus = True, 0
    for i, insn in enumerate(insns02):
        if insn.mnemonic.startswith("j") and insn.mnemonic != "jmp":
            vus += 1
            j = i - 1
            while j >= 0 and not insns02[j].mnemonic.startswith("cmp"):
                j -= 1
            if j < 0 or "," not in insns02[j].op_str:
                ok_const = False
            else:
                operands = insns02[j].op_str.split(", ")
                if not operands[-1].startswith("0x"):
                    ok_const = False
    controle("V1.k:tls13-02-temps-constant-structurel",
             ok_const and vus == 3,
             f"{vus} sauts conditionnels (charger/etendre/tour), chacun sur "
             "cmp compteur/constante (I3)")


# --- V2 : les vecteurs officiels FIPS 180-4 ----------------------------------------

def vecteur_v2(emul: Emulation):
    section("V2 — les vecteurs officiels FIPS 180-4 (octet pour octet)")
    for i, (nom, message, attendu_hex) in enumerate(VECTEURS):
        attendu = bytes.fromhex(attendu_hex)
        # la référence CROISÉE : hashlib == le vecteur officiel (l'instrument
        # se contrôle avant de juger — la constante fautive serait attrapée)
        if hashlib.sha256(message).hexdigest() != attendu_hex:
            controle(f"V2.{i}:reference-hashlib", False,
                     "la constante du vecteur diverge de hashlib — INSTRUMENT DÉFAILLANT")
            continue
        digest, r = hacher(emul, message)
        controle(f"V2.{i}:{nom}",
                 digest == attendu and r["rax"] == 0 and r["crash"] is None,
                 f"{digest.hex()[:16]}… == {attendu_hex[:16]}…, rax = 0")

    # la compression SEULE à découvert : init + UN appel tls13-02 sur le
    # bloc bourré de « abc » → H == le condensé officiel (la § 6.2.2 nue)
    emul.preparer_ctx()
    emul.appeler(L.TLS01_VA, {"rcx": ADRESSE_CTX})
    bloc = b"abc" + b"\x80" + b"\x00" * 52 + struct.pack(">Q", 24)
    emul.poser_message(bloc)
    avant = bytes(emul.uc.mem_read(ADRESSE_ENTREE, 64))
    avant_ctx = emul.lire_ctx()
    r = emul.appeler(L.TLS02_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_ENTREE})
    h = emul.lire_ctx()[:32]
    digest_decouvert = b"".join(struct.pack(">I", v) for v in struct.unpack("<8I", h))
    apres = bytes(emul.uc.mem_read(ADRESSE_ENTREE, 64))
    apres_ctx = emul.lire_ctx()
    controle("V2.5:la-compression-seule-a-decouvert",
             digest_decouvert == bytes.fromhex(VECTEURS[2][2]) and r["rax"] == 0,
             "H après UN appel de tls13-02 sur le bloc bourré == SHA-256(« abc »)")
    controle("V2.6:le-bloc-et-le-ctx-intacts (Q2 de tls13-02)",
             avant == apres and apres_ctx[32:] == avant_ctx[32:],
             "le bloc d'entrée relu identique ; tampon/remplissage/total intacts")


# --- V3 : l'invariance de découpage -------------------------------------------------

def vecteur_v3(emul: Emulation):
    section("V3 — l'invariance de découpage (Q2 de tls13-03)")
    message = VECTEURS[4][1]                      # le message 896 bits
    attendu = bytes.fromhex(VECTEURS[4][2])
    decoupages = [None, 1, 3, 63, 64, 65]
    ok, details = True, []
    for d in decoupages:
        digest, r = hacher(emul, message, decoupage=d)
        if digest != attendu:
            ok = False
            details.append(f"découpage {d} DIVERGE")
    controle("V3.a:le-message-896-bits-invariant",
             ok, f"{len(decoupages)} découpages (entier, 1, 3, 63, 64, 65) — le MÊME condensé")
    # un message plus long, découpage irrégulier par 13
    long_message = bytes((i * 7 + 3) & 0xFF for i in range(200))
    attendu_long = hashlib.sha256(long_message).digest()
    ok = True
    for d in [None, 13, 64, 199]:      # 199 + 1 : le dernier morceau court
        digest, _ = hacher(emul, long_message, decoupage=d)
        if digest != attendu_long:
            ok = False
    controle("V3.b:le-message-200-octets-invariant",
             ok, "découpages entier, 13, 64, 199+1 — le MÊME condensé")


# --- V4 : le contrat -----------------------------------------------------------------

def vecteur_v4(emul: Emulation):
    section("V4 — le contrat (les pré/post de chaque bloc, sur pièces)")

    # N = 0 : LÉGAL, rien ne bouge (P3 de tls13-03)
    emul.preparer_ctx()
    emul.appeler(L.TLS01_VA, {"rcx": ADRESSE_CTX})
    avant = emul.lire_ctx()
    emul.poser_message(b"\x00" * 16)
    r = emul.appeler(L.TLS03_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_ENTREE, "r8": 0})
    controle("V4.a:N-zero-legal-rien-ne-bouge",
             r["rax"] == 0 and emul.lire_ctx() == avant and r["crash"] is None,
             "le contexte relu OCTET POUR OCTET identique, rax = 0")

    # les non-volatiles rendus + la pile équilibrée + les canaris : les 4 blocs
    ok_nv, details = True, []
    for va, args, nom in [
            (L.TLS01_VA, {"rcx": ADRESSE_CTX}, "tls13-01"),
            (L.TLS02_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_ENTREE}, "tls13-02"),
            (L.TLS03_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_ENTREE, "r8": 16}, "tls13-03"),
            (L.TLS04_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_SORTIE}, "tls13-04")]:
        emul.preparer_ctx()
        emul.appeler(L.TLS01_VA, {"rcx": ADRESSE_CTX})
        emul.poser_message(b"contract-canari-01")
        r = emul.appeler(va, args)
        if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
                and r["canaris_haut"] and r["canaris_profond"] and r["rax"] == 0):
            ok_nv = False
            details.append(nom)
    controle("V4.b:non-volatiles-pile-et-canaris (I4, les quatre blocs)",
             ok_nv, "les 8 sentinelles rendues, rsp équilibrée, l'ombre et la "
                    "zone profonde intactes" + (f" — DÉFAUTS : {details}" if details else ""))

    # l'alignement msx64 à travers l'appel direct : à CHAQUE entrée de
    # tls13-02 (appelée par 03 et 04), rsp ≡ 8 (mod 16) — le point de vue
    # du CALLE, la chaîne ABI prouvée sur pièces (l'instrument permanent
    # surveille l'entrée — la leçon du hook posé après traduction : muet)
    emul.entrees_tls02 = []
    try:
        hacher(emul, VECTEURS[4][1])          # 896 bits : absorb ET finaliser compriment
    finally:
        entrees = list(emul.entrees_tls02)
        emul.entrees_tls02 = None
    controle("V4.c:l-alignement-msx64-a-l-entree-du-calle",
             len(entrees) >= 2 and all(e % 16 == 8 for e in entrees),
             f"{len(entrees)} entrées de tls13-02 par appel direct, rsp ≡ 8 (mod 16) chacune")

    # les données d'entrée INTACTES (Q3 de tls13-03) + les canaris de zones
    message = VECTEURS[3][1]
    emul.poser_message(message)
    emul.preparer_ctx()
    emul.appeler(L.TLS01_VA, {"rcx": ADRESSE_CTX})
    r = emul.appeler(L.TLS03_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_ENTREE,
                                  "r8": len(message)})
    relu = bytes(emul.uc.mem_read(ADRESSE_ENTREE, len(message)))
    controle("V4.d:les-donnees-intactes (Q3 de tls13-03)",
             relu == message and emul.canaris_entree_intacts(len(message))
             and emul.canaris_ctx_intacts() and emul.canaris_sortie_intacts(),
             "le message relu identique, les canaris des trois zones intacts")

    # le contexte CLOS détecté (Q3 de tls13-04) : un absorb APRÈS finalisation
    # est un comportement non défini — le harnais le REFUSE : le condensé
    # diverge de TOUT vecteur officiel, jamais une égalité en silence
    # l'état clos : absorb + finaliser ENCADRÉS sur le même contexte
    emul.preparer_ctx()
    emul.appeler(L.TLS01_VA, {"rcx": ADRESSE_CTX})
    emul.poser_message(b"abc")
    emul.appeler(L.TLS03_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_ENTREE, "r8": 3})
    emul.appeler(L.TLS04_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_SORTIE})
    emul.poser_message(b"def")
    emul.appeler(L.TLS03_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_ENTREE, "r8": 3})
    emul.appeler(L.TLS04_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_SORTIE})
    digest_clos = emul.lire_digest()
    officiels = {bytes.fromhex(v[2]) for v in VECTEURS}
    officiels.add(hashlib.sha256(b"abcdef").digest())
    controle("V4.e:le-contexte-clos-detected (Q3 de tls13-04)",
             digest_clos not in officiels,
             "le condensé après réutilisation diverge de tout vecteur — "
             "l'état clos est NOMMÉ, jamais toléré en silence")


# --- V5 : la falsification (zéro silence) ---------------------------------------------

def vecteur_v5(emul: Emulation):
    section("V5 — la falsification (chaque mutation ATTRAPÉE, zéro silence)")

    # chaque VECTEUR muté (premier, milieu, dernier bit du message) → divergence
    attrapes, total = 0, 0
    for nom, message, attendu_hex in VECTEURS:
        attendu = bytes.fromhex(attendu_hex)
        if not message:
            continue
        positions = [0, len(message) // 2, len(message) - 1]
        for pos in positions:
            mute = bytearray(message)
            mute[pos] ^= 0x01
            digest, _ = hacher(emul, bytes(mute))
            total += 1
            if digest != attendu:
                attrapes += 1
    controle("V5.a:les-messages-mutes-attrapes",
             attrapes == total and total > 0,
             f"{attrapes}/{total} mutations (premier/milieu/dernier bit) ATTRAPÉES")

    # la comparaison n'est pas muette : chaque bit SENSIBLE du condensé
    # attendu muté → l'égalité ÉCHOUE (l'instrument se prouve non-vide)
    attrapes, total = 0, 0
    for _, _, attendu_hex in VECTEURS:
        attendu = bytearray(bytes.fromhex(attendu_hex))
        for bit in (0, 127, 255):
            mute = bytearray(attendu)
            mute[bit // 8] ^= 1 << (bit % 8)
            total += 1
            if bytes(mute) != bytes(attendu):
                attrapes += 1
    controle("V5.b:la-comparaison-n-est-pas-muette",
             attrapes == total,
             f"{attrapes}/{total} condensés attendus mutés → l'égalité ÉCHOUE")

    # K corrompu → divergence : LA PREUVE que la table est LUE (I3 de tls13-02)
    k_orig = bytes(emul.uc.mem_read(L.R_K, 256))
    emul.uc.mem_write(L.R_K + 13 * 4, struct.pack("<I", L.K[13] ^ 1))
    digest, _ = hacher(emul, b"abc")
    emul.uc.mem_write(L.R_K, k_orig)
    controle("V5.c:K-corrompu-diverge",
             digest != bytes.fromhex(VECTEURS[2][2]),
             "K[13] muté → le condensé diverge : la table @0x2F00 est LUE")

    # H0 corrompu après init → divergence
    emul.preparer_ctx()
    emul.appeler(L.TLS01_VA, {"rcx": ADRESSE_CTX})
    emul.uc.mem_write(ADRESSE_CTX + 12, struct.pack("<I", 0xDEADBEEF))
    emul.poser_message(b"abc")
    emul.appeler(L.TLS03_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_ENTREE, "r8": 3})
    emul.appeler(L.TLS04_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_SORTIE})
    controle("V5.d:H0-corrompu-diverge",
             emul.lire_digest() != bytes.fromhex(VECTEURS[2][2]),
             "H[3] muté après init → le condensé diverge")

    # le total corrompu → divergence (le bourrage dépend du total public)
    emul.preparer_ctx()
    emul.appeler(L.TLS01_VA, {"rcx": ADRESSE_CTX})
    emul.poser_message(b"abc")
    emul.appeler(L.TLS03_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_ENTREE, "r8": 3})
    total_avant = struct.unpack_from("<Q", emul.lire_ctx(), L.CTX_TOTAL)[0]
    emul.uc.mem_write(ADRESSE_CTX + L.CTX_TOTAL, struct.pack("<Q", total_avant + 1))
    emul.appeler(L.TLS04_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_SORTIE})
    controle("V5.e:le-total-corrompu-diverge",
             emul.lire_digest() != bytes.fromhex(VECTEURS[2][2]),
             "total + 1 → la longueur en bits du bourrage diverge")


# --- V6 : le temps constant mesuré ------------------------------------------------------

def vecteur_v6(emul: Emulation, graine: int):
    section("V6 — le temps constant MESURÉ (I3 de tls13-02, la charte § 3)")
    rng = random.Random(graine)
    blocs = [bytes(rng.randrange(256) for _ in range(64)) for _ in range(4)]
    comptes = []
    for bloc in blocs:
        emul.preparer_ctx()
        emul.appeler(L.TLS01_VA, {"rcx": ADRESSE_CTX})
        emul.poser_message(bloc)
        r = emul.appeler(L.TLS02_VA, {"rcx": ADRESSE_CTX, "rdx": ADRESSE_ENTREE},
                         compter=True)
        comptes.append(r["compteur"])
    controle("V6.a:la-compression-compte-constant",
             len(set(comptes)) == 1,
             f"{len(blocs)} blocs aléatoires, {comptes[0]} instructions EXACTEMENT")

    messages = [bytes(rng.randrange(256) for _ in range(135)) for _ in range(4)]
    comptes = []
    for message in messages:
        _, r = hacher(emul, message, compter=True)
        comptes.append(r["compteur"])
    controle("V6.b:la-pipeline-compte-constant",
             len(set(comptes)) == 1,
             f"4 messages de 135 o, {comptes[0]} instructions EXACTEMENT — "
             "aucune branche ne lit les données")


# --- Le verdict --------------------------------------------------------------------------

def main() -> int:
    graine = 20261105
    if "--graine" in sys.argv:
        graine = int(sys.argv[sys.argv.index("--graine") + 1])
    print("=== tls13/harnais_sha.py — LE HARNAIS DE LA FAMILLE sha (chantier M9-(b)) ===")
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
