#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_cible_r3.py — Harnais de la révision http-08:R3 (0.6.0, D136).

Vecteurs de la spécification m5/I/http-08-cible-r3.md (écrite-avant-code) :
  V1  round-trip de notation 100 % — R3 (377 o == en-tête « Code : N o »,
      idempotence) ET l'ancêtre R2 scellé assemblé à son RVA 0x7340 (326 o
      déclarés) : le préalable du différentiel hérité — si l'assemblage de
      R2 ne reproduit pas ses octets, la comparaison qui suit ne prouve rien ;
  V2a différentiel HÉRITÉ SANS POLITIQUE (Q7/E2 — anti-régression R7
      comportementale) : R2 émulée contre R3 émulée avec P5 = 0 sur les
      MÊMES cas : ZÉRO écart autorisé — « sans politique : R2 OCTET POUR
      OCTET sur tout chemin » ; AVEC politique (P5 = 1) : divergence
      LÉGITIME unique = le domaine http:// absolu (R2 verdict 0 → R3
      verdict 5, la ZONE remplie aux mêmes règles R1 — forme 1, autorité,
      chemin : seule la valeur propre change) ;
  V2b différentiel de SPÉCIFICATION SOUS LES DEUX POLITIQUES — R3 émulée
      contre un modèle de référence écrit depuis la spécification (jamais
      depuis la notation) : verdict, zone 40 o octet par octet (forme @0,
      autorité @8/@16, chemin @24/@32 — le padding @4..7 n'est JAMAIS
      écrit), P5/P6/P7 (la politique en CINQUIÈME argument, loge
      [rsp+0x30] du callee, lue UNE fois), couvre Q1-Q6, I6 (l'ordre des
      tests : « http:// » D'ABORD — le verdict 5 naît À LA PLACE du
      succès générique ; « https:// » inchangé) ;
  V3  propriétés d'hygiène héritées D45 (entrées non fiables directes)
      sous les DEUX politiques — survie, terminaison bornée, verdict
      conforme au modèle, aucune écriture hors la zone d'accueil (canaris
      DST), SRC intact, non-volatils ;
  V4  falsification — des mutations D'UN SEUL point de la notation,
      STABLES EN TAILLE (leçon D82), doivent être ATTRAPÉES par le
      différentiel ; le témoin (notation intacte) doit rester vert.

