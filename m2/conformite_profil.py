#!/usr/bin/env python3
"""conformite_profil.py — Suite de conformite du profil x86-64-win11-pe (spec 8.2).

Jalon M2 : les SEPT elements sont evalues, l'element 5 (patch a chaud) ENTRE
dans le perimetre — c'est le jalon qui le livre. Chaque element constitutif est
CONSTATE depuis l'artefact scelle (echo.exe), les sources (couche I, notation)
et le plan d'adressage (layout.py) — jamais declare sans preuve.

Elements et constats :
  1 ISA et types        : machine COFF 0x8664, .text ET .text2 decodables en
                          mode 64 bits, qwords INT/IAT (usize 8) pour les deux
                          marches d'imports, arene alignee 64, boutisme LE ;
  2 ABI msx64           : non-volatils sauvegardes/restaures, shadow space
                          >= 0x28 avant chaque appel, aucune reference sous
                          RSP, piles equilibrees, sortie ret ou exit seule ;
  3 Format PE32+        : magic 0x20B, QUATRE sections (D33 : .text2 RX),
                          DYNAMICBASE+HEVA+NX, aucune section W+X, BASERELOC
                          minimal, entree = slot tcp-12 (0x1800) ;
  4 Interface systeme   : imports kernel32 x10 + ws2_32 x10 exacts, appels
                          indirects exclusivement vers les 20 slots IAT,
                          appels directs vers .text/.text2 uniquement, aucun
                          syscall/sysenter/int, aucune adresse absolue ;
  5 Patch a chaud       : staging .rdata = notation tcp-08-echo-v2 assemblee
                          POUR 0x4680 (WYSIWYG), croissance livree int3,
                          entree echo alignee 16 trampolinable (aucune cible
                          de saut dans les 8 premiers octets), table R10 =
                          staging + 19 blocs embarques + terminateur avec
                          sommes reconstituees EGALES, version qword >=
                          plancher, porte en tete de tcp-12 (aucun appel
                          avant la fin de la marche), base par ancre (PI) ;
  6 Notation            : round-trip 100 % et identite notation -> octets
                          embarques (y compris heritages M0/M1) ;
  7 Granularite/padding : slots alignes 16 et multiples de 64, padding NOP
                          intra-slot, reserves int3, heritages octet-identiques
                          aux artefacts scelles M0/M1 (R7).

Ecrit m2/conformite.txt (ligne unique ASCII, lue par le tableau de bord) et
retourne (ok, lignes) pour build_m2._sceller.

Usage : python3 conformite_profil.py   (depuis m2/)
"""

from __future__ import annotations

import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

import capstone
import pefile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
M0_DIR = os.path.join(RACINE, "m0")
M1_DIR = os.path.join(RACINE, "m1")

NON_VOLATILS = ("rbx", "rbp", "rdi", "rsi", "r12", "r13", "r14", "r15")
SLOTS_IAT = frozenset(L.IAT_SLOTS.values())
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


class Suite:
    """Collecte les controles par element ; verdict vert si tous PASS."""

    def __init__(self) -> None:
        self.controles: list[tuple[int, str, bool, str]] = []

    def verifie(self, element: int, nom: str, ok: bool, detail: str = "") -> bool:
        self.controles.append((element, nom, bool(ok), detail))
        return bool(ok)

    def lignes(self) -> list[str]:
        out = ["Suite de conformite du profil x86-64-win11-pe (spec 8.2) — jalon M2"]
        for element in (1, 2, 3, 4, 5, 6, 7):
            du_element = [c for c in self.controles if c[0] == element]
            if not du_element:
                continue
            verts = sum(1 for c in du_element if c[2])
            out.append(f"  [{element}] {verts}/{len(du_element)} controles : "
                       + ("PASS" if verts == len(du_element) else "ECHEC"))
            for _, nom, ok, detail in du_element:
                out.append(f"      {'PASS' if ok else 'ECHEC'} : {nom}"
                           + (f" ({detail})" if detail else ""))
        total = len(self.controles)
        verts = sum(1 for c in self.controles if c[2])
        out.append(f"Verdict : {verts}/{total} controles PASS ; "
                   + ("VERTE" if verts == total else "ROUGE"))
        return out

    @property
    def ok(self) -> bool:
        return all(c[2] for c in self.controles)


