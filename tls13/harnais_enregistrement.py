#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tls13/harnais_enregistrement.py — LE HARNAIS DE LA FAMILLE enregistrement.

Chantier M9-(b), cinquième geste : les blocs tls13-20/21 (l'enregistrement
protéger, l'enregistrement déprotéger — RFC 8446 § 5.2/§ 5.3 : le texte
interne charge || type, le nonce = IV ⊕ séquence, l'AAD = l'en-tête)
NOTÉS-MESURÉS-PROUVÉS sur les familles sha, hkdf, x25519 et aead
notées-mesurées-prouvées aux gestes précédents. Le modèle est le harnais
aead (tls13/harnais_aead.py — la référence GCM importée : la source unique
de la lignée) : l'émulation nue à les RVA du plan (mécanisme D79),
l'appelant factice pose les sentinelles non volatiles et les canaris, le
verdict est TRANCHÉ par le code — jamais cru.

LE CAHIER (la charte § 2 : les vecteurs officiels AVANT usage, la
falsification, zéro silence) :

  V0 — LES PIÈCES DU PLAN : le scellé 0.9.0 relu (l'ancre 1492b0bc…), les
       familles sha, hkdf, x25519 ET aead INTACTES (les DIX-NEUF notations
       re-round-tripées aux longueurs arrêtées — la frontière des gestes
       précédents), K[64] posé à R_K, LES FIXTURES DU DOMAINE posés à leur
       ARRÊT .text6, l'arbre I scellé relu VERT (verifier_specs_m9a rejoué
       — R2) ; LE CONTEXTE ENREGISTREMENT (200 o — la disposition DÉCLARÉE
       par tls13-20:R1 : clés de tour @+0 [176], IV @+176 [12], réserve
       @+188 [4], séquence @+192 [8]) posé par le harnais — le contexte
       sera POSÉ par tls13-24 au geste qui le dérivera, l'adresse choisie
       par l'appelant (charte § 6) ;
  V1 — LE ROUND-TRIP + LA CONCORDANCE : chaque notation ré-assemblée en
       ses octets (keystone == capstone, R5), les longueurs == l'ARRÊT du
       plan (349/403 o, D161 — le verdict 64 bits nommé par la sonde :
       mov rax, −N de la famille, re-mesuré 343→349 et 395→403), les
       appels directs de 20 == TLS18 (UNE composition) et de 21 == TLS19
       (UNE composition) ; LES IMMÉDIATS au plan : l'en-tête locale (23,
       3, 3 — CINQ octets FIXES), le N+17 u16 gros-boutiste (lea [r9+17],
       les octets forts/faibles), le nonce (les offset 176/184/192 du
       contexte, bswap la séquence GROS-BOUTISTE), les bornes (0x4000 de
       20, 23/18/16400 de 21) ; LA STRUCTURE : aucun site syscall, aucun
       appel indirect, AUCUN déplacement RIP (la famille enregistrement
       autoporteur comme l'aead) ; LE TEMPS CONSTANT STRUCTUREL : 20
       exactement SEPT sauts conditionnels, 21 exactement ONZE — TOUS sur
       les données PUBLIQUES (pointeurs, longueurs, compteurs de copie,
       l'en-tête REÇUE [des métadonnées de protocole], les verdicts
       propagés), les comptes EXACTS vérifiés source par source ;
  V2 — LES VECTEURS OFFICIELS — LE TRANSFERT RFC 8448 EN CHAÎNES : les
       QUATRE contextes de trafic du transcript (poignée serveur, poignée
       client, applicative serveur, applicative client) consommés EN
       SÉQUENCE — chaque enregistrement du § 3 PROTÉGÉ par tls13-20 (le
       nonce = IV ⊕ séquence, la séquence avançant 0, 1, 2…) == le
       transcript OCTET POUR OCTET, PUIS DÉPROTÉGÉ par tls13-21 (les
       charges ET les types restitués), ET LA REJOUE REFUSÉE (un
       enregistrement consommé rejoué → rax = −4 : la séquence a avancé,
       l'étiquette ne colle plus — L'ANTI-REJOUE DU PROTOCOLE tient dans
       la cryptographie, pas dans un compteur de logique) + l'oracle
       différentiel (des enregistrements aléatoires contre la référence) ;
  V3 — LES CAS PUNITIFS : LA BORNE (N = 2^14−1 scellé puis ouvert — le
       texte interne 2^14 EXACTEMENT la borne de la brique ; N = 2^14 →
       rax = −3 NOMMÉ le verdict PROPAGÉ de tls13-18 : le maximal du
       protocole refusé par la composition, la fragmentation à
       l'APPELANT ; N = 2^14+1 → −2), le type PASSE-PLAT (21/22/23 : le
       type réel vit DANS le chiffré), l'indifférence (N = 0 avec le
       pointeur de charge NUL : le couple longueur/pointeur, jamais le
       pointeur seul), les refus (les pointeurs nuls, l'en-tête ≠ 23 →
       −1 ; déclarée ≠ reçue, le minimum 5+18, la borne de la brique
       2^14+16 → −2), LA VERSION HÉRITAGE IGNORÉE par la logique MAIS
       COUVERTE par l'AAD (la mutation → −4 : la cryptographie attrape
       ce que la logique ignore — RFC 8446 § 5.1 « MUST be ignored ») ;
       L'ORDRE : la séquence AVANCE après le succès, JAMAIS après un
       échec (le −3 et le −4 ne bougent RIEN) ;
  V4 — LE CONTRAT : les non-volatiles rendus, la pile équilibrée,
       l'ombre et le logement intacts (le cadre 0x4078 : le texte interne
       jusqu'à 2^14+1 sur la pile — la zone morte PROFONDE déplacée sous
       le cadre : −0x5000), l'alignement msx64 à l'entrée de CHAQUE
       appelé à travers la composition (TLS18 par 20, TLS19 par 21 —
       les comptes exacts), la charge INTACTE (Q2), l'enregistrement
       reçu INTACT (Q4), LE CONTEXTE RÉÉCRIT SUR SA SÉQUENCE SEULE (les
       192 premiers octets — les clés de tour, l'IV, la réserve —
       OCTET-IDENTIQUES après le geste), les sorties JAMAIS dépassées,
       les refus SANS corruption (la sortie VIERGE sur le −3, la charge
       et le type VIERGES sur le −4) ;
  V5 — LA FALSIFICATION (zéro silence) : la charge mutée → l'enregistrement
       diverge, le type muté → diverge, la SÉQUENCE du contexte mutée →
       diverge (le nonce la porte), chaque octet du chiffré muté → −4,
       chaque octet de l'étiquette muté → −4, l'en-tête reçue mutée : le
       type → −1, la longueur → −2, LA VERSION → −4 (l'AAD couvre ce que
       la logique ignore), la comparaison n'est pas muette ;
  V6 — LE TEMPS CONSTANT MESURÉ : le scellement (2 charges de même
       longueur, 2 clés → LE MÊME compte — la longueur publique, le
       contenu jamais), le déscellement (2 enregistrements conformes de
       même longueur → LE MÊME compte), ET LE VERDICT (trois
       enregistrements divergents — le chiffré muté au premier, au
       milieu, au dernier octet → LE MÊME compte EXACTEMENT : le −4 de
       tls13-19 ne court-circuite pas, la position de la divergence est
       invisible dans le temps).

