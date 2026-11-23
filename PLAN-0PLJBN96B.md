# PLAN GELÉ — 0PLJBN96B (le kit de clôture idempotent : Tamarin 1.12.0 / Maude 3.4 / ProVerif)

> Le mandat : préparer le kit de clôture idempotent pour mener `CF3-v3b.spthy`
> à verdict complet sous Tamarin 1.12.0 / Maude 3.4 et ProVerif **au poste
> réel** (RAM ≥ 16 Go). Chaque lemme livre la commande exacte, l'évaluation
> partielle (`--partial-evaluation=SUMMARY`) et un budget mémoire borné. Le
> NÉGATIF D'ABORD. Aucune pièce scellée touchée ; le sceau-I 14/14 avant et
> après. Gelé AVANT tout run ; l'empreinte précède la première donnée.

## Le mandat

(1) **LE KIT, PAS LE RUN** : le laboratoire prépare et vérifie — le geste du
run appartient au poste réel (Tamarin 1.12.0 + Maude 3.4, RAM ≥ 16 Go, le
Linux du bac). Le kit est IDEMPOTENT : re-jouable sans effet de bord, chaque
lemme isolé, chaque budget nommé.

(2) **L'ORDRE OBLIGÉ** : le négatif D'ABORD (`CF3-v3-negatif.spthy`,
`--stop-on-trace=DFS --bound=8`) qui DOIT être falsifié — le défaut v2 public
attrapé est la preuve que l'instrument voit ; PUIS les positifs (L1
implication_secret, L2, T1–T3) ; PUIS le port ProVerif `CF3-v3.pv` (six
requêtes actives, événements miroir, l'oracle du seuil) avec les six écarts de
sémantique NOMMÉS.

(3) **LA TABLE DES STATUTS** : prouvé symbolique indépendant / borné / en
attente — mise à jour DEPUIS LES PIÈCES, jamais depuis l'intention.

## Les gestes

1. Le plan gelé ; l'empreinte consignée ; LE COMMIT D'ABORD.
2. **LE RUNNER** : `scripts/vague16/tamarin_cloture.py` — un lemme par
   invocation, la commande exacte rendue en clair (copiable telle quelle au
   poste réel), `--partial-evaluation=SUMMARY`, le budget mémoire borné, le
   code de sortie nommé, la sortie capturée verbatim dans le registre.
3. **LE NÉGATIF D'ABORD** : la commande du négatif, l'attente FALSIFIÉ nommée,
   la lecture `stop-on-trace=DFS --bound=8`.
4. **LES POSITIFS ET LE PORT** : les cinq commandes des lemmes, la commande
   ProVerif, les six écarts de sémantique énoncés (pas devinés).
5. **LE RAPPORT VERBATIM APPEND-ONLY** et la table des statuts.

## La vérification après modifications

Les verdicts Tamarin/ProVerif confrontés aux quatre propriétés P1–P4 de
l'invariant inductif (aucune contradiction attendue) ; le négatif bien
FALSIFIÉ (le défaut v2 public attrapé) ; les empreintes des modèles recoupées
au registre consigné ; la table des statuts de preuve mise à jour depuis les
pièces ; le rapport verbatim append-only ; le sceau-I 14/14 avant et après.

## Les refus

Jamais une pièce scellée touchée ; jamais un verdict inventé ; jamais un lemme
rapporté PROUVÉ quand il est INCOMPLETE (la cause nommée : la décomposition du
but K(p) contre la profondeur — et la voie, pas un camouflage) ; jamais le
négatif « vérifié » (il doit être falsifié) ; jamais un run du poste réel
simulé au laboratoire.
