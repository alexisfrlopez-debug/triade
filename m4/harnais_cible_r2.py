#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_cible_r2.py — Harnais de la révision http-08:R2 (D91).

Vecteurs de la spécification m4/I/http-08-cible-r2.md (écrite-avant-code,
D77 — le modèle des révisions inter-jalons, lignée win-02:R2) :
  V1  round-trip de notation 100 % — R2 (326 o == en-tête « Code : N o »,
      idempotence) ET l'ancêtre R1 scellé assemblé à son RVA 0x5380 (241 o
      déclarés) : le préalable du différentiel hérité — si l'assemblage de
      R1 ne reproduit pas ses octets, la comparaison qui suit ne prouve rien ;
  V2a différentiel HÉRITÉ (anti-régression R7 comportementale) — l'ancêtre
      R1 ÉMULÉ contre la révision R2 ÉMULÉE sur les mêmes cas : divergence
      LÉGITIME unique = le domaine https exact (R1 : verdict 3 schéma non
      supporté, zone intacte ; R2 : verdict 4 « cible TLS », zone aux règles
      R1) ; TOUT autre écart est une régression de l'héritage scellé ;
  V2b différentiel de SPÉCIFICATION — R2 émulée contre un modèle de
      référence écrit depuis la spécification (jamais depuis la notation) :
      verdict, zone 40 o octet par octet (forme @0, autorité @8/@16, chemin
      @24/@32 — le padding @4..7 n'est JAMAIS écrit, il reste à l'appelant),
      couvre P*, Q*, I* — vecteurs de bord nommés + cas structurés hostiles ;
  V3  propriétés d'hygiène héritées D45 (entrées non fiables directes) —
      survie, terminaison bornée, verdict conforme au modèle, aucune écriture
      hors la zone d'accueil (canaris DST), SRC intact, non-volatils ;
  V4  falsification — des mutations D'UN SEUL point de la notation, STABLES
      EN TAILLE (leçon D82), doivent être ATTRAPÉES par le différentiel ;
      le témoin (notation intacte) doit rester vert.

Le harnais émule les octets des NOTATIONS (ce que build_m4.py embarquera pour
R2, l'ancêtre scellé 0.4.0 pour R1 — la révision embarquée vit à 0x7340, son
ancêtre reste indexé par la carte génération 5 à 0x5380 : les DEUX sont
chargés dans la même page, exécutés sur les MÊMES entrées).
Usage : python3 harnais_cible_r2.py [--graine G] [--cas N] [--fuzz N]
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

# --- Mémoire du harnais (hors image PE : émulation nue des deux notations) ------

ZONE_TEXT = 0x5000            # couvre .text2 (R1 @0x5380) et .text3 (R2 @0x7340)
TAILLE_TEXT = 0x3000          # 0x5000-0x7FFF (page int3 de fond)
RET_MAGIQUE = 0x7F00          # ZONE_RESERVEE_T3 du plan — l'arrêt propre
RVA_R1 = 0x5380               # http-08:R1 (héritage scellé 0.4.0, R7)
_R2 = next((r, s) for b, _, r, s, _, _ in L.BLOCS_TLS + L.BLOCS_REVISIONS
           if b == "g70009")
RVA_R2, SLOT_R2 = _R2         # 0x7340 x 0x180 (layout.py, source unique)
ZONE_RDATA = 0x2000           # .rdata héritée (fixture « / » @ R_SLASH)
TAILLE_RDATA = 0x1000
ZONE_SRC = 0x10000            # span cible (tampon de l'appelant http-02)
TAILLE_SRC = 0x1000
ZONE_DST = 0x20000            # zone d'accueil « cible résolue » (40 o utiles)
TAILLE_DST = 0x1000
ZONE_PILE = 0x7F000000
TAILLE_PILE = 0x10000
RSP = 0x7F008000

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


