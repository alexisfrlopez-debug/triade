#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GÉNÉRATION DES PIÈCES 4 ET 5 DE L'ÉDITION v0.24.0 (atelier W17R5REL).

- 4-preuves-calculs/TRIADE_preuves_et_calculs_v0.24.0.pdf : les rapports des quatre
  ateliers de la vague 17 LUS VERBATIM de leurs fichiers, le registre de provenance,
  la table des empreintes des quatre autres pièces (aucun document ne porte son propre
  sha256), les limites nommées.
- 5-presentation/TRIADE_presentation_v240.pdf : la présentation de la vague 17.

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
PACK = REPO / "pack-v240"
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
    canvas.drawString(20 * mm, 12 * mm, "TRIADE — édition v0.24.0 (la vague 17, 24 novembre 2026)")
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
    p1 = PACK / "1-manuscrit" / "TRIADE_manuscrit_v0.24.0.pdf"
    p2 = PACK / "2-specification" / "Protocole_TRIADE_v0.15.9_Specification.pdf"
    p3 = PACK / "3-coffre-fort" / "Livre_du_Coffre_TRIADE_CF1-CF3_v1.8.pdf"
    pieces = [("Le manuscrit académique v0.24.0", p1), ("La spécification v0.15.9", p2),
              ("Le Livre du Coffre v1.8", p3)]
    ateliers = [
        ("W17R1D81 — la remise D81 historique, la garde active D223",
         REPO / "atelier-w17-d81-d223" / "rapport-purge-actives.txt"),
        ("W17R2PAT — la publication d'une bascule est atomique jusqu'à 8 octets",
         REPO / "atelier-w17-patch-a-chaud" / "rapport.txt"),
        ("W17R3R10 — la racine de confiance, l'ancre et ses limites",
         REPO / "atelier-w17-r10-confiance" / "rapport.txt"),
        ("W17R4PER — la provenance des tableaux et la réplication",
         REPO / "atelier-w17-performance-replication" / "rapport.txt"),
    ]
    h = [Paragraph("TRIADE — Preuves et calculs", H1),
         Paragraph("Édition v0.24.0 — la vague 17 (24 novembre 2026)", H2),
         Paragraph("Ce document rassemble les pièces de la vague 17 <b>lues verbatim de leurs "
                   "rapports</b> : aucun résultat n'y est retapé. Les empreintes de la table "
                   "sont recalculées des fichiers au moment de la génération ; ce document ne "
                   "porte pas son propre sha256 (la convention du pack).", BODY),
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
    h.append(Paragraph("2. Ce que porte l'édition v0.24.0", H2))
    h.append(Paragraph("La spécification gagne §7.1.1 (ce que garantit réellement la primitive "
                       "de publication, D253) et §8.6 (la racine de confiance, l'ancre par profil "
                       "et ses limites, D254). Le manuscrit corrige le seul ratio qui ne se "
                       "recomposait pas depuis ses opérandes imprimés (63,39/19,66 = 3,2243, "
                       "imprimé 3,23 ; corrigé à 3,22 — D255) et porte la note de la vague 17. Le "
                       "Livre du Coffre aligne sa plage de décisions sur sa table (D75–D137) et "
                       "ajoute les trois propriétés de fraîcheur (D254). <b>Aucune valeur mesurée "
                       "n'est modifiée.</b>", BODY))
    h.append(PageBreak())
    for titre, p in ateliers:
        h.append(Paragraph(titre, H2))
        h.append(Paragraph(f"<font size=7 color='#555F66'>source : {p.relative_to(REPO)}</font>", PETIT))
        h.append(Paragraph(extrait(p).replace("\n", "<br/>"), MONO))
        h.append(Spacer(1, 4 * mm))
    h.append(Paragraph("3. Le registre de provenance (11 lignes, recomposées)", H2))
    h.append(Paragraph("Chaque grandeur est recomposée depuis sa source canonique committée "
                       "(chemin + sha256) ; deux conventions de médiane sont nommées ; les quatre "
                       "grandeurs (a)-(d) ne sont jamais additionnées. Registre complet : "
                       "replication-v17/provenance-v17.json ; contrôles : 11/11 VERT, 4/4 refus "
                       "mutants.", BODY))
    h.append(Paragraph("4. Les limites nommées", H2))
    h.append(Paragraph("Aucune mesure au métal nu ; la bascule concurrente réelle et la sentinelle "
                       "Windows (SACL/4663) restent EN ATTENTE ; les outils Tamarin/ProVerif sont "
                       "absents du bac, les lemmes gardent leur statut « prouvés sous hypothèses » ; "
                       "le linter d'édition v2 n'a pas été porté à cette génération — la porte de "
                       "génération v0.24.0 couvre les versions, les empreintes et les recompositions, "
                       "pas les 1 991 tokens du linter v2 (défaut nommé).", BODY))
    construire(PACK / "4-preuves-calculs" / "TRIADE_preuves_et_calculs_v0.24.0.pdf",
               "TRIADE — Preuves et calculs v0.24.0", "v0.24.0", h)


def presentation():
    p1 = PACK / "1-manuscrit" / "TRIADE_manuscrit_v0.24.0.pdf"
    p2 = PACK / "2-specification" / "Protocole_TRIADE_v0.15.9_Specification.pdf"
    p3 = PACK / "3-coffre-fort" / "Livre_du_Coffre_TRIADE_CF1-CF3_v1.8.pdf"
    p4 = PACK / "4-preuves-calculs" / "TRIADE_preuves_et_calculs_v0.24.0.pdf"
    T = ParagraphStyle("T", fontName="SansB", fontSize=24, leading=30, textColor=colors.HexColor("#1F4E5F"))
    S = ParagraphStyle("S", fontName="Sans", fontSize=12, leading=17, textColor=colors.HexColor("#555F66"))
    Pu = ParagraphStyle("Pu", fontName="Sans", fontSize=12, leading=19, leftIndent=10, bulletIndent=0,
                        spaceAfter=7)
    h = [Spacer(1, 55 * mm),
         Paragraph("TRIADE — édition v0.24.0", T),
         Paragraph("La vague 17 : la promesse réduite à ce qui est garanti, l'ancre nommée, "
                   "la provenance contrôlée", S),
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
        "Six états : préparé → armé → rendez-vous → publication → invalidation → vérification → reprise.",
        "Rollback depuis publication/invalidation/vérification ; aucun état partiel n'est exécutable.",
        "Refus nommés : mot non aligné, 12 octets au magasin simple, 16 octets sans CPUID, magasin SSE, RIP dans la plage.",
        "Banc : 10/10 ; métal : EN ATTENTE (≥ 2 machines) — l'émulation ne prouve pas le cache d'instructions.",
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
        "Rotation/révocation : identifiant de clé, plancher d'époque, clé absente = refus nommé, jamais de récupération.",
        "Banc : 11/11 refus nommés rendus ; l'exploitation reste au poste réel.",
    ])
    slide("5. La provenance (D255)", [
        "Onze lignes recomposées depuis leurs JSONL/JSON committés, chacune avec chemin + sha256.",
        "Deux conventions de médiane nommées (18 tâches vs tâches vertes) ; v3 séparé en deux modes (jamais 24/36).",
        "Trois classes au linter : ratios recomposés depuis les opérandes, comptes relus, statuts fermés.",
        "Contrôles : 11/11 VERT, 4/4 mutations refusées (valeur, ratio, compte, statut).",
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
        "Aucune nouvelle mesure LLM dans cette édition : les campagnes de la vague 16 restent la référence.",
    ])
    slide("9. Ce qui reste au poste réel", [
        "Bascule concurrente au métal nu, sentinelle Windows SACL/4663, IMA/Authenticode configurés.",
        "Tamarin/ProVerif/Maude : outils absents, aucun verdict fabriqué.",
        "Le linter d'édition v2 n'est pas porté à cette génération — défaut nommé.",
    ])
    h.append(PageBreak())
    h.append(Paragraph("10. L'édition v0.24.0", H2))
    rows = [["Pièce", "Version"], ["Manuscrit", "v0.24.0"], ["Spécification", "v0.15.9"],
            ["Livre du Coffre", "v1.8"], ["Preuves et calculs", "v0.24.0"],
            ["Présentation", "v0.24.0"]]
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
    construire(PACK / "5-presentation" / "TRIADE_presentation_v240.pdf",
               "TRIADE — présentation v0.24.0", "v0.24.0", h)


if __name__ == "__main__":
    preuves()
    presentation()
    print("pièces 4 et 5 générées")
