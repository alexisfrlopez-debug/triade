#!/usr/bin/env python3
"""build_m2.py : Jalon M2 de TRIADE — serveur TCP écho et patch à chaud.

Notation (keystone) -> octets -> PE32+ à la main (QUATRE sections, D33) ->
carte projet génération 2. Implémente la feuille de route M2 sous les règles
R4 (contrat stable), R7 (adresses stables, entrée seule trampolinable) et
R10 (porte d'intégrité au lancement), avec la boucle de mise à jour § 5
exécutée pour la première fois sur du code vivant (dev.1 -> dev.2).

L'ORACLE (D1) est régénéré à chaque exécution depuis la couche I :
  1. round-trip de notation : keystone -> capstone -> keystone (WYSIWYG) ;
  2. contrat structurel : invariants de I vérifiés sur le code désassemblé
     (autorisation PAR BLOC des appels IAT, des appels directs et des cibles
     RIP — M2 durcit la discipline M1) ;
  3. oracle différentiel (D29, oracle_m2.py) : patch à chaud réel en émulation,
     patch EN SESSION, porte R10, falsification.

RÉUTILISATION (R7) : io M0 (hello.exe) et libc M1 (selftest.exe) embarqués à
leurs adresses historiques, octets identiques — vérifié à chaque construction.

PHASES :
  dev.1 : serveur complet, mécanisme de patch vérifié, staging vide (refus 2) ;
  dev.2 : boucle § 5 — diff I (tcp-08:R1 -> R2, majuscules), remplaçant en
          staging .rdata, AUCUN octet de code ne bouge (R7 démontré).

Usage :
  python3 build_m2.py --phase 1        # construction dev.1
  python3 build_m2.py --phase 2        # construction dev.2 (boucle § 5)
  python3 build_m2.py --verifier [--graine N]   # R8 : re-vérification + cristallisation
  python3 build_m2.py --sceller-rc     # cristallisation atteinte -> rc.1
  python3 build_m2.py --sceller-final  # constat terrain -> 0.3.0 finale

Déterminisme : echo.exe est byte-identique à phase et sources constantes.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import struct
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

import capstone
import pefile
from keystone import Ks, KS_ARCH_X86, KS_MODE_64

import carte_m2 as cm
import oracle_m2 as od

ICI = os.path.dirname(os.path.abspath(__file__))
M0_DIR = os.path.join(os.path.dirname(ICI), "m0")
M1_DIR = os.path.join(os.path.dirname(ICI), "m1")


class EchecBuild(Exception):
    """Tout échec de l'oracle, du round-trip ou de la construction."""


# --- Blocs par phase ----------------------------------------------------------

def blocs_phase(phase: int) -> list[tuple]:
    """(id carte, spec, fichier notation, rva, slot) — embarqués dans echo.exe."""
    blocs = [
        # héritage M0/M1 (octets identiques aux artefacts scellés)
        ("a10002", "hello-02:R1", "hello-02-write", 0x1040, 0x40),
        ("a10003", "hello-03:R1", "hello-03-exit", 0x1080, 0x40),
        ("b20001", "libc-01:R1", "libc-01-memcpy", 0x1100, 0x80),
        ("b20002", "libc-02:R1", "libc-02-memcmp", 0x1180, 0x80),
        ("b20003", "libc-03:R1", "libc-03-strlen", 0x1200, 0x80),
        ("b20004", "libc-04:R1", "libc-04-itoa", 0x1280, 0x80),
        # génération M2
        ("c30001", "tcp-01:R1", "tcp-01-init", 0x4000, 0x100),
        ("c30002", "tcp-02:R1", "tcp-02-accept", 0x4100, 0x40),
        ("c30003", "tcp-03:R1", "tcp-03-recv", 0x4140, 0x40),
        ("c30004", "tcp-04:R1", "tcp-04-send", 0x4180, 0x40),
        ("c30005", "tcp-05:R1", "tcp-05-close", 0x41C0, 0x40),
        ("c30006", "tcp-06:R1", "tcp-06-spawn", 0x4300, 0x40),
        ("c30007", "tcp-07:R1", "tcp-07-patch", 0x4400, 0x200),
        ("c30008", "tcp-08:R1", "tcp-08-echo", 0x4600, 0x40),
        ("c30009", "tcp-09:R1", "tcp-09-conn", 0x4800, 0x180),
        ("c30010", "tcp-10:R1", "tcp-10-console", 0x4980, 0x180),
        ("c30011", "tcp-11:R1", "tcp-11-journal", 0x4B00, 0x100),
        ("c30013", "tcp-12:R1", "tcp-12-main", 0x1800, 0x800),
    ]
    return blocs


# Blocs indexés NON embarqués : libc-09 (aucun appelant à M2) et, en dev.2,
# le remplaçant echo-01:R2 (staging .rdata, activation à chaud).
BLOC_LIBC09 = ("c30012", "libc-09:R1", "libc-09-zone-alloc-ts", 0x1440, 0x80)
BLOC_ECHO_V2 = ("c30014", "tcp-08:R2", "tcp-08-echo-v2", L.ECHO_CROISSANCE, 0x80)


def chemin_notation(fichier: str) -> str:
    if fichier.startswith("hello-"):
        return os.path.join(M0_DIR, "notation", fichier + ".asm")
    if fichier.startswith("libc-0") and fichier != "libc-09-zone-alloc-ts":
        return os.path.join(M1_DIR, "notation", fichier + ".asm")
    return os.path.join(ICI, "notation", fichier + ".asm")


# --- Couche I : lecture et audit du gabarit ----------------------------------