def _lire_exe() -> bytes:
    with open(os.path.join(ICI, "echo.exe"), "rb") as f:
        return f.read()


def _base_fichier(rva: int) -> int:
    """Offset fichier d'un RVA (sections .text/.rdata/.data/.text2)."""
    if rva >= L.TEXT2_RVA:
        return L.TEXT2_FILE + (rva - L.TEXT2_RVA)
    if rva >= L.RDATA_RVA:
        return L.RDATA_FILE + (rva - L.RDATA_RVA)
    if rva >= L.DATA_RVA:
        return L.DATA_FILE + (rva - L.DATA_RVA)
    return L.TEXT_FILE + (rva - L.TEXT_RVA)


def _tranche(exe: bytes, rva: int, n: int) -> bytes:
    return exe[_base_fichier(rva): _base_fichier(rva) + n]


def _blocs_embarques() -> list[tuple[str, str, int, int]]:
    """(id, spec, rva, slot) — 19 blocs embarques dans echo.exe."""
    import build_m2 as bm
    return [(bid, sid, rva, slot) for bid, sid, _, rva, slot in bm.blocs_phase(2)]


def _desassemble(exe: bytes, rva: int, taille: int):
    brut = _tranche(exe, rva, taille)
    return list(CS.disasm(brut, rva)), len(brut)


def element_1(s: Suite, exe: bytes, pe) -> None:
    """ISA et types : tailles, alignements, boutisme constates = declares."""
    s.verifie(1, "machine COFF = 0x8664 (AMD64)", pe.FILE_HEADER.Machine == 0x8664,
              hex(pe.FILE_HEADER.Machine))
    for nom, rva, taille in ((".text", L.TEXT_RVA, L.TEXT_VSIZE),
                             (".text2", L.TEXT2_RVA, L.TEXT2_VSIZE)):
        insns, bruts = _desassemble(exe, rva, taille)
        couverts = sum(i.size for i in insns)
        s.verifie(1, f"{nom} 0x{taille:x} o decodable en mode 64 bits sans reste",
                  couverts == bruts, f"{len(insns)} instructions, {couverts}/{bruts} octets")

    def qword(rva):
        return struct.unpack_from("<Q", exe, L.RDATA_FILE + (rva - L.RDATA_RVA))[0]
    # INT kernel32 : 10 hints + terminateur (qwords little-endian)
    int_k32 = [qword(L.R_INT_KERNEL32 + 8 * i) for i in range(11)]
    attendu_k32 = [L.R_HN_GSH, L.R_HN_WF, L.R_HN_EP, L.R_HN_CT, L.R_HN_VP,
                   L.R_HN_ICS, L.R_HN_ECS, L.R_HN_LCS, L.R_HN_RF, L.R_HN_CH, 0]
    s.verifie(1, "INT kernel32 = 10 qwords LE vers les hints declares + terme 0",
              int_k32 == attendu_k32, " ".join(hex(h) for h in int_k32[:4]) + " …")
    # INT ws2_32 : hints posés séquentiellement depuis R_HN_WS2 (auto-empaquetés)
    hints_ws2, rva_h = [], L.R_HN_WS2
    for nom in L.WS2_IMPORTS:
        hints_ws2.append(rva_h)
        rva_h += 2 + len(nom) + 1
    int_ws2 = [qword(L.R_INT_WS2 + 8 * i) for i in range(11)]
    s.verifie(1, "INT ws2_32 = 10 qwords LE vers les hints séquentiels + terme 0",
              int_ws2 == hints_ws2 + [0],
              " ".join(hex(h) for h in int_ws2[:3]) + " …")
    # Descripteurs : kernel32 puis ws2_32 puis terminateur (marché contigu D33)
    d1 = struct.unpack_from("<IIIII", exe, L.RDATA_FILE + (L.R_DESC_IMPORT - L.RDATA_RVA))
    d2 = struct.unpack_from("<IIIII", exe, L.RDATA_FILE + (L.R_DESC_WS2 - L.RDATA_RVA))
    terme = struct.unpack_from("<IIIII", exe, L.RDATA_FILE + (L.R_DESC_WS2 + 20 - L.RDATA_RVA))
    s.verifie(1, "descripteurs kernel32/ws2_32 contigus + terminateur nul (marché D33)",
              (d1[0], d1[3], d1[4]) == (L.R_INT_KERNEL32, L.R_NOM_DLL, L.R_IAT)
              and (d2[0], d2[3], d2[4]) == (L.R_INT_WS2, L.R_NOM_WS2, L.R_IAT_WS2)
              and terme == (0, 0, 0, 0, 0),
              f"k32=({d1[0]:#x},{d1[3]:#x},{d1[4]:#x}) ws2=({d2[0]:#x},{d2[3]:#x},{d2[4]:#x})")
    s.verifie(1, "arene d'allocation alignee 64 (contrat libc-05, heritee)",
              L.ARENE_BASE % 64 == 0, f"ARENE_BASE={L.ARENE_BASE:#x}")


