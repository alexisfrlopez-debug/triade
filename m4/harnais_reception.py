#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_reception.py — Harnais à propriétés de tls-07 (réception déchiffrée, D89 session).

La notation est émulée à ses RVA .text3 exacts AVEC les vrais octets de ses
dépendances (tls-02 verdicts, tls-03 descripteurs, libc-01 copie — héritage
scellé lu au dépôt m1, R7) ; l'IAT secur32 reçoit une fausse adresse
(résolution chargeur, mécanisme M2/M3 : page trampoline de ret + crochet
code). AUCUNE socket ici : tls-07 est un bloc de bibliothèque et de mémoire
— la réception tcp-03 est l'affaire de l'APPELANT tls-08 (I2). Vecteurs de
la spécification tls-07:R1 :

  V1  round-trip de notation 100 % (taille totale == « Code : N o », padding
      >= 16 — D8) pour tls-07 ET les trois blocs intégrés ;
  V2  oracle à shims — les scénarios de la spec, en CHAÎNES d'appels (le
      rôle appelant tls-08 est joué par le harnais : il lit la géométrie
      de la région vivante AU CADRE — champs D89 +0x3A/+0x3C — et
      réceptionne PAR-DESSUS, à zone+offset+longueur, jamais ailleurs) :
      enregistrement exact ; incomplet par un octet (Q2 puis Q1 après un
      octet de plus) ; deux enregistrements + Extra dans un même lot
      (Q1 puis Q1, résidu déplacé — le span du premier appel reste INTACT
      en zone : la preuve géométrique de la normalisation à l'appel
      SUIVANT) ; close_notify pur (Q3) ; close_notify avec résidu (E3,
      curiosité consignée) ; altération (E1) ; densité hostile par le lot
      ET par l'offset (E2 — zone et champs INTACTS, la garde étendue D89) ;
      verdicts 3 et 6 (table TOTALE) ; normalisation depuis un état offset
      non nul ; lot vide ; fin de contexte après un enregistrement —
      CHAQUE appel finit par l'état du cadre ET de la zone de réception
      EXACTEMENT PRÉDITS (image 0xD000 octet par octet : verdict, HRESULT
      d'origine, champs +0x3A/+0x3C, clair déchiffré, résidu brut — Q5 :
      zéro clair hors span livré) + le contrat d'appels complet (DM :
      phContext cadre+0x10, pMessage/pfQOP prédicats pile, MessageSeqNo 0,
      pfQOP réécrit 0 avant l'appel, descripteur tls-03 type 2 exact —
      DATA zone entière + 3 EMPTY) ;
  V3  fuzzing à propriétés : lots et offsets hostiles (les bornes E2
      visées exprès), verdicts shim aléatoires (documentés ET exotiques),
      géométries d'enregistrement aléatoires — survie, terminaison, ZÉRO
      écart contre le modèle ; PLUS des CHAÎNES fuzzées (l'appelant
      réceptionne par-dessus la région vivante lue au cadre entre les
      appels — la convention D89 éprouvée de bout en bout) ;
  V4  falsification : DIX mutations D'UN SEUL point de la notation, STABLES
      EN TAILLE (leçon D82), chacune ATTRAPÉE par le différentiel — dont la
      FRONTIÈRE EXACTE de la garde E2 (32769) ; le témoin intact reste vert.
      (Une onzième mutation — garde du lot SEUL relâchée — fut IMPOSSIBLE à
      attraper : la garde somme la SUBSUME ; une garde redondante est
      infalsifiable, elle a été SUPPRIMÉE de la notation — le différentiel
      nomme aussi ce qu'il ne peut pas prouver.)

Règles shims PARTAGÉES modèle/émulation (jamais deux sources de vérité —
règles D89, layout.py) : DecryptMessage en succès (ou fin de contexte)
déchiffre SUR PLACE — le clair (motif déterministe) remplace le brut à
l'offset de l'en-tête d'enregistrement — et réécrit le tampon 0 (cb =
longueur claire, DATA, pv = zone + en-tête) et le tampon 1 (cb = résidu
Extra, EXTRA, pv = zone + consommé) ; en message incomplet le tampon 0
devient (octets manquants, MISSING) SANS toucher la zone ; tout autre
verdict n'écrit RIEN ; pfQOP reçoit des drapeaux déterministes non nuls
en succès (la notation DOIT réécrire 0 avant chaque appel — falsifiable).
Descripteur invalide (notation mutée) : SEC_E_INVALID_TOKEN, fail-closed,
aucune écriture.

