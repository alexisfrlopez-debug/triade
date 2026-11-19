#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_presentation_v193.py — la présentation du 20/11, édition
v0.19.3 (l'écart fermé) : la table des statuts portée, les résultats de
la session 5ey7gmjra. Le motif v192 (ReportLab paysage + couverture)."""
import os
import subprocess

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

V7 = "/home/z/my-project/depot/scripts/vague7"
OUT = os.path.join(V7, "presentation_v193_body.pdf")

FDIR = "/usr/share/fonts/truetype/liberation"
for nom, fich in [("Serif", "LiberationSerif-Regular.ttf"),
                  ("Serif-Bold", "LiberationSerif-Bold.ttf"),
                  ("Serif-Italic", "LiberationSerif-Italic.ttf"),
                  ("Sans", "LiberationSans-Regular.ttf"),
                  ("Sans-Bold", "LiberationSans-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(nom, f"{FDIR}/{fich}"))

ACCENT = colors.HexColor("#4A90C4")
DARK = colors.HexColor("#162032")
PAGE = landscape(A4)

st_t = ParagraphStyle("t", fontName="Serif-Bold", fontSize=24, leading=30,
                      textColor=DARK, spaceAfter=10)
st_s = ParagraphStyle("s", fontName="Sans-Bold", fontSize=10, leading=14,
                      textColor=ACCENT, spaceAfter=6, spaceBefore=2)
st_b = ParagraphStyle("b", fontName="Serif", fontSize=13.5, leading=19,
                      textColor=colors.HexColor("#1a1a1a"))
st_bv = ParagraphStyle("bv", parent=st_b, fontSize=12.5, leading=18)
st_m = ParagraphStyle("m", fontName="Serif-Italic", fontSize=10.5,
                      leading=15, textColor=colors.HexColor("#5A6B7F"))


def p(x, st=st_b):
    return Paragraph(x, st)


def diapo(titre, sous, corps):
    els = [Spacer(1, 6), Paragraph(titre, st_t), Paragraph(sous, st_s)]
    if isinstance(corps, list):
        els += corps
    else:
        els.append(p(corps, st_bv))
    els.append(Spacer(1, 16))
    els.append(PageBreak())
    return els


def tabl(lignes, largeurs):
    t = Table([[Paragraph(c, st_bv) for c in l] for l in lignes],
              colWidths=largeurs)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#162032")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F0F4F8")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C8D4E0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


story = []

story += diapo(
    "TRIADE — l'écart de session fermé",
    "L'ÉDITION V0.19.3 · LA SESSION 5EY7GMJRA · 19-20 NOVEMBRE 2026",
    [tabl([["Ce que la campagne a découvert", "Ce que le modèle étendu ferme"],
           ["660 divergences d'UNE classe : la falsification du conteneur "
            "pendant une session ouverte — le modèle refusait (garde "
            "canonique-seule), la sentinelle concrète détruisait "
            "(destruction locale, PV, média intact).",
            "La garde alignée sur la sentinelle : falsification offerte "
            "aux DEUX phases — 30 000 traces aux trois graines, ZÉRO "
            "divergence ; exactement les 660 traces de la classe "
            "changées, rien d'autre."]],
          [12.4 * cm, 12.4 * cm]),
     Spacer(1, 8),
     p("La spécification v0.15.3 (aucune règle modifiée — la règle "
       "disait « seule la falsification <i>prouvée</i> détruit » ; le "
       "modèle sous-approximait, il est porté à la lettre) ; le "
       "manuscrit v0.19.3 ; les preuves v0.19.3 ; le Livre v1.3 "
       "inchangé."),
     Spacer(1, 8),
     p("LA LIGNÉE DES ÉDITIONS : v0.19.2 — la transition D81 → séquestre "
       "D183 PRÉPARÉE (D219), le dépôt GitHub PRIVÉ à trancher avant "
       "soumission ; v0.19.3 — la transition VÉCUE (la cérémonie D183 du "
       "19/11, la rotation vérifiée), le dépôt GitHub PUBLIC (D220, le "
       "passage vécu à la décision explicite du maître) et le DOI "
       "Zenodo vivant — la matrice de visibilité honorée jusqu'à sa "
       "dernière marche : le public seulement après la cérémonie VÉCUE "
       "et les rotations vérifiées — la règle tenue, jamais un passage "
       "implicite.")])

story += diapo(
    "Le programme de preuve — 96/96 vert",
    "TLC + APALACHE · LA BATTERIE 5EY7GMJRA — le SMT Apalache aux entiers non bornés",
    [tabl([["Le volet", "Le verdict sur pièces"],
           ["La fidélité", "La chaîne scellée reproduite : TLC 154 états "
            "distincts / 896 générés ; le modèle Python scellé 154/1 152 "
            "(D187). L'étendu : l'espace atteignable INVARIANT — 154 "
            "états, seules les transitions tirées croissent (896 → 926)."],
           ["Les preuves non bornées", "Init ⇒ I et I ∧ Next ⇒ I′ NoError "
            "sur le modèle étendu ; l'alignement TLA+ ↔ Python 13/13 "
            "règles (garde, image, activation) ; le lemme de translation "
            "d'époque LT1/LT2 re-prouvé ; OB1/OB2 ; le compte 288."],
           ["Les contrôles négatifs", "31 ATTRAPÉS — dont l'extension "
            "annulée (la garde v0.15.0 restaurée comme mutation : "
            "l'écart renaîtrait) et la destruction qui déborde sur le "
            "média (I3 violé). L'épinglage TLC : 13 règles, les deux "
            "sens, le contrôle tombe."]],
          [5.6 * cm, 19.2 * cm])])

story += diapo(
    "La campagne — 30 000 traces, zéro divergence",
    "LA GRAINE CONSIGNÉE + DEUX NOUVELLES · LE REJEU BIT-IDENTIQUE DEUX FOIS",
    [tabl([["La graine", "Traces", "Écarts", "Fins par destruction"],
           ["20261112 (consignée)", "10 000", "0", "3 268"],
           ["20261119 (nouvelle)", "10 000", "0", "3 275"],
           ["20261120 (nouvelle)", "10 000", "0", "3 229"]],
          [8 * cm, 4 * cm, 4 * cm, 8.8 * cm]),
     Spacer(1, 8),
     p("Le rejeu à la graine consignée : 10 000/10 000 condensats "
       "bit-identiques à CHAQUE passe — la triple égalité recoupée sur "
       "les CSV. Le recoup à la généalogie : contre le registre v0.18.0, "
       "9 340 digests identiques et 660 divergés — EXACTEMENT la classe "
       "consignée, l'égalité des ensembles vérifiée. Le ddmin prêt, "
       "aucun écart résiduel à réduire. Chaque chemin d'échec couvert "
       "(la porte, le seuil, le piège absent, le rejeu à e=1).")])

story += diapo(
    "Le temps constant — l'égalité hash-vérifiée",
    "LE HASH DES TRACES COMPLÈTES · 6/6 CIBLES · N=60/CLASSE",
    [tabl([["La cible", "Les événements par run", "Les 120 mesures"],
           ["tls13-01..04 (sha-256, le message)", "5 188", "1 seule empreinte"],
           ["tls13-05 (hmac-sha256, la clé)", "20 868", "1 seule empreinte"],
           ["tls13-06 (hkdf-extract, l'IKM)", "20 927", "1 seule empreinte"],
           ["tls13-13/14 (x25519, la clé privée)", "2 159 436",
            "1 seule empreinte — le compte 1 238 959 confirmé DEDANS"],
           ["tls13-15..19 (aes-gcm, la clé)", "16 608", "1 seule empreinte"],
           ["loupe-06 (md5, le contenu)", "155 588", "1 seule empreinte"]],
          [10.4 * cm, 5.2 * cm, 9.2 * cm]),
     Spacer(1, 6),
     p("Chaque run hache sa trace complète — chaque instruction "
       "(adresse, taille) et chaque accès de données (type, adresse, "
       "taille) ; les VALEURS jamais hachées. Le compte unique de la "
       "v0.18.0 demeure, SUBSUMÉ : deux traces de longueurs différentes "
       "ne peuvent partager l'empreinte. Le clone PUBLIC du dépôt, "
       "anonyme — la preuve du « quiconque clone ».")])

story += diapo(
    "Le matériel — le protocole pré-enregistré, en attente",
    "N≥10 RUNS PAR N · ≥2 MACHINES · LA FRÉQUENCE FIXÉE · LES PICS NOMMÉS D'AVANCE",
    [p("Le protocole P1-P8 pré-enregistré AVANT toute donnée : dix "
       "exécutions indépendantes par N ∈ {60, 200, 400}, deux machines "
       "au moins (l'empreinte CPU et l'état EFFECTIF du gouverneur "
       "consignés), l'affinité cœur, l'investigation des pics "
       "tls13-02/tls13-13 à N=200 (les valeurs consignées du témoin "
       "signé : 12,39 et 5,19) — les causes candidates NOMMÉES AVANT "
       "les données : le bruit d'une exécution unique, le cœur partagé, "
       "ou le vrai écart — la répétition tranche, aucune cause élue "
       "d'avance. Le mesureur scellé porté intact ; l'agrégation "
       "fail-closed (un run manquant : REFUS, aucune valeur fabriquée)."),
     Spacer(1, 8),
     p("<b>Aucun chiffre matériel fabriqué</b> — la ligne « wall-clock » "
       "demeure « measured (2 runs, 1 machine) » jusqu'au geste du "
       "développeur. Le kit attend sa main."),
     Spacer(1, 8),
     p("Les résultats mesurés portés (la discipline inter-pièces, "
       "reconduits à l'identique) : la plage RQ2 2,98–11,37× — "
       "l'ère Loupe contre la baseline M1 ; le canon M4 17,9× (l'écart "
       "d'arrondi 17,8× nommé à côté, la pièce R11 demeurant verbatim) ; "
       "les artefacts scellés passeur.exe [61 952 o, 4a7229e7418e8276…] "
       "et passeur-c.dll [102 390 o, fe4ddfc9842fb29b…] intacts ; le "
       "Livre du Coffre v1.3 inchangé. La formulation tenue : la "
       "notation est WYSIWYG — sans aucune chaîne de traduction "
       "optimisante ni opaque, le round-trip rend l'octet pour "
       "l'octet.")])

story += diapo(
    "L'état des pièces — les cinq documents",
    "LE PACK V0.19.3 · CHAQUE EMPREINTE SHA-256 · LE RAPPORT DE VÉRIFICATION",
    [tabl([["La pièce", "L'édition", "Ce qui change"],
           ["Le manuscrit", "v0.19.3 (31 p.)", "L'écart fermé, la table "
            "des statuts portée (4 lignes), l'égalité hash-vérifiée, le "
            "kit pré-enregistré — aucune valeur mesurée modifiée."],
           ["La spécification", "v0.15.3 (66 p.)", "L'alignement du "
            "modèle sur la règle : aucune règle modifiée, la lettre de "
            "la sentinelle rendue explicite aux deux phases, la section "
            "« Ce que change la v0.15.3 »."],
           ["Le Livre du Coffre", "v1.3 (28 p.)", "INCHANGÉ — aucun "
            "geste de cérémonie ne bouge (le runbook scellé D180 : le "
            "scan périodique attend l'édition documentée commandée)."],
           ["Les preuves et calculs", "v0.19.3 (9 p.)", "Les pièces de "
            "la session : le diff exact, la batterie 96/96, la campagne "
            "à zéro, les hash 6/6, le kit matériel."],
           ["La présentation", "20/11 (v0.19.3)", "Le présent document."]],
          [5.6 * cm, 4.4 * cm, 14.8 * cm])])

doc = BaseDocTemplate(OUT, pagesize=PAGE,
                      leftMargin=1.9 * cm, rightMargin=1.9 * cm,
                      topMargin=1.7 * cm, bottomMargin=1.7 * cm,
                      title="TRIADE — présentation du 20/11 (v0.19.3)",
                      author="TRIADE")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame])])
doc.build(story)
print(f"[VERT] {OUT}")

COVER = os.path.join(V7, "presentation_v193_cover.html")
with open(COVER, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>@page { size: A4 landscape; margin: 0; }
body { margin: 0; font-family: 'Liberation Serif', serif; }
.cover { width: 297mm; height: 210mm; background: #162032; color: #fff;
  padding: 26mm 30mm; box-sizing: border-box; }
.kicker { color: #7FB4D8; font-family: 'Liberation Sans', sans-serif;
  font-size: 12pt; letter-spacing: 3px; margin-bottom: 14mm; }
h1 { font-size: 38pt; margin: 0 0 6mm 0; font-weight: normal; }
.sub { font-size: 16pt; color: #B9C8D8; margin-bottom: 20mm; }
.meta { font-size: 11pt; color: #B9C8D8; line-height: 1.8; }
.label { color: #7FB4D8; font-family: 'Liberation Sans', sans-serif;
  font-size: 10pt; margin-bottom: 3mm; }</style></head><body>
<div class="cover"><div class="kicker">TRIADE</div>
<h1>L'écart de session fermé</h1>
<div class="sub">Le modèle align&eacute; sur la sentinelle &middot;
l'&eacute;dition v0.19.3</div>
<div class="label">LA SESSION 5EY7GMJRA</div>
<div class="meta">La campagne : 30 000 traces, z&eacute;ro divergence<br/>
La batterie de preuves : 96/96 vert, 31 contr&ocirc;les attrap&eacute;s<br/>
Le temps constant : l'&eacute;galit&eacute; hash-v&eacute;rifi&eacute;e, 6/6 cibles<br/>
Le kit mat&eacute;riel pr&eacute;-enregistr&eacute; &mdash; en attente du geste</div>
</div></body></html>""")
subprocess.run(["weasyprint", COVER,
                os.path.join(V7, "presentation_v193_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(os.path.join(V7, "presentation_v193_cover.pdf")).pages[0])
for pg in PdfReader(OUT).pages:
    w.add_page(pg)
w.add_metadata({"/Title": "TRIADE — présentation du 20/11 (v0.19.3)"})
FINAL = os.path.join(V7, "TRIADE_presentation_20261120_v193.pdf")
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(FINAL).pages)} pages)")
