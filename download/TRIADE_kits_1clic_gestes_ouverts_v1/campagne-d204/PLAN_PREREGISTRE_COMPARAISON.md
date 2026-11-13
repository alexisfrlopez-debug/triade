# PLAN PRÉ-ENREGISTRÉ — LA COMPARAISON DES WORKFLOWS (paquet 5 de la vague 3)

**Statut : PRÉ-ENREGISTREMENT — consigné AVANT TOUTE MESURE (l'instruction
54wni4hzh : « rédige et verrouille (empreinte sha256 consignée AVANT toute
mesure) un plan de comparaison pré-enregistré »). L'empreinte sha256 du
présent fichier est consignée à la décision D204 ; le dossier des résultats
(scripts/preuves_v150/comparaison_resultats/) sera CRÉÉ PAR LA PREMIÈRE
MESURE, jamais avant — toute modification du présent plan après le début
des mesures serait une fraude attrapable (la confrontation des empreintes,
CA5). Le présent plan ne contient AUCUN chiffre de résultat : les hypothèses
sont directionnelles, les seuils sont des SEUILS, et les seuls nombres
présents sont structurels (les tailles, les dates, les identifiants).**

## 1. L'OBJET

Les blocs D193/D195 (le bras de référence compilateur, v0.14.0) ont comparé
la QUALITÉ du code produit par les deux voies (instructions, tailles,
mutation — mêmes contrats, mêmes shims). Le présent plan compare les
WORKFLOWS eux-mêmes, de bout en bout : ce que coûte et ce que protège chaque
voie de développement quand LE MÊME AGENT exécute LA MÊME FAMILLE DE TÂCHES
sous les DEUX disciplines, livrée par LE MÊME MÉCANISME DE KIT TERRAIN.
La question n'est pas « quel code est meilleur » (répondue par D193/D195)
mais « que coûte, en défauts échappés, en tokens, en temps humain et en
temps de calcul, la gouvernance à intention signée — et que rapporte-t-elle
en retour ».

## 2. LES DEUX BRAS (les workflows, définis avant tout)

**LE BRAS T (TRIADE, la notation scellée)** — la discipline complète du
protocole, R1–R11 : la spécification de couche I lue et tenue
(écrite-avant-code, R2 — les contrats EXISTANTS du domaine loupe servent la
partie contrôlée, les nouveaux contrats de la commande réelle servent la
partie réaliste) ; la notation à la main par l'agent ; le round-trip à
chaque build (R5) ; la carte (re)générée ; les oracles régénérés depuis I ;
la cristallisation (les dix rebuilds consécutifs identiques, R6) ; le garde
des arbres signés AVANT tout geste ; la livraison par le kit terrain (la
pièce dev + le scénario + les témoins, le modèle de la campagne Loupe) ;
le run terrain appartient au développeur ; le recoup sur pièces au retour.
La cérémonie de scellement (la clé hors-ligne) est le geste du développeur :
si elle a lieu, elle est chronométrée au carnet ; sinon, son absence est un
écart nommé, jamais un chiffre fabriqué.

