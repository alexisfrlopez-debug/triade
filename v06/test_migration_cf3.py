#!/usr/bin/env python3
"""test_migration_cf3.py — D127 : la falsifiabilité de la migration CF2 → CF3.

Une garde qui ne rejette rien ne garde rien (leçon M3). Cette suite prouve
les actes de la cérémonie de migration un par un (spec v06/I/CF3/README.md
§ 12 — l'outillage naît D127, la preuve terrain de la serrure est acquise
D125) :

  M1  la CHAÎNE COMPLÈTE contre témoin indépendant : CF1 (coffre_fort.py)
      → CF2 (le VRAI migrer CF2) → CF3 (le migrer D127) — le clair passe
      OCTET POUR OCTET (rien à traduire : le clair CF3 == le clair que CF2
      scellait, témoin recalculé par le TEST), époque 1, checksum témoin,
      H_projet == condensé du MÊME clair, piège posé sur le média, miroir
      « 1 <checksum> », journal MIGRATION, conteneur CF2 INTACT (md5 avant
      == après), fragments INTACTS, aucun staging laissé
  M2  refus nommés AVANT toute écriture : conteneur CF3 déjà présent (jamais
      d'écrasement), phrase vide, conteneur CF2 absent, média du piège
      absent (il ne se CRÉE jamais), config CF2 explicite absente
  M3  la phrase DÉCIDE : le coffre migré sous la phrase B s'ouvre sous B
      (VERT) et REFUSE la phrase A (PhraseErronee nommée — JAMAIS de
      destruction : conteneur intact, aucun PV)
  M4  fragments INSUFFISANTS (2 valides < seuil 3) : refus nommé AVANT
      toute écriture — ni conteneur, ni piège, ni staging
  M5  PORTE D120 honorée : exiger_sentinelle=true + heart-beat absent →
      refus NOMMÉ avant toute lecture de fragment (rien écrit) ; le MÊME
      fichier avec heart-beat VIVANT passe — la porte distingue, elle ne
      bloque pas en aveugle
  M6  orphelin de piège : un piège d'époque 1 préexistant (migration
      interrompue — pas de conteneur CF3) est REMPLACÉ, la migration est
      REJOUABLE, verdict VERT
  M7  re-lecture À FROID : un scellage corrompu (le laboratoire mute UN
      octet du chiffretexte) est ATTRAPÉ — staging détruit, conteneur CF3
      JAMAIS posé, conteneur CF2 intact, PV écrit — et la migration est
      REJOUABLE immédiatement après (l'orphelin est remplacé, VERT)
  M8  detruire-cf2 : sans --oui-je-comprends → refus nommé, CF2 intact ;
      conteneur CF3 ABSENT → refus FAIL-CLOSED (jamais l'ancien sans le
      neuf) ; avec le drapeau : conteneur CF2 DÉTRUIT, fragments INTACTS
      octet pour octet, PV nommé (relève HISTORIQUE), journal DESTRUCTION,
      et le CF3 reste VERT après la mort de l'ancien
  M9  CLI en sous-processus (comme le terrain) : migrer --phrase-stdin
      code 0 avec sortie qui NOMME le checksum et le protocole
      detruire-cf2 ; detruire-cf2 sans drapeau refusé nommé ; verifier à
      froid code 0 ; un second migrer refusé nommé

Usage : python3 v06/test_migration_cf3.py   (~30-90 s selon machine —
Argon2id à chaque dérivation, c'est le prix de la preuve)
"""

import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)
from v06 import coffre_cf3 as C                    # noqa: E402
import coffre_fort as cf1                           # noqa: E402

# cf2 par l'instance MÊME que coffre_cf3 utilise en interne (C._cf2) : la
# suite attrape les exceptions de LA classe qui court réellement — un
# double import (from v06 import coffre_cf2) fabrique une seconde instance
# du module et des classes d'exception DISTINCTES : le refus levé par le
# cf2 interne traverserait l'except du test sans être attrapé (leçon de
# falsifiabilité : la preuve s'attache à la vérité vivante, pas à sa copie).
cf2 = C._cf2

