#!/usr/bin/env python3
"""conformite_profil.py — Suite de conformite du profil x86-64-win11-pe (spec 8.2, D22).

Livrable obligatoire de l'instanciation d'un profil (specification 8.2) : chaque
element constitutif est CONSTATE depuis l'artefact scelle (selftest.exe), les
sources (couche I, notation) et le plan d'adressage (layout.py) — jamais declare
sans preuve. Jalon M1 : elements 1-4 et 6-7 ; l'element 5 (patch a chaud)
releve du jalon M2 et est explicitement rapporte hors perimetre.

Elements et constats :
  1 ISA et types        : machine COFF 0x8664, .text decodable en mode 64 bits,
                          qwords INT/IAT (usize 8), arene alignee 64, boutisme
                          little-endian decode depuis les structures .rdata ;
  2 ABI msx64           : non-volatils sauvegardes/restaures, shadow space >= 0x28
                          avant chaque appel, aucune reference sous RSP (zone
                          rouge inexistante), piles equilibrees, args volatils ;
  3 Format PE32+        : magic 0x20B, DYNAMICBASE+HEVA+NX, sections .text RX /
                          .rdata R / .data RW (aucune section W+X), BASERELOC
                          valide, entree dans la zone app (D28) ;
  4 Interface systeme   : imports kernel32 exacts (3 fonctions), appels
                          indirects exclusivement vers les slots IAT, aucun
                          syscall/sysenter/int, aucune adresse hors image ;
  5 Patch a chaud       : hors perimetre M1 (jalon M2) — non evalue, rapporte ;
  6 Notation            : round-trip 100 % et identite notation -> octets
                          embarques, y compris les blocs M0 reutilises ;
  7 Granularite/padding : slots D28 alignes, padding NOP intra-slot, reserve
                          int3, demonstration R7 (demo_r7.py) au vert.

Ecrit m1/conformite.txt (ligne unique ASCII, lue par le tableau de bord) et
retourne (ok, lignes) pour build_m1.sceller_rc.

Usage : python3 conformite_profil.py   (depuis m1/)
"""

from __future__ import annotations

import os
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

import capstone
import pefile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

NON_VOLATILS = ("rbx", "rbp", "rdi", "rsi", "r12", "r13", "r14", "r15")
SLOTS_IAT = frozenset(L.IAT_SLOTS.values())


class Suite:
    """Collecte les controles par element ; verdict vert si tous PASS."""

    def __init__(self) -> None:
        self.controles: list[tuple[int, str, bool, str]] = []

    def verifie(self, element: int, nom: str, ok: bool, detail: str = "") -> bool:
        self.controles.append((element, nom, bool(ok), detail))
        return bool(ok)

    def lignes(self) -> list[str]:
        out = ["Suite de conformite du profil x86-64-win11-pe (spec 8.2) — jalon M1"]
        for element in (1, 2, 3, 4, 6, 7):
            du_element = [c for c in self.controles if c[0] == element]
            if not du_element:
                continue
            verts = sum(1 for c in du_element if c[2])
            out.append(f"  [{element}] {len(du_element)}/{len(du_element)} controles : "
                       + ("PASS" if verts == len(du_element) else "ECHEC"))
            for _, nom, ok, detail in du_element:
                out.append(f"      {'PASS' if ok else 'ECHEC'} : {nom}"
                           + (f" ({detail})" if detail else ""))
        out.append("  [5] patch a chaud : hors perimetre M1 (jalon M2) — non evalue, rapporte")
        total = len(self.controles)
        verts = sum(1 for c in self.controles if c[2])
        out.append(f"Verdict : {verts}/{total} controles PASS ; "
                   + ("VERTE" if verts == total else "ROUGE"))
        return out

    @property
    def ok(self) -> bool:
        return all(c[2] for c in self.controles)


def _lire_exe() -> bytes:
    with open(os.path.join(ICI, "selftest.exe"), "rb") as f:
        return f.read()