Le modèle de référence est écrit depuis la SPÉCIFICATION (jamais la
notation) : verdict_modele via layout.HRESULTS, cadre aux offsets
layout.CADRE_*, région vivante via layout.CADRE_UTILE/CADRE_OFFSET,
capacité layout.CAPACITE_RECEPTION (jamais constante inventée).
Les adresses de PILE du descripteur et de pfQOP sont vérifiées par
PRÉDICAT — l'adresse exacte appartient à la notation, le CONTENU au contrat.
Usage : python3 harnais_reception.py [--graine G] [--cas N] [--chaines N]
"""

from __future__ import annotations

import argparse
import os
import random
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, "outils"))
import layout as L  # noqa: E402

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE  # noqa: E402
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
    "r15": UC_X86_REG_R15, "rip": UC_X86_REG_RIP}

# --- Mémoire du harnais (émulation nue à les RVA du plan, mécanisme D79) ----------

ZONE_LIBC = 0x1000              # page .text : libc-01 @0x1100
TAILLE_LIBC = 0x1000
ZONE_RDATA = 0x2000             # page .rdata : IAT kernel32/ws2_32/secur32 + fixture
TAILLE_RDATA = 0x1000
ZONE_CODE = 0x6000              # page .text3 : tls-02/03/07 (le bloc sous test)
TAILLE_CODE = 0x1000
RET_MAGIQUE = 0x6F00            # adresse d'arrêt propre (int3 de la page code)
TRAMPOLINE = 0x140100000        # fausses adresses d'API (page RX, mécanisme M2/M3)
TAILLE_TRAMP = 0x1000
ZONE_CADRE = 0x150000000        # cadre de session TLS complet (0xC260, D89) + marge
TAILLE_CADRE_PAGE = 0xD000      # 0xC260 + canaris I4 (aucune écriture hors cadre)
ZONE_SPAN = 0x160000000         # span de sortie de l'appelant + canaris
TAILLE_SPAN = 0x10000
MARGE_SPAN = 0x100
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP = 0x7F008000

RVA_TLS07, SLOT_TLS07 = 0x6A40, 0x300
RVA_TLS02, SLOT_TLS02 = 0x6080, 0x100
RVA_TLS03, SLOT_TLS03 = 0x6180, 0x140
RVA_MEMCPY = 0x1100

ZONE_RECEPTION = ZONE_CADRE + L.CADRE_RECEPTION   # la zone DANS le cadre (D89)

# fausses adresses : secur32 (7) + le reste des imports M3 (toute frappe =
# faux pas nommé — I2/I3 : seul DecryptMessage est légitime ici)
FAUX = {nom: TRAMPOLINE + (i + 1) * 0x10
        for i, nom in enumerate(L.SECUR32_IMPORTS)}
FAUX.update({"recv": TRAMPOLINE + 0x100, "send": TRAMPOLINE + 0x110})
for i, (nom, _rva) in enumerate(L.IAT_SLOTS.items()):
    if nom not in FAUX:
        FAUX[nom] = TRAMPOLINE + 0x200 + i * 0x10
FAUX_REV = {v: k for k, v in FAUX.items()}

CANARI = b"\xA5"
SENTINELLES_NV = {
    "rbx": 0x1212121212121212, "rbp": 0x2323232323232323,
    "rdi": 0x3434343434343434, "rsi": 0x4545454545454545,
    "r12": 0x5656565656565656, "r13": 0x6767676767676767,
    "r14": 0x7878787878787878, "r15": 0x89898989898989,
}
MAGIC_CRED = (0xC1C1C1C1C1C1C1C1, 0xC2C2C2C2C2C2C2C2)   # acquis par tls-05 — intouchable
MAGIC_FINAL = (0xABABABABABABABAB, 0xCDCDCDCDCDCDCDCD)  # contexte ÉTABLI par tls-04 (P1)
SOCKET_SERVEUR = 0x7777777777777777

REUSSITES, ECHECS = [], []


def controle(nom: str, ok: bool, detail: str = "") -> None:
    if ok:
        REUSSITES.append(nom)
        print(f"  [PASS] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append(nom)
        print(f"  [FAIL] {nom}" + (f" — {detail}" if detail else ""))


# --- Motifs déterministes (partagés modèle/shims — dépendance en i ET en j) ------

_PATS = [bytes(((i * 31 + j * 7 + 11) & 0xFF) for j in range(256)) for i in range(64)]


def motif(i: int, n: int) -> bytes:
    if n <= 0:
        return b""
    p = _PATS[i % 64]
    return (p * ((n // 256) + 1))[:n]


def clair_dm(i: int, n: int) -> bytes:
    """Octets clairs déchiffrés SUR PLACE par la « bibliothèque » (règle D89)."""
    return motif(500 + i, n)


# --- V1 : round-trip ------------------------------------------------------------

def lignes_notation(chemin: str) -> list[str]:
    lignes = []
    with open(chemin, encoding="utf-8") as f:
        for brut in f:
            ligne = brut.split(";")[0].strip()
            if ligne:
                lignes.append(ligne)
    return lignes


def assembler_lignes(ks: Ks, lignes: list[str], rva: int) -> bytes:
    sortie, adresse = [], rva
    for ligne in lignes:
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise RuntimeError(f"ligne inassemblable à 0x{adresse:x} : {ligne!r}")
        sortie.append(bytes(enc))
        adresse += len(enc)
    return b"".join(sortie)


def octets_notation(ks: Ks, bloc: str, rva: int, mutation: tuple[str, str] | None = None,
                    chemin: str | None = None):
    chemin = chemin or os.path.join(ICI, "notation", bloc + ".asm")
    lignes = lignes_notation(chemin)
    declare = None
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            if ligne.startswith("; Code : "):
                declare = int(ligne.split("Code : ")[1].split(" o ")[0])
    if mutation:
        avant, apres = mutation
        cibles = [i for i, l in enumerate(lignes) if avant in l]
        if len(cibles) != 1:
            raise RuntimeError(f"mutation ambiguë ({len(cibles)} occurrences) : {avant!r}")
        lignes[cibles[0]] = lignes[cibles[0]].replace(avant, apres)
        return assembler_lignes(ks, lignes, rva), None
    return assembler_lignes(ks, lignes, rva), declare


# --- Modèle de référence (écrit depuis la SPÉCIFICATION — jamais la notation) -----

def verdict_modele(hresult: int) -> int:
    """tls-02:R1 via la liste blanche de la spécification (layout.HRESULTS)."""
    return L.HRESULTS.get(hresult & 0xFFFFFFFF, L.VERDICT_FATAL)


def image_initiale(utile: int = 0, offset: int = 0, zone_brut: bytes = b"",
                   tailles: tuple | None = (5, 16, 512, 4, 8)) -> bytearray:
    """Cadre post-poignée : credentials acquis, contexte ÉTABLI, socket connectée,
    tailles consignées (tls-06 a couru), champs D89 (utile, offset) décrivant
    la région vivante de la zone — la zone porte le brut reçu."""
    page = bytearray(CANARI * TAILLE_CADRE_PAGE)

    def q(off, lo, hi):
        page[off:off + 16] = struct.pack("<QQ", lo, hi)   # SecHandle = 2 x u64
    q(L.CADRE_CRED, *MAGIC_CRED)
    q(L.CADRE_CTXT, *MAGIC_FINAL)
    q(L.CADRE_SOCKET, SOCKET_SERVEUR, 0)
    q(L.CADRE_PTR_NOM, ZONE_CADRE + L.CADRE_NOM_ZONE, 0)
    page[L.CADRE_TAILLES:L.CADRE_TAILLES + 20] = (
        struct.pack("<5I", *tailles) if tailles else b"\x00" * 20)
    struct.pack_into("<H", page, L.CADRE_UTILE, utile & 0xFFFF)
    struct.pack_into("<H", page, L.CADRE_OFFSET, offset & 0xFFFF)
    debut = L.CADRE_RECEPTION + offset
    fin = min(debut + len(zone_brut), L.CADRE_RECEPTION + L.CAPACITE_RECEPTION)
    if fin > debut:
        page[debut:fin] = zone_brut[:fin - debut]
    return page


class Script:
    """Comportements shims déterministes par INDICE d'appel (jamais de file
    épuisable) : dm[i] = (HRESULT, en-tête, clair, queue) — la géométrie du
    record traité au i-ème appel DecryptMessage ; le verdict dérive de
    l'HRESULT par tls-02, le résidu de lot − consommé (règles D89)."""

    def __init__(self, dm: list):
        self.entries_dm = dm

    def comportement_dm(self, i: int) -> tuple:
        if i < len(self.entries_dm):
            return self.entries_dm[i]
        return (0, 5, 256, 16)


