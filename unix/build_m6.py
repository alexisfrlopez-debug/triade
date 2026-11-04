#!/usr/bin/env python3
"""build_m6.py — Lignée du jalon M6 (unix/, D149) : sonde, durcissement format.

Chantier M6-(a) : le writer du jalon porte l'image à ET_DYN (PIE, base
aléatoire), trois segments R/RX/RW, PT_GNU_STACK sans X ; la table ERRNOS
(contrat d'erreurs des syscalls, miroir de la table HRESULTS) vit en
.rodata du segment R ; le layout est unix/layout.py (modèle D8). Le critère
de sortie du chantier s'exécute au build même :

  1. couche I chargée et auditée (gabarit § 2.2, 4 specs, R2
     écrite-avant-code) ;
  2. round-trip R5 par bloc (keystone -> capstone -> keystone, WYSIWYG
     octets) ;
  3. oracle structurel : contrats I vérifiés sur le code désassemblé —
     appels directs autorisés PAR BLOC (les sous-programmes locaux déclarés
     passent la même porte : l'étiquette .emit de su-04 est une cible
     nommée), numéros de syscall autorisés PAR BLOC (I1), cibles RIP
     déclarées, accès [base + RVA] déclarés (I3 — le code est indifférent
     à la base), sauts internes aux frontières, padding >= 16, _start sans
     push + pile appariée du sous-programme, symboles @ des brouillons
     confrontés à layout.py ET les longueurs @L_* confrontées aux messages
     RÉELS (leçon C1) ;
  4. composition ELF64 DURCI à la main (ehdr 64 o + 4 phdr 224 o, aucun
     outil de liaison) : ET_DYN, PT_LOAD R (en-têtes + ERRNOS + messages),
     PT_LOAD RX (code, NOP intra-slot, int3 réserves), PT_LOAD RW (.bss
     pur, filesz 0), PT_GNU_STACK RW sans X ;
  5. W^X CONSTATÉ DEPUIS LES PHDR (le build relit son image : aucun
     segment inscriptible exécutable, GNU_STACK sans X) ;
  6. oracle natif : exécution RÉELLE au labo (le bac à sable EST Linux
     x86-64 — la base PIE est choisie par le NOYAU) : quatre lignes
     attendues octet pour octet, code de sortie 6, la table ERRNOS
     exercée sur ses DEUX branches (EBADF nommé → verdict 1 ; EFAULT
     hors table → VERDICT_FATAL 6, arrêt propre) ; la base aléatoire
     CONSTATÉE : >= 2 bases distinctes sur 6 exécutions, alignées à la
     page, et recoupée sous setarch -R (ADDR_NO_RANDOMIZE : deux
     exécutions, MÊME base — la base vient du noyau, jamais du programme) ;
  7. falsification : un octet corrompu dans le CODE de chaque bloc —
     au MOINS une divergence, zéro silence ;
  8. carte génération 1 de la lignée du jalon (sel Argon2id distinct —
     troisième sel : m2, hachoir D34, jalon unix), clés projet partagées
     D27, signature Ed25519, verrou croisé R8 + tableau de bord.

Usage :
  python3 build_m6.py             # construction + oracles + carte
  python3 build_m6.py --verifier  # re-vérification complète (R5/R8) + cristallisation
"""

from __future__ import annotations

import hashlib
import os
import re
import struct
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import layout as L                       # noqa: E402

import capstone                           # noqa: E402
import carte_sonde as cm                  # noqa: E402
from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(ICI), "m2"))
from carte_m2 import empreinte_racine     # noqa: E402  (mécanique commune D27)


class EchecBuild(Exception):
    """Tout échec de l'oracle, du round-trip ou de la construction."""


# --- Couche I : lecture et audit -------------------------------------------------