def modele_cible(cible: bytes, methode: int, revision: int = 2):
    """http-08 — Q1-Q5. revision=1 : comportement de l'ANCIEN R1 (le schéma
    https n'existe pas : il tombe dans le scan « :// » générique → 3).
    Retour : (verdict, forme, aut_off, aut_len, chm_off, chm_len) ;
    chm_off = -1 → fixture « / » ; None → pointeur nul ; zone remplie ssi
    verdict ∈ (0,) pour R1, (0, 4) pour R2."""
    n = len(cible)
    if methode == 8:                      # P3 : CONNECT — la cible entière
        return (0, 3, 0, n, None, 0)
    # I5 : l'ordre des tests est documenté — http:// D'ABORD (héritage R1)
    if n >= 7 and cible[:4] == b"http" and cible[4:6] == b":/" and cible[6:7] == b"/":
        return _absolu(cible, 7, 0)
    # Q4 NOUVEAU : https BYTE-EXACT 8 octets minuscules (revision 2 seule)
    if (revision >= 2 and n >= 8 and cible[:5] == b"https"
            and cible[5:6] == b":" and cible[6:8] == b"//"):
        return _absolu(cible, 8, 4)
    if cible[:1] == b"/":                 # Q1 : forme origine
        return (0, 2, None, 0, 0, n)
    # scan R1 : le PREMIER « : » décide — suivi de « // » DANS le span → 3,
    # sinon → 1 (le scan ne reprend JAMAIS après un « : » échoué)
    i = cible.find(b":")
    if i >= 0 and i + 2 < n and cible[i + 1:i + 3] == b"//":
        return (3, None, None, 0, None, 0)
    return (1, None, None, 0, None, 0)


def zone_attendue(cible: bytes, methode: int, revision: int):
    """(verdict, zone) — zone None = intacte ; sinon (forme_pack, qqqq_pack)
    pour les octets @0-3 et @8-39 (le padding @4-7 n'est jamais écrit)."""
    v, forme, aut_off, aut_len, chm_off, chm_len = modele_cible(cible, methode, revision)
    if v not in ((0,) if revision == 1 else (0, 4)):
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

    def charger(self, blobs: dict[int, bytes]):
        # leçon D79 : chaque chargement RECONSTRUIT l'émulateur (traduction
        # unicorn cachée — un mutant rechargé ne tournait jamais).
        self.__init__()
        page = b"\xCC" * TAILLE_TEXT
        for rva, blob in blobs.items():
            page = page[:rva - ZONE_TEXT] + blob + page[rva - ZONE_TEXT + len(blob):]
        self.uc.mem_write(ZONE_TEXT, page)

    def _preparer(self):
        self.uc.mem_write(ZONE_DST, self.canari_dst)
        for nom, valeur in SENTINELLES_NV.items():
            self.uc.reg_write(_REGS[nom], valeur)
        self.uc.reg_write(_REGS["rsp"], RSP)
        self.uc.mem_write(RSP, struct.pack("<Q", RET_MAGIQUE))

    def executer(self, rva: int, rcx: int, rdx: int, r8: int, r9: int):
        self._preparer()
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


def executer_cas(emu: Emulateur, rva: int, cible: bytes, methode: int):
    """Exécute un cas ; rend (statut, rax, zone_40). Statut « OK » = retour
    propre au RET + terminaison + non-volatils intacts + SRC intact."""
    n = len(cible)
    src_origin = cible + CANARI * (TAILLE_SRC - n)
    emu.uc.mem_write(ZONE_SRC, src_origin)
    try:
        rip, rax = emu.executer(rva, ZONE_SRC, n, methode, ZONE_DST)
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
    return ("OK", rax, zone)


def _diagnostique(cible, methode, statut, rax, v_m):
    return (f"cible={cible[:32]!r} m={methode} -> {statut} rax={rax} "
            f"(modèle {v_m})")


# --- V2/V3 : différentiels ---------------------------------------------------------

def differentiel_spec(emu: Emulateur, blob: bytes, cas: list, etiquette: str) -> int:
    """V2b/V3 — R2 émulée contre le modèle de spécification, hygiène intégrée."""
    emu.charger({RVA_R2: blob})
    ecarts = 0
    for cible, methode in cas:
        v_m, z_m = zone_attendue(cible, methode, 2)
        statut, rax, zone = executer_cas(emu, RVA_R2, cible, methode)
        if statut != "OK" or not conforme(v_m, z_m, rax, zone):
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart {etiquette} : "
                      f"{_diagnostique(cible, methode, statut, rax, v_m)}")
    return ecarts


