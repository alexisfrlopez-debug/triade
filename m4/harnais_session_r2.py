#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_session_r2.py — Harnais de http-10:R2 (D92 — la révision de routage TLS).

LA révision du jalon M4 côté orchestration : la session proxy scellée 0.4.0
(http-10:R3, 1847 o) reprend son comportement hérité TEL QUEL et AJOUTE le
routage du verdict « cible TLS » (http-08:R2 rax = 4) vers la session TLS
tls-08, avec l'entrée ÉTIQUETÉE de la table des réponses (502 « Certificat
rejete ») — le critère M4 « échec propre sur certificat invalide » ATERRIT
dans cette révision. La notation R2 (2109 o, slot préfiguré 0x74C0×0x900
conservé, padding 195 >= 16 — D8) est émulée à son RVA .text3 exact AVEC les
vrais octets de TOUTE sa chaîne d'appel — L'INTÉGRATION LA PLUS LARGE DU
PROJET : vingt-neuf blocs réels (M0 hello-02 ; M1 libc-01/03/04/07 ; M2
tcp-03/04/05/06/11 ; M3 tcp-13, http-01..09 ; M4 tls-01..08, http-08:R2) +
l'ANCIEN scellé (http-10:R3 @0x5580 avec http-08:R1 @0x5380) pour le
différentiel d'ancêtre. Vecteurs de la spécification http-10:R2 :

  V1  round-trip de notation 100 % (taille == « Code : N o », padding >= 16)
      pour la révision ET les vingt-huit blocs intégrés ;

  V2a DIFFÉRENTIEL D'ANCÊTRE (l'anti-régression R7 — « le chemin M3 http non
      TLS inchangé octet pour octet ») : l'ancêtre http-10:R3 (octets scellés
      0.4.0, assemblés à son RVA 0x5580) et la révision sont émulés sur les
      MÊMES scénarios ; les traces observables (lignes console, octets au
      client, résolutions/connexions, fermetures, spawns) sont comparées
      APRÈS NORMALISATION des pointeurs par la base du cadre de CHAQUE run
      (l'adresse appartient à la notation, le CONTENU au contrat — l'adresse
      du proc du thread détaché est exclue : .text2 pour l'ancêtre, .text3
      pour la révision) : ÉCART ZÉRO hors domaine https ; dans le domaine,
      l'ancêtre refuse 501 (« jamais d'un schéma https en requête directe »,
      http-08:R1:Q4) et la révision route — la divergence est EXACTEMENT la
      cible https byte-exact ;

  V2b oracle à scénarios TLS : chaque scénario vérifie la réponse EXACTE au
      client (octets de la table Q3' — l'entrée étiquetée comprise), les
      lignes console EXACTES (la ligne « certificat rejete » UNE FOIS — tls-08
      seul propriétaire, point croisé D91 : jamais de double émission), la
      compensation croisée tls-08:Q3 PAR COMPTAGE (ACH/DSC/FCH/CLOSESOCKET),
      le PAQUET DE SESSION au passage de tls-08 (hôte / port 443 ou explicite
      / requête réécrite forme origine / socket cliente — P6) et le CADRE TLS
      VIERGE (0xC260 en canaris AVANT l'appel, intégralement zéro AU passage —
      le rep stosq est la preuve, pas une supposition de pages fraîches) ;
      le paquet reste INTACT au retour (le clair de l'appant jamais touché) ;

  V3  NON APPLICABLE (spec http-10:R2:V3 — héritage M3 : la session reste
      hors fuzz direct, ses entrées non fiables traversent les blocs fuzzés) ;

  V4  falsification : ONZE mutations d'un seul point, STABLES EN TAILLE
      (leçon D82), chacune ATTRAPÉE ; le témoin intact reste vert ;

  V6bis contrôle statique du prologue étendu (héritage R3/D63 — le cadre a
      grandi de 0xC290 : paquet + cadre TLS) : la boucle de probing descend de
      -0x1000 à -0x13000 par pas de 0x1000, touche finale [rsp-0x13390],
      sub rsp, 0x13390 — la leçon terrain 21:38 reste armée ; ET le test de
      rejet I6' : les cibles d'appel direct ⊆ liste blanche héritage + tls-08
      + http-08:R2 (+ étiquettes internes du slot), UN SEUL appel IAT
      (CloseHandle — handle de la pompe détachée, miroir tcp-12:I4), AUCUN
      appel SSPI direct ni appel direct tls-01..07 (la chaîne cryptographique
      vit derrière tls-08).

Règles shims PARTAGÉES avec harnais_session.py (D90 — jamais deux sources de
vérité, l'Emulateur D90 est SOUS-CLASSÉ) : les entrées recv du script peuvent
être des OCTETS (les requêtes du client — l'accumulation est une vraie
réception) ou des longueurs (motifs déterministes côté serveur) ou 'max' ou
<= 0 ; GAI réussit et pose l'addrinfo factice ; socket/connect/closesocket/
recv/send pilotés par le script ; CreateThread rend un handle factice (le
thread détaché n'est PAS exécuté — son spawn et son CloseHandle sont le
contrat) ; CloseHandle rend 1. La pile arrive en CANARIS : le cadre TLS doit
être zéroé PAR la notation. La réponse 502 suit le RETOUR du verdict —
http-10:R2 mappe sur rax, jamais sur le cadre (README D90).

Usage : python3 harnais_session_r2.py [--graine G]
"""

from __future__ import annotations

import argparse
import os
import re
import struct
import sys
from collections import namedtuple

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, "outils"))
import layout as L  # noqa: E402

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX,  # noqa: E402
                               UC_X86_REG_RSP, UC_X86_REG_RDX)

import harnais_session as HS  # noqa: E402 — le harnais D90 (tls-08), sous-classé

from harnais_session import (  # noqa: E402
    REGS, Script, motif, clair_dm, permuter16, verdict_modele,
    OK, CONT, INCOMPLET, CONTEXTE_EXPIRE, ALTERE, CERT_INVALIDE,
    INVALID_TOKEN, EXOTIQUE,
    SOCKET_SERVEUR, SOCKET_CLIENT, FAKE_STDOUT, FAKE_ADDR,
    ADRESSE_ADDRINFO, ADRESSE_SOCKADDR, CANARI, SENTINELLES_NV,
    FAUX, FAUX_REV, lignes_notation, octets_notation,
    compter_compensation, Emulateur,
    ZONE_ADDRINFO, TAILLE_ADDRINFO,
)

# --- Mémoire du harnais (la pile porte le cadre de session 0x13390) ---------------

ZONE_TEXTE, TAILLE_TEXTE = 0x1000, 0x1000
ZONE_RDATA, TAILLE_RDATA = 0x2000, 0x1000
ZONE_TCP, TAILLE_TCP = 0x4000, 0x2000          # .text2 complète (tcp + http M3)
ZONE_CODE, TAILLE_CODE = 0x6000, 0x2000        # .text3 (tls + les DEUX révisions)
ZONE_DATA, TAILLE_DATA = 0x3000, 0x1000
RET_MAGIQUE = 0x7E00
TRAMPOLINE, TAILLE_TRAMP = 0x140100000, 0x1000
ZONE_PILE, TAILLE_PILE = 0x7F000000, 0x40000   # cadre 0x13390 + chaîne tls
RSP_ENTREE = 0x7F030008                        # ≡ 8 mod 16 — entrée ABI (P5)
HANDLE_THREAD = 0x6666666666666666

RVA_SESSION_R2, SLOT_R2 = 0x74C0, 0x900        # g70010 (préfiguré, conservé)
RVA_SESSION_R1 = 0x5580                        # e50010 (ancêtre scellé 0.4.0)
CADRE_R1, CADRE_R2 = 0x7100, L.TAILLE_CADRE_SESSION_R2   # 0x13390 (D92)
RVA_TLS08 = 0x6D40

# --- Fixtures .rdata (M3 scellées + M4 — textes consignés m3/layout.py) -----------

TXT_400 = b"HTTP/1.1 400 Requete mal formee\r\n\r\n"
TXT_431 = b"HTTP/1.1 431 Tete trop grande\r\n\r\n"
TXT_501 = b"HTTP/1.1 501 Non implemente\r\n\r\n"
TXT_411 = b"HTTP/1.1 411 Longueur requise\r\n\r\n"
TXT_505 = b"HTTP/1.1 505 Version non supportee\r\n\r\n"
TXT_502 = b"HTTP/1.1 502 Passerelle inaccessible\r\n\r\n"
TXT_TUNNEL = b"HTTP/1.1 200 Tunnel etabli\r\n\r\n"
MSG_CONNEXION = b"connexion entrante\r\n"
MSG_TUNNEL = b"tunnel\r\n"
MSG_FIN = b"fin connexion\r\n"
METHODES = [b"GET", b"HEAD", b"POST", b"PUT",
            b"DELETE", b"OPTIONS", b"TRACE", b"CONNECT"]

REUSSITES, ECHECS = [], []


def controle(nom: str, ok: bool, detail: str = "") -> None:
    if ok:
        REUSSITES.append(nom)
        print(f"  [PASS] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append(nom)
        print(f"  [FAIL] {nom}" + (f" — {detail}" if detail else ""))


# --- Script R2 : les entrées recv peuvent être des OCTETS (le client parle) -------

class ScriptR2(Script):
    """recv[i] = octets (requête cliente, livrée telle quelle) | n > 0 (motif)
    | 'max' | <= 0 (fermeture/erreur). Le modèle et les shims voient le même."""

    def donnees_recv(self, i: int, capacite: int) -> tuple[int, bytes]:
        if i < len(self.entries_recv):
            e = self.entries_recv[i]
        else:
            e = 16
        if isinstance(e, (bytes, bytearray)):
            n = min(len(e), capacite)
            return n, bytes(e[:n])
        if e == "max":
            return capacite, motif(i, capacite)
        if e <= 0:
            return e, b""
        n = min(e, capacite)
        return n, motif(i, n)


# --- Émulateur de session (hérite des shims D90 — jamais deux sources) -----------

def _u64(uc: Uc, p: int) -> int:
    return struct.unpack("<Q", bytes(uc.mem_read(p, 8)))[0]


def _u16(uc: Uc, p: int) -> int:
    return struct.unpack("<H", bytes(uc.mem_read(p, 2)))[0]


class EmulateurSession(Emulateur):
    """Un chargement = un émulateur NEUF (leçon D79). La session (révision OU
    ancêtre) est émulée à son RVA avec sa chaîne complète ; la pile arrive en
    CANARIS — le cadre TLS doit être zéroé PAR la notation (P6/P1 tls-08).
    Le passage de tls-08 est CAPTURÉ (rcx cadre, rdx paquet) : paquet et
    virginité du cadre sont constatés AU passage, jamais déduits."""

    def __init__(self, blobs: dict, rva_session: int, cadre_taille: int):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        for base, taille in ((ZONE_TEXTE, TAILLE_TEXTE), (ZONE_RDATA, TAILLE_RDATA),
                             (ZONE_TCP, TAILLE_TCP), (ZONE_CODE, TAILLE_CODE),
                             (ZONE_DATA, TAILLE_DATA), (TRAMPOLINE, TAILLE_TRAMP),
                             (ZONE_PILE, TAILLE_PILE),
                             (ZONE_ADDRINFO, TAILLE_ADDRINFO)):
            uc.mem_map(base, taille)
        # .text : hello-02 + libc (octets scellés M0/M1, R7)
        page = b"\xCC" * TAILLE_TEXTE
        for rva, cle in ((0x1040, "hello-02"), (0x1100, "libc-01"),
                         (0x1200, "libc-03"), (0x1280, "libc-04"),
                         (0x13C0, "libc-07")):
            page = page[:rva - ZONE_TEXTE] + blobs[cle] + page[rva - ZONE_TEXTE + len(blobs[cle]):]
        uc.mem_write(ZONE_TEXTE, page)
        # .text2 : tcp M2 + http M3 + tcp-13 + L'ANCIÊTRE http-10:R3 (R7)
        page = b"\xCC" * TAILLE_TCP
        for rva, cle in ((0x4140, "tcp-03"), (0x4180, "tcp-04"), (0x41C0, "tcp-05"),
                         (0x4300, "tcp-06"), (0x4400, "tcp-13"), (0x4B00, "tcp-11"),
                         (0x4C00, "http-01"), (0x4C80, "http-02"), (0x4E80, "http-03"),
                         (0x4F40, "http-04"), (0x5080, "http-05"), (0x5140, "http-06"),
                         (0x5200, "http-07"), (0x5380, "http-08-R1"), (0x54C0, "http-09"),
                         (0x5580, "http-10-R1")):
            page = page[:rva - ZONE_TCP] + blobs[cle] + page[rva - ZONE_TCP + len(blobs[cle]):]
        uc.mem_write(ZONE_TCP, page)
        # .text3 : tls-01..08 + http-08:R2 + http-10:R2 (génération 6)
        page = b"\xCC" * TAILLE_CODE
        for rva, cle in ((0x6000, "tls-01"), (0x6080, "tls-02"), (0x6180, "tls-03"),
                         (0x62C0, "tls-04"), (0x65C0, "tls-05"), (0x6740, "tls-06"),
                         (0x6A40, "tls-07"), (0x6D40, "tls-08"),
                         (0x7340, "http-08-R2"), (0x74C0, "http-10-R2")):
            page = page[:rva - ZONE_CODE] + blobs[cle] + page[rva - ZONE_CODE + len(blobs[cle]):]
        uc.mem_write(ZONE_CODE, page)
        uc.mem_write(TRAMPOLINE, b"\xc3" * TAILLE_TRAMP)
        # résolution chargeur : IAT kernel32/ws2_32/secur32 → fausses adresses
        for nom, rva in {**L.IAT_SLOTS, **L.IAT_SEC32_SLOTS}.items():
            uc.mem_write(rva, struct.pack("<Q", FAUX[nom]))
        # fixtures .rdata M3 scellées (textes consignés m3/layout.py, R7)
        offsets, cur = [], 0x24A0
        for m in METHODES:
            offsets.append(cur)
            cur += len(m) + 1
        table = b"".join(struct.pack("<QQ", p, len(m)) for p, m in zip(offsets, METHODES))
        table += struct.pack("<QQ", 0, 0)               # terminateur (len 0)
        for rva, contenu in (
                (0x2410, table),
                (0x24A0, b"".join(m + b"\x00" for m in METHODES)),
                (0x24D0, b"/\x00"),
                (0x2560, TXT_400), (0x2584, TXT_431), (0x25A8, TXT_501),
                (0x25C8, TXT_411), (0x25EC, TXT_505), (0x2614, TXT_502),
                (0x2640, TXT_TUNNEL), (0x2870, MSG_CONNEXION),
                (0x2890, MSG_TUNNEL), (0x28A0, MSG_FIN),
                (0x2950, b"Host\x00"), (0x2960, b"Content-Length\x00"),
                (0x2970, b"Transfer-Encoding\x00"),
                (L.R_PKG_M4, L.PKG_M4),
                (L.R_TXT_TLS_ETABLI, L.TXT_TLS_ETABLI),
                (L.R_TXT_TLS_CERT, L.TXT_TLS_CERT),
                (L.R_TXT_502_CERT, L.TXT_502_CERT)):
            uc.mem_write(rva, contenu)
        # addrinfo factice + .data (état serveur)
        ai = struct.pack("<iiiiQQQQ", 0, 2, 1, 0, 16, 0, ADRESSE_SOCKADDR, 0)
        uc.mem_write(ADRESSE_ADDRINFO, ai)
        uc.mem_write(ADRESSE_SOCKADDR,
                     struct.pack("<HH", 2, 0x1234) + struct.pack("<I", FAKE_ADDR))
        uc.mem_write(L.R_STDOUT, struct.pack("<Q", FAKE_STDOUT))
        uc.mem_write(L.R_CS, b"\x00" * 40)
        # les shims D90 (page ret + crochet code) + le passage de tls-08
        uc.hook_add(UC_HOOK_CODE, self._shim, begin=TRAMPOLINE,
                    end=TRAMPOLINE + TAILLE_TRAMP)
        uc.hook_add(UC_HOOK_CODE, self._passage_tls08, begin=RVA_TLS08, end=RVA_TLS08)
        self.rva_session = rva_session
        self.cadre_taille = cadre_taille
        self.rsp_session = RSP_ENTREE - 0x28 - cadre_taille
        self.script: Script | None = None
        self.appels: list[tuple] = []
        self.faux_pas: list[str] = []
        self.boundary: dict | None = None
        self._i_gai = self._i_socket = self._i_connect = 0
        self._i_isc = self._i_recv = self._i_send = 0
        self._i_qca = self._i_em = self._i_dm = self._i_dsc = self._i_fch = 0

    # --- le passage de tls-08 : le paquet et la virginité, constatés ------------

    def _passage_tls08(self, uc: Uc, adresse: int, taille: int, donnees):
        cadre = uc.reg_read(REGS["rcx"])
        paquet = uc.reg_read(REGS["rdx"])
        hote_ptr, hote_len = _u64(uc, paquet + 0x00), _u64(uc, paquet + 0x08)
        req_ptr, req_len = _u64(uc, paquet + 0x18), _u64(uc, paquet + 0x20)
        self.boundary = {
            "cadre": cadre, "paquet": paquet,
            "hote": bytes(uc.mem_read(hote_ptr, hote_len)) if hote_ptr else b"",
            "port": _u16(uc, paquet + 0x10),
            "requete": bytes(uc.mem_read(req_ptr, req_len)) if req_ptr else b"",
            "req_ptr": req_ptr, "req_len": req_len,
            "socket": _u64(uc, paquet + 0x28),
            "cadre_vierge": bytes(uc.mem_read(cadre, L.TAILLE_CADRE)) == b"\x00" * L.TAILLE_CADRE,
        }

    # --- shims propres à la session (le reste hérite de D90) -------------------

    def _api_send(self):
        uc = self.uc
        sock = uc.reg_read(REGS["rcx"])
        buf = uc.reg_read(REGS["rdx"])
        ln = uc.reg_read(REGS["r8"])
        r = self.script.comportement_send(self._i_send, ln)
        self._i_send += 1
        # le CONTRAT porte les octets EFFECTIVEMENT émis (émission partielle :
        # l'achèvement borne — la concaténation cliente n'en compte que l'émis)
        contenu = bytes(uc.mem_read(buf, min(ln, r))) if (ln > 0 and r > 0) else b""
        self.appels.append(("SEND", sock, buf, ln, contenu))
        uc.reg_write(REGS["rax"], r & 0xFFFFFFFFFFFFFFFF)

    def _api_CreateThread(self):
        proc = self.uc.reg_read(REGS["rcx"])
        arg = self.uc.reg_read(REGS["rdx"])
        # le thread détaché n'est PAS exécuté : spawn + CloseHandle sont le contrat
        self.appels.append(("CREATETHREAD", proc, arg))
        self.uc.reg_write(REGS["rax"], HANDLE_THREAD)

    def _api_CloseHandle(self):
        self.appels.append(("CH", self.uc.reg_read(REGS["rcx"])))
        self.uc.reg_write(REGS["rax"], 1)

    # --- pilotage ---------------------------------------------------------------

    def preparer(self) -> None:
        """UNE fois par scénario : la pile EN CANARIS (le cadre TLS sera zéroé
        PAR la notation — la preuve repose sur des canaris), .data, indices."""
        self.uc.mem_write(ZONE_PILE, CANARI * TAILLE_PILE)
        self.uc.mem_write(L.R_STDOUT, struct.pack("<Q", FAKE_STDOUT))
        self.uc.mem_write(L.R_CS, b"\x00" * 40)
        self.appels = []
        self.faux_pas = []
        self.boundary = None
        self._i_gai = self._i_socket = self._i_connect = 0
        self._i_isc = self._i_recv = self._i_send = 0
        self._i_qca = self._i_em = self._i_dm = self._i_dsc = self._i_fch = 0

    def appeler(self, script: Script) -> int:
        uc = self.uc
        self.script = script
        for nom, valeur in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], valeur)
        uc.reg_write(REGS["rsp"], RSP_ENTREE)
        uc.mem_write(RSP_ENTREE, struct.pack("<Q", RET_MAGIQUE))
        uc.reg_write(REGS["rcx"], SOCKET_CLIENT)
        uc.reg_write(REGS["rdx"], 0)
        uc.emu_start(self.rva_session, RET_MAGIQUE, timeout=20_000_000, count=6_000_000)
        return uc.reg_read(REGS["rax"]) & 0xFFFFFFFFFFFFFFFF

    def hygiene(self) -> list[str]:
        problemes = list(self.faux_pas)
        for nom, valeur in SENTINELLES_NV.items():
            if self.uc.reg_read(REGS[nom]) != valeur:
                problemes.append(f"non-volatil {nom} modifié (I2)")
        for nom, rva in {**L.IAT_SLOTS, **L.IAT_SEC32_SLOTS}.items():
            if struct.unpack("<Q", bytes(self.uc.mem_read(rva, 8)))[0] != FAUX[nom]:
                problemes.append(f"IAT {nom} réécrite")
        for rva, attendu, nomf in (
                (0x2560, TXT_400, "ligne 400"), (0x2584, TXT_431, "ligne 431"),
                (0x25A8, TXT_501, "ligne 501"), (0x25C8, TXT_411, "ligne 411"),
                (0x25EC, TXT_505, "ligne 505"), (0x2614, TXT_502, "ligne 502"),
                (0x2640, TXT_TUNNEL, "ligne tunnel"),
                (0x2870, MSG_CONNEXION, "ligne connexion"),
                (0x2890, MSG_TUNNEL, "ligne tunnel-journal"),
                (0x28A0, MSG_FIN, "ligne fin"),
                (0x2950, b"Host\x00", "chercheur Host"),
                (0x2960, b"Content-Length\x00", "chercheur CL"),
                (0x2970, b"Transfer-Encoding\x00", "chercheur TE"),
                (0x24D0, b"/\x00", "fixture slash"),
                (L.R_PKG_M4, L.PKG_M4, "fixture package"),
                (L.R_TXT_TLS_ETABLI, L.TXT_TLS_ETABLI, "ligne tunnel chiffre etabli"),
                (L.R_TXT_TLS_CERT, L.TXT_TLS_CERT, "ligne certificat rejete"),
                (L.R_TXT_502_CERT, L.TXT_502_CERT, "ligne 502 certificat")):
            if bytes(self.uc.mem_read(rva, len(attendu))) != attendu:
                problemes.append(f"fixture {nomf} altérée")
        if struct.unpack("<Q", bytes(self.uc.mem_read(L.R_STDOUT, 8)))[0] != FAKE_STDOUT:
            problemes.append("état .data stdout altéré")
        if bytes(self.uc.mem_read(L.R_CS, 40)) != b"\x00" * 40:
            problemes.append("section critique .data altérée")
        return problemes


# --- Normalisation du différentiel (l'adresse appartient à la notation) -----------

def normaliser(appels: list, base: int) -> list:
    """Pointeurs de PILE → offset (positif : dans le cadre ; négatif : chaîne
    d'appel sous le cadre — même géométrie des deux côtés). Les pointeurs
    HORS pile (fixtures .rdata, addrinfo, cadre-miroir ZONE_CADRE, sockets
    factices) passent tels quels — l'adresse appartient à la notation, le
    CONTENU au contrat. Le proc du thread détaché est exclus (.text2 ancêtre /
    .text3 révision). TOUS LES CHAMPS de TOUTES les entrées sont normalisés :
    la révision http-10:R3 pousse DEUX registres de plus (P8 — rsi/rdi) et
    déplace TOUTE la chaîne de 0x10 — un pointeur SSPI brut (ACH pAuthData,
    pfHandle) différerait de 0x10 entre ancêtre et révision sans AUCUN sens
    comportemental ; pour le différentiel R1/R2 (géométrie égale) la
    normalisation supplémentaire est un non-événement (les DEUX côtés)."""
    def norm(p):
        if isinstance(p, (tuple, list)):
            return type(p)(norm(x) for x in p)
        if isinstance(p, int) and ZONE_PILE <= p < ZONE_PILE + TAILLE_PILE:
            return p - base
        return p
    out = []
    for a in appels:
        nom = a[0]
        champs = [norm(x) for x in a[1:]]
        if nom == "CREATETHREAD":
            champs = [None] + champs[1:]
        out.append((nom, *champs))
    return out


# --- Le scénario type -------------------------------------------------------------

Sc = namedtuple("Sc", "nom entree script tls diverge client wf comptes paquet "
                      "ports gai ct")


def jouer(emu: EmulateurSession, sc: Sc) -> list[str]:
    """Exécute UN scénario contre la révision — écarts nommés."""
    emu.preparer()
    try:
        emu.appeler(sc.script)
    except Exception as e:                                  # faute = écart nommé
        return [f"faute d'exécution : {type(e).__name__} {e}"]
    appels = emu.appels
    problemes: list[str] = []
    envoi = b"".join(a[4] for a in appels if a[0] == "SEND" and a[1] == SOCKET_CLIENT)
    if envoi != sc.client:
        problemes.append(f"octets au client : {len(envoi)} o != {len(sc.client)} o attendus"
                         + (f" (début {envoi[:24]!r})" if envoi else ""))
    wfs = [a[2] for a in appels if a[0] == "WF"]
    if wfs != sc.wf:
        problemes.append(f"lignes console : {[w[:20] for w in wfs]} != "
                         f"{[w[:20] for w in sc.wf]}")
    comptes = compter_compensation(appels)
    if comptes != sc.comptes:
        problemes.append(f"comptes de compensation {comptes} != {sc.comptes} "
                         "(ACH, DSC, FCH, CLOSESOCKET)")
    ports = [permuter16(struct.unpack_from("<H", a[2], 2)[0])
             for a in appels if a[0] == "CONNECT"]
    if ports != sc.ports:
        problemes.append(f"ports de connexion {ports} != {sc.ports}")
    gai = [a[1] for a in appels if a[0] == "GAI"]
    if gai != sc.gai:
        problemes.append(f"hôtes résolus {gai} != {sc.gai}")
    ct = sum(1 for a in appels if a[0] == "CREATETHREAD")
    if ct != sc.ct:
        problemes.append(f"spawns de thread {ct} != {sc.ct}")
    if sc.paquet is not None:
        if emu.boundary is None:
            problemes.append("tls-08 jamais appelé (P6/Q2')")
        else:
            b = emu.boundary
            if (b["hote"] != sc.paquet[0] or b["port"] != sc.paquet[1]
                    or b["requete"] != sc.paquet[2] or b["socket"] != SOCKET_CLIENT):
                problemes.append(f"paquet de session : hôte {b['hote']!r} port "
                                 f"{b['port']} requête {b['requete'][:24]!r}… socket "
                                 f"{b['socket']:#x} != attendu")
            if not b["cadre_vierge"]:
                problemes.append("cadre TLS non vierge au passage (P6/P1)")
            # le paquet INTACT au retour : le clair de l'appelant jamais touché
            relue = bytes(emu.uc.mem_read(b["req_ptr"], b["req_len"]))
            if relue != sc.paquet[2]:
                problemes.append("requête claire altérée par le tunnel (Q3 tls-06)")
    elif emu.boundary is not None:
        problemes.append("tls-08 appelé à tort sur ce scénario")
    problemes += emu.hygiene()
    return problemes


def differentiel(emu_r1: EmulateurSession, emu_r2: EmulateurSession,
                 sc: Sc) -> list[str]:
    """L'ancêtre scellé et la révision sur les MÊMES entrées — l'anti-régression
    R7 (V2a) : écart zéro hors domaine https ; dans le domaine, l'ancêtre
    refuse 501 et la révision route."""
    problemes: list[str] = []
    emu_r1.preparer()
    emu_r2.preparer()
    try:
        emu_r1.appeler(sc.script)
        emu_r2.appeler(sc.script)
    except Exception as e:
        return [f"faute d'exécution au différentiel : {type(e).__name__} {e}"]
    t1 = normaliser(emu_r1.appels, emu_r1.rsp_session)
    t2 = normaliser(emu_r2.appels, emu_r2.rsp_session)
    if sc.diverge:
        client_r1 = b"".join(a[4] for a in emu_r1.appels
                             if a[0] == "SEND" and a[1] == SOCKET_CLIENT)
        if client_r1 != TXT_501:
            problemes.append(f"l'ancêtre ne refuse pas 501 sur le domaine https "
                             f"({client_r1[:24]!r}…)")
        if t1 == t2:
            problemes.append("aucune divergence sur un scénario du domaine https")
    else:
        if t1 != t2:
            k = next(i for i in range(max(len(t1), len(t2)))
                     if i >= len(t1) or i >= len(t2) or t1[i] != t2[i])
            problemes.append(f"trace #{k} : ancêtre {t1[k] if k < len(t1) else None} "
                             f"!= révision {t2[k] if k < len(t2) else None}")
    return problemes


# --- V2 : les scénarios (l'entrée cliente est recv[0] en OCTETS) ------------------

HOTE = b"exemple.fr"
GET_ABS = b"GET http://exemple.fr/chemin HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"
GET_ORI = b"GET /chemin HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"
GET_HTTPS = b"GET https://exemple.fr/chemin HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"
REQUETE_R = b"GET /chemin HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"   # la réécriture
CONN, TUNJ, FIN = MSG_CONNEXION, MSG_TUNNEL, MSG_FIN
ETABLI, CERTL = L.TXT_TLS_ETABLI, L.TXT_TLS_CERT

SCENARIOS = [
    Sc("GET absolu http sain — réécriture + relais réponse",
       GET_ABS, ScriptR2(recv=[GET_ABS, 16, 0]),
       False, False, motif(1, 16), [CONN, FIN], (0, 0, 0, 2), None, [80], [HOTE], 0),
    Sc("GET origine — l'autorité viendra de l'en-tête Host",
       GET_ORI, ScriptR2(recv=[GET_ORI, 16, 0]),
       False, False, motif(1, 16), [CONN, FIN], (0, 0, 0, 2), None, [80], [HOTE], 0),
    Sc("POST avec corps — CL borné inline (R2 de http-10:R1)",
       b"POST http://exemple.fr/s HTTP/1.1\r\nHost: exemple.fr\r\n"
       b"Content-Length: 10\r\n\r\n0123456789",
       ScriptR2(recv=[b"POST http://exemple.fr/s HTTP/1.1\r\nHost: exemple.fr\r\n"
                      b"Content-Length: 10\r\n\r\n0123456789", 16, 0]),
       False, False, motif(1, 16), [CONN, FIN], (0, 0, 0, 2), None, [80], [HOTE], 0),
    Sc("CONNECT — tunnel aveugle : 200, pompe détachée, pompe inline",
       b"CONNECT exemple.fr:443 HTTP/1.1\r\nHost: exemple.fr:443\r\n\r\n",
       ScriptR2(recv=[b"CONNECT exemple.fr:443 HTTP/1.1\r\nHost: exemple.fr:443\r\n\r\n",
                      16, 0]),
       False, False, TXT_TUNNEL, [CONN, TUNJ, FIN], (0, 0, 0, 2), None, [443], [HOTE], 1),
    Sc("cible mal formée (autorité nue hors CONNECT) → 400 (E1)",
       b"GET foo HTTP/1.1\r\nHost: exemple.fr\r\n\r\n",
       ScriptR2(recv=[b"GET foo HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"]),
       False, False, TXT_400, [CONN, FIN], (0, 0, 0, 1), None, [], [], 0),
    Sc("tête > 8192 → 431 (E3)",
       b"GET /" + b"A" * 8197 + b" HTTP/1.1\r\nHost: h\r\n\r\n",
       ScriptR2(recv=[b"GET /" + b"A" * 8197 + b" HTTP/1.1\r\nHost: h\r\n\r\n"]),
       False, False, TXT_431, [CONN, FIN], (0, 0, 0, 1), None, [], [], 0),
    Sc("Transfer-Encoding: chunked → 501 refus honnête (E4, périmètre M3)",
       b"GET /x HTTP/1.1\r\nHost: exemple.fr\r\nTransfer-Encoding: chunked\r\n\r\n",
       ScriptR2(recv=[b"GET /x HTTP/1.1\r\nHost: exemple.fr\r\n"
                      b"Transfer-Encoding: chunked\r\n\r\n"]),
       False, False, TXT_501, [CONN, FIN], (0, 0, 0, 1), None, [], [], 0),
    Sc("POST sans Content-Length → 411 (E5)",
       b"POST /x HTTP/1.1\r\nHost: exemple.fr\r\n\r\n",
       ScriptR2(recv=[b"POST /x HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"]),
       False, False, TXT_411, [CONN, FIN], (0, 0, 0, 1), None, [], [], 0),
    Sc("HTTP/2.0 → 505 (E6, version non supportée)",
       b"GET /x HTTP/2.0\r\nHost: exemple.fr\r\n\r\n",
       ScriptR2(recv=[b"GET /x HTTP/2.0\r\nHost: exemple.fr\r\n\r\n"]),
       False, False, TXT_505, [CONN, FIN], (0, 0, 0, 1), None, [], [], 0),
    Sc("amont injoignable (résolution) → 502 (E7)",
       GET_ABS, ScriptR2(gai=[0x2AFA], recv=[GET_ABS]),
       False, False, TXT_502, [CONN, FIN], (0, 0, 0, 1), None, [], [HOTE], 0),
    Sc("client parti en accumulation — fin SANS réponse (E8)",
       b"GET /x HTTP/1.1",
       ScriptR2(recv=[b"GET /x HTTP/1.1", 0]),
       False, False, b"", [CONN, FIN], (0, 0, 0, 1), None, [], [], 0),
    # --- le domaine TLS (V2b — la révision) ------------------------------------
    Sc("https SAIN — poignée 2 allers, un record, close_notify pur (P6/Q2')",
       GET_HTTPS, ScriptR2(isc=[(CONT, 64), (OK, 32)],
                            recv=[GET_HTTPS, 128, 121, 21],
                            dm=[(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)]),
       True, True, clair_dm(0, 100), [CONN, ETABLI, FIN], (1, 1, 1, 2),
       (HOTE, 443, REQUETE_R), [443], [HOTE], 0),
    Sc("https CERTIFICAT invalide — I4+Q3' : ligne console UNE fois (tls-08 "
       "seul) + 502 ÉTIQUETÉE au client",
       GET_HTTPS, ScriptR2(isc=[(CERT_INVALIDE, 0)], recv=[GET_HTTPS]),
       True, True, L.TXT_502_CERT, [CONN, CERTL, FIN], (1, 1, 1, 2),
       (HOTE, 443, REQUETE_R), [443], [HOTE], 0),
    Sc("https cible injoignable → verdict 7 → 502 GÉNÉRIQUE (Q3')",
       GET_HTTPS, ScriptR2(gai=[0x2AFA], recv=[GET_HTTPS]),
       True, True, TXT_502, [CONN, FIN], (0, 0, 0, 1),
       (HOTE, 443, REQUETE_R), [], [HOTE], 0),
    Sc("https verdict 5 à la poignée → 502 générique (« tunnel rompu »)",
       GET_HTTPS, ScriptR2(isc=[(INVALID_TOKEN, 0)], recv=[GET_HTTPS]),
       True, True, TXT_502, [CONN, FIN], (1, 1, 1, 2),
       (HOTE, 443, REQUETE_R), [443], [HOTE], 0),
    Sc("https port EXPLICITE 8443 — le défaut 443 n'écrase pas l'explicite",
       b"GET https://exemple.fr:8443/x HTTP/1.1\r\nHost: exemple.fr:8443\r\n\r\n",
       ScriptR2(isc=[(CONT, 64), (OK, 32)],
                recv=[b"GET https://exemple.fr:8443/x HTTP/1.1\r\n"
                      b"Host: exemple.fr:8443\r\n\r\n", 128, 121, 0],
                dm=[(OK, 5, 100, 16)]),
       True, True, clair_dm(0, 100), [CONN, ETABLI, FIN], (1, 1, 1, 2),
       (HOTE, 8443, b"GET /x HTTP/1.1\r\nHost: exemple.fr:8443\r\n\r\n"),
       [8443], [HOTE], 0),
    Sc("https altération en plein relais — E3 : réponse tronquée PROPRE puis 502",
       GET_HTTPS, ScriptR2(isc=[(CONT, 64), (OK, 32)],
                            recv=[GET_HTTPS, 128, 121],
                            dm=[(OK, 5, 100, 16), (ALTERE, 5, 100, 16)]),
       True, True, clair_dm(0, 100) + TXT_502, [CONN, ETABLI, FIN], (1, 1, 1, 2),
       (HOTE, 443, REQUETE_R), [443], [HOTE], 0),
    Sc("https + corps (CL > 0) → 501 refus honnête (ARRÊT D92 — le paquet "
       "porte UNE requête, miroir TE/E4)",
       b"POST https://exemple.fr/s HTTP/1.1\r\nHost: exemple.fr\r\n"
       b"Content-Length: 10\r\n\r\n0123456789",
       ScriptR2(recv=[b"POST https://exemple.fr/s HTTP/1.1\r\nHost: exemple.fr\r\n"
                      b"Content-Length: 10\r\n\r\n0123456789"]),
       True, False, TXT_501, [CONN, FIN], (0, 0, 0, 1), None, [], [], 0),
    Sc("« HTTPS:// » mal cassé → Q5 de http-08:R2 : le refus R1, AUCUNE "
       "tolérance nouvelle",
       b"GET HTTPS://exemple.fr/ HTTP/1.1\r\nHost: exemple.fr\r\n\r\n",
       ScriptR2(recv=[b"GET HTTPS://exemple.fr/ HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"]),
       True, False, TXT_501, [CONN, FIN], (0, 0, 0, 1), None, [], [], 0),
    Sc("« https:// » autorité vide → Q3 hérité : 400 (divergence 3→2 "
       "légitime, D91)",
       b"GET https:// HTTP/1.1\r\nHost: exemple.fr\r\n\r\n",
       ScriptR2(recv=[b"GET https:// HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"]),
       True, True, TXT_400, [CONN, FIN], (0, 0, 0, 1), None, [], [], 0),
    Sc("https verdict 6 exotique à la poignée → 502 (table TOTALE, E2)",
       GET_HTTPS, ScriptR2(isc=[(EXOTIQUE, 0)], recv=[GET_HTTPS]),
       True, True, TXT_502, [CONN, FIN], (1, 1, 1, 2),
       (HOTE, 443, REQUETE_R), [443], [HOTE], 0),
    Sc("https serveur ferme en relais (recv 0) → Q1 succès, réponse relayée",
       GET_HTTPS, ScriptR2(isc=[(CONT, 64), (OK, 32)],
                            recv=[GET_HTTPS, 128, 121, 0], dm=[(OK, 5, 100, 16)]),
       True, True, clair_dm(0, 100), [CONN, ETABLI, FIN], (1, 1, 1, 2),
       (HOTE, 443, REQUETE_R), [443], [HOTE], 0),
    Sc("émission cliente partielle — achèvement borné sur la 502 étiquetée "
       "(le témoin E8 de .emettre)",
       GET_HTTPS, ScriptR2(isc=[(CERT_INVALIDE, 0)], recv=[GET_HTTPS], send=[20]),
       True, True, L.TXT_502_CERT, [CONN, CERTL, FIN], (1, 1, 1, 2),
       (HOTE, 443, REQUETE_R), [443], [HOTE], 0),
]

# --- V4 : falsification (mutations d'un point, stables en taille) -----------------

MUTATIONS_V4 = [
    ("M1 verdict consigné à la dérive (+0x7010 → +0x7018 : le drapeau atterrit "
     "sur le compteur de réception — le canari y est lu, le routage meurt)",
     ("mov qword ptr [rsp + 0x7010], rax", "mov qword ptr [rsp + 0x7018], rax")),
    ("M2 port implicite TLS dévié (443 → 80 : la cible chiffrée serait jointe "
     "en clair)",
     ("mov r8d, 443", "mov r8d, 80")),
    ("M3 verdict cible TLS amnésié (cmp 4 → 5 : https tombe dans le refus 400)",
     ("cmp rax, 4", "cmp rax, 5")),
    ("M4 cadre TLS non vierge (0x184C → 0x184B : huit octets de canari "
     "survivent au rep stosq)",
     ("mov rcx, 0x184C", "mov rcx, 0x184B")),
    ("M5 verdict 3 remappé vers la ligne générique (l'entrée étiquetée "
     "devient muette)",
     ("je 0x7c57", "je 0x7c3c")),
    ("M6 socket du paquet déviée (rbx → r12 : r12 = 0 sur le chemin TLS, la "
     "socket serveur comme cliente)",
     ("mov qword ptr [rsp + 0x7128], rbx", "mov qword ptr [rsp + 0x7128], r12")),
    ("M7 hôte du paquet dévié (+0x6FA0 → +0x6FB0 : le champ PORT lu comme "
     "pointeur)",
     ("mov rax, qword ptr [rsp + 0x6FA0]", "mov rax, qword ptr [rsp + 0x6FB0]")),
    ("M8 dispatch post-réécriture inversé (jne → je : le chemin http ordinaire "
     "entre dans le tunnel)",
     ("jne 0x7a32", "je 0x7a32")),
    ("M9 garde corps TLS relâchée (r15 → r14 : la longueur de tête lue comme "
     "corps — tout https devient 501)",
     ("test r15, r15", "test r14, r14")),
    ("M10 probing du cadre élargi amputé d'une page (-0x13000 → -0x12000 : la "
     "leçon D63 désarmée — attrapée par V6bis)",
     ("cmp r10, -0x13000", "cmp r10, -0x12000")),
    ("M11 longueur de l'entrée étiquetée déviée (34 → 33 : la 502 certificat "
     "tronquée d'un octet)",
     ("mov r8, 34", "mov r8, 33")),
]

# --- V6bis : contrôle statique du prologue étendu + rejet I6' ---------------------

BLANCHE_I1 = {0x4140, 0x4180, 0x41C0, 0x4300, 0x4400, 0x4B00, 0x4C00, 0x4C80,
              0x4F40, 0x5080, 0x5140, 0x5200, 0x54C0,      # héritage M2/M3 (I1)
              0x6D40,                                        # tls-08 (Q2')
              0x7340}                                        # http-08:R2 (la révision appelée)


def controle_statique(lignes: list[str], rva: int, slot: int, brut: str = "") -> list[str]:
    """brut = le fichier de notation ENTIER (commentes compris) — la liste des
    déplacements RIP de l'en-tête porte la résolution de l'appel IAT."""
    problemes: list[str] = []
    debut = lignes[:12]
    texte = "\n".join(debut)
    # Q0 hérité (D63) étendu au cadre 0x13390 (D92) : boucle + touche finale + sub
    if not re.search(r"mov r10, (0xfffffffffffff000|-0x1000)", texte):
        problemes.append("prologue : init du probing absente")
    if "mov rax, qword ptr [rsp + r10]" not in texte:
        problemes.append("prologue : touche de boucle absente")
    if "sub r10, 0x1000" not in texte or "cmp r10, -0x13000" not in texte:
        problemes.append("prologue : bornes de la boucle de probing fautives")
    if not re.search(r"jge 0x[0-9a-f]+", texte):
        problemes.append("prologue : retour de boucle absent")
    if "mov rax, qword ptr [rsp - 0x13390]" not in texte:
        problemes.append("prologue : touche finale du bas de cadre absente")
    if "sub rsp, 0x13390" not in texte:
        problemes.append("prologue : cadre de session 0x13390 absent")
    # I6' : appels directs ⊆ liste blanche + étiquettes internes du slot
    internes = lambda c: rva <= c < rva + slot
    for ligne in lignes:
        m = re.match(r"^call (0x[0-9a-f]+)$", ligne)
        if m:
            cible = int(m.group(1), 16)
            if cible not in BLANCHE_I1 and not internes(cible):
                problemes.append(f"appel direct hors liste blanche : 0x{cible:x}")
                break
    iat = [ligne for ligne in lignes if ligne.startswith("call qword ptr")]
    if len(iat) != 1:
        problemes.append(f"{len(iat)} appels IAT != 1 (CloseHandle attendu)")
    elif "= 0x20f8" not in brut:
        problemes.append("l'appel IAT ne résout pas vers CloseHandle @0x20F8")
    return problemes


# --- main -------------------------------------------------------------------------

def charger(ks: Ks) -> dict:
    """V1 : round-trip de la révision + les vingt-huit blocs intégrés."""
    blobs: dict = {}
    TAILLES_M0 = {"hello-02-write": 27}
    INTEGRATIONS = [
        ("http-10-session-r2", RVA_SESSION_R2, None, "http-10-R2"),
        ("http-08-cible-r2", 0x7340, None, "http-08-R2"),
        ("tls-01-nom-utf16", 0x6000, None, "tls-01"),
        ("tls-02-verdicts", 0x6080, None, "tls-02"),
        ("tls-03-jetons", 0x6180, None, "tls-03"),
        ("tls-04-poignee", 0x62C0, None, "tls-04"),
        ("tls-05-cles", 0x65C0, None, "tls-05"),
        ("tls-06-emission", 0x6740, None, "tls-06"),
        ("tls-07-reception", 0x6A40, None, "tls-07"),
        ("tls-08-session", 0x6D40, None, "tls-08"),
        ("tcp-03-recv", 0x4140, os.path.join(ICI, os.pardir, "m2", "notation"), "tcp-03"),
        ("tcp-04-send", 0x4180, os.path.join(ICI, os.pardir, "m2", "notation"), "tcp-04"),
        ("tcp-05-close", 0x41C0, os.path.join(ICI, os.pardir, "m2", "notation"), "tcp-05"),
        ("tcp-06-spawn", 0x4300, os.path.join(ICI, os.pardir, "m2", "notation"), "tcp-06"),
        ("tcp-11-journal", 0x4B00, os.path.join(ICI, os.pardir, "m2", "notation"), "tcp-11"),
        ("tcp-13-connexion", 0x4400, os.path.join(ICI, os.pardir, "m3", "notation"), "tcp-13"),
        ("http-01-ligne", 0x4C00, os.path.join(ICI, os.pardir, "m3", "notation"), "http-01"),
        ("http-02-requete", 0x4C80, os.path.join(ICI, os.pardir, "m3", "notation"), "http-02"),
        ("http-03-entete", 0x4E80, os.path.join(ICI, os.pardir, "m3", "notation"), "http-03"),
        ("http-04-chercher", 0x4F40, os.path.join(ICI, os.pardir, "m3", "notation"), "http-04"),
        ("http-05-nombre", 0x5080, os.path.join(ICI, os.pardir, "m3", "notation"), "http-05"),
        ("http-06-tete", 0x5140, os.path.join(ICI, os.pardir, "m3", "notation"), "http-06"),
        ("http-07-autorite", 0x5200, os.path.join(ICI, os.pardir, "m3", "notation"), "http-07"),
        ("http-08-cible", 0x5380, os.path.join(ICI, os.pardir, "m3", "notation"), "http-08-R1"),
        ("http-09-pompe", 0x54C0, os.path.join(ICI, os.pardir, "m3", "notation"), "http-09"),
        ("http-10-session", RVA_SESSION_R1, os.path.join(ICI, os.pardir, "m3", "notation"),
         "http-10-R1"),
        ("libc-01-memcpy", 0x1100, os.path.join(ICI, os.pardir, "m1", "notation"), "libc-01"),
        ("libc-03-strlen", 0x1200, os.path.join(ICI, os.pardir, "m1", "notation"), "libc-03"),
        ("libc-04-itoa", 0x1280, os.path.join(ICI, os.pardir, "m1", "notation"), "libc-04"),
        ("libc-07-memset", 0x13C0, os.path.join(ICI, os.pardir, "m1", "notation"), "libc-07"),
        ("hello-02-write", 0x1040, os.path.join(ICI, os.pardir, "m0", "notation"), "hello-02"),
    ]
    for bloc, rva, chemin, cle in INTEGRATIONS:
        chemin_bloc = os.path.join(chemin, bloc + ".asm") if chemin else None
        b, d = octets_notation(ks, bloc, rva, chemin=chemin_bloc)
        blobs[cle] = b
        attendu = TAILLES_M0.get(bloc, d)
        controle(f"{bloc} == taille déclarée", attendu is not None and len(b) == attendu,
                 f"{len(b)} o")
    blob_r2, declare = octets_notation(ks, "http-10-session-r2", RVA_SESSION_R2)
    controle("http-10-session-r2 : padding du slot >= 16 (D8)",
             declare is not None and SLOT_R2 - len(blob_r2) >= 16,
             f"{SLOT_R2 - len(blob_r2)} o")
    return blobs


def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261028)
    args = parseur.parse_args()

    print("=== harnais_session_r2.py — http-10:R2 (D92 : routage TLS + table Q3') ===")
    print(f"graine {args.graine} · intégration : 29 blocs réels + l'ancêtre scellé "
          "(http-10:R3 @0x5580 + http-08:R1 @0x5380)")

    ks = Ks(KS_ARCH_X86, KS_MODE_64)

    print("\n[V1] round-trip de notation")
    blobs = charger(ks)

    emu_r2 = EmulateurSession(blobs, RVA_SESSION_R2, CADRE_R2)
    emu_r1 = EmulateurSession(blobs, RVA_SESSION_R1, CADRE_R1)

    print("\n[V2] oracle à scénarios + différentiel d'ancêtre — réponse exacte, "
          "lignes console, comptage, paquet P6, cadre VIERGE")
    for sc in SCENARIOS:
        problemes = jouer(emu_r2, sc)
        problemes += differentiel(emu_r1, emu_r2, sc)
        controle(f"scénario « {sc.nom} »", not problemes,
                 "; ".join(problemes[:3]) if problemes
                 else f"{len(emu_r2.appels)} appels, comptes "
                      f"{compter_compensation(emu_r2.appels)}")

    print("\n[V3] NON APPLICABLE — spec http-10:R2:V3 : la session reste hors fuzz "
          "direct (héritage M3 des orchestrateurs)")
    controle("V3 écarté conformément à la spécification (traçabilité)", True)

    print("\n[V4] falsification — onze mutations d'un point, chacune attrapée")
    for nom, mutation in MUTATIONS_V4:
        blob_m, _ = octets_notation(ks, "http-10-session-r2", RVA_SESSION_R2, mutation)
        blobs_m = dict(blobs)
        blobs_m["http-10-R2"] = blob_m
        emu_m = EmulateurSession(blobs_m, RVA_SESSION_R2, CADRE_R2)
        attrapes = 0
        for sc in SCENARIOS:
            try:
                if jouer(emu_m, sc):
                    attrapes += 1
            except Exception:
                attrapes += 1          # faute d'exécution = écart nommé
        # les mutations du prologue relèvent du contrôle statique (V6bis)
        lignes_m = lignes_notation(os.path.join(ICI, "notation", "http-10-session-r2.asm"))
        avant, _apres = mutation
        cibles = [i for i, l in enumerate(lignes_m) if avant in l]
        if cibles:
            lignes_m[cibles[0]] = lignes_m[cibles[0]].replace(avant, _apres)
        with open(os.path.join(ICI, "notation", "http-10-session-r2.asm"),
                  encoding="utf-8") as f:
            brut_m = f.read()
        if controle_statique(lignes_m, RVA_SESSION_R2, SLOT_R2, brut_m):
            attrapes += 1
        controle(f"mutation « {nom} » ATTRAPÉE", attrapes > 0,
                 f"{attrapes} armes en écart")
    emu_t = EmulateurSession(blobs, RVA_SESSION_R2, CADRE_R2)
    verts = sum(1 for sc in SCENARIOS if not jouer(emu_t, sc))
    controle("témoin intact : VERT sur les mêmes scénarios", verts == len(SCENARIOS),
             f"{verts}/{len(SCENARIOS)}")

    print("\n[V6bis] contrôle statique — prologue étendu (Q0/D63) + rejet I6'")
    chemin_notation = os.path.join(ICI, "notation", "http-10-session-r2.asm")
    lignes = lignes_notation(chemin_notation)
    with open(chemin_notation, encoding="utf-8") as f:
        brut = f.read()
    problemes = controle_statique(lignes, RVA_SESSION_R2, SLOT_R2, brut)
    controle("prologue : probing -0x1000..-0x13000, touche [rsp-0x13390], "
             "sub rsp, 0x13390 ; I6' : appels ⊆ liste blanche, un seul IAT "
             "(CloseHandle)", not problemes, "; ".join(problemes))

    print("\n" + "=" * 70)
    print(f"BILAN : {len(REUSSITES)} PASS, {len(ECHECS)} ÉCHEC")
    for nom in ECHECS:
        print(f"  FAIL {nom}")
    print("=" * 70)
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main())
