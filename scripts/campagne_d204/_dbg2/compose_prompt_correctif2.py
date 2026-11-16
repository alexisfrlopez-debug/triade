#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_correctif2.py — le second tour : les défauts D14-D17 nommés
par le build (le refus RÉSOLUTION-AUTEUR demeure) et la revue du labo."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent

prompt = """Tu es l'auteur du domaine Loupe au laboratoire TRIADE. Ton second brouillon
du bloc loupe-01 · ouvrir (ci-dessous) est ENCORE REFUSÉ par le build. La
revue du labo nomme QUATRE défauts RESTANTS — les voici, précis et
exigeables :

D14 — LES FORMES [rip + CADRE + offset] TOUJOURS PRÉSENTES (HUIT
     occurrences : « mov rbx, [rip + CADRE + 528] », « mov [rip + CADRE +
     528], rax », « lea rdx, [rip + CADRE + 520] », « mov rax, [rip +
     CADRE + 520] » ×2, « mov rcx, [rip + CADRE + 528] » ×3). L'outil
     auteur N'ACCEPTE PAS un offset après le symbole dans un déplacement
     RIP. LA FORME : poser la base UNE FOIS après le prologue —
     « lea rbx, [rip + CADRE] » — puis TOUT accès au cadre par
     « [rbx + offset] » (exemple : « mov rbx, [rbx + 528] » lit la
     poignée ; « mov [rbx + 528], rax » l'écrit ; « mov rax, [rbx + 520] »
     lit la taille ; « mov rcx, [rbx + 528] » charge la poignée pour
     CloseHandle). rbx est sauvé par le prologue : il vit jusqu'à
     l'épilogue.

D15 — L'ALIGNEMENT DE PILE FAUX : ton prologue « push rbx ; push r12 ;
     sub rsp, 0x30 » retire 64 octets — l'entrée ≡ 8 (mod 16) devient
     ≡ 8 (mod 16) : chaque appel IAT est PILE MISALIGNÉ (l'audit msx64
     refuse : le VRAI chargeur est SSE). LA FORME DE LA LIGNÉE : cinq
     push (« push rbx », « push r12 », « push r13 », « push r14 »,
     « push r15 ») puis « sub rsp, 0x40 » — 104 octets en tout, rsp ≡ 0
     (mod 16) à chaque appel, et la place des arguments 5+ existe.

D16 — r13 NON SAUVÉ : tu sauves le verdict de l'appelé dans r13 (non
     volatil) mais ton prologue ne pousse que rbx et r12 — r13 détruit,
     le sentinelle du harnais le nommera. Couvert par les CINQ push de
     D15 (r13 y vit).

D17 — LA SYNTAXE DES MOTS MÉMOIRE : « mov dword [rsp+0x20], 3 » est
     INASSEMBLABLE (keystone l'a refusé au labo — vérifié) : la forme
     exige « ptr » ET les espaces : « mov dword ptr [rsp + 0x20], 3 »
     (idem 0x28 et 0x30).

ET LA FORME DE L'ÉPILOGUE (la lignée) : UN SEUL point de sortie à
l'étiquette « .sortie: » — « add rsp, 0x40 ; pop r15 ; pop r14 ; pop
r13 ; pop r12 ; pop rbx ; ret ». Chaque chemin de refus pose son verdict
dans eax puis « jmp .sortie » (jamais six épilogues répétés — le bloc
est droit et économe : au plus 432 octets de code).

================================================================================
TON SECOND BROUILLON (les défauts D14-D17 à corriger)
================================================================================

"""

defauts_precedents = """
================================================================================
RAPPEL DES DÉFAUTS D1-D13 (déjà corrigés à ton second brouillon — ne les
réintroduis pas) : cmp rax, -1 pour CreateFileW ; les arguments 5-7 à
[rsp + 0x20/0x28/0x30] ; rcx sauvé en r12 AVANT call LOUPE04 ; word ptr ;
520 littéral ; LOUPE02 (si taille > 0) PUIS LOUPE07 (toujours) ; le verdict
de l'appelé SAUVÉ (r13) à travers call LOUPE03 ; le refus de GetFileSizeEx
ferme la poignée (CloseHandle puis LOUPE04 puis -6) ; jamais de push/pop
autour d'un appel ; la copie LIBC01 de r8 + 2 octets, source r12,
destination le cadre ; l'ordre E4 → LOUPE04 → CreateFileW → GetFileSizeEx →
borne → mesure → copie → session → retour.
================================================================================
"""

faits = pathlib.Path(UNITE, "prompts", "notation.txt").read_text(
    encoding="utf-8").split("LES FAITS DU PLAN (loupe/layout.py")
faits = "LES FAITS DU PLAN (loupe/layout.py" + faits[1]

brouillon = pathlib.Path(UNITE, "brouillons", "loupe-01-ouvrir.asm").read_text(
    encoding="utf-8")

consigne = """

================================================================================
LA CONSIGNE : produis LE BROUILLON CORRIGÉ ENTIER (troisième édition) —
D14 à D17 corrigés, la forme de la lignée tenue (cinq push + sub rsp, 0x40,
lea rbx [rip + CADRE] une fois, UN épilogue .sortie, chaque refus jmp
.sortie). Réponds par le BROUILLON SEUL : les lignes « ; » d'en-tête, puis
les instructions. AUCUN texte avant ou après, AUCUN bloc markdown.
"""

sortie = pathlib.Path(UNITE, "prompts", "correctif-2.txt")
sortie.write_text(prompt + brouillon + defauts_precedents + "\n" + faits
                  + consigne, encoding="utf-8")
print(f"[prompt] {sortie} : {sortie.stat().st_size} o")
