#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_session.py — Harnais à propriétés de tls-08 (session TLS cliente, D90 session).

LE bloc orchestrateur du jalon M4 : la session complète de bout en bout —
connexion, nom, credentials, poignée, requête chiffrée, relais, compensation
INTÉGRALE. La notation est émulée à son RVA .text3 exact AVEC les vrais
octets de TOUTE sa chaîne d'appel : tls-01..07 (M4), tcp-13 (M3),
tcp-03/04/05/tcp-11 (M2), hello-02 + libc-01/03/04/07 (M0/M1) — DIX-HUIT
blocs réels, l'intégration la plus large du projet ; l'IAT kernel32/ws2_32/
secur32 reçoit des fausses adresses (résolution chargeur, mécanisme M2/M3 :
page trampoline de ret + crochet code). Vecteurs de la spécification
tls-08:R1 :

  V1  round-trip de notation 100 % (taille totale == « Code : N o », padding
      >= 16 — D8) pour tls-08 ET les dix-sept blocs intégrés ;

  V2  oracle à scénarios — la compensation constatée PAR COMPTAGE (Q3) :
      les SEPT scénarios de la spec — succès complet ; certificat invalide
      (I4 : la ligne console « certificat rejete » ET la compensation,
      Delete 1 sur le contexte barbouillé par la bibliothèque) ; échec
      tcp-13 (compensation triviale : AUCUN appel) ; verdict 5 à la
      poignée ; altération en plein relais (E3 : réponse tronquée propre —
      le client garde ce qui fut déjà pompé, le verdict revient) ;
      close_notify avec résidu (curiosité consignée : utile > 0 au cadre) ;
      échec de libération simulé (E4 : verdict testé, UNE ressaisie,
      l'ordre jamAIS interrompu) — PLUS les frontières propres à
      l'orchestrateur : drain de deux enregistrements en un lot (aucune
      réception entre les deux tls-07 — jamais un record déchiffrable en
      zone pendant que tcp-03 attendrait) ; fermeture système par tcp-03 ;
      client parti en plein pompage ; boucle sans fin (E5, 16 allers) ;
      tls-01 en refus (la cible ne peut être nommée : verdict 7, socket
      compensée) ; densité hostile (garde chambre nulle AVANT tcp-03 — son
      P3 exige r8 > 0 : c'est la « zone dépassée » de la table http-10:R2) ;
      lot exactement consommé de 0x8000 (la région VIDE rend sa géométrie
      morte : offset repris en tête, D90 — sans elle une session saine
      mourrait à la frontière) ; ACH en échec (rien n'est acquis, la socket
      seule est compensée) ; verdict 6 exotique ; incomplet-puis-complet ;
      émission cliente partielle exigeant l'achèvement ; connect en échec
      (le nettoyage INTERNE de tcp-13 : closesocket+freeaddrinfo, sa Q4) —
      CHAQUE scénario finit par : l'image du cadre OCTET PAR OCTET
      (0xD000, cadre vierge = canari — la défense de tls-08 ne repose pas
      sur la bonne volonté de l'amont), le paquet INTACT (hôte/requête
      inchangés, Q3 de tls-06 — le clair de l'appelant jamAIS touché), le
      contrat d'appels COMPLET (GAI/socket/connect/freeaddrinfo, ACH, ISC
      [11 arguments + descripteurs tls-03 type 0], QCA, EM, DM, RECV/SEND
      socket-pointeur-longueur, DSC/FCH, closesocket, ECS/WF/LCS — la
      ligne console EXACTE, octets compris) ET les comptes de compensation
      attendus (Acquire 1 / Delete 0-1 [+1 en échec simulé] / Free 1
      [+1 idem] / tcp-05 serveur 1) ;

  V3  NON APPLICABLE (spec tls-08:V3 : aucune entrée non fiable directe —
      tout traverse tls-01..07 d'abord ; héritage de la règle M3 pour les
      orchestrateurs, consigné ici pour la traçabilité) ;

  V4  falsification : DOUZE mutations D'UN SEUL point de la notation,
      STABLES EN TAILLE (leçon D82), chacune ATTRAPÉE par le différentiel ;
      le témoin intact reste vert (une suite qui ne peut pas échouer ne
      prouve rien).

Règles shims PARTAGÉES modèle/émulation (jamais deux sources de vérité) :
GAI réussit et pose une addrinfo AF_INET factice ; socket/connect/closesocket/
recv/send pilotés par le script (déterministes par INDICE) ; ACH écrit le
handle au cadre (barbouille en échec — tls-05 annule, modèle D82) ; ISC
consigne le jeton produit + cbBuffer (jamais la capacité — leçon D83 (d)),
écrit le contexte (MAGIC_FINAL/PARTIAL/ORDURE) et pfContextAttr 0x141 ; QCA
écrit les tailles (barbouille en échec) ; EM chiffre SUR PLACE + en-tête/
queue PAR la bibliothèque + reconduit les cbBuffer ; DM déchiffre SUR PLACE
+ réécrit les tampons 0/1 (règles D89) + MISSING sans toucher la zone ;
DSC/FCH refusent un handle NUL (SEC_E_INVALID_HANDLE — la vraie bibliothèque
n'en veut pas : le mutant qui libère à vide est nommé) ; WF lit la ligne
composée (le contrat porte les OCTETS) ; ECS/LCS ne touchent pas la mémoire
de la section critique (le stub n'écrit rien — l'état .data reste intact).

Le modèle de référence est écrit depuis les SPÉCIFICATIONS (jamais la
notation) : verdict_modele via layout.HRESULTS, cadre aux offsets
layout.CADRE_*, paquet layout.PAQUET_*, verdict propre layout.VERDICT_CIBLE,
capacité layout.CAPACITE_RECEPTION. Les adresses de PILE internes aux
appelés (descripteurs, pfQOP, node tcp-13, sockaddr, tampon console) sont
vérifiées par PRÉDICAT — l'adresse exacte appartient à la notation de
L'APPELÉ, le CONTENU au contrat.
Usage : python3 harnais_session.py [--graine G]
"""

from __future__ import annotations

import argparse
import os
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

ZONE_TEXTE = 0x1000              # .text : hello-02 @0x1040, libc-01/03/04/07
TAILLE_TEXTE = 0x1000
ZONE_RDATA = 0x2000              # .rdata : IAT kernel32/ws2_32/secur32 + fixtures
TAILLE_RDATA = 0x1000
ZONE_TCP = 0x4000                # .text2 : tcp-03/04/05, tcp-13, tcp-11
TAILLE_TCP = 0x1000
ZONE_CODE = 0x6000               # .text3 : tls-01..08 (le bloc sous test + sa chaîne)
TAILLE_CODE = 0x2000
RET_MAGIQUE = 0x7E00             # int3 de la zone réservée .text3 (arrêt propre)
ZONE_DATA = 0x3000               # page couvrant .data (R_STDOUT @0x3800, R_CS @0x3830)
TAILLE_DATA = 0x1000             # 0x3800 n'est pas aligné page — la page englobe
TRAMPOLINE = 0x140100000         # fausses adresses d'API (page RX, mécanisme M2/M3)
TAILLE_TRAMP = 0x1000
ZONE_CADRE = 0x150000000         # cadre de session TLS complet (0xC260) + canaris
TAILLE_CADRE_PAGE = 0xD000
ZONE_PAQUET = 0x160000000        # paquet + hôte + requête + canaris
TAILLE_PAQUET = 0x10000
PAQUET_HOTE = ZONE_PAQUET + 0x100
PAQUET_REQUETE = ZONE_PAQUET + 0x200
ZONE_ADDRINFO = 0x170000000      # addrinfo factice posée par le shim getaddrinfo
TAILLE_ADDRINFO = 0x1000
ADRESSE_ADDRINFO = ZONE_ADDRINFO
ADRESSE_SOCKADDR = ZONE_ADDRINFO + 0x40
FAKE_ADDR = 0x0A000001           # 10.0.0.1 — l'adresse de la cible factice
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x20000
RSP = 0x7F008008                 # ≡ 8 mod 16 — entrée ABI exacte (P5 des M2/M3)

RVA_TLS08, SLOT_TLS08 = 0x6D40, 0x600
RVA_TLS01, RVA_TLS02, RVA_TLS03 = 0x6000, 0x6080, 0x6180
RVA_TLS04, RVA_TLS05 = 0x62C0, 0x65C0
RVA_TLS06, RVA_TLS07 = 0x6740, 0x6A40
RVA_TCP03, RVA_TCP04, RVA_TCP05 = 0x4140, 0x4180, 0x41C0
RVA_TCP11, RVA_TCP13 = 0x4B00, 0x4400
RVA_HELLO02, RVA_MEMCPY = 0x1040, 0x1100
RVA_STRLEN, RVA_ITOA, RVA_MEMSET = 0x1200, 0x1280, 0x13C0

ZONE_RECEPTION = ZONE_CADRE + L.CADRE_RECEPTION   # la zone DANS le cadre (D89)

# fausses adresses : secur32 (7) + ws2_32 réseau + kernel32 console — tout le
# reste des imports M3 reste faux (toute frappe = faux pas nommé — I2/I3)
FAUX = {nom: TRAMPOLINE + (i + 1) * 0x10
        for i, nom in enumerate(L.SECUR32_IMPORTS)}
FAUX.update({"recv": TRAMPOLINE + 0x100, "send": TRAMPOLINE + 0x110,
             "closesocket": TRAMPOLINE + 0x120, "socket": TRAMPOLINE + 0x130,
             "connect": TRAMPOLINE + 0x140, "getaddrinfo": TRAMPOLINE + 0x150,
             "freeaddrinfo": TRAMPOLINE + 0x160,
             "WriteFile": TRAMPOLINE + 0x170,
             "EnterCriticalSection": TRAMPOLINE + 0x180,
             "LeaveCriticalSection": TRAMPOLINE + 0x190})
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
MAGIC_CRED = (0xC1C1C1C1C1C1C1C1, 0xC2C2C2C2C2C2C2C2)   # acquis par tls-05
MAGIC_PARTIAL = (0x1111111111111111, 0x2222222222222222)  # en cours d'établissement
MAGIC_FINAL = (0xABABABABABABABAB, 0xCDCDCDCDCDCDCDCD)   # contexte établi
MAGIC_ORDURE = (0xDEAD, 0xBEEF)                           # barbouillage en échec
SOCKET_SERVEUR = 0x7777777777777777
SOCKET_CLIENT = 0x8888888888888888
FAKE_STDOUT = 0x5A5A5A5A5A5A5A5A

HOTE_DEFAUT = b"exemple.fr"
REQUETE_DEFAUT = b"GET /chemin HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"
PORT_DEFAUT = 443

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
    """Octets d'en-tête d'enregistrement écrits PAR la bibliothèque (règle D88)."""
    return motif(200 + i, n)


def queue_em(i: int, n: int) -> bytes:
    """Octets de queue d'enregistrement écrits PAR la bibliothèque (règle D88)."""
    return motif(300 + i, n)


def chiffrer(i: int, clair: bytes) -> bytes:
    """Chiffrement SUR PLACE déterministe (règle D88 — XOR flux)."""
    ks = motif(400 + i, len(clair))
    return bytes(a ^ b for a, b in zip(clair, ks))


def clair_dm(i: int, n: int) -> bytes:
    """Octets clairs déchiffrés SUR PLACE par la « bibliothèque » (règle D89)."""
    return motif(500 + i, n)


def permuter16(v: int) -> int:
    """Ordre hôte → ordre réseau sur 16 bits (l'instruction rol ax, 8 de tcp-13)."""
    return ((v & 0xFF) << 8) | ((v >> 8) & 0xFF)


# --- HRESULT canoniques -----------------------------------------------------------

OK = 0x00000000
CONT = 0x00090312
INCOMPLET = 0x80090318
CONTEXTE_EXPIRE = 0x00090317
ALTERE = 0x8009030F
CERT_INVALIDE = 0x80090325
INVALID_TOKEN = 0x80090308
INVALID_HANDLE = 0x80090301
EXOTIQUE = 0x81234567


def verdict_modele(hresult: int) -> int:
    """tls-02:R1 via la liste blanche de la spécification (layout.HRESULTS)."""
    return L.HRESULTS.get(hresult & 0xFFFFFFFF, L.VERDICT_FATAL)


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


# --- Script de comportements (index-based : modèle et shims voient le même) ------

class Script:
    """Comportements shims déterministes par INDICE d'appel (jamais de file
    épuisable) : gai[i] = code de retour (0 succès) ; socket[i] = valeur de
    retour de socket() (−1 échec) ; connect[i] = code de retour (0 succès) ;
    ach = HRESULT unique d'AcquireCredentialsHandleW ; isc[i] = (HRESULT,
    longueur du jeton produit) ; qca[i] = (HRESULT, tailles) ; em[i] =
    HRESULT ; dm[i] = (HRESULT, en-tête, clair, queue) ; recv[i] = n (> 0
    données, 0 fermeture, < 0 erreur) ou 'max' (remplit la capacité) ;
    send[i] = 'plein' | k (partiel) | <= 0 (échec) ; dsc[i]/fch[i] = HRESULT
    des libérations (la ressaisie E4 lit l'indice suivant)."""

    TAILLES_DEFAUT = (5, 16, 512, 4, 8)

    def __init__(self, gai: list | None = None, socket_: list | None = None,
                 connect: list | None = None, ach: int = 0, isc: list | None = None,
                 qca: list | None = None, em: list | None = None,
                 dm: list | None = None, recv: list | None = None,
                 send: list | None = None, dsc: list | None = None,
                 fch: list | None = None):
        self.entries_gai = gai or []
        self.entries_socket = socket_ or []
        self.entries_connect = connect or []
        self.hresult_ach = ach
        self.entries_isc = isc or []
        self.entries_qca = qca or []
        self.entries_em = em or []
        self.entries_dm = dm or []
        self.entries_recv = recv or []
        self.entries_send = send or []
        self.entries_dsc = dsc or []
        self.entries_fch = fch or []

    def hresult_gai(self, i: int) -> int:
        return self.entries_gai[i] if i < len(self.entries_gai) else 0

    def ret_socket(self, i: int) -> int:
        return self.entries_socket[i] if i < len(self.entries_socket) else SOCKET_SERVEUR

    def hresult_connect(self, i: int) -> int:
        return self.entries_connect[i] if i < len(self.entries_connect) else 0

    def comportement_isc(self, i: int) -> tuple[int, int]:
        if i < len(self.entries_isc):
            return self.entries_isc[i]
        return (CONT, 8)              # défaut : continuation, jeton de 8 o

    def comportement_qca(self, i: int) -> tuple[int, tuple]:
        if i < len(self.entries_qca):
            return self.entries_qca[i]
        return (0, self.TAILLES_DEFAUT)

    def hresult_em(self, i: int) -> int:
        return self.entries_em[i] if i < len(self.entries_em) else 0

    def comportement_dm(self, i: int) -> tuple:
        if i < len(self.entries_dm):
            return self.entries_dm[i]
        return (OK, 5, 256, 16)

    def donnees_recv(self, i: int, capacite: int) -> tuple[int, bytes]:
        if i < len(self.entries_recv):
            e = self.entries_recv[i]
        else:
            e = 16                   # défaut : 16 octets de données
        if e == "max":
            n = capacite
        elif e <= 0:
            n = e
        else:
            n = min(e, capacite)     # une vraie socket ne rend jamais plus que demandé
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

    def hresult_dsc(self, i: int) -> int:
        return self.entries_dsc[i] if i < len(self.entries_dsc) else 0

    def hresult_fch(self, i: int) -> int:
        return self.entries_fch[i] if i < len(self.entries_fch) else 0


# --- Modèle de référence (écrit depuis les SPÉCIFICATIONS — jamais la notation) ---

def image_vierge() -> bytes:
    """Cadre VIERGE réaliste (P1 de tls-08 : http-10:R2 le fournit zéro —
    pages de pile fraîches, mémoire Windows mise à zéro) : l'EN-TÊTE est
    ZÉRO sur [0x00, 0x60) — handles, verdict/HRESULT, allers, champs D89,
    tailles : la garde d'acquisition de tls-06 (cBuffers @+0x4C) y lit ZÉRO,
    son contrat — et les ZONES (nom/émission/réception) sont en CANARI :
    mémoire indéfinie dont l'image finale doit être prédite OCTET PAR OCTET.
    (Leçon D90 : un cadre tout-canari fait dévier la garde de tls-06 — le
    harnais DOIT honorer la virginité du contrat, pas la contredire.)"""
    return (b"\x00" * L.CADRE_NOM_ZONE +
            CANARI * (TAILLE_CADRE_PAGE - L.CADRE_NOM_ZONE))


class _Echec(Exception):
    """Échec nommé de la session — verdict transporté (Q2)."""

    def __init__(self, verdict: int):
        self.verdict = verdict


class _Fin(Exception):
    """Fin de relais par fermeture système (Q1 : SUCCÈS — tcp-03/tcp-04 ≤ 0)."""


class Modele:
    """La spécification tls-08:R1 en Python — l'orchestration complète, de la
    connexion à la compensation, sur les règles partagées des shims. Le cadre
    arrive VIERGE au sens du contrat P1 (image_vierge : en-tête zéro, zones
    canari) — http-10:R2 fournit des pages fraîches mises à zéro."""

    def __init__(self, script: Script, hote: bytes, requete: bytes, port: int):
        self.script = script
        self.page = bytearray(image_vierge())
        self.appels: list[tuple] = []
        self.hote = hote
        self.requete = requete
        self.port = port
        self.i_gai = self.i_socket = self.i_connect = 0
        self.i_isc = self.i_recv = self.i_send = 0
        self.i_qca = self.i_em = self.i_dm = self.i_dsc = self.i_fch = 0

    # --- primitives cadre ------------------------------------------------------

    def _dw32(self, off: int, v: int) -> None:
        struct.pack_into("<I", self.page, off, v & 0xFFFFFFFF)

    def _w16(self, off: int, v: int) -> None:
        struct.pack_into("<H", self.page, off, v & 0xFFFF)

    def _r16(self, off: int) -> int:
        return struct.unpack_from("<H", self.page, off)[0]

    def _u64(self, off: int) -> int:
        return struct.unpack_from("<Q", self.page, off)[0]

    def _sec(self, off: int, pair: tuple) -> None:
        self.page[off:off + 16] = struct.pack("<QQ", *pair)

    # --- tcp-13 (spec tcp-13:R1 : résolution, socket, connexion, nettoyage) ----

    def _tcp13(self) -> int:
        if not (0 < len(self.hote) <= 255):
            return 0
        h = self.script.hresult_gai(self.i_gai)
        self.appels.append(("GAI", self.hote, (2, 1, 0)))
        self.i_gai += 1
        if h != 0:
            return 0
        s = self.script.ret_socket(self.i_socket)
        self.appels.append(("SOCKET", 2, 1, 6))
        self.i_socket += 1
        if s == -1:
            self.appels.append(("FREEADDRINFO", ADRESSE_ADDRINFO))
            return 0
        sockaddr = (struct.pack("<HH", 2, permuter16(self.port)) +
                    struct.pack("<I", FAKE_ADDR) + b"\x00" * 8)
        c = self.script.hresult_connect(self.i_connect)
        self.appels.append(("CONNECT", s, sockaddr))
        self.i_connect += 1
        if c != 0:
            self.appels.append(("CLOSESOCKET", s))
            self.appels.append(("FREEADDRINFO", ADRESSE_ADDRINFO))
            return 0
        self.appels.append(("FREEADDRINFO", ADRESSE_ADDRINFO))
        return s

    # --- tls-01 (spec tls-01:R1 : refus 1 longueur / refus 2 encodage) ---------

    def _tls01(self) -> int:
        if len(self.hote) > L.HOTE_MAX:
            return 1
        if any(b >= 0x80 for b in self.hote):
            return 2
        utf16 = b"".join(struct.pack("<H", b) for b in self.hote) + b"\x00\x00"
        self.page[L.CADRE_NOM_ZONE:L.CADRE_NOM_ZONE + len(utf16)] = utf16
        self.page[L.CADRE_PTR_NOM:L.CADRE_PTR_NOM + 8] = struct.pack(
            "<Q", ZONE_CADRE + L.CADRE_NOM_ZONE)
        return 0

    # --- tls-05 op 0 (spec tls-05:R1 Q1 : rien d'acquis ne reste à compenser) --

    def _tls05_op0(self) -> int:
        h = self.script.hresult_ach
        self.appels.append(("ACH", 0, L.R_PKG_M4, 2, 0, 0, 0, 0,
                            ZONE_CADRE, 0, L.PKG_M4))
        v = verdict_modele(h)
        if v == 0:
            self._sec(L.CADRE_CRED, MAGIC_CRED)
        else:
            # la bibliothèque barbouille — tls-05 annule (zéro défensif, D82)
            self.page[L.CADRE_CRED:L.CADRE_CRED + 16] = b"\x00" * 16
        return v

    # --- tls-04 (spec tls-04:R1 — boucle ISC bornée 16 allers, miroir D83) -----

    def _emettre(self, cb: int, socket_) -> None:
        """Q3 : émission INTÉGRALE en boucle d'achèvement bornée (E3)."""
        envoye = 0
        while envoye < cb:
            r = self.script.comportement_send(self.i_send, cb - envoye)
            self.appels.append(("SEND", socket_,
                                ZONE_CADRE + L.CADRE_EMISSION + envoye, cb - envoye))
            self.i_send += 1
            if r <= 0:
                raise _Echec(5)
            envoye += r

    def _recevoir(self) -> None:
        """Q3 : UN tcp-03 par tour, accumulation au sommet (E4)."""
        n, donnees = self.script.donnees_recv(self.i_recv, L.MAX_JETON - self.entree)
        self.appels.append(("RECV", SOCKET_SERVEUR,
                            ZONE_RECEPTION + self.entree,
                            L.MAX_JETON - self.entree))
        self.i_recv += 1
        if n <= 0:
            raise _Echec(5)
        base = L.CADRE_RECEPTION + self.entree
        self.page[base:base + n] = donnees
        self.entree += n

    def _tls04(self) -> int:
        self.entree = 0
        self.allers = 0
        verdict_final = None
        try:
            while True:
                if self.allers >= 16:             # I1/E5 : bornée, TOUJOURS finie
                    raise _Echec(5)
                self.allers += 1
                h, lt = self.script.comportement_isc(self.i_isc)
                verdict = verdict_modele(h)
                self.appels.append((
                    "ISC", ZONE_CADRE,
                    0 if self.entree == 0 else ZONE_CADRE + L.CADRE_CTXT,
                    ZONE_CADRE + L.CADRE_NOM_ZONE, L.ISC_REQUETES, 0, 0,
                    0 if self.entree == 0 else "PILE",
                    0, ZONE_CADRE + L.CADRE_CTXT, "PILE", "PILE",
                    None if self.entree == 0 else
                    (0, 1, "+0x10", self.entree, 2, ZONE_RECEPTION),
                    (0, 1, "+0x10", L.MAX_JETON, 2, ZONE_CADRE + L.CADRE_EMISSION)))
                self.i_isc += 1
                self._dw32(L.CADRE_HRESULT, h)    # Q2 : HRESULT d'origine à CHAQUE retour
                if verdict == 0:
                    self._sec(L.CADRE_CTXT, MAGIC_FINAL)
                elif verdict == 1:
                    self._sec(L.CADRE_CTXT, MAGIC_PARTIAL)
                elif verdict >= 3:
                    self._sec(L.CADRE_CTXT, MAGIC_ORDURE)
                cb = L.MAX_JETON
                if verdict in (0, 1):
                    cb = lt
                    if lt > 0:
                        self.page[L.CADRE_EMISSION:L.CADRE_EMISSION + lt] = \
                            motif(self.i_isc - 1, lt)
                if verdict == 0:
                    if cb > 0:
                        self._emettre(cb, SOCKET_SERVEUR)
                    self._dw32(L.CADRE_VERDICT, 0)
                    verdict_final = 0
                    break
                if verdict == 1:
                    self.entree = 0               # entrée consommée (accumulation FRAÎCHE)
                    if cb > 0:
                        self._emettre(cb, SOCKET_SERVEUR)
                    self._recevoir()
                elif verdict == 2:
                    if self.entree >= L.MAX_JETON:   # E2 : jeton hors borne
                        raise _Echec(5)
                    self._recevoir()
                else:                              # Q2/E1 : échec nommé
                    verdict_final = verdict
                    self._dw32(L.CADRE_VERDICT, verdict)
                    break
        except _Echec as e:
            verdict_final = e.verdict
            self._dw32(L.CADRE_VERDICT, e.verdict)
        self._w16(L.CADRE_ALLERS, self.allers)
        return verdict_final

    # --- console tcp-11 (état nommé : ECS → WF → LCS, la ligne EXACTE) ---------

    def _console(self, ligne: bytes) -> None:
        self.appels.append(("ECS", L.R_CS))
        self.appels.append(("WF", FAKE_STDOUT, ligne))
        self.appels.append(("LCS", L.R_CS))

    # --- tls-06 (spec tls-06:R1 — découpe au négocié, miroir D88) --------------

    def _tls06(self) -> int:
        span, ln = self.requete, len(self.requete)
        if struct.unpack_from("<I", self.page, L.CADRE_TAILLES + 12)[0] == 0:
            h, tailles = self.script.comportement_qca(self.i_qca)
            self.appels.append(("QCA", ZONE_CADRE + L.CADRE_CTXT, 4,
                                ZONE_CADRE + L.CADRE_TAILLES))
            self.i_qca += 1
            v = verdict_modele(h)
            self._dw32(L.CADRE_HRESULT, h)
            if v != 0:
                self.page[L.CADRE_TAILLES:L.CADRE_TAILLES + 20] = b"\x00" * 20
                self._dw32(L.CADRE_VERDICT, v)
                return v
            struct.pack_into("<5I", self.page, L.CADRE_TAILLES, *tailles)
        cbh, cbt, maxmsg = struct.unpack_from("<3I", self.page, L.CADRE_TAILLES)
        pos, restant = 0, ln
        while True:
            m = restant if restant <= maxmsg else maxmsg
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
                n = cbh + m + cbt
                self.page[L.CADRE_EMISSION:L.CADRE_EMISSION + n] = b"\x00" * n
                self._dw32(L.CADRE_VERDICT, v)
                return v
            self.page[L.CADRE_EMISSION:L.CADRE_EMISSION + cbh] = entete_em(i_em, cbh)
            self.page[L.CADRE_EMISSION + cbh:L.CADRE_EMISSION + cbh + m] = \
                chiffrer(i_em, bytes(span[pos:pos + m]))
            self.page[L.CADRE_EMISSION + cbh + m:L.CADRE_EMISSION + cbh + m + cbt] = \
                queue_em(i_em, cbt)
            total = cbh + m + cbt
            envoye = 0
            while envoye < total:
                r = self.script.comportement_send(self.i_send, total - envoye)
                self.appels.append(("SEND", SOCKET_SERVEUR,
                                    ZONE_CADRE + L.CADRE_EMISSION + envoye,
                                    total - envoye))
                self.i_send += 1
                if r <= 0:
                    self._dw32(L.CADRE_VERDICT, 5)
                    return 5
                envoye += r
            pos += m
            restant -= m
            if restant == 0:
                break
        self._dw32(L.CADRE_VERDICT, 0)
        return 0

    # --- tls-07 (spec tls-07:R1 + règles D89 — miroir du harnais D89) ----------

    def _tls07(self, lot: int) -> tuple[int, int, int]:
        """UN appel tls-07 → (verdict, ptr span, longueur span)."""
        off0 = self._r16(L.CADRE_OFFSET)
        if off0 + lot > L.CAPACITE_RECEPTION:    # E2 : la garde SOMME (D89)
            self._dw32(L.CADRE_VERDICT, 5)
            return 5, 0, 0
        if off0:
            z = L.CADRE_RECEPTION
            self.page[z:z + lot] = self.page[z + off0:z + off0 + lot]
            self._w16(L.CADRE_OFFSET, 0)
        desc_att = [(lot, L.SECBUFFER_DATA, ZONE_RECEPTION),
                    (0, L.SECBUFFER_EMPTY, 0),
                    (0, L.SECBUFFER_EMPTY, 0),
                    (0, L.SECBUFFER_EMPTY, 0)]
        h, cbh, ln_c, cbt = self.script.comportement_dm(self.i_dm)
        v = verdict_modele(h)
        self.appels.append(("DM", ZONE_CADRE + L.CADRE_CTXT, "PILE", 0, "PILE",
                            (0, 4, "PBUF", desc_att), 0))
        self.i_dm += 1
        self._dw32(L.CADRE_HRESULT, h)
        c = cbh + ln_c + cbt
        r = lot - c if lot > c else 0
        if v in (0, 4):
            z = L.CADRE_RECEPTION
            self.page[z + cbh:z + cbh + ln_c] = clair_dm(self.i_dm - 1, ln_c)
        if v == 0:
            self._dw32(L.CADRE_VERDICT, 0)
            self._w16(L.CADRE_UTILE, r)
            self._w16(L.CADRE_OFFSET, lot - r)
            return 0, ZONE_RECEPTION + cbh, ln_c
        if v == 2:
            self._dw32(L.CADRE_VERDICT, 2)
            self._w16(L.CADRE_UTILE, lot)
            self._w16(L.CADRE_OFFSET, 0)
            return 2, 0, 0
        if v == 4:
            self._dw32(L.CADRE_VERDICT, 4)
            self._w16(L.CADRE_UTILE, r)     # curiosité « fin propre avec résidu »
            self._w16(L.CADRE_OFFSET, 0)    # purgée : plus rien de vivant
            return 4, 0, 0
        self._dw32(L.CADRE_VERDICT, v)
        self._w16(L.CADRE_UTILE, lot)
        self._w16(L.CADRE_OFFSET, 0)
        return v, 0, 0

    # --- le pompage (tcp-04 vers le CLIENT, boucle d'achèvement, span vide) ----

    def _pomper(self, span_ptr: int, span_len: int) -> None:
        if span_len == 0:
            return                             # span VIDE : jamAIS tcp-04 à 0 (P3)
        envoye = 0
        while envoye < span_len:
            r = self.script.comportement_send(self.i_send, span_len - envoye)
            self.appels.append(("SEND", SOCKET_CLIENT, span_ptr + envoye,
                                span_len - envoye))
            self.i_send += 1
            if r <= 0:
                raise _Fin()                   # le client est parti — Q1 fin de relais
            envoye += r

    # --- la boucle de relais (Q1 : recevoir, déchiffrer, pomper, DRAINER) ------

    def _relais(self) -> None:
        self._w16(L.CADRE_UTILE, 0)            # géométrie D89 née vierge (étape 7)
        self._w16(L.CADRE_OFFSET, 0)
        while True:                            # .relais
            utile = self._r16(L.CADRE_UTILE)
            if utile == 0:
                self._w16(L.CADRE_OFFSET, 0)   # région VIDE : la zone morte est
                position = 0                   # morte — reprise en tête (D90)
            else:
                position = self._r16(L.CADRE_OFFSET) + utile
                if position >= L.CAPACITE_RECEPTION:
                    raise _Echec(5)            # chambre NULLE avec résidu vivant
            chambre = L.CAPACITE_RECEPTION - position
            n, donnees = self.script.donnees_recv(self.i_recv, chambre)
            self.appels.append(("RECV", SOCKET_SERVEUR,
                                ZONE_RECEPTION + position, chambre))
            self.i_recv += 1
            if n <= 0:
                raise _Fin()                   # fermeture système — Q1 fin de relais
            base = L.CADRE_RECEPTION + position
            self.page[base:base + n] = donnees
            self._w16(L.CADRE_UTILE, utile + n)
            while True:                        # .decrypter (+ drain)
                v, span_ptr, span_len = self._tls07(self._r16(L.CADRE_UTILE))
                if v == 0:
                    self._pomper(span_ptr, span_len)
                    if self._r16(L.CADRE_UTILE) > 0:
                        continue               # DRAIN : record déchiffrable en zone
                    break                      # → .relais (réceptionner)
                if v == 4:
                    raise _Fin()               # fin de contexte — Q1
                if v == 2:
                    break                      # incomplet → .relais (réceptionner)
                raise _Echec(v)                # E3 : réponse tronquée propre

    # --- compensation INTÉGRALE (Q3 — l'ordre EST le contrat) -------------------

    def _liberer(self, champ: int, api: str, hresult: str, indice: str) -> None:
        """Une libération tls-05 + E4 : verdict testé, UNE ressaisie, continue."""
        i = getattr(self, indice)
        h = getattr(self.script, hresult)(i)
        setattr(self, indice, i + 1)
        self.appels.append((api, ZONE_CADRE + champ))
        if verdict_modele(h) == 0:
            self.page[champ:champ + 16] = b"\x00" * 16
            return
        i = getattr(self, indice)
        h = getattr(self.script, hresult)(i)
        setattr(self, indice, i + 1)
        self.appels.append((api, ZONE_CADRE + champ))
        if verdict_modele(h) == 0:
            self.page[champ:champ + 16] = b"\x00" * 16

    def _compensation(self) -> None:
        if self._u64(L.CADRE_CTXT) != 0:       # contexte ÉCRIT (le test : dwLower)
            self._liberer(L.CADRE_CTXT, "DSC", "hresult_dsc", "i_dsc")
        if self._u64(L.CADRE_CRED) != 0:       # credentials ACQUIS
            self._liberer(L.CADRE_CRED, "FCH", "hresult_fch", "i_fch")
        if self._u64(L.CADRE_SOCKET) != 0:     # socket serveur OUVERTE (I1)
            self.appels.append(("CLOSESOCKET", SOCKET_SERVEUR))

    # --- l'orchestration complète (l'ORDRE de Q1 est le contrat) ---------------

    def executer(self) -> tuple[int, list, bytes]:
        verdict_session: int | None = None
        try:
            # prologue : champs de compensation à zéro (défense, précédent D83)
            self.page[L.CADRE_CRED:L.CADRE_CRED + 16] = b"\x00" * 16
            self.page[L.CADRE_CTXT:L.CADRE_CTXT + 16] = b"\x00" * 16
            self.page[L.CADRE_SOCKET:L.CADRE_SOCKET + 8] = b"\x00" * 8
            # 1. connexion
            sock = self._tcp13()
            if sock == 0:
                raise _Echec(L.VERDICT_CIBLE)  # E1 : « cible injoignable »
            self.page[L.CADRE_SOCKET:L.CADRE_SOCKET + 8] = struct.pack("<Q", sock)
            # 2. nom UTF-16
            if self._tls01() != 0:
                raise _Echec(L.VERDICT_CIBLE)  # la cible ne peut être nommée
            # 3. credentials (validation AUTOMATIQUE)
            v = self._tls05_op0()
            if v != 0:
                raise _Echec(v)
            # 4. la poignée — le verdict 3 CONSOLE d'abord (I4 : LE critère M4)
            v = self._tls04()
            if v == 3:
                self._console(L.TXT_TLS_CERT)
                raise _Echec(3)
            if v != 0:
                raise _Echec(v)
            # 5. état nommé : le tunnel existe
            self._console(L.TXT_TLS_ETABLI)
            # 6. requête chiffrée
            v = self._tls06()
            if v != 0:
                raise _Echec(v)
            # 7-8. le relais
            self._relais()
            verdict_session = 0
        except _Fin:
            verdict_session = 0                # fermeture système / fin de contexte
        except _Echec as e:
            verdict_session = e.verdict
        # Q3 : TOUT chemin compensé, dans l'ordre, exactement une fois chacun
        self._compensation()
        return verdict_session, self.appels, bytes(self.page)


# --- Émulateur à shims (page ret + crochet code, mécanisme M2/M3) -----------------

def _pile_valide(p: int) -> bool:
    return ZONE_PILE <= p < ZONE_PILE + TAILLE_PILE


class Emulateur:
    """Un chargement = un émulateur NEUF (leçon D79). Toute la chaîne réelle
    de tls-08 vit à ses RVA : .text (hello-02, libc), .text2 (tcp), .text3
    (tls). Le cadre VIERGE arrive en canari (la défense de tls-08 est ainsi
    éprouvée) ; le paquet, l'état .data et l'addrinfo factice sont posés à
    chaque scénario ; la pile n'est jamAIS réinitialisée entre deux appels."""

    def __init__(self, blobs: dict):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        uc.mem_map(ZONE_TEXTE, TAILLE_TEXTE)
        uc.mem_map(ZONE_RDATA, TAILLE_RDATA)
        uc.mem_map(ZONE_TCP, TAILLE_TCP)
        uc.mem_map(ZONE_CODE, TAILLE_CODE)
        uc.mem_map(ZONE_DATA, TAILLE_DATA)
        uc.mem_map(TRAMPOLINE, TAILLE_TRAMP)
        uc.mem_map(ZONE_CADRE, TAILLE_CADRE_PAGE)
        uc.mem_map(ZONE_PAQUET, TAILLE_PAQUET)
        uc.mem_map(ZONE_ADDRINFO, TAILLE_ADDRINFO)
        uc.mem_map(ZONE_PILE, TAILLE_PILE)

        # .text : hello-02 + libc-01/03/04/07 (octets scellés M0/M1, R7)
        page_texte = b"\xCC" * TAILLE_TEXTE
        for rva, cle in ((RVA_HELLO02, "hello-02"), (RVA_MEMCPY, "libc-01"),
                         (RVA_STRLEN, "libc-03"), (RVA_ITOA, "libc-04"),
                         (RVA_MEMSET, "libc-07")):
            blob = blobs[cle]
            page_texte = (page_texte[:rva - ZONE_TEXTE] + blob +
                          page_texte[rva - ZONE_TEXTE + len(blob):])
        uc.mem_write(ZONE_TEXTE, page_texte)
        # .text2 : tcp-03/04/05, tcp-13, tcp-11 (octets scellés M2/M3, R7)
        page_tcp = b"\xCC" * TAILLE_TCP
        for rva, cle in ((RVA_TCP03, "tcp-03"), (RVA_TCP04, "tcp-04"),
                         (RVA_TCP05, "tcp-05"), (RVA_TCP13, "tcp-13"),
                         (RVA_TCP11, "tcp-11")):
            blob = blobs[cle]
            page_tcp = (page_tcp[:rva - ZONE_TCP] + blob +
                        page_tcp[rva - ZONE_TCP + len(blob):])
        uc.mem_write(ZONE_TCP, page_tcp)
        # .text3 : tls-01..08 (le bloc sous test + sa chaîne M4)
        page_tls = b"\xCC" * TAILLE_CODE
        for rva, cle in ((RVA_TLS01, "tls-01"), (RVA_TLS02, "tls-02"),
                         (RVA_TLS03, "tls-03"), (RVA_TLS04, "tls-04"),
                         (RVA_TLS05, "tls-05"), (RVA_TLS06, "tls-06"),
                         (RVA_TLS07, "tls-07"), (RVA_TLS08, "tls-08")):
            blob = blobs[cle]
            page_tls = (page_tls[:rva - ZONE_CODE] + blob +
                        page_tls[rva - ZONE_CODE + len(blob):])
        uc.mem_write(ZONE_CODE, page_tls)
        uc.mem_write(TRAMPOLINE, b"\xc3" * TAILLE_TRAMP)   # chaque shim retourne
        # résolution chargeur : IAT kernel32/ws2_32 + secur32 → fausses adresses
        for nom, rva in L.IAT_SLOTS.items():
            uc.mem_write(rva, struct.pack("<Q", FAUX[nom]))
        for nom, rva in L.IAT_SEC32_SLOTS.items():
            uc.mem_write(rva, struct.pack("<Q", FAUX[nom]))
        # fixtures .rdata M4 — doivent rester intactes (propriétaires uniques)
        uc.mem_write(L.R_PKG_M4, L.PKG_M4)
        uc.mem_write(L.R_TXT_TLS_ETABLI, L.TXT_TLS_ETABLI)
        uc.mem_write(L.R_TXT_TLS_CERT, L.TXT_TLS_CERT)
        # addrinfo factice (AF_INET, première entrée — tcp-13 la parcourt)
        ai = struct.pack("<iiiiQQQQ", 0, 2, 1, 0, 16, 0, ADRESSE_SOCKADDR, 0)
        uc.mem_write(ADRESSE_ADDRINFO, ai)
        uc.mem_write(ADRESSE_SOCKADDR,
                     struct.pack("<HH", 2, 0x1234) + struct.pack("<I", FAKE_ADDR))
        uc.hook_add(UC_HOOK_CODE, self._shim, begin=TRAMPOLINE, end=TRAMPOLINE + TAILLE_TRAMP)
        self.script: Script | None = None
        self.appels: list[tuple] = []
        self.faux_pas: list[str] = []
        self._i_gai = self._i_socket = self._i_connect = 0
        self._i_isc = self._i_recv = self._i_send = 0
        self._i_qca = self._i_em = self._i_dm = self._i_dsc = self._i_fch = 0

    def _shim(self, uc: Uc, adresse: int, taille: int, donnees):
        nom = FAUX_REV.get(adresse)
        if nom is None:
            self.faux_pas.append(f"shim inconnu @{adresse:#x}")
            return
        methode = getattr(self, "_api_" + nom, None)
        if methode is None:
            self.faux_pas.append(f"{nom} appelé par la chaîne tls-08 (faux pas nommé)")
            return
        methode()

    def _pile(self, offset: int) -> int:
        """Argument pile de l'appelant, vu du shim ([rsp+0x28] = arg5 msx64)."""
        rsp = self.uc.reg_read(REGS["rsp"])
        return struct.unpack("<Q", bytes(self.uc.mem_read(rsp + offset, 8)))[0]

    def _lire_desc_isc(self, p: int):
        """SecBufferDesc + premier SecBuffer (tls-03 type 0 : 32 octets)."""
        if not p:
            return None
        b = bytes(self.uc.mem_read(p, 32))
        ulv, nb = struct.unpack_from("<II", b, 0)
        (pb,) = struct.unpack_from("<Q", b, 8)
        cb, typ = struct.unpack_from("<II", b, 16)
        (pv,) = struct.unpack_from("<Q", b, 24)
        return (ulv, nb, pb, cb, typ, pv)

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

    def _lire_desc_dm(self, p: int):
        """SecBufferDesc à 4 tampons (DATA/EMPTY/EMPTY/EMPTY) — None si invalide."""
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

    # --- ws2_32 : la connexion, le flux, la fermeture ---------------------------

    def _api_getaddrinfo(self):
        uc = self.uc
        node = uc.reg_read(REGS["rcx"])
        hints = uc.reg_read(REGS["r8"])
        res_out = uc.reg_read(REGS["r9"])
        chaine = b""
        if node:
            brut = bytes(uc.mem_read(node, 256))
            chaine = brut[:brut.index(b"\x00")] if b"\x00" in brut else brut
        af, st, pr = 0, 0, 0
        if hints:
            valeurs = struct.unpack_from("<iiii", bytes(uc.mem_read(hints, 16)))
            af, st, pr = valeurs[1], valeurs[2], valeurs[3]   # flags, family, type, proto
        self.appels.append(("GAI", chaine, (af, st, pr)))
        h = self.script.hresult_gai(self._i_gai)
        self._i_gai += 1
        if h == 0:
            uc.mem_write(res_out, struct.pack("<Q", ADRESSE_ADDRINFO))
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

    def _api_freeaddrinfo(self):
        self.appels.append(("FREEADDRINFO", self.uc.reg_read(REGS["rcx"])))

    def _api_socket(self):
        uc = self.uc
        af = uc.reg_read(REGS["rcx"]) & 0xFFFFFFFF
        st = uc.reg_read(REGS["rdx"]) & 0xFFFFFFFF
        pr = uc.reg_read(REGS["r8"]) & 0xFFFFFFFF
        self.appels.append(("SOCKET", af, st, pr))
        s = self.script.ret_socket(self._i_socket)
        self._i_socket += 1
        uc.reg_write(REGS["rax"], s & 0xFFFFFFFFFFFFFFFF)

    def _api_connect(self):
        uc = self.uc
        sock = uc.reg_read(REGS["rcx"])
        sa = uc.reg_read(REGS["rdx"])
        ln = uc.reg_read(REGS["r8"]) & 0xFFFFFFFF
        brut = bytes(uc.mem_read(sa, ln)) if 0 < ln <= 16 else b""
        self.appels.append(("CONNECT", sock, brut))
        c = self.script.hresult_connect(self._i_connect)
        self._i_connect += 1
        uc.reg_write(REGS["rax"], c & 0xFFFFFFFF)

    def _api_closesocket(self):
        self.appels.append(("CLOSESOCKET", self.uc.reg_read(REGS["rcx"])))
        self.uc.reg_write(REGS["rax"], 0)

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

    # --- kernel32 : la console (tcp-11 → hello-02 → WriteFile) ------------------

    def _api_EnterCriticalSection(self):
        self.appels.append(("ECS", self.uc.reg_read(REGS["rcx"])))

    def _api_LeaveCriticalSection(self):
        self.appels.append(("LCS", self.uc.reg_read(REGS["rcx"])))

    def _api_WriteFile(self):
        uc = self.uc
        handle = uc.reg_read(REGS["rcx"])
        buf = uc.reg_read(REGS["rdx"])
        ln = uc.reg_read(REGS["r8"]) & 0xFFFFFFFF
        ligne = bytes(uc.mem_read(buf, ln)) if ln else b""
        self.appels.append(("WF", handle, ligne))
        uc.reg_write(REGS["rax"], 1)

    # --- secur32 : les SEPT entrées (tls-04..07 via tls-05) ---------------------

    def _api_AcquireCredentialsHandleW(self):
        uc = self.uc
        principal = uc.reg_read(REGS["rcx"])
        pkg = uc.reg_read(REGS["rdx"])
        usage = uc.reg_read(REGS["r8"]) & 0xFFFFFFFF
        logonid = uc.reg_read(REGS["r9"])
        authdata = self._pile(0x28)
        getkey = self._pile(0x30)
        getkeyarg = self._pile(0x38)
        phcred = self._pile(0x40)
        expiry = self._pile(0x48)
        pkg_lu = bytes(uc.mem_read(pkg, len(L.PKG_M4))) if pkg else b""
        self.appels.append(("ACH", principal, pkg, usage, logonid, authdata,
                            getkey, getkeyarg, phcred, expiry, pkg_lu))
        h = self.script.hresult_ach
        if verdict_modele(h) == 0:
            uc.mem_write(phcred, struct.pack("<QQ", *MAGIC_CRED))
        else:
            # la bibliothèque barbouille en échec — tls-05 annulera (D82)
            uc.mem_write(phcred, struct.pack("<QQ", *MAGIC_ORDURE))
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

    def _api_FreeCredentialsHandle(self):
        uc = self.uc
        ph = uc.reg_read(REGS["rcx"])
        self.appels.append(("FCH", ph))
        handle = bytes(uc.mem_read(ph, 16)) if ph else b"\x00" * 16
        if handle == b"\x00" * 16:
            uc.reg_write(REGS["rax"], INVALID_HANDLE)   # handle nul : refus réel
            return
        h = self.script.hresult_fch(self._i_fch)
        self._i_fch += 1
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

    def _api_DeleteSecurityContext(self):
        uc = self.uc
        ph = uc.reg_read(REGS["rcx"])
        self.appels.append(("DSC", ph))
        handle = bytes(uc.mem_read(ph, 16)) if ph else b"\x00" * 16
        if handle == b"\x00" * 16:
            uc.reg_write(REGS["rax"], INVALID_HANDLE)   # handle nul : refus réel
            return
        h = self.script.hresult_dsc(self._i_dsc)
        self._i_dsc += 1
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

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
        desc_in = self._lire_desc_isc(p_input)
        desc_out = self._lire_desc_isc(p_output)
        self.appels.append(("ISC", ph_cred, ph_ctxt, cible, requetes, reserved1,
                            datarep, p_input, reserved2, ph_new, p_output, pf_attr,
                            desc_in, desc_out))
        h, lt = self.script.comportement_isc(self._i_isc)
        self._i_isc += 1
        verdict = verdict_modele(h)
        if verdict in (0, 1) and desc_out is not None:
            # une vraie ISC consigne TOUJOURS cbBuffer à la longueur produite
            # (0 = aucun jeton) sur succès/continuation — jamais la capacité
            if lt > 0:
                uc.mem_write(desc_out[5], motif(self._i_isc - 1, lt))
            uc.mem_write(p_output + 0x10, struct.pack("<I", lt))
        if verdict == 0:
            uc.mem_write(ph_new, struct.pack("<QQ", *MAGIC_FINAL))
        elif verdict == 1:
            uc.mem_write(ph_new, struct.pack("<QQ", *MAGIC_PARTIAL))
        elif verdict >= 3:
            uc.mem_write(ph_new, struct.pack("<QQ", *MAGIC_ORDURE))
        if pf_attr:
            uc.mem_write(pf_attr, struct.pack("<I", 0x141))
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

    def _api_QueryContextAttributesW(self):
        uc = self.uc
        ph_ctxt = uc.reg_read(REGS["rcx"])
        attr = uc.reg_read(REGS["rdx"]) & 0xFFFFFFFF
        pbuf = uc.reg_read(REGS["r8"])
        self.appels.append(("QCA", ph_ctxt, attr, pbuf))
        h, tailles = self.script.comportement_qca(self._i_qca)
        self._i_qca += 1
        if verdict_modele(h) == 0:
            uc.mem_write(pbuf, struct.pack("<5I", *tailles))
        else:
            uc.mem_write(pbuf, struct.pack("<5I", 0xDEADBEEF, 0xCAFEBABE,
                                            0xFEEDFACE, 0xBAADF00D, 0x1DEA))
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

    def _api_EncryptMessage(self):
        uc = self.uc
        ph_ctxt = uc.reg_read(REGS["rcx"])
        fqop = uc.reg_read(REGS["rdx"]) & 0xFFFFFFFF
        p_msg = uc.reg_read(REGS["r8"])
        seq = uc.reg_read(REGS["r9"]) & 0xFFFFFFFF
        desc = self._lire_desc_em(p_msg)
        self.appels.append(("EM", ph_ctxt, fqop, p_msg, seq, desc))
        if desc is None:
            uc.reg_write(REGS["rax"], INVALID_TOKEN)
            return
        i = self._i_em
        h = self.script.hresult_em(i)
        if verdict_modele(h) == 0:
            _ulv, _nb, pb, bufs = desc
            (cbh, _th, ph) = bufs[0]
            (cm, _td, pm) = bufs[1]
            (cbt, _tq, pq) = bufs[2]
            clair = bytes(uc.mem_read(pm, cm))
            uc.mem_write(ph, entete_em(i, cbh))
            uc.mem_write(pm, chiffrer(i, clair))
            uc.mem_write(pq, queue_em(i, cbt))
            uc.mem_write(pb + 0x00, struct.pack("<I", cbh))
            uc.mem_write(pb + 0x10, struct.pack("<I", cm))
            uc.mem_write(pb + 0x20, struct.pack("<I", cbt))
        self._i_em += 1
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

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
            uc.reg_write(REGS["rax"], INVALID_TOKEN)
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
            uc.mem_write(pv0 + cbh, clair_dm(i, ln_c))
            uc.mem_write(pb + 0x00, struct.pack("<I", ln_c))
            uc.mem_write(pb + 0x04, struct.pack("<I", L.SECBUFFER_DATA))
            uc.mem_write(pb + 0x08, struct.pack("<Q", pv0 + cbh))
            uc.mem_write(pb + 0x10, struct.pack("<I", r))
            uc.mem_write(pb + 0x14, struct.pack("<I", L.SECBUFFER_EXTRA))
            uc.mem_write(pb + 0x18, struct.pack("<Q", pv0 + c))
        elif v == 2:
            manquant = c - lot if c > lot else 0
            pb = desc[2]
            uc.mem_write(pb + 0x00, struct.pack("<I", manquant))
            uc.mem_write(pb + 0x04, struct.pack("<I", L.SECBUFFER_MISSING))
        self._i_dm += 1
        if v == 0 and _pile_valide(pfqop):
            uc.mem_write(pfqop, struct.pack("<I", 2))   # QOP non nul — falsifiable
        uc.reg_write(REGS["rax"], h & 0xFFFFFFFF)

    # --- pilotage ----------------------------------------------------------------

    def preparer(self, hote: bytes, requete: bytes, port: int) -> None:
        """UNE fois par scénario : cadre VIERGE réaliste (en-tête zéro, zones
        canari — image_vierge, leçon D90), paquet + hôte + requête, état
        .data, indices de script remis à zéro."""
        uc = self.uc
        uc.mem_write(ZONE_CADRE, image_vierge())
        page = bytearray(CANARI * TAILLE_PAQUET)
        struct.pack_into("<Q", page, L.PAQUET_HOTE_PTR, PAQUET_HOTE)
        struct.pack_into("<Q", page, L.PAQUET_HOTE_LEN, len(hote))
        struct.pack_into("<H", page, L.PAQUET_PORT, port)
        struct.pack_into("<Q", page, L.PAQUET_REQUETE_PTR, PAQUET_REQUETE)
        struct.pack_into("<Q", page, L.PAQUET_REQUETE_LEN, len(requete))
        struct.pack_into("<Q", page, L.PAQUET_SOCKET_CLIENT, SOCKET_CLIENT)
        page[0x100:0x100 + len(hote)] = hote
        page[0x200:0x200 + len(requete)] = requete
        uc.mem_write(ZONE_PAQUET, bytes(page))
        uc.mem_write(L.R_STDOUT, struct.pack("<Q", FAKE_STDOUT))
        uc.mem_write(L.R_CS, b"\x00" * 40)
        self.appels = []
        self.faux_pas = []
        self._i_gai = self._i_socket = self._i_connect = 0
        self._i_isc = self._i_recv = self._i_send = 0
        self._i_qca = self._i_em = self._i_dm = self._i_dsc = self._i_fch = 0

    def appeler(self, script: Script) -> int:
        uc = self.uc
        self.script = script
        self.appels = []
        self.faux_pas = []
        for nom, valeur in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], valeur)
        uc.reg_write(REGS["rsp"], RSP)
        uc.mem_write(RSP, struct.pack("<Q", RET_MAGIQUE))
        uc.reg_write(REGS["rcx"], ZONE_CADRE)
        uc.reg_write(REGS["rdx"], ZONE_PAQUET)
        uc.emu_start(RVA_TLS08, RET_MAGIQUE, timeout=10_000_000, count=3_000_000)
        return uc.reg_read(REGS["rax"]) & 0xFFFFFFFF

    def hygiene(self) -> list[str]:
        problemes = list(self.faux_pas)
        for nom, valeur in SENTINELLES_NV.items():
            if self.uc.reg_read(REGS[nom]) != valeur:
                problemes.append(f"non-volatil {nom} modifié (I5)")
        for nom, rva in {**L.IAT_SLOTS, **L.IAT_SEC32_SLOTS}.items():
            if struct.unpack("<Q", bytes(self.uc.mem_read(rva, 8)))[0] != FAUX[nom]:
                problemes.append(f"IAT {nom} réécrite")
        for rva, attendu, nomf in ((L.R_PKG_M4, L.PKG_M4, "fixture package"),
                                   (L.R_TXT_TLS_ETABLI, L.TXT_TLS_ETABLI,
                                    "fixture « tunnel chiffre etabli »"),
                                   (L.R_TXT_TLS_CERT, L.TXT_TLS_CERT,
                                    "fixture « certificat rejete »")):
            if bytes(self.uc.mem_read(rva, len(attendu))) != attendu:
                problemes.append(f"{nomf} altérée")
        if struct.unpack("<Q", bytes(self.uc.mem_read(L.R_STDOUT, 8)))[0] != FAKE_STDOUT:
            problemes.append("état .data stdout altéré")
        if bytes(self.uc.mem_read(L.R_CS, 40)) != b"\x00" * 40:
            problemes.append("section critique .data altérée")
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
        nom = a[0]
        if nom in ("RECV", "SEND"):
            for idx, nomch in ((1, "socket"), (2, "pointeur"), (3, "longueur")):
                if a[idx] != e[idx]:
                    problemes.append(f"{nom} #{k} {nomch} {a[idx]!r} != {e[idx]!r}")
            continue
        if nom in ("GAI", "SOCKET", "FREEADDRINFO", "CLOSESOCKET", "ECS", "LCS",
                    "DSC", "FCH", "WF", "QCA", "ACH", "CONNECT"):
            if nom == "ACH":
                # (nom, principal, pkg, usage, logonid, authdata, getkey,
                #  getkeyarg, phcred, expiry, pkg_lu) — 11 champs
                for idx, nomch in ((1, "pszPrincipal"), (2, "pszPackage"),
                                   (3, "fCredentialUse"), (4, "pvLogonId"),
                                   (5, "pAuthData"), (6, "pGetKeyFn"),
                                   (7, "pvGetKeyFn"), (8, "phCredential"),
                                   (9, "ptsExpiry")):
                    if a[idx] != e[idx]:
                        problemes.append(f"ACH #{k} {nomch} {a[idx]!r} != {e[idx]!r}")
                if a[10] != e[10]:
                    problemes.append("ACH #%d : fixture package lue != attendue" % k)
                continue
            if nom == "QCA":
                if a[1] != e[1] or a[2] != e[2] or a[3] != e[3]:
                    problemes.append(f"QCA #{k} {a[1:]} != {e[1:]}")
                continue
            if a[1:] != e[1:]:
                if nom == "CONNECT":
                    problemes.append(f"CONNECT #{k} sockaddr {a[2]!r} != {e[2]!r}"
                                     if a[1] == e[1] else
                                     f"CONNECT #{k} socket {a[1]:#x} != {e[1]:#x}")
                elif nom == "WF":
                    problemes.append(f"WF #{k} ligne {a[2]!r} != {e[2]!r}"
                                     if a[1] == e[1] else
                                     f"WF #{k} handle {a[1]:#x} != {e[1]:#x}")
                elif nom == "GAI":
                    problemes.append(f"GAI #{k} {a[1:]} != {e[1:]} "
                                     "(node ou hints)")
                else:
                    problemes.append(f"{nom} #{k} {a[1:]} != {e[1:]}")
            continue
        if nom == "ISC":
            # (nom, ph_cred, ph_ctxt, cible, requetes, r1, datarep, p_in, r2,
            #  ph_new, p_out, pf_attr, desc_in, desc_out)
            exacts = [(1, "phCredential"), (2, "phContext"), (3, "pszTargetName"),
                      (4, "fContextReq"), (5, "Reserved1"), (6, "TargetDataRep"),
                      (8, "Reserved2"), (9, "phNewContext")]
            for idx, nomch in exacts:
                if a[idx] != e[idx]:
                    problemes.append(f"ISC #{k} {nomch} {a[idx]!r} != {e[idx]!r}")
            for idx, nomch in ((7, "pInput"), (10, "pOutput"), (11, "pfContextAttr")):
                if e[idx] == 0:
                    if a[idx] != 0:
                        problemes.append(f"ISC #{k} {nomch} {a[idx]:#x} != NULL (Q4)")
                elif not _pile_valide(a[idx]) or a[idx] % 8:
                    problemes.append(f"ISC #{k} {nomch} {a[idx]:#x} hors pile/aligné")
            for idx, nomch, p_idx in ((12, "descripteur entrée", 7),
                                      (13, "descripteur sortie", 10)):
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
                    problemes.append(f"ISC #{k} {nomch} pBuffers != pMessage+0x10")
                if pv != epv:
                    problemes.append(f"ISC #{k} {nomch} pv {pv:#x} != {epv:#x}")
            continue
        if nom == "EM":
            # (nom, ph_ctxt, fqop, p_msg, seq, desc)
            for idx, nomch in ((1, "phContext"), (2, "fQOP"), (4, "MessageSeqNo")):
                if a[idx] != e[idx]:
                    problemes.append(f"EM #{k} {nomch} {a[idx]!r} != {e[idx]!r}")
            if not _pile_valide(a[3]) or a[3] % 8:
                problemes.append(f"EM #{k} pMessage {a[3]:#x} hors pile/aligné")
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
                problemes.append(f"EM #{k} pBuffers != pMessage+0x10")
            for j, (ba, be) in enumerate(zip(bufs, e[5])):
                if ba != be:
                    problemes.append(f"EM #{k} tampon {j} {ba} != {be}")
            continue
        if nom == "DM":
            # (nom, ph_ctxt, p_msg, seq, pfqop, desc, qop_pre)
            for idx, nomch in ((1, "phContext"), (3, "MessageSeqNo"), (6, "pfQOP pré")):
                if a[idx] != e[idx]:
                    problemes.append(f"DM #{k} {nomch} {a[idx]!r} != {e[idx]!r}")
            for idx, nomch in ((2, "pMessage"), (4, "pfQOP")):
                if not _pile_valide(a[idx]) or a[idx] % 8:
                    problemes.append(f"DM #{k} {nomch} {a[idx]:#x} hors pile/aligné")
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
                problemes.append(f"DM #{k} pBuffers != pMessage+0x10")
            for j, (ba, be) in enumerate(zip(bufs, e[5][3])):
                if ba != be:
                    problemes.append(f"DM #{k} tampon {j} {ba} != {be}")
    return problemes


