#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_emission.py — Harnais à propriétés de tls-06 (émission chiffrée, D84 session).

La notation est émulée à ses RVA .text3 exacts AVEC les vrais octets de ses
dépendances (tls-02 verdicts, tls-03 descripteurs, tcp-04 émission, libc-01
copie, libc-07 neutralisation — héritage scellé lu aux dépôts m1/m2, R7) ;
l'IAT secur32 et ws2_32 reçoivent des fausses adresses (résolution chargeur,
mécanisme M2/M3 : page trampoline de ret + crochet code). Vecteurs de la
spécification tls-06:R1 :

  V1  round-trip de notation 100 % (taille totale == « Code : N o », padding
      >= 16 — D8) pour tls-06 ET les cinq blocs intégrés ;
  V2  oracle à shims — scénarios de la spec : span de 1 octet, du message
      maximal exact, de 2 × maximal + 1 (chaîne de découpe) ; tailles
      négociées exotiques ; EncryptMessage en verdict 5 AU MILIEU d'une
      chaîne ; tcp-04 en émission partielle exigeant l'achèvement et en
      échec système ; échec d'acquisition des tailles (E3 — la barbouille
      de la bibliothèque est annulée par le zéro défensif) ; span de
      longueur nulle (P3 : UN enregistrement vide, aucun cas spécial) ;
      tailles déjà consignées (I3 : QCA JAMAIS rappelée) — CHAQUE scénario
      finit par un état du cadre EXACTEMENT PRÉDIT (image 0x9000 octet par
      octet : verdict, HRESULT d'origine, tailles de flux, zone d'émission
      — clair copié, chiffré produit, ou ZÉROS après destruction) et un
      contrat d'appels complet (QCA : phContext cadre+0x10, ulAttribute 4
      = SECPKG_ATTR_STREAM_SIZES VÉRIFIÉ À LA SOURCE, pBuffer cadre+0x40 ;
      EM : phContext cadre+0x10, fQOP 0, MessageSeqNo 0, descripteur tls-03
      type 1 exact — en-tête/clair/queue aux pointeurs de la convention
      contiguë ; traces tcp-04 [socket, pointeur, longueur] prédites appel
      par appel — achèvement) ; le span de l'appelant est OCTET POUR OCTET
      intact (Q3) ;
  V3  fuzzing à propriétés : longueurs hostiles, tailles négociées
      aléatoires (message maximal >= 1 — un zéro est hors contrat : la
      bibliothèque d'une session vivante ne le rend jamais), verdicts shim
      aléatoires (documentés ET exotiques), émissions partielles et rompues
      — survie, terminaison, ZÉRO écart contre le modèle ;
  V4  falsification : SIX mutations D'UN SEUL point de la notation, STABLES
      EN TAILLE (leçon D82), chacune ATTRAPÉE par le différentiel ; le
      témoin intact reste vert.

Règles shims PARTAGÉES modèle/émulation (jamais deux sources de vérité) :
QCA en succès consigne les 5 u32 ; en échec elle BARBOUILLE (le zéro
défensif de la notation doit annuler — modèle tls-05 D82). EM en succès
chiffre SUR PLACE (en-tête et queue = motifs déterministes, clair XOR
flux déterministe) et CONSIGN les trois cbBuffer (leçon D83 (d) : une
vraie bibliothèque écrit les longueurs produites) ; en échec elle ne
touche rien (le clair copié subsiste — la notation DOIT le détruire,
Q2). EM en descripteur invalide (notation mutée) : SEC_E_INVALID_TOKEN,
fail-closed, aucune écriture. send : 'plein' | k partiel | <= 0 échec.

Le modèle de référence est écrit depuis la SPÉCIFICATION (jamais la
notation) : verdict_modele via layout.HRESULTS, cadre aux offsets
layout.CADRE_*, découpe au message maximal NÉGOCIÉ (jamais constante).
Les adresses de PILE du descripteur sont vérifiées par PRÉDICAT —
l'adresse exacte appartient à la notation, le CONTENU au contrat.
Usage : python3 harnais_emission.py [--graine G] [--cas N]
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

ZONE_LIBC = 0x1000              # page .text : libc-01 @0x1100, libc-07 @0x13C0
TAILLE_LIBC = 0x1000
ZONE_RDATA = 0x2000             # page .rdata : IAT kernel32/ws2_32/secur32 + fixture
TAILLE_RDATA = 0x1000
ZONE_TCP = 0x4000               # page .text2 : tcp-04 @0x4180
TAILLE_TCP = 0x1000
ZONE_CODE = 0x6000              # page .text3 : tls-02/03/06 (le bloc sous test)
TAILLE_CODE = 0x1000
RET_MAGIQUE = 0x6F00            # adresse d'arrêt propre (int3 de la page code)
TRAMPOLINE = 0x140100000        # fausses adresses d'API (page RX, mécanisme M2/M3)
TAILLE_TRAMP = 0x1000
ZONE_CADRE = 0x150000000        # cadre de session TLS complet (0x8260) + marge
TAILLE_CADRE_PAGE = 0x9000
ZONE_SPAN = 0x160000000         # span clair de l'appelant (http-10:R2) + canaris
TAILLE_SPAN = 0x10000
MARGE_SPAN = 0x100
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP = 0x7F008000

RVA_TLS06, SLOT_TLS06 = 0x6740, 0x300
RVA_TLS02, SLOT_TLS02 = 0x6080, 0x100
RVA_TLS03, SLOT_TLS03 = 0x6180, 0x140
RVA_TCP04 = 0x4180
RVA_MEMCPY = 0x1100
RVA_MEMSET = 0x13C0

# fausses adresses : secur32 (7) + ws2_32 send explicite + le reste des imports
# M3 (toute frappe = faux pas nommé — I1/I3 : seuls QCA, EM et send sont légitimes)
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
SOCKET_SENT = 0x7777777777777777

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


def entete_em(i: int, n: int) -> bytes:
    """Octets d'en-tête d'enregistrement écrits PAR la bibliothèque (règle shim)."""
    return motif(200 + i, n)


def queue_em(i: int, n: int) -> bytes:
    """Octets de queue d'enregistrement écrits PAR la bibliothèque (règle shim)."""
    return motif(300 + i, n)


def chiffrer(i: int, clair: bytes) -> bytes:
    """Chiffrement SUR PLACE déterministe (règle shim — XOR flux)."""
    ks = motif(400 + i, len(clair))
    return bytes(a ^ b for a, b in zip(clair, ks))


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


def image_initiale(tailles: tuple | None = None) -> bytearray:
    """Cadre post-tls-04 : credentials acquis, contexte ÉTABLI, socket connectée.
    Le bloc tailles est VIERGE (zéros — convention D81 : http-10:R2 fournit le
    cadre vierge, la garde cBuffers @+0x4C s'appuie dessus) ou déjà consigné
    (scénario I3 : acquisition sautée)."""
    page = bytearray(CANARI * TAILLE_CADRE_PAGE)

    def q(off, lo, hi):
        page[off:off + 16] = struct.pack("<QQ", lo, hi)   # SecHandle = 2 x u64
    q(L.CADRE_CRED, *MAGIC_CRED)
    q(L.CADRE_CTXT, *MAGIC_FINAL)
    q(L.CADRE_SOCKET, SOCKET_SENT, 0)
    q(L.CADRE_PTR_NOM, ZONE_CADRE + L.CADRE_NOM_ZONE, 0)
    page[L.CADRE_TAILLES:L.CADRE_TAILLES + 20] = (
        struct.pack("<5I", *tailles) if tailles else b"\x00" * 20)
    return page


def span_modele(ln: int) -> bytes:
    """Contenu clair du span de l'appelant — déterministe, partagé."""
    return motif(13, ln)


class Script:
    """Comportements shims déterministes par INDICE d'appel (jamais de file
    épuisable) : qca[i] = (HRESULT, tailles 5-tuple) ; em[i] = HRESULT ;
    send[i] = 'plein' | k (partiel) | <= 0 (échec)."""

    TAILLES_DEFAUT = (5, 16, 512, 4, 8)

    def __init__(self, qca: list, em: list, send: list):
        self.entries_qca = qca
        self.entries_em = em
        self.entries_send = send

    def comportement_qca(self, i: int) -> tuple[int, tuple]:
        if i < len(self.entries_qca):
            return self.entries_qca[i]
        return (0, self.TAILLES_DEFAUT)

    def hresult_em(self, i: int) -> int:
        if i < len(self.entries_em):
            return self.entries_em[i]
        return 0

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


class Modele:
    """La boucle de la spécification, en Python — même environnement shims."""

    def __init__(self, script: Script, image0: bytes):
        self.script = script
        self.page = bytearray(image0)
        self.appels: list[tuple] = []
        self.i_qca = self.i_em = self.i_send = 0

    def _dw32(self, off: int, v: int) -> None:
        self.page[off:off + 4] = struct.pack("<I", v & 0xFFFFFFFF)

    def executer(self, span: bytes, ln: int) -> tuple[int, list, bytes]:
        # --- P4 : acquisition UNE fois par session (garde cBuffers) ---
        if struct.unpack_from("<I", self.page, L.CADRE_TAILLES + 12)[0] == 0:
            h, tailles = self.script.comportement_qca(self.i_qca)
            self.appels.append(("QCA", ZONE_CADRE + L.CADRE_CTXT, 4,
                                ZONE_CADRE + L.CADRE_TAILLES))
            self.i_qca += 1
            v = verdict_modele(h)
            self._dw32(L.CADRE_HRESULT, h)
            if v != 0:
                # E3 : le zéro défensif de la notation annule la barbouille
                self.page[L.CADRE_TAILLES:L.CADRE_TAILLES + 20] = b"\x00" * 20
                self._dw32(L.CADRE_VERDICT, v)
                return v, self.appels, bytes(self.page)
            struct.pack_into("<5I", self.page, L.CADRE_TAILLES, *tailles)
        cbh, cbt, maxmsg = struct.unpack_from("<3I", self.page, L.CADRE_TAILLES)
        # --- do-while : longueur 0 → UN enregistrement vide (P3) ---
        pos, restant = 0, ln
        while True:
            m = restant if restant <= maxmsg else maxmsg
            # copie libc-01 du morceau vers zone+en-tête (Q3 : le span ne bouge pas)
            self.page[L.CADRE_EMISSION + cbh:L.CADRE_EMISSION + cbh + m] = span[pos:pos + m]
            i_em = self.i_em
            h = self.script.hresult_em(i_em)
            v = verdict_modele(h)
            self.appels.append((
                "EM", ZONE_CADRE + L.CADRE_CTXT, 0, "PILE", 0,
                [(cbh, L.SECBUFFER_STREAM_HEADER, ZONE_CADRE + L.CADRE_EMISSION),
                 (m, L.SECBUFFER_DATA, ZONE_CADRE + L.CADRE_EMISSION + cbh),
                 (cbt, L.SECBUFFER_STREAM_TRAILER,
                  ZONE_CADRE + L.CADRE_EMISSION + cbh + m)]))
            self.i_em += 1
            self._dw32(L.CADRE_HRESULT, h)
            if v != 0:
                # E1 : le clair copié est DÉTRUIT (Q2 — aucun octet clair résiduel)
                n = cbh + m + cbt
                self.page[L.CADRE_EMISSION:L.CADRE_EMISSION + n] = b"\x00" * n
                self._dw32(L.CADRE_VERDICT, v)
                return v, self.appels, bytes(self.page)
            # la bibliothèque chiffre SUR PLACE + consigne les longueurs (règle shim)
            self.page[L.CADRE_EMISSION:L.CADRE_EMISSION + cbh] = entete_em(i_em, cbh)
            self.page[L.CADRE_EMISSION + cbh:L.CADRE_EMISSION + cbh + m] = \
                chiffrer(i_em, bytes(span[pos:pos + m]))
            self.page[L.CADRE_EMISSION + cbh + m:L.CADRE_EMISSION + cbh + m + cbt] = \
                queue_em(i_em, cbt)
            total = cbh + m + cbt
            # émission tcp-04 en boucle d'achèvement bornée (E2)
            envoye = 0
            while envoye < total:
                r = self.script.comportement_send(self.i_send, total - envoye)
                self.appels.append(("SEND", SOCKET_SENT,
                                    ZONE_CADRE + L.CADRE_EMISSION + envoye,
                                    total - envoye))
                self.i_send += 1
                if r <= 0:
                    self._dw32(L.CADRE_VERDICT, 5)
                    return 5, self.appels, bytes(self.page)
                envoye += r
            pos += m
            restant -= m
            if restant == 0:
                break
        self._dw32(L.CADRE_VERDICT, 0)
        return 0, self.appels, bytes(self.page)


# --- Émulateur à shims SSPI/ws2_32 (page ret + crochet code, mécanisme M2/M3) ----

def _pile_valide(p: int) -> bool:
    return ZONE_PILE <= p < ZONE_PILE + TAILLE_PILE


class Emulateur:
    """Un chargement = un émulateur NEUF (leçon D79). Les shims sont pilotés
    par le Script du cas ; les écritures de la « bibliothèque » suivent la
    même règle que le modèle (tailles, chiffrement sur place, barbouille)."""

    def __init__(self, blobs: dict):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        uc.mem_map(ZONE_LIBC, TAILLE_LIBC)
        uc.mem_map(ZONE_RDATA, TAILLE_RDATA)
        uc.mem_map(ZONE_TCP, TAILLE_TCP)
        uc.mem_map(ZONE_CODE, TAILLE_CODE)
        uc.mem_map(TRAMPOLINE, TAILLE_TRAMP)
        uc.mem_map(ZONE_CADRE, TAILLE_CADRE_PAGE)
        uc.mem_map(ZONE_SPAN, TAILLE_SPAN)
        uc.mem_map(ZONE_PILE, TAILLE_PILE)
        page_libc = b"\xCC" * TAILLE_LIBC
        for rva, blob in ((RVA_MEMCPY, blobs["libc-01"]),
                          (RVA_MEMSET, blobs["libc-07"])):
            page_libc = (page_libc[:rva - ZONE_LIBC] + blob +
                         page_libc[rva - ZONE_LIBC + len(blob):])
        uc.mem_write(ZONE_LIBC, page_libc)
        page_tcp = b"\xCC" * TAILLE_TCP
        page_tcp = (page_tcp[:RVA_TCP04 - ZONE_TCP] + blobs["tcp-04"] +
                    page_tcp[RVA_TCP04 - ZONE_TCP + len(blobs["tcp-04"]):])
        uc.mem_write(ZONE_TCP, page_tcp)
        page = b"\xCC" * TAILLE_CODE
        for rva, blob in ((RVA_TLS02, blobs["tls-02"]), (RVA_TLS03, blobs["tls-03"]),
                          (RVA_TLS06, blobs["tls-06"])):
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
        self.span_initial = b""
        self._i_qca = self._i_em = self._i_send = 0

    def _shim(self, uc: Uc, adresse: int, taille: int, donnees):
        nom = FAUX_REV.get(adresse)
        if nom is None:
            self.faux_pas.append(f"shim inconnu @{adresse:#x}")
            return
        methode = getattr(self, "_api_" + nom, None)
        if methode is None:
            self.faux_pas.append(f"{nom} appelé par tls-06 (I1/I3 violée)")
            return
        methode()

    def _pile(self, offset: int) -> int:
        """Argument pile de l'appelant, vu du shim ([rsp+0x28] = arg5 msx64)."""
        rsp = self.uc.reg_read(REGS["rsp"])
        return struct.unpack("<Q", bytes(self.uc.mem_read(rsp + offset, 8)))[0]

    # --- les TROIS seules APIs légitimes (I1/I3 : QCA, EM, send) --------------

    def _api_send(self):
        uc = self.uc
        sock = uc.reg_read(REGS["rcx"])
        buf = uc.reg_read(REGS["rdx"])
        ln = uc.reg_read(REGS["r8"])
        self.appels.append(("SEND", sock, buf, ln))
        r = self.script.comportement_send(self._i_send, ln)
        self._i_send += 1
        uc.reg_write(REGS["rax"], r & 0xFFFFFFFFFFFFFFFF)

    def _api_QueryContextAttributesW(self):
        uc = self.uc
        ph_ctxt = uc.reg_read(REGS["rcx"])
        attr = uc.reg_read(REGS["rdx"]) & 0xFFFFFFFF
        pbuf = uc.reg_read(REGS["r8"])
        self.appels.append(("QCA", ph_ctxt, attr, pbuf))
        h, tailles = self.script.comportement_qca(self._i_qca)
        self._i_qca += 1
        v = verdict_modele(h)
        if v == 0:
            uc.mem_write(pbuf, struct.pack("<5I", *tailles))
        else:
            # la bibliothèque BARBOUILLE en échec — le zéro défensif de la
            # notation doit annuler (modèle tls-05 D82, falsifiable)
            uc.mem_write(pbuf, struct.pack("<5I", 0xDEADBEEF, 0xCAFEBABE,
                                           0xFEEDFACE, 0xBAADF00D, 0x1DEA))
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

    def _lire_desc_em(self, p: int):
        """SecBufferDesc à 3 tampons (7/1/6) — None si invalide (notation mutée)."""
        try:
            b = bytes(self.uc.mem_read(p, 16))
            ulv, nb = struct.unpack_from("<II", b, 0)
            (pb,) = struct.unpack_from("<Q", b, 8)
            if ulv != L.SECBUFFER_VERSION or nb != 3:
                return None
            bufs = []
            for k in range(3):
                bb = bytes(self.uc.mem_read(pb + 16 * k, 16))
                cb, typ = struct.unpack_from("<II", bb, 0)
                (pv,) = struct.unpack_from("<Q", bb, 8)
                bufs.append((cb, typ, pv))
            if [t for _, t, _ in bufs] != [L.SECBUFFER_STREAM_HEADER,
                                            L.SECBUFFER_DATA,
                                            L.SECBUFFER_STREAM_TRAILER]:
                return None
            if any(cb > L.MAX_JETON for cb, _, _ in bufs):
                return None
            return (ulv, nb, pb, bufs)
        except Exception:
            return None

    def _api_EncryptMessage(self):
        uc = self.uc
        ph_ctxt = uc.reg_read(REGS["rcx"])
        fqop = uc.reg_read(REGS["rdx"]) & 0xFFFFFFFF
        p_msg = uc.reg_read(REGS["r8"])
        seq = uc.reg_read(REGS["r9"]) & 0xFFFFFFFF
        desc = self._lire_desc_em(p_msg)
        self.appels.append(("EM", ph_ctxt, fqop, p_msg, seq, desc))
        if desc is None:
            # descripteur invalide (notation mutée) — fail-closed, aucune écriture
            uc.reg_write(REGS["rax"], 0x80090308)
            return
        i = self._i_em
        h = self.script.hresult_em(i)
        v = verdict_modele(h)
        if v == 0:
            _ulv, _nb, pb, bufs = desc
            (cbh, _th, ph) = bufs[0]
            (cm, _td, pm) = bufs[1]
            (cbt, _tq, pq) = bufs[2]
            clair = bytes(uc.mem_read(pm, cm))
            uc.mem_write(ph, entete_em(i, cbh))          # en-tête PAR la bibliothèque
            uc.mem_write(pm, chiffrer(i, clair))         # chiffrement SUR PLACE (Q3)
            uc.mem_write(pq, queue_em(i, cbt))           # queue PAR la bibliothèque
            # la bibliothèque CONSIGN les longueurs produites (leçon D83 (d))
            uc.mem_write(pb + 0x00, struct.pack("<I", cbh))
            uc.mem_write(pb + 0x10, struct.pack("<I", cm))
            uc.mem_write(pb + 0x20, struct.pack("<I", cbt))
        self._i_em += 1
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

    def executer(self, script: Script, span: bytes, ln: int, image0: bytes) -> int:
        uc = self.uc
        self.script = script
        self.appels = []
        self.faux_pas = []
        self._i_qca = self._i_em = self._i_send = 0
        uc.mem_write(ZONE_CADRE, bytes(image0))
        page_span = bytearray(CANARI * TAILLE_SPAN)
        page_span[MARGE_SPAN:MARGE_SPAN + len(span)] = span
        self.span_initial = bytes(page_span)
        uc.mem_write(ZONE_SPAN, self.span_initial)
        for nom, valeur in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], valeur)
        uc.reg_write(REGS["rsp"], RSP)
        uc.mem_write(RSP, struct.pack("<Q", RET_MAGIQUE))
        uc.reg_write(REGS["rcx"], ZONE_CADRE)
        uc.reg_write(REGS["rdx"], ZONE_SPAN + MARGE_SPAN)
        uc.reg_write(REGS["r8"], ln)
        uc.reg_write(REGS["r9"], 0xCCCCCCCC)
        uc.emu_start(RVA_TLS06, RET_MAGIQUE, timeout=5_000_000, count=2_000_000)
        return uc.reg_read(REGS["rax"]) & 0xFFFFFFFF

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
        if bytes(self.uc.mem_read(ZONE_SPAN, TAILLE_SPAN)) != self.span_initial:
            problemes.append("span de l'appelant modifié (Q3 violée)")
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
        if a[0] == "SEND":
            if a[1] != e[1]:
                problemes.append(f"SEND #{k} socket {a[1]:#x} != {e[1]:#x}")
            if a[2] != e[2]:
                problemes.append(f"SEND #{k} pointeur {a[2]:#x} != {e[2]:#x}")
            if a[3] != e[3]:
                problemes.append(f"SEND #{k} longueur {a[3]} != {e[3]}")
            continue
        if a[0] == "QCA":
            for idx, nomch in ((1, "phContext"), (2, "ulAttribute"), (3, "pBuffer")):
                if a[idx] != e[idx]:
                    problemes.append(f"QCA #{k} {nomch} {a[idx]!r} != {e[idx]!r}")
            continue
        # EM : (nom, phContext, fQOP, pMessage, MessageSeqNo, descripteur)
        for idx, nomch in ((1, "phContext"), (2, "fQOP"), (4, "MessageSeqNo")):
            if a[idx] != e[idx]:
                problemes.append(f"EM #{k} {nomch} {a[idx]!r} != {e[idx]!r}")
        if e[3] == "PILE":
            if not _pile_valide(a[3]) or a[3] % 8:
                problemes.append(f"EM #{k} pMessage {a[3]:#x} hors pile/aligné")
        elif a[3] != e[3]:
            problemes.append(f"EM #{k} pMessage {a[3]:#x} != {e[3]:#x}")
        if e[5] is None:
            if a[5] is not None:
                problemes.append(f"EM #{k} descripteur présent à tort")
            continue
        if a[5] is None:
            problemes.append(f"EM #{k} descripteur ABSENT/invalide")
            continue
        ulv, nb, pb, bufs = a[5]
        if (ulv, nb) != (0, 3):
            problemes.append(f"EM #{k} descripteur (v={ulv}, n={nb}) != (0, 3)")
        if pb != a[3] + 0x10:
            problemes.append(f"EM #{k} pBuffers {pb:#x} != pMessage+0x10")
        for j, ((cb_a, t_a, pv_a), (cb_e, t_e, pv_e)) in enumerate(zip(bufs, e[5])):
            if (cb_a, t_a, pv_a) != (cb_e, t_e, pv_e):
                problemes.append(
                    f"EM #{k} tampon {j} (cb={cb_a}, t={t_a}, pv={pv_a:#x}) != "
                    f"(cb={cb_e}, t={t_e}, pv={pv_e:#x})")
    return problemes


