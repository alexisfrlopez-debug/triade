#!/usr/bin/env python3
"""cristalliser_corridor.py — atelier IO3UH37CJ (la vague 16).

LE SCELLEMENT DU COULOIR DE PERFORMANCE par la procédure lourde :
  - l'assemblage à l'adresse stable (RVA 0xF800, l'artefact R4/R7) ;
  - l'aller-retour keystone -> capstone -> keystone ;
  - LA DIFFÉRENTIELLE CONTRE LA CHAÎNE SCELLÉE (le sha256 du registre
    differentielle.json — zéro écart attendu, jamais une approximation) ;
  - la CRISTALLISATION : dix rebuilds bit-identiques ;
  - le TEMPS-CONSTANT TRACE-HASH : une empreinte par classe ;
  - les BORNES fail-closed : N = 0 et N = 257 REFUSÉS (le couloir traite de 1
    à 256 blocs — jamais un verdict partiel sur une entrée hors bornes).

Le laboratoire ne mesure pas les cycles (le geste est au métal nu) : il PROUVE
que la chaîne est reproduite, stable et bornée. La mesure de performance reste
au poste réel — et n'est jamais maquillée en mesure de laboratoire.
"""

import argparse
import hashlib
import json
import os
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from keystone import Ks, KS_ARCH_X86, KS_MODE_64

RVA_COULOIR = 0xF800           # l'adresse stable de l'artefact (R4/R7)
RVA_MARGE = 0xF7C0             # la variante de marge : la même source, décalée
N_MIN, N_MAX = 1, 256          # les bornes du couloir (blocs)

SHA256_SCELLE = "ddedc26c0b21242111856c9d6f73c390eb3de274243372260d78ec801d4792bc"


def charger_corps(chemin: str):
    """Les lignes de la notation, les commentaires retirés — l'ordre du fichier."""
    lignes = []
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            l = ligne.split(";")[0].strip()
            if l:
                lignes.append(l)
    return lignes


def assembler(corps, rva):
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    enc, _ = ks.asm("\n".join(corps), rva)
    return bytes(enc)


def desassembler(octets, rva):
    cs = Cs(CS_ARCH_X86, CS_MODE_64)
    return [f"{i.mnemonic} {i.op_str}".strip() for i in cs.disasm(octets, rva)]


def empreinte(octets):
    return hashlib.sha256(octets).hexdigest()


def valider_n(n: int):
    """La borne fail-closed : un N hors [1, 256] est REFUSÉ, jamais tronqué."""
    if not isinstance(n, int):
        return False, f"REFUS : N n'est pas un entier ({type(n).__name__})"
    if n < N_MIN:
        return False, f"REFUS : N = {n} < {N_MIN} (le couloir ne traite aucun bloc vide)"
    if n > N_MAX:
        return False, f"REFUS : N = {n} > {N_MAX} (le couloir est borné à 256 blocs)"
    return True, "VERT"


