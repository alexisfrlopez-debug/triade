#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_162.py — JOURNAL_TRAVAIL.md : insère l'Entrée 162 PAR
SCRIPT (ordre 161<162<marqueur, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"

ENTREE = """## Entrée 162 — LE CHANTIER M8-(d) OUVERT ET SERVI : LE KIT TERRAIN DÉPOSÉ AU COFFRE /test (la suite annoncée au Task 79) — le scénario du VRAI ntdll écrit et recoupé (QUATRE temps : T0 le témoin, T1 la lecture par DEUX lecteurs indépendants, T2 LA TWIN — la même ligne par les DEUX chemins, T3 les gardes), l'épreuve de labo VERTE (recoup AST : 13 constantes du scénario == l'artefact/le plan, extraction vierge), la vague m8d posée (kit-m8d.zip md5 117eb10a… + LISEZMOI-m8d.txt), la vague m7d ARCHIVÉE (consommée : le run m7d vert, la finale 0.8.0 scellée), preuves-m8d/ NÉ — la finale 0.9.0 attend le geste du développeur

**Le scénario (m8/terrain/scenario-m8d.py — python SEUL, stdlib, aucun paquet, aucun réseau, aucun droit).** QUATRE temps, chaque constat tranché binaire : **T0 LE TÉMOIN** — l'empreinte de l'artefact ASSERTÉE avant tout geste (sha256 1492b0bc…, 44 544 o), l'environnement consigné (la version Windows, le Python, l'architecture — un Python 64 bits exigé, refus nommé sinon), le VRAI ntdll localisé (GetModuleHandleW — le SCÉNARIO est l'appelant : l'IAT lui est permise, la charte ne la lie qu'aux BLOCS) et son fichier haché (sha256 consigné), l'artefact CARTOGRAPHIÉ par LoadLibraryEx DONT_RESOLVE_DLL_REFERENCES (aucune entrée résolue, AUCUN point d'entrée appelé — le scénario est le CHARGEUR, jamais l'exécutant de l'artefact entier), les octets attendus constatés UN PAR UN avant tout appel (le trombone sys-01 49 89 CA 0F 05 C3 @0xA000, le span-nom @0x2EC0, la ligne 33 o @0x2ED0, la IA d'origine du slot WriteFile @0x20B8 pointant bien le nom — l'ancre R7 vérifiée SUR la table), LE GESTE DU CHARGEUR (le slot kernel32!WriteFile résolu par GetProcAddress et posé dans l'IAT — le seul, celui du CHEMIN A). **T1 LA LECTURE** — le VRAI ntdll lu par DEUX lecteurs INDÉPENDANTS : la marche EAT refaite en PYTHON (le miroir exact du contrat de sys-02 : la fenêtre e_lfanew [0x40, 0x400], le motif PE, le répertoire export, la marche BORNÉE par NumberOfNames, l'ordinal, la fonction) et le BLOC sys-02 appelé à son adresse scellée @0xA040 (ctypes, msx64) — LE MÊME SSN attendu des deux ; LE MOTIF CONFRONTÉ (4C 8B D1 B8 avant l'imm32 — les octets du stub consignés au témoin : un stub divergent — un hook — est un REFUS NOMMÉ, jamais un numéro extrait) ; un SECOND nom résolu (NtReadFile par un span Python : jamais un numéro en cache, les DEUX SSN distincts constatés) ; LA FALSIFICATION INVITÉE (un module minimal FORGÉ en mémoire — PE bien formé, EAT d'une entrée « NtWriteFile », stub CROCHETÉ B8 sans le mov r10 — sys-02 doit rendre -4 NOMMÉ : le refus du stub divergent DEMONTRÉ sur la machine réelle, pas seulement au harnais). **T2 LA TWIN** — LA MÊME LIGNE par les DEUX chemins : CHEMIN A hello-02 @0x1040 (le scellé M0) par l'IAT kernel32 (le slot résolu au T0) écrivant le fixture 33 o dans un fichier ; CHEMIN B sys-03 @0xA180 (la twin) par NtWriteFile EN SYSCALL DIRECT — zéro IAT, le SSN résolu AU GESTE MÊME par sys-02 interne — écrivant la même ligne dans un second fichier ; les DEUX sorties lues et comparées OCTET PAR OCTET au fixture (et entre elles). **T3 LES GARDES** — la base invalide (un tampon Python « PAS-UN-MODULE-PE ») : sys-03 rend -1 NOMMÉ (le verdict de résolution) et AUCUN syscall n'est émis — le fichier-témoin chemin-c demeure VIDE (la garde I5 constatée sur la machine réelle) ; l'intégrité : proxy.exe relu inchangé, l'entête et le stub du VRAI ntdll relus inchangés (I8 — le module lu n'est jamais touché), la cartographie libérée (FreeLibrary).

**L'épreuve de labo (scripts/assembler_kit_m8d.py — le labo NE PEUT PAS exécuter le scénario : Windows + VRAI ntdll exigés, le cœur même du chantier).** LE RECOUP PAR AST : les 13 constantes nommées du scénario (les adresses scellées R_HELLO02/R_SYS01/R_SYS02/R_SYS03/R_FIXTURE_*/R_IAT_WRITEFILE, les octets du trombone, les fixtures nom et ligne, le motif du stub, l'empreinte et la taille de l'artefact) relues PAR AST et CONFRONTÉES à l'artefact et au plan (m8/layout.py — la source unique) : AUCUN chiffre gravé de tête ; la compilation (py_compile) ; L'ÉPREUVE D'EXTRACTION VIERGE (le zip extrait dans un répertoire temporaire NEUF, les empreintes re-constatées, la structure exacte). VERT.

**Le dépôt (scripts/deposer_kit_m8d.py — modèle m7d, règle D143 : archivage par DÉPLACEMENT, jamais un jet).** La vague m7d CONSOMMÉE (le run m7d vert 16/16, le recoup labo 29/29, la finale 0.8.0 SCELLÉE — le jalon M7 franchi) ARCHIVÉE dans archives-livraisons/vagues-m7/ (kit-m7d.zip md5 4d17f3fa… + LISEZMOI-m7d.txt, déplacements PATCH, md5 constatés après) ; **preuves-m8d/ NÉ** au coffre avec son LISEZMOI-preuves.txt (les six pièces attendues : temoin-m8d.txt, journal, VERDICT, chemin-a-hello02.txt, chemin-b-sys03.txt, chemin-c-refus.txt [VIDE]) ; **LA VAGUE m8d POSÉE** à la racine : kit-m8d.zip (20 286 o, md5 117eb10aa7aba703d684f4329d0e3064, sha256 cc21cd855e537b56…, MATCH par relecture) + LISEZMOI-m8d.txt (le document du kit, lisible au coffre sans extraire) ; l'index LISEZMOI-archives-livraisons.txt mis à jour (la section m7d archivée + la vague courante m8d) ; la vérification : la racine porte la vague courante + les résidents (corriger-wsb.* de l'ère m5b ; signatures-I.txt [la remise CONSOMMÉE de la cérémonie de l'ère — la copie de référence vit au dépôt v06/sceau-I/]) + les réceptacles (preuves-m5b/m6/m7/m8d) + les salles d'archive — 11 entrées, rien jeté.

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES — la finale 0.9.0 attend le run terrain vert), l'artefact 0.9.0-dev.1 INTACT (le scénario ne l'écrit JAMAIS — lecture seule, relu inchangé au T3), le labo ne connaît toujours PAS le SSN du terrain (le scénario le résout SUR la machine du développeur, le témoin le consigne, le labo le recoupera SANS jamais le deviner), la carte ne voyage pas avec l'artefact (R1 — l'empreinte fait foi), le run est LE GESTE DU DÉVELOPPEUR (python scenario-m8d.py sur sa machine Windows — le LISEZMOI le sert). Livrables : m8/terrain/scenario-m8d.py + m8/terrain/LISEZMOI-m8d.txt, scripts/assembler_kit_m8d.py + scripts/deposer_kit_m8d.py, le kit au coffre /test (kit-m8d.zip + LISEZMOI + preuves-m8d/) ; consignations : la présente Entrée PAR SCRIPT, PLAN (la ligne (d) : le kit déposé), worklog +Task ID 80 ; scripts suivis : inserer_entree_162.py, assembler_kit_m8d.py, deposer_kit_m8d.py.

- SUITE : LE GESTE DU DÉVELOPPEUR (le run : python scenario-m8d.py sur la machine Windows — les pièces à renvoyer au coffre /test/preuves-m8d/) → LE RECOUP LABORATOIRE (sur pièces, D138/D145/D148 : l'empreinte du kit, le SSN cohérent avec la version Windows consignée, les DEUX lignes octet pour octet, le refus nommé au fichier VIDE) → SI VERT : LA FINALE 0.9.0 SCELLÉE (le jalon M8 franchi — le second chemin preuve : la même observable SANS un seul import, sur la machine du développeur).

"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Entrée 162" in texte:
    sys.exit("ECHEC : l'Entrée 162 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in texte:
    sys.exit("ECHEC : marqueur journal-des-builds introuvable")
i161 = texte.find("## Entrée 161")
if i161 < 0:
    sys.exit("ECHEC : l'Entrée 161 introuvable (l'ordre 161<162)")

nouveau = texte.replace(MARQUEUR, ENTREE + MARQUEUR, 1)

j161 = nouveau.find("## Entrée 161")
j162 = nouveau.find("## Entrée 162")
jm = nouveau.find(MARQUEUR)
if not (0 <= j161 < j162 < jm):
    sys.exit("ECHEC : l'ordre 161<162<marqueur n'est pas tenu "
             f"({j161}, {j162}, {jm})")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("Entrée 162 insérée (l'ordre 161<162<marqueur constaté)")
