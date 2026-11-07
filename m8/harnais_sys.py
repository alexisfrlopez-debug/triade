#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_sys.py — Harnais à propriétés du domaine sys (M8-(b), D161).

Les blocs notés-mesurés-prouvés du jalon M8 sur FIXTURES ntdll synthétiques
(le modèle différentiel M4/M5 — le laboratoire Linux ne possède aucun vrai
ntdll et n'en prétend aucun : le VRAI se lira au terrain, chantier (d),
modèle m6d/m7d). Le harnais émule les octets des NOTATIONS (ce que
build_m8.py embarquera au chantier (c)) à leurs RVA .text5 ARRÊTÉS D161
(sys-01 @0xA000, sys-02 @0xA040, sys-03 @0xA180), memcmp libc-02 (b20002,
l'héritage scellé M1) à 0x1180 et hello-02 (a10002, le scellé M0) à 0x1040
pour le différentiel.

Vecteurs (les specs m8/I/sys-0{1,2,3}:

  V1  round-trip de notation 100 % (machinerie m4 D158 — assemble,
      désassemble, compare, réassemble) + CONCORDANCE DES IMMUABLES : chaque
      immédiat de la notation re-contrôlé contre m8/layout.py (la source
      unique — la fenêtre e_lfanew, MOTIF_PE, les décalages EAT, MOTIF_STUB
      en dword, OFF_SSN, les longueurs des fixtures, les cibles d'appels) ;

  V2  l'épreuve à shims sur FIXTURES ntdll synthétiques :
      sys-01 — le trombone : le noyau simulé (hook UC_X86_INS_SYSCALL)
      constate le remappage rcx→r10, le SSN TRANSMIS TEL QUEL en rax (I2),
      les arguments de pile lus à [rsp+0x28] AU MOMENT du syscall (I3 : la
      pile de l'APPELANT est la pile du syscall — canaris au-dessus et
      en-dessous), le site UNIQUE (Q1), le NTSTATUS rendu tel quel (Q2),
      rcx/r11 détruits (Q3), SIX octets exacts, aucun prologue, aucun IAT ;
      sys-02 — le résolveur : les SIX verdicts nommés sur fixtures hostiles
      (-5 span, -2 pas PE / e_lfanew fou, -3 export absente, -1 marche
      complète, -4 stub crocheté) et le succès (SSN exact, rdx = l'adresse
      du stub — Q2) ; I1 la marche BORNÉE (NumberOfNames lu UNE fois —
      traceur de lectures), I4 AUCUN syscall émis (compteur), I7 non-volatils
      sentinelles, I8 AUCUNE écriture dans le module lu (empreinte de
      l'image avant/après + traceur d'écritures) ;
      sys-03 — LA TWIN AU DIFFÉRENTIEL : hello-02 émulé (WriteFile par
      l'IAT, mécanisme M2/M3 du trampoline) émet LA MÊME LIGNE que sys-03
      (NtWriteFile en syscall direct) — octet pour octet le fixture M0 ;
      les NEUF arguments vérifiés au noyau simulé (Q3), le SSN résolu AU
      GESTE MÊME (deux fixtures à SSN distincts, suite — Q2), I3 l'ordre
      résoudre-puis-émettre (structure), I5 échec de résolution = AUCUN
      syscall (compteur), -6 le STATUS non nul consigné en rdx, -6 la
      divergence iosb (le noyau ne parle pas deux fois), I6 non-volatils ;
  V2d/e/f  LE SOCLE SOCKET (chantier M9-(d)) sur FIXTURES AFD
      SYNTHÉTIQUES — le noyau simulé devient AFD STRICT : chaque geste
      transport VALIDE ses arguments contre le plan (la séquence MESURÉE
      mswsock, les VECTEURS DORÉS, l'erratum n° 10 au receive — LE
      TERRAIN A JUGÉ LA MESURE : TDI_RECEIVE_NORMAL 0x20 vit en TdiFlags,
      le 0x20 en AfdFlags serait REFUSÉ par le VRAI noyau — la notation
      suit LE TERRAIN, la mesure WinDbg citée serait REFUSÉE) : sys-04
      — create + bind WILDCARD + connect (la marche, les ONZE/DIX
      arguments, le handle en LOCALE posé à [P3] au succès SEULEMENT,
      Q4 : au -6 AUCUNE possession partielle — le canari de P3 le
      constate aux TROIS étages d'échec), la résolution double de
      « NtDeviceIoControlFile » (deux fixtures à SSN distincts — Q3),
      l'ordre create→bind→connect relu (I6) ; sys-05 — TOTALE ou refus
      -7 (le compteur du IOSB), AUCUNE COPIE (le noyau LIT chez le kit,
      le WSABUF pointe LA CHARGE du kit, jamais le cadre), -5/-1/-6
      nommés ; sys-06 — n ≥ 1 ou LA DEMI-FIN -7 (le zéro du pair), le
      noyau ÉCRIT chez le kit (I8 : le reçu INTÈGRE, les canaris au-delà
      de n intacts), STATUS_CONNECTION_RESET consigné (Q5) ;

  V3  fuzzing à propriétés : modules aléatoires en graine (noms, SSN,
      ordinals permutés, préfixes pièges, stubs crochetés, e_lfanew
      hostiles, cible en dernière position, doublons) — le MODÈLE (dérivé
      de la couche I et du plan, JAMAIS des octets de la notation) prédit
      le verdict, l'émulation confrontée ; l'intégrité du module et les
      non-volatils re-contrôlés à CHAQUE cas ; LE TRANSPORT EN SUITE :
      modules et comportements noyau aléatoires, le modèle marche la
      séquence create→bind→connect (chaque étage : succès | STATUS |
      divergence) et les verdicts d'émission/réception (TOTALE | partielle
      | zéro | STATUS), sys-05/06 confrontés verdict par verdict ;

  V4  falsification : les mutations D'UN SEUL point de chaque notation
      (stables en taille — leçon D82) doivent être ATTRAPÉES par le
      différentiel ; le témoin intact reste VERT — une suite qui ne peut
      pas échouer ne prouve rien. LE SOCLE EN SUITE : l'erratum n° 10
      falsifié DANS LES DEUX SENS (0→0x20 en AfdFlags — la mesure WinDbg
      rétablie, REFUSÉE par le VRAI noyau — et 0x20→0 en TdiFlags au
      receive : LE TERRAIN est la seule écriture qui passe le noyau
      strict), les IOCTL échangés, le sockaddr décalé, la garde
      span inversée, la demi-fin masquée (jz→jnz) — chaque mutante trahit
      la batterie.

Usage : python3 harnais_sys.py [--graine G] [--volume complet|reduit]
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import random
import re
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
M4_DIR = os.path.join(ICI, os.pardir, "m4")
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, "outils"))
sys.path.insert(0, M4_DIR)
sys.path.insert(0, os.path.join(M4_DIR, "outils"))

# Le plan M8 chargé par CHEMIN NOMINATIF (leçon D158 : m4/layout.py est
# devant au sys.path pour build_m4 — jamais d'import anonyme ici). En mode
# BUILD (le module build_m8 importe le harnais), le plan est DÉJÀ chargé
# sous ce nom : RÉUTILISÉ, jamais re-exécuté (une seule instance).
if "layout_m8" in sys.modules:
    L = sys.modules["layout_m8"]
else:
    _spec_l8 = importlib.util.spec_from_file_location(
        "layout_m8", os.path.join(ICI, "layout.py"))
    L = importlib.util.module_from_spec(_spec_l8)
    sys.modules["layout_m8"] = L
    _spec_l8.loader.exec_module(L)

# La machinerie de notation de la lignée, importée par chemin (leçon D158 :
# les build.py homonymes se chargent par importlib, jamais par sys.path) —
# réutilisée si build_m8 l'a déjà chargée (une seule instance du builder).
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
from unicorn import (Uc, UcError, UC_ARCH_X86, UC_MODE_64,  # noqa: E402
                     UC_HOOK_CODE, UC_HOOK_INSN, UC_HOOK_MEM_READ,
                     UC_HOOK_MEM_WRITE)
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX,  # noqa: E402
                               UC_X86_REG_RDX, UC_X86_REG_RSI, UC_X86_REG_RDI,
                               UC_X86_REG_RBP, UC_X86_REG_RSP, UC_X86_REG_R8,
                               UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11,
                               UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14,
                               UC_X86_REG_R15, UC_X86_REG_RIP, UC_X86_INS_SYSCALL)

REGS = {"rax": UC_X86_REG_RAX, "rbx": UC_X86_REG_RBX, "rcx": UC_X86_REG_RCX,
        "rdx": UC_X86_REG_RDX, "rsi": UC_X86_REG_RSI, "rdi": UC_X86_REG_RDI,
        "rbp": UC_X86_REG_RBP, "rsp": UC_X86_REG_RSP, "r8": UC_X86_REG_R8,
        "r9": UC_X86_REG_R9, "r10": UC_X86_REG_R10, "r11": UC_X86_REG_R11,
        "r12": UC_X86_REG_R12, "r13": UC_X86_REG_R13, "r14": UC_X86_REG_R14,
        "r15": UC_X86_REG_R15}

# --- La mémoire du harnais (émulation nue à les RVA du plan, mécanisme D79) ------

ZONE_CODE = (0x1000, 0x11000)    # .text/.rdata/.data/.text2-4/.text5 du plan
                                   # + .text6 (les fixtures transport du
                                   # socle, M9-(d) — jusqu'à 0x10CF0, borne)
MODULE_BASE = 0x150000000         # le module ntdll synthétique (page exacte)
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP0 = 0x7F008000
RET_MAGIQUE = 0xBF00              # arrêt propre (hlt, dans la réserve .text5)
TRAMPOLINE_WF = 0xBF10            # la fausse WriteFile (mécanisme M2/M3)

HANDLE_MAGIQUE = 0x0000ABCD       # le handle d'écriture des deux chemins
STATUS_INVALIDE = 0xC000001C      # STATUS_INVALID_SYSTEM_SERVICE (SSN inconnu)

# --- LE SOCLE SOCKET (chantier M9-(d)) : le ntdll et l'AFD simulés -------------
SSN_NT_CREATEFILE = 0x55          # le SSN de « NtCreateFile » du fixture
SSN_NT_IOCTL = 0x56               # le SSN de « NtDeviceIoControlFile »
HANDLE_AFD = 0x0000BEEF           # le handle d'endpoint posé au create
STATUS_PARAM_INVALIDE = 0xC000000D   # STATUS_INVALID_PARAMETER (le noyau
STATUS_ACCES_REFUSE = 0xC0000022      # strict refuse l'argument divergent)
STATUS_CNX_REINIT = 0xC000013C    # STATUS_CONNECTION_RESET (sys-06:Q5 — le
                                   # pair a coupé BRUTALEMENT)
KIT_SOCKADDR = RSP0 - 0x800       # le sockaddr_in DU KIT (16 o — P2)
KIT_CELLULE = RSP0 - 0x700        # la cellule u64 du handle CHEZ LE KIT (P3)
KIT_CHARGE = RSP0 + 0x2000        # la zone charge du kit (sys-05 — P3)
KIT_TAMPON = RSP0 + 0x4000        # la zone tampon du kit (sys-06 — P3)

SENTINELLES_NV = {
    "rbx": 0x1212121212121212, "rbp": 0x2323232323232323,
    "rdi": 0x3434343434343434, "rsi": 0x4545454545454545,
    "r12": 0x5656565656565656, "r13": 0x6767676767676767,
    "r14": 0x7878787878787878, "r15": 0x8989898989898989,
}

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


# --- Le forgeur de modules ntdll synthétiques ------------------------------------
# PE32+ minimal MAIS BIEN FORMÉ (P3 de sys-02 : c'est « ntdll » — les
# pointeurs EAT sont cohérents par construction ; l'hostilité vit dans les
# noms, les stubs, les bornes et la signature — jamais dans des pointeurs
# fous qui crasheraient au lieu de se faire REFUSER).

class ModuleFixe:
    """Un module PE32+ synthétique + sa carte (RVA → sens)."""

    def __init__(self, octets: bytes, dir_export_rva: int, noms: dict,
                 taille: int):
        self.octets = octets
        self.taille = taille                # la taille mappée (page exacte)
        self.dir_export_rva = dir_export_rva
        self.noms = noms                    # nom -> {ordinal, stub_rva, ssn}

    def empreinte(self) -> str:
        return hashlib.sha256(self.octets).hexdigest()[:16]


def forger_module(noms_ssns: list[tuple[str, int]] | None = None,
                  e_lfanew: int = 0x80,
                  sig_pe: bool = True,
                  export_absente: bool = False,
                  stub_trop: str | None = None) -> ModuleFixe:
    """Forge un module : les noms donnés (nom, ssn) ; stub_trop = un nom dont
    le stub est CROCHETÉ (le motif diverge — le hook) ; e_lfanew/sig_pe/
    export_absente = les hostiletés structurelles (verdicts -2/-3). Toutes
    les zones DÉRIVENT de e_lfanew (l'en-tête optionnel porte
    DataDirectory[0] à PE+0x88 : jamais de collision, quelle que soit la
    fenêtre — leçon de la graine 424242 : un répertoire export FIXE à 0x200
    écrasait l'entrée pour e_lfanew ∈ [0x178, 0x1A0])."""
    noms_ssns = noms_ssns or []
    TAILLE = 0x1000
    img = bytearray(b"\x00" * TAILLE)

    def pose(rva: int, donnees: bytes):
        img[rva:rva + len(donnees)] = donnees

    # DOS : « MZ » + e_lfanew (E_LFANEW 0x3C)
    pose(0x00, b"MZ")
    pose(L.E_LFANEW, struct.pack("<I", e_lfanew))
    # PE : signature + COFF (machine AMD64, 0 sections) + optionnel PE32+ nul
    pe = e_lfanew if sig_pe else e_lfanew + 0x40
    pose(pe, L.MOTIF_PE)
    pose(pe + 4, struct.pack("<HHIIIHH", 0x8664, 0, 0, 0, 0, 0x00F0, 0))
    pose(pe + 0x18, struct.pack("<H", 0x20B))       # magic PE32+
    # les zones de données dérivées de e_lfanew (aucune collision possible)
    zone = max(0x200, pe + 0xB0)
    export_rva = zone                        # le répertoire export VIT dans la zone
    rva_fonctions, rva_tbl_noms, rva_ord = zone + 0x100, zone + 0x180, zone + 0x1C0
    rva_blob, rva_stubs = zone + 0x200, zone + 0x400
    assert rva_stubs + 16 * max(len(noms_ssns), 1) <= TAILLE
    if export_absente:                       # l'hostilité -3 : RIEN de posé
        pose(pe + L.OFF_EXPORT_RVA, struct.pack("<I", 0))
        pose(pe + L.OFF_EXPORT_TAILLE, struct.pack("<I", 0))
        return ModuleFixe(bytes(img), 0, {}, TAILLE)

    # le répertoire export (l'entrée DataDirectory[0] POINTE la zone)
    pose(pe + L.OFF_EXPORT_RVA, struct.pack("<I", export_rva))
    pose(pe + L.OFF_EXPORT_TAILLE, struct.pack("<I", 0x40))

    # le répertoire export
    nb = len(noms_ssns)
    dir_exp = bytearray(b"\x00" * 0x28)
    struct.pack_into("<I", dir_exp, 0x0C, 0)            # base = 0 (RVAs nus)
    struct.pack_into("<I", dir_exp, L.EXP_NBFONC, max(nb, 1))
    struct.pack_into("<I", dir_exp, L.EXP_NBNOMS, nb)
    struct.pack_into("<I", dir_exp, L.EXP_ADRFONC, rva_fonctions)
    struct.pack_into("<I", dir_exp, L.EXP_ADRNOMS, rva_tbl_noms)
    struct.pack_into("<I", dir_exp, L.EXP_ADRORD, rva_ord)
    pose(export_rva, bytes(dir_exp))

    # les trois tables + les noms + les stubs
    fonctions, tbl_noms, ordinals = [], [], []
    carte: dict = {}
    blob_noms = bytearray()
    for i, (nom, ssn) in enumerate(noms_ssns):
        rva_nom = rva_blob + len(blob_noms)
        blob_noms += nom.encode("ascii") + b"\x00" + b"\x00" * (64 - len(nom) - 1)
        tbl_noms.append(rva_nom)
        ordinals.append(i)
        stub_rva = rva_stubs + i * 0x10
        fonctions.append(stub_rva)
        motif = L.MOTIF_STUB if nom != stub_trop else b"\x48\xB8\x90\x90\x90\x90"
        pose(stub_rva, motif + struct.pack("<I", ssn))
        carte[nom] = {"ordinal": i, "stub_rva": stub_rva, "ssn": ssn,
                      "crochete": nom == stub_trop}
    for i, rva in enumerate(fonctions):
        pose(rva_fonctions + i * 4, struct.pack("<I", rva))
    for i, rva in enumerate(tbl_noms):
        pose(rva_tbl_noms + i * 4, struct.pack("<I", rva))
    for i, o in enumerate(ordinals):
        pose(rva_ord + i * 2, struct.pack("<H", o))
    pose(rva_blob, bytes(blob_noms))
    return ModuleFixe(bytes(img), export_rva, carte, TAILLE)


# --- Le modèle (dérivé de la couche I et du plan — JAMAIS de la notation) --------

def modele_resoudre(module: ModuleFixe, span: bytes | None):
    """Le résolveur de la SPÉCIFICATION : (verdict, ssn, stub_va_absolu)."""
    if not span:                                   # P1/P2 — le span invalide
        return L.V_SPAN_INVALIDE, None, None
    base = MODULE_BASE
    e_lfanew = struct.unpack_from("<I", module.octets, L.E_LFANEW)[0]
    if not (L.E_LFANEW_MIN <= e_lfanew <= L.E_LFANEW_MAX):
        return L.V_PAS_MODULE, None, None
    if module.octets[e_lfanew:e_lfanew + 4] != L.MOTIF_PE:
        return L.V_PAS_MODULE, None, None
    pe = base + e_lfanew
    dir_rva = struct.unpack_from(
        "<I", module.octets, e_lfanew + L.OFF_EXPORT_RVA)[0]
    if dir_rva == 0:
        return L.V_EAT_ABSENTE, None, None
    d = base + dir_rva
    nb = struct.unpack_from("<I", module.octets, dir_rva + L.EXP_NBNOMS)[0]
    adr_noms = struct.unpack_from("<I", module.octets, dir_rva + L.EXP_ADRNOMS)[0]
    adr_ord = struct.unpack_from("<I", module.octets, dir_rva + L.EXP_ADRORD)[0]
    adr_fon = struct.unpack_from("<I", module.octets, dir_rva + L.EXP_ADRFONC)[0]
    for i in range(nb):                            # I1 : la marche BORNÉE
        rva_nom = struct.unpack_from("<I", module.octets, adr_noms + i * 4)[0]
        candidat = module.octets[rva_nom:rva_nom + len(span)]
        if candidat == span:                       # libc-04… libc-02 (erratum)
            o = struct.unpack_from("<H", module.octets, adr_ord + i * 2)[0]
            stub_rva = struct.unpack_from("<I", module.octets, adr_fon + o * 4)[0]
            stub_va = base + stub_rva
            motif = module.octets[stub_rva:stub_rva + 4]
            if motif != L.MOTIF_STUB:              # I3 : le motif AVANT l'imm32
                return L.V_STUB_DIVERGENT, None, None
            ssn = struct.unpack_from("<I", module.octets, stub_rva + L.OFF_SSN)[0]
            return L.V_RESOLU, ssn, stub_va
    return L.V_NOM_ABSENT, None, None              # la marche COMPLÈTE


# --- Le noyau simulé (le hook syscall paramétrable) -------------------------------

class Noyau:
    """Le noyau Windows simulé : la table des SSN connus, les captures."""

    def __init__(self):
        self.dispatch: dict[int, callable] = {}
        self.captures: list[dict] = []
        self.lignes_emises: list[bytes] = []

    def hook(self, uc: Uc, _data):
        rip = uc.reg_read(UC_X86_REG_RIP)
        rsp = uc.reg_read(UC_X86_REG_RSP)

        def pile(off: int) -> int:
            return struct.unpack("<Q", uc.mem_read(rsp + off, 8))[0]

        args = {
            "ssn": uc.reg_read(UC_X86_REG_RAX),
            "handle": uc.reg_read(UC_X86_REG_R10),     # le remappé de rcx
            "arg2": uc.reg_read(UC_X86_REG_RDX),
            "arg3": uc.reg_read(UC_X86_REG_R8),
            "arg4": uc.reg_read(UC_X86_REG_R9),
            "arg5": pile(0x28), "arg6": pile(0x30), "arg7": pile(0x38),
            "arg8": pile(0x40), "arg9": pile(0x48), "arg10": pile(0x50),
            "arg11": pile(0x58),
            "rsp": rsp, "ret": pile(0x00),
        }
        self.captures.append(args)
        ssn = args["ssn"]
        if ssn in self.dispatch:
            self.dispatch[ssn](uc, args)               # le comportement du service
        else:
            uc.reg_write(UC_X86_REG_RAX, STATUS_INVALIDE)
        uc.reg_write(UC_X86_REG_RCX, rip + 2)          # le coup du noyau (Q3)
        uc.reg_write(UC_X86_REG_R11, 0x246)


# --- Les fixtures AFD RE-DÉRIVÉS (le juge est le code, jamais une copie) --------

def ea_deterministe() -> bytes:
    """Le EA complet DÉTERMINISTE du plan (54 o) : l'en-tête FILE_FULL_EA_
    INFORMATION (NextEntryOffset 0, Flags 0, EaNameLength 15, EaValueLength
    30 — la MESURE p.1), le nom « AfdOpenPacketXX\\0 », la valeur aux SIX
    DWORD du jalon (AF_INET/SOCK_STREAM/IPPROTO_TCP PORTÉS PAR LE EA —
    jamais des octets de code), la marge NULLE (la divergence MESURÉE :
    ws2_32 y laisse du bruit de pile qu'afd.sys ne lit pas — les nôtres
    NULS, le transport reproductible)."""
    entete = struct.pack("<IBBH", 0, 0, L.LEN_AFD_EA_NOM, L.AFD_EA_VALEUR)
    valeur = struct.pack("<6I", 0, 0, L.AF_INET, L.SOCK_STREAM,
                         L.IPPROTO_TCP, 0)
    return entete + L.AFD_EA_NOM + b"\x00" + valeur + b"\x00" * 6


def bind_wildcard() -> bytes:
    """Le bind IMPLICITE WILDCARD du plan (20 o) : flags AFD_WILDCARDADDRESS
    (le noyau DÉDUIT l'adresse source — jamais une adresse choisie par le
    domaine), le sockaddr sauvage AF_INET LE / port 0 / INADDR_ANY en
    BOUTISME RÉSEAU / sin_zero NUL (la divergence MESURÉE p.2 : le padding
    mswsock est du bruit SANS SIGNIFICATION)."""
    return (struct.pack("<I", L.AFD_BIND_WILDCARD)
            + struct.pack("<H", L.AF_INET)
            + struct.pack(">H", 0) + struct.pack(">I", 0) + b"\x00" * 8)


def sockaddr_kit(port: int = 80, adresse: bytes = bytes([192, 168, 1, 1])) -> bytes:
    """Le sockaddr_in DU KIT (16 o — P2 de sys-04) : family en BOUTISME
    MACHINE, port et adresse en BOUTISME RÉSEAU (charte § 9 : le format
    est celui de la structure Windows, le kit répond de son boutisme)."""
    return struct.pack("<H", L.AF_INET) + struct.pack(">H", port) \
        + adresse + b"\x00" * 8


# --- Le noyau AFD STRICT du socle (chantier M9-(d)) -------------------------------

class NoyauAFD:
    """Le noyau AFD simulé STRICT : chaque geste transport VALIDE ses
    arguments contre le plan (les VECTEURS DORÉS, la séquence MESURÉE
    mswsock, l'erratum AfdFlags 0x20 au receive) — une divergence est le
    refus STATUS_INVALID_PARAMETER ET un écart NOMMÉ (jamais muet : le
    témoin du harnais le relit). L'état (le handle, la poignée, les
    échanges) vit ICI chez le noyau — jamais chez le bloc (charte § 6)."""

    def __init__(self, noyau: Noyau):
        self.noyau = noyau
        self.reinit()

    def reinit(self):
        self.ecarts: list[str] = []
        self.modes = {"create": ("succes", 0), "bind": ("succes", 0),
                      "connect": ("succes", 0), "send": ("succes", None),
                      "recv": ("succes", 0)}
        self.handle = None            # posé au create — HANDLE_AFD
        self.poignee_etablie = False  # posée au connect réussi
        self.sockaddr_attendu = b""   # le kit pose, le noyau recoupe
        self.longueur_attendue = 0    # le WSABUF.len du send
        self.capacite_attendue = 0    # le WSABUF.len du receive
        self.charge_vue = 0           # le WSABUF.buf — CHEZ LE KIT (P3)
        self.emis = b""               # lu au send chez le kit
        self.recu_pose = b""          # écrit au receive chez le kit
        self.noyau_sabotage = 0       # l'adresse (VA) du nom à corrompre (le juge Q3)

    # petits lecteurs little-endian dans l'espace du bloc
    def _q(self, uc, adr, off=0):
        return struct.unpack("<Q", uc.mem_read(adr + off, 8))[0]

    def _d(self, uc, adr, off=0):
        return struct.unpack("<I", uc.mem_read(adr + off, 4))[0]

    def _w(self, uc, adr, off=0):
        return struct.unpack("<H", uc.mem_read(adr + off, 2))[0]

    # --- le geste create : les ONZE arguments contre le plan ----------------------

    def creer(self, uc, a):
        a["_geste"] = "create"
        if a["arg2"] != L.AFD_DESIRED_ACCESS:
            self.ecarts.append(f"DesiredAccess {a['arg2']:#x}")
        oa = a["arg3"]
        if self._d(uc, oa) != L.OBJECT_ATTRIBUTES_TAILLE:
            self.ecarts.append("OA.Length")
        if self._q(uc, oa, 8) != 0:
            self.ecarts.append("RootDirectory")
        us = self._q(uc, oa, 16)
        if self._w(uc, us) != L.LEN_AFD_DEVICE \
                or self._w(uc, us, 2) != L.LEN_AFD_DEVICE + 2:
            self.ecarts.append("UNICODE_STRING Length/MaximumLength")
        tampon = self._q(uc, us, 8)
        if tampon != L.R_SYS_DEVICE:
            self.ecarts.append(f"device-cible {tampon:#x}")
        elif bytes(uc.mem_read(tampon, L.LEN_AFD_DEVICE)) != L.TXT_AFD_DEVICE:
            self.ecarts.append("device-octets")
        if self._d(uc, oa, 24) != L.OBJ_CASE_INSENSITIVE:
            self.ecarts.append("Attributes")
        if self._q(uc, oa, 32) != 0 or self._q(uc, oa, 40) != 0:
            self.ecarts.append("SecurityDescriptor/QoS")
        if a["arg5"] != 0 or a["arg6"] != 0:
            self.ecarts.append("AllocationSize/FileAttributes")
        if a["arg7"] != L.AFD_SHARE_ACCESS:
            self.ecarts.append("ShareAccess")
        if a["arg8"] != L.AFD_CREATE_DISPOSITION:
            self.ecarts.append("CreateDisposition")
        if a["arg9"] != L.AFD_CREATE_OPTIONS:
            self.ecarts.append("CreateOptions")
        if a["arg10"] != L.R_SYS_EA:
            self.ecarts.append(f"EaBuffer {a['arg10']:#x}")
        elif bytes(uc.mem_read(L.R_SYS_EA, L.AFD_EA_TAILLE)) != ea_deterministe():
            self.ecarts.append("EA-octets")
        if a["arg11"] != L.AFD_EA_TAILLE:
            self.ecarts.append("EaLength")
        if self.ecarts:
            uc.mem_write(a["arg4"], struct.pack("<QQ", STATUS_PARAM_INVALIDE, 0))
            uc.reg_write(UC_X86_REG_RAX, STATUS_PARAM_INVALIDE)
            return
        mode, status = self.modes["create"]
        if mode == "succes":
            uc.mem_write(a["handle"], struct.pack("<Q", HANDLE_AFD))
            self.handle = HANDLE_AFD
            uc.mem_write(a["arg4"], struct.pack("<QQ", 0, 0))
            uc.reg_write(UC_X86_REG_RAX, 0)
        elif mode == "status":              # le STATUS non nul, JAMAIS muet
            uc.mem_write(a["arg4"], struct.pack("<QQ", status, 0))
            uc.reg_write(UC_X86_REG_RAX, status)
        elif mode == "divergence":           # rax 0, l'IOSB diverge
            uc.mem_write(a["handle"], struct.pack("<Q", HANDLE_AFD))
            self.handle = HANDLE_AFD
            uc.mem_write(a["arg4"], struct.pack("<QQ", status, 0))
            uc.reg_write(UC_X86_REG_RAX, 0)

    # --- les gestes ioctl : le dispatch de l'IOCTL, la validation par geste ------

    def ioctl(self, uc, a):
        a["_geste"] = "ioctl"
        code = a["arg6"]
        if code == L.IOCTL_AFD_BIND:
            return self._bind(uc, a)
        if code == L.IOCTL_AFD_CONNECT:
            return self._connect(uc, a)
        if code == L.IOCTL_AFD_SEND:
            return self._send(uc, a)
        if code == L.IOCTL_AFD_RECEIVE:
            return self._recv(uc, a)
        self.ecarts.append(f"IOCTL inconnu {code:#x}")
        uc.mem_write(a["arg5"], struct.pack("<QQ", STATUS_PARAM_INVALIDE, 0))
        uc.reg_write(UC_X86_REG_RAX, STATUS_PARAM_INVALIDE)

    def _garde_ioctl(self, uc, a):
        if self.handle is None:
            self.ecarts.append("ioctl-sans-handle (jamais bind sans handle — I6)")
        if a["handle"] != self.handle:
            self.ecarts.append(f"handle {a['handle']:#x} ≠ endpoint")
        if a["arg2"] != 0 or a["arg3"] != 0 or a["arg4"] != 0:
            self.ecarts.append("Event/ApcRoutine/ApcContext")

    def _garde_sans_sortie(self, uc, a):
        """connect/send/recv : AUCUNE sortie attendue (Q2 de sys-04 : « NULL
        pour le CONNECT » ; Q4 de sys-05/06) — la réponse est le IOSB. Le
        BIND SEUL a une sortie (16 o — jamais pour les autres)."""
        if a["arg9"] != 0 or a["arg10"] != 0:
            self.ecarts.append("OutputBuffer/Length")

    def _wsabuf(self, uc, a, attendu_len, attendu_buf, nom_len, nom_buf):
        """Le WSABUF CANONIQUE 16 o (len à +0, PADDING 4 o, buf à +8 — la
        Révision 2 des specs sys-05/sys-06, la MESURE de la sonde Entrée 185 :
        le noyau lit buf à +8) + l'AFD_*_INFO 24 o : BufferArray → le WSABUF,
        BufferCount 1, les drapeaux du plan."""
        info = a["arg7"]
        if a["arg8"] != L.AFD_SENDRECV_TAILLE:
            self.ecarts.append("AFD_INFO taille")
        wsabuf = self._q(uc, info)
        if self._d(uc, wsabuf) != attendu_len:
            self.ecarts.append(nom_len)
        if self._q(uc, wsabuf, 8) != attendu_buf:
            self.ecarts.append(nom_buf)
        self.charge_vue = self._q(uc, wsabuf, 8)
        if self._d(uc, info, 8) != 1:
            self.ecarts.append("BufferCount")
        return info

    def _refus_param(self, uc, a):
        uc.mem_write(a["arg5"], struct.pack("<QQ", STATUS_PARAM_INVALIDE, 0))
        uc.reg_write(UC_X86_REG_RAX, STATUS_PARAM_INVALIDE)

    def _bind(self, uc, a):
        self._garde_ioctl(uc, a)
        if a["arg7"] != L.R_SYS_BIND:
            self.ecarts.append(f"bind-buffer {a['arg7']:#x} (le fixture CITÉ — I3)")
        elif bytes(uc.mem_read(L.R_SYS_BIND, L.AFD_BIND_TAILLE)) != bind_wildcard():
            self.ecarts.append("bind-octets")
        if a["arg8"] != L.AFD_BIND_TAILLE:
            self.ecarts.append("bind-taille")
        if a["arg10"] != L.AFD_BIND_SORTIE:
            self.ecarts.append("bind-sortie-taille")
        if self.ecarts:
            return self._refus_param(uc, a)
        mode, status = self.modes["bind"]
        if mode == "succes":
            uc.mem_write(a["arg9"], b"\x00" * L.AFD_BIND_SORTIE)  # l'adresse DÉDUITE
            uc.mem_write(a["arg5"], struct.pack("<QQ", 0, 0))
            uc.reg_write(UC_X86_REG_RAX, 0)
        elif mode == "status":
            uc.mem_write(a["arg5"], struct.pack("<QQ", status, 0))
            uc.reg_write(UC_X86_REG_RAX, status)
        elif mode == "divergence":
            uc.mem_write(a["arg5"], struct.pack("<QQ", status, 0))
            uc.reg_write(UC_X86_REG_RAX, 0)
        elif mode == "sabotage":
            """Le geste 3 mis à l'épreuve : le module CHANGE sous les pieds
            du bloc (l'octet du nom corrompu PAR LE NOYAU — la mémoire vit)
            : la TROISIÈME résolution doit échouer -1, jamais un numéro en
            cache (Q3 — le sabotage est le juge de la résolution double)."""
            uc.mem_write(a["arg5"], struct.pack("<QQ", 0, 0))
            uc.reg_write(UC_X86_REG_RAX, 0)
            nom_rva = self.noyau_sabotage
            uc.mem_write(nom_rva, b"\xFF")

    def _connect(self, uc, a):
        self._garde_ioctl(uc, a)
        self._garde_sans_sortie(uc, a)
        j = a["arg7"]
        if a["arg8"] != L.AFD_CONNECT_TAILLE:
            self.ecarts.append("connect-taille")
        if self._q(uc, j) != 0 or self._q(uc, j, 8) != 0 \
                or self._q(uc, j, 16) != 0:
            self.ecarts.append("SanActive/Root/ConnectEndpoint (les zéros MESURÉS)")
        sockaddr_vu = bytes(uc.mem_read(j + 24, L.SOCKADDR_TAILLE))
        if sockaddr_vu != self.sockaddr_attendu:
            self.ecarts.append(f"sockaddr copié {sockaddr_vu.hex()} ≠ "
                               f"{self.sockaddr_attendu.hex()} (LU, jamais interprété — I4)")
        if self.ecarts:
            return self._refus_param(uc, a)
        mode, status = self.modes["connect"]
        if mode == "succes":
            self.poignee_etablie = True          # LA POIGNÉE EST ÉTABLIE
            uc.mem_write(a["arg5"], struct.pack("<QQ", 0, 0))
            uc.reg_write(UC_X86_REG_RAX, 0)
        elif mode == "status":
            uc.mem_write(a["arg5"], struct.pack("<QQ", status, 0))
            uc.reg_write(UC_X86_REG_RAX, status)
        elif mode == "divergence":
            uc.mem_write(a["arg5"], struct.pack("<QQ", status, 0))
            uc.reg_write(UC_X86_REG_RAX, 0)

    def _send(self, uc, a):
        self._garde_ioctl(uc, a)
        self._garde_sans_sortie(uc, a)
        info = self._wsabuf(uc, a, self.longueur_attendue, KIT_CHARGE,
                            "WSABUF.len (la longueur demandée)",
                            "WSABUF.buf (LA CHARGE du kit — AUCUNE copie, I2)")
        if self._d(uc, info, 12) != 0 or self._d(uc, info, 16) != 0:
            self.ecarts.append("AfdFlags/TdiFlags (la MESURE p.3 : zéro et zéro)")
        if self.ecarts:
            return self._refus_param(uc, a)
        mode, compte = self.modes["send"]
        if mode == "succes":
            compte = self.longueur_attendue          # TOUT est émis
        if mode in ("succes", "partiel"):
            self.emis = bytes(uc.mem_read(self.charge_vue, self.longueur_attendue))
            uc.mem_write(a["arg5"], struct.pack("<QQ", 0, compte))
            uc.reg_write(UC_X86_REG_RAX, 0)
        elif mode == "status":
            uc.mem_write(a["arg5"], struct.pack("<QQ", compte, 0))
            uc.reg_write(UC_X86_REG_RAX, compte)
        elif mode == "divergence":
            self.emis = bytes(uc.mem_read(self.charge_vue, self.longueur_attendue))
            uc.mem_write(a["arg5"], struct.pack("<QQ", compte, 0))
            uc.reg_write(UC_X86_REG_RAX, 0)

    def _recv(self, uc, a):
        self._garde_ioctl(uc, a)
        self._garde_sans_sortie(uc, a)
        info = self._wsabuf(uc, a, self.capacite_attendue, KIT_TAMPON,
                            "WSABUF.len (la capacité)",
                            "WSABUF.buf (LE TAMPON du kit — le noyau ÉCRIT chez lui, I2)")
        # L'ERRATUM n° 10 : LE TERRAIN A JUGÉ LA MESURE — la sonde sys-06
        # (Entrée 191) a lu le refus du VRAI noyau sur le 0x20 posé en
        # AfdFlags (STATUS_INVALID_PARAMETER, trois fois) : TDI_RECEIVE_NORMAL
        # vit au champ TdiFlags (+16 — le placement de la littérature),
        # AfdFlags (+12) = 0 — le noyau strict est LE JUGE : il refuse ce
        # que le VRAI noyau refuse, la notation suit LE TERRAIN ou est
        # REFUSÉE (l'erratum de lecture de la révision 2 est MORT)
        if self._d(uc, info, 12) != 0:
            self.ecarts.append(f"AfdFlags {self._d(uc, info, 12):#x} ≠ 0 "
                               "(L'ERRATUM n° 10 : LE TERRAIN — le 0x20 "
                               "ici serait REFUSÉ par le VRAI noyau)")
        if self._d(uc, info, 16) != L.TDI_RECEIVE_NORMAL:
            self.ecarts.append(f"TdiFlags {self._d(uc, info, 16):#x} ≠ 0x20 "
                               "(LE TERRAIN A JUGÉ : TDI_RECEIVE_NORMAL "
                               "vit ICI, le placement de la littérature)")
        if self.ecarts:
            return self._refus_param(uc, a)
        mode, n = self.modes["recv"]
        if mode == "succes":
            uc.mem_write(self.charge_vue, self.recu_pose)   # le noyau ÉCRIT
            uc.mem_write(a["arg5"], struct.pack("<QQ", 0, len(self.recu_pose)))
            uc.reg_write(UC_X86_REG_RAX, 0)
        elif mode == "demi-fin":                     # le pair a fermé proprement
            uc.mem_write(a["arg5"], struct.pack("<QQ", 0, 0))
            uc.reg_write(UC_X86_REG_RAX, 0)
        elif mode == "status":
            uc.mem_write(a["arg5"], struct.pack("<QQ", n, 0))
            uc.reg_write(UC_X86_REG_RAX, n)
        elif mode == "divergence":
            uc.mem_write(a["arg5"], struct.pack("<QQ", n, 0))
            uc.reg_write(UC_X86_REG_RAX, 0)



# --- L'émulateur ------------------------------------------------------------------

class Emulateur:
    """L'image du plan + les notations + le module + les traceurs.

    blobs : les OCTETS du build (mode construire/verifier de build_m8 — le
    harnais re-constate byte-égal avec l'assemblage des notations : jamais
    deux sources de vérité) ; None : assemblage local (mode autonome)."""

    def __init__(self, noyau: Noyau, blobs: dict[str, bytes] | None = None):
        self.ks = Ks(KS_ARCH_X86, KS_MODE_64)
        self.noyau = noyau
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc = self.uc
        uc.mem_map(ZONE_CODE[0], ZONE_CODE[1] - ZONE_CODE[0])
        uc.mem_map(ZONE_PILE, TAILLE_PILE)
        uc.mem_write(RET_MAGIQUE, b"\xF4")             # hlt — l'arrêt propre
        uc.mem_write(TRAMPOLINE_WF, b"\xC3")           # ret — la fausse WriteFile

        # les notations (ce que build_m8.py embarquera) + les héritages scellés
        self.octets_blocs: dict[str, bytes] = {}
        for bid, (nom_fichier, cle_blob) in {
            "g90001": ("sys-01-emetteur", "sys-01"),
            "g90002": ("sys-02-resolveur", "sys-02"),
            "g90003": ("sys-03-ecriture", "sys-03"),
            "g90004": ("sys-04-transport", "sys-04"),
            "g90005": ("sys-05-emission", "sys-05"),
            "g90006": ("sys-06-reception", "sys-06"),
        }.items():
            rva, slot = L.SLOTS_SYS[bid]
            chemin = os.path.join(ICI, "notation", nom_fichier + ".asm")
            octets, _metas = B4.assembler_bloc(self.ks, chemin, rva, slot)
            if blobs is not None:
                # le build passe SES octets : re-constat byte-égal (une seule
                # source de vérité — la notation ; le build n'en est que le porteur)
                if blobs[cle_blob] != octets:
                    raise ErreurHarnais(
                        f"{bid} : les octets du build divergent de la notation "
                        f"assemblée ({len(blobs[cle_blob])} o vs {len(octets)} o)")
            self.octets_blocs[bid] = octets
            uc.mem_write(rva, octets + b"\x90" * (slot - len(octets)))
        # memcmp libc-02 (b20002 — l'héritage scellé M1) et hello-02 (a10002, M0)
        chemin = os.path.join(ICI, os.pardir, "m1", "notation", "libc-02-memcmp.asm")
        octets, _ = B4.assembler_bloc(self.ks, chemin, L.MEMCMP_VA, L.MEMCMP_SLOT)
        self.octets_blocs["b20002"] = octets
        uc.mem_write(L.MEMCMP_VA, octets + b"\x90" * (L.MEMCMP_SLOT - len(octets)))
        chemin = os.path.join(ICI, os.pardir, "m0", "notation", "hello-02-write.asm")
        octets, _ = B4.assembler_bloc(self.ks, chemin, 0x1040, 0x40)
        self.octets_blocs["a10002"] = octets
        uc.mem_write(0x1040, octets + b"\x90" * (0x40 - len(octets)))

        # les fixtures .rdata du domaine (le plan, source unique) + l'IAT M0
        uc.mem_write(L.R_SYS_NOM, L.TXT_SYS_NOM + b"\x00" * 16)
        uc.mem_write(L.R_SYS_LIGNE, L.TXT_SYS_LIGNE + b"\x00" * 16)
        uc.mem_write(0x20B8, struct.pack("<Q", TRAMPOLINE_WF))   # IAT[1] WriteFile

        # les fixtures .text6 du SOCLE SOCKET (chantier M9-(d) — le plan,
        # source unique ; RE-DÉRIVÉS des constantes, jamais recopiés : le
        # device UTF-16LE + NUL, le EA DÉTERMINISTE 54 o, le bind WILDCARD
        # 20 o, les noms de résolution en SPANS sans NUL — verifier_specs_m9d
        # en est le juge dédié des VALEURS, le harnais les re-pose ici)
        uc.mem_write(L.R_SYS_DEVICE, L.TXT_AFD_DEVICE + b"\x00\x00")
        uc.mem_write(L.R_SYS_EA, ea_deterministe())
        uc.mem_write(L.R_SYS_BIND, bind_wildcard())
        uc.mem_write(L.R_SYS_NOM_CREATEFILE, L.TXT_NT_CREATEFILE)
        uc.mem_write(L.R_SYS_NOM_DEVICEIOCTL, L.TXT_NT_DEVICEIOCTL)
        uc.mem_write(L.R_SYS_NOM_CLOSE, L.TXT_NT_CLOSE)

        # le module ntdll synthétique (posé par poser_module)
        self.module: ModuleFixe | None = None
        self.lectures_hors_module = []
        self.lectures_nbnoms = 0
        self.ecritures_module = []

        # les hooks : le noyau (syscall), la fausse WriteFile, les traceurs
        uc.hook_add(UC_HOOK_INSN, noyau.hook, None, 1, 0, UC_X86_INS_SYSCALL)
        uc.hook_add(UC_HOOK_CODE, self._hook_wf, begin=TRAMPOLINE_WF,
                    end=TRAMPOLINE_WF)
        uc.hook_add(UC_HOOK_MEM_READ, self._hook_lecture)
        uc.hook_add(UC_HOOK_MEM_WRITE, self._hook_ecriture)

        # le traceur SOUS-CADRE (chantier M9-(d)) : les blocs du socle ont une
        # chaîne d'appel (sys-02 → memcmp) dont les trames écrivent légitime-
        # ment AU-DESSOUS de la leur — la canariée pleine ne juge que les
        # blocs SANS cadre ; la PREUVE du socle est la PROVENANCE : chaque
        # écriture sous le cadre doit venir d'un bloc PRUVÉ (sys-02, memcmp
        # scellé M1, sys-01 six octets) ou du push d'un appel DU bloc
        # (taille 8, RIP dans sa plage) — TOUT autre scribble est une faute
        self.surveillance_basse: tuple[int, int] | None = None
        self.ecritures_basses: list[tuple[int, int, int]] = []

        # les captures de la fausse WriteFile (le chemin A du différentiel)
        self.captures_wf: list[dict] = []

    def _hook_wf(self, uc: Uc, _ad: int, _taille: int, _ud):
        """La fausse WriteFile : capture (handle, tampon, longueur), rend TRUE."""
        self.captures_wf.append({
            "handle": uc.reg_read(UC_X86_REG_RCX),
            "tampon": uc.reg_read(UC_X86_REG_RDX),
            "longueur": uc.reg_read(UC_X86_REG_R8),
        })
        uc.reg_write(UC_X86_REG_RAX, 1)

    def _hook_lecture(self, uc, acces, adresse, taille, valeur, _ud):
        m = self.module
        if m is None:
            return
        base, fin = MODULE_BASE, MODULE_BASE + m.taille
        if not (base <= adresse < fin):
            # une lecture hors du module n'est FAUTE que si elle part du module…
            return
        if base + m.dir_export_rva + L.EXP_NBNOMS <= adresse < \
                base + m.dir_export_rva + L.EXP_NBNOMS + 4:
            self.lectures_nbnoms += 1

    def _hook_ecriture(self, uc, acces, adresse, taille, valeur, _ud):
        m = self.module
        if m is not None:
            base, fin = MODULE_BASE, MODULE_BASE + m.taille
            if base <= adresse < fin:
                self.ecritures_module.append((adresse, taille, valeur))
        if self.surveillance_basse is not None \
                and self.surveillance_basse[0] <= adresse < self.surveillance_basse[1]:
            self.ecritures_basses.append(
                (adresse, taille, uc.reg_read(UC_X86_REG_RIP)))

    def reposer_bloc(self, va: int, octets: bytes):
        """Re-pose des octets de code ET invalide la cache de traduction
        (unicorn ne re-traduit pas seul un bloc déjà exécuté — la leçon du
        premier passage V4 : les mutations devaient être invisibles)."""
        self.uc.mem_write(va, octets)
        fin = va + len(octets)
        self.uc.ctl_remove_cache(va, (fin + 0xFFF) & ~0xFFF)

    def poser_module(self, module: ModuleFixe):
        if self.module is not None:
            self.uc.mem_unmap(MODULE_BASE, self.module.taille)
        self.uc.mem_map(MODULE_BASE, module.taille)
        self.uc.mem_write(MODULE_BASE, module.octets)
        self.module = module
        self.lectures_nbnoms = 0
        self.ecritures_module = []

    CANARI = b"\xA5"

    def appeler(self, va: int, args: dict[str, int] | None = None,
                rax: int = 0, args_pile: dict[int, int] | None = None):
        """Appelle un bloc comme une fonction msx64 : pose les sentinelles,
        pousse l'adresse de retour magique, pose les arguments de pile du
        FAUX APPELANT (loges 5-9 à [rsp_entrée+0x28]+), rend la main après
        le ret. Les canaris couvrent la pile de l'appelant AU-DESSUS de
        l'adresse de retour (aucun bloc ne doit y toucher)."""
        uc = self.uc
        for nom, val in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], val)
        for nom, val in (args or {}).items():
            uc.reg_write(REGS[nom], val)
        uc.reg_write(UC_X86_REG_RAX, rax)
        rsp = RSP0 - 0x100                    # l'entrée ≡ 8 mod 16 (le ret magique)
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.mem_write(rsp + 8, self.CANARI * 0x100)      # l'ombre + les loges (au callee)
        uc.mem_write(rsp - 0x200, self.CANARI * 0x200)  # la zone morte en-dessous
        for loge, valeur in (args_pile or {}).items():  # loges 5..9 du callee
            uc.mem_write(rsp + 0x28 + (loge - 5) * 8, struct.pack("<Q", valeur))
        # la pile de l'APPELANT AU-DESSUS des loges (0x50 = après la 9e) :
        # c'est SA zone à lui — aucun bloc ne doit y toucher
        uc.mem_write(rsp + 0x50, self.CANARI * 0x100)
        uc.mem_write(rsp, struct.pack("<Q", RET_MAGIQUE))
        entree_rsp = rsp
        try:
            uc.emu_start(va, RET_MAGIQUE, count=2_000_000)
        except UcError as err:
            return {"crash": str(err), "entree_rsp": entree_rsp,
                    "canaris_haut": False, "canaris_bas": False}
        sortie = {k: uc.reg_read(REGS[k]) for k in
                  ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp",
                   "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15", "rsp"]}
        sortie["rax"], sortie["rdx"] = s64(sortie["rax"]), s64(sortie["rdx"])
        sortie["entree_rsp"] = entree_rsp
        sortie["crash"] = None
        sortie["canaris_haut"] = bytes(
            uc.mem_read(rsp + 0x50, 0x100)) == self.CANARI * 0x100
        sortie["canaris_bas"] = bytes(
            uc.mem_read(entree_rsp - 0x200, 0x200)) == self.CANARI * 0x200
        return sortie