PHRASE = b"phrase-de-laboratoire-migration-D127"
RESULTATS = []


def _verifie(temoin: str, condition: bool) -> None:
    RESULTATS.append((temoin, bool(condition)))
    print(f"[test-migration] {temoin} : {'PASS' if condition else 'ÉCHEC'}")


def _refuse(temoin: str, fonction, *args, attendu: str, **kwargs) -> None:
    """Un refus NOMMÉ est une preuve ; un crash muet est un défaut."""
    try:
        fonction(*args, **kwargs)
        _verifie(temoin, False)
        print(f"           attendu : refus nommé contenant « {attendu} »")
    except (C.ErreurCoffre, cf2.ErreurCoffre) as exc:
        ok = attendu in str(exc)
        _verifie(temoin, ok)
        if not ok:
            print(f"           reçu : {exc}")


def _octets(chemin: str) -> bytes:
    with open(chemin, "rb") as f:
        return f.read()


def _texte(chemin: str) -> str:
    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()


def _md5(chemin: str) -> str:
    return hashlib.md5(_octets(chemin)).hexdigest()


# ---------------------------------------------------------------------------
# Le bac : CF1 → CF2 RÉELS (la migration CF3 part d'un coffre CF2 vivant)
# ---------------------------------------------------------------------------

class Bac:
    """Répertoire temporaire : conteneur CF2 (par le VRAI migrer CF2) +
    média du piège séparé + heart-beat vivant (la porte D120 est ARMÉE au
    laboratoire Linux ; les tests qui veulent la porte MORTE la fabriquent
    eux-mêmes — discipline D105 : tout vit dans le temporaire)."""

    def __init__(self, etiquette="migr"):
        self.rep = tempfile.mkdtemp(prefix=f"test-migr-cf3-{etiquette}-")
        self.cf1 = os.path.join(self.rep, "coffre_fort.bin")
        self.cf2 = os.path.join(self.rep, "coffre_cf2.bin")
        self.cf3 = os.path.join(self.rep, "coffre_cf3.bin")
        self.gardes = os.path.join(self.rep, "gardes")
        self.cfg = os.path.join(self.rep, "config_cf2.json")
        self.media = os.path.join(self.rep, "media-piege")
        os.makedirs(self.media)
        base = cf1.nouvelle_base()
        base["description"] = "laboratoire migration CF2 -> CF3 (D127)"
        base["projets"]["projet-labo"] = {"description": "", "entrees": [
            {"etiquette": "entree-a", "description": "",
             "phrase_b64": base64.b64encode(b"AAAA").decode("ascii")},
            {"etiquette": "entree-b", "description": "",
             "phrase_b64": base64.b64encode(b"BBBB").decode("ascii")}]}
        base["projets"]["second"] = {"description": "", "entrees": []}
        cf1.sauver(self.cf1, base, PHRASE)
        cf2.migrer(self.cf1, self.cf2, self.gardes, 5, 3, PHRASE, self.cfg)
        config = cf2.lire_config(self.cfg)
        config["journal"] = os.path.join(self.rep, "journal-sentinelle.txt")
        config["heartbeat"] = os.path.join(self.rep, "heartbeat.txt")
        config["pv_dir"] = os.path.join(self.rep, "pv-cf2")
        cf2.ecrire_config(self.cfg, config)
        self.config = config
        self.base = base
        self.heartbeat_vivant()

    def heartbeat_vivant(self) -> None:
        with open(self.config["heartbeat"], "w", encoding="utf-8") as f:
            json.dump({"ts": time.time()}, f)

    def fragments(self) -> dict:
        return {i: os.path.join(self.gardes, f"g{i}",
                                f"fragment-{i}.cf2f")
                for i in range(1, 6)}

    def piege(self, epoque: int = 1) -> str:
        return C.chemin_piege(self.media, epoque)

    def migrer_cf3(self, phrase=PHRASE, **kwargs):
        conteneur_cf2 = kwargs.pop("conteneur_cf2", self.cf2)
        kwargs.setdefault("conteneur_chemin", self.cf3)
        kwargs.setdefault("config_cf2", self.cfg)
        return C.migrer(conteneur_cf2, self.media, phrase, **kwargs)

    def rien_ecrit(self) -> bool:
        return (not os.path.isfile(self.cf3)
                and not os.path.isfile(self.cf3 + ".staging")
                and not os.path.isfile(self.piege(1)))

    def nettoyer(self) -> None:
        shutil.rmtree(self.rep, ignore_errors=True)


