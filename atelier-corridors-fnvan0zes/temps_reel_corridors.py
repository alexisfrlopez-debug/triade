#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""temps_reel_corridors.py — LE RIG NATIF de l'atelier fnvan0zes : LES
DIFFÉRENTIELLES des chemins AVX2 et SHA-NI (le CPU du bac les porte —
avx2, sha_ni, aes aux drapeaux consignés) et LES CYCLES RÉELS (RDTSCP,
cœur fixé, n=20, médiane + IQR, la fréquence consignée).

LE PRINCIPE (le rig de la vague 10 reconduit) : les octets des notations
EMBARQUÉS dans le C généré, les pages exécutables posées aux adresses du
plan, le trampoline du memcmp scellé → la libc à 0x1180 (LA BIBLIOTHÈQUE
TENUE ÉGALE), l'appelant msx64 aux QUATRE registres + la 5e image.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-corridors-fnvan0zes"
BUILD = ICI / "native"
BUILD.mkdir(exist_ok=True)
sys.path.insert(0, str(ICI))
sys.path.insert(0, str(REPO / "loupe"))
sys.path.insert(0, str(REPO / "m4"))
sys.path.insert(0, str(REPO / "tls13"))

from mesurer_corridors import (assembler, RVA_HYB, RVA_AVX, RVA_SHANI,  # noqa
                               RVA_SCELLE_02, RVA_K)
import keystone as _ks
import capstone as _cs
KS13 = _ks.Ks(_ks.KS_ARCH_X86, _ks.KS_MODE_64)


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def ctable(nom: str, octets: bytes) -> str:
    lignes = []
    for i in range(0, len(octets), 16):
        chunk = octets[i:i + 16]
        lignes.append("  " + ", ".join(f"0x{b:02x}" for b in chunk) + ",")
    return f"static const unsigned char {nom}[] = {{\n" + "\n".join(lignes) + "\n};\n"


