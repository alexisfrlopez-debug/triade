#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_145.py — JOURNAL_TRAVAIL.md : insère l'Entrée 145 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
144 < 145 < marqueur recoupé — le même contrat que les entrées 127-144)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 145 — LE CHANTIER M6-(a) ACCOMPLI (« continue M6 ») : LE DURCISSEMENT FORMAT DÉMONTRÉ EN EXÉCUTION — la sonde `unix/` (quatre blocs `su`, série f6xxxx, carte génération 1 au TROISIÈME sel, artefact 8 192 o) porte l'image à ET_DYN/PIE (base aléatoire CONSTATÉE : 6 bases distinctes sur 6 exécutions, alignées 0x1000, recoupées sous setarch -R — même base deux fois, la base vient du noyau — et par readelf indépendant), trois segments R/RX/RW, PT_GNU_STACK sans X, W^X CONSTATÉ DEPUIS LES PHDR ; la table ERRNOS (miroir de la table HRESULTS) EXERCÉE en exécution sur ses deux branches (EBADF nommé → verdict 1 ; EFAULT hors table → VERDICT_FATAL 6, arrêt propre code 6) ; round-trip 100 % (133 instructions), falsification 11/11 zéro silence ; LA BALISE 0.7.0-dev.1 POSÉE par le premier build M6 — exactement comme l'annonçait D149 ; D150 née (04/11)

**Le geste (la suite annoncée au Task 62 était le chantier M6-(a), « aucune décision développeur ne le bloque »).** Le writer du jalon `unix/build_m6.py` (modèle `m6/build_ah.py` de l'échelle D34) porte l'image à ET_DYN (PIE, base aléatoire ASLR noyau, e_entry RELATIF 0x1140, adresses de liaison = RVA — le code est indifférent à la base : les accès vivent en [rip] ou [base + RVA], jamais en lien-temps absolu), trois segments PT_LOAD R/RX/RW (offsets == vaddr, .bss pur filesz 0) et PT_GNU_STACK 0x6474e551 à drapeaux RW SANS X. Le layout `unix/layout.py` (modèle D8, série f6xxxx propre — les séries sont nommées PAR CARTE, m6/ et m7/ demeurent l'échelle D34) porte la table ERRNOS (source unique : [nombre u32] + {errno u32, verdict u32}, EBADF→1, VERDICT_FATAL 6 — tout errno hors table : arrêt propre nommé, fail-closed) et les messages de la sonde.

**La sonde (le critère de sortie du chantier, exécuté au labo).** Quatre blocs, specs écrites-avant-code : su-01 écrire (sys_write, miroir ah-01 — ET l'instrument des sondes d'erreur déclarées), su-02 hex64 (u64 → 16 caractères, %016lx du noyau), su-03 verdict (la table ERRNOS, miroir tls-02:R1/HRESULTS D79), su-04 principal (_start : calcule SA base par `lea rip` sur le témoin .rodata, l'émet, exerce la table sur ses DEUX branches — write(-1, lisible, 15) rend -EBADF nommé, write(1, 0x1 non mappé, 27) rend -EFAULT fatal — puis arrêt propre code 6 ; sous-programme local .emit déclaré en I1, la cible d'appel locale passe la même porte que les blocs). L'oracle natif : 6 exécutions, quatre lignes attendues octet pour octet et code 6 à chaque run ; les bases DISTINCTES entre runs (6/6 — l'ASLR CONSTATÉ jamais décrété, la sonde ne peut pas inventer sa base), alignées à la page ; setarch -R (ADDR_NO_RANDOMIZE) rend la MÊME base deux fois — la base vient du NOYAU, pas du programme ; readelf recoupe indépendamment (DYN, 3 LOAD R/R E/RW, GNU_STACK RW). Le build relit son image : valider_elf() constate W^X DEPUIS LES PHDR (aucun segment inscriptible exécutable), la concordance ERRNOS/HEXCHARS/messages au layout, et les 73 verrous structurels + 20 symboles @ confrontés au RÉEL (leçon C1).

**Les deux leçons du build, attrapées par les gardes (le cœur de D150).** (1) LA LEÇON C1 A FONCTIONNÉ EN DIRECT : @L_FATAL portait 36, le message réel en fait 37 (le «\\n» oublié au compte) — verifier_symboles a REFUSÉ le build avant toute exécution : l'arithmétique de l'auteur est vérifiée par la machine, jamais crue. (2) Le premier .emit plaçait le préfixe (r8) et la longueur (r9) en registres volatils puis appelait su-03 : su-02/su-03 clobber r8/r9 (travailleurs d'UN appel), chaque syscall de su-01 détruit r11 — le verdict et le préfixe MOURAIENT au premier appel (la sortie rendait deux lignes, la première émission du .emit écrivait à une adresse doublée → EFAULT → .echec → fatal silencieux) ; l'oracle natif a REFUSÉ fail-closed, jamais un faux vert. La correction : le préfixe est consommé AVANT le premier appel, le verdict vit au tampon .bss +32 (TAMPON_NUM — la mémoire traverse les appels et les syscalls), le brut traverse en r10 (registre de travail interne que ni su-01, ni su-02, ni su-03 ne touchent) — D150 consigne la règle.

**Les consignations d'état.** Fiche de profil § 3 : le durcissement passe de « À PRODUIRE » à « ACQUIS PAR LE CHANTIER M6-(a) » (constats datés, re-vérifiés au chantier qui les touche : keystone/capstone re-vérifiés par le round-trip même — le MÊME moteur que le primaire, la thèse de M6 à ISA constante ; le labo-EST-Linux re-vérifié par l'exécution native) ; l'écart acquis→jalon demeure NOMMÉ (l'ELF minimal auto-hôte ET_EXEC reste valide pour SA lignée). PLAN_MILESTONES : section « État du programme » du programme M6/M7 — M6-(a) RÉALISÉ le 04/11, les chantiers (b)/(c)/(d) attendent, les décisions développeur demeurent non bloquantes. La sonde vit au dépôt `unix/sonde` (8 192 o, sha256 consigné au tableau de bord de SA carte, génération 1 au TROISIÈME sel — m2, hachoir D34, jalon unix — clés projet partagées D27, verrou croisé R8 4/4, cristallisation 2/10 par la re-vérification).

