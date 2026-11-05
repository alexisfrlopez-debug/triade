#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""export_continuite.py — L'EXPORT DE CONTINUITÉ MULTI-PROFILS (chantier M7-(d)).

Le modèle : m1/export_continuite.py (D16, FORMAT_CARTE § 8) — le premier
conteneur de l'ère M1 portait UN profil. Le présent port le projet TOUT
ENTIER : l'état scellé COURANT de CHACUN des TROIS profils déclarés
(spécification § 10). Régénéré au geste de fermeture de l'ère M8 (le
modèle Entrée 156 : chaque fermeture d'ère refait l'export à la pointe) —

  x86-64-win11-pe      le scellé de la lignée : m8/proxy.exe 0.9.0 + m8/carte
                       (la carte génération 8 indexes les 55 blocs de la pile
                       win M0-M8 — le domaine sys compris, jalon franchi
                       le 05/11, D165) ; les couches I de toute la pile
                       (m0/I .. m5/I + m8/I)
  x86-64-linux-elf64   unix/sonde 0.7.0-dev.1 + unix/corpus 0.7.0 + leurs
                       cartes ; la couche I CANONIQUE (unix/I — chargée par
                       les instances unix ET riscv, zéro copie D149)
  riscv64-linux-elf64  riscv/sonde 0.8.0-dev.1 + riscv/corpus 0.8.0-rc.1 +
                       leurs cartes ; les miroirs sr-01..04 (riscv/I)