Usage : python3 harnais_enregistrement.py            # le cahier complet
        python3 harnais_enregistrement.py --graine N # la graine (défaut 20261107)
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

# LE HARNAIS AEAD DE LA LIGNÉE — la référence GCM (AES + GHASH + GCM en
# Python pur, contre-preuvée FIPS 197 C.1 / SP 800-38A F.1.1 / McGrew–Viega
# TC1..TC6 / RFC 8448 au geste précédent) ET les constantes du transfert
# (TRANSFERT_8448 : les SEPT enregistrements consignés) : la source unique
import harnais_aead as AEAD  # noqa: E402

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

ZONE_IMAGE = (0x1000, 0xF000)
RET_MAGIQUE = 0xEF00            # la marge .text6 (après la famille aead et
                                # enregistrement 0xED00, avant les fixtures)
ZONE_CTX = 0x500000             # le contexte enregistrement (200 o)
ZONE_DONNEES = 0x600000         # la charge, l'enregistrement reçu
TAILLE_DONNEES = 0x20000        # jusqu'à 2^14 + les canaris
ZONE_SORTIE = 0x700000          # l'enregistrement émis, la charge restituée
TAILLE_SORTIE = 0x20000
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP0 = 0x7F008000
ENTREE_RSP = RSP0 - 0x108

FENETRE = 0x100

ADR_CTX = ZONE_CTX + 0x100
ADR_CHARGE = ZONE_DONNEES + 0x1000
ADR_RECU = ZONE_DONNEES + 0x8000
ADR_EMIS = ZONE_SORTIE + 0x1000
ADR_RENDU = ZONE_SORTIE + 0x8000
ADR_TYPE = ZONE_SORTIE + 0x10000

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
# LA RÉFÉRENCE — la couche enregistrement (RFC 8446 § 5.2/§ 5.3) sur la
# référence GCM du harnais aead (la source unique de la lignée)
# ======================================================================

TYPE_ALERT = 21
TYPE_HANDSHAKE = 22
TYPE_DATA = 23


class Contexte:
    """La disposition DÉCLARÉE par tls13-20:R1 (200 o) : clés de tour @+0
    [176], IV @+176 [12], réserve @+188 [4], séquence u64 @+192 [8]."""

    def __init__(self, cle: bytes, iv: bytes, seq: int = 0):
        assert len(cle) == 16 and len(iv) == 12
        self.cle = cle
        self.rk = b"".join(AEAD.ref_cles_tour(cle))
        self.iv = iv
        self.seq = seq

    def serialiser(self) -> bytes:
        return (self.rk + self.iv + bytes(4)
                + self.seq.to_bytes(8, "little"))


def _nonce_de(iv: bytes, seq: int) -> bytes:
    """I2 : le nonce = IV ⊕ séquence (le u64 GROS-BOUTISTE sur les octets
    4..11) — RFC 8446 § 5.3."""
    n = bytearray(iv)
    s = seq.to_bytes(8, "big")
    for j in range(8):
        n[4 + j] ^= s[j]
    return bytes(n)


def _aad_de(n_charge: int) -> bytes:
    """L'AAD = l'en-tête ÉMISE : (23, 0x0303, N+17 en u16 gros-boutiste)."""
    return bytes([23, 3, 3]) + (n_charge + 17).to_bytes(2, "big")


def ref_proteger(ctx: Contexte, type_contenu: int, charge: bytes) -> bytes:
    """tls13-20 : l'enregistrement protégé — RFC 8446 § 5.2."""
    texte_interne = charge + bytes([type_contenu & 0xFF])
    nonce = _nonce_de(ctx.iv, ctx.seq)
    aad = _aad_de(len(charge))
    ct, tag = AEAD.ref_gcm_sceller(ctx.cle, nonce, aad, texte_interne)
    ctx.seq += 1          # l'incrémentation SUIT le scellement
    return aad + ct + tag


def ref_deprotéger(ctx: Contexte, enregistrement: bytes):
    """tls13-21 : l'inverse — l'en-tête confrontée AVANT TOUT (le type 23,
    la longueur déclarée == reçue, la version IGNORÉE), puis le verdict.
    Rend (charge, type) ou None (échec nommé par le code appelant)."""
    if len(enregistrement) < 5 + 18:
        return None                                   # -2 : le minimum structurel
    if enregistrement[0] != 23:
        return None                                   # -1 : le protégé est opaque
    declare = int.from_bytes(enregistrement[3:5], "big")
    if declare != len(enregistrement) - 5:
        return None                                   # -2 : l'épuisement exact
    if declare < 18 or declare > 2**14 + 16:
        return None                                   # -2 : les bornes (P2 + la brique)
    nonce = _nonce_de(ctx.iv, ctx.seq)
    aad = enregistrement[:5]                          # l'en-tête REÇUE TELLE QUELLE
    ct_tag = enregistrement[5:]
    clair = AEAD.ref_gcm_ouvrir(ctx.cle, nonce, aad, ct_tag[:-16], ct_tag[-16:])
    if clair is None:
        return None                                   # -4 : cryptographie divergente
    ctx.seq += 1
    return clair[:-1], clair[-1]


def chaines_depuis_8448():
    """LES QUATRE CHAÎNES du transcript — groupées par contexte de trafic
    (la clé ET l'IV). L'ORDRE du § 3 ENTRELACE les enregistrements (le vol
    serveur, le Finished client, le NST, les applicatives client/serveur,
    les close_notify client/serveur) : le groupement par contexte PRÉSERVE
    l'ordre de première apparition ET l'ordre des enregistrements (qui EST
    l'ordre des séquences : chaque contexte consomme 0, 1, 2…). Le payload
    = le clair interne SANS le type (le dernier octet), le type = cet
    octet (les constantes CONSIGNÉES au harnais aead : TRANSFERT_8448,
    parsées du texte officiel par le labo)."""
    groupes: dict[tuple[bytes, bytes], list] = {}
    for nom, cle_hex, iv_hex, seq, interne_hex, record_hex in AEAD.TRANSFERT_8448:
        interne, record = bytes.fromhex(interne_hex), bytes.fromhex(record_hex)
        cle, iv = bytes.fromhex(cle_hex), bytes.fromhex(iv_hex)
        clef = (cle, iv)
        if clef not in groupes:
            groupes[clef] = []
        groupes[clef].append((interne[-1], interne[:-1], record, seq))
    noms = ["la chaîne poignée serveur", "la chaîne poignée client",
            "la chaîne applicative serveur", "la chaîne applicative client"]
    assert len(groupes) == 4, len(groupes)
    # les séquences de chaque groupe : 0, 1, 2… consécutives (l'ordre du § 3)
    for records in groupes.values():
        assert [s for _, _, _, s in records] == list(range(len(records)))
    return [(nom, (cle, iv), groupes[(cle, iv)])
            for nom, (cle, iv) in zip(noms, groupes.keys())]


CHAINES = chaines_depuis_8448()


# --- L'émulation (le modèle harnais_aead — l'appelant factice msx64) --------------

