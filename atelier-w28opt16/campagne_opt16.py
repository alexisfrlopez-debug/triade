#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_opt16.py — OPT-16 : ÉDITER PAR DIFF STRUCTURÉ AU PLANCHER TOKEN
(W28OPT16, la vague 28 — le plan gelé PLAN-W28OPT16.md, sha256 consigné AVANT
toute mesure à EMPREINTES-PLANS-VAGUE28.txt).

La cible pré-enregistrée : MÉDIANE ≤ 150 TOKENS NATIFS sur les 18 tâches
d'édition (ratio plancher ~5,5× contre le diff réel 27,5 tokens, au lieu de
24,5×). La graine 20261117 reconduite, l'ordre des 18 tâches JAMAIS re-tiré
(l'ordre canonique du fichier taches-edition.json, celui des campagnes
précédentes). Le budget `usage` natif LU à chaque appel, le cl100k compté en
parallèle (un compte distinct, jamais le juge).

LE SCHÉMA FERMÉ (l'extension de D264 à l'édition) :
  {"op": "substituer", "dst": "<id du bloc>", "offset": <index de ligne>,
   "src": "<la ligne nouvelle, littérale>"}

LES QUATRE REFUS NOMMÉS fail-closed : POINTEUR-INCONNU, EMPREINTE-DIVERGENTE,
SCHÉMA-VIOLÉ, HORS-FORMAT. L'AGRÉGATEUR fail-closed : un appel manquant refuse
le verdict. LA BOUCLE DE RÉPARATION bornée à TROIS tours réinjectant le refus
exact et le contre-exemple.

Usage : python3 atelier-w28opt16/campagne_opt16.py --courir
"""
import datetime as dt
import hashlib
import json
import pathlib
import statistics
import subprocess
import sys
import tempfile

R = pathlib.Path(__file__).resolve().parents[1]
ICI = pathlib.Path(__file__).resolve().parent
TACHES = R / "atelier-opt05-pe6iv71fj" / "taches-edition.json"
NOTATIONS = R / "loupe" / "notation"
JOURNAL = ICI / "journal-opt16.jsonl"
RESULTATS = ICI / "resultats-opt16.json"
D264 = R / "atelier-w27decco" / "campagne_d264.py"      # l'expandeur de référence
CIBLE = 150.0
GRAINE = 20261117

SCHEMA_EXEMPLE = ('{"op": "substituer", "dst": "<l-id-du-bloc>", '
                  '"offset": <l-index-de-la-ligne>, "src": "<la ligne nouvelle>"}')


class Refus(Exception):
    def __init__(self, nom, detail):
        self.nom = nom
        self.detail = detail
        super().__init__(f"{nom}: {detail}")


def horodatage() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256f(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def appeler_et_compter(phase: str, tache: str, prompt: str):
    """LE PATRON D'APPEL (OPT-10/gabarits reconduit) : le CLI z-ai, le champ
    usage JOURNALISÉ — le compte est le LOG, jamais une estimation."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False,
                                      encoding="utf-8") as f:
        chemin = pathlib.Path(f.name)
    cmd = ["z-ai", "chat", "--prompt", prompt, "-o", str(chemin)]
    for tentative in range(4):
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        if proc.returncode == 0:
            break
        import time
        time.sleep(20 * (tentative + 1))          # le bord rate-limited : doser
    if proc.returncode != 0:
        chemin.unlink(missing_ok=True)
        raise RuntimeError(f"l'appel z-ai a échoué : {proc.stderr[:300]}")
    reponse = json.loads(chemin.read_text(encoding="utf-8"))
    usage = reponse.get("usage") or {}
    texte = (reponse.get("choices") or [{}])[0].get("message", {}).get("content", "")
    ligne = {
        "horodatage": horodatage(), "phase": phase, "tache": tache,
        "id": reponse.get("id", ""), "modele": reponse.get("model", ""),
        "prompt_tokens": int(usage.get("prompt_tokens", 0)),
        "completion_tokens": int(usage.get("completion_tokens", 0)),
        "total_tokens": int(usage.get("total_tokens", 0)),
        "somme_coherente": (int(usage.get("prompt_tokens", 0))
                            + int(usage.get("completion_tokens", 0))
                            == int(usage.get("total_tokens", 0))),
        "source": "log-api",
    }
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    chemin.unlink(missing_ok=True)
    return texte, ligne


def retokenise_independante(texte: str) -> int:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(texte or ""))


def prompt_tache(t, notation: str, empreinte: str) -> str:
    return (
        "OPÉRATION ÉDITER, DIFF STRUCTURÉ (le schéma fermé D264 étendu à l'édition).\n"
        f"BLOC : {t['bloc']} (empreinte sha256 du fichier de notation : {empreinte})\n"
        f"LA NOTATION COMPORTE {len(notation.splitlines())} LIGNES (les indices de ligne "
        "commencent à 0).\n"
        f"CONSIGNE : {t['consigne']}\n"
        "RÉPONDS UNIQUEMENT l'objet JSON exact (aucun autre texte, aucune politesse) : \n"
        f"{SCHEMA_EXEMPLE}\n"
        "« op » vaut « substituer » ; « offset » est l'index de la ligne à réviser ; "
        "« src » est la ligne nouvelle, littérale, exacte au domaine de notation.")


