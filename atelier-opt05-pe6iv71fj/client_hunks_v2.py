#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""client_hunks_v2.py — LE CLIENT DU FORMAT HUNK v2 (l'amendement
FORMAT-V2-AMENDEMENT.md : la sémantique d'ancre explicite — l'ancre EST
le premier point du changement ; la première ligne « - » répète l'ancre ;
sans « - » l'ancre précède l'insertion ; la numérotation sans total).

LES QUATRE REFUS NOMMÉS demeurent : HORS-FORMAT | HUNK-INCONNU |
CONTEXTE-DIVERGENT | ROUND-TRIP-DIVERGENT — fail-closed."""
from __future__ import annotations

import re

from client_hunks import Refus, round_trip  # la confrontation inchangée

LIGNE_HUNK = re.compile(r"^@@ hunk (\d+)$")
LIGNE_BASE = re.compile(r"^base: (.*)$")
LIGNE_MOINS = re.compile(r"^- (.*)$")
LIGNE_PLUS = re.compile(r"^\+ (.*)$")
FIN = "FIN-HUNKS"


def parse_hunks(reponse: str) -> list[dict]:
    if not isinstance(reponse, str):
        raise Refus("HORS-FORMAT", "la réponse n'est pas un texte")
    lignes = reponse.strip("\r\n").split("\n")
    if not lignes or lignes[-1].strip() != FIN:
        raise Refus("HORS-FORMAT", f"la dernière ligne n'est pas « {FIN} »")
    hunks: list[dict] = []
    courant: dict | None = None
    vu_fin = False
    for i, l in enumerate(lignes):
        s = l.rstrip("\r")
        if vu_fin:
            raise Refus("HORS-FORMAT", f"du texte après {FIN} (ligne {i+1})")
        if s.strip() == FIN:
            vu_fin = True
            continue
        m = LIGNE_HUNK.match(s)
        if m:
            if courant is not None:
                hunks.append(courant)
            k = int(m.group(1))
            if k != len(hunks) + 1:
                raise Refus("HORS-FORMAT",
                            f"le hunk {k} hors séquence (attendu {len(hunks)+1})")
            courant = {"k": k, "base": None, "moins": [], "plus": []}
            continue
        if courant is None:
            raise Refus("HORS-FORMAT", f"une ligne avant le premier « @@ hunk » (ligne {i+1})")
        m = LIGNE_BASE.match(s)
        if m and courant["base"] is None:
            courant["base"] = m.group(1)
            continue
        m = LIGNE_MOINS.match(s)
        if m:
            if courant["base"] is None:
                raise Refus("HORS-FORMAT", f"« - » avant « base: » (hunk {courant['k']})")
            courant["moins"].append(m.group(1))
            continue
        m = LIGNE_PLUS.match(s)
        if m:
            if courant["base"] is None:
                raise Refus("HORS-FORMAT", f"« + » avant « base: » (hunk {courant['k']})")
            courant["plus"].append(m.group(1))
            continue
        raise Refus("HORS-FORMAT", f"la ligne {i+1} n'est d'aucune forme admise : {s[:60]!r}")
    if courant is not None:
        hunks.append(courant)
    if not hunks:
        raise Refus("HORS-FORMAT", "aucun hunk dans la réponse")
    for h in hunks:
        if h["base"] is None:
            raise Refus("HORS-FORMAT", f"le hunk {h['k']} n'a pas d'ancre « base: »")
        if not h["plus"]:
            raise Refus("HORS-FORMAT", f"le hunk {h['k']} n'a aucune ligne « + »")
        if h["moins"] and h["moins"][0] != h["base"]:
            raise Refus("CONTEXTE-DIVERGENT",
                        f"la première ligne « - » du hunk {h['k']} ne répète pas "
                        f"l'ancre « {h['base'][:50]} »")
    return hunks


def appliquer(base_texte: str, hunks: list[dict]) -> str:
    """La sémantique v2 : l'ancre EST le premier point du changement.
    Avec « - » : les retraits (la première = l'ancre) sont remplacés par
    les « + » à la position de l'ancre. Sans « - » : les « + » sont
    insérés APRÈS l'ancre."""
    lignes = base_texte.split("\n")
    for h in hunks:
        ancre = h["base"]
        idx = None
        for i, l in enumerate(lignes):
            if l == ancre:
                idx = i
                break
        if idx is None:
            raise Refus("HUNK-INCONNU",
                        f"l'ancre « {ancre[:60]} » (hunk {h['k']}) absente du texte courant")
        if h["moins"]:
            # les « - » confrontées au texte À PARTIR DE L'ANCRE (la
            # première répète l'ancre par la grammaire)
            pos = idx
            for attendu in h["moins"]:
                if pos >= len(lignes) or lignes[pos] != attendu:
                    raise Refus("CONTEXTE-DIVERGENT",
                                f"la ligne « {attendu[:60]} » (hunk {h['k']}) n'est pas "
                                f"à l'ancre « {ancre[:40]} »")
                pos += 1
            lignes[idx:pos] = list(h["plus"])
        else:
            lignes[idx + 1:idx + 1] = list(h["plus"])
    return "\n".join(lignes)


def traiter(base_texte: str, reponse: str) -> tuple[str, str]:
    hunks = parse_hunks(reponse)
    reconstruit = appliquer(base_texte, hunks)
    ok, detail = round_trip(reconstruit)
    if not ok:
        raise Refus("ROUND-TRIP-DIVERGENT", detail)
    return reconstruit, detail


if __name__ == "__main__":
    base = "push rbx\nmov eax, 5\npop rbx\nret"
    # v2 : l'ancre = la ligne changée, la première « - » la répète
    ok_hunks = ("@@ hunk 1\n"
                "base: mov eax, 5\n"
                "- mov eax, 5\n"
                "+ mov eax, 6\n"
                "FIN-HUNKS")
    r, d = traiter(base, ok_hunks)
    assert "mov eax, 6" in r and "mov eax, 5" not in r, r
    print("VERT  v2 l'application et le round-trip exact :", d)
    # v2 : insertion pure APRÈS l'ancre
    ins = ("@@ hunk 1\n"
           "base: push rbx\n"
           "+ mov edx, 7\n"
           "FIN-HUNKS")
    r, d = traiter(base, ins)
    assert r.split("\n")[1] == "mov edx, 7", r
    print("VERT  v2 l'insertion pure après l'ancre :", d)
    cas = [
        ("HUNK-INCONNU", "@@ hunk 1\nbase: push rdx\n- push rdx\n+ mov eax, 6\nFIN-HUNKS"),
        ("CONTEXTE-DIVERGENT", "@@ hunk 1\nbase: mov eax, 5\n- mov eax, 6\n+ mov eax, 7\nFIN-HUNKS"),
        ("CONTEXTE-DIVERGENT", "@@ hunk 1\nbase: mov eax, 5\n- mov eax, 5\n- ret\n+ mov eax, 7\nFIN-HUNKS"),
        ("HORS-FORMAT", "mov eax, 6\nFIN-HUNKS"),
        ("HORS-FORMAT", "@@ hunk 1\nbase: push rbx\n+ mov eax, 6"),
        ("ROUND-TRIP-DIVERGENT", "@@ hunk 1\nbase: push rbx\n+ mov eax, 99999999999999999999\nFIN-HUNKS"),
    ]
    for attendu, rep in cas:
        try:
            traiter(base, rep)
            raise SystemExit(f"ÉCHEC — {attendu} NON ATTRAPÉ")
        except Refus as e:
            assert e.nom == attendu, (e.nom, attendu)
            print(f"VERT  le refus {e.nom} attrapé au premier nom — {e.detail[:64]}")
    print("LE CLIENT HUNK v2 : 2 VERT + 6 refus nommés — autotest VERT")
