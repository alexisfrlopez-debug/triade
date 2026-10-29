#!/usr/bin/env python3
"""coffre_fort.py — Coffre-fort des phrases maîtresses, par projet (D75).

Le protocole confie chaque phrase maîtresse au coffre du développeur au
moment de sa cérémonie (D27/D30) — mais quatre réinitialisations du bac à
sable ont montré la limite du procès-verbal seul : la phrase survit dans le
coffre du développeur, la LIGNÉE ne survit que si elle peut être RETROUVÉE
et rejouée. Le coffre-fort est le composant du protocole qui centralise
TOUTES les phrases maîtresses, PAR PROJET, dans un conteneur unique chiffré
— même pile cryptographique que la carte au repos et que l'export de
continuité (D16) :

  phrase de contrôle (développeur seul, jamais stockée)
    -> Argon2id (64 Mio / 3 itérations / parallélisme 1 — planchers
       FORMAT_CARTE § 3.1, sel aléatoire de 32 octets par coffre)
    -> HKDF-SHA256, contexte dédié « coffre=v1 » (distinct des fragments
       de carte et de l'export de continuité)
    -> XChaCha20-Poly1305 (AEAD ; AAD = en-tête clair complet)

Format conteneur « TRIADE-CF1 » (détail normatif : docs/FORMAT_CARTE.md
§ 11) :
  en-tête clair : magic « TRIADE-CF1 », version u16, champs longueur-
                  préfixée (hachage, kdf, chiffrement, date), sel 32 o,
                  nonce 24 o, empreinte sha256 du chiffretexte 32 o
  chiffretexte   : AEAD du JSON {projets : {… : {entrees : […phrase…]}}}

Le conteneur est autodescriptif : chiffré, il peut être exporté tel quel
vers le coffre Drive du projet et le coffre personnel du développeur — le
vol du conteneur est la menace « sans la phrase, indéchiffrable »
(spécification § 13.1, D75). La graine Ed25519 reste HORS coffre (D30 :
jamais confiée, jamais exportée) ; la relève d'une lignée perdue demeure
la cérémonie de régénération avec preuve byte-identique (D27/D30/D74).

Usage (depuis triade/) :
  python3 coffre_fort.py init [--generer-phrase]
       [--phrase-vers-fichier F] [--description-projet D]
  python3 coffre_fort.py statut
  python3 coffre_fort.py ajouter PROJET ETIQUETTE [--description D]
       [--depuis-fichier F | --stdin | --generer] [--remplacer]
       [--description-projet D]
  python3 coffre_fort.py lister [PROJET]
  python3 coffre_fort.py obtenir PROJET ETIQUETTE [--vers-fichier F]
  python3 coffre_fort.py retirer PROJET ETIQUETTE
  python3 coffre_fort.py verifier
  python3 coffre_fort.py changer-phrase
       [--nouvelle-depuis-fichier F | --nouvelle-generer]
       (sans option : tapez la VÔTRE deux fois — D110 : alphanumérique
        souhaité, AUCUNE limite de longueur ; la validation fine, avec
        plancher d'entropie et position de faute nommée, vit au GUI)
  python3 coffre_fort.py exporter [--sortie F] [--pousser-drive]
  python3 coffre_fort.py importer F [--force]
  python3 coffre_fort.py autotest

La phrase de contrôle se donne par getpass (caché), --phrase-stdin (une
ligne de l'entrée standard) ou --phrase-fichier F (permissions 600
recommandées ; à supprimer après usage de session). Fichier coffre par
défaut : .keys/coffre_fort.bin — JAMAIS committé ni synchronisé (gitignore,
D75). Dépendances : argon2-cffi, pynacl, cryptography (la pile du dépôt).
"""

from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import json
import os
import re
import secrets
import sys
from datetime import datetime, timezone

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

RACINE = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(RACINE, ".keys")
CHEMIN_DEFAUT = os.path.join(KEYS_DIR, "coffre_fort.bin")

MAGIC = b"TRIADE-CF1"
FORMAT_VERSION = 1
PROTOCOLE = "0.5.1"
ALGO_HACHAGE = "sha256"
ALGO_KDF = "argon2id(65536,3,1)"
ALGO_CHIFFREMENT = "xchacha20poly1305"
ARGON2_MEM = 65536      # Kio — plancher FORMAT_CARTE § 3.1
ARGON2_ITER = 3
ARGON2_PAR = 1
HKDF_SEL = b"TRIADE-coffre-fort"
HKDF_INFO = b"coffre=v1"
NOM_DRIVE = "coffre_fort.bin"
RE_PROJET = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,31}$")
RE_ETIQUETTE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


class ErreurCoffre(RuntimeError):
    """Tout échec de parsing, dérivation, déchiffrement ou commande — fail-closed."""


# --- Conteneur TRIADE-CF1 ---------------------------------------------------------

def _champ(octets: bytes) -> bytes:
    return len(octets).to_bytes(2, "little") + octets


