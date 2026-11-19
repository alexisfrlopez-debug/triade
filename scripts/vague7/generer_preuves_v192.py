#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère le corps du document TRIADE_preuves_et_calculs_v0.19.2.pdf (ReportLab).

Structure héritée de la v0.19.1 (le pack de présentation, pièce 4) avec les
apports de l'édition v0.19.2 — LA TRANSITION D81 → D183 PRÉPARÉE (D219,
l'instruction jx4l5vy5c) : le rapport de vérification de l'exécution (le kit
rafraîchi, la falsification prouvée, le scan de secrets au dry-run vert, le
tritage du vrai dépôt, les pièces scellées intactes), le diff annoté de
l'édition. Les pièces verbatim de la campagne, du modèle formel et des
mesures sont lues du dépôt (scripts/vague5/preuves/) — inchangées.
"""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

REPO = "/home/z/my-project/bac"
OUT = os.path.join(REPO, "scripts", "vague7", "preuves_v192_body.pdf")

# ---------- polices ----------
FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", f"{FDIR}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", f"{FDIR}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Italic", f"{FDIR}/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans", f"{FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", f"{FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", f"{FDIR}/LiberationMono-Regular.ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold",
                              italic="Serif-Italic", boldItalic="Serif-Bold")

ACCENT = colors.HexColor("#4A90C4")
DARK = colors.HexColor("#162032")
MUTED = colors.HexColor("#5A6B7F")

# ---------- styles ----------
st_body = ParagraphStyle("body", fontName="Serif", fontSize=9.6, leading=14.2,
                         alignment=TA_LEFT, spaceAfter=7, textColor=colors.HexColor("#1a1a1a"))
st_kicker = ParagraphStyle("kicker", parent=st_body, fontName="Sans-Bold", fontSize=8.2,
                           textColor=ACCENT, spaceBefore=6, spaceAfter=3,
                           leading=11, tracking=1)
st_h1 = ParagraphStyle("h1", fontName="Serif-Bold", fontSize=16.5, leading=21,
                       textColor=DARK, spaceBefore=2, spaceAfter=9)
st_h2 = ParagraphStyle("h2", fontName="Sans-Bold", fontSize=10.6, leading=14,
                       textColor=DARK, spaceBefore=10, spaceAfter=5)
st_mono = ParagraphStyle("mono", fontName="Mono", fontSize=7.0, leading=9.4,
                         textColor=colors.HexColor("#222222"))
st_verbatim_title = ParagraphStyle("vt", fontName="Mono", fontSize=8.4, leading=11.6,
                                   textColor=colors.white)
st_note = ParagraphStyle("note", parent=st_body, fontName="Serif-Italic",
                         fontSize=8.6, leading=12.4, textColor=MUTED)


def P(text, style=st_body):
    return Paragraph(text, style)


def verbatim_block(path, source_line, title=None, max_chars=None, chunk=46):
    """Encadré verbatim : titre sur bandeau bleu nuit + texte mono sur fond pâle.
    Le texte est découpé en morceaux de `chunk` lignes — chacun son tableau,
    la page peut tourner entre les morceaux (le filet accentué continue)."""
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    if max_chars:
        raw = raw[:max_chars]
    from xml.sax.saxutils import escape
    lines = raw.splitlines()
    head = (title or os.path.basename(path))
    head_esc = escape(head)

    def bloc(rows, first, last):
        cells = []
        if first:
            cells.append([Paragraph(head_esc, st_verbatim_title)])
        cells.append([Paragraph("<br/>".join(escape(l) if l.strip() else " " for l in rows) or " ", st_mono)])
        t = Table(cells, colWidths=[16.6 * cm])
        style = [
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F5F9")),
            ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#C8D2DE")),
            ("LINEBEFORE", (0, 0), (0, -1), 2.2, ACCENT),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]
        if first:
            style += [("BACKGROUND", (0, 0), (0, 0), DARK),
                      ("TOPPADDING", (0, 0), (-1, 0), 5), ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
                      ("TOPPADDING", (0, 1), (-1, 1), 7)]
        t.setStyle(TableStyle(style))
        return t

    out = []
    for i in range(0, len(lines), chunk):
        out.append(bloc(lines[i:i + chunk], i == 0, i + chunk >= len(lines)))
    out += [Spacer(1, 4), P(source_line, st_note), Spacer(1, 10)]
    return out


def stat_row(items):
    """Trois cartes de chiffres clés."""
    cells, widths = [], []
    for label, value in items:
        inner = Table(
            [[Paragraph(f'<font name="Serif-Bold" size="15" color="#162032">{value}</font>',
                        ParagraphStyle("v", fontName="Serif-Bold", fontSize=15, leading=18,
                                       alignment=1, textColor=DARK))],
             [Paragraph(f'<font name="Sans" size="7.2" color="#5A6B7F">{label}</font>',
                        ParagraphStyle("l", fontName="Sans", fontSize=7.2, leading=9.6,
                                       alignment=1, textColor=MUTED))]],
            colWidths=[5.35 * cm])
        inner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F5F9")),
            ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#C8D2DE")),
            ("LINEABOVE", (0, 0), (-1, 0), 2.0, ACCENT),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
            ("TOPPADDING", (0, 1), (-1, 1), 1),
            ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
        ]))
        cells.append(inner)
        widths.append(5.35 * cm)
    row = Table([cells], colWidths=widths)
    row.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return row


# ---------- gabarit de page ----------
class DocPreuves(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=A4, leftMargin=2.35 * cm, rightMargin=2.35 * cm,
                         topMargin=2.5 * cm, bottomMargin=2.2 * cm,
                         title="TRIADE — Preuves et calculs du protocole (édition v0.19.2)",
                         author="Z.ai", subject="Dossier d'évidence du protocole TRIADE — la transition D81 → D183 préparée",
                         creator="TRIADE — laboratoire (ReportLab, D219)", **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="corps")
        self.addPageTemplates([PageTemplate(id="page", frames=[frame], onPage=self.habille)])

    def habille(self, canv, doc):
        canv.saveState()
        canv.setStrokeColor(ACCENT)
        canv.setLineWidth(0.8)
        canv.line(doc.leftMargin, A4[1] - 1.55 * cm, A4[0] - doc.rightMargin, A4[1] - 1.55 * cm)
        canv.setFont("Sans", 7.4)
        canv.setFillColor(MUTED)
        canv.drawString(doc.leftMargin, A4[1] - 1.32 * cm,
                        "TRIADE — Preuves et calculs · édition v0.19.2")
        canv.setStrokeColor(colors.HexColor("#C8D2DE"))
        canv.setLineWidth(0.5)
        canv.line(doc.leftMargin, 1.52 * cm, A4[0] - doc.rightMargin, 1.52 * cm)
        canv.setFont("Sans", 7.4)
        canv.drawString(doc.leftMargin, 1.14 * cm,
                        "Projet TRIADE — le laboratoire · pack de présentation, pièce 4")
        canv.drawRightString(A4[0] - doc.rightMargin, 1.14 * cm, str(canv.getPageNumber()))
        canv.restoreState()


story = []

from xml.sax.saxutils import escape  # les blocs verbatim inline ci-dessous

# ============ 1. la chaîne d'épreuve ============
story.append(P("COMMENT TRIADE ÉTABLIT SES AFFIRMATIONS", st_kicker))
story.append(P("1. La chaîne d'épreuve du protocole", st_h1))
story.append(P(
    "Le protocole TRIADE ne déclare rien qu'il ne mesure ou ne prouve sur pièces. Chaque affirmation chiffrée du "
    "manuscrit est dérivée des sources brutes — les registres de campagne, les journaux d'usage, les sorties "
    "d'oracle — puis confrontée par un linter numérique qui refuse le build en cas d'écart : l'édition v0.19.2 "
    "porte les assertions chiffrées du registre v181 aux valeurs inchangées, le linter inter-pièces né à la "
    "v0.19.1 (D218) — les valeurs partagées (tailles d'artefacts, ratios, versions, nombre d'arbres signés, "
    "statut des outils formels, visibilité du dépôt) confrontées aux CINQ pièces du pack à chaque build — "
    "ÉTENDU à la présente édition aux STATUTS D81/D183 (la transition préparée exigée aux pièces, la "
    "visibilité PRIVÉ, la falsification du statut attrapée). Le présent document rassemble les pièces qui "
    "portent ces preuves : le rapport de vérification de l'exécution D219, la table complète de la campagne "
    "D204 et la clôture D210, l'alignement du modèle formel du coffre, les mesures de coût et de temps, "
    "l'égalité exacte des traces d'instructions, la table des empreintes et le diff annoté de l'édition."))
story.append(P(
    "La chaîne d'épreuve repose sur des mécanismes définis par la spécification (v0.15.2) : l'oracle éphémère — "
    "implémentation de référence triviale dérivée de la couche Intention, jamais du binaire, confrontée au bloc "
    "par bloc par tests différentiels par propriétés (environ douze mille cas par bloc critique) ; le round-trip "
    "de notation — chaque bloc assemblé est désassemblé et comparé exactement à sa notation d'origine ; le verrou "
    "croisé — empreintes et signature de la carte vérifiées avant chaque édition ; le modèle formel CF3 du "
    "coffre-fort, transcrit en TLA+ et vérifié par model-checking (TLC) et preuve déchargée (Apalache) ; et la "
    "réconciliation de campagne, rejouée à chaque édition depuis les registres bruts déposés par le terrain. Les "
    "contrôles négatifs systématisent la falsification : toute mutation d'une valeur consignée est attrapée, tout "
    "motif interdit est refusé à la réapparition."))
story.append(P(
    "Deux règles d'honnêteté gouvernent la formulation des résultats, et ce document y obéit : les observations "
    "défavorables sont consignées telles quelles (décision D189), et aucune propriété n'est déclarée prouvée "
    "au-delà de ce que les runs signés établissent — le manuscrit ne dit jamais « constant time proven » au-delà "
    "des traces effectivement vérifiées. La présente édition y ajoute sa propre frontière, tenue avant tout "
    "geste : le coffre réel et les phrases réelles ne sont JAMAIS approchés par le laboratoire (D105) — le kit "
    "de séquestre est prouvé sur des phrases de test publiques marquées, le scan ne lit jamais le contenu d'un "
    "fichier-jeton, et les pièces scellées sont re-hachées avant et après l'exécution."))
story.append(Spacer(1, 6))

# ============ 2. le rapport de vérification de l'exécution D219 ============
story.append(P("DIX POINTS, CHACUN SUR PIÈCES", st_kicker))
story.append(P("2. Le rapport de vérification de l'exécution D219 (l'édition v0.19.2)", st_h1))
story.append(P(
    "L'édition v0.19.2 est née de l'exécution de l'instruction jx4l5vy5c (la vague 7, la deuxième — la session "
    "détaillée par le RAPPORT-ANALYSES-VAGUE7) : la bascule de garde durable D81 vers le séquestre chiffré D183 "
    "PRÉPARÉE, sans jamais toucher au coffre réel ni aux phrases réelles. Le rapport de vérification ci-dessous "
    "atteste chacun des dix points de contrôle V1 à V10 de l'exécution : la première exigence tenue avant tout "
    "(les pièces scellées intactes), le kit rafraîchi, la falsification prouvée, le dry-run du scan, le triage "
    "du vrai dépôt, les livrables documentaires, les sources au statut exact, les diffs consignés, le linter "
    "étendu et le pack refusé si un seul contrôle est rouge."))
story.append(Spacer(1, 2))

with open(os.path.join(REPO, "scripts/vague7/rapport_verification_v0.19.2.txt"),
          encoding="utf-8") as f:
    RAPPORT_PATH = os.path.join(REPO, "scripts/vague7/rapport_verification_v0.19.2.txt")

story += verbatim_block(RAPPORT_PATH,
                        "Source : rapport_verification_v0.19.2.txt — la racine du coffre. Verbatim.",
                        title="L'ÉTAPE DE VÉRIFICATION DE L'ÉDITION v0.19.2 (LA TRANSITION PRÉPARÉE)")

# ============ 2bis. le kit D183 : l'autotest et la falsification ============
story.append(PageBreak())
story.append(P("LA PART FORGÉE EST REFUSÉE — LA PREUVE À FROID", st_kicker))
story.append(P("2 bis. Le kit de séquestre D183 : l'autotest rafraîchi et la falsification", st_h1))
story.append(P(
    "L'outil de la cérémonie est le partage CF2 D120 TEL QUEL (v06/coffre_cf2.py — l'instrument existant, "
    "jamais une réécriture, la doctrine D185) ; le kit l'enveloppe de la preuve à froid et, à la présente "
    "édition (D219), d'une porte fail-closed : le mode --verifier confronte le sha256 du rendu de "
    "reconstitution à l'empreinte de contrôle du manifeste — ÉGALITÉ exigée, tout écart un REFUS nommé. "
    "L'autotest rafraîchi du 19 novembre 2026, exécuté au dépôt sur une phrase de test PUBLIQUE marquée :"))
story += verbatim_block(os.path.join(REPO, "scripts/kit_ceremonie_d183/AUTOTEST.txt"),
                        "Source : scripts/kit_ceremonie_d183/AUTOTEST.txt — l'exécution du 19/11/2026. Verbatim.")
story.append(P(
    "La preuve vécue du mode --verifier (la cérémonie de TEST sur phrase publique marquée, 51 octets — les "
    "consoles de l'épreuve) : l'honnête rend VERT (le sha256 du rendu == l'empreinte de contrôle du "
    "manifeste), la part forgée (un octet muté) rend REFUS — le rejet nommé, fail-closed :"))
VERIF = """[D183] VERT — 3 parts, 51 octets : le sha256 du rendu == l'empreinte de
contrôle du manifeste
[D183] la phrase n'est pas affichée — la preuve est l'égalité des empreintes
                    (code de sortie 0 — la combinaison honnête)

