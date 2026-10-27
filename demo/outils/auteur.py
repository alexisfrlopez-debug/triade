#!/usr/bin/env python3
"""auteur.py — Outil d'auteur du jalon démo : résolution des étiquettes.

Même discipline qu'en M1/M2 (aucun compilateur entre l'intention et les octets :
keystone assemble, rien d'autre) — arithmétique d'adresses de l'auteur :
étiquettes locales -> adresses absolues, symboles de blocs -> cibles d'appels,
symboles de données -> déplacements RIP, calculés depuis le plan d'adressage
démo (demo/layout.py, héritage M2 + zones GUI).

Entrée : notation/brouillons/win-*.asm. Sortie : notation/win-*.asm — notation
explicite WYSIWYG, seule lue par build_demo.py (round-trip R5 sur la sortie).

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
    ("win-01-principal", "d40001", "win-01:R1", 0x1400, 0x40,
     "blocs win-02, win-03, io-02 exit @0x1080"),
    ("win-02-fenetre", "d40002", "win-02:R3", 0x1440, 0x180,
     "IAT user32 : RegisterClassExW, CreateWindowExW, LoadCursorW, MessageBoxW ; "
     "IAT kernel32 : GetModuleHandleW, GetLastError ; bloc win-05 (miroir "
     "écran+fichier, entrée trace) ; procédure @0x1640 ; chaînes UTF-16 + ASCII"),
    ("win-03-boucle", "d40003", "win-03:R1", 0x15C0, 0x80,
     "IAT user32 : GetMessageW, TranslateMessage, DispatchMessageW"),
    ("win-04-procedure", "d40004", "win-04:R4", 0x1640, 0x380,
     "IAT user32 : CreateWindowExW, SendMessageW, GetStockObject (gdi32), "
     "GetClientRect, MoveWindow, EnableWindow, DestroyWindow, PostQuitMessage, "
     "DefWindowProcW, GetModuleHandleW ; IAT kernel32 : CloseHandle, "
     "GetLastError ; bloc win-05 (miroir écran+fichier + diagnostics L4C/L4D) ; "
     "tcp-06 spawn @0x4300 ; scénario @0x4C00 ; état .data"),
    ("win-05-journal", "d40005", "win-05:R3", 0x5000, 0x200,
     "IAT user32 : SendMessageW ; blocs libc-03/04 ; bloc win-11 (miroir "
     "fichier) ; état .data (HWND_JOURNAL, BUF_MIROIR, BUF_CONV) ; deux "
     "entrées : scénario @0x5000 (force mode 2), trace @0x5008 (4 args)"),
    ("win-06-autotest", "d40006", "win-06:R1", 0x1AC0, 0x180,
     "blocs libc-01/02/03/04 ; table R10 + version + ancre .rdata ; fixtures"),
    ("win-07-client", "d40007", "win-07:R1", 0x1C40, 0xC0,
     "IAT ws2_32 : socket, connect, closesocket"),
    ("win-08-serveur", "d40008", "win-08:R2", 0x1D00, 0x100,
     "blocs tcp-01/02/06, win-05 (entrée trace, sondes S1/S2 D42) ; "
     "IAT kernel32 : CloseHandle ; état .data"),
    ("win-10-echange", "d40010", "win-10:R2", 0x4980, 0x180,
     "IAT ws2_32 : send, recv ; bloc libc-02 memcmp ; phrase .rdata ; "
     "win-05 (entrée trace, sondes 4/5 D42)"),
    ("win-09-scenario", "d40009", "win-09:R3", 0x4C00, 0x3C0,
     "blocs win-05/06/07/08, tcp-05/07, écho @0x4600, libc-02 ; "
     "IAT kernel32 : GetStdHandle, InitializeCriticalSection (D42 : init R_CS, "
     "le devoir de tcp-12), CloseHandle ; IAT ws2_32 : send, recv ; "
     "état .data + chaînes UTF-16 ; D40 : sondes trace mécanique "
     "(win-05 entrée trace, interstices .rdata)"),
    ("win-11-journal", "d40011", "win-11:R1", 0x1E00, 0x200,
     "IAT kernel32#2 : GetModuleFileNameA, CreateFileA, WriteFile (commune), "
     "FlushFileBuffers, GetLastError ; blocs libc-01/03/04 ; "
     "état .data (handle, tampons) ; NOM_FICHIER .rdata"),
]

SYMBOLES = {
    # blocs hérités (octets scellés M0/M1/M2)
    "WRITE": 0x1040, "EXIT": 0x1080,
    "MEMCPY": 0x1100, "MEMCMP": 0x1180, "STRLEN": 0x1200, "ITOA": 0x1280,
    "TCP_INIT": 0x4000, "TCP_ACCEPT": 0x4100, "TCP_RECV": 0x4140,
    "TCP_SEND": 0x4180, "TCP_CLOSE": 0x41C0, "TCP_SPAWN": 0x4300,
    "TCP_PATCH": 0x4400, "ECHO": 0x4600, "CONN": 0x4800,
    "TCP_JOURNAL": 0x4B00,
    # blocs démo
    "FENETRE": 0x1440, "BOUCLE": 0x15C0, "PROCEDURE": 0x1640,
    "JOURNAL_GUI": L.JOURNAL_GUI, "AUTOTEST": 0x1AC0, "CLIENT": 0x1C40,
    "SERVEUR": 0x1D00, "JOURNAL_FICHIER": 0x1E00, "SCENARIO": 0x4C00,
    "ECHANGE": 0x4980,
    # IAT (kernel32, kernel32#2, ws2_32, user32, gdi32)
    "IAT_GSH": L.IAT_SLOTS["GetStdHandle"], "IAT_CH": L.IAT_SLOTS["CloseHandle"],
    "IAT_GMH": L.IAT_SLOTS["GetModuleHandleW"],
    "IAT_WF": L.IAT_SLOTS["WriteFile"],
    "IAT_GMFA": L.IAT_SLOTS["GetModuleFileNameA"],
    "IAT_CREATEFILE": L.IAT_SLOTS["CreateFileA"],
    "IAT_FLUSH": L.IAT_SLOTS["FlushFileBuffers"],
    "IAT_GLE": L.IAT_SLOTS["GetLastError"],
    "IAT_SOCKET": L.IAT_SLOTS["socket"], "IAT_CONNECT": L.IAT_SLOTS["connect"],
    "IAT_CLOSESOCK": L.IAT_SLOTS["closesocket"],
    "IAT_SEND": L.IAT_SLOTS["send"], "IAT_RECV": L.IAT_SLOTS["recv"],
    "IAT_ICS": L.IAT_SLOTS["InitializeCriticalSection"],   # D42 : init R_CS
    "IAT_LOADCURSOR": L.IAT_SLOTS["LoadCursorW"],
    "IAT_REGISTERCLASSEX": L.IAT_SLOTS["RegisterClassExW"],
    "IAT_CREATEWINDOW": L.IAT_SLOTS["CreateWindowExW"],
    "IAT_MESSAGEBOX": L.IAT_SLOTS["MessageBoxW"],
    "IAT_GETMESSAGE": L.IAT_SLOTS["GetMessageW"],
    "IAT_TRANSLATE": L.IAT_SLOTS["TranslateMessage"],
    "IAT_DISPATCH": L.IAT_SLOTS["DispatchMessageW"],
    "IAT_POSTQUIT": L.IAT_SLOTS["PostQuitMessage"],
    "IAT_DESTROYWINDOW": L.IAT_SLOTS["DestroyWindow"],
    "IAT_SENDMESSAGE": L.IAT_SLOTS["SendMessageW"],
    "IAT_GETSTOCK": L.IAT_SLOTS["GetStockObject"],
    "IAT_GETCLIENTRECT": L.IAT_SLOTS["GetClientRect"],
    "IAT_MOVEWINDOW": L.IAT_SLOTS["MoveWindow"],
    "IAT_ENABLEWINDOW": L.IAT_SLOTS["EnableWindow"],
    "IAT_DEFWNDPROC": L.IAT_SLOTS["DefWindowProcW"],
    # données .rdata
    "ANCRE": L.R_ANCRE, "TAB_SUM": L.R_TAB_SUM, "VERSION": L.R_VERSION,
    "FIX_MEMCPY": 0x2630, "FIX_MEMCMP_A": 0x2640, "FIX_MEMCMP_B": 0x2644,
    "FIX_MEMCMP_C": 0x2648, "FIX_STRLEN": 0x264C, "FIX_ITOA": 0x265A,
    "PHRASE": L.R_PHRASE, "PHRASE_MAJ": L.R_PHRASE_MAJ,
    # état .data (héritage M2 + GUI + journal fichier D36)
    "STDOUT": L.R_STDOUT, "STDIN": L.R_STDIN, "LISTEN": L.R_LISTEN,
    "QUIT": L.R_QUIT, "ETAT_PATCH": L.R_ETAT_PATCH,
    "RCS": L.R_CS,   # D42 : section critique héritée M2 (P5 de tcp-11)
    "DRAPEAU_WORKER": L.DRAPEAU_WORKER, "DRAPEAU_SRV": L.DRAPEAU_SRV,
    "HWND_PRINCIPAL": L.HWND_PRINCIPAL, "HWND_JOURNAL": L.HWND_JOURNAL,
    "HWND_BOUTON": L.HWND_BOUTON,
    "JOURNAL_HANDLE": L.R_JOURNAL_HANDLE, "BUF_CONV": L.BUF_CONV,
    "BUF_CHEMIN": L.BUF_CHEMIN, "SCRATCH_ECRIT": L.SCRATCH_ECRIT,
    "BUF_MIROIR": L.BUF_MIROIR, "JOURNAL_TRACE": L.JOURNAL_TRACE,
}
for _nom, (_adr, _txt, _n) in L.CHAINES_UTF16.items():
    SYMBOLES[_nom] = _adr
for _nom, (_adr, _octets, _n) in L.CHAINES_ASCII.items():
    SYMBOLES[_nom] = _adr
for _nom, (_adr, _octets, _n) in L.CHAINES_SONDES.items():   # D40 : sondes R2
    SYMBOLES[_nom] = _adr

RE_ETIQUETTE = re.compile(r"^\s*\.(\w+)\s*:\s*$")
RE_OPERANDE_ETIQUETTE = re.compile(r"^(j\w+|loop\w*|call)\s+\.(\w+)$")
RE_OPERANDE_SYMBOLE = re.compile(r"^(call|jmp)\s+(\w+)$")
RE_RIP_SYMBOLE = re.compile(r"^(.*?\[rip\s*\+\s*)(\w+)(\s*\].*)$")
RE_LONGUEUR = re.compile(r"^mov\s+([er]\w+d?),\s+LEN_(\w+)$")


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
    m = RE_LONGUEUR.match(ligne)
    if m:
        reg, nom = m.groups()
        if nom not in L.LONGUEURS_ASCII:
            raise ErreurAuteur(f"symbole de longueur inconnu : LEN_{nom}")
        return f"mov {reg}, {L.LONGUEURS_ASCII[nom]}"
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
    for _ in range(16):
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
        raise ErreurAuteur(f"{fichier} : pas de point fixe en 16 passes")

    lignes_sortie, adresse = [], rva
    for ligne, _ in instructions:
        taille = tailles[len(lignes_sortie)]
        explicite = resoudre_rip(
            substituer(ligne, adresse, etiquettes, rva), adresse, taille)
        lignes_sortie.append((explicite, adresse, taille))
        adresse += taille
    total = adresse - rva
    if total > slot:
        raise ErreurAuteur(f"{fichier} : {total} o > slot {slot:#x} (D8)")
    if slot - total < 16:
        raise ErreurAuteur(f"{fichier} : padding {slot - total} < 16 (D8)")

    entete = [
        f"; {fichier} · bloc démo · spec {spec} · bloc carte {bid}",
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
        for ligne_e, adr, t in lignes_sortie:
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
    "win-01-principal": "principal — point d'entrée graphique",
    "win-02-fenetre": "fenêtre principale (classe + création + trace)",
    "win-03-boucle": "boucle de messages",
    "win-04-procedure": "procédure de fenêtre (géométrie corrigée D36)",
    "win-05-journal": "journal écran + fichier",
    "win-06-autotest": "autotest (porte R10 + vecteurs libc)",
    "win-07-client": "client TCP (connexion locale)",
    "win-08-serveur": "serveur d'acceptation (thread)",
    "win-09-scenario": "scénario complet (thread de démonstration)",
    "win-11-journal": "journal fichier (trace terrain D36)",
}


def main(verifier_seulement: bool) -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    print("=== outils/auteur.py : résolution des étiquettes (jalon démo) ===")
    for fichier, bid, spec, rva, slot, deps in BLOCS:
        chemin = os.path.join(BROUILLONS, fichier + ".asm")
        if not os.path.exists(chemin):
            raise ErreurAuteur(f"{fichier} : brouillon absent")
        total, n, e = resoudre_bloc(ks, fichier, bid, spec, rva, slot, deps)
        print(f"[ok] {fichier} ({bid}) : {total} o, {n} instructions, "
              f"{e} étiquettes, {slot - total} o de padding")
    if not verifier_seulement:
        print("Notation explicite écrite dans notation/*.asm")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verifier-seulement" in sys.argv))
