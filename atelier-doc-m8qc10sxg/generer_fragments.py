#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_fragments.py — m8qc10sxg LE GESTE SUIVANT : les onze fragments
restants (DEVELOPER_GUIDE, TROUBLESHOOTING, SECURITY, REFERENCE — humain ;
DOC-LOC, DOC-EDIT, DOC-ADD, DOC-REFUS, DOC-CEREMONY, DOC-FEEDBACK,
CAPABILITY_PROBE — agent) + LE MIROIR FR des treize, générés DES CANONS
(les tables numériques JAMAIS retapées : les budgets parsés du GUIDE-AGENT
[le canon 627/674/2200], les règles R1–R11 parsées du protocole, les dix-huit
blocs du dépôt, les cibles du PLAN-M8QC10SXG gelé).

Déterministe par construction (aucun timestamp, aucun aléa, entrées triées)
— LA CRISTALLISATION 10 rebuilds bit-identiques. Les identificateurs
demeurent LITTÉRAUX aux deux langues (jamais traduits) ; les nombres sont
PARALLÈLES par construction (les mêmes opérandes canoniques rendues aux
deux miroirs).

Sortie : fragments/*.md (EN) + fragments-fr/*.md (FR) +
registres/budgets-complet.json (les opérandes non arrondis, cl100k_base —
le tokenizer natif du relevé AGENT-CORE 216 / QUICKSTART 167) +
MANIFESTE-fragments.txt (sha256 par fichier).
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re

import tiktoken

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-doc-m8qc10sxg"
EN = ICI / "fragments"
FR = ICI / "fragments-fr"
CORPUS_KIT = REPO / "atelier-kit-v2n6v8rao" / "TRIADE_kit_developpeur"

# ------------------------------------------------------------- LES CANONS --
def canon_budgets() -> dict:
    """LES BUDGETS ADOPTÉS parsés du GUIDE-AGENT (la règle 9 — jamais
    retapés) : localiser 627 hiérarchique / éditer 674 / ajouter 2200."""
    t = (REPO / "atelier-guide-zd316de39" / "GUIDE-AGENT.md").read_text(
        encoding="utf-8")
    m = re.search(r"localiser\s+([\d\s]+?)\s+hiérarchique\s*/\s*éditer"
                  r"\s+([\d\s]+?)\s+TPL-EDIT-v1\s*/\s*ajouter"
                  r"\s+([\d\s]+?)\s+squelette", t)
    assert m, "le canon des budgets (GUIDE-AGENT règle 9) a bougé"
    propre = lambda s: int(re.sub(r"\s+", "", s))                  # noqa: E731
    return {"loc": propre(m.group(1)), "edit": propre(m.group(2)),
            "add": propre(m.group(3))}


def canon_regles() -> list:
    """LES ONZE RÈGLES R1–R11 parsées du protocole (le numéro seul est le
    canon ; le nom court EN/FR vit aux tables de rendu ci-dessous)."""
    t = (REPO / "docs" / "PROTOCOLE_TRIADE.md").read_text(encoding="utf-8")
    numeros = re.findall(r"^\|\s*(R\d+)\s*\|", t, re.M)
    assert len(numeros) == 11, f"le canon des règles a bougé: {numeros}"
    return numeros


def canon_blocs() -> list:
    """LES DIX-HUIT BLOCS du dépôt (les notations scellées — l'ordre
    canonique du répertoire, trié)."""
    p = REPO / "loupe" / "notation"
    noms = sorted(f.stem for f in p.glob("loupe-*.asm"))
    assert len(noms) == 18, f"le canon des blocs a bougé: {len(noms)}"
    return noms


def canon_cibles() -> dict:
    """LES CIBLES pré-enregistrées du plan gelé (CORE ≤1500, opérations
    ≤800, REFUS ≤600, CEREMONY ≤1200, FEEDBACK ≤400, PROBE ≤500)."""
    t = (REPO / "PLAN-M8QC10SXG.md").read_text(encoding="utf-8")
    m = re.search(r"CORE\s*≤\s*(\d+),\s*opérations\s*≤\s*(\d+),\s*REFUS"
                  r"\s*≤\s*(\d+),\s*CEREMONY\s*≤\s*(\d+),\s*FEEDBACK"
                  r"\s*≤\s*(\d+),\s*PROBE\s*≤\s*(\d+)", t)
    assert m, "le canon des cibles (le plan gelé) a bougé"
    return {"CORE": int(m.group(1)), "OPERATIONS": int(m.group(2)),
            "REFUS": int(m.group(3)), "CEREMONY": int(m.group(4)),
            "FEEDBACK": int(m.group(5)), "PROBE": int(m.group(6))}


