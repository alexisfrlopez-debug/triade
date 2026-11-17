# PLAN PRÉ-ENREGISTRÉ — LE COÛT DE L'OPÉRATION LOCALISER (5gfx6pwkj)
## Le mode de réponse minimale contre le mode actuel — OPT-02 du chantier

**L'instruction** (Qwen__20261116_5gfx6pwkj.txt, md5 227a28ccd2b9b2511a23ca67a6538f2d) :
« Optimise le coût tokens de l'opération localiser de la carte TRIADE : la
réponse actuelle ré-émet le header complet (médiane 604 tokens sur 1277,
≈47 % du total). Conçois un mode de réponse minimale (identifiant de bloc +
offset/plage, vérifié par la carte) et mesure-le contre le mode actuel selon
un plan pré-enregistré hash-consigné avant toute mesure : mêmes blocs, même
graine consignée, n≥15 par mode, tokenizer natif du modèle sur chaque appel
instrumenté (journal d'usage), cl100k_base en parallèle, distributions
complètes (médiane, quartiles, min/max). Aucun contrôle ne doit être retiré :
le round-trip, la garde de carte et la vérification d'adresse restent actifs. »

**Le statut au dépôt** : la baseline double-bras est CONSTRUITE puis ÉPROUVÉE
VERTE (les Entrées 324-326) — l'instruction est DÉBLOQUÉE (le séquencement
D207 : « 5gfx6pwkj après la baseline double-bras »).

---

## 1 · LA MESURE AVANT (le périmètre consigné, jamais refait)

La décomposition om3ewy9lf (v0.18.0, preuves_v180/p5-decomposition-contexte.txt)
— l'appel complet instrumenté, tokenizer natif lu du log :

| opération | matériau lu | prose req. | réponse écrite | TOTAL (natif) |
|---|---|---|---|---|
| localiser | 596 | 41 | **604** | **1 277** |

LA CIBLE : la réponse (604 tokens, ≈47 % du total) — l'agent ré-émet
l'entête complet du bloc. Le mode minimal la réduit à
IDENTIFIANT · NOM · PLAGE.

## 2 · LE MATÉRIAU (gelé par empreinte)

Les 18 blocs du domaine loupe (loupe.exe 0.1.1-dev.1, la carte génération 17,
sha256 c1115105…). L'ENTÊTE de chaque bloc = les lignes « ; » initiales de sa
notation (loupe/notation/loupe-*.asm), lues du fichier même — le matériau de
la mesure om3ewy9lf (« BLOC DE LA CARTE (entête lu du fichier même) »).

LA VÉRITÉ-TERRAIN par bloc (lue des entêtes, confrontée à la carte) :

| bloc | identifiant | slot | taille | fin (exclue) |
|---|---|---|---|---|
| loupe-01-ouvrir | i110001 | 0x4080 | 448 | 0x4240 |
| loupe-02-lire | i110002 | 0x4240 | 320 | 0x4380 |
| loupe-03-fermer | i110003 | 0x4380 | 192 | 0x4440 |
| loupe-04-cadre | i110004 | 0x4040 | 64 | 0x4080 |
| loupe-05-sha256 | i110005 | 0x4440 | 384 | 0x45c0 |
| loupe-06-md5 | i110006 | 0x45c0 | 896 | 0x4940 |
| loupe-07-cumul | i110007 | 0x4940 | 128 | 0x49c0 |
| loupe-08-ligne | i110008 | 0x49c0 | 320 | 0x4b00 |
| loupe-09-ecran | i110009 | 0x5c00 | 1152 | 0x6080 |
| loupe-10-peinture | i110010 | 0x4b00 | 1664 | 0x5180 |
| loupe-11-defilement | i110011 | 0x5180 | 640 | 0x5400 |
| loupe-12-aller | i110012 | 0x5400 | 832 | 0x5740 |
| loupe-13-recherche | i110013 | 0x5740 | 192 | 0x5800 |
| loupe-14-suivant | i110014 | 0x5800 | 1024 | 0x5c00 |
| loupe-15-curseur | i110015 | 0x6080 | 448 | 0x6240 |
| loupe-16-saisie | i110016 | 0x6240 | 704 | 0x6500 |
| loupe-17-sauver | i110017 | 0x6500 | 576 | 0x6740 |
| loupe-18-quitter | i110018 | 0x6740 | 192 | 0x6800 |

