#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consigner l'Entrée 223 (l'édition académique v0.10.0) au journal de travail
et le bloc correspondant au worklog — append-only, le format établi.
"""
import pathlib
import datetime

J = pathlib.Path("/home/z/my-project/triade/docs/JOURNAL_TRAVAIL.md")
W = pathlib.Path("/home/z/my-project/triade/worklog.md")

ENTREE = """
## Entrée 223 — « voici 3 fichiers d'instructions à exécuter » : LE PREMIER EXÉCUTÉ — L'ÉDITION ACADÉMIQUE v0.10.0 (le manuscrit IMRAD en anglais, résumé français inclus, né du dépôt ; D182/D183/D184 ; les livrables soumission et complet ; le fichier d'instruction ARCHIVÉ au coffre) (11/11, la session de l'édition)

**La commande et le geste.** Le développeur dépose TROIS fichiers d'instructions au dossier `/instructions` du coffre (créé au geste même) : « archive chaque fichier dès que son exécution est terminée ». Le PREMIER (Qwen\\_\\_20261111\\_pleo7tfy9.txt) ordonne l'édition académique publiable à partir du dépôt — le présent numéro consigne son exécution INTÉGRALE ; les deuxième et troisième (v0.11.0, v0.12.0) attendent leur session. NB : l'instruction nommait ses décisions D181–D183 ; D181 étant consommée par la balise `loupe 0.1.1` (Entrée 222), la numérotation COULISSE d'un cran — D182/D183/D184, l'ordre et le contenu tenus.

**Le manuscrit (la chaîne scripts/manuscrit_v100/ — main.tex, refs.bib, donnees/ GÉNÉRÉES).** Une édition IMRAD en anglais, résumé français inclus, dix pages : QUATRE questions de recherche en introduction (le taux de défauts échappés, le coût en tokens par changement validé, les classes invisibles à l'émulation, la sûreté du patch à chaud) ; Methods (le protocole en bref, la gouvernance à intention signée, L'ÉPISTÉMOLOGIE ORACLE/TERRAIN, l'agent décrit — Z.ai GLM, le journal et le worklog pour transcripts, JAMAIS co-auteur, l'auteur humain unique : Alexis Lopez) ; Results (RQ1 : onze itérations fautives sur douze, onze classes nommées, la vitrine vivante aux runs 10–12 ; RQ2 : 51/719/1 088 tokens mesurés contre 64/3 000/6 000, la lignée 13 873 ; RQ3 : les CINQ familles invisibles à l'émulation — chargeur/image, ABI/SSE, chargeur de bibliothèque, codes d'erreur, hypothèses du harnais — CHACUNE avec sa preuve ; RQ4 : zéro régression post-patch, la boucle vécue M2, fence.i M7, l'anti-rollback armé) ; Discussion (ce que les données soutiennent et NE soutiennent PAS) ; Threats to Validity (N=1, la circularité de l'oracle, l'absence de baseline, la sécurité mémoire non prouvée, le temps constant non analysé) ; Related Work (design by contract, N-version, property-based testing, DO-178C, reproducible builds/in-toto/SLSA/TUF/Sigstore, cérémonies DNSSEC, Shamir 1979, live patching kpatch/DSU, repo-maps et budgets de contexte — la nouveauté revendiquée est L'INTÉGRATION, pas les primitives) ; les déclarations Ethics/dual-use, Data Availability (DOI Zenodo À CRÉER — le manuscrit le dit honnêtement), Use of AI, Acknowledgements. **LA FORMULATION CORRIGÉE** (exigée par l'instruction) : « aucune chaîne de traduction optimisante ni opaque ; assemblage WYSIWYG vérifié par round-trip » (plus jamais « le compilateur disparaît ») ; « l'évolution du code volé est bloquée, son exécution ne l'est pas » ; les termes standards (key ceremony, signed manifest, sealed build) ; D19 requalifiée politique de projet explicite. **LES DONNÉES SONT GÉNÉRÉES, JAMAIS TAPÉES** : scripts/extraire\\_donnees\\_v100.py extrait ET VÉRIFIE (refus si une ancre manque au journal) — 11 jalons, 7 budgets, 10 volumes d'oracle, 12 runs Loupe, 3 empreintes scellées (loupe 0.1.1 c1115105… RECENSÉE SUR LA PIÈCE, loupe 0.1.0 054de960…, proxy 1.0.0 446279f3…) ; les tableaux du manuscrit sont \\input depuis donnees/tables\\_generees.tex — LE MANUSCRIT N'AFFIRME RIEN QUI NE SOIT EXTRAIT ET VÉRIFIÉ. La bibliographie : chaque entrée porte un DOI ou une référence institutionnelle vérifiable (les listes d'auteurs in-toto et Sigstore recoupées aux sources avant consignation).