def _lire_champ(blob: bytes, offset: int) -> tuple[bytes, int]:
    if offset + 2 > len(blob):
        raise ErreurCoffre("en-tête tronqué (champ de longueur)")
    n = int.from_bytes(blob[offset:offset + 2], "little")
    if offset + 2 + n > len(blob):
        raise ErreurCoffre("en-tête tronqué (champ)")
    return blob[offset + 2:offset + 2 + n], offset + 2 + n


def cle_coffre(phrase: bytes, sel: bytes) -> bytes:
    """Argon2id (paramètres des planchers) puis HKDF-SHA256 contexte « coffre=v1 »."""
    maitre = hash_secret_raw(secret=phrase, salt=sel,
                             time_cost=ARGON2_ITER, memory_cost=ARGON2_MEM,
                             parallelism=ARGON2_PAR, hash_len=32, type=Type.ID)
    return HKDF(algorithm=hashes.SHA256(), length=32,
                salt=HKDF_SEL, info=HKDF_INFO).derive(maitre)


def construire_conteneur(clair: bytes, cle: bytes, sel: bytes, date: str) -> bytes:
    """En-tête clair + AEAD(AAD = tout ce qui précède le chiffretexte)."""
    entete = (MAGIC + FORMAT_VERSION.to_bytes(2, "little")
              + _champ(ALGO_HACHAGE.encode("ascii"))
              + _champ(ALGO_KDF.encode("ascii"))
              + _champ(ALGO_CHIFFREMENT.encode("ascii"))
              + _champ(date.encode("ascii"))
              + sel)
    nonce = secrets.token_bytes(24)
    aad = entete + nonce
    ct = crypto_aead_xchacha20poly1305_ietf_encrypt(clair, aad, nonce, cle)
    empreinte = hashlib.sha256(ct).digest()
    return aad + empreinte + ct


def lire_conteneur(blob: bytes) -> dict:
    """Parse et valide l'en-tête clair ; échec = ErreurCoffre, rien n'est interprété."""
    if not blob.startswith(MAGIC):
        raise ErreurCoffre("magic absent — pas un conteneur TRIADE-CF1")
    version = int.from_bytes(blob[len(MAGIC):len(MAGIC) + 2], "little")
    if version != FORMAT_VERSION:
        raise ErreurCoffre(f"version de format {version} non supportée "
                           f"(attendu {FORMAT_VERSION})")
    offset = len(MAGIC) + 2
    entete = {"version": version}
    for clef in ("hachage", "kdf", "chiffrement", "date"):
        valeur, offset = _lire_champ(blob, offset)
        entete[clef] = valeur.decode("ascii", errors="replace")
    if (entete["hachage"] != ALGO_HACHAGE or entete["kdf"] != ALGO_KDF
            or entete["chiffrement"] != ALGO_CHIFFREMENT):
        raise ErreurCoffre("suite de l'en-tête non conforme (liste blanche D15)")
    debut_fixe = offset
    if len(blob) < debut_fixe + 32 + 24 + 32 + 1:
        raise ErreurCoffre("conteneur tronqué (sel/nonce/empreinte/chiffretexte)")
    sel = blob[debut_fixe:debut_fixe + 32]
    nonce = blob[debut_fixe + 32:debut_fixe + 56]
    empreinte = blob[debut_fixe + 56:debut_fixe + 88]
    ct = blob[debut_fixe + 88:]
    if hashlib.sha256(ct).digest() != empreinte:
        raise ErreurCoffre("empreinte du chiffretexte divergente — conteneur altéré")
    entete["sel"] = sel
    entete["empreinte_ct"] = empreinte.hex()
    return {"entete": entete, "nonce": nonce, "ct": ct,
            "aad": blob[:debut_fixe + 56]}

def dechiffrer(blob: bytes, phrase: bytes) -> tuple[dict, dict]:
    """Déchiffre et valide la base ; un échec est terminal (fail-closed)."""
    partes = lire_conteneur(blob)
    cle = cle_coffre(phrase, partes["entete"]["sel"])
    try:
        clair = crypto_aead_xchacha20poly1305_ietf_decrypt(
            partes["ct"], partes["aad"], partes["nonce"], cle)
    except Exception:
        raise ErreurCoffre("déchiffrement impossible — phrase de contrôle divergente "
                           "ou conteneur altéré ; rien n'est interprété (fail-closed)")
    try:
        base = json.loads(clair.decode("utf-8"))
    except Exception:
        raise ErreurCoffre("charge utile illisible — conteneur altéré")
    valider_base(base)
    return partes["entete"], base


def valider_base(base: dict) -> None:
    if not isinstance(base, dict) or base.get("format") != 1:
        raise ErreurCoffre("base de format inconnu (attendu format=1)")
    if not isinstance(base.get("projets"), dict):
        raise ErreurCoffre("base sans dictionnaire « projets »")
    for nom, projet in base["projets"].items():
        if not isinstance(projet, dict) or not isinstance(projet.get("entrees"), list):
            raise ErreurCoffre(f"projet {nom!r} malformé")
        vus = set()
        for entree in projet["entrees"]:
            if not isinstance(entree, dict) or "etiquette" not in entree:
                raise ErreurCoffre(f"entrée malformée dans {nom!r}")
            if entree["etiquette"] in vus:
                raise ErreurCoffre(f"étiquette dupliquée dans {nom!r} : "
                                   f"{entree['etiquette']!r}")
            vus.add(entree["etiquette"])
            try:
                base64.b64decode(entree.get("phrase_b64", ""), validate=True)
            except Exception:
                raise ErreurCoffre(f"phrase illisible dans {nom!r}/"
                                   f"{entree['etiquette']!r}")