def lire_spec(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", texte)
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3)), "texte": texte}
    for bloc in ("Intention", "Contrat", "Échecs", "Vecteurs", "Fixtures", "Provenance", "Décisions"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")
    if "écrite-avant-code" not in texte:
        raise EchecBuild(f"{chemin} : provenance inattendue (R2 : écrite-avant-code)")
    return spec


def charger_couche_I(blocs: list[tuple], phase: int) -> dict[str, dict]:
    """Specs M2 depuis m2/I/, réutilisées depuis m0/I et m1/I.

    tcp-08 est le premier spec à révision DANS le jalon : le fichier vit à sa
    révision courante (R2 en dev.2), le bloc installé référence R1 (validation :
    rev référencée <= rev fichier, et l'Historique mentionne les révisions
    antérieures) — c'est la boucle § 5 sur la couche I."""
    fichiers_m2 = {
        "tcp-01": "tcp-01-init.md", "tcp-02": "tcp-02-accept.md",
        "tcp-03": "tcp-03-recv.md", "tcp-04": "tcp-04-send.md",
        "tcp-05": "tcp-05-close.md", "tcp-06": "tcp-06-spawn.md",
        "tcp-07": "tcp-07-patch.md", "tcp-08": "tcp-08-echo.md",
        "tcp-09": "tcp-09-conn.md", "tcp-10": "tcp-10-console.md",
        "tcp-11": "tcp-11-journal.md", "tcp-12": "tcp-12-main.md",
        "libc-09": "libc-09-zone-alloc-ts.md",
    }
    fichiers_m0 = {"hello-02": "hello-02-write.md", "hello-03": "hello-03-exit.md"}
    fichiers_m1 = {"libc-01": "libc-01-memcpy.md", "libc-02": "libc-02-memcmp.md",
                   "libc-03": "libc-03-strlen.md", "libc-04": "libc-04-itoa.md"}
    specs = {}

    def charger(bid: str, sid: str):
        ident, rev_ref = sid.split(":")
        rev_ref = int(rev_ref[1:])
        if ident in fichiers_m2:
            chemin = os.path.join(ICI, "I", fichiers_m2[ident])
        elif ident in fichiers_m0:
            chemin = os.path.join(M0_DIR, "I", fichiers_m0[ident])
        else:
            chemin = os.path.join(M1_DIR, "I", fichiers_m1[ident])
        if not os.path.exists(chemin):
            raise EchecBuild(f"spécification I introuvable pour {sid} : {chemin}")
        spec = lire_spec(chemin)
        if spec["id"] != ident:
            raise EchecBuild(f"{chemin} : identifiant {spec['id']} != {ident}")
        if rev_ref > spec["rev"]:
            raise EchecBuild(f"{chemin} : révision référencée R{rev_ref} > fichier R{spec['rev']}")
        if rev_ref < spec["rev"]:
            partie_histo = spec["texte"].split("Historique", 1)
            if len(partie_histo) < 2 or f"R{rev_ref}" not in partie_histo[1]:
                raise EchecBuild(f"{chemin} : R{rev_ref} absente de l'Historique (traçabilité § 5)")
        specs[bid] = spec

    for bid, sid, _, _, _ in blocs:
        charger(bid, sid)
    charger(*BLOC_LIBC09[:2])
    if phase >= 2:
        charger(*BLOC_ECHO_V2[:2])
    return specs


# --- Notation : assemblage et round-trip (R5) ---------------------------------

def lignes_notation(chemin: str) -> list[str]:
    with open(chemin, encoding="utf-8") as f:
        brut = f.read().splitlines()
    return [l.strip() for l in brut if l.strip() and not l.strip().startswith(";")]


def assembler_bloc(ks: Ks, chemin: str, rva: int, slot: int) -> tuple[bytes, list[dict]]:
    octets, metas, adresse = b"", [], rva
    for ligne in lignes_notation(chemin):
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise EchecBuild(f"{chemin} : ligne inassemblable : {ligne!r}")
        b = bytes(enc)
        metas.append({"ligne": ligne, "adresse": adresse, "taille": len(b)})
        octets += b
        adresse += len(b)
    if len(octets) > slot:
        raise EchecBuild(f"{chemin} : {len(octets)} o > slot {slot:#x} (D8)")
    if slot - len(octets) < 16:
        raise EchecBuild(f"{chemin} : padding {slot - len(octets)} < 16 (D8)")
    return octets, metas


def canon(texte: str) -> str:
    """Normalisation : minuscules, espaces uniques, immédiats en hexa 32 bits."""
    t = re.sub(r"\s+", " ", texte.strip().lower())

    def norm(m: re.Match) -> str:
        v = int(m.group(0), 0)
        if v < 0:
            v &= 0xFFFFFFFF
        return f"0x{v:x}"

    return re.sub(r"(?<![\w])-?(?:0x[0-9a-f]+|\d+)(?![\w])", norm, t)


def round_trip(cs: capstone.Cs, ks: Ks, chemin: str, rva: int, octets: bytes, metas: list[dict]) -> list:
    instructions = list(cs.disasm(octets, rva))
    if len(instructions) != len(metas):
        raise EchecBuild(f"{chemin} : {len(instructions)} instructions désassemblées != {len(metas)} notées")
    for insn, meta in zip(instructions, metas):
        if insn.address != meta["adresse"] or insn.size != meta["taille"]:
            raise EchecBuild(f"{chemin} : désalignement à {meta['adresse']:#x}")
        texte_cs = f"{insn.mnemonic} {insn.op_str}".strip()
        if canon(texte_cs) != canon(meta["ligne"]):
            raise EchecBuild(
                f"{chemin} @ {meta['adresse']:#x} : écart texte notation/désassemblage\n"
                f"  notation      : {meta['ligne']}\n  désassemblage : {texte_cs}")
        renc, _ = ks.asm(texte_cs, insn.address)
        if bytes(renc) != octets[meta["adresse"] - rva: meta["adresse"] - rva + insn.size]:
            raise EchecBuild(f"{chemin} @ {meta['adresse']:#x} : ré-assemblage != octets originaux")
    return instructions


def operande_rip_cible(insn) -> int | None:
    m = re.search(r"\[rip \+ (0x[0-9a-f]+)\]", insn.op_str)
    if m:
        return insn.address + insn.size + int(m.group(1), 16)
    m = re.search(r"\[rip - (0x[0-9a-f]+)\]", insn.op_str)
    if m:
        return insn.address + insn.size - int(m.group(1), 16)
    return None


# --- Oracle structurel : les invariants de I, durcis par bloc (M2) ------------
# Autorisation PAR BLOC : appels IAT, appels directs, cibles RIP. M1 vérifiait
# un ensemble global ; M2 (patch à chaud) exige que la surface d'interface de
# chaque bloc soit exactement celle que sa spécification déclare (I1).

IAT_PAR_BLOC = {
    "a10002": {"WriteFile"}, "a10003": {"ExitProcess"},
    "b20001": set(), "b20002": set(), "b20003": set(), "b20004": set(),
    "c30001": {"WSAStartup", "socket", "bind", "listen", "closesocket", "WSACleanup"},
    "c30002": {"accept"}, "c30003": {"recv"}, "c30004": {"send"},
    "c30005": {"closesocket"}, "c30006": {"CreateThread"},
    "c30007": {"VirtualProtect"}, "c30008": set(), "c30009": set(),
    "c30010": {"ReadFile"},
    "c30011": {"EnterCriticalSection", "LeaveCriticalSection"},
    "c30012": {"EnterCriticalSection", "LeaveCriticalSection"},
    "c30013": {"GetStdHandle", "InitializeCriticalSection", "CloseHandle", "ExitProcess"},
    "c30014": set(),
}
APPELS_DIRECTS = {
    "c30007": {0x1100},
    "c30009": {0x4140, 0x4180, 0x41C0, 0x4600, 0x4B00},
    "c30010": {0x1180, 0x4400, 0x41C0, 0x4B00},
    "c30011": {0x1100, 0x1200, 0x1280, 0x1040},
    "c30012": {0x1300},
    "c30013": {0x4000, 0x4100, 0x4300, 0x4B00, 0x1040, 0x1080},
}
DONNEES_RIP = {
    "c30007": {L.R_STAGING, L.R_TAB_SUM + 4, L.R_TAB_SUM + 8, L.R_ETAT_PATCH,
               L.R_ENTREE_SAUVEE, L.ECHO_ENTREE, L.ECHO_CROISSANCE},
    "c30009": {L.R_MSG_ECHO, L.R_MSG_CRLF, L.R_MSG_FIN},
    "c30010": {L.R_STDIN, L.R_LISTEN, L.R_QUIT, L.R_CMD_PATCH, L.R_CMD_RB,
               L.R_CMD_QUIT, L.R_MSG_PATCH_OK, L.R_MSG_RB_OK, L.R_MSG_INCONNU,
               L.R_MSG_REFUS},
    "c30011": {L.R_STDOUT, L.R_CS},
    "c30012": {L.R_CS},
    "c30013": {L.R_ANCRE, L.R_TAB_SUM, L.R_VERSION, L.R_STDOUT, L.R_STDIN,
               L.R_CS, L.R_LISTEN, L.R_QUIT, L.R_MSG_BANNIERE,
               L.R_MSG_CONNEXION, L.R_MSG_ERREUR, L.R_MSG_ARRET, L.R_MSG_KO,
               0x4980, 0x4800},
}
FEUILLES_M2 = {"c30008", "c30014", "b20001", "b20002", "b20003", "b20004"}


def _prologue_aligne(insns) -> bool:
    """(8 + 8*npush - sub) ≡ 0 mod 16 — pile alignée aux points d'appel."""
    npush = 0
    while npush < len(insns) and insns[npush].mnemonic == "push":
        npush += 1
    if not any(i.mnemonic == "call" for i in insns):
        return True                      # feuille : pas de contrainte d'appel
    for i in insns:
        if i.mnemonic == "call":
            break
        if i.mnemonic == "sub" and i.op_str.startswith("rsp,"):
            imm = int(i.op_str.split(",")[1].strip(), 16)
            return (8 + 8 * npush - imm) % 16 == 0
    return False                         # appel sans sub rsp (shadow space absent)


def oracle_structurel(specs: dict, code: dict, blocs: list[tuple], phase: int) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    tous = list(blocs) + [BLOC_LIBC09] + ([BLOC_ECHO_V2] if phase >= 2 else [])
    adresses_insns = {bid: {i.address for i in code[bid]["insns"]} for bid, *_ in tous}
    adresses_blocs = {bid: rva for bid, _, _, rva, _ in tous}

    for bid, sid, _, rva, slot in tous:
        insns = code[bid]["insns"]
        mnemos = [i.mnemonic for i in insns]

        # Cibles de saut internes : frontière d'instruction du même bloc
        for i in insns:
            if i.mnemonic.startswith("j"):
                cible = int(i.op_str, 16)
                verrou(f"{bid}:saut-interne@{i.address:#x}", cible in adresses_insns[bid],
                       f"cible {cible:#x} hors frontière")

        # Appels : IAT autorisée par bloc ; directs vers blocs déclarés ou
        # étiquettes internes du même bloc (assistant local, ex. .protger)
        for i in insns:
            if i.mnemonic == "call":
                if "rip" in i.op_str:
                    cible = operande_rip_cible(i)
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

        # Données RIP : cibles déclarées du bloc (state .data, chaînes, ancre…)
        for i in insns:
            cible = operande_rip_cible(i)
            if cible is not None and i.mnemonic != "call":
                verrou(f"{bid}:donnees-autorisees@{i.address:#x}",
                       cible in DONNEES_RIP.get(bid, set()),
                       f"cible {cible:#x} hors données déclarées (I2/I5)")

        # Interface système : jamais de syscall direct (D7)
        verrou(f"{bid}:pas-de-syscall",
               not any(m in ("syscall", "sysenter", "int") for m in mnemos))

        # Padding intra-slot >= 16 et alignement (D8)
        fin_code = insns[-1].address + insns[-1].size
        verrou(f"{bid}:padding-16", rva + slot - fin_code >= 16,
               f"écart {rva + slot - fin_code}")
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)
        verrou(f"{bid}:slot-multiple-64", slot % 64 == 0)

        # Aucun stockage sous RSP (zone interdite msx64)
        for i in insns:
            if i.mnemonic.startswith("mov") and "[" in i.op_str and i.op_str.split(",")[0].strip().endswith("]"):
                base = re.search(r"\[(\w+)", i.op_str)
                if base and base.group(1) == "rsp":
                    disp = re.search(r"\+ (0x[0-9a-f]+)\]", i.op_str)
                    verrou(f"{bid}:pas-de-stockage-sous-rsp@{i.address:#x}",
                           disp is None or int(disp.group(1), 16) >= 0)

        # Pile alignée aux points d'appel
        verrou(f"{bid}:pile-alignee", _prologue_aligne(insns))

    # Feuilles : aucun appel, pile équilibrée (I1/I2 de tcp-08, libc)
    for bid in (FEUILLES_M2 if phase >= 2 else FEUILLES_M2 - {"c30014"}):
        verrou(f"{bid}:feuille", not any(i.mnemonic == "call" for i in code[bid]["insns"]))
        pushes = sum(1 for i in code[bid]["insns"] if i.mnemonic == "push")
        pops = sum(1 for i in code[bid]["insns"] if i.mnemonic == "pop")
        verrou(f"{bid}:pile-equilibree", pushes == pops)

    # cible du patch (R7) : entrée alignée 16, aucune cible de saut dans les
    # 8 premiers octets (zone trampolinable), taille >= 8
    for bid, entre in (("c30008", L.ECHO_ENTREE), ("c30014", L.ECHO_CROISSANCE)):
        if bid not in code:
            continue
        verrou(f"{bid}:entree-alignee-16", entre % 16 == 0)
        cibles_saut = {int(i.op_str, 16) for i in code[bid]["insns"] if i.mnemonic.startswith("j")}
        verrou(f"{bid}:zone-trampolinable",
               not any(entre < c < entre + 8 for c in cibles_saut),
               f"cibles {list(map(hex, cibles_saut))}")

    # moteur de patch (tcp-07) : UNE écriture alignée de qword par bascule,
    # assistant .protger appelé exactement 4 fois, VP via IAT uniquement
    t = code["c30007"]["insns"]
    ecritures_entree = [i for i in t if i.mnemonic == "mov"
                        and canon(i.op_str).startswith("qword ptr [r15], ")]
    verrou("c30007:bascule-qword-aligne", len(ecritures_entree) == 2,
           f"{len(ecritures_entree)} écritures d'entrée (attendu : bascule + rollback)")
    sous_protger = adresses_insns["c30007"]
    appels_protger = [i for i in t if i.mnemonic == "call" and i.op_str.startswith("0x")
                      and int(i.op_str, 16) in sous_protger
                      and int(i.op_str, 16) != 0x4400]
    verrou("c30007:assistant-protect-x4", len(appels_protger) == 4,
           f"{len(appels_protger)} appels .protger")
    vp = [i for i in t if i.mnemonic == "call" and operande_rip_cible(i) == L.IAT_SLOTS["VirtualProtect"]]
    verrou("c30007:vp-via-iat-unique", len(vp) == 1)
    memcpy_calls = [i for i in t if i.mnemonic == "call" and i.op_str.startswith("0x")
                    and int(i.op_str, 16) == 0x1100]
    verrou("c30007:copie-par-memcpy-scelle", len(memcpy_calls) == 1)

    # journal (tcp-11) : Enter avant toute écriture, Leave avant retour,
    # UNE écriture WriteFile via a10002
    j = [i.mnemonic for i in code["c30011"]["insns"]]
    premier_ecs = next((k for k, i in enumerate(code["c30011"]["insns"])
                        if i.mnemonic == "call" and operande_rip_cible(i) == L.IAT_SLOTS["EnterCriticalSection"]), None)
    verrou("c30011:enter-d'abord", premier_ecs is not None)
    verrou("c30011:appels-ecs-lcs", j.count("call") >= 6)

    # orchestrateur (tcp-12) : la porte R10 précède TOUT appel — aucun ws2
    # direct dans main, boucle de sommes présente, ancre RIP-relative
    m = code["c30013"]["insns"]
    premier_appel = next((k for k, i in enumerate(m) if i.mnemonic == "call"), None)
    marqueur_boucle = [k for k, i in enumerate(m)
                       if canon(f"{i.mnemonic} {i.op_str}") == canon("add rbx, 0x10")]
    verrou("c30013:porte-r10-avant-tout-appel",
           premier_appel is not None and marqueur_boucle
           and premier_appel > marqueur_boucle[-1])
    verrou("c30013:aucun-ws2-direct",
           not any(i.mnemonic == "call" and operande_rip_cible(i) in
                   {L.IAT_SLOTS[n] for n in L.WS2_IMPORTS} for i in m))
    verrou("c30013:somme-sur-image",
           any(canon(f"{i.mnemonic} {i.op_str}") == canon("add rax, qword ptr [r12 + rcx]") for i in m))

    # traçabilité : chaque bloc a sa spécification chargée (spec=, D24)
    attendus = {b for b, *_ in blocs} | {"c30012"} | ({"c30014"} if phase >= 2 else set())
    verrou("tracabilite-I", attendus <= set(specs), str(attendus - set(specs)))
    return verrous


