# PLAN GELÉ — GZXVZE3PY (la vague 15)
> L'atelier matériel : exécuter les protocoles matériels pré-enregistrés sans
> fabriquer aucun chiffre — le laboratoire PRÉPARE ET VÉRIFIE, ne simule jamais.
> Gelé AVANT toute préparation.

## Le mandat
(1) **DUEDECT** : n≥10 exécutions indépendantes par N∈{60,200,400}, ≥2 machines
(empreinte CPU + état de fréquence consignés), affinité de cœur fixe ;
l'investigation des pics tls13-02/tls13-13 à N=200 pré-enregistrée (bruit
d'horloge / interruption cœur partagé / gap réel — LE CRITÈRE DE MÉDIANE
TRANCHE, aucune cause élue d'avance).
(2) **FENCE.I** : le scénario M7 retargeté sur carte RV64 physique (C1–C5 : la
bascule vue par le cœur, l'invalidation prouvée au témoin, la cohérence du
plan, le scellé au silicium, zéro régression).
(3) **LA LOUPE TIERS** : T0→T7+S0 intégral + la vitrine [4/4] deux codes 0, les
empreintes avant/après inchangées.
Les runs appartiennent au DÉVELOPPEUR : la machine unique du bac ne peut ni les
n≥10 sur ≥2 machines, ni la carte RV64 — les kits sont préparés, l'agrégateur
fail-closed livré (run manquant = refus exit 2, JAMAIS un verdict partiel), les
témoins signés recoupés avant tout mouvement de la table des statuts.

## Les gestes
1. Le plan gelé ; les trois kits préparés (dudect, fence.i RV64, Loupe tiers) —
   chacun pré-enregistré avec sa graine, sa consigne de machine et son agrégateur.
2. L'agrégateur fail-closed + les autotests 57/57 re-verts.
3. Le protocole d'investigation des pics N=200 pré-enregistré (les trois causes
   candidates nommées, le critère de médiane).
4. La table des statuts prête au recoupement des témoins signés.

## La vérification après modifications
Agrégateur fail-closed éprouvé (run manquant = refus exit 2) ; témoins signés
recoupés avant tout mouvement de la table ; autotests 57/57 re-verts ; AUCUNE
revendication « constant time proven » (le scope est l'échantillon, la machine,
les runs) ; entrée append-only.

## Les refus
Jamais un chiffre matériel fabriqué au laboratoire ; jamais un verdict partiel ;
jamais une cause élue d'avance ; jamais « proven » hors scope.
