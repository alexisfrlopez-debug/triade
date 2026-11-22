#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_preuves_v232.py — le document TRIADE_preuves_et_calculs_v0.23.2.pdf
(ReportLab + weasyprint + pypdf, le modèle v230 reconduit) : les pièces de
la vague 14 lues VERBATIM de leurs rapports (jamais retapées), LA
CONSIGNATION DES CORRECTIONS (a)-(j) de io13olvxz (la génération
corrective v0.23.2 — la session promise à l'Entrée 384, la demande du
maître : « je n'ai pas la version presentation et soumission du pack dans
zenodo »), l'héritage mesuré des vagues 11-13, la table des empreintes des
cinq pièces de l'édition."""
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
ICI = REPO / "scripts" / "vague14"
FER = REPO / "atelier-fermeture-f3uznui3l"
GHA = REPO / "atelier-ghash-agrege-h1mz2sr8s"
HCG = REPO / "atelier-hcgp4-s2p9bm3zd"
AJV = REPO / "atelier-ajouter-v4-842vqyy1k"
VAL = REPO / "atelier-validite-tcb7tpf9q"

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

OUT = ICI / "preuves_v232_body.pdf"
doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=52, rightMargin=52,
                      topMargin=56, bottomMargin=52,
                      title="TRIADE preuves v0.23.2", author="TRIADE")
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


para("TRIADE — preuves et calculs, l'édition v0.23.2 (la vague 14, la "
     "génération corrective)", S_T)
para("Les pièces verbatim des cinq ateliers de la quatorzième vague, lues "
     "de leurs rapports — jamais retapées ; la consignation des dix "
     "corrections (a)-(j) de io13olvxz portées aux sources et aux pièces "
     "par la présente génération ; l'héritage mesuré des vagues 11-13 ; la "
     "table des empreintes des cinq pièces de l'édition.")
para("LA GÉNÉRATION CORRECTIVE v0.23.2 (io13olvxz, la session promise à "
     "l'Entrée 384)", S_H)
para("La v0.23.1 (la release corrective de la vague 14) porta les sources "
     "corrigées au seul pack COMPLET — la soumission et la présentation "
     "DEMEURÈRENT byte-byte à leur état v0.23.0, l'écart nommé au "
     "worklog ; la demande du maître (« je n'ai pas la version "
     "presentation et soumission du pack dans zenodo ») commande la "
     "présente GÉNÉRATION : les CINQ pièces régénérées aux sources "
     "corrigées, le linter étendu, les TROIS packs assemblés à la version "
     "courante, la version publiée au concept. LES DIX CORRECTIONS "
     "SOURCÉES, chacune portée à SA pièce : (a) le gain du cache 683,6× "
     "(le canon non arrondi 285,725/0,418, D244) aux générateurs de la "
     "présentation et des preuves ; (b) l'erratum append-only au rapport "
     "de requalification (la décomposition des 15 exclusions recomposée "
     "par code du census CSV — l'énumération manuelle sommait à 13 ; la "
     "table recomposée PAR CODE : 12 = 5+2+1+1+1+1+1 — "
     "l'état mourant est ×5, la famille « the field beyond the motif » "
     "portée à l'abstract EN, loupe-14@0xdc) ; (c) les opérandes non arrondis du ratio plancher M4 "
     "(6.912/2.056 = 3.362) publiés au §7 du manuscrit ; (d) le bandeau du "
     "Livre « Version 1.6 » → v1.7 (la date alignée, §10.1 v0.15.8, le "
     "chapitre 11 D75–D250) ; (e) la grille T/X → F/L (D203, la "
     "correspondance un-pour-un au kit) au §4.1 du manuscrit et à la "
     "table des statuts ; (f) la voix « présent édition » (déjà unique "
     "depuis la v0.23.0, reconduite) ; (g) la spec « treize arbres "
     "VERTS » → quatorze ; (h) le dénominateur H-CGP2 nommé T−(C+G) et "
     "la fermeture aux opérandes non arrondis (20.715+16.497+0.213 = "
     "37.425) au corps du manuscrit ; (i) la Table 8 D210 it2 = 2 avec "
     "l'erratum as-filed nommé ; (j) le canon GHASH unique sur la "
     "variante ADOPTÉE (schoolbook 63,39 c [IQR 30] contre le scellé "
     "806,35 : 12,7× ; le karatsuba 64,04 la variété livrée non "
     "adoptée).")
para("LA LECTURE DES ATELIERS (verbatims)", S_H)
verbatim(FER / "rapport-fermeture.txt",
         titre="(1) LA FERMETURE SÉCURITÉ — f3uznui3l")
verbatim(GHA / "rapport-ghash-agrege.txt",
         titre="(2) LE GHASH AGRÉGÉ — h1mz2sr8s")
verbatim(HCG / "rapport-hcgp4.txt", titre="(3) H-CGP4 — s2p9bm3zd")
verbatim(AJV / "rapport-ajouter-v4.txt", titre="(4) TPL-ADD-v4 — 842vqyy1k")
verbatim(VAL / "rapport-validite.txt",
         titre="(5) LA VALIDITÉ EXTERNE — tcb7tpf9q")
para("LA COUPURE AU BORD DE LIGNE (la règle reconduite des v0.21.0/"
     "v0.23.0) : le verbatim des rapports d'atelier INTÉGRAL par "
     "défaut — aucune troncature au milieu d'un mot, chaque ligne "
     "entière.")