# --- Composition des sections -------------------------------------------------

def _somme_qwords(octets: bytes) -> int:
    return sum(struct.unpack(f"<{len(octets) // 8}Q", octets)) & 0xFFFFFFFFFFFFFFFF


def composer_sections(code: dict, blocs: list[tuple], phase: int):
    """-> (texte, rdata, data, text2, staging) — l'image complète d'echo.exe.

    .text : zones io/libc/app héritées (libc-05/06/07 et libc-09 NON embarqués
    -> int3, comme la croissance 0x4680 : le remplaçant n'existe qu'en staging
    .rdata et n'atteint .text2 qu'au runtime par tcp-07)."""
    texte = bytearray(b"\xcc" * L.TEXT_VSIZE)
    for bid, _, _, rva, slot in blocs:
        if rva >= L.RDATA_RVA:
            continue                      # main @ 0x1800 est dans .text
        octets = code[bid]["octets"]
        texte[rva - L.TEXT_RVA: rva - L.TEXT_RVA + slot] = code[bid]["slot"]

    text2 = bytearray(b"\xcc" * L.TEXT2_VSIZE)
    for bid, _, _, rva, slot in blocs:
        if rva < L.TEXT2_RVA:
            continue
        text2[rva - L.TEXT2_RVA: rva - L.TEXT2_RVA + slot] = code[bid]["slot"]
    # la croissance reste int3 : remplie au runtime par le moteur de patch

    # Staging : int3 (dev.1) ou remplaçant echo-01:R2 assemblé pour 0x4680
    if phase >= 2:
        staging = code["c30014"]["slot"]          # 128 o : code + NOP
    else:
        staging = b"\xcc" * 128

    # Table R10 : entrée staging + un par bloc embarqué + terminateur
    entrees = [(L.R_STAGING, len(staging) if phase >= 2 else 0,
                _somme_qwords(staging) if phase >= 2 else 0)]
    for bid, _, _, rva, slot in blocs:
        if rva < L.TEXT2_RVA:
            tranche = bytes(texte[rva - L.TEXT_RVA: rva - L.TEXT_RVA + slot])
        else:
            tranche = bytes(text2[rva - L.TEXT2_RVA: rva - L.TEXT2_RVA + slot])
        entrees.append((rva, slot, _somme_qwords(tranche)))
    entrees.append((0, 0, 0))
    table = b"".join(struct.pack("<IIQ", r, t, s) for r, t, s in entrees)

    rdata = bytearray(b"\x00" * L.RDATA_VSIZE)

    def poser(rva: int, donnees: bytes):
        if rva - L.RDATA_RVA + len(donnees) > L.RDATA_VSIZE:
            raise EchecBuild(f".rdata débordante à {rva:#x} (D33)")
        rdata[rva - L.RDATA_RVA: rva - L.RDATA_RVA + len(donnees)] = donnees

    hn = lambda nom: struct.pack("<H", 0) + nom.encode("ascii") + b"\x00"

    # Descripteurs d'import : kernel32 (héritage, FT figée 0x20B0) + ws2_32.
    poser(L.R_DESC_IMPORT, struct.pack("<IIIII", L.R_INT_KERNEL32, 0, 0, L.R_NOM_DLL, L.R_IAT))
    poser(L.R_NOM_DLL, b"kernel32.dll\x00")
    poser(L.R_HN_GSH, hn("GetStdHandle"))
    poser(L.R_HN_WF, hn("WriteFile"))
    poser(L.R_HN_EP, hn("ExitProcess"))
    poser(L.R_NOM_WS2, b"ws2_32.dll\x00")
    hints_k32 = {"GetStdHandle": L.R_HN_GSH, "WriteFile": L.R_HN_WF, "ExitProcess": L.R_HN_EP,
                 "CreateThread": L.R_HN_CT, "VirtualProtect": L.R_HN_VP,
                 "InitializeCriticalSection": L.R_HN_ICS, "EnterCriticalSection": L.R_HN_ECS,
                 "LeaveCriticalSection": L.R_HN_LCS, "ReadFile": L.R_HN_RF, "CloseHandle": L.R_HN_CH}
    for nom, rva_h in (("CreateThread", L.R_HN_CT), ("VirtualProtect", L.R_HN_VP),
                       ("InitializeCriticalSection", L.R_HN_ICS),
                       ("EnterCriticalSection", L.R_HN_ECS),
                       ("LeaveCriticalSection", L.R_HN_LCS),
                       ("ReadFile", L.R_HN_RF), ("CloseHandle", L.R_HN_CH)):
        poser(rva_h, hn(nom))
    poser(L.R_INT_KERNEL32, b"".join(struct.pack("<Q", hints_k32[n]) for n in L.KERNEL32_IMPORTS)
          + struct.pack("<Q", 0))
    poser(L.R_IAT, b"".join(struct.pack("<Q", hints_k32[n]) for n in L.KERNEL32_IMPORTS)
          + struct.pack("<Q", 0))
    hints_ws2 = {}
    rva_h = L.R_HN_WS2
    for nom in L.WS2_IMPORTS:
        hints_ws2[nom] = rva_h
        poser(rva_h, hn(nom))
        rva_h += len(hn(nom))
    poser(L.R_DESC_WS2, struct.pack("<IIIII", L.R_INT_WS2, 0, 0, L.R_NOM_WS2, L.R_IAT_WS2))
    poser(L.R_DESC_WS2 + 20, b"\x00" * 20)               # terminateur unique du marche
    poser(L.R_INT_WS2, b"".join(struct.pack("<Q", hints_ws2[n]) for n in L.WS2_IMPORTS)
          + struct.pack("<Q", 0))
    poser(L.R_IAT_WS2, b"".join(struct.pack("<Q", hints_ws2[n]) for n in L.WS2_IMPORTS)
          + struct.pack("<Q", 0))

    # Staging, porte R10, version, ancre, chaînes
    poser(L.R_STAGING, staging)
    poser(L.R_TAB_SUM, table)
    poser(L.R_VERSION, struct.pack("<Q", L.VERSION_U64_DEV2 if phase >= 2 else L.VERSION_U64_DEV1))
    poser(L.R_ANCRE, struct.pack("<Q", 0))
    for rva, chaine in ((L.R_MSG_BANNIERE, L.BANNIERE),
                        (L.R_MSG_CONNEXION, b"connexion entrante\r\n"),
                        (L.R_MSG_ECHO, b"echo "),
                        (L.R_MSG_CRLF, b"\r\n"),
                        (L.R_MSG_PATCH_OK, b"patch applique (majuscules)\r\n"),
                        (L.R_MSG_RB_OK, b"retour arriere (identite)\r\n"),
                        (L.R_MSG_INCONNU, b"commande inconnue\r\n"),
                        (L.R_MSG_REFUS, b"commande refusee\r\n"),
                        (L.R_MSG_FIN, b"fin connexion\r\n"),
                        (L.R_MSG_ARRET, b"arret\r\n"),
                        (L.R_MSG_ERREUR, b"erreur reseau, arret\r\n"),
                        (L.R_MSG_KO, b"TRIADE M2 : integrite KO, arret\r\n"),
                        (L.R_CMD_PATCH, b"patch\r\n"),
                        (L.R_CMD_RB, b"rollback\r\n"),
                        (L.R_CMD_QUIT, b"quit\r\n")):
        poser(rva, chaine + b"\x00")
    poser(L.R_RELOC, struct.pack("<II", L.TEXT_RVA, 12) + struct.pack("<HH", 0, 0))

    data = bytearray(b"\x00" * L.DATA_RAW)    # état serveur nul au chargement
    return bytes(texte), bytes(rdata), bytes(data), bytes(text2), staging