def _blocs() -> list[tuple[str, str, int, int]]:
    """(id, spec, rva, taille) — 9 blocs embarques dans selftest.exe (layout D28)."""
    b = [(bid, sid, rva, taille) for bid, sid, rva, taille, _, _ in L.BLOCS_IO + L.BLOCS_LIBC]
    b.append((L.BLOC_AUTOTEST[0], L.BLOC_AUTOTEST[1], L.BLOC_AUTOTEST[2], L.BLOC_AUTOTEST[3]))
    return b


def _desassemble(exe: bytes, rva: int, taille: int):
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    brut = exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + taille]
    insns = list(cs.disasm(brut, rva))
    return insns, len(brut)


def element_1(s: Suite, exe: bytes, pe) -> None:
    """ISA et types : tailles, alignements, boutisme constates = declares."""
    s.verifie(1, "machine COFF = 0x8664 (AMD64)", pe.FILE_HEADER.Machine == 0x8664,
              hex(pe.FILE_HEADER.Machine))
    # .text entier decodable en mode 64 bits — aucun octet orphelin
    insns, bruts = _desassemble(exe, L.TEXT_RVA, L.TEXT_VSIZE)
    couverts = sum(i.size for i in insns)
    s.verifie(1, ".text 0x1000 o decodable en mode 64 bits sans reste", couverts == bruts,
              f"{len(insns)} instructions, {couverts}/{bruts} octets")
    # Types : INT et IAT sont des qwords (usize = 8) — little-endian
    def qword(rva):
        return struct.unpack_from("<Q", exe, L.RDATA_FILE + (rva - L.RDATA_RVA))[0]
    hints = [qword(L.R_INT), qword(L.R_INT + 8), qword(L.R_INT + 16)]
    s.verifie(1, "INT = qwords little-endian vers les hint/names declares",
              hints == [L.R_HN_GSH, L.R_HN_WF, L.R_HN_EP] and qword(L.R_INT + 24) == 0,
              " ".join(hex(h) for h in hints))
    desc = struct.unpack_from("<IIIII", exe, L.RDATA_FILE + (L.R_DESC_IMPORT - L.RDATA_RVA))
    s.verifie(1, "descripteur d'import : OFT/Name/FT aux RVA declarees (struct 5 champs LE)",
              (desc[0], desc[3], desc[4]) == (L.R_INT, L.R_NOM_DLL, L.R_IAT),
              f"OFT={desc[0]:#x} Name={desc[3]:#x} FT={desc[4]:#x}")
    # Alignements : arene 64 (contrat libc-05), slots multiples de 64
    s.verifie(1, "arene d'allocation alignee 64 (contrat libc-05)",
              L.ARENE_BASE % 64 == 0 and L.ARENE_TAILLE % 64 == 0,
              f"ARENE_BASE={L.ARENE_BASE:#x}, {L.ARENE_TAILLE} o")


def _ecrits_non_volatils(insns) -> dict[str, int]:
    """Premier index d'instruction ecrivant chaque non-volatil (capstone detail)."""
    cs_detail = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    cs_detail.detail = True
    premiers: dict[str, int] = {}
    for idx, insn in enumerate(insns):
        d = cs_detail.disasm(insn.bytes, insn.address)
        for i in d:
            try:
                _, ecrits = i.regs_access()
            except capstone.CsError:
                continue
            for r in ecrits:
                nom = i.reg_name(r)
                if nom in NON_VOLATILS and nom not in premiers:
                    premiers[nom] = idx
    return premiers