def s64(v: int) -> int:
    """unicorn rend les registres NON SIGNÉS ; les verdicts du domaine sont
    de vrais négatifs 64 bits — la comparaison se fait côté signé."""
    return v - (1 << 64) if v >= (1 << 63) else v


def fautes_sous_cadre(emu: "Emulateur", rva_bloc: int, taille_slot: int):
    """Le juge de PROVENANCE des écritures sous le cadre du bloc : chaque
    écriture doit venir d'un bloc PRUVÉ (sys-02 V2b, memcmp scellé M1, sys-01
    six octets — leurs trames sont leurs affaires, déjà prouvées) ou être le
    push d'un appel DU bloc (taille 8, RIP dans SA plage : les six call du
    socle) — TOUT autre scribble est une faute NOMMÉE."""
    plages_prouvees = [
        (L.SYS02_VA, L.SYS02_VA + L.SLOTS_SYS["g90002"][1]),
        (L.MEMCMP_VA, L.MEMCMP_VA + L.MEMCMP_SLOT),
        (L.SYS01_VA, L.SYS01_VA + 6),
    ]
    fautes = []
    for adresse, taille, rip in emu.ecritures_basses:
        if any(a <= rip < b for a, b in plages_prouvees):
            continue
        if rva_bloc <= rip < rva_bloc + taille_slot and taille == 8:
            continue          # le push d'un call du bloc lui-même
        fautes.append((adresse, taille, rip))
    return fautes


