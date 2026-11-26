# PLAN GELÉ — W28RLVR (l'entraînement sur juges de conformité, jamais sur similarité — coût/terrain)

> Vague 28, prompt 6 (dépôt du 26/11/2026). L'opération ajouter stagne à 5–7/18 (cible
> ≥ 15/18 à ≤ 3 000 tokens, SERVING-ABSENT consigné). La récompense est le verdict du juge,
> JAMAIS une similarité. Le juge d'expansion à empreinte sha256 INCHANGÉE (9fc325e2… —
> JUGE-MODIFIÉ est le refus). Aucun chiffre fabriqué ; le verdict manqué publié tel quel.

## Geste
1. LE PLAN D'ENTRAÎNEMENT PRÉ-ENREGISTRÉ (empreinte consignée avant tout run) : le modèle
   ouvert capable (la classe 7–14B coder, l'identifiant ET l'empreinte consignés au moment du
   choix — le geste compute appartient au développeur, la session d'entraînement vit hors
   bac), l'algorithme (DPO sur les 48 paires du corpus v2.1 PUIS RLVR sur l'environnement à
   récompense multi-niveaux typée), le budget compute, les critères d'arrêt ; LA CIBLE :
   ≥ 15/18 à ≤ 3 000 tokens sur les 18 tâches ajouter, le juge INCHANGÉ. La différenciation
   vs SuperCoder (RL orienté vitesse d'exécution) : la récompense fondée sur juges de
   conformité, pas sur le runtime.
2. LA DISCIPLINE DE L'ENVIRONNEMENT : l'entraînement sur le split TRAIN seul ; le held-out
   aux validateurs seuls, aucune notation dorée ; le canari de contamination vérifié à
   chaque évaluation ; DIX rebuilds bit-identiques de l'environnement avant tout run (la
   preuve vécue au bac, les empreintes consignées).
3. L'ÉVALUATION : l'échelle de capacité re-jouable (les rungs nomment la frontière, jamais
   une moyenne) ; la matrice checkpoint-kit-juges fail-closed ; chaque refus consigné par
   classe ; le verdict publié TEL QUEL, manqué inclus.
4. LA SONDE SERVING DEVENUE GATE DE SÉLECTION D'ENDPOINT : tout endpoint qui accepte
   response_format sans l'appliquer au décodage est REFUSÉ NOMMÉMENT (la sonde W27DECCO
   reconduite comme gate, l'identifiant de l'endpoint consigné) ; la campagne ne court JAMAIS
   sur un endpoint refusé. À défaut d'API conforme : le décodage contraint côté client sur
   modèle ouvert (le backend grammaire xgrammar/llguidance à brancher au moment du run —
   la commande consignée) et la sonde re-courue ; le verdict de conformité du serving
   consigné AVANT toute mesure de campagne.
5. LA CONSIGNATION : le registre CIBLES (CIB-ADD-STRUC demeure EN ATTENTE telle quelle
   tant que le gate refuse) et la table des ères mis à jour sans re-tirage ; la recomposition
   C25/C26 aux cinq pièces ; aucun artefact scellé touché.

## Critères d'acceptation
- Le plan d'entraînement gelé AVANT tout run (sha256 consignée, le commit d'abord) ; le
  juge recoupé à l'empreinte INCHANGÉE avant et après chaque évaluation.
- Les dix rebuilds bit-identiques vécus et consignés (les empreintes).
- Le gate vécu : la sonde re-courue, l'identifiant de l'endpoint consigné, le verdict
  SERVING-ABSENT (ou conforme) consigné avant toute mesure.
- Aucune cible re-tirée ; aucun chiffre fabriqué ; sceau-I 14/14 avant et après.
