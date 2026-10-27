#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Audit final demo.8 (D42 : section critique R_CS initialisée par
l'hôte démo — le devoir de tcp-12 non embarqué ; instrumentation bilatérale).

Vérifie sur les OCTETS RÉELS du binaire fraîchement construit :
  1. empreintes (md5/sha256) ;
  2. les 7 sondes posées (3 interstices D40 + 4 zone libre M2 D42) ;
  3. L00 = 0.3.0-demo.8 ; version u64 0x00030108 @0x2628 ;
  4. le CORRECTIF D42 : win-09 commence par InitializeCriticalSection(R_CS)
     — lea rcx,[rip±disp] → 0x3830 puis call [rip±disp] → IAT 0x20D8,
     AVANT GetStdHandle et tout spawn (I0 de win-09:R3) ;
  5. les sondes S1/S2 dans win-08 (entre accept et spawn, après spawn) et
     sonde4/sonde5 dans win-10 (entre boucle émission et boucle réception,
     entre boucle réception et memcmp) — chaque sonde = lea + mov edx +
     xor r8d + call 0x5000, longueurs exactes ;
  6. l'héritage D41 intact (constantes 0x40 ×2 dans tcp-07, sub/add rsp,0x28,
     lea r9,[rsp+0x20], zéro résiduel) — les blocs scellés n'ont pas bougé ;
  7. la zone M2 des sondes ne recouvre AUCUNE chaîne posée (0x266E-0x26AA,
     entre « echo \\0 » fin 0x266E et « fin connexion » 0x26D8) ;
  8. diff demo.7 → demo.8 CHIRURGICAL : uniquement le code des trois blocs
     révisés (win-08/win-09/win-10), les 4 chaînes de sondes, L00, l'u64
     version et les sommes R10 des trois blocs — RIEN d'autre.

Usage : .venv/bin/python scripts/audit_demo8.py
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

