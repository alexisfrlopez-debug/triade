# PLAN GELÉ — W28VAES (couloir VAES : domaine réfléchi, amortissement, schedule de notation — performance)

> Vague 28, prompt 1 (dépôt du 26/11/2026). R4 (contrat stable), R7 (aucune adresse scellée
> déplacée), R11 (avant/après au journal OPT). CIB-AES-105 (≤ 1,05 × OpenSSL EVP au même
> volume) est pré-enregistrée D273, JAMAIS re-tirée. L'écart notation-vs-C est un RÉSULTAT
> DISTINCT pré-enregistré au présent plan. Aucun gain revendiqué sans run recoupé.

## Geste
1. PRÉ-ENREGISTRER la mesure : mêmes 20 vecteurs NIST CAVP 14.0 (les vecteurs dorés de
   W27VAES, INTACTS), même volume 4 Kio, n=20, cœur épinglé 0, contre OpenSSL EVP 3.5.7 au
   même volume ; le chemin EVP réel consigné (OPENSSL_ia32cap, le drapeau VAES512 de la 3.1+) ;
   l'état de fréquence consigné (VM non goupillée = caveat nommé ; machine réelle goupillée =
   kit livré). LES TROIS PIÈCES MESURÉES : (i) le portage C AMÉLIORÉ — GHASH en domaine
   réfléchi de bout en bout (la conversion UNE FOIS aux frontières, H et ses puissances
   pré-calculées en bitref8), l'expansion de clé + les puissances H amorties par contexte de
   session (comme EVP), la frontière d'appel supprimée (le couloir inliné au point de mesure) ;
   (ii) LE SCHEDULE DE NOTATION — le couloir écrit en ASSEMBLAGE SUR le calendrier de la
   notation gelée couloir-vaes.asm (7911d03f… INTACTE : le dispatch hissé hors boucle, CTR
   deux blocs par vAESENC, GHASH Karatsuba huit blocs par pli, l'entrelacement CTR(g+1) avant
   GHASH(g)), assemblé et exécuté COMME BINAIRE ; (iii) EVP au même volume. L'ÉCART
   notation-vs-C = (ii) contre (i) à algorithme égal, publié comme RÉSULTAT DISTINCT.
2. LA PORTE AVANT TOUTE MESURE (dans l'ordre) : parité 20/20 CAVP contre EVP octet pour octet
   (4 Kio paddés, tags compris) pour CHACUNE des deux pièces mesurées ; la variante mutée
   (rk13 ⊕ 0x5a) refusée au premier vecteur ; round-trip inter-implémentations vert ; rejeu
   bit-identique.
3. LA MESURE : n=20 par pièce, quatre passes, médianes, IQR consigné ; le ratio contre EVP ;
   la décomposition du coût mise à jour par classe (les quatre causes de W27VAES : expansion
   hors boucle, conversion par bloc, schedule C, frontière d'appel — lesquelles soldées,
   lesquelles demeurent) ; le plafond ISA ~0,1–0,3 c/B nommé au rapport.
4. LE VERDICT : CIB-AES-105 tenue ou manquée, publié TEL QUEL (jamais re-tirée) ; l'écart
   notation-vs-C publié tel quel — si la notation schedulée bat le portage C à algorithme
   égal, c'est le résultat systèmes consigné : l'érosion de schedule compilateur sur
   co-planification SIMD, mesurée et contrôlée.

## Critères d'acceptation
- La notation gelée couloir-vaes.asm INTACTE (sha256 recoupé avant/après — l'empreinte
  consignée AVANT l'implémentation, la règle reconduite).
- Parité CAVP 20/20 pour chaque pièce mesurée AVANT toute mesure ; mutant refusé au premier
  vecteur ; round-trip vert ; rejeu bit-identique.
- Aucun artefact scellé touché ; sceau-I 14/14 avant et après ; le couloir demeure une pièce
  de laboratoire autonome.
- Les cibles et statuts recomposés aux registres (CIBLES.md, JOURNAL_OPTIMISATION.md OPT-19,
  STATUTS-EN-ATTENTE.md) ; le linter numérique recompose chaque ratio publié de ses opérandes
  non arrondis ; aucun chiffre fabriqué.