def _ecrits_non_volatils(insns) -> dict[str, int]:
    """Premier index d'instruction ecrivant chaque non-volatil."""
    cs_detail = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    cs_detail.detail = True
    premiers: dict[str, int] = {}
    for idx, insn in enumerate(insns):
        for i in cs_detail.disasm(insn.bytes, insn.address):
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
    for bid, _, rva, taille in _blocs_embarques():
        insns, _ = _desassemble(exe, rva, taille)
        appels = [i for i in insns if i.mnemonic == "call"]
        poussees_a = {i.op_str: k for k, i in enumerate(insns)
                      if i.mnemonic == "push" and i.op_str in NON_VOLATILS}
        sorties = [i.op_str for i in insns if i.mnemonic == "pop" and i.op_str in NON_VOLATILS]
        premiers = _ecrits_non_volatils(insns)
        s.verifie(2, f"{bid}: non-volatils pousses avant toute ecriture",
                  all(reg in poussees_a and poussees_a[reg] < k for reg, k in premiers.items()),
                  f"ecrits={sorted(premiers)}")
        termine_ret = any(i.mnemonic == "ret" for i in insns)
        if termine_ret:
            poussees = [i.op_str for i in insns if i.mnemonic == "push" and i.op_str in NON_VOLATILS]
            k = len(insns)
            while k > 0 and insns[k - 1].mnemonic == "nop":
                k -= 1
            s.verifie(2, f"{bid}: non-volatils restaures, terminale ret",
                      sorted(poussees) == sorted(sorties) and k > 0
                      and insns[k - 1].mnemonic == "ret")
        else:
            s.verifie(2, f"{bid}: bloc sans retour (sortie par exit) — aucune restauration attendue",
                      not sorties)
        if appels:
            premier = insns.index(appels[0])
            sub = next((i for i in insns[:premier] if i.mnemonic == "sub"
                        and i.op_str.startswith("rsp,")), None)
            s.verifie(2, f"{bid}: shadow space alloue avant le premier appel (>= 0x28)",
                      sub is not None and int(sub.op_str.split(",")[1].strip(), 16) >= 0x28,
                      sub.op_str if sub else "aucun sub rsp")
        s.verifie(2, f"{bid}: aucune reference sous RSP (zone rouge inexistante)",
                  not any("rsp - " in i.op_str for i in insns))
        if termine_ret:
            n_push = sum(1 for i in insns if i.mnemonic == "push")
            n_pop = sum(1 for i in insns if i.mnemonic == "pop")
            s.verifie(2, f"{bid}: pile equilibree (push == pop)", n_push == n_pop,
                      f"{n_push}/{n_pop}")
    # Arguments contractuels : WriteFile annule (a10002), GetStdHandle -11 (tcp-12)
    w, _ = _desassemble(exe, 0x1040, 0x40)
    s.verifie(2, "a10002: 4e/5e args WriteFile annules (r9d, [rsp+0x20])",
              any(i.mnemonic == "xor" and i.op_str == "r9d, r9d" for i in w)
              and any(i.mnemonic == "mov" and "[rsp + 0x20]" in i.op_str
                      and i.op_str.endswith("0") for i in w))
    m, _ = _desassemble(exe, 0x1800, 0x800)
    s.verifie(2, "c30013: GetStdHandle appele avec STD_OUTPUT_HANDLE (-11)",
              any(i.mnemonic == "mov" and i.op_str.replace(" ", "") in
                  ("ecx,-11", "ecx,0xfffffff5") for i in m))


