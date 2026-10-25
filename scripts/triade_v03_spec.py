#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corps du PDF — Protocole TRIADE v0.3, spécification du développement logiciel
en code machine natif par agent IA. Route Report (ReportLab), TOC auto, fusion
couverture. Régénération systématique via triade/scripts/build_pdf.sh (D17).

Sources faisant autorité : triade/docs/PROTOCOLE_TRIADE.md (v0.3),
FORMAT_CARTE.md, DECISIONS.md (D1-D16), PLAN_MILESTONES.md (M0-M7).
Le script vit dans le dépôt (triade/scripts/) ; tous les chemins dérivent de
TRIADE_BASE (défaut /home/z/my-project), ce qui le rend insensible à sa propre
localisation et restaurable sur un poste neuf.
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
BODY_PDF = os.path.join(REPO, "scripts", "triade_v03_body.pdf")
COVER_PDF = os.path.join(REPO, "scripts", "triade_v03_cover.pdf")
FINAL_PDF = os.path.join(REPO, "docs", "Protocole_TRIADE_v0.3_Specification.pdf")
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
# Cascade palette (design_engine.py palette-cascade --intent cold --mode minimal --seed 7)
# Identique à la v0.2 : continuité visuelle de la série documentaire.
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

DOC_TITLE = "Protocole TRIADE v0.3 — Spécification du développement logiciel en code machine natif par agent IA"
DOC_SUBJECT = ("Spécification du protocole TRIADE v0.3 : code machine natif par agent IA, "
               "couches I/B/C, profils de cible, suite cryptographique paramétrable, "
               "export de continuité")

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
    canvas.drawString(MARGIN, PAGE_H - 40, "PROTOCOLE TRIADE v0.3 — SPÉCIFICATION TECHNIQUE")
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, PAGE_H - 46, PAGE_W - MARGIN, PAGE_H - 46)
    # --- pied de page : filet + auteur + numero de page zone
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 40, PAGE_W - MARGIN, 40)
    canvas.setFont("FreeSerif", 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, 28, "TRIADE · spécification technique v0.3 · 25 octobre 2026")
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
    """Bloc de code : fond carte + filet accent à gauche."""
    nbsp = chr(160)
    lines = txt.rstrip("\n").split("\n")
    html_lines = []
    for ln in lines:
        stripped = ln.lstrip(" ")
        pad = len(ln) - len(stripped)
        html_lines.append(nbsp * pad + esc(stripped) if stripped else nbsp)
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
    "1. Vision et objectifs",
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
    "disparaît du pipeline de production : il n'existe plus aucune couche de traduction entre "
    "ce que l'agent écrit et les octets exécutés. Ce que l'agent écrit est ce qui s'exécute — "
    "et rien d'autre."))

story.append(para(
    "Le nom encode l'architecture : trois couches indissociables — <b>Intention</b> (I), "
    "<b>Binaire</b> (B), <b>Carte</b> (C) — unies par un verrou croisé cryptographique. La "
    "couche I contient le <i>quoi</i> et le <i>pourquoi</i> : contrats typés, pré et "
    "post-conditions, invariants. La couche B contient le <i>comment</i> : des octets scellés, "
    "versionnés, à adresses stables. La couche C — la formalisation du système de balises "
    "décrit au départ du projet — est l'index naviguable qui lie les deux et sert d'unique "
    "interface de développement à l'agent. La v0.3 étend cette architecture d'une seconde "
    "dimension : la cible d'exécution, traitée par profils instanciables plutôt que par une "
    "exception codée en dur."))

story += h2_block("1.1 Fonction objectif hiérarchisée", callout(
    "Sécurité > Performance > Optimisation > Coût en tokens",
    "Arbitrage lexicographique : un objectif n'est jamais sacrifié au profit d'un objectif "
    "de rang inférieur"))

story.append(para(
    "Toutes les décisions de cette spécification dérivent d'une fonction objectif ordonnée "
    "lexicographiquement, fournie par les objectifs du projet. La <b>sécurité</b> domine : un "
    "artefact plus rapide mais moins sûr est rejeté en amont. La <b>performance</b> suit "
    "immédiatement : l'artefact livré est du code machine sans couche d'exécution "
    "intermédiaire, ni machine virtuelle, ni runtime. L'<b>optimisation</b> vient ensuite : "
    "la descente à l'ISA sur les chemins critiques se fait par profilage, jamais à l'aveugle. "
    "Le <b>coût en tokens</b> n'est optimisé qu'à contrainte égale sur les trois premiers "
    "objectifs — typiquement par la compacité de la carte et le chargement paresseux, jamais "
    "en rognant la vérification."))

story += table_block("", make_table(
    ["Objectif", "Signification concrète", "Métrique de validation"],
    [
        ["<b>Sécurité</b>", "Sûreté mémoire validée par oracle, intégrité carte ↔ binaire, "
         "durcissement au chargement", "0 corruption détectée par l'oracle ; tout échec de "
         "verrou bloque la session"],
        ["<b>Performance</b>", "100 % code machine natif, zéro abstraction intermédiaire "
         "entre l'écriture et l'exécution", "Comparaison par bloc scellé face à une référence "
         "compilée (clang -O2 ou équivalent du profil)"],
        ["<b>Optimisation</b>", "Descente à l'ISA sur les hot paths identifiés par profilage",
         "Gain mesuré et journalisé pour chaque bloc optimisé"],
        ["<b>Coût en tokens</b>", "Édition ciblée via la carte, jamais de lecture intégrale "
         "du binaire", "Budgets par type d'édition (chapitre 9)"],
    ],
    [0.17, 0.44, 0.39]),
    "Tableau 1 — Les quatre objectifs et leurs métriques de validation associées.")

story += h2_block("1.2 Périmètre et non-objectifs", para(
    "Cette spécification couvre le format de la carte, les règles du protocole, la boucle de "
    "mise à jour, la stratégie de vérification, le modèle de menace et la feuille de route "
    "M0-M7. Trois non-objectifs doivent être posés d'emblée pour éviter tout malentendu "
    "d'usage. Premièrement, TRIADE ne prétend pas remplacer les langages dans l'industrie : "
    "c'est une architecture de laboratoire, conçue pour être validée sur une application "
    "réelle complète. Deuxièmement, la furtivité face aux EDR n'est pas recherchée : l'outil "
    "cible est un utilitaire de pentest destiné à des tests autorisés en environnement de "
    "laboratoire, et les API du système sont appelées via les interfaces standards du profil. "
    "Troisièmement, l'universalité revendiquée par la v0.3 est structurelle mais progressive : "
    "chaque profil de cible doit être instancié et validé (jalons M6 et M7) avant d'être "
    "déclaré supporté — le protocole ne promet pas la portabilité, il la vérifie."))

# ================================================================ CH 2
story += h1_block(
    "2. Journal des décisions (D1-D16)",
    para("Chaque décision structurante est consignée avec ses alternatives rejetées et sa "
         "justification rattachée à la fonction objectif — le journal complet figure dans "
         "<i>docs/DECISIONS.md</i> (D1-D10 issues de la v0.2 ; D11-D13 issues de "
         "l'infrastructure de sauvegarde ; D14-D16 issues de la v0.3, dont deux amendent des "
         "décisions antérieures). Ce journal est la mémoire des arbitrages : toute révision "
         "future du protocole doit soit respecter ces décisions, soit expliciter précisément "
         "ce qui les invalide. Cette discipline évite la dérive progressive qui transforme un "
         "protocole propre en accumulation d'exceptions incohérentes."))

story += table_block("", make_table(
    ["ID", "Décision", "Choix retenu", "Alternatives rejetées"],
    [
        ["D1", "Oracle de vérification", "Éphémère et obligatoire : régénéré à chaque session "
         "depuis la couche I, détruit après usage", "Oracle persistant versionné ; aucun "
         "oracle (confiance aveugle)"],
        ["D2", "Notation", "keystone (assemblage) + capstone (round-trip), in-process, "
         "granularité instruction", "nasm -f bin ; écriture directe des octets à la main"],
        ["D3", "Couche I", "Contrats légers : signatures typées, pré/post-conditions, "
         "invariants", "Spécification formelle lourde (TLA+, Alloy)"],
        ["D4", "Crypto de la carte", "Ed25519 (signature) + XChaCha20-Poly1305 (repos) + "
         "Argon2id (dérivation)", "AES-GCM ; clés dérivées par SHA-256 nu"],
        ["D5", "Verrou croisé", "SHA-256 par bloc scellé + carte signée en entier, vérifiés "
         "avant chaque édition et au chargement", "Signature du seul binaire"],
        ["D6", "Empreintes par build", "Variante unique par livraison : réordonnancement, "
         "nops, encodages équivalents", "Binaire identique pour tous les destinataires"],
        ["D7", "Appels système", "API Windows via IAT (kernel32, ws2_32, Schannel)",
         "Syscalls directs avec table par build de Windows"],
        ["D8", "Granularité des blocs", "32 à 512 instructions, un bloc = une "
         "responsabilité, padding de 16 octets ; budgets 40/200 tokens", "Micro-blocs (1-8 "
         "instructions) ; méga-blocs (plusieurs milliers)"],
        ["D9", "TLS", "Schannel (SSPI) au jalon M4", "TLS 1.3 pur implémenté en blocs "
         "scellés (reporté en objectif post-M5)"],
        ["D10", "Cible", "x86-64, Windows 11, PE32+ écrit à la main, DEP/ASLR/CFG respectés "
         "— profil primaire depuis D14", "RISC-V sous QEMU ; x86-64 Linux"],
        ["D11", "Architecture de sauvegarde", "Git local (source de vérité) + Google Drive "
         "(miroir lisible + bundle d'historique) + GitHub privé", "Dépôt Drive seul ; repo "
         "GitHub seul ; copie brute du répertoire .git"],
        ["D12", "Gestion des jetons", "Confinés dans .gdrive/ (permissions 600, exclus du "
         "dépôt et des synchronisations)", "Jetons commités ; variables d'environnement "
         "persistées"],
        ["D13", "Sauvegarde systématique", "sync_backup.sh après chaque modification + hook "
         "post-commit (synchro Drive à chaque commit)", "Sauvegardes manuelles ponctuelles ; "
         "synchronisation par lot en fin de session"],
        ["D14", "Universalité", "Profils de cible à sept éléments obligatoires ; le cœur du "
         "protocole est indépendant de la cible (amende D10)", "Cibles multiples codées en "
         "dur ; couche d'abstraction portable ; mono-cible"],
        ["D15", "Suite cryptographique", "Paramétrable dans des listes blanches, consignée "
         "dans l'en-tête signé de la carte ; empreintes préfixées ; re-cryptage atomique "
         "(amende D5)", "Suite figée ; liberté totale sans seuil (affaiblissement possible)"],
        ["D16", "Récupération de la carte", "Export de continuité chiffré et signé "
         "(I+B+C+manifeste autodescriptif), import en cinq étapes, oracle jamais exporté "
         "(précise R1)", "Carte non exportable (enfermement) ; export en clair ; export non "
         "signé"],
    ],
    [0.055, 0.155, 0.42, 0.37], font_small=True),
    "Tableau 2 — Journal des seize décisions structurantes (D11-D13 : infrastructure ; "
    "D14-D16 : v0.3).")