(Les 18 notations sont scellées au dépôt — leurs sha256 font foi du matériau ;
la table ci-dessus est régénérée par l'outil depuis les fichiers, jamais tapée.)

## 3 · LES DEUX MODES (les gabarits GELÉS — le seul degré de liberté de l'A/B)

### Mode A — LE MODE ACTUEL (la réponse rend l'entête complet)

```
L'OPÉRATION LOCALISER DE LA CARTE TRIADE (le format en vigueur — la réponse
rend l'entête complet du bloc localisé).

BLOC DE LA CARTE (entête lu du fichier même) :
{ENTÊTE}

REQUÊTE : localise le bloc ci-dessus dans la carte et rends SON ENTÊTE
COMPLET (toutes les lignes de l'entête du bloc localisé, le format en
vigueur de l'opération) — rien d'autre.
```

### Mode B — LE MODE MINIMAL (une ligne, la carte vérifie)

```
L'OPÉRATION LOCALISER DE LA CARTE TRIADE (le mode minimal — la réponse tient
en une ligne, la carte confronte la réponse aux octets réels).

BLOC DE LA CARTE (entête lu du fichier même) :
{ENTÊTE}

REQUÊTE : localise le bloc ci-dessus dans la carte et réponds AU FORMAT
MINIMAL, une seule ligne exactement :
IDENTIFIANT · NOM · PLAGE
— IDENTIFIANT : l'identifiant de bloc de la carte (la forme iNNNNNN de
l'entête) ;
— NOM : le nom du bloc tel que l'entête le porte ;
— PLAGE : début–fin du slot en RVA hexadécimal, la fin exclue (la forme
0x…–0x…).
Rien d'autre.
```

LE SEUL ÉCART entre les modes : la prose de requête (la prescription du
format au mode B — le coût de la prescription EST le coût du mode, compté
honnêtement). Le matériau ({ENTÊTE}) est IDENTIQUE aux deux modes, bloc pour
bloc.

## 4 · LE PLAN DE MESURE (pré-enregistré)

- **n = 18 par mode** (≥ 15 exigé) — les MÊMES 18 blocs aux deux modes ;
- **LA GRAINE : 20261117** (consignée ci-devant) — elle fixe l'ORDRE des
  blocs : `random.Random(20261117).shuffle` sur les 18 identifiants triés ;
  le MÊME ordre aux deux modes ;
- **L'ORDRE DES MODES** : les 18 appels du mode A d'abord (le mode actuel),
  puis les 18 appels du mode B — chacun dans l'ordre de la graine ;
- **L'INSTRUMENT** : compter_tokens.py (la rig L6, l'instrument byte-identique
  du kit — sha256 au dépôt) — chaque appel `--bras T --phase analyse --tache
  localiser-{A|B}-{identifiant}` avec `--journal` et `--garde-brut` vers
  l'atelier : LE TOKENIZER NATIF LU DU CHAMP USAGE (jamais estimé) ;
- **cl100k_base EN PARALLÈLE** : le prompt exact (conservé au geste —
  garde-prompts/) et la réponse (lue de la garde brute) re-tokenisés offline
  par tiktoken ;
- **AUCUN APPEL HORS INSTRUMENT** (CA3) — un appel manqué est un écart nommé,
  jamais reconstitué ;
- **LES DISTRIBUTIONS** : n, médiane, q1, q3, min, max — par mode, pour
  prompt/completion/total (natif) et total cl100k.

## 5 · LES CONTRÔLES (AUCUN RETIRÉ — la contrainte de l'instruction)

1. **LA VÉRIFICATION D'ADRESSE** (chaque réponse, les deux modes) : la plage
   nommée doit être EXACTEMENT [slot, fin) de la vérité-terrain — le slot
   relu de l'entête, la fin = slot + taille ;
2. **LA CONFRONTATION À LA CARTE** (chaque réponse) : l'identifiant et le nom
   doivent être ceux du bloc soumis — la table des 18 (régénérée des entêtes) ;
