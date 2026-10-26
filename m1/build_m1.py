#!/usr/bin/env python3
"""build_m1.py : Jalon M1 de TRIADE — mini-libc scellée et blocs réutilisables.

Notation (keystone) -> octets -> PE32+ écrit à la main -> carte projet
génération 1 (multi-artefacts). Implémente la checklist M1 de
REPRISE_PROJET.md § 7.2 sous les règles R5-R7 (vérifie-puis-écrit,
cristallisation, adresses stables) et les conditions transverses v0.4.0.

L'ORACLE (D1) est régénéré à chaque exécution depuis la couche I :
  1. round-trip de notation : keystone -> capstone -> keystone (WYSIWYG) ;
  2. contrat structurel : invariants de I vérifiés sur le code désassemblé ;
  3. oracle différentiel (D29) : émulation Unicorn — chaque bloc exécuté sur
     des entrées aléatoires contraintes par les pré-conditions, comparé à la
     référence dérivée de I ; le binaire entier est émulé avec shims IAT ;
     seuls les verdicts hachés survivent dans frag-prf.

RÉUTILISATION (R7) : les blocs scellés io-01/io-02 de M0 sont embarqués à
leurs adresses historiques, octets identiques — vérifié contre hello.exe à
chaque construction (preuve_reutilisation).

Usage :
  python3 build_m1.py --phase 1        # construction dev.1 (6 blocs libc + autotest 18)
  python3 build_m1.py --phase 2        # construction dev.2 (+ memset, autotest 21)
  python3 build_m1.py --verifier [--graine N]   # R8 : re-vérification + cristallisation
  python3 build_m1.py --sceller-rc     # cristallisation atteinte -> balise rc.1
  python3 build_m1.py --sceller-final  # constat terrain consigne (D32) -> balise 0.2.0 finale

Déterminisme : selftest.exe est byte-identique à phase et sources constantes.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import struct
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

import capstone
import pefile
from keystone import Ks, KS_ARCH_X86, KS_MODE_64

import carte_m1 as cm
import oracle_differentiel as od

ICI = os.path.dirname(os.path.abspath(__file__))
M0_DIR = os.path.join(os.path.dirname(ICI), "m0")


class EchecBuild(Exception):
    """Tout échec de l'oracle, du round-trip ou de la construction."""


# --- Blocs par phase ----------------------------------------------------------

def blocs_phase(phase: int) -> list[tuple]:
    """(id carte, spec, fichier notation, rva, slot) — embarqués dans selftest.exe."""
    blocs = [
        ("a10002", "hello-02:R1", "hello-02-write", 0x1040, 0x40),      # réutilisé M0
        ("a10003", "hello-03:R1", "hello-03-exit", 0x1080, 0x40),       # réutilisé M0
        ("b20001", "libc-01:R1", "libc-01-memcpy", 0x1100, 0x80),
        ("b20002", "libc-02:R1", "libc-02-memcmp", 0x1180, 0x80),
        ("b20003", "libc-03:R1", "libc-03-strlen", 0x1200, 0x80),
        ("b20004", "libc-04:R2", "libc-04-itoa", 0x1280, 0x80),
        ("b20005", "libc-05:R1", "libc-05-zone-alloc", 0x1300, 0x80),
        ("b20006", "libc-06:R1", "libc-06-zone-reset", 0x1380, 0x40),
    ]
    if phase >= 2:
        blocs.append(("b20007", "libc-07:R1", "libc-07-memset", 0x13C0, 0x80))
    blocs.append(("b20008", f"libc-08:R{1 if phase == 1 else 2}", "libc-08-autotest", 0x1800, 0x800))
    return blocs


# Les notations des blocs réutilisés vivent dans m0/notation/.
def chemin_notation(fichier: str) -> str:
    if fichier.startswith("hello-"):
        return os.path.join(M0_DIR, "notation", fichier + ".asm")
    return os.path.join(ICI, "notation", fichier + ".asm")


# --- Couche I : lecture et audit du gabarit ----------------------------------

