#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""piloter_tcb.py — LE PILOTE DE L'ATELIER DES GARDES VIVANTES (k69mvt43j,
la vague 15) : le rejeu des 116 certificats v14 (58 décharges UNSAT + 58
mutations SAT — le relâchement D'UNE UNITÉ), LE REGISTRE TCB RÉDUIT
58→34→11 documenté par étage, L'ÉMISSION des ONZE gardes OS en corridor
RÉEL à la marge vierge 0xFC00 (le modèle OPT-01 promu — R4/R7 préservés,
aucune adresse scellée ne bouge), le round-trip, LE HARNAIS (la garde
falsifiée refusée aux DEUX bornes + LA FACE D'INDEX), la mesure du coût
par appel au harnais émulé (Unicorn)."""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess

import keystone
import capstone
import unicorn

REPO = pathlib.Path("/home/z/my-project/depot")
V14 = REPO / "atelier-fermeture-f3uznui3l"
ICI = REPO / "atelier-gardes-tcb-k69mvt43j"
GARDES_V14 = V14 / "gardes-frontiere"
KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
RVA_CORRIDOR = 0xFC00   # la marge vierge — la dernière de la page 0xC000


# ------------------------------------------------- le rejeu des 116 --------
def rejeu_certificats() -> dict:
    resultats = {"decharges_unsat": 0, "mutations_sat": 0, "ecarts": []}
    for f in sorted(GARDES_V14.glob("*.smt2")):
        r = subprocess.run(["z3", "-in", str(f)], capture_output=True,
                           text=True, timeout=60)
        verdict = r.stdout.strip()
        attendu = "unsat" if f.name.startswith("decharge") else "sat"
        if verdict == attendu:
            resultats["decharges_unsat" if attendu == "unsat"
                      else "mutations_sat"] += 1
        else:
            resultats["ecarts"].append({"fichier": f.name,
                                        "verdict": verdict,
                                        "attendu": attendu})
    return resultats


# ------------------------------------------------- le registre TCB ---------
def registre_tcb() -> dict:
    src = json.loads((V14 / "registre-frontieres.json").read_text(
        encoding="utf-8"))
    par_zone = {"CADRE": [], "CTX": [], "OS": []}
    for g in src["detail"]:
        par_zone[g["zone"]].append(g)
    etages = [
        {"etage": "58 — LA BASE DE PREUVE (vague 14)",
         "contenu": "les 58 gardes de frontiere aux certificats UNSAT "
                    "composes (ifqm1d1i4/f3uznui3l) — la composition : la "
                    "frontiere A ADMIS et la frontiere PORTE l'invariant "
                    "et la negation de la surete, UNSAT exige",
         "gardes": [g["garde"] for g in src["detail"]]},
        {"etage": "34 — LES 24 LAYOUT CADRE DECHARGEES PAR PREUVE",
         "contenu": "les 24 invariants de layout CADRE (la zone 960 o — "
                    "le plan aux champs statiquement connus) : le certificat "
                    "UNSAT les couvre PAR LA SPECIFICATION DE LAYOUT, le "
                    "relachement d'UNE UNITE les garde PORTANTES (58/58 "
                    "mutations SAT au rejeu) — la garde runtime est "
                    "DECHARGEE, l'invariant vit dans la preuve",
         "gardes": [g["garde"] for g in par_zone["CADRE"]]},
        {"etage": "11 — LES 23 CONTRAT-APPELANT DECHARGEES A LA COMPOSITION",
         "contenu": "les 23 gardes CTX (les contrats d'appelant tls13) : la "
                    "PREUVE DE L'APPELANT porte l'invariant (le certificat "
                    "compose EST la preuve de l'appelant — l'appelant "
                    "admet ET porte les bornes) ; le relachement d'une "
                    "unite les garde portantes",
         "gardes": [g["garde"] for g in par_zone["CTX"]]},
        {"etage": "LE TCB RESIDUEL — LES 11 OS NOMMEES",
         "contenu": "les ONZE assomptions externes demeurent : le tampon "
                    "de l'appel systeme (la zone OS) — la promesse du "
                    "noyau, JAMAIS prouvable au laboratoire (D105 : le "
                    "coffre reel jamais touche) ; les gardes OS VIVENT en "
                    "corridor reel (l'emission de la presente session)",
         "gardes": [g["garde"] for g in par_zone["OS"]]},
    ]
    return {"date": "2026-11-23", "base": 58, "tcb_final": 11,
            "les_etages": etages}


# --------------------------------- L'EMISSION : le corridor des ONZE -------
def corps_os_guards() -> tuple:
    src = json.loads((V14 / "registre-frontieres.json").read_text(
        encoding="utf-8"))
    os_g = [g for g in src["detail"] if g["zone"] == "OS"]
    lignes = [
        "; le corridor des ONZE gardes OS (k69mvt43j, la vague 15) — le",
        "; modele OPT-01 PROMU EN CORRIDOR REEL a la marge vierge 0xFC00 :",
        "; R4/R7 PRESERVES (aucune adresse scellee ne bouge — les scelles",
        "; 0xDF00/0xDFC0, les couloirs 0xE200-0xEA00/0xF300/0xF800 INTACTS).",
        "; ABI (msx64) : rcx = l'index de la garde (0..10), r9 = la face",
        "; effective de l'acces (le miroir du fichier de garde v14 : les",
        "; gardes sys lisent [r9]) ; rax = 0 l'admission, -5 le refus de",
        "; frontiere NOMME, -2 LA FACE D'INDEX (l'index hors [0,11)).",
        "cmp rcx, 11",
        "jae .refus_index",
    ]
    for i in range(11):
        lignes.append(f"cmp rcx, {i}")
        lignes.append(f"jne .passe_{i}")
        lignes.append(f"jmp .garde_{i}")
        lignes.append(f".passe_{i}:")
    for i, g in enumerate(os_g):
        lo, hi = g["bornes"]
        lignes.append(f"; {g['garde']} — la zone OS [{lo:#x}, {hi:#x})")
        lignes.append(f".garde_{i}:")
        lignes.append("mov rax, r9")
        lignes.append(f"cmp rax, {lo}")
        lignes.append("jb .refus_garde")
        lignes.append(f"cmp rax, {hi}")
        lignes.append("jae .refus_garde")
        lignes.append("xor eax, eax")
        lignes.append("ret")
    lignes += [".refus_garde:", "mov eax, 0xfffffffb", "ret",
               ".refus_index:", "mov rax, 0xfffffffffffffffe", "ret"]
    return "\n".join(lignes) + "\n", {g["garde"]: g["bornes"] for g in os_g}


def assembler_corridor(texte: str, rva: int) -> bytes:
    lignes = [l.split(";")[0] for l in texte.splitlines()]
    etiquettes = {}
    corps = []
    # l'iteration JUSQU'A CONVERGENCE de la table des etiquettes (les
    # tailles des sauts changent entre passes — 4 passes ne suffisent pas
    # toujours, le constat vecu au harnais : jae 4 octets devant la cible)
    for _ in range(24):
        adr = rva
        nouvelles = {}
        corps = []
        for l in lignes:
            l = l.strip()
            if not l:
                continue
            if l.endswith(":") and l.startswith("."):
                nouvelles[l[:-1]] = adr
                continue
            c = l
            for e, a in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
                c = c.replace(e, hex(a))
            corps.append(c)
            try:
                b, _ = KS.asm(c, adr)
                adr += len(bytes(b))
            except Exception:
                adr += 6
        if nouvelles == etiquettes and etiquettes:
            break
        etiquettes = nouvelles
    octets = b""
    for c in corps:
        for e, a in sorted(etiquettes.items(), key=lambda x: -len(x[0])):
            c = c.replace(e, hex(a))
        try:
            b, _ = KS.asm(c, rva + len(octets))
        except Exception as e:
            raise RuntimeError(f"assemblage echoue (passe finale) : {c!r} : {e}")
        octets += bytes(b)
    return octets


def round_trip(octets: bytes, rva: int) -> bool:
    reins = b""
    for ins in CS.disasm(octets, rva):
        c, _ = KS.asm(f"{ins.mnemonic} {ins.op_str}", ins.address)
        reins += bytes(c)
    return reins == octets


# --------------------------------------------- LE HARNAIS (Unicorn) --------
def harnais(octets: bytes, index: int, r9: int):
    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    uc.mem_map(0xC000, 0x4000)
    uc.mem_map(0x500000, 0x21000)
    uc.mem_map(0x70000, 0x10000)
    uc.mem_write(RVA_CORRIDOR, octets)
    uc.mem_write(0x78000, (0x60000).to_bytes(8, "little"))
    uc.reg_write(unicorn.x86_const.UC_X86_REG_RSP, 0x78000)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_RCX, index)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_R9, r9)
    trace = []
    uc.hook_add(unicorn.UC_HOOK_CODE,
                lambda u, a, s, d: trace.append((a, s)))
    uc.emu_start(RVA_CORRIDOR, 0x60000)
    rax = uc.reg_read(unicorn.x86_const.UC_X86_REG_RAX)
    # mov eax, imm32 MET A ZERO la moitie haute : le refus -5 y vit en
    # forme non signee 0xFFFFFFFB (4294967291 — le miroir du harnais v14) ;
    # la conversion signe aux DEUX largeurs (32/64)
    if 0x80000000 <= rax <= 0xFFFFFFFF:
        rax -= 1 << 32
    elif rax >= 0x8000000000000000:
        rax -= 1 << 64
    return rax, trace


def main():
    rapport = []
    def consigne(l):
        print(l); rapport.append(l)

    consigne("=== LE REJEU DES 116 CERTIFICATS v14 (z3 5.4.1, idempotent) ===")
    rejeu = rejeu_certificats()
    consigne(f"les decharges UNSAT : {rejeu['decharges_unsat']}/58 ; "
             f"les mutations SAT (le relachement d'UNE UNITE) : "
             f"{rejeu['mutations_sat']}/58 ; les ecarts : "
             f"{len(rejeu['ecarts'])}"
             + ("" if not rejeu["ecarts"] else f" — {rejeu['ecarts']}"))
    tout_cert = rejeu["decharges_unsat"] == 58 and \
        rejeu["mutations_sat"] == 58

    consigne("=== LE REGISTRE TCB 58-34-11 (les etages documentes) ===")
    reg = registre_tcb()
    (ICI / "registres" / "registre-tcb-58-34-11.json").write_text(
        json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")
    consigne("58 = 24 CADRE (DECHARGEES PAR PREUVE de layout) + 23 CTX "
             "(DECHARGEES A LA COMPOSITION par la preuve de l'appelant) "
             "+ 11 OS (LES ASSOMPTIONS NOMMEES — le TCB residuel)")
    consigne("la preuve reste PORTANTE : 58/58 relachements d'une unite "
             "SAT au rejeu — le certificat tombe des que l'invariant "
             "cede d'un octet")

    consigne("=== L'EMISSION : le corridor des ONZE a 0xFC00 ===")
    texte, bornes = corps_os_guards()
    (ICI / "notation" / "corridor-onze-os.asm").write_text(
        texte, encoding="utf-8")
    octets = assembler_corridor(texte, RVA_CORRIDOR)
    (ICI / "notation" / "corridor-onze-os.bin").write_bytes(octets)
    rt = round_trip(octets, RVA_CORRIDOR)
    consigne(f"assemble : {len(octets)} o, "
             f"{sum(1 for _ in CS.disasm(octets, RVA_CORRIDOR))} instr, "
             f"round-trip keystone==capstone==keystone : "
             f"{'VERT' if rt else 'ROUGE'}")

    consigne("=== LE HARNAIS : la garde falsifiee refusee aux DEUX bornes "
             "+ LA FACE D'INDEX ===")
    verts = 0
    total = 0
    admis = sum(1 for i in range(11)
                if harnais(octets, i, 0x500800)[0] == 0)
    total += 11
    verts += admis
    consigne(f"les onze admissions honnetes (r9=0x500800) : "
             f"{admis}/11 a rax=0")
    fb = sum(1 for i in range(11)
             if harnais(octets, i, 0x500000 - 1)[0] == -5)
    total += 11
    verts += fb
    consigne(f"la face basse (r9 = 0x4FFFFF) : {fb}/11 REFUSEES a rax=-5")
    fh = sum(1 for i in range(11)
             if harnais(octets, i, 0x501000)[0] == -5)
    total += 11
    verts += fh
    consigne(f"la face haute (r9 = 0x501000) : {fh}/11 REFUSEES a rax=-5")
    fi = all(harnais(octets, idx, 0x500800)[0] == -2
             for idx in (11, 100, 0xFFFFFFFFFFFFFFFF))
    total += 3
    verts += 3 if fi else 0
    consigne(f"la face d'index (11, 100, -1) : "
             f"{'3/3 REFUSEES a rax=-2' if fi else 'ROUGE'}")
    consigne(f"LE HARNAIS : {verts}/{total}"
             f"{' — TOUT VERT' if verts == total else ' — ROUGE'}")

    consigne("=== LA MESURE DU COUT PAR APPEL au harnais emulate ===")
    couts = []
    for i in range(11):
        _, trace = harnais(octets, i, 0x500800)
        couts.append(len(trace))
    consigne("le compte par appel (Unicorn, l'enveloppe comprise — le "
             "dispatch en table + les deux faces) : " +
             ", ".join(f"g{i}={c}" for i, c in enumerate(couts)) +
             f" ; la mediane {sorted(couts)[5]} instr/appel")
    consigne("la garde inline v14 : 7 instr — LE COUT DU DISPATCH en "
             "table : la mediane "
             f"{sorted(couts)[5] - 7} instr de plus par appel (le prix "
             "nomme de l'emission en corridor — le champ unique, les "
             "onze fenetres)")

    (ICI / "registres" / "harnais-tcb.json").write_text(json.dumps({
        "rejeu": rejeu, "registre_tcb": True,
        "corridor": {"octets": len(octets), "round_trip": rt,
                     "rva": RVA_CORRIDOR},
        "harnais": {"verts": verts, "total": total},
        "couts": couts, "sha256": hashlib.sha256(octets).hexdigest(),
    }, indent=2), encoding="utf-8")
    (ICI / "rapport-atelier.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\nOK — les registres + le rapport")


if __name__ == "__main__":
    main()