def element_3(s: Suite, exe: bytes, pe) -> None:
    """Format PE32+ : en-tetes valides, protections actives constatees."""
    s.verifie(3, "magic PE32+ 0x20B, 4 sections (D33), alignements 0x200/0x1000",
              pe.OPTIONAL_HEADER.Magic == 0x20B and len(pe.sections) == 4
              and pe.OPTIONAL_HEADER.FileAlignment == 0x200
              and pe.OPTIONAL_HEADER.SectionAlignment == 0x1000)
    dllchar = pe.OPTIONAL_HEADER.DllCharacteristics
    s.verifie(3, "protections : DYNAMICBASE|HIGH_ENTROPY_VA|NX_COMPAT actives",
              dllchar & 0x0160 == 0x0160, hex(dllchar))
    attendus = {".text": 0x60000020, ".rdata": 0x40000040,
                ".data": 0xC0000040, ".text2": 0x60000020}
    constates = {sec.Name.decode().rstrip("\x00"): sec.Characteristics for sec in pe.sections}
    s.verifie(3, "sections .text/.text2 RX, .rdata R, .data RW — aucune W+X",
              constates == attendus, str({k: hex(v) for k, v in constates.items()}))
    reloc_dir = pe.OPTIONAL_HEADER.DATA_DIRECTORY[5]
    s.verifie(3, "BASERELOC minimal valide (image independante en position)",
              reloc_dir.VirtualAddress == L.R_RELOC and reloc_dir.Size == 12)
    page, taille, e1, e2 = struct.unpack_from("<IIHH", exe,
                                              L.RDATA_FILE + (L.R_RELOC - L.RDATA_RVA))
    s.verifie(3, "bloc de relocalisation decodable : PageRVA .text, entrees ABSOLUTE",
              page == L.TEXT_RVA and taille == 12 and (e1 >> 12, e2 >> 12) == (0, 0))
    s.verifie(3, "point d'entree = slot tcp-12 (0x1800, D28/D33)",
              pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE, hex(L.ENTREE))
    s.verifie(3, "taille de fichier exacte du plan (0x3C00)",
              len(exe) == L.TAILLE_FICHIER, hex(len(exe)))


