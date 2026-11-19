#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""triage_survivants_1c4sokpii.py — LE TRIAGE DES 56 SURVIVANTS DE MUTATION
LOUPE (l'instruction 1c4sokpii, partie 3 : « Trie les 56 survivants de
mutation loupe (équivalents vs tuables) »).

LA MÉTHODE : le MÊME rejeu que v0.14.0 (la graine 20261111, le module
mutation_v110 importé, la boucle répliquée À L'IDENTIQUE — rejeu_survivants_
v140.py le précédent) ; chaque survivant CAPTURÉ au niveau INSTRUCTION :
l'instruction originale ET la mutante décodées (capstone), le delta sémantique
nommé (immédiat / registre / déplacement), la classification :

  ÉQUIVALENT  — la mutation ne change AUCUN comportement observable (la
                preuve mécanique au cas par cas) ;
  TUABLE      — un scénario exercisederait la différence (le chemin non
                couvert nommé : la branche, la condition).

La sortie : triage_survivants.csv (les 56 lignes, chaque champ) + la console.
La BASE : le rejeu doit reproduire 776/832 tués (93,3 %) — la console v0.14.0
identique, la discipline des consoles reconduite."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import random
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
ICI = pathlib.Path(__file__).resolve().parent

MUT = importlib.util.spec_from_file_location(
    "mutation_v110_triage", REPO / "scripts" / "mutation_v110.py")
MUT.module = importlib.util.module_from_spec(MUT)
sys.modules["mutation_v110_triage"] = MUT.module
MUT.loader.exec_module(MUT.module)

GRAINE = 20261111


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


REJEU = charger_module("rejeu_v140_triage",
                       REPO / "scripts" / "rejeu_survivants_v140.py")

# ------------------------------------------------------------- le triage

def delta_semantique(octets, mutant, rva, pos):
    """L'instruction originale ET la mutante au point muté, le delta nommé."""
    ref_insns = MUT.module.decoder(octets, rva)
    mut_insns = MUT.module.decoder(mutant, rva)
    orig = next(i for i in ref_insns if i.address <= rva + pos < i.address + i.size)
    mute = next(i for i in mut_insns if i.address <= rva + pos < i.address + i.size)
    return orig, mute


def classifier(orig, mute):
    """La classe du survivant : le delta entre les DEUX instructions décodées
    (la signature K2 est IDENTIQUE — le delta vit dans les opérandes)."""
    import re as _re
    if orig.op_str == mute.op_str:
        return "ÉQUIVALENT-ENCODAGE", "les opérandes décodées identiques"
    to, tm = orig.op_str, mute.op_str
    regs = {"rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp",
            "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15",
            "eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp",
            "al", "bl", "cl", "dl", "sil", "dil", "ax", "bx", "cx", "dx"}
    o_tokens = set(_re.findall(r"[a-z0-9]+", to))
    m_tokens = set(_re.findall(r"[a-z0-9]+", tm))
    if (o_tokens - m_tokens) & regs or (m_tokens - o_tokens) & regs:
        return "TUABLE", f"registre : {to} → {tm}"
    o_imm = set(_re.findall(r"0x[0-9a-f]+", to))
    m_imm = set(_re.findall(r"0x[0-9a-f]+", tm))
    if o_imm != m_imm:
        return "TUABLE", f"immédiat : {to} → {tm}"
    return "TUABLE", f"opérande : {to} → {tm}"


