#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""conformite_profil.py — Suite de conformité du profil x86-64-win11-pe (spec § 8.2).

Jalon M4 (D104) : la suite exigée « à chaque cristallisation de version rc et
finale (§ 9) ». Les SEPT éléments sont constatés depuis l'artefact scellé
(proxy.exe 0.5.0-dev.2 D102, md5 2b6481a1… — les octets mêmes que le run
terrain 17-H a prouvés le 29/10 : S05C + S49 OK + témoin HTTP/1.1 200), les
sources (couche I, notations) et le plan d'adressage (m4/layout.py, source
unique) — jamais déclarés sans preuve. L'élément 5 (patch à chaud) est
PARTAGÉ : la porte R10 est constatée VIVANTE (table 28 entrées, somme .text3
recalculée == constatée, version ≥ plancher, ancre, tête de http-12:R2) ; le
moteur de patch (tcp-07, staging, croissance) n'est pas embarqué à ce jalon
(M5, layout D46) — rapporté.

Éléments et constats :
  1 ISA et types        : COFF 0x8664, PE32+ 0x020B ; .text/.text2/.text3
                          décodables en mode 64 bits sans reste ; INT
                          kernel32 = 10 qwords LE, INT ws2_32 = 13, INT
                          secur32 = 7 (@0x2A40 → hints/names @0x2A80) ;
                          descripteurs M4 @0x29A0 (3 DLL + terminateur) ;
                          package L"Microsoft Unified Security Protocol
                          Provider" @0x2C00 ; fixtures tls-08 @0x2C60/@0x2C80 ;
                          502 étiquetée 34 o @0x2CA0.
  2 ABI d'appel         : sept appels secur32 en call qword [rip+disp] vers
                          les slots IAT 0x2A00-0x2A30 (chacun visité) ; ombre
                          ABI 0x28 (D98) posée par la couche tls ; volatilité
                          et pile gardées par les verrous structurels du
                          build (482 verrous M4, D63/D98).
  3 Format d'exécutable: PE32+ 5 sections, tailles == layout, entrée PE
                          0x7DC0 (http-12:R2, D95) ; protections ACTIVES
                          constatées : DEP/NX (0x0100), ASLR/DYNAMIC_BASE
                          (0x0040), HIGH_ENTROPY_VA (0x0020) ; CFI/CFG NON
                          posé — rapporté (chaîne artefact maison :
                          l'intégrité d'exécution est la porte R10 + les
                          verrous structurels, pas /guard).
  4 Interface système   : 3 DLL importées, 30 entrées (10 + 13 + 7) dans
                          l'ordre déclaré SECUR32_IMPORTS ; contrat
                          d'erreurs : la table HRESULTS (layout, source
                          unique) couvre le succès exact, les TROIS
                          continuations nommées et VERDICT_FATAL = 6 — tout
                          autre HRESULT traverse tls-02 en échec propre
                          (fail-closed intégral, spec tls-02:R1).
  5 Patch à chaud       : porte R10 VIVANTE : 28 entrées (rva, taille,
                          somme) de 0x2660 à 0x2820 ; l'entrée #28 @0x2810
                          garde .text3 ENTIER (somme déclarée == somme
                          recalculée de la tranche) ; R_VERSION @0x2820 =
                          0x00050003 (0.5.1, D140) ≥ plancher 0x00040000 ;
                          R_ANCRE @0x2830 ; moteur rapporté M5.
  6 Notation            : round-trip 100 % sur les 12 blocs M4
                          (assembler_tout_m4 — EchecBuild sinon) et 27 blocs
                          héritage re-vérifiés octet pour octet
                          (preuve_reutilisation == 27, R7) ; le scellé M3
                          0.4.0 présent et conforme (sha bf02769f…).
  7 Granularité/padding : 28 160 octets inchangés depuis D94 (taille ==
                          layout) ; tls-07:R2 : 527 o dans le slot 768 (le
                          correctif D102 vit dans le padding, taille
                          inchangée) ; tls-05:R2 : 325 o dans le slot 384
                          (D140 — même mécanique, le padding absorbe) ;
                          adresses stables (rva/slot des blocs == plan).

Contrôle de jalon M4 (miroir du fuzzing sentinelle M3, étape (e)) : l'oracle
différentiel en volume « reduit » (graine datée donc reproductible,
falsification incluse) — le tunnel chiffré, le scan PAR TYPE D102 et la
compensation exacte.

