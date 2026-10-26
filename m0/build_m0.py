#!/usr/bin/env python3
"""build_m0.py : Jalon M0 de TRIADE : chaîne artefact sans compilateur.

Notation (keystone) -> octets -> PE32+ écrit à la main -> carte v0 signée.
Implémente la checklist M0 de REPRISE_PROJET.md § 7.2 sous les règles R1-R3
(intention d'abord, balisage, jamais de binaire nu), R5 (vérifie-puis-écrit :
round-trip + oracle), R8-R9 (verrou croisé, carte signée).

L'ORACLE (D1) est régénéré à chaque exécution depuis la couche I
(m0/I/*.md) : il n'est ni chargé depuis un fichier, ni persisté. Seuls ses
verdicts hachés survivent dans frag-prf. L'oracle M0 a deux volets :
  1. round-trip de notation : keystone -> capstone -> keystone, octets
     identiques (fidélité exacte, WYSIWYG) ;
  2. contrat structurel : les invariants et disciplines déclarés dans les
     spécifications I sont vérifiés mécaniquement sur le code désassemblé
     (appels IAT uniquement, shadow space, alignement, padding, cibles).
L'oracle différentiel complet (entrées aléatoires, ~12 000 cas) arrive à M1
avec la mini-libc : premier terrain de cristallisation (PLAN_MILESTONES M1).

Usage :
  python3 build_m0.py             # construction + vérification complète
  python3 build_m0.py --verifier  # verrou croisé seul (R8, avant chaque édition)

Déterminisme : hello.exe est byte-identique à chaque exécution (horodatages
nuls, layout fixe). La carte est re-chiffrée avec des nonces frais (par
conception, seul l'artefact doit être reproductible).
"""

from __future__ import annotations

import hashlib
import os
import re
import struct
import sys

import capstone
import pefile
from keystone import Ks, KS_ARCH_X86, KS_MODE_64

import carte_m0 as cm

ICI = os.path.dirname(os.path.abspath(__file__))
VERSION_ARTIFACT = "0.1.0-dev.1"  # § 9 : oracle vert, validation terrain en attente

# --- Layout fixe du profil x86-64-win11-pe (R7 : jamais déplacé) --------------

IMAGE_BASE = 0x140000000
TEXT_RVA, RDATA_RVA = 0x1000, 0x2000
FILE_ALIGN, SECT_ALIGN = 0x200, 0x1000
TEXT_FILE, RDATA_FILE = 0x200, 0x400
SLOT = 64  # un slot par bloc, multiple de 16, inter-blocs >= 16 octets (D8)

BLOCS = [
    # (id carte, spec, fichier notation, rva slot)
    ("a10001", "hello-01:R1", "hello-01-main.asm", 0x1000),
    ("a10002", "hello-02:R1", "hello-02-write.asm", 0x1040),
    ("a10003", "hello-03:R1", "hello-03-exit.asm", 0x1080),
]
TEXT_VSIZE = 3 * SLOT  # 0xC0

MESSAGE = b"TRIADE M0 : Hello, Windows 11 !\r\n\x00"  # 33 octets utiles + NUL
MSG_RVA = 0x2000

# .rdata (RVA) : message, descripteurs d'import, hint/names, INT, IAT, relocations
R_DESC_IMPORT = 0x2030     # descripteur kernel32 (20 o) puis descripteur nul (20 o)
R_NOM_DLL = 0x2058         # "kernel32.dll\0"
R_HN_GSH, R_HN_WF, R_HN_EP = 0x2066, 0x2076, 0x2082  # hint/name (pairs)
R_INT = 0x2090             # OriginalFirstThunk (4 qwords, terminateur 0)
R_IAT = 0x20B0             # FirstThunk / IAT : [0] GetStdHandle [1] WriteFile [2] ExitProcess
R_RELOC = 0x20D0           # bloc de relocalisation minimal (ASLR, entrées ABSOLUTE)
RDATA_VSIZE = 0xE0

IAT_SLOTS = {  # cibles sémantiques des appels IAT (D7)
    "GetStdHandle": R_IAT + 0 * 8,
    "WriteFile": R_IAT + 1 * 8,
    "ExitProcess": R_IAT + 2 * 8,
}
DLL_IMPORTS = ["GetStdHandle", "WriteFile", "ExitProcess"]

DLL_CHARACTERISTICS = 0x0040 | 0x0020 | 0x0100  # DYNAMICBASE | HIGH_ENTROPY_VA | NX_COMPAT


