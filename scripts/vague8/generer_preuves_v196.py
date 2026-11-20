#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_preuves_v196.py — le document TRIADE_preuves_et_calculs_v0.19.6.pdf
(ReportLab) : les pièces de la vague 8 — la cohérence, la gouvernance vécue,
l'intégrité pré-enregistrée, l'indépendance par dérivation-outillée, OPT-05.
Les pièces verbatim sont LUES des ateliers — jamais retapées."""
import os
import subprocess

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer)

REPO = "/home/z/my-project/depot"
V8 = os.path.join(REPO, "scripts", "vague8")
OUT = os.path.join(V8, "preuves_v196_body.pdf")
AT_O = os.path.join(REPO, "atelier-opt05-pe6iv71fj")
AT_I = os.path.join(REPO, "atelier-independance-peap6ws09")

FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", f"{FDIR}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", f"{FDIR}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", f"{FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", f"{FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/"
                               "DejaVuSansMono.ttf"))

DARK = colors.HexColor("#162032")
st_body = ParagraphStyle("body", fontName="Serif", fontSize=9.6, leading=14.2,
                         alignment=TA_LEFT, spaceAfter=7,
                         textColor=colors.HexColor("#1a1a1a"))
st_h1 = ParagraphStyle("h1", fontName="Serif-Bold", fontSize=16.5, leading=21,
                       textColor=DARK, spaceBefore=14, spaceAfter=8)
st_mono = ParagraphStyle("mono", fontName="Mono", fontSize=6.6, leading=8.6,
                         textColor=colors.HexColor("#222222"))
st_titre = ParagraphStyle("titre", fontName="Serif-Bold", fontSize=21,
                          leading=26, textColor=DARK, spaceAfter=4)
st_sous = ParagraphStyle("sous", fontName="Sans", fontSize=10.5, leading=15,
                         textColor=colors.HexColor("#555555"), spaceAfter=2)


def para(txt, st=st_body):
    return Paragraph(txt.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;").replace("\n", "<br/>"), st)


def lit(chemin):
    with open(chemin, encoding="utf-8") as f:
        return f.read()


story = [
    para("TRIADE — preuves et calculs", st_titre),
    para("Édition v0.19.6 — la vague 8 : la cohérence des cinq pièces, la "
         "gouvernance vécue, l'intégrité pré-enregistrée, l'indépendance "
         "par dérivation-outillée, OPT-05 les hunks", st_sous),
    Spacer(1, 6),
    para("Le présent document porte les pièces de la vague 8 : la re-mesure "
         "RQ2 du pointeur seul (la même graine, n=18, zéro divergence), la "
         "campagne OPT-05 de l'édition et de l'ajout par hunks (quatre "
         "cellules n=18, les gains, les falsifications), la mesure M4 "
         "avant/chaud/bras C (n=5, l'audit 1/10 vécu), la dérivation-"
         "outillée de l'indépendance inter-familles (les 128 constantes "
         "conformes), le bras C aux trois contrats, la classification des "
         "21 survivants (12 équivalents prouvés, le score ajusté 811/820). "
         "Les pièces verbatim sont lues des ateliers — jamais retapées."),
    para("LA VAGUE 8 EN UNE PAGE", st_h1),
    para("(1) LA COHÉRENCE (gq117wphb) : les macros régénérées des journaux "
         "vivants (D1–D223, les comptes exacts), les DOI réconciliés (le "
         "concept 10.5281/zenodo.24367343 résolvant sur la courante, les "
         "versions datées nommées), la probabilité du tirage corrigée à "
         "1/16 (quatre tirages indépendants), « avant 39,7 s » porté à la "
         "valeur mesurée du manuscrit (39,3/39,2 s, n=2) puis re-mesuré à "
         "la présente session (39,1 s médiane n=5). (2) LA GOUVERNANCE "
         "VÉCUE (ansz8lvdf) : D223 actant l'état vécu — la cérémonie D183 "
         "VÉCUE, D81 amendée, le dépôt public, la rotation vérifiée ; la "
         "spécification v0.15.5 et le Livre v1.4 à l'état vécu. (3) "
         "L'INTÉGRITÉ PRÉ-ENREGISTRÉE (nunsmzmrm) : H5 en deux verdicts "
         "distincts et datés, N=7 réconcilié, H6 au verdict brut affiché, "
         "H7 à la randomisation stratifiée pré-enregistrée, l'abstract en "
         "un seul paragraphe, RQ2 re-mesuré (1 103 médiane, réponse 52), "
         "§5 à TLC/Apalache. (4) L'INDÉPENDANCE PAR DÉRIVATION-OUTILLÉE "
         "(peap6ws09) : la seconde famille DÉRIVE les 128 constantes des "
         "définitions mathématiques seules — zéro divergence contre les "
         "définitions ET le plan ; la récitation pure 2/64 + 2/64 (les "
         "ancreurs seuls — la sonde de mémorisation) ; le bras C : "
         "loupe-13 1983/2011, loupe-02 et loupe-16 refusés à la "
         "compilation (les classes nommées) ; les 21 survivants classés "
         "(12 équivalents prouvés, 3 tuables restants, 6 limites du "
         "harnaïs), le score ajusté 811/820 = 98,9 %. (5) OPT-05 "
         "(pe6iv71fj) : l'édition par hunks −34,3 % au total, −97,7 % à "
         "la réponse (17/18 aux deux modes) ; l'ajout par hunks REFUSÉ en "
         "l'état (0/18 — l'écart nommé) ; l'attente du total FALSIFIÉE "
         "(le matériau domine) ; le double moteur audité sous vrai "
         "QEMU-user (divergence 0 sur 2 041 opérations) ; la mesure M4 : "
         "avant 39,1 s, chaud 6,6 s (l'audit 1/10 vécu), bras C 1,9 s — "
         "chaud/C 3,5× sous ×10."),
    para("LE RAPPORT OPT-05 (pe6iv71fj) — VERBATIM", st_h1),
    para(lit(os.path.join(AT_O, "RAPPORT-OPT05.txt")), st_mono),
    para("LE RAPPORT D'INDÉPENDANCE (peap6ws09) — VERBATIM", st_h1),
    para(lit(os.path.join(AT_I, "RAPPORT-PEAP6WS09.txt")), st_mono),
    para("LA CLASSIFICATION DES 21 SURVIVANTS — VERBATIM (le CSV pièce)", st_h1),
    para(lit(os.path.join(AT_I, "classification-21-survivants.csv")), st_mono),
    para("L'AMENDEMENT DU FORMAT HUNK (la falsification v1, la v2) — VERBATIM", st_h1),
    para(lit(os.path.join(AT_O, "FORMAT-V2-AMENDEMENT.md")), st_mono),
]

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2 * 2.834,
                      rightMargin=2 * 2.834, topMargin=2 * 2.834,
                      bottomMargin=2 * 2.834, title="TRIADE — preuves et "
                      "calculs v0.19.6")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width,
                          doc.height, id="f")])])
doc.build(story)
print("écrit:", OUT)

COVER_HTML = os.path.join(V8, "preuves_v196_cover.html")
with open(COVER_HTML, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
@page { size: A4; margin: 0; }
body { font-family: 'Liberation Serif', serif; margin: 0; }
.cover { width: 210mm; height: 297mm; background: #162032; color: #fff;
  padding: 30mm 24mm; box-sizing: border-box; }
.kicker { color: #7FB4D8; font-family: 'Liberation Sans', sans-serif;
  font-size: 12pt; letter-spacing: 3px; margin-bottom: 18mm; }
h1 { font-size: 34pt; line-height: 1.2; margin: 0 0 8mm 0; font-weight: normal; }
.sub { font-size: 15pt; color: #B9C8D8; margin-bottom: 26mm; }
.rule { border-top: 1px solid #7FB4D8; margin: 10mm 0; }
.meta { font-size: 10.5pt; color: #B9C8D8; line-height: 1.7; }
.label { color: #7FB4D8; font-family: 'Liberation Sans', sans-serif;
  font-size: 10pt; margin-bottom: 4mm; }
</style></head><body><div class="cover">
<div class="kicker">TRIADE</div>
<h1>Preuves et calculs</h1>
<div class="sub">La vague 8 — l'édition v0.19.6</div>
<div class="label">PIÈCES DE LA VAGUE</div>
<div class="meta">
La re-mesure RQ2 : le pointeur seul, m&eacute;diane 1&nbsp;103, z&eacute;ro divergence<br/>
OPT-05 : l'édition par hunks &minus;34,3&nbsp;% (r&eacute;ponse &minus;97,7&nbsp;%), l'ajout refus&eacute; en l'état<br/>
La mesure M4 : 39,1&nbsp;s &rarr; 6,6&nbsp;s, bras C 1,9&nbsp;s, chaud/C 3,5&times; sous &times;10<br/>
L'ind&eacute;pendance par d&eacute;rivation-outill&eacute;e : les 128 constantes conformes, z&eacute;ro divergence<br/>
Les 21 survivants : 12 &eacute;quivalents prouv&eacute;s, le score ajust&eacute; 811/820 = 98,9&nbsp;%
</div>
<div class="rule"></div>
<div class="meta">Document de preuve &middot; s&eacute;rie TRIADE &middot;
&eacute;dition v0.19.6 &middot; 20 novembre 2026</div>
</div></body></html>""")
subprocess.run(["weasyprint", COVER_HTML,
                os.path.join(V8, "preuves_v196_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(os.path.join(V8, "preuves_v196_cover.pdf")).pages[0])
for p_ in PdfReader(OUT).pages:
    w.add_page(p_)
w.add_metadata({"/Title": "TRIADE — preuves et calculs v0.19.6"})
FINAL = os.path.join(V8, "TRIADE_preuves_et_calculs_v0.19.6.pdf")
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(FINAL).pages)} pages)")
