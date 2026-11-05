#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scenario-m8d.py — LE TERRAIN M8-(d) : le VRAI ntdll lu sur la machine du
développeur, le motif confronté, la ligne comparée par les DEUX chemins.

Le kit porte UN artefact et UN scénario :
  proxy.exe   le build 0.9.0-dev.1 du jalon M8 — sha256
              1492b0bc0792e1ab162338b414fb20573134e84d752b9d0657292421f8eb0cd4
              (lecture seule pour le run — le scénario ne l'écrit JAMAIS) ;
  le présent script — python3 SEUL (aucun paquet à installer, aucun droit
              particulier, aucun réseau).

CE QUE LE RUN DEMONTRE (chaque constat tranché binaire, le verdict
POST-MORTEM — un échec nommé vaut plus qu'un vert muet) :
  T0 LE TÉMOIN   les empreintes ASSERTÉES avant tout geste (un kit corrompu
                 est un refus nommé) ; l'environnement consigné (la version
                 Windows, le Python, l'architecture) ; le VRAI ntdll
                 localisé et son fichier haché ; l'artefact cartographié
                 (mapping DONT_RESOLVE — les octets attendus constatés UN
                 PAR UN avant tout appel : sys-01 le trombone, les fixtures
                 .rdata, le slot IAT de WriteFile).
  T1 LA LECTURE   le VRAI ntdll lu par DEUX lecteurs indépendants : le
                 résolveur PYTHON (la marche EAT refaite ici, en Python) et
                 le BLOC sys-02 (le code de l'artefact, appelé à son adresse
                 scellée) — LE MÊME SSN rendu par les deux ; le MOTIF du
                 stub CONFRONTÉ (4C 8B D1 B8 avant l'imm32 — un stub
                 divergent est un refus nommé, jamais un numéro extrait) ;
                 un second nom résolu (NtReadFile — jamais un numéro en
                 cache : chaque appel résout) ; la FALSIFICATION INVITÉE
                 (un module forgé au stub crocheté : le refus -4 NOMMÉ sur
                 la machine réelle).
  T2 LA TWIN      LA MÊME LIGNE par les DEUX chemins : le CHEMIN A —
                 hello-02, le scellé M0, WriteFile PAR L'IAT kernel32 (le
                 slot résolu par le scénario, geste du chargeur) ; le
                 CHEMIN B — sys-03, la twin, NtWriteFile EN SYSCALL DIRECT
                 (zéro IAT, le SSN résolu au geste même par sys-02) ; les
                 DEUX fichiers comparés OCTET PAR OCTET au fixture
                 (33 octets, « TRIADE M0 : Hello, Windows 11 ! CRLF »).
  T3 LES GARDES   la base invalide : sys-03 rend -1 NOMMÉ et AUCUN syscall
                 n'est émis (le fichier-témoin demeure VIDE — la garde I5
                 constatée sur la machine réelle) ; l'intégrité : proxy.exe
                 relu inchangé, le ntdll mappé inchangé (le module lu
                 n'est jamais touché), la cartographie libérée.

Les pièces naissent toutes seules dans ./preuves-m8d/ :
  temoin-m8d.txt, scenario-m8d-journal.log, VERDICT-run-m8d.txt
— à renvoyer ENTIÈRES au coffre /test/preuves-m8d/ (dossier Drive « Triade »
→ « test »). Le laboratoire recoupe sur pièces (D138/D145/D148) et, si
elles établissent le critère, la finale 0.9.0 est scellée.

Un verdict ÉCHEC NOMMÉ se renvoie TEL QUEL : la ligne nomme le défaut.
"""

import ctypes
import ctypes.wintypes as wt
import hashlib
import os
import platform
import struct
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
PREUVES = os.path.join(ICI, "preuves-m8d")

SHA_PROXY = "1492b0bc0792e1ab162338b414fb20573134e84d752b9d0657292421f8eb0cd4"
TAILLE_PROXY = 44544

# --- les adresses scellées de l'artefact (R7 — la carte génération 8) -------
R_HELLO02 = 0x1040        # le scellé M0 — WriteFile par l'IAT
R_SYS01 = 0xA000          # l'émetteur — le trombone ABI (6 octets)
R_SYS02 = 0xA040          # le résolveur SSN — l'EAT de ntdll LUE
R_SYS03 = 0xA180          # la twin de hello-02 par NtWriteFile
R_FIXTURE_NOM = 0x2EC0    # « NtWriteFile » (11 octets, un SPAN sans NUL)
R_FIXTURE_LIGNE = 0x2ED0  # la ligne de hello-02 (33 octets — le fixture M0)
R_IAT_WRITEFILE = 0x20B8  # le slot kernel32!WriteFile (l'ancre R7 de M0)

OCTETS_SYS01 = bytes.fromhex("4989ca0f05c3")          # mov r10,rcx; syscall; ret
FIXTURE_NOM = b"NtWriteFile"
FIXTURE_LIGNE = b"TRIADE M0 : Hello, Windows 11 !\r\n"
MOTIF_STUB = bytes.fromhex("4c8bd1b8")                # mov r10,rcx ; mov eax —
NOM_SECONDAIRE = b"NtReadFile"

DONT_RESOLVE_DLL_REFERENCES = 0x00000001
PAGE_READWRITE = 0x04
PAGE_EXECUTE_READ = 0x20
GENERIC_WRITE = 0x40000000
CREATE_ALWAYS = 2
FILE_ATTRIBUTE_NORMAL = 0x80
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

# --- le journal et le témoin -------------------------------------------------

_journal = []
_temoin = []
_echecs = []


def journal(msg):
    ligne = time.strftime("%H:%M:%S") + "  " + msg
    _journal.append(ligne)
    print("[journal] " + msg)


def temoin(msg):
    _temoin.append(msg)
    print("  " + msg)


def verifie(nom, condition, detail=""):
    if condition:
        temoin(f"[ok] {nom}" + (f" — {detail}" if detail else ""))
    else:
        temoin(f"[ÉCHEC] {nom}" + (f" — {detail}" if detail else ""))
        _echecs.append(nom)
    return bool(condition)


def u16(adresse):
    return struct.unpack("<H", ctypes.string_at(adresse, 2))[0]


def u32(adresse):
    return struct.unpack("<I", ctypes.string_at(adresse, 4))[0]


def sha256_fichier(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


# --- le résolveur PYTHON (le lecteur indépendant — le miroir de sys-02) ------

def lire_ssn_python(base, span, longueur):
    """La marche EAT refaite en Python : (code, rva_stub, detail).

    LE MÊME contrat que sys-02 (la fenêtre e_lfanew [0x40, 0x400], le motif
    PE, le répertoire export, la marche BORNÉE par NumberOfNames, le motif
    du stub AVANT l'imm32) — implémenté SANS regarder le bloc : les deux
    lecteurs ne partagent que le ntdll sous leurs pieds.
    """
    try:
        e_lfanew = u32(base + 0x3C)
        if not (0x40 <= e_lfanew <= 0x400):
            return (-2, None, f"e_lfanew {e_lfanew:#x} hors fenêtre")
        if ctypes.string_at(base + e_lfanew, 4) != b"PE\x00\x00":
            return (-2, None, "le motif PE absent")
        opt = base + e_lfanew + 24
        if u16(opt) != 0x20B:
            return (-2, None, f"magic optionnel {u16(opt):#x} != 0x20B")
        exp_rva = u32(opt + 112)
        if exp_rva == 0:
            return (-3, None, "répertoire export absent")
        nb_noms = u32(base + exp_rva + 0x18)
        a_fonctions = u32(base + exp_rva + 0x1C)
        a_noms = u32(base + exp_rva + 0x20)
        a_ordinaux = u32(base + exp_rva + 0x24)
        for i in range(nb_noms):
            nom_rva = u32(base + a_noms + 4 * i)
            if ctypes.string_at(base + nom_rva, longueur) == span[:longueur]:
                ordinal = u16(base + a_ordinaux + 2 * i)
                stub_rva = u32(base + a_fonctions + 4 * ordinal)
                return (0, stub_rva, None)
        return (-1, None, f"« {span.decode('ascii', 'replace')} » introuvable "
                          f"({nb_noms} noms marchés)")
    except Exception as exc:
        return (-99, None, f"exception Python : {exc}")


def confronter_stub(base, stub_rva):
    """Le motif AVANT l'imm32 — retourne (ok, ssn, detail)."""
    adresse = base + stub_rva
    octets = ctypes.string_at(adresse, 8)
    if octets[:4] != MOTIF_STUB:
        return (False, None,
                f"stub divergent @RVA {stub_rva:#x} : {octets[:4].hex()} "
                f"!= {MOTIF_STUB.hex()} — REFUS NOMMÉ (jamais un numéro "
                f"extrait d'un stub inattendu)")
    return (True, struct.unpack("<I", octets[4:8])[0], None)


# --- le module forgé (la falsification invitée — le refus -4 sur pièces) -----

def forger_module_crochete():
    """Un module minimal BIEN FORMÉ dont le stub de « NtWriteFile » est
    CROCHETÉ (le motif absent) : sys-02 doit rendre -4, jamais le numéro."""
    tampon = ctypes.create_string_buffer(0x400)
    v = memoryview(tampon).cast("B")
    v[0:2] = b"MZ"
    struct.pack_into("<I", v, 0x3C, 0x40)                      # e_lfanew
    v[0x40:0x44] = b"PE\x00\x00"
    struct.pack_into("<H", v, 0x44, 0x8664)                    # machine
    struct.pack_into("<H", v, 0x58, 0x20B)                     # magic PE32+
    struct.pack_into("<I", v, 0x58 + 108, 1)                   # NumberOfRvaAndSizes
    struct.pack_into("<II", v, 0x58 + 112, 0x200, 0x50)        # data dir[0]
    # le répertoire export @0x200
    struct.pack_into("<I", v, 0x200 + 0x18, 1)                 # NumberOfNames
    struct.pack_into("<I", v, 0x200 + 0x1C, 0x280)             # AddressOfFunctions
    struct.pack_into("<I", v, 0x200 + 0x20, 0x290)             # AddressOfNames
    struct.pack_into("<I", v, 0x200 + 0x24, 0x294)             # AddressOfNameOrdinals
    struct.pack_into("<I", v, 0x280, 0x300)                    # fonctions[0]
    struct.pack_into("<I", v, 0x290, 0x2A0)                    # noms[0]
    struct.pack_into("<H", v, 0x294, 0)                        # ordinaux[0]
    v[0x2A0:0x2B0] = b"NtWriteFile\x00"
    # le stub CROCHETÉ : B8 <imm32> sans le « mov r10, rcx » — motif absent
    v[0x300:0x305] = b"\xB8\x44\x33\x22\x11"
    return ctypes.addressof(tampon), tampon


# --- les appelées de l'artefact (les CFUNCTYPE aux adresses scellées) --------

def lier_blocs(base):
    hello02 = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p,
                               ctypes.c_size_t)(base + R_HELLO02)
    sys02 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p, ctypes.c_uint64,
                             ctypes.c_void_p)(base + R_SYS02)
    sys03 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                             ctypes.c_void_p)(base + R_SYS03)
    return hello02, sys02, sys03