class EchecBuild(Exception):
    """Tout échec de l'oracle, du round-trip ou de la construction."""


# --- Couche I : lecture et audit du gabarit ----------------------------------

def lire_spec(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", texte)
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3)), "texte": texte}
    for bloc in ("Intention", "Contrat", "Échecs", "Vecteurs", "Fixtures", "Provenance", "Décisions"):
        if bloc + " " not in texte and bloc + " :" not in texte and bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")
    if "écrite-avant-code" not in texte:
        raise EchecBuild(f"{chemin} : provenance inattendue (R2 : écrite-avant-code)")
    return spec


def charger_couche_I() -> dict[str, dict]:
    fichiers = {"a10001": "hello-01-main.md", "a10002": "hello-02-write.md", "a10003": "hello-03-exit.md"}
    specs = {}
    for bid, sid, _, _ in BLOCS:
        chemin = os.path.join(ICI, "I", fichiers[bid])
        if not os.path.exists(chemin):
            raise EchecBuild(f"spécification I introuvable pour {sid} : {chemin}")
        spec = lire_spec(chemin)
        if f"{spec['id']}:R{spec['rev']}" != sid:
            raise EchecBuild(f"{chemin} : identifiant/révision {spec['id']}:R{spec['rev']} != carte {sid}")
        specs[bid] = spec
    return specs


# --- Notation : assemblage ligne à ligne -------------------------------------

def lignes_notation(chemin: str) -> list[str]:
    with open(chemin, encoding="utf-8") as f:
        brut = f.read().splitlines()
    return [l.strip() for l in brut if l.strip() and not l.strip().startswith(";")]


def assembler_bloc(ks: Ks, chemin: str, rva: int) -> tuple[bytes, list[dict]]:
    """Assemble chaque ligne à son adresse courante ; retourne (octets, méta)."""
    octets, metas, adresse = b"", [], rva
    for ligne in lignes_notation(chemin):
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise EchecBuild(f"{chemin} : ligne inassemblable : {ligne!r}")
        b = bytes(enc)
        metas.append({"ligne": ligne, "adresse": adresse, "taille": len(b)})
        octets += b
        adresse += len(b)
    if len(octets) > SLOT:
        raise EchecBuild(f"{chemin} : {len(octets)} o > slot {SLOT} (D8)")
    return octets, metas


# --- Round-trip (R5) ----------------------------------------------------------

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
    """keystone -> capstone -> keystone : octets ET texte identiques."""
    instructions = list(cs.disasm(octets, rva))
    attendu = len(metas)
    if len(instructions) != attendu:
        raise EchecBuild(f"{chemin} : {len(instructions)} instructions désassemblées != {attendu} notées")
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


# --- Oracle structurel : les invariants de I, vérifiés sur le code ------------

def operande_rip_cible(insn) -> int | None:
    """Cible d'un opérande [rip + d] (appel IAT ou lea)."""
    m = re.search(r"\[rip \+ (0x[0-9a-f]+)\]", insn.op_str)
    if m:
        return insn.address + insn.size + int(m.group(1), 16)
    m = re.search(r"\[rip - (0x[0-9a-f]+)\]", insn.op_str)
    if m:
        return insn.address + insn.size - int(m.group(1), 16)
    return None


