#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_preuves_v233.py — le document TRIADE_preuves_et_calculs_v0.23.3.pdf
(ReportLab + weasyprint + pypdf, le modèle v232 reconduit) : les pièces de
la vague 15 lues VERBATIM de leurs rapports (jamais retapées) — LES
DIX-SEPT INSTRUCTIONS en deux sessions (les quatre de l'Entrée 386 + les
treize de l'Entrée 387), LA CONSIGNATION DE LA GÉNÉRATION v0.23.3 (la
release de la vague 15 — la commande du maître « ok pour la suite (release
de la vague etc…) » : LES CINQ PIÈCES RÉGÉNÉRÉES au linter v2), L'ERRATUM
du rejeu TCB (l'invocation corrigée, le rapport demeuré verbatim), la
table des empreintes des cinq pièces de l'édition."""
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
ICI = REPO / "scripts" / "vague15"

# LES DIX-SEPT ATELIERS DE LA VAGUE 15 (l'ordre d'exécution consigné)
ATELIERS = [
    ("(1) CF3-VERS-LE-VERDICT — qa3k5putf (l'Entrée 386)",
     REPO / "atelier-cf3-verdict-qa3k5putf" / "rapport-cf3-verdict.txt"),
    ("(2) LA MESURE DE COMPOSITION — 2sown2h3z (l'Entrée 386)",
     REPO / "atelier-entrelacement-2sown2h3z" / "rapport-entrelacement.txt"),
    ("(3) L'OUTIL FEEDBACK — witgt6qta (l'Entrée 386)",
     REPO / "atelier-feedback-witgt6qta" / "rapport-atelier.txt"),
    ("(4) LE TRIAGE DES RAPPORTS — e1lr9i8ts (l'Entrée 386)",
     REPO / "atelier-triage-e1lr9i8ts" / "rapport-atelier.txt"),
    ("(5) LES GARDES VIVANTES ET LE TCB 58→34→11 — k69mvt43j",
     REPO / "atelier-gardes-tcb-k69mvt43j" / "rapport-atelier.txt"),
    ("(6) LE MOTEUR NATIF D'ORACLES — 8hguph5ee",
     REPO / "atelier-oracles-8hguph5ee" / "rapport-atelier.txt"),
    ("(7) TPL-ADD-v5 : LA CIBLE MANQUÉE — yfkpml1j2",
     REPO / "atelier-ajouter-v5-yfkpml1j2" / "rapport-atelier.txt"),
    ("(8) LES TROIS GAPS DE VALIDITÉ — ab2vh5c2m",
     REPO / "atelier-validite-ab2vh5c2m" / "rapport-atelier.txt"),
    ("(9) LE DATASET DE RÉPLICATION (LE TRIO D122) — 0i4pkzbyr",
     REPO / "atelier-dataset-0i4pkzbyr" / "rapport-atelier.txt"),
    ("(10) LE CORPUS D'ENTRAÎNEMENT — 2i7iy3xmg",
     REPO / "atelier-corpus-2i7iy3xmg" / "rapport-atelier.txt"),
    ("(11) TRIADE-GYM — 3x9cf4e5d",
     REPO / "atelier-gym-3x9cf4e5d" / "rapport-atelier.txt"),
    ("(12) L'EVAL RE-JOUABLE — vpcr7mh3t",
     REPO / "atelier-eval-vpcr7mh3t" / "rapport-atelier.txt"),
    ("(13) LE GUIDE D'AGENT — zd316de39",
     REPO / "atelier-guide-zd316de39" / "rapport-atelier.txt"),
    ("(14) LA DOC EN (LE NOYAU) — m8qc10sxg",
     REPO / "atelier-doc-m8qc10sxg" / "rapport-atelier.txt"),
    ("(15) LE KIT DÉVELOPPEUR PAR CONSTRUCTION — v2n6v8rao",
     REPO / "atelier-kit-v2n6v8rao" / "rapport-atelier.txt"),
    ("(16) LES PROTOCOLES MATÉRIELS — gzxvze3py",
     REPO / "atelier-materiel-gzxvze3py" / "rapport-atelier.txt"),
    ("(17) LE LINTER v2 ET LA COHÉRENCE — vxf37231r",
     REPO / "atelier-coherence-vxf37231r" / "rapport-atelier.txt"),
]

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

OUT = ICI / "preuves_v233_body.pdf"
doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=52, rightMargin=52,
                      topMargin=56, bottomMargin=52,
                      title="TRIADE preuves v0.23.3", author="TRIADE")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin,
                          doc.width, doc.height, id="f")])])
FLOTS = []


def para(t, s=S_P):
    FLOTS.append(Paragraph(t, s))


