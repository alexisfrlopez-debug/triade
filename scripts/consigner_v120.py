#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consigner D187, D188, D189 (le modèle formel v0.12.0) + l'Entrée 225 +
le worklog — append-only."""
import pathlib

D = pathlib.Path("/home/z/my-project/triade/docs/DECISIONS.md")
J = pathlib.Path("/home/z/my-project/triade/docs/JOURNAL_TRAVAIL.md")
W = pathlib.Path("/home/z/my-project/triade/worklog.md")

DECISIONS = """

## D187 — LE MODÈLE FORMEL DE CF3 : LES QUATRE PROPRIÉTÉS PROUVÉES DANS LE MODÈLE (l'explorateur d'états explicites : la sémantique opérationnelle de la chaîne du coffre scellé — dérivation KEK [les TROIS éléments entrent, HKDF à contexte d'époque], cycle en deux actes [brouillon chiffré sous clé de session, clés maîtresses mortes, canonique jamais réécrit], anti-retour d'époque [époques croisées conteneur/piège + le miroir de l'époque la plus haute vue], sentinelle instantanée [l'invocation : sans le piège l'ouverture est IMPOSSIBLE, pas seulement refusée], destruction sur falsification PROUVÉE [piège intact + phrase vérifiée + empreinte/AEAD échoue] — en machine à états finie abstraite, les primitives SYMBOLIQUES, l'espace ÉNUMÉRÉ EXHAUSTIVEMENT : 154 états, 1 152 transitions, profondeur 6, époques ≤ 3, l'adversaire à seuil ≤ 2 éléments AVEC le rejeu d'époques passées) ; LES HYPOTHÈSES D'ADVERSAIRE EXPLICITES A1-A5 (A1 le modèle symbolique : HKDF/AEAD/SHA parfaits, Argon2id la phrase inconnue sans le secret ; A2 le seuul : au plus DEUX des trois éléments, tous les sous-ensembles explorés ; A3 le média : falsifiable (le tag) mais jamais ENRICHI (les moitiés futures naissent hors machine) ; A4 les anciens couples : le rejeu complet modélisé ; A5 le HORS MODÈLE : canaux auxiliaires, failles d'implémentation, le vol des TROIS, le quantique — NOMMÉ, jamais confondu avec le prouvé) ; LES MANIFESTES DE KIT À SHA-256 (maj_kit.py : le manifeste du kit de cérémonie consigne sha256, la suite de D184 ; les kits LIVRÉS demeurent — leurs manifestes md5 sont des PREUVES ; md5 à l'idempotence Drive et à l'affichage Loupe)

**Le contexte qui fonde la décision (11/11).** Le troisième fichier d'instruction : « modéliser CF3 dans un vérificateur de protocoles (Tamarin ou ProVerif)… rapporter chaque propriété prouvée, réfutée ou hors modèle, avec les hypothèses d'adversaire explicites ». Tamarin et ProVerif sont ABSENTS du laboratoire (aucun Haskell/OCaml, aucune installation possible) : le choix du vérificateur est NOMMÉ — l'explorateur d'états explicites (model checking borné), la sémantique opérationnelle de v06/coffre_cf3.py transcrite en machine à états, LE SCRIPT EST LE MODÈLE (python3 scripts/modele_formel_v120.py : reproductible d'un clone frais, aucune boîte noire).

**Les règles.** (1) **P1 LE SECRET SOUS SEUIL** : l'adversaire à ≤ 2 éléments n'atteint JAMAIS l'état « secret appris » — 0 contre-exemple sur les 154 états ; la clé : derive_kek lie les TROIS éléments (la possession de la machine seule ne permet même pas d'ESSAYER des phrases — le champ verif exige V_piège, publique mais portée par le média). (2) **P2 LE REFUS DU ROLL-BACK** : aucune transition ne décrémente l'époque (la monotonie structurelle, RE-CONSTATÉE mécaniquement transition par transition) ; le rejeu d'un couple d'époque passée est REFUSÉ NOMMÉ (« RETOUR EN ARRIÈRE », l'époque du couple < le miroir). (3) **P3 L'ABSENCE DE DESTRUCTION SUR PHRASE ERRONÉE** : la phrase erronée mène à PhraseErronee (réessai à délai croissant), AUCUN état atteignable ne combine l'essai erroné et la destruction — 0 contre-exemple ; la destruction exige la falsification PROUVÉE (piège intact + phrase vérifiée + échec cryptographique). (4) **P4 LE RAYON BORNÉ À UNE ÉPOQUE** : la destruction touche l'état LOCAL (le conteneur, le brouillon, le PV), JAMAIS le média du piège (le TÉMOIN, jamais le coupable), JAMAIS les fragments CF2 (la coexistence § 12 : la destruction reste survivable) — 0 violation. (5) **LE RAPPORT PAR PROPRIÉTÉ** : PROUVÉE DANS LE MODÈLE signifie exactement cela — sous A1-A4, dans les bornes déclarées (époques ≤ 3, profondeur 6) ; ce qui sort est HORS MODÈLE et le dit.

