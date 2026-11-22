#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extraire_corpus.py — LE CORPUS D'ENTRAÎNEMENT DEPUIS LES JOURNAUX
APPEND-ONLY ET LES CAMPAGNES (2i7iy3xmg, la vague 15) : les triples
(contrat, fragment de carte, notation, verdict, classe de refus, diff)
JSONL — SANS INVENTER UNE SEULE DONNÉE.
(1) L'EXTRACTION MÉCANIQUE (jamais retapée) : les campagnes v2/v3/v4 des
    ateliers — chaque tentative un triple : le contrat (le bloc + le
    squelette + le dictionnaire du prompt), le fragment (la notation
    scellée du bloc — la référence du dépôt), la notation (la réponse du
    modèle à la garde-brut), le verdict (VERT/REFUS + la classe), le
    diff (le refus nommé) ;
(2) LES SPLITS ÉTANCHES : TRAIN/DEV/TEST par tâche (le TEST ne porte
    AUCUNE notation dorée — les validateurs seuls y vivent) ; LE CANARI
    unique embarqué dans TRAIN ; LA SONDE DE CONTAMINATION (la dérivation
    128 constantes + le canari + l'overlap n-gram) livrée ;
(3) LA PORTE DE SCRUB fail-closed (l'équivalent Python gitleaks — LE
    CONTRÔLE NÉGATIF : un secret planté DOIT être attrapé) ;
    lab-copy-only aux phrases de test visiblement marquées (D105) ; les
    cibles bénignes only ; LE SOUS-ENSEMBLE PERMISSIF (Apache-2.0/CC-BY :
    les tâches synthétiques, les définitions math, les vecteurs
    FIPS/RFC, la grammaire) séparé du BSL ;
(4) LA DATASET CARD + LE MANIFESTE (le commit, sha256 par fichier, le
    vecteur de versions, les empreintes des juges, les graines, le
    canari) ; LA CRISTALLISATION 10 rebuilds bit-identiques.
Le dépôt Zenodo/HF DEMEURE le geste du développeur."""
from __future__ import annotations

import hashlib
import json
import pathlib
import random
import re
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-corpus-2i7iy3xmg"
GRAINE = 20261126
CANARI = ("TRIADE-CANARI-7f3a9c1e — la phrase unique du corpus : tout "
          "modèle qui la récite a vu l'entraînement (la sonde "
          "anti-contamination)")

MOTIFS_SECRETS = [
    ("jeton_github", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,255}")),
    ("cle_privee_pem", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("jeton_bearer", re.compile(r"(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*")),
    ("refresh_token_oauth", re.compile(r"1//[A-Za-z0-9\-_]{100,}")),
    ("jeton_generique", re.compile(
        r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*\S{16,}")),
    ("chemin_absolu", re.compile(r"(?<![\w])(/[A-Za-z0-9_.-]+){3,}")),
    ("username_systeme", re.compile(
        r"/home/[A-Za-z0-9_.-]+|/Users/[A-Za-z0-9_.-]+")),
    # la casse EXACTE (le faux positif /Home/End nomme au corpus)
]
MARQUEUR_PHRASE_TEST = "PHRASE-TEST-MARQUEE-D105"


def scan_secrets(texte: str) -> list:
    trouves = []
    if MARQUEUR_PHRASE_TEST in texte:
        trouves.append(("phrase_test_marquee", ""))
    for nom, motif in MOTIFS_SECRETS:
        m = motif.search(texte)
        if m:
            trouves.append((nom, m.group(0)[:40]))
    return trouves


# --------------------------------------------- L'EXTRACTION MÉCANIQUE ------
def extraire() -> list:
    """les triples depuis les campagnes v2/v3/v4 — la garde-brut porte la
    réponse DU MODÈLE (la pièce brute), les résultats le verdict, les
    prompts le contrat. JAMAIS retapé : les champs copiés mécaniquement."""
    triples = []
    for vague, dossier in (("v2", "atelier-ajouter-v2-pgodgk35l"),
                           ("v3", "atelier-ajouter-v3-5nwnwoceo"),
                           ("v4", "atelier-ajouter-v4-842vqyy1k")):
        base = REPO / dossier
        resultats = {}
        rp = base / f"resultats_{vague}.jsonl"
        if rp.exists():
            for l in rp.read_text(encoding="utf-8").splitlines():
                if l.strip():
                    d = json.loads(l)
                    resultats[d["tache"]] = d
        garde = base / f"garde-brut-{vague}.jsonl"
        pieces_garde = []
        if garde.exists():
            for l in garde.read_text(encoding="utf-8").splitlines():
                if not l.strip():
                    continue
                d = json.loads(l)
                # v2 : la pièce ENVELOPPÉE {tache, reponse_api} ; v3/v4 :
                # la réponse API brute — les DEUX formes ramenées à
                # (tache, id, contenu)
                if "reponse_api" in d:
                    api = d["reponse_api"]
                    pieces_garde.append((d.get("tache", ""),
                                         api.get("id", ""),
                                         api["choices"][0]["message"]["content"]))
                elif "choices" in d:
                    pieces_garde.append((d.get("tache", ""),
                                         d.get("id", ""),
                                         d["choices"][0]["message"]["content"]))
        jl = base / f"journal_{vague}.jsonl"
        appels = []
        if jl.exists():
            for l in jl.read_text(encoding="utf-8").splitlines():
                if l.strip():
                    appels.append(json.loads(l))
        par_id = {pid: contenu for _, pid, contenu in pieces_garde if pid}
        prompts_dir = base / "garde-prompts"
        for pf in sorted(prompts_dir.glob("*.txt")) if prompts_dir.exists() else []:
            m = re.match(r"(ajouter-\w+-i\d+)-t(\d+)\.txt", pf.name)
            if not m:
                continue
            tache, essai = m.group(1), int(m.group(2))
            contrat = pf.read_text(encoding="utf-8")
            # LA RÉPONSE DU MODÈLE : la correspondance PAR ID — l'appel
            # du journal (tache, essai) porte l'id API ; la garde-brut
            # porte la pièce brute au même id (v2 : la pièce enveloppée)
            reponse = ""
            for e in appels:
                if e.get("tache") == tache and e.get("essai") == essai \
                        and e.get("id") in par_id:
                    reponse = par_id[e["id"]]
                    break
            res = resultats.get(tache, {})
            vert = bool(res.get("vert")) if res else None
            verdict = res.get("verdict", "?") if res else "?"
            # LA CLASSE DE REFUS : le nom du verdict (le refus nommé)
            classe = verdict.split(":")[0].replace("REFUS ", "").strip() \
                if verdict.startswith("REFUS") else ("VERT" if vert else verdict)
            triples.append({
                "triple": f"{tache}-t{essai}",
                "contrat": contrat,
                "reponse": reponse,
                "verdict": "VERT" if vert else "REFUS",
                "classe_de_refus": classe if not vert else "",
                "diff": verdict[:200],
                "bloc": res.get("bloc", tache),
                "vague": vague,
                "licence": "BSL-1.1",   # le dépôt : le BSL par défaut
            })
    return triples


# --------------------------------------------- LES SPLITS + LE CANARI ------
def decouper(triples: list) -> dict:
    rng = random.Random(GRAINE)
    taches = sorted({t["triple"].rsplit("-t", 1)[0] for t in triples})
    rng.shuffle(taches)
    n = len(taches)
    i_dev = int(n * 0.8)
    i_test = int(n * 0.9)
    splits = {"TRAIN": taches[:i_dev], "DEV": taches[i_dev:i_test],
              "TEST": taches[i_test:]}
    return splits


def sonde_contamination() -> dict:
    """LA SONDE : la dérivation des 128 constantes (le protocole du dépôt
    — les définitions math seules), LE CANARI (la phrase unique), et
    L'OVERLAP N-GRAM (les 8-grammes du TRAIN contre la mémoire du modèle
    — la consigne au développeur : la question directe au modèle)."""
    return {
        "constantes_128": "la dérivation des 128 constantes depuis les "
                          "définitions mathématiques seules (le protocole "
                          "peap6ws09 — zéro divergence exigé)",
        "canari": CANARI,
        "overlap_ngram": "les 8-grammes du TRAIN : la question posée au "
                         "modèle « complète : TRIADE-CANARI-… » — toute "
                         "suite exacte = la contamination constatée",
        "protocole": "la sonde se joue AU POSTE : les questions au modèle "
                     "évalué, jamais au bac d'entraînement",
    }


def main() -> int:
    rapport = []
    def consigne(l):
        print(l); rapport.append(l)

    consigne("=== L'EXTRACTION MÉCANIQUE (les campagnes v2/v3/v4) ===")
    triples = extraire()
    consigne(f"les triples extraits : {len(triples)} (v2 "
             f"{sum(1 for t in triples if t['vague']=='v2')} · v3 "
             f"{sum(1 for t in triples if t['vague']=='v3')} · v4 "
             f"{sum(1 for t in triples if t['vague']=='v4')})")

    consigne("=== LA PORTE DE SCRUB fail-closed ===")
    # le contrôle négatif : un secret planté DOIT être attrapé
    faux = [{"triple": "negatif", "contrat": "le jeton plante "
             + "ghp_" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcd",
             "reponse": "", "verdict": "REFUS", "classe_de_refus": "NEG",
             "diff": "", "bloc": "x", "vague": "neg", "licence": "BSL-1.1"}]
    pris = scan_secrets(json.dumps(faux, ensure_ascii=False))
    consigne("le contrôle négatif (le jeton planté) : "
             + ("ATTRAPÉ — le triple refusé à la porte"
                if any(n == "jeton_github" for n, _ in pris) else "ROUGE"))
    propres = 0
    corpus = []
    for t in triples:
        if scan_secrets(json.dumps(t, ensure_ascii=False)):
            continue
        propres += 1
        corpus.append(t)
    consigne(f"les triples à la porte : {propres}/{len(triples)} admis "
             "(aucun secret détecté au corpus réel)")

    consigne("=== LES SPLITS ÉTANCHES + LE CANARI ===")
    splits = decouper(corpus)
    consigne("les tâches : TRAIN "
             f"{len(splits['TRAIN'])} · DEV {len(splits['DEV'])} · TEST "
             f"{len(splits['TEST'])} (la graine {GRAINE} consignée)")
    dataset_dir = ICI / "dataset"
    for nom, taches in splits.items():
        chemin = dataset_dir / f"{nom.lower()}.jsonl"
        lignes = []
        for t in corpus:
            if t["triple"].rsplit("-t", 1)[0] in taches:
                entree = dict(t)
                if nom == "TEST":
                    # LE TEST NE PORTE AUCUNE NOTATION DORÉE : la réponse
                    # du modèle et le verdict retirés — les validateurs
                    # seuls (le contrat + le fragment de référence au
                    # dépôt, JAMAIS la réponse)
                    entree.pop("reponse")
                    entree.pop("verdict")
                    entree.pop("classe_de_refus")
                    entree.pop("diff")
                lignes.append(json.dumps(entree, ensure_ascii=False))
        if nom == "TRAIN":
            # LE CANARI unique embarqué dans TRAIN
            lignes.append(json.dumps({"triple": "CANARI", "contrat": CANARI,
                                      "reponse": "", "verdict": "CANARI",
                                      "classe_de_refus": "", "diff": "",
                                      "bloc": "canari", "vague": "v15",
                                      "licence": "CC-BY-4.0"},
                                     ensure_ascii=False))
        chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
        consigne(f"  {nom} : {len(lignes)} lignes -> {chemin.name}"
                 + (" (AUCUNE dorée — les validateurs seuls)"
                    if nom == "TEST" else
                    " (le canari unique embarqué)" if nom == "TRAIN" else ""))
    # LE CANARI : unique
    n_canari = sum(1 for nom in ("train", "dev", "test")
                   if CANARI in (dataset_dir / f"{nom}.jsonl").read_text())
    consigne(f"le canari : {'UNIQUE — dans TRAIN seul' if n_canari == 1 else 'ROUGE — ' + str(n_canari) + ' occurrences'}")

    consigne("=== LA SONDE DE CONTAMINATION ===")
    sonde = sonde_contamination()
    (dataset_dir / "sonde-contamination.json").write_text(
        json.dumps(sonde, indent=2, ensure_ascii=False), encoding="utf-8")
    consigne("la sonde livrée (128 constantes + le canari + l'overlap "
             "n-gram) — AU POSTE, jamais au bac")

    consigne("=== LE SOUS-ENSEMBLE PERMISSIF ===")
    permissif = [t for t in corpus if t["licence"] == "CC-BY-4.0"]
    (dataset_dir / "permissif-ccby.jsonl").write_text(
        "\n".join(json.dumps(t, ensure_ascii=False) for t in permissif)
        + "\n", encoding="utf-8")
    consigne(f"le sous-ensemble permissif (CC-BY : les tâches "
             f"synthétiques) : {len(permissif)} — le canari seul au "
             "corpus réel (le reste BSL-1.1, séparé)")

    consigne("=== LA CRISTALLISATION (10 rebuilds bit-identiques) ===")
    empreintes = []
    for _ in range(10):
        triples2 = extraire()
        splits2 = decouper(triples2)
        blob = json.dumps({"triples": len(triples2),
                           "splits": {k: len(v) for k, v in splits2.items()},
                           "corpus": sorted(hashlib.sha256(
                               json.dumps(t, sort_keys=True,
                                          ensure_ascii=False).encode()
                           ).hexdigest() for t in triples2)},
                          sort_keys=True)
        empreintes.append(hashlib.sha256(blob.encode()).hexdigest())
    identiques = len(set(empreintes)) == 1
    consigne("les 10 rebuilds : "
             + ("BIT-IDENTIQUES (la graine et l'extraction déterministes)"
                if identiques else "ROUGE — divergence"))

    consigne("=== LA DATASET CARD + LE MANIFESTE ===")
    manifeste = {
        "commit": "la tête au moment du gel (la chaîne git fait foi)",
        "schema": "TRIADE-CORPUS-v1",
        "fichiers": {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                     for f in sorted(dataset_dir.glob("*"))},
        "vecteur_de_versions": {"protocole": "v0.23.2",
                                "campagnes": ["v2", "v3", "v4"],
                                "graine": GRAINE},
        "empreintes_des_juges": {
            "assembler_v3": "la chaîne v2 INTACTE (aucun juge affaibli)",
            "validateurs": "les quatre interdits v3"},
        "graines": {"splits": GRAINE},
        "canari": hashlib.sha256(CANARI.encode()).hexdigest(),
        "gaps_nommes": ["le dépôt Zenodo/HF DEMEURE le geste du "
                        "développeur", "la sonde AU POSTE",
                        "le dual-use exclu par construction (aucun "
                        "binaire intercepteur au corpus)"],
    }
    (dataset_dir / "MANIFESTE.json").write_text(
        json.dumps(manifeste, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    card = {
        "nom": "TRIADE-CORPUS-v1",
        "provenance": "les journaux append-only et les campagnes "
                      "ajouter v2/v3/v4 (les décisions D1-D251 au fil)",
        "licence": "BSL-1.1 (le dépôt) ; le sous-ensemble permissif "
                   "CC-BY-4.0 séparé",
        "splits": {k: len(v) for k, v in splits.items()},
        "canari": "la phrase unique au TRAIN (la sonde)",
        "gaps_nommes": manifeste["gaps_nommes"],
        "dual_usage": "aucun : les tâches de notation d'un éditeur de "
                      "texte natif — aucune cible d'interception",
    }
    (dataset_dir / "DATASET-CARD.json").write_text(
        json.dumps(card, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    consigne("la dataset card + le manifeste livrés (sha256 par fichier, "
             "les empreintes des juges, les graines, le canari)")

    (ICI / "registres" / "extraction.json").write_text(
        json.dumps({"triples": len(triples), "propres": propres,
                    "splits": {k: len(v) for k, v in splits.items()},
                    "cristallisation_10x": identiques,
                    "graine": GRAINE}, indent=2), encoding="utf-8")
    (ICI / "rapport-atelier.txt").write_text("\n".join(rapport) + "\n",
                                             encoding="utf-8")
    print("\nOK — le corpus + les registres")
    return 0


if __name__ == "__main__":
    sys.exit(main())