def lire_spec(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", texte)
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3)), "texte": texte}
    for bloc in ("Intention", "Contrat", "Échecs", "Vecteurs", "Fixtures",
                 "Provenance", "Décisions"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")
    if "écrite-avant-code" not in texte:
        raise EchecBuild(f"{chemin} : provenance inattendue (R2)")
    return spec


def charger_couche_I() -> dict[str, dict]:
    specs = {}
    for bid, sid, fichier, _, _ in L.BLOCS_SU:
        chemin = os.path.join(ICI, "I", fichier + ".md")
        spec = lire_spec(chemin)
        if spec["id"] != sid.split(":")[0]:
            raise EchecBuild(f"{chemin} : identifiant {spec['id']} != {sid}")
        specs[bid] = spec
    return specs


# --- Assemblage : notation -> octets (R5) -----------------------------------------

CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


def assembler_bloc(fichier: str, rva: int, slot: int) -> dict:
    """Notation explicite -> octets + instructions + round-trip intégral.

    Les étiquettes résolues de l'en-tête (auteur) sont conservées : elles
    sont les cibles d'appel LOCALES déclarées (l'oracle les autorise —
    un sous-programme interne est une frontière d'instruction nommée)."""
    chemin = os.path.join(ICI, "notation", fichier + ".asm")
    with open(chemin, encoding="utf-8") as f:
        lignes = [l.strip() for l in f.read().splitlines()]
    instrs = [l for l in lignes if l and not l.startswith(";")]
    labels: dict[str, int] = {}
    for l in lignes:
        m = re.match(r"; Étiquettes résolues : (.+)$", l)
        if m:
            for champ in m.group(1).split(", "):
                nom, _, val = champ.partition("=")
                labels[nom.lstrip(".")] = int(val, 16)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    code, insns = bytearray(), []
    pos = rva
    for texte in instrs:
        enc, _ = ks.asm(texte, pos)
        if not enc:
            raise EchecBuild(f"{fichier} @ {pos:#x} : inassemblable : {texte!r}")
        octets = bytes(enc)
        # R5 : keystone -> capstone -> keystone, identité octets
        des = list(CS.disasm(octets, pos))
        if len(des) != 1:
            raise EchecBuild(f"{fichier} @ {pos:#x} : pas une instruction")
        texte_cs = f"{des[0].mnemonic} {des[0].op_str}".strip()
        enc2, _ = ks.asm(texte_cs, pos)
        if bytes(enc2) != octets:
            raise EchecBuild(f"{fichier} @ {pos:#x} : round-trip R5 rompu : {texte!r}")
        insns.append(des[0])
        code += octets
        pos += len(octets)
    if len(code) > slot:
        raise EchecBuild(f"{fichier} : {len(code)} o > slot {slot:#x} (D8)")
    if slot - len(code) < 16:
        raise EchecBuild(f"{fichier} : padding {slot - len(code)} < 16 (D8)")
    slot_plein = bytes(code) + b"\x90" * (slot - len(code))
    return {"octets": bytes(code), "slot": slot_plein, "insns": insns,
            "texte": instrs, "labels": labels}


def assembler_tout() -> tuple[list, dict, dict, list]:
    specs = charger_couche_I()
    code, verrous = {}, []
    for bid, sid, fichier, rva, slot in L.BLOCS_SU:
        code[bid] = assembler_bloc(fichier, rva, slot)
        code[bid]["spec"] = sid
        code[bid]["fichier"] = fichier
        code[bid]["rva"] = rva
        code[bid]["slot_taille"] = slot
    return list(L.BLOCS_SU), specs, code, verrous


# --- Oracle structurel : contrats I sur le code désassemblé -----------------------

APPELS_AUTORISES = {          # I1/I2 des specs : appels directs par bloc
    "f60004": {L.A_ECRIRE, L.A_HEX64, L.A_VERDICT},
    # (les étiquettes locales déclarées — .emit — s'ajoutent à l'oracle :
    # un sous-programme interne est une cible nommée, frontière du bloc)
}
SYSCALLS_AUTORISES = {        # I1/I2 : numéros de syscall par bloc
    "f60001": {1},            # write (su-01)
    "f60004": {231},          # exit_group (su-04 : trois sites, I2)
}
DONNEES_RIP = {               # I1/I3 : cibles RIP de données par bloc
    "f60002": {L.R_HEXCHARS},
    "f60003": {L.R_ERRNOS},
    "f60004": {L.R_MSG_BASE},   # le témoin de base (lea rip unique)
}
DONNEES_BASE = {              # I3 : accès [base + RVA] déclarés par bloc
    "f60004": {L.R_MSG_BASE, L.R_MSG_P1, L.R_MSG_P2, L.R_MSG_VERD,
               L.R_MSG_FIN, L.R_MSG_FATAL, L.R_TAMPON, L.R_TAMPON_VERD,
               L.R_TAMPON_NUM},
}


def cible_rip(insn) -> int | None:
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", insn.op_str)
    if not m:
        return None
    disp = int(m.group(2), 16)
    return insn.address + insn.size + (disp if m.group(1) == "+" else -disp)


def _prologue_aligne_sysv(insns) -> bool:
    """(8 + 8*npush - sub) ≡ 0 mod 16 — pile alignée aux points d'appel SysV."""
    npush = 0
    while npush < len(insns) and insns[npush].mnemonic == "push":
        npush += 1
    if not any(i.mnemonic == "call" for i in insns):
        return True
    for i in insns:
        if i.mnemonic == "call":
            break
        if i.mnemonic == "sub" and i.op_str.startswith("rsp,"):
            imm = int(i.op_str.split(",")[1].strip(), 16)
            return (8 + 8 * npush - imm) % 16 == 0
    return (8 + 8 * npush) % 16 == 0


def oracle_structurel(code: dict, specs: dict) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    adresses = {bid: {i.address for i in code[bid]["insns"]} for bid in code}
    for bid, bloc in code.items():
        insns = bloc["insns"]
        rva, slot = bloc["rva"], bloc["slot_taille"]
        labels = bloc.get("labels", {})
        # Sauts internes : frontière d'instruction du même bloc
        for i in insns:
            if i.mnemonic[0] == "j":
                cible = int(i.op_str, 16)
                verrou(f"{bid}:saut-interne@{i.address:#x}",
                       cible in adresses[bid], f"cible {cible:#x} hors frontière")
        # Appels directs : les blocs déclarés + les étiquettes locales
        # déclarées (le sous-programme .emit est une cible nommée en I1)
        locaux = set(labels.values())
        for i in insns:
            if i.mnemonic == "call":
                cible = int(i.op_str, 16)
                verrou(f"{bid}:appel-autorise@{i.address:#x}",
                       cible in APPELS_AUTORISES.get(bid, set()) | locaux,
                       f"cible {cible:#x} hors blocs déclarés (I1/I2)")
        # Syscalls : numéros autorisés par bloc, posés juste avant (mov/xor eax)
        nr = None
        for i in insns:
            if i.mnemonic == "mov" and i.op_str.startswith("eax,"):
                try:
                    nr = int(i.op_str.split(",")[1].strip(), 0)
                except ValueError:
                    nr = None
            elif i.mnemonic == "xor" and i.op_str.replace(" ", "") == "eax,eax":
                nr = 0
            if i.mnemonic == "syscall":
                verrou(f"{bid}:syscall-autorise@{i.address:#x}",
                       nr in SYSCALLS_AUTORISES.get(bid, set()),
                       f"nr={nr} non déclaré (I1)")
        # Données RIP : cibles déclarées
        for i in insns:
            cible = cible_rip(i)
            if cible is not None:
                verrou(f"{bid}:donnees-autorisees@{i.address:#x}",
                       cible in DONNEES_RIP.get(bid, set()),
                       f"cible {cible:#x} hors données déclarées (I1/I3)")
        # Accès [base + RVA] : déplacements déclarés (I3 — code indifférent
        # à la base : tout accès données passe par rip ou par rbx + RVA)
        for i in insns:
            for m in re.finditer(r"\[rbx \+ (0x[0-9a-f]+)\]", i.op_str):
                verrou(f"{bid}:base-rva-declaree@{i.address:#x}",
                       int(m.group(1), 16) in DONNEES_BASE.get(bid, set()),
                       f"rbx+{m.group(1)} hors données déclarées (I3)")
        # Padding/alignement (D8/D28/D33)
        fin_code = insns[-1].address + insns[-1].size
        verrou(f"{bid}:padding-16", rva + slot - fin_code >= 16)
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)
        verrou(f"{bid}:slot-multiple-64", slot % 64 == 0)
        # Pile : _start sans push (ABI de démarrage) + sous-programme apparié ;
        # les autres blocs : prologue aligné SysV aux points d'appel
        if bid != "f60004":
            verrou(f"{bid}:pile-alignee", _prologue_aligne_sysv(insns))
        else:
            verrou(f"{bid}:start-sans-push",
                   not any(i.mnemonic == "push" for i in insns))
            nsub = sum(1 for i in insns
                       if i.mnemonic == "sub" and i.op_str.replace(" ", "") == "rsp,8")
            nadd = sum(1 for i in insns
                       if i.mnemonic == "add" and i.op_str.replace(" ", "") == "rsp,8")
            verrou(f"{bid}:pile-appariee", nsub == nadd == 1,
                   f"sub rsp,8 x{nsub} / add rsp,8 x{nadd} (I4 : .emit)")
        # Feuilles pures : su-02/su-03 (I2)
        if bid in ("f60002", "f60003"):
            verrou(f"{bid}:feuille",
                   not any(i.mnemonic in ("call", "push") for i in insns))
    return verrous


