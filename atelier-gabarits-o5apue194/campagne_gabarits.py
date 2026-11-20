#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_gabarits.py — LA CAMPAGNE DE L'INSTRUCTION o5apue194 (la vague
11, le PLAN-O5APUE194.md gelé, empreinte consignée à
EMPREINTES-PLANS-VAGUE11.txt AVANT la première donnée) : LA PROSE
DOMINANTE DE L'OPÉRATION ÉDITER — le gabarit versionné, le localiser
hiérarchique, l'ajout par squelette.

LES SIX CELLULES (n=18, LA MÊME GRAINE 20261117, l'ordre JAMAIS re-tiré —
l'ordre consigné à verites-terrain.json, lu tel quel) :
  éditer : AVANT éditer-F2 (la fenêtre ±12 de la vague 10 re-mesurée à la
           même graine) PUIS éditer-T2 (LE GABARIT VERSIONNÉ TPL-EDIT-v1 :
           l'ID + l'empreinte + les paramètres littéraux — le corps du
           gabarit vit UNE FOIS par session, jamais dans l'opération) ;
  localiser : AVANT localiser-P (le pointeur seul, le gabarit de la
           campagne cq01qv1za/RQ2 TEL QUEL) PUIS localiser-H (le
           HIÉRARCHIQUE : l'index grossier de session + l'entrée fine
           après choix — la réponse le pointeur littéral, le record 52) ;
  ajouter : AVANT ajouter-H3 (le record — la grammaire v2 + l'exemple
           complet, la formulation de la vague 9 TELLE QUELLE, le format
           refusé à trois reprises) PUIS ajouter-S (LE SQUELETTE
           DÉTERMINISTE dérivé de la couche I — l'agent ne remplit que la
           logique).

L'INSTRUMENT : le CLI z-ai, le champ usage LU (le tokenizer natif —
prompt_tokens/completion_tokens/total_tokens), chaque appel journalisé au
JSONL (journal_gabarits.jsonl) ; cl100k PARALLÈLE + la re-tokenisation
indépendante à ±1. LA DÉCOMPOSITION matériau/prose/réponse consignée
séparément (cl100k, la convention de périmètre).

LA CONFRONTATION (fail-closed, AUCUN contrôle retiré) : le round-trip
keystone/capstone du client v8 TEL QUEL ; la garde sha256 de la notation
complète (CONTEXTE-DIVERGENT) ; la fenêtre ±12 DEMEURE ; la garde
d'empreinte du gabarit (GABARIT-DIVERGENT) ; l'expansion du pointeur
recoupée (POINTEUR-INCONNU, HORS-FORMAT, EMPREINTE-DIVERGENTE,
EXPANSION-DIVERGENTE) ; LE DIFF EXACT (le critère renforcé : le
reconstruit == la notation au diff exact de la tâche — l'insertion-only
sans retrait serait un round-trip vert mais un diff divergent).

Les refus nommés sont CONSIGNÉS, jamais re-tirés (le journal fait foi —
la reprise idempotente). Les pilotes de formulation vivent à part
(journal_pilotes.jsonl) — JAMAIS comptés."""
from __future__ import annotations

import datetime as dt
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
sys.path.insert(0, str(ICI))

import tiktoken  # noqa: E402

from campagne_opt05 import (CONVENTIONS, FORMAT_HUNK, GABARIT_BASE,  # noqa: E402
                            charger as charger_v8)
from client_hunks_v2 import traiter as traiter_v2, Refus  # noqa: E402
from client_hunks import round_trip  # noqa: E402

from client_gabarits import (  # noqa: E402
    FENETRE_N, NOTATIONS, TPL_ID, TPL_CHEMIN, INDEX_CHEMIN, SQUELETTES_DIR,
    charger_tpl, charger_index, table_carte, sha256_texte,
    prompt_editer_t2, appliquer_t2, diff_exact,
    prompt_localiser_h, confronte_h, RefusPointeur, expanser_pointeur,
    generer_squelette, prompt_ajouter_s, assembler_s)

JOURNAL = ICI / "journal_gabarits.jsonl"
JOURNAL_PILOTES = ICI / "journal_pilotes.jsonl"
GARDE = ICI / "garde-brut.jsonl"
GARDE_PILOTES = ICI / "garde-pilotes.jsonl"
PROMPTS = ICI / "garde-prompts"
RESULTATS = ICI / "resultats_gabarits.jsonl"
RESULTATS_JSON = ICI / "resultats_gabarits.json"
RAPPORT = ICI / "rapport-gabarits.txt"

CL100K = tiktoken.get_encoding("cl100k_base")
GRAPPE = "T"          # le bras (l'opération mesurée)


# ------------------------------------------------------------- l'instrument
def horodatage() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def appeler_et_compter(phase: str, tache: str, prompt: str,
                       journal: pathlib.Path = JOURNAL,
                       garde: pathlib.Path = GARDE,
                       system: str | None = None) -> tuple[str, dict]:
    """LE PATRON D'APPEL (la campagne OPT-10 reconduite) : le CLI z-ai,
    la réponse JSON lue, le champ usage JOURNALISÉ — le compte est le
    LOG, jamais une estimation."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                     delete=False, encoding="utf-8") as f:
        chemin = pathlib.Path(f.name)
    cmd = ["z-ai", "chat", "--prompt", prompt, "-o", str(chemin)]
    if system:
        cmd += ["--system", system]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if proc.returncode != 0:
        chemin.unlink(missing_ok=True)
        raise RuntimeError(f"l'appel z-ai a échoué : {proc.stderr[:300]}")
    reponse = json.loads(chemin.read_text(encoding="utf-8"))
    with open(garde, "a", encoding="utf-8") as f:
        f.write(json.dumps({"horodatage": horodatage(), "bras": GRAPPE,
                            "phase": phase, "tache": tache,
                            "reponse_api": reponse},
                           ensure_ascii=False) + "\n")
    usage = reponse.get("usage") or {}
    texte = (reponse.get("choices") or [{}])[0].get("message",
                                                    {}).get("content", "")
    ligne = {
        "horodatage": horodatage(), "bras": GRAPPE, "phase": phase,
        "tache": tache, "id": reponse.get("id", ""),
        "modele": reponse.get("model", ""),
        "prompt_tokens": int(usage.get("prompt_tokens", 0)),
        "completion_tokens": int(usage.get("completion_tokens", 0)),
        "total_tokens": int(usage.get("total_tokens", 0)),
        "somme_coherente": (int(usage.get("prompt_tokens", 0))
                            + int(usage.get("completion_tokens", 0))
                            == int(usage.get("total_tokens", 0))),
        "sha256_echange": hashlib.sha256(
            (prompt + "\x00" + texte).encode("utf-8")).hexdigest(),
        "source": "log-api",
    }
    chemin.unlink(missing_ok=True)
    with open(journal, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return texte, ligne


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


# ------------------------------------------------- les gabarits AVANT (verbatim)
# LE GABARIT F2 — la fenêtre ±12 de la vague 10, COPIÉ OCTET POUR OCTET
# de campagne_fenetre.py (atelier-fenetre-mqf258e4l — jamais touché)
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
    """LE CLIENT F2 (la vague 10 TEL QUEL) : la recoupe de l'empreinte
    (CONTEXTE-DIVERGENT), l'application des hunks, le round-trip."""
    emp_cache = hashlib.sha256(notation_cache.encode("utf-8")).hexdigest()
    if emp_cache != empreinte_prompt:
        raise Refus("CONTEXTE-DIVERGENT",
                    f"l'empreinte du cache {emp_cache[:16]}… != l'empreinte "
                    f"du prompt {empreinte_prompt[:16]}… — la base a divergé")
    return traiter_v2(notation_cache, reponse)


# LE GABARIT P — le pointeur seul, COPIÉ OCTET POUR OCTET de
# remesure_rq2_pointeur.py (la re-mesure RQ2 — la vague 8)
GABARIT_P = (
    "L'OPÉRATION LOCALISER DE LA CARTE TRIADE (le mode pointeur seul — la\n"
    "réponse tient en une ligne, le client expande le pointeur auprès de la\n"
    "carte et confronte l'empreinte aux octets réels).\n"
    "\n"
    "BLOC DE LA CARTE (entête lu du fichier même) :\n"
    "{entete}\n"
    "Empreinte notation : sha256:{empreinte}\n"
    "\n"
    "REQUÊTE : localise le bloc ci-dessus dans la carte et réponds AU FORMAT\n"
    "POINTEUR SEUL, une seule ligne exactement :\n"
    "IDENTIFIANT · sha256:<empreinte>\n"
    "— IDENTIFIANT : l'identifiant de bloc de la carte (la forme iNNNNNN de\n"
    "l'entête) ;\n"
    "— <empreinte> : l'empreinte sha256 recopiée TELLE QUELLE de la ligne\n"
    "« Empreinte notation » ci-dessus (64 hexadécimaux, aucun calcul).\n"
    "Rien d'autre.\n"
)


# LE GABARIT H3 — le record, COPIÉ OCTET POUR OCTET de campagne_vague9.py
# (atelier-tokens-uagz3fby7 — jamais touché)
def gabarit_ajouter_h3(contrat: str, exemple: str) -> str:
    return (
        "L'OPÉRATION AJOUTER DE LA CARTE TRIADE (le mode HUNKS — l'unité se\n"
        "compose PAR HÉRITAGE du gabarit de famille : la réponse ne rend QUE\n"
        "les hunks, le client les applique au gabarit et confronte).\n\n"
        f"LE CONTRAT DE COUCHE I (mot pour mot) :\n{contrat}\n\n"
        f"{CONVENTIONS}\n"
        "L'EXEMPLE DU FORMAT DE NOTATION (loupe-13, la notation RÉELLE du\n"
        "domaine — le format des lignes « + » de tes hunks) :\n"
        f"{exemple}\n\n"
        f"{FORMAT_HUNK}\n"
        "UN EXEMPLE COMPLET DE RÉPONSE D'AJOUT (le bloc qui vérifie un "
        "tampon non vide et rend sa taille — la réponse ENTIÈRE, "
        "caractère pour caractère, telle que le client l'attend) :\n"
        "@@ hunk 1\n"
        "base: ; --- LE CORPS DU BLOC ICI ---\n"
        "+ test rcx, rcx\n"
        "+ jz 0x1234\n"
        "+ mov rax, rdx\n"
        "+ jmp 0x1250\n"
        "+ mov eax, -5\n"
        "+ jmp 0x1250\n"
        "@@ hunk 2\n"
        "base: add rsp, 0x20\n"
        "+ nop\n"
        "FIN-HUNKS\n"
        "(REMARQUE : la réponse ci-dessus est TOUTE la réponse — elle "
        "commence à « @@ hunk 1 » et finit à « FIN-HUNKS », AUCUNE ligne "
        "de la notation du gabarit n'est re-dumpée, AUCUNE explication.)\n"
        "REQUÊTE : compose le bloc et rends UNIQUEMENT les hunks qui "
        "insèrent le corps dans le gabarit — la première ligne de ta "
        "réponse est EXACTEMENT « @@ hunk 1 », la dernière exactement « "
        "FIN-HUNKS ».\n"
    )


# ------------------------------------------------------------ les cellules
def cellules(taches: dict, par_id: dict, exemple_l13: str):
    """LES SIX CELLULES — chacune : (mode, fabrique, confrontation).
    La fabrique rend (prompt, meta) ; la confrontation rend (verdict,
    vert, extras)."""

    def f_f2(nom: str, t: dict):
        notation = (NOTATIONS / f"{nom}.asm").read_text(encoding="utf-8")
        prompt, emp = gabarit_editer_fenetre(notation, t["ligne_index"],
                                             t["consigne"])
        li = t["ligne_index"]
        fen = "\n".join(notation.split("\n")[max(0, li - FENETRE_N):
                                           li + FENETRE_N + 1])
        return prompt, {"notation": notation, "emp": emp, "fenetre": fen,
                        "t": t}

    def c_f2(texte: str, meta: dict):
        try:
            rec, detail = appliquer_f2(meta["notation"], meta["emp"], texte)
        except Refus as e:
            return f"REFUS {e.nom}: {e.detail[:70]}", False, {}
        de = diff_exact(meta["notation"], meta["t"]["ligne_index"],
                        meta["t"]["nouvelle"], rec)
        v = (f"GARDE+APPLIQUE+ROUND-TRIP+{'DIFF-EXACT' if de else 'DIFF-DIVERGENT'}"
             f":OK ({detail[:38]})")
        return v, de, {"diff_exact": de}

    def f_t2(nom: str, t: dict, rappel: bool = True):
        notation = (NOTATIONS / f"{nom}.asm").read_text(encoding="utf-8")
        prompt, meta = prompt_editer_t2(nom, notation, t["ligne_index"],
                                        t["ancienne"], t["nouvelle"],
                                        rappel_marqueurs=rappel)
        meta["notation"] = notation
        meta["t"] = t
        return prompt, meta

    def c_t2(texte: str, meta: dict):
        try:
            rec, detail = appliquer_t2(meta["notation"],
                                       meta["notation_empreinte"], texte,
                                       meta["tpl_empreinte"],
                                       meta["tpl_empreinte"])
        except Refus as e:
            return f"REFUS {e.nom}: {e.detail[:70]}", False, {}
        de = diff_exact(meta["notation"], meta["t"]["ligne_index"],
                        meta["t"]["nouvelle"], rec)
        v = (f"GABARIT+GARDE+APPLIQUE+ROUND-TRIP+"
             f"{'DIFF-EXACT' if de else 'DIFF-DIVERGENT'}:OK ({detail[:34]})")
        return v, de, {"diff_exact": de}

    def f_p(nom: str, t: dict):
        entete = []
        for l in (NOTATIONS / f"{nom}.asm").read_text(
                encoding="utf-8").splitlines():
            if l.startswith(";"):
                entete.append(l)
            elif l.strip() == "":
                continue
            else:
                break
        emp = sha256_texte((NOTATIONS / f"{nom}.asm").read_text(
            encoding="utf-8"))
        prompt = GABARIT_P.format(entete="\n".join(entete), empreinte=emp)
        return prompt, {"emp": emp, "entete": "\n".join(entete)}

    def c_p(texte: str, meta: dict):
        table = table_carte()
        attendu = None
        for bid, b in table.items():
            if b["empreinte"] == meta["emp"]:
                attendu = f"{bid} · sha256:{meta['emp']}"
        if texte.strip() != attendu:
            return (f"DIVERGENT: {texte.strip()[:60]!r}", False, {})
        try:
            ex = expanser_pointeur(texte.strip(), table)
            return ("CONFORME+EXPANSION:OK (le pointeur exact)", True,
                    {"expansion": ex["id"]})
        except RefusPointeur as e:
            return f"REFUS {e.nom}: {e.detail[:70]}", False, {}

    def f_h(nom: str, t: dict):
        emp = sha256_texte((NOTATIONS / f"{nom}.asm").read_text(
            encoding="utf-8"))
        prompt, meta = prompt_localiser_h(emp)
        return prompt, meta

    def c_h(texte: str, meta: dict):
        try:
            ex = confronte_h(texte, meta["empreinte_requise"],
                             meta["empreinte_index"])
            return (f"CHOIX+EXPANSION:OK (l'entrée fine {ex['id']}, "
                    f"le pointeur exact)", True, {"expansion": ex["id"]})
        except RefusPointeur as e:
            return f"REFUS {e.nom}: {e.detail[:70]}", False, {}

    def f_h3(nom: str, t: dict):
        contrat = (REPO / "loupe" / "I" / f"{nom}.md").read_text(
            encoding="utf-8")
        prompt = gabarit_ajouter_h3(contrat, exemple_l13)
        return prompt, {"contrat": contrat}

    def c_h3(texte: str, meta: dict):
        try:
            _, detail = traiter_v2(GABARIT_BASE, texte)
            return (f"APPLIQUE+ROUND-TRIP:OK ({detail[:44]}) — LE RECORD "
                    f"RENVERSÉ (le format refusé à trois reprises)", True,
                    {"renverse": True})
        except Refus as e:
            return (f"REFUS {e.nom}: {e.detail[:70]} — LE RECORD TENU "
                    f"(le format demeure refusé)", False,
                    {"refus_consigne": e.nom})

    def f_s(nom: str, t: dict):
        prompt, infos = prompt_ajouter_s(nom)
        return prompt, {"infos": infos,
                        "squelette": infos["squelette"],
                        "contrat": infos["spec"]}

    def c_s(texte: str, meta: dict):
        try:
            _, detail = assembler_s(meta["squelette"], texte,
                                    meta["infos"])
            return (f"ASSEMBLE+ROUND-TRIP+CADRE:OK ({detail[:40]})",
                    True, {})
        except Refus as e:
            return f"REFUS {e.nom}: {e.detail[:70]}", False, {}

    return [
        ("editer-F2", f_f2, c_f2),
        ("editer-T2", f_t2, c_t2),
        ("localiser-P", f_p, c_p),
        ("localiser-H", f_h, c_h),
        ("ajouter-H3", f_h3, c_h3),
        ("ajouter-S", f_s, c_s),
    ]


# ------------------------------------------------------------ les décompositions
def decomposition(mode: str, prompt: str, meta: dict) -> dict:
    """LA DÉCOMPOSITION matériau/prose/réponse (cl100k, la convention de
    périmètre — les trois champs consignés séparément, jamais fusionnés) ;
    pour ajouter-S : la décomposition squelette/logique/prose DU PLAN § 4."""
    d = {}
    if mode == "editer-F2":
        d["materiau"] = len(CL100K.encode(meta["fenetre"]))
    elif mode == "editer-T2":
        t = meta["t"]
        params = (f"bloc : {meta['nom']}\n"
                  f"ligne : {t['ligne_index'] + 1}\n"
                  f"ancienne : {t['ancienne']}\n"
                  f"nouvelle : {t['nouvelle']}\n")
        d["materiau_fenetre"] = len(CL100K.encode(meta["fenetre"]))
        d["materiau_params"] = len(CL100K.encode(params))
        d["materiau"] = d["materiau_fenetre"] + d["materiau_params"]
    elif mode == "localiser-P":
        d["materiau"] = (len(CL100K.encode(meta["entete"]))
                         + len(CL100K.encode(
                             f"Empreinte notation : sha256:{meta['emp']}\n")))
    elif mode == "localiser-H":
        idx = charger_index()
        d["materiau_index"] = len(CL100K.encode(idx["document"]))
        d["materiau_requete"] = len(CL100K.encode(
            f"sha256:{meta['empreinte_requise']}\n"))
        d["materiau"] = d["materiau_index"] + d["materiau_requete"]
    elif mode == "ajouter-H3":
        exemple = (NOTATIONS / "loupe-13-recherche.asm").read_text(
            encoding="utf-8")
        d["materiau"] = (len(CL100K.encode(meta["contrat"]))
                         + len(CL100K.encode(exemple)))
    elif mode == "ajouter-S":
        d["materiau_contrat"] = len(CL100K.encode(meta["contrat"]))
        d["materiau_squelette"] = len(CL100K.encode(meta["squelette"]))
        d["materiau"] = d["materiau_contrat"] + d["materiau_squelette"]
    d["prose"] = len(CL100K.encode(prompt)) - d["materiau"]
    return d


# ------------------------------------------------------------ les pilotes
def pilotes() -> int:
    """LES PILOTES DE FORMULATION — journalisés À PART (journal_pilotes
    .jsonl), JAMAIS comptés : la mesure vit chaque tâche UNE fois, à
    l'ordre de la graine. Le pilote tranchera la question du rappel des
    marqueurs littéraux au prompt T2 (le plan § 2 (2) : l'opération porte
    l'ID, l'empreinte, les paramètres — le rappel est un ÉCART à nommer
    s'il est nécessaire)."""
    vt, taches_v8 = charger_v8()
    taches = {t["bloc"]: t for t in taches_v8.values()}
    notation13 = (NOTATIONS / "loupe-13-recherche.asm").read_text(
        encoding="utf-8")
    # la tâche pilote : loupe-13, la ligne 16 (jz → je — l'alias), une
    # révision DIFFÉRENTE de la tâche mesurée (la ligne 17, cmp 32 → 31)
    t_pilote = {"ligne_index": 16, "ancienne": "jz 0x57ab",
                "nouvelle": "je 0x57ab"}

    # (1) T2 SANS le rappel des marqueurs (la lettre pure du plan)
    prompt, meta = prompt_editer_t2("loupe-13-recherche", notation13, 16,
                                    "jz 0x57ab", "je 0x57ab",
                                    rappel_marqueurs=False)
    (PROMPTS / "pilote-T2-strict.txt").write_text(prompt, encoding="utf-8")
    texte, ligne = appeler_et_compter("pilote", "pilote-T2-strict", prompt,
                                      journal=JOURNAL_PILOTES,
                                      garde=GARDE_PILOTES)
    verdict = "(voir la confrontation ci-dessous)"
    try:
        rec, det = appliquer_t2(notation13, meta["notation_empreinte"],
                                texte, meta["tpl_empreinte"],
                                meta["tpl_empreinte"])
        de = diff_exact(notation13, 16, "je 0x57ab", rec)
        verdict = f"VERT strict : diff exact={de} — {det[:40]} | {texte[:90]!r}"
    except Refus as e:
        verdict = f"ÉCHEC strict : REFUS {e.nom} — {texte[:90]!r}"
    print(f"[pilote T2 strict] {ligne['total_tokens']} tokens — {verdict}",
          flush=True)

    # (2) T2 AVEC le rappel des marqueurs littéraux
    prompt, meta = prompt_editer_t2("loupe-13-recherche", notation13, 16,
                                    "jz 0x57ab", "je 0x57ab",
                                    rappel_marqueurs=True)
    (PROMPTS / "pilote-T2-recap.txt").write_text(prompt, encoding="utf-8")
    texte, ligne = appeler_et_compter("pilote", "pilote-T2-recap", prompt,
                                      journal=JOURNAL_PILOTES,
                                      garde=GARDE_PILOTES)
    try:
        rec, det = appliquer_t2(notation13, meta["notation_empreinte"],
                                texte, meta["tpl_empreinte"],
                                meta["tpl_empreinte"])
        de = diff_exact(notation13, 16, "je 0x57ab", rec)
        verdict = f"VERT récap : diff exact={de} — {det[:40]}"
    except Refus as e:
        verdict = f"ÉCHEC récap : REFUS {e.nom} — {texte[:90]!r}"
    print(f"[pilote T2 récap] {ligne['total_tokens']} tokens — {verdict}",
          flush=True)

    # (3) H — la formulation hiérarchique (le sujet : loupe-05)
    emp05 = sha256_texte((NOTATIONS / "loupe-05-sha256.asm").read_text(
        encoding="utf-8"))
    prompt, meta = prompt_localiser_h(emp05)
    (PROMPTS / "pilote-H.txt").write_text(prompt, encoding="utf-8")
    texte, ligne = appeler_et_compter("pilote", "pilote-H", prompt,
                                      journal=JOURNAL_PILOTES,
                                      garde=GARDE_PILOTES)
    try:
        ex = confronte_h(texte, meta["empreinte_requise"],
                         meta["empreinte_index"])
        verdict = f"VERT H : l'entrée fine {ex['id']}"
    except RefusPointeur as e:
        verdict = f"ÉCHEC H : REFUS {e.nom} — {texte[:80]!r}"
    print(f"[pilote H] {ligne['total_tokens']} tokens — {verdict}",
          flush=True)

    # (4) S — la formulation squelette (le sujet : loupe-13)
    prompt, infos = prompt_ajouter_s("loupe-13-recherche")
    (PROMPTS / "pilote-S.txt").write_text(prompt, encoding="utf-8")
    texte, ligne = appeler_et_compter("pilote", "pilote-S", prompt,
                                      journal=JOURNAL_PILOTES,
                                      garde=GARDE_PILOTES)
    try:
        _, det = assembler_s(infos["squelette"], texte, infos)
        verdict = f"VERT S : {det[:44]}"
    except Refus as e:
        verdict = f"ÉCHEC S : REFUS {e.nom}: {e.detail[:70]} — {texte[:80]!r}"
    print(f"[pilote S] {ligne['total_tokens']} tokens — {verdict}",
          flush=True)

    # (5) LES INSTALLATIONS DE SESSION — le corps du gabarit TPL-EDIT-v1 et
    # l'index grossier portés AU SYSTÈME (leur coût natif mesuré UNE fois,
    # amorti /18 à la session — le plan : ils vivent UNE FOIS par session)
    tpl_corps, tpl_emp = charger_tpl()
    texte, ligne_tpl = appeler_et_compter(
        "installation", f"installation-{TPL_ID}", "Accuse réception du "
        "gabarit de session en une ligne.", journal=JOURNAL_PILOTES,
        garde=GARDE_PILOTES, system=tpl_corps)
    print(f"[installation {TPL_ID}] prompt_tokens natifs : "
          f"{ligne_tpl['prompt_tokens']} (le corps du gabarit — amorti "
          f"/18 = {ligne_tpl['prompt_tokens'] / 18:.0f} par opération)",
          flush=True)
    idx = charger_index()
    texte, ligne_idx = appeler_et_compter(
        "installation", "installation-INDEX-GROSSIER", "Accuse réception "
        "de l'index de session en une ligne.", journal=JOURNAL_PILOTES,
        garde=GARDE_PILOTES, system=idx["document"])
    print(f"[installation INDEX-GROSSIER] prompt_tokens natifs : "
          f"{ligne_idx['prompt_tokens']} (amorti /18 = "
          f"{ligne_idx['prompt_tokens'] / 18:.0f} par opération)",
          flush=True)
    return 0


# ------------------------------------------------------------ la campagne
def deja_faits(journal: pathlib.Path = JOURNAL) -> set:
    faits = set()
    if journal.exists():
        for l in journal.read_text(encoding="utf-8").splitlines():
            if l.strip():
                faits.add(json.loads(l)["tache"])
    return faits


def main() -> int:
    vt, taches_v8 = charger_v8()
    ordre = vt["ordre"]                    # la graine 20261117, JAMAIS re-tirée
    par_id = {b["id"]: b for b in vt["blocs"]}
    taches = {t["bloc"]: t for t in taches_v8.values()}
    exemple_l13 = (NOTATIONS / "loupe-13-recherche.asm").read_text(
        encoding="utf-8")
    faits = deja_faits()
    resultat_lignes = []

    # les squelettes dérivés (le livrable gabarits/squelettes/) — la
    # dérivation DÉTERMINISTE vécue AVANT la mesure, les fichiers posés
    for b in vt["blocs"]:
        sq, infos = generer_squelette(b["nom"])
        (SQUELETTES_DIR / f"{b['nom']}.asm").write_text(sq,
                                                        encoding="utf-8")

    for mode, fabrique, confronte in cellules(taches, par_id, exemple_l13):
        manquants = [bid for bid in ordre if f"{mode}-{bid}" not in faits]
        print(f"[{mode}] {len(manquants)} appel(s) à vivre (l'ordre de la "
              f"graine {vt['graine']})", flush=True)
        for bid in manquants:
            nom = par_id[bid]["nom"]
            t = taches[nom]
            tache = f"{mode}-{bid}"
            prompt, meta = fabrique(nom, t)
            (PROMPTS / f"{tache}.txt").write_text(prompt, encoding="utf-8")
            try:
                texte, ligne = appeler_et_compter("mesure", tache, prompt)
            except Exception as e:
                print(f"  ÉCHEC API {tache}: {e}", flush=True)
                time.sleep(20)
                continue
            verdict, vert, extras = confronte(texte, meta)
            dec = decomposition(mode, prompt, meta)
            r = {
                "tache": tache, "mode": mode, "bloc": nom,
                "verdict": verdict, "vert": vert,
                "prompt_tokens": ligne["prompt_tokens"],
                "completion_tokens": ligne["completion_tokens"],
                "total_tokens": ligne["total_tokens"],
                "cl100k_prompt": len(CL100K.encode(prompt)),
                "cl100k_reponse": len(CL100K.encode(texte)),
                "retok_prompt": retokenise_independante(prompt),
                "retok_reponse": retokenise_independante(texte),
                "materiau_cl100k": dec["materiau"],
                "prose_cl100k": dec["prose"],
            }
            for k, v in dec.items():
                if k not in ("materiau", "prose"):
                    r[k] = v
            r.update(extras)
            resultat_lignes.append(r)
            with open(RESULTATS, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(f"  {tache}: {ligne['total_tokens']} tokens (cl100k "
                  f"{r['cl100k_prompt'] + r['cl100k_reponse']}) — "
                  f"{verdict[:78]}", flush=True)
            faits.add(tache)
            time.sleep(3)
    print("LA CAMPAGNE : les six cellules visitées.", flush=True)
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--pilotes":
        raise SystemExit(pilotes())
    raise SystemExit(main())
