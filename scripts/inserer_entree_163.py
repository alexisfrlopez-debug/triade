#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_163.py — JOURNAL_TRAVAIL.md : insère l'Entrée 163 PAR
SCRIPT (ordre 162<163<marqueur, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"

ENTREE = """## Entrée 163 — LE KIT TERRAIN M8-(d) CORRIGÉ APRÈS LE PREMIER RUN DÉVELOPPEUR : le crash NOMMÉ (ligne 207 du scénario — l'assignation memoryview « different structures » : la tranche de 16 octets face à la valeur de 12, la LONGUEUR fait partie de la structure), la correction rétrécie à la longueur exacte (v[0x2A0:0x2AC] = le nom + son NUL — le motif déjà suivi par les voisins), le crash reproduit au labo (la MÊME ValueError, la même ligne), le kit réassemblé et rééprouvé (recoup AST 13 constantes, py_compile, extraction vierge), le contrat du forgé VÉRIFIÉ (la marche EAT trouve « NtWriteFile » au RVA 0x300, le motif ABSENT du stub crocheté → le refus -4 NOMMÉ attendu de sys-02), kit-m8d.zip MIS À JOUR EN PLACE au coffre /test (md5 117eb10a… → ad6cbffe… MATCH par relecture, l'original remplacé, le fichier conservé, rien jeté) — le geste du développeur peut REPRENDRE

**Le run du développeur (Windows 10.0 build 26300, Python 3.13.9 AMD64 — le 05/11).** T0 et T1 VERTS jusqu'à la falsification : l'empreinte de l'artefact MATCH (1492b0bc…, 44 544 o), le VRAI ntdll localisé (base consignée, sha256 du fichier consigné), la cartographie DONT_RESOLVE et les octets attendus constatés UN PAR UN (le trombone, les fixtures, le slot IAT résolu par le chargeur du scénario), la marche EAT en Python ET le bloc sys-02 D'ACCORD (NtWriteFile résolu, le motif 4C 8B D1 B8 confronté, le second nom NtReadFile résolu, les DEUX SSN distincts — jamais un numéro en cache) — puis le CRASH Python à la préparation de la falsification invitée : forger_module_crochete(), ligne 207, « ValueError: memoryview assignment: lvalue and rvalue have different structures ». Le run meurt AVANT T2 : AUCUN syscall émis, l'artefact INTACT (le crash est un refus de Python AVANT tout geste du forger — la preuve que le kit ne touche jamais rien qu'on ne lui demande pas).

**La cause racine, NOMMÉE sur pièces.** La ligne fautive écrivait le nom du forgé sur une tranche plus longue que la valeur : v[0x2A0:0x2B0] (16 octets) = b"NtWriteFile\\x00" (12 octets — 11 caractères + le NUL). L'assignation par tranche d'un memoryview exige la structure IDENTIQUE des deux côtés, et la LONGUEUR EST LA STRUCTURE (une tranche d'1-D 'B' a pour forme sa longueur) : 16 face à 12, c'est le refus « different structures » — JAMAIS un remplissage tacite, jamais une troncature silencieuse. La vue était pourtant saine (memoryview(create_string_buffer).cast("B") : format 'B', 1-D, 1 024 octets) : le défaut n'est PAS le format, c'est la FORME. Reproduit au labo à l'identique (Python 3.12 : la MÊME ValueError sur la MÊME ligne — le témoin bytearray confirme : c'est la règle, pas la machine).

**La correction (UNE ligne, le motif de la maison).** v[0x2A0:0x2AC] = b"NtWriteFile\\x00" — la tranche == la valeur, 12 octets exactement, comme les voisins l'ont toujours fait (MZ sur 2, « PE\\x00\\x00 » sur 4, le stub crocheté sur 5). Les 4 octets qui suivent (0x2AC..0x2AF) demeurent ZÉROS (le tampon naît nu : create_string_buffer) et la marche EAT ne lit QUE les 11 octets du span — le contrat du forger est inchangé. Le commentaire du correctif est PORTÉ PAR LA SOURCE (la règle nommée dans le code même).

**L'épreuve de labo rejouée (scripts/assembler_kit_m8d.py + scripts/verifier_m8d.py au labo).** LE RECOUP PAR AST : les 13 constantes du scénario == l'artefact/le plan (AUCUN chiffre gravé de tête — la correction ne touche AUCUNE constante) ; py_compile ; l'extraction vierge VERT ; ET le contrat du forgé vérifié SUR LE FICHIER LIVRÉ (import du scénario même, wintypes escamoté sous Linux) : forger_module_crochete() ne lève plus, le module relu UN PAR UN (MZ, e_lfanew 0x40, PE, magic 0x20B, export dir 0x200, NumberOfNames 1, noms[0] 0x2A0, fonctions[0] 0x300, le stub crocheté b8 44 33 22 11), la marche EAT (le miroir Python de sys-02) trouve « NtWriteFile » au stub RVA 0x300, confronter_stub rend le motif ABSENT — REFUS NOMMÉ : sur Windows, sys-02 rendra -4, exactement le verdict T1.falsification attendu. Vérifié AUSSI sur le script extrait du zip : la correction est DANS l'archive (zip == zone == dépôt, diff nul).

**Le dépôt corrigé (scripts/corriger_kit_m8d.py — modèle D143 adapté : MISE À JOUR EN PLACE, jamais un jet).** kit-m8d.zip du coffre /test portait l'original défectueux (md5 117eb10a…) : le contenu REMPLACÉ par le kit corrigé (20 410 o, md5 ad6cbffe…, sha256 3e777013…) PAR upload_update — le FICHIER même conservé (aucune entrée nouvelle à la racine, l'ancien scénario vit dans l'historique git), la relecture md5 MATCH (l'aller-retour), les résidents intacts (11 entrées : la vague courante, les réceptacles, les salles d'archive).

**Détail.** FRONTIÈRES : aucune balise ne bouge (la finale 0.9.0 attend TOUJOURS le vert du run terrain), l'artefact 0.9.0-dev.1 INTACT (le crash l'a précédé de part en part : lecture seule), le labo ne connaît toujours PAS le SSN du terrain (la sortie collée en conversation n'est pas une PIÈCE : le témoin temoin-m8d.txt reste la référence du recoup D138/D145/D148), la carte ne voyage pas (R1). Livrables : m8/terrain/scenario-m8d.py (la ligne corrigée + sa règle en commentaire), scripts/corriger_kit_m8d.py, le kit corrigé au coffre /test ; consignations : la présente Entrée PAR SCRIPT, worklog +Task ID 81 ; scripts suivis : inserer_entree_163.py, corriger_kit_m8d.py.

- SUITE : LE GESTE DU DÉVELOPPEUR REJOUE (re-télécharger kit-m8d.zip du coffre /test OU remplacer le seul scenario-m8d.py, puis python scenario-m8d.py — la sortie attendue : T1.falsification [ok] le stub crocheté REFUSÉ (-4), T2 LA TWIN, T3 LES GARDES, VERDICT VERT, les pièces au coffre /test/preuves-m8d/) → LE RECOUP LABORATOIRE (D138/D145/D148) → SI VERT : LA FINALE 0.9.0 SCELLÉE (le jalon M8 franchi).

"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Entrée 163" in texte:
    sys.exit("ECHEC : l'Entrée 163 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in texte:
    sys.exit("ECHEC : marqueur journal-des-builds introuvable")
i162 = texte.find("## Entrée 162")
if i162 < 0:
    sys.exit("ECHEC : l'Entrée 162 introuvable (l'ordre 162<163)")

nouveau = texte.replace(MARQUEUR, ENTREE + MARQUEUR, 1)

j162 = nouveau.find("## Entrée 162")
j163 = nouveau.find("## Entrée 163")
jm = nouveau.find(MARQUEUR)
if not (0 <= j162 < j163 < jm):
    sys.exit("ECHEC : l'ordre 162<163<marqueur n'est pas tenu "
             f"({j162}, {j163}, {jm})")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("Entrée 163 insérée (l'ordre 162<163<marqueur constaté)")
