#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_presentation_v196.py — la présentation du 20/11 à l'édition
v0.19.6 (la vague 8) : la cohérence, la gouvernance vécue, l'intégrité
pré-enregistrée, l'indépendance par dérivation-outillée, OPT-05."""
import os
import subprocess

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

REPO = "/home/z/my-project/depot"
V8 = os.path.join(REPO, "scripts", "vague8")
OUT = os.path.join(V8, "presentation_v196_body.pdf")

FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", f"{FDIR}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", f"{FDIR}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", f"{FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", f"{FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/"
                               "DejaVuSansMono.ttf"))

DARK = colors.HexColor("#162032")
st_body = ParagraphStyle("body", fontName="Serif", fontSize=9.8, leading=14.6,
                         alignment=TA_LEFT, spaceAfter=7,
                         textColor=colors.HexColor("#1a1a1a"))
st_h1 = ParagraphStyle("h1", fontName="Serif-Bold", fontSize=16.5, leading=21,
                       textColor=DARK, spaceBefore=13, spaceAfter=8)
st_titre = ParagraphStyle("titre", fontName="Serif-Bold", fontSize=21,
                          leading=26, textColor=DARK, spaceAfter=4)
st_sous = ParagraphStyle("sous", fontName="Sans", fontSize=10.5, leading=15,
                         textColor=colors.HexColor("#555555"), spaceAfter=2)
st_cell = ParagraphStyle("cell", fontName="Serif", fontSize=8.6, leading=11.6,
                         textColor=colors.HexColor("#1a1a1a"))


