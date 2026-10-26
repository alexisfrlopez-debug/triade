#!/usr/bin/env python3
"""export_continuite.py — Export de continuite chiffre et signe (D16, FORMAT_CARTE 8).

L'unique forme sous laquelle l'etat protocole quitte le poste de developpement :
couches I + B + C et manifeste autodescriptif, dans un conteneur unique chiffre
(XChaCha20-Poly1305 ; cle derivee de la phrase maitresse par Argon2id — memes
parametres que la carte au repos, contexte HKDF distinct) et signe (Ed25519,
la lignee de la carte — verifiable avec la cle publique commitee).

Contenu :
  I  m0/I/*.md, m1/I/*.md          contrats, pre/post-conditions, invariants
  B  m0/hello.exe, m1/selftest.exe binaires scelles du profil actif
  C  m0/carte/*, m1/carte/*        4 fragments + en-tete + signature + cle publique
  M  manifeste                     protocole, suite crypto, profils, empreinte
                                   racine, date, controles effectues a l'export

L'oracle est volontairement EXCLU (D1 : ephemere, regenere depuis I a l'arrivee).
La notation et la toolchain ne sont pas dans le conteneur : elles se restaurent
par l'infrastructure D11 (depot git + bundle Drive, REPRISE 4.1) — l'export
garantit l'ETAT SCELLE (carte avec compteurs de cristallisation et journal,
binaires, specifications) de bout en bout signe.

Format conteneur « TRIADE-EXP1 » :
  en-tete clair : magic, version, suite (3 algos), profils, date, empreinte
                  racine, nonce 24 o, sha256 du chiffretexte, signature Ed25519
                  (sur en-tete + nonce + empreinte + chiffretexte)
  chiffretexte   : AEAD(AAD = en-tete clair) du manifeste JSON + des fichiers

Usage (depuis m1/) :
  python3 export_continuite.py                generer + auto-verification import
  python3 export_continuite.py --verifier F   procedure d'import a sec sur F
  python3 export_continuite.py --pousser-drive F   copie de coffre au racine Drive
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import secrets
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layout as L

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_decrypt, crypto_aead_xchacha20poly1305_ietf_encrypt

import build_m1 as bm
import carte_m1 as cm

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
M0_DIR = os.path.join(RACINE, "m0")
EXPORT_DIR = os.path.join(ICI, "export")
MAGIC = b"TRIADE-EXP1"
FORMAT_VERSION = 1
PROTOCOLE = "0.4.0"

FICHIERS_I = sorted(
    [os.path.join(M0_DIR, "I", f) for f in os.listdir(os.path.join(M0_DIR, "I")) if f.endswith(".md")]
    + [os.path.join(ICI, "I", f) for f in os.listdir(os.path.join(ICI, "I")) if f.endswith(".md")]
)
FICHIERS_B = [os.path.join(M0_DIR, "hello.exe"), os.path.join(ICI, "selftest.exe")]
FICHIERS_C = [os.path.join(M0_DIR, "carte", f) for f in sorted(os.listdir(os.path.join(M0_DIR, "carte")))]
FICHIERS_C += [os.path.join(ICI, "carte", f) for f in sorted(os.listdir(os.path.join(ICI, "carte")))]


class ErreurExport(RuntimeError):
    """Tout echec de generation, dechiffrement ou de verification — fail-closed."""


# --- Cle du conteneur (meme lignee que la carte, contexte distinct) -------------

def cle_export(maitre: bytes) -> bytes:
    """HKDF-SHA256, contexte dedie a l'export (distinct des fragments, FORMAT_CARTE 8.1)."""
    return HKDF(algorithm=hashes.SHA256(), length=32,
                salt=b"TRIADE-export-continuite",
                info=b"export=v1;projet=TRIADE").derive(maitre)


def cle_export_depuis_phrase(phrase: bytes) -> bytes:
    """Argon2id 64 Mio / 3 it (parametres de la carte au repos) puis HKDF."""
    maitre = hash_secret_raw(secret=phrase, salt=cm.ARGON2_SALT,
                             time_cost=3, memory_cost=65536, parallelism=1,
                             hash_len=32, type=Type.ID)
    return cle_export(maitre)


# --- Serialization du conteneur --------------------------------------------------