def differentiel_heritage(emu: Emulateur, blob_r1: bytes, blob_r2: bytes,
                          cas: list) -> tuple[int, int, int]:
    """V2a — l'ancêtre R1 ÉMULÉ contre la révision R2 ÉMULÉE (anti-régression
    R7 comportementale). Retour (écarts-modèles, écarts-divergence, légitimes)
    : légitimes = cas du domaine https (le test byte-exact de la révision) —
    R1 unifiait https dans « schéma non supporté » (3, zone intacte) ; R2
    découpe aux règles R1 : verdict 4 si autorité, Q3 (2) si vide."""
    emu.charger({RVA_R1: blob_r1, RVA_R2: blob_r2})
    ecarts_modeles, ecarts_divergence, legitimes = 0, 0, 0
    for cible, methode in cas:
        v1m, z1m = zone_attendue(cible, methode, 1)
        v2m, z2m = zone_attendue(cible, methode, 2)
        s1, r1, zone1 = executer_cas(emu, RVA_R1, cible, methode)
        s2, r2, zone2 = executer_cas(emu, RVA_R2, cible, methode)
        if s1 != "OK" or not conforme(v1m, z1m, r1, zone1):
            ecarts_modeles += 1
            if ecarts_modeles <= 3:
                print(f"    écart R1-vs-modèle : "
                      f"{_diagnostique(cible, methode, s1, r1, v1m)}")
            continue
        if s2 != "OK" or not conforme(v2m, z2m, r2, zone2):
            ecarts_modeles += 1
            if ecarts_modeles <= 3:
                print(f"    écart R2-vs-modèle : "
                      f"{_diagnostique(cible, methode, s2, r2, v2m)}")
            continue
        if methode != 8 and len(cible) >= 8 and cible[:5] == b"https" \
                and cible[5:6] == b":" and cible[6:8] == b"//":
            # le domaine du Q4 nouveau : la divergence est LÉGITIME et
            # VÉRIFIÉE — R1 rend 3 (schéma non supporté, zone intacte) ;
            # la part R2 (4 avec zone, ou Q3 2 sans) est déjà couverte par
            # la conformité au modèle R2 ci-dessus.
            legitimes += 1
            if not (r1 == 3 and zone1 == CANARI * 40):
                ecarts_divergence += 1
                if ecarts_divergence <= 3:
                    print(f"    divergence INCORRECTE sur https : "
                          f"R1 rax={r1} ({cible[:24]!r})")
        elif (r1, zone1) != (r2, zone2):  # hors https : RÉGRESSION
            ecarts_divergence += 1
            if ecarts_divergence <= 3:
                print(f"    RÉGRESSION hors https : R1 rax={r1}, R2 rax={r2} "
                      f"({cible[:24]!r})")
    return ecarts_modeles, ecarts_divergence, legitimes


# --- Générateurs --------------------------------------------------------------------

def cas_diriges() -> list:
    """Vecteurs de bord — chaque frontière de la spécification, nommée."""
    return [
        # héritage R1 (V2 de R1, D46) — le différentiel hérité les exige TOUS
        (b"http://hote/chemin", 0), (b"http://hote", 0), (b"http://hote?q=1", 0),
        (b"http://", 0), (b"http:///", 0), (b"http:///chemin", 0),
        (b"http://hote:8080/chemin?x", 0), (b"http://HOTE/", 0),
        (b"HTTP://hote/", 0), (b"HtTp://hote/", 0), (b"http:/x", 0),
        (b"/chemin?q=1", 0), (b"/", 0), (b"/*", 0), (b"*", 0),
        (b"hote:443", 0), (b"hote:443", 8), (b"/chemin", 8),
        (b"http://hote/chemin", 8), (b"ftp://f/", 0), (b"x://y/", 0),
        (b"a:b//c", 0), (b"ax:b//http://q", 0),
        # Q4/I5 nouveaux — le domaine https, byte-exact, et ses leurres
        (b"https://hote/chemin", 0), (b"https://hote", 0),
        (b"https://hote?q=1", 0), (b"https://", 0), (b"https:///", 0),
        (b"https:///chemin", 0), (b"https://hote:8443/x?y", 0),
        (b"https://hote/", 0), (b"HTTPS://hote/", 0), (b"HTTPs://hote/", 0),
        (b"httpS://hote/", 0), (b"https:/hote", 0), (b"https:\\hote", 0),
        (b"https:////x", 0), (b"https://HOTE/", 0), (b"http://s://x", 0),
        (b"https://s://x", 0), (b"http://s", 0), (b"https", 0),
        (b"https:", 0), (b"https:/", 0), (b"https://x", 1), (b"https://x", 7),
        (b"https://x", 9), (b"https://hote/chemin", 8),
        # bornes de longueur (P2 > 0) — jamais de lecture hors span
        (b"h", 0), (b"ht", 0), (b"htt", 0), (b"http", 0), (b"http:", 0),
        (b"http:/", 0), (b"http://", 8), (b"https", 8),
    ]


