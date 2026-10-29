#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_feuilles.py — Harnais à propriétés des feuilles pures M4 (D79).

Vecteurs des spécifications tls-01/tls-02/tls-03 (m4/I, écrites-avant-code) :
  V1  round-trip de notation 100 % — chaque ligne de la notation explicite
      rassemblée à son adresse documentée reproduit exactement les octets
      que l'auteur a mesurés (taille totale == en-tête « Code : N o ») ;
  V2  propriété différentielle — la notation ÉMULÉE (unicorn) contre un
      modèle de référence écrit depuis la SPÉCIFICATION (jamais depuis la
      notation) : verdict, contenus, longueurs — couvre P*, Q*, I* ;
  V3  propriétés d'hygiène — canaris mémoire autour des zones d'écriture
      (rien n'est écrit hors destination/cadre, y compris sur les refus),
      registres non volatils sentinelles inchangés, terminaison bornée ;
  V4  falsification — des mutations D'UN SEUL point de la notation (borne
      relâchée, constante de classe confondue, verdict dévié, compte
      erroné) doivent être ATTRAPÉES par le différentiel ; le témoin
      sauvage (notation intacte) doit rester vert — une suite qui ne peut
      pas échouer ne prouve rien.

Le harnais émule les octets de la NOTATION (ce que build_m4.py embarquera),
pas le brouillon : c'est la chaîne complète notation → image qui est testée.
Usage : python3 harnais_feuilles.py [--graine G] [--cas N]
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

# --- Mémoire du harnais (hors image PE : émulation nue des feuilles) -------------

ZONE_CODE = 0x6000            # les trois feuilles à leurs RVA .text3
TAILLE_CODE = 0x1000
RET_MAGIQUE = 0x6F00          # adresse d'arrêt propre (dans la page code, int3)
ZONE_SRC = 0x10000            # hôte / tampon utile de l'appelant
TAILLE_SRC = 0x1000
ZONE_DST = 0x20000            # destination / cadre
TAILLE_DST = 0x1000
ZONE_TAILLES = 0x30000        # structure tailles de flux (type 1)
TAILLE_TAILLES = 0x1000       # multiple de 0x1000 (exigence mem_map unicorn)
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP = 0x7F008000

CANARI = b"\xA5"

RVA_TLS01, RVA_TLS02, RVA_TLS03 = 0x6000, 0x6080, 0x6180
SLOT_TLS01, SLOT_TLS02, SLOT_TLS03 = 0x80, 0x100, 0x140

REUSSITES, ECHECS = [], []