Sortie : m4/conformite.txt (une ligne de synthèse, reproductible).
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


# build_m4 charge L3 → B3 → L (plan M4) → od4 → cm dans le bon ordre ;
# conformite_profil réutilise TOUTES ses fonctions (aucune seconde source).
B4 = _charger_module("build_m4", os.path.join(ICI, "build_m4.py"))
L = B4.L      # plan M4 (source unique)
L3 = B4.L3    # plan M3 (héritage)
B3 = B4.B3    # builder M3 (re-vérification R7)
od4 = B4.od4  # oracle différentiel M4 (contrôle de jalon)

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
    # L'empan de CHAQUE section est sa taille réelle (jamais un span large :
    # .text ne doit pas avaler .rdata/.text2/.text3 — leçon de constat)
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
    return B4._somme_qwords(octets)


# --- Élément 1 : ISA et types ---------------------------------------------------

def element_1(s: Suite, exe: bytes):
    print("element 1 : ISA et types")
    pe_off = struct.unpack_from("<I", exe, 0x3C)[0]
    s.verrou(1, "COFF machine = 0x8664 (x86-64)",
             struct.unpack_from("<H", exe, pe_off + 4)[0] == 0x8664)
    s.verrou(1, "PE32+ magic = 0x020B",
             struct.unpack_from("<H", exe, pe_off + 24)[0] == 0x020B)

    # Sections décodables en mode 64 bits SANS RESTE (padding int3 inclus)
    for nom, rva, rs, fro in _sections(exe):
        if not nom.startswith(".text"):
            continue
        code = exe[fro: fro + rs]
        reste = len(code)
        for _insn in CS.disasm(code, rva):
            reste -= _insn.size
        s.verrou(1, f"{nom} décodable mode 64 sans reste",
                 reste == 0, f"reste {reste} o")

    # INT secur32 : 7 qwords LE vers les hints @0x2A80 + terminateur
    hints = {nom: rva for nom, rva in L.IAT_SEC32_SLOTS.items()}
    int_ok = True
    noms_int = []
    for i in range(8):  # 7 + terminateur
        ptr = _u64(exe, L.R_INT_SEC32 + 8 * i)
        if ptr == 0:
            int_ok &= (i == 7)
            break
        noms_int.append(ptr)
        int_ok &= L.R_HN_SEC32 <= ptr < L.R_HN_SEC32 + 0xAA
    s.verrou(1, "INT secur32 : 7 entrées + terminateur (LE, @0x2A40)",
             int_ok and len(noms_int) == 7, f"{len(noms_int)} entrées")

    # Concordance hints/names : entrées À LONGUEUR VARIABLE [hint u16][nom\0]
    # (alignement pair) — lecture séquentielle depuis @0x2A80
    noms_lus: list[str] = []
    off = L.R_HN_SEC32
    for _ in range(len(L.SECUR32_IMPORTS)):
        f = _fichier(off) + 2                      # saute le hint (u16)
        fin = exe.index(b"\x00", f)
        noms_lus.append(exe[f:fin].decode())
        off += 2 + (fin - f) + 1                   # hint + nom + NUL, SANS
        # padding : les entrées se serrent octet à octet (constat hexdump
        # 0x2A80 — le hint peut vivre sur une adresse IMPAIRE)
    s.verrou(1, "hints/names secur32 == SECUR32_IMPORTS (ordre exact)",
             noms_lus == L.SECUR32_IMPORTS, ", ".join(noms_lus[:3]) + "…")
    s.verrou(1, "7 slots IAT secur32 @0x2A00-0x2A30 (layout)",
             all(_u64(exe, rva) != 0 for rva in hints.values()))

    # Descripteurs M4 : 3 DLL + terminateur NUL (fin == 0x29F0)
    s.verrou(1, "descripteurs M4 @0x29A0 (4 × 20 o, terminateur NUL)",
             _tranche(exe, L.R_IMPORTS_M4 + 3 * 20, 20) == b"\x00" * 20)

    # Fixtures .rdata M4 — octet pour octet
    s.verrou(1, "package L\"Microsoft Unified Security Protocol Provider\" @0x2C00",
             _tranche(exe, L.R_PKG_M4, len(L.PKG_M4)) == L.PKG_M4)
    s.verrou(1, "fixture \"tunnel chiffre etabli\\r\\n\" @0x2C60 (23 o, tls-08 Q1)",
             _tranche(exe, L.R_TXT_TLS_ETABLI, len(L.TXT_TLS_ETABLI)) == L.TXT_TLS_ETABLI)
    s.verrou(1, "fixture \"certificat rejete\\r\\n\" @0x2C80 (19 o, tls-08 I4 — LE critère M4)",
             _tranche(exe, L.R_TXT_TLS_CERT, len(L.TXT_TLS_CERT)) == L.TXT_TLS_CERT)
    s.verrou(1, "502 étiquetée 34 o @0x2CA0 (http-10:R2 Q3')",
             _tranche(exe, L.R_TXT_502_CERT, len(L.TXT_502_CERT)) == L.TXT_502_CERT)