**Alternatives rejetées.** Attendre un environnement Tamarin — rejeté : la commande exige l'exécution à cette édition ; l'explorateur nommé fait le travail dans les bornes, le portage Tamarin demeure la voie future (le modèle est documenté, la transcription directe). Modéliser l'implémentation (Python, la RAM, le GC) — rejeté : A5 le nomme HORS MODÈLE ; le modèle vérifie le PROTOCOLE, pas sa réalisation — la falsifiabilité des autotests (92 contrôles) couvre l'écart.

**Frontières.** Aucun artefact scellé ne bouge ; aucun arbre signé ne bouge ; le coffre RÉEL intact (l'autotest vit aux répertoires temporaires, discipline D105 — l'empreinte du conteneur réel CONSTATÉE IDENTIQUE avant/après) ; les manifestes FUTURS à sha256, les kits livrés demeurés.

## D188 — LE MODÈLE DE MENACE EN DEUX PLANS : le plan IP (la propriété intellectuelle — rétro-ingénierie [temps acheté, érodé par les LLM de décompilation], expropriation [l'ÉVOLUTION du code volé bloquée : l'intention signée, l'héritage scellé, les clés hors-ligne, l'homme mort Shamir — son EXÉCUTION ne l'est pas], redistribution [empreintes par build, le canary trap] — la CONFIDENTIALITÉ d'abord, les pertes REMÉDIABLES [rotation, variantes]) ET le plan SÛRETÉ D'EXÉCUTION (l'empoisonnement/corruption de carte [signature, verrou croisé, AEAD], l'evil maid sur conteneur ou média [époques croisées, tags, le champ verif indérivable], le rollback conteneur+piège [les TROIS témoins d'époque], le binaire altéré [checksums par bloc, manifeste signé au chargement], l'environnement non conforme [contrôles de profil, fail-closed], l'agent défaillant [R2/R5, l'oracle issu de I, les budgets] — l'INTÉGRITÉ et la DISPONIBILITÉ d'abord, les pertes IRRÉMÉDIABLES) ; L'ORDRE INTRA-SÉCURITÉ EXPLICITE (la POLITIQUE DE PROJET qui manquait à la hiérarchie D19 : quand les deux plans se rencontrent, le plan sûreté GAGNE — un coffre cassé ne protège rien) ; LA TENSION D81 ↔ D183 CONSIGNÉE AVEC L'ANALYSE CHIFFRÉE (l'espérance de perte annuelle ≈ 4,0 × 10⁻²·C_exposition sous D81 contre ≈ 1,0 × 10⁻³ sous le séquestre Shamir 5/3 — un facteur ≈ 40 ; D81 DEMEURE la décision active, la cérémonie du séquestre appartient au développeur)

**Le contexte qui fonde la décision (11/11).** Le troisième fichier : « restructurer le modèle de menace en deux plans séparés et expliciter l'ordre intra-Sécurité (confidentialité vs disponibilité) qui manque à la hiérarchie D19 ; consigner la tension D81 et la contre-proposition de D182 [D183 après le coulissement de numérotation] avec analyse comparative chiffrée des risques perte/exposition ».