class Emulation:
    """Les VINGT-ET-UN blocs posés à leurs RVA du plan, appelés comme des
    fonctions msx64 ordinaires. Le mode « nue » (aucun hook) sert les
    longues exécutions. La zone morte PROFONDE vit à [−0x5000, −0x4C00) :
    le cadre de tls13-20/21 [0x4078] + celui de tls13-18/19 [0xE8] ≈ 0x4160
    sous l'entrée — la leçon du cadre NOMMÉ."""

    BLOCS = AEAD.Emulation.BLOCS + [
        ("h100020", "tls13-20-enregistrement-proteger"),
        ("h100021", "tls13-21-enregistrement-deproteger")]

    def __init__(self, nue: bool = False):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.ks = Ks(KS_ARCH_X86, KS_MODE_64)
        self.cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.cs.detail = False
        self.uc.mem_map(*ZONE_IMAGE)
        for zone, taille in ((ZONE_CTX, 0x1000),
                             (ZONE_DONNEES, TAILLE_DONNEES),
                             (ZONE_SORTIE, TAILLE_SORTIE),
                             (ZONE_PILE, TAILLE_PILE)):
            self.uc.mem_map(zone, taille)
        for zone, taille in ((ZONE_CTX, 0x1000),
                             (ZONE_DONNEES, TAILLE_DONNEES),
                             (ZONE_SORTIE, TAILLE_SORTIE)):
            self.uc.mem_write(zone, CANARI * taille)
        # les pièces du plan : K[64] à R_K, les fixtures à leur ARRÊT .text6
        self.uc.mem_write(L.R_K, struct.pack("<64I", *L.K))
        self.uc.mem_write(L.R_U9, L.X25519_BASE.to_bytes(32, "little"))
        self.uc.mem_write(L.R_EXP_INV, ((2**255 - 19) - 2).to_bytes(32, "little"))
        self.blobs: dict[str, tuple[bytes, list]] = {}
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
        sortie + canaris (le modèle harnais_aead)."""
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
        # la zone morte PROFONDE : sous TOUT cadre possible — le cadre NOMMÉ
        # de 20/21 [0x4078] + celui de 18/19 [0xE8] ≈ 0x4160 ; la zone vit
        # à [−0x5000, −0x4C00) (la leçon du geste : −0x1000 était INSIDE)
        uc.mem_write(rsp - 0x5000, CANARI * 0x400)
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
            uc.mem_read(entree_rsp - 0x5000, 0x400)) == CANARI * 0x400
        return sortie

    def non_volatiles_rendus(self, r: dict) -> bool:
        return all(r[nom] == SENTINELLES_NV[nom] for nom in SENTINELLES_NV)

    # --- les zones canaris ---------------------------------------------------

    def poser(self, adresse: int, donnees: bytes):
        self.uc.mem_write(adresse - FENETRE, CANARI * FENETRE)
        self.uc.mem_write(adresse, donnees)
        self.uc.mem_write(adresse + len(donnees),
                          CANARI * (FENETRE + 0x20))

    def intact_autour(self, adresse: int, longueur: int) -> bool:
        avant = bytes(self.uc.mem_read(adresse - FENETRE, FENETRE))
        apres = bytes(self.uc.mem_read(adresse + longueur, FENETRE + 0x20))
        return avant == CANARI * FENETRE and apres == CANARI * (FENETRE + 0x20)


# --- Les pipelines (les compositions du harnais) -----------------------------------

def poser_contexte(emul: Emulation, ctx: Contexte):
    """Pose le contexte (200 o) avec la fenêtre canaris — la séquence
    emulée fait foi : la relecture après CHAQUE appel (leçon de la sonde)."""
    emul.poser(ADR_CTX, ctx.serialiser())


def lire_sequence(emul: Emulation) -> int:
    return struct.unpack("<Q", bytes(emul.uc.mem_read(ADR_CTX + 192, 8)))[0]


def proteger(emul: Emulation, ctx: Contexte, type_contenu: int,
             charge: bytes, compter: bool = False, force: dict | None = None):
    """tls13-20 : l'enregistrement protégé. `force` substitue un argument
    (les refus : le pointeur nul, la taille hors borne)."""
    poser_contexte(emul, ctx)
    emul.poser(ADR_CHARGE, charge)
    emul.uc.mem_write(ADR_EMIS, CANARI * (len(charge) + 0x120))
    args = {"rcx": ADR_CTX, "rdx": type_contenu & 0xFF,
            "r8": ADR_CHARGE, "r9": len(charge)}
    pile = [ADR_EMIS]
    if force:
        if "rcx" in force:
            args["rcx"] = force["rcx"]
        if "r8" in force:
            args["r8"] = force["r8"]
        if "r9" in force:
            args["r9"] = force["r9"]
        if "sortie" in force:
            pile[0] = force["sortie"]
    r = emul.appeler(L.TLS20_VA, args, compter=compter, args_pile=pile)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-20 a crashé : {r['crash']}")
    emis = bytes(emul.uc.mem_read(ADR_EMIS, len(charge) + 22))
    ctx.seq = lire_sequence(emul)     # la séquence ÉMULÉE (le bloc avance la sienne)
    return emis, r


def deproteger(emul: Emulation, ctx: Contexte, record: bytes,
               compter: bool = False, force: dict | None = None):
    """tls13-21 : l'enregistrement déprotégé (le verdict AVANT la restitution)."""
    poser_contexte(emul, ctx)
    emul.poser(ADR_RECU, record)
    emul.uc.mem_write(ADR_RENDU, CANARI * (len(record) + 0x120))
    emul.uc.mem_write(ADR_TYPE, CANARI * 0x10)
    args = {"rcx": ADR_CTX, "rdx": ADR_RECU, "r8": len(record), "r9": ADR_RENDU}
    pile = [ADR_TYPE]
    if force:
        if "rcx" in force:
            args["rcx"] = force["rcx"]
        if "rdx" in force:
            args["rdx"] = force["rdx"]
        if "r9" in force:
            args["r9"] = force["r9"]
        if "type" in force:
            pile[0] = force["type"]
    r = emul.appeler(L.TLS21_VA, args, compter=compter, args_pile=pile)
    if r["crash"]:
        raise ErreurHarnais(f"tls13-21 a crashé : {r['crash']}")
    n_charge = len(record) - 5 - 17
    rendu = bytes(emul.uc.mem_read(ADR_RENDU, max(n_charge, 0)))
    type_r = bytes(emul.uc.mem_read(ADR_TYPE, 1))
    ctx.seq = lire_sequence(emul)
    return rendu, type_r, n_charge, r


# --- V0 : les pièces du plan ------------------------------------------------------

