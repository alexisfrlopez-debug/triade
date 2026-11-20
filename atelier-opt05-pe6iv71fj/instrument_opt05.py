#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""instrument_opt05.py — L'INSTRUMENT DE LA CAMPAGNE OPT-05 (le plan § 1.4) :
chaque appel au modèle passe PAR CET OUTIL — le CLI z-ai appelé, la réponse
JSON lue, le champ `usage` JOURNALISÉ (le compte est le LOG, jamais une
estimation, le ×1,08 interdit par construction). La ligne de journal au
format de la rig compter_tokens.py (la campagne cq01qv1za reconduite).

Usage :
  from instrument_opt05 import appeler_et_compter
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ICI = pathlib.Path(__file__).resolve().parent
JOURNAL = ICI / "journal_tokens.jsonl"
GARDE = ICI / "garde-brut.jsonl"


def horodatage() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def appeler_et_compter(bras: str, phase: str, tache: str,
                       prompt: str, system: str | None = None) -> tuple[str, dict]:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False,
                                     encoding="utf-8") as f:
        chemin_reponse = pathlib.Path(f.name)
    cmd = ["z-ai", "chat", "--prompt", prompt, "-o", str(chemin_reponse)]
    if system:
        cmd += ["--system", system]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if proc.returncode != 0:
        chemin_reponse.unlink(missing_ok=True)
        raise RuntimeError(f"l'appel z-ai a échoué : {proc.stderr[:400]}")
    reponse = json.loads(chemin_reponse.read_text(encoding="utf-8"))
    with open(GARDE, "a", encoding="utf-8") as f:
        f.write(json.dumps({"horodatage": horodatage(), "bras": bras,
                            "phase": phase, "tache": tache,
                            "reponse_api": reponse}, ensure_ascii=False) + "\n")
    usage = reponse.get("usage") or {}
    texte = (reponse.get("choices") or [{}])[0].get("message", {}).get("content", "")
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
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return texte, ligne
