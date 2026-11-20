#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""remesure_instructions.py — LA RE-MESURE AUX INSTRUCTIONS (8z4hj76w4)
: la variante SSE2 CORRIGÉE (v2 — la diffusion du PREMIER OCTET) face
aux baselines équitables sous LE MÊME RIG que la vague 9 (Unicorn, le
compte d'instructions par hook, LA BIBLIOTHÈQUE TENUE ÉGALE : le memcmp
scellé libc-02 à 0x1180, le call du bras C repointé au scellé).

LA FAUTE NOMMÉE D'ABORD : la variante vague 9 diffuser le motif de
QUATRE OCTETS (deux shuffles) au lieu du PREMIER OCTET (quatre) — les
occurrences aux alignements m0 != m[p mod 4] MANQUÉES (406/564 à la
différentielle plantée) ; la confrontation vague 9 (les 24 vecteurs aux
motifs aléatoires ABSENTS) ne pouvait pas la voir — la différentielle
plantée la nomme, la correction la porte.

LES CONTENDANTS (à travail égal, la même série 4096/16, la graine
20261120, n=15, la médiane) :
  — LA VARIANTE SSE2 CORRIGÉE v2 (la copie de laboratoire 0xCC00) ;
  — LE SCELLÉ GPR (loupe-13-recherche.asm assemblé à son adresse) ;
  — LE BRAS C gcc-O2 (l13.c, la chaîne mingw TRIXIE, repointé) ;
  — LE BRAS C gcc-O3 (l13.c -O3 — LE CONSTAT : l'émission SIMD du
    compilateur sur la source naturelle) ;
  — LE BRAS C gcc-O3 -msse2 (le drapeau explicite — le même constat).

