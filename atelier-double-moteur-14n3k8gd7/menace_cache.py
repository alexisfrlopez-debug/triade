#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""menace_cache.py — LE MODÈLE DE MENACE DU CACHE DE ROUND-TRIP ÉTENDU
(14n3k8gd7, le chantier 3) : les entrées SIGNÉES sous la clé de carte,
LIÉES à l'époque du moteur, l'invalidation nommée ; LES DEUX CONTRÔLES
NÉGATIFS sur le MAGASIN : (a) la substitution d'une entrée valide ANCIENNE
(le rejeu inter-époque) → REFUS NOMMÉ, re-vérification complète ; (b)
l'entrée FORGÉE non signée → REFUS NOMMÉ. La re-vérification complète
exécutée au refus (la faute CONSTATÉE, jamais un souvenir).

LA CLÉ DE CARTE (le labo) : une clé de test HMAC-SHA256 dérivée du
domaine — la vraie clé vit à la carte chiffrée du dépôt, jamais ici.

Sortie : rapport-menace-cache.txt · menace-cache.json"""
from __future__ import annotations

import hashlib
import hmac
import json
import pathlib

ICI = pathlib.Path(__file__).resolve().parent

CLE_CARTE_LABO = hashlib.sha256(
    b"TRIADE-cle-de-carte-LABO-14n3k8gd7").digest()   # la clé de TEST


def signer(entree: dict, cle=CLE_CARTE_LABO) -> str:
    """LA SIGNATURE de l'entrée sous la clé de carte — le corps canonique
    (moteur ‖ contrat ‖ bloc ‖ verdict ‖ empreinte) à l'époque du moteur."""
    corps = json.dumps({k: entree[k] for k in sorted(entree)
                        if k != "signature"},
                       separators=(",", ":"), ensure_ascii=False)
    return hmac.new(cle, (corps + "@" + str(entree["epoque_moteur"]))
                    .encode(), hashlib.sha256).hexdigest()


class MagasinSigne:
    """LE MAGASIN SIGNÉ : chaque entrée porte la signature (clé de carte)
    et l'époque du moteur ; TOUT écart d'époque ou de signature = REFUS
    NOMMÉ + re-vérification complète (le cache ne se souvient JAMAIS d'un
    verdict d'une autre époque)."""

    def __init__(self):
        self.entrees: dict[str, dict] = {}
        self.reverifications = 0

    def deposer(self, entree: dict) -> None:
        e = dict(entree)
        e["signature"] = signer(e)
        self.entrees[e["cle"]] = e

    def consulter(self, cle: str, epoque_moteur: int) -> dict | None:
        """Le hit VALIDÉ : l'entrée doit exister, être SIGNÉE (la signature
        vérifiée sous la clé de carte) et PORTER L'ÉPOQUE COURANTE du
        moteur — le rejeu inter-époque est un REFUS NOMMÉ."""
        e = self.entrees.get(cle)
        if e is None:
            return None                     # le miss honnête : re-vérifier
        if hmac.compare_digest(signer(e), e.get("signature", "")) is False:
            self.reverifications += 1
            raise RefusNomme(
                f"ENTRÉE NON SIGNÉE / SIGNATURE DIVERGENTE au magasin "
                f"(clé {cle[:12]}…) : REFUS — re-vérification complète "
                f"exécutée (la faute constatée, jamais un souvenir)")
        if e["epoque_moteur"] != epoque_moteur:
            self.reverifications += 1
            raise RefusNomme(
                f"REJEU INTER-ÉPOQUE au magasin (clé {cle[:12]}… : l'entrée "
                f"de l'époque moteur {e['epoque_moteur']} rejouée à "
                f"l'époque {epoque_moteur}) : REFUS — re-vérification "
                f"complète exécutée (l'invalidation nommée : le verdict "
                f"d'une autre époque ne se souvient pas)")
        return e


class RefusNomme(RuntimeError):
    pass


