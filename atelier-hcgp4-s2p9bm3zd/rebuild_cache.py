#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rebuild_cache.py — LA MÉMOÏSATION CONTENT-ADDRESSED DU RÉGIME (S2P9BM3D,
la vague 14, le levier (1) du plan gelé) : le mémo des 60 REBUILDS du bras T.

LA CLÉ (miroir de roundtrip_cache.py, la lettre du plan — un octet changé
d'UN SEUL terme = clé différente = ABSENCE = le rebuild court VIVANT) :

  cle = sha256( sha256(notation assemblée)   — l'arbre ENTIER de l'unité
                (pièce) OU le fichier scellé (bloc) +, pour la pièce, les
                notations scellées loupe/ lues aux arbres par le build
              ‖ le CONTRAT des contrôles       — ce qui fonde le verdict
              ‖ le PROFIL                      — l'unité, le niveau, la cible
              ‖ la GRAINE de campagne          — 20261123
              ‖ la CONFIG MOTEUR )             — python/keystone/capstone +
                                                   le sha256 des modules du
                                                   moteur (build_loupe, B4,
                                                   m3, l'auteur, le layout)

LE FAIL-CLOSED (miroir roundtrip_cache, la discipline, jamais l'optimisme) :
  — le mémo illisible, corrompu ou absent est traité comme VIDE (tout
    rebuild re-exécuté — jamais un produit cru sur un JSON tordu) ;
  — un produit caché mal formé, ou dont le verdict n'est pas VERT, est un
    hit REFUSÉ (miss — le rebuild court) ;
  — SEULS les produits VERTS sont cachés : un REFUS ne se souvient JAMAIS
    (l'échec se re-constate à chaque rebuild) ;
  — la CHAÎNE + la signature Ed25519 (miroir memo v2) : chaque entrée porte
    son h chaînée depuis la genèse, et LE COMPTEUR D'AUDIT vit dans le CŒUR
    SIGNÉ — toute mutation du compteur ou d'une entrée = SIGNATURE-INVALIDE
    ou CHAÎNE-ROMPUE = mémo TRAITÉ VIDE (fail-closed).

L'AUDIT 1-SUR-10 VIVANT ET CHAÎNÉ (CONSERVÉ — jamais contourné) : chaque
rebuild = UN scellement (le compteur +1, signé) ; le scellement qui porte
le compteur à un multiple de la période (10) déclenche LA RE-EXÉCUTION
COMPLÈTE du rebuild — le relevé re-exécuté CONFRONTÉ champ par champ au
produit caché : TOUT écart = ÉCHEC NOMMÉ (le registre porte les champs
divergents), jamais une confiance silencieuse.

ÉPHÉMÈRE : le JSON vit à l'ATELIER, JAMAIS dans les pièces scellées
(tls13/, loupe/, m4/, m1/ — lecture seule, les empreintes le prouvent).

L'ANCRE DE COPIE est neutre au produit : la confrontation des DIX produits
par unité (des noms de copies différents, des octets identiques) le prouve
à CHAQUE run — la clé hash l'arbre SOURCE, pas le nom de la copie.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")

# La version du contrat de rebuild (la liste des contrôles qui fondent le
# verdict — un changement de contrat = une clé différente = tout re-exécuté).
CONTRAT_REBUILD = "hcgp4-r1"
CONTRAT_DESC = {
    "contrat": CONTRAT_REBUILD,
    "n_par_unite": 10,                 # dix rebuilds par unité (le plan §2)
    "unites": ["loupe-01", "loupe-02", "loupe-05", "loupe-08",
               "loupe-13", "loupe-16"],          # 10 × 6 = 60 par bras
    "confrontation": "dix produits identiques + codes 0 par unité",
    "audit": "1 scellement sur 10 signé : re-exécution complète + "
             "confrontation champ par champ au produit caché",
    "cible": "x86-64-win11-pe · ABI msx64",
}

# Les champs exigés d'un produit caché valide (le hit refusé s'il en manque).
CHAMPS_PRODUIT = ("verdict", "sha256_produit", "octets", "code",
                  "verificateur", "niveau")

# La genèse, la constante de clé de test (publique — miroir memo v2), la
# période d'audit (l'instruction du plan : 1 sur 10).
GENESE = b"TRIADE-MEMO-REBUILDS-V1"
CONSTANTE_CLE_TEST = b"TRIADE-MEMO-REBUILDS-TEST-2026-v1"
FORMAT = "TRIADE-MEMO-REBUILDS-V1"
PERIODE_AUDIT = 10

# Les modules du moteur lus par les builds (LECTURE SEULE — hashés dans la
# config moteur de la clé : un octet changé du moteur = miss).
MOTEURS = [
    REPO / "loupe" / "build_loupe.py",
    REPO / "loupe" / "layout.py",
    REPO / "loupe" / "outils" / "auteur.py",
    REPO / "m4" / "build_m4.py",
    REPO / "m3" / "build_m3.py",
    REPO / "m3" / "layout.py",
    REPO / "m3" / "carte_m3.py",
    REPO / "m3" / "oracle_m3.py",
]


class MemoRefus(Exception):
    """Le mémo vérifié a échoué — refus nommé, fail-closed (jamais cru)."""


def sha(chemin: pathlib.Path) -> str:
    return hashlib.sha256(pathlib.Path(chemin).read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# LA CONFIG MOTEUR (les versions + les modules du moteur hashés)
# ---------------------------------------------------------------------------

def moteur_versions_rebuild() -> str:
    import capstone
    import keystone
    parties = [
        f"python={sys.version_info.major}.{sys.version_info.minor}."
        f"{sys.version_info.micro}",
        f"keystone={getattr(keystone, '__version__', '?')}",
        f"capstone={getattr(capstone, '__version__', '?')}"]
    for m in MOTEURS:
        rel = m.relative_to(REPO).as_posix()
        parties.append(f"{rel}={sha(m)[:16]}" if m.exists()
                       else f"{rel}=ABSENT")
    return ";".join(parties)


# ---------------------------------------------------------------------------
# LA NOTATION ASSEMBLÉE (tout ce que le rebuild lit — l'arbre déterministe)
# ---------------------------------------------------------------------------

IGNORE_ARBRE = {"kit", "kit-v2", "piece", "kit-temoins"}   # miroir copytree


def _fichiers_arbre(base: pathlib.Path):
    for f in sorted(base.rglob("*")):
        if any(part in IGNORE_ARBRE
               for part in f.relative_to(base).parts):
            continue
        if f.is_file():
            yield f


def arbre(base: pathlib.Path) -> tuple[str, int, int]:
    """Le hash déterministe d'un arbre : chemin relatif + octets de CHAQUE
    fichier (un octet changé n'importe où = hash différent)."""
    h = hashlib.sha256()
    n, tot = 0, 0
    for f in _fichiers_arbre(base):
        b = f.read_bytes()
        h.update(f.relative_to(base).as_posix().encode("utf-8"))
        h.update(len(b).to_bytes(8, "little"))
        h.update(b)
        n += 1
        tot += len(b)
    return h.hexdigest(), n, tot


def notation_assemblee_piece(src_dir: pathlib.Path) -> str:
    """PIÈCE : l'arbre de l'unité (tout ce qui est copié au rebuild, build
    compris) + LES NOTATIONS SCELLÉES loupe/ lues aux arbres par le build
    (les 17 blocs — lecture seule)."""
    h1, n1, o1 = arbre(src_dir)
    h2, n2, o2 = arbre(REPO / "loupe" / "notation")
    h = hashlib.sha256()
    h.update(h1.encode())
    h.update(h2.encode())
    return h.hexdigest()


def notation_assemblee_bloc(chemin: pathlib.Path) -> str:
    """BLOC (loupe-05) : le fichier de notation scellé SEUL — ce que la
    reconstruction lit (moteur et profil couverts par les leurs)."""
    return hashlib.sha256(pathlib.Path(chemin).read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# LA CLÉ (miroir roundtrip_cache.cle : les champs préfixés par leur longueur)
# ---------------------------------------------------------------------------

def cle_rebuild(notation_hex: str, contrat: str, profil: str,
                graine: int, moteur: str) -> str:
    h = hashlib.sha256()
    for champ in (notation_hex, contrat, profil, str(graine), moteur):
        b = champ.encode("utf-8")
        h.update(len(b).to_bytes(8, "little"))
        h.update(b)
    return h.hexdigest()


def profil_config(unite: str, niveau: str) -> str:
    """Le profil (miroir roundtrip_cache.profil_config) : le contrat, l'unité,
    le niveau, la cible — tout ce qui, sans changer la notation, changerait
    le déroulement."""
    return (f"{CONTRAT_REBUILD};{unite};{niveau};x86-64-win11-pe;msx64;"
            f"rebuild=1")


# ---------------------------------------------------------------------------
# LA CONFRONTATION CHAMP PAR CHAMP (l'audit — tout écart NOMMÉ)
# ---------------------------------------------------------------------------

def confronter_champ_par_champ(releve_vivant: dict,
                                produit_cache: dict) -> list[str]:
    """La preuve d'identité de l'audit : le relevé de la re-exécution
    vivante confronté au produit caché — TOUT écart nommé, bloquant.
    («secondes» n'est PAS un champ d'identité : le prix du vivant n'est pas
    le produit.)"""
    ecarts: list[str] = []
    champs = sorted(set(CHAMPS_PRODUIT)
                    | {k for k in produit_cache if k != "secondes"}
                    | {k for k in releve_vivant if k != "secondes"})
    for champ in champs:
        v = releve_vivant.get(champ, "<absent>")
        m = produit_cache.get(champ, "<absent>")
        if v != m:
            ecarts.append(f"{champ} : vivant {v!r} != mémo {m!r}")
    return ecarts


# ---------------------------------------------------------------------------
# LE MÉMO — chaîne + signature Ed25519, le compteur au CŒUR SIGNÉ
# (miroir memo_sessions_v2, adapté aux rebuilds)
# ---------------------------------------------------------------------------

def _ser(valeur: dict) -> bytes:
    return json.dumps(valeur, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def _h(precedent: bytes, cle: str, valeur: dict) -> str:
    return hashlib.sha256(
        precedent + bytes.fromhex(cle) + _ser(valeur)).hexdigest()


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


class MemoRebuilds:
    """Le mémo des rebuilds : charger() vérifie TOUT (chaîne, signature,
    compteur — le fail-closed du roundtrip_cache : un refus = un mémo VIDE) ;
    deposer() accumule ; sceller() recalcule, signe, INCRÉMENTE LE COMPTEUR
    et rend l'état d'audit du scellement."""

    def __init__(self, chemin, moteur: str | None = None, graine=None):
        self.chemin = pathlib.Path(chemin)
        self.moteur = moteur or moteur_versions_rebuild()
        self.graine = graine
        self.entrees: list[dict] = []
        self.index: dict[str, dict] = {}
        self._a_deposer: list[tuple[str, dict]] = []
        self.compteur_rebuilds = 0
        self.config_hash = ""
        self.compteurs = {"hit": 0, "miss": 0, "audit": 0,
                          "refus_produit": 0, "refus_chargement": None}
        self._charger_fail_closed()

    # -- le cœur signé (le compteur vit dedans : le muter = signature rompue)
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

    def _charger_fail_closed(self) -> None:
        """LE FAIL-CLOSED : un mémo absent, illisible ou qui échoue à la
        vérification est traité comme VIDE — tout rebuild re-exécuté ; le
        refus NOMMÉ aux compteurs (jamais un silicium de confiance)."""
        if not self.chemin.exists():
            return
        try:
            self._charger()
        except MemoRefus as exc:
            self.compteurs["refus_chargement"] = str(exc)
            self.entrees, self.index = [], {}
            self.compteurs["miss"] = 0

    def _charger(self) -> None:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import \
            Ed25519PublicKey
        doc = json.loads(self.chemin.read_text(encoding="utf-8"))
        if doc.get("format") != FORMAT:
            raise MemoRefus(f"FORMAT-INCONNU : {doc.get('format')!r}")
        if doc.get("constante") != CONSTANTE_CLE_TEST.hex():
            raise MemoRefus("CONSTANTE-DIVERGENTE")
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
                    f"CHAÎNE-ROMPUE à l'entrée {cle[:16]}… : h attendu "
                    f"{attendu[:16]}…, lu {h[:16]}…")
            precedent = bytes.fromhex(attendu)
        if doc.get("racine") != precedent.hex():
            raise MemoRefus("RACINE-DIVERGENTE : la chaîne ne ferme pas sur "
                            "la racine déclarée")
        coeur = self._coeur(doc["publique"], precedent.hex(),
                            int(doc.get("compteur_rebuilds", 0)),
                            len(entrees), doc.get("config_hash", ""),
                            doc.get("graine"))
        try:
            Ed25519PublicKey.from_public_bytes(
                bytes.fromhex(doc["publique"])).verify(
                bytes.fromhex(doc["signature"]), coeur)
        except InvalidSignature:
            raise MemoRefus(
                "SIGNATURE-INVALIDE : le mémo n'est pas scellé par la clé "
                "de test du format — le COMPTEUR D'AUDIT ou l'en-tête fut "
                "muté")
        self.entrees = entrees
        self.index = {e["cle"]: e["valeur"] for e in entrees}
        self.compteur_rebuilds = int(doc.get("compteur_rebuilds", 0))
        self.config_hash = doc.get("config_hash", "")
        self.graine = doc.get("graine")

    # -- consultation --
    def consulter(self, cle: str) -> dict | None:
        return self.index.get(cle)

    # -- dépôt (le hit refusé se RE-CACHE au miss — miroir roundtrip_cache) --
    def deposer(self, cle: str, valeur: dict) -> None:
        self._a_deposer.append((cle, valeur))

    def sceller(self, config: dict | None = None,
                graine=None) -> dict:
        """Recalcule la chaîne ENTIÈRE, signe (le compteur DANS le cœur),
        INCRÉMENTE le compteur de rebuilds, écrit — et recharge vérifiée.
        Retourne {n, racine, signature, compteur_rebuilds, audit_du} :
        audit_du = CE scellement porte le compteur à un multiple de la
        période — le rebuild qui scelle SAIT qu'il vient de courir l'audit."""
        entrees = [dict(e) for e in self.entrees]
        index = {e["cle"]: e for e in entrees}
        for cle, valeur in self._a_deposer:
            if cle in index:
                index[cle]["valeur"] = valeur      # le re-cache du miss
            else:
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
        self.compteur_rebuilds += 1       # UN SCELLEMENT DE REBUILD = UN RUN
        privee = _cle_test()
        publique = cle_publique_test_hex()
        coeur = self._coeur(publique, precedent.hex(),
                            self.compteur_rebuilds, len(entrees),
                            self.config_hash, self.graine)
        signature = privee.sign(coeur).hex()
        doc = {"format": FORMAT,
               "constante": CONSTANTE_CLE_TEST.hex(),
               "publique": publique,
               "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "config_hash": self.config_hash,
               "graine": self.graine,
               "compteur_rebuilds": self.compteur_rebuilds,
               "contrat": CONTRAT_REBUILD,
               "racine": precedent.hex(),
               "signature": signature,
               "entrees": entrees}
        tmp = self.chemin.with_suffix(".tmp")
        tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=1),
                       encoding="utf-8")
        tmp.replace(self.chemin)
        self.entrees, self.index, self._a_deposer = entrees, \
            {e["cle"]: e["valeur"] for e in entrees}, []
        return {"n": len(entrees), "racine": precedent.hex(),
                "signature": signature,
                "compteur_rebuilds": self.compteur_rebuilds,
                "audit_du": self.compteur_rebuilds % PERIODE_AUDIT == 0}


# ---------------------------------------------------------------------------
# L'OPÉRATION DE REBUILD AU MÉMO — hit / miss / audit (le juge partout)
# ---------------------------------------------------------------------------

def produit_valide(cache: dict | None, niveau: str) -> bool:
    return (cache is not None
            and all(k in cache for k in CHAMPS_PRODUIT)
            and cache["verdict"] == "VERT"
            and cache["verificateur"] == CONTRAT_REBUILD
            and cache["niveau"] == niveau)


def op_rebuild(memo: MemoRebuilds, cle: str, niveau: str,
               executeur_vivant) -> dict:
    """UN rebuild au mémo — LE MÊME JUGE PARTOUT :

    - l'AUDIT (le scellement porte le compteur à un multiple de 10, AVANT
      l'incrément) : LA RE-EXÉCUTION COMPLÈTE, JAMAIS servie du mémo ; le
      relevé vivant CONFRONTÉ champ par champ au produit caché — TOUT écart
      = ÉCHEC NOMMÉ (le registre porte les champs, la run échoue) ; à
      l'absence : le semis d'audit ;
    - le HIT (produit VERT bien formé) : le produit rendu SANS ré-exécution ;
    - le MISS : le rebuild court VIVANT (fail-closed), le produit VERT se
      sème ; un REFUS ne se cache JAMAIS.

    PUIS LE SCELLEMENT : compteur +1 dans le cœur signé. Retour
    {**releve, origine, ecarts, scellement}."""
    audit = (memo.compteur_rebuilds + 1) % PERIODE_AUDIT == 0
    cache = memo.consulter(cle)
    hit = produit_valide(cache, niveau)
    ecarts: list[str] = []
    if audit:
        memo.compteurs["audit"] += 1
        releve = executeur_vivant()            # LA RE-EXÉCUTION COMPLÈTE
        if hit:
            ecarts = confronter_champ_par_champ(releve, cache)
            if ecarts:
                # ÉCHEC NOMMÉ — le vivant fait foi, le caché discrédité ;
                # JAMAIS maquillé, JAMAIS guéri en silence
                memo.compteurs["refus_produit"] += 1
        elif cache is not None:
            ecarts = ["le produit caché MAL FORMÉ : " + ", ".join(
                sorted(set(CHAMPS_PRODUIT) - set(cache)))]
            memo.compteurs["refus_produit"] += 1
        else:
            if releve.get("verdict") == "VERT":
                memo.deposer(cle, _cacheable(releve))     # le semis d'audit
    elif hit:
        memo.compteurs["hit"] += 1
        releve = dict(cache)
    else:
        memo.compteurs["miss"] += 1
        releve = executeur_vivant()             # MISS : le rebuild court
        if releve.get("verdict") == "VERT":
            memo.deposer(cle, _cacheable(releve))
        else:
            memo.compteurs["refus_produit"] += 1
    scellement = memo.sceller(config={"moteur": memo.moteur,
                                      **CONTRAT_DESC},
                              graine=memo.graine)
    return {**releve, "origine": ("audit" if audit else
                                  "hit" if hit else "miss"),
            "ecarts": ecarts, "scellement": scellement}


def _cacheable(releve: dict) -> dict:
    """Le produit caché : les champs d'identité SEULES («secondes» — le prix
    du vivant — n'est pas le produit)."""
    out = {k: releve[k] for k in CHAMPS_PRODUIT if k in releve}
    for k in ("instructions", "unite"):
        if k in releve:
            out[k] = releve[k]
    return out
