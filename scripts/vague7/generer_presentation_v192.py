#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère le corps de TRIADE_presentation_20261120.pdf (ReportLab) — la pièce 5
du pack v0.19.2. Héritée de la présentation v0.19.1 (D218) avec l'état porté
à l'exécution de l'instruction jx4l5vy5c (D219, la vague 7, la deuxième) :
LA TRANSITION D81 → D183 PRÉPARÉE — le kit de séquestre rafraîchi (la
falsification prouvée, la porte --verifier fail-closed), le scan de secrets
de l'historique complet au dry-run vert, la checklist de rotation, la matrice
de visibilité du dépôt, l'extension transparence publique documentée non
appliquée ; l'état des éditions à v0.19.2 / v0.15.2 / v1.3."""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

OUT = "/home/z/my-project/bac/scripts/vague7/presentation_v192_body.pdf"

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
MUTED = colors.HexColor("#5A6B7F")
PALE = colors.HexColor("#F2F5F9")
BORD = colors.HexColor("#C8D2DE")

st_body = ParagraphStyle("body", fontName="Serif", fontSize=9.6, leading=14.4,
                         alignment=TA_JUSTIFY, spaceAfter=7, textColor=colors.HexColor("#1a1a1a"))
st_kicker = ParagraphStyle("kicker", parent=st_body, fontName="Sans-Bold", fontSize=8.2,
                           textColor=ACCENT, spaceBefore=6, spaceAfter=3, leading=11,
                           alignment=TA_LEFT)
st_h1 = ParagraphStyle("h1", fontName="Serif-Bold", fontSize=16.5, leading=21,
                       textColor=DARK, spaceBefore=2, spaceAfter=9, alignment=TA_LEFT)
st_encadre = ParagraphStyle("encadre", fontName="Serif-Italic", fontSize=9.2, leading=13.8,
                            textColor=colors.HexColor("#2a3a4e"), alignment=TA_JUSTIFY)
st_note = ParagraphStyle("note", parent=st_body, fontName="Serif-Italic",
                         fontSize=8.6, leading=12.4, textColor=MUTED, alignment=TA_LEFT)
st_cell = ParagraphStyle("cell", fontName="Serif", fontSize=8.8, leading=12.2,
                         textColor=colors.HexColor("#1a1a1a"), alignment=TA_LEFT)
st_cellb = ParagraphStyle("cellb", parent=st_cell, fontName="Sans-Bold", fontSize=8.4)
st_cellh = ParagraphStyle("cellh", fontName="Sans-Bold", fontSize=8.4, leading=11,
                          textColor=colors.white, alignment=TA_LEFT)


def P(t, s=st_body):
    return Paragraph(t, s)


def encadre(text):
    t = Table([[Paragraph(text, st_encadre)]], colWidths=[16.4 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 0.6, BORD),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def stat_row(items):
    cells, widths = [], []
    for label, value in items:
        inner = Table(
            [[Paragraph(f'<font name="Serif-Bold" size="15" color="#162032">{value}</font>',
                        ParagraphStyle("v", fontName="Serif-Bold", fontSize=15, leading=18,
                                       alignment=1, textColor=DARK))],
             [Paragraph(f'<font name="Sans" size="7.2" color="#5A6B7F">{label}</font>',
                        ParagraphStyle("l", fontName="Sans", fontSize=7.2, leading=9.6,
                                       alignment=1, textColor=MUTED))]],
            colWidths=[5.35 * cm])
        inner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PALE),
            ("BOX", (0, 0), (-1, -1), 0.6, BORD),
            ("LINEABOVE", (0, 0), (-1, 0), 2.0, ACCENT),
            ("TOPPADDING", (0, 0), (-1, 0), 8), ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
            ("TOPPADDING", (0, 1), (-1, 1), 1), ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
        ]))
        cells.append(inner)
        widths.append(5.35 * cm)
    row = Table([cells], colWidths=widths)
    row.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return row


