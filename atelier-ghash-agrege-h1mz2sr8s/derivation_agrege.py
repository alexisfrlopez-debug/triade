#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA DÉRIVATION du GHASH AGRÉGÉ 4 BLOCS — le simulateur du scellé tls13-17
(le juge ghash_juge du pilote v13 recopié TEL QUEL), la sémantique du twist
et de la réduction alg9 (le miroir exact du schoolbook v13, les couloirs
64 bits), la construction agrégée DÉRIVÉE (la table des puissances tordues
par le juge) et son contrôle contre QUATRE APPELS CHAÎNÉS au scellé ; plus
l'untwist du repli. Pièce de travail — PAS un livrable du plan."""
import random

M64 = (1 << 64) - 1
M128 = (1 << 128) - 1


# ---- le juge du pilote v13, recopié TEL QUEL ------------------------------
def rev128(v):
    r = 0
    for i in range(128):
        r |= ((v >> (127 - i)) & 1) << i
    return r


def clmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
    return r


def polymod(t):
    while t.bit_length() > 128:
        k = t.bit_length() - 129
        t ^= ((1 << 128) | 0x87) << k
    return t


def ghash_juge(NX, NY):
    return rev128(polymod(clmul(rev128(NX), rev128(NY))))


# ---- le simulateur EXACT du scellé (couloirs 64 bits) ----------------------
def lanes(v):
    return (v & M64, (v >> 64) & M64)


def join(lo, hi):
    return (lo & M64) | ((hi & M64) << 64)


def psllq(v, n):
    lo, hi = lanes(v)
    return join(lo << n, hi << n)


def psrlq(v, n):
    lo, hi = lanes(v)
    return join(lo >> n, hi >> n)


def pslldq8(v):
    lo, hi = lanes(v)
    return join(0, lo)


def psrldq8(v):
    lo, hi = lanes(v)
    return join(hi, 0)


CONST_C = (0xC200000000000000 << 64) | 1


def twist(v):
    """le twist SANS BRANCHE du scellé : v·x mod P̃."""
    carry127 = v >> 127
    w = psllq(v, 1)
    w |= pslldq8(psrlq(v, 63))
    if carry127:
        w ^= CONST_C
    return w & M128


CONST_C2 = 0xE1000000000000000000000000000000   # x^127+x^126+x^125+x^120


def untwist(w):
    """l'inverse du twist (le repli) : v = (w >> 1) ⊕ (w&1)·C2 — le miroir
    exact des instructions asm (psrlq/psrldq/psllq/por + le drapeau bit0 ->
    bit127 par pslldq/psllq/pshufd/pcmpgtd/pand/pxor). SANS BRANCHE."""
    lo, hi = lanes(w)
    porte = ((hi & 1) << 63)
    v = join((lo >> 1) | porte, hi >> 1)
    f = (w & 1) * CONST_C2
    return v ^ f


def alg9(P256):
    """la réduction alg9 PAR DÉCALAGES — le miroir exact du schoolbook v13."""
    A = P256 & M128
    B = (P256 >> 128) & M128
    xmm4 = A
    xmm5 = A
    xmm0 = psllq(A, 5)
    xmm5 ^= xmm0
    xmm0 = psllq(xmm0, 1)
    xmm0 ^= xmm5
    xmm0 = psllq(xmm0, 57)
    xmm5 = xmm0
    xmm0 = pslldq8(xmm0)
    xmm5b = psrldq8(xmm5)
    xmm0 ^= xmm4
    B ^= xmm5b
    xmm4 = xmm0
    xmm0 = psrlq(xmm0, 1)
    B ^= xmm4
    xmm4 ^= xmm0
    xmm0 = psrlq(xmm0, 5)
    xmm0 ^= xmm4
    xmm0 = psrlq(xmm0, 1)
    xmm0 ^= B
    return xmm0 & M128


def scelle_simu(NX, NH):
    """le scellé tls13-17 SIMULÉ (l'entier gros-boutiste en entrée et sortie)."""
    return alg9(clmul(NX, twist(NH)))


# ---- la construction agrégée DÉRIVÉE --------------------------------------
def table_tordue(NH):
    """la table des puissances tordues DÉRIVÉE par le juge :
    T_k = twist(N_{H^k}), k = 1..4 — JAMAIS devinée."""
    P1 = NH
    P2 = ghash_juge(NH, NH)
    P3 = ghash_juge(P2, NH)
    P4 = ghash_juge(P3, NH)
    return [twist(P1), twist(P2), twist(P3), twist(P4)]


def agrege_simu(X1, X2, X3, X4, table):
    """l'agrégé 4 blocs : quatre produits, l'accumulation 256 bits, UNE
    réduction alg9. X1..X4 : les entiers gros-boutistes ; table : [T1..T4]."""
    acc = 0
    for i, NXi in enumerate([X1, X2, X3, X4]):
        acc ^= clmul(NXi, table[3 - i])
    return alg9(acc)


def main():
    rng = random.Random(1234567)

    # (1) le scellé simulé == le juge (la convention d'octets corrigée)
    ok = 0
    for _ in range(64):
        X = rng.getrandbits(128)
        H = rng.getrandbits(128)
        Z = scelle_simu(X, H)
        ok += (Z == ghash_juge(X, H))
    print(f"(1) scellé simulé == juge : {ok}/64")

    # (2) l'untwist == l'inverse du twist
    ok = 0
    for _ in range(256):
        v0 = rng.getrandbits(128)
        ok += (untwist(twist(v0)) == v0)
    print(f"(2) untwist(twist(v)) == v : {ok}/256")

    # (3) L'AGRÉGÉ : quatre produits + UNE réduction alg9 == QUATRE chaînés
    ok = 0
    for _ in range(64):
        H = rng.getrandbits(128)
        Xs = [rng.getrandbits(128) for _ in range(4)]
        table = table_tordue(H)
        agg = agrege_simu(*Xs, table)
        # la référence : quatre appels chaînés au scellé
        Y = 0
        for Xi in Xs:
            Y = scelle_simu(Xi ^ Y, H)
        ok += (agg == Y)
    print(f"(3) l'agrégé == 4 chaînés au scellé : {ok}/64")

    # (4) l'agrégé avec l'accumulateur replié : agg(Y0 ⊕ b1, b2, b3, b4)
    #     == 4 chaînés PARTANT de Y0 — la composition GCM
    ok = 0
    for _ in range(64):
        H = rng.getrandbits(128)
        Y0 = rng.getrandbits(128)
        Bs = [rng.getrandbits(128) for _ in range(4)]
        table = table_tordue(H)
        agg = agrege_simu(Y0 ^ Bs[0], Bs[1], Bs[2], Bs[3], table)
        Y = Y0
        for b in Bs:
            Y = scelle_simu(b ^ Y, H)
        ok += (agg == Y)
    print(f"(4) l'agrégé replié == 4 chaînés partant de Y0 : {ok}/64")


if __name__ == "__main__":
    main()
