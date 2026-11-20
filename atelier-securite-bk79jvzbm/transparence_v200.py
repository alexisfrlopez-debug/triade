#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""transparence_v200.py — L'ANCRAGE DU TÉMOIN D'ÉPOQUE AU JOURNAL DE
TRANSPARENCE (la vague 9, l'instruction bk79jvzbm point 6, le
PLAN-BK79JVZBM H6 gelé).

LE JOURNAL DE TRANSPARENCE : la chaîne des ÉPOQUES du coffre (l'ère
D75 : la première lignée ; l'ère D80 : la rotation vécue le 19/11 —
la reconstitution à froid prouvée deux fois, D223) — CHAQUE époque
porte l'empreinte du témoin signé de sa cérémonie, chaînée depuis la
genèse (h_i = sha256(h_{i-1} ‖ époque ‖ témoin)).

L'ANCRAGE DU TÉMOIN D'ÉPOQUE : le témoin de l'ère COURANTE (l'empreinte
de la cérémonie + la hauteur de la chaîne + la date) ancré au journal —
LA VÉRIFICATION MACHINE : la chaîne recalculée de la genèse, le témoin
confronté, TOUT écart le refus nommé ANCRAGE-DIVERGENT.

LE DELTA AU MODÈLE DE MENACE (aux deux bords) :
  — CE QUE L'ANCRAGE AJOUTE : la détection de la RÉÉCRITURE d'époque
    (une époque omise ou falsifiée ROMPT la chaîne — le journal public
    la porte, le tiers peut vérifier) ;
  — CE QU'IL N'AJOUTE PAS : la preuve de PUBLICATION au monde (la
    chaîne locale ne prouve pas la diffusion — le dépôt public D220 la
    porte, l'ancrage l'assume, jamais ne la prétend).

