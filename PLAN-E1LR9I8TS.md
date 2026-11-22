# PLAN GELÉ — E1LR9I8TS (la vague 15)
> L'atelier triage : livrer le pipeline de triage des rapports adopteurs et le
> digest par release, sans JAMAIS amender le protocole automatiquement.
> Gelé AVANT toute donnée.

## Le mandat
(1) **LA VALIDATION À L'ENTRÉE** (schéma, scan de secrets, signature si
présente) fail-closed ; LE CLUSTERING MÉCANIQUE des classes de refus, défauts
F/L, doc_confusion, frontière de capacité par famille ; les rapports de versions
de schéma différentes JAMAIS poolés sans note de périmètre.
(2) **LE TRIAGE PROPOSE des décisions** (Dxxx : grammaire/gabarit, nouvelle
classe X + vecteur de falsification, révision doc, raffinement budget) ;
l'arbitrage appartient au développeur ; le journal est append-only (aucune
réécriture) ; le codage officiel des défauts : double annotation κ≥0,61 sur
n≥50 (kit annotateur), arbitrage 5 points.
(3) **LE DIGEST PAR RELEASE généré mécaniquement** (comptes, refus par famille,
distributions tokens aux périmètres étiquetés, frontière de capacité) + les notes
curatées ; zéro secret ; contributeurs acknowledged opt-in (CC-BY-4.0) ; le
dépôt Zenodo du digest DEMEURE le geste du développeur.

## Les gestes
1. Le plan gelé ; la validation d'entrée (schéma + secrets + signature) + les
   contrôles négatifs (rapport malformé refusé, rapport porteur d'un secret
   planté refusé, un pooling inter-schéma silencieux attrapé).
2. Le clustering mécanique (classes de refus, F/L, doc_confusion, frontière).
3. Le générateur de décisions proposées (jamais une décision prise).
4. Le générateur de digest (recomputable depuis les rapports bruts, zéro
   divergence) + le scan de secrets du digest + le contrôle négatif.

## La vérification après modifications
Contrôles négatifs vécus ; digest recomputable depuis les rapports bruts (zéro
divergence) ; aucune amendment du protocole sans décision humaine consignée ;
zéro secret dans le digest (scan + contrôle négatif) ; entrée append-only.

## Les refus
Jamais une décision auto-appliquée ; jamais un pool silencieux inter-schéma ;
jamais un secret dans le digest ; jamais une réécriture du journal.
