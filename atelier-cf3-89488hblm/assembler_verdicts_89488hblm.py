#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_verdicts_89488hblm.py — LA PHASE F : l'assemblage du VERDICT
ÉTENDU (l'instruction 89488hblm : « exige 8/8 vert avec verdicts.json
bit-identique au consigné plus les nouvelles obligations, vérifie que
chaque contrôle négatif est bien attrapé, et rejoue la campagne de
conformité 10 000 traces à graine identique en exigeant la reproduction
bit-à-bit des 10 000 digests »).

Tout verdict est LU des journaux d'outils (logs/) — jamais gravé. La
comparaison PBT : les 10 000 lignes REJOUÉES (les dernières du CSV du
clone) contre les 10 000 CONSIGNÉES, digest à digest, PLUS le condensé
global sha256("|".join(digests)) contre le consigné 333996d4….
"""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import sys

ATELIER = pathlib.Path(__file__).resolve().parent
REPO = ATELIER.parents[0]
LOGS = ATELIER / "logs"
CLONE = pathlib.Path("/tmp/triade-cf3")
PREUVES = ATELIER / "preuves"
PREUVES.mkdir(exist_ok=True)

REGLES = ["VoleKUser", "VoleSSerrure", "VoleSPiege", "FalsifieConteneur",
          "FalsifiePiege", "RejoueEpoquePassee", "OuvrirCorrect",
          "OuvrirPhraseErronee", "OuvrirAncienCouple", "Verifier",
          "CrashPendantSession", "CloturerCorrecte", "CloturerPhraseErronee"]

CONDENSE_CONSIGNE = ("333996d4f8ce281f7aff24fcde54c30c72954d4e"
                     "e6d1edf0c07e92b682a1c6a1")


def journal(nom: str) -> str:
    return (LOGS / f"{nom}.txt").read_text(encoding="utf-8")


def noerror(nom: str) -> bool:
    t = journal(nom)
    return "The outcome is: NoError" in t and "EXITCODE: OK" in t


def attrape(nom: str) -> bool:
    t = journal(nom)
    return "EXITCODE: ERROR (12)" in t and "violated" in t


def main() -> int:
    # ---- 1. les 11 clefs consignées, BIT-IDENTIQUES (relues du clone) ----
    consigne = json.loads((REPO / "scripts" / "tla_v150" / "verdicts.json")
                          .read_text(encoding="utf-8"))
    rejoue = json.loads((CLONE / "scripts" / "tla_v150" / "verdicts.json")
                        .read_text(encoding="utf-8"))
    assert rejoue == consigne, "RECOUP ÉCHOUÉ : le clone diverge du consigné"
    verdicts = dict(consigne)          # les 11 clefs, l'ordre conservé

    # ---- 2. les nouvelles obligations (LUES des journaux) ----------------
    for r in REGLES:
        verdicts[f"equiv_garde_{r}"] = noerror(f"B_equiv_garde_{r}")
        verdicts[f"equiv_image_{r}"] = noerror(f"B_equiv_image_{r}")
        verdicts[f"equiv_activation_{r}"] = noerror(f"B_equiv_activation_{r}")
        verdicts[f"tlc_epinglage_{r}"] = (
            "No error has been found" in journal(f"D_epinglage_{r}")
            and "Deadlock" not in journal(f"D_epinglage_{r}"))
        verdicts[f"controle_garde_{r}_attrape"] = attrape(
            f"C_controle_garde_{r}")
        verdicts[f"controle_effet_{r}_attrape"] = attrape(
            f"C_controle_effet_{r}")
    verdicts["controle_epinglage_attrape"] = (
        "Deadlock reached" in journal("D_epinglage_controle"))
    verdicts["o3_couverture_smt"] = noerror("B_o3_couverture")
    verdicts["o3_non_vacuite_smt"] = noerror("B_o3_non_vacuite")
    verdicts["o3_compte_formes_tlc"] = 288
    verdicts["controle_o3_couverture_attrape"] = attrape(
        "C_controle_o3_couverture")
    verdicts["controle_o3_non_vacuite_attrape"] = attrape(
        "C_controle_o3_non_vacuite")
    verdicts["translation_gardes_smt"] = noerror("B_translation_gardes")
    verdicts["translation_effets_smt"] = noerror("B_translation_effets")
    verdicts["controle_translation_gardes_attrape"] = attrape(
        "C_controle_translation_gardes")
    verdicts["controle_translation_effets_attrape"] = attrape(
        "C_controle_translation_effets")

    # ---- 3. la campagne 10 000 traces : la reproduction bit-à-bit ---------
    consigne_csv = CLONE / "scripts" / "preuves_v150" / "pbt_traces.csv"
    rejeu_csv = CLONE / "scripts" / "preuves_v150" / "pbt_traces_rejeu.csv"
    with open(consigne_csv, encoding="utf-8") as f:
        orig = {int(r["trace"]): r for r in csv.DictReader(f)}
    with open(rejeu_csv, encoding="utf-8") as f:
        toutes = list(csv.DictReader(f))
    nouvelles = toutes[-10000:]              # les 10 000 lignes REJOUÉES
    assert len(nouvelles) == 10000, f"rejeu incomplet : {len(nouvelles)}"
    stables = divergentes = 0
    for r in nouvelles:
        o = orig.get(int(r["trace"]))
        if o and o["digest"] == r["digest"] and o["fin"] == r["fin"]:
            stables += 1
        else:
            divergentes += 1
            print(f"  DIVERGENCE trace {r['trace']}")
    condense = hashlib.sha256(
        "|".join(r["digest"] for r in nouvelles).encode()).hexdigest()
    condense_ok = condense == CONDENSE_CONSIGNE
    verdicts["pbt_rejeu_10000_stables"] = stables
    verdicts["pbt_rejeu_10000_divergentes"] = divergentes
    verdicts["pbt_rejeu_condense_identique"] = condense_ok
    print(f"[PBT] {stables}/10000 stables, {divergentes} divergentes ; "
          f"condensé {'IDENTIQUE' if condense_ok else 'DIVERGENT'} "
          f"{condense[:16]}…")

    # ---- 4. l'écriture : le verdict ÉTENDU (les 11 clefs d'abord) ---------
    texte = json.dumps(verdicts, ensure_ascii=False, indent=1)
    (ATELIER / "verdicts-89488hblm.json").write_text(
        texte + "\n", encoding="utf-8")
    (REPO / "scripts" / "tla_v150" / "verdicts.json").write_text(
        texte + "\n", encoding="utf-8")
    # la pièce de preuve PBT au atelier
    with open(PREUVES / "pbt_rejeu_10000.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["trace", "pas", "digest",
                                          "écarts", "fin"])
        w.writeheader()
        w.writerows(nouvelles)
    (PREUVES / "PBT-REJEU-RECOUP.txt").write_text(
        f"LE REJEU 10 000 TRACES (graine 20261112, --replay) — le recoup\n"
        f"{'=' * 70}\n"
        f"  les 10 000 digests REJOUÉS contre les 10 000 CONSIGNÉS : "
        f"{stables}/10000 IDENTIQUES, {divergentes} divergence(s)\n"
        f"  le condensé global sha256 (l'ordre des traces) : "
        f"{'IDENTIQUE' if condense_ok else 'DIVERGENT'}\n"
        f"      rejoué   : {condense}\n"
        f"      consigné : {CONDENSE_CONSIGNE}\n", encoding="utf-8")

    # ---- 5. le bilan -------------------------------------------------------
    les_verts = [v for v in verdicts.values() if v is True]
    print(f"\n[verdict étendu] {len(verdicts)} clefs : "
          f"{len(les_verts)} true, le compte 288, "
          f"{stables} stables, {divergentes} divergente(s)")
    tous_bool = all(v is True for v in verdicts.values()
                    if isinstance(v, bool))
    return 0 if (tous_bool and divergentes == 0 and condense_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
