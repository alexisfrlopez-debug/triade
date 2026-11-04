#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d149.py — DECISIONS.md : insère D149 PAR SCRIPT À LA SUITE de
D148 (insertion ASSERTÉE : D148 présente une fois, D149 absente, D149
ajoutée APRÈS D148 — fin du fichier, modèle inserer_d148.py)."""

import sys

CHEMIN = "docs/DECISIONS.md"

DECISION = """

## D149 — LE PLAN DES JALONS M6/M7 : les fiches de profil complètes naissent AVANT le premier octet, le corpus nominal M6 est RESTREINT et NOMMÉ, le chantier M5-(c) est REPORTÉ au M6-(d) (explicite, jamais silencieux) — et les constats labo sont DATÉS

**Le contexte qui fonde la décision (04/11, « ok, on enchaine »).** Le jalon M5 est rentré (balise 0.6.0 scellée, validation terrain consignée — Entrée 143, D148) et le worklog annonçait « les jalons M6/M7 attendent leur plan » : le présent geste écrit ce plan. Il n'est pas une page blanche : l'échelle d'auto-hébergement (D34) vit déjà sur le profil `x86-64-linux-elf64` (hachoir `m6/` échelon 1, sceau `m7/` échelon 2 phase 1 — ELF64 écrit à la main, exécuté nativement au labo) ; le jalon M6 porte la PARITÉ du patrimoine M0–M5, pas la re-création de la chaîne. Trois constats labo fondent le plan et sont DATÉS du 04/11/2026 : keystone 0.9.2 ne porte PAS l'architecture RISC-V ; capstone 5.0.7 désassemble RV64 (constaté sur octets) ; aucun binaire qemu-riscv64 dans le bac à sable.

**La règle.** (1) **Aucune instanciation de profil sans fiche complète écrite et vérifiée** (les sept éléments + le huitième livrable anti-rollback, spécification § 16, manuel § 2 : « jamais d'instanciation approximative ») — les fiches `docs/PROFIL_x86-64-linux-elf64.md` et `docs/PROFIL_riscv64-linux-elf64.md` naissent AVANT le premier octet des jalons, constats datés et re-vérifiés au chantier qui les touche. (2) **Le corpus nominal M6 est restreint et nommé** : les SEPT blocs purs libc-01..07 + libc-08 autotest + tcp-07 (moteur de patch) + tcp-11 (journal) + les DEUX contrats d'interface (révisions formelles de hello-02/hello-03) + un principal propre au jalon — le serveur écho complet de M2 (contrats tcp d'interface socket) est une extension OUVERTE à la demande du développeur, jamais une réduction silencieuse : le critère § 18-M6 (diff nul, même oracle, parité) se démontre sur le corpus nominal. (3) **La voie du diff nul est la révision de granularité des contrats** : arguments nommés dans la couche I, convention d'appel déplacée vers frag-con (spécification § 8.3-4) — invariance des octets Windows ASSERTÉE (les scellés ne bougent pas), sceau de l'Intention suivi pour les arbres I modifiés ; le diff nul se mesure PAR SCRIPT (les instances des deux profils chargent les MÊMES fichiers I). (4) **Le chantier M5-(c) (patch à chaud du journal en production) est reporté au chantier M6-(d)** : le critère sera démontré sur le profil Linux, moteur tcp-07 instancié et EMBARQUÉ (bascule pendant le trafic, rollback, zéro régression) — le report est consigné au plan, à la spec et au présent journal. (5) **Convention de dossiers** : le jalon M6 vit dans `unix/`, le jalon M7 dans `riscv/` ; les noms `m6/` et `m7/` demeurent ceux de l'échelle d'auto-hébergement D34 (emprunt de nommage consigné — le plan ne le défait pas). (6) **Balises** : M6 → 0.7.0 (rc.1 puis finale après run terrain vert), M7 → 0.8.0 ; le scellage rc/final exécute le CONTRÔLE D146 ADAPTÉ : exécution full-ELF à la base réelle (l'image PIE chargée par le noyau à base aléatoire — un pointeur nu y meurt exactement comme sur le terrain, l'émulation à base fixe reste interdite comme témoin unique). (7) **L'ordre M6 puis M7 isole les variables** (D14) : l'OS à ISA constante, puis l'ISA — le MÊME corpus sera instancié trois fois depuis la même couche I.

**Alternatives rejetées.** Instancier un profil sans fiche complète (rejeté : le manuel § 2 en fait un refus de build — « un profil incomplet est un refus de build, exactement comme une carte manquante ») ; porter le corpus réseau complet de M2 au jalon M6 (rejeté : le coût des contrats socket ne sert pas le critère § 18 — le corpus restreint le démontre, l'extension reste un chantier ouvert) ; abandonner le chantier M5-(c) (rejeté : le critère § 18-M5 l'exige — le report au profil Linux le referme avec le moteur embarqué, mieux que le superviseur Windows ne le permettait) ; exécuter M7 avant M6 (rejeté : D14 isole chaque variable — le mécanisme des profils avant l'indépendance d'ISA) ; dupliquer les contrats purs par profil au lieu de la révision de granularité (rejeté : la duplication tuerait le diff nul, la preuve que « l'intention vit dans I et pas dans les octets ») ; compter sur keystone pour le RISC-V (rejeté : le constat labo est formel — l'assembleur RV64 maison ou un moteur tiers passé à la même porte, capstone restant le juge unique du round-trip).

**Frontières.** Les fiches de profil et le programme M6/M7 sont des LIVRABLES DU PLAN (jamais des scellés — aucune balise n'est posée par la présente : la 0.7.0-dev.1 viendra du premier build M6) ; les décisions développeur attendues (terrain M6 : WSL2 recommandé ou VM Linux isolée ; terrain M7 : qemu-riscv64 avec réserve instrumentale nommée ; aval du report M5-(c)) sont NOMMÉES au plan et non bloquantes pour le démarrage de M6-(a) ; l'état des jalons de la spécification v0.6.1 est mis à jour (M0–M5 franchis, M6/M7 ouverts — le PDF se régénère par le mécanisme établi D17/D134, empreinte consignée PAR LE BUILD) ; l'écart D81 du PHRASE-CONTROLE-COFFRE.txt de la racine Drive (nommé au Task 60 : 59 o, 3 lignes, ouverture impossible) est FERMÉ au même geste (phrase seule 33 o, identique à la remise du dépôt, ouverture du coffre VERT — coffre INTÈGRE, jamais muté).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "\\n" in DECISION:
    sys.exit("ECHEC : séquence parasite backslash-n dans la décision")
if "## D149" in texte:
    sys.exit("ECHEC : D149 existe déjà")
if texte.count("## D148 —") != 1:
    sys.exit(f"ECHEC : D148 présente {texte.count('## D148 —')} fois (1 attendue)")

nouveau = texte.rstrip("\n") + "\n" + DECISION

if not (nouveau.find("## D148 —") < nouveau.find("## D149")):
    sys.exit("ECHEC : ordre final inattendu (D149 avant D148)")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("D149 insérée à la suite de D148 — ordre recoupé")