Le harnais émule les octets des NOTATIONS (ce que build_m5.py embarquera :
R3 vit à 0x8000 en .text4 ; l'ancêtre R2 reste scellé à 0x7340 en .text3,
embarqué 0.5.1 — les DEUX sont chargés dans la même page, exécutés sur les
MÊMES entrées, la politique écrite à la loge de pile de l'appelant).
Usage : python3 harnais_cible_r3.py [--graine G] [--cas N] [--fuzz N]
"""

from __future__ import annotations

import argparse
import os
import random
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
# Le plan M5 chargé SOUS NOM PROPRE (miroir harnais_session_r3) : le fichier
# s'appelle layout.py des deux côtés — l'import classique dépendrait de
# l'ORDRE de sys.path du processus appelant (standalone : m5 ; depuis
# l'oracle : m4 d'abord pour les shims D90/D92). Le chargement direct est
# indépendant de l'ordre — même module, mêmes octets, jamais deux sources.
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location(
    "layout_m5", os.path.join(ICI, "layout.py"))
L = importlib.util.module_from_spec(_spec)   # le plan M5 (source unique)
_spec.loader.exec_module(L)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64  # noqa: E402

# --- Mémoire du harnais (hors image PE : émulation nue des deux notations) ------

ZONE_TEXT = 0x5000            # couvre .text2/.text3 (R2 @0x7340) et .text4 (R3 @0x8000)
TAILLE_TEXT = 0x5000          # 0x5000-0x9FFF (page int3 de fond)
RET_MAGIQUE = 0x7F00          # ZONE_RESERVEE_T3 du plan — l'arrêt propre
_R2 = next((r, s) for b, _, r, s, _, _ in
           L.L4.BLOCS_TLS + L.L4.BLOCS_REVISIONS if b == "g70009")
RVA_R2, SLOT_R2 = _R2         # 0x7340 x 0x180 (m4/layout.py, source unique)
_R3 = next((r, s) for b, _, r, s, _, _ in L.BLOCS_REVISIONS_M5 if b == "g80001")
RVA_R3, SLOT_R3 = _R3         # 0x8000 x 0x1C0 (m5/layout.py, source unique)
ZONE_RDATA = 0x2000           # .rdata héritée (fixture « / » @ R_SLASH)
TAILLE_RDATA = 0x1000
ZONE_SRC = 0x10000            # span cible (tampon de l'appelant http-02)
TAILLE_SRC = 0x1000
ZONE_DST = 0x20000            # zone d'accueil « cible résolue » (40 o utiles)
TAILLE_DST = 0x1000
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP = 0x7F008000
LOGE_POLITIQUE = 0x30         # P5 : la politique au callee — [rsp+0x30] du
                              # callee = 5e argument msx64 (rcx/rdx/r8/r9
                              # registres + loge 0x28 du CALL : +0x30 ici,
                              # le RET_MAGIQUE occupe [rsp])

CANARI = b"\xA5"
R_SLASH = L.R_SLASH           # 0x24D0 — fixture « / » de l'ancêtre R1 (R7)

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


# --- Modèle de référence (écrit depuis la SPÉCIFICATION — jamais la notation) ------

def _absolu(cible: bytes, debut: int, verdict: int):
    """Découpage absolu aux règles R1 depuis debut (7 http / 8 https) :
    autorité jusqu'au PREMIER « / » ou « ? » (I3), chemin du « / » à la fin,
    « / » par défaut sinon (Q1) ; autorité vide → Q3 (2, zone intacte)."""
    n = len(cible)
    pos = n
    for i in range(debut, n):
        if cible[i] in (0x2F, 0x3F):
            pos = i
            break
    if pos == debut:
        return (2, None, None, 0, None, 0)
    if cible[pos:pos + 1] == b"/":
        return (verdict, 1, debut, pos - debut, pos, n - pos)
    return (verdict, 1, debut, pos - debut, -1, 1)   # « ? » ou fin → fixture « / »


def modele_cible(cible: bytes, methode: int, politique: int = 0):
    """http-08:R3 — Q1-Q6. La révision ne change RIEN de R2 (le modèle R2 est
    repris tel quel) SAUF : forme absolue « http:// » ET politique armée →
    rax = 5, verdict « cible à relever » (valeur propre, distincte du succès
    générique 0 et du verdict TLS 4) ; la zone est remplie aux règles R1
    (forme ABSOLUE = 1 — la STRUCTURE est absolue, découpages identiques).
    Retour : (verdict, forme, aut_off, aut_len, chm_off, chm_len) ;
    chm_off = -1 → fixture « / » ; None → pointeur nul ; zone remplie ssi
    verdict ∈ (0, 4, 5) — sans politique le verdict 5 est IMPOSSIBLE (E2)."""
    n = len(cible)
    if methode == 8:                      # P3 : CONNECT — la cible entière
        return (0, 3, 0, n, None, 0)
    # I6 : l'ordre des tests est documenté — http:// D'ABORD : le verdict 5
    # naît À LA PLACE du succès générique (jamais après) ; le début
    # d'autorité du verdict 5 est rcx+7, distinct du seuil rcx+8 du verdict 4
    if n >= 7 and cible[:4] == b"http" and cible[4:6] == b":/" and cible[6:7] == b"/":
        return _absolu(cible, 7, 5 if politique else 0)
    # Q4 hérité : https BYTE-EXACT 8 octets minuscules — INCHANGÉ
    if n >= 8 and cible[:5] == b"https" and cible[5:6] == b":" and cible[6:8] == b"//":
        return _absolu(cible, 8, 4)
    if cible[:1] == b"/":                 # Q1 : forme origine
        return (0, 2, None, 0, 0, n)
    # scan R1 : le PREMIER « : » décide — suivi de « // » DANS le span → 3,
    # sinon → 1 (le scan ne reprend JAMAIS après un « : » échoué)
    i = cible.find(b":")
    if i >= 0 and i + 2 < n and cible[i + 1:i + 3] == b"//":
        return (3, None, None, 0, None, 0)
    return (1, None, None, 0, None, 0)


def zone_attendue(cible: bytes, methode: int, politique: int):
    """(verdict, zone) — zone None = intacte ; sinon (forme_pack, qqqq_pack)
    pour les octets @0-3 et @8-39 (le padding @4-7 n'est jamais écrit)."""
    v, forme, aut_off, aut_len, chm_off, chm_len = modele_cible(cible, methode, politique)
    if v not in (0, 4, 5):
        return v, None
    aut_ptr = ZONE_SRC + aut_off if aut_off is not None else 0
    if chm_off == -1:
        chm_ptr, chm_len = R_SLASH, 1
    elif chm_off is not None:
        chm_ptr = ZONE_SRC + chm_off
    else:
        chm_ptr = 0
    return v, (struct.pack("<I", forme), struct.pack("<QQQQ", aut_ptr, aut_len,
                                                     chm_ptr, chm_len))


def conforme(v_m, z_m, rax, zone_lue) -> bool:
    if rax != v_m:
        return False
    if z_m is None:
        return zone_lue == CANARI * 40
    forme_pack, qqqq = z_m
    return (zone_lue[0:4] == forme_pack and zone_lue[4:8] == CANARI * 4
            and zone_lue[8:40] == qqqq)


# --- Émulation (unicorn) -----------------------------------------------------------

SENTINELLES_NV = {  # non-volatils préchargés — I4
    "rbx": 0x1212121212121212, "rbp": 0x2323232323232323,
    "rdi": 0x3434343434343434, "rsi": 0x4545454545454545,
    "r12": 0x5656565656565656, "r13": 0x6767676767676767,
    "r14": 0x7878787878787878, "r15": 0x8989898989898989,
}


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


class Emulateur:
    def __init__(self):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        for base, taille in ((ZONE_TEXT, TAILLE_TEXT), (ZONE_RDATA, TAILLE_RDATA),
                              (ZONE_SRC, TAILLE_SRC), (ZONE_DST, TAILLE_DST),
                              (ZONE_PILE, TAILLE_PILE)):
            self.uc.mem_map(base, taille)
        self.canari_dst = CANARI * TAILLE_DST
        # fixture de l'ancêtre R1 — le chemin par défaut « / » (chaîne + NUL)
        self.uc.mem_write(R_SLASH, b"/\x00")
        # la PILE entière en canari : la loge de politique est écrite à chaque
        # exécution ; au-delà, TOUT octet lu est non nul — une notation mutée
        # qui lirait hors loge verrait « armée » et serait ATTRAPÉE (I7)
        self.uc.mem_write(ZONE_PILE, CANARI * TAILLE_PILE)

    def charger(self, blobs: dict[int, bytes]):
        # leçon D79 : chaque chargement RECONSTRUIT l'émulateur (traduction
        # unicorn cachée — un mutant rechargé ne tournait jamais).
        self.__init__()
        page = b"\xCC" * TAILLE_TEXT
        for rva, blob in blobs.items():
            page = page[:rva - ZONE_TEXT] + blob + page[rva - ZONE_TEXT + len(blob):]
        self.uc.mem_write(ZONE_TEXT, page)

    def _preparer(self, politique: int):
        self.uc.mem_write(ZONE_DST, self.canari_dst)
        for nom, valeur in SENTINELLES_NV.items():
            self.uc.reg_write(_REGS[nom], valeur)
        self.uc.reg_write(_REGS["rsp"], RSP)
        self.uc.mem_write(RSP, struct.pack("<Q", RET_MAGIQUE))
        # P5 : la politique à la loge du 5e argument — écrite par l'APPELANT
        self.uc.mem_write(RSP + LOGE_POLITIQUE, struct.pack("<Q", politique))

    def executer(self, rva: int, rcx: int, rdx: int, r8: int, r9: int,
                 politique: int):
        self._preparer(politique)
        self.uc.reg_write(_REGS["rcx"], rcx)
        self.uc.reg_write(_REGS["rdx"], rdx)
        self.uc.reg_write(_REGS["r8"], r8)
        self.uc.reg_write(_REGS["r9"], r9)
        self.uc.emu_start(rva, RET_MAGIQUE, timeout=2_000_000, count=100_000)
        return (self.uc.reg_read(_REGS["rip"]), self.uc.reg_read(_REGS["rax"]))

    def lecture_dst(self, n: int) -> bytes:
        return bytes(self.uc.mem_read(ZONE_DST, n))

    def non_volatils_intacts(self) -> bool:
        return all(self.uc.reg_read(_REGS[n]) == v
                   for n, v in SENTINELLES_NV.items())

    def pile_intacte_hors_loge(self) -> bool:
        """I7 — la notation n'écrit JAMAIS la pile : hors la loge de
        politique (écrite par l'appelant) et le mot de retour, le canari
        tient."""
        zone = bytes(self.uc.mem_read(RSP, 0x100))
        attendu = bytearray(CANARI * 0x100)
        attendu[0:8] = struct.pack("<Q", RET_MAGIQUE)
        attendu[LOGE_POLITIQUE:LOGE_POLITIQUE + 8] = struct.pack("<Q",
                                                                 self._pol)
        return zone == bytes(attendu)


def executer_cas(emu: Emulateur, rva: int, cible: bytes, methode: int,
                 politique: int):
    """Exécute un cas ; rend (statut, rax, zone_40). Statut « OK » = retour
    propre au RET + terminaison + non-volatils intacts + SRC intact +
    pile intacte hors loge."""
    n = len(cible)
    src_origin = cible + CANARI * (TAILLE_SRC - n)
    emu.uc.mem_write(ZONE_SRC, src_origin)
    emu._pol = politique
    try:
        rip, rax = emu.executer(rva, ZONE_SRC, n, methode, ZONE_DST, politique)
    except Exception as exc:
        return ("CRASH", repr(exc)[:60], None)
    if rip != RET_MAGIQUE:
        return ("PAS_RET", hex(rip), None)
    if not emu.non_volatils_intacts():
        return ("NV", "", None)
    if bytes(emu.uc.mem_read(ZONE_SRC, TAILLE_SRC)) != src_origin:
        return ("SRC", "", None)
    zone = emu.lecture_dst(40)
    if emu.lecture_dst(TAILLE_DST)[40:] != CANARI * (TAILLE_DST - 40):
        return ("DST", "", None)
    if not emu.pile_intacte_hors_loge():
        return ("PILE", "", None)
    return ("OK", rax, zone)


def _diagnostique(cible, methode, statut, rax, v_m):
    return (f"cible={cible[:32]!r} m={methode} -> {statut} rax={rax} "
            f"(modèle {v_m})")


# --- V2/V3 : différentiels ---------------------------------------------------------

def differentiel_spec(emu: Emulateur, blob: bytes, cas: list, etiquette: str,
                      politique: int) -> int:
    """V2b/V3 — R3 émulée contre le modèle de spécification, hygiène
    intégrée, sous la politique donnée."""
    emu.charger({RVA_R3: blob})
    ecarts = 0
    for cible, methode in cas:
        v_m, z_m = zone_attendue(cible, methode, politique)
        statut, rax, zone = executer_cas(emu, RVA_R3, cible, methode, politique)
        if statut != "OK" or not conforme(v_m, z_m, rax, zone):
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart {etiquette} : "
                      f"{_diagnostique(cible, methode, statut, rax, v_m)}")
    return ecarts


def differentiel_heritage(emu: Emulateur, blob_r2: bytes, blob_r3: bytes,
                          cas: list) -> tuple[int, int, int]:
    """V2a — l'ancêtre R2 ÉMULÉ contre la révision R3 ÉMULÉE. Retour
    (écarts-modèles, écarts-divergence, légitimes) : sans politique, ZÉRO
    divergence autorisée (Q7 : R2 octet pour octet) ; avec politique, la
    divergence est LÉGITIME UNIQUEMENT sur le domaine http:// absolu
    (R2 : 0 zone R1 ; R3 : 5 MÊME zone — seule la valeur propre change) —
    tout autre écart est une régression de l'héritage scellé."""
    emu.charger({RVA_R2: blob_r2, RVA_R3: blob_r3})
    ecarts_modeles, ecarts_divergence, legitimes = 0, 0, 0
    for cible, methode in cas:
        v2m, z2m = zone_attendue(cible, methode, 0)      # R2 == R3 sans politique
        v3m, z3m = zone_attendue(cible, methode, 1)
        s2, r2, zone2 = executer_cas(emu, RVA_R2, cible, methode, 0)
        if s2 != "OK" or not conforme(v2m, z2m, r2, zone2):
            ecarts_modeles += 1
            if ecarts_modeles <= 3:
                print(f"    écart R2-vs-modèle : "
                      f"{_diagnostique(cible, methode, s2, r2, v2m)}")
            continue
        # Q7 : SANS politique — R3 == R2, octet pour octet, tout chemin
        s3, r3, zone3 = executer_cas(emu, RVA_R3, cible, methode, 0)
        if s3 != "OK" or not conforme(v2m, z2m, r3, zone3):
            ecarts_modeles += 1
            if ecarts_modeles <= 3:
                print(f"    écart R3-sans-politique-vs-modèle : "
                      f"{_diagnostique(cible, methode, s3, r3, v2m)}")
            continue
        if (r3, zone3) != (r2, zone2):
            ecarts_divergence += 1
            if ecarts_divergence <= 3:
                print(f"    RÉGRESSION sans politique : R2 rax={r2}, "
                      f"R3 rax={r3} ({cible[:24]!r})")
            continue
        # P5 armée : le modèle R3 tranche
        s3b, r3b, zone3b = executer_cas(emu, RVA_R3, cible, methode, 1)
        if s3b != "OK" or not conforme(v3m, z3m, r3b, zone3b):
            ecarts_modeles += 1
            if ecarts_modeles <= 3:
                print(f"    écart R3-politique-vs-modèle : "
                      f"{_diagnostique(cible, methode, s3b, r3b, v3m)}")
            continue
        if r3b != r2 or zone3b != zone2:
            # la divergence doit être EXACTEMENT le verdict 5 du domaine
            # http:// absolu (zone identique, valeur propre seule)
            if not (r2 == 0 and r3b == 5 and zone3b == zone2
                    and _est_domaine_http_absolu(cible, methode)):
                ecarts_divergence += 1
                if ecarts_divergence <= 3:
                    print(f"    divergence HORS DOMAINE : R2 rax={r2}, "
                          f"R3 rax={r3b} ({cible[:24]!r})")
            else:
                legitimes += 1
    return ecarts_modeles, ecarts_divergence, legitimes


def _est_domaine_http_absolu(cible: bytes, methode: int) -> bool:
    v, *_ = modele_cible(cible, methode, 1)
    return v == 5


# --- Générateurs --------------------------------------------------------------------

def cas_diriges() -> list:
    """Vecteurs de bord — chaque frontière de la spécification, nommée."""
    return [
        # héritage R2 (V2 de R2, D91) — le différentiel hérité les exige TOUS
        (b"http://hote/chemin", 0), (b"http://hote", 0), (b"http://hote?q=1", 0),
        (b"http://", 0), (b"http:///", 0), (b"http:///chemin", 0),
        (b"http://hote:8080/chemin?x", 0), (b"http://HOTE/", 0),
        (b"HTTP://hote/", 0), (b"HtTp://hote/", 0), (b"http:/x", 0),
        (b"/chemin?q=1", 0), (b"/", 0), (b"/*", 0), (b"*", 0),
        (b"hote:443", 0), (b"hote:443", 8), (b"/chemin", 8),
        (b"http://hote/chemin", 8), (b"ftp://f/", 0), (b"x://y/", 0),
        (b"a:b//c", 0), (b"ax:b//http://q", 0),
        # le domaine https (Q4 hérité, INCHANGÉ par la révision)
        (b"https://hote/chemin", 0), (b"https://hote", 0),
        (b"https://hote?q=1", 0), (b"https://", 0), (b"https:///", 0),
        (b"https:///chemin", 0), (b"https://hote:8443/x?y", 0),
        (b"https://hote/", 0), (b"HTTPS://hote/", 0), (b"HTTPs://hote/", 0),
        (b"httpS://hote/", 0), (b"https:/hote", 0), (b"https:\\hote", 0),
        (b"https:////x", 0), (b"https://HOTE/", 0),
        # le domaine du Q6 NOUVEAU — le verdict 5 sous politique armée, et
        # ses leurres : préfixe, casse, autorité vide, port explicite (E3 de
        # http-10:R3 : l'explicite du navigateur est PERDU au relèvement)
        (b"http://s://x", 0), (b"https://s://x", 0), (b"http://s", 0),
        (b"http://autorite.test/", 0), (b"http://autorite.test", 0),
        (b"http://autorite.test:8080/", 0), (b"http://autorite.test?q=1", 0),
        (b"http://a.b.c.d.e.f.g/", 0), (b"http://\x80hote/", 0),
        (b"http://hote/\x00octet", 0), (b"Http://hote/", 0),
        (b"http://x", 1), (b"http://x", 7), (b"http://x", 9),
        (b"http://", 8), (b"https", 8), (b"https://x", 8),
        # bornes de longueur (P2 > 0) — jamais de lecture hors span
        (b"h", 0), (b"ht", 0), (b"htt", 0), (b"http", 0), (b"http:", 0),
        (b"http:/", 0), (b"http://", 8),
    ]


def cas_structures(alea: random.Random, n: int) -> list:
    """V2 — schémas hostiles, casse mixte, préfixes piégeux, autorités
    dégénérées, ports explicites (le générateur de R2 + le biais http://)."""
    cas = cas_diriges()
    schemas = [b"http://", b"https://", b"HTTP://", b"HTTPS://", b"Http://",
               b"HttpS://", b"httpS://", b"HTTPs://", b"hTTps://", b"ftp://",
               b"x://", b"s://", b"http:/", b"https:/", b"https:\\", b"http:",
               b"https:", b"https", b"http", b"://", b"/"]
    autorites = [b"hote", b"hote.example.com", b"1.2.3.4", b"hote:80",
                 b"hote:443", b"hote:8443", b"", b"a", b"HOST", b"HO-ST",
                 b"h\xf4te", b"\x80\x81", b"hote.", b".hote", b"autorite.test"]
    chemins = [b"", b"/", b"/chemin", b"/a/b/c", b"/?q=1", b"?q=1",
               b"/x?y=z", b"//double", b"/trailing/", b"/\x00octet"]
    for _ in range(n):
        cible = alea.choice(schemas) + alea.choice(autorites) + alea.choice(chemins)
        methode = alea.choice((0, 0, 0, 0, 1, 2, 8, 8, 9))
        if len(cible) == 0:               # P2 : longueur > 0 garantie
            cible = b"/"
        cas.append((cible, methode))
    return cas


def cas_fuzz(alea: random.Random, n: int) -> list:
    """V3 — entrées NON FIABLES (D45 hérité) : octets quelconques (y compris
    >= 0x80 et NUL), longueurs hostiles — survie, terminaison, verdict du
    modèle, aucune écriture hors zone."""
    cas = []
    for _ in range(n):
        lon = alea.randrange(1, 220)
        alphabet = bytes(b"htpsHTPS:/?.-@aZ019*\\[]%&") + bytes(range(0x80, 0x90))
        cible = bytes(alea.choice(alphabet) for _ in range(lon))
        if alea.random() < 0.5:           # biais schéma : http ET https
            pre = alea.choice((b"http://", b"https://", b"HTTP://", b"http:/",
                               b"https:/", b"http:", b"https:", b"HTTPS://"))
            cible = pre + cible[:max(1, lon - len(pre))]
        cas.append((cible, alea.choice((0, 0, 0, 0, 3, 8))))
    return cas


def cas_mutations(alea: random.Random) -> list:
    """V4 — cas DIRIGÉS : chaque mutation d'un point doit trouver ICI son
    cas exposant (Q6 byte-exact, politique, casse, préfixe, verdict, forme)."""
    return cas_diriges() + [
        (b"http://" + bytes(alea.randrange(0x61, 0x7A)
                            for _ in range(alea.randrange(1, 8))), 0)
        for _ in range(600)]


# --- Main ---------------------------------------------------------------------------

def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261103)
    parseur.add_argument("--cas", type=int, default=20000)
    parseur.add_argument("--fuzz", type=int, default=20000)
    args = parseur.parse_args()
    alea = random.Random(args.graine)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)

    chemin_r3 = os.path.join(ICI, "notation", "http-08-cible-r3.asm")
    chemin_r2 = os.path.join(ICI, "..", "m4", "notation", "http-08-cible-r2.asm")

    print("=== harnais_cible_r3.py — révision http-08:R3 (verdict 5 « cible à "
          "relever », 0.6.0), graine", args.graine, "===")

    # V1 — round-trip (R3 + ancêtre R2 : le préalable du différentiel hérité)
    print("\n--- V1 : round-trip de notation ---")
    blob_r3, declare_r3 = octets_notation(ks, chemin_r3, RVA_R3)
    controle(f"V1 http-08:R3 : rassemblage intégral ({len(blob_r3)} o == "
             f"« Code : {declare_r3} o » déclarés)", len(blob_r3) == declare_r3)
    passe2 = assembler_lignes(ks, lignes_notation(chemin_r3), RVA_R3)
    controle("V1 http-08:R3 : idempotence (2e passe octet-identique)",
             passe2 == blob_r3)
    blob_r2, declare_r2 = octets_notation(ks, chemin_r2, RVA_R2)
    controle(f"V1 http-08:R2 (ancêtre scellé 0.5.1) : assemblage à 0x{RVA_R2:x} "
             f"({len(blob_r2)} o == « Code : {declare_r2} o » déclarés)",
             len(blob_r2) == declare_r2)

    emu = Emulateur()

    # V2a — différentiel hérité (anti-régression R7 comportementale)
    print(f"\n--- V2a : différentiel hérité — R2 émulée contre R3 émulée "
          f"({args.cas} cas structurés, SANS politique ZÉRO écart / AVEC "
          f"politique divergence http:// SEULE) ---")
    cas_h = cas_structures(alea, args.cas)
    e_m, e_d, legit = differentiel_heritage(emu, blob_r2, blob_r3, cas_h)
    controle(f"V2a {len(cas_h)} cas : sans politique R3 == R2 octet pour "
             f"octet ; armée : {legit} cas du domaine http:// → verdict 5 "
             f"(zone identique), ZÉRO régression",
             e_m == 0 and e_d == 0, f"{e_m} + {e_d} écarts")

    # V2b — différentiel de spécification sous les DEUX politiques
    print(f"\n--- V2b : différentiel de spécification ({args.cas} cas x "
          f"politiques 0/1, modèle écrit depuis la spec — jamais la notation) ---")
    e_abs = differentiel_spec(emu, blob_r3, cas_h, "absente", 0)
    e_arm = differentiel_spec(emu, blob_r3, cas_h, "armée", 1)
    controle(f"V2b {len(cas_h)} cas x 2 : verdicts, zones 40 o octet par "
             f"octet (padding @4-7 jamais écrit), canaris, non-volatils, "
             f"SRC intact, pile intacte hors loge — ZÉRO écart",
             e_abs == 0 and e_arm == 0, f"{e_abs} + {e_arm} écarts")

    # V3 — fuzz à propriétés (entrées non fiables, D45 hérité)
    print(f"\n--- V3 : fuzz à propriétés ({args.fuzz} cas non fiables x "
          f"politiques 0/1) ---")
    cas_v3 = cas_fuzz(alea, args.fuzz)
    e_v3a = differentiel_spec(emu, blob_r3, cas_v3, "fuzz-absente", 0)
    e_v3b = differentiel_spec(emu, blob_r3, cas_v3, "fuzz-armée", 1)
    controle(f"V3 {len(cas_v3)} cas x 2 : survie, terminaison, verdict "
             f"conforme, aucune écriture hors zone — ZÉRO écart",
             e_v3a == 0 and e_v3b == 0, f"{e_v3a} + {e_v3b} écarts")

    # V4 — falsification : une mutation d'UN point (stable en taille, leçon
    # D82) doit être ATTRAPÉE ; le témoin intact reste vert.
    print("\n--- V4 : falsification (une suite qui ne peut pas échouer "
          "ne prouve rien) ---")
    mutations = [
        ("cmp qword ptr [rsp + 0x30], 0", "cmp qword ptr [rsp + 0x38], 0",
         "P5/I7 : la politique lue HORS loge — canari lu comme « armée »"),
        ("je 0x8144", "jne 0x8144",
         "P5 : le test de politique INVERSÉ — armée devient absente"),
        ("mov eax, 5", "mov eax, 4",
         "Q6 : verdict « à relever » dévié vers le verdict TLS"),
        ("mov eax, 5", "mov eax, 0",
         "Q6/E2 : le verdict 5 contrebandé en succès générique"),
        ("mov r11d, 1", "mov r11d, 5",
         "Q6 : forme ABSOLUE déviée dans la zone d'accueil"),
        ("cmp dword ptr [rcx], 0x70747468", "cmp dword ptr [rcx], 0x70747448",
         "I6 : « http » amnésié — régression de l'héritage R2"),
    ]
    alea_m = random.Random(args.graine + 1)
    cas_v4 = cas_mutations(alea_m)
    for avant, apres, desc in mutations:
        blob_m, _ = octets_notation(ks, chemin_r3, RVA_R3, mutation=(avant, apres))
        ecarts_a = differentiel_spec(emu, blob_m, cas_v4, "mutée-absente", 0)
        ecarts_b = differentiel_spec(emu, blob_m, cas_v4, "mutée-armée", 1)
        controle(f"V4 {desc} : ATTRAPÉE par le différentiel",
                 ecarts_a > 0 or ecarts_b > 0,
                 f"{ecarts_a} + {ecarts_b} écarts sur la mutée")
    e_temoin_a = differentiel_spec(emu, blob_r3, cas_v4, "témoin V4 absent", 0)
    e_temoin_b = differentiel_spec(emu, blob_r3, cas_v4, "témoin V4 armé", 1)
    controle(f"V4 témoin (notation intacte, {len(cas_v4)} cas x 2) : VERT",
             e_temoin_a == 0 and e_temoin_b == 0,
             f"{e_temoin_a} + {e_temoin_b} écarts")

    print("\n" + "=" * 78)
    print(f"BILAN : {len(REUSSITES)} PASS, {len(ECHECS)} ÉCHEC "
          f"(graine {args.graine}, {args.cas} cas structurés + "
          f"{args.fuzz} cas fuzz, politiques 0/1)")
    for nom in ECHECS:
        print(f"  FAIL {nom}")
    if not ECHECS:
        print("La révision http-08:R3 tient son contrat : notation round-trip"
              " 100 %, sans politique l'héritage R2 est reproduit octet pour")
        print("octet sur TOUT cas (ZÉRO divergence — Q7), armée la divergence"
              " est EXACTEMENT le verdict 5 du domaine http:// (zone aux")
        print("mêmes règles R1), le différentiel de spécification est sans"
              " écart sous les deux politiques, l'hygiène est constatée, la")
        print("suite est falsifiable (6/6 mutations attrapées, témoin vert).")
    print("=" * 78)
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main())
