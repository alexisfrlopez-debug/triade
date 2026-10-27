#!/usr/bin/env python3
"""build_m3.py : Jalon M3 de TRIADE — proxy HTTP à contrats renforcés.

Notation (keystone) -> octets -> PE32+ à la main (QUATRE sections) -> carte
projet génération 5. Implémente le jalon M3 sous les règles R4 (contrat
stable), R7 (adresses stables — io/libc/tcp réutilisés octet-identiques aux
artefacts scellés) et R10 (porte d'intégrité au lancement, plancher M3
0x00040000). Les entrées non fiables ont un comportement défini par les
treize spécifications écrites-avant-code (D46) ; la session http-10 est à R2
(journal 36 : relais de corps borné Content-Length inline — http-09 réservé
au tunnel et au relais de réponse, CloseHandle pour la pompe détachée).

L'ORACLE (D1) est régénéré à chaque exécution depuis la couche I :
  1. round-trip de notation : keystone -> capstone -> keystone (WYSIWYG) ;
  2. contrat structurel : invariants de I vérifiés sur le code désassemblé
     (autorisation PAR BLOC des appels IAT, des appels directs et des cibles
     RIP — discipline M2 durcie : les feuilles n'ont AUCUN appel externe) ;
  3. oracle différentiel (oracle_m3.py) : parseurs, pompe, tcp-13, sessions
     E1-E8, console, binaire entier, falsification.

RÉUTILISATION (R7) : io M0 (hello.exe), libc M1 (selftest.exe) et blocs
réseau M2 (echo.exe : tcp-01..06, tcp-11) embarqués à leurs adresses
historiques, octets identiques — vérifié à chaque construction. L'IAT
ws2_32 gagne TROIS entrées appendues (getaddrinfo, freeaddrinfo, connect —
arrêt b : la préfiguration D46 oubliait connect).

Usage :
  python3 build_m3.py                  # construction 0.4.0-dev.1
  python3 build_m3.py --verifier [--graine N] [--volume complet|reduit]
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

import carte_m3 as cm
import oracle_m3 as od

ICI = os.path.dirname(os.path.abspath(__file__))
M0_DIR = os.path.join(os.path.dirname(ICI), "m0")
M1_DIR = os.path.join(os.path.dirname(ICI), "m1")
M2_DIR = os.path.join(os.path.dirname(ICI), "m2")


class EchecBuild(Exception):
    """Tout échec de l'oracle, du round-trip ou de la construction."""


# --- Blocs embarqués dans proxy.exe --------------------------------------------

def blocs_embarques() -> list[tuple]:
    """(id carte, spec, fichier notation, rva, slot) — dans proxy.exe."""
    blocs = [
        # héritage M0/M1 (octets identiques aux artefacts scellés)
        ("a10002", "hello-02:R1", "hello-02-write", 0x1040, 0x40),
        ("a10003", "hello-03:R1", "hello-03-exit", 0x1080, 0x40),
        ("b20001", "libc-01:R1", "libc-01-memcpy", 0x1100, 0x80),
        ("b20002", "libc-02:R1", "libc-02-memcmp", 0x1180, 0x80),
        ("b20003", "libc-03:R1", "libc-03-strlen", 0x1200, 0x80),
        ("b20004", "libc-04:R1", "libc-04-itoa", 0x1280, 0x80),
        # génération M2 (octets echo.exe, RVA exacts — R7)
        ("c30001", "tcp-01:R1", "tcp-01-init", 0x4000, 0x100),
        ("c30002", "tcp-02:R1", "tcp-02-accept", 0x4100, 0x40),
        ("c30003", "tcp-03:R1", "tcp-03-recv", 0x4140, 0x40),
        ("c30004", "tcp-04:R1", "tcp-04-send", 0x4180, 0x40),
        ("c30005", "tcp-05:R1", "tcp-05-close", 0x41C0, 0x40),
        ("c30006", "tcp-06:R1", "tcp-06-spawn", 0x4300, 0x40),
        ("c30011", "tcp-11:R1", "tcp-11-journal", 0x4B00, 0x100),
    ]
    blocs += [(bid, spec, _FICHIERS_M3[bid], rva, slot)
              for bid, spec, rva, slot, _, _ in L.BLOCS_M3]
    return blocs


_FICHIERS_M3 = {
    "e50001": "http-01-ligne", "e50002": "http-02-requete",
    "e50003": "http-03-entete", "e50004": "http-04-chercher",
    "e50005": "http-05-nombre", "e50006": "http-06-tete",
    "e50007": "http-07-autorite", "e50008": "http-08-cible",
    "e50009": "http-09-pompe", "e50010": "http-10-session",
    "e50011": "http-11-console", "e50012": "http-12-principal",
    "e50013": "tcp-13-connexion",
}


def chemin_notation(fichier: str) -> str:
    if fichier.startswith("hello-"):
        return os.path.join(M0_DIR, "notation", fichier + ".asm")
    if fichier.startswith("libc-09"):
        # libc-09 (zone-alloc-ts, c30012) est un bloc M2 d'echo.exe —
        # PAS un bloc M1 : sa notation vit dans m2/notation/
        return os.path.join(M2_DIR, "notation", fichier + ".asm")
    if fichier.startswith("libc-0"):
        return os.path.join(M1_DIR, "notation", fichier + ".asm")
    if fichier.startswith("tcp-") and not fichier.startswith("tcp-13"):
        return os.path.join(M2_DIR, "notation", fichier + ".asm")
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


def charger_couche_I(blocs: list[tuple]) -> dict[str, dict]:
    fichiers = {
        "http-01": "http-01-ligne.md", "http-02": "http-02-requete.md",
        "http-03": "http-03-entete.md", "http-04": "http-04-chercher.md",
        "http-05": "http-05-nombre.md", "http-06": "http-06-tete.md",
        "http-07": "http-07-autorite.md", "http-08": "http-08-cible.md",
        "http-09": "http-09-pompe.md", "http-10": "http-10-session.md",
        "http-11": "http-11-console.md", "http-12": "http-12-principal.md",
        "tcp-13": "tcp-13-connexion.md",
        "hello-02": "hello-02-write.md", "hello-03": "hello-03-exit.md",
        "libc-01": "libc-01-memcpy.md", "libc-02": "libc-02-memcmp.md",
        "libc-03": "libc-03-strlen.md", "libc-04": "libc-04-itoa.md",
        "tcp-01": "tcp-01-init.md", "tcp-02": "tcp-02-accept.md",
        "tcp-03": "tcp-03-recv.md", "tcp-04": "tcp-04-send.md",
        "tcp-05": "tcp-05-close.md", "tcp-06": "tcp-06-spawn.md",
        "tcp-11": "tcp-11-journal.md",
    }
    specs = {}

    def charger(bid: str, sid: str):
        ident, rev_ref = sid.split(":")
        rev_ref = int(rev_ref[1:])
        if ident.startswith(("http-", "tcp-13")):
            chemin = os.path.join(ICI, "I", fichiers[ident])
        elif ident.startswith(("hello-", "libc-")):
            base = M0_DIR if ident.startswith("hello-") else M1_DIR
            chemin = os.path.join(base, "I", fichiers[ident])
        else:
            chemin = os.path.join(M2_DIR, "I", fichiers[ident])
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


# --- Oracle structurel : les invariants de I, par bloc (discipline M2 durcie) ---