def cas_structures(alea: random.Random, n: int) -> list:
    """V2 — schémas hostiles, casse mixte, préfixes piégeux, autorités
    dégénérées, ports explicites (le générateur étendu de V2-R1 + https)."""
    cas = cas_diriges()
    schemas = [b"http://", b"https://", b"HTTP://", b"HTTPS://", b"Http://",
               b"HttpS://", b"httpS://", b"HTTPs://", b"hTTps://", b"ftp://",
               b"x://", b"s://", b"http:/", b"https:/", b"https:\\", b"http:",
               b"https:", b"https", b"http", b"://", b"/"]
    autorites = [b"hote", b"hote.example.com", b"1.2.3.4", b"hote:80",
                 b"hote:443", b"hote:8443", b"", b"a", b"HOST", b"HO-ST",
                 b"h\xf4te", b"\x80\x81", b"hote.", b".hote"]
    chemins = [b"", b"/", b"/chemin", b"/a/b/c", b"/?q=1", b"?q=1",
               b"/x?y=z", b"//double", b"/trailing/", b"/\x00octet"]
    for _ in range(n):
        cible = alea.choice(schemas) + alea.choice(autorites) + alea.choice(chemins)
        methode = alea.choice((0, 0, 0, 1, 2, 8, 8, 9))
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
        if alea.random() < 0.4:           # biais schéma pour couvrir le Q4
            pre = alea.choice((b"http://", b"https://", b"HTTPS://", b"http:/",
                               b"https:/", b"http:", b"https:"))
            cible = pre + cible[:max(1, lon - len(pre))]
        cas.append((cible, alea.choice((0, 0, 0, 3, 8))))
    return cas


def cas_mutations(alea: random.Random) -> list:
    """V4 — cas DIRIGÉS : chaque mutation d'un point doit trouver ICI son
    cas exposant (I5 byte-exact, casse, préfixe, verdict, forme, « ? »)."""
    return cas_diriges() + [
        (b"https://hote/" + bytes(alea.randrange(0x61, 0x7A)
                                 for _ in range(alea.randrange(1, 8))), 0)
        for _ in range(600)]


# --- Main ---------------------------------------------------------------------------

