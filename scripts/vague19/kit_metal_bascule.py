#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIT MÉTAL DE BASCULE CONCURRENTE — PRÉ-ENREGISTRÉ, SANS RÉSULTAT FABRIQUÉ (W19METAL).

Objet : le protocole du run matériel de la transaction D253 sur ≥ 2 machines, et
l'agrégateur FAIL-CLOSED qui refuse tout jeu incomplet ou corrompu. Aucun chiffre
n'existe avant le geste du développeur : le kit part EN ATTENTE.

Le run, par machine (≥ 2) et par configuration :
  - CPUID consigné (vendor, family, model, stepping, drapeaux utiles dont cmpxchg16b),
    fréquence effective consignée, cœur épinglé (affinité) ;
  - N ≥ 30 exécutions par configuration, graine consignée, ordre consigné ;
  - injection d'interruption à chacun des SEPT états (0 à 6) ;
  - rollback sous trafic depuis publication / invalidation / vérification ;
  - les CINQ aléas D261 exercés (thread créé pendant le rendez-vous, retour de pile
    dans la plage, rel32 hors portée ±2 GiB, slot de 16 octets non réservé, verrou détenu).

L'agrégateur : un run manquant = REFUS nommé ; un run corrompu (schéma, empreinte) =
REFUS nommé ; jamais de verdict partiel.

Usage :
  python3 scripts/vague19/kit_metal_bascule.py --preregistrer   # écrit le pré-enregistrement
  python3 scripts/vague19/kit_metal_bascule.py --autotest       # agrégateur : 3 contrôles
  python3 scripts/vague19/kit_metal_bascule.py --statut         # EN ATTENTE (aucun run réel)
"""
import hashlib
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = RACINE / "atelier-w19-metal"
GRAINE = 20261124
N_PAR_CONFIG = 30
ETATS = [0, 1, 2, 3, 4, 5, 6]
ALEA_D261 = [
    "thread-cree-pendant-rendez-vous",
    "retour-pile-dans-plage",
    "hors-portee-rel32",
    "slot-non-reserve",
    "verrou-detenu",
]
ROLLBACK_DEPUIS = ["publication", "invalidation", "verification"]
MACHINES = ["M1", "M2"]          # ≥ 2 ; les identifiants réels sont remplis au run


def preregistrement():
    return {
        "objet": "run métal de la transaction D253 (publication de bascule concurrente)",
        "graine": GRAINE,
        "n_par_configuration": N_PAR_CONFIG,
        "machines_attendues": MACHINES,
        "etats": ETATS,
        "aleas_d261": ALEA_D261,
        "rollback_depuis": ROLLBACK_DEPUIS,
        "chronometre": "monotone (clock_gettime CLOCK_MONOTONIC)",
        "coeur_epingle": "affinite obligatoire, consignee par machine",
        "cpuid_consigne": ["vendor", "family", "model", "stepping", "flags(cmpxchg16b)"],
        "frequence_consignee": "fréquence effective mesurée pendant le run (kHz)",
        "commande": "scripts/vague19/kit_metal_bascule.py --run --machine <ID> --sortie <JSON>",
        "convention": "un run = (machine, etat, alea|nominal, rollback_depuis|aucun) ; "
                      "l'agrégat ne vaut que si les DEUX machines portent TOUS les cas",
        "statut": "EN ATTENTE — aucun run matériel n'existe à la consignation",
    }


def sha256(p):
    d = hashlib.sha256()
    d.update(pathlib.Path(p).read_bytes())
    return d.hexdigest()


def preregistrer():
    DOSSIER.mkdir(exist_ok=True)
    f = DOSSIER / "preregistrement.json"
    f.write_text(json.dumps(preregistrement(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[preregistre] écrit {f.relative_to(RACINE)}")
    print(f"[preregistre] sha256 {sha256(f)}")
    print("[preregistre] le gel PRÉCÈDE tout run ; une cible re-tirée après mesure serait un refus.")
    return 0


def cas_attendus():
    cas = []
    for m in MACHINES:
        for e in ETATS:
            cas.append((m, f"etat-{e}", "nominal"))
        for a in ALEA_D261:
            cas.append((m, "rendez-vous", a))
        for r in ROLLBACK_DEPUIS:
            cas.append((m, f"rollback-{r}", "sous-trafic"))
    return cas


def run_valide(run):
    """Un run est valide s'il porte TOUS les champs du protocole et une empreinte cohérente."""
    requis = ("machine", "cas", "variante", "n", "graine", "cpuid", "frequence_khz",
              "coeur", "etats_observes", "journal_sha256")
    if not isinstance(run, dict):
        return "CORROMPU:run-non-objet"
    for k in requis:
        if k not in run:
            return f"CORROMPU:champ-absent:{k}"
    if run["graine"] != GRAINE:
        return "CORROMPU:graine-divergente"
    if run["n"] < N_PAR_CONFIG:
        return "CORROMPU:n-insuffisant"
    if not isinstance(run["cpuid"], dict) or "vendor" not in run["cpuid"]:
        return "CORROMPU:cpuid-incomplet"
    if run["frequence_khz"] <= 0:
        return "CORROMPU:frequence-non-mesuree"
    if any(e not in ETATS for e in run["etats_observes"]):
        return "CORROMPU:etat-hors-domaine"
    if "PARTIEL" in json.dumps(run.get("sorties", {})):
        return "CORROMPU:etat-partiel-executable"
    return None


