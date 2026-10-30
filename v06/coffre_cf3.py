#!/usr/bin/env python3
"""coffre_cf3.py — CF3 : la serrure à triple scellement et le cycle en deux
actes (D121, v0.6.0 axe 4).

Spécification : v06/I/CF3/README.md (R2 écrite-avant-code — CE fichier
l'instancie, aucun écart toléré ; la spec est ENTRÉE dans l'arbre scellé
à la re-cérémonie D126, en compagnie de l'erratum § 12 du README CF2,
consigné 47e704f).

CF3 est la génération suivante de la serrure du coffre :

  - TROIS éléments (spec § 2) : K_user (Argon2id de la phrase — INVARIANT à
    travers les époques, la demande du terrain « clé utilisateur qui ne
    change pas »), S_serrure (moitié MACHINE, aléa frais par époque, en-tête
    clair du conteneur) et S_piège (moitié MÉDIA SÉPARÉ, aléa frais par
    époque) ; le hash du projet n'est qu'un LIANT (contexte HKDF), jamais
    une source d'entropie — un hash public ne protège pas, il lie ;
  - la SENTINELLE INSTANTANÉE (spec § 5) : l'exigence D120 (« si le
    déverrouillage est tenté et qu'elle n'est pas lancée, tous nos efforts
    sont inutiles ») réalisée par INVOCATION — vérifications in-process à
    CHAQUE acte — au lieu d'un démon résident usurpable (faux heart-beat,
    borne D120) : le piège EST le témoin, et il est hors machine. Sans lui,
    le déverrouillage est IMPOSSIBLE (pas seulement refusé) et le voleur de
    la machine seule ne peut même pas TESTER des phrases (champ verif, spec
    § 3 — il lui manque V_piège, publique mais portée par le média) ;
  - le CYCLE EN DEUX ACTES (spec § 6) : ACTE I ouverture (phrase + piège →
    brouillon chiffré sous clé de session éphémère ; les clés maîtresses
    meurent ; le canonique n'est JAMAIS réécrit pendant la session), SESSION
    (une panne auto-nettoie : K_session meurt, le brouillon devient déchet
    indéchiffrable), ACTE II clôture (phrase RETAPÉE + média REBRANCHÉ ;
    clé de clôture LIÉE AU CONTENU — elle ne scelle QUE l'état affiché ;
    moitiés fraîches, époque + 1 ; re-lecture à froid AVANT le remplacement
    atomique — le canonique n'est remplacé que par un conteneur PROUVÉ) ;
  - modes de défaillance SÉPARÉS (spec § 5) : phrase erronée = BÉNIGNE
    (PhraseErronee, réessai avec délai croissant, JAMAIS de destruction) ;
    falsification PROUVÉE côté machine (piège intègre + phrase vérifiée +
    empreinte/AEAD échoue) = destruction LOCALE + PV — JAMAIS le média du
    piège, JAMAIS les fragments CF2 (coexistence spec § 12 : la destruction
    reste survivable).

Discipline RAM (spec § 8) : K_user, KEK, moitiés et K_session ne vivent qu'en
bytearray, effacés après usage au mieux de Python ; aucun secret n'entre
dans un journal, un PV, une sortie ou une exception. Les conteneurs et
phrases RÉELS ne sont JAMAIS touchés par les autocontrôles (répertoires
temporaires — discipline D105).

Usage (depuis triade/) :
  python3 v06/coffre_cf3.py init [--piege-dir DIR] [--description D]
       [--phrase-stdin]
  python3 v06/coffre_cf3.py ouvrir [--piege-dir DIR | --piege FICHIER]
       [--phrase-stdin] [--epoque-attendue N]
  python3 v06/coffre_cf3.py verifier [--piege-dir DIR | --piege FICHIER]
       [--epoque-attendue N] [--phrase-stdin]
  python3 v06/coffre_cf3.py statut
  python3 v06/coffre_cf3.py bruler --oui-je-comprends
  python3 v06/coffre_cf3.py migrer --conteneur-cf2 F [--gardes RACINE]
       [--config-cf2 F] --piege-dir DIR [--conteneur F] [--phrase-stdin]
  python3 v06/coffre_cf3.py detruire-cf2 --conteneur-cf2 F
       [--conteneur F] --oui-je-comprends
  python3 v06/coffre_cf3.py autotest

En CLI, `ouvrir` porte la sentinelle complète et rend son verdict SANS écrire
de brouillon : une session CLI mourrait avec son processus (K_session morte,
brouillon déchet). Le cycle complet en deux actes vit dans l'API Python —
prouvé par v06/test_coffre_cf3.py — et entrera dans le GUI de cérémonie
après preuve terrain (spec § 1). `--piege-dir` par défaut : .keys/pieges-cf3
(COMMODITÉ DE LABORATOIRE — sur le terrain, passez le chemin du MÉDIA du
piège : clef USB du sachet ; un média par coffre, spec § 4). `--phrase-stdin`
= UN essai, sans confirmation (automatisation de laboratoire).

MIGRATION CF2 → CF3 (spec § 12, D127 — la preuve terrain étant acquise,
l'outillage naît) : `migrer` est une CÉRÉMONIE en quatre actes — (1) CF2
déverrouillé une dernière fois (porte D120 honorée), (2) base re-scellée
schéma identique (RIEN À TRADUIRE), (3) re-lecture à froid du scellage,
(4) conteneur CF2 laissé INTACT — sa destruction est EXPLICITE
(`detruire-cf2`, après verdict humain ; les fragments CF2 et leurs copies
hors-ligne restent la relève HISTORIQUE). Le GUI de cérémonie de migration
(v06/migration_cf3_gui.py) guide les quatre actes avec le trio D122.

Dépendances : argon2-cffi, pynacl, cryptography (la pile du dépôt — miroir
CF1/CF2).
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import secrets
import sys
import tempfile
import time

try:
    from argon2.low_level import Type, hash_secret_raw
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from nacl.bindings import (crypto_aead_xchacha20poly1305_ietf_decrypt,
                               crypto_aead_xchacha20poly1305_ietf_encrypt)
except ImportError as exc:  # pragma: no cover
    print(f"ECHEC : dépendance manquante ({exc}) — "
          "pip install argon2-cffi pynacl cryptography", file=sys.stderr)
    sys.exit(1)

# coffre_cf2 est la source unique de l'écriture atomique D119 (Windows-safe)
# et de la discipline RAM — CF3 ne les duplique JAMAIS.
_V06_DIR = os.path.dirname(os.path.abspath(__file__))
if _V06_DIR not in sys.path:
    sys.path.insert(0, _V06_DIR)
try:
    import coffre_cf2 as _cf2
except ImportError as exc:  # pragma: no cover
    print(f"ECHEC : v06/coffre_cf2.py introuvable ({exc}) — CF3 réutilise "
          "son écriture atomique D119 et sa discipline RAM", file=sys.stderr)
    sys.exit(1)

RACINE = _cf2.RACINE
KEYS_DIR = _cf2.KEYS_DIR
CONTENEUR_DEFAUT = os.path.join(KEYS_DIR, "coffre_cf3.bin")
PIEGE_DIR_DEFAUT = os.path.join(KEYS_DIR, "pieges-cf3")   # labo — spec § 4

MAGIC = b"TRIADE-CF3"
MAGIC_BROUILLON = b"TRIADE-CF3-BROUILLON"
MAGIC_PIEGE = "TRIADE-CF3-PIEGE v1"
FORMAT_VERSION = 1
PROTOCOLE = "0.6.0"
ALGO_KDF = "argon2id(65536,3,1)"      # miroir CF1 — plancher FORMAT_CARTE § 3.1
ARGON2_MEM = 65536                     # Kio
ARGON2_ITER = 3
ARGON2_PAR = 1
ARGON2_LONG = 32
HKDF_INFO = b"triade-CF3/v1"           # contexte DISTINCT de CF1/CF2
HKDF_INFO_VERIF = b"triade-CF3/verif/v1"
SEL_TAG_PIEGE = b"TRIADE-CF3-piege"
TAILLE_MOITIE = 32
TAILLE_V_PIEGE = 16
TAILLE_SEL_ARGON = 16
TAILLE_SEL_HKDF = 32
MOTIF_PIEGE = "piege-CF3-epoque-{}.txt"
HEXDIGITS = set("0123456789abcdef")

# spec § 5.4 — délai croissant sur phrase erronée : 1, 2, 4 s, plafond 8 s
# (le plafond borne aussi l'auto-verrouillage de compte par soi-même).
DELAI_MAX = 8.0

# Injection de panne (spec § 6, analyse de panne — prouvée par la suite de
# falsifiabilité) : un test pose C._DEFAUT_SIMULE = "<point>" et la clôture
# meurt NOMMÉE à ce point précis. Points : avant-piege, apres-piege,
# apres-staging, avant-replace, apres-replace.
_DEFAUT_SIMULE = None


class ErreurCoffre(RuntimeError):
    """Tout échec nommé de la serrure — fail-closed (spec § 5 : un verdict
    muet n'est pas une preuve ; miroir ErreurCoffre CF2 § 13)."""


class PhraseErronee(ErreurCoffre):
    """UNIQUE mode bénin (spec § 5.4) : phrase erronée — réessai possible,
    JAMAIS de destruction. Borne consignée : un piège entièrement forgé se
    présente pareil (verif diverge) — bénin, refus nommé."""


# ---------------------------------------------------------------------------
# Chemins frères du conteneur (tout vit près du coffre — répertoires
# temporaires des tests inclus, discipline D105)
# ---------------------------------------------------------------------------

def _dir(conteneur_chemin: str) -> str:
    return os.path.dirname(conteneur_chemin) or "."


def chemin_brouillon(conteneur_chemin: str) -> str:
    return os.path.join(_dir(conteneur_chemin), "brouillon-cf3.bin")


def chemin_journal(conteneur_chemin: str) -> str:
    return os.path.join(_dir(conteneur_chemin), "journal-cf3.txt")


def chemin_miroir(conteneur_chemin: str) -> str:
    """Miroir LOCAL d'époque (spec § 9 — le plus faible des trois témoins :
    effaçable par un attaquant admin ; la carte papier et le journal Git
    sont les témoins hors-bande)."""
    return os.path.join(_dir(conteneur_chemin), "epoque-cf3.txt")


def chemin_pv_dir(conteneur_chemin: str) -> str:
    return os.path.join(_dir(conteneur_chemin), "pv-cf3")


def chemin_piege(piege_dir: str, epoque: int) -> str:
    return os.path.join(piege_dir, MOTIF_PIEGE.format(epoque))


def trouver_piege(piege_dir: str, epoque: int):
    """Chemin du piège d'ÉPOQUE ÉGALE au conteneur (spec § 6 : la reprise
    après panne prend toujours le piège qui correspond au canonique)."""
    chemin = chemin_piege(piege_dir, epoque)
    return chemin if os.path.isfile(chemin) else None


# ---------------------------------------------------------------------------
# Journal et miroir (JAMAIS de secret — spec § 8)
# ---------------------------------------------------------------------------

def _journal(conteneur_chemin: str, message: str) -> None:
    """Best-effort (miroir _porte_journal CF2 D120) : un journal impossible
    à écrire ne noie JAMAIS le refus — le refus prime, le journal témoigne."""
    try:
        chemin = chemin_journal(conteneur_chemin)
        os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
        with open(chemin, "a", encoding="utf-8") as f:
            f.write(f"{_cf2._date_utc()} {message}\n")
    except OSError:
        pass


def _ecrire_miroir(conteneur_chemin: str, epoque: int, checksum: str) -> None:
    _cf2._ecrire_atomique(chemin_miroir(conteneur_chemin),
                          f"{epoque} {checksum}\n".encode("ascii"))


def _lire_miroir(conteneur_chemin: str):
    """Époque du miroir local, ou None si absent. Malformé → refus NOMMÉ
    (fail-closed : le miroir est écrit ATOMIQUEMENT, une écriture partielle
    n'existe pas — un miroir corrompu est une atteinte, pas une panne)."""
    chemin = chemin_miroir(conteneur_chemin)
    if not os.path.isfile(chemin):
        return None
    try:
        with open(chemin, "r", encoding="ascii") as f:
            premiere = f.readline().strip()
    except (OSError, UnicodeDecodeError) as exc:
        raise ErreurCoffre(f"miroir d'époque illisible : {chemin} ({exc}) — "
                           "refus (spec § 9)")
    parties = premiere.split()
    if not parties or not parties[0].isdigit():
        raise ErreurCoffre(f"miroir d'époque corrompu : {premiere!r} — refus "
                           "(écriture atomique : une panne n'écrit pas ça — "
                           "spec § 9)")
    return int(parties[0])


# ---------------------------------------------------------------------------
# Dérivations (spec § 3)
# ---------------------------------------------------------------------------

def cle_utilisateur(phrase: bytes, sel_argon: bytes) -> bytes:
    """K_user = Argon2id(phrase, sel_argon) — INVARIANT à travers les
    époques (spec § 2 : sel_argon et paramètres posés à l'init, jamais
    retouchés par une clôture)."""
    if not phrase:
        raise ErreurCoffre("phrase VIDE — refus (spec § 2)")
    if len(sel_argon) != TAILLE_SEL_ARGON:
        raise ErreurCoffre(f"sel_argon != {TAILLE_SEL_ARGON} o (spec § 3)")
    return hash_secret_raw(secret=phrase, salt=sel_argon,
                           time_cost=ARGON2_ITER, memory_cost=ARGON2_MEM,
                           parallelism=ARGON2_PAR, hash_len=ARGON2_LONG,
                           type=Type.ID)


def _hkdf(ikm: bytes, sel: bytes, info: bytes, longueur: int = 32) -> bytes:
    return HKDF(algorithm=hashes.SHA256(), length=longueur, salt=sel,
                info=info).derive(ikm)


def derive_kek(k_user, s_serrure, s_piege, sel_hkdf: bytes, epoque: int,
               h_projet: bytes) -> bytes:
    """KEK = HKDF(K_user ‖ S_serrure ‖ S_piège ; sel_hkdf ;
    « triade-CF3/v1|‖époque‖H_projet ») — les TROIS éléments entrent, le hash
    du projet n'est que LIANT (spec § 2/§ 3)."""
    return _hkdf(bytes(k_user) + bytes(s_serrure) + bytes(s_piege), sel_hkdf,
                 HKDF_INFO + b"|" + int(epoque).to_bytes(8, "little")
                 + h_projet)


def derive_verif(k_user, v_piege, sel_hkdf: bytes) -> bytes:
    """verif = sha256(HKDF(K_user ‖ V_piège ; sel_hkdf ; « …/verif »))[:16]
    — V_piège est PUBLIQUE mais vit sur le média : le conteneur seul ne
    permet AUCUN essai de phrase hors ligne (spec § 3)."""
    return hashlib.sha256(_hkdf(bytes(k_user) + bytes(v_piege), sel_hkdf,
                                HKDF_INFO_VERIF)).digest()[:16]


def tag_piege(epoque: int, h_projet: bytes, s_piege, v_piege) -> bytes:
    """sha256(« TRIADE-CF3-piege‖époque‖H_projet‖S_piège‖V_piège »)[:8] —
    nomme la corruption du média sans divulguer (miroir tag_fragment CF2
    § 4). PAS un MAC : intégrité du média, pas authenticité (spec § 4)."""
    return hashlib.sha256(SEL_TAG_PIEGE
                          + int(epoque).to_bytes(8, "little") + h_projet
                          + bytes(s_piege) + bytes(v_piege)).digest()[:8]


# ---------------------------------------------------------------------------
# Conteneur TRIADE-CF3 (spec § 3)
# ---------------------------------------------------------------------------

def _params_octets() -> bytes:
    return (ARGON2_MEM.to_bytes(4, "little") + ARGON2_ITER.to_bytes(4, "little")
            + ARGON2_PAR.to_bytes(4, "little"))


def _aad(epoque: int, h_projet: bytes, sel_argon: bytes, sel_hkdf: bytes,
         s_serrure: bytes, nonce: bytes) -> bytes:
    return (MAGIC + FORMAT_VERSION.to_bytes(2, "little")
            + int(epoque).to_bytes(8, "little") + h_projet + sel_argon
            + _params_octets() + sel_hkdf + s_serrure + nonce)


def _sceller_avec_kek(clair: bytes, kek: bytes, verif: bytes,
                      sel_argon: bytes, sel_hkdf: bytes, s_serrure: bytes,
                      epoque: int, h_projet: bytes) -> bytes:
    """Scellage bas niveau : en-tête clair (AAD intégral) + empreinte + verif
    + AEAD (miroir CF2 § 11.2 : l'empreinte est posée APRÈS la zone AAD, le
    tag AEAD reste la preuve, l'empreinte la redondance nommée). Le test de
    course (spec § 10) s'en sert aussi : c'est le FORMAT PUBLIÉ, un attaquant
    l'a sous la main."""
    if len(sel_hkdf) != TAILLE_SEL_HKDF:
        raise ErreurCoffre(f"sel_hkdf != {TAILLE_SEL_HKDF} o (spec § 3)")
    if len(s_serrure) != TAILLE_MOITIE:
        raise ErreurCoffre(f"S_serrure != {TAILLE_MOITIE} o (spec § 3)")
    nonce = secrets.token_bytes(24)
    aad = _aad(epoque, h_projet, sel_argon, sel_hkdf, s_serrure, nonce)
    chiffretexte = crypto_aead_xchacha20poly1305_ietf_encrypt(
        clair, aad, nonce, kek)
    empreinte = hashlib.sha256(chiffretexte).digest()
    return aad + empreinte + verif + chiffretexte


def construire_conteneur(clair: bytes, k_user, s_serrure, s_piege, v_piege,
                         sel_argon: bytes, sel_hkdf: bytes, epoque: int,
                         h_projet: bytes) -> bytes:
    """Chemin HONNÊTE : KEK et verif DÉRIVÉS des éléments (spec § 3), puis
    scellage bas niveau."""
    kek = derive_kek(k_user, s_serrure, s_piege, sel_hkdf, epoque, h_projet)
    verif = derive_verif(k_user, v_piege, sel_hkdf)
    return _sceller_avec_kek(clair, kek, verif, sel_argon, sel_hkdf,
                             bytes(s_serrure), epoque, h_projet)


def parser_entete(blob: bytes) -> dict:
    """En-tête clair complet — fail-closed NOMMÉ, liste blanche (spec § 3)."""
    fin_aad = 10 + 2 + 8 + 32 + 16 + 12 + 32 + 32 + 24
    fin_entete = fin_aad + 32 + 16
    if len(blob) < fin_entete:
        raise ErreurCoffre("conteneur trop court (en-tête tronqué)")
    if blob[:10] != MAGIC:
        raise ErreurCoffre(f"magic invalide : {blob[:10]!r} (TRIADE-CF3 "
                           "attendu)")
    version = int.from_bytes(blob[10:12], "little")
    if version != FORMAT_VERSION:
        raise ErreurCoffre(f"version conteneur non gérée : {version}")
    epoque = int.from_bytes(blob[12:20], "little")
    if epoque < 1:
        raise ErreurCoffre(f"époque invalide : {epoque} (>= 1 attendu)")
    h_projet = blob[20:52]
    sel_argon = blob[52:68]
    params = blob[68:80]
    if params != _params_octets():
        raise ErreurCoffre("paramètres Argon2id hors liste blanche : "
                           f"{params.hex()} (spec § 2 — plancher FORMAT_CARTE "
                           "§ 3.1, miroir CF1)")
    sel_hkdf = blob[80:112]
    s_serrure = blob[112:144]
    nonce = blob[144:168]
    empreinte = blob[fin_aad:fin_aad + 32]
    verif = blob[fin_aad + 32:fin_entete]
    chiffretexte = blob[fin_entete:]
    return {"version": version, "epoque": epoque, "h_projet": h_projet,
            "sel_argon": sel_argon, "sel_hkdf": sel_hkdf,
            "s_serrure": s_serrure, "nonce": nonce, "empreinte": empreinte,
            "verif": verif, "aad": blob[:fin_aad],
            "chiffretexte": chiffretexte, "entete": blob[:fin_entete],
            "taille": len(blob)}


def empreinte_conteneur(entete: bytes) -> str:
    return hashlib.sha256(entete).hexdigest()


# ---------------------------------------------------------------------------
# Fichier piège (spec § 4)
# ---------------------------------------------------------------------------

def serialiser_piege(epoque: int, h_projet: bytes, s_piege: bytes,
                     v_piege: bytes) -> str:
    return (f"{MAGIC_PIEGE}\n"
            f"epoque: {epoque}\n"
            f"projet: {h_projet.hex()}\n"
            f"piege: {bytes(s_piege).hex()}\n"
            f"verif: {bytes(v_piege).hex()}\n"
            f"tag: {tag_piege(epoque, h_projet, s_piege, v_piege).hex()}\n")


def parser_piege(texte: str) -> dict:
    """Parse + vérifications nommées (magic, champs, hex, tag) — spec § 4."""
    lignes = [l.strip() for l in texte.splitlines() if l.strip()]
    if not lignes or lignes[0] != MAGIC_PIEGE:
        raise ErreurCoffre(f"magic piège invalide ({MAGIC_PIEGE} attendu)")
    champs = {}
    for l in lignes[1:]:
        if ":" not in l:
            raise ErreurCoffre(f"ligne de piège malformée : {l!r}")
        clef, _, valeur = l.partition(":")
        champs[clef.strip()] = valeur.strip()
    manquants = [c for c in ("epoque", "projet", "piege", "verif", "tag")
                 if c not in champs]
    if manquants:
        raise ErreurCoffre(f"champs manquants dans le piège : {manquants}")
    if not champs["epoque"].isdigit() or int(champs["epoque"]) < 1:
        raise ErreurCoffre(f"époque du piège invalide : {champs['epoque']!r}")
    epoque = int(champs["epoque"])
    hexa = {}
    for clef, taille in (("projet", 64), ("piege", 64), ("verif", 32),
                         ("tag", 16)):
        valeur = champs[clef].lower()
        if len(valeur) != taille or any(c not in HEXDIGITS for c in valeur):
            raise ErreurCoffre(f"champ {clef} du piège : {taille} caractères "
                               f"hex attendus ({champs[clef]!r})")
        hexa[clef] = bytes.fromhex(valeur)
    if hexa["tag"] != tag_piege(epoque, hexa["projet"], hexa["piege"],
                                hexa["verif"]):
        raise ErreurCoffre("tag du piège INVALIDE — média corrompu ou "
                           "falsifié (spec § 4)")
    return {"epoque": epoque, "projet": hexa["projet"], "s_piege": hexa["piege"],
            "v_piege": hexa["verif"]}


def _lire_piege(piege_chemin: str) -> dict:
    try:
        with open(piege_chemin, "r", encoding="ascii") as f:
            return parser_piege(f.read())
    except FileNotFoundError:
        raise ErreurCoffre(f"piège ABSENT : {piege_chemin} — déverrouillage "
                           "IMPOSSIBLE : la seconde moitié de la serrure est "
                           "sur le média séparé (spec § 4/§ 5.1)")
    except (OSError, UnicodeDecodeError) as exc:
        raise ErreurCoffre(f"piège illisible : {piege_chemin} ({exc}) — refus "
                           "(spec § 5.2)")


# ---------------------------------------------------------------------------
# La destruction locale (spec § 7) — ne touche QUE la machine
# ---------------------------------------------------------------------------

def _detruire_fichier(chemin: str) -> None:
    """Trois passes + truncate + renommage aléatoire + unlink (miroir
    bruler CF2 § 7)."""
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
    nom_alea = os.path.join(os.path.dirname(chemin), secrets.token_hex(16))
    os.rename(chemin, nom_alea)
    os.unlink(nom_alea)
    _cf2._fsync_repertoire(os.path.dirname(chemin))


def _destruction_locale(conteneur_chemin: str, raison: str,
                        brouillon_chemin=None) -> str:
    """Destruction LOCALE + PV nommé (spec § 7) : conteneur, staging,
    brouillon — JAMAIS le média du piège, JAMAIS les fragments CF2 ni aucune
    autre création du dossier (la destruction n'est pas un balai)."""
    pv_dir = chemin_pv_dir(conteneur_chemin)
    os.makedirs(pv_dir, exist_ok=True)
    lignes_pv = [
        "PROCÈS-VERBAL DE DESTRUCTION LOCALE — TRIADE-CF3 (spec § 7, D121)",
        f"date : {_cf2._date_utc()}",
        f"raison : {raison}",
        "passes : aléatoire (CSPRNG) puis 0xFF puis 0x00, fsync par passe",
        "",
    ]
    cibles = [conteneur_chemin, conteneur_chemin + ".staging"]
    if brouillon_chemin:
        cibles.append(brouillon_chemin)
    detruits = 0
    for cible in cibles:
        if os.path.isfile(cible):
            _detruire_fichier(cible)
            detruits += 1
            lignes_pv.append(f"DETRUIT : {cible} (3 passes, tronqué, "
                             "renommé, unlink, fsync rép.)")
    lignes_pv.append("")
    lignes_pv.append(f"total : {detruits} artefact(s) machine détruit(s)")
    lignes_pv.append("le MÉDIA du piège est INTACT (externe — c'est la "
                     "relève) ; les fragments CF2 et copies hors-ligne sont "
                     "INTACTS (coexistence spec § 12)")
    lignes_pv.append("RELÈVE : copie hors-ligne du couple conteneur+piège, "
                     "ou re-scellement depuis CF2 (cérémonie spec § 12)")
    horodatage = _cf2._date_utc().replace(":", "").replace("-", "")
    base_pv = os.path.join(pv_dir, f"pv-destruction-cf3-{horodatage}")
    chemin_pv = base_pv + ".txt"
    suffixe = 2
    while os.path.exists(chemin_pv):
        # D123 : DEUX destructions la même seconde (prouvé par le rapport
        # terrain D122 — t8 rendait DEUX fois le MÊME chemin de PV : le
        # second ÉCRASAIT le premier) : chaque destruction laisse SON
        # procès-verbal — suffixe -2, -3, … jamais un écrasement.
        chemin_pv = f"{base_pv}-{suffixe}.txt"
        suffixe += 1
    with open(chemin_pv, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes_pv) + "\n")
    os.chmod(chemin_pv, 0o600)
    _journal(conteneur_chemin, f"PORTE : DESTRUCTION LOCALE — {raison} "
              f"(PV {chemin_pv})")
    print(f"[CF3] DESTRUCTION LOCALE : {detruits} artefact(s) — PV : "
          f"{chemin_pv}")
    return chemin_pv