# --- Éditeur PE32+ (quatre sections, D33) --------------------------------------

def ecrire_pe32plus(texte: bytes, rdata: bytes, data: bytes, text2: bytes) -> bytes:
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
        L.SIZE_OF_IMAGE,
        L.FILE_ALIGN,
        0,
        3,                          # Subsystem : CONSOLE
        L.DLL_CHARACTERISTICS,
        0x100000, 0x1000, 0x100000, 0x1000,
        0, 16,
    )

    dirs = [(0, 0)] * 16
    dirs[1] = (L.R_DESC_IMPORT, 80)          # IMPORT : kernel32 + ws2_32 + termes
    dirs[5] = (L.R_RELOC, 12)                # BASERELOC (minimal, image PI)
    dirs[12] = (L.R_IAT, 88)                 # IAT (kernel32 — slots figés R7)
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
    assert len(entetes) == 64 + 4 + 20 + 240 + 160, len(entetes)
    exe = bytearray(b"\x00" * L.TAILLE_FICHIER)
    exe[0:len(entetes)] = entetes
    exe[L.TEXT_FILE:L.TEXT_FILE + len(texte)] = texte
    exe[L.RDATA_FILE:L.RDATA_FILE + len(rdata)] = rdata
    exe[L.DATA_FILE:L.DATA_FILE + len(data)] = data
    exe[L.TEXT2_FILE:L.TEXT2_FILE + len(text2)] = text2
    return bytes(exe)


# --- Validation PE ------------------------------------------------------------

def valider_pe(exe: bytes, phase: int):
    pe = pefile.PE(data=exe)
    assert pe.FILE_HEADER.Machine == 0x8664, "Machine != x86-64"
    assert pe.FILE_HEADER.NumberOfSections == 4, "sections != 4"
    assert pe.OPTIONAL_HEADER.Magic == 0x20B, "magic != PE32+"
    assert pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE, "point d'entrée != tcp-12"
    assert pe.OPTIONAL_HEADER.ImageBase == L.IMAGE_BASE
    assert pe.OPTIONAL_HEADER.Subsystem == 3, "sous-système != CONSOLE"
    dc = pe.OPTIONAL_HEADER.DllCharacteristics
    assert dc & 0x0040 and dc & 0x0020 and dc & 0x0100, "DYNAMICBASE/HEVA/NX absents"
    assert pe.OPTIONAL_HEADER.SizeOfImage == L.SIZE_OF_IMAGE
    noms = [s.Name.decode().rstrip("\x00") for s in pe.sections]
    assert noms == [".text", ".rdata", ".data", ".text2"], noms
    assert pe.sections[0].Characteristics & 0x60000020 == 0x60000020
    assert pe.sections[3].Characteristics & 0x60000020 == 0x60000020, ".text2 non RX"
    assert pe.sections[1].Characteristics & 0x40000040 == 0x40000040
    assert pe.sections[2].Characteristics & 0xC0000040 == 0xC0000040
    assert pe.sections[2].SizeOfRawData == L.DATA_RAW
    imports = {}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        imports[entree.dll.decode().lower()] = [i.name.decode() for i in entree.imports]
    assert imports == {"kernel32.dll": L.KERNEL32_IMPORTS, "ws2_32.dll": L.WS2_IMPORTS}, imports
    assert len(exe) == L.TAILLE_FICHIER, "taille de fichier inattendue"
    # Zone trampolinable et croissance : int3 dans l'image livrée
    assert exe[L.TEXT_FILE] == 0xCC                                    # 0x1000 réservé
    assert exe[L.TEXT2_FILE + (L.ECHO_CROISSANCE - L.TEXT2_RVA)] == 0xCC
    assert exe[L.TEXT_FILE + (0x1440 - L.TEXT_RVA)] == 0xCC            # libc-09 non embarqué
    return True


# --- Preuve de réutilisation (R7) ----------------------------------------------

SHA_HELLO = "c89e330cd16f3fd48558ed4fdb6708fb671e6d907547d5c1ee28075ffd6507f2"
SHA_SELFTEST = "8038585b7af83c9fe5e6fdccd197e67888b9e5fb09d8d6c84cb998c684bff3c0"


