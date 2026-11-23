# PLAN GELÉ — 86D3USHRR (les six résidus des cinq pièces v0.23.3)

> Le mandat : corriger les six résidus (A)–(F) dans les cinq pièces v0.23.3,
> **chacun par une décision append-only** — jamais une réécriture des entrées
> historiques. Le linter v2 ÉTENDU aux trois contrôles nouveaux. Gelé AVANT
> toute correction ; l'empreinte précède la première donnée.

## Le mandat

**(A) LES MÉDIANES GHASH NON ARRONDIS** (règle D244) : publier les médianes
non arrondies (ex. 63 394 / 19 658) pour que le ratio 63,39 / 19,66 recalculé
donne **exactement** la valeur publiée ; le ratio aligné sur les opérandes non
arrondis.

**(B) LE RECOMPTE DES TRIPLES** : recompter les triples du corpus DEPUIS LES
FICHIERS LIVRÉS et le manifeste sha256 ; résoudre l'écart 97 + 13 ≠ 109 (delta
réel 12) ; consigner le compte exact PAR SPLIT (tâches et triples) et la cause
du triple manquant ou du compte initial erroné.

**(C) LE PÉRIMÈTRE DE LA CIBLE HEADLINE** : aligner la cible ≥ 15/18 avec le
split TEST réel (4 tâches / 16 triples) — soit la cible porte sur les 18
tâches régénérées de la ladder (le NOMMER), soit elle est re-scopée au TEST ;
le choix CONSIGNÉ.

**(D) LE LIVRE DU COFFRE** : aligner le titre du chapitre 11 et la couverture
sur la plage réellement listée dans la table (D75–D137) OU compléter la table
jusqu'à D250 depuis `docs/DECISIONS.md`.

**(E) LA SPÉCIFICATION** : déplacer les sections « ce que change v0.15.3/4/5 »
de § 4 vers § 1.19–1.21 dans l'ordre croissant ; ajouter les sections
manquantes v0.15.6/7/8 ; recale le TOC.

**(F) LE LINTER v2 ÉTENDU** — trois classes nouvelles :
- classe B : la plage annoncée vérifiée contre la TABLE LOCALE (pas seulement
  le journal) ;
- classe C : tout ratio publié se RECALCULE depuis ses opérandes publiés à la
  précision affichée ;
- classe D : la cohérence cible-périmètre (n tâches du split vs n de la cible).

## Les gestes

1. Le plan gelé ; l'empreinte consignée ; LE COMMIT D'ABORD.
2. **LES SIX DÉCISIONS** (D-numérotées, append-only, chacune avec sa pièce et
   sa preuve de calcul).
3. **LE LINTER v2 ÉTENDU** (`scripts/vague14/linter_v232.py` → la classe B
   corrigée, les classes C et D nouvelles) et ses contrôles négatifs plantés.
4. **LA RÉGÉNÉRATION DES CINQ PIÈCES** (tectonic + weasyprint) — si la chaîne
   est absente du poste, l'écart est NOMMÉ et les décisions restent livrées.
5. **LE RAPPORT VERBATIM APPEND-ONLY**.

## La vérification après modifications

Les cinq pièces régénérées ; le linter v2 étendu passe VERT avec les
**5 + 3 contrôles négatifs plantés ATTRAPÉS** ; chaque ratio modifié recalculé
MÉCANIQUEMENT depuis ses opérandes (zéro divergence) ; les triples recomptés
depuis les fichiers (la somme des splits == le total annoncé) ; les empreintes
sha256 des cinq pièces recoupées au manifeste du pack ; le rapport verbatim
append-only ; le sceau-I 14/14 avant et après.

## Les refus

Jamais une entrée historique réécrite ; jamais un ratio publié qui ne se
recalcule pas ; jamais un recompte qui ne somme pas ; jamais un contrôle qui
passe sans que le négatif planté soit attrapé ; jamais une pièce régénérée
sans sa chaîne nommée ; jamais une correction silencieuse.
