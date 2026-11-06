#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — SONDE CIBLE TERRAIN (le chantier (f), l'instrument du labo).

Un client TLS 1.3 de LABORATOIRE (cryptography — l'instrument du labo,
JAMAIS du kit) qui rejoue NOTRE offre scellée exacte (le CH minimal de
114 o, enregistrement corrigé 0x72) contre des serveurs réels, complète
la poignée ENTIÈRE (le calendrier, le Finished serveur VÉRIFIÉ, le
Finished client ÉMIS), puis :
  - EXTRAIT le certificat de l'entité servi (la PREMIÈRE entrée) → le
    candidat à l'ÉPINGLAGE (SHA-256 du DER) ;
  - ÉCHANGE la ligne applicative (le GET HTTP) → le témoin attendu ;
  - CONSIGNE le déroulé réel des enregistrements (tickets, alertes,
    close_notify) — la donnée de conception du kit.

Auto-test AVANT tout geste réseau : le calendrier de la référence
rejoué sur les pièces consignées RFC 8448 (le secret partagé 8bd4054f…,
la clé de poignée client b3eddb12…, le Finished serveur 9b9b141d…).
"""

import hashlib
import hmac
import os
import socket
import struct
import sys
import time

from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey, X25519PublicKey)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ---------------------------------------------------------------- notre offre

PRIVEE = bytes.fromhex(
    "49af42ba7f7994852d713ef2784bcbcaa7911de26adc5642cb634540e7ea5005")
PUBLIQUE = bytes.fromhex(
    "99381de560e4bd43d23d8e435a7dbafeb3c06e51c13cae4d5413691e529aaf2c")
SUITE_OK = 0x1301
GROUPE_OK = 0x001D

# les pièces consignées RFC 8448 (l'auto-test du calendrier)
SH_8448 = bytes.fromhex(
    "020000560303a6af06a4121860dc5e6e60249cd34c95930c8ac5cb1434dac155772e"
    "d3e2692800130100002e00330024001d0020c9828876112095fe66762bdbf7c672e1"
    "56d6cc253b833df1dd69b1b04e751f0f002b00020304")
PARTAGE_8448 = bytes.fromhex(
    "8bd4054fb55b9d63fdfbacf9f04b9f0d35e6d63f537563efd46272900f89492d")
C_HS_8448 = bytes.fromhex(
    "b3eddb126e067f35a780b3abf45e2d8f3b1a950738f52e9600746a0e27a55a21")
S_HS_8448 = bytes.fromhex(
    "b67b7d690cc16c4e75e54213cb2d37b4e9c912bcded9105d42befd59d391ad38")
C_AP_8448 = bytes.fromhex(
    "9e40646ce79a7f9dc05af8889bce6552875afa0b06df0087f792ebb7c17504a5")
S_AP_8448 = bytes.fromhex(
    "a11af9f05531f856ad47116b45a950328204b4f44bfb6b3a4b4f1f3fcb631643")
S_FIN_8448 = bytes.fromhex(
    "9b9b141d906337fbd2cbdce71df4deda4ab42c309572cb7fffee5454b78f0718")
EE_8448 = bytes.fromhex(
    "080000240022000a00140012001d00170018001901000101010201030104001c0002"
    "400100000000")
CERT_8448 = bytes.fromhex(
    "0b0001b9000001b50001b0308201ac30820115a003020102020102300d06092a8648"
    "86f70d01010b0500300e310c300a06035504031303727361301e170d313630373330"
    "3031323335395a170d3236303733303031323335395a300e310c300a060355040313"
    "0372736130819f300d06092a864886f70d010101050003818d0030818902818100b4"
    "bb498f8279303d980836399b36c6988c0c68de55e1bdb826d3901a2461eafd2de49a"
    "91d015abbc9a95137ace6c1af19eaa6af98c7ced43120998e187a80ee0ccb0524b1b"
    "018c3e0b63264d449a6d38e22a5fda430846748030530ef0461c8ca9d9efbfae8ea6"
    "d1d03e2bd193eff0ab9a8002c47428a6d35a8d88d79f7f1e3f0203010001a31a3018"
    "30090603551d1304023000300b0603551d0f0404030205a0300d06092a864886f70d"
    "01010b05000381810085aad2a0e5b9276b908c65f73a7267170618a54c5f8a7b337d"
    "2df7a594365417f2eae8f8a58c8f8172f9319cf36b7fd6c55b80f21a030151567260"
    "96fd335e5e67f2dbf102702e608ccae6bec1fc63a42a99be5c3eb7107c3c54e9b9eb"
    "2bd5203b1c3b84e0a8b2f759409ba3eac9d91d402dcc0cc8f8961229ac9187b42b4d"
    "e10000")
CV_8448 = bytes.fromhex(
    "0f000084080400805a747c5d88fa9bd2e55ab085a61015b7211f824cd484145ab3ff"
    "52f1fda8477b0b7abc90db78e2d33a5c141a078653fa6bef780c5ea248eeaaa785c4"
    "f394cab6d30bbe8d4859ee511f602957b15411ac027671459e46445c9ea58c181e81"
    "8e95b8c3fb0bf3278409d3be152a3da5043e063dda65cdf5aea20d53dfacd42f74f3")
ALEA_8448 = bytes.fromhex(
    "cb34ecb1e78163ba1c38c6dacb196a6dffa21a8d9912ec18a2ef6283024dece7")


def u16(x):
    return struct.pack(">H", x)


def construire_ch(alea, cle_publique):
    exts = (u16(0x002B) + u16(3) + bytes([2]) + u16(0x0304)
            + u16(0x000A) + u16(4) + u16(2) + u16(0x001D)
            + u16(0x000D) + u16(6) + u16(4) + u16(0x0804) + u16(0x0401)
            + u16(0x0033) + u16(38) + u16(36) + u16(0x001D)
            + u16(32) + cle_publique)
    corps = (u16(0x0303) + alea + bytes([0])
             + u16(2) + u16(0x1301) + bytes([1, 0]) + u16(len(exts)) + exts)
    ch = bytes([1]) + len(corps).to_bytes(3, "big") + corps
    assert len(ch) == 114
    return ch


# ---------------------------------------------------------------- le calendrier

def hkdf_extract(salt, ikm):
    return hmac.new(salt or b"\x00" * 32, ikm, hashlib.sha256).digest()


def expand_label(secret, libelle, contexte, n):
    info = (struct.pack(">H", n) + bytes([6 + len(libelle)])
            + b"tls13 " + libelle + bytes([len(contexte)]) + contexte)
    out, t, i = b"", b"", 1
    while len(out) < n:
        t = hmac.new(secret, t + info + bytes([i]), hashlib.sha256).digest()
        out += t
        i += 1
    return out[:n]


def derive_secret(secret, libelle, messages):
    return expand_label(secret, libelle, hashlib.sha256(messages).digest(), 32)


def calendrier(secret_partage, hash_ch_sh):
    """Le miroir exact de ref_Cadenas (le calendrier DU JALON)."""
    Z = b"\x00" * 32
    vide = hashlib.sha256(b"").digest()      # Hash("") — l'erratum n° 2
    early = hkdf_extract(Z, Z)
    derived = expand_label(early, b"derived", vide, 32)
    handshake = hkdf_extract(derived, secret_partage)
    c_hs = expand_label(handshake, b"c hs traffic", hash_ch_sh, 32)
    s_hs = expand_label(handshake, b"s hs traffic", hash_ch_sh, 32)
    return handshake, c_hs, s_hs


def application(handshake, hash_ch_fin):
    Z = b"\x00" * 32
    vide = hashlib.sha256(b"").digest()
    derived2 = expand_label(handshake, b"derived", vide, 32)
    master = hkdf_extract(derived2, Z)
    c_ap = expand_label(master, b"c ap traffic", hash_ch_fin, 32)
    s_ap = expand_label(master, b"s ap traffic", hash_ch_fin, 32)
    return c_ap, s_ap


def cle_finie(secret_trafic):
    return expand_label(secret_trafic, b"finished", b"", 32)


def iv_de(secret_trafic):
    return expand_label(secret_trafic, b"iv", b"", 12)


def cle_aes_de(secret_trafic):
    return expand_label(secret_trafic, b"key", b"", 16)


# ---------------------------------------------------------------- la lecture

class Flux:
    def __init__(self, sock):
        self.sock = sock
        self.tampon = b""
        self.journal = []

    def lire_enregistrement(self, attente=10.0):
        while len(self.tampon) < 5:
            self.sock.settimeout(attente)
            m = self.sock.recv(65536)
            if not m:
                raise EOFError("la demi-fin")
            self.tampon += m
        ctype = self.tampon[0]
        lng = int.from_bytes(self.tampon[3:5], "big")
        while len(self.tampon) < 5 + lng:
            m = self.sock.recv(65536)
            if not m:
                raise EOFError("enregistrement tronqué")
            self.tampon += m
        rec = self.tampon[5:5 + lng]
        self.tampon = self.tampon[5 + lng:]
        self.journal.append((ctype, lng))
        return ctype, rec


def deproteger(cle, iv, seq, ctype_rec, rec):
    nonce = bytes(iv[i] ^ ((seq >> (8 * (11 - i))) & 0xFF)
                  for i in range(12))
    aad = bytes([ctype_rec, 3, 3]) + len(rec).to_bytes(2, "big")
    clair = AESGCM(cle).decrypt(nonce, rec, aad)
    return clair[-1], clair[:-1]


def proteger(cle, iv, seq, type_interne, charge):
    clair = charge + bytes([type_interne])
    lng = len(clair) + 16
    nonce = bytes(iv[i] ^ ((seq >> (8 * (11 - i))) & 0xFF)
                  for i in range(12))
    aad = bytes([23, 3, 3]) + lng.to_bytes(2, "big")
    return bytes([23, 3, 3]) + lng.to_bytes(2, "big") + \
        AESGCM(cle).encrypt(nonce, clair, aad)


def marches_messages(charge):
    """La marche des messages de poignée d'un vol : [(type, corps)]."""
    out, pos = [], 0
    while pos + 4 <= len(charge):
        typ = charge[pos]
        lng = int.from_bytes(charge[pos + 1:pos + 4], "big")
        out.append((typ, charge[pos:pos + 4 + lng],
                    charge[pos + 4:pos + 4 + lng]))
        pos += 4 + lng
    return out


