# CHANTIER-OPTIMISATION-TOKENS — v1 (le 16/11/2026, l'Entrée 317)

La commande du développeur : « ensuite prochain chantier : optimiser le
protocole et trouver des solutions pour le cout en token ». Ce document
ouvre le chantier selon la loi du projet : LA MESURE AVANT TOUT (R11),
la hiérarchie verrouillée (D19 : Sécurité > Performance > Optimisation >
Coût en tokens — invariant de révision), et l'instrumentation qui suit
chaque geste (CA3 : 100 % des tokens lus des logs d'usage, jamais
estimés).

---

## 1 · LA MESURE AVANT TOUT — l'anatomie du coût

### 1.1 L'unique unité entièrement instrumentée de la campagne (loupe-01)

La campagne D204 a mesuré la première unité aux DEUX bras, chaque appel
lu du champ usage de la réponse (journal_tokens.jsonl — zéro estimation) :

| Phase | Bras T (notation) | part | Bras C (gcc -O2) | part |
|---|---|---|---|---|
| lecture de spécification | 5 313 | 10,0 % | 5 605 | 8,3 % |
| dérivation d'oracle (écrit-avant-code) | 3 752 | 7,1 % | 4 423 | 6,6 % |
| rédaction (notation à la main / source C) | 11 480 | 21,6 % | 14 660 | 21,7 % |
| **correctifs** | **32 613** | **61,4 %** | **39 224** | **58,1 %** |
| phase de tests (bras C seul) | — | — | 3 563 | 5,3 % |
| **TOTAL (M2)** | **53 158** | 100 % | **67 475** | 100 % |
| appels instrumentés | 9 | | 11 | |

Le rapport C/T = 1,27 : le bras compilé a consommé 27 % de tokens de
PLUS que le bras notation sur cette unité (la direction opposée à
l'hypothèse pré-enregistrée H3 — consignée au manuscrit v0.16.0).

### 1.2 Le hot path

**Le coût dominant est la spirale corrective : 61,4 % (T) / 58,1 % (C)
des tokens vont aux tours de correction** — six appels au bras T, sept
au bras C, chacun rec portant le contexte entier de l'unité (contrat +
rédaction + oracle + console). C'est ici, et nulle part ailleurs, que
le chantier attaque.

### 1.3 L'ère de la carte (pour mémoire, D195)

Les opérations de carte mesurées sur la carte finale : localiser 580
tokens [496-706] ; éditer 2 143 [1 085-3 463] ; ajouter 3 510
[3 128-4 091] ; baseline naive (désassemblage entier de loupe.exe) :
300 304. La lecture défavorable demeure : les opérations de l'ère
Loupe coûtent 3-11× celles de l'ère M1 (51/719/1 088) — la rigueur a
grossi le contexte. Le chantier vise le portage, pas la rigueur.

---

## 2 · LA LOI DU CHANTIER (les contraintes non négociables)

1. **La hiérarchie D19, invariant de révision** : Sécurité >
   Performance > Optimisation > Coût en tokens. Aucun levier ne peut
   toucher la discipline des défauts nommés, le verrou des arbres
   signés, ou la frontière oracle/terrain.
2. **CA3 tenu** : chaque appel reste instrumenté (compter_tokens.py
   lit le champ usage) — un levier optimisé qui échapperait à la mesure
   est un levier rejeté.
3. **R2 / R5 intacts** : écrit-avant-code et vérifie-puis-écris ne
   bougent pas. Les leviers réduisent le PORTEAGE du contexte, jamais
   l'obligation de dériver avant d'écrire.
4. **La règle des manquants nommés** (le plan D204 § 4) : un appel non
   loggé est un écart nommé, jamais un chiffre reconstruit — le levier
   L6 guérit la cause à la source.
5. **M3/M4 suivent** : le temps humain (carnet) et le temps de
   vérification (chronomètre) restent mesurés à chaque geste — une
   économie de tokens qui coûte du temps humain est un mauvais trade
   (D19 le dit : le coût en tokens est DERNIER).

---

## 3 · LES LEVIERS (rangés par économie attendue sur le profil mesuré)

### L1 · Circonscrire le contexte des correctifs — l'attaque au 61 %

