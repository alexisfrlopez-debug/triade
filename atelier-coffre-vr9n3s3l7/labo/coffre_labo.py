#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coffre_labo.py — LE MINI-COFFRE DE LABORATOIRE « LCF3 » (l'atelier
coffre-vr9n3s3l7, vague 11 — le plan gelé PLAN-VR9N3S3L7.md items (a)(b)(c)).

COPIE DE LABORATOIRE AUTOPORTÉE du coffre CF3 (v06/coffre_cf3.py — RÉFÉRENCE
JAMAIS MODIFIÉE, jamais importée : le laboratoire ne touche AUCUN coffre
réel, AUCUNE phrase réelle — discipline D105 ; la phrase de test publique
« PHRASE-TEST-PUBLIQUE-D105-vague11-labo » est la SEULE phrase manipulée).

Les TROIS durcissements demandés par le plan, à la lettre :

  (a) L'EMPREINTE DU CHIFFRETEXTE AVANT L'AEAD (la sentinelle instantanée
      étendue). L'empreinte 32 o du conteneur n'est PLUS un sha256 nu — elle
      est LIÉE À LA CLÉ : empreinte = HMAC-SHA256(K_emp, chiffretexte) avec
      K_emp = HKDF(K_user ‖ S_piège ; sel_hkdf ; « …/empreinte/v1 »). LA
      NOUVELLE LOI D'ORDRE (l'étage 5 de la sentinelle, AVANT l'AEAD) :
        - HMAC conforme                 → étage 6 (AEAD, la preuve restante) ;
        - HMAC diverge ET l'empreinte
          stockée == sha256(ct) naïf    → FALSIFICATION À EMPREINTE VALIDE :
                                          l'attaquant a réécrit le
                                          chiffretexte ET son empreinte — la
                                          paire est « valide » seulement sous
                                          la lecture naïve (sha256 nu), que
                                          le détenteur de la clé réfute :
                                          DESTRUCTION LOCALE + PROCÈS-VERBAL ;
        - HMAC diverge, naïf diverge    → CORRUPTION (panne/incident) :
                                          REFUS NOMMÉ SANS DESTRUCTION, le
                                          chiffretexte CONSERVÉ pour analyse
                                          (jamais la destruction sur un
                                          incident). BORNE CONSIGNÉE : une
                                          falsification SANS la clé (empreinte
          réécrite aléatoirement) se présente comme corruption — refus
          nommé, fail-closed : sans K_emp rien ne s'ouvre, et la destruction
          attend la PREUVE (la cohérence naïve).

  (b) V_piège DÉRIVÉE : V_piège = HKDF(S_piège ; sel fixe ;
      « piège » ‖ époque_le64) — 16 o, LIÉE au secret du piège ET à
      l'époque. Le fichier piège ne PORTE PLUS de V_piège aléatoire : il
      porte S_piège, et l'information de vérification (verif) est calculée
      À L'ÉPOQUE : verif = sha256(HKDF(K_user ‖ V_piège(épo-
      que) ; sel_hkdf ; « …/verif/v1 »))[:16]. L'époque retirée est REFUSÉE
      nommément (piège PÉRIMÉ / RETOUR EN ARRIÈRE — anti-rollback au piège).

  (c) L'AGILITÉ ARGON2 : les paramètres (mémoire, itérations, parallélisme)
      VERSIONNÉS AU CONTENEUR par un INDEX p_idx dans une LISTE BLANCHE
      (0 : 65536/3/1 plancher miroir CF1-CF3 ; 1 : 262144/4/1 ; 2 :
      524288/4/2). Toute valeur hors liste = REFUS NOMMÉ à l'ouverture. LA
      CÉRÉMONIE DE RE-PARAMÉTRAGE (ceremonie_reparametrage) : ancien
      conteneur vérifié vert, plancher d'entropie re-vérifié, paramètres
      neufs, conteneur ré-écrit à époque+1, RE-LECTURE À FROID avant
      remplacement atomique. LE PLANCHER D'ENTROPIE DE PHRASE (valeur gelée
      60 bits) : estimer_entropie() — dictionnaire FR/EN intégré (~430 mots
      courants, 11 bits par mot du dictionnaire), longueur, classes de
      caractères, dé-leétification minimale — REFUSANTE sous le plancher
      (ErreurPlancherEntropie, la valeur estimée NOMMÉE).

Modes de défaillance (miroir CF3 spec § 5) : phrase erronée = BÉNIGNE
(PhraseErronee, réessai, JAMAIS de destruction) ; falsification PROUVÉE
côté machine = destruction LOCALE + PV (JAMAIS le média du piège, JAMAIS
les parts du séquestre). Discipline RAM : K_user/KEK/K_emp en bytearray,
effacés après usage au mieux de Python.

Format conteneur « TRIADE-LCF3 » (petit-boutiste — DISTINCT du CF3 réel,
jamais confondable) :
  "TRIADE-LCF3" 11 o | version u16 (=2) | époque u64 | H_projet 32 o |
  sel_argon 16 o | p_idx u32 | sel_hkdf 32 o | S_serrure 32 o | nonce 24 o |
                        <- fin de l'AAD (175 o)
  empreinte 32 o = HMAC-SHA256(K_emp, chiffretexte) | verif 16 o |
  chiffretexte = XChaCha20-Poly1305(clair, aad, nonce, KEK)

Fichier piège « TRIADE-LCF3-PIEGE v2 » (texte ascii) :
  epoque / projet (H_projet hex) / piege (S_piège hex 32 o) /
  tag = sha256(ctx ‖ époque ‖ H_projet ‖ S_piège)[:8] — V_piège DÉRIVÉE,
  jamais stockée (b).