story.append(para(
    "Cinq décisions engagent l'architecture entière. <b>D1</b> : l'oracle éphémère est le "
    "pivot du compromis entre le « 100 % code machine » exigé pour l'artefact et la sûreté "
    "d'exécution. L'implémentation de référence — triviale, lente, écrite dans un langage "
    "sûr — ne sort jamais du laboratoire : elle est régénérée à chaque session puis "
    "détruite. Elle ne dégrade donc ni la performance ni la pureté de l'artefact livré, "
    "tout en attrapant les corruptions mémoire avant le scellage. Sur le plan du coût en "
    "tokens, elle est également rentable : régénérer un oracle trivial coûte moins cher que "
    "de traquer une corruption silencieuse dans un binaire déjà scellé."))

story.append(para(
    "<b>D2</b> : keystone et capstone forment le couple d'assemblage et de désassemblage de "
    "référence — depuis la v0.3, le moteur de notation est désigné par chaque profil de "
    "cible. La nuance capitale est que cette notation n'est pas un compilateur : aucune "
    "optimisation, aucune décision de réécriture ne s'intercale entre ce que l'agent écrit "
    "et les octets produits. Le principe WYSIWYG — ce que vous écrivez est ce qui s'exécute "
    "— est préservé intégralement, et l'artefact demeure le couple octets + carte."))

story.append(para(
    "<b>D5</b>, amendé par <b>D15</b> : le verrou croisé répond à la menace spécifique de "
    "l'empoisonnement de carte — un attaquant qui falsifierait les métadonnées ferait "
    "travailler l'agent sur des informations fausses, et pourrait lui faire introduire une "
    "porte dérobée en croyant respecter les contrats. La contre-mesure est bilatérale : la "
    "carte porte l'empreinte de chaque bloc scellé, et la carte entière est signée. Depuis "
    "la v0.3, les algorithmes deviennent des choix consignés dans l'en-tête signé de la "
    "carte, dans les limites d'une liste blanche : la volonté du développeur s'exerce entre "
    "algorithmes conformes au seuil de sécurité, jamais contre lui. <b>D7</b> enfin : les "
    "syscalls directs exigeraient une table de numéros par build de Windows — une carte "
    "cachée supplémentaire, fragile — pour un gain relevant de la furtivité, hors du "
    "périmètre."))

story.append(para(
    "<b>D14</b> : l'universalité est réalisée par des profils de cible vérifiables, et non "
    "par une couche d'abstraction logicielle. Un bytecode portable ou une machine virtuelle "
    "réintroduirait précisément la couche d'exécution intermédiaire que le protocole existe "
    "pour supprimer — un reniement de la fonction objectif Performance. Exiger sept éléments "
    "par profil rend l'extension vérifiable plutôt que déclarative : un profil incomplet est "
    "refusé, exactement comme un build sans carte. D16, dernière décision de la v0.3, fait "
    "l'objet du paragraphe 8.4 : l'export de continuité rétablit l'équilibre entre "
    "l'interdiction de livrer la carte et la propriété par le développeur de son état de "
    "travail."))

# ================================================================ CH 3
story += h1_block(
    "3. Architecture TRIADE",
    para("L'architecture repose sur une séparation stricte entre ce que l'artefact contient, "
         "ce que l'agent manipule et ce que le destinataire reçoit. La figure 1 montre les "
         "trois couches et leurs liaisons : le diff d'intention descend de I vers C, le "
         "verrou croisé relie C et B dans les deux sens, et la couche B seule quitte le "
         "laboratoire. Aucune couche n'est optionnelle : privé de I, le système perd son "
         "ancrage sémantique ; privé de C, l'agent devient aveugle ; privé de B, il n'y a "
         "plus rien à exécuter."))

story += figure(os.path.join(ASSETS, "diagram_arch.png"),
                "Figure 1 — Les trois couches du protocole TRIADE et leurs liaisons : diff "
                "d'intention (I vers C), verrou croisé par empreintes signées (C vers B). "
                "Seule la couche B est livrée.", 322)

story += h2_block("3.1 Les trois couches", make_table(
    ["Couche", "Contenu", "Visibilité", "Rôle"],
    [
        ["<b>I</b>", "Spécifications, contrats typés pré/post, invariants logiques",
         "Privée", "Compression de l'intention — le quoi et le pourquoi"],
        ["<b>C</b>", "Index des blocs, adresses, signatures, preuves, manifestes de build",
         "Privée, signée, chiffrée", "Unique interface de développement de l'agent"],
        ["<b>B</b>", "Code machine scellé, padding inter-blocs, checksums runtime",
         "Livrée", "Le comment — exécution pure, sémantiquement muette"],
    ],
    [0.09, 0.37, 0.20, 0.34]),
    "Tableau 3 — Contenu, visibilité et rôle de chaque couche.")

story.append(para(
    "Depuis la v0.3, la séparation des couches croise une seconde dimension : la cible. La "
    "couche I est <b>indépendante de la cible</b> — un contrat s'écrit une fois, ses types "
    "abstraits (<i>usize</i>, alignements) étant paramétrés par le profil. La couche B est "
    "<b>par profil</b> : chaque plateforme visée possède son jeu d'octets scellés. La couche "
    "C indexe l'ensemble : chaque entrée porte son profil, et frag-bld organise les "
    "empreintes par profil. Un même contrat I est ainsi instancié par autant de blocs "
    "machine que de profils supportés — c'est la condition de possibilité de la portabilité "
    "sans duplication de l'intention."))

story.append(para(
    "Le flux de travail découle directement de cette séparation. Pour toute évolution, "
    "l'agent produit d'abord un diff sur la couche I — on modifie le <i>quoi</i> avant le "
    "<i>comment</i>. Il localise ensuite les blocs concernés au travers de la carte, sans "
    "jamais scanner le binaire. Il régénère les seuls blocs impactés — pour le ou les "
    "profils visés —, les fait vérifier par l'oracle, puis commite l'ensemble de façon "
    "atomique : patch du binaire, mise à jour de la carte et scellage ne font qu'un."))

story += h2_block("3.2 Invariants structurels", para(
    "Quatre invariants non négociables structurent le système et sont vérifiés à chaque "
    "cycle de build. Leur violation n'est pas une erreur de conception parmi d'autres : "
    "c'est un refus de build, car chacun protège une propriété dont dépendent toutes les "
    "autres règles."))
story += bullets([
    "<b>B n'est jamais nu</b> (R1) : tout binaire est accompagné d'une carte à jour et "
    "signée, sous peine de perdre toute maintenabilité.",
    "<b>Les adresses exposées sont stables</b> (R7, par profil) : les points d'entrée des "
    "blocs scellés sont garantis par padding ; aucun patch ne déplace jamais du code "
    "existant au sein du binaire d'un profil.",
    "<b>La signature couvre la carte entière</b> (R9) : en-tête et fragments sont signés "
    "ensemble — une carte partielle ou contrefaite est rejetée avant la moindre opération.",
    "<b>B est auto-vérifiant au chargement</b> (R10) : le binaire contrôle ses checksums "
    "avant de s'exécuter et s'arrête proprement en cas d'écart (fail-closed).",
])

# ================================================================ CH 4
story += h1_block(
    "4. La carte : spécification (couche C)",
    para("La carte est le cœur opérationnel du protocole : c'est elle qui rend le binaire "
         "navigable pour l'agent, qui porte les preuves et qui concentre la valeur "
         "intellectuelle du projet. Sa conception obéit à quatre contraintes tirées de la "
         "fonction objectif : elle doit être compacte (coût en tokens), intègre (verrou "
         "croisé), résiliente face à la compromission (sharding et chiffrement) et, depuis "
         "la v0.3, autodescriptive — la carte porte elle-même sa version, sa suite "
         "cryptographique et ses profils actifs, de sorte qu'aucun agent n'ait besoin de "
         "connaissance extérieure pour la vérifier. Chacune de ces contraintes se traduit "
         "par un mécanisme précis, spécifié dans ce chapitre."))