# ---------------------------------------------------------------------------
# M1 — la chaîne complète contre témoin indépendant
# ---------------------------------------------------------------------------

def m1_cycle_complet():
    print("[test-migration] --- m1_cycle_complet (CF1 → CF2 → CF3) ---")
    bac = Bac("m1")
    try:
        md5_cf2_avant = _md5(bac.cf2)
        frags_avant = {p: _octets(p) for p in bac.fragments().values()}
        info = bac.migrer_cf3()
        _verifie("m1-verdict-epoque-1", info["epoque"] == 1)

        # TÉMOIN INDÉPENDANT : le clair et son condensé recalculés par le
        # TEST (pas par l'outil) — le MÊME clair que CF2 scellait
        clair_temoin = json.dumps(bac.base, ensure_ascii=False).encode()
        temoin = hashlib.sha256(clair_temoin).digest()
        _verifie("m1-checksum-temoin-independant",
                 info["checksum"] == temoin[:4].hex())

        base_cf3, entete = C.sentinelle_instantanee(
            _octets(bac.cf3), bac.piege(1), PHRASE, bac.cf3,
            brouillon_chemin=None, consigner=False)
        _verifie("m1-rien-a-traduire-octet-pour-octet",
                 C._serialiser(base_cf3) == clair_temoin)
        _verifie("m1-h-projet-condense-du-meme-clair",
                 entete["h_projet"] == temoin)
        _verifie("m1-base-identique-cf2-vers-cf3", base_cf3 == bac.base)

        _verifie("m1-piege-posé-sur-le-média", os.path.isfile(bac.piege(1)))
        _verifie("m1-miroir-consigne",
                 _texte(C.chemin_miroir(bac.cf3))
                 == f"1 {info['checksum']}\n")
        _verifie("m1-journal-migration",
                 "MIGRATION CF2" in _texte(C.chemin_journal(bac.cf3)))
        _verifie("m1-conteneur-cf2-intact",
                 _md5(bac.cf2) == md5_cf2_avant)
        _verifie("m1-fragments-cf2-intacts",
                 all(_octets(p) == b for p, b in frags_avant.items()))
        _verifie("m1-aucun-staging-laissé",
                 not os.path.isfile(bac.cf3 + ".staging"))

        # le verdict à froid après migration (l'acte 3 de la cérémonie)
        verdict = C.verifier(bac.cf3, bac.piege(1), PHRASE)
        _verifie("m1-verdict-a-froid-vert",
                 verdict["epoque"] == 1
                 and verdict["checksum"] == info["checksum"]
                 and verdict["projets"] == 2)
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# M2 — refus nommés AVANT toute écriture
# ---------------------------------------------------------------------------

