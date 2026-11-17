#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesure_localiser.py — LA CAMPAGNE 5gfx6pwkj VÉCUE selon le plan
pré-enregistré (PLAN-5gfx6pwkj.md, sha256 a0ecaf41…, consigné D211 AVANT
toute mesure).

Le geste : pour chaque bloc (l'ordre de la graine 20261117), DEUX appels
instrumentés (compter_tokens.py — le tokenizer natif lu du champ usage) :
  le mode A (l'actuel)  : la réponse rend l'entête complet ;
  le mode B (le minimal): la réponse tient en une ligne ID · NOM · PLAGE.

Chaque prompt exact est conservé au geste (garde-prompts/). La vérification
(zéro divergence : l'identifiant, le nom, la plage exacts — fail-closed) vit
à extraire_gain.py qui lit les logs bruts.

Aucun octet du domaine loupe n'est écrit — lecture seule."""
from __future__ import annotations

import pathlib
import random
import re
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
NOTATIONS = REPO / "loupe" / "notation"
RIG = REPO / "atelier-baseline-20261117" / "rig" / "compter_tokens.py"
GRAINE = 20261117  # consignée au plan § 4

GABARIT_A = (
    "L'OPÉRATION LOCALISER DE LA CARTE TRIADE (le format en vigueur — la réponse\n"
    "rend l'entête complet du bloc localisé).\n"
    "\n"
    "BLOC DE LA CARTE (entête lu du fichier même) :\n"
    "{entete}\n"
    "\n"
    "REQUÊTE : localise le bloc ci-dessus dans la carte et rends SON ENTÊTE\n"
    "COMPLET (toutes les lignes de l'entête du bloc localisé, le format en\n"
    "vigueur de l'opération) — rien d'autre.\n"
)

GABARIT_B = (
    "L'OPÉRATION LOCALISER DE LA CARTE TRIADE (le mode minimal — la réponse tient\n"
    "en une ligne, la carte confronte la réponse aux octets réels).\n"
    "\n"
    "BLOC DE LA CARTE (entête lu du fichier même) :\n"
    "{entete}\n"
    "\n"
    "REQUÊTE : localise le bloc ci-dessus dans la carte et réponds AU FORMAT\n"
    "MINIMAL, une seule ligne exactement :\n"
    "IDENTIFIANT · NOM · PLAGE\n"
    "— IDENTIFIANT : l'identifiant de bloc de la carte (la forme iNNNNNN de\n"
    "l'entête) ;\n"
    "— NOM : le nom du bloc tel que l'entête le porte ;\n"
    "— PLAGE : début–fin du slot en RVA hexadécimal, la fin exclue (la forme\n"
    "0x…–0x…).\n"
    "Rien d'autre.\n"
)


def verite_terrain() -> list[dict]:
    """la table des 18 — RÉGÉNÉRÉE des fichiers mêmes (jamais tapée)."""
    blocs = []
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
        m = re.search(r"slot RVA (0x[0-9a-f]+), taille (\d+) octets", joint)
        slot, taille = int(m.group(1), 16), int(m.group(2))
        nom = f.stem
        # le code (pour la confrontation aux octets réels) : « Code : N o »
        mcode = re.search(r"Code : (\d+) o", joint)
        blocs.append({"nom": nom, "id": bid, "slot": slot, "taille": taille,
                      "fin": slot + taille, "code": int(mcode.group(1)),
                      "entete": joint,
                      "notation_sha256": __import__("hashlib").sha256(
                          f.read_bytes()).hexdigest()})
    return blocs


def main() -> int:
    blocs = verite_terrain()
    assert len(blocs) == 18, f"18 blocs attendus, {len(blocs)} lus"

    # l'ordre de la graine (le plan § 4) — le même aux deux modes
    ids_tries = sorted(b["id"] for b in blocs)
    ordre = list(ids_tries)
    random.Random(GRAINE).shuffle(ordre)
    par_id = {b["id"]: b for b in blocs}
    (ICI / "verites-terrain.json").write_text(
        __import__("json").dumps(
            {"graine": GRAINE, "ordre": ordre,
             "blocs": [{k: v for k, v in b.items() if k != "entete"}
                       for b in sorted(blocs, key=lambda x: x["id"])]},
            ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[verites] 18 blocs régénérés des fichiers — l'ordre de la graine "
          f"{GRAINE} consigné à verites-terrain.json")

    journal = ICI / "journal_tokens.jsonl"
    garde = ICI / "garde-brut.jsonl"
    prompts_dir = ICI / "garde-prompts"
    prompts_dir.mkdir(exist_ok=True)

    # l'ordre des modes : A d'abord (le mode actuel), puis B (le plan § 4)
    for mode, gabarit in (("A", GABARIT_A), ("B", GABARIT_B)):
        for bid in ordre:
            b = par_id[bid]
            tache = f"localiser-{mode}-{bid}"
            prompt = gabarit.format(entete=b["entete"])
            pfile = prompts_dir / f"{tache}.txt"
            pfile.write_text(prompt, encoding="utf-8")
            cmd = ["python3", str(RIG),
                   "--bras", "T", "--phase", "analyse", "--tache", tache,
                   "--prompt-file", str(pfile),
                   "--journal", str(journal),
                   "--garde-brut", str(garde)]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if r.returncode != 0:
                print(f"[{tache}] ÉCHEC INSTRUMENT : {r.stderr[:300]}")
                return 2
            # la ligne née (le stderr du compteur)
            ligne = [l for l in r.stderr.splitlines() if "tokens" in l]
            print(f"[{tache}] {' | '.join(ligne[-1:]) if ligne else 'OK'}")
    print("\n[mesure] 36 appels instrumentés vécus — le journal et la garde "
          "à l'atelier ; l'extraction (extraire_gain.py) juge.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