def vecteur_v0(emul: Emulation):
    section("V0 — les pièces du plan (le scellé, sha+hkdf+x25519+aead, l'arbre I, le contexte)")
    donnees = open(os.path.join(TRIADE, SCELLE_M8), "rb").read()
    controle("V0.a:le-scelle-090-intact",
             len(donnees) == SCELLE_M8_TAILLE
             and hashlib.sha256(donnees).hexdigest() == SCELLE_M8_SHA256,
             f"{len(donnees)} o, sha256 1492b0bc…b0cd4 — l'ancre R7")
    # les familles précédentes INTACTES : les DIX-NEUF notations relues
    # aux longueurs ARRÊTÉES du plan (la frontière des gestes précédents)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    attendus = {"h100001": 74, "h100002": 387, "h100003": 139, "h100004": 165,
                "h100005": 435, "h100006": 151, "h100007": 347, "h100008": 310,
                "h100009": 54, "h100010": 252, "h100011": 1078,
                "h100012": 281, "h100013": 2887, "h100014": 23,
                "h100015": 520, "h100016": 129, "h100017": 162,
                "h100018": 1076, "h100019": 1163}
    noms = {bid: nom for bid, nom in Emulation.BLOCS if bid in attendus}
    ok, details = True, []
    for bid, attendu in attendus.items():
        rva, slot = L.SLOTS_TLS13[bid]
        chemin = os.path.join(ICI, "notation", noms[bid] + ".asm")
        octets, _ = B4.assembler_bloc(ks, chemin, rva, slot)
        if len(octets) != attendu:
            ok = False
            details.append(f"{noms[bid]} : {len(octets)} o ≠ {attendu}")
    controle("V0.b:les-familles-precedentes-intactes", ok,
             "les DIX-NEUF notations relues aux longueurs arrêtées : sha "
             "74/387/139/165 + hkdf 435/151/347/310 + x25519 54/252/1078/"
             "281/2887/23 + aead 520/129/162/1076/1163 o"
             + (f" — DÉFAUTS : {details}" if details else ""))
    # le contexte enregistrement : LA DISPOSITION DÉCLARÉE (200 o)
    ctx = Contexte(bytes(range(16)), bytes(range(12, 24)), seq=2026)
    poser_contexte(emul, ctx)
    ser = bytes(emul.uc.mem_read(ADR_CTX, 200))
    controle("V0.c:le-contexte-enregistrement-200o",
             ser == ctx.serialiser()
             and ser[0:176] == ctx.rk and ser[176:188] == ctx.iv
             and ser[188:192] == bytes(4)
             and ser[192:200] == (2026).to_bytes(8, "little"),
             "les clés de tour @+0 [176], l'IV @+176 [12], la réserve @+188 "
             "[4], la séquence u64 @+192 [8] — la disposition DÉCLARÉE par "
             "tls13-20:R1, posée par l'APPELANT (le contexte sera posé par "
             "tls13-24 au geste qui le dérivera — charte § 6)")
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
    attendus = {"h100020": 349, "h100021": 403}
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
    # la concordance des appels directs : UNE composition chacun (I1)
    cibles_attendues = {
        "h100020": {L.TLS18_VA: 1},
        "h100021": {L.TLS19_VA: 1},
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
             "20 → TLS18 (UNE composition — le scellement) ; 21 → TLS19 "
             "(UNE composition — le déverrouillage)"
             + (f" — DÉFAUTS : {details}" if details else ""))
    # la concordance des immédiats : l'en-tête locale, le nonce, les bornes
    texte20 = open(os.path.join(ICI, "notation",
                                "tls13-20-enregistrement-proteger.asm"),
                   encoding="utf-8").read()
    controle("V1.f:l-en-tete-de-20-au-plan",
             "mov byte ptr [rsp + 0x50], 23" in texte20
             and "mov byte ptr [rsp + 0x51], 3" in texte20
             and "mov byte ptr [rsp + 0x52], 3" in texte20
             and "lea r10, [r9 + 17]" in texte20,
             "CINQ octets FIXES : 23 opaque, 0x0303 héritage, N+17 en u16 "
             "gros-boutiste (les octets forts/faibles posés par octets)")
    controle("V1.g:le-nonce-de-20-au-plan",
             "mov r11, qword ptr [rcx + 176]" in texte20
             and "mov r11d, dword ptr [rcx + 184]" in texte20
             and "mov r11, qword ptr [rcx + 192]" in texte20
             and "\nbswap r11\n" in texte20
             and "xor qword ptr [rsp + 0x44], r11" in texte20,
             "l'IV copié en local depuis @+176, la séquence u64 depuis "
             "@+192, bswap le GROS-BOUTISTE, le XOR sur les octets 4..11 "
             "— le contexte jamais réécrit sur son IV (I2)")
    controle("V1.h:les-bornes-de-20",
             "cmp r9, 0x4000" in texte20
             and "add qword ptr [rcx + 192], 1" in texte20,
             "N ≤ 2^14 (TLSPlaintext.length, RFC 8446 § 5.1) ; "
             "l'incrémentation APRÈS le scellement (l'ordre nommé : un "
             "échec n'avance JAMAIS)")
    texte21 = open(os.path.join(ICI, "notation",
                                "tls13-21-enregistrement-deproteger.asm"),
                   encoding="utf-8").read()
    controle("V1.i:les-confrontations-de-21-au-plan",
             "cmp r8, 23" in texte21
             and "cmp byte ptr [rdx], 23" in texte21
             and "cmp r10, 18" in texte21
             and "cmp r10, 16400" in texte21
             and "lea r10, [rdx + r8 - 16]" in texte21,
             "le total ≥ 5+18, le type reçu == 23, le minimum L ≥ 18 (P2), "
             "la borne de la brique L ≤ 2^14+16 (le -4 de 19 ne peut plus "
             "refuser sur les longueurs : l'épuisement exact AVANT l'appel)")
    # la structure du domaine : AUCUN site syscall, AUCUN appel indirect,
    # AUCUN déplacement RIP (la famille autoporteur)
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
             "aucun syscall, aucun appel indirect, AUCUN déplacement RIP — "
             "la famille enregistrement autoporteur comme l'aead"
             + (f" — MOTIFS : {motifs}" if motifs else ""))
    # le temps constant STRUCTUREL : les comptes EXACTS, toutes les sources
    # publiques (l'en-tête reçue est une métadonnée de protocole)
    def inventaire_jcc(insns):
        out = []
        for k, insn in enumerate(insns):
            if insn.mnemonic.startswith("j") and insn.mnemonic != "jmp":
                j = k - 1
                while j >= 0 and insns[j].mnemonic not in (
                        "cmp", "test", "dec", "sub", "add"):
                    j -= 1
                out.append(f"{insns[j].mnemonic} {insns[j].op_str}")
        return out

    from collections import Counter
    inv20 = Counter(inventaire_jcc(insns_par_bloc["h100020"]))
    inv21 = Counter(inventaire_jcc(insns_par_bloc["h100021"]))
    attendu20 = Counter({"test rcx, rcx": 1, "cmp r9, 0x4000": 1,
                          "test rax, rax": 1, "test r9, r9": 1,
                          "test r8, r8": 1, "cmp r10, r9": 1,
                          "test eax, eax": 1})
    attendu21 = Counter({"test rcx, rcx": 1, "test rdx, rdx": 1,
                         "test r9, r9": 1, "test rax, rax": 1,
                         "cmp r8, 0x17": 1, "cmp byte ptr [rdx], 0x17": 1,
                         "cmp r10, r11": 1, "cmp r10, 0x12": 1,
                         "cmp r10, 0x4010": 1, "test eax, eax": 1,
                         "cmp rax, r11": 1})
    controle("V1.k:temps-constant-structurel",
             inv20 == attendu20 and inv21 == attendu21,
             f"20 : {sum(inv20.values())} sauts conditionnels (les "
             "pointeurs, N, le compteur de copie, le verdict propagé — "
             f"TOUS publics) ; 21 : {sum(inv21.values())} (idem + "
             "l'en-tête REÇUE : le type, les longueurs — des métadonnées "
             "de protocole, jamais un secret ; la charge et le chiffré ne "
             "touchent JAMAIS une branche — I3 hérité de 18/19)")


# --- V2 : les vecteurs officiels — LE TRANSFERT RFC 8448 EN CHAÎNES -----------------