def controle(nom: str, ok: bool, detail: str = "") -> None:
    if ok:
        REUSSITES.append(nom)
        print(f"  [PASS] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append(nom)
        print(f"  [FAIL] {nom}" + (f" — {detail}" if detail else ""))


# --- V1 : round-trip de notation ---------------------------------------------------

def lignes_notation(chemin: str) -> list[str]:
    lignes = []
    with open(chemin, encoding="utf-8") as f:
        for brut in f:
            ligne = brut.split(";")[0].strip()
            if ligne:
                lignes.append(ligne)
    return lignes


def assembler_lignes(ks: Ks, lignes: list[str], rva: int) -> bytes:
    """Assemble chaque ligne à son adresse courante — les cibles absolues des
    sauts reproduisent les choix rel8/rel32 de l'auteur (round-trip R5)."""
    sortie, adresse = [], rva
    for ligne in lignes:
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise RuntimeError(f"ligne inassemblable à 0x{adresse:x} : {ligne!r}")
        sortie.append(bytes(enc))
        adresse += len(enc)
    return b"".join(sortie)


def octets_notation(ks: Ks, bloc: str, rva: int, mutation: str | None = None) -> bytes:
    """Octets de la notation (mutée si demandé — V4) + taille de code déclarée."""
    chemin = os.path.join(ICI, "notation", bloc + ".asm")
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
        return blob, len(blob)          # taille déclarée sans objet pour une mutée
    blob = assembler_lignes(ks, lignes, rva)
    return blob, declare


# --- Modèles de référence (écrits depuis les SPÉCIFICATIONS — jamais la notation) --

def modele_tls01(hote: bytes):
    """tls-01:R1 — Q1 succès (0, contenu, 2*(n+1)) ; Q2 longueur (1) ; Q3 encodage (2)."""
    n = len(hote)
    if n == 0 or n > L.HOTE_MAX:
        return 1, b"", None
    if any(octet >= 0x80 for octet in hote):
        return 2, b"", None
    contenu = b"".join(bytes((o, 0)) for o in hote) + b"\x00\x00"
    return 0, contenu, 2 * (n + 1)


def modele_tls02(hresult: int):
    """tls-02:R1 — domaine = sign-étendu de 32 bits ; table TOTALE (liste blanche)."""
    if hresult != _signe32(hresult & 0xFFFFFFFF):
        return 6
    return L.HRESULTS.get(hresult & 0xFFFFFFFF, L.VERDICT_FATAL)


def _signe32(v: int) -> int:
    return v - 0x100000000 if v & 0x80000000 else v


def modele_tls03(type_desc: int, ptr: int, longueur: int, tailles: bytes):
    """tls-03:R1 — Q3 type ; Q2 bornes (type 0 : MAX_JETON, type 1 : négocié) ;
    Q1 descripteur complet. Mise en page sspi.h x64, convention cadre contigu
    (en-tête AVANT le clair, queue APRÈS — consommateur tls-06, m4/I/tls-06)."""
    if type_desc not in (0, 1, 2):
        return 2, b""
    if type_desc == 0:
        if longueur > L.MAX_JETON:
            return 1, b""
        return 0, (struct.pack("<IIQ", 0, 1, ZONE_DST + 0x10)
                   + struct.pack("<IIQ", longueur & 0xFFFFFFFF, L.SECBUFFER_TOKEN, ptr))
    if type_desc == 1:
        cb_max, cb_tete, cb_queue = (
            struct.unpack_from("<I", tailles, 8)[0],
            struct.unpack_from("<I", tailles, 0)[0],
            struct.unpack_from("<I", tailles, 4)[0])
        if longueur > cb_max:
            return 1, b""
        return 0, (struct.pack("<IIQ", 0, 3, ZONE_DST + 0x10)
                   + struct.pack("<IIQ", cb_tete, L.SECBUFFER_STREAM_HEADER, ptr - cb_tete)
                   + struct.pack("<IIQ", longueur & 0xFFFFFFFF, L.SECBUFFER_DATA, ptr)
                   + struct.pack("<IIQ", cb_queue, L.SECBUFFER_STREAM_TRAILER, ptr + longueur))
    return 0, (struct.pack("<IIQ", 0, 4, ZONE_DST + 0x10)
               + struct.pack("<IIQ", longueur & 0xFFFFFFFF, L.SECBUFFER_DATA, ptr)
               + struct.pack("<IIQ", 0, L.SECBUFFER_EMPTY, 0) * 3)


# --- Émulation (unicorn) -----------------------------------------------------------

SENTINELLES_NV = {  # registres non volatils préchargés — I3/I4 (tls-01/02/03)
    "rbx": 0x1212121212121212, "rbp": 0x2323232323232323,
    "rdi": 0x3434343434343434, "rsi": 0x4545454545454545,
    "r12": 0x5656565656565656, "r13": 0x6767676767676767,
    "r14": 0x7878787878787878, "r15": 0x89898989898989,
}


class Emulateur:
    def __init__(self):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.uc.mem_map(ZONE_CODE, TAILLE_CODE)
        self.uc.mem_map(ZONE_SRC, TAILLE_SRC)
        self.uc.mem_map(ZONE_DST, TAILLE_DST)
        self.uc.mem_map(ZONE_TAILLES, TAILLE_TAILLES)
        self.uc.mem_map(ZONE_PILE, TAILLE_PILE)
        self.canari_dst = CANARI * TAILLE_DST
        self.canari_src = CANARI * TAILLE_SRC

    def charger(self, blobs: dict[int, bytes]):
        # PIÈGE unicorn (leçon D79) : les blocs traduits sont CACHÉS et
        # mem_write sur du code déjà exécuté n'invalide PAS la traduction —
        # un mutant rechargé ne tournait jamais (code témoin caché). Chaque
        # chargement RECONSTRUIT l'émulateur : les octets testés sont
        # exactement ceux passés en argument.
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.uc.mem_map(ZONE_CODE, TAILLE_CODE)
        self.uc.mem_map(ZONE_SRC, TAILLE_SRC)
        self.uc.mem_map(ZONE_DST, TAILLE_DST)
        self.uc.mem_map(ZONE_TAILLES, TAILLE_TAILLES)
        self.uc.mem_map(ZONE_PILE, TAILLE_PILE)
        page = b"\xCC" * TAILLE_CODE
        for rva, blob in blobs.items():
            page = page[:rva - ZONE_CODE] + blob + page[rva - ZONE_CODE + len(blob):]
        self.page_code = page
        self.uc.mem_write(ZONE_CODE, page)

    def _preparer(self):
        # DST seul est réinitialisé (zone d'écriture surveillée par canaris) —
        # SRC et TAILLES sont les ENTRÉES du cas, écrites par le différentiel
        # AVANT l'appel : les réécrire ici effacerait le hôte et les tailles.
        self.uc.mem_write(ZONE_DST, self.canari_dst)
        for nom, valeur in SENTINELLES_NV.items():
            self.uc.reg_write(_REGS[nom], valeur)
        self.uc.reg_write(_REGS["rsp"], RSP)
        self.uc.mem_write(RSP, struct.pack("<Q", RET_MAGIQUE))

    def executer(self, rva: int, rcx: int, rdx: int, r8: int, r9: int,
                 cinquieme: int | None = None) -> tuple[int, int, int]:
        """Exécute la feuille ; retourne (rip_final, rax, rdx). Lève si crash."""
        self._preparer()
        if cinquieme is not None:      # 5e argument msx64 : [rsp+0x28]
            self.uc.mem_write(RSP + 0x28, struct.pack("<Q", cinquieme))
        self.uc.reg_write(_REGS["rcx"], rcx)
        self.uc.reg_write(_REGS["rdx"], rdx)
        self.uc.reg_write(_REGS["r8"], r8)
        self.uc.reg_write(_REGS["r9"], r9)
        self.uc.emu_start(rva, RET_MAGIQUE, timeout=2_000_000, count=100_000)
        return (self.uc.reg_read(_REGS["rip"]), self.uc.reg_read(_REGS["rax"]),
                self.uc.reg_read(_REGS["rdx"]))

    def lecture_dst(self, n: int) -> bytes:
        return bytes(self.uc.mem_read(ZONE_DST, n))

    def non_volatils_intacts(self) -> bool:
        for nom, valeur in SENTINELLES_NV.items():
            if self.uc.reg_read(_REGS[nom]) != valeur:
                return False
        return True

    def hors_canaris(self, zones_attendues: list[tuple[int, int]]) -> bool:
        """True ssi chaque octet de DST est soit canari intact, soit dans une
        zone couverte par une écriture attendue (I2 : rien d'autre ne bouge)."""
        dst = self.lecture_dst(TAILLE_DST)
        couvert = bytearray(TAILLE_DST)
        for debut, taille in zones_attendues:
            for i in range(debut, min(debut + taille, TAILLE_DST)):
                couvert[i] = 1
        return all(dst[i] == 0xA5 or couvert[i] for i in range(TAILLE_DST))

    def src_intact(self, original: bytes) -> bool:
        return bytes(self.uc.mem_read(ZONE_SRC, len(original))) == original


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


# --- V2/V3 : différentiel + hygiène ------------------------------------------------

def differentiel_tls01(emu: Emulateur, blob: bytes, cas: list[bytes], etiquette: str) -> int:
    emu.charger({RVA_TLS01: blob})
    ecarts = 0
    for hote in cas:
        verdict_m, contenu_m, rdx_m = modele_tls01(hote)
        # réinitialisation INTÉGRALE de SRC (résidus des cas précédents)
        emu.uc.mem_write(ZONE_SRC, hote + CANARI * (TAILLE_SRC - len(hote)))
        try:
            rip, rax, rdx = emu.executer(RVA_TLS01, ZONE_SRC, len(hote), ZONE_DST, 0)
        except Exception as exc:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart {etiquette} : crash {exc} (longueur {len(hote)})")
            continue
        ecrit = emu.lecture_dst(len(contenu_m) if verdict_m == 0 else 0)
        zones = [(0, len(contenu_m))] if verdict_m == 0 else []
        ok = (rip == RET_MAGIQUE and rax == verdict_m
              and (verdict_m != 0 or (rdx == rdx_m and ecrit == contenu_m))
              and emu.non_volatils_intacts() and emu.hors_canaris(zones)
              and emu.src_intact(hote + CANARI * (TAILLE_SRC - len(hote))))
        if not ok:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart {etiquette} : longueur {len(hote)} -> "
                      f"rax={rax} (modèle {verdict_m}), rdx={rdx} (modèle {rdx_m})")
    return ecarts


