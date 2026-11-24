# PAQUET DE RÉPLICATION — VAGUE 17 (paquet PUBLIC, expurgé)

> Atelier W17R4PER de la vague 17 (24/11/2026). Ce paquet ne contient **ni la couche I
> signée, ni la carte C, ni un secret, ni une donnée personnelle**. Il contient ce qui
> permet à un tiers de rejouer les VÉRIFICATIONS DE PROVENANCE et les CONTRÔLES de la
> porte R10 sur les pièces publiques du dépôt.

## 1. Ce qu'un tiers peut rejouer, et ce qu'il doit obtenir

| Commande | Attendu |
|---|---|
| `python3 scripts/vague17/provenance_tableaux.py --verifier` | `CONFORME — chaque ligne se recompose depuis sa source canonique` (10 lignes) |
| `python3 scripts/vague17/provenance_tableaux.py --controle-negatif` | `4/4 contrôles négatifs rendus` (valeur, ratio, compte, statut) |
| `python3 scripts/vague17/linter_v234.py --provenance` | `10/10 lignes VERTES` |
| `python3 scripts/vague17/linter_v234.py --provenance-negatif` | `contrôle négatif : 4/4` |
| `python3 scripts/vague17/linter_v234.py --controle-negatif` | `contrôle négatif : 2/2` (classes D81/D223) |
| `python3 atelier-w17-r10-confiance/controles_fail_closed.py` | `11/11 contrôles rendus` |
| `python3 v06/sceau_I.py verifier` | `14 arbres VERTS` |

Prérequis : Python 3, `cryptography` (porte R10). Aucun réseau n'est requis par les
contrôles ; `provenance_tableaux.py` lit uniquement des fichiers du dépôt.

## 2. Les sources canoniques du registre

Les nombres du dossier sont recomposés depuis : `atelier-ajouter-v{2,3,4,5}-*/resultats_v*.jsonl`,
`atelier-gabarits-o5apue194/resultats_gabarits.jsonl`, `depot-zenodo-corpus-v21/*.jsonl`
et `atelier-ghash-agrege-h1mz2sr8s/registres/ghash-agrege.json`. Chaque ligne du registre
`replication-v17/provenance-v17.json` porte le chemin et le sha256 de sa source ; une
source modifiée fait échouer le contrôle (classe EMPREINTE-SOURCE).

## 3. Ce qui est EXCLU de ce paquet, et pourquoi

- **La couche I signée et la carte C** : propriété intellectuelle (R1, D16) ; elles ne
  quittent pas le poste du développeur. Le paquet public ne cite que des empreintes.
- **Les secrets** (phrase de contrôle, parts du séquestre, jetons, clés privées) : jamais
  lus, jamais copiés (D105, D223). Le contrôle de provenance ne lit aucun `.keys/`.
- **Les données personnelles** : aucune n'entre dans le corpus ; le corpus v2.1 est
  publié sous son propre concept Zenodo avec sa DATASET-CARD.
- **Les rapports internes non expurgés** : le paquet cite les ateliers par leur nom ;
  les rapports verbatim restent au dépôt, sous la garde de l'auteur.

## 4. La procédure d'audit tiers (autorisée, pas seulement possible)

1. Cloner le dépôt public `https://github.com/alexisfrlopez-debug/triade` à la tête
   consignée par le rapport de release.
2. Exécuter les commandes du § 1 ; consigner les sorties **verbatim** (un écart se
   rapporte, il ne se corrige pas).
3. Recompter une mesure au hasard depuis sa source JSONL et comparer au registre ; toute
   divergence est un défaut de provenance à déclarer, avec la ligne et l'empreinte.
4. Vérifier que le sceau-I est à 14/14 avant et après les commandes (aucune pièce scellée
   n'est modifiée par les contrôles).
5. Publier le constat, favorable ou défavorable : la lecture défavorable est une pièce,
   pas un incident (règle du projet).

## 5. Limites nommées

- Le paquet ne prouve aucune **mesure matérielle** : le métal nu (≥ 2 machines), la
  sentinelle Windows et les runs Tamarin/ProVerif restent **EN ATTENTE**.
- `resultats_opt05.jsonl` porte des verdicts de round-trip en texte libre : le registre
  n'en extrait aucun compte sans un champ structuré — l'absence est NOMÉE, pas comblée.
- Les médianes de tokens sont celles de la **dernière tentative des tâches vertes** ; les
  tentatives refusées sont conservées dans les JSONL et ne sont pas exclues du dossier.