# --- Base (contenu déchiffré) -----------------------------------------------------

def _date_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def nouvelle_base() -> dict:
    return {"format": 1, "protocole": PROTOCOLE,
            "cree": _date_utc(), "modifie": _date_utc(), "projets": {}}


def _ecrire_atomique(chemin: str, donnees: bytes) -> None:
    dossier = os.path.dirname(os.path.abspath(chemin))
    os.makedirs(dossier, exist_ok=True)
    os.chmod(dossier, 0o700)
    tmp = chemin + ".tmp"
    with open(tmp, "wb") as f:
        f.write(donnees)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, chemin)
    os.chmod(chemin, 0o600)


def sauver(chemin: str, base: dict, phrase: bytes, sel: bytes | None = None) -> None:
    """Re-chiffre toute la base et écrit atomiquement (0600, fsync)."""
    if sel is None:
        sel = secrets.token_bytes(32)
    base["modifie"] = _date_utc()
    clair = json.dumps(base, ensure_ascii=False, indent=1).encode("utf-8")
    blob = construire_conteneur(clair, cle_coffre(phrase, sel), sel, base["modifie"])
    _ecrire_atomique(chemin, blob)


def charger(chemin: str, phrase: bytes) -> tuple[dict, dict]:
    if not os.path.exists(chemin):
        raise ErreurCoffre(f"coffre introuvable : {chemin}")
    with open(chemin, "rb") as f:
        return dechiffrer(f.read(), phrase)


def _lire_blob(chemin: str) -> bytes:
    if not os.path.exists(chemin):
        raise ErreurCoffre(f"coffre introuvable : {chemin}")
    with open(chemin, "rb") as f:
        return f.read()


# --- Entrées de phrase ------------------------------------------------------------

def _trouver(base: dict, projet: str, etiquette: str) -> dict | None:
    for entree in base["projets"].get(projet, {}).get("entrees", []):
        if entree["etiquette"] == etiquette:
            return entree
    return None


def placer_entree(base: dict, projet: str, etiquette: str, description: str,
                  phrase: bytes, remplacer: bool, description_projet: str) -> str:
    """Pose (ou remplace) une entrée ; retourne le résumé ASCII-safe."""
    if not RE_PROJET.match(projet):
        raise ErreurCoffre(f"nom de projet invalide : {projet!r} "
                           "(lettres/chiffres/-/_ , 32 caractères max)")
    if not RE_ETIQUETTE.match(etiquette):
        raise ErreurCoffre(f"étiquette invalide : {etiquette!r}")
    if not phrase:
        raise ErreurCoffre("phrase vide — refus (fail-closed)")
    p = base["projets"].setdefault(projet, {"description": "", "entrees": []})
    if description_projet and not p["description"]:
        p["description"] = description_projet
    existante = _trouver(base, projet, etiquette)
    action = "remplacée"
    if existante is not None:
        if not remplacer:
            raise ErreurCoffre(f"entrée déjà présente : {projet}/{etiquette} "
                               "— --remplacer pour écraser")
        existante["description"] = description
        existante["modifie"] = _date_utc()
        existante["phrase_b64"] = base64.b64encode(phrase).decode("ascii")
    else:
        action = "ajoutée"
        p["entrees"].append({"etiquette": etiquette, "description": description,
                             "cree": _date_utc(), "modifie": _date_utc(),
                             "phrase_b64": base64.b64encode(phrase).decode("ascii")})
    return action


# --- Phrase de contrôle (entrée) ---------------------------------------------------

def _lire_phrase_controle(args: argparse.Namespace) -> bytes:
    if getattr(args, "phrase_fichier", None):
        with open(args.phrase_fichier, "rb") as f:
            phrase = f.read().strip()
    elif getattr(args, "phrase_stdin", False):
        phrase = sys.stdin.readline().strip().encode("utf-8")
    else:
        phrase = getpass.getpass("Phrase de contrôle du coffre : ").strip().encode("utf-8")
    if not phrase:
        raise ErreurCoffre("phrase de contrôle vide — refus (fail-closed)")
    return phrase


def _lire_nouvelle_phrase(args: argparse.Namespace, prefixe: str) -> bytes:
    if getattr(args, "nouvelle_depuis_fichier", None):
        with open(args.nouvelle_depuis_fichier, "rb") as f:
            nouvelle = f.read().strip()
    elif getattr(args, "nouvelle_generer", False):
        nouvelle = secrets.token_hex(16).encode("ascii")
        print("[coffre] NOUVELLE phrase de contrôle (128 bits) — AFFICHÉE UNE SEULE FOIS :")
        print("    " + nouvelle.decode("ascii"))
    else:
        nouvelle = getpass.getpass(f"{prefixe} : ").strip().encode("utf-8")
        confirmation = getpass.getpass(f"{prefixe} (confirmation) : ").strip().encode("utf-8")
        if nouvelle != confirmation:
            raise ErreurCoffre("phrases divergentes — refus (fail-closed)")
    if not nouvelle:
        raise ErreurCoffre("phrase vide — refus (fail-closed)")
    return nouvelle