SONDES = {  # nom -> (rva attendu, longueur attendue)
    "SONDE_1": (L.R_SONDE_1, 17), "SONDE_2": (L.R_SONDE_2, 17),
    "SONDE_3": (L.R_SONDE_3, 12), "SONDE_S1": (L.R_SONDE_S1, 12),
    "SONDE_S2": (L.R_SONDE_S2, 17), "SONDE_4": (L.R_SONDE_4, 16),
    "SONDE_5": (L.R_SONDE_5, 14),
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

    # 2. sondes posées
    print("=" * 72)
    print("[2] sondes .rdata (3 interstices D40 + 4 zone libre M2 D42)")
    for nom, (adr, n) in SONDES.items():
        octets = L.CHAINES_SONDES[nom][1]
        off = rva_to_off(pe, adr)
        lu = data[off:off + n]
        bon = lu == octets
        ok &= bon
        print(f"    {nom} @ {adr:#x} : {lu.decode('ascii')!r} "
              f"{'CONFORME' if bon else 'DIVERGENT !'}")

    # 3. version
    print("=" * 72)
    off = rva_to_off(pe, L.CHAINES_ASCII["L00"][0])
    l00 = data[off:off + 40].decode("ascii")
    u64 = struct.unpack("<Q", data[rva_to_off(pe, L.R_VERSION):
                                   rva_to_off(pe, L.R_VERSION) + 8])[0]
    bon = l00 == "L00 demarrage demonstration 0.3.0-demo.8" and u64 == 0x00030108
    ok &= bon
    print(f"[3] L00 : {l00!r} {'CONFORME' if 'demo.8' in l00 else 'DIVERGENT !'}")
    print(f"    u64 version : {u64:#x} {'CONFORME' if u64 == 0x00030108 else 'DIVERGENT !'}")

    # 4. correctif D42 : InitializeCriticalSection(R_CS) en tête de win-09
    print("=" * 72)
    off9 = rva_to_off(pe, 0x4C00)
    code9 = data[off9:off9 + 902]
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
    print(f"[4] correctif D42 : prologue 5 pushes + sub 0x60 "
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

    # 5. sondes dans win-08 / win-10
    print("=" * 72)

    def sondes_bloc(rva, taille, attendu_sondes, nom_bloc):
        nonlocal ok
        code = data[rva_to_off(pe, rva):rva_to_off(pe, rva) + taille]
        ins = list(md.disasm(code, BASE + rva))
        trouves = []
        for i in range(len(ins) - 3):
            a, b, c, d = ins[i:i + 4]
            if (a.mnemonic == "lea" and b.mnemonic == "mov" and
                    c.mnemonic == "xor" and d.mnemonic == "call"):
                if "rip" not in a.op_str:
                    continue
                disp = int(a.op_str.split("rip ")[1].replace(" ", "")
                           .split("]")[0], 16)
                cible = a.address + a.size + disp - BASE
                mlen = b.op_str.split(", ")[1]
                n = int(mlen, 0)
                if cible in attendu_sondes and attendu_sondes[cible] == n \
                        and c.op_str == "r8d, r8d" and d.op_str == "0x140005000":
                    trouves.append((cible, n))
        bon_ = len(trouves) == len(attendu_sondes)
        ok &= bon_
        detail = ", ".join(f"{k:#x}/{v}" for k, v in trouves)
        print(f"    {nom_bloc} : {len(trouves)}/{len(attendu_sondes)} sondes "
              f"({detail}) {'CONFORME' if bon_ else 'DIVERGENT !'}")

    print("[5] instrumentation bilatérale (D42)")
    sondes_bloc(0x1D00, 179, {L.R_SONDE_S1: 12, L.R_SONDE_S2: 17}, "win-08:R2")
    sondes_bloc(0x4980, 195, {L.R_SONDE_4: 16, L.R_SONDE_5: 14}, "win-10:R2")

    # ordre win-10 : sonde4 APRÈS la boucle émission (dernier jb), AVANT la
    # boucle réception ; sonde5 APRÈS la boucle réception, AVANT le memcmp
    off10 = rva_to_off(pe, 0x4980)
    ins10 = list(md.disasm(data[off10:off10 + 195], BASE + 0x4980))
    pos = {m: next(i for i, x in enumerate(ins10) if x.mnemonic == m)
           for m in ("jb", "call")}
    jbs = [i for i, x in enumerate(ins10) if x.mnemonic == "jb"]
    memcmpp = next(i for i, x in enumerate(ins10)
                   if x.mnemonic == "call" and x.op_str == hex(BASE + 0x1180))
    s4 = next(i for i in range(len(ins10) - 3)
              if ins10[i].mnemonic == "lea" and "rip" in ins10[i].op_str
              and ins10[i].address + ins10[i].size + int(
                  ins10[i].op_str.split("rip ")[1].replace(" ", "")
                  .split("]")[0], 16) - BASE == L.R_SONDE_4)
    s5 = next(i for i in range(len(ins10) - 3)
              if ins10[i].mnemonic == "lea" and "rip" in ins10[i].op_str
              and ins10[i].address + ins10[i].size + int(
                  ins10[i].op_str.split("rip ")[1].replace(" ", "")
                  .split("]")[0], 16) - BASE == L.R_SONDE_5)
    bon = jbs[0] < s4 < jbs[1] and jbs[1] < s5 < memcmpp
    ok &= bon
    print(f"    ordre win-10 : jb(envoi) < sonde4 < jb(récep) < sonde5 < "
          f"memcmp {'CONFORME' if bon else 'DIVERGENT !'}")

    # 6. héritage D41 intact (tcp-07 inchangé)
    print("=" * 72)
    off7 = rva_to_off(pe, 0x4400)
    code7 = data[off7:off7 + 512]
    n40 = code7.count(bytes.fromhex("41b840000000"))
    s08 = code7.count(bytes.fromhex("4883ec08"))
    p28 = code7.count(bytes.fromhex("4883ec28"))
    l20 = code7.count(bytes.fromhex("4c8d4c2420"))
    bon = (n40 == 2 and s08 == 0 and p28 == 1 and l20 == 1)
    ok &= bon
    print(f"[6] héritage D41 tcp-07 : mov r8d,0x40 × {n40}/2 ; sub rsp,0x28 "
          f"× {p28}/1 ; lea r9,[rsp+0x20] × {l20}/1 ; sub rsp,8 résiduel "
          f"× {s08}/0 {'CONFORME' if bon else 'DIVERGENT !'}")

    # 7. zone sondes sans collision avec les chaînes posées
    print("=" * 72)
    debut, fin = L.R_SONDE_S1, L.R_SONDE_5 + 14
    nouvelles = {L.R_SONDE_S1, L.R_SONDE_S2, L.R_SONDE_4, L.R_SONDE_5}
    chaines = ([a for a, _t, _n in L.CHAINES_UTF16.values()] +
               [a for a, _o, _n in L.CHAINES_ASCII.values()] +
               [a for a, _o, _n in L.CHAINES_SONDES.values() if a not in nouvelles] +
               [L.R_MSG_CRLF, L.R_MSG_ECHO, L.R_MSG_FIN, L.R_PHRASE,
                L.R_PHRASE_MAJ, L.R_FIXTURES, L.R_STAGING, L.R_TAB_SUM,
                L.R_VERSION, L.R_ANCRE, L.R_RELOC])
    collision = [a for a in chaines if debut <= a < fin]
    bon = not collision and fin <= 0x26D8
    ok &= bon
    print(f"[7] zone sondes D42 : {debut:#x}-{fin:#x} (bornée par « fin "
          f"connexion » @0x26D8), 0 collision posée "
          f"{'CONFORME' if bon else 'DIVERGENT !'}")

    # 8. diff chirurgical demo.7 -> demo.8
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
        sondes_z = set(range(rva_to_off(pe, debut), rva_to_off(pe, fin)))
        l00_z = set(range(rva_to_off(pe, L.CHAINES_ASCII["L00"][0]),
                          rva_to_off(pe, L.CHAINES_ASCII["L00"][0]) + 41))
        ver_z = set(range(rva_to_off(pe, L.R_VERSION),
                          rva_to_off(pe, L.R_VERSION) + 8))
        table_z = set(range(rva_to_off(pe, L.R_TAB_SUM),
                            rva_to_off(pe, L.R_TAB_SUM) + 29 * 16))
        autorise = code | sondes_z | l00_z | ver_z | table_z
        hors = [i for i in diffs if i not in autorise]
        n_code = sum(1 for i in diffs if i in code)
        print(f"[8] diff demo.7 → demo.8 : {len(diffs)} octets "
              f"({n_code} dans le code des 3 blocs révisés, "
              f"{len(diffs) - n_code} en données : sondes {len(sondes_z & set(diffs))}, "
              f"L00, u64, sommes R10) ; hors zones autorisées : {len(hors)}")
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
        print("[8] demo.7 introuvable dans git — diff ignoré")

    print("=" * 72)
    print(f"VERDICT : {'TOUT CONFORME — demo.8 prête pour le terrain' if ok else 'DIVERGENCES !'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
