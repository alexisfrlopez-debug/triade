# PLAN PRÉ-ENREGISTRÉ — L'OPTIMISATION M4 AU-DELÀ DE 39,3 s (vljfs6pcj)

> L'instruction (Qwen__20261116_vljfs6pcj, lue INTÉGRALEMENT avant tout
> geste) : « Optimise le temps de vérification M4 du bras T au-delà des
> 39,3 s actuels, sans retirer aucun contrôle (règle R11 : aucune
> optimisation sans mesure) : (a) invalidation incrémentale des oracles
> différentiels par empreinte de bloc via la carte (ne rejouer que les
> sessions dont les blocs ou contrats ont changé) ; (b) mémoïsation
> scellée des sessions d'émulation pures (clé = empreinte du bloc +
> entrée ; le cache est un artifact vérifié et signé, jamais un état
> partagé entre juge et jugé — le compromis refusé de partage
> d'émulation reste refusé) ; (c) évalue un pré-filtre différentiel
> natif rapide suivi de l'émulation de confirmation, en mesurant d'abord
> son effet sur le chemin critique crypto (~10 s pour 196 KiB). Mesure
> avant/après sur la même machine de laboratoire, chronomètre monotone,
> n≥5 runs par configuration avec distributions, listes de commandes
> fixes par bras. ÉTAPE DE VÉRIFICATION : après modifications, exige que
> les sorties des oracles soient identiques ligne à ligne aux originales,
> que les rebuilds de cristallisation restent byte-identiques (10/10),
> que les empreintes scellées soient inchangées, que le bras C soit
> re-mesuré sur la même machine, et que le ratio M4 et le verdict H5
> soient recalculés depuis les logs bruts par le script d'extraction ;
> consigne le résultat même si H5 reste falsifiée. »

CE PLAN EST GELÉ AVANT TOUTE MESURE — son empreinte sha256 sera
consignée au journal des décisions (D214) et au journal
d'optimisation (OPT-03) AVANT la première exécution de mesure ; le
commit git de ce fichier précède toute donnée de mesure au dépôt.

---

## 1 · L'ÉTAT DE DÉPART (la mesure qui fait foi)

La liste fixe du bras T (le plan D204, vécue à la vague 5,
l'instruction mof9q10vq, consignée R11 au rapport p8) : TOTAL 39,3 /
39,2 s (deux exécutions consécutives, machine à 2 cœurs, n=2 — JAMAIS
moyennées) :

| étape | secondes |
|---|---|
| garde-sceau-I | 0,073 |
| cristallisation (12 rebuilds concourants) | 4,27 |
| round-trip-notation ×2 | 0,244 / 0,237 |
| oracle-bloc-loupe-01 (parallèle) | 10,428 |
| build-recomposition-loupe-02 | 0,471 |
| oracle-du-bloc-loupe-02 (parallèle) | 22,912 |
| epreuve-scenario-posix | 0,305 |
| assemblage-kits | 0,265 |

LE PROFIL MESURÉ (le rapport p8 le nomme) : l'OUVERTURE de session —
le md5+sha256 du fichier ENTIER sous émulation — domine tout : ~10 s
pour le témoin 196 Kio (loupe-01), 3,2 s pour 65 Kio (proxy.exe) ; les
lectures sont quasi gratuites (0,15 ms). Le chemin critique restant
EST l'émulation cryptographique des sessions de contrat — c'est lui
que les leviers (b)/(c) attaquent, c'est lui que (a) épargne au
re-jeu.

## 2 · LES TROIS LEVIERS, TELS QUELS (l'instruction les nomme, le plan les gèle)

### (a) L'INVALIDATION INCRÉMENTALE PAR EMPREINTE DE BLOC VIA LA CARTE

Le mémo (ci-dessous) est INDEXÉ par l'empreinte de TOUT ce qui
détermine le résultat d'une session pure :
l'empreinte du BLOC (sha256 des octets assemblés de la notation — la
carte porte le bloc, l'oracle l'assemble de toute façon : l'empreinte
est LUE de la carte vivante, jamais crue), l'empreinte de l'ENTRÉE
(sha256 du contenu du fichier soumis), l'empreinte du CONTRAT (sha256
du fichier de couche I qui porte les vecteurs : loupe-01-ouvrir.md /
loupe-02-lire.md), et l'identifiant de l'oracle. TOUT changement d'un
quelconque de ces termes CHANGE LA CLÉ → échec de recherche → LA
SESSION EST REJOUÉE EN ENTIER (l'invalidation est par construction :
rien ne peut être « invalidé de travers », une clé différente est une
absence). Ne rejouer que les sessions dont les blocs ou contrats ont
changé = ne réutiliser QUE les sessionsdont aucun terme n'a bougé.

