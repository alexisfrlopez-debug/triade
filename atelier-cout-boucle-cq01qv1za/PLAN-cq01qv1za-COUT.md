# PLAN PRÉ-ENREGISTRÉ — LE COÛT DE LA BOUCLE SOUS R11 (cq01qv1za)

> L'instruction (Qwen__20261118_cq01qv1za, lue INTÉGRALEMENT avant tout
> geste) : « Optimise le coût de la boucle sans retirer aucun contrôle,
> sous R11 (hot path identifié par profilage, avant/après consigné au
> journal OPT-NN, contrat stable R4, artefacts scellés intacts). (1)
> Protocole de réponse "pointeur seul" pour l'opération localiser :
> l'agent retourne ID d'entrée + hash au lieu de réémettre l'en-tête
> complet ; expansion côté client ; mesure avant/après sur n≥18 appels
> réels au tokenizer natif (cl100k en parallèle), re-tokenisation
> indépendante ±1 token. (2) Mémoïsation déterministe des ouvertures de
> session émulées (clé = sha256 fichier + config émulateur + graine),
> avec re-exécution d'audit périodique (1 run sur 10) et preuve
> d'identité des consoles ligne à ligne ; le déterminisme est déjà
> prouvé par cristallisation, le caching doit rester vérifiable. (3)
> Double moteur d'émulation : QEMU-user pour le volume, Unicorn pour
> l'échantillon d'audit consigné ; divergence=0 exigée sur l'échantillon,
> tout écart nommé et bloquant. (4) Réconcilie le mémo D214 sur pièces
> (39,5 s vs 39,3/39,2 s de la campagne) : re-mesure avant/après sur la
> même machine, chronomètre monotone, listes fixes ; si le ratio après
> adoption passe sous ×10, énonce explicitement que H5 devient tenue et
> mets à jour la table des statuts. Aucun compromis de couverture :
> aucune graine supprimée, aucun vecteur réduit, aucune vérification
> retirée ; le pool partagé inter-outils reste refusé (le juge ne
> partage pas l'état du jugé). »

CE PLAN EST GELÉ AVANT TOUTE MESURE — son empreinte sha256 sera
consignée au journal des décisions (D222) et au journal d'optimisation
(OPT-04) AVANT la première exécution de mesure ; le commit git de ce
fichier précède toute donnée de mesure au dépôt.

LA MACHINE DE RECORD : ce bac, 2 cœurs, 4 Go (la classe même de la
campagne D204 et de l'atelier vljfs6pcj) — la machine fait partie du
record, nommée ici avant tout geste. L'outillage re-provisionné aux
versions exactes du précédent : qemu-user 1:10.0.13+ds-0+deb13u1
(extrait du .deb sans root), la chaîne TRIXIE gcc-mingw-w64-x86-64
14.2.0-19+27+b1 / binutils-mingw-w64-x86-64 2.44-3+12+b1 / mingw-w64
12.0.0-5 (extraite des .deb sans root au chemin /tmp/mingw-try/root),
unicorn 2.1.4, capstone 5.0.7, keystone, tiktoken, pefile, pynacl.

---

## 1 · AXE (1) — LE POINTEUR SEUL POUR L'OPÉRATION LOCALISER

### 1.1 Le protocole (gelé)

LA MESURE AVANT = le mode A (le format en vigueur : la réponse rend
l'entête complet — le gabarit A de la campagne 5gfx6pwkj, TEL QUEL).
LE MODE P (le pointeur seul) :

- LE MATÉRIAU : l'entête du bloc (lu du fichier même, comme au mode A)
  PLUS la ligne d'empreinte que la carte porte pour l'entrée —
  « Empreinte notation : sha256:<64 hexadécimaux> » — régénérée du
  fichier même (le sha256 du fichier de notation), jamais tapée à la
  main. L'empreinte est un champ LITTÉRAL du matériau (la leçon B1 :
  le champ calculé est le champ faussé — ici RIEN n'est calculé).
- LA RÉPONSE : une seule ligne exactement —
  « IDENTIFIANT · sha256:<64 hexadécimaux> »
  (l'identifiant de la forme iNNNNNN, l'empreinte recopiée telle
  quelle). Rien d'autre.
- L'EXPANSION CÔTÉ CLIENT (le pointeur ne porte plus le contenu — le
  client le reconstruit) : expansion_pointeur.py prend la ligne-pointeur,
  1. cherche l'IDENTIFIANT dans la table de la carte (la table des 18,
    régénérée des fichiers mêmes) ;
  2. confronte l'empreinte rendue à l'empreinte de la carte OCTET POUR
    OCTET — toute divergence = REFUS nommé EMPREINTE-DIVERGENTE (le
    pointeur périmé : l'entrée a changé de version, R8 en esprit) ;
  3. expande le pointeur en l'ENTÊTE COMPLET de l'entrée (la lecture
    mécanique du fichier — le client, pas le modèle) ;
  4. confronte l'entête expansé à l'entête vrai du bloc SOUMIS (le
    matériau de la requête) — OCTET POUR OCTET : le pointeur doit
    désigner LE bloc demandé, toute divergence = REFUS nommé
    EXPANSION-DIVERGENTE.
  Fail-closed partout : POINTEUR-INCONNU, EMPREINTE-DIVERGENTE,
  EXPANSION-DIVERGENTE, HORS-FORMAT — quatre refus nommés.

### 1.2 La mesure (gelée)

Les MÊMES 18 blocs du domaine loupe, la MÊME graine 20261117, le MÊME
ordre (verites-terrain.json de 5gfx6pwkj, relu tel quel), le MÊME
instrument (la rig compter_tokens.py — le natif LU du champ usage,
100 % log-api), DEUX passes sur CE bac :

- passe A (l'avant) : 18 appels au gabarit A TEL QUEL ;
- passe P (l'après) : 18 appels au gabarit P.

Chaque prompt exact conservé (garde-prompts/), chaque réponse brute
conservée (garde-brut.jsonl). L'espacement 429 : 30 s tous les 4
appels, 75 s à la reprise (la leçon de 5gfx6pwkj).

LE CL100K EN PARALLÈLE : chaque prompt et chaque réponse comptés par
tiktoken cl100k_base en parallèle du natif (le rapport de cohérence
consigné, jamais confondu avec le natif).

LA RE-TOKENISATION INDÉPENDANTE ±1 TOKEN (l'instrument contrôlé) :
chaque prompt et chaque réponse RE-comptés par une seconde passe
indépendante (un deuxième objet d'encodage, constitu à part, comptant
le texte par segments concatenés) — l'écart exigé ≤ 1 token par texte
(l'instrument ne doit pas se contredire ; le natif reste la mesure
première, le cl100k le témoin parallèle, la re-tokenisation la preuve
que le témoin est stable).

### 1.3 La vérification (gelée)

Zéro divergence exigé au mode P : les 18 pointeurs exacts (l'ID et
l'empreinte OCTET POUR OCTET), l'expansion client verte 18/18 (l'entête
reconstruit == l'entête soumis), la confrontation aux octets réels
(loupe.exe lu au slot, le padding NOP uniforme, aucun int3
instruction — capstone) reprise TELLE QUELLE de 5gfx6pwkj. LA
FALSIFICATION DU POINTEUR : un octet de l'empreinte muté →
EMPREINTE-DIVERGENTE attrapé ; un identifiant inconnu →
POINTEUR-INCONNU attrapé ; une réponse hors format → HORS-FORMAT
attrapé — les trois contrôles négatifs vécus, consignés.

---

## 2 · AXE (2) — LA MÉMOÏSATION DÉTERMINISTE V2 DES OUVERTURES

### 2.1 La clé (gelée — l'instruction : « sha256 fichier + config
émulateur + graine »)

cle_v2 = sha256( sha256(octets_assemblés_du_bloc)
              ‖ sha256(contenu_de_l'entrée)
              ‖ sha256(octets_du_contrat)
              ‖ sha256(config_émulateur_sérialisée)
              ‖ graine
              ‖ identifiant_oracle )

LA CLÉ V1 DEMEURE ENTIÈRE (bloc, entrée, contrat, oracle — tout ce qui
détermine le résultat d'une session pure) et l'instruction AJOUTE les
deux termes qui déterminent l'ENVIRONNEMENT de la mesure : la CONFIG
ÉMULATEUR (sérialisation canonique JSON : le moteur [unicorn|qemu], les
déclarations du système de fichiers virtuel, les adresses du plan, les
héritages scellés et leurs empreintes, l'état des échecs armés) et la
GRAINE de la campagne. La clé v2 est un SUR-ENSEMBLE de la v1 : un
octet changé d'UN SEUL terme = absence = la session vit
(l'invalidation par construction, reconduite). Les entrées v1
(memo-sessions-v1.json, racine signée) NE SONT PAS migrées : le mémo
v2 naît vide, semé par ses propres exécutions — l'ancien demeure,
nommé PÉRIMÉ POUR LE V2 (jamais détruit, D143).

### 2.2 Le format (gelé)

memo-sessions-v2.json : l'en-tête v1 (format TRIADE-MEMO-V2, la
constante publique, la clé publique Ed25519 de test, la racine, la
signature) PLUS les deux champs nouveaux : config_hash (le sha256 de
la config de référence au semis) et graine. La chaîne de hachage et la
signature Ed25519 : LA MÊME DISCIPLINE QUE V1 (chaque entrée porte son
h, chaînée depuis la genèse TRIADE-MEMO-V2, racine signée, TOUT
recalculé à chaque chargement, tout écart = REFUS nommé, fail-closed).

### 2.3 L'AUDIT 1 RUN SUR 10 (gelé)

LE RUN EST L'UNITÉ : une exécution d'oracle = un run. Un COMPTEUR DE
RUNS persisté au mémo v2 (champ compteurs, chaîné comme une entrée à
part entière — incrémenté par le single-writer au scellement). À CHAQUE
10ᵉ RUN (compteur % 10 == 0) : L'AUDIT VIT — l'oracle courre avec
--audit-live : les sessions mémoirisables sont RE-EXÉCUTÉES VIVANTES
(le mémo consulté pour rien d'autre que la comparaison), et LA PREUVE
D'IDENTITÉ est exigée : le relevé vivant confronté au relevé mémoisé
CHAMP À CHAMP (rax, état propre, cadre 960 o, panneau 48 o, pos), ET
la console de l'audit comparée à la console de référence LIGNE À
LIGNE (le diff vide exigé — la même preuve que l'étape de vérification
exige des oracles contre les originaux). TOUT écart = BLOQUANT, nommé,
consigné (l'audit ne pardonne pas).

### 2.4 Les falsifications (gelées)

L'entrée de cache mutée (un octet du cadre relevé) → CHAÎNE-ROMPUE au
chargement (attrapé) ; la clé mutée → l'absence = la session vivante
(le repli, jamais l'échec muet) ; le compteur d'audit muté →
CHAÎNE-ROMPUE (le compteur est chaîné). Les TROIS vécus, consignés.

---

## 3 · AXE (3) — LE DOUBLE MOTEUR D'ÉMULATION

### 3.1 Le moteur de volume : QEMU-user (gelé)

LE LANCEUR (lanceur_qemu.c, compilé gcc -static) : un ELF64 STATIQUE
qui, sur CETTE machine, exécute les blocs scellés du domaine loupe à
leur plan d'adressage — le MÊME bytecode, le MÊME ABI msx64, une
AUTRE mécanique :

- LES ZONES du plan posées à leurs adresses (mmap fixe) : le slot du
  bloc, le cadre 960 o, le panneau 48 o, le journal, les zones
  d'empreintes — les adresses LUES de layout.py (le plan même),
  jamais retapées ;
- LE BLOC : les octets ASSEMBLÉS de la notation (assemblés par la
  chaîne keystone du dépôt — la même que l'oracle), chargés depuis un
  fichier au slot — le lanceur ne connaît AUCUN bloc, il exécute ;
- L'IAT : les SIX feuilles kernel32 du noyau loupe (CreateFileW,
  GetFileSizeEx, SetFilePointerEx, ReadFile, CloseHandle,
  GetLastError) en SHIMS ms_abi (__attribute__((ms_abi)) — gcc) sur un
  système de fichiers VIRTUEL EN MÉMOIRE (les témoins passés au
  lanceur comme fichiers) — la même liste fermée que le harnais noyau,
  les mêmes sémantiques (le journal des gle, le Nième ReadFile en
  échec armable) ;
- LE PROGRAMME D'OPÉRATIONS : le lanceur lit une liste d'opérations
  (ouvrir <chemin> / lire <décalage> / fermer / armer_echec <n>) et
  imprime UNE LIGNE JSON PAR OPÉRATION (op, rax, remplissage, vue,
  curseur, le tampon ≤ 384 o en hex, l'état des canaris et des
  non-volatils, le gle) — le relevé que le juge Python confronte au
  modèle indépendant (hashlib — LE JUGE DEMEURE PYTHON, le moteur
  n'est jamais le juge) ;
- L'EXÉCUTION : qemu-x86_64 (10.0.13) — le volume.

### 3.2 Le moteur de référence : Unicorn (gelé)

Le harnais noyau du dépôt (loupe/harnais_noyau.py) — l'outil qui fit
la campagne D204 et l'atelier vljfs6pcj, TEL QUEL (D185) : il demeure
LE MOTEUR DE L'ÉCHANTILLON D'AUDIT et le juge des contrôles séquentiels
bon marché (V3/V4/V5 — les échecs armés et la falsification demandée).

### 3.3 L'échantillon d'audit consigné (gelé)

LA LISTE CONSIGNÉE : les ouvertures des QUATRE fichiers du
différentiel V1 (temoin-1.bin, temoin-384.bin, temoin-3f.bin,
proxy.exe — le scellé M9 comme témoin) ET les lectures à la graine
20261114 de la campagne (les mêmes décalages_valides que l'oracle-02,
le même rng, le même ordre) — la liste EXACTE des opérations consignée
à echantillon-ops.json AVANT la première exécution, sha256 consigné.

LA DIVERGENCE=0 : l'échantillon exécuté AUX DEUX MOTEURS — Unicorn
(la référence) et QEMU (le lanceur) — LES FLUX DE RÉSULTATS comparés
OCTET POUR OCTET (chaque ligne JSON confrontée à la ligne de relevé
Unicorn équivalente, la sérialisation unifiée par le traducteur
Python). TOUT écart = nommé, BLOQUANT, consigné — il n'y a PAS de
divergence tolérée.

LE CONTRÔLE NÉGATIF DU MOTEUR DIVERGENT : un lanceur à shim MUTÉ (la
sémantique de ReadFile délibérément altérée d'un octet — la fausse
valeur du tampon) doit être ATTRAPÉ par la comparaison (le refus nommé
MOTEUR-DIVERGENT) — la preuve que la porte divise les moteurs honnêtes
des moteurs faux.

---

## 4 · AXE (4) — LA RÉCONCILIATION DU MÉMO D214 ET LE RATIO H5

### 4.1 La réconciliation sur pièces (gelée)

L'ÉCART À RÉCONCILIER : le mémo D214 (l'atelier vljfs6pcj) porta
AVANT 39,5 s MÉDIANE [39,1–39,7] n=5 ; la campagne vague 5 (mof9q10vq)
porta 39,3 / 39,2 s n=2. LA RÉCONCILIATION VÉCUE SUR CETTE MACHINE :
la liste fixe du bras T re-mesurée AVANT (les outils v180 TELS QUELS,
n=5, chronomètre monotone) — la distribution de CE bac confrontée aux
deux distributions consignées ; la cause de l'écart NOMMÉE sur pièces
(des bacS DIFFÉRENTS de la même classe 2 cœurs : la vague 5 au bac de
la campagne, vljfs6pcj au bac re-provisionné du 17/11 — les horloges
murales et la contention du pool varient au bac près ; la réserve de
la plage v181 [39,1–39,7] COUVRE les 39,3/39,2 de la vague 5 — jamais
moyennées, les trois distributions consignées côte à côte).

### 4.2 La re-mesure avant/après (gelée)

LA MÊME MACHINE (ce bac, 2 cœurs — le record), time.monotonic, LES
MÊMES LISTES FIXES que la vague 5 (aucune étape ajoutée, aucune
retirée — le runner de vljfs6pcj reconduit, ses étapes et ses
commandes TELLES QUELLES) :

- AVANT : les outils v180 (l'état sans mémo), n = 5 exécutions ;
- FROID : la pile adoptée (mémo v2 + double moteur), le mémo v2
  effacé avant : 1 exécution (la semence, consignée, jamais le
  régime) ;
- CHAUD : la pile adoptée, le mémo v2 présent et vérifié : n = 5 ;
- BRAS C : la liste fixe du bras C (mesure_c_v181.py, la chaîne
  TRIXIE re-provisionnée aux versions exactes) : n = 5 ;
- L'AUDIT : le 10ᵉ run de la pile (le compteur vécu sur la SÉQUENCE
  chaud : les 5 premiers runs semant, les runs d'audit conduits à la
  suite JUSQU'AU 10ᵉ — la preuve d'identité ligne à ligne exigée).

LES DISTRIBUTIONS par étape et au total (n, médiane, q1, q3, min, max
— jamais de moyenne sans distribution). Les consoles capturées à
CHAQUE exécution — l'identité des verdicts entre exécutions d'une
même configuration est une condition de validité (la preuve qu'aucun
contrôle ne fut retiré : les consoles des oracles de la pile adoptée
IDENTIQUES ligne à ligne aux originales v180/v181, diff vide).

### 4.3 Le ratio et H5 (gelé — l'instruction tranche)

LE RATIO = la médiane T (chaud) / la médiane C, les deux bras sur
CETTE machine. LA RÈGLE DE L'INSTRUCTION (elle tranche, le plan
l'applique à la lettre) : SI le ratio après adoption passe sous ×10 —
ÉNONCER EXPLICITEMENT QUE H5 DEVIENT TENUE et mettre à jour la table
des statuts (le manuscrit porte la table : H5 « au plus un facteur
dix » D204). SI le ratio reste ≥ ×10 : consigné tel quel. La
réhabilitation, si elle vit, est PORTÉE PAR L'INSTRUCTION DU MAÎTRE
(la décision explicite qui manquait à mof9q10vq — la règle de
vljfs6pcj « la réhabilitation exige le terrain » est AMENDÉE par la
présente instruction : le terrain à venir confirmera, la table porte
le statut TEL QUE mesuré, la source nommée).

---

## 5 · L'ÉTAPE DE VÉRIFICATION (gelée — l'instruction, sa lettre)

1. LES CONSOLES DES ORACLES diff-identiques aux originales (diff
   vide) — la pile adoptée contre les v180/v181 consignés ;
2. LES EMPREINTES DES PIÈCES SCELLÉES intactes avant/après chaque
   configuration (loupe.exe, proxy.exe, selftest.exe, les pièces des
   deux unités) ;
3. LES RE-RUNS D'AUDIT DE MÉMOÏSATION verts (l'identité champ à
   champ, la console ligne à ligne) ;
4. L'ÉCHANTILLON DOUBLE MOTEUR zéro divergence (octet pour octet) ;
5. LA RE-MESURE TOKENS confirmée par re-tokenisation indépendante
   (±1 token) ;
6. LES CONTRÔLES NÉGATIFS : l'entrée de cache mutée → attrapée ; le
   moteur divergent → refus nommé ; le pointeur muté → refus nommé ;
7. LES NOUVELLES ASSERTIONS M4/TOKENS AU LINTER (v194) : les valeurs
   OPT-04, la base d'arrondi M4 CANONISÉE (17,9× la valeur consignée
   — l'écart 17,8× de la pièce R11 verbatim demeurant NOMMÉ à côté),
   le pointeur seul, le ratio et le statut H5, la visibilité PUBLIC
   du dépôt (le statut exact porté depuis l'Entrée 369) ;
8. LE DIFF consigné append-only au journal d'optimisation (OPT-04, le
   format D205 : la mesure avant, le gain mesuré, le vérificateur).

---

## 6 · LA CONSIGNATION ET LE PACK (gelé)

OPT-04 au journal d'optimisation ; D222 au journal des décisions
(l'adoption du pointeur seul et de la pile mémo v2 + double moteur,
le statut H5, l'amendement du seuil — SI les mesures sont vertes ;
le rouge consigné tel quel sinon) ; l'Entrée 371 au worklog ; la
carte OU-TROUVER portée ; l'atelier entier au dépôt (D208) ; le push
GitHub au commandement (le jeton du coffre, jamais affiché) ; les
pièces au coffre /test SI le relais OAuth vit au bac — SINON l'écart
nommé (D189) et les pièces livrées à download/ + au dépôt.

LES CINQ DOCUMENTS RÉGÉNÉRÉS (le pack TRIADE_presentation_v0.19.4_
20261120.zip, refusé si un contrôle est rouge) : le manuscrit
v0.19.4 (la table des statuts à jour — H5 le cas échéant, les chiffres
OPT-04, le pointeur seul au format en vigueur de localiser SI mesuré
vert), la spécification v0.15.4 (SI le pointeur est adopté : le format
de réponse de l'opération localiser — une règle ADDITIVE, aucune
règle existante modifiée), le Livre du Coffre v1.3 INCHANGÉ, les
preuves & calculs v0.19.4 (l'OPT-04 verbatim, l'échantillon double
moteur, les distributions), la présentation du 20/11 (la table des
éditions à jour, le statut PUBLIC du dépôt, les chiffres OPT-04).
Chaque pièce gravée (empreintes SHA-256), le zip relu pièce à pièce.

---

## 7 · LA FRONTIÈRE (gelée — l'instruction, sa lettre)

Aucune graine supprimée, aucun vecteur réduit, aucune vérification
retirée (la preuve : les consoles identiques) ; le pool partagé
inter-outils REFUSÉ (le juge ne partage pas l'état du jugé — le mémo
demeure un relevé signé, jamais une émulation partagée ; le moteur
QEMU n'est jamais le juge : hashlib demeure le modèle indépendant) ;
le M10 périodique demeure la porte de scellement ; les artefacts
scellés INTACTS (R4 : le contrat stable — la pile optimise le chemin
de VÉRIFICATION, jamais les blocs vérifiés) ; la clé de test publique
ne prétend à aucune sécurité.
