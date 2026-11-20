# PLAN PRÉ-ENREGISTRÉ — OPT-05 : L'ÉDITION ET L'AJOUT PAR HUNKS + LE DOUBLE MOTEUR AU CHEMIN CHAUD (pe6iv71fj)

> L'instruction (Qwen_text_20261120_pe6iv71fj.txt, lue INTÉGRALEMENT avant
> tout geste, md5 recoupé au téléchargement) : « Optimise le coût en tokens
> d'édition/ajout et le temps de vérification du chemin chaud, sans retirer
> aucun contrôle, sans affaiblir aucun tueur, sans modifier les artefacts
> scellés (R11 : aucune optimisation sans mesure). (1) Pré-enregistre le
> plan OPT-05 (hypothèses, critères, graines, empreinte verrouillée) AVANT
> toute mesure. (2) Édition/ajout par hunks : définis un format de réponse
> où l'agent rend des hunks de notation (diff ciblé) au lieu de réémettre
> la notation complète ; le client applique les hunks, reconstruit le
> bloc, et confronte par round-trip exact ; quatre refus nommés
> fail-closed (HUNK-INCONNU, CONTEXTE-DIVERGENT, ROUND-TRIP-DIVERGENT,
> HORS-FORMAT). Mesure avant/après à la même graine sur les opérations
> éditer et ajouter (tokenizer natif, n≥18, distributions complètes).
> (3) Ouverture de session : étends le double moteur au chemin crypto
> émulé — volume sous QEMU-user (compteur plugin/bloc), échantillon
> d'audit sous Unicorn ; la clé de mémo v2 reste sha-256 de tout ce qui
> détermine le résultat ; le juge ne partage jamais l'état du jugé.
> Mesure M4 avant/après (horloge monotone, liste de commandes fixe, n≥5
> par configuration). (4) Reporte les gains et les ratios résiduels vs
> bras C ; nomme tout écart défavorable. »

CE PLAN EST GELÉ AVANT TOUTE MESURE — son empreinte sha256 sera consignée
au journal des décisions (D224) et au journal d'optimisation (OPT-05)
AVANT la première exécution de mesure ; le commit git de ce fichier
précède toute donnée de mesure au dépôt.

LA MACHINE DE RECORD : ce bac, 2 cœurs, 4 Go (la classe des campagnes
D204, vljfs6pcj et cq01qv1za) — la machine fait partie du record. La
pile re-provisionnée : qemu-user 1:10.0.13+ds-0+deb13u1 (extrait du
.deb sans root, chemin local), unicorn 2.1.4, capstone 5.0.9,
keystone-engine 0.9.2, gcc 14.2.0 (la cible C aux mêmes versions que
Trixie), le CLI z-ai (glm-4-plus, l'unique famille de l'API — le même
modèle que toutes les campagnes précédentes).

---

## 1 · LE FORMAT HUNK (gelé) — la réponse de l'agent à l'édition/ajout

### 1.1 La grammaire (une seule, pour éditer et ajouter)

L'agent rend UNIQUEMENT des hunks, jamais la notation complète :

```
@@ hunk <k>/<n>
base: <UNE ligne exacte de la base, recopiée telle quelle (l'ancre)>
- <une ligne exacte de la base à retirer à l'ancre>     [0..m lignes]
+ <une ligne de notation nouvelle à insérer à l'ancre>  [1..p lignes]
@@ hunk <k+1>/<n>
...
FIN-HUNKS
```

RÈGLES : (a) l'ancre « base: » est une ligne EXISTANTE de la base
(notation courante pour éditer ; gabarit de famille pour ajouter),
recopiée octet pour octet ; (b) les lignes « - » précisent les lignes
exactes retirées À PARTIR DE L'ANCRE ; (c) les lignes « + » sont les
lignes nouvelles insérées au même point ; (d) les hunks sont appliqués
EN ORDRE, chaque ancre cherchée dans le texte courant ; (e) RIEN
d'autre dans la réponse — aucun commentaire hors hunks, la dernière
ligne est exactement « FIN-HUNKS ».

### 1.2 Le client (application + confrontation, fail-closed)