NOMS_REGLES_EN = {
    "R1": "never a bare binary (every B ships with I and C)",
    "R2": "intent first (every change starts as a diff on I)",
    "R3": "mandatory marking (every block is described in C)",
    "R4": "patch at stable contract (callers are never invalidated)",
    "R5": "verify-then-write (no commit without oracle, gold vectors, "
          "round-trip)",
    "R6": "crystallization (ten green verifications make the block "
          "immutable)",
    "R7": "stable addresses (entry points never move; padding)",
    "R8": "cross-lock (block fingerprints and card signature checked "
          "before every edit)",
    "R9": "signed card required (an unsigned card is refused at startup)",
    "R10": "built-in controlled failure (checksums, manifest signature, "
           "anti-rollback, environment — fail-closed, no degraded path)",
    "R11": "measured optimization (a hot path identified by measure, "
           "before/after journaled, contract stable)",
}
NOMS_REGLES_FR = {
    "R1": "jamais un binaire nu (tout B livré avec I et C)",
    "R2": "l'intention d'abord (toute modification commence par un diff sur I)",
    "R3": "balisage obligatoire (chaque bloc décrit dans C)",
    "R4": "patch à contrat stable (les appelants jamais invalidés)",
    "R5": "vérifie-puis-écrit (aucun commit sans oracle, vecteurs dorés, "
          "round-trip)",
    "R6": "cristallisation (dix vérifications rendent le bloc immuable)",
    "R7": "adresses stables (les points d'entrée ne bougent jamais)",
    "R8": "verrou croisé (empreintes et signature vérifiées avant chaque "
          "édition)",
    "R9": "carte signée obligatoire (la carte non signée refusée au départ)",
    "R10": "échec contrôlé intégré (checksums, signature de manifeste, "
           "anti-rollback, environnement — fail-closed, aucun chemin "
           "dégradé)",
    "R11": "optimisation mesurée (un hot path identifié par mesure, "
           "l'avant/après consigné, le contrat stable)",
}

B = canon_budgets()
REGLES = canon_regles()
BLOCS = canon_blocs()
CIBLES = canon_cibles()
BLOCS_EN = "\n".join(BLOCS)
TABLE_REGLES_EN = "\n".join(f"- {n}: {NOMS_REGLES_EN[n]}" for n in REGLES)
TABLE_REGLES_FR = "\n".join(f"- {n} : {NOMS_REGLES_FR[n]}" for n in REGLES)


# ------------------------------------------------- LES DEUX EXISTANTS (EN) --
AGENT_CORE = (EN / "AGENT-CORE.md").read_text(encoding="utf-8")
QUICKSTART = (EN / "QUICKSTART.md").read_text(encoding="utf-8")