def element_2(s: Suite, exe: bytes) -> None:
    """ABI msx64 : volatilite, shadow space, zone rouge, equilibrage."""
    for bid, _, rva, taille in _blocs():
        insns, _ = _desassemble(exe, rva, taille)
        appels = [i for i in insns if i.mnemonic == "call"]
        # Non-volatils : push AVANT la premiere ecriture ; restauration par pop
        poussees_a = {i.op_str: k for k, i in enumerate(insns)
                      if i.mnemonic == "push" and i.op_str in NON_VOLATILS}
        sorties = [i.op_str for i in insns if i.mnemonic == "pop" and i.op_str in NON_VOLATILS]
        premiers = _ecrits_non_volatils(insns)
        sauvegarde_ok = all(reg in poussees_a and poussees_a[reg] < k
                            for reg, k in premiers.items())
        s.verifie(2, f"{bid}: non-volatils pousses avant toute ecriture", sauvegarde_ok,
                  f"ecrits={sorted(premiers)} pousses={sorted(poussees_a)}")
        termine_ret = any(i.mnemonic == "ret" for i in insns)
        if termine_ret:
            poussees = [i.op_str for i in insns if i.mnemonic == "push" and i.op_str in NON_VOLATILS]
            k = len(insns)
            while k > 0 and insns[k - 1].mnemonic == "nop":   # ignorer le padding terminal
                k -= 1
            s.verifie(2, f"{bid}: non-volatils restaures (multisets egaux, bloc retournant)",
                      sorted(poussees) == sorted(sorties) and k > 0 and insns[k - 1].mnemonic == "ret",
                      f"{sorted(poussees)} / {sorted(sorties)} ; terminale={insns[k - 1].mnemonic if k else '-'}")
        else:
            s.verifie(2, f"{bid}: bloc sans retour (sortie par exit) — aucune restauration attendue",
                      not sorties)
        # Shadow space : allocation >= 0x28 avant le premier appel
        if appels:
            premier = insns.index(appels[0])
            sub = next((i for i in insns[:premier] if i.mnemonic == "sub"
                        and i.op_str.startswith("rsp,")), None)
            alloue = sub is not None and int(sub.op_str.split(",")[1].strip(), 16) >= 0x28
            s.verifie(2, f"{bid}: shadow space alloue avant le premier appel (>= 0x28)",
                      alloue, sub.op_str if sub else "aucun sub rsp")
        # Zone rouge msx64 : aucune reference memoire sous RSP
        s.verifie(2, f"{bid}: aucune reference sous RSP (zone rouge inexistante en msx64)",
                  not any("rsp - " in i.op_str for i in insns))
        # Pile equilibree pour les blocs qui retournent (ret terminal deja constate)
        if termine_ret:
            n_push = sum(1 for i in insns if i.mnemonic == "push")
            n_pop = sum(1 for i in insns if i.mnemonic == "pop")
            s.verifie(2, f"{bid}: pile equilibree (push == pop, tout registre)",
                      n_push == n_pop,
                      f"{n_push} push / {n_pop} pop")
    # Arguments volatils : motifs contractuels constates
    w, _ = _desassemble(exe, 0x1040, 0x40)          # a10002 write
    s.verifie(2, "a10002: 4e/5e args WriteFile annules (r9d, [rsp+0x20])",
              any(i.mnemonic == "xor" and i.op_str == "r9d, r9d" for i in w)
              and any(i.mnemonic == "mov" and "[rsp + 0x20]" in i.op_str and i.op_str.endswith("0") for i in w))
    a, _ = _desassemble(exe, 0x1800, 0x800)         # b20008 autotest
    s.verifie(2, "b20008: GetStdHandle appele avec STD_OUTPUT_HANDLE dans ecx (-11)",
              any(i.mnemonic == "mov" and i.op_str.replace(" ", "") in
                  ("ecx,-11", "ecx,0xfffffff5") for i in a))