# --- Symboles des brouillons confrontés au layout (leçon C1) ---------------------

_MESSAGES = {   # symbole @L_* -> (message réel, longueur attendue)
    "L_BASE": (L.MSG_BASE, L.L_MSG_BASE),
    "L_P1": (L.MSG_P1, L.L_MSG_P1),
    "L_P2": (L.MSG_P2, L.L_MSG_P2),
    "L_VERD": (L.MSG_VERD, L.L_MSG_VERD),
    "L_FIN": (L.MSG_FIN, L.L_MSG_FIN),
    "L_FATAL": (L.MSG_FATAL, L.L_MSG_FATAL),
}
_ADRESSES = {   # symbole @nom -> constante layout (adresse de liaison)
    "A_ECRIRE": L.A_ECRIRE, "A_HEX64": L.A_HEX64, "A_VERDICT": L.A_VERDICT,
    "MSG_BASE": L.R_MSG_BASE, "MSG_P1": L.R_MSG_P1, "MSG_P2": L.R_MSG_P2,
    "MSG_VERD": L.R_MSG_VERD, "MSG_FIN": L.R_MSG_FIN, "MSG_FATAL": L.R_MSG_FATAL,
    "TAMPON": L.R_TAMPON, "TAMPON_VERD": L.R_TAMPON_VERD,
    "TAMPON_NUM": L.R_TAMPON_NUM, "HEXCHARS": L.R_HEXCHARS, "ERRNOS": L.R_ERRNOS,
}


def verifier_symboles() -> int:
    n = 0
    for bid, _, fichier, _, _ in L.BLOCS_SU:
        chemin = os.path.join(ICI, "notation", "brouillons", fichier + ".asm")
        with open(chemin, encoding="utf-8") as f:
            for l in f:
                m = re.match(r"@(\w+)\s*=\s*(0x[0-9a-fA-F]+|\d+)", l.strip())
                if not m:
                    continue
                nom, val = m.group(1), int(m.group(2), 0)
                if nom in _MESSAGES:
                    message, attendue = _MESSAGES[nom]
                    if val != attendue or len(message) != attendue:
                        raise EchecBuild(
                            f"{fichier} : @{nom}={val} != longueur RÉELLE "
                            f"{attendue} de {message!r} (leçon C1)")
                elif nom in _ADRESSES:
                    if val != _ADRESSES[nom]:
                        raise EchecBuild(
                            f"{fichier} : @{nom}={val:#x} != layout "
                            f"{_ADRESSES[nom]:#x} (leçon C1)")
                else:
                    raise EchecBuild(f"{fichier} : symbole inconnu @{nom}")
                n += 1
    return n


