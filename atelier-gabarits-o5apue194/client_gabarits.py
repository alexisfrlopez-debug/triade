#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""client_gabarits.py — LES CLIENTS DES TROIS OPÉRATIONS DE L'ATELIER
o5apue194 (le plan PLAN-O5APUE194.md gelé) :

  éditer-T2 (LE GABARIT VERSIONNÉ TPL-EDIT-v1) : la consigne en langue
      naturelle REMPLACÉE par l'invocation du gabarit — l'ID + l'empreinte
      sha256 GRAVÉS AU PROMPT (la garde) + LES PARAMÈTRES LITTÉRAUX (bloc,
      ligne, l'ancienne ligne, la nouvelle ligne — le diff lui-même). Le
      CORPS du gabarit (la grammaire hunk, l'exemple complet, les règles
      d'ancre) vit UNE FOIS PAR SESSION — jamais dans l'opération. Le
      client recoupe l'empreinte du gabarit chargé en session (fail-closed
      — GABARIT-DIVERGENT), la garde de notation (CONTEXTE-DIVERGENT),
      applique les hunks (le client hunk v2 TEL QUEL : HORS-FORMAT,
      HUNK-INCONNU, CONTEXTE-DIVERGENT), round-trip exact
      (ROUND-TRIP-DIVERGENT). La fenêtre ±12 lignes DEMEURE au prompt,
      l'empreinte sha256 de la notation complète DEMEURE la garde — AUCUN
      contrôle retiré.

  localiser-H (LE LOCALISER HIÉRARCHIQUE) : L'INDEX GROSSIER (les IDs +
      les empreintes COURTES, 8 hex — UN document compact par session,
      l'empreinte sha256 en garde) au prompt ; la requête porte l'identité
      du bloc (l'empreinte complète de sa notation) ; le modèle CHOISIT
      l'entrée de l'index (le niveau grossier : le préfixe 8 hex) puis
      rend L'ENTRÉE FINE — le pointeur littéral (l'ID + l'empreinte
      complète, le record 52). Le client expande et recoupe : le même
      oracle que le pointeur seul (POINTEUR-INCONNU, HORS-FORMAT,
      EMPREINTE-DIVERGENTE, EXPANSION-DIVERGENTE re-roulés) + l'entrée
      fine confrontée à l'index (ENTREE-DIVERGENTE) + la garde d'index
      (INDEX-DIVERGENT).

  ajouter-S (L'AJOUT PAR SQUELETTE) : LE SQUELETTE DÉTERMINISTE dérivé de
      la couche I (le cadre ABI — le prologue/épilogue aux non-volatils
      sauvés, le shadow space ; les types, la signature) GÉNÉRÉ PAR LE
      CLIENT depuis la spec I du bloc (zéro token LLM) ; l'agent ne rend
      QUE LA LOGIQUE (le corps entre les balises du squelette) ; le client
      ASSEMBLE squelette + logique, round-trip exact (keystone/capstone),
      l'oracle régénéré (le cadre intact, la liste fermée des appels).

LES REFUS NOMMÉS (fail-closed, le premier l'emporte) :
  HORS-FORMAT · HUNK-INCONNU · CONTEXTE-DIVERGENT · ROUND-TRIP-DIVERGENT ·
  GABARIT-DIVERGENT · POINTEUR-INCONNU · EMPREINTE-DIVERGENTE ·
  EXPANSION-DIVERGENTE · ENTREE-DIVERGENTE · INDEX-DIVERGENT"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
V8 = REPO / "atelier-opt05-pe6iv71fj"
sys.path.insert(0, str(V8))

from client_hunks_v2 import parse_hunks, appliquer  # noqa: E402
from client_hunks import round_trip, Refus  # noqa: E402

FENETRE_N = 12              # ±12 lignes — la fenêtre gelée (la vague 10)
TPL_ID = "TPL-EDIT-v1"
TPL_CHEMIN = ICI / "gabarits" / "TPL-EDIT-v1.txt"
INDEX_CHEMIN = ICI / "gabarits" / "index-grossier.txt"
NOTATIONS = REPO / "loupe" / "notation"
SPECS = REPO / "loupe" / "I"
SQUELETTES_DIR = ICI / "gabarits" / "squelettes"

# LES ADRESSES DU PLAN (la bibliothèque de gabarits scellés — la carte,
# lecture seule ; les appelés directs nommés par les specs I)
PLAN_APPELS = {
    "libc-01": ("memcpy (dst, src, n)", 0x1100),
    "libc-02": ("memcmp (a, b, n)", 0x1180),
    "libc-07": ("memset (dst, octet, n)", 0x13C0),
    "tls13-01": ("sha256-init (ctx 112 o)", 0xC000),
    "tls13-02": ("sha256-comprimer (ctx, bloc 64 o)", 0xC080),
    "tls13-03": ("sha256-absorber (ctx, données, n)", 0xC400),
    "tls13-04": ("sha256-finaliser (ctx, sortie 32 o)", 0xC5C0),
}


# ------------------------------------------------------------ les empreintes
def sha256_texte(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def charger_tpl() -> tuple[str, str]:
    """Le corps du gabarit TEL QUEL sur le disque + son empreinte (la
    version de session — la source unique de l'expansion)."""
    corps = TPL_CHEMIN.read_text(encoding="utf-8")
    return corps, sha256_texte(corps)


def charger_index() -> dict:
    """L'INDEX GROSSIER du disque : le document + son empreinte (la garde)
    + les entrées (id → empreinte courte 8 hex) re-parses du document."""
    doc = INDEX_CHEMIN.read_text(encoding="utf-8")
    m = re.search(r"^— la garde : sha256:([0-9a-f]{64})", doc, re.M)
    empreinte = m.group(1)
    entrees = {}
    for l in doc.splitlines():
        m = re.match(r"^(i\d{6}) ([0-9a-f]{8})$", l.strip())
        if m:
            entrees[m.group(1)] = m.group(2)
    return {"document": doc, "empreinte": empreinte, "entrees": entrees}


def table_carte() -> dict[str, dict]:
    """La table des 18 — RÉGÉNÉRÉE des fichiers mêmes (jamais tapée)."""
    table = {}
    for f in sorted(NOTATIONS.glob("loupe-*.asm")):
        entete = []
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.startswith(";"):
                entete.append(l)
            elif l.strip() == "":
                continue
            else:
                break
        joint = "\n".join(entete)
        bid = re.search(r"bloc carte (i\d+)", joint).group(1)
        table[bid] = {"nom": f.stem, "entete": joint,
                      "empreinte": hashlib.sha256(
                          f.read_bytes()).hexdigest()}
    return table


# ============================================== ÉDITER-T2 (le gabarit versionné)
def prompt_editer_t2(nom_bloc: str, notation: str, ligne_index: int,
                     ancienne: str, nouvelle: str,
                     rappel_marqueurs: bool = True) -> tuple[str, dict]:
    """LE PROMPT T2 — l'opération SEULE (le corps du gabarit vit une fois
    par session, jamais ici) : l'ID du gabarit, l'empreinte, LES
    PARAMÈTRES LITTÉRAUX (bloc, ligne, l'ancienne ligne, la nouvelle
    ligne — le diff lui-même), la fenêtre ±12, la garde de notation."""
    _, tpl_empreinte = charger_tpl()
    lignes = notation.split("\n")
    i = ligne_index
    i0, i1 = max(0, i - FENETRE_N), min(len(lignes), i + FENETRE_N + 1)
    fenetre = "\n".join(lignes[i0:i1])
    emp_notation = sha256_texte(notation)
    if rappel_marqueurs:
        requete = (
            "REQUÊTE : applique le gabarit aux paramètres — rends UNIQUEMENT\n"
            "les hunks : la PREMIÈRE ligne exactement « @@ hunk 1 », l'ancre\n"
            "« base: <la ligne exacte> », les retraits « - … », les\n"
            "insertions « + … », la DERNIÈRE ligne exactement « FIN-HUNKS »\n"
            "— aucune clôture de code (aucun ```), aucun autre texte.\n"
        )
    else:
        requete = (
            "REQUÊTE : applique le gabarit aux paramètres — rends UNIQUEMENT\n"
            "les hunks au format du gabarit, la dernière ligne exactement\n"
            "« FIN-HUNKS » — rien d'autre.\n"
        )
    prompt = (
        f"L'OPÉRATION ÉDITER DE LA CARTE TRIADE — LE GABARIT VERSIONNÉ\n"
        f"{TPL_ID} · sha256:{tpl_empreinte}\n"
        f"(le corps du gabarte vit en session ; le client recoupe son\n"
        f"empreinte AVANT l'application — GABARIT-DIVERGENT sinon.)\n\n"
        f"LA FENÊTRE DE LA CIBLE (les lignes {i0 + 1} à {i1} du bloc — la\n"
        f"ligne {i + 1} est la ligne cible) :\n{fenetre}\n\n"
        f"LA GARDE (l'expansion fail-closed) : l'empreinte sha256 de la\n"
        f"notation complète en cache : {emp_notation} — le client recoupe\n"
        f"cette empreinte AVANT l'application des hunks (toute divergence\n"
        f"de la base en cache : REFUS CONTEXTE-DIVERGENT).\n\n"
        f"LES PARAMÈTRES LITTÉRAUX (l'opération — le diff) :\n"
        f"bloc : {nom_bloc}\n"
        f"ligne : {i + 1}\n"
        f"ancienne : {ancienne}\n"
        f"nouvelle : {nouvelle}\n\n"
        f"{requete}"
    )
    return prompt, {"tpl_empreinte": tpl_empreinte,
                    "notation_empreinte": emp_notation,
                    "fenetre": fenetre, "nom": nom_bloc}


def appliquer_t2(notation_cache: str, notation_empreinte: str,
                 reponse: str, tpl_empreinte_session: str,
                 tpl_empreinte_prompt: str) -> tuple[str, str]:
    """LE CLIENT T2 : (1) la recoupe de l'empreinte DU GABARIT (fail-closed
    — GABARIT-DIVERGENT si la session diverge du prompt) ; (2) la recoupe
    de l'empreinte de la notation (CONTEXTE-DIVERGENT) ; (3) l'application
    des hunks + le round-trip (le client v2 — les quatre refus du hunk)."""
    if tpl_empreinte_session != tpl_empreinte_prompt:
        raise Refus(
            "GABARIT-DIVERGENT",
            f"l'empreinte du gabarit de session "
            f"{tpl_empreinte_session[:16]}… != l'empreinte gravée au prompt "
            f"{tpl_empreinte_prompt[:16]}… — le gabarit a divergé")
    if sha256_texte(notation_cache) != notation_empreinte:
        raise Refus(
            "CONTEXTE-DIVERGENT",
            f"l'empreinte du cache {sha256_texte(notation_cache)[:16]}… != "
            f"l'empreinte du prompt {notation_empreinte[:16]}… — la base a "
            f"divergé")
    hunks = parse_hunks(reponse)                     # HORS-FORMAT
    reconstruit = appliquer(notation_cache, hunks)   # HUNK-INCONNU, C-D
    ok, detail = round_trip(reconstruit)             # ROUND-TRIP-DIVERGENT
    if not ok:
        raise Refus("ROUND-TRIP-DIVERGENT", detail)
    return reconstruit, detail


def diff_exact(notation: str, ligne_index: int, nouvelle: str,
               reconstruit: str) -> bool:
    """L'ORACLE DU DIFF EXACT : la tâche connaît la ligne, l'ancienne et
    la nouvelle — le reconstruit DOIT être la notation au diff exact (la
    ligne remplacée, AUCUNE autre ligne changée). Le critère RENFORCÉ de
    la vague 11 (la vague 10 n'avait que le round-trip — AUCUN contrôle
    retiré, UN ajouté : l'insertion-only sans retrait serait un round-trip
    vert mais un diff divergent — l'écart NOMMÉ)."""
    attendu = list(notation.split("\n"))
    attendu[ligne_index] = nouvelle
    return reconstruit == "\n".join(attendu)


# ============================================== LOCALISER-H (le hiérarchique)
class RefusPointeur(Exception):
    """Un refus nommé du pointeur — fail-closed."""

    def __init__(self, nom: str, detail: str):
        super().__init__(f"{nom}: {detail}")
        self.nom = nom
        self.detail = detail


def prompt_localiser_h(emp_requise: str) -> tuple[str, dict]:
    """LE PROMPT H : L'INDEX GROSSIER (le niveau grossier — les IDs + les
    empreintes courtes 8 hex, UN document compact par session, l'empreinte
    sha256 en garde) + LA REQUÊTE (l'identité fine du bloc — l'empreinte
    complète de sa notation). Le modèle choisit l'entrée (le préfixe 8
    hex) et rend L'ENTRÉE FINE : le pointeur littéral (le record 52)."""
    idx = charger_index()
    prompt = (
        "L'OPÉRATION LOCALISER DE LA CARTE TRIADE (le mode hiérarchique —\n"
        "le client expande le pointeur auprès de la carte et confronte\n"
        "l'empreinte aux octets réels).\n\n"
        f"L'INDEX GROSSIER DE LA SESSION (les IDs des blocs et leurs\n"
        f"empreintes COURTES, 8 hex) :\n{idx['document']}\n\n"
        f"LE BLOC À LOCALISER (l'identité — l'empreinte sha256 COMPLÈTE de\n"
        f"sa notation) :\nsha256:{emp_requise}\n\n"
        f"REQUÊTE : localise le bloc ci-dessus dans l'index (l'entrée dont\n"
        f"l'empreinte courte est le PRÉFIXE de l'empreinte complète) et\n"
        f"récupère l'entrée fine — réponds AU FORMAT POINTEUR SEUL, une\n"
        f"seule ligne exactement :\n"
        f"IDENTIFIANT · sha256:<empreinte>\n"
        f"— IDENTIFIANT : l'iNNNNNN de l'entrée choisie de l'index ;\n"
        f"— <empreinte> : l'empreinte sha256 complète recopiée TELLE QUELLE\n"
        f"du bloc à localiser ci-dessus (64 hexadécimaux, aucun calcul).\n"
        f"Rien d'autre.\n"
    )
    return prompt, {"empreinte_index": idx["empreinte"],
                    "empreinte_requise": emp_requise}


def verifie_index_session(empreinte_lue: str) -> None:
    """La garde de l'index : l'empreinte du document d'index confrontée à
    celle du disque — INDEX-DIVERGENT sinon (fail-closed)."""
    idx = charger_index()
    if empreinte_lue != idx["empreinte"]:
        raise RefusPointeur(
            "INDEX-DIVERGENT",
            f"l'empreinte d'index {empreinte_lue[:16]}… != celle du disque "
            f"{idx['empreinte'][:16]}… — l'index a divergé")


def expanser_pointeur(ligne_pointeur: str,
                      table: dict[str, dict] | None = None,
                      entete_soumis: str | None = None) -> dict:
    """L'EXPANSION CÔTÉ CLIENT du pointeur seul (la campagne cq01qv1za —
    le même oracle) : HORS-FORMAT, POINTEUR-INCONNU, EMPREINTE-DIVERGENTE,
    EXPANSION-DIVERGENTE — les QUATRE refus re-roulés."""
    if table is None:
        table = table_carte()
    lignes = [x for x in ligne_pointeur.splitlines() if x.strip()]
    if len(lignes) != 1:
        raise RefusPointeur(
            "HORS-FORMAT",
            f"{len(lignes)} lignes rendues (une exigée) — "
            f"« {ligne_pointeur[:60]}… »")
    m = re.match(r"^(i\d+)\s*·\s*sha256:([0-9a-f]{64})$",
                 lignes[0].strip())
    if not m:
        raise RefusPointeur(
            "HORS-FORMAT",
            "la ligne-pointeur ne porte pas la forme IDENTIFIANT · "
            f"sha256:<64 hex> — « {lignes[0][:70]}… »")
    bid, empreinte = m.group(1), m.group(2)
    if bid not in table:
        raise RefusPointeur("POINTEUR-INCONNU",
                            f"l'identifiant {bid} n'est pas à la carte")
    if empreinte != table[bid]["empreinte"]:
        raise RefusPointeur(
            "EMPREINTE-DIVERGENTE",
            f"rendue {empreinte[:16]}…, la carte porte "
            f"{table[bid]['empreinte'][:16]}… — le pointeur est PÉRIMÉ")
    ex = {"id": bid, "empreinte": empreinte,
          "entete": table[bid]["entete"]}
    if entete_soumis is not None and ex["entete"] != entete_soumis:
        raise RefusPointeur(
            "EXPANSION-DIVERGENTE",
            f"l'entête expansé de {ex['id']} != l'entête du bloc soumis — "
            f"le pointeur désigne un AUTRE bloc que celui de la requête")
    return ex


def confronte_h(reponse: str, emp_requise: str,
                empreinte_index: str) -> dict:
    """LE CLIENT H — l'expansion recoupée (le même oracle que le pointeur
    seul, les QUATRE refus re-roulés) + l'entrée fine confrontée à
    l'index. Retourne l'expansion {id, empreinte, entete}."""
    verifie_index_session(empreinte_index)      # INDEX-DIVERGENT
    idx = charger_index()
    table = table_carte()
    # (1) HORS-FORMAT : la forme de la ligne
    lignes = [x for x in reponse.splitlines() if x.strip()]
    if len(lignes) != 1:
        raise RefusPointeur(
            "HORS-FORMAT",
            f"{len(lignes)} lignes rendues (une exigée) — "
            f"« {reponse[:60]}… »")
    m = re.match(r"^(i\d+)\s*·\s*sha256:([0-9a-f]{64})$",
                 lignes[0].strip())
    if not m:
        raise RefusPointeur(
            "HORS-FORMAT",
            "la ligne-pointeur ne porte pas la forme IDENTIFIANT · "
            f"sha256:<64 hex> — « {lignes[0][:70]}… »")
    bid, empreinte = m.group(1), m.group(2)
    # (2) POINTEUR-INCONNU : l'identifiant pas à la carte
    if bid not in table:
        raise RefusPointeur("POINTEUR-INCONNU",
                            f"l'identifiant {bid} n'est pas à la carte")
    # (3) EMPREINTE-DIVERGENTE : l'empreinte rendue != la carte
    if empreinte != table[bid]["empreinte"]:
        raise RefusPointeur(
            "EMPREINTE-DIVERGENTE",
            f"rendue {empreinte[:16]}…, la carte porte "
            f"{table[bid]['empreinte'][:16]}… — le pointeur est PÉRIMÉ")
    # (4) ENTREE-DIVERGENTE : l'entrée fine contredit l'index grossier
    if bid not in idx["entrees"] or idx["entrees"][bid] != empreinte[:8]:
        raise RefusPointeur(
            "ENTREE-DIVERGENTE",
            f"l'entrée {bid} de l'index porte "
            f"{idx['entrees'].get(bid, '—')} != le préfixe "
            f"{empreinte[:8]} de l'empreinte rendue")
    # (5) EXPANSION-DIVERGENTE : le pointeur désigne un AUTRE bloc que
    # celui de la requête (le choix du niveau grossier était faux)
    if table[bid]["empreinte"] != emp_requise:
        raise RefusPointeur(
            "EXPANSION-DIVERGENTE",
            f"l'entrée expansée {bid} ({table[bid]['nom']}) n'est pas le "
            f"bloc de la requête — l'empreinte demandée "
            f"{emp_requise[:16]}…")
    return {"id": bid, "empreinte": empreinte,
            "entete": table[bid]["entete"]}


# ============================================== AJOUTER-S (le squelette)
BALISE_DEBUT = "; >>> DEBUT-LOGIQUE (le corps du bloc — l'agent remplit ici)"
BALISE_FIN = "; <<< FIN-LOGIQUE"

# la politique de cadre du client (déterministe, dérivée de la spec I) :
# la feuille pure (aucune IAT déclarée) — les cinq non-volatils sauvés,
# l'ombre 0x20 ; le bloc d'IAT déclarée — quatre non-volatils, la zone
# d'appel 0x28 (la liste fermée de la spec le nomme)
CADRE_PUR = (["push rbx", "push r12", "push r13", "push r14", "push r15"],
             "sub rsp, 0x20")
CADRE_IAT = (["push rbx", "push r12", "push r13", "push r14"],
             "sub rsp, 0x28")


def _titre_de(spec: str) -> str:
    return spec.splitlines()[0].strip()


def generer_squelette(nom_bloc: str) -> tuple[str, dict]:
    """LE SQUELETTE DÉTERMINISTE DÉRIVÉ DE LA COUCHE I — généré par le
    client depuis la spec I du bloc (zéro token LLM) : le cadre ABI (le
    prologue/épilogue aux non-volatils sauvés, le shadow space), les
    types (les bornes nommées), la signature (les registres d'arguments).
    Le sujet : un bloc RÉEL du dépôt (l'unité loupe)."""
    spec = (SPECS / f"{nom_bloc}.md").read_text(encoding="utf-8")
    titre = _titre_de(spec)
    # la signature : les registres d'arguments lus des pré-conditions
    args = []
    for m in re.finditer(
            r"P\d+\s+(rcx|rdx|r8|r9|\[rsp\+0x28\])\s*=\s*([^;.\n]{1,70})",
            spec):
        reg, desc = m.group(1), m.group(2).strip().rstrip(",")
        if (reg, desc) not in [(a[0], a[1]) for a in args]:
            args.append((reg, desc))
    # les types : les bornes nommées de la spec ("1 à 32 (MOTIF_MAX)",
    # "TAMPON_SESSION octets (384)")
    types = []
    for m in re.finditer(
            r"\b(\d+)\s+à\s+(\d+)\s*(?:octets?\s*)?\(([A-Z][A-Z_0-9]{2,})\)",
            spec):
        nom, borne = m.group(3), m.group(2)
        if (nom, borne) not in [(t[0], t[1]) for t in types]:
            types.append((nom, borne))
    for m in re.finditer(r"\b([A-Z][A-Z_0-9]{2,})\s+octets\s*\((\d+)\)", spec):
        nom, borne = m.group(1), m.group(2)
        if (nom, borne) not in [(t[0], t[1]) for t in types]:
            types.append((nom, borne))
    # les verdicts nommés (la table des échecs — "verdict -5 ENTRÉE")
    verdicts = []
    for m in re.finditer(
            r"(?:verdict|→)\s+(-\d+)\s+([A-ZÉÈÀÙ][A-ZÉÈÀÙ-]+)", spec):
        v = (m.group(1), m.group(2))
        if v not in verdicts:
            verdicts.append(v)
    # les dépendances héritées (les appelés directs au plan)
    deps = sorted(set(re.findall(r"\b((?:libc|tls13|win)-\d+)\b", spec)))
    # l'IAT déclarée (la liste fermée) — la ligne porte la déclaration,
    # la ligne suivante porte la continuation (les specs s'enveloppent)
    iat = []
    ls = spec.splitlines()
    for k, l in enumerate(ls):
        if "IAT déclarée" not in l:
            continue
        morceau = l + (" " + ls[k + 1] if k + 1 < len(ls) else "")
        morceau = morceau.split("IAT déclarée", 1)[1]
        morceau = re.split(r"[;—]", morceau)[0]
        morceau = morceau.split(":", 1)[-1]
        for nom in re.split(r"[,\s]+", morceau.strip()):
            if nom and nom[0].isalpha() and nom[0].isupper() and nom not in iat:
                iat.append(nom)
    # la politique de cadre (déterministe depuis la spec)
    (pushes, sub) = CADRE_IAT if iat else CADRE_PUR
    pops = list(reversed(pushes))
    lignes_dep = []
    for d in deps:
        if d in PLAN_APPELS:
            sig, adr = PLAN_APPELS[d]
            lignes_dep.append(f";   {d} @ 0x{adr:x} — {sig}")
        else:
            lignes_dep.append(f";   {d} (l'adresse au plan de la carte)")
    entete = [
        f"; {titre}",
        "; LE SQUELETTE DÉTERMINISTE TPL-AJOUT-v1 — dérivé de la couche I",
        "; par le client (zéro token LLM) : le cadre, les types, la",
        "; signature ; l'agent ne remplit que LA LOGIQUE entre les balises.",
        f"; cadre ABI msx64 : non-volatils "
        f"{', '.join(r.split()[1] for r in pushes)} sauvés · "
        f"l'ombre 0x20 à l'appelant · le cadre aligné 16",
        f"; signature : "
        + (" · ".join(f"{r} = {d}" for r, d in args) if args else "—"),
    ]
    if types:
        entete.append("; types : " + " · ".join(f"{n} = {b}"
                                                for n, b in types))
    if verdicts:
        entete.append("; verdicts nommés : "
                      + " · ".join(f"{v} {n}" for v, n in verdicts))
    if lignes_dep:
        entete.append("; les appelés directs (le plan — la liste fermée) :")
        entete.extend(lignes_dep)
    if iat:
        entete.append("; IAT déclarée (la liste fermée) : "
                      + ", ".join(iat)
                      + " — les appels : call qword ptr [rip ± 0x…]")
    entete += [
        "; LA NOTATION DU DOMAINE (le format des lignes de la logique) :",
        "; une instruction par ligne, Intel EXPLICITE — la taille de la",
        "; mémoire TOUJOURS nommée : « mov r12, [rsp+0x28] » INTERDIT →",
        "; « mov r12, qword ptr [rsp + 0x28] » (qword/dword/word/byte ptr) —",
        "; les cibles de saut : des ADRESSES ABSOLUES 0x… OU des étiquettes",
        "; locales « nom : » (la définition seule en ligne, l'opérande",
        "; « jz nom » / « call nom » / « lea rax, [nom] » — le client les",
        "; RÉSOUT aux adresses absolues du slot, la discipline du brouillon)",
        "; — les appels directs call 0x… (les adresses au squelette) —",
        "; AUCUNE directive NASM, AUCUN commentaire dans la logique.",
    ]
    squelette = ("\n".join(entete) + "\n"
                 + "\n".join(pushes) + "\n" + sub + "\n"
                 + BALISE_DEBUT + "\n" + BALISE_FIN + "\n"
                 + "\n".join(f"pop {r.split()[1]}" for r in pops)
                 + "\nret\n")
    infos = {"nom": nom_bloc, "titre": titre, "spec": spec,
             "args": args, "types": types, "verdicts": verdicts,
             "deps": deps, "iat": iat, "pushes": pushes, "sub": sub,
             "squelette": squelette, "rva": _rva_du_bloc(nom_bloc),
             "slot": _taille_du_slot(nom_bloc)}
    return squelette, infos


def prompt_ajouter_s(nom_bloc: str) -> tuple[str, dict]:
    """LE PROMPT S : le contrat I + le squelette déterministe ; l'agent ne
    rend QUE LA LOGIQUE (le corps entre les balises) — JAMAIS le squelette."""
    squelette, infos = generer_squelette(nom_bloc)
    prompt = (
        "L'OPÉRATION AJOUTER DE LA CARTE TRIADE (le mode SQUELETTE — le\n"
        "cadre ABI, les types et la signature sont DÉRIVÉS de la couche I\n"
        "par le client : le squelette ci-dessous est DÉTERMINISTE ; tu ne\n"
        "remplis QUE LA LOGIQUE).\n\n"
        f"LE CONTRAT DE COUCHE I (mot pour mot) :\n{infos['spec']}\n\n"
        f"LE SQUELETTE (généré par le client — NE LE RENDS PAS, il est\n"
        f"déjà là ; les règles de notation vivent en tête du squelette) :\n"
        f"{squelette}\n"
        f"REQUÊTE : écris UNIQUEMENT LES LIGNES DE LA LOGIQUE — le corps du\n"
        f"bloc qui vivra entre les balises « {BALISE_DEBUT} » et\n"
        f"« {BALISE_FIN} » (les gardes des pré-conditions, la logique du\n"
        f"post-condition, les étiquettes résolues aux cibles absolues).\n"
        f"La PREMIÈRE ligne de ta réponse est la première instruction, la\n"
        f"DERNIÈRE est la dernière — aucune balise, aucun squelette, aucun\n"
        f"commentaire, aucune explication : la réponse n'est QUE les\n"
        f"instructions de la logique.\n"
    )
    return prompt, infos


# LES LIGNES D'INSTRUCTION ADMISES — le détecteur du domaine étendu au
# VOCABULAIRE RÉEL des notations (movsxd, jc, rol — l'inventaire des 18
# blocs, AUCUNE directive de données : db/dw/dd/dq refusés — le corps du
# domaine est l'instruction pure ; SUR-ensemble du DEBUT_CODE v8, aucun
# contrôle retiré)
from client_hunks import DEBUT_CODE  # noqa: E402
MON_INSTRUCTION = re.compile(
    r"^(?:add|and|call|cdq|cld|cmp|dec|div|idiv|imul|inc|ja|jae|jb|jbe|"
    r"jc|je|jg|jge|jl|jle|jmp|jne|jns|jnz|js|jz|lea|mov|movsx|movsxd|"
    r"movzx|neg|nop|not|or|pop|push|rep|ret|rol|sar|shl|shr|sub|test|"
    r"xor|xchg|mul|sete|setne|setg|setl|seta|setb|cmov\w+|cqo|leave|"
    r"loop|int3)\b")

# LA GRAMMAIRE DU BROUILLON (les étiquettes locales — l'auteur les écrit,
# le client les résout ; loupe/outils/auteur.py, la même discipline)
RE_DEF_ETIQ = re.compile(r"^\.?([A-Za-z_]\w*)\s*:\s*$")
RE_OP_ETIQ = re.compile(r"^(j\w+|loop\w*|call)\s+\.?([A-Za-z_]\w*)$")
RE_LEA_ETIQ = re.compile(r"^(lea\s+\w+), \[\.?([A-Za-z_]\w*)\]$")
REGISTRES64 = {"rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"} \
    | {f"r{i}" for i in range(8, 16)}


def resoudre_logique(lignes: list[str], rva_depart: int
                     ) -> tuple[list[str], dict]:
    """LA RÉSOLUTION DES ÉTIQUETTES LOCALES — LA DISCIPLINE DE L'AUTEUR
    (le point fixe des tailles, huit passes au plus ; keystone assemble,
    rien d'autre) : les définitions « nom : » deviennent des adresses
    absolues (rva_depart + la somme des tailles précédentes), les
    opérandes « jcc nom » / « call nom » / « lea reg, [nom] » sont
    substituées. Retourne (les lignes explicites, les étiquettes
    résolues)."""
    from keystone import Ks, KS_ARCH_X86, KS_MODE_64
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    instructions, etiquettes_idx = [], []
    for l in lignes:
        m = RE_DEF_ETIQ.match(l)
        if m:
            etiquettes_idx.append((m.group(1), len(instructions)))
            continue
        instructions.append(l)
    if not instructions:
        raise Refus("HORS-FORMAT", "la logique est vide")

    def _taille(ligne: str, adresse: int, etiquettes: dict) -> int:
        try:
            enc, _ = ks.asm(_substitue(ligne, adresse, etiquettes,
                                       taille=True), adresse)
        except Exception as err:
            raise Refus("HORS-FORMAT",
                        f"ligne inassemblable : {ligne!r} "
                        f"({str(err)[:60]})")
        if not enc:
            raise Refus("HORS-FORMAT",
                        f"ligne inassemblable (taille) : {ligne!r}")
        return len(enc)

    etiquettes = {nom: rva_depart + 0x80 for nom, _ in etiquettes_idx}
    for _ in range(8):
        tailles, adresse = [], rva_depart
        for ligne in instructions:
            t = _taille(ligne, adresse, etiquettes)
            tailles.append(t)
            adresse += t
        nouvelles = {nom: rva_depart + sum(tailles[:i])
                     for nom, i in etiquettes_idx}
        if nouvelles == etiquettes:
            break
        etiquettes = nouvelles
    else:
        raise Refus("HORS-FORMAT",
                    "le point fixe des étiquettes ne converge pas (8 passes)")
    explicites, adresse = [], rva_depart
    for ligne in instructions:
        explicites.append(_substitue(ligne, adresse, etiquettes))
        adresse += _taille(ligne, adresse, etiquettes)
    return explicites, etiquettes


def _substitue(ligne: str, adresse: int, etiquettes: dict,
               taille: bool = False) -> str:
    """La substitution d'une ligne : l'étiquette → l'adresse absolue (ou
    une forme de la MÊME TAILLE au calcul de taille) — le lea à la
    façon de l'auteur : [rip ± disp], disp = cible − (adresse + 7)."""
    m = RE_LEA_ETIQ.match(ligne)
    if m:
        if m.group(2) in REGISTRES64:
            return ligne               # lea reg, [reg] — l'adressage direct
        if taille:
            return f"{m.group(1)}, [rip + 0x0]"
        cible = etiquettes.get(m.group(2))
        if cible is None:
            raise Refus("HORS-FORMAT", f"étiquette inconnue : {m.group(2)}")
        disp = cible - (adresse + 7)
        if disp >= 0:
            return f"{m.group(1)}, [rip + 0x{disp:x}]"
        return f"{m.group(1)}, [rip - 0x{-disp:x}]"
    m = RE_OP_ETIQ.match(ligne)
    if m:
        mnemo, nom = m.groups()
        if nom in REGISTRES64:
            return ligne               # l'appel indirect DÉCLARÉ
        cible = etiquettes.get(nom)
        if cible is None:
            raise Refus("HORS-FORMAT", f"étiquette inconnue : {nom}")
        return f"{mnemo} 0x{cible:x}"
    return ligne


def _rva_du_bloc(nom_bloc: str) -> int | None:
    """Le slot RVA du bloc — LU de la vérité-terrain (le plan d'adressage,
    lecture seule)."""
    vt = json.loads((REPO / "atelier-localiser-5gfx6pwkj" /
                     "verites-terrain.json").read_text(encoding="utf-8"))
    for b in vt["blocs"]:
        if b["nom"] == nom_bloc:
            return b["slot"]
    return None


def _taille_du_slot(nom_bloc: str) -> int | None:
    vt = json.loads((REPO / "atelier-localiser-5gfx6pwkj" /
                     "verites-terrain.json").read_text(encoding="utf-8"))
    for b in vt["blocs"]:
        if b["nom"] == nom_bloc:
            return b["taille"]
    return None


def assembler_s(squelette: str, logique: str,
                infos: dict | None = None) -> tuple[str, str]:
    """LE CLIENT ASSEMBLE : (1) HORS-FORMAT — la logique ne rend QUE des
    lignes d'instruction du domaine OU des définitions d'étiquettes
    locales (la grammaire du brouillon : « nom : ») ; (2) LA RÉSOLUTION
    DES ÉTIQUETTES — LA DISCIPLINE DE L'AUTEUR (loupe/outils/auteur.py :
    le point fixe des tailles, keystone assemble, rien d'autre) aux
    adresses absolues du slot ; (3) l'assemblage squelette + logique
    entre les balises ; (4) LE CADRE INTACT (l'oracle régénéré : le
    prologue/épilogue présents, dans l'ordre) ; (5) le round-trip exact
    (keystone/capstone — ROUND-TRIP-DIVERGENT sinon)."""
    if BALISE_DEBUT not in squelette or BALISE_FIN not in squelette:
        raise Refus("HORS-FORMAT", "le squelette ne porte pas ses balises")
    lignes = [l.rstrip() for l in logique.strip("\r\n").split("\n")]
    if not any(l.strip() for l in lignes):
        raise Refus("HORS-FORMAT", "la logique est vide")
    for k, l in enumerate(lignes):
        s = l.split(";")[0].strip()
        if not s:
            continue
        if s.startswith(("```", ">>>", "<<<")) or "```" in s:
            raise Refus("HORS-FORMAT",
                        f"la ligne {k + 1} de la logique est un artefact : "
                        f"{s[:60]!r}")
        if RE_DEF_ETIQ.match(s):
            continue                     # la définition d'étiquette
        if not MON_INSTRUCTION.match(s):
            raise Refus("HORS-FORMAT",
                        f"la ligne {k + 1} n'est pas une instruction du "
                        f"domaine : {s[:60]!r}")
    # l'ancre d'adresse : le slot du bloc (le plan d'adressage) + la
    # taille du prologue (assemblée — déterministe)
    rva = 0x4000
    if infos is not None and infos.get("rva") is not None:
        rva = infos["rva"]
    from keystone import Ks, KS_ARCH_X86, KS_MODE_64
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    taille_prologue = 0
    if infos is not None:
        try:
            octets, _ = ks.asm("\n".join(infos["pushes"]
                                           + [infos["sub"]]))
            taille_prologue = len(octets)
        except Exception:
            taille_prologue = 0
    explicites, etiquettes_resolues = resoudre_logique(
        [l.split(";")[0].strip() for l in lignes if l.split(";")[0].strip()],
        rva + taille_prologue)
    corps = "\n".join(explicites)
    avant, apres = squelette.split(BALISE_DEBUT, 1)
    _, apres = apres.split(BALISE_FIN, 1)
    note_etiq = ""
    if etiquettes_resolues:
        note_etiq = ("; Étiquettes résolues : " + ", ".join(
            f"{n}=0x{a:x}" for n, a in etiquettes_resolues.items()) + "\n")
    assemble = (avant + note_etiq + BALISE_DEBUT + "\n" + corps + "\n"
                + BALISE_FIN + apres)
    # LE CADRE INTACT : le prologue et l'épilogue du squelette présents
    if infos is not None:
        for l in infos["pushes"] + [infos["sub"]]:
            if l not in assemble:
                raise Refus("HORS-FORMAT",
                            f"le cadre du squelette est cassé : « {l} » "
                            f"absent de l'assemblage")
    ok, detail = round_trip(assemble)
    if not ok:
        raise Refus("ROUND-TRIP-DIVERGENT", detail)
    return assemble, detail


# ------------------------------------------------------------ les autotests
def autotest() -> int:
    """LES GESTES DE SÉCURITÉ DU CLIENT — chaque refus nommé vécu."""
    verts = 0
    _, tpl_emp = charger_tpl()
    notation = (NOTATIONS / "loupe-13-recherche.asm").read_text(
        encoding="utf-8")

    # T2 : l'application honnête (le diff réel de la tâche loupe-13)
    p, meta = prompt_editer_t2("loupe-13-recherche", notation, 17,
                               "cmp r9, 32", "cmp r9, 31")
    assert TPL_ID in p and tpl_emp in p and "cmp r9, 32" in p
    assert "LA GRAMMAIRE" not in p        # le corps N'EST PAS au prompt
    hunks_ok = ("@@ hunk 1\nbase: cmp r9, 32\n- cmp r9, 32\n"
                "+ cmp r9, 31\nFIN-HUNKS")
    r, d = appliquer_t2(notation, meta["notation_empreinte"], hunks_ok,
                        tpl_emp, meta["tpl_empreinte"])
    assert "cmp r9, 31" in r and "cmp r9, 32" not in r
    assert diff_exact(notation, 17, "cmp r9, 31", r)
    print(f"VERT  T2 l'application honnête + round-trip + diff exact : "
          f"{d[:48]}")
    verts += 1
    # T2 : GABARIT-DIVERGENT (l'empreinte du gabarit mutée au prompt)
    try:
        appliquer_t2(notation, meta["notation_empreinte"], hunks_ok,
                     tpl_emp, "0" * 64)
        print("ROUGE : GABARIT-DIVERGENT non attrapé")
        return 2
    except Refus as e:
        assert e.nom == "GABARIT-DIVERGENT"
        print(f"VERT  T2 le refus {e.nom} attrapé au premier nom")
        verts += 1
    # T2 : CONTEXTE-DIVERGENT (la notation en cache diverge)
    try:
        appliquer_t2(notation + "\n; muté", meta["notation_empreinte"],
                     hunks_ok, tpl_emp, meta["tpl_empreinte"])
        print("ROUGE : CONTEXTE-DIVERGENT non attrapé")
        return 2
    except Refus as e:
        assert e.nom == "CONTEXTE-DIVERGENT"
        print(f"VERT  T2 le refus {e.nom} attrapé au premier nom")
        verts += 1
    # T2 : HORS-FORMAT (la réponse hors grammaire du gabarit)
    try:
        appliquer_t2(notation, meta["notation_empreinte"],
                     "Voici les hunks :\n@@ hunk 1\nFIN-HUNKS",
                     tpl_emp, meta["tpl_empreinte"])
        print("ROUGE : HORS-FORMAT non attrapé")
        return 2
    except Refus as e:
        assert e.nom == "HORS-FORMAT"
        print(f"VERT  T2 le refus {e.nom} attrapé au premier nom")
        verts += 1
    # T2 : le contrôle négatif de dépendance hors fenêtre — une ligne
    # HORS ±12 mutée dans le cache → la garde de la notation complète
    # attrape (CONTEXTE-DIVERGENT) : la fenêtre n'affaiblit PAS la garde
    lignes_mut = notation.split("\n")
    lignes_mut[-2] = "pop rbx ; muté hors fenêtre"
    try:
        appliquer_t2("\n".join(lignes_mut), meta["notation_empreinte"],
                     hunks_ok, tpl_emp, meta["tpl_empreinte"])
        print("ROUGE : la mutation hors fenêtre non attrapée")
        return 2
    except Refus as e:
        assert e.nom == "CONTEXTE-DIVERGENT"
        print(f"VERT  T2 la mutation HORS FENÊTRE attrapée — {e.nom} "
              f"(la garde sha256 de la notation complète)")
        verts += 1

    # H : l'expansion honnête + les quatre refus + les deux gardes
    idx = charger_index()
    assert len(idx["entrees"]) == 18
    table = table_carte()
    bid = "i110013"
    emp = table[bid]["empreinte"]
    ex = confronte_h(f"{bid} · sha256:{emp}", emp, idx["empreinte"])
    assert ex["id"] == bid and ex["entete"] == table[bid]["entete"]
    print("VERT  H l'expansion honnête (le choix exact, l'entrée fine)")
    verts += 1
    cas_h = [
        ("HORS-FORMAT", "Le pointeur est :\ni110013 · sha256:" + emp),
        ("POINTEUR-INCONNU", f"i999999 · sha256:{emp}"),
        ("EMPREINTE-DIVERGENTE",
         f"{bid} · sha256:{'0' * 63 + ('1' if emp[-1] != '1' else '2')}"),
        ("EXPANSION-DIVERGENTE",
         f"i110014 · sha256:{table['i110014']['empreinte']}"),
    ]
    emp_requise = emp
    for attendu, rep in cas_h:
        try:
            confronte_h(rep, emp_requise, idx["empreinte"])
            print(f"ROUGE : {attendu} non attrapé")
            return 2
        except RefusPointeur as e:
            assert e.nom == attendu, (e.nom, attendu)
            print(f"VERT  H le refus {e.nom} attrapé au premier nom")
            verts += 1
    # H : la garde d'index (INDEX-DIVERGENT)
    try:
        confronte_h(f"{bid} · sha256:{emp}", emp, "0" * 64)
        print("ROUGE : INDEX-DIVERGENT non attrapé")
        return 2
    except RefusPointeur as e:
        assert e.nom == "INDEX-DIVERGENT"
        print(f"VERT  H le refus {e.nom} attrapé au premier nom")
        verts += 1

    # S : l'assemblage honnête (la logique réelle de loupe-13 rendue)
    squelette, infos = generer_squelette("loupe-13-recherche")
    notation_reelle = (NOTATIONS / "loupe-13-recherche.asm").read_text(
        encoding="utf-8")
    lignes_reelles = []
    for l in notation_reelle.splitlines():
        s = l.strip()
        if not s or s.startswith(";"):
            continue
        if s.startswith(("push rbx", "push r12", "push r13", "push r14",
                         "push r15", "pop r15", "pop r14", "pop r13",
                         "pop r12", "pop rbx")) or s == "ret" \
                or s.startswith("sub rsp,"):
            continue
        lignes_reelles.append(s)
    logique = "\n".join(lignes_reelles)
    assemblage, det = assembler_s(squelette, logique, infos)
    print(f"VERT  S l'assemblage squelette + logique réelle : {det[:48]}")
    verts += 1
    # S : les étiquettes locales RÉSOLUES (la discipline du brouillon)
    assemblage, det = assembler_s(
        squelette, ".boucle:\ninc r15\ncmp r15, 32\njb .boucle", infos)
    assert "jb 0x" in assemblage
    print(f"VERT  S les étiquettes locales résolues aux adresses : {det[:44]}")
    verts += 1
    # S : l'étiquette inconnue → HORS-FORMAT
    try:
        assembler_s(squelette, "inc r15\njmp nulle_part", infos)
        print("ROUGE : l'étiquette inconnue non attrapée")
        return 2
    except Refus as e:
        assert e.nom == "HORS-FORMAT"
        print(f"VERT  S le refus {e.nom} attrapé (l'étiquette inconnue)")
        verts += 1
    # S : la logique vide → HORS-FORMAT
    try:
        assembler_s(squelette, "   ", infos)
        print("ROUGE : la logique vide non attrapée")
        return 2
    except Refus as e:
        assert e.nom == "HORS-FORMAT"
        print(f"VERT  S le refus {e.nom} attrapé (la logique vide)")
        verts += 1
    # S : l'instruction inassemblable → refus au premier nom (la ligne
    # meurt à la résolution — keystone refuse — HORS-FORMAT ; si elle
    # assemble mais diverge au désassemblage → ROUND-TRIP-DIVERGENT)
    try:
        assembler_s(squelette, "mov eax, 99999999999999999999", infos)
        print("ROUGE : l'instruction invalide non attrapée")
        return 2
    except Refus as e:
        assert e.nom in ("HORS-FORMAT", "ROUND-TRIP-DIVERGENT")
        print(f"VERT  S le refus {e.nom} attrapé (l'instruction impossible)")
        verts += 1

    print(f"\nLE CLIENT GABARITS : {verts} VERT — les refus nommés "
          "fail-closed, le round-trip inchangé")
    return 0


if __name__ == "__main__":
    sys.exit(autotest())