def verbatim(chemin, limite=64000, titre=""):
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


para("TRIADE — preuves et calculs, l'édition v0.23.3 (la vague 15, la "
     "release)", S_T)
para("Les pièces verbatim des dix-sept ateliers de la quinzième vague, "
     "lues de leurs rapports — jamais retapées ; la consignation de la "
     "génération v0.23.3 (les cinq pièces régénérées sous le linter v2 à "
     "cinq classes) ; l'erratum append-only du rejeu TCB ; la table des "
     "empreintes des cinq pièces de l'édition.")
para("LA GÉNÉRATION v0.23.3 (la release de la vague 15 — la commande du "
     "maître « ok pour la suite (release de la vague etc…) »)", S_H)
para("La vague 15 close à l'Entrée 387 (les dix-sept instructions exécutées "
     "en deux sessions, les instructions archivées au coffre, le "
     "/instructions laissé vide), la release porte LES CINQ PIÈCES "
     "RÉGÉNÉRÉES au linter v2 de vxf37231r (les cinq classes : les phrases "
     "sémantiques retirées — la formulation exacte D182 portée à la spec "
     "§1, le compilateur N'EST JAMAIS LIVRÉ, la notation scellée l'est —, "
     "les plages décisionnelles annoncées contre les entrées listées, les "
     "séquences de faisabilité n/18 datées partout — la campagne courante "
     "v5 (nov. 2026) nommée à part à 5/18, LA CIBLE MANQUÉE, la lecture défavorable "
     "consignée —, les claims DOI/version post-dépôt à la version courante "
     "v0.23.2, les gallicismes EN guéris : « settled on pieces », la "
     "formulation anglaise des cinq parts à seuil trois). LE CORPS PORTÉ : "
     "la composition 0,7271 c/octet@4096 (la médiane 2 978,2 c [IQR 5,6] "
     "par appel de 4 096 octets ; la cible ≤2,0 TENUE au 36 % ; OpenSSL "
     "EVP 0,5757 — 2 357,9 c [IQR 19,3] — au même silicium : le couloir à "
     "1,26× de la bibliothèque réglée ; la chaîne scellée 49,9376 — "
     "204 544,5 c — : le couloir 68,7× devant, aucun contrôle retiré) ; "
     "le TCB réduit 58→34→11 (le corridor des ONZE "
     "gardes OS émis à la marge vierge 0xFC00 — 424 o, 116 instr, LE "
     "HARNAIS 36/36, le coût du dispatch nommé 22 contre 7) ; le moteur "
     "d'oracles natif au jumeau Unicorn LIGNE-IDENTIQUE aux deux corps "
     "scellés (la mémo content-addressed, le gate, l'audit 1-sur-10 "
     "chaîné ; les médianes 0,960 ms → 0,000185 ms au hit — LE GAIN "
     "5189× aux opérandes non arrondis ; la composition avec la mémo de "
     "régime v14 (24,163 → 2,555 s = −89,4 %) : les mécanismes "
     "ORTHOGONAUX) ; TPL-ADD-v5 (nov. 2026) 5/18 — la cible "
     "≥15/18 MANQUÉE, le coût médian 4 604 (la cible ≤4 500 manquée de "
     "104), LA LECTURE DÉFAVORABLE CONSIGNÉE (la variance du sujet AU CLI "
     "nommée — les trois pertes avaient verti à la v4 aux mêmes prompts — "
     "les juges INTACTS) ; H7 SERVIE aux 28 unités (le générateur "
     "re-exécuté BIT-IDENTIQUE au sha canonique 2de7d488, l'agrégateur "
     "fail-closed au plafond D207 vécu au refus, le second annotateur "
     "re-autotesté, le confound 1,5B NOMMÉ 0/64) ; CF3-v3 AU VERDICT "
     "MACHINE (L3 VERIFIED 1 122 pas ; les cinq autres lemmes INCOMPLETE "
     "au mur de mémoire 4 Go — la cause nommée, la voie du poste réel ; "
     "le port ProVerif livré, les six écarts de sémantique nommés) ; "
     "l'ÉCOSYSTÈME D'ADOPTION (le corpus aux 109 triples — les splits "
     "recalculés des fichiers mêmes 28/4/4 tâches · 77/16/16 triples, le "
     "TEST sans dorée, le canari unique —, le gym à la récompense typée, "
     "la ladder re-jouable, le guide d'agent, la doc EN au noyau 216/167 "
     "tokens, le kit aux 156 pièces SANS AUCUNE ancre expédiée, les "
     "protocoles matériels pré-enregistrés, le linter v2 au contrôle "
     "négatif 5/5).")
para("LES DEUX ERRATA DE PASSE NOMMÉS À LA PRÉPARATION DE LA RELEASE "
     "(la recomposition par code des fichiers mêmes)", S_H)
