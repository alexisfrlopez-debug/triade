#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_presentation_v220.py — la présentation de la vague 11 à
l'édition v0.22.0 : la purge D81, les couloirs SIMD, la boucle porteuse
sous sa cible, les gabarits versionnés, le coffre durci, le quatrième
bras C+G+ (H-CGP2), les kits pré-enregistrés, la soundness du lifter au
domaine, les errata nommés. LES EMPREINTES SHA-256 des quatre autres
pièces y sont GRAVÉES (la convention : aucun document ne porte son
propre sha-256, le manifeste du pack porte les cinq)."""
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
ICI = REPO / "scripts" / "vague11"
OUT = ICI / "presentation_v220_body.pdf"

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
    "manuscrit": REPO / "edition-v0220" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v157" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v16" / "final.pdf",
    "preuves": ICI / "TRIADE_preuves_et_calculs_v0.22.0.pdf",
}

story = [
    para("TRIADE — la présentation de la vague 11", st_titre),
    para("L'édition v0.22.0 : la purge D81, les couloirs SIMD, la boucle "
         "porteuse sous sa cible, les gabarits versionnés, le coffre durci, "
         "le quatrième bras, la soundness du lifter au domaine — et les "
         "errata nommés ; le concept DOI 10.5281/zenodo.24367343 résout "
         "sur la version courante (le dépôt public D220)", st_sous),
    Spacer(1, 8),
    para("LES NEUF POINTS DE LA SESSION", st_h1),
    para("1 · LA PURGE DES INSTRUCTIONS DE REMISE D81 (ou6wn6wlv) — le "
         "séquestre 5/3 EST LA GARDE ACTIVE, le dépôt est public : les "
         "pièces opératoires portaient encore des instructions de remise "
         "dont l'exécution aujourd'hui POUSSERAIT la phrase de contrôle au "
         "dépôt public. LE LIVRE v1.6 (15 remplacements ancrés) ET LA SPEC "
         "v0.15.7 (11 remplacements) purgés ; le grep exhaustif : UNE "
         "occurrence par pièce, HISTORIQUE-DATÉE, zéro prescriptive ; LA "
         "SIMULATION du runbook au clone à phrase publique D105 : huit "
         "étapes sans écriture, LE GESTE PIÈGE REFUSÉ au premier nom, le "
         "scan des 513 commits ZÉRO FUITE."),
    para("2 · LES COULOIRS SIMD (fnvan0zes) — l'hybride memchr+memcmp 704 "
         "cycles [IQR 52] par recherche absente de 4 096 octets : 25,9× "
         "SOUS le scellé GPR (18 226) — DANS LA CLASSE des primitives SIMD "
         "de la libc ; le SHA-NI au corps natif 128,5 cycles/bloc (6,5× "
         "sous le scellé SHA-256, le dispatch hissé : 202 cycles nommés) ; "
         "l'AVX2 dominé par le sondage au bac virtualisé (cpuid ≈ 2 660 "
         "cycles par appel — le hissage par session exigé) ; LA BATTERIE "
         "ÉLARGIE 559 vecteurs ZÉRO DIVERGENCE (les queues de tampon à "
         "chaque alignement, les chevauchants, les longueurs 1-33, les "
         "pages, les multi-occurrences, 512 property-based à la graine "
         "consignée) ; le SHA-NI contre le scellé 256/256."),
    para("3 · LA BOUCLE PORTEUSE AES-NI RESTRUCTURÉE (ahult8jgd) — la "
         "v4-inline 7,09 cycles/bloc [0,09] : LA CIBLE ≤12 ENVELOPPE "
         "COMPRISE ATTEINTE, 7,1× sur le flux v2 (50,56), LA CLASSE du "
         "scellé appelé par le compilateur (7,62) REJOINTE ; les v3 "
         "nommées (la table 53,11, le déroulé 53,17 — le mode d'adressage "
         "indépendant est le levier, pas la précalcule) ; la parité FIPS "
         "197 256/256 octet pour octet, le contrôle négatif ATTRAPÉ, la "
         "borne fail-closed ; LE CACHE de round-trip 680,6× (la clé liée "
         "à la notation, au moteur et au profil — le contrôle négatif "
         "double) ; LA CRISTALLISATION INCRÉMENTALE −54 % au diff réel "
         "(l'audit 1/10 un FILET PROBABILISTE nommé — jamais une preuve) ; "
         "LES 37 s DÉCOMPOSÉES : les oracles 81 % du poste."),
    para("4 · LES GABARITS VERSIONNÉS (o5apue194) — LE CORPS DU GABARIT "
         "VIT UNE FOIS : TPL-EDIT-v1 identifié, son sha256 gravé au "
         "prompt, l'expansion recoupée côté client (fail-closed). ÉDITER "
         "1 106 → 674 natif (−39,1 % — LA PROSE −57 %, le levier nommé de "
         "la vague 10 saisi) ; LOCALISER 1 053 → 627 (−40,5 % — l'index "
         "grossier puis le pointeur fin) ; AJOUTER 3 074 → 2 200 (−28,5 % "
         "par squelette, la faisabilité 0→3 verts — LE GAP NOMMÉ aux "
         "quinze refus honnêtes : le modèle doit apprendre le domaine "
         "d'étiquettes et de constantes) ; la re-tokenisation à écart 0 "
         "aux 108 appels, le client 16 VERT, aucun contrôle retiré."),
    para("5 · LE COFFRE DURCI SUR COPIES DE LABORATOIRE (vr9n3s3l7) — les "
         "sept gestes (a)-(g) verts à la phrase publique D105 (aucun "
         "coffre réel, aucune phrase réelle — LA RÈGLE ABSOLUE) : la "
         "sentinelle à l'empreinte LIÉE À LA CLÉ AVANT l'AEAD (la "
         "corruption refusée sans destruction, la falsification détruite "
         "avec PV), V_piège dérivée à l'époque (l'anti-rollback au piège), "
         "la cérémonie Argon2 versionnée (le plancher 184 bits), le "
         "changement de phrase sous séquestre (trois parts à froid, "
         "l'ancienne inopérante), la garde RAM (mlock, explicit_bzero, "
         "dumpable), l'ancrage des témoins et le FIDO2 simulé — LE MODÈLE "
         "z3 : quatre invariants PROUVÉS, le contrôle négatif nommant la "
         "garde."),
    para("6 · LE QUATRIÈME BRAS C+G+ (3lmyfb2xa) — le C gcc-O2 recevant "
         "la gouvernance ET LE RÉGIME DE VÉRIFICATION COMPLET du bras T "
         "(les rebuilds confrontés, les volumes oracle égaux, la "
         "recomposition à chaque livraison). LES QUATRE BRAS (n=5, ordre "
         "alterné) : T 39,39 s · C+G+ 18,68 s · C+G 2,18 s · C 1,97 s — "
         "NOTATION PROPRE 20,72 s (55,7 %) + RÉGIME DE VÉRIFICATION "
         "16,50 s (44,3 %) + GOUVERNANCE 0,213 s : H-CGP2 CONFIRMÉE, la "
         "requalification REJETÉE aux deux fenêtres ; la ventilation "
         "fermée à la milliseconde ; les oracles à volumes égaux 33,48 s "
         "(T) contre 0,51 s (C+G+) ; la réconciliation 20/20, le contrôle "
         "négatif double ATTRAPÉ et attribué."),
    para("7 · LES KITS PRÉ-ENREGISTRÉS (l4nnwqlld) — six kits ferment les "
         "lignes « awaiting » SANS PRODUIRE AUCUN RÉSULTAT (la règle : "
         "aucun résultat sans le geste du développeur) : le fence.i au "
         "silicium RV64 (la sonde à deux bras, C1-C5), la Loupe troisième "
         "machine (T0→T7+S0), dudect (N∈{60,200,400} × 2 machines, "
         "l'investigation des pics pré-enregistrée), H7 stratifiée (14 "
         "strates), le second annotateur (la grille F/L, le κ autotesté), "
         "le modèle CF3 Tamarin — LES TRENTE EMPREINTES consignées AVANT "
         "la remise, les autotests 57/57 VERTS, Tamarin non installé LE "
         "GAP NOMMÉ."),
    para("8 · LA SOUNDNESS DU LIFTER AU DOMAINE (hrbdfy6i4) — la méthode "
         "exacte (les écritures au diff, les lectures à la sentinelle "
         "différentielle — le premier passage artefactuel consigné) : 942 "
         "encodages DISTINCTS ZÉRO DIVERGENCE ; le corpus mutant 7 769 "
         "confrontés, 155 divergences TOUTES HORS VOCABULAIRE — LA GARDE : "
         "le lifter déclare sa soundness AU DOMAINE VALIDÉ et REFUSE "
         "toute classe non modélisée au chargement (fail-closed) ; H "
         "SECRET COUVERT (tls13-17, ni branche ni adresse tachées) ; LA "
         "NON-INTERFÉRENCE 16/16 blocs, SEPT familles, tls13-04 au modèle "
         "affiné (l'état secret, la longueur publique nommée)."),
    para("9 · LES ERRATA NOMMÉS + LE LINTER v220 (zho5vilpy) — LA "
         "DÉCOMPOSITION MÉMOIRE CORRIGÉE : la ligne publiée « médiés 0 » "
         "sommait à 1750, pas 2098 — le recompte du CSV brut porte "
         "MÉDIÉS 348, la somme 2098 EXACTEMENT (l'erratum nommé aux "
         "preuves v0.22.0, le verbatim v0.21.0 demeuré) ; LA CAUSE du "
         "« couloir B : code 1 » consignée : le sous-processus mort À "
         "L'IMPORT (pefile/nacl absents du bac — ModuleNotFoundError), la "
         "re-exécution aux chiffres reproduits (v1 45 · v2 34,4 · scellé "
         "26) ; LES RATIOS §7 recalculés à une décimale (1,5× / 19,3×) ; "
         "LE PLANCHER ÉDITER re-tokenisé au NATIF (27,5 — le ratio "
         "natif/natif 24,5×, la ligne cl100k datée) ; LE LINTER v220 "
         "ÉTENDU À TOUT TOKEN NUMÉRIQUE de la prose des cinq pièces "
         "(chaque nombre confronté aux canons du manifeste brut, aux "
         "arithmétiques dérivées, aux historiques datés — toute "
         "divergence REFUSÉE, le contrôle négatif vécu)."),
    Spacer(1, 10),
]

# ---- la table des statuts ------------------------------------------------
lignes = [
    [cell("PIÈCE"), cell("AVANT (v0.21.0)"), cell("APRÈS (v0.22.0)")],
    [cell("La décomposition mémoire (preuves)"),
     cell("« pile 1247 · médiés 0 · … » — la ligne somme à 1750, pas 2098"),
     cell("MÉDIÉS 348 (le recompte du CSV) — la somme 2098 EXACTE, l'erratum nommé")],
    [cell("Le ratio au plancher éditer"),
     cell("63,6× mixte (le total natif ÷ le plancher 18 cl100k)"),
     cell("24,5× NATIF/NATIF (le plancher re-tokenisé au champ usage : 27,5) ; la ligne cl100k datée")],
    [cell("Les ratios prose §7"),
     cell("« 1,6× above the memchr idiom », « two orders below »"),
     cell("1,5× et 19,3× — recalculés à une décimale par code (833/561, 16 040/833)")],
    [cell("Les headers du manuscrit"),
     cell("pdftitle et running header v0.20.0 ; la spec v0.15.6 ; DOI v0.19.5"),
     cell("v0.22.0 partout ; la spec v0.15.7 ; le concept à la v0.21.0 (24397623), les archives v0.22.0 au geste")],
    [cell("La conclusion RQ2"),
     cell("les médianes 1 277/3 374/3 674 du périmètre v0.17.0"),
     cell("les formats adoptés : pointeur seul (D222) 1 053, la fenêtre OPT-10 TRANCHÉE, les gabarits 674")],
    [cell("Les verbatim des preuves"),
     cell("la coupure à 2 600 caractères (« n'émAUCUN »), le mojibake de couverture"),
     cell("le verbatim INTÉGRAL (la coupure à la ligne), la balise meta charset posée")],
    [cell("L'opération éditer"),
     cell("1 106 natifs (la fenêtre, la prose 866 domine)"),
     cell("674 natifs (−39,1 %, TPL-EDIT-v1 — la prose 372, −57 %)")],
    [cell("Le localiser / l'ajouter"),
     cell("1 053 (pointeur) / 3 074 (notation complète, 0/18)"),
     cell("627 (hiérarchique, −40,5 %) / 2 200 (squelette, −28,5 %, la faisabilité 0→3 — le gap nommé)")],
    [cell("L'effet notation"),
     cell("18,1× « isolé » au bras C+G (le régime non porté — la question ouverte)"),
     cell("la notation PROPRE 20,72 s (55,7 %) + le régime 16,50 s (44,3 %) + la gouvernance 0,213 s — H-CGP2")],
    [cell("La boucle porteuse AES-NI"),
     cell("le flux v2 à 50,56 c/bloc (la cible ≤12 ouverte)"),
     cell("7,09 c/bloc [0,09] — LA CIBLE ATTEINTE (7,1×), la classe du scellé rejointe")],
    [cell("La non-interférence / le lifter"),
     cell("13 blocs, l'hypothèse du lifter vérifiée au round-trip seul"),
     cell("16 blocs ; la soundness AU DOMAINE : 942 encodages, la garde fail-closed (155 hors vocabulaire)")],
    [cell("Les instructions de remise D81"),
     cell("présentes au Livre v1.5 et à la spec v0.15.6 (le risque au dépôt public)"),
     cell("PURGÉES : le Livre v1.6, la spec v0.15.7 — le séquestre 5/3 la garde active, 513 commits zéro fuite")],
    [cell("Le linter inter-pièces"),
     cell("v210 : les canons nommés + la cohérence interne"),
     cell("v220 : TOUT TOKEN NUMÉRIQUE de la prose — le manifeste brut, les arithmétiques, les historiques datés")],
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
                      title="TRIade presentation v220",
                      author="TRIade")
f = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="c")
doc.addPageTemplates([PageTemplate(id="p", frames=[f])])
doc.build(story)
print(f"[body] {OUT}")

COVER_HTML = ICI / "presentation_v220_cover.html"
COVER_HTML.write_text("""
<html><head><meta charset="utf-8"><style>
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
<div class="sub">La vague 11 &mdash; l'&eacute;dition v0.22.0 &mdash; la purge, les couloirs,
la cible atteinte, les gabarits, la soundness au domaine</div>
<div class="label">LES NEUF POINTS</div>
<div class="meta">
La purge D81 : le s&eacute;questre 5/3 la garde active &mdash; le geste pi&egrave;ge refus&eacute;, 513 commits z&eacute;ro fuite<br/>
Les couloirs SIMD : l'hybride 704 cycles (25,9&times;), le SHA-NI 128,5 c/bloc &mdash; 559 vecteurs z&eacute;ro divergence<br/>
La boucle porteuse : 7,09 c/bloc &mdash; la cible &le;12 ATTEINTE (7,1&times;), la classe du scell&eacute; rejointe<br/>
Les gabarits versionn&eacute;s : &eacute;diter 674 natifs (&minus;39,1&nbsp;%, la prose &minus;57&nbsp;%), localiser 627, ajouter par squelette<br/>
Le quatri&egrave;me bras : la notation propre 20,72&nbsp;s (55,7&nbsp;%) s&eacute;par&eacute;e du r&eacute;gime (44,3&nbsp;%) &mdash; H-CGP2 confirm&eacute;e<br/>
La soundness du lifter au domaine : 942 encodages, la garde fail-closed, 16 blocs aux sept familles<br/>
Le coffre durci (a)-(g) sur copies labo, le mod&egrave;le z3 &agrave; quatre invariants ; les six kits pr&eacute;-enregistr&eacute;s<br/>
Les errata nomm&eacute;s : la d&eacute;composition m&eacute;moire (m&eacute;di&eacute;s 348 &mdash; la somme 2098 exacte), la cause du &laquo; couloir B : code 1 &raquo;
</div>
<div class="rule"></div>
<div class="meta">La boucle de v&eacute;rification &middot; tout token num&eacute;rique contr&ocirc;l&eacute; &middot; fail-closed<br/>
Document de pr&eacute;sentation &middot; s&eacute;rie TRIADE &middot; &eacute;dition v0.22.0 &middot; 21 novembre 2026</div>
</div></body></html>""")
subprocess.run(["weasyprint", str(COVER_HTML),
                str(ICI / "presentation_v220_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "presentation_v220_cover.pdf")).pages[0])
for p_ in PdfReader(str(OUT)).pages:
    w.add_page(p_)
w.add_metadata({"/Title": "TRIADE — présentation v0.22.0"})
FINAL = ICI / "TRIADE_presentation_20261121_v220.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(str(FINAL)).pages)} pages)")
