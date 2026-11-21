# PLAN GELÉ — YLRZMLBN8 (la vague 13)
> La génération v0.23.0 : les écarts (a)-(f) du pack v0.22.0 portés aux pièces, les
> abstracts EN/FR depuis les MÊMES macros, le manuscrit refactoré à la voix
> « présent édition » unique.
> Gelé AVANT toute correction ; le verbatim historique demeure octet pour octet.

## Le mandat
Six écarts constatés, six corrections sur pièces, un refactoring :

(a) **La batterie 559** : la décomposition publiée « 64+3 queue · 4 chevauchants ·
13 longueurs · 3 pages · 8 multi · 512 » sommait à 607 ; le registre brut de
fnvan0zes (census_batterie.py, D244) porte **16 queue-16 + 3 queue-fin + 4
chevauchants + 13 longueurs + 3 pages + 8 multi + 512 property-based = 559
exactement**. La partition exacte publiée aux CINQ pièces (manuscrit, preuves —
ERRATUM append-only au texte des preuves v0.23.0, le modèle decomposition_corrigee
de v220 —, présentation, Livre, spec), étiquettes et comptes identiques ; le rapport
historique fnvan0zes DEMEURE verbatim.

(b) **Les longueurs** : le manuscrit « lengths 1–33 » ↔ les preuves « 13 longueurs » :
les DEUX exacts ENSEMBLE (les 13 longueurs COUVRENT 1–33 — la liste nominale
1,2,3,4,15,16,17,18,19,20,31,32,33 publiée une fois, la prose alignée).

(c) **Les opérandes non arrondis** : chaque ratio de la vague 11 publié avec ses
canons (ajouter 3 073,5 → 2 199,5 = −28,4 % ; cache 285,725 → 0,418 ms = ×683,6 ;
régime 39,24/2,163 = 18,1×) ; le « −28,5 % » corrigé PARTOUT (manuscrit l.1973 et
l.280, générateurs de présentation et de preuves) ; les macros \gabarit* BRANCHÉES
(aucun nombre cité sans macro sourcée).

(d) **Les abstracts EN et FR depuis les MÊMES macros** : une seule source de données
(gabarits, mutation, conformité, quatre bras, SIMD) ; le résumé FR ne titre PLUS les
valeurs v0.17/v0.19.6 (1 103/1 277/3 374/3 674) mais LES MÊMES canons que l'EN ; la
campagne générative alignée (30 000 traces, zéro divergence — le FR disait 10 000/une
classe d'écart : LE DÉSALIGNEMENT NOMMÉ ET CORRIGÉ).

(e) **La table canonique « budgets adoptés »** : une seule table (localiser 627
hiérarchique / éditer 674 TPL-EDIT-v1 / ajouter 2 200 squelette AVEC faisabilité
3/18 AU MÊME RANG — les résultats vague 13 à côté), chaque valeur portant ID de
décision, périmètre et statut (adopté/mesuré/historique) ; le dashboard de la spec
(Tableau 19) ALIGNÉ sur cette table (les budgets M1 51/719/1 088 deviennent
historiques datés) ; le dashboard brut de l'atelier régénéré.

(f) **« settled » scopé** : remplacé par la formulation exacte — la dérivation outillée
inter-familles à zéro divergence (128 constantes régénérées des définitions
mathématiques seules) ; la récitation pure par la seconde famille LOCALE hors
capacité du modèle disponible (0/64), le gap de capacité NOMMÉ (cohérence corps
l.1180-1196 et conclusion l.2163-2166).

5. **Le refactoring** : le corps = état courant UNIQUE (la voix « present edition »
unique — les ~18 redoublements narratifs par édition remplacés par l'état courant ;
les onzième et douzième vagues au changelog) ; **le changelog gelé** des vagues
(une section « Edition changelog » : v0.14.0 → v0.23.0, chaque vague UNE ligne
datée, le détail aux rapports d'atelier) ; chaque nombre via macro sourcée.

## Les gestes
1. Ce plan gelé AVANT toute correction.
2. edition-v0230/ né de v0220 (copie puis refactor) ; macros_v230.tex régénéré ;
   statuts_v230.tex (les lignes de q8kugkpdu) ; les générateurs preuves/présentation
   v0.23.0 ; le pack assemblé (manuscrit, spec v0.15.8, Livre v1.7, preuves,
   présentation) aux empreintes consignées.
3. Le linter v230 sur les cinq pièces (il attend edition-v0230) : zéro divergence ;
   les contrôles négatifs (somme fausse injectée, ratio à opérandes faux, version
   périmée injectée → chacun refusé nommément).

## La vérification après modifications
- la partition de la batterie somme exactement au total publié, aux mêmes étiquettes
  dans les cinq pièces ;
- les abstracts EN/FR comparés champ à champ par script : zéro écart de valeur ;
  re-tokenisation indépendante des budgets cités (écart ≤ 1 token) ;
- le linter v230 : zéro rouge, les contrôles négatifs vécus ; sceau 14/14 avant et
  après ; les empreintes des pièces régénérées consignées et croisées entre
  présentation et table des preuves.

## Les refus
Jamais un chiffre retapé à la main (macro sourcée ou rien) ; jamais le verbatim
historique réécrit (l'erratum vit au texte des preuves, à côté) ; jamais la version
périmée au dashboard courant.
