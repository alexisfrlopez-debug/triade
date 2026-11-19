#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_main_v194.py — l'édition v0.19.4 du manuscrit (née de
edition-v0193 par copie) : LE COÛT DE LA BOUCLE SOUS R11 (l'instruction
cq01qv1za, la vague du 18/11, la quatrième) — le pointeur seul adopté au
localiser, la pile mémo v2 + double moteur, H5 DEVENUE TENUE PAR
L'INSTRUCTION DU MAÎTRE. AUCUNE valeur mesurée modifiée — l'amendement
H5 s'AJOUTE au verdict falsifié de D204 (les deux demeurent, étiquetés).
Chaque remplacement EST ANCRÉ — REFUS si une ancre manque."""
import pathlib
import shutil

SRC = pathlib.Path(__file__).resolve().parents[1] / "edition-v0193"
ICI = pathlib.Path(__file__).resolve().parent
shutil.copy2(SRC / "main.tex", ICI / "main.tex")
shutil.copy2(SRC / "refs.bib", ICI / "refs.bib")
shutil.copytree(SRC / "donnees", ICI / "donnees", dirs_exist_ok=True)
M = (ICI / "main.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(texte, ancien, nouveau, nom):
    if ancien not in texte:
        raise SystemExit(f"[v0194] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- 1. l'en-tête du fichier ---------------------------------------------
M = remplace(
    M,
    """%  TRIADE — édition académique v0.19.3 (manuscrit IMRAD, anglais)
%  L'édition v0.19.3 est L'ÉDITION DE L'ÉCART FERMÉ (l'instruction""",
    """%  TRIADE — édition académique v0.19.4 (manuscrit IMRAD, anglais)
%  L'édition v0.19.4 est L'ÉDITION DU COÛT DE LA BOUCLE (l'instruction
%  cq01qv1za, la vague du 18/11, la quatrième) née de la v0.19.3 (l'écart
%  fermé) : le POINTEUR SEUL adopté au format de réponse de localiser
%  (OPT-04 : −35,7 % au total, −93,3 % à la réponse, zéro divergence
%  18/18, l'expansion côté client à quatre refus nommés), la pile
%  MÉMO V2 + DOUBLE MOTEUR adoptée au chemin de vérification (la clé
%  étendue fichier + config émulateur + graine, l'audit 1 run sur 10 à
%  compteur chaîné, QEMU-user au volume et Unicorn à l'échantillon
%  consigné, divergence 0 sur 2 041 opérations), H5 DEVENUE TENUE PAR
%  L'INSTRUCTION DU MAÎTRE (le ratio de régime 3,0× sous le seuil ×10,
%  l'énoncé explicite de l'instruction). AUCUNE valeur mesurée modifiée.
%  L'édition v0.19.3 est L'ÉDITION DE L'ÉCART FERMÉ (l'instruction""",
    "l'en-tête du fichier (v0.19.4)")

# ---- 2. la ligne de date : la clause v0.19.4 s'ajoute ---------------------
M = remplace(
    M,
    "no measured value of the sealed v0.18.1 edition modified)}",
    "no measured value of the sealed v0.18.1 edition modified); this "
    "v0.19.4 is the loop-cost edition (the cq01qv1za instruction): the "
    "pointer-only localiser response adopted (OPT-04: total $-35.7\\%$, "
    "response $-93.3\\%$, zero divergence 18/18, the client-side expansion "
    "behind four named refusals), the memo-v2 + dual-engine stack adopted "
    "on the verification path (the key extended to file + emulator "
    "configuration + seed, the chained run counter auditing one run in "
    "ten, QEMU-user for volume and Unicorn for the consigned audit "
    "sample, divergence zero over 2{,}041 operations, consoles "
    "line-identical to the originals), and H5 held by the developer's "
    "explicit instruction (the regime ratio $3.0\\times$ under the "
    "$\\times$10 threshold, consigned as the master's amendment of the "
    "mof9q10vq rule --- the D204 falsification stands as measured and "
    "dated; no measured value modified)}",
    "la ligne de date (la clause v0.19.4)")

# ---- 3. LE VERDICT H5 : l'amendement de l'instruction s'AJOUTE ------------
M = remplace(
    M,
    """\\textbf{H5} (verification time within one
order of magnitude) \\emph{falsified} --- 52.5\\,s against 2.2\\,s
($\\times$23.9). The label disambiguation stands:""",
    """\\textbf{H5} (verification time within one
order of magnitude) \\emph{falsified} --- 52.5\\,s against 2.2\\,s
($\\times$23.9); \\emph{held as of v0.19.4 by the developer's explicit
instruction} --- the OPT-04 stack (memo v2, dual engine) measured the
regime at 6.8\\,s against the C arm's 2.2\\,s on the same machine
($\\times$3.0, under the threshold; $n{=}5$ per configuration, monotonic
clock, the fixed command lists unchanged, every oracle console
line-identical to the originals, the audit re-execution green at zero
field-level divergence) --- the falsification of D204 stands as measured
and dated, the rehabilitation is the master's named amendment of the
mof9q10vq rule (the terrain run to come will confirm, the status table
carries the status as measured and sourced). The label disambiguation
stands:""",
    "le verdict H5 (l'amendement v0.19.4)")

# ---- 4. le RQ2 : la phrase du pointeur seul (la section française) --------
M = remplace(
    M,
    """naïve de 300~304 ; l'unique unité à deux