3. **LA CONFRONTATION AUX OCTETS RÉELS** (chaque bloc, une fois) : loupe.exe
   lu au slot — le padding terminal [slot+code, slot+taille) doit être TOUT
   0x90 (la convention NOP du build) et le code [slot, slot+code) sans 0xCC —
   la plage pointe les octets réels du bloc ;
4. **LA GARDE DE CARTE** (avant ET après la campagne) : le build loupe
   `--verifier` vécu au labo jusqu'à la frontière de la cérémonie (D87 — la
   clé jamais traversée) : le garde sceau-I 14/14, l'assemblage 18/18
   round-trip R5, l'oracle structurel 43 verrous, l'audit msx64 78 appels,
   la double preuve R7, la recomposition PE byte-identique à loupe.exe ;
5. **LES EMPREINTES SCELLÉES** (avant ET après) : sha256 de loupe.exe
   (c1115105…), carte.sig, frag-{loc,con,prf,bld}.bin, les 18 notations —
   INCHANGÉES par la campagne (elle ne touche RIEN : lecture seule).

## 6 · LES RÈGLES DE VERDICT (pré-enregistrées, falsifiables)

- **ZÉRO DIVERGENCE exigé** : chaque réponse (les deux modes) doit localiser
  LE BLOC SOUMIS — identifiant, nom et plage exacts. Une réponse non
  parsable au mode B est une DIVERGENCE (fail-closed : invérifiable = faux) ;
- **LE GAIN** : 1 − médiane(total B) / médiane(total A), lu des logs bruts
  par le script d'extraction — JAMAIS tapé à la main ;
- **L'ATTENTE DIRECTIONNELLE** (falsifiable) : le mode B réduit le total
  (la réponse 604 → ~25 tokens ; l'attente : −40 à −50 % du total) — SI la
  mesure la falsifie (gain nul, négatif, ou divergences), LE RÉSULTAT EST
  CONSIGNÉ TEL QUEL (l'instruction l'exige : « y compris s'il falsifie
  l'attente de gain ») ;
- **LA RÈGLE D'ARRÊT D207** (armée) : le mode B ne touche NI le round-trip,
  NI la garde, NI la vérification d'adresse — tout contrôle retiré serait un
  REJET ; le M3 (temps humain) est invérifiable au labo pour ce geste (une
  ligne à confronter contre ~15 lignes à relire — la lecture honnête le
  nommera).

## 7 · LA CONSIGNATION

- **D211** (docs/DECISIONS.md) : LE PRÉSENT PLAN, empreinte sha256 consignée
  AVANT TOUTE MESURE (la règle D204/D210 reconduite) ;
- **OPT-02** (JOURNAL-OPTIMISATION-TOKENS.txt, le canon) : la mesure après,
  le format D205 (la mesure avant, le gain mesuré, le vérificateur) —
  l'OPT-01 DEMEURE RÉSERVÉ au levier L1 de la prochaine unité (les Entrées
  324/326) ; l'inversion chronologique (OPT-02 mesuré avant l'unité L1) est
  NOMMÉE : la campagne localiser n'est pas une unité de construction, la
  règle « un levier par unité » demeure intacte ;
- **L'atelier** : journal_tokens.jsonl, garde-brut.jsonl, garde-prompts/,
  verites-terrain.json, le rapport RAPPORT-5gfx6pwkj.txt, les scripts
  (mesure_localiser.py, extraire_gain.py) — tout au dépôt (D208 : les pièces
  de preuve vivent au dépôt).

## 8 · LA FRONTIÈRE

- La campagne est UNE MESURE AU LABORATOIRE — lecture seule sur le domaine
  loupe, AUCUN octet écrit, AUCUNE carte re-signée, AUCUNE cérémonie ;
- L'ADOPTION du mode minimal comme format de l'opération localiser (si le
  vert est mesuré) est une DÉCISION À PART (D212, au verdict) — le protocole
  de la carte ne bouge pas sur une seule mesure ;
- Le M3 (temps humain) appartient au geste du développeur — nommé, jamais
  simulé.
