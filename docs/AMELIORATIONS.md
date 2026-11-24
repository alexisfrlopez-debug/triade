# LES CINQ AMÉLIORATIONS DE LA VAGUE 17 (D256–D260) — ET CE QU'ELLES CHANGENT

> Décidées le 24/11/2026 sur la commande du maître (« ok pour tes 5 suggestions »).
> Chacune est ACCOMPAGNÉE D'UN CONTRÔLE EXÉCUTABLE : une amélioration sans
> contrôle est un vœu. Les valeurs mesurées sont citées avec leur source.

## 1. La surface de gouvernance compressée par défaut (D256)

**Le constat mesuré.** 34 663 tokens par changement contre des budgets de
627/674/2 200 ; la forme compressée mesure 732 tokens (−97,9 %) — atelier
`couloirs-scelles-io3uh37cj`, Entrée 395.

**Le geste.** Un format canonique d'intention signée : version, opcode, empreinte
du contrat (8 o), longueur, corps, signature Ed25519 sur les octets canoniques.
Sur l'intention d'épreuve : 108 octets contre 154 pour l'équivalent JSON signé
(1,43× plus petit) ; un corps long paie le même en-tête de 11 octets.

**Le contrôle.** `scripts/vague17/gouvernance_compressee.py` — aller-retour,
signature, corps muté REFUSÉ, autre clé REFUSÉE, opcode inconnu REFUSÉ : 5/5.

## 2. Un seul juge : la grammaire devient la règle publiée (D257)

**Le constat mesuré.** Sur le corpus v2.1, le juge déclare 21 complétions vertes ;
la grammaire canonique TPL-ADD n'en accepte que **3** — 18 refus nommés :
13 étiquettes `LBL-xxx` que le contrat interdit, 3 mémoires nues sans taille,
1 mnémonique hors domaine, 1 autre étiquette.

**Le geste.** La grammaire est la règle ; toute campagne « contrainte » publie
les DEUX verdicts et l'écart. Une campagne qui ne le fait pas mesure un
changement de règle, pas un gain de modèle.

**Le contrôle.** `scripts/vague17/juge_grammaire.py` — rend `ÉCART NOMMÉ` (code 3)
tant que l'écart existe, `ALIGNÉ` (code 0) ensuite.

## 3. Le trampoline de huit octets, vérifié au build (D258)

**Le constat.** D253 : l'atomicité d'un magasin naturel s'arrête à huit octets ;
la promesse « 12 à 16 octets atomiques » était fausse.

**Le geste.** La forme courte (E9 rel32 + NOP, alignée 8) est la norme ; la forme
absolue de 12 octets n'est admise qu'avec `LOCK CMPXCHG16B` (CPUID) et un
emplacement aligné 16 ; tout le reste est refusé au build.

**Le contrôle.** `scripts/vague17/verifier_trampoline.py` — 7 cas, dont le
non-aligné, le remplissage non-NOP et la forme absolue sans CMPXCHG16B : 7/7.

## 4. Le témoin hors machine comme porte de release (D259)

**Le constat.** D254 : la restauration cohérente d'un couple binaire + état
échappe à toute ancre locale. Les témoins hors machine sont le seul remède.

**Le geste.** Avant toute release, un témoin consigné (carte papier, journal Git
poussé, ancre de transparence) doit attester : même édition, même empreinte,
époque ≥ celle de l'état, date non future. Sinon refus nommé.

**Le contrôle.** `scripts/vague17/temoin_fraicheur.py` — 6 cas ; la porte
d'édition le branche en **V6** et le déclare **EN ATTENTE** tant qu'aucun témoin
n'est consigné (jamais un vert de complaisance).

## 5. La performance en distance au plancher, les tableaux engendrés (D260)

**Le constat.** Les cibles en cycles absolus vieillissent avec la machine ; le
plancher de l'unité AES mesure 0,459 c/aesenc (4,59 c/bloc), le corps ent8@256
vit à 4,844 c/bloc — **1,055× le plancher**.

**Le geste.** Toute performance se publie en distance au plancher mesuré, à côté
des cycles ; et les tableaux se **engendrent** du registre de provenance
(12 lignes), à diff nul — plus de recopie manuelle.

**Le contrôle.** `provenance_tableaux.py --distance-plancher` (1,055×) et
`--tableaux` / `--tableaux-verifier` (le tableau descendant est identique au
registre, diff nul) ; la porte d'édition le branche en **V7**.

## Ce que ces cinq mesures ne règlent pas — nommé

- Le format compressé n'est pas encore dans la SPÉCIFICATION publiée : il entre
  à la prochaine édition (§ à écrire), avec le port du linter v2.
- L'alignement juge/grammaire exige de corriger 18 complétions du corpus ou la
  grammaire : le choix est un acte éditorial de la prochaine vague.
- Le témoin hors machine n'existe pas encore : la porte V6 reste EN ATTENTE
  jusqu'à la première consignation du maître.
- La distance au plancher n'est mesurée que sur les données d'époque (VM).
