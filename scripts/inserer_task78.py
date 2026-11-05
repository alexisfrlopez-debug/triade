#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_task78.py — worklog.md : appends la Task ID 78 (rejeu REFUSÉ
fail-closed si elle existe déjà)."""

import sys

CHEMIN = "worklog.md"

TACHE = """
## Task ID 78 — « signatures déposées dans le drive /test » : LA CÉRÉMONIE DE L'ÈRE M8 PASSÉE SUR PIÈCES — LA DETTE D162 SOLDÉE, LE GARDE VERT 12/12, L'ARTEFACT 0.9.0-dev.1 NÉ DU BUILD (déterministe : 1492b0bc… == la pièce du Task 76) ; le disque labo encore recyclé (troisième fois), la reprise D159 rejouée, le relais compte de service portant le geste (le jeton OAuth encore mort) (05/11)

- L'OUVERTURE (sur pièces, jamais sur mémoire) : le message du
  développeur annonce la remise ; l'état constaté : (1) le disque
  labo RECYCLÉ ENCORE — HEAD 402508f, worklog Task 65, Entrée 147,
  D152 : TOUT le jalon M7 et l'ère M8 absents du disque (troisième
  recyclage : Entrée 132, m7d/D159, aujourd'hui) ; (2) le jeton OAuth
  du relais MORT (invalid_grant — la deuxième fois, le même symptôme
  que le 29/10).
- LA REPRISE D159 REJOUÉE : ls-remote → origin à 7079df1 (EXACTEMENT
  la pointe consignée par la passation Task 77, bundle 080-b7b6e01) ;
  fetch + fast-forward PROPRE (les seuls écarts : 9 fichiers en bits
  de mode, ZÉRO contenu) ; les 24 gestes revenus : M6-(d) run terrain
  vert + LA FINALE 0.7.0, M7 ENTIER jusqu'à LA FINALE 0.8.0 (jalon
  franchi, D159 née de la reprise précédente), l'ère M8 (a/b/c :
  D160/D161/D162) et le kit de cérémonie Task 77 ; les instruments
  réinstallés PAR LA PROCÉDURE consignée à la reprise m7d (pip :
  keystone-engine 0.9.2, capstone 5.0.9, pefile, pynacl 1.6.2,
  unicorn 2.1.4) — RIEN ne s'est perdu (troisième recyclage, zéro
  perte).
