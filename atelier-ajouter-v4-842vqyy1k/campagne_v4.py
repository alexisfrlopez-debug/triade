#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_v4.py — TPL-ADD-v4 (842vqyy1k, la vague 14) : fermer le gap
AJOUTER sans affaiblir aucun juge. LES QUATRE LEVIERS :
(1) la grammaire au décodage — le CLI z-ai n'expose PAS response_format
    (le constat v3 reconduit, NOMMÉ au registre — l'écart d'instrument) ;
(2) LE SQUELETTE À TROUS TYPÉS — le prompt porte l'énoncé des trous typés ;
(3) LA RÉPARATION GUIDÉE PAR CONTRE-EXEMPLE — au refus, le prompt rend le
    diff exact + UN exemplaire canonique du motif fautif corrigé ;
(4) L'EXEMPLAIRE PAR PROCHE CONTRAT — le bloc scellé voisin injecté comme
    few-shot littéral. Graines 20261117, ordre JAMAIS re-tiré, budget 3.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
V3 = REPO / "atelier-ajouter-v3-5nwnwoceo"
V2 = REPO / "atelier-ajouter-v2-pgodgk35l"
GAB = REPO / "atelier-gabarits-o5apue194"
sys.path.insert(0, str(V3))
sys.path.insert(0, str(V2))
sys.path.insert(0, str(GAB))

import client_v3 as C3          # noqa: E402
from client_v3 import assembler_v3  # noqa: E402
from client_v2 import construire_dictionnaire  # noqa: E402

ICI = REPO / "atelier-ajouter-v4-842vqyy1k"
JOURNAL = ICI / "journal_v4.jsonl"
RESULTATS = ICI / "resultats_v4.jsonl"
GARDE = ICI / "garde-brut-v4.jsonl"
BUDGET = 3
BLOCS = ["loupe-07-cumul", "loupe-11-defilement", "loupe-02-lire",
         "loupe-12-aller", "loupe-03-fermer", "loupe-10-peinture",
         "loupe-09-ecran", "loupe-17-sauver", "loupe-16-saisie",
         "loupe-13-recherche", "loupe-14-suivant", "loupe-18-quitter",
         "loupe-06-md5", "loupe-15-curseur", "loupe-04-cadre",
         "loupe-08-ligne", "loupe-01-ouvrir", "loupe-05-sha256"]


def exemplaire_proche(bid: str) -> str:
    """LEVIER 4 : la notation scellée VOISINE (le proche contrat), les 14
    premières lignes de code — un few-shot LITTÉRAL (référence, jamais un
    calcul)."""
    p = REPO / "loupe" / "notation"
    fichiers = sorted(p.glob("loupe-*.asm"))
    noms = [f.stem for f in fichiers]
    voisin = noms[-1]
    for i, n in enumerate(noms):
        if bid.endswith(n.split("-")[-1]) or n.endswith(bid[-4:]):
            voisin = noms[(i + 1) % len(noms)]
            break
    t = (p / f"{voisin}.asm").read_text(encoding="utf-8")
    corps = [l for l in t.split("\n")
             if l.split(";")[0].strip() and not l.strip().startswith(";")]
    return "\n".join(corps[:14]), voisin


def prompt_ajouter_v4(nom_bloc: str) -> tuple:
    """LE PROMPT v4 = le v3 (la grammaire publiée) + L'EXEMPLAIRE PROCHE +
    LE SQUELETTE À TROUS TYPÉS."""
    prompt_v3, meta = C3.prompt_ajouter_v3(nom_bloc)
    exemplaire, voisin = exemplaire_proche(nom_bloc)
    insertion = (
        "\nUN EXEMPLAIRE SCELLÉ AU CONTRAT PROCHE (" + voisin + ", la "
        "référence littérale du dépôt — les formes admises y vivent, tout "
        "écart à la grammaire reste refusé) :\n" + exemplaire + "\n"
        "LE SQUELETTE À TROUS TYPÉS : écris la logique en COURTES lignes "
        "dont chaque trou est un TYTPE connu (registre, offset, cible "
        "LBL/CST) — une instruction par ligne, jamais d'expansion multiple "
        "par ligne, jamais d'opérande mémoire double.\n"
    )
    marqueur = "REQUÊTE : écris UNIQUEMENT LES LIGNES DE LA LOGIQUE"
    assert marqueur in prompt_v3, "le marqueur du prompt v3 a bougé"
    prompt = prompt_v3.replace(marqueur, insertion + "\n" + marqueur, 1)
    meta = dict(meta)
    meta["leviers"] = ["grammaire-v3", "exemplaire-proche-contrat",
                       "squelette-trous-typés"]
    return prompt, meta


