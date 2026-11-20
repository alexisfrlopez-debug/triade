#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_fenetre.py — LA CAMPAGNE DE L'INSTRUCTION mqf258e4l (la vague
10, le PLAN-MQF258E4L gelé) : LA FENÊTRE DE RELECTURE DE L'OPÉRATION ÉDITER.

LES DEUX CELLULES (la même graine 20261117, n=18, l'instrument de la
campagne — le CLI z-ai, le champ usage LU, chaque appel journalisé) :
  AVANT  éditer-H2 — la référence : LA NOTATION COMPLÈTE relue (le gabarit
         de la vague 9 TEL QUEL) ;
  APRÈS  éditer-F2 — LA FENÊTRE : ±12 lignes de notation autour de la
         cible + la consigne verbatim + LE FORMAT + L'EMPREINTE sha256 de
         la notation complète (le reste en CACHE client — jamais relu).

LA CONFRONTATION (fail-closed, les quatre refus reconduits) : le client
recoupe L'EMPREINTE de la notation en cache contre l'empreinte du prompt
(CONTEXTE-DIVERGENT sinon — l'expansion fail-closed), applique les hunks
à la notation complète, reconstruit, ROUND-TRIP EXACT.

LA MESURE : les médianes natives (usage) + cl100k parallèle + LA
RE-TOKENISATION INDÉPENDANTE ±1 (la passe encode_ordinary d'un objet
neuf) ; LA DÉCOMPOSITION matériau/prose/réponse (cl100k) ; LE RATIO AU
PLANCHER (éditer : la paire de lignes du diff réel — 18 cl100k, le
plancher gelé du tableau de bord).

L'AUTOTEST DES QUATRE REFUS DU POINTEUR (l'exigence de l'instruction) :
l'expansion_pointuer.py de la campagne cq01qv1za re-roulée — les quatre
refus nommés demeurent fail-closed."""
from __future__ import annotations

import hashlib
import json
import pathlib
import statistics
import subprocess
import sys
import time

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
V8 = REPO / "atelier-opt05-pe6iv71fj"
sys.path.insert(0, str(V8))

from campagne_opt05 import (gabarit_editer_hunk, FORMAT_HUNK,  # noqa: E402
                             charger as charger_v8)
from client_hunks_v2 import traiter as traiter_v2, Refus  # noqa: E402

import tiktoken  # noqa: E402

JOURNAL = ICI / "journal_fenetre.jsonl"
GARDE = ICI / "garde-fenetre.jsonl"
PROMPTS = ICI / "garde-prompts"
PROMPTS.mkdir(exist_ok=True)
RESULTATS = ICI / "resultats_fenetre.jsonl"

CL100K = tiktoken.get_encoding("cl100k_base")
FENETRE_N = 12          # ±12 lignes — la fenêtre gelée au plan


# ----------------------------------------------------------- l'instrument
def horodatage():
    import datetime as dt
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def appeler_et_compter(bras, phase, tache, prompt):
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                      delete=False, encoding="utf-8") as f:
        chemin = pathlib.Path(f.name)
    cmd = ["z-ai", "chat", "--prompt", prompt, "-o", str(chemin)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if proc.returncode != 0:
        chemin.unlink(missing_ok=True)
        raise RuntimeError(f"l'appel z-ai a échoué : {proc.stderr[:300]}")
    reponse = json.loads(chemin.read_text(encoding="utf-8"))
    with open(GARDE, "a", encoding="utf-8") as f:
        f.write(json.dumps({"horodatage": horodatage(), "bras": bras,
                            "phase": phase, "tache": tache,
                            "reponse_api": reponse},
                           ensure_ascii=False) + "\n")
    usage = reponse.get("usage") or {}
    texte = (reponse.get("choices") or [{}])[0].get("message",
                                                    {}).get("content", "")
    ligne = {
        "horodatage": horodatage(), "bras": bras, "phase": phase,
        "tache": tache, "id": reponse.get("id", ""),
        "modele": reponse.get("model", ""),
        "prompt_tokens": int(usage.get("prompt_tokens", 0)),
        "completion_tokens": int(usage.get("completion_tokens", 0)),
        "total_tokens": int(usage.get("total_tokens", 0)),
        "somme_coherente": (int(usage.get("prompt_tokens", 0))
                            + int(usage.get("completion_tokens", 0))
                            == int(usage.get("total_tokens", 0))),
        "source": "log-api",
    }
    chemin.unlink(missing_ok=True)
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return texte, ligne


# ------------------------------------------------------------ le gabarit F2
def gabarit_editer_fenetre(notation: str, ligne_index: int, consigne: str,
                           fenetre_n: int = FENETRE_N) -> tuple[str, str]:
    """LA FENÊTRE : ±N lignes autour de la cible, VERBATIM (les ancrés du
    format hunk demeurent des lignes exactes du texte courant) ; le RESTE
    en cache client, l'EMPREINTE sha256 posée au prompt (la garde)."""
    lignes = notation.split("\n")
    i = ligne_index
    i0, i1 = max(0, i - fenetre_n), min(len(lignes), i + fenetre_n + 1)
    fenetre = "\n".join(lignes[i0:i1])
    empreinte = hashlib.sha256(notation.encode("utf-8")).hexdigest()
    prompt = (
        "L'OPÉRATION ÉDITER DE LA CARTE TRIADE (le mode FENÊTRE — la base\n"
        "n'est PAS relue : la fenêtre de la cible seule est au prompt, la\n"
        "notation complète est en cache côté client ; la réponse ne rend\n"
        "QUE les hunks ciblés).\n\n"
        f"LA FENÊTRE DE LA CIBLE (les lignes {i0 + 1} à {i1} du bloc — la\n"
        f"ligne {i + 1} est la ligne cible) :\n{fenetre}\n\n"
        f"LA RÉVISION (la spécification de couche I, la consigne) :\n"
        f"{consigne}\n\n"
        f"LA GARDE (l'expansion fail-closed) : l'empreinte sha256 de la\n"
        f"notation complète en cache : {empreinte} — le client recoupe\n"
        f"cette empreinte AVANT l'application des hunks (toute divergence\n"
        f"de la base en cache : REFUS CONTEXTE-DIVERGENT).\n\n"
        f"{FORMAT_HUNK}"
        "REQUÊTE : applique la révision et rends UNIQUEMENT les hunks au\n"
        "format ci-dessus — les ancres « base: » sont des lignes exactes\n"
        "de la fenêtre ci-dessus — la dernière ligne exactement\n"
        "« FIN-HUNKS ».\n"
    )
    return prompt, empreinte


def appliquer_f2(notation_cache: str, empreinte_prompt: str,
                 reponse: str) -> tuple[str, str]:
    """LE CLIENT F2 : (1) la recoupe de l'empreinte (fail-closed —
    CONTEXTE-DIVERGENT si la cache diverge du prompt) ; (2) l'application
    des hunks à la notation complète ; (3) le round-trip (dans traiter_v2)."""
    emp_cache = hashlib.sha256(notation_cache.encode("utf-8")).hexdigest()
    if emp_cache != empreinte_prompt:
        raise Refus("CONTEXTE-DIVERGENT",
                    f"l'empreinte du cache {emp_cache[:16]}… != l'empreinte "
                    f"du prompt {empreinte_prompt[:16]}… — la base a divergé")
    return traiter_v2(notation_cache, reponse)


def retokenise_independante(texte: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")   # un objet NEUF, à part
    return len(enc.encode_ordinary(texte))


def stats(valeurs):
    v = sorted(valeurs)
    n = len(v)
    def pct(k):
        f, c = int(k * (n - 1)), int(-(-k * (n - 1) // 1))
        if f == c:
            return v[f]
        return v[f] + (v[c] - v[f]) * (k * (n - 1) - f)
    return {"n": n, "min": v[0], "q1": pct(0.25), "mediane": pct(0.5),
            "q3": pct(0.75), "max": v[-1]}


def main() -> int:
    vt, taches = charger_v8()
    ordre = vt["ordre"]
    par_id = {b["id"]: b for b in vt["blocs"]}
    cellules = {}
    for mode in ("editer-H2", "editer-F2"):
        faits = set()
        if JOURNAL.exists():
            for l in JOURNAL.read_text(encoding="utf-8").splitlines():
                if l.strip():
                    r = json.loads(l)
                    if r["tache"].startswith(mode + "-"):
                        faits.add(r["tache"])
        cellules[mode] = faits

    resultat_lignes = []
    for mode in ("editer-H2", "editer-F2"):
        manquants = [bid for bid in ordre
                     if f"{mode}-{bid}" not in cellules[mode]]
        print(f"[{mode}] {len(manquants)} appel(s) à vivre (l'ordre de la "
              f"graine {vt['graine']})", flush=True)
        for bid in manquants:
            nom = par_id[bid]["nom"]
            tache = f"{mode}-{bid}"
            notation = (REPO / "loupe" / "notation" /
                        f"{nom}.asm").read_text(encoding="utf-8")
            consigne = taches[nom]["consigne"]
            li = taches[nom]["ligne_index"]
            fenetre_texte = "\n".join(
                notation.split("\n")[max(0, li - FENETRE_N):
                                      li + FENETRE_N + 1])
            if mode == "editer-H2":
                prompt = gabarit_editer_hunk(notation, consigne)
                empreinte = None
            else:
                prompt, empreinte = gabarit_editer_fenetre(
                    notation, li, consigne)
            (PROMPTS / f"{tache}.txt").write_text(prompt, encoding="utf-8")
            try:
                texte, ligne = appeler_et_compter("T", "fenetre", tache,
                                                  prompt)
            except Exception as e:
                print(f"  ÉCHEC API {tache}: {e}", flush=True)
                time.sleep(15)
                continue
            try:
                if mode == "editer-H2":
                    _, detail = traiter_v2(notation, texte)
                    verdict = f"APPLIQUE+ROUND-TRIP:OK ({detail[:40]})"
                else:
                    _, detail = appliquer_f2(notation, empreinte, texte)
                    verdict = f"GARDE+APPLIQUE+ROUND-TRIP:OK ({detail[:40]})"
            except Refus as e:
                verdict = f"REFUS {e.nom}: {e.detail[:80]}"
            except Exception as e:
                verdict = f"ERREUR: {str(e)[:80]}"
            resultat_lignes.append({
                "tache": tache, "mode": mode, "bloc": nom,
                "verdict": verdict,
                "prompt_tokens": ligne["prompt_tokens"],
                "completion_tokens": ligne["completion_tokens"],
                "total_tokens": ligne["total_tokens"],
                "cl100k_prompt": len(CL100K.encode(prompt)),
                "cl100k_reponse": len(CL100K.encode(texte)),
                "retok_prompt": retokenise_independante(prompt),
                "retok_reponse": retokenise_independante(texte),
                "materiau_fenetre_cl100k": (
                    len(CL100K.encode(fenetre_texte)) if mode == "editer-F2"
                    else len(CL100K.encode(notation))),
                "vert": verdict.startswith(("APPLIQUE", "GARDE")),
                "vert": verdict.startswith(("APPLIQUE", "GARDE")),
            })
            cl_tot = (resultat_lignes[-1]["cl100k_prompt"]
                      + resultat_lignes[-1]["cl100k_reponse"])
            print(f"  {tache}: {ligne['total_tokens']} tokens "
                  f"(cl100k {cl_tot}) — {verdict[:70]}", flush=True)
            time.sleep(4)

    with open(RESULTATS, "a", encoding="utf-8") as f:
        for r in resultat_lignes:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # ---- l'analyse --------------------------------------------------------
    tous = []
    if RESULTATS.exists():
        for l in RESULTATS.read_text(encoding="utf-8").splitlines():
            if l.strip():
                tous.append(json.loads(l))
    rapport = ["LA CAMPAGNE FENÊTRE (mqf258e4l) — la vague 10", ""]
    ok_general = True
    for mode in ("editer-H2", "editer-F2"):
        rs = [r for r in tous if r["mode"] == mode]
        if not rs:
            continue
        verts = sum(1 for r in rs if r["vert"])
        tot = [r["total_tokens"] for r in rs]
        rep = [r["completion_tokens"] for r in rs]
        mat = [r["materiau_fenetre_cl100k"] for r in rs]
        prose = [r["cl100k_prompt"] - r["materiau_fenetre_cl100k"]
                 for r in rs]
        retok = [abs(r["cl100k_prompt"] - r["retok_prompt"])
                 + abs(r["cl100k_reponse"] - r["retok_reponse"])
                 for r in rs]
        plancher = 18            # la paire de lignes du diff réel (cl100k)
        rapport += [
            f"[{mode}] n={len(rs)} — verts {verts}/{len(rs)} ; TOTAL "
            f"natif médiane {stats(tot)['mediane']:.0f} "
            f"[q1 {stats(tot)['q1']:.0f}, q3 {stats(tot)['q3']:.0f}] ; "
            f"RÉPONSE médiane {stats(rep)['mediane']:.0f} ;",
            f"    DÉCOMPOSITION cl100k : matériau "
            f"{stats(mat)['mediane']:.0f} · prose "
            f"{stats(prose)['mediane']:.0f} · réponse "
            f"{stats(rep)['mediane']:.0f} (les trois champs consignés "
            f"séparément — la convention de périmètre) ;",
            f"    LA RE-TOKENISATION INDÉPENDANTE : écart max "
            f"{max(retok)} (±1 exigé) ; LE RATIO AU PLANCHER "
            f"(la paire de lignes du diff réel, {plancher} cl100k) : "
            f"{stats(tot)['mediane'] / plancher:.1f}× natif",
        ]
        if verts != len(rs) or max(retok) > 1:
            ok_general = False
    if tous:
        h2 = [r for r in tous if r["mode"] == "editer-H2"]
        f2 = [r for r in tous if r["mode"] == "editer-F2"]
        if h2 and f2:
            rapport += [
                "",
                f"LA RÉDUCTION : le total natif médiane "
                f"{stats([r['total_tokens'] for r in h2])['mediane']:.0f} → "
                f"{stats([r['total_tokens'] for r in f2])['mediane']:.0f} "
                f"({(1 - stats([r['total_tokens'] for r in f2])['mediane'] / stats([r['total_tokens'] for r in h2])['mediane']) * 100:.1f} %"
                f" de réduction) ; le matériau relu "
                f"{stats([r['materiau_fenetre_cl100k'] for r in h2])['mediane']:.0f} → "
                f"{stats([r['materiau_fenetre_cl100k'] for r in f2])['mediane']:.0f} cl100k "
                f"— LA FENÊTRE DU HUNK porte le gain, le cache de session "
                f"porte le reste",
            ]

    # ---- l'autotest des quatre refus du pointeur (l'exigence) -----------
    r = subprocess.run(
        [sys.executable, str(REPO / "atelier-cout-boucle-cq01qv1za" /
                             "expansion_pointeur.py")],
        capture_output=True, text=True, timeout=300)
    refus_ok = "4/4" in r.stdout or "QUATRE" in r.stdout.upper()
    rapport += ["", "LES QUATRE REFUS DU POINTEUR (l'exigence de "
                "l'instruction — l'expansion_pointuer re-roulée) :",
                *("    " + l for l in r.stdout.strip().splitlines()[-6:])]
    if r.returncode != 0:
        ok_general = False

    (ICI / "rapport-fenetre.txt").write_text("\n".join(rapport) + "\n",
                                             encoding="utf-8")
    print("\n".join(rapport))
    return 0 if ok_general else 2


if __name__ == "__main__":
    raise SystemExit(main())
