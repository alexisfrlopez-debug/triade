#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_v5.py — TPL-ADD-v5 (yfkpml1j2, la vague 15) : porter AJOUTER
de 7/18 à ≥15/18 au coût médian ≤ 4 500 tokens par changement validé, SANS
AFFAIBLIR AUCUN JUGE.
LE LEVIER v5 — LA RÉPARATION PAR DIFF D'EXPANSION STRUCTURÉ :
  (1) LE NORMALISEUR CANONIQUE à la sortie du modèle : les commentaires
      réduits, les espaces canoniques, la casse des étiquettes d'ID en
      MAJUSCULES — la forme canonique est celle que le juge compare
      DÉJÀ (aucun juge affaibli, les validateurs v3 et la chaîne v2
      INTACTS) ;
  (2) LE DIFF STRUCTURÉ au refus : la ligne fautive rendue à TROIS
      étages — TELLE QU'ÉCRITE / SON EXPANSION (ce que l'expandeur en
      fait : l'ID résolu, le déplacement calculé à l'adresse — ou le
      point exact où l'expansion CASSE) / LE MOTIF CANONIQUE ADMIS ;
  (3) LA GRAMMAIRE À TROUS TYPÉS VERSIONNÉE PAR DOMAINE (le dictionnaire
      du bloc porte les types aux trous) ;
  (4) L'EXEMPLAIRE PAR PLUS PROCHE CONTRAT (le v4 reconduit).