**Les règles.** (1) Les DEUX PLANS sont SÉPARÉS : chaque menace du tableau § 15.1 vit dans SON plan, la contre-mesure et le résiduel y restent ; la distinction fondatrice du protocole (« séparer l'obfuscation qui protège la propriété intellectuelle du durcissement qui protège l'exécution ») devient la STRUCTURE du tableau. (2) L'ORDRE INTRA-SÉCURITÉ : dans le plan IP, la confidentialité domine (les pertes remédiables : la rotation D80 l'a prouvé) ; dans le plan sûreté, l'intégrité et la disponibilité dominent (la perte du coffre est IRRÉVERSIBLE — l'incident fondateur de D81) ; ENTRE les plans, le plan sûreté gagne — c'est une POLITIQUE DE PROJET EXPLICITE (D19 requalifiée par D182 : la hiérarchie quadripartite demeure la règle, l'ordre interne de la sécurité est désormais ÉCRIT). (3) La TENSION D81 ↔ D183 : les deux décisions VIVENT l'une contre l'autre dans le tableau (la garde en clair contre le séquestre chiffré), l'analyse chiffrée de D183 citée — le facteur ≈ 40 en faveur du séquestre, les quatre raisons pour lesquelles D81 demeure néanmoins (le geste du développeur, la protection CF3 existante, l'incident fondateur, les mitigations en vigueur). (4) La restructuration vit À LA SPÉCIFICATION (le § 15 de la v0.12.0, la chaîne spec_v120) et AU MANUSCRIT (§ 4.6) — le tableau du CŒUR assaini, la hiérarchie D19 INTACTE.