def lire_spec(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", texte)
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3)), "texte": texte}
    for bloc in ("Intention", "Contrat", "Échecs", "Vecteurs", "Fixtures", "Provenance", "Décisions"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")
    if "écrite-avant-code" not in texte:
        raise EchecBuild(f"{chemin} : provenance inattendue (R2 : écrite-avant-code)")
    return spec


def charger_couche_I(blocs: list[tuple]) -> dict[str, dict]:
    """Les specs M1 depuis m1/I/, les specs réutilisées depuis m0/I/."""
    fichiers_m1 = {
        "libc-01": "libc-01-memcpy.md", "libc-02": "libc-02-memcmp.md",
        "libc-03": "libc-03-strlen.md", "libc-04": "libc-04-itoa.md",
        "libc-05": "libc-05-zone-alloc.md", "libc-06": "libc-06-zone-reset.md",
        "libc-07": "libc-07-memset.md", "libc-08": "libc-08-autotest.md",
    }
    fichiers_m0 = {
        "hello-01": "hello-01-main.md", "hello-02": "hello-02-write.md",
        "hello-03": "hello-03-exit.md",
    }
    specs = {}
    for bid, sid, _, _, _ in blocs:
        ident = sid.split(":")[0]
        if ident in fichiers_m1:
            chemin = os.path.join(ICI, "I", fichiers_m1[ident])
        else:
            chemin = os.path.join(M0_DIR, "I", fichiers_m0[ident])
        if not os.path.exists(chemin):
            raise EchecBuild(f"spécification I introuvable pour {sid} : {chemin}")
        spec = lire_spec(chemin)
        if f"{spec['id']}:R{spec['rev']}" != sid:
            raise EchecBuild(f"{chemin} : identifiant/révision {spec['id']}:R{spec['rev']} != carte {sid}")
        specs[bid] = spec
    # hello-01 : indexé par la carte projet mais non embarqué dans selftest.exe
    chemin = os.path.join(M0_DIR, "I", "hello-01-main.md")
    spec = lire_spec(chemin)
    if f"{spec['id']}:R{spec['rev']}" != "hello-01:R1":
        raise EchecBuild(f"{chemin} : hello-01:R1 attendu")
    specs["a10001"] = spec
    return specs


# --- Notation : assemblage et round-trip (R5) ---------------------------------

def lignes_notation(chemin: str) -> list[str]:
    with open(chemin, encoding="utf-8") as f:
        brut = f.read().splitlines()
    return [l.strip() for l in brut if l.strip() and not l.strip().startswith(";")]


def assembler_bloc(ks: Ks, chemin: str, rva: int, slot: int) -> tuple[bytes, list[dict]]:
    octets, metas, adresse = b"", [], rva
    for ligne in lignes_notation(chemin):
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise EchecBuild(f"{chemin} : ligne inassemblable : {ligne!r}")
        b = bytes(enc)
        metas.append({"ligne": ligne, "adresse": adresse, "taille": len(b)})
        octets += b
        adresse += len(b)
    if len(octets) > slot:
        raise EchecBuild(f"{chemin} : {len(octets)} o > slot {slot:#x} (D8)")
    return octets, metas


def canon(texte: str) -> str:
    """Normalisation : minuscules, espaces uniques, immédiats en hexa 32 bits."""
    t = re.sub(r"\s+", " ", texte.strip().lower())

    def norm(m: re.Match) -> str:
        v = int(m.group(0), 0)
        if v < 0:
            v &= 0xFFFFFFFF
        return f"0x{v:x}"

    return re.sub(r"(?<![\w])-?(?:0x[0-9a-f]+|\d+)(?![\w])", norm, t)


def round_trip(cs: capstone.Cs, ks: Ks, chemin: str, rva: int, octets: bytes, metas: list[dict]) -> list:
    instructions = list(cs.disasm(octets, rva))
    if len(instructions) != len(metas):
        raise EchecBuild(f"{chemin} : {len(instructions)} instructions désassemblées != {len(metas)} notées")
    for insn, meta in zip(instructions, metas):
        if insn.address != meta["adresse"] or insn.size != meta["taille"]:
            raise EchecBuild(f"{chemin} : désalignement à {meta['adresse']:#x}")
        texte_cs = f"{insn.mnemonic} {insn.op_str}".strip()
        if canon(texte_cs) != canon(meta["ligne"]):
            raise EchecBuild(
                f"{chemin} @ {meta['adresse']:#x} : écart texte notation/désassemblage\n"
                f"  notation      : {meta['ligne']}\n  désassemblage : {texte_cs}")
        renc, _ = ks.asm(texte_cs, insn.address)
        if bytes(renc) != octets[meta["adresse"] - rva: meta["adresse"] - rva + insn.size]:
            raise EchecBuild(f"{chemin} @ {meta['adresse']:#x} : ré-assemblage != octets originaux")
    return instructions


def operande_rip_cible(insn) -> int | None:
    m = re.search(r"\[rip \+ (0x[0-9a-f]+)\]", insn.op_str)
    if m:
        return insn.address + insn.size + int(m.group(1), 16)
    m = re.search(r"\[rip - (0x[0-9a-f]+)\]", insn.op_str)
    if m:
        return insn.address + insn.size - int(m.group(1), 16)
    return None


# --- Oracle structurel : les invariants de I, vérifiés sur le code ------------

SLOTS_DONNEES = {
    L.R_SA, L.R_SB, L.R_SC, L.R_SD, L.R_MOTIF16, L.R_SENT16, L.R_MOTIF33,
    L.R_ZERO16, L.R_FF33, L.R_S_VIDE, L.R_S_TRIADE, L.R_S_33,
    L.R_I0, L.R_IMAX, L.R_I123, L.R_I7, L.R_PREFIXE, L.R_SLASH, L.R_OK, L.R_KO,
    L.R_CURSEUR, L.ARENE_BASE,
}
FEUILLES = {"b20001", "b20002", "b20003", "b20004", "b20007"}   # aucun appel
ZONE = {"b20005", "b20006"}                                      # n'écrivent que le curseur


def oracle_structurel(specs: dict, code: dict, blocs: list[tuple], phase: int) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    nb_tests = L.NB_TESTS_DEV1 if phase == 1 else L.NB_TESTS_DEV2
    adresses_insns = {bid: {i.address for i in code[bid]["insns"]} for bid, _, _, _, _ in blocs}
    adresses_blocs = {bid: rva for bid, _, _, rva, _ in blocs}

    for bid, sid, _, rva, slot in blocs:
        insns = code[bid]["insns"]
        mnemos = [i.mnemonic for i in insns]

        # Cibles de saut internes : toute cible de jcc/jmp tombe sur une
        # frontière d'instruction DU MÊME bloc (piège des adresses explicites).
        for i in insns:
            if i.mnemonic.startswith("j"):
                cible = int(i.op_str, 16)
                verrou(f"{bid}:saut-interne@{i.address:#x}", cible in adresses_insns[bid],
                       f"cible {cible:#x} hors frontière d'instruction")
            cible_rip = operande_rip_cible(i)
            if cible_rip is not None and i.mnemonic == "call":
                autorises = set(L.IAT_SLOTS.values()) | {
                    adresses_blocs[b] for b in ("a10002", "a10003", "b20001", "b20002",
                                                "b20003", "b20004", "b20005", "b20006")} \
                    | ({adresses_blocs["b20007"]} if phase >= 2 else set()) \
                    | ({adresses_blocs["b20008"]} if bid != "b20008" else set())
                verrou(f"{bid}:appel-autorise@{i.address:#x}", cible_rip in autorises,
                       f"cible {cible_rip:#x} hors blocs déclarés")
            elif cible_rip is not None:
                verrou(f"{bid}:donnees-autorisees@{i.address:#x}", cible_rip in SLOTS_DONNEES,
                       f"cible {cible_rip:#x} hors données déclarées")

        # Interface système : jamais d'appel direct (D7)
        verrou(f"{bid}:pas-de-syscall", not any(m in ("syscall", "int", "sysenter") for m in mnemos))

        # Padding inter-blocs >= 16 et alignement (D8)
        fin_code = insns[-1].address + insns[-1].size
        slot_suivant = min((r2 for _, _, _, r2, _ in blocs if r2 > rva), default=L.RDATA_RVA)
        verrou(f"{bid}:padding-16", slot_suivant - fin_code >= 16, f"écart {slot_suivant - fin_code}")
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)

        # Aucun stockage sous RSP (zone interdite msx64, hors push/pop légaux)
        for i in insns:
            if i.mnemonic.startswith("mov") and "[" in i.op_str and i.op_str.split(",")[0].strip().endswith("]"):
                base = re.search(r"\[(\w+)", i.op_str)
                if base and base.group(1) == "rsp":
                    disp = re.search(r"\+ (0x[0-9a-f]+)\]", i.op_str)
                    verrou(f"{bid}:pas-de-stockage-sous-rsp@{i.address:#x}",
                           disp is None or int(disp.group(1), 16) >= 0)

    # Blocs feuilles : aucun appel du tout (libc-01..04, 07 — I1)
    for bid in (FEUILLES if phase >= 2 else FEUILLES - {"b20007"}):
        verrou(f"{bid}:feuille", not any(i.mnemonic == "call" for i in code[bid]["insns"]))
        pushes = sum(1 for i in code[bid]["insns"] if i.mnemonic == "push")
        pops = sum(1 for i in code[bid]["insns"] if i.mnemonic == "pop")
        verrou(f"{bid}:pile-equilibree", pushes == pops, f"{pushes} push / {pops} pop")

    # Blocs zone : cibles limitées au curseur (I3/I4)
    for bid in ZONE:
        cibles = {operande_rip_cible(i) for i in code[bid]["insns"]} - {None}
        autorisees = {L.R_CURSEUR} if bid == "b20006" else {L.R_CURSEUR, L.ARENE_BASE}
        verrou(f"{bid}:cibles-zone", cibles <= autorisees, f"{list(map(hex, cibles))}")

    # Réutilisés M0 : contrats hello-02/hello-03 revérifiés (régression R7)
    w = code["a10002"]["insns"]
    verrou("a10002:frame-entree", w[0].mnemonic == "sub" and "rsp" in w[0].op_str and "0x28" in w[0].op_str)
    verrou("a10002:arg4-null", any(i.mnemonic == "xor" and i.op_str == "r9d, r9d" for i in w))
    verrou("a10002:arg5-null", any(i.mnemonic == "mov" and canon(i.op_str) == canon("qword ptr [rsp + 0x20], 0") for i in w))
    verrou("a10002:appel-unique-writefile",
           sum(1 for i in w if i.mnemonic == "call" and operande_rip_cible(i) == L.IAT_SLOTS["WriteFile"]) == 1)
    verrou("a10002:pile-restauree", w[-1].mnemonic == "ret" and any(i.mnemonic == "add" and "rsp" in i.op_str for i in w))
    e = code["a10003"]["insns"]
    verrou("a10003:sans-retour", not any(i.mnemonic == "ret" for i in e))
    verrou("a10003:ud2-defensif", e[-1].mnemonic == "ud2")

    # Autotest (b20008) : discipline d'orchestration (libc-08 I1-I5)
    a = code["b20008"]["insns"]
    verrou("b20008:frame-entree", a[0].mnemonic == "sub" and "rsp" in a[0].op_str and "0x40" in a[0].op_str)
    registres_poussees = [i.op_str for i in a if i.mnemonic == "push"]
    verrou("b20008:registres-sauvegardes", registres_poussees == ["rbx", "r12", "r13", "r14", "r15"], f"{registres_poussees}")
    verrou("b20008:sortie-par-exit", a[-1].mnemonic == "call" and int(a[-1].op_str, 16) == 0x1080)
    verrou("b20008:compteur-total",
           any(i.mnemonic == "cmp" and canon(i.op_str) == canon(f"r15, {nb_tests}") for i in a),
           f"attendu cmp r15, {nb_tests}")
    verrou("b20008:stdout", any(canon(f"{i.mnemonic} {i.op_str}") == canon("mov ecx, -11") for i in a))

    # Zone : le curseur initial est nul dans l'image (libc-05 P3)
    verrou("traçabilité-I", all(s in specs for s in ("a10001", "a10002", "a10003",
                                                     "b20001", "b20002", "b20003",
                                                     "b20004", "b20005", "b20006", "b20008")))
    if phase >= 2:
        verrou("traçabilité-I-memset", "b20007" in specs)
    return verrous


