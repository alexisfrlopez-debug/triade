#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_169.py — LA CONSIGNATION DU GESTE « LA SPÉCIFICATION v0.7.0 » :
JOURNAL_TRAVAIL +Entrée 169 (ordre 168<169<marqueur, rejeu REFUSÉ), worklog
+Task ID 87. Tout ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 169 — LA SPÉCIFICATION v0.7.0 : LA CONSOLIDATION DU PROGRAMME D'APRÈS M7 livrée sur la demande du développeur (« je voudrais que tu produises la dernière version complète du document pdf Protocole TRIADE ») — M8 franchi, M9 ouvert, le sceau à TREIZE arbres, les cérémonies d'ère au protocole, la clause « hors périmètre courant » levée nommément (05/11 au soir)

**La demande et son moment.** La demande du développeur arrive au geste qui suit la cérémonie de l'ère M9 installée (Entrée 168) : produire LA DERNIÈRE VERSION COMPLÈTE du document PDF Protocole TRIADE. Le constat du geste : la spécification vivante était EN RETARD SUR LE PROGRAMME sur quatre points nommés — le § 12.4 disait « Dix arbres » (le sceau en porte treize) ; le § 18 titrait « jalons M0 à M7 » (M7 est franchi, M8/M9 absents) ; la clôture du § 21 tenait syscalls directs et TLS 1.3 pur « hors périmètre courant » (D160/D166 les ont ouverts, M8 est FRANCHI) ; l'en-tête s'arrêtait à M6. Le versionnement suit les RÉVISIONS, jamais les franchissements — mais un programme entré en exécution EST une révision en attente de sa passation : la v0.7.0 est la passation du programme d'après M7 dans la spécification, le miroir de ce que D133 fit pour la souveraineté.

**La révision du maître markdown (PAR SCRIPT, remplacements ASSERTÉS).** scripts/revision_v070_md.py (miroir de revision_v061_md.py) : DIX-HUIT remplacements assertés — le titre et le bloc d'en-tête (l'archive v0.6.1 ajoutée à la liste, la phrase de consolidation), la puce Version (M0–M8 franchis, M9 ouvert, le sceau à TREIZE arbres), la date (5 novembre 2026), le § 1.2 porté à M0–M9, le NOUVEAU § 1.9 « Ce que change la v0.7.0 », l'axe 3 du § 12 (treize arbres + les cérémonies d'ère), le § 12.4 RÉÉCRIT (Treize arbres + la discipline des ères : dette à la naissance D166 r. 8, charge au geste D168, déterminisme Ed25519 D163), la table des cérémonies § 13.1 (treize arbres VERTS), le NOUVEAU § 13.5 « Les cérémonies d'ère du sceau de l'Intention (5 novembre 2026) », le § 18 (titre M0 à M9, Dix jalons, M7 franchi 0.8.0, les lignes M8 et M9, la clôture étendue), le NOUVEAU § 19.9 « Correspondance v0.6.1 → v0.7.0 » avec QUATRE rejets explicites, la ligne v0.7.0 au journal des versions, la clôture du § 21 RÉÉCRITE (la clause levée nommément).

**La chaîne formelle (spec_v061 → spec_v070 par RENOMMAGE git, le modèle des révisions précédentes).** main.tex (en-tête de chaîne, fancyhead, pdftitle — v0.7.0) ; sec-a.tex (+ le § 1.9) ; sec-cf.tex (l'axe 3, le § 12.4, la table des cérémonies, la NOUVELLE § 13.5) ; sec-c.tex (le paragraphe des domaines du programme d'après M7 sur le profil primaire) ; sec-d.tex (le titre et l'intro des jalons, M5/M6/M7 PORTÉS franchis, les lignes M8 et M9 au tableau, la clôture étendue, le paragraphe « Ouverture de M5 » archivé pour mémoire et REMPLACÉ par « Le programme d'après M7 (D160) », la NOUVELLE correspondance v0.6.1 → v0.7.0 avec ses rejets, la synthèse du journal des décisions étendue à D169, l'annexe décisionnelle ÉTENDUE de D160 à D169 — NEUF lignes nouvelles) ; cover.html (v0.7.0, la consolidation en sous-titre — RACCOURCI d'une phrase après REFUS du validateur : chevauchement de 8 px avec .authors, la leçon de la v0.6.1 rejouée, l'écart final vert) ; merge_cover.py (métadonnées v0.7.0) ; build_pdf.sh → spec_v070/v0.7.0 ; scripts/revision_v070_tex.py (les QUATORZE remplacements LaTeX assertés).

**Le build et ses preuves.** build_pdf.sh --force : couverture validée (poster_validate + cover_validate PASS après le raccourcissement), corps Tectonic, fusion, pdf_qa WARN (12 advisories : la classe des tirets cadratins en début de ligne, consignée depuis D133, non bloquants ; le « content overflow » page 30 est un faux positif des filets du tableau des jalons — AUCUN mot au-delà de la marge, constaté par extraction des positions) ; L'ARTEFACT : docs/Protocole_TRIADE_v0.7.0_Specification.pdf — 42 pages, 999 631 o, sha256 dd36eb41e361…, md5 99423a6b67d2e8f7b7a2514d633c3240, EMPOINTE CONSIGNÉE PAR LE BUILD (n°23 au TABLEAU_DE_BORD, stamp 8b811a55…) ; empreintes_build.py verifier : 13 PDF livrés, 23 consignations, 0 refus — VERT. LE CAHIER scripts/spec_v070/verify_spec.py (V1–V16, miroir du cahier v0.6.1) : TOUT PASSÉ — hiérarchie intacte, règles intactes, aucune couche d'exécution, l'héritage v0.5.0–v0.6.1 intact (D75/D81/D133/D137), le § 12.4 à TREIZE arbres avec la discipline des ères, le § 13.5 présentes (M8 douze arbres, M9 treize — la charge régénérée D168), les jalons M0–M9, la correspondance v0.6.1 → v0.7.0 au PDF, l'annexe étendue à D169, aucune référence non résolue, aucun placeholder, aucune ligne parasite. Contrôle visuel : 42 pages rendues, AUCUNE quasi blanche, la couverture porte « VERSION 0.7.0 · Consolidation », le § 1.9 page 6, le § 12.4 page 20, le § 13.5 page 25, le tableau des jalons page 30, l'annexe D169 page 42.

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 — la révision documente, elle ne scelle rien), AUCUNE règle modifiée, AUCUNE couche d'exécution ajoutée, la hiérarchie inchangée ; l'archive v0.6.1 DEMEURE (sha 4aac10f1… — rien ne se jette) ; le *Livre du Coffre* v1.1 INCHANGÉ ; AUCUN octet de notation (R2) ; le sceau I vérifié au geste : TREIZE arbres VERTS. Livrables : docs/PROTOCOLE_TRIADE.md (v0.7.0), docs/Protocole_TRIADE_v0.7.0_Specification.pdf (42 pages, empreinte n°23), scripts/spec_v070/ (la chaîne + le cahier), scripts/revision_v070_md.py + scripts/revision_v070_tex.py + scripts/inserer_d169.py ; consignations : la présente Entrée PAR SCRIPT, D169 PAR SCRIPT, worklog +Task ID 87.

