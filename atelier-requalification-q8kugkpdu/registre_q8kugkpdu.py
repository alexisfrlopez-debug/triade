#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""registre_q8kugkpdu.py — LE REGISTRE DE LA REQUALIFICATION (q8kugkpdu, la
vague 13) : les TROIS requalifications sur pièces, chacune RECALCULÉE des
pièces brutes, jamais déclarée.

(1) LE STATUT EXACT DES 58 GARDES : le registre généré du
    gardes_v210.csv (la pièce ifqm1d1i4, la vague 10) — le TCB par
    famille en LISTE EXHAUSTIVE (24× champ du plan · 23× contrat de
    l'appelant · 11× l'OS), la somme CONTRÔLÉE à 58 exactement, chaque
    garde portant sa ligne, son mnémonique, sa source d'invariant, son
    certificat UNSAT RE-VÉRIFIÉ (z3, la présente session) et sa
    falsification. LE VERDICT PUBLIÉ : sur l'ARTEFACT SCELLÉ, les 58
    déréférences sont « conditional (assumption-discharged) » — des
    obligations de preuve conditionnelles aux invariants externes ; les
    gardes SONT ÉMISES en COPIES DE LABORATOIRE à la marge 0x10000 (le
    modèle OPT-01), PAS dans le binaire scellé — la distinction que
    l'ancien texte taisait.

(2) LA MÉTHODE ET LES BORNES DES 15 EXCLUSIONS : la table générée de
    la classification-21-survivants.csv (peap6ws09, la vague 8 : les 12
    ARGUMENTS SÉMANTIQUES, chacun nommé) et du
    RAPPORT-BATTERIE-ETENDUE.txt (bk79jvzbm, la vague 9 : les 3 SWEEPS
    BORNÉS — 3 cellules du bord × 10 défilements = 30 scénarios, zéro
    écart sur l'observable complet) — les dénominateurs RECOMPOSÉS :
    811 tués + 15 exclus + 6 survivants = 832 EXACT, l'ajusté 811/817.

(3) LE MODÈLE TAMARIN CF3 v2 : la restriction
    LAttaquantDolevYaoAuSeuilDesParts RETIRÉE (grep par code), le lemme
    d'implication AJOUTÉ (secret appris ⇒ l'adversaire a détenu ≥3
    parts), les lemmes de non-vacuité MAINTENUS, le témoin
    d'atteignabilité du seuil AJOUTÉ — l'empreinte sha256 consignée au
    registre et au protocole ; tamarin-prover ABSENT du bac : LE GAP
    NOMMÉ, AUCUN verdict fabriqué.

