#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_poignee.py — Harnais à propriétés de tls-04 (poignée de main, D83).

LE bloc du critère M4 : la boucle InitializeSecurityContext bornée 16 allers.
La notation est émulée à ses RVA .text3 exacts AVEC les vrais octets de ses
dépendances (tls-02 verdicts, tls-03 descripteurs, tcp-03/tcp-04 réception/
émission) ; l'IAT secur32 et ws2_32 reçoivent des fausses adresses (résolution
chargeur, mécanisme M2/M3 : page trampoline de ret + crochet code). Vecteurs
de la spécification tls-04:R1 :

  V1  round-trip de notation 100 % (taille totale == « Code : N o », padding
      >= 16 — D8) pour tls-04 ET les quatre blocs intégrés ;
  V2  oracle à shims — scénarios de la spec : poignées complètes en 2, 3 et
      9 allers (avec message incomplet), certificat invalide (verdict 3 — LE
      critère M4), jeton trucidé (5), HRESULT exotique (6), boucle sans fin
      (E5), jeton hors borne (E2), émission rompue (E3), réception rompue et
      fermeture propre (E4), émission partielle exigeant l'achèvement, fin
      de contexte en poignée (4), succès sans jeton final — CHAQUE scénario
      finit par un état du cadre EXACTEMENT PRÉDIT (image 0x9000 octet par
      octet : verdict, HRESULT d'origine, allers, handle de contexte écrit
      PAR la bibliothèque, zones émission/réception) et un contrat d'appels
      complet (les 11 arguments d'ISC : phCredential cadre+0, phContext NULL
      au premier appel PUIS cadre+0x10, pszTargetName lu tel quel, fContextReq
      == layout.ISC_REQUETES, Reserved/TargetDataRep nuls, phNewContext
      cadre+0x10, descripteurs ENTRÉE/SORTIE tls-03 type 0 exacts — ptr/long/
      type/contenu) ; les traces tcp-04/tcp-03 (socket, pointeur, longueur)
      sont prédites appel par appel (accumulation, achèvement) ;
  V3  fuzzing à propriétés : HRESULT documentés ET exotiques, jetons de
      longueurs hostiles (jusqu'à MAX_JETON), réceptions partielles, émissions
      partielles et rompues — survie, terminaison (I1 : la borne 16 garantit),
      verdict conforme au modèle, ZÉRO écart ;
  V4  falsification : SIX mutations D'UN SEUL point de la notation, STABLES
      EN TAILLE (leçon D82), chacune ATTRAPÉE par le différentiel ; le témoin
      intact reste vert.

Le modèle de référence est écrit depuis la SPÉCIFICATION (jamais la
notation) : verdict_modele via layout.HRESULTS, cadre aux offsets
layout.CADRE_*, fContextReq via layout.ISC_REQUETES. Les adresses de PILE
des descripteurs et de pfContextAttr sont vérifiées par PRÉDICAT (zone pile,
alignement) — l'adresse exacte appartient à la notation, le CONTENU des
descripteurs appartient au contrat.
Usage : python3 harnais_poignee.py [--graine G] [--cas N]
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

ZONE_CODE = 0x6000            # page .text3 : tls-02/03/04 (le bloc sous test)
TAILLE_CODE = 0x1000
RET_MAGIQUE = 0x6F00          # adresse d'arrêt propre (int3 de la page code)
ZONE_TCP = 0x4000             # page .text2 : tcp-03 @0x4140, tcp-04 @0x4180
TAILLE_TCP = 0x1000
ZONE_RDATA = 0x2000           # page .rdata : IAT kernel32/ws2_32/secur32 + fixture
TAILLE_RDATA = 0x1000
TRAMPOLINE = 0x140100000      # fausses adresses d'API (page RX, mécanisme M2/M3)
TAILLE_TRAMP = 0x1000
ZONE_CADRE = 0x150000000      # cadre de session TLS complet (0x8260) + marge
TAILLE_CADRE_PAGE = 0x9000
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP = 0x7F008000

RVA_TLS04, SLOT_TLS04 = 0x62C0, 0x300
RVA_TLS02, SLOT_TLS02 = 0x6080, 0x100
RVA_TLS03, SLOT_TLS03 = 0x6180, 0x140
RVA_TCP03, RVA_TCP04 = 0x4140, 0x4180

# fausses adresses : secur32 (7) + ws2_32 recv/send explicites + le reste des
# imports M3 (toute frappe = faux pas nommé — I3 : seule ISC est légitime)
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
MAGIC_PARTIAL = (0x1111111111111111, 0x2222222222222222)  # contexte en cours d'établissement
MAGIC_FINAL = (0xABABABABABABABAB, 0xCDCDCDCDCDCDCDCD)    # contexte établi
MAGIC_ORDURE = (0xDEAD, 0xBEEF)                            # la bibliothèque barbouille en échec
SOCKET_SENT = 0x7777777777777777
NOM_UTF16 = "hote.exemple".encode("utf-16-le") + b"\x00\x00"

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


# --- Script de comportements (index-based : modèle et shims voient le même) ------

class Script:
    """Comportements shims déterministes par INDICE d'appel (jamais de file
    épuisable) : isc[i] = (HRESULT, longueur du jeton produit) ; recv[i] =
    n (>0 données, 0 fermeture propre, <0 erreur) ou 'max' (remplit la
    capacité demandée) ; send[i] = 'plein' | k (partiel) | <=0 (échec)."""

    def __init__(self, isc: list, recv: list, send: list):
        self.entries_isc = isc
        self.entries_recv = recv
        self.entries_send = send

    def comportement_isc(self, i: int) -> tuple[int, int]:
        if i < len(self.entries_isc):
            return self.entries_isc[i]
        return (0x00090312, 8)          # défaut : CONTINUE_NEEDED, jeton de 8 o

    def donnees_recv(self, i: int, capacite: int) -> tuple[int, bytes]:
        if i < len(self.entries_recv):
            e = self.entries_recv[i]
        else:
            e = 16                        # défaut : 16 octets de données
        if e == "max":
            n = capacite
        elif e <= 0:
            n = e
        else:
            n = min(e, capacite)          # une vraie socket ne rend jamais plus que demandé
        return n, motif(i, n) if n > 0 else b""

    def comportement_send(self, i: int, demande: int) -> int:
        if i < len(self.entries_send):
            e = self.entries_send[i]
        else:
            e = "plein"
        if e == "plein":
            return demande
        if e <= 0:
            return e
        return min(e, demande)


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


def image_initiale() -> bytearray:
    """Cadre VIERGE fourni par http-10:R2 — P1 de tls-04 : credentials acquis
    par tls-05, contexte à zéro, socket connectée, nom traduit par tls-01."""
    page = bytearray(CANARI * TAILLE_CADRE_PAGE)
    def q(off, lo, hi):
        page[off:off + 16] = struct.pack("<QQ", lo, hi)   # SecHandle = 2 x u64
    q(L.CADRE_CRED, *MAGIC_CRED)
    q(L.CADRE_CTXT, 0, 0)                       # contexte à ZÉRO (P1)
    q(L.CADRE_SOCKET, SOCKET_SENT, 0)
    q(L.CADRE_PTR_NOM, ZONE_CADRE + L.CADRE_NOM_ZONE, 0)
    page[L.CADRE_NOM_ZONE:L.CADRE_NOM_ZONE + len(NOM_UTF16)] = NOM_UTF16
    return page


class _Echec(Exception):
    def __init__(self, verdict: int):
        self.verdict = verdict


class Modele:
    """La boucle de la spécification, en Python — même environnement shims."""

    def __init__(self, script: Script):
        self.script = script
        self.page = image_initiale()
        self.appels: list[tuple] = []
        self.allers = 0
        self.entree = 0
        self.i_isc = self.i_recv = self.i_send = 0

    def _dw32(self, off: int, v: int) -> None:
        self.page[off:off + 4] = struct.pack("<I", v & 0xFFFFFFFF)

    def _dw16(self, off: int, v: int) -> None:
        self.page[off:off + 2] = struct.pack("<H", v & 0xFFFF)

    def _q(self, off: int, lo: int, hi: int) -> None:
        self.page[off:off + 16] = struct.pack("<QQ", lo, hi)   # SecHandle = 2 x u64

    def _emettre(self, cb: int) -> None:
        """Q3 : émission INTÉGRALE en boucle d'achèvement bornée (E3)."""
        envoye = 0
        while envoye < cb:
            r = self.script.comportement_send(self.i_send, cb - envoye)
            self.appels.append(("SEND", SOCKET_SENT,
                                ZONE_CADRE + L.CADRE_EMISSION + envoye, cb - envoye))
            self.i_send += 1
            if r <= 0:
                raise _Echec(5)
            envoye += r

    def _recevoir(self) -> None:
        """Q3 : UN tcp-03 par tour, accumulation au sommet (E4)."""
        n, donnees = self.script.donnees_recv(self.i_recv, L.MAX_JETON - self.entree)
        self.appels.append(("RECV", SOCKET_SENT,
                            ZONE_CADRE + L.CADRE_RECEPTION + self.entree,
                            L.MAX_JETON - self.entree))
        self.i_recv += 1
        if n <= 0:
            raise _Echec(5)
        base = L.CADRE_RECEPTION + self.entree
        self.page[base:base + n] = donnees
        self.entree += n

    def executer(self) -> tuple[int, int, list, bytes]:
        verdict_final = None
        try:
            while True:
                if self.allers >= 16:                 # I1/E5 : bornée, TOUJOURS finie
                    raise _Echec(5)
                self.allers += 1
                h, lt = self.script.comportement_isc(self.i_isc)
                verdict = verdict_modele(h)
                # contrat d'appel attendu (trace ISC — cf. comparer_traces)
                self.appels.append((
                    "ISC", ZONE_CADRE,
                    0 if self.entree == 0 else ZONE_CADRE + L.CADRE_CTXT,
                    ZONE_CADRE + L.CADRE_NOM_ZONE, L.ISC_REQUETES, 0, 0,
                    0 if self.entree == 0 else "PILE",
                    0, ZONE_CADRE + L.CADRE_CTXT, "PILE", "PILE",
                    None if self.entree == 0 else
                    (0, 1, "+0x10", self.entree, 2, ZONE_CADRE + L.CADRE_RECEPTION),
                    (0, 1, "+0x10", L.MAX_JETON, 2, ZONE_CADRE + L.CADRE_EMISSION)))
                self.i_isc += 1
                # Q2 : la notation consigne l'HRESULT d'origine à CHAQUE retour
                self._dw32(L.CADRE_HRESULT, h)
                # écritures de la BIBLIOTHÈQUE (règle shim, partagée) :
                if verdict == 0:
                    self._q(L.CADRE_CTXT, *MAGIC_FINAL)
                elif verdict == 1:
                    self._q(L.CADRE_CTXT, *MAGIC_PARTIAL)
                elif verdict >= 3:
                    self._q(L.CADRE_CTXT, *MAGIC_ORDURE)   # verdict 2 : inchangé
                cb = L.MAX_JETON
                if verdict in (0, 1):
                    # la bibliothèque consigne la longueur produite (0 = aucun
                    # jeton) — l'appelant n'émet QUE ce qui fut produit (Q3)
                    cb = lt
                    if lt > 0:
                        jeton = motif(self.i_isc - 1, lt)
                        self.page[L.CADRE_EMISSION:L.CADRE_EMISSION + lt] = jeton
                if verdict == 0:                        # Q1 : contexte ÉTABLI
                    if cb > 0:
                        self._emettre(cb)               # jeton final émis (Q3)
                    self._dw32(L.CADRE_VERDICT, 0)
                    verdict_final = 0
                    break
                if verdict == 1:                         # l'aller continue
                    self.entree = 0                      # entrée consommée
                    if cb > 0:
                        self._emettre(cb)
                    self._recevoir()
                elif verdict == 2:                       # incomplet : recevoir plus
                    if self.entree >= L.MAX_JETON:       # E2 : jeton hors borne
                        raise _Echec(5)
                    self._recevoir()
                else:                                    # Q2/E1 : échec nommé
                    verdict_final = verdict
                    self._dw32(L.CADRE_VERDICT, verdict)
                    break
        except _Echec as e:
            verdict_final = e.verdict
            self._dw32(L.CADRE_VERDICT, e.verdict)
        self._dw16(L.CADRE_ALLERS, self.allers)
        return verdict_final, self.allers, self.appels, bytes(self.page)


# --- Émulateur à shims SSPI/ws2_32 (page ret + crochet code, mécanisme M2/M3) ----

def _pile_valide(p: int) -> bool:
    return ZONE_PILE <= p < ZONE_PILE + TAILLE_PILE


class Emulateur:
    """Un chargement = un émulateur NEUF (leçon D79). Les shims sont pilotés
    par le Script du cas ; les écritures de la « bibliothèque » suivent la
    même règle que le modèle (jetons, handles, barbouille en échec)."""

    def __init__(self, blobs: dict[str, bytes]):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        uc.mem_map(ZONE_CODE, TAILLE_CODE)
        uc.mem_map(ZONE_TCP, TAILLE_TCP)
        uc.mem_map(ZONE_RDATA, TAILLE_RDATA)
        uc.mem_map(TRAMPOLINE, TAILLE_TRAMP)
        uc.mem_map(ZONE_CADRE, TAILLE_CADRE_PAGE)
        uc.mem_map(ZONE_PILE, TAILLE_PILE)
        page = b"\xCC" * TAILLE_CODE
        for rva, blob in ((RVA_TLS02, blobs["tls-02"]), (RVA_TLS03, blobs["tls-03"]),
                          (RVA_TLS04, blobs["tls-04"])):
            page = page[:rva - ZONE_CODE] + blob + page[rva - ZONE_CODE + len(blob):]
        uc.mem_write(ZONE_CODE, page)
        page_tcp = b"\xCC" * TAILLE_TCP
        for rva, blob in ((RVA_TCP03, blobs["tcp-03"]), (RVA_TCP04, blobs["tcp-04"])):
            page_tcp = page_tcp[:rva - ZONE_TCP] + blob + page_tcp[rva - ZONE_TCP + len(blob):]
        uc.mem_write(ZONE_TCP, page_tcp)
        uc.mem_write(TRAMPOLINE, b"\xc3" * TAILLE_TRAMP)   # chaque shim retourne
        # résolution chargeur : IAT kernel32/ws2_32 + secur32 vers les fausses adresses
        for nom, rva in L.IAT_SLOTS.items():
            uc.mem_write(rva, struct.pack("<Q", FAUX[nom]))
        for nom, rva in L.IAT_SEC32_SLOTS.items():
            uc.mem_write(rva, struct.pack("<Q", FAUX[nom]))
        # fixture .rdata M4 (tls-05, unique propriétaire — doit rester intacte)
        uc.mem_write(L.R_PKG_M4, L.PKG_M4)
        uc.hook_add(UC_HOOK_CODE, self._shim, begin=TRAMPOLINE, end=TRAMPOLINE + TAILLE_TRAMP)
        self.script: Script | None = None
        self.appels: list[tuple] = []
        self.faux_pas: list[str] = []
        self._i_isc = self._i_recv = self._i_send = 0

    def _shim(self, uc: Uc, adresse: int, taille: int, donnees):
        nom = FAUX_REV.get(adresse)
        if nom is None:
            self.faux_pas.append(f"shim inconnu @{adresse:#x}")
            return
        methode = getattr(self, "_api_" + nom, None)
        if methode is None:
            self.faux_pas.append(f"{nom} appelé par tls-04 (I3 violée)")
            return
        methode()

    def _pile(self, offset: int) -> int:
        """Argument pile de l'appelant, vu du shim ([rsp+0x28] = arg5 msx64)."""
        rsp = self.uc.reg_read(REGS["rsp"])
        return struct.unpack("<Q", bytes(self.uc.mem_read(rsp + offset, 8)))[0]

    def _lire_desc(self, p: int):
        """SecBufferDesc + premier SecBuffer (tls-03 type 0 : 32 octets)."""
        if not p:
            return None
        b = bytes(self.uc.mem_read(p, 32))
        ulv, nb = struct.unpack_from("<II", b, 0)
        (pb,) = struct.unpack_from("<Q", b, 8)
        cb, typ = struct.unpack_from("<II", b, 16)
        (pv,) = struct.unpack_from("<Q", b, 24)
        return (ulv, nb, pb, cb, typ, pv)

    # --- les DEUX seules APIs réseau légitimes + l'unique API SSPI (I3) ---------

    def _api_recv(self):
        uc = self.uc
        sock = uc.reg_read(REGS["rcx"])
        buf = uc.reg_read(REGS["rdx"])
        ln = uc.reg_read(REGS["r8"])
        self.appels.append(("RECV", sock, buf, ln))
        n, donnees = self.script.donnees_recv(self._i_recv, ln)
        self._i_recv += 1
        if n > 0 and ln > 0:
            uc.mem_write(buf, donnees[:n])
        uc.reg_write(REGS["rax"], n & 0xFFFFFFFFFFFFFFFF)

    def _api_send(self):
        uc = self.uc
        sock = uc.reg_read(REGS["rcx"])
        buf = uc.reg_read(REGS["rdx"])
        ln = uc.reg_read(REGS["r8"])
        self.appels.append(("SEND", sock, buf, ln))
        r = self.script.comportement_send(self._i_send, ln)
        self._i_send += 1
        uc.reg_write(REGS["rax"], r & 0xFFFFFFFFFFFFFFFF)

    def _api_InitializeSecurityContextW(self):
        uc = self.uc
        ph_cred = uc.reg_read(REGS["rcx"])
        ph_ctxt = uc.reg_read(REGS["rdx"])
        cible = uc.reg_read(REGS["r8"])
        requetes = uc.reg_read(REGS["r9"]) & 0xFFFFFFFF
        reserved1 = self._pile(0x28)
        datarep = self._pile(0x30)
        p_input = self._pile(0x38)
        reserved2 = self._pile(0x40)
        ph_new = self._pile(0x48)
        p_output = self._pile(0x50)
        pf_attr = self._pile(0x58)
        desc_in = self._lire_desc(p_input)
        desc_out = self._lire_desc(p_output)
        self.appels.append(("ISC", ph_cred, ph_ctxt, cible, requetes, reserved1,
                            datarep, p_input, reserved2, ph_new, p_output, pf_attr,
                            desc_in, desc_out))
        # comportement scripté (règle partagée avec le modèle)
        h, lt = self.script.comportement_isc(self._i_isc)
        self._i_isc += 1
        verdict = verdict_modele(h)
        if verdict in (0, 1) and desc_out is not None:
            # une vraie ISC consigne TOUJOURS cbBuffer à la longueur produite
            # (0 = aucun jeton) sur succès/continuation — jamais la capacité
            if lt > 0:
                uc.mem_write(desc_out[5], motif(self._i_isc - 1, lt))   # le jeton
            uc.mem_write(p_output + 0x10, struct.pack("<I", lt))        # cbBuffer
        if verdict == 0:
            uc.mem_write(ph_new, struct.pack("<QQ", *MAGIC_FINAL))
        elif verdict == 1:
            uc.mem_write(ph_new, struct.pack("<QQ", *MAGIC_PARTIAL))
        elif verdict >= 3:
            uc.mem_write(ph_new, struct.pack("<QQ", *MAGIC_ORDURE))
        if pf_attr:
            uc.mem_write(pf_attr, struct.pack("<I", 0x141))             # attributs factices
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

    def executer(self, script: Script) -> int:
        uc = self.uc
        self.script = script
        self.appels = []
        self.faux_pas = []
        self._i_isc = self._i_recv = self._i_send = 0
        uc.mem_write(ZONE_CADRE, bytes(image_initiale()))
        for nom, valeur in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], valeur)
        uc.reg_write(REGS["rsp"], RSP)
        uc.mem_write(RSP, struct.pack("<Q", RET_MAGIQUE))
        uc.reg_write(REGS["rcx"], ZONE_CADRE)
        uc.reg_write(REGS["rdx"], 0xAAAAAAAA)
        uc.reg_write(REGS["r8"], 0xBBBBBBBB)
        uc.reg_write(REGS["r9"], 0xCCCCCCCC)
        uc.emu_start(RVA_TLS04, RET_MAGIQUE, timeout=5_000_000, count=2_000_000)
        return self.uc.reg_read(REGS["rax"]) & 0xFFFFFFFF

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
        if a[0] in ("RECV", "SEND"):
            if a[1] != e[1]:
                problemes.append(f"{a[0]} #{k} socket {a[1]:#x} != {e[1]:#x}")
            if a[2] != e[2]:
                problemes.append(f"{a[0]} #{k} pointeur {a[2]:#x} != {e[2]:#x}")
            if a[3] != e[3]:
                problemes.append(f"{a[0]} #{k} longueur {a[3]} != {e[3]}")
            continue
        # ISC : (nom, ph_cred, ph_ctxt, cible, requetes, r1, datarep, p_in,
        #        r2, ph_new, p_out, pf_attr, desc_in, desc_out)
        exacts = [(1, "phCredential"), (2, "phContext"), (3, "pszTargetName"),
                  (4, "fContextReq"), (5, "Reserved1"), (6, "TargetDataRep"),
                  (8, "Reserved2"), (9, "phNewContext")]
        for idx, nomch in exacts:
            if a[idx] != e[idx]:
                problemes.append(f"ISC #{k} {nomch} {a[idx]!r} != {e[idx]!r}")
        # p_in (7), p_out (10), pf_attr (11) : prédicats pile
        for idx, nomch in ((7, "pInput"), (10, "pOutput"), (11, "pfContextAttr")):
            if e[idx] == 0:
                if a[idx] != 0:
                    problemes.append(f"ISC #{k} {nomch} {a[idx]:#x} != NULL (Q4)")
            elif not _pile_valide(a[idx]) or a[idx] % 8:
                problemes.append(f"ISC #{k} {nomch} {a[idx]:#x} hors pile/aligné")
        # descripteurs (12 = entrée, 13 = sortie) : contenu exact
        for idx, nomch, p_idx in ((12, "descripteur entrée", 7), (13, "descripteur sortie", 10)):
            if e[idx] is None:
                if a[idx] is not None:
                    problemes.append(f"ISC #{k} {nomch} présent à tort")
                continue
            if a[idx] is None:
                problemes.append(f"ISC #{k} {nomch} ABSENT")
                continue
            ulv, nb, pb, cb, typ, pv = a[idx]
            eulv, enb, ecb, etyp, epv = e[idx][0], e[idx][1], e[idx][3], e[idx][4], e[idx][5]
            if (ulv, nb, cb, typ) != (eulv, enb, ecb, etyp):
                problemes.append(f"ISC #{k} {nomch} (v={ulv}, n={nb}, cb={cb}, "
                                 f"t={typ}) != (v={eulv}, n={enb}, cb={ecb}, t={etyp})")
            if pb != a[p_idx] + 0x10:
                problemes.append(f"ISC #{k} {nomch} pBuffers {pb:#x} != cadre+0x10 "
                                 f"du descripteur")
            if pv != epv:
                problemes.append(f"ISC #{k} {nomch} pv {pv:#x} != {epv:#x}")
    return problemes