class Modele:
    """La spécification tls-07:R1 en Python — même environnement shims. L'état
    (cadre + zone + span) VIT à travers les appels : le modèle est le miroir
    exact de ce que l'émulation doit produire, appel après appel."""

    def __init__(self, script: Script, image0: bytes):
        self.script = script
        self.page = bytearray(image0)
        self.span_page = bytearray(CANARI * TAILLE_SPAN)
        self.appels: list[tuple] = []
        self.i_dm = 0

    def _dw32(self, off, v):
        struct.pack_into("<I", self.page, off, v & 0xFFFFFFFF)

    def _w16(self, off, v):
        struct.pack_into("<H", self.page, off, v & 0xFFFF)

    def _r16(self, off) -> int:
        return struct.unpack_from("<H", self.page, off)[0]

    def step(self, lot: int) -> tuple[int, list]:
        """UN appel tls-07 — retourne (rax, contrat d'appels)."""
        self.appels = []
        # --- E2 : la région utile doit TENIR dans la zone (garde étendue D89 :
        # lot seul, PUIS offset + lot — AVANT tout appel, AVANT tout déplacement)
        if lot > L.CAPACITE_RECEPTION:
            self._dw32(L.CADRE_VERDICT, 5)
            return 5, self.appels
        off0 = self._r16(L.CADRE_OFFSET)
        if off0 + lot > L.CAPACITE_RECEPTION:
            self._dw32(L.CADRE_VERDICT, 5)
            return 5, self.appels
        # --- normalisation D89 : le lot vivant descend en tête (le clair pompé
        # --- est mort ; personne d'autre ne touche la zone entre deux appels)
        if off0:
            z = L.CADRE_RECEPTION
            self.page[z:z + lot] = self.page[z + off0:z + off0 + lot]
            self._w16(L.CADRE_OFFSET, 0)
        # --- descripteur tls-03 type 2 : la zone ENTIÈRE en DATA + 3 EMPTY
        desc_att = (0, 4, "PMSG",
                    [(lot, L.SECBUFFER_DATA, ZONE_RECEPTION),
                     (0, L.SECBUFFER_EMPTY, 0),
                     (0, L.SECBUFFER_EMPTY, 0),
                     (0, L.SECBUFFER_EMPTY, 0)])
        # --- DecryptMessage (règles D89)
        i = self.i_dm
        h, cbh, ln_c, cbt = self.script.comportement_dm(i)
        v = verdict_modele(h)
        self.appels.append(("DM", ZONE_CADRE + L.CADRE_CTXT, "PILE", 0,
                            "PILE", desc_att, 0))
        self.i_dm += 1
        self._dw32(L.CADRE_HRESULT, h)
        c = cbh + ln_c + cbt
        r = lot - c if lot > c else 0
        if v in (0, 4):
            # déchiffrement SUR PLACE : le clair remplace le brut à l'offset
            # de l'en-tête (les tampons 0/1 réécrits vivent sur la pile de la
            # notation — hors image vérifiée, le CONTRAT les porte ailleurs)
            z = L.CADRE_RECEPTION
            self.page[z + cbh:z + cbh + ln_c] = clair_dm(i, ln_c)
        # verdict 2 : MISSING dans le tampon 0 — la zone n'est PAS touchée ;
        # verdicts 1/3/5/6 : la bibliothèque n'écrit rien
        # --- post-états (le miroir EXACT de la notation, formule pour formule)
        if v == 0:
            self.span_page[MARGE_SPAN:MARGE_SPAN + 16] = struct.pack(
                "<QQ", ZONE_RECEPTION + cbh, ln_c)
            self._dw32(L.CADRE_VERDICT, 0)
            self._w16(L.CADRE_UTILE, r)
            self._w16(L.CADRE_OFFSET, lot - r)
            return 0, self.appels
        if v == 2:
            self._dw32(L.CADRE_VERDICT, 2)
            self._w16(L.CADRE_UTILE, lot)
            self._w16(L.CADRE_OFFSET, 0)
            return 2, self.appels
        if v == 4:
            self._dw32(L.CADRE_VERDICT, 4)
            self._w16(L.CADRE_UTILE, r)          # curiosité « fin propre avec résidu »
            self._w16(L.CADRE_OFFSET, 0)         # purgée : plus rien de vivant
            return 4, self.appels
        self._dw32(L.CADRE_VERDICT, v)
        self._w16(L.CADRE_UTILE, lot)
        self._w16(L.CADRE_OFFSET, 0)
        return v, self.appels


