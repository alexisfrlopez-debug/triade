#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""scenario-shani.py — LE TERRAIN DE LA MESURE AVANT/APRÈS SHA-NI (kit
terrain, D205 — le paquet 6/6 de la vague 3, l'instruction lfh49a1xf).

LA MESURE DU DÉVELOPPEUR sur SA machine, dans les conditions EXACTES que
l'instruction exige :
  - la MÊME machine (la vôtre — le scénario ne tourne que sur elle) ;
  - la MÊME entrée : 8 Mio de PRNG déterministe (graine 20261112) —
    bit-identiques par construction, les DEUX bras sur les MÊMES octets ;
  - le condensé VÉRIFIÉ à hashlib AVANT comptage (et CHAQUE répétition
    re-vérifie : une répétition au condensé faux ABORTE la mesure) ;
  - les opérations COMPLÈTES init+absorb+final — jamais un périmètre
    partiel : chaque bras hache le tampon ENTIER de bout en bout ;
  - l'avant = la composition SCELLÉE (tls13-01/03/04, les octets déployés
    de loupe.exe — ceux que vos onze runs ont vécus) ; l'après = la
    VARIANTE (tls13-01 + shani-03 à dispatch + tls13-04) TELLE QUE
    DISPATCHÉE par votre processeur ; le repli forcé (la sonde neutralisée
    en copie de laboratoire) mesure le chemin scalaire de la variante sur
    machine SHA-Ni — les TROIS bras, 15 répétitions chacun, médianes/IQR.

