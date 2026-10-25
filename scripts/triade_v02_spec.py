#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corps du PDF — Protocole TRIADE v0.2, specification du developpement logiciel
en code machine par agent IA. Route Report (ReportLab), TOC auto, fusion couverture."""

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
BASE = "/home/z/my-project"
SKILL_SCRIPTS = os.path.join(BASE, "skills", "pdf", "scripts")
sys.path.insert(0, SKILL_SCRIPTS)
from pdf import install_font_fallback  # noqa: E402

ASSETS = os.path.join(BASE, "scripts", "assets")
BODY_PDF = os.path.join(BASE, "scripts", "triade_body.pdf")
COVER_PDF = os.path.join(BASE, "scripts", "triade_cover.pdf")
FINAL_PDF = os.path.join(BASE, "download", "Protocole_TRIADE_v0.2_Specification.pdf")

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

install_font_fallback()

# ---------------------------------------------------------------- palette
# Cascade palette (design_engine.py palette-cascade --intent cold --mode minimal --seed 7)
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

DOC_TITLE = "Protocole TRIADE v0.2 — Spécification du développement logiciel en code machine par agent IA"

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
    """Marqueur invisible : la page ou il est dessine devient la page 1 du corps."""
    def __init__(self):
        Flowable.__init__(self)
        self.width = 0
        self.height = 0

    def draw(self):
        pass


class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, BodyStartMarker):
            # Erratum v0.2 : les pieds de page sont dessines au DEBUT de chaque
            # page ; une mise a jour de BODY_START en cours de passe laissait les
            # pages du sommaire avec la valeur de la passe anterieure (i, 1, 2, 2).
            # En phase 2 la valeur est gelee : plus de derive.
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
    canvas.drawString(MARGIN, PAGE_H - 40, "PROTOCOLE TRIADE v0.2 — SPÉCIFICATION TECHNIQUE")
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, PAGE_H - 46, PAGE_W - MARGIN, PAGE_H - 46)
    # --- pied de page : filet + auteur + numero de page zone
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 40, PAGE_W - MARGIN, 40)
    canvas.setFont("FreeSerif", 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, 28, "TRIADE · brouillon de travail · 25 octobre 2026")
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
    """Typographie francaise : tiret cadratin insecable au mot precedent."""
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
    """Bloc de code : fond carte + filet accent a gauche."""
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
    """Encadre metrique : grand chiffre + libelle."""
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
    """Encadre note : filet accent gauche + fond teinte."""
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
    """Tableau standard : en-tete M-tier, rayures L-tier, cellules Paragraph."""
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
    """Spacer + tableau + legende, avec anti-orphelin sur le titre."""
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
    "par l'agent, tandis que l'artefact livré est du code machine x86-64 pur. Le compilateur "
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
    "interface de développement à l'agent. Ce document en fixe la spécification complète."))

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
        ["<b>Performance</b>", "100 % code machine, zéro abstraction intermédiaire entre "
         "l'écriture et l'exécution", "Comparaison par bloc scellé face à une référence "
         "compilée (clang -O2)"],
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
    "M0-M5. Trois non-objectifs doivent être posés d'emblée pour éviter tout malentendu "
    "d'usage. Premièrement, TRIADE ne prétend pas remplacer les langages dans l'industrie : "
    "c'est une architecture de laboratoire, conçue pour être validée sur une application "
    "réelle complète. Deuxièmement, la furtivité face aux EDR n'est pas recherchée : l'outil "
    "cible est un utilitaire de pentest destiné à des tests autorisés en environnement de "
    "laboratoire, et les API du système sont appelées via la table d'imports standard. "
    "Troisièmement, seule l'architecture x86-64 est visée à ce stade ; une extension RISC-V "
    "est prévue après M5 comme validation de la portabilité du protocole lui-même."))

# ================================================================ CH 2
story += h1_block(
    "2. Journal des décisions (D1-D10)",
    para("Chaque décision structurante est consignée avec ses alternatives rejetées et sa "
         "justification rattachée à la fonction objectif. Ce journal est la mémoire des "
         "arbitrages : toute révision future du protocole doit soit respecter ces décisions, "
         "soit expliciter précisément ce qui les invalide. Cette discipline évite la dérive "
         "progressive qui transforme un protocole propre en accumulation d'exceptions "
         "incohérentes."))

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
         "Argon2id (dérivation)", "AES-GCM ; clés dérivées par SHA-256"],
        ["D5", "Verrou croisé", "SHA-256 par bloc scellé + carte signée en entier, vérifiés "
         "avant chaque édition et au chargement", "Signature du seul binaire"],
        ["D6", "Empreintes par build", "Variante unique par livraison : réordonnancement, "
         "nops, encodages équivalents", "Binaire identique pour tous les destinataires"],
        ["D7", "Appels système", "API Windows via IAT (kernel32, ws2_32, Schannel)",
         "Syscalls directs avec table par build de Windows"],
        ["D8", "Granularité des blocs", "32 à 512 instructions, un bloc = une "
         "responsabilité, padding de 16 octets", "Micro-blocs (1-8 instructions) ; "
         "méga-blocs (plusieurs milliers)"],
        ["D9", "TLS", "Schannel (SSPI) au jalon M4", "TLS 1.3 pur implémenté en blocs "
         "scellés (reporté en objectif post-M5)"],
        ["D10", "Cible", "x86-64, Windows 11, PE32+ écrit à la main, DEP/ASLR/CFG respectés",
         "RISC-V sous QEMU ; x86-64 Linux"],
    ],
    [0.055, 0.155, 0.42, 0.37], font_small=True),
    "Tableau 2 — Journal des dix décisions structurantes de la version v0.2.")

story.append(para(
    "Quatre décisions méritent un développement car elles engagent l'architecture entière. "
    "<b>D1</b> : l'oracle éphémère est le pivot du compromis entre le « 100 % langage "
    "machine » exigé pour l'artefact et la sûreté d'exécution. L'implémentation de "
    "référence — triviale, lente, écrite dans un langage sûr — ne sort jamais du "
    "laboratoire : elle est régénérée à chaque session puis détruite. Elle ne dégrade donc "
    "ni la performance ni la pureté de l'artefact livré, tout en attrapant les corruptions "
    "mémoire avant le scellage. Sur le plan du coût en tokens, elle est également "
    "rentable : régénérer un oracle trivial coûte moins cher que de traquer une corruption "
    "silencieuse dans un binaire déjà scellé."))

story.append(para(
    "<b>D2</b> : keystone et capstone forment le couple d'assemblage et de désassemblage de "
    "référence. Le choix se justifie par la granularité instruction et le contrôle octet par "
    "octet qu'ils offrent en processus, sans fichier objet intermédiaire. La nuance capitale "
    "est que cette notation n'est pas un compilateur : aucune optimisation, aucune décision "
    "de réécriture ne s'intercale entre ce que l'agent écrit et les octets produits. Le "
    "principe WYSIWYG — ce que vous écrivez est ce qui s'exécute — est préservé "
    "intégralement, et l'artefact demeure le couple octets + carte. nasm en mode binaire "
    "plat reste le repli pour les encodages exotiques que keystone ne saurait pas produire."))

story.append(para(
    "<b>D5</b> : le verrou croisé répond à la menace spécifique de l'empoisonnement de "
    "carte — un attaquant qui falsifierait les métadonnées ferait travailler l'agent sur "
    "des informations fausses, et pourrait lui faire introduire une porte dérobée en "
    "croyant respecter les contrats. La contre-mesure est bilatérale : la carte porte le "
    "SHA-256 de chaque bloc scellé, et la carte entière est signée Ed25519. L'agent refuse "
    "toute carte non signée et tout binaire dont les empreintes divergent ; le binaire, de "
    "son côté, vérifie ses propres checksums au chargement et s'arrête proprement en cas "
    "d'écart. <b>D7</b> enfin : les syscalls directs exigeraient une table de numéros par "
    "build de Windows — c'est-à-dire une carte cachée supplémentaire, fragile et "
    " coûteuse à maintenir — pour un gain relevant de la furtivité, hors du périmètre "
    "des jalons M0 à M4."))

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
                "d'intention (I vers C), verrou croisé SHA-256 / Ed25519 (C vers B). "
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
    "Le flux de travail découle directement de cette séparation. Pour toute évolution, "
    "l'agent produit d'abord un diff sur la couche I — on modifie le <i>quoi</i> avant le "
    "<i>comment</i>. Il localise ensuite les blocs concernés au travers de la carte, sans "
    "jamais scanner le binaire. Il régénère les seuls blocs impactés, les fait vérifier par "
    "l'oracle, puis commite l'ensemble de façon atomique : patch du binaire, mise à jour de "
    "la carte et scellage ne font qu'un. La cohérence de l'ensemble est garantie par le "
    "verrou croisé, vérifié avant chaque édition et à chaque chargement du binaire."))

story += h2_block("3.2 Invariants structurels", para(
    "Quatre invariants non négociables structurent le système et sont vérifiés à chaque "
    "cycle de build. Leur violation n'est pas une erreur de conception parmi d'autres : "
    "c'est un refus de build, car chacun protège une propriété dont dépendent toutes les "
    "autres règles."))
story += bullets([
    "<b>B n'est jamais nu</b> (R1) : tout binaire est accompagné d'une carte à jour et "
    "signée, sous peine de perdre toute maintenabilité.",
    "<b>Les adresses exposées sont stables</b> (R7) : les points d'entrée des blocs scellés "
    "sont garantis par padding ; aucun patch ne déplace jamais du code existant.",
    "<b>La signature couvre la carte entière</b> (R9) : les quatre fragments sont signés "
    "ensemble — une carte partielle ou contrefaite est rejetée avant la moindre opération.",
    "<b>B est auto-vérifiant au chargement</b> (R10) : le binaire contrôle ses checksums "
    "avant de s'exécuter et s'arrête proprement en cas d'écart (fail-closed).",
])

# ================================================================ CH 4
story += h1_block(
    "4. La carte : spécification (couche C)",
    para("La carte est le cœur opérationnel du protocole : c'est elle qui rend le binaire "
         "navigable pour l'agent, qui porte les preuves et qui concentre la valeur "
         "intellectuelle du projet. Sa conception obéit à trois contraintes tirées de la "
         "fonction objectif : elle doit être compacte (coût en tokens), intègre (verrou "
         "croisé) et résiliente face à la compromission (sharding et chiffrement). Chacune "
         "de ces contraintes se traduit par un mécanisme précis, spécifié dans ce chapitre."))

story += h2_block("4.1 Fragments et sharding", make_table(
    ["Fragment", "Contenu", "Raison d'être de la séparation"],
    [
        ["<b>frag-loc</b>", "Identifiants, noms, adresses, tailles, états, dépendances",
         "Localisation : le plus lu, le moins sensible — peut être chargé seul"],
        ["<b>frag-con</b>", "Signatures, pré/post-conditions, invariants, conventions "
         "d'appel", "Contrats : diffés à chaque changement (R2), lus à chaque édition"],
        ["<b>frag-prf</b>", "Vecteurs dorés hachés, compteurs de cristallisation, seuils",
         "Preuves : volumineux, rarement lu en entier après cristallisation"],
        ["<b>frag-bld</b>", "SHA-256 des blocs, manifestes de build, registre des variantes",
         "Verrou croisé et traçage (D5, D6) — jamais quitté le poste de développement"],
    ],
    [0.13, 0.44, 0.43]),
    "Tableau 4 — Les quatre fragments de la carte et leur justification.")

story.append(Spacer(1, 2))
story.append(callout_note(
    "<b>Quatre fragments chiffrés séparément.</b> Chaque fragment est chiffré avec sa "
    "propre clé dérivée de la clé maîtresse (XChaCha20-Poly1305). Un compromis partiel "
    "— la fuite d'un fragment isolé — n'est jamais une perte totale : les contrats sans "
    "les adresses, ou les preuves sans les contrats, ne reconstituent pas la carte."))

story.append(para(
    "Le chiffrement au repos et la signature sont précisés par la décision D4 : XChaCha20-"
    "Poly1305 pour le chiffrement (nonce aléatoire de 192 bits, sans risque de collision "
    "pratique), Argon2id pour la dérivation de la clé maîtresse depuis la phrase secrète "
    "(mémoire au moins 64 Mio, au moins 3 itérations), et Ed25519 pour la signature de "
    "l'ensemble des quatre fragments. La signature est calculée sur le concaténé des "
    "empreintes de chaque fragment, ce qui lie indissociablelement leur ensemble : toute "
    "substitution d'un seul fragment invalide la signature globale."))

story += h2_block("4.2 Format d'entrée de bloc", para(
    "Chaque bloc est décrit par une entrée dont la syntaxe est volontairement ASCII et "
    "ligne-par-ligne : la tokenisation est non ambiguë, le diff est lisible, et aucun "
    "caractère Unicode exotique ne peut corrompre l'encodage en transit. L'exemple ci-"
    "dessous est l'entrée complète du bloc de référence utilisé tout au long de la "
    "spécification."))

story.append(code_block(
    "[bloc] id=b7f3a9  addr=0x4012A0  size=212  v=4  etat=scelle\n"
    "  sig     : (ptr u8, usize) -> usize\n"
    "  pre     : ptr != 0 && len <= MAX_LEN\n"
    "  post    : ret <= len\n"
    "  regs    : rbx, r12-r15 sauvegardes ; conv: msx64\n"
    "  inv     : r8 aligne 16 dans la boucle\n"
    "  deps    : [a31c2 memcpy] [ext AVX2]\n"
    "  preuves : memsafe:ok bornes:ok term:ok\n"
    "  tests   : 12400 cas ; ref=oracle_v9 ; crist=10/10",
    "Entree complete — budget maximal : 200 tokens (D8)."))

story.append(para(
    "Les champs se répartissent en deux ensembles. La première ligne — identifiant, "
    "adresse, taille, version, état — constitue à elle seule l'entrée de localisation "
    "portée par frag-loc : c'est la seule partie que l'agent lit pour situer un bloc, et "
    "son budget est de 40 tokens maximum. Les lignes suivantes (signature, pré/post-"
    "conditions, registres préservés, invariants, dépendances, preuves, tests) forment "
    "l'entrée détaillée portée par frag-con et frag-prf : elles ne sont chargées que "
    "lorsque le bloc est effectivement édité. L'état du bloc suit le cycle de vie du "
    "paragraphe 4.4 : brouillon, scellé ou cristallisé."))

story += h2_block("4.3 Verrou croisé : procédure", para(
    "Le verrou croisé est la procédure d'intégrité exécutée avant chaque édition et avant "
    "chaque chargement. Avant toute opération d'écriture, l'agent exécute la séquence "
    "suivante, et tout échec interrompt la session — jamais de contournement, jamais de "
    "reprise forcée."))
story += bullets([
    "<b>Étape 1.</b> Vérifier la signature Ed25519 de la carte sur les quatre fragments ; "
    "une carte non signée ou à signature invalide est refusée (R9).",
    "<b>Étape 2.</b> Recalculer le SHA-256 de chaque bloc scellé visé par l'édition, ainsi "
    "que de l'ensemble de ses dépendances directes.",
    "<b>Étape 3.</b> Comparer les empreintes obtenues à celles portées par frag-bld ; tout "
    "écart signifie que binaire et carte ont divergé.",
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

story += h2_block("4.4 Cycle de vie d'une entrée", make_table(
    ["État", "Signification", "Transition"],
    [
        ["<b>brouillon</b>", "Bloc en cours d'écriture, non vérifié, non adressé",
         "Création par l'agent ; adresse provisoire"],
        ["<b>vérifié</b>", "Oracle passé une fois, round-trip conforme",
         "Après une session de vérification complète (R5)"],
        ["<b>scellé</b>", "Commité : adresse stable, SHA-256 dans frag-bld",
         "Commit atomique (étape 6 de la boucle)"],
        ["<b>cristallisé</b>", "Immuable : 10 vérifications réussies consécutives",
         "Seuil atteint (R6) ; modification = procédure lourde"],
        ["<b>déprécié</b>", "Remplacé par une version plus récente",
         "Conservé pour l'audit et le traçage des variantes"],
    ],
    [0.15, 0.44, 0.41]),
    "Tableau 5 — Cycle de vie d'une entrée de la carte.")

story.append(para(
    "La cristallisation est le mécanisme d'économie structurelle du protocole : un bloc "
    "cristallisé n'est plus jamais rechargé ni re-vérifié en session — seul son SHA-256 "
    "est contrôlé, ce qui coûte une comparaison de 64 caractères. La modification d'un "
    "bloc cristallisé reste possible mais relève d'une procédure délibérément lourde : "
    "justification sur la couche I, double vérification par oracle, et création d'un "
    "nouveau bloc plutôt qu'une réécriture — l'ancien passant à l'état déprécié. Cette "
    "asymétrie de coût est volontaire : elle rend l'évolution des blocs mûrs rare et "
    "réfléchie, exactement comme un noyau de système d'exploitation protège ses parties "
    "les plus éprouvées."))

# ================================================================ CH 5
story += h1_block(
    "5. Règles du protocole v0.2",
    para("Les règles constituent le noyau normatif du protocole : elles sont peu "
         "nombreuses, vérifiables mécaniquement et sanctionnées par des effets concrets "
         "— refus de build, refus de commit ou blocage de session — plutôt que par des "
         "recommandations. Les règles R1 à R7 proviennent de la v0.1 ; les règles R8 à "
         "R10 sont les ajouts de la v0.2, consacrés à l'intégrité de la chaîne carte "
         "vers binaire."))

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
        ["<b>R8</b> Verrou croisé", "SHA-256 des blocs et signature de la carte vérifiés "
         "avant chaque édition", "Session bloquée"],
        ["<b>R9</b> Carte signée obligatoire", "L'agent refuse toute carte non signée",
         "Refus de démarrage"],
        ["<b>R10</b> Fail-closed au chargement", "Checksums vérifiés au lancement ; "
         "écart = arrêt propre", "Arrêt de l'exécution"],
    ],
    [0.24, 0.48, 0.28]),
    "Tableau 6 — Les dix règles du protocole et leurs sanctions.")

story.append(para(
    "Deux points appellent une précision. D'abord, R4 ne signifie pas qu'un bloc ne peut "
    "jamais changer de comportement : elle signifie qu'un bloc remplaçant honore les "
    "contrats publiés de son prédécesseur — mêmes signatures, mêmes pré et post-"
    "conditions, mêmes invariants visibles. Les appelants compilés — ou scellés — contre "
    "l'ancienne version restent donc valides sans re-liage, ce qui est la condition de "
    "possibilité du patch à chaud du chapitre 6. Ensuite, R7 n'interdit pas d'ajouter du "
    "code : elle interdit de déplacer l'existant. Le padding inter-blocs de 16 octets et "
    "l'alignement sur 16 maintiennent des zones de croissance où de nouveaux blocs ou de "
    "nouveaux trampolines s'insèrent sans jamais déranger une adresse déjà promise."))

# ================================================================ CH 6
story += h1_block(
    "6. Boucle de mise à jour",
    para("La boucle de mise à jour est le battement de cœur du protocole : c'est la "
         "seule voie par laquelle le logiciel évolue. Elle se déroule en sept étapes "
         "réparties en deux phases — l'édition, puis la validation et le commit — "
         "séparées par un point de non-retour : rien n'est écrit dans le binaire avant "
         "que l'oracle n'ait rendu son verdict. La figure 2 en donne la vue d'ensemble, "
         "le tableau 7 en précise les entrées et sorties."))

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
    "Tableau 7 — Entrées, sorties et règles associées à chaque étape de la boucle.")

story += h2_block("6.1 Patch à chaud sur x86-64", callout(
    "12 à 16 octets",
    "Taille d'un trampoline de bascule atomique — la plus petite unité de patch à chaud"))

story.append(para(
    "Le patch à chaud — modifier un logiciel en cours d'exécution — est l'un des deux "
    "objectifs fondateurs du projet avec la performance. Sur x86-64, il se heurte à deux "
    "contraintes matérielles : la cohérence du cache d'instructions, et l'atomicité de la "
    "bascule. La méthode retenue contourne les deux en n'écrivant <b>jamais</b> un bloc "
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
    "seuls les points d'entrée — promis par R7 — sont susceptibles d'être trampolineés, "
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
    "avec la version courante des contrats ; et son coût de régénération — quelques "
    "milliers de tokens pour un bloc typique — reste très inférieur au coût de "
    "diagnostic d'une corruption mémoire découverte après scellage."))

story += h2_block("7.2 Round-trip de notation", para(
    "Le second pilier est purement mécanique : chaque bloc assemblé par keystone est "
    "désassemblé par capstone, et les instructions obtenues sont comparées à la "
    "notation d'origine. Tout désaccord — une instruction, un opérande, une taille "
    "d'encodage — est un échec de build. Ce contrôle à coût quasi nul attrape la classe "
    "d'erreurs la plus insidieuse du développement en code machine : l'écart silencieux "
    "entre ce que l'agent croit avoir écrit et les octets réellement produits, qu'il "
    "s'agisse d'un encodage alternatif choisi par l'assembleur ou d'une coquille dans "
    "la notation."))

story += h2_block("7.3 Cristallisation et chaîne de confiance du scellage", para(
    "La chaîne de confiance du scellage résume le parcours d'une preuve, de sa production "
    "à son ancrage cryptographique :"))
story += bullets([
    "L'oracle rend un verdict sur le bloc candidat (tests différentiels par propriétés).",
    "Les vecteurs dorés de la session sont hachés et consignés dans frag-prf, avec le "
    "compteur de vérifications du bloc.",
    "Le SHA-256 du bloc scellé est inscrit dans frag-bld — c'est la moitié binaire du "
    "verrou croisé.",
    "La carte complète est signée Ed25519, liant fragments, preuves et empreintes en un "
    "seul acte de confiance.",
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
         "Signature Ed25519 ; refus de carte non signée ; verrou croisé",
         "Détecté — session bloquée (fail-closed)"],
        ["Fuite de la carte", "Initié, poste compromis", "Fragments au repos",
         "Chiffrement XChaCha20 ; sharding ; escrow",
         "Perte partielle limitée à un fragment"],
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
    "Tableau 8 — Modèle de menace : acteur, cible, contre-mesure et risque résiduel.")

story.append(para(
    "Deux lectures de ce tableau méritent d'être explicitées. La rétro-ingénierie est "
    "traitée comme un objectif d'économie, pas d'impossibilité : rendre le coût de "
    "l'analyse supérieur à la valeur de ce qu'on obtient. Un binaire strippé, sans "
    "structure ni symboles, dont chaque exemplaire diffère, coûte sensiblement plus cher "
    "à analyser qu'un binaire compilé standard — mais les modèles de langage appliqués "
    "à la décompilation progressent, et l'avantage doit être réévalué à chaque "
    "génération de modèles. À l'inverse, l'empoisonnement de carte est une menace "
    "nouvelle, spécifique à ce paradigme : falsifier les métadonnées ferait travailler "
    "l'agent de confiance sur des informations fausses. C'est précisément la menace que "
    "les règles R8 et R9 neutralisent par la signature et le verrou croisé."))

story += h2_block("8.2 Empreintes par build", para(
    "Puisque la régénération du code machine est quasi gratuite dans ce paradigme, "
    "chaque livraison peut porter une variante unique sans coût marginal : "
    "réordonnancement des blocs scellés indépendants, insertion de nops multioctets, "
    "choix parmi les encodages équivalents que l'ISA offre pour une même instruction. "
    "Le registre des variantes est conservé dans frag-bld, côté développeur. Toute fuite "
    "du binaire devient ainsi traçable jusqu'à son destinataire — le canary trap "
    "classique, appliqué ici au code machine où il est structurellement plus facile à "
    "mettre en œuvre que dans un pipeline de compilation classique."))

story.append(code_block(
    "; deux encodages equivalents de la meme instruction\n"
    "  89 C0      ; mov eax, eax  (forme : rm <- r)\n"
    "  8B C0      ; mov eax, eax  (forme : r <- rm)\n"
    "; ni le sens ni les effets ne changent - seule la signature binaire change",
    "Exemple de variante d'encodage sélectionnable par build (D6)."))

story += h2_block("8.3 Gestion des clés", para(
    "La phrase secrète maîtresse traverse Argon2id — mémoire d'au moins 64 Mio, au "
    "moins trois itérations, parallélisme unitaire — pour produire la clé maîtresse ; "
    "les clés de chaque fragment en sont dérivées par HKDF avec un contexte distinct "
    "par fragment et par génération. Les sauvegardes suivent la règle 3-2-1 chiffrée, "
    "et l'escrow de la clé maîtresse peut recourir à un partage de secret deux-sur-trois "
    "pour éliminer le point de défaillance unique qu'une phrase secrète unique "
    "constituerait. La rotation des clés entraîne une re-signature complète de la carte "
    "— opération atomique, journalisée, et vérifiable après coup par la chaîne de "
    "confiance du scellage décrite au chapitre 7."))

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
    "à maturité. Le tableau 9 fixe les budgets par type d'opération."))

story += table_block("", make_table(
    ["Opération", "Fragments et données lus", "Budget"],
    [
        ["Localiser un bloc", "frag-loc — une entrée", "40 tokens max"],
        ["Éditer simplement un bloc", "frag-loc + frag-con du bloc + notation du bloc",
         "3 000 tokens max"],
        ["Ajouter un bloc", "frag-loc + frag-con + seuils frag-prf",
         "6 000 tokens max"],
        ["Audit complet (rare)", "Carte entière déchiffrée",
         "Non budgété — opération exceptionnelle"],
    ],
    [0.28, 0.47, 0.25]),
    "Tableau 9 — Budgets en tokens par type d'opération d'édition.")

story.append(para(
    "Pour situer ces ordres de grandeur : dans un pipeline classique, une modification "
    "modeste commence typiquement par relire le module source complet et son contexte "
    "— plusieurs dizaines de milliers de tokens — avant même d'écrire. Le budget TRIADE "
    "pour la même opération est borné à quelques milliers, parce que la localisation "
    "remplace la relecture. L'instrumentation obligatoire mesure le coût réel de chaque "
    "opération d'édition et alimente les indicateurs de santé du protocole : précision "
    "de localisation (le bon bloc identifié du premier coup, cible 95 % au jalon M0), "
    "coût moyen d'une édition simple (cible 5 000 tokens), et taux de régression "
    "post-patch (cible zéro, rollback exclus). Ces métriques font partie des critères "
    "de sortie des jalons — elles valident que l'économie promise est réellement "
    "délivrée, et pas seulement théorisée."))

# ================================================================ CH 10
story += h1_block(
    "10. Cible x86-64 / Windows 11",
    para("Le choix de la cible — décision D10, arrêtée pour le réalisme et le test "
         "direct sur une application Windows — fixe trois corps de contraintes que le "
         "protocole doit absorber : l'ABI d'appel Microsoft x64, le format d'exécutable "
         "PE32+, et les protections du système d'exploitation. Ce chapitre en donne les "
         "règles opérationnelles ; il constitue le raccourci de référence pour l'agent "
         "lors de l'écriture des blocs. Une précision d'importance : « sans compilateur » "
         "ne signifie pas « sans système d'exploitation » — les API sont appelées via la "
         "table d'imports, comme tout binaire natif légitime."))

story += h2_block("10.1 ABI Microsoft x64", make_table(
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
    "Tableau 10 — Règles essentielles de l'ABI Microsoft x64.")

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
    "Les dépendances système se limitent à trois ensembles : kernel32 pour les entrées-"
    "sorties, les threads et le tas ; ws2_32 pour le réseau à partir du jalon M2 ; et "
    "Schannel via SSPI pour TLS au jalon M4. Les adresses ne sont jamais codées en dur : "
    "chaque appel transite par la table d'imports, résolue par le chargeur — ce qui "
    "préserve la compatibilité entre builds de Windows et respecte l'ASLR. Les "
    "protections du système sont honorées par construction : DEP, puisque aucun code "
    "n'est jamais généré en pile ; ASLR, grâce aux relocations ; et Control Flow Guard, "
    "par la déclaration des cibles d'appel indirect valides. L'objectif est assumé : un "
    "outil légitime par construction, dont la transparence vis-à-vis du système est "
    "totale."))

# ================================================================ CH 11
story += h1_block(
    "11. Feuille de route M0-M5",
    para("La feuille de route décompose la validation du protocole en six jalons, "
         "chacun couvrant une capacité nouvelle et se terminant par des critères de "
         "sortie mesurables. Aucun jalon n'est franchi sans que la carte soit signée, "
         "le verrou croisé vérifié et l'oracle passé : la discipline protocolaire "
         "s'applique dès le premier octet. L'application cible — un outil de pentest "
         "de type intercepteur MITM pour Windows 11 — est choisie comme stress test : "
         "elle exige du réseau, de la concurrence, du parsing d'entrées non fiables et "
         "du chiffrement, soit un large éventail de blocs aux contrats très "
         "différents. Son usage est encadré : tests autorisés en environnement de "
         "laboratoire, machine virtuelle isolée, autorité de certification de test "
         "installée localement."))

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
    ],
    [0.09, 0.19, 0.34, 0.38], font_small=True),
    "Tableau 11 — Jalons, livrables et critères de sortie mesurables.")

story.append(para(
    "Deux jalons jouent un rôle charnière. M0 est le jalon existentiel : il prouve que "
    "la chaîne notation, octets, exécutable, exécution fonctionne de bout en bout sans "
    "compilateur, et que la carte rend le résultat vérifiable — s'il échoue, le "
    "paradigme entier est remis en question avant tout investissement supplémentaire. "
    "M2 est le jalon de vérité du protocole : le patch à chaud sur code en cours "
    "d'exécution est la capacité qui a motivé l'architecture de balises depuis la "
    "première discussion ; sa démonstration — bascule atomique, continuité de service, "
    "rollback — valide que l'investissement dans la carte et le verrou croisé paie "
    "concrètement. Les jalons suivants étendent le périmètre fonctionnel sans ajouter "
    "de mécanisme protocolaire nouveau : ils éprouvent les mêmes règles sur des "
    "contrats de plus en plus exigeants."))

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
         "de la carte, inscription du SHA-256"],
        ["<b>Cristallisation</b>", "Immuabilité d'un bloc après dix vérifications "
         "réussies ; modification dès lors soumise à procédure lourde"],
        ["<b>Oracle éphémère</b>", "Implémentation de référence triviale dérivée de la "
         "couche I, générée par session et détruite après usage"],
        ["<b>Verrou croisé</b>", "Contrôle bilatéral d'intégrité : SHA-256 des blocs "
         "dans la carte, signature Ed25519 de la carte, checksums au chargement"],
        ["<b>Contrat</b>", "Signature typée, pré et post-conditions et invariants "
         "publiés d'un bloc — la partie de I embarquée dans C"],
        ["<b>Fragment</b>", "Quart de carte chiffré séparément : localisation, "
         "contrats, preuves, builds"],
        ["<b>Empreinte de build</b>", "Variante binaire unique par livraison "
         "(réordonnancement, nops, encodages) rendant toute fuite traçable"],
        ["<b>Vecteurs dorés</b>", "Jeu de tests de référence d'un bloc, conservé haché "
         "dans frag-prf"],
        ["<b>Notation</b>", "Représentation textuelle des instructions assemblées par "
         "keystone — un média, jamais un langage compilé"],
        ["<b>Round-trip</b>", "Contrôle de fidélité : assemblage puis désassemblage "
         "d'un bloc, comparaison exacte"],
    ],
    [0.22, 0.78], font_small=True),
    "Tableau 12 — Glossaire normatif du protocole.")

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
    ],
    [0.11, 0.15, 0.74]),
    "Tableau 13 — Journal des versions de la spécification.")

story.append(para(
    "La présente version fige les arbitrages nécessaires au démarrage du jalon M0. Les "
    "évolutions prévisibles — extension RISC-V après M5, bloc optionnel de syscalls "
    "directs, TLS 1.3 pur en blocs scellés — sont volontairement laissées hors du "
    "périmètre courant afin que chaque addition au protocole s'appuie sur des "
    "résultats mesurés et non sur des anticipations. La règle de gouvernance reste "
    "celle du journal des décisions : toute évolution invalide explicitement ce "
    "qu'elle remplace, et rien ne se change en silence."))

# ================================================================ BUILD
# Build en deux phases : le pied de page est dessine en DEBUT de page, or le
# marqueur de debut de corps ne connait sa page definitive qu'en fin de passe
# (la TOC peut grossir entre les passes de multiBuild). Phase 1 : convergence
# vers la valeur stable. Phase 2 : reconstruction avec la valeur gelee.
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
    subject="Specification du protocole TRIADE v0.2 : code machine x86-64 par agent IA",
)
doc.multiBuild(story, onFirstPage=on_page, onLaterPages=on_page)
print("body OK ->", BODY_PDF)
if os.path.exists(BODY_PDF + ".pass1.pdf"):
    os.remove(BODY_PDF + ".pass1.pdf")

# ---------------------------------------------------------------- fusion couverture
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
    "/Subject": "Specification du protocole TRIADE v0.2 : code machine x86-64 par agent IA",
})
os.makedirs(os.path.dirname(FINAL_PDF), exist_ok=True)
with open(FINAL_PDF, "wb") as f:
    writer.write(f)
print("final OK ->", FINAL_PDF)

