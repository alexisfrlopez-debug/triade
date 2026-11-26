# PLAN GELÉ — W27VAES (couloir VAES + moteur oracle natif — performance/optimisation)

> Évaluation du pack — prompt 6 de la vague 27 (26/11/2026). R4 (contrat stable), R7 (aucune
> adresse scellée déplacée), R11 (avant/après consigné au journal OPT). La cible CIB-AES-105
> (≤ 1,05 × OpenSSL EVP au même volume) est pré-enregistrée, JAMAIS re-tirée. Aucun gain
> revendiqué sans run recoupé.

## Geste
1. ÉCRIRE LE COULOIR VAES/VPCLMULQDQ en notation sur copies laboratoire D'ABORD (la notation
   du projet, loupe/ + I/) : CPUID hissé hors boucle, GHASH Karatsuba 8 blocs, entrelacement
   CTR×GHASH — AES-256-GCM, 4 Kio, le contrat du couloir entrelacé (W20PERF) inchangé.
2. MESURER sur machine épinglée n ≥ 20 contre OpenSSL EVP au même volume — le bac porte le
   silicium VAES (Xeon, drapeaux vaes/vpclmulqdq/avx512f constatés, mmap_min_addr 4 096) :
   la mesure y est conduite AU MÊME TITRE que le couloir entrelacé de la vague 20
   (environnement consigné : machine virtuelle, cœur épinglé, fréquence non goupillée — le
   caveat nommé, jamais maquillé) ; le kit machine réelle goupillée livré pareil.
3. ÉTENDRE LE MOTEUR D'ORACLE NATIF au-delà du memo hit : le refus mmap 0xC000
   (vm.mmap_min_addr) du bac d'alors est RE-ÉPROUVÉ ici (mmap_min_addr = 4 096 : l'adresse
   0xC000 est au-dessus du plancher) ; si la cartographie vit, le moteur est mesuré à la cible
   T < 10 s (CIB-ORACLE-T) ; sinon le kit machine réelle, le refus nommé.

## Critères d'acceptation
- PARITÉ AUX VECTEURS DORÉS FIPS octet pour octet AVANT toute mesure (NIST CAVP AES-256-GCM).
- CONTRÔLE NÉGATIF : variante mutée refusée au premier vecteur.
- Round-trip vert ; garde 14/14 ; rejeu bit-identique.
- Verdict consigné au registre CIBLES (CIB-AES-105, CIB-ORACLE-T) tel que mesuré, environnement
  nommé ; avant/après au journal OPT ; aucune adresse scellée déplacée (sceau-I 14/14).
