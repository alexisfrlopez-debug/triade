#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_presentation_v210.py — la présentation de la vague 10 à
l'édition v0.21.0 : la faute SSE2 nommée et la re-mesure aux baselines
équitables, la fenêtre de relecture, les gardes et la non-interférence
étendue, le bras C+G isolant l'effet notation, la réconciliation et le
registre neutre. LES EMPREINTES SHA-256 des quatre autres pièces y sont
GRAVÉES (la convention : aucun document ne porte son propre sha-256, le
manifeste du pack porte les cinq)."""
import hashlib
import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

REPO = Path("/home/z/my-project/depot")
ICI = REPO / "scripts" / "vague10"
OUT = ICI / "presentation_v210_body.pdf"

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
st_cell = ParagraphStyle("cell", fontName="Serif", fontSize=8.6,
                         leading=11.6, textColor=colors.HexColor("#1a1a1a"))
st_mono = ParagraphStyle("mono", fontName="Mono", fontSize=6.8, leading=8.8,
                         textColor=colors.HexColor("#222222"))


def para(txt, st=st_body):
    return Paragraph(txt.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;").replace("\n", "<br/>"), st)


def cell(txt):
    return para(txt, st_cell)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


PIECES = {
    "manuscrit": REPO / "edition-v0210" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v156" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v15" / "final.pdf",
    "preuves": ICI / "TRIADE_preuves_et_calculs_v0.21.0.pdf",
}

story = [
    para("TRIADE — la présentation de la vague 10", st_titre),
    para("L'édition v0.21.0 : la faute nommée et corrigée, la fenêtre de "
         "relecture, les gardes prouvées, l'effet notation isolé, la "
         "réconciliation et le registre neutre — le concept DOI "
         "10.5281/zenodo.24367343 résout sur la version courante (le "
         "dépôt public D220)", st_sous),
    Spacer(1, 8),
    para("LES CINQ POINTS DE LA SESSION", st_h1),
    para("1 · LA FAUTE SSE2 NOMMÉE ET CORRIGÉE — la variante de la vague 9 "
         "diffusait le motif de QUATRE octets au lieu du premier : 406/564 "
         "occurrences plantées manquées (la différentielle plantée, "
         "introduite par la présente — l'épreuve antérieure n'exerçait "
         "AUCUNE occurrence, l'écart de l'épreuve nommé). La correction v2 : "
         "zéro divergence aux 88 vecteurs, le contrôle négatif attrapé. La "
         "re-mesure aux baselines ÉQUITABLES : les instructions (le "
         "compilateur n'émAUCUN SIMD sur la source naturelle — la baseline "
         "vectorisée du compilateur n'existe pas) ; LE TEMPS RÉEL sur "
         "matériel (RDTSC, cœur fixé, n=20) : 833 cycles/op — DANS LA "
         "CLASSE des primitives SIMD de la libc (l'idiome memchr 561, "
         "memmem 933, gcc-O2 16 040) ; le CPUID HISSÉ hors de la boucle "
         "(45 → 34,4 instr/bloc). UNE SEULE MACHINE : l'écart nommé."),
    para("2 · LA FENÊTRE DE RELECTURE (OPT-10) — l'opération ÉDITER ne "
         "relit plus la notation complète : la fenêtre ±12 lignes du hunk, "
         "la consigne, l'empreinte sha256 en garde, le reste en cache. "
         "n=18, la même graine : le total 2 452 → 1 146 (−53,3 %), le "
         "matériau relu 1 684 → 239 (×7,0) — LA PROSE DOMINE désormais "
         "(866) : le prochain levier nommé. La re-tokenisation "
         "indépendante : écart 0. Les quatre refus du pointeur re-roulés "
         "5/5 VERT."),
    para("3 · LES GARDES ET LA NON-INTERFÉRENCE ÉTENDUE — les 92 accès à "
         "base runtime : 100 % DÉCHARGÉ-OU-GARDÉ (34 LEA relationnels + 58 "
         "gardes à deux faces, prouvées UNSAT, falsifiées 58/58 : "
         "l'invariant violé ATTRAPÉ, l'adresse honnête admise). La "
         "non-interférence étendue à x25519 (le scalaire, la clé privée) "
         "et md5 (le contenu du fichier) : 13 blocs, sept familles, "
         "PROUVÉE SOUS L'HYPOTHÈSE DE SOUNDNESS DU LIFTER — vérifiée par "
         "le round-trip 13/13 zéro divergence, l'encodage alternatif "
         "attrapé. CF3 mécanisé 14/14 RECONDUIT (l'audit re-roulé "
         "vert)."),
    para("4 · LE TROISIÈME BRAS C+G — le C gcc-O2 RECEVANT la gouvernance "
         "TRIADE complète (les intentions signées Ed25519, la "
         "cristallisation chaînée, l'oracle dérivé de I, le kit au "
         "gabarit). La mesure aux TROIS bras sur la même machine (n=5) : "
         "T 39,24 s · C 1,95 s · C+G 2,16 s — L'EFFET NOTATION ISOLÉ "
         "37,07 s/session (18,1×), l'effet gouvernance 215 ms (1,11×). "
         "Loupe-05 close sur son rouge à la cap (trois échappées nommées). "
         "La réconciliation zéro écart, le contrôle négatif (la faute de "
         "rig injectée) ATTRAPÉ et attribué. M3 au geste du maître — "
         "jamais un chiffre inventé."),
    para("5 · LA RÉCONCILIATION ET LE REGISTRE NEUTRE — l'abstract aligné "
         "au corps (811/817 = 99,3 %, les 15 équivalents, les 6 survivants "
         "non équivalents) ; le ratio M4 RECALCULÉ des médianes non "
         "arrondies (6,912/2,056 = 3,4× partout où le courant) ; l'axe "
         "ajouter au COÛT OPÉRATIONNEL (3 674 — le format refusé 6 874 "
         "demeure nommé au bord, jamais rapporté comme coût) ; le linter "
         "v210 ÉTENDU à la cohérence INTERNE (abstract ↔ corps ↔ tableaux, "
         "le contrôle négatif refusé au premier nom) ; le registre "
         "neutralisé : le lexique ritualiste remplacé, AUCUNE valeur "
         "numérique modifiée hors la réconciliation documentée, la "
         "transparence intacte."),
    Spacer(1, 10),
]

# ---- la table des statuts ------------------------------------------------
lignes = [
    [cell("PIÈCE"), cell("AVANT (v0.20.0)"), cell("APRÈS (v0.21.0)")],
    [cell("Le score ajusté à l'abstract"),
     cell("811/820 = 98,9 % (12 équivalents — l'état du lot 8)"),
     cell("811/817 = 99,3 % (15 équivalents, 6 survivants — aligné au corps)")],
    [cell("Le ratio M4"),
     cell("3,3/3,4/3,5× selon les pièces"),
     cell("3,4× PARTOUT où le courant (recalculé : 6,912/2,056)")],
    [cell("L'axe token ajouter"),
     cell("le format refusé 6 874 rapporté comme valeur d'axe"),
     cell("le coût OPÉRATIONNEL 3 674 ; le refus nommé au bord")],
    [cell("La sûreté mémoire"),
     cell("2 006 déchargés, 92 nommés (95,6 %)"),
     cell("100 % DÉCHARGÉ-OU-GARDÉ (34 LEA + 58 gardes prouvées)")],
    [cell("La non-interférence"),
     cell("dix familles, PROUVÉE"),
     cell("13 blocs, sept familles, sous l'hypothèse du lifter (vérifiée)")],
    [cell("L'opération éditer"),
     cell("2 452 (la notation complète relue, matériau 1 684)"),
     cell("1 146 (−53,3 %), matériau 239, la prose domine (866)")],
    [cell("La SSE2 de recherche"),
     cell("3 928 instr/op (0,03× gcc-O2) — la faute non vue"),
     cell("4 087 instr/op ; 833 cycles RÉELS — dans la classe libc SIMD")],
    [cell("Le bras C+G"),
     cell("—"),
     cell("l'effet notation 18,1× isolé de la gouvernance (1,11×)")],
    [cell("Le registre"),
     cell("lexique ritualiste aux marges"),
     cell("neutre : les verbatim intacts, aucune valeur modifiée")],
]
tbl = Table(lignes, colWidths=[46*2.4, 68*2.4, 78*2.4])
tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), DARK),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9d2e0")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [colors.white, colors.HexColor("#f2f5f9")]),
]))
story += [para("LA TABLE DES STATUTS", st_h1), tbl, Spacer(1, 10)]

# ---- les empreintes gravées ---------------------------------------------
emp = ["LES EMPREINTES SHA-256 DES QUATRE AUTRES PIÈCES (gravées — la "
       "convention : ce document ne porte pas son propre sha-256, le "
       "manifeste du pack porte les cinq) :"]
for nom, ch in PIECES.items():
    emp.append(f"{sha(ch)}  {nom}")
story += [para("LES EMPREINTES DES PIÈCES", st_h1),
          para("\n".join(emp), st_mono)]

doc = BaseDocTemplate(str(OUT), pagesize=A4,
                      leftMargin=52, rightMargin=52,
                      topMargin=54, bottomMargin=54,
                      title="TRIade presentation v210",
                      author="TRIade")
f = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="c")
doc.addPageTemplates([PageTemplate(id="p", frames=[f])])
doc.build(story)
print(f"[body] {OUT}")

COVER_HTML = ICI / "presentation_v210_cover.html"
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
<h1>TRIADE</h1>
<div class="sub">La vague 10 &mdash; l'&eacute;dition v0.21.0 &mdash; la faute nomm&eacute;e,
la fen&ecirc;tre, les gardes, l'effet notation isol&eacute;</div>
<div class="label">LES CINQ POINTS</div>
<div class="meta">
La faute SSE2 : 406/564 occurrences manqu&eacute;es &mdash; la diff&eacute;rentielle plant&eacute;e la voit, la correction la porte<br/>
La re-mesure &eacute;quitable : le temps r&eacute;el sur mat&eacute;riel, la variante dans la classe des primitives SIMD<br/>
La fen&ecirc;tre d'&eacute;dition : 2&nbsp;452 &rarr; 1&nbsp;146 (&minus;53,3&nbsp;%), le mat&eacute;riau &times;7 &mdash; la prose domine<br/>
Les gardes : 58 preuves UNSAT, 58 falsifications &mdash; 100&nbsp;% d&eacute;charg&eacute;-ou-gard&eacute;<br/>
Le bras C+G : l'effet notation 18,1&times; isol&eacute; de la gouvernance (1,11&times;)<br/>
La r&eacute;conciliation : l'abstract align&eacute; (811/817 = 99,3&nbsp;%), le ratio recalcul&eacute; (3,4&times;), le registre neutre
</div>
<div class="rule"></div>
<div class="meta">La boucle de v&eacute;rification &middot; la faute nomm&eacute;e et corrig&eacute;e &middot; M4 3,4&times; recalcul&eacute;<br/>
Document de pr&eacute;sentation &middot; s&eacute;rie TRIADE &middot; &eacute;dition v0.21.0 &middot; 20 novembre 2026</div>
</div></body></html>""")
subprocess.run(["weasyprint", str(COVER_HTML),
                str(ICI / "presentation_v210_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "presentation_v210_cover.pdf")).pages[0])
for p_ in PdfReader(str(OUT)).pages:
    w.add_page(p_)
w.add_metadata({"/Title": "TRIADE — présentation v0.21.0"})
FINAL = ICI / "TRIADE_presentation_20261120_v210.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(str(FINAL)).pages)} pages)")
