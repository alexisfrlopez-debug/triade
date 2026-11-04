#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d155.py — DECISIONS.md : insère la décision D155 PAR SCRIPT à la
suite de D154 (append-only, pas de rétrodatage — le contrat D24)."""

import sys

CHEMIN = "docs/DECISIONS.md"

D155 = """
## D155 — LE MOTEUR DE NOTATION D'UN PROFIL NEUF PASSE LA MÊME PORTE QUE LE PRIMAIRE, ET LA PREUVE EST LA DIRECTION INVERSE (l'assembleur maison — ou tiers — n'est admis que si le rendu INTÉGRAL du juge ré-assemble en ses octets : le corpus de textes ne suffit JAMAIS, c'est l'espace d'ENCODAGE légal qui fait la preuve) ; LE JUGE DÉBORDE L'AUTEUR (le désassembleur rend plus de pseudos que l'auteur n'a d'habitudes — chaque écart attrapé par la porte est une leçon consignée, jamais un avertissement) ; UN EXÉCUTEUR ÉMULÉ SE PREUVE PAR SES PARAMÈTRES, JAMAIS PAR UN ASLR ÉMULÉ (la base d'une image PIE invitée sous qemu-user est CONSTANTE — un constat d'instrument NOMMÉ ; l'indifférence à la base se DÉMONTRE par des bases forcées du CHARGEUR, la preuve ne doit dépendre d'aucun aléa de l'instrument)

