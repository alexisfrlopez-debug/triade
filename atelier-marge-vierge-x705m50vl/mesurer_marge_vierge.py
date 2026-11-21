#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesurer_marge_vierge.py — L'ATELIER x705m50vl (la vague 12) : LES DEUX
VARIANTES À LA MARGE VIERGE — le v5-entrelacé (k ∈ {4, 8} calendriers de clés
à adresses INDÉPENDANTES, les corps aesenc entrelacés) et L'AVX2 APRÈS
HISSAGE (le sondage cpuid UNE fois par session, le dispatch résolu au
chargement SOUS R10, le repli SSE2 jamais un chemin mort).

LE PLAN GELÉ sha256 c24a729de4305df6… (PLAN-X705M50VL.md, le commit 4f5d59f
PRÉCÈDE toute donnée) ; LA CIBLE PRÉ-ENREGISTRÉE FALSIFIABLE : ≤ 3 c/bloc
enveloppe comprise aux 64 et 256 blocs — si manquée, l'écart publié par
mesure (latence vs débit, port pressure — LA SONDE plancher-aesenc), jamais
un chiffre ajusté.

LA PARITÉ EXIGÉE : le calendrier des clés par LE SCELLÉ tls13-15 confronté au
juge python FIPS 197 §5.2 (aux HUIT clés du banc différentiel) ; le vecteur
FIPS 197 C.1 (le scellé, v4-inline, ent4, ent8) ; LA DIFFÉRENTIELLE 64/64 ET
256/256 OCTET POUR OCTET contre le scellé appelé par bloc (aux clés ÉGALES
des calendriers indépendants) ET LE VÉRITABLE MAPPAGE aux HUIT clés
DIFFÉRENTES (le bloc i au calendrier i mod k, le juge le scellé appelé à la
bonne clé par bloc) ; LES QUEUES exercées (N mod k — les replis de la
famille) ; LE REPLI FORCÉ du couloir hissé (r10 = 1 → SSE2, la batterie
559 entière) ; LA BORNE N ≤ 256 fail-closed (rax = -2, rien chiffré) ; le
round-trip 100 % aux six notations + la référence v4-inline + le couloir
AVX2 à dispatch (fnvan0zes, la cellule de non-régression).

LA BATTERIE 559 RE-ROULÉE sur le couloir AVX2 HISSÉ (la graine 20261120,
jamais re-tirée) : le chemin AVX2 réel au rig natif (r10 = 0, le CPU du bac
porte avx2) ET LE REPLI SSE2 (r10 = 1) — zéro divergence au juge trivial ;
le repli SOUS UNICORN (r10 = 1 — LA BORNE NOMMÉE : Unicorn ne porte ni AVX
ni SHA-NI, le chemin ymm jamais simulé).

LES MESURES : le compte d'instructions Unicorn aux 64 et 256 blocs
(l'enveloppe comprise — prologue/épilogue dans le compte) ; LE TEMPS RÉEL
RDTSCP au cœur 1 épinglé, n = 20 (≥ 20 exigé), la MÉDIANE NON ARRONDIE et
l'IQR publiés (les cycles bruts AUSSI — la recomposabilité, la leçon
6kbfrpn7k) ; les cellules existantes re-mesurées : v4-inline (la référence
AVANT 7,09/5,10 publiée), le couloir AVX2 à dispatch 5 846, le scellé
loupe-13 18 226 (la non-régression).

LE SCELLÉ INTACT : la garde du sceau-I 14/14 AVANT et APRÈS chaque partie ;
les QUATRE pièces sha256 (loupe.exe c1115105… · proxy.exe 446279f3… ·
selftest.exe 8038585b… · demo.exe df8f2e50…) aux ancres R7 ; la marge vierge
seule écrite ; la convention du rig 8z4hj76w4 (octets
position-indépendants).

