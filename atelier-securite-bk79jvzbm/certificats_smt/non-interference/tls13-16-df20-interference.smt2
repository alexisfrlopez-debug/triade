; la non-interférence RÉFUTÉE — tls13-16 @ 0xdf20
; le site adresse dépend du secret : SAT (le contre-exemple au modèle)
; benchmark generated from python API
(set-info :status unknown)
(declare-fun s2 () (_ BitVec 64))
(declare-fun s1 () (_ BitVec 64))
(declare-fun v2 () (_ BitVec 64))
(declare-fun v1 () (_ BitVec 64))
(assert
 (and (and (distinct s1 s2) true)))
(assert
 (and (distinct v1 v2) true))
(check-sat)
