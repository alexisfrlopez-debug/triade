#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fido2_hmac_secret.py — LE PROTOTYPE FIDO2 HMAC-SECRET EN LABORATOIRE
(l'atelier coffre-vr9n3s3l7, plan (g) : le média).

LE MODÈLE DU PROTOCOLE, SIMULÉ EN LABORATOIRE (les clés de TEST — le
token physique AU GESTE DU MAÎTRE, le gap NOMMÉ) : l'extension CTAP2
« hmac-secret » — la médiation FIDO2 :

  - À LA CRÉATION DE LA PREUVE D'IDENTITÉ (makeCredential + l'extension
    hmac-secret) : l'authentificateur TIRE une graine par preuve
    d'identité (« credSecret », 32 o CSPRNG) — ELLE NE SORT JAMAIS du
    token (la propriété fondatrice : le facteur possession vit dans le
    médiateur, il n'est ni exportable ni dérivable ailleurs) ;
  - À L'ACTE (getAssertion + hmac-secret) : la plateforme et le token
    montent un accord ECDH P-256 (le « sharedSecret » du protocole
    CTAP2/pinUvAuthProtocol1) ; la plateforme chiffre les SELS en
    AES-256-CBC sous ce secret et les authentifie par
    saltAuth = HMAC-SHA256(sharedSecret, saltEnc)[:16] ; le token
    VÉRIFIE saltAuth, DÉCHIFFRE les sels, puis DÉRIVE :
        output1 = HMAC-SHA256(credSecret, salt1)          [32 o]
        output2 = HMAC-SHA256(output1, salt2)  si salt2    [32 o]
    et REND output1 ‖ output2 CHIFFRÉS en AES-256-CBC sous le même
    sharedSecret ;
  - la plateforme DÉCHIFFRE : la valeur dérivée par le token est
    reproductible À VOLONTÉ pour le MÊME couple (preuve d'identité,
    sel) — c'est le modèle de dérivation conforme CTAP2 (les vecteurs
    « RFC 8236-style » : les clés dérivées re-productibles).

L'INTÉGRATION AU COFFRE, SPÉCIFIÉE (le média du piège FIDO2 — la
cérémonie, le contrat) :

  - LE RÔLE : le token EST le média du piège (plan (g) : « le média ») —
    la valeur V_piège de l'item (b) devient UNE DÉRIVATION HMAC-SECRET :
        salt1 = « TRIADE-piege » ‖ époque_le64
        V_piège(époque) = output1[:16]  (la TRONCATURE 16 o, la taille
                                        de V_piège du conteneur LCF3)
    la graine par preuve d'identité joue S_piège : elle vit DANS le
    token, JAMAIS sur la machine, JAMAIS exportable — la moitié
    « possession » de la serrure LCF3 ;
  - LA CÉRÉMONIE (l'enrôlement) : makeCredential + extension — le
    credentialId est inscrit À L'EN-TÊTE CLAIR du conteneur (l'AAD le
    couvre), le pin/UV établi ; le token est ensuite DÉBRANCHÉ (le
    média du piège, hors machine — miroir spec CF3 § 4 : un média par
    coffre) ;
  - LE CONTRAT À CHAQUE ACTE : la sentinelle exige la valeur dérivée à
    l'ÉPOQUE courante (b) — le sel PORTE l'époque, l'époque retirée est
    refusée (anti-rollback) ; la PREUVE DE PRÉSENCE (le toucher du
    token) borne l'acte dans le temps (le médiateur ne répond qu'au
    doigt — un vol du token à distance ne teste RIEN) ;
  - LA RELÈVE : la perte du token ne perd PAS le coffre — la phrase +
    le séquestre 5/3 (d) demeurent la relève ; le ré-enrôlement est
    une cérémonie de re-scellement à époque+1.

LE GAP NOMMÉ : le token physique (l'achat, le toucher réel, le
firmware CTAP2 réel) AU GESTE DU MAÎTRE — le prototype livré, jamais
l'achat simulé.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import PublicFormat

SALT_CTX = b"TRIADE-piege"        # le domaine de dérivation du piège


def _pad_pkcs7(donnees: bytes) -> bytes:
    n = 16 - (len(donnees) % 16)
    return donnees + bytes([n]) * n


def _unpad_pkcs7(donnees: bytes) -> bytes:
    n = donnees[-1]
    if not 1 <= n <= 16 or donnees[-n:] != bytes([n]) * n:
        raise ValueError("padding invalide")
    return donnees[:-n]


def _aes_cbc(cle: bytes, iv: bytes, clair: bytes, chiffrer: bool) -> bytes:
    cipher = Cipher(algorithms.AES(cle), modes.CBC(iv))
    op = cipher.encryptor() if chiffrer else cipher.decryptor()
    return op.update(clair) + op.finalize()


