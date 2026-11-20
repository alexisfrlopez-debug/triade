#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""porteuse_meson.py — LE RIG DE LA BOUCLE PORTEUSE RESTRUCTURÉE (ahult8jgd) :
les TROIS variantes v3 (la table d'adresses précalculée ; le déroulage k=4 ;
l'inlining du bloc NI au mode d'adressage [r13 + rax*8]) contre la référence
v2 (la boucle à registres porteurs, 54 cycles/bloc enveloppe comprise au rig
8z4hj76w4) et le scellé tls13-16 appelé par bloc — LA CIBLE ≤ 12 cycles/bloc
ENVELOPPE COMPRISE.

LA PARITÉ OBSERVABLE : le calendrier des clés par LE SCELLÉ tls13-15 confronté
au juge python (FIPS 197 §5.2) ; le vecteur FIPS 197 C.1 ; la différentielle
64/64 ET 256/256 octet pour octet contre le scellé appelé par bloc ; les repli
forcés (le jz → jmp du laboratoire, le scellé intact) ; le contrôle négatif
(l'octet muté du déroulé) ; la borne N ≤ 256 fail-closed.

LA MESURE : RDTSCP, l'affinité au cœur 1, n=20 par cellule (≥20 exigé), la
médiane et l'IQR (q3−q1 empirique = s[15]−s[4]), la même machine (le bac
Xeon 3200 MHz, constant_tsc, aes — les drapeaux consignés au rapport).

LE SCELLÉ INTACT : les variantes vivent à la marge VIERGE (0xD200/0xD400/
0xD800, les copies de sonde à 0xE000+), le scellé tls13-16 assemblé à SON
slot 0xDF00 puis posé en copie de laboratoire à 0xC400 — la convention du rig
8z4hj76w4 reprise telle quelle (octets position-indépendants : aucun
déplacement RIP ni appel interne au bloc).

