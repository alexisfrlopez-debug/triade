#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fabrique_cf3_v3d.py — LE MODÈLE CF3-v3 DÉCOMPOSÉ (W27PREUV, la vague 27,
prompt 5a). Le modèle v3 DÉMEURE VERBATIM (aucune règle, aucune action, aucun
lemme existant modifié) ; les QUATRE SOUS-LEMMES de connaissance bornée sont
AJOUTÉS avant le « end » — la décomposition du but attaquant qui franchit le
mur mémoire 4 Gio :

  L1a — L'ÉTAGE CONNAISSANCE du lemme 1 : une phrase NÉE que l'adversaire
        apprend ne le peut que par la reconstitution illicite PRÉCÉDENTE
        (le but attaquant K(p) décomposé de sa conjonction triple) ;
  L1c — LE PONT DES PARTS : toute reconstitution illicite est précédée des
        TROIS fuites tenues (les témoins datés) ;
  L2a — LA CHAÎNE DES PHRASES HÔTES [use_induction] : toute phrase hôte
        remonte à une phrase NÉE (l'induction sur la chaîne de préservation) ;
  L2b — L'ÉTAGE IMMÉDIAT du lemme 2 : tout emploi de la clé h(p) est précédé
        d'une phrase hôte (le pas arrière unique).

  L1 = L1a ∘ L1c (la transitivité de <) ; L2 = L2b ∘ L2a. L'argument de
  composition est consigné au rapport — chaque sous-lemme est vérifié SEUL,
  dans le budget mémoire du bac ; les lemmes originaux demeurent, INTACTS.
"""
import hashlib
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parent / "atelier-cf3-verdict-qa3k5putf" / "CF3-v3.spthy"
DST = ICI / "CF3-v3d.spthy"

src = SRC.read_text(encoding="utf-8")
ANCRE = "lemma temoin_atteignabilite_du_seuil:\n  \"All p #i #j. ReconstitutionIllicite(p) @ #i & K(p) @ #j ==> F\"\n\nend"
AJOUT = """lemma temoin_atteignabilite_du_seuil:
  \"All p #i #j. ReconstitutionIllicite(p) @ #i & K(p) @ #j ==> F\"

/* ==================== LA DÉCOMPOSITION (v3d, W27PREUV 5a) ================== */
/* Le but attaquant K(p) du LEMMA 1 était confronté à SA conjonction triple
 * (la reconstitution ET les trois parts tenues, chacune ordonnée) : la
 * recherche arrière explosait au mur mémoire 4 Gio. La décomposition sépare
 * les étages — CHAQUE sous-lemme est une question de connaissance bornée,
 * vérifiable seule ; la composition par transitivité de < est l'argument
 * consigné au rapport (jamais une réécriture du lemme original, qui demeure
 * INTACT ci-dessus, énoncé pour l'histoire et le run machine réelle). */

/* SOUS-LEMME L1a — L'ÉTAGE CONNAISSANCE : une phrase NÉE (PhraseVivante,
 * l'action des règles de naissance) que l'adversaire apprend ne le peut que
 * par la reconstitution illicite PRÉCÉDENTE. Le but K(p) est décomposé de la
 * conjonction triple : la source de la connaissance SEULE. */
lemma l1a_connaissance_par_reconstitution [use_induction]:
  \"All p #k #i. PhraseVivante(p) @ #k & K(p) @ #i ==>
     Ex #j. ReconstitutionIllicite(p) @ #j & #j < #i\"

/* SOUS-LEMME L1c — LE PONT DES PARTS : toute reconstitution illicite est
 * précédée des trois fuites TENUES (les actions PartTenue des règles de
 * fuite, antérieures à la consommation du fait persistant !PartAdverse).
 * La distinctivité des trois positions est portée par la fraîcheur des cinq
 * champs de !PartsDe (l'argument du registre, la forme garde les témoins). */
lemma l1c_reconstitution_exige_trois_parts:
  \"All p #j. ReconstitutionIllicite(p) @ #j ==>
     Ex x1 x2 x3 #j1 #j2 #j3. PartTenue(x1) @ #j1 & PartTenue(x2) @ #j2 &
       PartTenue(x3) @ #j3 & #j1 < #j & #j2 < #j & #j3 < #j\"

/* SOUS-LEMME L2a — LA CHAÎNE DES PHRASES HÔTES, PAR INDUCTION : toute phrase
 * hôte (le fait linéaire préservé par les migrations, clôtures et ouvertures)
 * remonte à une phrase NÉE — l'induction sur la chaîne de préservation, la
 * borne d'évaluation que le lemme entier ne franchissait pas. */
lemma l2a_chaine_des_phrases_hotes [use_induction]:
  \"All p #i. PhraseHote(p) @ #i ==>
     Ex #j. PhraseVivante(p) @ #j & (#j = #i | #j < #i)\"

/* L2 COMPOSÉ À L'INDUCTION — l'essai direct : la borne d'évaluation que le
 * lemme entier ne franchissait pas sans elle (l'annotation est LA différence ;
 * l'énoncé est celui du LEMMA 2, VERBATIM). */
lemma l2_compose_induction [use_induction]:
  \"All p #i. CleUtilisateurEmployee(h(p)) @ #i ==>
     Ex #j. PhraseVivante(p) @ #j & #j < #i\"

/* SOUS-LEMME L2b — L'ÉTAGE IMMÉDIAT, ANCRÉ À LA NAISSANCE. La première
 * formulation (PhraseHote(p) @ #j < #i) fut REFUTÉE par tamarin 1.12.0 —
 * l'occurrence d'un fait linéaire s'ancre à sa CONSOMMATION (le
 * modèle-témoin atelier-w27preuv/test_occ.spthy le démontre en trois pas :
 * ce n'est pas une attaque du protocole, c'est la sémantique d'occurrence).
 * L'ancre correcte de l'étage immédiat est la NAISSANCE : l'action de la clé
 * exige une phrase née AU PLUS TÔT À #i — la STRICTE (< #i) suit de la
 * disjointure des actions (aucune règle ne tire PhraseVivante ET
 * CleUtilisateurEmployee : la création et le changement tirent la naissance,
 * les cinq règles de clé ne la tirent pas) — l'argument consigné au rapport. */
/* LA PREMIÈRE FORMULATION, conservée RÉFUTÉE (le document vivant de la
 * sémantique d'occurrence — son verdict attendu est FALSIFIED : ce n'est pas
 * une attaque, c'est l'ancre ; voir test_occ.spthy). */
lemma l2b_refutee_occurrence [use_induction]:
  \"All p #i. CleUtilisateurEmployee(h(p)) @ #i ==>
     Ex #j. PhraseHote(p) @ #j & #j < #i\"

lemma l2b_emploi_exige_naissance [use_induction]:
  \"All p #i. CleUtilisateurEmployee(h(p)) @ #i ==>
     Ex #j. PhraseVivante(p) @ #j & (#j = #i | #j < #i)\"

end"""

assert ANCRE in src, "l'ancre de décomposition est introuvable — le modèle a-t-il bougé ?"
assert src.count("\nend") == 1
DST.write_text(src.replace(ANCRE, AJOUT), encoding="utf-8")
print(f"[v3d] {DST.name} écrit — le modèle v3 verbatim + 4 sous-lemmes")
print(f"[v3d] sha256 {hashlib.sha256(DST.read_bytes()).hexdigest()}")
