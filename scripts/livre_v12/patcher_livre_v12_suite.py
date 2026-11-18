#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_livre_v12_suite.py — la suite (la table sha-256, la note terrain,
la couverture, les métadonnées). Ancre par ancre, REFUS si manquante."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
FAITS = []


def remplace(nom_fichier, ancien, nouveau, nom):
    p = ICI / nom_fichier
    t = p.read_text(encoding="utf-8")
    if ancien not in t:
        raise SystemExit(f"[livre_v12/suite] ANCRE INTROUVABLE — {nom}")
    p.write_text(t.replace(ancien, nouveau, 1), encoding="utf-8")
    FAITS.append(nom)


def sh(module, quartiles, role):
    return ("\\code{" + module + "} & \\code{\\allowbreak " +
            "\\allowbreak ".join(quartiles) + "} & " + role + " \\\\\n")


Q = {
    "coffre_fort": ["f5b2fb90cc020ba7", "fafc735ffa2b8adf", "e896f169f52409b7", "5fe837808b706198"],
    "cf2": ["603ab952b45243fa", "1d82b1fd0b4321a7", "e9af8cf97feda685", "d429814e6043f12f"],
    "cf3": ["ea871be616964a61", "677be92ca671ac3d", "12ce4cb96a105142", "a4d77a7694c24891"],
    "sceau": ["89048e813043a3dd", "73b805ac82f55f35", "91694c5db37f3ec9", "54ec2bafa8170810"],
    "horsligne": ["b5a3fc7ac25c7ab4", "aab22530e1882c48", "a6bc43f0603fecbb", "eb7c54060d7bb7b7"],
    "ceremonie_gui": ["9df2583e6aa55d6a", "8bfd780dc1cc309a", "d238c2bab30da3d3", "c2009e54420a28d5"],
    "migration_gui": ["ba5c2a92141deee0", "246e02015d718d8b", "a056412ff996b4b9", "a5e47403c5e86eda"],
    "autotest_gui": ["557add0cf4f69346", "d5dbbda218923aa5", "dd1e90e6daf4fecd", "cdd5c89396d3c04b"],
    "sentinelle": ["9454e7563b403853", "7d0189044fe69f81", "2017ad9b7dd4b472", "5549d6ce5708ead8"],
    "test_cf2": ["8445d97e94e5a812", "94387c1dec120ce1", "2e0bcc2cdd6cd191", "8ea007a7709b17b5"],
    "test_cf3": ["54066b1c5d7c7efe", "855e9a1cbcb3547d", "bd02b0470a619398", "0c1c60c463f21ce0"],
    "test_sceau": ["6758133cf0f62dc1", "c192757d371df9a2", "55c2f47e9adc1b23", "8a97cf14e5685f0c"],
    "test_mig": ["adcfe77ce6659510", "745c83e802f54ce7", "377c64e7124cdba2", "d3c6247684bdc04c"],
    "test_mig_gui": ["370364a2d68c9005", "dab89ed59840dc83", "d5ebd1cdf17beb52", "bf68110f1f618f12"],
    "test_cer_gui": ["fbfd15d9e8a49dc3", "f8ce4bc8273be63c", "ff26b869014f9885", "c2abd7cf6855a234"],
}

OLD_HEADER = ("\\caption{Empreintes md5 des modules v06 — référence D133.}\n"
              "\\label{tab:empreintslivre}\n"
              "\\begin{tabularx}{\\textwidth}{@{}l l Y@{}}\n"
              "\\toprule\n"
              "\\textbf{Module} & \\textbf{md5} & \\textbf{Rôle} \\\\")
NEW_HEADER = ("\\caption{Empreintes sha-256 des modules v06 — référence D184/D187, "
              "alignée sur\nl'annexe A de la spécification v0.15.1 (contenu canonique LF du dépôt).}\n"
              "\\label{tab:empreintslivre}\n"
              "\\begin{tabularx}{\\textwidth}{@{}l >{\\raggedright\\arraybackslash}p{5.6cm} Y@{}}\n"
              "\\toprule\n"
              "\\textbf{Module} & \\textbf{sha-256} & \\textbf{Rôle} \\\\")
remplace("sec-5.tex", OLD_HEADER, NEW_HEADER, "la table : l'en-tête sha-256")