def attendus_du_modele(modele):
    """Le modèle rend (verdict, ssn, stub_va) ; le bloc rend rax = LE SSN au
    succès (Q1 de sys-02 — jamais 0), rax = le verdict aux échecs ; rdx =
    l'adresse du stub au succès seulement (Q2)."""
    verdict, ssn, stub_va = modele
    if verdict == L.V_RESOLU:
        return ssn, stub_va
    return verdict, None


# --- Les modèles du SOCLE (dérivés des specs m8/I/sys-0{4,5,6} — jamais -----
# --- des octets de la notation) ------------------------------------------------

def modele_sys04(module: ModuleFixe, modes: dict):
    """La marche create→bind→connect de la SPÉCIFICATION : chaque étage
    réussit, rend un STATUS non nul, ou parle deux fois (la divergence) ;
    chaque résolution peut échouer (l'ordre est le contrat — I6). Rend
    (rax, rdx, nb_syscalls, handle_posé) — rdx n'est nommé qu'aux échecs."""
    v = modele_resoudre(module, L.TXT_NT_CREATEFILE)
    if v[0] != L.V_RESOLU:
        return (-1, v[0], 0, False)
    mode, status = modes["create"]
    if mode == "status":
        return (-6, status, 1, False)
    if mode == "divergence":
        return (-6, status, 1, False)
    v2 = modele_resoudre(module, L.TXT_NT_DEVICEIOCTL)
    if v2[0] != L.V_RESOLU:            # le module statique : geste 2 échoue ici
        return (-1, v2[0], 1, False)
    for geste, attendus in (("bind", 2), ("connect", 3)):
        mode, status = modes[geste]
        if mode == "status":
            return (-6, status, attendus, False)
        if mode == "divergence":
            return (-6, status, attendus, False)
    return (0, None, 3, True)          # le handle posé, la poignée établie


def modele_sys05(module: ModuleFixe, mode: str, compte: int, rdx_span: bool = False):
    """L'émission de la SPÉCIFICATION : TOTALE ou refus -7 (le compte
    consigné), -6 le STATUS nommé, -1 la résolution, -5 le span."""
    if rdx_span:
        return (-5, None, 0)
    v = modele_resoudre(module, L.TXT_NT_DEVICEIOCTL)
    if v[0] != L.V_RESOLU:
        return (-1, v[0], 0)
    if mode == "status" or mode == "divergence":
        return (-6, compte, 1)
    if mode == "partiel":
        return (-7, compte, 1)
    return (0, None, 1)                 # TOUT est émis


def modele_sys06(module: ModuleFixe, mode: str, n: int, compte: int,
                 rdx_span: bool = False):
    """La réception de la SPÉCIFICATION : n ≥ 1 ou LA DEMI-FIN -7 (le zéro
    du pair, rdx consigné 0), -6 le STATUS nommé (p. ex. CNX_REINIT), -1, -5."""
    if rdx_span:
        return (-5, None, 0)
    v = modele_resoudre(module, L.TXT_NT_DEVICEIOCTL)
    if v[0] != L.V_RESOLU:
        return (-1, v[0], 0)
    if mode == "status" or mode == "divergence":
        return (-6, compte, 1)
    if mode == "demi-fin":
        return (-7, 0, 1)
    return (n, None, 1)                 # n rendu au kit


# --- V1 : le round-trip + la concordance des immdiats -----------------------------

