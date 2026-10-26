#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corps du PDF — Protocole TRIADE v0.3, démonstration RoomEq (étude de cas).

Étude de démonstration du protocole TRIADE v0.3 : le recodage complet de
l'application RoomEq (v2.2.2 -> v3.0.0-dev.1) sert de validation à
échelle réelle, avec comparatifs de code avant/après. Route Report
(ReportLab), TOC auto, fusion couverture. Même fonte, palette et géométrie
que la spécification v0.3 (continuité de la série documentaire).

Sources faisant autorité :
  - triade/docs/PROTOCOLE_TRIADE.md, FORMAT_CARTE.md, DECISIONS.md (v0.3)
  - roomeq/CARTE.md, docs/PARITE-v2.2.2.md, docs/DECISIONS.md (D1-D11),
    docs/PLAN_RECODAGE.md, WORKLOG.md
  - code source : roomeq-git-ref/ (@ deff25c = v2.2.2) et roomeq/ (v3)

Le script vit dans le dépôt (triade/scripts/) ; tous les chemins dérivent
de TRIADE_BASE (défaut /home/z/my-project). Contrairement au PDF formel de
la spécification (régénéré par build_pdf.sh, décision D17), ce document est
une ÉDITION : sa régénération est manuelle —

  python3 skills/pdf/scripts/poster_validate.py check-html \\
      triade/scripts/triade_v03_demo_cover.html
  node skills/pdf/scripts/cover_validate.js triade/scripts/triade_v03_demo_cover.html
  node skills/pdf/scripts/html2poster.js triade/scripts/triade_v03_demo_cover.html \\
      --output triade/scripts/triade_v03_demo_cover.pdf --width 794px
  python3 triade/scripts/triade_v03_demo_roomeq.py
