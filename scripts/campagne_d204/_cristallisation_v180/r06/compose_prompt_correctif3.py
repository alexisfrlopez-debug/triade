#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_correctif3.py — le troisième tour : D18-D22 nommés."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent

prompt = """Tu es l'auteur du domaine Loupe au laboratoire TRIADE. Ton troisième
brouillon du bloc loupe-01 · ouvrir (ci-dessous) est presque droit : la
revue du labo nomme CINQ écarts restants — deux de syntaxe, deux de
logique, et UN qui n'aurait été vécu que sur le VRAI Windows (la classe
des défauts de terrain) :

D18 — « cmp qword [rbx + 528], -1 » : INASSEMBLABLE (vérifié au labo —
     keystone refuse la taille mémoire sans « ptr ») : la forme est
     « cmp qword ptr [rbx + 528], -1 ».

D19 — LE REFUS E4 SANS VERDICT : « jne .sortie » saute à l'épilogue sans
     poser le verdict — rax rendrait 0 (le harnais l'initialise ainsi),
     le refus -5 serait PERDU ; ton étiquette .verdict_deja_ouvert (mov
     eax, -5) existe et n'est JAMAIS atteinte : « jne
     .verdict_deja_ouvert ».

D20 — L'ORDRE DE LA SESSION INVERSÉ (encore) : le contrat Q4 : loupe-02
     D'ABORD (la fenêtre, SEULEMENT SI taille > 0) PUIS loupe-07 (le
     panneau, TOUjours). Ton édition appelle loupe-07 puis loupe-02 :
     ÉCHANGE les deux blocs — d'abord le test de taille et loupe-02,
     puis loupe-07 inconditionnel.

D21 — rcx SAUVÉ TROP TARD : « mov r12, rcx » vit APRÈS « call LOUPE04 » —
     or loupe-04 UTILISE rcx (il appelle libc-07 memset avec rcx = le
     cadre) : à ton « mov r12, rcx », le chemin est DÉJÀ PERDU, et
     CreateFileW recevra une valeur folle — TOUTES les ouvertures
     échoueraient. La forme : « mov r12, rcx » AVANT « call LOUPE04 »
     (juste après le test E4).

D22 — LE GABARIT hTemplateFile ÉCRIT SUR 4 OCTETS : « mov dword ptr
     [rsp + 0x30], 0 » ne pose que les 4 octets bas — les 4 octets HAUTS
     du 7e argument (un HANDLE, 64 bits) restent AU HASARD de la pile :
     l'émulation passerait, mais le VRAI Windows pourrait refuser
     l'ouverture sur un gabarit non nul — le défaut que seul le terrain
     aurait vécu. La forme : « mov qword ptr [rsp + 0x30], 0 » (les
     arguments 5 et 6 sont des DWORD : dword ptr demeure ; le 7e est un
     HANDLE : qword ptr).

================================================================================
TON TROISIÈME BROUILLON (les écarts D18-D22 à corriger)
================================================================================

"""

brouillon = pathlib.Path(UNITE, "brouillons", "loupe-01-ouvrir.asm").read_text(
    encoding="utf-8")

faits = pathlib.Path(UNITE, "prompts", "notation.txt").read_text(
    encoding="utf-8").split("LES FAITS DU PLAN (loupe/layout.py")
faits = "\nRAPPEL — LES FAITS DU PLAN ET LE FORMAT (phase notation)\n" \
        + "LES FAITS DU PLAN (loupe/layout.py" + faits[1]

consigne = """

================================================================================
LA CONSIGNE : produis LE BROUILLON CORRIGÉ ENTIER (quatrième édition) —
D18 à D22 corrigés, tout le reste DEMEURE tel quel (le prologue cinq push
+ sub rsp, 0x40, lea rbx [rip + CADRE], l'épilogue unique .sortie, jmp
.sortie pour chaque refus). Réponds par le BROUILLON SEUL : les lignes
« ; » d'en-tête, puis les instructions. AUCUN texte avant ou après,
AUCUN bloc markdown.
"""

sortie = pathlib.Path(UNITE, "prompts", "correctif-3.txt")
sortie.write_text(prompt + brouillon + faits + consigne, encoding="utf-8")
print(f"[prompt] {sortie} : {sortie.stat().st_size} o")
