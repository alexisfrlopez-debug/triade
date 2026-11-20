#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ancrage_temoins.py — L'ANCRAGE REKOR/RFC 3161 DES TÉMOINS D'ÉPOQUE
(l'atelier coffre-vr9n3s3l7, plan (f) — l'extension D219).

LE TÉMOIN D'ÉPOQUE (la structure, la lettre du plan : époque, checksum,
empreinte du conteneur) :

  { "magic": "TRIADE-TEMOIN-EPOQUE v1",
    "epoque": <u64>,                  # l'époque scellée
    "checksum": "<8 hex>",            # H_projet[:4].hex — la valeur humaine
    "empreinte_conteneur": "<64 hex>",  # sha256 de l'EN-TÊTE complet
    "empreinte_chiffretexte": "<64 hex>",  # sha256 du chiffretexte (nu — le
                                       # témoin est PUBLIC, il ne porte
                                       # JAMAIS l'empreinte LIÉE à la clé)
    "p_idx": <u32>,                   # le jeu Argon2 versionné (c)
    "date": "<UTC>" }

Le témoin est CANONISÉ (JSON trié, compact) puis haché : c'est LE HASH SEUL
(« jamais le contenu ») qui part à l'ancre.

LES DEUX MÉCANISMES, SPÉCIFIÉS puis IMPLÉMENTÉS EN LABORATOIRE :

  (1) RFC 3161 : la TimeStampReq DER (version 1, messageImprint =
      AlgorithmIdentifier(sha256) ‖ OCTET STRING digest, certReq FALSE,
      nonce aléatoire) — construite à la main (l'encodeur DER minimal du
      labo) ; la réponse de LABO : un « TSA de laboratoire » (clé Ed25519
      de TEST) signe (digest ‖ généré-à ‖ nonce) ; la VÉRIFICATION
      cryptographique locale : signature valide ∧ digest == celle du témoin
      ∧ nonce réciproque. LA REQUÊTE RÉSEAU RÉELLE vers une TSA nommée
      (DigiCert/GlobalSign/Sectigo…) est AU GESTE DU MAÎTRE — JAMAIS
      exécutée sans commande : LE GAP EST NOMMÉ.

  (2) Rekor : l'entrée {digest} au journal de transparence ; en labo : un
      arbre de Merkle (feuilles = entrées, la nôtre dedans), la CHECKSUM
      SIGNÉE de la racine (Ed25519 de test), la PREUVE D'INCLUSION
      (chemin des frères) — VÉRIFIÉE LOCALEMENT : la racine recalculée
      depuis la feuille + la preuve == la racine signée, la signature
      vérifiée. L'ENTRÉE RÉELLE au rekor.sigstore.dev est AU GESTE DU
      MAÎTRE — LE GAP EST NOMMÉ.

LA VÉRIFICATION MACHINE (la lettre : le timbre recoupé, la réécriture du
témoin REFUSÉE) : verifier_temoin() reconstruit le témoin depuis le
CONTENEUR sur disque et le confronte au témoin ancré — TOUT écart (un
champ muté, une époque réécrite, un conteneur substitué) = REFUS NOMMÉ.
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import time

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey)
from cryptography.hazmat.primitives import serialization

import coffre_labo as C

MAGIC_TEMOIN = "TRIADE-TEMOIN-EPOQUE v1"


# ---------------------------------------------------------------------------
# La construction du témoin (structure + canonique)
# ---------------------------------------------------------------------------

def construire_temoin(conteneur_chemin: str) -> dict:
    """Le témoin D'ÉPOQUE lu au conteneur — époque, checksum, empreinte du
    conteneur, empreinte du chiffretexte (NU — publique), p_idx, date."""
    with open(conteneur_chemin, "rb") as f:
        blob = f.read()
    entete = C.parser_entete(blob)
    return {
        "magic": MAGIC_TEMOIN,
        "epoque": entete["epoque"],
        "checksum": entete["h_projet"][:4].hex(),
        "empreinte_conteneur": hashlib.sha256(entete["entete"]).hexdigest(),
        "empreinte_chiffretexte": hashlib.sha256(
            entete["chiffretexte"]).hexdigest(),
        "p_idx": entete["p_idx"],
        "date": C._date_utc(),
    }


def canonique(temoin: dict) -> bytes:
    """JSON trié, compact — la forme CANONIQUE hachée (jamais la date ne
    dérive : le témoin ancré est FIGÉ, la date de vérification n'y entre
    pas)."""
    fige = {k: temoin[k] for k in ("magic", "epoque", "checksum",
                                   "empreinte_conteneur",
                                   "empreinte_chiffretexte", "p_idx")}
    return json.dumps(fige, sort_keys=True, separators=(",", ":")
                      ).encode("utf-8")


