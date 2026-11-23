#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_v6.py — TPL-ADD-v6 (7xuvsoqpuq, le geste suivant de yfkpml1j2) :
LA VOIE NOMMÉE du rapport v5, à la commande du maître (« go pour ce qui
reste » — l'Entrée 388 SUITE).

(1) LA RELANCE DES TROIS PERTES à graines identiques — loupe-11-defilement,
    loupe-16-saisie, loupe-04-cadre (vertes à la v4, refusées à la v5) :
    le prompt t0 REJOUÉ OCTET POUR OCTET (l'archive garde-prompts de la
    v5 recoupée byte-byte AVANT l'appel — fail-closed), la chaîne de
    réparation v5 reconduite à l'identique ; LA MESURE : la variance du
    sujet, jamais un re-tirage des tâches.
(2) LA PAIRE CONTRASTIVE DU CORPUS au prompt (la logique DPO du corpus
    2i7iy3xmg portée au prompt — l'entraînement AU GESTE DÉVELOPPEUR
    demeure, la voie du gym) : pour chaque classe chronique, UNE LIGNE
    RÉELLEMENT REFUSÉE au split TRAIN (extraction MÉCANIQUE — la cause
    nommée telle que le juge l'a rendue, jamais une ligne inventée) posée
    à côté du motif canonique admis.
(3) LE DÉCODAGE CONTRAINT : `z-ai chat --help` ne porte PAS response_format
    (vérifié à la congélation du plan 7xuvsoqpuq) — L'ÉCART D'INSTRUMENT
    NOMMÉ RECONDUIT ; la dégradation gracieuse demeure (la grammaire au
    prompt + les validateurs, JAMAIS un juge affaibli).

LES MÊMES 18 TÂCHES, graines 20261117, ordre JAMAIS re-tiré, budget 3,
LES JUGES INTACTS (assembler_v3 — la chaîne v2 + les validateurs v3 ; le
normalisateur canonique v5 reconduit)."""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
V5 = REPO / "atelier-ajouter-v5-yfkpml1j2"
V4 = REPO / "atelier-ajouter-v4-842vqyy1k"
CORPUS = REPO / "atelier-corpus-2i7iy3xmg" / "dataset"
ICI = REPO / "atelier-ajouter-v6-7xuvsoqpuq"
JOURNAL = ICI / "journal_v6.jsonl"
RESULTATS = ICI / "resultats_v6.jsonl"
GARDE = ICI / "garde-brut-v6.jsonl"
RELANCE = ICI / "registres" / "relance-3-pertes.jsonl"
BUDGET = 3
BLOCS = ["loupe-07-cumul", "loupe-11-defilement", "loupe-02-lire",
         "loupe-12-aller", "loupe-03-fermer", "loupe-10-peinture",
         "loupe-09-ecran", "loupe-17-sauver", "loupe-16-saisie",
         "loupe-13-recherche", "loupe-14-suivant", "loupe-18-quitter",
         "loupe-06-md5", "loupe-15-curseur", "loupe-04-cadre",
         "loupe-08-ligne", "loupe-01-ouvrir", "loupe-05-sha256"]
# LES TROIS PERTES v4→v5 (le rapport yfkpml1j2) : les indices dans BLOCS.
PERTES = [(1, "loupe-11-defilement"), (8, "loupe-16-saisie"),
          (14, "loupe-04-cadre")]

sys.path.insert(0, str(V5))
from campagne_v5 import (normaliser, prompt_reparation_v5,        # noqa: E402
                         prompt_ajouter_v5)
import campagne_v5 as CV5                                            # noqa: E402
sys.path.insert(0, str(V4))
from campagne_v4 import CONTRE_EXEMPLE                              # noqa: E402
import client_v3 as C3                                               # noqa: E402
from client_v3 import assembler_v3                                   # noqa: E402
from client_v2 import construire_dictionnaire                        # noqa: E402
from client_gabarits import Refus                                    # noqa: E402


# ----------------------------- LA PAIRE CONTRASTIVE (extraction mécanique) --
MOTIFS_ADMIS = {
    "HORS-FORMAT":
        "une instruction par ligne, la forme « mnémonique opérande, "
        "opérande » aux trous typés — le littéral COMPLET (jamais tronqué), "
        "pas de préfixe de chaîne REP, pas d'étiquette accolée",
    "ID-INCONNU":
        "les IDs vivent au DICTIONNAIRE du bloc (CST-001..NNN, "
        "LBL-001..NNN — l'énumération du prompt), jamais un symbole en clair",
    "EXPANSION-DIVERGENTE":
        "« mov reg, CST-001 » pour une constante ; « call CST-004 » pour "
        "l'IAT ; « jcc LBL-001 » pour un saut interne — l'ID au trou typé",
}


def extraire_contrastif() -> dict:
    """LA FACE REJETÉE par classe : la PREMIÈRE ligne REFUSÉE du split
    TRAIN (l'ordre du fichier, déterministe) — la cause nommée du juge
    VERBATIM (le champ diff), la ligne fautive extraite PAR CODE (le
    littéral quoté au diff, sinon l'ID nommé dans la cause, cherché dans
    la réponse refusée). JAMAIS une ligne inventée."""
    paires = {}
    for ligne in (CORPUS / "train.jsonl").read_text(
            encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        d = json.loads(ligne)
        classe = d.get("classe_de_refus")
        if d.get("verdict") != "REFUS" or classe not in MOTIFS_ADMIS:
            continue
        if classe in paires:            # la première par classe (l'ordre du
            continue                    # fichier — déterministe)
        diff = d["diff"]
        cause = diff.split("REFUS ", 1)[1].split(" (budget")[0].strip()
        # (a) le littéral quoté au diff : '…' ou « … »
        ligne_fautive = None
        m = re.search(r"[:«] '([^']+)'", diff) or re.search(
            r"assemblable : '([^']+)'", diff)
        if not m:
            m = re.search(r"« ([^»]+) »", cause)
        if m:
            ligne_fautive = m.group(1)
        else:
            # (b) l'ID nommé dans la cause, cherché dans la réponse refusée
            m2 = re.search(r"\b((?:LBL|CST)-\d{3})\b", cause)
            if m2:
                ident = m2.group(1)
                for l in d["reponse"].split("\n"):
                    if ident in l:
                        ligne_fautive = l.strip()
                        break
                if ligne_fautive is None:
                    ligne_fautive = ident
            else:
                ligne_fautive = cause[:60]
        paires[classe] = {"ligne": ligne_fautive, "cause": cause,
                          "triple": d["triple"]}
    return paires


def section_contrastive(paires: dict) -> str:
    """LA SECTION v6 AU PROMPT : la face rejetée (réelle, la cause du
    juge verbatim) POSÉE à côté de la face choisie (le motif canonique
    admis) — la logique DPO portée au prompt."""
    out = ["LA PAIRE CONTRASTIVE DU CORPUS (des lignes RÉELLEMENT REFUSÉES "
           "au corpus — la face rejetée avec LA CAUSE NOMMÉE du juge, la "
           "face choisie le motif canonique ; l'entraînement demeure au "
           "gym, jamais ici) :"]
    for classe in ("HORS-FORMAT", "ID-INCONNU", "EXPANSION-DIVERGENTE"):
        p = paires.get(classe)
        if not p:
            continue                    # fail-ouvert INTERDIT : la classe
        out.append(f"— REFUSÉE ({classe}) : « {p['ligne']} » — le juge : "
                   f"« {p['cause']} » → ADMISE : {MOTIFS_ADMIS[classe]}")
    return "\n".join(out)


def prompt_ajouter_v6(nom_bloc: str) -> tuple:
    """LE PROMPT v6 = le v5 (la grammaire + l'exemplaire scellé + le
    squelette à trous typés + la note du normalisateur) + LA PAIRE
    CONTRASTIVE DU CORPUS."""
    prompt_v5, meta = prompt_ajouter_v5(nom_bloc)
    paires = extraire_contrastif()
    assert len(paires) == 3, ("l'extraction contrastive doit rendre les "
                              "trois classes (le TRAIN du corpus)")
    insertion = ("\n" + section_contrastive(paires) + "\n")
    marqueur = "REQUÊTE : écris UNIQUEMENT LES LIGNES DE LA LOGIQUE"
    assert marqueur in prompt_v5, "le marqueur du prompt v5 a bougé"
    prompt = prompt_v5.replace(marqueur, insertion + "\n" + marqueur, 1)
    meta = dict(meta)
    meta["leviers"] = list(meta.get("leviers", [])) + [
        "paire-contrastive-corpus"]
    meta["leviers_v6"] = section_contrastive(paires)
    return prompt, meta


# --------------------------------------------------------------- L'APPEL ----
def appeler_et_compter(tache, essai, prompt, phase="campagne"):
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
            "tache": tache, "essai": essai, "phase": phase,
            "verdict": "APPEL",
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "secondes": round(dt, 1), "source": "log-api",
            "id": d.get("id", ""), "modele": d.get("model", "")},
            ensure_ascii=False) + "\n")
    return contenu, usage.get("total_tokens", 0)


# ------------------------------------------------- LA BOUCLE D'UNE TÂCHE ----
def boucle_tache(tache: str, bid: str, prompt, meta, phase="campagne") -> dict:
    """LA MÊME BOUCLE que la v5 : émettre → normaliser → assembler (LE
    JUGE) → le diff structuré au refus → budget 3. Les juges INTACTS."""
    squelette = meta.get("squelette", "")
    dico = construire_dictionnaire(bid)
    logique, refus = None, ("", "")
    journaux = []
    for essai in range(BUDGET + 1):
        p = prompt if essai == 0 else prompt_reparation_v5(
            prompt, logique or "", refus[0], refus[1], essai, dico)
        (ICI / "garde-prompts").mkdir(exist_ok=True)
        (ICI / "garde-prompts" / f"{tache}-t{essai}.txt").write_text(p)
        contenu, total = appeler_et_compter(tache, essai, p, phase)
        journaux.append({"essai": essai, "total": total})
        canonique = normaliser(contenu)
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


# --------------------------------------- (1) LA RELANCE DES TROIS PERTES ----
def relance() -> int:
    """LA PRÉFACE : les trois pertes rejouées à graines identiques — le
    prompt t0 RECROUPÉ byte-byte à l'archive v5 AVANT l'appel (fail-
    closed : un écart = REFUS NOMMÉ, aucun appel), la chaîne de réparation
    v5 reconduite à l'identique."""
    print("=== (1) LA RELANCE DES TROIS PERTES (graines identiques) ===",
          flush=True)
    deja = {}
    if RELANCE.exists():
        for l in RELANCE.read_text().splitlines():
            if l.strip():
                d = json.loads(l)
                deja[d["tache"]] = d
    for k, bid in PERTES:
        v5t = f"ajouter-v5-i261117{k+1:02d}"
        tache = f"relance-{v5t}"
        if tache in deja:
            print(f"  {tache} : déjà courue ({deja[tache]['verdict']})",
                  flush=True)
            continue
        # LA RECOUPE byte-byte AVANT TOUT APPEL (fail-closed)
        archive = V5 / "garde-prompts" / f"{v5t}-t0.txt"
        reconstruit, meta = prompt_ajouter_v5(bid)
        if not archive.exists():
            raise SystemExit(f"REFUS NOMMÉ : l'archive v5 {archive.name} "
                             "est absente — la relance exige le prompt t0 "
                             "octet pour octet")
        if archive.read_text(encoding="utf-8") != reconstruit:
            raise SystemExit("REFUS NOMMÉ : la reconstruction du prompt t0 "
                             f"diverge de l'archive v5 ({v5t}) — AUCUN "
                             "appel couru (des graines identiques exigées)")
        r = boucle_tache(tache, bid, reconstruit, meta, phase="relance")
        r["relance_de"] = v5t
        r["prompt_t0_recoupe"] = "byte-byte à l'archive v5"
        with open(RELANCE, "a") as f:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"  {tache} ({bid}) : {r['verdict']} en {r['essais']} essai(s)",
              flush=True)
        time.sleep(15)
    return 0


# -------------------------------------------- (2) LA CAMPAGNE DES 18 TÂCHES -
def campagne() -> int:
    print("=== (2) LA CAMPAGNE v6 : LES 18 TÂCHES, la paire contrastive "
          "au prompt ===", flush=True)
    fait = {}
    if RESULTATS.exists():
        for l in RESULTATS.read_text().splitlines():
            if l.strip():
                d = json.loads(l)
                fait[d["tache"]] = d
    for i, bid in enumerate(BLOCS):
        tache = f"ajouter-v6-i261117{i+1:02d}"
        if tache in fait:
            continue
        prompt, meta = prompt_ajouter_v6(bid)
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
    print(f"[fin] AJOUTER v6 {nb}/{len(verts)} verts ; coût médian par "
          f"changement validé {med} natifs ; cible ≥15/18 ET ≤4500",
          flush=True)
    return 0


def main() -> int:
    print("=== TPL-ADD-v6 (7xuvsoqpuq) : la voie nommée — la relance, la "
          "paire contrastive, l'écart d'instrument nommé ===", flush=True)
    relance()
    campagne()
    return 0


if __name__ == "__main__":
    sys.exit(main())