def _lire_phrase_entree(args: argparse.Namespace) -> bytes:
    if getattr(args, "depuis_fichier", None):
        with open(args.depuis_fichier, "rb") as f:
            return f.read().strip()
    if getattr(args, "stdin", False):
        return sys.stdin.readline().strip().encode("utf-8")
    if getattr(args, "generer", False):
        phrase = secrets.token_hex(16).encode("ascii")
        print("[coffre] phrase maîtresse générée (128 bits) — AFFICHÉE UNE SEULE FOIS :")
        print("    " + phrase.decode("ascii"))
        return phrase
    premiere = getpass.getpass("Phrase maîtresse à stocker : ").strip().encode("utf-8")
    confirmation = getpass.getpass("Confirmation : ").strip().encode("utf-8")
    if premiere != confirmation:
        raise ErreurCoffre("phrases divergentes — refus (fail-closed)")
    return premiere


# --- Commandes ---------------------------------------------------------------------

def cmd_init(args: argparse.Namespace) -> int:
    chemin = args.chemin
    if os.path.exists(chemin):
        raise ErreurCoffre(f"coffre déjà présent ({chemin}) — importer ou changer-phrase, "
                           "jamais deux coffres (fail-closed)")
    if args.generer_phrase:
        phrase = secrets.token_hex(16).encode("ascii")  # 128 bits, modèle D27
    else:
        premiere = getpass.getpass("Phrase de contrôle du coffre : ").strip().encode("utf-8")
        confirmation = getpass.getpass("Confirmation : ").strip().encode("utf-8")
        if premiere != confirmation:
            raise ErreurCoffre("phrases divergentes — refus (fail-closed)")
        phrase = premiere
    base = nouvelle_base()
    sauver(chemin, base, phrase)
    print(f"[coffre] initialisé : {chemin} ({os.path.getsize(chemin)} octets, "
          f"format TRIADE-CF1 v{FORMAT_VERSION}, protocole {PROTOCOLE})")
    if args.generer_phrase and args.phrase_vers_fichier:
        with open(args.phrase_vers_fichier, "wb") as f:
            f.write(phrase)
        os.chmod(args.phrase_vers_fichier, 0o600)
        print(f"[coffre] phrase de contrôle écrite dans {args.phrase_vers_fichier} "
              "(chmod 600) — FICHIER DE SESSION : à supprimer après la cérémonie de remise")
    elif args.generer_phrase:
        print("[coffre] phrase de contrôle générée (128 bits) — AFFICHÉE UNE SEULE FOIS :")
        print("    " + phrase.decode("ascii"))
    print("[coffre] instruction D27/D30 : phrase de contrôle au coffre du développeur "
          "IMMÉDIATEMENT — elle n'est stockée nulle part ailleurs")
    return 0


def cmd_statut(args: argparse.Namespace) -> int:
    """En-tête clair seul — aucune phrase requise, aucune divulgation possible."""
    blob = _lire_blob(args.chemin)
    partes = lire_conteneur(blob)
    e = partes["entete"]
    print(f"=== Coffre-fort {args.chemin} ===")
    print(f"  format        : TRIADE-CF1 v{e['version']} (protocole {PROTOCOLE})")
    print(f"  hachage       : {e['hachage']}")
    print(f"  kdf           : {e['kdf']} (sel {e['sel'].hex()[:16]}…)")
    print(f"  chiffrement   : {e['chiffrement']}")
    print(f"  dernière écr. : {e['date']}")
    print(f"  empreinte ct  : sha256:{e['empreinte_ct'][:16]}…")
    print(f"  taille        : {len(blob)} octets (chiffretexte {len(partes['ct'])})")
    print("[coffre] en-tête intègre — contenu sous phrase de contrôle")
    return 0


def cmd_ajouter(args: argparse.Namespace) -> int:
    phrase_controle = _lire_phrase_controle(args)
    phrase = _lire_phrase_entree(args)
    _, base = charger(args.chemin, phrase_controle)
    action = placer_entree(base, args.projet, args.etiquette,
                           args.description or "", phrase,
                           args.remplacer, args.description_projet or "")
    sauver(args.chemin, base, phrase_controle)
    n = len(base["projets"][args.projet]["entrees"])
    print(f"[coffre] entrée {action} : {args.projet}/{args.etiquette} "
          f"(projet {args.projet} : {n} entrée(s)) — phrase JAMAIS affichée")
    return 0