LIGNES = [
    ("\\code{coffre\\_fort.py} (racine) & \\code{8c79263b9b4694662fb722a67f14ee82} & CF1 \\\\",
     sh("coffre\\_fort.py} (racine", Q["coffre_fort"], "CF1")),
    ("\\code{v06/coffre\\_cf2.py} & \\code{f50ce894db276818d68dd1e22a92fa4c} & CF2 \\\\",
     sh("v06/coffre\\_cf2.py", Q["cf2"], "CF2 — Shamir, sentinelle, porte D120")),
    ("\\code{v06/coffre\\_cf3.py} & \\code{1cf18644d70073bf82f1f2847976f17d} & CF3 \\\\",
     sh("v06/coffre\\_cf3.py", Q["cf3"], "CF3 — serrure piégée, migration, destruction")),
    ("\\code{v06/sceau\\_I.py} & \\code{baf727058504490c288630dbc5bd9664} & sceau I \\\\",
     sh("v06/sceau\\_I.py", Q["sceau"], "sceau I (le registre au 14\\textsuperscript{e} arbre, D177)")),
    ("\\code{v06/ceremonie\\_hors\\_ligne.py} & \\code{982bf0a402607b67a3960952a0adcb11} &\ncérémonie air-gap \\\\",
     sh("v06/ceremonie\\_hors\\_ligne.py", Q["horsligne"], "cérémonie air-gap")),
    ("\\code{v06/ceremonie\\_gui.py} & \\code{e4745580b19e7e5508f596b83bb1652f} & GUI\ncérémonie (v2.2) \\\\",
     sh("v06/ceremonie\\_gui.py", Q["ceremonie_gui"], "GUI cérémonie (v2.2)")),
    ("\\code{v06/migration\\_cf3\\_gui.py} & \\code{933e8405fa49ecad1d11861bd37d1c7a} & GUI\nmigration (v1.1) \\\\",
     sh("v06/migration\\_cf3\\_gui.py", Q["migration_gui"], "GUI migration (v1.1)")),
    ("\\code{v06/autotest\\_cf3\\_gui.py} & \\code{bcd243448873d633852af27f204ecc27} &\nautotest CF3 \\\\",
     sh("v06/autotest\\_cf3\\_gui.py", Q["autotest_gui"], "autotest CF3")),
    ("\\code{v06/sentinelle\\_cf2.py} & \\code{bbc487423302c7f8f821ff348f3737c4} &\nsentinelle CF2 \\\\",
     sh("v06/sentinelle\\_cf2.py", Q["sentinelle"], "sentinelle CF2")),
    ("\\code{v06/test\\_cf2.py} & \\code{f55fbee3391bbbb4466ba096c06b2ad7} & falsifiabilité\nCF2 \\\\",
     sh("v06/test\\_cf2.py", Q["test_cf2"], "falsifiabilité CF2")),
    ("\\code{v06/test\\_coffre\\_cf3.py} & \\code{33f460171f69aa59ae40192b5de46114} &\nfalsifiabilité CF3 \\\\",
     sh("v06/test\\_coffre\\_cf3.py", Q["test_cf3"], "falsifiabilité CF3")),
    ("\\code{v06/test\\_sceau\\_I.py} & \\code{a4b43fd5aa37acb37e98b77dca5747fc} &\nfalsifiabilité sceau \\\\",
     sh("v06/test\\_sceau\\_I.py", Q["test_sceau"], "falsifiabilité sceau")),
    ("\\code{v06/test\\_migration\\_cf3.py} & \\code{9e078dfdebea4bbe88b72fb71ab907bd} &\nfalsifiabilité migration \\\\",
     sh("v06/test\\_migration\\_cf3.py", Q["test_mig"], "falsifiabilité migration")),
    ("\\code{v06/test\\_migration\\_cf3\\_gui.py} & \\code{5f93800b887e44f52b1e998d5aabf160} &\nfalsifiabilité GUI migration \\\\",
     sh("v06/test\\_migration\\_cf3\\_gui.py", Q["test_mig_gui"], "falsifiabilité GUI migration")),
    ("\\code{v06/test\\_ceremonie\\_gui.py} & \\code{e275efb83c104bcac30f05d96c7ce318} &\nfalsifiabilité GUI cérémonie \\\\",
     sh("v06/test\\_ceremonie\\_gui.py", Q["test_cer_gui"], "falsifiabilité GUI cérémonie")),
]
for ancien, nouveau in LIGNES:
    nom = "la table : " + nouveau.split("&")[0].strip().replace("\\code{", "")[:40]
    remplace("sec-5.tex", ancien, nouveau, nom)

# ---- la note de divergence terrain : ses md5 nommés HISTORIQUES ----
remplace("sec-5.tex",
         "Au rapport du 30/10 20:41, le \\code{coffre\\_fort.py} du clone terrain rend\n"
         "\\code{299fd124\\ldots{}} alors que le dépôt rend \\code{8c79263b\\ldots{}} — ni l'un ni",
         "Au rapport du 30/10 20:41, le \\code{coffre\\_fort.py} du clone terrain rendait\n"
         "\\code{299fd124\\ldots{}} (md5, la preuve historique telle que consignée) alors que\n"
         "le dépôt rendait \\code{8c79263b\\ldots{}} (md5) — ni l'un ni",
         "la divergence terrain : ses md5 nommés HISTORIQUES")

# ---- cover.html ----
remplace("cover.html",
         '<div class="label">Document compl&eacute;mentaire &middot; Version 1.1</div>',
         '<div class="label">Document compl&eacute;mentaire &middot; Version 1.2</div>',
         "cover.html : la version 1.2")
remplace("cover.html",
         "Compagnon op&eacute;ratoire de la sp&eacute;cification v0.6.1&nbsp;:",
         "Compagnon op&eacute;ratoire de la sp&eacute;cification (l'&eacute;dition courante v0.15.1)&nbsp;:",
         "cover.html : le compagnon de la spec courante")
remplace("cover.html",
         "R&eacute;vision v1.1 (D137)&nbsp;: le niveau d'un",
         "R&eacute;vision v1.2 (D218, &eacute;dition de coh&eacute;rence)&nbsp;: les empreintes &agrave; sha-256, les quatorze arbres sign&eacute;s, le sommaire des d&eacute;cisions D75&ndash;D137. La v1.1 portait le niveau d'un",
         "cover.html : la note de révision v1.2")
remplace("cover.html",
         "<span>S&eacute;rie TRIADE &middot; r&eacute;vision v1.1 (D137)</span>",
         "<span>S&eacute;rie TRIADE &middot; r&eacute;vision v1.2 (D218)</span>",
         "cover.html : le pied de révision v1.2")
remplace("cover.html",
         "<span>31 octobre 2026</span>",
         "<span>19 novembre 2026</span>",
         "cover.html : la date de l'édition")

# ---- merge_cover.py : les métadonnées ----
p = ICI / "merge_cover.py"
t = p.read_text(encoding="utf-8")
t = t.replace("v1.1", "v1.2")
p.write_text(t, encoding="utf-8")
FAITS.append("merge_cover.py : les métadonnées v1.2")

print(f"[livre_v12/suite] {len(FAITS)} éditions ancrées :")
for f in FAITS:
    print(f"  - {f}")