**Mécanisme.** Un tour de correction ne rec porte que trois choses : le
défaut NOMMÉ (classe + mécanisme + pièce à l'appui), le fragment
touché (le bloc de la carte, ses bornes d'octets), et le vecteur
d'oracle qui a échoué. Le format PATCH (né au bras C de l'unité 1 pour
vaincre les troncations : les remplacements exacts + la suite) devient
le FORMAT DE CORRECTION du protocole : le juge produit un
**bundle-défaut** (défaut + fragment + vecteur, jamais la rédaction
entière). Le six-tours de loupe-01 aurait porté ~6 × (défaut + bloc +
vecteur) au lieu de 6 × l'unité.
**Économie attendue (à mesurer)** : 30 à 50 % de la phase corrective —
sur le profil mesuré : ~10 à 16 k tokens par unité, soit **20 à 30 %
du total**.
**Tenue des lois** : R5 renforcé (le bundle EST le voisinage de
vérification) ; la correction reste diffée par pièces (byte-diff).
**Coût** : l'outil auteur (le même qui assembla le PATCH du bras C),
une demi-session.

### L2 · L'oracle par fragment, jamais par contrat entier

**Mécanisme.** La phase d'oracle dérive les attentes du juge depuis le
contrat ENTIER ; seuls les vecteurs du bloc en construction servent.
La carte porte déjà frag-con (les invariants par bloc) : le
**frag-oracle** (les vecteurs attendus du bloc, dérivés à la
construction et scellés avec la couche I) remplace la re-dérivation.
**Économie attendue** : 30 à 40 % de la phase oracle (~1,2-1,5 k par
unité).
**Tenue** : l'oracle est régénéré DEPUIS I (la règle demeure) — le
frag-oracle EST une lecture de I, signée.
**Coût** : une extension du format de carte, une session.

### L3 · Le digest de contrat (le cache de la couche I signée)

**Mécanisme.** Chaque unité relit le contrat entier (5 313 tokens) ;
les contrats sont SIGNÉS et stables. Un **digest de contrat** (l'ID +
les sections + l'empreinte par section, produit une fois à la signature
de l'arbre) permet à une nouvelle unité de ne lire que la section du
bloc + les deltas depuis sa propre naissance.
**Économie attendue** : 40 à 60 % de la phase de spéc (~2-3 k par
unité).
**Tenue** : la lecture demeure DE LA COUCHE I (jamais d'un cache
non signé — le digest est dérivé de l'arbre signé, vérifié par
empreinte).
**Coût** : une passe sur le sceau, une session.

### L4 · Les gabarits de notation du domaine (le squelette versionné)

**Mécanisme.** La rédaction à la main (11 480) réécrit à chaque bloc le
prologue/épilogue du domaine (l'espace d'ombre, l'alignement, le plan
d'adressage R7, les conventions d'appel) — la GRAMMAIRE de la notation,
pas son contenu. Un **squelette par domaine** (versionné AVEC la couche
I, écrit une fois, mesuré une fois) laisse la rédaction au cœur
spécifique du bloc.
**Économie attendue** : 20 à 30 % de la phase de rédaction (~2,5-3,5 k
par unité).
**Tenue** : R2 INTACT — le squelette est la syntaxe, le bloc reste
écrit-avant-code ; le round-trip WYSIWYG demeure la preuve (le squelette
assemblé se round-trippe comme toute notation).
**Coût** : deux sessions (un par domaine), la mesure du gain au
premier usage.
**RISQUE NOMMÉ** : le squelette peut masquer des choix qui DOIVENT
rester explicites (l'espace d'ombre de l'ABI — la classe de défaut de
la faute 4). Le squelette est donc VÉRIFIÉ par l'audit msx64 à chaque
assemblage — la loi de l'audit demeure.

### L5 · L'index d'instructions dans la carte (l'édition au voisinage)

**Mécanisme.** L'édition de carte (2 143 tokens, l'ère D195) relit le
frag-con + la notation du bloc ENTIER. La carte gagne un **index
d'instructions par bloc** (adresse → longueur, dérivé à l'assemblage —
le round-trip le produit déjà) : l'édition ne porte que le voisinage de
l'instruction visée + les bornes.
**Économie attendue** : 30 à 40 % de l'opération d'édition (~600-900
tokens par édition).
**Tenue** : la carte reste l'index (jamais le binaire) ; l'index est
dérivé, jamais écrit à la main.
**Coût** : une extension du format de carte + un passe sur le
vérificateur de round-trip.

### L6 · Réparer la rig d'instrumentation (les M2 manquants nommés)