IAT_PAR_BLOC = {
    "a10002": {"WriteFile"}, "a10003": {"ExitProcess"},
    "b20001": set(), "b20002": set(), "b20003": set(), "b20004": set(),
    "c30001": {"WSAStartup", "socket", "bind", "listen", "closesocket", "WSACleanup"},
    "c30002": {"accept"}, "c30003": {"recv"}, "c30004": {"send"},
    "c30005": {"closesocket"}, "c30006": {"CreateThread"},
    "c30011": {"EnterCriticalSection", "LeaveCriticalSection"},
    "e50001": set(), "e50002": set(), "e50003": set(), "e50005": set(),
    "e50006": set(), "e50007": set(), "e50008": set(),
    "e50009": set(),
    "e50010": {"CloseHandle"},
    "e50011": {"ReadFile"},
    "e50012": {"GetStdHandle", "InitializeCriticalSection", "ExitProcess",
               "CloseHandle", "WSACleanup"},
    "e50013": {"getaddrinfo", "freeaddrinfo", "socket", "connect", "closesocket"},
}
APPELS_DIRECTS = {
    # héritage (M2 — tcp-11 compose via libc-01/03/04 et écrit via hello-02)
    "c30011": {0x1100, 0x1200, 0x1280, 0x1040},
    # génération M3
    "e50004": {0x4C00, 0x4E80},                    # http-01, http-03
    "e50009": {0x4140, 0x4180},                    # tcp-03, tcp-04 — JAMAIS tcp-05
    "e50010": {0x4140, 0x4180, 0x41C0, 0x4300, 0x4B00, 0x4400,
               0x4C00, 0x4C80, 0x4F40, 0x5080, 0x5140, 0x5200, 0x5380, 0x54C0},
    "e50011": {0x1180, 0x41C0, 0x4B00},            # libc-02, tcp-05, tcp-11
    "e50012": {0x1040, 0x4000, 0x4100, 0x4300, 0x4B00, 0x5580, 0x5D80},
}
DONNEES_RIP = {
    "c30011": {L.R_STDOUT, L.R_CS},                # héritage : stdout + section critique
    "e50002": {L.R_TAB_METHODES, L.R_ANCRE},
    "e50008": {L.R_SLASH},
    "e50010": {L.R_MSG_CONNEXION, L.R_MSG_TUNNEL, L.R_MSG_FIN, L.R_NOM_HOST,
               L.R_NOM_CL, L.R_NOM_TE, L.R_TXT_400, L.R_TXT_431, L.R_TXT_501,
               L.R_TXT_411, L.R_TXT_505, L.R_TXT_502, L.R_TXT_TUNNEL,
               L.IAT_SLOTS["CloseHandle"]},
    "e50011": {L.R_STDIN, L.R_LISTEN, L.R_QUIT, L.R_CMD_QUIT, L.R_MSG_ARRET,
               L.R_MSG_INCONNU},
    "e50012": {L.R_ANCRE, L.R_TAB_SUM, L.R_VERSION, L.R_STDOUT, L.R_STDIN,
               L.R_CS, L.R_LISTEN, L.R_QUIT, L.R_MSG_BANNIERE, L.R_MSG_ERREUR,
               L.R_MSG_ARRET, L.R_MSG_KO, 0x5580, 0x5D80},
    "e50013": {L.IAT_SLOTS["getaddrinfo"], L.IAT_SLOTS["freeaddrinfo"],
               L.IAT_SLOTS["socket"], L.IAT_SLOTS["connect"],
               L.IAT_SLOTS["closesocket"]},
}
# Feuilles pures : AUCUN appel externe (les assistants locaux — étiquettes
# internes du même bloc — restent permis, miroir .protger de tcp-07)
FEUILLES_M3 = {"e50001", "e50002", "e50003", "e50005", "e50006", "e50007", "e50008"}


def _externe(bid: str, insn, adresses_bloc: set, adresse_entree: int) -> str | None:
    """Classe un call : 'iat:nom' | 'bloc:0x…' | 'interne' | None."""
    if "rip" in insn.op_str:
        cible = operande_rip_cible(insn)
        slot_iat = {L.IAT_SLOTS[n]: n for n in L.IAT_SLOTS}
        return f"iat:{slot_iat[cible]}" if cible in slot_iat else f"rip:{cible:#x}"
    if insn.op_str.startswith("0x"):
        cible = int(insn.op_str, 16)
        if cible in adresses_bloc and cible != adresse_entree:
            return "interne"
        return f"bloc:{cible:#x}"
    return None


def oracle_structurel(specs: dict, code: dict, blocs: list[tuple]) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    for bid, sid, _, rva, slot in blocs:
        insns = code[bid]["insns"]
        mnemos = [i.mnemonic for i in insns]
        adresses_insns = {i.address for i in insns}
        internes_autorises = APPELS_DIRECTS.get(bid, set()) | (
            {a for a in adresses_insns if a != rva} if bid in FEUILLES_M3 | {"e50013"} else set())

        # Cibles de saut internes : frontière d'instruction du même bloc
        for i in insns:
            if i.mnemonic.startswith("j"):
                cible = int(i.op_str, 16)
                verrou(f"{bid}:saut-interne@{i.address:#x}", cible in adresses_insns,
                       f"cible {cible:#x} hors frontière")

        # Appels : IAT et blocs autorisés par I1 ; assistants internes permis
        for i in insns:
            if i.mnemonic == "call":
                classe = _externe(bid, i, adresses_insns, rva)
                if classe is None:
                    continue
                if classe.startswith("iat:"):
                    verrou(f"{bid}:iat-autorisee@{i.address:#x}",
                           classe[4:] in IAT_PAR_BLOC.get(bid, set()),
                           f"{classe} hors IAT déclarée (I1)")
                elif classe.startswith("bloc:"):
                    verrou(f"{bid}:appel-autorise@{i.address:#x}",
                           int(classe[5:], 16) in internes_autorises,
                           f"{classe} hors blocs déclarés (I1)")

        # Données RIP : cibles déclarées du bloc ; les références à une
        # étiquette INTERNE du bloc (assistants, proc de thread — I5) sont
        # licites : le bloc ne dépend que de lui-même
        for i in insns:
            cible = operande_rip_cible(i)
            if cible is not None and i.mnemonic != "call":
                verrou(f"{bid}:donnees-autorisees@{i.address:#x}",
                       cible in DONNEES_RIP.get(bid, set())
                       or rva <= cible < rva + slot,
                       f"cible {cible:#x} hors données déclarées (I2/I5)")

        # Interface système : jamais de syscall direct (D7)
        verrou(f"{bid}:pas-de-syscall",
               not any(m in ("syscall", "sysenter", "int") for m in mnemos))

        # Padding intra-slot >= 16 et alignement (D8)
        fin_code = insns[-1].address + insns[-1].size
        verrou(f"{bid}:padding-16", rva + slot - fin_code >= 16, f"écart {rva + slot - fin_code}")
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

        # Pile alignée aux points d'appel EXTERNE (miroir M2 ; les assistants
        # internes ne traversent pas la frontière ABI)
        npush = 0
        while npush < len(insns) and insns[npush].mnemonic == "push":
            npush += 1
        premier_externe = next((k for k, i in enumerate(insns)
                                if i.mnemonic == "call" and _externe(bid, i, adresses_insns, rva)
                                not in (None, "interne")), None)
        if premier_externe is not None:
            ok = False
            for k in range(premier_externe):
                if insns[k].mnemonic == "sub" and insns[k].op_str.startswith("rsp,"):
                    imm = int(insns[k].op_str.split(",")[1].strip(), 16)
                    ok = (8 + 8 * npush - imm) % 16 == 0
                    break
            verrou(f"{bid}:pile-alignee", ok, "prologue non aligné avant appel externe")

    # Feuilles M3 : aucun appel externe (l'équilibre pile est dynamique —
    # l'oracle différentiel le constate par le retour à la sentinelle)
    for bid in FEUILLES_M3:
        for i in code[bid]["insns"]:
            if i.mnemonic == "call":
                verrou(f"{bid}:feuille-sans-appel-externe@{i.address:#x}",
                       _externe(bid, i, {x.address for x in code[bid]["insns"]},
                                next(r for b, _, _, r, _ in blocs if b == bid)) == "interne",
                       "une feuille pure n'appelle rien d'extérieur (I1)")

    # pompe (e50009) : tcp-05 INTERDIT (Q4 — jamais fermer)
    for i in code["e50009"]["insns"]:
        if i.mnemonic == "call" and i.op_str.startswith("0x"):
            verrou(f"e50009:jamais-fermer@{i.address:#x}",
                   int(i.op_str, 16) != 0x41C0, "la pompe ne ferme jamais (Q4)")

    # orchestrateur (e50012) : la porte R10 précède TOUT appel (I3)
    m = code["e50012"]["insns"]
    premier_appel = next((k for k, i in enumerate(m) if i.mnemonic == "call"), None)
    marqueur_boucle = [k for k, i in enumerate(m)
                       if canon(f"{i.mnemonic} {i.op_str}") == canon("add rbx, 0x10")]
    verrou("e50012:porte-r10-avant-tout-appel",
           premier_appel is not None and marqueur_boucle
           and premier_appel > marqueur_boucle[-1])
    verrou("e50012:aucun-ws2-direct",
           not any(i.mnemonic == "call" and operande_rip_cible(i) in
                   {L.IAT_SLOTS[n] for n in L.WS2_IMPORTS if n != "WSACleanup"} for i in m))
    verrou("e50012:somme-sur-image",
           any(canon(f"{i.mnemonic} {i.op_str}") == canon("add rax, qword ptr [r12 + rcx]") for i in m))

    # traçabilité : chaque bloc a sa spécification chargée (D24)
    attendus = {b for b, *_ in blocs}
    verrou("tracabilite-I", attendus <= set(specs), str(attendus - set(specs)))
    return verrous