Dépendances : argon2-cffi, pynacl, cryptography (la pile du dépôt).
"""
from __future__ import annotations

import hashlib
import hmac
import json
import math
import os
import secrets
import sys
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

# ---------------------------------------------------------------------------
# Constantes normatives (les valeurs NOMMÉES du plan)
# ---------------------------------------------------------------------------

MAGIC = b"TRIADE-LCF3"                # 11 o — LABO, distinct de TRIADE-CF3
MAGIC_PIEGE = "TRIADE-LCF3-PIEGE v2"
FORMAT_VERSION = 2
PROTOCOLE = "labo-vr9n3s3l7"

# (c) la liste blanche des jeux Argon2id — p_idx VERSIONNÉ AU CONTENEUR.
# 0 = le plancher 65536 Kio / 3 it. / par. 1 (miroir CF1-CF3, FORMAT_CARTE
# § 3.1) ; 1 et 2 = les paliers de montée (l'agilité).
PARAMS_ARGON2 = ((65536, 3, 1), (262144, 4, 1), (524288, 4, 2))

# (c) le plancher d'entropie de phrase — LA VALEUR GELÉE du plan (≥ 60 bits)
PLANCHER_ENTROPIE = 60.0
DICT_BITS = 11.0          # un mot du dictionnaire ≈ 2^11 candidats fréquents
LEET_BITS = 2.0           # la dé-leétification ajoute ~2 bits de permutations
LONGUEUR_MIN = 12         # sous 12 caractères : refus de longueur NOMMÉ

HKDF_INFO = b"triade-LCF3/v1"
HKDF_INFO_VERIF = b"triade-LCF3/verif/v1"
HKDF_INFO_EMPREINTE = b"triade-LCF3/empreinte/v1"   # (a) la liaison à la clé
SEL_V_PIEGE = b"TRIADE-LCF3-vpiege"                 # (b) sel fixe du domaine
TAG_CTX_PIEGE = b"TRIADE-LCF3-tag-piege"
TAILLE_MOITIE = 32
TAILLE_V_PIEGE = 16
TAILLE_SEL_ARGON = 16
TAILLE_SEL_HKDF = 32
TAILLE_VERIF = 16
TAILLE_EMPREINTE = 32
HEXDIGITS = set("0123456789abcdef")

FIN_AAD = 11 + 2 + 8 + 32 + 16 + 4 + 32 + 32 + 24          # 175
FIN_ENTETE = FIN_AAD + TAILLE_EMPREINTE + TAILLE_VERIF     # 223


class ErreurCoffre(RuntimeError):
    """Tout échec nommé de la serrure de laboratoire — fail-closed."""


class PhraseErronee(ErreurCoffre):
    """L'UNIQUE mode bénin : phrase erronée — réessai, JAMAIS de destruction."""


class ErreurPlancherEntropie(ErreurCoffre):
    """(c) la phrase est SOUS le plancher de 60 bits — cérémonie REFUSÉE."""


# ---------------------------------------------------------------------------
# Utilitaires de laboratoire (miroirs compacts des disciplines du dépôt :
# écriture atomique D119, discipline RAM, date UTC — autoportés, JAMAIS
# importés du dépôt pour ne toucher aucun fichier scellé)
# ---------------------------------------------------------------------------

def _date_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _fsync_repertoire(chemin: str) -> None:
    try:
        fd = os.open(chemin or ".", os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(fd)
    except OSError:
        pass
    finally:
        os.close(fd)


def _ecrire_atomique(chemin: str, donnees: bytes) -> None:
    """Écriture atomique (tmp + fsync + rename + fsync rép.) — miroir D119."""
    rep = os.path.dirname(chemin) or "."
    os.makedirs(rep, exist_ok=True)
    tmp = os.path.join(rep, f".{os.path.basename(chemin)}.{secrets.token_hex(8)}"
                             ".tmp")
    with open(tmp, "wb") as f:
        f.write(donnees)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, chemin)
    _fsync_repertoire(rep)


def _effacer(*buffers) -> None:
    """Discipline RAM : bytearray rempli de zéros, au mieux de Python."""
    for b in buffers:
        if b is None:
            continue
        try:
            b[:] = b"\x00" * len(b)
        except (TypeError, ValueError):
            pass


# ---------------------------------------------------------------------------
# (c) L'ESTIMATION D'ENTROPIE DE PHRASE — dictionnaire + longueur + classes
# ---------------------------------------------------------------------------

# Le dictionnaire intégré des mots courants FR/EN (~430 entrées — les plus
# fréquents des deux langues ; un mot y figurant est compté à DICT_BITS).
DICTIONNAIRE = set("""
le la les un une des du de d et est en que qui dans pour pas sur plus avec
par ce cette ces aux mais ou et donc or ni car comme tout tous toute toutes
être avoir faire dire aller voir savoir pouvoir vouloir venir prendre
trouver donner falloir parler mettre passer devoir croire aimer rester
montrer penser entendre arriver chercher rendre partir retourner devoir
homme femme enfant personnes temps jour an vie monde chose façon cas partie
morte mère père ami maison tête oeil main coeur eau feu terre ciel soleil
mot nom question rien personne jamais toujours souvent parfois maintenant
aujourd'hui demain hier bon bonne beau belle grand grande petit petite gros
grosse long longue court courte haut bas nouveau nouvelle vieux vieille
jeune chaud froid facile difficile vrai faux possible impossible autre même
tel telle bien mal mieux moins aussi assez très trop peu beaucoup
motdepasse mot de passe password passe admin administrator root test teste
compte utilisateur user login secret clef clé coffre porte serrure piege
piège sequestre séquestre azure loup chat chien oiseau arbre fleur
bonjour merci s'il vous plaît oui non peut-être alors ensuite puis enfin
the of and to in is you that it he was for on are with as his they at be
this have from or one had by word but not what all were we when your can
said there use an each which she do how their if will up other about out
many then them these so some her would make like him into time has look
two more write go see number no way could people my than first water been
call who oil its now find long down day did get come made may part
password letmein welcome monkey dragon sunshine princess football baseball
superman batman trustno7 iloveyou whatever qwerty abc123 123456 12345678
password1 admin123 root123 test123 azerty qwerty123 solei soleil lune étoile
correct horse battery staple orange purple silver golden tiger elephant
pineapple computer keyboard university network server neuve neuf
phrase vague labo publique loulou doudou chouchou minou titi toto tata
ete hiver printemps automne lundi mardi mercredi jeudi vendredi samedi
dimanche janvier fevrier mars avril mai juin juillet aout septembre octobre
novembre decembre
""".split())


def _classes_pool(texte: str) -> int:
    """La taille du réservoir de caractères couverte par les classes
    présentes (minuscules 26, majuscules 26, chiffres 10, symboles 33)."""
    pool = 0
    if any(c.islower() for c in texte):
        pool += 26
    if any(c.isupper() for c in texte):
        pool += 26
    if any(c.isdigit() for c in texte):
        pool += 10
    if any(not c.isalnum() for c in texte):
        pool += 33
    return max(pool, 1)


_LEET = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s",
                       "7": "t", "@": "a", "$": "s", "€": "e", "0": "o"})


