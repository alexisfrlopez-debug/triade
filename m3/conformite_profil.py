#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""conformite_profil.py — Suite de conformité du profil x86-64-win11-pe (spec 8.2).

Jalon M3, étape (e) (D73) : le fuzzing à propriétés REJOINT la suite de
conformité. Le harnais de la campagne million (m3/fuzz_million.py, D72 —
falsifiable, 2×10^6 cas sans crash) devient CONTRÔLE PERMANENT : chaque
passage de la suite exécute une campagne réduite (~10^4 cas, graine datée
donc reproductible, auto-test de falsification inclus) sur le périmètre D46
(http-01..09 + accumulation http-10). La spec 8.2 exige la suite « à chaque
cristallisation de version rc et finale (§ 9) » ; le critère quantitatif de
jalon (« un million de requêtes fuzzées sans crash ») reste démontré par la
campagne D72 — la suite en est la sentinelle perpétuelle : toute régression
d'un bloc du périmètre, à n'importe quelle cristallisation future, rend la
suite ROUGE.

Les SEPT éléments constitutifs sont constatés depuis l'artefact scellé
(proxy.exe 0.4.0-dev.2), les sources (couche I, notations) et le plan
d'adressage (layout.py) — jamais déclarés sans preuve. L'élément 5 (patch à
chaud) est PARTAGÉ : la porte R10 est constatée VIVANTE (table, sommes,
version, ancre, tête de http-12) ; le moteur de patch (tcp-07, staging,
croissance) n'est pas embarqué à ce jalon (M5, layout D46) — rapporté.

Éléments et constats :
  1 ISA et types        : machine COFF 0x8664, .text et .text2 décodables en
                          mode 64 bits sans reste, INT kernel32 = 10 qwords
                          LE vers les hints déclarés, INT ws2_32 = 13 qwords
                          LE vers les hints séquentiels (3 appendus M3 :
                          getaddrinfo/freeaddrinfo/connect), descripteurs
                          contigus + terminateur nul, arène alignée 64 ;
  2 ABI msx64           : non-volatils poussés avant toute première écriture
                          (premier push — les blocs multi-entrées poussent
                          chacun leur série, http-10:Q0/I5), aucun pop sans
                          push préalable, terminaison ret/exit, shadow space
                          >= 0x28 avant le premier appel EXTERNE (les
                          assistants internes d'une feuille — http-07 — ne
                          traversent pas la frontière ABI, journal 36/37),
                          aucun STOCKAGE sous RSP (les sondes de pile
                          http-10:R3/D63 sont des LECTURES de pages de
                          garde, constatées) ; l'équilibre dynamique des
                          blocs multi-sorties relève de la preuve P2
                          (sentinelle — oracle différentiel, re-vérifié par
                          le contrôle de jalon (e)) ; args contractuels
                          (WriteFile annulé, GetStdHandle -11) ;
  3 Format PE32+        : magic 0x20B, QUATRE sections (D33 : .text2 RX),
                          DYNAMICBASE+HEVA+NX, aucune section W+X, BASERELOC
                          minimal, entrée = slot http-12 (0x1800), taille
                          exacte du plan (0x4C00) ;
  4 Interface système   : imports kernel32 x10 + ws2_32 x13 exacts, IAT
                          identique à l'INT sur disque, appels indirects
                          exclusivement vers les 23 slots IAT, appels directs
                          vers .text/.text2 uniquement, aucun
                          syscall/sysenter/int, movabs = constantes du
                          contrat uniquement (http-02:Q4 littéraux « HTTP/1.x »
                          par 8 octets, http-05:Q5 borne u32) — aucune valeur
                          dans la fenêtre d'adresses de l'image (PI) ;
  5 Patch à chaud       : porte R10 — table = 26 blocs embarqués +
                          terminateur, sommes reconstituées depuis l'artefact
                          ÉGALES aux sommes posées, version qword >= plancher
                          0x00040000 (monotonie), base calculée par ancre
                          RIP-relative, marche de sommation AVANT le premier
                          appel de http-12 ; moteur de patch hors périmètre
                          M3 (jalon M5) — non évalué, rapporté ;
  6 Notation            : round-trip keystone->capstone 100 % et identité
                          notation -> octets embarqués (WYSIWYG, 26 blocs),
                          oracle structurel vert, 13 héritages M0/M1/M2
                          octet-identiques aux artefacts scellés ;
  7 Granularité/padding : slots alignés 16 et multiples de 64, padding NOP
                          intra-slot, réserves int3 (bornes constatées :
                          .text 0x1000-0x1040/0x10C0-0x1100/0x1300-0x1800/
                          0x1C80-0x2000, .text2 0x4200-0x4300/0x4340-0x4400/
                          0x45C0-0x4B00/0x5E80-0x6000), héritages aux RVA
                          historiques exacts (R7) ;
  [M3] Contrôle de jalon (étape (e)) — fuzzing à propriétés : campagne
                          réduite du harnais m3/fuzz_million.py (volet
                          feuilles différentiel http-01..09 + accumulation
                          http-10 P1-P5, sentinelles tournantes, auto-test
                          de falsification M1/M2) — PASS si zéro échec
                          confirmé, zéro échec non reproductible et harnais
                          falsifiable.

