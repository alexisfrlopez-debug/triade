#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sondes_instrument.py — LE GUICHET DE LA CAMPAGNE DU DÉCODAGE CONTRAINT
(81eruqtl6) : TROIS sondes par le SDK (bun, appel_contraint.js), AVANT
toute donnée de campagne — la règle : jamais une mesure habillée en
contrainte, le guichet tranche d'abord.

  P1 ACCEPTÉ       — response_format json_object : l'endpoint l'accepte
                     (HTTP 200) ou le rejette (400) ?
  P2 CONTRAINTE    — json_schema STRICT à un champ forcé (enum d'une
     RÉELLE          valeur « ok ») avec un prompt qui ORDONNE la
                     violation (« réponds exactement {"mot": "banane"} »)
                     — la contrainte est HONORÉE au décodeur ssi la
                     sortie rend la valeur forcée, JAMAIS « banane » ;
                     accepté-mais-ignoré = l'écart le pire (silencieux).
  P3 LA FORME      — le schéma PAR TÂCHE (motif_schema.schema_corps) sur
     TPL-ADD         le contrat d'un bloc réel (loupe-01-ouvrir) : le
                     schéma à motif vit-il (pas de 400 au pattern), la
                     forme sort-elle (le tableau des lignes au motif) ?

LE GUiCHET : P2 ET P3 VERTS → la campagne courue (campagne_v7.py) ;
P2 ou P3 ROUGE → LA CAMPAGNE N'EST PAS COURUE, l'écart d'instrument
nommé (le CLI ET le SDK/backend), aucune donnée de campagne."""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
PONT = ICI / "appel_contraint.js"
SONDES = ICI / "registres" / "probes-instrument.jsonl"
GARDE = ICI / "garde-brut-v7.jsonl"
GUICHET = ICI / "registres" / "guichet.txt"

sys.path.insert(0, str(ICI))
from motif_schema import schema_corps                          # noqa: E402
sys.path.insert(0, str(REPO / "atelier-ajouter-v6-7xuvsoqpuq"))
from campagne_v6 import prompt_ajouter_v6                      # noqa: E402
sys.path.insert(0, str(REPO / "atelier-ajouter-v5-yfkpml1j2"))
from campagne_v5 import normaliser                             # noqa: E402
sys.path.insert(0, str(REPO / "atelier-ajouter-v3-5nwnwoceo"))


def appeler(nom: str, prompt: str, response_format: dict | None) -> dict:
    """UNE SONDE par le pont SDK ; la réponse complète au garde-brut,
    l'entrée synthétique au registre des sondes."""
    d = ICI / f"tmp-sonde-{nom}"
    d.mkdir(exist_ok=True)
    pf = d / "prompt.txt"
    pf.write_text(prompt, encoding="utf-8")
    sf = None
    if response_format is not None:
        sf = d / "schema.json"
        sf.write_text(json.dumps(response_format, ensure_ascii=False),
                      encoding="utf-8")
    out = d / "reponse.json"
    t0 = time.monotonic()
    r = subprocess.run(["bun", str(PONT), str(pf),
                        str(sf) if sf else "-", str(out)],
                       capture_output=True, text=True, timeout=900)
    dt = time.monotonic() - t0
    entree = {"sonde": nom,
              "prompt_sha256": hashlib.sha256(
                  prompt.encode()).hexdigest(),
              "response_format": response_format,
              "secondes": round(dt, 1), "retour": r.returncode}
    if r.returncode != 0 or not out.exists():
        entree["erreur"] = (r.stderr or "")[:600]
        with open(SONDES, "a") as f:
            f.write(json.dumps(entree, ensure_ascii=False) + "\n")
        return entree
    rep = json.loads(out.read_text())
    with open(GARDE, "a") as f:
        f.write(json.dumps(rep, ensure_ascii=False) + "\n")
    entree["id"] = rep.get("id", "")
    entree["modele"] = rep.get("model", "")
    entree["usage"] = rep.get("usage", {})
    entree["contenu"] = rep["choices"][0]["message"]["content"]
    with open(SONDES, "a") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    out.unlink()
    return entree


def p1() -> tuple[bool, str]:
    """P1 ACCEPTÉ : json_object passé au SDK — 200 ou 400 ?"""
    e = appeler("P1-json_object",
                "Réponds en une phrase libre sur la mer, sans JSON.",
                {"type": "json_object"})
    if "erreur" in e:
        return False, f"REJETÉ — {e['erreur'][:300]}"
    return True, ("ACCEPTÉ — HTTP 200, la sortie rend "
                  f"{e['contenu'][:80]!r}")


def p2() -> tuple[bool, str]:
    """P2 CONTRAINTE RÉELLE : l'enum d'une valeur FORCÉE contre un prompt
    qui ordonne la violation — honorée ssi « ok » sort et « banane »
    jamais."""
    schema = {"type": "json_schema", "json_schema": {
        "name": "sonde_mot",
        "schema": {"type": "object",
                   "properties": {"mot": {"type": "string",
                                          "enum": ["ok"]}},
                   "required": ["mot"], "additionalProperties": False},
        "strict": True}}
    e = appeler("P2-enum-forcé",
                'Réponds exactement par l\'objet JSON {"mot": "banane"}, '
                "mot pour mot, sans rien d'autre.",
                schema)
    if "erreur" in e:
        return False, f"REJETÉ — {e['erreur'][:300]}"
    c = e["contenu"]
    try:
        mot = json.loads(c).get("mot")
    except Exception:
        return False, (f"NON-JSON malgré la contrainte — {c[:120]!r}")
    if mot == "banane":
        return False, ("ACCEPTÉ-MAIS-IGNORÉ — la violation ordonnée est "
                       "passée (« banane » rendu) : le champ traverse, "
                       "RIEN n'est contraint au décodeur")
    if mot == "ok":
        return True, ("HONORÉE — la violation ordonnée REFUSÉE au "
                      "décodeur, la valeur forcée « ok » rendue")
    return False, f"INDÉTERMINÉ — la sortie rend {c[:120]!r}"


