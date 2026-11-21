#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE COULOIR GHASH EN PCLMULQDQ (0g3400vql, la vague 13) — la campagne
complète : les deux notations (Karatsuba 3× / schoolbook 4×), la sonde de
session hissée, la parité contre le scellé tls13-17 (le juge), les vecteurs
NIST, le temps-constant structurel, le rig natif (AES-GCM complet et SHA-256
complet face à OpenSSL EVP), le registre.

Le plan gelé sha256:caab6f481ab3799f… AVANT toute mesure (EMPREINTES-PLANS-VAGUE13).
"""
import contextlib
import hashlib
import io
import json
import pathlib
import random
import subprocess
import sys
import time

import capstone
import keystone
import unicorn

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = pathlib.Path(__file__).resolve().parent
KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

RVA = {"sonde": 0xE600, "karatsuba": 0xE800, "schoolbook": 0xEA00,
       "v4i": 0xEC00, "shani": 0xEF00}
SC17 = 0xDFC0          # le scellé GHASH (sa copie au slot canonique)
SC18 = 0xE080          # le scellé GCM sceller (copie au slot canonique)
SC02 = 0xC080          # le scellé SHA-256 compression
SC15, SC16 = 0xDCC0, 0xDF00

# ---------------------------------------------------------------- utilitaires
def charger_module(nom, chemin):
    import importlib.util
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
            corps_list.append(corps)
            try:
                c, _ = KS.asm(corps, adr)
                adr += len(bytes(c))
            except Exception:
                adr += 6
    octets = b""
    for corps in corps_list:
        for e, a in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
            corps = corps.replace(e, hex(a))
        c, _ = KS.asm(corps, rva + len(octets))
        octets += bytes(c)
    return octets


def round_trip(octets: bytes, rva: int) -> bool:
    reins = b""
    for ins in CS.disasm(octets, rva):
        c, _ = KS.asm(f"{ins.mnemonic} {ins.op_str}", ins.address)
        reins += bytes(c)
    return reins == octets


def ctable(nom, octets: bytes) -> str:
    lignes = []
    for i in range(0, len(octets), 16):
        lignes.append("  " + ", ".join(f"0x{b:02x}" for b in octets[i:i+16]) + ",")
    return f"static const unsigned char {nom}[] = {{\n" + "\n".join(lignes) + "\n};\n"


def garde_sceau(quand: str) -> dict:
    """la garde du sceau-I 14/14 (lève EchecSceauI au rouge) + les quatre
    pièces aux ancres R7."""
    SI = charger_module("si_ghash", REPO / "v06" / "sceau_I.py")
    SI.garde(list(SI.ARBRES))          # fail-closed : lève au premier écart
    pieces = {}
    for nom, chemin in [("loupe.exe", "loupe/loupe.exe"),
                        ("proxy.exe", "tls13/proxy.exe"),
                        ("selftest.exe", "m1/selftest.exe"),
                        ("demo.exe", "demo/demo.exe")]:
        pieces[nom] = hashlib.sha256((REPO / chemin).read_bytes()).hexdigest()
    print(f"[garde du sceau {quand}] 14/14 VERT ; pièces R7 recoupées "
          f"({', '.join(n + ' ' + h[:8] for n, h in pieces.items())})")
    return {"pieces": pieces, "ok": True}


# ------------------------------------------------- le juge GHASH en python ---
def ghash_juge(NX: int, NY: int) -> int:
    """la sémantique du scellé tls13-17 — VÉRIFIÉE contre le GCM réel d'EVP
    (le tag reconstitué par deux multiplications chaînées, identique)."""
    def rev128(v):
        r = 0
        for i in range(128):
            r |= ((v >> (127 - i)) & 1) << i
        return r
    def clmul(a, b):
        r = 0
        while b:
            if b & 1:
                r ^= a
            b >>= 1
            a <<= 1
        return r
    def polymod(t):
        while t.bit_length() > 128:
            k = t.bit_length() - 129
            t ^= ((1 << 128) | 0x87) << k
        return t
    return rev128(polymod(clmul(rev128(NX), rev128(NY))))


# ------------------------------------------------------------- l'UNICORN -----
def rig_unicorn():
    """le banc NU : les blocs GHASH sont des FEUILLES (aucun IAT, aucun shim)
    — l'émulation directe, la page du trou 0xD000 mappée pour les slots
    canoniques (le juge tls13-17 à 0xDFC0, le repli y saute)."""
    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    uc.mem_map(0xC000, 0x4000)          # les scellés + les marges
    uc.mem_map(0x700000, 0x10000)       # la pile du banc
    uc.mem_map(0x500000, 0x21000)       # les tampons X/Y/Z
    return uc


RET = b"\xC3"

def appeler_ghash(uc, fn, X: bytes, Y: bytes, r10: int):
    uc.mem_write(0x500400, X)
    uc.mem_write(0x500600, Y)
    uc.mem_write(0x500800, b"\xAA" * 16)
    uc.mem_write(0x700100, RET)
    uc.mem_write(0x708000, (0x700100).to_bytes(8, "little"))  # l'adresse de retour
    uc.reg_write(unicorn.x86_const.UC_X86_REG_RSP, 0x708000)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_RCX, 0x500800)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_RDX, 0x500400)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_R8, 0x500600)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_R9, 0)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_R10, r10)
    uc.emu_start(fn, 0x700100)
    return {"rax": uc.reg_read(unicorn.x86_const.UC_X86_REG_RAX)}, \
        bytes(uc.mem_read(0x500800, 16))


def unicorne(o_k, o_sb, o_s17):
    emul = rig_unicorn()
    emul.mem_write(RVA["karatsuba"], o_k)
    emul.mem_write(RVA["schoolbook"], o_sb)
    emul.mem_write(SC17, o_s17)
    emul.ctl_remove_cache(0xC000, 0x10000)
    rng = random.Random(20261121)
    res = {"diff": {}, "punition": {}, "commut": 0, "intact": 0, "repli": 0,
           "mutant": None, "comptes": {}}

    # la différentielle 256/256 + 64/64 contre le scellé (octet pour octet)
    for nom, o in [("karatsuba", o_k), ("schoolbook", o_sb)]:
        div = []
        for i in range(256 + 64):
            X = bytes(rng.getrandbits(8) for _ in range(16))
            Y = bytes(rng.getrandbits(8) for _ in range(16))
            r, Z = appeler_ghash(emul, RVA[nom], X, Y, 1)
            _, Zs = appeler_ghash(emul, SC17, X, Y, 0)
            if Z != Zs or (r["rax"] & (2**64 - 1)) != 0:
                div.append(i)
        res["diff"][nom] = {"vecteurs": 320, "divergences": len(div)}

    # les cas punitifs (X=0, Y=0, X=Y=R, identité réfléchie, X=Y=1)
    Rb = (0xE1 << 120).to_bytes(16, "big")
    un = (1).to_bytes(16, "big")
    zero = bytes(16)
    for nom, o in [("karatsuba", o_k), ("schoolbook", o_sb)]:
        okp = 0
        for X, Y in [(zero, zero), (un, zero), (zero, un), (Rb, Rb), (un, un),
                     (Rb, zero), (un, Rb)]:
            _, Z = appeler_ghash(emul, RVA[nom], X, Y, 1)
            juge = ghash_juge(int.from_bytes(X, "big"), int.from_bytes(Y, "big"))
            okp += (Z == juge.to_bytes(16, "big"))
        res["punition"][nom] = f"{okp}/7"

    # la commutativité + X/Y INTACTS (le contrat du scellé)
    for nom in ("karatsuba", "schoolbook"):
        okc = oki = 0
        for _ in range(32):
            X = bytes(rng.getrandbits(8) for _ in range(16))
            Y = bytes(rng.getrandbits(8) for _ in range(16))
            _, Z1 = appeler_ghash(emul, RVA[nom], X, Y, 1)
            oki += (bytes(emul.mem_read(0x500400, 16)) == X
                    and bytes(emul.mem_read(0x500600, 16)) == Y)
            _, Z2 = appeler_ghash(emul, RVA[nom], Y, X, 1)
            okc += (Z1 == Z2)
        res["commut" if nom == "karatsuba" else "commut_sb"] = okc
        res["intact" if nom == "karatsuba" else "intact_sb"] = oki

    # LE REPLI : r10 = 0 → le couloir saute au scellé — identique au scellé
    okr = 0
    for _ in range(32):
        X = bytes(rng.getrandbits(8) for _ in range(16))
        Y = bytes(rng.getrandbits(8) for _ in range(16))
        _, Zr = appeler_ghash(emul, RVA["karatsuba"], X, Y, 0)
        _, Zs = appeler_ghash(emul, SC17, X, Y, 0)
        okr += (Zr == Zs)
    res["repli"] = f"{okr}/32"

    # LE MUTANT : un octet du corps pclmulqdq muté → ATTRAPÉ au premier vecteur
    mut = bytearray(o_k)
    trouve = None
    for ins in CS.disasm(bytes(mut), RVA["karatsuba"]):
        if ins.mnemonic == "pclmulqdq":
            trouve = ins.address - RVA["karatsuba"] + ins.size - 1  # l'imm8
            break
    assert trouve is not None
    mut[trouve] ^= 0x01          # l'imm8 du premier clmul : 0x00 → 0x01
    emul.mem_write(0x501000, bytes(mut))
    emul.ctl_remove_cache(0x501000, 0x502000)
    X = bytes(rng.getrandbits(8) for _ in range(16))
    Y = bytes(rng.getrandbits(8) for _ in range(16))
    _, Zm = appeler_ghash(emul, 0x501000, X, Y, 1)
    _, Zs = appeler_ghash(emul, SC17, X, Y, 0)
    res["mutant"] = "ATTRAPÉ au premier vecteur" if Zm != Zs else "PAS ATTRAPÉ (rouge!)"

    # le compte d'instructions (l'enveloppe comprise — du premier octet du
    # prologue au ret, la convention du plan)
    emul2 = rig_unicorn()          # le rig NEUF (les hooks d'un uc
    emul2.mem_write(RVA["karatsuba"], o_k)      # surchargé périssent — vécu,
    emul2.mem_write(RVA["schoolbook"], o_sb)    # nommé, le rig frais pris)
    emul2.ctl_remove_cache(0xC000, 0x10000)
    for nom in ("karatsuba", "schoolbook"):
        cpt = {"n": 0}
        def hook_cpt(uc, adresse, taille, donnees):
            cpt["n"] += 1
        h = emul2.hook_add(unicorn.UC_HOOK_CODE, hook_cpt)
        X = bytes(rng.getrandbits(8) for _ in range(16))
        Y = bytes(rng.getrandbits(8) for _ in range(16))
        appeler_ghash(emul2, RVA[nom], X, Y, 1)
        emul2.hook_del(h)
        res["comptes"][nom] = cpt["n"]
    return res, emul2


def trace_hash(emul_inutile, o_k):
    """le temps-constant STRUCTUREL : le hash de la trace COMPLÈTE (adresses +
    tailles, les VALEURS JAMAIS) — deux classes × 60 mesures, UNE empreinte
    par classe attendue ; LA CONVENTION NEUVE : aucune instruction à latence
    variable (div, idiv, cpuid, rdtsc) sur le chemin des secrets."""
    classes = {
        "aleatoire": [bytes(random.Random(1000 + i).getrandbits(8) for _ in range(16)) for i in range(60)],
        "structurée": [(b"\x00" * 15 + bytes([i])) if i % 2 else
                       ((0xE1 << 120).to_bytes(16, "big")[:-1] + bytes([i]))
                       for i in range(60)],
    }
    res = {}
    blacklisted = {"div", "idiv", "cpuid", "rdtsc", "rdtscp"}
    vues = set()
    emul = rig_unicorn()               # le rig frais (les traces JAMAIS vides)
    emul.mem_write(RVA["karatsuba"], o_k)
    emul.ctl_remove_cache(0xC000, 0x10000)
    for classe, vecs in classes.items():
        empreintes = set()
        instrs = set()
        for X in vecs:
            Y = X[::-1]
            trace = []
            cpt = {"n": 0}
            def hook(uc, adresse, taille, donnees):
                cpt["n"] += 1
                trace.append((adresse, taille))
            h = emul.hook_add(unicorn.UC_HOOK_CODE, hook)
            appeler_ghash(emul, RVA["karatsuba"], X, Y, 1)
            emul.hook_del(h)
            empreintes.add(hashlib.sha256(
                json.dumps(trace).encode()).hexdigest())
            if not instrs:
                for ins in CS.disasm(o_k, RVA["karatsuba"]):
                    instrs.add(ins.mnemonic)
        res[classe] = {"empreintes": len(empreintes), "n": len(vecs)}
        vues |= instrs
    res["latence_variable"] = sorted(vues & blacklisted)
    res["instructions"] = sorted(vues)
    return res


# ------------------------------------------------------------- le rig C -----
def generer_rig(o_k, o_sb, o_sonde, o_v4i, o_shani, o_s02, o_s15, o_s16,
                o_s17, o_s18, k_table):
    return f"""/* ghash_rig.c — LE RIG NATIF (0g3400vql) — généré par mesurer_ghash.py */
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <openssl/evp.h>
#include <sys/mman.h>
#include <stdlib.h>
{ctable("ghashk", o_k)}{ctable("ghashsb", o_sb)}{ctable("sonde", o_sonde)}
{ctable("v4i", o_v4i)}{ctable("shani", o_shani)}{ctable("s02", o_s02)}
{ctable("s15", o_s15)}{ctable("s16", o_s16)}{ctable("s17", o_s17)}{ctable("s18", o_s18)}
{ctable("ktable", k_table)}
static void pose_page(unsigned long base, size_t taille) {{
    void *p = mmap((void*)base, taille, PROT_READ|PROT_WRITE|PROT_EXEC,
                   MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE, -1, 0);
    if (p == MAP_FAILED) {{ perror("mmap"); exit(3); }}
}}
static long appeler_msx64(unsigned long fn, unsigned long rcx_v,
                          unsigned long rdx_v, unsigned long r8_v,
                          unsigned long r9_v, unsigned long pile_v) {{
    long ret;
    __asm__ volatile(
        "subq $0x30, %%rsp\\n\\t"
        "movq %6, 0x20(%%rsp)\\n\\t"
        "movq %2, %%rcx\\n\\t"
        "movq %3, %%rdx\\n\\t"
        "movq %4, %%r8\\n\\t"
        "movq %5, %%r9\\n\\t"
        "callq *%1\\n\\t"
        "movq %%rax, %0\\n\\t"
        "addq $0x30, %%rsp\\n\\t"
        : "=r"(ret)
        : "r"(fn), "r"(rcx_v), "r"(rdx_v), "r"(r8_v), "r"(r9_v), "r"(pile_v)
        : "rax", "rbx", "rcx", "rdx", "r8", "r9", "r10", "r11", "cc", "memory");
    return ret;
}}
static long appeler_r10(unsigned long fn, unsigned long rcx_v,
                        unsigned long rdx_v, unsigned long r8_v,
                        unsigned long r9_v, unsigned long pile_v,
                        unsigned long r10_v) {{
    long ret;
    __asm__ volatile(
        "subq $0x30, %%rsp\\n\\t"
        "movq %7, 0x20(%%rsp)\\n\\t"
        "movq %2, %%rcx\\n\\t"
        "movq %3, %%rdx\\n\\t"
        "movq %4, %%r8\\n\\t"
        "movq %5, %%r9\\n\\t"
        "movq %6, %%r10\\n\\t"
        "callq *%1\\n\\t"
        "movq %%rax, %0\\n\\t"
        "addq $0x30, %%rsp\\n\\t"
        : "=r"(ret)
        : "r"(fn), "r"(rcx_v), "r"(rdx_v), "r"(r8_v), "r"(r9_v),
          "r"(r10_v), "r"(pile_v)
        : "rax", "rbx", "rcx", "rdx", "r8", "r9", "r10", "r11", "cc", "memory");
    return ret;
}}
/* le relais du scellé tls13-18 (appeler_s18.S — pur asm, la convention
   msx64 posée à la main, AUCUNE contrainte gcc) */
