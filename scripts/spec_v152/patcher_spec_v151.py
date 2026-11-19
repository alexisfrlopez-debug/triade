#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v151.py — l'édition v0.15.2 de la spécification (née de
spec_v151 par copie) : LA LIGNE D81 DU MODÈLE DE MENACE AU STATUT EXACT
(l'instruction jx4l5vy5c, la vague 7, la deuxième — D219), le § 1.18, le
journal des versions. AUCUNE règle modifiée (l'édition documentaire).
Chaque remplacement EST ANCRÉ — REFUS si une ancre manque."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent

# ---- les versions (couverture, corps, fusion) ----------------------------
for f in ("cover.html", "main.tex", "merge_cover.py"):
    p = ICI / f
    t = p.read_text(encoding="utf-8")
    n = t.count("v0.15.1") + t.count("Version 0.15.1") + t.count("0.15.1")
    t = t.replace("v0.15.1", "v0.15.2").replace("Version 0.15.1",
                                                "Version 0.15.2")
    t = t.replace("l'édition de cohérence inter-pièces",
                  "la transition D81 préparée")
    p.write_text(t, encoding="utf-8")
    print(f"[versions] {f} : {n} occurrence(s) portée(s) à v0.15.2")

A = (ICI / "sec-a.tex").read_text(encoding="utf-8")
D = (ICI / "sec-d.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(texte, ancien, nouveau, nom):
    if ancien not in texte:
        raise SystemExit(f"[spec_v152] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- sec-a : le § 1.18 NOUVEAU (après le § 1.17) --------------------------
ANC_117_FIN = """partagées aux cinq pièces du pack à chaque build (D218).
"""
SEC118 = r"""\subsection{Ce que change la v0.15.2}\label{sec:nouveautes152}

L'ÉDITION DE LA TRANSITION PRÉPARÉE (D219, l'instruction jx4l5vy5c — la
vague du 18/11, la deuxième) : AUCUNE règle modifiée, aucune couche
ajoutée, aucun artefact scellé touché, le coffre réel et les phrases
réelles JAMAIS approchés (D105 : passeur.exe/passeur-c.dll re-téléchargés
intacts, le sceau 14 arbres verts). La ligne D81 du modèle de menace
(§\ref{sec:menaces}) est portée à SON STATUT EXACT : la transition vers
le séquestre chiffré D183 est \textbf{préparée, geste au développeur} —
le kit de cérémonie rafraîchi (l'autotest rejoué : 10/10 combinaisons
exactes, 10/10 paires sous le seuil inertes, la falsification PROUVÉE —
une part forgée REFUSÉE par la porte de l'empreinte de contrôle ; le
mode \code{--verifier} fail-closed né au geste), l'analyse chiffrée
perte/exposition reprise (le facteur $\approx$ 40 en faveur du
séquestre), le scan de secrets de l'historique git complet au dry-run
vert (l'équivalent Python nommé, gitleaks/trufflehog absents — six
secrets plantés sur six attrapés, zéro faux négatif ; le vrai dépôt
trié : la phrase D81 connue, neuf fixtures de test nommées, aucune
fuite réelle au-delà de l'arbitrage assumé), la checklist de rotation de
toute phrase exposée, la matrice de décision de visibilité du dépôt
(privé tant que la cérémonie n'est pas vécue et la rotation vérifiée ;
public + Zenodo seulement après), et l'extension transparence publique
DOCUMENTÉE NON APPLIQUÉE (l'ancrage du témoin d'époque à Rekor/Sigstore
ou RFC 3161 : le format du témoin, la vérification machine, le delta au
modèle de menace aux deux bords). D81 DEMEURE LA DÉCISION ACTIVE
jusqu'à ce que la cérémonie soit vécue de bout en bout — le protocole
prépare, le maître décide (D87).
"""
A = remplace(A, ANC_117_FIN, ANC_117_FIN + "\n" + SEC118,
             "le § 1.18 (Ce que change la v0.15.2)")

# ---- sec-d : la ligne D81 du modèle de menace au statut exact -------------
ANC_MENACE = r"""\textbf{Vol du coffre-fort des phrases} & chiffrement intégral (Argon2id, contexte
HKDF dédié, AEAD) ; écriture atomique ; depuis D81 la phrase de contrôle vit au coffre
Drive et au dépôt — mitigation première : restreindre le partage par lien & confidentialité
ramenée au contrôle d'accès du dossier ; une phrase commise en git y demeure à vie — la
rotation reste le remède (D75, étendu D81) \\"""
NOU_MENACE = r"""\textbf{Vol du coffre-fort des phrases} & chiffrement intégral (Argon2id, contexte
HKDF dédié, AEAD) ; écriture atomique ; depuis D81 la phrase de contrôle vit au coffre
Drive et au dépôt — mitigation première : restreindre le partage par lien ; la
transition vers le séquestre D183 est PRÉPARÉE (D219 : le kit rafraîchi avec la
falsification prouvée, le scan de secrets au dry-run vert, la checklist de rotation,
la matrice de visibilité — le geste au développeur) & confidentialité
ramenée au contrôle d'accès du dossier ; une phrase commise en git y demeure à vie — la
rotation reste le remède (D75, étendu D81) ; le dépôt demeure PRIVÉ tant que la
cérémonie D183 n'est pas vécue et la rotation vérifiée — public + Zenodo seulement
après (D219) \\"""
D = remplace(D, ANC_MENACE, NOU_MENACE,
             "la ligne D81 du modèle de menace au statut exact (D219)")

# ---- sec-d : le journal des versions (la phrase v0.15.2) ------------------
ANC_JOURNAL = "HISTORIQUES contre les mesures v0.17--v0.18 (D195). La v0.9.0 avait"
NOU_JOURNAL = ("HISTORIQUES contre les mesures v0.17--v0.18 (D195). La v0.15.2 est\n"
               "L'ÉDITION DE LA TRANSITION PRÉPARÉE (D219, la même vague, la\n"
               "deuxième instruction) : AUCUNE règle modifiée — la ligne D81 du\n"
               "modèle de menace à son statut exact (le kit de séquestre D183\n"
               "rafraîchi avec la falsification prouvée, le scan de secrets de\n"
               "l'historique complet au dry-run vert, la checklist de rotation,\n"
               "la matrice de visibilité du dépôt, l'extension transparence\n"
               "publique documentée non appliquée — le statut « préparée, geste\n"
               "au développeur », la garde D81 active jusqu'au geste vécu). "
               "La v0.9.0 avait")
D = remplace(D, ANC_JOURNAL, NOU_JOURNAL,
             "le journal des versions (la phrase v0.15.2)")

(ICI / "sec-a.tex").write_text(A, encoding="utf-8")
(ICI / "sec-d.tex").write_text(D, encoding="utf-8")
print(f"[spec_v152] {len(FAITS)} ancrage(s) remplacé(s) :")
for f in FAITS:
    print(f"  - {f}")
print("TOUT VERT — les sources v0.15.2 sont prêtes à compiler")