# --- Composition ELF64 durci (ehdr + 4 phdr à la main) ----------------------------

def octets_errnos() -> bytes:
    """La table ERRNOS : [nombre u32] + {errno u32, verdict u32} — layout,
    source unique (l'empreinte de la table est vérifiée par valider_elf)."""
    entrees = b"".join(struct.pack("<II", e, v) for e, v in sorted(L.ERRNOS.items()))
    return struct.pack("<I", len(L.ERRNOS)) + entrees


def composer_elf(code: dict) -> bytes:
    """Image durcie : segment R (en-têtes + tables + messages), segment RX
    (code aux slots, NOP intra-slot, int3 réserves), .bss pur (filesz 0)."""
    seg_r = bytearray(b"\xcc" * L.SEG_R_TAILLE)
    seg_rx = bytearray(b"\xcc" * L.SEG_RX_TAILLE)
    poses: list[tuple[int, int, str]] = []       # garde-fou chevauchement (C1)

    def poser(seg: bytearray, base: int, rva: int, donnees: bytes, nom: str = ""):
        poses.append((rva, rva + len(donnees), nom or hex(rva)))
        if rva + len(donnees) > base + len(seg):
            raise EchecBuild(f"segment débordant à {rva:#x} ({nom})")
        seg[rva - base: rva - base + len(donnees)] = donnees

    # — segment R : la table ERRNOS, HEXCHARS, les messages (longueurs
    # explicites — jamais de terminateur : le plan d'adressage les fige)
    poser(seg_r, L.SEG_R_RVA, L.R_ERRNOS, octets_errnos(), "ERRNOS")
    poser(seg_r, L.SEG_R_RVA, L.R_HEXCHARS, L.HEXCHARS, "HEXCHARS")
    for rva, donnees, nom in (
            (L.R_MSG_BASE, L.MSG_BASE, "MSG_BASE"),
            (L.R_MSG_P1, L.MSG_P1, "MSG_P1"),
            (L.R_MSG_P2, L.MSG_P2, "MSG_P2"),
            (L.R_MSG_VERD, L.MSG_VERD, "MSG_VERD"),
            (L.R_MSG_FIN, L.MSG_FIN, "MSG_FIN"),
            (L.R_MSG_FATAL, L.MSG_FATAL, "MSG_FATAL")):
        poser(seg_r, L.SEG_R_RVA, rva, donnees, nom)
    # — segment RX : les slots des quatre blocs
    for bid, _, _, rva, slot in L.BLOCS_SU:
        poser(seg_rx, L.SEG_RX_RVA, rva, code[bid]["slot"], bid)
    for (d1, f1, n1), (d2, f2, n2) in zip(poses, poses[1:]):
        if d1 < f2 and d2 < f1:
            raise EchecBuild(f"chevauchement : {n1} [{d1:#x},{f1:#x}) / {n2} [{d2:#x},{f2:#x})")

    # — ehdr (ET_DYN, e_entry RELATIF à la base) + 4 phdr par-dessus int3
    e_ident = b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\x00" * 8
    ehdr = struct.pack("<16sHHIQQQIHHHHHH", e_ident,
                       3, 0x3E, 1,                       # ET_DYN (PIE), x86-64, v1
                       L.ENTREE,                         # e_entry = RVA (relatif)
                       64, 0, 0,                         # phoff, shoff, flags
                       64, 56, 4, 0, 0, 0)               # ehsize, phentsize, phnum=4
    ph_r = struct.pack("<IIQQQQQQ", 1, 4,                # LOAD, R (lecture seule)
                       L.SEG_R_RVA, L.SEG_R_RVA, L.SEG_R_RVA,
                       L.SEG_R_TAILLE, L.SEG_R_TAILLE, L.TAILLE_PAGE)
    ph_rx = struct.pack("<IIQQQQQQ", 1, 5,               # LOAD, R+X
                        L.SEG_RX_RVA, L.SEG_RX_RVA, L.SEG_RX_RVA,
                        L.SEG_RX_TAILLE, L.SEG_RX_TAILLE, L.TAILLE_PAGE)
    ph_rw = struct.pack("<IIQQQQQQ", 1, 6,               # LOAD, R+W (.bss pur)
                        L.SEG_RW_RVA, L.SEG_RW_RVA, L.SEG_RW_RVA,
                        0, L.SEG_RW_TAILLE, L.TAILLE_PAGE)
    ph_stack = struct.pack("<IIQQQQQQ", L.PT_GNU_STACK, 6,   # RW SANS X (NX)
                           0, 0, 0, 0, 0, 0x10)
    seg_r[0:64] = ehdr
    seg_r[64:120] = ph_r
    seg_r[120:176] = ph_rx
    seg_r[176:232] = ph_rw
    seg_r[232:288] = ph_stack
    return bytes(seg_r) + bytes(seg_rx)


