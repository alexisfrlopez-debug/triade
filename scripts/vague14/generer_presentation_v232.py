#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_presentation_v232.py — la présentation de la vague 14 à l'édition
v0.23.2 (la génération corrective — la session promise à l'Entrée 384) : la
fermeture sécurité et le premier run Tamarin vécu, le GHASH agrégé, H-CGP4,
TPL-ADD-v4, la validité externe (H7 tirée), la génération corrective elle-même
(les dix corrections (a)-(j), le linter étendu) — LES EMPREINTES SHA-256 des
quatre autres pièces GRAVÉES (la convention : aucun document ne porte son
propre sha256, le manifeste du pack porte les cinq)."""
import hashlib
import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

REPO = Path("/home/z/my-project/depot")
ICI = REPO / "scripts" / "vague14"
OUT = ICI / "presentation_v232_body.pdf"

FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", FDIR + "/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", FDIR + "/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FDIR + "/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/"
                               "DejaVuSansMono.ttf"))

DARK = colors.HexColor("#162032")
GRIS = colors.HexColor("#555555")

st_titre = ParagraphStyle("t", fontName="Serif-Bold", fontSize=19,
                          leading=23, spaceAfter=4)
st_sous = ParagraphStyle("s", fontName="Serif", fontSize=10, leading=13,
                         textColor=GRIS, spaceAfter=10)
st_h1 = ParagraphStyle("h1", fontName="Sans-Bold", fontSize=11.5,
                       leading=14, spaceBefore=10, spaceAfter=5,
                       textColor=DARK)
st_p = ParagraphStyle("p", fontName="Serif", fontSize=9.0, leading=11.8,
                      spaceAfter=5)
st_m = ParagraphStyle("m", fontName="Mono", fontSize=6.6, leading=8.2,
                      leftIndent=6, spaceAfter=2)

story = []


def para(t, s=None):
    story.append(Paragraph(t, s or st_p))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


para("TRIADE — la présentation de la vague 14, la génération corrective",
     st_titre)
para("L'édition v0.23.2 : les dix corrections (a)-(j) portées aux cinq "
     "pièces, le linter inter-pièces étendu, les trois packs assemblés à "
     "la version courante — la vague 14 : le GHASH agrégé à 19,66 c/mult "
     "(41,0×), H-CGP4 à −89,4 %, TPL-ADD-v4 à 7/18, H7 tirée, le premier "
     "run Tamarin vécu ; le concept DOI 10.5281/zenodo.24367343 résout "
     "sur la version courante (le dépôt public D220)", st_sous)

para("LES SIX POINTS DE LA SESSION", st_h1)
para("1 · LA FERMETURE SÉCURITÉ (f3uznui3l) — les 58 certificats UNSAT "
     "re-vérifiés UN PAR UN au z3 du bac (58/58, le TCB 24+23+11 "
     "re-dénombré) ; LA COMPOSITION DES GARDES DE FRONTIÈRE : la frontière "
     "admise PORTE l'invariant (le binding des bornes) — 58/58 décharges "
     "UNSAT, la preuve PORTANTE (58 mutations relâchées d'une unité : "
     "58/58 SAT) ; le coût par bloc mesuré (la garde 56,0 c natifs [IQR 2] "
     "— la cible ≤ 1 % NON TRANCHÉE au bac émulé, l'appel système absent, "
     "le gap nommé) ; le kit de cérémonie des sept gestes (l'autotest "
     "(a)(b) re-vécu 5/5) ; TAMARIN 1.12.0 INSTALLÉ AU BAC avec Maude 3.4 "
     "— le modèle CF3-v2 AMENDÉ PAR ÉCRIT (zero→nul réservé, les 15 "
     "déclarations event retirées) — LE PREMIER RUN EFFECTIF : le lemme "
     "d'implication FALSIFIÉ (trace 2 pas, Send → !KU(p) — les parts en "
     "variables publiques rendent K trivialement satisfiable : un défaut "
     "de MODÉLISATION nommé, jamais une attaque ; l'amendement requis "
     "écrit, la trace JSON consignée, AUCUN VERDICT FABRIQUÉ).")
para("2 · LE GHASH AGRÉGÉ QUATRE BLOCS À RÉDUCTION DIFFÉRÉE (h1mz2sr8s) — "
     "le couloir 601 o à la marge VIERGE 0xF300 : les produits X1..X4 "
     "contre les puissances H⁴..H DÉRIVÉES PAR LE SCELLÉ LUI-MÊME "
     "(l'associativité vérifiée par mesure), l'accumulation 256 bits par "
     "XOR, LA RÉDUCTION UNIQUE ; différentielle 320/320 ZÉRO ÉCART, "
     "mutant ATTRAPÉ au premier vecteur, repli 32/32, trace-hash UNE "
     "empreinte par classe, sceau 14/14 avant/après ; LA MESURE 19,66 "
     "c/mult [IQR 19] n=20 RDTSCP cœur épinglé — LE GAIN 41,0× SUR LE "
     "SCALLÉ (806,35), 3,23× sur le couloir v13 ; la projection de "
     "composition ~1,6 c/octet@4096 (la cible ≤ 2,0 probablement tenue, "
     "la mesure d'entrelacement LE GESTE SUIVANT nommée) ; OPT-18.")
para("3 · H-CGP4 LA MÉMOÏSATION CONTENT-ADDRESSED DU RÉGIME (s2p9bm3zd) — "
     "la clé sha256 de TOUT ce qui détermine le résultat (le contrôle "
     "négatif ATTRAPÉ : un octet muté = miss) ; l'audit 1-sur-10 vivant "
     "chaîné (la confrontation champ par champ, aucun écart vécu) ; LA "
     "MESURE n=5 : SANS 24,163 s / AVEC 2,555 s — LA PART RÉGIME RÉDUITE "
     "DE 89,4 % SANS AUCUN CONTRÔLE RETIRÉ ; H-CGP4 TENUE (jamais "
     "fusionnée avec H-CGP2/H-CGP3) ; l'oracle natif OPT-07 le gap "
     "nommé.")
para("4 · TPL-ADD-v4 LES QUATRE LEVIERS (842vqyy1k) — la grammaire au "
     "prompt (l'écart response_format nommé), le squelette à trous "
     "typés, LA RÉPARATION PAR CONTRE-EXEMPLE (le diff exact + les motifs "
     "canoniques), l'exemplaire par proche contrat ; AJOUTER 7/18 — "
     "loupe-11 CONVERTI (LA PREMIÈRE CONVERSION d'un refus honnête par "
     "la boucle) et loupe-16, contre la perte loupe-15 nommée ; LE COÛT "
     "MÉDIAN 3 990 ≤ 4 500 TENU ; LA CIBLE ≥ 15/18 MANQUÉE — le gap "
     "nommé par classe, jamais re-tiré, aucun juge affaibli.")
para("5 · LA VALIDITÉ EXTERNE (tcb7tpf9q) — H7 AU GESTE --tirer : la "
     "table officielle 2de7d488c89ea892… CONSIGNÉE-SIGNÉE, LA CAMPAGNE "
     "OUVERTE aux 28 unités (le registre D207) ; le kit du second "
     "annotateur re-vérifié (κ autotesté VERT) ; les trois kits "
     "re-vérifiés (57/57 autotests, la table 30/30) ; L'ÉTAT DE L'ART "
     "2026 aux références vérifiées une à une (Cannavale 2611.03231, "
     "Kainan-Hershman 2610.40071, Wang 2606.04990, Wu HarnessDev "
     "2609.01437) ; le coût PAR TENTATIVE et PAR CHANGEMENT VALIDÉ "
     "publiés côte à côte (5 915/3 844 ajouter · 712/712 éditer).")
para("6 · LA GÉNÉRATION CORRECTIVE v0.23.2 (io13olvxz, la présente) — LES "
     "DIX CORRECTIONS SOURCÉES portées aux CINQ pièces : (a) le gain du "
     "cache 683,6× ; (b) l'erratum append-only à la requalification (la "
     "décomposition recomposée par code du census CSV) ; (c) les "
     "opérandes non arrondis du plancher M4 (6.912/2.056 = 3.362) ; (d) "
     "le bandeau du Livre v1.7 ; (e) la grille T/X → F/L (D203) au §4.1 "
     "et à la table des statuts ; (g) la spec quatorze arbres ; (h) le "
     "dénominateur T−(C+G) et la fermeture aux opérandes non arrondis "
     "(20,715+16,497+0,213 = 37,425 s) ; (i) la Table 8 it2 = 2 ; (j) le canon GHASH unique sur "
     "la variante ADOPTÉE (schoolbook 63,39 [IQR 30] → 12,7×, le "
     "karatsuba 64,04 livré non adopté) ; LE LINTER ÉTENDU : les chaînes "
     "de version (bandeaux, couvertures, dates, plages décisionnelles), "
     "les décompositions de familles recomposées par code depuis les "
     "CSV, TOUT ratio publié portant ses opérandes non arrondis, la "
     "détection T/X hors marqueur d'époque daté — zéro rouge, le contrôle "
     "négatif vécu ; LES TROIS PACKS assemblés à v0.23.2 (la soumission, "
     "la présentation, le complet) — la version publiée au concept.")

para("L'ÉTAT DES ÉDITIONS", st_h1)
para("v0.23.0 (la vague 13, l'édition) : le GHASH PCLMULQDQ, la "
     "requalification, la ventilation, TPL-ADD-v3, la purge v13 — le "
     "Livre v1.7 et la spec v0.15.8. v0.23.1 (la corrective) : le "
     "complet seul régénéré (les sources corrigées + les six ateliers), "
     "la soumission et la présentation demeurées byte-byte — l'écart "
     "nommé. v0.23.2 (la présente, la génération corrective) : les cinq "
     "pièces régénérées aux sources corrigées, le linter étendu, les "
     "trois packs à la version courante — LA DEMANDE DU MAÎTRE (« je "
     "n'ai pas la version presentation et soumission du pack dans "
     "zenodo ») honorée : la soumission et la présentation portées à "
     "v0.23.2 et publiées au concept avec le complet.")

para("L'HÉRITAGE MESURÉ (les canons des vagues 11-13 portés par la table "
     "canonique)", st_h1)
para("LES COULOIRS SIMD : l'hybride 704 cycles [IQR 52] — 25,9× sous le "
     "scellé GPR (18 226) ; le SHA-NI 128,5 cycles/bloc (6,5×) ; LA "
     "BATTERIE 559 à zéro divergence. LA BOUCLE PORTEUSE : 7,09 "
     "cycles/bloc [0,09] — 7,1× sur le v2 (50,56) ; LE CACHE de "
     "round-trip 285,725 → 0,418 ms — le gain 683,6× ; LES 37 s "
     "DÉCOMPOSÉES : les oracles 81 %, les round-trips 54 % du reste. "
     "LES QUATRE BRAS (la vague 11, l'outil non optimisé) : T 39,39 s · "
     "C+G+ 18,68 s — la notation propre 20,72 s (55,7 %), le régime "
     "16,50 s (44,3 %), la gouvernance 0,213 s — H-CGP2 confirmée. LE "
     "LIFTER AU DOMAINE : 942 encodages à zéro divergence, 155 mutantes, "
     "7 769 lignes, 16/16 blocs. LE COULOIR GHASH v13 : schoolbook "
     "63,39 c [30] ADOPTÉ (12,7×), karatsuba 64,04 c [22], les deux "
     "livrées ; LA VENTILATION aux volumes égalisés : la notation "
     "intrinsèque 5,5 %. TPL-ADD-v3 : 6/18 au coût 3 844, ÉDITER 18/18 "
     "au coût 712.")
para("LES GABARITS, LE COFFRE, LES KITS (la suite de l'héritage)", st_h1)
para("LES GABARITS VERSIONNÉS : éditer 1 106 → 674 natif (−39,1 %, la "
     "prose de prescription −57 %) · localiser 1 053 → 627 (−40,5 %) · "
     "ajouter 3 074 → 2 200 par squelette (le canon aux opérandes non "
     "arrondis −28,4 % : 3 073,5 → 2 199,5) ; LE COFFRE DURCI sur copies "
     "de laboratoire (les sept gestes (a)-(g) à la phrase publique D105, "
     "le plancher 184 bits, la sentinelle à l'empreinte liée à la clé) ; "
     "LA PURGE et le scan des 513 commits à zéro fuite ; LES KITS "
     "PRÉ-ENREGISTRÉS aux 57/57 autotests verts sans résultat produit "
     "(la règle des kits).")

para("LES GAPS NOMMÉS (jamais simulés)", st_h1)
para("LA CIBLE TPL-ADD ≥ 15/18 manquée à 7/18 (le gap par classe de "
     "refus : expansion-divergente ×9 · hors-format ×2 · ID-inconnu ×1) ; "
     "la cible ≤ 1 % du coût des gardes NON TRANCHÉE au bac émulé (le "
     "coût par appel système absent du bac, le gap nommé) ; la "
     "composition d'entrelacement GHASH LA MESURE SUIVANTE (la cible "
     "≤ 2,0 c/octet probablement tenue, jamais déclarée avant mesure) ; "
     "la preuve Tamarin AMENDÉE au modèle (le premier run falsifia le "
     "lemme — le re-run au geste) ; les 28 livraisons H7, l'annotateur, "
     "les machines du dudect — au geste du maître ; UNE SEULE MACHINE "
     "virtualisée.")

PIECES = {
    "manuscrit": REPO / "edition-v0230" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v158" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v17" / "final.pdf",
    "preuves": ICI / "TRIADE_preuves_et_calculs_v0.23.2.pdf",
}
para("LES EMPREINTES DES QUATRE AUTRES PIÈCES (gravées — le manifeste du "
     "pack porte les cinq)", st_h1)
lignes = [["pièce", "sha256 (gravée en entier)"]]
for nom, chemin in sorted(PIECES.items()):
    if chemin.exists():
        lignes.append([nom, sha(chemin)])
tab = Table(lignes, colWidths=[95, 395])
tab.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), "Sans-Bold"),
    ("FONTNAME", (0, 1), (-1, -1), "Mono"),
    ("FONTSIZE", (0, 0), (-1, -1), 5.9),
    ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#AAAAAA")),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
]))
story.append(Spacer(1, 4))
story.append(tab)

doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=50, rightMargin=50,
                      topMargin=54, bottomMargin=50,
                      title="TRIADE présentation v232", author="TRIADE")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin,
                          doc.width, doc.height, id="f")])])
doc.build(story)
print("[présentation v232] le corps : " + str(OUT))

COVER = ICI / "presentation_v232_cover.html"
COVER.write_text("""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>@page { size: A4; margin: 0; }
body { font-family: 'Liberation Serif', serif; margin: 0; }
.c { padding: 200px 64px 0 64px; }
.t { font-size: 36px; font-weight: bold; line-height: 1.2; }
.s { font-size: 17px; margin-top: 20px; color: #333; }
.f { position: absolute; bottom: 54px; left: 64px; right: 64px;
     font-size: 12px; color: #666; border-top: 1px solid #999;
     padding-top: 10px; }</style></head><body><div class="c">
<div class="t">TRIADE<br/>la vague 14</div>
<div class="s">La g&eacute;n&eacute;ration corrective v0.23.2 : les dix corrections
(a)-(j) port&eacute;es aux cinq pi&egrave;ces, le linter &eacute;tendu, les trois packs
&agrave; la version courante — le GHASH agr&eacute;g&eacute; &agrave; 19,66 c/mult (41,0&times;),
H-CGP4 &agrave; &minus;89,4 %, TPL-ADD-v4 &agrave; 7/18, H7 tir&eacute;e, le premier run
Tamarin v&eacute;cu (falsifi&eacute; honn&ecirc;te)</div>
<div class="f">S&eacute;rie TRIADE &middot; &eacute;dition v0.23.2 &middot; 22 novembre 2026
&middot; les empreintes grav&eacute;es, les gaps nomm&eacute;s</div>
</div></body></html>""", encoding="utf-8")
subprocess.run(["weasyprint", str(COVER),
                str(ICI / "presentation_v232_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "presentation_v232_cover.pdf")).pages[0])
for p in PdfReader(str(OUT)).pages:
    w.add_page(p)
w.add_metadata({"/Title": "TRIADE présentation v232"})
FINAL = ICI / "TRIADE_presentation_v232.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print("[présentation v232] LA PIÈCE : " + str(FINAL) + " (" +
      str(len(PdfReader(str(FINAL)).pages)) + " pages)")