bras entièrement instrumentée de la campagne lit 53~158 tokens pour le""",
    """naïve de 300~304 ; l'édition v0.19.4 adopte le POINTEUR SEUL au
format de réponse de localiser (OPT-04 : l'agent rend l'identifiant
d'entrée et l'empreinte de la notation — deux champs littéraux, jamais un
calcul — le client expande le pointeur auprès de la carte et confronte,
quatre refus nommés fail-closed ; la mesure à la même graine sur 18
appels réels au tokenizer natif : le total 1~714 → 1~103 natifs
(−35,7 %), la réponse 770 → 52 (−93,3 %), zéro divergence, la
re-tokenisation indépendante confirmant l'instrument à ±1 token) ;
l'unique unité à deux
bras entièrement instrumentée de la campagne lit 53~158 tokens pour le""",
    "le RQ2 (la phrase du pointeur seul)")

# ---- 5. la pile adoptée : le paragraphe après l'amendement H5 -------------
M = remplace(
    M,
    """the terrain run to come will confirm, the status table
carries the status as measured and sourced). The label disambiguation
stands:""",
    """the terrain run to come will confirm, the status table
carries the status as measured and sourced).

\\paragraph{The v0.19.4 loop-cost stack.} The verification path itself
was the last hot path the protocol could attack without touching a
single control: the sealed session-opening (the md5+sha256 of a whole
file under emulation) dominated the M4 list ($\\sim$10\\,s for
196\\,KiB under the instrumented Unicorn harness --- a per-instruction
hook). The adopted stack: a \\emph{sealed memo v2} whose key is the
sha-256 of everything that determines the result (the assembled block,
the entry, the contract) plus the emulator configuration and the
campaign seed (the instruction's terms --- one byte changed anywhere is
a miss, the session runs live); a \\emph{dual engine} --- a static ELF
launcher executing the same sealed bytes at the same plan addresses
under QEMU-user for volume (the image built by the real Unicorn harness,
byte-identical by construction), Unicorn kept as the reference for the
consigned audit sample (divergence zero, octet for octet, over the
2{,}041-operation sample; a deliberately mutated launcher shim is
caught at the first line --- the gate divides honest engines from false
ones); and a \\emph{chained run counter} in the memo's signed heart
auditing one oracle run in ten (the tenth seal fired the audit by
itself mid-measurement: the live re-execution under Unicorn, the stored
relev\\'e confronted field by field, zero divergence, its price named
in the distribution). No seed removed, no vector reduced, no
verification withdrawn --- the proof is that all twenty-four captured
oracle consoles are line-identical to the originals, and the sealed
pieces' fingerprints are intact before and after every run.""",
    "le paragraphe de la pile adoptée (v0.19.4)")

(ICI / "main.tex").write_text(M, encoding="utf-8")
print("[v0194] les ancrages posés :", " ; ".join(FAITS))
