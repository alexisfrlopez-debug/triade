#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""triade_feedback.py — L'OUTIL `triade feedback` (witgt6qta, la vague 15).
La part MEASURED est EXTRAITE MÉCANIQUEMENT du journal de session JSONL
déjà consigné (jamais retapée, coût token marginal ≈ 0) ; commentary est
la seule part budgétée (≤500 tokens). LES PORTES fail-closed :
  — champ requis manquant → REFUS nommé ;
  — SECRET DÉTECTÉ (l'équivalent Python gitleaks : les motifs jetons/
    clés/chemins absolus/usernames) → REFUS, le rapport JAMAIS écrit ;
  — chemins/usernames anonymisés (le pseudonymage mécanique à la porte).
LA SORTIE : report-<date>-<kitver>.json + le gabarit d'issue GitHub
pré-rempli ; JAMAIS d'envoi automatique (le geste humain D122) ;
AUCUNE dépendance réseau (R10 — zéro appel réseau à la génération).

Usage :
  triade_feedback.py generer <journal.jsonl> <kit_version> [--commentaire FICHIER]
  triade_feedback.py verifier <report.json>          (la porte de schéma)
  triade_feedback.py porte-secrets <fichier>         (le contrôle négatif)
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import sys

ICI = pathlib.Path(__file__).resolve().parent
SCHEMA = ICI / "TRIADE-FEEDBACK-v1.schema.json"

