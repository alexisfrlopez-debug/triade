# PLAN GELÉ — F3UZNUI3L (la vague 14)
> L'atelier de fermeture sécurité en quatre gestes, chacun sur pièces : le run
> Tamarin CF3 v2 préparé (et exécuté si le prover vit au bac), le kit de cérémonie
> du durcissement du coffre réel, les gardes enforced aux frontières, le dudect
> prêt. D105 : le laboratoire ne touche JAMAIS le coffre réel ni les phrases
> réelles — copies à phrase publique marquée uniquement.
> Gelé AVANT toute modification ; aucun verdict fabriqué.

## Le mandat
(1) **TAMARIN CF3 v2** : préparer le run au poste réel — installer tamarin-prover
(version épinglée, empreinte consignée), exécuter `CF3-v2.spthy` (sha256
f9a79efc… consigné) selon PROTOCOLE-VERIFICATION : lemme d'implication « secret
appris ⇒ ≥3 parts », témoins de non-vacuité, témoin d'atteignabilité du seuil ;
bornes nommées pour les lemmes 1-3, preuve interactive à l'induction si nécessaire
(les SIX lemmes — l'écart de dénombrement du protocole v1 corrigé par écrit) ;
tout écart de syntaxe ou de preuve se NOMME et s'amende PAR ÉCRIT (empreinte
reconsignée), jamais en silence ; le verdict (prouvé/échec/bornes) consigné au
registre et à la table des statuts. Si le prover demeure absent du bac : le
runbook complet livré, le gap nommé, aucun verdict fabriqué.
(2) **DURCISSEMENT DU COFFRE RÉEL** : préparer le kit de cérémonie déployant les
sept gestes (a)-(g) prouvés en copies labo (empreinte du chiffré liée à la clé
vérifiée AVANT l'AEAD, dérivation du piège liée à l'époque, re-paramétrage Argon2
versionné au plancher d'entropie, changement de phrase sous séquestre 5/3, garde
RAM mlock+zéroïsation, ancrage du témoin d'époque) — le kit prêt, le geste
appartient au développeur ; autotest complet sur copie publique AVANT livraison.
(3) **GARDES ENFORCED AUX FRONTIÈRES** : sur les 58 obligations conditionnelles
(TCB 24 plan + 23 appelant + 11 OS), émettre des gardes runtime aux SEULES
frontières de confiance dans des copies de laboratoire du scellé, mesurer le coût
par bloc (R11, cible ≤1 % sur les blocs non crypto, gardes de frontière only sur
crypto), prouver par z3 que la garde de frontière décharge l'obligation interne
(composer les 58 certificats UNSAT existants), falsifier par garde (invariant
violé REFUSÉ aux deux bornes et à la face d'index, adresse honnête ADMISE).
(4) **DUDECT** : préparer l'exécution de la répétition pré-enregistrée (n≥10 par
N∈{60,200,400}, ≥2 machines, fréquence fixée, cœur épinglé, investigation des pics
tls13-02/13 à N=200 aux trois causes testables) — agrégateur fail-closed
re-autotesté (complétude AVANT tout calcul), aucun chiffre sans le geste.

## Les gestes
1. Ce plan gelé AVANT toute modification.
2. `atelier-fermeture-f3uznui3l/` : le registre Tamarin (version épinglée,
   empreinte reconsignée, console intégrale le cas échéant), le kit de cérémonie
   (LISEZMOI + AUTOTEST + epreuves + checklist, empreintes hashées), la composition
   z3 des 58 certificats re-vérifiés + les gardes de frontière émises en copies de
   labo + le coût par bloc mesuré + la falsification vécue, le constat dudect.
3. Le coffre réel DEMEURE intact — aucune clé, aucune phrase réelle touchée.

## La vérification après modifications
z3 re-déchargé sur CHAQUE garde émise (UNSAT deux côtés) ; falsification par
garde vécue ; autotests coffre verts sur copies ; le modèle Tamarin re-hashé
après tout amendement ; les scellés 14/14 avant/après ; la table des statuts mise
à jour UNIQUEMENT sur pièces recoupées (prouvé non borné / prouvé borné / mesuré /
en attente) ; consigner les décisions append-only, les gaps restants nommés.

## Les refus
Jamais un verdict Tamarin fabriqué ; jamais le coffre réel touché au laboratoire ;
jamais une garde posée sur le scellé (copies de labo seules) ; jamais un chiffre
dudect sans le geste du développeur.