def para(txt, st=st_body):
    return Paragraph(txt.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;").replace("\n", "<br/>"), st)


def cell(txt):
    return para(txt, st_cell)


story = [
    para("TRIADE — présentation du 20/11", st_titre),
    para("Édition v0.19.6 — la vague 8 : la cohérence des cinq pièces, "
         "la gouvernance vécue, l'intégrité pré-enregistrée, "
         "l'indépendance par dérivation-outillée, OPT-05", st_sous),
    Spacer(1, 8),
    para("LE PROTOCOLE EN TROIS PHRASES", st_h1),
    para("TRIADE fait écrire à un agent IA du code machine natif pur "
         "(x86-64 Windows d'abord, Linux et RISC-V ensuite) sans chaîne "
         "de traduction optimisante ni opaque — la notation est WYSIWYG "
         "par le round-trip : l'agent manipule des intentions (couche "
         "I), une carte de balises signée et chiffrée (couche C), et ne "
         "livre que le binaire scellé (couche B). Onze règles non "
         "négociables, la vérification avant tout écrit (oracle "
         "différentiel, round-trip WYSIWYG, vecteurs dorés), la "
         "cristallisation au bout de dix vérifications. L'étude de cas "
         "unique est close et la vague 8 exécutée : les cinq documents "
         "unifiés, la gouvernance à l'état vécu, le dépôt public et le "
         "concept DOI 10.5281/zenodo.24367343 résolvant sur la version "
         "courante."),
    para("LA VAGUE 8 — LES CINQ POINTS", st_h1),
    para("(1) LA COHÉRENCE DES CINQ PIÈCES : les macros régénérées des "
         "journaux vivants (la plage D1–D223, les comptes exacts — "
         "jamais tapés), les DOI réconciliés (le concept résolvant sur "
         "la courante partout, les versions datées 24367344/24379173/"
         "24382460 nommées comme records), la probabilité du tirage "
         "corrigée à 1/16 (quatre tirages indépendants à une demi "
         "chacun), la valeur d'avant périmée REMPLACÉE par la valeur "
         "mesurée du manuscrit (39,3/39,2 s, n=2) puis re-mesurée à la "
         "session (39,1 s médiane n=5), le linter inter-pièces étendu aux "
         "nouvelles valeurs. (2) LA GOUVERNANCE À L'ÉTAT VÉCU (D223) : "
         "la cérémonie de séquestre D183 VÉCUE de bout en bout le "
         "19/11 — les sept gestes accomplis, la reconstitution à froid "
         "prouvée deux fois, la phrase TOURNÉE et l'ancienne REFUSÉE ; "
         "D81 amendée (le séquestre Shamir 5/3 la garde active) ; le "
         "dépôt PUBLIC (D220) ; la rotation vérifiée (le re-scan trié : "
         "aucune fuite réelle) — la spécification v0.15.5 et le Livre "
         "du Coffre v1.4 à l'état vécu, AUCUNE règle modifiée. (3) "
         "L'INTÉGRITÉ PRÉ-ENREGISTRÉE : H5 en DEUX VERDICTS DISTINCTS "
         "ET DATÉS (H5-D204 réfutée ×23,9 mesurée le 16/11 ; "
         "H5-amendée-OPT04 tenue ×3,0 le 19/11, l'amendement explicite "
         "du maître — jamais fusionnés) ; N=7 réconcilié (la lecture "
         "livraison tenue, la lecture instrumentation nommée relaxation "
         "avec son amendement) ; H6 au verdict brut affiché (3 échappés "
         "côté T, 0 côté C) à côté de l'attribution (14 VERT 0 ROUGE, "
         "la pièce jamais fautive) ; H7 à la randomisation stratifiée "
         "pré-enregistrée pour la prochaine campagne ; l'abstract en un "
         "seul paragraphe cohérent (la clôture 30 000 traces zéro "
         "divergence en premier, le gap 10 000 traces comme histoire "
         "datée) ; §5 à TLC/Apalache (D200) avec la déviation restante "
         "nommée. (4) L'INDÉPENDANCE PAR DÉRIVATION-OUTILLÉE : le "
         "protocole amendé — la récitation pure demeure la sonde de "
         "mémorisation (2/64 + 2/64 : les ancreurs seuls), le test "
         "d'indépendance devient LA DÉRIVATION OUTILLÉE : la seconde "
         "famille (Qwen2.5-Coder-1.5B, le même snapshot que la vague 7) "
         "ÉCRIT LE CODE qui dérive T[64] (RFC 1321) et K[64] (FIPS "
         "180-4) des définitions mathématiques seules — LES 128 "
         "CONSTANTES CONFORMES aux définitions ET au plan, zéro "
         "divergence ; le bras C aux TROIS contrats : loupe-13 "
         "1983/2011 (la classe de bord Q2 reproduite), loupe-02 et "
         "loupe-16 refusés à la compilation (l'ordre de déclaration, "
         "le type de retour — les classes nommées, les sources justes "
         "à la lecture) ; les 21 survivants classés : 12 ÉQUIVALENTS "
         "PROUVÉS (la preuve mécanique par classe), 3 tuables "
         "restants, 6 limites du harnaïs — le score ajusté 811/820 = "
         "98,9 % à côté du brut 811/832 = 97,5 %. (5) OPT-05 : "
         "L'ÉDITION PAR HUNKS mesurée verte (le total 3 732 → 2 452 = "
         "−34,3 %, la réponse 1 726 → 40 = −97,7 %, 17/18 aux deux "
         "modes, les quatre refus nommés autotestés) ; L'AJOUT PAR "
         "HUNKS REFUSÉ EN L'ÉTAT (0/18 — le modèle re-dumppe le "
         "contexte, l'écart nommé à sa classe) ; L'ATTENTE DU TOTAL "
         "FALSIFIÉE et consignée (le matériau domine : le hunk achète "
         "la réponse, pas la lecture) ; la re-mesure RQ2 du pointeur "
         "seul : médiane 1 103 [808..1502], réponse 52, 18/18 "
         "conformes — reproductible à l'identique de la campagne "
         "OPT-04 ; le double moteur audité sous VRAI QEMU-user : "
         "divergence 0 sur 2 041 opérations ; la mesure M4 : avant "
         "39,1 s, chaud 6,6 s (L'AUDIT 1/10 VÉCU au run 4), bras C "
         "1,9 s — chaud/C 3,5× SOUS ×10."),
    para("LA TABLE DES STATUTS — LES HYPOTHÈSES", st_h1),
    Table(
        [[cell("Hypothèse"), cell("Énoncé"), cell("Verdict")],
         [cell("H1"), cell("la notation tient le round-trip à 100 %"),
          cell("tenue")],
         [cell("H3"), cell("le bras compilé plus sobre en tokens"),
          cell("réfutée (×1,27 l'inverse)")],
         [cell("H5-D204"), cell("la vérification dans un facteur ×10 "
                               "(le 16/11, mesurée)"),
          cell("RÉFUTÉE (×23,9, n=1 — consignée comme mesurée et datée)")],
         [cell("H5-amendée-OPT04"), cell("la vérification dans un facteur "
                                         "×10 (le 19/11, l'amendement du "
                                         "maître)"),
          cell("TENUE (×3,0 ; re-mesurée ×3,5 à la vague 8 — les deux "
               "verdicts DISTINCTS, jamais fusionnés)")],
         [cell("H6"), cell("le taux d'échappées kit-side dans un facteur "
                          "2 entre bras"),
          cell("tenue PAR ATTRIBUTION (le brut affiché : 3 côté T, 0 "
               "côté C — la pièce jamais fautive, 14 VERT 0 ROUGE)")],
         [cell("H7"), cell("l'ordre randomisé n'affecte aucune métrique"),
          cell("non testée (aucun contraste — la randomisation "
               "stratifiée pré-enregistrée pour la prochaine)")],
         [cell("H8"), cell("la spirale corrective > 50 % des tokens"),
          cell("réfutée (51/39/9 % — la spirale déclina)")]],
        colWidths=[38, 168, 250]),
    Spacer(1, 6),
    para("L'ÉTAT DES ÉDITIONS — le manuscrit v0.19.6 (la cohérence et "
         "l'intégrité pré-enregistrée, l'abstract réécrit), la "
         "spécification v0.15.5 (l'état vécu de la gouvernance, aucune "
         "règle modifiée), le Livre du Coffre v1.4 (le runbook D183 au "
         "statut VÉCU, quatorze arbres, la matrice public + Zenodo), "
         "les preuves v0.19.6 (les pièces verbatim de la vague), la "
         "présentation du 20/11 à l'état exact. LA GOUVERNANCE VÉCUE : "
         "le séquestre Shamir 5/3 la garde active, la phrase TOURNÉE "
         "et l'ancienne REFUSÉE, le dépôt PUBLIC (github.com/"
         "alexisfrlopez-debug/triade), le concept DOI "
         "10.5281/zenodo.24367343 résolvant sur la version courante — "
         "la publication de la v0.19.6 AU GESTE DU MAÎTRE (jamais un "
         "DOI minté sans commande explicite)."),
]

# le style de la table
story_table_style = TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B9C8D8")),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EFF5")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
])
for el in story:
    if isinstance(el, Table):
        el.setStyle(story_table_style)

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2 * 2.834,
                      rightMargin=2 * 2.834, topMargin=2 * 2.834,
                      bottomMargin=2 * 2.834, title="TRIADE — présentation "
                      "du 20/11, édition v0.19.6")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width,
                          doc.height, id="f")])])