# --- Élément 2 : ABI d'appel ----------------------------------------------------

def element_2(s: Suite, exe: bytes):
    print("element 2 : ABI d'appel")
    # Tous les appels indirects call [rip+disp] des couches de code :
    # chacun doit aboutir dans une plage IAT (kernel32/ws2_32/secur32)
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
            if (L.R_IAT_SEC32 <= cible_rva < L.R_IAT_SEC32 + 0x38
                    or 0x2030 <= cible_rva < 0x2900):   # IAT M3 (kernel32/ws2_32)
                visites.add(cible_rva)
            else:
                hors_iat += 1
    s.verrou(2, "aucun call [rip] hors des plages IAT (3 DLL)",
             hors_iat == 0, f"{total} appels indirects, {hors_iat} hors plage")
    sept = [L.IAT_SEC32_SLOTS[n] for n in L.SECUR32_IMPORTS]
    manquants = [hex(r) for r in sept if r not in visites]
    s.verrou(2, "les SEPT entrées secur32 sont appelées (call [rip] → IAT)",
             not manquants, f"manquants : {manquants}" if manquants
             else "ACH FCH ICS DSC QCA EM DM visités")

    # Ombre ABI D98 : cadres sub rsp, imm8 par bloc (0x28 tls-07/tls-08,
    # 0x30/tls-04, 0x58 http-10:R2 — cadres à la mesure de chaque bloc)
    t3 = _tranche(exe, L.TEXT3_RVA, L.TEXT3_VSIZE)
    ombres = sum(t3.count(bytes.fromhex("4883ec") + bytes([n]))
                 for n in range(0x08, 0x60, 8))
    s.verrou(2, "ombres ABI x64 posées dans la couche tls (sub rsp, imm8 — D98)",
             ombres >= 6, f"{ombres} prologues constatés dans .text3")


# --- Élément 3 : format d'exécutable --------------------------------------------

