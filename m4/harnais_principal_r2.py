#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_principal_r2.py — Harnais de la révision http-12:R2 (D95, LE CÂBLAGE).

Vecteurs de la spécification m4/I/http-12-principal-r2.md (écrite-avant-code) :
  V1  round-trip de notation 100 % — R2 (458 o == en-tête « Code : N o »,
      idempotence) ET l'ancêtre http-12:R1 scellé assemblé à 0x1800 (438 o
      déclarés) : le préalable du différentiel hérité ;
  V2  différentiel d'ancêtre — R1 émulé contre R2 émulé sur les MÊMES
      scénarios (chaque génération nourrie de SA table : 26 entrées +
      terminateur @0x2800 pour R1, 28 entrées + porte .text3 @0x2810 pour
      R2 — la porte est génération-spécifique, l'orchestration ne l'est pas) :
      traces IDENTIQUES sauf la cible du spawn session (0x5580 -> 0x74C0,
      LE CÂBLAGE) ; divergences LÉGITIMES vérifiées : la corruption .text3
      (R1 ne la garde pas, R2 la nomme KO — miroir du domaine https D91) ;
      l'ordre d'initialisation Q2 est constaté TRACE À TRACE (I2/D42), la
      porte précède tout effet (I3 : aucune entrée de trace avant GSH) ;
  V3  fuzz de la porte R10 — table et image mutées D'UN point : le modèle
      de marche (écrit depuis la SPÉCIFICATION) et l'émulation (les OCTETS)
      doivent NOMMER le même verdict, et toute mutation doit donner KO —
      jamais de passage silencieux ; les octets mutés évitent le code du
      bloc lui-même et les cinq trappes (la corruption du VÉRIFICATEUR
      n'est pas décidable par le vérificateur — miroir M3) ;
  V4  falsification — mutations d'un point de la notation STABLES EN TAILLE
      (leçon D82) attrapées : le contre-câblage (lea -> 0x5580 : la
      falsification nominale), la borne décalée ±0x10 (l'entrée .text3
      sautée, ou la version lue comme entrée), le plancher abaissé, le code
      de sortie E3, le sens du test d'arrêt ; témoin vert.

Le harnais émule les octets des NOTATIONS (R2 à 0x7DC0, l'ancêtre R1 scellé
0.4.0 à 0x1800 — R7 : l'ancêtre reste embarqué, mort au lancement de R2).
L'image d'émulation couvre 0x1000-0xA000 : remplissage int3, les DEUX
orchestrateurs, cinq trappes (hello-02, tcp-01/02/06/11) aux RVA réels,
fixtures .rdata héritées, état .data, IAT fausse, et LA TABLE R10 — les
sommes sont calculées sur l'image AVANT mutation (la mutation simule la
corruption POSTÉRIEURE au scellement).
Usage : python3 harnais_principal_r2.py [--graine G] [--fuzz N]
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
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64  # noqa: E402
from unicorn import UC_HOOK_CODE  # noqa: E402

# --- Géométrie de l'image d'émulation (RVA = adresses unicorn) --------------------

RVA_R1, SLOT_R1 = 0x1800, 0x480           # http-12:R1 (ancêtre scellé, R7)
RVA_R2, SLOT_R2 = next((r, s) for b, _, r, s, _, _ in L.BLOCS_TLS + L.BLOCS_REVISIONS
                       if b == "g70011")   # 0x7DC0 x 0x200 (layout.py, source unique)
BASE_MEM, TAILLE_MEM = 0x1000, 0xA000     # image + trappes (0x8100+) + marge
ZONE_PILE, TAILLE_PILE = 0x7F000000, 0x10000
RSP = 0x7F008008                          # ≡ 8 mod 16 (P2, convention chargeur)

# Trappes : cinq blocs appelés directement par l'orchestrateur (aux RVA réels)
TRAPPE_WRITE, TRAPPE_TCP_INIT = 0x1040, 0x4000
TRAPPE_TCP_ACCEPT, TRAPPE_TCP_SPAWN = 0x4100, 0x4300
TRAPPE_TCP_JOURNAL = 0x4B00
TRAPPES = (TRAPPE_WRITE, TRAPPE_TCP_INIT, TRAPPE_TCP_ACCEPT,
           TRAPPE_TCP_SPAWN, TRAPPE_TCP_JOURNAL)
# Trappes IAT (adresses factices posées dans les slots .rdata)
SHIM_GSH, SHIM_EP, SHIM_ICS = 0x8100, 0x8110, 0x8120
SHIM_CH, SHIM_WSAC = 0x8130, 0x8140

CONSOLE = 0x5D80                          # http-11 (thread console)
SESSION_R1, SESSION_R2 = 0x5580, 0x74C0   # http-10:R1 (scellé) / http-10:R2 (D92)

# Fixtures .rdata héritées (R7 — contenu du harnais, longueurs scellées)
MSG_BANNIERE = b"TRIADE M3 : proxy demarre (port 25000)\r\n"   # 40 o
MSG_ERREUR = b"erreur reseau, arret\r\n"                        # 22 o
MSG_ARRET = b"arret\r\n"                                        # 7 o
MSG_KO = b"TRIADE M3 : integrite KO, arret\r\n"                 # 33 o
R_BANNIERE, R_ARRET, R_ERREUR, R_KO = 0x2840, 0x28C0, 0x28F0, 0x2910
R_STDOUT, R_STDIN, R_LISTEN, R_QUIT, R_CS = 0x3800, 0x3808, 0x3810, 0x3818, 0x3830

# Table R10 : 26 entrées squelette (géométrie réelle des slots) — génération R1 ;
# génération R2 : + libc-07 @0x2800 + LA PORTE .text3 @0x2810 (l'ancien
# terminateur remplacé — D95 : la table est PLEINE, marche aux bornes).
TABLE_SQUELETTE = [
    (0x1040, 0x40), (0x1080, 0x40),                       # io (hello-02/03)
    (0x1100, 0x80), (0x1180, 0x80), (0x1200, 0x80),       # libc
    (0x1280, 0x80), (0x1300, 0x80), (0x1380, 0x80),
    (0x1800, SLOT_R1),                                    # http-12:R1 (lui-même)
    (0x4000, 0x100), (0x4100, 0x40), (0x4140, 0x40),      # tcp
    (0x4180, 0x40), (0x41C0, 0x40), (0x4300, 0x100),
    (0x4400, 0x200), (0x4B00, 0x100),
    (0x4C00, 0x80), (0x4C80, 0x200), (0x4E80, 0xC0),      # http
    (0x4F40, 0x140), (0x5080, 0xC0), (0x5140, 0xC0),
    (0x5200, 0x180), (0x5380, 0x140), (0x54C0, 0xC0),
]
ENTREE_LIBC07 = (0x13C0, 0x80)             # @0x2800 (D94)
ENTREE_TEXT3 = (L.R10_TEXT3_RVA, L.R10_TEXT3_TAILLE)  # @0x2810 (D95) : (0x6000, 0x2000)

VERSION_R1, VERSION_R2 = 0x00040000, 0x00050002

REUSSITES, ECHECS = [], []


def controle(nom: str, ok: bool, detail: str = "") -> None:
    if ok:
        REUSSITES.append(nom)
        print(f"  [PASS] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append(nom)
        print(f"  [FAIL] {nom}" + (f" — {detail}" if detail else ""))


def somme_qwords(image: bytearray, rva: int, taille: int) -> int:
    n = taille // 8
    return sum(struct.unpack_from(f"<{n}Q", image, rva)) & 0xFFFFFFFFFFFFFFFF


# --- V1 : assemblage des notations -------------------------------------------------

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


def octets_notation(ks: Ks, chemin: str, rva: int, mutation: tuple | None = None):
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
        blob = assembler_lignes(ks, lignes, rva)
        return blob, len(blob)
    blob = assembler_lignes(ks, lignes, rva)
    return blob, declare


# --- Scénarios ----------------------------------------------------------------------

class Scenario:
    """Script d'exécution : retours des trappes, drapeau quit, mutations
    POSTÉRIEURES au scellement de la table (corruption simulée). r2_seul :
    le scénario cible l'entrée #28 — elle n'existe pas dans la table M3 de
    l'ancêtre (pas de différentiel R1 possible, la porte est génération 2)."""

    def __init__(self, tcp01=0x1001, console=0x7000, accepts=(-1,), sessions=None,
                 quit=1, version=None, image_mut=(), table_mut=(), r2_seul=False):
        self.tcp01, self.console, self.accepts = tcp01, console, list(accepts)
        self.sessions = list(sessions) if sessions is not None else \
            [0x7001 + i for i in range(max(0, len(self.accepts)))]
        self.quit, self.version = quit, version
        self.image_mut, self.table_mut = list(image_mut), list(table_mut)
        self.r2_seul = r2_seul


def scenario(nom, **kw) -> tuple[str, Scenario]:
    return nom, Scenario(**kw)


# --- Image d'émulation + table (l'artefact PARTAGÉ modèle/émulation) ---------------

def construire_artefact(gen: int, sc: Scenario, blob_r1: bytes, blob_r2: bytes):
    """-> (image, table, version) — l'image fait 0xB000 (RVA = index) ;
    la table est scellée sur l'image PUIS les mutations s'appliquent. Le
    remplissage est DÉTERMINISTE POSITION-DÉPENDANT (un remplissage uniforme
    rendait possibles des collisions de somme entre plages — le contenu réel
    des blocs du binaire vit des vies distinctes, l'image d'émulation aussi)."""
    image = bytearray(random.Random(0xC0FFEE).randbytes(BASE_MEM + TAILLE_MEM))
    image[RVA_R1:RVA_R1 + len(blob_r1)] = blob_r1          # ancêtre (R7 : présent)
    image[RVA_R1 + len(blob_r1):RVA_R1 + SLOT_R1] = b"\x90" * (SLOT_R1 - len(blob_r1))
    image[RVA_R2:RVA_R2 + len(blob_r2)] = blob_r2          # la révision
    image[RVA_R2 + len(blob_r2):RVA_R2 + SLOT_R2] = b"\x90" * (SLOT_R2 - len(blob_r2))
    for t in TRAPPES:
        image[t] = 0xC3                                    # ret — la sémantique vit dans le crochet
    image[R_BANNIERE:R_BANNIERE + len(MSG_BANNIERE)] = MSG_BANNIERE
    image[R_ARRET:R_ARRET + len(MSG_ARRET)] = MSG_ARRET
    image[R_ERREUR:R_ERREUR + len(MSG_ERREUR)] = MSG_ERREUR
    image[R_KO:R_KO + len(MSG_KO)] = MSG_KO
    image[R_STDOUT:R_CS + 0x40] = b"\x00" * (R_CS + 0x40 - R_STDOUT)  # P3 : état image
    struct.pack_into("<Q", image, R_QUIT, 1 if sc.quit else 0)
    # IAT fausse (les slots pointent sur les trappes IAT)
    for slot, shim in ((L.IAT_SLOTS["GetStdHandle"], SHIM_GSH),
                       (L.IAT_SLOTS["ExitProcess"], SHIM_EP),
                       (L.IAT_SLOTS["InitializeCriticalSection"], SHIM_ICS),
                       (L.IAT_SLOTS["CloseHandle"], SHIM_CH),
                       (L.IAT_SLOTS["WSACleanup"], SHIM_WSAC)):
        struct.pack_into("<Q", image, slot, shim)
    for s in (SHIM_GSH, SHIM_EP, SHIM_ICS, SHIM_CH, SHIM_WSAC):
        image[s] = 0xC3
    # table R10 : scellée sur l'image COURANTE (sommes réelles) PUIS écrite
    # en .rdata @R_TAB_SUM — la marche lira CES octets (jamais deux sources)
    entrees = [(r, t, somme_qwords(image, r, t)) for r, t in TABLE_SQUELETTE]
    if gen == 2:
        entrees.append((ENTREE_LIBC07[0], ENTREE_LIBC07[1],
                        somme_qwords(image, *ENTREE_LIBC07)))
        entrees.append((ENTREE_TEXT3[0], ENTREE_TEXT3[1],
                        somme_qwords(image, *ENTREE_TEXT3)))
        table = list(entrees)                              # PLEINE — pas de terminateur
    else:
        table = entrees + [(0, 0, 0)]                      # terminateur scellé M3
    for k, (r, t, s) in enumerate(table):
        struct.pack_into("<IIQ", image, L.R_TAB_SUM + 16 * k, r, t, s)
    version = sc.version if sc.version is not None else \
        (VERSION_R2 if gen == 2 else VERSION_R1)
    struct.pack_into("<Q", image, L.R_VERSION, version)
    # mutations POSTÉRIEURES au scellement (corruption, pas reconstruction) —
    # dans l'IMAGE (les octets que la marche lira) ET dans la liste (le modèle)
    for idx, champ, val in sc.table_mut:
        r, t, s = table[idx]
        table[idx] = (r, t, val) if champ == "somme" else \
            ((val, t, s) if champ == "rva" else (r, val, s))
        struct.pack_into("<IIQ", image, L.R_TAB_SUM + 16 * idx, *table[idx])
    for rva, val in sc.image_mut:
        if image[rva] == val & 0xFF:    # une NON-mutation n'est pas une mutation :
            val = (val ^ 0x5A) & 0xFF   # le fuzz exige un octet retourné EFFECTIVEMENT
        image[rva] = val & 0xFF
    return image, table, version


# --- Modèle (écrit depuis la SPÉCIFICATION — jamais la notation) -------------------

def porte_modele(image: bytearray, table: list, version: int, gen: int) -> bool:
    """Q1 — la porte, par génération. gen 2 : marche aux BORNES, table PLEINE,
    fail-closed (rva nul / taille nulle = KO). gen 1 : terminateur scellé."""
    if gen == 2:
        if len(table) != L.R10_NB_ENTREES:
            return False
        for r, t, s in table:
            if r == 0 or t == 0 or somme_qwords(image, r, t) != s:
                return False
    else:
        for r, t, s in table:
            if r == 0:                                     # terminateur : fin de marche
                break
            if t == 0:                                     # entrée sautée (sémantique scellée)
                continue
            if somme_qwords(image, r, t) != s:
                return False
    return version >= 0x00040000                           # plancher M3 (monotonie)


def modele_trace(gen: int, sc: Scenario, image, table, version) -> list[tuple]:
    porte_ok = porte_modele(image, table, version, gen)
    if not porte_ok:                                       # E1 — avant tout effet réseau
        return [("GSH", -11), ("write", MSG_KO), ("exit", 1)]
    cible = SESSION_R2 if gen == 2 else SESSION_R1
    tr = [("GSH", -11), ("GSH", -10), ("InitCS",), ("journal", MSG_BANNIERE)]
    tr.append(("tcp01", sc.tcp01))                        # l'appel A eu lieu (retour 0)
    if sc.tcp01 == 0:                                      # E2 : écoute
        return tr + [("journal", MSG_ERREUR), ("exit", 2)]
    tr.append(("spawn", CONSOLE, 0, sc.console))
    if sc.console == 0:                                    # E2 : console
        return tr + [("journal", MSG_ERREUR), ("exit", 2)]
    tr.append(("CH", sc.console))
    i_acc, i_sess = 0, 0
    while True:
        if i_acc >= len(sc.accepts):
            raise RuntimeError("scénario inachevé : accepts épuisé sans échec final")
        a = sc.accepts[i_acc]
        i_acc += 1
        tr.append(("accept", sc.tcp01, a))
        if a < 0:                                          # échec signé (tcp-02)
            if sc.quit != 0:                               # Q3 : arrêt demandé
                return tr + [("journal", MSG_ARRET), ("WSACLEANUP",), ("exit", 0)]
            return tr + [("journal", MSG_ERREUR), ("exit", 2)]   # E3
        h = sc.sessions[i_sess] if i_sess < len(sc.sessions) else 0
        i_sess += 1
        tr.append(("spawn", cible, a, h))
        if h == 0:                                         # E2 : lancement de session
            return tr + [("journal", MSG_ERREUR), ("exit", 2)]
        tr.append(("CH", h))


# --- Émulation (unicorn, octets réels + trappes crochetées) ------------------------

def _regs():
    from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX,
                                   UC_X86_REG_RDX, UC_X86_REG_RSI, UC_X86_REG_RDI,
                                   UC_X86_REG_RBP, UC_X86_REG_RSP, UC_X86_REG_R8,
                                   UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11,
                                   UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14,
                                   UC_X86_REG_R15, UC_X86_REG_RIP)
    return {"rax": UC_X86_REG_RAX, "rbx": UC_X86_REG_RBX, "rcx": UC_X86_REG_RCX,
            "rdx": UC_X86_REG_RDX, "rsi": UC_X86_REG_RSI, "rdi": UC_X86_REG_RDI,
            "rbp": UC_X86_REG_RBP, "rsp": UC_X86_REG_RSP, "r8": UC_X86_REG_R8,
            "r9": UC_X86_REG_R9, "r10": UC_X86_REG_R10, "r11": UC_X86_REG_R11,
            "r12": UC_X86_REG_R12, "r13": UC_X86_REG_R13, "r14": UC_X86_REG_R14,
            "r15": UC_X86_REG_R15, "rip": UC_X86_REG_RIP}


_REGS = _regs()
SENTINELLES_NV = {
    "rbx": 0x1212121212121212, "rbp": 0x2323232323232323,
    "rdi": 0x3434343434343434, "rsi": 0x4545454545454545,
    "r12": 0x5656565656565656, "r13": 0x6767676767676767,
    "r14": 0x7878787878787878, "r15": 0x8989898989898989,
}


class Emulateur:
    def __init__(self, image: bytearray, sc: Scenario):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.uc.mem_map(BASE_MEM, TAILLE_MEM)
        self.uc.mem_map(ZONE_PILE, TAILLE_PILE)
        self.uc.mem_write(BASE_MEM, bytes(image[BASE_MEM:]))
        self.sc = sc
        self.trace: list[tuple] = []
        self.i_acc, self.i_sess = 0, 0
        self.arret = False
        for adresse in (SHIM_GSH, SHIM_EP, SHIM_ICS, SHIM_CH, SHIM_WSAC,
                        TRAPPE_WRITE, TRAPPE_TCP_INIT, TRAPPE_TCP_ACCEPT,
                        TRAPPE_TCP_SPAWN, TRAPPE_TCP_JOURNAL):
            self.uc.hook_add(UC_HOOK_CODE, self._crochet, begin=adresse, end=adresse)

    # -- la sémantique des trappes (le modèle d'exécution du harnais) ---------------
    def _crochet(self, uc, adresse, taille_instruction, user_data):
        r = lambda n: uc.reg_read(_REGS[n])
        w = lambda n, v: uc.reg_write(_REGS[n], v)
        if adresse == SHIM_GSH:
            arg = r("rcx") & 0xFFFFFFFF          # mov ecx, -11 : zero-étendu en 64
            if arg & 0x80000000:
                arg -= 1 << 32
            self.trace.append(("GSH", arg))
            w("rax", 0xF00D0011 if arg == -11 else 0xF00D0010)
        elif adresse == SHIM_ICS:
            self.trace.append(("InitCS",))
        elif adresse == SHIM_EP:
            self.trace.append(("exit", r("rcx") & 0xFFFFFFFF))
            self.arret = True
            uc.emu_stop()
        elif adresse == SHIM_CH:
            self.trace.append(("CH", r("rcx")))
            w("rax", 1)
        elif adresse == SHIM_WSAC:
            self.trace.append(("WSACLEANUP",))
            w("rax", 0)
        elif adresse == TRAPPE_TCP_INIT:
            w("rax", self.sc.tcp01 & 0xFFFFFFFFFFFFFFFF)
            self.trace.append(("tcp01", self.sc.tcp01))
        elif adresse == TRAPPE_TCP_ACCEPT:
            if self.i_acc >= len(self.sc.accepts):
                raise RuntimeError("accepts épuisé — scénario inachevé")
            a = self.sc.accepts[self.i_acc]
            self.i_acc += 1
            w("rax", a & 0xFFFFFFFFFFFFFFFF)
            self.trace.append(("accept", r("rcx"), a))
        elif adresse == TRAPPE_TCP_SPAWN:
            fn, arg = r("rcx"), r("rdx")
            if fn == CONSOLE:
                h = self.sc.console
            else:
                h = self.sc.sessions[self.i_sess] if self.i_sess < len(self.sc.sessions) else 0
                self.i_sess += 1
            w("rax", h & 0xFFFFFFFFFFFFFFFF)
            self.trace.append(("spawn", fn, arg, h))
        elif adresse == TRAPPE_TCP_JOURNAL:
            n = r("rdx")
            self.trace.append(("journal", bytes(uc.mem_read(r("rcx"), n))))
            w("rax", n)
        elif adresse == TRAPPE_WRITE:
            n = r("r8")
            self.trace.append(("write", bytes(uc.mem_read(r("rdx"), n))))
            w("rax", n)

    def executer(self, entree: int) -> tuple[str, list[tuple]]:
        for nom, valeur in SENTINELLES_NV.items():
            self.uc.reg_write(_REGS[nom], valeur)
        self.uc.reg_write(_REGS["rsp"], RSP)
        try:
            self.uc.emu_start(entree, BASE_MEM + TAILLE_MEM - 0x10,
                              timeout=5_000_000, count=1_000_000)
        except Exception as exc:
            return ("CRASH:" + repr(exc)[:48], self.trace)
        if not self.arret:
            return ("SANS_EXIT", self.trace)
        # NOTE : pas de vérification de non-volatils — Q4 : le bloc ne
        # revient JAMAIS (ExitProcess terminal, miroir de l'ancêtre scellé :
        # les poussées du prologue ne sont pas restituées, l'ABI n'a plus
        # d'objet après la mort du processus).
        return ("OK", self.trace)


def executer_generation(gen: int, sc: Scenario, blob_r1: bytes, blob_r2: bytes):
    """-> (statut, trace, modele) — l'artefact est construit UNE fois et lu
    par le modèle ET l'émulation (jamais deux sources de l'image)."""
    image, table, version = construire_artefact(gen, sc, blob_r1, blob_r2)
    attendu = modele_trace(gen, sc, image, table, version)
    emu = Emulateur(image, sc)
    statut, trace = emu.executer(RVA_R2 if gen == 2 else RVA_R1)
    return statut, trace, attendu


def normaliser(trace: list[tuple], gen: int) -> list[tuple]:
    """La cible du spawn session EST la divergence légitime du câblage —
    pour la comparaison croisée R1/R2, elle est ramenée à l'ancêtre."""
    if gen != 2:
        return trace
    return [(("spawn", SESSION_R1) + t[2:]) if (t and t[0] == "spawn" and t[1] == SESSION_R2)
            else t for t in trace]


# --- V2 : différentiel d'ancêtre ----------------------------------------------------

def cas_v2() -> list[tuple[str, Scenario]]:
    s = scenario
    return [
        s("nominal : 3 accepts puis arrêt demandé",
          accepts=(0x3001, 0x3002, 0x3003, -1), quit=1),
        s("zéro accept : arrêt immédiat demandé", accepts=(-1,), quit=1),
        s("E3 : échec d'acceptation SANS arrêt demandé (fail-closed dispo)",
          accepts=(-1,), quit=0),
        s("E2 : échec d'écoute", tcp01=0, accepts=(-1,), quit=1),
        s("E2 : échec du thread console", console=0, accepts=(-1,), quit=1),
        s("E2 : échec du lancement de session", accepts=(0x3001,),
          sessions=[0], quit=1),
        s("porte : octet squelette corrompu (libc @0x1100)",
          accepts=(-1,), quit=1, image_mut=[(0x1100, 0x33)]),
        s("porte : octet .text3 corrompu (@0x6500 — LA NOUVELLE PORTE)",
          accepts=(-1,), quit=1, image_mut=[(0x6503, 0x55)]),
        s("porte : version sous plancher (0x30000)",
          accepts=(-1,), quit=1, version=0x30000),
        s("porte : entrée #5 de somme corrompue (les DEUX générations)",
          accepts=(-1,), quit=1, table_mut=[(4, "somme", 0xDEADBEEF)]),
        s("porte : entrée .text3 trouée (rva nul — fail-closed D95)",
          accepts=(-1,), quit=1, table_mut=[(27, "rva", 0)], r2_seul=True),
        s("porte : entrée .text3 de taille nulle (fail-closed D95)",
          accepts=(-1,), quit=1, table_mut=[(27, "taille", 0)], r2_seul=True),
    ]


def differentiel_v2(blob_r1: bytes, blob_r2: bytes) -> int:
    ecarts = 0
    for nom, sc in cas_v2():
        if sc.r2_seul:
            # l'entrée #28 n'existe qu'en génération 2 — pas d'ancêtre à
            # comparer (la porte .text3 est la NOUVELLE couche de R2)
            s2, t2, m2 = executer_generation(2, sc, blob_r1, blob_r2)
            if not (s2 == "OK" and t2 == m2
                    and m2 == [("GSH", -11), ("write", MSG_KO), ("exit", 1)]):
                ecarts += 1
                print(f"    écart [{nom}] : R2 {s2}, trace {t2[:3]}")
            continue
        s1, t1, m1 = executer_generation(1, sc, blob_r1, blob_r2)
        s2, t2, m2 = executer_generation(2, sc, blob_r1, blob_r2)
        ok1, ok2 = s1 == "OK" and t1 == m1, s2 == "OK" and t2 == m2
        # la corruption .text3 : R1 ne la garde pas (sa table est M3) — la
        # divergence est LÉGITIME et nommée : R1 nominal, R2 KO (E1)
        legit = ".text3 corrompu" in nom
        croisee = normaliser(t2, 2) == t1 if not legit else \
            (t1 == m1 and m2 == [("GSH", -11), ("write", MSG_KO), ("exit", 1)]
             and len([e for e in t1 if e[0] in ("tcp01", "accept")]) > 0)
        if not (ok1 and ok2 and croisee):
            ecarts += 1
            print(f"    écart [{nom}] : R1 {s1}/{ok1} R2 {s2}/{ok2} croisée {croisee}")
            if t1 != m1:
                print(f"      R1 trace {t1[:6]} != modèle {m1[:6]}")
            if t2 != m2:
                print(f"      R2 trace {t2[:6]} != modèle {m2[:6]}")
    return ecarts


# --- V3 : fuzz de la porte (modèle contre octets, aucune mutation ne passe) --------

def _plages_gardees() -> list[tuple[int, int]]:
    return (TABLE_SQUELETTE + [ENTREE_LIBC07, ENTREE_TEXT3])


def cas_fuzz_porte(alea: random.Random, n: int) -> list[tuple[str, Scenario]]:
    """Une mutation D'UN point (champ d'entrée OU octet gardé) par cas ; les
    octets mutés évitent le code de R2 (0x7DC0-0x7FC0) et les cinq trappes —
    la corruption du VÉRIFICATEUR n'est pas décidable par lui-même."""
    cas = []
    plages = _plages_gardees()
    exclus = set(TRAPPES) | set(range(RVA_R2, RVA_R2 + SLOT_R2))
    for i in range(n):
        sc = Scenario(accepts=(-1,), quit=1)
        if alea.random() < 0.5:                             # champ d'entrée
            idx = alea.randrange(L.R10_NB_ENTREES)
            champ = alea.choice(("rva", "taille", "somme"))
            original = (TABLE_SQUELETTE + [ENTREE_LIBC07, ENTREE_TEXT3])[idx]
            if champ == "rva":
                val = alea.choice((0, alea.randrange(0x1000, 0x9000)))
                while val == original[0]:                  # jamais de mutation sans effet
                    val = alea.randrange(0x1000, 0x9000)
            elif champ == "taille":
                val = alea.choice((0, alea.randrange(1, 0x2001)))
                while val == original[1]:                  # idem — une NON-mutation
                    val = alea.randrange(1, 0x2001) if val else 0
            else:
                val = alea.randrange(1 << 64)
            sc.table_mut = [(idx, champ, val)]
            cas.append((f"fuzz-porte champ {champ} entrée #{idx}", sc))
        else:                                               # octet dans une plage gardée
            while True:
                r, t = plages[alea.randrange(len(plages))]
                rva = r + alea.randrange(t)
                if rva not in exclus:                       # (le code de l'ancêtre R1 @0x1800
                    break                                   #  est MORT en génération 2 : sa
            sc.image_mut = [(rva, alea.randrange(256))]    #  plage est gardable — mutation licite)
            cas.append((f"fuzz-porte octet @{rva:#x}", sc))
    return cas


def fuzz_porte(blob_r1: bytes, blob_r2: bytes, alea: random.Random, n: int) -> int:
    ecarts = 0
    silencieux = 0
    for nom, sc in cas_fuzz_porte(alea, n):
        image, table, version = construire_artefact(2, sc, blob_r1, blob_r2)
        attendu = modele_trace(2, sc, image, table, version)
        emu = Emulateur(image, sc)
        statut, trace = emu.executer(RVA_R2)
        if statut != "OK" or trace != attendu:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart fuzz [{nom}] : {statut}, trace {trace[:3]}")
        if attendu != [("GSH", -11), ("write", MSG_KO), ("exit", 1)]:
            silencieux += 1                                 # mutation passée SANS KO
    return ecarts, silencieux


# --- V4 : falsification (mutations stables en taille, leçon D82) -------------------

def falsifier(ks: Ks, chemin_r2: str, blob_r1: bytes, alea: random.Random) -> int:
    mutations = [
        ("lea rcx, [rip - 0xa1e]", "lea rcx, [rip - 0x295e]",
         "LE CONTRE-CÂBLAGE : la boucle lance http-10:R1 (0x5580) — I1 nominal",
         scenario("exposition", accepts=(0x3001, 0x3002, -1), quit=1)),
        ("lea r15, [rip - 0x55cc]", "lea r15, [rip - 0x55bc]",
         "la borne remonte à 0x2830 : la VERSION est lue comme une entrée "
         "(taille nulle) — la table saine échoue",
         scenario("exposition", accepts=(-1,), quit=1)),
        ("lea r15, [rip - 0x55cc]", "lea r15, [rip - 0x55dc]",
         "la borne descend à 0x2810 : l'entrée .text3 est SAUTÉE — la porte "
         "ne garde plus la couche M4",
         scenario("exposition", accepts=(-1,), quit=1,
                  image_mut=[(0x6503, 0x55)])),
        ("cmp rax, 0x40000", "cmp rax, 0x30000",
         "le plancher anti-rollback abaissé — la version 0x30000 passe",
         scenario("exposition", accepts=(-1,), quit=1, version=0x30000)),
        ("mov ecx, 2", "mov ecx, 3",
         "E3 : le code de sortie structurel dévié (2 -> 3)",
         scenario("exposition", accepts=(-1,), quit=0)),
        ("jne 0x7f2e", "je 0x7f2e",
         "le sens du test d'arrêt inversé : l'échec SANS arrêt prend le "
         "chemin propre (exit 0)",
         scenario("exposition", accepts=(-1,), quit=0)),
    ]
    non_attrapees = 0
    exposes = []
    for avant, apres, desc, (nom_sc, sc) in mutations:
        blob_m, _ = octets_notation(ks, chemin_r2, RVA_R2, mutation=(avant, apres))
        s_m, t_m, m_m = executer_generation(2, sc, blob_r1, blob_m)
        attrapee = not (s_m == "OK" and t_m == m_m)
        controle(f"V4 {desc} : ATTRAPÉE", attrapee,
                 f"{s_m}, trace {t_m[:4]}")
        if not attrapee:
            non_attrapees += 1
        exposes.append(sc)
    # témoin : la notation INTACTE reste verte sur les MÊMES scénarios
    blob_t, _ = octets_notation(ks, chemin_r2, RVA_R2)
    temoin_ok = True
    for sc in exposes:
        s_t, t_t, m_t = executer_generation(2, sc, blob_r1, blob_t)
        if not (s_t == "OK" and t_t == m_t):
            temoin_ok = False
    controle("V4 témoin (notation intacte, 6 scénarios d'exposition) : VERT",
             temoin_ok)
    return non_attrapees


# --- Main ---------------------------------------------------------------------------

def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261028)
    parseur.add_argument("--fuzz", type=int, default=400)
    args = parseur.parse_args()
    alea = random.Random(args.graine)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    chemin_r2 = os.path.join(ICI, "notation", "http-12-principal-r2.asm")
    chemin_r1 = os.path.join(ICI, "..", "m3", "notation", "http-12-principal.asm")

    print("=== harnais_principal_r2.py — révision http-12:R2 (LE CÂBLAGE, D95), "
          f"graine {args.graine} ===")

    print("\n--- V1 : round-trip de notation ---")
    blob_r2, declare_r2 = octets_notation(ks, chemin_r2, RVA_R2)
    controle(f"V1 http-12:R2 : assemblage intégral ({len(blob_r2)} o == "
             f"« Code : {declare_r2} o » déclarés)", len(blob_r2) == declare_r2)
    passe2 = assembler_lignes(ks, lignes_notation(chemin_r2), RVA_R2)
    controle("V1 http-12:R2 : idempotence (2e passe octet-identique)",
             passe2 == blob_r2)
    blob_r1, declare_r1 = octets_notation(ks, chemin_r1, RVA_R1)
    controle(f"V1 http-12:R1 (ancêtre scellé) : assemblage à 0x{RVA_R1:x} "
             f"({len(blob_r1)} o == « Code : {declare_r1} o » déclarés)",
             len(blob_r1) == declare_r1)

    print("\n--- V2 : différentiel d'ancêtre (12 scénarios, R1 émulé contre "
          "R2 émulé — traces identiques sauf LE CÂBLAGE) ---")
    e_v2 = differentiel_v2(blob_r1, blob_r2)
    controle("V2 12 scénarios : R1 == modèle R1 ET R2 == modèle R2 ET traces "
             "croisées identiques (spawn 0x5580 -> 0x74C0 SEUL écart ; "
             "divergence légitime .text3 nommée), ordre Q2 constaté, porte "
             "avant tout effet (I3)", e_v2 == 0, f"{e_v2} écarts")

    print(f"\n--- V3 : fuzz de la porte R10 ({args.fuzz} mutations d'un point, "
          "modèle contre octets) ---")
    e_v3, silencieux = fuzz_porte(blob_r1, blob_r2, alea, args.fuzz)
    controle(f"V3 {args.fuzz} mutations : le modèle et les octets nomment le "
             f"MÊME verdict, ZÉRO passage silencieux", e_v3 == 0 and silencieux == 0,
             f"{e_v3} écarts, {silencieux} silencieux")

    print("\n--- V4 : falsification (une suite qui ne peut pas échouer "
          "ne prouve rien) ---")
    non_attrapees = falsifier(ks, chemin_r2, blob_r1, alea)

    print("\n" + "=" * 78)
    print(f"BILAN : {len(REUSSITES)} PASS, {len(ECHECS)} ÉCHEC "
          f"(graine {args.graine}, {args.fuzz} mutations de porte)")
    for nom in ECHECS:
        print(f"  FAIL {nom}")
    if not ECHECS:
        print("La révision http-12:R2 tient son contrat : notation round-trip 100 %,")
        print("l'héritage R1 est reproduit trace à trace (l'unique différence : la")
        print("cible du spawn session 0x74C0), la porte R10 marche aux bornes sur 28")
        print("entrées — fail-closed sur entrée trouée, la couche .text3 entière")
        print("gardée au lancement — et la suite est falsifiable (6/6 attrapées).")
    print("=" * 78)
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main())