doc.build(story)
print("écrit:", OUT)

COVER_HTML = os.path.join(V8, "presentation_v196_cover.html")
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
</style></head><body><div class="cover">
<div class="kicker">TRIADE</div>
<h1>Pr&eacute;sentation</h1>
<div class="sub">La vague 8 — l'édition v0.19.6 &middot; 20 novembre 2026</div>
<div class="meta">
La coh&eacute;rence des cinq pi&egrave;ces &middot; les macros r&eacute;g&eacute;n&eacute;r&eacute;es &middot; les DOI r&eacute;concili&eacute;s<br/>
La gouvernance v&eacute;cue (D223) &middot; le s&eacute;questre 5/3 la garde active &middot; le d&eacute;p&ocirc;t public<br/>
L'ind&eacute;pendance par d&eacute;rivation-outill&eacute;e &middot; les 128 constantes conformes &middot; 811/820 ajust&eacute;<br/>
OPT-05 &middot; l'édition par hunks &minus;34,3&nbsp;% &middot; M4 39,1&nbsp;s &rarr; 6,6&nbsp;s &middot; chaud/C 3,5&times;
</div>
<div class="rule"></div>
<div class="meta">S&eacute;rie TRIADE &middot; &eacute;dition v0.19.6 &middot; le concept DOI 10.5281/zenodo.24367343</div>
</div></body></html>""")
subprocess.run(["weasyprint", COVER_HTML,
                os.path.join(V8, "presentation_v196_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(os.path.join(V8, "presentation_v196_cover.pdf")).pages[0])
for p_ in PdfReader(OUT).pages:
    w.add_page(p_)
w.add_metadata({"/Title": "TRIADE — présentation du 20/11, édition v0.19.6"})
FINAL = os.path.join(V8, "TRIADE_presentation_20261120_v196.pdf")
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(FINAL).pages)} pages)")