# ---------------------------------------------------------------------------
# La sentinelle instantanée (spec § 5 — l'ordre EST la loi)
# ---------------------------------------------------------------------------

def _defaut(point: str) -> None:
    """Injection de panne (spec § 6) : meurt NOMMÉE au point posé par le
    test — la clôture est rejouable, l'état est vérifiable."""
    if _DEFAUT_SIMULE == point:
        raise ErreurCoffre(f"DÉFAUT SIMULÉ : {point} (spec § 6 — injection "
                           "de panne de la suite de falsifiabilité)")


def sentinelle_instantanee(blob: bytes, piege_chemin: str, phrase: bytes,
                           conteneur_chemin: str, brouillon_chemin=None,
                           epoque_attendue=None, miroir=True,
                           consigner=True) -> tuple[dict, dict]:
    """L'ordre NORMATIF (spec § 5) — à TOUT acte qui déverrouille :

    1. piège PRÉSENT — absent : impossible, rien n'est lu, rien ne brûle ;
    2. piège INTÈGRE (tag) — invalide : refus SANS destruction (le média est
       hors limite de confiance — corruption bénigne possible) ;
    3. cohérence des champs publics : époque du piège == époque du conteneur
       (piège PÉRIMÉ — anti roll-back), H_projet == (piège d'un autre coffre),
       conteneur >= miroir local (RETOUR EN ARRIÈRE), == témoin hors-bande ;
    4. PHRASE (verif) — diverge : PhraseErronee, réessai, JAMAIS de
       destruction ;
    5. empreinte + AEAD — échec APRÈS 1–4 verts : falsification/corruption
       PROUVÉE côté machine → destruction LOCALE + PV (spec § 7).

    Retour (base, entete). `consigner=False` pour la re-lecture à froid
    (pas de bruit d'événements — les vérifications courent pareil).
    """
    entete = parser_entete(blob)

    # 1 — piège présent (sine qua non D120, réalisé sans démon)
    if not piege_chemin or not os.path.isfile(piege_chemin):
        if consigner:
            _journal(conteneur_chemin, "PORTE : déverrouillage IMPOSSIBLE — "
                     "piège ABSENT (la seconde moitié de la serrure est sur "
                     "le média séparé)")
        raise ErreurCoffre("déverrouillage IMPOSSIBLE : la seconde moitié de "
                           "la serrure (piège) est ABSENTE — branchez le "
                           "média du piège (spec § 5.1 : sine qua non D120, "
                           "réalisé par invocation — le témoin est hors "
                           "machine)")

    # 2 — piège intègre
    try:
        piege = _lire_piege(piege_chemin)
    except ErreurCoffre as exc:
        if consigner:
            _journal(conteneur_chemin, f"PORTE : refus — piège illisible ou "
                     f"tag invalide ({exc})")
        raise ErreurCoffre(f"{exc} — refus SANS destruction : le média est "
                           "hors limite de confiance (une corruption bénigne "
                           "se relit depuis les copies hors-ligne — spec "
                           "§ 5.2 ; la destruction attend la PREUVE "
                           "cryptographique, § 7)") from exc

    # 3 — cohérence des champs publics
    if piege["epoque"] != entete["epoque"]:
        if consigner:
            _journal(conteneur_chemin, f"PORTE : refus — piège PÉRIMÉ "
                     f"(époque {piege['epoque']} ≠ conteneur "
                     f"{entete['epoque']})")
        raise ErreurCoffre(f"piège PÉRIMÉ : époque du piège "
                           f"{piege['epoque']} ≠ époque du conteneur "
                           f"{entete['epoque']} — anti retour-en-arrière "
                           "(spec § 9 ; prenez le piège de l'époque du "
                           "conteneur)")
    if piege["projet"] != entete["h_projet"]:
        if consigner:
            _journal(conteneur_chemin, "PORTE : refus — H_projet divergent "
                     "(piège d'un AUTRE coffre)")
        raise ErreurCoffre("H_projet du piège divergent — piège d'un AUTRE "
                           "coffre (spec § 5.3)")
    if miroir:
        miroir_epoque = _lire_miroir(conteneur_chemin)
        if (miroir_epoque is not None
                and entete["epoque"] < miroir_epoque):
            if consigner:
                _journal(conteneur_chemin, f"PORTE : refus — RETOUR EN "
                         f"ARRIÈRE (conteneur {entete['epoque']} < miroir "
                         f"{miroir_epoque})")
            raise ErreurCoffre(f"RETOUR EN ARRIÈRE : époque du conteneur "
                               f"({entete['epoque']}) < époque du miroir "
                               f"local ({miroir_epoque}) — un couple "
                               "conteneur+piège restauré est REFUSÉ (spec "
                               "§ 9 ; témoins hors-bande : carte papier, "
                               "journal Git)")
    if epoque_attendue is not None and entete["epoque"] != epoque_attendue:
        raise ErreurCoffre(f"époque du conteneur ({entete['epoque']}) "
                           f"diverge du témoin hors-bande ({epoque_attendue}) "
                           "— roll-back nommé par la carte papier ou le "
                           "journal Git (spec § 9)")

    # 4 — phrase (BÉNIGNE : réessai, jamais de destruction)
    k_user = bytearray(cle_utilisateur(phrase, entete["sel_argon"]))
    try:
        if derive_verif(k_user, piege["v_piege"], entete["sel_hkdf"]) \
                != entete["verif"]:
            if consigner:
                _journal(conteneur_chemin, "PORTE : phrase ERRONÉE (verif "
                         "divergent) — réessai, JAMAIS de destruction")
            raise PhraseErronee(
                "phrase ERRONÉE (verif divergent) — réessayez : une phrase "
                "erronée ne détruit JAMAIS (spec § 5.4 ; borne : un piège "
                "forgé se présente pareil — bénin)")

        # 5 — empreinte + AEAD : la falsification PROUVÉE détruit localement
        if hashlib.sha256(entete["chiffretexte"]).digest() \
                != entete["empreinte"]:
            _destruction_locale(
                conteneur_chemin,
                "empreinte du chiffretexte divergente — falsification ou "
                "corruption PROUVÉE côté machine (phrase vérifiée, piège "
                "intègre)", brouillon_chemin)
            raise ErreurCoffre("empreinte du chiffretexte divergente — "
                               "falsification PROUVÉE côté machine : "
                               "destruction LOCALE effectuée (PV écrit) ; le "
                               "média du piège et les fragments CF2 sont "
                               "INTACTS (spec § 5.5/§ 7)")
        kek = bytearray(derive_kek(k_user, entete["s_serrure"],
                                   piege["s_piege"], entete["sel_hkdf"],
                                   entete["epoque"], entete["h_projet"]))
        try:
            clair = crypto_aead_xchacha20poly1305_ietf_decrypt(
                entete["chiffretexte"], entete["aad"], entete["nonce"],
                bytes(kek))
        except Exception:
            _destruction_locale(
                conteneur_chemin,
                "tag AEAD invalide après piège intègre et phrase vérifiée — "
                "falsification ou corruption PROUVÉE côté machine",
                brouillon_chemin)
            raise ErreurCoffre("tag AEAD invalide — falsification PROUVÉE "
                               "côté machine : destruction LOCALE effectuée "
                               "(PV écrit) ; le média du piège et les "
                               "fragments CF2 sont INTACTS (spec § 5.5/§ 7)")
        finally:
            _cf2._effacer(kek)
        # L'ÉTIQUETTE est VÉRIFIÉE (spec § 5.5/§ 10) : le clair doit hacher
        # vers le H_projet de l'en-tête. C'est ce qui FERME la course de
        # clôture : un KEK volé peut chiffrer un contenu substitué sous une
        # étiquette honnête (en-tête H(A), chiffretexte B) — l'ouverture
        # honnête le DÉMASQUE : falsification PROUVÉE, destruction locale.
        # La clé de clôture ne scelle QUE l'état dont le hash a servi à la
        # dériver, ET le conteneur ne s'ouvre que si son contenu hache vers
        # son étiquette.
        if hashlib.sha256(clair).digest() != entete["h_projet"]:
            _destruction_locale(
                conteneur_chemin,
                "l'état déchiffré ne hache pas vers son étiquette H_projet — "
                "substitution PROUVÉE (course de clôture : un KEK volé ne "
                "scelle pas n'importe quoi, spec § 10)", brouillon_chemin)
            raise ErreurCoffre("état scellé ≠ étiquette H_projet — "
                               "falsification PROUVÉE (course de clôture) : "
                               "destruction LOCALE effectuée (PV écrit) ; le "
                               "média du piège et les fragments CF2 sont "
                               "INTACTS (spec § 5.5/§ 10)")
    finally:
        _cf2._effacer(k_user)

    try:
        base = json.loads(clair.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise ErreurCoffre("base JSON illisible après déchiffrement")
    return base, entete


# ---------------------------------------------------------------------------
# La base (MÊME schéma que CF1/CF2 — la migration ne traduit rien, spec § 12)
# ---------------------------------------------------------------------------

def nouvelle_base(description: str = "") -> dict:
    return {"format": 1, "protocole": PROTOCOLE, "cree": _cf2._date_utc(),
            "modifie": _cf2._date_utc(), "description": description,
            "projets": {}}


def _serialiser(base: dict) -> bytes:
    return json.dumps(base, ensure_ascii=False).encode("utf-8")


def empreinte_etat(base: dict) -> tuple[bytes, str]:
    """(H_projet, checksum 8 hex) de l'état clair — le LIANT de la clé de
    clôture au contenu et la valeur que l'humain recoupe avec sa carte
    (spec § 6.2/§ 9)."""
    h = hashlib.sha256(_serialiser(base)).digest()
    return h, h[:4].hex()


# ---------------------------------------------------------------------------
# Le brouillon de session (spec § 6 — clé de session éphémère)
# ---------------------------------------------------------------------------

def _chiffrer_brouillon(clair: bytes, k_session) -> bytes:
    nonce = secrets.token_bytes(24)
    aad = MAGIC_BROUILLON + FORMAT_VERSION.to_bytes(2, "little")
    chiffretexte = crypto_aead_xchacha20poly1305_ietf_encrypt(
        clair, aad, nonce, bytes(k_session))
    return aad + nonce + chiffretexte


def _dechiffrer_brouillon(blob: bytes, k_session) -> bytes:
    if len(blob) < 20 + 2 + 24:
        raise ErreurCoffre("brouillon tronqué")
    if blob[:20] != MAGIC_BROUILLON:
        raise ErreurCoffre(f"magic brouillon invalide : {blob[:20]!r}")
    if int.from_bytes(blob[20:22], "little") != FORMAT_VERSION:
        raise ErreurCoffre("version brouillon non gérée")
    nonce = blob[22:46]
    try:
        return crypto_aead_xchacha20poly1305_ietf_decrypt(
            blob[46:], blob[:22], nonce, bytes(k_session))
    except Exception:
        raise ErreurCoffre("brouillon ILLISIBLE — clé de session morte "
                           "(panne ou abandon : une panne auto-nettoie, spec "
                           "§ 6) ou brouillon altéré")


class Session:
    """ACTE I ouvert (spec § 6) : ne retient QUE K_session — aucune clé
    maîtresse (K_user, KEK, moitiés) ne survit à l'ouverture, et le conteneur
    canonique n'est JAMAIS réécrit pendant la session."""

    def __init__(self, k_session, conteneur_chemin: str, epoque: int,
                 h_projet_hex: str, empreinte_canonique_hex: str):
        self._k = k_session                    # bytearray — discipline § 8
        self.conteneur_chemin = conteneur_chemin
        self.chemin_brouillon = chemin_brouillon(conteneur_chemin)
        self.epoque = epoque
        self.h_projet = h_projet_hex
        self.empreinte_canonique = empreinte_canonique_hex

    def lire(self) -> dict:
        """Déchiffre le brouillon (K_session) — le clair ne vit que le temps
        de l'appel."""
        try:
            with open(self.chemin_brouillon, "rb") as f:
                blob = f.read()
        except FileNotFoundError:
            raise ErreurCoffre("brouillon ABSENT — session déjà close ou "
                               "abandonnée (spec § 6)")
        return json.loads(_dechiffrer_brouillon(blob, self._k).decode("utf-8"))

    def ecrire(self, base: dict) -> None:
        """Écrit le brouillon (AEAD sous K_session, écriture atomique D119).
        Le canonique n'est PAS touché — il reste scellé jusqu'à la clôture."""
        clair = bytearray(_serialiser(base))
        try:
            _cf2._ecrire_atomique(self.chemin_brouillon,
                                  _chiffrer_brouillon(bytes(clair), self._k))
        finally:
            _cf2._effacer(clair)

    def empreinte_brouillon(self) -> tuple[bytes, str]:
        """(H_final, checksum 8 hex) de l'état courant du brouillon — la
        valeur que la clôture scelle ET affiche (spec § 6.2/§ 10)."""
        return empreinte_etat(self.lire())

    def _nettoyer(self) -> None:
        if os.path.isfile(self.chemin_brouillon):
            os.unlink(self.chemin_brouillon)
        _cf2._effacer(self._k)

    def abandonner(self) -> None:
        """Abandon : brouillon effacé + K_session morte (spec § 6). Un
        brouillon abandonné est un déchet indéchiffrable."""
        self._nettoyer()
        _journal(self.conteneur_chemin, "ABANDON : brouillon effacé, clé de "
                 "session morte")


# ---------------------------------------------------------------------------
# ACTE I — ouverture (spec § 6)
# ---------------------------------------------------------------------------

def ouvrir(conteneur_chemin: str, piege_chemin: str, phrase: bytes,
           epoque_attendue=None, miroir: bool = True) -> Session:
    """Phrase + piège → sentinelle instantanée → brouillon sous clé de
    session éphémère. Les clés maîtresses meurent ici (spec § 6/§ 8) ; le
    média du piège est à DÉBRANCHER (geste humain consigné au journal de
    cérémonie)."""
    try:
        with open(conteneur_chemin, "rb") as f:
            blob = f.read()
    except FileNotFoundError:
        raise ErreurCoffre(f"conteneur ABSENT : {conteneur_chemin} — rien à "
                           "ouvrir (init ?)")
    if os.path.isfile(chemin_brouillon(conteneur_chemin)):
        print("[CF3] un brouillon d'une session morte existait — écrasé "
              "(illisible sans sa clé de session, spec § 6)", file=sys.stderr)
    base, entete = sentinelle_instantanee(
        blob, piege_chemin, phrase, conteneur_chemin,
        brouillon_chemin=chemin_brouillon(conteneur_chemin),
        epoque_attendue=epoque_attendue, miroir=miroir)
    clair = bytearray(_serialiser(base))
    k_session = bytearray(secrets.token_bytes(32))
    try:
        _cf2._ecrire_atomique(chemin_brouillon(conteneur_chemin),
                              _chiffrer_brouillon(bytes(clair), k_session))
    finally:
        _cf2._effacer(clair)
    _journal(conteneur_chemin, f"OUVERTURE : époque {entete['epoque']} — "
             "verdict VERT (les clés maîtresses meurent ici ; média du piège "
             "à débrancher)")
    return Session(k_session, conteneur_chemin, entete["epoque"],
                   entete["h_projet"].hex(),
                   empreinte_conteneur(entete["entete"]))


# ---------------------------------------------------------------------------
# ACTE II — clôture (spec § 6 — l'ordre des écritures est crash-cohérent)
# ---------------------------------------------------------------------------

def fermer(session: Session, phrase: bytes, piege_dir: str) -> dict:
    """Média rebranché + phrase RETAPÉE. Une faute de frappe est BÉNIGNE
    (vérifiée AVANT tout scellement). La clé de clôture est LIÉE AU CONTENU
    (H_final) ; moitiés fraîches ; époque + 1 ; re-lecture à froid AVANT le
    remplacement atomique. Retour {epoque, checksum, empreinte, piege}."""
    conteneur = session.conteneur_chemin
    try:
        with open(conteneur, "rb") as f:
            blob = f.read()
    except FileNotFoundError:
        raise ErreurCoffre(f"conteneur ABSENT : {conteneur} — la session "
                           "référence un coffre disparu (bruler ?)")
    entete = parser_entete(blob)
    epoque_n = entete["epoque"]

    # 1 — piège d'époque + phrase VÉRIFIÉS contre le canonique courant :
    #     échec ici = BÉNIN, rien n'est scellé (jamais de destruction).
    piege_ancien = chemin_piege(piege_dir, epoque_n)
    if not os.path.isfile(piege_ancien):
        raise ErreurCoffre(f"clôture IMPOSSIBLE : le média du piège est "
                           f"ABSENT (piège d'époque {epoque_n} introuvable : "
                           f"{piege_ancien}) — rebranchez-le (spec § 6 : la "
                           "clôture exige la seconde moitié FRAÎCHEMENT "
                           "présentée)")
    piege_n = _lire_piege(piege_ancien)
    if piege_n["projet"] != entete["h_projet"]:
        raise ErreurCoffre("H_projet du piège divergent — piège d'un AUTRE "
                           "coffre (spec § 5.3)")
    k_user = bytearray(cle_utilisateur(phrase, entete["sel_argon"]))
    clair = bytearray()
    s_serrure2 = s_piege2 = v_piege2 = None
    try:
        if derive_verif(k_user, piege_n["v_piege"], entete["sel_hkdf"]) \
                != entete["verif"]:
            raise PhraseErronee(
                "phrase ERRONÉE à la CLOTURE — aucun scellement n'a lieu : "
                "réessayez (jamais de destruction, spec § 5.4/§ 6.1)")
        clair = bytearray(_serialiser(session.lire()))
        h_final = hashlib.sha256(bytes(clair)).digest()
        checksum = h_final[:4].hex()

        # 2-4 — moitiés FRAÎCHES (métamorphose), époque + 1, K_user et
        #       sel_argon INTACTS (la clé utilisateur ne change pas)
        s_serrure2 = bytearray(secrets.token_bytes(TAILLE_MOITIE))
        s_piege2 = bytearray(secrets.token_bytes(TAILLE_MOITIE))
        v_piege2 = bytearray(secrets.token_bytes(TAILLE_V_PIEGE))
        sel_hkdf2 = secrets.token_bytes(TAILLE_SEL_HKDF)
        epoque2 = epoque_n + 1
        staging = conteneur + ".staging"
        piege2_chemin = chemin_piege(piege_dir, epoque2)
        if os.path.isfile(piege2_chemin):
            # orphelin d'une clôture interrompue (spec § 6 : le créneau
            # N+1 est le FUTUR — rien de vivant n'en dépend ; un média par
            # coffre, spec § 4)
            print(f"[CF3] un piège d'époque {epoque2} préexistant a été "
                  "REMPLACÉ (orphelin d'une clôture interrompue — spec § 6)",
                  file=sys.stderr)
        try:
            # 5 — écritures crash-cohérentes : piège d'abord…
            _defaut("avant-piege")
            _cf2._ecrire_atomique(
                piege2_chemin,
                serialiser_piege(epoque2, h_final, s_piege2,
                                 v_piege2).encode("ascii"))
            _defaut("apres-piege")
            # …puis staging (le canonique n'est JAMAIS touché ici)…
            blob2 = construire_conteneur(
                bytes(clair), k_user, s_serrure2, s_piege2, v_piege2,
                entete["sel_argon"], sel_hkdf2, epoque2, h_final)
            _cf2._ecrire_atomique(staging, blob2)
            _defaut("apres-staging")

            # 6 — re-lecture À FROID : uniquement depuis les artefacts
            #     ÉCRITS (la preuve que le scellage est honnête) — VERTE →
            #     remplacement atomique ; ÉCHEC → staging détruit, canonique
            #     et brouillon INTACTS, clôture rejouable.
            base2, _ = sentinelle_instantanee(
                blob2, piege2_chemin, phrase, staging, brouillon_chemin=None,
                miroir=True, consigner=False)
            if base2 != json.loads(bytes(clair).decode("utf-8")):
                raise ErreurCoffre("re-lecture à froid divergente — le "
                                   "staging ne relit pas l'état scellé")
            _defaut("avant-replace")
            os.replace(staging, conteneur)
            _defaut("apres-replace")

            # 7 — miroir + journal + nettoyage (l'ordre tolère la panne :
            #     miroir en retard = contrôle « conteneur >= miroir » VERT)
            _ecrire_miroir(conteneur, epoque2, checksum)
            _journal(conteneur, f"CLÔTURE : époque {epoque2}, checksum "
                     f"{checksum} — moitiés remplacées, piège {epoque2} sur "
                     "le média (l'ancien piège devient relève)")
            session._nettoyer()
            return {"epoque": epoque2, "checksum": checksum,
                    "empreinte": h_final.hex(), "piege": piege2_chemin}
        except ErreurCoffre:
            # clôture interrompue ou re-lecture échouée : le staging est un
            # déchet — canonique et brouillon INTACTS, la clôture est
            # rejouable (spec § 6.6)
            if os.path.isfile(staging):
                _detruire_fichier(staging)
            raise
        finally:
            _cf2._effacer(s_serrure2, s_piege2, v_piege2)
    finally:
        _cf2._effacer(clair)
        _cf2._effacer(k_user)


# ---------------------------------------------------------------------------
# Verdict à froid, étiquette, destruction manuelle (spec § 9/§ 7)
# ---------------------------------------------------------------------------

def verifier(conteneur_chemin: str, piege_chemin: str, phrase: bytes,
             epoque_attendue=None, miroir: bool = True) -> dict:
    """Sentinelle complète + verdict nominal : époque, empreinte, checksum
    (8 hex) pour recoupement humain avec la CARTE (spec § 9). Applique la
    même loi que tout acte (falsification prouvée → destruction locale)."""
    try:
        with open(conteneur_chemin, "rb") as f:
            blob = f.read()
    except FileNotFoundError:
        raise ErreurCoffre(f"conteneur ABSENT : {conteneur_chemin}")
    base, entete = sentinelle_instantanee(
        blob, piege_chemin, phrase, conteneur_chemin,
        brouillon_chemin=chemin_brouillon(conteneur_chemin),
        epoque_attendue=epoque_attendue, miroir=miroir)
    nb_projets = len(base.get("projets", {}))
    verdict = {"epoque": entete["epoque"],
               "empreinte": entete["h_projet"].hex(),
               "checksum": entete["h_projet"][:4].hex(),
               "projets": nb_projets}
    print(f"[CF3] VERDICT : VERT — époque {verdict['epoque']}, checksum "
          f"{verdict['checksum']} (carte papier / journal Git : recoupez), "
          f"{verdict['projets']} projet(s)")
    return verdict


def statut(conteneur_chemin: str) -> dict:
    """Lecture d'ÉTIQUETTE seule (en-tête clair — aucune clé, aucun piège,
    sentinelle NON courue). BORNE dite : ceci n'est pas un verdict (spec § 5
    — le verdict exige piège + phrase)."""
    try:
        with open(conteneur_chemin, "rb") as f:
            blob = f.read()
    except FileNotFoundError:
        raise ErreurCoffre(f"conteneur ABSENT : {conteneur_chemin}")
    entete = parser_entete(blob)
    miroir = None
    if os.path.isfile(chemin_miroir(conteneur_chemin)):
        try:
            miroir = _lire_miroir(conteneur_chemin)
        except ErreurCoffre as exc:
            miroir = f"ILLISIBLE ({exc})"
    info = {"epoque": entete["epoque"], "h_projet": entete["h_projet"].hex(),
            "empreinte_conteneur": empreinte_conteneur(entete["entete"]),
            "miroir_local": miroir, "taille": entete["taille"]}
    print(f"[CF3] conteneur : {conteneur_chemin} ({info['taille']} o)")
    print(f"[CF3] époque : {info['epoque']} — miroir local : {miroir}")
    print(f"[CF3] H_projet : {info['h_projet']}")
    print("[CF3] BORNE : lecture d'étiquette SANS piège ni phrase — la "
          "sentinelle instantanée n'a PAS couru (verdict : verifier)")
    return info


def bruler(conteneur_chemin: str, affirmation: bool) -> int:
    """Destruction MANUELLE explicite (spec § 7) — même routine que la
    falsification prouvée, déclencheur humain."""
    if not affirmation:
        raise ErreurCoffre("bruler exige --oui-je-comprends (destruction "
                           "LOCALE irréversible : conteneur, staging, "
                           "brouillon — jamais le média, jamais les "
                           "fragments)")
    if not os.path.isfile(conteneur_chemin):
        raise ErreurCoffre(f"conteneur ABSENT : {conteneur_chemin}")
    _destruction_locale(conteneur_chemin, "commande explicite bruler "
                        "(--oui-je-comprends)",
                        chemin_brouillon(conteneur_chemin))
    return 0


# ---------------------------------------------------------------------------
# Init (spec § 6 — ordre crash-cohérent : piège, conteneur, miroir)
# ---------------------------------------------------------------------------

def init(phrase: bytes, piege_dir: str, description: str = "",
         conteneur_chemin: str = CONTENEUR_DEFAUT) -> dict:
    """Coffre neuf : époque 1, moitiés fraîches, piège posé sur le média.
    Ordre crash-cohérent : piège d'abord (un crash ne laisse JAMAIS un
    conteneur sans piège), conteneur ensuite, miroir enfin (absent = pas de
    témoin, premier acte : verifier)."""
    if os.path.isfile(conteneur_chemin):
        raise ErreurCoffre(f"conteneur DÉJÀ PRÉSENT : {conteneur_chemin} — "
                           "refus d'écraser un coffre existant (bruler "
                           "d'abord si assumé)")
    if not phrase:
        raise ErreurCoffre("phrase VIDE — refus (spec § 2)")
    base = nouvelle_base(description)
    clair = _serialiser(base)
    h_projet, checksum = empreinte_etat(base)
    sel_argon = secrets.token_bytes(TAILLE_SEL_ARGON)
    sel_hkdf = secrets.token_bytes(TAILLE_SEL_HKDF)
    s_serrure = secrets.token_bytes(TAILLE_MOITIE)
    s_piege = secrets.token_bytes(TAILLE_MOITIE)
    v_piege = secrets.token_bytes(TAILLE_V_PIEGE)
    k_user = bytearray(cle_utilisateur(phrase, sel_argon))
    try:
        piege_chemin = chemin_piege(piege_dir, 1)
        _cf2._ecrire_atomique(piege_chemin,
                              serialiser_piege(1, h_projet, s_piege,
                                               v_piege).encode("ascii"))
        blob = construire_conteneur(clair, k_user, s_serrure, s_piege,
                                    v_piege, sel_argon, sel_hkdf, 1, h_projet)
        _cf2._ecrire_atomique(conteneur_chemin, blob)
        _ecrire_miroir(conteneur_chemin, 1, checksum)
    finally:
        _cf2._effacer(k_user)
    _journal(conteneur_chemin, "INIT : époque 1 — moitiés fraîches, piège "
             "posé sur le média (le coffre est né verrouillé)")
    print(f"[CF3] coffre scellé : {conteneur_chemin} (époque 1)")
    print(f"[CF3] piège posé sur le média : {piege_chemin}")
    print(f"[CF3] checksum de l'état initial : {checksum} — notez-le sur la "
          "carte du sachet (spec § 9)")
    return {"epoque": 1, "checksum": checksum, "piege": piege_chemin,
            "conteneur": conteneur_chemin}


# ---------------------------------------------------------------------------
# Migration CF2 → CF3 (spec § 12 — cérémonie consignée, outillage D127 :
# la preuve terrain est acquise, l'outil naît au mot du maître)
# ---------------------------------------------------------------------------

def _config_cf2_pour_migrer(conteneur_cf2: str, gardes, config_cf2):
    """Résolution NOMMÉE de la config CF2 pour la migration : (1) le
    chemin --config-cf2 s'il est donné (doit exister) ; (2) la config
    PAR DÉFAUT de CF2 si elle vit déjà (le déploiement réel en a une,
    écrite par son propre migrer) ; (3) à défaut, une config synthétisée
    depuis l'en-tête du conteneur (n, t) et la racine des gardes.
    La PORTE D120 y trouve ses champs (heartbeat, exiger_sentinelle) —
    chaque état est nommé, jamais un repli silencieux."""
    if config_cf2:
        if not os.path.isfile(config_cf2):
            raise ErreurCoffre(f"config CF2 ABSENTE : {config_cf2}")
        return _cf2.lire_config(config_cf2)
    if os.path.isfile(_cf2.CHEMIN_CONFIG_DEFAUT):
        config = _cf2.lire_config(_cf2.CHEMIN_CONFIG_DEFAUT)
    else:
        with open(conteneur_cf2, "rb") as f:
            entete = _cf2._parser_entete(f.read())
        racine = gardes if gardes else _cf2.RACINE_GARDES_DEFAUT
        config = _cf2.config_par_defaut(entete["n"], entete["t"], racine,
                                         conteneur_cf2)
    if gardes:
        n = int(config.get("n", 5))
        config["gardes"] = [os.path.join(gardes, f"g{i}")
                            for i in range(1, n + 1)]
    return config


def migrer(conteneur_cf2: str, piege_dir: str, phrase: bytes,
           conteneur_chemin: str = CONTENEUR_DEFAUT, gardes=None,
           config_cf2=None) -> dict:
    """Cérémonie de migration CF2 → CF3 (spec § 12, D127).

    (1) CF2 déverrouillé UNE DERNIÈRE FOIS — porte D120 honorée (la
        PORTE court AVANT toute lecture de fragment, là où le moteur
        existe elle EXIGE la sentinelle vivante) ; la clé maîtresse
        Shamir M ne vit que l'instant de la lecture et MEURT aussitôt
        (CF3 n'en a que faire : K_user vient de la phrase) ;
    (2) la base re-scellée sous CF3, SCHÉMA IDENTIQUE — RIEN À TRADUIRE :
        le JSON clair passe octet pour octet (H_projet CF3 = condensé du
        MÊME clair que CF2 scellait) ; époque 1, moitiés fraîches,
        sel_argon NEUF (K_user est invariable à travers les ÉPOQUES CF3,
        pas à travers les générations) ;
    (3) re-lecture À FROID du staging par la sentinelle COMPLÈTE avant
        le remplacement atomique — une migration qui ne relirait pas son
        scellage ne serait pas une cérémonie ; échec → staging détruit,
        CF2 et médias INTACTS, migration REJOUABLE ;
    (4) le conteneur CF2 reste INTACT : sa destruction est un acte
        EXPLICITE après verdict humain (detruire-cf2) — les fragments
        CF2 et leurs copies hors-ligne restent la RELÈVE HISTORIQUE.

    Retour {epoque, checksum, empreinte, piege, conteneur, conteneur_cf2}.
    """
    if not phrase:
        raise ErreurCoffre("phrase VIDE — refus (spec § 2)")
    if os.path.isfile(conteneur_chemin):
        raise ErreurCoffre(f"conteneur CF3 DÉJÀ PRÉSENT : {conteneur_chemin} "
                           "— refus d'écraser (bruler d'abord si assumé)")
    if not os.path.isfile(conteneur_cf2):
        raise ErreurCoffre(f"conteneur CF2 ABSENT : {conteneur_cf2} — la "
                           "migration part d'un coffre CF2 vivant (spec § 12)")
    if not os.path.isdir(piege_dir):
        raise ErreurCoffre(f"média du piège ABSENT : {piege_dir} — branchez-le "
                           "(spec § 4 : la seconde moitié vit sur un média "
                           "séparé, la machine ne le CRÉE jamais)")
    config = _config_cf2_pour_migrer(conteneur_cf2, gardes, config_cf2)
    _cf2.porte_sentinelle(config)     # D120 — la PORTE avant toute lecture
    base, _entete_cf2, m, _blob_cf2 = _cf2.deverrouiller(conteneur_cf2,
                                                         config["gardes"])
    try:
        clair = bytearray(_serialiser(base))
        h_projet = hashlib.sha256(bytes(clair)).digest()
        checksum = h_projet[:4].hex()
    finally:
        _cf2._effacer(m)
        del m
    sel_argon = secrets.token_bytes(TAILLE_SEL_ARGON)
    sel_hkdf = secrets.token_bytes(TAILLE_SEL_HKDF)
    s_serrure = bytearray(secrets.token_bytes(TAILLE_MOITIE))
    s_piege = bytearray(secrets.token_bytes(TAILLE_MOITIE))
    v_piege = bytearray(secrets.token_bytes(TAILLE_V_PIEGE))
    k_user = bytearray(cle_utilisateur(phrase, sel_argon))
    piege_chemin = chemin_piege(piege_dir, 1)
    staging = conteneur_chemin + ".staging"
    try:
        if os.path.isfile(piege_chemin):
            print(f"[CF3] un piège d'époque 1 préexistant a été REMPLACÉ "
                  "(orphelin d'une migration interrompue — spec § 6/§ 12)",
                  file=sys.stderr)
        _cf2._ecrire_atomique(
            piege_chemin,
            serialiser_piege(1, h_projet, s_piege, v_piege).encode("ascii"))
        blob = construire_conteneur(bytes(clair), k_user, s_serrure, s_piege,
                                    v_piege, sel_argon, sel_hkdf, 1, h_projet)
        _cf2._ecrire_atomique(staging, blob)
        # re-lecture À FROID — uniquement depuis les artefacts ÉCRITS :
        # VERTE → remplacement atomique ; ÉCHEC → staging détruit, CF2 et
        # médias INTACTS, migration rejouable (miroir de la clôture § 6.6)
        base2, _ = sentinelle_instantanee(
            blob, piege_chemin, phrase, conteneur_chemin,
            brouillon_chemin=None, miroir=True, consigner=False)
        if base2 != json.loads(bytes(clair).decode("utf-8")):
            raise ErreurCoffre("re-lecture à froid divergente — le staging "
                               "ne relit pas la base migrée")
        os.replace(staging, conteneur_chemin)
        _ecrire_miroir(conteneur_chemin, 1, checksum)
    except ErreurCoffre:
        if os.path.isfile(staging):
            _detruire_fichier(staging)
        raise
    finally:
        _cf2._effacer(k_user, s_serrure, s_piege, v_piege, clair)
    _journal(conteneur_chemin, f"MIGRATION CF2 → CF3 : époque 1, checksum "
             f"{checksum} — base re-scellée schéma identique (rien à "
             f"traduire) depuis {conteneur_cf2} ; conteneur CF2 laissé "
             "INTACT (destruction explicite après verdict : detruire-cf2, "
             "spec § 12)")
    print(f"[CF3-migration] CF2 déverrouillé une dernière fois (porte D120 "
          f"honorée) : {conteneur_cf2}")
    print(f"[CF3-migration] base re-scellée sous CF3 (schéma identique — "
          f"rien à traduire) : {conteneur_chemin} (époque 1)")
    print(f"[CF3-migration] piège posé sur le média : {piege_chemin}")
    print("[CF3-migration] re-lecture à froid du scellage : VERTE")
    print(f"[CF3-migration] VERDICT : VERT — époque 1, checksum {checksum} "
          f"({len(base.get('projets', {}))} projet(s)) — notez-le sur la "
          "carte du sachet (spec § 9)")
    print(f"[CF3-migration] conteneur CF2 laissé INTACT : {conteneur_cf2} — "
          "destruction EXPLICITE après verdict humain : "
          "coffre_cf3.py detruire-cf2 --conteneur-cf2 <…> "
          "--oui-je-comprends (les fragments CF2 et leurs copies hors-ligne "
          "restent la relève historique, spec § 12)")
    return {"epoque": 1, "checksum": checksum,
            "empreinte": h_projet.hex(), "piege": piege_chemin,
            "conteneur": conteneur_chemin, "conteneur_cf2": conteneur_cf2}


def detruire_cf2(conteneur_cf2: str, conteneur_cf3: str = CONTENEUR_DEFAUT,
                 affirmation: bool = False) -> int:
    """Destruction EXPLICITE du conteneur CF2 après migration (spec § 12.4).

    Le QUATRIÈME acte de la cérémonie — jamais automatique : migrer
    laisse le conteneur CF2 INTACT, c'est l'humain qui décide, après le
    verdict à froid VERT et le recoupement de la carte. Garde
    fail-closed : refus nommé si le conteneur CF3 qui le remplace est
    ABSENT (détruire l'ancien coffre sans le neuf serait une perte
    sèche). Les fragments CF2 et leurs copies hors-ligne ne sont JAMAIS
    touchés : ils restent la RELÈVE HISTORIQUE (spec § 12).
    """
    if not affirmation:
        raise ErreurCoffre("detruire-cf2 exige --oui-je-comprends — la "
                           "destruction du conteneur CF2 est EXPLICITE "
                           "(spec § 12.4 : après le verdict à froid VERT, "
                           "jamais automatique ; les fragments CF2 et leurs "
                           "copies hors-ligne restent la relève historique)")
    if not os.path.isfile(conteneur_cf2):
        raise ErreurCoffre(f"conteneur CF2 ABSENT : {conteneur_cf2}")
    if not os.path.isfile(conteneur_cf3):
        raise ErreurCoffre(f"refus FAIL-CLOSED : le conteneur CF3 qui remplace "
                           f"le coffre est ABSENT ({conteneur_cf3}) — détruire "
                           "l'ancien sans le neuf serait une perte sèche "
                           "(verifiez d'abord : coffre_cf3.py verifier)")
    _detruire_fichier(conteneur_cf2)
    # PV nommé dans le dossier PV du coffre CF3 (le survivant consigne
    # la mort de l'ancien) + ligne au journal CF3 — même loi que les
    # destructions locales spec § 7 : chaque mort laisse SON procès-verbal
    pv_dir = chemin_pv_dir(conteneur_cf3)
    os.makedirs(pv_dir, exist_ok=True)
    horodatage = _cf2._date_utc().replace(":", "").replace("-", "")
    chemin_pv = os.path.join(pv_dir, f"pv-destruction-cf2-{horodatage}.txt")
    _cf2._ecrire_atomique(chemin_pv, "\n".join([
        "PROCÈS-VERBAL — destruction explicite du conteneur CF2 "
        "(migration, spec § 12.4)",
        f"date : {_cf2._date_utc()}",
        f"conteneur CF2 détruit : {conteneur_cf2} (3 passes, tronqué, "
        "renommé, unlink, fsync rép.)",
        f"conteneur CF3 survivant : {conteneur_cf3}",
        "les fragments CF2 et leurs copies hors-ligne sont INTACTS : "
        "relève HISTORIQUE (spec § 12)",
        "le média du piège CF3 est INTACT (la relève vivante)",
    ]).encode("utf-8"))
    _journal(conteneur_cf3, f"DESTRUCTION CF2 : conteneur {conteneur_cf2} "
             "détruit EXPLICITEMENT après migration — fragments CF2 INTACTS "
             "(relève historique, spec § 12)")
    print(f"[CF3-migration] conteneur CF2 DÉTRUIT : {conteneur_cf2}")
    print(f"[CF3-migration] fragments CF2 et copies hors-ligne INTACTS "
          f"(relève historique) ; PV : {chemin_pv}")
    return 0


# ---------------------------------------------------------------------------
# Délai croissant (spec § 5.4)
# ---------------------------------------------------------------------------

def _delai_essai(essai: int) -> float:
    """1, 2, 4 s… plafond 8 s — le plafond borne aussi l'auto-verrouillage
    de compte par soi-même (spec § 5.4)."""
    return min(2.0 ** max(essai - 1, 0), DELAI_MAX)


# ---------------------------------------------------------------------------
# Autotest (spec § 11 — répertoires temporaires, discipline D105)
# ---------------------------------------------------------------------------

def _octets(chemin: str) -> bytes:
    with open(chemin, "rb") as f:
        return f.read()


def _texte(chemin: str) -> str:
    with open(chemin, "r", encoding="ascii") as f:
        return f.read()


def autotest() -> int:
    """Autocontrôles indépendants de la plateforme — le cycle deux actes et
    ses modes de défaillance, prouvés sur un coffre de laboratoire."""
    resultats = []

    def _verifie(temoin: str, condition: bool) -> None:
        resultats.append((temoin, bool(condition)))
        print(f"[CF3-autotest] {temoin} : "
              f"{'PASS' if condition else 'ECHEC'}")

    global _DEFAUT_SIMULE
    with tempfile.TemporaryDirectory(prefix="cf3-autotest-") as bac:
        conteneur = os.path.join(bac, "coffre_cf3.bin")
        media = os.path.join(bac, "media-piege")
        os.makedirs(media)
        phrase = b"phrase-autotest-cf3"

        # --- le cycle complet
        init(phrase, media, "autotest", conteneur)
        piege1 = chemin_piege(media, 1)
        _verifie("init-piege-sur-media", os.path.isfile(piege1))
        entete_epoque1 = parser_entete(_octets(conteneur))
        md5_avant_session = hashlib.md5(_octets(conteneur)).hexdigest()
        session = ouvrir(conteneur, piege1, phrase)
        base = session.lire()
        base["projets"]["projet-x"] = {"entrees": {"sceau": "valeur-1"}}
        session.ecrire(base)
        # pendant la session, le canonique n'est JAMAIS réécrit…
        _verifie("canonique-jamais-ecrit-en-session",
                 hashlib.md5(_octets(conteneur)).hexdigest()
                 == md5_avant_session)
        res = fermer(session, phrase, media)
        _verifie("cloture-epoque-2", res["epoque"] == 2)
        _verifie("cloture-checksum-temoin-independant",
                 res["checksum"] == hashlib.sha256(
                     _serialiser(base)).digest()[:4].hex())

        # ré-ouverture : contenu exact + métamorphose + K_user invariant
        piege2 = chemin_piege(media, 2)
        entete_epoque2 = parser_entete(_octets(conteneur))
        _verifie("moitie-serrure-remplacee",
                 entete_epoque1["s_serrure"] != entete_epoque2["s_serrure"])
        _verifie("sel-argon-invariant-cle-utilisateur",
                 entete_epoque1["sel_argon"] == entete_epoque2["sel_argon"])
        session2 = ouvrir(conteneur, piege2, phrase)
        _verifie("round-trip-contenu-exact",
                 session2.lire()["projets"]["projet-x"]["entrees"]["sceau"]
                 == "valeur-1")
        _verifie("piege-ancien-releve-present", os.path.isfile(piege1))

        # --- modes de défaillance
        octets_avant = _octets(conteneur)
        try:
            ouvrir(conteneur, piege2, b"mauvaise-phrase")
            _verifie("phrase-erronee-refusee", False)
        except PhraseErronee:
            _verifie("phrase-erronee-refusee", True)
        _verifie("phrase-erronee-benigne",
                 _octets(conteneur) == octets_avant
                 and not os.path.isdir(chemin_pv_dir(conteneur)))

        try:
            ouvrir(conteneur, chemin_piege(media, 99), phrase)
            _verifie("piege-absent-impossible", False)
        except ErreurCoffre as exc:
            _verifie("piege-absent-impossible", "ABSENTE" in str(exc))

        try:
            ouvrir(conteneur, piege1, phrase)   # piège d'époque 1 vs conteneur 2
            _verifie("piege-perime-refuse", False)
        except ErreurCoffre as exc:
            _verifie("piege-perime-refuse", "PÉRIMÉ" in str(exc))

        piege2_texte = _texte(piege2)
        texte_corrompu = piege2_texte.replace("piege: ", "piege: 0", 1)
        with open(piege2, "w", encoding="ascii") as f:
            f.write(texte_corrompu)
        try:
            ouvrir(conteneur, piege2, phrase)
            _verifie("tag-piege-invalide-sans-destruction", False)
        except ErreurCoffre as exc:
            _verifie("tag-piege-invalide-sans-destruction",
                     "refus SANS destruction" in str(exc)
                     and _octets(conteneur) == octets_avant)
        with open(piege2, "w", encoding="ascii") as f:
            f.write(piege2_texte)               # restauration du média

        blob_altere = bytearray(_octets(conteneur))
        blob_altere[-1] ^= 0x01                  # un octet du chiffretexte
        with open(conteneur, "wb") as f:
            f.write(bytes(blob_altere))
        media_octets = _octets(piege2)
        try:
            ouvrir(conteneur, piege2, phrase)
            _verifie("falsification-prouvee-detruit-localement", False)
        except ErreurCoffre as exc:
            _verifie("falsification-prouvee-detruit-localement",
                     "destruction LOCALE" in str(exc)
                     and not os.path.isfile(conteneur))
        _verifie("media-du-piege-intact",
                 _octets(piege2) == media_octets)
        _verifie("pv-ecrit", len(os.listdir(chemin_pv_dir(conteneur))) == 1)

        # --- crash-cohérence de la clôture (injection — spec § 6)
        init(phrase, media, "crash", conteneur)   # coffre neuf après destr.
        for point in ("avant-piege", "apres-piege", "apres-staging",
                      "avant-replace"):
            _DEFAUT_SIMULE = point
            s = ouvrir(conteneur, chemin_piege(media, 1), phrase)
            try:
                fermer(s, phrase, media)
                _verifie(f"panne-{point}-refusee", False)
            except ErreurCoffre as exc:
                _verifie(f"panne-{point}-refusee",
                         "DÉFAUT SIMULÉ" in str(exc))
            _DEFAUT_SIMULE = None
            _verifie(f"panne-{point}-canonique-intact",
                     parser_entete(_octets(conteneur))["epoque"] == 1)
            ouvrir(conteneur, chemin_piege(media, 1), phrase).abandonner()
        _DEFAUT_SIMULE = "apres-replace"
        s = ouvrir(conteneur, chemin_piege(media, 1), phrase)
        try:
            fermer(s, phrase, media)
        except ErreurCoffre:
            pass
        _DEFAUT_SIMULE = None
        _verifie("panne-apres-replace-canonical-a-n+1",
                 parser_entete(_octets(conteneur))["epoque"] == 2)
        _verifie("panne-apres-replace-reouverture-verte",
                 ouvrir(conteneur, chemin_piege(media, 2),
                        phrase).lire()["description"] == "crash")

        # --- auto-nettoyage par panne : le brouillon sans K_session
        s = ouvrir(conteneur, chemin_piege(media, 2), phrase)
        blob_brouillon = _octets(chemin_brouillon(conteneur))
        mauvaise_cle = bytearray(32)
        try:
            _dechiffrer_brouillon(blob_brouillon, mauvaise_cle)
            _verifie("brouillon-indechiffrable-sans-cle", False)
        except ErreurCoffre:
            _verifie("brouillon-indechiffrable-sans-cle", True)
        s.abandonner()
        _verifie("abandon-efface-brouillon",
                 not os.path.isfile(chemin_brouillon(conteneur)))

    echecs = [t for t, ok in resultats if not ok]
    print(f"[CF3-autotest] {len(resultats) - len(echecs)} PASS / "
          f"{len(echecs)} ÉCHEC")
    return 1 if echecs else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _demander_phrase_confirme(action_nom: str = "init") -> bytes:
    for _ in (1, 2, 3):
        a = getpass.getpass("Phrase du coffre : ").encode("utf-8")
        b = getpass.getpass("Confirmez la phrase : ").encode("utf-8")
        if a == b and a:
            return a
        print("[CF3] les deux phrases divergent (ou vide) — recomposez",
              file=sys.stderr)
    raise ErreurCoffre(f"trois essais de phrase — {action_nom} abandonné")


def _choisir_piege(args, conteneur: str) -> str:
    if getattr(args, "piege", None):
        return args.piege
    piege_dir = getattr(args, "piege_dir", None) or PIEGE_DIR_DEFAUT
    entete = parser_entete(_octets(conteneur))
    chemin = trouver_piege(piege_dir, entete["epoque"])
    if chemin is None:
        raise ErreurCoffre(f"piège d'époque {entete['epoque']} introuvable "
                           f"dans {piege_dir} — branchez le média du piège "
                           "(spec § 5.1)")
    return chemin


def _essais_phrase(action, phrase_stdin: bool = False) -> int:
    """Boucle CLI (spec § 5.4) : PhraseErronee → réessai avec délai
    croissant ; tout autre échec nommé est fatal (fail-closed). Via stdin :
    UN essai (stdin ne retape pas — automatisation de laboratoire)."""
    if phrase_stdin:
        return action(sys.stdin.buffer.read().strip(b"\r\n"))
    for essai in (1, 2, 3):
        try:
            phrase = getpass.getpass("Phrase du coffre : ").encode("utf-8")
            return action(phrase)
        except PhraseErronee as exc:
            if essai == 3:
                print(f"ECHEC : {exc} — trois essais, arrêt", file=sys.stderr)
                return 1
            delai = _delai_essai(essai)
            print(f"[CF3] {exc}", file=sys.stderr)
            print(f"[CF3] nouvel essai dans {delai:.0f} s "
                  f"(essai {essai}/3)", file=sys.stderr)
            time.sleep(delai)
    return 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="coffre_cf3.py",
        description="CF3 : la serrure à triple scellement et le cycle en "
                    "deux actes (D121, spec v06/I/CF3/README.md)")
    sous = parser.add_subparsers(dest="commande", required=True)

    p = sous.add_parser("init", help="coffre neuf (époque 1)")
    p.add_argument("--piege-dir", default=PIEGE_DIR_DEFAUT,
                   help="média du piège (LABO : .keys/pieges-cf3 — terrain : "
                        "chemin de la clef USB du sachet)")
    p.add_argument("--description", default="")
    p.add_argument("--phrase-stdin", action="store_true")
    p.add_argument("--conteneur", default=CONTENEUR_DEFAUT)

    p = sous.add_parser("ouvrir", help="acte I : sentinelle + verdict (la "
                                       "session CLI mourrait avec son "
                                       "processus — le cycle complet vit en "
                                       "API/GUI)")
    p.add_argument("--piege-dir", default=None)
    p.add_argument("--piege", default=None)
    p.add_argument("--phrase-stdin", action="store_true")
    p.add_argument("--conteneur", default=CONTENEUR_DEFAUT)
    p.add_argument("--epoque-attendue", type=int, default=None,
                   help="témoin hors-bande (carte papier / journal Git)")

    p = sous.add_parser("verifier", help="verdict à froid (sentinelle "
                                         "complète + checksum pour la carte)")
    p.add_argument("--piege-dir", default=None)
    p.add_argument("--piege", default=None)
    p.add_argument("--phrase-stdin", action="store_true")
    p.add_argument("--conteneur", default=CONTENEUR_DEFAUT)
    p.add_argument("--epoque-attendue", type=int, default=None)

    p = sous.add_parser("statut", help="étiquette seule (aucune clé, aucune "
                                       "sentinelle — la borne est dite)")
    p.add_argument("--conteneur", default=CONTENEUR_DEFAUT)

    p = sous.add_parser("bruler", help="destruction locale MANUELLE "
                                       "(irréversible)")
    p.add_argument("--oui-je-comprends", action="store_true")
    p.add_argument("--conteneur", default=CONTENEUR_DEFAUT)

    p = sous.add_parser("migrer", help="CF2 -> CF3 : cérémonie de "
                                       "migration (spec § 12)")
    p.add_argument("--conteneur-cf2", default=_cf2.CHEMIN_CONTENEUR_DEFAUT,
                   help="conteneur CF2 vivant (défaut : .keys/coffre_cf2.bin)")
    p.add_argument("--gardes", default=None,
                   help="racine des gardes CF2 (g1…gN — défaut : config CF2 "
                        "ou .keys/gardes-cf2)")
    p.add_argument("--config-cf2", default=None,
                   help="config CF2 explicite (défaut : .keys/config_cf2.json "
                        "si elle vit)")
    p.add_argument("--piege-dir", default=PIEGE_DIR_DEFAUT,
                   help="média du piège (LABO : .keys/pieges-cf3 — terrain : "
                        "chemin de la clef USB du sachet, REQUIS)")
    p.add_argument("--conteneur", default=CONTENEUR_DEFAUT)
    p.add_argument("--phrase-stdin", action="store_true")

    p = sous.add_parser("detruire-cf2", help="destruction EXPLICITE du "
                                             "conteneur CF2 après migration "
                                             "(spec § 12.4 — fragments "
                                             "INTACTS)")
    p.add_argument("--conteneur-cf2", default=_cf2.CHEMIN_CONTENEUR_DEFAUT)
    p.add_argument("--conteneur", default=CONTENEUR_DEFAUT,
                   help="le conteneur CF3 qui le remplace (garde fail-closed)")
    p.add_argument("--oui-je-comprends", action="store_true")

    sous.add_parser("autotest", help="autocontrôles (temporaire, D105)")

    args = parser.parse_args(argv)

    try:
        if args.commande == "init":
            phrase = (sys.stdin.buffer.read().strip(b"\r\n")
                      if args.phrase_stdin else _demander_phrase_confirme())
            init(phrase, args.piege_dir, args.description, args.conteneur)
            return 0
        if args.commande == "ouvrir":
            piege = _choisir_piege(args, args.conteneur)

            def action(phrase):
                _, entete = sentinelle_instantanee(
                    _octets(args.conteneur), piege, phrase, args.conteneur,
                    brouillon_chemin=chemin_brouillon(args.conteneur),
                    epoque_attendue=args.epoque_attendue)
                print(f"[CF3] ACTE I : VERT — époque {entete['epoque']} — "
                      "média du piège à DÉBRANCHER (spec § 6 : les clés "
                      "maîtresses meurent ici)")
                return 0
            return _essais_phrase(action, args.phrase_stdin)
        if args.commande == "verifier":
            piege = _choisir_piege(args, args.conteneur)

            def action(phrase):
                verifier(args.conteneur, piege, phrase,
                         epoque_attendue=args.epoque_attendue)
                return 0
            return _essais_phrase(action, args.phrase_stdin)
        if args.commande == "statut":
            statut(args.conteneur)
            return 0
        if args.commande == "bruler":
            return bruler(args.conteneur, args.oui_je_comprends)
        if args.commande == "migrer":
            phrase = (sys.stdin.buffer.read().strip(b"\r\n")
                      if args.phrase_stdin
                      else _demander_phrase_confirme("migration"))
            migrer(args.conteneur_cf2, args.piege_dir, phrase,
                   conteneur_chemin=args.conteneur, gardes=args.gardes,
                   config_cf2=args.config_cf2)
            return 0
        if args.commande == "detruire-cf2":
            return detruire_cf2(args.conteneur_cf2, args.conteneur,
                                args.oui_je_comprends)
        if args.commande == "autotest":
            return autotest()
    except ErreurCoffre as exc:
        print(f"ECHEC : {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ECHEC : {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