def estimer_entropie(phrase: bytes) -> float:
    """L'estimation REFUSANTE du plan (c) : dictionnaire des mots courants,
    longueur, classes — en bits. BORNES CONSIGNÉES : dé-leétification
    minimale (0→o, 1→l, 3→e, 4→a, 5→s, 7→t, @→a, $→s) ; PAS de détection
    des motifs clavier, des répétitions, des dates — l'estimation est donc
    OPTIMISTE sur ces familles, le plancher 60 bits garde la marge."""
    if not phrase:
        return 0.0
    texte = phrase.decode("utf-8", errors="replace")
    if len(texte) < LONGUEUR_MIN:
        # refus de longueur — le verdict nommé l'exprime via le plancher
        return float(len(texte))
    import re
    # les séparateurs COUPENT les jetons (espace, tiret, underscore, point,
    # slash, etc. — seuls les alphanumériques et accents lient un jeton) :
    # « PHRASE-TEST » est DEUX mots du dictionnaire, pas un.
    jetons = [t for t in re.split(r"[^A-Za-z0-9À-ÿ]+", texte) if t]
    pool = _classes_pool(texte)
    bits = 0.0
    import re as _re
    for jeton in jetons:
        bas = jeton.lower()
        m = _re.match(r"^([a-zà-ÿ]+)(\d+)$", bas)
        if bas in DICTIONNAIRE:
            bits += DICT_BITS
        elif m and m.group(1) in DICTIONNAIRE:
            # « MotDePasse123 » : le mot du dictionnaire + k chiffres —
            # les k chiffres comptent k×log2(10), jamais la longueur nue
            bits += DICT_BITS + len(m.group(2)) * math.log2(10)
        elif bas.translate(_LEET) in DICTIONNAIRE \
                or bas.translate(_LEET).replace("l", "i", 1) in DICTIONNAIRE:
            bits += DICT_BITS + LEET_BITS          # le leet ajoute ~2 bits
        else:
            bits += len(jeton) * math.log2(max(pool, 2))
    return bits


def verifier_plancher(phrase: bytes) -> float:
    """La porte du plancher (c) : REFUS NOMMÉ sous 60 bits — la valeur
    estimée est TOUJOURS nommée dans le message, jamais simulée."""
    bits = estimer_entropie(phrase)
    if bits < PLANCHER_ENTROPIE:
        raise ErreurPlancherEntropie(
            f"phrase SOUS le plancher d'entropie : {bits:.1f} bits < "
            f"{PLANCHER_ENTROPIE:.0f} bits (la valeur gelée) — cérémonie "
            f"REFUSÉE (dictionnaire/longueur/classes, plan (c))")
    return bits


# ---------------------------------------------------------------------------
# (b) V_piège DÉRIVÉE — liée à S_piège ET à l'époque
# ---------------------------------------------------------------------------

def derive_v_piege(s_piege, epoque: int) -> bytes:
    """V_piège = HKDF-SHA256(ikm = S_piège ; salt = SEL_V_PIEGE ;
    info = « piège » ‖ époque_le64), 16 o — la lettre du plan (b)."""
    return HKDF(algorithm=hashes.SHA256(), length=TAILLE_V_PIEGE,
                salt=SEL_V_PIEGE,
                info=b"piege" + int(epoque).to_bytes(8, "little")
                ).derive(bytes(s_piege))


# ---------------------------------------------------------------------------
# Dérivations (miroir CF3 § 3, adaptées LCF3)
# ---------------------------------------------------------------------------

def cle_utilisateur(phrase: bytes, sel_argon: bytes, p_idx: int) -> bytes:
    if not phrase:
        raise ErreurCoffre("phrase VIDE — refus")
    if len(sel_argon) != TAILLE_SEL_ARGON:
        raise ErreurCoffre(f"sel_argon != {TAILLE_SEL_ARGON} o")
    mem, it, par = PARAMS_ARGON2[p_idx]
    return hash_secret_raw(secret=phrase, salt=sel_argon, time_cost=it,
                           memory_cost=mem, parallelism=par,
                           hash_len=32, type=Type.ID)


def _hkdf(ikm: bytes, sel: bytes, info: bytes, longueur: int = 32) -> bytes:
    return HKDF(algorithm=hashes.SHA256(), length=longueur, salt=sel,
                info=info).derive(ikm)


def derive_kek(k_user, s_serrure, s_piege, sel_hkdf: bytes, epoque: int,
               h_projet: bytes) -> bytes:
    return _hkdf(bytes(k_user) + bytes(s_serrure) + bytes(s_piege), sel_hkdf,
                 HKDF_INFO + b"|" + int(epoque).to_bytes(8, "little")
                 + h_projet)


def derive_verif(k_user, v_piege, sel_hkdf: bytes) -> bytes:
    """verif = sha256(HKDF(K_user ‖ V_piège(époque) ; …))[:16] — V_piège est
    DÉRIVÉE à l'époque courante (b) : l'information de vérification est
    PORTÉE À L'ÉPOQUE."""
    return hashlib.sha256(_hkdf(bytes(k_user) + bytes(v_piege), sel_hkdf,
                                HKDF_INFO_VERIF)).digest()[:TAILLE_VERIF]


def derive_k_emp(k_user, s_piege, sel_hkdf: bytes) -> bytes:
    """(a) K_emp = HKDF(K_user ‖ S_piège ; sel_hkdf ; « …/empreinte/v1 ») —
    la clé qui LIE l'empreinte du chiffretexte à la détention de la phrase
    ET du média : sans elle, l'attaquant ne peut produire une empreinte
    conforme sur un chiffretexte réécrit."""
    return _hkdf(bytes(k_user) + bytes(s_piege), sel_hkdf,
                 HKDF_INFO_EMPREINTE)


def empreinte_liee(k_emp, chiffretexte: bytes) -> bytes:
    """(a) empreinte = HMAC-SHA256(K_emp, chiffretexte) — 32 o."""
    return hmac.new(bytes(k_emp), chiffretexte, hashlib.sha256).digest()


def tag_piege(epoque: int, h_projet: bytes, s_piege) -> bytes:
    """sha256(ctx ‖ époque ‖ H_projet ‖ S_piège)[:8] — intégrité du média
    (PAS un MAC : la corruption nommée, pas l'authenticité)."""
    return hashlib.sha256(TAG_CTX_PIEGE
                          + int(epoque).to_bytes(8, "little") + h_projet
                          + bytes(s_piege)).digest()[:8]


