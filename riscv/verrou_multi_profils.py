#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verrou_multi_profils.py — LE VERROU CROISÉ MULTI-PROFILS (chantier M7-(c) :
PLAN § chantier (c) — « empreintes des blocs des DEUX ISA vérifiées avant
chaque édition, R8 étendue »).

L'extension R8 aux DEUX ISA corpus : la parité inter-ISA se lit SUR LES
ARTÉFACTS ET LEURS CARTES — les empreintes des blocs re-vérifiées depuis le
disque pour l'instance x86-64-linux ET l'instance riscv64-linux, la
GÉOMÉTRIE MIROIR du plan constatée (les MÊMES spec/rva/slot), et la COUCHE
I partagée (les MÊMES fichiers canoniques, empreintes identiques dans les
DEUX cartes).

La règle d'usage (le plan) : le verrou se joue AVANT CHAQUE ÉDITION — le
scellage (une édition de carte) l'exige ; toute divergence est un REFUS.

Quatre recoupements, fail-closed :
  1. CHAQUE carte (unix/carte-corpus, riscv/carte-corpus) : signature
     Ed25519 vérifiée, frag-bld déchiffré, chaque empreinte de bloc ==
     sha256(artefact[rva:rva+slot]) relu du disque (13 blocs par instance) ;
  2. LA GÉOMÉTRIE MIROIR : la séquence (spec, rva, slot) du plan unix ==
     celle du plan riscv (les MÊMES adresses, les MÊMES slots — D8) ;
  3. LA COUCHE I PARTAGÉE : les empreintes [couche-I] des DEUX frag-prf
     nomment les MÊMES fichiers aux MÊMES empreintes, et chacune ==
     sha256 du fichier canonique sur le disque (la MÊME couche I chargée
     par les DEUX instances — la thèse du diff nul) ;
  4. LES SONDES de la lignée (riscv d122bc68…, unix f5f0a08f…) INTACTES :
     les artefactes voisins de la parité ne bougent pas.

Usage : python3 riscv/verrou_multi_profils.py (ou executer() — le scellage)
Retour : executer() -> (vert, lignes).
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RISCV = os.path.join(RACINE, "riscv")
UNIX = os.path.join(RACINE, "unix")


def _module(nom: str, chemin: str):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class EchecVerrou(Exception):
    """Toute divergence nommée (fail-closed)."""