"""

import os
import sys
import hashlib

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, Image, KeepTogether,
                                CondPageBreak, Flowable, HRFlowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from PIL import Image as PILImage

# ---------------------------------------------------------------- chemins
BASE = os.environ.get("TRIADE_BASE", "/home/z/my-project")
REPO = os.path.join(BASE, "triade")            # dépôt = source de vérité
ASSETS = os.path.join(REPO, "scripts", "assets")
BODY_PDF = os.path.join(REPO, "scripts", "triade_v03_demo_body.pdf")
COVER_PDF = os.path.join(REPO, "scripts", "triade_v03_demo_cover.pdf")
FINAL_PDF = os.path.join(REPO, "docs", "Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf")
DOWNLOAD_DIR = os.path.join(BASE, "download")  # copie livrable si présent

SKILL_SCRIPTS = os.path.join(BASE, "skills", "pdf", "scripts")
if os.path.isdir(SKILL_SCRIPTS):
    sys.path.insert(0, SKILL_SCRIPTS)
    try:
        from pdf import install_font_fallback  # noqa: E402
    except ImportError:
        install_font_fallback = None
else:
    install_font_fallback = None

# ---------------------------------------------------------------- fontes
FONT_DIR = "/usr/share/fonts"
pdfmetrics.registerFont(TTFont("FreeSerif", f"{FONT_DIR}/truetype/freefont/FreeSerif.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-Bold", f"{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-Italic", f"{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-BoldItalic", f"{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans", f"{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", f"{FONT_DIR}/truetype/dejavu/DejaVuSansMono-Bold.ttf"))
pdfmetrics.registerFont(TTFont("NotoSerifSC", f"{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NotoSerifSC-Bold", f"{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf"))

registerFontFamily("FreeSerif", normal="FreeSerif", bold="FreeSerif-Bold",
                   italic="FreeSerif-Italic", boldItalic="FreeSerif-BoldItalic")
registerFontFamily("DejaVuSans", normal="DejaVuSans", bold="DejaVuSans-Bold")
registerFontFamily("NotoSerifSC", normal="NotoSerifSC", bold="NotoSerifSC-Bold")

if install_font_fallback is not None:
    install_font_fallback()

# ---------------------------------------------------------------- palette
# Cascade palette (design_engine.py palette-cascade --intent cold --mode minimal
# --seed 7) — IDENTIQUE à la spécification v0.2/v0.3 : continuité visuelle de
# la série documentaire TRIADE.
PAGE_BG      = colors.HexColor("#eff0f1")   # XL
SECTION_BG   = colors.HexColor("#f0f1f2")   # XL
CARD_BG      = colors.HexColor("#e4e7e8")   # L
TABLE_STRIPE = colors.HexColor("#ebedee")   # L
HEADER_FILL  = colors.HexColor("#334650")   # M
COVER_BLOCK  = colors.HexColor("#5a7886")   # M
BORDER       = colors.HexColor("#b8c8cf")   # S
ICON         = colors.HexColor("#52798c")   # S
ACCENT       = colors.HexColor("#3681a6")   # XS
ACCENT_2     = colors.HexColor("#b43a4e")   # XS
TEXT_PRIMARY = colors.HexColor("#1a1b1c")
TEXT_MUTED   = colors.HexColor("#6f7578")
SEM_ERROR    = colors.HexColor("#92453e")

TABLE_HEADER_COLOR = HEADER_FILL
TABLE_ROW_EVEN = colors.white
TABLE_ROW_ODD = TABLE_STRIPE

# ---------------------------------------------------------------- geometrie
PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm                     # gauche = droite (symetrie)
TOP_MARGIN = 2.4 * cm
BOTTOM_MARGIN = 2.2 * cm
AVAIL_W = PAGE_W - 2 * MARGIN
AVAIL_H = PAGE_H - TOP_MARGIN - BOTTOM_MARGIN
H1_ORPHAN = AVAIL_H * 0.25

DOC_TITLE = ("Protocole TRIADE v0.3 — Démonstration RoomEq : "
             "le recodage complet d'une application réelle sous protocole")
DOC_SUBJECT = ("Étude de démonstration du protocole TRIADE v0.3 : recodage complet de "
               "RoomEq v3 (42 modules, 437 tests, parité v2.2.2), comparatifs de code "
               "avant/après")

# ---------------------------------------------------------------- styles
S = {}
S["body"] = ParagraphStyle("Body", fontName="FreeSerif", fontSize=10.5, leading=16.5,
                           alignment=TA_JUSTIFY, textColor=TEXT_PRIMARY,
                           spaceBefore=0, spaceAfter=8)
S["lead"] = ParagraphStyle("Lead", parent=S["body"], fontSize=11, leading=17.5,
                           textColor=TEXT_PRIMARY)
S["bullet"] = ParagraphStyle("Bullet", fontName="FreeSerif", fontSize=10.5, leading=15.5,
                             alignment=TA_LEFT, textColor=TEXT_PRIMARY,
                             leftIndent=16, bulletIndent=5, spaceAfter=5,
                             bulletFontName="FreeSerif")
S["h1"] = ParagraphStyle("H1", fontName="FreeSerif", fontSize=22, leading=27,
                         alignment=TA_LEFT, textColor=HEADER_FILL,
                         spaceBefore=0, spaceAfter=2)
S["h2"] = ParagraphStyle("H2", fontName="FreeSerif", fontSize=15, leading=19,
                         alignment=TA_LEFT, textColor=HEADER_FILL,
                         spaceBefore=16, spaceAfter=7)
S["h3"] = ParagraphStyle("H3", fontName="FreeSerif", fontSize=11.5, leading=15,
                         alignment=TA_LEFT, textColor=TEXT_PRIMARY,
                         spaceBefore=12, spaceAfter=5)
S["code"] = ParagraphStyle("Code", fontName="DejaVuSans", fontSize=8.5, leading=12.5,
                           alignment=TA_LEFT, textColor=TEXT_PRIMARY)
S["caption"] = ParagraphStyle("Caption", fontName="FreeSerif", fontSize=8.5, leading=12,
                              alignment=TA_CENTER, textColor=TEXT_MUTED,
                              spaceBefore=3, spaceAfter=6)
S["th"] = ParagraphStyle("TH", fontName="FreeSerif", fontSize=9, leading=12,
                         alignment=TA_CENTER, textColor=colors.white)
S["td"] = ParagraphStyle("TD", fontName="FreeSerif", fontSize=9, leading=12.5,
                         alignment=TA_LEFT, textColor=TEXT_PRIMARY)
S["tdc"] = ParagraphStyle("TDC", parent=S["td"], alignment=TA_CENTER)
S["tdm"] = ParagraphStyle("TDM", fontName="DejaVuSans", fontSize=8, leading=11.5,
                          alignment=TA_LEFT, textColor=TEXT_PRIMARY)
S["callout_stat"] = ParagraphStyle("CalloutStat", fontName="FreeSerif", fontSize=15,
                                   leading=20, alignment=TA_CENTER, textColor=ACCENT)
S["callout_label"] = ParagraphStyle("CalloutLabel", fontName="FreeSerif", fontSize=9,
                                    leading=12.5, alignment=TA_CENTER, textColor=TEXT_MUTED)
S["callout_text"] = ParagraphStyle("CalloutText", fontName="FreeSerif", fontSize=10.5,
                                   leading=16, alignment=TA_LEFT, textColor=TEXT_PRIMARY)
S["toc_title"] = ParagraphStyle("TocTitle", fontName="FreeSerif", fontSize=20, leading=25,
                                alignment=TA_LEFT, textColor=HEADER_FILL, spaceAfter=14)
S["toc0"] = ParagraphStyle("TOC0", fontName="FreeSerif", fontSize=11, leading=20,
                           leftIndent=0, textColor=TEXT_PRIMARY)
S["toc1"] = ParagraphStyle("TOC1", fontName="FreeSerif", fontSize=9.5, leading=16,
                           leftIndent=18, textColor=TEXT_MUTED)

# ---------------------------------------------------------------- helpers
BODY_START = [None]           # page de debut du corps (numerotation arabe)
BODY_FROZEN = [False]         # vrai en phase 2 : la valeur gelee ne bouge plus
MAX_KEEP_HEIGHT = PAGE_H * 0.4


def roman(n):
    vals = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


class BodyStartMarker(Flowable):
    """Marqueur invisible : la page où il est dessiné devient la page 1 du corps."""
    def __init__(self):
        Flowable.__init__(self)
        self.width = 0
        self.height = 0

    def draw(self):
        pass


class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, BodyStartMarker):
            # En phase 2 la valeur est gelee : les pieds de page sont dessines
            # au DEBUT de chaque page, donc une mise a jour en cours de passe
            # laisserait les pages precedentes avec la valeur de la passe
            # anterieure (sommaire sur 2 pages -> numerotation i, 1, 2, 2...).
            if not BODY_FROZEN[0]:
                BODY_START[0] = self.page
            return
        if hasattr(flowable, "bookmark_name"):
            level = getattr(flowable, "bookmark_level", 0)
            text = getattr(flowable, "bookmark_text", "")
            key = getattr(flowable, "bookmark_key", "")
            page = self.page
            # numero affiche = numero de zone (corps -> arabe renumerote),
            # pour coincider avec le pied de page
            if BODY_START[0] is not None and page >= BODY_START[0]:
                page = page - BODY_START[0] + 1
            self.notify("TOCEntry", (level, text, page, key))


def on_page(canvas, doc):
    # setFont AVANT saveState : l'etat restaure reste FreeSerif (jamais Helvetica)
    canvas.setFont("FreeSerif", 7.5)
    canvas.saveState()
    # --- en-tete : titre + filet accent
    canvas.setFont("FreeSerif", 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, PAGE_H - 40, "PROTOCOLE TRIADE v0.3 — DÉMONSTRATION ROOMEQ")
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, PAGE_H - 46, PAGE_W - MARGIN, PAGE_H - 46)
    # --- pied de page : filet + auteur + numero de page zone
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 40, PAGE_W - MARGIN, 40)
    canvas.setFont("FreeSerif", 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, 28, "TRIADE · démonstration RoomEq · 26 octobre 2026")
    if BODY_START[0] is None or doc.page < BODY_START[0]:
        label = roman(doc.page)
    else:
        label = str(doc.page - BODY_START[0] + 1)
    canvas.drawCentredString(PAGE_W / 2.0, 28, label)
    canvas.restoreState()


def heading(text, level=0, style=None):
    """Titre avec signet TOC cliquable."""
    st = style or (S["h1"] if level == 0 else S["h2"])
    key = "h_" + hashlib.md5(text.encode("utf-8")).hexdigest()[:8]
    p = Paragraph('<a name="%s"/><b>%s</b>' % (key, text), st)
    p.bookmark_name = key
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p


def h1_block(text, first_para=None):
    """Chapitre : saut conditionnel + titre + filet accent + 1er paragraphe."""
    items = [heading(text, 0),
             HRFlowable(width="100%", thickness=1.1, color=ACCENT,
                        spaceBefore=3, spaceAfter=10)]
    if first_para is not None:
        items.append(first_para)
    return [CondPageBreak(H1_ORPHAN), KeepTogether(items)]


def h2_block(text, *flowables):
    """Titre H2 + premier contenu, anti-orphelin avec plafond de hauteur."""
    items = [heading(text, 1)]
    for f in flowables:
        if isinstance(f, str):
            items += [Spacer(1, 4), Paragraph(f, S["caption"])]
        else:
            items.append(f)
    total_h = 0
    for el in items:
        try:
            _, h = el.wrap(AVAIL_W, PAGE_H)
        except Exception:
            h = 0
        total_h += h
    if total_h <= MAX_KEEP_HEIGHT:
        return [CondPageBreak(70), KeepTogether(items)]
    if len(items) >= 2:
        return [CondPageBreak(70), KeepTogether(items[:2])] + items[2:]
    return [CondPageBreak(70)] + items


def fr(txt):
    """Typographie française : tiret cadratin insécable au mot précédent."""
    return txt.replace(" " + chr(8212) + " ", chr(160) + chr(8212) + " ")


def para(txt, style="body"):
    return Paragraph(fr(txt), S[style])


def bullets(items):
    return [Paragraph(fr(t), S["bullet"], bulletText="\u2022") for t in items]


def esc(t):
    # entites construites via chr() pour immuniser le source aux retouches
    amp, lt, gt = chr(38), chr(60), chr(62)
    return (t.replace(amp, amp + "amp;")
             .replace(lt, amp + "lt;")
             .replace(gt, amp + "gt;"))


def code_block(txt, label=None):
    """Bloc de code : fond carte + filet accent à gauche.

    Toute ligne commençant par le marqueur '»' est mise en évidence
    (accent + gras) : convention des comparatifs avant/après.
    """
    nbsp = chr(160)
    lines = txt.rstrip("\n").split("\n")
    html_lines = []
    for ln in lines:
        hl = ln.startswith(chr(187))           # '»'
        if hl:
            ln = ln[1:]
        stripped = ln.lstrip(" ")
        pad = len(ln) - len(stripped)
        content = nbsp * pad + esc(stripped) if stripped else nbsp
        if hl:
            content = ('<font color="#3681a6"><b>' + content + "</b></font>")
        html_lines.append(content)
    body = "<br/>".join(html_lines)
    rows = [[Paragraph(body, S["code"])]]
    if label:
        rows.append([Paragraph('<font size="7.5" color="#6f7578">%s</font>' % esc(label),
                               S["code"])])
    t = Table(rows, colWidths=[AVAIL_W * 0.96], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (0, 0), 8),
        ("BOTTOMPADDING", (0, -1), (0, -1), 8),
        ("TOPPADDING", (0, 1), (0, -1), 2),
        ("BOTTOMPADDING", (0, 0), (0, 0), 2 if label else 8),
    ]))
    return t


def code_pair(label_avant, code_avant, label_apres, code_apres):
    """Paire avant/après : deux blocs successifs, libellés normalisés."""
    return [code_block(code_avant, label_avant),
            Spacer(1, 10),
            code_block(code_apres, label_apres),
            Spacer(1, 6)]


def callout(stat, label):
    """Encadré métrique : grand chiffre + libellé."""
    t = Table([[Paragraph("<b>%s</b>" % fr(stat), S["callout_stat"])],
               [Paragraph(fr(label), S["callout_label"])]],
              colWidths=[0.55 * AVAIL_W], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SECTION_BG),
        ("BOX", (0, 0), (-1, -1), 1, ACCENT),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
        ("TOPPADDING", (0, 1), (-1, 1), 2),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ]))
    return t


def callout_note(txt):
    """Encadré note : filet accent gauche + fond teinté."""
    t = Table([[Paragraph(fr(txt), S["callout_text"])]],
              colWidths=[0.96 * AVAIL_W], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SECTION_BG),
        ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return t


def make_table(header, rows, ratios, cell_style="td", header_style=None,
               font_small=False, mono_cols=()):
    """Tableau standard : en-tête M-tier, rayures L-tier, cellules Paragraph."""
    hs = header_style or S["th"]
    cs = S[cell_style]
    if font_small:
        cs = ParagraphStyle("TDS", parent=cs, fontSize=8.3, leading=11.3)
    col_widths = [r * (AVAIL_W * 0.97) for r in ratios]
    assert abs(sum(ratios) - 1.0) < 0.01, "ratios must sum to 1"
    assert sum(col_widths) <= AVAIL_W + 0.5, "table overflow"
    data = [[Paragraph("<b>%s</b>" % fr(h), hs) for h in header]]
    for row in rows:
        line = []
        for i, cell in enumerate(row):
            st = S["tdm"] if i in mono_cols else cs
            line.append(Paragraph(fr(cell), st))
        data.append(line)
    t = Table(data, colWidths=col_widths, hAlign="CENTER", repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
    ]
    for i in range(1, len(data)):
        style.append(("BACKGROUND", (0, i), (-1, i),
                      TABLE_ROW_ODD if i % 2 == 1 else TABLE_ROW_EVEN))
    t.setStyle(TableStyle(style))
    return t


def table_block(title_text, tbl, caption_text):
    """Spacer + tableau + légende, avec anti-orphelin sur le titre."""
    out = [Spacer(1, 14)]
    if len(tbl._cellvalues) <= 12:
        out.append(KeepTogether([tbl, Spacer(1, 4), Paragraph(fr(caption_text), S["caption"])]))
    else:
        out.append(tbl)
        out.append(Spacer(1, 4))
        out.append(Paragraph(fr(caption_text), S["caption"]))
    out.append(Spacer(1, 10))
    return out


def embed_image(path, max_width, max_height):
    pil = PILImage.open(path)
    ow, oh = pil.size
    ratio = min(max_width / ow if ow > max_width else 1.0,
                max_height / oh if oh > max_height else 1.0)
    return Image(path, width=ow * ratio, height=oh * ratio)


def figure(path, caption_text, max_h):
    img = embed_image(path, AVAIL_W, max_h)
    return [Spacer(1, 16),
            KeepTogether([img, Spacer(1, 6), Paragraph(fr(caption_text), S["caption"])]),
            Spacer(1, 12)]


# ================================================================ STORY
story = []

# ---- Sommaire (front matter, numerotation romaine)
toc = TableOfContents()
toc.levelStyles = [S["toc0"], S["toc1"]]
story.append(Paragraph("<b>Sommaire</b>", S["toc_title"]))
story.append(toc)
story.append(PageBreak())
story.append(BodyStartMarker())

# ================================================================ CH 1
story += h1_block(
    "1. Vision et fonction objectif",
    para("Le développement logiciel est entré dans l'ère <i>agent-first</i> : une part "
         "croissante du code est écrite, relue et modifiée par des modèles de langage plutôt "
         "que par des humains. Cette bascule remet en question une hypothèse centrale de nos "
         "outils — que le code source est optimisé pour la lecture humaine. Compilateurs, "
         "systèmes de build et langages ont été conçus autour de cette hypothèse ; si le "
         "lecteur principal devient une machine, l'empilement complet mérite un réexamen "
         "systématique plutôt qu'une révision marginale.", "lead"))

story.append(para(
    "TRIADE est la réponse disciplinée à ce réexamen. Plutôt que de supprimer les langages "
    "— une impossibilité de principe, puisqu'un modèle de langage manipule des symboles "
    "textuels et que tout format binaire rendu lisible par un agent constitue de facto un "
    "langage —, TRIADE déplace le langage vers une fine couche de spécification maintenue "
    "par l'agent, tandis que l'artefact livré est du code machine natif pur. Le compilateur "
    "disparaît du pipeline de production : ce que l'agent écrit est ce qui s'exécute. Le nom "
    "encode l'architecture : trois couches indissociables — <b>Intention</b> (I), "
    "<b>Binaire</b> (B), <b>Carte</b> (C) — unies par un verrou croisé cryptographique."))

story.append(para(
    "Une spécification, si propre soit-elle, reste une promesse tant qu'elle n'a pas survécu "
    "au contact d'un projet réel. C'est l'objet du présent document : exposer le protocole "
    "v0.3 — dont la spécification formelle fait autorité — à travers sa première application "
    "à échelle complète, le recodage intégral de l'application RoomEq. La démonstration est "
    "menée avec les pièces en main : métriques, empreintes, et surtout comparatifs de code "
    "<i>avant/après</i> tirés des deux dépôts, la base scellée v2.2.2 d'un côté, le recodage "
    "cristallisé v3.0.0-dev.1 de l'autre. Chaque comparatif montre la même mécanique : un "
    "défaut de classe « contrat non écrit » devient un contrat nommé, documenté et testé."))

story += h2_block("1.1 Fonction objectif hiérarchisée", callout(
    "Sécurité > Performance > Optimisation > Coût en tokens",
    "Arbitrage lexicographique : un objectif n'est jamais sacrifié au profit d'un objectif "
    "de rang inférieur"))

story.append(para(
    "Toutes les décisions dérivent de cette fonction objectif ordonnée. La <b>sécurité</b> "
    "domine : un artefact plus rapide mais moins sûr est rejeté en amont. La <b>performance</b> "
    "suit immédiatement : l'artefact livré est du code machine sans couche d'exécution "
    "intermédiaire. L'<b>optimisation</b> se fait par profilage sur les chemins critiques, "
    "jamais à l'aveugle. Le <b>coût en tokens</b> n'est optimisé qu'à contrainte égale sur les "
    "trois premiers objectifs — typiquement par la compacité de la carte et l'édition ciblée, "
    "jamais en rognant la vérification. Cette hiérarchie se retrouve à l'identique dans le "
    "journal des décisions de la démonstration RoomEq, dont chaque arbitrage cite la "
    "fonction objectif qu'il sert."))

story += table_block("", make_table(
    ["Objectif", "Signification concrète", "Métrique de validation"],
    [
        ["<b>Sécurité</b>", "Sûreté mémoire validée par oracle, intégrité carte ↔ binaire, "
         "durcissement au chargement", "0 corruption détectée par l'oracle ; tout échec de "
         "verrou bloque la session"],
        ["<b>Performance</b>", "100 % code machine natif, zéro abstraction intermédiaire "
         "entre l'écriture et l'exécution", "Comparaison par bloc scellé face à une référence "
         "compilée (clang -O2 ou équivalent du profil)"],
        ["<b>Optimisation</b>", "Descente à l'ISA sur les hot paths identifiés par "
         "profilage", "Gain mesuré et journalisé pour chaque bloc optimisé"],
        ["<b>Coût en tokens</b>", "Édition ciblée via la carte, jamais de lecture intégrale "
         "du binaire", "Budgets par type d'opération d'édition"],
    ],
    [0.17, 0.44, 0.39]),
    "Tableau 1 — Les quatre objectifs et leurs métriques de validation associées.")

story += h2_block("1.2 Périmètre et non-objectifs", para(
    "Trois non-objectifs bornent l'interprétation. Premièrement, TRIADE ne prétend pas "
    "remplacer les langages dans l'industrie : c'est une architecture de laboratoire, conçue "
    "pour être validée sur des applications réelles complètes — la démonstration RoomEq est "
    "précisément un tel exercice. Deuxièmement, la furtivité face aux EDR n'est pas "
    "recherchée : les interfaces système sont appelées selon les conventions du profil, "
    "comme tout binaire natif légitime. Troisièmement, l'universalité revendiquée par la "
    "v0.3 est structurelle mais progressive : chaque profil de cible doit être instancié et "
    "validé (jalons M6 et M7) avant d'être déclaré supporté — le protocole ne promet pas la "
    "portabilité, il la vérifie. La démonstration qui suit respecte la même exigence "
    "d'honnêteté : elle établira aussi bien ce qu'elle prouve que ce qu'elle ne prouve pas."))

# ================================================================ CH 2
story += h1_block(
    "2. Les trois couches et les dix règles",
    para("L'architecture repose sur une séparation stricte entre ce que l'artefact contient, "
         "ce que l'agent manipule et ce que le destinataire reçoit. Le diff d'intention "
         "descend de I vers C, le verrou croisé relie C et B dans les deux sens, et la couche "
         "B seule quitte le laboratoire. Aucune couche n'est optionnelle : privé de I, le "
         "système perd son ancrage sémantique ; privé de C, l'agent devient aveugle ; privé "
         "de B, il n'y a plus rien à exécuter.", "lead"))

story.append(para(
    "La démonstration RoomEq instancie chacune des trois couches sur un dépôt de code "
    "source — l'adaptation exacte est l'objet du chapitre 6. Le tableau ci-dessous présente "
    "donc chaque couche deux fois : telle que définie par la spécification, et telle "
    "qu'incarnée par le dépôt de démonstration. Cette double lecture est le cœur de la "
    "méthode : les concepts du protocole ne restent pas des abstractions, ils deviennent des "
    "fichiers concrets, diffables et versionnés."))

story += table_block("", make_table(
    ["Couche", "Contenu (spécification v0.3)", "Rôle", "Instanciation RoomEq"],
    [
        ["<b>I</b>", "Spécifications, contrats typés pré/post, invariants logiques — "
         "indépendants de la cible", "Compression de l'intention : le quoi et le pourquoi",
         "44 specs <i>diffables</i> dans I/ (une par module, IDs stables)"],
        ["<b>C</b>", "Index signé, chiffré, fragmenté des blocs : adresses, preuves, "
         "manifestes", "Unique interface de développement de l'agent",
         "CARTE.md — index à adresses stables M-<DOM>-NN, statut par module"],
        ["<b>B</b>", "Code machine scellé, padding inter-blocs, checksums runtime — un "
         "binaire par profil", "Le comment : exécution pure, sémantiquement muette",
         "src/ + tests/ versionnés par git, scellés par tags v3.x.y"],
    ],
    [0.09, 0.34, 0.27, 0.30], font_small=True),
    "Tableau 2 — Les trois couches : définition du protocole et instanciation "
    "dans le dépôt de démonstration.")

story += figure(os.path.join(ASSETS, "diagram_arch.png"),
    "Figure 1 — Architecture TRIADE : le diff d'intention descend de I vers C, le verrou "
    "croisé relie C et B, seule la couche B est livrée (diagramme de la spécification v0.3, "
    "réutilisé pour la continuité de la série).", PAGE_H * 0.34)

story += h2_block("2.1 Les dix règles", para(
    "R1 à R7 proviennent de la v0.1, R8 à R10 de la v0.2 ; la v0.3 n'ajoute aucune règle "
    "— preuve que le noyau normatif était déjà universel — mais en précise deux. Les règles "
    "sont peu nombreuses, vérifiables mécaniquement et sanctionnées par des effets concrets "
    "— refus de build, refus de commit ou blocage de session — plutôt que par des "
    "recommandations. La colonne de droite montre comment chacune se traduit dans le dépôt "
    "de démonstration : c'est la table de correspondance qui a gouverné sept vagues de "
    "recodage."))

story += table_block("", make_table(
    ["#", "Règle", "Énoncé (spécification)", "Traduction RoomEq"],
    [
        ["R1", "Jamais de binaire nu", "Tout artefact B est accompagné de I et C à jour",
         "Aucun fichier de src/ sans module cartographié ni spec I"],
        ["R2", "Intention d'abord", "Toute modification commence par un diff sur I",
         "La spec I du module est écrite AVANT le code (44 specs)"],
        ["R3", "Balisage obligatoire", "Chaque bloc est décrit dans C",
         "Chaque commit porte son module ; la Carte est tenue à jour"],
        ["R4", "Patch à contrat stable", "Le remplacement préserve signatures et contrats",
         "L'API publique d'un module ne change pas sans bump de sa spec"],
        ["R5", "Vérifie-puis-écrit", "Aucun commit sans oracle, vecteurs dorés, round-trip",
         "build 0/0 + 100 % des tests verts avant chaque commit"],
        ["R6", "Cristallisation", "Dix vérifications rendent le bloc immuable",
         "Tags de version ; modules verrouillés (42 au tag v3.0.0-dev.1)"],
        ["R7", "Adresses stables", "Les points d'entrée ne bougent jamais",
         "IDs de module M-<DOM>-NN immuables dans la Carte"],
        ["R8", "Verrou croisé", "Empreintes et signature vérifiées avant chaque édition",
         "Empreintes SHA-256 des données critiques ; parité md5 vérifiée"],
        ["R9", "Carte signée obligatoire", "L'agent refuse toute carte non signée",
         "Historique git intégral ; base de référence scellée (deff25c)"],
        ["R10", "Fail-closed au chargement", "Checksums vérifiés au lancement ; écart = arrêt",
         "Tests d'échec explicites (fragments courts, bruit seul, etc.)"],
    ],
    [0.06, 0.17, 0.37, 0.40], font_small=True),
    "Tableau 3 — Les dix règles du protocole et leur traduction concrète dans le dépôt "
    "de démonstration.")

story.append(para(
    "Quatre invariants structurels complètent le tableau, vérifiés à chaque cycle de build "
    "dont la violation est un refus de build : B n'est jamais nu (R1) ; les adresses "
    "exposées sont stables (R7, par profil) ; la signature couvre la carte entière (R9) ; "
    "B est auto-vérifiant au chargement (R10). Dans le dépôt de démonstration, ces "
    "invariants ont leurs homologues immédiats : aucun code orphelin, aucune refonte "
    "d'identifiants, un historique intégral et des tests d'échec qui garantissent que les "
    "conditions aux limites se traduisent par des exceptions propres plutôt que par des "
    "comportements indéfinis."))

# ================================================================ CH 3
story += h1_block(
    "3. Boucle de mise à jour et vérification",
    para("La boucle de mise à jour est le battement de cœur du protocole : c'est la seule "
         "voie par laquelle le logiciel évolue. Elle se déroule en sept étapes réparties en "
         "deux phases — l'édition, puis la validation et le commit — séparées par un point "
         "de non-retour : rien n'est écrit dans le binaire avant que l'oracle n'ait rendu "
         "son verdict.", "lead"))

story += table_block("", make_table(
    ["N", "Étape", "Entrées → sorties", "Règles"],
    [
        ["1", "Diff d'intention", "Requête de changement, couche I → diff minimal sur I", "R2"],
        ["2", "Localisation", "frag-loc → liste des blocs impactés", "R3"],
        ["3", "Verrou croisé", "frag-bld, binaire → verdict go / no-go", "R8, R9"],
        ["4", "Régénération ciblée", "frag-con, notation du bloc → octets candidats", "R4, R7"],
        ["5", "Vérification", "candidats, oracle, vecteurs dorés → verdict, journal", "R5"],
        ["6", "Commit atomique", "verdict favorable → patch B, carte à jour, scellage", "R1"],
        ["7", "Cristallisation", "compteur de vérifications → bloc immuable", "R6"],
    ],
    [0.06, 0.22, 0.52, 0.20]),
    "Tableau 4 — La boucle de mise à jour en sept étapes (spécification v0.3).")

story += h2_block("3.1 Les trois piliers de vérification", para(
    "Supprimer le compilateur, c'est perdre les filets de sécurité qu'il tendait "
    "gratuitement : vérification de types, initialisation, analyse de flot. La stratégie de "
    "vérification reconstruit une confiance équivalente — voire supérieure — sans "
    "réintroduire de couche de traduction dans l'artefact. Elle repose sur trois piliers. "
    "L'<b>oracle éphémère</b> d'abord : implémentation de référence de chaque bloc, triviale "
    "et volontairement lente, dérivée de la couche I, générée au début de chaque session, "
    "utilisée pour des tests différentiels puis détruite — jamais livrée, jamais archivée. "
    "Le <b>round-trip de notation</b> ensuite : chaque bloc assemblé est désassemblé et "
    "comparé à la notation d'origine, tout écart étant un échec de build — ce contrôle à "
    "coût quasi nul attrape la classe d'erreurs la plus insidieuse, l'écart silencieux entre "
    "ce que l'agent croit avoir écrit et les octets réellement produits. La "
    "<b>cristallisation</b> enfin : plus un bloc fait ses preuves, moins il coûte à "
    "vérifier, ce qui libère le budget pour les blocs jeunes et les zones actives."))

story.append(para(
    "Dans un recodage applicatif, ces trois piliers ont des homologues directs, et la "
    "démonstration les a exploités systématiquement. L'oracle devient la <b>suite de tests "
    "portée et étendue</b> : la suite v2.2.2 encode le comportement réellement validé, et "
    "chaque constante numérique de référence (tolérances, amplitudes, fréquences) en a été "
    "extraite — la décision D5 du dépôt de démonstration pose explicitement que les tests "
    "sont le contrat exécutable de la couche I. Le round-trip devient l'<b>audit de "
    "parité</b> : comparaison point par point des 14 familles de fonctionnalités du README "
    "de la base scellée, empreintes md5 des données embarquées, vérification ligne à ligne "
    "des comportements clés. La cristallisation devient le <b>tag</b> : le point nommé, "
    "restaurable, qui fige les contrats — avec la nuance des pré-versions -dev.N, "
    "inventées pendant la démonstration pour distinguer « vérifié par tests » de « validé "
    "sur machine réelle »."))

story.append(callout_note(
    "Le pivot de toute la boucle est R5 — <b>vérifie-puis-écrit</b> : aucun commit sans "
    "vérification complète. Dans la démonstration, cette règle s'est appliquée à chaque "
    "vague et à chaque commit intermédiaire : build 0 erreur 0 avertissement et 100 % des "
    "tests verts, sans exception. Ce sont exactement 437 vérifications unitaires qui "
    "défendent la cristallisation finale, contre 228 pour la base scellée."))

# ================================================================ CH 4
story += h1_block(
    "4. Universalité, profils et gouvernance",
    para("Depuis la v0.3, le cœur du protocole — couches, règles, boucle, vérification — "
         "est indépendant de la cible par construction, et tout ce qui dépend de la cible "
         "est regroupé dans un <b>profil de cible</b> défini par sept éléments vérifiables : "
         "ISA, ABI, format d'exécutable, interface système, mécanisme de patch à chaud, "
         "moteur de notation, granularité des blocs. L'universalité devient une propriété "
         "structurelle : instancier une plateforme nouvelle revient à écrire un profil, "
         "jamais à modifier le protocole.", "lead"))

story += table_block("", make_table(
    ["Profil", "ISA / OS", "Format", "Interface", "Statut"],
    [
        ["x86-64-win11-pe", "x86-64 / Windows 11", "PE32+", "IAT (kernel32, ws2_32, "
         "Schannel)", "Primaire — jalons M0-M5"],
        ["x86-64-linux-elf64", "x86-64 / Linux", "ELF64", "syscalls + libc",
         "M6 — portabilité inter-OS"],
        ["riscv64-linux-elf64", "RISC-V 64 / Linux", "ELF64", "syscalls + libc",
         "M7 — portabilité inter-ISA"],
        ["aarch64-macos-macho", "AArch64 / macOS", "Mach-O", "libSystem",
         "Réservé"],
        ["wasm32-wasi", "WebAssembly / WASI", "module Wasm", "WASI", "Réservé — étude"],
    ],
    [0.24, 0.20, 0.12, 0.26, 0.18], font_small=True, mono_cols=(0,)),
    "Tableau 5 — Les profils de cible de la v0.3 ; le cœur du protocole est partagé, "
    "chaque profil instancie ses octets et ses empreintes.")

story.append(para(
    "La gouvernance est le second pilier d'universalité : le protocole ne se révisant "
    "jamais en silence. Chaque décision structurante est consignée dans un journal — D1 à "
    "D17 pour le protocole lui-même, D1 à D11 pour la démonstration — avec ses alternatives "
    "rejetées et sa justification rattachée à la fonction objectif. Toute révision future "
    "doit soit respecter ces décisions, soit expliciter précisément ce qui les invalide : "
    "cette discipline évite la dérive progressive qui transforme un protocole propre en "
    "accumulation d'exceptions incohérentes. La démonstration en a bénéficié deux fois : "
    "l'amendement D9 (parité des données embarquées) et l'extension D11 (reverse-specs de "
    "l'installateur scellé, chapitre 10) sont des décisions journalisées, datées et "
    "justifiées, pas des accommodements improvisés."))

story.append(para(
    "Enfin, l'anti-enfermement : l'export de continuité (D16) permet au développeur de "
    "sauvegarder et transférer l'intégralité de son état de développement — couches I, B, C "
    "et manifeste autodescriptif — sous forme d'un conteneur chiffré et signé, afin de "
    "reprendre le projet avec n'importe quel agent conforme. Le dépôt de démonstration en "
    "applique l'esprit par sa redondance systématique : dépôt git local comme source de "
    "vérité, miroir Drive avec bundle d'historique restaurable, miroir GitHub privé — trois "
    "exemplaires de chaque avancée, synchronisés après chaque vague. Cette redondance n'est "
    "pas décorative : le recodage a survécu à une réinitialisation complète du bac à sable "
    "en cours de projet, restaurée depuis les sauvegardes sans perte de travail."))

# ================================================================ CH 5
story += h1_block(
    "5. Le candidat : RoomEq et sa dette",
    para("RoomEq est un égaliseur acoustique temps réel pour Windows et macOS : il mesure la "
         "réponse d'une pièce par balayage logarithmique, calcule une correction, l'applique "
         "en temps réel sur le son du système, et offre une console de mixage complète — "
         "pistes, EQ par piste, routage par carte son virtuelle, pont ASIO vers les DAW. "
         "L'application est écrite en C# / .NET 8 / Avalonia 11 et s'appuie sur des composants "
         "natifs scellés : un pilote audio virtuel Windows, une DLL ASIO, un greffon "
         "CoreAudio macOS et des installateurs.", "lead"))

story.append(para(
    "C'est un candidat de démonstration exigeant, donc honnête. Exigeant parce que le "
    "périmètre est réel et complet : traitement du signal (FFT, filtres, déconvolution), "
    "entrées-sorties audio multiplateformes, interface graphique à six onglets, persistance, "
    "télémétrie — quatorze familles de fonctionnalités documentées au README de la base de "
    "référence. Honnête parce que la base de référence est scellée et vérifiable : le tag "
    "v2.2.2 (commit deff25c, CI verte), cloné localement en lecture seule, sert d'oracle "
    "pour toute la démonstration — rien ne repose sur une mémoire de session."))

story.append(para(
    "L'état de départ concentre en revanche la dette que le protocole est censé éliminer. "
    "Le code applicatif est fonctionnel et testé — 228 tests verts — mais la structure s'est "
    "dégradée version après version : des ViewModels de plus de mille lignes mélangeant "
    "routage, volume, pilote et persistance ; des specs inexistantes ; des constantes "
    "critiques enfouies dans le code ; et, côté installateur, une histoire de défauts "
    "répétés qui ont coûté trois versions (v2.2.0, v2.2.1, v2.2.2) — défauts dont l'analyse "
    "a posteriori révélera qu'ils sont tous de classe « contrat non écrit », exactement la "
    "classe que TRIADE verrouille."))

story += table_block("", make_table(
    ["Mesure", "Base scellée v2.2.2 (deff25c)"],
    [
        ["Fichiers C# applicatifs (src/)", "82"],
        ["Lignes de code (src/)", "14 891"],
        ["Fichiers de tests / lignes", "23 / 4 032"],
        ["Tests unitaires (Core + Audio)", "228 (150 + 78) — aucun test App"],
        ["Plus gros fichier", "MixerViewModel.cs — <b>1 075 lignes</b>"],
        ["Autres monolithes", "MainViewModel 611 · CalibrationViewModel 474 · MicViewModel 417"],
        ["Spécifications d'intention", "aucune"],
        ["Avertissements de compilation", "tolérés"],
    ],
    [0.42, 0.58]),
    "Tableau 6 — État de la base de référence au démarrage de la démonstration.")

story.append(callout_note(
    "Le périmètre de recodage est délimité par la décision D1 du dépôt : l'application C# "
    "seule. Les composants natifs — pilote roomeqvad.sys, DLL ASIO, greffon macOS, "
    "installateurs — restent <b>scellés v2.2.2</b> et consommés tels quels via les mêmes "
    "points d'entrée. Le pilote n'a jamais été en cause dans aucun incident ; le réécrire "
    "aurait été un risque nu (BSOD) sans aucun gain — la fonction objectif l'interdit."))

# ================================================================ CH 6
story += h1_block(
    "6. L'adaptation du protocole au code source",
    para("La spécification v0.3 définit I/B/C pour du code machine ; un recodage applicatif "
         "manipule du code source compilé. La décision D4 du dépôt de démonstration pose "
         "l'équivalence structurelle : l'intention = la spec diffable, le binaire = le code "
         "compilé depuis une révision scellée, la carte = l'index des modules. Les règles "
         "s'appliquent alors telles quelles — seuls changent les artefacts concrets qui les "
         "portent.", "lead"))

story.append(para(
    "Concrètement : la couche I vit dans <b>I/<domaine>/I-*.md</b> — une spécification "
    "par module, à identifiant stable, écrite dans un format conçu pour être diffable ; la "
    "couche B vit dans <b>src/ + tests/</b>, versionnée par git et scellée par tags de "
    "version ; la couche C est <b>CARTE.md</b>, à la racine du dépôt — l'index de navigation "
    "à adresses stables qui relie chaque module à sa spec, son code et ses tests, avec son "
    "statut. Voici l'en-tête réel de la carte cristallisée :"))

story.append(code_block(
"""| En-tete | Valeur |
|---|---|
| projet | RoomEq v3.0.0-dev.1 - egaliseur acoustique temps reel |
| profil de cible | x86-64-pc-windows-msvc (.NET 8 + Avalonia 11) + macOS (greffon scelle) |
| base de reference | v2.2.2 (GitHub alexisfrlopez-debug/RoomEq @ deff25c, tag v2.2.2) |
| empreinte legacy | clone git roomeq-git-ref (code, CI verte) + miroir Drive roomeq-legacy |
| statut | cristallise au tag v3.0.0-dev.1 (D10) - 42 modules verrouilles, 437 tests |
         |  verts, parite v2.2.2 etablie (docs/PARITE-v2.2.2.md) |