Sortie : native/porteuse_rig.c · registres/porteuse-meson.json ·
rapport-porteuse-meson.txt (le rapport final assemblé à la main dans
rapport-porteuse.txt)."""
from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-porteuse-ahult8jgd"
sys.path.insert(0, str(REPO / "loupe"))
BUILD = ICI / "native"
BUILD.mkdir(exist_ok=True)
REG = ICI / "registres"
REG.mkdir(exist_ok=True)

import capstone  # noqa: E402
import keystone  # noqa: E402

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

# ---- la marge du laboratoire (VIERGE, documentée) ---------------------------
# 0xC080  la copie du scellé tls13-15 (assemblé à son slot 0xDCC0)
# 0xC400  la copie du scellé tls13-16 (assemblé à son slot 0xDF00)
# 0xCE00  le corps NI pur (labo v2 — la cible des appels des variantes à appel)
# 0xCF00  le flux v2 (la référence AVANT, labo 8z4hj76w4)
# 0xD200  v3-table   0xD400  v3-deroule   0xD800  v3-inline
# 0xDC00  v4-appel (la porteuse nue à appel)   0xDE00  v4-inline (la nue inlinée)
# 0xF400  le creux de calibration (le squelette sans crypto)
# 0xE400  le mutant (1 octet)   0xE800/0xEB00/0xED00  les repli forcés
# 0xF000  le stub ret (la calibration de l'enveloppe msx64)
RVA = {"tls15": 0xC080, "tls16": 0xC400, "pur": 0xCE00, "flux2": 0xCF00,
       "v3t": 0xD200, "v3d": 0xD400, "v3i": 0xD800,
       "v4a": 0xDC00, "v4i": 0xDE00, "creux": 0xF400,
       "mut": 0xE400, "frep_i": 0xE800, "frep_t": 0xEB00, "frep_d": 0xED00,
       "stub": 0xF000}


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def assembler(fichier: pathlib.Path, rva: int, subst: dict[str, str] | None = None):
    """L'assemblage maison (les étiquettes en PASSES — le format du rig
    8z4hj76w4/temps_reel.py, repris TEL QUEL ; subst : les substitutions de
    laboratoire une ligne pour une ligne, consignées)."""
    lignes = [l.split(";")[0] for l in fichier.read_text(
        encoding="utf-8").splitlines()]
    if subst:
        lignes = [subst.get(l.strip(), l) for l in lignes]
    etiquettes: dict[str, int] = {}
    corps_list = []
    for _ in range(4):
        adr = rva
        corps_list = []
        for l in lignes:
            l = l.strip()
            if not l:
                continue
            if l.endswith(":") and l.startswith("."):
                etiquettes[l[:-1]] = adr
                continue
            corps = l
            for e, a in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
                corps = corps.replace(e, hex(a))
            corps_list.append((corps, adr))
            try:
                c, _ = KS.asm(corps, adr)
                adr += len(bytes(c))
            except Exception:
                adr += 6
    octets = b""
    for corps, adr in corps_list:
        for e, a in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
            corps = corps.replace(e, hex(a))
        c, _ = KS.asm(corps, rva + len(octets))
        octets += bytes(c)
    return octets


def ctable(nom: str, octets: bytes) -> str:
    lignes = []
    for i in range(0, len(octets), 16):
        chunk = octets[i:i + 16]
        lignes.append("  " + ", ".join(f"0x{b:02x}" for b in chunk) + ",")
    return f"static const unsigned char {nom}[] = {{\n" + "\n".join(lignes) + "\n};\n"


# ---- le juge python du calendrier (FIPS 197 §5.2, dérivé par le code) -------
def _gmul(a: int, b: int) -> int:
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p


def _sbox() -> list[int]:
    sbox = []
    for a in range(256):
        if a == 0:
            inv = 0
        else:
            inv = next(b for b in range(1, 256) if _gmul(a, b) == 1)
        s = 0
        for i in range(8):
            bit = ((inv >> i) ^ (inv >> ((i + 4) % 8)) ^ (inv >> ((i + 5) % 8))
                   ^ (inv >> ((i + 6) % 8)) ^ (inv >> ((i + 7) % 8))
                   ^ (0x63 >> i)) & 1
            s |= bit << i
        sbox.append(s)
    return sbox


def expansion_aes128(cle: bytes) -> bytes:
    """Le calendrier FIPS 197 §5.2 — 176 octets, l'ordre des mots DU BLOC
    scellé (rk[j] = w4j..w4j+3 en octets, miroir du geste tls13-15)."""
    assert len(cle) == 16
    S = _sbox()
    assert S[0x00] == 0x63 and S[0x01] == 0x7C and S[0x53] == 0xED
    RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
    w = [list(cle[4 * i:4 * i + 4]) for i in range(4)]
    for i in range(4, 44):
        t = list(w[i - 1])
        if i % 4 == 0:
            t = [S[t[1]] ^ RCON[i // 4 - 1], S[t[2]], S[t[3]], S[t[0]]]
        w.append([w[i - 4][k] ^ t[k] for k in range(4)])
    return bytes(b for mot in w for b in mot)


# FIPS 197 Appendice C.1 (AES-128) — le vecteur officiel
FIPS_CLE = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
FIPS_CLAIR = bytes.fromhex("3243f6a8885a308d313198a2e0370734")
FIPS_CHIFFRE = bytes.fromhex("3925841d02dc09fbdc118597196a0b32")


def main() -> int:
    # ---- les octets : les scellés par LE lecteur canonique B4 ----------------
    sys.path.insert(0, str(REPO / "m4"))
    sys.path.insert(0, str(REPO / "tls13"))
    B4 = charger_module("b4_pr", REPO / "m4" / "build_m4.py")
    lay = charger_module("lay_pr", REPO / "tls13" / "layout.py")
    not15 = REPO / "tls13" / "notation" / "tls13-15-aes128-cles-tour.asm"
    not16 = REPO / "tls13" / "notation" / "tls13-16-aes128-bloc.asm"
    o15, m15 = B4.assembler_bloc(KS, str(not15), *lay.SLOTS_TLS13["h100015"])
    o16, m16 = B4.assembler_bloc(KS, str(not16), *lay.SLOTS_TLS13["h100016"])

    # ---- les octets : les copies de laboratoire (les notations de l'atelier) --
    NOT = ICI / "notation"
    o_pur = assembler(NOT / "tls13-16-ni-v2-pur.asm", RVA["pur"])
    o_flux2 = assembler(NOT / "tls13-16-ni-v2-flux.asm", RVA["flux2"])
    o_v3t = assembler(NOT / "tls13-16-ni-v3-table.asm", RVA["v3t"])
    o_v3d = assembler(NOT / "tls13-16-ni-v3-deroule.asm", RVA["v3d"])
    o_v3i = assembler(NOT / "tls13-16-ni-v3-inline.asm", RVA["v3i"])
    o_v4a = assembler(NOT / "tls13-16-ni-v4-appel.asm", RVA["v4a"])
    o_v4i = assembler(NOT / "tls13-16-ni-v4-inline.asm", RVA["v4i"])
    o_creux = assembler(NOT / "tls13-16-ni-v4-creux.asm", RVA["creux"])

    # les repli forcés : le jz → jmp DU LABORATOIRE (le scellé intact — la
    # substitution consignée, une ligne pour une ligne)
    subst = {"jz .repli_boucle": "jmp .repli_boucle"}
    o_frep_i = assembler(NOT / "tls13-16-ni-v3-inline.asm", RVA["frep_i"], subst)
    o_frep_t = assembler(NOT / "tls13-16-ni-v3-table.asm", RVA["frep_t"], subst)
    o_frep_d = assembler(NOT / "tls13-16-ni-v3-deroule.asm", RVA["frep_d"], subst)

    # le mutant : UN octet du déroulé (le déplacement 0x90 → 0x91 d'une clé de
    # tour — l'octet bas du disp32 de la DERNIÈRE lecture [r12 + 0x90])
    mut = bytearray(o_v3i)
    cible = None
    for ins in CS.disasm(bytes(mut), RVA["v3i"]):
        if (ins.mnemonic == "movdqu"
                and ins.op_str == "xmm4, xmmword ptr [r12 + 0x90]"):
            cible = ins.address - RVA["v3i"] + ins.size - 4
    assert cible is not None, "la lecture [r12 + 0x90] introuvable"
    assert bytes(mut[cible:cible + 4]) == bytes.fromhex("90000000")
    mut[cible] = 0x91
    o_mut = bytes(mut)

    # le round-trip octet (keystone == capstone == keystone, le geste du rig
    # d'instructions 8z4hj76w4 — les étiquettes contournées par l'octet juge)
    rt = {}
    for nom, octets, rva in [("v3t", o_v3t, RVA["v3t"]),
                             ("v3d", o_v3d, RVA["v3d"]),
                             ("v3i", o_v3i, RVA["v3i"]),
                             ("v4a", o_v4a, RVA["v4a"]),
                             ("v4i", o_v4i, RVA["v4i"]),
                             ("creux", o_creux, RVA["creux"]),
                             ("frep_i", o_frep_i, RVA["frep_i"]),
                             ("frep_t", o_frep_t, RVA["frep_t"]),
                             ("frep_d", o_frep_d, RVA["frep_d"]),
                             ("flux2", o_flux2, RVA["flux2"])]:
        ok = True
        for ins in CS.disasm(octets, rva):
            c, _ = KS.asm(f"{ins.mnemonic} {ins.op_str}", ins.address)
            if bytes(c) != octets[ins.address - rva:
                                  ins.address - rva + ins.size]:
                ok = False
                break
        rt[nom] = ok

    # le calendrier attendu (le juge python)
    rk_attendu = expansion_aes128(FIPS_CLE)
    assert rk_attendu[16:20] == bytes.fromhex("a0fafe17")  # C.1 : w4 — la
    # contre-preuve du juge lui-même (la première clé de tour du vecteur)

    # ---- le recouvrement des marges (aucun chevauchement, vérifié) -----------
    posees = [(RVA[k], RVA[k] + len(v)) for k, v in
              [("tls15", o15), ("tls16", o16), ("pur", o_pur),
               ("flux2", o_flux2), ("v3t", o_v3t), ("v3d", o_v3d),
               ("v3i", o_v3i), ("v4a", o_v4a), ("v4i", o_v4i),
               ("mut", o_mut), ("frep_i", o_frep_i),
               ("frep_t", o_frep_t), ("frep_d", o_frep_d),
               ("creux", o_creux)]]
    for i, (a1, b1) in enumerate(posees):
        for j, (a2, b2) in enumerate(posees):
            if i != j and a1 < b2 and a2 < b1:
                raise RuntimeError(f"marges chevauchées {a1:#x}-{b1:#x} / "
                                   f"{a2:#x}-{b2:#x}")

    # ---- le rig C --------------------------------------------------------------
    rig = r"""/* porteuse_rig.c — LE RIG DE LA PORTEUSE (ahult8jgd) — généré par
   porteuse_meson.py (jamais écrit à la main : les octets des notations
   EMBARQUÉS des fichiers, le scellé assemblé par le lecteur canonique B4). */
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <sys/mman.h>