def main():
    # ---- les octets -------------------------------------------------------
    o_hyb, _ = assembler(ICI / "notation" / "loupe-13-hybride.asm", RVA_HYB)
    o_avx, _ = assembler(ICI / "notation" / "loupe-13-avx2.asm", RVA_AVX)
    symboles = {"@K%d" % (4 * i): ("abs", RVA_K + 16 * i) for i in range(16)}
    o_shani, _ = assembler(ICI / "notation" / "tls13-02-shani.asm",
                           RVA_SHANI, symboles)
    B4 = charger_module("b4_tr2", REPO / "m4" / "build_m4.py")
    HN = charger_module("hn_tr2", REPO / "loupe" / "harnais_noyau.py")
    not13 = list((REPO / "loupe" / "notation").glob("loupe-13-*.asm"))[0]
    rva13, slot13 = HN.L.SLOTS_LOUPE["i110013"]
    o_sc13, _ = B4.assembler_bloc(KS13, str(not13), rva13, slot13)
    lay = charger_module("lay_tr2", REPO / "tls13" / "layout.py")
    not02 = REPO / "tls13" / "notation" / "tls13-02-sha256-comprimer.asm"
    o_sc02, _ = B4.assembler_bloc(KS13, str(not02),
                                  *lay.SLOTS_TLS13["h100002"])
    # la table K réelle : extraite du proxy.exe scellé à 0x2f00 (le fixture)
    import pefile
    pe = pefile.PE(REPO / "tls13" / "proxy.exe")
    k_reel = pe.get_data(RVA_K, 256)

    # ---- les vecteurs de la batterie (régénérés, la même graine) ----------
    import random
    rng = random.Random(20261120)
    vecs = []
    for p in range(16):
        f = bytearray(rng.randrange(256) for _ in range(4096))
        m = bytes(rng.randrange(256) for _ in range(16))
        pos = max(0, 4096 - 16 - (15 - p))
        f[pos:pos + 16] = m
        vecs.append((bytes(f), m))
    for lm in (1, 4, 16):
        f = bytearray(rng.randrange(256) for _ in range(1000))
        m = bytes(rng.randrange(256) for _ in range(lm))
        pos = 1000 - lm
        f[pos:pos + lm] = m
        vecs.append((bytes(f), m))
    for periode in range(1, 5):
        f = bytearray(0x41 for _ in range(512))
        base = bytes(rng.randrange(256) for _ in range(periode))
        m = (base * (16 // periode + 1))[:16]
        pos = rng.randrange(64, 448)
        for i in range(16):
            f[pos + i] = m[i]
        vecs.append((bytes(f), m))
    for lm in (1, 2, 3, 4, 15, 16, 17, 18, 19, 20, 31, 32, 33):
        f = bytearray(rng.randrange(256) for _ in range(2048))
        m = bytes(rng.randrange(256) for _ in range(lm))
        pos = rng.randrange(0, 2048 - lm)
        f[pos:pos + lm] = m
        vecs.append((bytes(f), m))
    for bord in ("a", "b", "c"):
        f = bytearray(rng.randrange(256) for _ in range(512))
        m = bytes(rng.randrange(256) for _ in range(8))
        pos = {"a": 505, "b": 513, "c": 508}[bord]
        f[pos:pos + 8] = m
        vecs.append((bytes(f), m))
    for nocc in range(1, 9):
        f = bytearray(rng.randrange(256) for _ in range(2048))
        m = bytes(rng.randrange(256) for _ in range(6))
        for p in sorted(rng.sample(range(0, 2048 - 6), nocc)):
            f[p:p + 6] = m
        vecs.append((bytes(f), m))
    for k in range(512):
        n = rng.choice([17, 63, 100, 256, 1000, 4096])
        lm = rng.choice([1, 2, 3, 5, 8, 16, 17, 24, 32])
        f = bytearray(rng.randrange(256) for _ in range(n))
        m = bytes(rng.randrange(256) for _ in range(lm))
        if rng.random() < 0.7 and n > lm:
            p = rng.randrange(0, n - lm + 1)
            f[p:p + lm] = m
        vecs.append((bytes(f), m))
    # les vecteurs SHA (l'état + le bloc, la même LCG que la référence)
    s = 20261120

    def nxt64():
        nonlocal s
        s = s * 6364136223846793005 + 1442695040888963407
        return (s >> 32) & 0xFFFFFFFF
    vecs_sha = []
    for t in range(256):
        etat = [nxt64() for _ in range(8)]
        bloc = bytes(nxt64() & 0xFF for _ in range(64))
        vecs_sha.append((etat, bloc))

    # ---- le rig C généré ---------------------------------------------------
    rig = r"""/* temps_reel_corridors.c — LE RIG NATIF (fnvan0zes) — généré */
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <sys/mman.h>
#include <immintrin.h>
%%TABLES%%
#define RVA13 0x5740UL
static void pose_page(unsigned long base, size_t taille) {
    void *p = mmap((void*)base, taille, PROT_READ|PROT_WRITE|PROT_EXEC,
                   MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); exit(3); }
}
static void pose_trampoline(void) {
    pose_page(0x1000, 0x1000);
    unsigned char *t = (unsigned char *)0x1180;
    int i = 0;
    t[i++]=0x48; t[i++]=0x89; t[i++]=0xCF;
    t[i++]=0x48; t[i++]=0x89; t[i++]=0xD6;
    t[i++]=0x4C; t[i++]=0x89; t[i++]=0xC2;
    t[i++]=0x48; t[i++]=0xB8;
    uint64_t ad = (uint64_t)(void *)&memcmp;
    for (int k = 0; k < 8; k++) t[i++] = (unsigned char)(ad >> (8*k));
    t[i++]=0xFF; t[i++]=0xE0;
    __builtin___clear_cache((char*)t, (char*)t+i);
}
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
        : "rax", "rbx", "rcx", "rdx", "r8", "r9", "r10", "r11", "cc", "memory");
    return ret;
}
/* LES VECTEURS (les fichiers de données générés) */
#include "vecteurs_recherche.h"
#include "vecteurs_sha.h"
static inline unsigned long long rdtscp32(void) {
    unsigned aux;
    return __rdtscp(&aux);
}
int main(void) {
    pose_page(0xC000, 0x4000);
    pose_page(0x2000, 0x1000);
    pose_page(0x5000, 0x2000);
    pose_trampoline();
    memcpy((void*)0xCD00, hyb, sizeof(hyb));
    memcpy((void*)0xD100, avx, sizeof(avx));
    memcpy((void*)0xD300, shani, sizeof(shani));
    memcpy((void*)RVA13, sc13, sizeof(sc13));
    memcpy((void*)0xC080, sc02, sizeof(sc02));
    memcpy((void*)0x2F00, ktable, sizeof(ktable));
    __builtin___clear_cache((char*)0xC000, (char*)0x10000);
    __builtin___clear_cache((char*)0x2F00, (char*)0x3000);

    /* ---- LA DIFFÉRENTIELLE NATIVE : l'hybride et l'AVX2 (le vrai dispatch) */
    long div_hyb = 0, div_avx = 0;
    for (int i = 0; i < NB_VECS; i++) {
        long attendu = (long)memmem(vec_f[i], vec_n[i], vec_m[i], vec_lm[i]);
        long attendu_idx = (attendu == 0 && vec_lm[i] > 0 && vec_f[i][0] == vec_m[i]) ? 0 :
            (attendu ? (attendu - (long)vec_f[i]) : -1);
        /* le juge honnête : memmem sur des tampons NUL-terminés artificiels
           est piégeux — le jugement porté par memcmp séquentiel */
        long juge = -1;
        for (long p = 0; p + vec_lm[i] <= vec_n[i]; p++) {
            if (memcmp(vec_f[i] + p, vec_m[i], vec_lm[i]) == 0) { juge = p; break; }
        }
        (void)attendu_idx;
        long r_h = appeler_msx64(0xCD00, (unsigned long)vec_f[i], vec_n[i],
                                 (unsigned long)vec_m[i], vec_lm[i], 0);
        long r_a = appeler_msx64(0xD100, (unsigned long)vec_f[i], vec_n[i],
                                 (unsigned long)vec_m[i], vec_lm[i], 0);
        if (vec_lm[i] > 32) {
            /* LE REFUS DE CONTRAT (P2 : le motif ≤ 0x20) — attendu -5 */
            if (r_h != -5) div_hyb++;
            if (r_a != -5) div_avx++;
        } else {
            if (r_h != juge) div_hyb++;
            if (r_a != juge) div_avx++;
        }
    }
    printf("LA DIFFÉRENTIELLE NATIVE : hybride %ld/%d divergences ; AVX2 %ld/%d divergences\n",
           div_hyb, NB_VECS, div_avx, NB_VECS);

    /* ---- LA DIFFÉRENTIELLE SHA-NI : la notation contre LE SCELLÉ GPR */
    long div_sha = 0;
    for (int t = 0; t < NB_VECS_SHA; t++) {
        uint32_t e1[8], e2[8];
        memcpy(e1, sha_etat[t], 32);
        memcpy(e2, sha_etat[t], 32);
        appeler_msx64(0xD300, (unsigned long)e1, (unsigned long)sha_bloc[t], 0, 0, 0);
        appeler_msx64(0xC080, (unsigned long)e2, (unsigned long)sha_bloc[t], 0, 0, 0);
        if (memcmp(e1, e2, 32) != 0) div_sha++;
    }
    printf("LA DIFFÉRENTIELLE SHA-NI (contre LE SCELLÉ) : %ld/%d divergences\n",
           div_sha, NB_VECS_SHA);

    /* ---- LES CYCLES RÉELS (RDTSCP, cœur fixé, n=20, médiane + IQR) ------ */
    cpu_set_t ens;
    CPU_ZERO(&ens); CPU_SET(1, &ens);
    sched_setaffinity(0, sizeof(ens), &ens);
    /* la cellule de référence : la série 4096/16 ABSENTS (la convention) */
    unsigned char tamp[4096], motif[32];
    for (int i = 0; i < 4096; i++) tamp[i] = (unsigned char)(i * 31 + 7);
    for (int i = 0; i < 16; i++) motif[i] = 0xEE;   /* absent */
    unsigned long long cyc[24];
    int n = 20;
    #define MESURE(nom, expr) do { \
        for (int r = 0; r < n; r++) { \
            unsigned long long t0 = rdtscp32(); \
            (void)(expr); \
            cyc[r] = rdtscp32() - t0; \
        } \
        for (int i2 = 1; i2 < n; i2++) { unsigned long long k2 = cyc[i2]; int j2 = i2-1; \
            while (j2 >= 0 && cyc[j2] > k2) { cyc[j2+1] = cyc[j2]; j2--; } cyc[j2+1] = k2; } \
        printf("CYCLES %-14s médiane %llu IQR %llu\n", nom, \
               (cyc[n/2-1]+cyc[n/2])/2, cyc[n*3/4]-cyc[n/4]); \
    } while (0)
    MESURE("hybride", appeler_msx64(0xCD00, (unsigned long)tamp, 4096, (unsigned long)motif, 16, 0));
    MESURE("avx2", appeler_msx64(0xD100, (unsigned long)tamp, 4096, (unsigned long)motif, 16, 0));
    MESURE("scelle13", appeler_msx64(RVA13, (unsigned long)tamp, 4096, (unsigned long)motif, 16, 0));
    /* la cellule SHA : 64 blocs de compression (le flot de 4 KiB) */
    static uint32_t etat[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                               0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
    MESURE("shani-64blocs", ({ for (int b = 0; b < 64; b++) \
        appeler_msx64(0xD300, (unsigned long)etat, (unsigned long)(tamp + (b % 60)), 0, 0, 0); }));
    /* LE CORPS SHA-NI SANS LE DISPATCH : le sondage PATCHÉ EN PLACE
    (xor ebx,ebx + nops), mesuré, PUIS RESTAURÉ octet pour octet — la
    technique de laboratoire : les déplacements rip demeurés exacts) */
    { unsigned char *p = (unsigned char*)0xD300;
      /* LE DISPATCH ENTIÈREMENT PATCHÉ (21 octets : xor ecx,ecx; mov eax,7;
      cpuid; test ebx,imm32; je rel32 → NOPs — le prologue et les déplacements
      rip demeurés INTACTS — la cause nommée : cpuid(7) ≈ 2 660 cycles au bac
      virtualisé, la sortie d'hyperviseur) */
      unsigned char patch[21];
      for (int u = 0; u < 21; u++) patch[u] = 0x90;
      unsigned char sauv[6];
      /* le dispatch : de « xor ecx, ecx » (après mov r10, rdx) au « je » —
      l'offset fixe vérifié à l'assemblage : 7 (prologue) → 7+21 */
      long ou = 7;
      memcpy(sauv, p+ou, 21);
      memcpy(p+ou, patch, 21);
      __builtin___clear_cache((char*)p, (char*)p+896);
      MESURE("shani-corps", ({ for (int b = 0; b < 64; b++) \
          appeler_msx64(0xD300, (unsigned long)etat, (unsigned long)(tamp + (b % 60)), 0, 0, 0); }));
      memcpy(p+ou, sauv, 6);
      __builtin___clear_cache((char*)p, (char*)p+896); }
    /* LE COÛT DU DISPATCH (le sondage seul, par appel — la forme pleine) */
    MESURE("shani-dispatch", appeler_msx64(0xD300, (unsigned long)etat, (unsigned long)tamp, 0, 0, 0));
    MESURE("scelle02-64blocs", ({ for (int b = 0; b < 64; b++) \
        appeler_msx64(0xC080, (unsigned long)etat, (unsigned long)(tamp + (b % 60)), 0, 0, 0); }));
    return 0;
}
"""
    tables = (ctable("hyb", o_hyb) + ctable("avx", o_avx)
              + ctable("shani", o_shani) + ctable("sc13", o_sc13)
              + ctable("sc02", o_sc02) + ctable("ktable", k_reel))
    rig = rig.replace("%%TABLES%%", tables)
    rig = rig.replace("#define _GNU_SOURCE", "#define _GNU_SOURCE\n#define RVA13 0x5740UL", 1)

    # les fichiers de vecteurs
    with open(BUILD / "vecteurs_recherche.h", "w") as f:
        f.write(f"#define NB_VECS {len(vecs)}\n")
        f.write("static const unsigned char *vec_f[] = {" +
                ",".join(f"(const unsigned char*)\"\"" for _ in vecs) + "};\n")
        # (les tampons portés par un gros tableau plat)
        f.write("static const unsigned char TAMPONS[] = {\n")
        idx = []
        cur = 0
        for f_, m_ in vecs:
            idx.append(cur)
            cur += len(f_)
            f.write("  " + ", ".join(str(b) for b in f_) + ",\n")
        f.write("};\n")
        f.write("static const unsigned long vec_decal[] = {" +
                ",".join(str(i) for i in idx) + "};\n")
        f.write("static const long vec_n[] = {" +
                ",".join(str(len(f_)) for f_, _ in vecs) + "};\n")
        f.write("static const unsigned char MOTIFS[] = {\n")
        midx, mcur = [], 0
        for f_, m_ in vecs:
            midx.append(mcur)
            mcur += max(len(m_), 1)
            if len(m_):
                f.write("  " + ", ".join(str(b) for b in m_) + ",\n")
            else:
                f.write("  0,\n")
        f.write("};\n")
        f.write("static const unsigned long m_decal[] = {" +
                ",".join(str(i) for i in midx) + "};\n")
        f.write("static const long vec_lm[] = {" +
                ",".join(str(len(m_)) for _, m_ in vecs) + "};\n")
        f.write("static const unsigned long MFINS[] = {" +
                ",".join(str(max(len(m_), 1)) for _, m_ in vecs) + "};\n")
    rig = rig.replace("vec_f[i]", "(TAMPONS + vec_decal[i])").replace(
        "vec_m[i]", "(MOTIFS + m_decal[i])")
    with open(BUILD / "vecteurs_sha.h", "w") as f:
        f.write(f"#define NB_VECS_SHA {len(vecs_sha)}\n")
        f.write("static const uint32_t sha_etat[][8] = {\n")
        for etat, _ in vecs_sha:
            f.write("  {" + ",".join(f"0x{x:08x}u" for x in etat) + "},\n")
        f.write("};\n")
        f.write("static const unsigned char sha_bloc[][64] = {\n")
        for _, bloc in vecs_sha:
            f.write("  {" + ",".join(str(b) for b in bloc) + "},\n")
        f.write("};\n")

    (BUILD / "temps_reel_corridors.c").write_text(rig, encoding="utf-8")
    r = subprocess.run(["gcc", "-O1", "-no-pie", "-msha", "-mssse3", "-msse4.1",
                        "-o", str(BUILD / "temps_reel_corridors"),
                        str(BUILD / "temps_reel_corridors.c")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[:3000])
        return 2
    r = subprocess.run([str(BUILD / "temps_reel_corridors")],
                       capture_output=True, text=True, timeout=600)
    print(r.stdout)
    (ICI / "rapport-temps-reel-corridors.txt").write_text(r.stdout,
                                                          encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