para("(1) LE REJEU TCB : la passe consignée au rapport k69mvt43j invoquait "
     "z3 avec l'option d'entrée standard ET un argument fichier — la "
     "sortie vide, les 116 verdicts consignés vides (0/58, 0/58, 116 "
     "écarts : la trace demeure, un échec mesuré est une pièce aussi "
     "précieuse qu'un vert) ; LA PASSE CORRIGÉE (z3 <fichier>) : 58 "
     "décharges UNSAT + 58 mutations SAT, ZÉRO écart — l'erratum vit "
     "APPEND-ONLY au registre (registres/rejeu-erratum-invocation.txt, la "
     "pièce verbatim ci-dessous), le rapport et le harnais demeurés octet "
     "pour octet. (2) LES SPLITS DU CORPUS : le rapport 2i7iy3xmg porte "
     "les comptes de la première passe (25 tâches / 69 lignes · 3/12 · "
     "4/16 — la passe AVANT l'admission des 13 triples du faux positif "
     "/Home/End, 97 ≠ 109 : la coquille interne nommée) ; la "
     "recomposition des fichiers livrés (le manifeste au sha256) : "
     "28/4/4 tâches · 77/16/16 triples = 109 — les valeurs de la voix "
     "courante portées aux pièces, le rapport demeuré verbatim.")
para("LA LECTURE DES ATELIERS (verbatims)", S_H)
for titre, chemin in ATELIERS:
    verbatim(chemin, titre=titre)
para("L'ERRATUM DU REJEU TCB (append-only — la pièce verbatim)", S_H)
verbatim(REPO / "atelier-gardes-tcb-k69mvt43j" / "registres" /
         "rejeu-erratum-invocation.txt")
para("LA COUPURE AU BORD DE LIGNE (la règle reconduite des v0.21.0/"
     "v0.23.0/v0.23.2) : le verbatim des rapports d'atelier INTÉGRAL par "
     "défaut — aucune troncature au milieu d'un mot, chaque ligne "
     "entière.")
para("LA TABLE DES EMPREINTES DES CINQ PIÈCES v0.23.3", S_H)
pieces = {
    "TRIADE_manuscrit_v0.23.3.pdf": REPO / "edition-v0230" / "main.pdf",
    "Protocole_TRIADE_v0.15.8_Specification.pdf":
        REPO / "scripts" / "spec_v158" / "main.pdf",
    "Livre_du_Coffre_TRIADE_CF1-CF3_v1.7.pdf":
        REPO / "scripts" / "livre_v17" / "final.pdf",
}
for nom, chemin in sorted(pieces.items()):
    if chemin.exists():
        para(nom + " — sha256 " +
             hashlib.sha256(chemin.read_bytes()).hexdigest(), S_M)
para("TRIADE_preuves_et_calculs_v0.23.3.pdf — la présente (l'empreinte "
     "consignée au manifeste du pack).", S_M)
para("TRIADE_presentation_v233.pdf — la présentation (l'empreinte "
     "consignée au manifeste du pack).", S_M)
doc.build(FLOTS)
print("[preuves v233] le corps : " + str(OUT))

COVER = ICI / "preuves_v233_cover.html"
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
<div class="s">La quinzi&egrave;me vague — la release
v0.23.3 : la composition 0,7271 c/octet@4096 (la cible tenue au
36&nbsp;%), le TCB r&eacute;duit 58&rarr;34&rarr;11, le moteur
d'oracles natif &agrave; 5189&times;, la campagne v5 (nov.&nbsp;2026)
&agrave; 5/18 (la cible
manqu&eacute;e, la lecture consign&eacute;e), les dix-sept ateliers
verbatim, l'erratum du rejeu, les empreintes crois&eacute;es</div>
<div class="f">S&eacute;rie TRIADE &middot; &eacute;dition v0.23.3 &middot; 23 novembre 2026
&middot; les pi&egrave;ces verbatim, les empreintes crois&eacute;es</div>
</div></body></html>""", encoding="utf-8")
subprocess.run(["weasyprint", str(COVER), str(ICI / "preuves_v233_cover.pdf")],
               check=True)

from pypdf import PdfReader, PdfWriter
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "preuves_v233_cover.pdf")).pages[0])
for p in PdfReader(str(OUT)).pages:
    w.add_page(p)
w.add_metadata({"/Title": "TRIADE preuves v0.23.3"})
FINAL = ICI / "TRIADE_preuves_et_calculs_v0.23.3.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print("[preuves v233] LA PIÈCE : " + str(FINAL) + " (" +
      str(len(PdfReader(str(FINAL)).pages)) + " pages)")
