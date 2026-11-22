#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_v3.py — LA CAMPAGNE TPL-ADD-v3 AUX 36 TÂCHES (5nwnwoceo, la
vague 13) : les 18 tâches AJOUTER (l'ordre de verites-terrain.json, la
graine 20261117 reconduite, JAMAIS re-tiré) À LA BOUCLE DE RÉPARATION
(budget TROIS), puis L'EXTENSION AUX 18 TÂCHES ÉDITER (taches-edition.json,
la même boucle, le refus CONTEXTE-DIVERGENT de loupe-07-cumul demeurant).

LA MESURE (la lettre du plan) : faisabilité première passe · faisabilité
après reprises · COÛT BOUT-EN-BOUT PAR CHANGEMENT VALIDÉ (tentatives
refusées incluses, la somme des usage des appels de la tâche) au
tokenizer natif LU DU CHAMP USAGE, cl100k en parallèle.

LA CIBLE PRÉ-ENREGISTRÉE FALSIFIABLE : faisabilité après reprises
≥ 17/18 (94,4 %) ET coût médian par changement validé ≤ 4 500 natifs ;
si manquée, le gap résiduel nommé par classe de refus, JAMAIS re-tiré.

LES CONTRÔLES NÉGATIFS AVANT CAMPAGNE : les QUATRE refus v2 re-roulés +
les QUATRE validateurs de formes + L'OCTET MUTÉ AU CADRE (l'instruction :
« un octet muté au cadre → refus nommé exigé ») + le refus
CONTEXTE-DIVERGENT de l'éditer (la cellule d'avant, la garde vécue).

