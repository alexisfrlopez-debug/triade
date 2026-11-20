#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v155.py — la spécification v0.15.5 (née de v0.15.4 par
copie) : L'ÉTAT VÉCU DE LA GOUVERNANCE (ansz8lvdf — D223) + les
corrections de cohérence de gq117wphb. AUCUNE règle R1–R11 modifiée.
Chaque remplacement EST ANCRÉ — REFUS si une ancre manque."""
import pathlib
import shutil

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parent / "spec_v154"
for f in [SRC / "main.tex", *SRC.glob("sec-*.tex"), SRC / "chaine_cf.png"]:
    if f.exists():
        shutil.copy2(f, ICI / f.name)

S = (ICI / "main.tex").read_text(encoding="utf-8")
A = (ICI / "sec-a.tex").read_text(encoding="utf-8")
D = (ICI / "sec-d.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(txt, ancien, nouveau, nom):
    if ancien not in txt:
        raise SystemExit(f"[v155] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return txt.replace(ancien, nouveau, 1)


# ---- l'en-tête de main.tex -------------------------------------------------
S = remplace(S, "%  PROTOCOLE TRIADE v0.15.4 — Manuscrit de spécification",
             "%  PROTOCOLE TRIADE v0.15.5 — Manuscrit de spécification",
             "l'en-tête (v0.15.5)")
S = remplace(S, "spécification v0.15.4}", "spécification v0.15.5}",
             "le titre courant (v0.15.5)")

# ---- (ansz8lvdf 2) la ligne D81 du modèle de menace (§15) -------------------
D = remplace(D,
             "\\textbf{Vol du coffre-fort des phrases} & chiffrement intégral (Argon2id, contexte\n"
             "HKDF dédié, AEAD) ; écriture atomique ; depuis D81 la phrase de contrôle vit au coffre\n"
             "Drive et au dépôt — mitigation première : restreindre le partage par lien ; la\n"
             "transition vers le séquestre D183 est PRÉPARÉE (D219 : le kit rafraîchi avec la\n"
             "falsification prouvée, le scan de secrets au dry-run vert, la checklist de rotation,\n"
             "la matrice de visibilité — le geste au développeur) & confidentialité\n"
             "ramenée au contrôle d'accès du dossier ; une phrase commise en git y demeure à vie — la\n"
             "rotation reste le remède (D75, étendu D81) ; le dépôt demeure PRIVÉ tant que la\n"
             "cérémonie D183 n'est pas vécue et la rotation vérifiée — public + Zenodo seulement\n"
             "après (D219) \\\\",
             "\\textbf{Vol du coffre-fort des phrases} & chiffrement intégral (Argon2id, contexte\n"
             "HKDF dédié, AEAD) ; écriture atomique ; DEPUIS D223 (l'état vécu acté) : la cérémonie\n"
             "D183 EST VÉCUE (19 novembre 2026) — le séquestre Shamir cinq parts seuil trois est LA\n"
             "GARDE ACTIVE, la phrase de contrôle commise FUT TOURNÉE et l'ancienne REFUSÉE à la\n"
             "ré-ouverture, la reconstitution à froid prouvée deux fois ; la phrase ne vit PLUS au\n"
             "dépôt ni au coffre Drive & la confidentialité repose sur le seuil trois-de-cinq (trois\n"
             "médias requis, deux hors nuage) ; le dépôt est PUBLIC (D220) — ce qu'il porte\n"
             "désormais (le code, les preuves, l'historique) n'ouvre plus le coffre ; la rotation\n"
             "demeure le remède d'une fuite de parts (D75, étendu D81, amendé D223) \\\\",
             "la ligne D81 du modèle de menace (l'état vécu)")

# ---- (ansz8lvdf 2) §14.3 : la phrase de garde -------------------------------
D = remplace(D,
             "phrase de contrôle sous garde durable (D81 — sauvegardée dès production au dépôt et au",
             "phrase de contrôle sous garde durable (D81, AMENDÉE PAR D223 — le séquestre chiffré\n"
             "D183 est la garde VÉCUE depuis le 19 novembre 2026 : la phrase ne vit plus au",
             "§14.3 la ligne de garde (l'amendement D223)")

# ---- (gq117wphb 5) l'ordre des versions §1.18-§1.20 -------------------------
ordre = A[A.index("\\subsection{Ce que change la v0.15.4}"):]
fin154 = ordre.index("\\subsection{Ce que change la v0.15.3}")
sec154 = ordre[:fin154]
reste = ordre[fin154:]
fin153 = reste.index("\\subsection{Ce que change la v0.15.2}")
sec153 = reste[:fin153]
sec152 = reste[fin153:]
A = A[:A.index("\\subsection{Ce que change la v0.15.4}")] + sec152 + sec153 + sec154
FAITS.append("l'ordre croissant des versions (§1.18-§1.20 : v0.15.2, v0.15.3, v0.15.4)")

# ---- (gq117wphb 5) l'étiquette D195 ------------------------------------------
A = remplace(A,
             "les MESURES d'édition v0.17--v0.18 (D195 : localiser 580, éditer 2~143, ajouter 3~510) font foi pour l'état courant.}",
             "les MESURES d'édition v0.17--v0.18 (l'instrumenté au tokenizer natif :\n"
             "localiser 1~277, éditer 3~374, ajouter 3~674 — puis le pointeur seul adopté\n"
             "OPT-04/D222 : localiser 1~103 mesuré à la graine consignée ; les valeurs\n"
             "580/2~143/3~510 sont la re-mesure v0.14.0 DE D195, au contenu seul, jamais\n"
             "confondues avec l'instrumenté) font foi pour l'état courant.}",
             "l'étiquette D195 distinguée de l'instrumenté v0.17")

# ---- (gq117wphb 5) le titre de l'annexe B -------------------------------------
D = remplace(D, "\\section{Tableau décisionnel du coffre-fort (D75--D198)}",
             "\\section{Tableau décisionnel du coffre-fort (D75--D223)}",
             "le titre de l'annexe B (la plage réelle)")
D = remplace(D, "falsifiabilité du maître de cérémonie \\\\",
             "falsifiabilité du maître de cérémonie \\\\\n"
             "D223 & L'état vécu acté (l'instruction ansz8lvdf) & La cérémonie D183 VÉCUE de bout\n"
             "en bout, la phrase TOURNÉE et l'ancienne REFUSÉE, le séquestre Shamir 5/3 la garde\n"
             "ACTIVE, le dépôt PUBLIC (D220), la rotation VÉRIFIÉE — la ligne D81 du modèle de\n"
             "menace porte l'état vécu ; le runbook § 7.5 du Livre au statut VÉCU \\\\",
             "la ligne D223 à l'annexe B")

# ---- (ansz8lvdf 2) la section nouveautés v0.15.5 ------------------------------
A = A + """

