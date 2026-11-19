#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""egalite_traces_hash_v190.py — L'INSTRUMENT TEMPS CONSTANT DURCI : LE HASH
DES TRACES COMPLÈTES (l'instruction 5ey7gmjra, point 3 : « hash des traces
COMPLÈTES (instructions + adresses + accès mémoire) par run, égalité des
hash entre classes secret-fixe/secret-aléatoire sur les 6 cibles (N=60/
classe, graine consignée) — le compte unique ne suffit plus comme preuve
d'égalité bit-identique »).

LA MÉTHODE — la promotion de l'instrument v180 (egalite_traces_v180.py,
la vague 5 : le COMPTE UNIQUE d'instructions) : chaque run porte DORSENAVANT
un hachage INCRÉMENTAL de sa trace COMPLÈTE —
  — chaque instruction exécutée : (l'adresse, la taille) ;
  — chaque accès mémoire de DONNÉES : (le type lecture/écriture, l'adresse,
    la taille) — les VALEURS ne sont JAMAIS hachées (le secret diffère par
    construction : c'est l'ACCÈS, pas la valeur, qui fait la divulgation) ;
l'égalité exigée : les 120 condensats (60 secret-fixe + 60 secret-aléatoire)
BIT-IDENTIQUES — UN SEUL hash distinct par cible : la preuve d'égalité
bit-identique des traces, PLUS la preuve de compte (le hash subsume le
compte : deux traces de longueurs différentes ont des hash différents).

LES 6 CIBLES — les MÊMES protocoles que v180 (les entrées, les tailles,
les appels) : sha-256 (tls13-01..04, le message), hmac-sha256 (tls13-05,
la clé), hkdf-extract (tls13-06, l'IKM), x25519 (tls13-13/14, la clé
privée — le compte consigné 1 238 959), aes-gcm (tls13-15..19, la clé),
md5 loupe (loupe-06, le contenu du fichier) — le clone PUBLIC du dépôt
(https://github.com/alexisfrlopez-debug/triade, anonyme : la preuve du
« quiconque clone », D220).

LA GRAINE CONSIGNÉE : 20261119 (la session) — les secrets aléatoires tirés
de random.Random((GRAINE, cible, classe, run)), le rejeu la reproduit.

Usage : egalite_traces_hash_v190.py --cible CIBLE [--debut 0] [--fin 120]
        egalite_traces_hash_v190.py --bilan
Les runs écrivent une ligne par run à traces_hash_v190.jsonl ; le --bilan
agrège et tranche (le rapport + le CSV).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import pathlib
import random
import sys

REPO = pathlib.Path("/tmp/triade-gh")
ATELIER = pathlib.Path(__file__).resolve().parent
SORTIE_JSONL = ATELIER / "traces_hash_v190.jsonl"

GRAINE = 20261119
N = 60                    # répétitions par classe (le protocole v180)
X25519_COMPTE_ATTENDU = 1_238_959   # le compte consigné au manuscrit

CIBLES = ["sha", "hmac", "hkdf", "x25519", "aead", "loupe"]


def charger_module(nom: str, chemin: pathlib.Path):
    sys.path.insert(0, str(chemin.parent))
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# LE TRACEUR : le hash incrémental des événements (code + données)
# ---------------------------------------------------------------------------

class Traceur:
    """Les crochets Unicorn nourrissent le sha256 incrémental — les
    événements : C(adresse, taille) par instruction ; M(type, adresse,
    taille) par accès mémoire de données. Les valeurs JAMAIS."""

    def __init__(self, emul):
        from unicorn import (UC_HOOK_CODE, UC_HOOK_MEM_READ,
                             UC_HOOK_MEM_WRITE)
        self.h = hashlib.sha256()
        self.actif = False
        self.n_events = 0
        self._buf = bytearray()

        def crochet_code(uc, adresse, taille, donnees):
            if self.actif:
                self._buf += b"C" + adresse.to_bytes(8, "little") \
                             + taille.to_bytes(1, "little")
                self.n_events += 1

        def crochet_mem(uc, acces, adresse, taille, valeur, donnees):
            if self.actif:
                self._buf += b"M" + bytes([acces & 0xFF]) \
                             + adresse.to_bytes(8, "little") \
                             + taille.to_bytes(1, "little")
                self.n_events += 1

        emul.uc.hook_add(UC_HOOK_CODE, crochet_code)
        emul.uc.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, crochet_mem)

    def commencer(self):
        self.h = hashlib.sha256()
        self._buf = bytearray()
        self.n_events = 0
        self.actif = True

    def _vider(self):
        if self._buf:
            self.h.update(bytes(self._buf))
            self._buf = bytearray()

    def clore(self) -> tuple[str, int]:
        self.actif = False
        self._vider()
        return self.h.hexdigest(), self.n_events


# ---------------------------------------------------------------------------
# les protocoles des 6 cibles — LES MÊMES que v180, le traceur en plus
# ---------------------------------------------------------------------------

def protocol_sha(hsha, traceur_unused, secret, rng):
    emul = hsha.Emulation()
    t = Traceur(emul)
    t.commencer()
    hsha.hacher(emul, secret, compter=True)
    d, n = t.clore()
    return d, n, emul.compteur


def protocol_hmac(hhkdf, traceur_unused, secret, rng):
    emul = hhkdf.Emulation()
    t = Traceur(emul)
    t.commencer()
    hhkdf.hmac_sha(emul, secret, b"message", compter=True)
    d, n = t.clore()
    return d, n, emul.compteur


def protocol_hkdf(hhkdf, traceur_unused, secret, rng):
    emul = hhkdf.Emulation()
    t = Traceur(emul)
    t.commencer()
    hhkdf.hkdf_extraire(emul, b"\x0b" * 22, secret, compter=True)
    d, n = t.clore()
    return d, n, emul.compteur


def protocol_x25519(hx, traceur_unused, secret, rng):
    emul = hx.Emulation()
    t = Traceur(emul)
    t.commencer()
    hx.cle_publique(emul, secret, compter=True)
    d, n = t.clore()
    return d, n, emul.compteur


def protocol_aead(ha, traceur_unused, secret, rng):
    emul = ha.Emulation()
    t = Traceur(emul)
    t.commencer()
    ha.sceller(emul, secret, bytes(range(12)),
               b"secret constant " * 4, b"", compter=True)
    d, n = t.clore()
    return d, n, emul.compteur


def protocol_loupe(hn, L, proxy_exe, selftest_exe, secret, rng):
    os_v = hn.OSVirtuel()
    os_v.declarer("cible.bin", hn.FichierVirtuel(contenu=secret))
    emul = hn.Emulation(os_v)
    emul.poser_heritages(proxy_exe, selftest_exe)
    t = Traceur(emul)
    t.commencer()
    emul.uc.mem_write(hn.ADRESSE_CHEMIN,
                      "cible.bin".encode("utf-16-le") + b"\x00\x00")
    emul.appeler(hn.L.LOUPE01_VA, {"rcx": hn.ADRESSE_CHEMIN})
    emul.appeler(hn.L.LOUPE06_VA,
                 {"rcx": 0, "rdx": len(secret), "r8": hn.ADRESSE_SORTIE16})
    emul.appeler(hn.L.LOUPE03_VA, {})
    return t.clore() + (0,)


# ---------------------------------------------------------------------------
# le pilote des runs
# ---------------------------------------------------------------------------

def faire_runs(cible: str, debut: int, fin: int) -> int:
    """Les runs [debut, fin) de la cible : l'index i < 60 = secret-fixe,
    i >= 60 = secret-aléatoire (le tirage (GRAINE, cible, classe, run))."""
    if cible == "sha":
        hsha = charger_module("h_sha_th", REPO / "tls13" / "harnais_sha.py")
        fixe = bytes.fromhex("ab") * 55

        def un_run(i):
            if i < N:
                secret = fixe
            else:
                rng = random.Random(f"{GRAINE}:{cible}:alea:{i}")
                secret = bytes(rng.randrange(256) for _ in range(55))
            return protocol_sha(hsha, None, secret, None)
    elif cible == "hmac":
        hhkdf = charger_module("h_hkdf_th", REPO / "tls13" / "harnais_hkdf.py")
        fixe = b"\x0b" * 32

        def un_run(i):
            if i < N:
                secret = fixe
            else:
                rng = random.Random(f"{GRAINE}:{cible}:alea:{i}")
                secret = bytes(rng.randrange(256) for _ in range(32))
            return protocol_hmac(hhkdf, None, secret, None)
    elif cible == "hkdf":
        hhkdf = charger_module("h_hkdf_th2", REPO / "tls13" / "harnais_hkdf.py")

        def un_run(i):
            if i < N:
                secret = b"\x00" * 22
            else:
                rng = random.Random(f"{GRAINE}:{cible}:alea:{i}")
                secret = bytes(rng.randrange(256) for _ in range(22))
            return protocol_hkdf(hhkdf, None, secret, None)
    elif cible == "x25519":
        hx = charger_module("h_x25519_th", REPO / "tls13" / "harnais_x25519.py")
        fixe = bytes.fromhex(
            "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")

        def un_run(i):
            if i < N:
                secret = fixe
            else:
                rng = random.Random(f"{GRAINE}:{cible}:alea:{i}")
                secret = bytes(rng.randrange(256) for _ in range(32))
            return protocol_x25519(hx, None, secret, None)
    elif cible == "aead":
        ha = charger_module("h_aead_th", REPO / "tls13" / "harnais_aead.py")
        fixe = bytes(range(16))

        def un_run(i):
            if i < N:
                secret = fixe
            else:
                rng = random.Random(f"{GRAINE}:{cible}:alea:{i}")
                secret = bytes(rng.randrange(256) for _ in range(16))
            return protocol_aead(ha, None, secret, None)
    elif cible == "loupe":
        hn = charger_module("h_noyau_th", REPO / "loupe" / "harnais_noyau.py")
        proxy = (REPO / "tls13" / "proxy.exe").read_bytes()
        selftest = (REPO / "m1" / "selftest.exe").read_bytes()
        fixe = b"A" * 1000

        def un_run(i):
            if i < N:
                secret = fixe
            else:
                rng = random.Random(f"{GRAINE}:{cible}:alea:{i}")
                secret = bytes(rng.randrange(256) for _ in range(1000))
            d, n, _ = protocol_loupe(hn, None, proxy, selftest, secret, None)
            return d, n, 0
    else:
        raise SystemExit(f"[ROUGE] cible inconnue {cible}")

    lignes = 0
    with open(SORTIE_JSONL, "a", encoding="utf-8") as f:
        for i in range(debut, min(fin, 2 * N)):
            digest, n_events, compte = un_run(i)
            f.write(json.dumps({
                "cible": cible, "run": i, "classe": "fixe" if i < N else "alea",
                "hash": digest, "events": n_events, "compte": compte})
                + "\n")
            lignes += 1
            print(f"[{cible}] run {i:>3} ({'fixe' if i < N else 'alea'}) : "
                  f"{n_events:>9} événements, hash {digest[:16]}…",
                  flush=True)
    print(f"[VERT] {lignes} runs écrits à {SORTIE_JSONL.name}")
    return 0


# ---------------------------------------------------------------------------
# le bilan : l'égalité des hash (UN seul distinct par cible, 120 mesures)
# ---------------------------------------------------------------------------

NOMS = {"sha": "tls13-01..04 (sha-256, le message)",
        "hmac": "tls13-05 (hmac-sha256, la clé)",
        "hkdf": "tls13-06 (hkdf-extract, l'IKM)",
        "x25519": "tls13-13/14 (x25519, la clé privée)",
        "aead": "tls13-15..19 (aes-gcm, la clé)",
        "loupe": "loupe-06 (md5, le contenu)"}


def bilan() -> int:
    runs = [json.loads(l) for l in
            SORTIE_JSONL.read_text(encoding="utf-8").splitlines() if l]
    lignes = []
    ok_global = True
    with open(ATELIER / "traces_hash_v190.csv", "w", newline="",
              encoding="utf-8") as fcsv:
        w = csv.DictWriter(fcsv, fieldnames=[
            "cible", "n_fixe", "n_alea", "hashes_distincts", "hash_unique",
            "events", "compte_unique", "egalite_hash", "x25519_confirme"])
        w.writeheader()
        for cible in CIBLES:
            rs = [r for r in runs if r["cible"] == cible]
            if not rs:
                continue
            fixe = [r for r in rs if r["classe"] == "fixe"]
            alea = [r for r in rs if r["classe"] == "alea"]
            hashes = {r["hash"] for r in rs}
            events = {r["events"] for r in rs}
            compte = {r["compte"] for r in rs}
            egalite = (len(fixe) == N and len(alea) == N
                       and len(hashes) == 1)
            ligne = {"cible": cible, "n_fixe": len(fixe), "n_alea": len(alea),
                     "hashes_distincts": len(hashes),
                     "hash_unique": next(iter(hashes)) if len(hashes) == 1
                     else "",
                     "events": f"{min(events)}..{max(events)}",
                     "compte_unique": str(next(iter(compte)))
                     if len(compte) == 1 else f"{len(compte)} distincts",
                     "egalite_hash": egalite, "x25519_confirme": ""}
            if cible == "x25519":
                attendu = compte == {X25519_COMPTE_ATTENDU}
                ligne["x25519_confirme"] = attendu
                egalite = egalite and attendu
            w.writerow(ligne)
            detail = (f"{len(fixe)}+{len(alea)} runs, {len(hashes)} hash "
                      f"distinct, {min(events)}-{max(events)} événements, "
                      f"le compte {'==' if len(compte) == 1 else '≠'} unique"
                      + (f", le compte {next(iter(compte)):,} == 1 238 959"
                         .replace(",", " ")
                         if cible == "x25519" and len(compte) == 1 else ""))
            lignes.append(f"  {NOMS[cible]:<40s} → "
                          f"{'ÉGALITÉ HASH-VÉRIFIÉE' if egalite else 'DIVERGENCE'}"
                          f" — {detail}")
            ok_global &= egalite

    rapport = [
        "L'ÉGALITÉ DES TRACES COMPLÈTES PAR HASH — L'INSTRUMENT DURCI "
        "DE L'INSTRUCTION 5ey7gmjra (v0.19.0)",
        f"  (les 6 cibles de l'instrument v180, N={N}/classe, la graine "
        f"consignée {GRAINE} ; le hash incrémental par run : chaque "
        "instruction (adresse, taille) + chaque accès de données (type, "
        "adresse, taille) — les VALEURS jamais hachées)",
        "",
    ] + lignes + [
        "",
        "LA PROMOTION : le compte unique (v180) demeure CONTENU dans le "
        "hash — deux traces de longueurs différentes ont des hash "
        "différents ; l'égalité des 120 condensats par cible est la "
        "preuve d'égalité BIT-IDENTIQUE des traces complètes : le flot "
        "d'exécution ET le patron d'accès mémoire, indépendants du "
        "secret — PLUS une divulgation de type adresse-ou-contrôle.",
        "",
        ("VERDICT : VERT — l'égalité hash-vérifiée sur les 6 cibles, le "
         "compte x25519 confirmé" if ok_global else
         "VERDICT : ROUGE — une divergence nommée, le refus s'impose"),
    ]
    (ATELIER / "RAPPORT-TRACES-HASH-V190.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))
    return 0 if ok_global else 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cible", choices=CIBLES)
    ap.add_argument("--debut", type=int, default=0)
    ap.add_argument("--fin", type=int, default=2 * N)
    ap.add_argument("--bilan", action="store_true")
    args = ap.parse_args()
    if args.bilan:
        return bilan()
    if not args.cible:
        raise SystemExit("[ROUGE] --cible requis (ou --bilan)")
    return faire_runs(args.cible, args.debut, args.fin)


if __name__ == "__main__":
    sys.exit(main())
