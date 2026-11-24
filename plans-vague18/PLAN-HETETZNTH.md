# PLAN GELÉ — HETETZNTH — le kit anti-rollback R10 à compteur NV TPM 2.0

## L'instruction, en une phrase
Pré-enregistrer un kit où le plancher de version est un compteur NV TPM 2.0 incrémenté
à chaque scellage et lu au chargement ; refus nommés RETOUR-EN-ARRIERE, ANCRE-PERDUE ;
kit éprouvé sur SIMULATEUR, run matériel EN ATTENTE.

## Le mécanisme (spécifié avant le code)
- compteur NV monotone (index consigné) : `NV_Increment` à chaque scellage ;
- au chargement : lecture avant toute exécution ; `version_scellée < compteur` →
  RETOUR-EN-ARRIERE ; compteur absent/inaccessible → ANCRE-PERDUE (fail-closed) ;
- TPM clear / ownership takeover → ANCRE-PERDUE, jamais de réinitialisation silencieuse ;
- la restauration cohérente binaire + état est REFUSÉE parce que le compteur NV survit ;
- aucun appel réseau.

## Ce qui sera livré
`simulateur_nv.py` (NV en mémoire + journal, sémantique TPM 2.0 nommée),
`kit_tpm_r10.py` (porte de chargement + agrégateur fail-closed qui refuse tout run
manquant), autotest 12/12 (nominal, rollback binaire, restauration cohérente, compteur
absent, TPM clear, incrément non monotone, agrégateur partiel refusé), rapport.

## Statut annoncé d'avance
« mécanisme éprouvé sur simulateur, run matériel EN ATTENTE » — aucun chiffre matériel.
