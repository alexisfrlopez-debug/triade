#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mutation_vague3.py — LA CAMPAGNE DE MUTATION ÉTENDUE (l'instruction
n4kwcs3wa de la vague 3 : « Étends la campagne de mutation des 52 blocs
scellés (copies de laboratoire uniquement) : ≥200 mutants par bloc avec
graine consignée, incluant mutations multi-octets, substitutions
d'opérateurs et de conditions, altérations d'offsets et de constantes ;
applique les tueurs en ordre de coût (round-trip, structurel,
différentiel, composition). Classe chaque survivant : mutant équivalent
(preuve d'équivalence argumentée) ou chemin non couvert (nommer le
chemin et le contrôle manquant) »).

LES QUATRE TYPES DE MUTATION (la graine 20261112, chaque mutant tiré de
Random("GRAIN:bloc:index") — reproductible à l'identique, par mutant) :
  A — OCTET SIMPLE (l'héritage v0.11.0) : un octet au hasard d'une
      instruction au hasard, une valeur différente ;
  B — MULTI-OCTETS : 2 à 4 octets CONSÉCUTIFS altérés (un dword, un
      mot, un couple immédiat) ;
  C — OPÉRATEUR/CONDITION : la substitution de l'opérateur À LONGUEUR
      CONSERVÉE — la paire ré-assemblée par keystone (jz↔jnz, add↔sub,
      and↔or, shl↔shr, inc↔dec, test↔cmp…), splice SI la longueur
      tient (sinon le mutant est rejeté au tirage suivant) ;
  D — OFFSET/CONSTANTE : l'altération de l'IMMÉDIAT ou du DÉPLACEMENT
      (rip+X) d'une instruction qui en porte — la valeur modifiée
      (±1, bit inversé, complément), ré-assemblage à longueur conservée.

LES TUEURS EN ORDRE DE COÛT (jamais affaiblis) :
  K1 ROUND-TRIP (capstone→keystone, l'identité d'encodage) ;
  K2 STRUCTUREL (mnémoniques + cibles d'appel + feuilles IAT + déplacements
      RIP — la signature du plan) ;
  K3 DIFFÉRENTIEL (les harnais de famille : sha/hkdf/x25519/aead aux
      vecteurs officiels croisés à hashlib/hmac, loupe-06 à md5) ;
  K4 COMPOSITION (le rejeu v0.14.0 réutilisé TEL QUEL : la boucle winmain
      complète pour loupe, la poignée + l'enregistrement pour
      l'orchestration tls13, le harnais sys autonome).

LA CLASSIFICATION DES SURVIVANTS (chacun porte sa classe et sa pièce) :
  ÉQUIVALENT (preuve mécanique) : le décodage COMPLET du bloc mutant est
      IDENTIQUE instruction par instruction (mnémonique ET opérandes) au
      bloc de référence — l'octet muté ne change QUE l'encodage de la
      MÊME sémantique (préfixe REX inerte, encodage alternatif) : la
      preuve d'équivalence est le décodage lui-même ;
  CHEMIN NON COUVERT (le défaut nommé) : la mutation vit dans
      [l'instruction, le champ] et le scénario [winmain / poignée+enreg /
      famille / sys] NE LA DISTINGUE PAS — le contrôle manquant est nommé
      (le vecteur qui exercerait la valeur/l'opération mutée).

LA FRONTIÈRE : les 52 blocs sont ASSEMBLÉS DEPUIS LES NOTATIONS (des
copies de laboratoire — les pièces scellées loupe.exe/proxy.exe JAMAIS
touchées : les sha256 avant/après sont contrôlés par le vérificateur).

Sorties (scripts/preuves_v150/mutation_vague3/) : verdicts.csv (une
ligne par mutant), survivants.csv (classés), taux.csv (par domaine, IC
Clopper-Pearson 95 % exacts), rapport.txt. Usage : --debut/--fin (les
blocs en tranches), --replay (le rejeu à graine identique).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import pathlib
import random
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
SORTIES = REPO / "scripts" / "preuves_v150" / "mutation_vague3"
SORTIES.mkdir(parents=True, exist_ok=True)

GRAINE = 20261112     # LA GRAINE CONSIGNÉE de la campagne étendue
MUTANTS_PAR_BLOC = 200


def charger(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


MUT = charger("mutation_v110_vague3", REPO / "scripts" / "mutation_v110.py")
R140 = charger("rejeu_v140_vague3", REPO / "scripts" / "rejeu_survivants_v140.py")

# ---------------------------------------------------------------------------
# LA GÉNÉRATION — les quatre types
# ---------------------------------------------------------------------------

# les paires d'opérateurs/conditions (la substitution C)
PAIRES = [
    ("jz", "jnz"), ("jnz", "jz"), ("je", "jne"), ("jne", "je"),
    ("jc", "jnc"), ("jnc", "jc"), ("ja", "jbe"), ("jbe", "ja"),
    ("jae", "jb"), ("jb", "jae"), ("jg", "jle"), ("jle", "jg"),
    ("jge", "jl"), ("jl", "jge"), ("js", "jns"), ("jns", "js"),
    ("add", "sub"), ("sub", "add"), ("and", "or"), ("or", "and"),
    ("shl", "shr"), ("shr", "shl"), ("inc", "dec"), ("dec", "inc"),
    ("test", "cmp"), ("cmp", "test"), ("mov", "lea"), ("lea", "mov"),
    ("xor", "or"), ("imul", "mul"),
]


def generer_mutant(octets: bytes, ref_insns, rng) -> tuple[bytes, str, str]:
    """Retourne (mutant, type, détail). Les types C/D préservent la
    longueur par construction (splice seulement si keystone rend la même
    taille) ; A/B mutent des octets en place."""
    for _essai in range(12):   # jusqu'à 12 tirages pour trouver un mutant
        type_ = rng.choices(["A", "B", "C", "D"],
                            weights=[35, 25, 20, 20], k=1)[0]
        if type_ in ("A", "B"):
            insn = ref_insns[rng.randrange(len(ref_insns))]
            pos = insn.address - ref_insns[0].address \
                + rng.randrange(insn.size)
            if type_ == "A":
                val = octets[pos]
                nouvelle = rng.choice(
                    [b for b in range(256) if b != val])
                m = bytearray(octets)
                m[pos] = nouvelle
                return (bytes(m), "A",
                        f"octet {pos:#04x} : {val:#04x}→{nouvelle:#04x}")
            n = rng.choice([2, 3, 4])
            n = min(n, len(octets) - pos)
            if n < 2:
                continue
            m = bytearray(octets)
            details = []
            for k in range(n):
                val = octets[pos + k]
                nouvelle = rng.choice(
                    [b for b in range(256) if b != val])
                m[pos + k] = nouvelle
                details.append(f"{val:#04x}→{nouvelle:#04x}")
            return (bytes(m), "B",
                    f"octets {pos:#04x}..{pos + n - 1:#04x} : "
                    + " ".join(details))

        # C : substitution d'opérateur/condition à longueur conservée
        if type_ == "C":
            insn = ref_insns[rng.randrange(len(ref_insns))]
            mnemo = insn.mnemonic
            cible = None
            for a, b in PAIRES:
                if mnemo == a:
                    cible = b
                    break
                if mnemo == b:
                    cible = a
                    break
            if cible is None:
                continue
            texte = cible + " " + insn.op_str
            try:
                enc, _ = MUT.KS.asm(texte, insn.address)
                enc = bytes(enc)
            except Exception:  # noqa: BLE001
                continue
            if not enc or len(enc) != insn.size:
                continue    # la longueur doit tenir EXACTEMENT
            pos = insn.address - ref_insns[0].address
            m = bytearray(octets)
            m[pos:pos + len(enc)] = enc
            if bytes(m) == octets:
                continue    # l'encodage serait identique : pas un mutant
            return (bytes(m), "C",
                    f"{pos:#04x} : {mnemo} → {cible} ({insn.op_str})")

        # D : altération d'immédiat ou de déplacement
        if type_ == "D":
            candidates = []
            for insn in ref_insns:
                texte = f"{insn.mnemonic} {insn.op_str}"
                if "#" in texte or "0x" in texte:
                    candidates.append(insn)
                elif any(ch.isdigit() for ch in insn.op_str):
                    candidates.append(insn)
            if not candidates:
                continue
            insn = candidates[rng.randrange(len(candidates))]
            pos = insn.address - ref_insns[0].address
            # les octets de l'immédiat/déplacement : à la fin pour les
            # immédiats ; on muter l'UN des octets non-opcode de fin
            fin = pos + insn.size
            debut_champ = pos + 2 if insn.size > 3 else pos + 1
            if fin - debut_champ < 1:
                continue
            cible_i = rng.randrange(debut_champ, fin)
            val = octets[cible_i]
            mode = rng.choice(["bit", "pm1", "complement"])
            if mode == "bit":
                nouvelle = val ^ (1 << rng.randrange(8))
            elif mode == "pm1":
                nouvelle = (val + rng.choice([1, -1])) % 256
            else:
                nouvelle = val ^ 0xFF
            if nouvelle == val:
                continue
            m = bytearray(octets)
            m[cible_i] = nouvelle
            return (bytes(m), "D",
                    f"champ {cible_i - pos:#04x} de {insn.mnemonic} "
                    f"({insn.op_str[:28]}) : {val:#04x}→{nouvelle:#04x}")
    return None, None, None   # aucun mutant trouvé (bloc dégénéré)


# ---------------------------------------------------------------------------
# LA CLASSIFICATION DES SURVIVANTS
# ---------------------------------------------------------------------------

def classifier(bloc, mutant: bytes, type_: str, detail: str) -> dict:
    """Chaque survivant porte sa classe et sa pièce. La preuve
    d'équivalence MÉCANIQUE : le décodage complet identique (l'octet muté
    ne change que l'encodage de la même sémantique)."""
    ref = MUT.decoder(bloc["octets"], bloc["rva"])
    mut = MUT.decoder(mutant, bloc["rva"])
    if ref is not None and mut is not None and len(ref) == len(mut):
        identiques = all(
            i.mnemonic == j.mnemonic and i.op_str == j.op_str
            for i, j in zip(ref, mut))
        if identiques:
            return {
                "classe": "MUTANT ÉQUIVALENT",
                "argument": ("le décodage COMPLET du bloc mutant est "
                             "IDENTIQUE instruction par instruction "
                             "(mnémoniques ET opérandes) : l'octet muté "
                             "n'a changé QUE l'encodage de la même "
                             "sémantique (préfixe inerte, encodage "
                             "alternatif) — la preuve d'équivalence est "
                             "le décodage lui-même"),
            }
    # la classe par défaut : le chemin non couvert, nommé
    bid = bloc["bid"]
    if bid.startswith("loupe"):
        scenario = ("la boucle winmain complète (l'ouverture, la cascade, "
                    "la peinture, la saisie, le défilement, le curseur, "
                    "la sauvegarde, la fermeture)")
    elif 20 <= int(bid.split("-")[1]) <= 28 and bid.startswith("tls13"):
        scenario = ("la composition de la poignée + l'enregistrement "
                    "protégé")
    elif bid.startswith("tls13"):
        scenario = "les vecteurs officiels de la famille (le différentiel)"
    else:
        scenario = "le harnais sys autonome (V1-V4)"
    return {
        "classe": "CHEMIN NON COUVERT",
        "argument": (f"la mutation ({type_} : {detail}) vit dans "
                     f"{bid} et {scenario} NE LA DISTINGUE PAS — le "
                     "contrôle manquant : un vecteur qui exercerait la "
                     "valeur/l'opération mutée (le mutant est vivant SOUS "
                     "CE SCÉNARIO : la limite constatée, jamais cachée)"),
    }


# ---------------------------------------------------------------------------
# LA CAMPAGNE
# ---------------------------------------------------------------------------

def clopper_pearson(tues: int, total: int, alpha: float = 0.05):
    from scipy.stats import beta
    if total == 0:
        return (0.0, 1.0)
    borne_basse = 0.0 if tues == 0 else \
        float(beta.ppf(alpha / 2, tues, total - tues + 1))
    borne_haute = 1.0 if tues == total else \
        float(beta.ppf(1 - alpha / 2, tues + 1, total - tues))
    return borne_basse, borne_haute


def scenario_du(bid: str) -> str:
    if bid.startswith("loupe"):
        return "K4-winmain"
    if bid.startswith("tls13"):
        num = int(bid.split("-")[1])
        return "K3-famille" if num <= 19 else "K4-orchestration"
    return "K4-sys"


def jouer_bloc(bloc, contexte, debut_idx=0, fin_idx=MUTANTS_PAR_BLOC):
    """Les mutants [debut_idx, fin_idx) d'un bloc — les verdicts lignes."""
    bid = bloc["bid"]
    octets = bloc["octets"]
    ref_insns = MUT.decoder(octets, bloc["rva"])
    lignes = []
    for i in range(debut_idx, fin_idx):
        rng = random.Random(f"{GRAINE}:{bid}:{i}")
        mutant, type_, detail = generer_mutant(octets, ref_insns, rng)
        if mutant is None:
            lignes.append({"bloc": bid, "idx": i, "type": "-", "détail":
                           "aucun mutant tirable", "k1": "-", "k2": "-",
                           "k3": "-", "k4": "-", "verdict": "REJETÉ",
                           "cause": "tirage épuisé"})
            continue
        # K1 : le round-trip
        m_insns = MUT.decoder(mutant, bloc["rva"])
        if m_insns is None or MUT.reassembler(m_insns) != mutant:
            lignes.append({"bloc": bid, "idx": i, "type": type_,
                           "détail": detail, "k1": "TUÉ", "k2": "-",
                           "k3": "-", "k4": "-", "verdict": "TUÉ",
                           "cause": "K1-roundtrip"})
            continue
        # K2 : la structure du plan
        if MUT.signature_structurelle(m_insns) != contexte["sigs"][bid]:
            lignes.append({"bloc": bid, "idx": i, "type": type_,
                           "détail": detail, "k1": "vivant", "k2": "TUÉ",
                           "k3": "-", "k4": "-", "verdict": "TUÉ",
                           "cause": "K2-structurel"})
            continue
        # K3 : le différentiel de famille (sous-ensemble honnête)
        k3 = "-"
        if (bid.startswith("tls13") and 1 <= int(bid.split("-")[1]) <= 19) \
                or bid == "loupe-06":
            tue, cause = contexte["juge"].tue(bloc, mutant)
            k3 = "TUÉ" if tue else "vivant"
            if tue:
                lignes.append({"bloc": bid, "idx": i, "type": type_,
                               "détail": detail, "k1": "vivant",
                               "k2": "vivant", "k3": k3, "k4": "-",
                               "verdict": "TUÉ", "cause": f"K3-{cause}"})
                continue
        # K4 : la composition (le rejeu v0.14.0 réutilisé TEL QUEL)
        k4 = "-"
        if bid.startswith("loupe"):
            tue, cause = R140.tuer_loupe(bid, mutant, bloc["rva"],
                                         contexte["base_loupe"])
            k4 = "TUÉ" if tue else "vivant"
        elif bid.startswith("tls13"):
            tue, cause = R140.tuer_tls13_orchestration(
                bid, mutant, bloc["rva"], contexte["bases_tls"])
            k4 = "TUÉ" if tue else "vivant"
        else:
            tue, cause = R140.tuer_sys(bid, mutant)
            k4 = "TUÉ" if tue else "vivant"
        if tue:
            lignes.append({"bloc": bid, "idx": i, "type": type_,
                           "détail": detail, "k1": "vivant", "k2": "vivant",
                           "k3": k3, "k4": k4, "verdict": "TUÉ",
                           "cause": f"K4-{cause}"})
        else:
            lignes.append({"bloc": bid, "idx": i, "type": type_,
                           "détail": detail, "k1": "vivant", "k2": "vivant",
                           "k3": k3, "k4": k4, "verdict": "VIVANT",
                           "cause": f"K4-{cause}"})
    return lignes


def contexte_sain(blocs):
    """Les bases SANE de la composition (les images propres)."""
    print("[base] la boucle winmain saine…", flush=True)
    os_v, emul = R140.instance_loupe()
    base_loupe = R140.observable_winmain(emul, os_v)
    assert base_loupe[0] == 0
    print("[base] les bases poignée + enregistrement…", flush=True)
    bases_tls = {"poignee": R140.base_poignee(),
                 "enregistrement": R140.base_enregistrement()}
    sigs = {}
    for domaine, liste in blocs.items():
        for bloc in liste:
            ref_insns = MUT.decoder(bloc["octets"], bloc["rva"])
            sigs[bloc["bid"]] = MUT.signature_structurelle(ref_insns)
    return {"base_loupe": base_loupe, "bases_tls": bases_tls, "sigs": sigs,
            "juge": MUT.JugeSemantique()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--debut", type=int, default=0,
                    help="l'index du PREMIER bloc (0..51)")
    ap.add_argument("--fin", type=int, default=52)
    ap.add_argument("--replay", action="store_true")
    ap.add_argument("--compare", action="store_true",
                    help="compare verdicts.csv et verdicts_rejeu.csv (fin de rejeu)")
    args = ap.parse_args()

    if args.compare:
        orig = list(csv.DictReader(
            open(SORTIES / "verdicts.csv", encoding="utf-8")))
        rejouees = list(csv.DictReader(
            open(SORTIES / "verdicts_rejeu.csv", encoding="utf-8")))
        pareil = len(orig) == len(rejouees) and all(
            all(o[k] == r[k] for k in ("bloc", "idx", "verdict", "cause"))
            for o, r in zip(orig, rejouees))
        print(f"[rejeu] {'BIT-IDENTIQUES' if pareil else 'DIVERGENTS'} "
              f"({len(rejouees)} lignes rejeu vs {len(orig)} originales)")
        return 0 if pareil else 1

    t0 = time.time()
    blocs = MUT.blocs_domaines()
    tous = ([(d, b) for d in ("loupe", "tls13", "sys") for b in blocs[d]])
    ctx = contexte_sain(blocs)

    fichier = SORTIES / ("verdicts_rejeu.csv" if args.replay
                         else "verdicts.csv")
    nouvelles = []
    existe = fichier.is_file()
    for d, bloc in tous[args.debut:args.fin]:
        t1 = time.time()
        lignes = jouer_bloc(bloc, ctx)
        nouvelles.extend(lignes)
        # l'écriture INCRÉMENTALE (un kill ne perd jamais un bloc joué)
        with open(fichier, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["bloc", "idx", "type",
                                              "détail", "k1", "k2", "k3",
                                              "k4", "verdict", "cause"])
            if not existe:
                w.writeheader()
                existe = True
            w.writerows(lignes)
        vivants = sum(1 for l in lignes if l["verdict"] == "VIVANT")
        tues = sum(1 for l in lignes if l["verdict"] == "TUÉ")
        print(f"[{d}] {bloc['bid']:12s} {len(lignes)} mutants : "
              f"{tues} tués, {vivants} vivants "
              f"({time.time() - t1:.1f} s)", flush=True)


    print(f"\n[campagne] {len(nouvelles)} mutants en "
          f"{time.time() - t0:.0f} s → {fichier.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
