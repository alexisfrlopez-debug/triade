#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_presentation_v230.py — la présentation de la vague 13 à
l'édition v0.23.0 : le GHASH, la requalification des gardes et des
exclusions, H-CGP3 à volumes égalisés, TPL-ADD-v3, la purge v13 (le Livre
v1.7, la spec v0.15.8) — LES EMPREINTES SHA-256 des quatre autres pièces
GRAVÉES (la convention : aucun document ne porte son propre sha256, le
manifeste du pack porte les cinq)."""
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
ICI = REPO / "scripts" / "vague13"
OUT = ICI / "presentation_v230_body.pdf"

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


para("TRIADE — la présentation de la vague 13", st_titre)
para("L'édition v0.23.0 : le couloir GHASH sous sa cible, la "
     "requalification des gardes et des exclusions, la ventilation à "
     "volumes égalisés (H-CGP3), la grammaire et la boucle de réparation "
     "(TPL-ADD-v3), la purge sémantique v13 — le Livre v1.7 et la spec "
     "v0.15.8 ; le concept DOI 10.5281/zenodo.24367343 résout sur la "
     "version courante (le dépôt public D220)", st_sous)

para("LES CINQ POINTS DE LA SESSION", st_h1)
para("1 · LE COULOIR GHASH EN PCLMULQDQ (0g3400vql) — LA CIBLE "
     "PRÉ-ENREGISTRÉE ≤ 80 CYCLES ATTEINTE : karatsuba 64,04 c [22] · "
     "schoolbook 63,39 c [30] contre le scellé 806,35 c — LE GAIN 12,6× ; "
     "la mesure TRANCHE (l'écart 0,65 c dans l'IQR, non significatif, les "
     "deux notations livrées) ; LA SONDE DE SESSION hissée une fois pour "
     "tous les corridors (le comptage cpuid/session == 1) ; L'AES-GCM "
     "COMPLET face à OpenSSL EVP : 7,556 c/octet @4096 (8,5× sur le "
     "scellé-18) ; @64 la composition couloir 19,47 DEVANT EVP 23,66 — le "
     "coût par appel d'EVP payé au petit message, l'agrégation nommée ; "
     "LA PARITÉ TRIPLE 25/25 octet pour octet ; le temps-constant "
     "structurel (une empreinte de trace par classe) ; OPT-17.")
para("2 · LES TROIS REQUALIFICATIONS (q8kugkpdu) — le statut exact des 58 "
     "gardes de sûreté mémoire : sur l'ARTEFACT SCELLÉ elles sont "
     "« conditional (assumption-discharged) » — des obligations de preuve "
     "conditionnelles aux invariants externes, le TCB en liste exhaustive "
     "24+23+11 = 58, les gardes ÉMISES en copies de laboratoire à la marge "
     "0x10000 (le modèle OPT-01), 58/58 certificats UNSAT re-vérifiés ; "
     "LES 15 EXCLUSIONS de mutants requalifiées « prouvé-argumenté borné » "
     "— 12 arguments sémantiques nommés + 3 sweeps bornés à 30 scénarios "
     "(JAMAIS des preuves mécaniques non bornées), 811+15+6 = 832 "
     "recomposé ; LE TAMARIN CF3 v2 : la restriction adversaire RETIRÉE, "
     "le lemme d'implication « secret appris ⇒ ≥3 parts » énoncé, le "
     "témoin d'atteignabilité du seuil, l'empreinte consignée — le prover "
     "absent du bac, LE GAP NOMMÉ, aucun verdict fabriqué.")
para("3 · LA VENTILATION QUATRE BRAS À VOLUMS ÉGALISÉS (ay6zuzm8o) — "
     "H-CGP3 PRÉ-ENREGISTRÉE PUIS TENUE : sur la pile optimisée, à "
     "volumes de rebuilds ÉGALISÉS (10 × 6 unités = 60 par bras, T "
     "inclus — l'asymétrie 12 vs 60 de la vague 11 fermée), la part de "
     "l'effet NOTATION INTRINSÈQUE dans T−C est 5,5 % (1,079 s / 19,787 "
     "s) ≤ 30 % — LE CONFOND TRANCHÉ PAR MESURE : le coût dominant de la "
     "vague 11 étiqueté « notation propre » (55,7 %) était l'effet "
     "IMPLÉMENTATION DE VÉRIFICATION (les oracles 33,5 s → 1,0 s à la "
     "pile optimisée) ; la réconciliation 20/20 aux tolérances, le run "
     "d'AUDIT nommé et exclu, le contrôle négatif +500 ms attrapé aux "
     "DEUX fenêtres, l'ordre randomisé à la graine consignée, les "
     "scellés intacts avant/après chaque run.")
para("4 · TPL-ADD-v3 : LA GRAMMAIRE ET LA BOUCLE DE RÉPARATION "
     "(5nwnwoceo) — la grammaire EBNF TPL-ADD-GRAMMAIRE-v1 PUBLIÉE au "
     "modèle dans le prompt (les quatre interdits de forme énoncés AVANT "
     "l'écriture) ; LES VALIDATEURS au client (cmp mémoire-à-mémoire · "
     "movzx r64/r64 · désalignement de taille · symbole en clair — refus "
     "FORME-INVALIDE au nom de la cause, la ligne fautive rendue) ; LA "
     "BOUCLE « assemble → refus nommé → réparation ciblée » au budget 3 ; "
     "LA MESURE aux 36 tâches : AJOUTER 6/18 verts (tous de première "
     "passe — la cible ≥ 17/18 MANQUÉE honnêtement, le coût 3 844 ≤ 4 500 "
     "tenu ; la boucle n'a converti AUCUN refus — le gap a déplacé à la "
     "STABILITÉ de l'écriture machine face au juge d'expansion) ; ÉDITER "
     "18/18 verts (17 de première passe + UNE réparation vécue, le coût "
     "712) ; LA TABLE CANONIQUE des budgets adoptés publiée.")
para("5 · LA PURGE v13, LE LIVRE v1.7 ET LA SPEC v0.15.8 (h66o54pjd) — le "
     "recensement EXHAUSTIF au vocabulaire élargi : les cibles nommées "
     "corrigées vers LA GARDE ACTIVE D223 (le Tableau 14 CF1, le §12.5, "
     "LE SPLICE §14.3 réparé par réécriture complète, l'énoncé périmé "
     "porté à l'état courant, les §17.3/glossaire/tables du protocole, "
     "les deux blocs du FORMAT_CARTE) ; LES PHRASES CASSÉES réécrites ; "
     "D236 portée à l'annexe B (la plage D75–D250) ; LE LINTER étendu (la "
     "règle à l'unité phrase/ligne) ; LA GARDE pre-commit/pre-push PAR "
     "EMPREINTES ET ENTROPIE (le piège et sa variante renommée refusés au "
     "premier nom, le faux positif nul sur 5 196 pièces) ; LES DEUX PDF "
     "reconstruits.")

para("LES ERRATA DE L'ÉDITION (ylrzmlbn8)", st_h1)
para("LA PARTITION 559 EXACTE : 16+3+4+13+3+8+512 = 559 (la ligne qui "
     "sommait à 607 portait 64←16, la coquille nommée, l'erratum "
     "append-only aux preuves) ; LE −28,4 % aux opérandes non arrondis "
     "(3 073,5 → 2 199,5 — le −28,5 % corrigé partout) ; LES ABSTRACTS "
     "EN/FR depuis les MÊMES canons (le résumé français ne titre plus les "
     "valeurs v0.17/v0.19.6 ; la campagne générative alignée à 30 000 "
     "traces zéro divergence) ; « SETTLED » SCOPÉ (la dérivation outillée "
     "zéro divergence ; la récitation pure 0/64, le gap de capacité "
     "nommé) ; LE CHANGELOG GELÉ des vagues (v0.14.0 → v0.23.0, une "
     "ligne par vague) ; la voix « présent édition » unique.")

para("L'HÉRITAGE MESURÉ (les canons de la vague 11 portés par la table "
     "canonique)", st_h1)
para("LES COULOIRS SIMD : l'hybride 704 cycles [IQR 52] — 25,9× sous le "
     "scellé GPR (18 226) ; le SHA-NI 128,5 cycles/bloc (6,5×) ; LA "
     "BATTERIE 559 à zéro divergence. LA BOUCLE PORTEUSE : 7,09 "
     "cycles/bloc [0,09] — 7,1× sur le v2 (50,56) ; LE CACHE de "
     "round-trip 285,725 → 0,418 ms — le gain 683,6× ; LES 37 s "
     "DÉCOMPOSÉES : les oracles 81 %, les round-trips 54 % du reste. "
     "LES QUATRE BRAS (la vague 11, l'outil non optimisé) : T 39,39 s · "
     "C+G+ 18,68 s — la notation propre 20,72 s (55,7 %), le régime "
     "16,50 s (44,3 %), la gouvernance 0,213 s — H-CGP2 confirmée (le "
     "verdict daté, DISTINCT de H-CGP3). LE LIFTER AU DOMAINE : 942 "
     "encodages à zéro divergence, 155 mutantes, 7 769 lignes, 16/16 "
     "blocs. LA DÉCOMPOSITION MÉMOIRE CORRIGÉE : médiés 348, la somme "
     "2098 EXACT — l'erratum nommé.")
para("LES GABARITS, LE COFFRE, LES KITS (la suite de l'héritage)", st_h1)
para("LES GABARITS VERSIONNÉS : éditer 1 106 → 674 natif (−39,1 %, la "
     "prose de prescription −57 %) · localiser 1 053 → 627 (−40,5 %) · "
     "ajouter 3 074 → 2 200 par squelette (−28,5 % publié à l'époque, le "
     "canon aux opérandes non arrondis −28,4 % : 3 073,5 → 2 199,5) ; LE "
     "COFFRE DURCI sur copies de laboratoire (les sept gestes (a)-(g) à "
     "la phrase publique D105, le plancher 184 bits, la sentinelle à "
     "l'empreinte liée à la clé) ; LA PURGE et le scan des 513 commits à "
     "zéro fuite ; LES KITS PRÉ-ENREGISTRÉS aux 57/57 autotests verts "
     "sans résultat produit (la règle des kits).")

para("LES GAPS NOMMÉS (jamais simulés)", st_h1)
para("UNE SEULE MACHINE virtualisée (le silicium nu au terrain, les "
     "cycles sont ceux de CETTE machine) ; TAMARIN-PROVER ABSENT du bac "
     "(le modèle v2 hashé, la vérification au geste du maître) ; la "
     "faisabilité de l'ajout 6/18 (le gap par classe de refus, jamais "
     "re-tiré) ; le run d'AUDIT du bras T (nommé et exclu du régime, le "
     "prix de la preuve) ; la limite de débit de l'API vécue (les "
     "reprises d'instrument nommées).")

PIECES = {
    "manuscrit": REPO / "edition-v0230" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v158" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v17" / "final.pdf",
    "preuves": ICI / "TRIADE_preuves_et_calculs_v0.23.0.pdf",
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
                      title="TRIADE présentation v230", author="TRIADE")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin,
                          doc.width, doc.height, id="f")])])
doc.build(story)
print("[présentation v230] le corps : " + str(OUT))

COVER = ICI / "presentation_v230_cover.html"
COVER.write_text("""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>@page { size: A4; margin: 0; }
body { font-family: 'Liberation Serif', serif; margin: 0; }
.c { padding: 200px 64px 0 64px; }
.t { font-size: 36px; font-weight: bold; line-height: 1.2; }
.s { font-size: 17px; margin-top: 20px; color: #333; }
.f { position: absolute; bottom: 54px; left: 64px; right: 64px;
     font-size: 12px; color: #666; border-top: 1px solid #999;
     padding-top: 10px; }</style></head><body><div class="c">
<div class="t">TRIADE<br/>la vague 13</div>
<div class="s">L'&eacute;dition v0.23.0 : le GHASH &agrave; 63-64 cycles (12,6&times;),
la requalification des 58 gardes et des 15 exclusions, H-CGP3 tenue &agrave;
5,5 % &agrave; volumes &eacute;galis&eacute;s, TPL-ADD-v3, la purge v13 — le Livre
v1.7 et la spec v0.15.8, la partition 559 exacte</div>
<div class="f">S&eacute;rie TRIADE &middot; &eacute;dition v0.23.0 &middot; 22 novembre 2026
&middot; les empreintes grav&eacute;es, les gaps nomm&eacute;s</div>
</div></body></html>""", encoding="utf-8")
subprocess.run(["weasyprint", str(COVER),
                str(ICI / "presentation_v230_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "presentation_v230_cover.pdf")).pages[0])
for p in PdfReader(str(OUT)).pages:
    w.add_page(p)
w.add_metadata({"/Title": "TRIADE présentation v230"})
FINAL = ICI / "TRIADE_presentation_v230.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print("[présentation v230] LA PIÈCE : " + str(FINAL) + " (" +
      str(len(PdfReader(str(FINAL)).pages)) + " pages)")
