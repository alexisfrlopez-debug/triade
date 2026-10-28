# PROTOCOLE TRIADE v0.5.2 — Spécification technique

> Source de travail faisant autorité pour la v0.5.2. Les archives formelles des versions
> précédentes demeurent : `docs/Protocole_TRIADE_v0.5.0_Specification.pdf` (v0.5.0),
> `docs/Protocole_TRIADE_v0.4.0_Specification.pdf` (v0.4.0),
> `docs/Protocole_TRIADE_v0.3_Specification.pdf` (v0.3),
> `docs/Protocole_TRIADE_v0.2_Specification.pdf` (v0.2). La série documentaire compte
> également la démonstration RoomEq (`docs/Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf`)
> et l'édition académique v0.4 (`docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf`, D18 —
> présentation IMRAD du noyau v0.3, sans valeur normative). Depuis la décision D17,
> le PDF formel de la version courante est **régénéré systématiquement** à chaque
> modification des sources du protocole : `scripts/build_pdf.sh` compare l'empreinte des
> sources au stamp du dernier build et reconstruit avant chaque sauvegarde (`sync_backup.sh`).
> La v0.5.2 consigne la garde durable de la phrase de contrôle du coffre-fort (D81) ;
> la v0.5.1 avait ajouté le coffre-fort des phrases maîtresses (D75) et consigné M3 franchi
> (balise finale 0.4.0) ; la v0.5.0 demeure la révision du retour du terrain (validation
> normée, taxonomie X1–X8, jalons M0–M2).

- Version : v0.5.2 — phrase de contrôle du coffre-fort sous garde durable dépôt + coffre Drive (D81) ; état des jalons constaté : M0–M3 franchis (balises 0.2.0, 0.3.0, 0.4.0), M4 ouvert (D77)
- Date : 28 octobre 2026
- Couches : I/B/C · Profil primaire : x86-64 / Windows 11 / PE32+
- Hiérarchie de la fonction objectif : **Sécurité > Performance > Optimisation > Coût en tokens** — inchangée et verrouillée (D19)

---

## 1. Vision et objectifs

Le développement logiciel est entré dans l'ère agent-first : une part croissante du code est
écrite, relue et modifiée par des modèles de langage plutôt que par des humains. Cette
bascule remet en question une hypothèse centrale de nos outils — que le code source est
optimisé pour la lecture humaine. Compilateurs, systèmes de build et langages ont été conçus
autour de cette hypothèse ; si le lecteur principal devient une machine, l'empilement
complet mérite un réexamen systématique plutôt qu'une révision marginale.

TRIADE est la réponse disciplinée à ce réexamen. Plutôt que de supprimer les langages — une
impossibilité de principe, puisqu'un modèle de langage manipule des symboles textuels et que
tout format binaire rendu lisible par un agent constitue de facto un langage —, TRIADE
déplace le langage vers une fine couche de spécification maintenue par l'agent, tandis que
l'artefact livré est du code machine natif pur. Le compilateur disparaît du pipeline de
livraison : ce que l'agent écrit est ce qui s'exécute — et rien d'autre.

Le nom encode l'architecture : trois couches indissociables — Intention (I), Binaire (B),
Carte (C) — unies par un verrou croisé cryptographique. La couche I contient le quoi et le
pourquoi : contrats typés, pré et post-conditions, invariants, cas d'échec, vecteurs de
vérification. La couche B contient le comment : des octets scellés, versionnés, à adresses
stables. La couche C est l'index naviguable qui lie les deux et sert d'unique interface de
développement à l'agent.

La v0.4.0 tire les enseignements de la première validation à l'échelle — le recodage complet
de RoomEq (démonstration v0.3) — et les convertit en normes : ce que la démonstration a
pratiqué (reverse-specs, pré-versions, partage de fixtures, mesure avant optimisation)
devient exigence ; ce que son analyse des défauts a révélé devient taxonomie ; ce que son
étude de cas a établi et ne prouve pas reste explicitement hors périmètre de preuve.

La v0.5.0 est la révision du retour du terrain. Les jalons M0 (chaîne artefact), M1
(mini-libc scellée) et M2 (patch à chaud en production, avec retour arrière) sont franchis
— chacun sur validation terrain Windows 11, chacun scellé par une balise finale immuable
(0.2.0, 0.3.0). La campagne M2 a coûté huit classes de défauts invisibles à l'émulation
(§ 8.5) — le prix d'une leçon : un oracle valide un artefact contre un modèle
d'environnement, et la complétude du modèle ne se démontre qu'en exécutant le binaire sur
le système réel. Ce que le terrain a appris devient norme : la boucle d'évidence (§ 8.4),
la taxonomie X, l'instrumentation contractualisée — et l'ouverture du jalon M3, contrats
renforcés sur entrées non fiables.

### 1.1 Fonction objectif hiérarchisée — invariant de révision

**Sécurité > Performance > Optimisation > Coût en tokens** — arbitrage lexicographique : un
objectif n'est jamais sacrifié au profit d'un objectif de rang inférieur. La v0.4.0 consigne
cette hiérarchie comme **invariant de révision** (D19) : aucune révision future du
protocole ne peut la modifier sans invalider explicitement le protocole entier — pas
l'ordre, pas les rangs, pas la non-compensation.

| Objectif | Signification concrète | Métrique de validation |
|---|---|---|
| Sécurité | Sûreté mémoire validée par oracle, intégrité carte ↔ binaire, durcissement au chargement | 0 corruption détectée par l'oracle ; tout échec de verrou bloque la session ; échec de vérification au lancement = arrêt propre |
| Performance | 100 % code machine natif, zéro abstraction intermédiaire entre l'écriture et l'exécution | Comparaison par bloc scellé face à une référence compilée (clang -O2 ou équivalent du profil) |
| Optimisation | Descente à l'ISA sur les hot paths identifiés par profilage — jamais sans mesure (R11) | Gain mesuré et journalisé pour chaque bloc optimisé |
| Coût en tokens | Édition ciblée via la carte, jamais de lecture intégrale du binaire | Budgets par type d'édition (§ 12) |

### 1.2 Périmètre et non-objectifs

Cinq non-objectifs posés d'emblée. Premièrement, TRIADE ne prétend pas remplacer les
langages dans l'industrie : c'est une architecture de laboratoire, conçue pour être validée
sur une application réelle complète. Deuxièmement, la furtivité face aux EDR n'est pas
recherchée : l'outil cible est un utilitaire de pentest destiné à des tests autorisés en
environnement de laboratoire, et les API du système sont appelées via les interfaces
standards du profil. Troisièmement, l'universalité revendiquée est structurelle mais
progressive : chaque profil de cible doit être instancié et validé (jalons M6 et M7) avant
d'être déclaré supporté — le protocole ne promet pas la portabilité, il la vérifie.
Quatrièmement, aucune couche d'abstraction à l'exécution — bytecode portable, machine
virtuelle, traduction à la volée — n'est introduite par la présente révision ni ne le sera :
elle trahirait la fonction objectif Performance (rejet consigné, D14). Cinquièmement, la
couche de gouvernance validée par la démonstration RoomEq (spécifications avant code,
vérifie-puis-écrit, cristallisation) et le cœur natif du protocole (notation, verrou
cryptographique sur octets, patch à chaud) restent des niveaux de preuve distincts : les
jalons M0 à M7 demeurent la charge de validation du cœur natif.

### 1.3 Ce que change la v0.4.0

Dix-sept évolutions, toutes tracées dans la correspondance du § 17 et dans le journal des
versions (§ 19), toutes rattachées aux décisions D19 à D24 : normalisation de la couche I
(§ 2), taxonomie des défauts de contrat non écrit (§ 3), traçabilité I ↔ C ↔ B ↔ tests
(§ 4.2), norme de fragmentation et localisation par intention (§ 7, § 12), R10 renforcée
et R11 nouvelle (§ 6), suite de conformité par profil et parité inter-profils (§ 8),
pré-versions de cristallisation (§ 9), reverse-specs (§ 10), journal d'optimisation
(§ 11), modèle de menace étendu (§ 13), journal des décisions normalisé et tableau de bord
de conformité (§ 15). Aucune règle existante n'est affaiblie ; aucune couche n'est ajoutée
à l'exécution ; la hiérarchie de la fonction objectif est inchangée.

### 1.4 Ce que change la v0.5.0

Huit évolutions, toutes tracées dans la correspondance (§ 17.3) et le journal des versions
(§ 19), toutes rattachées aux décisions D26 à D45 : la validation terrain devient une
couche de vérification normée — boucle d'évidence, journal d'exécution, instrumentation
contractualisée, diff chirurgical (§ 8.4) ; la taxonomie des défauts s'étend des classes T
(contrat non écrit) aux classes X — défauts invisibles à l'émulation, huit classes nommées
par la campagne M2 (§ 8.5) ; l'état des jalons est constaté — M0, M1 et M2 franchis sur
validations terrain Windows 11, balises finales 0.2.0 et 0.3.0 posées (§ 16) ; le budget
de localisation est corrigé à 64 tokens (D31) et les budgets affichent leurs valeurs
mesurées (§ 12, § 15.2) ; les volumes d'oracle effectifs sont consignés ; les preuves
terrain sont archivées brutes avec leurs empreintes ; le corpus de démonstration (huit
itérations instrumentées) devient l'occurrence de référence de la méthode ; le jalon M3
est ouvert — contrats renforcés sur entrées non fiables et fuzzing à propriétés (D45).
Aucune règle n'est modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de
la fonction objectif est inchangée.

### 1.5 Ce que change la v0.5.1

Un composant nouveau et deux constats, tous tracés dans la correspondance (§ 17.5) et le
journal des versions (§ 19), rattachés à la décision D75 : le **coffre-fort des phrases
maîtresses** — conteneur chiffré TRIADE-CF1 centralisant toutes les phrases maîtresses
par projet, sur la pile cryptographique de la carte au repos (Argon2id aux planchers,
HKDF à contexte dédié, XChaCha20-Poly1305), doté d'un autotest de falsification et de
règles d'export/import (§ 15.3, FORMAT_CARTE § 11) ; l'état des jalons est constaté —
M3 franchi le 28 octobre 2026 sur la campagne million (D72), la conformité permanente
(D73) et le scellage de la balise finale 0.4.0 (D74) ; le modèle de menace gagne la ligne
du vol du coffre-fort (§ 13.1). Aucune règle n'est modifiée ; aucune couche n'est ajoutée
à l'exécution ; la hiérarchie de la fonction objectif est inchangée.

### 1.6 Ce que change la v0.5.2

