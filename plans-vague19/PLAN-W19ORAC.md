# PLAN GELÉ — W19ORAC (moteur d'oracle natif étendu aux 52 blocs, performance à contrôles inchangés)

> Instruction source : Prompt 4 du message du maître du 24/11/2026 12:42. Contrôles
> inchangés : même plan d'adresses, mêmes octets scellés, aucun contrôle retiré.

## Périmètre
1. `scripts/vague19/moteur_oracle_etendu.py` — le pilote qui porte le moteur natif existant
   (`atelier-oracles-8hguph5ee/moteur_oracles`) aux 52 descripteurs de blocs de la génération 7
   (reconstruits par import des modules de build de laboratoire m4/m5 — JAMAIS depuis la carte
   chiffrée ni le coffre réel), avec :
   - le plan d'adresses et les octets scellés inchangés (le bloc lu à son RVA dans l'image de
     laboratoire, sha256 recoupé) ;
   - l'audit jumeau ligne-identique PAR BLOC (console native == console du jumeau) ;
   - l'audit chaîné 1-sur-10 conservé (chaque dixième bloc rejoué et confronté champ par champ) ;
   - un mémo CONTENT-ADDRESSED lié à (empreinte du bloc + configuration moteur + graine) :
     tout octet changé = miss, jamais une session figée ;
   - la cristallisation incrémentale généralisée par dédup content-addressed des rebuilds.
2. Pré-enregistrement de la cible : session T < 10 s à volumes d'oracle égalisés, liste de
   commandes fixe, chronomètre monotone, n ≥ 5 par configuration ;
   `atelier-w19-oracle/preregistrement.json` consigné avant mesure.

## Contraintes
- R11 : la mesure avant/après est consignée ; R4/R7 : aucune adresse scellée ne bouge ;
  les empreintes des pièces scellées sont recoupées avant et après chaque run.
- Si un contrôle ne peut pas être rendu (jumeau absent, vecteurs manquants), il est NOMMÉ et la
  pièce reste EN ATTENTE — jamais simulé.

## Critères d'acceptation
- Zéro divergence ligne-identique sur l'échantillon d'audit consigné.
- Les consoles d'oracle capturées identiques ligne pour ligne aux originales (là où les
  originales existent).
- Un shim de lanceur volontairement muté attrapé à la première ligne (porte honnête/faux).
- Audit 1-sur-10 déclenché et confronté champ par champ.
- Médianes publiées aux opérandes non arrondis (le lecteur recompose).
