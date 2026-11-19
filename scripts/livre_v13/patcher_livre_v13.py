#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_livre_v13.py — l'édition v1.3 du Livre du Coffre (née de
livre_v12 par copie) : LE RUNBOOK GAGNE LA SECTION CÉRÉMONIE DE SÉQUESTRE
D183 (l'instruction jx4l5vy5c, D219). AUCUN geste de cérémonie changé —
la section documente le kit PRÉPARÉ, le geste au développeur. Chaque
remplacement EST ANCRÉ — REFUS si une ancre manque."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent

# ---- les versions (couverture, corps, fusion) -----------------------------
for f in ("cover.html", "main.tex", "merge_cover.py"):
    p = ICI / f
    t = p.read_text(encoding="utf-8")
    t = t.replace("(v1.2, D218)", "(v1.3, D219)")
    t = t.replace("v1.2 : édition de cohérence inter-pièces (D218)",
                  "v1.3 : le runbook gagne la cérémonie de séquestre D183 (D219)")
    t = t.replace("Version 1.2", "Version 1.3")
    t = t.replace("(v1.2)", "(v1.3)")
    t = t.replace("révision v1.2 (D218, édition de cohérence)",
                  "révision v1.3 (D219, le séquestre préparé)")
    t = t.replace("révision v1.2 (D218)", "révision v1.3 (D219)")
    p.write_text(t, encoding="utf-8")
    print(f"[versions] {f} porté à v1.3")

S2 = (ICI / "sec-2.tex").read_text(encoding="utf-8")
S4 = (ICI / "sec-4.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(texte, ancien, nouveau, nom):
    if ancien not in texte:
        raise SystemExit(f"[livre_v13] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- sec-2 : la garde de la phrase — le pointeur D183 ----------------------
S2 = remplace(
    S2,
    r"""vie : on ne compte plus sur sa confidentialité, la rotation reste le remède.""",
    """vie : on ne compte plus sur sa confidentialité, la rotation reste le remède.
La transition vers une garde plus dure est \emph{préparée} (D219) : le
séquestre chiffré D183 — la phrase répartie en cinq parts à seuil trois
(cf. § \\ref{sec:cerd183}), la cérémonie au maître, la garde D81 demeure
ACTIVE jusqu'au geste vécu.""",
    "sec-2 : le pointeur D183 à la garde de la phrase")

# ---- sec-4 : LA SECTION CÉRÉMONIE D183 (avant « La clôture ») --------------
SEC_D183 = r"""
\subsection{La cérémonie de séquestre D183 — préparée, le geste au maître}\label{sec:cerd183}

\textbf{L'ÉTAT} : le kit vit au dépôt (\code{scripts/kit\_ceremonie\_d183/}),
\emph{préparé au laboratoire, NON appliqué} (D219) — le coffre réel n'a pas
été touché, la phrase demeure au fichier-remise D81, aucune clé manipulée.
\textbf{L'ANALYSE} qui la fonde : sous D81, l'espérance de perte annuelle
$\approx 4{,}0 \times 10^{-2}\,C_{exposure}$ (l'exposition domine — un seul
des quatre emplacements compromis suffit, $\approx 3{,}9~\%$/an) contre
$\approx 1{,}0 \times 10^{-3}$ sous le séquestre 5/3 — \textbf{un facteur
$\approx 40$}. Le partage est celui du coffre CF2 (D120, l'instrument
\code{v06/coffre\_cf2.py} TEL QUEL) : cinq parts, seuil trois.

\textbf{L'OUTIL EST PROUVÉ À FROID} : l'autotest du kit (19/11, D219) — les
dix combinaisons de trois parts reconstituent EXACTEMENT, les dix paires
sous le seuil rendent un déchet, \emph{une part forgée est REFUSÉE par la
porte de l'empreinte de contrôle} (la falsification prouvée), la même porte
rendant VERT la combinaison honnête. Le mode \code{--verifier} est
fail-closed : il confronte LUI-MÊME le sha256 du rendu à l'empreinte de
contrôle du manifeste — tout écart un refus nommé.

\textbf{LA CÉRÉMONIE, PAS À PAS} (vous, machine propre hors-ligne —
\code{python3 sequestre\_d183.py}) :

\begin{enumerate}
\item \textbf{Préparer} : python3, le dossier du kit, la phrase
(\code{PHRASE-CONTROLE-COFFRE.txt}, à lire vous-même — jamais copée au bac
à sable), et CINQ MÉDIAS : USB ×2, papier ×1, tiers de confiance ×1,
coffre Drive ×1 — au moins DEUX hors nuage (toutes les parts au même
nuage, et le nuage EST le coffre).
\item \textbf{La répétition générale} : \code{--autotest} → VERDICT VERT
exigé (les vingt lignes de reconstitution, la falsification refusée,
l'honnête vert).
\item \textbf{Le découpage} : \code{--ceremonie <fichier-phrase>} → les
cinq parts (une par média, séparément) + le manifeste (empreintes sha256
de chaque part, empreinte de contrôle de la phrase, plan de répartition,
listes de contrôle). Le manifeste peut vivre au dépôt : il ne contient
aucune part.
\item \textbf{La répartition} : chaque part sur son média, les empreintes
recoupées au manifeste.
\item \textbf{La preuve de reconstitution à froid — AVANT TOUT RETRAIT} :
\code{--verifier part-1 part-2 part-3 manifeste} → VERT exigé ; répétez
avec une autre combinaison (ex. 2+4+5) : \textbf{VERT deux fois} ou rien.
\item \textbf{Le retrait} (seulement alors — des gestes humains, jamais
automatisés, la liste de contrôle du manifeste) : la phrase en clair
retirée du dépôt git ET de la racine du coffre Drive ; l'entrée de journal
consignée ; D81 amendée. \textbf{La rotation suit} (la checklist du kit) :
la phrase commise vit à vie dans l'histoire git — seule la rotation la
rend inopérante.
\item \textbf{L'entretien} : un exercice de reconstitution périodique (les
parts se dégradent : médias perdus, gardiens qui changent) — la périodicité
est à vous, l'agenda nommé au manifeste.
\end{enumerate}

\textbf{LES FRONTIÈRES} : le laboratoire n'exécute \emph{jamais} la
cérémonie sur la phrase réelle (D87) ; l'outil ne supprime \emph{jamais}
rien (le retrait est humain, listé) ; le coffre réel demeure intact tant
que la cérémonie n'est pas vécue — et \textbf{le dépôt demeure PRIVÉ}
tant qu'elle ne l'est pas et que la rotation n'est pas vérifiée : public +
Zenodo seulement après (la matrice de visibilité du kit, D219). Le kit
porte aussi le scan de secrets de l'historique git complet (dry-run vert),
la checklist de rotation, la matrice de visibilité et l'extension
transparence publique (Rekor/RFC 3161) documentée sans être appliquée.

\begin{terrain}[— pourquoi le kit ne s'applique pas tout seul]
La raison est consignée à D183 : la proposition ne se substitue à la garde
durable QUE si la cérémonie des parts est VÉCUE de bout en bout — parts
réellement créées, réellement réparties, reconstitution PROUVÉE à froid
deux fois. Sinon elle AJOUTE un risque de perte au lieu d'en retirer un :
des parts qui n'existent pas protègent moins qu'un fichier qui existe.
Le protocole prépare, le maître décide.
\end{terrain}
"""
S4 = remplace(
    S4,
    "\\subsection{La clôture, cérémonie du quotidien}\\label{sec:cloture}",
    SEC_D183.strip() + "\n\n\\subsection{La clôture, cérémonie du quotidien}"
    "\\label{sec:cloture}",
    "sec-4 : la section cérémonie D183 (avant La clôture)")

# ---- sec-4 : le runbook, l'ordre des gestes — le pointeur D183 -------------
S4 = remplace(
    S4,
    """\\item \\textbf{DÉTRUIRE CF2} : après recoupement — la case explicite. Le rapport
part par « Envoyer le rapport ».
\\end{enumerate}""",
    """\\item \\textbf{DÉTRUIRE CF2} : après recoupement — la case explicite. Le rapport
part par « Envoyer le rapport ».
\\item \\textbf{Le séquestre de la phrase (D183, préparé D219)} : au
commandement — la cérémonie § \\ref{sec:cerd183} (le kit au dépôt) ; tant
qu'elle n'est pas vécue, la garde D81 demeure et le dépôt demeure PRIVÉ.
\\end{enumerate}""",
    "sec-4 : le runbook — le pointeur séquestre D183 à l'ordre des gestes")

(ICI / "sec-2.tex").write_text(S2, encoding="utf-8")
(ICI / "sec-4.tex").write_text(S4, encoding="utf-8")
print(f"[livre_v13] {len(FAITS)} ancrage(s) remplacé(s) :")
for f in FAITS:
    print(f"  - {f}")
print("TOUT VERT — les sources v1.3 sont prêtes à compiler")
