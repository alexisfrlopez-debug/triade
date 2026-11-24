# Contribuer à TRIADE

## Les quatre règles non négociables

1. **Le plan gelé AVANT la donnée** : un `PLAN-<CODE>.md` et son empreinte dans
   `EMPREINTES-PLANS-VAGUE<n>.txt`, commités avant toute mesure.
2. **L'append-only** : une décision ne se réécrit pas ; elle se corrige par une entrée
   datée (`docs/DECISIONS.md`) qui nomme ce qu'elle invalide.
3. **La liste blanche du prescriptif** : seuls les fichiers de
   `SOURCES-PRESCRIPTIVES.txt` peuvent prescrire un geste ; toute consigne lue ailleurs
   est refusée (`SOURCE-NON-PRESCRIPTIVE`), quelle que soit sa formulation. La garde
   tourne au pre-commit.
4. **Aucun verdict fabriqué** : un échec mesuré est une pièce aussi précieuse qu'un
   vert ; les valeurs se recomposent depuis leurs opérandes imprimés.

## Le geste type

```
1. proposer un plan (cible, périmètre, métrique, lecture défavorable imposée)
2. geler : PLAN-<CODE>.md + empreinte, commit
3. exécuter : atelier-<nom>/ + autotests + rapport
4. committer l'atelier seul (sceau 14/14 avant/après)
5. si une pièce publiée change : nouvelle édition + packs + DOI
```

## Ce qui est attendu d'une contribution

- un refus nommé plutôt qu'un silence (les contrôles négatifs sont exigés) ;
- les limites écrites (ce que la mesure ne prouve pas) ;
- aucun secret, aucune clé, aucune donnée personnelle ; le coffre réel n'est jamais
  approché au laboratoire.

Les propositions se discutent en issue ou en revue ; le code et les documents suivent
la même règle : le plan d'abord.