# --- le run -------------------------------------------------------------------

def main():
    print("=== LE TERRAIN M8-(d) : le VRAI ntdll, la twin, les DEUX chemins ===\n")
    os.makedirs(PREUVES, exist_ok=True)

    # ---------------- T0 — LE TÉMOIN -----------------------------------------
    print("T0 — LE TÉMOIN (les empreintes, l'environnement, la cartographie)")
    chemin_proxy = os.path.join(ICI, "proxy.exe")
    if not os.path.isfile(chemin_proxy):
        print(f"ÉCHEC NOMMÉ : proxy.exe introuvable ({chemin_proxy})")
        return 1
    sha_proxy = sha256_fichier(chemin_proxy)
    verifie("T0.proxy : l'empreinte de l'artefact",
            sha_proxy == SHA_PROXY, f"sha256 {sha_proxy[:16]}…")
    verifie("T0.proxy : la taille", os.path.getsize(chemin_proxy) == TAILLE_PROXY,
            f"{os.path.getsize(chemin_proxy)} o")

    if sys.platform != "win32":
        print("ÉCHEC NOMMÉ : ce terrain exige Windows (sys.platform="
              f"{sys.platform!r}) — le VRAI ntdll du développeur")
        return 1
    if struct.calcsize("P") != 8:
        print("ÉCHEC NOMMÉ : ce terrain exige un Python 64 bits "
              f"(pointeur {struct.calcsize('P') * 8} bits)")
        return 1

    wv = sys.getwindowsversion()
    temoin(f"[env] Windows {wv.major}.{wv.minor} build {wv.build}")
    temoin(f"[env] Python {platform.python_version()} · "
           f"{platform.machine()} · {platform.system()}")

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.GetModuleHandleW.restype = ctypes.c_void_p
    k32.GetModuleHandleW.argtypes = [wt.LPCWSTR]
    k32.GetProcAddress.restype = ctypes.c_void_p
    k32.GetProcAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    k32.LoadLibraryExW.restype = ctypes.c_void_p
    k32.LoadLibraryExW.argtypes = [wt.LPCWSTR, ctypes.c_void_p, wt.DWORD]
    k32.VirtualProtect.restype = wt.BOOL
    k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t, wt.DWORD,
                                   ctypes.POINTER(wt.DWORD)]
    k32.CreateFileW.restype = ctypes.c_void_p
    k32.CreateFileW.argtypes = [wt.LPCWSTR, wt.DWORD, wt.DWORD, ctypes.c_void_p,
                                wt.DWORD, wt.DWORD, ctypes.c_void_p]
    k32.CloseHandle.restype = wt.BOOL
    k32.CloseHandle.argtypes = [ctypes.c_void_p]
    k32.FreeLibrary.restype = wt.BOOL
    k32.FreeLibrary.argtypes = [ctypes.c_void_p]

    ntdll_base = k32.GetModuleHandleW("ntdll")
    verifie("T0.ntdll : le VRAI ntdll localisé", bool(ntdll_base),
            f"base {ntdll_base:#x}")
    chemin_ntdll = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"),
                                "System32", "ntdll.dll")
    sha_ntdll = sha256_fichier(chemin_ntdll)
    temoin(f"[env] ntdll : {chemin_ntdll}")
    temoin(f"[env] ntdll sha256 : {sha_ntdll}")
    octets_page = ctypes.string_at(ntdll_base, 16)
    verifie("T0.ntdll : le motif MZ de la base", octets_page[:2] == b"MZ",
            f"{octets_page[:8].hex()}")

    # la cartographie de l'artefact : DONT_RESOLVE (aucune entrée résolue,
    # AUCUN point d'entrée appelé — le scénario est le chargeur, jamais
    # l'exécutant de l'artefact entier)
    base = k32.LoadLibraryExW(chemin_proxy, None, DONT_RESOLVE_DLL_REFERENCES)
    verifie("T0.carte : l'artefact cartographié", bool(base), f"base {base:#x}")
    if not base:
        print(f"ÉCHEC NOMMÉ : LoadLibraryEx a rendu "
              f"{ctypes.get_last_error()}")
        return 1

    # les octets attendus, constatés UN PAR UN avant tout appel (la carte
    # génération 8 lue sur la machine réelle)
    verifie("T0.sys-01 : le trombone ABI",
            ctypes.string_at(base + R_SYS01, 6) == OCTETS_SYS01,
            f"{ctypes.string_at(base + R_SYS01, 6).hex()}")
    verifie("T0.fixture-nom : le span « NtWriteFile »",
            ctypes.string_at(base + R_FIXTURE_NOM, 11) == FIXTURE_NOM,
            f"{ctypes.string_at(base + R_FIXTURE_NOM, 11).decode('ascii')}")
    verifie("T0.fixture-ligne : les 33 octets du M0",
            ctypes.string_at(base + R_FIXTURE_LIGNE, 33) == FIXTURE_LIGNE,
            f"{ctypes.string_at(base + R_FIXTURE_LIGNE, 33)!r}")
    # le slot IAT : la IA d'origine pointe le nom « WriteFile » (R7 —
    # vérifié sur la table d'imports AVANT la résolution par le chargeur)
    ia_originale = struct.unpack("<Q",
                                 ctypes.string_at(base + R_IAT_WRITEFILE, 8))[0]
    verifie("T0.IAT : le slot WriteFile non résolu (la IA d'origine)",
            0 < ia_originale < base, f"IA {ia_originale:#x}")
    if 0 < ia_originale < base:
        indice = ctypes.string_at(base + ia_originale + 2, 12)
        verifie("T0.IAT : le nom visé par la IA est bien « WriteFile »",
                indice.split(b"\x00")[0] == b"WriteFile",
                f"{indice.split(b'\x00')[0].decode('ascii', 'replace')!r}")
    # le geste du chargeur : la section exécutable réaffirmée, le slot résolu
    ancien = wt.DWORD()
    k32.VirtualProtect(base + R_SYS01, 0x2000, PAGE_EXECUTE_READ,
                       ctypes.byref(ancien))
    k32.VirtualProtect(base + R_HELLO02, 0x40, PAGE_EXECUTE_READ,
                       ctypes.byref(ancien))
    writefile_addr = k32.GetProcAddress(k32.GetModuleHandleW("kernel32"),
                                        b"WriteFile")
    verifie("T0.IAT : kernel32!WriteFile résolu par le chargeur",
            bool(writefile_addr), f"@{writefile_addr:#x}")
    k32.VirtualProtect(base + R_IAT_WRITEFILE, 8, PAGE_READWRITE,
                       ctypes.byref(ancien))
    ctypes.memmove(base + R_IAT_WRITEFILE,
                   ctypes.byref(ctypes.c_void_p(writefile_addr)), 8)
    k32.VirtualProtect(base + R_IAT_WRITEFILE, 8, ancien.value,
                       ctypes.byref(ancien))
    slot = struct.unpack("<Q", ctypes.string_at(base + R_IAT_WRITEFILE, 8))[0]
    verifie("T0.IAT : le slot porte kernel32!WriteFile", slot == writefile_addr,
            f"@{slot:#x}")

    empreinte_entete_ntdll = hashlib.sha256(
        ctypes.string_at(ntdll_base, 0x1000)).hexdigest()
    hello02, sys02, sys03 = lier_blocs(base)

    # ---------------- T1 — LA LECTURE DU VRAI ntdll ---------------------------
    print("\nT1 — LA LECTURE (deux lecteurs indépendants, le motif confronté)")
    verdict_py, stub_rva, detail_py = lire_ssn_python(
        ntdll_base, FIXTURE_NOM, len(FIXTURE_NOM))
    verifie("T1.python : la marche EAT en Python trouve « NtWriteFile »",
            verdict_py == 0, detail_py or f"stub RVA {stub_rva:#x}")
    ssn_attendu, octets_stub = None, b""
    if verdict_py == 0:
        ok_motif, ssn_attendu, detail_stub = confronter_stub(ntdll_base, stub_rva)
        octets_stub = ctypes.string_at(ntdll_base + stub_rva, 16)
        verifie("T1.motif : le stub du VRAI ntdll confronté (4C 8B D1 B8 "
                "avant l'imm32)", ok_motif,
                detail_stub or f"@{ntdll_base + stub_rva:#x} : "
                               f"{octets_stub[:8].hex()}")
        temoin(f"[pièce] SSN(NtWriteFile) lu par Python : {ssn_attendu} "
               f"({ssn_attendu:#x})")

    ssn_bloc = sys02(base + R_FIXTURE_NOM, len(FIXTURE_NOM), ntdll_base)
    verifie("T1.sys-02 : le bloc rend un SSN positif", ssn_bloc >= 0,
            f"rax = {ssn_bloc}")
    if ssn_attendu is not None and ssn_bloc >= 0:
        verifie("T1.parité : LE MÊME SSN par les DEUX lecteurs",
                ssn_bloc == ssn_attendu,
                f"bloc {ssn_bloc} == python {ssn_attendu}")

    # le second nom — jamais un numéro en cache (chaque appel résout)
    verdict_py2, stub_rva2, detail_py2 = lire_ssn_python(
        ntdll_base, NOM_SECONDAIRE, len(NOM_SECONDAIRE))
    tampon_nom2 = ctypes.create_string_buffer(NOM_SECONDAIRE)
    ssn_bloc2 = sys02(ctypes.addressof(tampon_nom2), len(NOM_SECONDAIRE),
                      ntdll_base)
    if verdict_py2 == 0:
        ok2, ssn2, _ = confronter_stub(ntdll_base, stub_rva2)
        verifie("T1.second-nom : « NtReadFile » résolu par les DEUX lecteurs",
                ok2 and ssn_bloc2 == ssn2,
                f"bloc {ssn_bloc2} == python {ssn2}")
        verifie("T1.distincts : les DEUX SSN sont distincts (jamais un "
                "numéro en cache)", ssn_bloc != ssn_bloc2,
                f"NtWriteFile {ssn_bloc} != NtReadFile {ssn_bloc2}")

    # la falsification invitée : un module forgé au stub crocheté → -4 NOMMÉ
    adresse_forgé, _garde_forgé = forger_module_crochete()
    verdict_forgé = sys02(base + R_FIXTURE_NOM, len(FIXTURE_NOM), adresse_forgé)
    verifie("T1.falsification : le stub crocheté est REFUSÉ nommément (-4)",
            verdict_forgé == -4, f"rax = {verdict_forgé}")

    empreinte_apres = hashlib.sha256(
        ctypes.string_at(ntdll_base, 0x1000)).hexdigest()
    octets_stub_apres = ctypes.string_at(ntdll_base + stub_rva, 16)
    verifie("T1.I8 : le VRAI ntdll n'est pas touché (entête + stub relus "
            "inchangés)",
            empreinte_apres == empreinte_entete_ntdll
            and octets_stub_apres == octets_stub)

    # ---------------- T2 — LA TWIN (les DEUX chemins) -------------------------
    print("\nT2 — LA TWIN (la même ligne par hello-02 [IAT] et sys-03 [syscall])")
    chemin_a = os.path.join(PREUVES, "chemin-a-hello02.txt")
    chemin_b = os.path.join(PREUVES, "chemin-b-sys03.txt")
    h_a = k32.CreateFileW(chemin_a, GENERIC_WRITE, 0, None, CREATE_ALWAYS,
                          FILE_ATTRIBUTE_NORMAL, None)
    h_b = k32.CreateFileW(chemin_b, GENERIC_WRITE, 0, None, CREATE_ALWAYS,
                          FILE_ATTRIBUTE_NORMAL, None)
    verifie("T2.poignées : les deux fichiers d'écriture ouverts",
            h_a not in (None, INVALID_HANDLE_VALUE)
            and h_b not in (None, INVALID_HANDLE_VALUE))

    verdict_a = hello02(h_a, base + R_FIXTURE_LIGNE, len(FIXTURE_LIGNE))
    verifie("T2.chemin-A : hello-02 par l'IAT (kernel32!WriteFile)",
            verdict_a != 0, f"BOOL = {verdict_a}")
    k32.CloseHandle(h_a)

    verdict_b = sys03(ntdll_base, h_b)
    verifie("T2.chemin-B : sys-03 par NtWriteFile en syscall direct",
            verdict_b == 0, f"rax = {verdict_b}")
    k32.CloseHandle(h_b)

    octets_a = open(chemin_a, "rb").read()
    octets_b = open(chemin_b, "rb").read()
    verifie("T2.chemin-A : la ligne est le fixture (33 octets)",
            octets_a == FIXTURE_LIGNE, f"{len(octets_a)} o · {octets_a!r}")
    verifie("T2.chemin-B : la ligne est le fixture (33 octets)",
            octets_b == FIXTURE_LIGNE, f"{len(octets_b)} o · {octets_b!r}")
    verifie("T2.TWIN : la MÊME ligne par les DEUX chemins, octet pour octet",
            octets_a == octets_b == FIXTURE_LIGNE,
            f"sha(a) == sha(b) == {hashlib.sha256(octets_a).hexdigest()[:16]}…")

    # ---------------- T3 — LES GARDES ------------------------------------------
    print("\nT3 — LES GARDES (la base invalide, l'intégrité)")
    chemin_c = os.path.join(PREUVES, "chemin-c-refus.txt")
    h_c = k32.CreateFileW(chemin_c, GENERIC_WRITE, 0, None, CREATE_ALWAYS,
                          FILE_ATTRIBUTE_NORMAL, None)
    pas_un_module = ctypes.create_string_buffer(b"PAS-UN-MODULE-PE-"
                                                b"AAAAAAAAAAAAAAAA" * 64)
    verdict_invalide = sys03(ctypes.addressof(pas_un_module), h_c)
    k32.CloseHandle(h_c)
    octets_c = open(chemin_c, "rb").read()
    verifie("T3.refus-nommé : la base non-PE rend -1 (jamais un appel au "
            "numéro deviné)", verdict_invalide == -1, f"rax = {verdict_invalide}")
    verifie("T3.I5 : AUCUN syscall émis sur l'échec (le fichier-témoin "
            "demeure VIDE)", octets_c == b"", f"{len(octets_c)} o")

    sha_relu = sha256_fichier(chemin_proxy)
    verifie("T3.intégrité : proxy.exe relu inchangé", sha_relu == SHA_PROXY,
            f"sha256 {sha_relu[:16]}…")
    k32.FreeLibrary(base)
    temoin("[ok] T3.libération : la cartographie rendue au système")

    # ---------------- LE VERDICT ------------------------------------------------
    verdict = "VERT" if not _echecs else "ROUGE"
    ssn_ligne = (f"SSN(NtWriteFile) : {ssn_attendu} ({ssn_attendu:#x}) — lu "
                 f"par les DEUX lecteurs" if ssn_attendu is not None
                 else "SSN(NtWriteFile) : NON RÉSOLU (voir les échecs)")
    stub_ligne = (f"Stub NtWriteFile : RVA {stub_rva:#x} · "
                  f"@{ntdll_base + stub_rva:#x} · octets "
                  f"{octets_stub.hex()}" if stub_rva else "Stub : non localisé")
    lignes_temoin = [
        "TRIADE — TÉMOIN DU RUN TERRAIN M8-(d) — le VRAI ntdll, la twin, "
        "les DEUX chemins",
        "=" * 78,
        f"Date du run : {time.strftime('%Y-%m-%d %H:%M:%S')} (heure locale)",
        f"Machine : Windows {wv.major}.{wv.minor} build {wv.build} · "
        f"Python {platform.python_version()} · {platform.machine()}",
        f"ntdll : base {ntdll_base:#x} · {chemin_ntdll}",
        f"ntdll sha256 : {sha_ntdll}",
        f"Artefact : proxy.exe 0.9.0-dev.1 · {TAILLE_PROXY} o",
        f"Artefact sha256 : {sha_proxy}",
        ssn_ligne,
        stub_ligne,
        "",
    ] + _temoin + [
        "",
        f"Contrôles : {len(_temoin) - len(_echecs)} verts · "
        f"{len(_echecs)} échecs"
        + (f" ({', '.join(_echecs)})" if _echecs else ""),
        f"VERDICT : {verdict}",
    ]
    with open(os.path.join(PREUVES, "temoin-m8d.txt"), "w",
              encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lignes_temoin) + "\n")
    with open(os.path.join(PREUVES, "scenario-m8d-journal.log"), "w",
              encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(_journal) + "\n")
    with open(os.path.join(PREUVES, "VERDICT-run-m8d.txt"), "w",
              encoding="utf-8", newline="\r\n") as f:
        f.write(f"M8-(d) run terrain — VERDICT : {verdict}\n"
                f"Windows build {wv.build} · SSN(NtWriteFile)={ssn_attendu}\n"
                f"La ligne : identique par les DEUX chemins "
                f"({'oui' if octets_a == octets_b == FIXTURE_LIGNE else 'NON'})\n")

    print("\n" + "=" * 78)
    print(f"VERDICT : {verdict} — {len(_temoin) - len(_echecs)} verts, "
          f"{len(_echecs)} échecs")
    if _echecs:
        print("Échecs nommés : " + ", ".join(_echecs))
    print(f"Les pièces vivent dans : {PREUVES}")
    print("À renvoyer ENTIÈRES au coffre /test/preuves-m8d/ (dossier Drive "
          "« Triade » → « test »).")
    return 0 if not _echecs else 1


if __name__ == "__main__":
    sys.exit(main())
