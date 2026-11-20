#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_livre_v14.py — le Livre du Coffre v1.4 (né de v1.3 par copie) :
LE RUNBOOK § CÉRÉMONIE D183 AU STATUT VÉCU (ansz8lvdf — les sept gestes
accomplis, la reconstitution à froid prouvée deux fois), la matrice de
visibilité à public + Zenodo, QUATORZE arbres partout, les références de
spec à la courante. Chaque remplacement EST ANCRÉ."""
import pathlib
import shutil

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parent / "livre_v13"
for f in [SRC / "main.tex", *SRC.glob("sec-*.tex"), SRC / "cover.html",
          SRC / "merge_cover.py"]:
    if f.exists():
        shutil.copy2(f, ICI / f.name)

M = (ICI / "main.tex").read_text(encoding="utf-8")
T = {n: (ICI / f"sec-{n}.tex").read_text(encoding="utf-8")
     for n in range(1, 7)}
FAITS = []


def remplace(txt, ancien, nouveau, nom):
    if ancien not in txt:
        raise SystemExit(f"[v14] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return txt.replace(ancien, nouveau)


# ---- l'en-tête (v1.4) -------------------------------------------------------
M = remplace(M, "%  LE LIVRE DU COFFRE — TRIADE CF1 -> CF2 -> CF3 (v1.3, D219)",
             "%  LE LIVRE DU COFFRE — TRIADE CF1 -> CF2 -> CF3 (v1.4, D223)",
             "l'en-tête (v1.4)")
M = remplace(M, "v1.3 : le runbook gagne la cérémonie de séquestre D183 (D219)",
             "v1.4 : la cérémonie D183 VÉCUE (D223 — le runbook au statut vécu,\n"
             "%  la matrice de visibilité public + Zenodo, quatorze arbres)\n"
             "%  v1.3 : le runbook gagne la cérémonie de séquestre D183 (D219)",
             "la ligne de version (v1.4)")

# ---- (ansz8lvdf 3) le runbook D183 : PRÉPARÉE -> VÉCUE -----------------------
T[4] = remplace(T[4],
                "\\subsection{La cérémonie de séquestre D183 — préparée, le geste au maître}\\label{sec:cerd183}\n"
                "\n"
                "\\textbf{L'ÉTAT} : le kit vit au dépôt (\\code{scripts/kit\\_ceremonie\\_d183/}),\n"
                "\\emph{préparé au laboratoire, NON appliqué} (D219) — le coffre réel n'a pas\n"
                "été touché, la phrase demeure au fichier-remise D81, aucune clé manipulée.",
                "\\subsection{La cérémonie de séquestre D183 — VÉCUE le 19 novembre 2026}\\label{sec:cerd183}\n"
                "\n"
                "\\textbf{L'ÉTAT (D223, l'état vécu acté)} : la cérémonie EST VÉCUE de bout\n"
                "en bout le 19 novembre 2026 — les SEPT GESTES accomplis : le découpage\n"
                "Shamir cinq parts seuil trois, la répartition sur cinq médias dont deux\n"
                "hors nuage, LA RECONSTITUTION À FROID PROUVÉE DEUX FOIS (le mode\n"
                "\\code{--verifier} fail-closed, vert deux fois), la phrase de contrôle\n"
                "commise TOURNÉE, l'ANCIENNE REFUSÉE à la ré-ouverture (la preuve du\n"
                "renouvellement), le re-scan de l'historique git complet re-essayé et trié\n"
                "(dix constats, aucune fuite réelle — l'arbitrage assumé), et le dépôt\n"
                "passé PUBLIC (D220). Le coffre réel n'a PAS été migré d'époque ni\n"
                "re-manipulé : l'état vécu est ACTÉ (D223), la garde active est le\n"
                "séquestre 5/3, la phrase ne vit plus au fichier-remise D81.",
                "le runbook D183 (VÉCU, les sept gestes)")

# ---- (ansz8lvdf 3) la garde D81 (sec-2) : l'état vécu ------------------------
T[2] = remplace(T[2],
                "La transition vers une garde plus dure est \\emph{préparée} (D219) : le",
                "La garde plus dure EST VÉCUE depuis le 19 novembre 2026 (D223) : le",
                "sec-2 la transition (vécue)")
T[2] = remplace(T[2],
                "(cf. § \\ref{sec:cerd183}), la cérémonie au maître, la garde D81 demeure",
                "(cf. § \\ref{sec:cerd183}) — la cérémonie VÉCUE, la garde ACTIVE est le\n"
                "séquestre 5/3 ; la garde D81 est AMENDÉE (la phrase tournée, l'ancienne",
                "sec-2 la garde active (le séquestre)")

# ---- (gq117wphb 6) QUATORZE arbres partout ------------------------------------
T[4] = remplace(T[4], "\\code{sceau\\_I.py verifier} — dix arbres VERTS, code 0.",
                "\\code{sceau\\_I.py verifier} — quatorze arbres VERTS, code 0.",
                "quatorze arbres (sec-4, la vérification)")
T[4] = remplace(T[4], "py -3 v06\\sceau_I.py verifier      (dix arbres VERTS, code 0)",
                "py -3 v06\\sceau_I.py verifier      (quatorze arbres VERTS, code 0)",
                "quatorze arbres (sec-4, la commande)")
T[6] = remplace(T[6], "La signature Ed25519 des arbres de couche I ; dix arbres,",
                "La signature Ed25519 des arbres de couche I ; quatorze arbres,",
                "quatorze arbres (le glossaire)")

# ---- (gq117wphb 6) les références de spec à la courante -----------------------
T[5] = remplace(T[5],
                "sha-256 des modules, alignée sur l'annexe A de la spécification v0.15.2",
                "sha-256 des modules, alignée sur l'annexe A de la spécification v0.15.5",
                "la référence de spec (sec-5, la première)")
T[5] = remplace(T[5],
                "l'annexe A de la spécification v0.15.2 (contenu canonique LF du dépôt).}",
                "l'annexe A de la spécification v0.15.5 (contenu canonique LF du dépôt).}",
                "la référence de spec (sec-5, la caption)")

(ICI / "main.tex").write_text(M, encoding="utf-8")
for n, txt in T.items():
    (ICI / f"sec-{n}.tex").write_text(txt, encoding="utf-8")
print(f"LE PATCHER v14 : {len(FAITS)} remplacements ancrés — TOUS VERTS")
for f in FAITS:
    print(f"  — {f}")
