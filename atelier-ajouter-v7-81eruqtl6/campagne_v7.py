#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_v7.py — TPL-ADD-v7 (81eruqtl6, la campagne du DÉCODAGE
CONTRAINT) : LA ROUTE RESTANTE de la voie nommée (dite « campagne v6 à
la commande » aux SUITE 390/391 — l'atelier v6 [7xuvsoqpuq] ayant déjà
couru la relance et la paire contrastive, la présente porte v7, l'écart
de numérotation NOMMÉ au plan).

LE LEVIER : le décodage contraint PAR LE SDK (le CLI n'expose pas
response_format — l'écart nommé aux rapports v5/v6 ; le SDK 0.0.18
laisse passer le champ : la sonde P1-P3 a tranché au guichet AVANT la
présente). LE SCHÉMA PAR TÂCHE construit DEPUIS LES CANONS
(motif_schema.py) : les formes de ligne du juge, les IDs ÉNUMÉRÉS du
dictionnaire du bloc — HORS-FORMAT (les préfixes de chaîne, les db
inline, la prose) et ID-INCONNU IMPOSSIBLES AU DÉCODEUR.

LES MÊMES 18 TÂCHES (l'ordre JAMAIS re-tiré), graines 20261117
reconduites (la construction déterministe), budget 3, LES JUGES INTACTS
(assembler_v3 — la chaîne v2 + les validateurs v3 ; le normalisateur
canonique v5 reconduit ; le prompt v6 reconduit octet pour octet + LA
NOTE D'ÉMISSION du wrap, INSÉPARABLE du levier). CE QUE LA CONTRAINTE
NE COUVRE PAS : EXPANSION-DIVERGENTE et FORME-INVALIDE demeurent AU
JUGE (nommé au plan)."""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[1]
V6 = REPO / "atelier-ajouter-v6-7xuvsoqpuq"
V5 = REPO / "atelier-ajouter-v5-yfkpml1j2"
ICI = pathlib.Path(__file__).resolve().parent
PONT = ICI / "appel_contraint.js"
JOURNAL = ICI / "journal_v7.jsonl"
RESULTATS = ICI / "resultats_v7.jsonl"
GARDE = ICI / "garde-brut-v7.jsonl"
GUICHET = ICI / "registres" / "guichet.txt"
BUDGET = 3
BLOCS = ["loupe-07-cumul", "loupe-11-defilement", "loupe-02-lire",
         "loupe-12-aller", "loupe-03-fermer", "loupe-10-peinture",
         "loupe-09-ecran", "loupe-17-sauver", "loupe-16-saisie",
         "loupe-13-recherche", "loupe-14-suivant", "loupe-18-quitter",
         "loupe-06-md5", "loupe-15-curseur", "loupe-04-cadre",
         "loupe-08-ligne", "loupe-01-ouvrir", "loupe-05-sha256"]

sys.path.insert(0, str(ICI))
from motif_schema import schema_corps                              # noqa: E402
sys.path.insert(0, str(V6))
from campagne_v6 import prompt_ajouter_v6                          # noqa: E402
sys.path.insert(0, str(V5))
from campagne_v5 import normaliser, prompt_reparation_v5           # noqa: E402
sys.path.insert(0, str(REPO / "atelier-ajouter-v3-5nwnwoceo"))
from client_v3 import assembler_v3                                 # noqa: E402
from client_v2 import construire_dictionnaire                      # noqa: E402
from client_gabarits import Refus                                  # noqa: E402

# LA NOTE D'ÉMISSION — la même qu'à la sonde P3 (le wrap est INSÉPARABLE
# du levier : la contrainte exige l'objet à un champ, la note le DIT)
NOTE_EMISSION = (
    "\nLA FORME D'ÉMISSION (le schéma est IMPOSÉ AU DÉCODEUR — l'objet "
    "JSON à UN champ) : émets UNIQUEMENT l'objet "
    "{\"corps\": [\"ligne 1\", \"ligne 2\", …]} — le TABLEAU des lignes "
    "de la logique, une chaîne par ligne, RIEN D'AUTRE hors l'objet.\n")
MARQUEUR = "REQUÊTE : écris UNIQUEMENT LES LIGNES DE LA LOGIQUE"


def prompt_ajouter_v7(nom_bloc: str) -> tuple:
    """LE PROMPT v7 = le v6 (octet pour octet — la grammaire, l'exemplaire
    scellé, le squelette à trous typés, la note du normalisateur, LA PAIRE
    CONTRASTIVE du corpus) + LA NOTE D'ÉMISSION du wrap."""
    prompt_v6, meta = prompt_ajouter_v6(nom_bloc)
    assert MARQUEUR in prompt_v6, "le marqueur du prompt v6 a bougé"
    prompt = prompt_v6.replace(MARQUEUR, NOTE_EMISSION + "\n" + MARQUEUR, 1)
    meta = dict(meta)
    meta["leviers"] = list(meta.get("leviers", [])) + ["decodage-contraint"]
    return prompt, meta


# --------------------------------------------------------------- L'APPEL ----
def appeler_et_compter(tache, essai, prompt, schema, phase="campagne"):
    """L'APPEL PAR LE PONT SDK avec response_format (l'instrument que le
    CLI n'expose pas) ; la réponse complète au garde-brut, l'entrée au
    journal (le champ instrument CONSIGNÉ)."""
    d = ICI / f"tmp-{tache}-{essai}"
    d.mkdir(exist_ok=True)
    pf = d / "prompt.txt"
    pf.write_text(prompt, encoding="utf-8")
    sf = d / "schema.json"
    sf.write_text(json.dumps({"type": "json_schema",
                              "json_schema": schema}, ensure_ascii=False),
                  encoding="utf-8")
    out = d / "reponse.json"
    t0 = time.monotonic()
    r = subprocess.run(["bun", str(PONT), str(pf), str(sf), str(out)],
                       capture_output=True, text=True, timeout=900)
    dt = time.monotonic() - t0
    if r.returncode != 0 or not out.exists():
        raise RuntimeError(f"APPEL ÉCHEC : {(r.stderr or '')[:200]}")
    rep = json.loads(out.read_text())
    out.unlink()
    pf.unlink()
    sf.unlink()
    try:
        d.rmdir()
    except OSError:
        pass
    usage = rep.get("usage", {})
    contenu = rep["choices"][0]["message"]["content"]
    with open(GARDE, "a") as f:
        f.write(json.dumps(rep, ensure_ascii=False) + "\n")
    with open(JOURNAL, "a") as f:
        f.write(json.dumps({
            "tache": tache, "essai": essai, "phase": phase,
            "verdict": "APPEL",
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "secondes": round(dt, 1), "source": "log-api",
            "id": rep.get("id", ""), "modele": rep.get("model", ""),
            "instrument": "sdk-response_format-json_schema"},
            ensure_ascii=False) + "\n")
    return contenu, usage.get("total_tokens", 0)


def extraire_corps(contenu: str) -> str:
    """L'ÉMISSION SOUS CONTRAINTE → le corps texte : l'objet {"corps":
    [lignes]} exigé ; une émission hors la contrainte (non-JSON, corps
    absent, pas un tableau) = REFUS HORS-FORMAT NOMMÉ, l'essai consommé
    (la contrainte est au décodeur, le contrôle au retour EST AUSSI au
    juge — jamais un juge affaibli)."""
    try:
        o = json.loads(contenu)
        corps = o["corps"]
        assert isinstance(corps, list) and corps, "corps vide ou absent"
        assert all(isinstance(x, str) for x in corps), "pas des chaînes"
    except Exception as e:
        raise Refus("HORS-FORMAT",
                    f"l'émission n'est pas l'objet JSON {{\"corps\": "
                    f"[…]}} exigé par la contrainte ({type(e).__name__})")
    return "\n".join(corps)


# ------------------------------------------------- LA BOUCLE D'UNE TÂCHE ----
def boucle_tache(tache: str, bid: str, prompt, meta, phase="campagne") -> dict:
    """LA MÊME BOUCLE que la v6 : émettre → extraire le corps → normaliser
    → assembler (LE JUGE INTACT) → la réparation ciblée au refus nommé,
    budget 3."""
    squelette = meta.get("squelette", "")
    dico = construire_dictionnaire(bid)
    schema = schema_corps(meta.get("dico") or dico)
    logique, refus = None, ("", "")
    journaux = []
    for essai in range(BUDGET + 1):
        p = prompt if essai == 0 else prompt_reparation_v5(
            prompt, logique or "", refus[0], refus[1], essai, dico)
        (ICI / "garde-prompts").mkdir(exist_ok=True)
        (ICI / "garde-prompts" / f"{tache}-t{essai}.txt").write_text(p)
        contenu, total = appeler_et_compter(tache, essai, p, schema, phase)
        journaux.append({"essai": essai, "total": total})
        try:
            corps = extraire_corps(contenu)
            refus = ("", "")
        except Refus as e:
            refus = (e.args[0],
                     str(e.args[1])[:400] if len(e.args) > 1 else "")
            logique = contenu
            continue
        canonique = normaliser(corps)
        try:
            assembler_v3(squelette, canonique, meta)
            return {"tache": tache, "bloc": bid, "vert": True,
                    "essais": essai + 1, "journaux": journaux,
                    "verdict": "VERT", "phase": phase}
        except Refus as e:
            refus = (e.args[0],
                     str(e.args[1])[:400] if len(e.args) > 1 else "")
            logique = canonique
        except Exception as e:
            refus = (type(e).__name__, str(e)[:400])
            logique = canonique
    return {"tache": tache, "bloc": bid, "vert": False,
            "essais": BUDGET + 1, "journaux": journaux,
            "verdict": f"REFUS {refus[0]}", "phase": phase}


# ------------------------------------------------------- LA CAMPAGNE 18 ----
def campagne() -> int:
    print("=== LA CAMPAGNE v7 : LES 18 TÂCHES, le décodage contraint au "
          "SDK ===", flush=True)
    fait = {}
    if RESULTATS.exists():
        for l in RESULTATS.read_text().splitlines():
            if l.strip():
                d = json.loads(l)
                fait[d["tache"]] = d
    for i, bid in enumerate(BLOCS):
        tache = f"ajouter-v7-i261117{i+1:02d}"
        if tache in fait:
            continue
        prompt, meta = prompt_ajouter_v7(bid)
        r = boucle_tache(tache, bid, prompt, meta, phase="campagne")
        with open(RESULTATS, "a") as f:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"  {tache} ({bid}) : {r['verdict']}", flush=True)
        time.sleep(15)
    verts = [json.loads(l) for l in RESULTATS.read_text().splitlines()
             if l.strip()]
    nb = sum(1 for v in verts if v["vert"])
    couts = sorted(sum(j["total"] for j in v["journaux"])
                   for v in verts if v["vert"])
    med = couts[len(couts) // 2] if couts else 0
    print(f"[fin] AJOUTER v7 {nb}/{len(verts)} verts ; coût médian par "
          f"changement validé {med} natifs ; cible ≥15/18 ET ≤4500",
          flush=True)
    return 0


def main() -> int:
    print("=== TPL-ADD-v7 (81eruqtl6) : le décodage contraint — la route",
          "restante de la voie nommée ===", flush=True)
    if not GUICHET.exists() or "PASSER" not in GUICHET.read_text():
        raise SystemExit("REFUS NOMMÉ : le guichet d'instrument n'a pas "
                         "tranché PASSER (sondes_instrument.py d'abord — "
                         "jamais une mesure habillée en contrainte)")
    print("  le guichet : PASSER (P2 ET P3 verts — le levier vit au "
          "décodeur)", flush=True)
    campagne()
    return 0


if __name__ == "__main__":
    sys.exit(main())
