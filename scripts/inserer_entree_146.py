#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_146.py — JOURNAL_TRAVAIL.md : insère l'Entrée 146 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
145 < 146 < marqueur recoupé — le même contrat que les entrées 127-145)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 146 — LE CHANTIER M6-(b) ACCOMPLI (« continue M6 ») : LE CORPUS PARITAIRE INSTANCIÉ, LE DIFF NUL MESURÉ, L'ORACLE m1 RÉGÉNÉRÉ VERT SUR L'INSTANCE LINUX (76 631 cas verts, 20 verrous, exécution native — différentiel 12 000 cas/bloc, autotest ligne exacte + N rendu + vecteur falsifié KO, journal 4 000 lignes exactes + CONCURRENCE RÉELLE deux threads natifs 600 lignes entières, patch scénario complet apply/rollback/effet/refus 1-5, artefact 6 exécutions deux lignes octet-identiques code 0 + setarch -R, falsification 12/12 zéro silence, V7 DEP SIGSEGV en fils) ; LA CARTE génération 1 du corpus (fragments chiffrés, Ed25519, frag-con DEUX PROFILS par bloc § 8.3-4, verrou croisé R8 13/13, cristallisation 2/10) ; L'ARTEFACT `unix/corpus` 12 288 o ET_DYN/PIE, sha256 dd14195c9da5e9b990e8f9b141eedd6574bb8ecc793ffdd5b67edb71b81ddff7, LA BALISE 0.7.0-dev.2 POSÉE ; D151 née (04/11)

