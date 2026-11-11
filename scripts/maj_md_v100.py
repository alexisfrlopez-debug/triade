#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Porter docs/PROTOCOLE_TRIADE.md à la v0.10.0 (l'édition académique, D182) :
en-tête de version, § 1.11, correspondance § 19.12, journal des versions,
paragraphe de clôture. Aucune règle modifiée — le modèle D180.
"""
import pathlib

p = pathlib.Path("/home/z/my-project/triade/docs/PROTOCOLE_TRIADE.md")
src = p.read_text(encoding="utf-8")

# 1) Le bloc d'annonce de l'en-tête : la v0.10.0 avant le récit v0.9.0
annonce = """> La v0.10.0 consigne L'ÉDITION ACADÉMIQUE (D182, la commande du développeur du
> 11/11 : trois fichiers d'instructions au dossier `/instructions` du coffre) :
> le manuscrit IMRAD en anglais (résumé français inclus) — quatre questions de
> recherche (défauts échappés, coût en tokens par changement validé, classes
> invisibles à l'émulation, sûreté du patch à chaud), les données réelles du
> journal EXTRAITES PAR SCRIPT, la formulation corrigée (aucune chaîne de
> traduction optimisante ni opaque — assemblage WYSIWYG vérifié par round-trip ;
> l'évolution du code volé est bloquée, son exécution ne l'est pas ; les termes
> standards de l'ingénierie ; D19 requalifiée politique de projet explicite),
> l'auteur humain unique (l'agent IA en méthodes et remerciements, jamais
> co-auteur), les déclarations Ethics/dual-use, Data Availability, Limitations ;
> la proposition D183 (le séquestre chiffré de la phrase de contrôle —
> documentée, NON appliquée au coffre réel) ; l'annexe A portée à sha-256
> (D184 — md5 demeure une fonctionnalité d'affichage de Loupe, aucun octet de
> la pièce ne change) ; les livrables `TRIADE_soumission_v0.10.0.zip` (cinq
> fichiers au plus, readme inclus, le manuscrit en pdf) et
> `TRIADE_complet_v0.10.0.zip` (l'intégralité). Aucune règle modifiée, aucune
> couche d'exécution ajoutée, hiérarchie inchangée — l'édition consigne, elle
> ne légifère pas.

> La v0.9.0 consolide le programme d'après M10 (D178/D179) : LE JALON M10 — le test"""
src = src.replace("> La v0.9.0 consolide le programme d'après M10 (D178/D179) : LE JALON M10 — le test",
                  annonce, 1)

# 2) La ligne « - Version : » courante
vieux = "- Version : v0.9.0 — la révision de consolidation du programme d'après M10 (D178/D179) :"
nouveau = ("- Version : v0.10.0 — la révision de L'ÉDITION ACADÉMIQUE (D182/D183/D184) : "
           "le manuscrit IMRAD en anglais (résumé français) né du dépôt — quatre questions "
           "de recherche, les données du journal extraites par script "
           "(`extraire_donnees_v100.py`, le manuscrit n'affirme rien qui ne soit vérifié), "
           "la formulation corrigée dans les termes standards de l'ingénierie, l'auteur "
           "humain unique, les déclarations Ethics/Data/Limitations ; la proposition D183 "
           "(séquestre chiffré de la phrase de contrôle — alternative documentée à la garde "
           "durable D81, NON appliquée au coffre réel) ; l'annexe A de gouvernance portée à "
           "sha-256 (D184 — md5 demeure une fonctionnalité d'affichage de Loupe) ; les "
           "livrables soumission (cinq fichiers au plus) et complet. Sous la v0.9.0, la "
           "consolidation du programme d'après M10 (D178/D179/D180/D181 : la balise "
           "`loupe 0.1.1` scellée sur le douzième run recoupé 39/39)")
assert vieux in src
src = src.replace(vieux, nouveau, 1)
src = src.replace("- Date : 11 novembre 2026", "- Date : 11 novembre 2026 (édition académique)", 1)

# 3) § 1.11 après le § 1.10 (avant « ## 2. »)
s111 = """
### 1.11 Ce que change la v0.10.0

La révision de **l'édition académique** (D182, la commande du développeur du 11/11).
La présente révision **consigne** ; elle ne modifie AUCUNE règle, n'ajoute AUCUNE
couche d'exécution, laisse la hiérarchie de la fonction objectif inchangée — le
modèle D180 : le protocole consigne, il ne légifère pas.

**Le manuscrit académique** (`docs/TRIADE_manuscrit_v0.10.0.pdf`, la chaîne
`scripts/manuscrit_v100/`) : une édition IMRAD en anglais (résumé français inclus),
structurée autour de quatre questions de recherche — le taux de défauts échappés
(onze classes nommées sur douze runs terrain du TGN « Loupe »), le coût en tokens
par changement validé (51 / 719 / 1 088 mesurés M1, D31/D34), les classes de
défauts invisibles à l'émulation (cinq familles : chargeur/image, ABI/SSE,
sémantique du chargeur de bibliothèque, conventions de codes d'erreur, hypothèses
du harnais), la sûreté du patch à chaud (zéro régression post-patch, monotonie
signée, anti-rollback armé). L'auteur humain est unique ; l'agent IA est décrit en
méthodes et remerciements, jamais co-auteur. Les déclarations Ethics/dual-use
(outil de pentest autorisé — le projet ne porte AUCUN mécanisme de furtivité),
Data Availability (dépôt + DOI Zenodo à créer au dépôt), Limitations (N=1,
circularité de l'oracle, absence de baseline, sécurité mémoire non prouvée, temps
constant non analysé) sont explicites. Chaque donnée du manuscrit est GÉNÉRÉE
depuis le journal par `scripts/extraire_donnees_v100.py` — le manuscrit n'affirme
rien qui ne soit extrait et vérifié.

**La formulation corrigée** : « le compilateur disparaît » devient « aucune chaîne
de traduction optimisante ni opaque ; assemblage WYSIWYG vérifié par round-trip » ;
« code volé inexploitable » devient « l'évolution du code volé est bloquée, son
exécution ne l'est pas » ; les majuscules emphatiques et le vocabulaire
sacralisant cèdent aux termes standards (key ceremony, signed manifest, sealed
build) ; l'invariant D19 (Sécurité > Performance > Optimisation > Coût en tokens)
est requalifié **politique de projet explicite** — la hiérarchie demeure la règle
du projet, dite dans les termes de l'ingénierie.

**La proposition D183** (documentée, NON appliquée au coffre réel) : le séquestre
chiffré de la phrase de contrôle — l'alternative à la garde durable D81 (la phrase
en clair au dépôt et au coffre Drive, l'arbitrage PERTE > EXPOSITION). La
proposition : la phrase chiffrée vers une clé hors-ligne, ou partagée en parts
Shamir à seuil, la phrase en clair retirée du dépôt. L'analyse comparative
chiffrée des risques perte/exposition vit dans la décision D183. Le coffre réel
du développeur DEMEURE à la garde D81 — aucune clé touchée, aucun conteneur
réécrit : la proposition attend le geste du développeur.

**L'annexe A portée à sha-256** (D184) : les empreintes de gouvernance de l'annexe
A (les modules du coffre) passent de md5 à sha-256 — la même méthode au contenu
canonique LF, l'empreinte longue. md5 demeure UNIQUEMENT une fonctionnalité
d'affichage de Loupe (le panneau d'empreintes, loupe-06) : AUCUN octet de la
pièce ne change, et les empreintes md5 des preuves historiques (le journal, les
archives) demeurent ce qu'elles sont — les preuves ne se réécrivent jamais.

**Les livrables** : `TRIADE_soumission_v0.10.0.zip` (cinq fichiers au plus,
readme inclus, le manuscrit en pdf — prêt pour un comité de révision) et
`TRIADE_complet_v0.10.0.zip` (l'intégralité : sources LaTeX, bibliographie,
tableaux de données, script d'extraction, extraits de journal, empreintes). La
v0.9.0 demeure : ses sources et son PDF archivés à `docs/`, la chaîne
`spec_v090` intacte — chaque édition vit à sa chaîne.

"""
ancre = "## 2. La couche I : format normalisé des spécifications"
assert ancre in src
src = src.replace(ancre, s111 + ancre, 1)

# 4) § 19.12 après le § 19.11 (avant « ## 20. »)
s1912 = """### 19.12 Correspondance v0.9.0 → v0.10.0

| Évolution | En v0.9.0 | En v0.10.0 | Statut |
|---|---|---|---|
| Édition académique | — (le manuscrit n'existe pas ; l'article v0.4 de la démonstration RoomEq demeure) | LE MANUSCRIT IMRAD en anglais (résumé français), quatre questions de recherche, les données réelles du journal extraites par script, l'auteur humain unique, l'agent IA en méthodes et remerciements, les déclarations Ethics/Data/Limitations (D182) | nouveau (D182) |
| Formulation | « le compilateur disparaît » ; « code volé inexploitable » ; majuscules emphatiques | « aucune chaîne de traduction optimisante ni opaque ; assemblage WYSIWYG vérifié par round-trip » ; « l'évolution du code volé est bloquée, son exécution ne l'est pas » ; termes standards (key ceremony, signed manifest, sealed build) ; D19 requalifiée politique de projet explicite | révisé (D182) |
| Garde de la phrase de contrôle | D81 : la phrase en clair au dépôt et au coffre Drive (PERTE > EXPOSITION) | D81 DEMEURE la décision active ; la PROPOSITION D183 (séquestre chiffré : clé hors-ligne ou parts Shamir à seuil, analyse chiffrée perte/exposition) documentée — NON appliquée au coffre réel, aucune clé touchée | proposition (D183) |
| Annexe A (empreintes de gouvernance) | md5 des 15 modules du coffre (contenu canonique LF, D133) | sha-256 des 15 modules (la même méthode, D184) ; md5 demeure une fonctionnalité d'affichage de Loupe (loupe-06) — AUCUN octet de la pièce ne change ; les preuves historiques md5 demeurent | révisé (D184) |
| Livrables d'édition | — | `TRIADE_soumission_v0.10.0.zip` (cinq fichiers au plus, readme inclus, le manuscrit en pdf) et `TRIADE_complet_v0.10.0.zip` (l'intégralité) | nouveau (D182) |
| Chaîne PDF | spec_v090 (née spec_v084) ; les archives v0.7.0 à v0.8.4 demeurent | chaîne spec_v100 (née spec_v090) + la chaîne manuscrit_v100 ; les archives demeurent | révisé (D182) |

Modifications explicitement rejetées (v0.10.0) : appliquer D183 au coffre réel
sans le geste du développeur — rejeté : la proposition est documentée, l'arbitrage
PERTE > EXPOSITION demeure la décision active (D81). Réécrire les empreintes md5
des preuves historiques en sha-256 — rejeté : les preuves sont immuables, la
migration ne porte que sur la documentation de gouvernance vivante. Toucher à la
pièce Loupe (le panneau md5) — rejeté : md5 y est une fonctionnalité d'affichage
(RFC 1321 notée à la spécification loupe-06), l'artefact scellé ne bouge jamais.
Modifier les règles ou la hiérarchie — rejeté : l'édition consigne, elle ne
légifère pas (D180).

"""
ancre20 = "## 20. Glossaire"
assert ancre20 in src
src = src.replace(ancre20, s1912 + ancre20, 1)

# 5) Journal des versions : la rangée v0.10.0 en tête
rangée = ("| v0.10.0 | 11 nov. 2026 | Révision de L'ÉDITION ACADÉMIQUE (D182/D183/D184) : "
          "le manuscrit IMRAD en anglais (résumé français) — quatre questions de recherche, "
          "les données réelles du journal extraites par script, la formulation corrigée "
          "(WYSIWYG par round-trip ; l'évolution du code volé bloquée, son exécution non ; "
          "termes standards ; D19 requalifiée politique de projet), l'auteur humain unique, "
          "l'agent IA en méthodes et remerciements, les déclarations Ethics/Data/Limitations ; "
          "la proposition D183 (séquestre chiffré de la phrase de contrôle — documentée, non "
          "appliquée) ; l'annexe A portée à sha-256 (D184 — md5 demeure une fonctionnalité de "
          "Loupe) ; les livrables soumission et complet. La balise `loupe 0.1.1` scellée sur "
          "le douzième run recoupé (D181) est consignée à la rangée M10. Aucune règle "
          "modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |\n")
ancre_v090 = "| v0.9.0 | 11 nov. 2026 |"
assert ancre_v090 in src
src = src.replace(ancre_v090, rangée + ancre_v090, 1)

# 6) Le paragraphe de clôture
cloture_vieille = "La présente version consigne LA RÉVISION DE CONSOLIDATION DU PROGRAMME D'APRÈS M10 (v0.9.0, D178/D179) :"
cloture_nouvelle = """La présente version consigne LA RÉVISION DE L'ÉDITION ACADÉMIQUE (v0.10.0, D182) : le
protocole entre en manuscrit — quatre questions de recherche, les données réelles
du journal extraites par script, la formulation corrigée dans les termes standards
de l'ingénierie, l'auteur humain unique, l'agent IA décrit en méthodes et
remerciements, les déclarations Ethics/Data/Limitations explicites (N=1, la
circularité de l'oracle, l'absence de baseline, la sécurité mémoire non prouvée,
le temps constant non analysé) ; la proposition D183 (le séquestre chiffré de la
phrase de contrôle) documentée sans être appliquée ; l'annexe A de gouvernance
portée à sha-256. La version précédente (v0.9.0) avait consigné LA RÉVISION DE
CONSOLIDATION DU PROGRAMME D'APRÈS M10 (D178/D179) :"""
assert cloture_vieille in src
src = src.replace(cloture_vieille, cloture_nouvelle, 1)

p.write_text(src, encoding="utf-8")
print("[md] PROTOCOLE_TRIADE.md porté à la v0.10.0 (annonce, § 1.11, § 19.12, "
      "journal des versions, clôture)")
