#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_preuves_v230.py — le document TRIADE_preuves_et_calculs_v0.23.0.pdf
(ReportLab + weasyprint) : les pièces de la vague 13 — les cinq ateliers
lus VERBATIM de leurs rapports (jamais retapés), L'ERRATUM de la
partition 559 (la correction (a) de ylrzmlbn8), la table des empreintes.
La chaîne : le corps ReportLab, la couverture weasyprint, la fusion pypdf
(le modèle v220 reconduit)."""
import hashlib
import pathlib
import subprocess

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph)

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "scripts" / "vague13"
OUT = ICI / "preuves_v230_body.pdf"
GHA = REPO / "atelier-ghash-0g3400vql"
REQ = REPO / "atelier-requalification-q8kugkpdu"
HCG = REPO / "atelier-hcgp3-ay6zuzm8o"
AJV = REPO / "atelier-ajouter-v3-5nwnwoceo"
PUR = REPO / "atelier-purge-v13-h66o54pjd"
LIF = REPO / "atelier-lifter-hrbdfy6i4"
MED = REPO / "atelier-medians-zho5vilpy"
KIT = REPO / "atelier-preregistre-l4nnwqlld"

FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", FDIR + "/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("SerifB", FDIR + "/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("SansB", FDIR + "/LiberationSans-Bold.ttf"))

S_T = ParagraphStyle("t", fontName="SerifB", fontSize=13, leading=16,
                     spaceAfter=6, spaceBefore=10)
S_H = ParagraphStyle("h", fontName="SansB", fontSize=10.5, leading=13,
                     spaceAfter=4, spaceBefore=8)
S_P = ParagraphStyle("p", fontName="Serif", fontSize=9.2, leading=12,
                     spaceAfter=5)
S_M = ParagraphStyle("m", fontName="Serif", fontSize=7.3, leading=9,
                     spaceAfter=3, leftIndent=8)

doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=52, rightMargin=52,
                      topMargin=56, bottomMargin=52,
                      title="TRIADE preuves v0.23.0", author="TRIADE")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin,
                          doc.width, doc.height, id="f")])])
FLOTS = []


def para(t, s=S_P):
    FLOTS.append(Paragraph(t, s))


def verbatim(chemin, limite=32000, titre=""):
    t = chemin.read_text(encoding="utf-8")
    if titre:
        para(titre, S_H)
    para("<i>pièce verbatim — " + chemin.name + " — sha256 " +
         hashlib.sha256(chemin.read_bytes()).hexdigest()[:16] + "…</i>",
         S_M)
    for l in t[:limite].split("\n"):
        if l.strip():
            para(l.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;"), S_M)


para("TRIADE — preuves et calculs, l'édition v0.23.0 (la vague 13)", S_T)
para("Les pièces verbatim des cinq ateliers de la treizième vague, lues "
     "de leurs rapports — jamais retapées ; l'erratum de la partition "
     "559 ; la table des empreintes des cinq pièces de l'édition.")
para("L'ERRATUM DE LA PARTITION 559 (la correction (a) — append-only, le "
     "verbatim historique demeure)", S_H)
para("La décomposition publiée à la vague 11 portait « 64+3 queue · 4 "
     "chevauchants · 13 longueurs · 3 pages · 8 multi · 512 "
     "property-based » — la somme 607, PAS 559. LE REGISTRE BRUT "
     "(census_batterie.py, D244) porte la partition exacte : 16 queue-16 "
     "+ 3 queue-fin + 4 chevauchants + 13 longueurs + 3 pages + 8 multi "
     "+ 512 property-based = 559 EXACTEMENT. La coquille 64←16 nommée, "
     "la partition corrigée portée aux cinq pièces, les rapports "
     "historiques demeurent verbatim.")
para("LA LECTURE DES ATELIERS (verbatims)", S_H)
verbatim(GHA / "rapport-ghash.txt", titre="(1) LE COULOIR GHASH — 0g3400vql")
verbatim(REQ / "rapport-requalification.txt",
         titre="(2) LA REQUALIFICATION — q8kugkpdu")
verbatim(HCG / "rapport-ventilation.txt",
         titre="(3) LA VENTILATION QUATRE BRAS — ay6zuzm8o")
verbatim(AJV / "rapport-ajouter-v3.txt", titre="(4) TPL-ADD-v3 — 5nwnwoceo")
verbatim(PUR / "rapport-purge-v13.txt", titre="(5) LA PURGE v13 — h66o54pjd")
para("LA COUPURE AU BORD DE LIGNE (la correction (f) de la vague 11, "
     "reconduite) : la limite de 2 600 caractères de la v0.21.0 (qui "
     "tronquait « n'ÉMET AUCUN » en « n'émAUCUN », corrigée) demeure la "
     "coupure au bord de LIGNE — le verbatim des rapports d'atelier "
     "INTÉGRAL par défaut, la présente le reconduit.")
para("LES PIÈCES VERBATIM DE LA VAGUE 11 (l'héritage — le lifter au "
     "domaine, les errata des médianes, les kits pré-enregistrés)", S_H)
verbatim(LIF / "rapport-lifter.txt", titre="(6) LE LIFTER AU DOMAINE — hrbdfy6i4 (la vague 11)")
verbatim(MED / "rapport-recompte.txt", titre="(7) LES ERRATA ET LE RECOMPTE — zho5vilpy (la vague 11)")
verbatim(KIT / "rapport-preregistre.txt", titre="(8) LES KITS PRÉ-ENREGISTRÉS — l4nnwqlld (la vague 11)")

para("L'HÉRITAGE MESURÉ DE LA VAGUE 11 (les canons portés par la table "
     "canonique des budgets)", S_H)
para("LES GABARITS VERSIONNÉS : éditer 1 106 → 674 natif (−39,1 %, la "
     "prose −57 %) · localiser 1 053 → 627 (−40,5 %) · ajouter 3 074 → "
     "2 200 par squelette (−28,5 % publié à l'époque, le canon aux "
     "opérandes non arrondis −28,4 % : 3 073,5 → 2 199,5) ; LE COFFRE "
     "DURCI sur copies de laboratoire : les sept gestes (a)-(g) à la "
     "phrase publique D105, le plancher 184 bits, la sentinelle à "
     "l'empreinte liée à la clé AVANT l'AEAD ; LA PURGE D81 et le scan "
     "des 513 commits à zéro fuite ; LES KITS PRÉ-ENREGISTRÉS aux 57/57 "
     "autotests verts sans résultat produit (la règle des kits — le geste "
     "du maître demeure la seule source de terrain).")
para("LES COULOIRS SIMD : l'hybride 704 cycles [IQR 52] — 25,9× sous le "
     "scellé GPR ; le SHA-NI 128,5 cycles/bloc (6,5×) ; LA BATTERIE 559 "
     "à zéro divergence (la partition exacte 16+3+4+13+3+8+512). LA "
     "BOUCLE PORTEUSE : 7,09 cycles/bloc [0,09] — 7,1× sur le v2 "
     "(50,56) ; LE CACHE de round-trip 285,725 → 0,418 ms — le gain "
     "683,6× ; LA CRISTALLISATION INCRÉMENTALE −54 % ; LES 37 s "
     "DÉCOMPOSÉES : les oracles 81 %, la cristallisation, les round-trips "
     "54 % du reste. LES QUATRE BRAS (la vague 11, l'outil non optimisé, "
     "l'asymétrie nommée) : T 39,39 s · C+G+ 18,68 s · C+G 2,18 s · "
     "C 1,97 s — la notation propre 20,72 s (55,7 %), le régime 16,50 s "
     "(44,3 %), la gouvernance 0,213 s — H-CGP2 confirmée (le verdict "
     "daté, distinct de H-CGP3). LE LIFTER AU DOMAINE : 942 encodages à "
     "zéro divergence, 155 mutantes hors vocabulaire, 7 769 lignes "
     "confrontées, 16/16 blocs à la non-interférence. LE PLANCHER ÉDITER "
     "NATIF 27.5 — le ratio 24.5× (aux lectures françaises 27,5 / 24,5) ; "
     "LA DÉCOMPOSITION MÉMOIRE CORRIGÉE : "
     "MÉDIÉS 348, la somme 2098 EXACT — la ligne qui sommait à 1750, PAS "
     "2098, la faute nommée, le verbatim historique demeuré (la ligne "
     "« !! couloir B : code 1 » conservée, la cause MORT À L'IMPORT — "
     "ModuleNotFoundError — consignée à côté, la correction (f) portée).")
para("LA TABLE DES EMPREINTES DES CINQ PIÈCES v0.23.0", S_H)
pieces = {
    "TRIADE_manuscrit_v0.23.0.pdf": REPO / "edition-v0230" / "main.pdf",
    "Protocole_TRIADE_v0.15.8_Specification.pdf":
        REPO / "scripts" / "spec_v158" / "main.pdf",
    "Livre_du_Coffre_TRIADE_CF1-CF3_v1.7.pdf":
        REPO / "scripts" / "livre_v17" / "final.pdf",
}
for nom, chemin in sorted(pieces.items()):
    if chemin.exists():
        para(nom + " — sha256 " +
             hashlib.sha256(chemin.read_bytes()).hexdigest(), S_M)
para("TRIADE_preuves_et_calculs_v0.23.0.pdf — la présente (l'empreinte "
     "consignée au manifeste du pack).", S_M)
para("TRIADE_presentation_v230.pdf — la présentation (l'empreinte "
     "consignée au manifeste du pack).", S_M)
doc.build(FLOTS)
print("[preuves v230] le corps : " + str(OUT))

COVER = ICI / "preuves_v230_cover.html"
COVER.write_text("""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>@page { size: A4; margin: 0; }
body { font-family: 'Liberation Serif', serif; margin: 0; }
.c { padding: 210px 64px 0 64px; }
.t { font-size: 34px; font-weight: bold; line-height: 1.2; }
.s { font-size: 17px; margin-top: 18px; color: #333; }
.f { position: absolute; bottom: 54px; left: 64px; right: 64px;
     font-size: 12px; color: #666; border-top: 1px solid #999;
     padding-top: 10px; }</style></head><body><div class="c">
<div class="t">TRIADE<br/>preuves et calculs</div>
<div class="s">La treizième vague — l'&eacute;dition v0.23.0 : le GHASH &agrave;
63-64 cycles, la requalification des gardes et des exclusions, la
ventilation &agrave; volumes &eacute;galis&eacute;s, TPL-ADD-v3, la purge v13 —
la partition 559 exacte, l'erratum append-only</div>
<div class="f">S&eacute;rie TRIADE &middot; &eacute;dition v0.23.0 &middot; 22 novembre 2026
&middot; les pi&egrave;ces verbatim, les empreintes crois&eacute;es</div>
</div></body></html>""", encoding="utf-8")
subprocess.run(["weasyprint", str(COVER), str(ICI / "preuves_v230_cover.pdf")],
               check=True)

from pypdf import PdfReader, PdfWriter
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "preuves_v230_cover.pdf")).pages[0])
for p in PdfReader(str(OUT)).pages:
    w.add_page(p)
w.add_metadata({"/Title": "TRIADE preuves v0.23.0"})
FINAL = ICI / "TRIADE_preuves_et_calculs_v0.23.0.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print("[preuves v230] LA PIÈCE : " + str(FINAL) + " (" +
      str(len(PdfReader(str(FINAL)).pages)) + " pages)")
