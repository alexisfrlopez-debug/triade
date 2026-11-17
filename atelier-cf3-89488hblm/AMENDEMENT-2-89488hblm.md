# AMENDEMENT 2 AU PLAN PRÉ-ENREGISTRÉ 89488hblm — L'ENCODAGE DU POINT (a)

**La raison technique (constatée au premier run, le 17/11)** : l'encodage
XOR du plan gelé (dcb2d56) est REFUSÉ par Apalache 0.63.0 :

    Assignment error: CF3Equiv.tla:84:6-85:48: Illegal assignment inside
    an assignment-free expression

La discipline d'affectation d'Apalache (son manuel, principles/
assignments.html) interdit la NÉGATION d'un système d'affectations : le
XOR relationnel (R ∧ ¬P) ∨ (¬R ∧ P) où R et P portent des conjonctions
primées est inencodable. Un second constat au passage (la sonde
ProbeDl) : la vérification bornée d'Apalache NE RAPPORTE PAS les
deadlocks par état (l'absence de transition n'y est pas observable) —
le mécanisme « deadlock comme détecteur » n'existe pas de ce côté.

**Le nouvel encodage — LES COPIES MIROIR (strictement plus fort)** :

1. **EQUIV_GARDE_r (13 runs, SMT non borné, longueur 0, INCHANGÉ du
   plan)** : Init = TypeOK, Inv = GP_r ⟺ GT_r — la garde Python (la
   transcription CF3Python.tla) contre la garde TLA+ extraite (GT, 13
   lignes auditable).

2. **EQUIV_IMAGE_r (13 runs, SMT non borné, longueur 1 — REMPLACE le
   XOR)** : l'état de base demeure INVARIANT ; la copie R porte l'image
   par la règle RÉELLE (CF3R == INSTANCE CF3 — zéro retranscription) ;
   la copie P porte l'image par la relation PYTHON (CFP == INSTANCE
   CF3Python). Next = CF3R!r ∧ CFP!RPy_r ; Inv = InvImage (copie R =
   copie P). NoError ⟹ : quand la règle réelle tire ET que la garde
   Python tient, les images COÏNCIDENT — l'aspect effet-à-effet, contre
   l'artefact réel.

3. **EQUIV_ACTIVATION_r (13 runs, SMT non borné, longueur 1 — AJOUT)** :
   la règle RÉELLE tire sur la copie R et pose marque ; Inv =
   marque = FALSE ∨ GP_r (la garde Python se lit sur la base inchangée).
   NoError ⟹ : quand la règle réelle tire, la garde Python TENAIT — le
   sens « réel ⟹ Python » des activations.

4. **L'ÉPINGLAGE TLC (13 runs + 1 contrôle, TLC, AJOUT)** : le sens
   manquant « Python ⟹ réel » (la garde Python prétend, la règle réelle
   refuse) n'est pas observable en SMT borné — il l'est en TLC, dont le
   DEADLOCK est rapporté par état. Sur les 4 096 représentants (e ∈
   {1, 2} × les composants bien typés — la réduction JUSTIFIÉE :
   l'uniformité de classe des gardes Python est PROUVÉE par LT1 (le
   point (c), SMT non borné), celle des gardes réelles par l'audit
   mécanique consigné audit_regles.py) : Next = (marque = FALSE ∧ le
   tir réel ∧ marque' = TRUE) ∨ (marque = FALSE ∧ ¬GP_r ∧ recopie) ∨
   (marque = TRUE ∧ recopie) — l'exploration BORNÉE (le témoin gèle
   après le premier pas). TLC exige : AUCUN deadlock (le sens Python ∧
   ¬tir réel) ET l'invariant marque = FALSE ∨ GP_r (le sens tir réel ∧
   ¬Python). Le contrôle : la garde mutée GPw_FalsifieConteneur (LA
   simplification fausse croisée par la campagne PBT) DOIT produire le
   deadlock.

