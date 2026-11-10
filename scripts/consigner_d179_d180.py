#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consigner D179 + D180 — PAR SCRIPT (la commande « b et c » du développeur :
la version 0.1.1 [la dette soldée à la naissance] ET la consolidation v0.9.0)."""

CHEMIN = "/home/z/my-project/triade/docs/DECISIONS.md"

D179 = """
## D179 — LA VERSION 0.1.1 COMMANDÉE : LA DETTE [R10-PÉRIMÉE] SOLDÉE À LA NAISSANCE (la commande du développeur « b et c » — l'option (c) de l'Entrée 219 : la table des 17 sommes rafraîchie à la version 0.1.1+, à contrat stable) ; LA PIÈCE NAÎT DE LA RECOMPOSITION MÊME (le build calcule la table à la vérité des blocs DEPUIS TOUJOURS — la 0.1.1 la VIT : chaque somme == son bloc relu, PAR CONSTRUCTION ; le qword version porté 0x00010008 → 0x00010101, l'ère 0.1.1-dev.1 ; 0 OCTET AILLEURS — LE CODE BYTE-IDENTIQUE au vécu des ONZE RUNS [R4 : le contrat stable ; R7 : les adresses intactes] ; la pièce 0.1.0 [054de960…] SCELLÉE demeure au git et au coffre [loupe-kit-12]) ; LA CARTE GÉNÉRATION 17 (la 16 demeure celle de la balise 0.1.0 scellée ; LA LECTURE DE LA BALISE DEVIENT GÉNÉRATION-INDÉPENDANTE — l'en-tête signé, jamais le fragment chiffré : un passage d'ère n'aveugle JAMAIS l'anti-rollback) ; L'ANTI-ROLLBACK OUVERT À LA MONOTONIE R10 (la version STRICTEMENT SUPÉRIEURE ouvre la nouvelle ère — (0,1,1,−1,1) > (0,1,0,0,0) ; une pré-version de la balise scellée demeure REFUSÉE : (0,1,0,−1,N) < (0,1,0,0,0), jamais de retour en arrière) ; LE PORT D'ÈRE CONFINÉ AUX CHAMPS NOMMÉS (la pièce déployée ASSERTÉE == LA SCELLÉE 0.1.0 [054de960…] ; tout écart HORS des champs de sommes + le qword version = ÉCHEC NOMMÉ — R4/R7 gardés au geste même) ; LE KIT 0.1.1-dev.1 DÉPOSÉ au coffre /test (loupe-kit-13 aux QUATRE pièces, la vague versionnée vagues-m10, le réceptacle ARMÉ) — LE DOUZIÈME RUN ATTENDU : LE MÊME CRITÈRE que le onzième (le scénario ENTIER T0 → S0 → LA LIAISON ET la vitrine vivante), LA BALISE `loupe 0.1.1` SE SCELLERA sur le vert recoupé (le miroir D165/D170 : la porte est de processus) ; la cristallisation R6 poursuivie au scellage (les passes exigées à la porte — D178 règle 2, la carte à 2/10 au geste de la consignation)

**Le contexte qui fonde la décision (11/11, le message du développeur « b et c »).** L'Entrée 219 avait posé le programme d'après M10 au développeur en trois options ; la commande arrive le jour même : (b) la consolidation v0.9.0 de la spécification ET (c) le soldage de la dette [R10-PÉRIMÉE] à 0.1.1+. D178 l'avait nommé d'avance : « la table se rafraîchira à 0.1.1 le jour où le développeur commandera la version — R4, R10, jamais un hot-fix d'un scellé ».

**Les règles.** (1) **LA DETTE SE SOLDE À LA NAISSANCE** : la nouvelle pièce EST la recomposition (la table véridique par construction, le qword porté) — jamais un patch de la scellée. (2) **LE PORT D'ÈRE PORTE SES GARDES** : la déployée ASSERTÉE scellée 0.1.0, l'écart confiné aux champs nommés (17 sommes + le qword), 0 octet ailleurs — R4/R7 constatés au geste. (3) **LA MONOTONIE EST LA PORTE** : l'anti-rollback R6 s'ouvre à la version strictement supérieure (R10) et à elle seule. (4) **LA BALISE SE SCELLE SUR LE VÉCU** : le kit va au terrain, le scellage de la 0.1.1 attend le verdict du recoup vert DU DOUZIÈME RUN (D165/D170 — la pièce qui se scelle est la pièce qui a couru).

