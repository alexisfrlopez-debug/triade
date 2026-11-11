------------------------ MODULE CF3Controle ------------------------
(***************************************************************************
 * CF3Controle — LES CONTRÔLES NÉGATIFS (la non-vacuité du vérificateur
 * Apalache) : la méthodologie du pas inductif (--init=Inv) ne vaut que
 * si l'outil ATTRAPE un invariant non inductif. Deux contrôles :
 *
 * C1 — InvFaible : l'invariant I1-I4 SANS la contrainte sait ⊆
 *     Elements (le TypeOK réduit aux affectations sur un univers ÉTENDU
 *     d'une chaîne étrangère) : depuis sait = {KUser, SSerrure, junk1}
 *     (cardinalité 3, secret appris), VoleSPiege mène à sait de
 *     cardinalité 4 avec secret — I1 VIOLÉ : un contre-exemple DOIT
 *     être produit (la preuve que Cardinality est réellement raisonné
 *     par le SMT, pas ignoré).
 *
 * C2 — Faux : e = 99, violé dès l'état initial.
 ***************************************************************************)

EXTENDS CF3

UniversEtendu == Elements \union {"junk1"}

InvFaible ==
  /\ e \in Int
  /\ phase \in {"canonique", "brouillon"}
  /\ sait \in SUBSET UniversEtendu
  /\ trap_ok \in BOOLEAN
  /\ cf2_ok \in BOOLEAN
  /\ secret \in BOOLEAN
  /\ accepte \in BOOLEAN
  /\ detruit \in BOOLEAN
  /\ destr_injuste \in BOOLEAN
  /\ media_corrompu \in BOOLEAN
  /\ I1 /\ I2 /\ I3 /\ I4

Faux == e = 99
=============================================================================