**L'ENSEMBLE (avec l'amendement, l'équivalence du point (a))** : les
gardes équivalentes SANS PLAFOND D'ÉPOQUE (EQUIV_GARDE en SMT), les
images égales (EQUIV_IMAGE en SMT), les activations d'accord
(EQUIV_ACTIVATION en SMT + l'épinglage TLC dans les DEUX sens contre
l'artefact réel) — 39 runs SMT + 14 runs TLC pour le point (a), contre
26+26 prévus ; les OBLIGATIONS (garde-à-garde et effet-à-effet, par
règle, tout état bien typé) sont INCHANGÉES — seul l'encodage change,
forcé par l'outil, et il est STRICTEMENT PLUS FORT (la règle réelle
entre désormais DIRECTEMENT dans les preuves d'image et d'activation —
la transcription GT n'est plus la seule voie TLA+).

**Les contrôles (26 + 1, inchangés par la mutation)** : les 13 contrôles
GARDE (GPw ⟺ GT → Error 12) et les 13 contrôles IMAGE (la relation
mutée CFPw!RPyw_r — la garde intacte, l'effet dévié → InvImage violé →
Error 12) ; le contrôle de l'épinglage (le deadlock TLC). Les 26
MUTATIONS du plan gelé demeurent MOT POUR MOT (CF3PythonControles.tla).

**Les points (b) et (c) (INCHANGÉS sauf une précision)** : CF3O3.tla
intact (l'amendement 1 — le self-bouclage SuivantNul — demeure) ;
CF3Translation.tla : LT1 porte désormais les gardes PYTHON (GP) —
transitives aux gardes réelles PAR LES PREUVES DU POINT (a)
(EQUIV_GARDE + l'épinglage) — c'est la précision nommée : LT1 dit
« les gardes (telles qu'épinglées à l'artefact réel par (a)) sont
invariantes par translation » ; LT2 (la commutation des effets, les
règles RÉELLES des deux côtés) INCHANGÉ.

**Le livre des runs (phases B-C-D du plan, amendées)** :
- B : 13 EQUIV_GARDE + 13 EQUIV_IMAGE + 13 EQUIV_ACTIVATION + OB1 +
  OB2 + LT1 + LT2 = 42 runs SMT (NoError attendus) ;
- C : 13 contrôles GARDE + 13 contrôles IMAGE + CB1 + CB2 + CC1 + CC2 =
  30 runs SMT (Error 12 attendus) ;
- D : 13 épinglages TLC + 1 contrôle d'épinglage (deadlock attendu) +
  le compte 288 (TLC + Python, inchangé).

**Les clefs du verdict étendu (phase F, amendées)** :
equiv_garde_{r} × 13, equiv_image_{r} × 13, equiv_activation_{r} × 13,
tlc_epinglage_{r} × 13 (le double sens contre l'artefact réel),
controle_garde_{r}_attrape × 13, controle_effet_{r}_attrape × 13,
controle_epinglage_attrape, o3_couverture_smt, o3_non_vacuite_smt,
o3_compte_formes_tlc (288), controle_o3_couverture_attrape,
controle_o3_non_vacuite_attrape, translation_gardes_smt,
translation_effets_smt, controle_translation_gardes_attrape,
controle_translation_effets_attrape, pbt_rejeu_10000_stables (10000),
pbt_rejeu_10000_divergentes (0), pbt_rejeu_condense_identique (true) —
plus les 11 clefs consignées BIT-IDENTIQUES.

Le présent amendement est committé AVANT toute exécution des runs
amendés (la règle D204/D211 reconduite — le commit précède la donnée ;
le seul run exécuté sous le plan initial, equiv_garde_VoleKUser, suit
l'encodage INCHANGÉ du plan gelé : Init = TypeOK, Inv = OblGarde,
longueur 0).

---

## LE CORRECTIF DE L'AMENDEMENT 2 (avant tout run amendé) — deux leçons d'outil

1. **L'ÉNUMÉRABILITÉ TLC** : TypeOKClasses == TypeOK ∧ e ∈ {1, 2} n'est
   pas énumérable par TLC (« the right side of \IN is not enumerable » —
   le e ∈ Int de TypeOK) — réécrit en contraintes EXPLICITES finies
   (l'époque directement dans {1, 2}, les domaines des neuf autres
   composants) — la MÊME population : 4 096 représentants (vérifié au
   premier run : « 4096 distinct states generated »).
2. **LA PRÉCÉDENCE DES CONFIGS** : le drapeau CLI --init d'Apalache NE
   SURCHARGE PAS la section INIT du fichier de config (constaté : le
   même --init=TypeOK donne NoError sous MCE.cfg [INIT InitCopies] et
   l'erreur d'affectation sous MCC.cfg [INIT TypeOK]) — TOUT paramètre
   de run vit désormais DANS un config par run (73 configs générés :
   MCEg/MCEi/MCEa pour les obligations, MCCg/MCCi pour les contrôles,
   MCO_*, MCT_*) ; --length et --no-deadlock demeurent CLI (les précédents
   consignés les y ont toujours portés). Les runs de longueur 0 portent
   NEXT RecopieTout (non parcouru à profondeur 0 — le précédent C2 :
   --length=0 sous config à NEXT Next).
   L'INIT des obligations GARDE : InitCopies (TypeOK ∧ les copies
   couplées ∧ marque = FALSE) — les copies NE RESTREIGNENT PAS la base
   (elle parcourt TOUS les états bien typés) : l'obligation est la même
   que sous Init = TypeOK, l'initialisation des variables d'encodage en
   plus.
