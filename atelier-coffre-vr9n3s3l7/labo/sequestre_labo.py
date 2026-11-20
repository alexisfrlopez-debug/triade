#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sequestre_labo.py — LE SÉQUESTRE DE LABORATOIRE 5/3 (l'atelier
coffre-vr9n3s3l7, plan (d) : la cérémonie changer-phrase CF3 sous séquestre).

COPIE DE LABORATOIRE AUTOPORTÉE du kit scripts/kit_ceremonie_d183/
sequestre_d183.py (RÉFÉRENCE JAMAIS MODIFIÉE — ici le partage GF(2^8) est
ré-implémenté dans l'atelier : le laboratoire n'importe RIEN du dépôt, ne
touche AUCUN coffre réel, AUCUNE phrase réelle — D105).

LE PARTAGE : Shamir à seuil sur GF(2^8) au polynôme AES (0x11B), 5 parts à
seuil 3 (D183 : « le modèle CF2 D120 »), BLOC PAR BLOC : chaque bloc de 32
octets de la phrase est partagé 5/3, chaque part concatène ses tranches
(en-tête public [len_lo, len_hi, indice x] — la longueur et l'indice ne
sont JAMAIS des secrets).

LA PORTE D223 (la règle du plan (d)) : la phrase ne s'écrit JAMAIS au
dépôt — la garde refuse TOUTE écriture dont le tampon contient la phrase
en clair sous un chemin du dépôt (l'atelier compris : PLUS STRICT que la
lettre, NOMMÉ) ; les parts (inertes sous le seuil — l'information-théorie)
et les PV (sans secret) passent la porte.

LA PREUVE À FROID (miroir D183) : les C(5,3) = 10 combinaisons au seuil
reconstituent EXACTEMENT la phrase ; les C(5,2) = 10 paires sous le seuil
rendent un déchet ; une part forgée (un octet muté) est REFUSÉE par la
confrontation à l'empreinte de contrôle du manifeste.
"""
from __future__ import annotations

import hashlib
import itertools
import os

N_PARTS, SEUIL = 5, 3

# La racine du dépôt — la garde D223 en tire son périmètre (référentiel :
# le présent fichier vit à <depot>/atelier-coffre-vr9n3s3l7/labo/).
DEPOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


class ErreurD223(RuntimeError):
    """Le REFUS NOMMÉ : la phrase ne s'écrit JAMAIS au dépôt (plan (d))."""


# ---------------------------------------------------------------------------
# GF(2^8) au polynôme AES — le partage autoporté de l'atelier
# ---------------------------------------------------------------------------

def _gf_mul(a: int, b: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        if a & 0x80:
            a = ((a << 1) ^ 0x11B) & 0xFF
        else:
            a <<= 1
    return r


def _gf_inv(a: int) -> int:
    for b in range(1, 256):
        if _gf_mul(a, b) == 1:
            return b
    raise ValueError("inversible impossible en GF(2^8)")


def _gf_div(a: int, b: int) -> int:
    return _gf_mul(a, _gf_inv(b))


def _partager_bloc(bloc: bytes, alea=None):
    """Un bloc de 32 o : polynôme degré 2 sur GF(2^8) (miroir CF2 § 2 :
    coefficients FRAIS par octet, évaluation par mult. GF — jamais
    l'arithmétique entière), 5 parts à seuil 3. alea : source d'octets
    (les tests reproductibles)."""
    assert len(bloc) == 32
    rnd = os.urandom if alea is None else alea
    a1 = bytearray(rnd(32))
    a2 = bytearray(rnd(32))
    parts = []
    for x in range(1, N_PARTS + 1):
        tranche = bytearray(32)
        for i in range(32):
            y = bloc[i] ^ _gf_mul(a1[i], x) \
                ^ _gf_mul(a2[i], _gf_mul(x, x))
            tranche[i] = y
        parts.append((x, bytes(tranche)))
    return parts


def _reconstituer_bloc(frags):
    """Lagrange au seuil : TROIS points (x, y) rendent le secret exact."""
    if len(frags) < SEUIL:
        raise ValueError("sous le seuil : aucune information")
    frags = frags[:SEUIL]
    secret = bytearray(32)
    for i in range(32):
        acc = 0
        for j, (xj, yj) in enumerate(frags):
            num, den = 1, 1
            for k, (xk, _) in enumerate(frags):
                if k == j:
                    continue
                num = _gf_mul(num, xk)
                den = _gf_mul(den, xk ^ xj)
            acc ^= _gf_mul(yj[i], _gf_div(num, den))
        secret[i] = acc
    return bytes(secret)


def decouper_phrase(phrase: bytes) -> list[bytes]:
    """5 parts à seuil 3, BLOC PAR BLOC (miroir D183) : part =
    [len_lo, len_hi, x] + tranches."""
    longueur = len(phrase)
    parts = [bytearray([longueur & 0xFF, (longueur >> 8) & 0xFF, i + 1])
             for i in range(N_PARTS)]
    for o in range(0, longueur, 32):
        bloc = phrase[o:o + 32].ljust(32, b"\x00")
        for i, (x, tranche) in enumerate(_partager_bloc(bloc)):
            parts[i].extend(tranche)
    return [bytes(p) for p in parts]


def reconstituer_phrase(parts: list[bytes]) -> bytes:
    """Le miroir exact : chaque bloc reconstitué au seuil, la longueur coupe
    le padding."""
    longueur = parts[0][0] | (parts[0][1] << 8)
    rendu = bytearray()
    n_blocs = (longueur + 31) // 32
    for b in range(n_blocs):
        frags = [(p[2], p[3 + 32 * b:3 + 32 * (b + 1)]) for p in parts]
        rendu.extend(_reconstituer_bloc(frags))
    return bytes(rendu[:longueur])


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------------
# LA PORTE D223 — la phrase ne s'écrit JAMAIS au dépôt
# ---------------------------------------------------------------------------

def garde_d223(chemin: str, donnees: bytes, phrase: bytes) -> None:
    """Le REFUS NOMMÉ : si le tampon à écrire CONTIENT la phrase en clair et
    que la cible vit SOUS LE DÉPÔT, l'écriture est REFUSÉE (D223 — le plan
    (d) : « la phrase JAMAIS écrite au dépôt »). PLUS STRICT, NOMMÉ : la
    porte vaut pour TOUT chemin du dépôt, atelier compris. Les parts
    (inertes sous le seuil) et les PV (sans secret) passent : le test est
    l'appartenance EXACTE du secret au tampon, jamais une heuristique."""
    if not phrase:
        return
    cible = os.path.realpath(chemin)
    racine = os.path.realpath(DEPOT)
    sous_depots = cible == racine or cible.startswith(racine + os.sep)
    if sous_depots and (donnees == phrase or phrase in donnees):
        raise ErreurD223(
            f"REFUS D223 — la phrase ne s'écrit JAMAIS au dépôt : "
            f"{chemin} est sous {racine} et le tampon contient la phrase "
            f"en clair ({len(donnees)} octets, phrase {len(phrase)} octets) "
            "— le geste est REFUSÉ nommément, aucun fichier n'est créé "
            "(plan (d), la règle D223)")


def ecrire_sous_garde(chemin: str, donnees: bytes, phrase: bytes) -> None:
    """L'écriture QUI passe la porte D223 — le seul chemin d'écriture de la
    cérémonie (d)."""
    garde_d223(chemin, donnees, phrase)
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    tmp = os.path.join(os.path.dirname(chemin) or ".",
                       f".{os.path.basename(chemin)}.{os.urandom(8).hex()}"
                       ".tmp")
    with open(tmp, "wb") as f:
        f.write(donnees)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, chemin)


# ---------------------------------------------------------------------------
# Le manifeste du séquestre de laboratoire
# ---------------------------------------------------------------------------

def ecrire_manifeste(dossier: str, parts: list[bytes], phrase: bytes,
                     mention: str) -> str:
    """Écrit parts-N.txt + manifeste — SOUS LA GARDE D223 (les parts sont
    inertes sous le seuil : elles passent la porte ; le manifeste ne porte
    QUE l'empreinte de contrôle, JAMAIS la phrase)."""
    chemins = []
    for i, p in enumerate(parts, 1):
        chemin = os.path.join(dossier, f"part-{i}.txt")
        ecrire_sous_garde(chemin, p.hex().encode("ascii") + b"\n", phrase)
        chemins.append(chemin)
    lignes = [
        "MANIFESTE DU SÉQUESTRE DE LABORATOIRE — 5 parts à seuil 3 (GF(2^8), "
        "polynôme AES, plan (d))",
        mention,
        f"taille de la phrase : {len(phrase)} octets",
        f"empreinte de contrôle de la phrase (sha256) : {sha256_hex(phrase)}",
        "   (permet la vérification à froid SANS la phrase)",
        "",
        "LES EMPREINTES DES PARTS (sha256) :",
    ]
    for i, p in enumerate(parts, 1):
        lignes.append(f"  part-{i}.txt : {sha256_hex(p)}")
    lignes += [
        "",
        "LA PHRASE N'EST JAMAIS ÉCRITE — la porte D223 refuse tout tampon "
        "qui la contiendrait sous le dépôt (testée sur pièces).",
    ]
    chemin = os.path.join(dossier, "manifeste-sequestre.txt")
    ecrire_sous_garde(chemin, ("\n".join(lignes) + "\n").encode("utf-8"),
                      phrase)
    return chemin


def verifier_parts(parts: list[bytes], empreinte_controle: str) -> bool:
    """La preuve fail-closed : le sha256 du rendu == l'empreinte de contrôle
    du manifeste — ÉGALITÉ exigée, tout écart un REFUS nommé."""
    rendu = reconstituer_phrase(parts)
    return sha256_hex(rendu) == empreinte_controle


def autotest(phrase: bytes) -> tuple[bool, list[str]]:
    """La preuve à froid du partage sur la phrase de test (miroir D183) :
    les 10 combinaisons au seuil EXACTES, les 10 paires sous le seuil
    DÉCHETS, la part forgée REFUSÉE à l'empreinte de contrôle, le contrôle
    honnête VERT."""
    lignes = []
    ok = True
    parts = decouper_phrase(phrase)
    controle = sha256_hex(phrase)
    for combo in itertools.combinations(range(N_PARTS), SEUIL):
        rendu = reconstituer_phrase([parts[i] for i in combo])
        bon = rendu == phrase
        ok &= bon
        lignes.append(f"  parts {combo} : {'EXACTE' if bon else 'FAUX !'}")
    for paire in itertools.combinations(range(N_PARTS), 2):
        rendu = reconstituer_phrase([parts[i] for i in paire])
        fuite = rendu == phrase or phrase[:8] in rendu
        ok &= not fuite
        lignes.append(f"  paire {paire} (sous le seuil) : "
                      f"{'DÉCHET (rien ne fuite)' if not fuite else 'FUITE !'}")
    for combo in ((0, 1, 2), (2, 3, 4)):
        forge = bytearray(parts[combo[0]])
        forge[3 + 5] ^= 0x01
        rendu_f = reconstituer_phrase(
            [bytes(forge)] + [parts[i] for i in combo[1:]])
        refuse = sha256_hex(rendu_f) != controle
        ok &= refuse
        lignes.append(f"  parts {combo} dont une FORGÉE (octet muté) : "
                      f"{'REFUSÉE — sha256 ≠ contrôle' if refuse else 'ACCEPTÉE !'}")
    honnete = verifier_parts([parts[0], parts[1], parts[2]], controle)
    ok &= honnete
    lignes.append(f"  parts (0, 1, 2) honnêtes : "
                  f"{'VERT — sha256 == contrôle' if honnete else 'ROUGE !'}")
    return ok, lignes
