# GUIDE DÉVELOPPEUR — le kit au banc du développeur (le miroir FR)
Le kit développeur est bâti PAR CONSTRUCTION depuis le dépôt (D130 :
git ls-files — jamais de maintenance manuelle). Le manifeste porte un
sha256 par fichier, le vecteur de versions lie kit / protocole /
carte / profil, et la porte de compatibilité REFUSE tout triplet
incompatible (fail-closed, refus nommé).

Ce que le kit porte (le M0-en-boîte) :
- la notation et le round-trip : la chaîne d'expansion v2 au pointeur
  seul et les validateurs v3 — les juges INTACTS, jamais affaiblis ;
- les fragments de carte et l'expandeur, avec ses quatre refus nommés
  du pointeur (nul, hors zone, la taille, l'alignement) ;
- le GÉNÉRATEUR d'oracle dérivé de la couche I (jamais un oracle
  pré-dérivé expédié — la dette kit nommée), les vecteurs FIPS/RFC,
  les routes d'indépendance ;
- les portes R1-R11 (voir REFERENCE) ;
- la cérémonie de genèse de clé air-gap et le sceau LOCAL — aucune
  ancre de confiance du projet n'est expédiée (ni la clé publique du
  projet, ni les signatures de référence ; l'adopteur court sa propre
  genèse) ;
- le gabarit de journal append-only (horodatage, phase, tâche,
  verdict, tokens natifs) ;
- le guide d'agent, la ladder d'eval, le gym, l'outil feedback,
  l'outil rapport, le pipeline de triage.

La méthode : geler le plan AVANT toute donnée (le sha256 consigné, le
commit d'abord) ; mesurer et publier les opérandes non arrondis ; un
échec mesuré est une pièce aussi précieuse qu'un vert — jamais un
verdict fabriqué ; le verbatim historique demeure octet pour octet,
les corrections vivent en erratum append-only ; l'ordre des tâches
n'est jamais re-tiré, les graines sont consignées.

La régénération : courir le générateur — l'archive est déterministe
(10 rebuilds bit-identiques, les timestamps normalisés, les entrées
triées). Le dépôt Zenodo du kit demeure le geste du développeur
(BSL 1.1 au grant D209) — jamais minté sans commande.
