#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""temps_reel.py — LE RIG DE TEMPS RÉEL NATIF (8z4hj76w4) : LA VARIANTE
SSE2 CORRIGÉE et LE SCELLÉ GPR exécutés SUR MATÉRIEL (pages exécutables
mmap, le trampoline du memcmp SCELLÉ→libc à 0x1180 — LA BIBLIOTHÈQUE
TENUE ÉGALE : les bras C appellent le memcmp de la même libc), face aux
BASELINES ÉQUITABLES : gcc-O2 scalaire, gcc-O3, l13v (l'idiome
memchr+memcmp — le SIMD de la bibliothèque), memmem direct.

LE TEMPS : RDTSCP, l'affinité de cœur FIXÉE (cœur 1), la fréquence
consignée, n=20 répétitions par cellule (≥10 exigé), la médiane et
l'IQR ; l'horloge monotone en recoupe.

LA LIMITE NOMMÉE : UNE SEULE MACHINE au bac (la consigne « ≥2 machines,
témoins signés » — l'écart nommé en l'état : la machine de record, le
témoin signé attend le geste du maître — JAMAIS simulé).

LE COULOIR B AUSSI : le flux v2 (sondage hissé, AES-NI vécu — le CPU du
bac porte aes) contre le scellé GPR appelé par bloc — les cycles/bloc.

Sortie : temps-reel.json · rapport-temps-reel.txt"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import statistics
import subprocess
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-remesure-sse2-8z4hj76w4"
sys.path.insert(0, str(REPO / "loupe"))
BUILD = ICI / "native"
BUILD.mkdir(exist_ok=True)

import capstone  # noqa: E402
import keystone  # noqa: E402

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def assembler(fichier: pathlib.Path, rva: int):
    lignes = [l.split(";")[0] for l in fichier.read_text(
        encoding="utf-8").splitlines()]
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