LE KIT porte UNE image (image-shani.bin — l'empreinte au manifeste) : la
table K du scellé, le masque, la famille sha SCELLÉE (le repli, R7) et la
variante — TOUTES les références internes relatives : l'image vit à la
base que le scénario alloue. AUCUN SCELLAGE : pièce de laboratoire ; la
cérémonie d'ère et la décision d'embarquer la variante vous appartiennent.

Usage : python3 scenario-shani.py
        (écrit temoin-shani.txt au répertoire courant — renvoyez-le au labo)
"""

from __future__ import annotations

import ctypes
import hashlib
import mmap
import os
import platform
import random
import struct
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))

# --- L'IMAGE DU KIT (l'empreinte recoupée AVANT toute exécution) -------------------

IMAGE = "image-shani.bin"
EMPREINTE_IMAGE = ("df851b7c0041d700ce6500e401d98a4a"
                   "6b3c100a2b001d274256f6b7b16da47f")
DEBUT_RVA = 0x2000

# les RVA du plan (le miroir de shani/layout.py — la source unique au dépôt)
R_TLS01, R_TLS03, R_TLS04 = 0xC000, 0xC240, 0xC300
R_SHANI01, R_SHANI03 = 0xD000, 0xD400

# LES OCTETS PRÉ-ASSEMBLÉS (le labo les a assemblés par keystone — le
# scénario du terrain n'exige AUCUN outil : les gabarits sont CONSIGNÉS
# avec leur source ; l'imm64 du trampoline est patché au geste) :
#   le trampoline SysV→msx64 :
#     mov r8, rdx ; mov rdx, rsi ; mov rcx, rdi ; mov rax, imm64 ; jmp rax
#   (sous Windows, ctypes EST msx64 — le trampoline demeure inutilisé)
TRAMPO_SYSP = bytes.fromhex("4989d04889f24889f948b8") + b"\0" * 8 \
    + bytes.fromhex("ffe0")
TRAMPO_IMM64 = 11
#   le lecteur de cycles : lfence ; rdtsc ; shl rdx, 32 ; or rax, rdx ; ret
RDTSC = bytes.fromhex("0faee80f3148c1e2204809d0c3")

GRAINE = 20261112
TAILLE = 8 * 1024 * 1024
REPETITIONS = 15

VECTEURS_FIPS = [
    ("le vide", b"",
     "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("« abc »", b"abc",
     "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
    ("les 448 bits",
     b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
     "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
    ("les 896 bits",
     b"abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmno"
     b"ijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu",
     "cf5b16a778af8380036ce59e7b0492370b249b11e8f07a51afac45037afee9d1"),
]


class Terrain:
    """La mémoire exécutable allouée au geste, l'image posée, les appels
    par trampoline (POSIX) ou directly (Windows — ctypes est msx64)."""

    def __init__(self):
        self.est_windows = (sys.platform == "win32")
        donnees = open(os.path.join(ICI, IMAGE), "rb").read()
        eu = hashlib.sha256(donnees).hexdigest()
        if eu != EMPREINTE_IMAGE:
            raise SystemExit(f"l'image du kit a divergé : {eu}")
        self.image_octets = donnees
        # la carte : l'alignement de page + l'image (48 Kio) + les zones
        # de travail (contexte, sortie, rdtsc, trampolines) — généreuse
        taille = len(donnees) + 0x1000 + 0x20000
        if self.est_windows:
            k32 = ctypes.windll.kernel32
            self.adr = k32.VirtualAlloc(
                None, ctypes.c_size_t(taille), 0x3000, 0x40)
            if not self.adr:
                raise SystemExit("VirtualAlloc a refusé")
            self.base = self.adr + 0x1000
        else:
            self.mem = mmap.mmap(-1, taille,
                                 prot=mmap.PROT_READ | mmap.PROT_WRITE
                                 | mmap.PROT_EXEC)
            self.base = ctypes.addressof(
                ctypes.c_char.from_buffer(self.mem)) + 0x1000
        # l'image posée : le blob à base + 0 (les RVA internes relatifs)
        self._ecrire_abs(self.base, donnees)
        # les zones de travail AU-DELÀ de l'image (0xE000-0xEFFF libres)
        self.ctx = self.base + 0xE000
        self.sortie = self.base + 0xE100
        # le lecteur de cycles
        self.rdtsc_adr = self.base + 0xE200
        self._ecrire_abs(self.rdtsc_adr, RDTSC)
        # les trampolines (un par cible — inutiles sous Windows)
        self._trampolines: dict[int, int] = {}
        self._cur_trampo = 0xE300
        if self.est_windows:
            self.fn3 = ctypes.CFUNCTYPE(
                ctypes.c_uint64, ctypes.c_void_p, ctypes.c_void_p,
                ctypes.c_void_p)
        else:
            self.fn3 = ctypes.CFUNCTYPE(
                ctypes.c_uint64, ctypes.c_void_p, ctypes.c_void_p,
                ctypes.c_void_p)

    def _ecrire_abs(self, adr: int, donnees: bytes) -> None:
        if self.est_windows:
            ctypes.memmove(adr, donnees, len(donnees))
        else:
            offset = adr - (self.base - 0x1000)
            self.mem[offset:offset + len(donnees)] = donnees

    def _lire_abs(self, adr: int, n: int) -> bytes:
        if self.est_windows:
            tampon = ctypes.create_string_buffer(n)
            ctypes.memmove(tampon, adr, n)
            return tampon.raw[:n]
        offset = adr - (self.base - 0x1000)
        return bytes(self.mem[offset:offset + n])

    def adresse(self, rva: int) -> int:
        return self.base + (rva - DEBUT_RVA)

    def pointeur(self, rva: int):
        if self.est_windows:
            return ctypes.cast(self.adresse(rva), self.fn3)
        if rva not in self._trampolines:
            g = bytearray(TRAMPO_SYSP)
            struct.pack_into("<Q", g, TRAMPO_IMM64, self.adresse(rva))
            adr = self.base + self._cur_trampo
            self._ecrire_abs(adr, bytes(g))
            self._trampolines[rva] = adr
            self._cur_trampo += 32
        return ctypes.cast(self._trampolines[rva], self.fn3)

    def appeler(self, rva: int, a1=0, a2=0, a3=0):
        return self.pointeur(rva)(a1, a2, a3)

    def cycles(self) -> int:
        lecteur = ctypes.CFUNCTYPE(ctypes.c_uint64)(
            self.rdtsc_adr)
        return lecteur()


def main() -> int:
    print("=== scenario-shani.py — LA MESURE AVANT/APRÈS SHA-NI (kit D205) ===")
    print(f"machine : {platform.node()} · {platform.machine()} · "
          f"{platform.system()} · Python {platform.python_version()}")
    t = Terrain()
    print(f"l'image posée (sha256 recoupé) · la base "
          f"{t.base:#x} · le trampoline "
          f"{'INUTILE (ctypes est msx64)' if t.est_windows else 'SysV→msx64'}")

    # LA SONDE : le verdict de VOTRE processeur
    verdict = t.appeler(R_SHANI01)
    print(f"la sonde CPUID : rax = {verdict} "
          f"({'SHA-NI + SSSE3 présents' if verdict == 1 else 'le repli scalaire — la variante vivra le chemin scellé'})")

    # le tampon des données (LA MÊME entrée aux deux bras)
    rng = random.Random(f"{GRAINE}:mesure")
    tampon = rng.randbytes(TAILLE)
    attendu = hashlib.sha256(tampon).digest()
    if t.est_windows:
        buf = ctypes.create_string_buffer(tampon, len(tampon))
        buf_adr = ctypes.addressof(buf)
    else:
        membuf = mmap.mmap(-1, TAILLE,
                           prot=mmap.PROT_READ | mmap.PROT_WRITE)
        membuf[0:TAILLE] = tampon
        buf_adr = ctypes.addressof(ctypes.c_char.from_buffer(membuf))

    def condense(variante: bool) -> bytes:
        t.appeler(R_TLS01, t.ctx, 0, 0)
        cible = R_SHANI03 if variante else R_TLS03
        r = t.appeler(cible, t.ctx, buf_adr, TAILLE)
        assert r == 0, f"absorption rax={r}"
        r = t.appeler(R_TLS04, t.ctx, t.sortie, 0)
        assert r == 0, f"finalisation rax={r}"
        return t._lire_abs(t.sortie, 32)

    # 1. LES VECTEURS DORÉS aux TROIS compositions (avant toute mesure : un
    #    condensé faux ABORTE le kit — jamais de chiffre sur un hachage faux)
    lignes = []
    ok_fips = True
    for nom, message, attendu_hex in VECTEURS_FIPS:
        if t.est_windows:
            mb = ctypes.create_string_buffer(message, max(1, len(message)))
            m_adr = ctypes.addressof(mb)
        else:
            membuf2 = mmap.mmap(-1, max(1, len(message)),
                                prot=mmap.PROT_READ | mmap.PROT_WRITE)
            membuf2[0:len(message)] = message
            m_adr = ctypes.addressof(ctypes.c_char.from_buffer(membuf2))
        t.appeler(R_TLS01, t.ctx, 0, 0)
        r1 = t.appeler(R_TLS03, t.ctx, m_adr, len(message))
        r2 = t.appeler(R_TLS04, t.ctx, t.sortie, 0)
        eu_scellee = t._lire_abs(t.sortie, 32)
        t.appeler(R_TLS01, t.ctx, 0, 0)
        r3 = t.appeler(R_SHANI03, t.ctx, m_adr, len(message))
        r4 = t.appeler(R_TLS04, t.ctx, t.sortie, 0)
        eu_variante = t._lire_abs(t.sortie, 32)
        bon = (eu_scellee == eu_variante
               == bytes.fromhex(attendu_hex)
               == hashlib.sha256(message).digest()
               and r1 == r2 == r3 == r4 == 0)
        ok_fips &= bon
        lignes.append(f"FIPS {nom:14} : {'VERT' if bon else 'ÉCHEC'}")
        print(f"  FIPS {nom:14} : {'VERT' if bon else 'ÉCHEC'}")
    if not ok_fips:
        lignes.append("VERDICT : ÉCHEC — un vecteur doré faux, la mesure est REFUSÉE")
        open("temoin-shani.txt", "w").write("\n".join(lignes) + "\n")
        print("VERDICT : ÉCHEC — le témoin écrit, la mesure refusée")
        return 1

    # 2. LA MESURE — condensé vérifié AVANT comptage, répétitions re-vérifiées
    def mesurer(variante: bool):
        assert condense(variante) == attendu, \
            "le condensé du bras ne vérifie PAS — la mesure est refusée"
        valeurs = []
        for _ in range(REPETITIONS):
            c0 = t.cycles()
            eu = condense(variante)
            c1 = t.cycles()
            if eu != attendu:
                raise SystemExit("une répétition au condensé faux — "
                                 "la mesure est ABORTÉE")
            valeurs.append(c1 - c0)
        return valeurs

    bras = {}
    bras["l'avant (composition scellée)"] = mesurer(False)
    bras["l'après (variante dispatchée)"] = mesurer(True)

    # le repli forcé : la sonde neutralisée EN COPIE (l'image du kit est une
    # pièce de laboratoire — la neutralisation ne touche AUCUN scellé)
    neutre = bytes.fromhex("31c0c3")        # xor eax, eax ; ret
    vraie_sonde = t._lire_abs(t.adresse(R_SHANI01), 16)
    t._ecrire_abs(t.adresse(R_SHANI01), neutre)
    t.appeler(R_TLS01, t.ctx, 0, 0)        # ré-init : un contexte propre
    bras["la variante à repli forcé"] = mesurer(True)
    t._ecrire_abs(t.adresse(R_SHANI01), vraie_sonde)

    def stats(v):
        s = sorted(v)
        return s[len(s) // 2], s[len(s) // 4], s[3 * len(s) // 4]

    # la fréquence estimée (le mur autour de toutes les répétitions)
    m0 = time.monotonic()
    c0 = t.cycles()
    time.sleep(0)
    _ = condense(False)
    c1 = t.cycles()
    m1 = time.monotonic()
    hz = (c1 - c0) / max(1e-9, m1 - m0)

    print()
    rapports = {}
    for nom, vals in bras.items():
        med, q1, q3 = stats(vals)
        rapports[nom] = (med, q1, q3, med / TAILLE, med / hz if hz else 0)
        print(f"  {nom:32} médiane {med:>14,} cycles "
              f"[IQR {q1:,}..{q3:,}] · {med / TAILLE:.3f} cycles/o")
    gain = rapports["l'avant (composition scellée)"][0] \
        / rapports["l'après (variante dispatchée)"][0]
    surcharge = rapports["la variante à repli forcé"][0] \
        / rapports["l'avant (composition scellée)"][0]
    print(f"  → LE GAIN : {gain:.2f}× · la surcharge du dispatch : "
          f"{surcharge * 100 - 100:+.2f} % · le verdict de la sonde : "
          f"{verdict}")

    lignes += [
        "",
        "TÉMOIN DE LA MESURE AVANT/APRÈS SHA-NI (kit D205, l'instruction "
        "lfh49a1xf)",
        "=============================================================="
        "=====",
        f"machine      : {platform.node()} · {platform.system()} "
        f"{platform.machine()} · Python {platform.python_version()}",
        f"la sonde     : rax = {verdict} (1 = SHA-NI+SSSE3 présents, "
        "0 = le repli scalaire)",
        f"l'entrée     : {TAILLE} octets de PRNG déterministe (graine "
        f"{GRAINE}:mesure) — la MÊME aux deux bras",
        f"l'attendu    : sha256 {attendu.hex()}",
        "la discipline: le condensé VÉRIFIÉ à hashlib AVANT comptage, "
        "CHAQUE répétition re-vérifiée (une répétition fausse ABORTE), "
        "les opérations COMPLÈTES init+absorb+final, jamais un périmètre "
        "partiel",
        f"répétitions  : {REPETITIONS} par bras · les médianes et IQR "
        "en cycles RDTSC (lfence+rdtsc)",
        f"fréquence    : ~{hz / 1e9:.2f} GHz (estimation mur/cycles)",
        "",
    ]
    for nom, (med, q1, q3, cpo, ms) in rapports.items():
        lignes.append(f"{nom:32} médiane {med:>14,} cycles "
                      f"[IQR {q1:,}..{q3:,}] · {cpo:.3f} cycles/o "
                      f"· ~{ms * 1000:.1f} ms")
    lignes += [
        "",
        f"LE GAIN      : {gain:.2f}× (l'avant / l'après)",
        f"la surcharge : {surcharge * 100 - 100:+.2f} % (la variante à "
        "repli forcé contre la composition scellée)",
        "",
        "L'IMAGE DU KIT : image-shani.bin sha256 " + EMPREINTE_IMAGE,
        "la famille sha du repli : les octets DÉPLOYÉS de loupe.exe "
        "(c1115105…) extraits à leurs RVA scellées — R7",
        "AUCUN SCELLAGE : la cérémonie d'ère et la décision d'embarquer "
        "la variante appartiennent au développeur.",
    ]
    open("temoin-shani.txt", "w").write("\n".join(lignes) + "\n")
    print("\nle témoin écrit : temoin-shani.txt — renvoyez-le au labo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
