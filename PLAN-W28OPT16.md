# PLAN GELÉ — W28OPT16 (éditer par diff structuré au plancher token — coût, OPT-16)

> Vague 28, prompt 2 (dépôt du 26/11/2026). Le plus grand levier token restant. La cible
> pré-enregistrée : MÉDIANE ≤ 150 TOKENS NATIFS sur les 18 tâches d'édition (ratio plancher
> ~5,5× contre le diff réel 27,5 tokens, au lieu de 24,5×). La graine 20261117 reconduite,
> l'ordre des 18 tâches JAMAIS re-tiré. Le budget `usage` natif lu à chaque appel, le cl100k
> compté en parallèle (un compte distinct, jamais le juge). Aucune cible re-tirée.

## Geste
1. PRÉ-ENREGISTRER OPT-16 (empreinte du présent plan consignée avant toute mesure) : les 18
   tâches d'édition de taches-edition.json (les mêmes blocs loupe-*, la même graine, le même
   ordre — le matériau de la vague 10/OPT-05 reconduit, AUCUN nouveau tirage).
2. ÉTENDRE LE SCHÉMA FERMÉ à l'édition : la réponse de l'agent est UNIQUEMENT l'objet JSON
   {"op": "substituer", "dst": "<id du bloc>", "offset": <index de ligne dans la plage du
   bloc>, "src": "<la ligne nouvelle, littérale>"} — additionalProperties false, l'enum des
   op fermée (substituer), l'offset contraint à la plage de lignes du bloc, la ligne src du
   domaine de notation. L'agent ne rend QUE le diff structuré (~30–80 tokens attendus) ; LE
   CLIENT expande (applique la substitution à l'offset), assemble, round-trip, et confronte
   au bloc attendu (le diff exact : ligne unique révisée, AUCUNE autre ligne changée).
3. LES QUATRE REFUS NOMMÉS fail-closed : POINTEUR-INCONNU (dst inconnu), EMPREINTE-DIVERGENTE
   (la notation du bloc a divergé de son empreinte consignée), SCHÉMA-VIOLÉ (l'objet viole le
   schéma fermé), HORS-FORMAT (la réponse n'est pas l'objet JSON). L'AGRÉGATEUR fail-closed :
   un appel manquant refuse le verdict (APPEL-MANQUANT). LA BOUCLE DE RÉPARATION bornée à
   TROIS tours, réinjectant le refus exact et le contre-exemple.
4. LA MESURE : les 18 tâches dans l'ordre de la graine, chaque tâche UNE fois (les tours de
   réparation journalisés à part, jamais recomptés comme tâches) ; médianes publiées SUR 18
   ET sur les vertes (les deux conventions nommées) ; la re-tokenisation indépendante à
   écart ≤ 1 ; chaque conversion consignée par classe de refus ; la cible tenue ou manquée,
   publiée TELLE QUELLE.
5. LE PLANCHER RAPPELÉ : le diff réel des 18 tâches (une ligne substituée) ≈ 27,5 tokens —
   le ratio plancher publié à côté de la médiane.

## Critères d'acceptation
- Rejeu bit-identique à graine consignée (deux passes) ; fixtures 18/18 vertes au chemin
  vert (le client gabarits reconduit).
- Les quatre refus ÉPROUVÉS sur copies (une mutation par refus, chacun refusé nommément) ;
  l'expandeur importé à empreinte sha256 recoupée (JUGE-MODIFIÉ refusé).
- Le registre CIBLES (la ligne OPT-16 au budget publié) et la table des ères mis à jour sans
  re-tirage ; recomposition C25/C26 aux cinq pièces ; aucun artefact scellé touché.
- Aucune valeur mesurée modifiée ; sceau-I 14/14 avant et après.