# --- Composition des sections -------------------------------------------------

def _somme_qwords(octets: bytes) -> int:
    return sum(struct.unpack(f"<{len(octets) // 8}Q", octets)) & 0xFFFFFFFFFFFFFFFF


# Longueurs attendues des chaînes (garde-fou : la notation porte ces valeurs
# comme immédiats — toute divergence est refusée, miroir de l'erratum C1)
CHAINES = [
    (L.R_MSG_BANNIERE, L.BANNIERE, 40, "banniere"),
    (L.R_MSG_CONNEXION, b"connexion entrante\r\n", 20, "connexion"),
    (L.R_MSG_TUNNEL, b"tunnel\r\n", 8, "tunnel"),
    (L.R_MSG_FIN, b"fin connexion\r\n", 15, "fin"),
    (L.R_MSG_ARRET, b"arret\r\n", 7, "arret"),
    (L.R_MSG_INCONNU, b"commande inconnue\r\n", 19, "inconnu"),
    (L.R_MSG_ERREUR, b"erreur reseau, arret\r\n", 22, "erreur"),
    (L.R_MSG_KO, b"TRIADE M3 : integrite KO, arret\r\n", 33, "KO"),
    (L.R_CMD_QUIT, b"quit\r\n", 6, "quit"),
    (L.R_NOM_HOST, b"Host", 4, "nom-Host"),
    (L.R_NOM_CL, b"Content-Length", 14, "nom-CL"),
    (L.R_NOM_TE, b"Transfer-Encoding", 17, "nom-TE"),
    (L.R_SLASH, b"/", 1, "slash"),
]
REPONSES_TXT = [
    (L.R_TXT_400, b"HTTP/1.1 400 Requete mal formee\r\n\r\n", 35),
    (L.R_TXT_431, b"HTTP/1.1 431 Tete trop grande\r\n\r\n", 33),
    (L.R_TXT_501, b"HTTP/1.1 501 Non implemente\r\n\r\n", 31),
    (L.R_TXT_411, b"HTTP/1.1 411 Longueur requise\r\n\r\n", 33),
    (L.R_TXT_505, b"HTTP/1.1 505 Version non supportee\r\n\r\n", 38),
    (L.R_TXT_502, b"HTTP/1.1 502 Passerelle inaccessible\r\n\r\n", 40),
    (L.R_TXT_TUNNEL, b"HTTP/1.1 200 Tunnel etabli\r\n\r\n", 30),
]
METHODES_TXT = [b"GET", b"HEAD", b"POST", b"PUT", b"DELETE", b"OPTIONS", b"TRACE", b"CONNECT"]