story += h2_block("4.1 Fragments et sharding", make_table(
    ["Fragment", "Contenu", "Raison d'être de la séparation"],
    [
        ["<b>frag-loc</b>", "Identifiants, profils, adresses, tailles, états, dépendances",
         "Localisation : le plus lu, le moins sensible — peut être chargé seul"],
        ["<b>frag-con</b>", "Signatures, pré/post-conditions, invariants, conventions "
         "d'appel", "Contrats : diffés à chaque changement (R2), lus à chaque édition"],
        ["<b>frag-prf</b>", "Vecteurs dorés hachés, compteurs de cristallisation, seuils",
         "Preuves : volumineux, rarement lu en entier après cristallisation"],
        ["<b>frag-bld</b>", "Empreintes des blocs par profil, manifestes de build, registre "
         "des variantes", "Verrou croisé et traçage (D5, D6) — ne quitte jamais le poste "
         "de développement"],
    ],
    [0.13, 0.44, 0.43]),
    "Tableau 4 — Les quatre fragments de la carte et leur justification.")

story.append(Spacer(1, 2))
story.append(callout_note(
    "<b>Quatre fragments chiffrés séparément.</b> Chaque fragment est chiffré avec sa "
    "propre clé dérivée de la clé maîtresse — AEAD selon l'algorithme de l'en-tête, "
    "XChaCha20-Poly1305 par défaut, nonce aléatoire de 192 bits. Un compromis partiel "
    "— la fuite d'un fragment isolé — n'est jamais une perte totale : les contrats sans "
    "les adresses, ou les preuves sans les contrats, ne reconstituent pas la carte."))

story.append(para(
    "Le chiffrement au repos et la signature sont précisés par la décision D4, rendue "
    "paramétrable par D15 : XChaCha20-Poly1305 pour le chiffrement, Argon2id pour la "
    "dérivation de la clé maîtresse depuis la phrase secrète (mémoire au moins 64 Mio, au "
    "moins 3 itérations), et Ed25519 pour la signature de l'ensemble. La signature est "
    "calculée sur le concaténé des empreintes de chaque fragment — en-tête compris —, ce "
    "qui lie indissociablement leur ensemble : toute substitution d'un seul fragment "
    "invalide la signature globale."))

story += h2_block("4.2 En-tête normalisé et suite cryptographique", para(
    "L'en-tête est la première section de la carte, signée avec les fragments dont il fait "
    "partie intégrante. Sa syntaxe est identique au format d'entrée — ASCII, ligne par "
    "ligne — et il consigne les trois paramètres de la suite cryptographique ainsi que la "
    "liste des profils actifs du projet :"))

story.append(code_block(
    "[carte] version=0.3\n"
    "  algo_hachage     : sha256\n"
    "  algo_signature   : ed25519\n"
    "  algo_chiffrement : xchacha20poly1305\n"
    "  profils          : x86-64-win11-pe, x86-64-linux-elf64\n"
    "  empreinte_racine : sha256:9f3c...e21a",
    "En-tête normalisé de la carte — valeurs par défaut de la v0.3."))

story += table_block("", make_table(
    ["Champ", "Signification"],
    [
        ["<b>version</b>", "Version du protocole à laquelle la carte est conforme"],
        ["<b>algo_hachage</b>", "Algorithme des empreintes de blocs et de la racine — "
         "liste blanche D15, SHA-256 par défaut"],
        ["<b>algo_signature</b>", "Algorithme de signature de la carte — liste blanche "
         "D15, Ed25519 par défaut"],
        ["<b>algo_chiffrement</b>", "Algorithme AEAD du chiffrement des fragments — liste "
         "blanche D15, XChaCha20-Poly1305 par défaut"],
        ["<b>profils</b>", "Liste des profils de cible actifs, identifiants "
         "<i><isa>-<os>-<format></i>"],
        ["<b>empreinte_racine</b>", "Empreinte de l'ensemble des fragments, au format "
         "préfixé"],
    ],
    [0.22, 0.78]),
    "Tableau 5 — Champs de l'en-tête normalisé de la carte.")

story.append(para(
    "Deux propriétés découlent de cet en-tête. D'une part, tout agent vérifie le verrou "
    "croisé <b>avec l'algorithme de l'en-tête</b>, jamais avec un algorithme supposé : "
    "c'est la condition de l'autodescription. D'autre part, les empreintes portées par "
    "frag-bld sont toutes au format préfixé — <i>sha256:ab12…</i> — si bien qu'une "
    "migration cryptographique future reste lisible par les outils présents. Un agent "
    "d'aujourd'hui peut ainsi vérifier une carte générée par un agent de demain, et "
    "réciproquement : la carte ne dépend d'aucune connaissance extérieure à elle-même."))

story += h2_block("4.3 Format d'entrée de bloc", para(
    "Chaque bloc est décrit par une entrée dont la syntaxe est volontairement ASCII et "
    "ligne-par-ligne : la tokenisation est non ambiguë, le diff est lisible, et aucun "
    "caractère Unicode exotique ne peut corrompre l'encodage en transit. L'exemple "
    "ci-dessous est l'entrée complète du bloc de référence utilisé tout au long de la "
    "spécification — notons le champ <i>cible</i>, ajouté par la v0.3, qui porte le profil "
    "d'instanciation du bloc."))

story.append(code_block(
    "[bloc] id=b7f3a9 cible=x86-64-win11-pe addr=0x4012A0 size=212 v=4 etat=scelle\n"
    "  sig     : (ptr u8, usize) -> usize\n"
    "  pre     : ptr != 0 && len <= MAX_LEN\n"
    "  post    : ret <= len\n"
    "  regs    : rbx, r12-r15 sauvegardes ; conv: msx64\n"
    "  inv     : r8 aligne 16 dans la boucle\n"
    "  deps    : [a31c2 memcpy] [ext AVX2]\n"
    "  preuves : memsafe:ok bornes:ok term:ok\n"
    "  tests   : 12400 cas ; ref=oracle_v9 ; crist=10/10",
    "Entrée complète — budget maximal : 200 tokens (D8)."))

story.append(para(
    "Les champs se répartissent en deux ensembles. La première ligne — identifiant, "
    "profil, adresse, taille, version, état — constitue à elle seule l'entrée de "
    "localisation portée par frag-loc : c'est la seule partie que l'agent lit pour situer "
    "un bloc, et son budget est de 40 tokens maximum. Les lignes suivantes (signature, "
    "pré/post-conditions, registres préservés, invariants, dépendances, preuves, tests) "
    "forment l'entrée détaillée portée par frag-con et frag-prf : elles ne sont chargées "
    "que lorsque le bloc est effectivement édité. Le champ <i>regs</i> porte la convention "
    "d'appel effective du profil — msx64, sysv, lp64r — si bien que l'agent sait, pour "
    "chaque bloc, quelle convention appliquer sans la déduire du contexte."))

story += h2_block("4.4 Verrou croisé : procédure", para(
    "Le verrou croisé est la procédure d'intégrité exécutée avant chaque édition et avant "
    "chaque chargement. Avant toute opération d'écriture, l'agent exécute la séquence "
    "suivante, et tout échec interrompt la session — jamais de contournement, jamais de "
    "reprise forcée."))
story += bullets([
    "<b>Étape 1.</b> Vérifier la signature de la carte — avec <i>algo_signature</i> de "
    "l'en-tête — sur l'ensemble en-tête et fragments ; une carte non signée ou à "
    "signature invalide est refusée (R9).",
    "<b>Étape 2.</b> Recalculer l'empreinte de chaque bloc scellé visé par l'édition — "
    "avec <i>algo_hachage</i> de l'en-tête — ainsi que de l'ensemble de ses dépendances "
    "directes.",
    "<b>Étape 3.</b> Comparer les empreintes obtenues à celles portées par frag-bld, au "
    "format préfixé ; tout écart signifie que binaire et carte ont divergé.",
    "<b>Étape 4.</b> En cas d'écart : blocage de la session, journal de l'incident, état "
    "conservé pour audit — la reprise passe obligatoirement par une réconciliation "
    "manuelle documentée.",
])
story.append(para(
    "Au chargement — côté exécution cette fois — le binaire vérifie ses propres "
    "checksums avant d'entrer dans sa boucle principale : chaque bloc scellé porte une "
    "empreinte vérifiable, et un écart déclenche un arrêt propre plutôt qu'une exécution "
    "de code potentiellement altéré (R10). La protection est donc bilatérale : la carte "
    "authentifie le binaire pendant le développement, et le binaire s'authentifie lui-même "
    "en production. Falsifier l'un des deux côtés sans détection exige de compromettre "
    "simultanément la clé de signature et le binaire livré."))

story += h2_block("4.5 Cycle de vie d'une entrée", make_table(
    ["État", "Signification", "Transition"],
    [
        ["<b>brouillon</b>", "Bloc en cours d'écriture, non vérifié, non adressé",
         "Création par l'agent ; adresse provisoire"],
        ["<b>vérifié</b>", "Oracle passé une fois, round-trip conforme",
         "Après une session de vérification complète (R5)"],
        ["<b>scellé</b>", "Commité : adresse stable, empreinte dans frag-bld",
         "Commit atomique (étape 6 de la boucle)"],
        ["<b>cristallisé</b>", "Immuable : dix vérifications réussies consécutives",
         "Seuil atteint (R6) ; modification = procédure lourde"],
        ["<b>déprécié</b>", "Remplacé par une version plus récente",
         "Conservé pour l'audit et le traçage des variantes"],
    ],
    [0.15, 0.44, 0.41]),
    "Tableau 6 — Cycle de vie d'une entrée de la carte.")