def valider_elf(img: bytes) -> list[str]:
    """Relit l'image composée : ET_DYN, W^X DEPUIS LES PHDR, GNU_STACK sans X,
    offsets == vaddr, tables conformes au layout (source unique)."""
    lignes = []
    if len(img) != L.TAILLE_FICHIER:
        raise EchecBuild(f"taille {len(img):#x} != {L.TAILLE_FICHIER:#x}")
    if img[:4] != b"\x7fELF" or img[4] != 2 or img[5] != 1:
        raise EchecBuild("magie ELF64 LE absente")
    e_type, e_machine = struct.unpack_from("<HH", img, 16)
    e_entry = struct.unpack_from("<Q", img, 24)[0]
    if e_type != 3:
        raise EchecBuild(f"e_type {e_type} != 3 (ET_DYN exigé — le durcissement)")
    if e_machine != 0x3E:
        raise EchecBuild(f"e_machine {e_machine:#x} != 0x3E")
    if e_entry != L.ENTREE:
        raise EchecBuild(f"e_entry {e_entry:#x} != {L.ENTREE:#x} (RVA, relatif à la base)")
    phoff, phentsize, phnum = struct.unpack_from("<Q", img, 32)[0], \
        struct.unpack_from("<H", img, 54)[0], struct.unpack_from("<H", img, 56)[0]
    if (phoff, phentsize, phnum) != (64, 56, 4):
        raise EchecBuild(f"phdr ({phoff},{phentsize},{phnum}) != (64,56,4)")
    loads = []
    for i in range(phnum):
        # p = (type, flags, offset, vaddr, paddr, filesz, memsz, align)
        p = struct.unpack_from("<IIQQQQQQ", img, phoff + i * 56)
        if p[0] == 1:
            loads.append(p)
        elif p[0] == L.PT_GNU_STACK:
            if p[1] != 6:
                raise EchecBuild(f"PT_GNU_STACK drapeaux {p[1]:#x} != 6 (RW sans X — NX exigé)")
            if p[7] != 0x10:
                raise EchecBuild(f"PT_GNU_STACK align {p[7]:#x} != 0x10")
            lignes.append(f"[phdr] PT_GNU_STACK drapeaux {p[1]} (RW) SANS X — NX explicite, align 0x10")
        else:
            raise EchecBuild(f"p_type inattendu {p[0]:#x}")
    if len(loads) != 3:
        raise EchecBuild(f"{len(loads)} PT_LOAD != 3 (R/RX/RW)")
    if [p[1] for p in loads] != [4, 5, 6]:
        raise EchecBuild(f"drapeaux PT_LOAD {[p[1] for p in loads]} != [4, 5, 6] (R/RX/RW)")
    for p in loads:
        if p[1] & 2 and p[1] & 1:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : inscriptible ET exécutable (W^X rompu)")
        if p[2] != p[3]:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : offset {p[2]:#x} != vaddr {p[3]:#x}")
        if p[7] != L.TAILLE_PAGE:
            raise EchecBuild(f"PT_LOAD {p[1]:#x} : align {p[7]:#x} != {L.TAILLE_PAGE:#x}")
    # (vaddr, filesz, memsz) attendus par segment — le plan d'adressage
    attendus = {4: (L.SEG_R_RVA, L.SEG_R_TAILLE, L.SEG_R_TAILLE),
                5: (L.SEG_RX_RVA, L.SEG_RX_TAILLE, L.SEG_RX_TAILLE),
                6: (L.SEG_RW_RVA, 0, L.SEG_RW_TAILLE)}
    for p in loads:
        vaddr, filesz, memsz = attendus[p[1]]
        if (p[3], p[5], p[6]) != (vaddr, filesz, memsz):
            raise EchecBuild(
                f"PT_LOAD {p[1]:#x} : vaddr/filesz/memsz "
                f"{(p[3], p[5], p[6])} != {(vaddr, filesz, memsz)} (layout)")
    lignes.append("[phdr] 3 PT_LOAD R/RX/RW + PT_GNU_STACK RW sans X — "
                  "W^X CONSTATÉ depuis les phdr (aucun segment inscriptible exécutable)")
    lignes.append(f"[phdr] ET_DYN (PIE) : e_entry {e_entry:#x} RELATIF à la base, "
                  "3 segments identité offset==vaddr, RW .bss pur (filesz 0)")
    # Tables de données : empreintes conformes au layout (source unique)
    if img[L.R_ERRNOS:L.R_ERRNOS + len(octets_errnos())] != octets_errnos():
        raise EchecBuild("table ERRNOS divergente du layout (source unique)")
    if img[L.R_HEXCHARS:L.R_HEXCHARS + 16] != L.HEXCHARS:
        raise EchecBuild("HEXCHARS divergents")
    for rva, attendu in ((L.R_MSG_BASE, L.MSG_BASE), (L.R_MSG_P1, L.MSG_P1),
                         (L.R_MSG_P2, L.MSG_P2), (L.R_MSG_VERD, L.MSG_VERD),
                         (L.R_MSG_FIN, L.MSG_FIN), (L.R_MSG_FATAL, L.MSG_FATAL)):
        if img[rva:rva + len(attendu)] != attendu:
            raise EchecBuild(f"message @ {rva:#x} divergent")
    return lignes


# --- Oracle natif : exécution réelle, la base est choisie par le NOYAU ------------

class Terrain:
    """Exécution native de la sonde — le labo EST Linux x86-64 (fiche § 10)."""

    def __init__(self, img: bytes):
        parent = os.path.join(ICI, ".tmp")
        os.makedirs(parent, exist_ok=True)
        self.dossier = tempfile.mkdtemp(prefix="sonde-", dir=parent)
        self.chemin = os.path.join(self.dossier, "sonde")
        with open(self.chemin, "wb") as f:
            f.write(img)
        os.chmod(self.chemin, 0o755)

    def lancer(self, setarch_r: bool = False) -> tuple[bytes, bytes, int]:
        cmd = [self.chemin]
        if setarch_r:
            cmd = ["setarch", "-R", self.chemin]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=30)
            return r.stdout, r.stderr, r.returncode
        except subprocess.TimeoutExpired:
            return b"", b"<timeout>", -99

    def nettoyer(self):
        import shutil
        shutil.rmtree(self.dossier, ignore_errors=True)