# --------------------------------------------------------- LES TREIZE (EN) --
FRAGMENTS_EN = {
"AGENT-CORE": AGENT_CORE,
"QUICKSTART": QUICKSTART,
"DEVELOPER_GUIDE": f"""# DEVELOPER GUIDE — the kit from the developer's bench (canonical English)
The developer kit is built BY CONSTRUCTION from the repository (D130:
git ls-files — never hand-maintained). The manifest carries a sha256
per file, the version vector binds kit / protocol / card / profile,
and the compatibility gate refuses any incompatible triplet
(fail-closed, named refusal).

What the kit carries (M0-in-a-box):
- notation + round-trip: the pointer-alone expansion chain v2 and the
  v3 validators — the judges are INTACT, never weakened;
- the card fragments and the expander, with its four named pointer
  refusals (null, out-of-zone, size, alignment);
- the oracle GENERATOR derived from layer I (never a pre-derived
  oracle shipped — the named kit debt), the FIPS/RFC vectors, the
  independence routes;
- the gates R1-R11 (see REFERENCE);
- the air-gap key-genesis ceremony and the LOCAL seal — no project
  trust anchor ships (neither the project public key nor reference
  signatures; the adopter runs their own genesis);
- the append-only journal template (timestamp, phase, task, verdict,
  native tokens);
- the agent guide, the eval ladder, the gym, the feedback tool, the
  report tool, the triage pipeline.

How to work: freeze the plan BEFORE any data (sha256 recorded, commit
first); measure and publish unrounded operands; a measured failure is
as precious a piece as a green — never a fabricated verdict; the
historical verbatim stays byte for byte, corrections live as
append-only errata; the task order is never re-drawn, the seeds are
recorded.

Regeneration: run the generator — the archive is deterministic
(10 rebuilds bit-identical, timestamps normalized, entries sorted).
The Zenodo deposit of the kit remains the developer's gesture (BSL 1.1
with the D209 grant) — never minted without a command.
""",
"TROUBLESHOOTING": """# TROUBLESHOOTING — the named refusals and what they mean (canonical English)
The protocol never fails silently: every gate refuses with a NAMED
cause. Find the name, repair the named cause alone.

Model notations refused (the judge chain v2 + the validators v3):
- HORS-FORMAT — a line is not an admitted form (a string-prefix REP
  instruction, an inline db, a lowercase label glued to an
  instruction, a truncated literal). Repair: the canonical motif —
  one instruction per line, typed holes.
- ID-INCONNU — an ID absent from the block dictionary. Repair: the
  enumerated IDs only (CST-001..NNN, LBL-001..NNN), never a bare
  symbol.
- EXPANSION-DIVERGENTE — the expanded line diverges (a round-trip
  mismatch, an IAT reached through a label, an ID in a non-expandable
  operand). Repair: the typed hole (mov reg, CST-001 for a constant;
  call CST-004 for the IAT; jcc LBL-001 for an internal jump).
- FORME-INVALIDE — the emitted shape violates the sealed template.
The four pointer refusals at LOCATE (null, out-of-zone, size,
alignment) are named at the gate.

The budget (3 repairs) exhausted: the task ends refused — the verdict
is a piece as precious as a green; never a re-drawn task, never a
silently widened budget.
The doc linter refuses: a numeric divergence between the EN and FR
mirrors, a translated identifier — the parity gates.
The secret scan refuses: a secret, or the marked test phrase (D105) —
the lab copies carry visible marks; the real vault is never touched
in the lab.
The kit gate refuses: an incompatible checkpoint / kit / judges
triplet — fail-closed, named.
The aggregator refuses: a missing run (exit 2, never a partial
verdict); fewer than 10 complete strata reads NOT TESTED (D207).
The kappa gate needs BOTH conditions together (D203): 0.61 reached ON
at least 50 double-coded items.
R10 refuses at launch (checksums, manifest signature, anti-rollback,
environment) — no degraded path exists.
Without response_format at the endpoint: the grammar rides the prompt
and the validators judge — never a weakened judge (the graceful
degradation).
""",
"SECURITY": """# SECURITY — the model in one page (canonical English)
Secrets: never committed — the pre-commit guard combines known-secret
sha256 fingerprints, Shannon entropy (3.8 bits/char on assignments of
28 characters or more) and class patterns (ghp_ / GOCSPX- / PEM /
refresh). The scrub gate is fail-closed with a lived negative control:
a planted secret MUST be caught.

Anchors: NO project trust anchor ships with the kit — neither the
project public key nor reference signatures. The adopter runs their
own air-gap key genesis; the seal is LOCAL.

The real vault is never touched in the lab (D105): lab copies carry a
visible marked test phrase; a report carrying one is REFUSED at the
gate.

Access discipline: the pointer alone (never a bare path); the four
named pointer refusals (null, out-of-zone, size, alignment); one
instruction per line; one memory operand per instruction at most.

Feedback reports: anonymized mechanically (paths, usernames), secret
scan at the door, the schema frozen by sha256 BEFORE any report; the
commentary (500 tokens at most) is marked UNVERIFIED; sending is a
human gesture (D122) — never automatic, the tool is offline.

Dual use: interceptor binaries and dual-use material are excluded
from the permissive subset; the Apache-2.0/CC-BY synthetic tasks stay
separate from the BSL corpus in every split.

Licence: BSL 1.1 with the D209 grant; public digests under CC-BY-4.0
(contributors acknowledged opt-in).

Offline by construction: no network dependency at build (R10); the
tooling runs air-gap.
""",
"REFERENCE": f"""# REFERENCE — the protocol in one page (canonical English)
Three inseparable layers: I (the signed specifications), C (the
encrypted card), B (the byte-locked artifact). Lexicographic
priorities: security > performance > optimization > token cost.

The notation: one instruction per line; typed holes (register /
offset / LBL-CST target); dictionary IDs only — CST-001..NNN for
constants and IAT entries (the IAT is called: call CST-004), LBL-001
..NNN for internal labels (uppercase, on their own line); the narrow
source (movzx rax, ecx); one memory operand per instruction at most.

The judges: the pointer-alone expansion chain v2, the validators v3,
the round-trip (what you write is what expands is what comes back).
A one-byte mutant is caught — never game the judge.

The budgets (unrounded operands at the kit manifest): locate {B['loc']}
/ edit {B['edit']} / add {B['add']}; the repair budget is 3.

The gates R1-R11:
{TABLE_REGLES_EN}

The refusal classes: HORS-FORMAT, ID-INCONNU, EXPANSION-DIVERGENTE,
FORME-INVALIDE (the notation); HUNK-INCONNU, CONTEXTE-DIVERGENT,
ROUND-TRIP-DIVERGENT (the edit); POINTEUR-INCONNU,
EMPREINTE-DIVERGENTE (the pointer). Repair the named cause alone.

The 18 bench blocks (the sealed notations of the repository):
{BLOCS_EN}

The ceremonies: the air-gap key genesis, the LOCAL seal, the
append-only journal (corrections are errata, never rewrites), the
secret guard at commit, the release deposit as a human command.

Decisions cited as literals (never translated): D81 (the durable
guard), D105 (the marked test phrase), D122 (the human send), D130
(the kit by construction), D203 (the kappa grid), D207 (the stopping
rules), D209 (the grant), D250 (the arbitration to the developer).
""",
"DOC-LOC": f"""# DOC-LOC — the LOCATE operation (canonical English, compact)
The pointer alone is the access contract: never a bare path, never a
guessed offset. Observe the fragment, read the dictionary, emit the
pointer form; the gate names its four refusals — null, out-of-zone,
size, alignment — and you repair the named cause alone, the rest byte
for byte. The sealed fragment is the reference; the expander admits
only what the dictionary admits. Budget: {B['loc']} (hierarchical —
the unrounded operand lives at the kit manifest); the repair budget
is 3; on the fourth refusal the task ends refused — a piece as
precious as a green. Never game the judge: a one-byte mutant is
caught at the mutation battery. The loop in seven steps: observe the
fragment, read the dictionary, emit the notation, read the judge
verdict, read the named diff, repair the named cause alone, resubmit.
""",
"DOC-EDIT": f"""# DOC-EDIT — the EDIT operation (canonical English, compact)
The edit rides the sealed template TPL-EDIT-v1: emit the hunks, never
a free-text rewrite. The four edit refusals are named — HORS-FORMAT
(the hunk shape violates the template), HUNK-INCONNU (the hunk does
not apply at its anchor), CONTEXTE-DIVERGENT (the surrounding bytes
moved), ROUND-TRIP-DIVERGENT (what you wrote does not come back) —
repair the named cause alone, every untouched line byte for byte.
The patch honors the published contract (R4): same signature, same
pre- and post-conditions, the callers are never invalidated. No
commit without the oracle, the gold vectors and the round-trip (R5).
Budget: {B['edit']} (unrounded at the manifest); the repair budget is
3. The reference is the sealed notation of the block — never a
recitation of a neighbor, the exemplar is a reference, not a
shortcut.
""",
"DOC-ADD": f"""# DOC-ADD — the ADD operation (canonical English, compact)
The addition rides the skeleton SQUELETTE-v2: the ABI frame and the
typed holes are given; you emit the LOGIC lines only. One instruction
per line; one memory operand per instruction at most; typed holes
only (register / offset / LBL-CST target); the dictionary IDs —
CST-001..NNN for constants and IAT entries (the IAT is called: call
CST-004), LBL-001..NNN for internal labels, uppercase, on their own
line; the narrow source (movzx rax, ecx); no inline data (the data
lives in the frame); no string-prefix REP instructions. Budget:
{B['add']} (unrounded at the manifest); the repair budget is 3. On a
refusal, read the named diff, repair the named cause alone, resubmit
— the judges are intact, a weakened judge is a lost gain. The
canonical form is expected from you at the first emission: the
normalizer never repairs a forbidden form.
""",
"DOC-REFUS": """# DOC-REFUS — the refusal grammar (canonical English, compact)
Every refusal carries a NAMED class — the class is a protocol
constant, never translated: HORS-FORMAT, ID-INCONNU,
EXPANSION-DIVERGENTE, FORME-INVALIDE; at the pointer: null,
out-of-zone, size, alignment; at the edit: HUNK-INCONNU,
CONTEXTE-DIVERGENT, ROUND-TRIP-DIVERGENT. The loop on a refusal: read
the class, read the named cause, repair THE NAMED CAUSE ALONE — every
other line stays byte for byte — resubmit within the repair budget 3.
Never average a refusal away, never re-draw the task, never widen a
budget in silence: a refused verdict is data, as precious as a green.
""",
"DOC-CEREMONY": """# DOC-CEREMONY — the ceremonies (canonical English, compact)
The ceremonies bind the artifact, never the prose:
1. The plan is frozen BEFORE any data — the sha256 recorded, the
   commit first.
2. The key genesis is AIR-GAP: your own key, on your own machine — no
   project trust anchor ships with the kit (neither the project public
   key nor reference signatures).
3. The seal is LOCAL: the fourteen sealed trees verified green before
   and after every gesture (v06/sceau_I.py verifier).
4. The journal is APPEND-ONLY: no rewrite, ever — a correction is an
   erratum appended beside the historical verbatim, byte for byte.
5. The commit passes the secret guard (the fingerprints, the entropy,
   the class patterns) — a detected secret refuses the commit by name.
6. The release deposit (the archive, the DOI) is a HUMAN command —
   never minted automatically, never without the developer's word.
7. The task order is never re-drawn; the seeds are recorded; the
   measured operands are published unrounded.
""",
"DOC-FEEDBACK": """# DOC-FEEDBACK — the adopter report (canonical English, compact)
At the end of a session: RUN the feedback tool once (the measured part
is extracted mechanically from the journaled session — never retyped;
the marginal token cost is the invocation alone). REVIEW the report
and the pre-filled issue template — the fail-closed gates have run
(required fields, secret scan, anonymization); the human review
remains. SEND IF CONSENTED (D122): the send is a human gesture, never
automatic; the tool is offline, no network call, no build dependency
(R10). The commentary (500 tokens at most) is marked UNVERIFIED at the
schema; the adopter signature is optional and is never the anchor.
""",
"CAPABILITY_PROBE": """# CAPABILITY PROBE — before you invest (canonical English, compact)
Run the probe BEFORE any investment of effort:
1. Derive the 128 constants from the mathematical definitions ALONE —
   zero divergence required against the definitions; a recitation is
   worth nothing here (the recitation rung is expected to fail).
2. Pass the notation smoke test: emit a simple block to the
   validators, read the verdict.
3. Read the frontier NAMED: a model that fails the derivation will
   fail to add — this is fail-closed advice, not gatekeeping (the 1.5B
   finding: 0 of 64 at the recitation probe). The kit names the
   frontier of the model; it never bars the door.
""",
}

