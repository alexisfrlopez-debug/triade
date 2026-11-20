#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_preuves_v200.py — le document TRIADE_preuves_et_calculs_v0.20.0.pdf
(ReportLab) : les pièces de la vague 9 — la sécurité au plancher, la
boucle de vérification, les deux couloirs, les tokens, le tableau de
bord. Les pièces verbatim sont LUES des ateliers — jamais retapées."""
import os
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
ICI = REPO / "scripts" / "vague9"
OUT = ICI / "preuves_v200_body.pdf"

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
st_mono = ParagraphStyle("mono", fontName="Mono", fontSize=6.4, leading=8.4,
                         textColor=colors.HexColor("#222222"))
st_titre = ParagraphStyle("titre", fontName="Serif-Bold", fontSize=21,
                          leading=26, textColor=DARK, spaceAfter=4)
st_sous = ParagraphStyle("sous", fontName="Sans", fontSize=10.5, leading=15,
                         textColor=colors.HexColor("#555555"), spaceAfter=2)


def para(txt, st=st_body):
    return Paragraph(txt.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;").replace("\n", "<br/>"), st)


def lit(chemin, limite=2600):
    try:
        t = pathlib.Path(chemin).read_text(encoding="utf-8")
        return t[:limite] + ("\n[… tronqué à la pièce — le fichier entier "
                             "au dépôt]" if len(t) > limite else "")
    except FileNotFoundError:
        return f"[la pièce {chemin} — ABSENTE]"


SEC = REPO / "atelier-securite-bk79jvzbm"
BOU = REPO / "atelier-boucle-bkobf06nu"
PER = REPO / "atelier-perf-0205wxg5q"
TOK = REPO / "atelier-tokens-uagz3fby7"
DASH = REPO / "atelier-dashboard-h0mq0s2m6"

story = [
    para("TRIADE — preuves et calculs", st_titre),
    para("Édition v0.20.0 — la vague 9 : la sécurité au plancher, la boucle "
         "de vérification, les deux couloirs de performance, le coût en "
         "tokens au-delà d'OPT-05, le tableau de bord des quatre axes",
         st_sous),
    Spacer(1, 6),
    para("Le présent document porte les pièces de la vague 9 : les cinq "
         "instructions exécutées aux plans gelés d'abord (les empreintes "
         "consignées AVANT la première donnée), les re-productions à "
         "l'identique (la console v0.14.0, la console courante, la "
         "re-mesure localiser, la référence éditer), les preuves nouvelles "
         "(la sûreté mémoire déchargée à 95,6 %, la non-interférence aux "
         "dix familles, CF3 mécanisé 14/14, l'ancrage de transparence), "
         "les falsifications consignées telles quelles (l'ajout par hunks "
         "refusé pour la troisième fois, le composer-G à 3/18). Les pièces "
         "verbatim sont lues des ateliers — jamais retapées. Le concept "
         "DOI 10.5281/zenodo.24367343 résout sur la version courante (le "
         "dépôt public D220 — la publication AU GESTE DU MAÎTRE)."),
    para("LA VAGUE 9 EN UNE PAGE", st_h1),
    para("(1) LA SÉCURITÉ AU PLANCHER (bk79jvzbm) : la sûreté mémoire — "
         "2 006/2 098 accès DÉCHARGÉS par preuve (95,6 %), 92 NOMMÉS avec "
         "cause et certificat BMC, zéro hors-cadre ; la mutation — la "
         "console v0.14.0 REPRODUITE À L'IDENTIQUE (776/832) puis la "
         "courante (811/832), les DEUX nouveaux scénarios K5, LES TROIS "
         "« tuables » RE-CLASSÉS ÉQUIVALENTS-PAR-SWEEP (30 scénarios, "
         "zéro écart — l'hypothèse de la vague 8 corrigée par la preuve) ; "
         "le temps constant — la non-interférence statique PROUVÉE aux dix "
         "familles crypto ; CF3 — l'invariant MÉCANISÉ en z3 (14/14, "
         "l'assistant indépendant) ; la transparence — le témoin d'époque "
         "ANCRÉ, la réécriture refusée. (2) LA BOUCLE DE VÉRIFICATION "
         "(bkobf06nu) : le CERTIFICAT DE CRISTALLISATION (le diff d'un "
         "bloc : 3 contre 18, les trois falsifications refusées), le "
         "DOUBLE MOTEUR à l'ouverture (DIVERGENCE=0, le volume QEMU "
         "0,03 s contre l'échantillon 20,0 s), le régime ORACLE NATIF "
         "préparé, la mesure M4 (39,3/6,9/2,1 — le ratio 3,4×, la "
         "mesure re-jouée de la reprise : l'incident nommé, les pièces "
         "brutes de la session morte perdues, la mesure refaite aux "
         "mêmes n). "
         "(3) LES DEUX COULOIRS (0205wxg5q) : la parité SSE2 — la variante "
         "à 0,03× gcc-O2 (31,2× sur le GPR), zéro divergence aux 24 "
         "vecteurs ; le couloir B — AES-NI DÉJÀ LE SCELLÉ (l'ère "
         "l'exige), GHASH la frontière nommée. (4) LES TOKENS "
         "(uagz3fby7) : éditer-H2 reproduit (2 452/40), l'ajout refusé "
         "pour la troisième fois (0/18), composer-G 3/18 (4 846), "
         "localiser-P reproduit (1 103/52), le compilateur d'oracle "
         "(968 tokens supprimés), les ratios au plancher. (5) LE TABLEAU "
         "DE BORD (h0mq0s2m6) : les quatre axes générés des pièces "
         "brutes, les planchers nommés, l'ordre lexicographique."),
]

# ---------------- la pièce 1 : la sûreté mémoire -----------------------------
story += [para("LA PIÈCE 1 — LA SÛRETÉ MÉMOIRE AU PLANCHER (le rapport "
               "v200, verbatim)", st_h1),
          para(lit(SEC / "surete_memoire_v200_rapport.txt"), st_mono)]

# ---------------- la pièce 2 : la batterie étendue ---------------------------
story += [para("LA PIÈCE 2 — LA BATTERIE ÉTENDUE (le rapport, verbatim)",
               st_h1),
          para(lit(SEC / "RAPPORT-BATTERIE-ETENDUE.txt"), st_mono)]

# ---------------- la pièce 3 : les preuves CF3 et la non-interférence --------
story += [para("LA PIÈCE 3 — CF3 MÉCANISÉ ET LA NON-INTERFÉRENCE "
               "(les rapports, verbatim)", st_h1),
          para(lit(SEC / "rapport-cf3-smt.txt", 1800), st_mono),
          Spacer(1, 4),
          para(lit(SEC / "non_interference_v200_rapport.txt", 1500), st_mono)]

# ---------------- la pièce 4 : le certificat incrémental ---------------------
story += [para("LA PIÈCE 4 — LE CERTIFICAT DE CRISTALLISATION ET LE DOUBLE "
               "MOTEUR (les rapports, verbatim)", st_h1),
          para(lit(BOU / "rapport-verifier-incrementale.txt", 1600), st_mono),
          Spacer(1, 4),
          para(lit(BOU / "rapport-double-moteur-ouverture.txt", 1400), st_mono)]

# ---------------- la pièce 5 : les deux couloirs -----------------------------
story += [para("LA PIÈCE 5 — LES DEUX COULOIRS DE PERFORMANCE (les rapports, "
               "verbatim)", st_h1),
          para(lit(PER / "rapport-couloir-a-sse2.txt", 1400), st_mono),
          Spacer(1, 4),
          para(lit(PER / "rapport-couloir-b.txt", 1600), st_mono)]

# ---------------- la pièce 6 : les tokens ------------------------------------
story += [para("LA PIÈCE 6 — LA CAMPAGNE DE TOKENS ET LE COMPILATEUR "
               "D'ORACLE (les rapports, verbatim)", st_h1),
          para(lit(TOK / "extraire_vague9_rapport.txt", 1400), st_mono),
          Spacer(1, 4),
          para(lit(TOK / "rapport-compilateur-oracle.txt", 1200), st_mono)]

# ---------------- la pièce 7 : le tableau de bord ----------------------------
story += [para("LA PIÈCE 7 — LE TABLEAU DE BORD DES QUATRE AXES (généré des "
               "pièces brutes, verbatim)", st_h1),
          para(lit(DASH / "tableau-bord-quatre-axes.txt", 7000), st_mono)]

# ---------------- la pièce 8 : l'ancrage de transparence ---------------------
story += [para("LA PIÈCE 8 — L'ANCRAGE DE TRANSPARENCE (le rapport, "
               "verbatim)", st_h1),
          para(lit(SEC / "rapport-transparence.txt", 1400), st_mono)]

# ---------------- la table des empreintes des cinq pièces --------------------
import hashlib


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


MANUSCRIT = REPO / "edition-v0200" / "main.pdf"
SPEC = REPO / "scripts" / "spec_v156" / "main.pdf"
LIVRE = REPO / "scripts" / "livre_v15" / "final.pdf"

emp_m, emp_s, emp_l = sha(MANUSCRIT), sha(SPEC), sha(LIVRE)

story += [para("LES EMPREINTES SHA-256 DES CINQ PIÈCES DU PACK v0.20.0", st_h1),
          para("La consigne de l'instruction : les empreintes des cinq pièces "
               "consignées dans la présentation et le document de preuves. "
               "LA CONVENTION (l'écart nommé, physique du format) : aucun "
               "document ne peut porter son propre sha-256 ; la PRÉSENTE "
               "porte les trois pièces de contenu ci-dessous, la "
               "PRÉSENTATION (générée après la présente) porte les QUATRE "
               "autres — les trois de contenu PLUS la présente —, et le "
               "manifeste empreintes_livrables_v0.20.0.txt du pack porte "
               "les CINQ. Le linter inter-pièces v200 re-vérifie chaque "
               "empreinte au build (toute divergence un ROUGE).", st_body),
          para(f"TRIADE_manuscrit_v0.20.0.pdf\n  {emp_m}\n"
               f"Protocole_TRIADE_v0.15.6_Specification.pdf\n  {emp_s}\n"
               f"Livre_du_Coffre_TRIADE_CF1-CF3_v1.5.pdf\n  {emp_l}\n"
               f"TRIADE_preuves_et_calculs_v0.20.0.pdf\n  la présente — "
               f"consignée à la présentation et au manifeste du pack\n"
               f"TRIADE_presentation_20261120_v200.pdf\n  consignée au "
               f"manifeste du pack (aucun document ne porte son propre "
               f"sha-256)", st_mono)]

doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=52, rightMargin=52,
                      topMargin=56, bottomMargin=56, title=
                      "TRIADE preuves et calculs v0.20.0")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
              id="corps")
doc.addPageTemplates([PageTemplate(id="page", frames=[frame])])
doc.build(story)
print("le corps des preuves :", OUT)

# ---------------- la couverture ------------------------------------------------
COVER_HTML = ICI / "preuves_v200_cover.html"
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
<div class="sub">La vague 9 — l'édition v0.20.0</div>
<div class="label">PIÈCES DE LA VAGUE</div>
<div class="meta">
La s&ucirc;ret&eacute; m&eacute;moire : 2&nbsp;006/2&nbsp;098 d&eacute;charg&eacute;s par preuve (95,6&nbsp;%), 92 nomm&eacute;s<br/>
La mutation : les trois &laquo;&nbsp;tuables&nbsp;&raquo; re-class&eacute;s &eacute;quivalents-par-sweep, 811/817 ajust&eacute; (99,3&nbsp;%)<br/>
Le temps constant : la non-interf&eacute;rence statique PROUV&Eacute;E aux dix familles<br/>
CF3 : l'invariant m&eacute;canis&eacute; en z3, 14/14 obligations (l'assistant ind&eacute;pendant)<br/>
Le certificat de cristallisation : le diff d'un bloc, 3 blocs contre 18<br/>
Les deux couloirs : la parit&eacute; SSE2 0,03&times; gcc-O2, AES-NI d&eacute;j&agrave; le scell&eacute;<br/>
Les tokens : le compilateur d'oracle (968 supprim&eacute;s), les ratios au plancher<br/>
Le tableau de bord des quatre axes : g&eacute;n&eacute;r&eacute;, les planchers nomm&eacute;s
</div>
<div class="rule"></div>
<div class="meta">Document de preuve &middot; s&eacute;rie TRIADE &middot;
&eacute;dition v0.20.0 &middot; 20 novembre 2026</div>
</div></body></html>""")
subprocess.run(["weasyprint", str(COVER_HTML),
                str(ICI / "preuves_v200_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "preuves_v200_cover.pdf")).pages[0])
for p_ in PdfReader(str(OUT)).pages:
    w.add_page(p_)
w.add_metadata({"/Title": "TRIADE — preuves et calculs v0.20.0"})
FINAL = ICI / "TRIADE_preuves_et_calculs_v0.20.0.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(str(FINAL)).pages)} pages)")