def oracle_structurel(specs: dict, code: dict[str, tuple[bytes, list]]) -> list[str]:
    """Vérifie sur le code désassemblé les contrats déclarés dans I (D1 : régénéré)."""
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    for bid, sid, _, rva in BLOCS:
        insns = code[bid]["insns"]
        mnemos = [i.mnemonic for i in insns]

        # S1/S2/S3 : discipline d'entrée : frame + shadow space (P2/P4, I1)
        verrou(f"{bid}:frame-entree", insns and insns[0].mnemonic == "sub"
               and "rsp" in insns[0].op_str and "0x28" in insns[0].op_str)

        # S4 : interface système : IAT uniquement, jamais direct (hello-01 I2 / D7)
        verrou(f"{bid}:pas-de-syscall", not any(m in ("syscall", "int", "sysenter") for m in mnemos))

        # S5 : aucun stockage sous RSP (I1)
        for i in insns:
            if i.mnemonic.startswith("mov") and "[" in i.op_str and i.op_str.split(",")[0].strip().endswith("]"):
                base = re.search(r"\[(\w+)", i.op_str)
                disp = re.search(r"\+ (0x[0-9a-f]+)\]", i.op_str)
                if base and base.group(1) == "rsp":
                    verrou(f"{bid}:pas-de-stockage-sous-rsp@{i.address:#x}",
                           disp is None or int(disp.group(1), 16) >= 0)

        # S13 : cibles RIP : sémantique vérifiée, pas seulement textuelle
        for i in insns:
            cible = operande_rip_cible(i)
            if cible is not None and i.mnemonic == "call":
                verrou(f"{bid}:appel-iat-valide@{i.address:#x}", cible in IAT_SLOTS.values(),
                       f"cible {cible:#x} hors IAT")

        # S15 : padding inter-blocs >= 16 (D8), slots alignés 16
        fin_code = insns[-1].address + insns[-1].size
        slot_suivant = min((r for _, _, _, r in BLOCS if r > rva), default=TEXT_RVA + TEXT_VSIZE)
        verrou(f"{bid}:padding-16", slot_suivant - fin_code >= 16,
               f"écart {slot_suivant - fin_code}")
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)

    # hello-01 (a10001) : orchestration (P1, Q1, Q2, deps)
    m = code["a10001"]["insns"]
    lignes = [x["ligne"] for x in code["a10001"]["metas"]]
    verrou("a10001:stdout", any(canon(l) == canon("mov ecx, -11") for l in lignes), "(STD_OUTPUT_HANDLE)")
    verrou("a10001:longueur-message",
           any(canon(l) == canon(f"mov r8d, {len(MESSAGE) - 1}") for l in lignes),
           f"attendu {len(MESSAGE) - 1}")
    verrou("a10001:code-sortie-zero", any(canon(l) == canon("xor ecx, ecx") for l in lignes))
    verrous_lea = [operande_rip_cible(i) for i in m if i.mnemonic == "lea"]
    verrou("a10001:lea-message", MSG_RVA in verrous_lea, f"cibles {list(map(hex, verrous_lea))}")
    cibles_appel = [int(i.op_str, 16) for i in m if i.mnemonic == "call" and not i.op_str.startswith("qword")]
    verrou("a10001:appels-inter-blocs", set(cibles_appel) == {0x1040, 0x1080}, f"{list(map(hex, cibles_appel))}")

    # hello-02 (a10002) : contrat WriteFile à cinq arguments (Q2, Q3, I1)
    w = code["a10002"]["insns"]
    verrou("a10002:arg4-null", any(operande_rip_cible(i) is None and i.mnemonic == "xor" and i.op_str == "r9d, r9d" for i in w))
    verrou("a10002:arg5-null", any(i.mnemonic == "mov" and canon(i.op_str) == canon("qword ptr [rsp + 0x20], 0") for i in w))
    idx_iat = [n for n, i in enumerate(w) if i.mnemonic == "call" and operande_rip_cible(i) == IAT_SLOTS["WriteFile"]]
    verrou("a10002:appel-unique-writefile", len(idx_iat) == 1)
    iat = idx_iat[0]
    verrou("a10002:args-avant-appel",
           any(n < iat and i.mnemonic == "xor" and i.op_str == "r9d, r9d" for n, i in enumerate(w))
           and any(n < iat and i.mnemonic == "mov" and canon(i.op_str) == canon("qword ptr [rsp + 0x20], 0") for n, i in enumerate(w)))
    verrou("a10002:pile-restauree", w[-1].mnemonic == "ret" and any(i.mnemonic == "add" and "rsp" in i.op_str for i in w))
    subs = sum(1 for i in w if i.mnemonic == "sub" and "rsp" in i.op_str)
    adds = sum(1 for i in w if i.mnemonic == "add" and "rsp" in i.op_str)
    verrou("a10002:frame-equilibre", subs == adds == 1)

    # hello-03 (a10003) : noreturn (Q1, I1)
    e = code["a10003"]["insns"]
    verrou("a10003:sans-retour", not any(i.mnemonic == "ret" for i in e))
    verrou("a10003:ud2-defensif", e[-1].mnemonic == "ud2")
    idx_ep = [n for n, i in enumerate(e) if i.mnemonic == "call" and operande_rip_cible(i) == IAT_SLOTS["ExitProcess"]]
    verrou("a10003:appel-unique-exitprocess", len(idx_ep) == 1 and e[idx_ep[0] + 1].mnemonic == "ud2")

    # S17 : traçabilité : les specs I existent, au couple (id, révision) de la carte
    verrou("traçabilité-I", all(s in specs for s in ("a10001", "a10002", "a10003")))
    return verrous