# --------------------------------------------------------- LES TREIZE (FR) --
FRAGMENTS_FR = {
"AGENT-CORE": f"""# AGENT-CORE — le contrat d'agent indépendant du modèle (le miroir FR)
Le pointeur seul : le contrat d'accès vit à un pointeur, jamais un
chemin en clair ; ses quatre refus nommés (nul, hors zone, la taille,
l'alignement) nomment la cause. Une instruction par ligne ; un
opérande mémoire par instruction au plus. Les trous typés : registre /
offset / cible LBL-CST — les IDs du dictionnaire seuls, jamais un
symbole en clair. L'IAT s'appelle, jamais ne se compare. La source
étroite : movzx rax, ecx. Les constantes viennent du dictionnaire.
L'étiquette interne : LBL-001, MAJUSCULES, à la ligne seule. Les
budgets : locate 627, edit 674, add 2200 — les opérandes non arrondis
au MANIFESTE du kit. La boucle en sept étapes : observer le fragment,
lire le dictionnaire, émettre la notation, lire le verdict du juge,
lire le diff nommé, réparer la cause nommée seule, re-soumettre au
budget trois. Ne jamais jouer le juge : un mutant d'un octet est
attrapé.
""",
"QUICKSTART": f"""# QUICKSTART — une page (le miroir FR)
Prérequis : n'importe quel LLM capable, le manifeste du kit, le
fichier de contrat.
1. Courir d'abord la sonde de capacité : dériver les 128 constantes
   des seules définitions mathématiques ; un modèle qui échoue
   échouera à l'ajout — le conseil fail-closed, pas le gatekeeping.
2. Ouvrir un fragment, lire son dictionnaire, émettre la notation.
3. Lire le verdict du juge ; au refus, réparer la cause nommée seule.
4. Les budgets : locate 627 / edit 674 / add 2200 (les opérandes non
   arrondis publiés). La dégradation gracieuse : sans response_format,
   la grammaire vit au prompt et les validateurs jugent — jamais un
   juge affaibli.
5. À la fin de session : courir l'outil feedback, relire, envoyer si
   consenti.
""",
"DEVELOPER_GUIDE": f"""# GUIDE DÉVELOPPEUR — le kit au banc du développeur (le miroir FR)
Le kit développeur est bâti PAR CONSTRUCTION depuis le dépôt (D130 :
git ls-files — jamais de maintenance manuelle). Le manifeste porte un
sha256 par fichier, le vecteur de versions lie kit / protocole /
carte / profil, et la porte de compatibilité REFUSE tout triplet
incompatible (fail-closed, refus nommé).

Ce que le kit porte (le M0-en-boîte) :
- la notation et le round-trip : la chaîne d'expansion v2 au pointeur
  seul et les validateurs v3 — les juges INTACTS, jamais affaiblis ;
- les fragments de carte et l'expandeur, avec ses quatre refus nommés
  du pointeur (nul, hors zone, la taille, l'alignement) ;
- le GÉNÉRATEUR d'oracle dérivé de la couche I (jamais un oracle
  pré-dérivé expédié — la dette kit nommée), les vecteurs FIPS/RFC,
  les routes d'indépendance ;
- les portes R1-R11 (voir REFERENCE) ;
- la cérémonie de genèse de clé air-gap et le sceau LOCAL — aucune
  ancre de confiance du projet n'est expédiée (ni la clé publique du
  projet, ni les signatures de référence ; l'adopteur court sa propre
  genèse) ;
- le gabarit de journal append-only (horodatage, phase, tâche,
  verdict, tokens natifs) ;
- le guide d'agent, la ladder d'eval, le gym, l'outil feedback,
  l'outil rapport, le pipeline de triage.

La méthode : geler le plan AVANT toute donnée (le sha256 consigné, le
commit d'abord) ; mesurer et publier les opérandes non arrondis ; un
échec mesuré est une pièce aussi précieuse qu'un vert — jamais un
verdict fabriqué ; le verbatim historique demeure octet pour octet,
les corrections vivent en erratum append-only ; l'ordre des tâches
n'est jamais re-tiré, les graines sont consignées.

La régénération : courir le générateur — l'archive est déterministe
(10 rebuilds bit-identiques, les timestamps normalisés, les entrées
triées). Le dépôt Zenodo du kit demeure le geste du développeur
(BSL 1.1 au grant D209) — jamais minté sans commande.
""",
"TROUBLESHOOTING": """# DÉPANNAGE — les refus nommés et ce qu'ils veulent dire (le miroir FR)
Le protocole n'échoue jamais en silence : chaque porte refuse à un
NOM. Trouve le nom, répare la cause nommée seule.

Les notations refusées (la chaîne de juges v2 + les validateurs v3) :
- HORS-FORMAT — une ligne n'est pas une forme admise (une instruction
  à préfixe de chaîne REP, un db inline, une étiquette minuscule
  accolée à une instruction, un littéral tronqué). La réparation : le
  motif canonique — une instruction par ligne, les trous typés.
- ID-INCONNU — un ID absent du dictionnaire du bloc. La réparation :
  les IDs énumérés seuls (CST-001..NNN, LBL-001..NNN), jamais un
  symbole en clair.
- EXPANSION-DIVERGENTE — la ligne expandée a divergé (un round-trip
  en écart, une IAT jointe par une étiquette, un ID en opérande non
  expandable). La réparation : le trou typé (mov reg, CST-001 pour
  une constante ; call CST-004 pour l'IAT ; jcc LBL-001 pour un saut
  interne).
- FORME-INVALIDE — la forme émise viole le gabarit scellé.
Les quatre refus du pointeur au LOCATE (nul, hors zone, la taille,
l'alignement) sont nommés à la porte.

Le budget (3 réparations) épuisé : la tâche finit refusée — le
verdict est une pièce aussi précieuse qu'un vert ; jamais une tâche
re-tirée, jamais un budget élargi en silence.
Le linter doc refuse : une divergence numérique entre les miroirs EN
et FR, un identifiant traduit — les portes de parité.
Le scan de secrets refuse : un secret, ou la phrase de test marquée
(D105) — les copies de laboratoire portent la marque visible ; le
coffre réel n'est jamais touché au laboratoire.
La porte du kit refuse : un triplet checkpoint / kit / juges
incompatible — fail-closed, nommé.
L'agrégateur refuse : un run manquant (exit 2, jamais un verdict
partiel) ; moins de 10 strates complètes se lit NON TESTÉE (D207).
La porte kappa exige les DEUX conditions ensemble (D203) : 0,61
atteint SUR au moins 50 items double-codés.
R10 refuse au lancement (checksums, signature de manifeste,
anti-rollback, environnement) — aucun chemin dégradé n'existe.
Sans response_format à l'endpoint : la grammaire vit au prompt et les
validateurs jugent — jamais un juge affaibli (la dégradation
gracieuse).
""",
"SECURITY": """# SÉCURITÉ — le modèle en une page (le miroir FR)
Les secrets : jamais committés — la garde pre-commit combine les
empreintes sha256 des secrets connus, l'entropie de Shannon (3,8
bits/car sur les assignations de 28 caractères ou plus) et les motifs
de classe (ghp_ / GOCSPX- / PEM / refresh). La porte de scrub est
fail-closed au contrôle négatif vécu : un secret planté DOIT être
attrapé.

Les ancres : AUCUNE ancre de confiance du projet n'est expédiée avec
le kit — ni la clé publique du projet, ni les signatures de
référence. L'adopteur court sa propre genèse de clé air-gap ; le
sceau est LOCAL.

Le coffre réel n'est jamais touché au laboratoire (D105) : les copies
de laboratoire portent une phrase de test marquée visible ; un
rapport qui en porte une est REFUSÉ à la porte.

La discipline d'accès : le pointeur seul (jamais un chemin en clair) ;
les quatre refus nommés du pointeur (nul, hors zone, la taille,
l'alignement) ; une instruction par ligne ; un opérande mémoire par
instruction au plus.

Les rapports adopteurs : anonymisés mécaniquement (chemins,
usernames), le scan de secrets à la porte, le schéma gelé par sha256
AVANT tout rapport ; le commentary (500 tokens au plus) est marqué
NON VÉRIFIÉ ; l'envoi est un geste humain (D122) — jamais automatique,
l'outil est offline.

Le double usage : les binaires intercepteurs et le matériau dual-use
sont exclus du sous-ensemble permissif ; les tâches synthétiques
Apache-2.0/CC-BY demeurent séparées du corpus BSL à chaque split.

La licence : BSL 1.1 au grant D209 ; les digests publics sous
CC-BY-4.0 (les contributeurs acknowledged opt-in).

Offline par construction : aucune dépendance réseau au build (R10) ;
l'outillage court en air-gap.
""",
"REFERENCE": f"""# RÉFÉRENCE — le protocole en une page (le miroir FR)
Trois couches indissociables : I (les spécifications signées), C (la
carte chiffrée), B (l'artefact verrouillé aux octets). Les priorités
lexicographiques : sécurité > performance > optimisation > coût en
tokens.

La notation : une instruction par ligne ; les trous typés (registre /
offset / cible LBL-CST) ; les IDs du dictionnaire seuls — CST-001..NNN
pour les constantes et les entrées IAT (l'IAT s'appelle : call
CST-004), LBL-001..NNN pour les étiquettes internes (MAJUSCULES, à la
ligne seule) ; la source étroite (movzx rax, ecx) ; un opérande
mémoire par instruction au plus.

Les juges : la chaîne d'expansion v2 au pointeur seul, les
validateurs v3, le round-trip (ce que tu écris est ce qui s'expand est
ce qui revient). Un mutant d'un octet est attrapé — ne jamais jouer
le juge.

Les budgets (les opérandes non arrondies au manifeste du kit) :
locate {B['loc']} / edit {B['edit']} / add {B['add']} ; le budget de
réparation est 3.

Les portes R1-R11 :
{TABLE_REGLES_FR}

Les classes de refus : HORS-FORMAT, ID-INCONNU, EXPANSION-DIVERGENTE,
FORME-INVALIDE (la notation) ; HUNK-INCONNU, CONTEXTE-DIVERGENT,
ROUND-TRIP-DIVERGENT (l'édition) ; POINTEUR-INCONNU,
EMPREINTE-DIVERGENTE (le pointeur). Réparer la cause nommée seule.

Les 18 blocs du banc (les notations scellées du dépôt) :
{BLOCS_EN}

Les cérémonies : la genèse de clé air-gap, le sceau LOCAL, le journal
append-only (les corrections sont des errata, jamais des réécritures),
la garde de secrets au commit, le dépôt de release à la commande
humaine.

Les décisions citées en littéral (jamais traduites) : D81 (la garde
durable), D105 (la phrase de test marquée), D122 (l'envoi humain),
D130 (le kit par construction), D203 (la grille kappa), D207 (les
règles d'arrêt), D209 (le grant), D250 (l'arbitrage au développeur).
""",
"DOC-LOC": f"""# DOC-LOC — l'opération LOCATE (le miroir FR, compact)
Le pointeur seul est le contrat d'accès : jamais un chemin en clair,
jamais un offset deviné. Observe le fragment, lis le dictionnaire,
émets la forme au pointeur ; la porte nomme ses quatre refus — nul,
hors zone, la taille, l'alignement — et tu répare la cause nommée
seule, le reste octet pour octet. Le fragment scellé est la
référence ; l'expandeur n'admet que ce que le dictionnaire admet. Le
budget : {B['loc']} (hiérarchique — l'opérande non arrondi vit au
manifeste du kit) ; le budget de réparation est 3 ; au quatrième
refus la tâche finit refusée — une pièce aussi précieuse qu'un vert.
Ne jamais jouer le juge : un mutant d'un octet est attrapé à la
batterie de mutation. La boucle en sept étapes : observer le fragment,
lire le dictionnaire, émettre la notation, lire le verdict du juge,
lire le diff nommé, réparer la cause nommée seule, re-soumettre.
""",
"DOC-EDIT": f"""# DOC-EDIT — l'opération EDIT (le miroir FR, compact)
L'édition vit au gabarit scellé TPL-EDIT-v1 : émets les hunks, jamais
une réécriture en texte libre. Les quatre refus d'édition sont nommés
— HORS-FORMAT (la forme du hunk viole le gabarit), HUNK-INCONNU (le
hunk ne s'applique pas à son ancre), CONTEXTE-DIVERGENT (les octets
environnants ont bougé), ROUND-TRIP-DIVERGENT (ce que tu as écrit ne
revient pas) — répare la cause nommée seule, chaque ligne intacte
octet pour octet. Le patch honore le contrat publié (R4) : même
signature, mêmes pré et post-conditions, les appelants jamais
invalidés. Aucun commit sans l'oracle, les vecteurs dorés et le
round-trip (R5). Le budget : {B['edit']} (non arrondi au manifeste) ;
le budget de réparation est 3. La référence est la notation scellée
du bloc — jamais une récitation du voisin, l'exemplaire est une
référence, pas un raccourci.
""",
"DOC-ADD": f"""# DOC-ADD — l'opération ADD (le miroir FR, compact)
L'ajout vit au squelette SQUELETTE-v2 : le cadre ABI et les trous
typés sont donnés ; tu n'émets que les lignes de LOGIQUE. Une
instruction par ligne ; un opérande mémoire par instruction au plus ;
les trous typés seuls (registre / offset / cible LBL-CST) ; les IDs du
dictionnaire — CST-001..NNN pour les constantes et les entrées IAT
(l'IAT s'appelle : call CST-004), LBL-001..NNN pour les étiquettes
internes, MAJUSCULES, à la ligne seule ; la source étroite (movzx
rax, ecx) ; aucune donnée inline (la donnée vit au cadre) ; aucune
instruction à préfixe de chaîne REP. Le budget : {B['add']} (non
arrondi au manifeste) ; le budget de réparation est 3. Au refus, lis
le diff nommé, répare la cause nommée seule, re-soumets — les juges
sont intacts, un juge affaibli est un gain perdu. La forme canonique
est attendue de toi à la première émission : le normalisateur ne
répare JAMAIS une forme interdite.
""",
"DOC-REFUS": """# DOC-REFUS — la grammaire des refus (le miroir FR, compact)
Chaque refus porte une classe NOMMÉE — la classe est une constante du
protocole, jamais traduite : HORS-FORMAT, ID-INCONNU,
EXPANSION-DIVERGENTE, FORME-INVALIDE ; au pointeur : nul, hors zone,
la taille, l'alignement ; à l'édition : HUNK-INCONNU,
CONTEXTE-DIVERGENT, ROUND-TRIP-DIVERGENT. La boucle au refus : lis la
classe, lis la cause nommée, répare LA CAUSE NOMMÉE SEULE — chaque
autre ligne demeure octet pour octet — re-soumets au budget de
réparation 3. Ne jamais moyenner un refus, jamais re-tirer la tâche,
jamais élargir un budget en silence : un verdict refusé est une
donnée, aussi précieuse qu'un vert.
""",
"DOC-CEREMONY": """# DOC-CEREMONY — les cérémonies (le miroir FR, compact)
Les cérémonies lient l'artefact, jamais la prose :
1. Le plan est gelé AVANT toute donnée — le sha256 consigné, le
   commit d'abord.
2. La genèse de clé est AIR-GAP : ta propre clé, sur ta propre
   machine — aucune ancre de confiance du projet n'est expédiée avec
   le kit (ni la clé publique du projet, ni les signatures de
   référence).
3. Le sceau est LOCAL : les quatorze arbres scellés vérifiés verts
   avant et après chaque geste (v06/sceau_I.py verifier).
4. Le journal est APPEND-ONLY : aucune réécriture, jamais — une
   correction est un erratum appendu à côté du verbatim historique,
   octet pour octet.
5. Le commit passe la garde de secrets (les empreintes, l'entropie,
   les motifs de classe) — un secret détecté refuse le commit au nom.
6. Le dépôt de release (l'archive, le DOI) est une COMMANDE HUMAINE —
   jamais minté automatiquement, jamais sans la parole du
   développeur.
7. L'ordre des tâches n'est jamais re-tiré ; les graines sont
   consignées ; les opérandes mesurées sont publiées non arrondies.
""",
"DOC-FEEDBACK": """# DOC-FEEDBACK — le rapport adopteur (le miroir FR, compact)
À la fin d'une session : COURS l'outil feedback une fois (la part
measured est EXTRAITE MÉCANIQUEMENT de la session déjà consignée au
journal — jamais retapée ; le coût token marginal est l'invocation
seule). RELIS le rapport et le gabarit d'issue pré-rempli — les
portes fail-closed ont couru (champs requis, scan de secrets,
anonymisation) ; la relecture humaine demeure. ENVOIE SI CONSENTI
(D122) : l'envoi est un geste humain, jamais automatique ; l'outil
est offline, aucun appel réseau, aucune dépendance au build (R10). Le
commentary (500 tokens au plus) est marqué NON VÉRIFIÉ au schéma ; la
signature adopteur est optionnelle et n'est jamais l'ancre.
""",
"CAPABILITY_PROBE": """# CAPABILITY PROBE — avant d'investir (le miroir FR, compact)
Cours la sonde AVANT tout investissement d'effort :
1. Dérive les 128 constantes des définitions mathématiques SEULES —
   zéro divergence exigée contre les définitions ; une récitation ne
   vaut rien ici (le rung récitation est attendu en échec).
2. Passe le smoke test de notation : émets un bloc simple aux
   validateurs, lis le verdict.
3. Lis la frontière NOMMÉE : un modèle qui échoue la dérivation
   échouera à l'ajout — c'est le conseil fail-closed, pas le
   gatekeeping (le finding du 1.5B : 0 sur 64 à la sonde de
   récitation). Le kit nomme la frontière du modèle ; il ne barre
   jamais la porte.
""",
}