Une évolution de discipline, tracée dans la correspondance (§ 17.6) et le journal des
versions (§ 19), rattachée à la décision D81 : la **phrase de contrôle du coffre-fort
passe sous garde durable** — dès sa production (init, rotation, changement), elle est
sauvegardée dans le dépôt git (commit dédié, push GitHub, miroir du coffre Drive par le
hook) et au racine du coffre Drive AVANT toute autre action de la session ; le fichier
`PHRASE-CONTROLE-COFFRE.txt` (phrase seule sur une ligne, lisible tel quel par
`--phrase-fichier`) EST la remise — l'affichage unique de cérémonie (D27/D30) cesse
d'être le canal de survie. Le constat fondateur : la rotation D80 avait produit une
phrase neuve dont la remise prévue en fin de tour n'a jamais eu lieu — la session
d'exécution est morte avant (pannes d'infrastructure récurrentes, quatre réinitialisations
et une interruption de session déjà consignées) — et la phrase ne vivait plus que dans le
bac à sable éphémère : un décès d'infra de plus et le coffre entier devenait
indéchiffrable à jamais. L'arbitrage est consigné : le risque de PERTE (vécu, répété) est
jugé supérieur au risque d'EXPOSITION (URL non devinable) ; le modèle de menace (§ 13.1)
en tire la conséquence honnête — la confidentialité des phrases au repos repose désormais
sur le contrôle d'accès au dossier du coffre Drive, la mitigation première devient la
restriction du partage par lien, et une phrase entrée dans l'historique git y demeure à
vie : on ne compte plus sur sa confidentialité, la rotation reste le remède. Aucune règle
n'est modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de la fonction
objectif est inchangée.

## 2. La couche I : format normalisé des spécifications

La v0.3 décrivait la couche I comme « contrats légers : signatures typées, pré et
post-conditions, invariants » (D3), sans en fixer le gabarit — la légèreté demeure, la
structure devient normative (D19). Une spécification I n'est pas un document libre :
c'est un artefact diffable dont la structure conditionne la vérification. La démonstration
RoomEq en a fixé la pratique (44 spécifications, une par module, écrites avant le code) ;
la v0.4.0 en fait la règle.

### 2.1 Identifiants stables

Chaque spécification reçoit à sa création un identifiant `<DOM>-<NN>` : un domaine parmi
une liste figée par projet (dsp, eq, calibration, audio, io, app, installateur, securite,
outils…) et un numéro séquentiel à deux chiffres. L'identifiant est immuable et jamais
réutilisé ; un module supprimé laisse son identifiant vacant à jamais. C'est l'équivalent
exact, côté intention, de l'adresse stable côté binaire (R7) : les références croisées —
dépendances, carte, tests — ne cassent jamais. Le couple (identifiant, révision) est la
clé de traçabilité du § 4.2.

### 2.2 Gabarit obligatoire

```
<DOM>-<NN> · <nom court> · révision <R>
Intention : <une phrase — le pourquoi>
Contrat :
  pre  : P1…Pn    (préconditions numérotées, une phrase chacune)
  post : Q1…Qn    (postconditions numérotées)
  inv  : I1…In    (invariants)
Échecs :
  E1 : <condition> → <sanction nommée : exception | arrêt propre | repli documenté>
Vecteurs :
  V1 : <vecteur doré | propriété différentielle | test de rejet>
Fixtures    : <références aux fixtures contractuelles partagées, le cas échéant>
Provenance  : écrite-avant-code | reverse-spec de <binaire scellé @ tag>
Décisions   : <Dxx…>
```

Sept blocs, tous obligatoires — les échecs et vecteurs ne peuvent être vides que pour un
module sans effet observable, situation rare à justifier dans le champ Intention. Trois
règles de rédaction conditionnent la diffabilité exigée par R2 : **une exigence par phrase
numérotée** (le diff montre exactement quelle exigence change) ; **aucune connaissance
dupliquée** (ce qui est écrit dans une spécification n'est pas réécrit dans une autre —
renvoi par identifiant, sinon défaut T5) ; **chaque pre/post/invariant relie au moins un
vecteur** (une exigence invérifiable est une exigence mal formulée).

La provenance distingue les spécifications écrites avant le code — le cas normal, exigé par
R2 — des reverse-specs (§ 10), extraites de binaires scellés hérités.

### 2.3 Révision et cycle de vie

La révision R s'incrémente à chaque changement du contrat : postcondition modifiée, cas
d'échec ajouté, vecteur étendu. Une évolution qui rompt un contrat existant ne modifie pas
la spécification — elle en crée une nouvelle, l'ancienne étant dépréciée avec renvoi :
miroir exact du cycle de vie des blocs (FORMAT_CARTE § 6). Les appelants dépendent du
couple (identifiant, révision) ; la carte porte ce couple dans chaque entrée.

### 2.4 Fixtures contractuelles partagées

Quand plusieurs consommateurs se lient au même contrat externe — sortie d'un outil système,
format de fichier, API distante — les échantillons qui définissent ce contrat (fixtures)
appartiennent à la spécification, pas aux consommateurs. Le champ Fixtures référence un
jeu unique ; toute copie privée est un défaut de classe T5 (duplication). Le mécanisme est
né dans la démonstration RoomEq : l'installateur scellé et l'application recodée
partagent les fixtures de parsing de pnputil — le défaut historique qui a survécu à trois
versions vivait précisément de la duplication (trois copies divergentes du même contrat
implicite). Le partage élimine par construction la divergence des exemplaires.

## 3. Taxonomie des défauts de contrat non écrit

La classe de défauts que le protocole existe pour éliminer a un nom : **contrat non
écrit**. La v0.4.0 en fixe la taxonomie (D19), née de l'analyse des défauts historiques de
la démonstration RoomEq — défauts d'application et défauts d'installateur confondus.

| Classe | Définition | Détecteur typique | Verrou |
|---|---|---|---|
| T1 — valeur-seuil enfouie | Constante critique sans nom, sans justification, dupliquée ou non | revue ; oracle (comportement absurde sur entrée limite) | constante nommée + rationale dans la spec I |
| T2 — convention d'interface implicite | Structure ou ABI déclarée de mémoire, hors contrat | échec système nommé à l'exécution | contrat typé + invariant de taille testé |
| T3 — dépendance à l'hôte | Comportement dépendant de l'OS ou des paramètres d'exécution | tests multi-plateformes | contrat indépendant de l'hôte, union fixée |
| T4 — parsing de surface fragile | Analyse de libellés localisés ou volatils | fixtures multi-langues | fragments indépendants des libellés + fixtures partagées |
| T5 — contrat dupliqué | Même connaissance codée en N exemplaires qui divergent | diff des exemplaires | source unique : spec I + fixtures |
| T6 — garantie non testée | Comportement critique sans vecteur de rejet | revue de couverture des vecteurs | cas d'échec nommé + test de rejet |

Deux règles d'usage. D'abord, tout défaut corrigé est **classé dans cette taxonomie** au
journal des décisions du projet — la métrique « défauts ouverts par classe » du tableau de
bord (§ 15.2) en dérive. Ensuite, la taxonomie sert de liste de contrôle de rédaction :
chaque bloc du gabarit § 2.2 verrouille au moins une classe (Échecs verrouille T6, Fixtures
verrouille T4/T5, le contrat typé verrouille T1/T2/T3).

La démonstration fournit les occurrences de référence : le seuil de détection 8 non justifié
est T1 + T6 (le bruit seul passait) ; la structure `SP_DEVINFO_DATA` de 424 octets au lieu
de 32 est T2 (échec 0x6F8, deux copies) ; la sanitisation de noms de fichiers dépendante de
l'OS hôte est T3 ; le parsing de pnputil sur libellés français est T4 + T5 (trois copies) ;
le seuil dupliqué dans le message d'erreur est T5. Chacun est devenu un contrat nommé, un
cas d'échec et un test — la conversion est documentée dans la démonstration et sa méthode
est désormais la règle.

## 4. Architecture : les trois couches

L'architecture repose sur une séparation stricte entre ce que l'artefact contient, ce que
l'agent manipule et ce que le destinataire reçoit. Le diff d'intention descend de I vers C,
le verrou croisé relie C et B dans les deux sens, et la couche B seule quitte le
laboratoire. **Aucune couche n'est optionnelle** — la v0.4.0 le consigne comme propriété
normative, pas comme constat : privé de I, le système perd son ancrage sémantique ; privé
de C, l'agent devient aveugle ; privé de B, il n'y a plus rien à exécuter. Toute
implémentation qui livrerait B sans I et C à jour viole R1 ; toute évolution qui
contournerait C pour éditer B directement viole R3 et la boucle (§ 7).

### 4.1 Les trois couches

| Couche | Contenu | Visibilité | Rôle |
|---|---|---|---|
| I | Spécifications normalisées (§ 2) : contrats typés pré/post, invariants, cas d'échec, vecteurs de vérification | Privée | Compression de l'intention — le quoi et le pourquoi |
| C | Index des blocs, adresses, signatures, preuves, manifestes de build, traçabilité | Privée, signée, chiffrée | Unique interface de développement de l'agent |
| B | Code machine scellé, padding inter-blocs, checksums runtime | Livrée | Le comment — exécution pure, sémantiquement muette |

Depuis la v0.3, la séparation des couches croise une seconde dimension : la cible. La
couche I est **indépendante de la cible** — un contrat s'écrit une fois, ses types abstraits
(`usize`, alignements) étant paramétrés par le profil. La couche B est **par profil** :
chaque plateforme visée possède son jeu d'octets scellés. La couche C indexe l'ensemble :
chaque entrée porte son profil, et frag-bld organise les empreintes par profil. Un même
contrat I est ainsi instancié par autant de blocs machine que de profils supportés — c'est
la condition de possibilité de la portabilité sans duplication de l'intention.

Quatre invariants structurels, vérifiés à chaque cycle de build — leur violation est un
refus de build : B n'est jamais nu (R1) ; les adresses exposées sont stables (R7, par
profil) ; la signature couvre la carte entière (R9) ; B est auto-vérifiant au chargement
(R10, renforcée en v0.4.0).

### 4.2 Traçabilité I ↔ C ↔ B ↔ tests

La v0.4.0 rend obligatoire une chaîne de traçabilité complète (D24). Chaque entrée de la
carte référence quatre maillons :

| Maillon | Contenu | Porté par |
|---|---|---|
| I | spécification (identifiant + révision) | couche I |
| C | entrée de localisation + contrat embarqué | frag-loc, frag-con |
| B | bloc(s) instancié(s) + empreinte(s) par profil | frag-bld, binaire |
| tests | vecteurs exécutés + verdict du dernier cycle | frag-prf, suites |

Trois propriétés, contrôlées mécaniquement par la **commande d'audit de traçabilité** :
aucune spécification sans entrée de carte (l'exception visible étant la reverse-spec en
statut « prête », § 10) ; aucun bloc scellé sans spécification référencée ; aucun
vecteur orphelin (rattaché à une exigence numérotée du gabarit § 2.2). Une chaîne
incomplète est un refus de build — au même titre qu'un binaire nu. La traçabilité est la
condition de l'audit par des tiers : elle permet de répondre à « quelle exigence ce bloc
implémente-t-il, et quel test la défend ? » sans lecture du binaire.

## 5. La carte (couche C)