story.append(para(
    "La cristallisation est le mécanisme d'économie structurelle du protocole : un bloc "
    "cristallisé n'est plus jamais rechargé ni re-vérifié en session — seule son empreinte "
    "est contrôlée, ce qui coûte une comparaison de chaîne courte. La modification d'un "
    "bloc cristallisé reste possible mais relève d'une procédure délibérément lourde : "
    "justification sur la couche I, double vérification par oracle, et création d'un "
    "nouveau bloc plutôt qu'une réécriture — l'ancien passant à l'état déprécié. Cette "
    "asymétrie de coût est volontaire : elle rend l'évolution des blocs mûrs rare et "
    "réfléchie, exactement comme un noyau de système d'exploitation protège ses parties "
    "les plus éprouvées."))

# ================================================================ CH 5
story += h1_block(
    "5. Règles du protocole v0.3",
    para("Les règles constituent le noyau normatif du protocole : elles sont peu "
         "nombreuses, vérifiables mécaniquement et sanctionnées par des effets concrets "
         "— refus de build, refus de commit ou blocage de session — plutôt que par des "
         "recommandations. Les règles R1 à R7 proviennent de la v0.1 ; les règles R8 à "
         "R10 sont les ajouts de la v0.2, consacrés à l'intégrité de la chaîne carte "
         "vers binaire. La v0.3 n'ajoute aucune règle : elle précise deux d'entre elles "
         "— preuve que le noyau normatif était déjà universel — et s'appuie sur les "
         "décisions D14 à D16 pour les mécanismes."))

story += table_block("", make_table(
    ["Règle", "Énoncé", "Violation et sanction"],
    [
        ["<b>R1</b> Jamais de binaire nu", "Tout artefact B est accompagné de I et C à jour",
         "Build refusé"],
        ["<b>R2</b> Intention d'abord", "Toute modification commence par un diff sur I",
         "Édition rejetée par la boucle"],
        ["<b>R3</b> Balisage obligatoire", "Chaque bloc est décrit dans C",
         "Build refusé"],
        ["<b>R4</b> Patch à contrat stable", "Le remplacement préserve signature et "
         "contrats ; les appelants ne sont jamais invalidés", "Échec de vérification"],
        ["<b>R5</b> Vérifie-puis-écrit", "Aucun commit sans oracle, vecteurs dorés et "
         "round-trip", "Commit impossible"],
        ["<b>R6</b> Cristallisation", "Dix vérifications réussies rendent le bloc "
         "immuable ; le modifier exige la procédure lourde", "Nouvelle version du bloc"],
        ["<b>R7</b> Adresses stables", "Les points d'entrée sont garantis par padding ; "
         "patcher ne déplace rien", "Re-liage forcé — interdit"],
        ["<b>R8</b> Verrou croisé", "Empreintes des blocs et signature de la carte vérifiés "
         "avant chaque édition", "Session bloquée"],
        ["<b>R9</b> Carte signée obligatoire", "L'agent refuse toute carte non signée",
         "Refus de démarrage"],
        ["<b>R10</b> Fail-closed au chargement", "Checksums vérifiés au lancement ; "
         "écart = arrêt propre", "Arrêt de l'exécution"],
    ],
    [0.24, 0.48, 0.28]),
    "Tableau 7 — Les dix règles du protocole et leurs sanctions.")

story.append(para(
    "Trois points appellent une précision. D'abord, R4 ne signifie pas qu'un bloc ne peut "
    "jamais changer de comportement : elle signifie qu'un bloc remplaçant honore les "
    "contrats publiés de son prédécesseur — mêmes signatures, mêmes pré et post-"
    "conditions, mêmes invariants visibles. Les appelants scellés contre l'ancienne "
    "version restent donc valides sans re-liage, ce qui est la condition de possibilité "
    "du patch à chaud du chapitre 6. Ensuite, R7 s'entend <b>par profil</b> : les adresses "
    "sont stables au sein du binaire de chaque profil ; rien n'impose qu'elles coïncident "
    "entre profils. Enfin, R1, précisée par D16, interdit de livrer la carte <b>avec "
    "l'artefact</b> ou à des tiers — elle n'interdit pas au développeur de détenir, "
    "sauvegarder et transférer son propre état de développement : c'est précisément "
    "l'objet de l'export de continuité (paragraphe 8.4)."))

# ================================================================ CH 6
story += h1_block(
    "6. Boucle de mise à jour",
    para("La boucle de mise à jour est le battement de cœur du protocole : c'est la "
         "seule voie par laquelle le logiciel évolue. Elle se déroule en sept étapes "
         "réparties en deux phases — l'édition, puis la validation et le commit — "
         "séparées par un point de non-retour : rien n'est écrit dans le binaire avant "
         "que l'oracle n'ait rendu son verdict. La figure 2 en donne la vue d'ensemble, "
         "le tableau 8 en précise les entrées et sorties."))

story += figure(os.path.join(ASSETS, "diagram_loop.png"),
                "Figure 2 — La boucle de mise à jour en sept étapes. Le point de non-"
                "retour se situe à l'étape 5 : un échec de l'oracle déclenche le "
                "rollback copy-on-write et la carte reste intacte.", 300)

story += table_block("", make_table(
    ["N", "Étape", "Entrées", "Sorties", "Règles"],
    [
        ["1", "Diff d'intention", "Requête de changement, couche I", "Diff minimal sur I",
         "R2"],
        ["2", "Localisation", "frag-loc", "Liste des blocs impactés", "R3"],
        ["3", "Verrou croisé", "frag-bld, binaire", "Verdict go / no-go", "R8, R9"],
        ["4", "Régénération ciblée", "frag-con, notation du bloc", "Octets candidats",
         "R4, R7"],
        ["5", "Vérification", "Candidats, oracle, vecteurs dorés", "Verdict, journal",
         "R5"],
        ["6", "Commit atomique", "Verdict favorable", "Patch B, carte à jour, scellage",
         "R1"],
        ["7", "Cristallisation", "Compteur de vérifications", "Bloc immuable", "R6"],
    ],
    [0.05, 0.21, 0.30, 0.29, 0.15]),
    "Tableau 8 — Entrées, sorties et règles associées à chaque étape de la boucle.")

story += h2_block("6.1 Patch à chaud — instanciation du profil primaire", callout(
    "12 à 16 octets",
    "Taille d'un trampoline de bascule atomique sur x86-64 — la plus petite unité de "
    "patch à chaud du profil primaire"))

story.append(para(
    "Le patch à chaud — modifier un logiciel en cours d'exécution — est l'un des deux "
    "objectifs fondateurs du projet avec la performance. Depuis la v0.3, le mécanisme "
    "exact est <b>spécifié par chaque profil de cible</b> : taille minimale de bascule "
    "atomique et procédure d'invalidation du cache d'instructions. Ce paragraphe décrit "
    "l'instanciation du profil primaire x86-64 ; le paragraphe 10.4 esquisse les "
    "variantes des autres profils. La méthode contourne la cohérence du cache "
    "d'instructions et l'atomicité de la bascule en n'écrivant <b>jamais</b> un bloc "
    "pendant qu'il s'exécute. Le nouveau bloc est d'abord écrit dans une zone de "
    "croissance libre ; ensuite, et seulement ensuite, un trampoline de 12 à 16 octets — "
    "un saut relatif de 5 octets ou un couple chargement-saut absolu de 12 octets — est "
    "installé à l'ancien point d'entrée et basculé par une écriture alignée unique, "
    "atomique pour le processeur."))

story.append(code_block(
    "; trampoline de bascule atomique (aligne sur 16 octets)\n"
    "; forme courte : saut relatif 32 bits\n"
    "  E9 xx xx xx xx                ; jmp rel32  -> nouveau bloc\n"
    "; forme longue : saut absolu 64 bits\n"
    "  48 B8 xx xx xx xx xx xx xx xx ; mov rax, addr_new\n"
    "  FF E0                         ; jmp rax",
    "Deux formes de trampoline — le variant de build choisit (D6)."))

story.append(para(
    "L'ancien trampoline est conservé : le rollback copy-on-write de l'étape 5 consiste "
    "simplement à rebasculer vers lui, et la carte référence les deux versions tant que "
    "la nouvelle n'a pas atteint son seuil de cristallisation. Les adresses stables "
    "garantissent par ailleurs qu'aucun appelant ne référence l'intérieur d'un bloc : "
    "seuls les points d'entrée — promis par R7 — sont susceptibles d'être trampolinés, "
    "et la table de ces points est close et vérifiée par le verrou croisé. Le critère de "
    "sortie du jalon M2 est précisément ce scénario : remplacer le bloc d'écho d'un "
    "serveur TCP pendant qu'il traite des connexions, sans interruption de service et "
    "avec rollback démontré."))

# ================================================================ CH 7
story += h1_block(
    "7. Stratégie de vérification",
    para("Supprimer le compilateur, c'est perdre les filets de sécurité qu'il tendait "
         "gratuitement : vérification de types, initialisation, analyse de flot. La "
         "stratégie de vérification de TRIADE doit donc reconstruire une confiance "
         "équivalente — voire supérieure — sans réintroduire de couche de traduction "
         "dans l'artefact. Elle repose sur trois piliers : l'oracle éphémère pour la "
         "sûreté comportementale, le round-trip de notation pour la fidélité des octets, "
         "et la cristallisation pour l'économie de re-vérification."))

