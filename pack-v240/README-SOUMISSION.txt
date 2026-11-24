TRIADE — la soumission de l'édition v0.24.0 (la vague 17, 24 novembre 2026)
==========================================================================

Le manuscrit académique v0.24.0 porte les trois consolidations de la dix-septième
vague, sans aucune valeur mesurée modifiée :

(1) LA PUBLICATION D'UNE BASCULE EST BORNÉE À CE QUE L'ARCHITECTURE GARANTIT (D253) :
un magasin naturel est atomique jusqu'à huit octets, pas au-delà ; la forme absolue de
douze octets n'est publiée que par un LOCK CMPXCHG16B sous CPUID ; un thread dont RIP
tombe dans la plage remplacée n'est protégé par aucune atomicité de magasin, d'où la
quiescence obligatoire.

(2) LA GARANTIE DE R10 EST BORNÉE À SON ANCRE (D254) : intégrité, authenticité et
fraîcheur sont trois propriétés distinctes ; l'ancre réelle diffère par profil
(Authenticode, IMA ou signature de paquet, chaîne de boot signée) et, si elle est
modifiable avec l'artefact, R10 ne détecte plus l'administrateur local ; la
restauration cohérente d'un couple binaire + état échappe à toute ancre locale.

(3) LA PROVENANCE EST UN CONTRÔLE (D255) : onze lignes recomposées depuis leurs
sources canoniques committées, quatre refus mutants vivants ; le test du lecteur a
trouvé un ratio qui ne se recomposait pas (63,39/19,66 = 3,2243, imprimé 3,23) —
corrigé à 3,22 dans la source de cette édition, le PDF v0.23.3 scellé demeurant.

Le manuscrit est accompagné de : ses tableaux générés (tables_generees.txt), la table
des empreintes des cinq pièces (empreintes_livrables_v0.24.0.txt) et le rapport de
vérification (rapport_verification_v0.24.0.txt — porte 5/5, contrôles négatifs 5/5,
provenance 11/11, sceau-I 14/14). Aucune mesure au métal nu n'est revendiquée.
