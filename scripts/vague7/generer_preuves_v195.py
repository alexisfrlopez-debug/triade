#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_preuves_v195.py — le document TRIADE_preuves_et_calculs_v0.19.5.pdf
(ReportLab) : les pièces de la session 1c4sokpii — LA CLÔTURE DE LA VAGUE 7.
Les pièces verbatim (le rapport d'instruction, le rapport d'indépendance
inter-familles, le rapport du rejeu des fautes) sont LUES de l'atelier —
jamais retapées. Le corps ReportLab, la couverture weasyprint, la fusion
pypdf (le montage de la v0.19.3 reconduit)."""
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
V7 = os.path.join(REPO, "scripts", "vague7")
OUT = os.path.join(V7, "preuves_v195_body.pdf")
AT = os.path.join(REPO, "atelier-plan-final-1c4sokpii")

FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", f"{FDIR}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", f"{FDIR}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Italic", f"{FDIR}/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans", f"{FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", f"{FDIR}/LiberationSans-Bold.ttf"))
# le mono est DejaVu Sans Mono : le rapport d'indépendance porte ∛ (U+221B)
# et ᵢ (U+1D62) — absents de Liberation Mono ; le texte verbatim demeure
# octet-identique, seul le corps de rendu change.
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


def lit(nom):
    with open(os.path.join(AT, nom), encoding="utf-8") as f:
        return f.read()


story = [
    para("TRIADE — preuves et calculs", st_titre),
    para("Édition v0.19.5 — la clôture de la vague 7 "
         "(l'instruction 1c4sokpii, la vague du 19/11, la cinquième et "
         "dernière)", st_sous),
    Spacer(1, 6),
    para("Le présent document porte les pièces de la session : le plan "
         "D210 à son terme (le critère d'échantillon tenu à N = 7 sans "
         "nouveau tirage), l'indépendance inter-familles au gap nommé "
         "(jamais simulé), le tri des 56 survivants et la batterie "
         "d'injection de fautes (811/832, 97,5 %), le paquet "
         "d'évaluation (la reproduction en une commande, la grille "
         "codée, le protocole du second annotateur, le κ autotesté). "
         "Les pièces verbatim sont lues de l'atelier — jamais retapées."),
    para("LA SESSION EN UNE PAGE", st_h1),
    para("(1) LE PLAN D210 À SON TERME : le comptage LU DU REGISTRE "
         "(livraisons.csv, 29 lignes, jamais tapé) — SEPT unités "
         "entièrement livrées aux deux bras (app, loupe-01/02/05/08/13/"
         "16), N = 7 ≥ 6 : TENU SANS NOUVEAU TIRAGE ; la séquence D210 "
         "épuisée à la cap M1, l'amendement conditionnel jamais "
         "déclenché. (2) L'INDÉPENDANCE INTER-FAMILLES : la voie "
         "prescrite vécue — Qwen2.5-Coder-1.5B-Instruct open-weights "
         "local (1,54 G paramètres, CPU, 3 Go de RAM au bac : le 7B n'y "
         "tient pas) ; la confrontation math↔plan TENUE à zéro "
         "divergence AVANT toute génération (T et K égales aux "
         "définitions RFC 1321 / FIPS 180-4) ; la récitation pure "
         "0/64 + 0/64 (le modèle répète les ancres puis dérive), les "
         "rondes de correction 64/64 — LA COPIE, JAMAIS "
         "L'INDÉPENDANCE ; LE GAP NOMMÉ : la capacité du local "
         "disponible ; le bras C (le contrat loupe-13 mot pour mot → "
         "gcc -O2 → l'épreuve POSIX) : 1984/2011 — le second gap nommé "
         "(la plage restante trop courte rend -5 au lieu du -1 du "
         "contrat). (3) LE TRI DES 56 SURVIVANTS + LES SHIMS "
         "D'INJECTION : le rejeu reproduit la console v0.14.0 à "
         "l'identique (776/832, la graine 20261111), les 56 triés au "
         "niveau instruction (46 immédiats, 8 registres, 2 opérandes), "
         "la batterie K4 de seize scénarios — 35 tués PAR L'INJECTION "
         "(83,4 % → 93,3 % → 97,5 %), LE RESTE DE 21 NOMMÉ à treize "
         "familles de causes — AUCUN tueur affaibli. (4) LE PAQUET "
         "D'ÉVALUATION : la reproduction en une commande (sept étapes "
         "aux graines consignées, VERTE de bout en bout), la grille "
         "codée (les 11 défauts en F1×1/F2×1/F3×3/F5×3/L3×3), le "
         "second annotateur à recruter (le protocole écrit, κ ≥ 0,61 "
         "pré-enregistré, aucune annotation inventée), le κ autotesté "
         "3/3."),
    para("LE RAPPORT DE L'INSTRUCTION 1C4SOKPII — VERBATIM", st_h1),
    para(lit("RAPPORT-1C4SOKPII.txt"), st_mono),
    para("LE RAPPORT D'INDÉPENDANCE INTER-FAMILLES — VERBATIM", st_h1),
    para(lit("RAPPORT-INDEPENDANCE-FAMILLES.txt"), st_mono),
    para("LE RAPPORT DU REJEU DES FAUTES — VERBATIM", st_h1),
    para(lit("rejeu_fautes_rapport.txt"), st_mono),
]

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2 * 2.834,
                      rightMargin=2 * 2.834, topMargin=2 * 2.834,
                      bottomMargin=2 * 2.834, title="TRIADE — preuves et "
                      "calculs v0.19.5")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width,
                          doc.height, id="f")])])
doc.build(story)
print("écrit:", OUT)

# ---- la couverture (le montage de la v0.19.3 reconduit) --------------------
COVER_HTML = os.path.join(V7, "preuves_v195_cover.html")
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
<div class="sub">La clôture de la vague 7 — l'édition v0.19.5</div>
<div class="label">PIÈCES DE LA SESSION 1C4SOKPII</div>
<div class="meta">
Le plan D210 à son terme : N = 7 sans nouveau tirage, l'amendement jamais déclenché<br/>
L'indépendance inter-familles : le gap nommé sur pièces, jamais simulé<br/>
La batterie d'injection de fautes : 811/832 (97,5 %), le reste de 21 nommé<br/>
Le paquet d'évaluation : la reproduction en une commande, la grille codée, κ autotesté
</div>
<div class="rule"></div>
<div class="meta">Document de preuve &middot; s&eacute;rie TRIADE &middot;
&eacute;dition v0.19.5 &middot; 20 novembre 2026</div>
</div></body></html>""")
subprocess.run(["weasyprint", COVER_HTML,
                os.path.join(V7, "preuves_v195_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(os.path.join(V7, "preuves_v195_cover.pdf")).pages[0])
for p_ in PdfReader(OUT).pages:
    w.add_page(p_)
w.add_metadata({"/Title": "TRIADE — preuves et calculs v0.19.5"})
FINAL = os.path.join(V7, "TRIADE_preuves_et_calculs_v0.19.5.pdf")
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(FINAL).pages)} pages)")
