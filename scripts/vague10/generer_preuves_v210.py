#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_preuves_v210.py — le document TRIADE_preuves_et_calculs_v0.21.0.pdf
(ReportLab + weasyprint) : les pièces de la vague 10 — la re-mesure SSE2
à la faute nommée, la fenêtre de relecture, les gardes et la
non-interférence étendue, le bras C+G. Les pièces verbatim sont LUES des
ateliers — jamais retapées."""
import pathlib
import subprocess

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer)

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "scripts" / "vague10"
OUT = ICI / "preuves_v210_body.pdf"
SSE2 = REPO / "atelier-remesure-sse2-8z4hj76w4"
FEN = REPO / "atelier-fenetre-mqf258e4l"
GAR = REPO / "atelier-gardes-ifqm1d1i4"
CG = REPO / "atelier-cg-3a91o5whb"

FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", f"{FDIR}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", f"{FDIR}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/"
                               "DejaVuSansMono.ttf"))

DARK = colors.HexColor("#162032")
st_body = ParagraphStyle("body", fontName="Serif", fontSize=9.6, leading=14.2,
                         alignment=TA_LEFT, spaceAfter=7,
                         textColor=colors.HexColor("#1a1a1a"))
st_h1 = ParagraphStyle("h1", fontName="Serif-Bold", fontSize=15.5, leading=20,
                      textColor=DARK, spaceBefore=14, spaceAfter=8)
st_mono = ParagraphStyle("mono", fontName="Mono", fontSize=6.3, leading=8.2,
                        textColor=colors.HexColor("#222222"))
st_titre = ParagraphStyle("titre", fontName="Serif-Bold", fontSize=21,
                          leading=26, textColor=DARK, spaceAfter=4)
st_sous = ParagraphStyle("sous", fontName="Serif", fontSize=11.6, leading=15.6,
                         textColor=colors.HexColor("#444444"))


def para(txt, st):
    return Paragraph(txt.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;"), st)


def lit(chemin, max_chars=2600):
    t = pathlib.Path(chemin).read_text(encoding="utf-8", errors="replace")
    return t[:max_chars]


story = [
    para("TRIADE — preuves et calculs", st_titre),
    para("Édition v0.21.0 — la vague 10 : la re-mesure SSE2 à la faute "
         "nommée et aux baselines équitables, la fenêtre de relecture de "
         "l'édition, les gardes runtime et la non-interférence étendue, "
         "le troisième bras C+G isolant l'effet notation", st_sous),
    Spacer(1, 6),
    para("Le présent document porte les pièces de la vague 10 : les six "
         "instructions exécutées aux plans gelés d'abord (les empreintes "
         "consignées AVANT la première donnée, le commit 951e79b), la "
         "faute SSE2 nommée et corrigée sur pièces (la différentielle "
         "plantée qui la voit, la confrontation qui ne pouvait pas), la "
         "fenêtre de relecture mesurée avant/après à la même graine, "
         "les gardes prouvées et falsifiées par accès, la "
         "non-interférence étendue sous l'hypothèse du lifter vérifiée "
         "par le round-trip, le bras C+G mesuré aux trois bras sur la "
         "même machine. Les pièces verbatim sont lues des ateliers — "
         "jamais retapées. Le concept DOI 10.5281/zenodo.24367343 "
         "résout sur la version courante (le dépôt public D220).", st_body),
    para("LA VAGUE 10 EN UNE PAGE", st_h1),
    para("(1) 8z4hj76w4 — LA FAUTE SSE2 NOMMÉE ET LA RE-MESURE : la "
         "variante de la vague 9 diffuser le motif de QUATRE octets au "
         "lieu du premier (406/564 occurrences plantées manquées — "
         "l'épreuve de la vague 9 n'exerçait AUCUNE occurrence, l'écart "
         "de l'épreuve nommé) ; la correction v2 (zéro divergence aux 88 "
         "vecteurs, le contrôle négatif attrapé) ; les instructions (le "
         "compilateur n'ÉMET AUCUN SIMD sur la source naturelle — la "
         "baseline vectorisée du compilateur n'existe pas) ; le CPUID "
         "HISSÉ (45 → 34,4 instructions/bloc) ; le temps réel (la v2 "
         "833 cycles aux 4096/16 — DANS LA CLASSE des primitives SIMD de "
         "la libc : l'idiome memchr 561, memmem 933, gcc-O2 16 040) ; "
         "UNE SEULE MACHINE (l'écart nommé). (2) mqf258e4l (OPT-10) — LA "
         "FENÊTRE : n=18, la même graine ; l'AVANT 2 452 reproduit (+1 "
         "refus nommé), l'APRÈS 1 146 (−53,3 %), le matériau 1 684 → "
         "239, LA PROSE DOMINE désormais ; les quatre refus du pointeur "
         "re-roulés 5/5 VERT. (3) ifqm1d1i4 — LES GARDES ET LA "
         "NON-INTERFÉRENCE : 2 098 = 100 % déchargé-ou-gardé (34 LEA "
         "relationnels + 58 gardes prouvées UNSAT et falsifiées 58/58) ; "
         "la non-interférence étendue à x25519 et md5 : 13 blocs, sept "
         "familles, sous l'hypothèse de soundness du lifter vérifiée "
         "par le round-trip 13/13. (4) 3a91o5whb — LE BRAS C+G : la "
         "gouvernance complète reçue par le C gcc-O2 ; la mesure aux "
         "trois bras (T 39,24 · C 1,95 · C+G 2,16) — l'effet notation "
         "isolé 37,07 s/session (18,1×), l'effet gouvernance 215 ms "
         "(1,11×) ; loupe-05 close sur son rouge à la cap (trois "
         "échappées nommées) ; la réconciliation zéro écart + le "
         "contrôle négatif attrapé et attribué. (5) 1e2vq7rtw — LA "
         "RÉCONCILIATION : l'abstract aligné (811/817 = 99,3 %), le "
         "ratio M4 recalculé des médianes non arrondies (3,4×), l'axe "
         "ajouter au coût opérationnel. (6) rgttyp8bj — LE REGISTRE "
         "NEUTRE : le lexique ritualiste remplacé, aucune valeur "
         "modifiée hors la réconciliation, la transparence intacte ; "
         "CF3 mécanisé 14/14 RECONDUIT (l'audit re-roulé vert, "
         "identique au record — la vague 9 tenue).",
         st_body),
    Spacer(1, 10),
]

# ---- les pièces verbatim ----------------------------------------------
story += [para("LA PIÈCE 1 — LA FAUTE SSE2 ET LA RE-MESURE AUX INSTRUCTIONS "
               "(le rapport, verbatim)", st_h1),
          para(lit(SSE2 / "rapport-remesure.txt"), st_mono)]
story += [para("LA PIÈCE 2 — LE TEMPS RÉEL SUR MATÉRIEL (le rapport, "
               "verbatim)", st_h1),
          para(lit(SSE2 / "rapport-temps-reel.txt"), st_mono)]
story += [para("LA PIÈCE 3 — LA FENÊTRE DE RELECTURE (le rapport, verbatim)",
               st_h1),
          para(lit(FEN / "rapport-fenetre.txt"), st_mono)]
story += [para("LA PIÈCE 4 — LES GARDES (le rapport, verbatim)", st_h1),
          para(lit(GAR / "rapport-gardes.txt"), st_mono)]
story += [para("LA PIÈCE 5 — LA NON-INTERFÉRENCE ÉTENDUE (le rapport, "
               "verbatim)", st_h1),
          para(lit(GAR / "rapport-non-interference-v210.txt", 4400), st_mono)]
story += [para("LA PIÈCE 6 — LE BRAS C+G : LA CONSTRUCTION (le rapport, "
               "verbatim)", st_h1),
          para(lit(CG / "rapport-cg-construction.txt"), st_mono)]
story += [para("LA PIÈCE 7 — LE BRAS C+G : LA MESURE M4 (le rapport, "
               "verbatim)", st_h1),
          para(lit(CG / "rapport-cg-m4.txt"), st_mono)]
story += [para("LA PIÈCE 8 — LE BRAS C+G : LA RÉCONCILIATION (le rapport, "
               "verbatim — le contrôle négatif inclus)", st_h1),
          para(lit(CG / "rapport-cg-reconciliation.txt"), st_mono)]

# ---- la table des empreintes des pièces de contenu ----------------------
import hashlib  # noqa: E402

EMP = {
    "TRIADE_manuscrit_v0.21.0.pdf": REPO / "edition-v0210" / "main.pdf",
    "Protocole_TRIADE_v0.15.6_Specification.pdf":
        REPO / "scripts" / "spec_v156" / "main.pdf",
    "Livre_du_Coffre_TRIADE_CF1-CF3_v1.5.pdf":
        REPO / "scripts" / "livre_v15" / "final.pdf",
    "rapport-remesure.txt": SSE2 / "rapport-remesure.txt",
    "rapport-temps-reel.txt": SSE2 / "rapport-temps-reel.txt",
    "rapport-fenetre.txt": FEN / "rapport-fenetre.txt",
    "rapport-gardes.txt": GAR / "rapport-gardes.txt",
    "rapport-non-interference-v210.txt":
        GAR / "rapport-non-interference-v210.txt",
    "rapport-cg-reconciliation.txt": CG / "rapport-cg-reconciliation.txt",
}
lignes = ["LA TABLE DES EMPREINTES (les pièces de contenu gravées — la "
          "convention : le document ne porte pas son propre sha-256)"]
for nom, ch in EMP.items():
    h = hashlib.sha256(ch.read_bytes()).hexdigest()
    lignes.append(f"{h}  {nom}")
story += [para("LA TABLE DES EMPREINTES", st_h1),
          para("\n".join(lignes), st_mono)]


def _canard(c, d):
    return ""


doc = BaseDocTemplate(str(OUT), pagesize=A4,
                      leftMargin=52, rightMargin=52,
                      topMargin=54, bottomMargin=54,
                      title="TRIADE preuves v0.21.0",
                      author="TRIade")
f = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="c")
doc.addPageTemplates([PageTemplate(id="p", frames=[f])])
doc.build(story)
print(f"[body] {OUT}")

COVER_HTML = ICI / "preuves_v210_cover.html"
COVER_HTML.write_text("""
<html><head><style>
@page { size: A4; margin: 0; }
body { margin: 0; font-family: 'Liberation Serif', serif; }
.cover { width: 210mm; height: 297mm; background: #162032; color: #fff;
padding: 24mm 20mm; box-sizing: border-box; }
h1 { font-size: 34pt; margin: 0 0 4mm; }
.sub { font-size: 13pt; color: #cdd6e6; margin-bottom: 14mm; }
.label { font-size: 10pt; letter-spacing: 3px; color: #8fa3c8;
margin-bottom: 4mm; }
.meta { font-size: 10.5pt; line-height: 1.7; color: #dfe6f2; }
.rule { border-top: 1px solid #3a4a66; margin: 10mm 0; }
</style></head><body><div class="cover">
<h1>Preuves et calculs</h1>
<div class="sub">La vague 10 — l'édition v0.21.0</div>
<div class="label">PIÈCES DE LA VAGUE</div>
<div class="meta">
La faute SSE2 nomm&eacute;e et corrig&eacute;e : la diffusion du motif &agrave; quatre octets, 406/564 plant&eacute;es manqu&eacute;es<br/>
La re-mesure : les baselines &eacute;quitables (memchr, memmem, gcc-O3), le temps r&eacute;el sur mat&eacute;riel<br/>
La fen&ecirc;tre de relecture : 2&nbsp;452 &rarr; 1&nbsp;146 (&minus;53,3&nbsp;%), le mat&eacute;riau &times;7, la prose domine d&eacute;sormais<br/>
Les gardes : 58 preuves UNSAT, 58 falsifications, 100&nbsp;% d&eacute;charg&eacute;-ou-gard&eacute;<br/>
La non-interf&eacute;rence &eacute;tendue : x25519 et MD5, 13 blocs, sous l'hypoth&egrave;se du lifter<br/>
Le bras C+G : l'effet notation isol&eacute; (18,1&times;), l'effet gouvernance (1,11&times;)<br/>
La r&eacute;conciliation : l'abstract align&eacute;, le ratio M4 recalcul&eacute;, l'axe ajouter op&eacute;rationnel
</div>
<div class="rule"></div>
<div class="meta">Document de preuve &middot; s&eacute;rie TRIADE &middot;
&eacute;dition v0.21.0 &middot; 20 novembre 2026</div>
</div></body></html>""")
subprocess.run(["weasyprint", str(COVER_HTML),
                str(ICI / "preuves_v210_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "preuves_v210_cover.pdf")).pages[0])
for p_ in PdfReader(str(OUT)).pages:
    w.add_page(p_)
w.add_metadata({"/Title": "TRIADE — preuves et calculs v0.21.0"})
FINAL = ICI / "TRIADE_preuves_et_calculs_v0.21.0.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(str(FINAL)).pages)} pages)")