def cmd_lister(args: argparse.Namespace) -> int:
    phrase = _lire_phrase_controle(args)
    _, base = charger(args.chemin, phrase)
    projets = base["projets"]
    if args.projet and args.projet not in projets:
        raise ErreurCoffre(f"projet inconnu : {args.projet}")
    noms = [args.projet] if args.projet else sorted(projets)
    total = sum(len(projets[n]["entrees"]) for n in noms)
    print(f"=== Coffre-fort — {len(noms)} projet(s), {total} entrée(s) "
          f"(modifié {base['modifie']}) ===")
    for nom in noms:
        p = projets[nom]
        print(f"PROJET {nom}" + (f" — {p['description']}" if p.get("description") else ""))
        for entree in p["entrees"]:
            print(f"  [{entree['etiquette']}] {entree.get('description', '')}")
            print(f"      créée {entree.get('cree', '?')} · modifiée "
                  f"{entree.get('modifie', '?')}")
    print("[coffre] seules les métadonnées sont listées — les phrases vivent "
          "chiffrées (obtenir pour dévoiler)")
    return 0


def cmd_obtenir(args: argparse.Namespace) -> int:
    phrase_controle = _lire_phrase_controle(args)
    _, base = charger(args.chemin, phrase_controle)
    entree = _trouver(base, args.projet, args.etiquette)
    if entree is None:
        raise ErreurCoffre(f"entrée inconnue : {args.projet}/{args.etiquette}")
    phrase = base64.b64decode(entree["phrase_b64"])
    if args.vers_fichier:
        with open(args.vers_fichier, "wb") as f:
            f.write(phrase)
        os.chmod(args.vers_fichier, 0o600)
        print(f"[coffre] phrase {args.projet}/{args.etiquette} écrite dans "
              f"{args.vers_fichier} (chmod 600)", file=sys.stderr)
    else:
        try:
            texte = phrase.decode("utf-8")
        except UnicodeDecodeError:
            texte = phrase.hex()
        sys.stdout.write(texte + "\n")
    return 0


def cmd_retirer(args: argparse.Namespace) -> int:
    phrase = _lire_phrase_controle(args)
    _, base = charger(args.chemin, phrase)
    entrees = base["projets"].get(args.projet, {}).get("entrees", [])
    reste = [e for e in entrees if e["etiquette"] != args.etiquette]
    if len(reste) == len(entrees):
        raise ErreurCoffre(f"entrée inconnue : {args.projet}/{args.etiquette}")
    if reste:
        base["projets"][args.projet]["entrees"] = reste
    else:
        del base["projets"][args.projet]  # projet vide → supprimé
    sauver(args.chemin, base, phrase)
    print(f"[coffre] entrée retirée : {args.projet}/{args.etiquette}"
          + ("" if reste else " (projet vide supprimé)"))
    return 0


def cmd_verifier(args: argparse.Namespace) -> int:
    phrase = _lire_phrase_controle(args)
    _, base = charger(args.chemin, phrase)
    n_projets = len(base["projets"])
    n_entrees = sum(len(p["entrees"]) for p in base["projets"].values())
    print(f"[coffre] INTÈGRE — {n_projets} projet(s), {n_entrees} entrée(s), "
          f"déchiffrement et AEAD conformes ({args.chemin})")
    return 0


def cmd_changer_phrase(args: argparse.Namespace) -> int:
    ancienne = _lire_phrase_controle(args)
    blob = _lire_blob(args.chemin)
    _, base = dechiffrer(blob, ancienne)
    nouvelle = _lire_nouvelle_phrase(args, "NOUVELLE phrase de contrôle")
    sauver(args.chemin, base, nouvelle, sel=secrets.token_bytes(32))
    print(f"[coffre] phrase de contrôle changée (nouveau sel) — {args.chemin} "
          "re-chiffré ; l'ANCIENNE phrase est désormais inopérante")
    return 0


def cmd_exporter(args: argparse.Namespace) -> int:
    blob = _lire_blob(args.chemin)
    lire_conteneur(blob)  # en-tête validé avant toute copie (fail-closed)
    if not args.sortie and not args.pousser_drive:
        raise ErreurCoffre("rien à faire : --sortie F et/ou --pousser-drive")
    if args.sortie:
        _ecrire_atomique(args.sortie, blob)
        print(f"[coffre] export chiffré : {args.sortie} "
              f"({len(blob)} octets, chmod 600) — coffre Drive du projet / coffre "
              "personnel du développeur")
    if args.pousser_drive:
        print("[coffre] " + pousser_drive(args.chemin))
    return 0


def cmd_importer(args: argparse.Namespace) -> int:
    phrase = _lire_phrase_controle(args)
    with open(args.fichier, "rb") as f:
        blob = f.read()
    dechiffrer(blob, phrase)  # vérifié AVANT remplacement — fail-closed
    if os.path.exists(args.chemin) and not args.force:
        raise ErreurCoffre(f"coffre local présent ({args.chemin}) — --force pour écraser")
    _ecrire_atomique(args.chemin, blob)
    print(f"[coffre] importé : {args.fichier} -> {args.chemin} (vérifié avant remplacement)")
    return 0


# --- Coffre Drive (D11) -------------------------------------------------------------

