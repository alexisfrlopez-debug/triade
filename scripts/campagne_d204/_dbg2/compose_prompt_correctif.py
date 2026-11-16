#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_correctif.py — assemble le prompt de la phase correctif :
le brouillon FAUTIF + LES DÉFAUTS NOMMÉS PAR LE LABO (le build et l'audit,
D1-D13) + les faits du plan (les mêmes que la phase notation). Le modèle
corrige — le coût est la mesure."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent

prompt = """Tu es l'auteur du domaine Loupe au laboratoire TRIADE. Ton brouillon du bloc
loupe-01 · ouvrir (ci-dessous) a été soumis au build du labo : le build a
REFUSÉ, et la revue du labo a nommé TREIZE défauts (la liste suit). Corrige
LE BROUILLON COMPLET : reprends-le, défaut par défaut, et produis LE
BROUILLON CORRIGÉ ENTIER (pas un diff — le brouillon complet, prêt pour
l'outil auteur).

================================================================================
LES DÉFAUTS NOMMÉS (le build + la revue du labo — D1 à D13)
================================================================================

"""

defauts = pathlib.Path(UNITE, "defauts-nommes-labo.txt").read_text(encoding="utf-8")

brouillon = ("\n\n" + "=" * 80 + "\n"
             "TON BROUILLON FAUTIF (tel que soumis au build)\n"
             + "=" * 80 + "\n\n"
             + pathlib.Path(UNITE, "brouillons", "loupe-01-ouvrir.asm").read_text(
                 encoding="utf-8"))

faits = ("\n\n" + "=" * 80 + "\n"
         + "RAPPEL — LES FAITS DU PLAN ET LE FORMAT (les mêmes qu'à la phase "
           "notation)\n"
         + "=" * 80 + "\n"
         + pathlib.Path(UNITE, "prompts", "notation.txt").read_text(
             encoding="utf-8").split(
             "LES FAITS DU PLAN (loupe/layout.py")[1].join(
             ["LES FAITS DU PLAN (loupe/layout.py", ""]))

consigne = """

================================================================================
LA CONSIGNE : produis LE BROUILLON CORRIGÉ ENTIER. Chaque défaut D1-D13
corrigé ; l'ordre du geste du plan respecté (E4 d'abord, LOUPE04, CreateFileW
avec ses SEPT arguments dont les trois à [rsp+0x20+], GetFileSizeEx, la
borne 2 Gio (CloseHandle puis LOUPE04 puis -3), la mesure du chemin (260
sans NUL → CloseHandle, LOUPE04, -5), la copie LIBC01 (r8+2 octets, source
r12), LOUPE02 si taille > 0 PUIS LOUPE07 toujours, le refus d'un appelé
(verdict SAUVÉ, LOUPE03, verdict remonté), le succès rax = 0. Le cadre de
pile : cinq push (rbx, r12-r15 si utilisés) + sub rsp, 0x40 — l'alignement
rsp ≡ 0 (mod 16) à chaque appel IAT, les non-volatils rendus.

Réponds par le BROUILLON SEUL : les lignes « ; » d'en-tête (tes corrections
nommées D1-D13 en commentaires), puis les instructions. AUCUN texte avant
ou après, AUCUN bloc markdown.
"""

sortie = pathlib.Path(UNITE, "prompts", "correctif-1.txt")
sortie.write_text(prompt + defauts + brouillon + faits + consigne,
                  encoding="utf-8")
print(f"[prompt] {sortie} : {sortie.stat().st_size} o")
