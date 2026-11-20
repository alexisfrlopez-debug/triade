; certificat BMC-intervalle — tls13-08 @ 0xc8e6
; idx ∈ [0, 0) la garde ; la négation (hors tampon) est UNSAT
; benchmark generated from python API
(set-info :status unknown)
(declare-fun n () Int)
(declare-fun idx () Int)
(declare-fun p () Int)
(assert
 (>= n 0))
(assert
 (>= idx 0))
(assert
 (< idx 0))
(assert
 (or (< (+ p idx) p) (>= (+ p idx) (+ p n))))
(check-sat)