def vecteur_v1(ks: Ks, cs: capstone.Cs):
    section("V1 — round-trip de notation + concordance au plan (source unique)")
    for bid, attendu in [("g90001", 6), ("g90002", 293), ("g90003", 164),
                         ("g90004", 676), ("g90005", 289), ("g90006", 287)]:
        nom_fichier = {"g90001": "sys-01-emetteur", "g90002": "sys-02-resolveur",
                       "g90003": "sys-03-ecriture", "g90004": "sys-04-transport",
                       "g90005": "sys-05-emission",
                       "g90006": "sys-06-reception"}[bid]
        rva, slot = L.SLOTS_SYS[bid]
        chemin = os.path.join(ICI, "notation", nom_fichier + ".asm")
        octets, metas = B4.assembler_bloc(ks, chemin, rva, slot)
        insns = B4.round_trip(cs, ks, chemin, rva, octets, metas)
        controle(f"V1.{bid}:round-trip-100",
                 len(insns) == len(metas) and len(octets) == attendu,
                 f"{len(octets)} o == {attendu} o déclarés, "
                 f"{len(insns)}/{len(metas)} instructions")

    # la concordance : chaque immédiat de la notation re-contrôlé au plan
    def lignes(nom_fichier):
        with open(os.path.join(ICI, "notation", nom_fichier + ".asm"),
                  encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip() and
                    not l.startswith(";")]

    n1 = lignes("sys-01-emetteur")
    controle("V1.sys-01:six-octets-trombone",
             n1 == ["mov r10, rcx", "syscall", "ret"],
             "mov r10, rcx ; syscall ; ret — rien d'autre")
    n2 = "\n".join(lignes("sys-02-resolveur")).lower()
    attendus_2 = [
        (f"[r8 + {L.E_LFANEW:#x}]", "E_LFANEW"),
        (f"cmp r11d, {L.E_LFANEW_MIN:#x}", "E_LFANEW_MIN"),
        (f"cmp r11d, {L.E_LFANEW_MAX:#x}", "E_LFANEW_MAX"),
        (f"cmp dword ptr [r9], {int.from_bytes(L.MOTIF_PE, 'little'):#x}",
         "MOTIF_PE"),
        (f"[r9 + {L.OFF_EXPORT_RVA:#x}]", "OFF_EXPORT_RVA"),
        (f"[r10 + {L.EXP_NBNOMS:#x}]", "EXP_NBNOMS"),
        (f"[r10 + {L.EXP_ADRNOMS:#x}]", "EXP_ADRNOMS"),
        (f"[rdx + {L.EXP_ADRORD:#x}]", "EXP_ADRORD"),
        (f"[rdx + {L.EXP_ADRFONC:#x}]", "EXP_ADRFONC"),
        (f"cmp dword ptr [rdx], {int.from_bytes(L.MOTIF_STUB, 'little'):#x}",
         "MOTIF_STUB (dword little-endian)"),
        (f"[rdx + {L.OFF_SSN}]", "OFF_SSN"),
        (f"call {L.MEMCMP_VA:#x}", "MEMCMP (libc-02, la table scellée)"),
    ]
    # la concordance est INSENSIBLE À LA CASSE : keystone écrit « 0x3C », le
    # plan rend « 0x3c » — mêmes octets, mêmes nombres (n2 est minusculisé)
    manquants = [nom for morceau, nom in attendus_2 if morceau not in n2]
    controle("V1.sys-02:concordance-plan", not manquants,
             f"{len(attendus_2) - len(manquants)}/{len(attendus_2)} immédiats"
             + (f" — MANQUANTS : {manquants}" if manquants else ""))
    n3 = "\n".join(lignes("sys-03-ecriture")).lower()
    attendus_3 = [
        (f"mov edx, {L.LEN_SYS_NOM}", "LEN_SYS_NOM (erratum : 11)"),
        (f"mov qword ptr [rsp + 0x30], {L.LEN_SYS_LIGNE}", "LEN_SYS_LIGNE (33)"),
        (f"call {L.SYS02_VA:#x}", "SYS02 (résoudre)"),
        (f"call {L.SYS01_VA:#x}", "SYS01 (émettre — APRÈS)"),
    ]
    manquants = [nom for morceau, nom in attendus_3 if morceau not in n3]
    controle("V1.sys-03:concordance-plan", not manquants,
             f"{len(attendus_3) - len(manquants)}/{len(attendus_3)} immédiats"
             + (f" — MANQUANTS : {manquants}" if manquants else ""))
    # les déplacements RIP citent les fixtures (I4) — les cibles RÉSOLUES de
    # l'en-tête de notation (jamais d'adresses gravées ici) : exactement deux,
    # NOM et LIGNE, l'arithmétique re-faite au geste du contrôle
    with open(os.path.join(ICI, "notation", "sys-03-ecriture.asm"),
              encoding="utf-8") as f:
        brut03 = f.read()
    deplacements = re.findall(
        r";\s+0x([0-9a-f]+) \+ 0x([0-9a-f]+) ([+-]) 0x([0-9a-f]+) = 0x([0-9a-f]+)",
        brut03)
    cibles_rip = []
    for adr, t, signe, disp, cible in deplacements:
        calc = (int(adr, 16) + int(t, 16)
                + (int(disp, 16) if signe == "+" else -int(disp, 16)))
        cibles_rip.append(calc)
        if calc != int(cible, 16):
            manquants.append(f"arithmétique RIP fausse @ {adr}")
    attendu_cibles = sorted([L.R_SYS_NOM, L.R_SYS_LIGNE])
    controle("V1.sys-03:citations-fixtures",
             sorted(cibles_rip) == attendu_cibles,
             f"les DEUX seuls [rip] du bloc résolvent à "
             f"{[hex(c) for c in attendu_cibles]} — le nom et la ligne CITÉS")
    # I3 : l'ordre des appels — résoudre AVANT émettre
    pos_res = n3.find(f"call {L.SYS02_VA:#x}")
    pos_emi = n3.find(f"call {L.SYS01_VA:#x}")
    controle("V1.sys-03:ordre-resoudre-puis-emettre", 0 <= pos_res < pos_emi,
             "l'appel sys-02 précède l'appel sys-01 dans les octets (I3)")

    # ---- LE SOCLE (chantier M9-(d)) : la concordance des TROIS notations ----------

    def citations_rip(nom_fichier):
        """Les cibles RIP d'une notation, lues de son en-tête (jamais des
        adresses gravées ici — l'arithmétique re-faite au geste du contrôle)."""
        with open(os.path.join(ICI, "notation", nom_fichier + ".asm"),
                  encoding="utf-8") as f:
            brut = f.read()
        deplacements = re.findall(
            r";\s+0x([0-9a-f]+) \+ 0x([0-9a-f]+) ([+-]) 0x([0-9a-f]+)"
            r" = 0x([0-9a-f]+)", brut)
        cibles = []
        for adr, t, signe, disp, cible in deplacements:
            calc = (int(adr, 16) + int(t, 16)
                    + (int(disp, 16) if signe == "+" else -int(disp, 16)))
            cibles.append(calc)
            assert calc == int(cible, 16), f"arithmétique RIP fausse @ {adr}"
        return cibles

    n4 = "\n".join(lignes("sys-04-transport")).lower()
    attendus_4 = [
        (f"mov edx, {L.AFD_DESIRED_ACCESS:#x}",
         "AFD_DESIRED_ACCESS (mesuré — ZÉRO-étendu en edx : le C7 de mov "
         "rdx SIGNERAIT, le bit 31 est posé)"),
        (f"mov dword ptr [rsp + 0x90], {L.OBJECT_ATTRIBUTES_TAILLE:#x}",
         "OBJECT_ATTRIBUTES_TAILLE 0x30"),
        (f"mov dword ptr [rsp + 0xa8], {L.OBJ_CASE_INSENSITIVE:#x}",
         "OBJ_CASE_INSENSITIVE 0x40"),
        (f"mov word ptr [rsp + 0xc0], {L.LEN_AFD_DEVICE}",
         "LEN_AFD_DEVICE 40 (l'erratum : SANS le NUL)"),
        (f"mov word ptr [rsp + 0xc2], {L.LEN_AFD_DEVICE + 2}",
         "MaximumLength 42 (AVEC le NUL)"),
        (f"mov qword ptr [rsp + 0x50], {L.AFD_EA_TAILLE}", "AFD_EA_TAILLE 54"),
        (f"mov qword ptr [rsp + 0x28], {L.IOCTL_AFD_BIND:#x}", "IOCTL_AFD_BIND"),
        (f"mov qword ptr [rsp + 0x38], {L.AFD_BIND_TAILLE:#x}",
         "AFD_BIND_TAILLE 0x14"),
        (f"mov qword ptr [rsp + 0x48], {L.AFD_BIND_SORTIE:#x}",
         "AFD_BIND_SORTIE 0x10"),
        (f"mov qword ptr [rsp + 0x28], {L.IOCTL_AFD_CONNECT:#x}",
         "IOCTL_AFD_CONNECT"),
        (f"mov qword ptr [rsp + 0x38], {L.AFD_CONNECT_TAILLE:#x}",
         "AFD_CONNECT_TAILLE 0x28"),
        (f"mov edx, {L.LEN_NT_CREATEFILE}", "LEN_NT_CREATEFILE 11"),
        (f"call {L.SYS02_VA:#x}", "SYS02 (résoudre — × 3 au geste même)"),
        (f"call {L.SYS01_VA:#x}", "SYS01 (émettre — × 3)"),
    ]
    manquants = [nom for morceau, nom in attendus_4 if morceau not in n4]
    controle("V1.sys-04:concordance-plan", not manquants,
             f"{len(attendus_4) - len(manquants)}/{len(attendus_4)} immédiats"
             + (f" — MANQUANTS : {manquants}" if manquants else
                " — create/bind/connect au plan, jamais un littéral hors plan (T5)"))
    controle("V1.sys-04:les-trois-resolutions-au-geste-meme",
             n4.count(f"call {L.SYS02_VA:#x}") == 3
             and n4.count(f"call {L.SYS01_VA:#x}") == 3
             and re.findall(rf"call ({L.SYS02_VA:#x}|{L.SYS01_VA:#x})", n4)
             == [f"{L.SYS02_VA:#x}", f"{L.SYS01_VA:#x}"] * 3,
             "l'alternance résoudre-émettre × 3 dans les octets (Q3/I6 : "
             "create PUIS bind PUIS connect, chaque geste résout)")
    cibles_04 = sorted(citations_rip("sys-04-transport"))
    attendues_04 = sorted([L.R_SYS_DEVICE, L.R_SYS_EA, L.R_SYS_BIND,
                            L.R_SYS_NOM_CREATEFILE, L.R_SYS_NOM_DEVICEIOCTL,
                            L.R_SYS_NOM_DEVICEIOCTL])
    controle("V1.sys-04:citations-fixtures", cibles_04 == attendues_04,
             f"les SIX seuls [rip] résolvent à {[hex(c) for c in attendues_04]} "
             "— le device, le EA, le bind WILDCARD et les noms CITÉS (T5/I3)")

    n5 = "\n".join(lignes("sys-05-emission")).lower()
    attendus_5 = [
        (f"mov qword ptr [rsp + 0x28], {L.IOCTL_AFD_SEND:#x}", "IOCTL_AFD_SEND"),
        (f"mov qword ptr [rsp + 0x38], {L.AFD_SENDRECV_TAILLE:#x}",
         "AFD_SENDRECV_TAILLE 0x18 (le C_ASSERT send==recv)"),
        ("mov dword ptr [rsp + 0x78], 1", "BufferCount 1 (la MESURE)"),
        ("mov dword ptr [rsp + 0x7c], 0", "AfdFlags 0 (la MESURE p.3)"),
        ("mov dword ptr [rsp + 0x80], 0", "TdiFlags 0"),
        ("mov dword ptr [rsp + 0x60], esi", "WSABUF.len = la longueur demandée"),
        ("mov qword ptr [rsp + 0x68], rdi",
         "WSABUF.buf = LA CHARGE du kit, le CANONIQUE +8 "
         "(I2 — la Révision 2, la MESURE de la sonde)"),
        (f"mov edx, {L.LEN_NT_DEVICEIOCTL}", "LEN_NT_DEVICEIOCTL 21"),
    ]
    manquants = [nom for morceau, nom in attendus_5 if morceau not in n5]
    controle("V1.sys-05:concordance-plan", not manquants,
             f"{len(attendus_5) - len(manquants)}/{len(attendus_5)} immédiats"
             + (f" — MANQUANTS : {manquants}" if manquants else ""))
    controle("V1.sys-05:citation-fixture",
             citations_rip("sys-05-emission") == [L.R_SYS_NOM_DEVICEIOCTL],
             f"l'unique [rip] résout à {L.R_SYS_NOM_DEVICEIOCTL:#x} — le nom "
             "CITÉ, jamais reconstruit (T5)")

    n6 = "\n".join(lignes("sys-06-reception")).lower()
    attendus_6 = [
        (f"mov qword ptr [rsp + 0x28], {L.IOCTL_AFD_RECEIVE:#x}",
         "IOCTL_AFD_RECEIVE"),
        ("mov dword ptr [rsp + 0x7c], 0",
         "AfdFlags 0 (L'ERRATUM n° 10 : LE TERRAIN A JUGÉ — le VRAI noyau "
         "refuse le 0x20 ici, la sonde sys-06 l'a mesuré)"),
        (f"mov dword ptr [rsp + 0x80], {L.TDI_RECEIVE_NORMAL:#x}",
         "TdiFlags = TDI_RECEIVE_NORMAL 0x20 (LE TERRAIN : le placement "
         "de la littérature, la mesure WinDbg citée avait tort du champ)"),
        ("mov dword ptr [rsp + 0x78], 1", "BufferCount 1"),
        ("mov dword ptr [rsp + 0x60], esi", "WSABUF.len = la capacité"),
        ("mov qword ptr [rsp + 0x68], rdi",
         "WSABUF.buf = LE TAMPON du kit, le CANONIQUE +8 "
         "(la Révision 2 — l'erratum n° 9, le miroir de la sonde)"),
        (f"mov edx, {L.LEN_NT_DEVICEIOCTL}", "LEN_NT_DEVICEIOCTL 21"),
    ]
    manquants = [nom for morceau, nom in attendus_6 if morceau not in n6]
    controle("V1.sys-06:concordance-plan", not manquants,
             f"{len(attendus_6) - len(manquants)}/{len(attendus_6)} immédiats"
             + (f" — MANQUANTS : {manquants}" if manquants else
                " — l'erratum n° 10 tenu : RIEN en AfdFlags, 0x20 en TdiFlags"))
    controle("V1.sys-06:citation-fixture",
             citations_rip("sys-06-reception") == [L.R_SYS_NOM_DEVICEIOCTL],
             f"l'unique [rip] résout à {L.R_SYS_NOM_DEVICEIOCTL:#x} (T5)")


# --- V2 : l'épreuve à shims --------------------------------------------------------