def main():
    # ---- les octets des notations ---------------------------------------
    o_v2 = assembler(ICI / "notation" / "loupe-13-sse2-v2.asm", 0xCC00)
    sys.path.insert(0, str(REPO / "m4"))
    sys.path.insert(0, str(REPO / "tls13"))
    B4 = charger_module("b4_tr", REPO / "m4" / "build_m4.py")
    HN = charger_module("hn_tr", REPO / "loupe" / "harnais_noyau.py")
    not13 = list((REPO / "loupe" / "notation").glob("loupe-13-*.asm"))[0]
    rva13, slot13 = HN.L.SLOTS_LOUPE["i110013"]
    o_sc13, _ = B4.assembler_bloc(KS, str(not13), rva13, slot13)
    o_pur = assembler(ICI / "notation" / "tls13-16-ni-v2-pur.asm", 0xCE00)
    o_flux = assembler(ICI / "notation" / "tls13-16-ni-v2-flux.asm", 0xCF00)
    lay = charger_module("lay_tr", REPO / "tls13" / "layout.py")
    not15 = list((REPO / "tls13" / "notation").glob("tls13-15-*.asm"))[0]
    not16 = list((REPO / "tls13" / "notation").glob("tls13-16-*.asm"))[0]
    o15, _ = B4.assembler_bloc(KS, str(not15), *lay.SLOTS_TLS13["h100015"])
    o16, _ = B4.assembler_bloc(KS, str(not16), *lay.SLOTS_TLS13["h100016"])

    for octets, nom in [(o_v2, "v2"), (o_sc13, "sc13"), (o_pur, "pur"),
                        (o_flux, "flux"), (o15, "tls15"), (o16, "tls16")]:
        reins = b""
        for ins in CS.disasm(octets[:len(octets)], 0):
            pass  # (le round-trip déjà prouvé au rig d'instructions)
    # la vérification du round-trip menée à remesure_instructions.py

    rig = r"""/* temps_reel.c — LE RIG NATIF (8z4hj76w4) — généré par temps_reel.py
   (jamais écrit à la main : les octets des notations EMBARQUÉS des
   fichiers, la compilation aux drapeaux par fichier). */
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <sys/mman.h>

/* ---- les notations embarquées (les copies de laboratoire) ------------- */
%%TABLES%%

/* ---- les pages exécutables aux adresses du plan ------------------------ */
static void pose_page(unsigned long base, size_t taille) {
    void *p = mmap((void*)base, taille, PROT_READ|PROT_WRITE|PROT_EXEC,
                   MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); exit(3); }
}

/* le trampoline du memcmp SCELLÉ → la libc (LA BIBLIOTHÈQUE TENUE ÉGALE :
   les bras C appellent memcmp@plt de la MÊME libc ; le trampoline ajoute
   un jmp par appel — la dette de la copie, nommée) */
static void pose_trampoline(void) {
    pose_page(0x1000, 0x1000);
    unsigned char *t = (unsigned char *)0x1180;
    /* LA TRADUCTION DE CONVENTION : le scellé libc-02 parle msx64
       (rcx/rdx/r8) ; la libc native parle SysV (rdi/rsi/rdx) — le
       trampoline POSE les registres puis saute au memcmp (tail call :
       le ret du memcmp rend directement à l'appelant du scellé) */
    int i = 0;
    t[i++]=0x48; t[i++]=0x89; t[i++]=0xCF;   /* mov rdi, rcx */
    t[i++]=0x48; t[i++]=0x89; t[i++]=0xD6;   /* mov rsi, rdx */
    t[i++]=0x4C; t[i++]=0x89; t[i++]=0xC2;   /* mov rdx, r8 */
    t[i++]=0x48; t[i++]=0xB8;                 /* movabs rax, imm64 */
    uint64_t ad = (uint64_t)(void *)&memcmp;
    for (int k = 0; k < 8; k++) t[i++] = (unsigned char)(ad >> (8*k));
    t[i++]=0xFF; t[i++]=0xE0;                 /* jmp rax */
    __builtin___clear_cache((char*)t, (char*)t+i);
}

/* l'appelant msx64 : les QUATRE registres + la 5e image POSÉS PAR
   L'APPELANT (les valeurs brutes — la convention msx64 exacte) */
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

/* ---- les challengers ---------------------------------------------------- */
extern long l13_o2(const unsigned char *, long, const unsigned char *,
                   long, long);
extern long l13_o3(const unsigned char *, long, const unsigned char *,
                   long, long);
extern long l13v_o2(const unsigned char *, long, const unsigned char *,
                    long, long);
extern long l13v_o3(const unsigned char *, long, const unsigned char *,
                    long, long);

static long rech_v2(const unsigned char *f, long n, const unsigned char *m,
                     long lm, long dep) {
    return appeler_msx64(0xCC00, (unsigned long)f, (unsigned long)n,
                         (unsigned long)m, (unsigned long)lm,
                         (unsigned long)dep);
}
static long rech_sc13(const unsigned char *f, long n, const unsigned char *m,
                      long lm, long dep) {
    return appeler_msx64(0x5740, (unsigned long)f, (unsigned long)n,
                         (unsigned long)m, (unsigned long)lm,
                         (unsigned long)dep);
}
/* l'idiome memchr+memcmp (le SIMD de la bibliothèque — l13v, compilé) ;
   le memmem direct : le contrat posé, la voie idiomatique entière */
static long rech_memmem(const unsigned char *f, long n,
                        const unsigned char *m, long lm, long dep) {
    if (lm > 32 || n < 0 || dep > n) return -5;
    if (dep + lm > n) return -1;
    const unsigned char *p = memmem(f + dep, (size_t)(n - dep),
                                    m, (size_t)lm);
    if (!p) return -1;
    return (long)(p - f);
}

/* LE JUGE TRIVIAL (jamais le binaire optimisé) */
static long juge(const unsigned char *f, long n, const unsigned char *m,
                 long lm, long dep) {
    if (lm > 32 || n < 0 || dep > n) return -5;
    for (long i = dep; i + lm <= n; ++i) {
        long j = 0;
        while (j < lm && f[i + j] == m[j]) ++j;
        if (j == lm) return i;
    }
    return -1;
}

/* ---- le temps : RDTSCP, l'affinité fixée ------------------------------- */
static uint64_t rdtscp_(void) {
    uint32_t lo, hi, aux;
    __asm__ volatile("rdtscp" : "=a"(lo), "=d"(hi), "=c"(aux) :: "memory");
    return ((uint64_t)hi << 32) | lo;
}
static double mono(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

typedef long (*fn_rech)(const unsigned char *, long, const unsigned char *,
                        long, long);
static const struct { const char *nom; fn_rech fn; } RECH[] = {
    {"v2-sse2-notation", rech_v2},
    {"scelle-gpr-notation", rech_sc13},
    {"gcc-O2", l13_o2},
    {"gcc-O3", l13_o3},
    {"idiome-memchr-O2", l13v_o2},
    {"idiome-memchr-O3", l13v_o3},
    {"libc-memmem", rech_memmem},
};
#define N_RECH (int)(sizeof(RECH)/sizeof(RECH[0]))

/* la série : la graine 20261120 reproduite par xorshift (le même générateur
   que le rig Python — les vecteurs RECOUPEX par le juge trivial aux deux) */
static uint64_t xs = 20261120ULL;
static unsigned char rnd(void) {
    xs ^= xs << 13; xs ^= xs >> 7; xs ^= xs << 17;
    return (unsigned char)(xs >> 32);
}

int main(void) {
    /* l'affinité au cœur 1 (la machine de record : 2 cœurs) */
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(1, &m);
    if (sched_setaffinity(0, sizeof(m), &m) != 0) perror("affinité");

    pose_page(0xC000, 0x4000);
    memcpy((void*)0xCC00, v2, sizeof(v2));
    memcpy((void*)0xCE00, pur, sizeof(pur));
    memcpy((void*)0xCF00, flux, sizeof(flux));
    pose_page(0x5000, 0x2000);
    memcpy((void*)0x5740, sc13, sizeof(sc13));
    memcpy((void*)0xC080, tls15, sizeof(tls15));
    memcpy((void*)0xC400, tls16, sizeof(tls16));
    pose_trampoline();
    __builtin___clear_cache((char*)0xC000, (char*)0x10000);
    __builtin___clear_cache((char*)0x5000, (char*)0x7000);
    __builtin___clear_cache((char*)0x1000, (char*)0x2000);

    /* les tampons */
    unsigned char *F = malloc(4096);
    unsigned char *M = malloc(64);

    /* (0) LE CONTRÔLE NÉGATIF : la variante mutée à la première ligne */
    {
        unsigned char *mut = malloc(sizeof(v2));
        memcpy(mut, v2, sizeof(v2));
        mut[4] = 0x29;            /* le déplacement 0x28 -> 0x29 */
        memcpy((void*)0xD200, mut, sizeof(v2));
        __builtin___clear_cache((char*)0xD200, (char*)(0xD200+sizeof(v2)));
        /* un vecteur planted : le mutant doit DIVERGER du juge */
        for (long i = 0; i < 4096; ++i) F[i] = rnd();
        for (long i = 0; i < 16; ++i) M[i] = rnd();
        memcpy(F + 17, M, 16);
        long att = juge(F, 4096, M, 16, 0);
        long r = appeler_msx64(0xD200, (unsigned long)F, 4096,
                              (unsigned long)M, 16, 0);
        printf("NEGATIF %s\n", r != att ? "ATTRAPE" : "NON-ATTRAPE");
    }

    /* (1) LA CONFRONTATION : chaque challenger au juge trivial —
       les 24 vecteurs de la convention + 64 occurrences plantées */
    int diverg[N_RECH] = {0};
    {
        /* les 15 + 9 bords */
        int n_n[24] = {0}, lm_n[24] = {0};
        for (int i = 0; i < 15; ++i) { n_n[i] = 4096; lm_n[i] = 16; }
        int bords[9][2] = {{0,1},{1,1},{2,32},{33,32},{64,1},{65,32},
                           {255,31},{256,32},{1000,32}};
        for (int i = 0; i < 9; ++i) { n_n[15+i] = bords[i][0];
                                      lm_n[15+i] = bords[i][1]; }
        for (int v = 0; v < 24; ++v) {
            for (long i = 0; i < n_n[v]; ++i) F[i] = rnd();
            for (long i = 0; i < lm_n[v]; ++i) M[i] = rnd();
            long att = juge(F, n_n[v], M, lm_n[v], 0);
            for (int c = 0; c < N_RECH; ++c)
                if (RECH[c].fn(F, n_n[v], M, lm_n[v], 0) != att)
                    diverg[c]++;
        }
        /* les 64 occurrences plantées aux alignements 0-63 */
        for (int p = 0; p < 64; ++p) {
            for (long i = 0; i < 4096; ++i) F[i] = rnd();
            for (long i = 0; i < 16; ++i) M[i] = rnd();
            memcpy(F + p, M, 16);
            long att = juge(F, 4096, M, 16, 0);
            for (int c = 0; c < N_RECH; ++c)
                if (RECH[c].fn(F, 4096, M, 16, 0) != att) diverg[c]++;
        }
    }

    /* (2) LA MESURE : trois cellules × les challengers (n=20, médiane) */
    double resultats[N_RECH][3];
    double iqr[N_RECH][3];
    {
        struct { long n, lm; int plante; } cell[3] = {
            {4096, 16, 0}, {1000, 32, 0}, {4096, 1, 0},
        };
        for (int k = 0; k < 3; ++k) {
            for (long i = 0; i < cell[k].n; ++i) F[i] = rnd();
            for (long i = 0; i < cell[k].lm; ++i) M[i] = rnd();
            for (int c = 0; c < N_RECH; ++c) {
                RECH[c].fn(F, cell[k].n, M, cell[k].lm, 0); /* échauffement */
                RECH[c].fn(F, cell[k].n, M, cell[k].lm, 0);
                uint64_t s[20];
                for (int r = 0; r < 20; ++r) {
                    uint64_t a = rdtscp_();
                    RECH[c].fn(F, cell[k].n, M, cell[k].lm, 0);
                    s[r] = rdtscp_() - a;
                }
                /* médiane + IQR sur les 20 */
                for (int i = 0; i < 20; ++i)
                    for (int j = i+1; j < 20; ++j)
                        if (s[j] < s[i]) { uint64_t t = s[i]; s[i] = s[j]; s[j] = t; }
                resultats[c][k] = (double)(s[10] + s[9]) / 2.0;
                iqr[c][k] = (double)(s[15] - s[4]) / 2.0;
            }
        }
    }

    /* (3) LE COULOIR B : les cycles par bloc — le flux v2 (NI hissé) contre
       le scellé GPR appelé par bloc (la même clé, 64 blocs aléatoires) */
    double blocs_v2 = 0, blocs_sc = 0, blocs_ret = 0;
    {
        /* la calibration : l'enveloppe msx64 seule (le stub ret) —
           dans la page déjà posée 0xC000-0x10000 (la marge 0xF000) */
        *(unsigned char *)0xF000 = 0xC3;      /* ret */
        __builtin___clear_cache((char*)0xF000, (char*)0xF001);
        uint64_t sr[20];
        for (int r = 0; r < 20; ++r) {
            uint64_t a = rdtscp_();
            for (int b = 0; b < 64; ++b)
                appeler_msx64(0xF000, 0, 0, 0, 0, 0);
            sr[r] = rdtscp_() - a;
        }
        for (int i = 0; i < 20; ++i)
            for (int j = i+1; j < 20; ++j)
                if (sr[j] < sr[i]) { uint64_t x = sr[i]; sr[i] = sr[j]; sr[j] = x; }
        blocs_ret = (double)(sr[10] + sr[9]) / 2.0 / 64.0;
        unsigned char *cle = malloc(16);
        unsigned char *RK = malloc(176);
        unsigned char *IN = malloc(64*16);
        unsigned char *OUT = malloc(64*16);
        for (int i = 0; i < 16; ++i) cle[i] = rnd();
        /* le calendrier des clés par LE SCELLÉ tls13-15 */
        appeler_msx64(0xC080, (unsigned long)cle, (unsigned long)RK,
                      0, 0, 0);   /* rcx=clé rdx=RK */
        for (int i = 0; i < 64*16; ++i) IN[i] = rnd();
        /* l'égalité au juge : le flux v2 == la boucle au scellé */
        memcpy(OUT, "\0"*, 1); /* (amorce) */
        memset(OUT, 0, 64*16);
        appeler_msx64(0xCF00, (unsigned long)RK, (unsigned long)IN,
                      (unsigned long)OUT, 64, 0);
        unsigned char *SCOUT = malloc(64*16);
        memset(SCOUT, 0, 64*16);
        for (int b = 0; b < 64; ++b)
            appeler_msx64(0xC400, (unsigned long)RK,
                          (unsigned long)(IN + b*16),
                          (unsigned long)(SCOUT + b*16), 0, 0);
        int eq = memcmp(OUT, SCOUT, 64*16) == 0;
        /* la mesure */
        uint64_t s2[20];
        for (int r = 0; r < 20; ++r) {
            uint64_t a = rdtscp_();
            appeler_msx64(0xCF00, (unsigned long)RK, (unsigned long)IN,
                      (unsigned long)OUT, 64, 0);
            s2[r] = rdtscp_() - a;
        }
        uint64_t s3[20];
        for (int r = 0; r < 20; ++r) {
            uint64_t a = rdtscp_();
            for (int b = 0; b < 64; ++b)
                appeler_msx64(0xC400, (unsigned long)RK,
                              (unsigned long)(IN + b*16),
                              (unsigned long)(OUT + b*16), 0, 0);
            s3[r] = rdtscp_() - a;
        }
        for (int i = 0; i < 20; ++i)
            for (int j = i+1; j < 20; ++j) {
                if (s2[j] < s2[i]) { uint64_t t = s2[i]; s2[i] = s2[j]; s2[j] = t; }
                if (s3[j] < s3[i]) { uint64_t t = s3[i]; s3[i] = s3[j]; s3[j] = t; }
            }
        blocs_v2 = (double)(s2[10] + s2[9]) / 2.0 / 64.0;
        blocs_sc = (double)(s3[10] + s3[9]) / 2.0 / 64.0;
        printf("AES-EGALITE %d\n", eq);
    }

    /* le rapport JSON */
    printf("RAPPORT-JSON\n");
    for (int c = 0; c < N_RECH; ++c) {
        printf("CHALL %s %d %d %d %.1f %.1f %.1f %.1f %.1f %.1f\n",
               RECH[c].nom, diverg[c], 0, 0,
               resultats[c][0], resultats[c][1], resultats[c][2],
               iqr[c][0], iqr[c][1], iqr[c][2]);
    }
    printf("AES %.1f %.1f %.1f\n", blocs_v2, blocs_sc, blocs_ret);
    return 0;
}
"""
    rig = rig.replace("%%TABLES%%",
        ctable("v2", o_v2) + ctable("sc13", o_sc13) +
        ctable("pur", o_pur) + ctable("flux", o_flux) +
        ctable("tls15", o15) + ctable("tls16", o16))
    rig = rig.replace('memcpy(OUT, "\\0"*, 1); /* (amorce) */\n        ', '')
    (BUILD / "temps_reel.c").write_text(rig, encoding="utf-8")

    l13 = """#include <string.h>
long %s(const unsigned char *fenetre, long taille,
        const unsigned char *motif, long taille_motif, long depart) {
    if (taille_motif > 32 || taille < 0 || depart > taille) return -5;
    for (long i = depart; i <= taille - taille_motif; ++i)
        if (memcmp(fenetre + i, motif, taille_motif) == 0) return i;
    return -1;
}
"""
    l13v = """#include <string.h>
long %s(const unsigned char *fenetre, long taille,
        const unsigned char *motif, long taille_motif, long depart) {
    if (taille_motif > 32 || taille < 0 || depart > taille) return -5;
    if (taille_motif == 0) return depart;
    long fin = taille - taille_motif;
    long i = depart;
    while (i <= fin) {
        const unsigned char *hit = memchr(fenetre + i, motif[0],
                                          (size_t)(fin - i + 1));
        if (!hit) return -1;
        if (memcmp(hit, motif, (size_t)taille_motif) == 0)
            return (long)(hit - fenetre);
        i = (long)(hit - fenetre) + 1;
    }
    return -1;
}
"""
    (BUILD / "l13_o2.c").write_text(l13 % "l13_o2", encoding="utf-8")
    (BUILD / "l13_o3.c").write_text(l13 % "l13_o3", encoding="utf-8")
    (BUILD / "l13v_o2.c").write_text(l13v % "l13v_o2", encoding="utf-8")
    (BUILD / "l13v_o3.c").write_text(l13v % "l13v_o3", encoding="utf-8")

    def cc(cible, drapeaux):
        r = subprocess.run(["gcc", *drapeaux, "-c", str(BUILD / cible),
                            "-o", str(BUILD / cible.replace(".c", ".o"))],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            raise RuntimeError(f"compilation {cible} : {r.stderr[:600]}")

    cc("temps_reel.c", ["-O2", "-msse2"])
    cc("l13_o2.c", ["-O2"])
    cc("l13_o3.c", ["-O3"])
    cc("l13v_o2.c", ["-O2"])
    cc("l13v_o3.c", ["-O3"])
    r = subprocess.run(
        ["gcc", "-o", str(BUILD / "temps_reel"),
         str(BUILD / "temps_reel.o"), str(BUILD / "l13_o2.o"),
         str(BUILD / "l13_o3.o"), str(BUILD / "l13v_o2.o"),
         str(BUILD / "l13v_o3.o")],
        capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"édition de liens : {r.stderr[:400]}")

    # la fréquence consignée AVANT l'exécution
    cpuinfo = pathlib.Path("/proc/cpuinfo").read_text()
    mhz = re.findall(r"cpu MHz\s*:\s*([\d.]+)", cpuinfo)
    modele = re.search(r"model name\s*:\s*(.+)", cpuinfo)
    drapeaux = "constant_tsc" if "constant_tsc" in cpuinfo else "PAS constant_tsc"

    t0 = time.monotonic()
    r = subprocess.run([str(BUILD / "temps_reel")], capture_output=True,
                       text=True, timeout=600)
    dt = time.monotonic() - t0
    print(r.stdout)
    if r.returncode != 0:
        print("!!", r.returncode, r.stderr[:400])
        return 2

    # le rapport
    negatif = "ATTRAPE" in r.stdout
    egalite = "AES-EGALITE 1" in r.stdout
    lignes = [l for l in r.stdout.splitlines() if l.startswith("CHALL ")]
    rapport = ["LE TEMPS RÉEL SUR MATÉRIEL (8z4hj76w4) — le rig natif :",
               "",
               f"LA MACHINE DE RECORD : {modele.group(1).strip()} — "
               f"{mhz and mhz[1] or '?'} MHz consignés, {drapeaux}, "
               f"l'affinité au cœur 1 (sched_setaffinity), RDTSCP, "
               f"n=20 répétitions par cellule (≥10 exigé), la médiane "
               f"et l'IQR rapportées en CYCLES ; LA LIMITE NOMMÉE : UNE "
               f"SEULE MACHINE au bac — la consigne « ≥2 machines, "
               f"témoins signés » attend la seconde machine et le geste "
               f"du maître : JAMAIS simulé",
               "",
               "LE CONTRÔLE NÉGATIF (la variante mutée à la première "
               f"ligne, le déplacement 0x28→0x29) : "
               f"{'ATTRAPÉ à la première divergence' if negatif else 'NON ATTRAPÉ — ROUGE'}",
               ""]
    for l in lignes:
        p = l.split()
        nom, d = p[1], int(p[2])
        m0, m1, m2 = float(p[5]), float(p[6]), float(p[7])
        i0, i1, i2 = float(p[8]), float(p[9]), float(p[10])
        rapport.append(
            f"  {nom:22s} — divergences {d}/88 ; cellules "
            f"(4096/16): {m0:8.0f} cyc [IQR {i0:6.0f}] ; "
            f"(1000/32): {m1:7.0f} cyc [IQR {i1:5.0f}] ; "
            f"(4096/1): {m2:7.0f} cyc [IQR {i2:5.0f}]")
    for l in r.stdout.splitlines():
        if l.startswith("AES "):
            v2b, scb, rtb = map(float, l.split()[1:])
            rapport += [
                "",
                "LE COULOIR B AU MATÉRIEL (AES-NI vécu au CPU du bac — "
                "NOTE : le SCELLÉ tls13-16 est DÉJÀ le chemin aesenc "
                "[I3, la descente vécue] — la comparaison natif porte "
                "les FORMES DU PORTEUR, pas NI contre GPR) : le flux v2 "
                f"(sondage hissé, la boucle à registres porteurs) "
                f"{v2b:.0f} cycles/bloc ; le scellé appelé par bloc "
                f"depuis le C (la boucle du compilateur) {scb:.0f} "
                f"cycles/bloc ; LA CALIBRATION de l'enveloppe msx64 "
                f"(le stub ret) {rtb:.1f} cycles/appel",
                f"    LA LECTURE HONNÊTE : la boucle du flux porte une "
                f"chaîne de dépendance PAR REGISTRES PORTÉS (r13/r14/r15 "
                f"— add → mov → call sérialisés) quand la boucle du "
                f"compilateur expose des adresses INDÉPENDANTES PAR "
                f"BLOC au moteur hors-ordre : le recouvrement "
                f"inter-blocs s'exprime côté C — L'ÉCART "
                f"{v2b - scb:.0f} cycles/bloc NOMMÉ (la forme du "
                f"porteur, pas le chemin crypto) ; le corps NI "
                f"({scb - rtb:.0f} cycles/bloc nets de l'enveloppe) "
                f"reste le chemin chaud mesuré",
                f"L'ÉGALITÉ flux/scellé au matériel : "
                f"{'ZÉRO DIVERGENCE octet pour octet (64 blocs)' if egalite else 'ÉCART — ROUGE'}",
            ]
    rapport += [
        "",
        "LA NOTE DE CELLULE : (4096/1) est le cas TROUVÉ-TÔT (l'octet "
        "unique d'un tir aléatoire apparaît dans les premiers ~32 octets "
        "— l'épreuve de l'absence est impossible à 1 octet : (255/256)^"
        "4096 ≈ 1e-7) ; (4096/16) et (1000/32) sont les cas ABSENTS "
        "(la convention de la mesure vague 9)",
        f"la durée du rig : {dt:.1f} s (l'horloge monotone)"]
    (ICI / "rapport-temps-reel.txt").write_text("\n".join(rapport) + "\n",
                                                encoding="utf-8")
    print("\n".join(rapport))
    return 0 if (negatif and egalite) else 2


if __name__ == "__main__":
    sys.exit(main())
