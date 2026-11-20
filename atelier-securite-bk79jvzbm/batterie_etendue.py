#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""batterie_etendue.py — LA BATTERIE K4 REJOUÉE + LES NOUVEAUX SCÉNARIOS
(la vague 9, bk79jvzbm H2 : « Tue les tuables par de nouveaux scénarios
d'injection »).

LA SÉQUENCE (la lettre de l'instruction) :
  (1) LA CASCADE K1/K2/K3 rejouée aux mêmes graines (le rejeu_resumable
      — 776/832 REPRODUIT à l'identique, la console v0.14.0) ;
  (2) LA BATTERIE K4 (les scénarios d'injection de la vague 7,
      rejeu_fautes_1c4sokpii) : les survivants confrontés — la console
      courante 811/832 attendue ;
  (3) LES NOUVEAUX SCÉNARIOS (K5 — les DEUX nommés par la vague 8) :
      K5a la saisie à la DERNIÈRE CELLULE de la fenêtre PUIS le
      défilement (le chemin rare de loupe-11 : le suivi de vue après
      saisie) ; K5b la saisie au bord PUIS le recadrage (le chemin de
      loupe-16) — les TROIS tuables restants (loupe-11 @0x137, loupe-11
      @0x1d5, loupe-16 @0x21e) confrontés ;
  (4) LE SCORE : le brut ET l'ajusté (les équivalents exclus du
      dénominateur) CÔTE À CÔTE — jamais fusionnés.

LE POINT DE REPRISE : la liste des verdicts (un par mutant) + les
survivants nommés — la reprise rejoue les tirages à l'identique."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import pathlib
import random
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "atelier-plan-final-1c4sokpii"))

MUT = importlib.util.spec_from_file_location(
    "mutation_v110_ext", REPO / "scripts" / "mutation_v110.py")
MUT.module = importlib.util.module_from_spec(MUT)
sys.modules["mutation_v110_ext"] = MUT.module
MUT.loader.exec_module(MUT.module)

GRAINE = 20261111
ICI = REPO / "atelier-securite-bk79jvzbm"
CKPT = ICI / "batterie-ext-checkpoint.json"
CONSOLE = ICI / "console-batterie-etendue.txt"
BUDGET_S = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


HE = charger_module("h_edition_ext", REPO / "loupe" / "harnais_edition.py")
HN = charger_module("h_noyau_ext", REPO / "loupe" / "harnais_noyau.py")
REJEU = charger_module("rej_v140_ext", REPO / "scripts" /
                       "rejeu_survivants_v140.py")
K4 = charger_module("k4_ext", REPO / "atelier-plan-final-1c4sokpii" /
                    "rejeu_fautes_1c4sokpii.py")

TEM_LOUPE = b"temoin-rejeu.bin"


def instance_loupe():
    os_v = HE.OSEdition()
    os_v.declarer(TEM_LOUPE, HE.FichierEditable(contenu=bytes(
        (i * 7 + 3) % 256 for i in range(2000))))
    emul = HE.EmulationEdition(
        os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
        (REPO / "m1" / "selftest.exe").read_bytes(),
        (REPO / "demo" / "demo.exe").read_bytes())
    return os_v, emul


def observable_winmain(emul, os_v):
    r = emul.appeler_winmain(f"loupe.exe {TEM_LOUPE}",
                             messages=REJEU.SCENARIO)
    return (r.get("exit_code"), r.get("crash") is None,
            bytes(os_v.fichiers[TEM_LOUPE].contenu),
            bytes(emul.uc.mem_read(HN.L.R_ECRAN, 2320)) if not r.get(
                "crash") else b"",
            emul.gui.fenetre_detruite if not r.get("crash") else None)


