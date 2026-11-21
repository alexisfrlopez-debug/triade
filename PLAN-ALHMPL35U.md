# PLAN GELÉ — ALHMPL35U (la vague 12)
> La machinery de conformité générative branchée sur la machine z3 de la sentinelle durcie, et la grille de réception des témoins signés.
> Gelé AVANT toute exécution. Aucun résultat produit ; sur copies de laboratoire UNIQUEMENT (phrase publique D105, aucun coffre réel, aucune phrase réelle — règle absolue).

## Le mandat (deux chantiers)
1. **Brancher la machinery de conformité générative** (30 000 traces, trois graines, ddmin,
   replay bit-identique) sur la machine z3 de la sentinelle durcie (a)–(g) : chaque règle
   abstraite confrontée à l'implémentation Python durcie, chemins d'échec inclus (corruption
   sans destruction, falsification à empreinte naïve valide → destruction+PV, nonce altéré
   après empreinte verte, piège périmé/périmé d'époque, retour en arrière, phrase faible au
   plancher). Toute divergence est réduite, nommée, et le modèle ou l'implémentation corrigé
   PAR ÉCRIT avec empreinte reconsignée — jamais en silence. Les quatre invariants z3
   re-déchargés sur le modèle étendu, contrôles négatifs compris (la machine nue doit
   redevenir SAT).
2. **Préparer l'exécution des kits au geste du développeur sans produire de résultat** :
   la grille de réception des témoins signés (dudect n≥10 × N{60,200,400} × ≥2 machines
   avec empreinte CPU et fréquence, fence.i RV64 avec chaîne exacte consignée, 3e machine
   Loupe T0→T7+S0, tirage H7 stratifié signé à l'ouverture, double annotation κ≥0,61 sur
   n≥50, Tamarin au poste réel avec bornes nommées). L'agrégateur fail-closed refuse tout
   manque (exit 2, liste). AUCUN chiffre fabriqué, la table des statuts ne bouge QUE sur
   pièces recoupées.

## Les gestes
1. Ce plan gelé AVANT toute exécution.
2. Atelier atelier-conformite-alhmpl35u/ : le générateur génératif (30 000 traces, graines
   20261121a/b/c consignées), la réduction ddmin sur toute divergence, le replay
   bit-identique deux fois.
3. La machine z3 étendue depuis atelier-coffre-vr9n3s3l7/ (les quatre invariants + les
   chemins d'échec nommés), contrôles négatifs (axiomes retirés → SAT nommé).
4. La grille de réception : agrégateur fail-closed (exit 2 + liste des manques), les
   empreintes des kits pré-enregistrés d'EMPREINTES-KITS.txt (l4nnwqlld) référencées —
   aucun statut bougé, aucun chiffre fabriqué.

## La vérification après modifications
- campagne générative re-jouée → zéro divergence aux trois graines, replay bit-identique
  deux fois, chaque chemin d'échec couvert (comptes acceptés/refusés par règle lus des logs) ;
- les 5/5 vecteurs labo (a)-(g) re-verts ;
- contrôle négatif z3 (axiomes retirés) → SAT nommé ;
- autotests des kits 57/57 re-verts ;
- git diff VIDE hors atelier, aucun commit des données avant le plan ;
- sceau 14/14 avant/après, empreintes identiques ;
- les gaps restants (token FIDO2 physique, ancrage réseau, miroirs Windows, Tamarin au
  poste réel) nommés au rapport avec leur geste attendu.

## Les refus
Aucun coffre réel ; aucune phrase réelle ; aucun résultat produit au chantier 2 ; aucun
chiffre fabriqué ; tout écart nommé, jamais corrigé en silence.