**LE BRAS C (standard, C + gcc)** — le flux conventionnel : le MÊME contrat
de couche I lu comme cahier des charges ; le source C écrit par le MÊME
agent ; la compilation gcc -O2 (l'outil de la livraison, la commande
consignée) ; les tests écrits par l'agent comme il le ferait dans le flux
courant (aucune exigence de couverture imposée par le plan — le flux
standard est mesuré TEL QU'IL SE PRATIQUE, sinon la comparaison triche) ;
la livraison par LE MÊME MÉCANISME de kit terrain (le binaire compilé + le
même scénario adapté au chargement du PE compilé + les mêmes témoins) ; le
run terrain au développeur ; le recoup au retour.

**LES DEUX CONSTANTES** : le même agent (la famille GLM de Z.ai, « le
laboratoire », dirigé par le même développeur) et le même mécanisme de kit
terrain (le scénario, les témoins, la règle de recoup — le modèle de la
campagne Loupe inchangé). Tout écart à ces constantes est NOMMÉ au rapport.

## 3. LES TÂCHES (l'échantillon, pré-enregistré)

**La partie contrôlée — les six blocs du bras C** (les cinq familles de
Loupe, les MÊMES contrats I que D193/D195) : loupe-01 ouvrir, loupe-02
lire, loupe-05 sha256, loupe-08 ligne, loupe-13 recherche, loupe-16 saisie.
Chaque bloc est exécuté aux DEUX bras (douze exécutions de workflow,
appariées par contrat). Les pièces scellées du projet NE SONT PAS TOUCHÉES :
la campagne vit sur des artefacts dev de laboratoire, la carte réelle et
les arbres signés demeurent — le bras T de la campagne construit, vérifie
et cristallise sa propre pièce dev, le garde passe AVANT chaque geste.

**La partie réaliste — une application complète de type Loupe** : une
commande APPLICATIVE RÉELLE du développeur (le précédent de l'axe R2/D189 :
jamais un exercice démonstratif), exécutée aux DEUX bras. Tant qu'aucune
commande réelle n'est arrivée, cette partie demeure EN ATTENTE — un statut,
jamais un résultat fabriqué. Si la commande n'arrive jamais, la campagne
rend ses conclusions sur la partie contrôlée seule, l'absence NOMMÉE.

## 4. LES MÉTRIQUES (quatre, la commande)

**M1 — DÉFAUTS ÉCHAPPÉS PAR LIVRAISON** (la règle D202, par côté) : une
LIVRAISON est un run terrain d'un kit (le run, pas le défaut) ; la métrique
PRIMAIRE compte les livraisons où un défaut du CODE ÉCRIT PAR L'AGENT SEUL
échappa aux contrôles (côté pièce : la notation au bras T, le source et le
binaire au bras C) ; la métrique de LIVRAISON compte les livraisons où un
défaut QUELCONQUE échappa (l'ensemble kit+pièce). Un défaut est nommé
(classe, mécanisme, pièce à l'appui) AVANT toute correction — la discipline
du protocole vaut aux DEUX bras. Les exclusions de la règle § 2.3 du
manuscrit s'appliquent : nommé au laboratoire avant tout run (jamais
échappé), résidu sans porte, défaut de l'infrastructure du coffre (d'aucun
côté livré) — chaque exclusion consignée avec sa raison.

**M2 — TOKENS RÉELS, LUS DES LOGS D'USAGE API** : chaque appel au modèle de
la campagne passe par l'instrument compter_tokens.py, qui LIT le champ
`usage` de la réponse de l'API (prompt/completion/total) et journalise une
ligne par appel (bras, phase, tâche, horodatage). L'estimation ×1,08 (le
rapport génération/contenu des retouches de l'ère Loupe) est INTERDITE
quand un log existe : elle ne peut s'appliquer qu'à des appels documentés
MANQUANTS, chaque manque NOMMÉ au rapport. Les phases de comptage :
spec, notation, source-c, tests-c, oracle, build, correctif, ceremonie,
revue, analyse.

**M3 — TEMPS HUMAIN DE CÉRÉMONIE/REVUE** : le carnet du développeur
(carnet_temps_humain.csv, rempli AU GESTE — jamais reconstruit de mémoire,
arrondi à la minute). Les gestes chronométrés : les cérémonies (bras T :
cristallisation, garde, scellement si le geste a lieu ; bras C : le
tag/backup équivalent) et les revues (lire le livrable, arbitrer un défaut
nommé — aux deux bras). Le carnet est une PIÈCE : il retourne au coffre
avec les témoins.

**M4 — TEMPS DE CALCUL DE VÉRIFICATION** : le temps mural des commandes de
vérification, mesuré par chronometre_verification.py (horloge monotone,
journal JSONL). Les listes de commandes sont FIXÉES : bras T — le garde des
arbres signés, le round-trip de la notation livrée, l'oracle du bloc au
périmètre livré, le build ; bras C — la compilation gcc -O2, la suite de
tests du camp C, les contrôles binaires. Toute commande hors liste est un
écart nommé. Le débit d'émulation n'est PAS la métrique (la convention
v0.13.0 vaut) : c'est le coût de VÉRIFICATION qui se mesure.

## 5. LES HYPOTHÈSES (pré-enregistrées, directionnelles, falsifiables)

- **H1 (santé finale)** : les deux bras atteignent le vert terrain recoupé
  sur la partie contrôlée dans la limite d'itérations du § 7 — sinon
  l'écart est rapporté tel quel (l'hypothèse peut être INVALIDÉE ; aucune
  n'est protégée).
- **H2 (défauts échappés)** : sur la partie contrôlée, le taux par
  livraison (métrique PRIMAIRE, côté pièce) ne diffère pas de plus d'un
  facteur deux entre les bras — direction ouverte : la notation pourrait
  échapper davantage (les classes environnement de RQ3 : chargeur, ABI,
  conventions système) ou moins (les contrats écrits d'abord, les oracles
  régénérés). L'hypothèse est testée par les comptes nommés, pas par une
  impression.
- **H3 (tokens)** : le bras T consomme davantage de tokens par changement
  validé que le bras C (la lecture défavorable consignée à D195 : les
  notations plus longues, les contrats plus denses) — testée par les
  totaux loggés, phase par phase.
- **H4 (temps humain)** : le bras T demande davantage de temps humain de
  cérémonie que le bras C (la cristallisation, le garde) ; le temps de
  REVUE peut aller aux deux sens (le livrable T est plus court à lire —
  le WYSIWYG — mais la carte ajoute une couche). Les deux sens rapportés.
- **H5 (temps de calcul)** : le temps de vérification du bras T par
  livraison reste dans le même ordre de grandeur que celui du bras C
  (facteur au plus dix, le seuil pré-enregistré) — le round-trip et les
  oracles contre la compilation et les tests.

## 6. LES CRITÈRES D'ACCEPTATION (binaires, pré-enregistrés)

- **CA1 (le verrou)** : l'empreinte sha256 du présent plan est consignée à
  D204 AVANT tout fichier de résultats ; le dossier
  preuves_v150/comparaison_resultats/ naît de la première mesure
  (l'instrument le consigne à sa création) ; le plan n'est plus modifié
  après (la confrontation des empreintes à chaque jalon).
- **CA2 (les constantes)** : même agent, mêmes contrats de départ, même
  mécanisme de kit terrain — tout écart NOMMÉ au rapport.
- **CA3 (les tokens 100 % loggés)** : chaque appel au modèle passe par
  l'instrument ; les comptes sont LUS du log ; le ×1,08 n'apparaît que
  pour des appels manquants NOMMÉS — sinon le compte est invalide.
- **CA4 (la règle de comptage)** : M1 par la règle D202 (les deux
  métriques, les exclusions nommées, la pièce à l'appui de chaque défaut).
- **CA5 (tels quels)** : les résultats sont rapportés TELS QUELS,
  favorables ou non — la consigne explicite de la commande v0.14.0 (CA3 de
  D193) demeure la règle de la maison.
- **CA6 (la frontière terrain)** : AUCUNE mesure terrain par le
  laboratoire — les runs appartiennent au développeur, le laboratoire
  prépare, recoupe et consigne ; aucun chiffre n'est fabriqué.
- **CA7 (l'aveugle partiel)** : aucune agrégation intermédiaire orientant
  la suite — les agrégats ne se calculent qu'aux deux bras complets de
  chaque unité ; le journal brut demeure la seule vue courante.

## 7. LA TAILLE D'ÉCHANTILLON ET LA RÈGLE D'ARRÊT (avant toute exécution)

**La taille** : la partie contrôlée — six blocs × deux bras, appariés (les
mêmes contrats) ; la partie réaliste — une application × deux bras. Chaque
unité (bloc ou application, par bras) est livrée en itérations de run
terrain : **au plus TROIS livraisons par bloc** (le vert arrive tôt ou
l'écart est nommé — la cap pré-enregistrée) et **au plus DOUZE livraisons
par application** (le précédent de la campagne Loupe), l'arrêt au premier
vert recoupé. Une unité à la cap sans vert est CENSURÉE — rapportée comme
telle, jamais prolongée, jamais exclue.

**La règle d'arrêt globale** : (a) le garde des arbres signés rougit —
TOUT s'arrête (aucune mesure ne vaut une pièce scellée) ; (b) une pièce
livrée compromise — le bras concerné s'arrête, l'écart consigné ; (c)
l'arbitrage du développeur à tout moment, nommé au journal ; (d) la cap
d'itérations — l'unité est censurée. L'analyse (les agrégats, les tests
d'hypothèses) ne se fait qu'aux deux bras complets de la partie contrôlée
— jamais en cours de route (CA7).

**La réserve, écrite d'avance** : les livraisons sont SÉQUENTIELLES, d'un
seul binôme développeur–agent — les résultats sont DEScriptifs, JAMAIS
inférentiels (la réserve de non-indépendance du manuscrit vaut ici
intégralement). L'échantillon est petit et apparié : les écarts observés
seront rapportés avec leurs intervalles exacts quand un dénominateur le
permet, et nommés « descriptifs » sinon.

## 8. CE QUI N'EST PAS MESURÉ ICI (les frontières)

- La qualité du code produit (instructions, tailles, mutation — le bras
  D193/D195 l'a mesurée ; le présent plan mesure le WORKFLOW).
- La supériorité générale du protocole en productivité ou correction :
  N=1 développeur, 1 famille d'agent, 6+1 tâches — la comparaison est un
  ÉCHANTILLON, pas une loi (la leçon de Threats, la limite assumée).
- Le coût monétaire (les tokens suffisent) et le temps d'horloge d'émulation
  (la convention v0.13.0).
- Toute mesure terrain par le laboratoire (CA6).

## 9. LES PIÈCES DU KIT (livrées avec le présent plan)

- `compter_tokens.py` — l'instrument M2 (l'appel instrumenté, le journal
  JSONL, le récapitulatif par phase) ;
- `chronometre_verification.py` — l'instrument M4 (le temps mural, la
  calibration au dry-run, le journal JSONL) ;
- `carnet_temps_humain.csv` — le gabarit M3 (les règles au commentaire) ;
- `livraisons.csv` et `defauts.csv` — les gabarits M1 (la règle D202 au
  commentaire) ;
- `LISEZMOI-comparaison.txt` — le mode d'emploi de la campagne ;
- `verifier_comparaison_v150.py` — le vérificateur du paquet : le verrou
  (l'empreinte consignée AVANT tout fichier de résultats), l'audit du plan
  (AUCUN chiffre de résultat), la preuve du dry-run (les compteurs à
  l'unité près).

## 10. LA CONSIGNATION

Le présent plan est consigné (sha256 à D204) AVANT tout fichier de
résultats ; le dry-run d'instrumentation (la preuve des compteurs, PAS une
mesure de campagne) vit à preuves_v150/comparaison_dryrun/ ; les résultats
de la campagne vivront à preuves_v150/comparaison_resultats/ (le dossier
naîtra de la première mesure) ; l'analyse entrera au manuscrit par le
générateur, jamais tapée à la main. Les runs terrain appartiennent au
développeur ; le laboratoire ne fabriquera JAMAIS un résultat.