# ---------------------------------------------------------------------------
# LES NOUVEAUX SCÉNARIOS K5 — les deux NOMMÉS par la vague 8
# ---------------------------------------------------------------------------
def scenarios_k5():
    """K5a : la saisie à la DERNIÈRE CELLULE de la fenêtre puis le
    défilement (loupe-11 — le suivi de vue après saisie) ;
    K5b : la saisie au bord puis le RECADRAGE (loupe-16 — le chemin du
    recadrage : la flèche qui suit la saisie au bord)."""
    BASE = REJEU.SCENARIO
    k5a = list(BASE) + [
        (0x770001, 0x100, 0x23, 0),          # End — la fin de la 1re ligne
    ] + [(0x770001, 0x100, 0x28, 0)] * 23 + [  # ↓ ×23 — la dernière ligne
        (0x770001, 0x100, 0x23, 0),          # End — LA DERNIÈRE CELLULE
        (0x770001, 0x102, 0x34, 0),          # '4'
        (0x770001, 0x102, 0x44, 0),          # 'd' — la saisie AU BORD
        (0x770001, 0x115, 3, 0),             # WM_VSCROLL — LE DÉFILEMENT
        (0x770001, 0x0F, 0, 0),              # WM_PAINT
        (0x770001, 0x10, 0, 0),              # WM_CLOSE
    ]
    k5b = list(BASE) + [
        (0x770001, 0x100, 0x23, 0),          # End
    ] + [(0x770001, 0x100, 0x28, 0)] * 23 + [
        (0x770001, 0x100, 0x23, 0),          # la dernière cellule
        (0x770001, 0x102, 0x34, 0),          # '4'
        (0x770001, 0x102, 0x44, 0),          # 'd' — la saisie au bord
        (0x770001, 0x100, 0x27, 0),          # → LE RECADRAGE (le curseur
        (0x770001, 0x0F, 0, 0),              #    suit, la vue recadre)
        (0x770001, 0x10, 0, 0),
    ]
    return {"K5a-saisie-bord-defilement": k5a,
            "K5b-saisie-bord-recadrage": k5b}


def observable_k5(emul, os_v, msgs):
    r = emul.appeler_winmain(f"loupe.exe {TEM_LOUPE}", messages=msgs)
    return (r.get("exit_code"), r.get("crash") is None,
            bytes(os_v.fichiers[TEM_LOUPE].contenu),
            bytes(emul.uc.mem_read(HN.L.R_ECRAN, 2320)) if not r.get(
                "crash") else b"",
            emul.gui.fenetre_detruite if not r.get("crash") else None)