Le client applique les hunks à la base, reconstruit la notation
candidate, puis CONFRONTE PAR ROUND-TRIP EXACT : la notation candidate
est assemblée par keystone et désassemblée par capstone ; tout écart
d'instruction, d'opérande ou de taille d'encodage est un refus. LES
QUATRE REFUS NOMMÉS (le premier rencontré l'emporte, fail-closed) :

1. **HORS-FORMAT** — la réponse ne parse pas à la grammaire (pas de
   « FIN-HUNKS », un « @@ hunk » mal formé, une ligne hors formes
   admises, une réponse vide) ;
2. **HUNK-INCONNU** — l'ancre « base: » d'un hunk n'existe pas dans le
   texte courant (la base ou l'état après les hunks précédents) ;
3. **CONTEXTE-DIVERGENT** — une ligne « - » ne correspond pas
   exactement au texte à l'ancre (l'octet près) ;
4. **ROUND-TRIP-DIVERGENT** — la notation reconstruite ne round-trip
   pas (assemblage/désassemblage), ou la reconstruction ne produit pas
   le texte attendu de la confrontation.

Aucun refus n'est contournable : la sortie est le refus nommé, la
notation candidate n'est JAMAIS écrite.

### 1.3 Les tâches gelées (les MÊMES aux deux modes, la graine 20261117)

LES 18 BLOCS du domaine loupe, l'ORDRE de la graine 20261117 (la
vérité-terrain 5gfx6pwkj, jamais re-tirée) :
i110007, i110011, i110002, i110012, i110003, i110010, i110009, i110017,
i110016, i110013, i110014, i110018, i110006, i110015, i110004, i110008,
i110001, i110005.

**ÉDITER — LE TYPE GELÉ « LA CONSTANTE REVUE »** (une révision de
contrat réelle, la classe la plus fréquente des éditions vécues — les
révisions de garde et de borne du projet) : dans chaque bloc, LA
PREMIÈRE instruction portant un opérande immédiat de travail (cmp ou
mov, registre destination autre que rsp/rbp — les tailles de cadre et
les déplacements mémoire EXCLUS) voit son immédiat révisé : imm →
imm − 1 (imm > 0), l'immédiat 0 → −1 (la révision de sentinelle). LA
LISTE EXACTE DES 18 ÉDITIONS (le fichier, la ligne, l'ancienne
instruction, la nouvelle instruction) est générée par le script
`taches_edition.py` AVANT TOUTE MESURE et son empreinte sha256
consignée ici : sha256:1122251ef52006fb916077226010d1d955c2d2bc5cf07afa591fb51177e001d4 ; l'ordre des blocs est celui de
la graine 20261117, jamais re-tiré.