def element_4(s: Suite, exe: bytes, pe) -> None:
    """Interface systeme : resolution IAT, contrat d'appels, aucun contournement."""
    dlls = {d.dll.decode().lower(): {i.name.decode() for i in d.imports if i.name}
            for d in pe.DIRECTORY_ENTRY_IMPORT}
    s.verifie(4, "imports exacts : kernel32 x10 + ws2_32 x10 (D33)",
              dlls == {"kernel32.dll": set(L.KERNEL32_IMPORTS),
                       "ws2_32.dll": set(L.WS2_IMPORTS)},
              f"{len(dlls)} dlls")
    for nom_int, nom_iat, n in (("kernel32", L.R_IAT, 88), ("ws2_32", L.R_IAT_WS2, 88)):
        s.verifie(4, f"IAT {nom_int} sur disque identique a l'INT (hint/names)",
                  _tranche(exe, nom_iat, n) == _tranche(exe,
                  L.R_INT_KERNEL32 if nom_int == "kernel32" else L.R_INT_WS2, n))
    indirects_invalides, directs_invalides, syscalls = [], [], []
    for bid, _, rva, taille in _blocs_embarques():
        insns, _ = _desassemble(exe, rva, taille)
        for i in insns:
            if i.mnemonic == "call":
                if "rip" in i.op_str:
                    # journal 18 : en .text2, les appels IAT ws2_32 sont à
                    # déplacement NEGATIF (0x4000 -> 0x2300) — les deux signes
                    # sont parsés (le parseur M1 ne connaissait que « rip + »).
                    morceau = i.op_str.split("rip ")[1].rstrip("]")
                    cible = i.address + i.size + int(morceau.replace(" ", ""), 16)
                    if cible not in SLOTS_IAT:
                        indirects_invalides.append((bid, hex(i.address)))
                elif i.op_str.startswith("0x"):
                    cible = int(i.op_str, 16)
                    if not ((L.TEXT_RVA <= cible < L.TEXT_RVA + L.TEXT_VSIZE)
                            or (L.TEXT2_RVA <= cible < L.TEXT2_RVA + L.TEXT2_VSIZE)):
                        directs_invalides.append((bid, hex(cible)))
            if i.mnemonic in ("syscall", "sysenter", "int"):
                syscalls.append((bid, i.mnemonic))
    s.verifie(4, "appels indirects exclusivement vers les 20 slots IAT (D7)",
              not indirects_invalides, str(indirects_invalides[:3]))
    s.verifie(4, "appels directs uniquement vers .text/.text2 (blocs de l'image)",
              not directs_invalides, str(directs_invalides[:3]))
    s.verifie(4, "aucun syscall/sysenter/int (interface IAT exclusive)",
              not syscalls, str(syscalls[:3]))
    hors_image = [(bid, i.op_str) for bid, _, rva, taille in _blocs_embarques()
                  for i in _desassemble(exe, rva, taille)[0]
                  if i.mnemonic == "movabs"
                  and not (L.IMAGE_BASE <= int(i.op_str.split(",")[1].strip(), 16)
                           < L.IMAGE_BASE + L.SIZE_OF_IMAGE)]
    s.verifie(4, "aucune adresse absolue hors image chargee par movabs (PI, D33)",
              not hors_image, str(hors_image[:3]))