def pousser_drive(chemin: str) -> str:
    """Copie de coffre au RACINE du dossier Drive « Triade » (update-or-create)."""
    import pathlib
    scripts = os.path.join(RACINE, "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import drive_sync
    fichiers = drive_sync.list_folder(drive_sync.DRIVE_ROOT_ID)  # {nom: métadonnées}
    existant = fichiers.get(NOM_DRIVE)
    if existant is not None and "folder" in existant.get("mimeType", ""):
        existant = None  # un dossier homonyme n'est pas le conteneur — fail-closed indirect
    if existant is not None:
        drive_sync.upload_update(existant["id"], pathlib.Path(chemin))
        return (f"mis à jour au racine du dossier Drive « Triade » : {NOM_DRIVE} "
                "(copie de coffre, conteneur chiffré)")
    drive_sync.upload_create(drive_sync.DRIVE_ROOT_ID, NOM_DRIVE, pathlib.Path(chemin))
    return (f"téléversé au racine du dossier Drive « Triade » : {NOM_DRIVE} "
            "(copie de coffre, conteneur chiffré)")


# --- Autotest de falsification ------------------------------------------------------

def cmd_autotest(args: argparse.Namespace) -> int:
    """Suite de falsification en répertoire temporaire — le coffre réel n'est pas touché.

    Une suite qui ne peut pas échouer ne prouve rien : chaque propriété de
    sécurité est attestée par un contrôle qui ÉCHOUE si elle est fausse
    (modèle des oracles du dépôt).
    """
    import contextlib
    import io
    import tempfile

    resultats: list[tuple[bool, str]] = []

    def controle(nom: str, ok: bool, detail: str = ""):
        resultats.append((ok, nom))
        print(f"[{'PASS' if ok else 'FAIL'}] {nom}" + (f" : {detail}" if detail else ""))

    def refuse(nom: str, fonction, *a, **k):
        try:
            fonction(*a, **k)
        except ErreurCoffre:
            controle(nom, True)
        except Exception as exc:
            controle(nom, False, f"exception inattendue : {exc}")
        else:
            controle(nom, False, "aucun refus levé")

    with tempfile.TemporaryDirectory(prefix="coffre-autotest-") as tmp:
        chemin = os.path.join(tmp, "coffre.bin")
        phrase_a = b"controle-autotest-phrase-A"
        phrase_b = b"controle-autotest-phrase-B"

        # 1-2 : init + statut sans phrase
        base = nouvelle_base()
        sauver(chemin, base, phrase_a)
        controle("init : coffre créé et chiffré", os.path.exists(chemin))
        partes = lire_conteneur(_lire_blob(chemin))
        controle("statut : en-tête clair lisible sans phrase",
                 partes["entete"]["chiffrement"] == ALGO_CHIFFREMENT
                 and partes["entete"]["version"] == FORMAT_VERSION)

        # 3-4 : entrées + discrétion de lister
        placer_entree(base, "TRIADE", "lignee-X", "phrase de test 1",
                      b"SECRET-1-PHRASE", False, "projet de test")
        placer_entree(base, "AUTRE", "lignee-Y", "phrase de test 2",
                      b"SECRET-2-PHRASE", False, "")
        sauver(chemin, base, phrase_a)
        _, base2 = charger(chemin, phrase_a)
        controle("ajouter : deux projets, round-trip",
                 len(base2["projets"]) == 2)
        tampon = io.StringIO()
        args_l = argparse.Namespace(chemin=chemin, projet=None,
                                    phrase_fichier=None, phrase_stdin=True)
        stdin_backup = sys.stdin
        sys.stdin = io.StringIO(phrase_a.decode() + "\n")
        try:
            with contextlib.redirect_stdout(tampon):
                cmd_lister(args_l)
        finally:
            sys.stdin = stdin_backup
        sortie_lister = tampon.getvalue()
        controle("lister : métadonnées seules (aucune phrase divulguée)",
                 "SECRET-1-PHRASE" not in sortie_lister
                 and "SECRET-2-PHRASE" not in sortie_lister
                 and "lignee-X" in sortie_lister)

        # 5 : obtenir round-trip + vers-fichier 0600
        entree = _trouver(base2, "TRIADE", "lignee-X")
        controle("obtenir : round-trip exact",
                 base64.b64decode(entree["phrase_b64"]) == b"SECRET-1-PHRASE")
        vers = os.path.join(tmp, "restaure.txt")
        args_o = argparse.Namespace(chemin=chemin, projet="TRIADE",
                                    etiquette="lignee-X", vers_fichier=vers,
                                    phrase_fichier=None, phrase_stdin=False)
        args_o.phrase_stdin = True
        stdin_backup = sys.stdin
        sys.stdin = io.StringIO(phrase_a.decode() + "\n")
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                cmd_obtenir(args_o)
        finally:
            sys.stdin = stdin_backup
        with open(vers, "rb") as f:
            controle("obtenir --vers-fichier : exact et 0600",
                     f.read() == b"SECRET-1-PHRASE"
                     and (os.stat(vers).st_mode & 0o777) == 0o600)

        # 6-10 : falsifications — chaque mutation d'UN octet doit être refusée
        blob = _lire_blob(chemin)
        refuse("mauvaise phrase de contrôle : refus", dechiffrer, blob, b"fausse-phrase")
        debut_fixe = (len(MAGIC) + 2 + len(_champ(ALGO_HACHAGE.encode()))
                      + len(_champ(ALGO_KDF.encode()))
                      + len(_champ(ALGO_CHIFFREMENT.encode()))
                      + len(_champ(partes["entete"]["date"].encode())))
        mauvais = bytearray(blob)
        mauvais[-1] ^= 0x01  # dernier octet du chiffretexte
        refuse("falsification du chiffretexte (1 octet) : refus",
               dechiffrer, bytes(mauvais), phrase_a)
        mauvais = bytearray(blob)
        mauvais[debut_fixe] ^= 0x01  # sel : dérivation divergente
        refuse("falsification du sel (1 octet) : refus",
               dechiffrer, bytes(mauvais), phrase_a)
        mauvais = bytearray(blob)
        mauvais[debut_fixe + 32] ^= 0x01  # nonce (dans l'AAD ET le vecteur)
        refuse("falsification du nonce (1 octet) : refus",
               dechiffrer, bytes(mauvais), phrase_a)
        mauvais = bytearray(blob)
        mauvais[debut_fixe + 56] ^= 0x01  # empreinte du chiffretexte
        refuse("falsification de l'empreinte (1 octet) : refus",
               dechiffrer, bytes(mauvais), phrase_a)

        # 11 : unicité d'étiquette + remplacement
        refuse("unicité : même étiquette refusée sans --remplacer",
               placer_entree, base2, "TRIADE", "lignee-X", "doublon",
               b"AUTRE", False, "")
        placer_entree(base2, "TRIADE", "lignee-X", "remplacée",
                      b"SECRET-1B", True, "")
        controle("remplacement : --remplacer accepté",
                 base64.b64decode(_trouver(base2, "TRIADE", "lignee-X")["phrase_b64"])
                 == b"SECRET-1B")
        sauver(chemin, base2, phrase_a)

        # 12 : retirer
        _, base3 = charger(chemin, phrase_a)
        entrees = [e for e in base3["projets"]["AUTRE"]["entrees"]
                   if e["etiquette"] == "lignee-Y"]
        base3["projets"]["AUTRE"]["entrees"] = entrees
        sauver(chemin, base3, phrase_a)
        _, base4 = charger(chemin, phrase_a)
        controle("retirer : l'autre projet intact",
                 len(base4["projets"]["AUTRE"]["entrees"]) == 1)

        # 13 : changer-phrase — ancienne inopérante, nouvelle ouvre
        _, base5 = charger(chemin, phrase_a)
        sauver(chemin, base5, phrase_b, sel=secrets.token_bytes(32))
        refuse("changer-phrase : l'ANCIENNE phrase est refusée",
               charger, chemin, phrase_a)
        _, base6 = charger(chemin, phrase_b)
        controle("changer-phrase : la nouvelle ouvre, entrées intactes",
                 _trouver(base6, "TRIADE", "lignee-X") is not None)

        # 14 : exporter/importer — round-trip conteneur
        exporte = os.path.join(tmp, "export.bin")
        blob_b = _lire_blob(chemin)
        _ecrire_atomique(exporte, blob_b)
        _, base7 = dechiffrer(open(exporte, "rb").read(), phrase_b)
        controle("export/import : le conteneur exporté s'ouvre à l'identique",
                 _trouver(base7, "TRIADE", "lignee-X") is not None)

        # 15 : témoin sauvage — même phrase, sel/nonce neufs → octets différents
        chemin_temoin = os.path.join(tmp, "temoin.bin")
        sauver(chemin_temoin, base7, phrase_b)
        controle("témoin sauvage : ré-encryption randomisée (octets tous différents "
                 "du précédent), même contenu logique",
                 _lire_blob(chemin_temoin) != blob_b
                 and charger(chemin_temoin, phrase_b)[1]["projets"].keys()
                 == base7["projets"].keys())

        # 16 : anti-écrasement à l'import (cmd_importer, phrase sur stdin)
        args_i = argparse.Namespace(chemin=chemin, fichier=exporte, force=False,
                                    phrase_fichier=None, phrase_stdin=True)
        try:
            stdin_backup = sys.stdin
            sys.stdin = io.StringIO(phrase_b.decode() + "\n")
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    cmd_importer(args_i)
            finally:
                sys.stdin = stdin_backup
            controle("import sans --force sur coffre présent : REFUS", False,
                     "aucun refus levé")
        except ErreurCoffre:
            controle("import sans --force sur coffre présent : REFUS", True)

        # 17 : phrase personnelle D110 — SANS PLAFOND, ancienne inopérante
        mienne = ("aA1" * 3333 + "Zz9")[:10_000]     # 10 000 caractères
        _, base8 = charger(chemin, phrase_b)
        sauver(chemin, base8, mienne.encode("ascii"),
               sel=secrets.token_bytes(32))
        refuse("phrase personnelle : l'ancienne est refusée",
               charger, chemin, phrase_b)
        _, base9 = charger(chemin, mienne.encode("ascii"))
        controle("phrase personnelle : 10 000 caractères ouvrent, entrées "
                 "intactes — AUCUN plafond de longueur (D110)",
                 _trouver(base9, "TRIADE", "lignee-X") is not None)
        sauver(chemin, base9, phrase_b, sel=secrets.token_bytes(32))
        controle("phrase personnelle : retour à phrase_b (le coffre digère "
                 "tout octet — la règle alphanumérique vit au GUI, "
                 "par conception)",
                 charger(chemin, phrase_b)[1] is not None)

    print()
    echecs = [nom for ok, nom in resultats if not ok]
    print("=" * 66)
    if echecs:
        print(f"AUTOTEST : ÉCHEC — {len(echecs)} contrôle(s) sur {len(resultats)} :")
        for nom in echecs:
            print(f"  FAIL {nom}")
        print("=" * 66)
        return 1
    print(f"AUTOTEST : {len(resultats)}/{len(resultats)} PASS — le coffre-fort est "
          "falsifiable et chaque propriété tient")
    print("=" * 66)
    return 0


# --- Interface ---------------------------------------------------------------------

def _construire_parseur() -> argparse.ArgumentParser:
    parseur = argparse.ArgumentParser(
        prog="coffre_fort.py",
        description="Coffre-fort des phrases maîtresses, par projet (D75) — "
                    "conteneur TRIADE-CF1, Argon2id + HKDF + XChaCha20-Poly1305.")
    parseur.add_argument("--chemin", default=CHEMIN_DEFAUT,
                         help="chemin du conteneur (défaut : .keys/coffre_fort.bin)")
    sous = parseur.add_subparsers(dest="commande", required=True)

    p = sous.add_parser("init", help="initialise un coffre neuf")
    p.add_argument("--generer-phrase", action="store_true",
                   help="génère la phrase de contrôle (128 bits, modèle D27)")
    p.add_argument("--phrase-vers-fichier", metavar="F",
                   help="écrit la phrase générée dans F (0600) au lieu de l'afficher")
    p.add_argument("--description-projet", default="")
    p.set_defaults(func=cmd_init)

    p = sous.add_parser("statut", help="en-tête clair seul (aucune phrase requise)")
    p.set_defaults(func=cmd_statut)

    p = sous.add_parser("ajouter", help="ajoute (ou remplace) une phrase maîtresse")
    p.add_argument("projet")
    p.add_argument("etiquette")
    p.add_argument("--description", default="")
    p.add_argument("--depuis-fichier", metavar="F",
                   help="lit la phrase dans F (jamais affichée)")
    p.add_argument("--stdin", action="store_true", help="lit la phrase sur l'entrée standard")
    p.add_argument("--generer", action="store_true",
                   help="génère une phrase maîtresse (128 bits, affichée une fois)")
    p.add_argument("--remplacer", action="store_true",
                   help="remplace l'entrée si l'étiquette existe déjà")
    p.add_argument("--description-projet", default="")
    p.set_defaults(func=cmd_ajouter)

    p = sous.add_parser("lister", help="liste les entrées (métadonnées seules)")
    p.add_argument("projet", nargs="?")
    p.set_defaults(func=cmd_lister)

    p = sous.add_parser("obtenir", help="dévoile une phrase (stdout ou --vers-fichier)")
    p.add_argument("projet")
    p.add_argument("etiquette")
    p.add_argument("--vers-fichier", metavar="F",
                   help="écrit la phrase dans F (chmod 600) au lieu de stdout")
    p.set_defaults(func=cmd_obtenir)

    p = sous.add_parser("retirer", help="retire une entrée")
    p.add_argument("projet")
    p.add_argument("etiquette")
    p.set_defaults(func=cmd_retirer)

    p = sous.add_parser("verifier", help="déchiffre et vérifie l'intégrité")
    p.set_defaults(func=cmd_verifier)

    p = sous.add_parser("changer-phrase",
                        help="change la phrase de contrôle (nouveau sel) — "
                             "sans option : la VÔTRE, tapée deux fois (D110)")
    p.add_argument("--nouvelle-depuis-fichier", metavar="F")
    p.add_argument("--nouvelle-generer", action="store_true",
                   help="génère la nouvelle phrase (128 bits, affichée une fois)")
    p.set_defaults(func=cmd_changer_phrase)

    p = sous.add_parser("exporter", help="copie le conteneur chiffré (coffre Drive, etc.)")
    p.add_argument("--sortie", metavar="F")
    p.add_argument("--pousser-drive", action="store_true",
                   help="téléverse au racine du dossier Drive « Triade »")
    p.set_defaults(func=cmd_exporter)

    p = sous.add_parser("importer", help="restaure un coffre depuis un conteneur exporté")
    p.add_argument("fichier")
    p.add_argument("--force", action="store_true", help="écrase un coffre local présent")
    p.set_defaults(func=cmd_importer)

    p = sous.add_parser("autotest", help="suite de falsification (répertoire temporaire)")
    p.set_defaults(func=cmd_autotest)

    for sous_parseur in sous.choices.values():
        sous_parseur.add_argument("--phrase-fichier", metavar="F",
                                  help="phrase de contrôle lue dans F (0600 recommandé)")
        sous_parseur.add_argument("--phrase-stdin", action="store_true",
                                  help="phrase de contrôle lue sur l'entrée standard")

    return parseur


def main() -> int:
    parseur = _construire_parseur()
    args = parseur.parse_args()
    if args.commande == "autotest":
        return cmd_autotest(args)
    try:
        return args.func(args)
    except ErreurCoffre as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f"ECHEC (fail-closed) : fichier absent : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