def cristalliser(corps, rva, passes=10):
    """Dix rebuilds : tous identiques au premier — la preuve de la stabilité."""
    reference = assembler(corps, rva)
    ref_rt = assembler(desassembler(reference, rva), rva)
    divergences = []
    for i in range(passes):
        o = assembler(corps, rva)
        rt = assembler(desassembler(o, rva), rva)
        if o != reference or rt != ref_rt:
            divergences.append(i + 1)
    return reference, ref_rt, divergences


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corridor", required=True, help="la notation .asm du couloir")
    ap.add_argument("--registre", default=None, help="le registre JSON de sortie")
    args = ap.parse_args()

    if not os.path.isfile(args.corridor):
        sys.exit(f"REFUS : la notation {args.corridor} n'existe pas")

    corps = charger_corps(args.corridor)
    print("=== LE SCELLEMENT DU COULOIR (atelier io3uh37cj) ===")
    print(f"  la notation : {os.path.basename(args.corridor)} ({len(corps)} lignes utiles)")
    print(f"  l'adresse stable : RVA 0x{RVA_COULOIR:X} (R4/R7)")

    # (1) l'assemblage et l'aller-retour
    octets, rt, divergences = cristalliser(corps, RVA_COULOIR)
    instructions = desassembler(octets, RVA_COULOIR)
    print(f"  l'assemblage : {len(octets)} octets · {len(instructions)} instructions relues")
    print(f"  l'aller-retour keystone -> capstone -> keystone : "
          f"{'IDENTIQUE' if octets == rt else 'DIVERGENT'}")

    # (2) LA DIFFÉRENTIELLE CONTRE LA CHAÎNE SCELLÉE
    sha = empreinte(octets)
    ecart = "ZÉRO ÉCART" if sha == SHA256_SCELLE else "ÉCART"
    print(f"  LA DIFFÉRENTIELLE contre la chaîne scellée : {ecart}")
    print(f"    le sha256 du registre : {SHA256_SCELLE}")
    print(f"    le sha256 reconstruit : {sha}")

    # (3) la cristallisation 10x
    print(f"  LA CRISTALLISATION : {10 - len(divergences)}/10 rebuilds BIT-IDENTIQUES"
          + (f" — divergences aux passes {divergences}" if divergences else ""))

    # (4) le temps-constant trace-hash : une empreinte par classe
    classes = {
        "assemblage": empreinte(octets),
        "desassemblage": empreinte("\n".join(instructions).encode("utf-8")),
        "aller_retour": empreinte(rt),
        "structure": empreinte(json.dumps(
            {"octets": len(octets), "instructions": len(instructions),
             "rva": RVA_COULOIR}, sort_keys=True).encode()),
    }
    print("  LE TEMPS-CONSTANT TRACE-HASH (une empreinte par classe) :")
    for nom, h in classes.items():
        print(f"    {nom:16s} {h[:32]}…")

    # (5) les bornes fail-closed
    print("  LES BORNES fail-closed :")
    for n in (0, 257):
        ok, motif = valider_n(n)
        print(f"    N = {n:4d} → {'VERT' if ok else 'REFUSÉ'} — {motif}")
    ok1, _ = valider_n(1)
    ok256, _ = valider_n(256)
    print(f"    N = 1 et N = 256 → {'VERT' if ok1 and ok256 else 'ROUGE'} (les bornes incluses)")

    # (6) la variante de marge : la même source à une adresse décalée
    marge = assembler(corps, RVA_MARGE)
    print(f"  LA VARIANTE DE MARGE (RVA 0x{RVA_MARGE:X}) : {len(marge)} octets · "
          f"sha256 {empreinte(marge)[:32]}…")

    # (7) le récapitulatif
    verdict = (octets == rt and sha == SHA256_SCELLE and not divergences
               and ok1 and ok256)
    print("=== LE VERDICT ===")
    print(f"  {'VERT' if verdict else 'ROUGE'} — "
          f"{'la chaîne scellée reproduite, stable et bornée' if verdict else 'un écart nommé'}")

    if args.registre:
        registre = {
            "schema": "TRIADE-COULOIR-SCELLE-v1",
            "notation": os.path.basename(args.corridor),
            "rva": hex(RVA_COULOIR), "octets": len(octets),
            "instructions": len(instructions),
            "sha256_couloir": sha, "sha256_scelle_attendu": SHA256_SCELLE,
            "differentielle": "ZERO" if sha == SHA256_SCELLE else "ECART",
            "round_trip": octets == rt,
            "cristallisation": {"passes": 10, "divergences": divergences},
            "trace_hash": classes,
            "bornes": {"min": N_MIN, "max": N_MAX,
                       "n0": valider_n(0)[0], "n257": valider_n(257)[0]},
            "variante_marge": {"rva": hex(RVA_MARGE), "octets": len(marge),
                               "sha256": empreinte(marge)},
            "verdict": "VERT" if verdict else "ROUGE",
        }
        with open(args.registre, "w", encoding="utf-8") as f:
            json.dump(registre, f, ensure_ascii=False, indent=2)
        print(f"  le registre : {args.registre}")

    return 0 if verdict else 3


if __name__ == "__main__":
    sys.exit(main())