_RE_BASE = re.compile(rb"^sonde : base 0x([0-9a-f]{16})\n$")
LIGNE_S1 = (L.MSG_P1 + b"fffffffffffffff7" + L.MSG_VERD
            + b"0000000000000001" + L.MSG_FIN)
LIGNE_S2 = (L.MSG_P2 + b"fffffffffffffff2" + L.MSG_VERD
            + b"0000000000000006" + L.MSG_FIN)


def _sortie_conforme(sortie: bytes) -> tuple[bool, int | None]:
    """4 lignes : base (variable), les deux sondes et la fatale (exactes)."""
    lignes = sortie.split(b"\n")
    if len(lignes) != 5 or lignes[4] != b"":
        return False, None
    m = _RE_BASE.match(lignes[0] + b"\n")
    if not m:
        return False, None
    if lignes[1] + b"\n" != LIGNE_S1 or lignes[2] + b"\n" != LIGNE_S2:
        return False, None
    if lignes[3] + b"\n" != L.MSG_FATAL:
        return False, None
    return True, int(m.group(1), 16)


def oracle_natif(img: bytes, longueurs: dict[str, int] | None = None) -> dict:
    t = Terrain(img)
    try:
        # — 6 exécutions nominales : 4 lignes conformes + code 6 (le verdict
        # fatal d'EFAULT est terminal PAR CONTRAT : la démonstration complète
        # des deux branches de la table ERRNOS)
        bases: list[int] = []
        for _ in range(6):
            sortie, err, code = t.lancer()
            ok, base = _sortie_conforme(sortie)
            if code != 6 or err or not ok:
                raise EchecBuild(
                    f"oracle natif : code={code} base={base!r} sortie={sortie!r} err={err!r}")
            bases.append(base)
        # — la base : page-alignée, plausible, ALÉATOIRE (>= 2 distinctes sur
        # 6 exécutions — l'ASLR du noyau CONSTATÉ, jamais décrété)
        for b in bases:
            if b % L.TAILLE_PAGE != 0:
                raise EchecBuild(f"base {b:#x} non alignée à la page — le noyau ne l'a pas choisie")
            if b < 0x10000:
                raise EchecBuild(f"base {b:#x} < 0x10000 — implausible")
        distinctes = len(set(bases))
        if distinctes < 2:
            raise EchecBuild(
                f"base CONSTANTe {bases[0]:#x} sur 6 exécutions — l'image PIE n'est "
                f"pas chargée à une base aléatoire (ASLR noyau exigé, fiche § 3)")
        note_setarch = "base fixe recoupée (setarch -R)"
        bases_fixes: list[int] = []
        for _ in range(2):
            sortie, err, code = t.lancer(setarch_r=True)
            ok, base = _sortie_conforme(sortie)
            if code != 6 or err or not ok:
                raise EchecBuild(f"setarch -R : code={code} sortie={sortie!r} err={err!r}")
            bases_fixes.append(base)
        if bases_fixes[0] != bases_fixes[1]:
            raise EchecBuild(
                f"setarch -R : bases distinctes {bases_fixes[0]:#x}/{bases_fixes[1]:#x} "
                f"— ADDR_NO_RANDOMIZE ne fixe pas la base ?")
        if bases_fixes[0] in bases:
            note_setarch += f" — la base fixe {bases_fixes[0]:#x} fut aussi tirée sous ASLR"

        # — falsification : un octet de CODE corrompu par bloc, batterie
        # complète — au MOINS une divergence par mutant, zéro silence
        detectees = 0
        for bid, _, _, rva, _ in L.BLOCS_SU:
            longueur = (longueurs or {}).get(bid, 32)
            for offset in (0, 5, 10):
                if offset >= longueur:
                    continue
                mutant = bytearray(img)
                mutant[rva + offset] ^= 0xFF
                tm = Terrain(bytes(mutant))
                try:
                    sortie, err, code = tm.lancer()
                    ok, _ = _sortie_conforme(sortie)
                    if ok and code == 6 and not err:
                        raise EchecBuild(
                            f"falsification : {bid} +{offset} NON détectée (silence)")
                    detectees += 1
                finally:
                    tm.nettoyer()
        return {"cas": 6, "bases": bases, "bases_distinctes": distinctes,
                "bases_fixes": bases_fixes, "setarch": note_setarch,
                "falsification": detectees}
    finally:
        t.nettoyer()