**La spécification v0.10.0 (la chaîne spec_v100 née de spec_v090 PAR COPIE — l'archive v090 demeure).** Le md PROTOCOLE_TRIADE.md porté (l'annonce, le § 1.11 « Ce que change la v0.10.0 », le § 19.12 la correspondance v0.9.0 → v0.10.0 avec ses rejets, le journal des versions, le paragraphe de clôture) ; la chaîne LaTeX : l'annexe A « Empreintes md5 » DEVIENT « Empreintes sha-256 des modules du dépôt » (D184 — les QUINZE modules recalculés au contenu canonique LF, les césures posées tous les 16 hex pour la mise en page) ; l'annexe décisionnelle étendue D181–D184 ; le PDF formel docs/Protocole\\_TRIADE\\_v0.10.0\\_Specification.pdf (54 pages, sha256 consigné au registre D134 ; pdf_qa : la classe connue des tirets cadratins + l'overflow p.33 HÉRITÉ de la v0.9.0 — le même tableau des jalons, le même constat au PDF scellé v0.9.0).

**Les décisions (append-only).** D182 (l'édition académique : le manuscrit, la formulation, l'auteur unique, les déclarations, les livrables, les règles) ; D183 (LA PROPOSITION de séquestre chiffré de la phrase de contrôle — l'alternative à la garde durable D81, avec L'ANALYSE COMPARATIVE CHIFFRÉE perte/exposition : sous D81 la perte espérée ≈ 4,0 × 10⁻²·C\\_exposition/an contre ≈ 1,0 × 10⁻³ sous Shamir 5/3 réparti — un facteur ~40 ; la variante clé hors-ligne unique ÉCARTÉE par l'analyse elle-même : point de défaillance unique ; D81 DEMEURE la décision active, RIEN d'appliqué, aucune clé touchée) ; D184 (les empreintes de gouvernance migrent md5 → sha-256 : l'annexe A recalculée, md5 demeure une fonctionnalité d'affichage de Loupe, AUCUN octet de la pièce ne change, les preuves historiques md5 DEMEURENT — les preuves ne se réécrivent jamais).

**L'étape de vérification obligatoire (exigée par l'instruction, exécutée AVANT la livraison).** (a) Chaque affirmation factuelle renvoie à une entrée de journal ou d'archive — les données sont GÉNÉRÉES par le script d'extraction qui REFUSE si une ancre manque ; chaque citation possède un DOI ou une référence vérifiable (la bibliographie recoupée). (b) Les empreintes sha256 de loupe.exe et proxy.exe RECALÉES contre le journal et la carte : loupe.exe == c1115105… (la pièce INTACTE, byte pour byte), proxy.exe == 446279f3… — l'identité octet pour octet des artefacts scellés CONFIRMÉE. (c) L'audit de gouvernance (scripts/audit\\_gouvernance\\_v100.py : les champs des décisions, l'unicité des ID, le chaînage des amendements, les entrées du journal) VERT ; le vérificateur du sceau 14/14 (les QUATORZE arbres, docs/ hors sceau). (d) La conformité des DEUX archives livrées contrôlée (le zip soumission : CINQ fichiers au plus, readme inclus, le manuscrit en pdf, le numéro v0.10.0 aux noms ; le zip complet : l'intégralité — sources, bibliographie, données, script, extraits, empreintes).

**Les livrables.** TRIADE\\_soumission\\_v0.10.0.zip (cinq fichiers au plus : le README d'abord, le manuscrit PDF, les tableaux CSV, les empreintes) et TRIADE\\_complet\\_v0.10.0.zip (l'intégralité) — déposés au coffre Drive racine, le fichier d'instruction Qwen\\_\\_20261111\\_pleo7tfy9.txt ARCHIVÉ (déplacé vers ARCHIVE/, md5 recoupé après le déplacement — le geste exigé par la commande : « archive chaque fichier dès que son exécution est terminée »).

