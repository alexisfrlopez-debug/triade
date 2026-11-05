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

  V3  fuzzing à propriétés : modules aléatoires en graine (noms, SSN,
      ordinals permutés, préfixes pièges, stubs crochetés, e_lfanew
      hostiles, cible en dernière position, doublons) — le MODÈLE (dérivé
      de la couche I et du plan, JAMAIS des octets de la notation) prédit
      le verdict, l'émulation confrontée ; l'intégrité du module et les
      non-volatils re-contrôlés à CHAQUE cas ;

  V4  falsification : les mutations D'UN SEUL point de chaque notation
      (stables en taille — leçon D82) doivent être ATTRAPÉES par le
      différentiel ; le témoin intact reste VERT — une suite qui ne peut
      pas échouer ne prouve rien.

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
# devant au sys.path pour build_m4 — jamais d'import anonyme ici)
_spec_l8 = importlib.util.spec_from_file_location(
    "layout_m8", os.path.join(ICI, "layout.py"))
L = importlib.util.module_from_spec(_spec_l8)
sys.modules["layout_m8"] = L
_spec_l8.loader.exec_module(L)

# La machinerie de notation de la lignée, importée par chemin (leçon D158 :
# les build.py homonymes se chargent par importlib, jamais par sys.path)
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

ZONE_CODE = (0x1000, 0xC000)      # .text/.rdata/.data/.text2-4/.text5 du plan
MODULE_BASE = 0x150000000         # le module ntdll synthétique (page exacte)
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP0 = 0x7F008000
RET_MAGIQUE = 0xBF00              # arrêt propre (hlt, dans la réserve .text5)
TRAMPOLINE_WF = 0xBF10            # la fausse WriteFile (mécanisme M2/M3)

HANDLE_MAGIQUE = 0x0000ABCD       # le handle d'écriture des deux chemins
STATUS_INVALIDE = 0xC000001C      # STATUS_INVALID_SYSTEM_SERVICE (SSN inconnu)

SENTINELLES_NV = {
    "rbx": 0x1212121212121212, "rbp": 0x2323232323232323,
    "rdi": 0x3434343434343434, "rsi": 0x4545454545454545,
    "r12": 0x5656565656565656, "r13": 0x6767676767676767,
    "r14": 0x7878787878787878, "r15": 0x8989898989898989,
}

REUSSITES, ECHECS = [], []


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
            "arg8": pile(0x40), "arg9": pile(0x48),
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


# --- L'émulateur ------------------------------------------------------------------

class Emulateur:
    """L'image du plan + les notations + le module + les traceurs."""

    def __init__(self, noyau: Noyau):
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
        for bid, (nom_fichier, _spec, _dep) in {
            "g90001": ("sys-01-emetteur", None, None),
            "g90002": ("sys-02-resolveur", None, None),
            "g90003": ("sys-03-ecriture", None, None),
        }.items():
            rva, slot = L.SLOTS_SYS[bid]
            chemin = os.path.join(ICI, "notation", nom_fichier + ".asm")
            octets, _metas = B4.assembler_bloc(self.ks, chemin, rva, slot)
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


def attendus_du_modele(modele):
    """Le modèle rend (verdict, ssn, stub_va) ; le bloc rend rax = LE SSN au
    succès (Q1 de sys-02 — jamais 0), rax = le verdict aux échecs ; rdx =
    l'adresse du stub au succès seulement (Q2)."""
    verdict, ssn, stub_va = modele
    if verdict == L.V_RESOLU:
        return ssn, stub_va
    return verdict, None


# --- V1 : le round-trip + la concordance des immdiats -----------------------------

def vecteur_v1(ks: Ks, cs: capstone.Cs):
    section("V1 — round-trip de notation + concordance au plan (source unique)")
    for bid, attendu in [("g90001", 6), ("g90002", 293), ("g90003", 164)]:
        nom_fichier = {"g90001": "sys-01-emetteur", "g90002": "sys-02-resolveur",
                       "g90003": "sys-03-ecriture"}[bid]
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


def main() -> int:
    ap = argparse.ArgumentParser(description="Harnais du domaine sys (M8-(b))")
    ap.add_argument("--graine", type=int, default=20261105)
    ap.add_argument("--volume", choices=["complet", "reduit"], default="complet")
    args = ap.parse_args()
    rng = random.Random(args.graine)
    print("=== harnais_sys.py — le domaine sys noté-mesuré-prouvé (M8-(b), D161) ===")
    print(f"graine {args.graine} · volume {args.volume}")

    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    vecteur_v1(ks, cs)

    noyau = Noyau()
    emu = Emulateur(noyau)
    vecteur_v2(emu, noyau)
    vecteur_v3(emu, noyau, rng,
               300 if args.volume == "complet" else 60)
    vecteur_v4(emu, noyau)
    return bilan(args.graine)


if __name__ == "__main__":
    sys.exit(main())
