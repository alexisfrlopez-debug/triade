#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_livre_v16.py — le Livre du Coffre v1.6 (né de v1.5 par copie) :
LA PURGE DES INSTRUCTIONS DE REMISE D81 (ou6wn6wlv, la vague 11) — le
séquestre D183 est VÉCU (D223), le dépôt est PUBLIC (D220) : aucune
instruction opératoire ne peut plus faire committer/pousser
PHRASE-CONTROLE-COFFRE.txt. Chaque emplacement cité par l'instruction
remplacé par LA GARDE ACTIVE (le séquestre Shamir 5/3) ET LA CÉRÉMONIE DE
RECONSTITUTION À FROID, avec le REFUS NOMMÉ de la réécriture au dépôt.
Les mentions HISTORIQUES datées demeurent (append-only — l'histoire n'est
pas réécrite). Chaque remplacement EST ANCRÉ (échec si une ancre manque)."""
import pathlib
import shutil

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parent / "livre_v15"
for f in [SRC / "main.tex", *SRC.glob("sec-*.tex"), SRC / "cover.html",
          SRC / "merge_cover.py", SRC / "chaine_cf.html", SRC / "chaine_cf.png"]:
    if f.exists():
        shutil.copy2(f, ICI / f.name)

M = (ICI / "main.tex").read_text(encoding="utf-8")
T = {n: (ICI / f"sec-{n}.tex").read_text(encoding="utf-8")
     for n in range(1, 7)}
FAITS = []


def remplace(txt, ancien, nouveau, nom):
    if ancien not in txt:
        raise SystemExit(f"[v16] ANCRE INTROUVABLE — {nom}")
    if txt.count(ancien) != 1:
        raise SystemExit(f"[v16] ANCRE NON UNIQUE ({txt.count(ancien)}×) — {nom}")
    FAITS.append(nom)
    return txt.replace(ancien, nouveau)


# ---- l'en-tête (v1.6) -------------------------------------------------------
M = remplace(M, "%  LE LIVRE DU COFFRE — TRIADE CF1 -> CF2 -> CF3 (v1.5, D228)",
             "%  LE LIVRE DU COFFRE — TRIADE CF1 -> CF2 -> CF3 (v1.6, ou6wn6wlv)",
             "l'en-tête (v1.6)")
M = remplace(M, "%  v1.5 : la vague 9 (D228",
             "%  v1.6 : la purge des instructions de remise D81 (ou6wn6wlv — le\n"
             "%  séquestre 5/3 la garde active, la reconstitution à froid, le refus\n"
             "%  nommé de la réécriture au dépôt public)\n"
             "%  v1.5 : la vague 9 (D228",
             "la ligne de version (v1.6)")
M = remplace(M, r"\fancyhead[L]{\small\itshape Le Livre du Coffre — TRIADE CF1 → CF3 (v1.5)}",
             r"\fancyhead[L]{\small\itshape Le Livre du Coffre — TRIADE CF1 → CF3 (v1.6)}",
             "le running header (v1.6)")
M = remplace(M, "pdftitle={Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.5)},",
             "pdftitle={Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.6)},",
             "le pdftitle (v1.6)")

# ---- §1.4 règle 2 : la remise D81 -> le séquestre ---------------------------
T[1] = remplace(T[1],
                "\\item \\textbf{La remise précède l'usage.} Toute phrase de contrôle vit\n"
                "\\code{PHRASE-CONTROLE-COFFRE.txt} (une ligne, lisible par \\code{--phrase-fichier}),\n"
                "commitée et poussée AVANT toute autre action de la session (D81). Le fichier \\emph{est}\n"
                "la remise : l'affichage unique de cérémonie n'est plus un canal de survie.",
                "\\item \\textbf{La phrase vit au séquestre, jamais au dépôt.} La garde active\n"
                "est le séquestre D183 (D223) : cinq parts Shamir à seuil trois, les parts\n"
                "inertes sous le seuil, la phrase en AUCUN dépôt — le dépôt est PUBLIC\n"
                "(D220). La remise est la cérémonie de reconstitution à froid : trois parts\n"
                "assemblées hors-ligne, la phrase reconstituée jamais écrite au dépôt,\n"
                "l'usage transient détruit après le geste. Tout geste qui tenterait de\n"
                "réécrire la phrase (ou son fichier) au dépôt est REFUSÉ avec son nom.\n"
                "(La garde D81 — le fichier-remise commité — est l'histoire datée : la\n"
                "phrase y demeure à vie, la rotation fut le remède ; cf. § \\ref{sec:guarded81}.)",
                "§1.4 règle 2 (le séquestre, la reconstitution, le refus nommé)")

# ---- §2 : la garde D81 — le récit borné dans le temps ------------------------
T[2] = remplace(T[2],
                "\\subsection{La garde de la phrase (D81) — le fichier est la remise}",
                "\\subsection{La garde de la phrase (D81) — le fichier fut la remise}\\label{sec:guarded81}",
                "§2 le titre de la garde D81 (daté)")
T[2] = remplace(T[2],
                "(URL non devinable). Depuis : dès sa\n"
                "production — init, rotation, changement — la phrase est écrite dans",
                "(URL non devinable). De D81 au 19 novembre 2026 : dès sa\n"
                "production — init, rotation, changement — la phrase était écrite dans",
                "§2 le récit D81 borné (la date butoir)")

# ---- §6 : l'inventaire, la frontière, les rotations --------------------------
T[3] = remplace(T[3],
                "La phrase de contrôle & votre tête ; le fichier-remise D81 (dépôt git + coffre Drive,\n"
                "AVANT toute autre action) & sans la phrase, pas de K\\_user — le coffre est muet ; le\n"
                "fichier est la survie \\\\",
                "La phrase de contrôle & votre tête ; le séquestre D183/D223 (cinq parts\n"
                "Shamir à seuil trois, la reconstitution à froid) & sans la phrase, pas de\n"
                "K\\_user — le coffre est muet ; sous trois parts assemblables, la phrase est\n"
                "PERDUE (le seuil est la survie) \\\\",
                "§6 l'inventaire (la garde = le séquestre)")
T[3] = remplace(T[3],
                "Dépôt git (poussé) & le code, la spécification signée (\\code{v06/I/}), les preuves\n"
                "publiques du sceau, le journal de travail, la phrase de contrôle (D81 — le fichier\n"
                "est la remise) & aucun conteneur, aucun fragment, aucune graine :\n"
                "\\code{/.keys/} est gitignoré \\\\",
                "Dépôt git (poussé, PUBLIC depuis D220) & le code, la spécification signée\n"
                "(\\code{v06/I/}), les preuves publiques du sceau, le journal de travail & aucun\n"
                "conteneur, aucun fragment, aucune graine, AUCUNE PHRASE (le séquestre 5/3\n"
                "hors dépôt, D223) : \\code{/.keys/} est gitignoré \\\\",
                "§6 la frontière (aucune phrase au dépôt)")
T[3] = remplace(T[3],
                "Phrase de contrôle & \\code{changer-phrase} (l'ancienne devient inopérante, les\n"
                "entrées intactes) ; le fichier-remise D81 suit AVANT tout — c'est la discipline\n"
                "entière & le coffre, les projets, le sel (le re-chiffrement prend un sel neuf) \\\\",
                "Phrase de contrôle & \\code{changer-phrase} (l'ancienne devient inopérante, les\n"
                "entrées intactes) ; le changement passe par la cérémonie sous séquestre —\n"
                "trois parts assemblées à froid, la phrase neuve re-découpée en CINQ parts,\n"
                "JAMAIS écrite au dépôt (le refus nommé la garde) & le coffre, les projets,\n"
                "le sel (le re-chiffrement prend un sel neuf) \\\\",
                "§6 les rotations (le changement sous séquestre)")

# ---- §7 : la cérémonie D183 (la lecture locale, jamais commitée) -------------
T[4] = remplace(T[4],
                "\\item \\textbf{Préparer} : python3, le dossier du kit, la phrase\n"
                "(\\code{PHRASE-CONTROLE-COFFRE.txt}, à lire vous-même — jamais copée au bac\n"
                "à sable), et CINQ MÉDIAS :",
                "\\item \\textbf{Préparer} : python3, le dossier du kit, la phrase (lue de vos\n"
                "yeux depuis votre garde — jamais copée au bac à sable, jamais commitée au\n"
                "dépôt), et CINQ MÉDIAS :",
                "§7 D183 Préparer (la lecture locale, jamais commitée)")

# ---- §8.2 étape 3 : la phrase à vous — la cérémonie sous séquestre -----------
T[4] = remplace(T[4],
                "\\item \\textbf{La phrase à vous} (optionnel, D110) : changer la phrase de contrôle\n"
                "pour la vôtre — alphanumérique, sans plafond. Le fichier-remise D81 suit\n"
                "\\emph{immédiatement} : une ligne dans \\code{PHRASE-CONTROLE-\\allowbreak COFFRE.txt}, commit, push.",
                "\\item \\textbf{La phrase à vous} (optionnel, D110) : changer la phrase de contrôle\n"
                "pour la vôtre — alphanumérique, sans plafond — par la cérémonie de\n"
                "changement sous séquestre : trois parts assemblées à froid, la phrase neuve\n"
                "vérifiée au plancher d'entropie, le conteneur migré, la phrase neuve\n"
                "re-découpée en CINQ parts, l'ancienne détruite localement avec PV. La\n"
                "phrase n'est JAMAIS écrite au dépôt (D223) — un geste qui tenterait de la\n"
                "réécrire (ou son fichier) au dépôt est REFUSÉ avec son nom.",
                "§8.2 étape 3 (la cérémonie sous séquestre, le refus nommé)")

# ---- §8.3 item 2 : la check-list pré-vol -------------------------------------
T[4] = remplace(T[4],
                "\\item \\textbf{Le fichier-remise D81 dit la vérité} : la ligne de\n"
                "\\code{PHRASE-CONTROLE-COFFRE.txt} est la phrase que vous allez taper — sinon, posez-la\n"
                "d'abord, commit, push.",
                "\\item \\textbf{Le séquestre est entier} : le manifeste des parts (cinq\n"
                "empreintes, seuil trois) recoupe la carte du sachet — la phrase que vous\n"
                "taperez vient de la reconstitution à froid de trois parts, jamais d'un\n"
                "fichier au dépôt (D223).",
                "§8.3 item 2 (la check-list au séquestre)")

# ---- §9.2 : le remède « phrase de contrôle divergente » ----------------------
T[5] = remplace(T[5],
                "« phrase de contrôle divergente » (migrer) & la remise D81 n'est pas encore\n"
                "remplacée — le coffre vit sous une autre phrase que le fichier ne dit pas & posez la\n"
                "phrase courante dans \\code{PHRASE-CONTROLE-COFFRE.txt}, commit, push, puis rejouez la\n"
                "cérémonie \\\\",
                "« phrase de contrôle divergente » (migrer) & le coffre vit sous une autre\n"
                "phrase que celle tapée — la reconstitution n'a pas rendu la phrase courante\n"
                "& reconstituez à froid TROIS parts du séquestre courant (l'époque au\n"
                "manifeste), puis rejouez la cérémonie ; la phrase n'est JAMAIS réécrite au\n"
                "dépôt (le refus nommé D223) \\\\",
                "§9.2 le remède divergente (la reconstitution à froid)")

# ---- §11 : la décision D81 (l'histoire annotée de l'amendement) --------------
T[5] = remplace(T[5],
                "D81 & La phrase sous garde durable & \\code{PHRASE-CONTROLE-COFFRE.txt} au dépôt et\n"
                "au coffre Drive AVANT toute autre action — le fichier est la remise. \\\\",
                "D81 & La phrase sous garde durable (amendée D223) & le fichier-remise au\n"
                "dépôt et au coffre Drive AVANT toute autre action — l'histoire datée ; la\n"
                "garde active est le séquestre 5/3 (D183). \\\\",
                "§11 la décision D81 (l'amendement nommé)")

# ---- écriture ---------------------------------------------------------------
(ICI / "main.tex").write_text(M, encoding="utf-8")
for n, t in T.items():
    (ICI / f"sec-{n}.tex").write_text(t, encoding="utf-8")
print(f"[v16] {len(FAITS)} remplacements ancrés :")
for f in FAITS:
    print("  -", f)
