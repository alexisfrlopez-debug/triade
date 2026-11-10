#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consigner l'Entrée 221 + le PLAN (l'ère 0.1.1 ouverte) + le worklog Task
128 — PAR SCRIPT (la commande « b et c » : la version 0.1.1 [D179] ET la
consolidation v0.9.0 [D180])."""

import os

R = "/home/z/my-project/triade"

ENTREE_221 = """## Entrée 221 — « b et c » : LA VERSION 0.1.1 NÉE DE LA RECOMPOSITION (LA DETTE [R10-PÉRIMÉE] SOLDÉE À LA NAISSANCE) ET LA CONSOLIDATION v0.9.0 DE LA SPÉCIFICATION — LE DOUZIÈME RUN ATTENDU (11/11)

**Le fait (la commande du développeur).** Le message « b et c » tranche les trois options de l'Entrée 219 : (b) LA CONSOLIDATION v0.9.0 et (c) LE SOLDAGE DE LA DETTE [R10-PÉRIMÉE] À 0.1.1+. D178 l'avait nommé d'avance : « la table se rafraîchira à 0.1.1 le jour où le développeur commandera la version — R4, R10, jamais un hot-fix d'un scellé ».

**(c) LE GESTE 0.1.1 (D179).** LE PORT D'ÈRE : layout.py VERSION_DEV 0x00010008 → 0x00010101, VERSION_FINALE 0x00010100 ; carte_m10.py GÉNÉRATION 17 (« 0.1.1-dev.1 » / « 0.1.1 ») ; build_loupe.py — **_version_carte DEVENUE GÉNÉRATION-INDÉPENDANTE** (l'en-tête SIGNÉ, jamais le fragment chiffré : le passage d'ère n'aveugle jamais l'anti-rollback — la leçon de conception du geste), **_anti_rollback OUVERT À LA MONOTONIE R10** ((0,1,1,−1,1) > (0,1,0,0,0) : la version strictement supérieure ouvre l'ère ; une pré-version de la balise scellée demeure refusée), **_porte_ere_011** (la déployée ASSERTÉE == LA SCELLÉE 0.1.0 [054de960…] ; l'écart CONFINÉ aux champs nommés — les sommes de la porte R10 + le qword version — 0 octet ailleurs : R4/R7 gardés au geste même). LE BUILD VERT : garde 14/14, les TROIS ancres R7 intactes, 18/18 notations round-trip, 43 verrous, 78 appels IAT audités, l'héritage double preuve, la composition intégrale comptée, **LES TROIS HARNAIS 61/61 · 53/53 · 45/45** — puis **« [0.1.1] LA DETTE [R10-PÉRIMÉE] SOLDÉE À LA NAISSANCE : 17 sommes rafraîchies à la vérité des blocs, le qword porté 0x10008 → 0x10101, 0 octet ailleurs — le code BYTE-IDENTIQUE au vécu des onze runs (R4/R7) »** ; **loupe.exe 0.1.1-dev.1 NÉE — sha256 c111510535767a40…, 127 488 o** ; la carte GÉNÉRATION 17 écrite (lignée D80, graine durable D144 — le témoin ne bouge pas), le verrou croisé 26/26, le tableau de bord de l'ère. UNE PASSE DE CRISTALLISATION vécue : la recomposition == la pièce déployée (PLUS AUCUN écart [R10-PÉRIMÉE] — la dette soldée, CONSTATÉE), les compteurs 26 × 2/10 (les passes jusqu'à 10/10 se jouent au scellage — D178 règle 2, exigées à la porte).

**LE KIT 0.1.1-dev.1.** genere_kit_011_dev1.py : la pièce recopiée (sha256 c1115105… ASSERTÉ), le scénario dev.12 PORTÉ (SHA_EXE + VERSION_R10 0x00010101 + le docstring de l'ère — py_compile VERT), le témoin vitrine (les deux littéraux), le LISEZMOI (LE CHAPITRE 0.1.1 : l'ère 0.1.0 refermée sur sa balise scellée, la version commandée, la dette soldée, LE DOUZIÈME RUN — le même critère, la balise `loupe 0.1.1`) — kit-loupe.zip 38 585 o md5 dadfb48c…, extraction VIERGE, les QUATRE pièces du contrat. L'ARBRE PORTÉ : loupe/terrain/ == le kit 0.1.1-dev.1 (scenario 77872b71…, bat 2a3f22f4…, LISEZMOI 70340163…), loupe/loupe.exe == c1115105… — la consignation et l'arbre disent LA MÊME CHOSE.