# --- Comptage de compensation (V2 : l'oracle constate PAR COMPTAGE) ----------------

def compter_compensation(appels: list) -> tuple[int, int, int, int]:
    return (sum(1 for a in appels if a[0] == "ACH"),
            sum(1 for a in appels if a[0] == "DSC"),
            sum(1 for a in appels if a[0] == "FCH"),
            sum(1 for a in appels if a[0] == "CLOSESOCKET"))


# --- V2 : scénarios de la spécification -------------------------------------------

# (nom, script, rax attendu, comptes (ACH, DSC, FCH, CLOSE), hôte, requête)
SCENARIOS_V2 = [
    ("succès complet — poignée 2 allers, un record, close_notify pur",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, 121, 21],
            dm=[(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)]),
     0, (1, 1, 1, 1), None, None),
    ("certificat invalide — I4 : la ligne console « certificat rejete » ET la "
     "compensation (le contexte barbouillé par la bibliothèque EST détruit)",
     Script(isc=[(CERT_INVALIDE, 0)]),
     3, (1, 1, 1, 1), None, None),
    ("échec tcp-13 (résolution) — compensation TRIVIALE : aucun appel",
     Script(gai=[0x2AFA]),
     7, (0, 0, 0, 0), None, None),
    ("verdict 5 à la poignée — jeton trucidé",
     Script(isc=[(INVALID_TOKEN, 0)]),
     5, (1, 1, 1, 1), None, None),
    ("altération en plein relais — E3 : réponse tronquée PROPRE (le client "
     "garde le premier record, le verdict revient)",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, 121, 121],
            dm=[(OK, 5, 100, 16), (ALTERE, 5, 100, 16)]),
     5, (1, 1, 1, 1), None, None),
    ("close_notify avec résidu — la curiosité consignée (utile 37 au cadre)",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, 121, 58],
            dm=[(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)]),
     0, (1, 1, 1, 1), None, None),
    ("échec de libération simulé (Delete) — E4 : UNE ressaisie, l'ordre continue",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, 121, 21],
            dm=[(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)],
            dsc=[INVALID_HANDLE]),
     0, (1, 2, 1, 1), None, None),
    ("échec de libération simulé (Free, double échec) — la ressaisie unique, "
     "le verdict de session reste 0, le champ credentials survit",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, 121, 21],
            dm=[(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)],
            fch=[INVALID_HANDLE, INVALID_HANDLE]),
     0, (1, 1, 2, 1), None, None),
    ("drain de deux enregistrements en un lot — AUCUNE réception entre les "
     "deux tls-07 (jamais un record déchiffrable en zone pendant que tcp-03 "
     "attendrait)",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, 172, 0],
            dm=[(OK, 5, 100, 16), (OK, 3, 40, 8)]),
     0, (1, 1, 1, 1), None, None),
    ("fermeture système par tcp-03 — le serveur a fini (n = 0), Q1 succès",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, 121, 0],
            dm=[(OK, 5, 100, 16)]),
     0, (1, 1, 1, 1), None, None),
    ("client parti en plein pompage — tcp-04 ≤ 0 vers le CLIENT, Q1 succès",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, 121],
            dm=[(OK, 5, 100, 16)], send=["plein", "plein", "plein", -1]),
     0, (1, 1, 1, 1), None, None),
    ("boucle sans fin — E5 : seize allers, la poignée interminable",
     Script(isc=[(CONT, 8)] * 16, recv=[128]),
     5, (1, 1, 1, 1), None, None),
    ("tls-01 en refus (octet >= 0x80) — la cible ne peut être NOMMÉE : verdict "
     "7, la socket seule est compensée",
     Script(),
     7, (0, 0, 0, 1), b"ex\xe9mple.fr", None),
    ("densité hostile — garde chambre NULLE avant tcp-03 (r8 > 0 est SON "
     "contrat) : la « zone dépassée » de la table http-10:R2",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, "max"],
            dm=[(INCOMPLET, 5, 100, 16)]),
     5, (1, 1, 1, 1), None, None),
    ("verdict 6 exotique à la poignée — table TOTALE",
     Script(isc=[(EXOTIQUE, 0)]),
     6, (1, 1, 1, 1), None, None),
    ("incomplet puis complet — Q2 puis Q1 après un octet de plus, à travers "
     "l'orchestrateur (la géométrie D89 de bout en bout)",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, 120, 1, 0],
            dm=[(INCOMPLET, 5, 100, 16), (OK, 5, 100, 16)]),
     0, (1, 1, 1, 1), None, None),
    ("lot exactement consommé de 0x8000 — la région VIDE rend sa géométrie "
     "morte : reprise en tête (D90) — sans elle la session saine mourrait",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, "max", 0],
            dm=[(OK, 5, 32747, 16)]),
     0, (1, 1, 1, 1), None, None),
    ("ACH en échec (SEC_E_INVALID_HANDLE, hors liste blanche) — verdict 6 fatal, "
     "rien n'est acquis : la socket seule est compensée",
     Script(ach=INVALID_HANDLE),
     6, (1, 0, 0, 1), None, None),
    ("émission cliente partielle — l'achèvement borné vers le client",
     Script(isc=[(CONT, 64), (OK, 32)], recv=[128, 121, 21],
            dm=[(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)],
            send=["plein", "plein", "plein", 50]),
     0, (1, 1, 1, 1), None, None),
    ("connect en échec — le nettoyage INTERNE de tcp-13 (closesocket + "
     "freeaddrinfo, sa Q4) puis la compensation triviale",
     Script(connect=[-1]),
     7, (0, 0, 0, 1), None, None),
]