def vecteur_v2(emu: Emulateur, noyau: Noyau):
    section("V2a — sys-01 : le trombone ABI au noyau simulé")
    # l'émetteur : SSN 0x31A, quatre arguments en registres, cinq à la pile
    # (posés par le FAUX APPELANT aux loges 5-9 — le mécanisme de appeler)
    IOSB = RSP0 - 0x400                    # une iosb du côté de l'appelant
    BUF = RSP0 - 0x380                     # un tampon hors du module
    emu.uc.mem_write(BUF, L.TXT_SYS_LIGNE)

    def ntwritefile_trombone(uc, a):       # le comportement du SSN 0x31A
        noyau.lignes_emises.append(bytes(uc.mem_read(a["arg6"], a["arg7"])))
        uc.mem_write(a["arg5"], struct.pack("<QQ", 0, a["arg7"]))
        uc.reg_write(UC_X86_REG_RAX, 0)

    noyau.dispatch = {0x31A: ntwritefile_trombone}
    noyau.captures.clear()
    r = emu.appeler(L.SYS01_VA,
                    {"rcx": HANDLE_MAGIQUE, "rdx": 0, "r8": 0, "r9": 0},
                    rax=0x31A,
                    args_pile={5: IOSB, 6: BUF, 7: L.LEN_SYS_LIGNE, 8: 0, 9: 0})
    cap = noyau.captures[-1] if noyau.captures else {}
    controle("V2a.sys-01:remappage-rcx-r10",
             not r["crash"] and cap.get("handle") == HANDLE_MAGIQUE,
             f"le noyau lit r10 = {cap.get('handle', 0):#x} == rcx passé")
    controle("V2a.sys-01:ssn-transmis-tel-quel",
             cap.get("ssn") == 0x31A, "rax n'est jamais écrit avant le site (I2)")
    controle("V2a.sys-01:pile-lue-a-rsp28",
             cap.get("arg5") == IOSB and cap.get("arg6") == BUF
             and cap.get("arg7") == L.LEN_SYS_LIGNE and cap.get("arg8") == 0
             and cap.get("arg9") == 0,
             "les cinq arguments de pile lus à [rsp+0x28]+ AU site (I3)")
    controle("V2a.sys-01:site-unique",
             len(noyau.captures) == 1 and r.get("rax") == 0
             and noyau.lignes_emises[-1] == L.TXT_SYS_LIGNE[:L.LEN_SYS_LIGNE],
             "exactement un syscall, le NTSTATUS 0 traverse (Q1/Q2)")
    controle("V2a.sys-01:rcx-r11-detruits",
             r.get("rcx") == L.SYS01_VA + 5 and r.get("r11") == 0x246,
             "rcx = l'adresse de retour, r11 = les drapeaux (Q3)")
    controle("V2a.sys-01:non-volatils-et-pile",
             all(r[k] == v for k, v in SENTINELLES_NV.items())
             and r.get("rsp") == r.get("entree_rsp") + 8
             and r.get("canaris_haut") and r.get("canaris_bas"),
             "huit non-volatils sentinelles, la pile rendue (pop du ret), "
             "l'appelant ET la zone morte intacts (I4/Q4/I5 : le trombone "
             "n'écrit RIEN nulle part)")

    # un NTSTATUS d'échec traverse AUSSI tel quel (Q2) — jamais muet
    noyau.captures.clear()
    noyau.dispatch = {}
    r = emu.appeler(L.SYS01_VA, {"rcx": 1}, rax=0x31A)
    controle("V2a.sys-01:status-echec-traverse",
             not r["crash"] and r["rax"] == STATUS_INVALIDE
             and len(noyau.captures) == 1,
             f"SSN inconnu → {STATUS_INVALIDE:#x} rendu tel quel")

    section("V2b — sys-02 : le résolveur sur fixtures ntdll synthétiques")
    noyau.captures.clear()                 # le compteur syscall part à ZÉRO ici

    def jouer_sys02(module: ModuleFixe, span: bytes | None, ptr_span: int | None):
        """Appelle sys-02 (span, longueur, base) et rend (sortie, verdict_modèle)."""
        emu.poser_module(module)
        empreinte_avant = module.empreinte()
        args = {"rcx": ptr_span if span else 0, "rdx": len(span) if span else 0,
                "r8": MODULE_BASE}
        r = emu.appeler(L.SYS02_VA, args)
        modele = modele_resoudre(module, span)
        empreinte_apres = hashlib.sha256(
            emu.uc.mem_read(MODULE_BASE, module.taille)).hexdigest()[:16]
        return r, modele, empreinte_avant == empreinte_apres

    ESPACE_SPAN = RSP0 + 0x100          # un span hors du module (la pile)
    def poser_span(span: bytes) -> int:
        emu.uc.mem_write(ESPACE_SPAN, span + b"\x00" * 32)
        return ESPACE_SPAN

    # le succès : la cible AU MILIEU d'une table peuplée — rax = LE SSN (Q1 :
    # « succès : rax = le SSN »), rdx = l'adresse du stub (Q2)
    mod = forger_module([("NtClose", 0x0F), ("NtWriteFile", 0x31A),
                         ("NtReadFile", 0x31B), ("NtQueryValueKey", 0x22)])
    ptr = poser_span(b"NtWriteFile")
    r, modele, intact = jouer_sys02(mod, b"NtWriteFile", ptr)
    rax_att, rdx_att = attendus_du_modele(modele)
    controle("V2b.sys-02:resolu-au-milieu",
             r["rax"] == rax_att == 0x31A and r["rdx"] == rdx_att
             and not r["crash"],
             f"rax = LE SSN {rax_att:#x} (jamais 0 — Q1), rdx = le stub "
             f"{rdx_att:#x} (Q2)")
    controle("V2b.sys-02:module-intact-I8", intact and not emu.ecritures_module,
             f"{len(emu.ecritures_module)} écriture(s) dans le module lu")
    controle("V2b.sys-02:non-volatils-I7",
             all(r[k] == v for k, v in SENTINELLES_NV.items()))
    controle("V2b.sys-02:aucun-syscall-I4", len(noyau.captures) == 0,
             "le bloc qui LIT n'ÉMET pas — la séparation est la garde")
    controle("V2b.sys-02:borne-lue-une-fois-I1", emu.lectures_nbnoms == 1,
             f"NumberOfNames lu {emu.lectures_nbnoms} fois (la fenêtre)")
    noyau.captures.clear()

    # la cible en DERNIÈRE position (la marche complète jusqu'au bout)
    mod = forger_module([("NtClose", 1), ("NtAcceptConnectPort", 2),
                         ("NtWriteFile", 0x31A)])
    r, modele, intact = jouer_sys02(mod, b"NtWriteFile", poser_span(b"NtWriteFile"))
    rax_att, rdx_att = attendus_du_modele(modele)
    controle("V2b.sys-02:resolu-en-derniere",
             r["rax"] == rax_att and r["rdx"] == rdx_att, "le dernier nom")

    # la cible ABSENTE : la marche complète est une réponse (-1)
    mod = forger_module([("NtClose", 1), ("NtReadFile", 2)])
    r, modele, _ = jouer_sys02(mod, b"NtWriteFile", poser_span(b"NtWriteFile"))
    controle("V2b.sys-02:nom-absent-moins-1",
             r["rax"] == L.V_NOM_ABSENT and r["rax"] == modele[0],
             "marche COMPLÈTE des noms, aucun accès au-delà (I1)")
    controle("V2b.sys-02:EAT-vide-moins-1",
             (lambda m: (lambda rr: rr[0])(
                 jouer_sys02(m, b"NtWriteFile", poser_span(b"NtWriteFile"))))(
                 forger_module([]))["rax"] == L.V_NOM_ABSENT,
             "NumberOfNames = 0 : la marche vide est une réponse")

    # les refus nommés hostiles
    r, modele, _ = jouer_sys02(forger_module([("NtWriteFile", 9)],
                                             e_lfanew=0x3F),
                               b"NtWriteFile", poser_span(b"NtWriteFile"))
    controle("V2b.sys-02:elfanew-trop-petit-moins-2",
             r["rax"] == L.V_PAS_MODULE and r["rax"] == modele[0],
             "e_lfanew 0x3F < fenêtre [0x40, 0x400]")
    r, modele, _ = jouer_sys02(forger_module([("NtWriteFile", 9)],
                                             e_lfanew=0x401),
                               b"NtWriteFile", poser_span(b"NtWriteFile"))
    controle("V2b.sys-02:elfanew-fou-moins-2",
             r["rax"] == L.V_PAS_MODULE and r["rax"] == modele[0],
             "e_lfanew 0x401 > fenêtre")
    r, modele, _ = jouer_sys02(forger_module([("NtWriteFile", 9)],
                                             sig_pe=False),
                               b"NtWriteFile", poser_span(b"NtWriteFile"))
    controle("V2b.sys-02:pas-de-signature-moins-2",
             r["rax"] == L.V_PAS_MODULE and r["rax"] == modele[0],
             "le motif « PE\\0\\0 » absent à e_lfanew")
    r, modele, _ = jouer_sys02(forger_module([("NtWriteFile", 9)],
                                             export_absente=True),
                               b"NtWriteFile", poser_span(b"NtWriteFile"))
    controle("V2b.sys-02:export-absent-moins-3",
             r["rax"] == L.V_EAT_ABSENTE and r["rax"] == modele[0],
             "RVA nul : le module n'exporte rien")
    mod = forger_module([("NtClose", 1), ("NtWriteFile", 0x31A)],
                        stub_trop="NtWriteFile")
    r, modele, _ = jouer_sys02(mod, b"NtWriteFile", poser_span(b"NtWriteFile"))
    controle("V2b.sys-02:stub-crochete-moins-4",
             r["rax"] == L.V_STUB_DIVERGENT and r["rax"] == modele[0],
             "le motif diverge (hook) : le numéro N'EST PAS extrait (charte § 2)")
    r, _, _ = jouer_sys02(forger_module([("NtWriteFile", 9)]), None, None)
    controle("V2b.sys-02:span-invalide-moins-5",
             r["rax"] == L.V_SPAN_INVALIDE and not r["crash"],
             "pointeur nul / longueur nulle (P1/P2)")

    # le SSN pathologique à bit 31 : jamais confondu avec un verdict (zéro-étendu)
    mod = forger_module([("NtWriteFile", 0x80000001)])
    r, modele, _ = jouer_sys02(mod, b"NtWriteFile", poser_span(b"NtWriteFile"))
    controle("V2b.sys-02:ssn-bit31-positif-quand-meme",
             r["rax"] == 0x80000001 and r["rax"] == modele[1],
             "l'imm32 zéro-étendu reste POSITIF en 64 bits — la séparation"
             " verdicts(négatifs signés)/SSN(zéro-étendus) est structurelle")

    section("V2c — sys-03 : LA TWIN AU DIFFÉRENTIEL (la MÊME ligne, deux chemins)")

    # LE CHEMIN A : hello-02 (le scellé M0, WriteFile par l'IAT)
    noyau.captures.clear()
    r_a = emu.appeler(0x1040, {"rcx": HANDLE_MAGIQUE, "rdx": L.R_SYS_LIGNE,
                               "r8": L.LEN_SYS_LIGNE})
    cap_a = emu.captures_wf[-1]
    ligne_a = bytes(emu.uc.mem_read(cap_a["tampon"], cap_a["longueur"]))
    controle("V2c.chemin-A:hello-02-par-IAT",
             not r_a["crash"] and r_a["rax"] == 1
             and cap_a["handle"] == HANDLE_MAGIQUE
             and cap_a["tampon"] == L.R_SYS_LIGNE
             and cap_a["longueur"] == L.LEN_SYS_LIGNE,
             "WriteFile(handle, fixture-ligne, 33) — le scellé M0 émule vert")

    # LE CHEMIN B : sys-03 (NtWriteFile en syscall direct)
    mod = forger_module([("NtClose", 0x0F), ("NtWriteFile", 0x31A)])
    emu.poser_module(mod)

    def ntwritefile(uc, a):
        noyau.lignes_emises.append(bytes(uc.mem_read(a["arg6"], a["arg7"])))
        uc.mem_write(a["arg5"], struct.pack("<QQ", 0, a["arg7"]))
        uc.reg_write(UC_X86_REG_RAX, 0)

    noyau.dispatch = {0x31A: ntwritefile}
    noyau.captures.clear()
    noyau.lignes_emises.clear()
    emu.captures_wf.clear()
    r_b = emu.appeler(L.SYS03_VA, {"rcx": MODULE_BASE, "rdx": HANDLE_MAGIQUE})
    cap_b = noyau.captures[-1] if noyau.captures else {}
    ligne_b = noyau.lignes_emises[-1] if noyau.lignes_emises else b""
    controle("V2c.chemin-B:la-meme-ligne-octet-pour-octet",
             not r_b["crash"] and r_b["rax"] == 0 and ligne_a == ligne_b
             == L.TXT_SYS_LIGNE[:L.LEN_SYS_LIGNE],
             "la ligne émise par NtWriteFile == celle de WriteFile == "
             "le fixture M0 (Q1 — la preuve d'observable)")
    controle("V2c.chemin-B:les-neuf-arguments",
             cap_b.get("handle") == HANDLE_MAGIQUE and cap_b.get("arg2") == 0
             and cap_b.get("arg3") == 0 and cap_b.get("arg4") == 0
             and cap_b.get("arg6") == L.R_SYS_LIGNE
             and cap_b.get("arg7") == L.LEN_SYS_LIGNE
             and cap_b.get("arg8") == 0 and cap_b.get("arg9") == 0,
             "handle, Event/Apc/Context NULL, tampon le fixture, 33, "
             "ByteOffset NULL, Key 0 (Q3)")
    iosb_ptr = cap_b.get("arg5", 0)
    entree_rsp = r_b.get("entree_rsp", 0)
    controle("V2c.chemin-B:iosb-sur-la-pile-du-bloc",
             entree_rsp - 0x68 <= iosb_ptr < entree_rsp,
             f"l'IO_STATUS_BLOCK @ {iosb_ptr:#x} vit dans le cadre (I2 — "
             "zone morte au retour)")
    controle("V2c.chemin-B:non-volatils-intacts",
             all(r_b[k] == v for k, v in SENTINELLES_NV.items()),
             "rbx/rbp sauvés et rendus (I6)")
    controle("V2c.chemin-B:pile-de-l-appelant-intacte",
             r_b.get("rsp") == entree_rsp + 8 and r_b.get("canaris_haut"),
             "la pile rendue (pop du ret), l'appelant intact — l'ABI "
             "traversante ne coûte RIEN au cadre")

    # Q2 : le SSN résolu AU GESTE MÊME — deux fixtures, deux SSN, suite
    noyau.captures.clear()
    noyau.lignes_emises.clear()
    for ssn in (0x1122, 0x3344):
        emu.poser_module(forger_module([("NtWriteFile", ssn)]))
        noyau.dispatch = {ssn: ntwritefile}
        emu.appeler(L.SYS03_VA, {"rcx": MODULE_BASE, "rdx": HANDLE_MAGIQUE})
    controle("V2c.au-geste-meme:deux-ssn-distincts-suite",
             [c["ssn"] for c in noyau.captures] == [0x1122, 0x3344]
             and len(noyau.lignes_emises) == 2,
             "chaque appel résoud SA fixture — jamais un numéro en cache (Q2)")

    # I5 : échec de résolution = AUCUN syscall émis
    noyau.captures.clear()
    emu.poser_module(forger_module([("NtClose", 3)]))     # la cible absente
    r = emu.appeler(L.SYS03_VA, {"rcx": MODULE_BASE, "rdx": HANDLE_MAGIQUE})
    controle("V2c.echec-resolution:moins-1-aucun-syscall",
             r["rax"] == -1 and r["rdx"] == L.V_NOM_ABSENT
             and len(noyau.captures) == 0,
             "rax = -1 (le verdict de sys-03), rdx consigne LA CAUSE (le "
             "-1 du résolveur), le compteur syscall demeure à ZÉRO (I5 — "
             "la garde la plus importante)")

    # -6 : le STATUS non nul, consigné en rdx (jamais muet)
    def ntwritefile_refus(uc, a):
        uc.reg_write(UC_X86_REG_RAX, 0xC0000022)
        uc.mem_write(a["arg5"], struct.pack("<QQ", 0xC0000022, 0))

    emu.poser_module(forger_module([("NtWriteFile", 0x31A)]))
    noyau.dispatch = {0x31A: ntwritefile_refus}
    noyau.captures.clear()
    r = emu.appeler(L.SYS03_VA, {"rcx": MODULE_BASE, "rdx": HANDLE_MAGIQUE})
    controle("V2c.status-non-nul:moins-6-consigne",
             r["rax"] == L.V_STATUS_NONNUL and r["rdx"] == 0xC0000022,
             "rax = -6, rdx = 0xC0000022 (STATUS_ACCESS_DENIED) — nommé")

    # -6 : la divergence iosb (le noyau rend 0 mais parle deux fois)
    def ntwritefile_divergent(uc, a):
        uc.reg_write(UC_X86_REG_RAX, 0)
        uc.mem_write(a["arg5"], struct.pack("<QQ", 0xC0000094, 0))

    noyau.dispatch = {0x31A: ntwritefile_divergent}
    noyau.captures.clear()
    r = emu.appeler(L.SYS03_VA, {"rcx": MODULE_BASE, "rdx": HANDLE_MAGIQUE})
    controle("V2c.divergence-iosb:moins-6",
             r["rax"] == L.V_STATUS_NONNUL and r["rdx"] == 0xC0000094,
             "rax = 0 mais iosb = 0xC0000094 : un désaccord est une anomalie")

    # le module lu par la twin demeure intact (I8 de sys-02 au passage)
    empreinte = hashlib.sha256(
        emu.uc.mem_read(MODULE_BASE, emu.module.taille)).hexdigest()[:16]
    controle("V2c.module-intact", empreinte == emu.module.empreinte()
             and not emu.ecritures_module)


# --- V2d/e/f : LE SOCLE SOCKET au noyau AFD simulé (chantier M9-(d)) ---------------