def m2_refus_nommes():
    print("[test-migration] --- m2_refus_nommes ---")
    bac = Bac("m2")
    try:
        bac.migrer_cf3()
        _refuse("m2-conteneur-cf3-deja-present",
                bac.migrer_cf3, attendu="DÉJÀ PRÉSENT")

        bac2 = Bac("m2b")
        try:
            _refuse("m2-phrase-vide-refusée",
                    bac2.migrer_cf3, phrase=b"", attendu="phrase VIDE")
            _refuse("m2-conteneur-cf2-absent",
                    bac2.migrer_cf3,
                    conteneur_cf2=os.path.join(bac2.rep, "rien.bin"),
                    attendu="conteneur CF2 ABSENT")
            _refuse("m2-config-cf2-explicite-absente",
                    bac2.migrer_cf3,
                    config_cf2=os.path.join(bac2.rep, "config-absente.json"),
                    attendu="config CF2 ABSENTE")
            # le média du piège ne se CRÉE jamais — un chemin absent est un
            # refus nommé, pas un dossier fabriqué par la machine
            _refuse("m2-media-du-piege-absent",
                    C.migrer, bac2.cf2,
                    os.path.join(bac2.rep, "média-inconnu"), PHRASE,
                    conteneur_chemin=bac2.cf3, config_cf2=bac2.cfg,
                    attendu="média du piège ABSENT")
            _verifie("m2-rien-écrit-par-les-refus", bac2.rien_ecrit())
        finally:
            bac2.nettoyer()
        _verifie("m2-cf2-intact-après-refus",
                 os.path.isfile(bac.cf2) and _md5(bac.cf2) is not None)
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# M3 — la phrase décide (jamais de destruction sur phrase erronée)
# ---------------------------------------------------------------------------

def m3_phrase():
    print("[test-migration] --- m3_phrase ---")
    bac = Bac("m3")
    try:
        bac.migrer_cf3(phrase="phrase-B-de-ceremonie".encode("utf-8"))
        verdict = C.verifier(bac.cf3, bac.piege(1),
                             "phrase-B-de-ceremonie".encode("utf-8"))
        _verifie("m3-ouverte-sous-sa-phrase", verdict["epoque"] == 1)
        md5_avant = _md5(bac.cf3)
        pv_dir = C.chemin_pv_dir(bac.cf3)
        _refuse("m3-phrase-erronée-nommée-jamais-destruction",
                C.verifier, bac.cf3, bac.piege(1), PHRASE,
                attendu="phrase ERRONÉE")
        _verifie("m3-conteneur-intact-sur-phrase-erronée",
                 _md5(bac.cf3) == md5_avant
                 and (not os.path.isdir(pv_dir) or not os.listdir(pv_dir)))
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# M4 — fragments insuffisants : refus AVANT toute écriture
# ---------------------------------------------------------------------------

def m4_fragments_insuffisants():
    print("[test-migration] --- m4_fragments_insuffisants ---")
    bac = Bac("m4")
    try:
        for i in (3, 4, 5):        # 2 valides < seuil 3
            os.unlink(bac.fragments()[i])
        _refuse("m4-fragments-insuffisants-nommés",
                bac.migrer_cf3, attendu="fragments INSUFFISANTS")
        _verifie("m4-rien-écrit", bac.rien_ecrit())
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# M5 — la PORTE D120 honorée (les deux côtés)
# ---------------------------------------------------------------------------

def m5_porte_d120():
    print("[test-migration] --- m5_porte_d120 ---")
    bac = Bac("m5")
    try:
        config = dict(bac.config)
        config["exiger_sentinelle"] = True
        config["heartbeat"] = os.path.join(bac.rep, "heartbeat-MORT.txt")
        cfg_morte = os.path.join(bac.rep, "config-porte-morte.json")
        cf2.ecrire_config(cfg_morte, config)
        _refuse("m5-porte-sentinelle-morte-refus-nommé",
                C.migrer, bac.cf2, bac.media, PHRASE,
                conteneur_chemin=bac.cf3, config_cf2=cfg_morte,
                attendu="sentinelle NON VIVANTE")
        _verifie("m5-rien-écrit-porte-morte", bac.rien_ecrit())
        # le MÊME fichier, heart-beat VIVANT : la porte distingue
        with open(config["heartbeat"], "w", encoding="utf-8") as f:
            json.dump({"ts": time.time()}, f)
        info = C.migrer(bac.cf2, bac.media, PHRASE,
                        conteneur_chemin=bac.cf3, config_cf2=cfg_morte)
        _verifie("m5-porte-sentinelle-vivante-passe",
                 info["epoque"] == 1 and os.path.isfile(bac.cf3))
        verdict = C.verifier(bac.cf3, bac.piege(1), PHRASE)
        _verifie("m5-verdict-vert-après-porte-vivante",
                 verdict["epoque"] == 1)
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# M6 — orphelin de piège remplacé (migration rejouable)
# ---------------------------------------------------------------------------

