#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — SONDE ERRATUM n° 5 (le CH record : 0x76 contre 0x72).

La doctrine du projet (l'erratum n° 4 : « la sonde AVANT l'artefact ») :
l'artefact scellé 1.0.0-dev.1 émet le vol ClientHello `16 03 03 00 76 ||
CH(114 o)` — l'octet de longueur du enregistrement revendique 118 octets
de corps alors que le vol n'en porte que 114 (le brouillon tls13-27 le
dit lui-même : « ÉMIS au socle (119 o : 5 + 114) »). Le harnais a
codifié le même octet (harnais_poignee.py :758 ch_rec = 16 03 03 00 76) —
machine et référence sont cohérentes ENTRE ELLES, mais un serveur réel
lit la longueur déclarée et attend 4 octets qui ne viennent jamais.

La sonde envoie LES DEUX vols à des serveurs TLS 1.3 réels et tranche
sur pièces : le vol 0x76 doit rester SANS RÉPONSE (l'interblocage), le
vol corrigé 0x72 doit recevoir le ServerHello.
"""

import hashlib
import os
import socket
import struct
import sys

# ---------------------------------------------------------------- le CH exact

def u16(x):
    return struct.pack(">H", x)

PRIVEE_CLIENT = bytes.fromhex(
    "49af42ba7f7994852d713ef2784bcbcaa7911de26adc5642cb634540e7ea5005")
PUBLIQUE_CLIENT = bytes.fromhex(
    "99381de560e4bd43d23d8e435a7dbafeb3c06e51c13cae4d5413691e529aaf2c")
ALEA = bytes.fromhex(
    "cb34ecb1e78163ba1c38c6dacb196a6dffa21a8d9912ec18a2ef6283024dece7")


def x25519_base(priv):
    """RFC 7748 § 5 — l'échelle de Montgomery (le clamp × le point 9)."""
    p = 2 ** 255 - 19
    def cswap(s, a, b):
        return (b, a) if s else (a, b)
    k = int.from_bytes(priv, "little")
    k &= (1 << 254) - 8
    k |= 1 << 254
    x1, (x2, z2, x3, z3) = 9, (1, 0, 0, 1)
    swap = 0
    for t in range(254, -1, -1):
        k_t = (k >> t) & 1
        swap ^= k_t
        x2, x3 = cswap(swap, x2, x3)
        z2, z3 = cswap(swap, z2, z3)
        swap = k_t
        a = (x2 + z2) % p
        aa = a * a % p
        b = (x2 - z2) % p
        bb = b * b % p
        e = (aa - bb) % p
        c = (x3 + z3) % p
        d = (x3 - z3) % p
        da = d * a % p
        cb = c * b % p
        x3 = (da + cb) ** 2 % p
        z3 = x1 * (da - cb) ** 2 % p
        x2 = aa * bb % p
        z2 = e * (aa + ((p + 1) // 4) * e) % p
    x2, x3 = cswap(swap, x2, x3)
    z2, z3 = cswap(swap, z2, z3)
    return (x2 * pow(z2, p - 2, p) % p).to_bytes(32, "little")


def construire_ch(alea, cle_publique):
    """La construction re-jouée du plan — 114 o FIXES (tls13-22 Q1)."""
    exts = (u16(0x002B) + u16(3) + bytes([2]) + u16(0x0304)
            + u16(0x000A) + u16(4) + u16(2) + u16(0x001D)
            + u16(0x000D) + u16(6) + u16(4) + u16(0x0804) + u16(0x0401)
            + u16(0x0033) + u16(38) + u16(36) + u16(0x001D)
            + u16(32) + cle_publique)
    corps = (u16(0x0303) + alea + bytes([0])
             + u16(2) + u16(0x1301) + bytes([1, 0]) + u16(len(exts)) + exts)
    ch = bytes([1]) + len(corps).to_bytes(3, "big") + corps
    assert len(ch) == 114, len(ch)
    assert ch[6:38] == alea and ch[82:114] == cle_publique
    return ch


CH = construire_ch(ALEA, PUBLIQUE_CLIENT)
VOL_076 = b"\x16\x03\x03\x00\x76" + CH     # l'octet de l'artefact scellé
VOL_072 = b"\x16\x03\x03\x00\x72" + CH     # l'octet corrigé (5 + 114)

# ---------------------------------------------------------------- la sonde

CIBLES = [
    "www.google.com",
    "api.github.com",
    "www.wikipedia.org",
    "www.cloudflare.com",
    "www.debian.org",
]

ALERTES = {
    0: "close_notify", 10: "unexpected_message", 40: "handshake_failure",
    42: "bad_certificate", 47: "illegal_parameter", 50: "decode_error",
    51: "decrypt_error", 80: "internal_error", 112: "unrecognised_name",
    120: "no_application_protocol", 100: "no_renegotiation",
}


def sonder(hote, vol, attente=8.0):
    """Envoie le vol, rend (nb_octets, 8 premiers octets hex, description)."""
    try:
        s = socket.create_connection((hote, 443), timeout=10)
    except OSError as e:
        return None, None, f"connexion impossible : {e}"
    try:
        s.sendall(vol)
        s.settimeout(attente)
        morceaux = b""
        try:
            while len(morceaux) < 5:
                m = s.recv(4096)
                if not m:
                    return len(morceaux), morceaux[:8].hex(), (
                        "RÀS — la demi-fin (le serveur a FERMÉ sans rien "
                        "servir)" if not morceaux else "fermeture")
                morceaux += m
        except socket.timeout:
            if not morceaux:
                return 0, None, "SILENCE — le serveur attend (l'interblocage)"
            return len(morceaux), morceaux[:8].hex(), "partiel puis silence"
        # 5 octets reçus : analysons le premier enregistrement
        ctype = morceaux[0]
        lng = int.from_bytes(morceaux[3:5], "big")
        if ctype == 0x16:
            return len(morceaux), morceaux[:8].hex(), (
                f"SERVERHELLO/POIGNÉE — type 22, longueur {lng} : LE serveur "
                "A RÉPONDU")
        if ctype == 0x15:
            # le corps arrive derrière : lisons-le pour l'alerte
            try:
                while len(morceaux) < 5 + lng:
                    m = s.recv(4096)
                    if not m:
                        break
                    morceaux += m
                desc = morceaux[5] if len(morceaux) > 5 else 0
                nom = ALERTES.get(desc, f"code {desc}")
                return len(morceaux), morceaux[:8].hex(), (
                    f"ALERTE TLS (niveau {morceaux[5] if len(morceaux)>5 else '?'}"
                    f" desc {desc} {nom})")
            except socket.timeout:
                return len(morceaux), morceaux[:8].hex(), "alerte (corps partiel)"
        return len(morceaux), morceaux[:8].hex(), f"type {ctype} inconnu"
    finally:
        s.close()


def main():
    print("SONDE ERRATUM n° 5 — le CH record de l'artefact 1.0.0-dev.1")
    print(f"  CH construit : {len(CH)} o, aléa @ +6, clé @ +82, "
          f"extensions {CH[45:47].hex()} (67)")
    print(f"  VOL 0x76 (l'artefact)  : {VOL_076[:5].hex()} + 114 o "
          f"= {len(VOL_076)} o — longueur DÉCLARÉE 118")
    print(f"  VOL 0x72 (le corrigé)  : {VOL_072[:5].hex()} + 114 o "
          f"= {len(VOL_072)} o — longueur DÉCLARÉE 114")
    print()
    for hote in CIBLES:
        for nom, vol in (("0x76 (l'artefact)", VOL_076),
                         ("0x72 (le corrigé)", VOL_072)):
            n, hexa, verdict = sonder(hote, vol)
            print(f"  {hote:22s} {nom:18s} → {verdict}"
                  + (f" [{n} o, tête {hexa}]" if hexa else ""))
        print()


if __name__ == "__main__":
    main()
