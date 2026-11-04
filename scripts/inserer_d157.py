#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d157.py — DECISIONS.md : insère la décision D157 PAR SCRIPT à la
suite de D156 (append-only, pas de rétrodatage — le contrat D24)."""

import sys

CHEMIN = "docs/DECISIONS.md"

D157 = """
## D157 — LE PORT D'UN BLOC EST ÉPROUVÉ PAR SON CHEMIN D'EXÉCUTION RÉEL, JAMAIS PAR SA SEULE LECTURE (l'équivalent RV64 du `mov rdx, rdi` de l'instance x86-64 — le marshalling des arguments du syscall — a été OUBLIÉ au port : tcp-07 passait à mprotect un a2 de débris, la page perdait son bit X et l'exécution FAUTAIT à l'instruction suivante ; le bloc se lisait parfaitement, il se traduisait en un crash — SEUL LE CHEMIN RÉEL le nomme) ; LA PREUVE D'UN CRASH SE MÈNE AU JOURNAL DE L'EXÉCUTEUR (QEMU_STRACE a nommé `PROT_READ|PROT_WRITE|PROT_SEM` : le prot reçu était 0xB, des débris — le strace de l'instrument est une PIÈCE, pas un diagnostic de confort) ; UN SOUS-PROGRAMME QUI APPELLE SAUVE ra (jal écrase le lien — la leçon sr-04 réapprendue : .dire appelait écrire puis rendait vers sa propre boucle) ; CE QUI TRAVERSE UN APPEL VIT EN NON VOLATIL — LA RÈGLE D150 SE RÉAPPREND À CHAQUE GESTE (l'attendu du trafic dans t0, mort au premier appel ; le t0 des refus, recalé deux fois)