def differentiel_tls02(emu: Emulateur, blob: bytes, cas: list[int], etiquette: str) -> int:
    emu.charger({RVA_TLS02: blob})
    ecarts = 0
    for h in cas:
        verdict_m = modele_tls02(h)
        try:
            rip, rax, rdx = emu.executer(RVA_TLS02, h, 0, 0, 0)
        except Exception as exc:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart {etiquette} : crash {exc} (0x{h & 0xFFFFFFFFFFFFFFFF:x})")
            continue
        if not (rip == RET_MAGIQUE and rax == verdict_m
                and rdx == (h & 0xFFFFFFFFFFFFFFFF)   # registre non signé 64 bits
                and emu.non_volatils_intacts() and emu.hors_canaris([])):
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart {etiquette} : 0x{h & 0xFFFFFFFFFFFFFFFF:x} -> "
                      f"rax={rax} (modèle {verdict_m})")
    return ecarts


def differentiel_tls03(emu: Emulateur, blob: bytes, cas: list[tuple], etiquette: str) -> int:
    emu.charger({RVA_TLS03: blob})
    ecarts = 0
    for type_desc, ptr, longueur, tailles in cas:
        verdict_m, contenu_m = modele_tls03(type_desc, ptr, longueur, tailles)
        utile = CANARI * 64
        emu.uc.mem_write(ptr, utile)
        emu.uc.mem_write(ZONE_TAILLES, tailles)
        try:
            rip, rax, _ = emu.executer(RVA_TLS03, type_desc, ptr, longueur, ZONE_DST,
                                       cinquieme=ZONE_TAILLES)
        except Exception as exc:
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart {etiquette} : crash {exc} (type {type_desc})")
            continue
        ecrit = emu.lecture_dst(len(contenu_m) if verdict_m == 0 else 0)
        zones = [(0, len(contenu_m))] if verdict_m == 0 else []
        if not (rip == RET_MAGIQUE and rax == verdict_m
                and (verdict_m != 0 or ecrit == contenu_m)
                and emu.non_volatils_intacts() and emu.hors_canaris(zones)
                and bytes(emu.uc.mem_read(ptr, 64)) == utile):
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart {etiquette} : type {type_desc}, longueur {longueur} -> "
                      f"rax={rax} (modèle {verdict_m})")
    return ecarts


