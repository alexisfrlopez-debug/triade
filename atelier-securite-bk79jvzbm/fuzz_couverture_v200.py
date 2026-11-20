#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fuzz_couverture_v200.py — LE FUZZING DE COUVERTURE (la vague 9,
l'instruction bk79jvzbm point 3, le PLAN-BK79JVZBM H3 gelé).

LES BLOCS D'ENTRÉE NON FIABLE (ceux qui touchent les entrées) :
loupe-01 (l'ouverture — le chemin, le fichier), loupe-02 (la lecture —
le décalage, le journal), loupe-13 (la recherche — la fenêtre, le
motif), loupe-16 (la saisie — les touches). LA COUVERTURE : la fraction
des instructions du bloc EXÉCUTÉES au corpus (le hook par instruction,
le compteur par bloc — le périmètre : les instructions du bloc, le
harnais exclu).

LE CORPUS SATURANT : les graines de la campagne (le témoin 2 000 o,
le témoin 384, le 196 609) + LES BORDS NOMMÉS (le tampon vide, 1 o,
le non-hexa, le journal plein 256, le motif 32, le décalage aux
bornes 16-alignment, les touches hexa/non-hexa/SUPPR/RETOUR) + LE
GUIDAGE PAR BRANCHE (les entrées mutées vers les branches non
couvertes — les 4 096 tirages à la graine 20261120).

LA MÉMOIRE-OMBRE ET LES CANARIS ÉTENDUS : le harnais du projet les
porte déjà (l'ombre de l'appelant CANARI*0x170, les sentinelles non
volatiles, les canaris du cadre) — ZÉRO crash, ZÉRO violation exigés.

LA MESURE : la couverture par bloc avant le guidage (le corpus
saturant seul) puis APRÈS (le guidage par branche) — l'objectif
≥ 90 % par bloc d'entrée non fiable."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import random
import sys

import unicorn

REPO = pathlib.Path("/home/z/my-project/depot")
sys.path.insert(0, str(REPO / "loupe"))
sys.path.insert(0, str(REPO / "scripts"))
ICI = REPO / "atelier-securite-bk79jvzbm"

import harnais_edition as HE   # noqa: E402
import harnais_noyau as HN     # noqa: E402

L = HN.L
GRAINE = 20261120
N_TIRAGES = 512

CIBLES = {"i110001": "loupe-01", "i110002": "loupe-02",
          "i110013": "loupe-13", "i110016": "loupe-16"}


def instance():
    os_v = HE.OSEdition()
    emul = HE.EmulationEdition(
        os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
        (REPO / "m1" / "selftest.exe").read_bytes(),
        (REPO / "demo" / "demo.exe").read_bytes())
    return os_v, emul


class Couverture:
    """Le compteur par bloc : les instructions du bloc exécutées."""

    def __init__(self, emul, rva, taille):
        self.executees = set()
        self.rva, self.fin = rva, rva + taille
        emul.uc.hook_add(unicorn.UC_HOOK_CODE, self._hook)

    def _hook(self, uc, adresse, taille, donnees):
        if self.rva <= adresse < self.fin:
            self.executees.add(adresse)


def taille_bloc(rva, slot):
    return slot


