# PLAN GELÉ — W27RECON (réconciliation sémantique inter-pièces, priorité 1)

> Évaluation du pack — prompt 1 de la vague 27 (26/11/2026). Append-only ; aucune valeur
> mesurée modifiée ; aucun artefact scellé touché ; aucune cible re-tirée.

## Le constat à solder
Le statut de l'ancrage de transparence (D267) diverge ENTRE les cinq pièces : le Livre v1.15
(le paragraphe « L'ancrage de transparence, à son statut appliqué (D267, v1.15) » de la section
décisions) dit « la règle est adoptée et outillée, le déploiement n'est pas fait : aucun témoin
ancré n'existe à cette révision, et la porte de release le dit EN ATTENTE » — alors que la spec
§7.11, la présentation §4 et les preuves §5 portent le statut DÉRIVÉ DU JOURNAL : DÉPLOYÉ.
Le journal append-only (atelier-w20-ancrage-journal.jsonl) détient des entrées vérifiées pour
v0.27.0 → v0.31.0 (TSA freetsa.org, RFC 3161, jetons recoupés à chaque porte V6). La divergence
est démontrable : le pack revendique la fermeture des contradictions de statut inter-pièces
(D274, C20) et en contient une sur la pièce que C20 ne couvrait pas (le Livre).

## Geste
1. DÉRIVER LE STATUT UNIQUE du journal append-only (scripts/vague24/statut_ancrage.py,
   strict=False à la génération) : DÉPLOYÉ — entrée vérifiée recouvrant les pièces de
   l'édition courante.
2. RÉGÉNÉRER LA PIÈCE DIVERGENTE À LA SOURCE : scripts/livre_v18/sec-5.tex → livre_v19 (v1.16)
   par patcher ancré ; le paragraphe D267 réécrit au statut dérivé (la règle adoptée à la
   vague 20, LE DÉPLOIEMENT APPLIQUÉ depuis — le témoin d'époque RFC 3161 vérifié, le journal
   append-only des ancrages, les refus nommés intacts) ; la table 13 (chronologie) réordonnée
   au geste de W27RESID.
3. CLASSE C26 STATUS-INTERPIECES dans le linter : recompose TOUT statut sémantique partagé —
   ancrage (journal append-only), compteur NV (PREUVES-STATUTS.json), Tamarin/ProVerif
   (PREUVES-STATUTS.json), sentinelle Windows (registre étendu), fence.i (registre étendu) —
   et REFUSE toute pièce divergente, dans les deux sens, sur les CINQ pièces (le Livre et le
   manuscrit inclus, le trou de C20 nommé).
4. AU MOINS DEUX CONTRÔLES NÉGATIFS : (i) statut muté dans une pièce — le Livre retrouve
   « le déploiement n'est pas fait » → refus C26 nommé ; (ii) registre muté — le journal
   d'ancrage amputé de l'édition courante → le statut dérivé passe EN ATTENTE → les pièces
   disant DÉPLOYÉ refusées nommément.

## Critères d'acceptation
- Les cinq pièces régénérées (édition v0.32.0) ; porte complète V1..V7 + L1..L26 zéro rouge.
- Chaque mutation rejouée : refus nommé C26.
- Empreintes du pack recoupées (manifeste régénéré) ; sceau-I 14/14 avant/après.
- Décision consignée append-only (DECISIONS.md D277+) ; aucune valeur mesurée modifiée.
