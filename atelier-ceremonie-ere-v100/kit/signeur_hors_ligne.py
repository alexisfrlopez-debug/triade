#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""signeur_hors_ligne.py — LE SIGNEUR HORS-LIGNE de la cérémonie d'ère (v100).

AUTOPORTEUR, À EXÉCUTER HORS LIGNE, SANS LE DÉPÔT — le cœur Ed25519 est la
RÉFÉRENCE de v06/ceremonie_hors_ligne.py (le RFC 8032 en Python pur,
l'arithmétique entière seule, les vecteurs § 7.1 attestés multi-sources) :
la cérémonie d'ère signe avec LA MÊME clé que le sceau de l'Intention (la
continuité de clé D163 — la clé qui signe les 14 arbres signe l'ère).

Ce script ne dépend de RIEN d'autre que Python 3.8+ standard (hashlib, os,
sys). Il n'accède JAMAIS au réseau, ne lit jamais le dépôt, ne demande
jamais pip. Copiez-le SEUL sur la machine hors ligne (ou la clef USB) : la
clé privée du maître n'entre jamais dans le bac à sable de l'assistant —
le contrat D87/D183 : LE LABORATOIRE NE SIGNE JAMAIS.

Chaque démarrage en mode signer/verifier passe l'AUTOTEST des vecteurs
RFC 8032 § 7.1 (TEST 1-3 + la mutation attrapée) : si l'autotest échoue,
le script REFUSE de signer (fail-closed — une cérémonie dont la
cryptographie est cassée ne produit rien).

LA COMPATIBILITÉ : la charge « nom balise empreinte » (trois champs) est
la MÊME forme que a-signer.txt du sceau — l'OUTIL DU MAÎTRE
(v06/ceremonie_hors_ligne.py, byte pour byte la référence) signe la charge
de l'ère TELLE QUELLE, sans adaptation. Le présent signeur est le même
outil porté au kit (l'autonomie : le maître peut ne porter que le kit).

MODES
  autotest                                 les vecteurs RFC 8032, rien d'autre
  generer                                  clé privée (0600) + clé publique
  signer A-SIGNER CLE-PRIVEE               -> signatures-I.txt (auto-vérifiée)
  verifier A-SIGNER SIGNATURES CLE-PUBLIQUE   re-vérification autonome
"""
import argparse
import hashlib
import os
import sys

# --- confort console Windows (accents français) ---------------------------
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ===========================================================================
# Ed25519 en Python pur — RFC 8032 (la RÉFÉRENCE de v06/ceremonie_hors_ligne.py,
# les constantes validées par les vecteurs TEST 1-3 de § 7.1)
# ===========================================================================
P = 2 ** 255 - 19
L = 2 ** 252 + 27742317777372353535851937790883648493
D = (-121665 * pow(121666, P - 2, P)) % P
SQRT_M1 = pow(2, (P - 1) // 4, P)
G = (15112221349535400772501151409588531511454012693041857206046113283949847762202,
     46316835694926478169428394003475163141307993866256225615783033603165251855960)


def _sha512(donnees):
    return hashlib.sha512(donnees).digest()


def _inv(x):
    return pow(x, P - 2, P)


def _pt_add(P1, P2):
    """Addition de points, coordonnées homogènes étendues (RFC 8032 § 5.1.4)."""
    X1, Y1, Z1, T1 = P1
    X2, Y2, Z2, T2 = P2
    A = (Y1 - X1) * (Y2 - X2) % P
    B = (Y1 + X1) * (Y2 + X2) % P
    C = 2 * T1 * D * T2 % P
    Ee = 2 * Z1 * Z2 % P
    E, F, Gg, H = B - A, Ee - C, Ee + C, B + A
    return (E * F % P, Gg * H % P, F * Gg % P, E * H % P)


def _pt_mul(s, point):
    """Multiplication scalaire (double-and-add ; s supposé dans [0, L))."""
    Q = (0, 1, 1, 0)
    Pp = point
    while s > 0:
        if s & 1:
            Q = _pt_add(Q, Pp)
        Pp = _pt_add(Pp, Pp)
        s >>= 1
    return Q


def _pt_compress(point):
    x, y, z, _ = point
    zi = _inv(z)
    x = x * zi % P
    y = y * zi % P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _pt_decompress(octets):
    y = int.from_bytes(octets, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    if y >= P:
        return None
    x2 = (y * y - 1) * _inv(D * y * y + 1) % P
    if x2 == 0:
        if sign:
            return None
        x = 0
    else:
        x = pow(x2, (P + 3) // 8, P)
        if (x * x - x2) % P != 0:
            x = x * SQRT_M1 % P
        if (x * x - x2) % P != 0:
            return None
        if (x & 1) != sign:
            x = P - x
    return (x, y, 1, x * y % P)


_G_EXT = (G[0], G[1], 1, G[0] * G[1] % P)


def _pt_equal(P1, P2):
    """Égalité projective : x1/z1 == x2/z2 ET y1/z1 == y2/z2."""
    x1, y1, z1, _ = P1
    x2, y2, z2, _ = P2
    return (x1 * z2 - x2 * z1) % P == 0 and (y1 * z2 - y2 * z1) % P == 0


def cle_publique_depuis_graine(graine):
    """Clé publique (32 octets) depuis la graine — RFC 8032 § 5.1.5."""
    h = _sha512(graine)
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return _pt_compress(_pt_mul(a, _G_EXT))


def signer_ed25519(graine, message):
    """Signature Ed25519 (64 octets) — RFC 8032 § 5.1.6."""
    h = _sha512(graine)
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    prefixe = h[32:]
    r = int.from_bytes(_sha512(prefixe + message), "little") % L
    R = _pt_compress(_pt_mul(r, _G_EXT))
    A = _pt_compress(_pt_mul(a, _G_EXT))
    k = int.from_bytes(_sha512(R + A + message), "little") % L
    s = (r + k * a) % L
    return R + int.to_bytes(s, 32, "little")


def verifier_ed25519(cle_publique, message, signature):
    """Vérification Ed25519 — RFC 8032 § 5.1.7. True ssi valide."""
    if len(cle_publique) != 32 or len(signature) != 64:
        return False
    A = _pt_decompress(cle_publique)
    if A is None:
        return False
    Rs = signature[:32]
    R = _pt_decompress(Rs)
    if R is None:
        return False
    s = int.from_bytes(signature[32:], "little")
    if s >= L:
        return False
    k = int.from_bytes(_sha512(Rs + cle_publique + message), "little") % L
    sG = _pt_mul(s, _G_EXT)
    kA = _pt_mul(k, A)
    return _pt_equal(sG, _pt_add(R, kA))


# ===========================================================================
# AUTOTEST — vecteurs RFC 8032 § 7.1 (TEST 1-3) + la mutation attrapée
# (la RÉFÉRENCE v06/ceremonie_hors_ligne.py, attestée multi-sources)
# ===========================================================================
VECTEURS_RFC8032 = [
    ("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60",
     "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a",
     "",
     "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555f"
     "b8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"),
    ("4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb",
     "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c",
     "72",
     "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da0"
     "85ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00"),
    ("c5aa8df43f9f837bedb7442f31dcb7b166d38535076f094b85ce3a2e0b4458f7",
     "fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025",
     "af82",
     "6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac1"
     "8ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a"),
]


def autotest():
    """True ssi les TROIS vecteurs RFC passent + la mutation est attrapée."""
    tout = True
    for indice, (graine_hex, pub_hex, msg_hex, sig_hex) in enumerate(
            VECTEURS_RFC8032, 1):
        graine = bytes.fromhex(graine_hex)
        message = bytes.fromhex(msg_hex)
        signature = bytes.fromhex(sig_hex)
        ok = (cle_publique_depuis_graine(graine).hex() == pub_hex
              and signer_ed25519(graine, message).hex() == sig_hex
              and verifier_ed25519(bytes.fromhex(pub_hex), message, signature)
              and not verifier_ed25519(bytes.fromhex(pub_hex), message, bytes(64)))
        print(f"  RFC 8032 TEST {indice} : "
              f"{'VERT' if ok else 'ECHEC'} (message {len(message)} octet(s))")
        tout = tout and ok
    graine, _, msg_hex, sig_hex = VECTEURS_RFC8032[1]
    message = bytes.fromhex(msg_hex)
    mauvaise = bytes([message[0] ^ 1]) + message[1:]
    mutation = not verifier_ed25519(bytes.fromhex(
        VECTEURS_RFC8032[1][1]), mauvaise, bytes.fromhex(sig_hex))
    print(f"  mutation un octet : {'ATTRAPÉE' if mutation else 'MANQUÉE'} "
          f"(la vérification doit rejeter)")
    return tout and mutation


# ===========================================================================
# Les modes de la cérémonie d'ère (les formes de v06 — la compatibilité)
# ===========================================================================
def lire_lignes_a_signer(chemin):
    """Lignes « nom balise empreinte » -> [(nom, balise, empreinte_hex)]."""
    entrees = []
    with open(chemin, "r", encoding="utf-8") as f:
        for numero, ligne in enumerate(f, 1):
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#"):
                continue
            morceaux = ligne.split()
            if (len(morceaux) != 3 or not _est_hex_min(morceaux[2], 64)):
                raise SystemExit(f"ECHEC : a-signer ligne {numero} malformée : "
                                 f"{ligne!r} (format « nom balise empreinte »)")
            entrees.append((morceaux[0], morceaux[1], morceaux[2]))
    if not entrees:
        raise SystemExit(f"ECHEC : {chemin} vide — rien à signer")
    return entrees


def _est_hex_min(s, n):
    return (len(s) == n and all(c in "0123456789abcdef" for c in s))


def _lire_hex_fichier(chemin, quoi, n):
    with open(chemin, "r", encoding="utf-8") as f:
        lignes = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    if not lignes:
        raise SystemExit(f"ECHEC : {chemin} vide ({quoi})")
    v = lignes[0]
    if not _est_hex_min(v, n * 2):
        raise SystemExit(f"ECHEC : {chemin} : {quoi} attendue à {n} octets hexadécimaux")
    return bytes.fromhex(v)


def lire_graine_privee(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        lignes = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    if not lignes:
        raise SystemExit(f"ECHEC : {chemin} vide (graine privée)")
    v = lignes[0]
    if not _est_hex_min(v, 64):
        raise SystemExit("ECHEC : la graine privée attend 32 octets hexadécimaux "
                         "(64 caractères)")
    return bytes.fromhex(v)


def mode_generer():
    if not autotest():
        raise SystemExit("ECHEC AUTOTEST : cérémonie refusée (fail-closed)")
    graine = os.urandom(32)
    publique = cle_publique_depuis_graine(graine)
    with open("cle-privee.txt", "w", encoding="utf-8") as f:
        f.write(
            "# TRIADE — clé privée (la cérémonie d'ère, la continuité D163)\n"
            "# Générée HORS LIGNE ; ne doit JAMAIS entrer dans le bac à sable\n"
            "# de l'assistant, ni être synchronisée, ni être commitée.\n"
            "#\n"
            "# GARDE : si vous possédez déjà la clé I du sceau (cle-I-privee.txt),\n"
            "# N'EN GÉNÉREZ PAS UNE NOUVELLE — l'ère se signe À LA MÊME CLÉ que le\n"
            "# sceau de l'Intention (la continuité de clé D163 : la clé qui signe\n"
            "# les 14 arbres signe l'ère). Utilisez votre clé existante.\n"
            "#\n"
            + graine.hex() + "\n")
    try:
        os.chmod("cle-privee.txt", 0o600)
    except OSError:
        pass
    with open("cle-publique.txt", "w", encoding="utf-8") as f:
        f.write(publique.hex() + "\n")
    print("\n[signeur] generer : clé créée (SEULEMENT si vous n'en avez aucune).")
    print("  cle-privee.txt   — LA garde (impression papier recommandée)")
    print("  cle-publique.txt — publique, sans risque")


def mode_signer(chemin_a_signer, chemin_privee):
    if not autotest():
        raise SystemExit("ECHEC AUTOTEST : cérémonie refusée (fail-closed)")
    graine = lire_graine_privee(chemin_privee)
    publique = cle_publique_depuis_graine(graine)
    entrees = lire_lignes_a_signer(chemin_a_signer)
    lignes = []
    for nom, balise, empreinte_hex in entrees:
        message = bytes.fromhex(empreinte_hex)
        signature = signer_ed25519(graine, message)
        if not verifier_ed25519(publique, message, signature):
            raise SystemExit(f"ECHEC : auto-vérification invalide pour {nom} — "
                             f"RIEN n'est écrit (cérémonie douteuse)")
        lignes.append(f"{nom} {balise} {signature.hex()}")
    with open("signatures-I.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print(f"\n[signeur] signer : {len(lignes)} signatures -> signatures-I.txt")
    print("  Chaque signature a été VÉRIFIÉe avec la clé publique avant écriture.")
    print("  Remettez signatures-I.txt au kit (le bouton « Vérifier la signature »).")


def mode_verifier(chemin_a_signer, chemin_signatures, chemin_publique):
    entrees = lire_lignes_a_signer(chemin_a_signer)
    with open(chemin_signatures, "r", encoding="utf-8") as f:
        lignes_sig = [l.strip() for l in f if l.strip()]
    publique = _lire_hex_fichier(chemin_publique, "clé publique", 32)
    if len(lignes_sig) != len(entrees):
        raise SystemExit(f"ECHEC : {len(lignes_sig)} signatures != {len(entrees)} lignes")
    tout = True
    for (nom, balise, emp_hex), ligne in zip(entrees, lignes_sig):
        morceaux = ligne.split()
        if len(morceaux) != 3 or morceaux[:2] != [nom, balise]:
            print(f"  [ROUGE] {nom} : la ligne de signature ne correspond pas")
            tout = False
            continue
        ok = verifier_ed25519(publique, bytes.fromhex(emp_hex),
                              bytes.fromhex(morceaux[2]))
        print(f"  [{'VERT' if ok else 'ROUGE'}] {nom} {balise}")
        tout = tout and ok
    print("\nVERDICT : " + ("TOUT VERT — les signatures de l'ère tiennent"
                           if tout else "ROUGE — une signature ne tient pas"))
    return tout


def main():
    a = argparse.ArgumentParser(description="le signeur hors-ligne de la cérémonie d'ère")
    a.add_argument("mode", choices=["autotest", "generer", "signer", "verifier"])
    a.add_argument("chemins", nargs="*", help="signer: A-SIGNER CLE-PRIVEE · "
                                               "verifier: A-SIGNER SIGNATURES CLE-PUBLIQUE")
    args = a.parse_args()
    if args.mode == "autotest":
        return 0 if autotest() else 3
    if args.mode == "generer":
        mode_generer()
        return 0
    if args.mode == "signer":
        if len(args.chemins) != 2:
            print("usage : signeur_hors_ligne.py signer A-SIGNER CLE-PRIVEE")
            return 2
        mode_signer(args.chemins[0], args.chemins[1])
        return 0
    if args.mode == "verifier":
        if len(args.chemins) != 3:
            print("usage : signeur_hors_ligne.py verifier A-SIGNER SIGNATURES CLE-PUBLIQUE")
            return 2
        return 0 if mode_verifier(args.chemins[0], args.chemins[1],
                                  args.chemins[2]) else 3


if __name__ == "__main__":
    sys.exit(main())