| ID | Module | Spec I | Code | Tests | Statut |
|----|--------|--------|------|-------|--------|
| M-DSP-01 | FFT radix-2 | I/dsp/I-fft.md | src/RoomEq.Core/Dsp/Fft.cs | FftTests.cs | verrouille |
| M-CAL-02 | Analyse de balayage | I/calibration/I-analyse-balayage.md | SweepAnalyzer.cs | SweepAnalyzerTests.cs | verrouille |
| M-AUD-03 | Routage / mixeur | I/audio/I-routage.md | Routing/ (12 fichiers) | RingBuffer + 3 suites | verrouille |
| M-INS-02 | Contrat Win32 PnP | I/installateur/I-contrat-win32.md | futur Win32Pnp.cs | - | spec prete |""",
    "CARTE.md — en-tête et extrait de l'index (extrait adapté : pictogrammes de statut "
    "remplacés par leur libellé). Le tableau complet couvre 42 modules applicatifs, "
    "8 modules installateur et 4 natifs scellés."))

story.append(Spacer(1, 6))

story.append(para(
    "La convention de statut formalise le cycle de vie d'un module : non commencé, en "
    "cours, recodé avec tests verts et spec à jour, puis <b>verrouillé</b> — cristallisé par "
    "tag de version, contrat I gelé. La démonstration a enrichi cette convention d'une "
    "nuance devenue nécessaire en pratique : les <b>pré-versions de cristallisation</b> "
    "(-dev.N). Le tag v3.0.0-dev.1 marque l'état « recodage vérifié par 437 tests, "
    "validation utilisateur Windows réelle non encore effectuée » : les contrats sont "
    "gelés, mais l'ouverture de la version finale attend la validation terrain. Cette "
    "distinction — absente du protocole d'origine, qui cristallise à dix vérifications — "
    "est l'un des enseignements que la démonstration renvoie au protocole."))

story += h2_block("6.1 Le cycle de travail, appliqué", para(
    "Chaque vague a suivi le même cycle, dérivé de la boucle de mise à jour : écriture des "
    "specs I des modules de la vague (diff d'intention, R2) ; recodage clean-room informé "
    "par la lecture de la base scellée (régénération, R4 — l'API publique ne change pas "
    "sans bump de spec) ; portage et extension de la suite de tests (l'oracle, D5) ; "
    "vérification complète — build 0 erreur 0 avertissement, 100 % des tests verts "
    "(vérifie-puis-écrit, R5) ; marquage de la Carte (balisage, R3) ; commit et sauvegarde "
    "systématique sur trois destinations (le dépôt local, GitHub, le Drive avec bundle "
    "restaurable). Le respect de ce cycle n'a jamais été négociable : aucun commit de la "
    "démonstration n'a été réalisé sans vérification complète au préalable."))

# ================================================================ CH 7
story += h1_block(
    "7. Le recodage, vague par vague",
    para("L'ordre de recodage est bottom-up (décision D3) : d'abord RoomEq.Core — le DSP "
         "pur, sans dépendance sortante, entièrement testable — puis RoomEq.Audio, les "
         "entrées-sorties et le routage, enfin RoomEq.App, l'interface graphique. Valider "
         "d'abord le cœur garantit que les couches hautes s'appuient sur du solide : c'est "
         "l'application directe de R5 à l'échelle des modules. Sept vagues ont été "
         "nécessaires, réparties sur cinq sessions de travail.", "lead"))

story += table_block("", make_table(
    ["Vague", "Périmètre", "Modules", "Tests cumulés"],
    [
        ["1", "Fondations TRIADE : dépôt, Carte, décisions D1-D7, outillage de sauvegarde",
         "structure du dépôt", "s.o."],
        ["2", "Core / Dsp + Eq : FFT, fenêtres, biquads RBJ, bruits, ESS, spectre, chaîne EQ",
         "M-DSP-01..07, M-EQ-01..03", "86"],
        ["3", "Core / Calibration + casques : déconvolution, cibles, planificateur, profils",
         "M-CAL-01..08, M-HPH-01", "150"],
        ["4", "Core / Io : saveur test/public, journal, télémétrie, magasins",
         "M-IO-01..05", "212"],
        ["5", "Audio : capture/lecture WASAPI-AUHAL, routage, ponts ASIO et macOS, mesure",
         "M-AUD-01..06", "354"],
        ["6", "App : shell Avalonia, ViewModels décomposés, contrôles, six onglets",
         "M-APP-01..05, M-EQ-04", "436"],
        ["7", "Finalisation : parité v2.2.2, comblement D9, cristallisation, packaging, CI",
         "42 modules verrouillés", "437"],
    ],
    [0.08, 0.50, 0.24, 0.18], font_small=True),
    "Tableau 7 — Les sept vagues du recodage ; les specs I de chaque vague ont été écrites "
    "avant le code, et chaque vague s'est close par la vérification complète (R5).")

story.append(para(
    "Deux points méritent d'être soulignés. D'abord, la vague 5 a recodé la couche la plus "
    "déliée — 26 fichiers, 5 500 lignes, threads audio, protocole de mémoire partagée avec "
    "la DLL ASIO — en verrouillant le protocole du pont par huit tests à constantes, "
    "décalages et tailles figées : toute dérive du miroir C/C# serait détectée avant "
    "livraison. Ensuite, la vague 6 a appliqué une discipline de taille stricte — chaque "
    "fichier de ViewModel sous la barre des 300 lignes — en décomposant les monolithes par "
    "responsabilité, ce que le chapitre 8 détaille sur pièce."))

story.append(para(
    "La vague 7 a clos le chantier par la vérification de non-régression : audit de parité "
    "point par point contre la base scellée (chapitre 9), comblement de la bibliothèque "
    "casques de 255 à 321 modèles — l'audit avait révélé un jeu de données resté à la "
    "version v2.0.0 alors que la v2.1.0 l'avait étendu (décision D9, patch à contrat "
    "stable) — puis cristallisation : version 3.0.0-dev.1, Carte passée en statut "
    "verrouillé pour les 42 modules applicatifs, tag git annoté, packaging auto-contenu "
    "win-x64 en trois livrables, et intégration continue GitHub Actions couvrant les tests "
    "sur trois systèmes d'exploitation."))

story.append(callout(
    "437 / 437 tests verts · build 0 erreur 0 avertissement",
    "État de la cristallisation v3.0.0-dev.1 : 220 Core + 142 Audio + 75 App — "
    "contre 228 tests pour la base scellée"))

# ================================================================ CH 8
story += h1_block(
    "8. Avant / après : trois comparatifs de code",
    para("Ce chapitre est la pièce centrale de la démonstration. Trois comparatifs, tirés "
         "des deux dépôts réels — la base scellée v2.2.2 d'un côté, le recodage "
         "v3.0.0-dev.1 de l'autre — montrent la même mécanique à l'œuvre : ce que le "
         "protocole change concrètement au code. Les extraits sont verbatim, seule la "
         "présentation est adaptée (lignes saillantes marquées en couleur).", "lead"))

# ---------------------------------------------------------------- 8.1
story += h2_block("8.1 Le seuil de détection : d'un nombre magique à un contrat mesuré",
                  para(
    "L'analyseur de balayage détecte le pic de la réponse impulsionnelle dans une capture "
    "et le compare au plancher de bruit — la médiane des magnitudes. Si le rapport "
    "pic/médiane est trop faible, la capture ne contient pas de balayage et l'analyse doit "
    "le signaler à l'utilisateur plutôt que de produire des bandes absurdes. Voici le "
    "seuil tel qu'il vivait dans la base scellée :"))

story.append(code_block(
"""        // plancher de bruit : médiane des magnitudes de la zone de recherche
        var mags = new List<double>(Math.Max(1, searchEnd / 16));
        for (int i = 0; i < searchEnd; i += 16) mags.Add(Y[i].Magnitude);
        mags.Sort();
        double median = mags[mags.Count / 2];