MUTATIONS_V4 = [
    ("M1 verdict cible dévié (7 → 8)",
     ("mov dword ptr [rsp + 0x58], 7", "mov dword ptr [rsp + 0x58], 8")),
    ("M2 port dévié (+0x10 → +0x12 : le champ canari lu comme port)",
     ("movzx r8d, word ptr [r11 + 0x10]",
      "movzx r8d, word ptr [r11 + 0x12]")),
    ("M3 socket cliente déviée (+0x28 → +0x30)",
     ("mov rcx, [r11 + 0x28]", "mov rcx, [r11 + 0x30]")),
    ("M4 test de compensation du contexte dévié (+0x10 → +0x20 : la socket "
     "gâte l'entrée — DSC appelé sur un handle NUL, refusé)",
     ("cmp qword ptr [r10 + 0x10], 0", "cmp qword ptr [r10 + 0x20], 0")),
    ("M5 drain cassé (jnz → jz : le résidu déchiffrable reste en zone)",
     ("jnz 0x6ea3", "jz 0x6ea3")),
    ("M6 garde chambre relâchée (0x8000 → 0x8001 : tcp-03 à longueur nulle)",
     ("cmp rax, 0x8000", "cmp rax, 0x8001")),
    ("M7 champ utile dévié (+0x3A → +0x3E)",
     ("mov word ptr [r10 + 0x3A], cx", "mov word ptr [r10 + 0x3E], cx")),
    ("M8 routage console du verdict 3 dévié (cmp 3 → 4)",
     ("cmp eax, 3", "cmp eax, 4")),
    ("M9 longueur de la ligne certificat déviée (19 → 18)",
     ("mov edx, 19", "mov edx, 18")),
    ("M10 destination de réception déviée (rax → rcx : la socket comme offset)",
     ("add rdx, rax", "add rdx, rcx")),
    ("M11 verdict de succès dévié (0 → 1)",
     ("mov dword ptr [rsp + 0x58], 0", "mov dword ptr [rsp + 0x58], 1")),
    ("M12 pointeur de requête dévié (+0x18 → +0x10 : le port lu comme adresse)",
     ("mov rdx, [r11 + 0x18]", "mov rdx, [r11 + 0x10]")),
]