# --- V2/V3 : différentiel ---------------------------------------------------------

def jouer_cas(emu: Emulateur, script: Script, etiquette: str, ln: int,
              image0: bytes, span: bytes | None = None) -> list[str]:
    """Exécute UN cas contre le modèle — écarts nommés."""
    span = span if span is not None else span_modele(ln)
    v_att, appels_att, image_att = Modele(script, image0).executer(span, ln)
    rax = emu.executer(script, span, ln, image0)
    problemes: list[str] = []
    if rax != v_att:
        problemes.append(f"rax {rax} != {v_att} (modèle spec)")
    image_lue = bytes(emu.uc.mem_read(ZONE_CADRE, TAILLE_CADRE_PAGE))
    if image_lue != image_att:
        off = next(o for o in range(TAILLE_CADRE_PAGE) if image_lue[o] != image_att[o])
        problemes.append(f"cadre diverge @+0x{off:x} (attendu {image_att[off]:#04x}, "
                         f"lu {image_lue[off]:#04x})")
    problemes += comparer_traces(emu.appels, appels_att)
    problemes += emu.hygiene()
    return problemes


OK = 0x00000000
TAILLES_EXOTIQUES = (17, 33, 200, 4, 1)

SCENARIOS_V2 = [
    ("span de 1 octet",
     Script([(0, (5, 16, 512, 4, 8))], [], []), 1, None),
    ("span du message maximal exact (512)",
     Script([(0, (5, 16, 512, 4, 8))], [], []), 512, None),
    ("span de 2 × maximal + 1 (chaîne de découpe : 512+512+1)",
     Script([(0, (5, 16, 512, 4, 8))], [], []), 1025, None),
    ("tailles négociées exotiques (17/33/200) — découpe 200+200+50",
     Script([(0, TAILLES_EXOTIQUES)], [], []), 450, None),
    ("EncryptMessage en verdict 5 AU MILIEU d'une chaîne (E1, scrub)",
     Script([(0, (5, 16, 512, 4, 8))], [0, 0x80090308], []), 1025, None),
    ("tcp-04 en émission partielle exigeant l'achèvement",
     Script([(0, (5, 16, 512, 4, 8))], [], [40, 30, "plein"]), 100, None),
    ("tcp-04 en échec système — E2, verdict 5",
     Script([(0, (5, 16, 512, 4, 8))], [], [-1]), 100, None),
    ("échec d'acquisition des tailles — E3, barbouille annulée, AUCUN enregistrement",
     Script([(0x80090308, (5, 16, 512, 4, 8))], [], []), 100, None),
    ("span de longueur nulle — UN enregistrement vide (P3)",
     Script([(0, (5, 16, 512, 4, 8))], [], []), 0, None),
    ("tailles déjà consignées — QCA JAMAIS rappelée (I3/P4)",
     Script([], [], []), 300, (5, 16, 512, 4, 8)),
    ("EM en verdict 3 (HRESULT de certificat — routage tls-02 intégral)",
     Script([(0, (5, 16, 512, 4, 8))], [0x80090325], []), 100, None),
    ("EM en verdict 6 (HRESULT exotique — table TOTALE)",
     Script([(0, (5, 16, 512, 4, 8))], [0x81234567], []), 100, None),
    ("émission partielle sur plusieurs enregistrements",
     Script([(0, (5, 16, 300, 4, 8))], [], [50, "plein", 7]), 700, None),
]

