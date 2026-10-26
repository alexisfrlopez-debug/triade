#!/usr/bin/env python3
"""budgets_tokens.py — Instrumentation des budgets tokens (spec 12), jalon M1.

Premiere mesure EFFECTIVE des couts par operation (cibles de conception jusqu'ici) :
la metrique « budgets_tokens » du tableau de bord passe de cible a mesurée.

Operations mesurees (spec 12, table des budgets) — sur les DONNEES REELLES du
projet, jamais sur des exemples fabriqués :

  localiser  la ligne [bloc] de frag-loc d'un bloc (spec 4.3 : premiere ligne =
             localisation, budget 64 tokens — amendé par D31, la mesure M1 ayant
             constaté 43 tokens sur le gabarit canonique v0.4.0 en cl100k_base) —
             moyenne sur les 11 blocs indexés ;
  editer     frag-loc (ligne) + frag-con (entrée du bloc) + notation (.asm) —
             moyenne sur les 9 blocs embarqués (budget 3 000 tokens) ;
  ajouter    empreinte complete du dernier ajout REEL du projet : memset
             (b20007, dev.2) = spécification I (R2 : intention d'abord) +
             notation + entrées carte écrites (frag-loc, frag-con, frag-prf) —
             budget 6 000 tokens. La part « lectures fragment seules » de la
             table de la spec 12 est aussi consignée pour comparaison.

Les entrées de carte sont lues depuis la carte SCELLÉE (déchiffrement via
carte_m1 — discipline R8 : on mesure ce que l'agent lirait réellement) ;
l'échec de déchiffrement est terminal (fail-closed).

Tokenizer de référence : tiktoken cl100k_base (BPE, 100 277 entrées) —
documenté dans budgets.json pour reproductibilité.

Ecrit m1/budgets.json (lu par build_m1.tableau_de_bord).

Usage : python3 budgets_tokens.py   (depuis m1/)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

import tiktoken

import build_m1 as bm
import carte_m1 as cm

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
M0_DIR = os.path.join(RACINE, "m0")

CIBLES = {"localiser": 64, "editer": 3000, "ajouter": 6000}   # localiser amendé D31 (mesure M1)
ENCODAGE = "cl100k_base"


def chemin_notation(fichier: str) -> str:
    if fichier.startswith("hello-"):
        return os.path.join(M0_DIR, "notation", fichier + ".asm")
    return os.path.join(ICI, "notation", fichier + ".asm")


def lire(chemin: str) -> str:
    with open(chemin, encoding="utf-8") as f:
        return f.read()


def extraire_entree(fragment: str, bid: str, multi_lignes: bool) -> str:
    """Entrée [bloc] id=<bid> d'un fragment ; multi_lignes = jusqu'à la suivante."""
    lignes = fragment.splitlines()
    depart = next((k for k, l in enumerate(lignes) if l.startswith(f"[bloc] id={bid}")), None)
    if depart is None:
        raise SystemExit(f"ECHEC : entrée {bid} introuvable dans le fragment")
    if not multi_lignes:
        return lignes[depart]
    prises = [lignes[depart]]
    for l in lignes[depart + 1:]:
        if l.startswith("[") or l.startswith("  run "):
            break
        prises.append(l)
    return "\n".join(prises)


def executer() -> tuple[bool, list[str]]:
    lignes = ["Instrumentation des budgets tokens (spec 12) — jalon M1",
              f"Tokenizer : tiktoken {ENCODAGE} (BPE)"]

    enc = tiktoken.get_encoding(ENCODAGE)
    tok = lambda s: len(enc.encode(s))

    # Carte scellée : déchiffrement des fragments réels (fail-closed)
    try:
        phrase, _ = cm.charger_secrets(interactif=False)
        maitre = cm.cle_maitresse(phrase)
        _, fragments, _, _ = cm.lire_carte()
        frag_loc = cm.dechiffrer_fragment(maitre, "frag-loc", fragments["frag-loc"]).decode("ascii")
        frag_con = cm.dechiffrer_fragment(maitre, "frag-con", fragments["frag-con"]).decode("ascii")
        frag_prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("ascii")
    except (cm.ErreurCarte, FileNotFoundError) as exc:
        print(f"ECHEC (fail-closed) : carte illisible : {exc}", file=sys.stderr)
        return False, [f"ECHEC : carte illisible : {exc}"]
    lignes.append("Carte scellée déchiffrée : entrées réelles mesurées (R8)")

    blocs = [(b[0], b[2]) for b in bm.blocs_phase(2)]      # (id, fichier notation)
    tous_les_ids = [b[0] for b in blocs] + ["a10001"]

    # --- localiser : ligne [bloc] de frag-loc (spec 4.3) -----------------------
    par_bloc_loc = {bid: tok(extraire_entree(frag_loc, bid, multi_lignes=False))
                    for bid in tous_les_ids}
    localiser = round(sum(par_bloc_loc.values()) / len(par_bloc_loc))

    # --- editer : frag-loc + frag-con + notation (spec 12) --------------------
    par_bloc_ed = {}
    for bid, fichier in blocs:
        entree_con = extraire_entree(frag_con, bid, multi_lignes=True)
        par_bloc_ed[bid] = tok(extraire_entree(frag_loc, bid, multi_lignes=False)) \
            + tok(entree_con) + tok(lire(chemin_notation(fichier)))
    editer = round(sum(par_bloc_ed.values()) / len(par_bloc_ed))

    # --- ajouter : empreinte complete du dernier ajout reel (memset, dev.2) ---
    spec = lire(os.path.join(ICI, "I", "libc-07-memset.md"))
    notation = lire(chemin_notation("libc-07-memset"))
    e_loc = extraire_entree(frag_loc, "b20007", multi_lignes=False)
    e_con = extraire_entree(frag_con, "b20007", multi_lignes=True)
    e_prf = extraire_entree(frag_prf, "b20007", multi_lignes=True)
    ajouter = tok(spec) + tok(notation) + tok(e_loc) + tok(e_con) + tok(e_prf)
    lectures_seules = tok(e_loc) + tok(e_con) + tok(e_prf)
    lignes += [
        f"  composition de l'ajout mesuré (memset b20007, dev.2) :",
        f"    spec I = {tok(spec)} tok ; notation = {tok(notation)} tok ; "
        f"carte (loc+con+prf) = {tok(e_loc) + tok(e_con) + tok(e_prf)} tok",
    ]

    # --- verdicts contre les cibles --------------------------------------------
    rapports = {
        "localiser": (localiser, CIBLES["localiser"], par_bloc_loc),
        "editer": (editer, CIBLES["editer"], par_bloc_ed),
        "ajouter": (ajouter, CIBLES["ajouter"], None),
    }
    ok = True
    for operation, (mesure, cible, _) in rapports.items():
        conforme = mesure <= cible
        ok &= conforme
        ecart = cible - mesure
        lignes.append(f"  {operation:10} : {mesure:5} tok (cible {cible:5}) — "
                      f"{'CONFORME' if conforme else 'DEPASSE'} (marge {ecart:+d})")

    # --- budgets.json (lu par le tableau de bord) ------------------------------
    mesure_dict = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tokenizer": f"tiktoken {ENCODAGE} (BPE, {enc.n_vocab} entrees)",
        "source": "carte scellee (frag-loc/frag-con/frag-prf dechiffres) + sources m1/",
        "localiser": {"mesure": localiser, "cible": CIBLES["localiser"],
                      "detail": "ligne [bloc] de frag-loc, moyenne des 11 blocs indexes",
                      "par_bloc": par_bloc_loc},
        "editer": {"mesure": editer, "cible": CIBLES["editer"],
                   "detail": "frag-loc + frag-con + notation, moyenne des 9 blocs embarques",
                   "par_bloc": par_bloc_ed},
        "ajouter": {"mesure": ajouter, "cible": CIBLES["ajouter"],
                    "detail": "empreinte complete de l'ajout memset (dev.2) : spec I + "
                              "notation + entrees carte ecrites",
                    "lectures_fragment_seules": lectures_seules},
    }
    with open(os.path.join(ICI, "budgets.json"), "w", encoding="utf-8") as f:
        json.dump(mesure_dict, f, ensure_ascii=False, indent=2)
    lignes.append(f"  budgets.json écrit (mesures localiser/editer/ajouter)")
    lignes.append(f"Verdict : {'CONFORME aux trois cibles' if ok else 'DEPASSEMENT — voir ci-dessus'}")
    return ok, lignes


if __name__ == "__main__":
    ok, rapport = executer()
    print("\n".join(rapport))
    sys.exit(0 if ok else 1)