/* ---- les notations embarquées (les copies de laboratoire) ----------------- */
%%TABLES%%

static void pose_page(unsigned long base, size_t taille) {
    void *p = mmap((void*)base, taille, PROT_READ|PROT_WRITE|PROT_EXEC,
                   MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); exit(3); }
}

/* l'appelant msx64 (le geste du rig 8z4hj76w4, repris tel quel) */
static long appeler_msx64(unsigned long fn, unsigned long rcx_v,
                          unsigned long rdx_v, unsigned long r8_v,
                          unsigned long r9_v, unsigned long pile_v) {
    long ret;
    __asm__ volatile(
        "subq $0x30, %%rsp\n\t"
        "movq %6, 0x20(%%rsp)\n\t"
        "movq %2, %%rcx\n\t"
        "movq %3, %%rdx\n\t"
        "movq %4, %%r8\n\t"
        "movq %5, %%r9\n\t"
        "callq *%1\n\t"
        "movq %%rax, %0\n\t"
        "addq $0x30, %%rsp\n\t"
        : "=r"(ret)
        : "r"(fn), "r"(rcx_v), "r"(rdx_v), "r"(r8_v), "r"(r9_v),
          "r"(pile_v)
        : "rax", "rcx", "rdx", "r8", "r9", "r10", "r11", "memory");
    return ret;
}