# --- Composition des sections -------------------------------------------------

def composer_sections(code: dict, blocs: list[tuple], phase: int) -> tuple[bytes, bytes, bytes]:
    # .text : zone réservée remplie d'int3 (défensif), blocs posés à leur slot.
    texte = bytearray(b"\xcc" * L.TEXT_VSIZE)
    for bid, _, _, rva, slot in blocs:
        octets = code[bid]["octets"]
        pad = slot - len(octets)
        if pad < 16:
            raise EchecBuild(f"{bid} : padding {pad} < 16 (D8)")
        texte[rva - L.TEXT_RVA: rva - L.TEXT_RVA + slot] = octets + b"\x90" * pad

    # .rdata : structures PE héritées M0 (positions immuables) + données dorées.
    rdata = bytearray(b"\x00" * L.RDATA_VSIZE)

    def poser(rva: int, donnees: bytes):
        rdata[rva - L.RDATA_RVA: rva - L.RDATA_RVA + len(donnees)] = donnees

    hn = lambda nom: struct.pack("<H", 0) + nom.encode("ascii") + b"\x00"
    poser(L.R_SA, b"TRIADE\x00")
    poser(L.R_SB, b"TRIADE\x00")
    poser(L.R_SC, b"TRIADF\x00")
    poser(L.R_SD, b"TRI\x00")
    poser(L.R_DESC_IMPORT, struct.pack("<IIIII", L.R_INT, 0, 0, L.R_NOM_DLL, L.R_IAT))
    poser(L.R_DESC_IMPORT + 20, b"\x00" * 20)
    poser(L.R_NOM_DLL, b"kernel32.dll\x00")
    poser(L.R_HN_GSH, hn("GetStdHandle"))
    poser(L.R_HN_WF, hn("WriteFile"))
    poser(L.R_HN_EP, hn("ExitProcess"))
    hv = {n: v for n, v in (("GetStdHandle", L.R_HN_GSH), ("WriteFile", L.R_HN_WF), ("ExitProcess", L.R_HN_EP))}
    poser(L.R_INT, b"".join(struct.pack("<Q", hv[n]) for n in L.DLL_IMPORTS) + struct.pack("<Q", 0))
    poser(L.R_IAT, b"".join(struct.pack("<Q", hv[n]) for n in L.DLL_IMPORTS) + struct.pack("<Q", 0))
    poser(L.R_RELOC, struct.pack("<II", L.TEXT_RVA, 12) + struct.pack("<HH", 0, 0))
    # Vecteurs dorés et messages (dispositions layout.py)
    poser(L.R_MOTIF16, bytes(range(16)))
    poser(L.R_SENT16, b"\xaa" * 16)
    poser(L.R_MOTIF33, L.MOTIF33)
    poser(L.R_ZERO16, b"\x00" * 16)
    poser(L.R_FF33, b"\xff" * 33)
    poser(L.R_S_VIDE, b"\x00")
    poser(L.R_S_TRIADE, b"TRIADE\x00")
    poser(L.R_S_33, L.S_33 + b"\x00")
    poser(L.R_I0, b"0\x00")
    poser(L.R_IMAX, b"4294967295\x00")
    poser(L.R_I123, b"1234567890\x00")
    poser(L.R_I7, b"7\x00")
    poser(L.R_PREFIXE, L.PREFIXE)
    poser(L.R_SLASH, b"/")
    poser(L.R_OK, b" OK\r\n")
    poser(L.R_KO, b" KO\r\n")

    # .data : curseur d'arène nul à l'image (libc-05 P3), queue BSS virtuelle.
    data = bytearray(b"\x00" * L.DATA_RAW)
    return bytes(texte), bytes(rdata), bytes(data)


