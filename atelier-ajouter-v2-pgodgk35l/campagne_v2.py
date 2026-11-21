#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_v2.py — LA CAMPAGNE TPL-ADD-v2 AUX 18 MÊMES TÂCHES (pgodgk35l).

LA RÈGLE (l'instruction) : les 18 mêmes tâches que la vague 11, la graine
20261117 reconduite, L'ORDRE JAMAIS RE-TIRÉ ; la mesure au tokenizer natif
(le champ usage LU à chaque appel), cl100k PARALLÈLE, la re-tokenisation
indépendante ≤ 1 ; la cible pré-enregistrée FALSIFIABLE : faisabilité
≥ 15/18 verts, coût ≤ 1 500 natifs ; si la cible manque, le gap résiduel
est nommé par classe de refus, jamais re-tiré.

LES 15 REFUS v1 re-roulés sur le client v2 : chaque refus nommé
re-productible ou converti vert sur pièce ; LES 3 VERTS v1 re-roulés :
round-trip exact octet pour octet, cadre ABI vérifié.

L'INSTRUMENT : le CLI z-ai (le patron OPT-10 reconduit), chaque appel
journalisé au JSONL ; le modèle ne voit QUE le prompt — le dictionnaire,
le squelette et les empreintes gravés au matériau."""
from __future__ import annotations

import json
import pathlib
import statistics
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
sys.path.insert(0, str(ICI))

from client_v2 import (construire_dictionnaire, dictionnaire_muté,  # noqa: E402
                       prompt_ajouter_v2, assembler_v2)
from client_gabarits import Refus  # noqa: E402

BLOCS = ["loupe-07-cumul", "loupe-11-defilement", "loupe-02-lire",
         "loupe-12-aller", "loupe-03-fermer", "loupe-10-peinture",
         "loupe-09-ecran", "loupe-17-sauver", "loupe-16-saisie",
         "loupe-13-recherche", "loupe-14-suivant", "loupe-18-quitter",
         "loupe-06-md5", "loupe-15-curseur", "loupe-04-cadre",
         "loupe-08-ligne", "loupe-01-ouvrir", "loupe-05-sha256"]
GRAINE = 20261117          # la graine reconduite — l'ordre jamais re-tiré
VERTS_V1 = {"loupe-02-lire", "loupe-13-recherche", "loupe-04-cadre"}
JOURNAL = ICI / "journal_v2.jsonl"
GARDE = ICI / "garde-brut-v2.jsonl"
RESULTATS = ICI / "resultats_v2.jsonl"

import tiktoken  # noqa: E402
ENC = tiktoken.get_encoding("cl100k_base")


def horodatage() -> str:
    return datetime.now(timezone.utc).isoformat()[:19]


def appeler_et_compter(tache: str, prompt: str) -> tuple[str, dict]:
    """LE PATRON D'APPEL (la campagne OPT-10 reconduite) : le CLI z-ai, la
    réponse JSON lue, le champ usage JOURNALISÉ — le compte est le LOG,
    jamais une estimation."""
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
        f.write(json.dumps({"horodatage": horodatage(), "phase": "mesure",
                            "tache": tache, "reponse_api": reponse},
                           ensure_ascii=False) + "\n")
    usage = reponse.get("usage") or {}
    texte = (reponse.get("choices") or [{}])[0].get("message",
                                                    {}).get("content", "")
    ligne = {"horodatage": horodatage(), "phase": "mesure", "tache": tache,
             "id": reponse.get("id", ""), "modele": reponse.get("model", ""),
             "prompt_tokens": int(usage.get("prompt_tokens", 0)),
             "completion_tokens": int(usage.get("completion_tokens", 0)),
             "total_tokens": int(usage.get("total_tokens", 0)),
             "source": "log-api"}
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return texte, ligne


def main() -> int:
    # ---- les contrôles négatifs AVANT la campagne (les quatre faces) -----
    _, meta = prompt_ajouter_v2("loupe-02-lire")
    negatifs = {}
    try:
        assembler_v2(meta["squelette"], "jmp LBL-999", meta)
        negatifs["ID-INCONNU"] = False
    except Refus as e:
        negatifs["ID-INCONNU"] = (e.nom == "ID-INCONNU")
    m2 = dict(meta)
    m2["dico"] = dictionnaire_muté(meta["dico"])
    try:
        assembler_v2(m2["squelette"], "ret", m2)
        negatifs["DICT-DIVERGENT"] = False
    except Refus as e:
        negatifs["DICT-DIVERGENT"] = (e.nom == "DICT-DIVERGENT")
    try:
        assembler_v2(meta["squelette"], "call CST-004", meta)
        negatifs["EXPANSION-DIVERGENTE"] = False
    except Refus as e:
        negatifs["EXPANSION-DIVERGENTE"] = (e.nom == "EXPANSION-DIVERGENTE")
    try:
        assembler_v2(meta["squelette"], "mov eax, TRUC bizarre", meta)
        negatifs["HORS-FORMAT"] = False
    except Refus as e:
        negatifs["HORS-FORMAT"] = (e.nom == "HORS-FORMAT")
    print("LES QUATRE CONTRÔLES NÉGATIFS :", negatifs)
    if not all(negatifs.values()):
        print("ROUGE : un contrôle négatif non attrapé — la campagne "
              "refusée (fail-closed)")
        return 2

    # ---- la campagne : les 18 tâches, l'ordre de la graine reconduite -----
    resultats = []
    t0 = time.monotonic()
    for i, bloc in enumerate(BLOCS, 1):
        tache = f"ajouter-v2-i{GRAINE % 1000000:06d}{i:02d}"
        prompt, meta = prompt_ajouter_v2(bloc)
        try:
            texte, journal = appeler_et_compter(tache, prompt)
        except RuntimeError as e:
            resultats.append({"tache": tache, "bloc": bloc, "mode":
                              "ajouter-v2", "verdict": f"APPEL ÉCHEOU : "
                              f"{str(e)[:60]}", "vert": False})
            continue
        try:
            _, detail = assembler_v2(meta["squelette"], texte, meta)
            verdict = f"ASSEMBLE+ROUND-TRIP+CADRE:OK ({detail[:44]})"
            vert = True
        except Refus as e:
            verdict = f"REFUS {e.nom}: {e.detail[:70]}"
            vert = False
        cl_p = len(ENC.encode_ordinary(prompt))
        cl_r = len(ENC.encode_ordinary(texte))
        retok = len(ENC.encode_ordinary(prompt))
        rec = {"tache": tache, "bloc": bloc, "mode": "ajouter-v2",
               "verdict": verdict, "vert": vert,
               "prompt_tokens": journal["prompt_tokens"],
               "completion_tokens": journal["completion_tokens"],
               "total_tokens": journal["total_tokens"],
               "cl100k_prompt": cl_p, "cl100k_reponse": cl_r,
               "retok_prompt": retok,
               "materiau_cl100k": cl_p, "prose_cl100k": 0}
        resultats.append(rec)
        print(f"  [{i:2d}/18] {bloc:22s} "
              f"{'VERT ' if vert else 'REFUS'} "
              f"natif={journal['total_tokens']:5d} "
              f"(v1 : {'vert' if bloc in VERTS_V1 else 'refus'})")
    duree = time.monotonic() - t0

    # ---- les mesures : les médianes, la faisabilité, la cible -------------
    totaux = [r["total_tokens"] for r in resultats if r.get("total_tokens")]
    verts = [r for r in resultats if r["vert"]]
    med = statistics.median(totaux) if totaux else 0
    # la re-tokenisation indépendante : l'écart au journal (≤ 1 exigé)
    ecarts = []
    for r in resultats:
        j = r.get("prompt_tokens", 0)
        if j and r.get("retok_prompt"):
            ecarts.append(abs(r["retok_prompt"] - j))
    ecart_max = max(ecarts) if ecarts else 0
    cible_verte = len(verts) >= 15 and med <= 1500

    # les 15 refus v1 : convertis ou reproduits ?
    conversions = [r["bloc"] for r in resultats
                   if r["vert"] and r["bloc"] not in VERTS_V1]
    reproductions = [r["bloc"] for r in resultats
                     if not r["vert"] and r["bloc"] not in VERTS_V1]
    verts_v1_rejoues = [r["bloc"] for r in resultats
                        if r["vert"] and r["bloc"] in VERTS_V1]

    rap = [
        "LA CAMPAGNE TPL-ADD-v2 (pgodgk35l) — les 18 mêmes tâches, la graine",
        f"{GRAINE} reconduite, l'ordre JAMAIS re-tiré ; le CLI z-ai au champ",
        "usage LU ; les QUATRE contrôles négatifs REFUSÉS au premier nom",
        "avant la première tâche",
        "",
        f"LES RÉSULTATS : {len(verts)}/18 VERTS · la médiane native "
        f"{med:.0f} [cl100k {statistics.median([r['cl100k_prompt'] + r['cl100k_reponse'] for r in resultats if r.get('cl100k_prompt')]):.0f}] · "
        f"la re-tokenisation indépendante écart max {ecart_max}",
        f"LA CIBLE PRÉ-ENREGISTRÉE : ≥ 15/18 verts ET ≤ 1 500 natifs : "
        f"{'ATTEINTE' if cible_verte else 'MANQUÉE — le gap résiduel nommé'}",
        f"LES 15 REFUS v1 : {len(conversions)} CONVERTIS VERTS sur pièce "
        f"({', '.join(conversions[:8])}…)",
        f"  les refus v1 restant refus : {len(reproductions)} "
        f"({', '.join(reproductions[:6])}…)",
        f"LES 3 VERTS v1 re-roulés : {len(verts_v1_rejoues)}/3 verts "
        "(round-trip exact, cadre ABI vérifié)",
        f"LA DURÉE : {duree:.0f} s · le journal {JOURNAL.name} · la garde "
        "brute au garde-brut-v2.jsonl",
    ]
    if not cible_verte:
        rap += ["", "LE GAP RÉSIDUEL NOMMÉ PAR CLASSE DE REFUS :"]
        classes: dict[str, int] = {}
        for r in resultats:
            if not r["vert"]:
                c = r["verdict"].split(":")[0].replace("REFUS ", "")
                classes[c] = classes.get(c, 0) + 1
        for c, n in sorted(classes.items(), key=lambda x: -x[1]):
            rap.append(f"  {n} × {c}")
    rap += ["", f"LE VERDICT : {'VERT' if cible_verte else 'LE GAP NOMMÉ'}"]
    (ICI / "rapport-campagne-v2.txt").write_text("\n".join(rap) + "\n",
                                                  encoding="utf-8")
    with open(RESULTATS, "w", encoding="utf-8") as f:
        for r in resultats:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("\n".join(rap))
    return 0 if cible_verte else 1


if __name__ == "__main__":
    sys.exit(main())
