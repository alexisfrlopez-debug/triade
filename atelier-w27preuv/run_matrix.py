#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_matrix.sh — la matrice des runs Tamarin du modèle décomposé (W27PREUV).
Chaque sous-lemme est lancé SEUL, borné en temps (600 s) ; le mur mémoire se
voit à l'OOM-kill (exit 137). Empreinte du modèle consignée à chaque run."""
import hashlib
import json
import pathlib
import subprocess
import time

ICI = pathlib.Path(__file__).resolve().parent
MODELE = ICI / "CF3-v3d.spthy"
import os
ENV = dict(os.environ)
ENV["PATH"] = "/home/z/my-project/work/tools/maude-root/usr/bin:/home/z/my-project/work/tools:" + ENV["PATH"]
ENV["LD_LIBRARY_PATH"] = "/home/z/my-project/work/tools/maude-root/usr/lib/x86_64-linux-gnu"
ENV["MAUDE_LIB"] = "/home/z/my-project/work/tools/maude-root/usr/share/maude"
ENV.setdefault("LANG", "C.UTF-8")
LEMmes = [
    ("L3-rejeu", "atelier-cf3-verdict-qa3k5putf/CF3-v3.spthy", "absence_de_destruction_par_corruption"),
    ("NEGATIF-temoin", "atelier-cf3-verdict-qa3k5putf/CF3-v3-negatif.spthy", "temoin_falsification_et_destruction"),
    ("L1a", "CF3-v3d.spthy", "l1a_connaissance_par_reconstitution"),
    ("L1c", "CF3-v3d.spthy", "l1c_reconstitution_exige_trois_parts"),
    ("L2a", "CF3-v3d.spthy", "l2a_chaine_des_phrases_hotes"),
    ("L2b-naissance", "CF3-v3d.spthy", "l2b_emploi_exige_naissance"),
    ("L2-compose-ind", "CF3-v3d.spthy", "l2_compose_induction"),
    ("L2b-premiere-formulation-REFUTEE", "CF3-v3d.spthy", "l2b_refutee_occurrence"),
]
RESULTATS = []
for nom, fichier, lemme in LEMmes:
    chemin = (ICI / pathlib.Path(fichier).name) if "v3d" in fichier else (ICI.parent / fichier)
    t0 = time.time()
    try:
        r = subprocess.run(
            ["tamarin-prover", "--prove", f"--lemma={lemme}", str(chemin)],
            capture_output=True, text=True, timeout=240, env=ENV, cwd=str(ICI.parent))
        duree = round(time.time() - t0, 1)
        verdict = "?"
        for ligne in r.stdout.splitlines():
            if ligne.strip().startswith(lemme + " "):
                verdict = ligne.strip()
        oom = False
        code = r.returncode
    except subprocess.TimeoutExpired:
        duree = round(time.time() - t0, 1)
        verdict = "TIMEOUT (240 s)"
        oom, code = False, 124
    if code == 137 or "Killed" in verdict:
        oom, verdict, code = True, "OOM-KILLED (le mur mémoire 4 Gio)", 137
    RESULTATS.append({"run": nom, "modele": str(chemin), "lemme": lemme,
                      "modele_sha256": hashlib.sha256(chemin.read_bytes()).hexdigest(),
                      "secondes": duree, "code": code, "verdict": verdict})
    print(f"[{nom}] {duree}s code={code} → {verdict[:140]}")

(ICI / "matrix-resultats.json").write_text(json.dumps(RESULTATS, ensure_ascii=False, indent=1), encoding="utf-8")
print("→ matrix-resultats.json")