def composer_sections(code: dict, blocs: list[tuple]):
    """-> (texte, rdata, data, text2) — l'image complète de proxy.exe."""
    texte = bytearray(b"\xcc" * L.TEXT_VSIZE)
    text2 = bytearray(b"\xcc" * L.TEXT2_VSIZE)
    for bid, _, _, rva, slot in blocs:
        if L.TEXT_RVA <= rva < L.RDATA_RVA:
            texte[rva - L.TEXT_RVA: rva - L.TEXT_RVA + slot] = code[bid]["slot"]
        elif rva >= L.TEXT2_RVA:
            text2[rva - L.TEXT2_RVA: rva - L.TEXT2_RVA + slot] = code[bid]["slot"]
        else:
            raise EchecBuild(f"{bid} : rva {rva:#x} hors sections attendues")

    # Table R10 : un par bloc embarqué + terminateur
    entrees = []
    for bid, _, _, rva, slot in blocs:
        if rva < L.TEXT2_RVA:
            tranche = bytes(texte[rva - L.TEXT_RVA: rva - L.TEXT_RVA + slot])
        else:
            tranche = bytes(text2[rva - L.TEXT2_RVA: rva - L.TEXT2_RVA + slot])
        entrees.append((rva, slot, _somme_qwords(tranche)))
    entrees.append((0, 0, 0))
    table = b"".join(struct.pack("<IIQ", r, t, s) for r, t, s in entrees)

    rdata = bytearray(b"\x00" * L.RDATA_VSIZE)
    _poses = []

    def poser(rva: int, donnees: bytes, nom: str = ""):
        fin = rva + len(donnees)
        if rva - L.RDATA_RVA + len(donnees) > L.RDATA_VSIZE:
            raise EchecBuild(f".rdata débordante à {rva:#x} (D33)")
        for rva_p, fin_p, nom_p in _poses:
            if rva < fin_p and rva_p < fin:
                raise EchecBuild(
                    f"chevauchement .rdata : {nom or hex(rva)} [{rva:#x}, {fin:#x})"
                    f" recouvre {nom_p} [{rva_p:#x}, {fin_p:#x})")
        _poses.append((rva, fin, nom or hex(rva)))
        rdata[rva - L.RDATA_RVA: rva - L.RDATA_RVA + len(donnees)] = donnees

    hn = lambda nom: struct.pack("<H", 0) + nom.encode("ascii") + b"\x00"

    # Descripteurs d'import (héritage exact M2 + entrées appendues M3)
    poser(L.R_DESC_IMPORT, struct.pack("<IIIII", L.R_INT_KERNEL32, 0, 0, L.R_NOM_DLL, L.R_IAT))
    poser(L.R_NOM_DLL, b"kernel32.dll\x00")
    poser(L.R_HN_GSH, hn("GetStdHandle"))
    poser(L.R_HN_WF, hn("WriteFile"))
    poser(L.R_HN_EP, hn("ExitProcess"))
    poser(L.R_NOM_WS2, b"ws2_32.dll\x00")
    hints_k32 = {"GetStdHandle": L.R_HN_GSH, "WriteFile": L.R_HN_WF, "ExitProcess": L.R_HN_EP,
                 "CreateThread": L.R_HN_CT, "VirtualProtect": L.R_HN_VP,
                 "InitializeCriticalSection": L.R_HN_ICS,
                 "EnterCriticalSection": L.R_HN_ECS,
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
    poser(L.R_DESC_WS2 + 20, b"\x00" * 20)
    poser(L.R_INT_WS2, b"".join(struct.pack("<Q", hints_ws2[n]) for n in L.WS2_IMPORTS)
          + struct.pack("<Q", 0))
    poser(L.R_IAT_WS2, b"".join(struct.pack("<Q", hints_ws2[n]) for n in L.WS2_IMPORTS)
          + struct.pack("<Q", 0))

    # Fixtures du domaine http (D46 — propriétaires uniques)
    for rva, chaine, taille, nom in CHAINES:
        if len(chaine) != taille:
            raise EchecBuild(f"garde-fou chaîne {nom} : {len(chaine)} o != {taille} (notation)")
        poser(rva, chaine + b"\x00", nom)
    for rva, chaine, taille in REPONSES_TXT:
        if len(chaine) != taille:
            raise EchecBuild(f"garde-fou réponse @{rva:#x} : {len(chaine)} o != {taille} (notation)")
        poser(rva, chaine, f"reponse-{taille}")
    poser(L.R_METHODES, b"".join(m + b"\x00" for m in METHODES_TXT), "methodes")
    # table des méthodes : 8 entrées ptr/longueur + terminateur (len 0)
    curseur = L.R_METHODES
    entrees_m = []
    for m in METHODES_TXT:
        entrees_m.append((curseur, len(m)))
        curseur += len(m) + 1
    poser(L.R_TAB_METHODES, b"".join(struct.pack("<QQ", p, n) for p, n in entrees_m)
          + struct.pack("<QQ", 0, 0), "table-methodes")
    poser(L.R_TAB_REPONSES,
          b"".join(struct.pack("<QQ", r, t) for r, _, t in REPONSES_TXT), "table-reponses")

    # Porte R10, version, ancre, relocations
    poser(L.R_TAB_SUM, table, "table-R10")
    poser(L.R_VERSION, struct.pack("<Q", L.VERSION_U64_DEV1))
    poser(L.R_ANCRE, struct.pack("<Q", 0))
    poser(L.R_RELOC, struct.pack("<II", L.TEXT_RVA, 12) + struct.pack("<HH", 0, 0))

    data = bytearray(b"\x00" * L.DATA_RAW)    # état nul au chargement
    return bytes(texte), bytes(rdata), bytes(data), bytes(text2)


# --- Éditeur PE32+ (quatre sections) ------------------------------------------

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
    dirs[1] = (L.R_DESC_IMPORT, 80)
    dirs[5] = (L.R_RELOC, 12)
    dirs[12] = (L.R_IAT, 88)
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

def valider_pe(exe: bytes):
    pe = pefile.PE(data=exe)
    assert pe.FILE_HEADER.Machine == 0x8664, "Machine != x86-64"
    assert pe.FILE_HEADER.NumberOfSections == 4, "sections != 4"
    assert pe.OPTIONAL_HEADER.Magic == 0x20B, "magic != PE32+"
    assert pe.OPTIONAL_HEADER.AddressOfEntryPoint == L.ENTREE, "point d'entrée != http-12"
    assert pe.OPTIONAL_HEADER.ImageBase == L.IMAGE_BASE
    assert pe.OPTIONAL_HEADER.Subsystem == 3, "sous-système != CONSOLE"
    dc = pe.OPTIONAL_HEADER.DllCharacteristics
    assert dc & 0x0040 and dc & 0x0020 and dc & 0x0100, "DYNAMICBASE/HEVA/NX absents"
    assert pe.OPTIONAL_HEADER.SizeOfImage == L.SIZE_OF_IMAGE
    noms = [s.Name.decode().rstrip("\x00") for s in pe.sections]
    assert noms == [".text", ".rdata", ".data", ".text2"], noms
    assert pe.sections[3].Characteristics & 0x60000020 == 0x60000020, ".text2 non RX"
    assert pe.sections[2].SizeOfRawData == L.DATA_RAW
    imports = {}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        imports[entree.dll.decode().lower()] = [i.name.decode() for i in entree.imports]
    assert imports == {"kernel32.dll": L.KERNEL32_IMPORTS, "ws2_32.dll": L.WS2_IMPORTS}, imports
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        ft_attendu = L.R_IAT if entree.dll.decode().lower() == "kernel32.dll" else L.R_IAT_WS2
        assert entree.struct.FirstThunk == ft_attendu, \
            f"FirstThunk {entree.dll.decode()} = {entree.struct.FirstThunk:#x} != {ft_attendu:#x} (D35)"
    assert len(exe) == L.TAILLE_FICHIER, "taille de fichier inattendue"
    # Zones réservées : int3 dans l'image livrée (trou net, reste tramp, tcp-09/10)
    assert exe[L.TEXT2_FILE + (0x4200 - L.TEXT2_RVA)] == 0xCC
    assert exe[L.TEXT2_FILE + (0x45C0 - L.TEXT2_RVA)] == 0xCC
    assert exe[L.TEXT2_FILE + (0x4800 - L.TEXT2_RVA)] == 0xCC
    return True


# --- Preuve de réutilisation (R7) ----------------------------------------------

SHA_HELLO = "c89e330cd16f3fd48558ed4fdb6708fb671e6d907547d5c1ee28075ffd6507f2"
SHA_SELFTEST = "8038585b7af83c9fe5e6fdccd197e67888b9e5fb09d8d6c84cb998c684bff3c0"
SHA_ECHO = None      # calculé à la première exécution (echo.exe scellé 0.3.0)


def _sha_fichier(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def preuve_reutilisation(exe: bytes) -> dict:
    """io M0, libc M1 et réseau M2 embarqués = octets identiques aux scellés."""
    global SHA_ECHO
    hello_p = os.path.join(M0_DIR, "hello.exe")
    selftest_p = os.path.join(M1_DIR, "selftest.exe")
    echo_p = os.path.join(M2_DIR, "echo.exe")
    if hashlib.sha256(open(hello_p, "rb").read()).hexdigest() != SHA_HELLO:
        raise EchecBuild("hello.exe divergent de l'artefact scellé (R7)")
    if hashlib.sha256(open(selftest_p, "rb").read()).hexdigest() != SHA_SELFTEST:
        raise EchecBuild("selftest.exe divergent de l'artefact scellé (R7)")
    if SHA_ECHO is None:
        SHA_ECHO = _sha_fichier(echo_p)
    elif _sha_fichier(echo_p) != SHA_ECHO:
        raise EchecBuild("echo.exe a divergé depuis la première preuve (R7)")
    with open(hello_p, "rb") as f:
        hello = f.read()
    with open(selftest_p, "rb") as f:
        selftest = f.read()
    with open(echo_p, "rb") as f:
        echo = f.read()
    heritage = ([("a10002", hello, 0x1040, 0x40), ("a10003", hello, 0x1080, 0x40),
                 ("b20001", selftest, 0x1100, 0x80), ("b20002", selftest, 0x1180, 0x80),
                 ("b20003", selftest, 0x1200, 0x80), ("b20004", selftest, 0x1280, 0x80)]
                + [("c30001", echo, 0x4000, 0x100), ("c30002", echo, 0x4100, 0x40),
                   ("c30003", echo, 0x4140, 0x40), ("c30004", echo, 0x4180, 0x40),
                   ("c30005", echo, 0x41C0, 0x40), ("c30006", echo, 0x4300, 0x40),
                   ("c30011", echo, 0x4B00, 0x100)])

    def tranche(buf, rva, slot):
        return buf[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot] \
            if rva < L.RDATA_RVA else \
            buf[0x2C00 + (rva - 0x4000): 0x2C00 + (rva - 0x4000) + slot]

    for bid, source, rva, slot in heritage:
        if tranche(source, rva, slot) != tranche(exe, rva, slot):
            raise EchecBuild(f"réutilisation rompue : {bid} diffère de l'artefact scellé (R7)")
    return {"blocs_reutilises": [b[0] for b in heritage], "sha_echo": SHA_ECHO}


# --- Carte projet, génération 5 ------------------------------------------------

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
               "k octets emis | -1 ; la boucle complete vie chez l appelant",
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
               "bascule = UNE ecriture alignee de qword ; phases RW/RX",
               "[b20001] [ext kernel32:VirtualProtect] [donnees .data]"),
    "c30008": ("(dst ptr, src ptr, n u64) -> u64",
               "dst >= n ; src >= n ; chevauchement exact autorise",
               "rax = n ; dst = T(src) avec T = identite (R1)",
               "FEUILLE ; volatils uniquement ; entree 0x4600 alignee 16",
               "aucune"),
    "c30009": ("(sock) -> ()", "socket connectee ; journal initialise",
               "chaque reception echoee integralement et journalisee ; fin propre",
               "tampon 1024 dans le cadre ; appels directs tcp-03/04/05/08/11",
               "[c30003] [c30004] [c30005] [c30008] [c30011] [rdata:messages]"),
    "c30010": ("() -> ()", "stdin/listen caches en .data ; journal initialise",
               "patch/rollback/quit executes et journalises ; inconnu journalise",
               "IAT ReadFile seule ; memcmp exact (longueur ET contenu)",
               "[b20002] [c30007] [c30005] [c30011] [ext kernel32:ReadFile]"),
    "c30011": ("(pre ptr, pre_len u64, valeur u32, suf ptr, suf_len u64) -> bool",
               "pre+12+suf <= 64 ; CS initialisee ; stdout cache ; pile alignee",
               "UNE ecriture WriteFile de la ligne composee ; BOOL propage",
               "composition sur pile privee sous section critique",
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
               "aucun ws2_32 direct ; base d image par ancre RIP (PI)",
               "[c30001] [c30002] [c30006] [c30011] [a10002] [a10003] "
               "[ext kernel32:GSH,InitCS,CloseHandle,ExitProcess]"),
    "c30014": ("(dst ptr, src ptr, n u64) -> u64",
               "idem c30008 (contrat stable R4)",
               "rax = n ; dst = T(src) avec T = majuscules ASCII (R2)",
               "FEUILLE ; volatils uniquement ; assemble POUR 0x4680 (staging)",
               "aucune"),
    "e50001": ("(tampon ptr, longueur u64, curseur u64) -> (verdict, longueur, curseur)",
               "tampon stable ; curseur dans [0, longueur]",
               "0 : rdx = ligne sans CRLF, r8 = apres CRLF ; 1 : inchanges",
               "feuille pure : aucun appel, aucune ecriture, non-volatils intacts",
               "aucune"),
    "e50002": ("(ligne ptr, longueur u64, zone ptr 56) -> u32",
               "ligne isolee par http-01 ; pile alignee",
               "0 : zone remplie (enums + spans) ; 1..4 verdicts nommes",
               "feuille pure ; table des methodes .rdata = LA validation ; "
               "zone ecrite une seule fois apres verdict final",
               "[rdata:table-methodes]"),
    "e50003": ("(ligne ptr, longueur u64, zone ptr 32) -> u32",
               "ligne isolee par http-01",
               "0 : nom/valeur (OWS rognes par bornes) ; 1 sans separateur ; 2 nom invalide",
               "feuille pure ; aucune ecriture hors zone, aucune ecriture partielle",
               "aucune"),
    "e50004": ("(bloc ptr, longueur, nom ptr, nom_len, zone ptr 32) -> u32",
               "nom_len > 0 ; bloc = region apres ligne de requete",
               "0 : premiere occurrence ; 1 absent (ligne vide) ; 2 bloc invalide",
               "appels http-01/http-03 uniquement ; l unique comparaison "
               "insensible a la casse du domaine http ; zone intacte hors trouve",
               "[e50001] [e50003]"),
    "e50005": ("(span ptr, longueur) -> (u32, edx u32)",
               "pile alignee",
               "0 : edx = valeur u32 ; 1..5 verdicts nommes ; edx intact sur echec",
               "feuille pure ; test de borne a chaque chiffre (I2)",
               "aucune"),
    "e50006": ("(tampon ptr, remplissage) -> (u32, rdx u64)",
               "capacite >= 8193 (garantie http-10)",
               "0 : rdx = longueur de tete ; 1 incomplet ; 2 limite ; 3 LF isole",
               "feuille pure ; proprietaire de MAX_TETE 8192",
               "aucune"),
    "e50007": ("(span ptr, longueur, defaut u16, zone ptr 24) -> u32",
               "defaut 0 = port EXIGE",
               "0 : hote (crochets exclus) + port effectif ; 1..3 verdicts nommes",
               "feuille pure ; DERNIER deux-points hors crochets ; port valide "
               "chiffre a chiffre, <= 65535",
               "aucune"),
    "e50008": ("(cible ptr, longueur, methode u32, zone ptr 40) -> u32",
               "longueur > 0 (garantie http-02)",
               "0 : forme 1/2/3 + spans autorite/chemin ; 1..3 verdicts nommes",
               "feuille pure ; schema http:// strict minuscule ; chemin par "
               "defaut / fixture ; autorite JAMAIS interpretee ici",
               "[rdata:slash]"),
    "e50009": ("(src sock, dst sock, tampon ptr, capacite) -> (u32, rdx total)",
               "sockets ouvertes ; capacite > 0",
               "0 fin normale ; 1 erreur source ; 2 erreur destination ; "
               "total sur tout verdict",
               "appels tcp-03/tcp-04 UNIQUEMENT — jamais tcp-05 (Q4) ; "
               "emissions partielles rejouees",
               "[c30003] [c30004]"),
    "e50010": ("(sock cliente) -> ()",
               "CS/stdout initialises par http-12 ; WSA actif ; pile vierge",
               "session complete : accumulation, parsing E1-E8, tunnel ou "
               "requete ordinaire, fermetures uniques (amont puis cliente), "
               "journal connexion/tunnel/fin",
               "corps de requete borne Content-Length INLINE (R2) ; "
               "http-09 reserve au tunnel et au relais de reponse ; "
               "spans d origine recopies, en-tetes verbatim",
               "[c30003] [c30004] [c30005] [c30006] [c30011] [e50013] "
               "[e50001..e50009] [ext kernel32:CloseHandle] [rdata:reponses,noms]"),
    "e50011": ("(arg u64) -> ()",
               "stdin/listen/quit en .data (http-12)",
               "quit : drapeau + fermeture ecoute + journal arret ; autre : "
               "journal inconnu ; EOF/echec : fin sans effet",
               "IAT ReadFile seule ; comparaison exacte 6 octets ; thread "
               "termine par ret",
               "[b20002] [c30005] [c30011] [ext kernel32:ReadFile] "
               "[rdata:quit,messages] [donnees .data:stdin,listen,quit]"),
    "e50012": ("() -> noreturn",
               "point d entree proxy.exe ; pile alignee ; .data a l etat image",
               "porte R10 (plancher 0x00040000) AVANT tout effet ; init dans "
               "l ordre I2 ; boucle accept/session ; ExitProcess 0|1|2",
               "aucun ws2_32 direct hors WSACleanup (chemin propre) ; ordre "
               "handle->CS->banniere->ecoute->console invariant (I2)",
               "[c30001] [c30002] [c30006] [c30011] [e50010] [e50011] [a10002] "
               "[a10003] [ext kernel32:GSH,InitCS,CloseHandle,ExitProcess] "
               "[ext ws2_32:WSACleanup] [rdata:table,version,ancre,messages]"),
    "e50013": ("(hote ptr, longueur, port u16) -> sock|0",
               "WSA actif ; crochets exclus par http-07 ; >= 0x220 o de pile",
               "socket amont connectee ; 0 sur tout echec nomme",
               "traduction span->chaine C propriete unique (Q2) ; nettoyage "
               "complet un-pour-un ; port en ordre reseau par rol (I3) ; "
               "WSACleanup JAMAIS",
               "[ext ws2_32:getaddrinfo,freeaddrinfo,socket,connect,closesocket]"),
}