def vecteur_v2d(emu: Emulateur, noyau: Noyau):
    section("V2d — sys-04 : le transport établi au noyau AFD simulé")
    afd = NoyauAFD(noyau)
    SOCKADDR_KIT = sockaddr_kit(80, bytes([192, 168, 1, 1]))

    def poser_kit_sockaddr():
        emu.uc.mem_write(KIT_SOCKADDR - 0x20, emu.CANARI * 0x60)
        emu.uc.mem_write(KIT_SOCKADDR, SOCKADDR_KIT)

    def poser_cellule():
        emu.uc.mem_write(KIT_CELLULE - 0x20, emu.CANARI * 0x60)

    def cellule_lue() -> int:
        return struct.unpack("<Q", emu.uc.mem_read(KIT_CELLULE, 8))[0]

    def jouer_sys04(module, afd_modes=None, sabotage_va=0):
        """Un cas sys-04 : pose le kit, règle le noyau AFD, appelle le bloc.
        Rend (sortie, attendus_du_modèle, cellule, empreinte_avant)."""
        emu.poser_module(module)
        avant = module.empreinte()
        afd.reinit()
        if afd_modes:
            afd.modes.update(afd_modes)
        afd.sockaddr_attendu = SOCKADDR_KIT
        afd.noyau_sabotage = sabotage_va
        poser_kit_sockaddr()
        poser_cellule()
        noyau.dispatch = {SSN_NT_CREATEFILE: afd.creer, SSN_NT_IOCTL: afd.ioctl}
        noyau.captures.clear()
        entree = RSP0 - 0x100
        emu.surveillance_basse = (entree - 0x200, entree - 0x128)
        emu.ecritures_basses = []
        r = emu.appeler(L.SYS04_VA, {"rcx": MODULE_BASE, "rdx": KIT_SOCKADDR,
                                     "r8": KIT_CELLULE})
        emu.surveillance_basse = None
        attendus = modele_sys04(module, afd.modes)
        return r, attendus, cellule_lue(), avant

    MOD_COMPLET = forger_module([
        ("NtClose", 0x0F), ("NtCreateFile", SSN_NT_CREATEFILE),
        ("NtDeviceIoControlFile", SSN_NT_IOCTL)])

    # LE SUCCÈS : la marche ENTIERE, la poignée établie, le handle posé à [P3]
    r, attendus, cellule, avant = jouer_sys04(MOD_COMPLET)
    rax_att, rdx_att, nb_att, pose_att = attendus
    controle("V2d.sys-04:etabli-rax-0-handle-pose",
             not r["crash"] and r["rax"] == 0 and cellule == HANDLE_AFD
             and afd.poignee_etablie,
             f"rax = 0, [P3] = {HANDLE_AFD:#x} (posé au succès seulement — Q1), "
             "la poignée TCP EST ÉTABLIE (le connect synchrone a tenu)")
    controle("V2d.sys-04:la-marche-create-bind-connect",
             [c["ssn"] for c in noyau.captures] == [SSN_NT_CREATEFILE,
                                                    SSN_NT_IOCTL, SSN_NT_IOCTL]
             and [c["arg6"] for c in noyau.captures[1:]] ==
             [L.IOCTL_AFD_BIND, L.IOCTL_AFD_CONNECT] and len(noyau.captures) == 3,
             "TROIS syscalls : create PUIS BIND PUIS CONNECT — la séquence "
             "MESURÉE mswsock, jamais connect sans bind (I6)")
    controle("V2d.sys-04:aucun-ecart-noyau-strict", not afd.ecarts,
             f"les ONZE + DIX + DIX arguments validés : {afd.ecarts}" if afd.ecarts
             else "le noyau strict n'a RIEN à nommer")
    # le PHANDLE du create : la LOCALE du bloc, JAMAIS P3 (Q4) — le noyau
    # écrit chez le bloc, le bloc seul décide de copier au kit
    cap0 = noyau.captures[0]
    entree_rsp = r["entree_rsp"]
    controle("V2d.sys-04:phandle-en-locale-jamais-p3",
             entree_rsp - 0x138 <= cap0["handle"] < entree_rsp
             and cap0["handle"] != KIT_CELLULE,
             f"PHANDLE {cap0['handle']:#x} DANS le cadre (I2), la cellule du "
             "kit INTACTE jusqu'à la copie finale — aucune possession partielle")
    controle("V2d.sys-04:iosb-sur-la-pile-du-bloc",
             all(entree_rsp - 0x138 <= c["arg4" if i == 0 else "arg5"] < entree_rsp
                 for i, c in enumerate(noyau.captures)),
             "les TROIS IOSB vivent dans le cadre — zones mortes au retour (I2)")
    controle("V2d.sys-04:le-sockaddr-lu-copie-sans-interpretation",
             bytes(emu.uc.mem_read(KIT_SOCKADDR, 16)) == SOCKADDR_KIT,
             "les 16 o du kit copiés à +24 du AFD_CONNECT, family LE et port "
             "RÉSEAU INTACTS (charte § 9 — le domaine ne convertit JAMAIS)")
    controle("V2d.sys-04:le-kit-et-la-pile-intacts",
             all(r[k] == v for k, v in SENTINELLES_NV.items())
             and r.get("rsp") == entree_rsp + 8 and r.get("canaris_haut")
             and not fautes_sous_cadre(emu, L.SYS04_VA, L.SLOTS_SYS["g90004"][1])
             and bytes(emu.uc.mem_read(KIT_CELLULE - 0x20, 0x18)) == emu.CANARI * 0x18
             and bytes(emu.uc.mem_read(KIT_CELLULE + 8, 0x38)) == emu.CANARI * 0x38,
             "rbx/rbp/rdi sauvés et rendus (I7), la pile rendue, AUCUNE "
             "écriture sous le cadre hors les pushes des six call et les "
             "trames des blocs PRUVÉS — la cellule AVoisinante canariée "
             "intacte : le bloc n'écrit QUE les 8 o de [P3]")
    controle("V2d.sys-04:module-intact", avant == hashlib.sha256(
        emu.uc.mem_read(MODULE_BASE, emu.module.taille)).hexdigest()[:16]
        and not emu.ecritures_module,
        "l'EAT lue trois fois, JAMAIS écrite (I8 de sys-02 au passage)")

    # AU GESTE MÊME (Q3) : deux modules à SSN distincts — la suite suit
    noyau.captures.clear()
    for ssn_c, ssn_i in ((0x55, 0x56), (0xAA, 0xBB)):
        mod = forger_module([("NtCreateFile", ssn_c),
                             ("NtDeviceIoControlFile", ssn_i)])
        afd.reinit()
        afd.sockaddr_attendu = SOCKADDR_KIT
        poser_kit_sockaddr()
        poser_cellule()
        emu.poser_module(mod)
        noyau.dispatch = {ssn_c: afd.creer, ssn_i: afd.ioctl}
        emu.appeler(L.SYS04_VA, {"rcx": MODULE_BASE, "rdx": KIT_SOCKADDR,
                                 "r8": KIT_CELLULE})
    controle("V2d.sys-04:au-geste-meme-les-trois-ssn-suivent",
             [c["ssn"] for c in noyau.captures] == [0x55, 0x56, 0x56, 0xAA, 0xBB, 0xBB],
             "« NtDeviceIoControlFile » résolu DEUX FOIS par appel — jamais "
             "un numéro en cache (Q3, charte § 6)")

    # I5 : l'échec de résolution du GESTE 1 = AUCUN syscall émis
    r, attendus, cellule, _ = jouer_sys04(forger_module([("NtClose", 3)]))
    rax_att, rdx_att, nb_att, pose_att = attendus
    controle("V2d.sys-04:resolution-1-echouee-moins-1",
             r["rax"] == -1 and r["rdx"] == L.V_NOM_ABSENT
             and len(noyau.captures) == 0 and cellule == int.from_bytes(
                 emu.CANARI * 8, "little"),
             "« NtCreateFile » absent : rax = -1, rdx = LA CAUSE, le compteur "
             "syscall À ZÉRO (I5), la cellule canariée INTACTE")

    # le geste 2 : le create est émis (UN syscall), le bind jamais
    r, attendus, cellule, _ = jouer_sys04(forger_module(
        [("NtCreateFile", SSN_NT_CREATEFILE)]))
    controle("V2d.sys-04:resolution-2-echouee-la-marche-s-arrete",
             r["rax"] == -1 and r["rdx"] == L.V_NOM_ABSENT
             and len(noyau.captures) == 1 and cellule == int.from_bytes(
                 emu.CANARI * 8, "little"),
             "« NtDeviceIoControlFile » absent : le create parti, le bind "
             "JAMAIS (I5/I6), le handle JAMAIS posé (Q4)")

    # le geste 3 : le module CHANGE sous les pieds (le noyau corrompt le
    # MOTIF DU STUB au bind — la mémoire vit) — la TROISIÈME résolution doit
    # échouer -4 stub divergent (Q3 : jamais un numéro en cache)
    mod = forger_module([("NtCreateFile", SSN_NT_CREATEFILE),
                         ("NtDeviceIoControlFile", SSN_NT_IOCTL)])
    stub_va = MODULE_BASE + mod.noms["NtDeviceIoControlFile"]["stub_rva"]
    r, attendus, cellule, _ = jouer_sys04(
        mod, afd_modes={"bind": ("sabotage", 0)}, sabotage_va=stub_va)
    controle("V2d.sys-04:resolution-3-echouee-le-module-change",
             r["rax"] == -1 and r["rdx"] == L.V_STUB_DIVERGENT
             and len(noyau.captures) == 2 and cellule == int.from_bytes(
                 emu.CANARI * 8, "little") and not emu.ecritures_module,
             "le stub corrompu PAR LE NOYAU au bind : la 3e résolution rend "
             "-4 (create et bind partis — 2 syscalls), rax = -1 LA CAUSE, la "
             "cellule INTACTE (Q4), le bloc n'a RIEN écrit dans le module")

    # Q4 : -6 le STATUS brut consigné à CHAQUE étage, la cellule INTACTE
    for geste, status, attendus_sys in (
            ("create", 0xC0000034, 1), ("bind", 0xC0000094, 2),
            ("connect", 0xC0000236, 3)):
        r, attendus, cellule, _ = jouer_sys04(MOD_COMPLET,
                                              afd_modes={geste: ("status", status)})
        controle(f"V2d.sys-04:status-{geste}-moins-6-consigne",
                 r["rax"] == L.V_STATUS_NONNUL and s64(r["rdx"]) == status
                 and len(noyau.captures) == attendus_sys
                 and cellule == int.from_bytes(emu.CANARI * 8, "little"),
                 f"-6 au {geste} : rdx = {status:#x} le BRUT consigné, "
                 "le handle n'est PAS posé (aucune possession partielle — Q4)")

    # la divergence iosb au create : le noyau ne parle pas deux fois
    r, attendus, cellule, _ = jouer_sys04(
        MOD_COMPLET, afd_modes={"create": ("divergence", 0xC0000094)})
    controle("V2d.sys-04:divergence-iosb-create",
             r["rax"] == L.V_STATUS_NONNUL and s64(r["rdx"]) == 0xC0000094
             and cellule == int.from_bytes(emu.CANARI * 8, "little"),
             "rax = 0 mais l'IOSB rend 0xC0000094 : un désaccord est une "
             "anomalie — le BRUT de l'IOSB consigné en rdx")

    section("V2e — sys-05 : l'émission au noyau AFD simulé")
    CHARGE = bytes((i * 7 + 3) & 0xFF for i in range(16406))  # 5 + 2^14 + 17
    emu.uc.mem_write(KIT_CHARGE - 0x100, emu.CANARI * 0x100)
    emu.uc.mem_write(KIT_CHARGE, CHARGE)
    emu.uc.mem_write(KIT_CHARGE + len(CHARGE), emu.CANARI * 0x100)

    def jouer_sys05(module, mode="succes", compte=None, charge=CHARGE,
                    ptr=KIT_CHARGE, longueur=None, r9_defaut=None):
        emu.poser_module(module)
        avant = module.empreinte()
        afd.reinit()
        afd.handle = HANDLE_AFD               # l'endpoint EST établi (sys-04)
        afd.longueur_attendue = len(charge) if longueur is None else longueur
        if mode == "partiel":
            afd.modes["send"] = ("partiel", compte)
        elif mode in ("status", "divergence"):
            afd.modes["send"] = (mode, compte)
        noyau.dispatch = {SSN_NT_IOCTL: afd.ioctl}
        noyau.captures.clear()
        entree = RSP0 - 0x100
        emu.surveillance_basse = (entree - 0x200, entree - 0xA8)
        emu.ecritures_basses = []
        args = {"rcx": MODULE_BASE, "rdx": HANDLE_AFD, "r8": ptr,
                "r9": r9_defaut if r9_defaut is not None else afd.longueur_attendue}
        r = emu.appeler(L.SYS05_VA, args)
        emu.surveillance_basse = None
        attendus = modele_sys05(module, mode,
                                compte if compte is not None else 0,
                                rdx_span=(r9_defaut == 0 or ptr == 0))
        return r, attendus, avant

    MOD_IOCTL = forger_module([("NtClose", 0x0F),
                                ("NtDeviceIoControlFile", SSN_NT_IOCTL)])

    # Q1 : TOUT est émis — la charge MAXIMALE d'un enregistrement TLS
    r, attendus, avant = jouer_sys05(MOD_IOCTL)
    controle("V2e.sys-05:totale-emise-rax-0",
             not r["crash"] and r["rax"] == 0 and len(noyau.captures) == 1
             and afd.emis == CHARGE,
             f"le noyau a lu {len(afd.emis)} o == la demande : 16406 "
             "[5 + 2^14 + 17] — la borne du jalon tient d'un geste")
    controle("V2e.sys-05:aucune-copie-le-wsabuf-pointe-le-kit",
             afd.charge_vue == KIT_CHARGE and CHARGE == bytes(
                 emu.uc.mem_read(KIT_CHARGE, len(CHARGE)))
             and bytes(emu.uc.mem_read(KIT_CHARGE - 0x100, 0x100)) == emu.CANARI * 0x100,
             "le WSABUF pointe LA CHARGE du kit (P3 traverse — I2), les "
             "canaris autour INTACTS : le bloc n'y a JAMAIS touché")
    controle("V2e.sys-05:les-dix-arguments-nt",
             noyau.captures[0]["handle"] == HANDLE_AFD
             and noyau.captures[0]["arg2"] == 0
             and noyau.captures[0]["arg3"] == 0
             and noyau.captures[0]["arg4"] == 0
             and noyau.captures[0]["arg6"] == L.IOCTL_AFD_SEND
             and noyau.captures[0]["arg8"] == L.AFD_SENDRECV_TAILLE
             and noyau.captures[0]["arg9"] == 0
             and noyau.captures[0]["arg10"] == 0,
             "handle, Event/Apc/Context NULL, l'IOCTL du plan, 24, NULL, 0 (Q4)")
    controle("V2e.sys-05:non-volatils-pile-module",
             all(r[k] == v for k, v in SENTINELLES_NV.items())
             and r.get("canaris_haut")
             and not fautes_sous_cadre(emu, L.SYS05_VA, L.SLOTS_SYS["g90005"][1])
             and avant == hashlib.sha256(
                 emu.uc.mem_read(MODULE_BASE, emu.module.taille)).hexdigest()[:16]
             and not emu.ecritures_module,
             "rbx/rbp/rdi/rsi rendus (I6), AUCUNE écriture sous le cadre hors "
             "les pushes des DEUX call et les trames des blocs PRUVÉS, "
             "l'EAT intacte")

    # Q2 : l'émission PARTIELLE est LE REFUS -7 (le compte consigné)
    r, attendus, avant = jouer_sys05(MOD_IOCTL, mode="partiel", compte=16403)
    controle("V2e.sys-05:partielle-refusee-moins-7",
             r["rax"] == L.V_TRANSPORT_ECHEC and r["rdx"] == 16403,
             "le noyau a pris 16403 sur 16406 : -7, rdx = LE COMPTE — jamais "
             "une boucle silencieuse (le kit tranche de la suite)")
    r, attendus, avant = jouer_sys05(MOD_IOCTL, mode="partiel", compte=0)
    controle("V2e.sys-05:rien-parti-moins-7-compte-nul",
             r["rax"] == L.V_TRANSPORT_ECHEC and r["rdx"] == 0,
             "zéro octet parti : le refus -7 aussi — rdx = 0 consigné")

    # Q5 : -6 le STATUS brut, -6 la divergence iosb
    r, attendus, avant = jouer_sys05(MOD_IOCTL, mode="status",
                                     compte=STATUS_ACCES_REFUSE)
    controle("V2e.sys-05:status-moins-6-consigne",
             r["rax"] == L.V_STATUS_NONNUL and s64(r["rdx"]) == STATUS_ACCES_REFUSE,
             f"rdx = {STATUS_ACCES_REFUSE:#x} le BRUT — nommé, jamais muet")
    r, attendus, avant = jouer_sys05(MOD_IOCTL, mode="divergence",
                                     compte=0xC0000094)
    controle("V2e.sys-05:divergence-iosb-moins-6",
             r["rax"] == L.V_STATUS_NONNUL and s64(r["rdx"]) == 0xC0000094,
             "le noyau ne parle pas deux fois")

    # I5/I3 : -1 la résolution, AUCUN syscall ; -5 le span (la garde d'abord)
    r, attendus, avant = jouer_sys05(forger_module([("NtClose", 3)]))
    controle("V2e.sys-05:resolution-echouee-moins-1",
             r["rax"] == -1 and r["rdx"] == L.V_NOM_ABSENT
             and len(noyau.captures) == 0, "la cause consignée, 0 syscall (I5)")
    for nom, ptr, lon in (("pointeur-nul", 0, 100), ("longueur-nulle", KIT_CHARGE, 0)):
        r, attendus, avant = jouer_sys05(MOD_IOCTL, ptr=ptr, r9_defaut=lon)
        controle(f"V2e.sys-05:span-invalide-{nom}-moins-5",
                 r["rax"] == L.V_SPAN_INVALIDE and len(noyau.captures) == 0,
                 "la garde AVANT tout : AUCUN syscall émis (charte § 5)")

    section("V2f — sys-06 : la réception au noyau AFD simulé")
    CAPACITE = 4096                       # 0x1000 — la capacité MESURÉE p.4
    RECU = bytes((i * 13 + 5) & 0xFF for i in range(100))
    emu.uc.mem_write(KIT_TAMPON, emu.CANARI * CAPACITE)

    def jouer_sys06(module, mode="succes", recu=RECU, compte=None,
                    ptr=KIT_TAMPON, capacite=CAPACITE, r9_defaut=None):
        emu.poser_module(module)
        avant = module.empreinte()
        afd.reinit()
        afd.handle = HANDLE_AFD
        afd.capacite_attendue = capacite
        afd.recu_pose = recu
        if mode == "demi-fin":
            afd.modes["recv"] = ("demi-fin", 0)
        elif mode in ("status", "divergence"):
            afd.modes["recv"] = (mode, compte)
        noyau.dispatch = {SSN_NT_IOCTL: afd.ioctl}
        noyau.captures.clear()
        entree = RSP0 - 0x100
        emu.surveillance_basse = (entree - 0x200, entree - 0xA8)
        emu.ecritures_basses = []
        args = {"rcx": MODULE_BASE, "rdx": HANDLE_AFD, "r8": ptr,
                "r9": r9_defaut if r9_defaut is not None else capacite}
        emu.uc.mem_write(KIT_TAMPON, emu.CANARI * capacite)   # le tampon vierge
        r = emu.appeler(L.SYS06_VA, args)
        emu.surveillance_basse = None
        attendus = modele_sys06(module, mode, len(recu),
                                compte if compte is not None else 0,
                                rdx_span=(r9_defaut == 0 or ptr == 0))
        return r, attendus, avant

    # Q1 : n rendu, le noyau a ÉCRIT chez le kit, le reçu INTÈGRE
    r, attendus, avant = jouer_sys06(MOD_IOCTL)
    tampon = bytes(emu.uc.mem_read(KIT_TAMPON, CAPACITE))
    controle("V2f.sys-06:n-octets-rendus",
             not r["crash"] and r["rax"] == 100 and len(noyau.captures) == 1,
             "rax = 100 = le compte du IOSB (n ≥ 1 — Q1), UN syscall")
    controle("V2f.sys-06:le-noyau-ecrit-chez-le-kit-recu-integre",
             tampon[:100] == RECU and tampon[100:] == emu.CANARI * (CAPACITE - 100)
             and afd.charge_vue == KIT_TAMPON,
             "les 100 o du noyau INTACTS chez le kit (I8), le RESTE du tampon "
             "canarié INTACT (I7 : rien de caché — le noyau n'a pas livré plus)")
    controle("V2f.sys-06:les-dix-arguments-nt",
             noyau.captures[0]["arg6"] == L.IOCTL_AFD_RECEIVE
             and noyau.captures[0]["arg8"] == L.AFD_SENDRECV_TAILLE
             and not afd.ecarts,
             f"l'IOCTL du plan, la taille 24, Aucun écart : {afd.ecarts}"
             if afd.ecarts else "l'IOCTL du plan, la taille 24, le noyau strict VERT")
    controle("V2f.sys-06:non-volatils-pile-module",
             all(r[k] == v for k, v in SENTINELLES_NV.items())
             and r.get("canaris_haut")
             and not fautes_sous_cadre(emu, L.SYS06_VA, L.SLOTS_SYS["g90006"][1])
             and avant == hashlib.sha256(
                 emu.uc.mem_read(MODULE_BASE, emu.module.taille)).hexdigest()[:16]
             and not emu.ecritures_module,
             "rbx/rbp/rdi/rsi rendus (I6), AUCUNE écriture sous le cadre hors "
             "les pushes des DEUX call et les trames des blocs PRUVÉS, "
             "l'EAT intacte")

    # Q2 : LE ZÉRO EST LA DEMI-FIN — le refus -7, rdx = 0, le tampon VIERGE
    r, attendus, avant = jouer_sys06(MOD_IOCTL, mode="demi-fin", recu=b"")
    controle("V2f.sys-06:demi-fin-moins-7",
             r["rax"] == L.V_TRANSPORT_ECHEC and r["rdx"] == 0
             and bytes(emu.uc.mem_read(KIT_TAMPON, 32)) == emu.CANARI * 32,
             "le pair a fermé : -7 NOMMÉ, rdx = 0 le compte consigné — jamais "
             "un succès silencieux (le kit tranche)")

    # Q5 : STATUS_CONNECTION_RESET — le pair a coupé BRUTALEMENT
    r, attendus, avant = jouer_sys06(MOD_IOCTL, mode="status",
                                     compte=STATUS_CNX_REINIT)
    controle("V2f.sys-06:connexion-reset-moins-6-consigne",
             r["rax"] == L.V_STATUS_NONNUL and s64(r["rdx"]) == STATUS_CNX_REINIT,
             f"rdx = {STATUS_CNX_REINIT:#x} (STATUS_CONNECTION_RESET) — "
             "l'exemple NOMMÉ de la spec, jamais muet")
    r, attendus, avant = jouer_sys06(MOD_IOCTL, mode="divergence",
                                     compte=0xC0000094)
    controle("V2f.sys-06:divergence-iosb-moins-6",
             r["rax"] == L.V_STATUS_NONNUL and s64(r["rdx"]) == 0xC0000094,
             "le noyau ne parle pas deux fois")

    # I5 : -1 la résolution ; -5 le span (la garde d'abord)
    r, attendus, avant = jouer_sys06(forger_module([("NtClose", 3)]))
    controle("V2f.sys-06:resolution-echouee-moins-1",
             r["rax"] == -1 and r["rdx"] == L.V_NOM_ABSENT
             and len(noyau.captures) == 0, "la cause consignée, 0 syscall (I5)")
    for nom, ptr, cap in (("pointeur-nul", 0, 100), ("capacite-nulle", KIT_TAMPON, 0)):
        r, attendus, avant = jouer_sys06(MOD_IOCTL, ptr=ptr, r9_defaut=cap)
        controle(f"V2f.sys-06:span-invalide-{nom}-moins-5",
                 r["rax"] == L.V_SPAN_INVALIDE and len(noyau.captures) == 0,
                 "la garde AVANT tout : AUCUN syscall émis")

    del afd


# --- V3 : le fuzzing à propriétés ---------------------------------------------------

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"


def vecteur_v3(emu: Emulateur, noyau: Noyau, rng: random.Random, volume: int):
    section(f"V3 — fuzzing à propriétés ({volume} modules en graine)")
    noyau.captures.clear()
    ecarts, cas = [], 0
    ESPACE = RSP0 + 0x100
    for _ in range(volume):
        nb = rng.randint(0, 8)
        cible_presente = rng.random() < 0.6
        noms: list[tuple[str, int]] = []
        for i in range(nb):
            if cible_presente and i == rng.randrange(nb or 1):
                nom = "NtWriteFile" if rng.random() < 0.7 else \
                    "NtWriteFil" + rng.choice("ex")
            else:
                taille = rng.randint(1, 14)
                nom = "Nt" + "".join(rng.choice(ALPHABET) for _ in range(taille))
            noms.append((nom, rng.randint(1, 0xFFF)))
        if cible_presente and not any(n == "NtWriteFile" for n, _ in noms):
            noms.insert(rng.randint(0, len(noms)), ("NtWriteFile", rng.randint(1, 0xFFF)))
        knobs = {
            "e_lfanew": rng.choice([0x80, 0x40, 0x400, 0x100,
                                    rng.randint(0x41, 0x3FF)]),
            "sig_pe": rng.random() > 0.1,
            "export_absente": rng.random() < 0.1,
            "crochete": rng.random() < 0.2,
        }
        cible_crochetee = "NtWriteFile" if (
            knobs["crochete"] and any(n == "NtWriteFile" for n, _ in noms)
            and rng.random() < 0.7) else None
        mod = forger_module(noms, e_lfanew=knobs["e_lfanew"],
                            sig_pe=knobs["sig_pe"],
                            export_absente=knobs["export_absente"],
                            stub_trop=cible_crochetee)
        span_choix = rng.random()
        if span_choix < 0.5:
            span = b"NtWriteFile"
        elif span_choix < 0.65:
            span = b"NtWriteFile"[:rng.randint(1, 10)]
        elif span_choix < 0.8:
            span = bytes(rng.choice(ALPHABET.encode())
                         for _ in range(rng.randint(1, 12)))
        else:
            span = b""                      # le span invalide
        emu.uc.mem_write(ESPACE, span + b"\x00" * 48)
        emu.poser_module(mod)
        empreinte_avant = mod.empreinte()
        r = emu.appeler(L.SYS02_VA, {"rcx": ESPACE if span else 0,
                                     "rdx": len(span), "r8": MODULE_BASE})
        cas += 1
        verdict, ssn, stub_va = modele_resoudre(mod, span or None)
        rax_att, rdx_att = attendus_du_modele((verdict, ssn, stub_va))
        ok = (not r["crash"] and r["rax"] == rax_att
              and (rdx_att is None or r["rdx"] == rdx_att))
        intact = hashlib.sha256(
            emu.uc.mem_read(MODULE_BASE, mod.taille)).hexdigest()[:16] == empreinte_avant
        if not ok or not intact or emu.lectures_nbnoms > 1 or noyau.captures:
            ecarts.append((span, verdict, r.get("rax"), r.get("rdx"),
                           r.get("crash"), intact))
    controle("V3.fuzz:modele-contre-emulation", not ecarts,
             f"{cas} cas, 0 écart" if not ecarts else
             f"{len(ecarts)} écart(s) — premier : {ecarts[0]}")
    controle("V3.fuzz:integrite-et-gardes",
             not emu.ecritures_module and len(noyau.captures) == 0,
             "aucune écriture module, aucun syscall émis, "
             "NumberOfNames lu une fois par appel")


# --- V3b : le fuzzing du TRANSPORT à propriétés (le modèle marche la séquence) ---

