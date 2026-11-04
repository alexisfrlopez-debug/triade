#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d156.py — DECISIONS.md : insère la décision D156 PAR SCRIPT à la
suite de D155 (append-only, pas de rétrodatage — le contrat D24)."""

import sys

CHEMIN = "docs/DECISIONS.md"

D156 = """
## D156 — LA FENÊTRE D'UNE ZONE SE POSE À SA PORTÉE (l'ancre .bss vit AU CENTRE de la zone, jamais à sa base : la portée imm12 est une CONTRAINTE DE PLACE du plan — un accès hors plage est un REFUS NOMMÉ de l'assembleur, jamais un adressage absolu de repli) ; UN REGISTRE EST DÉDIÉ PAR RÔLE, JAMAIS RECYCLÉ (la fenêtre s3 de tcp-07 n'est pas l'ardoise de tcp-11 : l'oracle structurel attrape le recyclage au premier passage) ; L'AMO ADRESSE [rs1] SANS DÉPLACEMENT (le champ imm12 n'existe pas dans le format AMO — une demande de déplacement est un REFUS NOMMÉ, jamais un octet silencieux : le déplacement vit dans la formation addi, déclarée) ; LA PORTE S'ÉTEND AVEC L'INSTRUMENT (l'extension A du profil entre à la porte du jalon au geste qui l'exige : la couverture se démontre, elle ne se décrète pas)

**Le constat qui fonde la décision (05/11/2026, chantier M7-(b), Entrée 152 — le corpus paritaire RV64, la TROISIÈME instanciation de la même couche I).** Quatre leçons du geste, toutes attrapées par les gardes au PREMIER passage (aucune corrigée à la main : l'instrument a tranché, la notation a suivi) : (1) **LA LEÇON imm12** — le verrou du journal (0x3800) vu de l'ancre .bss posée à la BASE de la zone (0x3000) vit à +0x800 = 2048 : HORS imm12 DE UN — le premier `amoswap.d t2, t0, 0x800(s2)` a rendu le REFUS NOMMÉ d'as_rv64 (« hors plage imm12 [-2048, 2047] — l'accès lointain passe par une ancre ») ; la fenêtre s'est posée AU CENTRE de la zone (s2 = base + 0x3400) : le curseur à -0x400, l'arène à -0x3C0, le verrou à +0x400 — tout dans ±2047 ; (2) **LE PIÈGE AMO** — l'ISA AMO adresse [rs1] SANS déplacement (funct5 occupe les bits 31:27, il n'y a PAS de champ imm12 dans ce format) : le premier jet de l'extension assemblait `amoswap.d rd, rs2, 0x400(s2)` en IGNORANT silencieusement le déplacement demandé (l'espèce la plus grave : un octet qui n'est pas celui demandé, sans le dire) — le refus a été posé (AMO sans déplacement ; le déplacement vit dans la formation `addi t2, s2, 0x400`, déclarée et vérifiée) ; (3) **LE RECYCLAGE DE REGISTRE** — s3 portait la fenêtre d'entrée de tcp-07 ET l'arithmétique de longueur de tcp-11 (`addi s3, s3, 4`) : l'oracle structurel a refusé la formation non déclarée (`s3+4 hors données déclarées`) — les rôles ont été dédiés (s1/s2 les fenêtres GLOBALES du corpus, s3 la fenêtre PRIVÉE de tcp-07, s0/s4-s7 les ardoises de travail sauvegardées, t1 le registre du projet, jamais touché) ; (4) **LA PORTE A GRANDI AVEC L'INSTRUMENT** — l'extension A du profil (amoswap.w/d, aq/rl nuls — le verrou tournant du corpus) est entrée dans as_rv64 ET dans la porte du jalon (AVANT 783 → 791 textes, INVERSE 1037 → 1045 encodages) : le claim « la porte couvre l'espace d'encodage légal du profil » est resté VRAI par le geste, pas par décret — les autres AMO (amoadd…) et aq/rl armés vivent hors instrument, la frontière est nommée.