# --- Émulateur à shims SSPI (page ret + crochet code, mécanisme M2/M3) -----------

def _pile_valide(p: int) -> bool:
    return ZONE_PILE <= p < ZONE_PILE + TAILLE_PILE


class Emulateur:
    """Un chargement = un émulateur NEUF (leçon D79). Les pages CADRE et SPAN
    vivent à travers les appels (préparer UNE fois par chaîne, appeler autant
    de fois que la chaîne le demande) ; la PILE n'est JAMAIS réinitialisée —
    le pfQOP non nul laissé par un appel précédent éprouve la réécriture
    défensive de la notation (falsifiable)."""

    def __init__(self, blobs: dict):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        uc.mem_map(ZONE_LIBC, TAILLE_LIBC)
        uc.mem_map(ZONE_RDATA, TAILLE_RDATA)
        uc.mem_map(ZONE_CODE, TAILLE_CODE)
        uc.mem_map(TRAMPOLINE, TAILLE_TRAMP)
        uc.mem_map(ZONE_CADRE, TAILLE_CADRE_PAGE)
        uc.mem_map(ZONE_SPAN, TAILLE_SPAN)
        uc.mem_map(ZONE_PILE, TAILLE_PILE)
        page_libc = b"\xCC" * TAILLE_LIBC
        page_libc = (page_libc[:RVA_MEMCPY - ZONE_LIBC] + blobs["libc-01"] +
                     page_libc[RVA_MEMCPY - ZONE_LIBC + len(blobs["libc-01"]):])
        uc.mem_write(ZONE_LIBC, page_libc)
        page = b"\xCC" * TAILLE_CODE
        for rva, blob in ((RVA_TLS02, blobs["tls-02"]), (RVA_TLS03, blobs["tls-03"]),
                          (RVA_TLS07, blobs["tls-07"])):
            page = page[:rva - ZONE_CODE] + blob + page[rva - ZONE_CODE + len(blob):]
        uc.mem_write(ZONE_CODE, page)
        uc.mem_write(TRAMPOLINE, b"\xc3" * TAILLE_TRAMP)   # chaque shim retourne
        # résolution chargeur : IAT kernel32/ws2_32 + secur32 vers les fausses adresses
        for nom, rva in L.IAT_SLOTS.items():
            uc.mem_write(rva, struct.pack("<Q", FAUX[nom]))
        for nom, rva in L.IAT_SEC32_SLOTS.items():
            uc.mem_write(rva, struct.pack("<Q", FAUX[nom]))
        uc.mem_write(L.R_PKG_M4, L.PKG_M4)   # fixture tls-05 — doit rester intacte
        uc.hook_add(UC_HOOK_CODE, self._shim, begin=TRAMPOLINE, end=TRAMPOLINE + TAILLE_TRAMP)
        self.script: Script | None = None
        self.appels: list[tuple] = []
        self.faux_pas: list[str] = []
        self._i_dm = 0

    def _shim(self, uc: Uc, adresse: int, taille: int, donnees):
        nom = FAUX_REV.get(adresse)
        if nom is None:
            self.faux_pas.append(f"shim inconnu @{adresse:#x}")
            return
        methode = getattr(self, "_api_" + nom, None)
        if methode is None:
            self.faux_pas.append(f"{nom} appelé par tls-07 (I2/I3 violée)")
            return
        methode()

    # --- la SEULE API légitime (I2/I3 : DecryptMessage) ----------------------

    def _lire_desc_dm(self, p: int):
        """SecBufferDesc à 4 tampons (DATA/EMPTY/EMPTY/EMPTY) — None si invalide
        (notation mutée) : version, compte, types dans le contrat D89."""
        try:
            b = bytes(self.uc.mem_read(p, 16))
            ulv, nb = struct.unpack_from("<II", b, 0)
            (pb,) = struct.unpack_from("<Q", b, 8)
            if ulv != L.SECBUFFER_VERSION or nb != 4:
                return None
            bufs = []
            for k in range(4):
                bb = bytes(self.uc.mem_read(pb + 16 * k, 16))
                cb, typ = struct.unpack_from("<II", bb, 0)
                (pv,) = struct.unpack_from("<Q", bb, 8)
                bufs.append((cb, typ, pv))
            if [t for _, t, _ in bufs] != [L.SECBUFFER_DATA, L.SECBUFFER_EMPTY,
                                            L.SECBUFFER_EMPTY, L.SECBUFFER_EMPTY]:
                return None
            return (ulv, nb, pb, bufs)
        except Exception:
            return None

    def _api_DecryptMessage(self):
        uc = self.uc
        ph_ctxt = uc.reg_read(REGS["rcx"])
        p_msg = uc.reg_read(REGS["rdx"])
        seq = uc.reg_read(REGS["r8"]) & 0xFFFFFFFF
        pfqop = uc.reg_read(REGS["r9"])
        desc = self._lire_desc_dm(p_msg)
        qop_pre = None
        if _pile_valide(pfqop):
            qop_pre = struct.unpack("<I", bytes(uc.mem_read(pfqop, 4)))[0]
        self.appels.append(("DM", ph_ctxt, p_msg, seq, pfqop, desc, qop_pre))
        if desc is None:
            # descripteur invalide (notation mutée) — fail-closed, aucune écriture
            uc.reg_write(REGS["rax"], 0x80090308)
            return
        i = self._i_dm
        h, cbh, ln_c, cbt = self.script.comportement_dm(i)
        v = verdict_modele(h)
        lot = desc[3][0][0]
        c = cbh + ln_c + cbt
        r = lot - c if lot > c else 0
        if v in (0, 4):
            pv0 = desc[3][0][2]
            pb = desc[2]
            # déchiffrement SUR PLACE (règle D89) + tampons réécrits PAR la
            # bibliothèque (leçon D83 (d) : les longueurs produites consignées)
            uc.mem_write(pv0 + cbh, clair_dm(i, ln_c))
            uc.mem_write(pb + 0x00, struct.pack("<I", ln_c))
            uc.mem_write(pb + 0x04, struct.pack("<I", L.SECBUFFER_DATA))
            uc.mem_write(pb + 0x08, struct.pack("<Q", pv0 + cbh))
            uc.mem_write(pb + 0x10, struct.pack("<I", r))
            uc.mem_write(pb + 0x14, struct.pack("<I", L.SECBUFFER_EXTRA))
            uc.mem_write(pb + 0x18, struct.pack("<Q", pv0 + c))
        elif v == 2:
            # MISSING : octets manquants dans le tampon 0 — zone intacte
            manquant = c - lot if c > lot else 0
            pb = desc[2]
            uc.mem_write(pb + 0x00, struct.pack("<I", manquant))
            uc.mem_write(pb + 0x04, struct.pack("<I", L.SECBUFFER_MISSING))
        self._i_dm += 1
        if v == 0 and _pile_valide(pfqop):
            # drapeaux QOP déterministes NON NULS en succès — la notation DOIT
            # réécrire 0 avant chaque appel (aucun état résiduel, falsifiable)
            uc.mem_write(pfqop, struct.pack("<I", 2))
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

    # --- pilotage --------------------------------------------------------------

    def preparer(self, image0: bytes) -> None:
        """UNE fois par chaîne : le cadre arrive avec sa région vivante, le span
        vierge, les indices de script remis à zéro."""
        self.uc.mem_write(ZONE_CADRE, bytes(image0))
        self.uc.mem_write(ZONE_SPAN, CANARI * TAILLE_SPAN)
        self.appels = []
        self.faux_pas = []
        self._i_dm = 0

    def appeler(self, script: Script, lot: int) -> int:
        uc = self.uc
        self.script = script
        self.appels = []
        self.faux_pas = []
        for nom, valeur in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], valeur)
        uc.reg_write(REGS["rsp"], RSP)
        uc.mem_write(RSP, struct.pack("<Q", RET_MAGIQUE))
        uc.reg_write(REGS["rcx"], ZONE_CADRE)
        uc.reg_write(REGS["rdx"], ZONE_RECEPTION)
        uc.reg_write(REGS["r8"], lot)
        uc.reg_write(REGS["r9"], ZONE_SPAN + MARGE_SPAN)
        uc.emu_start(RVA_TLS07, RET_MAGIQUE, timeout=5_000_000, count=2_000_000)
        return uc.reg_read(REGS["rax"]) & 0xFFFFFFFF

    def lire16(self, off: int) -> int:
        return struct.unpack("<H", bytes(self.uc.mem_read(ZONE_CADRE + off, 2)))[0]

    def ecrire(self, off: int, brut: bytes) -> None:
        self.uc.mem_write(ZONE_CADRE + off, brut)

    def hygiene(self) -> list[str]:
        problemes = list(self.faux_pas)
        for nom, valeur in SENTINELLES_NV.items():
            if self.uc.reg_read(REGS[nom]) != valeur:
                problemes.append(f"non-volatil {nom} modifié (I5)")
        for nom, rva in {**L.IAT_SLOTS, **L.IAT_SEC32_SLOTS}.items():
            if struct.unpack("<Q", bytes(self.uc.mem_read(rva, 8)))[0] != FAUX[nom]:
                problemes.append(f"IAT {nom} réécrite")
        if bytes(self.uc.mem_read(L.R_PKG_M4, len(L.PKG_M4))) != L.PKG_M4:
            problemes.append("fixture package altérée")
        return problemes