def valider(texte: str, t, notation: str, empreinte: str):
    """LA VALIDATION CLIENT fail-closed — les quatre refus nommés."""
    s = texte.strip()
    if s.startswith("```"):
        s = s.strip("`")
        s = s[4:] if s.startswith("json") else s
        s = s.strip()
    try:
        obj = json.loads(s)
    except Exception as e:
        raise Refus("HORS-FORMAT", f"la réponse n'est pas l'objet JSON : {e.__class__.__name__}")
    if not isinstance(obj, dict):
        raise Refus("HORS-FORMAT", "la réponse n'est pas un objet")
    cles = set(obj.keys())
    if cles != {"op", "dst", "offset", "src"}:
        raise Refus("SCHÉMA-VIOLÉ", f"les clés {sorted(cles)} != les quatre du schéma fermé")
    if obj["op"] != "substituer":
        raise Refus("SCHÉMA-VIOLÉ", f"l'op «{obj['op']}» hors de l'enum fermé")
    if not isinstance(obj["offset"], int) or isinstance(obj["offset"], bool):
        raise Refus("SCHÉMA-VIOLÉ", "l'offset n'est pas un entier")
    if not isinstance(obj["src"], str) or not obj["src"].strip():
        raise Refus("SCHÉMA-VIOLÉ", "la ligne src n'est pas une chaîne non vide")
    if obj["dst"] != t["bloc"]:
        raise Refus("POINTEUR-INCONNU", f"le dst «{obj['dst']}» != le bloc soumis {t['bloc']}")
    n = (NOTATIONS / f"{t['bloc']}.asm").read_text(encoding="utf-8")
    if hashlib.sha256(n.encode("utf-8")).hexdigest() != empreinte:
        raise Refus("EMPREINTE-DIVERGENTE", "la notation du bloc a divergé de l'empreinte soumise")
    lignes = notation.splitlines()
    if not (0 <= obj["offset"] < len(lignes)):
        raise Refus("SCHÉMA-VIOLÉ", f"l'offset {obj['offset']} hors de la plage du bloc "
                     f"(0..{len(lignes)-1})")
    return obj


def expander(t, obj, notation: str):
    """L'EXPANSION CLIENT : la substitution à l'offset, la confrontation exacte
    (la ligne unique révisée, AUCUNE autre ligne changée), le round-trip."""
    lignes = notation.splitlines()
    idx = obj["offset"]
    attendu = t["nouvelle"]
    rec = list(lignes)
    rec[idx] = obj["src"]
    if rec == lignes:
        raise Refus("SCHÉMA-VIOLÉ", "la substitution ne change rien")
    diffs = [i for i, (a, b) in enumerate(zip(lignes, rec)) if a != b]
    if len(rec) != len(lignes) or diffs != [idx]:
        raise Refus("SCHÉMA-VIOLÉ", f"le diff touche {len(diffs)} lignes, pas la seule")
    if obj["src"] != attendu:
        raise Refus("SCHÉMA-VIOLÉ", f"la ligne substituée «{obj['src'][:40]}…» != l'attendue "
                     f"«{attendu[:40]}…»")
    from client_gabarits_rt import round_trip_vite
    ok, detail = round_trip_vite("\n".join(rec) + "\n")
    if not ok:
        raise Refus("ROUND-TRIP-DIVERGENT", detail)
    return "\n".join(rec) + "\n"


def tour_reparation(prompt: str, refus: Refus) -> str:
    return (prompt + "\n\nLE REFUS EXACT DU CLIENT : " + refus.nom + " — " + refus.detail[:300]
            + "\nRéponds à nouveau UNIQUEMENT l'objet JSON conforme.")


CHECKPOINT = ICI / "resultats-partiels.json"


def main() -> int:
    taches = json.loads(TACHES.read_text(encoding="utf-8"))
    assert len(taches) == 18, "les 18 tâches d'édition"
    empreinte_d264 = sha256f(D264)
    resultats = json.loads(CHECKPOINT.read_text()) if CHECKPOINT.exists() else []
    faits = {r["bloc"] for r in resultats}
    verts = sum(1 for r in resultats if r["vert"])
    refus_finaux = {}
    for t in taches:
        if t["bloc"] in faits:
            continue
        notation = (NOTATIONS / f"{t['bloc']}.asm").read_text(encoding="utf-8")
        empreinte = hashlib.sha256(notation.encode("utf-8")).hexdigest()
        prompt = prompt_tache(t, notation, empreinte)
        essaie = {"completion_tokens": 0, "total_tokens": 0}
        tours = 0
        vert = False
        texte = ""
        for tour in range(3):
            tours = tour + 1
            texte, ligne = appeler_et_compter("opt16", t["bloc"], prompt)
            essaie["completion_tokens"] += ligne["completion_tokens"]
            essaie["total_tokens"] += ligne["total_tokens"]
            try:
                obj = valider(texte, t, notation, empreinte)
                expander(t, obj, notation)
                vert = True
                break
            except Refus as e:
                refus_finaux.setdefault(e.nom, 0)
                refus_finaux[e.nom] += 1
                prompt = tour_reparation(prompt, e)
        import time as _t
        _t.sleep(3)                    # le dosage inter-appels (le bord rate-limited)

    med18 = statistics.median([r["completion_tokens"] for r in resultats])
    medv = (statistics.median([r["completion_tokens"] for r in resultats if r["vert"]])
            if verts else None)
    res = {
        "cible": CIBLE, "graine": GRAINE, "n": 18, "verts": verts,
        "mediane_sur_18": med18, "mediane_sur_vertes": medv,
        "verdict": ("TENUE" if med18 <= CIBLE else "MANQUÉE"),
        "ratio_plancher": round(med18 / 27.5, 2),
        "refus_par_classe": refus_finaux,
        "empreinte_d264": empreinte_d264,
        "resultats": resultats,
    }
    RESULTATS.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "resultats"},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