**Le constat qui fonde la décision (05/11/2026, chantier M7-(c), Entrée 153 — la démonstration du patch fence.i).** QUATRE défauts d'instrument et d'artefact, tous nommés par les gardes ou par le journal de l'exécuteur, aucun par la relecture : (1) **LE PORT OUBLIÉ** — tcp-07:R4 (riscv) portait `.protger` qui reçoit la protection dans a0, la garde dans t2, assemble l'adresse et la longueur — et ne passe JAMAIS a2 au syscall : mprotect recevait un a2 de débris (0xB = READ|WRITE|SEM observé) ; la page 0x1000 perdait son bit EXÉCUTABLE, le fetch suivant faute (ACCERR) et l'invité mourait en SIGSEGV — LE BLOC SE LISAIT PARFAITEMENT (le structurel, le round-trip, 1537 verrous — tout vert), le crash ne vivait qu'au CHEMIN RÉEL : la démonstration (le demo du patch, 1200 usages) l'a nommé au premier apply ; le strace de l'exécuteur a donné la pièce (`PROT_SEM` — un prot qui n'existe dans AUCUN plan) ; la correction est UNE ligne (`mv a2, t2` — l'équivalent exact du `mov rdx, rdi` de l'instance x86-64), le corpus a été REBUILDÉ (sha ec343b4e… — l'ancien b34a7147… consigné à son époque demeure le record de ce qui fut) ; (2) **LA LEÇON D150 RÉAPPRISE DEUX FOIS** — l'attendu du trafic vivait dans t0 (un VOLATIL) : le premier appel au journal le détruisait, le verdict échouait (l'attendu est passé en s10, non volatil) ; puis le t0 des refus (comparé APRÈS l'appel qui le clobberait) — recalé avant chaque bne : LA RÈGLE EST LA MÊME, L'ESPÈCE CHANGE À CHAQUE GESTE — la garde est le contrat écrit AVANT (D150), la conformité est le re-calage ; (3) **.dire ET ra** — le sous-programme local .dire (l'impression) appelait écrire via jal puis `ret` : ra avait été écrasé par l'appel interne, le ret remontait vers sa propre boucle (bltz/ret en spin — le trace in_asm a nommé la boucle à deux instructions) : le sous-programme qui APPELLE sauve ra (la leçon sr-04, réapprendue au port — le cadre -16/+16 apparié) ; (4) **LES REPRODUCERS IMPROVISÉS SONT UN MARÉCAGE** — trois images roulées à la main pour « isoler le mprotect » ont crashé pour leurs propres défauts (paires mal calculées, prot hors plage) et ont failli faire nommer une réserve d'instrument qui N'EXISTAIT PAS : le mprotect invité fonctionne PARFAITEMENT sous qemu (RWX puis RX, D39 tenu) — l'isolement d'un défaut se mène SUR L'IMAGE DE LA FAMILLE (le builder), jamais sur une image roulée à la main.

**La règle.** (1) UN BLOC PORTÉ N'EST CONFORME QUE CHEMIN RÉEL EXÉCUTÉ : tout port d'un bloc d'une ISA à l'autre exige que le bloc soit EXERCÉ en exécution par au moins un scénario qui traverse son chemin complet (la lecture structurelle, le round-trip et les verrous ne prouvent QUE la graphie — le marshalling des arguments ne vit QUE dans l'exécution) ; un bloc jamais exécuté au labo est un bloc NON ÉPROUVÉ, sa conformité est une lecture, pas une preuve. (2) LE JOURNAL DE L'EXÉCUTEUR EST UNE PIÈCE : QEMU_STRACE (et le trace in_asm) s'archivent comme témoin quand un défaut se présente — le strace nomme les arguments RÉELS des syscalls (PROT_SEM n'est dans aucun plan : la pièce désigne le marshalling, pas le service). (3) TOUT sous-programme local qui effectue un appel interne sauve ra AVANT l'appel et le restaure avant son ret (jal écrase le lien — la leçon sr-04 est une règle de la FAMILLE, pas de la sonde seule). (4) LA RÈGLE D150 (jamais un volatile qui traverse) SE VÉRIFIE À CHAQUE GESTE PAR ÉCRITURE PRÉALABLE : le registre porteur d'un attendu est nommé DANS LE CONTRAT DU BLOC (s10 ici), jamais laissé au choix du geste — et tout comparateur post-appel est recalé entre l'appel et la comparaison.

**Alternatives rejetées.** Déclarer tcp-07 conforme sur la lecture structurelle (rejeté : le marshalling a0→a2 ne vit dans AUCUNE lecture — 1537 verrous verts sur un bloc qui crashait au premier appel : l'espèce exacte du faux vert) ; nommer une réserve d'instrument sur qemu (rejeté : les reproducers crashaient pour leurs propres défauts — le mprotect invité marche, la réserve aurait été un mensonge d'instrument) ; tolérer le spin de .dire comme un défaut cosmétique (rejeté : le spin est un HANG — l'espèce la plus dure, un vert muet éternel) ; recalé t0 « une fois pour toutes » au début du bloc (rejeté : recalé AVANT CHAQUE comparaison — le clobber est répété, la défense aussi).

**Frontières.** La règle régit les PORTS de blocs entre ISA (le marshalling des arguments de service), les sous-programmes locaux (le cadre ra), les registres porteurs d'attendus (D150) et la discipline d'isolement des défauts (jamais d'image roulée à la main — la famille du builder) ; elle ne touche NI la réserve instrumentale D149 (nommée dans chaque verdict — TCG, noyau et syscalls réels), NI la frontière code 5 (le service refuse — STRUCTURALE sous qemu : l'hôte accorde RWX sur mapping privé, la branche fail-closed vit dans le bloc), NI le périmètre mono-fil (fiche § 5 : portée de fence.i = le cœur courant). La correction de tcp-07 (une ligne) et le rebuild du corpus (sha ec343b4e…) sont consignés à l'Entrée 153 ; le scellage 0.8.0-rc.1 a exigé le chemin réel VERT AVANT la balise (le verrou multi-profils, le D146 par trace, la conformité 7/7 — la suite EXÉCUTANT la démonstration).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## D157" in texte:
    sys.exit("ECHEC : la décision D157 existe déjà")
i156 = texte.find("## D156")
if i156 < 0:
    sys.exit("ECHEC : D156 introuvable")

nouveau = texte.rstrip("\n") + "\n" + D157
j156 = nouveau.find("## D156")
j157 = nouveau.find("## D157")
if not (0 <= j156 < j157):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"D157 insérée ({len(D157)} caractères) — à la suite de D156, append-only")