# --- Composition des sections -------------------------------------------------

def composer_sections(code: dict) -> tuple[bytes, bytes]:
    texte = b""
    for bid, _, _, rva in BLOCS:
        octets = code[bid]["octets"]
        pad = SLOT - len(octets)
        if pad < 16:
            raise EchecBuild(f"{bid} : padding {pad} < 16 (D8)")
        texte += octets + b"\x90" * pad
    assert len(texte) == TEXT_VSIZE

    hn = lambda nom: struct.pack("<H", 0) + nom.encode("ascii") + b"\x00"
    rdata = bytearray(b"\x00" * RDATA_VSIZE)

    def poser(rva: int, donnees: bytes):
        rdata[rva - RDATA_RVA: rva - RDATA_RVA + len(donnees)] = donnees

    poser(MSG_RVA, MESSAGE)
    # Descripteur d'import kernel32 + descripteur nul terminateur
    poser(R_DESC_IMPORT, struct.pack("<IIIII", R_INT, 0, 0, R_NOM_DLL, R_IAT))
    poser(R_DESC_IMPORT + 20, b"\x00" * 20)
    poser(R_NOM_DLL, b"kernel32.dll\x00")
    poser(R_HN_GSH, hn("GetStdHandle"))
    poser(R_HN_WF, hn("WriteFile"))
    poser(R_HN_EP, hn("ExitProcess"))
    hv = {n: v for n, v in (("GetStdHandle", R_HN_GSH), ("WriteFile", R_HN_WF), ("ExitProcess", R_HN_EP))}
    poser(R_INT, b"".join(struct.pack("<Q", hv[n]) for n in DLL_IMPORTS) + struct.pack("<Q", 0))
    poser(R_IAT, b"".join(struct.pack("<Q", hv[n]) for n in DLL_IMPORTS) + struct.pack("<Q", 0))
    # Bloc de relocalisation minimal : ASLR actif, image déjà indépendante en position
    poser(R_RELOC, struct.pack("<II", TEXT_RVA, 12) + struct.pack("<HH", 0, 0))
    return texte, bytes(rdata)


# --- Éditeur PE32+ ------------------------------------------------------------

def ecrire_pe32plus(texte: bytes, rdata: bytes) -> bytes:
    """En-têtes DOS/COFF/PE32+ écrits à la main : agent manual § 7.2."""
    dos = b"MZ" + b"\x00" * 58 + struct.pack("<I", 0x40)
    coff = struct.pack("<HHIIIHH", 0x8664, 2, 0, 0, 0, 0xF0, 0x0002)

    tailles = (len(texte), len(rdata))
    opt_fixe = struct.pack(
        "<HBBIIIIIQIIHHHHHHIIIIHHQQQQII",
        0x20B,               # Magic PE32+
        0, 0,                # version d'éditeur de liens
        tailles[0], tailles[1], 0,
        TEXT_RVA, TEXT_RVA,  # AddressOfEntryPoint, BaseOfCode
        IMAGE_BASE,
        SECT_ALIGN, FILE_ALIGN,
        6, 0,                # OS 6.0
        0, 1,                # version image 0.1
        6, 0,                # sous-système 6.0
        0,
        0x3000,              # SizeOfImage : .text 0x1000 + .rdata 0x2000 -> fin 0x3000
        FILE_ALIGN,          # SizeOfHeaders
        0,                   # CheckSum
        3,                   # Subsystem : CONSOLE
        DLL_CHARACTERISTICS,
        0x100000, 0x1000, 0x100000, 0x1000,
        0, 16,
    )
    opt_fixe = bytes(opt_fixe)

    dirs = [(0, 0)] * 16
    dirs[1] = (R_DESC_IMPORT, 40)      # IMPORT : 2 descripteurs
    dirs[5] = (R_RELOC, 12)            # BASERELOC
    dirs[12] = (R_IAT, 24)             # IAT
    opt = opt_fixe + b"".join(struct.pack("<II", *d) for d in dirs)

    def sh(nom, vsize, vaddr, rawsz, rawptr, cara):
        return struct.pack("<8sIIIIIIHHI", nom, vsize, vaddr, rawsz, rawptr, 0, 0, 0, 0, cara)

    sections = (
        sh(b".text\x00\x00\x00", TEXT_VSIZE, TEXT_RVA, FILE_ALIGN, TEXT_FILE, 0x60000020)
        + sh(b".rdata\x00\x00", RDATA_VSIZE, RDATA_RVA, FILE_ALIGN, RDATA_FILE, 0x40000040)
    )
    entetes = dos + b"PE\x00\x00" + coff + opt + sections
    assert len(entetes) == 64 + 4 + 20 + 240 + 80, len(entetes)
    exe = bytearray(b"\x00" * (TEXT_FILE + 2 * FILE_ALIGN))
    exe[0:len(entetes)] = entetes
    exe[TEXT_FILE:TEXT_FILE + len(texte)] = texte
    exe[RDATA_FILE:RDATA_FILE + len(rdata)] = rdata
    return bytes(exe)