**Mécanisme.** Les unités 2+ de la campagne ont vu leurs appels passer
hors journal (l'écart NOMMÉ à l'Entrée 289) — la mesure est la
condition du chantier : sans M2 complet, aucun gain ne peut être
consigné. compter_tokens.py est câblé dans CHAQUE outil auteur du labo
(le builder, l'outil de correctif, l'outil de tests) — le journal
naît des outils, jamais de la mémoire.
**Économie** : nulle (c'est la mesure) — mais le n=1 devient n+.
**Tenue** : CA3 guéri à la source (la guérison vit à la source, la
leçon D202).
**Coût** : une demi-session de rig.

### L7 · Les suites du bras C réutilisées (le compilé aussi)

**Mécanisme.** Le bras C paie tests-c (3 563) + une rédaction plus
longue (14 660 vs 11 480) ; les harnais de tests par domaine sont
réutilisables d'unité en unité (le même juge hashlib, les mêmes
générateurs) — la phase de tests devient une LECTURE de harnais
existant, pas une rédaction.
**Économie attendue** : 30 à 50 % de tests-c (~1-1,8 k par unité C).
**Tenue** : le juge indépendant demeure (jamais la pièce jugeant la
pièce).

---

## 4 · L'ARITHMÉTIQUE ATTENDUE (honnête — n = 1, à mesurer)

Sur le profil mesuré de loupe-01 (bras T, 53 158 tokens) :

| Levier | Phase attaquée | part du total | économie attendue |
|---|---|---|---|
| L1 correctifs circonscrits | 32 613 | 61,4 % | −10 à −16 k |
| L4 squelettes de domaine | 11 480 | 21,6 % | −2,5 à −3,5 k |
| L2 oracle par fragment | 3 752 | 7,1 % | −1,2 à −1,5 k |
| L3 digest de contrat | 5 313 | 10,0 % | −2 à −3 k |
| **potentiel cumulé (naïf)** | | | **−16 à −24 k (−30 à −45 %)** |

Au bras C (67 475) : L1 (−12 à −20 k) + L7 (−1 à −1,8 k) + L3/L2
(−3 à −4 k) → potentiel −25 à 35 %.

**LA LECTURE HONNÊTE** : ces bornes sont une ATTENTE projetée sur UNE
unité mesurée — jamais une promesse ; les leviers interagissent (L1
réduit le portage que L4 réduit aussi) ; le plan de mesure (§ 5) seul
rendra les chiffres. Le gain se juge AUSSI aux M1/M3/M4 : un levier
qui dégrade le taux d'échappés ou le temps humain est REJETÉ (D19).

---

## 5 · LE PLAN PRÉ-ENREGISTRÉ (la proposition de décision D207)

Le chantier se consigne comme les autres : un plan AVANT la mesure.

- **D207 (proposée)** — LE PLAN D'OPTIMISATION DU COÛT EN TOKENS : la
  hiérarchie D19 réaffirmée (le token est DERNIER) ; les leviers L1-L7
  définis avant toute mesure de gain ; l'ordre d'application SÉQUENTIEL
  (un levier par unité mesurée, jamais deux — l'attribution exige
  l'isolement) ; la baseline = la prochaine unité entièrement
  instrumentée (L6 d'abord) ; les quatre métriques M1-M4 maintenues à
  chaque unité ; LA RÈGLE D'ARRÊT : un levier qui dégrade M1 (un
  échappé imputable au levier) ou M3 (le temps humain) est REJETÉ et
  consigné ; les OPT-NN du journal d'optimisation (le format D205 :
  la mesure avant tout, le gain mesuré, le vérificateur).
- **La séquence proposée** : L6 (la rig, une demi-session) → la
  baseline (l'unité suivante au complet, deux bras) → L1 (le levier
  dominant, bundle-défaut) → L3 → L2 → L4 → L5/L7. Chaque étape : une
  unité de campagne mesurée, le delta consigné par phase, l'OPT-NN au
  journal.
- **Le juge** : les deltas lus des mêmes logs (journal_tokens.jsonl,
  le même champ usage) ; les mêmes commandes M4 (chronomètre) ; le
  carnet M3 au geste du développeur.

---

## 6 · LA FRONTIÈRE (ce que le chantier ne fera pas)

- Aucune suppression de l'écrit-avant-code (R2) ni du
  vérifie-puis-écris (R5) : le levier réduit le PORTEAGE, jamais
  l'obligation.
- Aucun cache non signé : tout digest est dérivé de l'arbre signé et
  vérifié par empreinte.
- Aucun oracle contourné : le frag-oracle EST la couche I relue.
- Aucune optimisation non mesurée (R11) : le journal d'optimisation
  porte chaque OPT-NN avec sa mesure avant et son gain après.
- Aucun trade du taux d'échappés contre des tokens (D19) : la règle
  d'arrêt est armée dès la première unité.

---

*Le chantier est ouvert : la rig (L6) est le premier geste — la mesure
est la condition de tout le reste. Ce document vit au coffre (racine),
la version PDF au /test ; le journal d'optimisation portera les OPT-NN.*
