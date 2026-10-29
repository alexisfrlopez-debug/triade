#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ceremonie_hors_ligne.py — TRIADE v0.6.0 axe 3 (D87) : le sceau de l'Intention.

CÉRÉMONIE DE LA CLÉ I — AUTOPORTEUR, À EXÉCUTER HORS LIGNE, SANS LE DÉPÔT.

Ce script ne dépend de RIEN d'autre que Python 3.8+ standard (hashlib, os,
sys, argparse). Il n'accède JAMAIS au réseau, ne lit jamais le dépôt, et ne
demande jamais pip. Copiez-le seul sur une machine hors ligne (ou une clef
USB) : c'est le point — la clé de l'Intention naît hors du bac à sable de
l'assistant et n'y entre jamais (discipline D30/D87).

L'implémentation Ed25519 ci-dessous est le référence RFC 8032 en Python pur
(arithmétique entière seule). Chaque démarrage en mode generer/signer passe
l'AUTOTEST des vecteurs RFC 8032 § 7.1 (TEST 1-3) : si l'autotest échoue, le
script REFUSE de signer (fail-closed — une cérémonie dont la cryptographie
est cassée ne produit rien). Les vecteurs sont eux-mêmes attestés par
l'implémentation auditée « cryptography » côté dépôt (test_sceau_I.py T1).