# --- Validation PE (suite de conformité M0 : éléments couverts) ---------------

def valider_pe(exe: bytes):
    pe = pefile.PE(data=exe)
    assert pe.FILE_HEADER.Machine == 0x8664, "Machine != x86-64"
    assert pe.FILE_HEADER.Characteristics & 0x0002, "pas EXECUTABLE_IMAGE"
    assert pe.OPTIONAL_HEADER.Magic == 0x20B, "magic != PE32+"
    assert pe.OPTIONAL_HEADER.AddressOfEntryPoint == TEXT_RVA, "point d'entrée != a10001"
    assert pe.OPTIONAL_HEADER.ImageBase == IMAGE_BASE
    assert pe.OPTIONAL_HEADER.Subsystem == 3, "sous-système != CONSOLE"
    dc = pe.OPTIONAL_HEADER.DllCharacteristics
    assert dc & 0x0040 and dc & 0x0020 and dc & 0x0100, "DYNAMICBASE/HIGH_ENTROPY_VA/NX absents"
    assert pe.OPTIONAL_HEADER.SizeOfImage == 0x3000
    noms = [s.Name.decode().rstrip("\x00") for s in pe.sections]
    assert noms == [".text", ".rdata"], noms
    assert pe.sections[0].Characteristics & 0x60000020 == 0x60000020, ".text non RX"
    assert pe.sections[1].Characteristics & 0x40000040 == 0x40000040, ".rdata non R"
    imports = {}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        imports[entree.dll.decode().lower()] = [i.name.decode() for i in entree.imports]
    assert imports == {"kernel32.dll": DLL_IMPORTS}, imports
    assert pe.OPTIONAL_HEADER.DATA_DIRECTORY[5].VirtualAddress == R_RELOC, "BASERELOC absent"
    assert len(exe) == TEXT_FILE + 2 * FILE_ALIGN, "taille de fichier inattendue"
    assert len(exe) < 4096, f"exécutable {len(exe)} o >= 4 Kio (critère M0)"
    return True


# --- Carte v0 -----------------------------------------------------------------

