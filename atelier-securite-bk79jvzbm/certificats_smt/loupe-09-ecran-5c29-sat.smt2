; la BMC de démonstration — loupe-09-ecran @ 0x5c29
; la base symbolique SANS invariant externe : la négation de la sûreté est SAT
; (le modèle : un contre-exemple hors zone) — la borne n'est PAS statique, elle vit à :
;   la base rdx est une VALEUR RUNTIME (chargée ou recomputée) — la borne vit à l'INVARIANT EXTERNE (le champ du plan, le contrat de l'appelant, l'OS)
; benchmark generated from python API
(set-info :status unknown)
(declare-fun zone_fin () (_ BitVec 64))
(declare-fun disp () (_ BitVec 64))
(declare-fun idx () (_ BitVec 64))
(declare-fun base () (_ BitVec 64))
(assert
 (= zone_fin (_ bv65536 64)))
(assert
 (or (bvslt (bvadd (bvadd base (bvmul idx (_ bv1 64))) disp) (_ bv0 64)) (bvsge (bvadd (bvadd base idx) disp) zone_fin)))
(check-sat)