[D183] REFUS — le sha256 du rendu ≠ l'empreinte de contrôle : une part est
fausse, forgée ou corrompue (le rejet est nommé, fail-closed ; essayez une
autre combinaison de TROIS parts recoupées au manifeste)
                    (code de sortie 1 — la part forgée REFUSÉE)"""
lines = VERIF.splitlines()
data = [[Paragraph("LA PREUVE VÉCUE DU MODE --verifier (les consoles de l'épreuve)", st_verbatim_title)],
        [Paragraph("<br/>".join(escape(l) if l.strip() else " " for l in lines), st_mono)]]
t = Table(data, colWidths=[16.6 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, 0), DARK),
    ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#F2F5F9")),
    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#C8D2DE")),
    ("LINEBEFORE", (0, 0), (0, -1), 2.2, ACCENT),
    ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, 0), 5), ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
    ("TOPPADDING", (0, 1), (-1, 1), 7), ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
]))
story += [t, Spacer(1, 10)]

# ============ 2ter. le scan de secrets : le dry-run et le triage ============
story.append(PageBreak())
story.append(P("SIX SECRETS PLANTÉS, SIX ATTRAPÉS — L'HISTORIQUE Y DEMEURE", st_kicker))
story.append(P("2 ter. Le scan de secrets : le dry-run et le triage du vrai dépôt", st_h1))
story.append(P(
    "L'instruction prescrivait gitleaks ou trufflehog ; TOUS DEUX ABSENTS du bac (l'écart d'outillage nommé "
    "à D207), l'équivalent Python NOMMÉ est livré : scan_secrets.py — jamais une simulation, chaque blob de "
    "l'historique git est réellement lu (un seul flux git cat-file --batch), confronté à six règles nommées, "
    "le contenu d'un secret n'est JAMAIS affiché (l'aperçu est masqué), et les fichiers-jetons ne sont JAMAIS "
    "lus (la présence EST le constat — D105). Le dry-run sur le dépôt de test à secrets plantés (déterministe, "
    "six secrets factices dont deux SUPPRIMÉS de la tête, trois fichiers propres) et le triage du vrai dépôt :"))
with open(os.path.join(REPO, "scripts/kit_ceremonie_d183/epreuves-d219/console-dryrun-scan.txt"),
          encoding="utf-8") as f:
    DRYRUN = f.read().rstrip()
lines = DRYRUN.splitlines()
data = [[Paragraph("LE DRY-RUN — LE DÉPÔT DE TEST À SECRETS PLANTÉS (console consignée)", st_verbatim_title)],
        [Paragraph("<br/>".join(escape(l) if l.strip() else " " for l in lines), st_mono)]]
t = Table(data, colWidths=[16.6 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, 0), DARK),
    ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#F2F5F9")),
    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#C8D2DE")),
    ("LINEBEFORE", (0, 0), (0, -1), 2.2, ACCENT),
    ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, 0), 5), ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
    ("TOPPADDING", (0, 1), (-1, 1), 7), ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
]))
story += [t, Spacer(1, 10)]
story.append(P(
    "LE TRIAGE DU VRAI DÉPÔT (l'historique complet : 472 commits, 5 847 blobs) : DIX constats — la phrase de "
    "contrôle (LA SITUATION CONNUE D81, le sujet même de la transition), les cinq clés de l'autorité de test "
    "locale M5 (D136 — nées fixtures, le constat demeurant au rapport), les quatre jetons de fixture de "
    "l'oracle terrain (les ya29. factices 254 octets de D70 — la TÊTE EST PROPRE, la fixture courante tronquée "
    "par concaténation, l'arbre terrain signé jamais touché) ; ET L'ABSENCE QUI FAIT FOI : aucun jeton git, "
    "aucun fichier OAuth du relais, aucun secret de client Google, aucune assignation secrète réelle dans "
    "5 847 blobs — la discipline des jetons (D12/D27) a tenu sur toute l'histoire. Le rapport complet vit au "
    "kit (PROCEDURE-SCAN-SECRETS.txt) ; la matrice de visibilité qui s'ensuit : PRIVÉ tant que la cérémonie "
    "D183 n'est pas vécue et la rotation vérifiée — public + Zenodo seulement après."))

# ============ 3. la campagne ============
story.append(NextPageTemplate("page"))
story.append(PageBreak())
story.append(P("LES DEUX BRAS, VINGT-DEUX LIVRAISONS, LA CLÔTURE D210", st_kicker))
story.append(P("3. La campagne D204 : la table complète, la réconciliation et la clôture D210", st_h1))
story.append(P(
    "La campagne D204 a confronté les deux bras du protocole sur des unités identiques : le bras T (TRIADE — la "
    "notation écrite à la main, sans compilateur) et le bras C (la référence compilée). Chaque run appartient au "
    "terrain et se termine par un témoin daté et signé de la main du développeur (décision D99) ; le laboratoire "
    "reçoit, recoupe octet par octet et consigne. L'extension D210 (le plan pré-enregistré, la graine consignée "
    "avant toute mesure) a clos le livre : quatre unités à formats identiques et ordre tiré, la quatrième close "
    "au rouge à la cap de livraison — trois échappées comptées, toutes kit-side au juge partagé, la pièce jamais "
    "en faute aux deux formats ; l'attribution tranchée sur pièces : la même pièce C re-livrée au kit standard "
    "minimal a lu 14 VERT, 0 ROUGE. La mesure M3 (le carnet de temps humain) est posée : cinq lignes run-terrain, "
    "l'écart des bornes consigné à côté (D189). Le livre est clos : 29 lignes de campagne, onze défauts nommés, "
    "aucune ouverture ne demeure."))
story.append(Spacer(1, 4))
story.append(stat_row([("livraisons D204 reçues et recoupées", "22"),
                       ("unités à la table de campagne", "14"),
                       ("défauts nommés sur pièces (D204)", "8")]))
story.append(Spacer(1, 8))
story += verbatim_block(os.path.join(REPO, "scripts/vague5/preuves/p3-table-campagne.txt"),
                        "Source : scripts/vague5/preuves/p3-table-campagne.txt (l'instruction bwxv9xzfa, la vague 5). Verbatim, lignes longues repliées.")
story.append(P(
    "LA CLÔTURE D210 — LES QUATRE UNITÉS DE L'EXTENSION (la table générée des registres reçus, la réconciliation "
    "de la vague 7) : chaque ligne est générée du registre brut, la colonne It. telle que déposée. La quatrième "
    "unité (loupe-16) close sur son rouge à la cap de livraison : trois échappées comptées, toutes les trois "
    "kit-side au juge partagé (le guichet-descripteur-quatre-champs, la liaison-memmove-deux-arguments, "
    "les-metriques-ecran-jamais-posees-par-le-juge) ; l'attribution tranchée sur pièces : la même pièce C "
    "re-livrée à travers le kit standard minimal a lu 14 VERT, 0 ROUGE — le format standard blanchi SUR PIÈCES, "
    "les échappées portées à la rig. Les fermetures H6–H8 portées au manuscrit : H6 tenue par attribution, H7 "
    "non testée sur ce tirage (le contraste vide, l'hypothèse reportée), H8 réfutée (51/39/9 % — la spirale "
    "corrective déclinante)."))
d210_rows = [
    ["livraison", "bras", "unité", "it.", "verdict", "échappée nommée", "attribution"],
    ["T-loupe-02-d210-it1", "T", "loupe-02", "1", "VERT", "—", "—"],
    ["T-loupe-08-d210-it1", "T", "loupe-08", "1", "VERT", "—", "—"],
    ["T-loupe-13-d210-it1", "T", "loupe-13", "1", "VERT", "—", "—"],
    ["T-loupe-16-d210-it1", "T", "loupe-16", "1", "ROUGE", "guichet-descripteur-quatre-champs", "kit (juge)"],
    ["T-loupe-16-d210-it2", "T", "loupe-16", "1", "ROUGE", "liaison-memmove-deux-arguments", "kit (juge)"],
    ["T-loupe-16-d210-it3", "T", "loupe-16", "3", "ROUGE", "les-metriques-ecran-jamais-posees-par-le-juge", "kit (juge)"],
    ["C-loupe-16-attr-it1", "C", "loupe-16", "1", "VERT", "—", "—"],
]
tbl = Table([[Paragraph(f"<b>{c}</b>" if i == 0 else c,
                        ParagraphStyle("c", fontName="Mono", fontSize=6.7, leading=8.8,
                                       textColor=colors.white if i == 0 else colors.HexColor("#222222")))
              for c in row] for i, row in enumerate(d210_rows)],
            colWidths=[3.5 * cm, 0.9 * cm, 1.7 * cm, 0.7 * cm, 1.4 * cm, 5.6 * cm, 2.5 * cm], repeatRows=1)
tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), DARK),
    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F2F5F9")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C8D2DE")),
    ("LINEBEFORE", (0, 0), (0, -1), 2.0, ACCENT),
    ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
]))
story += [tbl, Spacer(1, 4),
          P("Source : la table générée par reconciliation_campagne_d210.py des registres reçus (reception-357) — "
            "livraisons.csv à 29 lignes, defauts.csv à onze défauts, le carnet à cinq lignes run-terrain. "
            "Chaque ligne telle que déposée.", st_note), Spacer(1, 10)]

# ============ 4. le modèle formel ============
story.append(PageBreak())
story.append(P("TREIZE RÈGLES, 288 FORMES", st_kicker))
story.append(P("4. Le modèle formel du coffre : alignement et couverture", st_h1))
story.append(P(
    "Le coffre-fort du protocole — la garde de l'état de développement, ses trois niveaux CF1, CF2 et CF3 — est "
    "spécifié par un modèle TLA+ (CF3.tla) et par une sémantique opérationnelle Python (modele_invariant_v150.py). "
    "Deux preuves cadrent leur équivalence. D'abord l'alignement règle par règle : les treize règles du modèle "
    "sont confrontées état par état sur l'espace concret borné — chaque règle Python contre sa garde TLA+, chaque "
    "activation et chaque image comparées. Ensuite le lemme de couverture (l'obligation O3) : les 288 formes de "
    "la preuve couvrent exactement l'espace des états atteignables, avec les obligations O1 et O2 déchargées par "
    "Apalache et un contrôle négatif qui attrape la violation."))
story += verbatim_block(os.path.join(REPO, "scripts/vague5/preuves/p6-alignement-13-regles.txt"),
                        "Source : scripts/vague5/preuves/p6-alignement-13-regles.txt. Verbatim.")
story += verbatim_block(os.path.join(REPO, "scripts/vague5/preuves/p6-couverture-288.txt"),
                        "Source : scripts/vague5/preuves/p6-couverture-288.txt (l'instruction oc2y014vx). Verbatim.")

# ============ 5. les mesures ============
story.append(PageBreak())
story.append(P("CHAQUE NOMBRE DÉRIVÉ, JAMAIS TAPÉ", st_kicker))
story.append(P("5. Les mesures : périmètre RQ2, temps de vérification, tokens", st_h1))
story.append(P(
    "Trois familles de mesures portent les résultats quantitatifs du manuscrit. La question RQ2 (le coût en "
    "tokens de la localisation et de l'édition) se lit à périmètre constant : <b>l'écart de l'ère Loupe contre la "
    "baseline M1</b> tient à la plage exacte 2,98–11,37× (580/51, 2 143/719 et 3 510/1 088 selon l'opération — "
    "le contenu de l'ère Loupe contre les valeurs M1, PAS un écart entre les bras T et C), et l'évolution entre "
    "la v0.14.0 et la v0.17.0 s'explique par le périmètre instrumenté — le contenu seul contre l'appel complet "
    "au tokenizer natif — jamais par une différence de tokenizer. Le temps de vérification (M4) est consigné au "
    "journal d'optimisation sous la règle R11 : la mesure avant vaut 50,9 s sur la liste fixe originale, 3,0 % "
    "sous les 52,5 s consignés de la campagne, et la série d'après porte n = 2 (39,3 / 39,2 s) — deux mesures "
    "n = 1 jamais moyennées ; <b>le ratio canonique consigné est 23,1× → 17,9×</b> (39,3/2,2, la première "
    "exécution de la liste optimisée) — la pièce R11 verbatim calcule 17,8× sur la seconde exécution (39,2/2,2) : "
    "l'écart est nommé à côté, la pièce demeurant verbatim. Enfin, la décomposition des tokens de l'unité "
    "instrumentée est lue du journal d'usage : vingt appels, rien tapé à la main."))
story.append(Spacer(1, 4))
story.append(stat_row([("la plage RQ2, l'ère Loupe contre M1, l'opération par opération", "2,98–11,37×"),
                       ("M4 : le canon consigné (39,3/2,2)", "23,1× → 17,9×"),
                       ("la part corrective des tokens, bras T / bras C", "61,4 % / 58,1 %")]))
story.append(Spacer(1, 10))
story += verbatim_block(os.path.join(REPO, "scripts/vague5/preuves/p5-decomposition-contexte.txt"),
                        "Source : scripts/vague5/preuves/p5-decomposition-contexte.txt (l'instruction om3ewy9lf). Verbatim.")
story.append(P("Le rapport R11 — l'optimisation du temps de vérification (la pièce VERBATIM, l'écart d'arrondi nommé) :"))
story += verbatim_block(os.path.join(REPO, "scripts/vague5/preuves/p8-m4-rapport-r11.txt"),
                        "Source : scripts/vague5/preuves/p8-m4-rapport-r11.txt (l'instruction mof9q10vq). Verbatim, lignes "
                        "longues repliées. NOTE DE L'ÉDITION v0.19.1 (D218, correction 7) : le canon consigné est "
                        "17,9× (39,3/2,2, la première exécution de la liste optimisée) ; la pièce calcule 17,8× sur "
                        "la seconde exécution (39,2/2,2) — l'écart d'arrondi nommé à côté, la pièce demeurant verbatim.")
story.append(P("La décomposition des tokens de l'unité instrumentée (la table restructurée, la correction 8 de D218) :"))

TOKENS = """LA DÉCOMPOSITION DES TOKENS DE L'UNITÉ INSTRUMENTÉE (loupe-01, les
DEUX bras — lue du journal d'usage, 20 appels, rien tapé à la main)
(la vague 5, l'instruction 2l40ie6qn, point 3 — LA TABLE RESTRUCTURÉE à
l'édition v0.19.1 : les itérations correctives sont L'APPEL CORRECTIF
ENTIER, prompts ET complétions, jamais un sous-ensemble de la seule
écriture ; la pièce source demeure verbatim au dépôt)
================================================================================
====
catégorie                          bras T      bras C   part T   part C
--------------------------------------------------------------------------------
spécification (contrat lu/écrit)    5 313       5 605   10.0%     8.3%
oracle (dérivé du contrat)          3 752       4 423    7.1%     6.6%
notation (écrite à la main)        11 480           0   21.6%     0.0%
source C (écrit)                        0      14 660    0.0%    21.7%
suite de tests C                        0       3 563    0.0%     5.3%
ITÉRATIONS CORRECTIVES             32 613      39 224   61.4%    58.1%
   (l'appel correctif ENTIER :         6           7
    prompt + complétion)