Écrit m3/conformite.txt (ligne unique ASCII, lue par le tableau de bord) et
retourne (ok, lignes) — même contrat que m1/m2 pour le scellage rc (§ 9 :
« dev + suite de conformité du profil verte + critères du jalon courant »).

Usage :
  python3 conformite_profil.py                     # 10^4 cas, graine du jour
  python3 conformite_profil.py --graine 20261030   # graine imposée (rejeu)
  python3 conformite_profil.py --cas 100000 --accum 10000
"""

from __future__ import annotations

import argparse
import os
import struct
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

import capstone
import pefile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

NON_VOLATILS = ("rbx", "rbp", "rdi", "rsi", "r12", "r13", "r14", "r15")
SLOTS_IAT = frozenset(L.IAT_SLOTS.values())
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

HINTS_K32 = {"GetStdHandle": L.R_HN_GSH, "WriteFile": L.R_HN_WF, "ExitProcess": L.R_HN_EP,
             "CreateThread": L.R_HN_CT, "VirtualProtect": L.R_HN_VP,
             "InitializeCriticalSection": L.R_HN_ICS, "EnterCriticalSection": L.R_HN_ECS,
             "LeaveCriticalSection": L.R_HN_LCS, "ReadFile": L.R_HN_RF,
             "CloseHandle": L.R_HN_CH}
# Héritage R7 : l'octet de chaque bloc a1/b2/c3 vit dans l'artefact scellé
# d'origine, à son RVA historique (.text file 0x200 pour tous ; .text2 file
# 0x2C00 pour echo.exe — plans m0/m1/m2).
ARTIFACTS_HERITAGE = {"a1": ("m0", "hello.exe"), "b2": ("m1", "selftest.exe"),
                      "c3": ("m2", "echo.exe")}


class Suite:
    """Collecte les controles par element ; verdict vert si tous PASS.

    Les elements 1-7 suivent la spec 8.2 (D22) ; l'element 8 est le controle
    de jalon M3 (etape (e) : fuzzing a proprietes) — affiche sous l'etiquette
    [M3], distinct des sept elements constitutifs du profil.
    """

    def __init__(self) -> None:
        self.controles: list[tuple[int, str, bool, str]] = []

    def verifie(self, element: int, nom: str, ok: bool, detail: str = "") -> bool:
        self.controles.append((element, nom, bool(ok), detail))
        return bool(ok)

    def lignes(self) -> list[str]:
        out = ["Suite de conformite du profil x86-64-win11-pe (spec 8.2) — jalon M3"]
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
        du_jalon = [c for c in self.controles if c[0] == 8]
        if du_jalon:
            verts = sum(1 for c in du_jalon if c[2])
            out.append("  [M3] controle de jalon (etape (e)) — fuzzing a proprietes : "
                       + ("PASS" if verts == len(du_jalon) else "ECHEC")
                       + f" ({verts}/{len(du_jalon)})")
            for _, nom, ok, detail in du_jalon:
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
    with open(os.path.join(ICI, "proxy.exe"), "rb") as f:
        return f.read()


def _base_fichier(rva: int) -> int:
    """Offset fichier d'un RVA (sections .text/.rdata/.data/.text2, plan M3)."""
    if rva >= L.TEXT2_RVA:
        return L.TEXT2_FILE + (rva - L.TEXT2_RVA)
    if rva >= L.DATA_RVA:
        return L.DATA_FILE + (rva - L.DATA_RVA)
    if rva >= L.RDATA_RVA:
        return L.RDATA_FILE + (rva - L.RDATA_RVA)
    return L.TEXT_FILE + (rva - L.TEXT_RVA)