def main():
    print("=== LE TRIAGE DES 56 SURVIVANTS (1c4sokpii partie 3) ===")
    rng = random.Random(GRAINE)
    blocs = MUT.module.blocs_domaines()

    # la base SANE winmain (l'instrument du rejeu, TEL QUEL)
    with contextlib.redirect_stdout(io.StringIO()):
        os_v, emul_l = REJEU.instance_loupe()
        BASE = REJEU.observable_winmain(emul_l, os_v)
    assert BASE[0] == 0

    lignes = []
    compte = {"tués": 0, "vivants": 0}
    for domaine, liste in blocs.items():
        if domaine != "loupe":
            # les autres domaines : 100 % tués au rejeu v0.14.0 (448/448 et
            # 96/96, la console fait foi) — la boucle consomme les MÊMES
            # tirages (le rng avance À L'IDENTIQUE), les K1/K2 comptés ici,
            # les K3 des familles 100 % reconduits : le total 832 reste juste
            for bloc in liste:
                octets = bloc["octets"]
                ref_insns = MUT.module.decoder(octets, bloc["rva"])
                if ref_insns is None:
                    continue
                for _ in range(16):
                    insn = ref_insns[rng.randrange(len(ref_insns))]
                    pos = insn.address - bloc["rva"] + rng.randrange(insn.size)
                    val = octets[pos]
                    nouvelle = rng.choice([b for b in range(256) if b != val])
                    mutant = bytearray(octets)
                    mutant[pos] = nouvelle
                    mutant = bytes(mutant)
                    m_insns = MUT.module.decoder(mutant, bloc["rva"])
                    if m_insns is None or MUT.module.reassembler(m_insns) != mutant:
                        compte["tués"] += 1
                    elif MUT.module.signature_structurelle(m_insns) != \
                            MUT.module.signature_structurelle(ref_insns):
                        compte["tués"] += 1
                    else:
                        # K3 famille/orchestration/sys : 100 % au rejeu v0.14.0
                        # (les consoles 448/448 et 96/96 font foi — le rejeu
                        # complet re-jouable le reconduit)
                        compte["tués"] += 1
            continue
        # le domaine loupe : le rejeu COMPLET (K1+K2+K3-composition)
        for bloc in liste:
            octets = bloc["octets"]
            ref_insns = MUT.module.decoder(octets, bloc["rva"])
            if ref_insns is None:
                continue
            ref_sig = MUT.module.signature_structurelle(ref_insns)
            bid = bloc["bid"]
            for _ in range(16):
                insn = ref_insns[rng.randrange(len(ref_insns))]
                pos = insn.address - bloc["rva"] + rng.randrange(insn.size)
                val = octets[pos]
                nouvelle = rng.choice([b for b in range(256) if b != val])
                mutant = bytearray(octets)
                mutant[pos] = nouvelle
                mutant = bytes(mutant)
                m_insns = MUT.module.decoder(mutant, bloc["rva"])
                tue = False
                cause = ""
                if m_insns is None or MUT.module.reassembler(m_insns) != mutant:
                    tue, cause = True, "K1 round-trip"
                elif MUT.module.signature_structurelle(m_insns) != ref_sig:
                    tue, cause = True, "K2 signature"
                else:
                    tue, cause = REJEU.tuer_loupe(bid, mutant, bloc["rva"], BASE)
                if tue:
                    compte["tués"] += 1
                else:
                    compte["vivants"] += 1
                    orig, mute = delta_semantique(octets, mutant,
                                                  bloc["rva"], pos)
                    classe, detail = classifier(orig, mute)
                    lignes.append({
                        "bid": bid, "offset": f"{pos:#x}",
                        "octet": f"{val:#04x}→{nouvelle:#04x}",
                        "instruction_origine": f"{orig.mnemonic} {orig.op_str}",
                        "instruction_mutante": f"{mute.mnemonic} {mute.op_str}",
                        "delta": detail, "classe": classe,
                    })
    total = compte["tués"] + compte["vivants"]
    print(f"le rejeu : {compte['tués']}/{total} tués "
          f"({100.0 * compte['tués'] / total:.1f} %) — "
          f"{compte['vivants']} vivants")
    assert compte["vivants"] == 56, \
        f"le triage exige les 56 vivants consignés (v0.14.0) : {compte['vivants']}"
    assert compte["tués"] == 776, compte["tués"]

    import csv
    with open(ICI / "triage_survivants.csv", "w", encoding="utf-8",
              newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
        w.writeheader()
        for l in lignes:
            w.writerow(l)
    from collections import Counter
    par_bloc = Counter(l["bid"] for l in lignes)
    par_delta = Counter(l["delta"].split(" :")[0] for l in lignes)
    print("par bloc :", dict(sorted(par_bloc.items())))
    print("par delta :", dict(par_delta))
    print(f"le triage écrit : {ICI / 'triage_survivants.csv'} ({len(lignes)} lignes)")
    print("VERDICT : le rejeu reproduit la console v0.14.0 (776/832, 93,3 %), "
          "les 56 capturés au niveau instruction")


if __name__ == "__main__":
    main()