MUTATIONS_V4 = [
    ("M1 attribut QCA dévié (4 → 5)", ("mov edx, 4", "mov edx, 5")),
    ("M2 descripteur tls-03 dévié (r9 +0x98)",
     ("lea r9, [rsp + 0x90]", "lea r9, [rsp + 0x98]")),
    ("M3 pMessage EM dévié (r8 +0x98)",
     ("lea r8, [rsp + 0x90]", "lea r8, [rsp + 0x98]")),
    ("M4 socket déviée (cadre+0x28)",
     ("mov rcx, [rdx + 0x20]", "mov rcx, [rdx + 0x28]")),
    ("M5 scrub amputé (queue → en-tête)",
     ("add r8d, [rdx + 0x44]", "add r8d, [rdx + 0x40]")),
    ("M6 achèvement court-circuité (jz → jnz)", ("jz 0x68af", "jnz 0x68af")),
]


def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261028)
    parseur.add_argument("--cas", type=int, default=5000)
    args = parseur.parse_args()
    rng = random.Random(args.graine)

    print("=== harnais_emission.py — tls-06:R1 (émission chiffrée, D84 session) ===")
    print(f"graine {args.graine} · fuzz {args.cas} cas")

    ks = Ks(KS_ARCH_X86, KS_MODE_64)

    # --- V1 : round-trip ------------------------------------------------------
    print("\n[V1] round-trip de notation")
    blob06, declare = octets_notation(ks, "tls-06-emission", RVA_TLS06)
    controle("tls-06-emission rassemblée == taille déclarée (Code : N o)",
             declare is not None and len(blob06) == declare, f"{len(blob06)} o")
    controle("padding du slot >= 16 (D8) — slot 0x300 préfiguré conservé",
             SLOT_TLS06 - len(blob06) >= 16, f"{SLOT_TLS06 - len(blob06)} o")
    blobs = {"tls-06": blob06}
    # tls-02/tls-03 : notations M4 (locales) ; tcp-04 : m2 ; libc-01/07 : m1
    # (octets hérités scellés R7 — les chemins sont ceux des dépôts m1/m2)
    CHEMIN_M1 = os.path.join(ICI, os.pardir, "m1", "notation")
    CHEMIN_M2 = os.path.join(ICI, os.pardir, "m2", "notation")
    for bloc, rva, chemin in (("tls-02-verdicts", RVA_TLS02, None),
                              ("tls-03-jetons", RVA_TLS03, None),
                              ("tcp-04-send", RVA_TCP04, CHEMIN_M2),
                              ("libc-01-memcpy", RVA_MEMCPY, CHEMIN_M1),
                              ("libc-07-memset", RVA_MEMSET, CHEMIN_M1)):
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
    for nom, script, ln, tailles_pre in SCENARIOS_V2:
        image0 = image_initiale(tailles_pre)
        problemes = jouer_cas(emu, script, nom, ln, image0)
        v_att = Modele(script, image0).executer(span_modele(ln), ln)[0]
        controle(f"scénario « {nom} »", not problemes,
                 "; ".join(problemes[:3]) if problemes else
                 f"verdict {v_att}, {len(emu.appels)} appel(s)")

    # --- V3 : fuzzing à propriétés -------------------------------------------
    print(f"\n[V3] fuzzing à propriétés — {args.cas} cas hostiles")
    codes_documentes = list(L.HRESULTS.keys())
    ecarts = 0
    for i in range(args.cas):
        ln = rng.randint(0, 800)
        span = bytes(rng.getrandbits(8) for _ in range(ln))
        # tailles : message maximal >= 1 (un zéro est hors contrat — la boucle
        # do-while n'avancerait jamais ; une bibliothèque de session vivante
        # ne le rend jamais — borne consignée dans l'en-tête du harnais)
        t = (rng.randint(0, 64), rng.randint(0, 80), rng.randint(1, 600),
             rng.randint(1, 8), rng.randint(0, 16))
        pre = rng.random() < 0.3
        qca = [] if pre else [(rng.choice([0, 0, 0, 0,
                                           rng.choice(codes_documentes)]), t)]
        image0 = image_initiale(t if pre else None)
        maxmsg = t[2]
        n_rec = ln // maxmsg + 3
        em = [0 if rng.random() < 0.82 else
              (rng.choice(codes_documentes) if rng.random() < 0.6
               else rng.getrandbits(32))
              for _ in range(n_rec)]
        envois = [rng.choice(["plein", "plein", "plein", "plein",
                              rng.randint(1, 40), -1, 0]) for _ in range(24)]
        script = Script(qca, em, envois)
        problemes = jouer_cas(emu, script, "fuzz", ln, image0, span)
        if problemes:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart #{ecarts} cas {i} : {'; '.join(problemes[:3])}")
    controle(f"fuzz {args.cas} cas : ZÉRO écart", ecarts == 0, f"{ecarts} écart(s)")

    # --- V4 : falsification ---------------------------------------------------
    print("\n[V4] falsification — six mutations d'un point, chacune attrapée")
    cas_mutants = [(script, ln, image_initiale(tp)) for _, script, ln, tp in SCENARIOS_V2]
    for nom, mutation in MUTATIONS_V4:
        blob_m, _ = octets_notation(ks, "tls-06-emission", RVA_TLS06, mutation)
        blobs_m = dict(blobs)
        blobs_m["tls-06"] = blob_m
        emu_m = Emulateur(blobs_m)
        attrapes = 0
        for script, ln, image0 in cas_mutants:
            try:
                if jouer_cas(emu_m, script, "mutant", ln, image0):
                    attrapes += 1
            except Exception:
                attrapes += 1          # faute d'exécution = écart nommé
        controle(f"mutation « {nom} » ATTRAPÉE", attrapes > 0,
                 f"{attrapes}/{len(cas_mutants)} cas en écart")
    # témoin intact : le différentiel reste vert (une suite qui ne peut pas
    # échouer ne prouve rien — le témoin prouve que les pièges sont armés)
    emu_t = Emulateur(blobs)
    verts = sum(1 for script, ln, image0 in cas_mutants
                if not jouer_cas(emu_t, script, "témoin", ln, image0))
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