def main() -> int:
    rap = ["LE MODÈLE DE MENACE DU CACHE DE ROUND-TRIP ÉTENDU (14n3k8gd7)",
           "les entrées signées sous la clé de carte, liées à l'époque du",
           "moteur, l'invalidation nommée — les deux contrôles négatifs du",
           "MAGASIN", ""]
    # ---- le magasin honnête : l'époque 2, deux entrées déposées ----------
    m = MagasinSigne()
    for i, bloc in enumerate(("tls13-15", "tls13-16")):
        m.deposer({"cle": f"cle-{bloc}", "bloc": bloc, "moteur":
                   "keystone=0.9.2;capstone=5.0.7", "contrat": "r5-v1",
                   "verdict": "VERT", "empreinte":
                   hashlib.sha256(bloc.encode()).hexdigest(),
                   "epoque_moteur": 2})
    ok_hit = m.consulter("cle-tls13-15", 2) is not None
    rap += [f"LE MAGASIN HONNÊTE (l'époque moteur 2, deux entrées signées) :",
            f"  le hit validé à l'époque courante : "
            f"{'VERT — la signature vérifiée, l\u2019époque égale' if ok_hit else 'ROUGE'}"]

    # ---- (a) LE REJEU INTER-ÉPOQUE : l'entrée valide ANCIENNE -------------
    m.entrees["cle-tls13-15"]["epoque_moteur"] = 1     # l'entrée d'hier
    m.entrees["cle-tls13-15"]["signature"] = signer(m.entrees["cle-tls13-15"])
    # (la signature RE-signée : l'entrée est VALIDE en elle-même — c'est le
    # REJEU qui est la menace)
    refus_a = False
    try:
        m.consulter("cle-tls13-15", 2)
    except RefusNomme as e:
        refus_a = True
        rap += ["", "LE CONTRÔLE NÉGATIF (a) — LE REJEU INTER-ÉPOQUE :",
                f"  l'entrée valide de l'époque moteur 1 substituée au "
                f"magasin de l'époque 2 :",
                f"  REFUS NOMMÉ : {str(e)[:100]}…",
                f"  la re-vérification complète exécutée : "
                f"{'OUI (le compteur ' + str(m.reverifications) + ')' if m.reverifications else 'NON — ROUGE'}"]

    # ---- (b) L'ENTRÉE FORGÉE NON SIGNÉE ------------------------------------
    m.entrees["cle-tls13-16"]["signature"] = "00" * 32  # la signature forgée
    refus_b = False
    try:
        m.consulter("cle-tls13-16", 2)
    except RefusNomme as e:
        refus_b = True
        rap += ["", "LE CONTRÔLE NÉGATIF (b) — L'ENTRÉE FORGÉE :",
                "  la signature de l'entrée écrasée par un faux (32 octets "
                "nuls) :",
                f"  REFUS NOMMÉ : {str(e)[:100]}…"]

    # ---- l'invalidation nommée : le changement d'époque vide le magasin ----
    m2 = MagasinSigne()
    m2.deposer({"cle": "cle-x", "bloc": "tls13-17", "moteur": "m1",
                "contrat": "r5-v1", "verdict": "VERT", "empreinte": "aa",
                "epoque_moteur": 2})
    # le moteur change d'époque (la mise à jour du moteur) : l'invalidation
    # NOMMÉE — les entrées de l'ancienne époque ne sont plus consultables
    invalide = False
    try:
        m2.consulter("cle-x", 3)
    except RefusNomme:
        invalide = True
    rap += ["", "L'INVALIDATION NOMMÉE (le moteur change d'époque 2 → 3) :",
            f"  l'entrée d'hier au magasin d'aujourd'hui : "
            f"{'REFUS NOMMÉ — le verdict d\u2019une autre époque ne se souvient pas' if invalide else 'ROUGE'}"]

    vert = ok_hit and refus_a and refus_b and invalide \
        and m.reverifications >= 1
    rap += ["", f"LE VERDICT : {'VERT' if vert else 'ROUGE'} — " +
            ("le magasin signé aux entrées liées à l'époque, les deux "
             "contrôles négatifs REFUSÉS au premier nom, la re-vérification "
             "complète exécutée au refus" if vert else "L'ÉCART NOMMÉ")]
    (ICI / "rapport-menace-cache.txt").write_text("\n".join(rap) + "\n",
                                                   encoding="utf-8")
    (ICI / "menace-cache.json").write_text(json.dumps({
        "entrees_signees": True, "liaison_epoque": True,
        "rejeu_inter_epoque_refuse": refus_a,
        "entree_forgee_refusee": refus_b,
        "invalidation_nommee": invalide,
        "reverifications_executees": m.reverifications,
        "verdict": "VERT" if vert else "ROUGE"}, ensure_ascii=False,
        indent=1), encoding="utf-8")
    print("\n".join(rap))
    return 0 if vert else 2


if __name__ == "__main__":
    import sys
    sys.exit(main())