def table_pièces(rows, widths, header):
    data = [[Paragraph(h, st_cellh) for h in header]]
    for r in rows:
        data.append([Paragraph(c, st_cell) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("BACKGROUND", (0, 1), (-1, -1), PALE),
        ("GRID", (0, 0), (-1, -1), 0.4, BORD),
        ("LINEBEFORE", (0, 0), (0, -1), 2.0, ACCENT),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


class DocPres(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=A4, leftMargin=2.35 * cm, rightMargin=2.35 * cm,
                         topMargin=2.5 * cm, bottomMargin=2.2 * cm,
                         title="TRIADE — Présentation du protocole et état du projet (20 novembre 2026)",
                         author="Z.ai",
                         subject="Le protocole TRIADE en bref, le coffre, la validation D204/D210, la transition D81 → D183 préparée, l'état au 20/11/2026",
                         creator="TRIADE — laboratoire (ReportLab, Template 03, D219)", **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="corps")
        self.addPageTemplates([PageTemplate(id="page", frames=[frame], onPage=self.habille)])

    def habille(self, canv, doc):
        canv.saveState()
        canv.setStrokeColor(ACCENT)
        canv.setLineWidth(0.8)
        canv.line(doc.leftMargin, A4[1] - 1.55 * cm, A4[0] - doc.rightMargin, A4[1] - 1.55 * cm)
        canv.setFont("Sans", 7.4)
        canv.setFillColor(MUTED)
        canv.drawString(doc.leftMargin, A4[1] - 1.32 * cm,
                        "TRIADE — Présentation du protocole et état du projet · 20/11/2026")
        canv.setStrokeColor(BORD)
        canv.setLineWidth(0.5)
        canv.line(doc.leftMargin, 1.52 * cm, A4[0] - doc.rightMargin, 1.52 * cm)
        canv.setFont("Sans", 7.4)
        canv.drawString(doc.leftMargin, 1.14 * cm,
                        "Projet TRIADE — le laboratoire · pack de présentation, pièce 5")
        canv.drawRightString(A4[0] - doc.rightMargin, 1.14 * cm, str(canv.getPageNumber()))
        canv.restoreState()


story = []

# ---------- 1. le protocole en bref ----------
story.append(P("UNE PHRASE, TROIS COUCHES, ONZE RÈGLES", st_kicker))
story.append(P("1. Le protocole en bref", st_h1))
story.append(P(
    "TRIADE est un protocole de développement logiciel qui permet à un agent — humain ou IA — d'écrire, de "
    "vérifier et de mettre à jour du code machine natif pur sans aucune chaîne de traduction optimisante ni "
    "opaque : l'assemblage est WYSIWYG, vérifié par round-trip — ce que l'agent écrit est, par construction, ce "
    "qui s'exécute. L'agent manipule des intentions et une carte de balises, jamais le binaire brut. Le projet "
    "cible par défaut le profil x86-64 / Windows 11 (PE écrit à la main), et s'étend par profils à Linux (ELF64) "
    "et à RISC-V ; tout ce qui dépend de la plateforme vit dans la fiche de profil, jamais dans la méthode. "
    "L'objectif est assumé : un outil légitime par construction, vérifié à chaque pas, sans furtivité — les "
    "tests se font en laboratoire autorisé."))
story.append(P(
    "L'architecture sépare strictement trois couches : la couche I — Intention (spécifications, contrats typés "
    "pré/post, invariants — le quoi et le pourquoi, indépendante de la cible), la couche C — Carte (l'index signé "
    "et chiffré des blocs : adresses, signatures, preuves, manifestes — l'unique interface de développement) et "
    "la couche B — Binaire (le code machine scellé, livré — le comment). Seule la couche B quitte le "
    "laboratoire. Le développement suit la boucle de mise à jour en sept étapes, avec un point de non-retour : "
    "rien n'est écrit dans le binaire avant le verdict de l'oracle."))
story.append(Spacer(1, 2))
story.append(encadre(
    "Onze règles non négociables gouvernent chaque geste — parmi elles : jamais de binaire nu (R1), l'intention "
    "d'abord (R2), le patch à contrat stable (R4), vérifie-puis-écrit (R5), la cristallisation après dix "
    "vérifications (R6), les adresses stables (R7), le verrou croisé avant chaque édition (R8), la carte signée "
    "obligatoire (R9), l'échec contrôlé fail-closed au lancement (R10) et l'optimisation mesurée sous journal "
    "(R11)."))
story.append(Spacer(1, 7))
story.append(P(
    "La vérification est le cœur du protocole : un oracle éphémère — implémentation de référence dérivée de "
    "l'intention, jamais du binaire — confronte chaque bloc par tests différentiels (environ douze mille cas par "
    "bloc critique) ; le round-trip de notation exige que chaque bloc assemblé, désassemblé, soit exactement sa "
    "notation d'origine ; les vecteurs dorés et la cristallisation figent ce qui a été prouvé. La suite "
    "cryptographique (SHA-256, Ed25519, XChaCha20-Poly1305 par défaut, listes blanches) signe la carte et "
    "chiffre ses quatre fragments."))

# ---------- 2. le coffre-fort ----------
story.append(P("CF1, CF2, CF3 — LE LIVRE DU COFFRE", st_kicker))
story.append(P("2. Le coffre-fort et sa gouvernance", st_h1))
story.append(P(
    "Les phrases maîtresses du projet — les secrets qui gardent l'état — vivent dans un coffre-fort : l'ensemble "
    "des couches I, C et B d'un projet de développement, chiffré et signé (Argon2id, clés HKDF par fragment, "
    "sauvegardes 3-2-1). Le coffre-fort centralise les PHRASES MAÎTRESSES (D75) ; l'état de développement "
    "(I, C, B) se transfère, lui, par l'EXPORT DE CONTINUITÉ D16 — l'oracle est régénéré depuis l'intention à "
    "l'arrivée : les deux mécanismes sont distincts et le document les distingue. Le coffre connaît trois "
    "niveaux de sécurité cumulatifs :"))
story.append(P(
    "<b>CF1 — le coffre chiffré</b> (le conteneur à phrase maîtresse, l'autotest de falsification, les règles "
    "d'export/import) ; <b>CF2 — la clé maîtresse répartie</b> (D86 : le partage de Shamir à cinq gardes, seuil "
    "trois, la sentinelle à double seuil puis la PORTE D120 — l'ouverture exige trois gardes réunis, jamais "
    "deux) ; <b>CF3 — la serrure à triple scellement</b> (D121 : la serrure piégée — la clé utilisateur "
    "invariable, les moitiés serrure et piège fraîches à chaque époque, le piège porté par un média séparé "
    "HORS machine, le cycle en deux actes où les clés maîtresses meurent entre l'écriture du brouillard chiffré "
    "et la canonicalisation). Le niveau de naissance d'un coffre neuf est l'arbitrage du développeur (décision "
    "D137). Le coffre réel du projet est CF3, migré par cérémonies successives les 30 et 31 octobre 2026."))
story.append(P(
    "Le Livre du Coffre (v1.3, 28 pages — la pièce 3 de ce pack) est le complément opératoire de la "
    "spécification : les cérémonies d'ouverture et de fermeture, le runbook de migration CF1 vers CF3, LE RUNBOOK "
    "GAGNE À LA PRÉSENTE ÉDITION LA CÉRÉMONIE DE SÉQUESTRE D183 (§ 7.5 — préparée, le geste au maître : le kit "
    "au dépôt, le pas à pas en sept gestes, la preuve à froid ×2 avant tout retrait, les frontières D87), le "
    "mode dégradé et les obligations par niveau. Le modèle formel du coffre est disponible en TLA+ (CF3.tla) : "
    "ses treize règles sont confrontées état par état à la sémantique opérationnelle, et la couverture de la "
    "preuve — 288 formes couvrant l'espace atteignable — est déchargée par Apalache, contrôles négatifs à "
    "l'appui (voir la pièce 4, section 4)."))

# ---------- 3. la validation empirique ----------
story.append(PageBreak())
story.append(P("DEUX BRAS, UN LIVRE, DES PIÈCES", st_kicker))
story.append(P("3. La validation empirique : les campagnes D204 et D210", st_h1))
story.append(P(
    "La question faite au protocole — un agent peut-il vraiment écrire du code natif à la main, et à quel "
    "coût ? — a été mise à l'épreuve par des campagnes de développement contrôlées, chaque run appartenant au "
    "terrain et se terminant par un témoin daté et signé de la main du développeur (décision D99). Les campagnes "
    "confrontent deux bras sur des unités identiques : le bras T (TRIADE — la notation écrite à la main) et le "
    "bras C (la référence compilée). La campagne D204 a livré vingt-deux livraisons recoupées ; son extension "
    "D210 a clos quatre unités supplémentaires et tranché la question de l'attribution."))
story.append(Spacer(1, 4))
story.append(stat_row([("lignes de campagne au livre clos", "29"),
                       ("défauts nommés sur pièces", "11"),
                       ("mutants / survivants (14 blocs crypto)", "224 / 0")]))
story.append(Spacer(1, 8))
story.append(P(
    "Les résultats consolidés : à périmètre instrumenté, le contenu de l'ère Loupe se tient dans la plage "
    "2,98–11,37× la baseline M1 selon l'opération (localiser 580/51, éditer 2 143/719, ajouter 3 510/1 088 — "
    "l'ère Loupe contre M1, jamais un écart entre les bras T et C, dont les coûts réels se lisent à la métrique "
    "M2 : 53 158 contre 67 475 tokens) ; le temps de vérification M4 passe de 52,5 s (campagne) à 39,3 s après "
    "optimisation mesurée sous la règle R11 (le ratio canonique consigné : 23,1× → 17,9×) ; les six cibles "
    "cryptographiques rejouées à secret fixe donnent des traces d'instructions bit-identiques entre classes ; et "
    "le test de mutation — 224 mutants sur quatorze blocs des familles cryptographiques — ne laisse aucun "
    "survivant. Les échecs ne sont pas masqués : chaque run failli vit au livre avec sa faute nommée, et le taux "
    "d'échappées kit-side entre bras a été tranché par le test d'attribution empirique de la D210 — les "
    "échappées sont portées à la rig (le juge écrit du modèle aux terrains à état), le format standard minimal "
    "est blanchi sur pièces."))
story.append(P(
    "La campagne D210 s'est close le 18 novembre 2026 sur quatre unités — loupe-02 VERT, loupe-08 VERT, "
    "loupe-13 VERT, loupe-16 ROUGE à la cap — la séquence tirée de la graine D217 étant épuisée, jamais "
    "re-tirée. La mesure M3 (le carnet du temps humain) fut reçue le 19 novembre (l'Entrée 357) : cinq lignes "
    "run-terrain au carnet, l'écart des bornes consigné à côté (D189 — la main demeure la main, D99). LE LIVRE "
    "EST CLOS : 29 lignes de campagne, onze défauts nommés, aucune ouverture ne demeure."))

# ---------- 4. l'état du projet : la transition préparée + l'état des éditions ----------
story.append(P("VERSIONS COURANTES, LA TRANSITION PRÉPARÉE, LES CHANTIERS", st_kicker))
story.append(P("4. L'état du projet au 20 novembre 2026", st_h1))
story.append(P(
    "Les jalons M0 à M10 sont tous franchis sur validations terrain — de la preuve de chaîne (hello.exe sous "
    "4 Kio, M0) au test grandeur nature « Loupe » (M10, l'application entièrement écrite sous TRIADE, consolidé "
    "par la v0.9.0). Le programme empirique (v0.14.0) puis les preuves non bornées et le raffinement (v0.15.0) "
    "ont suivi ; le manuscrit a atteint la v0.19.0 (le PDF final portant la clôture D210), la v0.19.1 (la "
    "cohérence inter-pièces, D218), puis LA V0.19.2 — L'ÉDITION DE LA TRANSITION PRÉPARÉE (D219, l'instruction "
    "jx4l5vy5c exécutée à la session du 19 novembre) : la bascule de garde durable D81 vers le séquestre chiffré "
    "D183 est PRÉPARÉE, le geste de la cérémonie au développeur."))
story.append(P(
    "CE QUE LA PRÉPARATION PORTE : le kit de séquestre rafraîchi (l'autotest rejoué — dix combinaisons de trois "
    "parts exactes, dix paires sous le seuil inertes, UNE PART FORGÉE REFUSÉE par la porte de l'empreinte de "
    "contrôle : la falsification prouvée ; le mode --verifier fail-closed né au geste) ; LE SCAN DE SECRETS de "
    "l'historique git complet — l'équivalent Python nommé de gitleaks (absent du bac, l'écart D207), son dry-run "
    "sur un dépôt de test à secrets plantés VERT (six sur six attrapés dont deux supprimés de la tête, zéro faux "
    "négatif, zéro faux positif), et le triage du vrai dépôt (472 commits, 5 847 blobs : la phrase D81 connue, "
    "neuf fixtures de test nommées, AUCUN identifiant réel au-delà de l'arbitrage assumé) ; la CHECKLIST DE "
    "ROTATION de toute phrase exposée ; LA MATRICE DE VISIBILITÉ DU DÉPÔT ; et L'EXTENSION TRANSPARENCE "
    "PUBLIQUE documentée sans être appliquée (Rekor/Sigstore ou RFC 3161 : l'ancrage du témoin d'époque CF3, le "
    "delta au modèle de menace aux deux bords). L'ANALYSE CHIFFRÉE reprise : l'espérance de perte annuelle sous "
    "D81 ≈ 4,0 × 10⁻²·C(exposition) contre ≈ 1,0 × 10⁻³ sous le séquestre 5/3 — UN FACTEUR ≈ 40. L'ÉTAT DES "
    "ÉDITIONS :"))
story.append(Spacer(1, 2))
story.append(table_pièces([
    ["Spécification technique", "v0.15.2 (66 p.)",
     "L'édition de la transition préparée (D219) : AUCUNE règle modifiée — la ligne D81 du modèle de menace au "
     "statut exact, le § 1.18, le journal des versions ; la cohérence D218 portée"],
    ["Manuscrit académique", "v0.19.2 (31 p.)",
     "La clôture D210 et la cohérence inter-pièces portées ; la ligne D81 du §4.1 au statut exact (la transition "
     "préparée D219, la falsification prouvée, le scan, la matrice de visibilité)"],
    ["Livre du Coffre", "v1.3 (28 p.)",
     "Le runbook gagne la cérémonie de séquestre D183 (§ 7.5 : l'analyse au facteur ≈ 40, la preuve à froid, les "
     "sept gestes, les frontières) — aucun geste de cérémonie changé"],
    ["Preuves & calculs", "v0.19.2 (20 p.)",
     "Le dossier d'évidence : le rapport V1–V10 de l'exécution D219, l'autotest et la falsification, le dry-run "
     "du scan, la campagne, le modèle, les mesures, le diff annoté"],
    ["Dépôt et sauvegarde", "git + miroirs",
     "Dépôt git (source de vérité), miroir Drive du coffre — <b>GitHub PRIVÉ : la transition D81 → D183 est "
     "PRÉPARÉE (D219) — public + Zenodo seulement après la cérémonie VÉCUE et les rotations vérifiées "
     "(la matrice de visibilité)</b>"],
], [3.4 * cm, 2.9 * cm, 10.3 * cm], ["Pièce", "Version", "L'état VRAI au 20/11/2026"]))
story.append(Spacer(1, 4))
story.append(P("Tableau 1 — L'état des éditions au 20 novembre 2026 (la transition préparée, D219).", st_note))
story.append(Spacer(1, 6))
story.append(P(
    "Les chantiers ouverts, séquencés par l'analyse de la vague 7 (RAPPORT-ANALYSES-VAGUE7) : la bascule de "
    "garde durable D81 vers le séquestre chiffré D183 est PRÉPARÉE (l'instruction jx4l5vy5c EXÉCUTÉE — la "
    "cérémonie demeure au geste du développeur) ; suivent l'écart CF3 modèle↔implémentation et le temps constant "
    "durci (5ey7gmjra) ; le coût de la boucle sous R11 (cq01qv1za — la baseline double-bras précède tout "
    "levier) ; le plan D210 à son terme et l'indépendance inter-familles (1c4sokpii — l'amendement du plan "
    "avant tout nouveau tirage, les runs au geste du développeur). Le mémo M4 scellé (D214) — la re-vérification "
    "de 39,5 s à 10,4 s, moins 74 % sans aucun contrôle retiré — demeure une décision d'adoption à part, à "
    "l'épreuve du terrain."))

# ---------- 5. le contenu du pack ----------
story.append(PageBreak())
story.append(P("CINQ PIÈCES, DES EMPREINTES, UNE LICENCE", st_kicker))
story.append(P("5. Le contenu de ce pack", st_h1))
story.append(P(
    "Ce pack de présentation réunit les pièces qui présentent le protocole tel qu'il tient au 20 novembre "
    "2026 : le manuscrit scientifique, la spécification normative complète, le livre opératoire du coffre-fort, "
    "le dossier d'évidence et le présent document. Chaque pièce est l'édition courante, vérifiée ; les "
    "empreintes SHA-256 de tous les fichiers — y compris celles du pack — vivent au fichier "
    "empreintes_livrables_v0.19.2.txt à la racine du pack, et se recoupent au tableau de bord des builds du "
    "dépôt."))
story.append(Spacer(1, 2))
story.append(table_pièces([
    ["1 — Manuscrit", "TRIADE_manuscrit_v0.19.2.pdf",
     "L'édition académique (en anglais) : le protocole, la campagne, les résultats, la transition préparée"],
    ["2 — Spécification", "Protocole_TRIADE_v0.15.2_Specification.pdf",
     "Le document normatif complet : couches, règles, profils, coffre, gouvernance"],
    ["3 — Coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.3.pdf",
     "Le livre opératoire : cérémonies, runbook (le séquestre D183 § 7.5), mode dégradé"],
    ["4 — Preuves & calculs", "TRIADE_preuves_et_calculs_v0.19.2.pdf",
     "Le dossier d'évidence : l'exécution D219 V1–V10, l'autotest et la falsification, le scan, la campagne, "
     "le modèle, les mesures, les empreintes"],
    ["5 — Présentation", "TRIADE_presentation_20261120.pdf",
     "Le présent document — la vue d'ensemble et l'état du projet"],
], [3.1 * cm, 6.2 * cm, 7.3 * cm], ["Pièce", "Fichier", "Ce qu'elle porte"]))
story.append(Spacer(1, 4))
story.append(P("Tableau 2 — Les cinq pièces du pack de présentation v0.19.2.", st_note))
story.append(Spacer(1, 6))
story.append(P(
    "Le manuscrit v0.19.2 EST l'édition courante — le PDF final est né (la v0.19.0 : la clôture D210), la "
    "v0.19.1 en fut l'édition de cohérence inter-pièces, et la v0.19.2 porte la ligne D81 à son statut exact : "
    "la transition préparée, le geste au développeur. Le pack ne remplace ni le dépôt ni les registres bruts : "
    "il les met en main, chaque affirmation restant traçable jusqu'à ses pièces (la pièce 4 en rassemble les "
    "principales dans leur texte intégral)."))

# ---------- 6. la suite ----------
story.append(P("LA CÉRÉMONIE AU MAÎTRE, LE DOI AU JETON", st_kicker))
story.append(P("6. La suite", st_h1))
story.append(P(
    "LA CÉRÉMONIE DE SÉQUESTRE D183 attend le geste du développeur — le kit est prêt au dépôt "
    "(scripts/kit_ceremonie_d183/) : la répétition générale (l'autotest VERT), le découpage en cinq parts à "
    "seuil trois, la répartition sur cinq médias dont deux hors nuage, la preuve de reconstitution à froid "
    "DEUX fois (le mode --verifier : VERT exigé), PUIS le retrait de la phrase en clair et la rotation (la "
    "checklist du kit). Tant que la cérémonie n'est pas vécue et la rotation vérifiée, le dépôt demeure PRIVÉ "
    "(la matrice de visibilité). Le paquet de dépôt Zenodo est PRÉPARÉ (TRIADE_soumission_v0.19.0.zip, "
    "TRIADE_complet_v0.19.0.zip et zenodo-metadata-v0.19.0.json à la racine du coffre — la licence BSL-1.1 au "
    "grant académique D209) : le DOI attend LE JETON d'API du développeur (aucun jeton au /Tokens) ou le geste "
    "manuel à zenodo.org — public + Zenodo seulement après la matrice. Suivent les trois instructions restantes "
    "de la vague 7, séquencées : l'écart CF3 et le temps constant durci (5ey7gmjra), le coût de la boucle sous "
    "R11 (cq01qv1za), le plan D210 à son terme et l'indépendance inter-familles (1c4sokpii)."))
story.append(Spacer(1, 2))
story.append(encadre(
    "La loi qui garde chaque geste : rien n'est jamais détruit (D143), les observations défavorables se "
    "consignent telles quelles (D189), le témoin se date et se signe de la main (D99) — et le livre ne ment "
    "jamais."))
story.append(Spacer(1, 8))
story.append(P(
    "Ce document a été assemblé par le laboratoire le 19 novembre 2026, à l'Entrée 360 — l'exécution de "
    "l'instruction jx4l5vy5c (la vague 7, la deuxième) : la transition D81 → D183 préparée, la falsification "
    "prouvée, le scan au dry-run vert, le linter inter-pièces étendu aux statuts D81/D183 et vert sur les cinq "
    "pièces. Il accompagne le pack de présentation v0.19.2 déposé à la racine du coffre ; sa véracité se "
    "recoupe au worklog du dépôt, entrée par entrée, et aux registres bruts de la campagne."))

doc = DocPres(OUT)
doc.build(story)
print(f"OK — corps généré : {OUT}")