# --- Comparaison des traces (champs exacts + prédicats pile) ----------------------

def comparer_traces(recues: list, attendues: list) -> list[str]:
    problemes: list[str] = []
    if len(recues) != len(attendues):
        problemes.append(f"trace d'appels : {len(recues)} appel(s) != "
                         f"{len(attendues)} attendu(s)")
    for k, (a, e) in enumerate(zip(recues, attendues)):
        if a[0] != e[0]:
            problemes.append(f"appel #{k} : {a[0]} != {e[0]}")
            continue
        # DM : (nom, phContext, pMessage, MessageSeqNo, pfQOP, desc, qop_pre)
        for idx, nomch in ((1, "phContext"), (3, "MessageSeqNo")):
            if a[idx] != e[idx]:
                problemes.append(f"DM #{k} {nomch} {a[idx]!r} != {e[idx]!r}")
        for idx, nomch in ((2, "pMessage"), (4, "pfQOP")):
            if not _pile_valide(a[idx]) or a[idx] % 8:
                problemes.append(f"DM #{k} {nomch} {a[idx]:#x} hors pile/aligné")
        if a[6] != e[6]:
            problemes.append(f"DM #{k} pfQOP pré-appel {a[6]!r} != {e[6]!r} "
                             "(réécriture 0 absente)")
        if e[5] is None:
            if a[5] is not None:
                problemes.append(f"DM #{k} descripteur présent à tort")
            continue
        if a[5] is None:
            problemes.append(f"DM #{k} descripteur ABSENT/invalide")
            continue
        ulv, nb, pb, bufs = a[5]
        if (ulv, nb) != (0, 4):
            problemes.append(f"DM #{k} descripteur (v={ulv}, n={nb}) != (0, 4)")
        if pb != a[2] + 0x10:
            problemes.append(f"DM #{k} pBuffers {pb:#x} != pMessage+0x10")
        for j, ((cb_a, t_a, pv_a), (cb_e, t_e, pv_e)) in enumerate(zip(bufs, e[5][3])):
            if (cb_a, t_a, pv_a) != (cb_e, t_e, pv_e):
                problemes.append(
                    f"DM #{k} tampon {j} (cb={cb_a}, t={t_a}, pv={pv_a:#x}) != "
                    f"(cb={cb_e}, t={t_e}, pv={pv_e:#x})")
    return problemes


