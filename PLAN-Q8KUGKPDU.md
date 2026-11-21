# PLAN GELÉ — Q8KUGKPDU (la vague 13)
> Le statut exact des 58 gardes, la méthode et les bornes des 15 exclusions de
> mutants, le modèle Tamarin reformulé sans restriction.
> Gelé AVANT toute modification ; le verbatim historique demeure octet pour octet.

## Le mandat
Trois requalifications sur pièces, la table des statuts et le manuscrit alignés :

1. **Trancher le statut des 58 gardes** : les pièces (gardes_v210.csv, gardes/*.asm,
   gardes_smt/*.smt2) disent : les gardes SONT ÉMISES en COPIES DE LABORATOIRE à la
   marge 0x10000 (le modèle OPT-01), PAS dans le binaire scellé. Le verdict à publier :
   sur l'artefact scellé, les 58 déréférences sont « **conditional
   (assumption-discharged)** » — des obligations de preuve conditionnelles aux
   invariants externes ; l'émission runtime fail-closed est DÉMONTRÉE en variante de
   laboratoire (58/58 certificats UNSAT z3 deux côtés + falsification par garde aux
   deux bornes et à la face d'index, l'honnête admise). Le TCB publié en liste
   exhaustive : 24× champ du plan (CADRE 960 o, layout) · 23× contrat de l'appelant
   (contexte AEAD) · 11× l'OS (tampon de l'appel système) — la table générée du CSV.

2. **Publier la méthode et les bornes des 15 exclusions** : 12 par ARGUMENT
   SÉMANTIQUE sur la notation (chacun nommé : ensemble de lecture vide, sentinel
   adjacent, convergence des gardes, site hors table inatteignable, cible détournée
   retombant, RBP jamais relu) + 3 par SWEEP BORNÉ (3 cellules du bord × 10
   défilements = 30 scénarios, zéro écart sur l'observable complet) — PAS des preuves
   mécaniques non bornées. Le texte « mechanically proved equivalent » REMPLACÉ par
   le statut exact ; le score ajusté 811/817 requalifié « prouvé-argumenté borné » ;
   les 6 survivants non équivalents NOMMÉS par famille (shim aveugle ×3, voie de
   l'échec jamais servie ×2, code 3 jamais servi ×1) ; les dénominateurs publiés
   côte à côte (811/832 et 811/817 avec le statut des 15).

3. **Reformuler le modèle Tamarin CF3** : la restriction
   LAttaquantDolevYaoAuSeuilDesParts RETIRÉE ; le lemme d'implication ajouté
   (« secret appris ⇒ l'adversaire a détenu ≥3 parts » : All p #i. K(p) @ #i ==>
   Ex #j. ReconstitutionIllicite(p) @ #j & #j < #i) ; les lemmes de non-vacuité
   (trace honnête atteignable, témoin falsification/destruction) MAINTENUS ; le
   témoin d'atteignabilité du seuil AJOUTÉ (l'adversaire à 3 parts apprend — le
   modèle montre le seuil, il ne le suppose plus). tamarin-prover ABSENT du bac :
   le modèle v2 livré HASHÉ, l'empreinte consignée, LE GAP NOMMÉ au protocole de
   vérification, AUCUN verdict fabriqué.

4. **La table des statuts et le manuscrit** : statuts étendus (gardes, exclusions,
   Tamarin) ; l'abstract EN requalifié (les deux passages) ; le résumé FR ALIGNÉ
   (il ne porte NI le score, NI les gardes — le désalignement nommé à corriger).

## Les gestes
1. Ce plan gelé AVANT toute modification.
2. Atelier atelier-requalification-q8kugkpdu/ : le registre des 58 gardes généré du
   CSV (le TCB par famille), la table des 15 exclusions (méthode, bornes, noms), le
   CF3-v2.spthy hashé, le protocole de vérification mis à jour (le gap tamarin nommé),
   les requalifications du manuscrit aux lignes nommées (abstract 194-217, §floor
   2034-2044, §résultats 1043-1094, §limits 1752, §kits 2100-2107, table statuts).
3. La relecture intégrale des paragraphes modifiés (pas de grep seul).

## La vérification après modifications
- le TCB du registre somme à 58 exactement, les familles étiquetées ;
- la table des 15 : 12 + 3 = 15, chaque ligne porte sa méthode et sa borne ; les 6
  survivants nommés — la somme 811+15 exclus+6 survivants = 832 recompose ;
- CF3-v2.spthy : la restriction ABSENTE (grep par code), le lemme d'implication
  PRÉSENT, l'empreinte sha256 consignée au registre et au protocole ;
- le linter v230 re-roulé vert sur les cinq pièces v0.23.0 (le geste de ylrzmlbn8) ;
- sceau 14/14 avant et après ; append-only à DECISIONS et au worklog.

## Les refus
Aucun verdict Tamarin fabriqué (le prover absent, le gap nommé) ; aucun verbatim
historique réécrit ; aucun « prouvé » non borné étiqueté mécanique ; le manuscrit
corrigé, jamais le linter.