La carte est le cœur opérationnel du protocole : c'est elle qui rend le binaire navigable
pour l'agent, qui porte les preuves et qui concentre la valeur intellectuelle du projet.
Elle est compacte (coût en tokens, § 12), intègre (verrou croisé) et résiliente face à la
compromission (sharding et chiffrement). Sa spécification détaillée — en-tête normalisé,
quatre fragments, format d'entrée, procédure du verrou, cycle de vie, budgets, export de
continuité, re-cryptage — fait l'objet de `docs/FORMAT_CARTE.md`, mis à jour avec la
présente révision : l'en-tête porte `version=0.4.0`, chaque entrée de bloc porte le champ
de traçabilité `spec=<DOM>-<NN>:R` exigé par le § 4.2.

La carte est **autodescriptive** : un en-tête normalisé consigne la version du protocole,
la suite cryptographique retenue — `algo_hachage` (SHA-256 par défaut), `algo_signature`
(Ed25519 par défaut), `algo_chiffrement` (XChaCha20-Poly1305 par défaut), chacun modifiable
par le développeur dans les limites d'une liste blanche (D15) — et la liste des profils de
cible actifs. Les empreintes portées par frag-bld sont préfixées par leur algorithme
(`sha256:ab12…`) : n'importe quel agent, présent ou futur, sait vérifier le verrou croisé
sans connaissance extérieure à la carte.

## 6. Règles du protocole v0.4.0

R1 à R7 proviennent de la v0.1 ; R8 à R10 de la v0.2 ; **R10 est renforcée et R11 ajoutée
par la v0.4.0**. Les règles sont peu nombreuses, vérifiables mécaniquement et sanctionnées
par des effets concrets — refus de build, refus de commit ou blocage de session — plutôt
que par des recommandations. Aucune règle existante n'est affaiblie : les énoncés de R1 à
R9 sont repris à l'identique, celui de R10 est un sur-ensemble strict de la version v0.3.

| # | Règle | Énoncé | Violation et sanction |
|---|---|---|---|
| R1 | Jamais de binaire nu | Tout artefact B est accompagné de I et C à jour | Build refusé |
| R2 | Intention d'abord | Toute modification commence par un diff sur I | Édition rejetée par la boucle |
| R3 | Balisage obligatoire | Chaque bloc est décrit dans C | Build refusé |
| R4 | Patch à contrat stable | Le remplacement préserve signature et contrats ; les appelants ne sont jamais invalidés | Échec de vérification |
| R5 | Vérifie-puis-écrit | Aucun commit sans oracle, vecteurs dorés et round-trip | Commit impossible |
| R6 | Cristallisation | Dix vérifications réussies rendent le bloc immuable ; le modifier exige la procédure lourde | Nouvelle version du bloc |
| R7 | Adresses stables | Les points d'entrée sont garantis par padding ; patcher ne déplace rien | Re-liage forcé — interdit |
| R8 | Verrou croisé | Empreintes des blocs et signature de la carte vérifiés avant chaque édition | Session bloquée |
| R9 | Carte signée obligatoire | L'agent refuse toute carte non signée | Refus de démarrage |
| R10 | Échec contrôlé intégré (renforcée) | Au lancement — avant toute entrée dans le chemin d'exécution — l'artefact vérifie (a) les checksums de ses blocs scellés, (b) la signature du manifeste de build couvrant le code et les données embarquées, (c) la monotonie de version (anti-rollback : tout état antérieur à la version minimale acceptée est refusé), (d) la conformité minimale de l'environnement au profil. Tout écart = arrêt propre immédiat ; aucun chemin d'exécution dégradé n'existe (fail-closed explicite) | Arrêt avant tout effet |
| R11 | Optimisation mesurée (nouvelle) | Toute optimisation exige un hot path identifié par mesure, une mesure avant/après consignée au journal d'optimisation (§ 11) et un contrat stable (R4). L'optimisation prématurée — sans hot path identifié ni mesure — est interdite : la demande est refusée et consignée | Refus de commit |