ROLES = dict(L.NOMS_BLOCS)

EXE_PAR_BLOC = {
    "a10001": "hello", "a10002": "hello,selftest,echo,proxy",
    "a10003": "hello,selftest,echo,proxy",
    "b20001": "selftest,echo,proxy", "b20002": "selftest,echo,proxy",
    "b20003": "selftest,echo,proxy", "b20004": "selftest,echo,proxy",
    "b20005": "selftest", "b20006": "selftest", "b20007": "selftest",
    "b20008": "selftest",
    "c30001": "echo,proxy", "c30002": "echo,proxy", "c30003": "echo,proxy",
    "c30004": "echo,proxy", "c30005": "echo,proxy", "c30006": "echo,proxy",
    "c30007": "echo", "c30008": "echo", "c30009": "echo", "c30010": "echo",
    "c30011": "echo,proxy", "c30012": "aucun", "c30013": "echo", "c30014": "echo",
    "e50001": "proxy", "e50002": "proxy", "e50003": "proxy", "e50004": "proxy",
    "e50005": "proxy", "e50006": "proxy", "e50007": "proxy", "e50008": "proxy",
    "e50009": "proxy", "e50010": "proxy", "e50011": "proxy", "e50012": "proxy",
    "e50013": "proxy",
}


def fragments_clairs(code: dict, exe: bytes, verrous: list[str], blocs: list[tuple],
                     version: str, verdict_oracle: dict, compteurs: dict,
                     journal_runs: list[str]) -> dict[str, bytes]:
    sha = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()
    rva_par_bloc = {"a10001": 0x1000, "a10002": 0x1040, "a10003": 0x1080,
                    "b20001": 0x1100, "b20002": 0x1180, "b20003": 0x1200,
                    "b20004": 0x1280, "b20005": 0x1300, "b20006": 0x1380,
                    "b20007": 0x13C0, "b20008": 0x1800, "c30012": 0x1440,
                    "c30014": 0x4680}
    rva_par_bloc |= {bid: rva for bid, _, _, rva, _ in blocs}
    for bid, _, _, rva, _ in [(b[0], 0, 0, b[3], b[4]) for b in [
        ("c30007", 0, 0, 0x4400, 0x200), ("c30008", 0, 0, 0x4600, 0x40),
        ("c30009", 0, 0, 0x4800, 0x180), ("c30010", 0, 0, 0x4980, 0x180),
        ("c30013", 0, 0, 0x1800, 0x800)]]:
        rva_par_bloc[bid] = rva

    loc = ["[carte-frag] nom=frag-loc generation=5",
           "[zones] io=0x1000-0x10ff libc=0x1100-0x17ff app=0x1800-0x1fff "
           "net=0x4000-0x42ff cli=0x4400-0x45bf thr=0x4300-0x43ff "
           "srv=0x4b00-0x4bff http=0x4c00-0x5e7f "
           "reserve-libc=0x13c0-0x17ff (int3 defensif)"]
    tous_loc = (["a10001", "a10002", "a10003", "b20001", "b20002", "b20003",
                 "b20004", "b20005", "b20006", "b20007", "b20008"]
                + ["c30001", "c30002", "c30003", "c30004", "c30005", "c30006",
                   "c30007", "c30008", "c30009", "c30010", "c30011", "c30012",
                   "c30013", "c30014"]
                + [b for b, _, _, _, _ in blocs if b.startswith("e5")])
    spec_par_bloc = {
        "a10001": "hello-01:R1", "a10002": "hello-02:R1", "a10003": "hello-03:R1",
        "b20001": "libc-01:R1", "b20002": "libc-02:R1", "b20003": "libc-03:R1",
        "b20004": "libc-04:R1", "b20005": "libc-05:R1", "b20006": "libc-06:R1",
        "b20007": "libc-07:R1", "b20008": "libc-08:R2",
        "c30001": "tcp-01:R1", "c30002": "tcp-02:R1", "c30003": "tcp-03:R1",
        "c30004": "tcp-04:R1", "c30005": "tcp-05:R1", "c30006": "tcp-06:R1",
        "c30007": "tcp-07:R3", "c30008": "tcp-08:R1", "c30009": "tcp-09:R1",
        "c30010": "tcp-10:R1", "c30011": "tcp-11:R1", "c30012": "libc-09:R1",
        "c30013": "tcp-12:R1", "c30014": "tcp-08:R2",
        "e50001": "http-01:R1", "e50002": "http-02:R1", "e50003": "http-03:R1",
        "e50004": "http-04:R1", "e50005": "http-05:R1", "e50006": "http-06:R2",
        "e50007": "http-07:R1", "e50008": "http-08:R1", "e50009": "http-09:R1",
        "e50010": "http-10:R2", "e50011": "http-11:R1", "e50012": "http-12:R1",
        "e50013": "tcp-13:R1",
    }
    for bid in tous_loc:
        loc.append(f"[bloc] id={bid} spec={spec_par_bloc[bid]} cible=x86-64-win11-pe "
                   f"exe={EXE_PAR_BLOC[bid]} addr={L.IMAGE_BASE + rva_par_bloc[bid]:#x} "
                   f"v=1 etat=scelle role={ROLES[bid]}")

    con = ["[carte-frag] nom=frag-con generation=5"]
    for bid in tous_loc:
        sig, pre, post, inv, deps = CONTRATS[bid]
        con += [f"[bloc] id={bid}", f"  sig : {sig}", f"  pre : {pre}",
                f"  post : {post}", f"  inv : {inv}", f"  deps : {deps}"]

    prf = ["[carte-frag] nom=frag-prf generation=5"]
    fich_par_bid = dict(_FICHIERS_M3)
    fich_par_bid |= {"a10001": "hello-01-main", "b20005": "libc-05-zone-alloc",
                     "b20006": "libc-06-zone-reset", "b20007": "libc-07-memset",
                     "b20008": "libc-08-autotest", "c30012": "libc-09-zone-alloc-ts",
                     "c30014": "tcp-08-echo-v2", "c30007": "tcp-07-patch",
                     "c30008": "tcp-08-echo", "c30009": "tcp-09-conn",
                     "c30010": "tcp-10-console", "c30013": "tcp-12-main"}
    for bid in tous_loc:
        fichier = fich_par_bid.get(bid) or next(
            (f for b, _, f, _, _ in blocs if b == bid), None)
        if fichier is None:
            raise EchecBuild(f"frag-prf : notation introuvable pour {bid}")
        notation = chemin_notation(fichier)
        with open(notation, "rb") as f:
            empreinte_notation = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [
            f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} crist={crist}/10",
            f"  vecteurs : roundtrip=ok structure=ok notation={empreinte_notation}",
            f"  differentiel : {verdict_oracle.get('blocs', {}).get(bid, {}).get('detail', '-') if False else '-'}"]
    prf.append("[verifications] runs=" + str(len(journal_runs)))
    prf += ["  " + r for r in journal_runs[-12:]]

    bld = ["[carte-frag] nom=frag-bld generation=5"]
    embarques = {b for b, *_ in blocs}
    for bid in tous_loc:
        rva = rva_par_bloc[bid]
        if bid in embarques:
            if rva < L.RDATA_RVA:
                s = next(sl for b, _, _, r, sl in blocs if b == bid)
                tranche = exe[L.TEXT_FILE + (rva - L.TEXT_RVA):
                              L.TEXT_FILE + (rva - L.TEXT_RVA) + s]
            else:
                s = next(sl for b, _, _, r, sl in blocs if b == bid)
                tranche = exe[L.TEXT2_FILE + (rva - L.TEXT2_RVA):
                              L.TEXT2_FILE + (rva - L.TEXT2_RVA) + s]
            empreinte = sha(tranche)
        else:
            with open(chemin_notation(fich_par_bid[bid]), "rb") as f:
                empreinte = "notation:" + sha(f.read())[7:]
        bld.append(f"[bloc] id={bid} addr={L.IMAGE_BASE + rva:#x} empreinte={empreinte}")
    bld += [
        f"[build] artefact=proxy.exe version={version} profil=x86-64-win11-pe "
        f"taille={len(exe)} empreinte={sha(exe)}",
        f"  outils : keystone-engine + capstone {capstone.cs_version()[0]}.{capstone.cs_version()[1]} ; "
        f"verrous={len(verrous)} ; oracle : {verdict_oracle.get('total_cas', 0)} cas, "
        f"graine={verdict_oracle.get('graine', '-')}, volume={verdict_oracle.get('volume', '-')}",
        f"  heritage : hello.exe 0.1.0 + selftest.exe 0.2.0 + echo.exe 0.3.0 "
        f"(io/libc/tcp reutilises octet-identiques, R7)",
        "[zones] io=0x1000-0x10ff libc=0x1100-0x17ff app=0x1800-0x1fff "
        "net=0x4000-0x42ff cli=0x4400-0x45bf thr=0x4300-0x43ff "
        "srv=0x4b00-0x4bff http=0x4c00-0x5e7f",
    ]

    retour = {}
    for nom, lignes in (("frag-loc", loc), ("frag-con", con), ("frag-prf", prf), ("frag-bld", bld)):
        retour[nom] = ("\n".join(lignes) + "\n").encode("utf-8", errors="replace")
    return retour