class AuthentificateurLabo:
    """« Le token de laboratoire » — SIMULÉ (nommé) : les graines par
    preuve d'identité vivent dans un fichier d'état de labo ; ELLES NE
    SONT JAMAIS RENDUES par l'interface (seules les valeurs DÉRIVÉES
    sortent, et chiffrées sous le sharedSecret)."""

    def __init__(self, fichier_etat: str):
        self.fichier = fichier_etat
        self.cle_echange = ec.generate_private_key(ec.SECP256R1())
        if os.path.isfile(fichier_etat):
            with open(fichier_etat, "r", encoding="utf-8") as f:
                self.graines = json.load(f)
        else:
            self.graines = {}

    def cle_publique_octets(self) -> bytes:
        enc, fmt = serialization_encoding_raw()
        return self.cle_echange.public_key().public_bytes(enc, fmt)

    def make_credential(self, cred_id: str) -> str:
        """L'enrôlement : la graine TIRÉE au CSPRNG, CONSIGNÉE dans l'état
        du token, JAMAIS rendue."""
        if cred_id in self.graines:
            raise ValueError("credentialId déjà enrôlé")
        self.graines[cred_id] = secrets.token_hex(32)
        with open(self.fichier, "w", encoding="utf-8") as f:
            json.dump(self.graines, f)
        return cred_id

    def _graine(self, cred_id: str) -> bytes:
        if cred_id not in self.graines:
            raise KeyError("credentialId INCONNU au token — refus nommé")
        return bytes.fromhex(self.graines[cred_id])

    def get_hmac_secret(self, cred_id: str, cle_pub_plateforme,
                         salt_enc: bytes, salt_auth: bytes,
                         iv: bytes) -> bytes:
        """L'ACTE : ECDH (la clé publique de la PLATEFORME) → vérification
        saltAuth → dérivation → réponse chiffrée. Le toucher (la preuve de
        présence) est SIMULÉ par l'appel même (nommé : le toucher réel vit
        au token physique)."""
        partage = self.cle_echange.exchange(ec.ECDH(), cle_pub_plateforme)
        shared = hashlib.sha256(partage).digest()   # pinUvAuthProtocol1
        if not hmac.compare_digest(
                hmac.new(shared, salt_enc, hashlib.sha256).digest()[:16],
                salt_auth):
            raise ValueError("saltAuth INVALIDE — le token REFUSE (CTAP2 : "
                             "l'authenticité des sels exigée)")
        sels = _unpad_pkcs7(_aes_cbc(shared, iv, salt_enc, False))
        salt1 = sels[:32]
        salt2 = sels[32:64] if len(sels) >= 64 else None
        graine = self._graine(cred_id)
        sortie = hmac.new(graine, salt1, hashlib.sha256).digest()
        if salt2 is not None:
            sortie += hmac.new(sortie, salt2, hashlib.sha256).digest()
        return _aes_cbc(shared, iv, _pad_pkcs7(sortie), True)


def serialization_encoding_raw():
    return serialization.Encoding.X962, PublicFormat.UncompressedPoint


class PlateformeLabo:
    """« La plateforme de laboratoire » (le coffre) : monte l'accord, forge
    la requête hmac-secret, DÉCHIFFRE la réponse — la valeur dérivée."""

    def __init__(self):
        self.cle = ec.generate_private_key(ec.SECP256R1())

    def cle_publique(self):
        return self.cle.public_key()

    def cle_publique_octets(self) -> bytes:
        enc, fmt = serialization_encoding_raw()
        return self.cle.public_key().public_bytes(enc, fmt)

    def derive(self, token: AuthentificateurLabo, cred_id: str,
               salt1: bytes, salt2: bytes = None) -> bytes:
        """La valeur dérivée par le token (le modèle CTAP2 complet, en
        laboratoire) : output1 ‖ (output2 si salt2)."""
        if len(salt1) != 32:
            raise ValueError("salt1 = 32 o (CTAP2 hmac-secret)")
        sels = salt1 + (salt2 if salt2 is not None else b"")
        partage = self.cle.exchange(ec.ECDH(), token.cle_echange.public_key())
        shared = hashlib.sha256(partage).digest()
        iv = secrets.token_bytes(16)
        salt_enc = _aes_cbc(shared, iv, _pad_pkcs7(sels), True)
        salt_auth = hmac.new(shared, salt_enc, hashlib.sha256).digest()[:16]
        reponse = token.get_hmac_secret(cred_id, self.cle_publique(),
                                        salt_enc, salt_auth, iv)
        sortie = _unpad_pkcs7(_aes_cbc(shared, iv, reponse, False))
        return sortie


# ---------------------------------------------------------------------------
# L'intégration au coffre LCF3 : V_piège DÉRIVÉE PAR LE TOKEN (le contrat)
# ---------------------------------------------------------------------------

def sel_piege(epoque: int) -> bytes:
    """salt1 = « TRIADE-piege » ‖ époque_le64 — LE SEL PORTE L'ÉPOQUE
    (l'anti-rollback (b) vit dans le sel : l'époque retirée dérive une
    valeur différente, le conteneur ne la vérifie pas)."""
    return SALT_CTX + int(epoque).to_bytes(8, "little")


def v_piege_fido2(token: AuthentificateurLabo, plateforme: PlateformeLabo,
                  cred_id: str, epoque: int) -> bytes:
    """V_piège(époque) = output1[:16] — la valeur de vérification du
    conteneur LCF3 DÉRIVÉE PAR LE TOKEN à l'époque courante (le contrat
    du média du piège FIDO2, plan (g) : la cérémonie et le contrat)."""
    sortie = plateforme.derive(token, cred_id, sel_piege(epoque))
    return sortie[:16]
