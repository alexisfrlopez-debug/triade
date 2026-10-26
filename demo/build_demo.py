#!/usr/bin/env python3
"""build_demo.py — Jalon démo TRIADE : démonstration graphique complète en un clic.

demo.exe (PE32+ WINDOWS_GUI écrit à la main) embarque les blocs scellés
M0/M1/M2 octet-identiques (io, libc, tcp-01..09, tcp-11, staging echo v2)
plus dix blocs nouveaux win-01..win-10 : fenêtre, journal graphique, autotest
porte R10 + libc, client TCP, serveur d'acceptation, échange vérifié et
scénario complet — la boucle § 5 (patch à chaud EN PRODUCTION, rollback)
pilotée par UN clic, avec vérification memcmp octet par octet à chaque étape.

La chaîne réutilise build_m2.py (assemblage, round-trip, canon, lecture de
gabarit, sommes) — la démo est une EXTENSION de la lignée M2, pas sa copie :
sub-système WINDOWS_GUI, imports user32/gdi32, IAT ws2 étendue (connect) et
kernel32 étendue (GetModuleHandleW), le correctif D35 (FirstThunk = slots
appelés) intégré dès la première génération.

Usage :
  python3 build_demo.py                 # construction dev.1 + oracle + carte
  python3 build_demo.py --verifier [--graine N]   # R5/R8 : re-vérification
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
M2_DIR = os.path.join(os.path.dirname(ICI), "m2")
sys.path.insert(0, M2_DIR)
sys.path.insert(0, ICI)

# Deux plans d'adressage cohabitent : m2/layout.py (héritage, requis par
# build_m2.py) et demo/layout.py (le plan démo). Isolation par noms distincts
# — le module "layout" de sys.modules reste celui de M2 pour build_m2.
import importlib.util as _ilu
_spec_m2 = _ilu.spec_from_file_location("layout", os.path.join(M2_DIR, "layout.py"))
sys.modules["layout"] = _ilu.module_from_spec(_spec_m2)
_spec_m2.loader.exec_module(sys.modules["layout"])
import build_m2 as bm                    # chaîne scellée M2 (réutilisation)
_spec_demo = _ilu.spec_from_file_location("layout_demo", os.path.join(ICI, "layout.py"))
L = _ilu.module_from_spec(_spec_demo)
_spec_demo.loader.exec_module(L)
sys.modules["layout_demo"] = L

import carte_demo as cm
import oracle_demo as od

import capstone
import pefile
from keystone import Ks, KS_ARCH_X86, KS_MODE_64

M0_DIR = bm.M0_DIR
M1_DIR = bm.M1_DIR


class EchecBuild(Exception):
    pass


# --- Blocs embarqués dans demo.exe ----------------------------------------------

def blocs_demo() -> list[tuple]:
    """(id carte, spec, fichier notation, rva, slot) — héritage + génération démo."""
    return [
        # héritage M0/M1 (octets identiques aux artefacts scellés)
        ("a10002", "hello-02:R1", "hello-02-write", 0x1040, 0x40),
        ("a10003", "hello-03:R1", "hello-03-exit", 0x1080, 0x40),
        ("b20001", "libc-01:R1", "libc-01-memcpy", 0x1100, 0x80),
        ("b20002", "libc-02:R1", "libc-02-memcmp", 0x1180, 0x80),
        ("b20003", "libc-03:R1", "libc-03-strlen", 0x1200, 0x80),
        ("b20004", "libc-04:R1", "libc-04-itoa", 0x1280, 0x80),
        # héritage M2 (octets identiques à echo.exe 0.3.0-rc.2) — tcp-10/tcp-12
        # NON embarqués (console et point d'entrée console remplacés par win-*)
        ("c30001", "tcp-01:R1", "tcp-01-init", 0x4000, 0x100),
        ("c30002", "tcp-02:R1", "tcp-02-accept", 0x4100, 0x40),
        ("c30003", "tcp-03:R1", "tcp-03-recv", 0x4140, 0x40),
        ("c30004", "tcp-04:R1", "tcp-04-send", 0x4180, 0x40),
        ("c30005", "tcp-05:R1", "tcp-05-close", 0x41C0, 0x40),
        ("c30006", "tcp-06:R1", "tcp-06-spawn", 0x4300, 0x40),
        ("c30007", "tcp-07:R1", "tcp-07-patch", 0x4400, 0x200),
        ("c30008", "tcp-08:R1", "tcp-08-echo", 0x4600, 0x40),
        ("c30009", "tcp-09:R1", "tcp-09-conn", 0x4800, 0x180),
        ("c30011", "tcp-11:R1", "tcp-11-journal", 0x4B00, 0x100),
        # génération démo
        ("d40001", "win-01:R1", "win-01-principal", 0x1400, 0x40),
        ("d40002", "win-02:R1", "win-02-fenetre", 0x1440, 0x140),
        ("d40003", "win-03:R1", "win-03-boucle", 0x1580, 0x80),
        ("d40004", "win-04:R1", "win-04-procedure", 0x1600, 0x2C0),
        ("d40005", "win-05:R1", "win-05-journal", 0x18C0, 0x80),
        ("d40006", "win-06:R1", "win-06-autotest", 0x1940, 0x180),
        ("d40007", "win-07:R1", "win-07-client", 0x1AC0, 0xC0),
        ("d40008", "win-08:R1", "win-08-serveur", 0x1B80, 0x100),
        ("d40009", "win-09:R1", "win-09-scenario", 0x1C80, 0x380),
        ("d40010", "win-10:R1", "win-10-echange", 0x4980, 0x180),
    ]


BLOC_STAGING = ("c30014", "tcp-08:R2", "tcp-08-echo-v2",
                L.ECHO_CROISSANCE, 0x80)                    # .rdata, activation à chaud

FICHIERS_I_DEMO = {
    "win-01": "win-01-principal.md", "win-02": "win-02-fenetre.md",
    "win-03": "win-03-boucle.md", "win-04": "win-04-procedure.md",
    "win-05": "win-05-journal.md", "win-06": "win-06-autotest.md",
    "win-07": "win-07-client.md", "win-08": "win-08-serveur.md",
    "win-09": "win-09-scenario.md", "win-10": "win-10-echange.md",
}


def chemin_notation(fichier: str) -> str:
    if fichier.startswith("hello-"):
        return os.path.join(M0_DIR, "notation", fichier + ".asm")
    if fichier.startswith("libc-0") and fichier != "libc-09-zone-alloc-ts":
        return os.path.join(M1_DIR, "notation", fichier + ".asm")
    if fichier.startswith("tcp-"):
        return os.path.join(M2_DIR, "notation", fichier + ".asm")
    return os.path.join(ICI, "notation", fichier + ".asm")


def charger_couche_I(blocs: list[tuple]) -> dict[str, dict]:
    """Specs démo depuis demo/I/, héritage depuis m0/I, m1/I, m2/I (D24)."""
    specs = {}
    fichiers = {
        **{ident: ident + "-write.md" for ident in ("hello-02",)},
        **{ident: ident + "-exit.md" for ident in ("hello-03",)},
        **{ident: ident + "-memcpy.md" for ident in ("libc-01",)},
        **{ident: ident + "-memcmp.md" for ident in ("libc-02",)},
        **{ident: ident + "-strlen.md" for ident in ("libc-03",)},
        **{ident: ident + "-itoa.md" for ident in ("libc-04",)},
        **{ident: FICHIERS_I_DEMO[ident] for ident in FICHIERS_I_DEMO},
    }
    fichiers_m2 = {
        "tcp-01": "tcp-01-init.md", "tcp-02": "tcp-02-accept.md",
        "tcp-03": "tcp-03-recv.md", "tcp-04": "tcp-04-send.md",
        "tcp-05": "tcp-05-close.md", "tcp-06": "tcp-06-spawn.md",
        "tcp-07": "tcp-07-patch.md", "tcp-08": "tcp-08-echo.md",
        "tcp-09": "tcp-09-conn.md", "tcp-11": "tcp-11-journal.md",
    }

    def charger(bid: str, sid: str):
        ident, rev_ref = sid.split(":")
        rev_ref = int(rev_ref[1:])
        if ident in FICHIERS_I_DEMO:
            chemin = os.path.join(ICI, "I", FICHIERS_I_DEMO[ident])
        elif ident.startswith("hello-"):
            chemin = os.path.join(M0_DIR, "I", fichiers[ident])
        elif ident.startswith("libc-"):
            chemin = os.path.join(M1_DIR, "I", fichiers[ident])
        else:
            chemin = os.path.join(M2_DIR, "I", fichiers_m2[ident])
        if not os.path.exists(chemin):
            raise EchecBuild(f"spécification I introuvable pour {sid} : {chemin}")
        spec = bm.lire_spec(chemin)
        if spec["id"] != ident:
            raise EchecBuild(f"{chemin} : identifiant {spec['id']} != {ident}")
        if rev_ref > spec["rev"]:
            raise EchecBuild(f"{chemin} : révision référencée R{rev_ref} > fichier R{spec['rev']}")
        specs[bid] = spec

    for bid, sid, _, _, _ in blocs:
        charger(bid, sid)
    charger(*BLOC_STAGING[:2])
    return specs


# --- Oracle structurel : autorisations PAR BLOC (I1/I2, durci M2) ----------------

IAT_PAR_BLOC = {
    **bm.IAT_PAR_BLOC,
    "d40001": set(),
    "d40002": {"GetModuleHandleW", "LoadCursorW", "RegisterClassExW",
               "CreateWindowExW", "MessageBoxW"},
    "d40003": {"GetMessageW", "TranslateMessage", "DispatchMessageW"},
    "d40004": {"GetModuleHandleW", "CreateWindowExW", "GetStockObject",
               "SendMessageW", "GetClientRect", "MoveWindow", "EnableWindow",
               "DestroyWindow", "PostQuitMessage", "DefWindowProcW",
               "CloseHandle"},
    "d40005": {"SendMessageW"},
    "d40006": set(),
    "d40007": {"socket", "connect", "closesocket"},
    "d40008": {"CloseHandle"},
    "d40009": {"GetStdHandle", "CloseHandle", "send", "recv"},
    "d40010": {"send", "recv"},
}
APPELS_DIRECTS = {
    **bm.APPELS_DIRECTS,
    "d40001": {0x1440, 0x1580, 0x1080},
    "d40002": set(), "d40003": set(),
    "d40004": {0x4300, 0x1C40},
    "d40005": set(),
    "d40006": {0x1100, 0x1180, 0x1200, 0x1280},
    "d40007": set(),
    "d40008": {0x4000, 0x4100, 0x4300, 0x18C0},
    "d40009": {0x18C0, 0x1940, 0x1AC0, 0x1B80, 0x41C0, 0x4400, 0x4600, 0x1180, 0x4980, 0x4300},
    "d40010": {0x1180},
}
DONNEES_RIP = {
    **{k: v for k, v in bm.DONNEES_RIP.items()
       if k in {"c30007", "c30009", "c30011"}},   # blocs M2 embarqués (démo : héritage)
    "d40002": {L.CHAINES_UTF16["CLASSE"][0], L.CHAINES_UTF16["TITRE"][0],
               L.CHAINES_UTF16["MSG_ECHEC_GUI"][0], 0x1600, L.HWND_PRINCIPAL},
    "d40004": {L.HWND_JOURNAL, L.HWND_BOUTON, L.DRAPEAU_WORKER, 0x1C80,
               L.CHAINES_UTF16["CLASSE_EDIT"][0], L.CHAINES_UTF16["CLASSE_BOUTON"][0],
               L.CHAINES_UTF16["TXT_BOUTON"][0], L.CHAINES_UTF16["CHAINE_VIDE"][0]},
    "d40005": {L.HWND_JOURNAL},
    "d40006": {L.R_ANCRE, L.R_TAB_SUM, L.R_VERSION, 0x2630, 0x2640, 0x2644,
               0x2648, 0x264C, 0x265A},
    "d40007": set(),
    "d40008": {L.R_LISTEN, L.DRAPEAU_SRV, 0x4800, L.CHAINES_UTF16["J_SRV_KO"][0]},
    "d40009": {L.R_STDOUT, L.R_STDIN, L.R_QUIT, L.R_LISTEN, L.R_PHRASE,
               L.R_PHRASE_MAJ, 0x1B80,
               *[L.CHAINES_UTF16[n][0] for n in L.CHAINES_UTF16 if n.startswith("J_")] + [L.DRAPEAU_SRV]},
    "d40010": {L.R_PHRASE},
}
FEUILLES_DEMO = set()   # les blocs win appellent tous (IAT ou blocs) — pas de feuilles démo


def oracle_structurel(specs: dict, code: dict, blocs: list[tuple]) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    tous = list(blocs) + [BLOC_STAGING]
    adresses_insns = {bid: {i.address for i in code[bid]["insns"]} for bid, *_ in tous}
    adresses_blocs = {bid: rva for bid, _, _, rva, _ in tous}

    for bid, _, _, rva, slot in tous:
        insns = code[bid]["insns"]
        for i in insns:
            if i.mnemonic.startswith("j"):
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

    for bid in FEUILLES_DEMO:
        verrou(f"{bid}:feuille", not any(i.mnemonic == "call" for i in code[bid]["insns"]))

    # win-09 : en-tête puis autotest ; arrêt propre par drapeaux .data
    def canon_(i):
        return bm.canon(f"{i.mnemonic} {i.op_str}")

    s = code["d40009"]["insns"]
    verrou("d40009:autotest-present",
           any(canon_(i) == "call 0x1940" for i in s))
    verrou("d40009:arret-propre",
           any(canon_(i).startswith("mov qword ptr [rip") for i in s))

    # win-06 : porte R10 avant tout appel (I1) — miroir tcp-12
    a6 = code["d40006"]["insns"]
    premier_appel = next((k for k, i in enumerate(a6) if i.mnemonic == "call"), None)
    marqueur = [k for k, i in enumerate(a6) if canon_(i) == "add r12, 0x10"]
    verrou("d40006:porte-avant-tout-appel",
           premier_appel is not None and marqueur and premier_appel > marqueur[-1])
    verrou("tracabilite-I",
           set(specs) >= {b for b, *_ in blocs} | {"c30014"})
    return verrous


# --- Composition des sections -----------------------------------------------------

def composer_sections(code: dict, blocs: list[tuple]):
    texte = bytearray(b"\xcc" * L.TEXT_VSIZE)
    text2 = bytearray(b"\xcc" * L.TEXT2_VSIZE)
    for bid, _, _, rva, slot in blocs:
        if rva >= L.TEXT2_RVA:
            text2[rva - L.TEXT2_RVA: rva - L.TEXT2_RVA + slot] = code[bid]["slot"]
        else:
            texte[rva - L.TEXT_RVA: rva - L.TEXT_RVA + slot] = code[bid]["slot"]

    staging = code["c30014"]["slot"]

    # Table R10 : entrée 0 = staging (figée pour tcp-07), puis chaque bloc
    # embarqué, terminateur. La version u64 est celle de la lignée démo.
    entrees = [(L.R_STAGING, len(staging), bm._somme_qwords(staging))]
    for bid, _, _, rva, slot in blocs:
        base = texte if rva < L.TEXT2_RVA else text2
        off = rva - L.TEXT_RVA if rva < L.TEXT2_RVA else rva - L.TEXT2_RVA
        entrees.append((rva, slot, bm._somme_qwords(bytes(base[off: off + slot]))))
    entrees.append((0, 0, 0))
    table = b"".join(struct.pack("<IIQ", r, t, s) for r, t, s in entrees)
    assert L.R_TAB_SUM + len(table) <= L.R_VERSION, "table R10 déborde sur la version"

    rdata = bytearray(b"\x00" * L.RDATA_VSIZE)
    _poses = []

    def poser(rva: int, donnees: bytes, nom: str = ""):
        fin = rva + len(donnees)
        if rva - L.RDATA_RVA + len(donnees) > L.RDATA_VSIZE:
            raise EchecBuild(f".rdata débordante à {rva:#x}")
        for rva_p, fin_p, nom_p in _poses:
            if rva < fin_p and rva_p < fin:
                raise EchecBuild(f"chevauchement .rdata : {nom or hex(rva)} "
                                 f"recouvre {nom_p}")
        _poses.append((rva, fin, nom or hex(rva)))
        rdata[rva - L.RDATA_RVA: rva - L.RDATA_RVA + len(donnees)] = donnees

    hn = lambda nom: struct.pack("<H", 0) + nom.encode("ascii") + b"\x00"

    # Marché des imports : kernel32, ws2_32, user32, gdi32 + terminateur (D35)
    poser(L.R_DESC_IMPORT, struct.pack("<IIIII", L.R_INT_KERNEL32, 0, 0, L.R_NOM_DLL, L.R_IAT))
    poser(L.R_DESC_WS2, struct.pack("<IIIII", L.R_INT_WS2, 0, 0, L.R_NOM_WS2, L.R_IAT_WS2))
    poser(L.R_DESC_USER32, struct.pack("<IIIII", L.R_INT_USER32, 0, 0, L.R_NOM_USER32, L.R_IAT_USER32))
    poser(L.R_DESC_GDI32, struct.pack("<IIIII", L.R_INT_GDI32, 0, 0, L.R_NOM_GDI32, L.R_IAT_GDI32))
    poser(L.R_DESC_TERM, b"\x00" * 20)

    poser(L.R_NOM_DLL, b"kernel32.dll\x00")
    poser(L.R_NOM_WS2, b"ws2_32.dll\x00")
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

    hints_ws2 = {}
    rva_h = L.R_HN_WS2
    for nom in L2_WS2_BASE:
        hints_ws2[nom] = rva_h
        poser(rva_h, hn(nom))
        rva_h += len(hn(nom))
    hints_ws2["connect"] = L.R_HN_CONNECT
    poser(L.R_HN_CONNECT, hn("connect"))
    poser(L.R_INT_WS2, b"".join(struct.pack("<Q", hints_ws2[n]) for n in L.WS2_IMPORTS)
          + struct.pack("<Q", 0))
    poser(L.R_IAT_WS2, b"".join(struct.pack("<Q", hints_ws2[n]) for n in L.WS2_IMPORTS)
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

    poser(L.R_STAGING, staging)
    poser(L.R_TAB_SUM, table)
    poser(L.R_VERSION, struct.pack("<Q", L.VERSION_U64_DEMO1))
    poser(L.R_ANCRE, struct.pack("<Q", 0))
    poser(L.R_FIXTURES, L.FIXTURE_MEMCPY + L.FIXTURE_MEMCMP_A + L.FIXTURE_STRLEN
          + L.FIXTURE_ITOA)
    poser(L.R_MSG_CRLF, b"\r\n\x00", "CRLF")
    poser(L.R_MSG_ECHO, b"echo \x00", "ECHO")
    poser(L.R_MSG_FIN, b"fin connexion\r\n\x00", "FIN")
    poser(L.R_PHRASE, L.PHRASE, "PHRASE")
    poser(L.R_PHRASE_MAJ, L.PHRASE_MAJ, "PHRASE_MAJ")
    poser(L.R_RELOC, struct.pack("<II", L.TEXT_RVA, 12) + struct.pack("<HH", 0, 0))
    for nom, (adr, txt, n) in L.CHAINES_UTF16.items():
        poser(adr, txt.encode("utf-16-le") + b"\x00\x00", nom)

    data = bytearray(b"\x00" * L.DATA_RAW)
    return bytes(texte), bytes(rdata), bytes(data), bytes(text2), staging


L2_WS2_BASE = list(bm.L.WS2_IMPORTS)     # les 10 héritées (hints contigus 0x2360+)


# --- Éditeur PE32+ (WINDOWS_GUI) ---------------------------------------------------

def ecrire_pe32plus(texte, rdata, data, text2) -> bytes:
    dos = b"MZ" + b"\x00" * 58 + struct.pack("<I", 0x40)
    coff = struct.pack("<HHIIIHH", 0x8664, 4, 0, 0, 0, 0xF0, 0x0002)
    opt_fixe = struct.pack(
        "<HBBIIIIIQIIHHHHHHIIIIHHQQQQII",
        0x20B, 0, 0,
        L.ENTREE, len(texte) + len(text2), 0,
        L.ENTREE, L.TEXT_RVA,
        L.IMAGE_BASE,
        L.SECT_ALIGN, L.FILE_ALIGN,
        6, 0, 0, 1, 6, 0, 0,
        L.SIZE_OF_IMAGE, L.FILE_ALIGN, 0,
        L.SUBSYSTEM_GUI,                     # WINDOWS_GUI — la démo est graphique
        L.DLL_CHARACTERISTICS,
        0x100000, 0x1000, 0x100000, 0x1000,
        0, 16,
    )
    dirs = [(0, 0)] * 16
    dirs[1] = (L.R_DESC_IMPORT, 100)         # 5 descripteurs (4 dll + terminateur)
    dirs[5] = (L.R_RELOC, 12)
    dirs[12] = (L.R_IAT, 96)                 # IAT kernel32 (11 slots + terme)
    opt = bytes(opt_fixe) + b"".join(struct.pack("<II", *d) for d in dirs)

    def sh(nom, vsize, vaddr, rawsz, rawptr, cara):
        return struct.pack("<8sIIIIIIHHI", nom, vsize, vaddr, rawsz, rawptr, 0, 0, 0, 0, cara)

    sections = (
        sh(b".text\x00\x00\x00", L.TEXT_VSIZE, L.TEXT_RVA, L.TEXT_VSIZE, L.TEXT_FILE, 0x60000020)
        + sh(b".rdata\x00\x00", L.RDATA_VSIZE, L.RDATA_RVA, L.RDATA_VSIZE, L.RDATA_FILE, 0x40000040)
        + sh(b".data\x00\x00\x00", L.DATA_VSIZE, L.DATA_RVA, L.DATA_RAW, L.DATA_FILE, 0xC0000040)
        + sh(b".text2\x00\x00", L.TEXT2_VSIZE, L.TEXT2_RVA, L.TEXT2_VSIZE, L.TEXT2_FILE, 0x60000020)
    )
    entetes = dos + b"PE\x00\x00" + coff + opt + sections
    assert len(entetes) == 64 + 4 + 20 + 240 + 160
    exe = bytearray(b"\x00" * L.TAILLE_FICHIER)
    exe[0:len(entetes)] = entetes
    exe[L.TEXT_FILE:L.TEXT_FILE + len(texte)] = texte
    exe[L.RDATA_FILE:L.RDATA_FILE + len(rdata)] = rdata
    exe[L.DATA_FILE:L.DATA_FILE + len(data)] = data
    exe[L.TEXT2_FILE:L.TEXT2_FILE + len(text2)] = text2
    return bytes(exe)


def valider_pe(exe: bytes):
    pe = pefile.PE(data=exe)
    assert pe.FILE_HEADER.Machine == 0x8664
    assert pe.FILE_HEADER.NumberOfSections == 4
    assert pe.OPTIONAL_HEADER.Magic == 0x20B
    assert pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE, "entrée != win-01"
    assert pe.OPTIONAL_HEADER.Subsystem == L.SUBSYSTEM_GUI, "sous-système != WINDOWS_GUI"
    assert pe.OPTIONAL_HEADER.SizeOfImage == L.SIZE_OF_IMAGE
    noms = [s.Name.decode().rstrip("\x00") for s in pe.sections]
    assert noms == [".text", ".rdata", ".data", ".text2"], noms
    imports = {}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        imports[entree.dll.decode().lower()] = [i.name.decode() for i in entree.imports]
    attendu = {"kernel32.dll": L.KERNEL32_IMPORTS, "ws2_32.dll": L.WS2_IMPORTS,
               "user32.dll": L.USER32_IMPORTS, "gdi32.dll": L.GDI32_IMPORTS}
    assert imports == attendu, {k: set(v) ^ set(attendu.get(k, [])) for k, v in imports.items()}
    # D35 : verrou chargeur réel — FT = slots appelés par la notation
    ft_attendus = {"kernel32.dll": L.R_IAT, "ws2_32.dll": L.R_IAT_WS2,
                   "user32.dll": L.R_IAT_USER32, "gdi32.dll": L.R_IAT_GDI32}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        dll = entree.dll.decode().lower()
        assert entree.struct.FirstThunk == ft_attendus[dll], \
            f"FirstThunk {dll} != {ft_attendus[dll]:#x} (D35)"
    assert len(exe) == L.TAILLE_FICHIER
    assert exe[L.TEXT2_FILE + (L.ECHO_CROISSANCE - L.TEXT2_RVA)] == 0xCC   # croissance int3
    assert exe[L.TEXT_FILE + (0x1300 - L.TEXT_RVA)] == 0xCC                # réserve libc int3
    return True


SHA_HELLO = bm.SHA_HELLO
SHA_SELFTEST = bm.SHA_SELFTEST
SHA_ECHO = None       # rempli au chargement (empreinte d'echo.exe 0.3.0-rc.2)


def preuve_reutilisation(exe: bytes) -> dict:
    """io/libc vs hello.exe/selftest.exe ; tcp vs echo.exe rc.2 — R7."""
    with open(os.path.join(M0_DIR, "hello.exe"), "rb") as f:
        hello = f.read()
    with open(os.path.join(M1_DIR, "selftest.exe"), "rb") as f:
        selftest = f.read()
    with open(os.path.join(M2_DIR, "echo.exe"), "rb") as f:
        echo = f.read()
    global SHA_ECHO
    SHA_ECHO = hashlib.sha256(echo).hexdigest()
    assert len(echo) == L.TAILLE_FICHIER, "echo.exe rc.2 de taille inattendue"
    tranche = lambda buf, rva, slot, base_rva, base_file: (
        buf[base_file + (rva - base_rva): base_file + (rva - base_rva) + slot])
    heritage = ([("a10002", hello, 0x1040, 0x40), ("a10003", hello, 0x1080, 0x40),
                 ("b20001", selftest, 0x1100, 0x80), ("b20002", selftest, 0x1180, 0x80),
                 ("b20003", selftest, 0x1200, 0x80), ("b20004", selftest, 0x1280, 0x80)]
                + [(bid, echo, rva, slot) for bid, _, _, rva, slot in blocs_demo()
                   if bid.startswith("c3")])
    for bid, source, rva, slot in heritage:
        base_rva, base_file = (L.TEXT2_RVA, L.TEXT2_FILE) if rva >= L.TEXT2_RVA \
            else (L.TEXT_RVA, L.TEXT_FILE)
        if tranche(source, rva, slot, base_rva, base_file) != tranche(exe, rva, slot, base_rva, base_file):
            raise EchecBuild(f"réutilisation rompue : {bid} diffère de l'artefact scellé (R7)")
    # staging identique à celui d'echo.exe (tcp-08:R2, boucle § 5)
    if exe[L.RDATA_FILE + (L.R_STAGING - L.RDATA_RVA): L.RDATA_FILE + (L.R_STAGING - L.RDATA_RVA) + 0x80] \
            != echo[L.RDATA_FILE + (L.R_STAGING - L.RDATA_RVA): L.RDATA_FILE + (L.R_STAGING - L.RDATA_RVA) + 0x80]:
        raise EchecBuild("staging echo-01:R2 divergent d'echo.exe (R7)")
    return {"blocs_reutilises": [b[0] for b in heritage]}


# --- Carte lignée démo (génération 4) ----------------------------------------------

CONTRATS = {
    **bm.CONTRATS,          # contrats hérités M0/M1/M2 (frag-con : traçabilité)
    "d40001": ("() -> noreturn", "point d'entrée demo.exe ; pile alignée",
               "fenêtre puis boucle puis ExitProcess(0|1) via io-02 scellé",
               "appels win-02/win-03/io-02 uniquement ; aucun état",
               "[d40002] [d40003] [a10003]"),
    "d40002": ("() -> ptr|0", "IAT résolue (D35) ; pile alignée",
               "rax = hwnd ; HWND_PRINCIPAL posé ; échec -> MessageBoxW + 0",
               "WNDCLASSEXW sur pile ; aucune adresse absolue (PI)",
               "[ext user32:RegisterClassExW,CreateWindowExW,LoadCursorW,MessageBoxW] "
               "[ext kernel32:GetModuleHandleW] [rdata:UTF-16]"),
    "d40003": ("() -> u32", "fenêtre existante ; pile alignée",
               "file drainée ; rax = 0 après WM_QUIT ou erreur",
               "MSG sur pile ; aucune donnée .data",
               "[ext user32:GetMessageW,TranslateMessage,DispatchMessageW]"),
    "d40004": ("(hwnd, msg u32, wParam, lParam) -> lresult",
               "callback msx64 ; WM_CREATE précède tout ; IAT résolue",
               "contrôles créés au WM_CREATE ; clic unique -> spawn(win-09) ; "
               "défaut -> DefWindowProcW",
               "wParam/lParam sauvegardés avant appels ; spawn PAR tcp-06 scellé",
               "[c30006] [d40009] [ext user32:*] [ext gdi32:GetStockObject] "
               "[ext kernel32:GetModuleHandleW,CloseHandle] [donnees .data:hwnds,drapeau]"),
    "d40005": ("(ptr UTF-16, nchars u64) -> u32",
               "HWND_JOURNAL posé par win-04 ; pile alignée",
               "ligne ajoutée en fin de journal (EM_SETSEL + EM_REPLACESEL)",
               "exactement deux SendMessageW ; appelable de tout thread",
               "[ext user32:SendMessageW] [donnees .data:hwnd_journal]"),
    "d40006": ("() -> i32", "image cohérente avec la table R10 ; pile alignée",
               "eax = -1 (porte KO) | 0..4 (vecteurs libc verts)",
               "porte AVANT tout appel (R10) ; lecture seule .rdata",
               "[b20001] [b20002] [b20003] [b20004] "
               "[rdata:table,version,ancre,fixtures]"),
    "d40007": ("() -> ptr|0", "WSA actif (tcp-01 serveur lancé avant) ; pile alignée",
               "rax = socket cliente | 0 (échec : socket fermée, .data intact)",
               "sockaddr sur pile ; IAT ws2_32 exclusivement",
               "[ext ws2_32:socket,connect,closesocket]"),
    "d40008": ("(arg u64) -> u32", "thread dédié ; appelé une fois ; pile alignée",
               "écoute publiée (R_LISTEN, drapeau 1) ; boucle accept->spawn "
               "tcp-09 ; arrêt propre sur accept<0 ; échec -> drapeau 2",
               "aucun ExitProcess (thread de service) ; arrêt par R_QUIT+close",
               "[c30001] [c30002] [c30006] [d40005] [ext kernel32:CloseHandle] "
               "[donnees .data:listen,drapeau_srv]"),
    "d40009": ("(arg u64) -> u32", "lancé une fois par win-04 ; pile alignée",
               "journal = preuves : porte, libc, mécanique v1->v2->v1, "
               "serveur, client, boucle § 5 complète ; arrêt propre garanti",
               "aucun succès non prouvé par memcmp ; nettoyage sur tout chemin",
               "[d40005] [d40006] [d40007] [d40008] [d40010] [c30005] [c30007] "
               "[c30008] [b20002] [ext kernel32:GetStdHandle,CloseHandle] "
               "[ext ws2_32:send,recv] [donnees .data] [rdata:UTF-16,phrases]"),
    "d40010": ("(sock, attendu ptr) -> bool",
               "socket connectée ; attendu = 14 octets .rdata ; pile alignée",
               "eax = 1 si émission complète + 14 reçus == attendu (memcmp) ; 0 sinon",
               "socket laissée ouverte (politique de l'appelant) ; tampon sur pile",
               "[b20002] [ext ws2_32:send,recv] [rdata:PHRASE]"),
}


def fragments_clairs(code, exe, verrous, blocs, version, verdict, compteurs, journal_runs):
    sha = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()
    loc = ["[carte-frag] nom=frag-loc generation=4",
           "[zones] io=0x1000-0x10ff libc=0x1100-0x12ff app-win=0x1400-0x1fbf "
           "net=0x4000-0x42ff thr=0x4300-0x43ff tramp=0x4400-0x45ff "
           "echo=0x4600-0x46ff croissance=0x4680 srv=0x4800-0x4fff"]
    spec_map = {bid: sid for bid, sid, _, _, _ in blocs}
    for bid, _, _, rva, slot in blocs + [("c30014", "tcp-08:R2", None, L.ECHO_CROISSANCE, 0x80)]:
        etat = "verifie" if bid == "c30014" else "scelle"
        loc.append(f"[bloc] id={bid} spec={spec_map.get(bid, 'tcp-08:R2')} cible=x86-64-win11-pe "
                   f"exe=demo addr={L.IMAGE_BASE + rva:#x} size={slot} v=1 "
                   f"etat={etat} role={L.NOMS_BLOCS[bid]}")
    con = ["[carte-frag] nom=frag-con generation=4"]
    for bid, _, _, _, _ in blocs:
        sig, pre, post, inv, deps = CONTRATS[bid]
        con += [f"[bloc] id={bid}", f"  sig : {sig}", f"  pre : {pre}",
                f"  post : {post}", f"  inv : {inv}", f"  deps : {deps}"]
    prf = ["[carte-frag] nom=frag-prf generation=4"]
    for bid, _, fichier, _, _ in blocs:
        with open(chemin_notation(fichier), "rb") as f:
            empreinte = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} crist={crist}/10",
                f"  vecteurs : roundtrip=ok structure=ok notation={empreinte}",
                f"  differentiel : {verdict.get('blocs', {}).get(bid, {}).get('detail', '-')}"]
    prf.append("[verifications] runs=" + str(len(journal_runs)))
    prf += ["  " + r for r in journal_runs[-12:]]
    bld = ["[carte-frag] nom=frag-bld generation=4"]
    for bid, _, _, rva, slot in blocs:
        base_rva, base_file = (L.TEXT2_RVA, L.TEXT2_FILE) if rva >= L.TEXT2_RVA \
            else (L.TEXT_RVA, L.TEXT_FILE)
        tranche = exe[base_file + (rva - base_rva): base_file + (rva - base_rva) + slot]
        bld.append(f"[bloc] id={bid} addr={L.IMAGE_BASE + rva:#x} empreinte={sha(tranche)}")
    bld.append(f"[bloc] id=c30014 addr={L.IMAGE_BASE + L.ECHO_CROISSANCE:#x} "
               f"empreinte={sha(exe[L.RDATA_FILE + (L.R_STAGING - L.RDATA_RVA): L.RDATA_FILE + (L.R_STAGING - L.RDATA_RVA) + 0x80])}")
    bld += [
        f"[build] artefact=demo.exe version={version} profil=x86-64-win11-pe "
        f"taille={len(exe)} empreinte={sha(exe)}",
        f"  outils : keystone + capstone {capstone.cs_version()[0]}.{capstone.cs_version()[1]} ; "
        f"verrous={len(verrous)} ; oracle : {verdict.get('total_cas', 0)} cas, "
        f"graine={verdict.get('graine', '-')}",
        f"  heritage : hello.exe + selftest.exe + echo.exe 0.3.0-rc.2 "
        f"(io/libc/tcp + staging reutilises octet-identiques, R7 ; D35)",
        f"[zones] app-win=0x1400-0x1fbf srv-win10=0x4980",
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
    with open(os.path.join(ICI, "demo.exe"), "rb") as f:
        exe = f.read()
    empreintes, manifestes = {}, []
    for ligne in bld.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[champs["id"]] = champs["empreinte"]
        elif ligne.startswith("[build]"):
            manifestes.append(dict(re.findall(r"(\w+)=(\S+)", ligne)))
    manifeste = next((m for m in manifestes if m.get("artefact") == "demo.exe"), {})
    for bid, _, _, rva, slot in blocs:
        base_rva, base_file = (L.TEXT2_RVA, L.TEXT2_FILE) if rva >= L.TEXT2_RVA \
            else (L.TEXT_RVA, L.TEXT_FILE)
        tranche = exe[base_file + (rva - base_rva): base_file + (rva - base_rva) + slot]
        if "sha256:" + hashlib.sha256(tranche).hexdigest() != empreintes.get(bid):
            raise cm.ErreurCarte(f"verrou croisé : empreinte de {bid} divergente (R8)")
    if "sha256:" + hashlib.sha256(exe).hexdigest() != manifeste.get("empreinte"):
        raise cm.ErreurCarte("verrou croisé : empreinte de demo.exe divergente (R8)")
    return len(empreintes), manifeste


def tableau_de_bord(exe, verrous, nb, manifeste, verdict) -> str:
    lignes = [
        "[tableau] jalon=demo artefact=demo.exe version=" + manifeste.get("version", "?"),
        f"  blocs_avec_spec_a_jour        : {nb}/{nb} : tracabilite I->C->B (heritage M0/M1/M2 + win)",
        f"  chaines_I_C_B_tests           : {nb}/{nb}",
        f"  construction                  : 0 erreur / 0 avertissement",
        f"  tests_differentiels           : {verdict.get('total_cas', 0)} cas verts "
        f"(graine {verdict.get('graine', '-')}) ; oracle structurel {len(verrous)} verrous PASS",
        f"  empreintes_donnees_embarquees : conforme (staging, table R10, UTF-16, fixtures)",
        f"  defauts_T1_T6_ouverts         : 0 : D35 consignee (correctif rc.2 + demo)",
        f"  optimisations_sans_mesure     : 0 : aucune (R11)",
        f"  budgets_tokens                : cible (instrumentation a executer)",
        f"  suite_conformite_profil       : heritee M2 (124/124, rc.2) + porte D35 verifiee par oracle",
        f"  changements_hors_journal      : 0 : D35 consignee",
        f"  preversions                   : {manifeste.get('version', '?')} (lignee demo, "
        f"u64 0x{L.VERSION_U64_DEMO1:x}, plancher 0x{L.VERSION_U64_MIN:x})",
        f"  patch_a_chaud                 : boucle 5 complete en production "
        f"(patch pendant trafic + rollback) DEMONTREE par le scenario (oracle)",
        f"  artefact                      : {len(exe)} octets ; "
        f"reutilisation : 16 blocs + staging octet-identiques (R7)",
        f"  verrou_croise                 : {nb} empreintes reverifiees + signature Ed25519 (R8/R9)",
    ]
    return "\n".join(lignes) + "\n"


# --- Assemblage + vérification ------------------------------------------------------

def assembler_tout():
    blocs = blocs_demo()
    specs = charger_couche_I(blocs)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code = {}
    tous = list(blocs) + [BLOC_STAGING]
    for bid, sid, fichier, rva, slot in tous:
        chemin = chemin_notation(fichier)
        octets, metas = bm.assembler_bloc(ks, chemin, rva, slot)
        insns = bm.round_trip(cs, ks, chemin, rva, octets, metas)
        code[bid] = {"octets": octets, "insns": insns,
                     "slot": octets + b"\x90" * (slot - len(octets))}
        print(f"[R5] {bid} ({sid}) : {len(octets)} o, round-trip {len(insns)}/{len(insns)} = 100 %")
    verrous = oracle_structurel(specs, code, blocs)
    print(f"[oracle] structurel : {len(verrous)} verrous PASS (contrats I verifies par bloc)")
    return blocs, specs, code, verrous


def construire(graine: int) -> int:
    print("=== démo : chaîne artefact TRIADE (profil x86-64-win11-pe, WINDOWS_GUI) ===")
    blocs, specs, code, verrous = assembler_tout()
    version = L.VERSION_DEMO1
    texte, rdata, data, text2, staging = composer_sections(code, blocs)
    exe = ecrire_pe32plus(texte, rdata, data, text2)
    valider_pe(exe)
    heritage = preuve_reutilisation(exe)
    print(f"[PE] demo.exe : {len(exe)} octets, 4 sections, kernel32 x11 + ws2_32 x11 + "
          f"user32 x14 + gdi32 x1, WINDOWS_GUI, entree 0x{L.ENTREE:x}, FT=slots (D35)")
    print(f"[R7] réutilisation : {len(heritage['blocs_reutilises'])} blocs + staging "
          f"octet-identiques aux artefacts scellés M0/M1/M2 (echo 0.3.0-rc.2)")

    verdict = od.executer(exe, graine=graine)
    print(f"[oracle] différentiel : {verdict['total_cas']} cas verts ; "
          f"falsification : {verdict['falsification']}")

    with open(os.path.join(ICI, "demo.exe"), "wb") as f:
        f.write(exe)
    compteurs = {bid: 1 for bid, _, _, _, _ in blocs}
    journal = [f"run graine={graine} verdict={verdict['empreinte']} "
               f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} build={version}"]
    construire_carte(code, exe, verrous, blocs, version, verdict, compteurs, journal)
    nb, manifeste = verrou_croise(blocs)
    print(f"[carte] lignée démo (génération 4) écrite : 4 fragments, signature Ed25519, "
          f"{nb} empreintes indexées")
    print(f"[R8] verrou croisé : signature OK, racine OK, artefact {manifeste.get('version')}")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="utf-8") as f:
        f.write(tableau_de_bord(exe, verrous, nb, manifeste, verdict))
    print(f"[B] demo.exe scellé : sha256:{hashlib.sha256(exe).hexdigest()}")
    print(f"=== démo {version} (oracle vert) — validation terrain Windows 11 en attente ===")
    return 0


def verifier(graine: int) -> int:
    print(f"=== démo : re-vérification complète (R5/R8, graine {graine}) ===")
    blocs, specs, code, verrous = assembler_tout()
    with open(os.path.join(ICI, "demo.exe"), "rb") as f:
        exe = f.read()
    for bid, _, _, rva, slot in blocs:
        base_rva, base_file = (L.TEXT2_RVA, L.TEXT2_FILE) if rva >= L.TEXT2_RVA \
            else (L.TEXT_RVA, L.TEXT_FILE)
        if exe[base_file + (rva - base_rva): base_file + (rva - base_rva) + slot] != code[bid]["slot"]:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5)")
    verdict = od.executer(exe, graine=graine)
    print(f"[oracle] différentiel : {verdict['total_cas']} cas verts")
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
                    if "artefact=demo.exe" in l), L.VERSION_DEMO1)
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
        sys.exit(construire(graine))
    except (EchecBuild, cm.ErreurCarte, od.EchecOracle) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