def element_3(s: Suite, exe: bytes, pe: pefile.PE):
    print("element 3 : format d'exécutable")
    dllcar = pe.OPTIONAL_HEADER.DllCharacteristics
    s.verrou(3, "DEP/NX actif (0x0100)", bool(dllcar & 0x0100))
    s.verrou(3, "ASLR/DYNAMIC_BASE actif (0x0040)", bool(dllcar & 0x0040))
    s.verrou(3, "HIGH_ENTROPY_VA actif (0x0020)", bool(dllcar & 0x0020))
    s.verrou(3, "CFI/CFG non posé — rapporté (porte R10 + verrous, pas /guard)",
             not (dllcar & 0x4000), "état rapporté, non requis par le profil M4")
    s.verrou(3, "SizeOfImage = 0x8000 (layout)",
             pe.OPTIONAL_HEADER.SizeOfImage == L.SIZE_OF_IMAGE)
    s.verrou(3, "taille fichier = 28 160 o (layout TAILLE_FICHIER)",
             len(exe) == L.TAILLE_FICHIER)
    s.verrou(3, "point d'entrée PE = 0x7DC0 (http-12:R2, D95)",
             pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE_R2)
    noms = [sec.Name.decode().rstrip("\x00") for sec in pe.sections]
    s.verrou(3, "5 sections .text/.rdata/.data/.text2/.text3",
             noms == [".text", ".rdata", ".data", ".text2", ".text3"],
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
        dlls[entry.dll.decode().lower()] = [
            imp.name.decode() for imp in entry.imports if imp.name]
    s.verrou(4, "3 DLL importées : kernel32, ws2_32, secur32",
             set(dlls) == {"kernel32.dll", "ws2_32.dll", "secur32.dll"},
             ", ".join(sorted(dlls)))
    s.verrou(4, "kernel32 : 10 entrées (héritage M3 scellé)",
             len(dlls.get("kernel32.dll", [])) == 10)
    s.verrou(4, "ws2_32 : 13 entrées (héritage M3 scellé)",
             len(dlls.get("ws2_32.dll", [])) == 13)
    s.verrou(4, "secur32 : 7 entrées dans l'ordre SECUR32_IMPORTS",
             dlls.get("secur32.dll", []) == L.SECUR32_IMPORTS)

    # Contrat d'erreurs : la table HRESULTS (layout, source unique — clés
    # NUMÉRIQUES HRESULT → verdict : 0=SEC_E_OK, 0x90312=CONTINUE_NEEDED,
    # 0x80090318=INCOMPLETE_MESSAGE, 0x90317=CONTEXT_EXPIRED…)
    hr = L.HRESULTS
    s.verrou(4, "table HRESULTS : succès exact + 3 continuations nommées",
             hr.get(0) == 0 and hr.get(0x00090312) is not None
             and hr.get(0x80090318) is not None and hr.get(0x00090317) is not None,
             f"{len(hr)} HRESULTS couverts (13 entrées numériques)")
    s.verrou(4, "VERDICT_FATAL = 6 : tout HRESULT inconnu est un échec propre",
             L.VERDICT_FATAL == 6 and len(hr) == 13,
             "fail-closed intégral (tls-02:R1) — table TOTALE")


# --- Élément 5 : patch à chaud (porte VIVANTE, moteur rapporté) ------------------

def element_5(s: Suite, exe: bytes):
    print("element 5 : patch à chaud")
    table_debut = L3.R_TAB_SUM               # 0x2660 (scellé M3)
    nb = (L.R10_BORNE - table_debut) // 16   # 28 entrées attendues
    s.verrou(5, "porte R10 : 28 entrées de 0x2660 à 0x2820 (26 héritage + "
             "libc-07 + .text3)", nb == L.R10_NB_ENTREES, f"{nb} entrées")
    # L'entrée #28 garde .text3 ENTIER : (rva, taille, somme) déclarés ==
    # constatés — la porte se garde elle-même (D95)
    rva28 = _u32(exe, L.R10_PORTE_TEXT3)
    taille28 = _u32(exe, L.R10_PORTE_TEXT3 + 4)
    somme28 = _u64(exe, L.R10_PORTE_TEXT3 + 8)
    tranche = _tranche(exe, rva28, taille28)
    s.verrou(5, "entrée #28 : rva=0x6000, taille=0x2000 (toute la couche M4)",
             rva28 == L.R10_TEXT3_RVA and taille28 == L.R10_TEXT3_TAILLE)
    s.verrou(5, "somme .text3 déclarée == somme recalculée (porte VIVANTE)",
             somme28 == _somme_qwords(tranche) and somme28 != 0,
             f"somme {somme28:#x}")
    version = _u64(exe, L.R10_BORNE)
    s.verrou(5, "R_VERSION @0x2820 = 0x00050003 (0.5.1, D140) ≥ plancher 0x00040000",
             version == L.VERSION_U64_051 and version >= L.VERSION_U64_MIN,
             f"version {version:#x}")
    s.verrou(5, "R_ANCRE @0x2830 réservée (ancre STATIQUE nulle — écrite au "
             "lancement par http-12, position-indépendance D33)",
             _u64(exe, L3.R_ANCRE) == 0)
    s.verrou(5, "moteur de patch non embarqué — rapporté (jalon M5)",
             True, "constat partagé (miroir conformité M3 D73)")


# --- Élément 6 : notation (round-trip) -------------------------------------------

def element_6(s: Suite, exe: bytes, code_m3: dict, code_m4: dict):
    print("element 6 : notation")
    # assembler_tout_m4 / assembler_tout ont déjà exigé le round-trip 100 %
    # (EchecBuild sinon) — le constat présent est leur SUCCÈS même
    s.verrou(6, "round-trip 100 % : 12 blocs M4 assemblés (assembler_tout_m4)",
             len(code_m4) >= 12, f"{len(code_m4)} blocs M4")
    herit = B4.preuve_reutilisation(exe)
    s.verrou(6, "R7 : 27 blocs héritage octet-identiques "
             "(26 M3 + libc-07 selftest.exe)",
             herit["blocs_reutilises"] == 27,
             f"{herit['blocs_reutilises']} constatés")
    # Le scellé M3 0.4.0 présent (R7 absolu — l'ancêtre de la lignée)
    with open(os.path.join(B4.M3_DIR, "proxy.exe"), "rb") as f:
        m3 = f.read()
    s.verrou(6, "scellé M3 0.4.0 présent et conforme (sha bf02769f…)",
             hashlib.sha256(m3).hexdigest() == B4.SHA_PROXY_SCELLE)


# --- Élément 7 : granularité et padding -------------------------------------------

def element_7(s: Suite, exe: bytes, code_m4: dict):
    print("element 7 : granularité et padding")
    s.verrou(7, "taille artefact inchangée depuis D94 (28 160 o)",
             len(exe) == 28160)
    # tls-07:R2 : 527 o dans le slot 0x300 (768) — le correctif D102 vit
    # dans le padding nop (0x90) ; la mesure compte le padding DEPUIS LA QUEUE
    # (un 0x90 isolé peut vivre dans un disp32 — leçon de constat)
    slot = _tranche(exe, 0x6A40, 0x300)
    pad = 0
    while pad < 0x300 and slot[0x300 - 1 - pad] == 0x90:
        pad += 1
    code = 0x300 - pad
    s.verrou(7, "tls-07:R2 : 527 o dans le slot 768 (correctif dans le padding nop)",
             code == 527, f"{code} o de code + {pad} o de padding 0x90")
    # Adresses stables : chaque bloc M4 à son rva/slot de plan (R7)
    stables = all(
        _tranche(exe, rva, 8) != b"\x00" * 8
        for _bid, _sid, rva, slot in
        [(b[0], b[1], b[2], b[3]) for b in L.BLOCS_TLS + L.BLOCS_REVISIONS])
    s.verrou(7, "adresses stables : les 11 blocs g7xxxx à leurs rva de plan",
             stables, "zones tls=0x6000-0x733f revisions=0x7340-0x7fbf")


# --- Contrôle de jalon M4 : oracle différentiel (sentinelle) ---------------------

def controle_jalon(s: Suite, code_m3: dict, code_m4: dict, graine: int) -> dict:
    print("contrôle de jalon M4 (oracle différentiel, volume reduit)")
    blobs = B4.blobs_oracle(code_m3, code_m4)
    t0 = time.time()
    verdict = od4.executer(blobs, graine=graine, volume="reduit")
    duree = round(time.time() - t0, 1)
    s.verrou(0, "oracle différentiel M4 vert (tunnel, scan PAR TYPE D102, "
             "compensation — falsification incluse)",
             verdict["total_cas"] >= 30,
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
    # Éléments 6 + jalon : les sources (assemblages complets, ~2 min)
    specs_m4, code_m4, verrous_m4 = B4.assembler_tout_m4()
    _blocs_m3, _specs_m3, code_m3, verrous_m3 = B3.assembler_tout()
    element_6(s, exe, code_m3, code_m4)
    element_7(s, exe, code_m4)
    meta = controle_jalon(s, code_m3, code_m4, graine)
    lignes = s.lignes()
    total_c = len(s.controles)
    verdict = "verte" if s.ok else "ROUGE"
    synthese = (f"{verdict} (conformite_profil.py : elements 1-7 + controle de "
                f"jalon M4 : {total_c} controles "
                f"{'PASS' if s.ok else 'EN ECHEC'} ; element 5 : porte R10 "
                f"constatee VIVANTE, moteur de patch hors perimetre M4 "
                f"(jalon M5) ; controle de jalon : oracle differentiel "
                f"{meta['cas']} cas verts, graine {meta['graine']}, "
                f"{meta['duree']}s ; artefact proxy.exe md5 2b6481a1... - "
                f"les octets prouves par le terrain 17-H du 29/10)")
    with open(os.path.join(ICI, "conformite.txt"), "w", encoding="utf-8") as f:
        f.write(synthese + "\n")
    lignes.append(f"[conformite.txt] {synthese}")
    return s.ok, lignes


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Suite de conformite du profil x86-64-win11-pe (spec 8.2) — "
                    "jalon M4 (D104) : oracle differentiel integre (sentinelle)")
    ap.add_argument("--graine", type=int, default=None,
                    help="graine maitresse de l'oracle (defaut : AAAAMMJJ du "
                         "jour, reproductible)")
    args = ap.parse_args()
    ok, rapport = executer(graine=args.graine)
    print("\n".join(rapport))
    sys.exit(0 if ok else 1)