def vecteur_v3_transport(emu: Emulateur, noyau: Noyau, rng: random.Random,
                         volume: int):
    section(f"V3b — fuzzing transport à propriétés ({volume * 3} cas en graine)")
    afd = NoyauAFD(noyau)
    SOCKADDR_KIT = sockaddr_kit(80, bytes([192, 168, 1, 1]))
    STATUSES = [STATUS_ACCES_REFUSE, 0xC0000094, 0xC0000034, 0xC0000236,
                STATUS_CNX_REINIT]
    ecarts, cas = [], 0

    def mode_aleatoire():
        u = rng.random()
        if u < 0.55:
            return ("succes", 0)
        if u < 0.8:
            return ("status", rng.choice(STATUSES))
        return ("divergence", 0xC0000094)

    def module_transport_aleatoire():
        noms = []
        ssns_tires = set()

        def ssn_unique():                  # JAMAIS de collision : le dispatch
            while True:                   # du noyau suit LES SSN du module
                s = rng.randint(1, 0xFFF)
                if s not in ssns_tires:
                    ssns_tires.add(s)
                    return s
        for nom in ("NtCreateFile", "NtDeviceIoControlFile"):
            if rng.random() < 0.85:
                noms.append((nom, ssn_unique()))
        for i in range(rng.randint(0, 3)):             # les leurres hostiles
            taille = rng.randint(2, 20)
            noms.append(("Nt" + "".join(rng.choice(ALPHABET)
                                       for _ in range(taille)),
                         ssn_unique()))
        rng.shuffle(noms)
        crochet = None
        if rng.random() < 0.12:                        # le stub crocheté
            presentes = [n for n, _ in noms
                         if n in ("NtCreateFile", "NtDeviceIoControlFile")]
            if presentes:
                crochet = rng.choice(presentes)
        return forger_module(noms, stub_trop=crochet)

    def dispatch_transport(mod: ModuleFixe) -> dict:
        """Le noyau connaît les SSN DU MODULE (aléatoires — jamais des
        constantes de harnais : la résolution est la SEULE source du
        numéro, le dispatch suit la fixture, miroir de la Q2 au geste
        même)."""
        d = {}
        if "NtCreateFile" in mod.noms:
            d[mod.noms["NtCreateFile"]["ssn"]] = afd.creer
        if "NtDeviceIoControlFile" in mod.noms:
            d[mod.noms["NtDeviceIoControlFile"]["ssn"]] = afd.ioctl
        return d

    # --- sys-04 : la marche create→bind→connect contre le modèle ------------------
    for _ in range(volume):
        mod = module_transport_aleatoire()
        emu.poser_module(mod)
        avant = mod.empreinte()
        afd.reinit()
        for geste in ("create", "bind", "connect"):
            afd.modes[geste] = mode_aleatoire()
        afd.sockaddr_attendu = SOCKADDR_KIT
        emu.uc.mem_write(KIT_SOCKADDR, SOCKADDR_KIT + emu.CANARI * 0x40)
        emu.uc.mem_write(KIT_CELLULE - 0x20, emu.CANARI * 0x60)
        noyau.dispatch = dispatch_transport(mod)
        noyau.captures.clear()
        r = emu.appeler(L.SYS04_VA, {"rcx": MODULE_BASE, "rdx": KIT_SOCKADDR,
                                     "r8": KIT_CELLULE})
        cellule = struct.unpack("<Q", emu.uc.mem_read(KIT_CELLULE, 8))[0]
        rax_att, rdx_att, nb_att, pose_att = modele_sys04(mod, afd.modes)
        cas += 1
        ok = not r["crash"] and r["rax"] == rax_att and len(noyau.captures) == nb_att
        if rax_att < 0:
            ok = ok and r["rdx"] == rdx_att
        if pose_att:
            ok = ok and cellule == HANDLE_AFD and afd.poignee_etablie
        else:
            ok = ok and cellule == int.from_bytes(emu.CANARI * 8, "little")
        intact = hashlib.sha256(emu.uc.mem_read(
            MODULE_BASE, mod.taille)).hexdigest()[:16] == avant
        if not ok or not intact or afd.ecarts:
            ecarts.append(("sys-04", rax_att, r.get("rax"), r.get("rdx"),
                            len(noyau.captures), afd.ecarts[:2], r.get("crash")))

    # --- sys-05 / sys-06 : les verdicts d'échange contre le modèle -----------------
    for _ in range(volume):
        for bid, va, mode_set in (("g90005", L.SYS05_VA, "send"),
                                  ("g90006", L.SYS06_VA, "recv")):
            mod = module_transport_aleatoire()
            emu.poser_module(mod)
            avant = mod.empreinte()
            afd.reinit()
            afd.handle = HANDLE_AFD
            u = rng.random()
            if mode_set == "send":
                longueur = rng.randint(1, 16406)
                charge = bytes((i * 7 + 3) & 0xFF for i in range(longueur))
                emu.uc.mem_write(KIT_CHARGE - 0x40, emu.CANARI * 0x40)
                emu.uc.mem_write(KIT_CHARGE, charge)
                afd.longueur_attendue = longueur
                if u < 0.5:
                    mode, compte = "succes", longueur
                elif u < 0.7:
                    mode, compte = "partiel", rng.randint(0, longueur - 1)
                else:
                    mode, compte = ("status" if u < 0.85 else "divergence",
                                    rng.choice(STATUSES))
                afd.modes["send"] = (mode, compte)
                args = {"rcx": MODULE_BASE, "rdx": HANDLE_AFD,
                        "r8": KIT_CHARGE, "r9": longueur}
                rax_att, rdx_att, nb_att = modele_sys05(mod, mode, compte)
            else:
                capacite = rng.randint(1, 4096)
                n = rng.randint(0, capacite)
                recu = bytes((i * 13 + 5) & 0xFF for i in range(n))
                emu.uc.mem_write(KIT_TAMPON, emu.CANARI * capacite)
                afd.capacite_attendue = capacite
                afd.recu_pose = recu
                if u < 0.5 and n >= 1:
                    mode, compte = "succes", n
                elif u < 0.7:
                    mode, compte = "demi-fin", 0
                else:
                    mode, compte = ("status" if u < 0.85 else "divergence",
                                    rng.choice(STATUSES))
                afd.modes["recv"] = (mode, compte)
                args = {"rcx": MODULE_BASE, "rdx": HANDLE_AFD,
                        "r8": KIT_TAMPON, "r9": capacite}
                rax_att, rdx_att, nb_att = modele_sys06(mod, mode, n, compte)
            noyau.dispatch = dispatch_transport(mod)
            noyau.captures.clear()
            r = emu.appeler(va, args)
            cas += 1
            ok = not r["crash"] and r["rax"] == rax_att \
                and len(noyau.captures) == nb_att
            if rax_att < 0:
                ok = ok and r["rdx"] == rdx_att
            intact = hashlib.sha256(emu.uc.mem_read(
                MODULE_BASE, mod.taille)).hexdigest()[:16] == avant
            if not ok or not intact or afd.ecarts:
                ecarts.append((bid, rax_att, r.get("rax"), r.get("rdx"),
                               len(noyau.captures), afd.ecarts[:2], r.get("crash")))

    controle("V3b.fuzz-transport:modele-contre-emulation", not ecarts,
             f"{cas} cas, 0 écart — chaque verdict (-1/-4/-5/-6/-7, n, 0) "
             "prédit par le modèle de la couche I, consigné en rdx quand "
             "il est négatif, le noyau strict SANS AUCUN écart" if not ecarts
             else f"{len(ecarts)} écart(s) — premier : {ecarts[0]}")


# --- V4 : la falsification ----------------------------------------------------------

def octets_mutants(emu: Emulateur, bid: str, mutations: list[tuple[str, int, bytes]]):
    """Applique des mutations D'UN OCTET (stables en taille — leçon D82) aux
    octets ASSEMBLÉS du bloc (offset relatif au début du code)."""
    base = {"g90001": L.SYS01_VA, "g90002": L.SYS02_VA, "g90003": L.SYS03_VA}[bid]
    octets = bytearray(emu.octets_blocs[bid])
    noms = []
    for nom, offset, patch in mutations:
        octets[offset:offset + len(patch)] = patch
        noms.append(nom)
    return base, bytes(octets), noms


def vecteur_v4(emu: Emulateur, noyau: Noyau):
    section("V4 — falsification : un point muté, le différentiel attrape")
    ks = emu.ks

    def octets_de(src: str) -> bytes:
        """Assemble l'ancre au geste même (jamais une supposition d'encodage)."""
        enc, _ = ks.asm(src, 0)
        return bytes(enc)

    # --- sys-01 : les mutations du trombone (six octets — offsets connus)
    sys01 = emu.octets_blocs["g90001"]
    assert sys01 == bytes.fromhex("4989ca0f05c3"), sys01.hex()
    mutations_01 = [
        ("r10-recoit-rdx (le mauvais registre)", 0, bytes.fromhex("4989d2")),
        ("r10-recoit-r8 (le troisieme)", 0, bytes.fromhex("4d89c2")),
        ("syscall-nop-nop (aucune emission)", 3, b"\x90\x90"),
        ("ret-int3 (le retour rompu)", 5, b"\xcc"),
    ]

    def ntwritefile(uc, a):
        noyau.lignes_emises.append(bytes(uc.mem_read(a["arg6"], a["arg7"])))
        uc.mem_write(a["arg5"], struct.pack("<QQ", 0, a["arg7"]))
        uc.reg_write(UC_X86_REG_RAX, 0)

    def ntwritefile_divergent(uc, a):
        uc.reg_write(UC_X86_REG_RAX, 0)
        uc.mem_write(a["arg5"], struct.pack("<QQ", 0xC0000094, 0))

    mod = forger_module([("NtWriteFile", 0x31A)])
    emu.poser_module(mod)
    noyau.dispatch = {0x31A: ntwritefile}

    for nom, offset, patch in mutations_01:
        octets = bytearray(sys01)
        octets[offset:offset + len(patch)] = patch
        emu.reposer_bloc(L.SYS01_VA, bytes(octets))
        noyau.captures.clear()
        noyau.lignes_emises.clear()
        r = emu.appeler(L.SYS03_VA, {"rcx": MODULE_BASE, "rdx": HANDLE_MAGIQUE})
        cap = noyau.captures[-1] if noyau.captures else {}
        attrape = (r["crash"] or r["rax"] != 0
                   or cap.get("handle") != HANDLE_MAGIQUE
                   or len(noyau.captures) != 1
                   or (noyau.lignes_emises
                       and noyau.lignes_emises[-1] != L.TXT_SYS_LIGNE[:33]))
        controle(f"V4.sys-01:{nom}", attrape,
                 "la twin mutée trahit le différentiel" if attrape else
                 f"PAS ATTRAPÉE — rax={r['rax']}, capture={cap}")
        emu.reposer_bloc(L.SYS01_VA, sys01)     # le témoin restauré

    # le témoin intact reste vert
    noyau.captures.clear()
    noyau.lignes_emises.clear()
    r = emu.appeler(L.SYS03_VA, {"rcx": MODULE_BASE, "rdx": HANDLE_MAGIQUE})
    controle("V4.sys-01:temoin-intact-vert",
             not r["crash"] and r["rax"] == 0
             and noyau.lignes_emises[-1] == L.TXT_SYS_LIGNE[:33])

    # --- sys-02 : les mutations du résolveur (ancres assemblées au geste)
    sys02 = emu.octets_blocs["g90002"]

    def trouve(morceau: bytes) -> int:
        i = sys02.find(morceau)
        assert i >= 0, f"{morceau.hex()} introuvable dans sys-02"
        return i

    a_fenetre = octets_de("cmp r11d, 0x400")          # 41 81 FB imm32
    a_cmp_motif = octets_de("cmp dword ptr [rdx], 0xB8D18B4C")
    a_cmp_rax_r10 = octets_de("cmp rax, r10")         # le jae suit immédiatement
    off_fenetre = trouve(a_fenetre)
    off_verdict1 = trouve(octets_de("mov rax, -1"))   # 48 C7 C0 imm32
    off_jae = trouve(a_cmp_rax_r10) + len(a_cmp_rax_r10)
    off_jne_stub = trouve(a_cmp_motif) + len(a_cmp_motif)
    mutations_02 = [
        ("motif+1 (un hook serait accepté)", trouve(struct.pack("<I", 0xB8D18B4C)),
         struct.pack("<I", 0xB8D18B4D)),
        ("off-ssn-8 (le mauvais imm32)", trouve(octets_de("mov eax, dword ptr [rdx + 4]")),
         octets_de("mov eax, dword ptr [rdx + 8]")),
        ("fenetre-0x401 (la borne relâchée)", off_fenetre + 3,
         struct.pack("<I", 0x401)),
        ("verdict-mensonger (-1 rendu comme -3)", off_verdict1 + 3,
         struct.pack("<I", 0xFFFFFFFD)),
        ("marche-non-bornee (jae->jb)", off_jae, b"\x72"),
        ("motif-ignorer (jne->je)", off_jne_stub, b"\x74"),
    ]

    # la batterie : (module, span, rax ATTENDU — le SSN au succès, jamais 0)
    batterie = [
        (forger_module([("NtWrite", 0x0F), ("NtWriteFile", 0x31A)]),
         b"NtWriteFile", 0x31A),
        (forger_module([("NtWriteFile", 0x31A)], stub_trop="NtWriteFile"),
         b"NtWriteFile", L.V_STUB_DIVERGENT),
        (forger_module([("NtClose", 1)]), b"NtWriteFile", L.V_NOM_ABSENT),
        (forger_module([("NtWriteFile", 9)], e_lfanew=0x401),
         b"NtWriteFile", L.V_PAS_MODULE),
    ]

    for nom, offset, patch in mutations_02:
        octets = bytearray(sys02)
        octets[offset:offset + len(patch)] = patch
        emu.reposer_bloc(L.SYS02_VA, bytes(octets))
        ecarts = []
        for mod_c, span, rax_attendu in batterie:
            emu.poser_module(mod_c)
            emu.uc.mem_write(RSP0 + 0x100, span + b"\x00" * 48)
            r = emu.appeler(L.SYS02_VA, {"rcx": RSP0 + 0x100,
                                         "rdx": len(span), "r8": MODULE_BASE})
            if r["crash"] or r["rax"] != rax_attendu:
                ecarts.append((span, rax_attendu, r.get("rax"), r.get("crash")))
        controle(f"V4.sys-02:{nom}", bool(ecarts),
                 f"trahie sur {len(ecarts)}/4 cas" if ecarts else "PAS ATTRAPÉE — "
                 f"la batterie entière demeure verte sur la mutante")
        emu.reposer_bloc(L.SYS02_VA, sys02)     # le témoin restauré

    # le témoin intact reste vert sur la batterie
    ecarts = 0
    for mod_c, span, rax_attendu in batterie:
        emu.poser_module(mod_c)
        emu.uc.mem_write(RSP0 + 0x100, span + b"\x00" * 48)
        r = emu.appeler(L.SYS02_VA, {"rcx": RSP0 + 0x100, "rdx": len(span),
                                     "r8": MODULE_BASE})
        if r["crash"] or r["rax"] != rax_attendu:
            ecarts += 1
    controle("V4.sys-02:temoin-intact-vert", ecarts == 0,
             "les quatre cas de la batterie au témoin")

    # --- sys-03 : les mutations de la twin
    sys03 = emu.octets_blocs["g90003"]

    def trouve3(morceau: bytes) -> int:
        i = sys03.find(morceau)
        assert i >= 0, f"{morceau.hex()} introuvable dans sys-03"
        return i

    def trouve_appel(cible: int) -> int:
        """L'offset du call relatif qui vise la cible (le rel32 re-calculé)."""
        for i in range(len(sys03) - 5):
            if sys03[i] == 0xE8:
                rel = int.from_bytes(sys03[i + 1:i + 5], "little", signed=True)
                if L.SYS03_VA + i + 5 + rel == cible:
                    return i
        raise AssertionError(f"call vers {cible:#x} introuvable dans sys-03")

    a_len33 = octets_de("mov qword ptr [rsp + 0x30], 33")
    a_iosb = octets_de("cmp dword ptr [rsp + 0x48], 0")
    off_res = trouve_appel(L.SYS02_VA)                # résoudre…
    off_emi = trouve_appel(L.SYS01_VA)                # …puis émettre (I3)
    assert off_res < off_emi
    rel_sys01_premier = L.SYS01_VA - (L.SYS03_VA + off_res + 5)
    # (nom, offset, patch, le noyau du cas — le divergent pour la mutation iosb)
    mutations_03 = [
        ("longueur-32 (la ligne tronquée)",
         trouve3(a_len33) + 5, struct.pack("<I", 32), ntwritefile),
        ("handle-depuis-rbp (la base prise pour le handle)",
         trouve3(octets_de("mov rcx, rbx")), octets_de("mov rcx, rbp"),
         ntwritefile),
        ("span-nom-10 (le préfixe piège)",
         trouve3(octets_de("mov edx, 11")) + 1, struct.pack("<I", 10),
         ntwritefile),
        ("divergence-iosb-ignorée (jne->je)",
         trouve3(a_iosb) + len(a_iosb), b"\x74", ntwritefile_divergent),
        ("ordre-inverse (émettre avant résoudre)",
         off_res + 1, struct.pack("<i", rel_sys01_premier), ntwritefile),
    ]

    # le préfixe piège : « NtWriteFil » (10) attrape un autre export AVANT la cible
    mod_piege = forger_module([("NtClose", 0x0F), ("NtWriteFilter", 0x999),
                               ("NtWriteFile", 0x31A)])
    emu.poser_module(mod_piege)

    for nom, offset, patch, noyau_du_cas in mutations_03:
        octets = bytearray(sys03)
        octets[offset:offset + len(patch)] = patch
        emu.reposer_bloc(L.SYS03_VA, bytes(octets))
        noyau.dispatch = {0x31A: noyau_du_cas}
        noyau.captures.clear()
        noyau.lignes_emises.clear()
        r = emu.appeler(L.SYS03_VA, {"rcx": MODULE_BASE, "rdx": HANDLE_MAGIQUE})
        cap = noyau.captures[-1] if noyau.captures else {}
        attrape = (r["crash"] or r["rax"] != 0
                   or not noyau.lignes_emises
                   or noyau.lignes_emises[-1] != L.TXT_SYS_LIGNE[:33]
                   or cap.get("arg7") != 33 or cap.get("handle") != HANDLE_MAGIQUE)
        controle(f"V4.sys-03:{nom}", attrape,
                 "la twin mutée trahit le différentiel" if attrape else
                 f"PAS ATTRAPÉE — rax={r['rax']}, lignes={noyau.lignes_emises}")
        emu.reposer_bloc(L.SYS03_VA, sys03)     # le témoin restauré

    noyau.dispatch = {0x31A: ntwritefile}
    noyau.captures.clear()
    noyau.lignes_emises.clear()
    r = emu.appeler(L.SYS03_VA, {"rcx": MODULE_BASE, "rdx": HANDLE_MAGIQUE})
    controle("V4.sys-03:temoin-intact-vert",
             not r["crash"] and r["rax"] == 0
             and noyau.lignes_emises[-1] == L.TXT_SYS_LIGNE[:33])

    del ks


# --- V4b : la falsification du SOCLE (chantier M9-(d)) ------------------------------

def _offsets_saut(octets: bytes, va_base: int, court: int, long2: int,
                  cible: int) -> list[int]:
    """Tous les offsets des sauts (courts rel8 et longs rel32) vers la
    cible — keystone choisit la forme, le harnais les lit TOUTES."""
    out = []
    for i in range(len(octets) - 1):
        if octets[i] == court:
            rel = int.from_bytes(octets[i + 1:i + 2], "little", signed=True)
            if va_base + i + 2 + rel == cible:
                out.append(i)
        if i + 6 <= len(octets) and octets[i] == 0x0F and octets[i + 1] == long2:
            rel = int.from_bytes(octets[i + 2:i + 6], "little", signed=True)
            if va_base + i + 6 + rel == cible:
                out.append(i)
    return sorted(out)