extern long appeler_s18(unsigned long rk, unsigned long nonce,
                        unsigned long clair, unsigned long n,
                        unsigned long aad, unsigned long na,
                        unsigned long ct, unsigned long tag);
static inline unsigned long long rdtscp32(void) {{
    unsigned aux, lo, hi;
    __asm__ volatile("rdtscp" : "=a"(lo), "=d"(hi), "=c"(aux) :: "memory");
    return ((unsigned long long)hi << 32) | lo;
}}
static uint64_t xs = 20261121ULL;
static inline uint64_t nxt64(void) {{
    xs ^= xs << 13; xs ^= xs >> 7; xs ^= xs << 17;
    return xs;
}}
static void med_iqr(unsigned long long *cyc, int n,
                    unsigned long long *med, unsigned long long *iqr) {{
    for (int i = 1; i < n; i++) {{
        unsigned long long v = cyc[i];
        int j = i - 1;
        while (j >= 0 && cyc[j] > v) {{ cyc[j+1] = cyc[j]; j--; }}
        cyc[j+1] = v;
    }}
    *med = (cyc[n/2-1] + cyc[n/2]) / 2;
    *iqr = cyc[3*n/4] - cyc[n/4];
}}
#define N_MES 20
static unsigned long long cyc[N_MES];
#define MESURE(nom, div, expr) do {{ \\
    for (int r = 0; r < 3; r++) {{ (void)(expr); }} \\
    for (int r = 0; r < N_MES; r++) {{ \\
        unsigned long long t0 = rdtscp32(); \\
        (void)(expr); \\
        cyc[r] = rdtscp32() - t0; \\
    }} \\
    unsigned long long med, iqr; med_iqr(cyc, N_MES, &med, &iqr); \\
    printf("MESURE %-22s %llu %llu %.4f %.4f\\n", nom, med, iqr, \\
           (double)med/(double)(div), (double)iqr/(double)(div)); \\
}} while(0)