**Frontières.** La balise 0.7.0-dev.1 est POSÉE (geste de BUILD, jamais de scellage — le scellage 0.7.0-rc.1 viendra du chantier (c) avec le contrôle D146 adapté, la garde anti-rollback n'existe pas encore : la sonde est un DEV vivant) ; le scellé 0.6.0, les cartes m0-m5, le sceau ONZE arbres, les arbres I, les fixtures v5, le hachoir m6/ (l'échelle D34 demeure ET_EXEC — VALIDE pour sa lignée) : INTACTS ; aucune suppression Drive, corbeille non vidée ; .keys/ gitignoré ; D139 ouverte non bloquante ; scripts suivis : inserer_entree_145.py, inserer_d150.py ; livrables du chantier : unix/layout.py, unix/I/ (README + 4 specs), unix/notation/ (brouillons + générées), unix/outils/auteur.py, unix/carte_sonde.py, unix/build_m6.py, unix/sonde, unix/carte/.

**Vérifiabilité.** python3 unix/build_m6.py (oracles + carte, fail-closed — la re-vérification --verifier incrumente la cristallisation) ; python3 unix/outils/auteur.py (les notations se régénèrent, round-trip intégré) ; ./unix/sonde (la base change à chaque exécution, le code de sortie est 6) ; setarch -R ./unix/sonde (base fixe) ; readelf -lW unix/sonde (GNU_STACK RW sans X) ; docs/PROFIL_x86-64-linux-elf64.md § 3 (ACQUIS M6-(a)) ; PLAN_MILESTONES.md § État du programme ; DECISIONS.md D150 (à la suite de D149).

**SUITE.** Le chantier M6-(b) — le corpus paritaire : l'audit de couplage (contrats classés A/B/C), la révision de granularité R+1 au niveau FORMEL (arguments nommés dans I, convention d'appel vers frag-con, § 8.3-4), l'invariance des octets Windows ASSERTÉE, le diff nul MESURÉ PAR SCRIPT (les instances des deux profils chargent les MÊMES fichiers I) ; l'oracle m1 régénéré VERT sur l'instance Linux ; un principal propre au jalon (domaine neuf, modèle ah-09). Le chantier (c) (conformité + scellage 0.7.0-rc.1) et (d) (le patch en production — le report M5-(c) refermé) suivent ; les décisions développeur (terrain WSL2/VM, réserve qemu, aval du report) peuvent tomber au fil de l'eau.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-144) ------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 145" in texte:
    sys.exit("ECHEC : l'Entrée 145 existe déjà")
i144 = texte.find("## Entrée 144")
im = texte.find(MARQUEUR)
if not (0 <= i144 < im):
    sys.exit("ECHEC : ordre inattendu (144/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 144 < 145 < marqueur
j144 = nouveau.find("## Entrée 144")
j145 = nouveau.find("## Entrée 145")
jm = nouveau.find(MARQUEUR)
if not (0 <= j144 < j145 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 145 insérée ({len(ENTREE)} caractères) — ordre 144<145<marqueur recoupé")