**Le geste (la suite annoncée au Task 63 était le chantier M6-(b), le corpus paritaire).** Le geste avait été interrompu à 14:40, les sources écrites mais la chaîne jamais conduite jusqu'au vert ; la reprise l'a exécutée et a traversé SES REFUS un à un — chaque refus nommé (fail-closed, jamais un faux vert) a fondé une correction puis une règle (D151). L'audit de couplage (`unix/I/AUDIT-COUPLAGE-CORPUS.md`, livrable écrit-avant-code) avait établi le constat central : la classe A est VIDE — le paramétrage msx64 est partout dans le patrimoine, la voie du diff nul passe ENTIÈREMENT par la révision de granularité R+1 au niveau FORMEL (les DOUZE contrats révisés vivent dans l'arbre du jalon `unix/I/`, ancêtres scellés INTACTS dans m0/m1/m2 — la même couche I que M7 instanciera en troisième) ; la classe C (couplée à l'OS) est NOMMÉE, jamais réduite.

**Le diff nul, MESURÉ PAR SCRIPT (diff_nul.py, 39 recoupements, rejouable).** (1) les fichiers canoniques : l'instance Linux charge EXACTEMENT les fichiers de `unix/I/` (empreintes identiques, aucune copie nulle part) ; (2) l'équivalence des observables R1 ↔ R+1 : post-conditions, cas d'échec et vecteurs dorés des ancêtres scellés extraits et comparés aux révisions — diff NUL, seules les pré-conditions bougent (la granularité) ; (3) l'invariance des scellés : les sha256 des artefacts Windows (hello.exe, selftest.exe, echo.exe, proxy.exe 0.4.0/0.6.0) identiques à l'état zéro mesuré AVANT le geste (scripts/etat_zero_m6b.json). L'invariance des octets Windows est ASSERTÉE à chaque build : la chaîne s'arrête si le diff nul n'est pas VERT.

**Les refus traversés, et ce qu'ils ont fondé.** (1) SEGFAULT MUE dans l'autotest : `img.poser` écrivait une page R sans ouverture — l'instrument de mutation NOMME désormais son geste (ouvrir mprotect RW, écrire, restaurer la protection trouvée ; en mode partagé : refus nommé — jamais un poser nu, le segfault est un refus muet, la pire espèce). (2) « libc-08 falsifié : N=19 » : la fixture SC sert les DEUX sens (v6 inférieur memcmp(SA,SC)<0, v7 supérieur memcmp(SC,SA)>0) — l'attendu corrigé SUR PIÈCES (N=19, ligne « 19/21 KO ») : l'oracle croyait « +1 devient 0 », la notation constatait deux verdicts perdus. (3) SEGFAULT DÉTERMINISTE du journal (tcp-11:R2) : LA CHASSE du geste — bissection in-vivo (mutations NOP de l'image vivante) et reproducteur synthétique ; le coupable : `add r12, rax` placé APRÈS le `call @A_MEMCPY` du champ — memcpy rend dst (UNE ADRESSE, Q2 de son contrat), jamais la longueur : le compteur de longueur recevait une adresse géante et le suffixe sortait du mapping ; la correction : la longueur est capturée AVANT l'appel qui détruit son support volatile (add déplacé avant le call) — ET le STAGING (journal v2) portait LE MÊME PIÈGE : le remplaçant est corrigé AVANT d'être embarqué (il aurait crasheé au chantier (d) dès un appel réel avec champ). (4) « tcp-11 concurrence : verdicts divergents » : LA CARTOUCHE n'était pas ré-entrante — entrées, sorties, sauvegarde de pile et pages partagées entre threads : deux appels simultanés s'écrasaient mutuellement ; ré-écrite : entrées LOCALES à l'appel, sommet attribué PAR APPEL sous un verrou court (pas 0x800), fenêtre de sorties par appel [sommet-0x200, sommet-0x1B8] — sous la profondeur d'imbrication maximale (corpus-13 → autotest/journal → feuilles), les cadres imbriqués n'y touchent jamais ; les tests comparent rsp au SOMMET DONNÉ (r['sommet']). (5) « 1 lignes != 600 » : le travailleur du V3 doit terminer ses lignes (le journal émet ce qu'on lui donne — son contrat). (6) « V7 : l'immédiat 0x7 introuvable » : la fenêtre de scan 0x60 était trop courte (l'immédiat vit à +0x6e) — portée au slot 0x200. (7) « libc-06 PASSÉ SILENCIEUX » : la mutation de la première instruction était « guérie » par un RÉSIDU DE REGISTRE (lea r8 muté, le store [r8] tombait encore sur le curseur — r8 résiduel de l'appelant) : la falsification est désormais EXHAUSTIVE par instruction (un bloc est rompu dès qu'une mutation dévie). (8) « tcp-07 : 78 mutations TOUTES silencieuses » : tcp-07 est HORS-CHEMIN du principal (corpus-13 ne l'appelle pas — la démonstration du patch est le chantier (d)) : AUCUNE corruption d'un bloc non exécuté ne peut dévier l'artefact, c'est un FAIT DE PLAN ; la falsification porte les blocs DU CHEMIN (12), tcp-07 est épuisé par SON scénario (apply/rollback/effet, intégrité staging code 3, refus code 5) et par le V7 DEP EN FILS : la constante RWX 0x7 mutée en 0x3, la page entière du code devient R+W sans X, le RET du patch lui-même FAUTE — SIGSEGV constaté en fils (le père observe, le fils meurt : le code défaillant ne tue jamais l'instrument).

**L'incident de l'état zéro (consigné à l'audit § 6, porté en règle par D151).** En mesurant l'état zéro, `m1/build_m1.py` lancé SANS argument a tourné : la garde de l'ère m1 traite « carte illisible » comme « absente » (`except ErreurCarte: pass`) et échoue OUVERTE ; selftest.exe est resté OCTET-IDENTIQUE (chaîne déterministe), la carte m1 régénérée en dev.2 a été RESTAURÉE octet-pour-octet depuis git. LA RÈGLE : ABSENT ≠ ILLISIBLE — une carte PRÉSENTE et indéchiffrable est un REFUS, jamais une permission ; `build_corpus.py` distingue les deux dès sa naissance. Le correctif des cinq chaînes historiques (m1→m5) est un geste nommé pour le développeur — aucune urgence : les cartes m1→m4 sont des scellés d'archives, seule m5 vit sous la phrase du jour.

**Les consignations d'état.** Fiche de profil : § 7 (granularité) passe de « Jalon » à ACQUIS PAR LE CHANTIER M6-(b) (le layout du corpus, 13 blocs à slots stables, série f61xxxx, padding/réserves int3, table bloc↔slot au frag-loc de la carte génération 1) ; § 3 : le corpus du chantier (b) L'A HÉRITÉ (le durcissement M6-(a) : ET_DYN/PIE, 3 segments, GNU_STACK sans X — l'écart acquis→jalon demeure NOMMÉ, le hachoir m6/ reste VALIDE pour sa lignée). PLAN_MILESTONES § État du programme : M6-(b) RÉALISÉ le 04/11, (c)/(d) attendent. L'oracle est régénéré/exécuté à chaque session (D1) : seuls ses verdicts hachés survivent dans frag-prf (graine 1 : empreinte 0e3d96c3d32bf611… ; graine 2 : 09444ffbd9c2e6b7… — les graines différencient, D1).

**Frontières.** La balise 0.7.0-dev.2 est un geste de BUILD, JAMAIS de scellage (le scellage 0.7.0-rc.1 viendra du chantier (c) avec le contrôle D146 adapté full-ELF à la base réelle ; la garde anti-rollback n'existe pas encore : le corpus est un DEV vivant, la balise 0.7.0-dev.1 demeure le plancher) ; scellé 0.6.0 + cartes m0-m5 + sceau ONZE arbres + arbres I + fixtures v5 + hachoir m6/ INTACTS (l'état zéro mesuré avant, le diff_nul recoupe à chaque build — les sha256 des scellés Windows n'ont pas bougé d'un octet) ; aucune suppression Drive, corbeille non vidée ; .keys/ gitignoré ; D139 ouverte non bloquante ; scripts suivis : etat_zero_m6b.py, inserer_entree_146.py, inserer_d151.py, passe_bundle_m6b.py ; livrables du chantier : unix/layout.py (corpus), unix/I/ (audit + 13 specs R+1 + README), unix/notation/ (brouillons + générées — les DEUX journaux corrigés), unix/build_corpus.py, unix/oracle_corpus.py (la cartouche ré-entrante), unix/diff_nul.py, unix/carte_corpus.py, unix/corpus (12 288 o), unix/carte-corpus/.

**Vérifiabilité.** python3 unix/build_corpus.py (la chaîne intégrale, fail-closed) ; python3 unix/build_corpus.py --verifier --graine 2 (cristallisation) ; python3 unix/diff_nul.py (le diff nul seul, 39 recoupements) ; ./unix/corpus (les deux lignes exactes, code 0) ; setarch -R ./unix/corpus (base figée, mêmes lignes) ; readelf -lW unix/corpus (3 LOAD R/R E/RW, GNU_STACK RW) ; docs/PROFIL_x86-64-linux-elf64.md § 7 (ACQUIS M6-(b)) ; PLAN_MILESTONES.md § État du programme ; DECISIONS.md D151 (à la suite de D150).

**SUITE.** Le chantier M6-(c) — la suite de conformité (unix/conformite_profil.py, modèle m5 : les SEPT éléments constatés depuis l'artefact) + le scellage 0.7.0-rc.1 avec le contrôle D146 adapté (exécution full-ELF à la base réelle, l'émulation à base fixe interdite comme témoin unique) ; puis (d) le patch en production — le chantier M5-(c) refermé (bascule du journal PENDANT le trafic, moteur tcp-07 EMBARQUÉ, le staging v2 corrigé attend la démonstration), kit terrain au coffre /test (WSL2 recommandé D149) ; les décisions développeur (terrain WSL2/VM, réserve qemu, aval du report) peuvent tomber au fil de l'eau.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-145) ------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 146" in texte:
    sys.exit("ECHEC : l'Entrée 146 existe déjà")
i145 = texte.find("## Entrée 145")
im = texte.find(MARQUEUR)
if not (0 <= i145 < im):
    sys.exit("ECHEC : ordre inattendu (145/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 145 < 146 < marqueur
j145 = nouveau.find("## Entrée 145")
j146 = nouveau.find("## Entrée 146")
jm = nouveau.find(MARQUEUR)
if not (0 <= j145 < j146 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 146 insérée ({len(ENTREE)} caractères) — ordre 145<146<marqueur recoupé")