ORDRE = ["AGENT-CORE", "QUICKSTART", "DEVELOPER_GUIDE", "TROUBLESHOOTING",
         "SECURITY", "REFERENCE", "DOC-LOC", "DOC-EDIT", "DOC-ADD",
         "DOC-REFUS", "DOC-CEREMONY", "DOC-FEEDBACK", "CAPABILITY_PROBE"]
CIBLE_PAR_FRAG = {
    "AGENT-CORE": CIBLES["CORE"],
    "QUICKSTART": CIBLES["OPERATIONS"],      # la cible d'une page : ≤800
    "DOC-LOC": CIBLES["OPERATIONS"],
    "DOC-EDIT": CIBLES["OPERATIONS"],
    "DOC-ADD": CIBLES["OPERATIONS"],
    "DOC-REFUS": CIBLES["REFUS"],
    "DOC-CEREMONY": CIBLES["CEREMONY"],
    "DOC-FEEDBACK": CIBLES["FEEDBACK"],
    "CAPABILITY_PROBE": CIBLES["PROBE"],
}


def mesurer(texte: str, tok) -> int:
    """L'OPÉRANDE NON ARRONDI au tokenizer natif (cl100k_base — le
    canon du relevé AGENT-CORE 216 / QUICKSTART 167)."""
    return len(tok.encode(texte))