# --- Differentiel -----------------------------------------------------------------

def _comparer_image(etiquette: str, rax: int, rax_att: int, emu: Emulateur,
                    modele: Modele, appels_att: list) -> list[str]:
    problemes: list[str] = []
    if rax != rax_att:
        problemes.append(f"rax {rax} != {rax_att} (modèle spec)")
    image_lue = bytes(emu.uc.mem_read(ZONE_CADRE, TAILLE_CADRE_PAGE))
    image_att = bytes(modele.page)
    if image_lue != image_att:
        off = next(o for o in range(TAILLE_CADRE_PAGE) if image_lue[o] != image_att[o])
        problemes.append(f"cadre diverge @+0x{off:x} (attendu {image_att[off]:#04x}, "
                         f"lu {image_lue[off]:#04x})")
    span_lu = bytes(emu.uc.mem_read(ZONE_SPAN, TAILLE_SPAN))
    span_att = bytes(modele.span_page)
    if span_lu != span_att:
        off = next(o for o in range(TAILLE_SPAN) if span_lu[o] != span_att[o])
        problemes.append(f"span diverge @+0x{off:x} (attendu {span_att[off]:#04x}, "
                         f"lu {span_lu[off]:#04x})")
    problemes += comparer_traces(emu.appels, appels_att)
    problemes += emu.hygiene()
    return problemes


def jouer_cas(emu: Emulateur, script: Script, etiquette: str, lot: int,
              utile: int, offset: int, zone_brut: bytes) -> list[str]:
    """Exécute UN appel contre le modèle — écarts nommés."""
    image0 = image_initiale(utile, offset, zone_brut)
    modele = Modele(script, bytes(image0))
    emu.preparer(bytes(image0))
    rax_att, appels_att = modele.step(lot)
    rax = emu.appeler(script, lot)
    return _comparer_image(etiquette, rax, rax_att, emu, modele, appels_att)


def jouer_chaine(emu: Emulateur, script: Script, etiquette: str, etapes: list,
                 offset0: int, longueur0: int, zone_brut: bytes) -> list[str]:
    """Exécute une CHAÎNE d'appels — le rôle appelant (tls-08) est joué par le
    harnais : il lit la géométrie AU CADRE après chaque appel (champs D89) et
    réceptionne PAR-DESSUS la région vivante, à zone+offset+longueur, jamais
    ailleurs (P2) ; la réception est bornée par la capacité restante (tcp-03
    à longueur maximale — miroir exact de l'appelant réel)."""
    image0 = image_initiale(longueur0, offset0, zone_brut)
    modele = Modele(script, bytes(image0))
    emu.preparer(bytes(image0))
    problemes: list[str] = []
    lot = longueur0
    for k, etape in enumerate(etapes):
        if etape[0] == "recv":
            n_voulu = etape[1]
            off = emu.lire16(L.CADRE_OFFSET)
            lng = emu.lire16(L.CADRE_UTILE)
            chambre = L.CAPACITE_RECEPTION - (off + lng)
            n = min(n_voulu, chambre)
            if n > 0:
                brut = motif(42 + k, n)
                pos = L.CADRE_RECEPTION + off + lng
                emu.ecrire(pos, brut)
                modele.page[pos:pos + n] = brut
            lot += n
        else:
            rax_att, appels_att = modele.step(lot)
            rax = emu.appeler(script, lot)
            ecarts = _comparer_image(f"{etiquette}/{k}", rax, rax_att, emu,
                                     modele, appels_att)
            if ecarts:
                problemes += [f"[étape {k}] {e}" for e in ecarts]
            # le lot suivant : la longueur utile LUE AU CADRE (rôle tls-08 —
            # la convention D89 en acte, champs pour champs)
            lot = emu.lire16(L.CADRE_UTILE)
    return problemes


# --- V2 : scénarios de la spécification -------------------------------------------

OK = 0x00000000
INCOMPLET = 0x80090318
CONTEXTE_EXPIRE = 0x00090317
ALTERE = 0x8009030F
CERT_INVALIDE = 0x80090325
EXOTIQUE = 0x81234567