**La règle.** (1) TOUTE fenêtre d'ancrage (paire auipc+addi) est une DÉCLARATION DE PLAN dont la PLACE est contrainte par la portée imm12 : le plan choisit le centre qui couvre la zone (tout déplacement dans ±2047), et la contrainte est PORTEE PAR LE PLAN (documentée au layout, mesurée par l'oracle) — un accès hors plage est un refus nommé de l'assembleur, JAMAIS contourné par un adressage absolu de repli (qui tuerait l'indifférence à la base, la propriété du profil). (2) Les registres sont DÉDIÉS PAR RÔLE dans la lignée : les fenêtres (s1/s2 globales, s3 privée à tcp-07) ne sont jamais des ardoises de travail — les ardoises vivent dans les autres non volatils (s0, s4-s11), sauvegardées dans le cadre ; le recyclage est attrapé par l'oracle structurel (la formation non déclarée), pas par la relecture. (3) Toute EXTENSION de l'instrument (une instruction, un format, une ISA-extension) entre AVEC sa couverture : la porte du jalon est étendue au MÊME geste (les deux directions), et le domaine exclu est NOMMÉ (frontière, jamais un silence) ; une extension qui ne passe pas la porte n'entre pas. (4) Un format d'encodage dont un champ N'EXISTE PAS (AMO sans imm12) REFUSE la demande du champ — jamais un octet silencieux : la valeur appartient à une formation déclarée ailleurs.

**Alternatives rejetées.** Poser l'ancre .bss à la base de la zone et étendre par des calculs absolus (rejeté : l'adressage absolu tuerait la position-indépendance — la fenêtre est le mécanisme du profil) ; tolérer le déplacement AMO en l'ignorant (rejeté : le premier jet l'a fait — c'est un octet qui n'est pas celui demandé, l'espèce la plus grave) ; recycler s3 entre la fenêtre et l'ardoise (rejeté : l'oracle l'a attrapé — les rôles dédiés se vérifient, ils ne se souviennent pas) ; étendre l'assembleur sans étendre la porte (rejeté : la couverture se démontre — 791 + 1045 aux DEUX directions, le claim sinon serait un décret) ; passer les autres AMO sous silence (rejeté : la frontière est nommée — amoswap seul, aq/rl nuls, le corpus n'en porte aucun autre).

**Frontières.** La règle régit les plans d'adressage des lignées RV64 (la place des fenêtres), la dédicace des registres (frag-con la porte), les extensions de l'instrument (la porte grandit avec le domaine) et les formats d'encodage à champs absents (le refus nommé) ; elle ne touche NI le mécanisme des paires (D155/C1 : le site et le LO relativement à SON auipc — inchangés), NI la garde anti-table-x86 (D149 : asm-generic, la parité est sémantique), NI le scellage (le contrôle D146 adapté à l'exécuteur viendra du chantier (c)). Le corpus paritaire RV64 (riscv/corpus, balise 0.8.0-dev.2, sha256 b34a7147…) est né sous ces règles : 12 blocs du patrimoine + corpus-13, la TROISIÈME instanciation de la même couche I (les MÊMES fichiers canoniques unix/I/ — chargés, jamais copiés), l'oracle qemu vert (rituel 6/6 les DEUX lignes octet pour octet, code 0 — la parité § 8.3 PAR EXÉCUTION ; bases forcées VERTES ; falsification 12/12 zéro silence), 1535 verrous structurels, la carte génération 1 au SIXIÈME sel.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (append-only, D24) --------------------------------
if "## D156" in texte:
    sys.exit("ECHEC : la décision D156 existe déjà")
i155 = texte.find("## D155")
if i155 < 0:
    sys.exit("ECHEC : D155 introuvable")

nouveau = texte.rstrip("\n") + "\n" + D156

# ordre recoupé : D155 < D156
j155 = nouveau.find("## D155")
j156 = nouveau.find("## D156")
if not (0 <= j155 < j156):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"D156 insérée ({len(D156)} caractères) — à la suite de D155, append-only")
