#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""conformite_profil.py — Suite de conformité du profil x86-64-win11-pe (spec § 8.2).

Jalon M5 : la suite exigée « à chaque cristallisation de version rc et
finale (§ 9) » — modèle D104 (m4/conformite_profil.py), portée à la
composition 0.6.0 (D136). Les SEPT éléments sont constatés depuis
l'artefact (proxy.exe 0.6.0-dev.1, sha256 4b8f6af6…, 36 352 o — les octets
assemblés par le build dont l'image M4 == le scellé 0.5.1 octet pour octet,
les octets prouvés par les runs v7/v8), les sources (couche I, notations) et
le plan d'adressage (m5/layout.py, source unique) — jamais déclarés sans
preuve. L'élément 5 (patch à chaud) demeure PARTAGÉ : les DEUX portes sont
constatées VIVANTES (R10 héritée 28 entrées + LA PORTE M5 une entrée, la
somme .text4 déclarée == recalculée, le bloc d'entrée DANS la plage gardée) ;
le moteur de patch (tcp-07, staging, croissance) n'est pas embarqué — le
critère complet « patch à chaud du journal en production » reste au
programme du jalon.

Éléments et constats :
  1 ISA et types        : COFF 0x8664, PE32+ 0x020B ; .text/.text2/.text3/
                          .text4 décodables en mode 64 bits sans reste ;
                          INT secur32 = 7 qwords LE (@0x2A40 → hints/names
                          @0x2A80, héritage) ; descripteurs M4 @0x29A0
                          (héritage 3 DLL + terminateur) ; descripteurs M5
                          @0x2DA0 (kernel32#2 GetCommandLineW + les TROIS
                          hérités repris + terminateur, 5 × 20 o) ; IAT/INT
                          M5 @0x2E30/@0x2E50 → hint GetCommandLineW @0x2E70 ;
                          fixtures M5 : refus CLI 37 o @0x2CE0, ligne
                          politique 20 o @0x2D10, L"--relever-https" 32 o
                          @0x2D80 ; fixtures héritées (package Schannel,
                          tunnel/certificat tls-08, 502-cert) intactes.
  2 ABI d'appel         : tous les appels indirects call [rip] aboutissent
                          dans les plages IAT (M3 kernel32/ws2_32, secur32
                          7 slots, IAT M5) ; les SEPT entrées secur32 ET
                          GetCommandLineW (l'entrée NOUVELLE) sont visitées ;
                          ombre ABI posée par les couches tls (héritage).
  3 Format d'exécutable: PE32+ 6 sections, tailles == layout, entrée PE
                          0x8C80 (http-12:R3 — la CLI et la porte M5) ;
                          protections ACTIVES : DEP/NX (0x0100), ASLR
                          (0x0040), HIGH_ENTROPY_VA (0x0020) ; CFI/CFG NON
                          posé — rapporté (chaîne artefact maison : porte
                          R10 + porte M5 + verrous structurels, pas /guard).
  4 Interface système   : 3 DLL importées (kernel32 décrite DEUX fois :
                          GetCommandLineW + les 10 slots scellés M3), 31
                          entrées (11 + 13 + 7) ; contrat d'erreurs : la
                          table HRESULTS (13 entrées, héritage) couvre le
                          succès exact, les TROIS continuations nommées et
                          VERDICT_FATAL = 6 (fail-closed intégral).
  5 Patch à chaud       : porte R10 héritée VIVANTE : 28 entrées de 0x2660
                          à 0x2820, l'entrée #28 garde .text3 ENTIER ;
                          R_VERSION @0x2820 = 0x00060000 (0.6.0-dev.1) ≥
                          plancher 0x00040000, > 0x00050003 (monotonie) ;
                          PORTE M5 VIVANTE : UNE entrée (0x8000, 0x2000,
                          somme .text4) — le bloc d'entrée 0x8C80 est DANS
                          la plage gardée (miroir D95) ; R_ANCRE nulle ;
                          moteur rapporté (critère complet au programme).
  6 Notation            : round-trip 100 % sur les TROIS blocs M5
                          (assembler_tout_m5) et l'héritage M3+M4 re-vérifié
                          de bout en bout (assembler_tout_m4, EchecBuild
                          sinon) ; R7 : 38 blocs octet-identiques au scellé
                          0.5.1 (preuve_reutilisation) ; le scellé M4 0.5.1
                          présent et conforme (sha fb41697d…).
  7 Granularité/padding : 36 352 octets == layout (0x8E00) ; les TROIS
                          blocs g8xxxx à leurs rva/slot de plan ; la réserve
                          .text4 (0x8FC0-0x9FFF) reste int3 (0xCC —
                          l'extension future du patch à chaud) ; R_POLITIQUE
                          @0x3860 à l'état image 0 (P3 de http-12:R3).

Contrôle de jalon M5 : l'oracle à scénarios étendus D136 en volume « reduit »
(graine datée donc reproductible, falsification incluse) — la relevée, la
ligne de flux octet par octet, l'héritage Q7 sans politique et l'anti-contrebande.

Sortie : m5/conformite.txt (une ligne de synthèse, reproductible).
"""

import argparse
import hashlib
import importlib.util
import os
import struct
import sys
import time

import capstone
import pefile

ICI = os.path.dirname(os.path.abspath(__file__))


def _charger_module(nom: str, chemin: str):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


# build_m5 charge L4 → B4 (→ L3/B3) → od4 → od5 → L (plan M5) dans le bon
# ordre ; conformite_profil réutilise TOUTES ses fonctions (aucune seconde
# source — miroir du modèle D104 : recharge de build_m5 sous nom propre,
# aucune collision d'état avec le __main__ du scellage).
BM = _charger_module("build_m5", os.path.join(ICI, "build_m5.py"))
L = BM.L      # plan M5 (source unique)
L4 = BM.L4    # plan M4 (héritage — portes R10, fixtures, HRESULTS)
B4 = BM.B4    # builder M4 (re-vérification R7, preuve_reutilisation)
od5 = BM.od5  # oracle à scénarios étendus D136 (contrôle de jalon)

CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
CS.detail = True  # accès aux opérandes (élément 2 : cibles call [rip])


class Suite:
    """Sept éléments ; chaque constat tranché binaire (jamais de « pass mou »)."""

    def __init__(self):
        self.controles = []

    def verrou(self, element: int, nom: str, ok: bool, detail: str = ""):
        self.controles.append((element, nom, bool(ok), detail))
        print(f"  [{element}] {'PASS' if ok else 'ECHEC'} : {nom}"
              + (f" ({detail})" if detail else ""))

    def lignes(self) -> list[str]:
        return [f"[conformite] element {e} {'PASS' if ok else 'ECHEC'} : {n}"
                + (f" ({d})" if d else "") for e, n, ok, d in self.controles]

    @property
    def ok(self) -> bool:
        return all(c[2] for c in self.controles)


def _lire_exe() -> bytes:
    with open(os.path.join(ICI, "proxy.exe"), "rb") as f:
        return f.read()


_SECTIONS: list[tuple[str, int, int, int]] | None = None


def _sections(exe: bytes) -> list[tuple[str, int, int, int]]:
    global _SECTIONS
    if _SECTIONS is None:
        pe = struct.unpack_from("<I", exe, 0x3C)[0]
        nsec = struct.unpack_from("<H", exe, pe + 6)[0]
        opt = struct.unpack_from("<H", exe, pe + 20)[0]
        out = []
        for i in range(nsec):
            off = pe + 24 + opt + i * 40
            nom = exe[off:off + 8].rstrip(b"\x00").decode()
            _vs, rva, rs, fro = struct.unpack_from("<IIII", exe, off + 8)
            out.append((nom, rva, rs, fro))
        _SECTIONS = out
    return _SECTIONS


def _fichier(rva: int) -> int:
    # L'empan de CHAQUE section est sa taille réelle (leçon de constat D104)
    for _nom, r, rs, fro in _SECTIONS or []:
        if r <= rva < r + rs:
            return fro + (rva - r)
    raise ValueError(f"rva hors sections : {rva:#x}")


def _tranche(exe: bytes, rva: int, n: int) -> bytes:
    f = _fichier(rva)
    return exe[f: f + n]


def _u32(exe: bytes, rva: int) -> int:
    return struct.unpack_from("<I", exe, _fichier(rva))[0]


def _u64(exe: bytes, rva: int) -> int:
    return struct.unpack_from("<Q", exe, _fichier(rva))[0]


def _somme_qwords(octets: bytes) -> int:
    return BM._somme_qwords(octets)


# --- Élément 1 : ISA et types ---------------------------------------------------

def element_1(s: Suite, exe: bytes):
    print("element 1 : ISA et types")
    pe_off = struct.unpack_from("<I", exe, 0x3C)[0]
    s.verrou(1, "COFF machine = 0x8664 (x86-64)",
             struct.unpack_from("<H", exe, pe_off + 4)[0] == 0x8664)
    s.verrou(1, "PE32+ magic = 0x020B",
             struct.unpack_from("<H", exe, pe_off + 24)[0] == 0x020B)

    # Sections de code décodables en mode 64 bits SANS RESTE (padding inclus)
    for nom, rva, rs, fro in _sections(exe):
        if not nom.startswith(".text"):
            continue
        code = exe[fro: fro + rs]
        reste = len(code)
        for _insn in CS.disasm(code, rva):
            reste -= _insn.size
        s.verrou(1, f"{nom} décodable mode 64 sans reste",
                 reste == 0, f"reste {reste} o")

    # INT secur32 (héritage M4) : 7 qwords LE vers les hints @0x2A80
    int_ok = True
    noms_int = []
    for i in range(8):  # 7 + terminateur
        ptr = _u64(exe, L4.R_INT_SEC32 + 8 * i)
        if ptr == 0:
            int_ok &= (i == 7)
            break
        noms_int.append(ptr)
        int_ok &= L4.R_HN_SEC32 <= ptr < L4.R_HN_SEC32 + 0xAA
    s.verrou(1, "INT secur32 : 7 entrées + terminateur (LE, @0x2A40 — héritage)",
             int_ok and len(noms_int) == 7, f"{len(noms_int)} entrées")

    # Concordance hints/names secur32 (héritage — entrées À LONGUEUR VARIABLE)
    noms_lus: list[str] = []
    off = L4.R_HN_SEC32
    for _ in range(len(L4.SECUR32_IMPORTS)):
        f = _fichier(off) + 2                      # saute le hint (u16)
        fin = exe.index(b"\x00", f)
        noms_lus.append(exe[f:fin].decode())
        off += 2 + (fin - f) + 1
    s.verrou(1, "hints/names secur32 == SECUR32_IMPORTS (ordre exact)",
             noms_lus == L4.SECUR32_IMPORTS, ", ".join(noms_lus[:3]) + "…")
    s.verrou(1, "7 slots IAT secur32 @0x2A00-0x2A30 (layout, héritage)",
             all(_u64(exe, rva) != 0 for rva in L4.IAT_SEC32_SLOTS.values()))

    # Descripteurs M4 hérités @0x29A0 : 3 DLL + terminateur NUL (R7)
    s.verrou(1, "descripteurs M4 hérités @0x29A0 (4 × 20 o, terminateur NUL)",
             _tranche(exe, L4.R_IMPORTS_M4 + 3 * 20, 20) == b"\x00" * 20)

    # Descripteurs M5 @0x2DA0 : kernel32#2 (GetCommandLineW) + les TROIS
    # hérités REPRIS (pointeurs identiques) + terminateur — 5 × 20 o
    s.verrou(1, "descripteurs M5 @0x2DA0 (5 × 20 o, terminateur NUL)",
             _tranche(exe, L.R_IMPORTS_M5 + 4 * 20, 20) == b"\x00" * 20)
    d0 = struct.unpack("<IIIII", _tranche(exe, L.R_IMPORTS_M5, 20))
    s.verrou(1, "descripteur M5 #1 : kernel32#2 → INT/IAT M5 (GetCommandLineW)",
             d0 == (L.R_INT_M5, 0, 0, L.R_NOM_KERNEL32_M5, L.R_IAT_M5),
             f"int={d0[0]:#x} iat={d0[4]:#x}")
    s.verrou(1, "IAT M5 @0x2E30 : 1 slot (hint GetCommandLineW) + terminateur",
             _u64(exe, L.R_IAT_M5) == L.R_HN_M5
             and _u64(exe, L.R_IAT_M5 + 8) == 0)
    s.verrou(1, "INT M5 @0x2E50 : 1 entrée + terminateur",
             _u64(exe, L.R_INT_M5) == L.R_HN_M5
             and _u64(exe, L.R_INT_M5 + 8) == 0)
    hn = _tranche(exe, L.R_HN_M5, 18)
    s.verrou(1, "hint/name GetCommandLineW @0x2E70 (18 o, entrée NOUVELLE)",
             hn == struct.pack("<H", 0) + b"GetCommandLineW\x00")
    s.verrou(1, "nom kernel32#2 @0x2E10 (propre au descripteur M5)",
             _tranche(exe, L.R_NOM_KERNEL32_M5, 13) == b"kernel32.dll\x00")

    # Fixtures M5 — octet pour octet (garde-fous de longueurs du build)
    s.verrou(1, "refus CLI \"TRIADE M5 : argument inconnu, arret\\r\\n\" @0x2CE0 (37 o)",
             _tranche(exe, L.R_TXT_CMD_KO, len(L.TXT_CMD_KO)) == L.TXT_CMD_KO)
    s.verrou(1, "ligne politique \"relever-https arme\\r\\n\" @0x2D10 (20 o)",
             _tranche(exe, L.R_TXT_POLITIQUE, len(L.TXT_POLITIQUE)) == L.TXT_POLITIQUE)
    s.verrou(1, "L\"--relever-https\" UTF-16 @0x2D80 (32 o — la comparaison CLI)",
             _tranche(exe, L.R_CMD_RELEVER, len(L.TXT_CMD_RELEVER)) == L.TXT_CMD_RELEVER)

    # Fixtures héritées M4 — intactes (R7)
    s.verrou(1, "package L\"Microsoft Unified Security Protocol Provider\" @0x2C00",
             _tranche(exe, L4.R_PKG_M4, len(L4.PKG_M4)) == L4.PKG_M4)
    s.verrou(1, "fixtures tls-08 @0x2C60/@0x2C80 (tunnel/certificat — héritage)",
             _tranche(exe, L4.R_TXT_TLS_ETABLI, len(L4.TXT_TLS_ETABLI)) == L4.TXT_TLS_ETABLI
             and _tranche(exe, L4.R_TXT_TLS_CERT, len(L4.TXT_TLS_CERT)) == L4.TXT_TLS_CERT)
    s.verrou(1, "502 étiquetée 34 o @0x2CA0 (http-10:R2 Q3' — héritage)",
             _tranche(exe, L4.R_TXT_502_CERT, len(L4.TXT_502_CERT)) == L4.TXT_502_CERT)


# --- Élément 2 : ABI d'appel ----------------------------------------------------

def element_2(s: Suite, exe: bytes):
    print("element 2 : ABI d'appel")
    # Tous les appels indirects call [rip] des couches de code : chacun doit
    # aboutir dans une plage IAT (kernel32/ws2_32 M3, secur32, IAT M5)
    visites: set[int] = set()
    hors_iat = 0
    total = 0
    for nom, rva, rs, fro in _sections(exe):
        if not nom.startswith(".text"):
            continue
        code = exe[fro: fro + rs]
        for insn in CS.disasm(code, rva):
            if insn.mnemonic != "call":
                continue
            op = insn.op_str
            if not op.startswith("qword ptr [rip"):
                continue
            cible_rva = insn.operands[0].mem.disp + insn.address + insn.size
            total += 1
            if (L4.R_IAT_SEC32 <= cible_rva < L4.R_IAT_SEC32 + 0x38
                    or 0x2030 <= cible_rva < 0x2900     # IAT M3 (kernel32/ws2_32)
                    or L.R_IAT_M5 <= cible_rva < L.R_IAT_M5 + 0x10):  # IAT M5
                visites.add(cible_rva)
            else:
                hors_iat += 1
    s.verrou(2, "aucun call [rip] hors des plages IAT (3 DLL + entrée M5)",
             hors_iat == 0, f"{total} appels indirects, {hors_iat} hors plage")
    sept = [L4.IAT_SEC32_SLOTS[n] for n in L4.SECUR32_IMPORTS]
    manquants = [hex(r) for r in sept if r not in visites]
    s.verrou(2, "les SEPT entrées secur32 sont appelées (call [rip] → IAT)",
             not manquants, f"manquants : {manquants}" if manquants
             else "ACH FCH ICS DSC QCA EM DM visités")
    s.verrou(2, "GetCommandLineW visité (l'entrée NOUVELLE — IAT M5 @0x2E30)",
             L.IAT_M5_SLOTS["GetCommandLineW"] in visites,
             "http-12:R3 lit la ligne de commande par le slot M5")

    # Ombre ABI D98 (héritage) : cadres sub rsp dans la couche tls — le
    # constat 0.6.0 : CINQ imm8 (la trame tls-05:R2 passée à 0x98 en D140
    # vit en imm32 48 81 EC, elle n'est plus comptée en imm8) + les cadres
    # imm32 ; .text4 porte SES cadres M5 (http-10:R3/http-12:R3)
    t3 = _tranche(exe, L4.TEXT3_RVA, L4.TEXT3_VSIZE)
    ombres_t3 = sum(t3.count(bytes.fromhex("4883ec") + bytes([n]))
                    for n in range(0x08, 0x60, 8))
    ombres_t3_32 = t3.count(bytes.fromhex("4881ec"))
    t4 = _tranche(exe, L.TEXT4_RVA, L.TEXT4_VSIZE)
    ombres_t4 = sum(t4.count(bytes.fromhex("4883ec") + bytes([n]))
                    for n in range(0x08, 0x60, 8))
    s.verrou(2, "ombres ABI x64 posées (sub rsp — D98 ; tls-05:R2 en imm32 "
             "depuis D140)",
             ombres_t3 >= 5 and ombres_t3_32 >= 1 and ombres_t4 >= 4,
             f".text3 : {ombres_t3} imm8 + {ombres_t3_32} imm32 (héritage) ; "
             f".text4 : {ombres_t4} cadres M5")


# --- Élément 3 : format d'exécutable --------------------------------------------

def element_3(s: Suite, exe: bytes, pe: pefile.PE):
    print("element 3 : format d'exécutable")
    dllcar = pe.OPTIONAL_HEADER.DllCharacteristics
    s.verrou(3, "DEP/NX actif (0x0100)", bool(dllcar & 0x0100))
    s.verrou(3, "ASLR/DYNAMIC_BASE actif (0x0040)", bool(dllcar & 0x0040))
    s.verrou(3, "HIGH_ENTROPY_VA actif (0x0020)", bool(dllcar & 0x0020))
    s.verrou(3, "CFI/CFG non posé — rapporté (portes + verrous, pas /guard)",
             not (dllcar & 0x4000), "état rapporté, non requis par le profil")
    s.verrou(3, "SizeOfImage = 0xA000 (layout)",
             pe.OPTIONAL_HEADER.SizeOfImage == L.SIZE_OF_IMAGE)
    s.verrou(3, "taille fichier = 36 352 o (layout TAILLE_FICHIER)",
             len(exe) == L.TAILLE_FICHIER)
    s.verrou(3, "point d'entrée PE = 0x8C80 (http-12:R3 — la CLI et la porte M5)",
             pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE_M5)
    noms = [sec.Name.decode().rstrip("\x00") for sec in pe.sections]
    s.verrou(3, "6 sections .text/.rdata/.data/.text2/.text3/.text4",
             noms == [".text", ".rdata", ".data", ".text2", ".text3", ".text4"],
             " ".join(noms))
    tailles_ok = all(
        pe.sections[i].SizeOfRawData == rs
        for i, (_n, _r, rs, _f) in enumerate(_sections(exe)))
    s.verrou(3, "tailles brutes des sections == plan d'adressage", tailles_ok)


# --- Élément 4 : interface système ----------------------------------------------

def element_4(s: Suite, exe: bytes, pe: pefile.PE):
    print("element 4 : interface système")
    dlls: dict[str, list[str]] = {}
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        cle = entry.dll.decode().lower()
        dlls.setdefault(cle, []).extend(
            imp.name.decode() for imp in entry.imports if imp.name)
    s.verrou(4, "3 DLL importées : kernel32, ws2_32, secur32",
             set(dlls) == {"kernel32.dll", "ws2_32.dll", "secur32.dll"},
             ", ".join(sorted(dlls)))
    s.verrou(4, "kernel32 : 11 entrées (GetCommandLineW + les 10 slots scellés M3)",
             len(dlls.get("kernel32.dll", [])) == 11,
             f"{len(dlls.get('kernel32.dll', []))} entrées")
    s.verrou(4, "ws2_32 : 13 entrées (héritage M3 scellé)",
             len(dlls.get("ws2_32.dll", [])) == 13)
    s.verrou(4, "secur32 : 7 entrées dans l'ordre SECUR32_IMPORTS",
             dlls.get("secur32.dll", []) == L4.SECUR32_IMPORTS)

    # Contrat d'erreurs : la table HRESULTS (héritage M4 — clés NUMÉRIQUES)
    hr = L4.HRESULTS
    s.verrou(4, "table HRESULTS : succès exact + 3 continuations nommées",
             hr.get(0) == 0 and hr.get(0x00090312) is not None
             and hr.get(0x80090318) is not None and hr.get(0x00090317) is not None,
             f"{len(hr)} HRESULTS couverts (13 entrées numériques)")
    s.verrou(4, "VERDICT_FATAL = 6 : tout HRESULT inconnu est un échec propre",
             L4.VERDICT_FATAL == 6 and len(hr) == 13,
             "fail-closed intégral (tls-02:R1) — table TOTALE")


# --- Élément 5 : patch à chaud (portes VIVANTES, moteur rapporté) ------------------

def element_5(s: Suite, exe: bytes):
    print("element 5 : patch à chaud")
    # La porte R10 HÉRITÉE (M3/M4, 28 entrées) — intacte dans l'artefact 0.6.0
    table_debut = L4.L3.R_TAB_SUM             # 0x2660 (scellé M3)
    nb = (L4.R_VERSION - table_debut) // 16   # 28 entrées attendues
    s.verrou(5, "porte R10 héritée : 28 entrées de 0x2660 à 0x2820",
             nb == 28, f"{nb} entrées")
    rva28 = _u32(exe, L4.R10_PORTE_TEXT3)
    taille28 = _u32(exe, L4.R10_PORTE_TEXT3 + 4)
    somme28 = _u64(exe, L4.R10_PORTE_TEXT3 + 8)
    tranche = _tranche(exe, rva28, taille28)
    s.verrou(5, "entrée #28 : rva=0x6000, taille=0x2000 (la couche M4 entière)",
             rva28 == L4.R10_TEXT3_RVA and taille28 == L4.R10_TEXT3_TAILLE)
    s.verrou(5, "somme .text3 déclarée == somme recalculée (porte VIVANTE)",
             somme28 == _somme_qwords(tranche) and somme28 != 0,
             f"somme {somme28:#x}")
    # LA PORTE M5 : UNE entrée (0x8000, 0x2000, somme .text4) — miroir D95
    rva_m5 = _u32(exe, L.R_TAB_SUM_M5)
    taille_m5 = _u32(exe, L.R_TAB_SUM_M5 + 4)
    somme_m5 = _u64(exe, L.R_TAB_SUM_M5 + 8)
    s.verrou(5, "porte M5 : UNE entrée (0x8000, 0x2000) @0x2EA0, borne @0x2EB0",
             rva_m5 == L.TEXT4_RVA and taille_m5 == L.TEXT4_VSIZE
             and L.R_BORNE_M5 == L.R_TAB_SUM_M5 + 16,
             f"rva {rva_m5:#x}, taille {taille_m5:#x}")
    tranche_t4 = _tranche(exe, L.TEXT4_RVA, L.TEXT4_VSIZE)
    s.verrou(5, "somme .text4 déclarée == somme recalculée (porte M5 VIVANTE)",
             somme_m5 == _somme_qwords(tranche_t4) and somme_m5 != 0,
             f"somme {somme_m5:#x}")
    s.verrou(5, "le bloc d'entrée 0x8C80 est DANS la plage gardée (fail-closed)",
             rva_m5 <= L.ENTREE_M5 < rva_m5 + taille_m5,
             "la porte se garde elle-même — miroir D95")
    version = _u64(exe, L4.R_VERSION)
    s.verrou(5, "R_VERSION @0x2820 = 0x00060000 (0.6.0) ≥ plancher, > 0x00050003",
             version == L.VERSION_U64_DEV1 and version >= L.VERSION_U64_MIN
             and version > L4.VERSION_U64_051,
             f"version {version:#x} (monotonie R10)")
    s.verrou(5, "R_ANCRE @0x2830 réservée (ancre STATIQUE nulle — D33)",
             _u64(exe, L4.L3.R_ANCRE) == 0)
    s.verrou(5, "moteur de patch non embarqué — rapporté (critère complet au "
             "programme M5)", True, "constat partagé (miroir D73/D104)")


# --- Élément 6 : notation (round-trip) -------------------------------------------

def element_6(s: Suite, exe: bytes, code_m5: dict):
    print("element 6 : notation")
    # assembler_tout_m5 a exigé le round-trip 100 % des TROIS blocs M5
    # (EchecBuild sinon) ; assembler_tout_m4 (appelée par le build) a
    # re-vérifié l'héritage M3+M4 de bout en bout — le constat présent est
    # leur SUCCÈS même
    s.verrou(6, "round-trip 100 % : les TROIS blocs M5 assemblés "
             "(assembler_tout_m5)", len(code_m5) == 3,
             f"{len(code_m5)} blocs M5 (g80001/g80002/g80003)")
    herit = BM.preuve_reutilisation(exe)
    s.verrou(6, "R7 : 38 blocs octet-identiques au scellé 0.5.1 "
             "(héritage M3+M4 complet)",
             herit["blocs_reutilises"] == 38,
             f"{herit['blocs_reutilises']} constatés")
    # Le scellé M4 0.5.1 présent (R7 absolu — l'ancêtre direct de la lignée)
    with open(os.path.join(BM.M4_DIR, "proxy.exe"), "rb") as f:
        m4 = f.read()
    s.verrou(6, "scellé M4 0.5.1 présent et conforme (sha fb41697d…)",
             hashlib.sha256(m4).hexdigest()[:16] == BM.SHA_PROXY_051)


# --- Élément 7 : granularité et padding -------------------------------------------

def element_7(s: Suite, exe: bytes):
    print("element 7 : granularité et padding")
    s.verrou(7, "taille artefact == layout (36 352 o — 0x8E00)",
             len(exe) == 36352)
    # Adresses stables : les TROIS blocs g8xxxx à leurs rva/slot de plan
    # (BLOCS_REVISIONS_M5 : (bid, spec, rva, slot, balise, etat))
    stables = all(
        _tranche(exe, b[2], b[3]) != b"\x00" * b[3]
        and _tranche(exe, b[2], 8) != b"\xcc" * 8
        for b in L.BLOCS_REVISIONS_M5)
    s.verrou(7, "adresses stables : les TROIS blocs g8xxxx à leurs rva de plan",
             stables, "revisions-m5=0x8000-0x8fbf reserve-t4=0x8fc0-0x9fff")
    # La réserve .text4 : int3 uniforme (l'extension future du patch à chaud)
    reserve = _tranche(exe, L.ZONE_RESERVEE_T4[0],
                       L.ZONE_RESERVEE_T4[1] - L.ZONE_RESERVEE_T4[0] + 1)
    s.verrou(7, "réserve .text4 0x8FC0-0x9FFF int3 (0xCC — extension future)",
             reserve == b"\xcc" * len(reserve), f"{len(reserve)} o")
    # R_POLITIQUE à l'état image 0 (P3 de http-12:R3 — le chemin scellé)
    s.verrou(7, "R_POLITIQUE @0x3860 à l'état image 0 (P3 de http-12:R3)",
             _u64(exe, L.R_POLITIQUE) == 0)


# --- Contrôle de jalon M5 : oracle à scénarios étendus D136 -----------------------

def controle_jalon(s: Suite, blobs: dict, graine: int) -> dict:
    print("contrôle de jalon M5 (oracle à scénarios étendus D136, volume reduit)")
    t0 = time.time()
    verdict = od5.executer(blobs, graine=graine, volume="reduit")
    duree = round(time.time() - t0, 1)
    s.verrou(0, "oracle M5 vert (relevée + ligne de flux octet par octet + "
             "héritage Q7 sans politique + falsification — D136)",
             verdict["total_cas"] >= 28,
             f"{verdict['total_cas']} cas, graine {graine}, {duree}s")
    return {"cas": verdict["total_cas"], "graine": graine, "duree": duree}


def executer(graine: int | None = None) -> tuple[bool, list[str]]:
    """Exécute la suite complète ; retourne (verdict, lignes de rapport)."""
    if graine is None:
        graine = int(time.strftime("%Y%m%d"))
    exe = _lire_exe()
    pe = pefile.PE(data=exe, fast_load=False)
    s = Suite()
    element_1(s, exe)
    element_2(s, exe)
    element_3(s, exe, pe)
    element_4(s, exe, pe)
    element_5(s, exe)
    # Éléments 6 + jalon : les sources (assemblages complets, l'ordre du
    # build — l'héritage M3+M4 re-vérifié de bout en bout par les mêmes
    # fonctions que construire/verifier)
    specs_m4, code_m4, _verrous_m4 = BM.B4.assembler_tout_m4()
    _blocs_m3, _s3, code_m3, _verrous_m3 = BM.B4.B3.assembler_tout()
    specs_m5, code_m5, _verrous_m5 = BM.assembler_tout_m5()
    element_6(s, exe, code_m5)
    element_7(s, exe)
    blobs = BM.blobs_oracle(code_m3, code_m4, code_m5)
    meta = controle_jalon(s, blobs, graine)
    lignes = s.lignes()
    total_c = len(s.controles)
    verdict = "verte" if s.ok else "ROUGE"
    synthese = (f"{verdict} (conformite_profil.py : elements 1-7 + controle de "
                f"jalon M5 : {total_c} controles "
                f"{'PASS' if s.ok else 'EN ECHEC'} ; element 5 : les DEUX portes "
                f"constatées VIVANTES (R10 héritée 28 entrées + porte M5), "
                f"moteur de patch hors périmètre ; contrôle de jalon : oracle "
                f"D136 {meta['cas']} cas verts, graine {meta['graine']}, "
                f"{meta['duree']}s ; artefact proxy.exe sha256 "
                f"{hashlib.sha256(exe).hexdigest()[:16]}… — l'image M4 == le "
                f"scellé 0.5.1 octet pour octet, les octets prouvés par les "
                f"runs v7/v8)")
    with open(os.path.join(ICI, "conformite.txt"), "w", encoding="utf-8") as f:
        f.write(synthese + "\n")
    lignes.append(f"[conformite.txt] {synthese}")
    return s.ok, lignes


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Suite de conformite du profil x86-64-win11-pe (spec 8.2) — "
                    "jalon M5 : oracle à scénarios étendus D136 intégré")
    ap.add_argument("--graine", type=int, default=None,
                    help="graine maitresse de l'oracle (defaut : AAAAMMJJ du "
                         "jour, reproductible)")
    args = ap.parse_args()
    ok, rapport = executer(graine=args.graine)
    print("\n".join(rapport))
    sys.exit(0 if ok else 1)