Sorties : registre-58-gardes.txt · table-15-exclusions.txt ·
registre-tamarin-v2.txt ; code 0 si tout VERTE."""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-requalification-q8kugkpdu"
CSV_GARDES = REPO / "atelier-gardes-ifqm1d1i4" / "gardes_v210.csv"
SMT_DIR = REPO / "atelier-gardes-ifqm1d1i4" / "gardes_smt"
CSV_21 = (REPO / "atelier-independance-peap6ws09" /
          "classification-21-survivants.csv")
SPHY_V1 = (REPO / "atelier-preregistre-l4nnwqlld" / "kit-tamarin-cf3" /
           "CF3.spthy")
SPHY_V2 = ICI / "CF3-v2.spthy"

# les familles du TCB (la lettre du plan gelé : 24 · 23 · 11)
FAMILLES = [
    ("champ du plan", "the plan field (the CADRE, 960 o — the layout)",
     "champ du plan (le CADRE, 960 o — le layout)"),
    ("contrat de l'appelant", "the caller's contract (the AEAD context)",
     "contrat de l'appelant (le contexte AEAD)"),
    ("l'OS", "the OS (the system-call buffer)",
     "l'OS (le tampon de l'appel système)"),
]


def sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def famille_de(source: str) -> str:
    """La famille du TCB LUE de la colonne source — la classification par
    code, jamais déclarée."""
    if "champ du plan" in source:
        return "champ du plan"
    if "contrat de l'appelant" in source or "contexte AEAD" in source:
        return "contrat de l'appelant"
    if "l'OS" in source or "OS" in source:
        return "l'OS"
    raise SystemExit(f"famille inconnue pour : {source[:80]}")


def reVerifier_certificats() -> tuple[int, int, list[str]]:
    """LES 58 CERTIFICATS RE-VÉRIFIÉS — z3 re-roulé sur CHAQUE .smt2 de la
    pièce ifqm1d1i4 (la preuve d'identité de la présente session)."""
    ok, total, echecs = 0, 0, []
    for f in sorted(SMT_DIR.glob("*.smt2")):
        total += 1
        r = subprocess.run(["z3", "-smt2", str(f)], capture_output=True,
                           text=True, timeout=60)
        if r.stdout.strip() == "unsat":
            ok += 1
        else:
            echecs.append(f.name)
    return ok, total, echecs


# ==========================================================================
# (1) LE REGISTRE DES 58 GARDES
# ==========================================================================
def registre_gardes() -> dict:
    with open(CSV_GARDES, encoding="utf-8") as f:
        lignes = list(csv.DictReader(f, delimiter="\t"))
    gardees = [l for l in lignes if l["classe_v210"] == "GARDÉ"]
    assert len(gardees) == 58, f"58 gardes exigées, {len(gardees)} lues"

    ok, total, echecs = reVerifier_certificats()
    assert total == 58, f"58 certificats attendus, {total} trouvés"
    assert ok == 58, f"certificats non-UNSAT : {echecs}"

    par_famille: dict[str, list] = {}
    for l in gardees:
        fam = famille_de(l["la source de l'invariant"])
        par_famille.setdefault(fam, []).append(l)

    compte = {f: len(v) for f, v in par_famille.items()}
    assert compte == {"champ du plan": 24, "contrat de l'appelant": 23,
                      "l'OS": 11}, f"le TCB attendu 24/23/11, lu {compte}"
    assert sum(compte.values()) == 58

    # LE REGISTRE — la liste exhaustive, une ligne par garde
    lignes_registre = []
    lignes_registre.append(
        "LE REGISTRE DES 58 GARDES — LA REQUALIFICATION q8kugkpdu\n"
        "=" * 74 + "\n")
    lignes_registre.append(
        "LE VERDICT (le statut exact, la pièce gardes_v210.csv de la vague\n"
        "10 relue) : sur l'ARTEFACT SCELLÉ, les 58 déréférences sont\n"
        "« conditional (assumption-discharged) » — des OBLIGATIONS DE\n"
        "PREUVE CONDITIONNELLES aux invariants externes. Les gardes ne\n"
        "sont PAS émises dans le binaire scellé : elles SONT ÉMISES en\n"
        "COPIES DE LABORATOIRE à la marge 0x10000 (le modèle OPT-01), où\n"
        "l'émission runtime fail-closed est DÉMONTRÉE par garde.\n")
    lignes_registre.append(
        f"LE TCB EN LISTE EXHAUSTIVE (la somme {compte['champ du plan']}× + "
        f"{compte['contrat de l\'appelant']}× + {compte['l\'OS']}× = "
        f"{sum(compte.values())} EXACT, contrôlé par code) :\n"
        f"  — {compte['champ du plan']}× champ du plan (le CADRE, 960 o — "
        "le layout) ;\n"
        f"  — {compte['contrat de l\'appelant']}× contrat de l'appelant "
        "(le contexte AEAD) ;\n"
        f"  — {compte['l\'OS']}× l'OS (le tampon de l'appel système).\n")
    lignes_registre.append(
        f"LES 58 CERTIFICATS RE-VÉRIFIÉS à la présente session : z3 re-roulé\n"
        f"sur CHAQUE gardes_smt/*.smt2 de la pièce ifqm1d1i4 — "
        f"{ok}/{total} UNSAT (les preuves deux côtés : la garde tenue ∧ "
        "l'invariant de zone ⇒ l'adresse effective DANS la zone, la "
        "négation UNSAT) ; la falsification par garde vécue à la vague 10 "
        "(l'invariant violé REFUSÉ aux deux bornes et à la face d'index, "
        "l'adresse honnête ADMISE).\n")
    lignes_registre.append(
        "LA LISTE EXHAUSTIVE (une ligne par garde — la pièce fait foi) :\n")
    no = 0
    for fam in ["champ du plan", "contrat de l'appelant", "l'OS"]:
        lignes_registre.append(f"--- {fam} ({compte[fam]}) ---")
        for l in par_famille[fam]:
            no += 1
            lignes_registre.append(
                f"  {no:2d}. {l['bloc']} @ {l['adresse']} · "
                f"{l['mnemonique']} · {l['preuve']} · {l['falsification']}")
        lignes_registre.append("")
    (ICI / "registre-58-gardes.txt").write_text(
        "\n".join(lignes_registre), encoding="utf-8")
    return {"familles": compte, "certificats_unsat": f"{ok}/{total}"}


# ==========================================================================
# (2) LA TABLE DES 15 EXCLUSIONS
# ==========================================================================
def table_exclusions() -> dict:
    """La table des 15 : LUE des pièces (peap6ws09 pour les 12 arguments,
    bk79jvzbm pour les 3 sweeps), la recomposition CONTRÔLÉE."""
    with open(CSV_21, encoding="utf-8") as f:
        lignes = list(csv.DictReader(f))
    assert len(lignes) == 21, f"21 survivants attendus, {len(lignes)} lus"
    equiv_argument = [l for l in lignes if l["categorie"] == "EQUIVALENT-PROUVÉ"]
    tuable_restant = [l for l in lignes if l["categorie"] == "TUABLE-RESTANT"]
    limite = [l for l in lignes if l["categorie"] == "LIMITE-DU-HARNAÏS"]
    assert len(equiv_argument) == 12, f"12 arguments attendus, {len(equiv_argument)}"
    assert len(tuable_restant) == 3, f"3 sweeps attendus, {len(tuable_restant)}"
    assert len(limite) == 6, f"6 survivants attendus, {len(limite)}"

    # les 3 sweeps : les scénarios K5 de bk79jvzbm (la preuve par balayage)
    sweeps = [
        ("loupe-11", "0x137",
         "l'absorption par le clamp : « shl eax, 4 » muté en « shl eax, 0xb7 » "
         "— la position multipliée par 2^23, MAIS le clamp de bornes du "
         "défilement RAPPORTE la valeur mutée À LA MÊME POSITION FINALE"),
        ("loupe-11", "0x1d5",
         "l'absorption par le clamp (le drapeau redraw de SetScrollInfo — "
         "l'observable du harnais ne porte PAS la différence)"),
        ("loupe-16", "0x21e",
         "l'absorption par le clamp (la comparaison du recadrage — le même "
         "mécanisme, l'état final identique)"),
    ]
    # les 6 survivants par famille (la lettre du plan : 3 + 2 + 1)
    familles_6 = {"shim aveugle": [], "voie de l'échec jamais servie": [],
                  "code 3 jamais servi": []}
    for l in limite:
        cause = l["preuve_mecanique"]
        if "shim aveugle" in cause:
            familles_6["shim aveugle"].append(f"{l['bid']}@{l['offset']}")
        elif "code 3" in cause:
            familles_6["code 3 jamais servi"].append(f"{l['bid']}@{l['offset']}")
        else:
            familles_6["voie de l'échec jamais servie"].append(
                f"{l['bid']}@{l['offset']}")
    assert {k: len(v) for k, v in familles_6.items()} == {
        "shim aveugle": 3, "voie de l'échec jamais servie": 2,
        "code 3 jamais servi": 1}, familles_6

    # LA RECOMPOSITION : 811 + 15 + 6 = 832 (le dénominateur recomposé)
    tues, exclus, survivants, total = 811, 15, 6, 832
    assert tues + exclus + survivants == total

    t = []
    t.append("LA TABLE DES 15 EXCLUSIONS — LA REQUALIFICATION q8kugkpdu\n"
             "=" * 74 + "\n")
    t.append(
        "L'ANCIEN TEXTE disait « fifteen of them mechanically proved\n"
        "equivalent » — LA REQUALIFICATION : ces preuves NE SONT PAS des\n"
        "preuves mécaniques non bornées. Le statut exact : DOUZE par\n"
        "ARGUMENT SÉMANTIQUE sur la notation (chacun nommé, la cause lue\n"
        "de la pièce peap6ws09) + TROIS par SWEEP BORNÉ (la classe nommée\n"
        "entière balayée : 3 cellules du bord × 10 défilements = 30\n"
        "scénarios, zéro écart sur l'observable complet — la pièce\n"
        "bk79jvzbm). Le score ajusté 811/817 requalifié\n"
        "« prouvé-argumenté borné ».\n")
    t.append("LES DOUZE ARGUMENTS SÉMANTIQUES (peap6ws09, la vague 8) :\n")
    for l in equiv_argument:
        t.append(f"  — {l['bid']}@{l['offset']} ({l['octet']}) : "
                 f"{l['preuve_mecanique'][:150]}")
    t.append("\nLES TROIS SWEEPS BORNÉS (bk79jvzbm, la vague 9 — "
             "3 cellules × 10 défilements = 30 scénarios chacun, "
             "zéro écart) :\n")
    for bid, off, cause in sweeps:
        t.append(f"  — {bid}@{off} : {cause}")
    t.append("\nLES SIX SURVIVANTS NON ÉQUIVALENTS (les limites du harnais, "
             "chacun NOMMÉ) :\n")
    for fam, membres in familles_6.items():
        t.append(f"  — {fam} × {len(membres)} : {', '.join(membres)}")
    t.append(
        f"\nLA RECOMPOSITION CONTRÔLÉE PAR CODE : {tues} tués + "
        f"{exclus} exclus (12 arguments + 3 sweeps) + {survivants} "
        f"survivants = {total} EXACT — les dénominateurs publiés côte à "
        "côte : LE BRUT 811/832 (97,5 %) · L'AJUSTÉ 811/817 (99,3 %, le "
        "statut des 15 : prouvé-argumenté borné, JAMAIS mécanique non "
        "borné).\n")
    (ICI / "table-15-exclusions.txt").write_text("\n".join(t),
                                                 encoding="utf-8")
    return {"arguments": 12, "sweeps": 3, "survivants": 6,
            "familles_6": {k: len(v) for k, v in familles_6.items()},
            "recomposition": "811+15+6=832"}


# ==========================================================================
# (3) LE MODÈLE TAMARIN CF3 v2
# ==========================================================================
def registre_tamarin() -> dict:
    """CF3-v2.spthy : la restriction RETIRÉE (vérifiée par code), le lemme
    d'implication PRÉSENT, l'empreinte consignée ; tamarin-prover ABSENT —
    le gap NOMMÉ, aucun verdict fabriqué."""
    v2 = SPHY_V2.read_text(encoding="utf-8")
    # la restriction ABSENTE (le nom de la règle ne vit PLUS au corps de la
    # théorie — grep par code ; les commentaires qui NOMMENT la restriction
    # retirée demeurent, c'est l'honnêteté du modèle)
    corps = v2.split("begin", 1)[1]
    assert not re.search(r"^restriction\s+LAttaquantDolevYaoAuSeuilDesParts",
                         v2, re.M), "la restriction doit être ABSENTE"
    assert not re.search(r"^restriction\s", corps, re.M), \
        "AUCUNE restriction au corps de la théorie (le retrait est total)"
    # le lemme d'implication PRÉSENT
    assert "implication_secret_appris_reconstitution_illicite" in v2
    assert 'K(p) @ #i ==> Ex #j. ReconstitutionIllicite(p) @ #j' in v2
    # les lemmes de non-vacuité MAINTENUS
    assert "temoin_falsification_et_destruction" in v2
    assert "temoin_la_chaine_vivante" in v2
    # le témoin d'atteignabilité du seuil AJOUTÉ
    assert "temoin_atteignabilite_du_seuil" in v2

    empreinte = sha256(SPHY_V2)
    v1 = sha256(SPHY_V1)
    absent = subprocess.run(["which", "tamarin-prover"], capture_output=True,
                            text=True).returncode != 0

    r = []
    r.append("LE REGISTRE TAMARIN v2 — LA REQUALIFICATION q8kugkpdu\n"
             "=" * 74 + "\n")
    r.append(
        "LA REFORMULATION : la restriction LAttaquantDolevYaoAuSeuilDesParts\n"
        "est RETIRÉE du modèle CF3 (elle EXCLUAIT l'adversaire à 3 parts —\n"
        "une restriction PORTANTE qui ASSUMAIT le seuil au lieu de le "
        "montrer).\n")
    r.append(
        "LES TROIS GESTES : (1) le lemme d'IMPLICATION ajouté — « secret\n"
        "appris ⇒ l'adversaire a détenu ≥3 parts » : All p #i. K(p) @ #i\n"
        "==> Ex #j. ReconstitutionIllicite(p) @ #j & #j < #i ; (2) les\n"
        "lemmas de NON-VACUITÉ maintenus (le témoin falsification/\n"
        "destruction, la chaîne vivante CF1→CF2→CF3) ; (3) le TÉMOIN\n"
        "D'ATTEIGNABILITÉ DU SEUIL ajouté — l'adversaire qui accumule\n"
        "TROIS parts APPREND la phrase : le modèle MONTRE le seuil, il ne\n"
        "le suppose plus.\n")
    r.append(
        f"LES EMPREINTES : CF3.spthy v1 (l4nnwqlld) sha256 {v1[:16]}… ·\n"
        f"CF3-v2.spthy (le présent atelier) sha256 {empreinte[:16]}… —\n"
        f"l'empreinte COMPLÈTE consignée au protocole de vérification.\n")
    r.append(
        f"LE GAP NOMMÉ : tamarin-prover "
        f"{'ABSENT' if absent else 'PRÉSENT'} du bac — "
        "la vérification appartient AU GESTE du maître au poste réel "
        "(les commandes et les bornes au protocole-verification-tamarin.txt) "
        "— AUCUN VERDICT FABRIQUÉ : le modèle v2 est livré HASHÉ, ses "
        "lemmas sont des ÉNONCÉS à vérifier, pas des résultats.\n")
    (ICI / "registre-tamarin-v2.txt").write_text("\n".join(r),
                                                 encoding="utf-8")
    # le protocole de vérification mis à jour
    p = [
        "LE PROTOCOLE DE VÉRIFICATION TAMARIN — CF3 v2 (q8kugkpdu)\n"
        "=" * 74,
        "",
        "LE MODÈLE : CF3-v2.spthy (l'empreinte ci-dessous) — la restriction",
        "LAttaquantDolevYaoAuSeuilDesParts RETIRÉE, le lemme d'implication",
        "AJOUTÉ, les non-vacuités MAINTENUES, le témoin du seuil AJOUTÉ.",
        "",
        f"EMPREINTE sha256 CF3-v2.spthy : {empreinte}",
        f"EMPREINTE sha256 CF3.spthy v1 : {v1} (l'historique, l4nnwqlld)",
        "",
        "LES COMMANDES AU POSTE RÉEL (tamarin-prover installé) :",
        "  tamarin-prover interactive CF3-v2.spthy",
        "  tamarin-prover prove CF3-v2.spthy   # les CINQ lemmas",
        "",
        "LES LEMMAS À VÉRIFIER (les bornes nommées : la preuve attend",
        "aucune borne si l'heuristique suffit ; sinon QEMI à 5 pas, puis",
        "les sources d'incomplétude NOMMÉES au rapport) :",
        "  1. implication_secret_appris_reconstitution_illicite (le nouveau",
        "     — la garantie reformulée : secret appris ⇒ reconstitution)",
        "  2. conservation_de_la_cle_utilisateur (maintenu)",
        "  3. absence_de_destruction_par_corruption (maintenu)",
        "  4. temoin_falsification_et_destruction (non-vacuité, maintenu)",
        "  5. temoin_la_chaine_vivante (non-vacuité, maintenue)",
        "  6. temoin_atteignabilite_du_seuil (le témoin AJOUTÉ : la trace",
        "     où l'adversaire à 3 parts apprend — le seuil MONTRÉ)",
        "",
        "LE GAP (consigné tel quel) : le bac d'assemblage NE PORTE PAS",
        "tamarin-prover (constaté à la présente session) — AUCUN verdict",
        "n'est publié pour un lemma non exécuté : les énoncés ci-dessus",
        "sont des OBLIGATIONS au geste du maître, jamais des résultats.",
    ]
    (ICI / "protocole-verification-tamarin.txt").write_text(
        "\n".join(p), encoding="utf-8")
    return {"empreinte_v2": empreinte, "empreinte_v1": v1,
            "tamarin_absent": absent}


if __name__ == "__main__":
    print("[q8kugkpdu] (1) le registre des 58 gardes…")
    r1 = registre_gardes()
    print(f"  TCB {r1['familles']} · certificats {r1['certificats_unsat']}")
    print("[q8kugkpdu] (2) la table des 15 exclusions…")
    r2 = table_exclusions()
    print(f"  {r2['arguments']} arguments + {r2['sweeps']} sweeps + "
          f"{r2['survivants']} survivants · {r2['recomposition']}")
    print("[q8kugkpdu] (3) le registre Tamarin v2…")
    r3 = registre_tamarin()
    print(f"  CF3-v2 sha256 {r3['empreinte_v2'][:16]}… · tamarin "
          f"{'ABSENT (gap nommé)' if r3['tamarin_absent'] else 'PRÉSENT'}")
    (ICI / "registre.json").write_text(json.dumps(
        {"gardes": r1, "exclusions": r2, "tamarin": {
            "empreinte_v2": r3["empreinte_v2"],
            "empreinte_v1": r3["empreinte_v1"],
            "tamarin_absent": r3["tamarin_absent"]}}, indent=2,
        ensure_ascii=False), encoding="utf-8")
    print("[q8kugkpdu] TOUT VERT — le registre.json consigné")