def empreinte_temoin(temoin: dict) -> str:
    return hashlib.sha256(canonique(temoin)).hexdigest()


# ---------------------------------------------------------------------------
# L'encodeur DER minimal (RFC 3161 — la TimeStampReq)
# ---------------------------------------------------------------------------

def _der_longueur(n: int) -> bytes:
    if n < 0x80:
        return bytes([n])
    corps = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(corps)]) + corps


def _der(tag: int, contenu: bytes) -> bytes:
    return bytes([tag]) + _der_longueur(len(contenu)) + contenu


def _der_entier(n: int) -> bytes:
    if n == 0:
        return _der(0x02, b"\x00")
    corps = n.to_bytes((n.bit_length() + 7) // 8, "big")
    if corps[0] & 0x80:
        corps = b"\x00" + corps
    return _der(0x02, corps)


def construire_requete_tsa(digest: bytes, nonce: int) -> bytes:
    """TimeStampReq (RFC 3161 § 3.1) — version 1, messageImprint =
    AlgorithmIdentifier(sha256, paramètres ABSENTS) ‖ digest, certReq
    FALSE (omis — DEFAULT FALSE), nonce."""
    alg_sha256 = _der(0x30, _der(0x06, bytes.fromhex("0609608648016503040201")))
    # ^ l'OID 2.16.840.1.101.3.4.2.1 (sha256) encodé — la forme complète
    #   DER de l'OID utilisé par les TSA réels (vérifiable au décodeur).
    message_imprint = _der(0x30, alg_sha256 + _der(0x04, digest))
    return _der(0x30, _der_entier(1) + message_imprint + _der_entier(nonce))


def empreinte_requete(requete_der: bytes) -> str:
    """La requête elle-même est hachable — la pièce reproductible."""
    return hashlib.sha256(requete_der).hexdigest()


# ---------------------------------------------------------------------------
# Le TSA de LABORATOIRE (clé de TEST — le réseau JAMAIS sans commande)
# ---------------------------------------------------------------------------

class TsaLabo:
    """« TSA de laboratoire » : signe le digest avec une clé Ed25519 de
    TEST. LE GAP NOMMÉ : la TSA réelle (réseau, certificat X.509, chaîne
    d'horodatage agréée) vit AU GESTE DU MAÎTRE — la structure de la
    preuve est identique, la source du temps ne l'est pas (l'horloge locale
    consignée n'est PAS un temps agréé — nommé au rapport). La vérification
    est cryptographique et locale : signature Ed25519 sur la charge
    (digest ‖ date ‖ nonce de la requête)."""

    def __init__(self):
        self._cle = Ed25519PrivateKey.generate()
        self.publique = self._cle.public_key()
        self.date = C._date_utc()          # l'horloge LOCALE du labo

    def repondre(self, digest: bytes, requete_der: bytes) -> dict:
        """La réponse de labo : signe (digest ‖ date ‖ nonce-extrait)."""
        nonce = requete_der[-8:]            # le dernier INTEGER de la req.
        signature = self._cle.sign(
            digest + self.date.encode("ascii") + nonce)
        return {"digest": digest.hex(), "date": self.date,
                "nonce": nonce.hex(), "signature": signature.hex()}

    @staticmethod
    def verifier(reponse: dict, publique: Ed25519PublicKey,
                 digest: bytes, requete_der: bytes) -> bool:
        """La vérification cryptographique LOCALE : signature Ed25519
        valide SUR LA CHARGE (digest ‖ date ‖ nonce de la requête) — un
        digest substitué, une date réécrite ou un nonce échangé ÉCHOUE."""
        try:
            publique.verify(
                bytes.fromhex(reponse["signature"]),
                bytes.fromhex(reponse["digest"])
                + reponse["date"].encode("ascii")
                + bytes.fromhex(reponse["nonce"]))
            return (reponse["digest"] == digest.hex()
                    and reponse["nonce"] == requete_der[-8:].hex())
        except Exception:
            return False


# ---------------------------------------------------------------------------
# Le Rekor de LABORATOIRE (l'entrée + la preuve d'inclusion vérifiée)
# ---------------------------------------------------------------------------

def _h(feuille: bytes) -> bytes:
    """La feuille Rekor : le préfixe 0x00 (RFC 6962 § 2.1) sur le corps."""
    return hashlib.sha256(b"\x00" + feuille).digest()


def _p(gauche: bytes, droite: bytes) -> bytes:
    """Le nœud interne : le préfixe 0x01 (RFC 6962 § 2.1)."""
    return hashlib.sha256(b"\x01" + gauche + droite).digest()


class RekorLabo:
    """« Journal de transparence de laboratoire » : un arbre de Merkle
    (RFC 6962 — les préfixes 0x00/0x01, le chemin des frères), la racine
    SIGNÉE (checksum signée — Ed25519 de test), la preuve d'inclusion
    rendue pour l'entrée. LE GAP NOMMÉ : l'entrée au rekor.sigstore.dev
    (réseau, la signed entry timestamp réelle, la vérification publique)
    vit AU GESTE DU MAÎTRE."""

    def __init__(self, n_feuilles: int = 3):
        self.entrees = [secrets.token_bytes(32)
                        for _ in range(max(1, n_feuilles))]
        self.cle = Ed25519PrivateKey.generate()
        self.publique = self.cle.public_key()

    def ancrer(self, corps_entree: bytes) -> dict:
        """L'entrée (le corps : le digest du témoin + l'époque) rejoint la
        FEUILLE suivante du journal ; retour {indice, racine, preuve,
        racine_signee, st_date}."""
        self.entrees.append(corps_entree)
        indice = len(self.entrees) - 1
        feuilles = [_h(e) for e in self.entrees]
        racine, preuve = _arbre_et_preuve(feuilles, indice)
        st_date = C._date_utc()
        racine_signee = self.cle.sign(racine + st_date.encode("ascii"))
        return {"indice": indice, "racine": racine.hex(),
                "preuve": [(f.hex(), pos) for f, pos in preuve],
                "racine_signee": racine_signee.hex(), "st_date": st_date,
                "n_entrees": len(self.entrees)}

    def verifier(self, corps_entree: bytes, ancrage: dict) -> bool:
        """LA PREUVE D'INCLUSION VÉRIFIÉE : la racine recalculée depuis la
        feuille + le chemin des frères == la racine signée, ET la signature
        Ed25519 de (racine ‖ st_date) valide."""
        try:
            feuille = _h(corps_entree)
            racine_calculee = feuille
            for (frere_hex, position) in ancrage["preuve"]:
                frere = bytes.fromhex(frere_hex)
                if position == "droite":
                    racine_calculee = _p(racine_calculee, frere)
                else:
                    racine_calculee = _p(frere, racine_calculee)
            if racine_calculee.hex() != ancrage["racine"]:
                return False
            self.publique.verify(
                bytes.fromhex(ancrage["racine_signee"]),
                racine_calculee + ancrage["st_date"].encode("ascii"))
            return True
        except Exception:
            return False


def _arbre_et_preuve(feuilles: list, indice: int):
    """L'arbre de Merkle et le chemin d'inclusion de la feuille `indice`
    (chaque étape : (hash du frère, position du frère))."""
    if len(feuilles) == 1:
        return feuilles[0], []
    if len(feuilles) % 2 == 1:
        feuilles = feuilles + [feuilles[-1]]     # RFC 6962 : duplication
    niveau = feuilles
    chemin = []
    courante = indice
    while len(niveau) > 1:
        paire = courante ^ 1
        if paire < len(niveau):
            chemin.append((niveau[paire],
                           "droite" if paire > courante else "gauche"))
        else:
            chemin.append((niveau[courante], "droite"))
        niveau = [_p(niveau[i], niveau[i + 1])
                  for i in range(0, len(niveau) - 1, 2)]
        courante //= 2
    return niveau[0], chemin


# ---------------------------------------------------------------------------
# LA VÉRIFICATION MACHINE — le timbre recoupé, la réécriture REFUSÉE
# ---------------------------------------------------------------------------

class RefusTemoin(RuntimeError):
    """Le REFUS NOMMÉ : le témoin ne recoupe PAS — réécriture détectée."""


def verifier_temoin(temoin_ancore: dict, conteneur_chemin: str) -> None:
    """Le recoupement : le témoin RECONSTRUIT depuis le conteneur sur
    disque doit être IDENTIQUE au témoin ancré (la canonique FIGÉE).
    TOUT écart = REFUS NOMMÉ (réécriture du témoin, substitution du
    conteneur, époque réécrite)."""
    reconstruit = construire_temoin(conteneur_chemin)
    for champ in ("epoque", "checksum", "empreinte_conteneur",
                  "empreinte_chiffretexte", "p_idx"):
        if str(temoin_ancore.get(champ)) != str(reconstruit[champ]):
            raise RefusTemoin(
                f"REFUS — le témoin ne recoupe PAS : champ « {champ} » "
                f"ancré {temoin_ancore.get(champ)!r} ≠ reconstruit "
                f"{reconstruit[champ]!r} — la RÉÉCRITURE du témoin (ou la "
                "substitution du conteneur) est REFUSÉE nommément "
                "(plan (f), la vérification machine)")
    if empreinte_temoin(temoin_ancore) != empreinte_temoin(reconstruit):
        raise RefusTemoin("REFUS — l'empreinte canonique du témoin diverge : "
                          "réécriture REFUSÉE (plan (f))")
