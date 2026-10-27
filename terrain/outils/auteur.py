#!/usr/bin/env python3
"""auteur.py — Outil d'auteur du jalon terrain : résolution des étiquettes.

Même discipline qu'en M0/M1/M2/démo (aucun compilateur entre l'intention et
les octets : keystone assemble, rien d'autre) — arithmétique d'adresses de
l'auteur : étiquettes locales -> adresses absolues, symboles de blocs ->
cibles d'appels, symboles de données -> déplacements RIP, calculés depuis le
plan d'adressage terrain (terrain/layout.py, héritage M0/M1/M2/démo + zones
superviseur, D48).

Entrée : notation/brouillons/sup-*.asm. Sortie : notation/sup-*.asm —
notation explicite WYSIWYG, seule lue par build_terrain.py (round-trip R5).

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
    ("sup-01-principal", "f60001", "sup-01:R1", 0x1400, 0x40,
     "blocs sup-21, sup-02, win-03, io-02 exit @0x1080"),
    ("sup-02-fenetre", "f60002", "sup-02:R1", 0x1440, 0x180,
     "IAT user32 : RegisterClassExW, CreateWindowExW, LoadCursorW, MessageBoxW ; "
     "IAT kernel32 : GetModuleHandleW, GetLastError ; bloc win-05 (entrée trace) ; "
     "procédure win-04 @0x1640 ; chaînes UTF-16 + ASCII"),
    ("sup-21-horodatage", "f60021", "sup-21:R1", 0x1C40, 0x100,
     "IAT kernel32#3 : GetLocalTime ; bloc libc-01 memcpy ; "
     "état .data (TAMPON_NOM, TAMPON_AFF) ; chaîne S01_PREFIXE (zone données sup)"),
    ("sup-22-balaye", "f60022", "sup-22:R1", 0x1D40, 0xC0,
     "blocs libc-02 memcmp, libc-01 memcpy — pur, aucun état .data"),
    ("sup-11-journal", "f60011", "sup-11:R1", 0x1E00, 0x200,
     "IAT kernel32#2 : GetModuleFileNameA, CreateFileA, WriteFile (commune), "
     "FlushFileBuffers ; blocs libc-01/03/04 ; état .data (handle, tampons) ; "
     "TAMPON_NOM (.data, posé par sup-21)"),
    ("sup-09-scenario", "f60009", "sup-09:R1", 0x4C00, 0x200,
     "blocs win-05 (entrée trace), win-06 autotest, sup-33, sup-34, sup-35 ; "
     "lignes S00..S03/S90/S91 (zone données sup) ; TAMPON_AFF (.data)"),
    ("sup-31-lancer", "f60031", "sup-31:R1", 0x5200, 0x1C0,
     "IAT kernel32#3 : CreateProcessA, CreatePipe ; IAT kernel32#1/#2 : "
     "CloseHandle, GetModuleFileNameA ; état .data ETAT_SUP (HPROC, PID, TUYAU_*)"),
    ("sup-33-demo", "f60033", "sup-33:R1", 0x5400, 0x3C0,
     "IAT kernel32#3 : WaitForSingleObject, GetExitCodeProcess, "
     "TerminateProcess, Sleep ; IAT user32#2 : FindWindowW, FindWindowExW, "
     "SendMessageTimeoutW ; IAT kernel32#1 : CloseHandle ; blocs sup-31, "
     "sup-36, libc-02 ; chaînes S10..S16 + NOM_DEMO + CLASSE_DEMO + fixture "
     "finale (zones données)"),
    ("sup-34-proxy", "f60034", "sup-34:R1", 0x5800, 0x5C0,
     "IAT kernel32#3 : WaitForSingleObject, GetExitCodeProcess, "
     "TerminateProcess, PeekNamedPipe, Sleep, DeleteFileA ; IAT kernel32#2 : "
     "CreateFileA ; IAT kernel32#1 : CloseHandle, ReadFile, WriteFile ; "
     "blocs sup-31, sup-36, libc-01/02 ; chaînes S20..S28 + fixtures bannière/"
     "événements/arret + cmdlines curl (zones données)"),
    ("sup-35-envoi", "f60035", "sup-35:R1", 0x5E00, 0x4C0,
     "IAT kernel32#3 : WaitForSingleObject, GetExitCodeProcess, Sleep, "
     "DeleteFileA ; IAT kernel32#2 : CreateFileA ; IAT kernel32#1 : "
     "CloseHandle, ReadFile, WriteFile ; blocs sup-31, sup-22, sup-36, "
     "libc-01 ; chaînes S30..S36 + étiquettes + gabarits à marqueurs "
     "(zones données)"),
    ("sup-36-fichiers", "f60036", "sup-36:R1", 0x4E00, 0x1C0,
     "IAT kernel32#2 : CreateFileA ; IAT kernel32#1 : ReadFile, WriteFile, "
     "CloseHandle ; IAT kernel32#3 : DeleteFileA ; blocs libc-01/03 ; "
     "état .data (DIR_LONG, LU) ; BUF_CHEMIN/TAMPON_CMD"),
    ("sup-37-extraction", "f60037", "sup-37:R1", 0x6600, 0x400,
     "IAT kernel32#2 : CreateFileA ; IAT kernel32#1 : ReadFile, CloseHandle ; "
     "blocs libc-01/02/03, sup-36 (op 1 écrire / op 2 supprimer), win-05 "
     "(entrée trace) ; section .blob (BLOB_LONGUEURS/BLOB_DEMO/BLOB_PROXY/"
     "SLOT_JETONS) ; état .data (DIR_LONG, LU) ; TAMPON_CMD+ZONE_COMPO "
     "(relecture 512 o) ; lignes S04..S07 (zone données sup 3) ; "
     "NOM_DEMO/NOM_PROXY (.rdata), NOM_JETONS (zone données sup 2) ; "
     "entrée à mode @0x6600 : ecx 0 = extraire / 1 = nettoyer (D49)"),
]

SYMBOLES = {
    # blocs hérités scellés (octets M0/M1/M2/démo)
    "WRITE": 0x1040, "EXIT": 0x1080,
    "MEMCPY": 0x1100, "MEMCMP": 0x1180, "STRLEN": 0x1200, "ITOA": 0x1280,
    "TCP_SPAWN": 0x4300,
    "BOUCLE": 0x15C0, "PROCEDURE": 0x1640, "AUTOTEST": 0x1AC0,
    # blocs terrain
    "FENETRE": 0x1440, "HORODATAGE": 0x1C40, "BALAYEUR": 0x1D40,
    "JOURNAL_FICHIER": 0x1E00, "SCENARIO": 0x4C00, "LANCEUR": 0x5200,
    "TEST_DEMO": 0x5400, "TEST_PROXY": 0x5800, "TEST_ENVOI": 0x5E00,
    # entrées win-05 scellé (miroir écran + fichier, D37)
    "JOURNAL_TRACE": L.JOURNAL_TRACE, "JOURNAL_GUI": L.JOURNAL_GUI,
    # IAT (kernel32#1, #2, #3, user32, user32#2, gdi32)
    "IAT_GSH": L.IAT_SLOTS["GetStdHandle"], "IAT_CH": L.IAT_SLOTS["CloseHandle"],
    "IAT_WF": L.IAT_SLOTS["WriteFile"], "IAT_RF": L.IAT_SLOTS["ReadFile"],
    "IAT_GMH": L.IAT_SLOTS["GetModuleHandleW"],
    "IAT_GMFA": L.IAT_SLOTS["GetModuleFileNameA"],
    "IAT_CREATEFILE": L.IAT_SLOTS["CreateFileA"],
    "IAT_FLUSH": L.IAT_SLOTS["FlushFileBuffers"],
    "IAT_GLE": L.IAT_SLOTS["GetLastError"],
    "IAT_CREATEPROCESS": L.IAT_SLOTS["CreateProcessA"],
    "IAT_CREATEPIPE": L.IAT_SLOTS["CreatePipe"],
    "IAT_WAIT": L.IAT_SLOTS["WaitForSingleObject"],
    "IAT_EXITCODE": L.IAT_SLOTS["GetExitCodeProcess"],
    "IAT_TERMINATE": L.IAT_SLOTS["TerminateProcess"],
    "IAT_LOCALTIME": L.IAT_SLOTS["GetLocalTime"],
    "IAT_DELETEFILE": L.IAT_SLOTS["DeleteFileA"],
    "IAT_PEEKPIPE": L.IAT_SLOTS["PeekNamedPipe"],
    "IAT_SLEEP": L.IAT_SLOTS["Sleep"],
    "IAT_FINDWINDOW": L.IAT_SLOTS["FindWindowW"],
    "IAT_FINDWINDOWEX": L.IAT_SLOTS["FindWindowExW"],
    "IAT_SENDMSGTIMEOUT": L.IAT_SLOTS["SendMessageTimeoutW"],
    "IAT_LOADCURSOR": L.IAT_SLOTS["LoadCursorW"],
    "IAT_REGISTERCLASSEX": L.IAT_SLOTS["RegisterClassExW"],
    "IAT_CREATEWINDOW": L.IAT_SLOTS["CreateWindowExW"],
    "IAT_MESSAGEBOX": L.IAT_SLOTS["MessageBoxW"],
    # données .rdata scellées win-06
    "ANCRE": L.R_ANCRE, "TAB_SUM": L.R_TAB_SUM, "VERSION": L.R_VERSION,
    # état .data (héritage + terrain)
    "RCS": L.R_CS,
    "DRAPEAU_WORKER": L.DRAPEAU_WORKER,
    "HWND_PRINCIPAL": L.HWND_PRINCIPAL, "HWND_JOURNAL": L.HWND_JOURNAL,
    "HWND_BOUTON": L.HWND_BOUTON,
    "JOURNAL_HANDLE": L.R_JOURNAL_HANDLE, "BUF_CONV": L.BUF_CONV,
    "BUF_CHEMIN": L.BUF_CHEMIN, "SCRATCH_ECRIT": L.SCRATCH_ECRIT,
    "BUF_MIROIR": L.BUF_MIROIR,
    "TAMPON_NOM": L.TAMPON_NOM, "TAMPON_AFF": L.TAMPON_AFF,
    "TAMPON_JETON": L.TAMPON_JETON, "TAMPON_CMD": L.TAMPON_CMD,
    "HPROC": L.HPROC, "PID": L.PID, "HPROC_PROXY": L.DRAPEAU_SRV,
    "TUYAU_IN_RD": L.TUYAU_IN_RD, "TUYAU_IN_WR": L.TUYAU_IN_WR,
    "TUYAU_OUT_RD": L.TUYAU_OUT_RD, "TUYAU_OUT_WR": L.TUYAU_OUT_WR,
    "HWND_DEMO": L.HWND_DEMO, "HWND_BTN_DEMO": L.HWND_BTN_DEMO,
    "CODE_SORTIE": L.CODE_SORTIE, "LU": L.LU, "DISPO": L.DISPO,
    "DIR_LONG": L.DIR_LONG,
    "TAMPON_COMPO": L.TAMPON_CMD + L.ZONE_COMPO,
    "FICHIERS": 0x4E00,
    "EXTRACTION": L.EXTRACTION, "NETTOYAGE": L.NETTOYAGE,
    "BLOB_LONGUEURS": L.BLOB_LONGUEURS, "BLOB_LONGUEUR_PROXY": L.BLOB_LONGUEUR_PROXY,
    "BLOB_DEMO": L.BLOB_DEMO, "BLOB_PROXY": L.BLOB_PROXY, "SLOT_JETONS": L.SLOT_JETONS,
}
for _nom, (_adr, _txt, _n) in L.CHAINES_UTF16.items():
    SYMBOLES[_nom] = _adr
for _nom, (_adr, _octets, _n) in L.CHAINES_ASCII.items():
    SYMBOLES[_nom] = _adr
for _nom, (_adr, _octets, _n) in L.CHAINES_SUP.items():
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
        f"; {fichier} · bloc terrain · spec {spec} · bloc carte {bid}",
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
    "sup-01-principal": "principal — point d'entrée (horodatage avant fenêtre)",
    "sup-02-fenetre": "fenêtre principale « TRIADE superviseur terrain »",
    "sup-21-horodatage": "horodatage du run (nom + ligne S01)",
    "sup-22-balaye": "balayeur d'extrait (étiquette -> valeur)",
    "sup-11-journal": "journal fichier horodaté (jumeau win-11, nom dynamique)",
    "sup-09-scenario": "scénario — orchestrateur T1/T2/T3 + verdict final",
    "sup-31-lancer": "lanceur de processus (CreateProcessA + tuyaux)",
    "sup-33-demo": "test T1 — démo M2 (fenêtre, clic, journal, verdict)",
    "sup-34-proxy": "test T2 — proxy M3 (tuyaux, curl, événements, arrêt)",
    "sup-35-envoi": "test T3 — envoi Drive (OAuth, session, téléversement)",
    "sup-36-fichiers": "fichiers du terrain (lire/écrire/supprimer, préfixe)",
}


def main(verifier_seulement: bool) -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    print("=== outils/auteur.py : résolution des étiquettes (jalon terrain) ===")
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
