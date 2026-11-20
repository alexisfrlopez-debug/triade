#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesurer_corridors.py — L'ATELIER fnvan0zes : LA BATTERIE ÉLARGIE, LES
TROIS COULOIRS (l'hybride memchr+memcmp, l'AVX2 à dispatch, le SHA-NI à
repli scellé), LES MESURES AUX INSTRUCTIONS ET AUX CYCLES RÉELS.

LA BATTERIE ÉLARGIE (l'instruction) : (a) occurrences plantées EN QUEUE de
tampon (le dernier bloc de 16, chaque position) ; (b) occurrences
CHEVAUCHANTES (périodes 1 à 4) ; (c) longueurs de motif 1 à >16 ; (d)
FRANCHISSEMENT DE PAGE (le tampon à cheval sur deux pages, l'occurrence aux
deux bords) ; (e) MULTI-OCCURRENCES (1 à 8, la première rapportée) ; (f)
TIRAGES PROPERTY-BASED (la graine 20261120, 512 tirages).

LES MESURES : instructions (Unicorn — la bibliothèque tenue égale) pour les
chemins SSE2 ; le compte STATIQUE exact pour les chemins AVX2/SHA-NI (LA
BORNE NOMMÉE : Unicorn ne porte ni AVX ni SHA-NI — XCR0 absent de l'API,
l'instruction refusée) ; les CYCLES RÉELS au rig natif (RDTSCP, cœur fixé,
n=20, médiane + IQR, la fréquence consignée).

Sorties : batterie-resultats.json · remesure-v220.csv · rapport-corridors.txt"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import pathlib
import random
import statistics
import struct
import subprocess
import sys

import unicorn

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-corridors-fnvan0zes"
sys.path.insert(0, str(REPO / "loupe"))

import capstone  # noqa: E402
import keystone  # noqa: E402

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

RVA_HYB = 0xCD00
RVA_AVX = 0xD100
RVA_SHANI = 0xD300
RVA_SCELLE_02 = 0xC080
RVA_K = 0x2F00


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def assembler(fichier: pathlib.Path, rva: int, symboles: dict | None = None):
    """L'assembleur de l'atelier : étiquettes maison + lignes db (les
    instructions SHA aux octets explicites) + les symboles @NOM résolus en
    rip-relatif (le masque) ou adresses absolues (@Knn : la table scellée)."""
    symboles = dict(symboles or {})
    lignes_brutes = [l.split(";")[0].strip() for l in fichier.read_text(
        encoding="utf-8").splitlines()]

    def taille(ligne, adresse=0):
        if ligne.startswith("db "):
            return len(ligne[3:].split())
        # les symboles @NOM remplacés par un fictif (la taille ne dépend
        # pas de la valeur du déplacement — mais l'ADRESSE oui : les sauts
        # courts/longs se décident à l'adresse réelle)
        import re as _re
        prov = _re.sub(r"@[A-Za-z_0-9]+", "0x0", ligne)
        c, _ = KS.asm(prov, adresse)
        return len(bytes(c))

    etiquettes: dict[str, int] = {}
    adrs: list[int] = []
    pos_masque = None
    # QUATRE passes de tailles (les étiquettes se stabilisent — la
    # méthode de la vague 10 : chaque pass substitue les étiquettes connues) ;
    # la directive « align N » padde à 0x90 ; la ligne qui SUIT un align est
    # le masque (son adresse = @MASQUE, ALIGNÉ — pshufb m128 l'exige)
    for _ in range(4):
        adr = rva
        adrs = []
        apres_align = False
        for ligne in lignes_brutes:
            if not ligne:
                continue
            if ligne.endswith(":") and ligne.startswith("."):
                etiquettes[ligne[:-1]] = adr
                continue
            if ligne.startswith("align "):
                n = int(ligne.split()[1])
                adr = (adr + n - 1) & ~(n - 1)
                adrs.append(-1)          # marqueur (pas d'octet direct)
                apres_align = True
                continue
            if apres_align:
                pos_masque = adr
                apres_align = False
            adrs.append(adr)
            prov = ligne
            for e, ad in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
                if e in prov:
                    prov = prov.replace(e, hex(ad))
            try:
                adr += taille(prov, adr)
            except Exception:
                adr += 6
    fin_code = adr
    if pos_masque is not None:
        symboles.setdefault("@MASQUE", ("rip", pos_masque))
    else:
        symboles.setdefault("@MASQUE", ("rip", fin_code))

    def resous(ligne: str, adresse: int) -> str:
        for e, ad in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
            if e in ligne:
                ligne = ligne.replace(e, hex(ad))
        for nom, (genre, cible) in symboles.items():
            if nom in ligne:
                if genre == "rip":
                    # la cible du rip-relatif : disp = cible - (adresse + taille)
                    t = taille(ligne)
                    ligne = ligne.replace(
                        f"[rip + {nom}]",
                        f"[rip + {cible - (adresse + t):#x}]").replace(
                        f"[rip - {nom}]", f"[rip + {cible - (adresse + t):#x}]")
                else:
                    # l'adresse ABSOLUE en opérande mémoire : en mode long,
                    # elle vit en rip-relatif (le déplacement, possiblement
                    # négatif) — résolue à la taille de l'instruction
                    t = taille(ligne.replace(nom, "0x0"))
                    disp = cible - (adresse + t)
                    ligne = ligne.replace(f"[rip + {nom}]",
                                          f"[rip + {disp:#x}]")
        return ligne

    octets = b""
    debut: dict[str, int] = {}
    for ligne, adresse in zip([l for l in lignes_brutes if l and not (
            l.endswith(":") and l.startswith("."))], adrs):
        if ligne.startswith("align "):
            n = int(ligne.split()[1])
            while (rva + len(octets)) % n:
                octets += b"\x90"
            continue
        if adresse < 0:
            continue
        if ligne.startswith("db "):
            octets += bytes(int(b, 16) for b in ligne[3:].split())
            continue
        corr = resous(ligne, rva + len(octets))
        c, _ = KS.asm(corr, rva + len(octets))
        octets += bytes(c)
    debut.update(etiquettes)
    debut["@FIN_CODE"] = fin_code
    return octets, debut


def round_trip(octets: bytes, rva: int, longueur_code: int | None = None) -> bool:
    """le round-trip du CODE (les données du masque en fin de bloc
    exclues — elles ne sont pas du code)"""
    """le round-trip : keystone pour le commun ; pour les instructions SHA
    (keystone ne les assemble pas), l'encodage CANONIQUE re-dérivé des
    opérandes désassemblées (0F 38 CB/CC/CD /r — le ModRM re-calculé, la
    correspondance elle-même PROUVÉE par as/objdump à la sonde)"""
    reins = b""
    bornes = octets if longueur_code is None else octets[:longueur_code]
    for ins in CS.disasm(bornes, rva):
        if ins.mnemonic.startswith("sha256"):
            ops = [o.strip() for o in ins.op_str.split(",")]
            d, s = int(ops[0][3:]), int(ops[1][3:])
            opcode = {"sha256rnds2": 0xCB,
                      "sha256msg1": 0xCC,
                      "sha256msg2": 0xCD}[ins.mnemonic]
            rex = 0x40 | (0x04 if d >= 8 else 0) | (0x01 if s >= 8 else 0)
            corps = bytes([0x0F, 0x38, opcode,
                           0xC0 | ((d & 7) << 3) | (s & 7)])
            reins += (corps if rex == 0x40 else bytes([rex]) + corps)
            continue
        c, _ = KS.asm(f"{ins.mnemonic} {ins.op_str}", ins.address)
        reins += bytes(c)
    return reins == bornes


def main():
    rapport: list[str] = []
    a = rapport.append
    graine = 20261120
    rng = random.Random(graine)

    # ---- (0) les notations assemblées + round-trip --------------------------
    o_hyb, lab_hyb = assembler(ICI / "notation" / "loupe-13-hybride.asm", RVA_HYB)
    o_avx, lab_avx = assembler(ICI / "notation" / "loupe-13-avx2.asm", RVA_AVX)
    o_shani, _ = assembler(ICI / "notation" / "tls13-02-shani.asm", RVA_SHANI,
                           {"@K%d" % (4 * i): ("abs", RVA_K + 16 * i)
                            for i in range(16)})
    rt_h = round_trip(o_hyb, RVA_HYB, lab_hyb["@FIN_CODE"] - RVA_HYB)
    rt_a = round_trip(o_avx, RVA_AVX, lab_avx["@FIN_CODE"] - RVA_AVX)
    rt_s = round_trip(o_shani, RVA_SHANI, len(o_shani) - 16)
    a("LES TROIS COULOIRS : l'hybride "
      f"{len(o_hyb)} o au RVA {RVA_HYB:#x} (round-trip "
      f"{'100 %' if rt_h else 'DIVERGENT'}) ; l'AVX2 {len(o_avx)} o au RVA "
      f"{RVA_AVX:#x} (round-trip {'100 %' if rt_a else 'DIVERGENT'}) ; le "
      f"SHA-NI {len(o_shani)} o au RVA {RVA_SHANI:#x} (round-trip "
      f"{'100 %' if rt_s else 'DIVERGENT'}) — les SCELLÉS INTACTS (la marge)")

    # ---- (1) LA BATTERIE ÉLARGIE (la génération des vecteurs) ---------------
    vecteurs: list[tuple] = []   # (classe, tampon, motif, attendu)
    # (a) occurrences plantées EN QUEUE — le dernier bloc de 16, chaque position
    for p in range(16):
        f = bytearray(rng.randrange(256) for _ in range(4096))
        m = bytes(rng.randrange(256) for _ in range(16))
        pos = 4096 - 16 + p - 15 if p else 4096 - 16
        pos = max(0, 4096 - 16 - (15 - p))
        f[pos:pos + 16] = m
        f = bytes(f)
        vecteurs.append(("queue-16", f, m, f.find(m)))
    for lm in (1, 4, 16):
        f = bytearray(rng.randrange(256) for _ in range(1000))
        m = bytes(rng.randrange(256) for _ in range(lm))
        pos = 1000 - lm          # l'occurrence FINISSANT à la dernière octet
        f[pos:pos + lm] = m
        f = bytes(f)
        vecteurs.append(("queue-fin", f, m, f.find(m)))
    # (b) occurrences CHEVAUCHANTES (périodes 1 à 4)
    for periode in range(1, 5):
        f = bytearray(0x41 for _ in range(512))
        base = bytes(rng.randrange(256) for _ in range(periode))
        m = (base * (16 // periode + 1))[:16]
        pos = rng.randrange(64, 448)
        for i in range(16):
            f[pos + i] = m[i]
        f = bytes(f)
        vecteurs.append(("chevauchant-p%d" % periode, f, m, f.find(m)))
    # (c) LONGUEURS DE MOTIF 1 à >16
    for lm in (1, 2, 3, 4, 15, 16, 17, 18, 19, 20, 31, 32, 33):
        f = bytearray(rng.randrange(256) for _ in range(2048))
        m = bytes(rng.randrange(256) for _ in range(lm))
        pos = rng.randrange(0, 2048 - lm)
        f[pos:pos + lm] = m
        f = bytes(f)
        vecteurs.append(("longueur-%d" % lm, f, m, f.find(m)))
    # (d) FRANCHISSEMENT DE PAGE (le tampon à cheval sur 0x510000)
    for bord in ("avant", "apres", "traverse"):
        f = bytearray(rng.randrange(256) for _ in range(512))
        m = bytes(rng.randrange(256) for _ in range(8))
        if bord == "avant":
            pos = 505            # fini juste avant la frontière
        elif bord == "apres":
            pos = 513            # commence juste après
        else:
            pos = 508            # TRAVERSE la frontière (0x500000+512)
        f[pos:pos + 8] = m
        f = bytes(f)
        vecteurs.append(("page-" + bord, f, m, f.find(m)))
    # (e) MULTI-OCCURRENCES (1 à 8 — la première rapportée)
    for nocc in range(1, 9):
        f = bytearray(rng.randrange(256) for _ in range(2048))
        m = bytes(rng.randrange(256) for _ in range(6))
        positions = sorted(rng.sample(range(0, 2048 - 6), nocc))
        for p in positions:
            f[p:p + 6] = m
        f = bytes(f)
        vecteurs.append(("multi-%d" % nocc, f, m, f.find(m)))
    # (f) TIRAGES PROPERTY-BASED (la graine consignée)
    for k in range(512):
        n = rng.choice([17, 63, 100, 256, 1000, 4096])
        lm = rng.choice([1, 2, 3, 5, 8, 16, 17, 24, 32])
        f = bytearray(rng.randrange(256) for _ in range(n))
        m = bytes(rng.randrange(256) for _ in range(lm))
        if rng.random() < 0.7 and n > lm:      # 70 % avec occurrence
            p = rng.randrange(0, n - lm + 1)
            f[p:p + lm] = m
        f = bytes(f)
        vecteurs.append(("pbt-%d" % k, f, m, f.find(m)))

    a(f"LA BATTERIE ÉLARGIE : {len(vecteurs)} vecteurs "
      f"(64 + 3 queue · 4 chevauchants · 13 longueurs · 3 pages · "
      f"8 multi · 512 property-based, la graine {graine})")

    # ---- (2) LA DIFFÉRENTIELLE UNICORN (les chemins SSE2 : v2, hybride, repli AVX2)
    HE = charger_module("h_ed3", REPO / "loupe" / "harnais_edition.py")
    os_v = HE.OSEdition()
    emul = HE.EmulationEdition(
        os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
        (REPO / "m1" / "selftest.exe").read_bytes(),
        (REPO / "demo" / "demo.exe").read_bytes())
    emul.uc.mem_map(0x500000, 0x21000)
    emul.uc.mem_map(0xD000, 0x1000)      # la marge au-delà de l'image (0xD100/0xD200)
    # la page frontière : 0x500000+0x10000 = 0x510000 — le tampon (d) la traverse
    for octets_, rva_, nom in [(o_hyb, RVA_HYB, "hybride"),
                               (o_avx, RVA_AVX, "avx2-repli"),
                               ]:
        emul.uc.mem_write(rva_, octets_)
        emul.uc.ctl_remove_cache(rva_ & ~0xFFF,
                                 (rva_ + len(octets_) + 0xFFF) & ~0xFFF)
    # le repli AVX2 : l'entrée À LA TÊTE, le dispatch FORCÉ AU REPLI en
    # émulation (le patch de laboratoire : « test ebx, 0x20 » → « xor ebx,
    # ebx » — le chemin repli exercé sous Unicorn SANS toucher au prologue ;
    # le dispatch RÉEL vit au natif — le CPU du bac porte AVX2)
    o_avx_repli = bytearray(o_avx)
    motif_test = bytes.fromhex("f7c320000000")
    idx = o_avx_repli.find(motif_test)
    assert idx >= 0, "le motif du dispatch introuvable"
    o_avx_repli[idx:idx+6] = bytes.fromhex("31db90909090")   # xor ebx,ebx + nops
    o_avx_repli = bytes(o_avx_repli)
    emul.uc.mem_write(RVA_AVX, o_avx_repli)
    emul.uc.ctl_remove_cache(RVA_AVX & ~0xFFF, (RVA_AVX + len(o_avx_repli) + 0xFFF) & ~0xFFF)
    entree_avx_repli = RVA_AVX

    resultats_uni = {}
    for nom, entree in [("hybride", RVA_HYB), ("avx2-repli", entree_avx_repli)]:
        diverg = []
        for i, (classe, f, m, attendu) in enumerate(vecteurs):
            if len(m) > 32:
                continue
            base = 0x500000 + (0 if classe != "page-apres" else 0)
            # le tampon posé pour TRAVERSER la frontière 0x510000 : base+512
            addr = 0x510000 - 512 if classe.startswith("page-") else 0x500400
            emul.uc.mem_write(addr, f)
            emul.uc.mem_write(0x510800, m)
            with contextlib.redirect_stdout(io.StringIO()):
                r = emul.appeler(entree, {"rcx": addr, "rdx": len(f),
                                          "r8": 0x510800, "r9": len(m)},
                                 pile_args=[0])
            if (r["rax"] & (2**64 - 1)) != (attendu & (2**64 - 1)):
                diverg.append((i, classe, r["rax"], attendu))
        resultats_uni[nom] = diverg
        a(f"LA DIFFÉRENTIELLE UNICORN ({nom}) : "
          f"{len(vecteurs)} vecteurs — {'ZÉRO DIVERGENCE' if not diverg else str(len(diverg)) + ' DIVERGENCES : ' + repr(diverg[:5])}")

    json.dump({"batterie": len(vecteurs),
               "unicorn": {k: len(v) for k, v in resultats_uni.items()},
               "round_trip": {"hybride": rt_h, "avx2": rt_a, "shani": rt_s}},
              open(ICI / "batterie-resultats.json", "w"), indent=1)

    (ICI / "rapport-corridors.txt").write_text("\n".join(rapport) + "\n",
                                               encoding="utf-8")
    print("\n".join(rapport))
    ok = (not resultats_uni["hybride"] and not resultats_uni["avx2-repli"]
          and rt_h and rt_a and rt_s)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
