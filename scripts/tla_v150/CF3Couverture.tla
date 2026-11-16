--------------------------- MODULE CF3Couverture ---------------------------
(***************************************************************************
 * CF3Couverture — LE LEMME DE COUVERTURE (la vague 5, l'instruction
 * oc2y014vx, point 1) : « tout état concret atteignable de la sémantique
 * opérationnelle est représenté par au moins une des 288 formes (par
 * construction de l'abstraction + vérification Apalache/SMT d'une
 * obligation de couverture) ».
 *
 * LA STRUCTURE DE LA PREUVE, EN TROIS OBLIGATIONS :
 *   (O1) LA TOTALITÉ DE α — la fonction d'abstraction (projetter chaque
 *        composant d'un état concret sur son domaine d'abstraction :
 *        phase, sait, les booléens, et l'époque sur ses DEUX classes
 *        {1} et {≥2}) est définie sur tout état dont les composants
 *        vivent dans leurs domaines. Dans le portage TLA+, les domaines
 *        de α SONT exactement les contraintes TypeOK — l'obligation
 *        devient : TOUT état atteignable satisfait TypeOK.
 *   (O2) L'INDUCTIVITÉ DE LA COUVERTURE — Couverture == TypeOK est
 *        inductive : Init l'établit, chaque règle la préserve (Apalache,
 *        entiers NON bornés). Combinée à (O1) : tout état atteignable
 *        est dans le domaine de α — la totalité est MÉCANIQUE.
 *   (O3) L'EXHAUSTIVITÉ DES FORMES — l'ensemble des 288 formes
 *        (l'énumération de forme_domaines, l'époque par classes) est
 *        EXACTEMENT l'image de {TypeOK ∧ Inv} par α (la bijection est
 *        vérifiée côté Python : verifie_couverture_288.py — 288 formes,
 *        chacune atteinte, aucune hors Inv).
 *   (O1)∧(O2)∧(O3) + l'inductivité de Inv (déjà déchargée : CF3.tla)
 *   ⟹ LE LEMME : tout état concret atteignable est représenté par au
 *   moins une des 288 formes — et la preuve de préservation sur les
 *   288 formes couvre donc TOUT l'espace atteignable.
 *
 * LE CONTRÔLE NÉGATIF (un vérificateur qui n'attrape pas ne vaut rien) :
 *   CouvertureFaible affaiblit le domaine de phase à {canonique} seul —
 *   OuvrirCorrect mène à phase = "brouillon" : un contre-exemple DOIT
 *   être produit (Error 12 attendu).
 ***************************************************************************)

EXTENDS CF3

Couverture == TypeOK

(* Le contrôle négatif : le domaine de phase AMPUTÉ de "brouillon". *)
CouvertureFaible ==
  /\ e \in Int
  /\ phase = "canonique"
  /\ sait \in SUBSET Elements
  /\ trap_ok \in BOOLEAN
  /\ cf2_ok \in BOOLEAN
  /\ secret \in BOOLEAN
  /\ accepte \in BOOLEAN
  /\ detruit \in BOOLEAN
  /\ destr_injuste \in BOOLEAN
  /\ media_corrompu \in BOOLEAN

=============================================================================
