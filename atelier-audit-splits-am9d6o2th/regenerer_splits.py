#!/usr/bin/env python3
"""regenerer_splits.py — atelier AM9D6O2TH (la vague 16).

La réparation constatée : le corpus v2 est FUITE par contrat — dix contrats
partagés entre TRAIN et DEV/TEST (l'audit `auditer_splits.py`, code 3).
La cause : les splits furent tirés PAR INSTANCE DE TÂCHE ; or v3, v4 et v6
portent LE MÊME contrat — l'identifiant de contrat est l'unité d'étanchéité.

La règle réparée : GROUPE-DE-CONTRAT — les 18 contrats répartis 80/10/10 à la
graine consignée 20261126 (JAMAIS re-tirée), TRAIN 14 · DEV 2 · TEST 2.
Le TEST reste NU (validateurs seuls : ni `reponse` ni `verdict`) ; le canari
reste UNIQUE au TRAIN.

Déterministe : dix exécutions rendent dix jeux d'octets identiques.
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys

GRAINE = 20261126          # la graine consignée — jamais re-tirée
PROPORTION = (14, 2, 2)    # 18 contrats -> 80/10/10
RE_CONTRAT = re.compile(r"^(loupe-\d+|tls13-\d+|sys-\d+)\s*·", re.MULTILINE)
CLES_NUES = ("triple", "contrat", "bloc", "vague", "licence")


def contrat_id(enreg):
    m = RE_CONTRAT.search(enreg.get("contrat", ""))
    if m:
        return m.group(1)
    m = re.match(r"^((?:loupe|tls13|sys)-\d+)", enreg.get("bloc", ""))
    return m.group(1) if m else None


def charger(dataset):
    """Toutes les lignes du corpus v2, toutes campagnes confondues."""
    enregistrements = []
    for split in ("train", "dev", "test"):
        with open(os.path.join(dataset, f"{split}.jsonl"), encoding="utf-8") as f:
            for ligne in f:
                if ligne.strip():
                    e = json.loads(ligne)
                    e["_origine"] = split
                    enregistrements.append(e)
    return enregistrements


def repartir(contrats):
    """La répartition 80/10/10 à la graine consignée — l'ordre gelé."""
    rang = sorted(contrats)
    random.Random(GRAINE).shuffle(rang)
    n_tr, n_dev, n_test = PROPORTION
    assert n_tr + n_dev + n_test == len(rang), (n_tr + n_dev + n_test, len(rang))
    return (rang[:n_tr], rang[n_tr:n_tr + n_dev], rang[n_tr + n_dev:])


def ecrire(chemin, lignes):
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        for e in lignes:
            f.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")