# ---------------------------------------------------------------------------
# Conteneur TRIADE-LCF3
# ---------------------------------------------------------------------------

def _aad(epoque: int, h_projet: bytes, sel_argon: bytes, p_idx: int,
         sel_hkdf: bytes, s_serrure: bytes, nonce: bytes) -> bytes:
    return (MAGIC + FORMAT_VERSION.to_bytes(2, "little")
            + int(epoque).to_bytes(8, "little") + h_projet + sel_argon
            + int(p_idx).to_bytes(4, "little") + sel_hkdf + s_serrure
            + nonce)


def construire_conteneur(clair: bytes, k_user, s_serrure, s_piege,
                         sel_argon: bytes, sel_hkdf: bytes, epoque: int,
                         h_projet: bytes, p_idx: int) -> bytes:
    """Le chemin HONNÊTE : KEK, V_piège DÉRIVÉE (b), verif, empreinte LIÉE
    (a), AEAD — l'ordre d'écriture est le contrat de la sentinelle."""
    kek = bytearray(derive_kek(k_user, s_serrure, s_piege, sel_hkdf, epoque,
                               h_projet))
    k_emp = bytearray(derive_k_emp(k_user, s_piege, sel_hkdf))
    try:
        v_piege = derive_v_piege(s_piege, epoque)      # (b)
        verif = derive_verif(k_user, v_piege, sel_hkdf)
        nonce = secrets.token_bytes(24)
        aad = _aad(epoque, h_projet, sel_argon, p_idx, sel_hkdf,
                   bytes(s_serrure), nonce)
        chiffretexte = crypto_aead_xchacha20poly1305_ietf_encrypt(
            clair, aad, nonce, bytes(kek))
        empreinte = empreinte_liee(k_emp, chiffretexte)  # (a)
        return aad + empreinte + verif + chiffretexte
    finally:
        _effacer(kek, k_emp)


def parser_entete(blob: bytes) -> dict:
    """En-tête clair complet — fail-closed NOMMÉ, p_idx à la liste blanche
    (c)."""
    if len(blob) < FIN_ENTETE:
        raise ErreurCoffre("conteneur trop court (en-tête tronqué)")
    if blob[:11] != MAGIC:
        raise ErreurCoffre(f"magic invalide : {blob[:11]!r} (TRIADE-LCF3 "
                           "attendu — ce n'est pas un conteneur de labo)")
    version = int.from_bytes(blob[11:13], "little")
    if version != FORMAT_VERSION:
        raise ErreurCoffre(f"version conteneur non gérée : {version}")
    epoque = int.from_bytes(blob[13:21], "little")
    if epoque < 1:
        raise ErreurCoffre(f"époque invalide : {epoque} (>= 1 attendu)")
    h_projet = blob[21:53]
    sel_argon = blob[53:69]
    p_idx = int.from_bytes(blob[69:73], "little")
    if p_idx not in range(len(PARAMS_ARGON2)):
        raise ErreurCoffre(f"p_idx {p_idx} HORS LISTE BLANCHE des paramètres "
                           "Argon2id (0.."
                           f"{len(PARAMS_ARGON2) - 1} — plan (c) l'agilité) : "
                           "REFUS NOMMÉ")
    sel_hkdf = blob[73:105]
    s_serrure = blob[105:137]
    nonce = blob[137:161]
    empreinte = blob[FIN_AAD:FIN_AAD + TAILLE_EMPREINTE]
    verif = blob[FIN_AAD + TAILLE_EMPREINTE:FIN_ENTETE]
    return {"version": version, "epoque": epoque, "h_projet": h_projet,
            "sel_argon": sel_argon, "p_idx": p_idx, "sel_hkdf": sel_hkdf,
            "s_serrure": s_serrure, "nonce": nonce, "empreinte": empreinte,
            "verif": verif, "aad": blob[:FIN_AAD],
            "chiffretexte": blob[FIN_ENTETE:], "entete": blob[:FIN_ENTETE],
            "taille": len(blob)}


# ---------------------------------------------------------------------------
# Fichier piège v2 (b) — S_piège + époque ; V_piège DÉRIVÉE, jamais stockée
# ---------------------------------------------------------------------------

def serialiser_piege(epoque: int, h_projet: bytes, s_piege) -> str:
    return (f"{MAGIC_PIEGE}\n"
            f"epoque: {epoque}\n"
            f"projet: {h_projet.hex()}\n"
            f"piege: {bytes(s_piege).hex()}\n"
            f"tag: {tag_piege(epoque, h_projet, s_piege).hex()}\n")


def parser_piege(texte: str) -> dict:
    lignes = [l.strip() for l in texte.splitlines() if l.strip()]
    if not lignes or lignes[0] != MAGIC_PIEGE:
        raise ErreurCoffre(f"magic piège invalide ({MAGIC_PIEGE} attendu)")
    champs = {}
    for l in lignes[1:]:
        if ":" not in l:
            raise ErreurCoffre(f"ligne de piège malformée : {l!r}")
        clef, _, valeur = l.partition(":")
        champs[clef.strip()] = valeur.strip()
    manquants = [c for c in ("epoque", "projet", "piege", "tag")
                 if c not in champs]
    if manquants:
        raise ErreurCoffre(f"champs manquants dans le piège : {manquants}")
    if not champs["epoque"].isdigit() or int(champs["epoque"]) < 1:
        raise ErreurCoffre(f"époque du piège invalide : {champs['epoque']!r}")
    epoque = int(champs["epoque"])
    hexa = {}
    for clef, taille in (("projet", 64), ("piege", 64), ("tag", 16)):
        valeur = champs[clef].lower()
        if len(valeur) != taille or any(c not in HEXDIGITS for c in valeur):
            raise ErreurCoffre(f"champ {clef} du piège : {taille} caractères "
                               f"hex attendus ({champs[clef]!r})")
        hexa[clef] = bytes.fromhex(valeur)
    if hexa["tag"] != tag_piege(epoque, hexa["projet"], hexa["piege"]):
        raise ErreurCoffre("tag du piège INVALIDE — média corrompu ou "
                           "falsifié (spec piège § 4 miroir)")
    return {"epoque": epoque, "projet": hexa["projet"],
            "s_piege": hexa["piege"]}