»       if (peakMag < Math.Max(median * 8.0, 1e-9))
        {
            double snr = median > 0 ? peakMag / median : 0;
            throw new InvalidOperationException(
»               $"Balayage non détecté dans la capture (rapport pic/bruit {snr:0.0} < 8, " +
                $"retard du meilleur candidat {peak / (double)sampleRate:0.000} s) : vérifiez le " +
                "niveau de test, le micro sélectionné (évitez les cartes virtuelles type « RoomEq " +
                "Output ») et le routage.");
        }""",
    "AVANT — v2.2.2 · src/RoomEq.Core/Calibration/SweepAnalyzer.cs, lignes 95-107. "
    "Le seuil 8 est un littéral sans nom, dupliqué dans le message, sans justification "
    "ni test."))

story.append(Spacer(1, 8))
story.append(para(
    "Le seuil vaut 8. Pourquoi 8 ? Rien dans le code ne le dit — c'est un nombre magique, "
    "typique de la classe « contrat non écrit ». Le défaut est réel : la déconvolution "
    "divise par le spectre du balayage au carré, ce qui agit comme un différenciateur hors "
    "bande ; une capture de <i>bruit seul</i> produit ainsi un faux pic à retard proche de "
    "zéro avec un rapport pic/médiane mesuré à environ 186 — largement au-dessus de 8. "
    "Concrètement : un utilisateur qui a mal routé sa capture se voyait attribuer une "
    "« correction » aléatoire au lieu du message d'aide. Le protocole ne se contente pas de "
    "corriger : il établit d'abord les faits, par un diagnostic empirique mené en "
    "laboratoire — bruit blanc pur : rapport 186 ; bruit passe-bas réaliste : 9,2 ; "
    "balayage réel, même atténué : au-delà de 10<super>5</super>, mesuré à 1,2 × "
    "10<super>7</super>. La décision D8 en découle : un seuil de 1000 rejette le bruit "
    "seul avec quatre décades de marge et garde quatre décades de marge aux balayages "
    "réels faibles."))

story.append(code_block(
"""    /// <summary>
    /// Seuil de détection du balayage : rapport minimal pic/médiane de la réponse
    /// impulsionnelle. Amélioration v3 (décision D8) : la v2.2.2 utilisait 8, ce
    /// qui laissait passer une capture de bruit seul (ratio mesuré ~186 par effet
    /// différenciateur du 1/|X|<super>2</super>) et produisait des bandes absurdes au lieu du
    /// message d'aide. Un balayage réel, même faible, dépasse 1e5 (mesuré ~1,2e7) ;
    /// le seuil 1000 rejette le bruit seul avec quatre décades de marge.
    /// </summary>