def _champ(octets: bytes) -> bytes:
    return len(octets).to_bytes(2, "little") + octets


def _lire_champ(blob: bytes, offset: int) -> tuple[bytes, int]:
    n = int.from_bytes(blob[offset:offset + 2], "little")
    return blob[offset + 2:offset + 2 + n], offset + 2 + n


def construire_conteneur(plaintext: bytes, entete_clair: dict, cle: bytes,
                         prive: Ed25519PrivateKey) -> bytes:
    entete = (MAGIC + FORMAT_VERSION.to_bytes(2, "little")
              + _champ(entete_clair["hachage"].encode()) + _champ(entete_clair["signature"].encode())
              + _champ(entete_clair["chiffrement"].encode()) + _champ(entete_clair["profils"].encode())
              + _champ(entete_clair["date"].encode()) + entete_clair["racine"])
    nonce = secrets.token_bytes(24)
    ct = crypto_aead_xchacha20poly1305_ietf_encrypt(plaintext, entete + nonce, nonce, cle)
    empreinte_ct = hashlib.sha256(ct).digest()
    signature = prive.sign(entete + nonce + empreinte_ct + ct)
    return entete + nonce + empreinte_ct + signature + ct


def lire_conteneur(blob: bytes) -> tuple[dict, bytes, bytes, bytes, bytes, bytes]:
    """Retourne (entete_clair, nonce, empreinte_ct, signature, chiffretexte)."""
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
        raise ErreurExport("empreinte du chiffretexte divergente — conteneur altere")
    return entete, nonce, empreinte_ct, signature, ct, blob[:fin_entete]


# --- Generation -------------------------------------------------------------------

def _manifeste() -> tuple[dict, bytes]:
    """Controles a l'export + manifeste ; retourne (manifeste, empreinte_racine)."""
    blocs = bm.blocs_phase(2)
    nb, manifeste_carte = bm.verrou_croise(blocs)                 # R8/R9/D15 fresh
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("ascii")
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("ascii")
    crists = {ch["id"]: ch.get("crist", "?") for ch in
              (dict(re.findall(r"(\w+)=(\S+)", l)) for l in prf.splitlines() if l.startswith("[bloc]"))}
    avec_tableau = os.path.join(ICI, "carte", "tableau-de-bord.txt")
    with open(avec_tableau, encoding="ascii") as f:
        tableau = f.read()
    oracle = next((l.split(":", 1)[1].strip() for l in tableau.splitlines()
                   if l.strip().startswith("tests_differentiels")), "-")
    conformite = open(os.path.join(ICI, "conformite.txt"), encoding="ascii").read().strip()
    racine = cm.empreinte_racine(fragments)

    manifeste = {
        "protocole": PROTOCOLE,
        "jalon": "M1",
        "version_carte": manifeste_carte.get("version", "?"),
        "suite": {"hachage": "sha256", "signature": "ed25519", "chiffrement": "xchacha20poly1305"},
        "profils": ["x86-64-win11-pe"],
        "empreinte_racine": "sha256:" + racine.hex(),
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "controles_export": [
            f"verrou croise R8 : {nb} empreintes de blocs reverifiees contre les artefacts",
            "signature carte R9 : Ed25519 valide ; listes blanches D15 conformes",
            f"cristallisation R6 : {sum(1 for c in crists.values() if c == '10/10')}/{len(crists)} blocs a 10/10",
            f"dernier verdict oracle : {oracle}",
            f"suite de conformite profil : {conformite}",
        ],
        "restauration": "depot git + bundle Drive (D11, REPRISE 4.1) pour la notation et la "
                        "toolchain ; phrase maitresse du coffre pour le dechiffrement ; "
                        "oracle regenere depuis I (D1) ; procedure d'import FORMAT_CARTE 8.2",
        "fichiers": [],
    }
    return manifeste, racine