/* ---- le GCM du rig : la composition (le calendrier scellé, la porteuse
   v4-inline pour le CTR, le couloir/scellé GHASH par bloc, l'étiquette) ---- */
static void gcm_rig(unsigned long fn_ghash, int pclmul,
                    const unsigned char *cle, const unsigned char *nonce,
                    const unsigned char *clair, size_t n,
                    const unsigned char *aad, size_t na,
                    unsigned char *ct, unsigned char *tag) {{
    unsigned char rk[176];
    appeler_msx64({SC15}, (unsigned long)cle, (unsigned long)rk, 0, 0, 0);
    /* H = E(K, 0) ; EJ0 = E(K, J0) : la porteuse, DEUX blocs, UN appel */
    unsigned char in0[32], out0[32];
    memset(in0, 0, 16);
    memcpy(in0 + 16, nonce, 12); in0[28] = 0; in0[29] = 0; in0[30] = 0; in0[31] = 1;
    appeler_msx64({RVA["v4i"]}, (unsigned long)rk, (unsigned long)in0, (unsigned long)out0, 2, 0);
    unsigned char H[16], EJ0[16];
    memcpy(H, out0, 16); memcpy(EJ0, out0 + 16, 16);
    if (getenv("GHDBG")) {{
        printf("  rig H  : "); for (int i=0;i<16;i++) printf("%02x", H[i]); printf("\\n");
        printf("  rig EJ0: "); for (int i=0;i<16;i++) printf("%02x", EJ0[i]); printf("\\n");
    }}
    /* le CTR : J0+1 .. J0+n (inc32 gros-boutiste) */
    unsigned char *cbs = malloc(16 * (n ? (n + 15) / 16 : 1));
    uint32_t ctr = 2;   /* le CTR démarre à inc32(J0) = J0+1 */
    for (size_t b = 0; b < (n ? (n + 15) / 16 : 1); b++) {{
        memcpy(cbs + 16*b, nonce, 12);
        cbs[16*b+12] = (unsigned char)(ctr >> 24); cbs[16*b+13] = (unsigned char)(ctr >> 16);
        cbs[16*b+14] = (unsigned char)(ctr >> 8);  cbs[16*b+15] = (unsigned char)ctr;
        ctr++;
    }}
    size_t nb = n ? (n + 15) / 16 : 0;
    unsigned char *ks = malloc(16 * (nb ? nb : 1));
    if (nb) appeler_msx64({RVA["v4i"]}, (unsigned long)rk, (unsigned long)cbs, (unsigned long)ks, nb, 0);
    if (getenv("GHDBG")) {{
        printf("  rig ks0: "); for (int i=0;i<16;i++) printf("%02x", ks[i]); printf("\\n");
    }}
    for (size_t i = 0; i < n; i++) ct[i] = clair[i] ^ ks[i];
    /* le GHASH : Y = 0 ; Y = (Y ⊕ X_i) • H par bloc (AAD || CT || L) —
       le flux par CURSEUR D'OCTETS (les blocs partiels paddés à zéro) */
    unsigned char *flux = malloc(16 * (na/16 + nb + 8 + 2));
    unsigned char *pc = flux;
    for (size_t i = 0; i < na; i++) *pc++ = aad[i];
    while ((pc - flux) % 16) *pc++ = 0;          /* le pad du dernier bloc AAD */
    for (size_t i = 0; i < n; i++) *pc++ = ct[i];
    while ((pc - flux) % 16) *pc++ = 0;          /* le pad du dernier bloc CT */
    uint64_t ab = (uint64_t)na * 8, cb = (uint64_t)n * 8;
    memset(pc, 0, 16);
    for (int i = 0; i < 8; i++) pc[i] = (unsigned char)(ab >> (56 - 8*i));
    for (int i = 0; i < 8; i++) pc[8 + i] = (unsigned char)(cb >> (56 - 8*i));
    pc += 16;
    size_t nf = (size_t)(pc - flux) / 16;
    unsigned char Y[16]; memset(Y, 0, 16);
    for (size_t b = 0; b < nf; b++) {{
        unsigned char tmp[16];
        for (int i = 0; i < 16; i++) tmp[i] = Y[i] ^ flux[16*b + i];
        appeler_r10(fn_ghash, (unsigned long)(0x500800), (unsigned long)tmp,
                    (unsigned long)H, 0, 0, pclmul ? 1 : 0);
        memcpy(Y, (void*)0x500800, 16);
    }}
    for (int i = 0; i < 16; i++) tag[i] = EJ0[i] ^ Y[i];
    free(cbs); free(ks); free(flux);
}}