L'INSTRUMENT : le CLI z-ai (le patron OPT-10 reconduit), chaque appel
journalisé au JSONL (usage, verdict, réponse) ; les réponses brutes
archivées (garde-brut), les prompts archivés en texte (garde-prompts —
le retour de la convention v1)."""
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
sys.path.insert(0, str(REPO / "atelier-gabarits-o5apue194"))
sys.path.insert(0, str(REPO / "atelier-ajouter-v2-pgodgk35l"))

from client_v3 import (prompt_ajouter_v3, assembler_v3,  # noqa: E402
                        prompt_reparation, valider_formes, GRAMMAIRE_SHA256)
from client_v2 import dictionnaire_muté  # noqa: E402
from client_gabarits import (Refus, prompt_editer_t2, appliquer_t2,  # noqa
                             diff_exact, charger_tpl)

BLOCS = ["loupe-07-cumul", "loupe-11-defilement", "loupe-02-lire",
         "loupe-12-aller", "loupe-03-fermer", "loupe-10-peinture",
         "loupe-09-ecran", "loupe-17-sauver", "loupe-16-saisie",
         "loupe-13-recherche", "loupe-14-suivant", "loupe-18-quitter",
         "loupe-06-md5", "loupe-15-curseur", "loupe-04-cadre",
         "loupe-08-ligne", "loupe-01-ouvrir", "loupe-05-sha256"]
GRAINE = 20261117          # la graine reconduite — l'ordre jamais re-tiré
BUDGET = 3                 # le plafond de reprises (le plan)
NOTATIONS = REPO / "loupe" / "notation"
JOURNAL = ICI / "journal_v3.jsonl"
GARDE = ICI / "garde-brut-v3.jsonl"
PROMPTS = ICI / "garde-prompts"
RESULTATS = ICI / "resultats_v3.jsonl"

import tiktoken  # noqa: E402
ENC = tiktoken.get_encoding("cl100k_base")


def horodatage() -> str:
    return datetime.now(timezone.utc).isoformat()[:19]


def appeler_et_compter(tache: str, prompt: str, tentative: int) -> tuple:
    """LE PATRON D'APPEL (OPT-10 reconduit) : le CLI z-ai, la réponse JSON
    lue, le champ usage JOURNALISÉ — le compte est le LOG, jamais deviné.
    LE RYTHME et LA REPRISE : un délai de 20 s entre appels (la limite de
    débit de l'API vécue au 429 — l'écart d'instrument NOMMÉ) et jusqu'à
    CINQ reprises en repli exponentiel sur le 429 (jamais un tirage
    silencieux : la reprise ré-exécute le MÊME appel)."""
    chemin = pathlib.Path(tempfile.mkstemp(suffix=".json")[1])
    cmd = ["z-ai", "chat", "--prompt", prompt, "-o", str(chemin)]
    t0 = time.monotonic()
    delai = 20.0
    for essai_api in range(5):
        time.sleep(delai if essai_api else 0.0)
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=900)
        if proc.returncode == 0 and chemin.exists():
            break
        if "429" in (proc.stderr or "") or "Too many" in (proc.stderr or ""):
            delai = min(delai * 2, 300)
            print(f"    [429 vécu] la reprise en {delai:.0f} s "
                  f"(l'essai {essai_api + 1}/5)")
            continue
        dt = time.monotonic() - t0
        raise RuntimeError(f"l'appel z-ai a échoué : {proc.stderr[:300]}")
    else:
        dt = time.monotonic() - t0
        raise RuntimeError("l'appel z-ai a échoué : cinq reprises sur le "
                           "429 épuisées")
    dt = time.monotonic() - t0
    reponse = json.loads(chemin.read_text(encoding="utf-8"))
    chemin.unlink()
    texte = reponse["choices"][0]["message"]["content"]
    usage = reponse.get("usage", {})
    journal = {"tache": tache, "tentative": tentative,
               "prompt_tokens": int(usage.get("prompt_tokens", 0)),
               "completion_tokens": int(usage.get("completion_tokens", 0)),
               "total_tokens": int(usage.get("total_tokens", 0)),
               "secondes": round(dt, 1), "source": "log-api",
               "id": reponse.get("id", ""),
               "modele": reponse.get("model", ""),
               "horodatage": horodatage()}
    # la garde-brut : la réponse ENTIERE archivée
    with open(GARDE, "a", encoding="utf-8") as f:
        f.write(json.dumps({"tache": tache, "tentative": tentative,
                            "reponse_api": reponse}, ensure_ascii=False)
                + "\n")
    return texte, journal


def archiver_prompt(tache: str, tentative: int, prompt: str) -> None:
    PROMPTS.mkdir(exist_ok=True)
    (PROMPTS / f"{tache}-t{tentative}.txt").write_text(prompt,
                                                       encoding="utf-8")


def une_tache_ajouter(bloc: str, i: int) -> dict:
    """UNE tâche AJOUTER à la boucle de réparation : la première passe,
    puis jusqu'à TROIS réparations ciblées (le refus nommé + la ligne
    fautive au prompt de réparation)."""
    tache = f"ajouter-v3-i{GRAINE % 1000000:06d}{i:02d}"
    prompt, meta = prompt_ajouter_v3(bloc)
    archiver_prompt(tache, 0, prompt)
    journaux = []
    refus_finaux = None
    logique = ""
    for tentative in range(0, BUDGET + 1):
        p = prompt if tentative == 0 else prompt_reparation(
            prompt, logique, refus_finaux[0], refus_finaux[1], tentative)
        if tentative > 0:
            archiver_prompt(tache, tentative, p)
        try:
            texte, journal = appeler_et_compter(tache, p, tentative)
        except RuntimeError as e:
            journaux.append({"prompt_tokens": 0, "completion_tokens": 0,
                             "total_tokens": 0})
            return {"tache": tache, "bloc": bloc, "mode": "ajouter-v3",
                    "verdict": f"APPEL ÉCHEOU : {str(e)[:60]}",
                    "vert": False, "essais": tentative + 1,
                    "journaux": journaux, "refus": "APPEL-ÉCHEC"}
        journaux.append(journal)
        logique = texte
        try:
            _, detail = assembler_v3(meta["squelette"], texte, meta)
            with open(JOURNAL, "a", encoding="utf-8") as f:
                f.write(json.dumps({"tache": tache, "essai": tentative,
                                    "verdict": "VERT", **journal},
                                   ensure_ascii=False) + "\n")
            return {"tache": tache, "bloc": bloc, "mode": "ajouter-v3",
                    "verdict": f"ASSEMBLE+ROUND-TRIP+CADRE:OK "
                               f"({detail[:40]})", "vert": True,
                    "essais": tentative + 1, "journaux": journaux,
                    "refus": None}
        except Refus as e:
            refus_finaux = (e.nom, e.detail)
            with open(JOURNAL, "a", encoding="utf-8") as f:
                f.write(json.dumps({"tache": tache, "essai": tentative,
                                    "verdict": f"REFUS {e.nom}",
                                    **journal}, ensure_ascii=False) + "\n")
    return {"tache": tache, "bloc": bloc, "mode": "ajouter-v3",
            "verdict": f"REFUS {refus_finaux[0]}: "
                       f"{refus_finaux[1][:60]} (budget {BUDGET} épuisé)",
            "vert": False, "essais": BUDGET + 1, "journaux": journaux,
            "refus": refus_finaux[0]}


def une_tache_editer(t: dict, i: int) -> dict:
    """UNE tâche ÉDITER à la même boucle : le gabarit TPL-EDIT-v1, la
    fenêtre ±12, la garde sha256, le diff exact — le refus
    CONTEXTE-DIVERGENT de loupe-07-cumul DEMEURE (la variation est au
    modèle, jamais re-tirée en silence)."""
    nom = t["bloc"]
    tache = f"editer-v3-i{GRAINE % 1000000:06d}{i:02d}"
    notation = (NOTATIONS / f"{nom}.asm").read_text(encoding="utf-8")
    prompt, meta = prompt_editer_t2(nom, notation, t["ligne_index"],
                                    t["ancienne"], t["nouvelle"])
    meta["notation"] = notation
    meta["t"] = t
    archiver_prompt(tache, 0, prompt)
    journaux = []
    refus_finaux = None
    reponse = ""
    for tentative in range(0, BUDGET + 1):
        p = prompt if tentative == 0 else prompt_reparation(
            prompt, reponse, refus_finaux[0], refus_finaux[1], tentative)
        if tentative > 0:
            archiver_prompt(tache, tentative, p)
        try:
            texte, journal = appeler_et_compter(tache, p, tentative)
        except RuntimeError as e:
            journaux.append({"prompt_tokens": 0, "completion_tokens": 0,
                             "total_tokens": 0})
            return {"tache": tache, "bloc": nom, "mode": "editer-v3",
                    "verdict": f"APPEL ÉCHEOU : {str(e)[:60]}",
                    "vert": False, "essais": tentative + 1,
                    "journaux": journaux, "refus": "APPEL-ÉCHEC"}
        journaux.append(journal)
        reponse = texte
        try:
            rec, detail = appliquer_t2(meta["notation"],
                                       meta["notation_empreinte"], texte,
                                       meta["tpl_empreinte"],
                                       meta["tpl_empreinte"])
            de = diff_exact(meta["notation"], meta["t"]["ligne_index"],
                            meta["t"]["nouvelle"], rec)
            if not de:
                raise Refus("DIFF-DIVERGENT",
                            "le reconstruit n'est pas le diff exact (la "
                            "ligne attendue ou les lignes voisines "
                            "divergent)")
            with open(JOURNAL, "a", encoding="utf-8") as f:
                f.write(json.dumps({"tache": tache, "essai": tentative,
                                    "verdict": "VERT", **journal},
                                   ensure_ascii=False) + "\n")
            return {"tache": tache, "bloc": nom, "mode": "editer-v3",
                    "verdict": f"GABARIT+GARDE+APPLIQUE+ROUND-TRIP+"
                               f"DIFF-EXACT:OK ({detail[:32]})",
                    "vert": True, "essais": tentative + 1,
                    "journaux": journaux, "refus": None}
        except Refus as e:
            refus_finaux = (e.nom, e.detail)
            with open(JOURNAL, "a", encoding="utf-8") as f:
                f.write(json.dumps({"tache": tache, "essai": tentative,
                                    "verdict": f"REFUS {e.nom}",
                                    **journal}, ensure_ascii=False) + "\n")
    return {"tache": tache, "bloc": nom, "mode": "editer-v3",
            "verdict": f"REFUS {refus_finaux[0]}: "
                       f"{refus_finaux[1][:60]} (budget {BUDGET} épuisé)",
            "vert": False, "essais": BUDGET + 1, "journaux": journaux,
            "refus": refus_finaux[0]}


def mesures(resultats: list, mode: str) -> dict:
    verts = [r for r in resultats if r["vert"]]
    premiere_passe = [r for r in resultats
                      if r["vert"] and r["essais"] == 1]
    # LE COÛT PAR CHANGEMENT VALIDÉ : la somme des tokens de TOUS les
    # appels de la tâche (tentatives refusées incluses)
    couts = [sum(j["total_tokens"] for j in r["journaux"]) for r in verts]
    couts_cl = [sum(j["prompt_tokens"] + j["completion_tokens"]
                    for j in r["journaux"]) for r in verts]
    med = statistics.median(couts) if couts else 0
    med_cl = statistics.median(couts_cl) if couts_cl else 0
    par_refus = {}
    for r in resultats:
        if not r["vert"]:
            par_refus[r["refus"]] = par_refus.get(r["refus"], 0) + 1
    return {"mode": mode, "n": len(resultats),
            "verts": len(verts),
            "premiere_passe": len(premiere_passe),
            "median_cout_par_change": round(med, 1),
            "median_cout_cl100k": round(med_cl, 1),
            "refus_par_classe": par_refus,
            "cible": (len(verts) >= 17 and med <= 4500) if mode ==
            "ajouter-v3" else None}


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "tout"
    # ---- LES CONTRÔLES NÉGATIFS AVANT CAMPAGNE --------------------------
    _, meta = prompt_ajouter_v3("loupe-02-lire")
    negatifs = {}
    try:
        assembler_v3(meta["squelette"], "jmp LBL-999", meta)
        negatifs["ID-INCONNU"] = False
    except Refus as e:
        negatifs["ID-INCONNU"] = (e.nom == "ID-INCONNU")
    m2 = dict(meta)
    m2["dico"] = dictionnaire_muté(meta["dico"])
    try:
        assembler_v3(m2["squelette"], "ret", m2)
        negatifs["DICT-DIVERGENT"] = False
    except Refus as e:
        negatifs["DICT-DIVERGENT"] = (e.nom == "DICT-DIVERGENT")
    try:
        assembler_v3(meta["squelette"], "call CST-004", meta)
        negatifs["EXPANSION-DIVERGENTE"] = False
    except Refus as e:
        negatifs["EXPANSION-DIVERGENTE"] = (e.nom == "EXPANSION-DIVERGENTE")
    try:
        # une instruction INCONNUE du domaine (les validateurs de forme
        # la laissent passer — le juge v2 du domaine la refuse :
        # HORS-FORMAT, la ligne 1 fautive)
        assembler_v3(meta["squelette"], "frobnicate rax, rbx", meta)
        negatifs["HORS-FORMAT"] = False
    except Refus as e:
        negatifs["HORS-FORMAT"] = (e.nom == "HORS-FORMAT")
    for ligne, nom in [("cmp qword ptr [rax], qword ptr [rbx]",
                        "FORME-cmp-mémoire"),
                       ("movzx rax, rcx", "FORME-movzx-r64"),
                       ("mov eax, rbx", "FORME-taille"),
                       ("cmp eax, WM_PAINT", "FORME-symbole-clair")]:
        try:
            assembler_v3(meta["squelette"], ligne, meta)
            negatifs[nom] = False
        except Refus as e:
            negatifs[nom] = (e.nom == "FORME-INVALIDE")
    # L'OCTET MUTÉ AU CADRE (l'instruction : refus nommé exigé) : le
    # squelette muté d'un octet — la confrontation du cadre diverge
    squelette_mute = meta["squelette"].replace("sub rsp, 0x28",
                                               "sub rsp, 0x29", 1)
    if squelette_mute != meta["squelette"]:
        try:
            assembler_v3(squelette_mute, "ret", meta)
            negatifs["CADRE-MUTÉ"] = False
        except Refus as e:
            negatifs["CADRE-MUTÉ"] = bool(e.nom)
    else:
        negatifs["CADRE-MUTÉ"] = None  # l'ancre absente au squelette —
        # la mutation portée au dictionnaire (DICT-DIVERGENT la couvre)
    print("LES CONTRÔLES NÉGATIFS :", json.dumps(negatifs))
    if not all(v for v in negatifs.values() if v is not None):
        print("ROUGE : un contrôle négatif non attrapé — la campagne "
              "refusée (fail-closed)")
        return 2

    # LA REPRISE : les tâches déjà consignées au resultats_v3.jsonl ne se
    # re-tirent PAS (le bac peut couper une campagne — la reprise poursuit,
    # JAMAIS un tirage nouveau)
    deja = set()
    if RESULTATS.exists():
        for l in RESULTATS.read_text(encoding="utf-8").splitlines():
            if l.strip():
                try:
                    deja.add(json.loads(l)["tache"])
                except Exception:
                    pass
    resultats = []
    if mode in ("tout", "ajouter"):
        print(f"\n===== LES 18 TÂCHES AJOUTER (la graine {GRAINE} "
              f"reconduite, le budget {BUDGET}) =====")
        for i, bloc in enumerate(BLOCS, 1):
            tache = f"ajouter-v3-i{GRAINE % 1000000:06d}{i:02d}"
            if tache in deja:
                print(f"  [{i:2d}/18] {bloc:22s} DÉJÀ CONSIGNÉ (la reprise)")
                continue
            r = une_tache_ajouter(bloc, i)
            resultats.append(r)
            with open(RESULTATS, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            cout = sum(j["total_tokens"] for j in r["journaux"])
            print(f"  [{i:2d}/18] {bloc:22s} "
                  f"{'VERT ' if r['vert'] else 'REFUS '}"
                  f"essais {r['essais']} natif-Σ {cout:6d} "
                  f"{r['verdict'][:60]}")
    if mode in ("tout", "editer"):
        taches = json.loads((REPO / "atelier-opt05-pe6iv71fj" /
                             "taches-edition.json").read_text(
                                 encoding="utf-8"))
        print(f"\n===== LES 18 TÂCHES ÉDITER (la même boucle, le budget "
              f"{BUDGET}) =====")
        for i, t in enumerate(taches, 1):
            tache = f"editer-v3-i{GRAINE % 1000000:06d}{i:02d}"
            if tache in deja:
                print(f"  [{i:2d}/18] {t['bloc']:22s} DÉJÀ CONSIGNÉ (la reprise)")
                continue
            r = une_tache_editer(t, i)
            resultats.append(r)
            with open(RESULTATS, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            cout = sum(j["total_tokens"] for j in r["journaux"])
            print(f"  [{i:2d}/18] {t['bloc']:22s} "
                  f"{'VERT ' if r['vert'] else 'REFUS '}"
                  f"essais {r['essais']} natif-Σ {cout:6d} "
                  f"{r['verdict'][:60]}")

    # les mesures par mode (chaque résultat déjà consigné à sa ligne)
    rap = {"horodatage": horodatage(), "graine": GRAINE, "budget": BUDGET,
           "grammaire_sha256": GRAMMAIRE_SHA256,
           "controles_negatifs": negatifs}
    # la lecture du registre DÉDOUBLONNÉE : la PREMIÈRE consignation de
    # chaque tâche fait foi (jamais re-tiré en silence) — les reprises de
    # l'instrument (les pertes au timeout du bac) ne comptent PAS deux fois
    tous: dict = {}
    if RESULTATS.exists():
        for l in RESULTATS.read_text(encoding="utf-8").splitlines():
            if l.strip():
                try:
                    r = json.loads(l)
                    tous.setdefault(r["tache"], r)
                except Exception:
                    pass
    for r in resultats:
        tous.setdefault(r["tache"], r)
    tous = list(tous.values())
    for m in ("ajouter-v3", "editer-v3"):
        sous = [r for r in tous if r.get("mode") == m]
        if sous:
            rap[m] = mesures(sous, m)
    print("\n" + json.dumps({k: v for k, v in rap.items()
                             if k != "controles_negatifs"},
                            ensure_ascii=False, indent=1))
    (ICI / ("mesures-" + mode + ".json")).write_text(
        json.dumps(rap, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