LES MÊMES 18 TÂCHES, graines 20261117, ordre JAMAIS re-tiré, budget 3."""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
V4 = REPO / "atelier-ajouter-v4-842vqyy1k"
ICI = REPO / "atelier-ajouter-v5-yfkpml1j2"
JOURNAL = ICI / "journal_v5.jsonl"
RESULTATS = ICI / "resultats_v5.jsonl"
GARDE = ICI / "garde-brut-v5.jsonl"
BUDGET = 3
BLOCS = ["loupe-07-cumul", "loupe-11-defilement", "loupe-02-lire",
         "loupe-12-aller", "loupe-03-fermer", "loupe-10-peinture",
         "loupe-09-ecran", "loupe-17-sauver", "loupe-16-saisie",
         "loupe-13-recherche", "loupe-14-suivant", "loupe-18-quitter",
         "loupe-06-md5", "loupe-15-curseur", "loupe-04-cadre",
         "loupe-08-ligne", "loupe-01-ouvrir", "loupe-05-sha256"]

sys.path.insert(0, str(V4))
from campagne_v4 import exemplaire_proche, CONTRE_EXEMPLE  # noqa: E402
import campagne_v4 as CV4                                                   # noqa: E402
import client_v3 as C3                                                      # noqa: E402
from client_v3 import assembler_v3                                          # noqa: E402
from client_v2 import construire_dictionnaire, expandir_ligne               # noqa: E402
from client_gabarits import Refus                                           # noqa: E402


# --------------------------------------------- LE NORMALISEUR CANONIQUE ----
def normaliser(logique: str) -> str:
    """LA FORME CANONIQUE (celle que le juge compare déjà) : les
    commentaires après « ; » jetés, les espaces réduits, les étiquettes
    d'ID en MAJUSCULES — AUCUNE forme interdite n'y devient admise (les
    validateurs voient la forme canonique : la normalisation ne touche
    NI les mnémoniques NI les opérandes NI les littéraux)."""
    lignes = []
    for l in logique.replace("\r\n", "\n").split("\n"):
        l = l.split(";")[0].rstrip()
        l = re.sub(r"\s+", " ", l.strip())
        m = re.match(r"^(lbl|cst)-(\d{3})\s*:$", l.lower())
        if m:
            l = f"{m.group(1).upper()}-{m.group(2)} :"
        lignes.append(l)
    return "\n".join(lignes)


# --------------------------------- LE DIFF D'EXPANSION STRUCTURÉ (v5) ------
def diff_expansion(ligne: str, dico: dict, adresse: int) -> str:
    """LA LIGNE À TROIS ÉTAGES : TELLE QU'ÉCRITE / SON EXPANSION (le
    point exact où elle casse) / LE MOTIF CANONIQUE ADMIS — au niveau
    opcode/opérande/offset, JAMAIS un diff de texte."""
    etage1 = f"  ÉCRIT    : {ligne.strip()}"
    try:
        e = expandir_ligne(ligne.strip(), dico, adresse)
        return etage1 + f"\n  EXPANSION: {e}   [l'expandeur l'admet]"
    except Refus as r:
        cause = str(r.args[1]) if len(r.args) > 1 else str(r)
        return (etage1 + f"\n  EXPANSION: CASSE — {r.args[0]} : {cause}"
                f"\n  ADMIS    : {motif_canonique(ligne, r.args[0])}")
    except Exception as e:
        return (etage1 + f"\n  EXPANSION: CASSE — {type(e).__name__}"
                f"\n  ADMIS    : {motif_canonique(ligne, 'HORS-FORMAT')}")


def motif_canonique(ligne: str, nom_refus: str) -> str:
    """LE MOTIF CANONIQUE par classe de refus — le gabarit de la
    grammaire, jamais un texte libre."""
    l = ligne.strip()
    if re.match(r"^(lbl|cst)-\d+\s*:", l, re.I):
        return ("l'étiquette INTERNE : « LBL-001 : » (MAJUSCULES, le trou "
                "typé cible de saut — elle se déclare à la ligne SEULE)")
    if re.match(r"^(db|dw|dd|dq|resb|resq)\b", l, re.I):
        return ("AUCUNE donnée inline à la logique (la donnée vit au "
                "CADRE du squelette) — la logique ne porte QUE des "
                "instructions : la chaîne s'écrit par les appels CST du "
                "dictionnaire")
    if re.search(r"\b(rep|repne|repe|scas|stos|movs|lods)\b", l, re.I):
        return ("les instructions à préfixe de chaîne HORS domaine — le "
                "motif canonique : « cmp byte ptr [rsi], CST-001 » puis "
                "le saut conditionnel LBL")
    if nom_refus == "ID-INCONNU":
        return ("l'ID doit vivre AU DICTIONNAIRE du bloc (CST-001..NNN, "
                "LBL-001..NNN — l'énumération du prompt) ; jamais un "
                "symbole en clair")
    if nom_refus == "EXPANSION-DIVERGENTE":
        return ("la cible d'appel : « call CST-004 » (l'IAT s'appelle en "
                "call) ; l'opérande : « mov reg, CST-001 » pour une "
                "constante ; « jcc LBL-001 » pour un saut interne")
    if l.count("qword ptr [") >= 2 or l.count("ptr [") >= 2:
        return ("PAS d'opérande mémoire DOUBLE : « mov rax, qword ptr "
                "[rbx] » PUIS « cmp rax, CST-001 » — un accès mémoire par "
                "instruction au plus")
    return ("une instruction par ligne, la forme « mnémonique opérande, "
            "opérande » aux trous TYPÉS du dictionnaire (registre / "
            "offset / cible LBL/CST)")


def prompt_ajouter_v5(nom_bloc: str) -> tuple:
    """LE PROMPT v5 : le v4 (la grammaire + l'exemplaire + le squelette à
    trous typés) + LA NOTE DU NORMALISEUR (la forme canonique attendue)."""
    prompt_v4, meta = CV4.prompt_ajouter_v4(nom_bloc)
    insertion = (
        "\nLA FORME CANONIQUE (ta sortie est normalisée avant le juge — "
        "les commentaires après « ; » jetés, les espaces réduits, les "
        "étiquettes en MAJUSCULES « LBL-001 : ») : écris DÉJÀ la forme "
        "canonique ; le normalisateur ne corrigera JAMAIS une forme "
        "interdite (donc : pas de « db », pas de préfixe de chaîne REP, "
        "pas d'étiquette minuscule accolée à une instruction).\n"
    )
    marqueur = "REQUÊTE : écris UNIQUEMENT LES LIGNES DE LA LOGIQUE"
    assert marqueur in prompt_v4, "le marqueur du prompt v4 a bougé"
    prompt = prompt_v4.replace(marqueur, insertion + "\n" + marqueur, 1)
    meta = dict(meta)
    meta["leviers"] = ["grammaire-v3", "exemplaire-proche-contrat",
                       "squelette-trous-typés",
                       "normalisateur-canonique", "diff-expansion-structuré"]
    return prompt, meta


def prompt_reparation_v5(prompt, logique_fautif, refus_nom, refus_detail,
                         tentative, dico):
    """LE LEVIER v5 : LE DIFF D'EXPANSION STRUCTURÉ — chaque ligne
    fautive à TROIS étages (écrit/expansion/le motif admis), le niveau
    opcode/opérande/offset, les motifs canoniques."""
    lignes = [l for l in (logique_fautif or "").split("\n") if l.strip()]
    k = None
    m = re.search(r"la ligne (\d+)", refus_detail)
    if m:
        k = int(m.group(1)) - 1
    vue = []
    adresse = 0x10000
    for i, l in enumerate(lignes):
        if k is None or i == k:
            vue.append(diff_expansion(l, dico, adresse))
        adresse += 8
    diff = "\n".join(vue[:8])
    return (C3.prompt_reparation(prompt, logique_fautif, refus_nom,
                                 refus_detail, tentative)
            + "\nLE DIFF D'EXPANSION STRUCTURÉ (au niveau "
            "opcode/opérande/offset — TELLE QU'ÉCRITE / CE QUE "
            "L'EXPANDEUR EN FAIT / LE MOTIF ADMIS) :\n" + diff + "\n"
            + CONTRE_EXEMPLE)


def appeler_et_compter(tache, essai, prompt):
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
    tache = f"ajouter-v5-i261117{i+1:02d}"
    prompt, meta = prompt_ajouter_v5(bid)
    squelette = meta.get("squelette", "")
    dico = construire_dictionnaire(bid)
    logique, refus = None, ("", "")
    journaux = []
    for essai in range(BUDGET + 1):
        p = prompt if essai == 0 else prompt_reparation_v5(
            prompt, logique or "", refus[0], refus[1], essai, dico)
        (ICI / "garde-prompts").mkdir(exist_ok=True)
        (ICI / "garde-prompts" / f"{tache}-t{essai}.txt").write_text(p)
        contenu, total = appeler_et_compter(tache, essai, p)
        journaux.append({"essai": essai, "total": total})
        canonique = normaliser(contenu)
        try:
            assembler_v3(squelette, canonique, meta)
            return {"tache": tache, "bloc": bid, "vert": True,
                    "essais": essai + 1, "journaux": journaux,
                    "verdict": "VERT"}
        except Refus as e:
            refus = (e.args[0],
                     str(e.args[1])[:400] if len(e.args) > 1 else "")
            logique = canonique
        except Exception as e:
            refus = (type(e).__name__, str(e)[:400])
            logique = canonique
    return {"tache": tache, "bloc": bid, "vert": False,
            "essais": BUDGET + 1, "journaux": journaux,
            "verdict": f"REFUS {refus[0]}"}


def main() -> int:
    print("=== TPL-ADD-v5 : LE DIFF D'EXPANSION STRUCTURÉ (yfkpml1j2) ===",
          flush=True)
    fait = {}
    if RESULTATS.exists():
        for l in RESULTATS.read_text().splitlines():
            if l.strip():
                d = json.loads(l)
                fait[d["tache"]] = d
    for i, bid in enumerate(BLOCS):
        tache = f"ajouter-v5-i261117{i+1:02d}"
        if tache in fait:
            continue
        r = une_tache(i, bid)
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
    print(f"[fin] AJOUTER {nb}/{len(verts)} verts ; coût médian par "
          f"changement validé {med} natifs ; cible ≥15/18 ET ≤4500",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