# --- V2/V3 : différentiel ---------------------------------------------------------

def jouer_cas(emu: Emulateur, script: Script, etiquette: str) -> list[str]:
    """Exécute UN cas contre le modèle — écarts nommés."""
    v_att, allers_att, appels_att, image_att = Modele(script).executer()
    rax = emu.executer(script)
    problemes: list[str] = []
    if rax != v_att:
        problemes.append(f"rax {rax} != {v_att} (modèle spec)")
    image_lue = bytes(emu.uc.mem_read(ZONE_CADRE, TAILLE_CADRE_PAGE))
    if image_lue != image_att:
        off = next(o for o in range(TAILLE_CADRE_PAGE) if image_lue[o] != image_att[o])
        problemes.append(f"cadre diverge @+0x{off:x} (attendu "
                         f"{image_att[off]:#04x}, lu {image_lue[off]:#04x})")
    problemes += comparer_traces(emu.appels, appels_att)
    problemes += emu.hygiene()
    return problemes


OK, CONT, INC = 0x00000000, 0x00090312, 0x80090318

SCENARIOS_V2 = [
    ("poignée complète en 2 allers",
     Script([(CONT, 64), (OK, 32)], [128], ["plein"])),
    ("poignée en 3 allers avec message incomplet",
     Script([(CONT, 96), (INC, 0), (OK, 16)], [50, 60], ["plein"])),
    ("poignée en 9 allers",
     Script([(CONT, 120), (CONT, 80), (CONT, 60), (CONT, 200), (CONT, 40),
             (CONT, 90), (INC, 0), (CONT, 70), (OK, 24)],
            [300, 30, 150, 20, 400, 60, 90, 85], ["plein"])),
    ("certificat invalide — verdict 3 (LE critère M4)",
     Script([(CONT, 64), (0x80090325, 0)], [90], ["plein"])),
    ("jeton trucidé — verdict 5",
     Script([(CONT, 64), (0x80090308, 0)], [90], ["plein"])),
    ("HRESULT exotique au premier appel — verdict 6",
     Script([(0x81234567, 0)], [], [])),
    ("boucle sans fin — E5 à 16 allers (I1)",
     Script([], [], [])),
    ("jeton hors borne — E2 (garde avant réception)",
     Script([(CONT, 16), (INC, 0)], ["max"], ["plein"])),
    ("émission rompue — E3",
     Script([(CONT, 64)], [16], [-1])),
    ("réception rompue — E4 (erreur système)",
     Script([(CONT, 64)], [-1], ["plein"])),
    ("fermeture propre du serveur — E4 (n = 0)",
     Script([(CONT, 64)], [0], ["plein"])),
    ("émission partielle exigeant l'achèvement",
     Script([(CONT, 100), (OK, 8)], [40], [40, 60, 3, 5])),
    ("fin de contexte en poignée — verdict 4 (Q2)",
     Script([(CONT, 64), (0x00090317, 0)], [90], ["plein"])),
    ("continuer sans jeton produit (l = 0)",
     Script([(CONT, 0), (OK, 8)], [60], ["plein"])),
    ("succès immédiat sans jeton final (l = 0)",
     Script([(OK, 0)], [], [])),
    ("succès au premier appel avec jeton final",
     Script([(OK, 20)], [], [])),
]