- LE MODE AVANT (le format en vigueur) : le matériau = la notation
  complète du bloc (lue du fichier même) + la consigne de révision ;
  la réponse = LA NOTATION COMPLÈTE RÉVISÉE (le format actuel de
  l'opération éditer, la pratique de toutes les ères).
- LE MODE HUNK : le même matériau, la même consigne ; la réponse = LES
  HUNKS (le format § 1.1), le client applique, reconstruit, round-trip.

**AJOUTER — LE TYPE GELÉ « LE BLOC RÉÉCRIT DEPUIS LE CONTRAT »** (la
classe d'ajout vécue : une nouvelle unité écrite de sa spécification) :
le matériau = le contrat de couche I du bloc (loupe/I/loupe-XX.md, MOT
POUR MOT) + les conventions de notation du domaine (l'extrait de
gabarit : prologue/épilogue msx64, la feuille pure sans IAT) ; la
réponse = la notation complète (mode AVANT) ou LES HUNKS contre le
GABARIT DE FAMILLE (mode HUNK : le gabarit = le squelette de feuille
pure — les pushes, sub rsp, le retour d'épilogue — l'agent rend les
hunks qui insèrent le corps, les gardes et les étiquettes entre les
lignes du gabarit).

### 1.4 Les règles de verdict (pré-enregistrées, falsifiables)

- **ZÉRO DIVERGENCE EXIGÉ AUX DEUX MODES** : au mode AVANT de l'édition,
  la notation complète rendue doit être la notation du bloc révisée (la
  confrontation : la partie CODE de la réponse contre la notation du
  dépôt porteuse de LA MÊME révision — l'égalité ligne à ligne aux
  lignes de code, les commentaires d'en-tête exclus) ; au mode HUNK,
  l'application des hunks doit produire LA MÊME notation révisée (la
  même confrontation croisée : le résultat appliqué du mode HUNK contre
  la réponse du mode AVANT, la partie CODE égale) et round-triper.
  Pour AJOUTER, la confrontation croisée est IMPOSSIBLE PAR
  CONSTRUCTION (deux générations indépendantes d'un même contrat
  diffèrent légitimement) : la conformité y est (a) le format (les
  refus nommés à l'application), (b) LE ROUND-TRIP EXACT de la notation
  reconstruite (assemblage keystone + désassemblage capstone, tout
  écart un refus), (c) les obligations structurelles du contrat (la
  convention de signature, les gardes de pré-conditions P1..Pn là où
  le contrat les exige, la sortie nommée du post-condition). Toute
  réponse non conforme est une divergence NOMMÉE (le refus ou l'écart),
  JAMAIS une correction silencieuse.
- **LE GAIN LU DES LOGS BRUTS** par le script d'extraction
  (extraire_opt05.py) : 1 − médiane(hunk)/médiane(avant), par
  opération (éditer, ajouter), le total ET la réponse séparément ;
  jamais tapé à la main.
- **L'ATTENTE DIRECTIONNELLE FALSIFIABLE** : éditer −60 à −80 % (la
  réponse de l'édition complète est le bloc entier ~40-400 lignes, le
  hunk ~5-15 lignes) ; ajouter −40 à −70 % (le corps reste à écrire,
  le squelette ne l'est plus). SI la mesure falsifie ces bornes, le
  résultat est consigné TEL QUEL et l'adoption n'a pas lieu.
- **n = 18 PAR CELLULE** (2 opérations × 2 modes × 18 blocs = 72
  appels instrumentés, tous au tokenizer natif LU du champ usage — le
  ×1,08 interdit ; les distributions complètes consignées : n, médiane,
  q1, q3, min, max par cellule et par champ prompt/complétion).
- **AUCUN CONTRÔLE RETIRÉ** : la confrontation de notation (l'égalité
  au attendu), le round-trip keystone/capstone, la vérification
  d'adresse (le slot du bloc inchangé — l'édition ne déplace RIEN,
  R7), les empreintes scellées vérifiées avant/après (loupe.exe,
  proxy.exe, selftest.exe et les pièces de campagne INTACTES).
- **LES CONTRÔLES NÉGATIFS** (trois, nommés au premier refus) : (a) un
  hunk volontairement faux (une ligne « + » qui n'appartient pas à la
  notation attendue) → ROUND-TRIP-DIVERGENT ; (b) une ancre
  volontairement divergente (une ligne « base: » inexistante) →
  HUNK-INCONNU ; (c) une réponse hors format (une notation complète au
  lieu des hunks) → HORS-FORMAT. Chacun ATTRAPÉ au premier refus.

### 1.5 L'adoption (une décision à part, jamais sur une seule mesure)

L'adoption du format hunk comme format D'ÉDITION de la carte est une
décision append-only AU DÉVELOPPEUR si la mesure est verte — le
précédent D213/D222 reconduit : le protocole ne bascule jamais sur une
seule campagne ; la spécification v0.15.5 ne porte PAS de règle hunk
(la règle viendra de l'adoption, la vague suivante la consignera).

---

## 2 · LE DOUBLE MOTEUR AU CHEMIN CHAUD DE L'OUVERTURE DE SESSION (gelé)

### 2.1 Le périmètre étendu : le chemin crypto émulé

LA PILE TELLE QU'ADOPTÉE (D222) : mémo v2 (la clé = sha256 du bloc ‖
l'entrée ‖ le contrat ‖ la configuration d'émulateur ‖ la graine ‖
l'oracle — tout ce qui détermine le résultat), le compteur de runs
chaîné au cœur signé, l'audit 1 run sur 10 (re-exécution vivante,
preuve d'identité champ à champ), QEMU-user au volume, Unicorn à
l'échantillon consigné. LE JUGE NE PARTAGE JAMAIS L'ÉTAT DU JUGÉ.

L'EXTENSION (le point 3 de l'instruction) : le chemin chaud de
l'ouverture de session couvre désormais les DEUX voies d'émulation :
(a) les blocs du noyau loupe (l'existant, les oracles des unités) ET
(b) LE CHEMIN CRYPTO ÉMULÉ — les blocs sha-256/md5/cumul du domaine
(les cibles crypto de l'oracle : loupe-05, loupe-06, loupe-07),
exécutés au volume sous QEMU-user AVEC COMPTEUR PAR BLOC (le plugin :
chaque opération compte les blocs traversés), et l'ÉCHANTILLON
D'AUDIT sous Unicorn (le même programme d'opérations, la sérialisation
au même format, la comparaison octet pour octet des deux flux :
divergence = 0 exigée, tout écart nommé et bloquant).

### 2.2 La mesure M4 avant/après (gelée)

LA LISTE DE COMMANDES FIXE : celle de la vague 5 (le runner
outil_m4_v182.py — les étapes et les commandes TELLES QUELLES, aucune
ajoutée, aucune retirée), étendue de l'étape crypto (le programme
d'opérations crypto au même harnais, la même liste pour les deux
configurations). LES CONFIGURATIONS :

- **--mode avant** : la pile v180 (SANS mémo, SANS double moteur) —
  n = 5 ;
- **--mode chaud** : la pile v182 ÉTENDUE crypto (mémo v2 + double
  moteur au noyau ET au chemin crypto) — n = 5, l'audit 1 run sur 10
  y vit ;
- **--mode audit** : la preuve d'identité dédiée (1 exécution, hors
  distribution — son prix est le prix de la vérification, nommé).

LE CHRONOMÈTRE : monotone (time.monotonic), chaque étape mesurée
séparément, la même machine, les empreintes scellées vérifiées
AVANT/APRÈS chaque exécution. LES CONSOLES des oracles capturées
INTÉGRALEMENT — l'identité ligne à ligne avec les originales exigée
(les 24 consoles d'oracles de la campagne précédente demeurent la
référence : AUCUNE ne doit changer).

### 2.3 Les règles de verdict M4 (pré-enregistrées)

- Les gains rapportés par configuration (avant/chaud), le ratio au
  bras C (re-mesuré à la même session, n=5) — AUCUN chiffre attendu
  écrit avant mesure (R11 : la mesure fait foi).
- TOUT ÉCART DÉFAVORABLE NOMMÉ : si le chemin chaud étendu coûte PLUS
  que la pile v182 au noyau seul, l'écart est consigné tel quel et
  l'extension n'est pas adoptée.
- Les 24 consoles d'oracles ligne-identiques aux originales ; la
  batterie de mutation re-visitée aux mêmes graines : 811/832 INTACT
  (aucun tueur affaibli — la vérification de la conformité est la
  pièce jointe, jamais re-écrite).

---

## 3 · LA CONSIGNATION

- OPT-05 au journal d'optimisation des tokens (le format D205), la
  décision append-only D224 (les faits, les alternatives rejetées, le
  développement).
- L'atelier atelier-opt05-pe6iv71fj/ porte TOUTES les pièces : le
  plan, les tâches gelées, les journaux bruts (jsonl), les réponses
  conservées, les contrôles négatifs, les rapports.
- Les empreintes sha256 des artefacts scellés avant/après : INTACTES
  (loupe.exe, proxy.exe, selftest.exe, les pièces de campagne).
- Le rapport RAPPORT-OPT05.txt : les distributions complètes, les
  gains, les ratios, les écarts nommés, les verdicts.

L'EMPREINTE DE CE PLAN (verrouillée au commit) :
sha256:consignée au commit par generer_empreinte (le plan gelé AVANT toute mesure ; la valeur consignée à D224)