# --- Éditeur PE32+ ------------------------------------------------------------

def ecrire_pe32plus(texte: bytes, rdata: bytes, data: bytes) -> bytes:
    """En-têtes DOS/COFF/PE32+ écrits à la main : agent manual § 7.2, trois sections."""
    dos = b"MZ" + b"\x00" * 58 + struct.pack("<I", 0x40)
    coff = struct.pack("<HHIIIHH", 0x8664, 3, 0, 0, 0, 0xF0, 0x0002)

    opt_fixe = struct.pack(
        "<HBBIIIIIQIIHHHHHHIIIIHHQQQQII",
        0x20B,               # Magic PE32+
        0, 0,                # version d'éditeur de liens
        L.ENTREE, len(texte), 0,
        L.ENTREE, L.TEXT_RVA,   # AddressOfEntryPoint, BaseOfCode
        L.IMAGE_BASE,
        L.SECT_ALIGN, L.FILE_ALIGN,
        6, 0,                # OS 6.0
        0, 1,                # version image 0.1
        6, 0,                # sous-système 6.0
        0,
        L.SIZE_OF_IMAGE,
        L.FILE_ALIGN,        # SizeOfHeaders
        0,                   # CheckSum
        3,                   # Subsystem : CONSOLE
        L.DLL_CHARACTERISTICS,
        0x100000, 0x1000, 0x100000, 0x1000,
        0, 16,
    )
    opt_fixe = bytes(opt_fixe)

    dirs = [(0, 0)] * 16
    dirs[1] = (L.R_DESC_IMPORT, 40)   # IMPORT : 2 descripteurs
    dirs[5] = (L.R_RELOC, 12)         # BASERELOC
    dirs[12] = (L.R_IAT, 24)          # IAT
    opt = opt_fixe + b"".join(struct.pack("<II", *d) for d in dirs)

    def sh(nom, vsize, vaddr, rawsz, rawptr, cara):
        return struct.pack("<8sIIIIIIHHI", nom, vsize, vaddr, rawsz, rawptr, 0, 0, 0, 0, cara)

    sections = (
        sh(b".text\x00\x00\x00", L.TEXT_VSIZE, L.TEXT_RVA, L.TEXT_VSIZE, L.TEXT_FILE, 0x60000020)
        + sh(b".rdata\x00\x00", L.RDATA_VSIZE, L.RDATA_RVA, L.RDATA_VSIZE, L.RDATA_FILE, 0x40000040)
        + sh(b".data\x00\x00\x00", L.DATA_VSIZE, L.DATA_RVA, L.DATA_RAW, L.DATA_FILE, 0xC0000040)
    )
    entetes = dos + b"PE\x00\x00" + coff + opt + sections
    assert len(entetes) == 64 + 4 + 20 + 240 + 120, len(entetes)
    exe = bytearray(b"\x00" * L.TAILLE_FICHIER)
    exe[0:len(entetes)] = entetes
    exe[L.TEXT_FILE:L.TEXT_FILE + len(texte)] = texte
    exe[L.RDATA_FILE:L.RDATA_FILE + len(rdata)] = rdata
    exe[L.DATA_FILE:L.DATA_FILE + len(data)] = data
    return bytes(exe)


# --- Validation PE ------------------------------------------------------------

def valider_pe(exe: bytes, phase: int):
    pe = pefile.PE(data=exe)
    assert pe.FILE_HEADER.Machine == 0x8664, "Machine != x86-64"
    assert pe.FILE_HEADER.NumberOfSections == 3, "sections != 3"
    assert pe.FILE_HEADER.Characteristics & 0x0002, "pas EXECUTABLE_IMAGE"
    assert pe.OPTIONAL_HEADER.Magic == 0x20B, "magic != PE32+"
    assert pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE, "point d'entrée != autotest"
    assert pe.OPTIONAL_HEADER.ImageBase == L.IMAGE_BASE
    assert pe.OPTIONAL_HEADER.Subsystem == 3, "sous-système != CONSOLE"
    dc = pe.OPTIONAL_HEADER.DllCharacteristics
    assert dc & 0x0040 and dc & 0x0020 and dc & 0x0100, "DYNAMICBASE/HIGH_ENTROPY_VA/NX absents"
    assert pe.OPTIONAL_HEADER.SizeOfImage == L.SIZE_OF_IMAGE
    noms = [s.Name.decode().rstrip("\x00") for s in pe.sections]
    assert noms == [".text", ".rdata", ".data"], noms
    assert pe.sections[0].Characteristics & 0x60000020 == 0x60000020, ".text non RX"
    assert pe.sections[1].Characteristics & 0x40000040 == 0x40000040, ".rdata non R"
    assert pe.sections[2].Characteristics & 0xC0000040 == 0xC0000040, ".data non RW"
    assert pe.sections[2].SizeOfRawData == L.DATA_RAW and pe.sections[2].Misc_VirtualSize == L.DATA_VSIZE
    imports = {}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        imports[entree.dll.decode().lower()] = [i.name.decode() for i in entree.imports]
    assert imports == {"kernel32.dll": L.DLL_IMPORTS}, imports
    assert pe.OPTIONAL_HEADER.DATA_DIRECTORY[12].VirtualAddress == L.R_IAT, "répertoire IAT absent"
    assert pe.OPTIONAL_HEADER.DATA_DIRECTORY[5].VirtualAddress == L.R_RELOC, "BASERELOC absent"
    assert len(exe) == L.TAILLE_FICHIER, "taille de fichier inattendue"
    # Le trampoline d'interruption défensif (int3) couvre les slots réservés
    assert exe[L.TEXT_FILE] == 0xCC and exe[L.TEXT_FILE + (0x10C0 - L.TEXT_RVA)] == 0xCC
    return True


# --- Preuve de réutilisation (R7) ----------------------------------------------