def _tranche(exe: bytes, rva: int, n: int) -> bytes:
    return exe[_base_fichier(rva): _base_fichier(rva) + n]


def _blocs_embarques() -> list[tuple[str, str, int, int]]:
    """(id, spec, rva, slot) — 26 blocs embarqués dans proxy.exe."""
    import build_m3 as bm
    return [(bid, sid, rva, slot) for bid, sid, _, rva, slot in bm.blocs_embarques()]


def _desassemble(exe: bytes, rva: int, taille: int):
    brut = _tranche(exe, rva, taille)
    return list(CS.disasm(brut, rva)), len(brut)


_ASSEMBLER_CACHE = None


def _assembler_tout():
    """assembler_tout() mémoisé — l'assemblage keystone ne tourne qu'une fois."""
    global _ASSEMBLER_CACHE
    if _ASSEMBLER_CACHE is None:
        import build_m3 as bm
        _ASSEMBLER_CACHE = bm.assembler_tout()
    return _ASSEMBLER_CACHE


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
        return struct.unpack_from("<Q", exe, _base_fichier(rva))[0]
    # INT kernel32 : 10 hints + terminateur (qwords little-endian, ordre figé)
    int_k32 = [qword(L.R_INT_KERNEL32 + 8 * i) for i in range(11)]
    attendu_k32 = [HINTS_K32[n] for n in L.KERNEL32_IMPORTS] + [0]
    s.verifie(1, "INT kernel32 = 10 qwords LE vers les hints declares + terme 0",
              int_k32 == attendu_k32, " ".join(hex(h) for h in int_k32[:4]) + " …")
    # INT ws2_32 : hints posés séquentiellement depuis R_HN_WS2 (10 hérités +
    # 3 appendés M3 : getaddrinfo, freeaddrinfo, connect — arrêt b D46)
    hints_ws2, rva_h = [], L.R_HN_WS2
    for nom in L.WS2_IMPORTS:
        hints_ws2.append(rva_h)
        rva_h += 2 + len(nom) + 1
    int_ws2 = [qword(L.R_INT_WS2 + 8 * i) for i in range(14)]
    s.verifie(1, "INT ws2_32 = 13 qwords LE vers les hints sequentiels + terme 0",
              int_ws2 == hints_ws2 + [0],
              " ".join(hex(h) for h in int_ws2[:3]) + " … "
              + " ".join(hex(h) for h in int_ws2[10:13]))
    # Descripteurs : kernel32 puis ws2_32 puis terminateur (marché contigu)
    d1 = struct.unpack_from("<IIIII", exe, _base_fichier(L.R_DESC_IMPORT))
    d2 = struct.unpack_from("<IIIII", exe, _base_fichier(L.R_DESC_WS2))
    terme = struct.unpack_from("<IIIII", exe, _base_fichier(L.R_DESC_WS2 + 20))
    s.verifie(1, "descripteurs kernel32/ws2_32 contigus + terminateur nul",
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
    """ABI msx64 : volatilite, shadow space, zone rouge, discipline de pile.

    Norme M3 (miroir de l'oracle structurel du build — journal 36/37) :
    la shadow space s'impose aux appels EXTERNES seuls (les assistants
    internes d'une feuille ne traversent pas la frontière ABI) ; aucun
    STOCKAGE sous RSP (les sondes de pile http-10:R3/D63 sont des LECTURES
    de pages de garde, licites — constatées ci-dessous) ; l'équilibre des
    blocs multi-sorties (http-07 : assistant à deux sorties) et
    multi-entrées (http-10 : session + thread tunnel + pompe, I5/D63)
    relève de la preuve DYNAMIQUE — P2, retour à la sentinelle de l'oracle
    différentiel, re-vérifié à chaque passage par le contrôle de jalon (e).
    La suite constate ici la discipline STATIQUE : premier push avant
    première écriture, aucun pop sans push, terminaison ret/exit.
    """
    for bid, _, rva, taille in _blocs_embarques():
        insns, _ = _desassemble(exe, rva, taille)
        # a. non-volatils : PREMIER push (min) avant première écriture — les
        #    blocs multi-entrées poussent chacun leur série ; l'ordre
        #    programme du premier push domine toute écriture du registre.
        premiers_ecrits = _ecrits_non_volatils(insns)
        premier_push: dict[str, int] = {}
        for k, i in enumerate(insns):
            if i.mnemonic == "push" and i.op_str in NON_VOLATILS \
                    and i.op_str not in premier_push:
                premier_push[i.op_str] = k
        s.verifie(2, f"{bid}: non-volatils pousses avant premiere ecriture (premier push)",
                  all(reg in premier_push and premier_push[reg] < k
                      for reg, k in premiers_ecrits.items()),
                  f"ecrits={sorted(premiers_ecrits)}")
        # b. discipline de pile : aucun pop de non-volatil sans push préalable
        vus: set[str] = set()
        pop_sans_push = []
        for i in insns:
            if i.mnemonic == "push" and i.op_str in NON_VOLATILS:
                vus.add(i.op_str)
            elif i.mnemonic == "pop" and i.op_str in NON_VOLATILS \
                    and i.op_str not in vus:
                pop_sans_push.append(i.op_str)
        s.verifie(2, f"{bid}: aucun pop de non-volatil sans push prealable",
                  not pop_sans_push, str(pop_sans_push))
        # c. terminaison : ret terminale (bloc retournant) ou exit sans pop
        termine_ret = any(i.mnemonic == "ret" for i in insns)
        if termine_ret:
            k = len(insns)
            while k > 0 and insns[k - 1].mnemonic == "nop":
                k -= 1
            s.verifie(2, f"{bid}: terminale ret (bloc retournant)",
                      k > 0 and insns[k - 1].mnemonic == "ret")
        else:
            sorties = [i.op_str for i in insns
                       if i.mnemonic == "pop" and i.op_str in NON_VOLATILS]
            s.verifie(2, f"{bid}: bloc sans retour (sortie par exit) — aucune restauration attendue",
                      not sorties)
        # d. shadow space : avant le premier appel EXTERNE uniquement — les
        #    assistants internes (cible dans le slot du bloc) ne traversent
        #    pas la frontière ABI (miroir oracle structurel « pile alignée »)
        externes = []
        for i in insns:
            if i.mnemonic != "call":
                continue
            if "rip" in i.op_str:
                externes.append(i)              # IAT : toujours externe
            elif i.op_str.startswith("0x"):
                cible = int(i.op_str, 16)
                if not (rva <= cible < rva + taille):
                    externes.append(i)          # appel direct à un autre bloc
        if externes:
            premier = insns.index(externes[0])
            sub = next((i for i in insns[:premier] if i.mnemonic == "sub"
                        and i.op_str.startswith("rsp,")), None)
            s.verifie(2, f"{bid}: shadow space alloue avant le premier appel externe (>= 0x28)",
                      sub is not None and int(sub.op_str.split(",")[1].strip(), 16) >= 0x28,
                      sub.op_str if sub else "aucun sub rsp")
        # e. zone rouge msx64 : aucun STOCKAGE sous RSP (mov destination
        #    mémoire, base rsp, déplacement négatif) — plus strict que le
        #    garde-fou du build (qui ne parse que « + disp ») ; les LECTURES
        #    sous RSP (sondes D63) sont licites et constatées ci-dessous
        stockages = [(hex(i.address), i.op_str.split(",")[0].strip()) for i in insns
                     if i.mnemonic.startswith("mov") and "," in i.op_str
                     and i.op_str.split(",")[0].strip().endswith("]")
                     and "rsp - " in i.op_str.split(",")[0]]
        s.verifie(2, f"{bid}: aucun stockage sous RSP (zone interdite msx64)",
                  not stockages, str(stockages[:3]))
    # --- constats M3 documentés (couche I / D63 / journal 36-37) ----------
    blocs = {bid: (rva, taille) for bid, _, rva, taille in _blocs_embarques()}
    # http-07 : feuille à assistant interne (deux sorties, pop rbx chacune)
    rva07, taille07 = blocs["e50007"]
    i07, _ = _desassemble(exe, rva07, taille07)
    internes07 = [i for i in i07 if i.mnemonic == "call" and i.op_str.startswith("0x")
                  and rva07 <= int(i.op_str, 16) < rva07 + taille07]
    externes07 = [i for i in i07 if i.mnemonic == "call" and (
        "rip" in i.op_str or (i.op_str.startswith("0x")
                              and not (rva07 <= int(i.op_str, 16) < rva07 + taille07)))]
    s.verifie(2, "e50007: feuille a assistant interne (appels au slot seul, frontiere ABI non traversee)",
              bool(internes07) and not externes07,
              f"{len(internes07)} appel(s) interne(s), {len(externes07)} externe(s)")
    # http-10 : sondes de pile http-10:R3 (D63) — LECTURES sous RSP des
    # pages de garde AVANT le grand sub rsp, 0x7100 (Q0 de la spécification)
    rva10, taille10 = blocs["e50010"]
    i10, _ = _desassemble(exe, rva10, taille10)
    lectures_sonde = [i for i in i10 if i.mnemonic == "mov"
                      and i.op_str.startswith("rax, ") and "rsp" in i.op_str
                      and ("rsp - " in i.op_str or "rsp + r10" in i.op_str)]
    motif_r10 = any(i.mnemonic == "mov"
                    and i.op_str.replace(" ", "") == "r10,0xfffffffffffff000" for i in i10)
    s.verifie(2, "e50010: sondes de pile D63 = LECTURES sous RSP (pages de garde), r10 negatif",
              len(lectures_sonde) >= 2 and motif_r10,
              f"{len(lectures_sonde)} lectures de sonde + boucle r10")
    # Arguments contractuels : WriteFile annule (a10002, heritage M0) ;
    # GetStdHandle STD_OUTPUT_HANDLE dans l'orchestrateur http-12 (e50012)
    w, _ = _desassemble(exe, 0x1040, 0x40)
    s.verifie(2, "a10002: 4e/5e args WriteFile annules (r9d, [rsp+0x20])",
              any(i.mnemonic == "xor" and i.op_str == "r9d, r9d" for i in w)
              and any(i.mnemonic == "mov" and "[rsp + 0x20]" in i.op_str
                      and i.op_str.endswith("0") for i in w))
    m, _ = _desassemble(exe, L.ENTREE, 0x480)
    s.verifie(2, "e50012: GetStdHandle appele avec STD_OUTPUT_HANDLE (-11)",
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
    page, taille, e1, e2 = struct.unpack_from("<IIHH", exe, _base_fichier(L.R_RELOC))
    s.verifie(3, "bloc de relocalisation decodable : PageRVA .text, entrees ABSOLUTE",
              page == L.TEXT_RVA and taille == 12 and (e1 >> 12, e2 >> 12) == (0, 0))
    s.verifie(3, "point d'entree = slot http-12 (0x1800, D46)",
              pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE, hex(L.ENTREE))
    s.verifie(3, "taille de fichier exacte du plan (0x4C00)",
              len(exe) == L.TAILLE_FICHIER, hex(len(exe)))


def element_4(s: Suite, exe: bytes, pe) -> None:
    """Interface systeme : resolution IAT, contrat d'appels, aucun contournement."""
    dlls = {d.dll.decode().lower(): {i.name.decode() for i in d.imports if i.name}
            for d in pe.DIRECTORY_ENTRY_IMPORT}
    s.verifie(4, "imports exacts : kernel32 x10 + ws2_32 x13 (D46, connect appendu)",
              dlls == {"kernel32.dll": set(L.KERNEL32_IMPORTS),
                       "ws2_32.dll": set(L.WS2_IMPORTS)},
              f"{len(dlls)} dlls, {sum(len(v) for v in dlls.values())} fonctions")
    for nom, int_rva, iat_rva, n in (("kernel32", L.R_INT_KERNEL32, L.R_IAT, 88),
                                     ("ws2_32", L.R_INT_WS2, L.R_IAT_WS2, 112)):
        s.verifie(4, f"IAT {nom} sur disque identique a l'INT (hint/names)",
                  _tranche(exe, iat_rva, n) == _tranche(exe, int_rva, n))
    # Appels : indirects -> slots IAT uniquement (les DEUX signes de
    # déplacement RIP — journal 18 : en .text2 les appels ws2_32 hérités sont
    # à déplacement négatif) ; directs -> .text/.text2 uniquement.
    indirects_invalides, directs_invalides, syscalls = [], [], []
    for bid, _, rva, taille in _blocs_embarques():
        insns, _ = _desassemble(exe, rva, taille)
        for i in insns:
            if i.mnemonic == "call":
                if "rip" in i.op_str:
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
    s.verifie(4, "appels indirects exclusivement vers les 23 slots IAT (D7/D46)",
              not indirects_invalides, str(indirects_invalides[:3]))
    s.verifie(4, "appels directs uniquement vers .text/.text2 (blocs de l'image)",
              not directs_invalides, str(directs_invalides[:3]))
    s.verifie(4, "aucun syscall/sysenter/int (interface IAT exclusive)",
              not syscalls, str(syscalls[:3]))
    # movabs : constantes du contrat uniquement — http-02:Q4 compare les
    # littéraux « HTTP/1.0 »/« HTTP/1.1 » par mots de 8 octets (immédiats
    # ASCII > 2^48, hors fenêtre canonique d'adresses par construction) ;
    # http-05:Q5 porte la borne u32 0xFFFFFFFF. AUCUNE valeur dans la
    # fenêtre d'adresses de l'image — une adresse absolue casserait la
    # position-indépendance (base par ancre, D33/D46).
    valeurs_movabs: dict[int, list[str]] = {}
    for bid, _, rva, taille in _blocs_embarques():
        for i in _desassemble(exe, rva, taille)[0]:
            if i.mnemonic == "movabs":
                valeurs_movabs.setdefault(
                    int(i.op_str.split(",")[1].strip(), 16), []).append(bid)
    fenetre_image = [hex(v) for v in valeurs_movabs
                     if L.IMAGE_BASE <= v < L.IMAGE_BASE + L.SIZE_OF_IMAGE]
    s.verifie(4, "aucune movabs dans la fenetre d'adresses de l'image (PI par ancre)",
              not fenetre_image, str(fenetre_image))
    hors_contrat = [(hex(v), valeurs_movabs[v]) for v in valeurs_movabs
                    if not (v > 0x7FFFFFFFFFFF or v == 0xFFFFFFFF or v < 0x10000)]
    s.verifie(4, "movabs = constantes du contrat (litteraux HTTP/1.x http-02:Q4, borne u32 http-05:Q5)",
              not hors_contrat,
              f"{len(valeurs_movabs)} immediats : "
              + ", ".join(f"{hex(v)}->{valeurs_movabs[v][0]}" for v in sorted(valeurs_movabs)))


def element_5(s: Suite, exe: bytes) -> None:
    """Patch a chaud (perimetre M3) : porte R10 constatee ; moteur rapporte.

    La porte R10 est VIVANTE dans proxy.exe : http-12 la franchit au
    demarrage (marche de sommation avant tout appel — integrite KO = arret).
    Le moteur de patch (tcp-07, staging, croissance) n'est PAS embarque a ce
    jalon (layout D46 : « le patch a chaud revient au jalon M5 ») — rapporte,
    non evalue, exactement comme l'element 5 l'etait au jalon M1.
    """
    # a. table R10 : 26 blocs embarques + terminateur, dans l'ordre du build
    entrees_table, rva_t = [], L.R_TAB_SUM
    while True:
        r, t, som = struct.unpack_from("<IIQ", exe, _base_fichier(rva_t))
        entrees_table.append((r, t, som))
        if r == 0 and t == 0:
            break
        rva_t += 16
        if len(entrees_table) > 40:
            s.verifie(5, "table R10 bornée (terminateur atteint)", False,
                      f"{len(entrees_table)} entrées sans terme")
            return
    attendus_table = [(rva, slot) for _, _, rva, slot in _blocs_embarques()]
    s.verifie(5, "table R10 = 26 blocs embarques + terminateur (exactement)",
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
    # b. version qword >= plancher (monotonie, anti-rollback)
    version = struct.unpack_from("<Q", exe, _base_fichier(L.R_VERSION))[0]
    s.verifie(5, "qword version >= plancher 0x00040000 (monotonie R10)",
              version >= L.VERSION_U64_MIN, hex(version))
    # c. la porte est EN TETE de http-12 : aucun appel avant la fin de la marche
    m, _ = _desassemble(exe, L.ENTREE, 0x480)
    idx_premier_appel = next((k for k, i in enumerate(m) if i.mnemonic == "call"), None)
    idx_avancee = next((k for k, i in enumerate(m)
                        if i.mnemonic == "add" and i.op_str == "rbx, 0x10"), None)
    s.verifie(5, "porte R10 en tete : premier appel APRES la marche de sommation (I2)",
              idx_premier_appel is not None and idx_avancee is not None
              and idx_premier_appel > idx_avancee,
              f"marche@{idx_avancee} < appel@{idx_premier_appel}")
    motif_ancre = any(i.mnemonic == "sub" and i.op_str.startswith(f"r14, {L.R_ANCRE:#x}")
                      for i in m)
    s.verifie(5, "base calculee par ancre RIP-relative (image PI, D33/D46)", motif_ancre)
    # d. moteur de patch : hors perimetre M3 — rapporte (jalon M5)
    s.verifie(5, "moteur de patch hors perimetre M3 (tcp-07 non embarque, jalon M5) — rapporte",
              True, "constat de plan (layout D46) ; zones tramp/echo/tcp-09/10 = int3")


def element_6(s: Suite, exe: bytes) -> None:
    """Notation : round-trip 100 % et identite notation -> artefact scelle."""
    try:
        blocs, _, code, verrous = _assembler_tout()
    except Exception as exc:                     # EchecBuild — fail-closed
        s.verifie(6, "assemblage + oracle structurel (build_m3.assembler_tout)", False, str(exc))
        return
    embarques = _blocs_embarques()
    s.verifie(6, "round-trip keystone->capstone 100 % sur les 26 blocs embarques",
              all(len(code[bid]["insns"]) > 0 for bid, _, _, _ in embarques),
              f"{sum(len(code[bid]['insns']) for bid, _, _, _ in embarques)} instructions")
    divergents = []
    for bid, _, rva, slot in embarques:
        if _tranche(exe, rva, slot) != code[bid]["slot"]:
            divergents.append(bid)
    s.verifie(6, "identite notation -> octets embarques (WYSIWYG, aucun post-patching)",
              not divergents, str(divergents))
    s.verifie(6, "oracle structurel vert sur le corpus du profil",
              len(verrous) >= 500, f"{len(verrous)} verrous")
    # Heritages R7 : 13 blocs octet-identiques aux artefacts scelles
    heritages = []
    for bid, _, rva, slot in embarques:
        rep = ARTIFACTS_HERITAGE.get(bid[:2])
        if rep:
            with open(os.path.join(RACINE, rep[0], rep[1]), "rb") as f:
                art = f.read()
            if rva >= L.TEXT2_RVA:
                tranche_art = art[0x2C00 + (rva - 0x4000): 0x2C00 + (rva - 0x4000) + slot]
            else:
                tranche_art = art[0x200 + (rva - 0x1000): 0x200 + (rva - 0x1000) + slot]
            heritages.append((bid, tranche_art == _tranche(exe, rva, slot)))
    ecartes = [bid for bid, identique in heritages if not identique]
    s.verifie(6, "13 blocs heritages M0/M1/M2 octet-identiques aux artefacts scelles (R7)",
              not ecartes and len(heritages) == 13, str(ecartes))


def element_7(s: Suite, exe: bytes) -> None:
    """Granularite et padding : slots, remplissages, reserves, R7."""
    blocs = _blocs_embarques()
    s.verifie(7, "slots alignes 16 et multiples de 64 (granularite D8/D46)",
              all(rva % 16 == 0 and slot % 64 == 0 and slot >= 0x40
                  for _, _, rva, slot in blocs))
    # Reserves int3 — bornes constatees depuis l'artefact (le trou net
    # 0x4200, le reste tramp+echo M2 0x45C0-0x4B00, tcp-09/10 inclus, et la
    # fin de zone http 0x5E80-0x6000 ; en .text, l'encadrement io/libc/app)
    reserves = [(".text tete", 0x1000, 0x1040), (".text io->libc", 0x10C0, 0x1100),
                (".text libc->app", 0x1300, 0x1800), (".text app->fin", 0x1C80, 0x2000),
                (".text2 trou net", 0x4200, 0x4300), (".text2 thr->cli", 0x4340, 0x4400),
                (".text2 cli->srv", 0x45C0, 0x4B00), (".text2 http->fin", 0x5E80, 0x6000)]
    defauts = [nom for nom, debut, fin in reserves
               if _tranche(exe, debut, fin - debut) != b"\xcc" * (fin - debut)]
    s.verifie(7, "reserves .text/.text2 remplies d'int3 (emplacements libres scelles)",
              not defauts, str(defauts))
    # Padding intra-slot : NOP apres le code (constat par notation embarquee)
    _, _, code, _ = _assembler_tout()
    non_nop = [bid for bid, _, _, _ in blocs
               if not all(b == 0x90 for b in code[bid]["slot"][len(code[bid]["octets"]):])]
    s.verifie(7, "padding intra-slot = NOP (0x90) jusqu'au bord du slot", not non_nop,
              str(non_nop))
    # R7 structurel : les heritages vivent a leurs RVA historiques M0/M1/M2 —
    # jamais deplaces (le constat octet-identique est fait a l'element 6).
    heritages_rva = [rva for bid, _, rva, _ in blocs if bid[:2] in ARTIFACTS_HERITAGE]
    s.verifie(7, "13 heritages aux RVA historiques exacts (jamais deplaces, R7)",
              heritages_rva == [0x1040, 0x1080, 0x1100, 0x1180, 0x1200, 0x1280,
                                0x4000, 0x4100, 0x4140, 0x4180, 0x41C0, 0x4300, 0x4B00],
              f"{len(heritages_rva)} blocs")


def controle_jalon_fuzz(s: Suite, exe: bytes, graine: int,
                        total: int, accum: int) -> dict:
    """Étape (e) : le harnais de la campagne million devient contrôle permanent.

    La campagne réduite réutilise INTÉGRALEMENT le harnais D72
    (m3/fuzz_million.py — volet feuilles différentiel par tranches
    d'émulateur neuf, volet accumulation à propriétés P1-P5, sentinelles
    tournantes, auto-test de falsification par mutations d'un octet) : zéro
    logique copiée, zéro dérive modèle possible. VERT si et seulement si :
    auto-test PASS (le harnais détecte les défauts injectés) ET zéro échec
    confirmé ET zéro échec non reproductible.
    """
    import fuzz_million as fm
    rapport, ok = fm.campagne(exe, total, accum, graine, tranche=1_000, lot=250,
                              verbeux=False, avec_auto_test=True)
    at = rapport.get("auto_test", {})
    at_verdict = str(at.get("verdict", "?"))
    s.verifie(8, "falsification du harnais : mutations M1/M2 DETECTEES, temoin sauvage PASS",
              at_verdict.startswith("PASS"), at_verdict)
    s.verifie(8, f"campagne reduite {total} cas SANS CRASH (P1-P5, zero echec)",
              bool(ok), str(rapport.get("verdict", "interrompu (auto-test en echec)")))
    acc = rapport.get("accumulation", {})
    sent = acc.get("sentinelles", {})
    return {"cas": rapport.get("total_cas", total),
            "graine": graine,
            "duree": rapport.get("duree_totale_s", "?"),
            "sentinelles": f"{sent.get('ok', 0)}/{sent.get('executions', 0)}",
            "auto_test": "PASS" if at_verdict.startswith("PASS") else "ECHEC",
            "fuzz_ok": bool(ok) and at_verdict.startswith("PASS")}


def executer(graine: int | None = None, total: int = 10_000,
             accum: int = 1_000) -> tuple[bool, list[str]]:
    """Exécute la suite complète ; retourne (verdict, lignes de rapport)."""
    if graine is None:
        graine = int(time.strftime("%Y%m%d"))
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
    meta = controle_jalon_fuzz(s, exe, graine, total, accum)
    lignes = s.lignes()
    total_c = len(s.controles)
    verdict = ("verte" if s.ok else "ROUGE")
    etat_fuzz = ("SANS CRASH P1-P5" if meta["fuzz_ok"] else "EN ECHEC")
    synthese = (f"{verdict} (conformite_profil.py : elements 1-7 + controle de jalon M3 : "
                f"{total_c} controles {'PASS' if s.ok else 'EN ECHEC'} ; element 5 : porte R10 "
                f"constatee, moteur de patch hors perimetre M3 (jalon M5) ; etape (e) : "
                f"fuzzing {meta['cas']} cas {etat_fuzz}, graine {meta['graine']}, sentinelles "
                f"{meta['sentinelles']}, auto-test {meta['auto_test']}, {meta['duree']}s)")
    with open(os.path.join(ICI, "conformite.txt"), "w", encoding="ascii") as f:
        f.write(synthese + "\n")
    lignes.append(f"[conformite.txt] {synthese}")
    return s.ok, lignes


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Suite de conformite du profil x86-64-win11-pe (spec 8.2) — "
                    "jalon M3, etape (e) : fuzzing a proprietes integre")
    ap.add_argument("--graine", type=int, default=None,
                    help="graine maitresse du fuzzing (defaut : AAAAMMJJ du jour, "
                         "reproductible)")
    ap.add_argument("--cas", type=int, default=10_000,
                    help="volume total de la campagne reduite (defaut 10^4)")
    ap.add_argument("--accum", type=int, default=1_000,
                    help="part du volet accumulation http-10 (defaut 10^3)")
    args = ap.parse_args()
    ok, rapport = executer(graine=args.graine, total=args.cas, accum=args.accum)
    print("\n".join(rapport))
    sys.exit(0 if ok else 1)