--------------------------------------------------------------------------------
LA COUPE PROMPTS / COMPLÉTIONS (tous appels confondus — une coupe
ORTHOGONALE aux catégories : chaque appel, correctif ou premier passage,
lit son contexte puis écrit) :
LECTURE DE CONTEXTE (prompts)      34 920      42 122   65.7%    62.4%
ÉCRITURE (complétions)             18 238      25 353   34.3%    37.6%
--------------------------------------------------------------------------------
TOTAL                              53 158      67 475

LA LECTURE CORRIGÉE (D218, correction 8) : les ITÉRATIONS CORRECTIVES ne
sont PAS un sous-ensemble de la seule écriture — 32 613 tokens correctifs
au bras T ne peuvent pas vivre dans les 18 238 de l'écriture : l'appel
correctif est ENTIER (son prompt lu + sa complétion écrite). Le CHEMIN
CHAUD demeure le même aux deux bras — la spirale corrective (61,4 % de T,
58,1 % de C) ; la spécification et l'oracle coûtent PLUS au bras C
(5 605/4 423 contre 5 313/3 752 : le contrat lu deux fois, l'oracle
réécrit pour la suite standard) ; la notation T (11 480) contre le source
C (14 660) : le C est PLUS LONG À ÉCRIRE que la notation — la première
contre-intuition de H3.
LE RAISONNEMENT : le GAP NOMMÉ — l'API compte le raisonnement DANS la
complétion (jamais séparé au log) ; l'estimation ×1,08 est INTERDITE là
où un log existe (la règle M2 du plan D204) : la catégorie
« raisonnement » n'est PAS reconstruite.
Source : scripts/vague5/preuves/p9-decomposition-tokens.txt (l'instruction 2l40ie6qn,
point 3). La table restructurée à l'édition v0.19.1 (D218, correction 8) ; la pièce
source verbatim au dépôt."""
lines = TOKENS.splitlines()
data = [[Paragraph("LA DÉCOMPOSITION DES TOKENS — LA TABLE RESTRUCTURÉE", st_verbatim_title)],
        [Paragraph("<br/>".join(escape(l) if l.strip() else " " for l in lines), st_mono)]]
t = Table(data, colWidths=[16.6 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, 0), DARK),
    ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#F2F5F9")),
    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#C8D2DE")),
    ("LINEBEFORE", (0, 0), (0, -1), 2.2, ACCENT),
    ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, 0), 5), ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
    ("TOPPADDING", (0, 1), (-1, 1), 7), ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
]))
story += [t, Spacer(1, 10)]

# ============ 6. égalité des traces + empreintes ============
story.append(PageBreak())
story.append(P("L'OCTET EST LA VÉRITÉ", st_kicker))
story.append(P("6. L'égalité des traces et la table des empreintes", st_h1))
story.append(P(
    "Les six cibles cryptographiques et de traitement (les familles tls13 et la loupe de contenu md5) ont été "
    "rejouées à classes fixées et secret fixe, N = 60 par classe, graine consignée : les traces d'instructions "
    "sont bit-identiques entre les classes — c'est l'égalité exacte des comptes, la formulation correcte qui "
    "remplace l'affirmation erronée « toutes les traces de longueur nulle ». La table des empreintes confronte "
    "ensuite chaque artefact livré, octet par octet, à l'empreinte attendue — y compris le GAP nommé du pilote "
    "d'installation, consigné comme tel plutôt que masqué. Les tailles passeur portées à cette table "
    "(61 952 / 102 390 o) sont la mesure re-faite sur les octets réels des archives — la réconciliation D218 ; "
    "à la présente édition, les deux pièces sont re-téléchargées et re-hachées INTACTES (la preuve V1 du "
    "rapport)."))
story += verbatim_block(os.path.join(REPO, "scripts/vague5/preuves/p7-egalite-traces.txt"),
                        "Source : scripts/vague5/preuves/p7-egalite-traces.txt (l'instruction gfylb610p). Verbatim.")
story += verbatim_block(os.path.join(REPO, "scripts/vague5/preuves/p10-table5-octets.txt"),
                        "Source : scripts/vague5/preuves/p10-table5-octets.txt (l'instruction iz5b9sv09). Verbatim, lignes "
                        "longues repliées. NOTE : les tailles passeur (61 952 / 102 390 o) re-hachées aux archives — D218 ; "
                        "re-téléchargées intactes à la présente édition (D219, la preuve V1).")

# ============ 7. le diff annoté ============
story.append(PageBreak())
story.append(P("TROIS SOURCES, CHAQUE CHANGEMENT NOMMÉ", st_kicker))
story.append(P("7. L'édition v0.19.2 : le diff annoté", st_h1))
story.append(P(
    "L'édition v0.19.2 porte la ligne D81 du modèle de menace à SON STATUT EXACT aux trois pièces qui la portent "
    "— la spécification v0.15.2, le manuscrit §4.1, le runbook du Livre v1.3 — sans toucher une seule valeur "
    "mesurée, une seule règle de la spécification ou un seul geste de cérémonie du Livre. Le diff annoté "
    "ci-dessous nomme, pour chaque changement, l'écart constaté, la source qui le fonde et la correction "
    "rendue. Les diffs machine (diff-spec-v151-v152.patch, diff-livre-v12-v13.patch, "
    "diff-main-v191-v192.patch) accompagnent l'édition au dépôt ; la décision D219 (append-only) fait foi pour "
    "la chronologie."))
story += verbatim_block(os.path.join(REPO, "scripts/vague7/diff-annote-v192.txt"),
                        "Source : scripts/vague7/diff-annote-v192.txt — chaque changement sourcé. Verbatim.")

# ============ 8. empreintes du pack ============
story.append(PageBreak())
story.append(P("SHA256 — RECOUPABLES AU DÉPÔT ET AU COFFRE", st_kicker))
story.append(P("8. Empreintes des pièces du pack", st_h1))
story.append(P(
    "Les pièces scellées du pack portent les empreintes consignées au tableau de bord des builds du dépôt (chaque "
    "build y laisse son sha256, toute divergence est un refus nommé). Les valeurs ci-dessous sont recalculées à "
    "l'assemblage du pack, le 20 novembre 2026, à partir des fichiers reproduits dans ce pack ; le fichier "
    "empreintes_livrables_v0.19.2.txt, au sommet du pack, porte la liste complète — y compris les empreintes du "
    "pack lui-même et du présent document."))
story.append(Spacer(1, 2))
story.append(P("<i>La table des empreintes des pièces du pack est gravée à l'assemblage du zip "
               "(empreintes_livrables_v0.19.2.txt) — les cinq pièces à leurs nouvelles versions, chaque "
               "empreinte recalculée au geste.</i>", st_note))
story.append(Spacer(1, 8))
story.append(P(
    "Ce document accompagne le manuscrit v0.19.2 : il ne remplace ni la spécification normative (v0.15.2), ni le "
    "Livre du Coffre (v1.3), ni les registres bruts au dépôt — il les met en main. Chaque affirmation du "
    "manuscrit reste traçable jusqu'aux pièces reproduites ici, et jusqu'aux sources brutes dont elles "
    "dérivent ; c'est la discipline que la spécification appelle l'évidence, et que le journal de travail "
    "consigne entrée par entrée."))

doc = DocPreuves(OUT)
doc.build(story)
print(f"OK — corps généré : {OUT}")
