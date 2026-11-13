#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compter_tokens.py — LE COMPTEUR DE TOKENS DE LA CAMPAGNE DE COMPARAISON
(paquet 5 de la vague 3, l'instruction 54wni4hzh ; le plan pré-enregistré
consigné à D204).

LA COMMANDE : « tokens réels mesurés depuis les logs d'usage API (plus
jamais ×1,08 quand un log existe) ». L'instrument :

  1. CHAQUE appel au modèle passe PAR CET OUTIL (le chemin instrumenté
     du plan, CA3) — l'outil appelle le CLI z-ai, reçoit la réponse
     JSON, et LIT le champ `usage` DEPUIS LA RÉPONSE DE L'API : le
     compte est le LOG, jamais une estimation ;
  2. chaque appel est journalisé UNE LIGNE JSON au fichier de campagne
     (horodatage, bras, phase, tâche, appel id, modèle, prompt /
     completion / total tokens, la empreinte sha256 de l'échange) ;
  3. L'ESTIMATION ×1,08 EST REFUSÉE PAR CONSTRUCTION quand le log
     existe : l'outil ne sait même pas estimer — il ne sait que lire ;
     un appel manquant (hors chemin instrumenté) est un ÉCART NOMMÉ au
     rapport, jamais un chiffre reconstruit.

LA SORTIE : la réponse du modèle à l'appelant (stdout, le texte), et la
ligne JSON au journal (l'option --journal, par défaut le journal de
campagne nommé par le plan).

Usage :
  python3 compter_tokens.py --bras T --phase notation --tache loupe-05 \
      --prompt-file demande.txt [--system-file syst.txt] \
      [--journal preuves_v150/comparaison_resultats/journal_tokens.jsonl]
  python3 compter_tokens.py --total \
      --journal preuves_v150/comparaison_resultats/journal_tokens.jsonl

L'ÉDITION v2 (le 14/11/2026 au soir) — LA SORTIE SANS FAUTE DE PAGE DE
CODES, la même réparation que le chronomètre v3 (l'écart nommé du
premier run du GUI : un stdout PIPÉ sous Windows vit en cp1252 où
« ≠ » est inencodable — UnicodeEncodeError à l'annonce d'un écart) :
les flux reconfigurés en UTF-8 errors="replace" (le préambule
(ci-dessous) protège AUSSI l'impression de la réponse du modèle, qui
peut porter n'importe quel Unicode) ; l'annonce de l'écart rendue
cp1252-sûre (« != » au lieu de « ≠ »). Le format du journal demeure
CELUI DE LA v1, octet pour octet.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

# v2 — LA SORTIE SANS FAUTE DE PAGE DE CODES (la réparation du
# chronomètre v3, portée au compteur) : un stdout PIPÉ ou REDIRIGÉ sous
# Windows vit en cp1252 — « ≠ » (U+2260) y est inencodable, et la
# réponse du modèle peut porter n'importe quel Unicode. Les flux se
# reconfigurent en UTF-8 errors="replace" : AUCUNE annonce ne peut
# lever, quel que soit le flux.
for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        # un flux fermé ou étranger : l'annonce cp1252-sûre ci-dessous
        # demeure
        pass

# le journal de campagne — créé PAR LA PREMIÈRE MESURE (CA1 : le dossier
# des résultats naît du premier appel instrumenté, jamais avant le plan)
JOURNAL_DEFAUT = (pathlib.Path(__file__).resolve().parents[1]
                  / "preuves_v150" / "comparaison_resultats"
                  / "journal_tokens.jsonl")

PHASES = ("spec", "notation", "source-c", "tests-c", "oracle", "build",
          "correctif", "ceremonie", "revue", "analyse", "autre")


def horodatage() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def appeler_et_compter(bras: str, phase: str, tache: str,
                       prompt: str, system: str | None,
                       journal: pathlib.Path,
                       garde_brut: pathlib.Path | None = None) -> tuple[str, dict]:
    """UN appel au modèle, compté DEPUIS LA RÉPONSE (le log d'usage).

    Retourne (le texte de la réponse, la ligne journalisée).
    L'option garde_brut conserve la réponse BRUTE de l'API (le log
    intégral) à côté du journal — la preuve du dry-run : la ligne
    journalisée doit être ÉGALE au champ usage du log, à l'unité près."""
    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False,
            encoding="utf-8") as f:
        chemin_reponse = pathlib.Path(f.name)
    cmd = ["z-ai", "chat", "--prompt", prompt, "-o", str(chemin_reponse)]
    if system:
        cmd += ["--system", system]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if proc.returncode != 0:
        chemin_reponse.unlink(missing_ok=True)
        raise RuntimeError(f"l'appel z-ai a échoué : {proc.stderr[:400]}")
    reponse = json.loads(chemin_reponse.read_text(encoding="utf-8"))
    if garde_brut is not None:
        garde_brut.parent.mkdir(parents=True, exist_ok=True)
        # le log BRUT de l'API, conservé TEL QUEL (la pièce du dry-run)
        with open(garde_brut, "a", encoding="utf-8") as f:
            f.write(json.dumps({"horodatage": horodatage(),
                                "bras": bras, "phase": phase,
                                "tache": tache,
                                "reponse_api": reponse},
                               ensure_ascii=False) + "\n")
    usage = reponse.get("usage") or {}
    texte = (reponse.get("choices") or [{}])[0].get("message",
                                                    {}).get("content", "")
    # LA LIGNE DE JOURNAL — chaque champ LU, jamais calculé hors la
    # somme arithmétique total = prompt + completion (recoupée : si
    # l'API la contredit, l'écart est NOMMÉ, la ligne le porte)
    ligne = {
        "horodatage": horodatage(),
        "bras": bras, "phase": phase, "tache": tache,
        "id": reponse.get("id", ""), "modele": reponse.get("model", ""),
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
    chemin_reponse.unlink(missing_ok=True)
    journal.parent.mkdir(parents=True, exist_ok=True)
    existe = journal.exists()
    with open(journal, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    if not existe:
        print(f"[compter_tokens] journal CRÉÉ (la première mesure le "
              f"fait naître — CA1) : {journal}", file=sys.stderr)
    return texte, ligne


def total(journal: pathlib.Path) -> None:
    """Le récapitulatif PAR BRAS ET PAR PHASE — lu du journal, rien d'autre."""
    lignes = [json.loads(l) for l in
              journal.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not lignes:
        print("[total] journal vide")
        return
    print(f"[total] {len(lignes)} appel(s) instrumenté(s) — "
          f"100 % lus du log d'usage, zéro estimation")
    clefs: dict[tuple[str, str], list[int]] = {}
    for l in lignes:
        clefs.setdefault((l["bras"], l["phase"]), []).append(
            l["total_tokens"])
    tout = 0
    for (bras, phase), totaux in sorted(clefs.items()):
        p = sum(1 for _ in totaux)
        s = sum(totaux)
        tout += s
        print(f"  {bras:1s} {phase:10s} : {p:3d} appel(s), "
              f"{s:8d} tokens")
    incoherences = [l for l in lignes if not l.get("somme_coherente")]
    print(f"  TOTAL : {tout} tokens")
    if incoherences:
        # v2 — l'annonce cp1252-sûre : « != » au lieu de « ≠ »
        print(f"  [ÉCART NOMMÉ] {len(incoherences)} ligne(s) où "
              f"prompt+completion != total (l'API contredite, la ligne "
              f"porte l'écart)")
    hors_log = [l for l in lignes if l.get("source") != "log-api"]
    if hors_log:
        print(f"  [ÉCART NOMMÉ] {len(hors_log)} ligne(s) HORS log "
              f"— interdit par le plan (CA3), à nommer")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bras", choices=("T", "C"), required=False)
    ap.add_argument("--phase", choices=PHASES, required=False)
    ap.add_argument("--tache", default="")
    ap.add_argument("--prompt-file")
    ap.add_argument("--system-file")
    ap.add_argument("--journal", type=pathlib.Path, default=JOURNAL_DEFAUT)
    ap.add_argument("--garde-brut", type=pathlib.Path, default=None,
                    help="conserver la réponse BRUTE de l'API (le log) à "
                         "côté du journal — la preuve du dry-run")
    ap.add_argument("--total", action="store_true",
                    help="le récapitulatif du journal, rien d'autre")
    args = ap.parse_args()
    if args.total:
        total(args.journal)
        return 0
    manquants = [n for n, v in (("bras", args.bras), ("phase", args.phase),
                                ("prompt-file", args.prompt_file))
                 if not v]
    if manquants:
        ap.error(f"arguments manquants : {manquants} "
                 f"(ou --total pour le récapitulatif)")
    prompt = pathlib.Path(args.prompt_file).read_text(encoding="utf-8")
    system = (pathlib.Path(args.system_file).read_text(encoding="utf-8")
              if args.system_file else None)
    texte, ligne = appeler_et_compter(args.bras, args.phase, args.tache,
                                      prompt, system, args.journal,
                                      args.garde_brut)
    print(texte)
    print(f"[compter_tokens] {ligne['prompt_tokens']}+"
          f"{ligne['completion_tokens']}={ligne['total_tokens']} tokens "
          f"(lus du log) — bras {args.bras}, phase {args.phase}, "
          f"tâche {args.tache}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
