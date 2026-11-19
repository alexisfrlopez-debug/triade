#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_preuves_v194.py — le corps du document
TRIADE_preuves_et_calculs_v0.19.4.pdf (ReportLab) : les pièces de la
session cq01qv1za — le coût de la boucle sous R11. Les pièces verbatim
(le rapport pointeur, le rapport M4, les contrôles négatifs, le verdict
du double moteur) sont LUES de l'atelier — jamais retapées."""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer)

REPO = "/home/z/my-project/depot"
V7 = os.path.join(REPO, "scripts", "vague7")
OUT = os.path.join(V7, "preuves_v194_body.pdf")
AT = os.path.join(REPO, "atelier-cout-boucle-cq01qv1za")

FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", f"{FDIR}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", f"{FDIR}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Italic", f"{FDIR}/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans", f"{FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", f"{FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", f"{FDIR}/LiberationMono-Regular.ttf"))

DARK = colors.HexColor("#162032")
st_body = ParagraphStyle("body", fontName="Serif", fontSize=9.6, leading=14.2,
                         alignment=TA_LEFT, spaceAfter=7,
                         textColor=colors.HexColor("#1a1a1a"))
st_h1 = ParagraphStyle("h1", fontName="Serif-Bold", fontSize=16.5, leading=21,
                       textColor=DARK, spaceBefore=14, spaceAfter=8)
st_h2 = ParagraphStyle("h2", fontName="Sans-Bold", fontSize=11, leading=15,
                       textColor=colors.HexColor("#4A90C4"), spaceBefore=10,
                       spaceAfter=5)
st_mono = ParagraphStyle("mono", fontName="Mono", fontSize=6.6, leading=8.6,
                         textColor=colors.HexColor("#222222"))
st_titre = ParagraphStyle("titre", fontName="Serif-Bold", fontSize=21,
                          leading=26, textColor=DARK, spaceAfter=4)
st_sous = ParagraphStyle("sous", fontName="Sans", fontSize=10.5, leading=15,
                         textColor=colors.HexColor("#555555"), spaceAfter=2)


def para(txt, st=st_body):
    return Paragraph(txt.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;").replace("\n", "<br/>"), st)


def lit(nom):
    with open(os.path.join(AT, nom), encoding="utf-8") as f:
        return f.read()


story = [
    para("TRIADE — preuves et calculs", st_titre),
    para("Édition v0.19.4 — le coût de la boucle sous R11 "
         "(l'instruction cq01qv1za, la vague du 18/11, la quatrième)",
         st_sous),
    Spacer(1, 6),
    para("Le présent document porte les pièces de la session : le pointeur "
         "seul (la campagne 36 appels réels au tokenizer natif, zéro "
         "divergence, l'expansion client), la pile mémo v2 + double moteur "
         "(l'échantillon d'audit à divergence 0 sur 2 041 opérations, le "
         "ratio M4 3,0× — H5 tenue par l'instruction du maître), les "
         "contrôles négatifs (cinq sur cinq attrapés). Les pièces verbatim "
         "sont lues de l'atelier — jamais retapées."),
    para("LA SESSION EN UNE PAGE", st_h1),
    para("(1) LE POINTEUR SEUL : la mesure avant/après sur n=18 appels "
         "réels (la même graine qu'OPT-02, la rig compter_tokens, le natif "
         "lu du champ usage, 100 % log-api, le modèle glm-4-plus) — le "
         "total 1 714 → 1 103 natifs (−35,7 %), la réponse 770 → 52 "
         "(−93,3 %), zéro divergence 18/18, l'expansion client verte 18/18 "
         "(quatre refus nommés), la re-tokenisation indépendante à 0 écart "
         "(l'artefact +2 de la voie segmentée nommé). (2) LE MÉMO V2 : la "
         "clé = sha256(bloc + entrée + contrat + config émulateur + graine "
         "+ oracle), le compteur de runs CHAÎNÉ AU CŒUR SIGNÉ, l'audit 1 "
         "run sur 10 — le 10ᵉ scellement a déclenché l'audit TOUT SEUL "
         "pendant la mesure. (3) LE DOUBLE MOTEUR : le lanceur C statique "
         "(ms_abi, six feuilles kernel32, l'image bâtie par le vrai "
         "harnais) sous QEMU-user au volume, Unicorn à l'échantillon "
         "consigné — DIVERGENCE=0 octet pour octet sur 2 041 opérations. "
         "(4) LE RATIO : l'avant 39,7 s / le C 2,2 s = 17,9× ; le régime "
         "6,8 s / 2,2 s = 3,0× — SOUS ×10 : H5 DEVIENT TENUE (l'énoncé "
         "explicite de l'instruction ; les consoles des oracles, 24 "
         "capturées, identiques ligne à ligne aux originales)."),
    para("LE RAPPORT DE LA CAMPAGNE POINTEUR — VERBATIM", st_h1),
    para(lit("RAPPORT-cq01qv1za-POINTEUR.txt"), st_mono),
    para("LE RAPPORT M4/OPT-04 — VERBATIM", st_h1),
    para(lit("RAPPORT-cq01qv1za-M4.txt"), st_mono),
    para("LES CONTRÔLES NÉGATIFS — VERBATIM", st_h1),
    para(lit("preuves/controle-negatif-v2.txt"), st_mono),
]

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2 * 2.834,
                      rightMargin=2 * 2.834, topMargin=2 * 2.834,
                      bottomMargin=2 * 2.834, title="TRIADE — preuves et "
                      "calculs v0.19.4")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width,
                          doc.height, id="f")])])
doc.build(story)
print("écrit:", OUT)
