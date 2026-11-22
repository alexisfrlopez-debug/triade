# PLAN GELÉ — K69MVT43J (la vague 15)
> L'atelier des gardes vivantes : faire vivre les 58 gardes de frontière dans
> l'artefact scellé et réduire le TCB de 58 à 11 assomptions externes —
> 24 déchargées par PREUVE z3 (UNSAT), 23 à la composition par la preuve de
> l'appelant, les 11 OS restantes nommées.
> Gelé AVANT toute preuve ; l'empreinte du registre TCB précède le premier run z3.

## Le mandat
Les 58 gardes de frontière (vagues 13-14) demeurent des contrôles à l'exécution ;
le présent atelier les réduit à leur noyau porteur :

(1) **DÉCHARGER PAR PREUVE les 24 invariants de layout CADRE (960 o)** : chaque
invariant statiquement connu passe au z3 — la preuve UNSAT (l'invariant ne peut
PAS être violé : la garde est déchargée) + LE CONTRÔLE NÉGATIF SAT par invariant
relâché d'une unité (la preuve reste portante — relâché d'un octet, le SAT tombe).
(2) **DÉCHARGER les 23 contrat-appelant à la composition** : la preuve de
l'appelant couvre la garde (la composition par preuve, le contrat nommé).
(3) **GARDER les 11 OS comme assomptions nommées** — le registre TCB réduit
documenté par étage 58→34→11.
(4) **ÉMETTRE les gardes restantes dans la marge vierge** (le modèle OPT-01
promu en corridor réel) : R4/R7 préservés — aucune adresse scellée ne bouge,
round-trip 100 %.
(5) **MESURER le coût par bloc au harnais émulé** (ratio nommé comme avant) ET
préparer le kit terrain pour la cible ≤1 % avec vrais appels système — le run
appartient au développeur.

## Les gestes
1. Le plan gelé ; le registre TCB ouvert AVANT la première preuve.
2. Les 24 UNSAT + 24 SAT-négatifs (z3, graines/versions consignées).
3. Les 23 décharges à la composition (la preuve de l'appelant citée par contrat).
4. L'émission en marge vierge (OPT-01), R4/R7, round-trip 100 %.
5. La mesure de coût par bloc au harnais ; le kit terrain pré-enregistré
   (agrégateur fail-closed).

## La vérification après modifications
58/58 décharges re-vérifiées + 58/58 mutations SAT ; une garde falsifiée REFUSÉE
aux deux bornes + face d'index au harnais ; empreintes des pièces scellées
intactes avant/après pour tout bloc non gardé ; consoles d'oracle
ligne-identiques ; sceau 14/14 avant/après ; kit terrain pré-enregistré avec
agrégateur fail-closed ; entrée append-only.

## Les refus
Jamais une garde déchargée sans preuve ; jamais le négatif SAT omis ; jamais une
adresse scellée déplacée ; jamais un chiffre terrain fabriqué.