story += h2_block("7.1 L'oracle éphémère", para(
    "L'oracle est une implémentation de référence de chaque bloc — triviale, "
    "volontairement lente, écrite dans un langage sûr et dérivant directement de la "
    "couche I. Il est généré au début de chaque session de développement, utilisé pour "
    "des tests différentiels par propriétés, puis détruit à la fin de la session : il "
    "n'est jamais livré, jamais archivé dans la carte, et seuls ses vecteurs de test "
    "dorés — hachés — y survivent. Ce caractère éphémère n'est pas une contrainte de "
    "confort mais une décision de sécurité : il n'existe aucun artefact persistant à "
    "empoisonner, et la surface d'attaque de la chaîne de développement s'en trouve "
    "réduite d'autant."))

story.append(para(
    "Le protocole de test est différentiel : l'oracle et le bloc machine reçoivent des "
    "entrées aléatoires contraintes par les pré-conditions du contrat, et leurs sorties "
    "sont comparées octet par octet, de même que les invariants internes après chaque "
    "appel. Le volume de référence est de l'ordre de douze mille cas par bloc critique "
    "— l'ordre de grandeur validé lors de l'expérimentation v0.1. Trois propriétés "
    "rendent l'oracle fiable là où un jumeau de référence permanent faillirait : il "
    "dérive de l'intention (I) et non du binaire (B), il ne peut donc pas hériter d'un "
    "bug du code machine ; il est régénéré à chaque session, donc jamais en désaccord "
    "avec la version courante des contrats ; et son coût de régénération reste très "
    "inférieur au coût de diagnostic d'une corruption mémoire découverte après "
    "scellage. Depuis la v0.3, une quatrième propriété s'y ajoute : l'oracle étant "
    "dérivé de I — couche indépendante de la cible — le <b>même</b> oracle valide les "
    "blocs de tous les profils. La portabilité ne divise pas le coût de vérification, "
    "elle le mutualise."))

story += h2_block("7.2 Round-trip de notation", para(
    "Le second pilier est purement mécanique : chaque bloc assemblé par le moteur de "
    "notation du profil — keystone sur les profils x86-64 — est désassemblé par le "
    "vérificateur correspondant — capstone —, et les instructions obtenues sont "
    "comparées à la notation d'origine. Tout désaccord — une instruction, un opérande, "
    "une taille d'encodage — est un échec de build. Ce contrôle à coût quasi nul attrape "
    "la classe d'erreurs la plus insidieuse du développement en code machine : l'écart "
    "silencieux entre ce que l'agent croit avoir écrit et les octets réellement "
    "produits, qu'il s'agisse d'un encodage alternatif choisi par l'assembleur ou d'une "
    "coquille dans la notation."))

story += h2_block("7.3 Cristallisation et chaîne de confiance du scellage", para(
    "La chaîne de confiance du scellage résume le parcours d'une preuve, de sa production "
    "à son ancrage cryptographique :"))
story += bullets([
    "L'oracle rend un verdict sur le bloc candidat (tests différentiels par propriétés).",
    "Les vecteurs dorés de la session sont hachés et consignés dans frag-prf, avec le "
    "compteur de vérifications du bloc.",
    "L'empreinte du bloc scellé — algorithme de l'en-tête — est inscrite dans frag-bld : "
    "c'est la moitié binaire du verrou croisé.",
    "La carte complète est signée — algorithme de l'en-tête —, liant en-tête, fragments, "
    "preuves et empreintes en un seul acte de confiance.",
    "Au seuil de dix vérifications réussies, le bloc est cristallisé : son entrée devient "
    "immuable et son coût de re-contrôle tombe à une comparaison d'empreinte.",
])
story.append(para(
    "Cette chaîne garantit qu'à tout instant, la confiance accordée à un bloc est "
    "traçable jusqu'à des preuves datées et chiffrées — et que cette traçabilité "
    "elle-même est protégée par la signature de la carte. La cristallisation ferme la "
    "boucle économique : plus un bloc fait ses preuves, moins il coûte à vérifier, ce "
    "qui libère le budget de vérification pour les blocs jeunes et les zones actives "
    "de développement."))

# ================================================================ CH 8
story += h1_block(
    "8. Sécurité et anti-rétro-ingénierie",
    para("La question qui a motivé la v0.2 — détenir la cartographie uniquement côté "
         "développeur pour coder en binaire pur et freiner la rétro-ingénierie — reçoit "
         "ici sa réponse systématique. Le principe directeur est la séparation de deux "
         "budgets souvent confondus : l'<b>obfuscation</b>, qui protège la propriété "
         "intellectuelle (le <i>comment</i>), et le <b>durcissement</b>, qui protège "
         "l'exécution (le <i>où ça casse</i>). La carte privée relève du premier ; la "
         "sûreté mémoire, les contrats et le fuzzing relèvent du second. Conformément "
         "au principe de Kerckhoffs, la sécurité du système ne repose jamais sur le "
         "secret de la carte : elle survivrait à sa divulgation."))

story += h2_block("8.1 Modèle de menace", make_table(
    ["Menace", "Acteur", "Cible", "Contre-mesure", "Résiduel"],
    [
        ["Rétro-ingénierie de l'IP", "Concurrent, pirate", "Binaire livré",
         "Carte privée ; binaire sémantiquement muet ; variantes par build",
         "Temps acheté — s'érode avec les LLM de décompilation"],
        ["Empoisonnement de carte", "Attaquant supply-chain", "Fragments",
         "Signature (algo de l'en-tête) ; refus de carte non signée ; verrou croisé",
         "Détecté — session bloquée (fail-closed)"],
        ["Fuite de la carte", "Initié, poste compromis", "Fragments au repos",
         "Chiffrement (algo de l'en-tête) ; sharding ; escrow",
         "Perte partielle limitée à un fragment"],
        ["Vol de l'export de continuité", "Voleur, stockage cloud compromis",
         "Conteneur exporté", "Chiffrement intégral (phrase maîtresse + Argon2id) ; "
         "signature", "Sans la phrase, indéchiffrable — aucune donnée en clair"],
        ["Fuzzing boîte noire", "Attaquant externe", "Runtime",
         "Contrats, oracle, tests par propriétés, fail-closed",
         "Indépendant du secret de la carte"],
        ["Redistribution frauduleuse", "Pirate", "Binaire livré",
         "Empreintes par build — canary trap",
         "Fuite traçable à son destinataire"],
        ["Instrumentation dynamique", "Analyste", "Exécution",
         "Anti-debug léger par mesure de temps (rdtsc)",
         "Assumé — l'obscurité n'est pas la sécurité"],
    ],
    [0.17, 0.14, 0.14, 0.32, 0.23], font_small=True),
    "Tableau 9 — Modèle de menace : acteur, cible, contre-mesure et risque résiduel.")

story.append(para(
    "Deux lectures de ce tableau méritent d'être explicitées. La rétro-ingénierie est "
    "traitée comme un objectif d'économie, pas d'impossibilité : rendre le coût de "
    "l'analyse supérieur à la valeur de ce qu'on obtient. Un binaire strippé, sans "
    "structure ni symboles, dont chaque exemplaire diffère, coûte sensiblement plus cher "
    "à analyser qu'un binaire compilé standard — mais les modèles de langage appliqués "
    "à la décompilation progressent, et l'avantage doit être réévalué à chaque "
    "génération de modèles. La ligne « vol de l'export de continuité », ajoutée par la "
    "v0.3, étend le modèle au nouveau conteneur : son risque résiduel est nul sans la "
    "phrase maîtresse, précisément parce que l'export est chiffré intégralement avant "
    "de quitter le poste — aucun métadonnée, aucun index, aucune donnée en clair."))

story += h2_block("8.2 Empreintes par build", para(
    "Puisque la régénération du code machine est quasi gratuite dans ce paradigme, "
    "chaque livraison peut porter une variante unique sans coût marginal : "
    "réordonnancement des blocs scellés indépendants, insertion de nops multioctets, "
    "choix parmi les encodages équivalents que l'ISA offre pour une même instruction. "
    "Le registre des variantes est conservé dans frag-bld, côté développeur, "
    "<b>par profil</b> : chaque plateforme visée possède ses propres variantes, et "
    "toute fuite d'un binaire d'un profil donné devient traçable jusqu'à son "
    "destinataire — le canary trap classique, appliqué ici au code machine où il est "
    "structurellement plus facile à mettre en œuvre que dans un pipeline de "
    "compilation classique."))

story.append(code_block(
    "; deux encodages equivalents de la meme instruction\n"
    "  89 C0      ; mov eax, eax  (forme : rm <- r)\n"
    "  8B C0      ; mov eax, eax  (forme : r <- rm)\n"
    "; ni le sens ni les effets ne changent - seule la signature binaire change",
    "Exemple de variante d'encodage sélectionnable par build (D6)."))

story += h2_block("8.3 Suite cryptographique paramétrable et gestion des clés", para(
    "Depuis la v0.3, la suite cryptographique est <b>paramétrable par le développeur</b> "
    "(D15) : l'en-tête de la carte consigne les trois algorithmes retenus, chacun choisi "
    "dans une liste blanche. La liberté s'exerce entre algorithmes atteignant le seuil de "
    "sécurité du protocole — au moins 128 bits de sécurité et résistance à la collision "
    "pour le hachage ; signatures déterministes ou protégées par randomisation "
    "<i>hedged</i> pour la signature ; chiffrement authentifié (AEAD) uniquement. Tout "
    "algorithme sous le seuil — MD5, SHA-1 — est refusé au chargement de la carte : la "
    "volonté du développeur s'exerce entre algorithmes conformes, jamais contre la "
    "fonction objectif. L'ajout d'un algorithme à la liste blanche relève de la "
    "gouvernance du protocole, jamais d'un choix local de projet."))

