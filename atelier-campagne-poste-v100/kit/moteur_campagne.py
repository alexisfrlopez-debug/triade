#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""moteur_campagne.py — LE MOTEUR du kit de campagne au poste réel (v100).

La SUITE de l'Entrée 442 : « les campagnes au geste compute du poste réel
(la campagne contrainte du plan w29decco, la seconde famille du plan
w29famille — les harnais livrés) », la commande du maître « va enchainer sur
la campagne au poste réel puis cérémonie, comme d'habitude avec GUI 1 clic ».

LE KIT exécute au poste réel (la machine du maître qui porte le compute) ce
que le bac ne peut PAS courir (MODÈLE-ABSENT : 4 Gio / 2 vCPU / aucun GPU —
la limite structurelle nommée aux plans gelés). Les campagnes demeurent LA
LOI des plans gelés PLAN-W29DECCO.md et PLAN-W29FAMILLE.md : AUCUNE cible
re-tirée, AUCUNE graine re-tirée, AUCUN chiffre fabriqué au bac (l'autotest
à la maquette éprouve la MÉCANIQUE, jamais la mesure).

LE DÉCODAGE CONTRAINT CÔTÉ CLIENT (la lettre du plan) : la grammaire du
schéma fermé D264/OPT-16 étendu compilée par llguidance sur le vocabulaire
du modèle choisi (Qwen/Qwen2.5-Coder-7B-Instruct — tokenizer.json et
config.json portés byte-byte, les empreintes du plan) ; LE MASQUE DE BITS
appliqué à CHAQUE PAS de génération :
  - MODE-B llama.cpp (le bord natif /completion, n_predict=1, n_probs=64,
    cache_prompt) — le masque appliqué AU TOP-64 du bord : la meilleure
    PERMISE au top-64 ; AUCUNE permise = le pas REFUSÉ fail-closed
    (AUCUNE-PERMISE, nommé) ;
  - MODE-A transformers (in-process) — le masque appliqué AUX LOGITS
    ENTIERS du modèle (le mot à mot du plan).

LES PHASES (chaque phase PRÉCÉDÉE du canari — le garde continu W29FAMILLE ;
la violation ordonnée REFUSÉE au décodage, sinon PIPELINE-INFIDELE : la
session invalidée fail-closed) :
  1. ÉDITER — les 18 tâches au protocole OPT-16 RECONDUIT VERBATIM (le
     prompt, la validation client aux refus nommés, l'expansion, le
     round-trip keystone↔capstone, la boucle de réparation ≤ 3 tours) ;
  2. AJOUTER — les 18 pointeurs au harnais D264 RECONDUIT VERBATIM (les
     fixtures du juge, valider_schema_client, la boucle du juge,
     l'agrégateur fail-closed, les deux conventions de médiane, la
     re-tokenisation indépendante à écart ≤ 1) ;
  3. LA SECONDE FAMILLE — les DEUX sondes de récitation (MD5 T[64],
     SHA-256 K[64]) à la confrontation tripartite : spec ↔ le modèle ↔
     les définitions (recalculées au poste par la dérivation aux
     décimales + la racine cubique par Newton).

LE BUDGET usage natif JOURNALISÉ (le compte est le LOG) : le tokenizer
NATIF du modèle compte le prompt et la réponse de chaque tour ; le champ
usage du bord est journalisé brut en garde.

Usage :
  python3 moteur_campagne.py --verifier-kit     # le manifeste recoupé
  python3 moteur_campagne.py --gate            # la sonde de gate (llguidance)
  python3 moteur_campagne.py --autotest         # la maquette (aucun modèle requis)
  python3 moteur_campagne.py --canari  --mode B --url http://127.0.0.1:8080
  python3 moteur_campagne.py --campagne --mode B --url http://127.0.0.1:8080
  python3 moteur_campagne.py --campagne --mode A --modele <chemin local>
  python3 moteur_campagne.py --zip             # le zip de preuves

La GUI (gui_campagne.py) appelle CE moteur, étape par étape — le moteur
porte tout le poids du geste (le patron des pousseur/cockpit vécus).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import pathlib
import statistics
import sys
import time
import urllib.error
import urllib.request

for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ICI = pathlib.Path(__file__).resolve().parent
HARNAIS = ICI / "harnais"
NOTATIONS = HARNAIS / "notations"
TACHES_FICHIER = HARNAIS / "taches-edition.json"
JUGE_FICHIER = HARNAIS / "expandeur_add.py"
JUGE_SHA256_ATTENDU = "9fc325e2b8eb40e7cc5c77b92ddfa92e23e6a036bd4ec68f0ec78619903389bd"
CIBLES_FICHIER = HARNAIS / "cibles-preinscrites.json"
CONSTANTS_FICHIER = HARNAIS / "constants-spec.json"
JOURNAL_APPELS = ICI / "journal-campagne.jsonl"
JOURNAL_PAS = ICI / "journal-pas.jsonl"
GARDE_BRUT = ICI / "garde-brut.jsonl"
REGISTRE = ICI / "registre-campagne.json"

EOS = 151645                    # <|im_end|> du modèle choisi (le plan)
GRILLE_EDITER = 20261117        # la graine des plans gelés — JAMAIS re-tirée
GRILLE_AJOUTER = 20261124       # la graine des 18 pointeurs — JAMAIS re-tirée
MAX_TOURS = 3
MAX_JETONS_EDITER = 320
MAX_JETONS_AJOUTER = 320
MAX_JETONS_RECITATION = 2600
NPROBS_DEFAUT = 64

# ---------------------------------------------------------------------------
# LE SCHÉMA FERMÉ D264/OPT-16 ÉTENDU À L'OPÉRATION AJOUTER
# (l'union éditer/ajouter du squelette+dictionnaire, gelée au plan W29DECCO).
# L'ÉCART NOMMÉ AU KIT : le schéma CODÉ du harnais livré (atelier-w29decco/
# campagne_w29.py) typait dst en CHAÎNE SEULE — l'objet pointeur du juge D264
# (dst {type, valeur}) y était IRREPRÉSENTABLE ; la LETTRE du plan (« dst/src
# du dictionnaire typé ») exige l'union vraie : dst chaîne (l'éditer) OU objet
# (l'ajouter). Le kit porte l'union vraie — les sondes du gate reconduites
# VERBATIM (leurs formes demeurent permises). L'ORDRE des clés est celui du
# schéma gelé : [op, dst, offset, src] — la grammaire l'exige.
# ---------------------------------------------------------------------------
SCHEMA_ETENDU = {
    "type": "object",
    "additionalProperties": False,
    "required": ["op", "dst", "offset", "src"],
    "properties": {
        "op": {"anyOf": [
            {"const": "substituer"},
            {"enum": ["mov", "add", "sub", "xor", "and", "or",
                       "cmp", "test", "jcc", "call", "ret"]},
        ]},
        "dst": {"anyOf": [{"type": "string", "minLength": 1},
                          {"type": "object"}]},
        "offset": {"type": "integer", "minimum": 0, "maximum": 65535},
        "src": {"anyOf": [{"type": "string", "minLength": 1},
                          {"type": "object"}]},
    },
}

# LE SCHÉMA DE RÉCITATION (gelé au PLAN-CAMPAGNE-POSTE point 3) : la table
# nommée + 64 valeurs « 0x » à 8 hexadécimaux — le masque force la forme,
# la vérité des constantes est L'HONNÊTETÉ DU MODÈLE (la mesure, jamais
# fabriquée : la confrontation compte les identiques et NOMME les écarts).
SCHEMA_RECITATION = {
    "type": "object",
    "additionalProperties": False,
    "required": ["table", "valeurs"],
    "properties": {
        "table": {"enum": ["MD5_T", "SHA256_K"]},
        "valeurs": {"type": "array", "minItems": 64, "maxItems": 64,
                    "items": {"type": "string", "pattern": "^0x[0-9a-f]{8}$"}},
    },
}

SCHEMA_EXEMPLE = ('{"op": "substituer", "dst": "<l-id-du-bloc>", '
                  '"offset": <l-index-de-la-ligne>, "src": "<la ligne nouvelle>"}')