def generer() -> tuple[str, list[str]]:
    lignes = ["=== Export de continuite (D16) — generation ==="]
    manifeste, racine = _manifeste()
    for chemin in FICHIERS_I + FICHIERS_B + FICHIERS_C:
        with open(chemin, "rb") as f:
            contenu = f.read()
        couche = "I" if "/I/" in chemin.replace("\\", "/") else "B" if chemin.endswith(".exe") else "C"
        manifeste["fichiers"].append({
            "couche": couche,
            "chemin": os.path.relpath(chemin, RACINE),
            "sha256": hashlib.sha256(contenu).hexdigest(),
            "taille": len(contenu),
            "contenu": base64.b64encode(contenu).decode("ascii"),
        })
    for controle in manifeste["controles_export"]:
        lignes.append(f"  controle : {controle}")
    lignes.append(f"  contenu  : {len(manifeste['fichiers'])} fichiers "
                  f"({sum(f['taille'] for f in manifeste['fichiers'])} octets) "
                  f"— couches I ({len(FICHIERS_I)}), B ({len(FICHIERS_B)}), C ({len(FICHIERS_C)})")

    phrase, graine = cm.charger_secrets(interactif=False)
    cle = cle_export_depuis_phrase(phrase)
    prive, _ = cm.paire_cles(graine)
    entete_clair = {"hachage": "sha256", "signature": "ed25519",
                    "chiffrement": "xchacha20poly1305", "profils": "x86-64-win11-pe",
                    "date": manifeste["date"], "racine": racine}
    conteneur = construire_conteneur(json.dumps(manifeste, ensure_ascii=False).encode("utf-8"),
                                     entete_clair, cle, prive)
    os.makedirs(EXPORT_DIR, exist_ok=True)
    nom = f"TRIADE-continuite-{manifeste['version_carte']}-{manifeste['date'].replace(':', '').replace('-', '')}.bin"
    sortie = os.path.join(EXPORT_DIR, nom)
    with open(sortie, "wb") as f:
        f.write(conteneur)
    lignes.append(f"  conteneur : {nom} ({len(conteneur)} octets, chiffre + signe)")
    lignes.append(f"  racine    : sha256:{racine.hex()[:16]}...")
    return sortie, lignes


# --- Import (FORMAT_CARTE 8.2, cinq etapes) ----------------------------------------