def vecteur_v2(emul: Emulation, nue: Emulation, graine: int):
    section("V2 — LE TRANSFERT RFC 8448 EN CHAÎNES + l'oracle différentiel")

    # (a) les QUATRE chaînes PROTÉGÉES : chaque contexte consomme ses
    # séquences 0, 1, 2… — chaque enregistrement du transcript reconstruit
    # OCTET POUR OCTET par les briques mêmes
    for nom_chaine, (cle, iv), records in CHAINES:
        ctx = Contexte(cle, iv, seq=0)
        tous, details = True, []
        for i, (type_att, payload, record, seq_att) in enumerate(records):
            assert ctx.seq == seq_att, (nom_chaine, i, ctx.seq, seq_att)
            emis, r = proteger(emul, ctx, type_att, payload)
            if not (r["rax"] == 0 and emis == record):
                tous = False
                details.append(f"#{i}(rax={r['rax']})")
        controle(f"V2.a:{nom_chaine}:PROTEGER-en-chaine", tous,
                 f"{len(records)} enregistrement(s) == le transcript OCTET "
                 f"POUR OCTET — le nonce = IV ⊕ séquence, les séquences "
                 f"0..{len(records) - 1} consommées successivement"
                 + (f" — DÉFAUTS : {details}" if details else ""))
        # (b) la même chaîne DÉPROTÉGÉE : UN contexte neuf, les
        # enregistrements consommés dans l'ordre → les charges ET les types
        ctx2 = Contexte(cle, iv, seq=0)
        tous, details = True, []
        for i, (type_att, payload, record, _) in enumerate(records):
            rendu, type_r, _, r = deproteger(emul, ctx2, record)
            if not (r["rax"] == 0 and rendu == payload
                    and type_r == bytes([type_att])):
                tous = False
                details.append(f"#{i}(rax={r['rax']})")
        controle(f"V2.b:{nom_chaine}:DEPROTEGER-en-chaine", tous,
                 "les charges ET les types restitués — le type = le "
                 "DERNIER octet du texte interne"
                 + (f" — DÉFAUTS : {details}" if details else ""))
        # (c) LA REJOUE : l'enregistrement #0 déjà consommé → -4
        S = nue
        ctx3 = Contexte(cle, iv, seq=0)
        for _, _, record, _ in records:
            deproteger(S, ctx3, record)
        rendu, type_r, n_ch, r = deproteger(S, ctx3, records[0][2])
        intact = rendu == CANARI * n_ch and type_r == CANARI
        controle(f"V2.c:{nom_chaine}:la-REJOUE-refusee",
                 r["rax"] == -4 and intact,
                 "l'enregistrement #0 REJOUÉ après la chaîne : la séquence "
                 "a avancé, l'étiquette ne colle plus → rax = −4 NOMMÉ, la "
                 "charge et le type INTACTS — L'ANTI-REJOUE DU PROTOCOLE "
                 "tient dans la cryptographie, pas dans un compteur de "
                 "logique (Q5 de tls13-21)")

    # (d) l'oracle différentiel : des enregistrements aléatoires contre la
    # référence (l'émulation NUE pour les longues exécutions)
    rng = random.Random(graine)
    ecarts, joues = 0, 0
    for _ in range(60):
        cle = bytes(rng.randrange(256) for _ in range(16))
        iv = bytes(rng.randrange(256) for _ in range(12))
        seq0 = rng.randrange(0, 1 << 32)
        type_contenu = rng.choice((TYPE_ALERT, TYPE_HANDSHAKE, TYPE_DATA))
        charge = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 200)))
        ref_ctx = Contexte(cle, iv, seq0)
        attendu = ref_proteger(ref_ctx, type_contenu, charge)
        ctx = Contexte(cle, iv, seq0)
        emis, r = proteger(nue, ctx, type_contenu, charge)
        joues += 1
        if not (r["rax"] == 0 and emis == attendu and ctx.seq == seq0 + 1):
            ecarts += 1
            continue
        ctx2 = Contexte(cle, iv, seq0)
        rendu, type_r, _, r2 = deproteger(nue, ctx2, attendu)
        joues += 1
        if not (r2["rax"] == 0 and rendu == charge
                and type_r == bytes([type_contenu]) and ctx2.seq == seq0 + 1):
            ecarts += 1
    controle("V2.d:l-oracle-differentiel-60-enregistrements", ecarts == 0,
             f"{joues} exécutions (60 scellages + 60 déscellages, les "
             "charges de 0 à 199 o, les séquences jusqu'à 2^32, les TROIS "
             "types de contenu) — ZÉRO écart contre la référence")


# --- V3 : les cas punitifs (les bornes, les refus, l'ordre) -------------------------