# --- Carte génération 1 de la lignée du jalon ------------------------------------

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fragments_clairs(code: dict, img: bytes, verrous: list, specs: dict,
                     verdict: dict, compteurs: dict, journal: list) -> dict:
    loc = ["[carte-frag] nom=frag-loc generation=1"]
    for bid, sid, fichier, rva, slot in L.BLOCS_SU:
        loc.append(f"[bloc] id={bid} spec={sid} cible={L.PROFIL} "
                   f"addr={rva:#x} size={slot} v=1 etat=scelle "
                   f"(RVA — PIE : la base est choisie par le noyau)")
    con = ["[carte-frag] nom=frag-con generation=1"]
    for bid in code:
        spec = specs[bid]["texte"]
        sig = re.search(r"Intention : (.+?)\n", spec).group(1)
        con.append(f"[bloc] id={bid}\n  sig : {sig[:100]}")
    prf = ["[carte-frag] nom=frag-prf generation=1"]
    for bid, _, fichier, _, _ in L.BLOCS_SU:
        with open(os.path.join(ICI, "notation", fichier + ".asm"), "rb") as f:
            emp = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} "
                f"crist={crist}/10",
                f"  vecteurs : roundtrip=ok structure=ok notation={emp}",
                f"  differentiel : natif ok (PIE/ASLR/ERRNOS, falsification "
                f"{verdict['falsification']})"]
    prf.append("[verifications] runs=" + str(len(journal)))
    prf += ["  " + r for r in journal[-12:]]
    bld = ["[carte-frag] nom=frag-bld generation=1"]
    for bid, _, fichier, rva, slot in L.BLOCS_SU:
        bld.append(f"[bloc] id={bid} addr={rva:#x} "
                   f"empreinte={sha(code[bid]['slot'])}")
    bld += [
        f"[build] artefact=sonde version={L.VERSION_DEV1} profil={L.PROFIL} "
        f"taille={len(img)} empreinte={sha(img)}",
        f"  outils : keystone + capstone {capstone.cs_version()[0]}."
        f"{capstone.cs_version()[1]} ; verrous={len(verrous)} ; symboles vérifiés",
        f"  durcissement : ET_DYN/PIE (base aléatoire noyau), 3 segments R/RX/RW, "
        f"PT_GNU_STACK sans X, W^X depuis les phdr ; ERRNOS {len(L.ERRNOS)} entrée(s)",
        f"  oracle : natif — {verdict['bases_distinctes']} bases distinctes sur 6 runs "
        f"(ASLR constaté), setarch -R {verdict['setarch']}",
        f"[zones] sys=0x1000-0x1040 hex=0x1040-0x10c0 verdict=0x10c0-0x1140 "
        f"app=0x1140-0x13c0 rodata=0x140-0x284 bss=0x2000-0x2040",
    ]
    return {n: ("\n".join(l) + "\n").encode("utf-8")
            for n, l in (("frag-loc", loc), ("frag-con", con),
                         ("frag-prf", prf), ("frag-bld", bld))}


def verrou_croise(code: dict, img: bytes) -> int:
    """R8 : signature + empreintes re-vérifiées depuis le disque."""
    entete, fragments, signature, pub = cm.lire_carte()
    cm.verifier_signature(pub, entete, fragments, signature)
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode()
    n = 0
    for bid, _, fichier, rva, slot in L.BLOCS_SU:
        m = re.search(rf"\[bloc\] id={bid} addr=\S+ empreinte=(\S+)", bld)
        if not m or m.group(1) != sha(img[rva:rva + slot]):
            raise EchecBuild(f"verrou croisé : {bid} divergent (R8)")
        n += 1
    return n


def construire_carte(code: dict, img: bytes, verrous: list, specs: dict,
                     verdict: dict, compteurs: dict, journal: list):
    clairs = fragments_clairs(code, img, verrous, specs, verdict, compteurs, journal)
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    prive, pub = cm.paire_cles(graine)
    entete = cm.construire_entete(empreinte_racine(fragments))
    signature = cm.signer(prive, entete, fragments)
    cm.ecrire_carte(entete, fragments, signature, pub)


def tableau_de_bord(img: bytes, verrous: list, specs: dict, verdict: dict,
                    phdr_lignes: list[str]) -> str:
    return "\n".join([
        "[tableau] jalon=M6-(a) artefact=sonde version=" + L.VERSION_DEV1,
        "  profil                       : " + L.PROFIL + " (fiche § 3 — le durcissement)",
        "  blocs_avec_spec_a_jour        : 4/4 : audit I->C->B (specs, carte, artefact)",
        "  chaines_I_C_B_tests           : 4/4 : " + str(len(verrous)) + " verrous PASS",
        "  construction                 : 0 erreur / 0 avertissement : build script",
        "  format_durci                 : ET_DYN (PIE), 3 segments R/RX/RW, "
        "PT_GNU_STACK RW sans X, W^X constaté depuis les phdr, "
        "offsets==vaddr, RW .bss pur (filesz 0)",
        "  contrat_erreurs               : table ERRNOS " + str(len(L.ERRNOS))
        + " entrée(s) (EBADF nommé, " + str(len(L.ERRNOS))
        + " motivée par su-04:E1) ; VERDICT_FATAL=" + str(L.VERDICT_FATAL)
        + " (fail-closed) ; exercée en exécution sur les DEUX branches",
        "  tests_differentiels           : oracle natif 6/6 runs conformes "
        "(4 lignes octet pour octet, code 6) ; falsification "
        + str(verdict["falsification"]) + " mutations attrapées (zéro silence)",
        "  pie_aslr                      : " + str(verdict["bases_distinctes"])
        + " bases distinctes sur 6 exécutions (alignées 0x1000, >= 0x10000) ; "
        + verdict["setarch"],
        "  reutilisation_heritage        : 0 bloc réutilisé (lignée neuve — la "
        "parité du patrimoine est le chantier (b), la sonde démontre le FORMAT)",
        "  defauts_ouverts               : 0",
        "  preversions                   : " + L.VERSION_DEV1
        + " conforme (R10 : monotonie, plancher " + hex(L.VERSION_U64_MIN) + ")",
        "  artefact                      : " + str(len(img)) + " octets ; "
        "empreinte sha256:" + sha(img)[:24] + "…",
        "  verrou_croise                 : 4 empreintes + signature Ed25519 (R8)",
    ]) + "\n" + "\n".join("  " + l for l in phdr_lignes) + "\n"