# ---------------------------------------------------------------- l'auto-test

def autotest():
    """Les hash DU RFC en ARGUMENTS, les secrets CONSIGNÉS du RFC en
    attendus — la méthode du harnais (les octets émis par la machine
    sont NOTRES ; la dérivation, elle, se recoupe sur les pièces
    officielles)."""
    hash_ch_sh = bytes.fromhex(
        "860c06edc07858ee8e78f0e7428c58edd6b43f2ca3e6e95f02ed063cf0e1cad8")
    hash_ch_cv = bytes.fromhex(
        "edb7725fa7a3473b031ec8ef65a2485493900138a2b91291407d7951a06110ed")
    hash_ch_fin = bytes.fromhex(
        "9608102a0f1ccc6db6250b7b7e417b1a000eaada3daae4777a7686c9ff83df13")
    handshake, c_hs, s_hs = calendrier(PARTAGE_8448, hash_ch_sh)
    ok = (c_hs == C_HS_8448 and s_hs == S_HS_8448)
    c_ap, s_ap = application(handshake, hash_ch_fin)
    ok = ok and c_ap == C_AP_8448 and s_ap == S_AP_8448
    attendu = hmac.new(cle_finie(s_hs), hash_ch_cv, hashlib.sha256).digest()
    ok = ok and attendu == S_FIN_8448
    # la construction re-jouée du CH (la nôtre) : le juge de structure
    ch = construire_ch(ALEA_8448, PUBLIQUE)
    ok = ok and len(ch) == 114 and ch[6:38] == ALEA_8448 \
        and ch[82:114] == PUBLIQUE
    if not ok:
        print("AUTO-TEST ROUGE — le calendrier de référence diverge")
        sys.exit(1)
    print("AUTO-TEST VERT — le calendrier rejoué sur les pièces RFC 8448 "
          "(c_hs, s_hs, c_ap, s_ap, le Finished serveur ; les hash du RFC "
          "en ARGUMENTS)")
    return ok