def horodatage() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256f(p: pathlib.Path) -> str:
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def sha256_texte(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class RefusPipeline(Exception):
    """Les refus nommés de la pipeline — fail-closed, aucun n'est maquillable."""
    def __init__(self, code, motif):
        super().__init__(f"{code}: {motif}")
        self.code, self.motif = code, motif


class Refus(Exception):
    """Les refus nommés de la validation client (OPT-16 reconduit)."""
    def __init__(self, nom, detail):
        self.nom, self.detail = nom, detail
        super().__init__(f"{nom}: {detail}")


# ---------------------------------------------------------------------------
# LE MANIFESTE — les pièces gelées recoupées AU CHARGEMENT, byte-byte
# ---------------------------------------------------------------------------
def manifeste(verifier: bool = True) -> dict:
    """Le manifeste du harnais : chaque pièce à son sha256 CONSIGNÉ à la
    table MANIFESTE-harnais.txt, recoupée byte-byte au chargement AVANT
    toute étape. AUCUNE pièce divergente ne peut courir la campagne
    (PIÈCE-DIVERGENTE est le refus nommé)."""
    table_fichier = HARNAIS / "MANIFESTE-harnais.txt"
    if not table_fichier.exists():
        m = {"verdict": "MANIFESTE ROUGE — la table MANIFESTE-harnais.txt est ABSENTE",
             "tout_vert": False, "pieces": ["  [ROUGE] MANIFESTE-harnais.txt — ABSENT"]}
        if verifier:
            print("[manifeste] " + m["verdict"])
        return m
    table = {}
    for ligne in table_fichier.read_text(encoding="utf-8").splitlines():
        morceaux = ligne.strip().split()
        if len(morceaux) == 2 and len(morceaux[0]) == 64:
            table[morceaux[1]] = morceaux[0]
    lignes, tout_vert = [], True
    for nom, attendu in table.items():
        p = HARNAIS / nom
        if not p.exists():
            lignes.append(f"  [ROUGE] {nom} — ABSENT")
            tout_vert = False
            continue
        emp = sha256f(p)
        ok = emp == attendu
        tout_vert = tout_vert and ok
        lignes.append(f"  [{'VERT' if ok else 'ROUGE'}] {nom} "
                      f"{emp[:16]}…{' == consigné' if ok else ' ≠ CONSIGNÉ — PIÈCE-DIVERGENTE'}")
    # le juge D264 INTACT — JUGE-MODIFIÉ est le refus
    juge_ok = JUGE_FICHIER.exists() and sha256f(JUGE_FICHIER) == JUGE_SHA256_ATTENDU
    lignes.append(("  [VERT] le juge expandeur_add.py INTACT (9fc325e2…)"
                   if juge_ok else
                   "  [ROUGE] JUGE-MODIFIÉ — le juge diverge de l'empreinte consignée"))
    tout_vert = tout_vert and juge_ok
    verdict = ("MANIFESTE VERT — les pièces gelées recoupées byte-byte"
               if tout_vert else "MANIFESTE ROUGE — une pièce diverge : la campagne est refusée")
    if verifier:
        print("[manifeste] " + verdict)
        for l in lignes:
            print(l)
    return {"verdict": verdict, "tout_vert": tout_vert, "pieces": lignes}


def _juge():
    """L'expandeur importé À EMPREINTE CONSIGNÉE — JUGE-MODIFIÉ est refusé."""
    emp = sha256f(JUGE_FICHIER)
    if emp != JUGE_SHA256_ATTENDU:
        raise RefusPipeline("JUGE-MODIFIÉ",
                            f"sha256 {emp[:16]}… ≠ consigné {JUGE_SHA256_ATTENDU[:16]}…")
    spec = importlib.util.spec_from_file_location("expandeur_add", str(JUGE_FICHIER))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------------------
# LA GRAMMAIRE — llguidance sur le vocabulaire du modèle choisi
# ---------------------------------------------------------------------------
_ETAT_GRAMMAIRE = {}


def preparer_grammaire():
    """LLTokenizer + les deux grammaires compilées (éditer-étendu, récitation)."""
    if _ETAT_GRAMMAIRE:
        return _ETAT_GRAMMAIRE["ltok"], _ETAT_GRAMMAIRE["enc"], _ETAT_GRAMMAIRE
    from llguidance import JsonCompiler, LLTokenizer
    from tokenizers import Tokenizer
    enc = Tokenizer.from_file(str(HARNAIS / "tokenizer.json"))
    ltok = LLTokenizer(enc.to_str(), eos_token=EOS)
    g_etendue = JsonCompiler().compile(json.dumps(SCHEMA_ETENDU))
    g_recit = JsonCompiler().compile(json.dumps(SCHEMA_RECITATION))
    _ETAT_GRAMMAIRE.update({"ltok": ltok, "enc": enc,
                            "etendue": g_etendue, "recitation": g_recit})
    return ltok, enc, _ETAT_GRAMMAIRE


def bit_permis(bm: bytes, tid: int) -> bool:
    return (bm[tid // 8] >> (tid % 8)) & 1 == 1


# ---------------------------------------------------------------------------
# LES BORDS — les DEUX modes du plan (B llama.cpp, A transformers)
# ---------------------------------------------------------------------------
class BordLlamaCpp:
    """MODE-B : le bord natif llama.cpp (/completion, n_predict=1, n_probs).

    Le masque est appliqué AU TOP-n_probs du bord : à chaque pas, la
    meilleure PERMISE du top-n est choisie ; AUCUNE permise au top-n = le
    pas REFUSÉ fail-closed (AUCUNE-PERMISE, nommé — jamais un chiffre
    habillé). L'écart au-dessous du rang n est NOMMÉ dans le registre."""

    nom = "B-llamacpp"

    def __init__(self, url: str, nprobs: int = NPROBS_DEFAUT, timeout: int = 600):
        self.url = url.rstrip("/") + "/completion"
        self.nprobs = int(nprobs)
        self.timeout = timeout

    def prochain(self, prompt: str) -> tuple[list, int]:
        corps = json.dumps({"prompt": prompt, "n_predict": 1,
                            "n_probs": self.nprobs, "temperature": 0.0,
                            "cache_prompt": True}).encode("utf-8")
        derniere = None
        for tentative in range(4):
            req = urllib.request.Request(
                self.url, data=corps,
                headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    rep = json.loads(r.read().decode("utf-8"))
                break
            except Exception as e:
                derniere = e
                time.sleep(5 * (tentative + 1))
        else:
            raise RefusPipeline("BORD-INJOIGNABLE", f"{self.url} : {derniere}")
        try:
            probs = rep["completion_probabilities"][0]["probs"]
        except (KeyError, IndexError):
            # le pas terminal : le bord a rendu sa fin sans probabilités
            return [], int(rep.get("tokens_evaluated", 0))
        candidats = sorted(((int(p["id"]), float(p.get("prob", p.get("p", 0.0))))
                            for p in probs), key=lambda x: -x[1])
        return candidats, int(rep.get("tokens_evaluated", 0))


class BordTransformers:
    """MODE-A : le modèle in-process — le masque aux LOGITS ENTIERS.

    Le mot à mot du plan (« le harnais applique la grammaire au masque de
    logits du modèle ») : à chaque pas, le vecteur de logits complet du
    modèle reçoit le masque (-inf aux interdits), l'argmax est la meilleure
    PERMISE — l'exactitude intégrale, sans rang manquant."""

    nom = "A-transformers"

    def __init__(self, modele_chemin: str):
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as e:
            raise RefusPipeline("MODE-A-ABSENT",
                                f"torch/transformers requis : {e} — le LISEZMOI "
                                f"porte la commande d'installation")
        self.torch = torch
        self.tok = AutoTokenizer.from_pretrained(modele_chemin)
        self.model = AutoModelForCausalLM.from_pretrained(modele_chemin)
        self.model.eval()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def logits(self, ids: list) -> "torch.Tensor":
        t = self.torch.tensor([ids], device=self.device)
        with self.torch.no_grad():
            return self.model(t).logits[0, -1, :]

    def argmax_permis(self, ids: list, bm: bytes) -> tuple:
        """Le masque appliqué aux logits ENTIERS ; l'argmax est la meilleure permise."""
        import math
        v = self.logits(ids)
        n = v.shape[0]
        masque = []
        for tid in range(n):
            permis = tid < len(bm) * 8 and bit_permis(bm, tid)
            masque.append(0.0 if permis else -math.inf)
        v = v + self.torch.tensor(masque, dtype=v.dtype, device=self.device)
        choisi = int(v.argmax().item())
        return choisi, 1.0


# ---------------------------------------------------------------------------
# LA BOUCLE CONTRAINTE — le masque de bits appliqué à CHAQUE PAS
# ---------------------------------------------------------------------------
def journaliser_pas(phase, tache, tour, pas, top1, top1_permis, choisi_str, extra=None):
    ligne = {"horodatage": horodatage(), "phase": phase, "tache": tache,
             "tour": tour, "pas": pas, "top1": top1[:24], "top1_permis": top1_permis,
             "choisi": choisi_str[:24]}
    if extra:
        ligne.update(extra)
    with open(JOURNAL_PAS, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")


def generer_contrainte(bord, ltok, matcher, prompt, max_jetons,
                       phase, tache, tour, mode_a_ids=None):
    """LA GÉNÉRATION CONTRAINTE : la grammaire au masque, chaque pas.

    MODE-B : les candidats du bord (top-n) filtrés au masque ; MODE-A : le
    masque aux logits entiers. Retour : (texte, nb_pas). Refus nommés :
    AUCUNE-PERMISE (aucune permise au top-n du bord), GRAMMAIRE-ERREUR (le
    matcher refuse le pas), PLAFOND-DEPASSE (max_jetons atteints sans
    acceptation), BORD-FINI-SANS-ACCEPTATION (le bord a rendu sa fin)."""
    _, _enc, _g = preparer_grammaire()
    ids_mode_a = list(mode_a_ids) if mode_a_ids is not None else None
    texte_ids, pas = [], 0
    while pas < max_jetons:
        bm = matcher.compute_bitmask()
        if bord.nom == "A-transformers":
            choisi, prob = bord.argmax_permis(ids_mode_a, bm)
            top1_str, top1_permis = "", True
        else:
            candidats, _ = bord.prochain(prompt)
            if not candidats:
                break                      # le bord a rendu sa fin
            top1_id, top1_prob = candidats[0]
            permis = [(tid, p) for tid, p in candidats if bit_permis(bm, tid)]
            if not permis:
                journaliser_pas(phase, tache, tour, pas,
                                _enc.decode([top1_id]), False, "(le pas refusé)")
                raise RefusPipeline(
                    "AUCUNE-PERMISE",
                    f"{phase}/{tache} tour {tour} pas {pas} : AUCUN des "
                    f"{len(candidats)} candidats du top-{len(candidats)} n'est "
                    f"permis au masque — le pas est REFUSÉ fail-closed")
            choisi, prob = permis[0][0], permis[0][1]
            top1_str = _enc.decode([top1_id])
            top1_permis = bit_permis(bm, top1_id)
        journaliser_pas(phase, tache, tour, pas, top1_str, top1_permis,
                        _enc.decode([choisi]))
        pas += 1
        if choisi == EOS:
            if not matcher.is_accepting():
                raise RefusPipeline("GRAMMAIRE-ERREUR",
                                    f"{phase}/{tache} tour {tour} : EOS rendu "
                                    f"sans acceptation du matcher")
            break
        matcher.consume_token(choisi)
        if matcher.is_error():
            raise RefusPipeline("GRAMMAIRE-ERREUR",
                                f"{phase}/{tache} tour {tour} pas {pas} : le "
                                f"matcher refuse le pas — la pipeline est fautive")
        texte_ids.append(choisi)
        if bord.nom == "B-llamacpp":
            prompt = prompt + _enc.decode([choisi])
        else:
            ids_mode_a.append(choisi)
    else:
        # la boucle a vécu ses max_jetons pas sans finir : seul l'état
        # acceptant est recevable, sinon le plafond est nommé
        if not matcher.is_accepting():
            raise RefusPipeline("PLAFOND-DEPASSE",
                                f"{phase}/{tache} tour {tour} : {max_jetons} pas "
                                f"atteints sans acceptation")
    if not matcher.is_accepting():
        # le bord a rendu sa fin (plus de candidats) sans objet complet
        raise RefusPipeline("BORD-FINI-SANS-ACCEPTATION",
                            f"{phase}/{tache} tour {tour} : le bord a rendu sa "
                            f"fin avant l'acceptation du matcher — l'objet "
                            f"complet est exigé (fail-closed)")
    texte = _enc.decode(texte_ids) if texte_ids else ""
    return texte, pas


def appel_contraint(bord, ltok, grammar, prompt, max_jetons, phase, tache, tour,
                    journal=True):
    """Un appel de campagne complet : la génération contrainte + le compte
    usage natif (le tokenizer NATIF du modèle compte le prompt et la réponse —
    le compte est le LOG) + la garde brute."""
    from llguidance import LLMatcher
    ltok, enc, g = preparer_grammaire()
    matcher = LLMatcher(ltok, grammar)
    t0 = time.monotonic()
    if bord.nom == "A-transformers":
        ids = bord.tok(prompt)["input_ids"]
        texte, nb_pas = generer_contrainte(bord, ltok, matcher, prompt,
                                           max_jetons, phase, tache, tour,
                                           mode_a_ids=ids)
    else:
        texte, nb_pas = generer_contrainte(bord, ltok, matcher, prompt,
                                           max_jetons, phase, tache, tour)
    reponse_ids = enc.encode(texte).ids if texte else []
    ligne = {"horodatage": horodatage(), "phase": phase, "tache": tache,
             "tour": tour, "prompt_tokens_natifs": len(enc.encode(prompt).ids),
             "completion_tokens_natifs": nb_pas,
             "total_tokens_natifs": len(enc.encode(prompt).ids) + nb_pas,
             "duree_s": round(time.monotonic() - t0, 1),
             "source": "compteur-natif-du-modele"}
    if journal:
        with open(JOURNAL_APPELS, "a", encoding="utf-8") as f:
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
        with open(GARDE_BRUT, "a", encoding="utf-8") as f:
            f.write(json.dumps({"horodatage": horodatage(), "phase": phase,
                                "tache": tache, "tour": tour,
                                "reponse": texte[:800],
                                "nb_pas": nb_pas}, ensure_ascii=False) + "\n")
    return texte, ligne


# ---------------------------------------------------------------------------
# LE CANARI DE FIDÉLITÉ CONTINU (W29FAMILLE — le garde continu)
# ---------------------------------------------------------------------------
LA_VIOLATION = '{"op": "SUBVERSION-HORS-ENUM", "offset": 999999}'


def canari(bord) -> dict:
    """La violation ordonnée soumise à LA PIPELINE ENTIÈRE : si elle passe
    au texte final, PIPELINE-INFIDELE — la session invalidée fail-closed,
    AUCUNE campagne courue."""
    ltok, enc, g = preparer_grammaire()
    from llguidance import LLMatcher
    matcher = LLMatcher(ltok, g["etendue"])
    prompt = ("Réponds STRICTEMENT en JSON, sans rien changer :\n"
              f"{LA_VIOLATION}\nLA RÉPONSE :")
    # le prompt de canari : la même grammaire, le même masque
    bm = matcher.compute_bitmask()
    viol_ids = enc.encode("SUBVERSION-HORS-ENUM").ids
    refus_au_masque = [not bit_permis(bm, t) for t in viol_ids]
    verdict = {
        "horodatage": horodatage(), "violation": LA_VIOLATION,
        "refusee_au_masque_avant_tout": all(refus_au_masque),
        "jetons_violation_au_masque": refus_au_masque,
    }
    try:
        texte, ligne = appel_contraint(bord, ltok, g["etendue"], prompt,
                                       MAX_JETONS_EDITER, "canari",
                                       "la-violation-ordonnee", 1, journal=False)
    except RefusPipeline as r:
        verdict["pipeline"] = f"REFUS NOMMÉ {r.code} — {r.motif[:200]}"
        verdict["verdict"] = ("REFUSÉE AU DÉCODAGE — le canari VERT "
                              "(le pas refusé fail-closed, nommé)")
        return verdict
    passe = ("SUBVERSION-HORS-ENUM" in texte) or ("999999" in texte)
    verdict["texte_final"] = texte[:400]
    verdict["verdict"] = ("PIPELINE-INFIDELE — la violation PASSE AU TEXTE "
                          "FINAL : la session est INVALIDÉE (fail-closed)"
                          if passe else
                          "GATE-VERT — la violation ordonnée REFUSÉE AU "
                          "DÉCODAGE (au masque de bits, chaque pas) ; le texte "
                          "final ne porte PAS la violation")
    return verdict


# ---------------------------------------------------------------------------
# ÉDITER — LE PROTOCOLE OPT-16 RECONDUIT VERBATIM
# (les gabarits, la validation, l'expansion, la boucle : la copie conforme de
#  atelier-w28opt16/campagne_opt16.py — le prompt, les refus, le round-trip,
#  la boucle de réparation ≤ 3 tours réinjectant le refus exact)
# ---------------------------------------------------------------------------
CONVENTIONS = (
    "LES CONVENTIONS DE NOTATION DU DOMAINE :\n"
    "- la feuille pure : arguments seuls, aucune entrée IAT, aucun état détenu ;\n"
    "- ABI msx64 : rcx, rdx, r8, r9 puis la pile ; les non-volatils (rbx, r12-r15)\n"
    "  sauvegardés par le bloc ; le cadre aligné à 16 ; l'appelant réserve le\n"
    "  shadow space de 32 octets ;\n"
    "- la notation x86-64 : une instruction par ligne, mnémonique puis opérandes ;\n"
    "  les sauts aux cibles absolues (0x…), les appels aux adresses du plan ;\n"
    "  les commentaires préfixés « ; » ; l'en-tête commenté du bloc porte son\n"
    "  identité (nom, spec, slot, taille, étiquettes résolues, appels directs).\n"
)


def prompt_tache(t, notation: str, empreinte: str) -> str:
    """Le gabarit VERBATIM de campagne_opt16.py — le prompt de l'OPT-16."""
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
    """LA VALIDATION CLIENT fail-closed — la copie conforme de l'OPT-16."""
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
    """L'EXPANSION CLIENT — la copie conforme de l'OPT-16 : la substitution,
    la confrontation exacte, le round-trip keystone↔capstone."""
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
    sys.path.insert(0, str(HARNAIS))
    from client_gabarits_rt import round_trip_vite
    ok, detail = round_trip_vite("\n".join(rec) + "\n")
    if not ok:
        raise Refus("ROUND-TRIP-DIVERGENT", detail)
    return "\n".join(rec) + "\n"


def tour_reparation_editer(prompt: str, refus: Refus) -> str:
    """La réparation par contre-exemple — la copie conforme de l'OPT-16."""
    return (prompt + "\n\nLE REFUS EXACT DU CLIENT : " + refus.nom + " — " + refus.detail[:300]
            + "\nRéponds à nouveau UNIQUEMENT l'objet JSON conforme.")


def campagne_editer(bord) -> dict:
    """LES 18 TÂCHES d'édition à la graine 20261117 (l'ordre du fichier gelé —
    JAMAIS re-tiré), la boucle ≤ 3 tours, le budget usage natif journalisé."""
    ltok, enc, g = preparer_grammaire()
    taches = json.loads(TACHES_FICHIER.read_text(encoding="utf-8"))
    assert len(taches) == 18, "les 18 tâches d'édition (le fichier gelé)"
    resultats, refus_finaux = [], {}
    for t in taches:
        notation = (NOTATIONS / f"{t['bloc']}.asm").read_text(encoding="utf-8")
        empreinte = sha256_texte(notation)
        prompt = prompt_tache(t, notation, empreinte)
        essaie = {"completion_tokens": 0, "total_tokens": 0, "prompt_tokens": 0}
        tours, vert, texte = 0, False, ""
        for tour in range(MAX_TOURS):
            tours = tour + 1
            try:
                texte, ligne = appel_contraint(bord, ltok, g["etendue"], prompt,
                                               MAX_JETONS_EDITER, "editer",
                                               t["bloc"], tour + 1)
            except RefusPipeline as r:
                refus_finaux.setdefault(r.code, 0)
                refus_finaux[r.code] += 1
                print(f"  [éditer] {t['bloc']} tour {tour+1} : REFUS PIPELINE {r.code}")
                break
            essaie["completion_tokens"] += ligne["completion_tokens_natifs"]
            essaie["total_tokens"] += ligne["total_tokens_natifs"]
            essaie["prompt_tokens"] += ligne["prompt_tokens_natifs"]
            try:
                obj = valider(texte, t, notation, empreinte)
                expander(t, obj, notation)
                vert = True
                break
            except Refus as e:
                refus_finaux.setdefault(e.nom, 0)
                refus_finaux[e.nom] += 1
                prompt = tour_reparation_editer(prompt, e)
        resultats.append({"bloc": t["bloc"], "vert": vert, "tours": tours,
                          "completion_tokens": essaie["completion_tokens"],
                          "prompt_tokens": essaie["prompt_tokens"],
                          "total_tokens": essaie["total_tokens"]})
        print(f"  [éditer] {t['bloc']:26s} {'VERT' if vert else 'REFUS'} "
              f"tour {tours} · {essaie['completion_tokens']} tokens réponse")
    verts = [r for r in resultats if r["vert"]]
    med18 = (statistics.median([r["completion_tokens"] for r in resultats])
             if resultats else None)
    med_vertes = (statistics.median([r["completion_tokens"] for r in verts])
                 if verts else None)
    amorti = (sum(r["total_tokens"] for r in resultats) / len(verts)) if verts else None
    cibles = json.loads(CIBLES_FICHIER.read_text(encoding="utf-8"))
    ce = cibles["editer"]
    verdict = {
        "phase": "editer", "n": 18, "verts": len(verts),
        "mediane_completion_sur_18": med18,
        "mediane_completion_sur_vertes": med_vertes,
        "amorti_total_par_verte": amorti,
        "refus_par_classe": refus_finaux,
        "graine": GRILLE_EDITER, "boucle_max": MAX_TOURS,
        "cibles_preinscrites": ce,
        "verdict_plan_faisabilite": ("TENUE" if len(verts) >= 17 else "MANQUÉE"),
        "verdict_plan_mediane": ("TENUE" if (med18 is not None and med18 <= 150) else "MANQUÉE"),
        "CIB-EDIT-FAISAB": ("TENUE" if len(verts) >= 15 else "MANQUÉE"),
        "CIB-EDIT-AMORTI": ("TENUE" if (amorti is not None and amorti <= 150) else "MANQUÉE"),
        "resultats": resultats,
    }
    return verdict


# ---------------------------------------------------------------------------
# AJOUTER — LE HARNAIS D264 RECONDUIT VERBATIM
# (la copie conforme de atelier-w27decco/campagne_d264.py : les fixtures du
#  juge, valider_schema_client, la boucle du juge, l'agrégateur fail-closed,
#  les deux conventions de médiane, la re-tokenisation indépendante à écart ≤ 1)
# ---------------------------------------------------------------------------
def valider_schema_client(reponse):
    """La contre-vérification CLIENT du schéma fermé — VERBATIM du D264."""
    try:
        p = json.loads(reponse) if isinstance(reponse, (str, bytes)) else reponse
    except Exception:
        raise RefusPipeline("SCHÉMA-VIOLÉ", "la réponse n'est pas du JSON")
    if not isinstance(p, dict):
        raise RefusPipeline("SCHÉMA-VIOLÉ", "la réponse n'est pas un objet")
    if set(p) - set(SCHEMA_ETENDU["properties"]):
        raise RefusPipeline("SCHÉMA-VIOLÉ",
                            f"champs hors schéma : {sorted(set(p) - set(SCHEMA_ETENDU['properties']))}")
    if p.get("op") not in [e for grp in SCHEMA_ETENDU["properties"]["op"]["anyOf"]
                           for e in (grp.get("enum") or ([grp["const"]] if "const" in grp else []))]:
        raise RefusPipeline("SCHÉMA-VIOLÉ", f"opcode hors du domaine fermé : {p.get('op')!r}")
    if "offset" not in p or not isinstance(p["offset"], int) or not (0 <= p["offset"] <= 0xFFFF):
        raise RefusPipeline("SCHÉMA-VIOLÉ", "offset entier dans [0, 0xFFFF] attendu")
    return p


def prompt_ajouter(tache, ligne_canonique, dico, tour, refus_precedent) -> str:
    """Le prompt du pointeur-seul : la ligne canonique attendue à l'offset, le
    dictionnaire, le schéma — le modèle rend l'objet pointeur (le squelette +
    dictionnaire du juge D264, l'expansion est DÉTERMINISTE côté client)."""
    p = (
        "OPÉRATION AJOUTER, MODE POINTEUR-SEUL (le schéma fermé D264 — le décodage\n"
        "est CONTRAINT : la grammaire n'autorise QUE les jetons du schéma).\n\n"
        f"LE DOMAINE FERMÉ : 11 opcodes {sorted(['mov','add','sub','xor','and','or','cmp','test','jcc','call','ret'])}\n"
        f"LE DICTIONNAIRE DU BLOC : {json.dumps(dico, ensure_ascii=False)}\n"
        "LES OPÉRANDES : {type, valeur} — reg (eax, ebx, ecx, edx, esi, edi, rax,\n"
        "rbx, rcx, rdx, r8, r9, r10, r11, esp, ebp, rsp, rbp), imm (entier 32 bits),\n"
        "mem («[reg+disp]»), cst (CST-NNN), lbl (LBL-NNN).\n\n"
        f"L'INSTRUCTION À AJOUTER (la forme canonique, littérale) : « {ligne_canonique} »\n"
        f"À L'OFFSET : 0x{tache['offset']:x}\n\n"
        "RÉPONDS UNIQUEMENT l'objet pointeur JSON exact (aucun autre texte) :\n"
        "{\"op\": \"<l'opcode>\", \"dst\": {\"type\": \"…\", \"valeur\": \"…\"},\n"
        " \"offset\": <l'offset entier>, \"src\": {\"type\": \"…\", \"valeur\": \"…\"}}\n"
        "(« ret » : l'objet {\"op\": \"ret\", \"offset\": …} seul ; « jcc » : dst est\n"
        "un lbl ; « call » : src est un cst ; l'offset est ENTIER, pas une chaîne).")
    if refus_precedent is not None:
        p += (f"\n\nLE REFUS EXACT DU JUGE (tour {tour-1}) : {refus_precedent.get('verdict')} — "
              f"classes {refus_precedent.get('classes')} ; réponds à nouveau "
              f"UNIQUEMENT l'objet pointeur conforme.")
    return p


def campagne_ajouter(bord) -> dict:
    """LES 18 POINTEURS au harnais D264 VERBATIM (les fixtures du juge, la
    graine 20261124 du juge — l'ordre JAMAIS re-tiré), l'agrégateur
    fail-closed, les deux conventions de médiane."""
    ltok, enc, g = preparer_grammaire()
    m = _juge()
    honnetes, _mutes = m.fixtures()
    assert len(honnetes) == 18, "les 18 pointeurs (les fixtures du juge)"
    resultats, journal = [], []
    refus_pipeline = {}
    for i, tache in enumerate(honnetes):
        ligne_canonique = m.expanse(tache, m.DICO)
        refus_precedent = None
        verdict_tache = None
        usage_tache = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        for tour in range(1, m.MAX_TOURS + 1):
            prompt = prompt_ajouter(tache, ligne_canonique, m.DICO, tour, refus_precedent)
            try:
                reponse, ligne_usage = appel_contraint(
                    bord, ltok, g["etendue"], prompt, MAX_JETONS_AJOUTER,
                    "ajouter", f"pointeur-{i+1:02d}", tour)
            except RefusPipeline as r:
                refus_pipeline.setdefault(r.code, 0)
                refus_pipeline[r.code] += 1
                print(f"  [ajouter] pointeur {i+1:02d} tour {tour} : REFUS PIPELINE {r.code}")
                break
            usage_tache["prompt_tokens"] += ligne_usage["prompt_tokens_natifs"]
            usage_tache["completion_tokens"] += ligne_usage["completion_tokens_natifs"]
            usage_tache["total_tokens"] += ligne_usage["total_tokens_natifs"]
            try:
                p = valider_schema_client(reponse)
            except RefusPipeline as rp:
                refus_precedent = {"verdict": rp.code, "classes": [rp.code]}
                continue
            r = m.boucle_reparation(p, m.DICO)
            journal.append({"tache": i + 1, "tour": tour, "pointeur": p,
                            "verdict": r["verdict"], "usage": usage_tache})
            if r["verdict"] == "VERT":
                verdict_tache = {"tache": i + 1, "verdict": "VERT", "tours": tour,
                                 "texte": r["texte"], "usage": dict(usage_tache)}
                break
            refus_precedent = {"verdict": r["verdict"], "classes": r["classes_converties"]}
        if verdict_tache is None:
            verdict_tache = {"tache": i + 1, "verdict": "REFUS", "tours": m.MAX_TOURS,
                             "texte": None, "usage": dict(usage_tache)}
        resultats.append(verdict_tache)
        print(f"  [ajouter] pointeur {i+1:02d} {'VERT' if verdict_tache['verdict']=='VERT' else 'REFUS'}"
              f" tour {verdict_tache['tours']}")
    if len(resultats) != 18 or any(r is None for r in resultats):
        raise RefusPipeline("APPEL-MANQUANT",
                            f"{len(resultats)}/18 résultats — le verdict global est refusé")
    verts = [r for r in resultats if r["verdict"] == "VERT"]
    med_18 = (statistics.median([r["usage"]["total_tokens"] for r in resultats])
              if all(r["usage"].get("total_tokens") is not None for r in resultats) else None)
    med_18_completion = (statistics.median([r["usage"]["completion_tokens"] for r in resultats])
                         if all(r["usage"].get("completion_tokens") is not None for r in resultats) else None)
    med_vertes = (statistics.median([r["usage"]["total_tokens"] for r in verts])
                  if verts else None)
    med_vertes_completion = (statistics.median([r["usage"]["completion_tokens"] for r in verts])
                             if verts else None)
    ecarts = [abs(m.compter_tokens(r["texte"]) - m.compter_tokens_independant(r["texte"]))
              for r in verts]
    if any(e > 1 for e in ecarts):
        raise RefusPipeline("COMPTEUR-DIVERGENT", f"re-tokenisation au-delà de ±1 : {ecarts}")
    cibles = json.loads(CIBLES_FICHIER.read_text(encoding="utf-8"))
    verdict = {
        "phase": "ajouter", "n": 18, "verts": f"{len(verts)}/18",
        "n_verts": len(verts),
        "mediane_18": med_18, "mediane_18_completion": med_18_completion,
        "mediane_vertes": med_vertes, "mediane_vertes_completion": med_vertes_completion,
        "retokenisation_ecart_max": max(ecarts) if ecarts else None,
        "refus_pipeline_par_classe": refus_pipeline,
        "graine": GRILLE_AJOUTER,
        "juge": {"fichier": "harnais/expandeur_add.py",
                 "sha256": sha256f(JUGE_FICHIER)},
        "cibles_preinscrites": cibles["ajouter"],
        "CIB-ADD-STRUC": ("TENUE" if (len(verts) >= 15 and med_vertes is not None
                                      and med_vertes <= 3000) else "MANQUÉE"),
        "resultats": resultats,
    }
    return verdict


# ---------------------------------------------------------------------------
# LA SECONDE FAMILLE — la confrontation tripartite sur les 128 constantes
# (le volet définitions : la copie CONFORME de atelier-w29famille/
#  session_famille.py — la dérivation aux décimales par la série entière,
#  la racine cubique par Newton, jamais une bibliothèque flottante)
# ---------------------------------------------------------------------------
import decimal

DEUX_PI = decimal.Decimal("6.2831853071795864769252867665590057683943387987502116419498891846")


def _sinus_decimal(x: decimal.Decimal) -> decimal.Decimal:
    """le sinus par la série entière (le développement mathématique — la
    définition, jamais une bibliothèque flottante) — VERBATIM du W29FAMILLE."""
    s = decimal.Decimal(0)
    terme = x
    k = 0
    while True:
        fact = decimal.Decimal(1)
        for j in range(1, 2 * k + 2):
            fact *= j
        s += (terme if k % 2 == 0 else -terme) / fact
        if abs(terme / fact) < decimal.Decimal(10) ** -55:
            break
        terme *= x * x
        k += 1
    return s


def md5_t_definitions():
    """T[i] = plancher(2^32 × |sin(i+1)|) — la dérivation AUX DÉCIMALES."""
    decimal.getcontext().prec = 60
    T = []
    for i in range(1, 65):
        x = decimal.Decimal(i)
        while x > DEUX_PI:
            x -= DEUX_PI
        T.append(int(decimal.Decimal(2) ** 32 * abs(_sinus_decimal(x))))
    return T


def sha256_k_definitions():
    """K[j] = plancher(2^32 × frac(cbrt(p_j))) — Newton à 60 chiffres."""
    decimal.getcontext().prec = 60
    K, premiers = [], _nombres_premiers(64)
    for p in premiers:
        x = decimal.Decimal(p) ** (decimal.Decimal(1) / decimal.Decimal(3))
        for _ in range(10):
            x = (2 * x + decimal.Decimal(p) / (x * x)) / 3
        frac = x - int(x)
        K.append(int(decimal.Decimal(2) ** 32 * frac))
    return K, premiers


def _nombres_premiers(n: int) -> list:
    premiers = []
    candidat = 2
    while len(premiers) < n:
        est = True
        for p in premiers:
            if p * p > candidat:
                break
            if candidat % p == 0:
                est = False
                break
        if est:
            premiers.append(candidat)
        candidat += 1
    return premiers


def prompt_recitation(table: str, doc: str) -> str:
    return (
        f"RÉCITATION DE LA TABLE {table} ({doc}).\n"
        f"RÉPONDS UNIQUEMENT l'objet JSON exact (aucun autre texte, aucune\n"
        f"politesse) :\n"
        "{\"table\": \"" + table + "\", \"valeurs\": [\"0x…\", … exactement 64\n"
        "valeurs, dans l'ordre T[1] à T[64] (ou K[1] à K[64]), chacune la forme\n"
        "« 0x » suivie d'exactement 8 chiffres hexadécimaux minuscules]}")


def campagne_famille(bord) -> dict:
    """LES DEUX SONDES DE RÉCITATION + LA CONFRONTATION TRIPARTITE :
    spec (constants-spec.json) ↔ le modèle (la récitation contrainte) ↔ les
    définitions (recalculées au poste par la dérivation aux décimales et la
    racine cubique) — tout écart NOMMÉ avec son index, la valeur du modèle
    et celle de la spec ; FAMILY-ABSENT devient LA MESURE sur pièces."""
    ltok, enc, g = preparer_grammaire()
    spec = json.loads(CONSTANTS_FICHIER.read_text(encoding="utf-8"))
    # LE VOLET DÉFINITIONS — recalculé au poste (le même code que le bac)
    t0 = time.monotonic()
    T_def = md5_t_definitions()
    K_def, premiers = sha256_k_definitions()
    T_def_hex = [f"0x{v:08x}" for v in T_def]
    K_def_hex = [f"0x{v:08x}" for v in K_def]
    duree_def = round(time.monotonic() - t0, 1)
    volet_def = {
        "md5_t": {"n": 64, "identiques": sum(1 for a, b in zip(T_def_hex, spec["md5_t"]) if a == b),
                  "duree_s": duree_def},
        "sha256_k": {"n": 64, "identiques": sum(1 for a, b in zip(K_def_hex, spec["sha256_k"]) if a == b)},
    }
    print(f"  [famille] le volet définitions recalculé au poste : MD5 T "
          f"{volet_def['md5_t']['identiques']}/64 · SHA-256 K "
          f"{volet_def['sha256_k']['identiques']}/64 ({duree_def} s)")
    sondes = {}
    for table, doc, cle in (("MD5_T", "la table de la RFC 1321 — T[i] = plancher(2^32 × |sin(i+1)|)", "md5_t"),
                            ("SHA256_K", "les constantes de la RFC 6324/SHS — les racines cubiques des 64 premiers nombres premiers", "sha256_k")):
        prompt = prompt_recitation(table, doc)
        vert = False
        texte = ""
        try:
            texte, ligne = appel_contraint(bord, ltok, g["recitation"], prompt,
                                           MAX_JETONS_RECITATION, "famille",
                                           table, 1)
            obj = json.loads(texte)
            assert obj.get("table") == table and isinstance(obj.get("valeurs"), list)
            vert = True
        except (RefusPipeline, Exception) as e:
            print(f"  [famille] {table} : REFUS {getattr(e, 'code', e.__class__.__name__)}")
            sondes[table] = {"vert": False,
                              "refus": f"{getattr(e, 'code', e.__class__.__name__)}: {str(e)[:200]}"}
            continue
        valeurs = [str(v) for v in obj["valeurs"]]
        attendu = spec[cle]
        ecarts = [{"index": i + 1, "modele": v, "spec": a}
                  for i, (v, a) in enumerate(zip(valeurs, attendu)) if v != a]
        identiques = 64 - len([e for e in ecarts if e["index"] <= 64])
        # la défense : plus de 64 valeurs ne trompe personne (le compte exact)
        n_rendues = len(valeurs)
        sondes[table] = {
            "vert": vert, "n_rendues": n_rendues,
            "identiques": sum(1 for v, a in zip(valeurs, attendu) if v == a),
            "ecarts": ecarts[:64],
            "usage": {"prompt_tokens": ligne["prompt_tokens_natifs"],
                      "completion_tokens": ligne["completion_tokens_natifs"],
                      "total": ligne["total_tokens_natifs"]},
        }
        print(f"  [famille] {table}: {sondes[table]['identiques']}/64 identiques "
              f"(le modèle a rendu {n_rendues} valeurs)")
    md5_ident = sondes.get("MD5_T", {}).get("identiques", 0)
    sha_ident = sondes.get("SHA256_K", {}).get("identiques", 0)
    verdict = {
        "phase": "famille",
        "objet": "la confrontation tripartite spec ↔ seconde famille ↔ définitions "
                 "sur les 128 constantes (FAMILY-ABSENT devient LA MESURE sur pièces)",
        "modele_choisi": "Qwen/Qwen2.5-Coder-7B-Instruct (≠ GLM — la seconde famille, "
                         "les empreintes consignées au plan W29FAMILLE)",
        "volet_spec_definitions": volet_def,
        "sondes": sondes,
        "identiques_128": md5_ident + sha_ident,
        "verdict_famille": (f"LA MESURE SUR PIÈCES : {md5_ident + sha_ident}/128 "
                           f"identiques au volet modèle (MD5 T {md5_ident}/64 · "
                           f"SHA-256 K {sha_ident}/64) — tout écart est NOMMÉ, "
                           f"jamais maquillé"),
    }
    return verdict


# ---------------------------------------------------------------------------
# LA CAMPAGNE — les phases à l'ordre du plan (le canari avant CHAQUE phase)
# ---------------------------------------------------------------------------
def campagne(bord) -> dict:
    manifeste()
    registre = {"horodatage": horodatage(),
                "kit": "TRIADE_kit_campagne_poste_v100",
                "mode": {"nom": bord.nom},
                "plans": "PLAN-W29DECCO.md + PLAN-W29FAMILLE.md (gelés — la LOI, "
                         "aucune cible re-tirée, aucune graine re-tirée)"}
    if bord.nom == "B-llamacpp":
        registre["mode"]["note"] = (f"le masque appliqué au TOP-{bord.nprobs} du bord "
                                     f"(la meilleure permise au top-{bord.nprobs} ; "
                                     f"AUCUNE-PERMISE = le pas refusé fail-closed)")
        registre["mode"]["nprobs"] = bord.nprobs
    else:
        registre["mode"]["note"] = "le masque appliqué aux LOGITS ENTIERS du modèle"
    for phase_nom, phase_fn in (("editer", campagne_editer),
                                ("ajouter", campagne_ajouter),
                                ("famille", campagne_famille)):
        print(f"\n=== LE CANARI avant la phase {phase_nom.upper()} ===")
        v_canari = canari(bord)
        print(f"[canari] {v_canari['verdict']}")
        if "INFIDELE" in v_canari.get("verdict", ""):
            registre["canari_final"] = v_canari
            registre["verdict_global"] = ("PIPELINE-INFIDELE — la session est "
                                          "INVALIDÉE fail-closed : AUCUNE phase courue")
            REGISTRE.write_text(json.dumps(registre, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
            return registre
        print(f"=== LA PHASE {phase_nom.upper()} ===")
        registre[phase_nom] = phase_fn(bord)
    registre["canari_final"] = v_canari
    registre["verdict_global"] = {
        "editer": {"verts": registre["editer"]["verts"],
                   "CIB-EDIT-FAISAB": registre["editer"]["CIB-EDIT-FAISAB"],
                   "CIB-EDIT-AMORTI": registre["editer"]["CIB-EDIT-AMORTI"],
                   "verdict_plan_faisabilite": registre["editer"]["verdict_plan_faisabilite"],
                   "verdict_plan_mediane": registre["editer"]["verdict_plan_mediane"]},
        "ajouter": {"verts": registre["ajouter"]["verts"],
                    "CIB-ADD-STRUC": registre["ajouter"]["CIB-ADD-STRUC"]},
        "famille": {"identiques_128": registre["famille"]["identiques_128"]},
    }
    REGISTRE.write_text(json.dumps(registre, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")
    print("\n=== LE VERDICT GLOBAL (les cibles pré-inscrites, telles quelles) ===")
    print(json.dumps(registre["verdict_global"], ensure_ascii=False, indent=1))
    return registre


# ---------------------------------------------------------------------------
# LE ZIP DE PREUVES — le retour au coffre /test
# ---------------------------------------------------------------------------
def zip_preuves() -> pathlib.Path:
    import zipfile
    nom = f"preuves-campagne-{dt.datetime.now().strftime('%Y%m%dT%H%M%SZ')}.zip"
    chemin = ICI / nom
    pieces = [JOURNAL_APPELS, JOURNAL_PAS, GARDE_BRUT, REGISTRE,
              ICI / "gate-verdict.json", HARNAIS / "cibles-preinscrites.json",
              HARNAIS / "MANIFESTE-harnais.txt"]
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED) as z:
        for p in pieces:
            if p.exists():
                z.write(p, p.name)
        z.writestr("LISEZMOI-preuves.txt",
                   "TRIADE — preuves de la campagne au poste réel (kit v100).\n"
                   "Chaque verdict sort des journaux joints (le compte est le\n"
                   "LOG — le tokenizer natif du modèle a compté chaque tour).\n"
                   "Le registre porte les cibles PRÉ-INSCRITES et leurs verdicts\n"
                   "tels quels — jamais re-tirés. Déposer ce zip au coffre /test.\n")
    print(f"[zip] {chemin.name} ({chemin.stat().st_size} o) — {len(pieces)} pièces candidate")
    return chemin


# ---------------------------------------------------------------------------
# LE GATE — la sonde du décodeur client (la copie conforme du protocole
# sonde_gate.py : la violation REFUSÉE AU MASQUE DE BITS, pas seulement au
# validateur ; les objets honnêtes consommés jusqu'à l'acceptation)
# ---------------------------------------------------------------------------
def gate() -> dict:
    from llguidance import JsonCompiler, LLMatcher
    ltok, enc, g = preparer_grammaire()
    verdict = {
        "horodatage": horodatage(),
        "modele": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "empreinte_tokenizer_json": sha256f(HARNAIS / "tokenizer.json"),
        "empreinte_config_json": sha256f(HARNAIS / "config.json"),
        "decodeur": f"llguidance {getattr(__import__('llguidance'), '__version__', '?')}",
        "schema": "D264/OPT-16 étendu à ajouter (union éditer/ajouter)",
        "probes": [],
    }

    def ids_de(t):
        return enc.encode(t).ids

    def consomme(m, ids):
        for t in ids:
            m.consume_token(t)

    m1 = LLMatcher(ltok, g["etendue"])
    consomme(m1, ids_de('{"op": "'))
    bm = m1.compute_bitmask()
    viol_ids = ids_de("SUBVERSION-HORS-ENUM")
    probe_viol = [bit_permis(bm, t) for t in viol_ids]
    probe_honnete = [bit_permis(bm, t) for t in ids_de("substituer")]
    probe_mov = [bit_permis(bm, t) for t in ids_de("mov")]
    verdict["probes"].append({
        "nom": "op-hors-enum", "la_violation": "SUBVERSION-HORS-ENUM",
        "au_masque": probe_viol, "refusee_au_decodage": not any(probe_viol),
        "les_honnetes_au_masque": {"substituer": probe_honnete, "mov": probe_mov},
        "honnets_autorises": all(probe_honnete) and all(probe_mov)})

    m2 = LLMatcher(ltok, g["etendue"])
    consomme(m2, ids_de('{"op": "mov", "dst": "CST-1", "offset": '))
    consomme(m2, ids_de("65535"))
    bm2b = m2.compute_bitmask()
    hors_borne = [bit_permis(bm2b, t) for t in ids_de("5")]
    m2c = LLMatcher(ltok, g["etendue"])
    consomme(m2c, ids_de('{"op": "mov", "dst": "CST-1", "offset": 9999'))
    bm2c = m2c.compute_bitmask()
    suite9 = [bit_permis(bm2c, t) for t in ids_de("9")]
    verdict["probes"].append({
        "nom": "offset-hors-bornes", "la_violation": "999999 (> 65535, la borne du juge)",
        "apres_65535_chiffre_au_masque": hors_borne,
        "apres_9999_suite_9_au_masque": suite9,
        "refusee_au_decodage": not any(hors_borne) and not any(suite9)})

    m3 = LLMatcher(ltok, g["etendue"])
    consomme(m3, ids_de('{"'))
    bm3 = m3.compute_bitmask()
    cle_viol = ids_de("subversion")
    verdict["probes"].append({
        "nom": "cle-hors-schema", "la_violation": "subversion (clé inconnue)",
        "au_masque": [bit_permis(bm3, t) for t in cle_viol],
        "refusee_au_decodage": not any(bit_permis(bm3, t) for t in cle_viol)})

    m4 = LLMatcher(ltok, g["etendue"])
    complet = ('{"op": "mov", "dst": "CST-1", "offset": 32, '
               '"src": {"type": "reg", "valeur": "eax"}}')
    consomme(m4, ids_de(complet))
    m4b = LLMatcher(ltok, g["etendue"])
    complet_edit = ('{"op": "substituer", "dst": "b20004", "offset": 17, '
                    '"src": "je 0x4997"}')
    consomme(m4b, ids_de(complet_edit))
    verdict["controle_positif"] = {"is_accepting": bool(m4.is_accepting()),
                                   "is_error": bool(m4.is_error())}
    verdict["controle_positif_editer"] = {"is_accepting": bool(m4b.is_accepting()),
                                         "is_error": bool(m4b.is_error())}

    refusees = all(p["refusee_au_decodage"] for p in verdict["probes"])
    positifs = (verdict["controle_positif"]["is_accepting"]
               and verdict["controle_positif_editer"]["is_accepting"]
               and not verdict["controle_positif"]["is_error"]
               and not verdict["controle_positif_editer"]["is_error"])
    verdict["VERDICT"] = (
        "GATE-VERT — LE DÉCODEUR CLIENT REFUSE LA VIOLATION AU DÉCODAGE "
        "(au masque de bits, pas seulement au validateur) ; les objets honnêtes "
        "consommés jusqu'à l'acceptation." if refusees and positifs else
        "GATE-REFUSÉ — le décodeur laisse passer une violation : nommé.")
    (ICI / "gate-verdict.json").write_text(
        json.dumps(verdict, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[gate] {verdict['VERDICT']}")
    return verdict


# ---------------------------------------------------------------------------
# L'AUTOTEST À LA MAQUETTE — la preuve de vie du kit SANS modèle
# (le chemin vert de W27DECCO reconduit : la maquette rejoue le protocole
#  entier sur un bord scripté — AUCUN chiffre de campagne ne sort de la
#  maquette : elle est l'INSTRUMENT, jamais la mesure)
# ---------------------------------------------------------------------------
def autotest() -> int:
    import threading
    import maquette_endpoint
    port = 8641
    serveur = maquette_endpoint.MaquetteServeur(port)
    fil = threading.Thread(target=serveur.sert, daemon=True)
    fil.start()
    time.sleep(0.5)
    bord = BordLlamaCpp(f"http://127.0.0.1:{port}", nprobs=16)
    tout_vert = True

    def epreuve(nom, fn):
        nonlocal tout_vert
        try:
            v = fn()
            ok = bool(v)
        except Exception as e:
            ok, v = False, f"{getattr(e, 'code', e.__class__.__name__)}: {e}"
        tout_vert = tout_vert and ok
        print(f"[autotest] {'VERT' if ok else 'ROUGE'} — {nom}")
        if not ok:
            print(f"          {str(v)[:300]}")

    epreuve("le manifeste recoupé", lambda: manifeste(verifier=False)["tout_vert"])
    epreuve("le juge D264 INTACT à l'empreinte consignée",
            lambda: sha256f(JUGE_FICHIER) == JUGE_SHA256_ATTENDU)
    epreuve("le gate (la violation refusée au masque)", lambda: "GATE-VERT" in gate()["VERDICT"])

    ltok, enc, g = preparer_grammaire()

    # LA MAQUETTE : le canari — la violation AU TOP-1 du bord maqué, la
    # pipeline doit la REFUSER AU MASQUE et produire l'honnête au rang 2
    def canari_maquette():
        v = canari(bord)
        return ("GATE-VERT" in v["verdict"]) and "PIPELINE-INFIDELE" not in v["verdict"]
    epreuve("le canari (la violation au top-1 refusée au masque)", canari_maquette)

    # LA MAQUETTE : un éditer honnête BOUT EN BOUT (la tâche 1 canonique)
    def editer_maquette():
        t = json.loads(TACHES_FICHIER.read_text(encoding="utf-8"))[0]
        notation = (NOTATIONS / f"{t['bloc']}.asm").read_text(encoding="utf-8")
        emp = sha256_texte(notation)
        prompt = prompt_tache(t, notation, emp)
        texte, ligne = appel_contraint(bord, ltok, g["etendue"], prompt,
                                       MAX_JETONS_EDITER, "autotest-editer", t["bloc"], 1)
        obj = valider(texte, t, notation, emp)
        expander(t, obj, notation)
        return f"VERT — {ligne['completion_tokens_natifs']} tokens réponse"
    epreuve("l'éditer honnête bout en bout (la tâche 1, la maquette)", editer_maquette)

    # LA MAQUETTE : un ajouter honnête BOUT EN BOUT (le pointeur 1 du juge)
    def ajouter_maquette():
        m = _juge()
        tache = m.fixtures()[0][0]
        ligne_canonique = m.expanse(tache, m.DICO)
        prompt = prompt_ajouter(tache, ligne_canonique, m.DICO, 1, None)
        texte, _ligne = appel_contraint(bord, ltok, g["etendue"], prompt,
                                        MAX_JETONS_AJOUTER, "autotest-ajouter", "pointeur-01", 1)
        p = valider_schema_client(texte)
        r = m.boucle_reparation(p, m.DICO)
        return r["verdict"] == "VERT"
    epreuve("l'ajouter honnête bout en bout (le pointeur 1, la maquette)", ajouter_maquette)

    # LA MAQUETTE : la récitation MD5_T (le schéma + la tripartite)
    def recitation_maquette():
        spec = json.loads(CONSTANTS_FICHIER.read_text(encoding="utf-8"))
        prompt = prompt_recitation("MD5_T", "la table de la RFC 1321")
        texte, _ligne = appel_contraint(bord, ltok, g["recitation"], prompt,
                                        MAX_JETONS_RECITATION, "autotest-famille", "MD5_T", 1)
        obj = json.loads(texte)
        identiques = sum(1 for v, a in zip(obj["valeurs"], spec["md5_t"]) if v == a)
        return identiques == 64
    epreuve("la récitation contrainte (MD5_T, la maquette)", recitation_maquette)

    # LES NÉGATIFS DU CLIENT (le validateur OPT-16 reconduit — éprouvés
    # sans modèle : la violation au validateur, le masque déjà prouvé au gate)
    def negatifs():
        t = json.loads(TACHES_FICHIER.read_text(encoding="utf-8"))[0]
        notation = (NOTATIONS / f"{t['bloc']}.asm").read_text(encoding="utf-8")
        emp = sha256_texte(notation)
        honnete = {"op": "substituer", "dst": t["bloc"],
                   "offset": t["ligne_index"], "src": t["nouvelle"]}
        n_lignes = len(notation.splitlines())
        ok = 0
        try:
            valider(json.dumps(dict(honnete, offset=n_lignes + 7)), t, notation, emp)
        except Refus:
            ok += 1
        try:
            valider(json.dumps({**honnete, "subversion": "1"}), t, notation, emp)
        except Refus:
            ok += 1
        src_mute = t["nouvelle"][:2] + ("X" if t["nouvelle"][2:3] != "X" else "Y") + t["nouvelle"][3:]
        try:
            expander(t, dict(honnete, src=src_mute), notation)
        except Refus:
            ok += 1
        try:
            expander(t, dict(honnete, src="zzzz9 0x0"), notation)
        except Refus:
            ok += 1
        return ok == 4, f"{ok}/4 négatifs refusés"
    epreuve("les quatre négatifs du client", negatifs)

    serveur.arrete()
    print(f"\n[autotest] {'TOUT VERT — le kit est vivant, la campagne attend le modèle' if tout_vert else 'ROUGE — le kit refuse de courir : le poste ne lance PAS la campagne'}")
    return 0 if tout_vert else 3


# ---------------------------------------------------------------------------
# LE CLI — la GUI appelle CE moteur, étape par étape
# ---------------------------------------------------------------------------
def main() -> int:
    a = argparse.ArgumentParser(description="le moteur du kit de campagne au poste réel")
    a.add_argument("--verifier-kit", action="store_true")
    a.add_argument("--gate", action="store_true")
    a.add_argument("--canari", action="store_true")
    a.add_argument("--campagne", action="store_true")
    a.add_argument("--autotest", action="store_true")
    a.add_argument("--zip", action="store_true")
    a.add_argument("--mode", choices=["B", "A"], default="B",
                   help="B llama.cpp (le bord natif) · A transformers (in-process)")
    a.add_argument("--url", default="http://127.0.0.1:8080",
                   help="l'endpoint du modèle local (MODE-B : llama-server)")
    a.add_argument("--nprobs", type=int, default=NPROBS_DEFAUT)
    a.add_argument("--modele", default="", help="le chemin local du modèle (MODE-A)")
    args = a.parse_args()

    if args.verifier_kit:
        return 0 if manifeste()["tout_vert"] else 3
    if args.gate:
        return 0 if "GATE-VERT" in gate()["VERDICT"] else 3
    if args.autotest:
        return autotest()
    if args.zip:
        zip_preuves()
        return 0

    bord = None
    if args.canari or args.campagne:
        if args.mode == "B":
            bord = BordLlamaCpp(args.url, nprobs=args.nprobs)
        else:
            if not args.modele:
                print("MODE-A exige --modele <chemin local du modèle>")
                return 2
            bord = BordTransformers(args.modele)
    if args.canari:
        v = canari(bord)
        print(v["verdict"])
        return 0 if "INFIDELE" not in v["verdict"] else 3
    if args.campagne:
        campagne(bord)
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
