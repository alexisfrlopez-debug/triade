; PREUVE de la garde 60098 — la zone CTX [0x500000,0x501000)
; (la garde tenue) ∧ (la négation de la sûreté) — UNSAT exigé
; benchmark generated from python API
(set-info :status unknown)
(declare-fun base () (_ BitVec 64))
(declare-fun adresse_effective () (_ BitVec 64))
(assert
 (let ((?x124 (bvadd base (_ bv1 64))))
 (= adresse_effective ?x124)))
(assert
 (bvuge adresse_effective (_ bv5242880 64)))
(assert
 (bvult adresse_effective (_ bv5246976 64)))
(assert
 (or (bvult adresse_effective (_ bv5242880 64)) (bvuge adresse_effective (_ bv5246976 64))))
(check-sat)
