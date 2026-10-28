#!/usr/bin/env python3
"""build_terrain.py — Jalon terrain TRIADE : le superviseur (D48).

superviseur.exe (PE32+ WINDOWS_GUI écrit à la main) : TOUS les tests du
projet en UN clic (T1 démo M2, T2 proxy M3, T3 envoi Drive) et le journal
du run téléversé dans le dossier test du Drive par relais curl.exe —
l'exigence du développeur, exécutable par exécutable.

La chaîne réutilise build_demo.py (assemblage, round-trip, canon, PE, cartes)
— le superviseur est une EXTENSION de la lignée démo : mêmes IAT scellées
(kernel32#1, user32, gdi32, kernel32#2), NOUVELLES IAT kernel32#3 et user32#2
dans l'ancienne zone ws2_32 libérée (le superviseur n'a pas de sockets : le
réseau vit dans les processus testés et dans curl.exe), table R10 étendue aux
zones de données sup (D48 — l'intégrité couvre les gabarits Drive).

Usage :
  python3 build_terrain.py                       # construction + oracle + carte
  python3 build_terrain.py --verifier [--graine N]        # R5/R8
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import struct
import sys
from datetime import datetime, timezone

ICI = os.path.dirname(os.path.abspath(__file__))
DEMO_DIR = os.path.join(os.path.dirname(ICI), "demo")
M2_DIR = os.path.join(os.path.dirname(ICI), "m2")
sys.path.insert(0, M2_DIR)
sys.path.insert(0, DEMO_DIR)
sys.path.insert(0, ICI)

# Trois plans cohabitent : m2 (héritage, requis par build_m2/build_demo) et
# terrain. Isolation par noms distincts dans sys.modules.
import importlib.util as _ilu
if "layout" not in sys.modules:
    _spec_m2 = _ilu.spec_from_file_location("layout", os.path.join(M2_DIR, "layout.py"))
    sys.modules["layout"] = _ilu.module_from_spec(_spec_m2)
    _spec_m2.loader.exec_module(sys.modules["layout"])
import build_m2 as bm                    # chaîne scellée M2 (réutilisation)
import build_demo as bd                  # chaîne scellée démo (héritage win-*)
_spec_demo = _ilu.spec_from_file_location("layout_demo", os.path.join(DEMO_DIR, "layout.py"))
if "layout_demo" not in sys.modules:
    _mod = _ilu.module_from_spec(_spec_demo)
    _spec_demo.loader.exec_module(_mod)
    sys.modules["layout_demo"] = _mod
_spec = _ilu.spec_from_file_location("layout_terrain", os.path.join(ICI, "layout.py"))
L = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(L)
sys.modules["layout_terrain"] = L

import carte_terrain as cm
import oracle_terrain as od

import capstone
import pefile
from keystone import Ks, KS_ARCH_X86, KS_MODE_64

M0_DIR = bm.M0_DIR
M1_DIR = bm.M1_DIR
M3_DIR = os.path.join(os.path.dirname(ICI), "m3")


class EchecBuild(Exception):
    pass


# --- Blocs embarqués dans superviseur.exe -----------------------------------------

# id carte -> fichier de notation (l'héritage lit les artefacts scellés, les
# blocs sup lisent terrain/notation — générés par outils/auteur.py)
NOTATION = {
    "a10002": "hello-02-write", "a10003": "hello-03-exit",
    "b20001": "libc-01-memcpy", "b20002": "libc-02-memcmp",
    "b20003": "libc-03-strlen", "b20004": "libc-04-itoa",
    "d40003": "win-03-boucle", "d40004": "win-04-procedure",
    "d40006": "win-06-autotest", "d40005": "win-05-journal",
    "c30006": "tcp-06-spawn",
    "f60001": "sup-01-principal", "f60002": "sup-02-fenetre",
    "f60021": "sup-21-horodatage", "f60022": "sup-22-balaye",
    "f60011": "sup-11-journal", "f60009": "sup-09-scenario",
    "f60031": "sup-31-lancer", "f60036": "sup-36-fichiers",
    "f60033": "sup-33-demo", "f60034": "sup-34-proxy", "f60035": "sup-35-envoi",
    "f60037": "sup-37-extraction",
}

FICHIERS_I = {
    "hello-02": "hello-02-write.md", "hello-03": "hello-03-exit.md",
    "libc-01": "libc-01-memcpy.md", "libc-02": "libc-02-memcmp.md",
    "libc-03": "libc-03-strlen.md", "libc-04": "libc-04-itoa.md",
    "win-03": "win-03-boucle.md", "win-04": "win-04-procedure.md",
    "win-05": "win-05-journal.md", "win-06": "win-06-autotest.md",
    "tcp-06": "tcp-06-spawn.md",
    "sup-01": "sup-01-principal.md", "sup-02": "sup-02-fenetre.md",
    "sup-09": "sup-09-scenario.md", "sup-11": "sup-11-journal.md",
    "sup-21": "sup-21-horodatage.md", "sup-22": "sup-22-balaye.md",
    "sup-31": "sup-31-lancer.md", "sup-33": "sup-33-demo.md",
    "sup-34": "sup-34-proxy.md", "sup-35": "sup-35-envoi.md",
    "sup-36": "sup-36-fichiers.md", "sup-37": "sup-37-extraction.md",
}


def blocs_terrain() -> list[tuple]:
    """(id carte, spec, fichier notation, rva, slot) — depuis le plan."""
    return [(bid, spec, NOTATION[bid], rva, slot)
            for bid, spec, rva, slot, _gen, _v in L.BLOCS_TERRAIN]


def chemin_notation(fichier: str) -> str:
    if fichier.startswith("hello-"):
        return os.path.join(M0_DIR, "notation", fichier + ".asm")
    if fichier.startswith("libc-"):
        return os.path.join(M1_DIR, "notation", fichier + ".asm")
    if fichier.startswith("tcp-"):
        return os.path.join(M2_DIR, "notation", fichier + ".asm")
    if fichier.startswith("win-"):
        return os.path.join(DEMO_DIR, "notation", fichier + ".asm")
    return os.path.join(ICI, "notation", fichier + ".asm")


def _chemin_spec(ident: str) -> str:
    if ident.startswith("hello-"):
        return os.path.join(M0_DIR, "I", FICHIERS_I[ident])
    if ident.startswith("libc-"):
        return os.path.join(M1_DIR, "I", FICHIERS_I[ident])
    if ident.startswith("tcp-"):
        return os.path.join(M2_DIR, "I", FICHIERS_I[ident])
    if ident.startswith("win-"):
        return os.path.join(DEMO_DIR, "I", FICHIERS_I[ident])
    return os.path.join(ICI, "I", FICHIERS_I[ident])


def charger_couche_I(blocs: list[tuple]) -> dict[str, dict]:
    specs = {}
    for bid, sid, _f, _rva, _slot in blocs:
        ident, rev_ref = sid.split(":")
        rev_ref = int(rev_ref[1:])
        chemin = _chemin_spec(ident)
        if not os.path.exists(chemin):
            raise EchecBuild(f"spécification I introuvable pour {sid} : {chemin}")
        spec = bm.lire_spec(chemin)
        if spec["id"] != ident:
            raise EchecBuild(f"{chemin} : identifiant {spec['id']} != {ident}")
        if rev_ref > spec["rev"]:
            raise EchecBuild(f"{chemin} : révision référencée R{rev_ref} > fichier R{spec['rev']}")
        specs[bid] = spec
    return specs


# --- Oracle structurel : autorisations PAR BLOC (I1/I2, héritage + terrain) ------

_HERITAGE = {"a10002", "a10003", "b20001", "b20002", "b20003", "b20004",
             "c30006", "d40003", "d40004", "d40005", "d40006"}

SUP = L.CHAINES_SUP
AD = L.CHAINES_ASCII

IAT_PAR_BLOC = {
    **{k: v for k, v in bd.IAT_PAR_BLOC.items() if k in _HERITAGE},
    "f60001": set(),
    "f60002": {"CreateWindowExW", "GetLastError", "GetModuleHandleW",
               "LoadCursorW", "MessageBoxW", "RegisterClassExW"},
    "f60021": {"GetLocalTime"},
    "f60022": set(),
    "f60011": {"CreateFileA", "FlushFileBuffers", "GetModuleFileNameA", "WriteFile"},
    "f60009": set(),
    "f60031": {"CloseHandle", "CreatePipe", "CreateProcessA", "GetModuleFileNameA"},
    "f60033": {"CloseHandle", "FindWindowExW", "FindWindowW", "GetExitCodeProcess",
               "SendMessageTimeoutW", "Sleep", "TerminateProcess", "WaitForSingleObject"},
    "f60034": {"CloseHandle", "GetExitCodeProcess", "PeekNamedPipe", "ReadFile",
               "Sleep", "TerminateProcess", "WaitForSingleObject", "WriteFile"},
    "f60035": {"CloseHandle", "GetExitCodeProcess", "WaitForSingleObject"},
    "f60036": {"CloseHandle", "CreateFileA", "DeleteFileA", "ReadFile", "WriteFile"},
    "f60037": {"CloseHandle", "CreateFileA", "ReadFile", "WriteFile"},
}
APPELS_DIRECTS = {
    **{k: v for k, v in bd.APPELS_DIRECTS.items() if k in _HERITAGE},
    "f60001": {0x1080, 0x1440, 0x15C0, 0x1C40},                  # exit, fenêtre, boucle, horodatage
    "f60002": {L.JOURNAL_TRACE},
    "f60021": {0x1100},
    "f60022": {0x1100, 0x1180},
    "f60011": {0x1100, 0x1200, 0x1280},
    "f60009": {0x1AC0, L.JOURNAL_TRACE, 0x5400, 0x5800, 0x5E00, L.EXTRACTION},  # porte + trace + kit + T1/T2/T3
    "f60031": set(),
    "f60033": {0x1180, 0x4E00, L.JOURNAL_TRACE, 0x5200},          # memcmp, fichiers, trace, lanceur
    "f60034": {0x1180, 0x4E00, L.JOURNAL_TRACE, 0x5200},
    "f60035": {0x1100, 0x1D40, 0x4E00, L.JOURNAL_TRACE, 0x5200},  # memcpy, balayeur, fichiers, trace, lanceur
    "f60036": {0x1100, 0x1200},
    "f60037": {0x1100, 0x1180, 0x1200, 0x4E00, L.JOURNAL_TRACE},  # memcpy, memcmp, strlen, fichiers, trace
}
DONNEES_RIP = {
    **{k: v for k, v in bd.DONNEES_RIP.items() if k in _HERITAGE},
    "f60001": set(),
    "f60002": {0x1640, L.CHAINES_UTF16["CLASSE"][0], L.CHAINES_UTF16["TITRE"][0],
               L.CHAINES_UTF16["MSG_ECHEC_GUI"][0], L.HWND_PRINCIPAL,
               AD["L00"][0], AD["L01"][0], AD["LKO_GUI"][0]},
    "f60021": {L.TAMPON_NOM, L.TAMPON_AFF},
    "f60022": set(),
    "f60011": {L.R_JOURNAL_HANDLE, L.BUF_CONV, L.BUF_CHEMIN, L.SCRATCH_ECRIT,
               L.TAMPON_NOM},
    "f60009": {L.TAMPON_AFF, SUP["S00"][0], SUP["S02A"][0], SUP["S02B"][0],
               SUP["S03A"][0], SUP["S03B"][0], SUP["S90"][0], SUP["S91"][0]},
    "f60031": {L.HPROC, L.TUYAU_IN_RD, L.TUYAU_OUT_WR},
    "f60033": {L.CHAINES_UTF16["CLASSE_BOUTON"][0], L.CHAINES_UTF16["CLASSE_DEMO"][0],
               AD["NOM_DEMO"][0], L.HPROC, L.HWND_DEMO, L.CODE_SORTIE, L.LU,
               L.TAMPON_CMD,
               *[SUP[n][0] for n in ("S10", "S10B", "S11A", "S11B", "S12A", "S12B",
                                     "S13", "S14", "S15A", "S15B", "S16A", "S16B")],
               SUP["FIX_FINAL_DEMO"][0], SUP["NOM_JOURNAL_DEMO"][0]},
    "f60034": {AD["NOM_PROXY"][0], AD["QUIT"][0], L.HPROC, L.DRAPEAU_SRV, L.TUYAU_IN_WR,
               L.TUYAU_OUT_RD, L.CODE_SORTIE, L.LU, L.DISPO, L.TAMPON_CMD,
               *[SUP[n][0] for n in ("S20", "S20B", "S21A", "S21B", "S22A", "S22B",
                                     "S23", "S24", "S25", "S26", "S27A", "S27B",
                                     "S28A", "S28B")],
               SUP["FIX_BANNIERE"][0], SUP["FIX_EVT_HTTP"][0], SUP["FIX_EVT_HTTPS"][0],
               SUP["FIX_ARRET"][0], SUP["NOM_PAGE_HTTP"][0], SUP["NOM_PAGE_HTTPS"][0],
               SUP["CMD_CURL_HTTP"][0], SUP["CMD_CURL_HTTPS"][0]},
    "f60035": {L.BUF_CHEMIN, L.TAMPON_NOM, L.HPROC, L.CODE_SORTIE, L.TAMPON_JETON,
               L.TAMPON_CMD, L.TAMPON_COMPO,
               *[SUP[n][0] for n in ("S30", "S31", "S32", "S33A", "S33B", "S34A",
                                     "S34B", "S35A", "S35B", "S36A", "S36B")],
               SUP["ETIQ_TOKEN"][0], SUP["ETIQ_LOCATION"][0], SUP["DOSSIER_TEST"][0],
               SUP["GABARIT_OAUTH"][0], SUP["GABARIT_META"][0], SUP["GABARIT_JETON"][0],
               SUP["GABARIT_SESSION"][0], SUP["GABARIT_PUT"][0],
               SUP["NOM_JETONS"][0], SUP["NOM_REQ"][0], SUP["NOM_JETON_JSON"][0],
               SUP["NOM_META"][0], SUP["NOM_SESSION"][0]},
    "f60036": {L.BUF_CHEMIN, L.LU, L.DIR_LONG, L.TAMPON_CMD, L.TAMPON_COMPO},
    "f60037": {L.BUF_CHEMIN, L.LU, L.DIR_LONG, L.SCRATCH_ECRIT, L.TAMPON_CMD,
               L.TAMPON_COMPO, L.BLOB_LONGUEURS, L.BLOB_LONGUEUR_PROXY,
               L.BLOB_DEMO, L.BLOB_PROXY, L.SLOT_JETONS,
               AD["NOM_DEMO"][0], AD["NOM_PROXY"][0], SUP["NOM_JETONS"][0],
               *[SUP[n][0] for n in ("S04A", "S04B", "S04C", "S04D",
                                     "S05A", "S05B", "S05C", "S05D",
                                     "S06A", "S06B", "S06C", "S07A")]},
}


def oracle_structurel(specs: dict, code: dict, blocs: list[tuple]) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    tous = list(blocs)
    adresses_insns = {bid: {i.address for i in code[bid]["insns"]} for bid, *_ in tous}
    adresses_blocs = {bid: rva for bid, _, _, rva, _ in tous}

    for bid, _, _, rva, slot in tous:
        insns = code[bid]["insns"]
        for i in insns:
            if i.mnemonic == "jmp" and i.op_str.startswith("0x"):
                cible = int(i.op_str, 16)
                verrou(f"{bid}:jmp-autorise@{i.address:#x}",
                       cible in APPELS_DIRECTS.get(bid, set())
                       or cible in adresses_insns[bid],
                       f"cible {cible:#x} hors blocs déclarés (I1)")
            elif i.mnemonic.startswith("j"):
                verrou(f"{bid}:saut-interne@{i.address:#x}",
                       int(i.op_str, 16) in adresses_insns[bid])
            if i.mnemonic == "call":
                if "rip" in i.op_str:
                    cible = bm.operande_rip_cible(i)
                    slot_iat = {L.IAT_SLOTS[n]: n for n in L.IAT_SLOTS}
                    verrou(f"{bid}:iat-autorisee@{i.address:#x}",
                           cible in slot_iat and slot_iat[cible] in IAT_PAR_BLOC.get(bid, set()),
                           f"cible {cible:#x} hors IAT déclarée (I1)")
                elif i.op_str.startswith("0x"):
                    cible = int(i.op_str, 16)
                    interne = cible in adresses_insns[bid] and cible != adresses_blocs[bid]
                    verrou(f"{bid}:appel-autorise@{i.address:#x}",
                           cible in APPELS_DIRECTS.get(bid, set()) or interne,
                           f"cible {cible:#x} hors blocs déclarés (I1)")
        for i in insns:
            cible = bm.operande_rip_cible(i)
            if cible is not None and i.mnemonic != "call":
                verrou(f"{bid}:donnees-autorisees@{i.address:#x}",
                       cible in DONNEES_RIP.get(bid, set()),
                       f"cible {cible:#x} hors données déclarées (I2/I5)")
        verrou(f"{bid}:pas-de-syscall",
               not any(m.mnemonic in ("syscall", "sysenter", "int") for m in insns))
        fin_code = insns[-1].address + insns[-1].size
        verrou(f"{bid}:padding-16", rva + slot - fin_code >= 16, f"écart {rva + slot - fin_code}")
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)
        verrou(f"{bid}:slot-multiple-64", slot % 64 == 0)
        verrou(f"{bid}:pile-alignee", bm._prologue_aligne(insns))

    def canon_(i):
        return bm.canon(f"{i.mnemonic} {i.op_str}")

    # sup-01 : l'horodatage AVANT la fenêtre (Q1 — le journal naît avec son nom)
    s1 = [canon_(i) for i in code["f60001"]["insns"]]
    hor = s1.index("call 0x1c40")
    fen = s1.index("call 0x1440")
    verrou("f60001:horodatage-avant-fenetre", hor < fen,
           "le journal s'ouvrirait sans nom (D48)")

    # sup-09 : la porte R10 précède tout test (I4, héritage win-09)
    s9 = code["f60009"]["insns"]
    premier_test = next((k for k, i in enumerate(s9)
                         if canon_(i) in ("call 0x5400", "call 0x5800", "call 0x5c00")), None)
    porte = next((k for k, i in enumerate(s9) if canon_(i) == "call 0x1ac0"), None)
    verrou("f60009:porte-avant-tests", premier_test is not None and porte is not None
           and porte < premier_test, "la porte doit précéder T1/T2/T3 (R10)")

    # win-06 : porte R10 avant tout appel (I1) — miroir tcp-12
    a6 = code["d40006"]["insns"]
    premier_appel = next((k for k, i in enumerate(a6) if i.mnemonic == "call"), None)
    marqueur = [k for k, i in enumerate(a6) if canon_(i) == "add r12, 0x10"]
    verrou("d40006:porte-avant-tout-appel",
           premier_appel is not None and marqueur and premier_appel > marqueur[-1])
    verrou("tracabilite-I",
           set(specs) >= {b for b, *_ in blocs})
    return verrous


# --- Composition des sections -----------------------------------------------------

def composer_sections(code: dict, blocs: list[tuple], blob: bytes):
    texte = bytearray(b"\xcc" * L.TEXT_VSIZE)
    text2 = bytearray(b"\xcc" * L.TEXT2_VSIZE)

    def deposer(rva: int, donnees: bytes, base: bytearray, base_rva: int, nom=""):
        fin = rva + len(donnees)
        if rva < base_rva or fin > base_rva + len(base):
            raise EchecBuild(f"débordement de section : {nom or hex(rva)} "
                             f"({rva:#x}..{fin:#x})")
        base[rva - base_rva: rva - base_rva + len(donnees)] = donnees

    for bid, _, _, rva, slot in blocs:
        if rva >= L.TEXT2_RVA:
            deposer(rva, code[bid]["slot"], text2, L.TEXT2_RVA, bid)
        else:
            deposer(rva, code[bid]["slot"], texte, L.TEXT_RVA, bid)

    # --- zones données sup (.text2, RX — l'espace .rdata est épuisé, D48) -----
    for nom, (adr, octets, _n) in L.CHAINES_SUP.items():
        deposer(adr, octets, text2, L.TEXT2_RVA, "SUP:" + nom)

    # --- INT/hints kernel32#3 + user32#2 (en fin de zone 2, D48) --------------
    hn = lambda nom: struct.pack("<H", 0) + nom.encode("ascii") + b"\x00"

    def poser_hints(noms, rva_depart):
        rva = rva_depart
        table = {}
        for nom in noms:
            deposer(rva, hn(nom), text2, L.TEXT2_RVA, "hint:" + nom)
            table[nom] = rva
            rva += len(hn(nom))
        return table

    hints_k32c = poser_hints(L.KERNEL32C_IMPORTS, L.R_HN_K32C)
    hints_u32b = poser_hints(L.USER32B_IMPORTS, L.R_HN_U32B)
    deposer(L.R_INT_K32C, b"".join(struct.pack("<Q", hints_k32c[n]) for n in L.KERNEL32C_IMPORTS)
            + struct.pack("<Q", 0), text2, L.TEXT2_RVA, "INT k32c")
    deposer(L.R_INT_U32B, b"".join(struct.pack("<Q", hints_u32b[n]) for n in L.USER32B_IMPORTS)
            + struct.pack("<Q", 0), text2, L.TEXT2_RVA, "INT u32b")

    # --- .rdata ------------------------------------------------------------
    rdata = bytearray(b"\x00" * L.RDATA_VSIZE)
    _poses = []

    def poser(rva: int, donnees: bytes, nom: str = ""):
        fin = rva + len(donnees)
        if rva - L.RDATA_RVA + len(donnees) > L.RDATA_VSIZE:
            raise EchecBuild(f".rdata débordante à {rva:#x} ({nom})")
        for rva_p, fin_p, nom_p in _poses:
            if rva < fin_p and rva_p < fin:
                raise EchecBuild(f"chevauchement .rdata : {nom or hex(rva)} "
                                 f"recouvre {nom_p}")
        _poses.append((rva, fin, nom or hex(rva)))
        rdata[rva - L.RDATA_RVA: rva - L.RDATA_RVA + len(donnees)] = donnees

    # marché des imports : SIX descripteurs + terminateur (D48) — la table des
    # descripteurs vit @0x2380 (l'ancrage démo @0x2030 chevaucherait l'IAT
    # kernel32#1 scellée @0x20B0 — défaut latent corrigé avant la notation)
    poser(L.R_DESC_IMPORT, struct.pack("<IIIII", L.R_INT_KERNEL32, 0, 0, L.R_NOM_DLL, L.R_IAT))
    poser(L.R_DESC_USER32, struct.pack("<IIIII", L.R_INT_USER32, 0, 0, L.R_NOM_USER32, L.R_IAT_USER32))
    poser(L.R_DESC_GDI32, struct.pack("<IIIII", L.R_INT_GDI32, 0, 0, L.R_NOM_GDI32, L.R_IAT_GDI32))
    poser(L.R_DESC_K32B, struct.pack("<IIIII", L.R_INT_K32B, 0, 0, L.R_NOM_DLL, L.R_IAT_K32B))
    poser(L.R_DESC_K32C, struct.pack("<IIIII", L.R_INT_K32C, 0, 0, L.R_NOM_DLL, L.R_IAT_K32C))
    poser(L.R_DESC_U32B, struct.pack("<IIIII", L.R_INT_U32B, 0, 0, L.R_NOM_USER32, L.R_IAT_U32B))
    poser(L.R_DESC_TERM, b"\x00" * 20)

    poser(L.R_NOM_DLL, b"kernel32.dll\x00")
    poser(L.R_NOM_USER32, b"user32.dll\x00")
    poser(L.R_NOM_GDI32, b"gdi32.dll\x00")

    hints_k32 = {"GetStdHandle": L.R_HN_GSH, "WriteFile": L.R_HN_WF,
                 "ExitProcess": L.R_HN_EP, "CreateThread": L.R_HN_CT,
                 "VirtualProtect": L.R_HN_VP, "InitializeCriticalSection": L.R_HN_ICS,
                 "EnterCriticalSection": L.R_HN_ECS, "LeaveCriticalSection": L.R_HN_LCS,
                 "ReadFile": L.R_HN_RF, "CloseHandle": L.R_HN_CH,
                 "GetModuleHandleW": L.R_HN_GMH}
    for rva_h, nom in ((L.R_HN_GSH, "GetStdHandle"), (L.R_HN_WF, "WriteFile"),
                       (L.R_HN_EP, "ExitProcess"), (L.R_HN_CT, "CreateThread"),
                       (L.R_HN_VP, "VirtualProtect"), (L.R_HN_ICS, "InitializeCriticalSection"),
                       (L.R_HN_ECS, "EnterCriticalSection"), (L.R_HN_LCS, "LeaveCriticalSection"),
                       (L.R_HN_RF, "ReadFile"), (L.R_HN_CH, "CloseHandle"),
                       (L.R_HN_GMH, "GetModuleHandleW")):
        poser(rva_h, hn(nom))
    poser(L.R_INT_KERNEL32, b"".join(struct.pack("<Q", hints_k32[n]) for n in L.KERNEL32_IMPORTS)
          + struct.pack("<Q", 0))
    poser(L.R_IAT, b"".join(struct.pack("<Q", hints_k32[n]) for n in L.KERNEL32_IMPORTS)
          + struct.pack("<Q", 0))

    hints_u32 = {}
    rva_h = L.R_HN_USER32
    for nom in L.USER32_IMPORTS:
        hints_u32[nom] = rva_h
        poser(rva_h, hn(nom))
        rva_h += len(hn(nom))
    poser(L.R_INT_USER32, b"".join(struct.pack("<Q", hints_u32[n]) for n in L.USER32_IMPORTS)
          + struct.pack("<Q", 0))
    poser(L.R_IAT_USER32, b"".join(struct.pack("<Q", hints_u32[n]) for n in L.USER32_IMPORTS)
          + struct.pack("<Q", 0))

    poser(L.R_INT_GDI32, struct.pack("<Q", L.R_HN_GDI32) + struct.pack("<Q", 0))
    poser(L.R_IAT_GDI32, struct.pack("<Q", L.R_HN_GDI32) + struct.pack("<Q", 0))
    poser(L.R_HN_GDI32, hn("GetStockObject"))

    # kernel32#2 (héritage démo, D36) : hints dans les interstices libres
    hints_k32b = {"GetModuleFileNameA": L.R_HN_GMFA, "CreateFileA": L.R_HN_CFA,
                  "FlushFileBuffers": L.R_HN_FFB, "GetLastError": L.R_HN_GLE}
    for nom, rva_h in hints_k32b.items():
        poser(rva_h, hn(nom))
    poser(L.R_INT_K32B, b"".join(struct.pack("<Q", hints_k32b[n]) for n in L.KERNEL32B_IMPORTS)
          + struct.pack("<Q", 0))
    poser(L.R_IAT_K32B, b"".join(struct.pack("<Q", hints_k32b[n]) for n in L.KERNEL32B_IMPORTS)
          + struct.pack("<Q", 0))

    # table R10 : 23 blocs + 4 zones données (sup 1/2/3 + blob intégrée) +
    # terminateur (D48/D49 — la porte couvre AUSSI les gabarits du canal Drive
    # et la section .blob embarquée, l'emplacement annexe EXCLU : propriété de
    # la variante, seul octet mutable de l'image)
    entrees = []
    for bid, _, _, rva, slot in blocs:
        base = texte if rva < L.TEXT2_RVA else text2
        base_rva = L.TEXT_RVA if rva < L.TEXT2_RVA else L.TEXT2_RVA
        off = rva - base_rva
        entrees.append((rva, slot, bm._somme_qwords(bytes(base[off: off + slot]))))
    for nom_zone in (L.ZONE_DATA_SUP, L.ZONE_DATA_SUP_2, L.ZONE_DATA_SUP_3):
        debut, fin = nom_zone
        tranche = bytes(text2[debut - L.TEXT2_RVA: fin - L.TEXT2_RVA + 1])
        entrees.append((debut, fin - debut + 1, bm._somme_qwords(tranche)))
    debut, fin = L.ZONE_BLOB_INTEG
    tranche = blob[debut - L.BLOB_RVA: fin - L.BLOB_RVA + 1]
    entrees.append((debut, fin - debut + 1, bm._somme_qwords(tranche)))
    entrees.append((0, 0, 0))
    table = b"".join(struct.pack("<IIQ", r, t, s) for r, t, s in entrees)
    if L.R_TAB_SUM + len(table) > L.R_VERSION:
        raise EchecBuild(f"table R10 déborde sur la version "
                         f"({len(entrees)} entrées, {len(table)} octets)")
    poser(L.R_TAB_SUM, table)
    poser(L.R_VERSION, struct.pack("<Q", L.VERSION_U64_TERRAIN3))
    poser(L.R_ANCRE, struct.pack("<Q", 0))
    poser(L.R_FIX_MEMCPY, L.FIXTURE_MEMCPY + L.FIXTURE_MEMCMP_A + L.FIXTURE_STRLEN
          + L.FIXTURE_ITOA)
    poser(L.R_RELOC, struct.pack("<II", L.TEXT_RVA, 12) + struct.pack("<HH", 0, 0))

    for nom, (adr, txt, _n) in L.CHAINES_UTF16.items():
        poser(adr, txt.encode("utf-16-le") + b"\x00\x00", nom)
    for nom, (adr, octets, _n) in L.CHAINES_ASCII.items():
        poser(adr, octets, "ASCII:" + nom)

    data = bytearray(b"\x00" * L.DATA_RAW)
    return bytes(texte), bytes(rdata), bytes(data), bytes(text2)


# --- Kit embarqué + habillage ressources (D49) --------------------------------------

def composer_blob(jetons: bytes | None) -> bytes:
    """Section .blob : en-tête longueurs + demo.exe + proxy.exe scellés +
    emplacement annexe (None/248 o — les DEUX variantes du même code)."""
    with open(os.path.join(DEMO_DIR, "demo.exe"), "rb") as f:
        demo = f.read()
    with open(os.path.join(M3_DIR, "proxy.exe"), "rb") as f:
        proxy = f.read()
    if len(demo) != L.LONGUEUR_DEMO or hashlib.md5(demo).hexdigest().encode() != L.MD5_DEMO_HEXA:
        raise EchecBuild("demo.exe divergent du scellé M2 0.3.0 (md5/longueur)")
    if len(proxy) != L.LONGUEUR_PROXY or hashlib.md5(proxy).hexdigest().encode() != L.MD5_PROXY_HEXA:
        raise EchecBuild("proxy.exe divergent du scellé M3 0.4.0-dev.1 (md5/longueur)")
    if jetons is not None and len(jetons) != L.LONGUEUR_ANNEXE:
        raise EchecBuild(f"annexe de jetons inattendue ({len(jetons)} o != {L.LONGUEUR_ANNEXE})")
    slot = (struct.pack("<Q", len(jetons) if jetons is not None else 0)
            + (jetons if jetons is not None else b"\x00" * L.LONGUEUR_ANNEXE))
    blob = struct.pack("<QQ", L.LONGUEUR_DEMO, L.LONGUEUR_PROXY) + demo + proxy + slot
    if len(blob) != L.BLOB_VSIZE:
        raise EchecBuild(f"section .blob de taille inattendue ({len(blob):#x} != {L.BLOB_VSIZE:#x})")
    return blob


def _noeud_vsi(wtype: int, cle: str, valeur: bytes = b"", enfants: bytes = b"",
               wlen: int | None = None) -> bytes:
    """Nœud VERSIONINFO : wLength calculé, clé UTF-16, alignement 32 bits."""
    tete = (struct.pack("<HHH", 0, len(valeur) if wlen is None else wlen, wtype)
            + cle.encode("utf-16-le") + b"\x00\x00")
    tete += b"\x00" * ((4 - len(tete) % 4) % 4)
    corps = valeur + b"\x00" * ((4 - len(valeur) % 4) % 4) + enfants
    total = tete + corps
    return struct.pack("<H", len(total)) + total[2:]


def _chaine_vsi(cle: str, valeur: str) -> bytes:
    """StringStruct : wValueLength en CARACTÈRES (NUL compris)."""
    return _noeud_vsi(1, cle, valeur.encode("utf-16-le") + b"\x00\x00",
                      wlen=len(valeur) + 1)


def composer_rsrc() -> tuple[bytes, int]:
    """Section .rsrc : arbre ressources (RT_VERSION 16 / RT_MANIFEST 24) +
    VS_VERSIONINFO + manifeste asInvoker — l'habillage légitime du superviseur
    face aux heuristiques antivirus (constat Defender 27/10, D49)."""
    ffi = struct.pack("<13I",
                      0xFEEF04BD,      # signature
                      0x00010000,      # version de structure 1.0
                      0x00050000, 0x00000003,   # version fichier 0.5.0.3
                      0x00050000, 0x00000003,   # version produit 0.5.0.3
                      0x0000003F, 0x00000000,   # masque drapeaux / drapeaux
                      0x00040004,      # VOS_NT_WINDOWS32
                      0x00000001,      # VFT_APP
                      0x00000000, 0x00000000, 0x00000000)
    chaines = b"".join([
        _chaine_vsi("FileDescription", "TRIADE superviseur terrain"),
        _chaine_vsi("FileVersion", "0.5.0.3"),
        _chaine_vsi("InternalName", "superviseur"),
        _chaine_vsi("OriginalFilename", "superviseur.exe"),
        _chaine_vsi("ProductName", "Protocole TRIADE"),
        _chaine_vsi("ProductVersion", "0.5.0-terrain.3"),
        _chaine_vsi("LegalCopyright", "Projet TRIADE - tests terrain"),
    ])
    table = _noeud_vsi(1, "040904B0", enfants=chaines)
    sfi = _noeud_vsi(1, "StringFileInfo", enfants=table)
    trad = _noeud_vsi(0, "Translation", struct.pack("<HH", 0x0409, 0x04B0), wlen=4)
    vfi = _noeud_vsi(1, "VarFileInfo", enfants=trad)
    versioninfo = _noeud_vsi(0, "VS_VERSION_INFO", valeur=ffi, enfants=sfi + vfi)

    manifeste = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        '<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">'
        '<assemblyIdentity type="win32" name="TRIADE.superviseur" version="0.5.0.3"/>'
        '<description>TRIADE : superviseur terrain de tests</description>'
        '<trustInfo xmlns="urn:schemas-microsoft-com:asm.v3"><security>'
        '<requestedPrivileges>'
        '<requestedExecutionLevel level="asInvoker" uiAccess="false"/>'
        '</requestedPrivileges></security></trustInfo>'
        '<compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">'
        '<application>'
        '<supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>'
        '</application></compatibility>'
        '<application xmlns="urn:schemas-microsoft-com:asm.v3"><windowsSettings>'
        '<dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true'
        '</dpiAware></windowsSettings></application>'
        '</assembly>\r\n'
    ).encode("utf-8")

    # arbre : racine (2 entrées) -> type -> nom -> langue -> donnée
    def dir_entrees(entrees: list[tuple[int, int]]) -> bytes:
        return (struct.pack("<IIHHHH", 0, 0, 4, 0, 0, len(entrees))
                + b"".join(struct.pack("<II", nom, off) for nom, off in entrees))

    off = 0
    racine_rva = L.RSRC_RVA
    o_racine = off; off += 16 + 2 * 8            # 32
    o_type_v = off; off += 16 + 8                # 24
    o_nom_v = off; off += 16 + 8                 # 24
    o_data_v = off; off += 16                    # 16
    o_type_m = off; off += 16 + 8
    o_nom_m = off; off += 16 + 8
    o_data_m = off; off += 16
    o_version = off; off += len(versioninfo)
    o_manifeste = off
    rsrc = bytearray(b"\x00" * (o_manifeste + len(manifeste)))
    # NB (format PE) : les décalages D'ANNUAIRE sont RELATIFS au début de la
    # section .rsrc ; seul l'OffsetToData de l'entrée de DONNÉE est un RVA
    # absolu — le premier jet confondait les deux (attrapé par pefile).
    rsrc[o_racine:o_racine + 32] = dir_entrees([
        (16, o_type_v | 0x80000000),
        (24, o_type_m | 0x80000000)])
    rsrc[o_type_v:o_type_v + 24] = dir_entrees([(1, o_nom_v | 0x80000000)])
    rsrc[o_nom_v:o_nom_v + 24] = dir_entrees([(0x409, o_data_v)])
    rsrc[o_data_v:o_data_v + 16] = struct.pack("<IIII", racine_rva + o_version,
                                               len(versioninfo), 0, 0)
    rsrc[o_type_m:o_type_m + 24] = dir_entrees([(1, o_nom_m | 0x80000000)])
    rsrc[o_nom_m:o_nom_m + 24] = dir_entrees([(0x409, o_data_m)])
    rsrc[o_data_m:o_data_m + 16] = struct.pack("<IIII", racine_rva + o_manifeste,
                                               len(manifeste), 0, 0)
    rsrc[o_version:o_version + len(versioninfo)] = versioninfo
    rsrc[o_manifeste:o_manifeste + len(manifeste)] = manifeste
    if len(rsrc) > L.RSRC_VSIZE:
        raise EchecBuild(f"section .rsrc débordante ({len(rsrc):#x} > {L.RSRC_VSIZE:#x})")
    return bytes(rsrc) + b"\x00" * (L.RSRC_VSIZE - len(rsrc)), len(rsrc)



RSRC_RAW = 0x800      # tailles brutes alignées FILE_ALIGN (D49)
BLOB_RAW = 0x8E00


def ecrire_pe32plus(texte, rdata, data, text2, rsrc, blob) -> bytes:
    dos = b"MZ" + b"\x00" * 58 + struct.pack("<I", 0x40)
    coff = struct.pack("<HHIIIHH", 0x8664, 6, 0, 0, 0, 0xF0, 0x0002)
    opt_fixe = struct.pack(
        "<HBBIIIIIQIIHHHHHHIIIIHHQQQQII",
        0x20B, 0, 0,
        L.ENTREE, len(texte) + len(text2), 0,
        L.ENTREE, L.TEXT_RVA,
        L.IMAGE_BASE,
        L.SECT_ALIGN, L.FILE_ALIGN,
        6, 0, 0, 1, 6, 0, 0,
        L.SIZE_OF_IMAGE, L.SIZE_HEADERS, 0,   # D50 : la vraie taille d'en-têtes
                                               # (0x400) — PLUS L.FILE_ALIGN, qui
                                               # ne coïncidait avec la bonne valeur
                                               # que pour quatre sections ou moins
        L.SUBSYSTEM_GUI,                     # WINDOWS_GUI — le superviseur est graphique
        L.DLL_CHARACTERISTICS,
        0x100000, 0x1000, 0x100000, 0x1000,
        0, 16,
    )
    dirs = [(0, 0)] * 16
    dirs[1] = (L.R_DESC_IMPORT, 140)        # 7 descripteurs (6 dll + terminateur)
    dirs[2] = (L.RSRC_RVA, RSRC_RAW)        # ressources : VERSIONINFO + manifeste
    dirs[5] = (L.R_RELOC, 12)
    dirs[12] = (L.R_IAT, 96)                # IAT kernel32#1 (11 slots + terme)
    opt = bytes(opt_fixe) + b"".join(struct.pack("<II", *d) for d in dirs)

    def sh(nom, vsize, vaddr, rawsz, rawptr, cara):
        return struct.pack("<8sIIIIIIHHI", nom, vsize, vaddr, rawsz, rawptr, 0, 0, 0, 0, cara)

    sections = (
        sh(b".text\x00\x00\x00", L.TEXT_VSIZE, L.TEXT_RVA, L.TEXT_VSIZE, L.TEXT_FILE, 0x60000020)
        + sh(b".rdata\x00\x00", L.RDATA_VSIZE, L.RDATA_RVA, L.RDATA_VSIZE, L.RDATA_FILE, 0x40000040)
        + sh(b".data\x00\x00\x00", L.DATA_VSIZE, L.DATA_RVA, L.DATA_RAW, L.DATA_FILE, 0xC0000040)
        + sh(b".text2\x00\x00", L.TEXT2_VSIZE, L.TEXT2_RVA, L.TEXT2_VSIZE, L.TEXT2_FILE, 0x60000020)
        + sh(b".rsrc\x00\x00\x00", L.RSRC_VSIZE, L.RSRC_RVA, RSRC_RAW, L.RSRC_FILE, 0x40000040)
        + sh(b".blob\x00\x00\x00", L.BLOB_VSIZE, L.BLOB_RVA, BLOB_RAW, L.BLOB_FILE, 0x40000040)
    )
    entetes = dos + b"PE\x00\x00" + coff + opt + sections
    assert len(entetes) == 64 + 4 + 20 + 240 + 240, len(entetes)
    assert len(entetes) <= L.TEXT_FILE, "en-têtes 6 sections débordent sur .text"
    exe = bytearray(b"\x00" * L.TAILLE_FICHIER)
    exe[0:len(entetes)] = entetes
    exe[L.TEXT_FILE:L.TEXT_FILE + len(texte)] = texte
    exe[L.RDATA_FILE:L.RDATA_FILE + len(rdata)] = rdata
    exe[L.DATA_FILE:L.DATA_FILE + len(data)] = data
    exe[L.TEXT2_FILE:L.TEXT2_FILE + len(text2)] = text2
    exe[L.RSRC_FILE:L.RSRC_FILE + len(rsrc)] = rsrc
    exe[L.BLOB_FILE:L.BLOB_FILE + len(blob)] = blob
    return bytes(exe)


def valider_pe(exe: bytes, jetons: bytes | None = None):
    pe = pefile.PE(data=exe)
    assert pe.FILE_HEADER.Machine == 0x8664
    assert pe.FILE_HEADER.NumberOfSections == 6
    assert pe.OPTIONAL_HEADER.Magic == 0x20B
    assert pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE, "entrée != sup-01"
    assert pe.OPTIONAL_HEADER.Subsystem == L.SUBSYSTEM_GUI, "sous-système != WINDOWS_GUI"
    assert pe.OPTIONAL_HEADER.SizeOfImage == L.SIZE_OF_IMAGE
    noms = [s.Name.decode().rstrip("\x00") for s in pe.sections]
    assert noms == [".text", ".rdata", ".data", ".text2", ".rsrc", ".blob"], noms
    # ressources (D49) : VERSIONINFO lisible par l'OS, manifeste asInvoker
    assert pe.OPTIONAL_HEADER.DATA_DIRECTORY[2].VirtualAddress == L.RSRC_RVA
    fic = None
    for bloc_info in pe.FileInfo:
        for d in bloc_info:
            if getattr(d, "Key", b"") == b"StringFileInfo":
                for table in d.StringTable:
                    for k, v in table.entries.items():
                        if k == b"FileVersion":
                            fic = v.decode("ascii")
    assert fic == "0.5.0.3", f"FileVersion ressources = {fic!r}"
    # D50 : règle du chargeur RÉEL — la table des sections doit tenir DANS
    # SizeOfHeaders (aligné FILE_ALIGN). Le terrain.2 violait cette règle
    # (0x238 d'en-têtes réels pour 0x200 déclarés) : Windows refusait de
    # lancer l'exécutable — pefile et l'oracle, plus tolérants, restaient
    # verts (défaut de classe « oracle aveugle au chargeur »).
    fin_reelle = (pe.DOS_HEADER.e_lfanew + 4 + 20
                  + pe.FILE_HEADER.SizeOfOptionalHeader
                  + pe.FILE_HEADER.NumberOfSections * 40)
    soh = pe.OPTIONAL_HEADER.SizeOfHeaders
    assert soh == L.SIZE_HEADERS, f"SizeOfHeaders {soh:#x} != plan {L.SIZE_HEADERS:#x}"
    assert soh >= fin_reelle, (f"table des sections ({fin_reelle:#x}) hors "
                               f"SizeOfHeaders ({soh:#x}) — chargeur KO")
    assert soh % pe.OPTIONAL_HEADER.FileAlignment == 0, "SizeOfHeaders non aligné"
    for s in pe.sections:
        assert s.PointerToRawData >= soh, (f"{s.Name.decode().rstrip(chr(0))} : "
                                           f"brute à {s.PointerToRawData:#x} < en-têtes")
    # kit embarqué (D49) : les octets .blob SONT les artefacts scellés
    with open(os.path.join(DEMO_DIR, "demo.exe"), "rb") as f:
        demo = f.read()
    with open(os.path.join(M3_DIR, "proxy.exe"), "rb") as f:
        proxy = f.read()
    assert exe[L.BLOB_FILE + 0x10: L.BLOB_FILE + 0x10 + L.LONGUEUR_DEMO] == demo
    assert exe[L.BLOB_FILE + 0x10 + L.LONGUEUR_DEMO:
               L.BLOB_FILE + 0x10 + L.LONGUEUR_DEMO + L.LONGUEUR_PROXY] == proxy
    attendu_slot = jetons if jetons is not None else b"\x00" * L.LONGUEUR_ANNEXE
    off_slot = L.BLOB_FILE + (L.SLOT_JETONS - L.BLOB_RVA)
    longueur_attendue = len(jetons) if jetons is not None else 0
    assert struct.unpack_from("<Q", exe, off_slot)[0] == longueur_attendue
    assert exe[off_slot + 8: off_slot + 8 + L.LONGUEUR_ANNEXE] == attendu_slot
    imports = {}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        dll = entree.dll.decode().lower()
        imports.setdefault(dll, []).extend(i.name.decode() for i in entree.imports)
    imports = {dll: sorted(noms) for dll, noms in imports.items()}
    attendu = {"kernel32.dll": sorted(L.KERNEL32_IMPORTS + L.KERNEL32B_IMPORTS
                                      + L.KERNEL32C_IMPORTS),
               "user32.dll": sorted(L.USER32_IMPORTS + L.USER32B_IMPORTS),
               "gdi32.dll": sorted(L.GDI32_IMPORTS)}
    assert imports == attendu, {k: set(v) ^ set(attendu.get(k, [])) for k, v in imports.items()}
    # D35 : verrou chargeur réel — FT = slots appelés par la notation
    ft_attendus = {"kernel32.dll": {L.R_IAT, L.R_IAT_K32B, L.R_IAT_K32C},
                   "user32.dll": {L.R_IAT_USER32, L.R_IAT_U32B},
                   "gdi32.dll": {L.R_IAT_GDI32}}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        dll = entree.dll.decode().lower()
        assert entree.struct.FirstThunk in ft_attendus[dll], \
            f"FirstThunk {dll} != {ft_attendus[dll]} (D35)"
    assert len(exe) == L.TAILLE_FICHIER
    return True


def preuve_reutilisation(exe: bytes) -> dict:
    """R7 : les blocs hérités sont octet-identiques aux artefacts scellés."""
    LD = sys.modules["layout_demo"]        # plan démo (convention fichier M2)
    artefacts = {}
    for nom, chemin in (("hello.exe", os.path.join(M0_DIR, "hello.exe")),
                        ("selftest.exe", os.path.join(M1_DIR, "selftest.exe")),
                        ("echo.exe", os.path.join(M2_DIR, "echo.exe")),
                        ("demo.exe", os.path.join(DEMO_DIR, "demo.exe"))):
        with open(chemin, "rb") as f:
            artefacts[nom] = f.read()

    def tranche_artefact(buf, rva, slot):
        """Offsets fichier du PLAN DÉMO (hello/selftest/echo/demo partagent la
        convention M2 : première section brute à 0x200 — terrain.2 NON : six
        sections, en-têtes 568 o, première brute à 0x400, d'où les DEUX
        fonctions de tranche, D49)."""
        if rva >= L.TEXT2_RVA:
            return buf[LD.TEXT2_FILE + (rva - L.TEXT2_RVA):][:slot]
        return buf[LD.TEXT_FILE + (rva - L.TEXT_RVA):][:slot]

    def tranche_terrain(buf, rva, slot):
        if rva >= L.TEXT2_RVA:
            return buf[L.TEXT2_FILE + (rva - L.TEXT2_RVA):][:slot]
        return buf[L.TEXT_FILE + (rva - L.TEXT_RVA):][:slot]

    sources = {"a1000": "hello.exe", "b2000": "selftest.exe",
               "c3000": "echo.exe", "d4000": "demo.exe"}
    heritage = []
    for bid, _, _, rva, slot in blocs_terrain():
        if bid not in _HERITAGE:
            continue
        source = artefacts[sources[bid[:4] + "0"]]
        if tranche_artefact(source, rva, slot) != tranche_terrain(exe, rva, slot):
            raise EchecBuild(f"réutilisation rompue : {bid} diffère de l'artefact "
                             f"scellé {sources[bid[:4] + '0']} (R7)")
        heritage.append(bid)
    return {"blocs_reutilises": heritage}


# --- Carte lignée terrain (génération 5) -------------------------------------------

CONTRATS = {
    **{k: v for k, v in bm.CONTRATS.items() if k in _HERITAGE},
    **{k: v for k, v in bd.CONTRATS.items() if k in _HERITAGE},
    "f60001": ("() -> noreturn", "chargeur ; pile alignée",
               "horodatage AVANT fenêtre ; boucle drainée ; io-02(0|1)",
               "appels sup-21/sup-02/win-03/io-02 uniquement ; aucun IAT",
               "[f60021] [f60002] [d40003] [a10003]"),
    "f60002": ("() -> ptr|0", "TAMPON_NOM posé (P1 sup-01) ; IAT résolue",
               "rax = hwnd ; HWND_PRINCIPAL posé ; échec -> LKO_GUI + MessageBoxW + 0",
               "classe TRIADE_superviseur (anti-collision démo) ; wndproc scellé 0x1640",
               "[ext user32:RegisterClassExW,CreateWindowExW,LoadCursorW,MessageBoxW] "
               "[ext kernel32:GetModuleHandleW,GetLastError] [d40005] [rdata:UTF-16,ASCII]"),
    "f60021": ("() -> u64", "pile alignée",
               "TAMPON_NOM = terrain_YYYYMMDD_HHMMSS.txt ; TAMPON_AFF = S01 date … ; rax = 24",
               "chiffres par division inline ; une seule lecture d'heure",
               "[ext kernel32#3:GetLocalTime] [b20001] [donnees .data:TAMPON_NOM,TAMPON_AFF]"),
    "f60022": ("(buf, len, étiquette, étiquette_len, arrêt, dest, cap) -> u64",
               "7 args ; pile alignée",
               "rax = octets copiés (NUL posé) ; 0 = absent/vide/tronqué (défaillance visible)",
               "bornes I1 strictes ; memcmp/memcpy scellées ; pur, réentrant",
               "[b20002] [b20001]"),
    "f60011": ("(ptr, len, mode, valeur) -> u32", "TAMPON_NOM posé ; bornes win-11 P4",
               "contrat win-11:R1 intégral, nom dynamique du run ; BUF_CHEMIN reste valide",
               "I6 BUF_CHEMIN propriété unique (sup-35 le relit) ; jamais demo_journal.txt",
               "[b20001] [b20003] [b20004] "
               "[ext kernel32#2:GetModuleFileNameA,CreateFileA] [ext kernel32:WriteFile,"
               "FlushFileBuffers] [donnees .data:handle,tampons,TAMPON_NOM]"),
    "f60009": ("(arg u64) -> u32", "lancé une fois par win-04 ; TAMPON_* posés",
               "porte -> libc -> extraction kit -> T1 -> T2 -> T3 -> nettoyage -> S90/S91 ; "
               "rax = 1 ssi les verdicts COMPTÉS sont verts (T3 non applicable en "
               "variante publique n'est pas compté — D49)",
               "un KO n'arrête rien ; la porte précède tout test ; l'envoi vient en "
               "dernier ; le nettoyage suit T3 (l'annexe vit le temps de l'envoi)",
               "[d40006] [d40005] [f60037] [f60033] [f60034] [f60035] "
               "[donnees sup:S00..S03,S90,S91] [donnees .data:TAMPON_AFF]"),
    "f60031": ("(cmdline ptr, mode u32) -> u32", "pile alignée",
               "rax = 1 : HPROC/PID posés, hThread fermé, extrémités enfant fermées ; "
               "0 = échec (zéro fuite, quatre fermetures en mode 1)",
               "SA initialisé AVANT CreatePipe ; cwd forcé au répertoire de l'exe (D36) ; "
               "héritage demandé uniquement en mode 1",
               "[ext kernel32#3:CreateProcessA,CreatePipe] [ext kernel32:CloseHandle] "
               "[ext kernel32#2:GetModuleFileNameA] [donnees .data:ETAT_SUP]"),
    "f60033": ("() -> u32", "journal opérationnel ; pile alignée",
               "T1 : fenêtre (sondage borné), BM_CLICK, marqueur 31 o, 17 lignes "
               "exactes embarquées brutes ; S16 verdict",
               "attentes = événements bornés ; journal démo en lecture seule",
               "[f60031] [f60036] [d40005] [b20002] "
               "[ext kernel32#3:WaitForSingleObject,GetExitCodeProcess,TerminateProcess,"
               "Sleep] [ext user32#2:FindWindowW,FindWindowExW,SendMessageTimeoutW] "
               "[ext kernel32:CloseHandle] [donnees sup:S10..S16,NOM_DEMO] "
               "[rdata:CLASSE_DEMO,CLASSE_BOUTON]"),
    "f60034": ("() -> u32", "journal opérationnel ; pile alignée",
               "T2 : bannière/événements/arret memcmp exacts, curl http+https, "
               "pages comptées, flux embarqué ; 9 drapeaux -> S28",
               "aucun ReadFile sans PeekNamedPipe ; quit écrit avant l'attente ; "
               "nettoyage des pages et tuyaux sur tout chemin",
               "[f60031] [f60036] [d40005] [b20001] [b20002] "
               "[ext kernel32#3:WaitForSingleObject,GetExitCodeProcess,TerminateProcess,"
               "PeekNamedPipe,Sleep,DeleteFileA] [ext kernel32:CloseHandle,ReadFile,"
               "WriteFile] [donnees sup:S20..S28,fixtures,cmdlines] [rdata:NOM_PROXY,QUIT]"),
    "f60035": ("() -> u32", "BUF_CHEMIN valide (journal ouvert) ; pile alignée",
               "T3 : jetons lus, OAuth composé exact, jeton extrait, métadonnées, "
               "session, PUT --data-binary @journal ; S36 verdict",
               "les secrets ne passent jamais par le journal (I1) ; BUF_CHEMIN jamais "
               "recomposé (I2) ; 5 suppressions sur tout chemin",
               "[f60031] [f60022] [f60036] [d40005] [b20001] "
               "[ext kernel32#3:WaitForSingleObject,GetExitCodeProcess] "
               "[ext kernel32:CloseHandle] [donnees sup:S30..S36,étiquettes,gabarits,"
               "noms] [donnees .data:TAMPON_JETON,TAMPON_CMD]"),
    "f60036": ("(nom, op, len, contenu_len) -> u64", "BUF_CHEMIN valide ; pile alignée",
               "lire -> rax = LU (contenu à TAMPON_CMD+0) ; écrire -> 1/0 ; "
               "supprimer -> retour DeleteFileA ; op inconnue -> 0",
               "chemins TOUJOURS préfixés du répertoire de l'exe (DIR_LONG caché, "
               "un seul propriétaire) ; zéro fuite de handle",
               "[b20001] [b20003] [ext kernel32#2:CreateFileA] "
               "[ext kernel32:ReadFile,WriteFile,CloseHandle] "
               "[ext kernel32#3:DeleteFileA] [donnees .data:DIR_LONG,LU]"),
    "f60037": ("(mode u32 ecx) -> u32", "BUF_CHEMIN valide ; pile alignée ; mode 0/1",
               "mode 0 : bit0 demo.exe posé+relu conforme, bit1 proxy.exe idem, "
               "bit2 T3 applicable (variante livraison) ; mode 1 : trois fichiers "
               "retirés + S07",
               "écriture ET relecture en morceaux 512 o depuis/vers l'embarqué ; "
               "zéro fuite de handle ; longueurs lues à l'en-tête .blob (jamais en dur) ; "
               "l'emplacement annexe est hors table R10 (seul octet mutable, D49)",
               "[b20001] [b20002] [b20003] [f60036] [d40005] "
               "[ext kernel32#2:CreateFileA] [ext kernel32:ReadFile,WriteFile,CloseHandle] "
               "[donnees .blob:BLOB_LONGUEURS,BLOB_DEMO,BLOB_PROXY,SLOT_JETONS] "
               "[donnees sup:S04..S07,NOM_JETONS] [rdata:NOM_DEMO,NOM_PROXY]"),
}


def fragments_clairs(code, exe, verrous, blocs, version, verdict, compteurs, journal_runs):
    sha = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()
    loc = ["[carte-frag] nom=frag-loc generation=5",
           "[zones] io=0x1000-0x10ff libc=0x1100-0x12ff coquille=0x1400-0x1fff "
           "scenario=0x4c00 fichiers=0x4e00 miroir=0x5000 lanceur=0x5200 "
           "t1=0x5400 t2=0x5800 t3=0x5e00 kit=0x6600 "
           "donnees-sup=0x4340-0x4bff,0x6300-0x65ff,0x6a00-0x6dff blob=0x8000"]
    spec_map = {bid: sid for bid, sid, _, _, _ in blocs}
    for bid, _, _, rva, slot in blocs:
        loc.append(f"[bloc] id={bid} spec={spec_map[bid]} cible=x86-64-win11-pe "
                   f"exe=superviseur addr={L.IMAGE_BASE + rva:#x} size={slot} v=1 "
                   f"etat=scelle role={L.NOMS_BLOCS[bid]}")
    con = ["[carte-frag] nom=frag-con generation=5"]
    for bid, _, _, _, _ in blocs:
        sig, pre, post, inv, deps = CONTRATS[bid]
        con += [f"[bloc] id={bid}", f"  sig : {sig}", f"  pre : {pre}",
                f"  post : {post}", f"  inv : {inv}", f"  deps : {deps}"]
    prf = ["[carte-frag] nom=frag-prf generation=5"]
    for bid, _, fichier, _, _ in blocs:
        with open(chemin_notation(fichier), "rb") as f:
            empreinte = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} crist={crist}/10",
                f"  vecteurs : roundtrip=ok structure=ok notation={empreinte}",
                f"  differentiel : {verdict.get('blocs', {}).get(bid, {}).get('detail', '-')}"]
    prf.append("[verifications] runs=" + str(len(journal_runs)))
    prf += ["  " + r for r in journal_runs[-12:]]
    bld = ["[carte-frag] nom=frag-bld generation=5"]
    for bid, _, _, rva, slot in blocs:
        base_rva, base_file = (L.TEXT2_RVA, L.TEXT2_FILE) if rva >= L.TEXT2_RVA \
            else (L.TEXT_RVA, L.TEXT_FILE)
        tranche = exe[base_file + (rva - base_rva): base_file + (rva - base_rva) + slot]
        bld.append(f"[bloc] id={bid} addr={L.IMAGE_BASE + rva:#x} empreinte={sha(tranche)}")
    for nom_zone, zone in (("donnees-sup-1", L.ZONE_DATA_SUP), ("donnees-sup-2", L.ZONE_DATA_SUP_2),
                           ("donnees-sup-3", L.ZONE_DATA_SUP_3)):
        debut, fin = zone
        tranche = exe[L.TEXT2_FILE + (debut - L.TEXT2_RVA):
                      L.TEXT2_FILE + (fin - L.TEXT2_RVA) + 1]
        bld.append(f"[zone] id={nom_zone} addr={L.IMAGE_BASE + debut:#x} "
                   f"empreinte={sha(tranche)}")
    debut, fin = L.ZONE_BLOB_INTEG
    tranche = exe[L.BLOB_FILE + (debut - L.BLOB_RVA): L.BLOB_FILE + (fin - L.BLOB_RVA) + 1]
    bld.append(f"[zone] id=blob-integrite addr={L.IMAGE_BASE + debut:#x} "
               f"empreinte={sha(tranche)}")
    bld += [
        f"[build] artefact=superviseur.exe version={version} profil=x86-64-win11-pe "
        f"taille={len(exe)} empreinte={sha(exe)}",
        f"  outils : keystone + capstone {capstone.cs_version()[0]}.{capstone.cs_version()[1]} ; "
        f"verrous={len(verrous)} ; oracle : {verdict.get('total_cas', 0)} cas, "
        f"graine={verdict.get('graine', '-')}",
        f"  heritage : hello.exe + selftest.exe + echo.exe + demo.exe 0.3.0-demo.9 "
        f"(io/libc/tcp-06 + coquille win réutilisés octet-identiques, R7)",
        f"  kit embarqué : demo.exe 0.3.0 + proxy.exe 0.4.0-dev.1 en .blob "
        f"(md5 assertés au build, table R10 zone blob — emplacement annexe exclu, D49)",
        f"[zones] coquille=0x1400-0x1fff scenario=0x4c00 t1=0x5400 t2=0x5800 t3=0x5e00 "
        f"kit=0x6600 donnees-sup=0x4340-0x4bff,0x6300-0x65ff,0x6a00-0x6dff blob=0x8000",
    ]
    retour = {}
    for nom, lignes in (("frag-loc", loc), ("frag-con", con), ("frag-prf", prf), ("frag-bld", bld)):
        retour[nom] = ("\n".join(lignes) + "\n").encode("utf-8")
    return retour


def construire_carte(code, exe, verrous, blocs, version, verdict, compteurs, journal_runs):
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    clairs = fragments_clairs(code, exe, verrous, blocs, version, verdict,
                              compteurs, journal_runs)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = cm.empreinte_racine(fragments)
    entete = cm.construire_entete(racine)
    prive, pub = cm.paire_cles(graine)
    signature = cm.signer(prive, entete, fragments)
    cm.ecrire_carte(entete, fragments, signature, pub)
    return pub


def verrou_croise(blocs):
    phrase, _ = cm.charger_secrets(interactif=False)
    entete, fragments, signature, pub = cm.lire_carte()
    cm.verifier_listes_blanches(entete.decode("ascii"))
    cm.verifier_signature(pub, entete, fragments, signature)
    if cm.empreinte_racine(fragments).hex() not in entete.decode("ascii"):
        raise cm.ErreurCarte("empreinte racine divergente")
    maitre = cm.cle_maitresse(phrase)
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
    with open(os.path.join(ICI, "superviseur.exe"), "rb") as f:
        exe = f.read()
    empreintes, manifestes = {}, []
    for ligne in bld.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[champs["id"]] = champs["empreinte"]
        elif ligne.startswith("[build]"):
            manifestes.append(dict(re.findall(r"(\w+)=(\S+)", ligne)))
    manifeste = next((m for m in manifestes if m.get("artefact") == "superviseur.exe"), {})
    for bid, _, _, rva, slot in blocs:
        base_rva, base_file = (L.TEXT2_RVA, L.TEXT2_FILE) if rva >= L.TEXT2_RVA \
            else (L.TEXT_RVA, L.TEXT_FILE)
        tranche = exe[base_file + (rva - base_rva): base_file + (rva - base_rva) + slot]
        if "sha256:" + hashlib.sha256(tranche).hexdigest() != empreintes.get(bid):
            raise cm.ErreurCarte(f"verrou croisé : empreinte de {bid} divergente (R8)")
    if "sha256:" + hashlib.sha256(exe).hexdigest() != manifeste.get("empreinte"):
        raise cm.ErreurCarte("verrou croisé : empreinte de superviseur.exe divergente (R8)")
    return len(empreintes), manifeste


def tableau_de_bord(exe, verrous, nb, manifeste, verdict) -> str:
    herit = len(_HERITAGE)
    lignes = [
        "[tableau] jalon=terrain artefact=superviseur.exe version=" + manifeste.get("version", "?"),
        f"  blocs_avec_spec_a_jour        : {nb}/{nb} : tracabilite I->C->B "
        f"(heritage M0/M1/M2/demo + {nb - herit} blocs sup)",
        f"  chaines_I_C_B_tests           : {nb}/{nb}",
        f"  construction                  : 0 erreur / 0 avertissement",
        f"  tests_oracle                  : {verdict.get('total_cas', 0)} cas verts "
        f"(graine {verdict.get('graine', '-')}) ; oracle structurel {len(verrous)} verrous PASS ; "
        f"falsification : {verdict.get('falsification', '-')}",
        f"  empreintes_donnees_embarquees : conforme (table R10 27 entrees + terminateur dont "
        f"4 zones de donnees sup + zone blob, UTF-16 contraint, fixtures)",
        f"  defauts_attrapes_avant_build  : 6 classes (constante terrain_, mode .curl, "
        f"flux banniere 39->38, mapping .champ decale, 7 traces valeur en mode 0, "
        f"SA consomme avant initialisation) — le systeme a fonctionne comme concu",
        f"  reutilisation_R7              : {herit} blocs octet-identiques "
        f"(hello/selftest/echo/demo.9)",
        f"  preversions                   : {manifeste.get('version', '?')} (lignee terrain, "
        f"u64 0x{L.VERSION_U64_TERRAIN3:x}, plancher 0x{L.VERSION_U64_MIN:x})",
        f"  exigence_developpeur          : 1 SEUL EXE qui contient tout (D49) — kit "
        f"embarque .blob (demo.exe 0.3.0 + proxy.exe 0.4.0-dev.1 + annexe jetons), "
        f"extraction verifiee par relecture octet a octet, nettoyage apres run ; "
        f"variante publique (depot, slot vide) / livraison (--jetons, annexe D48)",
        f"  artefact                      : {len(exe)} octets ; "
        f"subsystem WINDOWS_GUI ; entree 0x{L.ENTREE:x}",
        f"  verrou_croise                 : {nb} empreintes reverifiees + signature "
        f"Ed25519 (R8/R9)",
    ]
    return "\n".join(lignes) + "\n"


# --- Assemblage + vérification ------------------------------------------------------

def assembler_tout():
    blocs = blocs_terrain()
    specs = charger_couche_I(blocs)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code = {}
    for bid, sid, fichier, rva, slot in blocs:
        chemin = chemin_notation(fichier)
        octets, metas = bm.assembler_bloc(ks, chemin, rva, slot)
        insns = bm.round_trip(cs, ks, chemin, rva, octets, metas)
        code[bid] = {"octets": octets, "insns": insns,
                     "slot": octets + b"\x90" * (slot - len(octets))}
        print(f"[R5] {bid} ({sid}) : {len(octets)} o, round-trip {len(insns)}/{len(insns)} = 100 %")
    verrous = oracle_structurel(specs, code, blocs)
    print(f"[oracle] structurel : {len(verrous)} verrous PASS (contrats I verifies par bloc)")
    return blocs, specs, code, verrous


def construire(graine: int, avec_jetons: bool = False) -> int:
    print("=== terrain : chaîne artefact TRIADE (profil x86-64-win11-pe, WINDOWS_GUI) ===")
    blocs, specs, code, verrous = assembler_tout()
    version = L.VERSION_TERRAIN3
    blob_public = composer_blob(None)
    rsrc, taille_rsrc = composer_rsrc()
    texte, rdata, data, text2 = composer_sections(code, blocs, blob_public)
    exe = ecrire_pe32plus(texte, rdata, data, text2, rsrc, blob_public)
    valider_pe(exe)
    heritage = preuve_reutilisation(exe)
    print(f"[PE] superviseur.exe : {len(exe)} octets, 6 sections (.rsrc {taille_rsrc} o, "
          f".blob {L.BLOB_VSIZE:#x} — kit embarqué), kernel32 x24 (3 IAT) + "
          f"user32 x17 (2 IAT) + gdi32 x1, WINDOWS_GUI, entree 0x{L.ENTREE:x}, FT=slots (D35)")
    print(f"[R7] réutilisation : {len(heritage['blocs_reutilises'])} blocs octet-identiques "
          f"aux artefacts scellés M0/M1/M2/démo (demo.exe 0.3.0-demo.9)")

    verdict = od.executer(exe, graine=graine)
    print(f"[oracle] {verdict['total_cas']} cas verts ; "
          f"falsification : {verdict['falsification']}")

    with open(os.path.join(ICI, "superviseur.exe"), "wb") as f:
        f.write(exe)
    compteurs = {bid: 1 for bid, _, _, _, _ in blocs}
    journal = [f"run graine={graine} verdict={verdict['empreinte']} "
               f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} build={version}"]
    construire_carte(code, exe, verrous, blocs, version, verdict, compteurs, journal)
    nb, manifeste = verrou_croise(blocs)
    print(f"[carte] lignée terrain (génération 5) écrite : 4 fragments, signature Ed25519, "
          f"{nb} empreintes indexées")
    print(f"[R8] verrou croisé : signature OK, racine OK, artefact {manifeste.get('version')}")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="utf-8") as f:
        f.write(tableau_de_bord(exe, verrous, nb, manifeste, verdict))
    print(f"[B] superviseur.exe (publique) scellé : sha256:{hashlib.sha256(exe).hexdigest()}")

    if avec_jetons:
        chemin_jetons = os.path.join(os.path.dirname(ICI),
                                     ".gdrive", "terrain_jetons.bin")
        with open(chemin_jetons, "rb") as f:
            jetons = f.read()
        blob_livraison = composer_blob(jetons)
        exe_livraison = ecrire_pe32plus(texte, rdata, data, text2, rsrc, blob_livraison)
        valider_pe(exe_livraison, jetons)
        off_slot = L.BLOB_FILE + (L.SLOT_JETONS - L.BLOB_RVA)
        ecarts = [i for i, (a, b) in enumerate(zip(exe, exe_livraison)) if a != b]
        if not ecarts or min(ecarts) < off_slot or max(ecarts) >= off_slot + L.TAILLE_SLOT_JETONS:
            raise EchecBuild("variante livraison : écart hors emplacement annexe (D49)")
        dossier = os.path.join(ICI, "livraison")
        os.makedirs(dossier, exist_ok=True)
        with open(os.path.join(dossier, "superviseur.exe"), "wb") as f:
            f.write(exe_livraison)
        print(f"[B] superviseur.exe (livraison, annexe intégrée) : "
              f"sha256:{hashlib.sha256(exe_livraison).hexdigest()} ; "
              f"écart public/livraison confiné au slot ({len(ecarts)} octets) ; "
              f"livraison/superviseur.exe — JAMAIS commité (interdit 11)")
    print(f"=== terrain {version} (oracle vert) — validation terrain Windows 11 en attente ===")
    return 0


def verifier(graine: int) -> int:
    print(f"=== terrain : re-vérification complète (R5/R8, graine {graine}) ===")
    blocs, specs, code, verrous = assembler_tout()
    with open(os.path.join(ICI, "superviseur.exe"), "rb") as f:
        exe = f.read()
    for bid, _, _, rva, slot in blocs:
        base_rva, base_file = (L.TEXT2_RVA, L.TEXT2_FILE) if rva >= L.TEXT2_RVA \
            else (L.TEXT_RVA, L.TEXT_FILE)
        if exe[base_file + (rva - base_rva): base_file + (rva - base_rva) + slot] != code[bid]["slot"]:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5)")
    verdict = od.executer(exe, graine=graine)
    print(f"[oracle] {verdict['total_cas']} cas verts")
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("utf-8")
    compteurs, journal = {}, []
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            m = re.match(r"(\d+)/10", champs.get("crist", "1/10"))
            compteurs[champs["id"]] = int(m.group(1))
        elif ligne.startswith("  run "):
            journal.append(ligne.strip())
    for bid, _, _, _, _ in blocs:
        compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal.append(f"run graine={graine} verdict={verdict['empreinte']} "
                   f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
    version = next((dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
                    if "artefact=superviseur.exe" in l), L.VERSION_TERRAIN3)
    construire_carte(code, exe, verrous, blocs, version, verdict, compteurs, journal)
    nb, manifeste = verrou_croise(blocs)
    print(f"[R6] cristallisation enclenchée ; [R8] {nb} empreintes conformes ; "
          f"artefact {manifeste.get('version')}")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="utf-8") as f:
        f.write(tableau_de_bord(exe, verrous, nb, manifeste, verdict))
    return 0


if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 1
        if "--verifier" in args:
            sys.exit(verifier(graine))
        sys.exit(construire(graine, avec_jetons="--jetons" in args))
    except (EchecBuild, cm.ErreurCarte, od.EchecOracle) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
