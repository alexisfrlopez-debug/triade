#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""expansion_pointeur.py — L'EXPANSION CÔTÉ CLIENT du pointeur seul (le plan
§ 1.1 : le pointeur ne porte plus le contenu — le client le reconstruit et
le confronte, fail-closed, QUATRE refus nommés).

Le pointeur : « IDENTIFIANT · sha256:<64 hex> » — une ligne exactement.
Le client : la table de la carte (régénérée des fichiers mêmes), la
confrontation octet pour octet, l'expansion mécanique de l'entête."""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
NOTATIONS = REPO / "loupe" / "notation"


class RefusPointeur(Exception):
    """Un refus nommé — fail-closed (le plan § 1.1)."""


def table_carte() -> dict[str, dict]:
    """La table des 18 — RÉGÉNÉRÉE des fichiers mêmes (jamais tapée)."""
    table = {}
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
        table[bid] = {"nom": f.stem, "entete": joint,
                      "empreinte": hashlib.sha256(
                          f.read_bytes()).hexdigest()}
    return table


def expanser(ligne_pointeur: str, table: dict[str, dict] | None = None) -> dict:
    """Le geste client complet — quatre refus nommés :

    1. HORS-FORMAT       — la ligne ne porte pas la forme exigée ;
    2. POINTEUR-INCONNU  — l'identifiant n'est pas à la carte ;
    3. EMPREINTE-DIVERGENTE — l'empreinte rendue != l'empreinte de la carte ;
    4. EXPANSION-DIVERGENTE — l'entête expansé != l'entête du bloc soumis
       (l'appelant fournit l'entête soumis via attendu_entete=).

    Retourne {id, empreinte, entete} — l'expansion mécanique."""
    if table is None:
        table = table_carte()
    lignes = [x for x in ligne_pointeur.splitlines() if x.strip()]
    if len(lignes) != 1:
        raise RefusPointeur(
            f"HORS-FORMAT : {len(lignes)} lignes rendues (une exigée) — "
            f"« {ligne_pointeur[:60]}… »")
    m = re.match(r"^(i\d+)\s*·\s*sha256:([0-9a-f]{64})$", lignes[0].strip())
    if not m:
        raise RefusPointeur(
            f"HORS-FORMAT : la ligne-pointeur ne porte pas la forme "
            f"IDENTIFIANT · sha256:<64 hex> — « {lignes[0][:70]}… »")
    bid, empreinte = m.group(1), m.group(2)
    if bid not in table:
        raise RefusPointeur(
            f"POINTEUR-INCONNU : l'identifiant {bid} n'est pas à la carte")
    attendu = table[bid]["empreinte"]
    if empreinte != attendu:
        raise RefusPointeur(
            f"EMPREINTE-DIVERGENTE : rendue {empreinte[:16]}…, la carte "
            f"porte {attendu[:16]}… — le pointeur est PÉRIMÉ (l'entrée a "
            f"changé de version, R8 en esprit)")
    entete = table[bid]["entete"]
    return {"id": bid, "empreinte": empreinte, "entete": entete}


def confronte(ligne_pointeur: str, entete_soumis: str,
              table: dict[str, dict] | None = None) -> dict:
    """L'expansion + LA QUATRIÈME PORTE : l'entête expansé confronté à
    l'entête du bloc SOUMIS (le matériau de la requête) — octet pour
    octet, le pointeur doit désigner LE bloc demandé."""
    ex = expanser(ligne_pointeur, table)
    if ex["entete"] != entete_soumis:
        raise RefusPointeur(
            "EXPANSION-DIVERGENTE : l'entête expansé de "
            f"{ex['id']} != l'entête du bloc soumis — le pointeur désigne "
            "un AUTRE bloc que celui de la requête")
    return ex


def _demonstration() -> int:
    """La falsification du pointeur (le plan § 1.3) : les trois contrôles
    négatifs vécus + les 18 expansions honnêtes."""
    table = table_carte()
    assert len(table) == 18, f"18 blocs attendus, {len(table)} lus"
    verts = 0

    # (1) l'empreinte mutée → EMPREINTE-DIVERGENTE
    un = next(iter(table.values()))
    vrai = f"{next(iter(table))} · sha256:{un['empreinte']}"
    faux = vrai[: len(vrai) - 1] + ("0" if vrai[-1] != "0" else "1")
    try:
        expanser(faux, table)
        print("ROUGE : l'empreinte mutée NON attrapée")
        return 2
    except RefusPointeur as e:
        if not str(e).startswith("EMPREINTE-DIVERGENTE"):
            print(f"ROUGE : le refus inattendu : {e}")
            return 2
        print(f"VERT  l'empreinte mutée → REFUS {str(e).split(':')[0]}")
        verts += 1

    # (2) l'identifiant inconnu → POINTEUR-INCONNU
    try:
        expanser(f"i999999 · sha256:{un['empreinte']}", table)
        print("ROUGE : l'identifiant inconnu NON attrapé")
        return 2
    except RefusPointeur as e:
        if not str(e).startswith("POINTEUR-INCONNU"):
            print(f"ROUGE : le refus inattendu : {e}")
            return 2
        print(f"VERT  l'identifiant inconnu → REFUS {str(e).split(':')[0]}")
        verts += 1

    # (3) la réponse hors format → HORS-FORMAT
    for bid, b in table.items():
        pass
    try:
        expanser(f"{bid} · sha3:{un['empreinte']}", table)
        print("ROUGE : la réponse hors format NON attrapée")
        return 2
    except RefusPointeur as e:
        if not str(e).startswith("HORS-FORMAT"):
            print(f"ROUGE : le refus inattendu : {e}")
            return 2
        print(f"VERT  la réponse hors format → REFUS {str(e).split(':')[0]}")
        verts += 1

    # (4) les 18 expansions honnêtes + la confrontation
    for bid, b in table.items():
        ex = confronte(f"{bid} · sha256:{b['empreinte']}", b["entete"],
                       table)
        assert ex["entete"] == b["entete"] and ex["id"] == bid
    print("VERT  les 18 expansions honnêtes — l'entête reconstruit == "
          "l'entête soumis, octet pour octet")
    verts += 1

    # (5) l'expansion désignant un autre bloc → EXPANSION-DIVERGENTE
    ids = sorted(table)
    bid_a, bid_b = ids[0], ids[1]
    try:
        confronte(f"{bid_a} · sha256:{table[bid_a]['empreinte']}",
                  table[bid_b]["entete"], table)
        print("ROUGE : le pointeur croisé NON attrapé")
        return 2
    except RefusPointeur as e:
        if not str(e).startswith("EXPANSION-DIVERGENTE"):
            print(f"ROUGE : le refus inattendu : {e}")
            return 2
        print(f"VERT  le pointeur croisé (désigne un autre bloc) → REFUS "
              f"{str(e).split(':')[0]}")
        verts += 1

    print(f"\nL'EXPANSION CÔTÉ CLIENT : {verts}/5 VERT — QUATRE refus "
          "nommés, fail-closed, la table régénérée des fichiers mêmes")
    return 0


if __name__ == "__main__":
    sys.exit(_demonstration())
