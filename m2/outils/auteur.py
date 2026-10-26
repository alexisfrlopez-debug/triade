#!/usr/bin/env python3
"""auteur.py — Outil d'auteur du jalon M2 : résolution des étiquettes.

Même discipline qu'en M1 (aucun compilateur entre l'intention et les octets :
keystone assemble, rien d'autre) — cet outil fait l'arithmétique d'adresses
de l'auteur : étiquettes locales -> adresses absolues des sauts, symboles de
blocs -> cibles d'appels directes, symboles de données -> déplacements RIP
calculés une fois pour toutes depuis le plan d'adressage M2 (layout.py,
D28 étendu par D33).

Entrée : notation/brouillons/*.asm. Sortie : notation/*.asm — notation
explicite WYSIWYG, seule lue par build_m2.py (round-trip R5 sur la sortie).

Le brouillon echo-01-v2 (remplaçant majuscules, boucle § 5) est déclaré dès
le départ mais ignoré tant que absent : il n'existe qu'à partir de dev.2,
assemblé POUR l'adresse de croissance 0x4680.

Usage : python3 outils/auteur.py [--verifier-seulement]
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import layout as L

from keystone import Ks, KS_ARCH_X86, KS_MODE_64

ICI = os.path.dirname(os.path.abspath(__file__))
BROUILLONS = os.path.join(ICI, "..", "notation", "brouillons")
SORTIE = os.path.join(ICI, "..", "notation")

# (fichier brouillon, id bloc, spec, rva, slot, dépendances)
BLOCS = [
    ("tcp-01-init", "c30001", "tcp-01:R1", 0x4000, 0x100,
     "IAT ws2_32 : WSAStartup, socket, bind, listen, closesocket, WSACleanup"),
    ("tcp-02-accept", "c30002", "tcp-02:R1", 0x4100, 0x40,
     "IAT ws2_32 : accept"),
    ("tcp-03-recv", "c30003", "tcp-03:R1", 0x4140, 0x40,
     "IAT ws2_32 : recv"),
    ("tcp-04-send", "c30004", "tcp-04:R1", 0x4180, 0x40,
     "IAT ws2_32 : send"),
    ("tcp-05-close", "c30005", "tcp-05:R1", 0x41C0, 0x40,
     "IAT ws2_32 : closesocket"),
    ("tcp-06-spawn", "c30006", "tcp-06:R1", 0x4300, 0x40,
     "IAT kernel32 : CreateThread"),
    ("tcp-07-patch", "c30007", "tcp-07:R2", 0x4400, 0x200,
     "IAT kernel32 : VirtualProtect ; bloc libc-01 memcpy @0x1100 ; "
     "données : echo @0x4600, croissance @0x4680, staging, table, état .data ; "
     "D39 : phases d'écriture en PAGE_EXECUTE_READWRITE (0x40), jamais RW"),
    ("tcp-08-echo", "c30008", "tcp-08:R1", 0x4600, 0x40,
     "bloc feuille ; aucun accès extérieur (cible du patch à chaud)"),
    ("tcp-09-conn", "c30009", "tcp-09:R1", 0x4800, 0x180,
     "blocs tcp-03/04/05, tcp-08 echo @0x4600, tcp-11 ; chaînes .rdata"),
    ("tcp-10-console", "c30010", "tcp-10:R1", 0x4980, 0x180,
     "IAT kernel32 : ReadFile ; blocs libc-02, tcp-07, tcp-05, tcp-11 ; "
     "état .data (stdin, listen, quit) ; chaînes .rdata"),
    ("tcp-11-journal", "c30011", "tcp-11:R1", 0x4B00, 0x100,
     "IAT kernel32 : Enter/LeaveCriticalSection ; blocs libc-01/03/04, "
     "io-01 write @0x1040 ; état .data (stdout, CS)"),
    ("tcp-12-main", "c30013", "tcp-12:R1", 0x1800, 0x800,
     "IAT kernel32 : GSH, InitCS, CloseHandle, ExitProcess ; blocs tcp-01/02/"
     "06/11, io-01 write, io-02 exit ; table R10 + version .rdata ; état .data"),
    ("libc-09-zone-alloc-ts", "c30012", "libc-09:R1", 0x1440, 0x80,
     "IAT kernel32 : Enter/LeaveCriticalSection ; bloc libc-05 @0x1300 ; "
     "données .data : CS (NON embarqué dans echo.exe)"),
    # Remplaçant echo-01:R2 (dev.2, boucle § 5) — assemblé POUR la croissance.
    ("tcp-08-echo-v2", "c30014", "tcp-08:R2", 0x4680, 0x80,
     "bloc feuille ; aucun accès extérieur (remplaçant, zone de croissance)"),
]

SYMBOLES = {
    # blocs hérités (octets scellés M0/M1)
    "WRITE": 0x1040, "EXIT": 0x1080,
    "MEMCPY": 0x1100, "MEMCMP": 0x1180, "STRLEN": 0x1200, "ITOA": 0x1280,
    "ZONE_ALLOC": 0x1300, "ZONE_RESET": 0x1380, "MEMSET": 0x13C0,
    # blocs M2
    "TCP_INIT": 0x4000, "TCP_ACCEPT": 0x4100, "TCP_RECV": 0x4140,
    "TCP_SEND": 0x4180, "TCP_CLOSE": 0x41C0, "TCP_SPAWN": 0x4300,
    "TCP_PATCH": 0x4400, "ECHO": 0x4600, "CONN": 0x4800,
    "CONSOLE": 0x4980, "TCP_JOURNAL": 0x4B00, "ECHO_V2": 0x4680,
    # IAT kernel32
    "IAT_GSH": L.IAT_SLOTS["GetStdHandle"], "IAT_WF": L.IAT_SLOTS["WriteFile"],
    "IAT_EP": L.IAT_SLOTS["ExitProcess"], "IAT_CREATETHREAD": L.IAT_SLOTS["CreateThread"],
    "IAT_VPROTECT": L.IAT_SLOTS["VirtualProtect"],
    "IAT_ICS": L.IAT_SLOTS["InitializeCriticalSection"],
    "IAT_ECS": L.IAT_SLOTS["EnterCriticalSection"],
    "IAT_LCS": L.IAT_SLOTS["LeaveCriticalSection"],
    "IAT_READFILE": L.IAT_SLOTS["ReadFile"], "IAT_CH": L.IAT_SLOTS["CloseHandle"],
    # IAT ws2_32
    "IAT_WSASTARTUP": L.IAT_SLOTS["WSAStartup"], "IAT_SOCKET": L.IAT_SLOTS["socket"],
    "IAT_BIND": L.IAT_SLOTS["bind"], "IAT_LISTEN": L.IAT_SLOTS["listen"],
    "IAT_ACCEPT": L.IAT_SLOTS["accept"], "IAT_RECV": L.IAT_SLOTS["recv"],
    "IAT_SEND": L.IAT_SLOTS["send"], "IAT_CLOSESOCK": L.IAT_SLOTS["closesocket"],
    "IAT_WSAGLE": L.IAT_SLOTS["WSAGetLastError"],
    "IAT_WSACLEANUP": L.IAT_SLOTS["WSACleanup"],
    # code .text2 (points trampolinables)
    "CROISSANCE": L.ECHO_CROISSANCE,
    # données .rdata (M2)
    "STAGING": L.R_STAGING,
    "TAB_SUM": L.R_TAB_SUM,
    "TAB_TAILLE": L.R_TAB_SUM + 4,
    "TAB_SOMME": L.R_TAB_SUM + 8,
    "VERSION": L.R_VERSION,
    "ANCRE": L.R_ANCRE,
    "MSG_BANNIERE": L.R_MSG_BANNIERE, "MSG_CONNEXION": L.R_MSG_CONNEXION,
    "MSG_ECHO": L.R_MSG_ECHO, "MSG_CRLF": L.R_MSG_CRLF,
    "MSG_PATCH_OK": L.R_MSG_PATCH_OK, "MSG_RB_OK": L.R_MSG_RB_OK,
    "MSG_INCONNU": L.R_MSG_INCONNU, "MSG_REFUS": L.R_MSG_REFUS,
    "MSG_FIN": L.R_MSG_FIN, "MSG_ARRET": L.R_MSG_ARRET,
    "MSG_ERREUR": L.R_MSG_ERREUR, "MSG_KO": L.R_MSG_KO,
    "CMD_PATCH": L.R_CMD_PATCH, "CMD_RB": L.R_CMD_RB, "CMD_QUIT": L.R_CMD_QUIT,
    # état .data (M2)
    "STDOUT": L.R_STDOUT, "STDIN": L.R_STDIN, "LISTEN": L.R_LISTEN,
    "QUIT": L.R_QUIT, "ETAT_PATCH": L.R_ETAT_PATCH,
    "ENTREE_SAUVEE": L.R_ENTREE_SAUVEE, "CS": L.R_CS,
    "CURSEUR": L.R_CURSEUR, "ARENE": L.ARENE_BASE,
}

RE_ETIQUETTE = re.compile(r"^\s*\.(\w+)\s*:\s*$")
RE_OPERANDE_ETIQUETTE = re.compile(r"^(j\w+|loop\w*|call)\s+\.(\w+)$")
RE_OPERANDE_SYMBOLE = re.compile(r"^(call)\s+(\w+)$")
RE_RIP_SYMBOLE = re.compile(r"^(.*?\[rip\s*\+\s*)(\w+)(\s*\].*)$")


class ErreurAuteur(Exception):
    pass


def lire_brouillon(chemin: str):
    instructions, etiquettes_lignes = [], []
    with open(chemin, encoding="utf-8") as f:
        for numero, brut in enumerate(f.read().splitlines(), 1):
            ligne = brut.split(";")[0].strip()
            if not ligne:
                continue
            m = RE_ETIQUETTE.match(ligne)
            if m:
                etiquettes_lignes.append((m.group(1), len(instructions)))
                continue
            instructions.append((ligne, numero))
    return instructions, etiquettes_lignes


def taille_ligne(ks: Ks, ligne: str, adresse: int, etiquettes: dict, base: int) -> int:
    enc, _ = ks.asm(substituer(ligne, adresse, etiquettes, base, taille=True), adresse)
    if not enc:
        raise ErreurAuteur(f"ligne inassemblable (calcul de taille) : {ligne!r}")
    return len(enc)


def substituer(ligne: str, adresse: int, etiquettes: dict, base: int, taille: int = 0) -> str:
    m = RE_OPERANDE_ETIQUETTE.match(ligne)
    if m:
        mnemo, nom = m.groups()
        cible = etiquettes.get(nom)
        if cible is None:
            raise ErreurAuteur(f"étiquette inconnue : .{nom}")
        return f"{mnemo} 0x{cible:x}"
    m = RE_OPERANDE_SYMBOLE.match(ligne)
    if m:
        mnemo, nom = m.groups()
        if nom not in SYMBOLES:
            raise ErreurAuteur(f"symbole de bloc inconnu : {nom}")
        return f"{mnemo} 0x{SYMBOLES[nom]:x}"
    m = RE_RIP_SYMBOLE.match(ligne)
    if m:
        avant, nom, apres = m.groups()
        if nom not in SYMBOLES:
            raise ErreurAuteur(f"symbole de données inconnu : {nom}")
        return f"{avant}0x0{apres}" if taille else ligne
    return ligne


def resoudre_rip(ligne: str, adresse: int, taille: int) -> str:
    m = RE_RIP_SYMBOLE.match(ligne)
    if not m:
        return ligne
    avant, nom, apres = m.groups()
    if nom not in SYMBOLES:
        raise ErreurAuteur(f"symbole de données inconnu : {nom}")
    cible = SYMBOLES[nom]
    disp = cible - (adresse + taille)
    if disp >= 0:
        return f"{avant}0x{disp:x}{apres}"
    base = avant[:avant.rindex("+")].rstrip()
    return f"{base} - 0x{-disp:x}{apres}"


def resoudre_bloc(ks: Ks, fichier: str, bid: str, spec: str, rva: int, slot: int, deps: str):
    chemin = os.path.join(BROUILLONS, fichier + ".asm")
    instructions, etiquettes_lignes = lire_brouillon(chemin)
    if not instructions:
        raise ErreurAuteur(f"{fichier} : brouillon vide")

    etiquettes = {nom: rva + 0x800 for nom, _ in etiquettes_lignes}
    for _ in range(4):
        tailles, adresse = [], rva
        for ligne, _ in instructions:
            t = taille_ligne(ks, ligne, adresse, etiquettes, rva)
            tailles.append(t)
            adresse += t
        nouvelles = {}
        for nom, index in etiquettes_lignes:
            nouvelles[nom] = rva + sum(tailles[:index])
        if nouvelles == etiquettes:
            break
        etiquettes = nouvelles
    else:
        raise ErreurAuteur(f"{fichier} : pas de point fixe en 4 passes")

    lignes_sortie, adresse, calculs = [], rva, []
    for ligne, numero in instructions:
        taille = tailles[len(lignes_sortie)]
        explicite = resoudre_rip(
            substituer(ligne, adresse, etiquettes, rva), adresse, taille)
        lignes_sortie.append((explicite, adresse, taille, numero))
        adresse += taille
    total = adresse - rva
    if total > slot:
        raise ErreurAuteur(f"{fichier} : {total} o > slot {slot:#x} (D8)")
    if slot - total < 16:
        raise ErreurAuteur(f"{fichier} : padding {slot - total} < 16 (D8)")

    entete = [
        f"; {fichier} · bloc {NOMS_COURTS.get(fichier, fichier)} · spec {spec} · bloc carte {bid}",
        f"; Profil : x86-64-win11-pe · ABI msx64 · slot RVA 0x{rva:x}, taille {slot} octets",
        f"; Dépendances : {deps}",
        f"; Notation explicite générée par outils/auteur.py depuis brouillons/{fichier}.asm",
        f"; (outil d'arithmétique d'adresses de l'auteur — keystone assemble, rien d'autre)",
        f"; Code : {total} o · padding : {slot - total} o (NOP)",
    ]
    if etiquettes_lignes:
        entete.append("; Étiquettes résolues : " + ", ".join(
            f".{nom}=0x{etiquettes[nom]:x}" for nom, _ in etiquettes_lignes))
    refs = [l for l, *_ in lignes_sortie if "[rip" in l]
    if refs:
        entete.append("; Déplacements RIP (cible = adresse + taille + disp) :")
        for ligne_e, adr, t, _ in lignes_sortie:
            m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", ligne_e)
            if m:
                cible = adr + t + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16))
                entete.append(f";   0x{adr:x} + 0x{t:x} {m.group(1)} {m.group(2)} = 0x{cible:x}")

    chemin_sortie = os.path.join(SORTIE, fichier + ".asm")
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(entete) + "\n")
        for ligne_e, *_ in lignes_sortie:
            f.write(ligne_e + "\n")
    return total, len(instructions), len(etiquettes_lignes)


NOMS_COURTS = {
    "tcp-01-init": "initialisation serveur TCP",
    "tcp-02-accept": "acceptation d'une connexion",
    "tcp-03-recv": "réception d'octets",
    "tcp-04-send": "émission d'octets",
    "tcp-05-close": "fermeture de socket",
    "tcp-06-spawn": "lancement de thread",
    "tcp-07-patch": "moteur de patch à chaud",
    "tcp-08-echo": "écho v1 — transformation identité (cible)",
    "tcp-08-echo-v2": "écho v2 — transformation majuscules (remplaçant)",
    "tcp-09-conn": "thread par connexion",
    "tcp-10-console": "thread console",
    "tcp-11-journal": "ligne de journal console",
    "tcp-12-main": "orchestration serveur (point d'entrée)",
    "libc-09-zone-alloc-ts": "allocateur par zone thread-safe",
}


def main(verifier_seulement: bool) -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    print("=== outils/auteur.py : résolution des étiquettes (jalon M2) ===")
    for fichier, bid, spec, rva, slot, deps in BLOCS:
        chemin = os.path.join(BROUILLONS, fichier + ".asm")
        if not os.path.exists(chemin):
            print(f"[absent] {fichier} : brouillon absent, ignoré (attendu selon la phase)")
            continue
        total, n, e = resoudre_bloc(ks, fichier, bid, spec, rva, slot, deps)
        print(f"[ok] {fichier} ({bid}) : {total} o, {n} instructions, "
              f"{e} étiquettes, {slot - total} o de padding")
    if not verifier_seulement:
        print("Notation explicite écrite dans notation/*.asm")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verifier-seulement" in sys.argv))