LE CONTRÔLE NÉGATIF : une époque RÉÉCRITE au journal → l'ancrage la
REFUSE nommément (la falsification vécue au labo sur le mécanisme)."""
from __future__ import annotations

import hashlib
import json
import pathlib

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-securite-bk79jvzbm"

GENESE = b"TRIADE-TRANSPARENCE-2026"
# LES ÉPOQUES DU COFFRE (les pièces de cérémonie — les empreintes des
# témoins signés, LUES des pièces de la cérémonie D80/D183)
EPOQUES = [
    {"id": "epoque-D75", "date": "2026-10-28",
     "evenement": "la première lignée du coffre — la phrase de contrôle "
                  "posée, la garde active D81",
     "temoin": "d36bff0f963b7a5192d1969971b814810e44e871d75e72152beaca6051ed5b05"
               " (le Livre v1.0 — la pièce de la cérémonie)"},
    {"id": "epoque-D80", "date": "2026-10-29",
     "evenement": "LA ROTATION VÉCUE — la rotation de lignée, la nouvelle "
                  "phrase, la reconstitution préparée",
     "temoin": "25be93488d6d6f6273a6259e6e966a0b711cfb4c450d00f79e1d55a18"
               "0a8baef (le Livre v1.1 — la pièce de la cérémonie D80)"},
    {"id": "epoque-D183", "date": "2026-11-19",
     "evenement": "LA CÉRÉMONIE VÉCUE DE BOUT EN BOUT — le découpage Shamir "
                  "5/3, la répartition sur cinq médias, LA RECONSTITUTION "
                  "À FROID PROUVÉE DEUX FOIS (D223 : l'état vécu acté)",
     "temoin": "2b27fb8e2c7e936017f5b64e0f27ba1ad9b3ce823ea49b2d0d47c7e18"
               "18cf74 (la console-rescan — la pièce de l'Entrée 368)"},
]


def h(continu: bytes) -> str:
    return hashlib.sha256(continu).hexdigest()


def construire_chainon(epoques: list[dict]) -> list[dict]:
    prec = h(GENESE)
    out = []
    for e in epoques:
        corps = json.dumps({"id": e["id"], "date": e["date"],
                            "evenement": e["evenement"],
                            "temoin": e["temoin"]}, sort_keys=True)
        e2 = dict(e)
        e2["h"] = h(prec.encode() + e["id"].encode() + corps.encode())
        prec = e2["h"]
        out.append(e2)
    return out


def verifier_chainon(chainon: list[dict]) -> None:
    prec = h(GENESE)
    for e in chainon:
        corps = json.dumps({"id": e["id"], "date": e["date"],
                            "evenement": e["evenement"],
                            "temoin": e["temoin"]}, sort_keys=True)
        attendu = h(prec.encode() + e["id"].encode() + corps.encode())
        if e["h"] != attendu:
            raise RuntimeError(f"ANCRAGE-DIVERGENT : la chaîne rompue à "
                               f"{e['id']} — attendu {attendu[:16]}… rendu "
                               f"{e['h'][:16]}… (la réécriture ou "
                               "l'omission NOMMÉES)")
        prec = e["h"]


def main():
    rapport = ["L'ANCRAGE DU TÉMOIN D'ÉPOQUE AU JOURNAL DE TRANSPARENCE",
               "======================================================", ""]
    chainon = construire_chainon(EPOQUES)
    rapport.append("LE JOURNAL DE TRANSPARENCE (la chaîne des époques du "
                   "coffre) :")
    for e in chainon:
        rapport.append(f"  {e['id']} ({e['date']}) : h = {e['h'][:24]}… — "
                       f"{e['evenement'][:60]}…")

    # LA VÉRIFICATION MACHINE : la chaîne recalculée de la genèse
    verifier_chainon(chainon)
    rapport.append("\nLA VÉRIFICATION MACHINE : VERT — la chaîne recalculée "
                   "de la genèse, chaque chaînon conforme (h_i = "
                   "sha256(h_{{i-1}} ‖ époque ‖ témoin))")

    # L'ANCRAGE DU TÉMOIN COURANT : l'époque D183 (la courante)
    courant = chainon[-1]
    ancrage = {"regime": "TRIADE-TRANSPARENCE/1",
               "epoque_courante": courant["id"],
               "hauteur": len(chainon),
               "temoin": courant["temoin"],
               "racine": courant["h"],
               "note": "le témoin d'époque ANCRÉ — la réécriture rompt la "
                       "chaîne, l'omission aussi (la hauteur compte les "
                       "époques)"}
    (ICI / "ancrage-temoin-epoque.json").write_text(json.dumps(
        {"journal": chainon, "ancrage": ancrage}, indent=1,
        ensure_ascii=False), encoding="utf-8")
    rapport.append(f"L'ANCRAGE DU TÉMOIN COURANT : {courant['id']} à la "
                   f"hauteur {len(chainon)} — la racine {courant['h'][:24]}…"
                   f" — la pièce ancrage-temoin-epoque.json")

    # LE CONTRÔLE NÉGATIF : une époque RÉÉCRITE
    falsifie = [dict(e) for e in chainon]
    falsifie[1]["temoin"] = falsifie[1]["temoin"][:-1] + ("0" if
                                                          falsifie[1]["temoin"][-1] != "0" else "1")
    try:
        verifier_chainon(falsifie)
        rapport.append("LE CONTRÔLE NÉGATIF : ROUGE — la réécriture "
                       "ACCEPTÉE (l'échec du contrôle)")
        return 2
    except RuntimeError as exc:
        rapport.append(f"LE CONTRÔLE NÉGATIF : VERT — une époque réécrite "
                       f"est REFUSÉE nommément : {exc}")

    # LE DELTA AU MODÈLE DE MENACE (aux deux bords)
    rapport += [
        "",
        "LE DELTA AU MODÈLE DE MENACE (aux deux bords) :",
        "  — CE QUE L'ANCRAGE AJOUTE (le bord du coffre) : la détection de "
        "la RÉÉCRITURE d'époque (la falsification ROMPT la chaîne — le "
        "contrôle négatif VÉCU ci-dessus) et de L'OMISSION (la hauteur "
        "compte les époques : une époque sautée change la racine) ;",
        "  — CE QU'IL N'AJOUTE PAS : la preuve de PUBLICATION au monde — "
        "la chaîne locale ne prouve pas la diffusion (le dépôt public "
        "D220 la porte, l'ancrage l'ASSUME, jamais ne la prétend) ; la "
        "confiance dans le secret de cérémonie (le séquestre Shamir 5/3 "
        "demeure la garde active — D223).",
    ]
    (ICI / "rapport-transparence.txt").write_text("\n".join(rapport) + "\n",
                                                  encoding="utf-8")
    print("\n".join(rapport))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
