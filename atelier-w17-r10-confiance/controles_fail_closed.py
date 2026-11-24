#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATELIER W17R3R10 — les contrôles fail-closed de la racine de confiance (au banc).

Objet : éprouver, hors matériel et hors réseau, les SEPT refus nommés que la
spécification exige au chargement (R10) et l'ACCEPTATION du cas nominal. Le banc
ne revendique aucune exécution matérielle : il vérifie la LOGIQUE de la porte,
telle qu'elle est écrite au plan gelé W17R3R10.

Ce que le banc modélise : la carte (manifeste signé Ed25519), le plancher de
version, l'état local (époque), la clé d'ancre locale, et l'interdiction de toute
dépendance réseau au chargement. Ce que le banc NE modélise PAS : l'ancre
d'exploitation réelle (signature de code du système, secure boot, TEE) — elle
reste au poste réel, statut « en attente », jamais simulée.

Aucun secret réel n'est lu ni écrit : la clé est engendrée EN MÉMOIRE au début
du run, les fichiers de travail vivent dans un répertoire temporaire détruit à
la fin.

Codes : 0 = tous les contrôles attendus rendus ; 1 = un contrôle a divergé ;
2 = le banc n'a pas pu s'exécuter (dépendance absente) — jamais un vert de
complaisance.
"""
import hashlib
import json
import os
import socket
import sys
import tempfile

try:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey,
        Ed25519PublicKey,
    )
    from cryptography.hazmat.primitives import serialization
except Exception as e:  # pragma: no cover - dépendance du poste
    print(f"[R10] DEPENDANCE ABSENTE : cryptography ({e}) — banc NON EXECUTE")
    sys.exit(2)

PLANCHER = "0.7.0"
VERSION = "0.24.0"
PROFIL = "x86-64-linux-elf64"

# ---- la porte, telle que la spécification la décrit (référence exécutable) ----
class Refus(Exception):
    def __init__(self, nom):
        super().__init__(nom)
        self.nom = nom


def empreinte_manifeste(carte):
    """L'empreinte du manifeste de build : la carte porte les blocs, pas les octets."""
    corps = json.dumps(carte["blocs"], sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(corps).hexdigest()


def octet_signe(carte):
    corps = {
        "profil": carte["profil"],
        "version": carte["version"],
        "plancher": carte["plancher"],
        "manifeste": carte["manifeste"],
        "blocs": carte["blocs"],
        "epoque": carte["epoque"],
    }
    return json.dumps(corps, sort_keys=True, separators=(",", ":")).encode()


def porte_r10(carte, cle_pub, etat, premiere_ouverture=False, reseau_interdit=True):
    """Rend (verdict, detail). Verdict : 'OUVERT' ou le nom du refus.

    L'ordre des portes est celui du plan : présence → signature → manifeste →
    plancher → fraîcheur → état. Un refus est TERMINAL : aucune porte suivante
    n'est évaluée et aucun chemin dégradé n'existe.
    """
    # (0) la carte existe
    if carte is None:
        return "CARTE ABSENTE", "aucune carte au dépôt"
    # (0 bis) la clé d'ancre est locale et présente — jamais récupérée
    if cle_pub is None:
        return "CLE D'ANCRE ABSENTE", "clé publique introuvable — aucune récupération"
    # (1) authenticité : la signature couvre la carte entière
    try:
        cle_pub.verify(carte["signature"], octet_signe(carte))
    except InvalidSignature:
        return "SIGNATURE INVALIDE", "la signature ne couvre pas la carte présentée"
    # (2) intégrité : le manifeste recomposé égale le manifeste scellé
    if empreinte_manifeste(carte) != carte["manifeste"]:
        return "MANIFESTE DIVERGENT", "empreinte recomposée != empreinte signée"
    # (3) fraîcheur, volet version : monotonie contre le plancher
    if not _version_ge(carte["version"], carte["plancher"]):
        return "VERSION SOUS LE PLANCHER", f"{carte['version']} < {carte['plancher']}"
    # (4) fraîcheur, volet époque : l'état local ne recule pas
    if etat is None:
        if not premiere_ouverture:
            return "ETAT ABSENT", "première ouverture non déclarée"
    elif carte["epoque"] < etat["epoque"]:
        return "RETOUR EN ARRIERE", f"époque {carte['epoque']} < état {etat['epoque']}"
    # (5) aucune dépendance réseau au chargement
    if reseau_interdit and _socket_utilise():
        return "RESEAU AU CHARGEMENT", "une tentative réseau a été constatée"
    return "OUVERT", "toutes les portes franchies"


def _version_ge(a, b):
    def t(v):
        return tuple(int(x) for x in v.split("."))
    return t(a) >= t(b)


_TENTATIVES = {"n": 0}
_ORIG_SOCKET = socket.socket


def _socket_utilise():
    return _TENTATIVES["n"] > 0


def _neutraliser_reseau():
    """Toute tentative réseau au chargement est COMPTÉE puis refusée — jamais servie."""
    def refus(*a, **k):
        _TENTATIVES["n"] += 1
        raise OSError("réseau interdit au chargement (R10)")
    socket.socket = refus
    socket.create_connection = refus
    socket.getaddrinfo = refus


def _restaurer_reseau():
    socket.socket = _ORIG_SOCKET


# ----------------------------- le banc -----------------------------
def _carte_signee(cle_priv, **remplacements):
    blocs = [{"nom": "b7f3a9", "sha256": "a" * 64}, {"nom": "c1d2e3", "sha256": "b" * 64}]
    carte = {
        "profil": PROFIL,
        "version": VERSION,
        "plancher": PLANCHER,
        "blocs": blocs,
        "epoque": 12,
    }
    carte["manifeste"] = empreinte_manifeste(carte)
    carte.update(remplacements)
    if "signature_forcee" in carte:
        carte["signature"] = carte.pop("signature_forcee")
    else:
        carte["signature"] = cle_priv.sign(octet_signe(carte))
    return carte


def banc():
    cle_priv = Ed25519PrivateKey.generate()
    cle_pub = cle_priv.public_key()
    autre_priv = Ed25519PrivateKey.generate()
    etat = {"epoque": 12, "version": VERSION}

    controles = []

    def attendre(nom, attendu, carte, **kw):
        reseau = kw.pop("reseau_interdit", True)
        if kw.pop("neutraliser", True):
            _neutraliser_reseau()
        try:
            verdict, detail = porte_r10(carte, kw.pop("cle_pub", cle_pub), kw.pop("etat", etat), **kw)
        finally:
            _restaurer_reseau()
        ok = verdict == attendu
        controles.append((nom, attendu, verdict, detail, ok))
        return ok

    # [1] le cas nominal : la carte signée, l'état cohérent, hors ligne → OUVERT
    attendre("nominal (carte signée, état à l'époque, hors ligne)", "OUVERT", _carte_signee(cle_priv))
    # [2] carte absente
    attendre("carte absente", "CARTE ABSENTE", None)
    # [3] signature d'une autre clé (la carte est authentique pour un autre signataire)
    attendre("signature d'une autre clé", "SIGNATURE INVALIDE",
             _carte_signee(autre_priv))
    # [4] un octet du corps muté APRÈS signature
    c = _carte_signee(cle_priv)
    c["blocs"][0]["sha256"] = "c" * 64
    attendre("corps muté après signature", "SIGNATURE INVALIDE", c)
    # [5] manifeste recomposé divergent (bloc retiré, signature refaite sur la carte mutée)
    c = _carte_signee(cle_priv)
    c["manifeste"] = "0" * 64
    c["signature"] = cle_priv.sign(octet_signe(c))
    attendre("manifeste divergent (signé sur une carte mutée)", "MANIFESTE DIVERGENT", c)
    # [6] version sous le plancher
    c = _carte_signee(cle_priv, version="0.6.0")
    attendre("version sous le plancher", "VERSION SOUS LE PLANCHER", c)
    # [7] état restauré ancien (l'époque de la carte recule sous l'état local)
    c = _carte_signee(cle_priv, epoque=9)
    attendre("état restauré (époque 9 < état 12)", "RETOUR EN ARRIERE", c, etat={"epoque": 12, "version": VERSION})
    # [8] premier chargement sans état : refusé sans déclaration explicite
    attendre("état absent sans déclaration", "ETAT ABSENT", _carte_signee(cle_priv), etat=None)
    # [9] premier chargement déclaré : admis (la première ouverture est un acte nommé)
    attendre("première ouverture déclarée", "OUVERT", _carte_signee(cle_priv), etat=None,
             premiere_ouverture=True)
    # [10] clé d'ancre absente du disque : refus propre, jamais de récupération
    attendre("clé d'ancre absente", "CLE D'ANCRE ABSENTE", _carte_signee(cle_priv), cle_pub=None)
    # [11] une tentative réseau au chargement (le vérificateur tenterait de résoudre une révocation)
    def avec_reseau():
        try:
            socket.getaddrinfo("exemple.invalid", 443)
        except OSError:
            pass
    _neutraliser_reseau()
    try:
        avec_reseau()  # la tentative est COMPTÉE par le refus réseau
        verdict, detail = porte_r10(_carte_signee(cle_priv), cle_pub, etat, reseau_interdit=True)
    finally:
        _restaurer_reseau()
    ok = verdict == "RESEAU AU CHARGEMENT"
    controles.append(("tentative réseau au chargement", "RESEAU AU CHARGEMENT", verdict, detail, ok))

    print("=" * 78)
    print("ATELIER W17R3R10 — CONTRÔLES FAIL-CLOSED DE LA PORTE R10 (BANC)")
    print("=" * 78)
    verts = 0
    for nom, attendu, verdict, detail, ok in controles:
        marque = "VERT" if ok else "ROUGE"
        verts += 1 if ok else 0
        print(f"[{marque}] {nom}")
        print(f"        attendu : {attendu} · rendu : {verdict} ({detail})")
    print("-" * 78)
    print(f"{verts}/{len(controles)} contrôles rendus — aucun résultat matériel revendiqué")
    return 0 if verts == len(controles) else 1


if __name__ == "__main__":
    sys.exit(banc())