**Le constat qui fonde la décision (05/11/2026, chantier M7-(a), Entrée 150).** Trois constats du geste fondent la règle : (1) **LA DIRECTION INVERSE EST LA PREUVE** — la porte round-trip du jalon a été construite en deux directions : AVANT (783 textes du corpus du profil : assemble → désassemble → ré-assemble) et INVERSE (1037 encodages légaux de l'espace RV64IMA+Zifencei : champs f7/f3 exhaustifs, shamt exhaustifs, décalages de bord, les 225 couples de fence — le rendu du juge ré-assemble en ses octets) ; les QUATRE défauts de l'assembleur maison (le pseudo `negw` manquant, le funct7 de SEPT bits des décalages W, la forme deux-opérandes mémoire de `jalr`, la frontière « unknown » des champs fence vides) ont TOUS été attrapés par la direction inverse — aucun par la direction avant : un corpus de textes écrit par l'auteur ne prouve que ce que l'auteur a prévu ; (2) **LE JUGE DÉBORDE L'AUTEUR** — capstone rend `mv` pour addi imm=0, `sext.w` pour addiw imm=0, `beqz` pour beq rs2=x0, `jal` à UN opérande (ra implicite), `negw` pour subw x0 — la graphie canonique de la notation est CELLE DU JUGE (le modèle du jalon unix, généralisé : l'identité exigée est sur les OCTETS, jamais sur la graphie) ; (3) **L'ÉPREUVE DES BASES FORCÉES A MORT NOMMÉE À SA PREMIÈRE FORME** — sous qemu-riscv64 10.0.13, la base par défaut de l'image PIE invitée est CONSTANTE (0x555555556000 au labo, constatée sur 6 exécutions : qemu-user ne randomise PAS l'image invitée), et `-B` (guest_base) seul est SANS effet sur l'adresse d'image ET_DYN : deux configurations -B distinctes rendaient la MÊME base — l'instrument a été INSTRUIT SUR PIÈCES avant d'être contourné (le levier du chargeur est `-R`, la fenêtre de réservation VA) ; trois configurations forcées VERTES (0x2aaac000 / 0xaaaac000 / 0x55556000) démontrent l'indifférence à la base PAR LES PARAMÈTRES DU CHARGEUR.

**La règle.** (1) TOUT moteur de notation d'un profil neuf (maison ou tiers) passe LA MÊME PORTE que keystone au primaire : le round-trip à 100 % avec le juge du profil (capstone), EXIGÉ EN DEUX DIRECTIONS — le corpus de textes du profil ET l'espace d'encodage lébal parcouru systématiquement (champs d'encodage exhaustifs par famille, immédiats et décalages de bord) ; toute entrée de l'espace légal que le juge décode doit ré-assembler en ses octets — la direction inverse EST la preuve, la direction avant n'est qu'un échauffement. (2) La graphie canonique de la notation est TOUJOURS celle du juge (l'auteur peut écrire addi, la notation porte mv — l'identité WYSIWYG est sur les octets) ; chaque écart attrapé par la porte est CONSIGNÉ comme leçon (jamais un avertissement silencieux, jamais une tolérance locale). (3) Un exécuteur émulé (qemu-user) est un INSTRUMENT dont les comportements se CONSTATENT et se NOMMENT — jamais des hypothèses : la randomisation (ou non) de la base invitée, l'effet (ou non) des options, se vérifient SUR PIÈCES avant d'entrer dans une épreuve ; quand l'aléa fait défaut, la propriété (l'indifférence à la base) se démontre par les PARAMÈTRES DU CHARGEUR (bases forcées), jamais en feignant l'aléa — une preuve ne doit dépendre d'AUCUN aléa de l'instrument. (4) L'échec nommé d'une épreuve s'instruit comme DÉFAUT D'INSTRUMENT avant d'être un défaut d'artefact (la lignée D151/D152/D154) : l'épreuve est corrigée sur pièces et rejouée, l'artefact n'a pas bougé d'un octet.

**Alternatives rejetées.** Admettre l'assembleur sur la seule direction avant (rejeté : les quatre défauts du chantier étaient invisibles de cette direction — un corpus écrit par l'auteur ne prouve que les prévisions de l'auteur) ; tolérer localement les pseudos non rendus par l'assembleur (rejeté : le juge est juge unique — un rendu inassemblable est un échec de build, jamais un avertissement) ; compter sur l'ASLR émulé de qemu pour la preuve PIE (rejeté : la base invitée est CONSTANTE sous qemu 10 — un vert à base constante ne prouve RIEN de l'aléa, et n'a pas à : la propriété à prouver est l'INDIFFÉRENCE à la base, pas la variété) ; dater l'option -B comme levier sans l'éprouver (rejeté : l'épreuve a mort nommée — l'option est sans effet sur l'image ET_DYN, instruit sur pièces) ; rendre la preuve dépendante du tirage aléatoire du jour (rejeté : les bases forcées du chargeur déterminent l'épreuve — la preuve est rejouable à l'identique).

**Frontières.** La règle régit les moteurs de notation des profils neufs (leur porte d'admission), la graphie canonique des notations (le juge tranche) et les épreuves d'exécution sous émulateur (leurs constats d'instrument et leurs bases forcées) ; elle ne touche NI le juge du primaire (keystone/capstone x86-64 — le round-trip R5 demeure), NI la chaîne de scellage (D147/D152 : le scellage 0.8.0-rc.1 exigera le contrôle D146 adapté à l'exécuteur du jalon — l'image PIE exécutée sous qemu à des bases constatées et forcées), NI la réserve instrumentale D149 (elle demeure NOMMÉE dans chaque verdict : l'ISA est exécutée par TCG, le noyau et les syscalls sont réels, jamais déguisés en exécution native). L'assembleur maison as_rv64 (riscv/outils/as_rv64.py) est admis par la porte du chantier : 783 + 1037 à 100 % (Entrée 150).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (append-only, D24) --------------------------------
if "## D155" in texte:
    sys.exit("ECHEC : la décision D155 existe déjà")
i154 = texte.find("## D154")
if i154 < 0:
    sys.exit("ECHEC : D154 introuvable")

nouveau = texte.rstrip("\n") + "\n" + D155

# ordre recoupé : D154 < D155
j154 = nouveau.find("## D154")
j155 = nouveau.find("## D155")
if not (0 <= j154 < j155):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"D155 insérée ({len(D155)} caractères) — à la suite de D154, append-only")
