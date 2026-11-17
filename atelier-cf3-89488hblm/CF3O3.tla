--------------------------- MODULE CF3O3 ---------------------------
(***************************************************************************
 * CF3O3 — LE LEMME O3 PAR SMT NON BORNÉ (l'instruction 89488hblm, point
 * (b) : « explicite et décharge le lemme O3 (bijection 288 formes ↔
 * image des états bien typés satisfaisant l'invariant) par SMT non
 * borné, en distinguant clairement ce qui est prouvé de ce qui est
 * énuméré borné »).
 *
 * LA FONCTION D'ABSTRACTION α : un état → sa FORME — l'époque projetée
 * sur ses DEUX classes {1} (l'époque du départ) et {≥2} (la classe
 * uniforme — D198), les NEUF autres composants inchangés. Hors I4
 * (e < 1), la classe vaut 0 : HORS DOMAINE (aucune forme).
 *
 * CE QUI EST PROUVÉ PAR SMT NON BORNÉ (les deux obligations) :
 *   OB1 — LA COUVERTURE (l'image ⊆ le domaine des formes) : pour TOUT
 *     état bien typé satisfaisant Inv — e ∈ Int NON BORNÉ — la forme
 *     α(s) satisfait FormDomain. C'est l'argument qui rend la preuve
 *     par formes finies COMPLÈTE sur l'espace non borné des époques :
 *     I4 (e ≥ 1) force la classe dans {1, 2}, QUELLE QUE SOIT e.
 *   OB2 — LA NON-VACUITÉ PAR FORME (le domaine ⊆ l'image) : toute forme
 *     du domaine a un témoin — l'état construit en instantiant la
 *     classe en époque (1 → e = 1, 2 → e = 2) — qui est bien typé,
 *     satisfait Inv, et dont la forme EST la forme donnée (α∘ι = id).
 *   OB1 ∧ OB2 : l'image de {TypeOK ∧ Inv} par α est EXACTEMENT
 *   FormDomain (la surjection et l'injection des formes).
 *
 * CE QUI EST ÉNUMÉRÉ BORNÉ (jamais prétendu autrement) :
 *   |FormDomain| = 288 — le NOMBRE de formes. Énuméré DEUX FOIS par
 *   des outils indépendants : le TLC (l'énumération exhaustive des
 *   états de FormeDomaineEtat — tlc_o3_compte, 288 attendus) et le
 *   Python (verifie_couverture_288.py — les 288 formes, chacune
 *   atteinte, aucune hors Inv). Les époques représentatives
 *   {1, 2, 3, 7, 50, 1000} de la vague 5 demeurent des TÉMOINS, plus
 *   jamais des preuves.
 *
 * LES CONTRÔLES NÉGATIFS (l'affaiblissement volontaire, attrapé) :
 *   CB1 — OB1 SANS I4 (l'hypothèse affaiblie : e ∈ Int sans e ≥ 1) :
 *     l'état e = 0 (bien typé, I1-I3 tenus) a sa classe = 0 — HORS
 *     domaine : un contre-exemple DOIT être produit. I4 est PORTANTE.
 *   CB2 — OB2 avec le domaine des formes SANS I1 (secret sans seuil) :
 *     la forme secret = TRUE ∧ sait = {} n'a AUCUN témoin Inv — un
 *     contre-exemple DOIT être produit. I1 est PORTANTE.
 ***************************************************************************)

EXTENDS CF3

(* la classe d'époque : 1, ≥2 — ou 0 (hors domaine, e < 1) *)
Classe == IF e = 1 THEN 1 ELSE IF e >= 2 THEN 2 ELSE 0

(* la forme d'un état : la classe AU LIEU de l'époque, le reste tel quel *)
FormeOf == <<Classe, phase, sait, trap_ok, cf2_ok, secret, accepte,
             detruit, destr_injuste, media_corrompu>>

(* le domaine des formes — les indices : 1=classe, 2=phase, 3=sait,
 * 4=trap_ok, 5=cf2_ok, 6=secret, 7=accepte, 8=detruit,
 * 9=destr_injuste, 10=media_corrompu *)
FormDomain(f) ==
  /\ f[1] \in {1, 2}
  /\ f[2] \in {"canonique", "brouillon"}
  /\ f[3] \in SUBSET Elements
  /\ f[4] \in BOOLEAN
  /\ f[5] \in BOOLEAN
  /\ f[6] \in BOOLEAN
  /\ f[7] \in BOOLEAN
  /\ f[8] \in BOOLEAN
  /\ f[9] \in BOOLEAN
  /\ f[10] \in BOOLEAN
  /\ (f[6] = FALSE \/ Cardinality(f[3]) = 3)   \* I1 : secret ⟹ seuil 3
  /\ f[9] = FALSE                              \* I2 : pas d'injustice
  /\ f[5] /\ f[10] = FALSE                     \* I3 : CF2 et média intacts

(* OB1 — LA COUVERTURE : tout état bien typé ∧ Inv a sa forme AU DOMAINE.
 * Vérifié : Init = TypeOK /\ Inv, Inv = OblOB1, longueur 0. *)
OblOB1 == FormDomain(FormeOf)

(* le domaine des formes VU COMME UN ÉTAT : la classe instantiée en
 * époque (le témoin ι de chaque forme — 1 → e = 1, 2 → e = 2) *)
FormeDomaineEtat ==
  /\ e \in {1, 2}
  /\ phase \in {"canonique", "brouillon"}
  /\ sait \in SUBSET Elements
  /\ trap_ok \in BOOLEAN
  /\ cf2_ok \in BOOLEAN
  /\ secret \in BOOLEAN
  /\ accepte \in BOOLEAN
  /\ detruit \in BOOLEAN
  /\ destr_injuste \in BOOLEAN
  /\ media_corrompu \in BOOLEAN
  /\ (secret = FALSE \/ Cardinality(sait) = 3)
  /\ destr_injuste = FALSE
  /\ cf2_ok /\ media_corrompu = FALSE

(* OB2 — LA NON-VACUITÉ PAR FORME : toute forme du domaine a un témoin
 * bien typé, Inv, de forme elle-même (α∘ι = id : Classe = e pour
 * e ∈ {1, 2}). Vérifié : Init = FormeDomaineEtat, Inv = OblOB2,
 * longueur 0. *)
OblOB2 == Inv /\ Classe = e

(* CB1 — l'hypothèse affaiblie : Inv SANS I4 (l'époque peut être < 1) *)
InvSansI4 == TypeOK /\ I1 /\ I2 /\ I3

(* CB2 — le domaine des formes affaibli : SANS I1 (secret sans seuil) *)
FormDomainFaible ==
  /\ e \in {1, 2}
  /\ phase \in {"canonique", "brouillon"}
  /\ sait \in SUBSET Elements
  /\ trap_ok \in BOOLEAN
  /\ cf2_ok \in BOOLEAN
  /\ secret \in BOOLEAN
  /\ accepte \in BOOLEAN
  /\ detruit \in BOOLEAN
  /\ destr_injuste = FALSE
  /\ cf2_ok /\ media_corrompu = FALSE

(* l'énumération TLC du compte : le self-bouclage (TLC refuse une action
 * suivante constante — l'amendement nommé du 17/11 : SuivantNul était
 * FALSE, l'énumération des états de FormeDomaineEtat est INCHANGÉE) ;
 * l'invariant vide tautologique — TLC compte : 288 attendus *)
SuivantNul ==
  UNCHANGED <<e, phase, sait, trap_ok, cf2_ok, secret, accepte,
              detruit, destr_injuste, media_corrompu>>
Tautologie == TRUE
=============================================================================
