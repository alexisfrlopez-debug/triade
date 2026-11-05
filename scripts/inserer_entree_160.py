#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_160.py — JOURNAL_TRAVAIL.md : insère l'Entrée 160 PAR
SCRIPT (ordre 159<160<marqueur, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"

ENTREE = """## Entrée 160 — LA CÉRÉMONIE DE L'ÈRE M8 PASSÉE SUR PIÈCES, LA DETTE D162 SOLDÉE, LE GARDE VERT 12/12, L'ARTEFACT 0.9.0-dev.1 NÉ DU BUILD (« signatures déposées dans le drive /test ») — le disque labo encore recyclé en ouverture (troisième fois), la reprise D159 rejouée, le jeton OAuth du relais encore mort (le relais compte de service porte le geste)

**La demande (consignée fidèlement) et l'état constaté AVANT tout geste.** « signatures déposées dans le drive /test » — le geste du développeur annoncé au LISEZMOI-ceremonie-ere-M8.txt est FAIT, le labo recueille. L'état constaté en ouverture (la doctrine : sur pièces, jamais sur mémoire) : (1) le disque labo RECYCLÉ ENCORE (troisième fois — Entrée 132, reprise m7d/D159, aujourd'hui) : HEAD à 402508f (la passation M6-(c)), worklog Task 65, Entrée 147, D152 — TOUT le jalon M7 et l'ère M8 absents du disque local ; (2) le jeton OAuth du relais MORT (HTTP 400 invalid_grant au rafraîchissement — la deuxième fois, le même symptôme que le 29/10 08:11). Les deux obstacles sont connus : D159 pour le premier (l'état VRAI vit aux miroirs : la reprise est un FETCH + la POINTE CONSIGNÉE), relais_service_account.py pour le second (le compte de service avait déjà pris le relais le 29/10).

**LA REPRISE D159 REJOUÉE AU GESTE MÊME.** git ls-remote : origin (GitHub) à 7079df1 — EXACTEMENT la pointe consignée par la dernière passation (le bundle 080-b7b6e01, Task 77) ; fetch + fast-forward PROPRE (les seuls écarts locaux : 9 fichiers en bits de mode 644→755, ZÉRO contenu — le même constat qu'à la reprise m7d). Les 24 gestes revenus : M6-(d) le run terrain vert + LA FINALE 0.7.0 SCELLÉE (jalon M6 franchi), M7 ENTIER (le moteur RV64, le corpus paritaire, le scellage 0.8.0-rc.1, le run terrain M7-(d) vert recoupé 29/29, LA FINALE 0.8.0 SCELLÉE — jalon M7 franchi, D159 née de la reprise précédente), l'ère M8 ouverte (D160 : la fondation du domaine sys ; D161 : les trois blocs notés-mesurés-prouvés 61/61 ; D162 : le garde nomme la dette, le build écrit par pièces détachées) et LE KIT DE CÉRÉMONIE DE L'ÈRE DÉPOSÉ (Task 77, Entrée 159 — la réponse à la demande « synchro git et drive + kit pour la cérémonie »). Les instruments réinstallés par LA PROCÉDURE consignée à la reprise m7d : pip keystone-engine 0.9.2 + capstone 5.0.9 + pefile + pynacl 1.6.2 + unicorn 2.1.4 — RIEN ne s'est perdu (troisième recyclage, zéro perte : ce qui est consigné revient, toujours).

**LE JETON MORT — LE RELAIS COMPTE DE SERVICE PORTE LE GESTE (scripts/sonder_coffre_sa.py, LECTURE SEULE).** Le mécanisme du 29/10 (relais_service_account.py : JWT RS256 du compte de service, surgiage de get_access_token) étendu au SONDAGE DU COFFRE ENTIER : la racine /Triade (14 entrées — l'export de continuité 0.8.0 du 05/11 04:49 posé, le miroir à la pointe 080-b7b6e01), le kit /Cérémonie (17 entrées — LISEZMOI-ceremonie-ere-M8.txt en place, md5 04f22750…), le miroir TRIADE-sauvegarde-git (41 entrées racine, les lignées m0-m8), et /test (10 entrées) où LA PIÈCE attend : **signatures-I.txt** (md5 annoncé Drive ab22512a6864d8841d1ff0e371db1450).

**LE RAPATRIEMENT + LE RECOUP (scripts/rapatrier_ceremonie_m8.py — lecture seule sur le dépôt, aucun écrit avant le verdict).** La pièce téléchargée, md5 CONTRÔLÉ APRÈS ÉCRITURE contre les métadonnées Drive : MATCH (1 703 o). PUIS le recoup intégral : (1) L'ANCRE DE CLÉ tenue — cle-publique-I.txt local == 173fae9c75229b15… (l'ancre écrite noir sur blanc au LISEZMOI de l'ère ; « si cle-publique-I.txt diverge : ARRÊT » — elle ne diverge pas) ; (2) le format : 12/12 lignes valides (arbre balise signature-128hex, balises == la table canonique) ; (3) **LE RECOUP DE L'ÈRE — la preuve par le déterminisme : les DIX arbres inchangés (m1-m7, demo, terrain, v06) portent les MÊMES signatures que les déposées du 04/11** — Ed25519 (RFC 8032) est déterministe : re-signer un arbre inchangé avec la clé du 04/11 redonne EXACTEMENT la signature déposée ; la comparaison bit à bit PROUVE la réutilisation de la clé SANS JAMAIS ACCÉDER à la clé privée ; (4) m0 RE-SIGNÉ (l'empreinte vivante d94154840c9de80a… — le registre étendu au M8-(a), les specs hello INTACTES) et m8 ARBRE NEUF (621daf173debcc4c… — le domaine sys, aucune signature déposée au 04/11) : exactement les DEUX arbres que D162 nommait ; (5) les empreintes vivantes des 12 arbres == a-signer.txt (la remise fraîche du kit) 12/12 ; (6) chaque signature VÉRIFIÉE Ed25519 contre 173fae9c… sur l'empreinte du manifeste VIVANT local — par les instruments du dépôt (sceau_I chargé par chemin absolu, la leçon D158). **VERDICT : RECOUPE INTÉGRAL VERT 12/12.**

**LE DÉPÔT CANONIQUE (l'atomicité de cérémonie, spec § 5).** Le garde AVANT le dépôt nommait la dette EXACTEMENT comme au Task 76 : m0 CODE 10 « fichier modifie : README.md », m8 CODE 12 « manifeste depose absent », les DIX autres verts. Puis `sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt` : les 12 signatures VÉRIFIÉES INTÉGRALEMENT avant toute écriture (le dépôt re-vérifie ce que le recoup avait établi — jamais une seule source de vérité), PUIS installées avec les manifestes vivants ; l'état de clé demeure « reelle (ceremonie hors-ligne, D87) ». **LE GARDE REPASSÉ : 12/12 arbres VERTS, code 0** — m0 vert (d941548…), m8 vert (621daf17…), les DIX intacts : LA DETTE DE CÉRÉMONIE DE L'ÈRE D162 EST SOLDÉE.

**LE BUILD EXÉCUTÉ (m8/build_m8.py construire(), graine 20261105, volume complet).** Le garde armé en tête PASSE (m0-m5+m8 tous verts) ; l'héritage re-vérifié de bout en bout : oracle M4 560 cas verts + oracle M5 365 cas verts (scénarios étendus D136) + structurels M3 524 + M4 492 + M5 312 verrous, l'image M5 composée confrontée OCTET PAR OCTET au scellé 0.6.0 (c1e46fb0…) ; le domaine assemblé (sys-01 le trombone, sys-02 le résolveur, sys-03 la twin) ; l'image PE32+ à SEPT sections composée (.text5 RX @0xA000, les fixtures dans la zone VIERGE 0x2EC0-0x2EFF, la version 0x00090001 : GESTE DE BUILD, jamais scellage) ; LA PREUVE R7 : **44 blocs octet-identiques au scellé 0.6.0**, les deltas .rdata/.text5/PE documentés ; LE HARNAIS M8 : **61/61 VERTS** (empreinte 628ff4de712d6ccb, graine 20261105 — V1 round-trip + concordance au plan, V2 le trombone au noyau simulé + le résolveur sur fixtures + LA TWIN au différentiel, V3 le fuzzing 300 modules 0 écart, V4 la falsification 15/15 mutations attrapées) ; **L'ARTEFACT m8/proxy.exe NÉ : 44 544 o (0xAE00), sha256 1492b0bc0792e1ab162338b414fb20573134e84d752b9d0657292421f8eb0cd4 — IDENTIQUE à la pièce de vérification du Task 76 : l'artefact né == l'artefact annoncé, le déterminisme tenu d'un poste à l'autre** ; LA CARTE GÉNÉRATION 8 VIVANTE (4 fragments chiffrés, signature Ed25519, 55 blocs indexés sur 7 artefacts — la clé publique e9cd8c549485… : LE TÉMOIN NE BOUGE PAS, la graine durable D144) ; le verrou croisé re-vérifié (signature OK, racine OK, 55 empreintes) ; le tableau de bord écrit (construction 0 erreur / 0 avertissement, défauts T1-T6 ouverts 0, changements hors journal 0, optimisations sans mesure 0).

**Frontières.** AUCUNE balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES) — la 0.9.0-dev.1 est posée par un GESTE DE BUILD, jamais un scellage : **la finale 0.9.0 attend le run terrain vert du chantier (d)** ; le scellé 0.6.0 INTACT (l'ancre R7 — 44 blocs octet-identiques au nouveau-né) ; l'état de clé du sceau « réelle » INTACT (la cérémonie du développeur, reçue et déposée — le labo n'a rien signé) ; le SSN du terrain demeure INCONNU du labo (les fixtures synthétiques font la preuve au harnais, le VRAI ntdll se lira au chantier (d)) ; la zone download/ (labo, non suivie) conserve la pièce rapatriée. Livrables : m8/proxy.exe (l'artefact 0.9.0-dev.1), m8/carte/ (les 8 pièces de la génération 8), v06/sceau-I/ (m0 re-signé + m8 signé, 12/12), scripts/sonder_coffre_sa.py (le sondage lecture seule par compte de service), scripts/rapatrier_ceremonie_m8.py (le rapatriement + le recoup de l'ère) ; consignations : la présente Entrée PAR SCRIPT, DECISIONS +D163 PAR SCRIPT, PLAN (le chantier M8-(c) RÉALISÉ), worklog +Task ID 78.

- SUITE : LA PASSATION (le bundle de la série 080 au miroir, l'ancien archivé versionné, GitHub porté à la pointe) ; puis LE CHANTIER M8-(d) — le kit terrain au coffre /test (le VRAI ntdll lu sur la machine du développeur, le motif confronté, la ligne comparée par les DEUX chemins), la finale 0.9.0 attend le vert.

"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Entrée 160" in texte:
    sys.exit("ECHEC : l'Entrée 160 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in texte:
    sys.exit("ECHEC : marqueur journal-des-builds introuvable")
i159 = texte.find("## Entrée 159")
if i159 < 0:
    sys.exit("ECHEC : l'Entrée 159 introuvable (l'ordre 159<160)")

nouveau = texte.replace(MARQUEUR, ENTREE + MARQUEUR, 1)

j159 = nouveau.find("## Entrée 159")
j160 = nouveau.find("## Entrée 160")
jm = nouveau.find(MARQUEUR)
if not (0 <= j159 < j160 < jm):
    sys.exit("ECHEC : l'ordre 159<160<marqueur n'est pas tenu "
             f"({j159}, {j160}, {jm})")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("Entrée 160 insérée (l'ordre 159<160<marqueur constaté)")