**Alternatives rejetées.** Sceller la 0.1.1 au labo sans run (rejetée : le miroir D165/D170 — le scellage REFUSE en l'absence du verdict du recoup vert ; la 0.1.0 fut scellée sur le onzième run, la 0.1.1 se scellera sur le douzième) ; patcher la table de la pièce scellée en place (rejetée : jamais un hot-fix d'un scellé — D178) ; rouvrir le jalon M10 pour la 0.1.1 (rejetée : M10 est clos sur sa balise ; la 0.1.1 est une version de maintenance à contrat stable, R4) ; hériter les compteurs de cristallisation de la carte 16 (rejetée : la carte 17 est une carte neuve d'une ère neuve — les passes re-vérifient, R6 au sens plein).

**Frontières.** La balise `loupe 0.1.0` SCELLÉE DEMEURE (l'anti-rollback vivant) ; les balises sœurs INTACTES (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0) ; loupe.exe 0.1.1-dev.1 (c1115105…, 127 488 o) — le code byte-identique au vécu des onze runs ; les secrets au seul .keys/ (D12) ; la clé privée jamais traversée (D87). Les pièces : loupe/ (l'ère 0.1.1-dev.1, la carte génération 17), le kit 0.1.1-dev.1 au coffre /test (loupe-kit-13), scripts/porte_ere_011.py, scripts/genere_kit_011_dev1.py, scripts/depot_entree_221.py.
"""

D180 = """
## D180 — LA CONSOLIDATION v0.9.0 : LE PROGRAMME D'APRÈS M10 ENTRE EN SPÉCIFICATION (le modèle D169/D176 — v0.7.0 après M8, v0.8.0 après M9, v0.9.0 après M10 — servie sur la commande du développeur, l'option (b) de l'Entrée 219) ; LE JALON M10 FRANCHI consigné au document (la rangée M10 du § 18 PORTÉE FRANCHIE : ONZE RUNS TERRAIN, ONZE DÉFAUTS NOMMÉS, ONZE RETOUCHES DOCUMENTÉES — LA VITRINE VIVANTE chez son utilisateur, LE ONZIÈME RUN recoupé 39/39, LA BALISE `loupe 0.1.0` SCELLÉE PAR FAIT DE CARTE — LA MÉTHODE TRIADE ENTIÈRE PROUVÉE PAR LA CRÉATION : de l'intention à l'octet vécu) ; LA VERSION 0.1.1-dev.1 COMMANDÉE au document (le § 1.10 réécrit, la correspondance v0.8.4 → v0.9.0 NOUVELLE, l'annexe décisionnelle étendue D177–D180, le journal des versions, la clôture) ; LA CHAÎNE spec_v090 NÉE DE spec_v084 PAR COPIE (l'archive v084 DEMEURE — dd36eb…, e92689ab… aux archives consignées) ; le md PROTOCOLE_TRIADE.md en v0.9.0 ; AUCUNE règle modifiée, AUCUNE couche d'exécution ajoutée, hiérarchie inchangée — le protocole CONSIGNE, il ne légifère pas

**Le contexte qui fonde la décision (11/11).** La consolidation suit le franchissement : M10 franchi le 11/11 (D178), la version 0.1.1 commandée le jour même (D179) — la v0.9.0 consigne L'ÉTAT et OUVRÉ le programme d'après M10 au document.

**Les rejets nommés (v0.9.0).** Rafraîchir la table R10 au scellage de la 0.1.0 (rejeté : la pièce ne bouge jamais au scellage — fait de carte ; la dette se paie à la version suivante, D178) ; sceller la 0.1.1 au build sans le run (rejeté : le miroir D165/D170 exige la pièce) ; rouvrir M10 pour la 0.1.1 (rejeté : version de maintenance à contrat stable, R4) ; modifier les notations D172–D175 (rejeté : le code byte-identique au vécu, les notations décrivent LA PIÈCE — R2/R5).

**Frontières.** Les archives v0.2 → v0.8.4 DEMEURENT ; le Livre du Coffre v1.1 INCHANGÉ ; aucune balise ne bouge ; la dette [R10-PÉRIMÉE] SOLDÉE (D179) ; l'artefact PDF : docs/Protocole_TRIADE_v0.9.0_Specification.pdf (51 pages, sha256 465331b2…, consigné n°39 au registre D134 — pdf_qa WARN, la classe connue des tirets cadratins consignée depuis D133, l'overflow p.32 le faux positif des filets du tableau des jalons).
"""

texte = open(CHEMIN, encoding="utf-8").read()
for marqueur, bloc in (("## D179 —", D179), ("## D180 —", D180)):
    if marqueur in texte:
        print(f"[décisions] {marqueur} y vit déjà")
    else:
        texte += bloc
        print(f"[décisions] {marqueur} consignée")
open(CHEMIN, "w", encoding="utf-8").write(texte)
