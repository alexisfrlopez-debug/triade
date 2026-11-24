#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GÉNÉRATION DES PIÈCES 4 ET 5 DE L'ÉDITION v0.27.0 (atelier W20LINT).

- 4-preuves-calculs/TRIADE_preuves_et_calculs_<EDITION>.pdf : les rapports des quatre
  ateliers de la vague 17 LUS VERBATIM de leurs fichiers, le registre de provenance,
  la table des empreintes des quatre autres pièces (aucun document ne porte son propre
  sha256), les limites nommées.
- 5-presentation/TRIADE_presentation_<EDITION>.pdf : la présentation de la vague 17.

Aucune valeur n'est retapée : les textes viennent des rapports ; les empreintes sont
recalculées des fichiers mêmes au moment de la génération.
"""
import hashlib
import pathlib
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, PageBreak, Table, TableStyle)

REPO = pathlib.Path(__file__).resolve().parents[2]
import os
PACK = pathlib.Path(os.environ.get("TRIADE_PACK", str(REPO / "pack-v270")))
EDITION = os.environ.get("TRIADE_EDITION", "v0.27.0")
SPECVER = os.environ.get("TRIADE_SPECVER", "v0.15.12")
BOOKVER = os.environ.get("TRIADE_BOOKVER", "v1.11")
FDIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("Serif", FDIR + "/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("SerifB", FDIR + "/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", FDIR + "/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("SansB", FDIR + "/DejaVuSans-Bold.ttf"))

H1 = ParagraphStyle("H1", fontName="SerifB", fontSize=17, leading=21, spaceAfter=8)
H2 = ParagraphStyle("H2", fontName="SansB", fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("Body", fontName="Serif", fontSize=9.4, leading=13.2, alignment=TA_LEFT,
                      spaceAfter=5)
MONO = ParagraphStyle("Mono", fontName="Serif", fontSize=7.6, leading=10.2, spaceAfter=3)
PETIT = ParagraphStyle("Petit", fontName="Sans", fontSize=8.2, leading=11)


def sha(p):
    d = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            d.update(b)
    return d.hexdigest()


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def extrait(chemin, maxlignes=95):
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    txt = "\n".join(lignes[:maxlignes])
    if len(lignes) > maxlignes:
        txt += "\n[... la suite au rapport du dépôt, lue verbatim sans coupure]"
    return esc(txt)


def page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Sans", 7.5)
    canvas.setFillColor(colors.HexColor("#555F66"))
    canvas.drawString(20 * mm, 12 * mm, f"TRIADE — édition {EDITION} (la vague 20, 24 novembre 2026)")
    canvas.drawRightString(190 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def construire(chemin, titre, sous_titre, histoire):
    doc = BaseDocTemplate(str(chemin), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=18 * mm, bottomMargin=18 * mm,
                          title=titre, author="Alexis Lopez")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=page)])
    doc.build(histoire)


def preuves():
    p1 = PACK / "1-manuscrit" / f"TRIADE_manuscrit_{EDITION}.pdf"
    p2 = PACK / "2-specification" / f"Protocole_TRIADE_{SPECVER}_Specification.pdf"
    p3 = PACK / "3-coffre-fort" / f"Livre_du_Coffre_TRIADE_CF1-CF3_{BOOKVER}.pdf"
    pieces = [(f"Le manuscrit académique {EDITION}", p1), (f"La spécification {SPECVER}", p2),
              (f"Le Livre du Coffre {BOOKVER}", p3)]
    ateliers = [
        ("W22AUDT — cible relative, contextes d'exécution, C17, péremption (D272)",
         REPO / "atelier-w22-audit.rapport.txt"),
        ("W21IMPR — les quatre améliorations issues de la vague 20 (D271)",
         REPO / "atelier-w21-impr.rapport.txt"),
        ("W20LINT — le linter v4 à quinze classes, les quatre résidus soldés",
         REPO / "atelier-w20-lint.rapport.txt"),
        ("W20ORAC — les vecteurs d'oracle des 50 blocs dérivés de la couche I",
         REPO / "atelier-w20-orac.rapport.txt"),
        ("W20ADD — la campagne add structurée, pré-enregistrée",
         REPO / "atelier-w20-add.rapport.txt"),
        ("W20PERF — les couloirs de performance, pré-enregistrés",
         REPO / "atelier-w20-perf.rapport.txt"),
        ("W20SEC — l'ancrage de transparence, les preuves symboliques, le durcissement",
         REPO / "atelier-w20-sec.rapport.txt"),
    ]
    h = [Paragraph("TRIADE — Preuves et calculs", H1),
         Paragraph(f"Édition {EDITION} — la vague 20 (24 novembre 2026)", H2),
         Paragraph("Ce document rassemble les pièces de la vague 19 <b>lues verbatim de leurs "
                   "rapports</b> : aucun résultat n'y est retapé. Les empreintes de la table "
                   "sont recalculées des fichiers au moment de la génération ; ce document ne "
                   "porte pas son propre sha256 (la convention du pack). Les pièces du "
                   "document sont numérotées <b>1. à 5.</b> ; tout renvoi à la spécification "
                   "porte son numéro de section propre, précédé de « spec » (§ spec 7.6, "
                   "§ spec 7.7, § spec 7.8, § spec 7.9, § spec 7.10, § spec 7.11) — une seule "
                   "convention, jamais un numéro de section employé pour un autre document.", BODY),
         Paragraph("1. Les pièces de l'édition", H2)]
    rows = [["Pièce", "octets", "sha256"]]
    for nom, p in pieces:
        rows.append([nom, str(p.stat().st_size), sha(p)])
    t = Table(rows, colWidths=[62 * mm, 20 * mm, 88 * mm])
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Serif", 7.2),
        ("FONT", (0, 0), (-1, 0), "SansB", 7.6),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#B8C2C8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    h.append(t)
    h.append(Paragraph(f"2. Ce que porte l'édition {EDITION}", H2))
    h.append(Paragraph(
        "Le linter d'édition passe à <b>seize classes</b> (la seizième, C16, recompose le "
        "registre unique des statuts) : VERSION-PROSE (toute "
        "mention « édition courante vX » ou « révision vX » dans les cinq pièces confrontée "
        "au manifeste — le trou de couverture qui laissait le Livre annoncer v0.15.10 et la "
        "révision v1.9), WAVE-CONTINUITY (toute « vague N » renvoie à une entrée datée du "
        "changelog), ABSTRACT-LENGTH (résumé ≤ 250 mots), READER-TEST-COUNT (le compte se "
        "recompose depuis ses cas énumérés). Les quatre résidus de l'évaluation sont soldés "
        "à la source : les versions de prose du Livre, la référence de vague de la "
        "présentation (vague 15, les campagnes linguistiques ; la vague 16 est la vague "
        "corpus et kit, sans édition donc sans entrée au changelog), le −35,7 % annoté de "
        "ses opérandes entiers (611/1 714 = 35,653 %) et épinglé au registre de provenance, "
        "et le test du lecteur décomposé ; la vague 21 ajoute l'audit oracle tiré par le "
        "contenu, le résumé anglais à 235 mots, le registre des statuts et le ré-ancrage "
        "RFC 3161 automatique (D271). <b>Aucune valeur mesurée n'est modifiée ; aucun "
        "artefact scellé n'est touché.</b>", BODY))
    h.append(PageBreak())
    for titre, p in ateliers:
        h.append(Paragraph(titre, H2))
        h.append(Paragraph(f"<font size=7 color='#555F66'>source : {p.relative_to(REPO)}</font>", PETIT))
        h.append(Paragraph(extrait(p).replace("\n", "<br/>"), MONO))
        h.append(Spacer(1, 4 * mm))
    h.append(Paragraph("3. Le registre de provenance (12 lignes, recomposées)", H2))
    h.append(Paragraph("Chaque grandeur est recomposée depuis sa source canonique committée "
                       "(chemin + sha256) ; deux conventions de médiane sont nommées ; les quatre "
                       "grandeurs (a)-(d) ne sont jamais additionnées. Registre complet : "
                       "replication-v17/provenance-v17.json ; contrôles : 12/12 VERT, 4/4 refus "
                       "mutants.", BODY))
    h.append(Paragraph("4. Notes de lecture rétablies (résidus d'édition soldés)", H2))
    h.append(Paragraph(
        "Sept états de la transaction de bascule (0 à 6 : préparé, armé, rendez-vous, publication, "
        "invalidation, vérification, reprise), plus le rollback depuis publication, invalidation ou "
        "vérification. Ventilation des quatre bras aux opérandes NON ARRONDIS : 20,715 + 16,497 + "
        "0,213 = 37,425 s (le résidu de 13 ms des macros arrondies est nommé, jamais lissé). Mutants : "
        "776/832 = 93,3 % est l'ÈRE v0.14.0 ; l'ère v0.19.5 porte 811/832 = 97,5 %. GHASH : 49,12× "
        "(78 888 / 1 606) est le ratio PAR APPEL, distinct du ratio par multiplication (19,66 / 63,39). "
        "Médiane du mode éditer : 712,5 — le 712 publié est sa troncature, nommée comme telle. "
        "Banc de bascule : 16/16 = 7 cas de transaction + 1 rendez-vous nominal + 5 aléas D261 + "
        "3 invariants (recompté depuis les cas du kit, écart zéro). "
        "Test du lecteur : <b>9/9</b>, une ligne par cas — "
        "(1) 3,22 = 63,39/19,66 (manuscrit) ; (2) 12,7 = 806,35/63,39 (présentation) ; "
        "(3) 41,0 = 806,35/19,66 (présentation) ; (4) 1,055 = 4,844/4,59 (spécification) ; "
        "(5) 49,12 = 78 888/1 606 (preuves) ; (6) 37,425 = 20,715+16,497+0,213 (preuves) ; "
        "(7) 712,5 médiane de l'éditeur (preuves) ; (8) 811/832 = 97,5 % (manuscrit et preuves) ; "
        "(9) 16/16 = 7+1+5+3 (présentation).", BODY))
    h.append(Paragraph("5. Les limites nommées", H2))
    h.append(Paragraph("Aucune mesure au métal nu ; la bascule concurrente réelle, le compteur NV "
                       "matériel et la campagne structurée restent EN ATTENTE ; la sentinelle "
                       "Windows (SACL/4663) et IMA/Authenticode configurés restent au poste réel ; "
                       "les outils Tamarin/ProVerif sont absents du bac, les lemmes gardent leur "
                       "statut « prouvés sous hypothèses » ; l'ancrage de transparence est adopté, "
                       "outillé et NON DÉPLOYÉ (D267). La porte de génération couvre seize classes ; "
                       "elle ne rejoue pas les 1 991 tokens de l'ancienne extraction — l'extraction "
                       "est remplacée par les classes et le test du lecteur, et le rapport le dit.", BODY))
    construire(PACK / "4-preuves-calculs" / f"TRIADE_preuves_et_calculs_{EDITION}.pdf",
               f"TRIADE — Preuves et calculs {EDITION}", EDITION, h)


def presentation():
    p1 = PACK / "1-manuscrit" / f"TRIADE_manuscrit_{EDITION}.pdf"
    p2 = PACK / "2-specification" / f"Protocole_TRIADE_{SPECVER}_Specification.pdf"
    p3 = PACK / "3-coffre-fort" / f"Livre_du_Coffre_TRIADE_CF1-CF3_{BOOKVER}.pdf"
    p4 = PACK / "4-preuves-calculs" / f"TRIADE_preuves_et_calculs_{EDITION}.pdf"
    T = ParagraphStyle("T", fontName="SansB", fontSize=24, leading=30, textColor=colors.HexColor("#1F4E5F"))
    S = ParagraphStyle("S", fontName="Sans", fontSize=12, leading=17, textColor=colors.HexColor("#555F66"))
    Pu = ParagraphStyle("Pu", fontName="Sans", fontSize=12, leading=19, leftIndent=10, bulletIndent=0,
                        spaceAfter=7)
    h = [Spacer(1, 55 * mm),
         Paragraph(f"TRIADE — édition {EDITION}", T),
         Paragraph("La vague 19 : la porte qui porte le linter, les décisions au journal, "
                   "les bornes nommées", S),
         Spacer(1, 8 * mm),
         Paragraph("Alexis Lopez · 24 novembre 2026", S), PageBreak()]

    def slide(titre, points):
        h.append(Paragraph(titre, H2))
        for b in points:
            h.append(Paragraph(b, Pu, bulletText="•"))
        h.append(Spacer(1, 6 * mm))

    slide("1. La promesse corrigée (D253)", [
        "La spécification annonçait un trampoline de 12 à 16 octets « atomique par écriture alignée unique ».",
        "Faux : un magasin naturel est atomique jusqu'à 8 octets ; 16 octets n'existent que par LOCK CMPXCHG16B.",
        "Quatre propriétés séparées : alignement, atomicité, cohérence des instructions, état des threads.",
        "Un thread dont RIP tombe dans la plage remplacée n'est protégé par AUCUNE atomicité de magasin.",
        "Conséquence : la quiescence devient obligatoire — la publication est conditionnée au rendez-vous.",
    ])
    h.append(PageBreak())
    slide("2. La transaction et ses refus", [
        "Sept états (0 à 6) : préparé → armé → rendez-vous → publication → invalidation → vérification → reprise.",
        "Rollback depuis publication/invalidation/vérification ; aucun état partiel n'est exécutable.",
        "Refus nommés : mot non aligné, 12 octets au magasin simple, 16 octets sans CPUID, magasin SSE, RIP dans la plage.",
        "Banc : 16/16 = 7 cas de transaction + 1 rendez-vous nominal + 5 aléas D261 + 3 invariants ; métal : EN ATTENTE (≥ 2 machines).",
    ])
    slide("3. La racine de confiance (D254)", [
        "R10 est local et hors ligne : checksums, signature du manifeste, version ≥ plancher, conformité.",
        "La garantie vaut ce que vaut l'ANCRE : Authenticode, IMA/signature de paquet, chaîne de boot signée.",
        "Trois propriétés distinctes : intégrité, authenticité, fraîcheur.",
        "Si l'ancre est modifiable avec l'artefact, R10 détecte la corruption — pas l'administrateur local.",
    ])
    h.append(PageBreak())
    slide("4. Ce que R10 ne garantit pas", [
        "La restauration cohérente d'un couple binaire + état échappe à toute ancre locale.",
        "Seuls les témoins hors machine du coffre la voient : carte papier, journal Git poussé, ancre de transparence.",
        "Le plancher R10 protège l'artefact ; l'époque CF3 protège la clé ; les témoins protègent l'état — trois choses.",
        "D267 : l'ancrage de transparence est adopté, outillé, NON DÉPLOYÉ — la porte le dit EN ATTENTE.",
        "Banc : 11/11 contrôles dont 9 refus nommés et 2 invariants rendus ; l'exploitation reste au poste réel.",
    ])
    slide("5. La provenance (D255)", [
        "Douze lignes recomposées depuis leurs JSONL/JSON committés, chacune avec chemin + sha256.",
        "Deux conventions de médiane nommées (18 tâches vs tâches vertes) ; v3 séparé en deux modes (jamais 24/36).",
        "Trois classes au linter : ratios recomposés depuis les opérandes, comptes relus, statuts fermés.",
        "Contrôles : 12/12 VERT, 4/4 mutations refusées (valeur, ratio, compte, statut).",
    ])
    h.append(PageBreak())
    slide("6. Le rouge trouvé sur pièces", [
        "Le manuscrit v0.23.3 imprimait « 3.23× (63.39/19.66) » : 3,2243 s'arrondit à 3,22.",
        "Corrigé à la SOURCE de l'édition ; le PDF scellé v0.23.3 demeure (append-only).",
        "Les deux autres ratios recomposent : 806,35/63,39 = 12,7× ; 806,35/19,66 = 41,0×.",
    ])
    slide("7. La réplication publique", [
        "replication-v17/ : commandes reproductibles, sorties attendues, procédure d'audit tiers.",
        "Exclus : couche I signée, carte C, secrets, données personnelles.",
        "Le paquet ne prouve aucune mesure matérielle — et le dit.",
    ])
    h.append(PageBreak())
    slide("8. Corpus et entraînement", [
        "Corpus v2.1 : 127/24/19 triples, 48 paires DPO, splits par groupe-de-contrat, TEST sans dorée.",
        "Pack d'entraînement : recettes SFT/DPO/RLVR agnostiques en famille, récompense = verdict du juge.",
        "Aucune nouvelle mesure LLM dans cette édition : les campagnes de la vague 15 restent la référence.",
    ])
    slide("9. Ce qui reste au poste réel", [
        "Bascule concurrente au métal nu (kit pré-enregistré, agrégateur fail-closed), sentinelle Windows SACL/4663, IMA/Authenticode configurés.",
        "Compteur NV matériel (D263) et campagne structurée (D264) : simulateur et instrument verts, runs EN ATTENTE.",
        "Tamarin/ProVerif/Maude : outils absents, aucun verdict fabriqué.",
        "Vecteurs d'oracle : 235 exécutables, 95 exécutés au contexte standard (IAT bouchonnée, "
        "deux ABI), 27 blocs sans exécution — recomposé depuis les fichiers (C17).",
        "Le registre unique des chantiers en attente porte 10 entrées (STATUTS-EN-ATTENTE.md) ; "
        "la porte recompose ce compte (C16) et refuse tout écart.",
    ])
    h.append(PageBreak())
    h.append(Paragraph(f"10. L'édition {EDITION}", H2))
    rows = [["Pièce", "Version"], ["Manuscrit", EDITION], ["Spécification", SPECVER],
            ["Livre du Coffre", BOOKVER], ["Preuves et calculs", EDITION],
            ["Présentation", EDITION]]
    t = Table(rows, colWidths=[90 * mm, 40 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Serif", 9),
                           ("FONT", (0, 0), (-1, 0), "SansB", 9),
                           ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#B8C2C8"))]))
    h.append(t)
    h.append(Spacer(1, 5 * mm))
    h.append(Paragraph("Empreintes sha256 des quatre autres pièces (le manifeste du pack porte "
                       "les cinq) :", BODY))
    for nom, p in (("manuscrit", p1), ("spécification", p2), ("Livre", p3), ("preuves", p4)):
        h.append(Paragraph(f"{nom} : {sha(p)}", ParagraphStyle("FP", fontName="Serif", fontSize=7, leading=10)))
    construire(PACK / "5-presentation" / f"TRIADE_presentation_{EDITION.replace('.','')}.pdf",
               f"TRIADE — présentation {EDITION}", EDITION, h)


def reancrer():
    """Le témoin d'époque est PÉRISSABLE : on le ré-ancre après chaque génération (D271)."""
    import subprocess
    r = subprocess.run([sys.executable, str(REPO / "scripts/vague20/ancrage_transparence.py")],
                       capture_output=True, text=True)
    print((r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr) else "[ancrage] ?")
    return r.returncode == 0


if __name__ == "__main__":
    preuves()
    presentation()
    print("pièces 4 et 5 générées")
    reancrer()