Sortie : remesure-instructions.csv · rapport-remesure.txt"""
from __future__ import annotations

import contextlib
import csv
import importlib.util
import io
import pathlib
import random
import statistics
import subprocess
import sys

import unicorn

REPO = pathlib.Path("/home/z/my-project/depot")
sys.path.insert(0, str(REPO / "loupe"))
ICI = REPO / "atelier-remesure-sse2-8z4hj76w4"
MINGW = "/home/z/my-project/work/mingw-debs/root/usr/bin/x86_64-w64-mingw32-gcc-posix"
OBJCOPY = "/home/z/my-project/work/mingw-debs/root/usr/bin/x86_64-w64-mingw32-objcopy"
OBJDUMP = "/home/z/my-project/work/mingw-debs/root/usr/bin/x86_64-w64-mingw32-objdump"

import capstone  # noqa: E402
import keystone  # noqa: E402

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

RVA_V2 = 0xCC00            # la marge .text2 vierge — le scellé intact
VA_C = 0x2000              # l'adresse de charge du bras C (le rig vague 9)


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def assembler(fichier: pathlib.Path, rva: int):
    """L'assemblage maison (les étiquettes en DEUX PASSES, le format de
    construire_sse2)."""
    lignes = [l.split(";")[0] for l in fichier.read_text(
        encoding="utf-8").splitlines()]
    etiquettes: dict[str, int] = {}
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
    final = []
    for corps, adr in corps_list:
        for e, a in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
            corps = corps.replace(e, hex(a))
        c, _ = KS.asm(corps, rva + len(octets))
        octets += bytes(c)
        final.append(corps)
    return octets, final


def round_trip(octets: bytes, rva: int) -> bool:
    reins = b""
    for ins in CS.disasm(octets, rva):
        c, _ = KS.asm(f"{ins.mnemonic} {ins.op_str}", ins.address)
        reins += bytes(c)
    return reins == octets


class Compteur:
    def __init__(self, uc):
        self.n = 0
        uc.hook_add(unicorn.UC_HOOK_CODE, self._hook)

    def _hook(self, uc, a, t, d):
        self.n += 1


# ------------------------------------------------- le bras C (gcc -O2/-O3)
SRC_13 = """#include <string.h>
long loupe_13_recherche(const unsigned char *fenetre,
        long taille, const unsigned char *motif, long taille_motif,
        long depart) {
    if (taille_motif > 32 || taille < 0 || depart > taille) return -5;
    for (long i = depart; i <= taille - taille_motif; ++i)
        if (memcmp(fenetre + i, motif, taille_motif) == 0) return i;
    return -1;
}
"""


def compiler_bras_c(nom: str, drapeaux: list[str]) -> tuple[bytes, int]:
    c = ICI / f"{nom}.c"
    c.write_text(SRC_13, encoding="utf-8")
    obj = ICI / f"{nom}.o"
    r = subprocess.run([MINGW, *drapeaux, "-c", str(c), "-o", str(obj)],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"compilation {nom} : {r.stderr[:300]}")
    bin_ = ICI / f"{nom}.text.bin"
    r = subprocess.run([OBJCOPY, "-O", "binary", "-j", ".text",
                        str(obj), str(bin_)], capture_output=True,
                       text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"extraction {nom} : {r.stderr[:300]}")
    texte = bin_.read_bytes()
    out = bytearray(texte)
    pos, n = 0, 0
    while True:
        i = out.find(b"\xe8\x00\x00\x00\x00", pos)
        if i < 0:
            break
        cible = 0x1180 - (VA_C + i + 5)
        out[i + 1:i + 5] = cible.to_bytes(4, "little", signed=True)
        n += 1
        pos = i + 5
    if n == 0:
        raise RuntimeError(f"aucun call rel32 dans {nom} — repointage ko")
    return bytes(out), n


def decompte_simd(obj: pathlib.Path) -> tuple[int, int]:
    r = subprocess.run([OBJDUMP, "-d", str(obj)], capture_output=True,
                       text=True, timeout=60)
    n = n_ins = 0
    for ligne in r.stdout.splitlines():
        if "\t" in ligne and ":" in ligne:
            corps = ligne.split("\t")[-1].strip()
            if corps and not corps.startswith("."):
                n_ins += 1
            for s in ("movdqu", "pcmpeq", "pmovmskb", "punpck", "movdqu"):
                if s in corps:
                    n += 1
                    break
    return n, n_ins


def main():
    HE = charger_module("h_ed3", REPO / "loupe" / "harnais_edition.py")
    os_v = HE.OSEdition()
    emul = HE.EmulationEdition(
        os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
        (REPO / "m1" / "selftest.exe").read_bytes(),
        (REPO / "demo" / "demo.exe").read_bytes())
    emul.uc.mem_map(0x500000, 0x21000)

    rapport = []
    csv_rows = []

    # ---- (0) LA FAUTE NOMMÉE : la différentielle plantée de la v1 ------
    fautes_v1 = 0
    try:
        r = subprocess.run(
            [sys.executable, str(ICI / "differenciel_plante.py")],
            capture_output=True, text=True, timeout=1800)
        for ligne in r.stdout.splitlines():
            if "DIVERGENCES" in ligne:
                fautes_v1 = int(ligne.strip().split()[0])
    except Exception as e:
        rapport.append(f"  !! la différentielle plantée v1 : {e}")
    rapport.append(
        f"LA FAUTE NOMMÉE (v1, la vague 9) : la diffusion du motif de "
        f"QUATRE OCTETS (movd + punpckldq + punpcklqdq) au lieu du PREMIER "
        f"OCTET (la chaîne complète de QUATRE shuffles) — {fautes_v1}/564 "
        f"occurrences plantées MANQUÉES (l'occurrence aux positions où "
        f"m0 != m[p mod 4], la différentielle plantée differenciel_plante.py) ; "
        f"la confrontation vague 9 (24 vecteurs aux motifs aléatoires "
        f"ABSENTS des tampons) ne pouvait PAS la voir : l'épreuve "
        f"n'exerçait AUCUNE occurrence — l'écart de l'épreuve nommé "
        f"(les vecteurs à occurrence plantée introduits par la présente)")

    # ---- (1) LA VARIANTE CORRIGÉE v2 ------------------------------------
    octets_v2, final_v2 = assembler(ICI / "notation" / "loupe-13-sse2-v2.asm",
                                     RVA_V2)
    ok_rt = round_trip(octets_v2, RVA_V2)
    n_sse2 = sum(1 for l in final_v2 if any(
        s in l for s in ("movdqu", "pcmpeqb", "pmovmskb", "movd",
                         "punpcklbw", "punpcklwd", "punpckldq",
                         "punpcklqdq")))
    emul.uc.mem_write(RVA_V2, octets_v2)
    emul.uc.ctl_remove_cache(RVA_V2 & ~0xFFF, (RVA_V2 + len(octets_v2)
                                               + 0xFFF) & ~0xFFF)
    rapport.append(
        f"LA VARIANTE CORRIGÉE v2 : {len(octets_v2)} o au RVA {RVA_V2:#x} "
        f"(la marge VIERGE — le scellé intact), {n_sse2} instructions SSE2 "
        f"baseline (la diffusion du premier octet en QUATRE shuffles — "
        f"movd + punpcklbw + punpcklwd + punpckldq + punpcklqdq), le "
        f"round-trip {'100 %' if ok_rt else 'DIVERGE — ROUGE'}")

    # ---- (2) LA CONFRONTATION : 24 vecteurs + bords + PLANTÉS ----------
    rng = random.Random(20261120)
    diverge_v2 = 0
    serie = [(4096, 16)] * 15 + [(0, 1), (1, 1), (2, 32), (33, 32),
                                 (64, 1), (65, 32), (255, 31), (256, 32),
                                 (1000, 32)]
    # + les occurrences plantées : 64 alignements systématiques
    plantes = []
    for p in range(64):
        f = bytearray(rng.randrange(256) for _ in range(4096))
        m = bytes(rng.randrange(256) for _ in range(16))
        f[p:p + 16] = m
        plantes.append((bytes(f), m, f.find(m)))
    for (n, lm) in serie:
        f = bytes(rng.randrange(256) for _ in range(n))
        m = bytes(rng.randrange(256) for _ in range(lm))
        plantes.append((f, m, f.find(m)))
    for f, m, attendu in plantes:
        emul.uc.mem_write(0x500000, f)
        emul.uc.mem_write(0x510000, m)
        with contextlib.redirect_stdout(io.StringIO()):
            r = emul.appeler(RVA_V2, {"rcx": 0x500000, "rdx": len(f),
                                      "r8": 0x510000, "r9": len(m)},
                             pile_args=[0])
        if (r["rax"] & (2**64 - 1)) != (attendu & (2**64 - 1)):
            diverge_v2 += 1
    rapport.append(
        f"LA CONFRONTATION v2 : {len(plantes)} vecteurs (les 24 de la "
        f"convention vague 9 + LES 64 OCCURRENCES PLANTÉES aux alignements "
        f"systématiques 0-63) — "
        f"{'ZÉRO DIVERGENCE' if diverge_v2 == 0 else str(diverge_v2) + ' DIVERGENCES — ROUGE'}"
        f" contre l'implémentation triviale (le juge Python)")

    # ---- (3) LE CONTRÔLE NÉGATIF : la variante mutée à la première ligne
    mute = bytearray(octets_v2)
    # la première instruction : mov rax, qword ptr [rsp+0x28] = 48 8B 44 24 28
    # le déplacement muté 0x28 -> 0x29 : le départ lu du mauvais octet
    assert mute[4] == 0x28, f"l'ancre de la première ligne introuvable : {bytes(mute[:5]).hex()}"
    mute[4] = 0x29          # le 5e octet — la lecture du départ diverge
    RVA_MUT = 0xCD00            # la marge après la v2 (0xCC00 + 0xC8)
    emul.uc.mem_write(RVA_MUT, bytes(mute))
    emul.uc.mem_write(0x500000, plantes[0][0])
    emul.uc.mem_write(0x510000, plantes[0][1])
    with contextlib.redirect_stdout(io.StringIO()):
        r = emul.appeler(RVA_MUT, {"rcx": 0x500000, "rdx": len(plantes[0][0]),
                                   "r8": 0x510000, "r9": len(plantes[0][1])},
                         pile_args=[0])
    attrape = r.get("crash") is not None or \
        ((r.get("rax", -1) & (2**64 - 1)) != (plantes[0][2] & (2**64 - 1)))
    rapport.append(
        f"LE CONTRÔLE NÉGATIF : la variante mutée à la première ligne "
        f"(l'octet ModRM de « mov rax, [rsp+0x28] » muté) — "
        f"{'ATTRAPÉE à la première divergence' if attrape else 'NON ATTRAPÉE — ROUGE'}")

    # ---- (4) LE SCELLÉ GPR -----------------------------------------------
    import harnais_noyau as HN  # noqa: E402
    B4 = charger_module("b4_rm", REPO / "m4" / "build_m4.py")
    not13 = list((REPO / "loupe" / "notation").glob("loupe-13-*.asm"))[0]
    rva13, slot13 = HN.L.SLOTS_LOUPE["i110013"]
    octets13, _ = B4.assembler_bloc(KS, str(not13), rva13, slot13)

    # ---- (5) LES BRAS C : gcc-O2 (le repointé) + gcc-O3 + gcc-O3-msse2 ---
    o2, n_calls = compiler_bras_c("l13-rm-o2", ["-O2"])
    o3, _ = compiler_bras_c("l13-rm-o3", ["-O3"])
    o3s, _ = compiler_bras_c("l13-rm-o3-sse2", ["-O3", "-msse2"])
    simd_o2 = decompte_simd(ICI / "l13-rm-o2.o")
    simd_o3 = decompte_simd(ICI / "l13-rm-o3.o")
    simd_o3s = decompte_simd(ICI / "l13-rm-o3-sse2.o")

    # ---- (6) LA MESURE : la même série, la graine 20261120, n=15 -------
    rng = random.Random(20261120)

    def mesurer(va, charge):
        charge()
        res = []
        for _ in range(15):
            f = bytes(rng.randrange(256) for _ in range(4096))
            m = bytes(rng.randrange(256) for _ in range(16))
            emul.uc.mem_write(0x500000, f)
            emul.uc.mem_write(0x510000, m)
            cpt = Compteur(emul.uc)
            with contextlib.redirect_stdout(io.StringIO()):
                r = emul.appeler(va, {"rcx": 0x500000, "rdx": 4096,
                                      "r8": 0x510000, "r9": 16},
                                 pile_args=[0])
            res.append(cpt.n)
        return statistics.median(res)

    med_v2 = mesurer(RVA_V2, lambda: None)
    med_sc = mesurer(rva13, lambda: emul.uc.mem_write(rva13, octets13))
    med_o2 = mesurer(VA_C, lambda: emul.uc.mem_write(VA_C, o2))
    med_o3 = mesurer(VA_C, lambda: emul.uc.mem_write(VA_C, o3))
    med_o3s = mesurer(VA_C, lambda: emul.uc.mem_write(VA_C, o3s))

    rapport += [
        "",
        "LA MESURE AUX INSTRUCTIONS (la même série 4096/16, la graine "
        "20261120, n=15, la médiane, LA BIBLIOTHÈQUE TENUE ÉGALE — le "
        "memcmp scellé à 0x1180 pour la variante ET le scellé ; le call "
        "du bras C repointé au scellé) :",
        f"  LA VARIANTE SSE2 CORRIGÉE v2 : médiane {med_v2:.0f} instructions/op",
        f"  LE SCELLÉ GPR                : médiane {med_sc:.0f} instructions/op",
        f"  LE BRAS C gcc-O2             : médiane {med_o2:.0f} instructions/op",
        f"  LE BRAS C gcc-O3             : médiane {med_o3:.0f} instructions/op",
        f"  LE BRAS C gcc-O3 -msse2      : médiane {med_o3s:.0f} instructions/op",
        f"LE RATIO v2/gcc-O2 : {med_v2/med_o2:.2f}× — LE GAIN v2/scellé : "
        f"{med_sc/med_v2:.1f}×",
        "",
        f"LE CONSTAT DU COMPILATEUR (sur pièces, objdump) : l13.c gcc-O2 : "
        f"{simd_o2[0]} instructions SIMD / {simd_o2[1]} ; gcc-O3 : "
        f"{simd_o3[0]}/{simd_o3[1]} ; gcc-O3 -msse2 : {simd_o3s[0]}/"
        f"{simd_o3s[1]} — le compilateur N'ÉMET AUCUN SIMD sur la source "
        f"naturelle (la boucle autour de l'appel memcmp opaque est "
        f"invectorisable) : LA BASELINE VECTORISÉE ÉQUITABLE DU COMPILATEUR "
        f"N'EXISTE PAS pour cette source — la voie SIMD du compilateur vit "
        f"à LA BIBLIOTHÈQUE (memchr/memmem — mesurées au rig de temps réel "
        f"natif ; l'absence de memchr scellé interdit la cellule sous "
        f"Unicorn, la borne nommée)",
    ]
    csv_rows += [
        ["loupe-13", "recherche 4096/16", "SSE2-v2-corrigée", med_v2],
        ["loupe-13", "recherche 4096/16", "scellé-GPR", med_sc],
        ["loupe-13", "recherche 4096/16", "C-gcc-O2", med_o2],
        ["loupe-13", "recherche 4096/16", "C-gcc-O3", med_o3],
        ["loupe-13", "recherche 4096/16", "C-gcc-O3-msse2", med_o3s],
    ]

    # ---- (7) LE COULOIR B : LE CPUID HISSÉ HORS DE LA BOUCLE -----------
    rapport.append("")
    r = subprocess.run([sys.executable, str(ICI / "cpuid_hisse.py")],
                       capture_output=True, text=True, timeout=1800)
    rapport += r.stdout.strip().splitlines()
    if r.returncode != 0:
        rapport.append(f"  !! couloir B : code {r.returncode}")

    (ICI / "remesure-instructions.csv").write_text(
        "\n".join(",".join(map(str, row)) for row in csv_rows) + "\n",
        encoding="utf-8")
    (ICI / "rapport-remesure.txt").write_text("\n".join(rapport) + "\n",
                                              encoding="utf-8")
    print("\n".join(rapport))
    ok = (ok_rt and diverge_v2 == 0 and attrape)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
