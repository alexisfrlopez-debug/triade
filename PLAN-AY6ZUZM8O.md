# PLAN GELÉ — AYZUZM8O (la vague 13)
> H-CGP3 pré-enregistré : la ventilation à quatre bras sur la PILE OPTIMISÉE, les
> volumes ÉGALISÉS, le confond « notation intrinsèque » vs « implémentation du
> harnais » tranché par mesure.
> Gelé AVANT toute mesure ; la graine de randomisation consignée avant le premier
> tirage.

## Le mandat
La vague 11 a mesuré la ventilation (notation propre 20,72 s / régime 16,50 s /
gouvernance 0,213 s) avec le bras T sur l'outil vague 9 NON optimisé (39,4 s) et une
asymétrie de rebuilds 12 vs 60. La pile adoptée mesure ~6,9 s ailleurs. H-CGP3 sépare
les effets :

1. **Le pré-enregistrement** : ce plan hashé AVANT toute mesure. **H-CGP3 (énoncé
   falsifiable)** : sur la pile optimisée, à volumes de rebuilds et d'oracle ÉGALISÉS
   par unité, la part de l'effet NOTATION INTRINSÈQUE (round-trips + recomposition +
   cristallisation, HORS oracles) dans T−C est **≤ 30 %** — le coût dominant de la
   vague 11 étiqueté « notation » était l'effet IMPLÉMENTATION DE VÉRIFICATION
   (oracles, émulation vs natif). Si la part mesurée > 30 %, H-CGP3 REJETÉE et le
   verdict dit que le coût intrinsèque domine. **Marges d'équivalence fixées à
   l'avance** : réconciliation par run aux tolérances vague 11 (T ±0,150 s ·
   C+G+ ±0,100 s · C+G, C ±0,050 s) ; l'égalisation exigée par unité (table par
   unité publiée) ; la classification par poste (notation intrinsèque /
   implémentation de vérification / régime / gouvernance) figée au présent document :
   - notation intrinsèque : round-trips de notation, recomposition du plan,
     cristallisation ;
   - implémentation de vérification : oracles (re-exécutions vivantes), gardes de
     sceau, confrontations d'octets ;
   - régime : rebuilds (compilations gcc / re-vérifications de volume) ;
   - gouvernance : g1–g4.

2. **Les quatre bras sur la pile optimisée** : T = l'outil M4 complet en mode CHAUD
   (mémo v2 + double moteur QEMU-user/Unicorn + cache de round-trip +
   cristallisation incrémentale), rebuilds égalisés (10 rebuilds × 6 unités = 60 par
   bras, T inclus) ; C+G+ = le C gcc-O2 avec gouvernance et régime complet égalisé ;
   C+G ; C. Même machine, **n ≥ 5 par bras**, **ordre des bras randomisé dans chaque
   run** (random.Random, graine consignée AVANT le premier tirage), volumes d'oracle
   égaux (u01 : 12 épreuves/14 contrôles ; u02 : 2 032 décalages, graine 20261114).
   QEMU-user 11.1.3 re-extrait au bac (la version vague 12, l'empreinte consignée).

3. **Les contrôles négatifs double fenêtre rejoués** : inter-étapes et in-étape
   (+500 ms), la normalisation de dérive reconduite (déviation normalisée > 0,30 s ET
   valeur > 2× médiane de l'étape), 0 faux positif exigé sur les runs honnêtes ;
   toute session interrompue archivée sans fusion (le précédent session-interrompue-1).

4. **La publication côte à côte** : les DEUX ventilations (vague 11 datée sur l'outil
   non optimisé / vague 13 sur la pile optimisée), les verdicts H-CGP2 et H-CGP3
   DISTINCTS et datés, JAMAIS fusionnés ; la décomposition par poste des quatre bras
   aux QUATRE effets nommés.

## Les gestes
1. Ce plan gelé AVANT toute mesure.
2. Atelier atelier-hcgp3-ay6zuzm8o/ : le pilote quatre bras (composition de la pile
   optimisée, ordre randomisé, registres m4v13-*.json), le réconciliateur (quatre
   effets), le rig des contrôles négatifs, les registres bruts.
3. Les mesures : l'horloge monotone par étape, les consoles ligne-identiques aux
   originales (hors horodatages nommés), les empreintes des scellés avant/après
   chaque run.

## La vérification après modifications
- la réconciliation de chaque total depuis ses étapes aux tolérances publiées
  (20/20 runs) ; la somme de la ventilation == T−C à la milliseconde ;
- les consoles d'oracle ligne-identiques ; les scellés 14/14 avant/après chaque run ;
- le contrôle négatif +500 ms attrapé aux DEUX fenêtres, attribué au premier nom,
  zéro faux positif sur les honnêtes ;
- le rejeu à graine identique des TIRAGES d'ordre bit-identique ; les registres bruts
  archivés ; les gaps nommés (une seule machine virtualisée, n=5).

## Les refus
Aucun chiffre fabriqué ; aucune session interrompue fusionnée ; les verdicts vague 11
et vague 13 jamais confondus ; l'asymétrie de volumes jamais reintroduite en silence.