- LE RELAIS COMPTE DE SERVICE PORTE LE GESTE (scripts/sonder_coffre_
  sa.py, LECTURE SEULE — le mécanisme du 29/10 étendu au sondage du
  coffre entier) : racine 14 entrées (l'export de continuité 0.8.0
  posé, le miroir à la pointe 080-b7b6e01), /Cérémonie 17 (le
  LISEZMOI de l'ère en place), /test 10 — LA PIÈCE : signatures-I.txt
  (md5 annoncé ab22512a6864…).
- LE RAPATRIEMENT + LE RECOUP (scripts/rapatrier_ceremonie_m8.py,
  lecture seule sur le dépôt) : md5 MATCH après écriture (1 703 o) ;
  L'ANCRE DE CLÉ tenue (cle-publique-I.txt == 173fae9c75229b15…) ;
  12/12 lignes valides ; LE RECOUP DE L'ÈRE : les DIX arbres inchangés
  (m1-m7, demo, terrain, v06) portent les MÊMES signatures que les
  déposées du 04/11 — Ed25519 déterministe : la réutilisation de la
  clé du 04/11 PROUVÉE par la comparaison bit à bit, sans jamais voir
  la clé privée ; m0 RE-SIGNÉ (d941548… le registre étendu), m8 ARBRE
  NEUF (621daf17…) ; les empreintes vivantes == a-signer.txt 12/12 ;
  chaque signature VÉRIFIÉE Ed25519 contre 173fae9c… — RECOUPE
  INTÉGRAL VERT 12/12.
- LE DÉPÔT CANONIQUE : le garde AVANT nommait la dette EXACTEMENT
  (m0 CODE 10 « fichier modifie : README.md », m8 CODE 12 « manifeste
  depose absent », les DIX verts) ; sceau_I.py deposer --cle : les 12
  signatures VÉRIFIÉES INTÉGRALEMENT avant toute écriture, PUIS
  installées (manifestes vivants), l'état « reelle » INTACT ; LE
  GARDE REPASSÉ : 12/12 arbres VERTS code 0 — LA DETTE D162 SOLDÉE.
- LE BUILD EXÉCUTÉ (m8/build_m8.py construire(), graine 20261105,
  volume complet) : le garde en tête PASSE ; l'héritage re-vérifié
  (oracle M4 560 + M5 365 cas verts, structurels M3 524 + M4 492 +
  M5 312 verrous, l'image M5 == scellé 0.6.0 octet/octet) ; la preuve
  R7 : 44 blocs octet-identiques au scellé 0.6.0 ; le harnais M8
  61/61 VERTS (empreinte 628ff4de…, graine 20261105) ; L'ARTEFACT
  m8/proxy.exe NÉ : 44 544 o, sha256 1492b0bc0792e1ab162338b414fb2057
  3134e84d752b9d0657292421f8eb0cd4 — IDENTIQUE à la pièce de
  vérification du Task 76 (le déterminisme d'un poste à l'autre) ;
  LA CARTE GÉNÉRATION 8 vivante (4 fragments chiffrés, signature
  Ed25519, 55 blocs sur 7 artefacts, le témoin e9cd8c549485… ne
  bouge pas — graine durable D144) ; verrou croisé 55 empreintes
  (signature OK, racine OK) ; tableau de bord écrit (0 défaut ouvert,
  0 changement hors journal).
- FRONTIÈRES : AUCUNE balise ne bouge (win 0.6.0 / linux 0.7.0 /
  riscv 0.8.0 INTACTES — la 0.9.0-dev.1 est un GESTE DE BUILD, jamais
  un scellage : la finale 0.9.0 attend le run terrain vert du (d)) ;
  le scellé 0.6.0 INTACT (l'ancre R7) ; l'état de clé « réelle »
  INTACT (le labo n'a RIEN signé — la cérémonie appartient au
  développeur, D87/D162) ; le SSN du terrain INCONNU du labo (les
  fixtures synthétiques font la preuve au harnais) ; download/ la
  zone labo (la pièce rapatriée y demeure, non suivie).
- Consignations : JOURNAL_TRAVAIL +Entrée 160 PAR SCRIPT (ordre
  159<160<marqueur, rejeu REFUSÉ), DECISIONS +D163 PAR SCRIPT (à la
  suite de D162), PLAN (le chantier M8-(c) RÉALISÉ —
  scripts/maj_plan_m8c.py), ce worklog +Task ID 78 ; scripts suivis :
  inserer_entree_160.py, inserer_d163.py, maj_plan_m8c.py,
  sonder_coffre_sa.py, rapatrier_ceremonie_m8.py.
- SUITE : LA PASSATION (le bundle de la série 080 au miroir, l'ancien
  archivé versionné, GitHub porté à la pointe) ; puis LE CHANTIER
  M8-(d) — le kit terrain au coffre /test (le VRAI ntdll lu sur la
  machine du développeur, le motif confronté, la ligne comparée par
  les DEUX chemins, tout stub divergent = refus nommé), la finale
  0.9.0 attend le vert.

Stage Summary:
- LA CÉRÉMONIE DE L'ÈRE M8 EST PASSÉE SUR PIÈCES : la remise du
  développeur (signatures-I.txt, 1 703 o, md5 ab22512a… MATCH)
  rapatriée du coffre /test par le RELAIS COMPTE DE SERVICE (le
  jeton OAuth encore mort), recoupée INTÉGRALEMENT avant dépôt —
  l'ancre de clé 173fae9c… tenue, les DIX signatures des arbres
  inchangés IDENTIQUES aux déposées du 04/11 (la clé réutilisée
  PROUVÉE par le déterminisme Ed25519), m0 re-signé, m8 neuf,
  empreintes == a-signer.txt 12/12, Ed25519 12/12.
- LA DETTE D162 EST SOLDÉE : le dépôt canonique a installé les 12
  signatures (l'atomicité vérifiée AVANT écriture), le garde REPASSÉ
  est VERT 12/12 (code 0).
- L'ARTEFACT 0.9.0-dev.1 EST NÉ DU BUILD : 44 544 o, sha256
  1492b0bc… IDENTIQUE à la pièce de vérification du Task 76 (le
  déterminisme d'un poste à l'autre, à travers un recyclage de disque
  et une reprise D159) ; la carte génération 8 vivante (le témoin ne
  bouge pas), le verrou croisé 55 empreintes, la preuve R7 (44 blocs
  octet-identiques au scellé 0.6.0), le harnais 61/61.
- LE POSTE A ENCORE ÉTÉ RECYCLÉ (troisième fois) : la reprise D159
  rejouée au geste même — fetch + pointe consignée 7079df1, les
  instruments par leur procédure ; RIEN ne s'est perdu.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Task ID 78" in texte:
    sys.exit("ECHEC : la Task ID 78 existe déjà")

if not texte.endswith("\n"):
    texte += "\n"
texte += TACHE

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(texte)
print("Task ID 78 apposée au worklog (append-only)")
