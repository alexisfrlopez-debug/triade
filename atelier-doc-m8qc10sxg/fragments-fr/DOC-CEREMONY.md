# DOC-CEREMONY — les cérémonies (le miroir FR, compact)
Les cérémonies lient l'artefact, jamais la prose :
1. Le plan est gelé AVANT toute donnée — le sha256 consigné, le
   commit d'abord.
2. La genèse de clé est AIR-GAP : ta propre clé, sur ta propre
   machine — aucune ancre de confiance du projet n'est expédiée avec
   le kit (ni la clé publique du projet, ni les signatures de
   référence).
3. Le sceau est LOCAL : les quatorze arbres scellés vérifiés verts
   avant et après chaque geste (v06/sceau_I.py verifier).
4. Le journal est APPEND-ONLY : aucune réécriture, jamais — une
   correction est un erratum appendu à côté du verbatim historique,
   octet pour octet.
5. Le commit passe la garde de secrets (les empreintes, l'entropie,
   les motifs de classe) — un secret détecté refuse le commit au nom.
6. Le dépôt de release (l'archive, le DOI) est une COMMANDE HUMAINE —
   jamais minté automatiquement, jamais sans la parole du
   développeur.
7. L'ordre des tâches n'est jamais re-tiré ; les graines sont
   consignées ; les opérandes mesurées sont publiées non arrondies.
