# PLAN GELÉ — 0J7YWZA2H (la campagne TPL-ADD-v6 : le décodage contraint et les paires DPO)

> Le mandat : pré-enregistrer une campagne TPL-ADD-v6 visant **≥ 15/18 verts à
> ≤ 4 500 tokens par changement validé**, aux mêmes graines et aux mêmes juges
> (la chaîne v2 + les validateurs v3 INTACTS, jamais affaiblis). Deux leviers :
> le décodage contraint par la grammaire canonique de la notation, et les paires
> DPO à grande échelle par rejection sampling dans TRIADE-GYM. Gelé AVANT toute
> mesure ; l'empreinte du plan précède la première donnée.

## Le mandat

(1) **LE LEVIER DÉCODAGE CONTRAINT** : la grammaire canonique de la notation
devenue CONTRAINTE au décodage (GBNF / outlines / xgrammar en serving local, ou
provider exposant structured outputs) pour éliminer la classe HORS-FORMAT à la
source — la notation qui ne peut pas naître hors format ne coûte ni rejet ni
re-tentative. **LA RÈGLE DE L'INSTRUMENT, RECONDUITE DE L'ENTRÉE 392** : si le
CLI n'expose pas `response_format`, le serving contraint est LIVRÉ COMME
INSTRUMENT et l'écart est NOMMÉ — jamais une mesure habillée en contrainte.

(2) **LE LEVIER DPO** : la génération de paires DPO à grande échelle par
rejection sampling dans TRIADE-GYM — pour chaque contrat, échantillonnage de k
complétions, appariement notation VERTE vs REFUS **au même contrat**
(récompense = le verdict du juge, **jamais la similarité**), scrub fail-closed,
split étanche par contrat.

(3) **LES RECETTES ET LE BUDGET** : les recettes SFT / DPO / RLVR livrées
agnostiques en famille, et le budget compute CONSIGNÉ (le compute reste au
développeur — la route nommée à l'Entrée 393).

## Les gestes

1. Le plan gelé ; l'empreinte consignée à `EMPREINTES-PLANS-VAGUE16.txt` ; LE
   COMMIT D'ABORD (la règle reconduite des vagues 8-15).
2. **L'INSTRUMENT** : le serving contraint — la grammaire canonique de la
   notation (le matériau TPL-ADD de `loupe/` et `tls13/notation/`) rendue en
   GBNF et en xgrammar, le harnais de conformité (la complétion HORS-FORMAT
   REFUSÉE PAR LA GRAMMAIRE, pas par le juge : le contrôle négatif de
   l'instrument, avant toute campagne).
3. **LA CAMPAGNE v6** : le re-jeu aux graines consignées (bit-identique à
   l'extraction), la comparaison v5→v6 **par classe de refus**.
4. **LES PAIRES DPO** : k complétions par contrat, l'appariement par contrat,
   le contrôle anti-hacking P2 (aucune notation mutée à la récompense).
5. **LE RAPPORT** : les opérandes NON ARRONDIS, le déplacement v5→v6 par classe
   de refus, le budget compute, la lecture DÉFAVORABLE si la cible est manquée.

## La vérification après modifications

Le re-jeu aux graines consignées (bit-identique à l'extraction) ; les juges
INTACTS (les falsifications re-vertes au sceau 14/14 avant et après) ; le
contrôle anti-hacking P2 refuse toute notation mutée à la récompense ; les
paires DPO étanches PAR CONTRAT ; la lecture DÉFAVORABLE consignée si la cible
est manquée (jamais un chiffre ajusté, jamais une cible re-tirée) ; les
opérandes non arrondis et le déplacement v5→v6 par classe de refus publiés.

## Les refus

Jamais un verdict fabriqué ; jamais une cible re-tirée ; jamais un juge
affaibli ; jamais la similarité comme récompense ; jamais une paire à cheval
sur deux contrats ; jamais une paire DPO tirée d'un refus scrubbeux ; jamais
une mesure de contrainte sans l'instrument qui la porte.
