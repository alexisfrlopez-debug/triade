# PLAN PRÉ-ENREGISTRÉ — LE RENFORCEMENT DU PROGRAMME DE PREUVE CF3 (89488hblm)

**Le gel** : ce plan précède TOUTE donnée de vérification (règle D204/D211
reconduite — le commit qui le scelle précède la première exécution). Son
sha256 sera consigné au journal des décisions. AUCUN des runs décrits
ci-dessous n'a été exécuté à l'heure du gel ; les modules TLA+ du présent
atelier ont subi la seule passerelle de COMPILATION (apalache parse —
huit EXITCODE: OK), qui n'est pas une mesure.

**L'instruction** (89488hblm, reçue au /instructions, exécutée ici) :
(a) remplace la confrontation TLA+↔sémantique Python échantillonnée
(512 états/règle) par une équivalence déchargée par SMT sur entiers non
bornés, garde-à-garde et effet-à-effet, pour chacune des 13 règles et
tout état bien typé ; (b) explicite et décharge le lemme O3 (bijection
288 formes ↔ image des états bien typés satisfaisant l'invariant) par
SMT non borné, en distinguant clairement ce qui est prouvé de ce qui est
énuméré borné ; (c) formalise l'argument d'uniformité en époque en un
lemme de translation quantifié (∀δ) déchargé mécaniquement, au lieu du
seul audit syntaxique + translations {7, 50, 1000}. Conserve les
contrôles négatifs existants et ajoute-en UN PAR NOUVELLE OBLIGATION
(affaiblissement volontaire devant être attrapé). ÉTAPE DE VÉRIFICATION :
rejoue la batterie complète de model-checkers (TLC borné : 154 états /
1 152 transitions reproduits exactement ; Apalache/SMT : Init⟹I et
I∧Next⟹I′), exige 8/8 vert avec verdicts.json bit-identique au consigné
PLUS les nouvelles obligations, vérifie que chaque contrôle négatif est
bien attrapé, et rejoue la campagne de conformité 10 000 traces à graine
identique en exigeant la reproduction bit-à-bit des 10 000 digests.

---

## 0. L'OUTILLAGE RE-PROVISIONNÉ — ET L'ÉCART NOMMÉ

- **Apalache 0.63.0** : tarball amont
  `github.com/apalache-mc/apalache/releases/download/v0.63.0/apalache-0.63.0.tgz`,
  sha256 **a756e96af249bf33cd7629667a49472cb26ac8227c48583da139b414834d59df ==
  l'empreinte consignée** (outils_consignes.txt). EXACT, recoupé.
- **tla2tools.jar (TLC)** : l'ÉCART NOMMÉ. L'octet-à-octet consigné
  (e1f11b75c4b5bc4478ba0ac5cb6ae28e40a01b0016bc33e0aa97da22dfdbcd7f)
  **n'est plus obtensible à l'amont ce jour** : la release v1.8.0 est un
  dépôt roulant (le tag suit chaque build master) ; l'asset actuel —
  digest sha256 7e53aa636dac8a3cb0533f343115c0548e03fc0ce5edc7739becf58d3d0fb84f
  attesté PAR GITHUB, asset créé 2026-11-15T00:27:39Z jamais remplacé —
  est le build **2026.11.15.002146, rev bc1b506**, LA VERSION ET RÉVISION
  EXACTES des journaux consignés (logs/tlc_fidelite.txt). La fonction de
  l'outil est déterminée par sa version+révision, identiques ; le recoup
  FONCTIONNEL exigé par le présent plan : LA BATTERIE ORIGINALE REJOUÉE
  DOIT REPRODUIRE LES COMPTES CONSIGNÉS AU NOMBRE EXACT (154/216/360) ET
  LES VERDICTS 8/8 BIT-IDENTIQUES — sinon l'atelier ÉCHOUE (échec fermé).
- **Java** : OpenJDK 21.0.13 (le même runtime que les logs consignés).
- Le socle : CF3.tla copié au présent atelier depuis scripts/tla_v150/,
  md5 b762c2c8627f699a11b62a8004900905 recoupé == le dépôt.

## 1. LE POINT (a) — L'ÉQUIVALENCE PAR RÈGLE, SMT NON BORNÉ

**Les modules** : CF3Equiv.tla (les deux sémantiques : côté TLA+ les
règles RÉELLES via EXTENDS CF3 — zéro retranscription pour les
relations ; côté Python la transcription fidèle de
modele_invariant_v150.py : GP_r la garde effective — l'offre ∧
appliquer ≠ None —, FP_r l'effet ; le seuil Python LITTÉRAL
Cardinality(sait ∩ Elements) ≥ 3) ; CF3EquivDiff.tla (l'enveloppe du
témoin diff — l'égalité relationnelle exige un invariant non-violé à la
profondeur 0 : la transition XOR pose diff′ = TRUE, l'invariant
diff = FALSE tombe à la profondeur 1 si et seulement si le XOR est
non vide) ; CF3EquivControles.tla + CF3EquivDiffC.tla (les 26 mutations).

**Les 26 obligations nouvelles** (une par règle × aspect, tout état bien
typé — e ∈ Int NON BORNÉ) et leurs runs Apalache :

- **13 × EQUIV_GARDE_r** : Init = TypeOK, Inv = OblGarde_r
  (GP_r ⟺ GT_r — la garde Python contre la garde TLA+ extraite),
  longueur 0. Attendu : **NoError** pour chacune.
- **13 × EQUIV_EFFET_r** : Init = InitTypeOKdiff, Next = NextDiff_r
  (le XOR de la règle RÉELLE CF3.r contre la relation Python
  RPy_r == GP_r ∧ FP_r), Inv = DiffInv, longueur 1. Attendu :
  **NoError** pour chacune — les relations sont ÉGALES (garde ET effet,
  contre l'artefact réel ; les effets étant déterministes, l'égalité
  relationnelle entraîne l'égalité des gardes ET des fonctions d'effet).

**Les 26 contrôles négatifs** (un par obligation — la faute de
transcription plausible, CHACUNE devant être ATTRAPÉE, Error 12) :

| # | règle | garde mutée GPw (le défaut simulé) | effet muté FPw (le défaut simulé) |
|---|-------|-----------------------------------|-----------------------------------|
| 1 | VoleKUser | le vol restreint à tort au canonique | le vol prend le MAUVAIS élément (SSerrure) |
| 2 | VoleSSerrure | le vol conditionné au piège (étranger) | le vol SANS EFFET (sait′ = sait) |
| 3 | VoleSPiege | le vol réservé à e > 1 | le vol prend DEUX éléments |
| 4 | FalsifieConteneur | la phase canonique OUBLIÉE (l'écart de couverture v0.15.0 croisé par la PBT) | la destruction DÉBORDE sur le média (P4) |
| 5 | FalsifiePiege | le tag jamais testé (GPw = TRUE) | le piège cassé qui DÉTRUIT |
| 6 | RejoueEpoquePassee | le e > 1 oublié (rejeu à l'époque 1) | LE ROLL-BACK (e′ = e − 1 — la faute P2) |
| 7 | OuvrirCorrect | la branche honnête K_user ∉ sait AMPUTÉE | le secret TOUJOURS appris (la faute P1) |
| 8 | OuvrirPhraseErronee | offerte au brouillon aussi | la phrase erronée qui OUVRE |
| 9 | OuvrirAncienCouple | le e > 1 oublié | l'ancien couple qui OUVRE |
| 10 | Verifier | offerte au brouillon aussi | la vérification qui ACCEPTE (P2) |
| 11 | CrashPendantSession | le crash réservé au brouillon | le crash qui AVALE une époque |
| 12 | CloturerCorrecte | le trap_ok oublié | l'époque qui n'AVANCE PAS (P2) |
| 13 | CloturerPhraseErronee | offerte au canonique | la phrase erronée qui SCELLE (e′ = e+1) |

Runs : 13 × (Init = TypeOK, Inv = OblFaibleGarde_r, longueur 0) et
13 × (Init = InitTypeOKdiffC, Next = NextDiffw_r, Inv = DiffInvC,
longueur 1). Attendu pour CHACUN : **Error 12** (contre-exemple produit).

## 2. LE POINT (b) — LE LEMME O3 PAR SMT NON BORNÉ

**Le module** : CF3O3.tla. La fonction d'abstraction α : l'époque
projetée sur ses classes {1} ∪ {≥2} (0 = hors domaine, e < 1), les neuf
autres composants inchangés. FormDomain : le domaine des formes (les
contraintes de domaine + I1 + I2 + I3, la classe dans {1, 2}).

**Les 2 obligations SMT NON BORNÉES** (les clefs du lemme) :
- **OB1 — LA COUVERTURE** (image ⊆ domaine) : Init = TypeOK ∧ Inv,
  Inv = OblOB1 (FormDomain(α(s))), longueur 0. Attendu : **NoError** —
  pour TOUT état bien typé satisfaisant Inv, l'époque QUELLE QU'ELLE
  SOIT, la classe est dans {1, 2} : l'argument de complétude.
- **OB2 — LA NON-VACUITÉ PAR FORME** (domaine ⊆ image) : Init =
  FormeDomaineEtat (la forme instantiée en état-témoin : la classe lue
  comme époque), Inv = OblOB2 (Inv ∧ Classe = e — le témoin satisfait
  l'invariant et sa forme est lui-même, α∘ι = id), longueur 0. Attendu :
  **NoError**.
- OB1 ∧ OB2 : **l'image de {TypeOK ∧ Inv} par α est EXACTEMENT
  FormDomain** — la bijection des formes.

**CE QUI EST ÉNUMÉRÉ BORNÉ (jamais prétendu prouvé)** : le NOMBRE
|FormDomain| = **288**, énuméré DEUX FOIS par des outils indépendants :
- **tlc_o3_compte** : TLC énumère FormeDomaineEtat (Next == FALSE,
  -deadlock) — attendu **288 états distincts** ;
- le Python **verifie_couverture_288.py** (vague 5) re-exécuté depuis
  le clone frais — attendu **288 formes, la bijection VERT**.
Les époques représentatives {1, 2, 3, 7, 50, 1000} demeurent des
TÉMOINS, plus jamais des preuves.

**Les 2 contrôles négatifs** :
- **CB1** : OB1 SANS I4 (Init = InvSansI4 — l'époque peut être < 1) :
  l'état e = 0, I1-I3 tenus, a sa classe = 0 — HORS domaine. Attendu :
  **Error 12** (I4 est PORTANTE).
- **CB2** : OB2 avec le domaine SANS I1 (Init = FormDomainFaible —
  secret sans seuil) : la forme secret ∧ sait = {} n'a AUCUN témoin
  Inv. Attendu : **Error 12** (I1 est PORTANTE).

## 3. LE POINT (c) — LE LEMME DE TRANSLATION ∀δ

**Le module** : CF3Translation.tla. La copie décalée vit dans des
variables miroir (te = e + delta, composants égaux) ; les règles RÉELLES
s'appliquent à la copie par INSTANCE CF3 (zéro retranscription) ; le
décalage delta est UNCHANGED dans toute transition (un couplage
« réparé » en bougeant δ′ ne prouverait rien).

**Les 2 obligations** (e ≥ 2, δ ≥ 0, TOUS DEUX NON BORNÉS) :
- **LT1 — LES GARDES** : Init = InitLT, Inv = LT1 (les 13 gardes à
  l'origine ⟺ au décalé), longueur 0. Attendu : **NoError**.
- **LT2 — LES EFFETS** : Init = InitLT, Next = NextLTScelle (la règle
  tire SIMULTANÉMENT des deux côtés — les règles réelles), Inv =
  Couplage, longueur 1. Attendu : **NoError** — l'image décalée EST le
  décalé de l'image (σ_δ ∘ FT = FT ∘ σ_δ).
- LT1 ∧ LT2 : un contre-exemple à grande époque aurait, par translation
  inverse, un contre-exemple à petite époque — la complétude de la
  preuve par formes finies aux classes {1} ∪ {≥2} est MÉCANIQUE. Les
  témoins {7, 50, 1000} demeurent, plus jamais la preuve.

**Les 2 contrôles négatifs** :
- **CC1** : LT1 avec l'hypothèse affaiblie e ≥ 1 (Init = InitLTfaible) :
  à e = 1, δ ≥ 1, la garde de rejeu diverge (fausse à l'origine, vraie
  au décalé). Attendu : **Error 12** (LA FRONTIÈRE DE CLASSE {1}/{≥2}
  EST PORTANTE).
- **CC2** : LT2 avec la clôture REMPLACÉE PAR LE PLAFOND v120
  (e ← min(e+1, 3)) des deux côtés (Next = NextLTplafond) : à e = 3,
  δ = 1, les deux saturent à 3, le couplage exige 3 + δ. Attendu :
  **Error 12** (LE PLAFOND N'EST PAS TRANSLATION-UNIFORME — la raison
  historique de son retrait v120 → v0.15.0).

## 4. L'ÉTAPE DE VÉRIFICATION — LA BATTERIE INTÉGRALE

**Phase A — LE CLONE FRAIS** (le rejeu depuis l'état committé) : git
clone NEUF du dépôt au commit du présent plan ; les OUTILS copiés au
clone (empreintes du § 0) ; **les 7 RUNS ORIGINAUX rejoués** depuis le
clone (jouer_tous_les_runs.py du clone) :
- TLC 1 CF3Fidelite : **154 états** attendus EXACTS (les comptes D187) ;
- TLC 2 CF3Plafond : **216** ; TLC 3 CF3Bornes : **360** ;
- APA 1 base (Init⟹Inv), APA 2 inductif (Inv∧Next⟹Inv′) : NoError ;
- APA 3-4 les contrôles C1/C2 : Error 12 (conservés).
**Le verdict attendu : les 11 clefs du verdicts.json consigné
BIT-IDENTIQUES, 8/8 VERT.** Toute divergence : l'atelier ÉCHOUE
(échec fermé — l'écart d'outillage du § 0 serait CONDAMNÉ par là).

**Phase B — LES NOUVELLES OBLIGATIONS** : les 26 + 2 + 2 runs du § 1-3,
NoError attendus, journalisés au logs/ du présent atelier.

**Phase C — LES 30 CONTRÔLES NÉGATIFS** : les 26 + 2 + 2 runs, Error 12
attendus pour CHACUN — la falsifiabilité de chaque obligation neuve.

**Phase D — LE COMPTE 288** : tlc_o3_compte (TLC, 288 attendus) +
verifie_couverture_288.py depuis le clone (288, bijection VERT).

**Phase E — LA CAMPAGNE 10 000 TRACES REJOUÉE** : depuis le clone frais,
`pbt_raffinement_v150.py --debut 0 --fin 10000 --replay` (graine
consignée 20261112) — attendu : **10 000 stables, 0 divergentes, les
10 000 digests BIT-À-BIT identiques au CSV consigné**, le condensé
global des verdicts sha256 **333996d4f8ce281f7aff24fcde54c30c72954d4e
6d1edf0c07e92b682a1c6a1** REPRODUIT. (La frontière de la trace demeure
celle consignée : 660 écarts d'UNE classe — l'écart de couverture
« falsifie_conteneur en session » v0.15.0, réduit, analysé, P1-P4 non
menacées — le présent chantier ne touche NI le modèle Python NI le
coffre : il les REJOUE.)

**Phase F — LE VERDICT ÉTENDU** : verdicts.json (scripts/tla_v150/)
reçoit LES 11 CLEFS CONSIGNÉES INCHANGÉES (bit-identiques) PLUS les
nouvelles clefs : equiv_garde_{r} × 13, equiv_effet_{r} × 13,
controle_garde_{r}_attrape × 13, controle_effet_{r}_attrape × 13,
o3_couverture_smt, o3_non_vacuite_smt, o3_compte_formes_tlc (288),
controle_o3_couverture_attrape, controle_o3_non_vacuite_attrape,
translation_gardes_smt, translation_effets_smt,
controle_translation_gardes_attrape, controle_translation_effets_attrape,
pbt_rejeu_10000_stables (10000), pbt_rejeu_10000_divergentes (0),
pbt_rejeu_condense_identique (true). Le total attendu : 75 clefs, TOUTES
à leurs valeurs attendues.

## 5. LA FRONTIÈRE (l'honnêteté du chantier)

- CE QUI EST PROUVÉ (SMT, entiers non bornés, Apalache 0.63.0/z3) :
  les 26 équivalences par règle (garde et effet), la couverture OB1, la
  non-vacuité OB2, les gardes LT1 et la commutation LT2 — les 30
  obligations, chacune avec son contrôle négatif ATTRAPÉ.
- CE QUI EST ÉNUMÉRÉ BORNÉ (et le dit) : le compte 288 (TLC + Python,
  deux énumérations indépendantes) ; les époques représentatives et les
  translations témoins {7, 50, 1000} (démues de rôle probatoire).
- CE QUI N'EST PAS TOUCHÉ : le modèle Python (modele_invariant_v150.py),
  le coffre (v06/coffre_cf3.py), la spec CF3.tla (copie recoupée md5,
  jamais réécrite), les pièces consignées de la vague 3/5 (rejouées,
  jamais modifiées) ; les 660 écarts de la PBT demeurent l'écart de
  couverture CONSIGNÉ (un chantier futur au commandement du développeur).
- L'ÉCART D'OUTILLAGE (§ 0) : nommé, borné par le recoup fonctionnel de
  la phase A — la batterie originale DOIT reproduire, sinon échec fermé.

## 6. LA CONSIGNATION PRÉVUE

L'Entrée 329 au worklog ; D215 au journal des décisions ; le rapport
RAPPORT-89488hblm.txt au présent atelier ; les logs intégraux au
logs/ ; le verdicts.json étendu ; le push GitHub au commandement du
développeur (ses identifiants, sa machine) ; les livrables à download/ ;
l'archivage de l'instruction 89488hblm au /ARCHIVE du coffre (le rituel
des instructions exécutées, md5 recoupés avant le geste).