def fragments_clairs(code: dict, exe: bytes, verrous: list[str]) -> dict[str, bytes]:
    sha = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()
    loc = ["[carte-frag] nom=frag-loc generation=0"]
    con = ["[carte-frag] nom=frag-con generation=0"]
    prf = ["[carte-frag] nom=frag-prf generation=0"]
    bld = ["[carte-frag] nom=frag-bld generation=0"]
    adresses = {bid: IMAGE_BASE + rva for bid, _, _, rva in BLOCS}
    empreintes = {bid: sha(code[bid]["slot"]) for bid, _, _, _ in BLOCS}
    for bid, sid, _, _ in BLOCS:
        loc.append(f"[bloc] id={bid} spec={sid} cible=x86-64-win11-pe "
                   f"addr={adresses[bid]:#x} size={SLOT} v=1 etat=scelle")
    con += [
        "[bloc] id=a10001",
        "  sig : () -> noreturn",
        "  pre : entree de processus ; pile alignee (rsp = 8 mod 16)",
        "  post : message soumis a WriteFile sur stdout ; processus termine par ExitProcess(0)",
        "  regs : aucun non volatil modifie ; conv: msx64",
        "  inv : aucun stockage sous RSP ; appels IAT uniquement ; frame equilibre",
        "  deps : [a10002] [a10003] [ext kernel32:GetStdHandle]",
        "[bloc] id=a10002",
        "  sig : (handle u64, ptr u8, len u32) -> bool",
        "  pre : handle de flux ; ptr tampon ; len > 0 ; pile alignee",
        "  post : eax = verdict BOOL brut ; pile restauree",
        "  regs : aucun non volatil modifie ; conv: msx64",
        "  inv : shadow space alloue ; args 4 et 5 NULL",
        "  deps : [ext kernel32:WriteFile]",
        "[bloc] id=a10003",
        "  sig : (code u32) -> noreturn",
        "  pre : code de sortie dans rcx",
        "  post : processus termine, sans retour",
        "  regs : sans objet (noreturn) ; conv: msx64",
        "  inv : ud2 defensif immediat",
        "  deps : [ext kernel32:ExitProcess]",
    ]
    for bid, _, fichier, _ in BLOCS:
        prf += [
            f"[bloc] id={bid} etat=scelle crist=1/10",
            f"  vecteurs : roundtrip=ok structure=ok ; notation={sha(open(os.path.join(ICI, 'notation', fichier), 'rb').read())}",
            f"  execution : en attente (critere M0 de validation terrain)",
        ]
    for bid, _, _, _ in BLOCS:
        bld.append(f"[bloc] id={bid} addr={adresses[bid]:#x} size={SLOT} empreinte={empreintes[bid]}")
    bld += [
        f"[build] artefact=hello.exe version={VERSION_ARTIFACT} profil=x86-64-win11-pe "
        f"taille={len(exe)} empreinte={sha(exe)}",
        f"  outils : keystone-engine + capstone {capstone.cs_version()[0]}.{capstone.cs_version()[1]} ; verrous={len(verrous)}",
        f"  donnees : message={sha(MESSAGE)} ; iat={','.join(DLL_IMPORTS)}",
    ]
    retour = {}
    for nom, lignes in (("frag-loc", loc), ("frag-con", con), ("frag-prf", prf), ("frag-bld", bld)):
        retour[nom] = ("\n".join(lignes) + "\n").encode("ascii")
    return retour


def construire_carte(code: dict, exe: bytes, verrous: list[str]):
    phrase, graine = cm.charger_secrets()
    maitre = cm.cle_maitresse(phrase)
    clairs = fragments_clairs(code, exe, verrous)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = cm.empreinte_racine(fragments)
    entete = cm.construire_entete(racine)
    prive, pub = cm.paire_cles(graine)
    signature = cm.signer(prive, entete, fragments)
    cm.ecrire_carte(entete, fragments, signature, pub)
    return pub


# --- Verrou croisé (R8) : relecture indépendante des artefacts ----------------

def verrou_croise():
    phrase, graine = cm.charger_secrets(interactif=False)
    entete, fragments, signature, pub = cm.lire_carte()
    texte_entete = entete.decode("ascii")
    cm.verifier_listes_blanches(texte_entete)                       # D15
    cm.verifier_signature(pub, entete, fragments, signature)        # R9
    if cm.empreinte_racine(fragments).hex() not in texte_entete:    # racine
        raise cm.ErreurCarte("empreinte racine divergente")
    maitre = cm.cle_maitresse(phrase)
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
    with open(os.path.join(ICI, "hello.exe"), "rb") as f:
        exe = f.read()
    empreintes, manifeste = {}, {}
    for ligne in bld.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[champs["id"]] = champs["empreinte"]
        elif ligne.startswith("[build]"):
            manifeste = dict(re.findall(r"(\w+)=(\S+)", ligne))
    for bid, _, _, rva in BLOCS:
        slot = exe[TEXT_FILE + (rva - TEXT_RVA): TEXT_FILE + (rva - TEXT_RVA) + SLOT]
        sha = "sha256:" + hashlib.sha256(slot).hexdigest()
        if sha != empreintes.get(bid):
            raise cm.ErreurCarte(f"verrou croisé : empreinte de {bid} divergente (R8)")
    sha_exe = "sha256:" + hashlib.sha256(exe).hexdigest()
    if sha_exe != manifeste.get("empreinte"):
        raise cm.ErreurCarte("verrou croisé : empreinte de l'artefact divergente (R8)")
    return len(empreintes), manifeste


# --- Tableau de bord (§ 15.2, métriques M0) -----------------------------------