def _lire_piege(chemin: str) -> dict:
    try:
        with open(chemin, "r", encoding="ascii") as f:
            return parser_piege(f.read())
    except FileNotFoundError:
        raise ErreurCoffre(f"piège ABSENT : {chemin} — déverrouillage "
                           "IMPOSSIBLE : la seconde moitié de la serrure est "
                           "sur le média séparé")
    except (OSError, UnicodeDecodeError) as exc:
        raise ErreurCoffre(f"piège illisible : {chemin} ({exc}) — refus")


# ---------------------------------------------------------------------------
# Journal, miroir d'époque, PV (miroirs compacts CF3 § 7/§ 9)
# ---------------------------------------------------------------------------

def _dir(conteneur_chemin: str) -> str:
    return os.path.dirname(conteneur_chemin) or "."


def chemin_journal(conteneur_chemin: str) -> str:
    return os.path.join(_dir(conteneur_chemin), "journal-lcf3.txt")


def chemin_miroir(conteneur_chemin: str) -> str:
    return os.path.join(_dir(conteneur_chemin), "epoque-lcf3.txt")


def chemin_pv_dir(conteneur_chemin: str) -> str:
    return os.path.join(_dir(conteneur_chemin), "pv-lcf3")


def chemin_piege(piege_dir: str, epoque: int) -> str:
    return os.path.join(piege_dir, f"piege-LCF3-epoque-{epoque}.txt")


def _journal(conteneur_chemin: str, message: str) -> None:
    try:
        chemin = chemin_journal(conteneur_chemin)
        os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
        with open(chemin, "a", encoding="utf-8") as f:
            f.write(f"{_date_utc()} {message}\n")
    except OSError:
        pass


def _ecrire_miroir(conteneur_chemin: str, epoque: int, checksum: str) -> None:
    _ecrire_atomique(chemin_miroir(conteneur_chemin),
                     f"{epoque} {checksum}\n".encode("ascii"))


def _lire_miroir(conteneur_chemin: str):
    chemin = chemin_miroir(conteneur_chemin)
    if not os.path.isfile(chemin):
        return None
    try:
        with open(chemin, "r", encoding="ascii") as f:
            premiere = f.readline().strip()
    except (OSError, UnicodeDecodeError) as exc:
        raise ErreurCoffre(f"miroir d'époque illisible : {chemin} ({exc}) — "
                           "refus")
    parties = premiere.split()
    if not parties or not parties[0].isdigit():
        raise ErreurCoffre(f"miroir d'époque corrompu : {premiere!r} — refus "
                           "(écriture atomique : une panne n'écrit pas ça)")
    return int(parties[0])


def _detruire_fichier(chemin: str) -> None:
    """Trois passes (aléa, 0xFF, 0x00) + truncate + renommage aléatoire +
    unlink (miroir bruler CF2 § 7)."""
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
    _fsync_repertoire(os.path.dirname(chemin))


def destruction_locale(conteneur_chemin: str, raison: str,
                       cibles_extra: list = None) -> str:
    """(a) la DESTRUCTION LOCALE + PV nommé : conteneur + staging ; JAMAIS
    le média du piège, JAMAIS les parts du séquestre ni aucune autre
    création du dossier (la destruction n'est pas un balai)."""
    pv_dir = chemin_pv_dir(conteneur_chemin)
    os.makedirs(pv_dir, exist_ok=True)
    lignes_pv = [
        "PROCÈS-VERBAL DE DESTRUCTION LOCALE — TRIADE-LCF3 (labo "
        "vr9n3s3l7, plan (a))",
        f"date : {_date_utc()}",
        f"raison : {raison}",
        "passes : aléatoire (CSPRNG) puis 0xFF puis 0x00, fsync par passe",
        "",
    ]
    cibles = [conteneur_chemin, conteneur_chemin + ".staging"] \
        + list(cibles_extra or [])
    detruits = 0
    for cible in cibles:
        if os.path.isfile(cible):
            _detruire_fichier(cible)
            detruits += 1
            lignes_pv.append(f"DETRUIT : {cible} (3 passes, tronqué, "
                             "renommé, unlink, fsync rép.)")
    lignes_pv += ["",
                  f"total : {detruits} artefact(s) machine détruit(s)",
                  "le MÉDIA du piège est INTACT (externe — c'est la relève) ; "
                  "les PARTS du séquestre sont INTACTES (le plan (d) : la "
                  "reconstitution à froid demeure la relève)",
                  "AUCUNE phrase écrite — le PV ne contient JAMAIS de secret "
                  "(discipline RAM, miroir spec CF3 § 8)"]
    horodatage = _date_utc().replace(":", "").replace("-", "")
    base_pv = os.path.join(pv_dir, f"pv-destruction-lcf3-{horodatage}")
    chemin_pv = base_pv + ".txt"
    suffixe = 2
    while os.path.exists(chemin_pv):
        chemin_pv = f"{base_pv}-{suffixe}.txt"
        suffixe += 1
    with open(chemin_pv, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes_pv) + "\n")
    os.chmod(chemin_pv, 0o600)
    _journal(conteneur_chemin, f"PORTE : DESTRUCTION LOCALE — {raison} "
              f"(PV {chemin_pv})")
    print(f"[LCF3] DESTRUCTION LOCALE : {detruits} artefact(s) — PV : "
          f"{chemin_pv}")
    return chemin_pv


# ---------------------------------------------------------------------------
# LA SENTINELLE LCF3 — l'ordre EST la loi (le plan (a) : l'étage 5 NOUVEAU)
# ---------------------------------------------------------------------------

