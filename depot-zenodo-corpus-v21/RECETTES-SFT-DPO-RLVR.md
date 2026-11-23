# LES RECETTES SFT / DPO / RLVR — le corpus TRIADE-CORPUS v2.1
> Agnostiques en famille de modèle : aucune recette n'exige un fournisseur, un
> API ni un format propriétaire. Le compute est CONSIGNÉ, jamais supposé.

## LA MATIÈRE
- **TRIPLES** (train.jsonl) : 127 lignes au TRAIN (126 triples + le canari), le
  prompt = le contrat de couche I (le squelette, le dictionnaire, la grammaire),
  la cible = la notation émise, le verdict du juge (VERT / REFUS + classe).
- **PAIRES DPO** (dpo-paires.jsonl) : 48 paires, CHOSEN = une complétion VERTE
  du juge, REJECTED = une complétion REFUS **au même contrat** — la récompense
  est LE VERDICT DU JUGE, jamais une similarité. La porte P2 refuse toute
  notation mutée (sha256 par membre, vérifiée byte-byte contre le corpus).
- **LE TEST** (test.jsonl) : NU — ni cible ni verdict : les validateurs seuls
  décident. Aucune dorée ne fuit.

## RECETTE SFT (le socle)
1. Filtrer les triples au verdict VERT du split TRAIN uniquement (le REFUS
   n'enseigne pas la notation, il enseigne l'échec).
2. LoRA ou plein réglage — la recette est la même : prompt = contrat,
   complétion supervisée = la notation VERTE.
3. **JAMAIS** le canari en cible (il vit au TRAIN comme sonde, pas comme
   enseignement : il n'est pas une notation).
4. Budget indicatif : ~120 exemples × ~3 000 tokens ≈ 0,4 M tokens par époque ;
   3 époques suffisent au registre observé (le corpus est PETIT — c'est un
   corpus de preuve, pas de bruit).

## RECETTE DPO (le raffinage)
1. Les paires sont PRÊTES (dpo-paires.jsonl) : prompt / chosen / rejected.
2. β (le cap de la dérive) : 0,1 par défaut ; monter au-dessus de 0,3 risque
   d'éroder la fidélité au squelette (le prompt porte le cadre ABI).
3. **LA RÈGLE D'ÉTANCHÉITÉ** : les paires naissent du TRAIN seul — les splits
   étant PAR GROUPE-DE-CONTRAT, aucun contrat du TEST ne peut fuiter dans
   l'entraînement PAR CONSTRUCTION. Ne re-tirez jamais les splits.
4. Budget indicatif : 48 paires × 2 membres ≈ 0,5 M tokens par époque ; la
   diversité vient des contrats (4 porteurs), pas du volume.

## RECETTE RLVR (la boucle à verdict)
1. Le juge = la chaîne v2 + les validateurs v3 (INTACTS — jamais affaiblis).
2. La récompense = LE VERDICT (VERT = 1, REFUS = 0), **jamais** une similarité
   au corpus (la similarité récompense le par-heart : l'anti-apprentissage).
3. Le prompt au contrat du TRAIN ; le rejet nommé (la classe de refus) alimente
   le diagnostic, pas la récompense.
4. **LE GARDIEN ANTI-HACKING (P2)** : à chaque pas, la notation récompensée
   doit être byte-identique à une notation admise par le juge — une notation
   mutée (un octet) est REFUSÉE (la porte le prouve à l'autotest).

## LE BUDGET COMPUTE CONSIGNÉ (l'honnêteté, pas la promesse)
- SFT : 0,4 M tokens/époque × 3 époques ≈ **1,2 M tokens**.
- DPO : 0,5 M tokens/époque × 2 époques ≈ **1,0 M tokens**.
- RLVR : la boucle au juge — le coût DOMINE au juge (CPU), pas au GPU ;
  compter ~k complétions par contrat × 14 contrats.
- Le corpus est un instrument de PREUVE (l'étanchéité, la porte, le canari) ;
  le gain mesuré sur 18 tâches régénérées à graines consignées, jamais ajusté.

## LES INTERDITS (les mêmes que le protocole)
Jamais la similarité comme récompense ; jamais une paire à cheval sur deux
contrats ; jamais une dorée au TEST ; jamais le canari en cible ; jamais un
juge affaibli pour faire monter le score ; jamais une cible re-tirée.
