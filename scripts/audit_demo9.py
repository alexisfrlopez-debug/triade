#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Audit final demo.9 (D43 : retrait de TOUTES les sondes après constat
vert terrain demo.8 — « boucle § 5 complète — DÉMO OK », 28/28 lignes).

Vérifie sur les OCTETS RÉELS du binaire fraîchement construit :
  1. empreintes (md5/sha256) ;
  2. les 7 zones de sondes de demo.8 VIDES (retour au zéro des zones libres :
     3 interstices D40 + 4 adresses zone libre M2 D42) ;
  3. L00 = 0.3.0-demo.9 ; version u64 0x00030109 @0x2628 ;
  4. le CORRECTIF D42 VIVANT : win-09 commence toujours par
     InitializeCriticalSection(R_CS) — lea → 0x3830 puis call → IAT 0x20D8,
     AVANT GetStdHandle et tout spawn (I0 de win-09) ;
  5. AUCUN appel à l'entrée trace de win-05 (0x5000) depuis win-08, win-09
     et win-10 — les sondes sont retirées des trois côtés (le journal
     nominal vit ailleurs : 11 lignes du scénario + 6 de démarrage GUI) ;
  6. la séquence win-10 revenue à R1 : boucle émission → boucle réception →
     memcmp, sans intermédiaire ;
  7. l'héritage D41 intact (constantes 0x40 ×2 dans tcp-07, sub/add rsp,0x28,
     lea r9,[rsp+0x20], zéro résiduel) — les blocs scellés n'ont pas bougé ;
  8. diff demo.8 → demo.9 CHIRURGICAL : uniquement le code des trois blocs
     révisés (win-08/win-09/win-10), les 7 zones de sondes (retour zéro),
     L00, l'u64 version et les sommes R10 des trois blocs — RIEN d'autre.

