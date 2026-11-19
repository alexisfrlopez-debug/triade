---------------------- MODULE CF3FideliteEtendu ---------------------
(***************************************************************************
 * CF3Fidelite — LA REPRODUCTION EXACTE DES COMPTES BORNÉS D187 (le
 * contrôle de fidélité de l'instruction 6zqo2h60n) : la variante
 * plafond (e <- min(e+1, EpoquesMax)) PLUS le compteur de profondeur
 * prof — l'explorateur D187 coupait l'exploration à profondeur 6
 * (les états ATTEINTS à profondeur ≤ 6 comptés, leurs successeurs non
 * générés). Chaque règle s'exécute via Pas(A) : garde prof < 6,
 * prof' = prof + 1.
 *
 * La profondeur ne compte PAS dans l'identité d'état : la clause VIEW
 * du fichier de configuration déduplique par l'état ABSTRAIT (vars) —
 * la convention même de l'explorateur Python (un état atteint à
 * plusieurs profondeurs compte UNE fois, à sa profondeur minimale —
 * l'exploration en largeur la trouve d'abord).
 *
 * Attendu : 154 états distincts — le compte consigné D187.
 ***************************************************************************)

EXTENDS CF3PlafondEtendu, Naturals

VARIABLE
  \* @type: Int;
  prof

ProfMax == 6   (* la borne de profondeur de l'explorateur D187 *)

Pas(A) ==
  /\ prof < ProfMax
  /\ A
  /\ prof' = prof + 1

NextFidelite ==
  \/ Pas(VoleKUser)
  \/ Pas(VoleSSerrure)
  \/ Pas(VoleSPiege)
  \/ Pas(FalsifieConteneur)
  \/ Pas(FalsifiePiege)
  \/ Pas(RejoueEpoquePassee)
  \/ Pas(OuvrirCorrect)
  \/ Pas(OuvrirPhraseErronee)
  \/ Pas(OuvrirAncienCouple)
  \/ Pas(Verifier)
  \/ Pas(CrashPendantSession)
  \/ Pas(CloturerCorrectePlafond)
  \/ Pas(CloturerPhraseErronee)

InitFidelite == Init /\ prof = 0

SpecFidelite == InitFidelite /\ [][NextFidelite]_<<vars, prof>>

Vue == vars

=============================================================================