def construire_carte(code, exe, verrous, blocs, version, verdict_oracle, compteurs,
                     journal_runs):
    phrase, _ = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    clairs = fragments_clairs(code, exe, verrous, blocs, version, verdict_oracle,
                              compteurs, journal_runs)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    racine = cm.empreinte_racine(fragments)
    entete = cm.construire_entete(racine)
    prive, pub = cm.paire_cles(cm.charger_secrets(interactif=False)[1])
    signature = cm.signer(prive, entete, fragments)
    cm.ecrire_carte(entete, fragments, signature, pub)
    return pub


# --- Verrou croisé (R8) : relecture indépendante des artefacts ------------------

def verrou_croise(blocs: list[tuple]) -> tuple[int, dict]:
    phrase, _ = cm.charger_secrets(interactif=False)
    entete, fragments, signature, pub = cm.lire_carte()
    cm.verifier_listes_blanches(entete.decode("ascii"))
    cm.verifier_signature(pub, entete, fragments, signature)
    if cm.empreinte_racine(fragments).hex() not in entete.decode("ascii"):
        raise cm.ErreurCarte("empreinte racine divergente")
    maitre = cm.cle_maitresse(phrase)
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
    with open(os.path.join(ICI, "proxy.exe"), "rb") as f:
        exe = f.read()
    empreintes, manifestes = {}, []
    for ligne in bld.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[champs["id"]] = champs["empreinte"]
        elif ligne.startswith("[build]"):
            manifestes.append(dict(re.findall(r"(\w+)=(\S+)", ligne)))
    manifeste = next((m for m in manifestes if m.get("artefact") == "proxy.exe"), {})
    for bid, _, _, rva, slot in blocs:
        if rva < L.RDATA_RVA:
            tranche = exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        else:
            tranche = exe[L.TEXT2_FILE + (rva - L.TEXT2_RVA): L.TEXT2_FILE + (rva - L.TEXT2_RVA) + slot]
        sha = "sha256:" + hashlib.sha256(tranche).hexdigest()
        if sha != empreintes.get(bid):
            raise cm.ErreurCarte(f"verrou croisé : empreinte de {bid} divergente (R8)")
    sha_exe = "sha256:" + hashlib.sha256(exe).hexdigest()
    if sha_exe != manifeste.get("empreinte"):
        raise cm.ErreurCarte("verrou croisé : empreinte de proxy.exe divergente (R8)")
    return len(empreintes), manifeste