# ---------------------------------------------------------------- la sonde

def sonder(hote, attente_main=10.0):
    print(f"\n=== {hote} ===")
    s = socket.create_connection((hote, 443), timeout=10)
    flux = Flux(s)
    alea = os.urandom(32)

    # (1) le CH — NOTRE offre scellée, l'enregistrement corrigé 0x72
    ch = construire_ch(alea, PUBLIQUE)
    s.sendall(b"\x16\x03\x03\x00\x72" + ch)
    print("  CH émis (119 o, 0x72)")

    # (2) le ServerHello (une lecture, enregistrement 16 03 03 00 5A)
    while True:
        ctype, rec = flux.lire_enregistrement(attente_main)
        if ctype == 0x14:
            # le CCS hérité de compatibilité — RFC 8446 § 4.1.3 : IGNORÉ
            continue
        break
    if ctype != 0x16 or not rec or rec[0] != 2:
        print(f"  PAS de ServerHello (type {ctype}, "
              f"{rec[:6].hex() if rec else '?'})")
        s.close()
        return None
    assert rec[38] == 0, "l'écho session_id non vide"
    assert int.from_bytes(rec[39:41], "big") == SUITE_OK
    corps = rec[4:]
    i = 2 + 32 + 1 + 2 + 1 + 2
    fin = i + int.from_bytes(corps[i - 2:i], "big")
    partage_serveur = None
    while i < fin:
        ext = int.from_bytes(corps[i:i + 2], "big")
        lng = int.from_bytes(corps[i + 2:i + 4], "big")
        if ext == 0x0033:
            ce = corps[i + 4:i + 4 + lng]
            assert int.from_bytes(ce[0:2], "big") == GROUPE_OK
            klg = int.from_bytes(ce[2:4], "big")
            partage_serveur = ce[4:4 + klg]
        i += 4 + lng
    assert partage_serveur is not None
    print(f"  SH reçu : suite 1301, x25519, clé serveur "
          f"{partage_serveur[:8].hex()}…")

    # (3) le calendrier
    messages = ch + rec
    handshake, c_hs, s_hs = calendrier(
        X25519PrivateKey.from_private_bytes(PRIVEE).exchange(
            X25519PublicKey.from_public_bytes(partage_serveur)),
        hashlib.sha256(messages).digest())
    c_cle, s_cle = cle_aes_de(c_hs), cle_aes_de(s_hs)
    c_hs_iv, s_hs_iv = iv_de(c_hs), iv_de(s_hs)

    # (4) le vol serveur déverrouillé : EE/Cert/CV/Fin — RÉASSEMBLAGE par
    #     le flux (les messages de poignée FRAGMENTENT les enregistrements)
    seq_s = 0
    messages_s = b""
    tampon_v = b""
    certificat = None
    fin_serveur = None
    while fin_serveur is None:
        ctype, rec = flux.lire_enregistrement(attente_main)
        if ctype == 0x14:
            # le CCS hérité — RFC 8446 § 4.1.3 : IGNORÉ pendant la poignée
            continue
        assert ctype != 0x16, "la poignée en clair inattendue"
        interieur, charge = deproteger(s_cle, s_hs_iv, seq_s, ctype, rec)
        seq_s += 1
        tampon_v += charge
        while fin_serveur is None and len(tampon_v) >= 4:
            lng = int.from_bytes(tampon_v[1:4], "big")
            if len(tampon_v) < 4 + lng:
                break                       # le message attend la suite
            typ = tampon_v[0]
            msg = tampon_v[:4 + lng]
            tampon_v = tampon_v[4 + lng:]
            if typ == 0x14:
                fin_serveur = (msg, msg[4:])
            else:
                messages_s += msg           # ABSORBÉ (charte § 4)
                if typ == 0x0B and certificat is None:
                    corps_m = msg[4:]
                    # Certificate § 4.4.2 : ctx u8 puis liste u24 puis
                    # l'entrée : le DER à l'offset message 11 (le DÉTROIT
                    # de tls13-26 — DER_8448 = CERT_8448[11:11+432])
                    entree_lng = int.from_bytes(corps_m[4:7], "big")
                    certificat = corps_m[7:7 + entree_lng]
                    assert len(certificat) == entree_lng
    messages += messages_s
    attendu = hmac.new(cle_finie(s_hs),
                       hashlib.sha256(messages).digest(),
                       hashlib.sha256).digest()
    ok_fin = hmac.compare_digest(attendu, fin_serveur[1])
    messages += fin_serveur[0]
    c_ap, s_ap = application(handshake, hashlib.sha256(messages).digest())
    c_ap_cle, s_ap_cle = cle_aes_de(c_ap), cle_aes_de(s_ap)
    c_ap_iv, s_ap_iv = iv_de(c_ap), iv_de(s_ap)
    print(f"  le certificat servi : {len(certificat)} o DER ; "
          f"Finished serveur VÉRIFIÉ : {ok_fin}")

    # (5) le Finished client ÉMIS (sous la chaîne de POIGNÉE client)
    fin_c = hmac.new(cle_finie(c_hs), hashlib.sha256(messages).digest(),
                     hashlib.sha256).digest()
    msg_fin_c = bytes([0x14, 0, 0, 0x20]) + fin_c
    seq_c = 0
    s.sendall(proteger(c_cle, c_hs_iv, seq_c, 22, msg_fin_c))
    seq_c += 1
    print("  le Finished client émis")

    # (6) LA LIGNE APPLICATIVE : le GET (la séquence REPART À ZÉRO sous
    #     les nouvelles clés — RFC 8446 § 5.3, le miroir de la machine)
    ligne = (f"GET / HTTP/1.1\r\nHost: {hote}\r\n"
             f"User-Agent: TRIADE-M9-sonde\r\nConnection: close\r\n\r\n"
             ).encode()
    s.sendall(proteger(c_ap_cle, c_ap_iv, 0, 23, ligne))
    print(f"  la ligne applicative émise ({len(ligne)} o)")

    # (7) la réception : tickets, réponse, close_notify (séquence ZÉRO)
    reponse = b""
    tickets = 0
    alertes = []
    close_vu = False
    seq_ap_s = 0
    try:
        for _ in range(40):
            ctype, rec = flux.lire_enregistrement(12.0)
            if ctype == 0x16:
                alertes.append(("clair", ctype))
                continue
            interieur, charge = deproteger(s_ap_cle, s_ap_iv, seq_ap_s, ctype, rec)
            seq_ap_s += 1
            if interieur == 22:
                tickets += 1
            elif interieur == 23:
                reponse += charge
            elif interieur == 21:
                alertes.append(charge[:2].hex())
                if charge[:2] == b"\x01\x00":
                    close_vu = True
                    break
    except (EOFError, socket.timeout):
        pass

    # le close_notify du client (la séquence APPLICATIVE du client)
    if not close_vu:
        try:
            s.sendall(proteger(c_ap_cle, c_ap_iv, 1, 21, b"\x01\x00"))
        except OSError:
            pass
    s.close()

    statut = reponse.split(b"\r\n")[0] if reponse else b"(rien)"
    empreinte = hashlib.sha256(certificat).hexdigest()
    print(f"  tickets reçus : {tickets} ; close_notify : {close_vu} ; "
          f"alertes : {alertes}")
    print(f"  RÉPONSE : {statut!r} ({len(reponse)} o au total)")
    print(f"  EMPREINTE DU CERTIFICAT : {empreinte}")
    return {
        "hote": hote, "cert_der_len": len(certificat), "empreinte": empreinte,
        "cert_der": certificat, "tickets": tickets, "close": close_vu,
        "statut": statut.decode(errors="replace"),
        "reponse_octets": len(reponse), "fin_serveur_ok": ok_fin,
    }


CIBLES = ["www.google.com", "api.github.com", "www.cloudflare.com",
          "www.debian.org"]


def main():
    autotest()
    rapports = {}
    for hote in CIBLES:
        try:
            rapports[hote] = sonder(hote)
        except Exception as e:
            print(f"  ÉCHEC : {type(e).__name__}: {e}")
            rapports[hote] = None
    print("\n================ RÉCAPITULATIF =================")
    for hote, r in rapports.items():
        if r:
            print(f"  {hote:22s} cert {r['cert_der_len']:5d} o, empreinte "
                  f"{r['empreinte'][:16]}…, statut « {r['statut'][:40]} », "
                  f"tickets {r['tickets']}, close {r['close']}")
        else:
            print(f"  {hote:22s} ÉCHEC")


if __name__ == "__main__":
    main()