### (b) LA MÉMOÏSATION SCELLÉE DES SESSIONS D'ÉMULATION PURES

Une session d'ouverture est PURE : le bloc (les octets assemblés) et
l'entrée (le contenu du fichier) déterminent le résultat — la sortie
(rax, l'état propre — pile équilibrée, canaris intacts, non-volatils
rendus —, le cadre né : chemin, taille, vue, curseur, remplissage,
tampon, le panneau 48 o) est une FONCTION de (bloc, entrée).
LE MÉMO enregistre cette sortie sous la clé (a). LE SCEAU :
chaque entrée porte son hachage ; les entrées sont CHAÎNÉES
(h_i = sha256(h_{i-1} ‖ clé_i ‖ valeur_i)) ; la racine de la chaîne
est SIGNÉE Ed25519 par la clé de TEST du laboratoire (la même
discipline que le sceau-I spec § 8 : dérivée d'une constante
PUBLIQUE, sa non-sécurité EST la preuve visible de l'état
laboratoire ; la clé RÉELLE du développeur n'apparaît jamais ici —
la cérémonie réelle du mémo est un geste du développeur si adoption
il y a). À CHAQUE chargement : la chaîne ENTIÈRE est recalculée et la
signature VÉRIFIÉE — tout écart = REFUS nommé, fail-closed (le
mémo n'est jamais cru, il est vérifié).
LE MÉMO EST UN ARTIFACT, PAS UN ÉTAT : chaque outil (le build, le
round-trip, l'oracle) garde SA propre émulation vivante — le refus
de la vague 5 (le pool persistant inter-outils : « le juge ne partage
pas l'état du jugé ») DEMEURE INTACT. Le mémo n'est pas une émulation
partagée : c'est un relevé signé de sessions passées, réduit par clé
et jugé à chaque usage.

### (c) LE PRÉ-FILTRE DIFFÉRENTIEL NATIF + L'ÉMULATION DE CONFIRMATION

Le chemin critique crypto (le md5+sha256 du témoin 196 Kio sous
émulation, ~10 s) voit son jugement PRÉ-CALCULÉ nativement : le juge
indépendant (hashlib) produit l'attendu en ~2 ms (mesuré au § 5). LE
PRÉ-FILTRE : l'attendu natif EST comparé au panneau RELEVÉ (du mémo
scellé si la clé vit, d'une émulation vivante sinon). CONCORDANCE →
la session est vérifiée (le relevé une fois produit, le juge juge à
chaque usage). DISCORDANCE OU ABSENCE → L'ÉMULATION DE CONFIRMATION
court en entier (le ~10 s) et tranche — et le mémo est corrigé par
la même occasion (la session re-jouée remplace le relevé fautif ou
absent). Le pré-filtre ne RETIRE rien : il ne fait que RÉORDONNER le
calcul du juge — l'attendu natif remplace l'attendu différé, la
confrontation reste intégrale.
L'EFFET MESURÉ D'ABORD (l'instruction l'exige) : le coût du calcul
natif md5+sha256 sur 196 Kio est chronométré seul (n≥5) et rapporté
face au coût de l'émulation du même calcul (le chemin critique) —
l'ordre de grandeur du levier est consigné AVANT la mesure de bout
en bout.

### CE QUE LES LEVIERS NE TOUCHENT PAS (gelé)

- Les FALSIFICATIONS DEMANDÉES (V4 loupe-01, V5 loupe-02) : VIVANTES
  — elles opèrent sur des sessions BON MARCHÉ (le témoin 384 o) que
  le mémo n'atteint jamais.
- Les LECTURES du bloc sous test (loupe-02) : VIVANTES à chaque
  décalage — l'unité sous test n'est JAMAIS relue du mémo dans SON
  propre oracle ; seul le loupe-01 SCELLÉ (l'auxiliaire crypto) est
  relevé, et son relevé est JUGÉ (le différentiel contre le modèle
  indépendant reste intégral, ligne à ligne).
- Les sessions < 64 Kio : VIVANTES (leur coût est nul — temoin-1,
  temoin-384, vide, rfc1321) ; le périmètre du mémo est EXACTEMENT
  le chemin critique mesuré : les ouvertures pures ≥ 64 Kio
  (temoin-3f.bin 196 609 o ; proxy.exe 65 024 o).
- La CRISTALLISATION (12 rebuilds concourants), le garde-sceau-I,
  les round-trips, le scénario POSIX, l'assemblage : INTACTS.
- La re-vérification complète périodique (la suite M10, 159×3
  graines) : HORS de cette liste, INCHANGÉE — elle demeure la porte
  de scellement.

### LE RISQUE RÉSIDUEL NOMMÉ (l'honnêteté l'exige)

Le mémo relève une exécution ; si un bloc était NON-DÉTERMINISTE
(mêmes octets, mêmes entrées, sorties différentes — un compteur, une
horloge), le relevé gèlerait UNE sortie et masquerait la variance.
LES GARDES : (1) la cristallisation prouve le déterminisme des
rebuilds à chaque M4 (12 sorties byte-identiques) ; (2) la porte M10
re-joue tout périodiquement ; (3) le mémo naît d'une exécution
vivante et CHAQUE contrôle de session re-juge le relevé contre le
modèle indépendant. Le risque est NOMMÉ, borné par les gardes, et
consigné au rapport.

## 3 · LE MÉMO — FORMAT EXACT (gelé)

Fichier : memo-sessions-v1.json — l'en-tête porte la version du
format, l'horodatage de semence, la constante publique de la clé de
test, la clé publique Ed25519, la racine de la chaîne, la signature
(64 o hex). Chaque entrée : {cle, valeur, h} où cle = sha256(
  sha256(octets_assemblés_du_bloc) ‖ sha256(contenu_de_l'entrée) ‖
  sha256(octets_du_contrat) ‖ identifiant_oracle) et valeur = {rax,
  etat_propre, chemin, taille, vue, curseur, remplissage, tampon_hex
  (≤ 384 o), panneau_hex (48 o), secondes_vivantes (le coût de la
  session vivante au semis — le prix évité, consigné)}.
La chaîne : h_0 = sha256("TRIADE-MEMO-V1" ‖ cle_0 ‖ valeur_sérialisée_0),
h_i = sha256(h_{i-1} ‖ cle_i ‖ valeur_sérialisée_i) ; la racine h_n
est signée. Toute insertion/retrait recalcule la chaîne et re-signe.
UN MÉMO JAMAIS VÉRIFIÉ = UN MÉMO REFUSÉ (code 2, REFUS nommé).

## 4 · LE PROTOCOLE DE MESURE (gelé — n≥5 par configuration)

LA MÊME MACHINE (ce bac, 2 cœurs — la machine fait partie du record),
le chronomètre time.monotonic, LES MÊMES LISTES FIXES que la vague 5
(aucun ajout, aucune suppression d'étape) :

- **AVANT** — la liste fixe de la vague 5 (les outils v180 tels
  quels, l'état actuel du projet) : n = 5 exécutions consécutives.
- **APRÈS-FROID** — la liste v181, mémo ABSENT (effacé avant) : 1
  exécution (la semence — le prix du premier passage, consigné, il
  n'est PAS la mesure de régime).
- **APRÈS-CHAUD** — la liste v181, mémo présent et vérifié :
  n = 5 exécutions consécutives.
- **BRAS C** — la liste fixe du bras C (mesure_c_v180.py, la chaîne
  croisée TRIXIE re-provisionnée aux versions EXACTES de la
  campagne : gcc-mingw-w64 14.2.0-19+27+b1, binutils 2.44-3+12+b1,
  mingw-w64 12.0.0-5) : n = 5 exécutions consécutives.
- **LE PRÉ-FILTRE SEUL** — le coût natif hashlib (md5+sha256) du
  témoin 196 609 o : n = 5, chronométré isolément (l'effet (c)
  mesuré d'abord).

LES DISTRIBUTIONS consignées par étape et au total : n, médiane, q1,
q3, min, max — JAMAIS de moyenne sans distribution. Les consoles
capturées à CHAQUE exécution (l'identité des verdicts entre
exécutions d'une même configuration est une condition de validité).

## 5 · L'ÉTAPE DE VÉRIFICATION (gelée — l'instruction l'exige)

1. **Les consoles des oracles v181 IDENTIQUES ligne à ligne aux
   originales** (les v180 de la vague 5, qui sont identiques aux
   outils de campagne) : diff vide exigé, les deux oracles.
2. **La cristallisation byte-identique** : les 12 rebuilds (les 10 +
   l'édification + le témoin — l'instruction dit 10/10, la liste
   fixe en porte 12) TOUS identiques, la pièce d'origine intacte.
3. **Les empreintes scellées inchangées** : loupe.exe, proxy.exe,
   selftest.exe, les pièces des deux unités — vérifiées AVANT/APRÈS
   chaque configuration.
4. **Le bras C re-mesuré** sur cette machine (n=5).
5. **Le ratio M4 et le verdict H5 recalculés depuis les logs bruts
   par le script d'extraction** (extraire_m4_v181.py — jamais tapé à
   la main) : le ratio T/C lu des médianes des distributions, le
   verdict H5 (« au plus un facteur dix » — D204) RÉ-ÉVALUÉ ; SI le
   ratio repasse sous ×10 : rapporté comme NOUVELLE MESURE (n=5) SANS
   DÉCLARER H5 RÉHABILITÉE (la règle mof9q10vq reconduite — la
   réhabilitation d'une hypothèse pré-enregistrée falsifiée exige le
   terrain, pas un levier) ; SI H5 reste falsifiée : consigné tel
   quel, l'instruction l'exige.
6. **La falsification du mémo vécue** (le contrôle négatif — la
   culture du projet l'exige) : un octet du mémo muté → le chargement
   REFUSE (chaîne rompue) ; une entrée mutée → REFUS ; le mémo
   absent → la session vivante court (le repli est l'émulation
   complète, jamais l'échec muet).

## 6 · LA CONSIGNATION (gelée)

OPT-03 au journal d'optimisation (le format D205 : la mesure avant
tout, le gain mesuré, le vérificateur) ; D214 au journal des
décisions ; l'Entrée 328 au worklog ; l'atelier entier au dépôt (la
règle D208 : les pièces de preuve vivent au DÉPÔT) ; le push GitHub
au commandement du développeur (la synchro git/drive d'abord — vécue
à l'ouverture de la session : les jetons /Tokens recoupés byte-byte,
GitHub 0/0 au 75aaebd, le Drive recoupé) ; les livrables à download/.
L'ADOPTION du mémo comme OUTIL DU PROTOLOLE est UNE DÉCISION À PART
— jamais le protocole sur une seule mesure (la règle de D213
reconduite : le mémo vivra l'épreuve du terrain avant l'adoption).

## 7 · LA FRONTIÈRE (gelée)

Aucun contrôle retiré (le juge indépendant juge CHAQUE session —
relevée ou vivante) ; aucun état partagé entre juge et jugé (le
refus de la vague 5 demeure) ; aucune graine supprimée, aucun
vecteur réduit ; la clé de test publique ne prétend à aucune
sécurité (la cérémonie réelle appartient au développeur) ; la
machine (2 cœurs) fait partie du record ; le M10 périodique demeure
la porte de scellement.