static uint64_t rdtscp_(void) {
    uint32_t lo, hi, aux;
    __asm__ volatile("rdtscp" : "=a"(lo), "=d"(hi), "=c"(aux) :: "memory");
    return ((uint64_t)hi << 32) | lo;
}

/* la série (le rig 8z4hj76w4 : la graine 20261120 reproduite par xorshift) */
static uint64_t xs = 20261120ULL;
static unsigned char rnd(void) {
    xs ^= xs << 13; xs ^= xs >> 7; xs ^= xs << 17;
    return (unsigned char)(xs >> 32);
}

typedef long (*fn_flux)(unsigned long, unsigned long, unsigned long,
                        unsigned long);
static long flux_v2(unsigned long rk, unsigned long in, unsigned long out,
                    unsigned long n) {
    return appeler_msx64(0xCF00, rk, in, out, n, 0);
}
static long flux_v3t(unsigned long rk, unsigned long in, unsigned long out,
                     unsigned long n) {
    return appeler_msx64(0xD200, rk, in, out, n, 0);
}
static long flux_v3d(unsigned long rk, unsigned long in, unsigned long out,
                     unsigned long n) {
    return appeler_msx64(0xD400, rk, in, out, n, 0);
}
static long flux_v3i(unsigned long rk, unsigned long in, unsigned long out,
                     unsigned long n) {
    return appeler_msx64(0xD800, rk, in, out, n, 0);
}
static long flux_frep_i(unsigned long rk, unsigned long in,
                        unsigned long out, unsigned long n) {
    return appeler_msx64(0xE800, rk, in, out, n, 0);
}
static long flux_frep_t(unsigned long rk, unsigned long in,
                        unsigned long out, unsigned long n) {
    return appeler_msx64(0xEB00, rk, in, out, n, 0);
}
static long flux_frep_d(unsigned long rk, unsigned long in,
                        unsigned long out, unsigned long n) {
    return appeler_msx64(0xED00, rk, in, out, n, 0);
}
static long flux_mut(unsigned long rk, unsigned long in, unsigned long out,
                     unsigned long n) {
    return appeler_msx64(0xE400, rk, in, out, n, 0);
}
static long flux_v4a(unsigned long rk, unsigned long in, unsigned long out,
                     unsigned long n) {
    return appeler_msx64(0xDC00, rk, in, out, n, 0);
}
static long flux_v4i(unsigned long rk, unsigned long in, unsigned long out,
                     unsigned long n) {
    return appeler_msx64(0xDE00, rk, in, out, n, 0);
}
static long flux_creux(unsigned long rk, unsigned long in, unsigned long out,
                       unsigned long n) {
    return appeler_msx64(0xF400, rk, in, out, n, 0);
}

