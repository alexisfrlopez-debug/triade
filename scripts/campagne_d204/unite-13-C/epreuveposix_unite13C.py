#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuveposix_unite13C.py — LE CONTRAT REJOUÉ AU POSIX contre la pièce
même (l'unité 5, loupe-13 × bras C, la campagne D204). La dll est mappée par
sections comme le chargeur (RVA → adresse, la base préférée — AUCUN
relocation à appliquer), l'export loupe_13_recherche APPELÉ NATURELLEMENT
(LE TRAMPOLINE SysV→msx64 À CINQ ARGUMENTS : les quatre registres
réarrangés + le départ posé AU SLOT [rsp+0x28] — le choc des ABI nommé et
adapté, jamais la pièce réécrite) — le juge est le MODÈLE INDÉPENDANT.

  V1 le doré : LE CORPUS DE L'ÉCOLE (le premier octet, le dernier, à
     cheval sur le départ, l'occurrence DOUBLE, AAAA dans AAAAB, le
     presque-frère, le départ au milieu, la fenêtre vide, la plage vide,
     le motif trop long) + LES MARQUES DE PROXY.EXE SCELLÉ (MZ, PE,
     « This program » et « PEMax » les marques ABSENTES → LA FIN NOMMÉE) ;
  V2 le différentiel : 10 000 cas (la graine 20261115, les MÊMES tirages
     que le juge T), rax == bytes.find À L'IDENTIQUE y compris les -1 ;
     la fenêtre et le motif LUS SEULS (I3) ;
  V3 les rejets : le motif vide, le motif de 33 o, le départ au-delà →
     les TROIS -5 (E1/E2/E3) ;
  V4 la falsification : (a) LA FENÊTRE MUTÉE — la première occurrence
     détruite d'un octet : la réponse DIVERGE du modèle de l'original ET
     == le modèle du mutant (la pièce a lu SES octets) ; (b) LE PAS DE LA
     PIÈCE MUTÉ (add rbx, 1 → 2, l'octet @+0x13c3) : les 100 cas de
     l'école impairs TOUS divergents — le juge attrape la pièce fausse
     (charte § 3), le pas restauré rend le vert ;
  LES CONTRÔLES BINAIRES : PE32+ DLL x86-64, l'export UNIQUE
     loupe_13_recherche, LA LISTE D'APPELS FERMÉE dans la clôture (le
     seul appel : le memcmp de la bibliothèque par son thunk IAT — I2),
     les imports = l'affaire du démarreur CRT seul (nommé, jamais de la
     pièce).
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
from keystone import Ks, KS_ARCH_X86, KS_MODE_64

ICI = os.path.dirname(os.path.abspath(__file__))
PIECE = os.path.join(ICI, "source", "loupe-13-c.dll")
GRAINE = 20261115

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
PROXY = os.path.join(REPO, "tls13", "proxy.exe")

VERTS, ROUGES = 0, 0


def controle(nom, ok, detail=""):
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}"
          + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


def modele_recherche(fenetre: bytes, motif: bytes, depart: int) -> int:
    """LE MODÈLE INDÉPENDANT — la sémantique du contrat, jamais les octets
    de la pièce."""
    if len(motif) < 1 or len(motif) > 32:
        return -5
    if depart > len(fenetre):
        return -5
    if len(motif) > len(fenetre) - depart:
        return -1
    return fenetre.find(motif, depart)