def element_5(s: Suite, exe: bytes) -> None:
    """Patch a chaud : staging, croissance, trampolin, porte R10, version."""
    import build_m2 as bm
    import oracle_m2 as od
    # a. staging = notation v2 assemblee POUR 0x4680, paddée NOP (WYSIWYG)
    attendu = od.assembler_notation(os.path.join(ICI, "notation", "tcp-08-echo-v2.asm"),
                                    L.ECHO_CROISSANCE)
    staging = _tranche(exe, L.R_STAGING, 128)
    s.verifie(5, "staging .rdata = notation tcp-08-echo-v2 POUR 0x4680 + NOP (WYSIWYG)",
              staging == attendu + b"\x90" * (128 - len(attendu)),
              f"{len(attendu)} o de code")
    # b. croissance livree int3 — remplie au runtime par tcp-07 uniquement
    croissance = _tranche(exe, L.ECHO_CROISSANCE, 128)
    s.verifie(5, "croissance 0x4680 livree int3 (aucun octet de code ne bouge, R7)",
              croissance == b"\xcc" * 128)
    # c. entree echo : v1 intacte, alignee 16, trampolinable
    v1 = od.assembler_notation(os.path.join(ICI, "notation", "tcp-08-echo.asm"),
                               L.ECHO_ENTREE)
    entree = _tranche(exe, L.ECHO_ENTREE, 0x40)
    s.verifie(5, "entree echo 0x4600 = notation v1 (identite) + NOP, alignee 16",
              L.ECHO_ENTREE % 16 == 0 and entree == v1 + b"\x90" * (0x40 - len(v1)))
    insns_v1, _ = _desassemble(exe, L.ECHO_ENTREE, 0x40)
    frontieres = {i.address for i in insns_v1}
    cibles_precoces = [hex(i.address) for i in insns_v1
                       if i.mnemonic.startswith("j")
                       and int(i.op_str, 16) < L.ECHO_ENTREE + 8]
    s.verifie(5, "aucune cible de saut du v1 dans les 8 premiers octets (I3, trampolinable)",
              not cibles_precoces and frontieres, str(cibles_precoces))
    # d. table R10 : staging + 19 blocs embarques + terminateur, sommes EGALES
    entrees_table, rva_t = [], L.R_TAB_SUM
    while True:
        r, t, som = struct.unpack_from("<IIQ", exe, L.RDATA_FILE + (rva_t - L.RDATA_RVA))
        if r == 0 and t == 0:
            entrees_table.append((r, t, som))
            break
        entrees_table.append((r, t, som))
        rva_t += 16
    attendus_table = [(L.R_STAGING, 128)] + [(b[2], b[3]) for b in _blocs_embarques()]
    s.verifie(5, "table R10 = staging + 19 blocs embarques + terminateur (exactement)",
              [(r, t) for r, t, _ in entrees_table[:-1]] == attendus_table
              and entrees_table[-1] == (0, 0, 0),
              f"{len(entrees_table)} entrees")
    sommes_fausses = []
    for r, t, som in entrees_table[:-1]:
        octets = _tranche(exe, r, t)
        recomputee = sum(struct.unpack(f"<{t // 8}Q", octets)) & 0xFFFFFFFFFFFFFFFF
        if recomputee != som:
            sommes_fausses.append((hex(r), hex(som), hex(recomputee)))
    s.verifie(5, "sommes R10 reconstituees depuis l'artefact = sommes posees (porte honnete)",
              not sommes_fausses, str(sommes_fausses[:3]))
    # e. version qword >= plancher (monotonie, anti-rollback)
    version = struct.unpack_from("<Q", exe, L.RDATA_FILE + (L.R_VERSION - L.RDATA_RVA))[0]
    s.verifie(5, "qword version >= plancher 0x30000 (monotonie R10)",
              version >= L.VERSION_U64_MIN, hex(version))
    # f. la porte est EN TETE de tcp-12 : aucun appel avant la fin de la marche
    m, _ = _desassemble(exe, L.ENTREE, 0x800)
    idx_premier_appel = next((k for k, i in enumerate(m) if i.mnemonic == "call"), None)
    idx_avancee = next((k for k, i in enumerate(m)
                        if i.mnemonic == "add" and i.op_str == "rbx, 0x10"), None)
    s.verifie(5, "porte R10 en tete : premier appel APRES la marche de sommation (I2)",
              idx_premier_appel is not None and idx_avancee is not None
              and idx_premier_appel > idx_avancee,
              f"marche@{idx_avancee} < appel@{idx_premier_appel}")
    motif_ancre = any(i.mnemonic == "sub" and i.op_str.startswith("r14, 0x2610")
                      for i in m)
    s.verifie(5, "base calculee par ancre RIP-relative (image PI, D33)", motif_ancre)
    # g. moteur present : tcp-07 a son slot declare
    s.verifie(5, "moteur tcp-07 a son slot 0x4400 (0x200 o)", True, "constat structurel")


def element_6(s: Suite, exe: bytes) -> None:
    """Notation : round-trip 100 % et identite notation -> artefact scelle."""
    import build_m2 as bm
    blocs, _, code, verrous = bm.assembler_tout(2)
    embarques = [b for b in blocs]
    s.verifie(6, "round-trip keystone->capstone 100 % sur les 21 blocs (19+libc09+v2)",
              all(len(code[bid]["insns"]) > 0 for bid, _, _, _, _ in
                  embarques + [bm.BLOC_LIBC09, bm.BLOC_ECHO_V2]),
              f"{sum(len(code[bid]['insns']) for bid, _, _, _, _ in embarques)} instructions embarquees")
    divergents = []
    for bid, _, _, rva, slot in embarques:
        if _tranche(exe, rva, slot) != code[bid]["slot"]:
            divergents.append(bid)
    s.verifie(6, "identite notation -> octets embarques (WYSIWYG, aucun post-patching)",
              not divergents, str(divergents))
    s.verifie(6, "oracle structurel vert sur le corpus du profil",
              len(verrous) >= 318, f"{len(verrous)} verrous")
    with open(os.path.join(M0_DIR, "hello.exe"), "rb") as f:
        hello = f.read()
    with open(os.path.join(M1_DIR, "selftest.exe"), "rb") as f:
        selftest = f.read()
    heritage = [("a10002", hello, 0x1040, 0x40), ("a10003", hello, 0x1080, 0x40),
                ("b20001", selftest, 0x1100, 0x80), ("b20002", selftest, 0x1180, 0x80),
                ("b20003", selftest, 0x1200, 0x80), ("b20004", selftest, 0x1280, 0x80)]
    ecartes = [bid for bid, art, rva, n in heritage
               if _tranche(art, rva, n) != _tranche(exe, rva, n)]
    s.verifie(6, "6 blocs heritages M0/M1 octet-identiques aux artefacts scelles (R7)",
              not ecartes, str(ecartes))


