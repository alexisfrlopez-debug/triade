#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan ABI : registres volatiles relus après un appel sans rechargement.

Classe de défaut D38 (bouton invisible demo.3) : un registre caller-saved
(rax rcx rdx r8-r11) chargé avant un `call` et CONSULTÉ après sans rechargement
— légal en notation, mort en terrain réel (syscall détruit r11 par matériel).

Parcours linéaire des notations (le flux est linéaire : labels = sauts
conditionnels courts, conservateur ici). Toute lecture-source d'un volatile
dont le dernier événement est « call » est signalée ; toute réécriture
(destination) réinitialise l'état.
"""
import pathlib
import re

VOLATILES = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11",
             "eax", "ecx", "edx", "r8d", "r9d", "r10d", "r11d"}
REG64 = {r.replace("d", "") if r.endswith("d") else r for r in VOLATILES}

MOV = re.compile(r"^(mov|lea)\s+(%w),\s*(.+)$")
CALL_IAT = re.compile(r"^call\s+qword ptr \[rip")
CALL_DIR = re.compile(r"^call\s+0x[0-9a-f]+$")
JMP = re.compile(r"^(j\w+|jmp)\s+0x[0-9a-f]+$")
USE_SRC = re.compile(r"^(mov|add|sub|and|or|xor|cmp|test|lea|push|imul|shl|shr|sar|movzx|movsx|cdq|neg|not|inc|dec)\s+(.+?),\s*(.+)$|^(push)\s+(.+)$|^(cmp|test)\s+(.+?),\s*(.+)$")

def registres_dans(texte):
    """Noms de registres volatiles apparaissant comme TERMES SOURCE."""
    out = set()
    for reg in VOLATILES:
        if re.search(r"(?<![a-z0-9_])" + reg + r"(?![a-z0-9_])", texte):
            out.add(reg)
    return out


def scanner(fichier):
    alertes = []
    dernier = {}          # reg -> ("charge", n) | ("call", n)
    for n, brute in enumerate(fichier.read_text().splitlines(), 1):
        l = brute.split(";")[0].strip()
        if not l:
            continue
        if CALL_IAT.match(l) or CALL_DIR.match(l):
            for r in VOLATILES:
                dernier[r] = ("call", n)
            continue
        if JMP.match(l):
            # saut : les chemins fusionnent — on nettoie (conservateur)
            dernier = {}
            continue
        m = re.match(r"^(mov|lea|movzx|movsx|pop)\s+([\w\[\]\+ ]+?),\s*(.+)$", l)
        if m:
            dest, src = m.group(2).strip(), m.group(3).strip()
            # registres sources consultés
            for reg in registres_dans(src):
                etat = dernier.get(reg)
                if etat and etat[0] == "call":
                    alertes.append((n, l, reg, etat[1]))
            # destination : si dest est un volatile, il est rechargé
            for reg in VOLATILES:
                if re.search(r"(?<![a-z0-9_])" + reg + r"(?![a-z0-9_])", dest):
                    dernier[reg] = ("charge", n)
            continue
        # autres instructions binaires/unaires : sources consultées
        mm = re.match(r"^(\w+)\s+(.+)$", l)
        if mm:
            ops = mm.group(2)
            for reg in registres_dans(ops):
                etat = dernier.get(reg)
                if etat and etat[0] == "call":
                    alertes.append((n, l, reg, etat[1]))
            # toute écriture en destination (premier opérande) recharge
            prem = ops.split(",")[0].strip()
            for reg in VOLATILES:
                if re.search(r"(?<![a-z0-9_])" + reg + r"(?![a-z0-9_])", prem):
                    dernier[reg] = ("charge", n)
    return alertes


total = 0
for rep in ["demo/notation", "m2/notation", "m1/notation", "m6/notation",
            "m7/notation", "demo/notation/brouillons"]:
    d = pathlib.Path(rep)
    if not d.exists():
        continue
    for f in sorted(d.glob("*.asm")):
        alertes = scanner(f)
        if alertes:
            print(f"\n### {f}")
            for n, l, reg, ncall in alertes:
                print(f"  ligne {n}: « {l} » — {reg} lu après call ligne {ncall}")
            total += len(alertes)
print(f"\n=== {total} alerte(s) au total ===")