Quatre précisions. R4 signifie qu'un bloc remplaçant honore les contrats publiés de son
prédécesseur — mêmes signatures, mêmes pré et post-conditions, mêmes invariants visibles —
condition de possibilité du patch à chaud. R7 s'entend **par profil** : les adresses sont
stables au sein du binaire de chaque profil ; rien n'impose qu'elles coïncident entre
profils. R1, précisée par D16, interdit de livrer la carte **avec l'artefact** ou à des
tiers — elle n'interdit pas au développeur de détenir, sauvegarder et transférer son propre
état de développement : c'est précisément l'objet de l'export de continuité (FORMAT_CARTE
§ 8). R10 renforcée (D20) étend le fail-closed de la v0.3 — checksums au lancement — en
un contrôle intégré à quatre volets ; la vérification est strictement **locale** (aucune
dépendance réseau au chargement : l'outil doit échouer proprement hors ligne), et la
politique anti-rollback précise (registre des versions acceptées, stockage du plancher)
appartient au profil de cible.

## 7. Boucle de mise à jour

La boucle de mise à jour est la seule voie par laquelle le logiciel évolue. Elle se déroule
en sept étapes réparties en deux phases — l'édition, puis la validation et le commit —
séparées par un point de non-retour : rien n'est écrit dans le binaire avant que l'oracle
n'ait rendu son verdict.

| N | Étape | Entrées | Sorties | Règles |
|---|---|---|---|---|
| 1 | Diff d'intention | Requête de changement, couche I | Diff minimal sur I | R2 |
| 2 | Localisation par intention | frag-loc, diff I | Liste des blocs impactés | R3 |
| 3 | Verrou croisé | frag-bld, binaire | Verdict go / no-go | R8, R9 |
| 4 | Régénération ciblée | frag-con, notation du bloc | Octets candidats | R4, R7, R11 |
| 5 | Vérification | Candidats, oracle, vecteurs dorés | Verdict, journal | R5 |
| 6 | Commit atomique | Verdict favorable | Patch B, carte à jour, scellage | R1 |
| 7 | Cristallisation | Compteur de vérifications | Bloc immuable | R6 |

**Localisation par intention (norme v0.4.0).** L'étape 2 porte désormais son nom entier :
la localisation est **dérivée du diff d'intention** par l'index de la carte — jamais par
balayage du binaire, jamais par recherche de motif dans les octets. Un diff qui ne localise
aucun bloc est une erreur de spécification à corriger dans I, pas une licence de scan ;
un balayage serait d'ailleurs une violation du budget (§ 12) et de R3. C'est la
formalisation du principe « l'agent ne lit jamais le binaire en entier », appliqué à
l'étape la plus fréquente de la boucle. La précision de localisation — bon bloc identifié
du premier coup — reste l'indicateur de santé mesuré dès M0 (cible 95 %).

### 7.1 Patch à chaud — exemple du profil primaire

Le patch à chaud — modifier un logiciel en cours d'exécution — est l'un des deux objectifs
fondateurs du projet avec la performance. Le mécanisme exact est **spécifié par chaque
profil de cible** (taille minimale de bascule atomique, procédure d'invalidation du cache
d'instructions) ; ce paragraphe décrit l'instanciation du profil primaire x86-64. La
méthode contourne la cohérence du cache d'instructions et l'atomicité de la bascule en
n'écrivant jamais un bloc pendant qu'il s'exécute : le nouveau bloc est d'abord écrit dans
une zone de croissance libre ; ensuite, et seulement ensuite, un trampoline de 12 à 16
octets est installé à l'ancien point d'entrée et basculé par une écriture alignée unique,
atomique pour le processeur.

```
; trampoline de bascule atomique (aligné sur 16 octets)
; forme courte : saut relatif 32 bits
  E9 xx xx xx xx                ; jmp rel32 -> nouveau bloc
; forme longue : saut absolu 64 bits
  48 B8 xx xx xx xx xx xx xx xx ; mov rax, addr_new
  FF E0                         ; jmp rax
```

L'ancien trampoline est conservé : le rollback copy-on-write de l'étape 5 consiste à
rebasculer vers lui, et la carte référence les deux versions tant que la nouvelle n'a pas
atteint son seuil de cristallisation. Les adresses stables garantissent qu'aucun appelant
ne référence l'intérieur d'un bloc : seuls les points d'entrée — promis par R7 — sont
susceptibles d'être trampolinés, et la table de ces points est close et vérifiée par le
verrou croisé. Le critère de sortie du jalon M2 est précisément ce scénario : remplacer le
bloc d'écho d'un serveur TCP pendant qu'il traite des connexions, sans interruption de
service et avec rollback démontré.

## 8. Stratégie de vérification

Supprimer le compilateur, c'est perdre les filets de sécurité qu'il tendait gratuitement :
vérification de types, initialisation, analyse de flot. La stratégie de vérification
reconstruit une confiance équivalente — voire supérieure — sans réintroduire de couche de
traduction dans l'artefact. Elle repose sur trois piliers, complétés en v0.4.0 par la
couverture des vecteurs, la suite de conformité par profil et la parité inter-profils
(§ 8.1 à § 8.3), puis en v0.5.0 par la validation terrain normée (§ 8.4) et la taxonomie
des défauts invisibles à l'émulation (§ 8.5).

**L'oracle éphémère** : implémentation de référence de chaque bloc — triviale,
volontairement lente, écrite dans un langage sûr et dérivant directement de la couche I. Il
est généré au début de chaque session, utilisé pour des tests différentiels par propriétés,
puis détruit : jamais livré, jamais archivé dans la carte ; seuls ses vecteurs de test
dorés — hachés — y survivent. Le protocole de test est différentiel : l'oracle et le bloc
machine reçoivent des entrées aléatoires contraintes par les pré-conditions du contrat, et
leurs sorties sont comparées octet par octet. Volume de référence : douze mille cas par
bloc critique. Trois propriétés rendent l'oracle fiable : il dérive de I et non de B (il ne
peut pas hériter d'un bug du code machine) ; il est régénéré à chaque session (jamais en
désaccord avec les contrats courants) ; sa régénération coûte moins que le diagnostic d'une
corruption découverte après scellage. L'oracle étant dérivé de I — couche indépendante de
la cible — le **même** oracle valide les blocs de tous les profils : la portabilité ne
divise pas le coût de vérification, elle le mutualise.

**Le round-trip de notation** : chaque bloc assemblé par le moteur de notation du profil
est désassemblé par le vérificateur correspondant, et les instructions obtenues sont
comparées à la notation d'origine. Tout désaccord — une instruction, un opérande, une
taille d'encodage — est un échec de build. Ce contrôle à coût quasi nul attrape la classe
d'erreurs la plus insidieuse : l'écart silencieux entre ce que l'agent croit avoir écrit et
les octets réellement produits. La nuance capitale est que la notation n'est pas un
compilateur — aucune optimisation, aucune réécriture ne s'intercale entre l'écriture et les
octets (principe WYSIWYG).

**La cristallisation** ferme la boucle économique : plus un bloc fait ses preuves, moins il
coûte à vérifier, ce qui libère le budget pour les blocs jeunes et les zones actives. La
chaîne de confiance du scellage résume le parcours d'une preuve : verdict de l'oracle →
vecteurs dorés hachés dans frag-prf → empreinte du bloc dans frag-bld → signature de la
carte entière → immuabilité à dix vérifications.

### 8.1 Vecteurs de vérification

Les vecteurs exigés par le gabarit § 2.2 sont de trois espèces : **vecteurs dorés**
(entrées/sorties de référence, conservés hachés dans frag-prf) ; **propriétés
différentielles** (invariants testés par l'oracle sur entrées aléatoires contraintes) ;
**tests de rejet** (les cas d'échec E1…En du contrat, chacun matérialisé par un test qui
exige la sanction nommée). Exigence de couverture : chaque exigence numérotée du contrat
(pre, post, inv) et chaque cas d'échec relie au moins un vecteur — la commande d'audit de
traçabilité (§ 4.2) vérifie ce maillon.

### 8.2 Suite de conformité par profil

Chaque profil embarque une **suite de conformité** vérifiant ses sept éléments
constitutifs (D22) :

| # | Élément du profil | Contrôle de la suite |
|---|---|---|
| 1 | ISA et types | tailles, alignements, boutisme constatés = déclarés |
| 2 | ABI d'appel | appels et retours conformes ; volatilité ; shadow space ou zone rouge |
| 3 | Format d'exécutable | en-têtes valides ; protections actives constatées (DEP/NX, ASLR/PIE, CFI/CFG) |
| 4 | Interface système | résolution des imports ou syscalls ; contrat d'erreurs |
| 5 | Patch à chaud | bascule atomique et invalidation du cache d'instructions démontrées |
| 6 | Notation | round-trip 100 % sur le corpus d'instructions du profil |
| 7 | Granularité et padding | adresses stables après patch (R7) |

Un profil sans suite verte n'est pas déclarable supporté — un profil incomplet est refusé
exactement comme un build sans carte (D14). La suite est un livrable obligatoire de
l'instanciation d'un profil et le critère d'acceptation des jalons M6 et M7. Elle est
exécutée à chaque cristallisation de version rc et finale (§ 9) sur le profil concerné.

### 8.3 Parité inter-profils à contrat constant

Deux profils P1 et P2 sont **paritaires** pour le contrat σ si et seulement si : (1) σ est
instancié sur les deux profils depuis la même spécification I, à la paramétrisation près ;
(2) l'oracle — dérivé de I, mutualisé — est vert sur les deux ; (3) les verdicts des
vecteurs de vérification de σ sont équivalents sur les deux profils ; (4) les différences
de profil sont documentées dans frag-con de chaque bloc. La parité se **vérifie par
exécution**, jamais par déduction : c'est le critère de sortie de M6 (inter-OS, à ISA
constante) et M7 (inter-ISA). Aucune couche d'abstraction n'est introduite pour l'obtenir —
un bytecode portable trahirait la fonction objectif Performance (rejet consigné, D14 et
§ 17.2).

### 8.4 La validation terrain — la boucle d'évidence

La v0.5.0 élève la validation terrain au rang de couche de vérification normée (D43). Le
principe est né d'un constat structurel : l'oracle différentiel exécute le binaire contre
un **modèle** de l'environnement — chargeur, ABI, sémantique des API, protections
mémoire. Un binaire peut donc être exact au sens du round-trip, intègre au sens de la
porte R10, conforme au sens de la suite du profil, vert au sens de l'oracle — et mourir
au premier appel sur machine réelle, parce que le modèle était plus pauvre que la
réalité. Les jalons M1 et M2 en ont fourni la preuve expérimentale : huit classes de
défauts ainsi invisibles (§ 8.5) n'ont été révélées que par l'exécution terrain.

La boucle d'évidence comporte cinq éléments normés :

1. **Le journal d'exécution** — l'artefact livré écrit ses preuves au fil de l'eau
   (fichier à côté de l'exécutable, ligne par ligne). La règle d'honnêteté est absolue :
   une ligne n'est écrite qu'après la vérification de l'étape qu'elle atteste (memcmp
   exact) — une ligne présente vaut preuve ; la dernière ligne visible localise toute
   mortalité à l'intervalle près.
2. **La lecture asymétrique** — le terrain retourne son verdict par un canal à faible
   bande passante : le journal (éventuellement complété d'une capture). L'atelier
   n'exige du terrain que ce document, jamais un diagnostic : la charge d'analyse reste
   à l'agent.
3. **L'instrumentation contractualisée** — quand l'intervalle de mortalité reste
   aveugle, l'itération suivante embarque des sondes de trace aux frontières (D40) :
   elles journalisent des faits (positions d'exécution, retours vérifiés), jamais un
   succès non prouvé ; leur retrait après constat vert est promis dans la spécification
   (D43 a honoré la promesse) et vérifié par l'oracle — le journal nominal redevient
   exactement sa séquence de preuves, toute ligne parasite est un échec.
4. **Le diff chirurgical** — chaque itération terrain ne modifie que les blocs révisés ;
   l'audit d'itération vérifie mécaniquement qu'aucun octet hors des zones autorisées
   (blocs révisés, chaînes, version, sommes) n'a bougé — l'héritage scellé reste
   octet-identique (R7).
5. **L'archive brute** — chaque journal terrain est archivé tel quel (octets d'origine,
   encodage et CRLF compris) avec son empreinte : la preuve est le document, pas son
   résumé.

Le protocole est ensuite économique : huit lectures de journal ont suffi à nommer huit
classes de défauts en deux jours (demo.1 à demo.8), et le dernier diagnostic a été obtenu
sans run supplémentaire — par lecture statique des octets appuyée sur les preuves
accumulées (D42). La contrepartie est la garantie de progression : chaque défaut nommé
devient un vecteur de falsification permanent de l'oracle — le modèle d'environnement
s'enrichit de chaque lecture terrain et ne peut plus régresser en silence.

### 8.5 Taxonomie étendue — les défauts invisibles à l'émulation (X1–X8)

Les classes T1–T6 (§ 3) classent les défauts de contrat non écrit : lisibles dans la
spécification, corrigeables en écrivant le contrat. La campagne M2 a révélé une seconde
famille, structurellement différente : des défauts dont ni la spécification, ni la
notation, ni le round-trip, ni l'oracle ne parlent — parce que le modèle d'environnement
de l'oracle était, sur un point précis, plus pauvre que le système réel. La v0.5.0 en
fixe la taxonomie (D35–D43) :

| Classe | Décision | Dimension du modèle défaillant | Défaut de référence | Garde permanente |
|---|---|---|---|---|
| X1 | D35 | sémantique du chargeur | `FirstThunk` ≠ slots appelés : le chargeur réel résout ailleurs que le code n'appelle — `call 0` au premier appel réseau | verrou « chargeur réel » : FirstThunk = slots appelés, contrôlé au build et par l'oracle |
| X2 | D36 | lecture de structure | `RECT.top` lu comme largeur : spécification juste, octets faux — bloc jamais exécuté, shim témoin muet | coquille entière exécutée + invariant géométrique + falsification de l'octet |
| X3 | D37 | canal de vérité | jumeau silencieux : le journal fichier vivait, l'écran restait vide — le défaut vivait dans la spécification elle-même | miroir universel : chaque ligne écrite écran puis fichier, les deux canaux contrôlés |
| X4 | D38 | ABI caller-saved | dimensions relues dans des registres volatils après l'appel : un retour de syscall écrit RFLAGS dans r11 | clobber des volatiles à chaque retour simulé + falsification |
| X5 | D39 | protections mémoire | phase de patch `PAGE_READWRITE` sans bit execute : DEP permanent x64, le fetch suivant faute | le shim applique les permissions réelles + falsification 0x40 → 0x04 |
| X6 | D40 | écart émulation/terrain | défaut latent qu'aucune exécution n'avait déclenché : l'audit exhaustif était vert | sondes de trace aux frontières (§ 8.4), instrumentation contractualisée |
| X7 | D41 | obligations ABI de l'appelant | zone d'accueil msx64 absente : l'appelé (/homeparams) écrit sur l'adresse de retour — le ret saute à 0x700 | shim /homeparams + audit systémique des sites d'appel + falsification |
| X8 | D42 | état hérité | section critique exigée par un bloc scellé (P5) mais initialisée par un bloc orchestrateur retiré de l'hôte | shims à état + exécution réelle du bloc consommateur + contrôle post-run |

Trois règles d'usage, miroir de celles de la taxonomie T. Premièrement, tout défaut
terrain corrigé est classé T ou X au journal des décisions — la métrique « défauts
ouverts par classe » du tableau de bord (§ 15.2) couvre désormais les deux familles.
Deuxièmement, chaque classe X est gardée par une falsification : réintroduire le défaut
doit faire échouer l'oracle — le modèle s'enrichit mais ne régresse jamais en silence.
Troisièmement, la taxonomie est ouverte : une neuvième classe sera nommée X9 avec sa
décision, jamais dissimulée dans un correctif muet.

La lecture académique : un oracle différentiel valide la conformité d'un artefact à un
modèle ; la validation terrain valide le modèle lui-même. Les deux couches sont
complémentaires, non redondantes — l'oracle couvre l'espace des entrées à coût nul, le
terrain couvre l'espace des environnements au coût d'un run. Le protocole exige les
deux : R5 (vérifie-puis-écrit) pour la première, la boucle d'évidence (§ 8.4) pour la
seconde.

## 9. Cristallisation et pré-versions

La v0.3 connaissait les balises de version sans en fixer la sémantique ; la démonstration
RoomEq a inventé en cours de route la pré-version `-dev.N` pour distinguer « vérifié par
l'oracle » de « validé sur le terrain ». La v0.4.0 formalise le schéma complet (D23) :

| Segment | Signification | Conditions d'ouverture |
|---|---|---|
| `X.Y.Z-dev.N` | pré-version de développement | oracle vert (R5) ; construction 0 erreur / 0 avertissement ; jamais validée terrain ; usage interne |
| `X.Y.Z-rc.N` | candidate à la validation | dev + suite de conformité du profil verte (§ 8.2) + critères du jalon courant ; soumise à la validation terrain |
| `X.Y.Z` | version finale | validation terrain consignée au journal des décisions ; balise immuable |

Trois règles gouvernent le schéma. **Monotonie** : pour un même triplet X.Y.Z,
dev.N < rc.N < version finale ; la version minimale acceptée alimente le contrôle
anti-rollback de R10. **Immuabilité** : une balise posée n'est jamais déplacée ni
supprimée ; un défaut découvert après cristallisation se corrige en `X.Y.Z+1` à contrat
stable (R4) — l'échec est honoré, pas effacé. **Progression de contrat** : une évolution
qui rompt un contrat publié passe par `X.(Y+1).0` avec révision explicite de la
spécification I concernée (§ 2.3). Le schéma généralise la séquence vécue par RoomEq
(v3.0.0-dev.1 → v3.0.0 → v3.0.1 → v3.0.2 : deux échecs d'intégration continue honorés puis
corrigés en patchs à contrat stable), qui demeure l'occurrence de référence.

## 10. Binaires scellés hérités : reverse-specs

Un projet agent-first hérite presque toujours d'un patrimoine : binaires scellés, validés
sur le terrain, dont le code source existe mais dont les contrats ne sont écrits nulle
part. La v0.3 ne disait rien de ce cas — la démonstration RoomEq y a répondu par
invention, en écrivant les spécifications de l'installateur scellé v2.2.2 par
rétro-ingénierie (décision D11 du dépôt de démonstration, huit modules M-INS). La v0.4.0
officialise la pratique (D23).

**Définition.** Une *reverse-spec* est une spécification I extraite d'un artefact scellé
existant : le gabarit § 2.2 s'applique intégralement, avec deux particularités. La
**provenance** est `reverse-spec de <binaire scellé @ tag>` — elle identifie l'artefact
source et sa balise. Le **statut** est « prête » tant que la spécification n'a pas été
confrontée au comportement réel (fixtures issues de l'artefact, tests de discrimination) ;
il passe à « validée » lorsque les vecteurs ont tranché. Une reverse-spec ne modifie
jamais l'artefact scellé : elle le documente.

**Règles.** Premièrement, le recodage d'un binaire scellé ne peut partir que de sa
reverse-spec validée — jamais du code relu en séance, jamais d'une mémoire de session.
Deuxièmement, une reverse-spec en statut « prête » figure dans la traçabilité (§ 4.2) avec
son statut visible : l'exception est nommée, pas silencieuse. Troisièmement, la
rétro-ingénierie se fait par lecture ligne à ligne du code source scellé — la méthode est
déclarée dans la spécification, reproductible par un tiers. La reverse-spec étend la couche
I au patrimoine sans l'exiger de recoder : figer la connaissance avant de décider.

## 11. Optimisation : interdiction du prématuré et journal

La fonction objectif place l'optimisation au troisième rang — après sécurité et
performance, avant le coût en tokens — et l'assortit d'une condition : « descente à l'ISA
sur les hot paths identifiés par profilage ». La v0.4.0 en tire l'interdiction normative
(R11) et son instrument, le **journal d'optimisation** (D21) : l'optimisation sans hot
path identifié ni mesure est prématurée, donc interdite ; sa demande est refusée et
consignée — le refus motivé fait partie de la gouvernance, exactement comme les
alternatives rejetées du journal des décisions.

Format normalisé d'une entrée :

```
[OPT-NN] date · bloc/chemin · décideur
  hot path       : <identification + preuve de mesure (profilage, charge)>
  mesure avant   : <valeur, conditions, matériel>
  changement     : <description> · contrat stable : oui/non (R4)
  mesure après   : <valeur, conditions identiques>
  gain           : <× ou %> · décision : appliquée | refusée (motif)
  décision liée  : Dxx
```

Le journal est versionné avec la couche I ; toute entrée d'optimisation appliquée doit
précéder le commit du bloc optimisé (R11 sanctionne le commit, pas seulement
l'intention). L'entrée de référence est l'occurrence RoomEq : la demande d'« optimisation
maximale » a été honorée par la mesure — chaîne d'égalisation à 152× le temps réel, zéro
allocation par bloc — puis refusée en tant que transformation, faute de problème de
performance à corriger ; le tout consigné en une entrée unique (décision D15 du dépôt de
démonstration). La métrique « optimisations sans mesure » du tableau de bord (§ 15.2) doit
rester à zéro.

## 12. Coût en tokens : fragmentation, localisation, budgets

Le coût en tokens est le seul des quatre objectifs spécifique à l'ère agent-first. Il est
traité comme une contrainte d'ingénierie — budgets, mécanismes, instrumentation — toujours
subordonnée aux trois objectifs supérieurs : aucune économie de tokens ne justifie de
sauter une vérification.

**Fragmentation (norme).** La carte est fragmentée en quatre (frag-loc, frag-con, frag-prf,
frag-bld ; FORMAT_CARTE § 2), et la v0.4.0 pose la norme en trois volets : aucune opération
de la boucle n'exige la lecture de plus d'un fragment ; **aucune opération n'exige la
lecture intégrale du binaire** — la carte est l'unique index, le balayage est interdit
(§ 7) ; l'audit complet de la carte est une opération exceptionnelle, non budgétée,
journalisée. Le multi-profils n'alourdit pas la localisation : l'entrée de frag-loc porte
le profil, et l'instanciation d'un contrat sur un profil nouveau est budgétée comme un
ajout — la couche I, elle, n'est jamais dupliquée.

**Budgets par type d'opération** (désormais instrumentés — § 15.2 ; le budget de
localisation est amendé à 64 tokens par D31 : la mesure M1 a constaté 43 tokens sur le
gabarit canonique de la v0.4.0 lui-même, tokenizer BPE cl100k_base) :

| Opération | Fragments et données lus | Budget |
|---|---|---|
| Localiser un bloc | frag-loc — une entrée | 64 tokens max (D31) |
| Éditer simplement un bloc | frag-loc + frag-con du bloc + notation du bloc | 3 000 tokens max |
| Ajouter un bloc | frag-loc + frag-con + seuils frag-prf | 6 000 tokens max |
| Instancier un profil nouveau pour un contrat existant | I partagée + frag-con + notation du profil | 6 000 tokens max par bloc |
| Audit complet (rare) | Carte entière déchiffrée | Non budgété — opération exceptionnelle |

Indicateurs de santé : précision de localisation (cible 95 % au jalon M0), coût moyen
d'une édition simple (cible 5 000 tokens), taux de régression post-patch (cible zéro,
rollback exclu). Ces budgets, cibles de conception jusqu'à leur instrumentation, sont
mesurés depuis M1 (`m1/budgets_tokens.py`, tokenizer cl100k_base, mesure sur la carte
scellée et les sources réelles) ; le tableau de bord les affiche comme métriques
mesurées, avec leur écart.

## 13. Sécurité : modèle de menace et limites

Le principe directeur demeure : séparer l'obfuscation, qui protège la propriété
intellectuelle (le comment), du durcissement, qui protège l'exécution (le où ça casse).
La carte privée relève du premier ; la sûreté mémoire, les contrats et le fuzzing relèvent
du second. Conformément au principe de Kerckhoffs, la sécurité du système ne repose jamais
sur le secret de la carte : elle survivrait à sa divulgation.

### 13.1 Modèle de menace (étendu en v0.4.0, D20)

| Menace | Acteur | Cible | Contre-mesure | Résiduel |
|---|---|---|---|---|
| Rétro-ingénierie de l'IP | Concurrent, pirate | Binaire livré | Carte privée ; binaire sémantiquement muet ; variantes par build | Temps acheté — s'érode avec les LLM de décompilation |
| Empoisonnement de carte | Attaquant supply-chain | Fragments | Signature (algo de l'en-tête) ; refus de carte non signée ; verrou croisé (R8, R9) | Détecté — session bloquée |
| Corruption de carte (accidentelle) | Bit rot, panne de stockage | Fragments au repos | AEAD (intégrité par fragment) + signature + verrou croisé | Détecté au chargement — refus propre |
| Fuite de la carte | Initié, poste compromis | Fragments au repos | Chiffrement (algo de l'en-tête) ; sharding ; escrow | Perte partielle limitée à un fragment |
| Vol de l'export de continuité | Voleur, stockage cloud compromis | Conteneur exporté | Chiffrement intégral (phrase maîtresse + Argon2id) ; signature | Sans la phrase, indéchiffrable |
| **Vol du coffre-fort des phrases** | Voleur, stockage cloud compromis | Conteneur du coffre-fort (D75) ; depuis D81 la phrase de contrôle elle-même vit au coffre Drive et dans le dépôt (arbitrage PERTE > EXPOSITION) | Chiffrement intégral (Argon2id, contexte HKDF dédié, AEAD) ; écriture atomique 0600 ; mitigation première : restreindre le partage par lien du dossier (§ 15.3) | Confidentialité ramenée au contrôle d'accès du dossier ; une phrase commise en git y demeure à vie — on ne compte plus sur sa confidentialité, la rotation reste le remède |
| **Binaire altéré** | Attaquant local, fichier modifié | Artefact livré | Checksums par bloc + signature du manifeste au lancement (R10 a, b) | Détecté — arrêt avant tout effet |
| **Rollback non autorisé** | Rejeu d'une version ancienne vulnérable | Artefact, état | Monotonie de version signée, plancher anti-rollback (R10 c) | Détecté — refus |
| **Agent défaillant** | Hallucination, dérive hors périmètre | Processus de développement | R2 (intention d'abord) ; R5 (vérifie-puis-écrit) ; oracle dérivé de I ; budgets (§ 12) | L'erreur ne devient jamais permanente sans vérification |
| **Données embarquées modifiées** | Supply chain des données | Tables, profils, ressources livrés | Empreintes des données dans la carte ; vérification au lancement (R10 b) ; parité par hachage | Détecté — arrêt propre |
| **Environnement non conforme** | OS, ABI, protections inattendues | Exécution | Contrôles de conformité au profil au lancement (R10 d) ; fail-closed | Refus propre avant exécution |
| Fuzzing boîte noire | Attaquant externe | Runtime | Contrats, oracle, tests par propriétés, fail-closed | Indépendant du secret de la carte |
| Redistribution frauduleuse | Pirate | Binaire livré | Empreintes par build — canary trap | Fuite traçable à son destinataire |
| Instrumentation dynamique | Analyste | Exécution | Anti-debug léger par mesure de temps | Assumé — l'obscurité n'est pas la sécurité |

Les six menaces en gras sont les additions de la v0.4.0 ; toutes sont neutralisées par des
mécanismes **locaux et vérifiables** — la contre-mesure anti-rollback ne dépend d'aucun
service en ligne (le chargement doit échouer proprement hors ligne), et les vérifications
de R10 s'exécutent avant toute entrée dans le chemin d'exécution.

### 13.2 Limites assumées

La rétro-ingénierie est traitée comme un objectif d'économie, pas d'impossibilité : rendre
le coût de l'analyse supérieur à la valeur de ce qu'on obtient. Un binaire strippé, sans
structure ni symboles, dont chaque exemplaire diffère, coûte sensiblement plus cher à
analyser qu'un binaire compilé standard — mais les modèles de langage appliqués à la
décompilation progressent, et l'avantage doit être réévalué à chaque génération de
modèles. L'anti-debug reste léger et assumé : l'obscurité n'est pas la sécurité. La
furtivité face aux EDR est hors périmètre (§ 1.2) : un outil légitime par construction,
dont la transparence vis-à-vis du système est totale. Et la gouvernance du protocole a été
validée sur un cas unique (N = 1) — l'étude de cas RoomEq, dont les limites sont
documentées dans l'édition académique (D18) : la généralité reste à établir par
réplication, le cœur natif par les jalons M0 à M7 — dont M0, M1 et M2 sont désormais
franchis (§ 16), preuves terrain archivées.

## 14. Profils de cible — universalité

Le cœur du protocole — couches, règles, boucle, vérification — est indépendant de la cible
par construction, et tout ce qui dépend de la cible est regroupé dans un **profil de
cible**. L'universalité reste une propriété structurelle : instancier une plateforme
nouvelle revient à écrire un profil — ses sept éléments **et sa suite de conformité**
(§ 8.2, D22) — jamais à modifier le protocole.

Un profil définit obligatoirement sept éléments, qui font de l'extension une opération
vérifiable plutôt que déclarative : (1) l'ISA et la largeur de ses types — `usize`,
alignements, boutisme ; (2) l'ABI d'appel — registres de passage, volatilité, shadow space
ou zone rouge ; (3) le format d'exécutable et les protections à honorer — DEP/NX,
ASLR/PIE, CFI/CFG ; (4) l'interface système autorisée — IAT, syscalls, libc de la cible ;
(5) le mécanisme de patch à chaud natif — taille minimale de bascule atomique et procédure
d'invalidation du cache d'instructions ; (6) le moteur de notation et son vérificateur de
round-trip ; (7) la granularité des blocs et le padding garantissant les adresses stables
(R7). Un huitième livrable s'ajoute en v0.4.0 : la **politique anti-rollback et de
vérification au chargement** propre au profil (déclinaison concrète de R10 — registre des
versions acceptées, stockage du plancher, contrôles d'environnement).

| Profil | ISA | OS | Format | Interface | Statut |
|---|---|---|---|---|---|
| `x86-64-win11-pe` | x86-64 | Windows 11 | PE32+ | IAT (kernel32, ws2_32, Schannel) | Primaire — jalons M0-M5 |
| `x86-64-linux-elf64` | x86-64 | Linux | ELF64 | syscalls + libc | M6 — portabilité inter-OS |
| `riscv64-linux-elf64` | RISC-V 64 | Linux | ELF64 | syscalls + libc | M7 — portabilité inter-ISA |
| `aarch64-macos-macho` | AArch64 | macOS | Mach-O | libSystem | Réservé — hors feuille de route courante |
| `wasm32-wasi` | WebAssembly | WASI | module Wasm | WASI | Réservé — étude de niche |

L'identifiant d'un profil suit la convention `<isa>-<os>-<format>`. La correspondance des
couches est la suivante : la couche I est partagée par tous les profils du projet ; chaque
entrée de la carte porte son profil ; chaque profil possède son binaire, ses empreintes de
build et son registre de variantes dans frag-bld. « Sans compilateur » ne signifie pas
« sans système d'exploitation » — les interfaces sont appelées selon les conventions du
profil, comme tout binaire natif légitime.

### 14.1 Profil primaire : ABI Microsoft x64

| Convention | Règle |
|---|---|
| Passation des arguments | RCX, RDX, R8, R9, puis la pile — de droite à gauche |
| Valeur de retour | RAX (RDX pour une valeur de 128 bits) |
| Shadow space | 32 octets réservés par l'appelant avant chaque CALL |
| Registres volatils | RAX, RCX, RDX, R8 à R11 — détruits par l'appelé |
| Registres non volatils | RBX, RBP, RDI, RSI, R12 à R15 — préservés par l'appelé |
| Registres flottants | XMM0 à XMM5 volatils, XMM6 à XMM15 préservés |
| Alignement de pile | RSP multiple de 16 au point d'appel |
| Zone rouge | Aucune — contrairement à System V : stocker sous RSP sans allocation préalable est interdit |

L'absence de zone rouge est le piège classique pour qui vient de System V. La convention
interne du projet en tire les conséquences : R10 et R11 sont désignés registres de travail
internes — volatils selon l'ABI, donc jamais promis à un appelant ; aucune donnée vivante
ne séjourne entre RSP et RSP+32 au moment d'un appel ; tout bloc qui appelle une API
alloue son cadre avant d'y toucher. Ces règles internes sont portées par frag-con.

### 14.2 Différences entre profils — aperçu

| Élément | `x86-64-win11-pe` (primaire) | `x86-64-linux-elf64` (M6) | `riscv64-linux-elf64` (M7) |
|---|---|---|---|
| ABI | msx64 : RCX RDX R8 R9 ; shadow space 32 o. | SysV : RDI RSI RDX RCX R8 R9 ; zone rouge 128 o. | psABI RISC-V : a0-a7 |
| Format | PE32+ : DYNAMICBASE, HIGH_ENTROPY_VA, NX | ELF64 : PIE, RELRO, NX | ELF64 : PIE, RELRO, NX |
| Interface | IAT : kernel32, ws2_32, Schannel | syscalls + libc | syscalls + libc |
| Patch à chaud | trampoline 5/12 o., écriture alignée atomique | identique x86-64 | instructions de taille fixe : bascule par registre scratch + `fence.i` |
| Notation | keystone / capstone x86-64 | keystone / capstone x86-64 | keystone / capstone RISC-V |

Deux transitions méritent une vigilance documentée. Le passage Windows → Linux **inverse**
le piège de la zone rouge : ce qui était interdit sur msx64 (stocker sous RSP) redevient
permis sur SysV pour une fonction feuille — l'agent doit désapprendre le réflexe acquis sur
le profil primaire, et frag-con porte la convention effective de chaque bloc. Le passage
x86-64 → RISC-V change la nature du patch à chaud : sur une ISA à instructions de taille
fixe, il n'existe pas de trampoline relatif de 5 octets insérable n'importe où ; la bascule
passe par un registre scratch chargé de l'adresse cible, suivi d'une barrière
d'invalidation du cache d'instructions (`fence.i`) — le profil spécifie la séquence exacte
et son atomicité.

## 15. Gouvernance

### 15.1 Journal des décisions — format normalisé

Le protocole ne se révisant jamais en silence, chaque décision structurante est consignée
dans un journal des décisions. La v0.4.0 normalise le format (D24) — les entrées D19 à
D25 du dépôt l'appliquent dès à présent :

| Champ | Exigence |
|---|---|
| ID | `DNNN`, séquentiel, jamais réutilisé |
| Date | date de consignation |
| Statut | active · amendée par Dxx · invalidée par Dxx |
| Contexte | exigence, incident ou évaluation qui motive la décision |
| Choix retenu | décision en une phrase, rattachée à la fonction objectif |
| Alternatives rejetées | au moins une, avec motif |
| Amendements | référence explicite à la décision remplacée, le cas échéant |
| Développement | argumentaire détaillé si la décision engage l'architecture |

Trois règles : le journal est **append-only** (une entrée ne s'efface jamais) ; une
révision **invalide explicitement** ce qu'elle remplace (la procédure D14→amende D10
illustre le mécanisme) ; aucune entrée n'est rétrodatée. La conformité du journal —
présence des champs, unicité des ID, chaînage des amendements — est contrôlée
mécaniquement par l'audit de gouvernance (§ 15.2).

### 15.2 Tableau de bord de conformité

La v0.4.0 unifie les indicateurs de santé en un **tableau de bord de conformité** (D24),
généré par la commande d'audit à chaque commit et à chaque cristallisation, archivé avec
la carte :

| Métrique | Cible | Source de mesure |
|---|---|---|
| Blocs avec spécification I à jour | 100 % | audit de traçabilité (§ 4.2) |
| Chaînes de traçabilité complètes I ↔ C ↔ B ↔ tests | 100 % | audit de traçabilité |
| Construction | 0 erreur · 0 avertissement | build |
| Tests différentiels | 100 % verts | oracle |
| Empreintes des données embarquées | conformes à la carte | hachage |
| Défauts ouverts par classe T1–T6 | 0 | journal des décisions (classification) |
| Optimisations sans mesure (R11) | 0 | journal d'optimisation |
| Budgets tokens (localiser / éditer / ajouter) | ≤ 64 / 3 000 / 6 000 | instrumentation — mesurés M1 : 51 / 719 / 1 088 (D31) |
| Suite de conformité par profil actif | verte | suite du profil (§ 8.2) |
| Changements hors journal des décisions | 0 | diff vs journal (audit de gouvernance) |
| Pré-versions : dev/rc/final correctement balisées | 100 % | registre des balises (§ 9) |

Le tableau de bord est la contrepartie mesurable de la gouvernance : chaque affirmation du
protocole s'y retrouve sous forme de métrique avec sa cible et sa source — aucune ne
s'appuie sur une déclaration non vérifiable. Les métriques dépendantes de l'outillage
(instrumentation des budgets) affichent leur statut « cible » jusqu'à leur premier
mesurage.

### 15.3 Continuité et anti-enfermement

L'export de continuité (D16, FORMAT_CARTE § 8) demeure l'unique forme de transfert de
l'état de développement : conteneur chiffré et signé regroupant I, B, C et un manifeste
autodescriptif ; oracle régénéré depuis I à l'arrivée, jamais exporté ; procédure d'import
en cinq étapes dont l'échec d'une seule est terminal. Les pré-requis de sauvegarde (3-2-1
chiffrée, escrow de la clé maîtresse) sont inchangés.

**Le coffre-fort des phrases maîtresses (D75, FORMAT_CARTE § 11).** Le composant qui
centralise toutes les phrases maîtresses d'un projet — et de tout projet ultérieur conduit
sous le protocole — dans un conteneur unique chiffré « TRIADE-CF1 » (`coffre_fort.py`) :
phrase de contrôle détenue par le seul développeur (jamais stockée), Argon2id aux
planchers de la carte au repos puis HKDF à contexte dédié, XChaCha20-Poly1305 avec
l'en-tête clair pour AAD, écriture atomique 0600, autotest de falsification exigé à chaque
installation de l'outil. Le conteneur chiffré s'exporte tel quel vers le coffre Drive du
projet et le coffre personnel du développeur — son vol relève de la menace « sans la
phrase, indéchiffrable » (§ 13.1). Après une réinitialisation du poste, l'import du
conteneur puis `obtenir --vers-fichier` restaurent la phrase opérationnelle sans cérémonie
de régénération. La règle de discipline évolue en D81 sur un point, l'arbitrage étant
consigné : chaque cérémonie de clés (D27/D30) alimente le coffre-fort dans la même
session, et **la phrase de contrôle est sauvegardée durablement AVANT TOUTE AUTRE
ACTION** — `PHRASE-CONTROLE-COFFRE.txt` au racine du dépôt (phrase seule sur une ligne,
lisible par `--phrase-fichier`), commit dédié, push GitHub, miroir du coffre Drive par
le hook, copie au racine du coffre Drive — le fichier EST la remise (l'affichage unique
de D27/D30 demeure possible mais n'est plus le canal de survie). À chaque rotation le
fichier est remplacé et git conserve les phrases retirées du service. La graine Ed25519
reste hors coffre (D30) — la relève d'une lignée perdue resterait la cérémonie avec
preuve byte-identique. Contrepartie consignée : la phrase vit désormais sur le stockage
du coffre Drive partagé par lien — la confidentialité au repos y repose sur le contrôle
d'accès au dossier (restriction du partage par lien et vidage de corbeille sont les
mitigations premières) ; une phrase entrée dans l'historique git y demeure, la rotation
reste le remède à toute exposition avérée.

## 16. Critères d'acceptation des jalons M0 à M7

Huit jalons, chacun couvrant une capacité nouvelle et se terminant par des critères de
sortie mesurables — détail dans `docs/PLAN_MILESTONES.md`, mis à jour avec la présente
révision. **Conditions transverses** (v0.4.0) : aucun jalon n'est franchi sans oracle
vert, suite de conformité verte pour les éléments couverts, tableau de bord conforme
(§ 15.2) et carte signée. Les critères propres à chaque jalon :

| Jalon | Capacité | Critères de sortie mesurables | Statut |
|---|---|---|---|
| M0 | Chaîne artefact | exécution sur Windows 11 ; round-trip 100 % ; carte v0 signée et vérifiée ; exécutable < 4 Kio ; R1-R3, R8-R9 dès le premier octet | **franchi** 26/10/2026 (D26) |
| M1 | Blocs réutilisables | oracle 100 % sur la mini-libc ; première cristallisation ; adresses stables démontrées ; budgets tokens instrumentés (première mesure) | **franchi** 26/10/2026 — balise 0.2.0 (D32) |
| M2 | Patch à chaud | remplacement du bloc d'écho en exécution, sans interruption ; rollback démontré ; taux de régression post-patch nul | **franchi** 27/10/2026 — balise 0.3.0, boucle § 5 démontrée sur machine réelle (D43) |
| M3 | Entrées non fiables | un million de requêtes fuzzées sans crash ; proxy transparent ; contrats renforcés sur la surface de parsing | **franchi** 28/10/2026 — balise 0.4.0 (D74) |
| M4 | Tunnel chiffré | HTTPS en transit via Schannel ; échec propre sur certificat invalide | à venir |
| M5 | Outil complet | interception d'un flux navigateur en VM isolée ; patch à chaud du journal en production ; empreintes par build actives | à venir |
| M6 | Portabilité inter-OS | profil `x86-64-linux-elf64` : suite de conformité verte ; **diff nul sur la couche I** ; parité inter-profils vérifiée (§ 8.3) ; même oracle vert sur les deux profils | à venir |
| M7 | Portabilité inter-ISA | profil `riscv64-linux-elf64` : round-trip 100 % sur la nouvelle ISA ; patch à chaud conforme (scratch + `fence.i`) ; verrou croisé multi-profils ; export de continuité multi-profils vérifié | à venir |

M0 est le jalon existentiel — il prouve la chaîne notation, octets, exécutable, exécution
sans compilateur ; il est franchi. M2 est le jalon de vérité — le patch à chaud sur code
en exécution a motivé l'architecture ; il est franchi : la boucle complète (bascule
pendant le trafic, vérification memcmp, retour arrière, re-vérification) a été
démontrée sur machine réelle le 27 octobre 2026 (D43), au terme de la campagne
d'instrumentation relatée en § 8.4 — huit itérations, huit classes de défauts nommées,
zéro régression possible (chaque classe est gardée par une falsification). M6 et M7 transforment la portabilité de promesse en propriété
démontrée, en isolant chaque variable ; la suite de conformité par profil (§ 8.2) en est
désormais le critère d'acceptation explicite.

## 17. Correspondance des versions

### 17.1 Traçabilité des évolutions

| # | Évolution | En v0.3 | En v0.4.0 | Statut |
|---|---|---|---|---|
| 1 | Couche I normalisée | « contrats légers » sans gabarit | gabarit § 2 : identifiants stables, pre/post, invariants, cas d'échec, vecteurs | renforcé (D19) |
| 2 | Taxonomie des défauts | absente (analyse dans la seule démonstration) | classes T1–T6, § 3 | nouveau (D19) |
| 3 | Threat model minimal | 7 menaces | 13, dont 6 nouvelles, § 13.1 | étendu (D20) |
| 4 | R10 renforcée | checksums au lancement | + signature du manifeste, anti-rollback, conformité environnement, fail-closed explicite | renforcé (D20) |
| 5 | Optimisation prématurée | interdite implicitement (ordre lexicographique) | interdiction normative R11 | explicité (D21) |
| 6 | Journal d'optimisation | pratique de la démonstration (D15 RoomEq) | format normalisé OPT-NN, § 11 | officialisé (D21) |
| 7 | Fragmentation de la carte | 4 fragments (D4) | + norme « aucune opération ne lit tout », § 12 | consolidé (D24) |
| 8 | Localisation par intention | étape 2 de la boucle, implicite | interdiction du balayage formalisée, § 7 | renforcé (D24) |
| 9 | Budgets de tokens | 40 / 3 000 / 6 000 | inchangés, instrumentés au tableau de bord | consolidé (D24) |
| 10 | Suite de conformité par profil | implicite (7 éléments du profil) | suite obligatoire, § 8.2 | nouveau (D22) |
| 11 | Parité inter-profils | critères M6/M7 dispersés | définition formelle à contrat constant, § 8.3 | formalisé (D22) |
| 12 | Reverse-specs | absente (pratique née de la démonstration) | officialisées, § 10 | officialisé (D23) |
| 13 | Pré-versions | absente (pratique `-dev.1`) | dev.N / rc.N / X.Y.Z, § 9 | officialisé (D23) |
| 14 | Fixtures partagées | absente (pratique installateur) | contractuelles, § 2.4 | officialisé (D23) |
| 15 | Traçabilité I ↔ C ↔ B ↔ tests | implicite | table normative + audit mécanique, § 4.2 | formalisé (D24) |
| 16 | Journal des décisions | pratique (« mode de gouvernance ») | format normalisé, § 15.1 | normalisé (D24) |
| 17 | Tableau de bord de conformité | indicateurs dispersés (plan M0-M7) | métriques unifiées mesurables, § 15.2 | nouveau (D24) |

### 17.2 Modifications explicitement rejetées

Conformément au cahier de révision, les modifications suivantes — demandées ou
envisageables — ont été examinées et **rejetées, donc non appliquées** :

| Modification | Verdict | Motif |
|---|---|---|
| Modifier la hiérarchie Sécurité > Performance > Optimisation > Coût en tokens | rejetée | invariant de révision (D19) — c'est la condition même de l'arbitrage |
| Introduire une couche d'abstraction à l'exécution (bytecode portable, VM) | rejetée | trahit la fonction objectif Performance (D14) ; la parité s'obtient par vérification, pas par couche |
| Promettre la portabilité universelle immédiate | rejetée | la portabilité se vérifie par profil (M6/M7), elle ne se déclare pas |
| Introduire des mécanismes de furtivité face aux EDR | rejetée | hors périmètre assumé (§ 1.2) — transparence totale de l'outil |
| Affaiblir R5, R8, R9 ou R10 | rejeté | la révision ne contient que des renforcements ; les énoncés v0.3 de R1-R9 sont repris à l'identique |
| Anti-rollback par contrôle en ligne au chargement | rejetée | R10 doit échouer proprement hors ligne — aucune dépendance réseau |
| Optimisation validée sans mesure | rejetée | R11 : hot path + mesure avant/après + contrat stable |

### 17.3 Correspondance v0.4.0 → v0.5.0

| # | Évolution | En v0.4.0 | En v0.5.0 | Statut |
|---|---|---|---|---|
| 1 | Validation terrain | constats dispersés au journal des décisions | couche normée : boucle d'évidence, journal d'exécution, sondes contractualisées, diff chirurgical (§ 8.4) | nouveau (D43) |
| 2 | Taxonomie des défauts | classes T1–T6 (contrat non écrit) | + classes X1–X8, défauts invisibles à l'émulation (§ 8.5) | étendu (D35–D42) |
| 3 | État des jalons | M0 planifié, M1-M7 à venir | M0, M1, M2 franchis — preuves terrain archivées (§ 16) | constaté (D26, D32, D43) |
| 4 | Budgets de tokens | 40 / 3 000 / 6 000 (cibles) | 64 / 3 000 / 6 000 — corrigé et mesuré : 51 / 719 / 1 088 (D31) | corrigé (D31) |
| 5 | Suite de conformité | définie (7 éléments, 124 contrôles) | exécutée à chaque scellage rc/final — 124/124 sur le profil primaire | mesuré (D39–D43) |
| 6 | Volume d'oracle | 12 000 cas par bloc critique (référence) | campagnes effectives consignées : M1 76 010 cas, M2 50 533 cas, démo 86 cas | consolidé |
| 7 | Preuves terrain | non normées | archives brutes (journaux octet-exacts, empreintes) référencées au journal des décisions | officialisé (D43) |
| 8 | Fuzzing | mentionné (menace « fuzzing boîte noire », § 13.1) | jalon M3 ouvert : fuzzing à propriétés sur la surface d'entrées non fiables (D45) | structuré |

### 17.4 Modifications explicitement rejetées (v0.5.0)

Conformément au cahier de révision, les modifications suivantes ont été examinées et
**rejetées, donc non appliquées** :

| Modification | Verdict | Motif |
|---|---|---|
| Ajouter une règle R12 « validation terrain obligatoire » | rejetée | la boucle d'évidence découle de R5 et des critères de jalon ; une règle de plus diluerait le corpus sans rien exiger de nouveau |
| Étendre le fuzzing à tous les blocs scellés | rejetée | M3 cible la surface d'entrées non fiables ; les blocs à appelants de confiance relèvent des vecteurs existants (§ 8.1) |
| Reconstruire les artefacts scellés 0.2.0 / 0.3.0 pour la documentation | rejetée | les balises finales sont immuables (§ 9) ; la documentation cite les empreintes |
| Fusionner les classes X dans les classes T (T7–T14) | rejetée | les deux familles appellent des remèdes distincts : écrire le contrat (T) contre enrichir le modèle d'environnement et falsifier (X) |

### 17.5 Correspondance v0.5.0 → v0.5.1

| # | Évolution | En v0.5.0 | En v0.5.1 | Statut |
|---|---|---|---|---|
| 1 | Phrases maîtresses | instruction de cérémonie seule (D27/D30) — quatre réinitialisations du poste ont montré la limite | coffre-fort TRIADE-CF1 : conteneur chiffré par projet, export/import, restauration post-réinitialisation (§ 15.3, FORMAT_CARTE § 11) | nouveau (D75) |
| 2 | État des jalons | M0–M2 constatés, M3 ouvert | M3 franchi 28/10/2026 — campagne million (D72), conformité permanente (D73), scellage 0.4.0 (D74) | constaté (D72–D74) |
| 3 | Modèle de menace | 13 menaces, dont le vol de l'export de continuité | + vol du coffre-fort des phrases — sans la phrase de contrôle, indéchiffrable | étendu (D75) |

Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée. Les
alternatives rejetées à D75 : conserver la seule instruction de coffre développeur (le
statu quo que les quatre réinitialisations ont démenti) ; stocker les phrases en clair
dans `.keys/` (l'état opérationnel du poste n'est pas un coffre) ; embarquer la graine
Ed25519 dans le coffre (contraire à D30 — jamais confiée) ; confier le conteneur au seul
gestionnaire de mots de passe du développeur sans copie de coffre projet (la continuité
exige les deux copies, le conteneur étant indéchiffrable sans la phrase).

### 17.6 Correspondance v0.5.1 → v0.5.2

| # | Évolution | En v0.5.1 | En v0.5.2 | Statut |
|---|---|---|---|---|
| 1 | Garde de la phrase de contrôle | détenue par le seul développeur, jamais stockée, affichée une seule fois (D75) | sauvegardée durablement dès production : `PHRASE-CONTROLE-COFFRE.txt` au dépôt (git + GitHub + miroir Drive) et au racine du coffre Drive, AVANT toute autre action ; le fichier est la remise (§ 15.3, FORMAT_CARTE § 11) | modifié (D81) |
| 2 | Menace « vol du coffre-fort » | sans la phrase, indéchiffrable | la phrase vit sur le coffre Drive partagé par lien : confidentialité au repos ramenée au contrôle d'accès du dossier ; mitigation première = restreindre le partage ; une phrase commise en git y demeure à vie, la rotation reste le remède | étendu (D81) |
| 3 | État des jalons | M0–M3 franchis, M4 à venir | M4 ouvert (D77 — couche I écrite-avant-code : huit spécifications tls + deux révisions http) ; M0–M3 inchangés | constaté (D77) |

Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée. Les
alternatives rejetées à D81 : conserver la remise par affichage unique (le statu quo que
la session morte de D80 a démenti — la phrase ne vivait plus que dans le bac à sable) ;
sceller la phrase de contrôle sous une phrase antérieure (déplace le problème : la phrase
de secours exigerait sa propre garde) ; exporter la seule copie chiffrée du coffre sans
garder la phrase (le conteneur indéchiffrable protège de l'exposition, pas de la perte —
or c'est la perte qui est le risque vécu) ; restreindre d'office le partage du dossier
Drive (décision appartenant au développeur, hors du champ de l'agent — consignée en
recommandation, § 15.3).

## 18. Glossaire

| Terme | Définition |
|---|---|
| Carte | Couche C : index signé et chiffré liant intention et binaire, unique interface de développement de l'agent |
| Bloc | Unité de code machine de 32 à 512 instructions, une responsabilité, un point d'entrée stable |
| Spécification I | Artefact normalisé (§ 2) : identifiant stable, intention, contrat pré/post, invariants, cas d'échec, vecteurs, fixtures, provenance |
| Identifiant stable | Clé `<DOM>-<NN>` d'une spécification I — immuable, jamais réutilisée (miroir de l'adresse stable côté B) |
| Scellage | Acte atomique d'engagement : écriture du bloc, mise à jour de la carte, inscription de l'empreinte |
| Cristallisation | Immuabilité d'un bloc après dix vérifications réussies ; modification dès lors soumise à procédure lourde |
| Pré-version | Segment `dev.N` (oracle vert) ou `rc.N` (candidate terrain) précédant une version finale `X.Y.Z` |
| Oracle éphémère | Implémentation de référence triviale dérivée de la couche I, générée par session et détruite après usage |
| Verrou croisé | Contrôle bilatéral d'intégrité : empreintes des blocs dans la carte, signature de la carte, contrôles au chargement |
| Contrat | Signature typée, pré et post-conditions, invariants et cas d'échec publiés d'un bloc — la partie de I embarquée dans C |
| Fragment | Quart de carte chiffré séparément : localisation, contrats, preuves, builds |
| Profil de cible | Instanciation complète du protocole pour un couple ISA/OS : sept éléments + suite de conformité |
| Suite de conformité | Suite de tests vérifiant les sept éléments d'un profil (§ 8.2) — condition de déclaration de support |
| Parité inter-profils | Équivalence vérifiée par exécution de deux profils sur un même contrat, à paramétrisation près (§ 8.3) |
| Reverse-spec | Spécification I extraite d'un binaire scellé hérité, avec provenance et statut (§ 10) |
| Taxonomie T1–T6 | Classification des défauts de contrat non écrit (§ 3) |
| Journal d'optimisation | Registre normalisé des optimisations mesurées — appliquées ou refusées (§ 11) |
| Fixtures contractuelles | Échantillons partagés d'un contrat externe, portés par la spécification I (§ 2.4) |
| Traçabilité I ↔ C ↔ B ↔ tests | Chaîne complète exigence → index → bloc → défense, auditée mécaniquement (§ 4.2) |
| Tableau de bord de conformité | Métriques mesurables avec cibles, générées à chaque cycle (§ 15.2) |
| Suite cryptographique | Paramètres de l'en-tête de carte — hachage, signature, chiffrement — choisis par le développeur dans une liste blanche |
| Re-cryptage | Migration atomique de la suite cryptographique : recalcul des empreintes, re-chiffrement, re-signature, archivage |
| Export de continuité | Conteneur chiffré et signé regroupant I, B, C et un manifeste — seule forme de transfert de l'état de développement |
| Empreinte de build | Variante binaire unique par livraison et par profil, rendant toute fuite traçable |
| Vecteurs de vérification | Vecteurs dorés, propriétés différentielles et tests de rejet rattachés aux exigences (§ 8.1) |
| Notation | Représentation textuelle des instructions assemblées par le moteur du profil — un média, jamais un langage compilé |
| Round-trip | Contrôle de fidélité : assemblage puis désassemblage d'un bloc, comparaison exacte |
| Validation terrain | Exécution de l'artefact livré sur système réel, preuve archivée — valide le modèle d'environnement de l'oracle (§ 8.4) |
| Journal d'exécution | Fichier de preuves écrit au fil de l'eau par l'artefact ; une ligne n'est écrite qu'après vérification de l'étape qu'elle atteste |
| Sonde de trace | Instrumentation temporaire aux frontières d'un intervalle suspect : journalise des faits vérifiés ; retrait promis dans la spécification (D40, D43) |
| Défaut invisible à l'émulation | Défaut dont le modèle d'environnement de l'oracle ne rend pas compte — classes X1–X8 (§ 8.5) |
| Diff chirurgical | Itération terrain dont l'audit vérifie qu'aucun octet hors des zones autorisées n'a changé |
| Fuzzing à propriétés | Génération d'entrées aléatoires contraintes, vérifiées par propriétés (jamais de crash, domaines de retour, bornes mémoire) — cœur du jalon M3 |
| Coffre-fort des phrases maîtresses | Conteneur chiffré TRIADE-CF1 centralisant toutes les phrases maîtresses d'un projet (D75, § 15.3) — l'outil vit dans le dépôt, le conteneur jamais |
| Phrase de contrôle | Secret ouvrant le coffre-fort — sous garde durable depuis D81 : `PHRASE-CONTROLE-COFFRE.txt` au dépôt et au racine du coffre Drive, sauvegardé AVANT toute autre action dès production (§ 15.3) |

## 19. Journal des versions

| Version | Date | Contenu |
|---|---|---|
| v0.1 | 25 oct. 2026 | Première ébauche : couches I/B/C, règles R1 à R7, boucle en sept étapes, feuille de route M0–M5 |
| v0.2 | 25 oct. 2026 | Décisions D1 à D10 ; sharding en quatre fragments chiffrés ; suite cryptographique (Ed25519, XChaCha20-Poly1305, Argon2id) ; règles R8 à R10 ; empreintes par build ; budgets en tokens ; spécification de la cible x86-64 / Windows 11 ; critères de sortie mesurables |
| v0.3 | 25 oct. 2026 | Universalité par profils de cible (D14, amende D10) ; suite cryptographique paramétrable (D15, amende D5) ; export de continuité chiffré et signé (D16, précise R1) ; en-tête de carte normalisé ; jalons M6-M7 |
| v0.5.0 | 27 oct. 2026 | Révision du retour du terrain : validation terrain normée — boucle d'évidence, journal d'exécution, instrumentation contractualisée, diff chirurgical (D43) ; taxonomie étendue X1–X8 des défauts invisibles à l'émulation (D35–D42) ; jalons M0–M2 constatés franchis (balises 0.2.0 et 0.3.0 — D26, D32, D43) ; budget de localisation corrigé à 64 tokens et budgets mesurés (D31) ; ouverture du jalon M3 — contrats renforcés sur entrées non fiables, fuzzing à propriétés (D45). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.5.1 | 28 oct. 2026 | Coffre-fort des phrases maîtresses (D75) : conteneur chiffré TRIADE-CF1 centralisant toutes les phrases maîtresses par projet — Argon2id aux planchers de la carte, HKDF à contexte dédié, XChaCha20-Poly1305, autotest de falsification (19 contrôles), export chiffré vers les coffres projet et développeur, restauration post-réinitialisation (§ 15.3, FORMAT_CARTE § 11) ; état des jalons constaté — M3 franchi le 28/10/2026 (campagne million D72, conformité permanente D73, scellage balise 0.4.0 D74) ; modèle de menace étendu au vol du coffre-fort (§ 13.1). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.5.2 | 28 oct. 2026 | Garde durable de la phrase de contrôle du coffre-fort (D81) : sauvegardée AVANT TOUTE AUTRE ACTION dès production — fichier `PHRASE-CONTROLE-COFFRE.txt` au racine du dépôt (phrase seule sur une ligne, lisible par `--phrase-fichier`), commit dédié, push GitHub, miroir du coffre Drive, copie au racine du coffre Drive ; le fichier est la remise, l'affichage unique de cérémonie cesse d'être le canal de survie ; restauration post-panne prouvée de bout en bout (téléchargement Drive → coffre ouvert, entrées listées) ; menace « vol du coffre-fort » étendue — la confidentialité au repos repose désormais sur le contrôle d'accès au dossier Drive (mitigation première : restriction du partage par lien), une phrase commise en git y demeure à vie ; M4 constaté ouvert (D77, couche I écrite-avant-code). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.4.0 | 26 oct. 2026 | Révision de gouvernance vérifiée : couche I normalisée et taxonomie des défauts T1–T6 (D19) ; threat model étendu et R10 renforcée — checksums, signature de manifeste, anti-rollback, fail-closed explicite (D20) ; R11 optimisation mesurée et journal d'optimisation (D21) ; suite de conformité par profil et parité inter-profils à contrat constant (D22) ; reverse-specs, pré-versions dev.N/rc.N/final et fixtures partagées officialisées (D23) ; traçabilité I↔C↔B↔tests, journal des décisions normalisé, tableau de bord de conformité, norme de fragmentation et localisation par intention, budgets tokens instrumentés (D24). Hiérarchie de la fonction objectif inchangée et verrouillée (D19) ; aucune règle affaiblie ; aucune couche d'exécution ajoutée ; numérotation à trois segments |

La présente version consigne l'état au passage de relais : jalons M0 à M3 franchis sur
validations terrain (balises finales 0.2.0, 0.3.0, 0.4.0), coffre-fort des phrases
maîtresses opérationnel (D75) et sa phrase de contrôle sous garde durable (D81), jalon
M4 (tunnel chiffré) ouvert — couche I écrite-avant-code (D77), étape (b) en cours. Les évolutions prévisibles — bloc optionnel de syscalls directs,
TLS 1.3 pur en blocs scellés, profils additionnels après M7 — restent volontairement hors
du périmètre courant afin que chaque addition s'appuie sur des résultats mesurés. La règle
de gouvernance demeure : toute évolution invalide explicitement ce qu'elle remplace, et
rien ne se change en silence — le terrain compris : chaque lecture d'exécution est une
révision potentielle du modèle, et son enseignement se consigne (§ 8.4, § 8.5).