def executer(bavard: bool = True) -> tuple[bool, list[str]]:
    lignes: list[str] = []
    vert = True

    def constat(message: str, ok: bool, detail: str = "") -> None:
        nonlocal vert
        vert = vert and ok
        l = f"[verrou-multi] {'PASS' if ok else 'ECHEC'} : {message}"
        if detail:
            l += f" ({detail})"
        lignes.append(l)

    # — 1. les DEUX cartes : signature + empreintes re-lues du disque -------
    total = 0
    for nom, rep in (("x86-64-linux-elf64", UNIX), ("riscv64-linux-elf64", RISCV)):
        cm = _module(f"carte_corpus_{nom}", os.path.join(rep, "carte_corpus.py"))
        L = _module(f"layout_{nom}", os.path.join(rep, "layout.py"))
        art = open(os.path.join(rep, "corpus"), "rb").read()
        entete, fragments, signature, pub = cm.lire_carte()
        cm.verifier_signature(pub, entete, fragments, signature)
        phrase, _ = cm.charger_secrets(interactif=False)
        maitre = cm.cle_maitresse(phrase)
        bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode()
        n = 0
        for bid, _spec, _f, rva, slot in L.BLOCS_CORPUS:
            m = re.search(rf"\[bloc\] id={bid} addr=\S+ empreinte=(\S+)", bld)
            attendu = m.group(1) if m else None
            reel = _sha(art[rva:rva + slot])
            if attendu != reel:
                raise EchecVerrou(f"{nom}/{bid} : l'empreinte de carte {attendu} "
                                  f"!= l'artefact relu {reel}")
            n += 1
        total += n
        constat(f"la carte {nom} : signature Ed25519 vérifiée, {n} empreintes "
                "de bloc == l'artefact relu du disque", True, f"{n} blocs")

    # — 2. la GÉOMÉTRIE MIROIR : les MÊMES spec/rva/slot aux DEUX ISA --------
    Lu = _module("layout_unix_m", os.path.join(UNIX, "layout.py"))
    Lr = _module("layout_riscv_m", os.path.join(RISCV, "layout.py"))
    miroir_u = [(spec, rva, slot) for _, spec, _, rva, slot in Lu.BLOCS_CORPUS]
    miroir_r = [(spec, rva, slot) for _, spec, _, rva, slot in Lr.BLOCS_CORPUS]
    constat("LA GÉOMÉTRIE MIROIR (D8) : la séquence spec/rva/slot du plan "
            "unix == celle du plan riscv — les MÊMES adresses, les MÊMES "
            "slots, la croissance au même plan, le staging au même plan",
            miroir_u == miroir_r,
            f"{len(miroir_u)} blocs miroir" if miroir_u == miroir_r
            else f"ÉCART : {[x for x in zip(miroir_u, miroir_r) if x[0] != x[1]][:3]}")

    # — 3. la COUCHE I PARTAGée : les MÊMES fichiers aux MÊMES empreintes ----
    couche = {}
    for nom, rep in (("x86-64-linux-elf64", UNIX), ("riscv64-linux-elf64", RISCV)):
        cm = _module(f"carte_corpus_{nom}", os.path.join(rep, "carte_corpus.py"))
        phrase, _ = cm.charger_secrets(interactif=False)
        maitre = cm.cle_maitresse(phrase)
        _, fragments, _, _ = cm.lire_carte()
        prf = cm.dechiffrer_fragment(maitre, "frag-prf",
                                     fragments["frag-prf"]).decode()
        ligne = next((l for l in prf.splitlines() if l.startswith("[couche-I]")), "")
        couples = dict(re.findall(r"(\S+?)=([0-9a-f]{12})", ligne))
        couche[nom] = couples
    fichiers_communs = set(couche["x86-64-linux-elf64"]) & set(couche["riscv64-linux-elf64"])
    memes = all(couche["x86-64-linux-elf64"][f] == couche["riscv64-linux-elf64"][f]
                for f in fichiers_communs)
    disque = True
    for f in fichiers_communs:
        with open(os.path.join(UNIX, "I", f + ".md"), "rb") as fh:
            if _sha(fh.read())[:12] != couche["x86-64-linux-elf64"][f]:
                disque = False
    constat("LA COUCHE I PARTAGÉE : les empreintes [couche-I] des DEUX "
            "frag-prf nomment les MÊMES fichiers canoniques aux MÊMES "
            "empreintes, et chacune == le fichier sur le disque (la thèse "
            "du diff nul — la MÊME couche chargée par les DEUX instances)",
            memes and disque and len(fichiers_communs) >= 13,
            f"{len(fichiers_communs)} fichiers, empreintes identiques")

    # — 4. les artefacts voisins de la parité INTACTS -------------------------
    attendus = {
        "riscv/sonde": "d122bc68fec2412677a9ebdd529a5f1d7d42b95898d680d78baa3a349f28d96e",
        "unix/sonde": "f5f0a08fa4f63067ccfbd96576de59c92049eb29650298f9d1cdca00fa24a810",
        "unix/corpus": "dd14195c9da5e9b990e8f9b141eedd6574bb8ecc793ffdd5b67edb71b81ddff7",
        "riscv/corpus": "ec343b4e8bebf21c8b29a6da1a5eb022fb7b8e4b50ce95c5906734ef0b043799",
    }
    for rel, attendu in attendus.items():
        with open(os.path.join(RACINE, rel), "rb") as f:
            reel = _sha(f.read())
        constat(f"l'artefact {rel} INTACT", reel == attendu, f"sha {reel[:16]}…")

    lignes.append(f"[verrou-multi] VERDICT : {'VERT' if vert else 'KO'} — "
                  f"{total} empreintes de bloc re-vérifiées depuis le disque "
                  "aux DEUX ISA, la géométrie miroir, la couche I partagée — "
                  "R8 ÉTENDUE aux deux instances de la parité (le verrou se "
                  "joue AVANT CHAQUE ÉDITION — le scellage l'exige)")
    if bavard:
        print("\n".join(lignes))
    return vert, lignes


if __name__ == "__main__":
    try:
        ok, _ = executer(bavard=True)
        sys.exit(0 if ok else 1)
    except EchecVerrou as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
