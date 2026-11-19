#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_preuves_v193.py — le corps du document
TRIADE_preuves_et_calculs_v0.19.3.pdf (ReportLab) : les pièces de la
session 5ey7gmjra — l'écart de session fermé. La structure hérite de la
v0.19.2 ; les pièces verbatim (la batterie, la campagne, les hash) sont
LUES de l'atelier — jamais retapées."""
import os
import subprocess

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

REPO = "/home/z/my-project/depot"
V7 = os.path.join(REPO, "scripts", "vague7")
OUT = os.path.join(V7, "preuves_v193_body.pdf")
AT = os.path.join(REPO, "atelier-cf3-5ey7gmjra")

FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", f"{FDIR}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", f"{FDIR}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Italic", f"{FDIR}/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans", f"{FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", f"{FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", f"{FDIR}/LiberationMono-Regular.ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold",
                              italic="Serif-Italic", boldItalic="Serif-Bold")

ACCENT = colors.HexColor("#4A90C4")
DARK = colors.HexColor("#162032")

st_body = ParagraphStyle("body", fontName="Serif", fontSize=9.6, leading=14.2,
                         alignment=TA_LEFT, spaceAfter=7,
                         textColor=colors.HexColor("#1a1a1a"))
st_h1 = ParagraphStyle("h1", fontName="Serif-Bold", fontSize=16.5, leading=21,
                       textColor=DARK, spaceBefore=14, spaceAfter=8)
st_h2 = ParagraphStyle("h2", fontName="Sans-Bold", fontSize=11, leading=15,
                       textColor=ACCENT, spaceBefore=10, spaceAfter=5)
st_mono = ParagraphStyle("mono", fontName="Mono", fontSize=7.4, leading=9.6,
                         textColor=colors.HexColor("#222222"))
st_titre = ParagraphStyle("titre", fontName="Serif-Bold", fontSize=21,
                          leading=26, textColor=DARK, spaceAfter=4)


def lit(nom):
    with open(os.path.join(AT, nom), encoding="utf-8") as f:
        return f.read().splitlines()


def para(txt, st=st_body):
    return Paragraph(txt.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;"), st)


def encadre(titre, lignes, garde=40):
    corps = lignes[:garde]
    flux = [Paragraph(titre, st_h2)]
    txt = "<br/>".join(x.replace(" ", "&nbsp;") for x in corps)
    t = Table([[Paragraph(txt, st_mono)]], colWidths=[16.6 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F7FA")),
        ("BOX", (0, 0), (-1, -1), 0.6, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    flux.append(t)
    if len(lignes) > garde:
        flux.append(para(f"<i>… {len(lignes) - garde} lignes suite à la "
                         f"pièce de l'atelier ({titre.split('—')[0].strip()})"
                         f"</i>"))
    return flux


story = [
    Paragraph("TRIADE — preuves et calculs", st_titre),
    para("<b>Édition v0.19.3 — l'écart de session fermé</b> (l'instruction "
         "5ey7gmjra, la vague du 18/11, la troisième). Les pièces de la "
         "session, lues de l'atelier "
         "<code>atelier-cf3-5ey7gmjra/</code> du dépôt public — chaque "
         "nombre lu des artefacts, jamais retapé."),
    para("LE MANDAT : fermer l'écart modèle↔implémentation du coffre CF3 "
         "(la falsification pendant une session ouverte — les 660 "
         "divergences de la campagne v0.18.0, consignées comme la "
         "découverte), durcir la preuve temps constant (le hash des traces "
         "complètes), décharger symboliquement l'uniformité d'époque sur le "
         "modèle étendu, et préparer le kit de mesure matérielle "
         "pré-enregistré — EN ATTENTE, aucun chiffre fabriqué."),
    PageBreak(),
]

# (1) le modèle étendu + le diff
story += [Paragraph("1. Le modèle étendu — CF3Etendu.tla "
                    "(la spécification v0.15.3)", st_h1),
          para("La règle 4 (FalsifieConteneur) : la garde devient le piège "
               "intègre seul — la falsification prouvée offerte aux DEUX "
               "phases (la session ouverte comprise), l'effet inchangé : "
               "destruction LOCALE, PV, le média et les fragments INTACTS. "
               "Les DOUZE autres règles demeurent la copie de la v0.15.0 "
               "scellée. Le résultat historique (660 divergences, une "
               "classe) DEMEURE consigné append-only — la découverte qui "
               "motiva l'extension. Le diff intégral des modules étendus :")]
story += encadre("DIFF-MODULES-ETENDUS.txt — le diff exact (80 lignes)",
                 lit("DIFF-MODULES-ETENDUS.txt"), garde=44)

# (2) la batterie — 96/96
story += [PageBreak(),
          Paragraph("2. La batterie de preuves — 96/96 VERT "
                    "(TLC + Apalache, SMT entiers non bornés)", st_h1),
          para("Le pré-vol : la chaîne SCELLÉE reproduite (TLC 154 états "
               "distincts / 896 générés, profondeur 7, le journal aux "
               "lignes de fond identiques au consigné ; le modèle Python "
               "scellé : 154/1 152 — D187 reproduit). L'ÉTENDUE : l'espace "
               "atteignable INVARIANT (154 états distincts — l'extension "
               "n'ajoute AUCUN état, seules les transitions tirées "
               "croissent 896 → 926 : la falsification offerte en "
               "session). Les preuves non bornées : Init⇒I et I∧Next⇒I′ "
               "NoError ; l'alignement 13/13 règles (garde, image, "
               "activation) ; le lemme de translation LT1/LT2 ; OB1/OB2 ; "
               "le compte 288. Les contrôles négatifs : 31 ATTRAPÉS — "
               "dont l'EXTENSION ANNULÉE (la garde v0.15.0 restaurée comme "
               "mutation : l'écart des 660 traces renaîtrait — ATTRAPÉ) et "
               "le débordement sur le média (I3 violé — ATTRAPÉ). "
               "L'épinglage TLC : 13 règles, les DEUX sens, + son "
               "contrôle (l'invariant du pin TOMBE).")]
story += encadre("RAPPORT-BATTERIE-5EY7GMJRA.txt — les 96 verdicts",
                 lit("RAPPORT-BATTERIE-5EY7GMJRA.txt"), garde=60)

# (3) la campagne
story += [PageBreak(),
          Paragraph("3. La campagne générative — 30 000 traces, "
                    "ZÉRO divergence", st_h1),
          para("Trois graines (la consignée 20261112 + les nouvelles "
               "20261119/20261120), 10 000 traces chacune, 3-8 pas, "
               "chaque règle et chaque chemin de refus couvert ; le "
               "rejeu bit-identique DEUX fois à la graine consignée "
               "(10 000/10 000 à chaque passe, la triple égalité "
               "recoupée). Le recoup à la généalogie : contre le registre "
               "v0.15.0 — 9 340 condensats IDENTIQUES, 660 DIVERGÉS : "
               "EXACTEMENT la classe des écarts consignés, l'égalité des "
               "ensembles vérifiée, RIEN d'autre changé. Le ddmin : "
               "prêt (la machine v150), AUCUN écart résiduel à réduire.")]
story += encadre("RAPPORT-CAMPAGNE-PBT-5EY7GMJRA.txt — les trois campagnes",
                 lit("RAPPORT-CAMPAGNE-PBT-5EY7GMJRA.txt"), garde=54)

# (4) l'instrument hash
story += [PageBreak(),
          Paragraph("4. L'instrument temps constant durci — le hash des "
                    "traces complètes", st_h1),
          para("La promotion de l'instrument : chaque run hache sa trace "
               "COMPLÈTE — chaque instruction (adresse, taille), chaque "
               "accès mémoire de données (type, adresse, taille) ; les "
               "VALEURS jamais hachées. Les 6 cibles, N=60/classe, la "
               "graine consignée 20261119, le clone PUBLIC du dépôt "
               "(anonyme — la preuve du « quiconque clone ») : UNE "
               "seule empreinte par cible sur les 120 mesures — le compte "
               "unique demeure, SUBSUMÉ par le hash (x25519 : "
               "1 238 959 confirmé dedans).")]
story += encadre("RAPPORT-TRACES-HASH-V190.txt — les 6 cibles",
                 lit("RAPPORT-TRACES-HASH-V190.txt"), garde=30)

# (5) le kit matériel
story += [PageBreak(),
          Paragraph("5. Le kit de mesure matérielle pré-enregistré — "
                    "EN ATTENTE", st_h1),
          para("Le protocole P1-P8 pré-enregistré AVANT toute donnée : "
               "n≥10 exécutions indépendantes par N ∈ {60, 200, 400}, "
               "≥2 machines (l'empreinte et l'état EFFECTIF de la "
               "fréquence consignés), l'affinité cœur, l'investigation "
               "des pics tls13-02/tls13-13 à N=200 (les causes "
               "candidates NOMMÉES D'AVANCE — le bruit d'horloge, le "
               "cœur partagé, le vrai écart : les données tranchent, "
               "aucune cause élue d'avance), le critère au seuil "
               "médian, l'agrégation fail-closed. Le mesureur SCELLÉ "
               "dudect_v150.c [8c90ef82…] porté INTACT. AUCUN chiffre "
               "matériel fabriqué : la ligne « wall-clock » de la table "
               "des statuts demeure « measured (2 runs, 1 machine) » "
               "jusqu'au geste du développeur.")]
story += encadre("KIT-MESURE-MATERIELLE-V190/LISEZMOI — le protocole P1-P8",
                 lit("KIT-MESURE-MATERIELLE-V190/LISEZMOI-kit-materiel.txt"),
                 garde=40)

# (6) LES PIÈCES PERMANENTES (la discipline inter-pièces : les valeurs
#     partagées portées par TOUS les packs — la v0.19.3 les reconduit)
story += [PageBreak(),
          Paragraph("6. Les pièces permanentes — les valeurs partagées "
                    "reconduites", st_h1),
          para("Les artefacts scellés (re-téléchargés en double passe "
               "byte-byte aux archives du coffre — unite-14-app / "
               "unite-13-app, D204) : passeur.exe v0.2 (T) — "
               "<b>61952 o</b> (61 952), sha256 <b>4a7229e7418e8276…</b> ; "
               "passeur-c.dll v0.2 (C) — <b>102390 o</b> (102 390), "
               "sha256 <b>fe4ddfc9842fb29b…</b> ; loupe.exe 0.1.1 scellé "
               "<b>c1115105…</b> ; proxy.exe <b>446279f3…</b>. INTACTS == "
               "les valeurs consignées. LE SCEAU DE L'INTENTION : les "
               "QUATORZE arbres signés (D177) — la garde courue au dépôt, "
               "14/14 VERTS."),
          para("LA FALSIFICATION (D219) — l'autotest du kit de séquestre "
               "rafraîchi (v0.19.2, reconduit) : les 10/10 combinaisons "
               "de 3 parts exactes reconstituent, les 10/10 paires sous "
               "le seuil inertes (rien ne fuit), et la part forgée "
               "REFUSÉE par la porte de l'empreinte de contrôle — le "
               "contrôle négatif qui prouve que le REFUS vient de la "
               "falsification, pas d'une porte muette."),
          para("Les résultats mesurés portés : la plage RQ2 "
               "<b>2,98–11,37×</b> attribuée à <b>l'ère Loupe contre la "
               "baseline M1</b> (jamais l'inverse) ; le canon M4 "
               "<b>17,9×</b> (39,3/2,2, la première exécution de la liste "
               "optimisée) — l'écart d'arrondi <b>17,8×</b> NOMMÉ à côté "
               "(la pièce R11 verbatim calcule 17,8 sur la seconde : "
               "l'écart dit tel quel, la pièce demeurant verbatim). Le "
               "Livre du Coffre v1.3 — le document de cérémonie, "
               "INCHANGÉ par la présente édition (aucun geste ne bouge ; "
               "le runbook scellé D180 : l'entrée du scan périodique "
               "attend l'édition documentée commandée du maître)."),
          Spacer(1, 8)]

# (7) la table des statuts
story += [
          Paragraph("6. La table des statuts — les quatre lignes "
                    "portées", st_h1),
          para("Écart de session → FERMÉ (le modèle étendu, la campagne à "
               "zéro, exactement les 660 changées) ; preuves non bornées "
               "→ couvrant désormais la falsification en session "
               "(l'alignement 13/13 re-déchargé, 31 contrôles attrapés) ; "
               "égalité de traces → HASH-VÉRIFIÉE (une empreinte par "
               "cible sur 120 mesures) ; wall-clock → le protocole "
               "pré-enregistré livré en attente. La table complète vit au "
               "manuscrit v0.19.3 (§ résultats) et à la spécification "
               "v0.15.3 (§ Ce que change la v0.15.3)."),
          para("<b>LE VERDICT DE LA SESSION : VERT</b> — les quatre points "
               "de l'instruction exécutés en leur lettre ; le pack "
               "refusé si un seul contrôle est rouge — aucun ne l'est."),
          Spacer(1, 8),
          para("<i>Les pièces complètes vivent à "
               "atelier-cf3-5ey7gmjra/ du dépôt public (github.com/"
               "alexisfrlopez-debug/triade) : les modules TLA+ étendus, "
               "les 92 configs de run, les journaux d'outils (logs/), les "
               "CSV de campagne, le jsonl des 720 runs de hash, le kit "
               "matériel. Reproduction : python3 "
               "jouer_batterie_5ey7gmjra.py A|B|C|D ; python3 "
               "pbt_raffinement_v153.py --debut 0 --fin 10000 ; python3 "
               "egalite_traces_hash_v190.py --cible … --bilan.</i>")]

doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                      topMargin=2.0 * cm, bottomMargin=2.0 * cm,
                      title="TRIADE — preuves et calculs v0.19.3",
                      author="TRIADE")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame])])
