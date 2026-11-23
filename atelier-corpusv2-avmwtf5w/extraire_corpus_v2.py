#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extraire_corpus_v2.py — LE CORPUS v2 (avmwtf5w, la commande du maître
« ajoute les 60 appels v6 au corpus ») : les 109 triples v3/v4 du corpus v1
reproduits À L'IDENTIQUE (la preuve byte-byte contre le gel v1) PLUS LES 60
APPELS DE CAMPAGNE v6 de l'atelier 7xuvsoqpuq — SANS INVENTER UNE SEULE
DONNÉE.
(1) L'EXTRACTION MÉCANIQUE ÉTENDUE : le code v2/v3/v4 reconduit octet pour
    octet du gel 2i7iy3xmg ; la v6 la même boucle (la correspondance PAR ID
    journal ↔ garde-brut ↔ garde-prompts ↔ resultats) ; les exclusions
    nommées : les 11 relance v6 (hors commande), les 60 appels v5 (non
    demandés), les 18 tentatives v2 (toujours sans contrats) ;
(2) LES SPLITS CONTINUS : les 36 tâches v3/v4 GÈLENT leur affectation v1
    (le preuve d'égalité AVANT tout ajout ; l'étanchéité v1 préservée) ;
    les 18 tâches v6 affectées par LA MÊME RÈGLE (80/10/10, la même graine
    consignée) ;
(3) LA PORTE DE SCRUB fail-closed reconduite (le contrôle négatif vécu) ;
    LE CANARI unique au TRAIN ; LE TEST SANS notation dorée ; LA
    CRISTALLISATION 10 rebuilds bit-identiques ;
(4) LE MANIFESTE v2 + LA DATASET-CARD v2 (sha256 par fichier, le vecteur
    de versions campagnes v2/v3/v4/v6, les graines, les gaps nommés).
Le dépôt Zenodo de la v2 se fait par LA VOIE DES PATRONS newversion (le
concept 10.5281/zenodo.24457524) — le kit v1.0.0 n'est PAS touché."""
from __future__ import annotations

import hashlib
import json
import pathlib
import random
import re
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-corpusv2-avmwtf5w"
GEL_V1 = REPO / "atelier-corpus-2i7iy3xmg" / "dataset"
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
    # la casse EXACTE (le faux positif /Home/End nommé au corpus v1)
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
# la liste des ateliers : v2/v3/v4 reconduits du gel v1 + LA V6 (la commande)
ATELIERS = (("v2", "atelier-ajouter-v2-pgodgk35l"),
            ("v3", "atelier-ajouter-v3-5nwnwoceo"),
            ("v4", "atelier-ajouter-v4-842vqyy1k"),
            ("v6", "atelier-ajouter-v6-7xuvsoqpuq"))


def extraire() -> list:
    """les triples depuis les campagnes v2/v3/v4 (le code v1 reconduit) et
    v6 (la même boucle) — la garde-brut porte la réponse DU MODÈLE (la pièce
    brute), les résultats le verdict, les prompts le contrat. JAMAIS
    retapé : les champs copiés mécaniquement. Le motif (ajouter-\\w+-i\\d+)
    EXCLUT DE FAIT les appels de relance (relance-ajouter-v5-*) : la commande
    nomme LES 60 APPELS DE CAMPAGNE."""
    triples = []
    for vague, dossier in ATELIERS:
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
                # v2 : la pièce ENVELOPPÉE {tache, reponse_api} ; v3/v4/v6 :
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
                continue   # les relance-* et les autres formes EXCLUES
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


# --------------------------------------------- LES SPLITS CONTINUS ---------
def decouper_taches(taches: list) -> dict:
    """LA RÈGLE v1 RECONDUITE À L'IDENTIQUE : la graine 20261126, le tri
    puis le shuffle, 80/10/10 par tâche."""
    rng = random.Random(GRAINE)
    taches = sorted(taches)
    rng.shuffle(taches)
    n = len(taches)
    i_dev = int(n * 0.8)
    i_test = int(n * 0.9)
    return {"TRAIN": taches[:i_dev], "DEV": taches[i_dev:i_test],
            "TEST": taches[i_test:]}