# (nom, script, étapes, offset0, longueur0, zone_brut)
SCENARIOS_V2 = [
    ("enregistrement exact (un record, résidu nul)",
     Script([(OK, 5, 100, 16)]), [("appel",)], 0, 121, motif(7, 121)),
    ("incomplet par un octet — Q2 puis Q1 après un octet de plus",
     Script([(INCOMPLET, 5, 100, 16), (OK, 5, 100, 16)]),
     [("appel",), ("recv", 1), ("appel",)], 0, 120, motif(7, 120)),
    ("deux enregistrements + Extra dans un même lot — Q1 puis Q1, résidu déplacé "
     "(le span du premier appel reste INTACT : la normalisation est l'œuvre de "
     "l'appel SUIVANT)",
     Script([(OK, 5, 100, 16), (OK, 3, 40, 8)]),
     [("appel",), ("appel",)], 0, 172, motif(7, 172)),
    ("close_notify pur — Q3, fin propre sans résidu",
     Script([(CONTEXTE_EXPIRE, 5, 0, 16)]), [("appel",)], 0, 21, motif(7, 21)),
    ("close_notify avec résidu — E3, curiosité « fin propre avec résidu » consignée",
     Script([(CONTEXTE_EXPIRE, 5, 0, 16)]), [("appel",)], 0, 58, motif(7, 58)),
    ("altération en plein record — E1, verdict 5, HRESULT d'origine au cadre",
     Script([(ALTERE, 5, 100, 16)]), [("appel",)], 0, 121, motif(7, 121)),
    ("densité hostile par le lot — E2, zone et champs INTACTS (32769)",
     Script([(OK, 5, 100, 16)]), [("appel",)], 0, 32769, motif(7, 32768)),
    ("densité hostile par l'offset — E2 (garde étendue D89), zone et champs "
     "INTACTS (32500 + 500 > 32768)",
     Script([(OK, 5, 100, 16)]), [("appel",)], 32500, 500, motif(7, 268)),
    ("la FRONTIÈRE EXACTE de la garde — offset + lot = 32769 : E2, un octet "
     "de plus que la capacité",
     Script([(OK, 5, 100, 16)]), [("appel",)], 32269, 500, motif(7, 500)),
    ("la capacité EXACTE — offset + lot = 32768 : la garde passe, la région "
     "vit jusqu'au dernier octet de la zone",
     Script([(OK, 5, 700, 16)]), [("appel",)], 32000, 768, motif(7, 768)),
    ("verdict 6 exotique — HRESULT non documenté, table TOTALE",
     Script([(EXOTIQUE, 5, 100, 16)]), [("appel",)], 0, 121, motif(7, 121)),
    ("verdict 3 (HRESULT de certificat — table TOTALE, Q4)",
     Script([(CERT_INVALIDE, 5, 100, 16)]), [("appel",)], 0, 121, motif(7, 121)),
    ("normalisation depuis un état offset non nul — recv par-dessus puis Q1",
     Script([(OK, 5, 80, 16)]),
     [("recv", 50), ("appel",)], 100, 60, motif(7, 60)),
    ("lot vide (r8 = 0) — incomplet immédiat, champs (0, 0)",
     Script([(INCOMPLET, 5, 100, 16)]), [("appel",)], 0, 0, b""),
    ("enregistrement puis close_notify — Q1 puis Q3 (la fin du relais réel)",
     Script([(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)]),
     [("appel",), ("appel",)], 0, 142, motif(7, 142)),
    ("incomplet PUIS complet PUIS résidu — trois appels, la géométrie D89 "
     "de bout en bout",
     Script([(INCOMPLET, 5, 60, 8), (OK, 5, 60, 8), (OK, 2, 20, 4)]),
     [("appel",), ("recv", 31), ("appel",), ("appel",)], 0, 72, motif(7, 72)),
]

MUTATIONS_V4 = [
    ("M1 garde région relâchée (0x8000 → 0x8001) — la frontière 32769 glisse",
     ("cmp rcx, 0x8000", "cmp rcx, 0x8001")),
    ("M2 verdict Q2 dévié (2 → 3)",
     ("mov dword ptr [r10 + 0x30], 2",
      "mov dword ptr [r10 + 0x30], 3")),
    ("M3 offset lu dévié (+0x3C → +0x3E)",
     ("movzx eax, word ptr [r10 + 0x3C]",
      "movzx eax, word ptr [r10 + 0x3E]")),
    ("M4 longueur utile écrite déviée (+0x3A → +0x3E)",
     ("mov word ptr [r10 + 0x3A], cx",
      "mov word ptr [r10 + 0x3E], cx")),
    ("M5 span ptr dévié (tampon 0 → tampon 1)",
     ("mov rcx, [rsp + 0xA8]", "mov rcx, [rsp + 0xB8]")),
    ("M6 routage incomplet dévié (cmp 2 → 3)",
     ("cmp eax, 2", "cmp eax, 3")),
    ("M7 résidu lu dévié (tampon 1 → tampon 2)",
     ("mov ecx, [rsp + 0xB0]", "mov ecx, [rsp + 0xC0]")),
    ("M8 pfQOP non réécrit (0 → 1)",
     ("mov dword ptr [rsp + 0x58], 0", "mov dword ptr [rsp + 0x58], 1")),
    ("M9 descripteur tls-03 dévié (r9 +0x98)",
     ("lea r9, [rsp + 0x90]", "lea r9, [rsp + 0x98]")),
    ("M10 pMessage DM dévié (rdx +0x98)",
     ("lea rdx, [rsp + 0x90]", "lea rdx, [rsp + 0x98]")),
]