story += table_block("", make_table(
    ["Paramètre", "Défaut", "Liste blanche (D15)"],
    [
        ["<b>algo_hachage</b>", "sha256",
         "sha256, sha384, sha512, sha3-256, sha3-512, blake2b-256, blake2b-512, blake3"],
        ["<b>algo_signature</b>", "ed25519",
         "ed25519, ed448, ecdsa-p256-rfc6979, ecdsa-p384-rfc6979"],
        ["<b>algo_chiffrement</b>", "xchacha20poly1305",
         "xchacha20poly1305, chacha20poly1305, aes-256-gcm"],
    ],
    [0.21, 0.17, 0.62], font_small=True, mono_cols=(1, 2)),
    "Tableau 10 — Les trois paramètres cryptographiques, leurs défauts et leurs listes "
    "blanches.")

story.append(para(
    "Les motivations typiques d'un changement sont la conformité réglementaire (FIPS "
    "140-3, CNSA), la résistance anticipée (migration vers SHA-3 ou BLAKE3) ou la "
    "performance (BLAKE3 sur les très gros blocs). Le changement en cours de projet est "
    "une migration complète, atomique et journalisée — le <b>re-cryptage</b> : "
    "justification consignée au journal des décisions, recalcul de toutes les empreintes "
    "des blocs scellés et réécriture de frag-bld au format préfixé, re-chiffrement des "
    "quatre fragments avec les nouvelles clés dérivées, re-signature complète de la "
    "carte et régénération de l'empreinte racine, archivage de l'ancienne carte — "
    "dépréciée, jamais détruite en silence — puis production immédiate d'un nouvel "
    "export de continuité. L'opération réussit entièrement ou laisse l'ancienne carte en "
    "place ; la première édition qui suit un re-cryptage vérifie l'intégralité des "
    "empreintes, pas seulement les blocs visés."))

story.append(para(
    "La dérivation de clés, elle, n'est pas paramétrable : ses paramètres de coût sont "
    "des planchers. La phrase secrète maîtresse traverse Argon2id — mémoire d'au moins "
    "64 Mio, au moins trois itérations, parallélisme unitaire — pour produire la clé "
    "maîtresse ; les clés de chaque fragment en sont dérivées par HKDF avec un contexte "
    "distinct par fragment et par génération. Les sauvegardes suivent la règle 3-2-1 "
    "chiffrée, et l'escrow de la clé maîtresse peut recourir à un partage de secret "
    "deux-sur-trois pour éliminer le point de défaillance unique qu'une phrase secrète "
    "unique constituerait. La rotation des clés entraîne une re-signature complète de "
    "la carte — opération atomique, journalisée, vérifiable après coup par la chaîne "
    "de confiance du scellage décrite au chapitre 7."))

story += h2_block("8.4 Export de continuité", para(
    "La règle R1 interdit de livrer la carte avec l'artefact ; elle n'interdit pas au "
    "développeur de détenir et transférer son propre état de développement. Sans "
    "mécanisme de récupération, l'interdiction créerait un enfermement : le projet ne "
    "survivrait ni au changement d'agent, ni au changement de poste. La v0.3 formalise "
    "donc l'<b>export de continuité</b> (D16) : un conteneur unique, chiffré "
    "intégralement et signé, regroupant les couches I, B et C complètes ainsi qu'un "
    "manifeste autodescriptif — version du protocole, suite cryptographique, profils "
    "actifs, empreinte racine, date et liste des contrôles effectués à l'export. "
    "Chiffré, l'export peut être stocké n'importe où — y compris un stockage cloud — "
    "sans exposer la carte, ce qui satisfait la règle 3-2-1 ; signé, il est vérifiable "
    "à l'import ; autodescriptif, il ne requiert aucune connaissance extérieure à "
    "lui-même."))

story.append(para(
    "L'oracle est volontairement exclu du conteneur : éphémère par conception (D1), il "
    "est régénéré depuis I à l'arrivée — l'export n'embarque ainsi aucun artefact "
    "empoisonnable persistant, et sa surface d'attaque s'en trouve réduite d'autant. "
    "La procédure d'import, exécutée par tout agent conforme TRIADE sur un poste ou un "
    "agent nouveau, comporte cinq étapes :"))
story += bullets([
    "<b>1. Déchiffrement</b> du conteneur par la phrase maîtresse — escrow deux-sur-"
    "trois si le contexte est organisationnel ; un échec de déchiffrement est "
    "terminal, rien n'est interprété.",
    "<b>2. Vérification de la signature</b> du conteneur et de la carte qu'il "
    "contient — un export non signé ou à signature invalide est refusé (R9), sans "
    "exception, même si son contenu paraît sain.",
    "<b>3. Vérification du verrou croisé</b> : recalcul des empreintes de B avec "
    "l'algorithme de l'en-tête, comparaison à frag-bld ; tout écart bloque la "
    "reprise (R8).",
    "<b>4. Régénération de l'oracle</b> depuis la couche I — l'oracle n'est jamais "
    "importé.",
    "<b>5. Reprise normale</b> : la boucle de mise à jour s'applique à l'identique.",
])
story.append(para(
    "Cette procédure garantit l'anti-enfermement : le développeur peut changer d'agent, "
    "de poste ou de fournisseur à tout moment, sans perte et sans dépendance envers "
    "l'agent qui l'a précédé. Elle garantit aussi la traçabilité : le manifeste "
    "conserve la date, la suite cryptographique et les contrôles de l'export, ce qui "
    "l'inscrit dans la chaîne de confiance du scellage. Le statut de l'interdiction de "
    "livraison s'en trouve clarifié : la carte, la couche I et les vecteurs de test ne "
    "sont jamais livrés avec l'artefact ni communiqués à des tiers ; l'export de "
    "continuité est l'unique exception — réservée au développeur, exclusivement sous "
    "forme chiffrée et signée. Un export en clair est une violation du protocole."))

# ================================================================ CH 9
story += h1_block(
    "9. Optimisation du coût en tokens",
    para("Le coût en tokens est le seul des quatre objectifs qui soit spécifique à "
         "l'ère agent-first : il n'existait pas dans l'économie du développement humain. "
         "Dans TRIADE, il est traité comme une contrainte d'ingénierie à part entière — "
         "avec des budgets, des mécanismes et une instrumentation — mais toujours "
         "subordonnée aux trois objectifs supérieurs : aucune économie de tokens ne "
         "justifie de sauter une vérification."))

story.append(callout("40 / 200", "tokens — budget par entrée de localisation (frag-loc) / "
                                "par entrée complète de bloc (D8)"))
story.append(Spacer(1, 8))

story.append(para(
    "Le principe directeur tient en une phrase : <b>l'agent ne lit jamais le binaire en "
    "entier</b>. La carte est son unique index, et elle est conçue pour être lue "
    "parcellairement. Trois mécanismes rendent cette lecture parcimonieuse effective : "
    "la compacité du format d'entrée (syntaxe ASCII, abréviations stables, budgets par "
    "champ) ; le chargement paresseux par fragment, où frag-loc seul suffit à situer un "
    "bloc ; et la cristallisation, qui exempte de tout rechargement les blocs parvenus "
    "à maturité. Le tableau 11 fixe les budgets par type d'opération — y compris "
    "l'instanciation d'un profil nouveau, ajoutée par la v0.3."))

story += table_block("", make_table(
    ["Opération", "Fragments et données lus", "Budget"],
    [
        ["Localiser un bloc", "frag-loc — une entrée", "40 tokens max"],
        ["Éditer simplement un bloc", "frag-loc + frag-con du bloc + notation du bloc",
         "3 000 tokens max"],
        ["Ajouter un bloc (profil existant)", "frag-loc + frag-con + notation",
         "6 000 tokens max"],
        ["Instancier un profil nouveau", "I partagée + frag-con + notation du profil",
         "6 000 tokens max par bloc"],
        ["Audit complet (rare)", "Carte entière déchiffrée",
         "Non budgété — opération exceptionnelle"],
    ],
    [0.30, 0.44, 0.26]),
    "Tableau 11 — Budgets en tokens par type d'opération d'édition.")

story.append(para(
    "Pour situer ces ordres de grandeur : dans un pipeline classique, une modification "
    "modeste commence typiquement par relire le module source complet et son contexte "
    "— plusieurs dizaines de milliers de tokens — avant même d'écrire. Le budget TRIADE "
    "pour la même opération est borné à quelques milliers, parce que la localisation "
    "remplace la relecture. L'instrumentation obligatoire mesure le coût réel de chaque "
    "opération d'édition et alimente les indicateurs de santé du protocole : précision "
    "de localisation (le bon bloc identifié du premier coup, cible 95 % au jalon M0), "
    "coût moyen d'une édition simple (cible 5 000 tokens), et taux de régression "
    "post-patch (cible zéro, rollback exclu). Le multi-profils n'altère pas ces "
    "budgets : l'entrée de localisation porte le profil, l'édition d'un bloc pour un "
    "profil existant relève du budget « édition », et l'instanciation d'un contrat sur "
    "un profil nouveau relève du budget « ajout » — la couche I, elle, n'est jamais "
    "dupliquée."))