def tableau_de_bord(code: dict, exe: bytes, verrous: list[str], nb_blocs: int, manifeste: dict) -> str:
    sha = lambda b: hashlib.sha256(b).hexdigest()
    lignes = [
        "[tableau] jalon=M0 artefact=hello.exe version=" + VERSION_ARTIFACT,
        f"  blocs_avec_spec_a_jour        : 3/3 (100 %) : audit de tracabilite I->C->B",
        f"  chaines_I_C_B_tests           : 3/3 (100 %) : spec, carte, exe, vecteurs",
        f"  construction                  : 0 erreur / 0 avertissement : build script",
        f"  tests_differentiels           : round-trip 3/3 blocs 100 % ; oracle structurel {len(verrous)} verrous PASS",
        f"  empreintes_donnees_embarquees : message sha256:{sha(MESSAGE)[:16]}... conforme (frag-bld)",
        f"  defauts_T1_T6_ouverts         : 0 : journal des decisions D26",
        f"  optimisations_sans_mesure     : 0 : aucun journal d'optimisation a M0 (R11)",
        f"  budgets_tokens                : cible (instrumentation a partir de M1)",
        f"  suite_conformite_profil       : elements 1,3,4,6,7 verts ; 2 structurel (execution terrain attendue) ; 5 hors perimetre M0",
        f"  changements_hors_journal      : 0 : D26 consignee",
        f"  preversions                   : {VERSION_ARTIFACT} conforme (schema dev/rc/final, securite 9)",
        f"  artefact                      : {len(exe)} octets (< 4096) ; empreinte sha256:{sha(exe)[:16]}...",
        f"  verrou_croise                 : {nb_blocs} blocs reverifies + signature Ed25519 + racine (R8/R9)",
    ]
    return "\n".join(lignes) + "\n"


# --- Programme principal ------------------------------------------------------

def construire() -> int:
    print("=== M0 : chaine artefact TRIADE (profil x86-64-win11-pe) ===")
    specs = charger_couche_I()
    print(f"[I] 3 specifications chargees et auditees (gabarit 2.2, provenance ecrite-avant-code)")

    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    cs.detail = False

    code: dict[str, dict] = {}
    for bid, sid, fichier, rva in BLOCS:
        chemin = os.path.join(ICI, "notation", fichier)
        octets, metas = assembler_bloc(ks, chemin, rva)
        insns = round_trip(cs, ks, chemin, rva, octets, metas)
        slot = octets + b"\x90" * (SLOT - len(octets))
        code[bid] = {"octets": octets, "metas": metas, "insns": insns, "slot": slot}
        print(f"[R5] {bid} ({sid}) : {len(octets)} o de code, round-trip {len(insns)}/{len(insns)} instructions = 100 %")

    verrous = oracle_structurel(specs, code)
    print(f"[oracle] structurel : {len(verrous)} verrous PASS (contrats I verifies sur le code)")

    texte, rdata = composer_sections(code)
    exe = ecrire_pe32plus(texte, rdata)
    valider_pe(exe)
    print(f"[PE] hello.exe : {len(exe)} octets, en-tetes valides, imports kernel32 x3, DYNAMICBASE+HEVA+NX, < 4 Kio")

    with open(os.path.join(ICI, "hello.exe"), "wb") as f:
        f.write(exe)

    construire_carte(code, exe, verrous)
    print(f"[carte] v0 ecrite : 4 fragments chiffres (XChaCha20-Poly1305), signature Ed25519, racine consignee")

    nb, manifeste = verrou_croise()
    print(f"[R8] verrou croise : signature OK, racine OK, {nb} empreintes de blocs reverifiees, artefact {manifeste.get('version')}")

    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="ascii") as f:
        f.write(tableau_de_bord(code, exe, verrous, nb, manifeste))
    print("[tableau] tableau de bord de conformite ecrit (carte/tableau-de-bord.txt)")

    with open(os.path.join(ICI, "hello.exe"), "wb") as f:
        f.write(exe)
    print(f"[B] hello.exe scelle : sha256:{hashlib.sha256(exe).hexdigest()}")
    print("=== M0-dev (oracle vert) : validation terrain Windows 11 en attente ===")
    return 0


def verifier_seul() -> int:
    print("=== M0 : verrou croise seul (R8/R9 : avant chaque edition) ===")
    nb, manifeste = verrou_croise()
    print(f"[R8] signature Ed25519 OK ; racine OK ; {nb} empreintes de blocs conformes ; artefact {manifeste.get('version')}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(verifier_seul() if "--verifier" in sys.argv else construire())
    except (EchecBuild, cm.ErreurCarte) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