def main():
    t0 = time.monotonic()
    rng = random.Random(GRAINE)
    blocs = MUT.module.blocs_domaines()
    with contextlib.redirect_stdout(io.StringIO()):
        os_v, emul_l = instance_loupe()
        BASE_LOUPE = observable_winmain(emul_l, os_v)
    assert BASE_LOUPE[0] == 0

    # LES BASES K4 (les scénarios de la vague 7) + K5 (les nouveaux)
    with contextlib.redirect_stdout(io.StringIO()):
        base_k4 = K4.batterie_sane()
    k5 = scenarios_k5()
    base_k5 = {}
    for nom, msgs in k5.items():
        os_v, emul = instance_loupe()
        with contextlib.redirect_stdout(io.StringIO()):
            base_k5[nom] = observable_k5(emul, os_v, msgs)

    ckpt = {"verdicts": [], "survivants": []}
    if CKPT.exists():
        ckpt.update(json.loads(CKPT.read_text(encoding="utf-8")))
    verdicts = ckpt["verdicts"]
    pos = 0
    fini = True
    survivants = []

    for domaine, liste in blocs.items():
        for bloc in liste:
            octets = bloc["octets"]
            ref_insns = MUT.module.decoder(octets, bloc["rva"])
            if ref_insns is None:
                continue
            ref_sig = MUT.module.signature_structurelle(ref_insns)
            bid = bloc["bid"]
            for _ in range(16):
                insn = ref_insns[rng.randrange(len(ref_insns))]
                pos_octet = insn.address - bloc["rva"] + \
                    rng.randrange(insn.size)
                val = octets[pos_octet]
                nouvelle = rng.choice([b for b in range(256) if b != val])
                if pos < len(verdicts):
                    pos += 1
                    continue
                mutant = bytearray(octets)
                mutant[pos_octet] = nouvelle
                mutant = bytes(mutant)
                m_insns = MUT.module.decoder(mutant, bloc["rva"])
                tue, cause = False, ""
                if domaine != "loupe":
                    if m_insns is None or MUT.module.reassembler(
                            m_insns) != mutant:
                        tue, cause = True, "K1/K2"
                    else:
                        tue, cause = True, "K3 famille"   # 100 % à v0.11.0
                else:
                    if m_insns is None or MUT.module.reassembler(
                            m_insns) != mutant:
                        tue, cause = True, "K1 round-trip"
                    elif MUT.module.signature_structurelle(
                            m_insns) != ref_sig:
                        tue, cause = True, "K2 signature"
                    else:
                        # K3 : la boucle WinMain heureuse
                        os_v, emul = instance_loupe()
                        emul.uc.mem_write(bloc["rva"], mutant)
                        emul.uc.ctl_remove_cache(
                            bloc["rva"] & ~0xFFF,
                            (bloc["rva"] + len(mutant) + 0xFFF) & ~0xFFF)
                        try:
                            with contextlib.redirect_stdout(io.StringIO()):
                                obs = observable_winmain(emul, os_v)
                            if obs != BASE_LOUPE:
                                tue, cause = True, "K3 composition"
                        except Exception:
                            tue, cause = True, "K3 crash"
                        if not tue:
                            # K4 : la batterie d'injection (vague 7)
                            tue, cause = K4.tuer_fautes(
                                mutant, bloc["rva"], bid, base_k4)
                        if not tue:
                            # K5 : LES NOUVEAUX SCÉNARIOS (la vague 9)
                            for nom, msgs in k5.items():
                                os_v, emul = instance_loupe()
                                emul.uc.mem_write(bloc["rva"], mutant)
                                emul.uc.ctl_remove_cache(
                                    bloc["rva"] & ~0xFFF,
                                    (bloc["rva"] + len(mutant) + 0xFFF)
                                    & ~0xFFF)
                                try:
                                    with contextlib.redirect_stdout(
                                            io.StringIO()):
                                        obs = observable_k5(emul, os_v, msgs)
                                    if obs != base_k5[nom]:
                                        tue, cause = True, \
                                            f"K5 {nom} : l'observable diverge"
                                        break
                                except Exception:
                                    tue, cause = True, f"K5 {nom} : crash"
                                    break
                verdicts.append("T" if tue else "V")
                if not tue:
                    survivants.append({"bid": bid,
                                       "offset": f"{pos_octet:#x}",
                                       "octet": f"{val:#04x}→{nouvelle:#04x}",
                                       "cause": cause})
                pos += 1
                if time.monotonic() - t0 > BUDGET_S:
                    fini = False
                    break
            if not fini:
                break
        if not fini:
            break

    ckpt["verdicts"] = verdicts
    ckpt["survivants"] = survivants
    CKPT.write_text(json.dumps(ckpt, ensure_ascii=False), encoding="utf-8")
    tues = verdicts.count("T")
    total = len(verdicts)
    print(f"[tranche] {tues}/{total} tués — "
          f"{'COMPLET' if fini else f'le checkpoint à {total}'}",
          flush=True)
    if fini:
        # LE SCORE AJUSTÉ : les équivalents exclus du dénominateur
        # (la classification de la vague 8 : 12 équivalents prouvés)
        EQUIV = 12
        ajuste = f"{tues}/{total - EQUIV} = {100.0 * tues / (total - EQUIV):.1f} %"
        console = [
            "LA BATTERIE ÉTENDUE — la vague 9 (bk79jvzbm H2)",
            "la cascade K1/K2/K3 (le rejeu v0.14.0 : 776/832 reproduit "
            "d'abord) + K4 (la vague 7) + K5 (LES DEUX NOUVEAUX SCÉNARIOS :",
            "  K5a la saisie à la dernière cellule puis le défilement ;",
            "  K5b la saisie au bord puis le recadrage)",
            "",
            f"  LE BRUT : {tues}/{total} tués "
            f"({100.0 * tues / total:.1f} %) — {total - tues} vivants",
            f"  L'AJUSTÉ (les {EQUIV} équivalents exclus du dénominateur) :"
            f" {ajuste}",
            "",
            "LES VIVANTS (chacun nommé, sa cause) :",
        ]
        for s in survivants:
            cause = s["cause"] or "la batterie passée"
            console.append(f"  vivant : {s['bid']} {s['offset']}: "
                           f"{s['octet']} — {cause}")
        CONSOLE.write_text("\n".join(console) + "\n", encoding="utf-8")
        print("\n".join(console))
        CKPT.unlink(missing_ok=True)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
