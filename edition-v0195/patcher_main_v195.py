#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_main_v195.py — l'édition v0.19.5 du manuscrit (née de
edition-v0194 par copie) : LA CLÔTURE DE LA VAGUE 7 (l'instruction
1c4sokpii, la cinquième et dernière) — le critère d'échantillon D210 tenu
à N=7 sans nouveau tirage, la batterie d'injection de fautes (811/832,
97,5 %, le reste de 21 nommé à treize familles), l'indépendance
inter-familles au GAP NOMMÉ (jamais simulé), le paquet d'évaluation
(reproduction en une commande, grille codée, protocole du second
annotateur pré-enregistré, κ autotesté 3/3) — ET LE STATUT DE
GOUVERNANCE PORTÉ À L'ÉTAT VÉCU : la cérémonie D183 fut VÉCUE le 19/11
(l'Entrée 365 — cinq parts à seuil trois, la reconstitution à froid
prouvée deux fois, la phrase commise tournée et l'ancienne refusée, le
re-scan de l'historique complet re-essayé et trié), le dépôt rendu
public à la décision D220 : les lignes « préparée, geste au
développeur » de la v0.19.4 étaient DEvenues STALES À SON SCELLAGE —
la présente les porte à l'état exact. AUCUNE valeur mesurée modifiée.
Chaque remplacement EST ANCRÉ — REFUS si une ancre manque."""
import pathlib
import shutil

SRC = pathlib.Path(__file__).resolve().parents[1] / "edition-v0194"
ICI = pathlib.Path(__file__).resolve().parent
shutil.copy2(SRC / "main.tex", ICI / "main.tex")
shutil.copy2(SRC / "refs.bib", ICI / "refs.bib")
shutil.copytree(SRC / "donnees", ICI / "donnees", dirs_exist_ok=True)
M = (ICI / "main.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(texte, ancien, nouveau, nom):
    if ancien not in texte:
        raise SystemExit(f"[v0195] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- 1. l'en-tête du fichier ---------------------------------------------
M = remplace(
    M,
    """%  TRIADE — édition académique v0.19.4 (manuscrit IMRAD, anglais)
%  L'édition v0.19.4 est L'ÉDITION DU COÛT DE LA BOUCLE (l'instruction""",
    """%  TRIADE — édition académique v0.19.5 (manuscrit IMRAD, anglais)
%  L'édition v0.19.5 est L'ÉDITION DE LA CLÔTURE DE LA VAGUE 7
%  (l'instruction 1c4sokpii, la vague du 19/11, la cinquième et
%  dernière) née de la v0.19.4 (le coût de la boucle) : le CRITÈRE
%  D'ÉCHANTILLON du plan D210 TENU À N=7 SANS NOUVEAU TIRAGE (le
%  comptage lu du registre, l'amendement conditionnel jamais déclenché),
%  LA BATTERIE D'INJECTION DE FAUTES aux seize scénarios (811/832 tués,
%  97,5 % — 35 tués par l'injection, le reste de 21 NOMMÉ à treize
%  familles de causes, AUCUN tueur affaibli — la console v0.14.0
%  reproduite d'abord), L'INDÉPENDANCE INTER-FAMILLES au GAP NOMMÉ
%  (la confrontation mathématique tenue ; le modèle local open-weights
%  de seconde famille récite 0/64 et COPIE à la correction — le gap de
%  capacité du 1,5B disponible ; le bras C généré passe l'épreuve POSIX
%  à 1984/2011 — jamais simulé), LE PAQUET D'ÉVALUATION (la
%  reproduction en une commande aux graines consignées, la grille codée
%  des 11 défauts, le protocole du second annotateur pré-enregistré
%  κ ≥ 0,61, le calculateur autotesté 3/3) — ET LE STATUT DE
%  GOUVERNANCE PORTÉ À L'ÉTAT VÉCU : la cérémonie D183 VÉCUE le 19/11
%  (l'Entrée 365 : cinq parts à seuil trois, la reconstitution à froid
%  prouvée deux fois, la phrase commise tournée et l'ancienne refusée,
%  le re-scan de tout l'historique re-essayé — dix constats triés,
%  aucun jeton réel commis), le dépôt PUBLIC à la décision D220. Les
%  lignes « préparée, geste au développeur » portées par la v0.19.4
%  étaient devenues STALES À SON SCELLAGE (la cérémonie vécut à 11:17,
%  l'édition fut scellée à 19:56) — la présente les porte à l'état
%  exact. AUCUNE valeur mesurée modifiée.
%  L'édition v0.19.4 est L'ÉDITION DU COÛT DE LA BOUCLE (l'instruction""",
    "l'en-tête du fichier (v0.19.5)")

# ---- 2. la ligne de date : la clause v0.19.5 s'ajoute ---------------------
M = remplace(
    M,
    "the D204 falsification stands as measured and dated; no measured "
    "value modified)}",
    "the D204 falsification stands as measured and dated; no measured "
    "value modified); this v0.19.5 is the wave-7-close edition (the "
    "1c4sokpii instruction): the plan-D210 sample criterion held at "
    "$N{=}7$ without a new draw (seven units fully delivered at both "
    "arms --- the application and loupe-01, -02, -05, -08, -13, -16 --- "
    "read from the register, the conditional amendment never "
    "triggered), the fault-injection battery killing thirty-five of "
    "the fifty-six named survivors --- 811/832 (97.5\\%), the "
    "twenty-one remaining each named to one of thirteen cause "
    "families, no killer weakened (the v0.14.0 console reproduced "
    "first at the consigned seed), the inter-family independence "
    "attempt named to its gap (the mathematical confrontation held at "
    "zero divergence; the local open-weights second family recites "
    "0/64 and copies at correction --- the capacity gap of the "
    "available 1.5B model; the generated C arm passes the POSIX "
    "differential at 1984/2011, its remaining range short --- never "
    "simulated), the evaluation packet delivered (the one-command "
    "reproduction at the consigned seeds, green end-to-end; the coded "
    "grid; the pre-registered $\\kappa\\ge0.61$ second-annotator "
    "protocol; the calculator autotested 3/3), and the governance "
    "status carried as lived (the D183 sequestration ceremony lived "
    "end-to-end on 19 November --- the five-part threshold-three "
    "split, the cold reconstitution proven twice, the committed phrase "
    "rotated and the old one refused, the full-history secrets scan "
    "re-tried with ten findings triaged and no real token ever "
    "committed; the repository public at D220); no measured value "
    "modified)}",
    "la ligne de date (la clause v0.19.5)")

# ---- 3. le plan D210 : le critère d'échantillon clos sans tirage ----------
M = remplace(
    M,
    """verbatim at its arity).

\\section{Results}""",
    """verbatim at its arity).

\\paragraph{The sample criterion, closed without a new draw (v0.19.5).}
The plan's $n\\ge6$ criterion was closed by reading the register (the
fifth wave-7 instruction): \\emph{seven} units fully delivered at both
arms --- the application and loupe-01, -02, -05, -08, -13 and -16 ---
$N{=}7\\ge6$: \\emph{held}. The four-unit draw sequence was exhausted
at the delivery cap (the closure consigned with the v0.19.0 edition),
so the plan's conditional amendment (``amend before any new draw if
the sequence is exhausted'') was never triggered --- there was no draw
to precede; no new draw took place, none was needed. The field runs
remain at the developer's gesture, the ledger's every line closed.

\\section{Results}""",
    "le critère d'échantillon D210 (v0.19.5)")

# ---- 4. la batterie d'injection de fautes (après le paragraphe v0.14.0) ---
M = remplace(
    M,
    """this gap is \\emph{named}, not
hidden, and is the primary target of the next edition.""",
    """this gap is \\emph{named}, not
hidden, and is the primary target of the next edition.

\\paragraph{Fault-injection battery (v0.19.5).} The fifty-six named
survivors were re-run under a \\emph{fault-injection battery}: sixteen
application scenarios at the evidence conventions --- the missed,
locked and refused opens; the GO mode lived end-to-end (the empty
commit, out-of-bounds, the hexa keys, DEL, ESC); the search to the end
and past the last occurrence (the occurrence count read from the file
itself); the full 256-distinct-byte journal and the non-hexa
character; the incomplete bottom line; the boundary keys; the handle
at the most-significant word; and the block-level faults (no session,
outside file, null exit, the \\code{ReadFile} shim failing, the search
string at the input convention --- the clean state at every call, the
non-volatiles verified, the verdicts read at the block). The battery
reproduces the v0.14.0 console \\emph{identically first} (776/832 at
the consigned seed 20261111 --- no new draw), then kills thirty-five
of the fifty-six: \\textbf{811/832 (97.5\\%)} --- 83.4\\% $\\rightarrow$
93.3\\% $\\rightarrow$ 97.5\\% across the three programmes. The
twenty-one remaining survivors are each named to one of thirteen cause
families (six the dying state --- fields written at close die with the
window, no observable reads them back; three the blind shim --- the
scroll and invalidation calls read neither flag nor handle; two the
post-entry view tracking; and one each: the never-served error code,
the volatile RBP under msx64, the adjacent sentinel, the off-table
transfer site, the never-served handle, the field beyond the pattern,
the never-served failure path, the converging guards, the reframe
path, the diverted target falling back). \\emph{No killer weakened}:
the original console was reproduced before the battery ran, and the
sealed pieces were never touched --- the battery writes to the
emulations.""",
    "la batterie d'injection de fautes (v0.19.5)")

# ---- 5. la discussion : D81/D183 portés à l'état vécu ---------------------
M = remplace(
    M,
    """--- and D81 \\emph{remains} the active decision (the ceremony belongs to
the developer) --- \\emph{now prepared} as decision D219: the escrow kit
refreshed (the autotest re-run with proven falsification), the
full-history secrets scan dry-run green, the rotation checklist and the
repository visibility matrix delivered, the transparency-log extension
documented without applying it.""",
    """--- D81 remained the active decision while the ceremony belonged to
the developer: decision D219 prepared it (the escrow kit refreshed
with proven falsification, the full-history secrets scan dry-run
green, the rotation checklist and the repository visibility matrix
delivered, the transparency-log extension documented without applying
it), and the D183 sequestration ceremony was then \\emph{lived
end-to-end} on 19 November: the five-part threshold-three split, the
cold reconstitution proven twice, the committed phrase rotated and the
old one refused, the full-history secrets scan re-tried (ten findings
triaged, no real token ever committed), the repository made public at
decision D220.""",
    "la discussion D81/D183 à l'état vécu (v0.19.5)")

# ---- 6. la conséquence D81 : la phrase retirée, le troisième geste --------
M = remplace(
    M,
    """honest accounting of the current decision adds a row to the threat
model: the control passphrase lives in clear at the repository (the
survival-over-confidentiality arbitration, D81), and the CF3 container""",
    """honest accounting of the decision as it stood added a row to the
threat model: the control passphrase lived in clear at the repository
(the survival-over-confidentiality arbitration, D81) until the D183
ceremony withdrew it on 19 November, and the CF3 container""",
    "la conséquence D81 — la phrase retirée (v0.19.5)")

M = remplace(
    M,
    """transparency-log extension documented \\emph{without applying it} ---
closing the passphrase exposure belongs to the developer; and the
laboratory's own tests run on temporary clones with test phrases only""",
    """transparency-log extension documented \\emph{without applying it} ---
and the developer then lived the third gesture: the D183 sequestration
executed end-to-end on 19 November (the five-part threshold-three
split, the cold reconstitution proven twice), the committed phrase
rotated and the old one refused, the full-history secrets scan
re-tried and triaged (ten findings, no real token ever committed), the
repository made public at decision D220 --- the passphrase exposure is
closed, and the laboratory's own tests run on temporary clones with
test phrases only""",
    "la conséquence D81 — le troisième geste vécu (v0.19.5)")

# ---- 7. la conclusion : la batterie au canon des survivants ----------------
M = remplace(
    M,
    """and the mutation campaign re-run with
composition killers (93.3\\%, tls13 and sys at 100\\%, the 56 remaining
survivors named). The v0.15.0 programme closes the formal side:""",
    """and the mutation campaign re-run with
composition killers (93.3\\%, tls13 and sys at 100\\%, the 56 remaining
survivors named; the v0.19.5 fault-injection battery then killing
thirty-five more --- 811/832, 97.5\\%, the twenty-one remaining each
named to one of thirteen cause families, no killer weakened). The
v0.15.0 programme closes the formal side:""",
    "la conclusion — la batterie au canon (v0.19.5)")

# ---- 8. la conclusion : l'indépendance inter-familles et le paquet --------
M = remplace(
    M,
    """bit-identical at replay), every claim carrying a systematic
status. What remains open""",
    """bit-identical at replay), every claim carrying a systematic
status. The v0.19.5 wave-close programme adds the evaluation packet:
the sample criterion held at $N{=}7$ without a new draw, the
inter-family independence attempt named to its gap (the mathematical
confrontation held at zero divergence; the local open-weights second
family recites 0/64 and copies at correction --- the capacity gap of
the available 1.5B model, never simulated; the generated C arm passes
the POSIX differential at 1984/2011, its remaining range short), the
one-command reproduction at the consigned seeds (green end-to-end),
the coded defect grid, and the pre-registered second-annotator
protocol with its calculator autotested. What remains open""",
    "la conclusion — le paquet d'évaluation (v0.19.5)")

# ---- 9. la conclusion : ce qui demeure ouvert, à l'état exact --------------
M = remplace(
    M,
    """What remains open
is now precisely measured: the 56 mutation survivors in orchestration
blocks, the single-run scope""",
    """What remains open
is now precisely measured: the twenty-one mutation survivors, each
named to one of thirteen cause families (thirty-five killed by the
v0.19.5 fault-injection battery), the single-run scope""",
    "la conclusion — le reste de 21 (v0.19.5)")

M = remplace(
    M,
    """the missing
independent replication
(the T/X grid and the $\\kappa$ calculator are ready; the second
annotator is yet to be recruited) --- and, on the
governance side, the D183 escrow ceremony, prepared and waiting for the
developer's gesture.""",
    """the missing
independent replication
(the grid coded, the $\\kappa$ calculator autotested, the protocol
pre-registered at $\\kappa\\ge0.61$; the second annotator is yet to be
recruited) --- and, on the governance side, nothing prepared remains
waiting: the D183 escrow ceremony was lived end-to-end on 19 November
(the five-part threshold-three split, the cold reconstitution proven
twice), the committed phrase rotated and the old one refused, the
full-history secrets scan re-tried (ten findings triaged, no real
token ever committed), the repository made public at decision D220 and
joined by the Zenodo version DOI.""",
    "la conclusion — la gouvernance à l'état vécu (v0.19.5)")

(ICI / "main.tex").write_text(M, encoding="utf-8")
print("[v0195] les ancrages posés :", " ; ".join(FAITS))