/* le cpuid nu (la forme exacte du sondage : eax=1, ecx=0 — l'éléphant
   mesuré directement, le virtualisateur du bac paie l'interception) */
static void cpuid_n(int n) {
    for (int i = 0; i < n; ++i) {
        unsigned a, b, c, d;
        __asm__ volatile("cpuid" : "=a"(a), "=b"(b), "=c"(c), "=d"(d)
                                : "a"(1u), "c"(0u));
    }
}

/* le juge : le scellé tls13-16 APPELÉ PAR BLOC depuis le C (la boucle du
   compilateur — les adresses indépendantes par bloc, la référence 8/bloc) */
static void scelle_par_bloc(unsigned long rk, const unsigned char *in,
                            unsigned char *out, long n) {
    for (long b = 0; b < n; ++b)
        appeler_msx64(0xC400, rk, (unsigned long)(in + b*16),
                      (unsigned long)(out + b*16), 0, 0);
}

static int egal(const unsigned char *a, const unsigned char *b, long n) {
    return memcmp(a, b, (size_t)n) == 0;
}

int main(void) {
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(1, &m);
    if (sched_setaffinity(0, sizeof(m), &m) != 0) perror("affinité");

    pose_page(0xC000, 0x4000);
    memcpy((void*)0xC080, tls15, sizeof(tls15));
    memcpy((void*)0xC400, tls16, sizeof(tls16));
    memcpy((void*)0xCE00, pur, sizeof(pur));
    memcpy((void*)0xCF00, flux2, sizeof(flux2));
    memcpy((void*)0xD200, v3t, sizeof(v3t));
    memcpy((void*)0xD400, v3d, sizeof(v3d));
    memcpy((void*)0xD800, v3i, sizeof(v3i));
    memcpy((void*)0xDC00, v4a, sizeof(v4a));
    memcpy((void*)0xDE00, v4i, sizeof(v4i));
    memcpy((void*)0xE400, mut, sizeof(mut));
    memcpy((void*)0xE800, frep_i, sizeof(frep_i));
    memcpy((void*)0xEB00, frep_t, sizeof(frep_t));
    memcpy((void*)0xED00, frep_d, sizeof(frep_d));
    memcpy((void*)0xF400, creux, sizeof(creux));
    *(unsigned char *)0xF000 = 0xC3;
    __builtin___clear_cache((char*)0xC000, (char*)0x10000);

    /* (0) LE CALENDRIER : le scellé tls13-15 confronté au juge python
       (FIPS 197 §5.2 — les 176 octets attendus embarqués) */
    unsigned char *RK = malloc(176);
    %%RK_ATTENDU%%
    appeler_msx64(0xC080, (unsigned long)FIPS_CLE, (unsigned long)RK, 0, 0, 0);
    printf("CALENDRIER %d\n", egal(RK, RK_ATTENDU, 176));

    /* (1) LE VECTEUR FIPS 197 C.1 : le scellé, le flux v2, les trois v3,
       les repli forcés — le même chiffre attendu */
    unsigned char *CT = malloc(16);
    appeler_msx64(0xC400, (unsigned long)RK, (unsigned long)FIPS_CLAIR,
                  (unsigned long)CT, 0, 0);
    printf("FIPS scelle %d\n", egal(CT, FIPS_CHIFFRE, 16));
    struct { const char *nom; fn_flux f; } FL[] = {
        {"flux-v2", flux_v2}, {"v3-table", flux_v3t},
        {"v3-deroule", flux_v3d}, {"v3-inline", flux_v3i},
        {"v4-appel", flux_v4a}, {"v4-inline", flux_v4i},
        {"frep-inline", flux_frep_i}, {"frep-table", flux_frep_t},
        {"frep-deroule", flux_frep_d}};
    #define N_FL (int)(sizeof(FL)/sizeof(FL[0]))
    unsigned char *OUT = malloc(16);
    for (int i = 0; i < N_FL; ++i) {
        memset(OUT, 0, 16);
        FL[i].f((unsigned long)RK, (unsigned long)FIPS_CLAIR,
                (unsigned long)OUT, 1);
        printf("FIPS %s %d\n", FL[i].nom, egal(OUT, FIPS_CHIFFRE, 16));
    }

    /* (2) LA DIFFÉRENTIELLE 64/64 puis 256/256 : chaque variant contre le
       scellé appelé par bloc, octet pour octet */
    for (int nb = 64; nb <= 256; nb *= 4) {
        unsigned char *IN = malloc(nb*16);
        unsigned char *SC = malloc(nb*16);
        unsigned char *OU = malloc(nb*16);
        for (int i = 0; i < nb*16; ++i) IN[i] = rnd();
        scelle_par_bloc((unsigned long)RK, IN, SC, nb);
        for (int i = 0; i < N_FL; ++i) {
            memset(OU, 0, nb*16);
            FL[i].f((unsigned long)RK, (unsigned long)IN,
                    (unsigned long)OU, nb);
            int k = 0;
            for (int b = 0; b < nb; ++b)
                k += egal(OU + b*16, SC + b*16, 16);
            printf("DIFF%d %s %d/%d\n", nb, FL[i].nom, k, nb);
        }
        if (nb == 64) {
            /* les repli forcés déjà dans FL ; le mutant : DOIT diverger */
            memset(OU, 0, nb*16);
            flux_mut((unsigned long)RK, (unsigned long)IN,
                     (unsigned long)OU, nb);
            int k = 0;
            for (int b = 0; b < nb; ++b)
                k += egal(OU + b*16, SC + b*16, 16);
            printf("NEGATIF %s\n", k < nb ? "ATTRAPE" : "NON-ATTRAPE");
        }
        free(IN); free(SC); free(OU);
    }

    /* (3) LA BORNE : N = 257 → rax = -2, RIEN chiffré (fail-closed) */
    {
        unsigned char *IN = malloc(257*16);
        unsigned char *OU = malloc(257*16);
        for (int i = 0; i < 257*16; ++i) IN[i] = rnd();
        memset(OU, 0xAA, 257*16);
        long r = flux_v3t((unsigned long)RK, (unsigned long)IN,
                          (unsigned long)OU, 257);
        int intact = 1;
        for (int i = 0; i < 257*16; ++i) if (OU[i] != 0xAA) intact = 0;
        printf("BORNE %d %d\n", r == -2, intact);
        free(IN); free(OU);
    }

    /* (4) LA MESURE : RDTSCP, n=20, médiane + IQR — chaque cellule */
    #define NCELL 20
    const char *NOMS[NCELL] = {
        "stub-msx64", "flux-v2@64", "scelle-C@64", "v3-table@64",
        "v3-deroule@64", "v3-inline@64", "v4-appel@64", "v4-inline@64",
        "creux@64", "cpuid@64", "pur-C@64",
        "flux-v2@256", "scelle-C@256", "v3-table@256", "v3-deroule@256",
        "v3-inline@256", "v4-appel@256", "v4-inline@256", "creux@256",
        "cpuid@256"};
    unsigned char *IN = malloc(256*16);
    unsigned char *OU = malloc(256*16);
    for (int i = 0; i < 256*16; ++i) IN[i] = rnd();

    for (int c = 0; c < NCELL; ++c) {
        long nb = (strstr(NOMS[c], "@256")) ? 256 : 64;
        uint64_t s[20];
        /* échauffement */
        for (int w = 0; w < 3; ++w) {
            if (c == 0) { for (int b = 0; b < nb; ++b)
                appeler_msx64(0xF000, 0, 0, 0, 0, 0); }
            else if (strstr(NOMS[c], "cpuid")) cpuid_n((int)nb);
            else if (strstr(NOMS[c], "scelle-C"))
                scelle_par_bloc((unsigned long)RK, IN, OU, nb);
            else if (strstr(NOMS[c], "pur-C"))
                for (int b = 0; b < nb; ++b)
                    appeler_msx64(0xCE00, (unsigned long)RK,
                                  (unsigned long)(IN + b*16),
                                  (unsigned long)(OU + b*16), 0, 0);
            else {
                unsigned long va = strstr(NOMS[c], "flux-v2") ? 0xCF00 :
                    strstr(NOMS[c], "v3-table") ? 0xD200 :
                    strstr(NOMS[c], "v3-deroule") ? 0xD400 :
                    strstr(NOMS[c], "v3-inline") ? 0xD800 :
                    strstr(NOMS[c], "v4-appel") ? 0xDC00 :
                    strstr(NOMS[c], "v4-inline") ? 0xDE00 : 0xF400;
                appeler_msx64(va, (unsigned long)RK, (unsigned long)IN,
                              (unsigned long)OU, nb, 0);
            }
        }
        for (int r = 0; r < 20; ++r) {
            uint64_t a = rdtscp_();
            if (c == 0) { for (int b = 0; b < nb; ++b)
                appeler_msx64(0xF000, 0, 0, 0, 0, 0); }
            else if (strstr(NOMS[c], "cpuid")) cpuid_n((int)nb);
            else if (strstr(NOMS[c], "scelle-C"))
                scelle_par_bloc((unsigned long)RK, IN, OU, nb);
            else if (strstr(NOMS[c], "pur-C"))
                for (int b = 0; b < nb; ++b)
                    appeler_msx64(0xCE00, (unsigned long)RK,
                                  (unsigned long)(IN + b*16),
                                  (unsigned long)(OU + b*16), 0, 0);
            else {
                unsigned long va = strstr(NOMS[c], "flux-v2") ? 0xCF00 :
                    strstr(NOMS[c], "v3-table") ? 0xD200 :
                    strstr(NOMS[c], "v3-deroule") ? 0xD400 :
                    strstr(NOMS[c], "v3-inline") ? 0xD800 :
                    strstr(NOMS[c], "v4-appel") ? 0xDC00 :
                    strstr(NOMS[c], "v4-inline") ? 0xDE00 : 0xF400;
                appeler_msx64(va, (unsigned long)RK, (unsigned long)IN,
                              (unsigned long)OU, nb, 0);
            }
            s[r] = rdtscp_() - a;
        }
        for (int i = 0; i < 20; ++i)
            for (int j = i+1; j < 20; ++j)
                if (s[j] < s[i]) { uint64_t t = s[i]; s[i] = s[j]; s[j] = t; }
        double med = (double)(s[10] + s[9]) / 2.0;
        double iqr = (double)(s[15] - s[4]);
        printf("MESURE %s %.2f %.2f\n", NOMS[c], med / (double)nb, iqr / (double)nb);
    }
    return 0;
}
"""
    rk_att = expansion_aes128(FIPS_CLE)
    rk_c = "static const unsigned char FIPS_CLE[] = {" + \
        ", ".join(f"0x{b:02x}" for b in FIPS_CLE) + "};\n" + \
        "static const unsigned char FIPS_CLAIR[] = {" + \
        ", ".join(f"0x{b:02x}" for b in FIPS_CLAIR) + "};\n" + \
        "static const unsigned char FIPS_CHIFFRE[] = {" + \
        ", ".join(f"0x{b:02x}" for b in FIPS_CHIFFRE) + "};\n" + \
        "static const unsigned char RK_ATTENDU[] = {" + \
        ", ".join(f"0x{b:02x}" for b in rk_att) + "};\n"
    rig = rig.replace("%%TABLES%%",
                      ctable("tls15", o15) + ctable("tls16", o16) +
                      ctable("pur", o_pur) + ctable("flux2", o_flux2) +
                      ctable("v3t", o_v3t) + ctable("v3d", o_v3d) +
                      ctable("v3i", o_v3i) + ctable("v4a", o_v4a) +
                      ctable("v4i", o_v4i) + ctable("mut", o_mut) +
                      ctable("frep_i", o_frep_i) + ctable("frep_t", o_frep_t) +
                      ctable("frep_d", o_frep_d) + ctable("creux", o_creux))
    rig = rig.replace("%%RK_ATTENDU%%", rk_c)
    (BUILD / "porteuse_rig.c").write_text(rig, encoding="utf-8")

    r = subprocess.run(["gcc", "-O2", "-o", str(BUILD / "porteuse_rig"),
                        str(BUILD / "porteuse_rig.c")],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"compilation : {r.stderr[:800]}")

    cpuinfo = pathlib.Path("/proc/cpuinfo").read_text()
    modele = re.search(r"model name\s*:\s*(.+)", cpuinfo).group(1).strip()
    mhz = re.findall(r"cpu MHz\s*:\s*([\d.]+)", cpuinfo)
    tous = [l.split(":", 1)[1].split() for l in cpuinfo.splitlines()
            if l.startswith("flags")][0]
    drapeaux = " ".join(sorted(
        set(tous) & {"aes", "constant_tsc", "rdtscp", "avx", "sse2",
                     "pclmulqdq"}))

    t0 = time.monotonic()
    r = subprocess.run([str(BUILD / "porteuse_rig")], capture_output=True,
                       text=True, timeout=600)
    dt = time.monotonic() - t0
    print(r.stdout)
    if r.returncode != 0:
        print("!!", r.returncode, r.stderr[:600])
        return 2

    # ---- le registre ------------------------------------------------------------
    lignes = r.stdout.splitlines()
    reg = {"machine": modele, "mhz": mhz[0] if mhz else "?",
           "drapeaux": drapeaux, "duree_rig_s": round(dt, 2),
           "round_trip_octet": rt,
           "octets": {"tls15": len(o15), "tls16": len(o16),
                      "pur": len(o_pur), "flux2": len(o_flux2),
                      "v3t": len(o_v3t), "v3d": len(o_v3d),
                      "v3i": len(o_v3i), "v4a": len(o_v4a),
                      "v4i": len(o_v4i), "creux": len(o_creux),
                      "mut": len(o_mut),
                      "frep_i": len(o_frep_i), "frep_t": len(o_frep_t),
                      "frep_d": len(o_frep_d)},
           "rva": {k: hex(v) for k, v in RVA.items()},
           "mutation": {"offset": cible, "avant": "0x90", "apres": "0x91"},
           "parite": {}, "mesures": {}}
    for l in lignes:
        p = l.split()
        if not p:
            continue
        if p[0] == "CALENDRIER":
            reg["parite"]["calendrier"] = p[1] == "1"
        elif p[0] == "FIPS":
            reg["parite"].setdefault("fips", {})[p[1]] = p[2] == "1"
        elif p[0] in ("DIFF64", "DIFF256"):
            reg["parite"].setdefault(p[0].lower(), {})[p[1]] = p[2]
        elif p[0] == "NEGATIF":
            reg["parite"]["negatif"] = p[1]
        elif p[0] == "BORNE":
            reg["parite"]["borne_rax_m2"] = p[1] == "1"
            reg["parite"]["borne_rien_chiffre"] = p[2] == "1"
        elif p[0] == "MESURE":
            reg["mesures"][p[1]] = {"mediane_c_bloc": float(p[2]),
                                    "iqr_c_bloc": float(p[3])}
    (REG / "porteuse-meson.json").write_text(
        json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- le contrôle python du verdict ----------------------------------------
    ok = (reg["parite"]["calendrier"]
          and all(v for v in reg["parite"]["fips"].values())
          and all(v == "64/64" for v in reg["parite"]["diff64"].values())
          and all(v == "256/256" for v in reg["parite"]["diff256"].values())
          and reg["parite"]["negatif"] == "ATTRAPE"
          and reg["parite"]["borne_rax_m2"]
          and reg["parite"]["borne_rien_chiffre"]
          and all(rt.values()))
    print(f"VERDICT {'VERT' if ok else 'ROUGE'}")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
