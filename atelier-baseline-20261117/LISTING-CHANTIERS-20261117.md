# LISTING DES CHANTIERS EN COURS — TRIADE (le 17/11/2026, la session de reprise)

> La commande du développeur : « fais moi un listing des chantiers en
> cours, avec un ordre de priorité, puis lance le premier ». L'ordre ci-
> dessous suit le SÉQUENÇAGE PRESCRIT par le projet lui-même (la décision
> D207 scellée le 16/11, la checklist de la vague 6, le guide L6) — pas
> une invention de session.

---

## 1. LA BASELINE DOUBLE-BRAS — PRIORITÉ 1 ✅ CLOS (le 17/11 au soir, la
session suivante — l'épreuve V1-V5 vécue par le harnais né, les deux bras
rejetés, la boucle corrective § 5 vécue : le bras C un tour, le bras T
deux, LE REJEU CONFORME V1-V5 et I5 aux deux bras — le détail aux
Entrées 325-326, le RAPPORT-BOUCLE-CORRECTIVE.txt)

~~PRIORITÉ 1 ✅ LANCÉE (la présente session)~~

**Ce que c'est** : la prochaine unité entièrement instrumentée AUX DEUX
BRAS PAR LA RIG (le n=1 devient n=2) — le geste-gate qui débloque les
leviers d'optimisation. Prescrit par : le guide L6 (« la rig attend son
premier vrai chantier : la baseline »), le journal d'optimisation
(« LA BASELINE PEUT COURIR »), le rapport vague 6 (« le geste de la
prochaine session de chantier »).

**L'état après la session** : CONSTRUITE — loupe-05 rebâtie intégralement
par la rig aux deux bras (23 appels, 67 302 tokens, 100 % log-api,
modèle glm-4-plus) ; le bras T CONFORME (376 octets cristallisés, revue
verte), le bras C propre à gcc (arbitrage I1/I2 nommé) ; le journal né
avec son garde-brut, les empreintes gravées. **Ce qui reste** : l'épreuve
d'exécution (V1-V5 — le harnais ou le terrain), la consignation au
journal canonique, le push (la main du développeur).

## 2. LES LEVIERS D'OPTIMISATION DU COÛT (L1 → L3 → L2 → L4 → L5/L7) — PRIORITÉ 2

**Ce que c'est** : le cœur du chantier d'optimisation (Entrée 317) — un
levier par unité mesurée, jamais deux (D207) ; la règle d'arrêt armée
(un levier qui dégrade M1 ou M3 est REJETÉ). Deux instructions Qwen en
attente en dépendent directement :
- **5gfx6pwkj — le coût « localiser »** : le mode de réponse minimale
  (identifiant de bloc + plage, vérifié par la carte) contre le header
  complet (médiane 604/1 277 ≈ 47 %) — plan pré-enregistré hash-consigné,
  n≥15 par mode, tokenizer natif + cl100k_base, aucun contrôle retiré ;
- **vljfs6pcj — le temps de vérification M4** : invalidation incrémentale
  par empreinte de bloc, mémoïsation scellée des sessions d'émulation,
  pré-filtre différentiel natif (le chemin critique crypto ~10 s/196 Kio),
  n≥5 par configuration, rebuilds byte-identiques.

**Débloqué par** : la baseline (fait) + l'épreuve d'exécution des pièces.

## 3. LE PROGRAMME DE PREUVE CF3 — PRIORITÉ 3 (préparation en parallèle)

**L'instruction 89488hblm** : l'équivalence TLA+↔sémantique déchargée par
SMT sur entiers non bornés (les 13 règles, garde à garde, effet à
effet), le lemme O3 par SMT non borné, le lemme de translation ∀δ
mécanisé, un contrôle négatif par nouvelle obligation, la batterie 8/8
avec verdicts.json bit-identique, les 10 000 traces re-jouées.

**Le prérequis nommé** : l'outillage de model-checking à RE-PROVISIONNER
(Apalache 0.63.0 + tla2tools, aux versions et empreintes consignées au
dépôt — le clone /tmp/triade-gh fut recyclé avec le conteneur). **La part
préparable** : la structure des obligations SMT par règle et le plan des
contrôles négatifs — « le chantier s'ouvre à la commande du développeur ».

## 4. LE TEMPS CONSTANT STRUCTUREL — PRIORITÉ 4 (l'audit statique au labo)

**L'instruction fkkqc7v8t** : l'analyse de flux d'information prouvant
que branchements et adresses ne dépendent pas du secret (système de types
constant-time ou décharge SMT), intégrée au build à côté de l'audit ABI
msx64, pour les SIX cibles scellées (sha-256, hmac, hkdf, x25519,
aes-gcm, md5) ; en parallèle l'investigation du renversement dudect
(N=200 : |t|=12,39/5,19 → N=400 sous le seuil) : warm-up, turbo,
outliers, ordre des classes.

**La frontière** : l'audit statique est un chantier d'OUTIL AU
LABORATOIRE (les six cibles scellées sont à portée) ; les runs dudect
durcis (warm-up contrôlé, affinity, fréquence fixée, ordre randomisé,
plusieurs runs par N) sont des GESTES DU TERRAIN [D99] — le kit se
prépare au labo, la course et la signature appartiennent au développeur.

## 5. LA CAMPAGNE D210 — PRIORITÉ 5 (la dernière de la séquence)

**L'instruction p39uklsca** : n≥6 unités entièrement instrumentées,
formats identiques aux deux bras, ordre randomisé (graine consignée),
le test d'attribution empirique (re-livraison de la pièce C par un kit
standard minimal), la règle D202 et ses exclusions, tokens et temps
humain LUS des journaux, distributions appariées avec intervalles de
confiance, les cinq hypothèses directionnelles re-testées.

**L'état** : le plan D210 est pré-enregistré (hash consigné avant toute
mesure) ; l'exécution exige de NOUVEAUX CYCLES DE CAMPAGNE avec
coordination terrain — c'est la dernière de la séquence prescrite.

---

## Les gestes du développeur en attente (mémoire — pas des chantiers agent)

- **L'archivage vague 5** (dix fichiers, le kit-archivage-vague5 livré,
  échec fermé) ;
- **La consignation D212 + l'Entrée 323** au journal canonique (les
  brouillons livrés avec la vague 6) ;
- **Le push GitHub** (ses identifiants, sa machine) ;
- **Les runs des unités 13/14** (PASSEUR v0.2 : LANCEUR-UNITE-13-T.bat
  puis 14-C.bat, le témoin daté signé [D99]) et **le geste du livre**
  (le guide 313 : les trois retouches prescrites) ;
- **Le PDF final** (attendu à la fermeture des sessions de runs) ;
- **Le DOI Zenodo et le grant d'évaluation** à la licence (les gestes du
  concédant).

## Les accès de la session (état constaté)

- Le jeton OAuth du relais (alexis.fr.lopez@gmail.com) : **EXPIRÉ**
  (invalid_grant — la ré-autorisation interactive prévue par la note du
  fichier est À VIVRE au prochain besoin du compte personnel) ;
- Le compte de service (z-ai-811@physichong.iam.gserviceaccount.com) :
  OPÉRATIONNEL — l'accès au coffre et au miroir Git vécu à la présente
  session par ce chemin ;
- Le CLI z-ai du labo : OPÉRATIONNEL (le modèle glm-4-plus, l'identique
  de la campagne D204).