\\subsection{Ce que change la v0.15.5}\\label{sec:nouveautes155}

L'édition v0.15.5 est L'ÉDITION DE L'ÉTAT VÉCU DE LA GOUVERNANCE
(l'instruction ansz8lvdf, la décision D223) : AUCUNE règle R1--R11
modifiée, AUCUN profil touché — le modèle de menace (§ 15) et la
gouvernance (§ 14) portés à l'État VÉCU : (1) la cérémonie de séquestre
D183 EST VÉCUE (19 novembre 2026) — le découpage Shamir cinq parts
seuil trois, la répartition sur cinq médias dont deux hors nuage, la
reconstitution à froid PROUVÉE DEUX FOIS, la phrase de contrôle commise
TOURNÉE et l'ancienne REFUSÉE à la ré-ouverture ; (2) la ligne D81 du
modèle de menace porte le séquestre chiffré comme LA GARDE ACTIVE — la
phrase de contrôle ne vit plus au dépôt ni au coffre Drive ; (3) le
dépôt est PUBLIC (D220) — la matrice de visibilité honorée ; (4) la
rotation VÉRIFIÉE : le re-scan de l'historique git complet re-essayé et
trié (dix constats, aucune fuite réelle au-delà de l'arbitrage assumé).
Les corrections de cohérence de l'instruction gq117wphb portées : le
titre de l'annexe décisionnelle à la plage réelle de la table
(D75--D223), l'ordre croissant des sections de versions (§ 1.18--§ 1.21),
l'étiquette D195 (la re-mesure v0.14.0 au contenu seul) DISTINGUÉE des
mesures instrumentées v0.17 et de la médiane adoptée OPT-04. Le Livre
du Coffre v1.4 porte le runbook § 7.5 au statut VÉCU ; le manuscrit
v0.19.6 porte les statuts à l'état vécu ; le linter inter-pièces v196
confronte le statut D81/D183/D220 aux cinq pièces.
"""

(ICI / "main.tex").write_text(S, encoding="utf-8")
(ICI / "sec-a.tex").write_text(A, encoding="utf-8")
(ICI / "sec-d.tex").write_text(D, encoding="utf-8")
print(f"LE PATCHER v155 : {len(FAITS)} remplacements ancrés — TOUS VERTS")
for f in FAITS:
    print(f"  — {f}")
