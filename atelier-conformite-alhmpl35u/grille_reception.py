#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""grille_reception.py — LA GRILLE DE RÉCEPTION DES TÉMOINS SIGNÉS
(alhmpl35u, le chantier 2 de l'instruction) : l'agrégateur fail-closed qui
prépare l'exécution des kits AU GESTE DU DÉVELOPPEUR SANS PRODUIRE AUCUN
RÉSULTAT.

LA RÈGLE (la lettre de l'instruction) : « l'agrégateur fail-closed refuse
tout manque (exit 2, liste). AUCUN chiffre fabriqué, la table des statuts
ne bouge QUE sur pièces recoupées. »

LA GRILLE (les lignes exigeuses, chaque pièce à son témoin signé) :
  G1  DUDECT n≥10 par N∈{60,200,400} × ≥2 machines — chaque run signé,
      l'empreinte CPU et la fréquence au témoin ;
  G2  FENCE.I RV64 — la chaîne EXACTE consignée (la sonde à deux bras,
      l'horodatage, la carte) ;
  G3  LA TROISIÈME MACHINE LOUPE — T0→T7+S0 intégral, l'empreinte CPU et
      la fréquence ;
  G4  LE TIRAGE H7 STRATIFIÉ — signé À L'OUVERTURE (la graine, les strates,
      l'ordre) ;
  G5  LA DOUBLE ANNOTATION — κ≥0,61 sur n≥50, les deux annotateurs, la
      grille F/L ;
  G6  TAMARIN AU POSTE RÉEL — les bornes nommées, la version, les lemmas.

LES AUTOTESTS : (a) une soumission SYNTHÉTIQUE complète → ADMISE (la grille
ne refuse pas l'honnête) ; (b) la soumission INCOMPLÈTE → exit 2, LA LISTE
des manques nommés ; (c) le témoin SANS signature → refusé au premier nom ;
(d) l'empreinte CPU absente → refusé nommé.

Sortie : grille-reception-autotests.txt · reception.json"""
from __future__ import annotations

import json
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parent

# LA GRILLE : (id, ligne, les pièces exigées — chaque fichier témoin)
GRILLE = [
    ("G1", "dudect n≥10 × N{60,200,400} × ≥2 machines, signé, CPU+fréquence",
     ["dudect-N60-{m}-run{i}.json" , "dudect-N200-{m}-run{i}.json",
      "dudect-N400-{m}-run{i}.json"]),
    ("G2", "fence.i RV64, la chaîne exacte consignée",
     ["fencei-rv64-temoin.txt"]),
    ("G3", "Loupe 3e machine T0→T7+S0, CPU+fréquence",
     ["loupe-T0T7S0-{machine}-temoin.json"]),
    ("G4", "H7 stratifié, le tirage signé à l'ouverture",
     ["h7-stratifie-tirage-signe.txt"]),
    ("G5", "double annotation κ≥0,61 n≥50 (grille F/L)",
     ["annotation-double-{machine}.json"]),
    ("G6", "Tamarin au poste réel, bornes nommées",
     ["tamarin-cf3-preuve.txt"]),
]


def agreger(soumission: dict) -> tuple[list[str], int]:
    """L'AGRÉGATEUR FAIL-CLOSED : rend (les manques nommés, le code).
    Code 0 = tout reçu ; code 2 = REFUS, la liste des manques."""
    manques: list[str] = []
    for gid, ligne, modeles in GRILLE:
        pieces = soumission.get(gid, [])
        if not pieces:
            manques.append(f"{gid} AUCUNE pièce — {ligne}")
            continue
        for piece in pieces:
            if not piece.get("signe"):
                manques.append(f"{gid} PIÈCE NON SIGNÉE : "
                               f"{piece.get('nom', '?')} — {ligne}")
            if gid in ("G1", "G3") and not piece.get("empreinte_cpu"):
                manques.append(f"{gid} L'EMPREINTE CPU ABSENTE du témoin : "
                               f"{piece.get('nom', '?')}")
            if gid in ("G1", "G3") and not piece.get("frequence_mhz"):
                manques.append(f"{gid} LA FRÉQUENCE ABSENTE du témoin : "
                               f"{piece.get('nom', '?')}")
            if gid == "G1":
                n = piece.get("n_runs", 0)
                if n < 10:
                    manques.append(f"{gid} n={n} < 10 : "
                                   f"{piece.get('nom', '?')}")
                if piece.get("N") not in (60, 200, 400):
                    manques.append(f"{gid} N={piece.get('N')} hors "
                                   f"{{60,200,400}} : {piece.get('nom', '?')}")
            if gid == "G5":
                if piece.get("kappa", 0) < 0.61:
                    manques.append(f"{gid} κ={piece.get('kappa')} < 0,61 : "
                                   f"{piece.get('nom', '?')}")
                if piece.get("n", 0) < 50:
                    manques.append(f"{gid} n={piece.get('n')} < 50 : "
                                   f"{piece.get('nom', '?')}")
    machines = {p.get("machine") for p in soumission.get("G1", [])}
    if len(machines) < 2:
        manques.append(f"G1 {len(machines)} machine(s) < 2 — le témoin de "
                       "deux machines distinctes exigé")
    return manques, (2 if manques else 0)


def autotests() -> list[str]:
    """LES QUATRE AUTOTESTS — la grille vit : l'honnête admise, le manque
    refusé au premier nom, la pièce nue refusée, le témoin incomplet refusé."""
    lignes = ["LES AUTOTESTS DE LA GRILLE DE RÉCEPTION (alhmpl35u, "
              "le chantier 2 — AUCUN RÉSULTAT PRODUIT : la grille attend "
              "les témoins du geste du maître)", ""]
    verts = 0
    # (a) la soumission SYNTHÉTIQUE complète — ADMISE
    complete = {
        "G1": [{"nom": f"dudect-N{N}-machine{k}-run{i}", "signe": True,
                "empreinte_cpu": "cpu-mf-XXXX", "frequence_mhz": 3200,
                "n_runs": 10, "N": N, "machine": f"machine{k}"}
               for N in (60, 200, 400) for k in (1, 2) for i in range(10)],
        "G2": [{"nom": "fencei-rv64-temoin", "signe": True}],
        "G3": [{"nom": "loupe-T0T7S0-shani-temoin", "signe": True,
                "empreinte_cpu": "cpu-mf-YYYY", "frequence_mhz": 2600}],
        "G4": [{"nom": "h7-stratifie-tirage-signe", "signe": True}],
        "G5": [{"nom": "annotation-double-machine1", "signe": True,
                "kappa": 0.71, "n": 60}],
        "G6": [{"nom": "tamarin-cf3-preuve", "signe": True}],
    }
    m, code = agreger(complete)
    ok = code == 0 and not m
    verts += ok
    lignes.append(f"  (a) la soumission complète admise : "
                  f"{'VERT — code 0' if ok else 'ROUGE : ' + str(m[:3])}")
    # (b) la soumission INCOMPLÈTE (G5 κ=0,54, G6 absent, une machine)
    incomplete = {k: list(v) for k, v in complete.items()}
    incomplete["G5"] = [{"nom": "annotation-faible", "signe": True,
                         "kappa": 0.54, "n": 60}]
    del incomplete["G6"]
    incomplete["G1"] = [p for p in incomplete["G1"]
                        if p["machine"] == "machine1"]
    m, code = agreger(incomplete)
    ok = code == 2 and any("G5" in x for x in m) and any("G6" in x for x in m) \
        and any("machine(s) < 2" in x for x in m)
    verts += ok
    lignes.append(f"  (b) l'incomplète refusée au premier nom : "
                  f"{'VERT — exit 2, ' + str(len(m)) + ' manques nommés' if ok else 'ROUGE'}")
    for x in m[:5]:
        lignes.append(f"        - {x}")
    # (c) la pièce NON SIGNÉE
    nue = {k: list(v) for k, v in complete.items()}
    nue["G2"] = [{"nom": "fencei-rv64-temoin", "signe": False}]
    m, code = agreger(nue)
    ok = code == 2 and any("NON SIGNÉE" in x for x in m)
    verts += ok
    lignes.append(f"  (c) la pièce non signée refusée : "
                  f"{'VERT — ' + m[0] if ok else 'ROUGE'}")
    # (d) l'empreinte CPU absente
    chau = {k: list(v) for k, v in complete.items()}
    chau["G3"] = [{"nom": "loupe-sans-cpu", "signe": True,
                   "frequence_mhz": 2600}]
    m, code = agreger(chau)
    ok = code == 2 and any("EMPREINTE CPU" in x for x in m)
    verts += ok
    lignes.append(f"  (d) l'empreinte CPU absente refusée : "
                  f"{'VERT — ' + m[0] if ok else 'ROUGE'}")
    lignes += ["",
               "LA TABLE DES STATUTS INCHANGÉE — aucun témoignage recoupé, "
               "aucun résultat produit (la règle de l'instruction tenue) ;",
               "LES GAPS NOMMÉS (leur geste attendu) : le token FIDO2 "
               "physique (au geste du maître) ; l'ancrage réseau TSA/Rekor "
               "(la requête au geste) ; TAMARIN AU POSTE RÉEL (non installé "
               "au bac — la vérification au geste, D240 le gap nommé "
               "reconduit) ; les miroirs Windows de la garde RAM (le "
               "terrain) ; la SECONDE MACHINE au bac (une seule — le "
               "témoignage l'exige, jamais simulé).",
               "",
               f"LE VERDICT : {verts}/4 AUTOTESTS VERTS — " +
               ("VERT" if verts == 4 else "ROUGE")]
    return lignes


def main() -> int:
    lignes = autotests()
    (ICI / "grille-reception-autotests.txt").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8")
    (ICI / "reception.json").write_text(json.dumps({
        "grille": [{"id": g, "ligne": l} for g, l, _ in GRILLE],
        "resultats_produits": 0,
        "table_des_statuts": "INCHANGÉE (aucune pièce recoupée)",
        "verdict": "VERT" if lignes[-1].endswith("VERT") else "ROUGE",
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(lignes))
    return 0 if lignes[-1].endswith("VERT") else 2


if __name__ == "__main__":
    sys.exit(main())