# --- Générateurs --------------------------------------------------------------------

def cas_tls01(alea: random.Random, n: int) -> list[bytes]:
    cas = [b"", b"a", b"host.example.com", bytes(255), bytes(256), bytes(300),
           b"\x80abc", b"abc\x80", b"ab\x80cd"]
    cas += [bytes([alea.choice((0x61, 0x7A, 0x30, 0x2D, 0x80 + alea.randrange(0x40)))
                   for _ in range(alea.randrange(0, 300))]) for _ in range(n)]
    return cas


def cas_tls02(alea: random.Random, n: int) -> list[int]:
    cas = [0]
    for code in L.HRESULTS:
        cas.append(_signe32(code))
        cas.append(code)                       # forme non sign-étendue : hors domaine
        cas.append(_signe32(code ^ (1 << alea.randrange(32))))   # voisin à un bit
    cas.append(_signe32(0x80090321))           # le leurre BUFFER_TOO_SMALL -> 6
    cas.append(_signe32(0x80090326))           # SEC_E_ILLEGAL_MESSAGE -> 6
    cas.append(_signe32(0x00090313))           # SEC_I_COMPLETE_NEEDED -> 6
    for _ in range(n):
        v = alea.getrandbits(32)
        cas.append(_signe32(v))
        if alea.random() < 0.25:               # contrebande de domaine
            cas.append(v | (alea.getrandbits(32) << 32))
    return cas