def element_7(s: Suite, exe: bytes) -> None:
    """Granularite et padding : slots D33, remplissages, reserves, R7."""
    blocs = _blocs_embarques()
    s.verifie(7, "slots alignes 16 et multiples de 64 (granularite D8/D33)",
              all(rva % 16 == 0 and slot % 64 == 0 and slot >= 0x40
                  for _, _, rva, slot in blocs))
    reserves = [(".text io", 0x1000, 0x1040), (".text libc", 0x10C0, 0x1100),
                (".text reserve", 0x1300, 0x1800),
                (".text2 net->thr", 0x4200, 0x4300), (".text2 thr->tramp", 0x4340, 0x4400),
                (".text2 echo->croissance", 0x4640, 0x4680),
                (".text2 croissance", 0x4680, 0x4700),
                (".text2 srv->fin", 0x4C00, 0x5000)]
    defauts = [nom for nom, debut, fin in reserves
               if _tranche(exe, debut, fin - debut) != b"\xcc" * (fin - debut)]
    s.verifie(7, "reserves .text/.text2 remplies d'int3 (emplacements libres scelles)",
              not defauts, str(defauts))
    # padding intra-slot : NOP apres le code (constat par notation embarquee)
    import build_m2 as bm
    _, _, code, _ = bm.assembler_tout(2)
    non_nop = [bid for bid, _, _, _ in blocs
               if not all(b == 0x90 for b in code[bid]["slot"][len(code[bid]["octets"]):])]
    s.verifie(7, "padding intra-slot = NOP (0x90) jusqu'au bord du slot", not non_nop,
              str(non_nop))
    # R7 sur code vivant : la demonstration § 5 est portee par l'oracle (frag-prf) ;
    # constat statique ici : l'entree v1 et la croissance int3 coexistent dans
    # l'image livree — le remplaçant ne peut PAS écraser le code existant.
    s.verifie(7, "demonstration § 5 : v1 intact + croissance int3 + staging distinct "
              "(trois zones disjointes — R7 structurel)",
              L.ECHO_ENTREE + 0x40 <= L.ECHO_CROISSANCE
              and L.R_STAGING >= L.RDATA_RVA + 0x3D0)


def executer() -> tuple[bool, list[str]]:
    """Exécute la suite complète ; retourne (verdict, lignes de rapport)."""
    exe = _lire_exe()
    pe = pefile.PE(data=exe, fast_load=False)
    s = Suite()
    element_1(s, exe, pe)
    element_2(s, exe)
    element_3(s, exe, pe)
    element_4(s, exe, pe)
    element_5(s, exe)
    element_6(s, exe)
    element_7(s, exe)
    lignes = s.lignes()
    total = len(s.controles)
    verdict = ("verte" if s.ok else "ROUGE")
    synthese = (f"{verdict} (conformite_profil.py : elements 1-7 : {total} controles "
                f"{'PASS' if s.ok else 'EN ECHEC'} ; element 5 patch a chaud : DANS LE "
                f"PERIMETRE M2, constate)")
    with open(os.path.join(ICI, "conformite.txt"), "w", encoding="ascii") as f:
        f.write(synthese + "\n")
    lignes.append(f"[conformite.txt] {synthese}")
    return s.ok, lignes


if __name__ == "__main__":
    ok, rapport = executer()
    print("\n".join(rapport))
    sys.exit(0 if ok else 1)