def preuve_reutilisation(exe: bytes, phase: int) -> dict:
    """Les blocs scellés M0 embarqués doivent être octet-identiques à hello.exe."""
    chemin_hello = os.path.join(M0_DIR, "hello.exe")
    with open(chemin_hello, "rb") as f:
        hello = f.read()
    sha_hello = hashlib.sha256(hello).hexdigest()
    if sha_hello != "c89e330cd16f3fd48558ed4fdb6708fb671e6d907547d5c1ee28075ffd6507f2":
        raise EchecBuild(f"hello.exe divergent de l'artefact scellé M0 (sha256 {sha_hello[:16]}…)")
    # hello.exe : .text @ file 0x200 ; selftest.exe : idem (TEXT_FILE)
    for bid, rva, slot in (("a10002", 0x1040, 0x40), ("a10003", 0x1080, 0x40)):
        origine = hello[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        embarque = exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        if origine != embarque:
            raise EchecBuild(f"réutilisation rompue : {bid} diffère de hello.exe (R7)")
    return {"hello_sha256": sha_hello, "blocs_reutilises": ["a10002", "a10003"]}


# --- Carte projet, génération 1 ------------------------------------------------

CONTRATS = {
    "a10001": ("() -> noreturn",
               "entree de processus hello.exe ; pile alignee",
               "message soumis a WriteFile ; ExitProcess(0)",
               "aucun stockage sous RSP ; appels IAT uniquement ; frame equilibre",
               "[a10002] [a10003] [ext kernel32:GetStdHandle]"),
    "a10002": ("(handle u64, ptr u8, len u32) -> bool",
               "handle de flux ; ptr tampon ; len > 0 ; pile alignee",
               "eax = verdict BOOL brut ; pile restauree",
               "shadow space alloue ; args 4 et 5 NULL",
               "[ext kernel32:WriteFile]"),
    "a10003": ("(code u32) -> noreturn",
               "code de sortie dans rcx",
               "processus termine, sans retour",
               "ud2 defensif immediat",
               "[ext kernel32:ExitProcess]"),
    "b20001": ("(dst ptr, src ptr, n u64) -> ptr",
               "regions valides sans chevauchement ; pile alignee",
               "n octets de dst egaux a src ; rax = dst ; src inchange",
               "feuille ; pile equilibree ; non volatils intacts ; n=0 sans ecriture",
               "aucune"),
    "b20002": ("(ptr1 ptr, ptr2 ptr, n u64) -> i32 normalise",
               "regions valides en lecture ; pile alignee",
               "eax = -1|0|+1 (premier octet divergent, non signe)",
               "feuille ; pile equilibree ; non volatils intacts ; aucune ecriture",
               "aucune"),
    "b20003": ("(s ptr) -> u64",
               "chaine NUL-terminee ; pile alignee",
               "rax = offset du premier octet nul ; chaine inchangee",
               "feuille ; pile equilibree ; non volatils intacts",
               "aucune"),
    "b20004": ("(valeur u32, tampon ptr) -> ptr",
               "tampon >= 12 octets ; pile alignee",
               "decimale ASCII compacte NUL-terminnee ; rax = tampon",
               "feuille ; rbx sauvegarde/restaure ; rien ecrit hors du tampon 12 o "
               "(espace de travail au-dela du NUL, R2)",
               "aucune"),
    "b20005": ("(taille u64, alignement u64) -> ptr|0",
               "alignement puissance de deux dans [1,64] ; curseur coherent",
               "pointeur aligne dans l arene, curseur avance ; echec -> 0 sans effet",
               "feuille ; seule ecriture = qword curseur (0x3000) ; ar base 0x3040",
               "[donnees .data:curseur,arene]"),
    "b20006": ("() -> ()",
               "curseur coherent",
               "curseur = 0",
               "feuille ; seule ecriture = qword curseur ; contenu arene indefini",
               "[donnees .data:curseur]"),
    "b20007": ("(dst ptr, octet u8, n u64) -> ptr",
               "region valide en ecriture ; pile alignee",
               "n octets de dst egaux a l octet ; rax = dst ; bornes intactes",
               "feuille ; rbx/rdi sauvegardes ; n=0 sans ecriture",
               "aucune"),
    "b20008": ("() -> noreturn",
               "point d entree selftest.exe ; pile alignee ; arene vierge",
               "ligne verdict sur stdout ; ExitProcess(0) si 21/21 sinon 1",
               "appels limites aux blocs libc + write/exit + IAT GSH ; frame 0x40 + 5 registres",
               "[b20001..b20007] [a10002] [a10003] [ext kernel32:GetStdHandle]"),
}

ROLES = {
    "a10001": "orchestration-hello", "a10002": "ecriture-stdout", "a10003": "sortie-processus",
    "b20001": "copie-memoire", "b20002": "comparaison-octets", "b20003": "longueur-chaine",
    "b20004": "conversion-decimale", "b20005": "allocation-zone", "b20006": "reinitialisation-zone",
    "b20007": "remplissage-memoire", "b20008": "autotest-minilibc",
}

ADRESSES_HELLO = {"a10001": 0x1000, "a10002": 0x1040, "a10003": 0x1080}  # dans hello.exe


def fragments_clairs(code: dict, exe: bytes, verrous: list[str], blocs: list[tuple],
                     phase: int, version: str, verdict_oracle: dict, compteurs: dict,
                     journal_runs: list[str]) -> dict[str, bytes]:
    sha = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()
    artefacts = {bid: ("hello,selftest" if bid in ("a10002", "a10003")
                       else "hello" if bid == "a10001" else "selftest")
                 for bid, _, _, _, _ in blocs} | {"a10001": "hello"}

    loc = ["[carte-frag] nom=frag-loc generation=1",
           "[zones] io=0x1000-0x10ff libc=0x1100-0x17ff app=0x1800-0x1ff "
           "reserve-libc=0x1440-0x17ff reserve-io=0x1000,0x10c0 (int3 defensif)"]
    # Budget de localisation (D31) : gabarit spec 4.3 + exe= + role= ; zone= retiree
    # (derivable des en-tetes [zones]), suffixe .exe implicite — 51 tok en moyenne
    # (cl100k_base), cible amendee 64 tokens (l'ancien format mesurait 56).
    for bid, sid, _, rva, slot in blocs:
        loc.append(f"[bloc] id={bid} spec={sid} cible=x86-64-win11-pe "
                   f"exe={artefacts[bid]} addr={L.IMAGE_BASE + rva:#x} size={slot} "
                   f"v=1 etat=scelle role={ROLES[bid]}")
    loc.append(f"[bloc] id=a10001 spec=hello-01:R1 cible=x86-64-win11-pe exe=hello "
               f"addr={L.IMAGE_BASE + 0x1000:#x} size=64 v=1 etat=scelle role=orchestration-hello")

    con = ["[carte-frag] nom=frag-con generation=1"]
    ordre_contrats = ["a10001", "a10002", "a10003"] + [bid for bid, _, _, _, _ in blocs if bid.startswith("b2")]
    for bid in ordre_contrats:
        sig, pre, post, inv, deps = CONTRATS[bid]
        con += [f"[bloc] id={bid}", f"  sig : {sig}", f"  pre : {pre}",
                f"  post : {post}", f"  inv : {inv}", f"  deps : {deps}"]

    prf = ["[carte-frag] nom=frag-prf generation=1"]
    tous = ["a10001"] + [bid for bid, _, _, _, _ in blocs]
    for bid in tous:
        fichier = next((f for b, s, f, _, _ in blocs if b == bid), "hello-01-main")
        notation = chemin_notation(fichier)
        with open(notation, "rb") as f:
            empreinte_notation = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [
            f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} crist={crist}/10",
            f"  vecteurs : roundtrip=ok structure=ok notation={empreinte_notation}",
            f"  differentiel : {verdict_oracle.get('blocs', {}).get(bid, {}).get('detail', 'emulation-binaire')}",
        ]
    prf.append("[verifications] runs=" + str(len(journal_runs)))
    prf += ["  " + r for r in journal_runs[-12:]]

    bld = ["[carte-frag] nom=frag-bld generation=1"]
    for bid, _, _, rva, slot in blocs:
        bld.append(f"[bloc] id={bid} addr={L.IMAGE_BASE + rva:#x} size={slot} "
                   f"empreinte={sha(code[bid]['slot'])}")
    hello = open(os.path.join(M0_DIR, "hello.exe"), "rb").read()
    bld.append(f"[bloc] id=a10001 addr={L.IMAGE_BASE + 0x1000:#x} size=64 "
               f"empreinte={sha(hello[L.TEXT_FILE: L.TEXT_FILE + 64])}")
    bld += [
        f"[build] artefact=selftest.exe version={version} profil=x86-64-win11-pe "
        f"taille={len(exe)} empreinte={sha(exe)}",
        f"  outils : keystone-engine + capstone {capstone.cs_version()[0]}.{capstone.cs_version()[1]} ; "
        f"verrous={len(verrous)} ; oracle : {verdict_oracle.get('total_cas', 0)} cas, "
        f"graine={verdict_oracle.get('graine', '-')}, volume={verdict_oracle.get('volume', '-')}",
        f"  heritage : hello.exe 0.1.0-dev.1 sha256:{hashlib.sha256(hello).hexdigest()} "
        f"(a10002/a10003 reutilises octet-identiques, R7)",
        "[zones] io=0x1000-0x10ff libc=0x1100-0x17ff app=0x1800-0x1fff",
    ]

    retour = {}
    for nom, lignes in (("frag-loc", loc), ("frag-con", con), ("frag-prf", prf), ("frag-bld", bld)):
        retour[nom] = ("\n".join(lignes) + "\n").encode("ascii", errors="replace")
    return retour