# ------------------------------------------------- LA PORTE DE SECRETS -----
# l'équivalent Python gitleaks : les MOTIFS nommés, chaque classe une
# règle ; le contrôle négatif vit au test (la phrase marquée plantée).
MOTIFS_SECRETS = [
    ("jeton_github", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,255}")),
    ("cle_privee_pem", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("jeton_bearer", re.compile(r"(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*")),
    ("refresh_token_oauth", re.compile(
        r"1//[A-Za-z0-9\-_]{100,}")),
    ("jeton_generique", re.compile(
        r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*\S{16,}")),
    ("chemin_absolu", re.compile(
        r"(?<![\w])(/[A-Za-z0-9_.-]+){3,}")),
    ("username_système", re.compile(
        r"(?i)/home/[A-Za-z0-9_.-]+|/Users/[A-Za-z0-9_.-]+")),
]
# la phrase marquée : TOUTE ligne portant la balise de test est un secret
# par construction (le contrôle négatif D105 : la phrase PUBBLIQUE MARQUÉE)
MARQUEUR_PHRASE_TEST = "PHRASE-TEST-MARQUEE-D105"


def scan_secrets(texte: str) -> list[tuple[str, str]]:
    trouves = []
    if MARQUEUR_PHRASE_TEST in texte:
        trouves.append(("phrase_test_marquee",
                        "la balise de phrase de test D105 interdit le rapport"))
    for nom, motif in MOTIFS_SECRETS:
        m = motif.search(texte)
        if m:
            trouves.append((nom, m.group(0)[:40] + "…"))
    return trouves


# ------------------------------------- L'ANONYMISATION MÉCANIQUE ----------
def anonymiser(texte: str) -> str:
    """chemins et usernames : le pseudonymage mécanique à la porte."""
    texte = re.sub(r"/home/[A-Za-z0-9_.-]+", "/home/USER", texte)
    texte = re.sub(r"/Users/[A-Za-z0-9_.-]+", "/Users/USER", texte)
    texte = re.sub(r"(?<![\w])C:\\Users\\[A-Za-z0-9_.-]+",
                   "C:\\\\Users\\\\USER", texte)
    return texte


# ----------------------------- L'EXTRACTION MÉCANIQUE (≈0 token) ----------
def extraire_measured(journal: list[dict]) -> dict:
    """la part measured DU JOURNAL (jamais retapée) : les opérations, les
    refus par classe, les tokens natifs, le wall ; les défauts F/L."""
    operations = 0
    refus: dict[str, int] = {}
    tokens = 0
    wall = 0.0
    defauts = []
    for entree in journal:
        kind = entree.get("type", "")
        if kind == "operation":
            operations += 1
            tokens += int(entree.get("tokens_natifs", 0))
            wall += float(entree.get("wall_s", 0))
        elif kind == "refus":
            classe = entree.get("classe", "non_nomme")
            refus[classe] = refus.get(classe, 0) + 1
            tokens += int(entree.get("tokens_natifs", 0))
        elif kind == "defaut_fl":
            defauts.append({
                "classe": entree.get("classe", "non_nomme"),
                "locus": entree.get("locus", "kit"),
                "evidence_sha256": entree.get("evidence_sha256", ""),
            })
    return {"operations": operations, "refus_par_classe": refus,
            "tokens_natifs": tokens, "wall": round(wall, 3),
            "defauts_fl": defauts}


# ------------------------------------------------- LA PORTE DE SCHÉMA -----
def verifier_schema(rapport: dict) -> list[str]:
    erreurs = []
    if rapport.get("schema") != "TRIADE-FEEDBACK-v1":
        erreurs.append("champ requis manquant/erroné : schema "
                       "(TRIADE-FEEDBACK-v1 attendu)")
    for champ in ("kit", "agent", "env", "capability", "measured", "consent"):
        if champ not in rapport:
            erreurs.append(f"champ requis manquant : {champ}")
    if "kit" in rapport:
        for c in ("contract", "manifest"):
            if c not in rapport["kit"]:
                erreurs.append(f"champ requis manquant : kit.{c}")
    if "agent" in rapport and "family" not in rapport["agent"]:
        erreurs.append("champ requis manquant : agent.family")
    if "env" in rapport:
        for c in ("os", "cpu_class"):
            if c not in rapport["env"]:
                erreurs.append(f"champ requis manquant : env.{c}")
    if "capability" in rapport:
        for c in ("constantes_128", "smoke_notation"):
            if c not in rapport["capability"]:
                erreurs.append(f"champ requis manquant : capability.{c}")
    if "measured" in rapport:
        for c in ("operations", "refus_par_classe", "tokens_natifs", "wall"):
            if c not in rapport["measured"]:
                erreurs.append(f"champ requis manquant : measured.{c}")
        for d in rapport["measured"].get("defauts_fl", []):
            for c in ("classe", "locus", "evidence_sha256"):
                if c not in d:
                    erreurs.append(
                        f"champ requis manquant : measured.defauts_fl[].{c}")
            if d.get("locus") not in ("kit", "piece"):
                erreurs.append("measured.defauts_fl[].locus ∈ {kit, piece} "
                               "exigé")
    if "consent" in rapport:
        if rapport["consent"].get("licence") != "CC-BY-4.0":
            erreurs.append("consent.licence = CC-BY-4.0 exigé")
        if "public_digest" not in rapport["consent"]:
            erreurs.append("champ requis manquant : consent.public_digest")
    if "commentary" in rapport and len(rapport["commentary"]) > 5000:
        erreurs.append("commentary > 5000 caractères (la part budgétée "
                       "≤500 tokens)")
    inconnus = set(rapport) - {"schema", "kit", "agent", "env", "capability",
                               "measured", "commentary", "consent",
                               "signature_adopteur"}
    if inconnus:
        erreurs.append(f"champs inconnus refusés : {sorted(inconnus)}")
    return erreurs


# ------------------------------------------------- LA COMMANDE ------------
def cmd_generer(args) -> int:
    journal_txt = pathlib.Path(args.journal).read_text(encoding="utf-8")
    journal = [json.loads(l) for l in journal_txt.splitlines() if l.strip()]

    # LA PORTE DE SECRETS sur le journal BRUT (fail-closed : le rapport
    # n'est JAMAIS écrit si un secret est détecté)
    secrets = scan_secrets(journal_txt)
    if secrets:
        print("REFUS — secrets détectés au journal (le rapport n'est pas écrit) :",
              file=sys.stderr)
        for nom, extrait in secrets:
            print(f"  [{nom}] {extrait}", file=sys.stderr)
        return 2

    measured = extraire_measured(journal)
    commentaire = ""
    if args.commentaire:
        commentaire = pathlib.Path(args.commentaire).read_text(
            encoding="utf-8").strip()
        secrets_c = scan_secrets(commentaire)
        if secrets_c:
            print("REFUS — secrets détectés au commentaire :", file=sys.stderr)
            for nom, extrait in secrets_c:
                print(f"  [{nom}] {extrait}", file=sys.stderr)
            return 2

    agent_id = os.environ.get("TRIADE_AGENT_ID", "identifier_as_exposed")
    rapport = {
        "schema": "TRIADE-FEEDBACK-v1",
        "kit": {
            "contract": os.environ.get("TRIADE_KIT_CONTRACT", "CONTRAT-<version>"),
            "manifest": os.environ.get("TRIADE_KIT_MANIFEST", "MANIFESTE-<sha256>"),
        },
        "agent": {
            "family": os.environ.get("TRIADE_AGENT_FAMILY", "famille-non-nommee"),
            "identifier_as_exposed": anonymiser(agent_id),
            "checkpoint": "not_exposed",
        },
        "env": {
            "os": anonymiser(os.environ.get("TRIADE_ENV_OS", "non-nomme")),
            "cpu_class": os.environ.get("TRIADE_ENV_CPU", "non-nommee"),
        },
        "capability": {
            "constantes_128": os.environ.get(
                "TRIADE_CAP_128", "non-mesure"),
            "smoke_notation": os.environ.get(
                "TRIADE_CAP_SMOKE", "non-mesure"),
        },
        "measured": measured,
        "commentary": anonymiser(commentaire),
        "consent": {
            "public_digest": hashlib.sha256(
                json.dumps(measured, sort_keys=True).encode()).hexdigest(),
            "licence": "CC-BY-4.0",
        },
    }
    erreurs = verifier_schema(rapport)
    if erreurs:
        print("REFUS — la porte de schéma (le rapport n'est pas écrit) :",
              file=sys.stderr)
        for e in erreurs:
            print(f"  {e}", file=sys.stderr)
        return 2

    date = datetime.date.today().strftime("%Y%m%d")
    sortie = pathlib.Path(f"report-{date}-{args.kit_version}.json")
    sortie.write_text(json.dumps(rapport, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")

    # LE GABARIT D'ISSUE (pré-rempli, JAMAIS envoyé — le geste humain D122)
    gabarit = pathlib.Path(f"issue-{date}-{args.kit_version}.md")
    gabarit.write_text(f"""<!-- le gabarit d'issue GitHub PRÉ-REMPLI — l'envoi
     appartient à l'adopteur (le geste humain D122) ; RELIRE avant
     d'envoyer (DOC-FEEDBACK : lancer à la fin de session, relire,
     envoyer si consenti) -->
**Rapport adopteur TRIADE-FEEDBACK-v1** — kit {args.kit_version}

- famille : {rapport['agent']['family']} (identifiant tel qu'exposé :
  {rapport['agent']['identifier_as_exposed']})
- opérations : {measured['operations']} ; tokens natifs :
  {measured['tokens_natifs']} ; wall : {measured['wall']} s
- refus par classe : {json.dumps(measured['refus_par_classe'])}
- défauts F/L : {len(measured['defauts_fl'])} (locus kit/pièce, les
  empreintes au rapport)
- la dérivation des 128 constantes : {rapport['capability']['constantes_128']}
- le digest public du bloc mesuré : {rapport['consent']['public_digest'][:16]}…
- licence : CC-BY-4.0 (le consentement au rapport joint)

<!-- Joindre : {sortie.name} — relire le rapport AVANT l'envoi -->
""", encoding="utf-8")
    print(f"OK — {sortie} + {gabarit} (le geste d'envoi appartient à "
          f"l'adopteur ; AUCUN appel réseau effectué)")
    return 0


def cmd_verifier(args) -> int:
    rapport = json.loads(pathlib.Path(args.rapport).read_text(encoding="utf-8"))
    erreurs = verifier_schema(rapport)
    if erreurs:
        print("REFUS — la porte de schéma :", file=sys.stderr)
        for e in erreurs:
            print(f"  {e}", file=sys.stderr)
        return 2
    print("VERT — le rapport conforme au schéma TRIADE-FEEDBACK-v1")
    return 0


def cmd_porte_secrets(args) -> int:
    texte = pathlib.Path(args.fichier).read_text(encoding="utf-8")
    secrets = scan_secrets(texte)
    if secrets:
        print("REFUS — secrets détectés :", file=sys.stderr)
        for nom, extrait in secrets:
            print(f"  [{nom}] {extrait}", file=sys.stderr)
        return 2
    print("VERT — aucun secret détecté")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="triade feedback",
                                description="l'outil de rapport adopteur "
                                "TRIADE-FEEDBACK-v1 (witgt6qta)")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generer", help="extraire le rapport du journal "
                        "(la part measured mécanique)")
    g.add_argument("journal")
    g.add_argument("kit_version")
    g.add_argument("--commentaire")
    g.set_defaults(f=cmd_generer)
    v = sub.add_parser("verifier", help="la porte de schéma sur un rapport")
    v.add_argument("rapport")
    v.set_defaults(f=cmd_verifier)
    s = sub.add_parser("porte-secrets", help="le scan seul (le contrôle)")
    s.add_argument("fichier")
    s.set_defaults(f=cmd_porte_secrets)
    args = p.parse_args()
    return args.f(args)


if __name__ == "__main__":
    sys.exit(main())