def vecteur_v3(emul: Emulation, nue: Emulation, graine: int):
    section("V3 — les cas punitifs (la borne, le type passe-plat, les refus, l'ordre)")
    rng = random.Random(graine ^ 0xC0FFEE)
    cle = bytes(rng.randrange(256) for _ in range(16))
    iv = bytes(rng.randrange(256) for _ in range(12))

    # (a) LA BORNE : N = 2^14−1 scellé puis ouvert (le texte interne
    # 2^14 == EXACTEMENT la borne de la brique) ; N = 2^14 → le -3
    # PROPAGÉ (le texte interne 2^14+1 : le maximal du protocole REFUSÉ
    # par la composition — la fragmentation à l'appelant) ; N = 2^14+1 → -2
    grande = bytes(rng.randrange(256) for _ in range(2**14 - 1))
    ctx = Contexte(cle, iv, seq=0)
    emis, r = proteger(nue, ctx, TYPE_DATA, grande)
    ctx2 = Contexte(cle, iv, seq=0)
    rendu, type_r, _, r2 = deproteger(nue, ctx2, emis)
    controle("V3.a:la-borne-n-2-14-moins-1",
             r["rax"] == 0 and len(emis) == 5 + 16383 + 17
             and r2["rax"] == 0 and rendu == grande
             and type_r == bytes([TYPE_DATA]),
             "N = 16383 scellé PUIS ouvert, le clair rendu OCTET POUR "
             "OCTET — le texte interne 16384 == la borne P4 de tls13-18")
    S = nue
    S.uc.mem_write(ADR_EMIS, CANARI * 0x100)
    _, r = proteger(S, Contexte(cle, iv, seq=0), TYPE_DATA, bytes(2**14))
    vierge = bytes(S.uc.mem_read(ADR_EMIS, 0x60)) == CANARI * 0x60
    controle("V3.b:la-borne-n-2-14-le-moins-3-propage",
             r["rax"] == -3 and vierge,
             "N = 2^14 (LA borne TLSPlaintext) : le texte interne 2^14+1 "
             "HORS la brique → le verdict PROPAGÉ de 18, rax = −3 NOMMÉ, "
             "la sortie VIERGE, la séquence INCHANGÉE — l'émission "
             "effective est bornée à 2^14−1, la FRAGMENTATION est à "
             "l'APPELANT (RFC 8446 § 5.1 : le choix de fragmentation est libre)")
    _, r = proteger(emul, Contexte(cle, iv, seq=0), TYPE_DATA, bytes(2**14 + 1))
    controle("V3.c:la-borne-n-2-14-plus-1-le-moins-2",
             r["rax"] == -2, "N = 16385 > TLSPlaintext.length → rax = −2 NOMMÉ")

    # (b) le type PASSE-PLAT : 21 alerte, 22 poignée, 23 données — le type
    # réel vit DANS le chiffré, l'enregistrement émis est TOUJOURS opaque
    tous = True
    for type_contenu in (TYPE_ALERT, TYPE_HANDSHAKE, TYPE_DATA):
        ctx = Contexte(cle, iv, seq=0)
        emis, r = proteger(emul, ctx, type_contenu, b"charge")
        ref_ctx = Contexte(cle, iv, seq=0)
        attendu = ref_proteger(ref_ctx, type_contenu, b"charge")
        tous = tous and (r["rax"] == 0 and emis == attendu
                         and emis[0] == 23)
    controle("V3.d:le-type-passe-plat (21/22/23)", tous,
             "le type réel DEVIENT le dernier octet du texte interne ; "
             "l'enregistrement émis est TOUJOURS de type opaque 23 — "
             "l'en-tête ne trahit JAMAIS l'étage")

    # (c) L'INDIFFÉRENCE : N = 0 avec le pointeur de charge NUL — le
    # couple longueur/pointeur, jamais le pointeur seul
    ctx = Contexte(cle, iv, seq=0)
    S = emul
    poser_contexte(S, ctx)             # LE CONTEXTE POSÉ (la leçon du
                                        # premier jet : jamais d'appel sans
                                        # son contexte — la faute du harnais
                                        # nommée par l'échec)
    S.uc.mem_write(ADR_CHARGE & ~0xFFF, CANARI * 0x1000)
    S.uc.mem_write(ADR_EMIS, CANARI * 0x100)
    r = S.appeler(L.TLS20_VA, {"rcx": ADR_CTX, "rdx": TYPE_ALERT,
                                "r8": 0, "r9": 0},
                  args_pile=[ADR_EMIS])
    emis0 = bytes(S.uc.mem_read(ADR_EMIS, 22))
    controle("V3.e:l-indifference-n-0-charge-nulle",
             r["rax"] == 0 and len(emis0) == 22 and emis0[0] == 23
             and lire_sequence(S) == 1,
             "N = 0, r8 NUL : l'alerte VIDE scellée (l'en-tête + le type "
             "seul + l'étiquette : 22 o) — la charge n'est PAS lue, PAS un "
             "refus (le miroir de l'AAD de 18 : le couple, jamais le pointeur)")

    # (f) les refus -1 : les pointeurs nuls (20 : le contexte, la charge si
    # N > 0, la sortie ; 21 : le contexte, l'enregistrement, la charge, le type)
    ok_20 = True
    for champ in ("rcx", "r8"):
        _, r = proteger(emul, Contexte(cle, iv, seq=0), TYPE_DATA,
                        b"x", force={champ: 0})
        ok_20 = ok_20 and r["rax"] == -1
    _, r = proteger(emul, Contexte(cle, iv, seq=0), TYPE_DATA,
                    b"x", force={"sortie": 0})
    ok_20 = ok_20 and r["rax"] == -1
    controle("V3.f:les-refus-1-de-20 (les pointeurs)", ok_20,
             "le contexte, la charge (si N > 0), la sortie — chaque refus NOMMÉ")
    ctx_ok = Contexte(cle, iv, seq=0)
    rec_ok = ref_proteger(Contexte(cle, iv, seq=0), TYPE_DATA, b"charge utile")
    ok_21 = True
    for champ in ("rcx", "rdx", "r9"):
        _, _, _, r = deproteger(emul, ctx_ok, rec_ok, force={champ: 0})
        ok_21 = ok_21 and r["rax"] == -1
    _, _, _, r = deproteger(emul, ctx_ok, rec_ok, force={"type": 0})
    ok_21 = ok_21 and r["rax"] == -1
    controle("V3.g:les-refus-1-de-21 (les pointeurs)", ok_21,
             "le contexte, l'enregistrement, la charge, le type — chaque refus NOMMÉ")

    # (h) les confrontations de l'en-tête : le type ≠ 23 → -1 ; déclarée ≠
    # reçue → -2 ; le total < 5+18 → -2 ; déclaré > 2^14+16 → -2 (la borne
    # de la brique) ; LA VERSION HÉRITAGE mutée → -4 (l'AAD couvre ce que
    # la logique ignore — RFC 8446 § 5.1 « MUST be ignored »)
    ctx5 = Contexte(cle, iv, seq=0)
    rec = ref_proteger(Contexte(cle, iv, seq=0), TYPE_DATA, b"charge utile")
    mutes = [("le type d'en-tête ≠ 23", bytearray([22]) + bytearray(rec[1:]), -1),
             ("déclarée ≠ reçue", (lambda b: b[:4] + bytes([b[4] ^ 1]) + b[5:])(bytearray(rec)), -2),
             ("le total < 5+18", bytearray(rec[:20]), -2),
             ("LA VERSION héritage mutée", (lambda b: bytes([b[0], b[1] ^ 0xFF]) + b[2:])(bytearray(rec)), -4)]
    ok, details = True, []
    for nom, m, attendu in mutes:
        rendu, type_r, _, r = deproteger(emul, ctx5, bytes(m))
        if r["rax"] != attendu:
            ok = False
            details.append(f"{nom}:rax={r['rax']}≠{attendu}")
    controle("V3.h:les-confrontations-de-l-en-tete", ok,
             "le type → −1 ; la longueur → −2 ; le minimum → −2 ; LA "
             "VERSION : IGNORÉE par la logique (RFC 8446 § 5.1 « MUST be "
             "ignored ») mais COUVERTE par l'AAD : la mutation → −4 — la "
             "cryptographie attrape ce que la logique ignore"
             + (f" — DÉFAUTS : {details}" if details else ""))

    # (i) L'ORDRE : la séquence AVANCE après le succès, JAMAIS après
    # l'échec (le -3 et le -4 ne bougent RIEN) — l'enregistrement du cas
    # de succès scellé À LA séquence du contexte (7), la faute du premier
    # jet : scellé à 0, ouvert à 7 — l'échec était le HARNAIS, pas le bloc
    rec7 = ref_proteger(Contexte(cle, iv, seq=7), TYPE_HANDSHAKE, b"abc")
    ctx6 = Contexte(cle, iv, seq=7)
    _, r = proteger(emul, ctx6, TYPE_HANDSHAKE, b"abc")
    avance = lire_sequence(emul) == 8
    _, r = proteger(emul, Contexte(cle, iv, seq=7), TYPE_HANDSHAKE, bytes(2**14))
    fige_3 = lire_sequence(emul) == 7
    ctx7 = Contexte(cle, iv, seq=7)
    _, _, _, r = deproteger(emul, ctx7, rec7)
    avance_apres = lire_sequence(emul) == 8
    ctx8 = Contexte(cle, iv, seq=7)
    rec_faux = bytearray(rec7)
    rec_faux[-1] ^= 1
    _, _, _, r = deproteger(emul, ctx8, bytes(rec_faux))
    fige_4 = lire_sequence(emul) == 7
    controle("V3.i:l-ordre-de-la-sequence",
             avance and fige_3 and avance_apres and fige_4,
             "le succès 7 → 8 (le scellement ET le déscellement) ; le −3 "
             "et le −4 : la séquence FIGÉE à 7 — un échec n'avance JAMAIS "
             "(Q1 de 20, Q3 de 21)")


# --- V4 : le contrat ---------------------------------------------------------------

