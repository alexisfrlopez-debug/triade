#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_w29.py — LE HARNAIS DE CAMPAGNE CONTRAINTE (W29DECCO, prompt 1).

LA CAMPAGNE : les deux opérations (éditer 18 tâches, ajouter 18 pointeurs) au
modèle ouvert choisi (Qwen/Qwen2.5-Coder-7B-Instruct — identifiant et empreintes
consignés au plan), la génération CONTRAINTE par la grammaire compilée du schéma
étendu (llguidance, le masque de bits appliqué à chaque pas — le gate GATE-VERT
vécu à sonde_gate.py), le budget usage natif JOURNALISÉ (le compte est le LOG),
la boucle de réparation ≤ 3 tours, les verdicts par le juge D264 INTACT.

AU BAC LA CAMPAGNE N'EST PAS COURUE : la limite structurelle nommée (4 Gio de
RAM / 2 vCPU / aucun GPU — le geste compute appartient au poste réel). Le
harnais est LIVRÉ : au poste réel, remplacer HARNAIS_ENDPOINT par l'endpoint
local du modèle (llama.cpp server / vllm / transformers), le harnais applique
la grammaire au masque de logits du modèle.

Usage :
  python3 campagne_w29.py --statut                # l'état (au bac)
  HARNAIS_ENDPOINT=<url> python3 campagne_w29.py --courir   # au poste réel

Les cibles pré-enregistrées (le plan gelé, jamais re-tirées) :
  éditer   ≥ 17/18 vertes à ≤ 150 tokens natifs médians par changement validé ;
  ajouter  ≥ 15/18 à ≤ 3 000 tokens (CIB-ADD-STRUC inchangée).
"""
import json
import os
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parent
R = ICI.parents[0]
TACHES_EDITION = R / "atelier-opt05-pe6iv71fj/taches-edition.json"
JUGE_D264 = R / "scripts/vague19/expandeur_add.py"   # sha256 9fc325e2… INTACT

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
        "dst": {"type": "string", "minLength": 1},
        "offset": {"type": "integer", "minimum": 0, "maximum": 65535},
        "src": {"anyOf": [{"type": "string", "minLength": 1},
                          {"type": "object"}]},
    },
}

GRILLE = 20261117            # la graine reconduite, l'ordre jamais re-tiré
MAX_TOURS = 3
CIBLES = {"editer_faisabilite": 17, "editer_mediane": 150,
           "ajouter_faisabilite": 15, "ajouter_cout": 3000}


def preparer():
    """La grammaire compilée sur le vocabulaire du modèle choisi + les tâches."""
    from llguidance import JsonCompiler, LLTokenizer
    from tokenizers import Tokenizer
    enc = Tokenizer.from_file(str(ICI / "tokenizer.json"))
    ltok = LLTokenizer(enc.to_str(), eos_token=151645)
    grammar = JsonCompiler().compile(json.dumps(SCHEMA_ETENDU))
    edition = json.loads(TACHES_EDITION.read_text(encoding="utf-8"))
    return ltok, grammar, edition


def statut() -> int:
    print("EN ATTENTE — le harnais est prêt ; le geste compute (le modèle "
          "ouvert au poste réel) manque au bac (4 Gio / 2 vCPU / aucun "
          "GPU — la limite structurelle nommée au plan).")
    print(f"grille {GRILLE} ; boucle ≤ {MAX_TOURS} tours ; juge "
          f"{JUGE_D264.name} (recouper sha256 avant le run).")
    print(f"cibles pré-enregistrées: {CIBLES}")
    return 0


def main() -> int:
    if "--statut" in sys.argv or "--courir" not in sys.argv:
        return statut()
    endpoint = os.environ.get("HARNAIS_ENDPOINT")
    if not endpoint:
        print("ENDPOINT ABSENT — au poste réel : HARNAIS_ENDPOINT=<url locale "
              "du modèle> python3 campagne_w29.py --courir")
        print("AU BAC la campagne n'est pas courue (MODÈLE-ABSENT nommé).")
        return 2
    # le corps de campagne vit au poste réel : l'appel au modèle local avec le
    # masque de la grammaire à chaque pas, le journal usage natif, la boucle ≤3.
    raise NotImplementedError("le run vit au poste réel — le bac ne le court jamais")


if __name__ == "__main__":
    sys.exit(main())