def jouer_scenario(emu: Emulateur, script: Script, hote: bytes, requete: bytes,
                   port: int) -> tuple[int, list, bytes, list[str]]:
    """Exécute UN scénario contre le modèle — écarts nommés."""
    modele = Modele(script, hote, requete, port)
    rax_att, appels_att, image_att = modele.executer()
    emu.preparer(hote, requete, port)
    rax = emu.appeler(script)
    problemes: list[str] = []
    if rax != rax_att:
        problemes.append(f"rax {rax} != {rax_att} (modèle spec)")
    image_lue = bytes(emu.uc.mem_read(ZONE_CADRE, TAILLE_CADRE_PAGE))
    if image_lue != image_att:
        off = next(o for o in range(TAILLE_CADRE_PAGE) if image_lue[o] != image_att[o])
        problemes.append(f"cadre diverge @+0x{off:x} (attendu {image_att[off]:#04x}, "
                         f"lu {image_lue[off]:#04x})")
    problemes += comparer_traces(emu.appels, appels_att)
    problemes += emu.hygiene()
    return rax_att, appels_att, image_att, problemes


def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261028)
    args = parseur.parse_args()

    print("=== harnais_session.py — tls-08:R1 (session TLS cliente, D90 session) ===")
    print(f"graine {args.graine} · intégration : 18 blocs réels "
          "(M0 hello-02, M1 libc-01/03/04/07, M2/M3 tcp, M4 tls-01..08)")

    ks = Ks(KS_ARCH_X86, KS_MODE_64)

    # --- V1 : round-trip (tls-08 + les dix-sept blocs intégrés) ---------------
    print("\n[V1] round-trip de notation")
    blob08, declare = octets_notation(ks, "tls-08-session", RVA_TLS08)
    controle("tls-08-session rassemblée == taille déclarée (Code : N o)",
             declare is not None and len(blob08) == declare, f"{len(blob08)} o")
    controle("padding du slot >= 16 (D8) — slot 0x600 préfiguré conservé",
             SLOT_TLS08 - len(blob08) >= 16, f"{SLOT_TLS08 - len(blob08)} o")
    blobs = {"tls-08": blob08}
    # hello-02 : format d'en-tête M0 hérité (pas de ligne « Code : ») — la
    # taille attendue est la mesure M0, consignée ici une seule fois
    TAILLES_M0 = {"hello-02-write": 27}
    INTEGRATIONS = [
        ("tls-01-nom-utf16", RVA_TLS01, None, "tls-01"),
        ("tls-02-verdicts", RVA_TLS02, None, "tls-02"),
        ("tls-03-jetons", RVA_TLS03, None, "tls-03"),
        ("tls-04-poignee", RVA_TLS04, None, "tls-04"),
        ("tls-05-cles", RVA_TLS05, None, "tls-05"),
        ("tls-06-emission", RVA_TLS06, None, "tls-06"),
        ("tls-07-reception", RVA_TLS07, None, "tls-07"),
        ("tcp-03-recv", RVA_TCP03, os.path.join(ICI, os.pardir, "m2", "notation"), "tcp-03"),
        ("tcp-04-send", RVA_TCP04, os.path.join(ICI, os.pardir, "m2", "notation"), "tcp-04"),
        ("tcp-05-close", RVA_TCP05, os.path.join(ICI, os.pardir, "m2", "notation"), "tcp-05"),
        ("tcp-11-journal", RVA_TCP11, os.path.join(ICI, os.pardir, "m2", "notation"), "tcp-11"),
        ("tcp-13-connexion", RVA_TCP13, os.path.join(ICI, os.pardir, "m3", "notation"), "tcp-13"),
        ("libc-01-memcpy", RVA_MEMCPY, os.path.join(ICI, os.pardir, "m1", "notation"), "libc-01"),
        ("libc-03-strlen", RVA_STRLEN, os.path.join(ICI, os.pardir, "m1", "notation"), "libc-03"),
        ("libc-04-itoa", RVA_ITOA, os.path.join(ICI, os.pardir, "m1", "notation"), "libc-04"),
        ("libc-07-memset", RVA_MEMSET, os.path.join(ICI, os.pardir, "m1", "notation"), "libc-07"),
        ("hello-02-write", RVA_HELLO02, os.path.join(ICI, os.pardir, "m0", "notation"), "hello-02"),
    ]
    for bloc, rva, chemin, cle in INTEGRATIONS:
        chemin_bloc = os.path.join(chemin, bloc + ".asm") if chemin else None
        b, d = octets_notation(ks, bloc, rva, chemin=chemin_bloc)
        blobs[cle] = b
        attendu = TAILLES_M0.get(bloc, d)
        controle(f"{bloc} (intégration) == taille déclarée",
                 attendu is not None and len(b) == attendu, f"{len(b)} o")
    emu = Emulateur(blobs)

    # --- V2 : oracle à scénarios — la compensation constatée PAR COMPTAGE -----
    print("\n[V2] oracle à scénarios — cadre 0xD000 + paquet + contrat d'appels "
          "complet + comptes de compensation")
    for nom, script, rax_att, comptes_att, hote, requete in SCENARIOS_V2:
        hote = hote or HOTE_DEFAUT
        requete = requete or REQUETE_DEFAUT
        rax_mod, appels_att, _img, problemes = jouer_scenario(
            emu, script, hote, requete, PORT_DEFAUT)
        comptes = compter_compensation(emu.appels)
        if comptes != comptes_att:
            problemes.append(f"comptes de compensation {comptes} != {comptes_att} "
                             "(ACH, DSC, FCH, CLOSESOCKET)")
        if rax_att is not None and rax_mod != rax_att:
            problemes.append(f"le modèle dit rax={rax_mod}, la spec attend {rax_att}")
        # le paquet INTACT (Q3 de tls-06 : le clair de l'appelant jamAIS touché)
        paquet_lu = bytes(emu.uc.mem_read(ZONE_PAQUET, TAILLE_PAQUET))
        if (paquet_lu[0x100:0x100 + len(hote)] != hote or
                paquet_lu[0x200:0x200 + len(requete)] != requete or
                paquet_lu[0x30:0x100] != CANARI * (0x100 - 0x30)):
            problemes.append("paquet altéré (hôte/requête/canaris)")
        n_appels = len(appels_att)
        controle(f"scénario « {nom} »", not problemes,
                 "; ".join(problemes[:3]) if problemes else
                 f"{n_appels} appels, rax={rax_mod}, comptes {comptes}")

    # --- V3 : non applicable (héritage M3 pour les orchestrateurs) -----------
    print("\n[V3] NON APPLICABLE — spec tls-08:V3 : aucune entrée non fiable "
          "directe (tout traverse tls-01..07) ; héritage de la règle M3")
    controle("V3 écarté conformément à la spécification (traçabilité)", True)

    # --- V4 : falsification ---------------------------------------------------
    print("\n[V4] falsification — douze mutations d'un point, chacune attrapée")
    for nom, mutation in MUTATIONS_V4:
        blob_m, _ = octets_notation(ks, "tls-08-session", RVA_TLS08, mutation)
        blobs_m = dict(blobs)
        blobs_m["tls-08"] = blob_m
        emu_m = Emulateur(blobs_m)
        attrapes = 0
        for nom_s, script, _rax, _c, hote, requete in SCENARIOS_V2:
            try:
                hote = hote or HOTE_DEFAUT
                requete = requete or REQUETE_DEFAUT
                if jouer_scenario(emu_m, script, hote, requete, PORT_DEFAUT)[3]:
                    attrapes += 1
            except Exception:
                attrapes += 1          # faute d'exécution = écart nommé
        controle(f"mutation « {nom} » ATTRAPÉE", attrapes > 0,
                 f"{attrapes}/{len(SCENARIOS_V2)} scénarios en écart")
    # témoin intact : le différentiel reste vert (une suite qui ne peut pas
    # échouer ne prouve rien — le témoin prouve que les pièges sont armés)
    emu_t = Emulateur(blobs)
    verts = sum(1 for nom_s, script, _rax, _c, hote, requete in SCENARIOS_V2
                if not jouer_scenario(emu_t, script, hote or HOTE_DEFAUT,
                                      requete or REQUETE_DEFAUT, PORT_DEFAUT)[3])
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