MUTATIONS_V4 = [
    ("M1 borne E5 relâchée (16 → 17)", ("cmp ecx, 16", "cmp ecx, 17")),
    ("M2 garde E2 relâchée (16384 → 16385)",
     ("cmp qword ptr [rsp + 0x68], 16384", "cmp qword ptr [rsp + 0x68], 16385")),
    ("M3 phNewContext dévié (cadre+0x18)",
     ("lea rax, [rax + 0x10]", "lea rax, [rax + 0x18]")),
    ("M4 drapeau ISC corrompu (0xC01D)",
     ("mov r9d, 0xC01C", "mov r9d, 0xC01D")),
    ("M5 routage continuer dévié (cmp 1 → 3)", ("cmp eax, 1", "cmp eax, 3")),
    ("M6 émission depuis la zone réception",
     ("lea rdx, [rdx + 0x260]", "lea rdx, [rdx + 0x4260]")),
]


def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261028)
    parseur.add_argument("--cas", type=int, default=5000)
    args = parseur.parse_args()
    rng = random.Random(args.graine)

    print("=== harnais_poignee.py — tls-04:R1 (poignée de main cliente, D83) ===")
    print(f"graine {args.graine} · fuzz {args.cas} cas")

    ks = Ks(KS_ARCH_X86, KS_MODE_64)

    # --- V1 : round-trip ------------------------------------------------------
    print("\n[V1] round-trip de notation")
    blob04, declare = octets_notation(ks, "tls-04-poignee", RVA_TLS04)
    controle("tls-04-poignee rassemblée == taille déclarée (Code : N o)",
             declare is not None and len(blob04) == declare, f"{len(blob04)} o")
    controle("padding du slot >= 16 (D8) — slot 0x300 conservé",
             SLOT_TLS04 - len(blob04) >= 16, f"{SLOT_TLS04 - len(blob04)} o")
    blobs = {"tls-04": blob04}
    # tls-02/tls-03 : notations M4 (locales) ; tcp-03/tcp-04 : notations M2
    # scellées (octets hérités R7 — le chemin est celui du dépôt m2/)
    CHEMIN_M2 = os.path.join(ICI, os.pardir, "m2", "notation")
    for bloc, rva, chemin in (("tls-02-verdicts", RVA_TLS02, None),
                              ("tls-03-jetons", RVA_TLS03, None),
                              ("tcp-03-recv", RVA_TCP03, CHEMIN_M2),
                              ("tcp-04-send", RVA_TCP04, CHEMIN_M2)):
        nom_court = bloc.split("-")[0] + "-" + bloc.split("-")[1]
        chemin_bloc = os.path.join(chemin, bloc + ".asm") if chemin else None
        b, d = octets_notation(ks, bloc, rva, chemin=chemin_bloc)
        blobs[nom_court] = b
        controle(f"{bloc} (intégration) == taille déclarée",
                 d is not None and len(b) == d, f"{len(b)} o")
    emu = Emulateur(blobs)

    # --- V2 : oracle à shims, scénarios de la spécification -------------------
    print("\n[V2] oracle à shims — scénarios de la spec "
          "(cadre 0x9000 octet par octet + contrat d'appels)")
    for nom, script in SCENARIOS_V2:
        problemes = jouer_cas(emu, script, nom)
        v_att, allers_att = Modele(script).executer()[:2]
        controle(f"scénario « {nom} »", not problemes,
                "; ".join(problemes[:3]) if problemes else
                f"verdict {v_att}, {allers_att} aller(s), {len(emu.appels)} appel(s)")

    # --- V3 : fuzzing à propriétés -------------------------------------------
    print(f"\n[V3] fuzzing à propriétés — {args.cas} cas hostiles")
    codes_documentes = list(L.HRESULTS.keys())
    ecarts = 0
    for i in range(args.cas):
        n_isc = rng.randint(1, 17)
        isc = []
        for _ in range(n_isc):
            t = rng.random()
            if t < 0.45:
                h, lt = CONT, rng.randint(0, 300)
            elif t < 0.60:
                h, lt = OK, rng.randint(0, 300)
            elif t < 0.70:
                h, lt = INC, 0
            elif t < 0.85:
                h, lt = rng.choice(codes_documentes), rng.randint(0, 200)
            else:
                h, lt = rng.getrandbits(32), rng.randint(0, 100)
            if rng.random() < 0.08:
                lt = rng.randint(16000, L.MAX_JETON)     # jeton presque MAX_JETON
            isc.append((h, lt))
        recus = [rng.choice([rng.randint(1, 600), rng.randint(1, 50), "max",
                             0, -1]) for _ in range(20)]
        envois = [rng.choice(["plein", "plein", "plein", "plein",
                              rng.randint(1, 40), -1, 0]) for _ in range(24)]
        script = Script(isc, recus, envois)
        problemes = jouer_cas(emu, script, "fuzz")
        if problemes:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart #{ecarts} cas {i} : {'; '.join(problemes[:3])}")
    controle(f"fuzz {args.cas} cas : ZÉRO écart", ecarts == 0, f"{ecarts} écart(s)")

    # --- V4 : falsification ---------------------------------------------------
    print("\n[V4] falsification — six mutations d'un point, chacune attrapée")
    cas_mutants = [script for _, script in SCENARIOS_V2]
    for nom, mutation in MUTATIONS_V4:
        blob_m, _ = octets_notation(ks, "tls-04-poignee", RVA_TLS04, mutation)
        blobs_m = dict(blobs)
        blobs_m["tls-04"] = blob_m
        emu_m = Emulateur(blobs_m)
        attrapes = 0
        for script in cas_mutants:
            try:
                if jouer_cas(emu_m, script, "mutant"):
                    attrapes += 1
            except Exception:
                attrapes += 1          # faute d'exécution = écart nommé
        controle(f"mutation « {nom} » ATTRAPÉE", attrapes > 0,
                 f"{attrapes}/{len(cas_mutants)} cas en écart")
    # témoin intact : le différentiel reste vert (une suite qui ne peut pas
    # échouer ne prouve rien — le témoin prouve que les pièges sont armés)
    emu_t = Emulateur(blobs)
    verts = sum(1 for script in cas_mutants if not jouer_cas(emu_t, script, "témoin"))
    controle("témoin intact : VERT sur les mêmes cas", verts == len(cas_mutants),
             f"{verts}/{len(cas_mutants)}")

    print("\n" + "=" * 70)
    print(f"BILAN : {len(REUSSITES)} PASS, {len(ECHECS)} ÉCHEC")
    for nom in ECHECS:
        print(f"  FAIL {nom}")
    print("=" * 70)
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main())
