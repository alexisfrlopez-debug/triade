# PLAN GELÉ — W29VAES512 (l'ère VAES512 zmm, les deux bras schedule-gap)

> Vague 29, prompt 3 (dépôt du 27/11/2026, instructions.txt §10 Prompt 3 — suggestion
> B6 de l'évaluation). Ouvrir une ÈRE NOUVELLE : la voie 512-bit. La cible CIB-AES-105
> (≤ 1,05 × EVP) demeure MANQUÉE et datée — JAMAIS re-tirée ; le résidu structurel est
> nommé (EVP = VAES512 zmm, la notation gelée = ymm, l'empreinte 7911d03f… INTACTE).
> Le présent plan gèle l'atelier AVANT toute mesure.

## Geste
1. LA NOTATION NOUVELLE : un fichier DISTINCT couloir-vaes512.asm — le couloir
   AES-256-GCM en VAES512/VPCLMULQDQ zmm (QUATRE blocs AES par vAESENC, le calendrier
   de couloir-vaes.asm adapté à la voie 512 : les étages 0–3 reconduits — dispatch
   hors boucle, CTR×VAES, GHASH×VPCLMULQDQ, la réduction). La notation écrite SUR
   COPIE LABORATOIRE avant toute mesure (R5), l'empreinte sha256 consignée AVANT
   l'implémentation exécutable. LA DETTE DE CÉRÉMONIE NOMMÉE À LA NAISSANCE : l'ère
   n'est scellée que par la clé hors-ligne du développeur — le laboratoire ne signe
   jamais (le kit de remise préparé : la notation, l'empreinte, la consigne de
   cérémonie).
2. LA CIBLE NOUVELLE — CIB-AES-512 (pré-enregistrée AU PRÉSENT PLAN, jamais un
   re-tirage) : ≤ 1,05 × EVP à contexte posé au même volume (4 Kio, cœur épinglé,
   n=20, la convention « comme EVP » de W28VAES). LA MÉTHODE À L'IDENTIQUE : EVP
   mesuré dans CHAQUE passe (chaque ratio porte les opérandes de SA PROPRE passe —
   l'erratum de la 441 reconduit).
3. LES DEUX BRAS : (a) la notation-zmm écrite en forme ILP-friendly (les leçons de
   w28vaes : locals/restrict, le domaine réfléchi, la frontière d'appel supprimée —
   le schedule assemblé via gcc -O2 des sources .S au calendrier de la notation) ;
   (b) le portage C-zmm compilé gcc -O3 (le même algorithme à l'identique — SEUL LE
   CALENDRIER DIFFÈRE). L'ÉCART NOTATION-VS-C publié comme RÉSULTAT DISTINCT (la
   référence datée : 1,07× au profit du C à ymm, W28VAES).
4. LA PORTE AVANT MESURE : la parité 20/20 vecteurs NIST CAVP 14.0 contre EVP octet
   pour octet (4 Kio paddés, tag compris) pour CHAQUE pièce ; la variante mutée
   (rk13 ⊕ 0x5a) REFUSÉE au premier vecteur ; le round-trip inter-implémentations
   VERT ; la convention session recoupée octet pour octet ; le rejeu bit-identique
   (deux passes).
5. LE CAVEAT VM nommé (fréquence non goupillée — le même que W20PERF/W27VAES/W28VAES) ;
   le kit machine réelle goupillée livré à empreintes consignées (les sources, la
   notation, la porte, les commandes).
6. LA GRAINE : les 20 vecteurs CAVP reconduits intacts (vecteurs-dores-nist.json —
   AUCUN nouveau tirage) ; n=20 passes par pièce.

## Critères d'acceptation
- La notation ymm gelée couloir-vaes.asm 7911d03f… INTACTE (aucun octet changé) ; le
  sceau-I 14/14 avant et après (la nouvelle ère signée par le développeur hors ligne,
  jamais par le laboratoire — la dette nommée).
- La porte complète verte avant la mesure (20/20 CAVP, le mutant refusé, le round-trip,
  le rejeu) ; la mesure n=20 publiée TELLE QUELLE avec les opérandes de chaque passe.
- CIBLES.md : la ligne CIB-AES-512 nouvelle (tenue/manquée, telle quelle) ; la ligne
  CIB-AES-105 DEMEURE MANQUÉE et datée (aucun re-tirage) ; le linter C32 recompose
  chaque ratio publié.
- Aucun chiffre fabriqué.