def verifier(chemin: str) -> tuple[bool, list[str]]:
    lignes = [f"=== Import de continuite (FORMAT_CARTE 8.2) — verification a sec : {os.path.basename(chemin)} ==="]
    with open(chemin, "rb") as f:
        blob = f.read()
    try:
        entete, nonce, empreinte_ct, signature, ct, entete_brut = lire_conteneur(blob)
    except ErreurExport as exc:
        return False, lignes + [f"ECHEC (etape 0, parsing) : {exc}"]

    # (1) Dechiffrement — un echec est terminal, rien n'est interprete
    phrase, graine = cm.charger_secrets(interactif=False)
    try:
        clair = crypto_aead_xchacha20poly1305_ietf_decrypt(ct, entete_brut + nonce, nonce,
                                                           cle_export_depuis_phrase(phrase))
    except Exception:
        return False, lignes + ["ECHEC (etape 1) : dechiffrement impossible — phrase maitresse divergente "
                                "ou conteneur altere ; rien n'est interprete (fail-closed)"]
    lignes.append(f"  (1) dechiffrement : OK ({len(clair)} octets)")
    manifeste = json.loads(clair.decode("utf-8"))
    fichiers = {f["chemin"]: f for f in manifeste["fichiers"]}

    # (2) Signature du conteneur, puis de la carte qu'il contient
    pub = open(os.path.join(ICI, "carte", "cle-publique.ed25519"), "rb").read()
    try:
        Ed25519PublicKey.from_public_bytes(pub).verify(signature, entete_brut + nonce + empreinte_ct + ct)
    except Exception:
        return False, lignes + ["ECHEC (etape 2) : signature du conteneur invalide — refus (R9)"]
    lignes.append("  (2) signature du conteneur : Ed25519 valide (cle publique du projet, R9)")

    def octets_fichier(rel: str) -> bytes:
        return base64.b64decode(fichiers[rel]["contenu"])

    # Signature de la carte transportee (m1 = carte projet, generation 1)
    try:
        frag = {n: octets_fichier(f"m1/carte/{n}.bin") for n in cm.FRAGMENTS}
        frag["header.txt"] = octets_fichier("m1/carte/header.txt")
        cm.verifier_signature(octets_fichier("m1/carte/cle-publique.ed25519"),
                              frag["header.txt"], frag, octets_fichier("m1/carte/carte.sig"))
    except (KeyError, cm.ErreurCarte) as exc:
        return False, lignes + [f"ECHEC (etape 2) : signature de la carte transportee invalide (R9) : {exc}"]
    lignes.append("  (2) signature de la carte transportee : Ed25519 valide (R9)")

    # (3) Verrou croise : empreintes de B recalculees vs frag-bld du conteneur
    maitre = cm.cle_maitresse(phrase)
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", frag["frag-bld"]).decode("ascii")
    empreintes, manifestes = {}, []
    for ligne in bld.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[champs["id"]] = champs["empreinte"]
        elif ligne.startswith("[build]"):
            manifestes.append(dict(re.findall(r"(\w+)=(\S+)", ligne)))
    hello = octets_fichier("m0/hello.exe")
    selftest = octets_fichier("m1/selftest.exe")
    for bid, _, _, rva, slot in bm.blocs_phase(2):
        extrait = selftest[L.TEXT_FILE + (rva - L.TEXT_RVA): L.TEXT_FILE + (rva - L.TEXT_RVA) + slot]
        if "sha256:" + hashlib.sha256(extrait).hexdigest() != empreintes.get(bid):
            return False, lignes + [f"ECHEC (etape 3) : empreinte de {bid} divergente (R8) — reprise bloquee"]
    if "sha256:" + hashlib.sha256(selftest).hexdigest() != \
            next(m for m in manifestes if m.get("artefact") == "selftest.exe")["empreinte"]:
        return False, lignes + ["ECHEC (etape 3) : empreinte de selftest.exe divergente (R8)"]
    if "sha256:" + hashlib.sha256(hello[L.TEXT_FILE:L.TEXT_FILE + 64]).hexdigest() != empreintes.get("a10001"):
        return False, lignes + ["ECHEC (etape 3) : empreinte de a10001 divergente vs hello.exe (R8)"]
    if entete["racine"].hex() not in frag["header.txt"].decode("ascii", errors="replace"):
        return False, lignes + ["ECHEC (etape 3) : empreinte racine incoherente avec l'en-tete de carte"]
    lignes.append(f"  (3) verrou croise : {len(empreintes)} empreintes conformes, "
                  f"2 artefacts, racine coherente (R8)")
    # Integrite des fichiers transportes
    modifies = [f["chemin"] for f in manifeste["fichiers"]
                if hashlib.sha256(base64.b64decode(f["contenu"])).hexdigest() != f["sha256"]]
    if modifies:
        return False, lignes + [f"ECHEC : fichiers alteres dans le conteneur : {modifies}"]

    # (4) Regeneration de l'oracle depuis I — signalee (D1 : jamais importe)
    specs_i = [f for f in manifeste["fichiers"] if f["couche"] == "I"]
    lignes.append(f"  (4) oracle : a regenerer depuis les {len(specs_i)} specifications I "
                  f"a l'arrivee (D1 — jamais importe)")

    # (5) Reprise normale
    lignes.append(f"  (5) reprise : etat scelle coherent — carte {manifeste['version_carte']}, "
                  f"cristallisation consignee dans frag-prf ; reprise normale possible")
    for controle in manifeste["controles_export"]:
        lignes.append(f"      export du {manifeste['date']} : {controle}")
    return True, lignes


# --- Coffre Drive (D11) -------------------------------------------------------------

def pousser_drive(chemin: str) -> tuple[bool, str]:
    """Copie de coffre : televerse le conteneur au RACINE du dossier Drive (hors miroir)."""
    import pathlib
    sys.path.insert(0, os.path.join(RACINE, "scripts"))
    import drive_sync
    drive_sync.upload_create(drive_sync.DRIVE_ROOT_ID, os.path.basename(chemin),
                             pathlib.Path(chemin))
    return True, f"conteneur televerse au racine du dossier Drive « Triade » : {os.path.basename(chemin)}"


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
            print(("[coffre] " if ok else "[coffre] ECHEC : ") + message)
            sys.exit(0 if ok else 1)
        sortie, rapport = generer()
        print("\n".join(rapport))
        ok, verif = verifier(sortie)          # auto-verification immediatement
        print("\n".join(verif))
        print(f"\n[export] {sortie}")
        print("[export] round-trip import : " + ("OK" if ok else "ECHEC"))
        sys.exit(0 if ok else 1)
    except (ErreurExport, cm.ErreurCarte, FileNotFoundError) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