para("L'HÉRITAGE MESURÉ DES VAGUES 11-13 (les canons portés par la table "
     "canonique des budgets)", S_H)
para("LES GABARITS VERSIONNÉS : éditer 1 106 → 674 natif (−39,1 %, la "
     "prose −57 %) · localiser 1 053 → 627 (−40,5 %) · ajouter 3 074 → "
     "2 200 par squelette (−28,5 % publié à l'époque, le canon aux "
     "opérandes non arrondis −28,4 % : 3 073,5 → 2 199,5) ; LE COFFRE "
     "DURCI sur copies de laboratoire : les sept gestes (a)-(g) à la "
     "phrase publique D105, le plancher 184 bits, la sentinelle à "
     "l'empreinte liée à la clé AVANT l'AEAD ; LA PURGE D81 et le scan "
     "des 513 commits à zéro fuite ; LES KITS PRÉ-ENREGISTRÉS aux 57/57 "
     "autotests verts sans résultat produit (la règle des kits).")
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
     "LA DÉCOMPOSITION MÉMOIRE CORRIGÉE : MÉDIÉS 348, la somme 2098 "
     "EXACT — l'erratum nommé.")
para("LA VAGUE 13 (l'édition v0.23.0) : LE COULOIR GHASH PCLMULQDQ — "
     "karatsuba 64,04 c [22] · schoolbook 63,39 c [30] contre le scellé "
     "GPR 806,35 c — le schoolbook ADOPTÉ au gabarit courant (12,7× ; "
     "l'écart 0,65 c DANS l'IQR, non significatif, les deux notations "
     "livrées) ; LA VENTILATION QUATRE BRAS aux volumes ÉGALISÉS "
     "(10×6 = 60 par bras) : T 21,633 s · C+G+ 18,325 s · C+G 2,110 s · "
     "C 1,934 s — la notation intrinsèque 1,079 s (5,5 %), "
     "l'implémentation de vérification 0,779 s, le régime 17,487 s, la "
     "gouvernance 0,442 s ; TPL-ADD-v3 : AJOUTER 6/18 au coût médian "
     "3 844 ≤ 4 500, ÉDITER 18/18 (17 de première passe + UNE "
     "réparation) au coût 712 ; LES TROIS REQUALIFICATIONS : les 58 "
     "gardes conditional assumption-discharged au TCB 24+23+11, les 15 "
     "exclusions proved-argued-bounded (12 arguments sémantiques + 3 "
     "sweeps bornés), le Tamarin CF3 v2 sans restriction adversaire.")
para("LA TABLE DES EMPREINTES DES CINQ PIÈCES v0.23.2", S_H)
pieces = {
    "TRIADE_manuscrit_v0.23.2.pdf": REPO / "edition-v0230" / "main.pdf",
    "Protocole_TRIADE_v0.15.8_Specification.pdf":
        REPO / "scripts" / "spec_v158" / "main.pdf",
    "Livre_du_Coffre_TRIADE_CF1-CF3_v1.7.pdf":
        REPO / "scripts" / "livre_v17" / "final.pdf",
}
for nom, chemin in sorted(pieces.items()):
    if chemin.exists():
        para(nom + " — sha256 " +
             hashlib.sha256(chemin.read_bytes()).hexdigest(), S_M)
para("TRIADE_preuves_et_calculs_v0.23.2.pdf — la présente (l'empreinte "
     "consignée au manifeste du pack).", S_M)
para("TRIADE_presentation_v232.pdf — la présentation (l'empreinte "
     "consignée au manifeste du pack).", S_M)
doc.build(FLOTS)
print("[preuves v232] le corps : " + str(OUT))

COVER = ICI / "preuves_v232_cover.html"
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
<div class="s">La quatorzi&egrave;me vague — la g&eacute;n&eacute;ration
corrective v0.23.2 : les dix corrections (a)-(j) port&eacute;es aux cinq
pi&egrave;ces, le GHASH agr&eacute;g&eacute; &agrave; 19,66 c/mult (41,0&times;),
H-CGP4 &agrave; &minus;89,4 %, TPL-ADD-v4 &agrave; 7/18, H7 tir&eacute;e, le
premier run Tamarin v&eacute;cu — les pi&egrave;ces verbatim, les empreintes
crois&eacute;es</div>
<div class="f">S&eacute;rie TRIADE &middot; &eacute;dition v0.23.2 &middot; 22 novembre 2026
&middot; les pi&egrave;ces verbatim, les empreintes crois&eacute;es</div>
</div></body></html>""", encoding="utf-8")
subprocess.run(["weasyprint", str(COVER), str(ICI / "preuves_v232_cover.pdf")],
               check=True)

from pypdf import PdfReader, PdfWriter
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "preuves_v232_cover.pdf")).pages[0])
for p in PdfReader(str(OUT)).pages:
    w.add_page(p)
w.add_metadata({"/Title": "TRIADE preuves v0.23.2"})
FINAL = ICI / "TRIADE_preuves_et_calculs_v0.23.2.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print("[preuves v232] LA PIÈCE : " + str(FINAL) + " (" +
      str(len(PdfReader(str(FINAL)).pages)) + " pages)")
