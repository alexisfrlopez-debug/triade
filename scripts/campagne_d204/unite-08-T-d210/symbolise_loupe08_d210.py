#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""symbolise_loupe08_d210.py — LA SYMBOLISATION du final it8 vers le
brouillon de campagne (l'unité 02 D210, loupe-08 ligne × bras T) : les
déplacements explicites de l'atelier deviennent les SYMBOLES DU PLAN
que l'outil auteur résoudra (R_HEX = 0x2050) — le geste du partage
atelier/campagne consigné depuis l'unité 1 (loupe-02 : l'it5 explicite,
le brouillon symbolique CADRE/IAT_*/JOURNAL)."""
import pathlib

ATELIER = pathlib.Path(
    "/home/z/my-project/triade/lab/atelier-d210-p39uklsca/bras-T")
CAMPAGNE = pathlib.Path(
    "/home/z/my-project/triade/lab/repo2/scripts/campagne_d204/"
    "unite-08-T-d210/brouillons")

src = (ATELIER / "loupe-08-it8.asm").read_text(encoding="utf-8")

lignes, out = src.splitlines(), []
for l in lignes:
    s = l.strip()
    if s.startswith("```"):
        continue
    if s.startswith("section .text") or s.startswith("global loupe_08_ligne"):
        continue
    if s.startswith("LIGNE_TAILLE equ"):   # l'équ inutilisée, jamais au brouillon
        continue
    if s == "loupe_08_ligne:":   # l'étiquette d'entrée : jamais au brouillon
        continue                 # (RE_ETIQUETTE ne connaît que les locales)
    if "; loupe-08 · ligne · révision 1" in l or \
       "; ÉCRIT-AVANT-CODE" in l:
        continue
    # LE GESTE : le déplacement explicite de l'atelier → le symbole du plan
    l = l.replace("lea r11, [rip - 0x29b4]", "lea r11, [rip + HEX]")
    out.append(l)

entete = [
    "; loupe-08-ligne × bras T — la notation de campagne D210 (l'unité 02)",
    "; LA CONSTRUCTION PAR LA RIG : spec → notation → correctif 1 (SYNTAXE : la table",
    ";   au plan R_HEX par le lea, les formes ptr) → oracle-depuis-I → correctifs",
    ";   2-6 (le faisceau STRUCTUREL : le plan VOLATIL — les sept registres rax, rcx,",
    ";   rdx, r8, r9, r10, r11, aucun push, la pile jamais touchée ; les deux espaces ;",
    ";   le lea UNE fois ; l'extraction par les deux nibbles ; Q4 rax remis) — 100 %",
    ";   log-api au journal-tokens-d210.jsonl ; le geste MÉCANIQUE du labo nommé :",
    ";   la remappe bijective r12/r13/r14/r15 → r8/rdx/r9d/rax (la phase 1) et la",
    ";   normalisation de largeur cmp r9d, rdx → edx (la classe registre 32/64).",
    "; slot RVA 0x49C0, taille 320 octets · ABI msx64 · AUCUNE entrée IAT (la feuille",
    ";   pure) · la table hexa « 0123456789ABCDEF » du plan (R_HEX 0x2050, lea + HEX)",
]

(CAMPAGNE / "loupe-08-ligne.asm").write_text(
    "\n".join(entete + out) + "\n", encoding="utf-8")
print(f"[symbolisé] {CAMPAGNE / 'loupe-08-ligne.asm'} : "
      f"{len(out) + len(entete)} lignes")