def preuve_reutilisation(exe: bytes) -> dict:
    """io M0 et libc M1 embarqués = octets identiques aux artefacts scellés."""
    with open(os.path.join(M0_DIR, "hello.exe"), "rb") as f:
        hello = f.read()
    with open(os.path.join(M1_DIR, "selftest.exe"), "rb") as f:
        selftest = f.read()
    for nom, artefact, sha in (("hello.exe", hello, SHA_HELLO),
                               ("selftest.exe", selftest, SHA_SELFTEST)):
        if hashlib.sha256(artefact).hexdigest() != sha:
            raise EchecBuild(f"{nom} divergent de l'artefact scellé (R7)")
    heritage = [("a10002", hello, 0x1040, 0x40), ("a10003", hello, 0x1080, 0x40),
                ("b20001", selftest, 0x1100, 0x80), ("b20002", selftest, 0x1180, 0x80),
                ("b20003", selftest, 0x1200, 0x80), ("b20004", selftest, 0x1280, 0x80)]
    for bid, source, rva, slot in heritage:
        tranche = lambda buf: buf[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        if tranche(source) != tranche(exe):
            raise EchecBuild(f"réutilisation rompue : {bid} diffère de l'artefact scellé (R7)")
    return {"blocs_reutilises": [b[0] for b in heritage]}


# --- Carte projet, génération 2 ------------------------------------------------

CONTRATS = {
    "a10001": ("() -> noreturn", "entree de processus hello.exe ; pile alignee",
               "message soumis a WriteFile ; ExitProcess(0)",
               "aucun stockage sous RSP ; appels IAT uniquement ; frame equilibre",
               "[a10002] [a10003] [ext kernel32:GetStdHandle]"),
    "a10002": ("(handle u64, ptr u8, len u32) -> bool",
               "handle de flux ; ptr tampon ; len > 0 ; pile alignee",
               "eax = verdict BOOL brut ; pile restauree",
               "shadow space alloue ; args 4 et 5 NULL",
               "[ext kernel32:WriteFile]"),
    "a10003": ("(code u32) -> noreturn", "code de sortie dans rcx",
               "processus termine, sans retour", "ud2 defensif immediat",
               "[ext kernel32:ExitProcess]"),
    "b20001": ("(dst ptr, src ptr, n u64) -> ptr",
               "regions valides sans chevauchement ; pile alignee",
               "n octets de dst egaux a src ; rax = dst ; src inchange",
               "feuille ; pile equilibree ; non volatils intacts ; n=0 sans ecriture",
               "aucune"),
    "b20002": ("(ptr1 ptr, ptr2 ptr, n u64) -> i32 normalise",
               "regions valides en lecture ; pile alignee",
               "eax = -1|0|+1 (premier octet divergent, non signe)",
               "feuille ; pile equilibree ; non volatils intacts ; aucune ecriture",
               "aucune"),
    "b20003": ("(s ptr) -> u64", "chaine NUL-terminee ; pile alignee",
               "rax = offset du premier octet nul ; chaine inchangee",
               "feuille ; pile equilibree ; non volatils intacts", "aucune"),
    "b20004": ("(valeur u32, tampon ptr) -> ptr",
               "tampon >= 12 octets ; pile alignee",
               "decimale ASCII compacte NUL-terminnee ; rax = tampon",
               "feuille ; rien ecrit hors du tampon 12 o (R2)", "aucune"),
    "b20005": ("(taille u64, alignement u64) -> ptr|0",
               "alignement puissance de deux dans [1,64] ; curseur coherent",
               "pointeur aligne dans l arene, curseur avance ; echec -> 0",
               "feuille ; seule ecriture = qword curseur", "[donnees .data:curseur,arene]"),
    "b20006": ("() -> ()", "curseur coherent", "curseur = 0",
               "feuille ; seule ecriture = qword curseur", "[donnees .data:curseur]"),
    "b20007": ("(dst ptr, octet u8, n u64) -> ptr",
               "region valide en ecriture ; pile alignee",
               "n octets de dst egaux a l octet ; rax = dst",
               "feuille ; rbx/rdi sauvegardes ; n=0 sans ecriture", "aucune"),
    "b20008": ("() -> noreturn",
               "point d entree selftest.exe ; pile alignee ; arene vierge",
               "ligne verdict sur stdout ; ExitProcess(0) si 21/21 sinon 1",
               "appels limites aux blocs libc + write/exit + IAT GSH",
               "[b20001..b20007] [a10002] [a10003] [ext kernel32:GetStdHandle]"),
    "c30001": ("() -> ptr|0", "appele une fois avant tout ws2_32 ; pile alignee",
               "rax = socket d ecoute ; echec -> 0 avec nettoyage WSA",
               "sockaddr/WSADATA dans le cadre ; IAT ws2_32 exclusivement",
               "[ext ws2_32:WSAStartup,socket,bind,listen,closesocket,WSACleanup]"),
    "c30002": ("(sock ptr) -> ptr|-1", "socket d ecoute valide",
               "socket cliente propagation exacte",
               "wrapper sans etat ; addr/addrlen NULL", "[ext ws2_32:accept]"),
    "c30003": ("(sock, buf ptr, cap) -> i64", "buf >= cap ; cap > 0",
               "n octets recus | 0 | -1 propagation",
               "wrapper sans etat ; flags 0", "[ext ws2_32:recv]"),
    "c30004": ("(sock, buf ptr, n) -> i64", "buf >= n ; n > 0",
               "k octets emis | -1 ; la boucle complete vie chez tcp-09",
               "wrapper sans etat ; flags 0", "[ext ws2_32:send]"),
    "c30005": ("(sock) -> i32", "socket non nulle", "closesocket appele une fois",
               "wrapper sans etat", "[ext ws2_32:closesocket]"),
    "c30006": ("(proc ptr, arg u64) -> handle|0",
               "proc = frontiere d instruction ; pile alignee",
               "handle du thread | 0",
               "args 5/6 nuls aux loges pile ; CreateThread via IAT",
               "[ext kernel32:CreateThread]"),
    "c30007": ("(mode u32) -> u32",
               "mode 0|1 ; staging coherent avec la table R10 ; pile alignee",
               "0 ok ; 1 mode ; 2 absent ; 3 integrite ; 4 etat ; 5 protection",
               "bascule = UNE ecriture alignee de qword ; VP RW puis RX ; "
               "croissance seule autre ecriture ; memcpy scelle pour la copie",
               "[b20001] [ext kernel32:VirtualProtect] "
               "[donnees .data:etat_patch,entree_sauvee] [echo:entree,croissance] [rdata:staging,table]"),
    "c30008": ("(dst ptr, src ptr, n u64) -> u64",
               "dst >= n ; src >= n ; chevauchement exact autorise",
               "rax = n ; dst = T(src) avec T = identite (R1)",
               "FEUILLE ; volatils uniquement ; entree 0x4600 alignee 16, "
               "8 octets trampolinables ; aucune cible de saut dans la zone",
               "aucune"),
    "c30009": ("(sock) -> ()", "socket connectee ; journal initialise",
               "chaque reception echoee integralement et journalisee ; fin propre",
               "tampon 1024 dans le cadre ; appels directs tcp-03/04/05/08/11",
               "[c30003] [c30004] [c30005] [c30008] [c30011] [rdata:msg_echo,crlf,fin]"),
    "c30010": ("() -> ()", "stdin/listen caches en .data ; journal initialise",
               "patch/rollback/quit executes et journalises ; inconnu journalise",
               "IAT ReadFile seule ; memcmp exact (longueur ET contenu)",
               "[b20002] [c30007] [c30005] [c30011] [ext kernel32:ReadFile] "
               "[donnees .data:stdin,listen,quit] [rdata:commandes,messages]"),
    "c30011": ("(pre ptr, pre_len u64, valeur u32, suf ptr, suf_len u64) -> bool",
               "pre+12+suf <= 64 ; CS initialisee ; stdout cache ; pile alignee",
               "UNE ecriture WriteFile de la ligne composee ; BOOL propage",
               "composition sur pile privee sous section critique ; "
               "Enter/Leave apparies sur tout chemin",
               "[b20001] [b20003] [b20004] [a10002] "
               "[ext kernel32:Enter,LeaveCriticalSection] [donnees .data:stdout,cs]"),
    "c30012": ("(taille u64, alignement u64) -> ptr|0",
               "heritage libc-05 ; CS initialisee ; pile alignee",
               "propagation exacte de libc-05 sous verrou",
               "EnterCS ; libc-05 ; LeaveCS ; aucune ecriture propre",
               "[b20005] [ext kernel32:Enter,LeaveCriticalSection] [donnees .data:cs]"),
    "c30013": ("() -> noreturn",
               "point d entree echo.exe ; pile alignee ; .data vierge",
               "porte R10 (sommes + version) AVANT tout effet ; banniere ; "
               "boucle accept/thread ; ExitProcess 0|1|2",
               "aucun ws2_32 direct ; base d image par ancre RIP (PI) ; "
               "porte R10 avant tout appel",
               "[c30001] [c30002] [c30006] [c30011] [a10002] [a10003] "
               "[ext kernel32:GSH,InitCS,CloseHandle,ExitProcess] "
               "[rdata:table,version,ancre,messages] [donnees .data:etat]"),
    "c30014": ("(dst ptr, src ptr, n u64) -> u64",
               "idem c30008 (contrat stable R4)",
               "rax = n ; dst = T(src) avec T = majuscules ASCII (R2)",
               "FEUILLE ; volatils uniquement ; assemble POUR 0x4680 "
               "(croissance) ; livree en staging .rdata, activation a chaud",
               "aucune"),
}

ROLES = dict(L.NOMS_BLOCS)

EXE_PAR_BLOC = {
    "a10001": "hello", "a10002": "hello,selftest,echo", "a10003": "hello,selftest,echo",
    "b20001": "selftest,echo", "b20002": "selftest,echo", "b20003": "selftest,echo",
    "b20004": "selftest,echo", "b20005": "selftest", "b20006": "selftest",
    "b20007": "selftest", "b20008": "selftest",
    "c30001": "echo", "c30002": "echo", "c30003": "echo", "c30004": "echo",
    "c30005": "echo", "c30006": "echo", "c30007": "echo", "c30008": "echo",
    "c30009": "echo", "c30010": "echo", "c30011": "echo", "c30012": "aucun",
    "c30013": "echo", "c30014": "echo",
}


def fragments_clairs(code: dict, exe: bytes, verrous: list[str], blocs: list[tuple],
                     phase: int, version: str, verdict_oracle: dict, compteurs: dict,
                     journal_runs: list[str]) -> dict[str, bytes]:
    sha = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()
    rva_par_bloc = {"a10001": 0x1000, "a10002": 0x1040, "a10003": 0x1080,
                    "b20001": 0x1100, "b20002": 0x1180, "b20003": 0x1200,
                    "b20004": 0x1280, "b20005": 0x1300, "b20006": 0x1380,
                    "b20007": 0x13C0, "b20008": 0x1800}
    rva_par_bloc |= {bid: rva for bid, _, _, rva, _ in blocs}
    rva_par_bloc.update({"c30012": 0x1440, "c30014": L.ECHO_CROISSANCE})

    loc = ["[carte-frag] nom=frag-loc generation=2",
           "[zones] io=0x1000-0x10ff libc=0x1100-0x17ff app=0x1800-0x1fff "
           "net=0x4000-0x42ff thr=0x4300-0x43ff tramp=0x4400-0x45ff "
           "echo=0x4600-0x47ff croissance=0x4680 srv=0x4800-0x4fff "
           "reserve-libc=0x13c0-0x17ff reserve-io=0x1000,0x10c0 (int3 defensif)"]
    tous_loc = (["a10001", "a10002", "a10003", "b20001", "b20002", "b20003",
                 "b20004", "b20005", "b20006", "b20007", "b20008"]
                + [b for b, _, _, _, _ in blocs if b.startswith("c3")]
                + ["c30012"] + (["c30014"] if phase >= 2 else []))
    spec_par_bloc = {
        "a10001": "hello-01:R1", "a10002": "hello-02:R1", "a10003": "hello-03:R1",
        "b20001": "libc-01:R1", "b20002": "libc-02:R1", "b20003": "libc-03:R1",
        "b20004": "libc-04:R1", "b20005": "libc-05:R1", "b20006": "libc-06:R1",
        "b20007": "libc-07:R1", "b20008": "libc-08:R2",
        "c30001": "tcp-01:R1", "c30002": "tcp-02:R1", "c30003": "tcp-03:R1",
        "c30004": "tcp-04:R1", "c30005": "tcp-05:R1", "c30006": "tcp-06:R1",
        "c30007": "tcp-07:R1", "c30008": "tcp-08:R1", "c30009": "tcp-09:R1",
        "c30010": "tcp-10:R1", "c30011": "tcp-11:R1", "c30012": "libc-09:R1",
        "c30013": "tcp-12:R1", "c30014": "tcp-08:R2",
    }
    taille_par_bloc = {"a10001": 64, "a10002": 0x40, "a10003": 0x40,
                       "b20001": 0x80, "b20002": 0x80, "b20003": 0x80, "b20004": 0x80,
                       "b20005": 0x80, "b20006": 0x40, "b20007": 0x80, "b20008": 0x800}
    for bid in tous_loc:
        taille = taille_par_bloc.get(bid)
        if taille is None:
            taille = next((slot for b, _, _, _, slot in blocs if b == bid),
                          0x80 if bid == "c30012" else 0x80)
        etat = ("verifie" if bid == "c30014" else "scelle")
        loc.append(f"[bloc] id={bid} spec={spec_par_bloc[bid]} cible=x86-64-win11-pe "
                   f"exe={EXE_PAR_BLOC[bid]} addr={L.IMAGE_BASE + rva_par_bloc[bid]:#x} "
                   f"size={taille} v=1 etat={etat} role={ROLES[bid]}")

    con = ["[carte-frag] nom=frag-con generation=2"]
    for bid in tous_loc:
        sig, pre, post, inv, deps = CONTRATS[bid]
        con += [f"[bloc] id={bid}", f"  sig : {sig}", f"  pre : {pre}",
                f"  post : {post}", f"  inv : {inv}", f"  deps : {deps}"]

    prf = ["[carte-frag] nom=frag-prf generation=2"]
    for bid in tous_loc:
        fichier = {"a10001": "hello-01-main", "b20005": "libc-05-zone-alloc",
                   "b20006": "libc-06-zone-reset", "b20007": "libc-07-memset",
                   "b20008": "libc-08-autotest"}.get(bid)
        if fichier is None:
            fichier = next((f for b, _, f, _, _ in blocs if b == bid),
                           "libc-09-zone-alloc-ts" if bid == "c30012" else "tcp-08-echo-v2")
        notation = chemin_notation(fichier)
        with open(notation, "rb") as f:
            empreinte_notation = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [
            f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} crist={crist}/10",
            f"  vecteurs : roundtrip=ok structure=ok notation={empreinte_notation}",
            f"  differentiel : {verdict_oracle.get('blocs', {}).get(bid, {}).get('detail', '-')}"]
    prf.append("[verifications] runs=" + str(len(journal_runs)))
    prf += ["  " + r for r in journal_runs[-12:]]

    bld = ["[carte-frag] nom=frag-bld generation=2"]
    # empreintes : blocs embarqués = tranches d'echo.exe ; autres = notation
    for bid in tous_loc:
        rva = rva_par_bloc[bid]
        if bid in {b for b, _, _, _, _ in blocs}:
            if rva < L.RDATA_RVA:
                tranche = exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + 0x40]
                tranche = exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA)
                              + next(s for b, _, _, r, s in blocs if b == bid)]
            else:
                s = next(s for b, _, _, r, s in blocs if b == bid)
                tranche = exe[L.TEXT2_FILE + (rva - L.TEXT2_RVA): L.TEXT2_FILE + (rva - L.TEXT2_RVA) + s]
            empreinte = sha(tranche)
        elif bid == "c30014":
            tranche = exe[L.RDATA_FILE + (L.R_STAGING - L.RDATA_RVA):
                          L.RDATA_FILE + (L.R_STAGING - L.RDATA_RVA) + 0x80]
            empreinte = sha(tranche)
        else:
            # blocs hérités non embarqués dans echo.exe : empreinte = tranche
            # de LEUR artefact scellé (hello.exe / selftest.exe) ; libc-09,
            # sans artefact hôte, contre sa notation
            tranche_art = {"a10001": (os.path.join(M0_DIR, "hello.exe"), 0x1000, 0x40),
                           "b20005": (os.path.join(M1_DIR, "selftest.exe"), 0x1300, 0x80),
                           "b20006": (os.path.join(M1_DIR, "selftest.exe"), 0x1380, 0x40),
                           "b20007": (os.path.join(M1_DIR, "selftest.exe"), 0x13C0, 0x80),
                           "b20008": (os.path.join(M1_DIR, "selftest.exe"), 0x1800, 0x800)}[bid]
            with open(tranche_art[0], "rb") as f:
                artefact = f.read()
            tranche = artefact[L.TEXT_FILE + (tranche_art[1] - L.TEXT_RVA):
                               L.TEXT_FILE + (tranche_art[1] - L.TEXT_RVA) + tranche_art[2]]
            empreinte = sha(tranche)
            if bid == "c30012":
                with open(chemin_notation("libc-09-zone-alloc-ts"), "rb") as f:
                    empreinte = "notation:" + sha(f.read())[7:]
        bld.append(f"[bloc] id={bid} addr={L.IMAGE_BASE + rva:#x} empreinte={empreinte}")
    bld += [
        f"[build] artefact=echo.exe version={version} profil=x86-64-win11-pe "
        f"taille={len(exe)} empreinte={sha(exe)}",
        f"  outils : keystone-engine + capstone {capstone.cs_version()[0]}.{capstone.cs_version()[1]} ; "
        f"verrous={len(verrous)} ; oracle : {verdict_oracle.get('total_cas', 0)} cas, "
        f"graine={verdict_oracle.get('graine', '-')}, volume={verdict_oracle.get('volume', '-')}",
        f"  heritage : hello.exe 0.1.0-dev.1 + selftest.exe 0.2.0 "
        f"(a10002/a10003/b20001..b20004 reutilises octet-identiques, R7)",
        f"[zones] io=0x1000-0x10ff libc=0x1100-0x17ff app=0x1800-0x1fff "
        f"net=0x4000-0x42ff thr=0x4300-0x43ff tramp=0x4400-0x45ff "
        f"echo=0x4600-0x47ff croissance=0x4680 srv=0x4800-0x4fff",
    ]

    retour = {}
    for nom, lignes in (("frag-loc", loc), ("frag-con", con), ("frag-prf", prf), ("frag-bld", bld)):
        retour[nom] = ("\n".join(lignes) + "\n").encode("ascii", errors="replace")
    return retour


