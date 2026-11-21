# PLAN GELÉ — 14N3K8GD7 (la vague 12)
> Le double moteur validé généralisé à l'ouverture de session, et le budget de risque de la cristallisation incrémentale.
> Gelé AVANT toute mesure. Toute donnée suit ce plan ; tout écart est nommé au rapport.

## Le mandat (deux chantiers)
La décomposition des 37 s porte 81 % aux oracles (33,5 s sous Unicorn). Deux chantiers :

1. **Généraliser le double moteur validé à l'ouverture de session** (launcher ELF natif
   exécutant les octets scellés aux mêmes adresses, QEMU-user pour le volume, Unicorn pour
   l'audit) à TOUS les postes oracle de la liste fixe de la vague 5. La même image est
   construite par le harnais Unicorn réel (byte-identique par construction), la divergence
   doit être ZÉRO octet pour octet sur l'échantillon d'audit consigné, un shim muté du
   launcher doit être attrapé à la première ligne. Mesurer avant/après à l'horloge
   monotone, n=5, liste de commandes fixe, consoles des oracles exigées LIGNE-IDENTIQUES
   aux originales (le critère de non-affaiblissement).

2. **Formaliser le budget de risque de la cristallisation incrémentale** : pour un audit
   1/k sur la fermeture transitive du diff, publier P(détection par tirage), le temps
   espéré de détection sous un adversaire empoisonnant un bloc hors fermeture, et la borne
   de la semence full-card. Remplacer le tirage uniforme par un tirage pondéré par risque
   (fan-in du bloc, diffs récents, blocs porteurs de gardes) à budget de vérification
   ÉGAL, et re-démontrer la capture à la graine cherchée. Le modèle de menace du cache
   round-trip est étendu : entrées signées sous la clé de carte, liées à l'époque du
   moteur, invalidation nommée ; contrôle négatif sur le MAGASIN (substitution d'une
   entrée valide ancienne, rejeu inter-époque) → REFUS nommé, re-vérification complète.

## Les gestes
1. Ce plan gelé AVANT toute mesure.
2. Atelier atelier-double-moteur-14n3k8gd7/ : le launcher ELF natif (mêmes adresses que
   le scellé), le volume QEMU-user (si disponible au bac — sinon le gap nommé), l'audit
   Unicorn ; l'échantillon d'audit consigné ; le shim muté planté ; la mesure avant/après
   (horloge monotone, n=5, liste fixe).
3. Le budget de risque : les formules publiées (P(détection), temps espéré, borne
   full-card), le tirage pondéré par risque implémenté, la capture re-démontrée à la
   graine cherchée de l'atelier vague 11 (ahult8jgd).
4. Le cache round-trip étendu : entrées signées (clé de carte), liées à l'époque du
   moteur, invalidation nommée ; les deux contrôles négatifs du magasin REFUSÉS.

## La vérification après modifications
- divergence zéro sur l'échantillon d'audit aux deux moteurs ;
- shim muté attrapé ;
- les consoles d'oracle ligne-identiques ;
- empreintes des scellés intactes avant/après CHAQUE exécution ;
- cristal empoisonné hors fermeture → évasion nommée au tirage uniforme, capture
  démontrée au pondéré à la graine cherchée ;
- les deux contrôles négatifs du magasin de cache REFUSÉS ;
- réconciliation des totaux par run dans les tolérances publiées ;
- aucun vecteur retiré, aucune graine retirée ;
- sceau 14/14.

## Les refus
Aucun scellé modifié ; aucune console d'oracle réécrite pour passer ; le critère de
non-affaiblissement ligne-identique ; l'écart nommé par mesure, jamais ajusté.
