#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controles_binaires.py — LES CONTRÔLES BINAIRES DU BRAS C (loupe-02 × C,
la campagne D204 — l'unité 2) : la DLL livrée, auditée AVANT le montage du
kit :
  1. le format : PE32+ DLL x86-64 (la cible du terrain) ;
  2. la table d'exports : loupe_01_ouvrir, loupe_02_lire, loupe_03_fermer
     (fonctions), cadre, journal et panneau (DONNÉES — les adresses du juge) ;
  3. la table d'imports KERNEL32 : les SIX feuilles de la pièce —
     SetFilePointerEx PRÉSENTE cette fois (la pièce la raconte à CHAQUE
     lecture : l'écart nommé du kit 01 n'existe plus) ;
  4. AUCUN appel CRT dans la clôture des fonctions de la pièce (les
     fonctions, leurs appelés internes ET les thunks d'import — tout
     __imp_ référencé ne peut être qu'une feuille kernel32 : le CRT
     n'est jamais initialisé sous DONT_RESOLVE) ;
  5. les relocations présentes (l'image peut être rebasée)."""
import pathlib
import re
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
OBJDUMP = ("/home/z/my-project/work/mingw-debs/root/usr/bin/"
           "x86_64-w64-mingw32-objdump")
DLL = ICI / "loupe-02-c.dll"

FEUILLES = {"__imp_CreateFileW", "__imp_GetFileSizeEx",
            "__imp_SetFilePointerEx", "__imp_ReadFile",
            "__imp_CloseHandle", "__imp_GetLastError"}

VERT, ROUGE = 0, 0


def verdit(nom, ok, detail=""):
    global VERT, ROUGE
    if ok:
        VERT += 1
        print(f"  VERT {nom}" + (f" — {detail}" if detail else ""))
    else:
        ROUGE += 1
        print(f"  ROUGE {nom}" + (f" — {detail}" if detail else ""))


def objdump(*args):
    r = subprocess.run([OBJDUMP, *args, str(DLL)], capture_output=True,
                       text=True)
    return r.stdout


def main() -> int:
    # --- 1. le format ---
    r = subprocess.run(["file", str(DLL)], capture_output=True, text=True)
    verdit("format:PE32+-DLL",
           "PE32+ executable for MS Windows" in r.stdout
           and "(DLL)" in r.stdout and "x86-64" in r.stdout,
           r.stdout.strip().split(": ", 1)[1])

    # --- 2. la table d'exports ---
    x = objdump("-x")
    noms_exports = re.findall(
        r"\[\s*\d+\] \+base\[\s*\d+\]\s+\w+\s+(\w+)\s*$", x, re.M)
    for symbole in ("loupe_01_ouvrir", "loupe_02_lire", "loupe_03_fermer",
                    "cadre", "journal", "panneau"):
        verdit(f"exports:{symbole}", symbole in noms_exports,
               f"à la table ({len(noms_exports)} exports)")
    m = re.search(r"Export Address Table -- Ordinal Base \d+\n.*?"
                  r"Ordinal  Address  Type\n((?:\t\[.*\n)+)", x, re.S)
    rvas = re.findall(r"\+base\[\s*\d+\] ([0-9a-f]+) Export RVA",
                      m.group(1)) if m else []
    # les noms par ordinal (la table des pointeurs de noms)
    paires = re.findall(r"\[\s*\d+\] \+base\[\s*\d+\]\s+\w+\s+(\w+)\s*$",
                        x, re.M)
    rva_par_nom = {nom: int(rvas[k], 16) for k, nom in enumerate(paires)
                   if k < len(rvas)}
    verdit("exports:donnees-en-.data",
           len(rvas) == 6
           and all(rva_par_nom.get(n, 0) >= 0x8000
                   for n in ("cadre", "journal", "panneau"))
           and all(rva_par_nom.get(n, 0) < 0x8000
                   for n in ("loupe_01_ouvrir", "loupe_02_lire",
                             "loupe_03_fermer")),
           f"cadre @{rva_par_nom.get('cadre', 0):#x}, journal "
           f"@{rva_par_nom.get('journal', 0):#x}, panneau "
           f"@{rva_par_nom.get('panneau', 0):#x} — les DONNÉES en .data ; "
           f"les TROIS fonctions en .text")

    # --- 3. les imports KERNEL32 ---
    m32 = re.search(r"DLL Name: KERNEL32\.dll\n(?:.*\n)*?(?=\n\s*DLL Name:|\n\n)",
                    x)
    noms32 = re.findall(r"^\s*[0-9a-f]+\s+<none>\s+\w+\s+(\w+)\s*$",
                        m32.group(0), re.M) if m32 else []
    for feuille in ("CreateFileW", "GetFileSizeEx", "SetFilePointerEx",
                    "ReadFile", "CloseHandle", "GetLastError"):
        verdit(f"imports:{feuille}", feuille in noms32,
               "résolue par le scénario à l'IAT réelle" if feuille in noms32
               else f"ABSENTE (kernel32 : {noms32})")
    verdit("imports:le-CRT-du-lanceur-nomme",
           any(n in noms32 for n in ("InitializeCriticalSection",
                                     "DeleteCriticalSection")),
           "les imports du CRT de lancement mingw (jamais appelées sous "
           "DONT_RESOLVE : aucun point d'entrée ne court) — nommé")

    # --- 4. AUCUN appel CRT dans la clôture des fonctions de la pièce ---
    d = objdump("-d")
    fonctions = {}
    for m in re.finditer(r"^[0-9a-f]+ <([\w.$@]+)>:\n((?:.*\n)+?)(?:\n|$)",
                         d, re.M):
        fonctions[m.group(1)] = m.group(2)
    adresses_k32 = {}
    for adresse, symbole in re.findall(
            r"# ([0-9a-f]+) <(__imp_\w+|__IAT_start__)>", d):
        if symbole == "__IAT_start__":
            adresses_k32[adresse] = "kernel32 (la première entrée)"
        else:
            adresses_k32[adresse] = symbole[len("__imp_"):]
    slots_k32 = {a for a, n in adresses_k32.items()
                 if n in noms32 or n.startswith("kernel32 (")}
    visites, pile = set(), ["loupe_01_ouvrir", "loupe_02_lire",
                            "loupe_03_fermer"]
    appels_imp = set()
    cibles_directes = set()
    while pile:
        f = pile.pop()
        if f in visites or f not in fonctions:
            continue
        visites.add(f)
        corps = fonctions[f]
        for imp in re.findall(r"<(__imp_\w+)>", corps):
            appels_imp.add(imp)
        for adr in re.findall(r"(?:call|jmp)\s+\*\w+\(%rip\)\s*#\s*"
                              r"([0-9a-f]+)", corps):
            cibles_directes.add(adr)
        for cible in re.findall(r"(?:call|jmp)\s+[0-9a-f]+ <([\w.$@]+)>",
                                corps):
            if cible not in visites:
                pile.append(cible)
    verdit("audit:cloture-des-fonctions", len(visites) >= 6,
           f"{len(visites)} fonctions dans la clôture de "
           f"loupe_01_ouvrir/loupe_02_lire/loupe_03_fermer (les fonctions, "
           f"leurs appelés, les thunks)")
    hors_k32 = sorted(a for a in cibles_directes if a not in slots_k32)
    verdit("audit:aucun-appel-CRT",
           appels_imp <= FEUILLES and not hors_k32,
           f"les __imp_ référencés : {sorted(appels_imp)} ; les appels "
           f"directs par l'IAT : {len(cibles_directes)}, tous aux slots "
           f"kernel32 — "
           f"{'QUE les feuilles kernel32 de la pièce' if appels_imp <= FEUILLES and not hors_k32 else 'UN APPEL CRT VIT ICI : ' + str(hors_k32)}")

    # --- 5. les relocations ---
    verdit("relocations:présentes",
           "Base Relocation Directory [.reloc]" in x or "HAS_RELOC" in x,
           "l'image peut être rebasée par le chargeur")

    print(f"\n=== CONTRÔLES BINAIRES : {VERT} VERT, {ROUGE} ROUGE ===")
    return 0 if ROUGE == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
