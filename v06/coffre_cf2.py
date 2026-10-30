#!/usr/bin/env python3
"""coffre_cf2.py — Coffre CF2 : l'interrupteur d'homme mort (D86, v0.6.0 axe 2).

Spécification : v06/I/CF2/README.md (R2 écrite-avant-code — CE fichier
l'instancie, aucun écart toléré). CF2 remplace la cérémonie de clé du coffre :
la base (mêmes entrées que CF1) est chiffrée sous une clé maîtresse M de 32
octets JAMAIS stockée entière — découpée par Shamir en N fragments logés
dans des gardes distinctes ; le déverrouillage reconstitue M en RAM puis
l'efface. Une sentinelle (v06/sentinelle_cf2.py) surveille la couche C :
lecture par un processus hors liste blanche -> destruction des fragments
(routine `bruler` ci-dessous, source unique de vérité) -> sous le seuil, le
coffre est informationnellement mort.

Discipline (spec § 8) : M ne vit qu'en `bytearray`, effacé après usage au
mieux de Python ; aucun secret n'entre dans un journal, un PV ou une sortie.
Le conteneur réel et les phrases réels ne sont JAMAIS touchés par les
autocontrôles (répertoires temporaires uniquement — discipline D105).

D119 (rapport de cérémonie du terrain v1.8) : le fsync de RÉPERTOIRE est
POSIX-seul — Windows refuse os.open() sur un dossier (PermissionError
errno 13 : « migrer » y mourait en écrivant .keys/coffre_cf2.bin) ;
l'atomicité ne change pas (os.replace est atomique sur les deux familles).

Usage (depuis triade/) :
  python3 v06/coffre_cf2.py init [--fragments N] [--seuil T]
       [--racine-gardes DIR] [--description-projet D]
  python3 v06/coffre_cf2.py migrer [--depuis F] [--phrase-stdin]
       [--fragments N] [--seuil T] [--racine-gardes DIR]
  python3 v06/coffre_cf2.py statut
  python3 v06/coffre_cf2.py etat-fragments
  python3 v06/coffre_cf2.py lister [PROJET]
  python3 v06/coffre_cf2.py obtenir PROJET ETIQUETTE
  python3 v06/coffre_cf2.py ajouter PROJET ETIQUETTE [--description D]
       [--depuis-fichier F | --stdin | --generer] [--remplacer]
  python3 v06/coffre_cf2.py retirer PROJET ETIQUETTE
  python3 v06/coffre_cf2.py verifier
  python3 v06/coffre_cf2.py restaurer FICHIER [FICHIER ...]
  python3 v06/coffre_cf2.py bruler [--oui-je-comprends]
  python3 v06/coffre_cf2.py autotest

Dépendances : pynacl, cryptography (la pile du dépôt — spec § 3).
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import sys
from datetime import datetime, timezone

try:
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes
    from nacl.bindings import (crypto_aead_xchacha20poly1305_ietf_decrypt,
                               crypto_aead_xchacha20poly1305_ietf_encrypt)
except ImportError as exc:  # pragma: no cover
    print(f"ECHEC : dépendance manquante ({exc}) — "
          "pip install pynacl cryptography", file=sys.stderr)
    sys.exit(1)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS_DIR = os.path.join(RACINE, ".keys")
CHEMIN_CONTENEUR_DEFAUT = os.path.join(KEYS_DIR, "coffre_cf2.bin")
CHEMIN_CONFIG_DEFAUT = os.path.join(KEYS_DIR, "config_cf2.json")
RACINE_GARDES_DEFAUT = os.path.join(KEYS_DIR, "gardes-cf2")

MAGIC = b"TRIADE-CF2"
FORMAT_VERSION = 1
PROTOCOLE = "0.6.0"
ALGO_HACHAGE = "sha256"
ALGO_KDF = "hkdf-sha256"
ALGO_CHIFFREMENT = "xchacha20poly1305"
HKDF_INFO_CLE = b"coffre=v2"          # spec § 3 — contexte DISTINCT de CF1
HKDF_INFO_VERIF = b"cf2=verif"
TAILLE_M = 32                          # spec § 2
N_DEFAUT = 5                           # spec § 5 — arbitrage consigné
T_DEFAUT = 3
MAGIC_FRAG = "TRIADE-CF2-FRAG v1"
MOTIF_FRAG = "fragment-*.cf2f"         # spec § 7 — seuls ces fichiers brûlent
PREFIXE_FRAG = "fragment-"

RE_PROJET = None  # posé après import coffre_fort (mêmes règles que CF1)


class ErreurCoffre(RuntimeError):
    """Tout échec de parsing, reconstitution, déchiffrement ou commande —
    fail-closed NOMMÉ (spec § 13 : un verdict muet n'est pas une preuve)."""


# ---------------------------------------------------------------------------
# GF(2^8), polynôme 0x11B (spec § 2)
# ---------------------------------------------------------------------------

POLYNOME_GF = 0x11B
_EXP = [0] * 512
_LOG = [0] * 256


def _construire_tables() -> None:
    """Tables log/exp sur le générateur PRIMITIF 0x03 du corps 0x11B.

    0x02 n'est PAS primitif modulo 0x11B (ordre 51 : 204 éléments sans
    logarithme — l'erreur constatée en autotest, piégée par des tests de
    coin qui coïncidaient avec la faute). 0x03 est primitif (ordre 255).
    """
    x = 1
    for i in range(255):
        _EXP[i] = x
        _LOG[x] = i
        double = (x << 1) ^ (POLYNOME_GF if x & 0x80 else 0)   # 2·x
        x = double ^ x                                          # 3·x
    for i in range(255, 512):
        _EXP[i] = _EXP[i - 255]


_construire_tables()


def gf_mult(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return _EXP[_LOG[a] + _LOG[b]]


def gf_inv(a: int) -> int:
    if a == 0:
        raise ErreurCoffre("inverse de 0 dans GF(2^8) — polynôme dégénéré")
    return _EXP[255 - _LOG[a]]


def _evaluer_poly(coeffs: list, x: int) -> int:
    """Horner (spec § 2) — coeffs[0] = terme constant."""
    y = 0
    for c in reversed(coeffs):
        y = gf_mult(y, x) ^ c
    return y


# ---------------------------------------------------------------------------
# Shamir (spec § 2)
# ---------------------------------------------------------------------------

def decouper(m: bytes, n: int, t: int, alea=None):
    """M -> N fragments (x, 32 o). `alea` : source d'octets (tests).

    Coefficients FRAIS du CSPRNG pour CHACUN des 32 octets (spec § 2) —
    jamais réutilisés d'un octet à l'autre.
    """
    if len(m) != TAILLE_M:
        raise ErreurCoffre(f"secret maître != {TAILLE_M} o ({len(m)})")
    if not 2 <= t <= n <= 255:
        raise ErreurCoffre(f"seuil invalide : 2 <= t <= n <= 255 requis "
                           f"(t={t}, n={n}) — spec § 2")
    source = alea if alea is not None else secrets.token_bytes
    polynomes = []
    for k in range(TAILLE_M):
        coeffs = [m[k]] + list(source(t - 1))
        if len(coeffs) != t:
            raise ErreurCoffre("source aléatoire incomplète (fail-closed)")
        polynomes.append(coeffs)
    fragments = []
    for x in range(1, n + 1):
        fragments.append((x, bytes(_evaluer_poly(polynomes[k], x)
                                   for k in range(TAILLE_M))))
    return fragments


def reconstituer(fragments):
    """Lagrange en x=0 (spec § 2) — T fragments valides distincts."""
    if len(fragments) < 2:
        raise ErreurCoffre("moins de 2 fragments — la reconstitution est "
                           "refusée (spec § 2)")
    xs = [x for x, _ in fragments]
    if len(set(xs)) != len(xs):
        raise ErreurCoffre(f"indices x dupliqués : {sorted(xs)} — spec § 2")
    for x in xs:
        if not 1 <= x <= 255:
            raise ErreurCoffre(f"indice x hors bornes : {x} — spec § 2")
    if any(len(f) != TAILLE_M for _, f in fragments):
        raise ErreurCoffre("fragment de taille invalide (32 o attendus)")
    m = bytearray(TAILLE_M)
    for k in range(TAILLE_M):
        acc = 0
        for j, (xj, fj) in enumerate(fragments):
            poids = 1
            for m_, (xm, _) in enumerate(fragments):
                if m_ == j:
                    continue
                # L(0) : Π x_m · (x_j ⊕ x_m)^-1  (soustraction = XOR en GF(2^8))
                poids = gf_mult(poids, gf_mult(xm, gf_inv(xj ^ xm)))
            acc ^= gf_mult(fj[k], poids)
        m[k] = acc
    return bytes(m)


def tag_fragment(x: int, frag: bytes) -> bytes:
    """sha256("TRIADE-CF2-frag" || x || fragment)[:8] — nomme le fautif
    sans le divulguer (spec § 4)."""
    return hashlib.sha256(b"TRIADE-CF2-frag" + bytes([x]) + frag).digest()[:8]


# ---------------------------------------------------------------------------
# Conteneur TRIADE-CF2 (spec § 3)
# ---------------------------------------------------------------------------

def _champ(octets: bytes) -> bytes:
    return len(octets).to_bytes(2, "little") + octets


def _lire_champ(blob: bytes, offset: int) -> tuple[bytes, int]:
    if offset + 2 > len(blob):
        raise ErreurCoffre("champ longueur-préfixée tronqué (en-tête)")
    n = int.from_bytes(blob[offset:offset + 2], "little")
    if offset + 2 + n > len(blob):
        raise ErreurCoffre("champ longueur-préfixée tronqué (valeur)")
    return blob[offset + 2:offset + 2 + n], offset + 2 + n


def _hkdf(m: bytes, sel: bytes, info: bytes, longueur: int = 32) -> bytes:
    return HKDF(algorithm=hashes.SHA256(), length=longueur, salt=sel,
                info=info).derive(m)


def cle_session(m: bytes, sel: bytes) -> bytes:
    """K = HKDF(M, sel, « coffre=v2 ») — spec § 3."""
    return _hkdf(m, sel, HKDF_INFO_CLE)


def empreinte_verif(m: bytes, sel: bytes) -> bytes:
    """verif = sha256(HKDF(M, sel, « cf2=verif »))[:16] — spec § 3."""
    return hashlib.sha256(_hkdf(m, sel, HKDF_INFO_VERIF)).digest()[:16]


def construire_conteneur(clair: bytes, m: bytes, sel: bytes, date: str,
                         t: int, n: int) -> bytes:
    """En-tête clair + AEAD(AAD = tout ce qui précède l'empreinte).

    Miroir exact de CF1 (§ 11.2) : l'empreinte du chiffretexte est posée
    APRÈS la zone AAD — pas de circularité, le tag AEAD reste la preuve
    d'authenticité, l'empreinte la redondance nommée.
    """
    if len(sel) != 32:
        raise ErreurCoffre("sel HKDF != 32 o (spec § 3)")
    k = cle_session(m, sel)
    verif = empreinte_verif(m, sel)
    nonce = secrets.token_bytes(24)
    aad = (MAGIC + FORMAT_VERSION.to_bytes(2, "little")
           + _champ(ALGO_HACHAGE.encode()) + _champ(ALGO_KDF.encode())
           + _champ(ALGO_CHIFFREMENT.encode()) + _champ(date.encode())
           + _champ(f"t={t}/n={n}".encode())
           + sel + nonce)
    chiffretexte = crypto_aead_xchacha20poly1305_ietf_encrypt(
        clair, aad, nonce, k)
    empreinte = hashlib.sha256(chiffretexte).digest()
    return aad + empreinte + verif + chiffretexte


def _parser_entete(blob: bytes) -> dict:
    """En-tête clair complet (fail-closed, liste blanche — spec § 3)."""
    if len(blob) < 10 + 2:
        raise ErreurCoffre("conteneur trop court")
    if blob[:10] != MAGIC:
        raise ErreurCoffre(f"magic invalide : {blob[:10]!r} (TRIADE-CF2 attendu)")
    version = int.from_bytes(blob[10:12], "little")
    if version != FORMAT_VERSION:
        raise ErreurCoffre(f"version conteneur non gérée : {version}")
    offset = 12
    champs = {}
    for clef in ("hachage", "kdf", "chiffrement", "date", "shamir"):
        champs[clef], offset = _lire_champ(blob, offset)
    debut_aad = offset
    fin_aad = debut_aad + 32 + 24
    if len(blob) < fin_aad:
        raise ErreurCoffre("en-tête tronqué (sel/nonce)")
    fin_entete = fin_aad + 32 + 16
    if len(blob) < fin_entete:
        raise ErreurCoffre("en-tête tronqué (empreinte/verif)")
    algos_attendus = {"hachage": ALGO_HACHAGE.encode(),
                      "kdf": ALGO_KDF.encode(),
                      "chiffrement": ALGO_CHIFFREMENT.encode()}
    for clef, attendu in algos_attendus.items():
        if champs[clef] != attendu:
            raise ErreurCoffre(f"algorithme {clef} hors liste blanche : "
                               f"{champs[clef]!r}")
    sel = blob[debut_aad:debut_aad + 32]
    nonce = blob[debut_aad + 32:fin_aad]
    empreinte = blob[fin_aad:fin_aad + 32]
    verif = blob[fin_aad + 32:fin_entete]
    chiffretexte = blob[fin_entete:]
    try:
        shamir = champs["shamir"].decode("ascii")
        st, sn = shamir.split("/")
        t = int(st.replace("t=", ""))
        n = int(sn.replace("n=", ""))
    except (ValueError, UnicodeDecodeError):
        raise ErreurCoffre(f"champ shamir malformé : {champs['shamir']!r}")
    if not 2 <= t <= n <= 255:
        raise ErreurCoffre(f"seuil du conteneur invalide : {shamir!r}")
    return {"version": version, "date": champs["date"].decode("ascii"),
            "shamir": shamir, "t": t, "n": n, "sel": sel, "nonce": nonce,
            "empreinte": empreinte, "verif": verif, "aad": blob[:fin_aad],
            "chiffretexte": chiffretexte,
            "entete": blob[:fin_entete], "taille": len(blob)}


def dechiffrer(blob: bytes, m: bytes) -> tuple[dict, dict]:
    """Fail-closed NOMMÉ : verif, empreinte, tag AEAD (spec § 3)."""
    entete = _parser_entete(blob)
    if empreinte_verif(m, entete["sel"]) != entete["verif"]:
        raise ErreurCoffre("verif divergent : clé maîtresse FAUSSE "
                           "(fragments insuffisants, substitués ou corrompus) "
                           "— spec § 3")
    if hashlib.sha256(entete["chiffretexte"]).digest() != entete["empreinte"]:
        raise ErreurCoffre("empreinte du chiffretexte divergente "
                           "(conteneur altéré) — spec § 3")
    k = cle_session(m, entete["sel"])
    try:
        clair = crypto_aead_xchacha20poly1305_ietf_decrypt(
            entete["chiffretexte"], entete["aad"], entete["nonce"], k)
    except Exception:
        raise ErreurCoffre("tag AEAD invalide — conteneur altéré (spec § 3)")
    try:
        base = json.loads(clair.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise ErreurCoffre("base JSON illisible après déchiffrement")
    return base, entete


def empreinte_conteneur(entete: bytes) -> str:
    """sha256 de l'en-tête clair — le lien fragment -> conteneur (spec § 4)."""
    return hashlib.sha256(entete).hexdigest()


# ---------------------------------------------------------------------------
# Fragment TRIADE-CF2-FRAG (spec § 4)
# ---------------------------------------------------------------------------

def serialiser_fragment(x: int, frag: bytes, t: int, n: int,
                        sel_coffre: str) -> str:
    """Le fragment lie au SEL DU COFFRE (identité STABLE) — jamais à
    l'empreinte de l'en-tête : le nonce est frais à CHAQUE écriture, lier à
    l'en-tête invaliderait les copies papier à chaque ajouter/retirer
    (faute dénoncée par le parcours CLI complet, consignée D106)."""
    return (f"{MAGIC_FRAG}\n"
            f"coffre: {sel_coffre}\n"
            f"x: {x}\n"
            f"seuil: t={t}/n={n}\n"
            f"fragment: {frag.hex()}\n"
            f"tag: {tag_fragment(x, frag).hex()}\n")


def parser_fragment(texte: str) -> dict:
    """Parse + vérifications nommées (magic, formats, tag) — spec § 4."""
    lignes = [l.strip() for l in texte.splitlines() if l.strip()]
    if not lignes or lignes[0] != MAGIC_FRAG:
        raise ErreurCoffre("magic fragment invalide (TRIADE-CF2-FRAG v1 attendu)")
    champs = {}
    for l in lignes[1:]:
        if ":" not in l:
            raise ErreurCoffre(f"ligne de fragment malformée : {l!r}")
        clef, _, valeur = l.partition(":")
        champs[clef.strip()] = valeur.strip()
    manquants = [c for c in ("coffre", "x", "seuil", "fragment", "tag")
                 if c not in champs]
    if manquants:
        raise ErreurCoffre(f"champs manquants dans le fragment : {manquants}")
    try:
        x = int(champs["x"])
    except ValueError:
        raise ErreurCoffre(f"indice x non numérique : {champs['x']!r}")
    if not 1 <= x <= 255:
        raise ErreurCoffre(f"indice x hors bornes : {x}")
    try:
        st, sn = champs["seuil"].split("/")
        t = int(st.replace("t=", ""))
        n = int(sn.replace("n=", ""))
    except ValueError:
        raise ErreurCoffre(f"champ seuil malformé : {champs['seuil']!r}")
    if not 2 <= t <= n <= 255:
        raise ErreurCoffre(f"seuil du fragment invalide : {champs['seuil']!r}")
    hexa = champs["fragment"]
    if len(hexa) != 64 or any(c not in "0123456789abcdef" for c in hexa):
        raise ErreurCoffre("fragment : 64 caractères hex attendus")
    frag = bytes.fromhex(hexa)
    tag = champs["tag"]
    if len(tag) != 16 or any(c not in "0123456789abcdef" for c in tag):
        raise ErreurCoffre("tag : 16 caractères hex attendus")
    if bytes.fromhex(tag) != tag_fragment(x, frag):
        raise ErreurCoffre(f"tag du fragment x={x} INVALIDE — fragment "
                           "corrompu ou falsifié (spec § 4)")
    return {"x": x, "t": t, "n": n, "fragment": frag,
            "coffre": champs["coffre"]}


# ---------------------------------------------------------------------------
# Base (même schéma que CF1 — la migration ne traduit rien, spec § 3/§ 10)
# ---------------------------------------------------------------------------

def _date_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def nouvelle_base(description: str = "") -> dict:
    return {"format": 1, "protocole": PROTOCOLE,
            "cree": _date_utc(), "modifie": _date_utc(),
            "description": description, "projets": {}}


def _fsync_repertoire(chemin: str) -> None:
    """D119 — fsync du répertoire conteneur, POSIX SEUL : Windows refuse
    os.open() sur un répertoire (PermissionError errno 13 — le rapport de
    cérémonie du terrain v1.8 portait la preuve : « CF2 — migrer » mourait
    en écrivant .keys/coffre_cf2.bin). L'atomicité ne dépend PAS de ce
    fsync (os.replace est atomique sur les deux familles) : sous Windows
    il est absent, et sous POSIX un répertoire impossible à ouvrir
    n'abandonne pas une écriture déjà posée (la durabilité du dossier est
    un mieux-disant, pas une garantie)."""
    if os.name != "posix":
        return
    try:
        rep = os.open(chemin, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(rep)
    finally:
        os.close(rep)


def _ecrire_atomique(chemin: str, donnees: bytes) -> None:
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    tmp = chemin + ".tmp"
    with open(tmp, "wb") as f:
        f.write(donnees)
        f.flush()
        os.fsync(f.fileno())
    os.chmod(tmp, 0o600)
    os.replace(tmp, chemin)
    _fsync_repertoire(os.path.dirname(chemin))


# ---------------------------------------------------------------------------
# Configuration partagée outil/sentinelle (spec § 5-6)
# ---------------------------------------------------------------------------

def config_par_defaut(n: int, t: int, racine_gardes: str,
                      conteneur: str) -> dict:
    gardes = [os.path.join(racine_gardes, f"g{i}") for i in range(1, n + 1)]
    couche_c = []
    for rel in ("m0/carte", "m1/carte", "m2/carte", "m3/carte", "m4/carte",
                "demo/carte", "terrain/carte"):
        chemin = os.path.join(RACINE, rel)
        if os.path.isdir(chemin):
            couche_c.append(chemin)
    for rel in ("m3/proxy.exe", "m4/proxy.exe", "m3/echo.exe"):
        chemin = os.path.join(RACINE, rel)
        if os.path.isfile(chemin):
            couche_c.append(chemin)
    return {
        "version": 1, "conteneur": conteneur, "gardes": gardes,
        "n": n, "t": t, "couche_c": couche_c,
        # Liste blanche MINIMALE (spec § 6) : build, vérificateurs, outils du
        # coffre, sentinelle — l'ÉDITEUR du développeur s'ajoute au déploiement
        # (download/LISEZMOI-coffre-CF2.txt). Motifs sur l'image RÉSOLUE ou la
        # ligne de commande COMPLÈTE — jamais « tout python3 ».
        "liste_blanche": [r"[/]build_m[0-9]+\.py", r"[/]build_terrain\.py",
                          r"[/]oracle_m[0-9]+\.py", r"[/]verifier",
                          r"[/]conformite_profil\.py",
                          r"[/]coffre_cf2\.py", r"[/]coffre_fort\.py",
                          r"[/]sentinelle_cf2\.py", r"[/]test_cf2\.py"],
        "periode_sondage": 0.25,
        "journal": os.path.join(KEYS_DIR, "journal-sentinelle.txt"),
        "pv_dir": os.path.join(KEYS_DIR, "pv-cf2"),
        "heartbeat": os.path.join(KEYS_DIR, "heartbeat-sentinelle.txt"),
    }


def ecrire_config(chemin: str, config: dict) -> None:
    _ecrire_atomique(chemin, json.dumps(config, indent=2,
                                        ensure_ascii=False).encode("utf-8"))


def lire_config(chemin: str) -> dict:
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, ValueError) as exc:
        raise ErreurCoffre(f"config illisible : {chemin} ({exc})")
    for clef in ("conteneur", "gardes", "couche_c", "liste_blanche"):
        if clef not in config:
            raise ErreurCoffre(f"config incomplète : champ {clef!r} absent")
    return config


# ---------------------------------------------------------------------------
# Fragments présents dans les gardes (spec § 5/§ 8)
# ---------------------------------------------------------------------------

def _fragments_presents(gardes, sel_coffre: str, t_attendu: int,
                        n_attendu: int):
    """Collecte les fragments VALIDES + avertissements nommés.

    Un fragment corrompu n'entâche pas les autres (custodie répartie) :
    il est SIGNALÉ ; c'est le compte de valides qui décide (>= T).
    """
    import glob as _glob
    valides, avertissements = {}, []
    for garde in gardes:
        if not os.path.isdir(garde):
            avertissements.append(f"garde absente : {garde}")
            continue
        for chemin in sorted(_glob.glob(os.path.join(garde, MOTIF_FRAG))):
            try:
                with open(chemin, "r", encoding="ascii") as f:
                    frag = parser_fragment(f.read())
            except (OSError, UnicodeDecodeError) as exc:
                avertissements.append(f"fragment illisible : {chemin} ({exc})")
                continue
            except ErreurCoffre as exc:
                avertissements.append(f"{chemin} : {exc}")
                continue
            if frag["coffre"] != sel_coffre:
                avertissements.append(
                    f"{chemin} : sel du coffre divergent — fragment "
                    "d'un AUTRE coffre (spec § 4)")
                continue
            if (frag["t"], frag["n"]) != (t_attendu, n_attendu):
                avertissements.append(
                    f"{chemin} : seuil divergent {frag['t']}/{frag['n']} "
                    f"(conteneur : {t_attendu}/{n_attendu})")
                continue
            x = frag["x"]
            if x in valides and valides[x] != frag["fragment"]:
                raise ErreurCoffre(
                    f"conflit d'indice x={x} : deux fragments DIVERGENTS "
                    f"dans les gardes — coffre menteur, refus (spec § 2)")
            valides.setdefault(x, frag["fragment"])
    return valides, avertissements


def _effacer(*buffers) -> None:
    """Discipline RAM (spec § 8) — au mieux de Python : écrase les buffers
    muables avant libération. La garantie native est une affaire Windows."""
    for buf in buffers:
        try:
            for i in range(len(buf)):
                buf[i] = 0
        except TypeError:
            pass


def deverrouiller(conteneur_chemin: str, gardes):
    """Cycle complet spec § 8 : fragments -> M (RAM) -> verif -> AEAD.

    Retour (base, entete, m_bytearray, blob) — l'appelant DOIT effacer m
    (_effacer + del) après usage. Aucun secret ne fuit dans les messages.
    """
    with open(conteneur_chemin, "rb") as f:
        blob = f.read()
    entete = _parser_entete(blob)
    sel_coffre = entete["sel"].hex()
    valides, avertissements = _fragments_presents(
        gardes, sel_coffre, entete["t"], entete["n"])
    for a in avertissements:
        print(f"[coffre-CF2] AVERTISSEMENT : {a}", file=sys.stderr)
    if len(valides) < entete["t"]:
        manquant = entete["t"] - len(valides)
        raise ErreurCoffre(
            f"fragments INSUFFISANTS : {len(valides)} valides / seuil "
            f"{entete['t']} (il manque {manquant} fragment(s) — coffre mort "
            "ou gardes incomplètes, spec § 2)")
    retenus = sorted(valides.items())[:entete["t"]]
    m = bytearray(reconstituer([(x, f) for x, f in retenus]))
    try:
        base, entete2 = dechiffrer(blob, bytes(m))
    except ErreurCoffre:
        _effacer(m)
        raise
    return base, entete2, m, blob


def reverrouiller(conteneur_chemin: str, base: dict, m: bytearray,
                  sel: bytes, t: int, n: int) -> None:
    """Ré-encrypte la base (nonce FRAIS — spec § 3) par-dessus l'atomique."""
    base["modifie"] = _date_utc()
    clair = json.dumps(base, ensure_ascii=False).encode("utf-8")
    blob = construire_conteneur(clair, bytes(m), sel, _date_utc(), t, n)
    _ecrire_atomique(conteneur_chemin, blob)


# ---------------------------------------------------------------------------
# La destruction (spec § 7) — source unique, sentinelle ET commande manuelle
# ---------------------------------------------------------------------------

def bruler(config: dict, declencheur: str) -> str:
    """Trois passes + PV. Ne touche QUE les fichiers fragment-*.cf2f des
    gardes (spec § 7) — jamais le conteneur, jamais autre chose."""
    pv_dir = config.get("pv_dir", os.path.join(KEYS_DIR, "pv-cf2"))
    os.makedirs(pv_dir, exist_ok=True)
    lignes_pv = [
        "PROCÈS-VERBAL DE DESTRUCTION — TRIADE-CF2 (spec § 7, D86)",
        f"date : {_date_utc()}",
        f"déclencheur : {declencheur}",
        "passes : aléatoire (CSPRNG) puis 0xFF puis 0x00, fsync par passe",
        "",
    ]
    import glob as _glob
    detruits = 0
    for garde in config["gardes"]:
        if not os.path.isdir(garde):
            continue
        for chemin in sorted(_glob.glob(os.path.join(garde, MOTIF_FRAG))):
            taille = os.path.getsize(chemin)
            with open(chemin, "rb+") as f:
                for passe in (secrets.token_bytes(taille), b"\xff" * taille,
                              b"\x00" * taille):
                    f.seek(0)
                    f.write(passe)
                    f.flush()
                    os.fsync(f.fileno())
                f.truncate(0)
                f.flush()
                os.fsync(f.fileno())
            nom_alea = os.path.join(os.path.dirname(chemin),
                                    secrets.token_hex(16))
            os.rename(chemin, nom_alea)
            os.unlink(nom_alea)
            _fsync_repertoire(os.path.dirname(chemin))
            detruits += 1
            lignes_pv.append(f"DETRUIT : {chemin} ({taille} o, 3 passes, "
                             "tronqué, renommé, unlink, fsync rép.)")
    lignes_pv.append("")
    lignes_pv.append(f"total : {detruits} fragment(s) détruit(s)")
    lignes_pv.append("le conteneur reste en place — sous le seuil, il est "
                     "indéchiffrable (Shamir informationnel, spec § 2)")
    lignes_pv.append("RELÈVE : restaurer les copies hors-ligne "
                     "(restaurer FICHIER...) — spec § 10")
    texte = "\n".join(lignes_pv) + "\n"
    chemin_pv = os.path.join(pv_dir, f"pv-destruction-{_date_utc().replace(':', '').replace('-', '')}.txt")
    with open(chemin_pv, "w", encoding="utf-8") as f:
        f.write(texte)
    os.chmod(chemin_pv, 0o600)
    journaliser(config, f"DESTRUCTION : {detruits} fragment(s) — {declencheur}"
                f" — PV {chemin_pv}")
    print(f"[coffre-CF2] {detruits} fragment(s) DÉTRUIT(S) — PV : {chemin_pv}")
    return chemin_pv


def journaliser(config: dict, message: str) -> None:
    """Journal partagé outil/sentinelle — JAMAIS de secret (spec § 8)."""
    chemin = config.get("journal")
    if not chemin:
        return
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(f"{_date_utc()} {message}\n")


# ---------------------------------------------------------------------------
# Restauration atomique (spec § 10)
# ---------------------------------------------------------------------------

def restaurer(config: dict, fichiers: list) -> int:
    conteneur = config["conteneur"]
    with open(conteneur, "rb") as f:
        entete = _parser_entete(f.read())
    sel_coffre = entete["sel"].hex()
    valides_presents, _ = _fragments_presents(
        config["gardes"], sel_coffre, entete["t"], entete["n"])
    # Phase 1 : TOUT valider, RIEN écrire (atomicité — motif D105 [11])
    a_ecrire = []
    for fichier in fichiers:
        with open(fichier, "r", encoding="ascii") as f:
            frag = parser_fragment(f.read())
        if frag["coffre"] != sel_coffre:
            raise ErreurCoffre(
                f"{fichier} : sel du coffre divergent — fragment d'un "
                "AUTRE coffre, remise refusée SANS ÉCRIRE (spec § 10)")
        if (frag["t"], frag["n"]) != (entete["t"], entete["n"]):
            raise ErreurCoffre(
                f"{fichier} : seuil divergent — remise refusée SANS ÉCRIRE")
        if frag["x"] in valides_presents:
            raise ErreurCoffre(
                f"{fichier} : indice x={frag['x']} DÉJÀ présent dans les "
                "gardes — remise refusée SANS ÉCRIRE (spec § 10)")
        if any(frag["x"] == x for x, _ in a_ecrire):
            raise ErreurCoffre(
                f"{fichier} : indice x={frag['x']} dupliqué dans la remise — "
                "refus SANS ÉCRIRE")
        if frag["x"] > len(config["gardes"]):
            raise ErreurCoffre(
                f"{fichier} : indice x={frag['x']} > nombre de gardes "
                f"({len(config['gardes'])}) — refus SANS ÉCRIRE")
        a_ecrire.append((frag["x"], fichier))
    # Phase 2 : tout écrire (les validations ont toutes passé)
    for x, fichier in a_ecrire:
        garde = config["gardes"][x - 1]
        os.makedirs(garde, exist_ok=True)
        os.chmod(garde, 0o700)
        with open(fichier, "r", encoding="ascii") as f:
            texte = f.read()
        _ecrire_atomique(os.path.join(garde, f"fragment-{x}.cf2f"),
                         texte.encode("ascii"))
        print(f"[coffre-CF2] fragment x={x} restauré -> {garde}")
    journaliser(config, f"restauration : {len(a_ecrire)} fragment(s) "
                f"(x={', '.join(str(x) for x, _ in a_ecrire)})")
    return 0


# ---------------------------------------------------------------------------
# État des fragments (spec § 8 : etat-fragments)
# ---------------------------------------------------------------------------

def etat_fragments(config: dict) -> int:
    with open(config["conteneur"], "rb") as f:
        entete = _parser_entete(f.read())
    sel_coffre = entete["sel"].hex()
    valides, avertissements = _fragments_presents(
        config["gardes"], sel_coffre, entete["t"], entete["n"])
    print(f"[coffre-CF2] conteneur : {config['conteneur']}")
    print(f"[coffre-CF2] seuil : t={entete['t']}/n={entete['n']} — "
          f"date {entete['date']}")
    for garde in config["gardes"]:
        idx = config["gardes"].index(garde) + 1
        etat = "PRÉSENT" if idx in valides else "absent"
        print(f"  garde {idx} : {garde} — fragment x={idx} {etat}")
    for a in avertissements:
        print(f"  AVERTISSEMENT : {a}", file=sys.stderr)
    verdict = "VIVANT" if len(valides) >= entete["t"] else "MORT"
    print(f"[coffre-CF2] VERDICT : {len(valides)}/{entete['n']} fragments "
          f"valides — coffre {verdict}")
    return 0


# ---------------------------------------------------------------------------
# Migration CF1 -> CF2 (spec § 10)
# ---------------------------------------------------------------------------

def _charger_cf1():
    """Charge coffre_fort.py par chemin — source unique, zéro duplication."""
    import importlib.util
    chemin = os.path.join(RACINE, "coffre_fort.py")
    if not os.path.isfile(chemin):
        raise ErreurCoffre(f"coffre_fort.py introuvable : {chemin}")
    spec = importlib.util.spec_from_file_location("coffre_fort_cf1", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def migrer(depuis: str, conteneur_cf2: str, racine_gardes: str, n: int,
           t: int, phrase: bytes, config_chemin: str) -> int:
    cf1 = _charger_cf1()
    _, base = cf1.charger(depuis, phrase)          # (entete, base) — CF1
    m = bytearray(secrets.token_bytes(TAILLE_M))
    sel = secrets.token_bytes(32)
    try:
        fragments = decouper(bytes(m), n, t)
        clair = json.dumps(base, ensure_ascii=False).encode("utf-8")
        blob = construire_conteneur(clair, bytes(m), sel, _date_utc(), t, n)
        _ecrire_atomique(conteneur_cf2, blob)
        sel_coffre = _parser_entete(blob)["sel"].hex()
        for x, frag in fragments:
            garde = os.path.join(racine_gardes, f"g{x}")
            os.makedirs(garde, exist_ok=True)
            os.chmod(garde, 0o700)
            _ecrire_atomique(
                os.path.join(garde, f"fragment-{x}.cf2f"),
                serialiser_fragment(x, frag, t, n,
                                    sel_coffre).encode("ascii"))
        config = config_par_defaut(n, t, racine_gardes, conteneur_cf2)
        ecrire_config(config_chemin, config)
    finally:
        _effacer(m)
    print(f"[coffre-CF2] migration CF1 -> CF2 : {conteneur_cf2}")
    print(f"[coffre-CF2] {n} fragments posés sous {racine_gardes} "
          f"(seuil {t}) — copiez {t} fragments hors-ligne (papier/USB, "
          "= le SEUIL :")
    print("[coffre-CF2] deux copies de moins que le seuil et la relève est "
          "impossible après brûlage — spec § 5), puis démarrez la sentinelle "
          "(python3 v06/sentinelle_cf2.py demarrer)")
    print(f"[coffre-CF2] CF1 laissé INTACT : {depuis} (destruction = acte "
          "explicite après vérification — spec § 10)")
    return 0


# ---------------------------------------------------------------------------
# Commandes CLI
# ---------------------------------------------------------------------------

def _config_ou_defauts(args) -> tuple[dict, str]:
    chemin = getattr(args, "config", None) or CHEMIN_CONFIG_DEFAUT
    if os.path.isfile(chemin):
        return lire_config(chemin), chemin
    if not os.path.isfile(CHEMIN_CONTENEUR_DEFAUT):
        raise ErreurCoffre(f"ni config ({chemin}) ni conteneur par défaut "
                           f"({CHEMIN_CONTENEUR_DEFAUT}) — init/migrer d'abord")
    config = config_par_defaut(N_DEFAUT, T_DEFAUT, RACINE_GARDES_DEFAUT,
                               CHEMIN_CONTENEUR_DEFAUT)
    return config, chemin


def cmd_init(args) -> int:
    n, t = args.fragments, args.seuil
    if not 2 <= t <= n <= 255:
        raise ErreurCoffre("2 <= seuil <= fragments <= 255 requis (spec § 2)")
    if os.path.exists(args.conteneur):
        raise ErreurCoffre(f"conteneur déjà présent : {args.conteneur} — "
                           "refus (mono-génération, garde anti-écrasement)")
    base = nouvelle_base(getattr(args, "description_projet", "") or "")
    m = bytearray(secrets.token_bytes(TAILLE_M))
    sel = secrets.token_bytes(32)
    try:
        fragments = decouper(bytes(m), n, t)
        blob = construire_conteneur(
            json.dumps(base, ensure_ascii=False).encode("utf-8"),
            bytes(m), sel, _date_utc(), t, n)
        _ecrire_atomique(args.conteneur, blob)
        sel_coffre = _parser_entete(blob)["sel"].hex()
        for x, frag in fragments:
            garde = os.path.join(args.racine_gardes, f"g{x}")
            os.makedirs(garde, exist_ok=True)
            os.chmod(garde, 0o700)
            _ecrire_atomique(
                os.path.join(garde, f"fragment-{x}.cf2f"),
                serialiser_fragment(x, frag, t, n,
                                    sel_coffre).encode("ascii"))
        ecrire_config(args.config,
                      config_par_defaut(n, t, args.racine_gardes,
                                        args.conteneur))
    finally:
        _effacer(m)
    print(f"[coffre-CF2] coffre neuf : {args.conteneur} (t={t}/n={n})")
    print(f"[coffre-CF2] {n} fragments posés sous {args.racine_gardes}")
    print("[coffre-CF2] LABORATOIRE — la cérémonie réelle passe par migrer "
          "(download/LISEZMOI-coffre-CF2.txt, spec § 12)")
    return 0


def cmd_statut(args) -> int:
    config, _ = _config_ou_defauts(args)
    with open(config["conteneur"], "rb") as f:
        entete = _parser_entete(f.read())
    print(f"[coffre-CF2] conteneur : {config['conteneur']} "
          f"({entete['taille']} o)")
    print(f"[coffre-CF2] version {entete['version']} — suite "
          f"{ALGO_HACHAGE}/{ALGO_KDF}/{ALGO_CHIFFREMENT}")
    print(f"[coffre-CF2] shamir : {entete['shamir']} — date {entete['date']}")
    print(f"[coffre-CF2] empreinte en-tête : "
          f"{empreinte_conteneur(entete['entete'])}")
    return 0


def _avec_deverrouillage(args):
    """Ouvre le coffre et rend (config, base, entete, m) — l'appelant ferme."""
    config, _ = _config_ou_defauts(args)
    base, entete, m, _ = deverrouiller(config["conteneur"], config["gardes"])
    return config, base, entete, m


def cmd_lister(args) -> int:
    config, base, _, m = _avec_deverrouillage(args)
    try:
        if not base["projets"]:
            print("[coffre-CF2] coffre vide (aucun projet)")
            return 0
        for projet in sorted(base["projets"]):
            details = base["projets"][projet]
            print(f"{projet} — {details.get('description', '')}")
            for entree in details.get("entrees", []):
                print(f"    {entree['etiquette']:<24} "
                      f"{entree.get('description', '')}")
    finally:
        _effacer(m)
        del m
    return 0


def _trouver(base: dict, projet: str, etiquette: str):
    for entree in base["projets"].get(projet, {}).get("entrees", []):
        if entree["etiquette"] == etiquette:
            return entree
    return None


def cmd_obtenir(args) -> int:
    config, base, _, m = _avec_deverrouillage(args)
    try:
        entree = _trouver(base, args.projet, args.etiquette)
        if entree is None:
            raise ErreurCoffre(
                f"entrée inconnue : {args.projet}/{args.etiquette}")
        phrase = base64.b64decode(entree["phrase_b64"])
        if args.vers_fichier:
            with open(args.vers_fichier, "wb") as f:
                f.write(phrase)
            os.chmod(args.vers_fichier, 0o600)
            print(f"[coffre-CF2] phrase écrite dans {args.vers_fichier} "
                  "(chmod 600)", file=sys.stderr)
        else:
            try:
                texte = phrase.decode("utf-8")
            except UnicodeDecodeError:
                texte = phrase.hex()
            sys.stdout.write(texte + "\n")
    finally:
        _effacer(m)
        del m
    return 0


def cmd_ajouter(args) -> int:
    if getattr(args, "depuis_fichier", None):
        with open(args.depuis_fichier, "rb") as f:
            phrase = f.read().strip()
    elif getattr(args, "stdin", False):
        phrase = sys.stdin.readline().strip().encode("utf-8")
    elif getattr(args, "generer", False):
        phrase = secrets.token_hex(16).encode("ascii")
        print("[coffre-CF2] NOUVELLE phrase (128 bits) — AFFICHÉE UNE SEULE "
              "FOIS :")
        print("    " + phrase.decode("ascii"))
    else:
        import getpass
        phrase = getpass.getpass("Phrase de l'entrée : ").strip().encode("utf-8")
    if not phrase:
        raise ErreurCoffre("phrase vide — refus (fail-closed)")
    config, base, entete, m = _avec_deverrouillage(args)
    try:
        projet = base["projets"].setdefault(
            args.projet, {"description": getattr(args, "description_projet", "")
                          or "", "entrees": []})
        if _trouver(base, args.projet, args.etiquette) is not None:
            if not args.remplacer:
                raise ErreurCoffre(
                    f"entrée existante : {args.projet}/{args.etiquette} — "
                    "--remplacer pour écraser")
            projet["entrees"] = [e for e in projet["entrees"]
                                 if e["etiquette"] != args.etiquette]
        projet["entrees"].append({
            "etiquette": args.etiquette,
            "description": args.description or "",
            "cree": _date_utc(), "modifie": _date_utc(),
            "phrase_b64": base64.b64encode(phrase).decode("ascii")})
        reverrouiller(config["conteneur"], base, m, entete["sel"],
                      entete["t"], entete["n"])
    finally:
        _effacer(m)
        del m
    print(f"[coffre-CF2] entrée ajoutée : {args.projet}/{args.etiquette}")
    return 0


def cmd_retirer(args) -> int:
    config, base, entete, m = _avec_deverrouillage(args)
    try:
        entrees = base["projets"].get(args.projet, {}).get("entrees", [])
        reste = [e for e in entrees if e["etiquette"] != args.etiquette]
        if len(reste) == len(entrees):
            raise ErreurCoffre(
                f"entrée inconnue : {args.projet}/{args.etiquette}")
        if reste:
            base["projets"][args.projet]["entrees"] = reste
        else:
            del base["projets"][args.projet]
        reverrouiller(config["conteneur"], base, m, entete["sel"],
                      entete["t"], entete["n"])
    finally:
        _effacer(m)
        del m
    print(f"[coffre-CF2] entrée retirée : {args.projet}/{args.etiquette}")
    return 0


def cmd_verifier(args) -> int:
    config, _ = _config_ou_defauts(args)
    with open(config["conteneur"], "rb") as f:
        entete = _parser_entete(f.read())       # fail-closed dès l'en-tête
    print(f"[coffre-CF2] en-tête VALIDE — seuil {entete['shamir']}, "
          f"{entete['taille']} o")
    etat_fragments(config)
    base, entete2, m, _ = deverrouiller(config["conteneur"], config["gardes"])
    try:
        nb = sum(len(p.get("entrees", []))
                 for p in base["projets"].values())
        print(f"[coffre-CF2] déverrouillage COMPLET : verif + AEAD verts — "
              f"{len(base['projets'])} projet(s), {nb} entrée(s)")
    finally:
        _effacer(m)
        del m
    print("[coffre-CF2] verifier : VERT")
    return 0


def cmd_restaurer(args) -> int:
    config, _ = _config_ou_defauts(args)
    return restaurer(config, list(args.fichiers))


def cmd_bruler(args) -> int:
    if not getattr(args, "oui_je_comprends", False):
        print("[coffre-CF2] la destruction est IRRÉVERSIBLE PAR CONSTRUCTION "
              "(D86) — répondez --oui-je-comprends pour bruler")
        return 2
    config, _ = _config_ou_defauts(args)
    bruler(config, "commande manuelle (coffre_cf2.py bruler)")
    return 0


def cmd_migrer(args) -> int:
    import getpass
    if getattr(args, "phrase_stdin", False):
        phrase = sys.stdin.readline().strip().encode("utf-8")
    elif getattr(args, "phrase_fichier", None):
        with open(args.phrase_fichier, "rb") as f:
            phrase = f.read().strip()
    else:
        phrase = getpass.getpass(
            "Phrase de contrôle du coffre CF1 : ").strip().encode("utf-8")
    if not phrase:
        raise ErreurCoffre("phrase de contrôle vide — refus (fail-closed)")
    if os.path.exists(args.conteneur):
        raise ErreurCoffre(f"conteneur CF2 déjà présent : {args.conteneur}")
    return migrer(args.depuis, args.conteneur, args.racine_gardes,
                  args.fragments, args.seuil, phrase, args.config)


# ---------------------------------------------------------------------------
# Autotest (spec § 8 — répertoires TEMPORAIRES, aucun coffre réel touché)
# ---------------------------------------------------------------------------

def cmd_autotest(args) -> int:
    passes, echecs = [], []

    def controle(nom, ok, detail=""):
        (passes if ok else echecs).append(nom if ok else f"{nom} ({detail})")
        print(f"  {'PASS' if ok else 'ÉCHEC'} {nom}"
              + (f" — {detail}" if detail and not ok else ""))

    def refuse(nom, fonction, *a, **k):
        try:
            fonction(*a, **k)
            controle(nom, False, "aucun refus levé")
        except ErreurCoffre as exc:
            controle(nom, str(exc) != "", str(exc))

    import tempfile
    avec = tempfile.TemporaryDirectory(prefix="cf2-autotest-")
    with avec:
        racine = avec.name
        # 1. Shamir : round-trip exhaustif C(5,3) + bornes
        m = secrets.token_bytes(TAILLE_M)
        frags = decouper(m, 5, 3)
        from itertools import combinations
        ok = all(reconstituer([frags[i - 1] for i in c]) == m
                 for c in combinations(range(1, 6), 3))
        controle("shamir-roundtrip-10-combinaisons", ok)
        refuse("shamir-t1-refusé", decouper, m, 5, 1)
        refuse("shamir-t-sup-n-refusé", decouper, m, 2, 3)
        # 2. Conteneur : round-trip + falsifications nommées
        sel = secrets.token_bytes(32)
        base = nouvelle_base("autotest")
        blob = construire_conteneur(
            json.dumps(base).encode(), m, sel, _date_utc(), 3, 5)
        base2, _ = dechiffrer(blob, m)
        controle("conteneur-roundtrip", base2["format"] == 1)
        mauvais = bytearray(m)
        mauvais[0] ^= 1
        refuse("verif-nomme-cle-fausse", dechiffrer, blob, bytes(mauvais))
        tampon = bytearray(blob)
        tampon[-1] ^= 1
        refuse("aead-nomme-tampon", dechiffrer, bytes(tampon), m)
        # 3. Fragments + gardes : cycle vie/mort/relève COMPLET
        conteneur = os.path.join(racine, "coffre.bin")
        gardes = [os.path.join(racine, f"g{i}") for i in range(1, 6)]
        _ecrire_atomique(conteneur, blob)
        sel_coffre = _parser_entete(blob)["sel"].hex()
        for x, frag in frags:
            os.makedirs(gardes[x - 1], exist_ok=True)
            with open(os.path.join(gardes[x - 1], f"fragment-{x}.cf2f"),
                      "w", encoding="ascii") as f:
                f.write(serialiser_fragment(x, frag, 3, 5, sel_coffre))
        base3, _, mram, _ = deverrouiller(conteneur, gardes)
        controle("deverrouillage-3-sur-5", base3 == base)
        _effacer(mram)
        config = config_par_defaut(5, 3, os.path.join(racine, "gardes"),
                                   conteneur)
        config["gardes"] = gardes
        config["pv_dir"] = os.path.join(racine, "pv")
        config["journal"] = os.path.join(racine, "journal.txt")
        copies = [os.path.join(racine, f"copie-{x}.txt") for x in (3, 4, 5)]
        for x, copie in zip((3, 4, 5), copies):
            shutil_fragment = os.path.join(gardes[x - 1], f"fragment-{x}.cf2f")
            with open(shutil_fragment, "r", encoding="ascii") as f_in, \
                    open(copie, "w", encoding="ascii") as f_out:
                f_out.write(f_in.read())
        pv = bruler(config, "autotest")
        controle("brulage-pv-ecrit", os.path.isfile(pv))
        reste = [f for g in gardes for f in os.listdir(g)]
        controle("brulage-gardes-vides", reste == [], str(reste))
        refuse("coffre-mort-refuse", deverrouiller, conteneur, gardes)
        # Sémantique du SEUIL de relève : 2 copies < seuil 3 -> toujours mort
        restaurer(config, copies[:2])
        refuse("releve-2-copies-toujours-morte", deverrouiller, conteneur,
               gardes)
        # La TROISIÈME copie franchit le seuil -> vie (spec § 5)
        restaurer(config, [copies[2]])
        base4, _, mram2, _ = deverrouiller(conteneur, gardes)
        controle("releve-3-copies-restaure-vie", base4 == base)
        _effacer(mram2)
        # 4. Le coffre RÉEL n'existe pas / n'est pas touché
        controle("aucun-coffre-reel-touché",
                 not os.path.exists(CHEMIN_CONTENEUR_DEFAUT))
    print(f"[coffre-CF2] autotest : {len(passes)} PASS, "
          f"{len(echecs)} ÉCHEC(s)")
    return 0 if not echecs else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _construire_parseur() -> argparse.ArgumentParser:
    parseur = argparse.ArgumentParser(
        description="Coffre CF2 — interrupteur d'homme mort (D86, v0.6.0 axe 2)")
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--config", help="config JSON (défaut : "
                                          ".keys/config_cf2.json)")
    sous = parseur.add_subparsers(dest="commande", required=True)

    p = sous.add_parser("init", help="coffre neuf de LABORATOIRE",
                        parents=[parent])
    p.add_argument("--fragments", type=int, default=N_DEFAUT)
    p.add_argument("--seuil", type=int, default=T_DEFAUT)
    p.add_argument("--racine-gardes", default=RACINE_GARDES_DEFAUT)
    p.add_argument("--conteneur", default=CHEMIN_CONTENEUR_DEFAUT)
    p.add_argument("--description-projet", default="")
    p.set_defaults(func=cmd_init)

    p = sous.add_parser("migrer", help="CF1 -> CF2 (cérémonie réelle)",
                        parents=[parent])
    p.add_argument("--depuis", default=os.path.join(KEYS_DIR, "coffre_fort.bin"))
    p.add_argument("--phrase-stdin", action="store_true")
    p.add_argument("--phrase-fichier")
    p.add_argument("--fragments", type=int, default=N_DEFAUT)
    p.add_argument("--seuil", type=int, default=T_DEFAUT)
    p.add_argument("--racine-gardes", default=RACINE_GARDES_DEFAUT)
    p.add_argument("--conteneur", default=CHEMIN_CONTENEUR_DEFAUT)
    p.set_defaults(func=cmd_migrer)

    p = sous.add_parser("statut", help="en-tête clair seul (aucune clé)",
                        parents=[parent])
    p.set_defaults(func=cmd_statut)
    p = sous.add_parser("etat-fragments", help="gardes / seuil / verdict",
                        parents=[parent])
    p.set_defaults(func=cmd_etat_cli)
    p = sous.add_parser("lister", help="projets et entrées", parents=[parent])
    p.add_argument("projet", nargs="?")
    p.set_defaults(func=cmd_lister)

    p = sous.add_parser("obtenir", help="une entrée (sortie locale)",
                        parents=[parent])
    p.add_argument("projet")
    p.add_argument("etiquette")
    p.add_argument("--vers-fichier")
    p.set_defaults(func=cmd_obtenir)

    p = sous.add_parser("ajouter", help="nouvelle entrée", parents=[parent])
    p.add_argument("projet")
    p.add_argument("etiquette")
    p.add_argument("--description")
    p.add_argument("--description-projet", default="")
    p.add_argument("--depuis-fichier")
    p.add_argument("--stdin", action="store_true")
    p.add_argument("--generer", action="store_true")
    p.add_argument("--remplacer", action="store_true")
    p.set_defaults(func=cmd_ajouter)

    p = sous.add_parser("retirer", help="supprime une entrée", parents=[parent])
    p.add_argument("projet")
    p.add_argument("etiquette")
    p.set_defaults(func=cmd_retirer)

    p = sous.add_parser("verifier", help="intégrité complète",
                        parents=[parent])
    p.set_defaults(func=cmd_verifier)
    p = sous.add_parser("restaurer", help="remise hors-ligne (atomique)",
                        parents=[parent])
    p.add_argument("fichiers", nargs="+")
    p.set_defaults(func=cmd_restaurer)

    p = sous.add_parser("bruler", help="destruction manuelle (irréversible)",
                        parents=[parent])
    p.add_argument("--oui-je-comprends", action="store_true",
                   dest="oui_je_comprends")
    p.set_defaults(func=cmd_bruler)

    p = sous.add_parser("autotest", help="autocontrôles (temporaire)",
                        parents=[parent])
    p.set_defaults(func=cmd_autotest)
    return parseur


def cmd_etat_cli(args) -> int:
    config, _ = _config_ou_defauts(args)
    return etat_fragments(config)


def main() -> int:
    parseur = _construire_parseur()
    args = parseur.parse_args()
    try:
        return args.func(args)
    except ErreurCoffre as exc:
        print(f"ECHEC : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