Usage : .venv/bin/python scripts/audit_demo9.py
"""

import hashlib
import pathlib
import struct
import subprocess
import sys

import capstone
import pefile

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "demo"))
import layout as L  # noqa: E402

EXE = REPO / "demo" / "demo.exe"
BASE = 0x140000000

# Adresses/longueurs des sondes telles que posées en demo.6..demo.8
# (D40 : 3 interstices ; D42 : 4 en zone libre M2) — retirées en demo.9.
SONDES_DEMO8 = {  # nom -> (rva, longueur)
    "SONDE_1": (0x2748, 17), "SONDE_2": (0x276C, 17), "SONDE_3": (0x22F1, 12),
    "SONDE_S1": (0x266E, 12), "SONDE_S2": (0x267A, 17),
    "SONDE_4": (0x268B, 16), "SONDE_5": (0x269B, 14),
}


def rva_to_off(pe, rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.Misc_VirtualSize:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    raise ValueError(rva)


def main():
    data = EXE.read_bytes()
    pe = pefile.PE(str(EXE), fast_load=True)
    md5 = hashlib.md5(data).hexdigest()
    sha = hashlib.sha256(data).hexdigest()
    ok = True
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

    print("=" * 72)
    print(f"[1] demo.exe : {len(data):,} o — md5 {md5}")
    print(f"    sha256 {sha}")

    # 2. zones de sondes VIDES (retour au zéro des zones libres)
    print("=" * 72)
    print("[2] sondes .rdata RETIRÉES (3 interstices D40 + 4 zone libre M2 D42)")
    for nom, (adr, n) in SONDES_DEMO8.items():
        off = rva_to_off(pe, adr)
        lu = data[off:off + n]
        bon = lu == b"\x00" * n
        ok &= bon
        print(f"    {nom} @ {adr:#x} ({n} o) : "
              f"{'ZÉRO CONFORME (retirée)' if bon else 'RÉSIDUEL ! ' + lu!r}")

    # 3. version
    print("=" * 72)
    off = rva_to_off(pe, L.CHAINES_ASCII["L00"][0])
    l00 = data[off:off + 40].decode("ascii")
    u64 = struct.unpack("<Q", data[rva_to_off(pe, L.R_VERSION):
                                   rva_to_off(pe, L.R_VERSION) + 8])[0]
    bon = l00 == "L00 demarrage demonstration 0.3.0-demo.9" and u64 == 0x00030109
    ok &= bon
    print(f"[3] L00 : {l00!r} {'CONFORME' if 'demo.9' in l00 else 'DIVERGENT !'}")
    print(f"    u64 version : {u64:#x} {'CONFORME' if u64 == 0x00030109 else 'DIVERGENT !'}")

    # 4. correctif D42 : InitializeCriticalSection(R_CS) en tête de win-09
    print("=" * 72)
    off9 = rva_to_off(pe, 0x4C00)
    code9 = data[off9:off9 + 842]
    insns = list(md.disasm(code9, BASE + 0x4C00))
    attendus = [("push", "rbx"), ("push", "r12"), ("push", "r13"),
                ("push", "r14"), ("push", "r15"), ("sub", "rsp, 0x60")]
    seq = [(i.mnemonic, i.op_str) for i in insns[:6]]
    prologue_bon = seq == attendus
    init_lea = init_call = None
    if prologue_bon and len(insns) >= 8:
        a, b = insns[6], insns[7]
        if a.mnemonic == "lea" and b.mnemonic == "call" and "rip" in a.op_str:
            disp = int(a.op_str.split("rip ")[1].replace(" ", "").split("]")[0], 16)
            cible_lea = a.address + a.size + disp
            if "rip" in b.op_str:
                disp = int(b.op_str.split("rip ")[1].replace(" ", "").split("]")[0], 16)
                cible_call = b.address + b.size + disp
                init_lea, init_call = cible_lea - BASE, cible_call
    bon = prologue_bon and init_lea == 0x3830 and init_call == BASE + 0x20D8
    ok &= bon
    print(f"[4] correctif D42 VIVANT : prologue 5 pushes + sub 0x60 "
          f"{'✓' if prologue_bon else 'DIVERGENT !'} ; "
          f"1er appel = InitializeCriticalSection : lea → "
          f"{init_lea:#x} "
          f"{'(R_CS) ✓' if init_lea == 0x3830 else 'DIVERGENT !'} ; "
          f"call → IAT {'0x20D8 ✓' if init_call == BASE + 0x20D8 else 'DIVERGENT !'}")
    # l'appel précède GetStdHandle (I0 : avant TOUT)
    gsh = next((i.address for i in insns if i.mnemonic == "call"
                and "rip" in i.op_str and
                i.address + i.size + int(i.op_str.split("rip ")[1]
                                         .replace(" ", "").split("]")[0], 16)
                == BASE + 0x20B0), None)
    bon2 = gsh is not None and insns[7].address < gsh
    ok &= bon2
    print(f"    ordre I0 : init AVANT GetStdHandle "
          f"{'CONFORME' if bon2 else 'DIVERGENT !'} "
          f"(init @ {insns[7].address - BASE:#x}, GSH @ "
          f"{(gsh - BASE) if gsh else 0:#x})")

    # 5. AUCUN appel à l'entrée trace (0x5000) depuis les trois blocs
    print("=" * 72)
    print("[5] retrait des sondes — aucun appel trace (0x5000) des trois blocs")
    for nom_bloc, rva, taille in (("win-08:R3", 0x1D00, 139),
                                  ("win-09:R4", 0x4C00, 842),
                                  ("win-10:R3", 0x4980, 155)):
        code = data[rva_to_off(pe, rva):rva_to_off(pe, rva) + taille]
        ins = list(md.disasm(code, BASE + rva))
        appels_trace = [i.address - BASE for i in ins
                        if i.mnemonic == "call" and i.op_str == hex(BASE + 0x5000)]
        bon_ = not appels_trace
        ok &= bon_
        print(f"    {nom_bloc} : {len(appels_trace)} appel(s) à 0x5000 "
              f"{'— CONFORME (muet)' if bon_ else 'SONDE RÉSIDUELLE ! ' + str(appels_trace)}")
    # win-05 lui-même reste joignable depuis win-02/04 (entrées légitimes)
    for nom_bloc, rva, taille in (("win-02:R3", 0x1440, 364),
                                  ("win-04:R4", 0x1640, 876)):
        code = data[rva_to_off(pe, rva):rva_to_off(pe, rva) + taille]
        ins = list(md.disasm(code, BASE + rva))
        n_trace = sum(1 for i in ins if i.mnemonic == "call"
                      and i.op_str in (hex(BASE + 0x5000), hex(BASE + 0x5100)))
        bon_ = n_trace > 0
        ok &= bon_
        print(f"    {nom_bloc} : {n_trace} appel(s) journal win-05 "
              f"{'(légitimes, intacts)' if bon_ else '— DIVERGENT !'}")

    # 6. win-10 revenu à R1 : dernier jb réception → (préparation memcmp
    #    EXACTEMENT : lea rcx,[rsp+0x20] ; mov rdx,r12 ; mov r8d,14) → memcmp
    print("=" * 72)
    off10 = rva_to_off(pe, 0x4980)
    ins10 = list(md.disasm(data[off10:off10 + 155], BASE + 0x4980))
    jbs = [i for i, x in enumerate(ins10) if x.mnemonic == "jb"]
    memcmpp = next(i for i, x in enumerate(ins10)
                   if x.mnemonic == "call" and x.op_str == hex(BASE + 0x1180))
    entre = [(x.mnemonic, x.op_str) for x in ins10[jbs[1] + 1:memcmpp]]
    attendu_entre = [("lea", "rcx, [rsp + 0x20]"), ("mov", "rdx, r12"),
                     ("mov", "r8d, 0xe")]
    bon = (len(jbs) == 2 and entre == attendu_entre)
    ok &= bon
    print(f"[6] win-10 séquence R1 : jb(récep) → préparation memcmp exacte "
          f"{'CONFORME' if bon else 'DIVERGENT !'} "
          f"(dernier jb @ {ins10[jbs[1]].address - BASE:#x}, memcmp @ "
          f"{ins10[memcmpp].address - BASE:#x}, entre : {entre})")

    # 7. héritage D41 intact (tcp-07 inchangé)
    print("=" * 72)
    off7 = rva_to_off(pe, 0x4400)
    code7 = data[off7:off7 + 512]
    n40 = code7.count(bytes.fromhex("41b840000000"))
    s08 = code7.count(bytes.fromhex("4883ec08"))
    p28 = code7.count(bytes.fromhex("4883ec28"))
    l20 = code7.count(bytes.fromhex("4c8d4c2420"))
    bon = (n40 == 2 and s08 == 0 and p28 == 1 and l20 == 1)
    ok &= bon
    print(f"[7] héritage D41 tcp-07 : mov r8d,0x40 × {n40}/2 ; sub rsp,0x28 "
          f"× {p28}/1 ; lea r9,[rsp+0x20] × {l20}/1 ; sub rsp,8 résiduel "
          f"× {s08}/0 {'CONFORME' if bon else 'DIVERGENT !'}")

    # 8. diff chirurgical demo.8 -> demo.9
    print("=" * 72)
    ancien = subprocess.run(
        ["git", "-C", str(REPO), "show", "HEAD:demo/demo.exe"],
        capture_output=True).stdout
    if len(ancien) == len(data):
        diffs = [i for i in range(len(data)) if ancien[i] != data[i]]

        def zone(rva, taille):
            o = rva_to_off(pe, rva)
            return range(o, o + taille)

        code = set(zone(0x1D00, 0x100)) | set(zone(0x4C00, 0x3C0)) \
            | set(zone(0x4980, 0x180))                     # blocs révisés
        sondes_z = set()
        for _nom, (adr, n) in SONDES_DEMO8.items():
            sondes_z |= set(range(rva_to_off(pe, adr), rva_to_off(pe, adr) + n))
        l00_z = set(range(rva_to_off(pe, L.CHAINES_ASCII["L00"][0]),
                          rva_to_off(pe, L.CHAINES_ASCII["L00"][0]) + 41))
        ver_z = set(range(rva_to_off(pe, L.R_VERSION),
                          rva_to_off(pe, L.R_VERSION) + 8))
        table_z = set(range(rva_to_off(pe, L.R_TAB_SUM),
                            rva_to_off(pe, L.R_TAB_SUM) + 29 * 16))
        autorise = code | sondes_z | l00_z | ver_z | table_z
        hors = [i for i in diffs if i not in autorise]
        n_code = sum(1 for i in diffs if i in code)
        print(f"[8] diff demo.8 → demo.9 : {len(diffs)} octets "
              f"({n_code} dans le code des 3 blocs révisés, "
              f"{len(diffs) - n_code} en données : sondes {len(sondes_z & set(diffs))} "
              f"(retour zéro), L00, u64, sommes R10) ; "
              f"hors zones autorisées : {len(hors)}")
        if hors:
            for i in hors[:8]:
                rva = None
                for s in pe.sections:
                    if s.PointerToRawData <= i < s.PointerToRawData + s.SizeOfRawData:
                        rva = s.VirtualAddress + (i - s.PointerToRawData)
                print(f"      !! offset {i:#x} (rva {rva:#x})")
        bon = not hors
        ok &= bon
        print(f"    {'CHIRURGICAL CONFORME' if bon else 'ÉTENDUE INATTENDUE !'}")
    else:
        print("[8] demo.8 introuvable dans git — diff ignoré")

    print("=" * 72)
    print(f"VERDICT : {'TOUT CONFORME — demo.9 finale de lignée (sondes retirées, correctifs vivants)' if ok else 'DIVERGENCES !'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
