; couloir-vaes512.asm · AES-256-GCM VAES512/VPCLMULQDQ · L'ÈRE NOUVELLE 512-bit (W29VAES512)
; Écrit en NOTATION sur copie laboratoire AVANT toute mesure (prompt 3 de la vague 29)
; — sha256 consigné AVANT l'implémentation exécutable (le plan gelé, la même règle R5).
; Profil : x86-64 · VAES512 (zmm, QUATRE blocs AES par vAESENC) + VPCLMULQDQ (zmm, QUATRE
;   produits par passe) — la voie 512-bit que le résidu structurel de CIB-AES-105 nommait
;   (EVP emprunte VAES512 zmm ; la notation gelée ymm 7911d03f… INTACTE, jamais retouchée).
; Domaine : couloir de performance (l'ère VAES512 — la cible NOUVELLE CIB-AES-512
;   ≤ 1,05 × EVP à contexte posé, pré-enregistrée au plan W29VAES512).
; Dépendances : aucune (le couloir est autonome — le référentiel est OpenSSL EVP au même
;   volume, le chemin zmm dispatché depuis OpenSSL 3.1, OPENSSL_ia32cap consigné).
;
; LA DETTE DE CÉRÉMONIE NOMMÉE À LA NAISSANCE : l'ère nouvelle n'est scellée que par la
; clé hors-ligne du développeur — le laboratoire ne signe JAMAIS (D87/D183). Le kit de
; remise préparé : la présente notation, son empreinte, la consigne de cérémonie (l'ère
; signée à la clé du maître au geste hors-ligne ; jusqu'alors la notation vit SUR COPIE
; LABORATOIRE, exécutable et éprouvée, jamais scellée).
;
; LES QUATRE ÉTAGES, tels qu'écrits :
;
; ---- ÉTAGE 0 · LE DISPATCH HISSÉ HORS BOUCLE ----------------------------------
;   cpuid vaes? vpclmulqdq? avx512f/dq? — UNE FOIS à l'entrée du couloir
;   absent → refus nommé SILICIUM-ABSENT (aucun repli silencieux, jamais un chemin non
;   mesuré — le même refus que couloir-vaes.asm, l'ère reconduite)
;
; ---- ÉTAGE 1 · CTR × VAES512 (QUATRE blocs par vAESENC) -------------------------
;   J0 = IV(96 bits) || 0x00000001 ; la ligne de départ : les compteurs [2 | 3 | 4 | 5]
;   aux QUATRE voies du zmm (le premier bloc de message = J1 = le compteur 2)
;   boucle (8 plis de 512 octets pour 4 Kio ; 8 frappes par pli, CHACUNE un zmm de
;   QUATRE blocs — 32 blocs par pli, 256 blocs au total) :
;     zmm_ligne = [ctr | ctr+1 | ctr+2 | ctr+3]    ; les QUATRE compteurs, une par voie
;     la CTL : [iv || ctr BE]                        ; la voie réordonnée (4..15 puis 3,2,1,0)
;     vpaddd zmm_ligne += 4 AU DWORD 0 DE CHAQUE VOIE SEULEMENT (l'IV aux dwords 1-3
;       intouchable — le masque QUATRE, l'incrément masqué : la faute nommée de la v2
;       ne se reproduit pas à l'ère nouvelle)
;     zmm_x = vpshufb(zmm_ligne, CTL)
;     vpxor  zmm_x, zmm_x, rk0                       ; l'éclaircissement (les QUATRE voies)
;     vaesenc zmm_x, zmm_x, rk1 … rk13                ; TREIZE tours (AES-256 : 14 tours)
;     vaesenclast zmm_x, zmm_x, rk14                 ; le dernier tour
;     vpxor  zmm_x, zmm_x, [clair+64k]               ; le masque ⊕ le clair (64 octets)
;     vmovdqu64 [chiffre+64k], zmm_x                 ; QUATRE blocs AES par passe
;   L'ILP : les chaînes DEUX À DEUX pipelinées (la leçon de couloir_sched.S — deux
;   frappes en vol, l'écart de dépendance couvert ; à l'ère 512 la même discipline)
;
; ---- ÉTAGE 2 · GHASH × VPCLMULQDQ, LE PLI DE 32 BLOCS --------------------------
;   H = E_K(0^128), réfléchi ; les puissances H¹..H³² précalculées (les produits, UNE
;   fois par clé — hors boucle)
;   par frappe (les QUATRE blocs du zmm) : le vb de la frappe = [H^{32-4p} | H^{31-4p} |
;     H^{30-4p} | H^{29-4p}] (une puissance par voie, la k-ième voie du pli)
;   la frontière réfléchie AU ZMM (QUATRE blocs par passe) : vpshufb la table en
;     REGISTRE (le contrôle seul peut être mémoire — la faute (5) de la vague 28 nommée)
;   NEUF produits par... NON — à l'ère 512 : les QUATRE voies par vpclmulqdq, le
;   KARATSUBA par voie (lo/hi/croisé — trois clmul par voie), les piles ZMM (le
;   franchissement de voie UNE fois par pli)
;   la réduction du pli : la pile pliée aux QUATRE voies + acc⊗H³² — UNE SEULE
;     réduction par pli (la réduction EXACTE du corps réfléchi — Gueron, la même)
;
; ---- ÉTAGE 3 · LA QUEUE (le bloc des longueurs + le tag) -------------------------
;   lb = [alen_bits BE || 4096×8 bits BE] ; acc = (acc ⊕ rev(lb)) × H
;   le tag = rev128(acc) ⊕ E_K(J0)         ; le dernier retournement AVANT l'usage
;
; ---- LES CONVENTIONS DE MESURE --------------------------------------------------
;   le volume 4 Kio, le cœur épinglé, n=20, EVP mesuré DANS CHAQUE PASSE (chaque
;   ratio publié porte les opérandes de SA PROPRE passe — l'erratum de l'Entrée 441)
;   la cible CIB-AES-512 ≤ 1,05 × EVP à contexte posé ; CIB-AES-105 DEMEURE MANQUÉE
;   et datée (jamais re-tirée — l'ère nouvelle OUvre la voie, l'ancienne garde son
;   verdict) ; l'écart notation-vs-C le RÉSULTAT DISTINCT pré-enregistré (la
;   référence datée : 1,07× au profit du C à ymm, W28VAES)
;   LA PORTE AVANT MESURE : parité 20/20 CAVP contre EVP octet pour octet (le clair
;   paddé, tag compris) pour CHAQUE pièce ; la variante mutée (rk13 ⊕ 0x5a) REFUSÉE
;   au premier vecteur ; le round-trip inter-implémentations VERT ; la convention
;   session recoupée ; le rejeu bit-identique.
;
; LE CAVEAT VM nommé (fréquence non goupillée — le même que W20PERF/W27VAES/W28VAES) ;
; le kit machine réelle goupillée : les sources, la notation, la porte, les commandes.