Le nom du conteneur porte LA POINTE des balises (max des versions par
profil — 0.9.0 à l'ère M8).

Conteneur « TRIADE-EXP1 » (le MÊME format que M1 — seul le champ profils
s'étend) : en-tête clair + AEAD XChaCha20-Poly1305 (AAD = en-tête) +
signature Ed25519 (la lignée de clés du projet, D27 — vérifiable avec la
clé publique commitee). L'oracle demeure EXCLU (D1 : régénéré depuis I à
l'arrivée, jamais importé) ; la notation et la toolchain se restaurent par
l'infrastructure D11 (dépôt git + bundle Drive).

L'IMPORT EST AUTO-PORTANT : le manifeste (chiffré) porte TOUT ce que les
cinq étapes exigent — la table de géométrie PAR ARTEFACT (id, offset
fichier, taille, empreinte de chaque bloc), les paramètres PUBLICS de
dérivation de chaque carte (sel Argon2id, contexte HKDF, génération —
publics par conception, la phrase maîtresse reste le seul secret), les
noms de fichiers de chaque carte. Seuls la phrase maîtresse (coffre) et
la clé publique du projet (committée au dépôt — un canal externe au
conteneur) viennent de l'extérieur.

Les CINQ ÉTAPES (FORMAT_CARTE § 8.2, « § 6 du manuel » du plan M7-(d)) :
  (1) déchiffrer   un échec est terminal, rien n'est interprété ;
  (2) signature    le conteneur, puis chacune des cinq cartes transportées ;
  (3) verrou croisé les empreintes de B recalculées aux offsets du
                    manifeste == manifeste == frag-bld de la carte ;
  (4) oracle       régénéré depuis I à l'arrivée (jamais importé) — la
                    preuve d'exécution au labo rejoue les RITUELS sur les
                    octets TRANSPORTÉS (le conteneur déchiffré en mémoire,
                    jamais le disque) ;
  (5) reprise      l'état scellé cohérent (versions par profil, racines,
                    cristallisation) — la reprise normale est possible.

Usage (depuis riscv/) :
  python3 export_continuite.py                  générer + import à sec + preuve
  python3 export_continuite.py --verifier F     procédure d'import à sec sur F
  python3 export_continuite.py --pousser-drive F  copie de coffre au racine Drive
"""

from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
EXPORT_DIR = os.path.join(ICI, "export")
MAGIC = b"TRIADE-EXP1"
FORMAT_VERSION = 1
PROTOCOLE = "0.6.1"
JALON = "M8"

PROFILS = ["x86-64-win11-pe", "x86-64-linux-elf64", "riscv64-linux-elf64"]

# --- La phrase maîtresse : la lignée courante (carte du jalon, D27) ------------

sys.path.insert(0, ICI)
import carte_corpus as cc                # noqa: E402  (les secrets, la source)

from argon2.low_level import Type, hash_secret_raw                     # noqa: E402
from cryptography.hazmat.primitives import hashes                      # noqa: E402
from cryptography.hazmat.primitives.asymmetric.ed25519 import (        # noqa: E402
    Ed25519PrivateKey, Ed25519PublicKey)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF               # noqa: E402
from nacl.bindings import (                                            # noqa: E402
    crypto_aead_xchacha20poly1305_ietf_decrypt,
    crypto_aead_xchacha20poly1305_ietf_encrypt)

# --- Les layouts des DEUX ISA, chargés par chemins ABSOLUS --------------------
# La leçon du geste : les lignées unix/ et riscv/ portent des modules
# HOMONYMES (layout.py, carte_corpus.py…) — sys.path les écraserait. Chaque
# module est chargé sous SON nom, une seule fois.


def _charger_module(nom: str, chemin: str):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


L_RISCV = _charger_module("layout_riscv_export", os.path.join(ICI, "layout.py"))
L_UNIX = _charger_module("layout_unix_export", os.path.join(RACINE, "unix", "layout.py"))

# --- Les pièces par profil -----------------------------------------------------

# (répertoire, en-tête, signature, clé publique, sel Argon2id, sel HKDF, génération)
CARTES = [
    ("m8/carte", "header.txt", "carte.sig", "cle-publique.ed25519",
     hashlib.sha256(b"TRIADE-M8-carte-argon2id-v1").digest(),
     b"TRIADE-carte-M8", 8),
    ("unix/carte", "entete.txt", "signature.bin", "cle-publique.txt",
     hashlib.sha256(b"TRIADE-M6-jalon-unix-carte-argon2id-v1").digest(),
     b"TRIADE-carte-M6-unix", 1),
    ("unix/carte-corpus", "entete.txt", "signature.bin", "cle-publique.txt",
     hashlib.sha256(b"TRIADE-M6-corpus-carte-argon2id-v1").digest(),
     b"TRIADE-carte-M6-corpus", 1),
    ("riscv/carte", "entete.txt", "signature.bin", "cle-publique.txt",
     hashlib.sha256(b"TRIADE-M7-jalon-riscv-carte-argon2id-v1").digest(),
     b"TRIADE-carte-M7-riscv", 1),
    ("riscv/carte-corpus", "entete.txt", "signature.bin", "cle-publique.txt",
     hashlib.sha256(b"TRIADE-M7-corpus-riscv-carte-argon2id-v1").digest(),
     b"TRIADE-carte-M7-corpus-riscv", 1),
]

# (chemin artefact, carte, profil, table de blocs [(id, rva, slot)] ou None)
ARTEFACTS = [
    # le scellé win COURANT : m8/proxy.exe 0.9.0 (le corps 0.6.0 y vit
    # R7-octet-identique ; la table de blocs win reste None — l'offset
    # fichier ≠ RVA au PE, le verrou croisé porte l'ARTEFACT ENTIER)
    ("m8/proxy.exe", "m8/carte", "x86-64-win11-pe", None),
    ("unix/sonde", "unix/carte", "x86-64-linux-elf64",
     [(b[0], b[3], b[4]) for b in L_UNIX.BLOCS_SU]),
    ("unix/corpus", "unix/carte-corpus", "x86-64-linux-elf64",
     [(b[0], b[3], b[4]) for b in L_UNIX.BLOCS_CORPUS]),
    ("riscv/sonde", "riscv/carte", "riscv64-linux-elf64",
     [(b[0], b[3], b[4]) for b in L_RISCV.BLOCS_SR]),
    ("riscv/corpus", "riscv/carte-corpus", "riscv64-linux-elf64",
     [(b[0], b[3], b[4]) for b in L_RISCV.BLOCS_CORPUS]),
]

_ARBRES_I = ["m0", "m1", "m2", "m3", "m4", "m5", "m8", "unix", "riscv"]
FICHIERS_I = sorted(
    os.path.join(RACINE, a, "I", f)
    for a in _ARBRES_I
    for f in os.listdir(os.path.join(RACINE, a, "I")) if f.endswith(".md")
)

RITUEL_CORPUS = (b"TRIADE M1 : minilibc 21/21 OK\n"
                 b"corpus : autotest 21 vecteurs\n")
_MOTIF_BASE = re.compile(rb"^sonde : base 0x[0-9a-f]{12,16}$")
RITUEL_SONDE = (b"sonde : write(-1) : %s 0xfffffffffffffff7 verdict 0x0000000000000001\n"
                b"sonde : write(0x1) : %s 0xfffffffffffffff2 verdict 0x0000000000000006\n"
                b"sonde : VERDICT_FATAL (arret propre)\n")

# La clé du conteneur : Argon2id (mêmes planchers que la carte au repos) sur
# un sel DÉDIÉ à l'export (jamais celui d'une carte), puis HKDF à contexte
# propre — un conteneur falsifié ne donne jamais une clé de carte, et
# réciproquement.
ARGON2_SALT_EXPORT = hashlib.sha256(b"TRIADE-M7-export-continuite-argon2id-v1").digest()


class ErreurExport(RuntimeError):
    """Tout échec de génération, déchiffrement ou vérification — fail-closed."""


# --- Clés -----------------------------------------------------------------------

def cle_export_depuis_phrase(phrase: bytes) -> bytes:
    maitre = hash_secret_raw(secret=phrase, salt=ARGON2_SALT_EXPORT,
                             time_cost=3, memory_cost=65536, parallelism=1,
                             hash_len=32, type=Type.ID)
    return HKDF(algorithm=hashes.SHA256(), length=32,
                salt=b"TRIADE-export-continuite",
                info=b"export=m7-multiprofils;projet=TRIADE").derive(maitre)


def cle_carte_portee(phrase: bytes, sel_argon2: bytes, sel_hkdf: bytes,
                     generation: int, nom_fragment: str) -> bytes:
    """La dérivation d'une carte, RECONSTRUITE depuis les paramètres publics
    portés au manifeste (le miroir exact des modules du dépôt — prouvé
    équivalent au geste d'export)."""
    maitre = hash_secret_raw(secret=phrase, salt=sel_argon2,
                             time_cost=3, memory_cost=65536, parallelism=1,
                             hash_len=32, type=Type.ID)
    return HKDF(algorithm=hashes.SHA256(), length=32, salt=sel_hkdf,
                info=f"frag={nom_fragment};gen={generation}".encode("ascii")
                ).derive(maitre)


def dechiffrer_fragment_portee(phrase: bytes, sel_argon2: bytes, sel_hkdf: bytes,
                               generation: int, nom_fragment: str, blob: bytes) -> bytes:
    if len(blob) < 24 + 16:
        raise ErreurExport(f"{nom_fragment} : blob trop court")
    from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_decrypt
    nonce, ct = blob[:24], blob[24:]
    try:
        return crypto_aead_xchacha20poly1305_ietf_decrypt(
            ct, nom_fragment.encode("ascii"), nonce,
            cle_carte_portee(phrase, sel_argon2, sel_hkdf, generation, nom_fragment))
    except Exception as exc:
        raise ErreurExport(f"{nom_fragment} : déchiffrement impossible ({exc})") from exc


# --- Le conteneur TRIADE-EXP1 (octet pour octet le format M1) -------------------


def _champ(octets: bytes) -> bytes:
    return len(octets).to_bytes(2, "little") + octets


def _lire_champ(blob: bytes, offset: int) -> tuple[bytes, int]:
    n = int.from_bytes(blob[offset:offset + 2], "little")
    return blob[offset + 2:offset + 2 + n], offset + 2 + n


def construire_conteneur(plaintext: bytes, entete_clair: dict, cle: bytes,
                         prive: Ed25519PrivateKey) -> bytes:
    entete = (MAGIC + FORMAT_VERSION.to_bytes(2, "little")
              + _champ(entete_clair["hachage"].encode())
              + _champ(entete_clair["signature"].encode())
              + _champ(entete_clair["chiffrement"].encode())
              + _champ(entete_clair["profils"].encode())
              + _champ(entete_clair["date"].encode()) + entete_clair["racine"])
    nonce = secrets.token_bytes(24)
    ct = crypto_aead_xchacha20poly1305_ietf_encrypt(plaintext, entete + nonce, nonce, cle)
    empreinte_ct = hashlib.sha256(ct).digest()
    signature = prive.sign(entete + nonce + empreinte_ct + ct)
    return entete + nonce + empreinte_ct + signature + ct


def lire_conteneur(blob: bytes):
    if not blob.startswith(MAGIC):
        raise ErreurExport("magic absent — pas un conteneur TRIADE-EXP1")
    offset = len(MAGIC) + 2
    entete = {"format": int.from_bytes(blob[len(MAGIC):len(MAGIC) + 2], "little")}
    for clef in ("hachage", "signature", "chiffrement", "profils", "date"):
        valeur, offset = _lire_champ(blob, offset)
        entete[clef] = valeur.decode("ascii")
    racine, offset = blob[offset:offset + 32], offset + 32
    entete["racine"] = racine
    fin_entete = offset
    nonce = blob[fin_entete:fin_entete + 24]
    empreinte_ct = blob[fin_entete + 24:fin_entete + 56]
    signature = blob[fin_entete + 56:fin_entete + 120]
    ct = blob[fin_entete + 120:]
    if hashlib.sha256(ct).digest() != empreinte_ct:
        raise ErreurExport("empreinte du chiffretexte divergente — conteneur altéré")
    return entete, nonce, empreinte_ct, signature, ct, blob[:fin_entete]


# --- Le verrou croisé : les empreintes des blocs aux offsets du manifeste -------


def table_blocs(artefact: bytes, table) -> list[dict]:
    """Recalcule chaque empreinte de bloc aux offsets du plan — la géométrie
    du corpus (offset fichier == rva, les segments alignés sur la page) est
    PROUVÉE par le recoupement au frag-bld, jamais crue."""
    sortie = []
    for bid, rva, slot in table:
        extrait = artefact[rva:rva + slot]
        if len(extrait) != slot:
            raise ErreurExport(f"bloc {bid} : {slot} o attendus à {rva:#x}, "
                               f"{len(extrait)} lus — artefact tronqué")
        sortie.append({"id": bid, "offset": rva, "taille": slot,
                       "empreinte": hashlib.sha256(extrait).hexdigest()})
    return sortie


def _lire_frag_bld(clair: str) -> tuple[dict, dict]:
    empreintes, builds = {}, {}
    for ligne in clair.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[champs["id"]] = champs["empreinte"].removeprefix("sha256:")
        elif ligne.startswith("[build]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            builds[champs["artefact"]] = champs
    return empreintes, builds


# --- Les rituels (la preuve d'exécution AVANT l'export — l'état vivant) --------


def _chemin_qemu() -> str:
    bc = _charger_module("build_corpus_export_qemu",
                         os.path.join(ICI, "build_corpus.py"))
    return bc.chemin_qemu()


def _executer(chemin: str, extra: list[str] | None = None):
    cmd = list(extra or []) + [chemin]
    r = subprocess.run(cmd, capture_output=True, timeout=60)
    return r.stdout, r.stderr, r.returncode


def jouer_rituel(nom: str, img: bytes, qemu: str | None) -> tuple[bool, str]:
    """Exécute un artefact TRANSPORTÉ (octets en mémoire) — natif ou sous
    qemu (réserve instrumentale D149 : TCG, noyau et syscalls réels)."""
    dossier = tempfile.mkdtemp(prefix="exp-rituel-")
    try:
        chemin = os.path.join(dossier, os.path.basename(nom))
        with open(chemin, "wb") as f:
            f.write(img)
        os.chmod(chemin, 0o755)
        if qemu:
            sortie, err, code = _executer(chemin, [qemu])
        else:
            sortie, err, code = _executer(chemin)
        if nom.endswith("corpus"):
            ok = (code == 0 and not err and sortie == RITUEL_CORPUS)
            return ok, (f"code={code}, {len(sortie)} o — les DEUX lignes octet "
                        "pour octet" if ok else
                        f"code={code}, sortie={sortie[:80]!r}, err={err[:60]!r}")
        # la sonde : la ligne de base porte la base RÉELLE du run (ASLR natif
        # ou base constante qemu) — motif, jamais littéral ; la graphie du
        # registre diffère par ISA (rax SysV x86-64, a0 psABI RV64)
        parties = sortie.split(b"\n", 1)
        premiere = parties[0]
        reste = parties[1] if len(parties) == 2 else b""
        ok = False
        for reg in (b"rax", b"a0"):
            if (code == 6 and not err and _MOTIF_BASE.match(premiere)
                    and reste == RITUEL_SONDE % (reg, reg)):
                ok = True
                break
        return ok, (f"code={code} (VERDICT_FATAL propre)" if ok
                    else f"code={code}, sortie={sortie[:120]!r}")
    finally:
        shutil.rmtree(dossier, ignore_errors=True)


# --- La génération --------------------------------------------------------------


def generer() -> tuple[str, list[str]]:
    lignes = ["=== Export de continuité MULTI-PROFILS (D16 ; M7-(d), régénéré "
              "à la fermeture de l'ère M8 — le modèle Entrée 156) — génération ==="]
    phrase, graine = cc.charger_secrets(interactif=False)
    prive, pub = cc.paire_cles(graine)

    # (0) le verrou croisé AVANT l'export : chaque carte déchiffrée PAR SON
    #     MODULE (la source du dépôt), chaque artefact relu, chaque empreinte
    #     de bloc recalculée aux offsets du plan — la table PORTÉE est PROUVÉE
    cartes_manifeste, artefacts_manifeste = [], []
    nb_empreintes = 0
    modules_cartes = {
        "m8/carte": _charger_module("carte_m8_export", os.path.join(RACINE, "m8", "carte_m8.py")),
        "unix/carte": _charger_module("carte_sonde_unix_export", os.path.join(RACINE, "unix", "carte_sonde.py")),
        "unix/carte-corpus": _charger_module("carte_corpus_unix_export", os.path.join(RACINE, "unix", "carte_corpus.py")),
        "riscv/carte": _charger_module("carte_sonde_riscv_export", os.path.join(ICI, "carte_sonde.py")),
        "riscv/carte-corpus": cc,
    }
    frag_bld_par_carte = {}
    for repertoire, f_entete, f_sig, f_pub, sel_argon2, sel_hkdf, gen in CARTES:
        mod = modules_cartes[repertoire]
        entete, frags, sig, pub_carte = mod.lire_carte()
        mod.verifier_signature(pub_carte, entete, frags, sig)
        if pub_carte != pub:
            raise ErreurExport(f"{repertoire} : clé publique divergente de la lignée D27")
        maitre = mod.cle_maitresse(phrase)
        clair = mod.dechiffrer_fragment(maitre, "frag-bld", frags["frag-bld"])
        # la preuve d'équivalence : la dérivation PORTÉE == la dérivation du module
        if dechiffrer_fragment_portee(phrase, sel_argon2, sel_hkdf, gen,
                                      "frag-bld", frags["frag-bld"]) != clair:
            raise ErreurExport(f"{repertoire} : les paramètres de dérivation portés "
                               "≠ le module du dépôt — le manifeste serait faux")
        frag_bld_par_carte[repertoire] = clair.decode("utf-8")
        cartes_manifeste.append({
            "chemin": repertoire, "entete": f_entete, "signature": f_sig,
            "cle_publique": f_pub,
            "sel_argon2id": sel_argon2.hex(), "sel_hkdf": sel_hkdf.decode("ascii"),
            "generation": gen,
            "racine": "sha256:" + hashlib.sha256(
                b"".join(frags[n] for n in cc.FRAGMENTS)).hexdigest(),
        })

    versions = {}
    for chemin_artefact, carte, profil, table in ARTEFACTS:
        with open(os.path.join(RACINE, chemin_artefact), "rb") as f:
            artefact = f.read()
        empreintes, builds = _lire_frag_bld(frag_bld_par_carte[carte])
        nom = os.path.basename(chemin_artefact)
        build = builds.get(nom) or builds.get(nom.replace(".exe", ""))
        if not build:
            raise ErreurExport(f"{carte} : [build] {nom} introuvable au frag-bld")
        if build["empreinte"].removeprefix("sha256:") != hashlib.sha256(artefact).hexdigest():
            raise ErreurExport(f"{chemin_artefact} : empreinte entière divergente du frag-bld (R8)")
        blocs = []
        if table:
            blocs = table_blocs(artefact, table)
            for b in blocs:
                if empreintes.get(b["id"]) != b["empreinte"]:
                    raise ErreurExport(
                        f"{chemin_artefact} : bloc {b['id']} — empreinte aux offsets "
                        f"du plan {b['empreinte'][:12]}… ≠ frag-bld "
                        f"{empreintes.get(b['id'], 'ABSENT')[:12]}… — la géométrie "
                        "portée serait fausse (R8)")
            nb_empreintes += len(blocs)
        versions[profil] = build["version"]
        artefacts_manifeste.append({
            "chemin": chemin_artefact, "carte": carte, "profil": profil,
            "version": build["version"], "taille": len(artefact),
            "sha256": hashlib.sha256(artefact).hexdigest(), "blocs": blocs,
        })
    lignes.append(f"  verrou croisé R8 : {nb_empreintes} empreintes de blocs "
                  f"recalculées aux offsets du plan + {len(ARTEFACTS)} artefacts "
                  f"entiers — TOUTES conformes aux frag-bld (les DEUX ISA)")

    # (1) la preuve d'exécution AVANT l'export : l'état exporté est l'état
    #     VIVANT — les rituels rejoués sur les octets DU DISQUE (la couche B)
    qemu = _chemin_qemu()
    for chemin_artefact, _, profil, _ in ARTEFACTS:
        if chemin_artefact.startswith("m8/"):
            continue                       # le scellé win : son rituel vit au
                                             # poste Windows — le verrou (3) porte
                                             # ses octets ; frontière nommée
        with open(os.path.join(RACINE, chemin_artefact), "rb") as f:
            img = f.read()
        ok, detail = jouer_rituel(chemin_artefact, img,
                                  qemu if profil == "riscv64-linux-elf64" else None)
        if not ok:
            raise ErreurExport(f"le rituel de {chemin_artefact} n'est pas vert "
                               f"({detail}) — l'état exporté ne serait pas vivant")
    lignes.append("  rituels : corpus unix (natif) + corpus riscv (qemu) — les "
                  "DEUX lignes code 0 ; sondes unix/riscv — 4 lignes, VERDICT_FATAL "
                  "propre code 6 ; le scellé win se rejoue au poste Windows "
                  "(frontière nommée)")

    # (2) le manifeste
    manifeste = {
        "protocole": PROTOCOLE, "jalon": JALON,
        "profils": PROFILS, "versions": versions,
        "suite": {"hachage": "sha256", "signature": "ed25519",
                  "chiffrement": "xchacha20poly1305"},
        "empreinte_racine": "sha256:" + hashlib.sha256(b"".join(
            cc.lire_carte()[1][n] for n in cc.FRAGMENTS)).hexdigest(),
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "controles_export": [
            f"verrou croisé R8 multi-profils : {nb_empreintes} empreintes de blocs "
            f"(13+13 corpus, 4+4 sondes — les DEUX ISA) + {len(ARTEFACTS)} artefacts "
            "entiers, recalculés aux offsets du plan et recoupés aux frag-bld",
            "signatures R9 : le conteneur + les CINQ cartes transportées "
            "(vérificateur porté, prouvé équivalent aux modules du dépôt)",
            "rituels d'exécution VERTS au geste même : corpus unix natif et "
            "corpus riscv sous qemu (réserve instrumentale D149 : TCG, noyau "
            "et syscalls réels), sondes aux quatre lignes code 6",
            "l'oracle demeure EXCLU (D1) : régénéré depuis la couche I à l'arrivée",
        ],
        "cartes": cartes_manifeste,
        "artefacts": artefacts_manifeste,
        "restauration": "dépôt git + bundle Drive (D11, REPRISE) pour la notation "
                        "et la toolchain ; phrase maîtresse du coffre pour le "
                        "déchiffrement ; clés publiques des cartes transportées ; "
                        "oracle régénéré depuis I (D1) — jamais importé",
        "fichiers": [],
    }

    for chemin in FICHIERS_I + [os.path.join(RACINE, a) for a, _, _, _ in ARTEFACTS]:
        with open(chemin, "rb") as f:
            contenu = f.read()
        rel = os.path.relpath(chemin, RACINE)
        couche = "I" if os.sep + "I" + os.sep in chemin else "B"
        manifeste["fichiers"].append({
            "couche": couche, "chemin": rel,
            "sha256": hashlib.sha256(contenu).hexdigest(),
            "taille": len(contenu),
            "contenu": base64.b64encode(contenu).decode("ascii"),
        })
    for repertoire, f_entete, f_sig, f_pub, *_ in CARTES:
        for f in sorted(os.listdir(os.path.join(RACINE, repertoire))):
            chemin = os.path.join(RACINE, repertoire, f)
            if os.path.isdir(chemin):
                continue
            with open(chemin, "rb") as f2:
                contenu = f2.read()
            manifeste["fichiers"].append({
                "couche": "C", "chemin": os.path.relpath(chemin, RACINE),
                "sha256": hashlib.sha256(contenu).hexdigest(),
                "taille": len(contenu),
                "contenu": base64.b64encode(contenu).decode("ascii"),
            })
    nb_i = sum(1 for f in manifeste["fichiers"] if f["couche"] == "I")
    nb_b = sum(1 for f in manifeste["fichiers"] if f["couche"] == "B")
    nb_c = sum(1 for f in manifeste["fichiers"] if f["couche"] == "C")
    lignes.append(f"  contenu  : {len(manifeste['fichiers'])} fichiers — "
                  f"couches I ({nb_i}), B ({nb_b}), C ({nb_c})")

    # (3) le conteneur
    cle = cle_export_depuis_phrase(phrase)
    entete_clair = {"hachage": "sha256", "signature": "ed25519",
                    "chiffrement": "xchacha20poly1305",
                    "profils": ",".join(PROFILS),
                    "date": manifeste["date"],
                    "racine": bytes.fromhex(manifeste["empreinte_racine"].removeprefix("sha256:"))}
    conteneur = construire_conteneur(
        json.dumps(manifeste, ensure_ascii=False).encode("utf-8"),
        entete_clair, cle, prive)
    os.makedirs(EXPORT_DIR, exist_ok=True)
    nom = (f"TRIADE-continuite-multiprofils-{max(versions.values())}"
           f"-{manifeste['date'].replace(':', '').replace('-', '')}.bin")
    sortie = os.path.join(EXPORT_DIR, nom)
    with open(sortie, "wb") as f:
        f.write(conteneur)
    lignes.append(f"  conteneur : {nom} ({len(conteneur)} o, chiffré + signé)")
    lignes.append(f"  versions  : {versions}")
    return sortie, lignes


# --- L'import à sec — les CINQ ÉTAPES (FORMAT_CARTE § 8.2) ----------------------


def verifier(chemin: str, cle_publique: bytes | None = None) -> tuple[bool, list[str]]:
    lignes = [f"=== Import de continuité MULTI-PROFILS — les CINQ étapes : "
              f"{os.path.basename(chemin)} ==="]
    with open(chemin, "rb") as f:
        blob = f.read()
    try:
        entete, nonce, empreinte_ct, signature, ct, entete_brut = lire_conteneur(blob)
    except ErreurExport as exc:
        return False, lignes + [f"ÉCHEC (étape 0, parsing) : {exc}"]

    phrase, _ = cc.charger_secrets(interactif=False)

    # (1) DÉCHIFFREMENT — un échec est terminal, rien n'est interprété
    try:
        clair = crypto_aead_xchacha20poly1305_ietf_decrypt(
            ct, entete_brut + nonce, nonce, cle_export_depuis_phrase(phrase))
    except Exception:
        return False, lignes + ["ÉCHEC (étape 1) : déchiffrement impossible — phrase "
                                "maîtresse divergente ou conteneur altéré ; rien "
                                "n'est interprété (fail-closed)"]
    manifeste = json.loads(clair.decode("utf-8"))
    fichiers = {f["chemin"]: f for f in manifeste["fichiers"]}

    def octets_fichier(rel: str) -> bytes:
        if rel not in fichiers:
            raise ErreurExport(f"fichier absent du conteneur : {rel}")
        return base64.b64decode(fichiers[rel]["contenu"])

    # (2) SIGNATURE — le conteneur, puis chacune des cartes transportées
    def _lire_cle_publique(blob: bytes) -> bytes:
        # les cartes de l'ère courante portent l'hex ascii, la lignée win le
        # binaire 32 o — les deux graphies, UNE seule clé
        if len(blob) == 32:
            return blob
        try:
            return bytes.fromhex(blob.decode("ascii").strip())
        except (UnicodeDecodeError, ValueError) as exc:
            raise ErreurExport("clé publique illisible (ni 32 o binaires, ni hex "
                               f"ascii) : {exc}") from exc

    cles_transportees = set()
    for carte in manifeste["cartes"]:
        cles_transportees.add(_lire_cle_publique(
            octets_fichier(f"{carte['chemin']}/{carte['cle_publique']}")))
    if len(cles_transportees) != 1:
        return False, lignes + [f"ÉCHEC (étape 2) : {len(cles_transportees)} clés "
                                "publiques divergentes parmi les cartes transportées (R9)"]
    pub_transportee = next(iter(cles_transportees))
    if cle_publique is None:
        chemin_pub = os.path.join(ICI, "carte-corpus", "cle-publique.txt")
        cle_publique = pub_transportee
        ancrage = ("la clé publique TRANSPORTÉE (ancrage au conteneur — la "
                   "recouper par le dépôt git pour une confiance pleine)")
        if os.path.exists(chemin_pub):
            with open(chemin_pub, encoding="ascii") as f:
                if f.read().strip() != pub_transportee.hex():
                    return False, lignes + ["ÉCHEC (étape 2) : clé publique transportée "
                                            "≠ clé du dépôt (R9)"]
            cle_publique = pub_transportee
            ancrage = "la clé publique du projet (recoupée au dépôt)"
    try:
        Ed25519PublicKey.from_public_bytes(cle_publique).verify(
            signature, entete_brut + nonce + empreinte_ct + ct)
    except Exception:
        return False, lignes + ["ÉCHEC (étape 2) : signature du conteneur invalide (R9)"]
    lignes.append("  (1) déchiffrement : OK "
                  f"({len(clair)} o — Argon2id 64 Mio/3 it, sel export dédié)")
    lignes.append(f"  (2) signature du conteneur : Ed25519 valide — {ancrage}")
    nb_cartes_ok = 0
    for carte in manifeste["cartes"]:
        frags = {n: octets_fichier(f"{carte['chemin']}/{n}.bin")
                 for n in ("frag-loc", "frag-con", "frag-prf", "frag-bld")}
        ent = octets_fichier(f"{carte['chemin']}/{carte['entete']}")
        sig = octets_fichier(f"{carte['chemin']}/{carte['signature']}")
        try:
            Ed25519PublicKey.from_public_bytes(pub_transportee).verify(
                sig, ent + b"".join(frags[n] for n in
                                    ("frag-loc", "frag-con", "frag-prf", "frag-bld")))
        except Exception:
            return False, lignes + [f"ÉCHEC (étape 2) : signature de la carte "
                                    f"{carte['chemin']} invalide (R9)"]
        nb_cartes_ok += 1
    lignes.append(f"  (2) signatures des {nb_cartes_ok} cartes transportées : "
                  "Ed25519 valides (une seule lignée, D27)")

    # (3) VERROU CROISÉ — les empreintes de B recalculées == manifeste == frag-bld
    nb_blocs = nb_entiers = 0
    for artefact in manifeste["artefacts"]:
        img = octets_fichier(artefact["chemin"])
        if hashlib.sha256(img).hexdigest() != artefact["sha256"]:
            return False, lignes + [f"ÉCHEC (étape 3) : {artefact['chemin']} altéré "
                                    "dans le conteneur (sha divergent)"]
        carte = next(c for c in manifeste["cartes"] if c["chemin"] == artefact["carte"])
        blob_bld = octets_fichier(f"{carte['chemin']}/frag-bld.bin")
        bld = dechiffrer_fragment_portee(
            phrase, bytes.fromhex(carte["sel_argon2id"]),
            carte["sel_hkdf"].encode("ascii"), carte["generation"],
            "frag-bld", blob_bld).decode("utf-8")
        empreintes, builds = _lire_frag_bld(bld)
        nom_court = os.path.basename(artefact["chemin"])
        build = builds.get(nom_court) or builds.get(nom_court.replace(".exe", ""))
        if not build:
            return False, lignes + [f"ÉCHEC (étape 3) : [build] {nom_court} "
                                    f"absent du frag-bld de {carte['chemin']}"]
        if build["empreinte"].removeprefix("sha256:") != hashlib.sha256(img).hexdigest():
            return False, lignes + [f"ÉCHEC (étape 3) : {artefact['chemin']} — "
                                    "empreinte entière ≠ frag-bld (R8)"]
        if build["version"] != artefact["version"]:
            return False, lignes + [f"ÉCHEC (étape 3) : {artefact['chemin']} — "
                                    "version manifeste ≠ frag-bld"]
        nb_entiers += 1
        for b in artefact["blocs"]:
            extrait = img[b["offset"]:b["offset"] + b["taille"]]
            calc = hashlib.sha256(extrait).hexdigest()
            if calc != b["empreinte"]:
                return False, lignes + [f"ÉCHEC (étape 3) : bloc {b['id']} de "
                                        f"{artefact['chemin']} — empreinte "
                                        "recalculée ≠ manifeste (R8)"]
            if empreintes.get(b["id"]) != calc:
                return False, lignes + [f"ÉCHEC (étape 3) : bloc {b['id']} de "
                                        f"{artefact['chemin']} — empreinte "
                                        "manifeste ≠ frag-bld (R8)"]
            nb_blocs += 1
    lignes.append(f"  (3) verrou croisé : {nb_blocs} empreintes de blocs + "
                  f"{nb_entiers} artefacts entiers — recalculées aux offsets du "
                  "manifeste, conformes au manifeste ET aux frag-bld (R8, les DEUX ISA)")
    modifies = [f["chemin"] for f in manifeste["fichiers"]
                if hashlib.sha256(base64.b64decode(f["contenu"])).hexdigest() != f["sha256"]]
    if modifies:
        return False, lignes + [f"ÉCHEC (étape 3) : fichiers altérés : {modifies}"]

    # (4) ORACLE RÉGÉNÉRÉ depuis I — jamais importé (D1)
    specs_i = [f for f in manifeste["fichiers"] if f["couche"] == "I"]
    par_profil = {}
    for f in specs_i:
        racine_profil = f["chemin"].split(os.sep)[0]
        par_profil[racine_profil] = par_profil.get(racine_profil, 0) + 1
    detail = ", ".join(f"{v} specs {k}/I" for k, v in sorted(par_profil.items()))
    lignes.append(f"  (4) oracle : à régénérer depuis les {len(specs_i)} "
                  f"spécifications I ({detail}) — jamais importé (D1) ; au "
                  "laboratoire la preuve d'exécution rejoue les RITUELS sur "
                  "les octets TRANSPORTÉS")

    # (5) REPRISE — l'état scellé cohérent
    if entete["racine"].hex() not in octets_fichier(
            "riscv/carte-corpus/entete.txt").decode("ascii", errors="replace"):
        return False, lignes + ["ÉCHEC (étape 5) : empreinte racine incohérente "
                                "avec l'en-tête de la carte du jalon"]
    for profil, version in manifeste["versions"].items():
        lignes.append(f"      profil {profil} : scellé {version}")
    lignes.append(f"  (5) reprise : état scellé cohérent — carte du jalon "
                  f"racine {entete['racine'].hex()[:16]}…, {len(specs_i)} specs I, "
                  f"{nb_entiers} artefacts, {nb_cartes_ok} cartes ; reprise "
                  "normale possible")
    for controle in manifeste["controles_export"]:
        lignes.append(f"      export du {manifeste['date']} : {controle}")
    return True, lignes


# --- La preuve d'exécution de bout en bout (le geste labo de l'étape 4) ---------


def preuve_execution(chemin: str) -> tuple[bool, list[str]]:
    """L'étape 4 MENÉE : les rituels rejoués sur les octets DU CONTENEUR
    (déchiffrés en mémoire, écrit en temporaire — jamais le disque du dépôt)."""
    lignes = ["=== La preuve d'exécution de bout en bout : les rituels sur les "
              "octets TRANSPORTÉS ==="]
    with open(chemin, "rb") as f:
        blob = f.read()
    entete, nonce, _, _, ct, entete_brut = lire_conteneur(blob)
    phrase, _ = cc.charger_secrets(interactif=False)
    clair = crypto_aead_xchacha20poly1305_ietf_decrypt(
        ct, entete_brut + nonce, nonce, cle_export_depuis_phrase(phrase))
    manifeste = json.loads(clair.decode("utf-8"))
    fichiers = {f["chemin"]: base64.b64decode(f["contenu"])
                for f in manifeste["fichiers"]}
    qemu = _chemin_qemu()
    vert = True
    for artefact in manifeste["artefacts"]:
        if artefact["chemin"].startswith("m8/"):
            lignes.append(f"  [{os.path.basename(artefact['chemin'])}] scellé "
                          f"{artefact['version']} win — le rituel se rejoue au "
                          "poste Windows du développeur (frontière nommée : le "
                          "verrou croisé (3) porte ses octets)")
            continue
        ok, detail = jouer_rituel(artefact["chemin"], fichiers[artefact["chemin"]],
                                  qemu if artefact["profil"] == "riscv64-linux-elf64" else None)
        vert = vert and ok
        lignes.append(f"  [{os.path.basename(artefact['chemin'])}] "
                      f"{'PASS' if ok else 'ÉCHEC'} : {detail}")
    lignes.append("  VERDICT : " + ("VERT — l'export → l'import → la reprise SANS "
                                    "écart ; les rituels vivent dans les octets "
                                    "transportés (réserve instrumentale D149 "
                                    "nommée : qemu TCG, noyau et syscalls réels)"
                                    if vert else "KO"))
    return vert, lignes


# --- Coffre Drive (D11) ----------------------------------------------------------


def pousser_drive(chemin: str) -> tuple[bool, str]:
    import pathlib
    sys.path.insert(0, os.path.join(RACINE, "scripts"))
    import drive_sync
    drive_sync.upload_create(drive_sync.DRIVE_ROOT_ID, os.path.basename(chemin),
                             pathlib.Path(chemin))
    return True, (f"conteneur téléversé au racine du dossier Drive « Triade » : "
                  f"{os.path.basename(chemin)}")


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if "--verifier" in args:
            cible = args[args.index("--verifier") + 1]
            ok, rapport = verifier(cible)
            print("\n".join(rapport))
            sys.exit(0 if ok else 1)
        if "--pousser-drive" in args:
            cible = args[args.index("--pousser-drive") + 1]
            ok, message = pousser_drive(cible)
            print(("[coffre] " if ok else "[coffre] ÉCHEC : ") + message)
            sys.exit(0 if ok else 1)
        sortie, rapport = generer()
        print("\n".join(rapport))
        ok, verif = verifier(sortie)
        print("\n".join(verif))
        ok2, preuve = preuve_execution(sortie)
        print("\n".join(preuve))
        print(f"\n[export] {sortie}")
        print("[export] import à sec : " + ("OK" if ok else "ÉCHEC")
              + " ; preuve d'exécution : " + ("VERT" if ok2 else "KO"))
        sys.exit(0 if (ok and ok2) else 1)
    except (ErreurExport, cc.ErreurCarte, FileNotFoundError) as exc:
        print(f"ÉCHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