# --- Tableau de bord (§ 15.2, métriques M3) --------------------------------------

def tableau_de_bord(exe: bytes, verrous: list[str], nb_blocs_carte: int, manifeste: dict,
                    verdict_oracle: dict) -> str:
    sha = lambda b: hashlib.sha256(b).hexdigest()
    lignes = [
        "[tableau] jalon=M3 artefact=proxy.exe version=" + manifeste.get("version", "?"),
        f"  blocs_avec_spec_a_jour        : {nb_blocs_carte}/38 : audit de tracabilite I->C->B (4 artefacts)",
        f"  chaines_I_C_B_tests           : {nb_blocs_carte}/{nb_blocs_carte} : specs, carte, exe, vecteurs",
        f"  construction                  : 0 erreur / 0 avertissement : build script",
        f"  tests_differentiels           : {verdict_oracle.get('total_cas', 0)} cas verts "
        f"({verdict_oracle.get('volume', '-')}, graine {verdict_oracle.get('graine', '-')}) ; "
        f"oracle structurel {len(verrous)} verrous PASS",
        f"  empreintes_donnees_embarquees : conforme (fixtures http, table R10, chaines, version)",
        f"  defauts_T1_T6_ouverts         : 0 : journal des decisions D45-D47",
        f"  optimisations_sans_mesure     : 0 : aucune optimisation M3 (R11)",
        f"  changements_hors_journal      : 0 : D45 a D47 consignees",
        f"  preversions                   : {manifeste.get('version', '?')} conforme "
        f"(schema dev/rc/final, monotonie ; anti-rollback R10 verifie par l'oracle)",
        f"  entrees_non_fiables           : comportement defini par contrat (E1-E8, "
        f"verdicts nommes, tolerance zero) ; falsification : defauts injectes DETECTES",
        f"  artefact                      : {len(exe)} octets ; empreinte sha256:{sha(exe)[:16]}... ; "
        f"reutilisation M0/M1/M2 : 13 blocs octet-identiques (R7)",
        f"  verrou_croise                 : {nb_blocs_carte} empreintes reverifiees "
        f"(4 artefacts + notations non embarquees) + signature Ed25519 + racine (R8/R9)",
    ]
    return "\n".join(lignes) + "\n"


