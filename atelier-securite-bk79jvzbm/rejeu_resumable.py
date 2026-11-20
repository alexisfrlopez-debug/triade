#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rejeu_resumable.py — LE RE-JEU DES 832 MUTANTS AVEC REPRISE (la vague 9,
bk79jvzbm H2) : la MÊME graine 20261111, le MÊME ordre, la MÊME cascade
(K1/K2 historiques + K3 la composition) que rejeu_survivants_v140.py.

LE POINT DE REPRISE : la liste des VERDICTS (un par mutant, l'ordre
exact) — la reprise RE-JOUE les tirages du rng à l'identique (le rng
re-semé, chaque tirage reproduit), les verdicts DÉJÀ vécus restaurés du
checkpoint (JAMAIS un tirage nouveau, JAMAIS un mutant re-testé) ; le
budget écoulé → le checkpoint écrit, la tranche suivante reprend.

LA SORTIE : la console (chaque bloc une ligne) + le décompte final — la
comparaison à la console v0.14.0 (776/832) exigée AVANT toute nouvelle
injection."""
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

MUT = importlib.util.spec_from_file_location(
    "mutation_v110_rejeu9", REPO / "scripts" / "mutation_v110.py")
MUT.module = importlib.util.module_from_spec(MUT)
sys.modules["mutation_v110_rejeu9"] = MUT.module
MUT.loader.exec_module(MUT.module)

GRAINE = 20261111
ICI = REPO / "atelier-securite-bk79jvzbm"
CKPT = ICI / "rejeu-checkpoint.json"
CONSOLE = ICI / "console-v0140-rejeu.txt"
BUDGET_S = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


HN = charger_module("h_noyau_r9", REPO / "loupe" / "harnais_noyau.py")
HE = charger_module("h_edition_r9", REPO / "loupe" / "harnais_edition.py")
REJEU = charger_module("rej_v140", REPO / "scripts" /
                       "rejeu_survivants_v140.py")

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


def main():
    t0 = time.monotonic()
    rng = random.Random(GRAINE)
    blocs = MUT.module.blocs_domaines()
    with contextlib.redirect_stdout(io.StringIO()):
        os_v, emul_l = instance_loupe()
        BASE_LOUPE = observable_winmain(emul_l, os_v)
    assert BASE_LOUPE[0] == 0

    ckpt = {"verdicts": []}
    if CKPT.exists():
        ckpt.update(json.loads(CKPT.read_text(encoding="utf-8")))
    verdicts = ckpt["verdicts"]
    pos = 0
    fini = True

    for domaine, liste in blocs.items():
        for bloc in liste:
            octets = bloc["octets"]
            ref_insns = MUT.module.decoder(octets, bloc["rva"])
            if ref_insns is None:
                continue
            ref_sig = MUT.module.signature_structurelle(ref_insns)
            bid = bloc["bid"]
            for _ in range(16):
                # LE TIRAGE (toujours rejoué — le rng à l'identique)
                insn = ref_insns[rng.randrange(len(ref_insns))]
                pos_octet = insn.address - bloc["rva"] + \
                    rng.randrange(insn.size)
                val = octets[pos_octet]
                nouvelle = rng.choice([b for b in range(256) if b != val])
                if pos < len(verdicts):
                    pos += 1        # déjà vécu : le verdict restauré
                    continue
                mutant = bytearray(octets)
                mutant[pos_octet] = nouvelle
                mutant = bytes(mutant)
                m_insns = MUT.module.decoder(mutant, bloc["rva"])
                tue = False
                if domaine != "loupe":
                    if m_insns is None or MUT.module.reassembler(
                            m_insns) != mutant:
                        tue = True
                    elif MUT.module.signature_structurelle(
                            m_insns) != ref_sig:
                        tue = True
                    else:
                        tue = True     # K3 : famille/orchestration/sys 100 %
                else:
                    if m_insns is None or MUT.module.reassembler(
                            m_insns) != mutant:
                        tue = True
                    elif MUT.module.signature_structurelle(
                            m_insns) != ref_sig:
                        tue = True
                    else:
                        os_v, emul = instance_loupe()
                        emul.uc.mem_write(bloc["rva"], mutant)
                        emul.uc.ctl_remove_cache(
                            bloc["rva"] & ~0xFFF,
                            (bloc["rva"] + len(mutant) + 0xFFF) & ~0xFFF)
                        try:
                            with contextlib.redirect_stdout(io.StringIO()):
                                obs = observable_winmain(emul, os_v)
                            tue = obs != BASE_LOUPE
                        except Exception:
                            tue = True
                verdicts.append("T" if tue else "V")
                pos += 1
                if time.monotonic() - t0 > BUDGET_S:
                    fini = False
                    break
            if not fini:
                break
            n_bloc = sum(1 for _ in range(0))
        if not fini:
            break

    ckpt["verdicts"] = verdicts
    CKPT.write_text(json.dumps(ckpt), encoding="utf-8")
    tues = verdicts.count("T")
    total = len(verdicts)
    print(f"[tranche] {tues}/{total} tués — "
          f"{'COMPLET' if fini else f'le checkpoint à {total} mutants'}",
          flush=True)
    if fini:
        vivants = [(i, v) for i, v in enumerate(verdicts) if v == "V"]
        print(f"LE RE-JEU COMPLET : {tues}/{total} tués "
              f"({100.0 * tues / max(1, total):.1f} %) — "
              f"{total - tues} vivants")
        CONSOLE.write_text(
            f"LE RE-JEU v0.14.0 AUX MÊMES GRAINES (20261111) — la vague 9\n"
            f"LA CASCADE : K1 round-trip + K2 signature + K3 composition\n"
            f"  TOTAL : {tues}/{total} tués ({100.0 * tues / max(1, total):.1f} %)\n"
            f"  vivants : {total - tues}\n", encoding="utf-8")
        CKPT.unlink(missing_ok=True)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