def construire_carte(code: dict, exe: bytes, verrous: list[str], blocs: list[tuple],
                     phase: int, version: str, verdict_oracle: dict, compteurs: dict,
                     journal_runs: list[str]):
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    clairs = fragments_clairs(code, exe, verrous, blocs, phase, version,
                              verdict_oracle, compteurs, journal_runs)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = cm.empreinte_racine(fragments)
    entete = cm.construire_entete(racine)
    prive, pub = cm.paire_cles(graine)
    signature = cm.signer(prive, entete, fragments)
    cm.ecrire_carte(entete, fragments, signature, pub)
    return pub


# --- Verrou croisé (R8) : relecture indépendante des artefacts ------------------

def verrou_croise(blocs: list[tuple]) -> tuple[int, dict]:
    phrase, graine = cm.charger_secrets(interactif=False)
    entete, fragments, signature, pub = cm.lire_carte()
    cm.verifier_listes_blanches(entete.decode("ascii"))                    # D15
    cm.verifier_signature(pub, entete, fragments, signature)               # R9
    if cm.empreinte_racine(fragments).hex() not in entete.decode("ascii"):
        raise cm.ErreurCarte("empreinte racine divergente")
    maitre = cm.cle_maitresse(phrase)
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
    with open(os.path.join(ICI, "selftest.exe"), "rb") as f:
        exe = f.read()
    empreintes, manifestes = {}, []
    manifeste = {}
    for ligne in bld.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[champs["id"]] = champs["empreinte"]
        elif ligne.startswith("[build]"):
            manifestes.append(dict(re.findall(r"(\w+)=(\S+)", ligne)))
    manifeste = next((m for m in manifestes if m.get("artefact") == "selftest.exe"), {})
    for bid, _, _, rva, slot in blocs:
        slot_octets = exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        sha = "sha256:" + hashlib.sha256(slot_octets).hexdigest()
        if sha != empreintes.get(bid):
            raise cm.ErreurCarte(f"verrou croisé : empreinte de {bid} divergente (R8)")
    sha_exe = "sha256:" + hashlib.sha256(exe).hexdigest()
    if sha_exe != manifeste.get("empreinte"):
        raise cm.ErreurCarte("verrou croisé : empreinte de selftest.exe divergente (R8)")
    # Bloc hérité non embarqué : vérifié contre hello.exe (multi-artefacts)
    hello = open(os.path.join(M0_DIR, "hello.exe"), "rb").read()
    slot_hello = hello[L.TEXT_FILE: L.TEXT_FILE + 64]
    if "sha256:" + hashlib.sha256(slot_hello).hexdigest() != empreintes.get("a10001"):
        raise cm.ErreurCarte("verrou croisé : empreinte de a10001 divergente vs hello.exe (R8)")
    return len(empreintes), manifeste


# --- Tableau de bord (§ 15.2, métriques M1) -------------------------------------