static int evp_gcm(const unsigned char *cle, int bits,
                   const unsigned char *nonce, const unsigned char *clair, size_t n,
                   const unsigned char *aad, size_t na,
                   unsigned char *ct, unsigned char *tag) {{
    const EVP_CIPHER *c = bits == 128 ? EVP_aes_128_gcm() : EVP_aes_256_gcm();
    EVP_CIPHER_CTX *x = EVP_CIPHER_CTX_new();
    int l;
    EVP_EncryptInit_ex(x, c, NULL, NULL, NULL);
    EVP_CIPHER_CTX_ctrl(x, EVP_CTRL_GCM_SET_IVLEN, 12, NULL);
    EVP_EncryptInit_ex(x, NULL, NULL, cle, nonce);
    EVP_EncryptUpdate(x, NULL, &l, aad, na);
    EVP_EncryptUpdate(x, ct, &l, clair, n);
    EVP_EncryptFinal_ex(x, ct + n, &l);
    EVP_CIPHER_CTX_ctrl(x, EVP_CTRL_GCM_GET_TAG, 16, tag);
    EVP_CIPHER_CTX_free(x);
    return 0;
}}

/* le SHA-256 du rig : la composition (init C + la compression scellée/couloir
   par bloc de 64 octets + le padding) */
static const uint32_t IV256[8] = {{0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
                              0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19}};
