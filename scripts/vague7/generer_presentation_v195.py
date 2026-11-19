#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_presentation_v195.py — le document de présentation du 20/11,
l'édition v0.19.5 (la clôture de la vague 7 — l'instruction 1c4sokpii).
La structure hérite de la v0.19.4 ; les chiffres sont ceux de la session,
lus des rapports de l'atelier. Corps ReportLab, couverture weasyprint,
fusion pypdf."""
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

V7 = "/home/z/my-project/depot/scripts/vague7"
OUT = os.path.join(V7, "presentation_v195_body.pdf")

FDIR = "/usr/share/fonts/truetype/liberation"
for nom, fich in [("Serif", "LiberationSerif-Regular.ttf"),
                  ("Serif-Bold", "LiberationSerif-Bold.ttf"),
                  ("Serif-Italic", "LiberationSerif-Italic.ttf"),
                  ("Sans", "LiberationSans-Regular.ttf"),
                  ("Sans-Bold", "LiberationSans-Bold.ttf"),
                  ("Mono", "LiberationMono-Regular.ttf")]:
    pdfmetrics.registerFont(TTFont(nom, f"{FDIR}/{fich}"))

DARK = colors.HexColor("#162032")
ACCENT = colors.HexColor("#4A90C4")
st_body = ParagraphStyle("body", fontName="Serif", fontSize=9.8,
                         leading=14.6, alignment=TA_LEFT, spaceAfter=7,
                         textColor=colors.HexColor("#1a1a1a"))
st_h1 = ParagraphStyle("h1", fontName="Serif-Bold", fontSize=16.5,
                       leading=21, textColor=DARK, spaceBefore=14,
                       spaceAfter=8)
st_titre = ParagraphStyle("titre", fontName="Serif-Bold", fontSize=21,
                          leading=26, textColor=DARK, spaceAfter=4)
st_sous = ParagraphStyle("sous", fontName="Sans", fontSize=10.5, leading=15,
                         textColor=colors.HexColor("#555555"), spaceAfter=2)
st_cell = ParagraphStyle("cell", fontName="Sans", fontSize=8.6, leading=12)


def para(txt, st=st_body):
    return Paragraph(txt.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;").replace("\n", "<br/>"), st)


def cell(txt):
    return para(txt, st_cell)


story = [
    para("TRIADE — présentation du 20/11", st_titre),
    para("Édition v0.19.5 — la clôture de la vague 7 (l'instruction "
         "1c4sokpii, la vague du 19/11, la cinquième et dernière)",
         st_sous),
    Spacer(1, 8),
    para("LE PROTOCOLE EN TROIS PHRASES", st_h1),
    para("TRIADE fait écrire à un agent IA du code machine natif pur "
         "(x86-64 Windows d'abord, Linux et RISC-V ensuite) sans chaîne "
         "de traduction optimisante ni opaque — la notation est WYSIWYG "
         "par le round-trip : l'agent manipule des "
         "intentions (couche I), une carte de balises signée et chiffrée "
         "(couche C), et ne livre que le binaire scellé (couche B). Onze "
         "règles non négociables, la vérification avant tout écrit "
         "(oracle différentiel, round-trip WYSIWYG, vecteurs dorés), la "
         "cristallisation au bout de dix vérifications. L'étude de cas "
         "unique est close : sept unités aux deux bras, les verdicts "
         "explicites, la vague 7 entière exécutée, le dépôt public et "
         "le DOI Zenodo vivant."),
    para("LA CLÔTURE DE LA VAGUE 7 — LES QUATRE POINTS", st_h1),
    para("(1) LE PLAN D210 À SON TERME : le critère d'échantillon tenu "
         "à N = 7 SANS NOUVEAU TIRAGE — sept unités entièrement livrées "
         "aux deux bras (app, loupe-01/02/05/08/13/16), le comptage lu "
         "du registre ; la séquence épuisée à la cap, l'amendement "
         "conditionnel jamais déclenché. (2) L'INDÉPENDANCE "
         "INTER-FAMILLES : LE GAP NOMMÉ, jamais simulé — la "
         "confrontation math↔plan tenue à zéro divergence AVANT toute "
         "génération ; la seconde famille locale open-weights "
         "(Qwen2.5-Coder-1.5B, 1,54 G paramètres, CPU) récite 0/64 + "
         "0/64 à la pure et COPIE à la correction — le gap est la "
         "capacité du local disponible ; le bras C généré (le contrat "
         "loupe-13 → gcc -O2) passe l'épreuve POSIX à 1984/2011 — le "
         "second gap nommé (la plage restante trop courte). "
         "(3) LA BATTERIE D'INJECTION DE FAUTES : 811/832 TUÉS "
         "(97,5 %) — 83,4 % → 93,3 % → 97,5 % ; la console v0.14.0 "
         "reproduite à l'identique d'abord (la graine 20261111), 35 "
         "tués PAR L'INJECTION, LE RESTE DE 21 NOMMÉ à treize familles "
         "de causes — AUCUN tueur affaibli. (4) LE PAQUET "
         "D'ÉVALUATION : la reproduction en UNE COMMANDE (sept étapes "
         "aux graines consignées, verte de bout en bout), la grille "
         "codée des 11 défauts (F1×1/F2×1/F3×3/F5×3/L3×3), le second "
         "annotateur à recruter (κ ≥ 0,61 pré-enregistré), le "
         "calculateur κ autotesté 3/3."),
    para("LES CANONS RECONDUITS DE LA VAGUE : le pointeur seul au "
         "format de réponse de localiser (−35,7 % au total, −93,3 % à "
         "la réponse, zéro divergence 18/18, l'expansion côté client à "
         "quatre refus nommés) ; le ratio M4 — l'avant 39,7 s contre "
         "le bras C 2,2 s = 17,9×, le régime 6,8 s = 3,0× SOUS ×10 : "
         "H5 TENUE depuis OPT-04 (la falsification D204 demeure "
         "consignée) ; la pile mémo v2 + double moteur (divergence 0 "
         "sur 2 041 opérations) ; les 24 consoles d'oracles capturées "
         "identiques ligne à ligne aux originales — aucune graine "
         "supprimée, aucun vecteur réduit, aucune vérification retirée."),
    para("LA TABLE DES STATUTS — LES HYPOTHÈSES", st_h1),
    Table(
        [[cell("Hypothèse"), cell("Énoncé"), cell("Verdict")],
         [cell("H1"), cell("la notation tient le round-trip à 100 %"),
          cell("tenue")],
         [cell("H3"), cell("le bras compilé plus sobre en tokens"),
          cell("réfutée (×1,27 l'inverse)")],
         [cell("H4-D204"), cell("les cérémonies humaines plus longues à T"),
          cell("tenue (×6,1)")],
         [cell("H5"), cell("la vérification dans un facteur ×10"),
          cell("TENUE depuis OPT-04 (×3,0 ; falsifiée à ×23,9 en D204 — "
               "l'amendement explicite du maître, les deux consignés)")],
         [cell("H6"), cell("le taux d'échappés dans un facteur ×2"),
          cell("tenue par attribution")],
         [cell("H7"), cell("l'effet d'ordre des formats"),
          cell("non testée (aucun contraste)")],
         [cell("H8"), cell("la spirale corrective au chemin chaud"),
          cell("réfutée (51/39/9 %)")]],
        colWidths=[38, 205, 205]),
    Spacer(1, 6),
    para("L'ÉTAT DES ÉDITIONS", st_h1),
    Table(
        [[cell("Pièce"), cell("Édition"), cell("Ce qu'elle porte")],
         [cell("Le manuscrit"), cell("v0.19.5"),
          cell("La clôture de la vague 7 : N = 7 sans tirage, la "
               "batterie d'injection (97,5 %), le gap nommé, le paquet "
               "d'évaluation — et la gouvernance portée à l'état vécu "
               "(D183 vécue, D220 public)")],
         [cell("La spécification"), cell("v0.15.4"),
          cell("Le pointeur seul — une règle ADDITIVE à localiser, "
               "aucune règle modifiée (D222) ; INCHANGÉE par la "
               "v0.19.5 (aucune règle ne bouge)")],
         [cell("Le Livre du Coffre"), cell("v1.3"),
          cell("INCHANGÉ (aucun geste de cérémonie ne bouge)")],
         [cell("Les preuves et calculs"), cell("v0.19.5"),
          cell("Les pièces 1c4sokpii verbatim : le rapport "
               "d'instruction, l'indépendance inter-familles, le rejeu "
               "des fautes")],
         [cell("La présentation"), cell("20/11 (v0.19.5)"),
          cell("Le présent document.")]],
        colWidths=[85, 80, 283]),
    Spacer(1, 6),
    para("LA GOUVERNANCE À L'ÉTAT VÉCU : la cérémonie D183 VÉCUE de bout "
         "en bout le 19/11 (cinq parts à seuil trois, la reconstitution "
         "à froid prouvée deux fois, la phrase commise tournée et "
         "l'ancienne refusée, le re-scan de l'historique complet trié — "
         "dix constats, aucun jeton réel commis). LE DÉPÔT : PUBLIC "
         "(D220) ; le DOI Zenodo vivant : 10.5281/zenodo.24367344. "
         "github.com/alexisfrlopez-debug/triade"),
]

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2 * 2.834,
                      rightMargin=2 * 2.834, topMargin=2 * 2.834,
                      bottomMargin=2 * 2.834,
                      title="TRIADE — présentation du 20/11 (v0.19.5)")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width,
                          doc.height, id="f")])])
doc.build(story)
print("écrit:", OUT)

# ---- la couverture ----------------------------------------------------------
COVER_HTML = os.path.join(V7, "presentation_v195_cover.html")
with open(COVER_HTML, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
@page { size: A4; margin: 0; }
body { font-family: 'Liberation Serif', serif; margin: 0; }
.cover { width: 210mm; height: 297mm; background: #162032; color: #fff;
  padding: 30mm 24mm; box-sizing: border-box; }
.kicker { color: #7FB4D8; font-family: 'Liberation Sans', sans-serif;
  font-size: 12pt; letter-spacing: 3px; margin-bottom: 18mm; }
h1 { font-size: 30pt; line-height: 1.25; margin: 0 0 8mm 0; font-weight: normal; }
.sub { font-size: 14pt; color: #B9C8D8; margin-bottom: 24mm; }
.rule { border-top: 1px solid #7FB4D8; margin: 10mm 0; }
.meta { font-size: 10.5pt; color: #B9C8D8; line-height: 1.7; }
.label { color: #7FB4D8; font-family: 'Liberation Sans', sans-serif;
  font-size: 10pt; margin-bottom: 4mm; }
</style></head><body><div class="cover">
<div class="kicker">TRIADE</div>
<h1>La clôture de la vague 7</h1>
<div class="sub">L'édition v0.19.5 — la présentation du 20 novembre 2026</div>
<div class="label">LES QUATRE POINTS DE LA SESSION 1C4SOKPII</div>
<div class="meta">
Le plan D210 à son terme : N = 7 sans nouveau tirage<br/>
L'indépendance inter-familles : le gap nommé, jamais simulé<br/>
La batterie d'injection : 811/832 (97,5 %), le reste de 21 nommé<br/>
Le paquet d'évaluation : une commande, la grille, le protocole &kappa;
</div>
<div class="rule"></div>
<div class="meta">Pr&eacute;sentation de synth&egrave;se &middot; s&eacute;rie TRIADE &middot;
&eacute;dition v0.19.5 &middot; 20 novembre 2026</div>
</div></body></html>""")
subprocess.run(["weasyprint", COVER_HTML,
                os.path.join(V7, "presentation_v195_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(os.path.join(V7, "presentation_v195_cover.pdf")).pages[0])
for p_ in PdfReader(OUT).pages:
    w.add_page(p_)
w.add_metadata({"/Title": "TRIADE — présentation du 20/11 (v0.19.5)"})
FINAL = os.path.join(V7, "TRIADE_presentation_20261120_v195.pdf")
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(FINAL).pages)} pages)")