**Détail.** FRONTIÈRES : aucun artefact scellé ne bouge (loupe.exe, proxy.exe, les balises INTACTES) ; aucun arbre signé ne bouge (le garde 14/14 le constate) ; aucune clé touchée (D183 est une PROPOSITION) ; les preuves historiques md5 inchangées (D184 : les preuves ne se réécrivent jamais) ; la chaîne spec_v090 et le PDF v0.9.0 archivés INTACTS. Livrables : manuscrit\\_v100/, spec\\_v100/, extraire\\_donnees\\_v100.py, audit\\_gouvernance\\_v100.py, verifier\\_edition\\_v100.py, les décisions D182–D184, la présente entrée. SUITE : LE DEUXIÈME FICHIER D'INSTRUCTION (v0.11.0 — renforcer le niveau de preuve : mutation testing, fuzzing guidé, sûreté mémoire statique, dudect, benchmarks, indépendance de l'oracle, D185+), puis le troisième (v0.12.0 — le vérificateur de protocoles, le modèle de menace en deux plans, la cristallisation, D186+).
"""

W_BLOC = """
Task ID: 130
Agent: Z.ai (agent principal)
Task: LE PREMIER FICHIER D'INSTRUCTION EXÉCUTÉ — L'ÉDITION ACADÉMIQUE
v0.10.0 : le manuscrit IMRAD en anglais (résumé français) né du dépôt,
D182/D183/D184, les deux livrables, l'instruction archivée.

Work Log:
- LE MANUSCRIT (manuscrit_v100/) : IMRAD anglais 10 p., quatre RQ,
  la formulation corrigée (WYSIWYG par round-trip ; l'évolution du code
  volé bloquée, son exécution non ; termes standards ; D19 requalifiée
  politique de projet), l'auteur humain unique (l'agent en méthodes et
  remerciements), Ethics/Data/Limitations, la bibliographie à DOI
  vérifiables (auteurs in-toto/Sigstore/RepoCoder recoupés aux sources).
- LES DONNÉES GÉNÉRÉES (extraire_donnees_v100.py) : 11 jalons, 7
  budgets (51/719/1088), 10 oracles, 12 runs Loupe, 3 empreintes
  scellées — chaque valeur ancrée au journal, le script REFUSE si une
  ancre manque ; les tableaux \input depuis donnees/.
- LA SPÉCIFICATION v0.10.0 : md porté (§ 1.11, § 19.12, versions) ;
  chaîne spec_v100 née de spec_v090 ; l'annexe A md5 → sha256 (D184,
  les 15 modules au contenu canonique LF) ; annexe décisionnelle
  D181-D184 ; le PDF 54 pages consigné au registre.
- LES DÉCISIONS : D182 (l'édition), D183 (le séquestre chiffré —
  PROPOSITION documentée avec l'analyse perte/exposition chiffrée,
  facteur ~40 en faveur du Shamir 5/3, RIEN d'appliqué), D184
  (gouvernance sha-256, md5 = fonctionnalité Loupe, les preuves
  historiques demeurent).
- LA VÉRIFICATION (l'étape obligatoire de l'instruction) : (a) données
  générées/vérifiées, citations à DOI ; (b) loupe.exe == c1115105…,
  proxy.exe == 446279f3… byte pour byte ; (c) l'audit de gouvernance
  VERT + le sceau 14/14 ; (d) les deux zips contrôlés.
- LE COFFRE : les deux livrables à la racine du coffre Drive,
  l'instruction pleo7tfy9 ARCHIVÉE (ARCHIVE/, md5 recoupé après).
- SUITE : le deuxième fichier (v0.11.0 — renforcer le niveau de
  preuve, D185+), puis le troisième (v0.12.0 — la vérification
  formelle, D186+).
"""

src = J.read_text(encoding="utf-8")
src += ENTREE
J.write_text(src, encoding="utf-8")

w = W.read_text(encoding="utf-8")
w += W_BLOC
W.write_text(w, encoding="utf-8")

print("[journal] Entrée 223 consignée + worklog Task 130")