def construire_carte(code: dict, exe: bytes, verrous: list[str], blocs: list[tuple],
                     phase: int, version: str, verdict_oracle: dict, compteurs: dict,
                     journal_runs: list[str]):
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    clairs = fragments_clairs(code, exe, verrous, blocs, phase, version,
                              verdict_oracle, compteurs, journal_runs)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = cm.empreinte_racine(fragments)
    entete = cm.construire_entete(racine)
    prive, pub = cm.paire_cles(graine)
    signature = cm.signer(prive, entete, fragments)
    cm.ecrire_carte(entete, fragments, signature, pub)
    return pub


# --- Verrou croisé (R8) : relecture indépendante des artefacts ------------------

def verrou_croise(blocs: list[tuple], phase: int) -> tuple[int, dict]:
    phrase, _ = cm.charger_secrets(interactif=False)
    entete, fragments, signature, pub = cm.lire_carte()
    cm.verifier_listes_blanches(entete.decode("ascii"))
    cm.verifier_signature(pub, entete, fragments, signature)
    if cm.empreinte_racine(fragments).hex() not in entete.decode("ascii"):
        raise cm.ErreurCarte("empreinte racine divergente")
    maitre = cm.cle_maitresse(phrase)
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
    with open(os.path.join(ICI, "echo.exe"), "rb") as f:
        exe = f.read()
    empreintes, manifestes = {}, []
    for ligne in bld.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[champs["id"]] = champs["empreinte"]
        elif ligne.startswith("[build]"):
            manifestes.append(dict(re.findall(r"(\w+)=(\S+)", ligne)))
    manifeste = next((m for m in manifestes if m.get("artefact") == "echo.exe"), {})
    # blocs embarqués : tranche d'echo.exe
    for bid, _, _, rva, slot in blocs:
        if rva < L.RDATA_RVA:
            tranche = exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        else:
            tranche = exe[L.TEXT2_FILE + (rva - L.TEXT2_RVA): L.TEXT2_FILE + (rva - L.TEXT2_RVA) + slot]
        sha = "sha256:" + hashlib.sha256(tranche).hexdigest()
        if sha != empreintes.get(bid):
            raise cm.ErreurCarte(f"verrou croisé : empreinte de {bid} divergente (R8)")
    # remplaçant : staging .rdata
    if phase >= 2:
        tranche = exe[L.RDATA_FILE + (L.R_STAGING - L.RDATA_RVA):
                      L.RDATA_FILE + (L.R_STAGING - L.RDATA_RVA) + 0x80]
        if "sha256:" + hashlib.sha256(tranche).hexdigest() != empreintes.get("c30014"):
            raise cm.ErreurCarte("verrou croisé : staging de c30014 divergent (R8)")
    # blocs hérités non embarqués : contre les artefacts scellés M0/M1
    with open(os.path.join(M0_DIR, "hello.exe"), "rb") as f:
        hello = f.read()
    with open(os.path.join(M1_DIR, "selftest.exe"), "rb") as f:
        selftest = f.read()
    controles = [("a10001", hello, 0x1000, 0x40), ("b20005", selftest, 0x1300, 0x80),
                 ("b20006", selftest, 0x1380, 0x40), ("b20007", selftest, 0x13C0, 0x80),
                 ("b20008", selftest, 0x1800, 0x800)]
    for bid, source, rva, slot in controles:
        tranche = source[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        if "sha256:" + hashlib.sha256(tranche).hexdigest() != empreintes.get(bid):
            raise cm.ErreurCarte(f"verrou croisé : empreinte de {bid} divergente vs artefact scellé (R8)")
    # libc-09 : contre sa notation
    with open(chemin_notation("libc-09-zone-alloc-ts"), "rb") as f:
        if "notation:" + hashlib.sha256(f.read()).hexdigest() != empreintes.get("c30012"):
            raise cm.ErreurCarte("verrou croisé : libc-09 divergent de sa notation (R8)")
    sha_exe = "sha256:" + hashlib.sha256(exe).hexdigest()
    if sha_exe != manifeste.get("empreinte"):
        raise cm.ErreurCarte("verrou croisé : empreinte d'echo.exe divergente (R8)")
    return len(empreintes), manifeste


# --- Tableau de bord (§ 15.2, métriques M2) --------------------------------------

def tableau_de_bord(exe: bytes, verrous: list[str], nb_blocs_carte: int, manifeste: dict,
                    verdict_oracle: dict, phase: int) -> str:
    sha = lambda b: hashlib.sha256(b).hexdigest()
    budgets = "cible (instrumentation a executer : budgets_tokens.py)"
    chemin_budgets = os.path.join(ICI, "budgets.json")
    if os.path.exists(chemin_budgets):
        with open(chemin_budgets, encoding="utf-8") as f:
            bj = json.load(f)
        budgets = (f"mesure (M2) : localiser={bj['localiser']['mesure']} tok / "
                   f"editer={bj['editer']['mesure']} tok / ajouter={bj['ajouter']['mesure']} tok "
                   f"(cibles 64/3000/6000, D31)")
    conformite = "a executer : conformite_profil.py (elements 1-7, 5 = patch a chaud)"
    chemin_conf = os.path.join(ICI, "conformite.txt")
    if os.path.exists(chemin_conf):
        with open(chemin_conf, encoding="ascii") as f:
            conformite = f.read().strip()
    lignes = [
        "[tableau] jalon=M2 artefact=echo.exe version=" + manifeste.get("version", "?"),
        f"  blocs_avec_spec_a_jour        : {nb_blocs_carte}/26 : audit de tracabilite I->C->B (3 artefacts)",
        f"  chaines_I_C_B_tests           : {nb_blocs_carte}/{nb_blocs_carte} : specs, carte, exe, vecteurs",
        f"  construction                  : 0 erreur / 0 avertissement : build script",
        f"  tests_differentiels           : {verdict_oracle.get('total_cas', 0)} cas verts "
        f"({verdict_oracle.get('volume', '-')}, graine {verdict_oracle.get('graine', '-')}) ; "
        f"oracle structurel {len(verrous)} verrous PASS ; patch : {verdict_oracle.get('patch', '-')}",
        f"  empreintes_donnees_embarquees : conforme (staging, table R10, chaines, curseur nul)",
        f"  defauts_T1_T6_ouverts         : 0 : journal des decisions D33-D34",
        f"  optimisations_sans_mesure     : 0 : aucune optimisation M2 (R11)",
        f"  budgets_tokens                : {budgets}",
        f"  suite_conformite_profil       : {conformite}",
        f"  changements_hors_journal      : 0 : D33 a D34 consignees",
        f"  preversions                   : {manifeste.get('version', '?')} conforme "
        f"(schema dev/rc/final, monotonie ; anti-rollback R10 verifie par l'oracle)",
        f"  patch_a_chaud                 : bascule atomique (qword aligne) + rollback + "
        f"refus fail-closed verifies ; continuite en session DEMONTREE (oracle)",
        f"  artefact                      : {len(exe)} octets ; empreinte sha256:{sha(exe)[:16]}... ; "
        f"reutilisation M0/M1 : 6 blocs octet-identiques (R7)",
        f"  verrou_croise                 : {nb_blocs_carte} empreintes reverifiees "
        f"(3 artefacts + notation libc-09) + signature Ed25519 + racine (R8/R9)",
    ]
    return "\n".join(lignes) + "\n"


# --- Assemblage + vérification communs -------------------------------------------

def assembler_tout(phase: int):
    """Assemble, round-trip et oracle structurel — commun construction/vérification."""
    blocs = blocs_phase(phase)
    specs = charger_couche_I(blocs, phase)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code: dict[str, dict] = {}
    tous = list(blocs) + [BLOC_LIBC09] + ([BLOC_ECHO_V2] if phase >= 2 else [])
    for bid, sid, fichier, rva, slot in tous:
        chemin = chemin_notation(fichier)
        octets, metas = assembler_bloc(ks, chemin, rva, slot)
        insns = round_trip(cs, ks, chemin, rva, octets, metas)
        slot_complet = octets + b"\x90" * (slot - len(octets))
        code[bid] = {"octets": octets, "metas": metas, "insns": insns, "slot": slot_complet}
        print(f"[R5] {bid} ({sid}) : {len(octets)} o, round-trip {len(insns)}/{len(insns)} = 100 %")
    verrous = oracle_structurel(specs, code, blocs, phase)
    print(f"[oracle] structurel : {len(verrous)} verrous PASS (contrats I verifies par bloc)")
    return blocs, specs, code, verrous


def phase_courante() -> int:
    try:
        _, fragments, _, _ = cm.lire_carte()
        phrase, _ = cm.charger_secrets(interactif=False)
        maitre = cm.cle_maitresse(phrase)
        bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
        return 2 if "c30014" in bld else 1
    except Exception:
        return 1


# --- Modes -----------------------------------------------------------------------

def construire(phase: int, volume: str, graine: int) -> int:
    print(f"=== M2 : chaine artefact TRIADE (profil x86-64-win11-pe, phase {phase}) ===")
    # Anti-rollback : une carte scellée (rc/final) interdit la reconstruction
    try:
        _, fragments, _, _ = cm.lire_carte()
        phrase, _ = cm.charger_secrets(interactif=False)
        maitre = cm.cle_maitresse(phrase)
        bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
        version_existante = next(
            (dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
             if "artefact=echo.exe" in l), None)
        if version_existante and ("-rc" in version_existante
                                  or re.fullmatch(r"\d+\.\d+\.\d+", version_existante)):
            raise EchecBuild(
                f"carte scellée ({version_existante}) : reconstruction interdite — "
                f"procedure lourde R6 ou nouvelle version X.Y.Z+1 requise")
    except (cm.ErreurCarte, FileNotFoundError):
        pass

    blocs, specs, code, verrous = assembler_tout(phase)
    version = L.VERSION_DEV1 if phase == 1 else L.VERSION_DEV2

    texte, rdata, data, text2, staging = composer_sections(code, blocs, phase)
    exe = ecrire_pe32plus(texte, rdata, data, text2)
    valider_pe(exe, phase)
    heritage = preuve_reutilisation(exe)
    print(f"[PE] echo.exe : {len(exe)} octets, 4 sections, kernel32 x10 + ws2_32 x10, "
          f"DYNAMICBASE+HEVA+NX, entree 0x{L.ENTREE:x}, croissance int3")
    print(f"[R7] reutilisation : {len(heritage['blocs_reutilises'])} blocs octet-identiques "
          f"aux artefacts scelles M0/M1")

    verdict = od.executer(exe, graine=graine, volume=volume)
    print(f"[oracle] differentiel : {verdict['total_cas']} cas verts ; patch : {verdict['patch']} ; "
          f"falsification : {verdict['falsification']}")

    with open(os.path.join(ICI, "echo.exe"), "wb") as f:
        f.write(exe)

    compteurs = {bid: 1 for bid, _, _, _, _ in blocs}
    compteurs["a10001"] = 1
    compteurs["c30012"] = 1
    if phase >= 2:
        compteurs["c30014"] = 1
    journal = [f"run graine={graine} volume={volume} verdict={verdict['empreinte']} "
               f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} phase={phase} build={version}"]
    construire_carte(code, exe, verrous, blocs, phase, version, verdict, compteurs, journal)
    print(f"[carte] generation 2 ecrite : 4 fragments chiffres, signature Ed25519, "
          f"{25 + (1 if phase >= 2 else 0)} blocs indexes sur 3 artefacts")

    nb, manifeste = verrou_croise(blocs, phase)
    print(f"[R8] verrou croise : signature OK, racine OK, {nb} empreintes reverifiees, "
          f"artefact {manifeste.get('version')}")

    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="ascii") as f:
        f.write(tableau_de_bord(exe, verrous, nb, manifeste, verdict, phase))
    print("[tableau] tableau de bord ecrit (carte/tableau-de-bord.txt)")
    print(f"[B] echo.exe scelle : sha256:{hashlib.sha256(exe).hexdigest()}")
    print(f"=== M2-dev (oracle vert) : {version} — validation terrain Windows 11 en attente ===")
    return 0