- SUITE : LA PASSATION D141 (le bundle de la série 090 au miroir + le push GitHub + la synchro du coffre Drive) ; puis LES CHANTIERS M9 — (b) la notation des 28 blocs aux adresses préfigurées + les vecteurs officiels, (e) le build 1.0.0-dev.1 (le garde est vert, construire() peut naître), (f) le terrain — la session réelle.

"""

TASK = """

## Task ID 87 — LA SPÉCIFICATION v0.7.0 LIVRÉE : la consolidation du programme d'après M7 (la demande du développeur : la dernière version complète du document PDF) (05/11 au soir)

- LA DEMANDE : « je voudrais que tu produises la dernière version complète du
  document pdf Protocole TRIADE » — au geste qui suit la cérémonie de l'ère
  installée ; le constat : la spécification était en retard sur le programme
  (dix arbres vs treize, M7 franchi non constaté, M8/M9 absents, la clause
  « hors périmètre courant » périmée).
- LA RÉVISION : revision_v070_md.py — 18 remplacements ASSERTÉS (titre,
  en-tête, § 1.9 NOUVEAU, § 12.4 treize arbres + discipline des ères,
  § 13.1, § 13.5 NOUVEAU, § 18 M0-M9 + lignes M8/M9, § 19.9 NOUVEAU +
  rejets, journal des versions, clôture réécrite).
- LA CHAÎNE : spec_v061 → spec_v070 (git mv) ; main/sec-a/sec-c/sec-cf/sec-d
  édités (14 remplacements assertés) ; la couverture v0.7.0 RACCOURCIE après
  REFUS du validateur (8 px de chevauchement — la leçon v0.6.1 rejouée) ;
  l'annexe décisionnelle étendue D160–D169.
- LES PREUVES : le PDF 42 pages, 999 631 o, sha256 dd36eb41…, empreinte
  CONSIGNÉE PAR LE BUILD (n°23, stamp 8b811a55…) ; empreintes verifier VERT
  (23 consignations, 0 refus) ; LE CAHIER V1–V16 TOUT PASSÉ ; 42 pages
  rendues, aucune quasi blanche ; le sceau I vérifié au geste (13 verts).
- FRONTIÈRES : aucune balise, aucune règle modifiée, aucune couche
  d'exécution, hiérarchie inchangée ; l'archive v0.6.1 demeure ; le Livre
  v1.1 inchangé ; consignations : Entrée 169 PAR SCRIPT, D169 PAR SCRIPT,
  worklog +Task ID 87.
- SUITE : LA PASSATION D141 (bundle 090 + GitHub + Drive) ; les chantiers
  M9 (b)/(e)/(f).

Stage Summary:
- LA DERNIÈRE VERSION COMPLÈTE EST LIVRÉE : la v0.7.0 consolide le
  programme d'après M7 — M8 franchi, M9 ouvert, le sceau à treize arbres,
  les cérémonies d'ère au protocole.
- LA DEMANDE DU DÉVELOPPEUR EST SERVIE SUR LES DEUX TABLES : le document
  PDF formel (42 pages, empreinte consignée) et la source maîtresse
  markdown — la série documentaire continue.
"""


def inserer():
    j = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 169 —" in j:
        print("[inserer-169] REJEU REFUSÉ : l'Entrée 169 existe déjà.")
        return 1
    n = j.count(MARQUEUR)
    if n != 1:
        print(f"[inserer-169] ÉCHEC : marqueur {n} fois dans le journal.")
        return 1
    if "## Entrée 168 —" not in j:
        print("[inserer-169] ÉCHEC : l'Entrée 168 est absente (ordre 168<169).")
        return 1
    j = j.replace(MARQUEUR, ENTREE + MARQUEUR)
    JOURNAL.write_text(j, encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 87 —" in w:
        print("[inserer-169] REJEU REFUSÉ : le Task ID 87 existe déjà.")
        return 1
    w = w.rstrip("\n") + "\n" + TASK
    WORKLOG.write_text(w, encoding="utf-8")
    print("[inserer-169] PASSÉ : Entrée 169 insérée avant le marqueur ; worklog +Task ID 87.")
    return 0


if __name__ == "__main__":
    sys.exit(inserer())