»   public const double DetectionSnr = 1000.0;
    [...]
        // plancher de bruit : médiane des magnitudes de la zone de recherche
        [...]
»       if (peakMag < Math.Max(median * DetectionSnr, 1e-9))
        {
            double snr = median > 0 ? peakMag / median : 0;
            throw new InvalidOperationException(
»               $"Balayage non détecté dans la capture (rapport pic/bruit {snr:0.0} "
                + $"< {(int)DetectionSnr}, " + [...]""",
    "APRÈS — v3 · src/RoomEq.Core/Calibration/SweepAnalyzer.cs. Le seuil devient une "
    "constante publique nommée, sa rationale est documentée à même le code, et le message "
    "dérive de la constante (plus de duplication)."))

story.append(Spacer(1, 8))
story.append(para(
    "Mais l'essentiel est ailleurs : le contrat ne vit plus seulement dans le code. Il est "
    "d'abord écrit dans la spec I du module — la couche d'intention, diffable — puis "
    "verrouillé par un test qui rejette explicitement le bruit seul :"))

story.append(code_block(
"""3. Détection : pic de la RI dans [-0,5 s ; +1,2 s] ; plancher = médiane des
   magnitudes ; rejet si pic < 1000× la médiane (InvalidOperationException explicite).
   [v3/D8 : la v2.2.2 rejetait sous 8× — laissait passer une capture de bruit
   seul, ratio ~186 par effet différenciateur du 1/|X|<super>2</super>, et rendait des bandes
   absurdes ; balayage réel mesuré ~1,2e7, bruit passe-bas réaliste 9,2 → le
   seuil 1000 sépare avec quatre décades de marge]""",
    "Couche I — I/calibration/I-analyse-balayage.md (extrait). Le contrat porte la "
    "décision, sa mesure et sa justification : diffable, datée, vérifiable."))

story.append(Spacer(1, 8))

story.append(code_block(
"""    [Fact]
    public void PureNoise_IsRejected()
    {
        var spec = new LogSweepSpec(20, 20000, 4.0);
        var rng = new Random(99);
        var noise = new float[Fs * 4];
        for (int i = 0; i < noise.Length; i++)
            noise[i] = (float)(rng.NextDouble() * 2 - 1) * 0.01f;

        var ex = Assert.Throws<InvalidOperationException>(
            () => SweepAnalyzer.Analyze(noise, Fs, spec));
        Assert.Contains("Balayage non détecté", ex.Message, StringComparison.Ordinal);
    }""",
    "Couche B — tests/RoomEq.Core.Tests/CalibrationHeadphoneTests.cs : le verrou "
    "exécutable. Un balayage réel doit passer (test KnownRoom_IsDeconvolved) ; le bruit "
    "seul doit être rejeté."))

story.append(Spacer(1, 6))
story.append(para(
    "Le même défaut est désormais verrouillé à quatre niveaux : la constante nommée dans "
    "le code, la rationale documentée dans le commentaire, le contrat dans la spec I, et "
    "le test qui rejette le bruit seul. C'est l'illustration la plus directe de ce que le "
    "protocole apporte : un réglage critique n'est plus une valeur enfouie — c'est une "
    "décision datée, mesurée, justifiée et défendue par l'oracle. Et le coût marginal a "
    "été faible : le diagnostic complet, la décision, la spec et les tests représentent une "
    "fraction de ce qu'aurait coûté le seul dépannage du défaut en production."))

# ---------------------------------------------------------------- 8.2
story += h2_block("8.2 Le monolithe : mille soixante-quinze lignes, cinq responsabilités",
                  para(
    "Le ViewModel de la table de mixage concentrait tout ce qu'un God object fait de "
    "pire : routage de la carte virtuelle, synchronisation des curseurs de volume, "
    "installation du pilote, persistance du mixeur et politique de presets, entrelacés sur "
    "1 075 lignes. L'extrait suivant montre le haut du fichier — les seuls champs "
    "d'instance et propriétés observables occupent des dizaines de lignes, et chaque "
    "responsabilité y côtoie les autres :"))

story.append(code_block(
"""public partial class MixerViewModel : ObservableObject
{
    private readonly PlaybackEngine _engine;
    private readonly AudioDeviceCatalog _catalog = new();
    private readonly MixerStore _store = new();
    private readonly DispatcherTimer _timer;
    private readonly EndpointVolumeController _endpointVolume = new();
    private readonly DriverSetupManager _driverSetup = new();
    private DispatcherTimer? _eqSyncDebounce;

    // synchro des deux curseurs de volume (barre du haut + Mixage) : une seule
    // source de vérité (le volume Windows de la carte), tous les affichages suivent
    private readonly Action<double>? _syncTopBarVolume; // recale le curseur de la barre du haut
    private bool _syncingRoutedVolume;   // écriture PROGRAMMATIQUE de RoutedVolume en cours
    private bool _routedVolumeReady;     // premier état réel reçu (le binding initial ne doit rien écrire)
    private double _lastEndpointSeen = -1; // détection des changements faits hors de l'application
    [...]
    [ObservableProperty] private OutputDeviceInfo? selectedOutput;
    [ObservableProperty] private OutputPresetOption? selectedOutputPresetOption;
    [ObservableProperty] private bool autoOutputPreset = true;
    [ObservableProperty] private IVirtualAudioProvider selectedProvider = VirtualAudioCatalog.Default;
    [ObservableProperty] private VirtualCardStatus virtualCard = new();
    [ObservableProperty] private string virtualStatusText = "Recherche de la carte son virtuelle…";
    [ObservableProperty] private bool isInstalling;
    [ObservableProperty] private string installPhaseText = "";
    [ObservableProperty] private double installPercent;
    [ObservableProperty] private bool installIndeterminate = true;
    [ObservableProperty] private string routingStatusText = "Routage à l'arrêt.";
    [ObservableProperty] private string asioStatusText = "Pont ASIO à l'arrêt.";
    [...]
    // ... 39 propriétés observables et commandes au total ; routage, volume,
    // pilote, persistance et presets entrelacés jusqu'à la ligne 1 075.""",
    "AVANT — v2.2.2 · src/RoomEq.App/ViewModels/MixerViewModel.cs (extrait des lignes "
    "25-95). Aucun test ne peut s'approcher de cette classe sans périphérique audio réel."))

story.append(Spacer(1, 8))
story.append(para(
    "Le recodage a décomposé ce monolithe par responsabilité — le spec I de l'onglet "
    "mixage l'exigeait avant même que le code n'existe — et extrait la politique de presets "
    "vers une classe dédiée à interfaces étroites :"))

story.append(code_block(
"""src/RoomEq.App/ViewModels/
├── MixerViewModel.cs            399 lignes   cœur : canaux, transport, VU, état
├── MixerViewModel.Routing.cs    224 lignes   routage : carte virtuelle, boucle, défauts
├── MixerViewModel.Driver.cs     209 lignes   pilote : détection, installation pnputil
├── MixerViewModel.Volume.cs     160 lignes   volume : synchro barre ↔ master ↔ système
└── MixerViewModel.Persist.cs    138 lignes   persistance : mixer.json, restauration
                                ───────
                                1 130 lignes en 5 fichiers, 1 responsabilité chacun

+ OutputPresetCoordinator.cs     politique « preset adapté à la sortie », extraite
  du monolithe derrière deux interfaces étroites (IOutputPresetEqView,
  IOutputPresetMixerView) → la priorité calibration > usine reconnue > manuel
  mémorisé est testée SANS périphérique audio (75 tests App, dont les replis)""",
    "APRÈS — v3 · structure du dépôt recodé. Chaque fichier porte une responsabilité "
    "unique ; la politique de presets est devenue testable."))

story.append(Spacer(1, 8))
story.append(para(
    "Le gain n'est pas cosmétique. La décomposition a rendu visibles — et donc "
    "corrigeables — deux défauts fonctionnels que le monolithe masquait : le message "
    "d'aide ASIO n'était jamais affiché sans pilote (la propriété SelectedDriver restait "
    "nulle, aucun PropertyChanged n'était levé) ; le garde-fou « Lier ce preset à la "
    "sortie » laissait passer le preset plat par défaut, déclenchant une demande de nom "
    "puis un refus en cascade. Les deux correctifs sont couverts par des tests, et la "
    "politique de presets extraite est vérifiée sans périphérique : ce qui était "
    "impensable sur le monolithe est devenu une suite de tests ordinaire. C'est la "
    "règle R3 — le balisage — appliquée à l'architecture : un module, une responsabilité, "
    "une adresse stable dans la Carte."))

# ---------------------------------------------------------------- 8.3
story += h2_block("8.3 Le caractère invisible : un défaut révélé par l'oracle multi-plateformes",
                  para(
    "Les magasins de réglages sécurisent les noms de fichiers avant écrire sur disque. "
    "La base scellée déléguait cette sécurité à l'API de l'OS hôte :"))

story.append(code_block(
"""    public static string SanitizeFileName(string name)
    {
»       foreach (char c in Path.GetInvalidFileNameChars())
            name = name.Replace(c, '_');
        return name.Trim();
    }""",
    "AVANT — v2.2.2 · src/RoomEq.Core/Io/Stores.cs, lignes 37-42. La liste des caractères "
    "interdits dépend du système qui exécute le code."))

story.append(Spacer(1, 8))
story.append(para(
    "Le défaut est invisible sur la machine de développement Windows, et c'est précisément "
    "le problème : <i>Path.GetInvalidFileNameChars()</i> renvoie la liste de l'OS hôte. Un "
    "nom sanitizé sous Linux — où les deux-points sont légaux — peut donc produire un "
    "fichier invalide s'il est copié sous Windows. Le défaut n'a été révélé que parce que "
    "la vérification R5 de la démonstration exécute les tests sous Linux : l'oracle a fait "
    "son travail. Le correctif fige l'union des deux mondes, indépendamment de l'hôte :"))

story.append(code_block(
"""    /// <summary>
    /// Caractères interdits dans un nom de fichier sur AU MOINS une plateforme
    /// cible (Windows + macOS/Linux) — union fixe, indépendante de l'OS hôte :
    /// un nom sanitizé sous Linux doit rester valide s'il est copié sous Windows
    /// (v2.2.2 : Path.GetInvalidFileNameChars() dépendait de l'OS hôte).
    /// </summary>
    private const string InvalidFileNameChars =
        "<>:\\"/\\\\|?*" +
        "\\u0000\\u0001\\u0002\\u0003\\u0004\\u0005\\u0006\\u0007" +
        "\\u0008\\u0009\\u000a\\u000b\\u000c\\u000d\\u000e\\u000f" +
        "\\u0010\\u0011\\u0012\\u0013\\u0014\\u0015\\u0016\\u0017" +
        "\\u0018\\u0019\\u001a\\u001b\\u001c\\u001d\\u001e\\u001f";

    /// <summary>Remplace tout caractère interdit (union multi-plateformes) par « _ ».</summary>
    public static string SanitizeFileName(string name)
    {
»       foreach (char c in InvalidFileNameChars)
            name = name.Replace(c, '_');
        return name.Trim();
    }""",
    "APRÈS — v3 · src/RoomEq.Core/Io/Stores.cs. L'union fixe remplace l'interrogation de "
    "l'hôte ; la rationale est documentée dans le code (séquences d'échappement restituées "
    "ici sous forme littérale pour la lisibilité)."))

story.append(Spacer(1, 6))
story.append(para(
    "Trois leçons se dégagent de ce petit comparatif, et elles valent pour le protocole "
    "entier. D'abord, la vérification doit s'exécuter dans l'environnement qui révèle le "
    "défaut : l'intégration continue de la démonstration teste sur trois OS précisément "
    "pour cela. Ensuite, un défaut de portabilité est un défaut de contrat — le contrat "
    "implicite « un nom de fichier sanitizé est portable » n'était écrit nulle part ; il "
    "l'est désormais, dans la spec I du module et dans le code. Enfin, la taille du "
    "correctif est sans rapport avec sa portée : six lignes remplacées par quinze, mais un "
    "changement de classe — d'un comportement dépendant de l'hôte à une garantie "
    "multi-plateformes par construction."))

# ================================================================ CH 9
story += h1_block(
    "9. Résultats mesurés",
    para("La démonstration se juge sur des chiffres, pas sur des impressions. Le tableau "
         "ci-dessous confronte la base scellée et le recodage cristallisé sur les mêmes "
         "mesures — celles qui décrivent la structure du code, sa défense et sa "
         "gouvernance. Le volume de code est volontairement resté comparable : le recodage "
         "n'a pas gonflé l'application, il a déplacé l'effort vers la spécification et la "
         "vérification.", "lead"))

story += table_block("", make_table(
    ["Mesure", "Base scellée v2.2.2", "Recodage v3.0.0-dev.1"],
    [
        ["Fichiers C# (src/)", "82", "93"],
        ["Lignes de code (src/)", "14 891", "15 438"],
        ["Lignes de tests", "4 032", "<b>5 963</b> (+48 %)"],
        ["Tests unitaires", "228", "<b>437</b> (+91 %)"],
        ["Plus gros fichier", "1 075 lignes (MixerViewModel)", "<b>497</b> lignes (ConsoleMixer, Audio)"],
        ["Plus gros ViewModel", "1 075 lignes", "<b>399</b> lignes (5 partiels)"],
        ["Avertissements de compilation", "tolérés", "<b>0</b> erreur <b>0</b> avertissement"],
        ["Spécifications d'intention", "0", "<b>44</b> specs I diffables"],
        ["Modules cartographiés", "0", "<b>42</b> verrouillés + 8 specs installateur"],
        ["Décisions journalisées", "aucune", "<b>D1 à D11</b> avec alternatives rejetées"],
    ],
    [0.38, 0.29, 0.33], font_small=True),
    "Tableau 8 — Confrontation des deux révisions sur les mesures structurelles, "
    "défensives et de gouvernance.")

story.append(para(
    "La suite de tests mérite le détail, car elle est le cœur de la vérification. Les 228 "
    "tests de la base scellée ont été portés intégralement — c'était l'oracle — puis "
    "étendus : la couche Core passe de 150 à 220 tests, la couche Audio de 78 à 142, et "
    "une suite App de 75 tests apparaît, rendue possible par la décomposition des "
    "ViewModels et les interfaces étroites du comparatif 8.2. Chaque extension attaque une "
    "faiblesse de la base : parité des données embarquées, replis de la politique de "
    "presets, comportements aux limites du pont ASIO, inertie plateforme des moteurs "
    "d'entrées-sorties."))

story += table_block("", make_table(
    ["Suite", "v2.2.2", "v3", "Nature des extensions"],
    [
        ["RoomEq.Core.Tests", "150", "<b>220</b>", "parité casques, comportements aux limites, "
         "diagnostics injectables"],
        ["RoomEq.Audio.Tests", "78", "<b>142</b>", "providers, MasterBus, anti-larsen vérifiable "
         "sous Linux, rognage exact"],
        ["RoomEq.App.Tests", "aucun", "<b>75</b>", "ViewModels décomposés, politique preset↔sortie "
         "sans périphérique"],
        ["<b>Total</b>", "<b>228</b>", "<b>437</b>", "portage intégral + extensions ciblées"],
    ],
    [0.26, 0.12, 0.12, 0.50], font_small=True),
    "Tableau 9 — Décomposition de la suite de tests : l'oracle porté intégralement, puis "
    "étendu là où la base était aveugle.")

story.append(para(
    "La non-régression se démontre famille par famille : les quatorze familles de "
    "fonctionnalités du README de la base scellée — de l'égaliseur paramétrique à la "
    "télémétrie de test — ont été auditées point par point, avec pour chacune les modules "
    "correspondants, la méthode de vérification et le verdict. Les données embarquées sont "
    "contrôlées par empreintes cryptographiques, reproductibles par quiconque exécute la "
    "commande de hachage sur les deux dépôts :"))

story += table_block("", make_table(
    ["Donnée embarquée", "Contenu", "Empreinte md5 (v2.2.2 = v3)"],
    [
        ["headphone_presets.json", "corrections casques AutoEq — 321 modèles, 58 marques",
         "ffff00a5fa1078986f523cb9aa3a9563"],
        ["MicLibrary.json", "profils de mesure micro — 36 entrées",
         "f126f6f5892daff7d7ec13edaeaaedcc"],
    ],
    [0.24, 0.36, 0.40], font_small=True, mono_cols=(2,)),
    "Tableau 11 — Empreintes des données embarquées après le comblement D9 : la "
    "bibliothèque casques (321 modèles) et les profils micro (36) sont identiques octet "
    "pour octet à la base scellée.")

story += table_block("", make_table(
    ["Volet audité", "Verdict"],
    [
        ["Fonctionnalités applicatives (14 familles du README)", "parité intégrale — 14/14"],
        ["Données embarquées (casques 321, micros 36)", "empreintes identiques après "
         "comblement D9"],
        ["Jeux de tests", "portage intégral + extensions (437 vs 228)"],
        ["Natifs (pilote, ASIO, installateurs)", "scellés v2.2.2, consommés tels quels (D1)"],
        ["Écarts volontaires", "3, tous documentés (voir ci-dessous)"],
    ],
    [0.55, 0.45]),
    "Tableau 12 — Synthèse de l'audit de parité (docs/PARITE-v2.2.2.md du dépôt de "
    "démonstration).")

story.append(para(
    "Trois écarts volontaires subsistent, et leur existence même est une propriété du "
    "protocole : aucun n'est silencieux. Le premier est le seuil de détection du "
    "comparatif 8.1 — un défaut connu corrigé par décision journalisée plutôt que "
    "perpétué au nom d'une parité stricte. Le deuxième regroupe les améliorations v3 "
    "consignées vague par vague : préampli appliqué dans la chaîne EQ, fichier de la "
    "tranche Lecteur restauré au démarrage, message ASIO sans pilote, garde-fou étendu au "
    "preset plat — des correctifs de bogues de la base, chacun couvert par un test. Le "
    "troisième est structurel : ViewModels décomposés, classes dupliquées fusionnées, "
    "interfaces étroites — sans changement de comportement observable. La règle de "
    "gouvernance est respectée à la lettre : ce qui change est écrit, justifié et daté."))

story.append(callout(
    "42 modules · 437 tests · 14/14 familles · 0 avertissement",
    "La cristallisation v3.0.0-dev.1 en une ligne — chiffres reproduits par la commande "
    "de vérification du dépôt, pas déclarés"))

# ================================================================ CH 10
story += h1_block(
    "10. Les reverse-specs : le contrat avant le code",
    para("La démonstration s'est prolongée au-delà du recodage par une extension inédite, "
         "née de l'analyse des incidents d'installation qui ont marqué l'histoire de "
         "RoomEq. Les versions v2.2.0 à v2.2.2 se sont succédé pour corriger trois défauts "
         "d'installateur ; l'analyse des journaux et des commits révèle qu'ils partagent "
         "tous la même classe : des contrats non écrits, dupliqués en plusieurs "
         "exemplaires dans le code.", "lead"))

story += table_block("", make_table(
    ["Défaut historique", "Symptôme", "Verrou posé par la spec I"],
    [
        ["Structure Win32 déclarée de mémoire — SP_DEVINFO_DATA de 424 octets au lieu de "
         "32 sur x64", "échec 0x6F8 à l'installation du pilote (2 copies du défaut)",
         "M-INS-02 : invariant Marshal.SizeOf == 32, testé ; contrat complet "
         "SetupAPI/newdev/cfgmgr32"],
        ["Signature INF erronée — $Windows NT$ au lieu de $CHICAGO$", "échec 0xE0000205, "
         "pilote refusé par Windows",
         "M-INS-03 : validateur bloquant au build ET à l'installation"],
        ["Parsing de pnputil sur libellés localisés français", "échec silencieux du "
         "détecteur d'origine (3 copies du défaut)",
         "M-INS-04 : fragments publi/orig indépendants des libellés, décodage CP850, "
         "repli par scan ; fixtures partagées avec l'application"],
    ],
    [0.34, 0.30, 0.36], font_small=True),
    "Tableau 13 — Les trois défauts historiques de l'installateur et les verrous posés par "
    "les reverse-specs (décision D11 du dépôt de démonstration).")

story.append(para(
    "La réponse du protocole est contre-intuitive et mérite d'être exposée : plutôt que de "
    "recoder l'installateur — ce qui ajouterait un chantier non validé à un chantier en "
    "attente de validation —, la démonstration a écrit les <b>specs I de l'installateur "
    "scellé</b> : huit modules M-INS-01 à 08 rédigés par rétro-ingénierie du code source "
    "v2.2.2 relu ligne à ligne. Le binaire reste la référence exploitable ; le contrat, "
    "lui, devient diffable, versionné et testable. La règle R2 — l'intention d'abord — "
    "s'applique ici à l'envers du temps : le contrat précède même la décision de recoder."))

story.append(para(
    "Cette extension a une seconde vertu, cruciale pour un projet mené par agents : elle "
    "fige la connaissance. Les specs dérivent du code relu, pas d'une mémoire de session ; "
    "les conditions qui ont permis aux trois défauts de survivre trois versions — "
    "contrats implicites, duplication, parsing sur libellés — sont désormais éliminées par "
    "construction, puisque les fixtures de parsing sont partagées contractuellement entre "
    "l'installateur futur et l'application recodée. Si la vague 8 est un jour lancée, elle "
    "partira de contrats déjà testés ; si elle ne l'est jamais, le comportement validé "
    "reste spécifié pour quiconque viendra après."))

# ================================================================ CH 11
story += h1_block(
    "11. Ce que la démonstration établit",
    para("Un protocole se juge à ce qu'il rend impossible. Sur les trois comparatifs du "
         "chapitre 8 comme sur l'extension du chapitre 10, la démonstration établit que "
         "la classe de défauts « contrat non écrit » — nombre magique, structure déclarée "
         "de mémoire, comportement dépendant de l'hôte, parsing sur libellés — est "
         "systématiquement convertie en contrat nommé, documenté, testé et journalisé.",
         "lead"))

story.append(para(
    "Les résultats vont au-delà de l'anecdote. Les règles ont opéré sans exception sur un "
    "périmètre réel et complet : 42 modules cartographiés, 44 specs écrites avant le code, "
    "dix commits tous précédés de la vérification complète, sept vagues closes par une "
    "sauvegarde systématique. L'oracle a joué son rôle jusque dans la révélation de "
    "défauts invisibles sur la machine de développement. La parité est démontrable par "
    "des tiers — empreintes reproductibles, quatorze familles auditées, écarts "
    "documentés. Et la structure s'est améliorée sans growthisme : à volume de code "
    "comparable, la défense double et le plus gros fichier applicatif passe de 1 075 à "
    "399 lignes."))

story.append(para(
    "La démonstration valide aussi, indirectement, la gouvernance du protocole. Le "
    "journal des décisions du dépôt — onze décisions en cinq sessions, chacune avec ses "
    "alternatives rejetées — a servi de mémoire d'arbitrage effectivement consultée : "
    "aucune révision silencieuse, aucun accommodement improvisé, y compris sous la "
    "pression d'une réinitialisation d'environnement en cours de projet. La redondance "
    "des sauvegardes a été éprouvée en conditions réelles, et la restauration complète "
    "n'a coûté aucune perte de travail. L'anti-enfermement n'est pas théorique : "
    "l'historique, les contrats et l'état sont récupérables par un agent neuf depuis les "
    "seuls artefacts du dépôt."))

story += h2_block("11.1 Ce que la démonstration ne prouve pas", para(
    "L'honnêteté impose la contrepartie. La démonstration valide la <b>méthode</b> du "
    "protocole — la discipline des couches, les règles, la boucle, la vérification, la "
    "gouvernance — sur du code source applicatif ; elle ne valide pas le <b>cœur machine</b> "
    "de la spécification : la notation, l'oracle différentiel par propriétés, le verrou "
    "croisé cryptographique, le patch à chaud et les adresses stables restent à démontrer "
    "par les jalons M0 à M7, sur le profil primaire puis par portabilité inter-OS et "
    "inter-ISA. De même, la cristallisation v3.0.0-dev.1 demeure une pré-version : la "
    "validation utilisateur sur machine Windows réelle — l'installation du pilote scellé, "
    "la mesure d'une pièce, l'écoute — est l'étape d'ouverture que les tests ne peuvent "
    "pas remplacer. La démonstration a précisément été conçue pour ne pas confondre ces "
    "niveaux de preuve."))

story.append(para(
    "Enfin, la démonstration renvoie au protocole trois enseignements concrets, que la "
    "prochaine révision pourra instruire : la notion de pré-version de cristallisation "
    "(-dev.N), qui distingue « vérifié par l'oracle » de « validé sur le terrain » ; la "
    "pratique des reverse-specs, qui étend la couche I aux binaires scellés hérités — "
    "situations que la spécification n'avait pas prévues ; et la valeur du partage de "
    "fixtures entre consommateurs d'un même contrat externe, qui élimine par "
    "construction la duplication qui laisse vivre les défauts."))

# ================================================================ CH 12
story += h1_block(
    "12. Feuille de route",
    para("La démonstration étant cristallisée, les étapes suivantes sont d'ores et déjà "
         "délimitées par les décisions du dépôt et la feuille de route du protocole — "
         "chacune avec ses conditions de lancement explicites, dans l'esprit de la "
         "gouvernance TRIADE.", "lead"))

story += table_block("", make_table(
    ["Étape", "Contenu", "Condition"],
    [
        ["Validation Windows", "Checklist de l'audit de parité sur machine réelle : "
         "installation du pilote scellé v2.2.2, mesure, écoute, comportements clés",
         "machine Windows 11 physique"],
        ["Ouverture v3.0.0", "Retrait du suffixe -dev.1, tag final, livrables définitifs",
         "validation Windows effectuée"],
        ["Vague 8 — installateur", "Recodage éventuel depuis les 8 specs M-INS prêtes",
         "validation v3 + décision de signature (certificat EV / attestation) + "
         "environnement Windows pour R5"],
        ["Jalon M0 — protocole", "Chaîne notation → octets → PE32+ → exécution Windows 11, "
         "exécutable de moins de 4 Kio, carte v0 signée", "départ de la phase de "
         "réalisation du protocole"],
        ["Jalon M2 — patch à chaud", "Remplacement d'un bloc en cours d'exécution, sans "
         "interruption, avec rollback démontré", "M0-M1 franchis"],
        ["Jalons M6-M7 — universalité", "Portabilité inter-OS (Linux) puis inter-ISA "
         "(RISC-V), à contrat I constant", "M0-M5 franchis"],
    ],
    [0.20, 0.48, 0.32], font_small=True),
    "Tableau 14 — Les étapes ouvertes : démonstration RoomEq d'un côté, réalisation du "
    "protocole de l'autre.")

story.append(para(
    "Le fil conducteur reste celui du chapitre premier : développer avec un agent exige "
    "de l'agent qu'il prouve ce qu'il affirme, et du projet qu'il survive à l'agent. La "
    "démonstration RoomEq montre que les mécanismes du protocole — couches, règles, "
    "boucle, vérification, gouvernance — tiennent ces deux promesses à l'échelle d'une "
    "application réelle complète. Le prochain rendez-vous de vérité est le jalon M0, "
    "où la même discipline devra tenir sur l'artefact même du protocole : des octets "
    "écrits à la main, vérifiés par l'oracle, scellés par la carte."))

# ================================================================ BUILD
# Build en deux phases : le pied de page est dessiné en DÉBUT de page, or le
# marqueur de début de corps ne connaît sa page définitive qu'en fin de passe
# (la TOC peut grossir entre les passes de multiBuild). Phase 1 : convergence
# vers la valeur stable. Phase 2 : reconstruction avec la valeur gelée.
import copy  # noqa: E402

story_pass1 = copy.deepcopy(story)
doc1 = TocDocTemplate(
    BODY_PDF + ".pass1.pdf", pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
)
doc1.multiBuild(story_pass1, onFirstPage=on_page, onLaterPages=on_page)
frozen_body_start = BODY_START[0]
print("phase 1 OK, body_start =", frozen_body_start)

BODY_START[0] = frozen_body_start  # valeur gelee pour toute la phase 2
BODY_FROZEN[0] = True               # interdit toute mise a jour en cours de passe
doc = TocDocTemplate(
    BODY_PDF, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
    title=DOC_TITLE, author="Z.ai", creator="Z.ai",
    subject=DOC_SUBJECT,
)
doc.multiBuild(story, onFirstPage=on_page, onLaterPages=on_page)
print("body OK ->", BODY_PDF)
if os.path.exists(BODY_PDF + ".pass1.pdf"):
    os.remove(BODY_PDF + ".pass1.pdf")

# ------------------------------------------------ fusion couverture
from pypdf import PdfReader, PdfWriter  # noqa: E402

A4_W, A4_H = 595.28, 841.89


def normalize_page_to_a4(page):
    box = page.mediabox
    w, h = float(box.width), float(box.height)
    if abs(w - A4_W) > 0.5 or abs(h - A4_H) > 0.5:
        page.scale_to(A4_W, A4_H)
    return page


writer = PdfWriter()
writer.add_page(normalize_page_to_a4(PdfReader(COVER_PDF).pages[0]))
for page in PdfReader(BODY_PDF).pages:
    writer.add_page(normalize_page_to_a4(page))
writer.add_metadata({
    "/Title": DOC_TITLE,
    "/Author": "Z.ai",
    "/Creator": "Z.ai",
    "/Subject": DOC_SUBJECT,
})
os.makedirs(os.path.dirname(FINAL_PDF), exist_ok=True)
with open(FINAL_PDF, "wb") as f:
    writer.write(f)
print("final OK ->", FINAL_PDF)

# Copie livrable dans download/ si le répertoire existe (espace de travail)
if os.path.isdir(DOWNLOAD_DIR):
    import shutil
    shutil.copy2(FINAL_PDF, os.path.join(
        DOWNLOAD_DIR, "Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf"))
    print("copie livrable ->", os.path.join(
        DOWNLOAD_DIR, "Protocole_TRIADE_v0.3_Demonstration_RoomEq.pdf"))
