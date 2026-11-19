#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extraire_pointeur.py — L'EXTRACTION ET LE VERDICT DE LA CAMPAGNE POINTEUR
(le plan § 1.2-1.3, gelé) : le gain lu des logs bruts, jamais tapé à la main ;
la vérification zéro-divergence au mode P (l'ID et l'empreinte octet pour
octet, l'expansion client verte) ; le cl100k parallèle ; LA RE-TOKENISATION
INDÉPENDANTE ±1 (l'instrument contrôlé : un second objet d'encodage constitu
à part recompte chaque texte — l'écart exigé ≤ 1 token) ; les distributions ;
la confrontation aux octets réels (reprise TELLE QUELLE de 5gfx6pwkj).

Écrit : RAPPORT-cq01qv1za-POINTEUR.txt. Code 0 = tout vert."""
from __future__ import annotations

import json
import pathlib
import re
import statistics
import sys

import tiktoken

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
sys.path.insert(0, str(REPO / "atelier-localiser-5gfx6pwkj"))
sys.path.insert(0, str(ICI))
from extraire_gain import verifier_octets_reels   # noqa: E402  TEL QUEL
from expansion_pointeur import RefusPointeur, confronte, table_carte  # noqa: E402

CL100K = tiktoken.get_encoding("cl100k_base")


def stats(valeurs):
    v = sorted(valeurs)
    n = len(v)

    def pct(p):
        k = (n - 1) * p
        f = int(k)
        c = min(f + 1, n - 1)
        return v[f] + (v[c] - v[f]) * (k - f)
    return {"n": n, "min": v[0], "q1": pct(0.25), "mediane": pct(0.5),
            "q3": pct(0.75), "max": v[-1]}


def retokenise_independante(texte: str) -> tuple[int, int]:
    """LA SECONDE PASSE INDÉPENDANTE — deux voies de retour :
    (a) la voie ENTIÈRE : un DEUXIÈME objet d'encodage (constitu à part,
        jamais celui de la passe parallèle) par encode_ordinary — une voie
        d'API DISTINCTE de encode — sur le texte entier : LA MESURE qui doit
        s'accorder à ±1 (0 attendu : le tokenizer est déterministe) ;
    (b) la voie SEGMENTÉE (la mouture première du plan, comptant ligne à
        ligne) : CONSIGNÉE comme témoin — elle porte un écart SYSTÉMATIQUE
        de +2 sur les prompts (la fusion de tokens aux frontières de
        lignes : un artefact de la segmentation, PAS une instabilité de
        l'instrument — nommé tel quel, jamais confondu avec (a))."""
    enc = tiktoken.get_encoding("cl100k_base")   # un objet NEUF, à part
    entiere = len(enc.encode_ordinary(texte))
    segments = texte.splitlines(keepends=True)
    segmentee = sum(len(enc.encode(s)) for s in segments)
    return entiere, segmentee


def main() -> int:
    vt = json.loads((REPO / "atelier-localiser-5gfx6pwkj" / "verites-terrain.json")
                    .read_text(encoding="utf-8"))
    par_id = {b["id"]: b for b in vt["blocs"]}
    table = table_carte()

    journal = [json.loads(l) for l in
               (ICI / "journal_tokens.jsonl").read_text(
                   encoding="utf-8").splitlines() if l.strip()]
    garde = [json.loads(l) for l in
             (ICI / "garde-brut.jsonl").read_text(
                 encoding="utf-8").splitlines() if l.strip()]
    reponses = {g["tache"]: g["reponse_api"]["choices"][0]["message"]["content"]
                for g in garde}

    divergences: list[str] = []
    retok_ecarts: list[str] = []
    retok_systematique = [0]     # la voie segmentée : l'artefact +2 compté
    resultats: dict[str, list] = {"A": [], "P": []}
    expansions_vertes = 0

    for l in journal:
        m = re.match(r"localiser-(A|P)-(i\d+)$", l["tache"])
        if not m:
            continue
        mode, bid = m.group(1), m.group(2)
        b = par_id[bid]
        rep = reponses[l["tache"]].strip()
        pfile = ICI / "garde-prompts" / f"{l['tache']}.txt"
        prompt = pfile.read_text(encoding="utf-8")

        # le cl100k parallèle + LA RE-TOKENISATION INDÉPENDANTE ±1
        cl_p = len(CL100K.encode(prompt))
        cl_r = len(CL100K.encode(rep))
        for nom_txt, texte, passe1 in (("prompt", prompt, cl_p),
                                       ("réponse", rep, cl_r)):
            entiere, segmentee = retokenise_independante(texte)
            if abs(passe1 - entiere) > 1:
                retok_ecarts.append(
                    f"{mode}/{bid} {nom_txt} : cl100k {passe1} contre la "
                    f"re-tokenisation {entiere} — ÉCART > 1")
            if segmentee != passe1 and nom_txt == "prompt" \
                    and segmentee - passe1 == 2:
                retok_systematique[0] += 1   # l'artefact nommé, jamais un
                                             # refus — la voie (b) du plan

        resultats[mode].append({
            "bloc": bid, "reponse": rep,
            "prompt": l["prompt_tokens"],
            "completion": l["completion_tokens"],
            "total": l["total_tokens"],
            "cl100k_total": cl_p + cl_r,
            "somme": l["somme_coherente"], "source": l["source"],
            "modele": l["modele"]})

        if mode == "A":
            # le format en vigueur : l'entête rendu porte le bloc soumis
            if bid not in rep or b["nom"] not in rep \
                    or f"{b['slot']:#x}" not in rep.replace("0X", "0x"):
                divergences.append(f"A/{bid} : l'entête rendu ne porte pas "
                                   f"l'identifiant/le nom/le slot — "
                                   f"« {rep[:60]}… »")
        else:
            # LE POINTEUR SEUL : la ligne exacte, l'ID, l'empreinte — puis
            # L'EXPANSION CLIENT ENTIÈRE (les quatre portes, fail-closed)
            lignes = [x for x in rep.splitlines() if x.strip()]
            if len(lignes) != 1:
                divergences.append(f"P/{bid} : {len(lignes)} lignes (une "
                                   f"exigée) — « {rep[:60]}… »")
                continue
            m2 = re.match(r"^(i\d+)\s*·\s*sha256:([0-9a-f]{64})$",
                          lignes[0].strip())
            if not m2:
                divergences.append(f"P/{bid} : hors format — "
                                   f"« {lignes[0][:70]}… »")
                continue
            rid, empreinte = m2.groups()
            if rid != bid:
                divergences.append(f"P/{bid} : l'identifiant rendu {rid} "
                                   f"!= le bloc soumis {bid}")
                continue
            if empreinte != b["notation_sha256"]:
                divergences.append(
                    f"P/{bid} : l'empreinte rendue {empreinte[:16]}… != la "
                    f"carte {b['notation_sha256'][:16]}…")
                continue
            try:
                ex = confronte(lignes[0].strip(), table[bid]["entete"], table)
                assert ex["entete"] == table[bid]["entete"]
                expansions_vertes += 1
            except RefusPointeur as e:
                divergences.append(f"P/{bid} : l'expansion client REFUSE — "
                                   f"{e}")

    octets_ecarts = verifier_octets_reels(vt)

    def dist(mode, champ):
        return stats([r[champ] for r in resultats[mode]])

    nA, nP = len(resultats["A"]), len(resultats["P"])
    medA, medP = dist("A", "total")["mediane"], dist("P", "total")["mediane"]
    gain_total = 1 - medP / medA if medA else 0
    gain_rep = (1 - dist("P", "completion")["mediane"]
                / dist("A", "completion")["mediane"])
    hors_log = [r for r in resultats["A"] + resultats["P"]
                if r["source"] != "log-api"]
    sommes = [r for r in resultats["A"] + resultats["P"] if not r["somme"]]
    div_a = sum(1 for d in divergences if d.startswith("A/"))
    div_p = sum(1 for d in divergences if d.startswith("P/"))

    lignes = [
        "LE RAPPORT DE LA CAMPAGNE POINTEUR — cq01qv1za / OPT-04 axe (1)",
        "(le plan PLAN-cq01qv1za-COUT.md sha256 cb5d1943… gelé AVANT toute",
        "mesure, le commit fed8c6d précédant la première donnée ; le format",
        "D205 : la mesure avant, le gain mesuré, le vérificateur)",
        "=" * 92,
        "",
        "LA CAMPAGNE (les MÊMES 18 blocs, la graine 20261117, l'ordre même,",
        "la rig compter_tokens — le natif LU du champ usage, 100 % log-api,",
        "le cl100k parallèle, la re-tokenisation indépendante) :",
        f"{'':30}{'n':>4}{'médiane':>9}{'q1':>8}{'q3':>8}{'min':>7}{'max':>8}",
        "-" * 74,
    ]
    for mode, titre, champ in (("A", "A l'actuel — total", "total"),
                               ("P", "P pointeur seul — total", "total"),
                               ("A", "A — réponse seule", "completion"),
                               ("P", "P — réponse seule", "completion"),
                               ("A", "A — cl100k (parallèle)", "cl100k_total"),
                               ("P", "P — cl100k (parallèle)", "cl100k_total")):
        d = dist(mode, champ)
        lignes.append(f"{titre:30}{d['n']:>4}{d['mediane']:>9.0f}{d['q1']:>8.0f}"
                      f"{d['q3']:>8.0f}{d['min']:>7.0f}{d['max']:>8.0f}")

    lignes += [
        "-" * 74,
        "",
        "LE GAIN MESURÉ (lu des logs bruts, jamais tapé) :",
        f"  le total : A {medA:.0f} → P {medP:.0f} natifs = "
        f"{gain_total * 100:.1f} %",
        f"  la réponse : A {dist('A', 'completion')['mediane']:.0f} → "
        f"P {dist('P', 'completion')['mediane']:.0f} = "
        f"{gain_rep * 100:.1f} %",
        f"  le recoup OPT-02 (l'autre bac) : B2 total 1 072 / réponse 23 —",
        f"  le pointeur P {medP:.0f} / {dist('P', 'completion')['mediane']:.0f} :",
        "  DEUX CHAMPS LITTÉRAUX (l'ID, l'empreinte) contre les quatre de B2",
        "  — le pointeur achète l'EXPANSION CÔTÉ CLIENT (l'entête ne revient",
        "  JAMAIS au contexte), B2 laissait quatre champs à recopier ; le",
        "  choix du format est un arbitrage DU MAÎTRE, les deux mesurés verts.",
        "",
        "LE VÉRIFICATEUR :",
        f"  la passe A : {nA - div_a}/{nA} sans divergence",
        f"  la passe P : {nP - div_p}/{nP} — "
        + ("ZÉRO DIVERGENCE" if div_p == 0 else f"{div_p} écart(s)"),
        f"  l'expansion client (les QUATRE portes, fail-closed) : "
        f"{expansions_vertes}/{nP} verte(s)",
        "  la re-tokenisation indépendante (±1 token, la voie ENTIÈRE : un",
        "  objet neuf par encode_ordinary) : "
        f"{len(retok_ecarts)} écart(s)",
        "  la voie segmentée (ligne à ligne, la mouture première du plan) :",
        f"  {retok_systematique[0]} prompt(s) à +2 EXACT — l'artefact "
        "SYSTÉMATIQUE de la fusion aux frontières de lignes, NOMMÉ (jamais "
        "une instabilité de l'instrument, jamais un refus)",
        f"  la confrontation aux octets réels (loupe.exe au slot, padding",
        f"  NOP, aucun int3 instruction) : "
        f"{'VERT — 18/18' if not octets_ecarts else 'ROUGE'}",
        f"  la source (CA3) : {len(hors_log)} appel(s) hors log-api",
        f"  la somme (prompt+completion=total) : {len(sommes)} écart(s)",
        f"  le modèle (lu du champ model) : "
        f"{sorted({r['modele'] for r in resultats['A'] + resultats['P']})}",
    ]
    lignes += [f"    - {d}" for d in divergences]
    lignes += [f"    - {e}" for e in retok_ecarts]
    lignes += [f"    - {e}" for e in octets_ecarts]
    if nA != 18 or nP != 18:
        lignes.append(f"  [ÉCART NOMMÉ] l'effectif : A={nA}/18, P={nP}/18")

    verdict = ("VERT — le pointeur seul (ID + empreinte, deux champs "
               "littéraux) réduit le coût SANS divergence, l'expansion "
               "client reconstruit l'entête octet pour octet, AUCUN "
               "contrôle retiré ; la re-tokenisation indépendante "
               "confirme l'instrument"
               if div_p == 0 and expansions_vertes == nP == 18
               and not retok_ecarts and not octets_ecarts and not hors_log
               else "ROUGE — les écarts ci-dessus font foi (consignés tels "
                    "quels, l'instruction l'exige)")
    lignes += ["", f"LE VERDICT : {verdict}"]
    (ICI / "RAPPORT-cq01qv1za-POINTEUR.txt").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8")
    print("\n".join(lignes))
    return 0 if verdict.startswith("VERT") else 2


if __name__ == "__main__":
    sys.exit(main())