def _patch_saut_inverse(octets: bytes, offset: int) -> tuple[int, bytes]:
    """L'inversion du sens du saut (je↔jne, jz↔jnz, js↔jns) — stable en
    taille : un octet muté, la cible demeure."""
    if octets[offset] == 0x0F:            # la forme longue : 0F 84/88 → 0F 85/89
        return offset + 1, bytes([octets[offset + 1] + 1])
    return offset, bytes([octets[offset] + 1])   # la courte : 74/78 → 75/79


def vecteur_v4_transport(emu: Emulateur, noyau: Noyau):
    section("V4b — falsification du socle : chaque mutante trahit la batterie")
    ks = emu.ks

    def octets_de(src: str) -> bytes:
        enc, _ = ks.asm(src, 0)
        return bytes(enc)

    def etiquette(nom_fichier, nom_etiquette):
        with open(os.path.join(ICI, "notation", nom_fichier + ".asm"),
                  encoding="utf-8") as f:
            entete = f.read()
        m = re.search(rf"\.{nom_etiquette}=0x([0-9a-f]+)", entete)
        assert m, f".{nom_etiquette} absente de l'en-tête de {nom_fichier}"
        return int(m.group(1), 16)

    afd = NoyauAFD(noyau)
    SOCKADDR_KIT = sockaddr_kit(80, bytes([192, 168, 1, 1]))
    MOD_COMPLET = forger_module([("NtClose", 0x0F),
                                 ("NtCreateFile", SSN_NT_CREATEFILE),
                                 ("NtDeviceIoControlFile", SSN_NT_IOCTL)])
    MOD_SANS_IOCTL = forger_module([("NtCreateFile", SSN_NT_CREATEFILE)])
    MOD_SANS_CREATE = forger_module([("NtClose", 3)])
    MOD_IOCTL_SEUL = forger_module([("NtClose", 0x0F),
                                    ("NtDeviceIoControlFile", SSN_NT_IOCTL)])
    CHARGE = bytes((i * 7 + 3) & 0xFF for i in range(16406))
    RECU = bytes((i * 13 + 5) & 0xFF for i in range(100))

    # --- sys-04 : la batterie et les mutations de l'établissement -----------------
    def cas_sys04(module, afd_modes=None):
        emu.poser_module(module)
        afd.reinit()
        if afd_modes:
            afd.modes.update(afd_modes)
        afd.sockaddr_attendu = SOCKADDR_KIT
        emu.uc.mem_write(KIT_SOCKADDR, SOCKADDR_KIT + emu.CANARI * 0x40)
        emu.uc.mem_write(KIT_CELLULE - 0x20, emu.CANARI * 0x60)
        noyau.dispatch = {SSN_NT_CREATEFILE: afd.creer, SSN_NT_IOCTL: afd.ioctl}
        noyau.captures.clear()
        r = emu.appeler(L.SYS04_VA, {"rcx": MODULE_BASE, "rdx": KIT_SOCKADDR,
                                     "r8": KIT_CELLULE})
        cellule = struct.unpack("<Q", emu.uc.mem_read(KIT_CELLULE, 8))[0]
        rax_att, rdx_att, nb_att, pose_att = modele_sys04(module, afd.modes)
        ok = (not r["crash"] and r["rax"] == rax_att
              and len(noyau.captures) == nb_att
              and (rax_att >= 0 or r["rdx"] == rdx_att))
        if pose_att:
            return ok and cellule == HANDLE_AFD
        return ok and cellule == int.from_bytes(emu.CANARI * 8, "little")

    BATTERIE_04 = [
        ("succès", lambda: cas_sys04(MOD_COMPLET)),
        ("bind-status", lambda: cas_sys04(
            MOD_COMPLET, {"bind": ("status", 0xC0000094)})),
        ("sans-create", lambda: cas_sys04(MOD_SANS_CREATE)),
        ("sans-ioctl", lambda: cas_sys04(MOD_SANS_IOCTL)),
        ("connect-status", lambda: cas_sys04(
            MOD_COMPLET, {"connect": ("status", 0xC0000236)})),
    ]

    sys04 = emu.octets_blocs["g90004"]

    def trouve04(morceau: bytes) -> int:
        i = sys04.find(morceau)
        assert i >= 0, f"{morceau.hex()} introuvable dans sys-04"
        return i

    a_desired = octets_de("mov edx, 0xC0140000")
    a_ioctl_bind = octets_de("mov qword ptr [rsp + 0x28], 0x12003")
    a_ioctl_connect = octets_de("mov qword ptr [rsp + 0x28], 0x12007")
    a_ea_len = octets_de("mov qword ptr [rsp + 0x50], 54")
    a_maxlen = octets_de("mov word ptr [rsp + 0xC2], 42")
    a_sockaddr = octets_de("mov r10, qword ptr [rdi + 8]")
    a_handle_src = octets_de("mov r10, qword ptr [rsp + 0x58]")
    a_iosb_create = octets_de("cmp dword ptr [rsp + 0x60], 0")
    js_echec = _offsets_saut(sys04, L.SYS04_VA, 0x78, 0x88,
                             etiquette("sys-04-transport", "resolution_echouee"))
    assert len(js_echec) == 3, f"{len(js_echec)} js vers .resolution_echouee"
    off_patch, patch_sens = _patch_saut_inverse(sys04, js_echec[1])
    mutations_04 = [
        ("desired-access-+1 (le noyau strict refuse)",
         trouve04(a_desired) + 1, struct.pack("<I", 0xC0140001)),
        ("ioctl-bind-inconnu (0x12003→0x12004)",
         trouve04(a_ioctl_bind) + len(a_ioctl_bind) - 4, struct.pack("<I", 0x12004)),
        ("ioctl-connect-confondu-bind (0x12007→0x12003)",
         trouve04(a_ioctl_connect) + len(a_ioctl_connect) - 4,
         struct.pack("<I", 0x12003)),
        ("ea-length-53 (le EA tronqué)",
         trouve04(a_ea_len) + len(a_ea_len) - 4, struct.pack("<I", 53)),
        ("device-maxlength-44 (l'erratum d'instrument rejoué)",
         trouve04(a_maxlen) + len(a_maxlen) - 2, struct.pack("<H", 44)),
        ("sockaddr-decale (+8→+16 : la copie au-delà du kit)",
         trouve04(a_sockaddr) + 3, b"\x10"),
        ("handle-fausse-source ([rsp+0x58]→[rsp+0x50])",
         trouve04(a_handle_src) + 4, b"\x50"),
        ("create-iosb-aveugle (0x60→0x70 : le mauvais IOSB relu)",
         trouve04(a_iosb_create) + 3, b"\x70"),
        ("resolution2-sautee (js→jns : la marche sans garde)",
         off_patch, patch_sens),
    ]

    for nom, offset, patch in mutations_04:
        octets = bytearray(sys04)
        octets[offset:offset + len(patch)] = patch
        emu.reposer_bloc(L.SYS04_VA, bytes(octets))
        trahis = [nom_cas for nom_cas, cas in BATTERIE_04 if not cas()]
        controle(f"V4b.sys-04:{nom}", bool(trahis),
                 f"trahie sur {len(trahis)}/5 ({', '.join(trahis)})"
                 if trahis else "PAS ATTRAPÉE — la batterie demeure verte")
        emu.reposer_bloc(L.SYS04_VA, sys04)     # le témoin restauré
    controle("V4b.sys-04:temoin-intact-vert",
             all(cas() for _, cas in BATTERIE_04),
             "les cinq cas de la batterie au témoin")

    # --- sys-05 : la batterie et les mutations de l'émission -----------------------
    def cas_sys05(module, mode="succes", compte=None, ptr=KIT_CHARGE, r9=None):
        emu.poser_module(module)
        afd.reinit()
        afd.handle = HANDLE_AFD
        afd.longueur_attendue = len(CHARGE)
        if mode in ("partiel", "status", "divergence"):
            afd.modes["send"] = (mode, compte)
        noyau.dispatch = {SSN_NT_IOCTL: afd.ioctl}
        noyau.captures.clear()
        emu.uc.mem_write(KIT_CHARGE, CHARGE)
        r = emu.appeler(L.SYS05_VA, {"rcx": MODULE_BASE, "rdx": HANDLE_AFD,
                                     "r8": ptr,
                                     "r9": r9 if r9 is not None else len(CHARGE)})
        rax_att, rdx_att, nb_att = modele_sys05(
            module, mode, compte if compte is not None else 0,
            rdx_span=(r9 == 0 or ptr == 0))
        return (not r["crash"] and r["rax"] == rax_att
                and len(noyau.captures) == nb_att
                and (rax_att >= 0 or rdx_att is None or r["rdx"] == rdx_att))

    BATTERIE_05 = [
        ("succès", lambda: cas_sys05(MOD_IOCTL_SEUL)),
        ("partiel", lambda: cas_sys05(MOD_IOCTL_SEUL, "partiel", 16403)),
        ("status", lambda: cas_sys05(MOD_IOCTL_SEUL, "status", STATUS_ACCES_REFUSE)),
        ("sans-nom", lambda: cas_sys05(MOD_SANS_CREATE)),
        ("span", lambda: cas_sys05(MOD_IOCTL_SEUL, ptr=0)),
    ]

    sys05 = emu.octets_blocs["g90005"]

    def trouve05(morceau: bytes) -> int:
        i = sys05.find(morceau)
        assert i >= 0, f"{morceau.hex()} introuvable dans sys-05"
        return i

    a_ioctl_send = octets_de("mov qword ptr [rsp + 0x28], 0x1201F")
    a_wsabuf_len = octets_de("mov dword ptr [rsp + 0x60], esi")
    a_compteur = octets_de("cmp qword ptr [rsp + 0x58], rsi")
    a_afdflags = octets_de("mov dword ptr [rsp + 0x7C], 0")
    je_span = _offsets_saut(sys05, L.SYS05_VA, 0x74, 0x84,
                            etiquette("sys-05-emission", "span_invalide"))
    assert len(je_span) == 2, f"{len(je_span)} je vers .span_invalide"
    off_patch, patch_sens = _patch_saut_inverse(sys05, je_span[0])
    mutations_05 = [
        ("ioctl-send-confondu-recv (0x1201F→0x12017)",
         trouve05(a_ioctl_send) + len(a_ioctl_send) - 4, struct.pack("<I", 0x12017)),
        ("wsabuf-len-pour-ptr (esi→edi : la longueur faussée)",
         trouve05(a_wsabuf_len), bytes.fromhex("897c2460")),
        ("compteur-compare-a-rax (rsi→rax : le partiel passe)",
         trouve05(a_compteur), bytes.fromhex("483b442458")),
        ("afdflags-0x20-au-send (le drapeau du recv, pas du send)",
         trouve05(a_afdflags) + len(a_afdflags) - 4, struct.pack("<I", 0x20)),
        ("span-garde-inversee (je→jne : le refus des sains)",
         off_patch, patch_sens),
    ]

    for nom, offset, patch in mutations_05:
        octets = bytearray(sys05)
        octets[offset:offset + len(patch)] = patch
        emu.reposer_bloc(L.SYS05_VA, bytes(octets))
        trahis = [nom_cas for nom_cas, cas in BATTERIE_05 if not cas()]
        controle(f"V4b.sys-05:{nom}", bool(trahis),
                 f"trahie sur {len(trahis)}/5 ({', '.join(trahis)})"
                 if trahis else "PAS ATTRAPÉE — la batterie demeure verte")
        emu.reposer_bloc(L.SYS05_VA, sys05)
    controle("V4b.sys-05:temoin-intact-vert",
             all(cas() for _, cas in BATTERIE_05),
             "les cinq cas de la batterie au témoin")

    # --- sys-06 : la batterie et les mutations de la réception ---------------------
    def cas_sys06(module, mode="succes", n=100, compte=None, ptr=KIT_TAMPON,
                  r9=None):
        emu.poser_module(module)
        afd.reinit()
        afd.handle = HANDLE_AFD
        afd.capacite_attendue = 4096
        afd.recu_pose = RECU[:n]
        if mode in ("demi-fin", "status", "divergence"):
            afd.modes["recv"] = (mode, compte)
        noyau.dispatch = {SSN_NT_IOCTL: afd.ioctl}
        noyau.captures.clear()
        emu.uc.mem_write(KIT_TAMPON, emu.CANARI * 4096)
        r = emu.appeler(L.SYS06_VA, {"rcx": MODULE_BASE, "rdx": HANDLE_AFD,
                                     "r8": ptr,
                                     "r9": r9 if r9 is not None else 4096})
        rax_att, rdx_att, nb_att = modele_sys06(
            module, mode, n, compte if compte is not None else 0,
            rdx_span=(r9 == 0 or ptr == 0))
        return (not r["crash"] and r["rax"] == rax_att
                and len(noyau.captures) == nb_att
                and (rax_att >= 0 or rdx_att is None or r["rdx"] == rdx_att))

    BATTERIE_06 = [
        ("succès", lambda: cas_sys06(MOD_IOCTL_SEUL)),
        ("demi-fin", lambda: cas_sys06(MOD_IOCTL_SEUL, "demi-fin", 0)),
        ("cnx-reset", lambda: cas_sys06(MOD_IOCTL_SEUL, "status", 100,
                                        STATUS_CNX_REINIT)),
        ("sans-nom", lambda: cas_sys06(MOD_SANS_CREATE)),
        ("span", lambda: cas_sys06(MOD_IOCTL_SEUL, ptr=0)),
    ]

    sys06 = emu.octets_blocs["g90006"]

    def trouve06(morceau: bytes) -> int:
        i = sys06.find(morceau)
        assert i >= 0, f"{morceau.hex()} introuvable dans sys-06"
        return i

    a_erratum = octets_de("mov dword ptr [rsp + 0x7C], 0")
    a_litterature = octets_de("mov dword ptr [rsp + 0x80], 0x20")
    a_ioctl_recv = octets_de("mov qword ptr [rsp + 0x28], 0x12017")
    a_wsabuf_buf = octets_de("mov qword ptr [rsp + 0x68], rdi")
    jz_demifin = _offsets_saut(sys06, L.SYS06_VA, 0x74, 0x84,
                               etiquette("sys-06-reception", "demi_fin"))
    assert len(jz_demifin) == 1, f"{len(jz_demifin)} jz vers .demi_fin"
    off_patch, patch_sens = _patch_saut_inverse(sys06, jz_demifin[0])
    mutations_06 = [
        ("LE-TERRAIN-falsifie (AfdFlags 0→0x20 : la mesure WinDbg "
         "rétablie — REFUSÉE par le VRAI noyau, Entrée 191)",
         trouve06(a_erratum) + len(a_erratum) - 4, struct.pack("<I", 0x20)),
        ("LE-TERRAIN-VIDÉ (TdiFlags 0x20→0 : le placement perdu)",
         trouve06(a_litterature) + len(a_litterature) - 4, struct.pack("<I", 0)),
        ("demi-fin-masquee (jz→jnz : le zéro déguisé en succès)",
         off_patch, patch_sens),
        ("ioctl-recv-confondu-send (0x12017→0x1201F)",
         trouve06(a_ioctl_recv) + len(a_ioctl_recv) - 4, struct.pack("<I", 0x1201F)),
        ("wsabuf-buf-pour-capacite (rdi→rsi : le tampon perdu)",
         trouve06(a_wsabuf_buf), bytes.fromhex("4889742468")),
    ]

    for nom, offset, patch in mutations_06:
        octets = bytearray(sys06)
        octets[offset:offset + len(patch)] = patch
        emu.reposer_bloc(L.SYS06_VA, bytes(octets))
        trahis = [nom_cas for nom_cas, cas in BATTERIE_06 if not cas()]
        controle(f"V4b.sys-06:{nom}", bool(trahis),
                 f"trahie sur {len(trahis)}/5 ({', '.join(trahis)})"
                 if trahis else "PAS ATTRAPÉE — la batterie demeure verte")
        emu.reposer_bloc(L.SYS06_VA, sys06)
    controle("V4b.sys-06:temoin-intact-vert",
             all(cas() for _, cas in BATTERIE_06),
             "les cinq cas de la batterie au témoin")

    del ks


# --- Le bilan -----------------------------------------------------------------------

def bilan(graine: int) -> int:
    total = len(REUSSITES) + len(ECHECS)
    empreinte = hashlib.sha256(
        ("|".join(REUSSITES) + "#" + "|".join(f"{n}:{d}" for n, d in ECHECS)
         + f"#{graine}").encode()).hexdigest()[:16]
    print("\n" + "=" * 70)
    print(f"BILAN : {total} contrôles · {len(REUSSITES)} verts · "
          f"{len(ECHECS)} échec(s) · empreinte {empreinte} · graine {graine}")
    if ECHECS:
        for nom, detail in ECHECS:
            print(f"  ÉCHEC : {nom} — {detail}")
    print("=" * 70)
    return 1 if ECHECS else 0


def executer(blobs: dict[str, bytes] | None = None, graine: int = 20261105,
             volume: str = "complet") -> dict:
    """Le point d'entrée du BUILD (modèle oracle_m5.executer — D136) : joue
    la batterie V1-V4 sur les blobs passés (ou les notations assemblées en
    mode autonome) et rend le verdict ; LÈVE ErreurHarnais sur TOUT échec
    (le build ne continue jamais sur un harnais non vert).

    -> {"total_cas", "verts", "empreinte", "graine", "volume"}"""
    global REUSSITES, ECHECS
    REUSSITES, ECHECS = [], []
    print(f"=== harnais_sys.py — le domaine sys noté-mesuré-prouvé "
          f"(M8, blobs {'du build' if blobs else 'locaux'}) ===")
    print(f"graine {graine} · volume {volume}")

    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    vecteur_v1(ks, cs)

    noyau = Noyau()
    emu = Emulateur(noyau, blobs=blobs)
    vecteur_v2(emu, noyau)
    vecteur_v3(emu, noyau, random.Random(graine),
               300 if volume == "complet" else 60)
    vecteur_v4(emu, noyau)
    # LE SOCLE SOCKET (chantier M9-(d)) : le noyau AFD strict, le fuzz
    # transport, la falsification des TROIS blocs — la graine dérivée
    # (jamais la même suite : chaque série de preuves vit seule)
    vecteur_v2d(emu, noyau)
    vecteur_v3_transport(emu, noyau, random.Random(graine ^ 0xA0A0),
                         120 if volume == "complet" else 40)
    vecteur_v4_transport(emu, noyau)
    if ECHECS:
        raise ErreurHarnais(
            f"harnais non vert : {len(ECHECS)} échec(s) — premier : "
            f"{ECHECS[0][0]} : {ECHECS[0][1]}")
    empreinte = hashlib.sha256(
        ("|".join(REUSSITES) + f"#{graine}").encode()).hexdigest()[:16]
    print(f"[harnais] {len(REUSSITES)} contrôles VERTS · empreinte "
          f"{empreinte} · graine {graine}")
    return {"total_cas": len(REUSSITES), "verts": len(REUSSITES),
            "empreinte": empreinte, "graine": graine, "volume": volume}


def main() -> int:
    ap = argparse.ArgumentParser(description="Harnais du domaine sys (M8)")
    ap.add_argument("--graine", type=int, default=20261105)
    ap.add_argument("--volume", choices=["complet", "reduit"], default="complet")
    args = ap.parse_args()
    executer(None, graine=args.graine, volume=args.volume)
    return bilan(args.graine)


if __name__ == "__main__":
    sys.exit(main())
