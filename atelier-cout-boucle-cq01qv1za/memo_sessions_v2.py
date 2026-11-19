#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""memo_sessions_v2.py — LE MÉMO SCELLÉ V2 DES SESSIONS D'ÉMULATION PURES
(l'instruction cq01qv1za, axe (2) : « Mémoïsation déterministe des ouvertures
de session émulées (clé = sha256 fichier + config émulateur + graine), avec
re-exécution d'audit périodique (1 run sur 10) et preuve d'identité des
consoles ligne à ligne »).

LA CLÉ V2 — le SUR-ENSEMBLE de la v1 (tout ce qui détermine le résultat :
le bloc, l'entrée, le contrat, l'oracle) PLUS les deux termes de
l'environnement de mesure que l'instruction ajoute (la CONFIG ÉMULATEUR,
la GRAINE de campagne) :

  cle_v2 = sha256( sha256(octets_assemblés_du_bloc)
                ‖ sha256(contenu_de_l'entrée)
                ‖ sha256(octets_du_contrat)
                ‖ sha256(config_émulateur_sérialisée)
                ‖ graine
                ‖ identifiant_oracle )

Un octet changé d'UN SEUL terme = clé différente = ABSENCE = la session
vit (l'invalidation par construction — la v1 reconduite, étendue).

LE FORMAT V2 : la discipline de chaîne et de signature v1 (chaque entrée
porte son h, chaînée depuis la genèse TRIADE-MEMO-V2, racine signée Ed25519
par la clé de test publique, TOUT recalculé à chaque chargement, tout
écart = REFUS nommé, fail-closed) PLUS : config_hash et graine à l'en-tête,
ET LE COMPTEUR DE RUNS — l'audit 1 run sur 10 : le compteur vit DANS LE
CŒUR SIGNÉ (toute mutation du compteur = SIGNATURE-INVALIDE) ; l'oracle
dont le scellement portera le compteur à un multiple de 10 COURT EN MODE
AUDIT (la re-exécution vivante, la preuve d'identité champ à champ et
console ligne à ligne).

Les entrées v1 (memo-sessions-v1.json) NE SONT PAS migrées : le v2 naît
vide, semé par ses propres exécutions — l'ancien demeure, PÉRIMÉ POUR LE
V2, jamais détruit (D143)."""
from __future__ import annotations

import hashlib
import json
import os
import time

CONSTANTE_CLE_TEST = b"TRIADE-MEMO-SESSIONS-TEST-2026-v2"   # publique (spec § 8)
GENESE = b"TRIADE-MEMO-V2"
FORMAT = "TRIADE-MEMO-V2"
PERIODE_AUDIT = 10          # 1 run sur 10 — l'instruction, sa lettre


class MemoRefus(Exception):
    """Le mémo vérifié a échoué — refus nommé, fail-closed (jamais cru)."""


# --- la clé v2 (l'instruction : fichier + config émulateur + graine ;
#     la v1 entière demeure — le sur-ensemble) ------------------------------

def cle_session_v2(bloc: bytes, entree: bytes, contrat: bytes,
                   config: dict, graine: int, oracle_id: str) -> str:
    config_ser = json.dumps(config, sort_keys=True,
                            separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(
        hashlib.sha256(bloc).digest()
        + hashlib.sha256(entree).digest()
        + hashlib.sha256(contrat).digest()
        + hashlib.sha256(config_ser).digest()
        + str(graine).encode("ascii")
        + oracle_id.encode("utf-8")).hexdigest()


def config_emulateur(moteur: str, heritages: dict[str, str],
                     zones: list, echecs_armes=None) -> dict:
    """LA CONFIG SÉRIALISÉE de la clé : le moteur (unicorn|qemu), les
    empreintes des héritages scellés posés à l'émulation, la carte des
    zones du plan, l'état des échecs armés — tout ce qui, SANS changer le
    bloc ni l'entrée, changerait le déroulement."""
    return {"moteur": moteur,
            "heritages": dict(sorted(heritages.items())),
            "zones": [list(z) for z in zones],
            "echecs_armes": echecs_armes}


# --- la clé de test Ed25519 (publique, déterministe — spec § 8) ------------

def _cle_test():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import \
        Ed25519PrivateKey
    return Ed25519PrivateKey.from_private_bytes(
        hashlib.sha256(CONSTANTE_CLE_TEST).digest())


def cle_publique_test_hex() -> str:
    from cryptography.hazmat.primitives.serialization import \
        Encoding, PublicFormat
    return _cle_test().public_key().public_bytes(
        Encoding.Raw, PublicFormat.Raw).hex()


# --- la sérialisation canonique ------------------------------------------------

def _ser(valeur: dict) -> bytes:
    return json.dumps(valeur, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def _h(precedent: bytes, cle: str, valeur: dict) -> str:
    return hashlib.sha256(
        precedent + bytes.fromhex(cle) + _ser(valeur)).hexdigest()


# --- le mémo v2 ----------------------------------------------------------------

class MemoSessionsV2:
    """Le relevé scellé v2 : charger() vérifie TOUT (chaîne, signature,
    compteur) ; deposer() accumule ; sceller() recalcule, signe, INCRÉMENTE
    LE COMPTEUR DE RUNS (chaque scellement d'oracle = un run) et rend
    l'état d'audit : ce scellement est-il un multiple de la période ?"""

    def __init__(self):
        self.entrees: list[dict] = []
        self.index: dict[str, dict] = {}
        self._a_deposer: list[tuple[str, dict]] = []
        self.compteur_runs = 0
        self.config_hash = ""
        self.graine = None

    # -- le cœur signé (le compteur vit dedans : le muter = signature rompue) --
    @staticmethod
    def _coeur(publique_hex: str, racine_hex: str, compteur: int,
               n_entrees: int, config_hash: str, graine) -> bytes:
        return (FORMAT.encode()
                + bytes.fromhex(CONSTANTE_CLE_TEST.hex())
                + bytes.fromhex(publique_hex)
                + bytes.fromhex(racine_hex)
                + str(compteur).encode()
                + str(n_entrees).encode()
                + config_hash.encode()
                + str(graine).encode())

    # -- chargement vérifié (fail-closed) --
    @classmethod
    def charger(cls, chemin: str) -> "MemoSessionsV2":
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
                            "celle du format v2")
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
        coeur = cls._coeur(doc["publique"], precedent.hex(),
                           int(doc.get("compteur_runs", 0)), len(entrees),
                           doc.get("config_hash", ""),
                           doc.get("graine"))
        try:
            Ed25519PublicKey.from_public_bytes(
                bytes.fromhex(doc["publique"])).verify(
                bytes.fromhex(doc["signature"]), coeur)
        except InvalidSignature:
            raise MemoRefus("SIGNATURE-INVALIDE : le mémo n'est pas scellé "
                            "par la clé de test du format v2 — le compteur "
                            "d'audit ou l'en-tête fut muté")
        m = cls()
        m.entrees = entrees
        m.index = {e["cle"]: e["valeur"] for e in entrees}
        m.compteur_runs = int(doc.get("compteur_runs", 0))
        m.config_hash = doc.get("config_hash", "")
        m.graine = doc.get("graine")
        return m

    # -- consultation --
    def consulter(self, cle: str) -> dict | None:
        return self.index.get(cle)

    # -- dépôt (single-writer : le parent) --
    def deposer(self, cle: str, valeur: dict) -> None:
        if cle not in self.index:
            self._a_deposer.append((cle, valeur))

    def sceller(self, chemin: str, config: dict | None = None,
                graine=None) -> dict:
        """Recalcule la chaîne ENTIÈRE, signe (le compteur DANS le cœur),
        INCRÉMENTE le compteur de runs, écrit — et recharge vérifiée.
        Retourne {n, racine, signature, compteur_runs, audit_du: bool} :
        audit_du = CE scellement porte le compteur à un multiple de la
        période — l'oracle qui scelle SAIT qu'il vient de courir l'audit
        (ou doit le courir : le protocole l'exige au 10ᵉ, pas après)."""
        entrees = [dict(e) for e in self.entrees]
        index = {e["cle"]: e for e in entrees}
        for cle, valeur in self._a_deposer:
            if cle in index:
                continue
            entrees.append({"cle": cle, "valeur": valeur, "h": ""})
            index[cle] = entrees[-1]
        precedent = hashlib.sha256(GENESE).digest()
        for e in entrees:
            e["h"] = _h(precedent, e["cle"], e["valeur"])
            precedent = bytes.fromhex(e["h"])
        if config is not None:
            self.config_hash = hashlib.sha256(json.dumps(
                config, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")).hexdigest()
        if graine is not None:
            self.graine = graine
        compteur_avant = self.compteur_runs
        self.compteur_runs += 1          # UN SCELLEMENT D'ORACLE = UN RUN
        privee = _cle_test()
        publique = cle_publique_test_hex()
        coeur = self._coeur(publique, precedent.hex(), self.compteur_runs,
                            len(entrees), self.config_hash, self.graine)
        signature = privee.sign(coeur).hex()
        doc = {"format": FORMAT,
               "constante": CONSTANTE_CLE_TEST.hex(),
               "publique": publique,
               "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "config_hash": self.config_hash,
               "graine": self.graine,
               "compteur_runs": self.compteur_runs,
               "racine": precedent.hex(),
               "signature": signature,
               "entrees": entrees}
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        recharge = MemoSessionsV2.charger(chemin)
        self.entrees = recharge.entrees
        self.index = recharge.index
        self._a_deposer = []
        return {"n": len(entrees), "racine": precedent.hex(),
                "signature": signature,
                "compteur_runs": self.compteur_runs,
                "audit_du": self.compteur_runs % PERIODE_AUDIT == 0,
                "audit_prochain": PERIODE_AUDIT - (
                    self.compteur_runs % PERIODE_AUDIT)}


# --- l'ouverture au mémo v2 : le chemin partagé par les oracles v182 ----------

SEUIL_KIO = 64          # gelé au plan v181 : les sessions ≥ 64 Kio seules


def session_memorisable(contenu: bytes) -> bool:
    return len(contenu) >= SEUIL_KIO * 1024


def ouvrir_memorise_v2(memo, bloc: bytes, entree: bytes, contrat: bytes,
                       config: dict, graine: int, oracle_id: str,
                       executer_vivant, consulter=None):
    """L'ouverture de session AU MÉMO V2 — LE MÊME JUGE PARTOUT :

    - la clé v2 (le bloc, l'entrée, le contrat, la config, la graine,
      l'oracle) ;
    - PRÉSENCE : le RELEVÉ rendu — l'oracle appelant mène SES contrôles ;
    - ABSENCE : la session vivante court PAR LE MOTEUR DE VOLUME
      (executer_vivant — la fonction de l'oracle, QEMU au régime,
      Unicorn à l'audit), son état RELEVÉ puis déposé (le semis).

    Retourne (releve, memo_hit, depots) où releve = {rax, etat_propre,
    cadre (960 o), panneau (48 o), pos, secondes}."""
    cle = cle_session_v2(bloc, entree, contrat, config, graine, oracle_id)
    hit = memo.consulter(cle) if memo is not None else None
    if hit is not None:
        return {"rax": hit["rax"], "etat_propre": hit["etat_propre"],
                "cadre": bytes.fromhex(hit["cadre_hex"]),
                "panneau": bytes.fromhex(hit["panneau_hex"]),
                "pos": hit["pos"],
                "secondes": hit.get("secondes", 0.0)}, True, []
    import time as _t
    t0 = _t.monotonic()
    r = executer_vivant()
    dt = _t.monotonic() - t0
    releve = {"rax": r["rax"], "etat_propre": r["etat_propre"],
              "cadre": r["cadre"], "panneau": r["panneau"],
              "pos": r["pos"], "secondes": round(dt, 3)}
    depots: list = []
    if memo is not None:
        valeur = {"rax": releve["rax"],
                  "etat_propre": releve["etat_propre"],
                  "cadre_hex": releve["cadre"].hex(),
                  "panneau_hex": releve["panneau"].hex(),
                  "pos": releve["pos"], "secondes": round(dt, 3)}
        memo.deposer(cle, valeur)
        depots = [(cle, valeur)]
    return releve, False, depots


def audit_memorise(memo, bloc: bytes, entree: bytes, contrat: bytes,
                   config: dict, graine: int, oracle_id: str,
                   executer_vivant):
    """LE CHEMIN D'AUDIT (le plan § 2.3) — DIFFÉRENT du régime en TOUT :

    - la session court TOUJOURS VIVANTE (executer_vivant — l'Unicorn de
      référence chez les oracles), JAMAIS servie du mémo ;
    - le relevé vivant confronté AU RELEVÉ MÉMOISÉ champ à champ (la
      preuve d'identité — comparaison_audit) ;
    - à l'absence au mémo : le relevé vivant déposé (le semis d'audit).

    Retourne (releve, memo_existant, depots, ecarts)."""
    cle = cle_session_v2(bloc, entree, contrat, config, graine, oracle_id)
    valeur = memo.consulter(cle) if memo is not None else None
    releve = executer_vivant()
    ecarts: list = []
    depots: list = []
    if valeur is not None:
        ecarts = comparaison_audit(
            releve, {"rax": valeur["rax"],
                     "etat_propre": valeur["etat_propre"],
                     "cadre": valeur["cadre_hex"],      # la forme hex du
                     "panneau": valeur["panneau_hex"],  # dépôt — la comparaison
                     "pos": valeur["pos"]})             # convertit des deux bords
    elif memo is not None:
        v = {"rax": releve["rax"], "etat_propre": releve["etat_propre"],
             "cadre_hex": releve["cadre"].hex(),
             "panneau_hex": releve["panneau"].hex(),
             "pos": releve["pos"], "secondes": releve["secondes"]}
        memo.deposer(cle, v)
        depots = [(cle, v)]
    return releve, valeur is not None, depots, ecarts


def comparaison_audit(releve_vivant: dict, releve_memo: dict) -> list[str]:
    """LA PREUVE D'IDENTITÉ CHAMP À CHAMP de l'audit (le plan § 2.3) : le
    relevé de la re-exécution vivante confronté au relevé mémoisé — TOUT
    écart nommé, bloquant."""
    ecarts = []
    for champ in ("rax", "etat_propre", "pos"):
        if releve_vivant[champ] != releve_memo[champ]:
            ecarts.append(f"{champ} : vivant {releve_vivant[champ]!r} != "
                          f"mémo {releve_memo[champ]!r}")
    for champ, taille in (("cadre", 960), ("panneau", 48)):
        v = releve_vivant[champ]
        m = releve_memo[champ]
        vb = v if isinstance(v, bytes) else bytes.fromhex(v)
        mb = m if isinstance(m, bytes) else bytes.fromhex(m)
        if vb != mb:
            premier = next((i for i in range(taille) if vb[i] != mb[i]),
                           None)
            ecarts.append(f"{champ} : l'octet {premier} diverge")
    return ecarts


def reconstruire_session(emul, os_v, chemin: str, releve: dict) -> int:
    """La reconstruction de l'état né (la discipline v1 reconduite à
    l'identique) : le cadre et le panneau RELEVÉS posés à leurs adresses,
    la poignée rendue à l'OS virtuel. Retourne la poignée. Après ceci,
    l'émulation est VIVANTE."""
    import struct
    import harnais_noyau as HN
    emul.uc.mem_write(HN.L.R_CADRE, releve["cadre"])
    emul.uc.mem_write(HN.L.R_EMPREINTES, releve["panneau"])
    poignee = struct.unpack("<Q", releve["cadre"][528:536])[0]
    os_v.poignees[poignee] = (chemin, releve["pos"])
    return poignee