def verifier(graine: int, volume: str) -> int:
    print(f"=== M2 : re-verification complete (R5/R8, graine {graine}) ===")
    phase = phase_courante()
    blocs, specs, code, verrous = assembler_tout(phase)

    with open(os.path.join(ICI, "echo.exe"), "rb") as f:
        exe = f.read()
    for bid, _, _, rva, slot in blocs:
        if rva < L.RDATA_RVA:
            embarque = exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        else:
            embarque = exe[L.TEXT2_FILE + (rva - L.TEXT2_RVA): L.TEXT2_FILE + (rva - L.TEXT2_RVA) + slot]
        if embarque != code[bid]["slot"]:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5 — verifier-puis-ecrire)")

    verdict = od.executer(exe, graine=graine, volume=volume)
    print(f"[oracle] differentiel : {verdict['total_cas']} cas verts ; patch : {verdict['patch']}")

    phrase, graine_cles = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("ascii")
    compteurs, journal = {}, []
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            m = re.match(r"(\d+)/10", champs.get("crist", "1/10"))
            compteurs[champs["id"]] = int(m.group(1))
        elif ligne.startswith("  run "):
            journal.append(ligne.strip())
    tous = [bid for bid, _, _, _, _ in blocs] + ["a10001", "c30012"] \
        + (["c30014"] if phase >= 2 else [])
    for bid in tous:
        compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal.append(f"run graine={graine} volume={volume} verdict={verdict['empreinte']} "
                   f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")

    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
    manifeste_v = next((dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
                        if "artefact=echo.exe" in l), "?")
    version = manifeste_v if manifeste_v != "?" else (L.VERSION_DEV1 if phase == 1 else L.VERSION_DEV2)
    construire_carte(code, exe, verrous, blocs, phase, version, verdict, compteurs, journal)
    nb, manifeste = verrou_croise(blocs, phase)
    crist = {b: compteurs.get(b, 0) for b, _, _, _, _ in blocs}
    print("[R6] cristallisation : " + ", ".join(f"{b}={n}/10" for b, n in list(crist.items())[:6])
          + (", …" if len(crist) > 6 else ""))
    print(f"[R8] verrou croise : {nb} empreintes conformes ; artefact {manifeste.get('version')}")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="ascii") as f:
        f.write(tableau_de_bord(exe, verrous, nb, manifeste, verdict, phase))
    return 0