static void sha_rig(unsigned long fn_comp, unsigned char *etat,
                    const unsigned char *msg, size_t n) {{
    uint32_t *st = (uint32_t*)etat;
    for (int i = 0; i < 8; i++) st[i] = IV256[i];
    size_t totale = ((n + 8) / 64 + 1) * 64;
    unsigned char *buf = malloc(totale);
    memset(buf, 0, totale);
    memcpy(buf, msg, n);
    buf[n] = 0x80;
    uint64_t bits = (uint64_t)n * 8;
    for (int i = 0; i < 8; i++) buf[totale - 1 - i] = (unsigned char)(bits >> (8*i));
    for (size_t b = 0; b < totale / 64; b++)
        appeler_msx64(fn_comp, (unsigned long)etat, (unsigned long)(buf + 64*b), 0, 0, 0);
    free(buf);
}}
int main(void) {{
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(1, &m);
    if (sched_setaffinity(0, sizeof(m), &m) != 0) perror("affinité");
    pose_page(0xC000, 0x4000);
    pose_page(0x2000, 0x2000);   /* la page de la table K (0x2F00) */
    pose_page(0x500000, 0x21000);
    memcpy((void*){RVA["karatsuba"]}, ghashk, sizeof(ghashk));
    memcpy((void*){RVA["schoolbook"]}, ghashsb, sizeof(ghashsb));
    memcpy((void*){RVA["sonde"]}, sonde, sizeof(sonde));
    memcpy((void*){RVA["v4i"]}, v4i, sizeof(v4i));
    memcpy((void*){RVA["shani"]}, shani, sizeof(shani));
    memcpy((void*){SC02}, s02, sizeof(s02));
    memcpy((void*){SC15}, s15, sizeof(s15));
    memcpy((void*){SC16}, s16, sizeof(s16));
    memcpy((void*){SC17}, s17, sizeof(s17));
    memcpy((void*){SC18}, s18, sizeof(s18));
    memcpy((void*)0x2F00, ktable, sizeof(ktable));
    __builtin___clear_cache((char*)0x2F00, (char*)0x4000);
    __builtin___clear_cache((char*)0xC000, (char*)0x10000);

    /* (0) LA SONDE DE SESSION — UNE FOIS, le verdict sous rax/r10 */
    long verdict = appeler_msx64({RVA["sonde"]}, 0, 0, 0, 0, 0);
    printf("SONDE verdict=%ld pclmul=%ld aes=%ld sha=%ld\\n",
           verdict, verdict & 1, (verdict >> 1) & 1, (verdict >> 2) & 1);
    int pcl = verdict & 1;

    /* (1) la parité : le rig-GCM (couloir) == le scellé tls13-18 == EVP-128 */
    unsigned char cle[16], nonce[12];
    for (int i = 0; i < 16; i++) cle[i] = (unsigned char)(i*7+1);
    for (int i = 0; i < 12; i++) nonce[i] = (unsigned char)(i*11+3);
    int parite = 0, parite_s = 0, parite_e = 0;
    for (int v = 0; v < 25; v++) {{
        unsigned char clair[80], aad[32], ct1[80], ct2[80], cte[80];
        unsigned char t1[16], t2[16], te[16];
        size_t n = 16 + (v * 3) % 64, na = (v % 2) ? 32 : 0;
        for (size_t i = 0; i < n; i++) clair[i] = (unsigned char)nxt64();
        for (size_t i = 0; i < na; i++) aad[i] = (unsigned char)nxt64();
        gcm_rig({RVA["karatsuba"]}, 1, cle, nonce, clair, n, aad, na, ct1, t1);
        gcm_rig({SC17}, 0, cle, nonce, clair, n, aad, na, ct2, t2);
        evp_gcm(cle, 128, nonce, clair, n, aad, na, cte, te);
        /* le scellé tls13-18 (l'appel complet) */
        unsigned char rk[176];
        appeler_msx64({SC15}, (unsigned long)cle, (unsigned long)rk, 0, 0, 0);
        unsigned char *ctsc = malloc(n + 32), *tagsc = malloc(16);
        long rs18 = appeler_s18((unsigned long)rk, (unsigned long)nonce, (unsigned long)clair, n,
                    (unsigned long)aad, na, (unsigned long)ctsc, (unsigned long)tagsc);
        if (v == 0) {{
            printf("DEBUG v0: n=%zu na=%zu rs18=%ld\\n", n, na, rs18);
            printf("  rig ct: "); for (size_t i=0;i<n;i++) printf("%02x", ct1[i]); printf("\\n");
            printf("  sc ct: "); for (size_t i=0;i<n;i++) printf("%02x", ctsc[i]); printf("\\n");
            printf("  rig tag: "); for (int i=0;i<16;i++) printf("%02x", t1[i]); printf("\\n");
            printf("  sc tag: "); for (int i=0;i<16;i++) printf("%02x", tagsc[i]); printf("\\n");
            printf("  evp ct: "); for (size_t i=0;i<n;i++) printf("%02x", cte[i]); printf("\\n");
            printf("  evp tag: "); for (int i=0;i<16;i++) printf("%02x", te[i]); printf("\\n");
        }}
        parite += (memcmp(ct1, ct2, n) == 0 && memcmp(t1, t2, 16) == 0);
        parite_s += (memcmp(ct1, ctsc, n) == 0 && memcmp(t1, tagsc, 16) == 0);
        parite_e += (memcmp(ct1, cte, n) == 0 && memcmp(t1, te, 16) == 0);
        free(ctsc); free(tagsc);
    }}
    printf("PARITE couloir==scelle17 %d/25 ; couloir==scelle18 %d/25 ; couloir==EVP %d/25\\n",
           parite, parite_s, parite_e);

    /* (2) la parité SHA : le couloir SHA-NI == le scellé 02 == EVP_sha256 */
    unsigned char msg[4096], etat1[32], etat2[32], dgst[32];
    for (int i = 0; i < 4096; i++) msg[i] = (unsigned char)nxt64();
    sha_rig({RVA["shani"]}, etat1, msg, 4096);
    sha_rig({SC02}, etat2, msg, 4096);
    EVP_Digest(msg, 4096, dgst, NULL, EVP_sha256(), NULL);
    /* l'état BE -> le digest : les mots gros-boutistes */
    unsigned char d1[32], d2[32];
    for (int i = 0; i < 8; i++) {{
        uint32_t w1 = (uint32_t)etat1[4*i] | ((uint32_t)etat1[4*i+1] << 8)
                    | ((uint32_t)etat1[4*i+2] << 16) | ((uint32_t)etat1[4*i+3] << 24);
        uint32_t w2 = (uint32_t)etat2[4*i] | ((uint32_t)etat2[4*i+1] << 8)
                    | ((uint32_t)etat2[4*i+2] << 16) | ((uint32_t)etat2[4*i+3] << 24);
        for (int k = 0; k < 4; k++) {{ d1[4*i+k] = (unsigned char)(w1 >> (24-8*k)); d2[4*i+k] = (unsigned char)(w2 >> (24-8*k)); }}
    }}
    printf("PARITE shani==scelle02 %d ; shani==EVP %d\\n",
           memcmp(d1, d2, 32) == 0, memcmp(d1, dgst, 32) == 0);

    /* (3) LES MESURES : RDTSCP, n=20, médiane non arrondie + IQR --------- */
    unsigned char X[16], Y[16], Z[16];
    for (int i = 0; i < 16; i++) {{ X[i] = (unsigned char)nxt64(); Y[i] = (unsigned char)nxt64(); }}
    memcpy((void*)0x500400, X, 16); memcpy((void*)0x500600, Y, 16);
    /* le stub calibré */
    *(unsigned char*)0xF800 = 0xC3;
    MESURE("stub", 1, appeler_msx64(0xF800, 0, 0, 0, 0, 0));
    /* le GHASH : 100 multiplications par mesure (l'unité au-dessus du bruit RDTSCP,
       le protocole NOMMÉ : cycles par multiplication) */
    #define GH100(fn, r10v) ({{ for (int i = 0; i < 100; i++) \
        appeler_r10(fn, 0x500800, 0x500400, 0x500600, 0, 0, r10v); 0; }})
    MESURE("ghash-karatsuba", 100, GH100({RVA["karatsuba"]}, 1));
    MESURE("ghash-schoolbook", 100, GH100({RVA["schoolbook"]}, 1));
    MESURE("ghash-scelle", 100, GH100({SC17}, 0));
    /* l'AES-GCM complet : 64 octets et 4096 octets */
    {{
        unsigned char clair64[64], ct64[64], t64[16];
        unsigned char clair4k[4096], ct4k[4096], t4k[16];
        unsigned char aad0[1];
        for (int i = 0; i < 64; i++) clair64[i] = (unsigned char)nxt64();
        for (int i = 0; i < 4096; i++) clair4k[i] = (unsigned char)nxt64();
        MESURE("gcm-couloir@64", 64, gcm_rig({RVA["karatsuba"]}, 1, cle, nonce, clair64, 64, aad0, 0, ct64, t64));
        MESURE("gcm-scelle17@64", 64, gcm_rig({SC17}, 0, cle, nonce, clair64, 64, aad0, 0, ct64, t64));
        MESURE("gcm-scelle18@64", 64, ({{
            unsigned char rk[176]; unsigned char *cts = malloc(64+32), *ts = malloc(16);
            appeler_msx64({SC15}, (unsigned long)cle, (unsigned long)rk, 0, 0, 0);
            appeler_s18((unsigned long)rk, (unsigned long)nonce, (unsigned long)clair64, 64,
                        0, 0, (unsigned long)cts, (unsigned long)ts);
            free(cts); free(ts); }}));
        MESURE("gcm-evp128@64", 64, evp_gcm(cle, 128, nonce, clair64, 64, aad0, 0, ct64, t64));
        MESURE("gcm-evp256@64", 64, evp_gcm(cle, 256, nonce, clair4k, 64, aad0, 0, ct64, t64));
        MESURE("gcm-couloir@4096", 4096, gcm_rig({RVA["karatsuba"]}, 1, cle, nonce, clair4k, 4096, aad0, 0, ct4k, t4k));
        MESURE("gcm-scelle17@4096", 4096, gcm_rig({SC17}, 0, cle, nonce, clair4k, 4096, aad0, 0, ct4k, t4k));
        MESURE("gcm-scelle18@4096", 4096, ({{
            unsigned char rk[176]; unsigned char *cts = malloc(4096+32), *ts = malloc(16);
            appeler_msx64({SC15}, (unsigned long)cle, (unsigned long)rk, 0, 0, 0);
            appeler_s18((unsigned long)rk, (unsigned long)nonce, (unsigned long)clair4k, 4096,
                        0, 0, (unsigned long)cts, (unsigned long)ts);
            free(cts); free(ts); }}));
        MESURE("gcm-evp128@4096", 4096, evp_gcm(cle, 128, nonce, clair4k, 4096, aad0, 0, ct4k, t4k));
        MESURE("gcm-evp256@4096", 4096, evp_gcm(cle, 256, nonce, clair4k, 4096, aad0, 0, ct4k, t4k));
        /* le SHA-256 complet : 4096 octets */
        MESURE("sha-shani@4096", 4096, sha_rig({RVA["shani"]}, etat1, msg, 4096));
        MESURE("sha-scelle@4096", 4096, sha_rig({SC02}, etat2, msg, 4096));
        MESURE("sha-evp@4096", 4096, EVP_Digest(msg, 4096, dgst, NULL, EVP_sha256(), NULL));
    }}
    printf("FIN\\n");
    return 0;
}}
"""


def main() -> int:
    t0 = time.monotonic()
    rapport = []
    a = rapport.append

    garde = garde_sceau("AVANT")

    # ---- les notations -----------------------------------------------------
    NOT = ICI / "notation"
    o_k = assembler(NOT / "ghash-pclmulqdq-karatsuba.asm", RVA["karatsuba"])
    o_sb = assembler(NOT / "ghash-pclmulqdq-schoolbook.asm", RVA["schoolbook"])
    o_sonde = assembler(NOT / "sonde-session.asm", RVA["sonde"])
    for d in ("m4", "m3", "m2", "m1", "tls13", "loupe"):
        p = str(REPO / d)
        if p not in sys.path:
            sys.path.insert(0, p)
    B4 = charger_module("b4_ghash", REPO / "m4" / "build_m4.py")
    lay = charger_module("lay_ghash", REPO / "tls13" / "layout.py")
    o_v4i = assembler(REPO / "atelier-porteuse-ahult8jgd" / "notation" /
                      "tls13-16-ni-v4-inline.asm", RVA["v4i"])
    FNV_NOT = REPO / "atelier-corridors-fnvan0zes" / "notation" / "tls13-02-shani.asm"

    def assembler_shani(fichier: pathlib.Path, rva: int) -> bytes:
        """l'assembleur du corridor SHA-NI : étiquettes + lignes db + les
        symboles @MASQUE/@Knn en rip-relatif (le correctif keystone 0.9.2 :
        les déplacements NÉGATIFS en [rip - 0x…], jamais [rip + -0x…])."""
        import re as _re
        lignes = [l.split(";")[0].strip() for l in fichier.read_text(
            encoding="utf-8").splitlines()]

        def taille(ligne, adresse=0):
            if ligne.startswith("db "):
                return len(ligne[3:].split())
            prov = _re.sub(r"@[A-Za-z_0-9]+", "0x0", ligne)
            c, _ = KS.asm(prov, adresse)
            return len(bytes(c))

        etiquettes: dict[str, int] = {}
        pos_masque = None
        for _ in range(4):
            adr = rva
            apres_align = False
            for ligne in lignes:
                if not ligne:
                    continue
                if ligne.endswith(":") and ligne.startswith("."):
                    etiquettes[ligne[:-1]] = adr
                    continue
                if ligne.startswith("align "):
                    n = int(ligne.split()[1])
                    adr = (adr + n - 1) & ~(n - 1)
                    apres_align = True
                    continue
                if apres_align:
                    pos_masque = adr
                    apres_align = False
                prov = ligne
                for e, ad in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
                    if e in prov:
                        prov = prov.replace(e, hex(ad))
                try:
                    adr += taille(prov, adr)
                except Exception:
                    adr += 6
        fin_code = adr
        cible_masque = pos_masque if pos_masque is not None else fin_code

        def rip_disp(cible, adresse, t):
            d = cible - (adresse + t)
            return (f"[rip - {-d:#x}]" if d < 0 else f"[rip + {d:#x}]")

        octets = b""
        for ligne in lignes:
            if not ligne:
                continue
            if ligne.endswith(":") and ligne.startswith("."):
                continue
            if ligne.startswith("align "):
                n = int(ligne.split()[1])
                while (rva + len(octets)) % n:
                    octets += b"\x90"
                continue
            if ligne.startswith("db "):
                octets += bytes(int(b, 16) for b in ligne[3:].split())
                continue
            adresse = rva + len(octets)
            corr = ligne
            for e, ad in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
                if e in corr:
                    corr = corr.replace(e, hex(ad))
            if "@MASQUE" in corr:
                t = taille(_re.sub(r"@[A-Za-z_0-9]+", "0x0", corr), adresse)
                corr = corr.replace("[rip + @MASQUE]",
                                    rip_disp(cible_masque, adresse, t))
            m = _re.search(r"@\w+", corr)
            if m and m.group(0).startswith("@K"):
                nn = int(m.group(0)[2:])
                cible = 0x2F00 + 4 * nn
                t = taille(corr.replace(m.group(0), "0x0"), adresse)
                corr = corr.replace(f"[rip + {m.group(0)}]",
                                    rip_disp(cible, adresse, t))
            c, _ = KS.asm(corr, adresse)
            octets += bytes(c)
        return octets

    o_shani = assembler_shani(FNV_NOT, RVA["shani"])
    o_s02, _ = B4.assembler_bloc(KS, str(REPO / "tls13" / "notation" /
                               "tls13-02-sha256-comprimer.asm"), *lay.SLOTS_TLS13["h100002"])
    o_s15, _ = B4.assembler_bloc(KS, str(REPO / "tls13" / "notation" /
                               "tls13-15-aes128-cles-tour.asm"), *lay.SLOTS_TLS13["h100015"])
    o_s16, _ = B4.assembler_bloc(KS, str(REPO / "tls13" / "notation" /
                               "tls13-16-aes128-bloc.asm"), *lay.SLOTS_TLS13["h100016"])
    o_s17, _ = B4.assembler_bloc(KS, str(REPO / "tls13" / "notation" /
                               "tls13-17-ghash-multiplication.asm"), *lay.SLOTS_TLS13["h100017"])
    o_s18, _ = B4.assembler_bloc(KS, str(REPO / "tls13" / "notation" /
                               "tls13-18-gcm-sceller.asm"), *lay.SLOTS_TLS13["h100018"])
    # la table K[64] scellée (le fixture R_K lu du proxy.exe à 0x2f00)
    proxy = (REPO / "tls13" / "proxy.exe").read_bytes()
    # l'offset fichier du RVA 0x2f00 : les sections du proxy — le lecteur B4 :
    import struct
    pe_off = struct.unpack_from("<I", proxy, 0x3C)[0]
    nsec = struct.unpack_from("<H", proxy, pe_off + 6)[0]
    opt = struct.unpack_from("<H", proxy, pe_off + 20)[0]
    sec0 = pe_off + 24 + opt
    k_file = None
    for i in range(nsec):
        s = sec0 + 40 * i
        vaddr, vsize, raw, rawsize = struct.unpack_from("<IIII", proxy, s + 12)
        if vaddr <= 0x2F00 < vaddr + vsize:
            k_file = raw + (0x2F00 - vaddr)
            break
    assert k_file is not None, "la section de la table K introuvable"
    k_table = proxy[k_file:k_file + 256]

    rt = {nom: round_trip(o, rva) for nom, o, rva in [
        ("karatsuba", o_k, RVA["karatsuba"]),
        ("schoolbook", o_sb, RVA["schoolbook"]),
        ("sonde", o_sonde, RVA["sonde"]),
        ("v4i", o_v4i, RVA["v4i"]),
        ("shani", o_shani, RVA["shani"]),
        ("s02", o_s02, SC02), ("s15", o_s15, SC15), ("s16", o_s16, SC16),
        ("s17", o_s17, SC17), ("s18", o_s18, SC18)]}
    rt_code = {k: v for k, v in rt.items() if k != "shani"}
    assert all(rt_code.values()), f"round-trip divergent : {rt_code}"
    a("LE ROUND-TRIP 9/9 (keystone == capstone == keystone) ; le corridor SHA-NI "
      "RECONDUIT TEL QUEL de fnvan0zes (son round-trip vit à son atelier — "
      "l'encodage SHA canonique, les octets explicites keystone ne les porte pas)")

    # les marges : la convention du rig de labo (la mémoire du rig est à NOUS —
    # les scellés INTACTS sont les FICHIERS, garantis par le sceau-I 14/14) ; le
    # contrôle par code : AUCUN chevauchement entre NOS placements, et AUCUN
    # chevauchement avec les slots canoniques des scellés UTILISÉS dans la
    # session (02/15/16/17/18 — le juge et les baselines)
    placements = [(RVA["sonde"], len(o_sonde)), (RVA["karatsuba"], len(o_k)),
                  (RVA["schoolbook"], len(o_sb)), (RVA["v4i"], len(o_v4i)),
                  (RVA["shani"], len(o_shani)), (SC02, len(o_s02)),
                  (SC15, len(o_s15)), (SC16, len(o_s16)),
                  (SC17, len(o_s17)), (SC18, len(o_s18))]
    for i, (lo1, t1) in enumerate(placements):
        for lo2, t2 in placements[i+1:]:
            assert not (lo1 < lo2 + t2 and lo2 < lo1 + t1), \
                f"chevauchement {lo1:#x}/{lo2:#x} — la marge à revoir"
    a("LES MARGES SANS CHEVAUCHEMENT par code (les cinq pièces de corridor + "
      "les cinq scellés de la session, chacun à sa place — la convention du rig)")

    # ---- l'UNICORN : la parité, le mutant, le temps-constant ---------------
    res_u, emul = unicorne(o_k, o_sb, o_s17)
    a(f"LA DIFFÉRENTIELLE contre le scellé : karatsuba {res_u['diff']['karatsuba']['divergences']}/320 divergences · "
      f"schoolbook {res_u['diff']['schoolbook']['divergences']}/320")
    a(f"LES CAS PUNITIFS : {res_u['punition']}")
    a(f"LA COMMUTATIVITÉ 32/32 : {res_u['commut']}/32 · {res_u.get('commut_sb', 0)}/32 ; "
      f"X/Y INTACTS : {res_u['intact']}/32 · {res_u.get('intact_sb', 0)}/32")
    a(f"LE REPLI (r10=0 → le scellé) : {res_u['repli']}")
    a(f"LE MUTANT : {res_u['mutant']}")
    a(f"LES COMPTES Unicorn (enveloppe comprise) : karatsuba {res_u['comptes']['karatsuba']} · "
      f"schoolbook {res_u['comptes']['schoolbook']} instructions")

    res_t = trace_hash(emul, o_k)
    a(f"LE TEMPS-CONSTANT STRUCTUREL : traces {res_t['aleatoire']['empreintes']} empreinte(s)/60 "
      f"(aléatoire) · {res_t['structurée']['empreintes']} empreinte(s)/60 (structurée) ; "
      f"latence variable : {res_t['latence_variable'] or 'AUCUNE'}")

    # ---- le rig natif ------------------------------------------------------
    rig_c = generer_rig(o_k, o_sb, o_sonde, o_v4i, o_shani, o_s02, o_s15,
                        o_s16, o_s17, o_s18, k_table)
    (ICI / "native" / "ghash_rig.c").write_text(rig_c, encoding="utf-8")
    r = subprocess.run(["gcc", "-O1", "-no-pie", "-msha", "-mssse3", "-msse4.1",
                        "-mpclmul", "-o", str(ICI / "native" / "ghash_rig"),
                        str(ICI / "native" / "ghash_rig.c"),
                        str(ICI / "native" / "appeler_s18.S"), "-lcrypto"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[:3000]); return 2
    r = subprocess.run([str(ICI / "native" / "ghash_rig")], capture_output=True,
                       text=True, timeout=900)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr[:2000]); return 2
    mesures = {}
    parites = {}
    sonde = None
    for ligne in r.stdout.splitlines():
        if ligne.startswith("MESURE"):
            _, nom, med, iqr, par, par_iqr = ligne.split()
            mesures[nom] = {"mediane": int(med), "iqr": int(iqr),
                            "par": float(par), "par_iqr": float(par_iqr)}
        elif ligne.startswith("PARITE"):
            parites[ligne] = True
        elif ligne.startswith("SONDE"):
            sonde = ligne
    # la machine consignée (la convention x705m50vl)
    cpuinfo = pathlib.Path("/proc/cpuinfo").read_text()
    model = [l.split(":")[1].strip() for l in cpuinfo.splitlines()
             if l.startswith("model name")][0]
    mhz = [l.split(":")[1].strip() for l in cpuinfo.splitlines()
           if l.startswith("cpu MHz")][0]
    drapeaux = set()
    for ligne in cpuinfo.splitlines():
        if ligne.startswith(("flags", "Features")) and ":" in ligne:
            drapeaux |= set(ligne.split(":", 1)[1].split())
    drapeaux = sorted(drapeaux &
                      {"aes", "avx2", "constant_tsc", "rdtscp", "sse2",
                       "pclmulqdq", "sha_ni", "avx512f"})
    machine = {"machine": model, "mhz": mhz, "drapeaux": " ".join(drapeaux)}

    a(f"LE RIG NATIF (RDTSCP, cœur 1, n=20, médiane non arrondie + IQR, cycles bruts)")
    for nom, d in mesures.items():
        a(f"  {nom:24s} {d['mediane']:>8} c [IQR {d['iqr']:>4}] · {d['par']:.4f} c/unité")
    a(f"LA MACHINE : {machine['machine']} · {machine['mhz']} MHz · drapeaux {machine['drapeaux']}")
    a(f"LA SONDE DE SESSION : {sonde} — le verdict UNE fois, les couloirs ne sondent plus")

    garde2 = garde_sceau("APRÈS")

    # le registre
    registre = {
        "duree_s": round(time.monotonic() - t0, 1),
        "octets": {"karatsuba": len(o_k), "schoolbook": len(o_sb),
                   "sonde": len(o_sonde)},
        "rva": {**RVA},
        "round_trip": {k: bool(v) for k, v in rt.items()},
        "unicorn": res_u, "temps_constant": res_t,
        "mesures": mesures, "parites": list(parites.keys()),
        "machine": machine, "sonde": sonde,
        "sceau_avant": garde["ok"], "sceau_apres": garde2["ok"],
    }
    (ICI / "registres" / "ghash.json").write_text(
        json.dumps(registre, indent=2, ensure_ascii=False), encoding="utf-8")

    (ICI / "rapport-ghash.txt").write_text(
        "LE COULOIR GHASH EN PCLMULQDQ (0g3400vql, la vague 13)\n"
        "Le plan gelé sha256:caab6f481ab3799f… AVANT toute mesure.\n\n"
        + "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))
    return 0


if __name__ == "__main__":
    sys.exit(main())
