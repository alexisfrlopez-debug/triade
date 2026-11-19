#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_presentation_v194.py — le corps du document de présentation du
20/11, l'édition v0.19.4 (le coût de la boucle sous R11). La structure
hérite de la v0.19.3 ; les chiffres sont ceux d'OPT-04, lus des
rapports de l'atelier."""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

V7 = "/home/z/my-project/depot/scripts/vague7"
OUT = os.path.join(V7, "presentation_v194_body.pdf")

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
    para("Édition v0.19.4 — le coût de la boucle sous R11 (l'instruction "
         "cq01qv1za, la vague du 18/11, la quatrième)", st_sous),
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
         "unique est close : quatre unités de campagne aux deux bras, les "
         "verdicts explicites, le dépôt public et le DOI Zenodo vivant."),
    para("LE COÛT DE LA BOUCLE — LES TROIS LEVIERS D'OPT-04", st_h1),
    para("(1) LE POINTEUR SEUL au format de réponse de localiser : l'agent "
         "rend l'identifiant d'entrée et l'empreinte sha256 de la "
         "notation — deux champs littéraux — et le CLIENT expande le "
         "pointeur auprès de la carte (quatre refus nommés fail-closed). "
         "Mesuré sur 18 appels réels au tokenizer natif, la même graine "
         "qu'OPT-02 : le total 1 714 → 1 103 tokens (−35,7 %), la réponse "
         "770 → 52 (−93,3 %), zéro divergence, l'expansion 18/18. "
         "(2) LE MÉMO SCELLÉ V2 des ouvertures de session : la clé porte "
         "le bloc, l'entrée, le contrat, la configuration de l'émulateur "
         "et la graine (l'instruction) ; le compteur de runs vit dans le "
         "cœur signé — l'audit 1 run sur 10, la re-exécution vivante, la "
         "preuve d'identité champ à champ. (3) LE DOUBLE MOTEUR "
         "d'émulation : QEMU-user pour le volume (un lanceur C statique "
         "qui exécute les mêmes octets scellés aux mêmes adresses, "
         "l'image bâtie par le vrai harnais), Unicorn pour l'échantillon "
         "d'audit consigné — DIVERGENCE 0, octet pour octet, sur 2 041 "
         "opérations ; un shim muté est attrapé à la première ligne."),
    para("LA TABLE DES STATUTS — L'HYPOTHÈSE H5 RETENUE", st_h1),
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
    para("Le ratio M4 : l'avant 39,7 s contre le bras C 2,2 s = 17,9× ; le "
         "régime 6,8 s contre 2,2 s = 3,0× — sous le seuil ×10. Les 24 "
         "consoles d'oracles capturées (5 avant re-mesurés, le froid, 5 "
         "chaud, l'audit) identiques ligne à ligne aux originales : "
         "aucune graine supprimée, aucun vecteur réduit, aucune "
         "vérification retirée."),
    para("L'ÉTAT DES ÉDITIONS", st_h1),
    Table(
        [[cell("Pièce"), cell("Édition"), cell("Ce qu'elle porte")],
         [cell("Le manuscrit"), cell("v0.19.4"),
          cell("L'édition du coût de la boucle : le pointeur seul, la "
               "pile mémo v2 + double moteur, H5 tenue (l'amendement du "
               "maître)")],
         [cell("La spécification"), cell("v0.15.4"),
          cell("Le pointeur seul — une règle ADDITIVE à localiser, "
               "aucune règle modifiée (D222)")],
         [cell("Le Livre du Coffre"), cell("v1.3"),
          cell("INCHANGÉ (aucun geste de cérémonie ne bouge)")],
         [cell("Les preuves et calculs"), cell("v0.19.4"),
          cell("Les pièces OPT-04 verbatim : la campagne pointeur, le "
               "rapport M4, les cinq contrôles négatifs")],
         [cell("La présentation"), cell("20/11 (v0.19.4)"),
          cell("Le présent document.")]],
        colWidths=[85, 80, 283]),
    Spacer(1, 6),
    para("LE DÉPÔT : PUBLIC (D220 — le passage public vécu à la décision "
         "explicite du maître le 19/11, la cérémonie D183 vécue, la "
         "rotation vérifiée, le re-scan trié : la matrice parcourue "
         "jusqu'au bout) ; le DOI Zenodo vivant : 10.5281/zenodo.24367344. "
         "github.com/alexisfrlopez-debug/triade"),
]

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2 * 2.834,
                      rightMargin=2 * 2.834, topMargin=2 * 2.834,
                      bottomMargin=2 * 2.834,
                      title="TRIADE — présentation du 20/11 (v0.19.4)")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width,
                          doc.height, id="f")])])
doc.build(story)
print("écrit:", OUT)