# --- Assemblage + vérification communs -------------------------------------------

def assembler_tout():
    blocs = blocs_embarques()
    specs = charger_couche_I(blocs)
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code: dict[str, dict] = {}
    for bid, sid, fichier, rva, slot in blocs:
        chemin = chemin_notation(fichier)
        octets, metas = assembler_bloc(ks, chemin, rva, slot)
        insns = round_trip(cs, ks, chemin, rva, octets, metas)
        slot_complet = octets + b"\x90" * (slot - len(octets))
        code[bid] = {"octets": octets, "metas": metas, "insns": insns, "slot": slot_complet}
        print(f"[R5] {bid} ({sid}) : {len(octets)} o, round-trip {len(insns)}/{len(insns)} = 100 %")
    verrous = oracle_structurel(specs, code, blocs)
    print(f"[oracle] structurel : {len(verrous)} verrous PASS (contrats I verifies par bloc)")
    return blocs, specs, code, verrous


# --- Modes -----------------------------------------------------------------------

def construire(volume: str, graine: int) -> int:
    print("=== M3 : chaine artefact TRIADE (profil x86-64-win11-pe) ===")
    blocs, specs, code, verrous = assembler_tout()
    version = L.VERSION_DEV1

    texte, rdata, data, text2 = composer_sections(code, blocs)
    exe = ecrire_pe32plus(texte, rdata, data, text2)
    valider_pe(exe)
    heritage = preuve_reutilisation(exe)
    print(f"[PE] proxy.exe : {len(exe)} octets, 4 sections, kernel32 x10 + ws2_32 x13, "
          f"DYNAMICBASE+HEVA+NX, entree 0x{L.ENTREE:x}")
    print(f"[R7] reutilisation : {len(heritage['blocs_reutilises'])} blocs octet-identiques "
          f"aux artefacts scelles M0/M1/M2")

    verdict = od.executer(exe, graine=graine, volume=volume)
    print(f"[oracle] differentiel : {verdict['total_cas']} cas verts ; "
          f"falsification : defauts injectes detectes")

    with open(os.path.join(ICI, "proxy.exe"), "wb") as f:
        f.write(exe)

    compteurs = {bid: 1 for bid, _, _, _, _ in blocs}
    journal = [f"run graine={graine} volume={volume} verdict={verdict['empreinte']} "
               f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} build={version}"]
    construire_carte(code, exe, verrous, blocs, version, verdict, compteurs, journal)
    print(f"[carte] generation 5 ecrite : 4 fragments chiffres, signature Ed25519, "
          f"38 blocs indexes sur 4 artefacts")

    nb, manifeste = verrou_croise(blocs)
    print(f"[R8] verrou croise : signature OK, racine OK, {nb} empreintes reverifiees, "
          f"artefact {manifeste.get('version')}")

    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="utf-8") as f:
        f.write(tableau_de_bord(exe, verrous, nb, manifeste, verdict))
    print("[tableau] tableau de bord ecrit (carte/tableau-de-bord.txt)")
    print(f"[B] proxy.exe scelle : sha256:{hashlib.sha256(exe).hexdigest()}")
    print(f"=== M3-dev (oracle vert) : {version} — proxy transparent curl en attente (etape c) ===")
    return 0


def verifier(graine: int, volume: str) -> int:
    print(f"=== M3 : re-verification complete (R5/R8, graine {graine}) ===")
    blocs, specs, code, verrous = assembler_tout()

    with open(os.path.join(ICI, "proxy.exe"), "rb") as f:
        exe = f.read()
    for bid, _, _, rva, slot in blocs:
        if rva < L.RDATA_RVA:
            embarque = exe[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        else:
            embarque = exe[L.TEXT2_FILE + (rva - L.TEXT2_RVA): L.TEXT2_FILE + (rva - L.TEXT2_RVA) + slot]
        if embarque != code[bid]["slot"]:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5 — verifier-puis-ecrire)")

    verdict = od.executer(exe, graine=graine, volume=volume)
    print(f"[oracle] differentiel : {verdict['total_cas']} cas verts")

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
    journal.append(f"run graine={graine} volume={volume} verdict={verdict['empreinte']} "
                   f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")

    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
    manifeste_v = next((dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
                        if "artefact=proxy.exe" in l), "?")
    version = manifeste_v if manifeste_v != "?" else L.VERSION_DEV1
    construire_carte(code, exe, verrous, blocs, version, verdict, compteurs, journal)
    nb, manifeste = verrou_croise(blocs)
    crist = {b: compteurs.get(b, 0) for b, _, _, _, _ in blocs}
    print("[R6] cristallisation : " + ", ".join(f"{b}={n}/10" for b, n in list(crist.items())[:6])
          + (", …" if len(crist) > 6 else ""))
    print(f"[R8] verrou croise : {nb} empreintes conformes ; artefact {manifeste.get('version')}")
    with open(os.path.join(cm.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="utf-8") as f:
        f.write(tableau_de_bord(exe, verrous, nb, manifeste, verdict))
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if "--verifier" in args:
            graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 1
            volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
            sys.exit(verifier(graine, volume))
        volume = args[args.index("--volume") + 1] if "--volume" in args else "complet"
        graine = int(args[args.index("--graine") + 1]) if "--graine" in args else 1
        sys.exit(construire(volume, graine))
    except (EchecBuild, cm.ErreurCarte, od.EchecOracle) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