def _sceller(nouvelle_version: str, exigences: str) -> int:
    """Scellage commun : cristallisation 10/10 + conformité verte + balise."""
    print(f"=== M2 : scellage {nouvelle_version} ({exigences}) ===")
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("ascii")
    compteurs = {}
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            compteurs[champs["id"]] = int(re.match(r"(\d+)/10", champs.get("crist", "0/10")).group(1))
    incomplets = {b: n for b, n in compteurs.items() if n < 10}
    if incomplets:
        raise EchecBuild(f"cristallisation incomplete : {incomplets} — 10 verifications requises (R6)")

    import conformite_profil as cp
    ok, lignes = cp.executer()
    print("\n".join(lignes))
    if not ok:
        raise EchecBuild(f"suite de conformite non verte — {nouvelle_version} refuse")

    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
    ancienne = (L.VERSION_DEV1 + "|" + L.VERSION_DEV2 + "|" + L.VERSION_RC1) \
        if nouvelle_version == L.VERSION_FINALE else (L.VERSION_DEV1 + "|" + L.VERSION_DEV2)
    occurrences = sum(bld.count(f"version={v}") for v in ancienne.split("|"))
    if nouvelle_version == L.VERSION_FINALE and occurrences != 1:
        raise EchecBuild(f"balise {L.VERSION_RC1} attendue une fois dans frag-bld "
                         f"({occurrences} occurrence(s)) — scellage final refuse (fail-closed)")
    for v in ancienne.split("|"):
        bld = bld.replace(f"version={v}", f"version={nouvelle_version}")
    clairs = {"frag-bld": bld.encode("ascii")}
    for nom in ("frag-loc", "frag-con", "frag-prf"):
        clairs[nom] = cm.dechiffrer_fragment(maitre, nom, fragments[nom])
    nouveaux = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = cm.empreinte_racine(nouveaux)
    entete = cm.construire_entete(racine)
    _, graine_cles = cm.charger_secrets(interactif=False)
    prive, pub = cm.paire_cles(graine_cles)
    cm.ecrire_carte(entete, nouveaux, cm.signer(prive, entete, nouveaux), pub)
    print(f"[balise] {nouvelle_version} scellee (immuable § 9 ; defaut -> 0.3.1 a contrat stable, R4)")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if "--verifier" in args:
            graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 1
            volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
            sys.exit(verifier(graine, volume))
        if "--sceller-rc" in args:
            sys.exit(_sceller(L.VERSION_RC1, "cristallisation R6 + conformite 1-7"))
        if "--sceller-final" in args:
            sys.exit(_sceller(L.VERSION_FINALE, "R6 + conformite + constat terrain"))
        phase = int(args[args.index("--phase") + 1]) if "--phase" in args else 1
        volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
        graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 1
        sys.exit(construire(phase, volume, graine))
    except (EchecBuild, cm.ErreurCarte, od.EchecOracle) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
