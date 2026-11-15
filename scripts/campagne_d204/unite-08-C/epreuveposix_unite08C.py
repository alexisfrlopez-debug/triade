#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuveposix_unite08C.py — LE CONTRAT REJOUÉ AU POSIX contre la pièce
même (l'unité 4, loupe-08 × bras C, la campagne D204). La dll est mappée par
sections comme le chargeur (RVA → adresse, la base préférée — AUCUN
relocation à appliquer), l'export loupe_08_ligne APPELÉ NATURELLEMENT (la
feuille pure ne connaît aucun import : le code x86-64 court au CPU réel du
labo) — le juge est le MODÈLE INDÉPENDANT.

  V1 le doré : la première ligne de proxy.exe scellé + la ligne finale
     incomplète du témoin 3 × 64 Kio + 1 (Q1-Q4) ;
  V2 le différentiel : 10 000 lignes (la graine 20261115, les MÊMES
     tirages que le juge T), la sortie == le modèle OCTET PAR OCTET, le
     poison au-delà de 77 INTACT (I2), la source LUE SEULE (I3) ;
  V3 les rejets : longueur 0 / 17, source nulle, sortie nulle → -5, la
     sortie POISON INTACTE (E1/E2/E3) ;
  V4 la falsification : (a) le source muté — la ligne diverge ET == le
     modèle du mutant ; (b) LA TABLE HEX DE LA PIÈCE MUTÉE — chaque ligne
     diverge : le juge attrape la pièce fausse (charte § 3) ;
  LES CONTRÔLES BINAIRES : PE32+ DLL x86-64, l'export UNIQUE
     loupe_08_ligne, AUCUN appel dans la clôture de la fonction
     (l'ASM désassemblé par capstone), les imports = l'affaire du
     démarreur CRT seul (nommé, jamais de la pièce).
"""
import ctypes
import hashlib
import mmap
import os
import pefile
import random
import struct
import sys

import capstone

ICI = os.path.dirname(os.path.abspath(__file__))
PIECE = os.path.join(ICI, "source", "loupe-08-c.dll")
GRAINE = 20261115
POISON = b"\xCC"

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
PROXY = os.path.join(REPO, "tls13", "proxy.exe")
TEMOIN_3F_LONGUEUR = 3 * 65536 + 1

VERTS, ROUGES = 0, 0


def controle(nom, ok, detail=""):
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}"
          + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


def modele_ligne(decalage: int, octets: bytes) -> bytes:
    s = f"{decalage:08X}  "
    g = [f"{b:02X}" if i < len(octets) else "  "
         for i, b in enumerate(octets + b"\x00" * (16 - len(octets)))]
    s += " ".join(g[:8]) + "  " + " ".join(g[8:]) + "  "
    miroir = "".join(chr(b) if 0x20 <= b <= 0x7E else "."
                     for b in octets[:16])
    s += miroir + " " * (16 - len(miroir))
    return s.encode("latin-1") + b"\x00"


def main() -> int:
    print("=== LE CONTRAT REJOUÉ AU POSIX — l'unité 4 (loupe-08 × bras C) : "
          "la dll mappée, l'export appelé NATURELLEMENT ===")

    # ---- LA CARTE DE LA PIÈCE (le chargeur du labo) -----------------------
    pe = pefile.PE(PIECE)
    base = pe.OPTIONAL_HEADER.ImageBase
    taille = pe.OPTIONAL_HEADER.SizeOfImage
    export = {(e.name.decode(), e.address)
              for e in pe.DIRECTORY_ENTRY_EXPORT.symbols}
    assert export == {("loupe_08_ligne", 0x1380)}, \
        f"les exports inattendus : {export}"

    # ---- LE MAPPAGE PAR SECTIONS (comme le chargeur, la base préférée) ---
    brut = open(PIECE, "rb").read()
    mmap_obj = mmap.mmap(-1, taille)
    mmap_obj.close()
    import ctypes as _ct
    libc = _ct.CDLL("libc.so.6", use_errno=True)
    libc.mmap.restype = _ct.c_void_p
    libc.mmap.argtypes = [_ct.c_void_p, _ct.c_size_t, _ct.c_int, _ct.c_int,
                          _ct.c_int, _ct.c_long]
    PROT_READ, PROT_WRITE, PROT_EXEC = 1, 2, 4
    MAP_PRIVATE, MAP_FIXED, MAP_ANONYMOUS = 2, 0x10, 0x20
    zone = libc.mmap(_ct.c_void_p(base), _ct.c_size_t(taille),
                     PROT_READ | PROT_WRITE | PROT_EXEC,
                     MAP_PRIVATE | MAP_FIXED | MAP_ANONYMOUS, -1, 0)
    if not zone or zone == -1:
        print(f"[REFUS] mmap à {base:#x} impossible "
              f"(errno {ctypes.get_errno()})")
        return 2
    for s in pe.sections:
        donnees = s.get_data()
        if donnees:
            ctypes.memmove(base + s.VirtualAddress, donnees, len(donnees))
    print(f"[mappage] l'image @ {base:#x} (la base préférée — AUCUN "
          f"relocation), les {len(pe.sections)} sections posées")

    # ---- L'ADAPTATEUR SysV→msx64 (le choc des ABI nommé) : ctypes appelle
    # en SysV (RDI RSI RDX RCX) ; la pièce mingw lit en msx64 (RCX RDX R8
    # R9). LE TRAMPOLINE réarrange les quatre registres puis saute — le
    # code de la pièce court NATURELLEMENT au CPU réel, l'appel du labo
    # adapté, jamais la pièce réécrite.
    ADAPT = (bytes.fromhex("4989d2")          # mov r10, rdx   (la sortie)
            + bytes.fromhex("4889f2")        # mov rdx, rsi   (la longueur)
            + bytes.fromhex("4d89d0")        # mov r8, r10    (la sortie)
            + bytes.fromhex("4989ca")        # mov r10, rcx   (le décalage)
            + bytes.fromhex("4889f9")        # mov rcx, rdi   (la source)
            + bytes.fromhex("4d89d1")        # mov r9, r10    (le décalage)
            + bytes.fromhex("49ba")
            + struct.pack("<Q", base + 0x1380)  # movabs r10, la pièce
            + bytes.fromhex("41ffe2"))       # jmp r10 — le retour direct
    tampon_adapt = ctypes.create_string_buffer(bytes(4096))
    adresse_adapt = ctypes.addressof(tampon_adapt)
    libc.mprotect(_ct.c_void_p(adresse_adapt & ~0xFFF), _ct.c_size_t(0x1000),
                  _ct.c_int(PROT_READ | PROT_WRITE | PROT_EXEC))
    ctypes.memmove(adresse_adapt, ADAPT, len(ADAPT))
    LOUPE08 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                               ctypes.c_uint64, ctypes.c_void_p,
                               ctypes.c_uint64)(adresse_adapt)
    print(f"[adaptateur] le trampoline SysV→msx64 posé @ {adresse_adapt:#x} "
          f"({len(ADAPT)} o) — la pièce appelée au CPU réel")

    def verdict(rax: int) -> int:
        v = rax & 0xFFFFFFFF
        return v - 0x100000000 if v > 0x7FFFFFFF else v

    source_buf = ctypes.create_string_buffer(16)
    sortie_buf = ctypes.create_string_buffer(96)

    def composer(source: bytes, longueur: int, decalage: int,
                 src_ptr=None, out_ptr=None):
        ctypes.memmove(source_buf, source, 16)
        ctypes.memmove(sortie_buf, POISON * 96, 96)
        r = LOUPE08(src_ptr if src_ptr is not None
                    else ctypes.cast(source_buf, ctypes.c_void_p),
                    longueur,
                    out_ptr if out_ptr is not None
                    else ctypes.cast(sortie_buf, ctypes.c_void_p),
                    decalage)
        brut96 = (ctypes.c_ubyte * 96)()
        ctypes.memmove(brut96, sortie_buf, 96)
        return verdict(r), bytes(brut96)

    # ---- V1 : LE DORÉ ------------------------------------------------------
    premiere = open(PROXY, "rb").read(16)
    r, ligne = composer(premiere, 16, 0)
    controle("V1:le-dore-proxy-premiere-ligne",
             r == 0 and ligne[:77] == modele_ligne(0, premiere)
             and ligne[77:] == POISON * 19,
             f"« {modele_ligne(0, premiere)[:32].decode('latin-1')}… »")

    rng3f = random.Random(20261107)        # la génération FIXE du labo
    _ = rng3f.randbytes(384)
    temoin3f = rng3f.randbytes(TEMOIN_3F_LONGUEUR)
    r, ligne = composer(temoin3f[-1:] + b"\x00" * 15, 1, 3 * 65536)
    controle("V1:le-temoin-3f-ligne-finale-incomplete",
             r == 0 and ligne[:77] == modele_ligne(3 * 65536, temoin3f[-1:])
             and ligne[77:] == POISON * 19,
             "UN octet valide : quinze groupes d'espaces, la colonne "
             "droite — Q3")

    # ---- V2 : LE DIFFÉRENTIEL — les MÊMES tirages que le juge T ------------
    rng = random.Random(GRAINE)
    ecarts, poison, source_intacte = 0, 0, 0
    for _ in range(10_000):
        decalage = rng.randrange(0, 0x8000_0000 // 16) * 16
        longueur = rng.randrange(1, 17)
        source = rng.randbytes(16)
        r, ligne = composer(source, longueur, decalage)
        if r != 0 or ligne[:77] != modele_ligne(decalage, source[:longueur]):
            ecarts += 1
        if ligne[77:] != POISON * 19:
            poison += 1
        if bytes((ctypes.c_ubyte * 16).from_buffer(source_buf)) != source:
            source_intacte += 1
    controle("V2:le-differentiel-10-000-lignes", ecarts == 0,
             f"{10_000 - ecarts}/10 000 == le modèle (la graine {GRAINE}, "
             "les MÊMES tirages que le juge T)")
    controle("V2:exactement-77-o", poison == 0,
             "le poison au-delà de 77 demeure (I2 : jamais un de plus)")
    controle("V2:la-source-lue-seule", source_intacte == 0,
             "les octets de la source INTACTS (I3)")

    # ---- V3 : LES REJETS ---------------------------------------------------
    source16 = bytes(range(0x10, 0x20))
    ctypes.memmove(source_buf, source16, 16)
    for nom, src, lon, srt in (
            ("E1:la-longueur-nulle", source_buf, 0, sortie_buf),
            ("E2:la-longueur-dix-sept", source_buf, 17, sortie_buf),
            ("E3:la-source-nulle", None, 5, sortie_buf),
            ("E3:la-sortie-nulle", source_buf, 5, None)):
        ctypes.memmove(sortie_buf, POISON * 96, 96)
        r = verdict(LOUPE08(ctypes.cast(src, ctypes.c_void_p)
                            if src is not None else None,
                            lon,
                            ctypes.cast(srt, ctypes.c_void_p)
                            if srt is not None else None,
                            0))
        brut96 = (ctypes.c_ubyte * 96)()
        ctypes.memmove(brut96, sortie_buf, 96)
        controle(f"V3:{nom}",
                 r == -5 and bytes(brut96) == POISON * 96,
                 f"verdict {r}, la sortie POISON INTACTE")

    # ---- V4 : LA FALSIFICATION ---------------------------------------------
    mutant = bytearray(premiere)
    mutant[3] ^= 0x6F
    mutant = bytes(mutant)
    r, ligne = composer(mutant, 16, 0)
    controle("V4:l-octet-mute-la-ligne-diverge",
             r == 0 and ligne[:77] != modele_ligne(0, premiere)
             and ligne[:77] == modele_ligne(0, mutant),
             "la ligne DIVERGE du modèle de l'original ET == le modèle du "
             "mutant — la pièce a lu SES octets")

    # (b) LA TABLE HEX DE LA PIÈCE MUTÉE : chaque ligne diverge — le juge
    # attrape la pièce fausse (la falsification demandée, le miroir du T)
    texte = pe.get_section_by_rva(
        pe.OPTIONAL_HEADER.DATA_DIRECTORY[6].VirtualAddress)  # .rdata heur.
    table_rva = None
    for s in pe.sections:
        donnees = s.get_data()
        off = donnees.find(b"0123456789ABCDEF\x00")
        if off != -1:
            table_rva = s.VirtualAddress + off
            break
    assert table_rva is not None, "la table HEX introuvable à la pièce"
    avant = bytes((ctypes.c_ubyte * 16).from_buffer_copy(
        ctypes.string_at(base + table_rva, 16)))
    ctypes.memmove(base + table_rva, b"#" * 16 + b"\x00", 16)
    pris = 0
    rng = random.Random(GRAINE + 1)
    for _ in range(50):
        decalage = rng.randrange(0, 0x8000_0000 // 16) * 16
        longueur = rng.randrange(1, 17)
        source = rng.randbytes(16)
        r, ligne = composer(source, longueur, decalage)
        if ligne[:77] != modele_ligne(decalage, source[:longueur]):
            pris += 1
    ctypes.memmove(base + table_rva, avant, 16)   # la table restaurée
    controle("V4:la-table-he-mutee-attrapee", pris == 50,
             "les 50 lignes de la pièce mutée DIVERGENT — la falsification "
             "DÉTECTABLE, la table restaurée le vert rendu")
    r, ligne = composer(premiere, 16, 0)
    controle("V4:la-piece-restauree-rejouee", r == 0
             and ligne[:77] == modele_ligne(0, premiere),
             "la ligne du doré rendue au retrait de la mutation")

    # ---- LES CONTRÔLES BINAIRES ---------------------------------------------
    controle("B1:pe32plus-dll-x86-64",
             pe.FILE_HEADER.Machine == 0x8664
             and pe.OPTIONAL_HEADER.Magic == 0x20B,
             f"machine {pe.FILE_HEADER.Machine:#x}, magic "
             f"{pe.OPTIONAL_HEADER.Magic:#x}")
    controle("B2:l-export-unique", export == {("loupe_08_ligne", 0x1380)},
             "loupe_08_ligne @ RVA 0x1380, AUCUNE autre")
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code = ctypes.string_at(base + 0x1380, 0x300)
    insns = list(cs.disasm(code, 0x1380))
    premier_ret = next(i.address + i.size for i in insns
                       if i.mnemonic == "ret")
    fermeture = [i for i in insns if i.address < premier_ret]
    appels = [i for i in fermeture if i.mnemonic in ("call", "jmp")
              and "ret" not in i.op_str]
    controle("B3:aucun-appel-dans-la-fermeture", not appels,
             f"{len(fermeture)} instructions jusqu'au premier ret, "
             f"{len(appels)} appel(s) — la feuille pure")
    controle("B4:les-imports-l-affaire-du-demarreur",
             all(nom.startswith("KERNEL32") or nom.startswith("msvcrt")
                 or nom.startswith("api-ms")
                 for nom in (e.dll.decode(errors="replace")
                             for e in pe.DIRECTORY_ENTRY_IMPORT)),
             "les feuilles déclarées servent DllMainCRTStartup seul — "
             "AUCUNE n'est dans la fermeture de la pièce")

    sha = hashlib.sha256(brut).hexdigest()
    print(f"\nla pièce : loupe-08-c.dll {len(brut)} o, sha256 {sha}")
    print(f"=== LE REJEU POSIX {VERTS} VERT, {ROUGES} ROUGE ===")
    return 0 if ROUGES == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
