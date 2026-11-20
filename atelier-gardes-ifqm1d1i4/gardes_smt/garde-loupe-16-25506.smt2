; PREUVE de la garde 25506 — la zone CADRE [0xe000,0xe3c0)
; (la garde tenue) ∧ (la négation de la sûreté) — UNSAT exigé
; benchmark generated from python API
(set-info :status unknown)
(declare-fun base () (_ BitVec 64))
(declare-fun adresse_effective () (_ BitVec 64))
(assert
 (let ((?x124 (bvadd base (_ bv4096 64))))
 (= adresse_effective ?x124)))
(assert
 (bvuge adresse_effective (_ bv57344 64)))
(assert
 (bvult adresse_effective (_ bv58304 64)))
(assert
 (or (bvult adresse_effective (_ bv57344 64)) (bvuge adresse_effective (_ bv58304 64))))
(check-sat)