def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261028)
    parseur.add_argument("--cas", type=int, default=4000)
    parseur.add_argument("--chaines", type=int, default=1000)
    args = parseur.parse_args()
    rng = random.Random(args.graine)

    print("=== harnais_reception.py — tls-07:R1 (réception déchiffrée, D89 session) ===")
    print(f"graine {args.graine} · fuzz {args.cas} cas · {args.chaines} chaînes")

    ks = Ks(KS_ARCH_X86, KS_MODE_64)

    # --- V1 : round-trip ------------------------------------------------------
    print("\n[V1] round-trip de notation")
    blob07, declare = octets_notation(ks, "tls-07-reception", RVA_TLS07)
    controle("tls-07-reception rassemblée == taille déclarée (Code : N o)",
             declare is not None and len(blob07) == declare, f"{len(blob07)} o")
    controle("padding du slot >= 16 (D8) — slot 0x300 préfiguré conservé",
             SLOT_TLS07 - len(blob07) >= 16, f"{SLOT_TLS07 - len(blob07)} o")
    blobs = {"tls-07": blob07}
    # tls-02/tls-03 : notations M4 (locales) ; libc-01 : m1 (octets hérités
    # scellés R7 — le chemin est celui du dépôt m1)
    CHEMIN_M1 = os.path.join(ICI, os.pardir, "m1", "notation")
    for bloc, rva, chemin in (("tls-02-verdicts", RVA_TLS02, None),
                              ("tls-03-jetons", RVA_TLS03, None),
                              ("libc-01-memcpy", RVA_MEMCPY, CHEMIN_M1)):
        nom_court = bloc.split("-")[0] + "-" + bloc.split("-")[1]
        chemin_bloc = os.path.join(chemin, bloc + ".asm") if chemin else None
        b, d = octets_notation(ks, bloc, rva, chemin=chemin_bloc)
        blobs[nom_court] = b
        controle(f"{bloc} (intégration) == taille déclarée",
                 d is not None and len(b) == d, f"{len(b)} o")
    emu = Emulateur(blobs)

    # --- V2 : oracle à shims, scénarios de la spécification -------------------
    print("\n[V2] oracle à shims — scénarios de la spec, en CHAÎNES "
          "(cadre 0xD000 + zone + span octet par octet + contrat d'appels)")
    for nom, script, etapes, offset0, lng0, brut in SCENARIOS_V2:
        problemes = jouer_chaine(emu, script, nom, etapes, offset0, lng0, brut)
        controle(f"scénario « {nom} »", not problemes,
                 "; ".join(problemes[:3]) if problemes else
                 f"{len(etapes)} étape(s), conforme")

    # --- V3 : fuzzing à propriétés -------------------------------------------
    print(f"\n[V3a] fuzzing à propriétés — {args.cas} appels hostiles")
    codes_documentes = list(L.HRESULTS.keys())
    ecarts = 0
    for i in range(args.cas):
        if rng.random() < 0.06:
            lot = rng.choice([32768, 32769, 33000, 60000])
        else:
            lot = rng.randint(0, 900)
        if rng.random() < 0.10:
            offset0 = rng.choice([0x7000, 0x7FFF, rng.randint(400, 800)])
        elif rng.random() < 0.5:
            offset0 = 0
        else:
            offset0 = rng.randint(0, 400)
        if offset0 + lot > L.CAPACITE_RECEPTION:
            brut = motif(9, max(0, L.CAPACITE_RECEPTION - offset0))
        else:
            brut = bytes(rng.getrandbits(8) for _ in range(lot))
        utile0 = rng.randint(0, lot) if lot else 0
        h = (0 if rng.random() < 0.55 else
             (INCOMPLET if rng.random() < 0.5 else
              (rng.choice(codes_documentes) if rng.random() < 0.6
               else rng.getrandbits(32))))
        dm = [(h, rng.randint(0, 64), rng.randint(0, 600), rng.randint(0, 80))]
        script = Script(dm)
        problemes = jouer_cas(emu, script, "fuzz", lot, utile0, offset0, brut)
        if problemes:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart #{ecarts} cas {i} : {'; '.join(problemes[:3])}")
    controle(f"fuzz {args.cas} appels : ZÉRO écart", ecarts == 0, f"{ecarts} écart(s)")

    print(f"\n[V3b] fuzzing à propriétés — {args.chaines} chaînes × 3-4 appels "
          "(l'appelant réceptionne par-dessus la région lue AU CADRE)")
    ecarts = 0
    for i in range(args.chaines):
        n_appels = rng.randint(3, 4)
        dm = []
        for _ in range(n_appels + 1):
            h = (0 if rng.random() < 0.7 else
                 (INCOMPLET if rng.random() < 0.4 else
                  (rng.choice(codes_documentes) if rng.random() < 0.5
                   else rng.getrandbits(32))))
            dm.append((h, rng.randint(0, 64), rng.randint(0, 500),
                       rng.randint(0, 80)))
        script = Script(dm)
        lot0 = rng.randint(0, 500)
        etapes = []
        for _ in range(n_appels):
            etapes.append(("recv", rng.randint(0, 300)))
            etapes.append(("appel",))
        problemes = jouer_chaine(emu, script, f"chaîne {i}", etapes, 0, lot0,
                                 bytes(rng.getrandbits(8) for _ in range(lot0)))
        if problemes:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart #{ecarts} chaîne {i} : "
                      f"{'; '.join(problemes[:3])}")
    controle(f"fuzz {args.chaines} chaînes : ZÉRO écart", ecarts == 0,
             f"{ecarts} écart(s)")

    # --- V4 : falsification ---------------------------------------------------
    print("\n[V4] falsification — dix mutations d'un point, chacune attrapée")
    for nom, mutation in MUTATIONS_V4:
        blob_m, _ = octets_notation(ks, "tls-07-reception", RVA_TLS07, mutation)
        blobs_m = dict(blobs)
        blobs_m["tls-07"] = blob_m
        emu_m = Emulateur(blobs_m)
        attrapes = 0
        for nom_s, script, etapes, offset0, lng0, brut in SCENARIOS_V2:
            try:
                if jouer_chaine(emu_m, script, "mutant", etapes, offset0, lng0, brut):
                    attrapes += 1
            except Exception:
                attrapes += 1          # faute d'exécution = écart nommé
        controle(f"mutation « {nom} » ATTRAPÉE", attrapes > 0,
                 f"{attrapes}/{len(SCENARIOS_V2)} scénarios en écart")
    # témoin intact : le différentiel reste vert (une suite qui ne peut pas
    # échouer ne prouve rien — le témoin prouve que les pièges sont armés)
    emu_t = Emulateur(blobs)
    verts = sum(1 for nom_s, script, etapes, offset0, lng0, brut in SCENARIOS_V2
                if not jouer_chaine(emu_t, script, "témoin", etapes, offset0,
                                    lng0, brut))
    controle("témoin intact : VERT sur les mêmes scénarios", verts == len(SCENARIOS_V2),
             f"{verts}/{len(SCENARIOS_V2)}")

    print("\n" + "=" * 70)
    print(f"BILAN : {len(REUSSITES)} PASS, {len(ECHECS)} ÉCHEC")
    for nom in ECHECS:
        print(f"  FAIL {nom}")
    print("=" * 70)
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main())