CONTRE_EXEMPLE = (
    "\nLE CONTRE-EXEMPLE (les motifs fautifs et leurs corrections "
    "canoniques) :\n"
    "  FAUTIF   : call CST-004            jamais : un IAT en opérande cmp\n"
    "  ADMIS    : call CST-004            (l'IAT s'appelle en call)\n"
    "  FAUTIF   : cmp qword ptr [rax], qword ptr [rbx]\n"
    "  ADMIS    : mov rax, qword ptr [rbx]  puis  cmp rax, CST-001\n"
    "  FAUTIF   : movzx rax, rcx\n"
    "  ADMIS    : movzx rax, ecx        (la source 32 bits ou moins)\n"
    "  FAUTIF   : cmp eax, WM_PAINT\n"
    "  ADMIS    : cmp eax, CST-002      (un ID du dictionnaire, jamais un "
    "symbole en clair)\n"
)


def prompt_reparation_v4(prompt, logique_fautif, refus_nom, refus_detail,
                         tentative) -> str:
    """LEVIER 3 : la réparation par CONTRE-EXEMPLE (le diff exact + les
    motifs canoniques corrigés) — sur le prompt de réparation v3."""
    lignes = [l for l in (logique_fautif or "").split("\n") if l.strip()]
    diff = "\n".join("  OBTENU   : " + l for l in lignes[:6])
    return (C3.prompt_reparation(prompt, logique_fautif, refus_nom,
                                 refus_detail, tentative)
            + "\nLE DIFF EXACT (attendu : des lignes à la grammaire ; "
            "obtenu :)\n" + diff + "\n" + CONTRE_EXEMPLE)


def appeler_et_compter(tache, essai, prompt):
    """L'appel au LLM via le CLI z-ai (l'instrument v3 reconduit : le
    journal au champ usage, la garde-brut archivée par appel)."""
    tmp = ICI / f"tmp-{tache}-{essai}.json"
    t0 = time.monotonic()
    r = subprocess.run(["z-ai", "chat", "--prompt", prompt, "-o",
                        str(tmp)], capture_output=True, text=True,
                       timeout=900)
    dt = time.monotonic() - t0
    if r.returncode != 0 or not tmp.exists():
        raise RuntimeError(f"APPEL ÉCHEC : {r.stderr[:200]}")
    d = json.loads(tmp.read_text())
    tmp.unlink()
    usage = d.get("usage", {})
    contenu = d["choices"][0]["message"]["content"]
    with open(GARDE, "a") as f:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")
    with open(JOURNAL, "a") as f:
        f.write(json.dumps({
            "tache": tache, "essai": essai, "verdict": "APPEL",
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "secondes": round(dt, 1), "source": "log-api",
            "id": d.get("id", ""), "modele": d.get("model", "")},
            ensure_ascii=False) + "\n")
    return contenu, usage.get("total_tokens", 0)


def une_tache(i: int, bid: str) -> dict:
    tache = f"ajouter-v4-i261117{i+1:02d}"
    prompt, meta = prompt_ajouter_v4(bid)
    squelette = meta.get("squelette", "")
    logique, refus = None, ("", "")
    journaux = []
    for essai in range(BUDGET + 1):
        p = prompt if essai == 0 else prompt_reparation_v4(
            prompt, logique or "", refus[0], refus[1], essai)
        (ICI / "garde-prompts").mkdir(exist_ok=True)
        (ICI / "garde-prompts" / f"{tache}-t{essai}.txt").write_text(p)
        contenu, total = appeler_et_compter(tache, essai, p)
        journaux.append({"essai": essai, "total": total})
        try:
            assembler_v3(squelette, contenu, meta)
            return {"tache": tache, "bloc": bid, "vert": True,
                    "essais": essai + 1, "journaux": journaux,
                    "verdict": "VERT"}
        except Exception as e:
            refus = (type(e).__name__, str(e)[:400])
            logique = contenu
    return {"tache": tache, "bloc": bid, "vert": False,
            "essais": BUDGET + 1, "journaux": journaux,
            "verdict": f"REFUS {refus[0]}"}


def main() -> int:
    print("=== TPL-ADD-v4 : LES QUATRE LEVIERS (842vqyy1k) ===")
    fait = {}
    if RESULTATS.exists():
        for l in RESULTATS.read_text().splitlines():
            if l.strip():
                d = json.loads(l)
                fait[d["tache"]] = d
    for i, bid in enumerate(BLOCS):
        tache = f"ajouter-v4-i261117{i+1:02d}"
        if tache in fait:
            continue
        r = une_tache(i, bid)
        with open(RESULTATS, "a") as f:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"  {tache} ({bid}) : {r['verdict']}", flush=True)
        time.sleep(20)
    verts = [json.loads(l) for l in RESULTATS.read_text().splitlines()
             if l.strip()]
    nb = sum(1 for v in verts if v["vert"])
    couts = sorted(sum(j["total"] for j in v["journaux"])
                   for v in verts if v["vert"])
    med = couts[len(couts) // 2] if couts else 0
    print(f"[fin] AJOUTER {nb}/{len(verts)} verts ; coût médian par "
          f"changement validé {med} natifs ; cible ≥15/18 ET ≤4500")
    return 0


if __name__ == "__main__":
    sys.exit(main())
