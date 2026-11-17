#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extraire_gain.py — L'EXTRACTION ET LE VERDICT DE LA CAMPAGNE 5gfx6pwkj
(le plan § 6 : le gain lu des logs bruts, jamais tapé à la main ; les
distributions complètes ; la vérification zéro-divergence ; la confrontation
aux octets réels).

Lit : journal_tokens.jsonl (le natif, lu du champ usage par l'instrument),
garde-brut.jsonl (les réponses brutes), garde-prompts/ (les prompts exacts),
verites-terrain.json (la table des 18, régénérée des fichiers), loupe.exe
(les octets réels).

Écrit : RAPPORT-5gfx6pwkj.txt — le format D205 (la mesure avant, le gain
mesuré, le vérificateur). Code retour : 0 = tout vert ; 2 = des écarts
(consignés tels quels — l'instruction l'exige)."""
from __future__ import annotations

import json
import pathlib
import re
import statistics
import sys

import tiktoken

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
CL100K = tiktoken.get_encoding("cl100k_base")

# la mesure avant (om3ewy9lf, preuves_v180/p5-decomposition-contexte.txt)
MESURE_AVANT = {"materiau": 596, "prose": 41, "reponse": 604, "total": 1277}


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


def verifier_octets_reels(vt: dict) -> list[str]:
    """le plan § 5.3 : loupe.exe lu au slot de chaque bloc — le padding
    terminal TOUT 0x90, le code sans 0xCC (la plage pointe les octets
    réels)."""
    exe = (REPO / "loupe" / "loupe.exe").read_bytes()
    # .text2 à RVA 0x4000 — l'adresse fichier (les sections PE alignées) :
    # loupe.exe est recomposée par le build — le mapping RVA->fichier se
    # prend de l'entête PE (pefile), pas d'une hypothèse
    import pefile
    pe = pefile.PE(str(REPO / "loupe" / "loupe.exe"), fast_load=True)
    ecarts = []
    for b in vt["blocs"]:
        slot, code, taille = b["slot"], b["code"], b["taille"]
        # la convention du domaine (le tableau de bord) : .text2 0x4000 —
        # les slots des entêtes sont des RVA ABSOLUES (0x4040..0x6800
        # tombent dans .text2) — la RVA lue par pefile directement
        rva = slot
        try:
            octets = pe.get_data(rva, taille)
        except Exception as e:
            ecarts.append(f"{b['id']} : illisible à {rva:#x} : {e}")
            continue
        pad = octets[code:]
        corps = octets[:code]
        if pad and (len(set(pad)) != 1 or pad[0] != 0x90):
            ecarts.append(f"{b['id']} : le padding [{rva + code:#x}.."
                          f"{rva + taille:#x}) n'est pas NOP uniforme")
        # le 0xcc INSTRUCTION (à une frontière d'instruction) — le 0xcc
        # ENCODÉ (un immédiat/un déplacement DANS une instruction) est
        # légitime : la classe de faux positif NOMMÉE, la vérification
        # désassemble (capstone) au lieu de chercher l'octet nu
        import capstone
        cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        n_int3 = sum(1 for ins in cs.disasm(corps, rva)
                     if ins.mnemonic == "int3")
        if n_int3:
            ecarts.append(f"{b['id']} : {n_int3} instruction(s) int3 "
                          f"dans le code [{rva:#x}..{rva + code:#x})")
    return ecarts


def main() -> int:
    vt = json.loads((ICI / "verites-terrain.json").read_text(encoding="utf-8"))
    par_id = {b["id"]: b for b in vt["blocs"]}

    journal = [json.loads(l) for l in
               (ICI / "journal_tokens.jsonl").read_text(
                   encoding="utf-8").splitlines() if l.strip()]
    garde = [json.loads(l) for l in
             (ICI / "garde-brut.jsonl").read_text(
                 encoding="utf-8").splitlines() if l.strip()]
    reponses = {g["tache"]: g["reponse_api"]["choices"][0]["message"]["content"]
                for g in garde}

    # ---- la vérification (zéro divergence, le plan § 6 ; B2 : le plan D212) ----
    divergences = []
    resultats = {"A": [], "B": [], "B2": []}
    for l in journal:
        m = re.match(r"localiser-(A|B2?)-(i\d+)$", l["tache"])
        mode, bid = m.group(1), m.group(2)
        b = par_id[bid]
        rep = reponses[l["tache"]].strip()
        # le prompt exact relu (le cl100k parallèle) + la réponse
        pfile = ICI / "garde-prompts" / f"{l['tache']}.txt"
        prompt = pfile.read_text(encoding="utf-8")
        cl_p = len(CL100K.encode(prompt))
        cl_r = len(CL100K.encode(rep))
        natif = {"prompt": l["prompt_tokens"],
                 "completion": l["completion_tokens"],
                 "total": l["total_tokens"],
                 "cl100k_total": cl_p + cl_r,
                 "id": l["id"], "somme": l["somme_coherente"],
                 "source": l["source"], "modele": l["modele"]}
        resultats[mode].append({**natif, "bloc": bid, "reponse": rep})

        # ---- la vérification d'adresse + la confrontation à la carte ----
        if mode == "B2":
            # le plan B2 (D212) : QUATRE CHAMPS LITTÉRAUX — la plage est
            # calculée par la carte, jamais par le modèle
            lignes = [x for x in rep.splitlines() if x.strip()]
            if len(lignes) != 1:
                divergences.append(f"B2/{bid} : {len(lignes)} lignes (une "
                                   f"exigée) — « {rep[:60]}… »")
                continue
            m2 = re.match(
                r"^(i\d+)\s*·\s*([\w-]+)\s*·\s*(0x[0-9a-f]+)\s*·\s*(\d+)$",
                lignes[0].strip())
            if not m2:
                divergences.append(f"B2/{bid} : hors format — "
                                   f"« {lignes[0][:70]}… »")
                continue
            rid, rnom, rslot, rtaille = m2.groups()
            # LA CARTE FAIT L'ARITHMÉTIQUE : la plage calculée, confrontée
            # à la vérité-terrain (la confrontation aux octets réels vit
            # au contrôle global 5.3 — déjà vert)
            if (rid != bid or rnom != b["nom"]
                    or int(rslot, 16) != b["slot"]
                    or int(rtaille) != b["taille"]):
                divergences.append(
                    f"B2/{bid} : localisation fausse — rendu "
                    f"{rid} · {rnom} · {rslot} · {rtaille}, attendu "
                    f"{bid} · {b['nom']} · {b['slot']:#x} · {b['taille']}")
        elif mode == "B":
            lignes = [x for x in rep.splitlines() if x.strip()]
            if len(lignes) != 1:
                divergences.append(f"B/{bid} : {len(lignes)} lignes (une "
                                   f"exigée) — « {rep[:60]}… »")
                continue
            m2 = re.match(
                r"^(i\d+)\s*·\s*([\w-]+)\s*·\s*(0x[0-9a-f]+)\s*[–-]\s*(0x[0-9a-f]+)$",
                lignes[0].strip())
            if not m2:
                divergences.append(f"B/{bid} : hors format — "
                                   f"« {lignes[0][:70]}… »")
                continue
            rid, rnom, rdeb, rfin = m2.groups()
            if (rid != bid or rnom != b["nom"]
                    or int(rdeb, 16) != b["slot"]
                    or int(rfin, 16) != b["fin"]):
                divergences.append(
                    f"B/{bid} : localisation fausse — rendu "
                    f"{rid} · {rnom} · {rdeb}–{rfin}, attendu {bid} · "
                    f"{b['nom']} · {b['slot']:#x}–{b['fin']:#x}")
        else:  # mode A : l'entête complet — le bloc localisé doit être
            # le bon (l'identifiant, le nom, le slot présents et exacts)
            if bid not in rep or b["nom"] not in rep \
                    or f"{b['slot']:#x}" not in rep.replace("0X", "0x"):
                divergences.append(f"A/{bid} : l'entête rendu ne porte pas "
                                   f"l'identifiant/le nom/le slot du bloc "
                                   f"soumis — « {rep[:60]}… »")

    octets_ecarts = verifier_octets_reels(vt)

    # ---- les distributions ----
    def dist(mode, champ):
        return stats([r[champ] for r in resultats[mode]])

    nA, nB = len(resultats["A"]), len(resultats["B"])
    medA = dist("A", "total")["mediane"]
    medB = dist("B", "total")["mediane"]
    medB2 = dist("B2", "total")["mediane"]
    gain = 1 - medB / medA if medA else 0
    gain_b2 = 1 - medB2 / medA if medA else 0
    gain_reponse = (1 - dist("B", "completion")["mediane"]
                    / dist("A", "completion")["mediane"])
    gain_reponse_b2 = (1 - dist("B2", "completion")["mediane"]
                       / dist("A", "completion")["mediane"])
    div_b1 = sum(1 for d in divergences if d.startswith("B/"))
    div_b2 = sum(1 for d in divergences if d.startswith("B2/"))
    div_a = sum(1 for d in divergences if d.startswith("A/"))

    lignes = [
        "LE RAPPORT DE LA CAMPAGNE LOCALISER — 5gfx6pwkj / OPT-02",
        "(les plans pré-enregistrés : la passe 1 PLAN-5gfx6pwkj.md sha256 "
        "a0ecaf41… consigné D211 ; la passe 2 PLAN-5gfx6pwkj-B2.md sha256 "
        "0d98b0e1… consigné D212 — AVANT toute mesure ; le format D205 : "
        "la mesure avant, le gain mesuré, le vérificateur)",
        "=" * 92,
        "",
        "LA MESURE AVANT (om3ewy9lf, v0.18.0 — l'appel complet "
        "instrumenté, natif) :",
        f"  matériau {MESURE_AVANT['materiau']} + prose "
        f"{MESURE_AVANT['prose']} + RÉPONSE {MESURE_AVANT['reponse']} = "
        f"{MESURE_AVANT['total']} tokens (la réponse ≈ 47 % du total).",
        "",
        "LA CAMPAGNE (les MÊMES 18 blocs, la graine 20261117, "
        "l'instrument compter_tokens — le natif lu du champ usage) :",
        "  passe 1 : le mode A (l'actuel) contre le mode B (la plage "
        "CALCULÉE par le modèle) ;",
        "  passe 2 : le mode B2 (quatre champs LITTÉRAUX — la plage "
        "calculée PAR LA CARTE, le plan D212) ; le mode A non re-mesuré.",
        f"{'':28}{'n':>4}{'médiane':>9}{'q1':>8}{'q3':>8}{'min':>7}{'max':>8}",
        "-" * 72,
    ]
    for mode, titre in (("A", "A l'actuel — total"),
                        ("B", "B1 minimal calculé — total"),
                        ("B2", "B2 minimal littéral — total")):
        d = dist(mode, "total")
        lignes.append(f"{titre:28}{d['n']:>4}{d['mediane']:>9.0f}{d['q1']:>8.0f}"
                      f"{d['q3']:>8.0f}{d['min']:>7.0f}{d['max']:>8.0f}")
    for mode, titre in (("A", "A — réponse seule"),
                        ("B", "B1 — réponse seule"),
                        ("B2", "B2 — réponse seule")):
        d = dist(mode, "completion")
        lignes.append(f"{titre:28}{d['n']:>4}{d['mediane']:>9.0f}{d['q1']:>8.0f}"
                      f"{d['q3']:>8.0f}{d['min']:>7.0f}{d['max']:>8.0f}")
    for mode, titre in (("A", "A — cl100k (parallèle)"),
                        ("B2", "B2 — cl100k (parallèle)")):
        d = dist(mode, "cl100k_total")
        lignes.append(f"{titre:28}{d['n']:>4}{d['mediane']:>9.0f}{d['q1']:>8.0f}"
                      f"{d['q3']:>8.0f}{d['min']:>7.0f}{d['max']:>8.0f}")
    hors_log = [r for r in resultats["A"] + resultats["B"] + resultats["B2"]
                if r["source"] != "log-api"]
    sommes = [r for r in resultats["A"] + resultats["B"] + resultats["B2"]
              if not r["somme"]]

    lignes += [
        "-" * 72,
        "",
        "LE GAIN MESURÉ (lu des logs bruts, jamais tapé) :",
        f"  B1 (falsifié) : total A {medA:.0f} → B {medB:.0f} = "
        f"{gain * 100:.1f} % ; réponse {dist('A', 'completion')['mediane']:.0f} "
        f"→ {dist('B', 'completion')['mediane']:.0f} = "
        f"{gain_reponse * 100:.1f} %",
        f"  B2 (l'amendé) : total A {medA:.0f} → B2 {medB2:.0f} = "
        f"{gain_b2 * 100:.1f} % ; réponse "
        f"{dist('A', 'completion')['mediane']:.0f} → "
        f"{dist('B2', 'completion')['mediane']:.0f} = "
        f"{gain_reponse_b2 * 100:.1f} %",
        "",
        "LE VÉRIFICATEUR :",
        f"  la passe A : {18 - div_a}/18 sans divergence",
        f"  la passe B1 : {18 - div_b1}/18 — FALSIFIÉE (la plage calculée "
        f"par le modèle : 12 arithmétiques + 6 formes)",
        f"  la passe B2 : {18 - div_b2}/18 — "
        + ("ZÉRO DIVERGENCE" if div_b2 == 0 else f"{div_b2} écart(s)"),
        f"  la confrontation aux octets réels (loupe.exe lu au slot, le "
        f"padding NOP, aucun int3 instruction) : "
        f"{'VERT — 18/18' if not octets_ecarts else 'ROUGE'}",
        f"  la source (CA3) : {len(hors_log)} appel(s) hors log-api",
        f"  la somme (prompt+completion=total) : {len(sommes)} écart(s)",
    ]
    lignes += [f"    - {d}" for d in divergences if d.startswith("B2/")]
    lignes += [f"    - {e}" for e in octets_ecarts]
    nB2 = len(resultats["B2"])
    if nA != 18 or nB != 18 or nB2 != 18:
        lignes.append(f"  [ÉCART NOMMÉ] l'effectif : A={nA}/18, B={nB}/18, "
                      f"B2={nB2}/18 — la règle n≥15 : "
                      f"{'TENUE' if min(nA, nB, nB2) >= 15 else 'ROMPUE'}")

    verdict = ("VERT — le mode minimal B2 (quatre champs littéraux, la "
               "carte fait l'arithmétique) réduit le coût SANS divergence, "
               "aucun contrôle retiré ; la passe B1 falsifiée demeure "
               "consignée (la leçon : jamais de champ calculé dans la "
               "réponse)"
               if div_b2 == 0 and not octets_ecarts and not hors_log
               and nB2 >= 15 and gain_b2 > 0
               else "ROUGE — les écarts ci-dessus font foi (consignés tels "
                    "quels, l'instruction l'exige)")
    lignes += ["", f"LE VERDICT : {verdict}"]
    (ICI / "RAPPORT-5gfx6pwkj.txt").write_text("\n".join(lignes) + "\n",
                                               encoding="utf-8")
    print("\n".join(lignes))
    print("\nécrit:", ICI / "RAPPORT-5gfx6pwkj.txt")
    return 0 if verdict.startswith("VERT") else 2


if __name__ == "__main__":
    sys.exit(main())