def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261028)
    parseur.add_argument("--cas", type=int, default=20000)
    parseur.add_argument("--fuzz", type=int, default=20000)
    args = parseur.parse_args()
    alea = random.Random(args.graine)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)

    chemin_r2 = os.path.join(ICI, "notation", "http-08-cible-r2.asm")
    chemin_r1 = os.path.join(ICI, "..", "m3", "notation", "http-08-cible.asm")

    print("=== harnais_cible_r2.py — révision http-08:R2 (schéma https, D91), "
          f"graine {args.graine} ===")

    # V1 — round-trip (R2 + ancêtre R1 : le préalable du différentiel hérité)
    print("\n--- V1 : round-trip de notation ---")
    blob_r2, declare_r2 = octets_notation(ks, chemin_r2, RVA_R2)
    controle(f"V1 http-08:R2 : rassemblage intégral ({len(blob_r2)} o == "
             f"« Code : {declare_r2} o » déclarés)", len(blob_r2) == declare_r2)
    passe2 = assembler_lignes(ks, lignes_notation(chemin_r2), RVA_R2)
    controle("V1 http-08:R2 : idempotence (2e passe octet-identique)",
             passe2 == blob_r2)
    blob_r1, declare_r1 = octets_notation(ks, chemin_r1, RVA_R1)
    controle(f"V1 http-08:R1 (ancêtre scellé) : assemblage à 0x{RVA_R1:x} "
             f"({len(blob_r1)} o == « Code : {declare_r1} o » déclarés)",
             len(blob_r1) == declare_r1)

    emu = Emulateur()

    # V2a — différentiel hérité (anti-régression R7 comportementale)
    print(f"\n--- V2a : différentiel hérité — R1 émulée contre R2 émulée "
          f"({args.cas} cas structurés + vecteurs de bord) ---")
    cas_h = cas_structures(alea, args.cas)
    e_m, e_d, legit = differentiel_heritage(emu, blob_r1, blob_r2, cas_h)
    controle(f"V2a {len(cas_h)} cas : R1 == modèle R1 ET R2 == modèle R2, "
             f"ZÉRO écart ({legit} cas du domaine https : R1 3 -> R2 4 "
             f"ou Q3 2, divergences vérifiées)",
             e_m == 0 and e_d == 0, f"{e_m} + {e_d} écarts")

    # V2b — différentiel de spécification (le témoin sauvage de V4)
    print(f"\n--- V2b : différentiel de spécification ({args.cas} cas, "
          f"modèle écrit depuis la spec — jamais la notation) ---")
    e_spec = differentiel_spec(emu, blob_r2, cas_h, "témoin")
    controle(f"V2b {len(cas_h)} cas : verdicts, zones 40 o octet par octet "
             f"(padding @4-7 jamais écrit), canaris, non-volatils, SRC intact "
             f"— ZÉRO écart", e_spec == 0, f"{e_spec} écarts")

    # V3 — fuzz à propriétés (entrées non fiables, D45 hérité)
    print(f"\n--- V3 : fuzz à propriétés ({args.fuzz} cas non fiables) ---")
    cas_v3 = cas_fuzz(alea, args.fuzz)
    e_v3 = differentiel_spec(emu, blob_r2, cas_v3, "fuzz")
    controle(f"V3 {len(cas_v3)} cas : survie, terminaison, verdict conforme, "
             f"aucune écriture hors zone — ZÉRO écart", e_v3 == 0,
             f"{e_v3} écarts")

    # V4 — falsification : une mutation d'UN point (stable en taille, leçon
    # D82) doit être ATTRAPÉE ; le témoin intact reste vert.
    print("\n--- V4 : falsification (une suite qui ne peut pas échouer "
          "ne prouve rien) ---")
    mutations = [
        ("cmp byte ptr [rcx + 7], 0x2F", "cmp byte ptr [rcx + 6], 0x2F",
         "Q4/I5 : le huitième octet amnésié — « https:/x » lu comme https"),
        ("cmp byte ptr [rcx + 4], 0x73", "cmp byte ptr [rcx + 4], 0x53",
         "I5 : minuscules — « httpS:// » (casse mixte) accepté à tort"),
        ("lea r11, [rcx + 8]", "lea r11, [rcx + 7]",
         "I5 : le schéma préfixe — « http://x » reçoit le verdict TLS"),
        ("mov eax, 4", "mov eax, 5",
         "Q4 : verdict « cible TLS » dévié vers une valeur non spécifiée"),
        ("mov r11d, 1", "mov r11d, 5",
         "Q1 : forme ABSOLUE déviée dans la zone d'accueil"),
        ("cmp r11, 0x3F", "cmp r11, 0x40",
         "I3 : le « ? » délimiteur amnésié — découpage d'autorité faux"),
    ]
    alea_m = random.Random(args.graine + 1)
    cas_v4 = cas_mutations(alea_m)
    for avant, apres, desc in mutations:
        blob_m, _ = octets_notation(ks, chemin_r2, RVA_R2, mutation=(avant, apres))
        ecarts = differentiel_spec(emu, blob_m, cas_v4, "mutée")
        controle(f"V4 {desc} : ATTRAPÉE par le différentiel", ecarts > 0,
                 f"{ecarts} écarts sur la mutée")
    e_temoin = differentiel_spec(emu, blob_r2, cas_v4, "témoin V4")
    controle(f"V4 témoin (notation intacte, {len(cas_v4)} cas) : VERT",
             e_temoin == 0, f"{e_temoin} écarts")

    print("\n" + "=" * 78)
    print(f"BILAN : {len(REUSSITES)} PASS, {len(ECHECS)} ÉCHEC "
          f"(graine {args.graine}, {args.cas} cas structurés + "
          f"{args.fuzz} cas fuzz)")
    for nom in ECHECS:
        print(f"  FAIL {nom}")
    if not ECHECS:
        print("La révision http-08:R2 tient son contrat : notation round-trip"
              " 100 %, l'héritage R1 est reproduit octet pour octet sur tout")
        print("cas hors https (divergence UNIQUE : le verdict 4 du domaine"
              " https), le différentiel de spécification est sans écart,")
        print("l'hygiène est constatée, la suite est falsifiable (6/6"
              " mutations attrapées, témoin vert).")
    print("=" * 78)
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main())