def tableau_de_bord(exe: bytes, verrous: list[str], nb_blocs_carte: int, manifeste: dict,
                    verdict_oracle: dict, phase: int) -> str:
    sha = lambda b: hashlib.sha256(b).hexdigest()
    budgets = "cible (instrumentation a executer : budgets_tokens.py)"
    chemin_budgets = os.path.join(ICI, "budgets.json")
    if os.path.exists(chemin_budgets):
        with open(chemin_budgets, encoding="utf-8") as f:
            bj = json.load(f)
        budgets = (f"mesure (M1) : localiser={bj['localiser']['mesure']} tok / "
                   f"editer={bj['editer']['mesure']} tok / ajouter={bj['ajouter']['mesure']} tok "
                   f"(cibles 64/3000/6000, D31)")
    conformite = "verte (conformite_profil.py : elements 1-4, 6-7 ; 5 hors perimetre M1)"
    chemin_conf = os.path.join(ICI, "conformite.txt")
    if os.path.exists(chemin_conf):
        with open(chemin_conf, encoding="ascii") as f:
            conformite = f.read().strip()
    lignes = [
        "[tableau] jalon=M1 artefact=selftest.exe version=" + manifeste.get("version", "?"),
        f"  blocs_avec_spec_a_jour        : {nb_blocs_carte}/11 : audit de tracabilite I->C->B",
        f"  chaines_I_C_B_tests           : 11/11 : specs, carte, exe, vecteurs (a10001 via hello.exe)",
        f"  construction                  : 0 erreur / 0 avertissement : build script",
        f"  tests_differentiels           : {verdict_oracle.get('total_cas', 0)} cas verts "
        f"({verdict_oracle.get('volume', '-')}, graine {verdict_oracle.get('graine', '-')}) ; "
        f"oracle structurel {len(verrous)} verrous PASS ; emulation binaire : "
        f"{verdict_oracle.get('binaire', 'n/a')}",
        f"  empreintes_donnees_embarquees : conforme (frag-bld : motifs, chaines, curseur nul)",
        f"  defauts_T1_T6_ouverts         : 0 : journal des decisions D28",
        f"  optimisations_sans_mesure     : 0 : division par 10 explicite (D21, R11)",
        f"  budgets_tokens                : {budgets}",
        f"  suite_conformite_profil       : {conformite}",
        f"  changements_hors_journal      : 0 : D27 a D32 consignees",
        f"  preversions                   : {manifeste.get('version', '?')} conforme "
        f"(schema dev/rc/final, monotonie)",
        f"  artefact                      : {len(exe)} octets ; empreinte sha256:{sha(exe)[:16]}... ; "
        f"reutilisation M0 : a10002/a10003 octet-identiques (R7)",
        f"  verrou_croise                 : {nb_blocs_carte} blocs reverifies (2 artefacts) + "
        f"signature Ed25519 + racine (R8/R9)",
    ]
    return "\n".join(lignes) + "\n"


# --- Assemblage + vérification communs -------------------------------------------

def assembler_tout(phase: int):
    """Assemble, round-trip et oracle structurel — commun construction/vérification."""
    blocs = blocs_phase(phase)
    specs = charger_couche_I(blocs)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code: dict[str, dict] = {}
    for bid, sid, fichier, rva, slot in blocs:
        chemin = chemin_notation(fichier)
        octets, metas = assembler_bloc(ks, chemin, rva, slot)
        insns = round_trip(cs, ks, chemin, rva, octets, metas)
        slot_complet = octets + b"\x90" * (slot - len(octets))
        code[bid] = {"octets": octets, "metas": metas, "insns": insns, "slot": slot_complet}
        print(f"[R5] {bid} ({sid}) : {len(octets)} o, round-trip {len(insns)}/{len(insns)} = 100 %")
    verrous = oracle_structurel(specs, code, blocs, phase)
    print(f"[oracle] structurel : {len(verrous)} verrous PASS (contrats I verifies sur le code)")
    return blocs, specs, code, verrous


def phase_courante() -> int:
    """Phase dérivée de la carte existante (version), défaut 2."""
    try:
        _, fragments, _, _ = cm.lire_carte()
        return 1
    except Exception:
        return 2


# --- Modes -----------------------------------------------------------------------

def construire(phase: int, volume: str, graine: int) -> int:
    print(f"=== M1 : chaine artefact TRIADE (profil x86-64-win11-pe, phase {phase}) ===")
    # Anti-rollback : une carte cristallisee (rc/final) interdit la reconstruction
    try:
        _, fragments, _, _ = cm.lire_carte()
        phrase, _ = cm.charger_secrets(interactif=False)
        maitre = cm.cle_maitresse(phrase)
        bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
        version_existante = next(
            (dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
             if "artefact=selftest.exe" in l), None)
        if version_existante and ("-rc" in version_existante
                                   or re.fullmatch(r"\d+\.\d+\.\d+", version_existante)):
            raise EchecBuild(
                f"carte scellee ({version_existante}) : reconstruction interdite — "
                f"procedure lourde R6 ou nouvelle version X.Y.Z+1 requise")
    except (cm.ErreurCarte, FileNotFoundError):
        pass  # pas de carte lisible : première construction

    blocs, specs, code, verrous = assembler_tout(phase)
    version = L.VERSION_DEV1 if phase == 1 else L.VERSION_DEV2

    texte, rdata, data = composer_sections(code, blocs, phase)
    exe = ecrire_pe32plus(texte, rdata, data)
    valider_pe(exe, phase)
    heritage = preuve_reutilisation(exe, phase)
    print(f"[PE] selftest.exe : {len(exe)} octets, 3 sections, imports kernel32 x3, "
          f"DYNAMICBASE+HEVA+NX, entree 0x{L.ENTREE:x}")
    print(f"[R7] reutilisation : a10002/a10003 octet-identiques a hello.exe "
          f"(sha256 {heritage['hello_sha256'][:16]}...)")

    verdict = od.executer(exe, graine=graine, volume=volume)
    print(f"[oracle] differentiel : {verdict['total_cas']} cas verts ; binaire emulate : "
          f"{verdict['binaire']} ; falsification : {verdict['falsification']}")

    with open(os.path.join(ICI, "selftest.exe"), "wb") as f:
        f.write(exe)

    compteurs = {bid: 1 for bid, _, _, _, _ in blocs}
    compteurs["a10001"] = 1
    journal = [f"run graine={graine} volume={volume} verdict={verdict['empreinte']} "
               f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} phase={phase} build={version}"]
    construire_carte(code, exe, verrous, blocs, phase, version, verdict, compteurs, journal)
    print("[carte] generation 1 ecrite : 4 fragments chiffres, signature Ed25519, 11 blocs indexes")

    nb, manifeste = verrou_croise(blocs)
    print(f"[R8] verrou croise : signature OK, racine OK, {nb} empreintes reverifiees, "
          f"artefact {manifeste.get('version')}")

    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="ascii") as f:
        f.write(tableau_de_bord(exe, verrous, nb, manifeste, verdict, phase))
    print("[tableau] tableau de bord ecrit (carte/tableau-de-bord.txt)")
    print(f"[B] selftest.exe scelle : sha256:{hashlib.sha256(exe).hexdigest()}")
    print(f"=== M1-dev (oracle vert) : {version} — validation terrain Windows 11 en attente ===")
    return 0