def main() -> int:
    tok = tiktoken.get_encoding("cl100k_base")
    EN.mkdir(exist_ok=True)
    FR.mkdir(exist_ok=True)
    registres = ICI / "registres"
    registres.mkdir(exist_ok=True)

    # (1) l'assertion de parité des canaux AVANT l'écriture : les deux
    #     miroirs portent les m^emes clés
    assert set(FRAGMENTS_EN) == set(FRAGMENTS_FR) == set(ORDRE), \
        "les miroirs EN/FR doivent porter les treize canaux"

    budgets = {}
    manifeste = ["# MANIFESTE DES FRAGMENTS — m8qc10sxg (le geste suivant)",
                 "# le tokenizer natif cl100k_base ; les opérandes NON "
                 "ARRONDIS ; les cibles du plan gelé",
                 "# sha256 par fichier — EN à fragments/, FR à fragments-fr/"]
    for nom in ORDRE:
        texte_en = FRAGMENTS_EN[nom]
        texte_fr = FRAGMENTS_FR[nom]
        (EN / f"{nom}.md").write_text(texte_en, encoding="utf-8")
        (FR / f"{nom}.md").write_text(texte_fr, encoding="utf-8")
        n_en = mesurer(texte_en, tok)
        n_fr = mesurer(texte_fr, tok)
        cible = CIBLE_PAR_FRAG.get(nom)
        entry = {"tokens_en": n_en, "tokens_fr": n_fr}
        if cible is not None:
            entry["cible"] = cible
            entry["verdict"] = ("VERT" if n_en <= cible and n_fr <= cible
                                else f"REFUS (hors budget : {nom})")
        budgets[nom] = entry
        manifeste.append(
            f"{nom}.md | EN {n_en} tokens / FR {n_fr} tokens"
            + (f" | cible <= {cible} | {entry.get('verdict', '(humain : aucune cible nommée)')}"
               if cible is not None else " | (audience humaine : aucune cible nommée)")
            + f" | sha256-en {hashlib.sha256(texte_en.encode()).hexdigest()}"
            + f" | sha256-fr {hashlib.sha256(texte_fr.encode()).hexdigest()}")
    (registres / "budgets-complet.json").write_text(
        json.dumps(budgets, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    manifeste.append("")
    manifeste.append("# les canons : les budgets parsés du GUIDE-AGENT "
                     f"(locate {B['loc']} / edit {B['edit']} / add "
                     f"{B['add']}), les règles {REGLES[0]}-{REGLES[-1]} "
                     "parsées du protocole, les 18 blocs du dépôt, les "
                     "cibles du PLAN-M8QC10SXG gelé — jamais retapés")
    (ICI / "MANIFESTE-fragments.txt").write_text(
        "\n".join(manifeste) + "\n", encoding="utf-8")

    hors = [n for n, e in budgets.items()
            if e.get("verdict", "").startswith("REFUS")]
    print("[generer_fragments] 13 canaux x 2 miroirs écrits ;",
          f"fragments hors budget : {hors if hors else 'AUCUN'}")
    for nom in ORDRE:
        e = budgets[nom]
        print(f"  {nom:16s} EN {e['tokens_en']:5d} | FR {e['tokens_fr']:5d}"
              + (f" | cible {e['cible']}" if "cible" in e else ""))
    return 1 if hors else 0


if __name__ == "__main__":
    raise SystemExit(main())
