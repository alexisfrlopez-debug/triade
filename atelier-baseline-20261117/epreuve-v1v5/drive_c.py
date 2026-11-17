#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""drive_c.py — LE PILOTE DE L'ÉPREUVE DU BRAS C : génère les gammes (la
MÊME graine que le harnais T — 20261117), compile la pièce contre le shim
du labo + le harnais, exécute, et JUGE chaque condensé contre
hashlib.sha256 (la référence externe — jamais les fonctions de la pièce).
Assemble epreuve-v1v5-bras-C.json au format du bras T."""
from __future__ import annotations

import hashlib
import json
import os
import random
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
ATELIER = os.path.dirname(ICI)
REPO_TLS13 = "/home/z/my-project/triade/tls13"
GRAINE = 20261117


def main():
    proxy = open(os.path.join(REPO_TLS13, "proxy.exe"), "rb").read()
    assert hashlib.sha256(proxy).hexdigest().startswith("446279f3")
    temoin_bi = proxy + proxy
    rng = random.Random(GRAINE)
    lignes = ["0 %d" % len(proxy)]
    for _ in range(1000):
        off = rng.randint(0, len(proxy))
        lon = rng.randint(0, len(proxy) - off)
        lignes.append(f"{off} {lon}")
    lignes.append("-1 -1")
    for _ in range(100):
        off = rng.randint(0, len(temoin_bi) - 65537)
        lon = rng.randint(65537, len(temoin_bi) - off)
        lignes.append(f"{off} {lon}")
    gammes_txt = os.path.join(ICI, "gammes.txt")
    open(gammes_txt, "w").write("\n".join(lignes) + "\n")

    # la compilation : la pièce + le harnais contre le shim du labo
    binaire = os.path.join(ICI, "harnais_c")
    cmd = ["gcc", "-O2", "-std=c11", "-Wall", "-Wextra",
           "-I", os.path.join(ATELIER, "lab", "shim"),
           os.path.join(ICI, "harnais_c.c"), "-o", binaire]
    comp = subprocess.run(cmd, capture_output=True, text=True)
    if comp.returncode != 0:
        print("ÉCHEC COMPILATION:\n", comp.stderr)
        sys.exit(2)
    if comp.stderr.strip():
        print("avertissements gcc (inattendus — la pièce devait être propre) :",
              comp.stderr[:500])

    run = subprocess.run([binaire, os.path.join(REPO_TLS13, "proxy.exe"),
                          gammes_txt], capture_output=True, text=True, timeout=300)
    if run.returncode != 0:
        print("ÉCHEC EXÉCUTION:", run.stderr[:500])
        sys.exit(2)

    # le jugement : hashlib contre chaque condensé produit
    verdicts = {"bras": "C", "graine": GRAINE, "vecteurs": {}}
    lignes_v1 = []
    crashs = divergents = 0
    echantillon = []
    v2_vide = v2_abc = None
    v3 = v4 = v5 = None
    for l in run.stdout.splitlines():
        p = l.split()
        if l.startswith("V1D "):
            multi, off, lon, rax = int(p[1]), int(p[2]), int(p[3]), int(p[4])
            produit = p[5]
            src = temoin_bi if multi else proxy
            attendu = hashlib.sha256(src[off:off + lon]).hexdigest()
            if rax != 0 or produit != attendu:
                divergents += 1
                if len(echantillon) < 6:
                    echantillon.append({"cas": f"{'multi' if multi else 'proxy'}",
                                        "gamme": [off, lon], "rax": rax,
                                        "produit": produit[:16] + "…",
                                        "attendu": attendu[:16] + "…"})
            lignes_v1.append(1)
        elif l.startswith("V1 "):
            n = int(p[1])
        elif l.startswith("V2 vide"):
            v2_vide = {"produit": p[2], "rax0": p[3] == "1",
                       "attendu": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                       "ok": p[2] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" and p[3] == "1"}
        elif l.startswith("V2 abc"):
            v2_abc = {"produit": p[2], "rax0": p[3] == "1",
                      "attendu": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
                      "ok": p[2] == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" and p[3] == "1"}
        elif l.startswith("V3 "):
            v3 = {"E1_session": {"rax": int(p[1]), "attendu": -4, "ok": int(p[1]) == -4},
                  "E2_bornes": {"rax": int(p[2]), "attendu": -3, "ok": int(p[2]) == -3},
                  "E3_entree": {"rax": int(p[3]), "attendu": -5, "ok": int(p[3]) == -5},
                  "verdict": "VERT" if p[4] == "1" else "ROUGE"}
        elif l.startswith("V4 "):
            v4 = {"rax": int(p[1]), "attendu": -6, "ok_verdict": int(p[1]) == -6,
                  "sortie_intacte": p[2] == "1", "ok_sortie": p[2] == "1",
                  "fenetres": int(p[3]), "code_consigne": int(p[4]),
                  "verdict": "VERT" if (int(p[1]) == -6 and p[2] == "1") else "ROUGE"}
        elif l.startswith("V5 "):
            v5 = {"produit_ref": p[1], "produit_mute": p[2],
                  "divergence": p[3] == "1", "attendu": True,
                  "verdict": "VERT" if p[3] == "1" else "ROUGE"}

    n = len(lignes_v1)
    verdicts["vecteurs"]["V1"] = {
        "n": n, "crashs": 0, "divergents": divergents, "echantillon": echantillon,
        "verdict": "ROUGE" if divergents else "VERT",
        "detail": (f"{divergents} condensés divergents sur {n} gammes"
                   if divergents else "égalité octet par octet partout "
                   "(jugée par hashlib, jamais par les fonctions de la pièce)")}
    v2 = {"vide": v2_vide, "abc": v2_abc,
          "verdict": "VERT" if (v2_vide["ok"] and v2_abc["ok"]) else "ROUGE"}
    verdicts["vecteurs"]["V2"] = v2
    verdicts["vecteurs"]["V3"] = v3
    verdicts["vecteurs"]["V4"] = v4
    verdicts["vecteurs"]["V5"] = v5
    verdicts["VERDICT"] = ("CONFORME" if all(
        v["verdict"] == "VERT" for v in verdicts["vecteurs"].values()) else "REJET")

    sortie = os.path.join(ATELIER, "preuves-baseline", "epreuve-v1v5-bras-C.json")
    json.dump(verdicts, open(sortie, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(json.dumps(verdicts, ensure_ascii=False, indent=1))
    print("\nécrit:", sortie)


if __name__ == "__main__":
    main()