def vecteur_v4(emul: Emulation):
    section("V4 — le contrat (les pré/post de chaque bloc, sur pièces)")
    rng = random.Random(20261107)
    cle = bytes(rng.randrange(256) for _ in range(16))
    iv = bytes(rng.randrange(256) for _ in range(12))
    charge = bytes(rng.randrange(256) for _ in range(37))

    # (a) les non-volatiles rendus + la pile équilibrée + les canaris : un
    # cas représentatif de CHAQUE bloc (le cadre 0x4078, la zone morte
    # PROFONDE à −0x5000)
    ok_nv, details = True, []
    ctx = Contexte(cle, iv, seq=3)
    emis, r = proteger(emul, ctx, TYPE_DATA, charge)
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"]
            and r["logements_intacts"] and r["rax"] == 0):
        ok_nv = False
        details.append("tls13-20")
    ctx2 = Contexte(cle, iv, seq=3)
    rendu, type_r, _, r = deproteger(emul, ctx2, emis)
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"]
            and r["logements_intacts"] and r["rax"] == 0):
        ok_nv = False
        details.append("tls13-21")
    controle("V4.a:non-volatiles-pile-canaris (les deux blocs)", ok_nv,
             "les 8 sentinelles rendues, rsp équilibrée, l'ombre et le "
             "logement intacts, la zone morte PROFONDE à −0x5000 intacte "
             "(sous le cadre NOMMÉ 0x4078)"
             + (f" — DÉFAUTS : {details}" if details else ""))

    # (b) l'alignement msx64 à travers la composition : à CHAQUE entrée de
    # TLS18 (par 20) et TLS19 (par 21) — les comptes exacts
    emul.surveillance = {va: [] for va in (L.TLS18_VA, L.TLS19_VA)}
    try:
        proteger(emul, Contexte(cle, iv, seq=0), TYPE_DATA, charge)
        deproteger(emul, Contexte(cle, iv, seq=0), emis)
    finally:
        entrees = {va: list(l) for va, l in emul.surveillance.items()}
        emul.surveillance = None
    total = sum(len(l) for l in entrees.values())
    ok_align = total == 2 and all(e % 16 == 8
                                  for l in entrees.values() for e in l)
    controle("V4.b:l-alignement-msx64-a-l-entree-de-chaque-calle",
             ok_align and len(entrees[L.TLS18_VA]) == 1
             and len(entrees[L.TLS19_VA]) == 1,
             f"{total} entrées surveillées (TLS18 ×{len(entrees[L.TLS18_VA])} "
             f"par 20, TLS19 ×{len(entrees[L.TLS19_VA])} par 21) — rsp ≡ 8 "
             "(mod 16) chacune, UNE composition par bloc")

    # (c) LES ENTRÉES INTACTES : la charge (Q2 de 20), l'enregistrement
    # reçu (Q4 de 21), ET LE CONTEXTE RÉÉCRIT SUR SA SÉQUENCE SEULE (Q2)
    # — l'enregistrement du déscellement scellé À LA séquence du contexte
    # (41), la même leçon : la divergence de séquence N'EST PAS un défaut
    # du bloc, c'est l'anti-rejoue qui PARLE
    ctx3 = Contexte(cle, iv, seq=41)
    rec41 = ref_proteger(Contexte(cle, iv, seq=41), TYPE_DATA, charge)
    proteger(emul, ctx3, TYPE_DATA, charge)
    ok_charge = emul.intact_autour(ADR_CHARGE, len(charge))
    ctx4 = Contexte(cle, iv, seq=41)
    deproteger(emul, ctx4, rec41)
    ok_recu = emul.intact_autour(ADR_RECU, len(rec41))
    octets_ctx = bytes(emul.uc.mem_read(ADR_CTX, 192))
    ok_ctx = (octets_ctx == ctx4.serialiser()[:192]
              and lire_sequence(emul) == 42)
    controle("V4.c:les-entrees-et-le-contexte-intacts (Q2/Q4)",
             ok_charge and ok_recu and ok_ctx,
             "la charge et l'enregistrement reçu relus OCTET POUR OCTET ; "
             "le contexte : les 192 premiers octets (les clés de tour, "
             "l'IV, la réserve) OCTET-IDENTIQUES, LA SÉQUENCE SEULE "
             "avancée 41 → 42 — le contexte réécrit sur sa séquence seule")

    # (d) les sorties JAMAIS dépassées : les canaris après l'émission,
    # la charge restituée et le type
    ok_dep = (emul.intact_autour(ADR_EMIS, len(charge) + 22)
              and emul.intact_autour(ADR_RENDU, len(charge))
              and emul.intact_autour(ADR_TYPE, 1))
    controle("V4.d:les-sorties-jamais-depassee", ok_dep,
             f"les canaris après l'enregistrement émis ({len(charge) + 22} "
             "o), la charge restituée (37 o) et le type intacts")

    # (e) les refus SANS corruption : le -3 laisse la sortie VIERGE (le
    # fail-closed de 20 : l'en-tête LOCALE jusqu'au succès) ; le -4 laisse
    # la charge et le type VIERGES
    emul.uc.mem_write(ADR_EMIS, CANARI * 0x100)
    _, r = proteger(emul, Contexte(cle, iv, seq=0), TYPE_DATA, bytes(2**14))
    vierge_3 = bytes(emul.uc.mem_read(ADR_EMIS, 0x60)) == CANARI * 0x60
    rec_faux = bytearray(emis)
    rec_faux[-1] ^= 1
    emul.uc.mem_write(ADR_RENDU, CANARI * 0x100)
    emul.uc.mem_write(ADR_TYPE, CANARI * 0x10)
    _, type_r, n_ch, r2 = deproteger(emul, Contexte(cle, iv, seq=0),
                                     bytes(rec_faux))
    vierge_4 = (bytes(emul.uc.mem_read(ADR_RENDU, n_ch)) == CANARI * n_ch
                and bytes(emul.uc.mem_read(ADR_TYPE, 1)) == CANARI)
    controle("V4.e:les-refus-sans-corruption",
             r["rax"] == -3 and vierge_3 and r2["rax"] == -4 and vierge_4,
             "le −3 : l'en-tête reste LOCALE, la sortie VIERGE ; le −4 : "
             "la charge et le type VIERGES — l'échec n'écrit RIEN (le "
             "fail-closed de la famille)")


# --- V5 : la falsification ---------------------------------------------------------