def sentinelle_lcf3(blob: bytes, piege_chemin: str, phrase: bytes,
                    conteneur_chemin: str, epoque_attendue=None,
                    miroir: bool = True, consigner: bool = True
                    ) -> tuple[dict, dict]:
    """L'ordre NORMATIF — à TOUT acte qui déverrouille :

    1. piège PRÉSENT — absent : impossible, rien n'est lu, rien ne brûle ;
    2. piège INTÈGRE (tag) — invalide : refus SANS destruction ;
    3. cohérence des champs publics : époque du piège == époque du conteneur
       (PÉRIMÉ — (b) anti-rollback), H_projet, conteneur >= miroir local
       (RETOUR EN ARRIÈRE), témoin hors-bande ;
    4. PHRASE (verif, avec V_piège DÉRIVÉE à l'époque (b)) — diverge :
       PhraseErronee, réessai, JAMAIS de destruction ;
    5. (a) EMPREINTE LIÉE À LA CLÉ, AVANT L'AEAD :
       HMAC(K_emp, ct) == empreinte stockée → étage 6 ;
       diverge ∧ empreinte stockée == sha256(ct) naïf → FALSIFICATION À
       EMPREINTE VALIDE : DESTRUCTION LOCALE + PV ;
       diverge ∧ naïf diverge → CORRUPTION : REFUS NOMMÉ SANS DESTRUCTION,
       le chiffretexte CONSERVÉ ;
    6. AEAD — échec APRÈS 1–5 verts : falsification PROUVÉE → destruction
       LOCALE + PV ; puis l'étiquette H_projet du clair (miroir CF3 § 10).
    """
    entete = parser_entete(blob)

    # 1 — piège présent
    if not piege_chemin or not os.path.isfile(piege_chemin):
        if consigner:
            _journal(conteneur_chemin, "PORTE : déverrouillage IMPOSSIBLE — "
                     "piège ABSENT")
        raise ErreurCoffre("déverrouillage IMPOSSIBLE : le piège est ABSENT — "
                           "branchez le média (sine qua non D120)")

    # 2 — piège intègre
    try:
        piege = _lire_piege(piege_chemin)
    except ErreurCoffre as exc:
        if consigner:
            _journal(conteneur_chemin, f"PORTE : refus — piège illisible ou "
                     f"tag invalide ({exc})")
        raise ErreurCoffre(f"{exc} — refus SANS destruction : le média est "
                           "hors limite de confiance") from exc

    # 3 — cohérence des champs publics (b : l'époque retirée REFUSÉE)
    if piege["epoque"] != entete["epoque"]:
        if consigner:
            _journal(conteneur_chemin, f"PORTE : refus — piège PÉRIMÉ "
                     f"(époque {piege['epoque']} ≠ conteneur "
                     f"{entete['epoque']})")
        raise ErreurCoffre(
            f"piège PÉRIMÉ : époque du piège {piege['epoque']} ≠ époque du "
            f"conteneur {entete['epoque']} — V_piège DÉRIVÉE à l'époque (b) : "
            "l'époque RETIRÉE est REFUSÉE (anti-rollback)")
    if piege["projet"] != entete["h_projet"]:
        raise ErreurCoffre("H_projet du piège divergent — piège d'un AUTRE "
                           "coffre")
    if miroir:
        miroir_epoque = _lire_miroir(conteneur_chemin)
        if miroir_epoque is not None \
                and entete["epoque"] < miroir_epoque:
            if consigner:
                _journal(conteneur_chemin, f"PORTE : refus — RETOUR EN "
                         f"ARRIÈRE (conteneur {entete['epoque']} < miroir "
                         f"{miroir_epoque})")
            raise ErreurCoffre(f"RETOUR EN ARRIÈRE : époque du conteneur "
                               f"({entete['epoque']}) < miroir local "
                               f"({miroir_epoque}) — couple restauré REFUSÉ")
    if epoque_attendue is not None and entete["epoque"] != epoque_attendue:
        raise ErreurCoffre(f"époque du conteneur ({entete['epoque']}) diverge "
                           f"du témoin hors-bande ({epoque_attendue})")

    # 4 — phrase (BÉNIGNE) — verif PORTÉE À L'ÉPOQUE (b)
    k_user = bytearray(cle_utilisateur(phrase, entete["sel_argon"],
                                       entete["p_idx"]))
    try:
        v_piege = derive_v_piege(piege["s_piege"], entete["epoque"])
        if derive_verif(k_user, v_piege, entete["sel_hkdf"]) \
                != entete["verif"]:
            if consigner:
                _journal(conteneur_chemin, "PORTE : phrase ERRONÉE (verif "
                         "divergent) — réessai, JAMAIS de destruction")
            raise PhraseErronee("phrase ERRONÉE (verif divergent, V_piège "
                                "dérivée à l'époque " 
                                f"{entete['epoque']}) — réessayez : une "
                                "phrase erronée ne détruit JAMAIS")

        # 5 — (a) L'EMPREINTE LIÉE À LA CLÉ, AVANT L'AEAD
        k_emp = bytearray(derive_k_emp(k_user, piege["s_piege"],
                                       entete["sel_hkdf"]))
        try:
            hmac_calcule = empreinte_liee(k_emp, entete["chiffretexte"])
            if hmac_calcule != entete["empreinte"]:
                naive = hashlib.sha256(entete["chiffretexte"]).digest()
                if entete["empreinte"] == naive:
                    destruction_locale(
                        conteneur_chemin,
                        "FALSIFICATION À EMPREINTE VALIDE — l'attaquant a "
                        "réécrit le chiffretexte ET son empreinte (cohérence "
                        "NAÏVE sha256 seule) ; l'empreinte LIÉE À LA CLÉ "
                        "(HMAC, plan (a)) réfute la paire : falsification "
                        "PROUVÉE côté machine (phrase vérifiée, piège "
                        "intègre)")
                    raise ErreurCoffre(
                        "FALSIFICATION À EMPREINTE VALIDE — la paire "
                        "(chiffretexte, empreinte) est cohérente sous la "
                        "lecture naïve (sha256 nu) mais PAS sous l'empreinte "
                        "LIÉE À LA CLÉ : destruction LOCALE effectuée (PV "
                        "écrit) ; le média du piège et les parts du "
                        "séquestre sont INTACTS (plan (a))")
                if consigner:
                    _journal(conteneur_chemin,
                             "PORTE : REFUS NOMMÉ — CORRUPTION (empreinte "
                             "liée divergente, naïve divergente) : AUCUNE "
                             "destruction, le chiffretexte est CONSERVÉ pour "
                             "l'analyse")
                raise ErreurCoffre(
                    "CORRUPTION — empreinte du chiffretexte divergente sans "
                    "cohérence naïve : refus NOMMÉ SANS destruction (le "
                    "chiffretexte est CONSERVÉ pour l'analyse ; la "
                    "destruction attend la PREUVE de falsification — plan "
                    "(a))")

            # 6 — l'AEAD (la preuve restante) puis l'étiquette
            kek = bytearray(derive_kek(k_user, entete["s_serrure"],
                                       piege["s_piege"], entete["sel_hkdf"],
                                       entete["epoque"], entete["h_projet"]))
            try:
                clair = crypto_aead_xchacha20poly1305_ietf_decrypt(
                    entete["chiffretexte"], entete["aad"], entete["nonce"],
                    bytes(kek))
            except Exception:
                destruction_locale(
                    conteneur_chemin,
                    "tag AEAD invalide après piège intègre, phrase vérifiée "
                    "et empreinte liée conforme — falsification PROUVÉE "
                    "côté machine (l'étage (a) est passé VERT : l'altération "
                    "vit dans l'en-tête chiffrant)")
                raise ErreurCoffre("tag AEAD invalide — falsification PROUVÉE "
                                   "côté machine : destruction LOCALE "
                                   "effectuée (PV écrit) ; le média et les "
                                   "parts sont INTACTS")
            finally:
                _effacer(kek)
        finally:
            _effacer(k_emp)
        if hashlib.sha256(clair).digest() != entete["h_projet"]:
            destruction_locale(
                conteneur_chemin,
                "l'état déchiffré ne hache pas vers son étiquette H_projet — "
                "substitution PROUVÉE (miroir CF3 § 10)")
            raise ErreurCoffre("état scellé ≠ étiquette H_projet — "
                               "falsification PROUVÉE : destruction LOCALE "
                               "effectuée (PV écrit)")
    finally:
        _effacer(k_user)

    try:
        base = json.loads(clair.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise ErreurCoffre("base JSON illisible après déchiffrement")
    return base, entete


# ---------------------------------------------------------------------------
# La base (MÊME schéma que CF1/CF2/CF3 — rien à traduire)
# ---------------------------------------------------------------------------

def nouvelle_base(description: str = "") -> dict:
    return {"format": 1, "protocole": PROTOCOLE, "cree": _date_utc(),
            "modifie": _date_utc(), "description": description,
            "projets": {}}


def serialiser(base: dict) -> bytes:
    return json.dumps(base, ensure_ascii=False).encode("utf-8")


def empreinte_etat(base: dict) -> tuple[bytes, str]:
    h = hashlib.sha256(serialiser(base)).digest()
    return h, h[:4].hex()


# ---------------------------------------------------------------------------
# INIT / OUVRIR / VÉRIFIER / CLORE (le cycle compact de laboratoire)
# ---------------------------------------------------------------------------

def init(conteneur_chemin: str, piege_dir: str, phrase: bytes,
         description: str = "", p_idx: int = 0) -> dict:
    """L'init : le plancher d'entropie (c) est vérifié AVANT tout scellement,
    les moitiés fraîches, V_piège DÉRIVÉE (b), l'empreinte LIÉE (a)."""
    bits = verifier_plancher(phrase)
    if p_idx not in range(len(PARAMS_ARGON2)):
        raise ErreurCoffre(f"p_idx {p_idx} hors liste blanche (0..2)")
    base = nouvelle_base(description)
    h_projet, checksum = empreinte_etat(base)
    sel_argon = secrets.token_bytes(TAILLE_SEL_ARGON)
    sel_hkdf = secrets.token_bytes(TAILLE_SEL_HKDF)
    s_serrure = secrets.token_bytes(TAILLE_MOITIE)
    s_piege = secrets.token_bytes(TAILLE_MOITIE)
    k_user = bytearray(cle_utilisateur(phrase, sel_argon, p_idx))
    try:
        blob = construire_conteneur(serialiser(base), k_user, s_serrure,
                                    s_piege, sel_argon, sel_hkdf, 1,
                                    h_projet, p_idx)
    finally:
        _effacer(k_user)
    os.makedirs(piege_dir, exist_ok=True)
    _ecrire_atomique(chemin_piege(piege_dir, 1),
                     serialiser_piege(1, h_projet, s_piege).encode("ascii"))
    _ecrire_atomique(conteneur_chemin, blob)
    _ecrire_miroir(conteneur_chemin, 1, checksum)
    _journal(conteneur_chemin, f"INIT : époque 1, p_idx {p_idx}, entropie "
             f"estimée {bits:.1f} bits (plancher {PLANCHER_ENTROPIE:.0f} "
             "vérifié)")
    return {"epoque": 1, "checksum": checksum, "entropie_bits": bits}


def ouvrir(conteneur_chemin: str, piege_dir: str, phrase: bytes,
           epoque_attendue=None, miroir: bool = True) -> dict:
    """La sentinelle complète à l'ouverture — rend le verdict SANS session
    (le laboratoire : la base lue, les clés mortes à la sortie)."""
    with open(conteneur_chemin, "rb") as f:
        blob = f.read()
    epoque_courante = parser_entete(blob)["epoque"]
    base, entete = sentinelle_lcf3(blob, chemin_piege(piege_dir, epoque_courante),
                                   phrase, conteneur_chemin,
                                   epoque_attendue=epoque_attendue,
                                   miroir=miroir)
    _journal(conteneur_chemin, f"OUVERTURE : époque {entete['epoque']} — "
             "verdict VERT (les clés meurent à la sortie)")
    return {"base": base, "entete": entete}


def verifier(conteneur_chemin: str, piege_dir: str, phrase: bytes,
             epoque_attendue=None, miroir: bool = True) -> dict:
    """La vérification à froid : la sentinelle court pareil, SANS session,
    verdict rendu (consigner=False interdit ici : la vérification EST un
    événement)."""
    return ouvrir(conteneur_chemin, piege_dir, phrase,
                  epoque_attendue=epoque_attendue, miroir=miroir)


def fermer(conteneur_chemin: str, piege_dir: str, phrase: bytes,
           base: dict, p_idx: int = None) -> dict:
    """La clôture compacte de laboratoire : phrase RETAPÉE vérifiée contre
    le canonique, moitiés FRAÎCHES, époque + 1, V_piège DÉRIVÉE à la
    nouvelle époque, RE-LECTURE À FROID avant remplacement atomique."""
    with open(conteneur_chemin, "rb") as f:
        blob = f.read()
    entete = parser_entete(blob)
    epoque_n = entete["epoque"]
    piege_ancien = chemin_piege(piege_dir, epoque_n)
    if not os.path.isfile(piege_ancien):
        raise ErreurCoffre(f"clôture IMPOSSIBLE : le piège d'époque "
                           f"{epoque_n} est ABSENT")
    piege_n = _lire_piege(piege_ancien)
    if piege_n["projet"] != entete["h_projet"]:
        raise ErreurCoffre("H_projet du piège divergent — autre coffre")
    p_idx = entete["p_idx"] if p_idx is None else p_idx
    if p_idx not in range(len(PARAMS_ARGON2)):
        raise ErreurCoffre(f"p_idx {p_idx} hors liste blanche — REFUS NOMMÉ")
    k_user = bytearray(cle_utilisateur(phrase, entete["sel_argon"],
                                       entete["p_idx"]))
    try:
        v_piege_n = derive_v_piege(piege_n["s_piege"], epoque_n)
        if derive_verif(k_user, v_piege_n, entete["sel_hkdf"]) \
                != entete["verif"]:
            raise PhraseErronee("phrase ERRONÉE à la CLOTURE — aucun "
                                "scellement : réessayez (jamais de "
                                "destruction)")
        # le contenu modifié (ou identique) de la session :
        clair = serialiser(base)
        h_final = hashlib.sha256(clair).digest()
        checksum = h_final[:4].hex()
        s_serrure2 = secrets.token_bytes(TAILLE_MOITIE)
        s_piege2 = secrets.token_bytes(TAILLE_MOITIE)
        sel_hkdf2 = secrets.token_bytes(TAILLE_SEL_HKDF)
        epoque2 = epoque_n + 1
        # K_user aux NOUVEAUX paramètres si la clôture change p_idx (c)
        k_user2 = bytearray(cle_utilisateur(phrase, entete["sel_argon"], p_idx))
        try:
            blob2 = construire_conteneur(clair, k_user2, s_serrure2, s_piege2,
                                         entete["sel_argon"], sel_hkdf2,
                                         epoque2, h_final, p_idx)
        finally:
            _effacer(k_user2)
        # piège d'abord (le créneau N+1 est le FUTUR), puis staging…
        piege2_chemin = chemin_piege(piege_dir, epoque2)
        _ecrire_atomique(piege2_chemin,
                         serialiser_piege(epoque2, h_final,
                                          s_piege2).encode("ascii"))
        staging = conteneur_chemin + ".staging"
        _ecrire_atomique(staging, blob2)
        # RE-LECTURE À FROID du staging AVANT le remplacement atomique
        base2, _ = sentinelle_lcf3(blob2, piege2_chemin, phrase, staging,
                                   miroir=False, consigner=False)
        if empreinte_etat(base2)[1] != checksum:
            raise ErreurCoffre("re-lecture à froid : checksum divergent — "
                               "le staging n'est PAS un conteneur prouvé")
        os.replace(staging, conteneur_chemin)
        _fsync_repertoire(_dir(conteneur_chemin))
        _ecrire_miroir(conteneur_chemin, epoque2, checksum)
        _journal(conteneur_chemin, f"CLOTURE : époque {epoque_n} -> "
                 f"{epoque2} (p_idx {entete['p_idx']} -> {p_idx}), "
                 f"checksum {checksum} — re-lecture à froid VERTE")
        return {"epoque": epoque2, "checksum": checksum,
                "piege": piege2_chemin}
    finally:
        _effacer(k_user)


# ---------------------------------------------------------------------------
# (c) LA CÉRÉMONIE DE RE-PARAMÉTRAGE ARGON2 (l'agilité)
# ---------------------------------------------------------------------------

def ceremonie_reparametrage(conteneur_chemin: str, piege_dir: str,
                            phrase: bytes, p_idx_nouveau: int) -> dict:
    """La cérémonie (c) en cinq actes : (1) l'ancien conteneur vérifié VERT
    (les anciens paramètres honorés jusqu'au bout), (2) le plancher
    d'entropie re-vérifié, (3) p_idx neuf à la liste blanche, (4) le
    conteneur ré-écrit à époque+1 avec les paramètres neufs (K_user
    RECALCULÉ : l'agilité brise l'invariance de K_user — la SEULE cérémonie
    qui le fait, NOMMÉ), (5) re-lecture à froid avant remplacement. Le PV
    de cérémonie est écrit à côté du conteneur."""
    res = verifier(conteneur_chemin, piege_dir, phrase)
    entete = res["entete"]
    if p_idx_nouveau not in range(len(PARAMS_ARGON2)):
        raise ErreurCoffre(f"p_idx neuf {p_idx_nouveau} HORS LISTE BLANCHE — "
                           "cérémonie REFUSÉE (plan (c))")
    bits = verifier_plancher(phrase)
    base = res["base"]
    base["modifie"] = _date_utc()
    res2 = fermer(conteneur_chemin, piege_dir, phrase, base,
                  p_idx=p_idx_nouveau)
    pv_dir = chemin_pv_dir(conteneur_chemin)
    os.makedirs(pv_dir, exist_ok=True)
    anciens = PARAMS_ARGON2[entete["p_idx"]]
    nouveaux = PARAMS_ARGON2[p_idx_nouveau]
    pv = os.path.join(pv_dir, f"pv-reparametrage-{res2['epoque']}.txt")
    with open(pv, "w", encoding="utf-8") as f:
        f.write("\n".join([
            "PROCÈS-VERBAL DE CÉRÉMONIE DE RE-PARAMÉTRAGE ARGON2 — LCF3 "
            "(plan (c), l'agilité)",
            f"date : {_date_utc()}",
            f"époque : {entete['epoque']} -> {res2['epoque']}",
            f"paramètres anciens (p_idx {entete['p_idx']}) : Argon2id("
            f"{anciens[0]} Kio, {anciens[1]} it., {anciens[2]} par.)",
            f"paramètres neufs (p_idx {p_idx_nouveau}) : Argon2id("
            f"{nouveaux[0]} Kio, {nouveaux[1]} it., {nouveaux[2]} par.)",
            f"plancher d'entropie vérifié : {bits:.1f} bits >= "
            f"{PLANCHER_ENTROPIE:.0f}",
            "K_user RECALCULÉ aux paramètres neufs (l'invariance brisée par "
            "la seule cérémonie d'agilité — NOMMÉ)",
            f"re-lecture à froid : VERTE (checksum {res2['checksum']})",
            "AUCUN secret écrit — le PV ne contient que des valeurs "
            "publiques.",
        ]) + "\n")
    os.chmod(pv, 0o600)
    _journal(conteneur_chemin, f"CÉRÉMONIE (c) re-paramétrage : p_idx "
             f"{entete['p_idx']} -> {p_idx_nouveau}, PV {pv}")
    return {"epoque": res2["epoque"], "p_idx": p_idx_nouveau, "pv": pv,
            "entropie_bits": bits, "checksum": res2["checksum"]}