**LE COFFRE (depot_entree_221.py).** LA VAGUE 0.1.1-dev.1 VERSIONNÉE → archives-livraisons/vagues-m10/ [kit-loupe-0.1.1-dev.1.zip dadfb48c… + LISEZMOI-loupe-0.1.1-dev.1.txt 70340163… — l'archive poursuit : dev.1 → dev.12 + 0.1.1-dev.1] ; LA RACINE PORTÉE [kit-loupe.zip dadfb48c… + LISEZMOI-loupe.txt 70340163… + loupe-kit-13/ aux QUATRE pièces : loupe.exe md5 5fc07b78…, scenario 77872b71…, bat 2a3f22f4…, LISEZMOI — recoupés] ; LE RÉCEPTACLE preuves-loupe/ RÉ-ARMÉ [LISEZMOI-preuves.txt 79781694… — le douzième run attend ses pièces : temoin-loupe.txt + temoin-vitrine.txt REQUIS + temoin-fichier.bin + captures] ; L'INDEX des livraisons mis à jour [4ae0c72f…] ; la racine 27 entrées, AUCUN doublon (la leçon [CORBEILLE-VIDE] tenue : chaque remplacement à l'unicité).

**(b) LA CONSOLIDATION v0.9.0 (D180).** LE MD : PROTOCOLE_TRIADE.md en v0.9.0 (revision_v090_md.py + le complément — 9 remplacements assertés : le titre, la source, les archives v0.8.x, l'en-tête, la ligne Version, § 1.10 RÉÉCRIT [la consolidation du programme d'après M10], la rangée M10 du § 18 PORTÉE **franchi** [onze runs, onze défauts, onze retouches — la story entière], le préambule, le journal des versions [+ l'entrée v0.9.0], la clôture RÉÉCRITE ; § 19.11 NOUVEAU [la correspondance v0.8.4 → v0.9.0 + les QUATRE rejets]). LA CHAÎNE spec_v090 NÉE DE spec_v084 PAR COPIE (revision_v090_tex.py — l'archive v084 DEMEURE) : main 3, cover 2 (le sous-titre RÉÉCRIT — le chevauchement 30px du pied de page NOMMÉ et réparé, la date portée), merge 1, sec-cf 2 (l'ère du TGN ACCOMPLIE — les phrases périmées guéries), sec-a § 1.10 RÉÉCIT, sec-d [la rangée M10 FRANCHIE + le préambule + la ligne de chaîne + la correspondance v0.8.4 → v0.9.0 NOUVELLE + l'intro du journal + le titre du tableau D75–D180 + l'annexe ÉTENDUE D177–D180], verify_spec PORTÉ [5 contrôles à l'ère : M10 franchi, l'annexe à D180, 51 pages, la clôture, l'extraction jointe TLS1.3pur] ; build_pdf.sh → la chaîne spec_v090. **L'ARTEFACT : docs/Protocole_TRIADE_v0.9.0_Specification.pdf — 51 pages, 1 058 254 o, sha256 465331b2a1cd…, md5 3338525f…, EMPOINTE consignée n°39 au registre D134** ; pdf_qa WARN (12 advisories : la classe des tirets cadratins consignée depuis D133 ; l'overflow p.32 le faux positif des filets du tableau des jalons). **LES PREUVES : LE CAHIER spec_v090/verify_spec.py : TOUT PASSÉ** (V1-V16 : hiérarchie intacte, règles intactes, l'héritage v0.5.0-v0.8.4 intact, § 12.4 les TREIZE arbres + la dette du quatorzième SOLDÉE, l'ère du TGN ACCOMPLIE, jalons M0-M10 FRANCHIS, la correspondance v0.8.4 → v0.9.0, l'annexe D177-D180, D179/D180 consignées, AUCUNE référence non résolue, aucun placeholder) ; **CONTRÔLE VISUEL PAR CODE (controle_visuel_v090.py : 51 pages rendues, AUCUNE quasi blanche, la couverture pleine page sombre)** + les pages clés constatées à la couche texte (la couverture v0.9.0, § 1.10 p.7, la rangée M10 p.31, la correspondance p.42, l'annexe close sur D180 p.50).

**Détail.** FRONTIÈRES : la balise `loupe 0.1.0` SCELLÉE DEMEURE (l'anti-rollback vivant — la 0.1.1 s'ouvre à la monotonie, jamais elle ne referme l'ancienne) ; les balises sœurs INTACTES ; la pièce 0.1.0 (054de960…) au git et au coffre ; les notations D172-D175 INTACTES (R2 — la 0.1.1 ne touche AUCUN octet de notation : la table est un geste de BUILD) ; les secrets au seul .keys/ (D12) ; la clé privée jamais traversée (D87). Consignations : D179 PAR SCRIPT, D180 PAR SCRIPT, le PLAN (l'État + la rangée (e) étendue), la présente Entrée, worklog +Task ID 128. SUITE : LE DOUZIÈME RUN — le kit loupe-kit-13/ au coffre /test, python scenario-loupe.py (T0 → S0 → LA LIAISON), LA VITRINE PAR SON TÉMOIN (temoin-vitrine.bat, les deux codes, le [4/4]), preuves-loupe/ ENTIER au coffre QUEL QUE SOIT le verdict ; le labo rapatrie, recoupe, complète la cristallisation 10/10 puis LE SCELLAGE 0.1.1 (les portes adaptées au verdict du douzième run — le miroir D165/D170) ; si le vert tient : LA BALISE `loupe 0.1.1` SCELLÉE — LA VERSION DE LA DETTE SOLDÉE.

"""

PLAN_ETAT = """**LA VERSION 0.1.1-dev.1 COMMANDÉE le 11/11/2026 (Entrée 221, D179) : LA DETTE [R10-PÉRIMÉE] SOLDÉE À LA NAISSANCE — la pièce née de la recomposition même (les 17 sommes rafraîchies à la vérité des blocs, le qword porté 0x00010101, 0 octet de code changé — R4/R7), la carte génération 17, le kit loupe-kit-13/ au coffre /test, LE DOUZIÈME RUN ATTENDU : si le vert tient, LA BALISE `loupe 0.1.1` SCELLÉE sur run recoupé (le miroir D165/D170) ; ET LA CONSOLIDATION v0.9.0 SERVIE (D180) : la spécification documente le programme d'après M10 — le § 1.10, la rangée M10 FRANCHIE, la correspondance v0.8.4 → v0.9.0, l'annexe D177–D180, le PDF formel 51 pages consigné n°39.** """

PLAN_E_SUITE = """ ; **LA SUITE (D179, l'ère 0.1.1) : LA VERSION COMMANDÉE AU TERRAIN — le kit loupe-kit-13/ (la pièce 0.1.1-dev.1 c1115105…, la dette [R10-PÉRIMÉE] soldée à la naissance, 0 octet de code changé), LE DOUZIÈME RUN attendu (le même critère : le scénario ENTIER T0 → S0 → LA LIAISON ET la vitrine vivante) ; le labo recoupe, complète la cristallisation 10/10, ADAPTE les portes du scellage au verdict du run — si le vert tient : LA BALISE `loupe 0.1.1` SCELLÉE (la version de la dette soldée)**"""

WORKLOG_128 = """
---
Task ID: 128
Agent: Z.ai (agent principal)
Task: « b et c » — LA VERSION 0.1.1 NÉE DE LA RECOMPOSITION (la dette
[R10-PÉRIMÉE] soldée à la naissance, D179) ET LA CONSOLIDATION v0.9.0
de la spécification (D180) — le douzième run attendu.

Work Log:
- (c) LE GESTE 0.1.1 : layout/carte_m10 portés à l'ère (0x00010101,
  GÉNÉRATION 17), _version_carte génération-indépendante (l'en-tête
  signé — le passage d'ère n'aveugle jamais l'anti-rollback),
  _anti_rollback ouvert à LA MONOTONIE R10, _porte_ere_011 (la
  déployée ASSERTÉE scellée 0.1.0, l'écart confiné aux champs nommés) ;
  LE BUILD VERT : garde 14/14, 18/18 round-trip, 43 verrous, 78 IAT,
  harnais 61/61 · 53/53 · 45/45 — LA DETTE SOLDÉE À LA NAISSANCE :
  17 sommes rafraîchies, le qword porté, 0 octet ailleurs ;
  loupe.exe 0.1.1-dev.1 NÉE (c1115105…, 127 488 o), la carte
  génération 17, le verrou croisé 26/26 ; une passe de cristallisation
  (la recomposition == la pièce, PLUS AUCUN écart — compteurs 2/10,
  les passes au scellage).
- LE KIT + LE COFFRE : kit-loupe.zip 38 585 o dadfb48c… (les QUATRE
  pièces, extraction vierge, py_compile) ; la vague versionnée
  vagues-m10/, la racine portée (kit-loupe.zip + LISEZMOI +
  loupe-kit-13/), le réceptacle ARMÉ (le douzième run), l'index à
  jour — 27 entrées, AUCUN doublon.
- (b) LA CONSOLIDATION v0.9.0 : le md révisé (§ 1.10, la rangée M10
  FRANCHIE, § 19.11 la correspondance + 4 rejets, le journal, la
  clôture) ; la chaîne spec_v090 née de spec_v084 (cover, sec-a/cf/d,
  l'annexe D177–D180) ; LE PDF 51 pages sha256 465331b2… consigné
  n°39 ; LE CAHIER TOUT PASSÉ ; le contrôle visuel par code (51
  pages, aucune quasi blanche) + les pages clés constatées.
- CONSIGNATIONS : D179, D180, l'Entrée 221, le PLAN (l'État + la
  rangée (e)), le présent worklog.
- SUITE : LE DOUZIÈME RUN (le kit loupe-kit-13/ au /test — python
  scenario-loupe.py puis temoin-vitrine.bat, preuves-loupe/ ENTIER au
  coffre) ; puis le scellage 0.1.1 au labo (le recoup, la
  cristallisation 10/10, les portes adaptées, la balise `loupe 0.1.1`
  sur le vert recoupé).
"""


def main() -> int:
    # 1. JOURNAL_TRAVAIL.md — l'Entrée 221 AVANT le marqueur m5a
    chemin = os.path.join(R, "docs", "JOURNAL_TRAVAIL.md")
    texte = open(chemin, encoding="utf-8").read()
    marqueur = "<!-- m5a:journal-des-builds v1"
    idx = texte.index(marqueur)
    if "## Entrée 221" in texte:
        print("[journal] l'Entrée 221 y vit déjà")
    else:
        texte = texte[:idx] + ENTREE_221 + "\n" + texte[idx:]
        open(chemin, "w", encoding="utf-8").write(texte)
        print("[journal] l'Entrée 221 consignée")

    # 2. PLAN_MILESTONES.md — l'État porté + la rangée (e) étendue ET RÉPARÉE
    #    (le script 219 avait dédoublé la cellule critère : 5 cellules au
    #    lieu de 3 — nommé et guéri au geste même)
    chemin = os.path.join(R, "docs", "PLAN_MILESTONES.md")
    texte = open(chemin, encoding="utf-8").read()
    if "LA VERSION 0.1.1-dev.1 COMMANDÉE" in texte:
        print("[plan] l'État porte déjà l'ère 0.1.1")
    else:
        ancien = "**État du programme.** **LE JALON M10 FRANCHI le 11/11/2026"
        assert texte.count(ancien) == 1, "l'ancre de l'État du programme"
        texte = texte.replace(
            ancien, "**État du programme.** " + PLAN_ETAT
            + "**LE JALON M10 FRANCHI le 11/11/2026")
        # la rangée (e) — le dédoublement réparé + la suite 0.1.1
        critere = ("le run VERT sur pièces + recoup N/N sur pièces croisées + la "
                   "0.1.0 SCELLÉE (fait de carte, l'artefact INTACT) + la clôture "
                   "D143 des pièces")
        dedouble = f"ONZE RUNS, ONZE LEÇONS** | {critere} | | {critere} |"
        assert texte.count(dedouble) == 1, "le dédoublement de la rangée (e)"
        texte = texte.replace(
            dedouble,
            f"ONZE RUNS, ONZE LEÇONS**{PLAN_E_SUITE} | {critere} |")
        open(chemin, "w", encoding="utf-8").write(texte)
        print("[plan] l'État porté à l'ère 0.1.1 + la rangée (e) étendue ET "
              "RÉPARÉE (la cellule critère dédoublée par le script 219, nommée "
              "et guérie — 3 cellules)")

    # 3. worklog.md — le Task ID 128 en fin
    chemin = os.path.join(R, "worklog.md")
    texte = open(chemin, encoding="utf-8").read()
    if "Task ID: 128" in texte:
        print("[worklog] le Task ID 128 y vit déjà")
    else:
        open(chemin, "a", encoding="utf-8").write(WORKLOG_128)
        print("[worklog] le Task ID 128 consigné")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
