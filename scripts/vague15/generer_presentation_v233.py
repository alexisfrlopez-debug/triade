#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_presentation_v233.py — la présentation de la vague 15 à l'édition
v0.23.3 (la release — la commande du maître « ok pour la suite (release de
la vague etc…) ») : la composition mesurée, le TCB réduit, le moteur
d'oracles natif, TPL-ADD-v5 (la cible manquée, la lecture défavorable
consignée), la validité externe servie, CF3-v3 au verdict machine,
l'écosystème d'adoption, le linter v2 et la génération elle-même — LES
EMPREINTES SHA-256 des quatre autres pièces GRAVÉES (la convention : aucun
document ne porte son propre sha256, le manifeste du pack porte les cinq)."""
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
ICI = REPO / "scripts" / "vague15"
OUT = ICI / "presentation_v233_body.pdf"

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

story = []


def para(t, s=None):
    story.append(Paragraph(t, s or st_p))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


para("TRIADE — la présentation de la vague 15, la release v0.23.3",
     st_titre)
para("L'édition v0.23.3 : LES CINQ PIÈCES RÉGÉNÉRÉES sous le linter v2 à "
     "cinq classes (les phrases sémantiques, les plages décisionnelles, "
     "les faisabilités datées, les versions post-dépôt, les gallicismes "
     "EN), les trois packs assemblés à la version courante ; la vague 15 : "
     "la composition 0,7271 c/octet@4096, le TCB 58→34→11, le moteur "
     "d'oracles natif à 5189×, la campagne v5 (nov. 2026) à 5/18 (la "
     "cible manquée, la lecture consignée), H7 servie, CF3-v3 au verdict "
     "l'écosystème d'adoption ; le concept DOI 10.5281/zenodo.24367343 "
     "résout sur la version courante (le dépôt public D220)", st_sous)

para("LES SEPT POINTS DE LA SESSION", st_h1)
para("1 · LA MESURE DE COMPOSITION (2sown2h3z) — le couloir ctr-v4i-ghash-"
     "agrege4 à la marge vierge 0xF800 (1 295 o, 274 instr, round-trip "
     "VERT, la différentielle 320/320 ZÉRO ÉCART, le mutant imm8 ATTRAPÉ "
     "au premier vecteur, le repli 32/32, les bornes N≤256 fail-closed "
     "vécues, la table des puissances DÉRIVÉE PAR LE SCELLÉ) : 0,7271 "
     "c/octet@4096 — la médiane 2 978,2 c [IQR 5,6] par appel de 4 096 "
     "octets (n=20, le cœur épinglé, la machine virtualisée NOMMÉE) ; LA "
     "CIBLE PRÉ-ENREGISTRÉE ≤ 2,0 TENUE au 36 % de la cible ; OpenSSL EVP "
     "AES-128-GCM à la même entrée : 0,5757 c/octet@4096 (2 357,9 c [IQR "
     "19,3]) — le couloir à 1,26× de la bibliothèque réglée au même "
     "silicium ; LE REPLI (la chaîne scellée par bloc) : 49,9376 "
     "c/octet@4096 — 204 544,5 c [IQR 7 223,5] — le couloir 68,7× DEVANT "
     "(204 544,5/2 978,2), aucun contrôle retiré ; LA "
     "PARITÉ AU RIG (les 4 112 octets identiques, la garde verte avant la "
     "mesure) ; la décomposition 11,63 c/bloc = CTR 4,76 + GHASH agrégé "
     "4,92 + jointure 1,95 — la projection v14 (~1,6) DÉPASSÉE par la "
     "mesure (0,73), jamais une projection présentée comme mesure.")
para("2 · LE TCB RÉDUIT 58→34→11 ET LE CORRIDOR DES ONZE (k69mvt43j) — le "
     "registre par étages : 24 gardes CADRE déchargées PAR PREUVE de "
     "layout, 23 CTX déchargées à la composition par la preuve de "
     "l'appelant, LES 11 OS les assomptions nommées (le TCB résiduel) ; "
     "la preuve PORTANTE (les 116 certificats : 58 UNSAT + 58 mutations "
     "SAT au relâchement d'UNE unité — LA PASSE CORRIGÉE consignée à "
     "l'erratum append-only, le bogue d'invocation de la première passe "
     "nommé, la trace demeurée) ; L'ÉMISSION le corridor des onze à "
     "0xFC00 (424 o, 116 instr, round-trip VERT, R4/R7 préservés) ; LE "
     "HARNAIS 36/36 (les onze admissions honnêtes à rax=0, la face basse "
     "11/11 REFUSÉE, la face haute 11/11 REFUSÉE, LA FACE D'INDEX 3/3 "
     "REFUSÉE) ; le coût du dispatch NOMMÉ (la médiane 22 instr/appel "
     "contre l'inline 7) ; le kit terrain ≤ 1 % au geste du développeur.")
para("3 · LE MOTEUR NATIF D'ORACLES (8hguph5ee) — le natif (mmap+appel, la "
     "console JSONL) contre LE JUMEAU UNICORN LIGNE-IDENTIQUE aux deux "
     "corps scellés (tls13-16, tls13-17 — 128 vecteurs chacun) ; LA MÉMO "
     "content-addressed (un octet muté = UNE AUTRE CLÉ = MISS, le négatif "
     "vécu) ; LE GATE (le shim au déplacement de calendrier muté ATTRAPÉ "
     "au premier vecteur aux deux corps) ; L'AUDIT 1-sur-10 chaîné "
     "(ZÉRO ÉCART) ; LA MESURE les médianes 0,960 ms → 0,000185 ms au hit "
     "— LE GAIN 5189× aux opérandes non arrondis ; la composition avec la "
     "mémo de régime (−89,4 % — les médianes 24,163 → 2,555 s) et la "
     "cristallisation incrémentale "
     "(−54 %) : les mécanismes ORTHOGONAUX.")
para("4 · TPL-ADD-v5 : LA CIBLE MANQUÉE (yfkpml1j2, nov. 2026) — les leviers : le "
     "normalisateur canonique (la forme que le juge compare déjà, AUCUN "
     "juge affaibli), LE DIFF D'EXPANSION STRUCTURÉ au refus (la ligne à "
     "TROIS étages : écrite / expansion-le point exact où elle casse / le "
     "motif canonique admis — au niveau opcode/opérande/offset) ; LE "
     "VERDICT (nov. 2026) : 5/18 verts, la cible ≥15/18 MANQUÉE — le "
     "coût médian 4 604 (la "
     "cible ≤4 500 manquée de 104) — LA LECTURE DÉFAVORABLE CONSIGNÉE "
     "(jamais un chiffre ajusté, jamais la cible re-tirée) ; le "
     "déplacement v4→v5 : 4 les deux vertes, 1 conversion, 3 PERTES (la "
     "variance du modèle AU CLI nommée — les trois avaient verti à la v4 "
     "aux mêmes prompts — les juges INTACTS), 10 les deux refusées ; LA "
     "VOIE NOMMÉE : le décodage contraint, les paires DPO du corpus, la "
     "relance des pertes à graines identiques.")
para("5 · LA VALIDITÉ EXTERNE SERVIE (ab2vh5c2m, 0i4pkzbyr) — H7 aux 28 "
     "unités : la re-exécution BIT-IDENTIQUE du générateur (le sha "
     "canonique 2de7d488 par sa propre sortie), l'agrégateur fail-closed "
     "(le plafond D207 vécu au refus exit 2, le t apparié 2,160, les "
     "quatre métriques) ; LE SECOND ANNOTATEUR servi (le κ re-autotesté "
     "aux quatre fixtures, l'arbitrage cinq points) ; L'INDÉPENDANCE le "
     "confound 1,5B NOMMÉ (0/64 — la seconde famille LOCALE sous la "
     "frontière, le kit prêt, l'endpoint au développeur) ; LE TRIO D122 "
     "généralisé (la boîte noire chaînée, le bouton envoyer JAMAIS "
     "automatique, la porte de secrets vécue au refus).")
para("6 · CF3-v3 AU VERDICT MACHINE (qa3k5putf) — les TROIS amendements du "
     "registre v14 portés (les parts fraîches, !PartAdverse, le lemme "
     "d'implication aux variables privées aux deux étages) ; LES 36 "
     "avertissements nommés et résolus à la source ; L3 VERIFIED (1 122 "
     "pas) ; L1, L2, T1-T3 INCOMPLETE au mur de mémoire 4 Go du bac — LA "
     "CAUSE NOMMÉE (la décomposition du but K(p), pas la profondeur : "
     "l'évaluation partielle borne la mémoire mais converge au-delà du "
     "budget — LA VOIE du poste réel) ; LE PORT PROVERIF livré (les six "
     "requêtes actives, les six écarts de sémantique nommés) ; le "
     "négatif en deux moutures consigné ; AUCUN VERDICT FABRIQUÉ.")
para("7 · L'ÉCOSYSTÈME D'ADOPTION ET LA GÉNÉRATION — LE CORPUS aux 109 "
     "triples extraits mécaniquement (v3 57 + v4 52 ; les splits "
     "recalculés des fichiers : 28/4/4 tâches · 77/16/16 triples — les "
     "comptes de la première passe au rapport nommés à l'erratum ; le "
     "TEST SANS AUCUNE dorée, le canari unique, les 10 rebuilds "
     "bit-identiques) ; TRIADE-GYM (la récompense typée multi-niveaux — "
     "LA RÉCOMPENSE = LE VERDICT DU JUGE, jamais la similarité ; le check "
     "anti-hacking de P2 à la récompense ; le plan headline PRÉ-ENREGISTRÉ "
     "gelé avant toute mesure) ; LA LADDER re-jouable (les rungs nomment "
     "la frontière, la matrice checkpoint↔kit↔juges fail-closed, le "
     "générateur procédural anti-contamination) ; LE GUIDE d'agent "
     "indépendant du modèle (les 11 règles, la dégradation gracieuse "
     "NOMMÉE, la sonde de capacité avant investissement, AUCUNE ancre "
     "expédiée) ; LA DOC EN au noyau (216/167 tokens aux cibles "
     "≤1 500/≤800 VERTES) ; LE KIT aux 156 pièces PAR CONSTRUCTION (git "
     "ls-files, la porte de compatibilité fail-closed, AUCUNE ancre, la "
     "dette nommée à la naissance) ; LES PROTOCOLES MATÉRIELS "
     "pré-enregistrés (dudect n≥10 × N∈{60,200,400} × ≥2 machines, "
     "fence.i C1-C5, l'agrégateur fail-closed au refus vécu, les autotests "
     "57/57 du dépôt re-verts au sceau) ; LE LINTER "
     "v2 aux cinq classes (le contrôle négatif 5/5 ATTRAPÉES) — la "
     "présente génération régénère les cinq pièces sous lui : les "
     "phrases sémantiques retirées de la spec (le compilateur N'EST "
     "JAMAIS LIVRÉ), les faisabilités datées partout, la campagne v5 "
     "nommée à part, les gallicismes guéris, les trois packs assemblés à "
     "v0.23.3.")

para("L'ÉTAT DES ÉDITIONS", st_h1)
para("v0.23.0 (la vague 13, l'édition) : le GHASH PCLMULQDQ, la "
     "requalification, la ventilation, TPL-ADD-v3, la purge v13 — le "
     "Livre v1.7 et la spec v0.15.8. v0.23.1 (la corrective) : le complet "
     "seul régénéré, l'écart nommé. v0.23.2 (la génération corrective) : "
     "les cinq pièces aux sources corrigées, le linter étendu aux quatre "
     "règles, les trois packs à la version courante. v0.23.3 (la "
     "présente, la release de la vague 15) : les cinq pièces régénérées "
     "sous le linter v2 à cinq classes, la vague 15 portée au corps (la "
     "composition mesurée, le TCB réduit, le moteur d'oracles, la "
     "campagne v5 à sa cible manquée consignée, l'écosystème), les trois "
     "packs assemblés et publiés au concept — la version courante au "
     "jour de la rédaction : la v0.23.2, le record 24442951.")

para("LES GAPS NOMMÉS (jamais simulés)", st_h1)
para("LA CIBLE TPL-ADD (nov. 2026) ≥ 15/18 manquée à 5/18 (la campagne v5) "
     "— la variance du sujet AU CLI nommée, les dix refus chroniques "
     "HORS-FORMAT au texte libre non convertis, LA VOIE nommée (le "
     "décodage contraint, les paires DPO, la relance à graines "
     "identiques) ; la cible ≤ 1 % du coût des gardes NON TRANCHÉE au "
     "bac émulé (le kit terrain pré-enregistré, la machine nommée) ; les "
     "lemmas L1, L2 et les témoins T1-T3 au MUR DE MÉMOIRE du bac 4 Go "
     "(les modèles prêts, l'évaluation partielle la voie, le poste réel "
     "RAM ≥ 16 Go au geste du maître) ; le run ProVerif au poste réel ; "
     "les 28 livraisons H7, l'annotateur, l'endpoint de la seconde "
     "famille, les machines du dudect (≥ 2), la carte RV64 — au geste du "
     "développeur ; les sept fragments EN restants et le miroir FR de la "
     "doc ; les dépôts Zenodo du kit et du corpus — JAMAIS mintés sans "
     "commande ; UNE SEULE MACHINE virtualisée.")

PIECES = {
    "manuscrit": REPO / "edition-v0230" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v158" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v17" / "final.pdf",
    "preuves": ICI / "TRIADE_preuves_et_calculs_v0.23.3.pdf",
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
                      title="TRIADE présentation v233", author="TRIADE")
doc.addPageTemplates([PageTemplate(
    id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin,
                          doc.width, doc.height, id="f")])])
doc.build(story)
print("[présentation v233] le corps : " + str(OUT))

COVER = ICI / "presentation_v233_cover.html"
COVER.write_text("""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>@page { size: A4; margin: 0; }
body { font-family: 'Liberation Serif', serif; margin: 0; }
.c { padding: 200px 64px 0 64px; }
.t { font-size: 36px; font-weight: bold; line-height: 1.2; }
.s { font-size: 17px; margin-top: 20px; color: #333; }
.f { position: absolute; bottom: 54px; left: 64px; right: 64px;
     font-size: 12px; color: #666; border-top: 1px solid #999;
     padding-top: 10px; }</style></head><body><div class="c">
<div class="t">TRIADE<br/>la vague 15</div>
<div class="s">La release v0.23.3 : les cinq pi&egrave;ces
r&eacute;g&eacute;n&eacute;r&eacute;es sous le linter v2 &agrave; cinq
classes — la composition 0,7271 c/octet@4096 (la cible tenue au
36&nbsp;%), le TCB r&eacute;duit 58&rarr;34&rarr;11, le moteur
d'oracles natif &agrave; 5189&times;, la campagne v5 (nov.&nbsp;2026)
&agrave; 5/18 (la cible
manqu&eacute;e, la lecture consign&eacute;e), H7 servie, CF3-v3 au
verdict machine, l'&eacute;cosyst&egrave;me d'adoption</div>
<div class="f">S&eacute;rie TRIADE &middot; &eacute;dition v0.23.3 &middot; 23 novembre 2026
&middot; les empreintes grav&eacute;es, les gaps nomm&eacute;s</div>
</div></body></html>""", encoding="utf-8")
subprocess.run(["weasyprint", str(COVER),
                str(ICI / "presentation_v233_cover.pdf")], check=True)

from pypdf import PdfReader, PdfWriter
w = PdfWriter()
w.add_page(PdfReader(str(ICI / "presentation_v233_cover.pdf")).pages[0])
for p in PdfReader(str(OUT)).pages:
    w.add_page(p)
w.add_metadata({"/Title": "TRIADE présentation v233"})
FINAL = ICI / "TRIADE_presentation_v233.pdf"
with open(FINAL, "wb") as f:
    w.write(f)
print("[présentation v233] LA PIÈCE : " + str(FINAL) + " (" +
      str(len(PdfReader(str(FINAL)).pages)) + " pages)")