def cas_tls03(alea: random.Random, n: int) -> list[tuple]:
    tailles_canoniques = struct.pack("<IIIII", 5, 16, 512, 4, 1)
    cas = []
    for t in (0, 1, 2, 3, 7, 0xFFFFFFFF):
        for lon in (0, 1, 16384, 16385, 511, 512, 513, 4096):
            cas.append((t, ZONE_SRC + 0x10, lon, tailles_canoniques))
    cas += [(1, ZONE_SRC + 0x10, lon, struct.pack("<IIIII", t, q, m, 4, 1))
            for t in (0, 1, 5, 0xFFFF) for q in (0, 1, 16, 0xFFFF)
            for m in (0, 1, 512, 0xFFFF) for lon in (0, 1, m, m + 1)]
    for _ in range(n):
        t = alea.randrange(0, 5)
        tailles = struct.pack("<IIIII", alea.randrange(0, 64),
                              alea.randrange(0, 64), alea.randrange(0, 2048), 4, 1)
        cas.append((t, ZONE_SRC + 0x10, alea.randrange(0, 8192), tailles))
    return cas


# --- Main ---------------------------------------------------------------------------

def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261028)
    parseur.add_argument("--cas", type=int, default=20000)
    args = parseur.parse_args()
    alea = random.Random(args.graine)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)

    print("=== harnais_feuilles.py — feuilles pures M4 (tls-01..03), "
          f"graine {args.graine} ===")

    # V1 — round-trip
    print("\n--- V1 : round-trip de notation ---")
    blocs = [("tls-01-nom-utf16", RVA_TLS01), ("tls-02-verdicts", RVA_TLS02),
             ("tls-03-jetons", RVA_TLS03)]
    blobs = {}
    for nom, rva in blocs:
        blob, declare = octets_notation(ks, nom, rva)
        blobs[nom] = blob
        controle(f"V1 {nom} : rassemblage intégral ({len(blob)} o == "
                 f"« Code : {declare} o » déclarés)", len(blob) == declare)
        passe2 = assembler_lignes(ks, lignes_notation(os.path.join(
            ICI, "notation", nom + ".asm")), rva)
        controle(f"V1 {nom} : idempotence (2e passe octet-identique)", passe2 == blob)

    emu = Emulateur()

    # V2/V3 — différentiel + hygiène (témoin sauvage = notation intacte)
    print(f"\n--- V2/V3 : différentiel contre modèle de spécification "
          f"({args.cas} cas par feuille + vecteurs de bord) ---")
    c1 = cas_tls01(alea, args.cas)
    e1 = differentiel_tls01(emu, blobs["tls-01-nom-utf16"], c1, "témoin")
    controle(f"V2/V3 tls-01 : {len(c1)} cas, ZÉRO écart "
             f"(verdicts, contenus, longueurs, canaris, non-volatils)", e1 == 0,
             f"{e1} écarts")

    c2 = cas_tls02(alea, args.cas * 5)
    e2 = differentiel_tls02(emu, blobs["tls-02-verdicts"], c2, "témoin")
    controle(f"V2/V3 tls-02 : {len(c2)} HRESULT (codes exacts + voisins à un bit + "
             f"hors domaine + aléatoires), ZÉRO écart", e2 == 0, f"{e2} écarts")

    c3 = cas_tls03(alea, args.cas)
    e3 = differentiel_tls03(emu, blobs["tls-03-jetons"], c3, "témoin")
    controle(f"V2/V3 tls-03 : {len(c3)} triplets (types hostiles, bornes exactes "
             f"16384/max ±1, tailles exotiques), ZÉRO écart", e3 == 0, f"{e3} écarts")

    # V4 — falsification : une mutation d'UN point doit être attrapée
    print("\n--- V4 : falsification (une suite qui ne peut pas échouer ne prouve rien) ---")
    mutations = [
        ("tls-01-nom-utf16", RVA_TLS01, "cmp rdx, 255", "cmp rdx, 256",
         differentiel_tls01, lambda a, r: cas_tls01(a, 2000),
         "tls-01 borne HOTE_MAX relâchée de 1 (hôte de 255 accepté à tort)"),
        ("tls-01-nom-utf16", RVA_TLS01, "add rdx, 2", "add rdx, 4",
         differentiel_tls01, lambda a, r: cas_tls01(a, 2000),
         "tls-01 longueur écrite faussée (+2)"),
        ("tls-02-verdicts", RVA_TLS02, "cmp ecx, 0x80090330", "cmp ecx, 0x80090321",
         differentiel_tls02, lambda a, r: cas_tls02(a, 5000),
         "tls-02 DECRYPT_FAILURE confondu avec BUFFER_TOO_SMALL (contrebande de classe)"),
        ("tls-02-verdicts", RVA_TLS02, "mov eax, 3", "mov eax, 5",
         differentiel_tls02, lambda a, r: cas_tls02(a, 5000),
         "tls-02 verdict certificat dévié vers échec négocié"),
        ("tls-03-jetons", RVA_TLS03, "cmp r8, 16384", "cmp r8, 32768",
         differentiel_tls03, lambda a, r: cas_tls03(a, 2000),
         "tls-03 borne MAX_JETON doublée (jeton de 20000 accepté à tort)"),
        ("tls-03-jetons", RVA_TLS03, "mov dword ptr [r9 + 4], 4", "mov dword ptr [r9 + 4], 3",
         differentiel_tls03, lambda a, r: cas_tls03(a, 2000),
         "tls-03 compte de tampons de réception erroné (4 -> 3)"),
    ]
    for nom, rva, avant, apres, fonc, gen, desc in mutations:
        blob_m, _ = octets_notation(ks, nom, rva, mutation=(avant, apres))
        alea_m = random.Random(args.graine + 1)
        ecarts = fonc(emu, blob_m, gen(alea_m, None), "mutée")
        controle(f"V4 {desc} : ATTRAPÉE par le différentiel", ecarts > 0,
                 f"{ecarts} écarts sur la mutée")

    print("\n" + "=" * 78)
    print(f"BILAN : {len(REUSSITES)} PASS, {len(ECHECS)} ÉCHEC "
          f"(graine {args.graine}, {args.cas} cas/feuille)")
    for nom in ECHECS:
        print(f"  FAIL {nom}")
    if not ECHECS:
        print("Les trois feuilles pures tiennent leurs contrats : notation "
              "round-trip 100 %, différentiel de spécification sans écart,")
        print("hygiène (canaris, non-volatils, terminaison) constatée, suite "
              "falsifiable (6/6 mutations attrapées, témoin vert).")
    print("=" * 78)
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main())