def vecteur_v5(emul: Emulation, nue: Emulation):
    section("V5 — la falsification (zéro silence)")
    rng = random.Random(0xFEED)
    cle = bytes(rng.randrange(256) for _ in range(16))
    iv = bytes(rng.randrange(256) for _ in range(12))
    charge = bytes(rng.randrange(256) for _ in range(53))
    rec_ref = ref_proteger(Contexte(cle, iv, seq=0), TYPE_DATA, charge)
    emis, r = proteger(emul, Contexte(cle, iv, seq=0), TYPE_DATA, charge)
    assert r["rax"] == 0 and emis == rec_ref

    # (a) la charge, le type et la SÉQUENCE mutés → l'enregistrement diverge
    attrapes, total = 0, 0
    for pos in (0, 26, 52):
        mute = bytearray(charge)
        mute[pos] ^= 1
        emis2, _ = proteger(nue, Contexte(cle, iv, seq=0), TYPE_DATA,
                            bytes(mute))
        total += 1
        attrapes += emis2 != rec_ref
    for type_m in (TYPE_ALERT, TYPE_HANDSHAKE):
        emis2, _ = proteger(nue, Contexte(cle, iv, seq=0), type_m, charge)
        total += 1
        attrapes += emis2 != rec_ref
    emis2, _ = proteger(nue, Contexte(cle, iv, seq=1), TYPE_DATA, charge)
    total += 1
    attrapes += emis2 != rec_ref
    controle("V5.a:charge-type-et-sequence-mutes-attrapes",
             attrapes == total,
             f"{attrapes}/{total} mutations — la charge (3 octets), le "
             "type (2 valeurs), LA SÉQUENCE du contexte (le nonce la "
             "porte : l'enregistrement diverge)")

    # (b) chaque octet du chiffré ET de l'étiquette muté → -4 (la garde
    # mutation par mutation — Q4 de 21, la falsification invitée)
    attrapes, total = 0, 0
    for pos in (5, 5 + len(charge) // 2, len(rec_ref) - 17):
        mute = bytearray(rec_ref)
        mute[pos] ^= 1
        _, _, _, r = deproteger(nue, Contexte(cle, iv, seq=0), bytes(mute))
        total += 1
        attrapes += r["rax"] == -4
    for pos in (0, 8, 15):
        mute = bytearray(rec_ref)
        mute[len(rec_ref) - 16 + pos] ^= 0x80
        _, _, _, r = deproteger(nue, Contexte(cle, iv, seq=0), bytes(mute))
        total += 1
        attrapes += r["rax"] == -4
    controle("V5.b:le-chiffre-et-l-etiquette-mutes-attrapes",
             attrapes == total,
             f"{attrapes}/{total} mutations (le chiffré au premier/milieu/"
             "dernier octet, l'étiquette aux octets 0/8/15) → rax = −4 "
             "NOMMÉ — l'AAD couvre l'en-tête, l'étiquette couvre le reste")

    # (c) l'en-tête reçue mutée : le type → -1, la longueur → -2, LA
    # VERSION → -4 (la cryptographie attrape ce que la logique ignore —
    # LE TEST NOMMÉ par la spec : « les octets version reçus restent
    # couverts par l'AAD »)
    attrapes, total = 0, 0
    for pos, attendu in ((0, -1), (3, -2), (4, -2), (1, -4), (2, -4)):
        mute = bytearray(rec_ref)
        mute[pos] ^= 1
        _, _, _, r = deproteger(nue, Contexte(cle, iv, seq=0), bytes(mute))
        total += 1
        attrapes += r["rax"] == attendu
    controle("V5.c:l-en-tete-mutee-le-verdict-juste", attrapes == total,
             f"{attrapes}/{total} mutations : l'octet 0 (le type) → −1, "
             "les octets 3/4 (la longueur) → −2, LES OCTETS 1/2 (LA "
             "VERSION héritage) → −4 — la logique les ignore, l'AAD les "
             "couvre : la cryptographie attrape ce que la logique ignore")

    # (d) la REJOUE d'un enregistrement consommé → -4 (l'anti-rejoue)
    ctx = Contexte(cle, iv, seq=0)
    deproteger(nue, ctx, rec_ref)
    rendu, type_r, n_ch, r = deproteger(nue, ctx, rec_ref)
    controle("V5.d:la-rejoue-attrapee",
             r["rax"] == -4 and rendu == CANARI * n_ch,
             "l'enregistrement consommé REJOUÉ : la séquence a avancé, "
             "l'étiquette ne colle plus → −4, la sortie INTACTE — la "
             "preuve de l'anti-rejoue du protocole tient dans la "
             "cryptographie")

    # (e) la comparaison n'est pas muette (l'instrument se prouve non vide)
    attrapes, total = 0, 0
    for bit in (0, 63, 127):
        mute = bytearray(rec_ref)
        mute[bit // 8] ^= 1 << (bit % 8)
        total += 1
        attrapes += bytes(mute) != rec_ref
    controle("V5.e:la-comparaison-n-est-pas-muette", attrapes == total,
             f"{attrapes}/{total} enregistrements attendus mutés → l'égalité ÉCHOUE")


# --- V6 : le temps constant mesuré ---------------------------------------------------

def vecteur_v6(emul: Emulation, graine: int):
    section("V6 — le temps constant MESURÉ (I3, la charte § 3)")
    rng = random.Random(graine ^ 0x7)

    # (a) le scellement : 2 charges de même longueur (contenus et clés
    # différents) → LE MÊME compte — la longueur publique, le contenu jamais
    comptes = []
    for _ in range(2):
        cle = bytes(rng.randrange(256) for _ in range(16))
        charge = bytes(rng.randrange(256) for _ in range(45))
        _, r = proteger(emul, Contexte(cle, bytes(12), seq=0),
                        TYPE_DATA, charge, compter=True)
        comptes.append(r["compteur"])
    controle("V6.a:le-scellage-compte-constant", len(set(comptes)) == 1,
             f"2 scellages (clés ET charges différentes, N = 45), "
             f"{comptes[0]} instructions EXACTEMENT")

    # (b) le déscellement : 2 enregistrements conformes de même longueur
    # → LE MÊME compte
    comptes = []
    for _ in range(2):
        cle = bytes(rng.randrange(256) for _ in range(16))
        charge = bytes(rng.randrange(256) for _ in range(45))
        rec = ref_proteger(Contexte(cle, bytes(12), seq=0), TYPE_DATA, charge)
        _, _, _, r = deproteger(emul, Contexte(cle, bytes(12), seq=0),
                                rec, compter=True)
        comptes.append(r["compteur"])
    controle("V6.b:le-descellage-compte-constant", len(set(comptes)) == 1,
             f"2 déscellages conformes, {comptes[0]} instructions EXACTEMENT")

    # (c) LE VERDICT : trois enregistrements divergents (le chiffré muté
    # au PREMIER, au MILIEU, au DERNIER octet) → LE MÊME compte — le -4
    # hérité de tls13-19 ne court-circuite pas, la position de la
    # divergence est invisible dans le temps
    cle = bytes(rng.randrange(256) for _ in range(16))
    charge = bytes(rng.randrange(256) for _ in range(45))
    rec = ref_proteger(Contexte(cle, bytes(12), seq=0), TYPE_DATA, charge)
    comptes = []
    for pos in (5, 5 + len(charge) // 2, len(rec) - 17):
        mute = bytearray(rec)
        mute[pos] ^= 1
        _, _, _, r = deproteger(emul, Contexte(cle, bytes(12), seq=0),
                                 bytes(mute), compter=True)
        comptes.append(r["compteur"])
    controle("V6.c:le-verdict-compte-constant", len(set(comptes)) == 1,
             f"3 enregistrements divergents (le chiffré muté au premier, "
             f"milieu, dernier octet), {comptes[0]} instructions "
             "EXACTEMENT — la position de la divergence INVISIBLE dans le "
             "temps (I3 hérité de 19)")


# --- Le verdict ----------------------------------------------------------------------

def main() -> int:
    graine = 20261107
    if "--graine" in sys.argv:
        graine = int(sys.argv[sys.argv.index("--graine") + 1])
    print("=== tls13/harnais_enregistrement.py — LE HARNAIS DE LA FAMILLE "
          "enregistrement (chantier M9-(b), le geste cinq) ===")
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
