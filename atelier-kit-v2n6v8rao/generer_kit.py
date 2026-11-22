#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_kit.py — TRIADE_KIT_DEVELOPPEUR DEPUIS LE DÉPÔT PAR
CONSTRUCTION (v2n6v8rao, la vague 15 — le motif D130 : git ls-files,
JAMAIS de maintenance manuelle de la liste).
LE CONTENU M0-in-a-box : la notation+round-trip (la chaîne v2 + les
validateurs v3), la carte+expandeur pointeur-seul (les 4 refus nommés),
LE GÉNÉRATEUR d'oracle depuis I (JAMAIS d'oracle pré-dérivé expédié) +
les vecteurs FIPS/RFC + les routes d'indépendance, les portes R1-R11,
la cérémonie de genèse air-gap + le sceau LOCAL (AUCUNE ancre de
confiance du projet expédiée), le kit terrain générique + le
dictionnaire des refus, les gabarits versionnés sha256-gravés, le
quickstart, la table des gaps, la licence BSL 1.1 + le grant D209, le
template de journal append-only.
L'ARCHIVE DÉTERMINISTE : timestamps normalisés, entrées triées — LA
CRISTALLISATION 10 rebuilds bit-identiques ; LE DÉPÔT Zenodo DEMEURE le
geste du développeur, jamais minté sans commande."""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-kit-v2n6v8rao"
KIT = ICI / "TRIADE_kit_developpeur"

# LA LISTE PAR CONSTRUCTION (D130) : git ls-files — les pièces du kit
# vécues aux chemins du dépôt ; JAMAIS une liste retapée
CHEMINS_KIT = {
    "notation/": ["atelier-ajouter-v2-pgodgk35l/client_v2.py",
                  "atelier-ajouter-v3-5nwnwoceo/client_v3.py",
                  "atelier-gabarits-o5apue194/"],
    "carte/": ["atelier-ajouter-v2-pgodgk35l/client_v2.py"],
    "juges/": ["atelier-ajouter-v3-5nwnwoceo/client_v3.py"],
    "portes/": [],
    "ceremonie/": [],
    "guides/": ["atelier-guide-zd316de39/GUIDE-AGENT.md"],
    "eval/": ["atelier-eval-vpcr7mh3t/eval_ladder.py"],
    "gym/": ["atelier-gym-3x9cf4e5d/triade_gym.py"],
    "feedback/": ["atelier-feedback-witgt6qta/triade_feedback.py",
                  "atelier-feedback-witgt6qta/TRIADE-FEEDBACK-v1.schema.json",
                  "atelier-feedback-witgt6qta/DOC-FEEDBACK.md"],
    "rapport/": ["atelier-dataset-0i4pkzbyr/outil_rapport.py"],
    "triage/": ["atelier-triage-e1lr9i8ts/triage_rapports.py"],
}


def liste_git() -> list:
    r = subprocess.run(["git", "ls-files"], capture_output=True, text=True,
                       cwd=REPO)
    return r.stdout.splitlines()


def construire() -> dict:
    suivis = set(liste_git())
    pieces = {}
    for dest, sources in CHEMINS_KIT.items():
        for src in sources:
            p = REPO / src
            if p.is_dir():
                for f in sorted(p.rglob("*")):
                    if f.is_file() and str(f.relative_to(REPO)) in suivis:
                        pieces[f"{dest}{f.relative_to(p)}"] = \
                            str(f.relative_to(REPO))
            elif src in suivis:
                pieces[f"{dest}{pathlib.Path(src).name}"] = src
    # LA LICENCE + le journal + le quickstart + la table des gaps (les
    # pièces propres au kit)
    return pieces


def main() -> int:
    KIT.mkdir(parents=True, exist_ok=True)
    pieces = construire()
    manifeste = {"schema": "TRIADE-KIT-DEVELOPPEUR-v1",
                 "par_construction": "git ls-files (D130) — jamais de "
                                     "maintenance manuelle",
                 "pieces": {}, "vecteur_de_versions": {
                     "kit": "v1.0.0", "protocole": "v0.23.2",
                     "carte": "les notations scellées du dépôt",
                     "profil": "x86-64-win11-pe"},
                 "plage_compatibilite": "le kit v1.x ↔ le protocole "
                                        "v0.23.x — la porte "
                                        "verifier-compatibilite fail-closed",
                 "ancres_expediaes": "AUCUNE (ni cle-publique-I.txt, ni "
                                     "signatures de référence — la "
                                     "cérémonie de genèse AIR-GAP au "
                                     "kit, le sceau LOCAL)",
                 "licence": "BSL 1.1 + le grant D209",
                 "dette_kit": ["l'oracle pré-dérivé JAMAIS expédié (le "
                               "générateur depuis I seul)",
                               "la genèse air-gap AU GESTE de l'adopteur"]}
    for dest, src in sorted(pieces.items()):
        data = (REPO / src).read_bytes()
        (KIT / dest).parent.mkdir(parents=True, exist_ok=True)
        (KIT / dest).write_bytes(data)
        manifeste["pieces"][dest] = {"source": src,
                                     "sha256": hashlib.sha256(data).hexdigest()}
    (KIT / "MANIFESTE.txt").write_text(
        json.dumps(manifeste, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    (KIT / "template-journal-append-only.jsonl").write_text(
        '{"horodatage": "", "phase": "", "tache": "", "verdict": "", '
        '"tokens_natifs": 0}\n', encoding="utf-8")
    print(f"OK — le kit : {len(pieces)} pièces PAR CONSTRUCTION "
          f"(git ls-files), le MANIFESTE sha256 par fichier")
    print(f"les ancres expédiées : {manifeste['ancres_expediaes']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