MODES
  autotest                          vecteurs RFC 8032, rien d'autre
  generer                           clé I privée (0600) + clé publique
  signer A-SIGNER CLE-PRIVEE        -> signatures-I.txt (vérifiées avant
                                      écriture : une cérémonie douteuse
                                      n'écrit rien)
  verifier A-SIGNER SIGNATURES CLE  re-vérification autonome d'une remise

FLUX AIR-GAP COMPLET (mode d'emploi pas à pas) :
  1. Côté dépôt (machine connectée) :
         python3 v06/sceau_I.py preparer
     -> v06/sceau-I/a-signer.txt  (une ligne par arbre d'intention :
        « arbre balise empreinte », quelques lignes hexadécimales —
        imprimables sur papier).
  2. Transportez a-signer.txt vers la machine hors ligne (papier, clef USB).
  3. Hors ligne, UNE FOIS (première cérémonie) :
         python3 ceremonie_hors_ligne.py generer
     -> cle-I-privee.txt (LA garde : impression papier recommandée —
        64 caractères hexadécimaux) et cle-publique-I.txt (publique).
  4. Hors ligne, à chaque remise :
         python3 ceremonie_hors_ligne.py signer a-signer.txt cle-I-privee.txt
     -> signatures-I.txt.
  5. Transportez cle-publique-I.txt (première fois) et signatures-I.txt
     vers le dépôt, puis côté dépôt :
         python3 v06/sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt
     (les rotations suivantes re-signent SANS --cle : la clé ne bouge plus).
  6. Côté dépôt : python3 v06/sceau_I.py verifier  (tout doit être vert).

LA CLÉ PRIVÉE NE TRAVERSE JAMAIS LE BAC À SABLE. Si un assistant, un
synchro ou un script demande ce fichier : refus, c'est le contrat D87.
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
# Ed25519 en Python pur — RFC 8032 (toutes les constantes validées par les
# vecteurs TEST 1-3 de § 7.1, attestés multi-sources + implémentation auditée)
# ===========================================================================

P = 2 ** 255 - 19                                   # corps premier
L = 2 ** 252 + 27742317777372353535851937790883648493   # ordre du point de base
D = (-121665 * pow(121666, P - 2, P)) % P           # paramètre de courbe
SQRT_M1 = pow(2, (P - 1) // 4, P)                   # racine de -1
G = (15112221349535400772501151409588531511454012693041857206046113283949847762202,
     46316835694926478169428394003475163141307993866256225615783033603165251855960)  # base


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
    Q = (0, 1, 1, 0)                                # élément neutre
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
    """Clé publique (32 octets) depuis la graine (32 octets) — RFC 8032 § 5.1.5."""
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
# AUTOTEST — vecteurs RFC 8032 § 7.1 (TEST 1-3), attestés multi-sources et
# contre l'implémentation auditée « cryptography » (v06/test_sceau_I.py T1).
# ===========================================================================

VECTEURS_RFC8032 = [
    # (graine, clé publique, message, signature)
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
    """True ssi les TROIS vecteurs RFC passent (clé, signature, vérification)."""
    tout = True
    for indice, (graine_hex, pub_hex, msg_hex, sig_hex) in enumerate(
            VECTEURS_RFC8032, 1):
        graine = bytes.fromhex(graine_hex)
        message = bytes.fromhex(msg_hex)
        signature = bytes.fromhex(sig_hex)
        publique_calculee = cle_publique_depuis_graine(graine)
        signature_calculee = signer_ed25519(graine, message)
        ok = (publique_calculee.hex() == pub_hex
              and signature_calculee.hex() == sig_hex
              and verifier_ed25519(bytes.fromhex(pub_hex), message, signature)
              and not verifier_ed25519(bytes.fromhex(pub_hex), message,
                                       bytes(64)))
        print(f"  RFC 8032 TEST {indice} : "
              f"{'VERT' if ok else 'ECHEC'} (message {len(message)} octet(s))")
        tout = tout and ok
    # Mutation ciblée : un octet de message changé => signature invalide
    graine, _, msg_hex, sig_hex = VECTEURS_RFC8032[1]
    message = bytes.fromhex(msg_hex)
    mauvaise = bytes([message[0] ^ 1]) + message[1:]
    mutation = not verifier_ed25519(bytes.fromhex(
        VECTEURS_RFC8032[1][1]), mauvaise, bytes.fromhex(sig_hex))
    print(f"  mutation un octet : {'ATTRAPÉE' if mutation else 'MANQUÉE'} "
          f"(la vérification doit rejeter)")
    return tout and mutation


# ===========================================================================
# Formats de fichiers (v06/I/README.md § 4-5)
# ===========================================================================

HEX_MIN = set("0123456789abcdef")


def _est_hex_min(texte, taille):
    return (len(texte) == taille and all(c in HEX_MIN for c in texte))


def lire_graine_privee(chemin):
    """Extrait la graine (64 hex minuscules) de cle-I-privee.txt."""
    with open(chemin, "r", encoding="utf-8") as f:
        lignes = f.read().splitlines()
    for ligne in lignes:
        cand = ligne.strip()
        if _est_hex_min(cand, 64):
            return bytes.fromhex(cand)
    raise SystemExit(f"ECHEC : aucune graine (64 hex minuscules) lisible "
                     f"dans {chemin}")


def lire_hex_fichier(chemin, quoi, taille):
    with open(chemin, "r", encoding="utf-8") as f:
        texte = f.read().strip()
    if not _est_hex_min(texte, taille * 2):
        raise SystemExit(f"ECHEC : {quoi} malformé dans {chemin} "
                         f"({taille * 2} hexadécimaux minuscules attendus)")
    return bytes.fromhex(texte)


def lire_lignes_a_signer(chemin):
    """Lignes « arbre balise empreinte » -> [(arbre, balise, empreinte_bytes)]."""
    entrees = []
    with open(chemin, "r", encoding="utf-8") as f:
        for numero, ligne in enumerate(f, 1):
            ligne = ligne.strip()
            if not ligne:
                continue
            morceaux = ligne.split()
            if (len(morceaux) != 3 or not _est_hex_min(morceaux[2], 64)):
                raise SystemExit(f"ECHEC : a-signer ligne {numero} malformée : "
                                 f"{ligne!r} (format « arbre balise empreinte »)")
            entrees.append((morceaux[0], morceaux[1], morceaux[2]))
    if not entrees:
        raise SystemExit(f"ECHEC : {chemin} vide — rien à signer")
    return entrees


# ===========================================================================
# Modes de cérémonie
# ===========================================================================

def mode_generer():
    if not autotest():
        raise SystemExit("ECHEC AUTOTEST : cérémonie refusée (fail-closed)")
    graine = os.urandom(32)
    publique = cle_publique_depuis_graine(graine)
    with open("cle-I-privee.txt", "w", encoding="utf-8") as f:
        f.write(
            "# TRIADE — clé I PRIVÉE (sceau de l'Intention, D87)\n"
            "# Générée HORS LIGNE ; ne doit JAMAIS entrer dans le bac à sable\n"
            "# de l'assistant, ni être synchronisée, ni être commitée.\n"
            "#\n"
            "# GARDE : imprimez la ligne de 64 caractères ci-dessous, conservez\n"
            "# le papier en lieu sûr (deux copies, deux lieux). Une graine perdue\n"
            "# = toute évolution future de l'intention devient impossible ; une\n"
            "# graine volée = la souveraineté est morte. Détruisez ce fichier\n"
            "# après copie papier, ou conservez-le chiffré sur le média dédié.\n"
            "#\n"
            + graine.hex() + "\n")
    try:
        os.chmod("cle-I-privee.txt", 0o600)
    except OSError:
        pass  # Windows : attributs ACL, le fichier reste privé par posture
    with open("cle-publique-I.txt", "w", encoding="utf-8") as f:
        f.write(publique.hex() + "\n")
    print("\n[ceremonie] generer : clé I créée.")
    print("  cle-I-privee.txt   — LA garde (voir l'en-tête du fichier : "
          "impression papier recommandée)")
    print("  cle-publique-I.txt — à remettre au dépôt (publique, sans risque)")
    print("  La graine ne s'affiche JAMAIS ici : le fichier est la remise.")


def mode_signer(chemin_a_signer, chemin_privee):
    if not autotest():
        raise SystemExit("ECHEC AUTOTEST : cérémonie refusée (fail-closed)")
    graine = lire_graine_privee(chemin_privee)
    publique = cle_publique_depuis_graine(graine)
    entrees = lire_lignes_a_signer(chemin_a_signer)
    lignes = []
    for arbre, balise, empreinte_hex in entrees:
        message = bytes.fromhex(empreinte_hex)
        signature = signer_ed25519(graine, message)
        if not verifier_ed25519(publique, message, signature):
            raise SystemExit(
                f"ECHEC : signature auto-vérification invalide pour {arbre} — "
                f"RIEN n'est écrit (cérémonie douteuse, spec § 4)")
        lignes.append(f"{arbre} {balise} {signature.hex()}")
    with open("signatures-I.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print(f"\n[ceremonie] signer : {len(lignes)} signatures -> signatures-I.txt")
    print("  Chaque signature a été VÉRIFIée avec la clé publique avant "
          "écriture.")
    print("  Remettez signatures-I.txt au dépôt "
          "(v06/sceau_I.py deposer signatures-I.txt).")


def mode_verifier(chemin_a_signer, chemin_signatures, chemin_publique):
    entrees = lire_lignes_a_signer(chemin_a_signer)
    with open(chemin_signatures, "r", encoding="utf-8") as f:
        lignes_sig = [l.strip() for l in f if l.strip()]
    publique = lire_hex_fichier(chemin_publique, "clé publique", 32)
    vues, tout = set(), True
    for ligne in lignes_sig:
        morceaux = ligne.split()
        if len(morceaux) != 3 or not _est_hex_min(morceaux[2], 128):
            print(f"  ECHEC : ligne de signature malformée : {ligne!r}")
            tout = False
            continue
        arbre, balise, signature_hex = morceaux
        correspond = [e for e in entrees if e[0] == arbre]
        if not correspond:
            print(f"  ECHEC : {arbre} absent de {chemin_a_signer}")
            tout = False
            continue
        if correspond[0][1] != balise:
            print(f"  ECHEC : balise divergente pour {arbre} : {balise!r}")
            tout = False
            continue
        ok = verifier_ed25519(publique, bytes.fromhex(correspond[0][2]),
                              bytes.fromhex(signature_hex))
        print(f"  {arbre}: {'VERT' if ok else 'SIGNATURE INVALIDE'}")
        vues.add(arbre)
        tout = tout and ok
    manquants = sorted({a for a, _, _ in entrees} - vues)
    if manquants:
        print(f"  ECHEC : arbres sans signature : {', '.join(manquants)}")
        tout = False
    print("[ceremonie] verifier : " + ("TOUT VERT" if tout else "ÉCHEC"))
    return 0 if tout else 1


def main():
    parseur = argparse.ArgumentParser(
        description="Cérémonie de la clé I — TRIADE v0.6.0 axe 3 (D87). "
                    "Script autoporteur, hors ligne, stdlib seule.")
    parseur.add_argument("mode", choices=["autotest", "generer", "signer",
                                          "verifier"])
    parseur.add_argument("a_signer", nargs="?", help="signer/verifier : "
                                                     "a-signer.txt")
    parseur.add_argument("cle_ou_signatures", nargs="?",
                         help="signer : cle-I-privee.txt ; verifier : "
                              "signatures-I.txt")
    parseur.add_argument("cle_publique", nargs="?",
                         help="verifier : cle-publique-I.txt")
    arguments = parseur.parse_args()
    if arguments.mode == "autotest":
        ok = autotest()
        print("[ceremonie] autotest : " + ("VERT" if ok else "ÉCHEC"))
        return 0 if ok else 1
    if arguments.mode == "generer":
        mode_generer()
        return 0
    if arguments.mode == "signer":
        if not arguments.a_signer or not arguments.cle_ou_signatures:
            parseur.error("signer exige A-SIGNER et CLE-PRIVEE")
        mode_signer(arguments.a_signer, arguments.cle_ou_signatures)
        return 0
    if arguments.mode == "verifier":
        if not (arguments.a_signer and arguments.cle_ou_signatures
                and arguments.cle_publique):
            parseur.error("verifier exige A-SIGNER SIGNATURES CLE-PUBLIQUE")
        return mode_verifier(arguments.a_signer, arguments.cle_ou_signatures,
                             arguments.cle_publique)
    return 2


if __name__ == "__main__":
    sys.exit(main())
