#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v157.py — la spécification v0.15.7 (née de v0.15.6 par copie) :
LA PURGE DES INSTRUCTIONS DE REMISE D81 (ou6wn6wlv, la vague 11) — le
séquestre D183 est VÉCU (D223), le dépôt est PUBLIC (D220). Les emplacements
cités par l'instruction : §14.3 (la clause de garde durable de la phrase) et
la table des cérémonies (tab:ceremonies) ; la table d'évolutions v0.5.2 et la
décision D81 demeurent HISTORIQUES, annotées de l'amendement D223. Chaque
remplacement EST ANCRÉ (échec si une ancre manque)."""
import pathlib
import shutil

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parent / "spec_v156"
for f in [SRC / "main.tex", *SRC.glob("sec-*.tex"), SRC / "chaine_cf.png"]:
    if f.exists():
        shutil.copy2(f, ICI / f.name)

M = (ICI / "main.tex").read_text(encoding="utf-8")
A = (ICI / "sec-a.tex").read_text(encoding="utf-8")
CF = (ICI / "sec-cf.tex").read_text(encoding="utf-8")
D = (ICI / "sec-d.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(txt, ancien, nouveau, nom):
    if ancien not in txt:
        raise SystemExit(f"[v157] ANCRE INTROUVABLE — {nom}")
    if txt.count(ancien) != 1:
        raise SystemExit(f"[v157] ANCRE NON UNIQUE ({txt.count(ancien)}×) — {nom}")
    FAITS.append(nom)
    return txt.replace(ancien, nouveau)


# ---- l'en-tête (v0.15.7) ----------------------------------------------------
M = remplace(M, "%  PROTOCOLE TRIADE v0.15.6 — Manuscrit de spécification",
             "%  PROTOCOLE TRIADE v0.15.7 — Manuscrit de spécification",
             "l'en-tête (v0.15.7)")
M = remplace(M, r"\fancyhead[L]{\small\itshape Protocole TRIADE — spécification v0.15.6}",
             r"\fancyhead[L]{\small\itshape Protocole TRIADE — spécification v0.15.7}",
             "le running header (v0.15.7)")
M = remplace(M, "pdftitle={Protocole TRIADE v0.15.6 — spécification technique},",
             "pdftitle={Protocole TRIADE v0.15.7 — spécification technique},",
             "le pdftitle (v0.15.7)")

# ---- l'évolution de discipline D81 (sec-a) : amendée D223 --------------------
A = remplace(A,
             "Une évolution de discipline, tracée dans la correspondance (§\\ref{sec:evolutions052}) et\n"
             "le journal des versions, rattachée à la décision D81 : la \\textbf{phrase de contrôle du\n"
             "coffre-fort passe sous garde durable} — dès sa production (init, rotation,\n"
             "changement), elle est sauvegardée dans le dépôt git (commit dédié, push GitHub, miroir\n"
             "du coffre Drive par le hook) et au racine du coffre Drive \\emph{avant} toute autre action\n"
             "de la session ; le fichier \\code{PHRASE-CONTROLE-COFFRE.txt} (phrase seule sur une\n"
             "ligne, lisible tel quel par \\code{--phrase-fichier}) \\emph{est} la remise — l’affichage\n"
             "unique de cérémonie (D27/D30) cesse d’être le canal de survie.",
             "Une évolution de discipline, tracée dans la correspondance (§\\ref{sec:evolutions052}) et\n"
             "le journal des versions, rattachée à la décision D81 puis \\textbf{amendée par D223} :\n"
             "la phrase de contrôle fut mise sous garde durable (le fichier au dépôt, du 4 au\n"
             "19 novembre 2026) ; depuis le séquestre vécu D183, la garde ACTIVE est les CINQ\n"
             "PARTS Shamir à seuil trois — la reconstitution à froid quand la phrase sert,\n"
             "la phrase en AUCUN dépôt (public depuis D220) ; tout geste qui tenterait de\n"
             "réécrire la phrase (ou son fichier) au dépôt est refusé avec son nom.",
             "sec-a l'évolution D81 (amendée D223)")

# ---- la table des gardes (sec-cf, tab:gardehi) : la phrase au séquestre ------
CF = remplace(CF,
              "Phrase de lignée & chiffre les enveloppes de carte — vol du dépôt au repos & en tête\n"
              "du développeur, secours au coffre Drive (D81 : le fichier \\code{PHRASE-CONTROLE-COFFRE.txt}\n"
              "est la remise) \\\\",
              "Phrase de lignée & chiffre les enveloppes de carte — vol du dépôt au repos & en tête\n"
              "du développeur, séquestre D183/D223 (cinq parts Shamir à seuil trois, la\n"
              "reconstitution à froid — la phrase en aucun dépôt) \\\\",
              "sec-cf tab:gardehi (la phrase au séquestre)")

# ---- la table des cérémonies (tab:ceremonies) : CF1→CF2 sans remise D81 ------
CF = remplace(CF,
              "CF1 $\\to$ CF2 (D106) & phrase de contrôle (D81 : remise AVANT tout) ; \\code{migrer} ;",
              "CF1 $\\to$ CF2 (D106) & phrase de contrôle (la reconstitution à froid du\n"
              "séquestre la fournit — jamais un fichier au dépôt, D223) ; \\code{migrer} ;",
              "sec-cf tab:ceremonies (CF1→CF2 sans remise D81)")

# ---- §14.3 : la restauration post-panne et la clause -------------------------
D = remplace(D,
             "du conteneur, la relecture de la phrase depuis \\code{PHRASE-CONTROLE-COFFRE.txt}, puis",
             "du conteneur, la reconstitution à froid de la phrase depuis TROIS parts du\n"
             "séquestre (D183/D223), puis",
             "§14.3 la restauration post-panne (la reconstitution)")
D = remplace(D,
             "Discipline évoluant en D81 sur un point, l'arbitrage (risque de PERTE\n"
             "vécu contre risque d'EXPOSITION théorique) étant consigné : chaque cérémonie de clés\n"
             "(D27/D30) alimente le coffre dans la même session, la phrase de contrôle est sauvegardée\n"
             "durablement AVANT TOUTE AUTRE ACTION — \\code{PHRASE-CONTROLE-COFFRE.txt} au racine du\n"
             "dépôt (commit dédié, push GitHub, miroir Drive par le hook) et au racine du coffre\n"
             "Drive, md5 vérifiés : le fichier est la remise, l'affichage unique cesse d'être le canal\n"
             "de survie — et la graine Ed25519 reste hors coffre (D30).",
             "Discipline évoluant en D81 puis amendée en D223, l'arbitrage (risque de PERTE\n"
             "vécu contre risque d'EXPOSITION théorique) étant consigné : chaque cérémonie de clés\n"
             "(D27/D30) alimente le coffre dans la même session, la phrase de contrôle est mise\n"
             "au séquestre AVANT TOUTE AUTRE ACTION — cinq parts Shamir à seuil trois (D183,\n"
             "la garde active D223), la reconstitution à froid quand la phrase sert, la phrase\n"
             "en AUCUN dépôt (public depuis D220) : tout geste qui tenterait de la réécrire\n"
             "(ou son fichier) au dépôt est refusé avec son nom — et la graine Ed25519 reste\n"
             "hors coffre (D30).",
             "§14.3 la clause (le séquestre, le refus nommé)")

# ---- la table d'évolutions v0.5.2 : l'annotation de l'amendement -------------
D = remplace(D,
             "coffre Drive, AVANT toute autre action ; le fichier est la remise & modifié (D81) \\\\",
             "coffre Drive, AVANT toute autre action ; le fichier est la remise & modifié\n"
             "(D81 ; amendé D223 — le séquestre 5/3, la phrase hors dépôt) \\\\",
             "la table v0.5.2 (l'amendement annoté)")

# ---- la décision D81 (table décisionnelle) : l'annotation --------------------
D = remplace(D,
             "D81 & Garde durable de la phrase de contrôle & \\code{PHRASE-CONTROLE-COFFRE.txt} au\n"
             "dépôt et au coffre Drive AVANT toute autre action — le fichier est la remise. \\\\",
             "D81 & Garde durable de la phrase de contrôle (amendée D223) & le fichier-remise\n"
             "au dépôt et au coffre Drive AVANT toute autre action — l'histoire datée ; la\n"
             "garde active est le séquestre 5/3 (D183). \\\\",
             "la décision D81 (l'amendement nommé)")

# ---- la correspondance v0.15.6 -> v0.15.7 (le journal des versions) ----------
D = remplace(D,
             "v0.15.1 est L'ÉDITION DE COHÉRENCE INTER-PIÈCES (D218, la vague",
             "La v0.15.7 est L'ÉDITION DE LA PURGE D81 (ou6wn6wlv, la vague 11) : aucune\n"
             "règle du protocole modifiée — la clause de garde durable de la phrase (§14.3)\n"
             "et la table des cérémonies réécrites à la garde active (le séquestre D183\n"
             "vécu, cinq parts à seuil trois, la reconstitution à froid, le refus nommé de\n"
             "la réécriture au dépôt public D220) ; l'évolution de discipline D81 (§\\ref{sec:evolutions052})\n"
             "bornée dans le temps et annotée de l'amendement D223 ; la restauration\n"
             "post-panne à la reconstitution à froid. Les mentions historiques datées\n"
             "demeurent (append-only). La\n"
             "v0.15.1 est L'ÉDITION DE COHÉRENCE INTER-PIÈCES (D218, la vague",
             "la correspondance v0.15.7 (le journal des versions)")

# ---- écriture ---------------------------------------------------------------
(ICI / "main.tex").write_text(M, encoding="utf-8")
(ICI / "sec-a.tex").write_text(A, encoding="utf-8")
(ICI / "sec-cf.tex").write_text(CF, encoding="utf-8")
(ICI / "sec-d.tex").write_text(D, encoding="utf-8")
print(f"[v157] {len(FAITS)} remplacements ancrés :")
for f in FAITS:
    print("  -", f)
