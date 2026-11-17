#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""memo_sessions.py — LE MÉMO SCELLÉ DES SESSIONS D'ÉMULATION PURES
(l'instruction vljfs6pcj, levier (b) : « mémoïsation scellée des sessions
d'émulation pures (clé = empreinte du bloc + entrée ; le cache est un
artifact vérifié et signé, jamais un état partagé entre juge et jugé) »).

LE FORMAT (gelé au PLAN-vljfs6pcj-M4.md § 3) :

  cle_i = sha256( sha256(octets_du_bloc) ‖ sha256(contenu_de_l'entrée) ‖
                  sha256(octets_du_contrat) ‖ identifiant_oracle )
  valeur = {rax, etat_propre, cadre_hex (960 o), panneau_hex (48 o),
            pos (la position de lecture à la fin de la session vivante),
            secondes (le coût vivant au semis — le prix évité, consigné)}
  chaîne : h_0 = sha256(GENÈSE ‖ cle_0 ‖ sérialisé(valeur_0))
           h_i = sha256(h_{i-1} ‖ cle_i ‖ sérialisé(valeur_i))
  racine = h_n, SIGNÉE Ed25519 par la clé de TEST du laboratoire
  (la discipline du sceau-I spec § 8 : dérivée d'une CONSTANTE PUBLIQUE —
  sa non-sécurité EST la preuve visible de l'état laboratoire ; la clé
  RÉELLE du développeur n'apparaît jamais ici).

LE MÉMO N'EST JAMAIS CRU : à chaque chargement la chaîne ENTIÈRE est
recalculée et la signature VÉRIFIÉE — tout écart = MemoRefus (fail-closed).
Le mémo n'est PAS un état partagé : chaque outil garde SA propre émulation
vivante ; le mémo est un RELEVÉ signé, réduit par clé et JUGÉ à chaque
usage (le différentiel contre le modèle indépendant reste à la charge de
l'oracle appelant).
"""
from __future__ import annotations

import hashlib
import json
import os
import time

CONSTANTE_CLE_TEST = b"TRIADE-MEMO-SESSIONS-TEST-2026-v1"   # publique (spec § 8)
GENESE = b"TRIADE-MEMO-V1"
FORMAT = "TRIADE-MEMO-V1"


class MemoRefus(Exception):
    """Le mémo vérifié a échoué — refus nommé, fail-closed (jamais cru)."""


# --- la clé (levier (a) : l'invalidation par empreinte) ------------------------

def cle_session(bloc: bytes, entree: bytes, contrat: bytes,
                oracle_id: str) -> str:
    """La clé d'une session pure : TOUT terme qui détermine le résultat —
    le bloc (les octets assemblés qui courent), l'entrée (le contenu soumis),
    le contrat (la couche I qui porte les vecteurs), l'oracle (l'outil).
    Un seul octet changé dans un seul terme → clé différente → ABSENCE →
    la session est rejouée en entier (l'invalidation est par construction)."""
    return hashlib.sha256(
        hashlib.sha256(bloc).digest()
        + hashlib.sha256(entree).digest()
        + hashlib.sha256(contrat).digest()
        + oracle_id.encode("utf-8")).hexdigest()


# --- la clé de test Ed25519 (publique, déterministe — spec § 8) ----------------

def _cle_test():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import \
        Ed25519PrivateKey
    privee = Ed25519PrivateKey.from_private_bytes(
        hashlib.sha256(CONSTANTE_CLE_TEST).digest())
    return privee


def cle_publique_test_hex() -> str:
    from cryptography.hazmat.primitives.serialization import \
        Encoding, PublicFormat
    return _cle_test().public_key().public_bytes(
        Encoding.Raw, PublicFormat.Raw).hex()


# --- la sérialisation canonique (le hachage ne dépend pas de l'ordre des clés) --

def _ser(valeur: dict) -> bytes:
    return json.dumps(valeur, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def _h(precedent: bytes, cle: str, valeur: dict) -> str:
    return hashlib.sha256(
        precedent + bytes.fromhex(cle) + _ser(valeur)).hexdigest()


# --- le mémo -------------------------------------------------------------------

class MemoSessions:
    """Le relevé scellé. charger() vérifie TOUT ; deposer() accumulate ;
    sceller() recalcule la chaîne entière et signe (l'écriture est
    single-writer : l'oracle parent, jamais les travailleurs)."""

    def __init__(self):
        self.entrees: list[dict] = []      # [{cle, valeur, h}] dans l'ordre
        self.index: dict[str, dict] = {}
        self._a_deposer: list[tuple[str, dict]] = []

    # -- chargement vérifié (fail-closed) --
    @classmethod
    def charger(cls, chemin: str) -> "MemoSessions":
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import \
            Ed25519PublicKey
        if not os.path.exists(chemin):
            raise MemoRefus(f"MÉMO-ABSENT : {chemin}")
        with open(chemin, encoding="utf-8") as f:
            doc = json.load(f)
        if doc.get("format") != FORMAT:
            raise MemoRefus(f"FORMAT-INCONNU : {doc.get('format')!r}")
        if doc.get("constante") != CONSTANTE_CLE_TEST.hex():
            raise MemoRefus("CONSTANTE-DIVERGENTE : la clé de test n'est pas "
                            "celle du format")
        entrees = doc.get("entrees", [])
        precedent = hashlib.sha256(GENESE).digest()
        vus = set()
        for e in entrees:
            cle, valeur, h = e["cle"], e["valeur"], e["h"]
            if cle in vus:
                raise MemoRefus(f"CLÉ-DUPLIQUÉE : {cle[:16]}…")
            vus.add(cle)
            attendu = _h(precedent, cle, valeur)
            if attendu != h:
                raise MemoRefus(
                    f"CHAÎNE-ROMPUE à l'entrée {cle[:16]}… : "
                    f"h attendu {attendu[:16]}…, lu {h[:16]}…")
            precedent = bytes.fromhex(attendu)
        if doc.get("racine") != precedent.hex():
            raise MemoRefus("RACINE-DIVERGENTE : la chaîne ne ferme pas "
                            "sur la racine déclarée")
        # la signature : sur le cœur de l'en-tête
        coeur = (doc["format"].encode()
                 + bytes.fromhex(doc["constante"])
                 + bytes.fromhex(doc["publique"])
                 + precedent + str(len(entrees)).encode())
        try:
            Ed25519PublicKey.from_public_bytes(
                bytes.fromhex(doc["publique"])).verify(
                bytes.fromhex(doc["signature"]), coeur)
        except InvalidSignature:
            raise MemoRefus("SIGNATURE-INVALIDE : le mémo n'est pas scellé "
                            "par la clé de test du format")
        m = cls()
        m.entrees = entrees
        m.index = {e["cle"]: e["valeur"] for e in entrees}
        return m

    # -- consultation (la clé fait toute la validation) --
    def consulter(self, cle: str) -> dict | None:
        return self.index.get(cle)

    # -- dépôt (single-writer : le parent) --
    def deposer(self, cle: str, valeur: dict) -> None:
        if cle not in self.index:
            self._a_deposer.append((cle, valeur))

    def sceller(self, chemin: str) -> dict:
        """Recalcule la chaîne ENTIÈRE (chargées + nouvelles, l'ordre
        d'insertion), signe la racine, écrit — et recharge vérifiée."""
        entrees = [dict(e) for e in self.entrees]
        index = {e["cle"]: e for e in entrees}
        for cle, valeur in self._a_deposer:
            if cle in index:
                continue                     # jamais deux fois la même clé
            entrees.append({"cle": cle, "valeur": valeur, "h": ""})
            index[cle] = entrees[-1]
        precedent = hashlib.sha256(GENESE).digest()
        for e in entrees:
            e["h"] = _h(precedent, e["cle"], e["valeur"])
            precedent = bytes.fromhex(e["h"])
        privee = _cle_test()
        publique = cle_publique_test_hex()
        coeur = (FORMAT.encode()
                 + bytes.fromhex(CONSTANTE_CLE_TEST.hex())
                 + bytes.fromhex(publique)
                 + precedent + str(len(entrees)).encode())
        signature = privee.sign(coeur).hex()
        doc = {"format": FORMAT,
               "constante": CONSTANTE_CLE_TEST.hex(),
               "publique": publique,
               "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "racine": precedent.hex(),
               "signature": signature,
               "entrees": entrees}
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        # recharge vérifiée immédiate (le sceau n'est cru qu'une fois prouvé)
        recharge = MemoSessions.charger(chemin)
        self.entrees = recharge.entrees
        self.index = recharge.index
        self._a_deposer = []
        return {"n": len(entrees), "racine": precedent.hex(),
                "signature": signature}


# --- l'ouverture au mémo : le chemin (a)+(b)+(c) partagé par les oracles --------

SEUIL_KIO = 64          # gelé au plan : seules les sessions ≥ 64 Kio (le
                        # chemin critique mesuré) passent par le mémo


def session_memorisable(contenu: bytes) -> bool:
    return len(contenu) >= SEUIL_KIO * 1024


def ouvrir_memorise(emul, os_v, memo, bloc: bytes, entree: bytes,
                    contrat: bytes, oracle_id: str, chemin: str,
                    ouvrir_vivant) -> tuple[dict, bool, list]:
    """L'ouverture de session AU MÉMO — LE MÊME JUGE PARTOUT :

    - la clé est calculée (le bloc assemblé, l'entrée, le contrat, l'oracle) ;
    - PRÉSENCE (clé vivante au mémo vérifié) : le RELEVÉ est rendu —
      l'oracle appelant mène SES contrôles dessus (le différentiel contre
      le modèle indépendant reste intégral) et reconstruit l'état vivant
      s'il doit poursuivre (reconstruire_session) ;
    - ABSENCE : la session vivante court (l'original INTACT — le repli EST
      l'émulation complète, jamais l'échec muet), son état est RELEVÉ puis
      déposé au mémo (le semis).

    Retourne (releve, memo_hit, depots) où releve = {rax, etat_propre,
    cadre (960 o), panneau (48 o), pos, secondes} et depots = [(cle,
    valeur)] le relevé nouveau (vide au relevé jugé). Le mémo RELÈVE, il
    ne juge pas : chaque contrôle demeure à l'oracle, sur le relevé ou
    sur le vivant — les mêmes textes, les mêmes verdicts attendus."""
    cle = cle_session(bloc, entree, contrat, oracle_id)
    hit = memo.consulter(cle) if memo is not None else None
    if hit is not None:
        return {"rax": hit["rax"], "etat_propre": hit["etat_propre"],
                "cadre": bytes.fromhex(hit["cadre_hex"]),
                "panneau": bytes.fromhex(hit["panneau_hex"]),
                "pos": hit["pos"],
                "secondes": hit.get("secondes", 0.0)}, True, []
    # ---- la session vivante (l'original INTACT) + le relevé ----
    import time as _t
    t0 = _t.monotonic()
    r = ouvrir_vivant(emul, os_v, chemin)
    dt = _t.monotonic() - t0
    cadre = emul.cadre()
    panneau = emul.panneau()
    poignee = emul.u64(528)
    pos = os_v.poignees.get(poignee, (chemin, 0))[1]
    releve = {"rax": r["rax"], "etat_propre": emul.etat_propre(r),
              "cadre": cadre, "panneau": panneau,
              "pos": pos, "secondes": round(dt, 3)}
    depots: list = []
    if memo is not None:
        valeur = {"rax": releve["rax"], "etat_propre": releve["etat_propre"],
                  "cadre_hex": cadre.hex(), "panneau_hex": panneau.hex(),
                  "pos": pos, "secondes": round(dt, 3)}
        memo.deposer(cle, valeur)
        depots = [(cle, valeur)]
    return releve, False, depots


def reconstruire_session(emul, os_v, chemin: str, releve: dict) -> int:
    """La reconstruction de l'état né : le cadre et le panneau RELEVÉS
    posés à leurs adresses, la poignée rendue à l'OS virtuel (le shim
    SetFilePointerEx la CHERCHE — sans elle la lecture vivante qui suit
    échouerait faussement). Retourne la poignée. Après ceci, l'émulation
    est VIVANTE : les lectures du bloc sous test courent réellement."""
    import struct
    import harnais_noyau as HN
    emul.uc.mem_write(HN.L.R_CADRE, releve["cadre"])
    emul.uc.mem_write(HN.L.R_EMPREINTES, releve["panneau"])
    poignee = struct.unpack("<Q", releve["cadre"][528:536])[0]
    os_v.poignees[poignee] = (chemin, releve["pos"])
    return poignee