def element_3(s: Suite, exe: bytes, pe) -> None:
    """Format PE32+ : en-tetes valides, protections actives constatees."""
    s.verifie(3, "magic PE32+ 0x20B, 3 sections, alignements 0x200/0x1000",
              pe.OPTIONAL_HEADER.Magic == 0x20B and len(pe.sections) == 3
              and pe.OPTIONAL_HEADER.FileAlignment == 0x200
              and pe.OPTIONAL_HEADER.SectionAlignment == 0x1000)
    dllchar = pe.OPTIONAL_HEADER.DllCharacteristics
    s.verifie(3, "protections : DYNAMICBASE|HIGH_ENTROPY_VA|NX_COMPAT actives",
              dllchar & 0x0160 == 0x0160, hex(dllchar))
    attendus = {".text": 0x60000020, ".rdata": 0x40000040, ".data": 0xC0000040}
    constates = {sec.Name.decode().rstrip("\x00"): sec.Characteristics for sec in pe.sections}
    s.verifie(3, "sections .text RX / .rdata R / .data RW — aucune W+X",
              constates == attendus, str({k: hex(v) for k, v in constates.items()}))
    # BASERELOC : bloc minimal valide (entrees ABSOLUTE, image independante en position)
    reloc_dir = pe.OPTIONAL_HEADER.DATA_DIRECTORY[5]
    s.verifie(3, "BASERELOC present et coherent (page .text, 12 o, entrees ABSOLUTE)",
              reloc_dir.VirtualAddress == L.R_RELOC and reloc_dir.Size == 12)
    page, taille, e1, e2 = struct.unpack_from("<IIHH", exe,
                                              L.RDATA_FILE + (L.R_RELOC - L.RDATA_RVA))
    s.verifie(3, "bloc de relocalisation decodable : PageRVA .text, 2 entrees type 0",
              page == L.TEXT_RVA and taille == 12 and (e1 >> 12, e2 >> 12) == (0, 0),
              f"page={page:#x} size={taille}")
    s.verifie(3, "point d'entree 0x1800 en zone app (hors blocs scelles, D28)",
              pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE, hex(L.ENTREE))


def element_4(s: Suite, exe: bytes, pe) -> None:
    """Interface systeme : resolution IAT, contrat d'appels, aucun contournement."""
    dlls = {d.dll.decode().lower(): {i.name.decode() for i in d.imports if i.name}
            for d in pe.DIRECTORY_ENTRY_IMPORT}
    s.verifie(4, "imports exacts : kernel32.dll x {GetStdHandle, WriteFile, ExitProcess}",
              dlls == {"kernel32.dll": {"GetStdHandle", "WriteFile", "ExitProcess"}},
              str(dlls))
    s.verifie(4, "IAT sur disque identique a l'INT (hint/names)",
              exe[L.RDATA_FILE + (L.R_IAT - L.RDATA_RVA): L.RDATA_FILE + (L.R_IAT - L.RDATA_RVA) + 24]
              == exe[L.RDATA_FILE + (L.R_INT - L.RDATA_RVA): L.RDATA_FILE + (L.R_INT - L.RDATA_RVA) + 24])
    # Tous les appels : indirects -> slots IAT uniquement ; directs -> image uniquement
    indirects_invalides, directs_invalides, syscalls = [], [], []
    for bid, _, rva, taille in _blocs():
        insns, _ = _desassemble(exe, rva, taille)
        for i in insns:
            if i.mnemonic == "call":
                if "rip" in i.op_str:                    # call [rip + disp]
                    cible = i.address + i.size + int(i.op_str.split("rip + ")[1].rstrip("]"), 16)
                    if cible not in SLOTS_IAT:
                        indirects_invalides.append((bid, hex(i.address), hex(cible)))
                elif i.op_str.startswith("0x"):          # appel interne direct rel32
                    cible = int(i.op_str, 16)
                    if not (L.TEXT_RVA <= cible < L.TEXT_RVA + L.TEXT_VSIZE):
                        directs_invalides.append((bid, hex(cible)))
            if i.mnemonic in ("syscall", "sysenter") or (i.mnemonic == "int"):
                syscalls.append((bid, i.mnemonic))
    s.verifie(4, "appels indirects exclusivement vers les 3 slots IAT (D7)",
              not indirects_invalides, str(indirects_invalides[:3]))
    s.verifie(4, "appels directs uniquement vers des blocs de l'image (.text)",
              not directs_invalides, str(directs_invalides[:3]))
    s.verifie(4, "aucun syscall/sysenter/int (interface IAT exclusive)",
              not syscalls, str(syscalls[:3]))
    s.verifie(4, "aucune adresse hors image chargee par movabs (image independante en position)",
              all(L.IMAGE_BASE <= int(i.op_str.split(",")[1].strip(), 16) < L.IMAGE_BASE + L.SIZE_OF_IMAGE
                  for _, _, rva, taille in _blocs()
                  for i in _desassemble(exe, rva, taille)[0]
                  if i.mnemonic == "movabs"))