**Alternatives rejetées.** Fusionner les plans en un tableau unique annoté — rejeté : la commande exige la SÉPARATION (l'amalgame est précisément le défaut nommé). Modifier la hiérarchie D19 — rejeté : l'ordre intra-sécurité est une politique explicite AJOUTÉE, jamais une règle changée en silence.

**Frontières.** La spécification v0.12.0 porte le tableau restructuré ; le manuscrit § 4.6 le présente ; AUCUNE règle du cœur modifiée ; AUCUN coffre touché (D81 demeure, D183 demeure une proposition).

## D189 — LA CRISTALLISATION ÉVALUÉE ET LE PROTOCOLE DE RÉPLICATION PROPOSÉ : le seuil de 10 rebuilds consécutifs identiques JUSTIFIÉ par le test séquentiel (le SPRT de Wald sur la probabilité de divergence q par rebuild : H0 q ≤ 1 % contre H1 q ≥ 50 % — CINQ rebuilds identiques atteignent déjà α = 5 %, le seuil historique DIX atteint α = 1,08 × 10⁻³, 46× plus strict que le canonique) — LE SEUIL DEMEURE 10 (la politique de projet, jamais changée en silence : l'analyse est la JUSTIFICATION consignée, la voie documentée d'un relâchement futur SI le développeur l'arbitre) ; LE PROTOCOLE DE RÉPLICATION (les trois axes indépendants : R1 un second développeur mène un jalon complet depuis le dépôt public ; R2 une seconde application réelle neuve en un autre domaine ; R3 le port d'un bloc vers un profil non primaire — avec la GRILLE DE CODAGE T/X à CINQ classes terrain [T1 chargeur/image, T2 ABI/matériel, T3 sémantique du chargeur, T4 conventions système, T5 environnement] et TROIS classes laboratoire [X1 logique, X2 structure, X3 harnais], la DOUBLE ANNOTATION par deux codeurs indépendants, le KAPPA DE COHEN [κ ≥ 0,61 l'acceptation : substantiel], les critères d'acceptation PRÉ-ENREGISTRÉS [le jalon franchi, les défauts codés, les classes T du réplicant ⊆ celles du premier développeur — une classe NOUVELLE est un RÉSULTAT, jamais un échec]) — PROPOSÉ, JAMAIS EXÉCUTÉ (N = 1 demeure la limite déclarée du manuscrit, l'arbitrage et les ressources appartiennent au développeur)

**Le contexte qui fonde la décision (11/11).** Le troisième fichier : « évaluer la cristallisation : proposer un modèle statistique justifiant le seuil de 10 vérifications — ou le remplacer par un critère de confiance séquentiel — et un protocole de réplication… avec grille de codage T/X à double annotation et kappa de Cohen ».

**Les règles.** (1) LE MODÈLE : chaque rebuild est une épreuve de Bernoulli (divergence q) ; le SPRT accepte « déterministe » quand Λₙ = ((1−q₀)/(1−q₁))ⁿ ≥ 1/α — les bornes du projet (q₀ = 1 %, q₁ = 50 %, α = 5 %) donnent n = 5 ; le seuil 10 atteint α = 1,08 × 10⁻³ (≈ 3,3σ). (2) LE SEUIL DEMEURE : la règle R6 est la POLITIQUE de projet — l'analyse la justifie (46× plus strict que nécessaire) et documente la voie d'un relâchement (5 rebuilds au même α que le canonique) — JAMAIS changée en silence. (3) LE PROTOCOLE : le document scripts/preuves_v120/protocole_replication.md (les trois axes avec leurs mesures, la grille T/X — l'EXTENSION naturelle des classes constatées aux douze runs Loupe [les T1-T5 sont exactement les cinq familles du RQ3], la double annotation, le κ de Cohen avec l'interprétation de Landis & Koch, les quatre critères d'acceptation pré-enregistrés, le coût estimé). (4) La grille T/X relie le protocole À L'EXPÉRIENCE VÉCUE : les classes T1-T5 du manuscrit § 4.5/RQ3 SONT la grille — la réplication codera les défauts dans la taxonomie que la méthode a déjà produite.

**Alternatives rejetées.** Remplacer le seuil 10 par le SPRT à 5 — rejeté : changer une règle du cœur exige l'arbitrage du développeur (l'analyse est consignée, la décision lui appartient). Exécuter la réplication à cette édition — rejeté : un second développeur n'est pas au laboratoire ; exécuter le protocole soi-même serait la nier (N = 1 demeure la limite HONNÊTE, le protocole est la voie de sa levée).

**Frontières.** Le protocole est un DOCUMENT PROPOSÉ ; aucune réplication exécutée ; le seuil 10 inchangé ; le manuscrit v0.12.0 déclare la limite et la voie.
"""

ENTREE = """

## Entrée 225 — le TROISIÈME FICHIER D'INSTRUCTION EXÉCUTÉ : LE MODÈLE FORMEL ET LA GOUVERNANCE ASSAINIE v0.12.0 (CF3 modélisé et vérifié — les QUATRE propriétés PROUVÉES DANS LE MODÈLE ; le modèle de menace en DEUX PLANS avec l'ordre intra-sécurité explicite ; la cristallisation JUSTIFIÉE par le SPRT ; le protocole de réplication PROPOSÉ ; les manifestes à sha256 ; D187/D188/D189 ; l'instruction ruim4qzsd ARCHIVÉE) (11/11, la session du modèle)

**La commande et le geste.** Le troisième fichier (Qwen__20261111_ruim4qzsd.txt) : le vérificateur de protocoles sur CF3, le modèle de menace en deux plans, la migration sha256 des manifestes, l'évaluation de la cristallisation, l'intégration au manuscrit — les deux livrables v0.12.0. Le laboratoire exécute INTEGRALEMENT.

**Le modèle formel (D187).** Le choix du vérificateur NOMMÉ : Tamarin/ProVerif absents du laboratoire — l'EXPLORATEUR D'ÉTATS EXPLICITES tient la place (la sémantique opérationnelle de v06/coffre_cf3.py transcrite en machine à états finie abstraite, les primitives SYMBOLIQUES, LE SCRIPT EST LE MODÈLE — scripts/modele_formel_v120.py, reproductible d'un clone frais). L'espace : 154 états, 1 152 transitions (257 refus nommés), profondeur 6, époques ≤ 3, l'adversaire à seuil ≤ 2 éléments (tous les sous-ensembles) AVEC le rejeu d'époques passées et les falsifications des deux côtés. LES QUATRE PROPRIÉTÉS : P1 le secret sous seuil (0 contre-exemple — le KEK lie les trois éléments, le champ verif exige le média : la machine seule ne permet même pas d'ESSAYER des phrases) ; P2 le refus du roll-back (la monotonie structurelle re-constatée MÉCANIQUEMENT transition par transition, le rejeu refusé nommé) ; P3 l'absence de destruction sur phrase erronée (0 contre-exemple — la destruction exige la falsification PROUVÉE) ; P4 le rayon borné à une époque (0 violation — le média est le TÉMOIN jamais le coupable, les fragments CF2 coexistent). LES HYPOTHÈSES A1-A5 EXPLICITES : le symbolique, le seuil, le média jamais enrichi, les anciens couples, le HORS MODÈLE nommé (canaux auxiliaires, implémentation, trois éléments, quantique). LE RAPPORT PAR PROPRIÉTÉ : prouvée DANS LE MODÈLE, réfutée, hors modèle — jamais confondus.

**Le modèle de menace en deux plans (D188).** Le plan IP (la confidentialité d'abord — les pertes REMÉDIABLES : rotation, variantes) et le plan sûreté d'exécution (l'intégrité et la disponibilité d'abord — les pertes IRRÉMÉDIABLES) ; L'ORDRE INTRA-SÉCURITÉ EXPLICITE (la politique qui manquait à D19 : entre les plans, le plan sûreté GAGNE — un coffre cassé ne protège rien) ; la tension D81 ↔ D183 consignée AVEC l'analyse chiffrée (le facteur ≈ 40 en faveur du séquestre Shamir ; D81 DEMEURE — les quatre raisons, le geste au développeur). Le tableau restructuré vit à la spécification v0.12.0 (§ 15) et au manuscrit (§ 4.6).

**La cristallisation (D189).** Le SPRT de Wald : 5 rebuilds identiques atteignent α = 5 %, le seuil historique 10 atteint α = 1,08 × 10⁻³ (46× plus strict) — LE SEUIL DEMEURE (la politique, jamais changée en silence ; l'analyse est la justification consignée). LE PROTOCOLE DE RÉPLICATION : les trois axes (second développeur / second domaine / second profil), la grille T/X (les CINQ classes terrain == les cinq familles du RQ3 — la taxonomie vécue devient la grille), la double annotation, le κ de Cohen ≥ 0,61, les critères pré-enregistrés — PROPOSÉ, jamais exécuté.

**Les manifestes (D187).** maj_kit.py consigne désormais sha256 au manifeste du kit de cérémonie (la suite de D184) ; les kits LIVRÉS demeurent (preuves) ; md5 à l'idempotence Drive et à l'affichage Loupe.

**L'étape de vérification obligatoire (exigée par l'instruction, exécutée avant la livraison).** (a) Le modèle formel EXÉCUTÉ et ses sorties brutes jointes (preuves_v120/modele_formel.csv + rapport — chaque claim du manuscrit correspond à un résultat d'outil). (b) Les autotests CF2/CF3 et de falsification du sceau REJOUÉS aux répertoires temporaires : coffre_cf3 autotest 28 PASS, test_coffre_cf3 92 PASS, test_cf2 54 PASS, test_sceau_I 54 PASS + le dépôt réel VERT (14 arbres) — le conteneur RÉEL constaté IDENTIQUE avant/après (md5), AUCUN chemin réel touché. (c) Les harnais et le garde 14/14 : le rejeu vécu à la session v0.11.0 (Entrée 224, 159+284+131 verts) demeure la référence courante — le garde du sceau re-passé VERT au geste. (d) L'audit de gouvernance VERT (D1..D189, la cohérence D81/D183 vérifiée : les deux décisions vivent l'une contre l'autre au tableau restructuré). (e) La conformité des DEUX archives livrées contrôlée.

**Les livrables.** TRIADE_soumission_v0.12.0.zip (cinq fichiers au plus) et TRIADE_complet_v0.12.0.zip (l'intégralité : le modèle formel AVEC ses sorties, le protocole de réplication, l'analyse SPRT, les sources du manuscrit v0.12.0, la chaîne spec_v120, les données v0.10.0+v0.11.0+v0.12.0, les extraits, les empreintes) — déposés au coffre, l'instruction ruim4qzsd ARCHIVÉE (ARCHIVE/, md5 recoupé après le déplacement).

**Détail.** FRONTIÈRES : aucun artefact scellé ne bouge, aucun arbre signé ne bouge, le coffre réel INTACT, le seuil de cristallisation INCHANGÉ, la réplication NON exécutée, D81 DEMEURE. Le dossier /instructions est VIDE : les trois fichiers exécutés et archivés. SUITE : au développeur — les trois éditions livrées (v0.10.0 le manuscrit, v0.11.0 les preuves renforcées, v0.12.0 le modèle formel) ; les voies ouvertes : la cérémonie d'ère du quinzième arbre (la spec CSPRNG en brouillon), l'arbitrage du séquestre D183, le relâchement SPRT éventuel, la réplication, le DOI Zenodo au dépôt du manuscrit.
"""

W_BLOC = """
Task ID: 132
Agent: Z.ai (agent principal)
Task: LE TROISIÈME FICHIER D'INSTRUCTION EXÉCUTÉ — LE MODÈLE FORMEL
ET LA GOUVERNANCE ASSAINIE v0.12.0 : les quatre propriétés prouvées,
les deux plans, le SPRT, le protocole de réplication, D187/D188/D189,
les deux livrables, l'instruction archivée.

Work Log:
- LE MODÈLE FORMEL (modele_formel_v120.py — le script EST le modèle) :
  154 états, 1 152 transitions, adversaire ≤ 2 éléments + rejeu —
  P1 secret sous seuil / P2 refus du roll-back / P3 pas de destruction
  sur phrase erronée / P4 rayon borné : les quatre PROUVÉES DANS LE
  MODÈLE ; hypothèses A1-A5 explicites, le hors modèle nommé ;
  Tamarin/ProVerif absents — l'explorateur nommé.
- LE MODÈLE DE MENACE EN DEUX PLANS (D188) : IP (remédiable) /
  sûreté (irrémédiable), l'ordre intra-sécurité EXPLICITE (le plan
  sûreté gagne), D81↔D183 chiffrée (facteur ≈ 40 — D81 demeure).
- LA CRISTALLISATION (D189) : le SPRT justifie le seuil 10 (α = 1,08 ×
  10⁻³, 46× plus strict) — le seuil DEMEURE ; le protocole de
  réplication proposé (trois axes, grille T/X == les cinq familles du
  RQ3, double annotation, κ de Cohen ≥ 0,61) — jamais exécuté.
- LES MANIFESTES à sha256 (maj_kit.py, la suite de D184 — les kits
  livrés demeurent, preuves).
- LES AUTOTESTS rejoués aux répertoires temporaires : CF3 28 + 92,
  CF2 54, sceau 54 + dépôt réel VERT — le coffre réel constaté
  IDENTIQUE avant/après, aucun chemin réel touché.
- LE MANUSCRIT v0.12.0 (§ 4.6, 14 pages) + la chaîne spec_v120 + le md
  (§ 1.13, § 19.14) + le PDF consigné n°48.
- LES LIVRABLES au coffre + l'instruction ruim4qzsd ARCHIVÉE (md5
  recoupé) — le dossier /instructions VIDE : les trois exécutés.
- SUITE : au développeur — la cérémonie d'ère (tls13-29), l'arbitrage
  D183, le SPRT éventuel, la réplication, le DOI Zenodo.
"""

D.write_text(D.read_text(encoding="utf-8") + DECISIONS, encoding="utf-8")
J.write_text(J.read_text(encoding="utf-8") + ENTREE, encoding="utf-8")
W.write_text(W.read_text(encoding="utf-8") + W_BLOC, encoding="utf-8")
print("[consignes] D187 + D188 + D189 + Entrée 225 + worklog Task 132")