Sorties : native/marge_rig.c · registres/marge-vierge.json ·
rapport-marge-vierge.txt."""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import random
import re
import subprocess
import sys
import time

import capstone  # noqa: E402
import keystone  # noqa: E402
import unicorn  # noqa: E402
from unicorn import x86_const  # noqa: E402

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-marge-vierge-x705m50vl"
sys.path.insert(0, str(REPO / "loupe"))
sys.path.insert(0, str(REPO / "m4"))
sys.path.insert(0, str(REPO / "tls13"))
BUILD = ICI / "native"
BUILD.mkdir(exist_ok=True)
REG = ICI / "registres"
REG.mkdir(exist_ok=True)

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

# ---- la marge du laboratoire (VIERGE, documentée) ---------------------------
# 0xC080  la copie du scellé tls13-15 (assemblé à son slot 0xDCC0)
# 0xC400  la copie du scellé tls13-16 (assemblé à son slot 0xDF00)
# 0xC800..0xCF00  les HUIT calendriers indépendants (176 o, espacés 0x100)
# 0xD100  le couloir AVX2 à dispatch par appel (fnvan0zes — non-régression)
# 0xD400  v4-inline (la référence AVANT, la porteuse de la vague 11)
# 0xD800  les HUIT calendriers du banc aux clés différentes (8 × 176 o)
# 0xE200  ent4 (v5-entrelacé k=4)   0xE600  loupe-13-avx2-hisse
# 0xE800  ent8 (v5-entrelacé k=8)   0xF000  le mutant (ent4, un octet)
# 0xF400  plancher-aesenc (la sonde de débit pur)
# 0xF800  le stub ret (la calibration de l'enveloppe msx64)
# 0x5740  le scellé loupe-13 à son slot (page 0x5000)
RVA = {"tls15": 0xC080, "tls16": 0xC400, "avx2": 0xD100, "v4i": 0xD400,
       "ent4": 0xE200, "hisse": 0xE600, "ent8": 0xE800, "mut": 0xF000,
       "plancher": 0xF400, "stub": 0xF800, "scelle13": 0x5740,
       "rk_meme": [0xC800 + 0x100 * i for i in range(8)],
       "rk_diff": 0xD800}

ARBRES_GARDE = ["m0", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8",
                "tls13", "loupe", "demo", "terrain", "v06"]

SCELLES_ANCRES = {
    "loupe/loupe.exe": "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1",
    "tls13/proxy.exe": "446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d",
    "m1/selftest.exe": "8038585b7af83c9fe5e6fdccd197e67888b9e5fb09d8d6c84cb998c684bff3c0",
    "demo/demo.exe": "df8f2e50949b14c072f139013a6166a041e573e49b6872d826958f522495e4af",
}


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


# ---- l'assemblage maison (le rig 8z4hj76w4, les étiquettes en PASSES) ------
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
    """le round-trip octet : keystone == capstone == keystone (le geste du
    rig d'instructions 8z4hj76w4)."""
    reins = b""
    for ins in CS.disasm(octets, rva):
        c, _ = KS.asm(f"{ins.mnemonic} {ins.op_str}", ins.address)
        reins += bytes(c)
    return reins == octets


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


FIPS_CLE = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
FIPS_CLAIR = bytes.fromhex("3243f6a8885a308d313198a2e0370734")
FIPS_CHIFFRE = bytes.fromhex("3925841d02dc09fbdc118597196a0b32")


# ---- la batterie 559 (la génération fnvan0zes, la graine 20261120) ----------
def generer_batterie():
    """LES 559 VECTEURS — la même série que fnvan0zes (la graine consignée,
    jamais re-tirée) : 16 queue-16 + 3 queue-fin · 4 chevauchants ·
    13 longueurs · 3 pages · 8 multi · 512 property-based."""
    rng = random.Random(20261120)
    vecteurs: list[tuple[str, bytes, bytes]] = []
    for p in range(16):
        f = bytearray(rng.randrange(256) for _ in range(4096))
        m = bytes(rng.randrange(256) for _ in range(16))
        pos = max(0, 4096 - 16 - (15 - p))
        f[pos:pos + 16] = m
        vecteurs.append(("queue-16", bytes(f), m))
    for lm in (1, 4, 16):
        f = bytearray(rng.randrange(256) for _ in range(1000))
        m = bytes(rng.randrange(256) for _ in range(lm))
        pos = 1000 - lm
        f[pos:pos + lm] = m
        vecteurs.append(("queue-fin", bytes(f), m))
    for periode in range(1, 5):
        f = bytearray(0x41 for _ in range(512))
        base = bytes(rng.randrange(256) for _ in range(periode))
        m = (base * (16 // periode + 1))[:16]
        pos = rng.randrange(64, 448)
        for i in range(16):
            f[pos + i] = m[i]
        vecteurs.append(("chevauchant-p%d" % periode, bytes(f), m))
    for lm in (1, 2, 3, 4, 15, 16, 17, 18, 19, 20, 31, 32, 33):
        f = bytearray(rng.randrange(256) for _ in range(2048))
        m = bytes(rng.randrange(256) for _ in range(lm))
        pos = rng.randrange(0, 2048 - lm)
        f[pos:pos + lm] = m
        vecteurs.append(("longueur-%d" % lm, bytes(f), m))
    for bord in ("a", "b", "c"):
        f = bytearray(rng.randrange(256) for _ in range(512))
        m = bytes(rng.randrange(256) for _ in range(8))
        pos = {"a": 505, "b": 513, "c": 508}[bord]
        f[pos:pos + 8] = m
        vecteurs.append(("page-" + bord, bytes(f), m))
    for nocc in range(1, 9):
        f = bytearray(rng.randrange(256) for _ in range(2048))
        m = bytes(rng.randrange(256) for _ in range(6))
        for p in sorted(rng.sample(range(0, 2048 - 6), nocc)):
            f[p:p + 6] = m
        vecteurs.append(("multi-%d" % nocc, bytes(f), m))
    for k in range(512):
        n = rng.choice([17, 63, 100, 256, 1000, 4096])
        lm = rng.choice([1, 2, 3, 5, 8, 16, 17, 24, 32])
        f = bytearray(rng.randrange(256) for _ in range(n))
        m = bytes(rng.randrange(256) for _ in range(lm))
        if rng.random() < 0.7 and n > lm:
            p = rng.randrange(0, n - lm + 1)
            f[p:p + lm] = m
        vecteurs.append(("pbt-%d" % k, bytes(f), m))
    return vecteurs


# ---- la garde du sceau (14/14 + les quatre pièces aux ancres R7) ------------
def garde_sceau(quand: str) -> dict:
    sceau = charger_module("sceau_I_x705", REPO / "v06" / "sceau_I.py")
    sceau.garde(ARBRES_GARDE)            # lève EchecSceauI — fail-closed
    empreintes = {}
    for rel, ancre in SCELLES_ANCRES.items():
        calculee = hashlib.sha256((REPO / rel).read_bytes()).hexdigest()
        if calculee != ancre:
            raise RuntimeError(f"le scellé {rel} a divergé de son ancre")
        empreintes[rel] = calculee[:16] + "…"
    print(f"[sceau] {quand} : la garde 14/14 VERTE ; les QUATRE pièces aux "
          f"ancres R7 INTACTES (loupe.exe c1115105… · proxy.exe 446279f3… · "
          f"selftest.exe 8038585b… · demo.exe df8f2e50…)")
    return empreintes


class Compteur:
    """le compteur d'instructions du rig 8z4hj76w4 (UC_HOOK_CODE)."""

    def __init__(self, uc):
        self.n = 0
        uc.hook_add(unicorn.UC_HOOK_CODE, self._hook)

    def _hook(self, uc, adresse, taille, donnees):
        self.n += 1


# ---- LA PARTIE UNICORN : la batterie 559 sur le couloir hissé (repli SSE2) --
def batterie_unicorn(o_hisse: bytes) -> dict:
    HE = charger_module("h_ed_x705", REPO / "loupe" / "harnais_edition.py")
    os_v = HE.OSEdition()
    emul = HE.EmulationEdition(
        os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
        (REPO / "m1" / "selftest.exe").read_bytes(),
        (REPO / "demo" / "demo.exe").read_bytes())
    emul.uc.mem_map(0x500000, 0x21000)      # les tampons de la batterie
    # le couloir posé À SON ADRESSE D'ASSEMBLAGE 0xE600 (la marge .data du
    # harnais — l'appel ABSOLU au memcmp scellé 0x1180 interdit le déplacement
    # des octets ; la zone 0xE000-0x20000 est déjà mappée par le harnais)
    emul.uc.mem_write(0xE600, o_hisse)
    emul.uc.ctl_remove_cache(0xE000, 0xF000)
    vecteurs = generer_batterie()
    divergences = []
    for i, (classe, f, m) in enumerate(vecteurs):
        attendu = -5 if len(m) > 32 else f.find(m)
        addr = 0x510000 - 512 if classe.startswith("page-") else 0x500400
        emul.uc.mem_write(addr, f)
        emul.uc.mem_write(0x510800, m)
        with contextlib.redirect_stdout(io.StringIO()):
            r = emul.appeler(0xE600, {"rcx": addr, "rdx": len(f),
                                      "r8": 0x510800, "r9": len(m),
                                      "r10": 1},        # LE REPLI FORCÉ
                             pile_args=[0])
        if "crash" in r and r["crash"]:
            divergences.append((i, classe, "crash:" + r["crash"], attendu))
            continue
        if (r["rax"] & (2**64 - 1)) != (attendu & (2**64 - 1)):
            divergences.append((i, classe, r["rax"], attendu))
    return {"batterie": len(vecteurs), "divergences": divergences,
            "vecteurs": len(vecteurs)}


# ---- LA PARTIE UNICORN : le compte d'instructions (l'enveloppe comprise) ----
def compter_instructions(o_ent4, o_ent8, o_v4i, rk_fois8: list[bytes]) -> dict:
    """le compte d'instructions par appel — l'ENVELOPPE comprise (du premier
    octet du prologue au ret, la convention du plan)."""
    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    uc.mem_map(0x600000, 0x10000)           # le code du banc
    uc.mem_map(0x7F000000, 0x10000)         # la pile
    RET = 0x600100
    uc.mem_write(0x602000, o_ent4)
    uc.mem_write(0x604000, o_ent8)
    uc.mem_write(0x606000, o_v4i)
    # les données : les HUIT calendriers indépendants + les tableaux + IN/OUT
    for i, rk in enumerate(rk_fois8):
        uc.mem_write(0x608000 + 0x100 * i, rk)
    ptr4 = b"".join((0x608000 + 0x100 * i).to_bytes(8, "little")
                    for i in range(4))
    ptr8 = b"".join((0x608000 + 0x100 * i).to_bytes(8, "little")
                    for i in range(8))
    uc.mem_write(0x609000, ptr4)
    uc.mem_write(0x609040, ptr8)
    n_max = 256
    donnees = bytes((i * 31 + 7) & 0xFF for i in range(n_max * 16))
    uc.mem_write(0x60A000, donnees)
    uc.mem_write(0x60B000, b"\x00" * (n_max * 16))
    compteur = Compteur(uc)

    def un_appel(entree: int, rcx: int, rdx: int, r8: int, r9: int) -> int:
        compteur.n = 0
        uc.reg_write(x86_const.UC_X86_REG_RCX, rcx)
        uc.reg_write(x86_const.UC_X86_REG_RDX, rdx)
        uc.reg_write(x86_const.UC_X86_REG_R8, r8)
        uc.reg_write(x86_const.UC_X86_REG_R9, r9)
        uc.reg_write(x86_const.UC_X86_REG_RAX, 0)
        uc.reg_write(x86_const.UC_X86_REG_RSP, 0x7F001000)
        uc.mem_write(0x7F001000, RET.to_bytes(8, "little"))
        uc.emu_start(entree, RET, count=50_000_000)
        return compteur.n

    resultats = {}
    for nom, entree, est_ent in [("ent4", 0x602000, True),
                                 ("ent8", 0x604000, True),
                                 ("v4i", 0x606000, False)]:
        for nb in (64, 256):
            rcx = (0x609000 if nom == "ent4" else
                   0x609040 if nom == "ent8" else 0x608000)
            n = un_appel(entree, rcx, 0x60A000, 0x60B000, nb)
            resultats[f"{nom}@{nb}"] = {"instructions": n,
                                        "par_bloc": round(n / nb, 3)}
            print(f"[unicorn] {nom}@{nb} : {n} instructions "
                  f"({n / nb:.2f}/bloc, l'enveloppe comprise)")
    return resultats


# ---- LA PARTIE NATIVE : le rig C généré --------------------------------------
RIG_C = r"""/* marge_rig.c — LE RIG NATIF (x705m50vl) — généré par mesurer_marge_vierge.py
(jamais écrit à la main : les octets des notations EMBARQUÉS des fichiers, les
scellés assemblés par le lecteur canonique B4). */
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <sys/mman.h>
%%TABLES%%
/* les calendriers du banc : le FIPS + les HUIT clés différentes (le juge
python FIPS 197 §5.2 les a dérivées AVANT le rig — le C les confronte au
scellé tls13-15 un à un) */
static const unsigned char RK_FIPS[] = {
%%RK_FIPS%%};
static const unsigned char CLES8[][16] = {
%%CLES8%%};
static const unsigned char RK8[][176] = {
%%RK8%%};
static const unsigned char FIPS_CLE[] = {
%%FIPS_CLE%%};
static const unsigned char FIPS_CLAIR[] = {
%%FIPS_CLAIR%%};
static const unsigned char FIPS_CHIFFRE[] = {
%%FIPS_CHIFFRE%%};
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
/* l'appelant AU VERDICT HISSÉ : r10 = le verdict de session (0 → AVX2,
   ≠ 0 → le repli SSE2) — le sondage cpuid VIT À L'APPELANT, UNE FOIS PAR
   SESSION (la condition nommée de fnvan0zes, la note TENUE) */
static long appeler_r10(unsigned long fn, unsigned long rcx_v,
                        unsigned long rdx_v, unsigned long r8_v,
                        unsigned long r9_v, unsigned long pile_v,
                        unsigned long r10_v) {
    long ret;
    __asm__ volatile(
        "subq $0x30, %%rsp\n\t"
        "movq %7, 0x20(%%rsp)\n\t"
        "movq %2, %%rcx\n\t"
        "movq %3, %%rdx\n\t"
        "movq %4, %%r8\n\t"
        "movq %5, %%r9\n\t"
        "movq %6, %%r10\n\t"
        "callq *%1\n\t"
        "movq %%rax, %0\n\t"
        "addq $0x30, %%rsp\n\t"
        : "=r"(ret)
        : "r"(fn), "r"(rcx_v), "r"(rdx_v), "r"(r8_v), "r"(r9_v),
          "r"(r10_v), "r"(pile_v)
        : "rax", "rbx", "rcx", "rdx", "r8", "r9", "r10", "r11", "cc", "memory");
    return ret;
}
static inline unsigned long long rdtscp32(void) {
    unsigned aux, lo, hi;
    __asm__ volatile("rdtscp" : "=a"(lo), "=d"(hi), "=c"(aux) :: "memory");
    return ((unsigned long long)hi << 32) | lo;
}
/* la série (le rig 8z4hj76w4 : la graine 20261120 reproduite par xorshift) */
static uint64_t xs = 20261120ULL;
static unsigned char rnd(void) {
    xs ^= xs << 13; xs ^= xs >> 7; xs ^= xs << 17;
    return (unsigned char)(xs >> 32);
}
static int egal(const unsigned char *a, const unsigned char *b, long n) {
    return memcmp(a, b, (size_t)n) == 0;
}
/* le juge : le scellé tls13-16 APPELÉ PAR BLOC depuis le C (les adresses
   indépendantes par bloc, la référence de la différentielle) */
static void scelle_par_bloc(unsigned long rk, const unsigned char *in,
                            unsigned char *out, long n) {
    for (long b = 0; b < n; ++b)
        appeler_msx64(0xC400, rk, (unsigned long)(in + b*16),
                      (unsigned long)(out + b*16), 0, 0);
}
/* les tableaux de pointeurs (les calendriers aux adresses indépendantes) */
static const unsigned long PTR4[]  = {0xC800UL, 0xC900UL, 0xCA00UL, 0xCB00UL};
static const unsigned long PTR8[]  = {0xC800UL, 0xC900UL, 0xCA00UL, 0xCB00UL,
                                      0xCC00UL, 0xCD00UL, 0xCE00UL, 0xCF00UL};
static const unsigned long PTR4D[] = {0xD800UL, 0xD8B0UL, 0xD960UL, 0xDA10UL};
static const unsigned long PTR8D[] = {0xD800UL, 0xD8B0UL, 0xD960UL, 0xDA10UL,
                                      0xDAC0UL, 0xDB70UL, 0xDC20UL, 0xDCD0UL};
#include "vecteurs.h"
int main(void) {
    cpu_set_t m; CPU_ZERO(&m); CPU_SET(1, &m);
    if (sched_setaffinity(0, sizeof(m), &m) != 0) perror("affinité");
    pose_page(0xC000, 0x4000);
    pose_page(0x5000, 0x2000);
    pose_trampoline();
    memcpy((void*)0xC080, tls15, sizeof(tls15));
    memcpy((void*)0xC400, tls16, sizeof(tls16));
    memcpy((void*)0xD100, avx2, sizeof(avx2));
    memcpy((void*)0xD400, v4i, sizeof(v4i));
    memcpy((void*)0xE200, ent4, sizeof(ent4));
    memcpy((void*)0xE600, hisse, sizeof(hisse));
    memcpy((void*)0xE800, ent8, sizeof(ent8));
    memcpy((void*)0xF000, mut, sizeof(mut));
    memcpy((void*)0xF400, plancher, sizeof(plancher));
    memcpy((void*)0x5740, sc13, sizeof(sc13));
    for (int i = 0; i < 8; ++i) {
        memcpy((void*)(0xC800UL + 0x100UL*i), RK_FIPS, 176);
        memcpy((void*)(0xD800UL + 176UL*i), RK8[i], 176);
    }
    *(unsigned char *)0xF800 = 0xC3;
    __builtin___clear_cache((char*)0x1000, (char*)0x10000);
    __builtin___clear_cache((char*)0x5000, (char*)0x7000);

    /* (0) LE CALENDRIER : le scellé tls13-15 au juge python FIPS 197 §5.2 */
    unsigned char *RK = malloc(176);
    appeler_msx64(0xC080, (unsigned long)FIPS_CLE, (unsigned long)RK, 0, 0, 0);
    printf("CALENDRIER %d\n", egal(RK, RK_FIPS, 176));
    /* les HUIT clés différentes : chaque calendrier par le scellé au juge */
    int cal8 = 0;
    for (int i = 0; i < 8; ++i) {
        unsigned char *rk = malloc(176);
        appeler_msx64(0xC080, (unsigned long)CLES8[i], (unsigned long)rk, 0, 0, 0);
        cal8 += egal(rk, RK8[i], 176);
        free(rk);
    }
    printf("CALENDRIER8 %d/8\n", cal8);

    /* (1) LE VECTEUR FIPS 197 C.1 : le scellé, v4-inline, ent4, ent8 */
    unsigned char *CT = malloc(16), *OUT = malloc(16);
    appeler_msx64(0xC400, (unsigned long)RK, (unsigned long)FIPS_CLAIR,
                  (unsigned long)CT, 0, 0);
    printf("FIPS scelle %d\n", egal(CT, FIPS_CHIFFRE, 16));
    appeler_msx64(0xD400, (unsigned long)RK, (unsigned long)FIPS_CLAIR,
                  (unsigned long)OUT, 1, 0);
    printf("FIPS v4i %d\n", egal(OUT, FIPS_CHIFFRE, 16));
    appeler_msx64(0xE200, (unsigned long)PTR4, (unsigned long)FIPS_CLAIR,
                  (unsigned long)OUT, 1, 0);
    printf("FIPS ent4 %d\n", egal(OUT, FIPS_CHIFFRE, 16));
    appeler_msx64(0xE800, (unsigned long)PTR8, (unsigned long)FIPS_CLAIR,
                  (unsigned long)OUT, 1, 0);
    printf("FIPS ent8 %d\n", egal(OUT, FIPS_CHIFFRE, 16));
    /* LE CONTRÔLE NÉGATIF : l'octet du corps entrelacé muté — ATTRAPÉ au
       premier vecteur (le FIPS : le bloc 0 = le flot 0 = la base mutée) */
    appeler_msx64(0xF000, (unsigned long)PTR4, (unsigned long)FIPS_CLAIR,
                  (unsigned long)OUT, 1, 0);
    printf("NEGATIF %s\n", egal(OUT, FIPS_CHIFFRE, 16) ? "NON-ATTRAPE" : "ATTRAPE");

    /* (2) LA DIFFÉRENTIELLE 64/64 puis 256/256 : chaque variante contre le
       scellé appelé par bloc, octet pour octet — PUIS LES QUEUES (N mod k)
       ET LE VÉRITABLE MAPPAGE aux HUIT clés différentes */
    long tailles[] = {64, 256, 1, 2, 3, 5, 7, 63, 65, 255};
    for (unsigned t = 0; t < sizeof(tailles)/sizeof(tailles[0]); ++t) {
        long nb = tailles[t];
        unsigned char *IN = malloc(nb*16);
        unsigned char *SC = malloc(nb*16);
        unsigned char *OU = malloc(nb*16);
        for (long i = 0; i < nb*16; ++i) IN[i] = rnd();
        scelle_par_bloc((unsigned long)RK, IN, SC, nb);
        const char *etiquette = (nb == 64 || nb == 256) ? "DIFF" : "QUEUE";
        memset(OU, 0, nb*16);
        appeler_msx64(0xD400, (unsigned long)RK, (unsigned long)IN,
                      (unsigned long)OU, nb, 0);
        long k = 0;
        for (long b = 0; b < nb; ++b) k += egal(OU + b*16, SC + b*16, 16);
        printf("%s v4i %ld/%ld\n", etiquette, k, nb);
        memset(OU, 0, nb*16);
        appeler_msx64(0xE200, (unsigned long)PTR4, (unsigned long)IN,
                      (unsigned long)OU, nb, 0);
        k = 0;
        for (long b = 0; b < nb; ++b) k += egal(OU + b*16, SC + b*16, 16);
        printf("%s ent4 %ld/%ld\n", etiquette, k, nb);
        memset(OU, 0, nb*16);
        appeler_msx64(0xE800, (unsigned long)PTR8, (unsigned long)IN,
                      (unsigned long)OU, nb, 0);
        k = 0;
        for (long b = 0; b < nb; ++b) k += egal(OU + b*16, SC + b*16, 16);
        printf("%s ent8 %ld/%ld\n", etiquette, k, nb);
        if (nb == 64 || nb == 256) {
            /* LE MAPPAGE aux clés différentes : le bloc i au calendrier
               i mod k — le juge le scellé appelé À LA BONNE clé par bloc */
            unsigned char *SCD = malloc(nb*16);
            for (int kk = 0; kk < 2; ++kk) {
                for (long b = 0; b < nb; ++b)
                    appeler_msx64(0xC400, 0xD800UL + 176UL*(b % (kk ? 8 : 4)),
                                  (unsigned long)(IN + b*16),
                                  (unsigned long)(SCD + b*16), 0, 0);
                memset(OU, 0, nb*16);
                appeler_msx64(kk ? 0xE800UL : 0xE200UL,
                              (unsigned long)(kk ? PTR8D : PTR4D),
                              (unsigned long)IN, (unsigned long)OU, nb, 0);
                long kd = 0;
                for (long b = 0; b < nb; ++b)
                    kd += egal(OU + b*16, SCD + b*16, 16);
                printf("DIFFCLES%d %s %ld/%ld\n", (int)nb,
                       kk ? "ent8" : "ent4", kd, nb);
            }
            free(SCD);
        }
        free(IN); free(SC); free(OU);
    }

    /* (3) LA BORNE : N = 257 → rax = -2, RIEN chiffré (fail-closed) */
    for (int v = 0; v < 2; ++v) {
        unsigned char *IN = malloc(257*16);
        unsigned char *OU = malloc(257*16);
        for (int i = 0; i < 257*16; ++i) IN[i] = rnd();
        memset(OU, 0xAA, 257*16);
        long r = appeler_msx64(v ? 0xE800UL : 0xE200UL,
                               (unsigned long)(v ? PTR8 : PTR4),
                               (unsigned long)IN, (unsigned long)OU, 257, 0);
        int intact = 1;
        for (int i = 0; i < 257*16; ++i) if (OU[i] != 0xAA) intact = 0;
        printf("BORNE %s %d %d\n", v ? "ent8" : "ent4", r == -2, intact);
        free(IN); free(OU);
    }

    /* (4) LA BATTERIE 559 sur le couloir HISSÉ : le chemin AVX2 réel
       (r10 = 0) ET LE REPLI FORCÉ (r10 = 1) — le juge séquentiel */
    long div_avx = 0, div_repli = 0;
    for (int i = 0; i < NB_VECS; i++) {
        const unsigned char *f = TAMPONS + vec_decal[i];
        const unsigned char *m = MOTIFS + m_decal[i];
        long juge = -5;
        if (vec_lm[i] <= 32) {
            juge = -1;
            for (long p = 0; p + vec_lm[i] <= vec_n[i]; p++) {
                if (memcmp(f + p, m, vec_lm[i]) == 0) { juge = p; break; }
            }
        }
        long r_a = appeler_r10(0xE600, (unsigned long)f, vec_n[i],
                               (unsigned long)m, vec_lm[i], 0, 0);
        long r_r = appeler_r10(0xE600, (unsigned long)f, vec_n[i],
                               (unsigned long)m, vec_lm[i], 0, 1);
        if (r_a != juge) div_avx++;
        if (r_r != juge) div_repli++;
    }
    printf("BATTERIE avx2 %ld repli %ld (sur %d)\n", div_avx, div_repli, NB_VECS);

    /* (5) LES MESURES : RDTSCP, n = 20, la médiane NON ARRONDIE et l'IQR —
       les cycles BRUTS publiés (la recomposabilité) */
    unsigned char tamp[4096], motif[32];
    for (int i = 0; i < 4096; i++) tamp[i] = (unsigned char)(i * 31 + 7);
    for (int i = 0; i < 16; i++) motif[i] = 0xEE;   /* absent — la convention */
    unsigned long long cyc[24];
    int n = 20;
    #define MESURE(nom, div, expr) do { \
        for (int w = 0; w < 3; ++w) { (void)(expr); } \
        for (int r = 0; r < n; r++) { \
            unsigned long long t0 = rdtscp32(); \
            (void)(expr); \
            cyc[r] = rdtscp32() - t0; \
        } \
        for (int i2 = 1; i2 < n; i2++) { unsigned long long k2 = cyc[i2]; int j2 = i2-1; \
            while (j2 >= 0 && cyc[j2] > k2) { cyc[j2+1] = cyc[j2]; j2--; } cyc[j2+1] = k2; } \
        unsigned long long med = (cyc[n/2-1]+cyc[n/2])/2; \
        unsigned long long iqr = cyc[n*3/4]-cyc[n/4]; \
        printf("MESURE %-16s %llu %llu %.6f %.6f\n", nom, med, iqr, \
               (double)med/(double)(div), (double)iqr/(double)(div)); \
    } while (0)
    unsigned char *IN = malloc(256*16);
    unsigned char *OU = malloc(256*16);
    for (int i = 0; i < 256*16; ++i) IN[i] = rnd();
    MESURE("stub", 1, appeler_msx64(0xF800, 0, 0, 0, 0, 0));
    MESURE("plancher", 512*8, appeler_msx64(0xF400, 512, 0, 0, 0, 0));
    MESURE("v4i@64", 64, appeler_msx64(0xD400, (unsigned long)RK, (unsigned long)IN, (unsigned long)OU, 64, 0));
    MESURE("v4i@256", 256, appeler_msx64(0xD400, (unsigned long)RK, (unsigned long)IN, (unsigned long)OU, 256, 0));
    MESURE("ent4@64", 64, appeler_msx64(0xE200, (unsigned long)PTR4, (unsigned long)IN, (unsigned long)OU, 64, 0));
    MESURE("ent4@256", 256, appeler_msx64(0xE200, (unsigned long)PTR4, (unsigned long)IN, (unsigned long)OU, 256, 0));
    MESURE("ent8@64", 64, appeler_msx64(0xE800, (unsigned long)PTR8, (unsigned long)IN, (unsigned long)OU, 64, 0));
    MESURE("ent8@256", 256, appeler_msx64(0xE800, (unsigned long)PTR8, (unsigned long)IN, (unsigned long)OU, 256, 0));
    MESURE("hisse-avx2@4096", 1, appeler_r10(0xE600, (unsigned long)tamp, 4096, (unsigned long)motif, 16, 0, 0));
    MESURE("hisse-repli@4096", 1, appeler_r10(0xE600, (unsigned long)tamp, 4096, (unsigned long)motif, 16, 0, 1));
    MESURE("avx2@4096", 1, appeler_msx64(0xD100, (unsigned long)tamp, 4096, (unsigned long)motif, 16, 0));
    MESURE("scelle13@4096", 1, appeler_msx64(0x5740, (unsigned long)tamp, 4096, (unsigned long)motif, 16, 0));
    return 0;
}
"""


def main() -> int:
    rapport: list[str] = []
    a = rapport.append
    t0 = time.monotonic()

    # ---- (0) LA GARDE DU SCEAU AVANT ----------------------------------------
    empreintes = garde_sceau("AVANT")

    # ---- (1) les octets : les notations + les scellés ------------------------
    NOT = ICI / "notation"
    o_ent4 = assembler(NOT / "tls13-16-ni-v5-ent4.asm", RVA["ent4"])
    o_ent8 = assembler(NOT / "tls13-16-ni-v5-ent8.asm", RVA["ent8"])
    o_hisse = assembler(NOT / "loupe-13-avx2-hisse.asm", RVA["hisse"])
    o_plancher = assembler(NOT / "plancher-aesenc.asm", RVA["plancher"])
    o_v4i = assembler(REPO / "atelier-porteuse-ahult8jgd" / "notation" /
                      "tls13-16-ni-v4-inline.asm", RVA["v4i"])
    o_avx2 = assembler(REPO / "atelier-corridors-fnvan0zes" / "notation" /
                       "loupe-13-avx2.asm", RVA["avx2"])
    B4 = charger_module("b4_x705", REPO / "m4" / "build_m4.py")
    lay = charger_module("lay_x705", REPO / "tls13" / "layout.py")
    not15 = REPO / "tls13" / "notation" / "tls13-15-aes128-cles-tour.asm"
    not16 = REPO / "tls13" / "notation" / "tls13-16-aes128-bloc.asm"
    o_tls15, _ = B4.assembler_bloc(KS, str(not15), *lay.SLOTS_TLS13["h100015"])
    o_tls16, _ = B4.assembler_bloc(KS, str(not16), *lay.SLOTS_TLS13["h100016"])
    HN = charger_module("hn_x705", REPO / "loupe" / "harnais_noyau.py")
    not13 = REPO / "loupe" / "notation" / "loupe-13-recherche.asm"
    rva13, slot13 = HN.L.SLOTS_LOUPE["i110013"]
    o_sc13, _ = B4.assembler_bloc(KS, str(not13), rva13, slot13)

    # le round-trip (les SIX notations de la marge + les deux références)
    rt = {}
    for nom, octets, rva in [("ent4", o_ent4, RVA["ent4"]),
                             ("ent8", o_ent8, RVA["ent8"]),
                             ("hisse", o_hisse, RVA["hisse"]),
                             ("plancher", o_plancher, RVA["plancher"]),
                             ("v4i", o_v4i, RVA["v4i"]),
                             ("avx2", o_avx2, RVA["avx2"]),
                             ("tls15", o_tls15, lay.SLOTS_TLS13["h100015"][0]),
                             ("tls16", o_tls16, lay.SLOTS_TLS13["h100016"][0]),
                             ("scelle13", o_sc13, rva13)]:
        rt[nom] = round_trip(octets, rva)
    assert all(rt.values()), f"round-trip divergent : {rt}"

    # le mutant : UN octet du corps entrelacé — la lecture [rbx + 0x90] du
    # flot 0 (la neuvième clé de tour), le déplacement disp32 0x90 → 0x91 (le
    # geste exact du mutant de la porteuse — l'octet BAS du disp32)
    mut = bytearray(o_ent4)
    cible = None
    for ins in CS.disasm(bytes(mut), RVA["ent4"]):
        if (ins.mnemonic == "movdqu"
                and ins.op_str == "xmm4, xmmword ptr [rbx + 0x90]"):
            cible = ins.address - RVA["ent4"] + ins.size - 4
    assert cible is not None, "la lecture [rbx + 0x90] du flot 0 introuvable"
    assert bytes(mut[cible:cible + 4]) == bytes.fromhex("90000000")
    mut[cible] = 0x91
    o_mut = bytes(mut)

    # les marges : aucun chevauchement (vérifié)
    posees = [("tls15", 0xC080, 0xC080 + len(o_tls15)),
              ("tls16", 0xC400, 0xC400 + len(o_tls16)),
              ("rk0..rk7", 0xC800, 0xCF00 + 176),
              ("avx2", RVA["avx2"], RVA["avx2"] + len(o_avx2)),
              ("v4i", RVA["v4i"], RVA["v4i"] + len(o_v4i)),
              ("rk_diff", 0xD800, 0xD800 + 8 * 176),
              ("ent4", RVA["ent4"], RVA["ent4"] + len(o_ent4)),
              ("hisse", RVA["hisse"], RVA["hisse"] + len(o_hisse)),
              ("ent8", RVA["ent8"], RVA["ent8"] + len(o_ent8)),
              ("mut", RVA["mut"], RVA["mut"] + len(o_mut)),
              ("plancher", RVA["plancher"], RVA["plancher"] + len(o_plancher)),
              ("stub", 0xF800, 0xF801)]
    for i, (n1, a1, b1) in enumerate(posees):
        for j, (n2, a2, b2) in enumerate(posees):
            if i != j and a1 < b2 and a2 < b1:
                raise RuntimeError(
                    f"marges chevauchées {n1} {a1:#x}-{b1:#x} / "
                    f"{n2} {a2:#x}-{b2:#x}")
    a("LES OCTETS À LA MARGE VIERGE : ent4 {} o au RVA {:#x} · hisse {} o à "
      "{:#x} · ent8 {} o à {:#x} (L'ÉCART AU PLAN NOMMÉ : le plan gelé "
      "posait ent8 à 0xE400 — le corps k=8 ({}) NE TIENT PAS dans la fenêtre "
      "0x200, ET ent4 lui-même ({}) déborde 0xE400 — posé à 0xE800, la cause "
      "mesurée, le plan demeuré gelé) ; le mutant {} o à {:#x} (l'octet "
      "{:#x} : 0x90 → 0x91, la lecture [rbx+0x90] du flot 0) ; le plancher "
      "{} o à {:#x} ; v4-inline la référence à 0xD400 ; le couloir AVX2 à "
      "dispatch (fnvan0zes) la cellule de non-régression à 0xD100 — le "
      "round-trip 100 % aux NEUF corps, les marges sans chevauchement, les "
      "SCELLÉS assemblés à leurs slots par le lecteur canonique B4 "
      "(tls13-15 à 0xDCC0, tls13-16 à 0xDF00, loupe-13 à 0x5740)".format(
          len(o_ent4), RVA["ent4"], len(o_hisse), RVA["hisse"], len(o_ent8),
          RVA["ent8"], len(o_ent8), len(o_ent4), len(o_mut), RVA["mut"],
          cible, len(o_plancher), RVA["plancher"]))

    # ---- (2) les calendriers du banc (le juge python FIPS 197 §5.2) ---------
    rk_fips = expansion_aes128(FIPS_CLE)
    assert rk_fips[16:20] == bytes.fromhex("a0fafe17")   # C.1 : w4
    s = 20261120

    def nxt64():
        nonlocal s
        s = s * 6364136223846793005 + 1442695040888963407
        return (s >> 32) & 0xFFFFFFFF
    cles8 = [bytes(nxt64() & 0xFF for _ in range(16)) for _ in range(8)]
    rk8 = [expansion_aes128(cle) for cle in cles8]

    # ---- (3) LA BATTERIE 559 SOUS UNICORN (le repli forcé r10 = 1) ----------
    bat_unicorn = batterie_unicorn(o_hisse)
    assert not bat_unicorn["divergences"], \
        f"la batterie Unicorn diverge : {bat_unicorn['divergences'][:5]}"
    a(f"LA BATTERIE 559 SOUS UNICORN (le couloir hissé au REPLI FORCÉ "
      f"r10 = 1 — LA BORNE NOMMÉE : Unicorn ne porte ni AVX ni SHA-NI, le "
      f"chemin ymm JAMAIS simulé) : {bat_unicorn['batterie']} vecteurs — "
      f"ZÉRO DIVERGENCE (les lm > 32 au REFUS DE CONTRAT -5 attendu)")
    garde_sceau("APRÈS UNICORN-BATTERIE")

    # ---- (4) LE COMPTE D'INSTRUCTIONS UNICORN (l'enveloppe comprise) --------
    rk_fois8 = [rk_fips] * 8
    comptes = compter_instructions(o_ent4, o_ent8, o_v4i, rk_fois8)
    garde_sceau("APRÈS UNICORN-COMPTES")

    # ---- (5) LE RIG NATIF ----------------------------------------------------
    tables = (ctable("tls15", o_tls15) + ctable("tls16", o_tls16)
              + ctable("avx2", o_avx2) + ctable("v4i", o_v4i)
              + ctable("ent4", o_ent4) + ctable("hisse", o_hisse)
              + ctable("ent8", o_ent8) + ctable("mut", o_mut)
              + ctable("plancher", o_plancher) + ctable("sc13", o_sc13))

    def ctab_lignes(nom, donnees, largeur, fmt):
        lignes = []
        for i in range(0, len(donnees), largeur):
            chunk = donnees[i:i + largeur]
            lignes.append("  {" + ",".join(fmt % b for b in chunk) + "},")
        return "static const unsigned char {}[][{}] = {{\n{}\n}};\n".format(
            nom, largeur, "\n".join(lignes))

    rig = RIG_C
    rig = rig.replace("%%TABLES%%", tables)
    rig = rig.replace("%%RK_FIPS%%",
                      ",".join(f"0x{b:02x}" for b in rk_fips))
    rig = rig.replace("%%CLES8%%", "\n".join(
        "  {" + ",".join(f"0x{b:02x}" for b in cle) + "}," for cle in cles8))
    rig = rig.replace("%%RK8%%", "\n".join(
        "  {" + ",".join(f"0x{b:02x}" for b in rk) + "}," for rk in rk8))
    rig = rig.replace("%%FIPS_CLE%%", ",".join(f"0x{b:02x}" for b in FIPS_CLE))
    rig = rig.replace("%%FIPS_CLAIR%%",
                      ",".join(f"0x{b:02x}" for b in FIPS_CLAIR))
    rig = rig.replace("%%FIPS_CHIFFRE%%",
                      ",".join(f"0x{b:02x}" for b in FIPS_CHIFFRE))
    (BUILD / "marge_rig.c").write_text(rig, encoding="utf-8")

    # les vecteurs de la batterie (le fichier de données)
    vecteurs = generer_batterie()
    with open(BUILD / "vecteurs.h", "w") as f:
        f.write(f"#define NB_VECS {len(vecteurs)}\n")
        f.write("static const unsigned char TAMPONS[] = {\n")
        idx, cur = [], 0
        for _, f_, m_ in vecteurs:
            idx.append(cur)
            cur += len(f_)
            f.write("  " + ", ".join(str(b) for b in f_) + ",\n")
        f.write("};\n")
        f.write("static const unsigned long vec_decal[] = {" +
                ",".join(str(i) for i in idx) + "};\n")
        f.write("static const long vec_n[] = {" +
                ",".join(str(len(f_)) for _, f_, _ in vecteurs) + "};\n")
        f.write("static const unsigned char MOTIFS[] = {\n")
        midx, mcur = [], 0
        for _, f_, m_ in vecteurs:
            midx.append(mcur)
            mcur += len(m_)
            f.write("  " + ", ".join(str(b) for b in m_) + ",\n")
        f.write("};\n")
        f.write("static const unsigned long m_decal[] = {" +
                ",".join(str(i) for i in midx) + "};\n")
        f.write("static const long vec_lm[] = {" +
                ",".join(str(len(m_)) for _, _, m_ in vecteurs) + "};\n")

    r = subprocess.run(["gcc", "-O1", "-no-pie", "-o",
                        str(BUILD / "marge_rig"),
                        str(BUILD / "marge_rig.c")],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"compilation : {r.stderr[:2000]}")
    r = subprocess.run([str(BUILD / "marge_rig")], capture_output=True,
                       text=True, timeout=600)
    print(r.stdout)
    if r.returncode != 0:
        print("!!", r.returncode, r.stderr[:600])
        return 2
    lignes = r.stdout.splitlines()

    # ---- le registre ----------------------------------------------------------
    reg: dict = {"duree_s": round(time.monotonic() - t0, 1),
                 "octets": {"ent4": len(o_ent4), "hisse": len(o_hisse),
                            "ent8": len(o_ent8), "mut": len(o_mut),
                            "plancher": len(o_plancher), "v4i": len(o_v4i),
                            "avx2": len(o_avx2), "tls15": len(o_tls15),
                            "tls16": len(o_tls16), "scelle13": len(o_sc13)},
                 "rva": {k: (hex(v) if isinstance(v, int)
                             else [hex(x) for x in v])
                         for k, v in RVA.items()},
                 "round_trip": rt,
                 "mutation": {"offset": cible, "avant": "0x90",
                              "apres": "0x91",
                              "cible": "movdqu xmm4, [rbx + 0x90] (flot 0)"},
                 "comptes_unicorn": comptes,
                 "batterie_unicorn": {"vecteurs": bat_unicorn["batterie"],
                                      "divergences":
                                          len(bat_unicorn["divergences"])},
                 "parite": {}, "mesures": {}}
    cpuinfo = pathlib.Path("/proc/cpuinfo").read_text()
    modele = re.search(r"model name\s*:\s*(.+)", cpuinfo).group(1).strip()
    mhz = re.findall(r"cpu MHz\s*:\s*([\d.]+)", cpuinfo)
    tous = [l.split(":", 1)[1].split() for l in cpuinfo.splitlines()
            if l.startswith("flags")][0]
    reg["machine"] = modele
    reg["mhz"] = mhz[0] if mhz else "?"
    reg["drapeaux"] = " ".join(sorted(
        set(tous) & {"aes", "avx2", "constant_tsc", "rdtscp", "sse2",
                     "pclmulqdq", "avx512f"}))
    for l in lignes:
        p = l.split()
        if not p:
            continue
        if p[0] == "CALENDRIER":
            reg["parite"]["calendrier_fips"] = p[1] == "1"
        elif p[0] == "CALENDRIER8":
            reg["parite"]["calendrier_huit_cles"] = p[1]
        elif p[0] == "FIPS":
            reg["parite"].setdefault("fips_c1", {})[p[1]] = p[2] == "1"
        elif p[0] == "NEGATIF":
            reg["parite"]["negatif"] = p[1]
        elif p[0] in ("DIFF", "QUEUE", "DIFFCLES64", "DIFFCLES256"):
            reg["parite"].setdefault(p[0].lower(), {})[
                f"{p[1]}@{p[2].split('/')[0].zfill(4)}"] = p[2]
        elif p[0] == "BORNE":
            reg["parite"].setdefault("borne", {})[p[1]] = {
                "rax_m2": p[2] == "1", "rien_chiffre": p[3] == "1"}
        elif p[0] == "BATTERIE":
            # BATTERIE avx2 <n> repli <n> (sur 559)
            reg["parite"]["batterie_native_avx2"] = p[2]
            reg["parite"]["batterie_native_repli"] = p[4]
        elif p[0] == "MESURE":
            reg["mesures"][p[1]] = {
                "cycles_mediane": int(p[2]), "cycles_iqr": int(p[3]),
                "par_op_mediane": float(p[4]), "par_op_iqr": float(p[5])}

    # ---- la garde APRÈS -------------------------------------------------------
    empreintes_apres = garde_sceau("APRÈS")
    assert empreintes_apres == empreintes

    (REG / "marge-vierge.json").write_text(
        json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    (ICI / "rapport-marge-vierge.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("VERDICT", "VERT" if verdit(reg) else "ROUGE")
    return 0 if verdit(reg) else 2


def verdit(reg: dict) -> bool:
    p = reg["parite"]

    def plein(d: dict) -> bool:
        return d and all(v.split("/")[0] == v.split("/")[1]
                         for v in d.values())

    return (p["calendrier_fips"] and p["calendrier_huit_cles"] == "8/8"
            and all(p["fips_c1"].values()) and p["negatif"] == "ATTRAPE"
            and plein(p["diff"]) and plein(p["queue"])
            and plein(p.get("diffcles64", {}))
            and plein(p.get("diffcles256", {}))
            and p["batterie_native_avx2"] == "0"
            and p["batterie_native_repli"] == "0"
            and all(v["rax_m2"] and v["rien_chiffre"]
                    for v in p["borne"].values())
            and all(rt for rt in reg["round_trip"].values())
            and not reg["batterie_unicorn"]["divergences"]
            and "hisse-avx2@4096" in reg["mesures"])


if __name__ == "__main__":
    sys.exit(main())