# ================================================================ CH 10
story += h1_block(
    "10. Profils de cible — universalité",
    para("La v0.2 fixait une cible unique — x86-64 / Windows 11 / PE32+ — et renvoyait "
         "la portabilité à un objectif post-M5. La v0.3 généralise : le cœur du "
         "protocole — couches, règles, boucle, vérification — est indépendant de la "
         "cible par construction, et tout ce qui dépend de la cible est regroupé dans "
         "un <b>profil de cible</b>. L'universalité devient une propriété "
         "structurelle : instancier une plateforme nouvelle revient à écrire un "
         "profil, jamais à modifier le protocole."))

story.append(para(
    "Un profil définit obligatoirement sept éléments, qui font de l'extension une "
    "opération vérifiable plutôt que déclarative : (1) l'ISA et la largeur de ses "
    "types — <i>usize</i>, alignements, boutisme ; (2) l'ABI d'appel — registres de "
    "passage, volatilité, shadow space ou zone rouge ; (3) le format d'exécutable et "
    "les protections à honorer — DEP/NX, ASLR/PIE, CFI/CFG ; (4) l'interface système "
    "autorisée — IAT, syscalls, libc de la cible ; (5) le mécanisme de patch à chaud "
    "natif — taille minimale de bascule atomique et procédure d'invalidation du cache "
    "d'instructions ; (6) le moteur de notation et son vérificateur de round-trip ; "
    "(7) la granularité des blocs et le padding garantissant les adresses stables "
    "(R7). Un profil incomplet est refusé, exactement comme un build sans carte."))

story += table_block("", make_table(
    ["Profil", "ISA", "OS", "Format", "Interface", "Statut"],
    [
        ["x86-64-win11-pe", "x86-64", "Windows 11", "PE32+",
         "IAT (kernel32, ws2_32, Schannel)", "Primaire — jalons M0-M5"],
        ["x86-64-linux-elf64", "x86-64", "Linux", "ELF64", "syscalls + libc",
         "M6 — portabilité inter-OS"],
        ["riscv64-linux-elf64", "RISC-V 64", "Linux", "ELF64", "syscalls + libc",
         "M7 — portabilité inter-ISA"],
        ["aarch64-macos-macho", "AArch64", "macOS", "Mach-O", "libSystem",
         "Réservé — hors feuille de route"],
        ["wasm32-wasi", "WebAssembly", "WASI", "module Wasm", "WASI",
         "Réservé — étude de niche"],
    ],
    [0.205, 0.10, 0.115, 0.09, 0.27, 0.22], font_small=True, mono_cols=(0,)),
    "Tableau 12 — Les profils de cible : identifiant, instanciation et statut de "
    "validation.")

story.append(para(
    "L'identifiant d'un profil suit la convention <i><isa>-<os>-<"
    "format></i>. La correspondance des couches est la suivante : la couche I est "
    "partagée par tous les profils du projet ; chaque entrée de la carte porte son "
    "profil ; chaque profil possède son binaire, ses empreintes de build et son "
    "registre de variantes dans frag-bld. « Sans compilateur » ne signifie pas « sans "
    "système d'exploitation » — les interfaces sont appelées selon les conventions du "
    "profil, comme tout binaire natif légitime. Les deux sections suivantes détaillent "
    "le profil primaire ; la section 10.4 met en regard les trois profils de la "
    "feuille de route."))

story += h2_block("10.1 Profil primaire : ABI Microsoft x64", make_table(
    ["Convention", "Règle"],
    [
        ["Passation des arguments", "RCX, RDX, R8, R9, puis la pile — de droite à gauche"],
        ["Valeur de retour", "RAX (RDX pour une valeur de 128 bits)"],
        ["Shadow space", "32 octets réservés par l'appelant avant chaque CALL"],
        ["Registres volatils", "RAX, RCX, RDX, R8 à R11 — détruits par l'appelé"],
        ["Registres non volatils", "RBX, RBP, RDI, RSI, R12 à R15 — préservés par "
         "l'appelé"],
        ["Registres flottants", "XMM0 à XMM5 volatils, XMM6 à XMM15 préservés"],
        ["Alignement de pile", "RSP multiple de 16 au point d'appel"],
        ["Zone rouge", "<b>Aucune</b> — contrairement à System V : stocker sous RSP "
         "sans allocation préalable est interdit"],
    ],
    [0.26, 0.74]),
    "Tableau 13 — Règles essentielles de l'ABI Microsoft x64 (profil primaire).")

story.append(para(
    "L'absence de zone rouge est le piège classique pour qui vient de System V : sur "
    "Linux, une fonction feuille peut stocker des données sous RSP sans décrémenter la "
    "pile ; sur Windows, cette zone appartient au système et toute interruption "
    "l'écrase. La convention interne du projet en tire les conséquences : R10 et R11 "
    "sont désignés registres de travail internes — ils sont volatils selon l'ABI, donc "
    "jamais promis à un appelant ; aucune donnée vivante ne séjourne entre RSP et "
    "RSP+32 au moment d'un appel, zone occupée par le shadow space ; et tout bloc qui "
    "appelle une API alloue son cadre avant d'y toucher. Ces règles internes sont "
    "portées par frag-con pour chaque bloc concerné."))

story += h2_block("10.2 Format PE32+ minimal", para(
    "L'exécutable est écrit à la main par l'agent, sans outil de liaison : c'est la "
    "preuve de maîtrise du pipeline artefact exigée au jalon M0. La structure minimale "
    "comprend l'en-tête DOS et son stub, la signature PE, l'en-tête COFF (machine "
    "0x8664, quatre sections au maximum), l'en-tête optionnel PE32+ (magic 0x20B, "
    "alignement de section 0x1000, caractéristiques DYNAMICBASE, HIGH_ENTROPY_VA et "
    "NX_COMPAT activées), la section .text en lecture-exécution, la section .rdata "
    "portant les imports et les relocations, la table d'imports et la table .reloc qui "
    "rend l'ASLR possible. L'objectif de taille pour M0 est un exécutable de moins de "
    "quatre Kio — l'ordre de grandeur d'un binaire minimal, loin des dizaines de Kio "
    "qu'imposent les environnements d'exécution."))

story += h2_block("10.3 Appels via IAT et protections du système", para(
    "Les dépendances système du profil primaire se limitent à trois ensembles : "
    "kernel32 pour les entrées-sorties, les threads et le tas ; ws2_32 pour le réseau "
    "à partir du jalon M2 ; et Schannel via SSPI pour TLS au jalon M4. Les adresses ne "
    "sont jamais codées en dur : chaque appel transite par la table d'imports, résolue "
    "par le chargeur — ce qui préserve la compatibilité entre builds de Windows et "
    "respecte l'ASLR. Les protections du système sont honorées par construction : DEP, "
    "puisque aucun code n'est jamais généré en pile ; ASLR, grâce aux relocations ; et "
    "Control Flow Guard, par la déclaration des cibles d'appel indirect valides. "
    "L'objectif est assumé : un outil légitime par construction, dont la transparence "
    "vis-à-vis du système est totale."))

story += h2_block("10.4 Différences entre profils — aperçu", make_table(
    ["Élément", "x86-64-win11-pe (primaire)", "x86-64-linux-elf64 (M6)",
     "riscv64-linux-elf64 (M7)"],
    [
        ["ABI", "msx64 : RCX RDX R8 R9 ; shadow space 32 o.",
         "SysV : RDI RSI RDX RCX R8 R9 ; zone rouge 128 o.", "psABI : a0-a7"],
        ["Format", "PE32+ : DYNAMICBASE, HIGH_ENTROPY_VA, NX",
         "ELF64 : PIE, RELRO, NX", "ELF64 : PIE, RELRO, NX"],
        ["Interface", "IAT : kernel32, ws2_32, Schannel", "syscalls + libc",
         "syscalls + libc"],
        ["Patch à chaud", "trampoline 5/12 o., écriture alignée atomique",
         "identique x86-64", "taille fixe : registre scratch + fence.i"],
        ["Notation", "keystone / capstone x86-64", "keystone / capstone x86-64",
         "keystone / capstone RISC-V"],
    ],
    [0.13, 0.31, 0.29, 0.27], font_small=True),
    "Tableau 14 — Mise en regard des trois profils de la feuille de route.")

story.append(para(
    "Deux transitions méritent une vigilance documentée. Le passage Windows vers Linux "
    "<b>inverse</b> le piège de la zone rouge : ce qui était interdit sur msx64 "
    "(stocker sous RSP) redevient permis sur SysV pour une fonction feuille — l'agent "
    "doit désapprendre le réflexe acquis sur le profil primaire, et frag-con porte la "
    "convention effective de chaque bloc. Le passage x86-64 vers RISC-V change la "
    "nature du patch à chaud : sur une ISA à instructions de taille fixe, il n'existe "
    "pas de trampoline relatif de 5 octets insérable n'importe où ; la bascule passe "
    "par un registre scratch chargé de l'adresse cible, suivi d'une barrière "
    "d'invalidation du cache d'instructions — <i>fence.i</i> — et le profil spécifie "
    "la séquence exacte et son atomicité."))

# ================================================================ CH 11
story += h1_block(
    "11. Feuille de route M0-M7",
    para("La feuille de route décompose la validation du protocole en huit jalons, "
         "chacun couvrant une capacité nouvelle et se terminant par des critères de "
         "sortie mesurables — le détail figure dans <i>docs/PLAN_MILESTONES.md</i>. "
         "Aucun jalon n'est franchi sans que la carte soit signée, le verrou croisé "
         "vérifié et l'oracle passé : la discipline protocolaire s'applique dès le "
         "premier octet. L'application cible — un outil de pentest de type "
         "intercepteur MITM pour Windows 11 — est choisie comme stress test : elle "
         "exige du réseau, de la concurrence, du parsing d'entrées non fiables et du "
         "chiffrement, soit un large éventail de blocs aux contrats très différents. "
         "Son usage est encadré : tests autorisés en environnement de laboratoire, "
         "machine virtuelle isolée, autorité de certification de test installée "
         "localement."))