def main() -> int:
    print("=== LE CONTRAT REJOUÉ AU POSIX — l'unité 5 (loupe-13 × bras C) : "
          "la dll mappée, l'export appelé NATURELLEMENT ===")

    # ---- LA CARTE DE LA PIÈCE (le chargeur du labo) -----------------------
    pe = pefile.PE(PIECE)
    base = pe.OPTIONAL_HEADER.ImageBase
    taille = pe.OPTIONAL_HEADER.SizeOfImage
    export = {(e.name.decode(), e.address)
              for e in pe.DIRECTORY_ENTRY_EXPORT.symbols}
    assert export == {("loupe_13_recherche", 0x1380)}, \
        f"les exports inattendus : {export}"
    print(f"[carte] loupe-13-c.dll : l'export UNIQUE loupe_13_recherche "
          f"@+0x1380, l'image {taille:#x} o à la base {base:#x}")

    brut = open(PIECE, "rb").read()
    mmap_obj = mmap.mmap(-1, taille)
    mmap_obj.close()
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    libc.mmap.restype = ctypes.c_void_p
    libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int,
                          ctypes.c_int, ctypes.c_int, ctypes.c_long]
    PROT_READ, PROT_WRITE, PROT_EXEC = 1, 2, 4
    MAP_PRIVATE, MAP_FIXED, MAP_ANONYMOUS = 2, 0x10, 0x20
    zone = libc.mmap(ctypes.c_void_p(base), ctypes.c_size_t(taille),
                     PROT_READ | PROT_WRITE | PROT_EXEC,
                     MAP_PRIVATE | MAP_FIXED | MAP_ANONYMOUS, -1, 0)
    if not zone or zone == -1:
        print(f"[REFUS] mmap à {base:#x} impossible "
              f"(errno {ctypes.get_errno()})")
        return 2
    # les EN-TÊTES D'ABORD (le vrai chargeur les mappe — le bloc découverte
    # livré lit la table d'exports dans l'image mappée même)
    ctypes.memmove(base, brut[:pe.OPTIONAL_HEADER.SizeOfHeaders],
                   pe.OPTIONAL_HEADER.SizeOfHeaders)
    for s in pe.sections:
        donnees = s.get_data()
        if donnees:
            ctypes.memmove(base + s.VirtualAddress, donnees, len(donnees))
    print(f"[mappage] l'image @ {base:#x} (la base préférée — AUCUN "
          f"relocation), les {len(pe.sections)} sections posées")

    # ---- LE SHIM MEMCMP (la feuille unique de la liste fermée) : la pièce
    # appelle le memcmp DE LA BIBLIOTHÈQUE par son thunk IAT — le thunk saute
    # au slot brut de l'image (jamais résolu hors Windows). LE LABO SERT LA
    # FEUILLE (la discipline des shims du harnais, charte § 9) : un shim
    # msx64→SysV réarrange (rcx, rdx, r8) → (rdi, rsi, rdx) et appelle LE
    # VRAI memcmp de la libc du labo — la comparaison par la bibliothèque,
    # deux fois (la pièce par l'IAT, le shim par la libc). LA CONVENTION
    # TENUE : RDI ET RSI SONT NON-VOLATILS EN msx64 (la pièce y garde ses
    # invariants à travers l'appel) — le shim les SAUVE ET LES REND,
    # l'alignement du call SysV compté (deux pushes + 8 ≡ l'entrée libc).
    libc_memcmp = ctypes.cast(libc.memcmp, ctypes.c_void_p).value
    ks = Ks(KS_ARCH_X86, KS_MODE_64)   # l'assembleur du labo (shim + trampoline)
    shim_asm = (
        "push rdi\n"                # non-volatif msx64 — sauvé, rendu
        "push rsi\n"                # idem
        "sub rsp, 8\n"              # l'alignement du call SysV
        "mov rdi, rcx\n"            # ptr1 (msx64 rcx → SysV rdi)
        "mov rsi, rdx\n"            # ptr2
        "mov rdx, r8\n"             # le compte
        f"mov rax, {libc_memcmp:#x}\n"
        "call rax\n"
        "add rsp, 8\n"
        "pop rsi\n"
        "pop rdi\n"
        "ret\n")
    SHIM, _ = ks.asm(shim_asm)
    SHIM = bytes(SHIM)
    tampon_shim = ctypes.create_string_buffer(bytes(4096))
    adresse_shim = ctypes.addressof(tampon_shim)
    libc.mprotect(ctypes.c_void_p(adresse_shim & ~0xFFF),
                  ctypes.c_size_t(0x1000),
                  ctypes.c_int(PROT_READ | PROT_WRITE | PROT_EXEC))
    ctypes.memmove(adresse_shim, SHIM, len(SHIM))
    # LE SLOT IAT de msvcrt ! memcmp REPOINTÉ au shim (le chargeur du labo) —
    # pefile rend l'adresse VIRTUELLE (la base préférée + la RVA) : c'est
    # DÉJÀ l'adresse absolue de l'image mappée à sa base préférée
    slot_memcmp = None
    for desc in pe.DIRECTORY_ENTRY_IMPORT:
        for entree in desc.imports:
            if entree.name and entree.name.decode() == "memcmp":
                slot_memcmp = entree.address        # la VA du slot IAT
    assert slot_memcmp is not None, "le slot IAT de memcmp introuvable"
    assert base <= slot_memcmp < base + taille, \
        f"le slot {slot_memcmp:#x} hors de l'image mappée"
    ctypes.memmove(slot_memcmp, struct.pack("<Q", adresse_shim), 8)
    print(f"[shim] memcmp servi @ {adresse_shim:#x} ({len(SHIM)} o, "
          f"msx64→SysV → la libc du labo), le slot IAT @"
          f"{slot_memcmp - base:+#x} repointé — la feuille unique de la "
          f"liste fermée")

    # ---- L'ADAPTATEUR SysV→msx64 À CINQ ARGUMENTS (le choc des ABI nommé) :
    # ctypes appelle en SysV (RDI RSI RDX RCX R8) ; la pièce mingw lit en
    # msx64 (RCX RDX R8 R9 + le 5e À LA PILE [rsp+0x28]). LE TRAMPOLINE
    # réarrange les quatre registres, pose le départ au slot msx64 du 5e,
    # donne l'ombre 0x20 à l'appelé — le code de la pièce court
    # NATURELLEMENT au CPU réel, l'appel du labo adapté, jamais la pièce
    # réécrite.
    R_EXPORT = 0x1380
    trampoline_asm = (
        "mov r11, r8\n"              # le départ (le 5e SysV)
        "mov r8, rdx\n"              # le motif
        "mov rdx, rsi\n"             # la taille
        "mov r9, rcx\n"              # la taille du motif
        "mov rcx, rdi\n"             # la fenêtre
        "sub rsp, 0x28\n"            # l'ombre de l'appelé + le slot du 5e
        "mov qword ptr [rsp + 0x20], r11\n"   # le départ au slot msx64
        f"mov r10, {base + R_EXPORT:#x}\n"    # la pièce
        "call r10\n"
        "add rsp, 0x28\n"
        "ret\n")
    ADAPT, _ = ks.asm(trampoline_asm)
    ADAPT = bytes(ADAPT)
    tampon_adapt = ctypes.create_string_buffer(bytes(4096))
    adresse_adapt = ctypes.addressof(tampon_adapt)
    libc.mprotect(ctypes.c_void_p(adresse_adapt & ~0xFFF),
                  ctypes.c_size_t(0x1000),
                  ctypes.c_int(PROT_READ | PROT_WRITE | PROT_EXEC))
    ctypes.memmove(adresse_adapt, ADAPT, len(ADAPT))
    LOUPE13 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                               ctypes.c_uint64, ctypes.c_void_p,
                               ctypes.c_uint64,
                               ctypes.c_uint64)(adresse_adapt)
    print(f"[adaptateur] le trampoline SysV→msx64 à cinq arguments posé @ "
          f"{adresse_adapt:#x} ({len(ADAPT)} o) — la pièce appelée au CPU "
          f"réel, le départ au slot [rsp+0x28]")

    def verdict(rax: int) -> int:
        v = rax & 0xFFFFFFFF
        return v - 0x100000000 if v > 0x7FFFFFFF else v

    fenetre_buf = ctypes.create_string_buffer(8200)   # 4 096 du plan + le
    motif_buf = ctypes.create_string_buffer(40)       # témoin proxy 8 192

    def chercher(fenetre: bytes, motif: bytes, depart: int):
        ctypes.memmove(fenetre_buf, fenetre, len(fenetre))
        ctypes.memmove(motif_buf, motif, len(motif))
        r = LOUPE13(ctypes.cast(fenetre_buf, ctypes.c_void_p),
                    len(fenetre),
                    ctypes.cast(motif_buf, ctypes.c_void_p),
                    len(motif), depart)
        return verdict(r)

    # ---- V1 : LE DORÉ — l'école + les marques du scellé --------------------
    ecole = [
        (b"premiere-occurrence", b"premiere", 0, 0),
        (b"premiere-occurrence", b"occurrence", 0, 9),
        (b"XXabcYY", b"abc", 2, 2),
        (b"abcXabc", b"abc", 0, 0),
        (b"AAAAB", b"AAAA", 0, 0),
        (b"AAAAB", b"AAAB", 0, 1),
        (b"abcabcabc", b"abc", 4, 6),
        (b"", b"A", 0, -1),
        (b"abc", b"abc", 3, -1),
        (b"abcd", b"cdef", 2, -1),
    ]
    ecarts = [(f, m, d, chercher(f, m, d)) for f, m, d, a in ecole
              if chercher(f, m, d) != a]
    controle("V1:le-corpus-de-l-ecole", not ecarts,
             f"{len(ecole) - len(ecarts)}/{len(ecole)} == le modèle (le "
             "premier octet, le dernier, à cheval sur le départ, "
             "l'occurrence DOUBLE — LA PREMIÈRE, AAAA dans AAAAB, le "
             "presque-frère, le départ au milieu, la fenêtre vide, la "
             "plage vide, le motif trop long)"
             + (f" — ÉCARTS : {ecarts}" if ecarts else ""))

    proxy8k = open(PROXY, "rb").read(8192)
    marques = [(b"MZ", proxy8k.find(b"MZ")),
               (b"PE\x00\x00", proxy8k.find(b"PE\x00\x00")),
               (b"This program", proxy8k.find(b"This program")),
               (b"PEMax", proxy8k.find(b"PEMax"))]
    ecarts_m = [(m, a, chercher(proxy8k, m, 0)) for m, a in marques
                if chercher(proxy8k, m, 0) != a]
    controle("V1:les-marques-de-proxy", not ecarts_m,
             f"MZ @0, PE @+{marques[1][1]}, « This program » et « PEMax » "
             "les marques ABSENTES du scellé → -1 LA FIN NOMMÉE"
             + (f" — ÉCARTS : {ecarts_m}" if ecarts_m else ""))

    # ---- V2 : LE DIFFÉRENTIEL — les MÊMES tirages que le juge T ------------
    rng = random.Random(GRAINE)
    ecarts, lecture = 0, 0
    for _ in range(10_000):
        n = rng.randrange(0, 4097)
        pauvre = rng.randrange(2)
        alphabet = b"AB" if pauvre else bytes(range(256))
        fenetre = bytes(alphabet[rng.randrange(len(alphabet))]
                        for _ in range(n))
        m = rng.randrange(1, 33)
        motif = bytes(alphabet[rng.randrange(len(alphabet))]
                      for _ in range(m))
        depart = rng.randrange(0, n + 1) if n else 0
        r = chercher(fenetre, motif, depart)
        if r != modele_recherche(fenetre, motif, depart):
            ecarts += 1
            if ecarts <= 3:
                print(f"    écart : n={n} m={m} départ={depart} → {r}")
        if bytes((ctypes.c_ubyte * len(fenetre))
                 .from_buffer(fenetre_buf, 0))[:len(fenetre)] != fenetre \
                or bytes((ctypes.c_ubyte * len(motif))
                         .from_buffer(motif_buf, 0))[:len(motif)] != motif:
            lecture += 1
    controle("V2:le-differentiel-10-000-cas", ecarts == 0,
             f"{10_000 - ecarts}/10 000 == le modèle (la graine {GRAINE}, "
             "les MÊMES tirages que le juge T, y compris les -1)")
    controle("V2:la-fenetre-et-le-motif-lus-seuls", lecture == 0,
             "les octets de la fenêtre et du motif INTACTS (I3 — la pureté)")

    # ---- V3 : LES REJETS ----------------------------------------------------
    fenetre4 = b"ABCD"
    for nom, motif, depart in (
            ("E1:le-motif-vide", b"", 0),
            ("E2:le-motif-de-trente-trois", b"X" * 33, 0),
            ("E3:le-depart-au-dela", b"A", 5)):
        r = chercher(fenetre4, motif, depart)
        controle(f"V3:{nom}", r == -5,
                 f"verdict {r} — chercher rien n'est pas chercher ; la "
                 "borne MOTIF_MAX ; le départ est une position, pas un vœu")

    # ---- V4 : LA FALSIFICATION ---------------------------------------------
    # (a) LA FENÊTRE MUTÉE — la première occurrence détruite d'un octet :
    # la réponse DIVERGE du modèle de l'original ET == le modèle du mutant
    original = b"AB" + b"MZ" + b"CD" + b"MZ" + b"EF"      # la 1re @2, la 2de @6
    mutant = original[:3] + b"X" + original[4:]            # la 1re détruite
    r_original = chercher(original, b"MZ", 0)
    r_mutant = chercher(mutant, b"MZ", 0)
    controle("V4:la-fenetre-mutee-attrapee",
             r_original == 2 and r_mutant == 6
             and r_mutant != modele_recherche(original, b"MZ", 0)
             and r_mutant == modele_recherche(mutant, b"MZ", 0),
             f"l'original rend 2 (la première), le mutant rend 6 (la "
             "seconde — la première détruite d'un octet) : la pièce a lu "
             "SES octets, la différentielle attrape le faux")

    # (b) LE PAS DE LA PIÈCE MUTÉ — add rbx, 1 → 2 (l'octet @+0x13c3) :
    # les candidats impairs JAMAIS visités — les 100 cas de l'école
    # impairs TOUS divergents, le pas restauré rend le vert
    site = base + R_EXPORT + (0x13C3 - 0x1380)
    octet_juste = ctypes.string_at(site, 1)
    assert octet_juste == b"\x01", \
        f"l'octet @+0x13c3 != 0x01 (le pas du add rbx, 1) : {octet_juste!r}"
    ctypes.memmove(site, b"\x02", 1)          # le pas muté : 1 → 2
    pris = 0
    for k in range(100):
        fen = b"\x00" + b"AB" + bytes(2 * k + 1) + b"\x00" + b"\x00"
        # le motif « AB » à l'indice IMPAIR 1, seul de la fenêtre : le pas
        # de 2 ne visite que les candidats pairs — l'occurrence est sautée
        attendu = fen.find(b"AB", 0)
        r = chercher(fen, b"AB", 0)
        if attendu == 1 and r != attendu:
            pris += 1
    ctypes.memmove(site, octet_juste, 1)      # le pas restauré
    r_rendu = chercher(b"xAB", b"AB", 0)
    controle("V4:le-pas-de-la-piece-mute", pris == 100 and r_rendu == 1,
             f"les {pris}/100 cas de l'école impairs DIVERGENT (le motif "
             "au candidat impair, le pas de 2 ne le visite jamais) — le "
             "juge attrape la pièce fausse ; le pas restauré rend le vert "
             "(xAB → 1)")

    # ---- LES CONTRÔLES BINAIRES --------------------------------------------
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code = bytes(ctypes.string_at(base + R_EXPORT, 0x80))
    appels = [i for i in md.disasm(code, R_EXPORT) if i.mnemonic == "call"]
    controle("B:la-liste-d-appels-fermee", len(appels) == 1
             and appels[0].op_str == "0x2398",
             f"{len(appels)} appel dans la clôture : le thunk memcmp de "
             "la bibliothèque (I2 — jamais une boucle de comparaison "
             "réécrite), les imports KERNEL32/msvcrt servent le "
             "démarreur CRT du lieur seul")
    pe2 = pefile.PE(data=brut)
    controle("B:pe32plus-dll-x86-64",
             pe2.FILE_HEADER.Machine == 0x8664
             and bool(pe2.FILE_HEADER.Characteristics & 0x2000)
             and pe2.OPTIONAL_HEADER.Magic == 0x20b,
             "PE32+ DLL x86-64, l'export UNIQUE loupe_13_recherche")

    print(f"\n=== LE POSIX {VERTS} VERT, {ROUGES} ROUGE ===")
    return 0 if ROUGES == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