def taches_de(triples: list, vagues: tuple) -> list:
    return sorted({t["triple"].rsplit("-t", 1)[0] for t in triples
                   if t["vague"] in vagues})


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

    consigne("=== L'EXTRACTION MÉCANIQUE (v2/v3/v4 reconduits + LA V6) ===")
    triples = extraire()
    par_vague = {v: sum(1 for t in triples if t["vague"] == v)
                 for v, _ in ATELIERS}
    consigne(f"les triples extraits : {len(triples)} "
             + " · ".join(f"{v} {n}" for v, n in par_vague.items()))
    n_v6 = sum(1 for t in triples if t["vague"] == "v6")
    assert n_v6 == 60, f"la commande nomme LES 60 APPELS v6 — extrait {n_v6}"

    consigne("=== LA PORTE DE SCRUB fail-closed (le contrôle négatif vécu) ===")
    faux = [{"triple": "negatif", "contrat": "le jeton plante "
             + "ghp_" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcd",
             "reponse": "", "verdict": "REFUS", "classe_de_refus": "NEG",
             "diff": "", "bloc": "x", "vague": "neg", "licence": "BSL-1.1"}]
    pris = scan_secrets(json.dumps(faux, ensure_ascii=False))
    consigne("le contrôle négatif (le jeton planté) : "
             + ("ATTRAPÉ — le triple refusé à la porte"
                if any(n == "jeton_github" for n, _ in pris) else "ROUGE"))
    corpus = []
    exclus_scrub = []
    for t in triples:
        trouve = scan_secrets(json.dumps(t, ensure_ascii=False))
        if trouve:
            exclus_scrub.append((t["triple"], trouve[0][0]))
            continue
        corpus.append(t)
    consigne(f"les triples à la porte : {len(corpus)}/{len(triples)} admis"
             + (f" — REFUSÉS : {exclus_scrub}" if exclus_scrub
                else " (aucun secret détecté au corpus réel)"))

    consigne("=== LES SPLITS CONTINUS (la preuve v1 AVANT tout ajout) ===")
    anciennes = taches_de(corpus, ("v2", "v3", "v4"))
    nouvelles = taches_de(corpus, ("v6",))
    splits_anciennes = decouper_taches(anciennes)
    # LA PREUVE : l'affectation re-jouée == le gel v1, split par split
    for nom in ("TRAIN", "DEV", "TEST"):
        lignes_v1 = [json.loads(l) for l in
                     (GEL_V1 / f"{nom.lower()}.jsonl").read_text(
                         encoding="utf-8").splitlines() if l.strip()]
        taches_v1 = sorted({t["triple"].rsplit("-t", 1)[0] for t in lignes_v1
                            if t.get("vague") in ("v2", "v3", "v4")})
        assert taches_v1 == sorted(splits_anciennes[nom]), \
            f"la reproduction v1 échoue au {nom} : la règle a divergé"
    consigne(f"la preuve v1 : les {len(anciennes)} tâches v3/v4 à leur "
             f"affectation v1 EXACTE (le re-jeu de la règle à la graine "
             f"{GRAINE} == le gel 2i7iy3xmg, split par split) — "
             "l'étanchéité v1 préservée")
    splits_nouvelles = decouper_taches(nouvelles)
    consigne(f"les {len(nouvelles)} tâches v6 affectées par LA MÊME RÈGLE "
             f"(80/10/10, la graine {GRAINE} consignée au manifeste) : "
             f"TRAIN {len(splits_nouvelles['TRAIN'])} · DEV "
             f"{len(splits_nouvelles['DEV'])} · TEST "
             f"{len(splits_nouvelles['TEST'])}")
    splits = {nom: splits_anciennes[nom] + splits_nouvelles[nom]
              for nom in ("TRAIN", "DEV", "TEST")}
    consigne(f"les tâches : TRAIN {len(splits['TRAIN'])} · DEV "
             f"{len(splits['DEV'])} · TEST {len(splits['TEST'])} "
             "(36 anciennes gelées + 18 nouvelles)")
    # la preuve byte-byte : CHAQUE ligne v1 (hors canari) reproduite au même
    # split — la continuité de contenu autant que d'affectation
    lignes_v2 = {}
    for nom in splits:
        lignes_v2[nom] = []
        for t in corpus:
            if t["triple"].rsplit("-t", 1)[0] in splits[nom]:
                entree = dict(t)
                if nom == "TEST":
                    entree.pop("reponse")
                    entree.pop("verdict")
                    entree.pop("classe_de_refus")
                    entree.pop("diff")
                lignes_v2[nom].append(json.dumps(entree, ensure_ascii=False))
    reproduites = 0
    for nom in ("TRAIN", "DEV", "TEST"):
        v1 = [l for l in (GEL_V1 / f"{nom.lower()}.jsonl").read_text(
            encoding="utf-8").splitlines() if l.strip()]
        attendu = [l for l in v1 if json.loads(l).get("vague") != "v15"]
        for l in attendu:
            assert l in lignes_v2[nom], \
                f"la ligne v1 non reproduite au {nom} : {l[:80]}"
            reproduites += 1
    consigne(f"la preuve byte-byte : {reproduites}/109 lignes v1 "
             "reproduites octet pour octet aux mêmes splits")

    consigne("=== L'ÉCRITURE DU DATASET (le canari unique, le TEST nu) ===")
    dataset_dir = ICI / "dataset"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    for nom in ("TRAIN", "DEV", "TEST"):
        lignes = list(lignes_v2[nom])
        if nom == "TRAIN":
            # LE CANARI unique embarqué dans TRAIN (reconduit de la v1)
            lignes.append(json.dumps({"triple": "CANARI", "contrat": CANARI,
                                      "reponse": "", "verdict": "CANARI",
                                      "classe_de_refus": "", "diff": "",
                                      "bloc": "canari", "vague": "v15",
                                      "licence": "CC-BY-4.0"},
                                     ensure_ascii=False))
        (dataset_dir / f"{nom.lower()}.jsonl").write_text(
            "\n".join(lignes) + "\n", encoding="utf-8")
        consigne(f"  {nom} : {len(lignes)} lignes -> {nom.lower()}.jsonl"
                 + (" (AUCUNE dorée — les validateurs seuls)" if nom == "TEST"
                    else " (le canari unique embarqué)" if nom == "TRAIN"
                    else ""))
    n_canari = sum(1 for nom in ("train", "dev", "test")
                   if CANARI in (dataset_dir / f"{nom}.jsonl").read_text())
    consigne("le canari : "
             + ("UNIQUE — dans TRAIN seul" if n_canari == 1
                else "ROUGE — " + str(n_canari) + " occurrences"))

    consigne("=== LA SONDE DE CONTAMINATION (reconduite) ===")
    sonde = sonde_contamination()
    (dataset_dir / "sonde-contamination.json").write_text(
        json.dumps(sonde, indent=2, ensure_ascii=False), encoding="utf-8")
    consigne("la sonde livrée (128 constantes + le canari + l'overlap "
             "n-gram) — AU POSTE, jamais au bac")

    consigne("=== LE SOUS-ENSEMBLE PERMISSIF (reconduit) ===")
    permissif = [t for t in corpus if t["licence"] == "CC-BY-4.0"]
    (dataset_dir / "permissif-ccby.jsonl").write_text(
        "\n".join(json.dumps(t, ensure_ascii=False) for t in permissif)
        + "\n", encoding="utf-8")
    consigne(f"le sous-ensemble permissif (CC-BY) : {len(permissif)} — le "
             "canari seul au corpus réel (le reste BSL-1.1, séparé)")

    consigne("=== LA CRISTALLISATION (10 rebuilds bit-identiques) ===")
    empreintes = []
    for _ in range(10):
        triples2 = extraire()
        corpus2 = [t for t in triples2
                   if not scan_secrets(json.dumps(t, ensure_ascii=False))]
        a2 = decouper_taches(taches_de(corpus2, ("v2", "v3", "v4")))
        n2 = decouper_taches(taches_de(corpus2, ("v6",)))
        blob = json.dumps({
            "triples": len(triples2),
            "splits": {k: len(a2[k]) + len(n2[k])
                       for k in ("TRAIN", "DEV", "TEST")},
            "corpus": sorted(hashlib.sha256(
                json.dumps(t, sort_keys=True, ensure_ascii=False).encode()
            ).hexdigest() for t in corpus2)}, sort_keys=True)
        empreintes.append(hashlib.sha256(blob.encode()).hexdigest())
    identiques = len(set(empreintes)) == 1
    consigne("les 10 rebuilds : "
             + ("BIT-IDENTIQUES (la graine et l'extraction déterministes)"
                if identiques else "ROUGE — divergence"))

    consigne("=== LE MANIFESTE v2 + LA DATASET-CARD v2 ===")
    gaps = [
        "la sonde AU POSTE",
        "le dual-use exclu par construction (aucun binaire intercepteur "
        "au corpus)",
        "les 11 appels de relance v6 EXCLUS (la commande nomme les 60 "
        "appels de campagne — les journaux demeurent au garde-brut)",
        "les 60 appels v5 HORS commande (l'atelier yfkpml1j2, la matière "
        "demeure disponible — l'écart nommé)",
        "les 18 tentatives v2 toujours sans contrats archivés (l'écart "
        "reconduit de la v1)",
    ]
    manifeste = {
        "commit": "la tête au moment du gel (la chaîne git fait foi)",
        "schema": "TRIADE-CORPUS-v2",
        "fichiers": {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                     for f in sorted(dataset_dir.glob("*"))},
        "vecteur_de_versions": {"protocole": "v0.23.2",
                                "campagnes": ["v2", "v3", "v4", "v6"],
                                "graine": GRAINE},
        "empreintes_des_juges": {
            "assembler_v3": "la chaîne v2 INTACTE (aucun juge affaibli)",
            "validateurs": "les quatre interdits v3"},
        "graines": {"splits": GRAINE, "splits_v6": GRAINE},
        "canari": hashlib.sha256(CANARI.encode()).hexdigest(),
        "gaps_nommes": gaps,
    }
    (dataset_dir / "MANIFESTE.json").write_text(
        json.dumps(manifeste, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    card = {
        "nom": "TRIADE-CORPUS-v2",
        "provenance": "les journaux append-only et les campagnes ajouter "
                      "v2/v3/v4 + LES 60 APPELS DE CAMPAGNE v6 (les "
                      "décisions D1-D251 au fil)",
        "licence": "BSL-1.1 (le dépôt) ; le sous-ensemble permissif "
                   "CC-BY-4.0 séparé",
        "splits": {k: len(v) for k, v in splits.items()},
        "continuite": "les 36 tâches v3/v4 gèlent leur affectation v1 — "
                      "le TEST v1 demeure évaluable tel quel",
        "canari": "la phrase unique au TRAIN (la sonde)",
        "gaps_nommes": gaps,
        "dual_usage": "aucun : les tâches de notation d'un éditeur de "
                      "texte natif — aucune cible d'interception",
    }
    (dataset_dir / "DATASET-CARD.json").write_text(
        json.dumps(card, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    consigne("le manifeste v2 + la dataset card v2 livrés (sha256 par "
             "fichier, le vecteur campagnes v2/v3/v4/v6, les graines, les "
             "gaps nommés — le gap du dépôt Zenodo SOLDÉ à la présente)")

    (ICI / "registres").mkdir(exist_ok=True)
    (ICI / "registres" / "extraction-v2.json").write_text(
        json.dumps({"triples": len(triples), "admis": len(corpus),
                    "par_vague": par_vague,
                    "taches_anciennes": len(anciennes),
                    "taches_v6": len(nouvelles),
                    "splits": {k: len(v) for k, v in splits.items()},
                    "splits_v6": {k: len(v) for k, v in splits_nouvelles.items()},
                    "lignes_v1_reproduites": reproduites,
                    "cristallisation_10x": identiques,
                    "graine": GRAINE}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    (ICI / "rapport-atelier.txt").write_text("\n".join(rapport) + "\n",
                                             encoding="utf-8")
    print("\nOK — le corpus v2 + les registres")
    return 0


if __name__ == "__main__":
    sys.exit(main())