def m6_orphelin_piege():
    print("[test-migration] --- m6_orphelin_piege ---")
    bac = Bac("m6")
    try:
        # un piège d'époque 1 préexistant : déchet d'une migration
        # interrompue (le conteneur CF3 n'existe pas)
        with open(bac.piege(1), "wb") as f:
            f.write(b"TRIADE-CF3-PIEGE v1\nepoque: 1\ngarbage\n")
        info = bac.migrer_cf3()
        _verifie("m6-orphelin-remplacé", info["epoque"] == 1)
        verdict = C.verifier(bac.cf3, bac.piege(1), PHRASE)
        _verifie("m6-verdict-vert-après-rejeu", verdict["epoque"] == 1)
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# M7 — la re-lecture à froid attrape un scellage corrompu
# ---------------------------------------------------------------------------

def m7_relecture_froide():
    print("[test-migration] --- m7_relecture_froide ---")
    bac = Bac("m7")
    try:
        md5_cf2_avant = _md5(bac.cf2)
        constructeur = C.construire_conteneur

        def corrompu(*args, **kwargs):
            blob = constructeur(*args, **kwargs)
            return blob[:-1] + bytes([blob[-1] ^ 1])   # UN octet muté

        C.construire_conteneur = corrompu
        try:
            _refuse("m7-scellage-corrompu-attrapé",
                    bac.migrer_cf3, attendu="falsification")
        finally:
            C.construire_conteneur = constructeur
        _verifie("m7-conteneur-cf3-jamais-posé", not os.path.isfile(bac.cf3))
        _verifie("m7-staging-détruit",
                 not os.path.isfile(bac.cf3 + ".staging"))
        _verifie("m7-conteneur-cf2-intact",
                 _md5(bac.cf2) == md5_cf2_avant)
        pv_dir = C.chemin_pv_dir(bac.cf3)
        _verifie("m7-pv-écrit",
                 os.path.isdir(pv_dir) and os.listdir(pv_dir))
        # REJOUABLE immédiatement : l'orphelin de piège est remplacé
        info = bac.migrer_cf3()
        verdict = C.verifier(bac.cf3, bac.piege(1), PHRASE)
        _verifie("m7-migration-rejouable-verte",
                 info["epoque"] == 1 and verdict["epoque"] == 1)
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# M8 — detruire-cf2 (le quatrième acte, explicite)
# ---------------------------------------------------------------------------

def m8_detruire_cf2():
    print("[test-migration] --- m8_detruire_cf2 ---")
    bac = Bac("m8")
    try:
        bac.migrer_cf3()
        frags_avant = {p: _octets(p) for p in bac.fragments().values()}
        _refuse("m8-sans-affirmation-refus-nommé",
                C.detruire_cf2, bac.cf2, bac.cf3,
                attendu="--oui-je-comprends")
        _verifie("m8-cf2-intact-sans-affirmation",
                 os.path.isfile(bac.cf2))
        _refuse("m8-cf3-absent-refus-fail-closed",
                C.detruire_cf2, bac.cf2,
                os.path.join(bac.rep, "cf3-absent.bin"), True,
                attendu="perte sèche")
        _verifie("m8-cf2-intact-garde-fail-closed",
                 os.path.isfile(bac.cf2))

        C.detruire_cf2(bac.cf2, bac.cf3, True)
        _verifie("m8-conteneur-cf2-détruit", not os.path.isfile(bac.cf2))
        _verifie("m8-fragments-intacts-octet-pour-octet",
                 all(_octets(p) == b for p, b in frags_avant.items()))
        pv_dir = C.chemin_pv_dir(bac.cf3)
        pvs = os.listdir(pv_dir) if os.path.isdir(pv_dir) else []
        _verifie("m8-pv-nomme-la-relève-historique",
                 len(pvs) == 1
                 and "relève HISTORIQUE" in _texte(
                     os.path.join(pv_dir, pvs[0])))
        _verifie("m8-journal-destruction",
                 "DESTRUCTION CF2" in _texte(C.chemin_journal(bac.cf3)))
        verdict = C.verifier(bac.cf3, bac.piege(1), PHRASE)
        _verifie("m8-cf3-vert-après-la-mort-de-l-ancien",
                 verdict["epoque"] == 1)
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# M9 — CLI en sous-processus (comme le terrain)
# ---------------------------------------------------------------------------