def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, help="le corpus v2 publié (la source)")
    ap.add_argument("--sortie", required=True, help="le dossier du dataset corrigé")
    args = ap.parse_args()

    os.makedirs(args.sortie, exist_ok=True)
    tout = charger(args.dataset)

    canari = [e for e in tout if contrat_id(e) is None]
    par_contrat = {}
    for e in tout:
        c = contrat_id(e)
        if c:
            par_contrat.setdefault(c, []).append(e)

    train_c, dev_c, test_c = repartir(list(par_contrat))

    def prendre(contrats, nu=False):
        lignes = []
        for c in sorted(contrats):
            for e in sorted(par_contrat[c], key=lambda x: (x.get("vague", ""), x.get("triple", ""))):
                if nu:
                    e = {k: e[k] for k in CLES_NUES if k in e}
                else:
                    e = {k: v for k, v in e.items() if not k.startswith("_")}
                lignes.append(e)
        return lignes

    train = sorted(canari, key=lambda x: x.get("triple", "")) + prendre(train_c)
    dev = prendre(dev_c)
    test = prendre(test_c, nu=True)

    ecrire(os.path.join(args.sortie, "train.jsonl"), train)
    ecrire(os.path.join(args.sortie, "dev.jsonl"), dev)
    ecrire(os.path.join(args.sortie, "test.jsonl"), test)

    # le canari unique au TRAIN — la preuve, pas l'intention
    assert len(canari) == 1, f"le canari doit être UNIQUE, {len(canari)} trouvés"
    assert not any(contrat_id(e) is None for e in dev + test), "un canari hors du TRAIN"

    # l'étanchéité PAR CONTRAT — la preuve mécanique
    def contrats_de(lignes):
        return {contrat_id(e) for e in lignes if contrat_id(e)}

    ensembles = {"train": contrats_de(train), "dev": contrats_de(dev), "test": contrats_de(test)}
    fuites = []
    for a, b in (("train", "dev"), ("train", "test"), ("dev", "test")):
        communs = sorted(ensembles[a] & ensembles[b])
        if communs:
            fuites.append({"a": a, "b": b, "contrats": communs})
    assert not fuites, f"FUITE subsiste : {fuites}"

    # le TEST nu — aucune dorée
    for e in test:
        assert "reponse" not in e and "verdict" not in e, f"dorée au TEST : {e.get('triple')}"

    manifeste = {
        "schema": "TRIADE-CORPUS-v2.1",
        "correction": "les splits par GROUPE-DE-CONTRAT (l'unité : l'identifiant de contrat) — la fuite de dix contrats du v2 fermée",
        "graine": GRAINE,
        "proportion_contrats": {"train": PROPORTION[0], "dev": PROPORTION[1], "test": PROPORTION[2]},
        "fichiers": {n + ".jsonl": sha256(os.path.join(args.sortie, n + ".jsonl"))
                     for n in ("train", "dev", "test")},
        "vecteur_de_versions": {"protocole": "v0.23.3", "campagnes": ["v3", "v4", "v6"],
                                "graine": GRAINE},
        "canari": "UNIQUE au TRAIN",
    }
    with open(os.path.join(args.sortie, "MANIFESTE.json"), "w", encoding="utf-8") as f:
        json.dump(manifeste, f, ensure_ascii=False, indent=2)

    carte = {
        "nom": "TRIADE-CORPUS-v2.1",
        "provenance": "le corpus v2 (les 169 triples v3/v4/v6) aux splits réparés par groupe-de-contrat",
        "licence": "BSL-1.1 (le dépôt) ; le sous-ensemble permissif CC-BY-4.0 séparé",
        "splits_en_contrats": {"TRAIN": len(train_c), "DEV": len(dev_c), "TEST": len(test_c)},
        "splits_en_lignes": {"TRAIN": len(train), "DEV": len(dev), "TEST": len(test)},
        "continuite": "le TEST v2 demeure évaluable : aucun contrat du TEST ne vit au TRAIN — la continuité de l'ÉVALUATION est préservée, pas l'affectation",
        "canari": "la phrase unique au TRAIN (la sonde)",
        "ecart_nomme": "la version Zenodo (le corpus v2 au DOI 10.5281/zenodo.24463681) demeure IMMUAABLE ; la présente correction attend la commande du maître",
    }
    with open(os.path.join(args.sortie, "DATASET-CARD.json"), "w", encoding="utf-8") as f:
        json.dump(carte, f, ensure_ascii=False, indent=2)

    print("=== LA RÉGÉNÉRATION PAR GROUPE-DE-CONTRAT ===")
    print(f"  la graine consignée : {GRAINE} (jamais re-tirée)")
    print(f"  TRAIN : {len(train_c)} contrats · {len(train)} lignes (le canari unique)")
    print(f"  DEV   : {len(dev_c)} contrats · {len(dev)} lignes")
    print(f"  TEST  : {len(test_c)} contrats · {len(test)} lignes (NU — validateurs seuls)")
    print(f"  TEST  : {', '.join(sorted(test_c))}")
    print(f"  DEV   : {', '.join(sorted(dev_c))}")
    print("  l'étanchéité par contrat : AUCUNE fuite (la preuve mécanique)")
    for n in ("train", "dev", "test"):
        print(f"  sha256 {n}.jsonl : {manifeste['fichiers'][n + '.jsonl']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