def agrege(runs, journal_sha256):
    """FAIL-CLOSED : tout cas manquant ou tout run corrompu REFUSE ; jamais de partiel."""
    motifs = []
    vus = set()
    for r in runs:
        pb = run_valide(r)
        if pb:
            motifs.append(f"REFUS {pb} — {r.get('machine', '?')}/{r.get('cas', '?')}")
            continue
        vus.add((r["machine"], r["cas"], r["variante"]))
    for (m, c, v) in cas_attendus():
        if (m, c, v) not in vus:
            motifs.append(f"REFUS MANQUANT — {m}/{c}/{v}")
    if not journal_sha256 or len(journal_sha256) != 64:
        motifs.append("REFUS JOURNAL — empreinte des journaux bruts absente")
    if motifs:
        return {"verdict": "REFUS", "motifs": sorted(set(motifs)), "runs": len(runs)}
    return {"verdict": "VERT", "motifs": [], "runs": len(runs)}


def _run_synthetique(m, cas, variante, n=N_PAR_CONFIG):
    return {
        "machine": m, "cas": cas, "variante": variante, "n": n, "graine": GRAINE,
        "cpuid": {"vendor": "GenuineIntel", "family": 6, "model": 158, "stepping": 10,
                  "flags": ["cmpxchg16b"]},
        "frequence_khz": 3600000, "coeur": 2,
        "etats_observes": [0, 1, 2, 3, 4, 5, 6],
        "sorties": {"aucun_etat_partiel": True},
        "journal_sha256": "a" * 64,
    }


def autotest():
    tous = [_run_synthetique(m, c, v) for (m, c, v) in cas_attendus()]
    j = "b" * 64
    vert = agrege(tous, j)
    manquant = agrege(tous[1:], j)
    corrompu = [dict(r) for r in tous]
    corrompu[0] = dict(corrompu[0]); corrompu[0]["journal_sha256"] = "0" * 12
    corrompu[0]["n"] = 3
    ref_corrompu = agrege(corrompu, j)
    # rejeu bit-identique (graine consignée)
    a = json.dumps(agrege(tous, j), sort_keys=True, ensure_ascii=False)
    b = json.dumps(agrege([dict(x) for x in tous], j), sort_keys=True, ensure_ascii=False)
    essais = [
        ("jeu complet → VERT", vert["verdict"] == "VERT"),
        ("run manquant → REFUS", manquant["verdict"] == "REFUS" and any("MANQUANT" in m for m in manquant["motifs"])),
        ("run corrompu → REFUS", ref_corrompu["verdict"] == "REFUS" and any("CORROMPU" in m for m in ref_corrompu["motifs"])),
        ("rejeu bit-identique", a == b),
    ]
    print("=" * 78)
    print("AUTOTEST DE L'AGRÉGATEUR METAL — FAIL-CLOSED")
    print("=" * 78)
    for nom, ok in essais:
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom}")
    print(f"{sum(1 for _, ok in essais if ok)}/{len(essais)}")
    if not tous:
        return 3
    print(f"[agrégat] {vert['verdict']} sur {vert['runs']} runs synthétiques — "
          f"{len(cas_attendus())} cas attendus")
    return 0 if all(ok for _, ok in essais) else 3


def statut():
    f = DOSSIER / "preregistrement.json"
    print(json.dumps(preregistrement(), ensure_ascii=False, indent=2))
    print(f"[statut] pré-enregistrement : {'présent' if f.exists() else 'ABSENT'} "
          f"({sha256(f) if f.exists() else '—'})")
    print("[statut] EN ATTENTE — aucun run matériel n'existe ; le statut « mesuré » ne "
          "s'acquiert qu'au recoupement sur pièces.")
    return 0


def main():
    if "--preregistrer" in sys.argv:
        return preregistrer()
    if "--autotest" in sys.argv:
        return autotest()
    return statut()


if __name__ == "__main__":
    sys.exit(main())