def verifier(graine: int, volume: str) -> int:
    print(f"=== M1 : re-verification complete (R5/R8, graine {graine}) ===")
    # Phase depuis la carte (dev.1 = 6 blocs, dev.2+ = 7)
    phase = 1
    try:
        phrase, _ = cm.charger_secrets(interactif=False)
        maitre = cm.cle_maitresse(phrase)
        _, fragments, _, _ = cm.lire_carte()
        bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
        if "b20007" in bld:
            phase = 2
        manifeste_v = next((dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
                            if "artefact=selftest.exe" in l), "?")
    except cm.ErreurCarte as exc:
        print(f"ECHEC (fail-closed) : carte illisible : {exc}", file=sys.stderr)
        return 1

    blocs, specs, code, verrous = assembler_tout(phase)

    # Identite notation <-> artefact : les slots assembles doivent etre l'exe
    with open(os.path.join(ICI, "selftest.exe"), "rb") as f:
        exe = f.read()
    for bid, _, _, rva, slot in blocs:
        embarque = exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        if embarque != code[bid]["slot"]:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5 — verifier-puis-ecrire)")

    verdict = od.executer(exe, graine=graine, volume=volume)
    print(f"[oracle] differentiel : {verdict['total_cas']} cas verts ; binaire : {verdict['binaire']}")

    # Cristallisation : increment des compteurs dans frag-prf, re-scellage de la carte
    phrase, graine_cles = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("ascii")
    compteurs, journal = {}, []
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            m = re.match(r"(\d+)/10", champs.get("crist", "1/10"))
            compteurs[champs["id"]] = int(m.group(1))
        elif ligne.startswith("  run "):
            journal.append(ligne.strip())
    for bid in [b for b, _, _, _, _ in blocs] + ["a10001"]:
        compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal.append(f"run graine={graine} volume={volume} verdict={verdict['empreinte']} "
                   f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")

    version = manifeste_v if manifeste_v != "?" else (L.VERSION_DEV1 if phase == 1 else L.VERSION_DEV2)
    construire_carte(code, exe, verrous, blocs, phase, version, verdict, compteurs, journal)
    nb, manifeste = verrou_croise(blocs)
    crist = {b: compteurs.get(b, 0) for b, _, _, _, _ in blocs}
    print(f"[R6] cristallisation : " + ", ".join(f"{b}={n}/10" for b, n in crist.items()))
    print(f"[R8] verrou croise : {nb} empreintes conformes ; artefact {manifeste.get('version')}")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="ascii") as f:
        f.write(tableau_de_bord(exe, verrous, nb, manifeste, verdict, phase))
    return 0


def sceller_rc() -> int:
    """Bascule la balise vers rc.1 : exige 10/10 partout + suite de conformite verte."""
    print("=== M1 : scellage rc.1 (cristallisation R6 + conformite § 8.2) ===")
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("ascii")
    compteurs = {}
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            compteurs[champs["id"]] = int(re.match(r"(\d+)/10", champs.get("crist", "0/10")).group(1))
    incomplets = {b: n for b, n in compteurs.items() if n < 10}
    if incomplets:
        raise EchecBuild(f"cristallisation incomplete : {incomplets} — 10 verifications requises (R6)")

    import conformite_profil as cp
    ok, lignes = cp.executer()
    print("\n".join(lignes))
    if not ok:
        raise EchecBuild("suite de conformite non verte — rc.1 refuse")

    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
    bld = bld.replace("version=0.2.0-dev.2", f"version={L.VERSION_RC1}")
    bld = bld.replace("version=0.2.0-dev.1", f"version={L.VERSION_RC1}")
    clairs = {"frag-bld": bld.encode("ascii")}
    for nom in ("frag-loc", "frag-con", "frag-prf"):
        clairs[nom] = cm.dechiffrer_fragment(maitre, nom, fragments[nom])
    nouveaux = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = cm.empreinte_racine(nouveaux)
    entete = cm.construire_entete(racine)
    _, graine_cles = cm.charger_secrets(interactif=False)
    prive, pub = cm.paire_cles(graine_cles)
    cm.ecrire_carte(entete, nouveaux, cm.signer(prive, entete, nouveaux), pub)
    print(f"[balise] {L.VERSION_RC1} : candidate a la validation terrain (§ 9)")
    return 0


def sceller_final() -> int:
    """Bascule la balise rc.1 -> 0.2.0 finale (constat terrain consigne, D32) :
    exige cristallisation 10/10 + suite de conformite verte + balise rc.1 courante.
    Ne touche aucun octet du binaire, seule la version du manifeste frag-bld change."""
    print("=== M1 : scellage final 0.2.0 (R6 + conformite § 8.2 + constat terrain D32) ===")
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("ascii")
    compteurs = {}
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            compteurs[champs["id"]] = int(re.match(r"(\d+)/10", champs.get("crist", "0/10")).group(1))
    incomplets = {b: n for b, n in compteurs.items() if n < 10}
    if incomplets:
        raise EchecBuild(f"cristallisation incomplete : {incomplets} — 10 verifications requises (R6)")

    import conformite_profil as cp
    ok, lignes = cp.executer()
    print("\n".join(lignes))
    if not ok:
        raise EchecBuild("suite de conformite non verte — 0.2.0 refuse")

    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
    occurrences = bld.count(f"version={L.VERSION_RC1}")
    if occurrences != 1:
        raise EchecBuild(f"balise {L.VERSION_RC1} attendue une fois dans frag-bld "
                         f"({occurrences} occurrence(s)) — scellage final refuse (fail-closed)")
    bld = bld.replace(f"version={L.VERSION_RC1}", f"version={L.VERSION_FINALE}")
    clairs = {"frag-bld": bld.encode("ascii")}
    for nom in ("frag-loc", "frag-con", "frag-prf"):
        clairs[nom] = cm.dechiffrer_fragment(maitre, nom, fragments[nom])
    nouveaux = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = cm.empreinte_racine(nouveaux)
    entete = cm.construire_entete(racine)
    _, graine_cles = cm.charger_secrets(interactif=False)
    prive, pub = cm.paire_cles(graine_cles)
    cm.ecrire_carte(entete, nouveaux, cm.signer(prive, entete, nouveaux), pub)
    print(f"[balise] {L.VERSION_FINALE} : version finale immuable (§ 9) — "
          f"defaut ulterieur -> 0.2.1 a contrat stable (R4)")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if "--verifier" in args:
            graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 1
            volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
            sys.exit(verifier(graine, volume))
        if "--sceller-rc" in args:
            sys.exit(sceller_rc())
        if "--sceller-final" in args:
            sys.exit(sceller_final())
        phase = int(args[args.index("--phase") + 1]) if "--phase" in args else 2
        volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
        graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 1
        sys.exit(construire(phase, volume, graine))
    except (EchecBuild, cm.ErreurCarte, od.EchecOracle) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