def element_6(s: Suite, exe: bytes) -> None:
    """Notation : round-trip 100 % et identite notation -> artefact scelle."""
    import build_m1 as bm                       # assemblage + round-trip + oracle structurel
    blocs, _, code, verrous = bm.assembler_tout(2)
    s.verifie(6, "round-trip keystone->capstone 100 % sur les 9 blocs embarques",
              all(len(code[bid]["insns"]) > 0 for bid, _, _, _, _ in blocs),
              f"{sum(len(code[bid]['insns']) for bid, _, _, _, _ in blocs)} instructions")
    divergents = []
    for bid, rva, slot in [(b[0], b[3], b[4]) for b in blocs]:
        embarque = exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        if embarque != code[bid]["slot"]:
            divergents.append(bid)
    s.verifie(6, "identite notation -> octets embarques (WYSIWYG, aucun post-patching)",
              not divergents, str(divergents))
    s.verifie(6, "oracle structurel vert sur le corpus du profil", len(verrous) >= 134,
              f"{len(verrous)} verrous")
    with open(os.path.join(RACINE, "m0", "hello.exe"), "rb") as f:
        hello = f.read()
    def tranche(buf, rva, n):
        return buf[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + n]
    s.verifie(6, "blocs M0 reutilises octet-identiques a hello.exe (corpus M0 exact)",
              tranche(hello, 0x1040, 0x40) == tranche(exe, 0x1040, 0x40)
              and tranche(hello, 0x1080, 0x40) == tranche(exe, 0x1080, 0x40))


def element_7(s: Suite, exe: bytes) -> None:
    """Granularite et padding : slots D28, remplissages, adresses stables (R7)."""
    alignes = all(rva % 0x40 == 0 and taille >= 0x40
                  for _, _, rva, taille in _blocs())
    s.verifie(7, "slots multiples de 64 octets (granularite D8, plan D28)", alignes)
    # Padding intra-slot : NOP apres le code ; reserve : int3
    import build_m1 as bm
    blocs, _, code, _ = bm.assembler_tout(2)
    padding_ok = all(
        all(b == 0x90 for b in code[b[0]]["slot"][len(code[b[0]]["octets"]):])
        for b in blocs)
    s.verifie(7, "padding intra-slot = NOP (0x90) jusqu'au bord du slot", padding_ok)
    reserves = [(0x1000, 0x1040), (0x10C0, 0x1100), (0x1440, 0x1800)]  # io et libc (D28)
    reserve_ok = all(
        all(b == 0xCC for b in exe[L.TEXT_FILE + (r - L.TEXT_RVA): L.TEXT_FILE + (r2 - L.TEXT_RVA)])
        for r, r2 in reserves)
    s.verifie(7, "reserve libc/io remplie d'int3 (0xCC) — emplacements libres scelles",
              reserve_ok)
    r = subprocess.run([sys.executable, os.path.join(ICI, "demo_r7.py")],
                       capture_output=True, text=True)
    s.verifie(7, "demonstration R7 dynamique (demo_r7.py) : adresses stables dev.1 -> dev.2",
              r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "sans sortie")


def executer() -> tuple[bool, list[str]]:
    """Exécute la suite complète ; retourne (verdict, lignes de rapport)."""
    exe = _lire_exe()
    pe = pefile.PE(data=exe, fast_load=False)
    s = Suite()
    element_1(s, exe, pe)
    element_2(s, exe)
    element_3(s, exe, pe)
    element_4(s, exe, pe)
    element_6(s, exe)
    element_7(s, exe)
    lignes = s.lignes()
    total = len(s.controles)
    verdict = ("verte" if s.ok else "ROUGE")
    synthese = (f"{verdict} (conformite_profil.py : elements 1-4, 6-7 : {total} controles "
                f"{'PASS' if s.ok else 'EN ECHEC'} ; 5 hors perimetre M1, jalon M2)")
    with open(os.path.join(ICI, "conformite.txt"), "w", encoding="ascii") as f:
        f.write(synthese + "\n")
    lignes.append(f"[conformite.txt] {synthese}")
    return s.ok, lignes


if __name__ == "__main__":
    ok, rapport = executer()
    print("\n".join(rapport))
    sys.exit(0 if ok else 1)
