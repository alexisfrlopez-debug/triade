#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d161.py — DECISIONS.md : insère la décision D161 PAR SCRIPT
(append-only à la suite de D160, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/DECISIONS.md"

D161 = """
## D161 — LES SLOTS DU DOMAINE `sys` ARRÊTÉS SUR LES LONGUEURS RÉELLES DES NOTATIONS (la mesure auteur décide — D47/D79 rejoués : la préfiguration 0xA000/0xA400/0xB000 n'était pas un droit) ; LES FIXTURES .rdata DU DOMAINE ARRÊTÉS DANS LA ZONE VIERGE DU SCELLÉ 0.6.0 (le nom @0x2EC0, la ligne de hello-02 @0x2ED0, la borne @0x2F00 — le corps ne bouge d'AUCUN octet R7) ; LES TROIS ERRATA DE LA COUCHE I CORRIGÉS NOMMÉMENT AVANT LA NOTATION (memcmp est libc-02 jamais libc-04 ; « NtWriteFile » mesure 11 octets jamais 10 ; le padding de slot de la lignée est NOP 0x90 jamais int3) ; LA SÉPARATION VERDICTS/SSN EST STRUCTURELLE (les verdicts de vrais négatifs 64 bits signe-étendus, les SSN zéro-étendus — jamais de collision)

**Le contexte qui fonde la décision (05/11, chantier M8-(b)).** La couche I du domaine `sys` était née écrite-avant-code (D160, Entrée 156) : la charte à huit règles, les trois spécifications, le plan d'adressage PRÉFIGURÉ — « les RVA et tailles définitifs seront ARRÊTÉS au chantier (b) sur les longueurs réelles des notations (modèle D47/D79 : la mesure auteur décide, la préfiguration n'est pas un droit) ». Le chantier (b) a produit les notations (à la main, auteur.py, keystone assemble — rien d'autre), les a MESURÉES, et la mesure décide : sys-01 SIX octets, sys-02 293, sys-03 164. La préfiguration s'incline.

**La règle.** (1) **Les slots arrêtés** : sys-01 @ **0xA000** slot **0x40** (padding 58), sys-02 @ **0xA040** slot **0x140** (padding 27), sys-03 @ **0xA180** slot **0xC0** (padding 28) — tassés depuis 0xA000 (D8 : multiples de 64, alignés 16, padding >= 16), la réserve contiguë **0xA240-0xBFFF** (7 488 o) porte la croissance du domaine (sys-04 et suivants ; TLS 1.3 pur attend sa décision propre, D160). (2) **Les fixtures .rdata du domaine arrêtés dans la zone VIERGE 0x2EB0-0x2FFF du scellé 0.6.0** (vérifiée sur pièces au geste : 336 octets NULS dans proxy.exe après la borne de marche M5 R_BORNE_M5) : le span-nom « NtWriteFile » @ **0x2EC0** (11 octets, AUCUN NUL — P1 de sys-02 est un SPAN, jamais une terminaison supposée), la LIGNE de hello-02 @ **0x2ED0** (34 o dont NUL, byte-exact le MESSAGE de m0/build_m0.py — la twin ÉMET ces octets, jamais une seconde copie : I4 de sys-03), la borne @ **0x2F00** (fail-closed, miroir D95 — le prochain fixture pose là, jamais au-delà sans arrêt nommé). Le corps scellé ne bouge d'AUCUN octet (R7) : la zone VIERGE reçoit les nouveaux. (3) **Les trois errata de la couche I, corrigés nommément AVANT la notation** : memcmp est **libc-02** (b20002 — le registre figé m1/I/README.md fait foi), la couche I citait libc-04 (itoa) ; « NtWriteFile » mesure **11 octets** (N-t-W-r-i-t-e-F-i-l-e — la mesure sur pièces fait foi), la couche I disait 10 ; le padding de slot de toute la lignée win est **NOP 0x90** (build_m0.py : `octets + b"\\x90" * pad` — int3 est la convention des zones RÉSERVÉES inter-blocs), la couche I disait int3. Aucun octet n'avait encore été écrit sur les citations fausses : la correction précède l'octet, chaque erratum consigné DANS le fichier de la couche I qu'il corrige. (4) **La séparation verdicts/SSN est structurelle** : les verdicts du domaine sont de VRAIS négatifs 64 bits (`mov rax, -N` signe-étendu), les SSN des imm32 zéro-étendus (`mov eax, [rdx+4]`) — un SSN à bit 31 posé reste POSITIF en 64 bits, jamais confondu avec un verdict ; le test en est fait au harnais (le cas pathologique 0x80000001). (5) **La preuve au harnais sur FIXTURES ntdll synthétiques** (le modèle différentiel M4/M5) : le labo ne possède aucun vrai ntdll, n'en prétend aucun et NE DEVINE JAMAIS le SSN du terrain — les fixtures forgées (PE32+ minimales mais bien formées : l'hostilité vit dans les noms, les stubs, les bornes, jamais dans des pointeurs fous) font la preuve ; le VRAI ntdll se lira au terrain (chantier (d), modèle m6d/m7d). Le bilan du premier passage complet : **61 contrôles · 61 VERTS** (round-trip + concordance au plan ; le trombone au noyau simulé ; le résolveur et ses SIX verdicts nommés ; LA TWIN au différentiel — la MÊME ligne par les DEUX chemins octet pour octet ; le fuzzing à trois graines ; les QUINZE mutations de falsification attrapées, les témoins intacts verts).

**Alternatives rejetées.** Garder la préfiguration 0xA000/0xA400/0xB000 (rejeté : D47/D79 — la préfiguration n'est pas un droit, la mesure décide ; le tassement laisse 7 488 o contigus à la croissance) ; poser les fixtures dans une section nouvelle (rejeté : la zone vierge 0x2EB0-0x2FFF du .rdata EXISTANT suffit — aucune section de plus, aucun octet du scellé déplacé) ; recopier la ligne de hello-02 dans le bloc (rejeté : I4 — une seconde copie serait une divergence d'observable en sursis ; la twin CITE par déplacement) ; un NUL après le span-nom (rejeté : P1 de sys-02 est un SPAN — poser une terminaison supposerait ce que le contrat interdit de supposer) ; corriger les errata SILENCIEUSEMENT (rejeté : la doctrine — sur pièces, jamais sur mémoire ; chaque coquille est NOMMÉE dans le fichier qu'elle corrompait, la lignée peut relire le geste) ; graver les SSN des fixtures dans le modèle (rejeté : le modèle dérive de la couche I et du plan, JAMAIS des octets de la notation — deux sources de vérité seraient une de trop).

**Frontières.** La présente décision est un ARRÊT D'ADRESSAGE, NI un build NI un scellage : AUCUNE balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 — INTACTES ; la 0.9.0-dev.1 viendra du premier build M8 au chantier (c), geste de BUILD) ; le corps scellé 0.6.0 ne bouge pas d'un octet (R7) ; les octets des fixtures .rdata seront POSÉS au build (c) dans la zone vierge (les adresses sont arrêtées, la pose attend le bâtisseur) ; le labo ne connaît pas le SSN du terrain (les fixtures synthétiques, la frontière du README) ; TLS 1.3 pur et les profils additionnels HORS PÉRIMÈTRE (une décision propre chacun) ; la PEB-walk et la contre-mesure du hooking CHANTIERS FUTURS NOMMÉS. Les pièces de l'arrêt : m8/notation/ (les TROIS notations explicites + brouillons), m8/outils/auteur.py, m8/harnais_sys.py, m8/layout.py (arrêté), m8/I/ (les errata consignés), les empreintes au harnais (19e24b48… graine 20261105, re-jouée 424242/777).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## D161" in texte:
    sys.exit("ECHEC : la décision D161 existe déjà")
i160 = texte.find("## D160")
if i160 < 0:
    sys.exit("ECHEC : D160 introuvable")

# D160 est la dernière décision : l'insert se fait à la suite (fin de fichier)
nouveau = texte.rstrip("\n") + "\n" + D161.rstrip("\n") + "\n"

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("D161 insérée à la suite de D160 (append-only)")
