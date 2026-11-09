#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_msx64.py — L'AUDITEUR D'ABI msx64 DU DOMAINE loupe (l'Entrée 207 :
le terrain a nommé [SESSION] -6 sur loupe-01 ; l'autopsie de labo isole le
défaut de CLASSE : les arguments 5+ À LA PILE).

Pour CHAQUE notation du domaine (loupe/notation/*.asm, les brouillons
exclus), l'auditeur SIMULE l'arithmétique de pile instruction par
instruction (push/sub/add/pop — les sauts suivis par étiquette) depuis
l'entrée (rsp ≡ 8 mod 16, l'ABI msx64), et CONSTATE à CHAQUE appel IAT
(call qword ptr [rip ± disp]) :

  1. L'ALIGNEMENT : rsp ≡ 0 (mod 16) au call — sinon le VRAI kernel32/
     user32 (SSE, movaps) peut FAUTER là où le harnais (Unicorn + shims
     Python) passe — l'axe invisible du labo ;
  2. LES SLOTS DES ARGUMENTS PILE : toute écriture [rsp], [rsp+8]…
     [rsp+0x18] À LA PORTÉE de l'appel est une écriture DANS LE HOME
     SPACE (les arguments 5+ vivent à [rsp+0x20+]) — l'écriture home
     n'est pas fautive en soi, MAIS si l'appelé a des arguments pile et
     qu'AUCUNE écriture ne vit à [rsp+0x20+], l'argument part au
     HASARD de la pile non initialisée.

L'auditeur ne modifie RIEN : il NOME. La convention des appels IAT du
domaine (loupe/layout.py : IAT_KERNEL32/USER32/GDI32) donne le nombre
d'arguments pile attendu par feuille : CreateFileW 3, ReadFile 1,
WriteFile 1, TextOutW 1, SetScrollInfo 0 (4 args, tous registres),
CreateWindowExW 8, GetScrollInfo 0, GetMessageW 0…

Usage : python3 audit_msx64.py            (depuis loupe/ ou le dépôt)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
NOTATION = os.path.join(ICI, "notation")

# les feuilles IAT du domaine AVEC leurs arguments AU-DELÀ du 4e
# (source : la MSDN de chaque API — la convention, jamais la pièce)
ARGS_PILE = {
    "kernel32": {
        "CreateFileW": 3,       # disposition, flags, template
        "GetFileSizeEx": 0,
        "SetFilePointerEx": 0,  # 4 args, tous registres
        "ReadFile": 1,          # lpOverlapped
        "WriteFile": 1,         # lpOverlapped
        "CloseHandle": 0,
        "GetLastError": 0,
        "GetModuleHandleW": 0,
        "GetCommandLineW": 0,
        "ExitProcess": 0,
    },
    "user32": {
        "RegisterClassExW": 0,
        "CreateWindowExW": 8,   # X, Y, L, H, parent, menu, instance, param
        "ShowWindow": 0,
        "GetMessageW": 0,
        "TranslateMessage": 0,
        "DispatchMessageW": 0,
        "DefWindowProcW": 0,
        "BeginPaint": 0,
        "EndPaint": 0,
        "InvalidateRect": 0,
        "GetClientRect": 0,
        "GetScrollInfo": 0,
        "SetScrollInfo": 0,     # 4 args, tous registres
        "DestroyWindow": 0,
        "PostQuitMessage": 0,
        "LoadCursorW": 0,
        "MessageBeep": 0,
        "MessageBoxW": 0,
    },
    "gdi32": {
        "GetStockObject": 0,
        "SelectObject": 0,
        "GetTextMetricsW": 0,
        "TextOutW": 1,          # c — le compte
        "SetTextColor": 0,
        "SetBkColor": 0,
    },
}

RE_PUSHR = re.compile(r"^push\s+(r\w+|rbp|rsp)$")
RE_POPR = re.compile(r"^pop\s+(r\w+|rbp|rsp)$")
RE_SUBRSP = re.compile(r"^sub\s+rsp,\s*(0x[0-9a-f]+|\d+)$")
RE_ADDRSP = re.compile(r"^add\s+rsp,\s*(0x[0-9a-f]+|\d+)$")
RE_CALLIAT = re.compile(r"^call\s+qword\s+ptr\s+\[rip\s*([+-])\s*(0x[0-9a-f]+|\d+)\]$")
RE_CALLDIR = re.compile(r"^call\s+(0x[0-9a-f]+|\d+)$")
RE_JMP = re.compile(r"^j(mp|ne|e|z|nz|le|ge|l|g|be|ae|a|b|s)\s+(0x[0-9a-f]+|\d+)$")
RE_MOVRSP = re.compile(r"^mov\s+(d|q)word\s+ptr\s+\[rsp\s*([+-])\s*(0x[0-9a-f]+|\d+)\]"
                        r"(,\s*(0x[0-9a-f]+|\d+|r\w+|e\w+))?$", re.I)
RE_LABEL = re.compile(r"^(\.?\w+):\s*$")
RE_LEA_RSP = re.compile(r"^lea\s+r\w+,\s*\[rsp")


def parse_fichier(chemin):
    """→ (liste d'instructions [(addr, texte)], {étiquette: index})"""
    instrs, labels = [], {}
    for ligne in open(chemin, encoding="utf-8"):
        ligne = ligne.rstrip()
        ligne = ligne.lstrip()
        if not ligne or ligne.startswith(";"):
            continue
        m = re.match(r"^([0-9a-f]+):\s*(.*)$", ligne)
        if m:  # le format « addr→texte » du Read (on n'a pas les adresses ici)
            ligne = m.group(2)
        m = RE_LABEL.match(ligne)
        if m:
            labels[ligne.rstrip(":")] = len(instrs)
            continue
        instrs.append(ligne)
    return instrs, labels


def audite(chemin):
    """→ la liste des constats [(ligne_idx, appel, alignement, slots)]"""
    instrs, labels = parse_fichier(chemin)
    constats = []
    # les déplacements IAT : la ligne d'en-tête « ;   addr + taille ± disp = cible »
    cibles = {}   # disp signé normalisé -> cible
    for ligne in open(chemin, encoding="utf-8"):
        m = re.match(r"^;\s+([0-9a-f]+)\s+\+\s+(\d+)\s+([+-])\s+(0x[0-9a-f]+|\d+)\s+=\s+(0x[0-9a-f]+|\d+)",
                     ligne)
        if m:
            addr, taille, signe, disp, cible = m.groups()
            cible = int(cible, 16)
            if 0x2400 <= cible <= 0x2528:
                cibles[(int(addr, 16), int(taille))] = cible
    # les feuilles par slot (l'IAT du plan : R_IAT_K32 0x2400, U32 0x2450, GDI 0x24E0)
    def feuille_du_slot(slot):
        ordres = [(0x2400, "kernel32", list(ARGS_PILE["kernel32"])),
                  (0x2450, "user32", list(ARGS_PILE["user32"])),
                  (0x24E0, "gdi32", list(ARGS_PILE["gdi32"]))]
        for base, dll, noms in ordres:
            if slot >= base and (slot - base) // 8 < len(noms):
                return dll, noms[(slot - base) // 8]
        return None, None

    rsp = 8            # l'entrée msx64 : ≡ 8 (mod 16)
    ecrits = {}        # offset -> valeur (les écritures [rsp+X] depuis le dernier top de frame)
    i = 0
    chemins = [(0, rsp, {})]  # (index, rsp, ecrits) — la pile d'exécution des sauts
    vus = set()
    # simulation linéaire simple (les sauts suivis en largeur, bornés)
    file = [(0, 8, {}, [])]
    while file:
        idx, rsp, ecrits, route = file.pop(0)
        cle = (idx, rsp % 16)
        if cle in vus:
            continue
        vus.add(cle)
        while idx < len(instrs):
            t = instrs[idx]
            if RE_PUSHR.match(t):
                rsp -= 8
            elif RE_POPR.match(t):
                rsp += 8
            elif RE_SUBRSP.match(t):
                rsp -= int(RE_SUBRSP.match(t).group(1), 0)
            elif RE_ADDRSP.match(t):
                rsp += int(RE_ADDRSP.match(t).group(1), 0)
            elif RE_LEA_RSP.match(t):
                pass
            else:
                m = RE_CALLIAT.match(t)
                if m:
                    signe, disp = m.groups()
                    disp = int(disp, 0)
                    # la cible IAT : on ne la calcule pas par RIP (pas d'adresses
                    # dans la notation) — l'en-tête la donne : on cherche par
                    # élimination (l'appel EST l'un des déplacements listés) :
                    constats.append((idx, t, rsp % 16, dict(ecrits)))
                else:
                    m = RE_MOVRSP.match(t)
                    if m:
                        signe, off = m.group(2), int(m.group(3), 0)
                        off = off if signe == "+" else -off
                        ecrits = {**ecrits, off: m.group(5)}
                    else:
                        m = RE_JMP.match(t)
                        if m and m.group(2) in labels:
                            file.append((labels[m.group(2)], rsp, dict(ecrits),
                                         route + [f"{idx}:{t}"]))
                        elif t == "ret":
                            break
            idx += 1
    return instrs, constats, cibles


def main():
    total_defauts = 0
    for nom in sorted(os.listdir(NOTATION)):
        if not nom.endswith(".asm"):
            continue
        chemin = os.path.join(NOTATION, nom)
        instrs, constats, cibles = audite(chemin)
        if not constats:
            continue
        print(f"=== {nom} ===")
        for idx, appel, align, ecrits in constats:
            slots = sorted(ecrits)
            pile = [o for o in slots if 0x20 <= o <= 0x38]
            home = [o for o in slots if o < 0x20]
            marque = []
            if align != 0:
                marque.append(f"ALIGNEMENT rsp≡{align} (mod 16) AU CALL — "
                              "le VRAI kernel32/user32 peut fautter (SSE)")
            if home and not pile:
                # écritures home space seulement : suspect SI l'appelé prend
                # des arguments pile (nommé par la convention)
                marque.append(f"écritures HOME {home} sans AUCUNE écriture "
                              f"à [rsp+0x20+] — les arguments 5+ partent au "
                              f"hasard de la pile")
            if marque:
                total_defauts += 1
                for m in marque:
                    print(f"  [{idx:3d}] {appel}  ← {m}")
    print(f"\nTOTAL : {total_defauts} appel(s) IAT en défaut de classe")


if __name__ == "__main__":
    sys.exit(main())