def _cli(*args, stdin: bytes = b""):
    commande = [sys.executable, os.path.join("v06", "coffre_cf3.py"), *args]
    r = subprocess.run(commande, input=stdin, cwd=RACINE,
                       capture_output=True, timeout=600)
    return SimpleNamespace(code=r.returncode,
                           out=r.stdout.decode("utf-8", "replace"),
                           err=r.stderr.decode("utf-8", "replace"))


def m9_cli():
    print("[test-migration] --- m9_cli (sous-processus) ---")
    bac = Bac("m9")
    try:
        r = _cli("migrer", "--conteneur-cf2", bac.cf2,
                 "--config-cf2", bac.cfg, "--piege-dir", bac.media,
                 "--conteneur", bac.cf3, "--phrase-stdin", stdin=PHRASE)
        _verifie("m9-migrer-code-0", r.code == 0)
        _verifie("m9-migrer-nomme-checksum-et-protocole",
                 "VERDICT : VERT" in r.out and "checksum" in r.out
                 and "detruire-cf2" in r.out
                 and "porte D120" in r.out)
        _verifie("m9-migrer-rien-à-traduire-dit",
                 "rien à traduire" in r.out)

        r = _cli("verifier", "--piege-dir", bac.media,
                 "--conteneur", bac.cf3, "--phrase-stdin", stdin=PHRASE)
        _verifie("m9-verifier-à-froid-code-0",
                 r.code == 0 and "VERDICT : VERT" in r.out)

        r = _cli("detruire-cf2", "--conteneur-cf2", bac.cf2,
                 "--conteneur", bac.cf3)
        _verifie("m9-detruire-cf2-sans-drapeau-refusé",
                 r.code != 0 and "--oui-je-comprends" in r.err)

        r = _cli("migrer", "--conteneur-cf2", bac.cf2,
                 "--config-cf2", bac.cfg, "--piege-dir", bac.media,
                 "--conteneur", bac.cf3, "--phrase-stdin", stdin=PHRASE)
        _verifie("m9-second-migrer-refusé-nommé",
                 r.code != 0 and "DÉJÀ PRÉSENT" in r.err)

        r = _cli("detruire-cf2", "--conteneur-cf2", bac.cf2,
                 "--conteneur", bac.cf3, "--oui-je-comprends")
        _verifie("m9-detruire-cf2-code-0",
                 r.code == 0 and "relève historique" in r.out)
        _verifie("m9-cf2-disparu-par-cli", not os.path.isfile(bac.cf2))
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------

def main() -> int:
    print("[test-migration] suite de falsifiabilité D127 — spec "
          "v06/I/CF3/README.md § 12 (cérémonie de migration CF2 → CF3)")
    for groupe in (m1_cycle_complet, m2_refus_nommes, m3_phrase,
                   m4_fragments_insuffisants, m5_porte_d120,
                   m6_orphelin_piege, m7_relecture_froide,
                   m8_detruire_cf2, m9_cli):
        groupe()
    echecs = [t for t, ok in RESULTATS if not ok]
    print(f"\n[test-migration] {len(RESULTATS) - len(echecs)} PASS / "
          f"{len(echecs)} ÉCHEC")
    if echecs:
        for temoin in echecs:
            print(f"  ÉCHEC : {temoin}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