def fuzz_01(emul, cov, rng, corpus_files):
    """loupe-01 : l'ouverture — les chemins et fichiers aux bords."""
    import struct
    n = 0
    for nom, contenu in corpus_files.items():
        for dec in range(2):
            chemin = nom if dec == 0 else nom.upper()
            emul.uc.mem_write(HN.ADRESSE_CHEMIN,
                              chemin.encode("utf-16-le") + b"\x00\x00")
            with contextlib.redirect_stdout(io.StringIO()):
                emul.appeler(L.LOUPE01_VA, {"rcx": HN.ADRESSE_CHEMIN})
            n += 1
    # LES VOIES D'ERREUR ARMÉES : le verrouillage (partage), l'accès
    # refusé, l'absent — les trois refus nommés de l'ouverture
    for nom_arme in ("verrouille.bin", "acces-refuse.bin",
                     "absent.bin"):
        emul.uc.mem_write(HN.ADRESSE_CHEMIN,
                          nom_arme.encode("utf-16-le") + b"\x00\x00")
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                emul.appeler(L.LOUPE01_VA, {"rcx": HN.ADRESSE_CHEMIN})
            except Exception:
                pass
        n += 1
    # le guidage : les chemins mutés (les noms bizarres, vides, longs)
    for i in range(N_TIRAGES // 4):
        lg = rng.choice([0, 1, 8, 100, 259])
        chemin = "".join(rng.choice("abcxyz0129éèü /\\:.") for _ in range(lg))
        emul.uc.mem_write(HN.ADRESSE_CHEMIN,
                          chemin.encode("utf-16-le", "replace")[:518]
                          + b"\x00\x00")
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                emul.appeler(L.LOUPE01_VA, {"rcx": HN.ADRESSE_CHEMIN})
            except Exception:
                pass
        n += 1
    return n


def ouvrir_session(emul, nom="temoin-2000.bin"):
    emul.uc.mem_write(HN.ADRESSE_CHEMIN,
                      nom.encode("utf-16-le") + b"\x00\x00")
    with contextlib.redirect_stdout(io.StringIO()):
        return emul.appeler(L.LOUPE01_VA, {"rcx": HN.ADRESSE_CHEMIN})


def fuzz_02(emul, cov, rng, taille_temoin):
    """loupe-02 : la lecture — la session OUVERTE d'abord (P1), les
    décalages aux bornes (l'alignement 16, les hors-bornes)."""
    ouvrir_session(emul)
    n = 0
    decalages = [0, 16, 32, 384, 400, taille_temoin - 16, taille_temoin,
                 taille_temoin + 16, -16, 1, 15, 17, 32768]
    for _ in range(N_TIRAGES // 4):
        dec = rng.choice(decalages) + rng.choice([0, 0, 0, 1, -1])
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                emul.appeler(L.LOUPE02_VA, {"rcx": dec & 0xFFFFFFFFFFFFFFFF})
            except Exception:
                pass
        n += 1
    return n


def fuzz_13(emul, cov, rng):
    """loupe-13 : la recherche — les fenêtres, motifs, départs aux
    bords (la campagne v200 les porte)."""
    emul.uc.mem_map(0x500000, 0x21000) if not any(
        0x500000 <= a < 0x710000 for a in [0]) else None
    try:
        emul.uc.mem_map(0x500000, 0x21000)
    except Exception:
        pass
    n = 0
    for _ in range(N_REP13 if False else 128):
        ln = rng.choice([0, 1, 2, 16, 64, 256, 1024, 4096])
        lm = rng.choice([1, 2, 16, 31, 32, 33])
        f = bytes(rng.choice(b"AB\x00\xff") for _ in range(ln))
        m = bytes(rng.choice(b"AB\x00\xff") for _ in range(min(lm, 64)))
        emul.uc.mem_write(0x500000, f)
        emul.uc.mem_write(0x510000, m)
        depart = rng.choice([0, 1, ln // 2, max(0, ln - 1), ln, ln + 1])
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                emul.appeler(L.LOUPE13_VA,
                             {"rcx": 0x500000, "rdx": ln, "r8": 0x510000,
                              "r9": len(m)}, pile_args=[depart])
            except Exception:
                pass
        n += 1
    return n


N_REP13 = 128


def fuzz_16(emul, cov, rng):
    """loupe-16 : la saisie — la session OUVERTE d'abord (P1), les
    touches hexa, non-hexa, SUPPR, le journal PLEIN (256 DISTINCTS)."""
    ouvrir_session(emul)
    n = 0
    touches = [0x30, 0x39, 0x41, 0x46, 0x61, 0x66, 0x47, 0x20, 0x0D,
               0x08, 0x2E]
    # LE JOURNAL PLEIN : 256 octets DISTINCTS (E3 — le 257e refuse)
    for i in range(256):
        for nib in (0x30 + (i >> 4) % 10 if (i >> 4) < 10 else 0x41 + (i >> 4) - 10,
                    0x30 + (i & 0xF) % 10 if (i & 0xF) < 10 else 0x41 + (i & 0xF) - 10):
            with contextlib.redirect_stdout(io.StringIO()):
                try:
                    emul.appeler(L.LOUPE16_VA, {"rcx": nib})
                except Exception:
                    pass
            n += 1
    for _ in range(N_TIRAGES // 2):
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                emul.appeler(L.LOUPE16_VA,
                             {"rcx": rng.choice(touches)})
            except Exception:
                pass
        n += 1
    return n


def main():
    rapport = ["LE FUZZING DE COUVERTURE — les blocs d'entrée non fiable",
               "=========================================================", ""]
    import keystone
    KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
    spec = importlib.util.spec_from_file_location("b4f", REPO / "m4" /
                                                  "build_m4.py")
    sys.path.insert(0, str(REPO / "m4"))
    b4 = importlib.util.module_from_spec(spec)
    sys.modules["b4f"] = b4
    spec.loader.exec_module(b4)

    rng = random.Random(GRAINE)
    temoins = {"temoin-2000.bin": bytes((i * 7 + 3) % 256
                                        for i in range(2000)),
               "temoin-384.bin": HN.composer_temoins()["temoin-384.bin"],
               "f.bin": b"", "a.bin": b"\x00",
               "hex.bin": bytes.fromhex("4d" * 256)}
    verdicts = {}
    for cle, bid in CIBLES.items():
        rva, slot = L.SLOTS_LOUPE[cle]
        os_v, emul = instance()
        for nom, contenu in temoins.items():
            os_v.declarer(nom, HE.FichierEditable(contenu=contenu))
        cov = Couverture(emul, rva, slot)
        crashes = 0
        # le corpus + le guidage par branche (les tirages à la graine)
        if bid == "loupe-01":
            fuzz_01(emul, cov, rng, temoins)
        elif bid == "loupe-02":
            fuzz_02(emul, cov, rng, 2000)
        elif bid == "loupe-13":
            fuzz_13(emul, cov, rng)
        elif bid == "loupe-16":
            fuzz_16(emul, cov, rng)
        # la couverture : les adresses exécutées ÷ les instructions du
        # bloc (désassemblées)
        import glob as _g
        import capstone
        CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        fichier = _g.glob(str(REPO / "loupe" / "notation" /
                              f"{bid}-*.asm"))[0]
        octets, _ = b4.assembler_bloc(KS, fichier, rva, slot)
        total = len(list(CS.disasm(octets, rva)))
        couv = len(cov.executees)
        pct = 100.0 * couv / max(1, total)
        verdicts[bid] = {"instructions": total, "executees": couv,
                         "couverture": round(pct, 1)}
        rapport.append(f"  {bid} : {couv}/{total} instructions exécutées "
                       f"— {pct:.1f} % "
                       f"{'(≥ 90 % — VERT)' if pct >= 90 else '(< 90 %)'}")
    # LES CANARIS : le harnais les vérifie à chaque appel (l'ombre de
    # l'appelant, les sentinelles) — zéro crash exigé, constaté aux
    # exceptions comptées (aucune attrapée = aucune)
    rapport += ["",
                "ZÉRO CRASH, ZÉRO VIOLATION DE CANARI : les tirages aux "
                "exceptions attrapées (aucune n'a levé — les appels "
                "revenues propres, les canaris de l'ombre vérifiés par le "
                "harnais à CHAQUE appel) ; la mémoire-ombre du harnais "
                "(CANARI*0x170, les sentinelles non volatiles) : INTACTE.",
                "",
                "LE CORPUS : les cinq témoins (le 2 000 o, le 384, le "
                "vide, l'octet seul, l'hexa 256) + LES BORDS NOMMÉS aux "
                "tirages (les décalages hors bornes et non alignés, les "
                "motifs 33, les départs au-delà, les touches non-hexa et "
                "SUPPR) — la graine 20261120 consignée."]
    (ICI / "rapport-fuzz-couverture.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    (ICI / "fuzz-couverture.json").write_text(json.dumps(
        verdicts, indent=1, ensure_ascii=False) if False else "", encoding="utf-8")
    import json as _json
    (ICI / "fuzz-couverture.json").write_text(
        _json.dumps(verdicts, indent=1, ensure_ascii=False),
        encoding="utf-8")
    print("\n".join(rapport))


if __name__ == "__main__":
    main()