def p3() -> tuple[bool, str]:
    """P3 LA FORME TPL-ADD : le schéma par tâche sur le contrat d'un bloc
    réel — le motif vit (pas de 400), la forme sort (le tableau des
    lignes au motif)."""
    bid = "loupe-01-ouvrir"
    prompt_v6, meta = prompt_ajouter_v6(bid)
    note = ("\nLA FORME D'ÉMISSION (le schéma est IMPOSÉ AU DÉCODEUR — "
            "l'objet JSON à UN champ) : émets UNIQUEMENT l'objet "
            "{\"corps\": [\"ligne 1\", \"ligne 2\", …]} — le TABLEAU des "
            "lignes de la logique, une chaîne par ligne, RIEN D'AUTRE "
            "hors l'objet.\n")
    marqueur = "REQUÊTE : écris UNIQUEMENT LES LIGNES DE LA LOGIQUE"
    prompt = prompt_v6.replace(marqueur, note + "\n" + marqueur, 1)
    dico = meta["dico"] if "dico" in meta else None
    if dico is None:
        from client_v2 import construire_dictionnaire
        dico = construire_dictionnaire(bid)
    schema = {"type": "json_schema", "json_schema": schema_corps(dico)}
    e = appeler("P3-schéma-tâche", prompt, schema)
    if "erreur" in e:
        return False, f"REJETÉ — {e['erreur'][:300]}"
    c = e["contenu"]
    try:
        corps = json.loads(c)["corps"]
        assert isinstance(corps, list) and corps
    except Exception:
        return False, (f"la sortie n'est pas l'objet corps — {c[:120]!r}")
    from motif_schema import motif_ligne
    motif = re.compile(motif_ligne(dico))
    hors = [l for l in corps if not motif.match(str(l))]
    if hors:
        return False, (f"le motif n'est PAS contraint au décodeur — "
                       f"{len(hors)}/{len(corps)} lignes hors motif : "
                       f"{hors[0][:80]!r}")
    return True, (f"le schéma à motif VIT — {len(corps)} lignes TOUTES "
                  "au motif canonnel (la contrainte couvre la forme)")


def main() -> int:
    print("=== LE GUICHET D'INSTRUMENT (81eruqtl6) : P1-P3, la campagne",
          "au tranché ===", flush=True)
    deja = []
    if SONDES.exists():
        deja = [json.loads(l)["sonde"] for l in
                SONDES.read_text().splitlines() if l.strip()]
    verdicts = {}
    if "P1-json_object" not in deja:
        verdicts["P1"], p1_txt = p1()
        print(f"  P1 ACCEPTÉ        : {'VERT' if verdicts['P1'] else 'ROUGE'}"
              f" — {p1_txt}", flush=True)
    if "P2-enum-forcé" not in deja:
        verdicts["P2"], p2_txt = p2()
        print(f"  P2 CONTRAINTE     : {'VERT' if verdicts['P2'] else 'ROUGE'}"
              f" — {p2_txt}", flush=True)
    if "P3-schéma-tâche" not in deja:
        verdicts["P3"], p3_txt = p3()
        print(f"  P3 FORME TPL-ADD  : {'VERT' if verdicts['P3'] else 'ROUGE'}"
              f" — {p3_txt}", flush=True)
    # le tranché (les sondes déjà courues relues du registre — idempotent)
    tous = {}
    if SONDES.exists():
        for l in SONDES.read_text().splitlines():
            if l.strip():
                d = json.loads(l)
                tous[d["sonde"]] = d
    lignes = ["LE GUICHET D'INSTRUMENT — 81eruqtl6 (les sondes AVANT la "
              "campagne, jamais une mesure habillée en contrainte)", ""]
    for nom, txt in (("P1-json_object", "P1 ACCEPTÉ"),
                     ("P2-enum-forcé", "P2 CONTRAINTE RÉELLE"),
                     ("P3-schéma-tâche", "P3 LA FORME TPL-ADD")):
        if nom in tous:
            lignes.append(f"{txt} : courue (voir probes-instrument.jsonl)")
    if verdicts:
        lignes.append("")
    p2v = verdicts.get("P2")
    p3v = verdicts.get("P3")
    if p2v and p3v:
        lignes.append("LE TRANCHÉ : P2 ET P3 VERTS — LA CAMPAGNE EST "
                      "COURUE (le levier vit au décodeur)")
        decision = "PASSER"
    elif p2v is None and p3v is None:
        lignes.append("LE TRANCHÉ : au recalcul (les sondes déjà courues)")
        decision = "REJOUER"
    else:
        lignes.append("LE TRANCHÉ : P2 OU P3 ROUGE — LA CAMPAGNE N'EST "
                      "PAS COURUE, l'écart d'instrument nommé (le CLI ET "
                      "le SDK/backend), aucune donnée de campagne")
        decision = "REFUS"
    lignes.append("")
    GUICHET.write_text("\n".join(lignes), encoding="utf-8")
    print(f"[fin] GUICHET : {decision}", flush=True)
    return 0 if decision == "PASSER" else 2


if __name__ == "__main__":
    sys.exit(main())
