# PLAN GELÉ — W27DECCO (campagne add à décodage contraint — coût tokens, le levier pré-enregistré)

> Évaluation du pack — prompt 4 de la vague 27 (26/11/2026). La cible CIB-ADD-STRUC
> (≥ 15/18 à ≤ 3 000 tokens) est PRÉ-ENREGISTRÉE et JAMAIS re-tirée. Aucun chiffre fabriqué.

## Geste
1. PRÉPARER LA CAMPAGNE D264 : le harnais complet —
   - schéma fermé {op, dst, src, offset}, 11 opcodes, additionalProperties:false, le schéma
     JSON consigné à empreinte sha256 ;
   - l'expandeur importé À EMPREINTE CONSIGNÉE (le juge intact — celui de la campagne
     TPL-ADD, jamais retouché pour plaire) ;
   - la boucle de réparation bornée à TROIS tours, réinjectant le refus EXACT du juge et le
     contre-exemple ;
   - la graine consignée ; n = 18 (les dix-huit tâches de la campagne, l'ordre jamais re-tiré) ;
   - les médianes calculées sur 18 ET sur les vertes seules ;
   - la re-tokenisation indépendante à écart ≤ 1 ;
   - l'agrégateur FAIL-CLOSED : un appel manquant refuse le verdict.
2. VÉRIFIER LE SERVING : dès qu'un serving à structured output (json_schema strict) est
   disponible, EXÉCUTER. Si le serving est absent : livrer le harnais PRÊT et le refus nommé
   SERVING-ABSENT — aucun chiffre fabriqué, la cible demeure EN ATTENTE telle quelle.

## Critères d'acceptation
- Fixtures : 18/18 vertes au harnais local (le juge rejoué sur les réponses connues).
- QUATRE refus nommés éprouvés (appel manquant → agrégateur refuse ; schéma violé → refus ;
  juge divergent → refus ; boucle au-delà de trois tours → refus).
- Rejeu bit-identique (la graine, l'ordre, les empreintes).
- Compteurs à écart zéro (re-tokenisation ± 1).
- Le verdict consigné TEL QUEL (tenu ou manqué) au registre CIBLES et au journal ; si le
  serving est absent : SERVING-ABSENT consigné, la ligne CIB-ADD-STRUC inchangée (EN ATTENTE).