doc.build(story)
print(f"[VERT] {OUT}")

# la couverture + la fusion (le motif v192)
COVER_HTML = os.path.join(V7, "preuves_v193_cover.html")
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
<div class="sub">L'écart de session fermé — l'édition v0.19.3</div>
<div class="label">PIÈCES DE LA SESSION 5EY7GMJRA</div>
<div class="meta">
Le modèle CF3 étendu — la falsification offerte en session ouverte<br/>
La campagne générative : 30 000 traces, zéro divergence<br/>
La batterie TLC + Apalache : 96/96 vert, 31 contrôles négatifs attrapés<br/>
L'instrument temps constant : le hash des traces complètes, 6/6 cibles<br/>
Le kit de mesure matérielle pré-enregistré — en attente
</div>
<div class="rule"></div>
<div class="meta">Document de preuve &middot; s&eacute;rie TRIADE &middot;
&eacute;dition v0.19.3 &middot; 19 novembre 2026</div>
</div></body></html>""")
subprocess.run(["weasyprint", COVER_HTML,
                os.path.join(V7, "preuves_v193_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter  # noqa: E402
w = PdfWriter()
w.add_page(PdfReader(os.path.join(V7, "preuves_v193_cover.pdf")).pages[0])
for p_ in PdfReader(OUT).pages:
    w.add_page(p_)
w.add_metadata({"/Title": "TRIADE — preuves et calculs v0.19.3"})
FINAL = os.path.join(V7, "TRIADE_preuves_et_calculs_v0.19.3.pdf")
with open(FINAL, "wb") as f:
    w.write(f)
print(f"[VERT] {FINAL} ({len(PdfReader(FINAL).pages)} pages)")
