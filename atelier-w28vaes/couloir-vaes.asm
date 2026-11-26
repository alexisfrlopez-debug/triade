; couloir-vaes · AES-256-GCM VAES/VPCLMULQDQ · le couloir pré-enregistré D273 (CIB-AES-105)
; Écrit en NOTATION sur copie laboratoire AVANT toute mesure (W27VAES, prompt 6) —
; sha256 consigné AVANT l'implémentation exécutable (le plan gelé, la même règle).
; Profil : x86-64 · VAES (ymm, 2 blocs AES par vAESENC) + VPCLMULQDQ (ymm, 2 CLMUL par instruction)
; Domaine : couloir de performance scellé W20PERF (a_aesgcm_vaes) — R4 contrat stable, R7 aucune
;   adresse scellée déplacée, R11 avant/après au journal OPT.
; Dépendances : aucune (le couloir est autonome — le référentiel est OpenSSL EVP au même volume)
;
; LES TROIS ÉTAGES, tels qu'écrits :
;
; ---- ÉTAGE 0 · LE DISPATCH HISSÉ HORS BOUCLE ----------------------------------
;   cpuid vaes? vpclmulqdq? avx2?  — UNE FOIS à l'entrée du couloir (jamais dans la boucle)
;   absent → refus nommé SILICIUM-ABSENT (aucun repli silencieux, jamais un chemin non mesuré)
;
; ---- ÉTAGE 1 · CTR × VAES (deux blocs par vAESENC) -----------------------------
;   J0 = IV(96 bits) || 0x00000001        ; le compteur initial, grand ordre
;   boucle (32 itérations pour 4 Kio) :
;     ymm0 = [J_{2i}   | J_{2i+1}]        ; les DEUX compteurs, un par voie
;     vpxor  ymm0, ymm0, rk0              ; l'éclaircissement initial (les deux voies)
;     vaesenc ymm0, ymm0, rk1  … rk13     ; TREIZE tours (AES-256 : 14 tours)
;     vaesenclast ymm0, ymm0, rk14        ; le dernier tour, sans MixColumns
;     vpxor  ymm0, ymm0, [clair+32i]      ; le masque ⊕ le clair → le chiffré
;     vmovdqu [chiffre+32i], ymm0         ; 32 octets par itération (2 blocs AES)
;   les rk_j sont des ymm BROADCASTS (la même clé de tour aux deux voies)
;
; ---- ÉTAGE 2 · GHASH × VPCLMULQDQ, KARATSUBA, HUIT BLOCS PAR PLI ---------------
;   H = E_K(0^128), réfléchi (l'ordre des octets inversé — le corps biségré de GCM)
;   les puissances H¹..H⁸ précalculées (huit produits, UNE fois par clé — hors boucle)
;   boucle (4 plis pour 4 Kio — 4 Kio = 32 blocs = 4 × 8) :
;     Z = (acc ⊗ H⁸)                      ; le pli du compte précédent
;       ⊕ (C₁ ⊗ H⁸) ⊕ (C₂ ⊗ H⁷) ⊕ (C₃ ⊗ H⁶) ⊕ (C₄ ⊗ H⁵)
;       ⊕ (C₅ ⊗ H⁴) ⊕ (C₆ ⊗ H³) ⊕ (C₇ ⊗ H²) ⊕ (C₈ ⊗ H¹)
;     NEUF produits indépendants par pli, chacun 128×128 par KARATSUBA :
;       lo = vpclmulqdq(a, b, 0x00)  ; les moitiés basses (DEUX voies par instruction)
;       hi = vpclmulqdq(a, b, 0x11)  ; les moitiés hautes
;       mid = vpclmulqdq(a⊕a', b⊕b', 0x00) ⊕ lo ⊕ hi   ; le terme croisé (3 CLMUL par produit)
;     les huit produits SOMMÉS en (V_lo, V_hi) — puis UNE SEULE réduction par pli :
;       V = L ⊕ H ⊕ (H ≪ 121) ⊕ (H ≪ 126) ⊕ (H ≪ 127) mod (x^128+x^127+x^126+x^121+1)
;       (la réduction EXACTE du corps réfléchi — le polynôme de GCM inversé)
;
; ---- ÉTAGE 3 · L'ENTRELACEMENT CTR×GHASH ----------------------------------------
;   le calendrier : pour chaque pli g, la frappe CTR du pli g+1 précède le pli GHASH de g —
;   les latences VAES (≈ 4-7 cycles) recouvrent les VPCLMULQDQ (≈ 4-10 cycles), les deux
;   familles partagent le port 0/5 sans se serialiser — le couloir entrelacé de W20PERF
;   (0,7271 c/B mesuré) en était la version AVX2/AES-NI ; celui-ci est la version VAES.
;
; ---- LA FIN : le tag ------------------------------------------------------------
;   T = GHASH_final(len(A) || len(C)) ⊕ E_K(J0)   ; l'épreuve des vecteurs dorés juge tout
;
; LES ÉPREUVES AVANT TOUTE MESURE (la porte, dans l'ordre) :
;   1. PARITÉ aux 20 vecteurs dorés NIST CAVP 14.0 (gcmEncryptExtIV256.rsp) OCTET POUR OCTET
;   2. CONTRÔLE NÉGATIF : la variante mutée (une clé de tour décalée) refusée au PREMIER vecteur
;   3. ROUND-TRIP : corridor-chiffré puis EVP-déchiffré == le clair (l'aller-retour inter-implémentations)
;   PUIS la mesure : n=20, cœur épinglé (affinité), 4 Kio, contre OpenSSL EVP AU MÊME VOLUME,
;   médianes, ratio, la cible ≤ 1,05 × EVP (pré-enregistrée D273, jamais re-tirée).