# --- Construction -----------------------------------------------------------------

def construire() -> int:
    print("=== M6-(a) : lignée du jalon (unix/, D149) — sonde, durcissement format ===")
    t0 = time.perf_counter()
    specs = charger_couche_I()
    print(f"[I] 4 specs chargées et auditées (gabarit § 2.2, R2)")

    blocs, _, code, _ = assembler_tout()
    total_insns = sum(len(code[b[0]]["insns"]) for b in blocs)
    total_code = sum(len(code[b[0]]["octets"]) for b in blocs)
    print(f"[R5] 4 blocs, {total_insns} instructions, {total_code} o de code — "
          f"round-trip keystone/capstone 100 %")

    verrous = oracle_structurel(code, specs)
    n_symboles = verifier_symboles()
    print(f"[oracle] structurel : {len(verrous)} verrous PASS ; "
          f"{n_symboles} symboles @ vérifiés contre layout/réel (leçon C1)")

    img = composer_elf(code)
    phdr_lignes = valider_elf(img)
    for l in phdr_lignes:
        print(l)
    print(f"[ELF] sonde : {len(img)} o (ET_DYN, ehdr + 4 phdr à la main, "
          f"R 0x1000 + RX 0x1000 + RW .bss 0x1000), entrée {L.ENTREE:#x} (RVA)")

    verdict = oracle_natif(img, {bid: len(code[bid]["octets"]) for bid, _, _, _, _ in blocs})
    bases_court = ", ".join(f"{b:#x}" for b in verdict["bases"][:3])
    print(f"[oracle] natif : 6/6 runs conformes, code 6 ; PIE/ASLR : "
          f"{verdict['bases_distinctes']} bases distinctes ({bases_court} …) ; "
          f"{verdict['setarch']}")
    print(f"[oracle] ERRNOS exercée : EBADF nommé (verdict 1) ET EFAULT hors table "
          f"(VERDICT_FATAL 6, arrêt propre) ; falsification "
          f"{verdict['falsification']} détectées (zéro silence)")

    chemin_art = os.path.join(ICI, "sonde")
    with open(chemin_art, "wb") as f:
        f.write(img)
    os.chmod(chemin_art, 0o755)

    journal = [f"run natif date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
               f"build={L.VERSION_DEV1} bases={verdict['bases_distinctes']}/6 "
               f"falsif={verdict['falsification']}"]
    compteurs = {bid: 1 for bid, _, _, _, _ in blocs}
    construire_carte(code, img, verrous, specs, verdict, compteurs, journal)
    nb = verrou_croise(code, img)
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w",
              encoding="utf-8") as f:
        f.write(tableau_de_bord(img, verrous, specs, verdict, phdr_lignes))
    print(f"[carte] génération 1 du jalon écrite : 4 fragments chiffrés "
          f"(sel distinct — 3e sel), signature Ed25519 (clés projet D27), "
          f"verrou croisé {nb}/4, tableau de bord")

    print(f"[B] sonde scellée : sha256:{sha(img)}")
    print(f"=== M6-(a) dev (oracles verts) : {L.VERSION_DEV1} — "
          f"{round(time.perf_counter() - t0, 1)} s ===")
    return 0


def verifier() -> int:
    print("=== M6-(a) : re-vérification complète (R5/R8) ===")
    with open(os.path.join(ICI, "sonde"), "rb") as f:
        img = f.read()
    blocs, _, code, _ = assembler_tout()
    for bid, _, fichier, rva, slot in blocs:
        if img[rva:rva + slot] != code[bid]["slot"]:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5)")
    specs = charger_couche_I()
    oracle_structurel(code, specs)
    valider_elf(img)
    verdict = oracle_natif(img, {bid: len(code[bid]["octets"]) for bid, _, _, _, _ in blocs})
    print(f"[oracle] natif : 6/6 runs conformes ; falsification "
          f"{verdict['falsification']} détectées")
    # Cristallisation : compteurs incrémentés dans frag-prf
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode()
    compteurs = {}
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            compteurs[champs["id"]] = int(
                re.match(r"(\d+)/10", champs.get("crist", "1/10")).group(1))
    for bid, _, _, _, _ in blocs:
        compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal = [l.strip() for l in prf.splitlines() if l.startswith("  run ")]
    journal.append(f"run natif date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
                   f"verif bases={verdict['bases_distinctes']}/6 falsif={verdict['falsification']}")
    construire_carte(code, img, [], specs, verdict, compteurs, journal)
    nb = verrou_croise(code, img)
    crist = ", ".join(f"{b}={compteurs.get(b, 0)}/10" for b, _, _, _, _ in blocs)
    print(f"[R6] cristallisation : {crist}")
    print(f"[R8] verrou croisé : {nb}/4 empreintes conformes")
    return 0


if __name__ == "__main__":
    sys.exit(verifier() if "--verifier" in sys.argv else construire())