story += table_block("", make_table(
    ["Jalon", "Objectif", "Livrables", "Critères de sortie"],
    [
        ["<b>M0</b>", "Prouver la chaîne artefact", "Éditeur PE32+ minimal ; hello.exe "
         "via WriteFile ; carte v0 à trois blocs ; vérificateur de round-trip",
         "Exécution sur Windows 11 ; round-trip 100 % ; carte signée et vérifiée ; "
         "moins de 4 Kio. Règles : R1-R3, R8-R9"],
        ["<b>M1</b>", "Blocs réutilisables", "Mini-libc scellée : memcpy, memcmp, "
         "strlen, itoa, allocateur par zone",
         "Oracle à 100 % ; première cristallisation ; adresses stables démontrées. "
         "Règles : R5-R7"],
        ["<b>M2</b>", "Code actif et patch à chaud", "Serveur TCP écho ; thread par "
         "connexion ; journal console",
         "Patch du bloc écho pendant exécution, sans interruption ; rollback démontré. "
         "Boucle complète"],
        ["<b>M3</b>", "Entrées non fiables", "Proxy HTTP ; parseur à contrats "
         "renforcés ; threading du tunnel",
         "Un million de requêtes fuzzées sans crash ; proxy transparent pour curl. "
         "Contrats renforcés"],
        ["<b>M4</b>", "Tunnel chiffré", "Contexte SSPI / Schannel ; poignée de main "
         "TLS ; relais chiffré",
         "HTTPS en transit ; échec propre sur certificat invalide. Contrats "
         "cryptographiques"],
        ["<b>M5</b>", "L'outil complet", "Autorité de test locale ; interception et "
         "re-chiffrement ; journal des flux ; interface en ligne de commande",
         "Interception d'un flux navigateur en VM isolée ; patch à chaud du journal en "
         "production ; empreintes par build activées. Intégralité du protocole"],
        ["<b>M6</b>", "Portabilité inter-OS", "Profil x86-64-linux-elf64 complet : "
         "couche I réutilisée sans modification ; mini-libc re-scellée ; hello et "
         "serveur écho sur Linux",
         "Diff nul sur la couche I ; carte multi-profils signée et vérifiée ; le même "
         "oracle passe sur les deux profils"],
        ["<b>M7</b>", "Portabilité inter-ISA", "Profil riscv64-linux-elf64 : blocs "
         "re-générés pour une ISA à instructions de taille fixe ; patch à chaud "
         "adapté (registre scratch + fence.i)",
         "Round-trip 100 % sur la nouvelle ISA ; patch à chaud conforme au profil ; "
         "verrou croisé multi-profils ; export de continuité multi-profils vérifié"],
    ],
    [0.09, 0.19, 0.34, 0.38], font_small=True),
    "Tableau 15 — Jalons M0-M7, livrables et critères de sortie mesurables.")

story.append(para(
    "Trois jalons jouent un rôle charnière. M0 est le jalon existentiel : il prouve que "
    "la chaîne notation, octets, exécutable, exécution fonctionne de bout en bout sans "
    "compilateur, et que la carte rend le résultat vérifiable — s'il échoue, le "
    "paradigme entier est remis en question avant tout investissement supplémentaire. "
    "M2 est le jalon de vérité du protocole : le patch à chaud sur code en cours "
    "d'exécution est la capacité qui a motivé l'architecture de balises depuis la "
    "première discussion ; sa démonstration — bascule atomique, continuité de service, "
    "rollback — valide que l'investissement dans la carte et le verrou croisé paie "
    "concrètement. M6 et M7, ajoutés par la v0.3, valident l'universalité en isolant "
    "chaque variable : M6 change l'OS à ISA constante — le critère décisif est le "
    "diff nul sur la couche I, preuve que l'intention vit bien dans I et pas dans les "
    "octets — et M7 change d'ISA — le critère décisif est que le même oracle valide "
    "les blocs des deux ISA : le coût de vérification ne double pas, il se mutualise. "
    "Ensemble, ils transforment la portabilité de promesse en propriété démontrée."))

# ================================================================ CH 12
story += h1_block(
    "12. Glossaire et journal des versions",
    para("Ce chapitre fixe le vocabulaire normatif du protocole et consigne "
         "l'évolution de la spécification. Le glossaire fait foi : lorsqu'un terme "
         "technique apparaît dans un contrat, une règle ou un critère de sortie, c'est "
         "la définition ci-dessous qui s'applique, sans interprétation libre."))

story += table_block("", make_table(
    ["Terme", "Définition"],
    [
        ["<b>Carte</b>", "Couche C : index signé et chiffré liant intention et binaire, "
         "unique interface de développement de l'agent"],
        ["<b>Bloc</b>", "Unité de code machine de 32 à 512 instructions, une "
         "responsabilité, un point d'entrée stable"],
        ["<b>Scellage</b>", "Acte atomique d'engagement : écriture du bloc, mise à jour "
         "de la carte, inscription de l'empreinte"],
        ["<b>Cristallisation</b>", "Immuabilité d'un bloc après dix vérifications "
         "réussies ; modification dès lors soumise à procédure lourde"],
        ["<b>Oracle éphémère</b>", "Implémentation de référence triviale dérivée de la "
         "couche I, générée par session et détruite après usage"],
        ["<b>Verrou croisé</b>", "Contrôle bilatéral d'intégrité : empreintes des blocs "
         "dans la carte, signature de la carte, checksums au chargement"],
        ["<b>Contrat</b>", "Signature typée, pré et post-conditions et invariants "
         "publiés d'un bloc — la partie de I embarquée dans C"],
        ["<b>Fragment</b>", "Quart de carte chiffré séparément : localisation, "
         "contrats, preuves, builds"],
        ["<b>Profil de cible</b>", "Instanciation complète du protocole pour un couple "
         "ISA/OS : ABI, format, interface système, patch à chaud, notation, padding"],
        ["<b>Suite cryptographique</b>", "Paramètres de l'en-tête de carte — hachage, "
         "signature, chiffrement — choisis par le développeur dans une liste blanche"],
        ["<b>Re-cryptage</b>", "Migration atomique de la suite cryptographique : "
         "recalcul des empreintes, re-chiffrement, re-signature, archivage de "
         "l'ancienne carte"],
        ["<b>Export de continuité</b>", "Conteneur chiffré et signé regroupant I, B, C "
         "et un manifeste — seule forme de transfert de l'état de développement"],
        ["<b>Empreinte de build</b>", "Variante binaire unique par livraison et par "
         "profil, rendant toute fuite traçable"],
        ["<b>Vecteurs dorés</b>", "Jeu de tests de référence d'un bloc, conservé haché "
         "dans frag-prf"],
        ["<b>Notation</b>", "Représentation textuelle des instructions assemblées par "
         "le moteur du profil — un média, jamais un langage compilé"],
        ["<b>Round-trip</b>", "Contrôle de fidélité : assemblage puis désassemblage "
         "d'un bloc, comparaison exacte"],
    ],
    [0.22, 0.78], font_small=True),
    "Tableau 16 — Glossaire normatif du protocole.")

story += table_block("", make_table(
    ["Version", "Date", "Contenu"],
    [
        ["v0.1", "25 oct. 2026", "Première ébauche : couches I/B/C, règles R1 à R7, "
         "boucle de mise à jour en sept étapes, feuille de route M0-M5"],
        ["v0.2", "25 oct. 2026", "Décisions D1 à D10 ; sharding de la carte en quatre "
         "fragments chiffrés ; suite cryptographique (Ed25519, XChaCha20-Poly1305, "
         "Argon2id) ; règles R8 à R10 (verrou croisé, signature obligatoire, fail-"
         "closed) ; empreintes par build ; budgets en tokens ; spécification de la "
         "cible x86-64 / Windows 11 ; critères de sortie mesurables pour chaque jalon"],
        ["v0.3", "25 oct. 2026", "Universalité par profils de cible (D14, amende "
         "D10) ; suite cryptographique paramétrable — SHA-256 par défaut, listes "
         "blanches (D15, amende D5) ; export de continuité chiffré et signé (D16, "
         "précise R1) ; en-tête de carte normalisé ; jalons M6-M7"],
    ],
    [0.11, 0.15, 0.74]),
    "Tableau 17 — Journal des versions de la spécification.")

story.append(para(
    "La présente version fige les arbitrages nécessaires au démarrage du jalon M0, qui "
    "s'effectue sur le profil primaire. Les évolutions prévisibles — bloc optionnel de "
    "syscalls directs, TLS 1.3 pur en blocs scellés, profils additionnels après M7 — "
    "sont volontairement hors du périmètre courant afin que chaque addition s'appuie "
    "sur des résultats mesurés. La règle de gouvernance reste celle du journal des "
    "décisions : toute évolution invalide explicitement ce qu'elle remplace, et rien "
    "ne se change en silence."))

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
        DOWNLOAD_DIR, "Protocole_TRIADE_v0.3_Specification.pdf"))
    print("copie livrable ->", os.path.join(
        DOWNLOAD_DIR, "Protocole_TRIADE_v0.3_Specification.pdf"))
