#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""campagne_opt05.py — LA CAMPAGNE OPT-05 (le plan § 1.3-1.4, gelé) :
éditer et ajouter, aux DEUX modes (AVANT = la notation complète ;
HUNK = les hunks ciblés), les 18 blocs du domaine loupe à l'ordre de la
graine 20261117, le tokenizer natif lu du champ usage, n=18 par cellule
(72 appels instrumentés), les distributions complètes.

La reprise est IDempotente : chaque appel journalisé n'est jamais
re-vécu (le journal fait foi)."""
from __future__ import annotations

import json
import pathlib
import sys
import time

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
sys.path.insert(0, str(ICI))

from instrument_opt05 import appeler_et_compter  # noqa: E402
from client_hunks import round_trip, extraire_notation  # noqa: E402
from client_hunks_v2 import traiter as traiter_v2, Refus  # noqa: E402

VT = REPO / "atelier-localiser-5gfx6pwkj" / "verites-terrain.json"
TACHES = ICI / "taches-edition.json"
CONVENTIONS = (
    "LES CONVENTIONS DE NOTATION DU DOMAINE :\n"
    "- la feuille pure : arguments seuls, aucune entrée IAT, aucun état détenu ;\n"
    "- ABI msx64 : rcx, rdx, r8, r9 puis la pile ; les non-volatils (rbx, r12-r15)\n"
    "  sauvegardés par le bloc ; le cadre aligné à 16 ; l'appelant réserve le\n"
    "  shadow space de 32 octets ;\n"
    "- la notation x86-64 : une instruction par ligne, mnémonique puis opérandes ;\n"
    "  les sauts aux cibles absolues (0x…), les appels aux adresses du plan ;\n"
    "  les commentaires préfixés « ; » ; l'en-tête commenté du bloc porte son\n"
    "  identité (nom, spec, slot, taille, étiquettes résolues, appels directs).\n"
)

# LE GABARIT DE FAMILLE — la source unique (au prompt ET à l'application)
GABARIT_BASE = (
    "push rbx\npush r12\npush r13\npush r14\npush r15\nsub rsp, 0x20\n"
    "; --- LE CORPS DU BLOC ICI ---\n"
    "add rsp, 0x20\npop r15\npop r14\npop r13\npop r12\npop rbx\nret\n"
)
GABARIT = "LE GABARIT DE FAMILLE (la base — le squelette de la feuille pure du\ndomaine, TOUTES les lignes comptent) :\n" + GABARIT_BASE

# LE FORMAT v2 (l'amendement FORMAT-V2-AMENDEMENT.md : la sémantique
# d'ancre explicite, la numérotation sans total, UN EXEMPLE COMPLET)
FORMAT_HUNK = (
    "LE FORMAT DE RÉPONSE HUNK (obligatoire, fail-closed — le client applique,\n"
    "reconstruit et confronte par round-trip exact ; quatre refus nommés :\n"
    "HORS-FORMAT, HUNK-INCONNU, CONTEXTE-DIVERGENT, ROUND-TRIP-DIVERGENT).\n"
    "LA GRAMMAIRE :\n"
    "@@ hunk <k>          (k = 1, 2, 3… le rang du hunk, en ordre)\n"
    "base: <UNE ligne exacte du texte courant — LE PREMIER POINT DU CHANGEMENT>\n"
    "- <une ligne retirée à partir de l'ancre>   [0 ou plus]\n"
    "+ <une ligne insérée au même point>         [1 ou plus]\n"
    "… (les hunks suivent, chacun commence par « @@ hunk k »)\n"
    "FIN-HUNKS\n"
    "LA SÉMANTIQUE DE L'ANCRE : l'ancre est la ligne OÙ LE CHANGEMENT SE PRODUIT.\n"
    "Si le hunk retire des lignes, la PREMIÈRE ligne « - » EST L'ANCRE ELLE-MÊME\n"
    "(la ligne remplacée, répétée) et les retraits suivent dans l'ordre À PARTIR\n"
    "DE L'ANCRE — elles sont remplacées par les lignes « + ». Si le hunk ne\n"
    "retire RIEN, l'ancre est la ligne APRÈS laquelle l'insertion se fait.\n"
    "UN EXEMPLE COMPLET (remplacer « mov eax, 5 » par « mov eax, 6 » puis\n"
    "insérer « nop » après « pop rbx ») :\n"
    "@@ hunk 1\n"
    "base: mov eax, 5\n"
    "- mov eax, 5\n"
    "+ mov eax, 6\n"
    "@@ hunk 2\n"
    "base: pop rbx\n"
    "+ nop\n"
    "FIN-HUNKS\n"
    "RIEN d'autre dans la réponse — aucun texte hors hunks, aucune politesse,\n"
    "la dernière ligne est exactement « FIN-HUNKS ».\n"
)


def gabarit_editer_avant(notation: str, consigne: str) -> str:
    return (
        "L'OPÉRATION ÉDITER DE LA CARTE TRIADE (le format en vigueur — la\n"
        "réponse rend la notation complète du bloc révisé).\n\n"
        f"LA NOTATION COURANTE DU BLOC (lue du fichier même) :\n{notation}\n\n"
        f"LA RÉVISION (la spécification de couche I, la consigne) :\n{consigne}\n\n"
        "REQUÊTE : applique la révision et rends LA NOTATION COMPLÈTE RÉVISÉE\n"
        "du bloc — l'en-tête commenté puis tout le code, rien d'autre. AUCUNE\n"
        "autre ligne de code ne change : les adresses, les étiquettes et les\n"
        "instructions non concernées demeurent octet pour octet.\n"
    )


def gabarit_editer_hunk(notation: str, consigne: str) -> str:
    return (
        "L'OPÉRATION ÉDITER DE LA CARTE TRIADE (le mode HUNKS — la réponse ne\n"
        "rend QUE les hunks ciblés, le client applique et confronte).\n\n"
        f"LA NOTATION COURANTE DU BLOC (la base, lue du fichier même) :\n{notation}\n\n"
        f"LA RÉVISION (la spécification de couche I, la consigne) :\n{consigne}\n\n"
        f"{FORMAT_HUNK}\n"
        "REQUÊTE : applique la révision et rends UNIQUEMENT les hunks au format\n"
        "ci-dessus — la dernière ligne exactement « FIN-HUNKS ».\n"
    )


def gabarit_ajouter_avant(contrat: str, exemple: str) -> str:
    return (
        "L'OPÉRATION AJOUTER DE LA CARTE TRIADE (le format en vigueur — l'unité\n"
        "nouvelle s'écrit de sa spécification, la notation complète).\n\n"
        f"LE CONTRAT DE COUCHE I (mot pour mot) :\n{contrat}\n\n"
        f"{CONVENTIONS}\n"
        "L'EXEMPLE DU FORMAT DE NOTATION (loupe-13, la notation RÉELLE du\n"
        "domaine — le format à suivre EXACTEMENT : l'en-tête commenté, les\n"
        "adresses absolues, AUCUNE directive NASM, AUCUN label à deux-points,\n"
        "les appels aux adresses du plan) :\n"
        f"{exemple}\n\n"
        "REQUÊTE : écris LA NOTATION COMPLÈTE du bloc qui honore le contrat —\n"
        "au format EXACT de l'exemple ci-dessus (l'en-tête commenté puis le\n"
        "code : une instruction par ligne, les sauts aux cibles absolues,\n"
        "AUCUNE directive, AUCUN label) — rien d'autre.\n"
    )


def gabarit_ajouter_hunk(contrat: str, exemple: str) -> str:
    return (
        "L'OPÉRATION AJOUTER DE LA CARTE TRIADE (le mode HUNKS — l'unité se\n"
        "compose PAR HÉRITAGE du gabarit de famille : la réponse ne rend QUE\n"
        "les hunks, le client les applique au gabarit et confronte).\n\n"
        f"LE CONTRAT DE COUCHE I (mot pour mot) :\n{contrat}\n\n"
        f"{CONVENTIONS}\n"
        "L'EXEMPLE DU FORMAT DE NOTATION (loupe-13, la notation RÉELLE du\n"
        "domaine — le format des lignes « + » de tes hunks) :\n"
        f"{exemple}\n\n"
        f"{GABARIT}\n"
        f"{FORMAT_HUNK}\n"
        "REQUÊTE : compose le bloc et rends UNIQUEMENT les hunks qui insèrent\n"
        "le corps (les gardes des pré-conditions, la logique du post-condition,\n"
        "les étiquettes résolues) dans le gabarit — les lignes du gabarit non\n"
        "concernées demeurent ; la dernière ligne exactement « FIN-HUNKS ».\n"
    )


def charger():
    vt = json.loads(VT.read_text(encoding="utf-8"))
    taches = {t["bloc"]: t for t in json.loads(TACHES.read_text(encoding="utf-8"))}
    return vt, taches


def deja_faits() -> set:
    j = ICI / "journal_tokens.jsonl"
    faits = set()
    if j.exists():
        for l in j.read_text(encoding="utf-8").splitlines():
            if l.strip():
                faits.add(json.loads(l)["tache"])
    return faits


def code_de(notation: str) -> list:
    return [l.strip() for l in notation.split("\n")
            if l.strip() and not l.strip().startswith(";")]


def exemple_pour(nom: str) -> str:
    """L'EXEMPLE DU FORMAT pour la tâche « nom » — TOUJOURS un bloc
    FRÈRE, jamais la tâche elle-même (loupe-13 reçoit loupe-14, les
    autres reçoivent loupe-13 — le mapping gelé à l'amendement)."""
    source = "loupe-14-suivant" if nom == "loupe-13-recherche" else "loupe-13-recherche"
    return (REPO / "loupe/notation" / f"{source}.asm").read_text(encoding="utf-8")


def main() -> int:
    vt, taches = charger()
    faits = deja_faits()
    ordre = vt["ordre"]
    par_id = {b["id"]: b for b in vt["blocs"]}
    resultats = ICI / "resultats_opt05.jsonl"

    cellules = [
        ("editer-H2", lambda nom: gabarit_editer_hunk(
            (REPO / "loupe/notation" / f"{nom}.asm").read_text(encoding="utf-8"),
            taches[nom]["consigne"])),
        ("ajouter-A2", lambda nom: gabarit_ajouter_avant(
            (REPO / "loupe/I" / f"{nom}.md").read_text(encoding="utf-8"),
            exemple_pour(nom))),
        ("ajouter-H2", lambda nom: gabarit_ajouter_hunk(
            (REPO / "loupe/I" / f"{nom}.md").read_text(encoding="utf-8"),
            exemple_pour(nom))),
    ]

    for mode, fabrique in cellules:
        manquants = [bid for bid in ordre if f"{mode}-{bid}" not in faits]
        print(f"[{mode}] {len(manquants)} appel(s) à vivre "
              f"(l'ordre de la graine {vt['graine']})", flush=True)
        for bid in manquants:
            nom = par_id[bid]["nom"]
            prompt = fabrique(nom)
            tache = f"{mode}-{bid}"
            try:
                texte, ligne = appeler_et_compter("T", "analyse", tache, prompt)
            except Exception as e:
                print(f"  ÉCHEC API {tache}: {e}", flush=True)
                time.sleep(20)
                continue
            verdict = ""
            try:
                if mode == "editer-A":
                    ok, detail = round_trip(extraire_notation(texte))
                    verdict = "ROUND-TRIP:OK" if ok else f"ROUND-TRIP-DIVERGENT:{detail[:80]}"
                elif mode == "editer-H2":
                    base = (REPO / "loupe/notation" / f"{nom}.asm").read_text(encoding="utf-8")
                    reconstruit, detail = traiter_v2(base, texte)
                    verdict = f"APPLIQUE+ROUND-TRIP:OK ({detail[:40]})"
                elif mode == "ajouter-A2":
                    ok, detail = round_trip(extraire_notation(texte))
                    verdict = "ROUND-TRIP:OK" if ok else f"ROUND-TRIP-DIVERGENT:{detail[:80]}"
                elif mode == "ajouter-H2":
                    reconstruit, detail = traiter_v2(GABARIT_BASE, texte)
                    verdict = f"APPLIQUE+ROUND-TRIP:OK ({detail[:40]})"
            except Refus as e:
                verdict = f"REFUS {e.nom}: {e.detail[:80]}"
            except Exception as e:
                verdict = f"ERREUR: {str(e)[:80]}"
            with open(resultats, "a", encoding="utf-8") as f:
                f.write(json.dumps({"tache": tache, "mode": mode, "bloc": nom,
                                    "verdict": verdict,
                                    "sha256_echange": ligne["sha256_echange"]},
                                   ensure_ascii=False) + "\n")
            print(f"  {tache}: {ligne['total_tokens']} tokens — {verdict[:90]}", flush=True)
            faits.add(tache)
            time.sleep(6)
    print("LA CAMPAGNE OPT-05 : les quatre cellules visitées.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
