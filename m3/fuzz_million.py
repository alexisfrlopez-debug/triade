#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fuzz_million.py — Campagne million du jalon M3, étape (d) (D45→D46→D71).

Périmètre CONTRACTUEL (D46) : « http-01..09 + accumulation http-10 — le
périmètre du million ». Deux volets :

  VOLET FEUILLES (http-01..09) — différentiel pur. L'oracle (référence
  DÉRIVÉE DE LA COUCHE I, jamais de la notation) fournit les suites et les
  modèles ref_httpXX : le présent harnais n'est qu'un ORCHESTRATEUR. Il
  découpe la campagne en tranches — une suite = un émutateur NEUF, graine
  déterministe par (cible, tranche) — rattrape tout échec et le CONFIRME en
  re-exécutant la tranche (état vierge, même graine : un échec reproductible
  est un défaut réel ; un échec non reproductible est un artefact de
  réutilisation et reste consigné). AUCUNE logique de vérification n'est
  copiée : zéro dérive modèle possible.

  VOLET ACCUMULATION (http-10) — propriétés P1-P5 sur des flux de réceptions
  arbitraires : la surface où les octets non fiables s'accumulent dans le
  tampon de tête (MAX_TETE = 8192) et son corps borné Content-Length.
    P1 SURVIE      : aucune faute d'exécution (crash processus terrain) ;
    P2 TERMINAISON : la session rend la main dans le budget d'instructions ;
    P3 (sentinelles) : trois différentiels canoniques exacts — GET relayé,
                     déchet → 400 octet près, tête géante → 431 octet près ;
    P4 FERMETURES  : chaque socket fermée AU PLUS une fois, cliente toujours,
                     ordre amont→cliente (Q5), jamais l'écoute ni l'étrangère ;
    P5 MÉMOIRE     : crochet d'écriture — pages de code (.text/.text2)
                     interdites, pile profonde interdite (récursion folle),
                     getaddrinfo↔freeaddrinfo appariés un-pour-un.

  Générateurs nommés, déterministes par (graine, cible, indice) ; rejeu sur
  état vierge de tout échec ; rapport JSON traçable (m3/rapport_million.json).

  Auto-test (falsification du harnais — un oracle qui ne peut pas échouer ne
  prouve rien) : DEUX mutations D'UN OCTET de proxy.exe, détecteurs
  déterministes :
    M1 table des méthodes @0x16A0 (« GET »→« AET ») — la table EST la
       validation (http-02) : verdict divergent + sentinelle GET fautive ;
    M2 réponse 400 @0x1760 (« 400 »→« 500 ») — sentinelle déchet : l'émission
       cliente diverge du modèle octet près.

Usage :
  python3 m3/fuzz_million.py --calibration
  python3 m3/fuzz_million.py --auto-test
  python3 m3/fuzz_million.py --cas 1000000 --graine 20261028
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import struct
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import oracle_m3 as om

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX

# ---------------------------------------------------------------------------
# Constantes du harnais
# ---------------------------------------------------------------------------

PROXY = os.path.join(ICI, "proxy.exe")
RAPPORT_DEFAUT = os.path.join(ICI, "rapport_million.json")

SOCK_C, SOCK_A = om.SOCKET_CLIENTE, om.SOCKET_AMONT
RVA_HTTP10 = om._rva_depuis_spec("http-10")
BUDGET_SESSION = 20_000_000          # P2 : même budget que l'oracle (suite_sessions)
ENTREE_RSP = om.PILE_SOMMET - 0x10000     # rsp posé par executer_bloc
PLAFOND_PILE = ENTREE_RSP - 0x30000       # en dessous = récursion folle (marge 4x)
LIGNES_OK = ([om.LIGNE_CONNEXION, om.LIGNE_FIN],
             [om.LIGNE_CONNEXION, om.LIGNE_TUNNEL, om.LIGNE_FIN])

# Falsification : sites D'UN OCTET, uniques dans l'image (vérifiés au chargement)
SITE_METHODES = 0x16A0               # « GET\0HEAD\0… » — 1er octet 'G'→'A'
SITE_400 = 0x1760 + 9                # « HTTP/1.1 400 … » — le '4' du code
TETE_GET = b"GET /a HTTP/1.1\r\nHost: h\r\n\r\n"

SUITES = {
    "http-01": om.suite_http01, "http-02": om.suite_http02,
    "http-03": om.suite_http03, "http-04": om.suite_http04,
    "http-05": om.suite_http05, "http-06": om.suite_http06,
    "http-07": om.suite_http07, "http-08": om.suite_http08,
    "http-09": om.suite_http09,
}
CIBLES_FEUILLES = list(SUITES)


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def md5_hex(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()


# ---------------------------------------------------------------------------
# Volet accumulation — crochet mémoire (P5) et exécution d'un cas
# ---------------------------------------------------------------------------

def installer_crochet(em):
    """P5 : écritures interdites sur .text/.text2 (code) et pile profonde."""
    etat = {"violation": None}

    def crochet(uc, acces, adresse, taille, valeur, donnees):
        if etat["violation"] is not None:
            return
        rva = adresse - om.IMAGE
        if om.L.TEXT_RVA <= rva < om.L.TEXT_RVA + om.L.TEXT_VSIZE:
            etat["violation"] = f"écriture page de code .text @{rva:#x}"
        elif om.L.TEXT2_RVA <= rva < om.L.TEXT2_RVA + om.L.TEXT2_VSIZE:
            etat["violation"] = f"écriture page de code .text2 @{rva:#x}"
        elif om.PILE_BASE <= adresse < PLAFOND_PILE:
            etat["violation"] = (f"écriture pile profonde @{adresse - om.PILE_BASE:#x} "
                                 f"(plafond {PLAFOND_PILE - om.PILE_BASE:#x})")

    em.uc.hook_add(UC_HOOK_MEM_WRITE, crochet,
                   begin=om.IMAGE + om.L.TEXT_RVA,
                   end=om.IMAGE + om.L.TEXT_RVA + om.L.TEXT_VSIZE - 1)
    em.uc.hook_add(UC_HOOK_MEM_WRITE, crochet,
                   begin=om.IMAGE + om.L.TEXT2_RVA,
                   end=om.IMAGE + om.L.TEXT2_RVA + om.L.TEXT2_VSIZE - 1)
    em.uc.hook_add(UC_HOOK_MEM_WRITE, crochet,
                   begin=om.PILE_BASE, end=PLAFOND_PILE - 1)
    return etat


def nouvel_emulateur(exe):
    em = om.Emulateur(exe)
    etat = installer_crochet(em)
    return em, etat


def jouer_session(em, cas, etat_memoire):
    """Pose les scripts d'un cas et exécute http-10 ; retourne les fautes."""
    em.poser_scripts(recv={SOCK_C: list(cas["chunks"]), SOCK_A: list(cas["recv_amont"])},
                     send={SOCK_C: list(cas.get("caps_client", ())),
                           SOCK_A: list(cas.get("caps_amont", ()))},
                     getaddrinfo=list(cas.get("gai", [(0, [2])])),
                     connect=list(cas.get("connect", [0])))
    em.sortie_journal.clear()
    etat_memoire["violation"] = None
    fautes = []
    try:
        em.executer_bloc(RVA_HTTP10, (SOCK_C, 0, 0, 0), budget=BUDGET_SESSION)
    except om.EchecOracle as exc:
        return [f"P1/P2 {exc}"]
    # --- P4 : fermetures (Q5)
    ferm = list(em.fermetures)
    if len(ferm) != len(set(ferm)):
        fautes.append(f"P4 fermeture(s) dupliquée(s) {ferm}")
    if SOCK_C not in ferm:
        fautes.append(f"P4 socket cliente jamais fermée {ferm}")
    if any(s not in (SOCK_C, SOCK_A) for s in ferm):
        fautes.append(f"P4 fermeture étrangère {ferm}")
    if SOCK_A in ferm and SOCK_C in ferm and ferm.index(SOCK_A) > ferm.index(SOCK_C):
        fautes.append(f"P4 ordre violé {ferm} (Q5 : amont puis cliente)")
    # --- journal console : exactement les lignes du contrat http-10
    if list(em.sortie_journal) not in LIGNES_OK:
        fautes.append(f"journal console {em.sortie_journal!r} hors contrat")
    # --- P5 : mémoire
    if etat_memoire["violation"]:
        fautes.append(f"P5 {etat_memoire['violation']}")
    # --- nettoyage addrinfo un-pour-un (devoir tcp-13, déclenché par la session)
    gai = sum(1 for a in em.appels if a[0] == "getaddrinfo")
    if gai and em.nettoyages_addrinfo != gai:
        fautes.append(f"P5 getaddrinfo {gai} != freeaddrinfo {em.nettoyages_addrinfo}")
    # --- la session ne démonte jamais WSA (devoir de http-11/http-12)
    if any(a[0] == "WSACleanup" for a in em.appels):
        fautes.append("WSACleanup appelé par la session")
    return fautes


# --- sentinelles différentielles (P3 borné : trois formes canoniques) -------

def sentinelle_get(em, etat_memoire):
    """GET origine relayé : réécriture identité, réponse relayée, [amont, cliente]."""
    cas = {"chunks": [TETE_GET], "recv_amont": [b"RESP", 0]}
    em.poser_scripts(recv={SOCK_C: cas["chunks"], SOCK_A: cas["recv_amont"]},
                     getaddrinfo=[(0, [2])], connect=[0])
    em.sortie_journal.clear()
    etat_memoire["violation"] = None
    fautes = []
    try:
        em.executer_bloc(RVA_HTTP10, (SOCK_C, 0, 0, 0), budget=BUDGET_SESSION)
        om._verdict_session(em, journal=[om.LIGNE_CONNEXION, om.LIGNE_FIN],
                            client=b"RESP", amont=TETE_GET,
                            fermetures=[SOCK_A, SOCK_C])
    except om.EchecOracle as exc:
        fautes.append(f"sentinelle GET : {exc}")
    if etat_memoire["violation"]:
        fautes.append(f"sentinelle GET : P5 {etat_memoire['violation']}")
    return fautes


def sentinelle_dechet(em, etat_memoire):
    """Déchet d'un octet-variable : 400 exact, fermeture cliente seule."""
    cas = [b"\x01\x02\x03d\xe9chet\r\n\r\n"]
    em.poser_scripts(recv={SOCK_C: cas}, getaddrinfo=[(0, [2])], connect=[0])
    em.sortie_journal.clear()
    etat_memoire["violation"] = None
    fautes = []
    try:
        em.executer_bloc(RVA_HTTP10, (SOCK_C, 0, 0, 0), budget=BUDGET_SESSION)
        om._verdict_session(em, journal=[om.LIGNE_CONNEXION, om.LIGNE_FIN],
                            client=om.REPONSES[0], fermetures=[SOCK_C])
    except om.EchecOracle as exc:
        fautes.append(f"sentinelle déchet : {exc}")
    if etat_memoire["violation"]:
        fautes.append(f"sentinelle déchet : P5 {etat_memoire['violation']}")
    return fautes


def sentinelle_geante(em, etat_memoire):
    """Tête > 8192 avec terminateur : 431 exact, fermeture cliente seule."""
    cas = [b"GET / HTTP/1.1\r\nHost: h\r\nX-Pad: " + b"a" * 8200 + b"\r\n\r\n"]
    em.poser_scripts(recv={SOCK_C: cas}, getaddrinfo=[(0, [2])], connect=[0])
    em.sortie_journal.clear()
    etat_memoire["violation"] = None
    fautes = []
    try:
        em.executer_bloc(RVA_HTTP10, (SOCK_C, 0, 0, 0), budget=BUDGET_SESSION)
        om._verdict_session(em, journal=[om.LIGNE_CONNEXION, om.LIGNE_FIN],
                            client=om.REPONSES[1], fermetures=[SOCK_C])
    except om.EchecOracle as exc:
        fautes.append(f"sentinelle tête géante : {exc}")
    if etat_memoire["violation"]:
        fautes.append(f"sentinelle tête géante : P5 {etat_memoire['violation']}")
    return fautes


SENTINELLES = [sentinelle_get, sentinelle_dechet, sentinelle_geante]


# ---------------------------------------------------------------------------
# Générateurs du volet accumulation (nommés, déterministes par indice)
# ---------------------------------------------------------------------------

MAX_TETE = 8192                    # http-06 : la frontière du 431


def _fin(rng):
    return rng.choice([0, 0, 0, -1])


def gen_dechets(rng):
    """Octets uniformément aléatoires, découpe arbitraire, fin aléatoire."""
    chunks = [bytes(rng.getrandbits(8) for _ in range(rng.randint(0, 900)))
              for _ in range(rng.randint(1, 8))]
    chunks.append(_fin(rng))
    return {"chunks": chunks, "recv_amont": []}


def gen_tete_fragmentee(rng):
    """Tête valide découpée en fragments TCP de 1-7 octets."""
    tete = (b"GET /a/b?q=1 HTTP/1.1\r\nHost: h.example\r\n"
            b"X-Long: " + b"v" * rng.randint(0, 200) + b"\r\n\r\n")
    chunks, i = [], 0
    while i < len(tete):
        pas = rng.randint(1, 7)
        chunks.append(tete[i:i + pas])
        i += pas
    chunks.append(_fin(rng))
    return {"chunks": chunks, "recv_amont": [b"R", 0]}


def gen_tete_geante(rng):
    """Tête traversant la frontière MAX_TETE (7900-8600), fin incluse."""
    pad = rng.randint(7900, 8600)
    tete = (b"GET / HTTP/1.1\r\nHost: h\r\nX-Pad: " + b"a" * pad + b"\r\n\r\n")
    n = rng.randint(1, 4)
    taille = max(1, len(tete) // n)
    chunks = [tete[i:i + taille] for i in range(0, len(tete), taille)]
    chunks.append(_fin(rng))
    return {"chunks": chunks, "recv_amont": []}


def gen_corps_post(rng):
    """POST borné Content-Length : corps partiel, exact ou débordant."""
    cl = rng.randint(0, 50)
    corps = bytes(rng.getrandbits(8) for _ in range(rng.choice(
        [cl, max(0, cl - 1), cl + rng.randint(1, 20)])))
    tete = (b"POST /p HTTP/1.1\r\nHost: h\r\n"
            + b"Content-Length: " + str(cl).encode() + b"\r\n\r\n")
    morceaux = [tete]
    while corps:
        k = rng.randint(1, max(1, len(corps)))
        morceaux.append(corps[:k])
        corps = corps[k:]
    morceaux.append(_fin(rng))
    return {"chunks": morceaux, "recv_amont": [rng.choice([b"R", b""]), 0]}


def gen_connect_hostile(rng):
    """CONNECT : autorité variable, données montantes, fin parfois brutale."""
    autorite = rng.choice([b"h:443", b"h", b":443", b"[::1]:443", b"",
                           b"x" * rng.randint(1, 30)])
    ligne = b"CONNECT " + autorite + b" HTTP/1.1\r\n\r\n"
    chunks = [ligne[:rng.randint(0, len(ligne))] or ligne,
              ligne[rng.randint(0, len(ligne)):]] if rng.random() < 0.5 else [ligne]
    chunks = [c for c in chunks if c] or [ligne]
    if rng.random() < 0.6:
        chunks.append(bytes(rng.getrandbits(8) for _ in range(rng.randint(1, 100))))
    chunks.append(_fin(rng))
    return {"chunks": chunks, "recv_amont": [b"d", 0],
            "caps_amont": [rng.choice([-1, 1, 40])] if rng.random() < 0.3 else []}


def gen_fins_brutales(rng):
    """EOF/erreur immédiats ou après un ou deux octets."""
    choix = rng.random()
    if choix < 0.3:
        chunks = [rng.choice([0, -1])]
    elif choix < 0.6:
        chunks = [b"G", 0]
    else:
        chunks = [bytes(rng.getrandbits(8) for _ in range(rng.randint(1, 2))), -1]
    return {"chunks": chunks, "recv_amont": []}


def gen_caps_hostiles(rng):
    """GET valide mais émissions sabotées (cap -1 ou partielle, deux côtés)."""
    caps_c = [rng.choice([-1, rng.randint(0, 5)])] if rng.random() < 0.7 else []
    caps_a = [rng.choice([-1, rng.randint(0, 5)])] if rng.random() < 0.5 else []
    return {"chunks": [TETE_GET, _fin(rng)], "recv_amont": [b"RESP", 0],
            "caps_client": caps_c, "caps_amont": caps_a}


def gen_lignes_mutantes(rng):
    """Presque-valides : chaque défaut nommé de la couche I, un par cas."""
    tete = rng.choice([
        b"GET  / HTTP/1.1\r\nHost: h\r\n\r\n",              # double espace
        b"GET / HTTP/1.1\nHost: h\r\n\r\n",                 # LF isolé
        b"\r\nGET / HTTP/1.1\r\nHost: h\r\n\r\n",           # ligne vide d'abord
        b"GET / HTTP/1.1\r\nX-A: b\r\n\r\n",                # Host absent
        b"GET / HTTP/1.1\r\nHost: :80\r\n\r\n",             # autorité vide
        b"GET / HTTP/1.1\r\nbadline\r\nHost: h\r\n\r\n",    # en-tête invalide
        b"POST /p HTTP/1.1\r\nHost: h\r\nContent-Length: 007\r\n\r\n",
        b"FOO / HTTP/1.1\r\nHost: h\r\n\r\n",               # méthode inconnue
        b"GET https://h/ HTTP/1.1\r\nHost: h\r\n\r\n",      # https explicite
        b"GET / HTTP/2.0\r\nHost: h\r\n\r\n",               # version non sue
        b"GET /" + b"y" * 2048 + b" HTTP/1.1\r\nHost: h\r\n\r\n",  # cible 2049
        b"GET / HTTP/1.1\r\nHost: h\r\nTransfer-Encoding: chunked\r\n\r\n",
    ])
    n = rng.randint(1, 3)
    taille = max(1, len(tete) // n)
    chunks = [tete[i:i + taille] for i in range(0, len(tete), taille)]
    chunks.append(_fin(rng))
    return {"chunks": chunks, "recv_amont": [0]}


GENERATEURS_ACC = [
    ("dechets", gen_dechets),
    ("tete-fragmentee", gen_tete_fragmentee),
    ("tete-geante", gen_tete_geante),
    ("corps-post", gen_corps_post),
    ("connect-hostile", gen_connect_hostile),
    ("fins-brutales", gen_fins_brutales),
    ("caps-hostiles", gen_caps_hostiles),
    ("lignes-mutantes", gen_lignes_mutantes),
]


def cas_accumulation(graine: int, indice: int):
    """Cas déterministe par (graine, indice) — rejeu exact garanti."""
    rng = random.Random(f"M3million:{graine}:acc:{indice}")
    nom, gen = GENERATEURS_ACC[indice % len(GENERATEURS_ACC)]
    return nom, gen(rng)


# ---------------------------------------------------------------------------
# Auto-test — falsification déterministe du harnais
# ---------------------------------------------------------------------------

def _verifier_site(exe: bytes, offset: int, attendu: bytes, nom: str):
    if exe[offset:offset + len(attendu)] != attendu:
        raise SystemExit(f"auto-test : site {nom} divergent à {offset:#x} "
                         f"({exe[offset:offset + len(attendu)]!r} != {attendu!r})")


def auto_test(exe: bytes) -> dict:
    """Quatre détections déterministes : M1 (feuille + sentinelle), M2, témoin."""
    _verifier_site(exe, SITE_METHODES, b"GET\x00", "table des méthodes")
    _verifier_site(exe, SITE_400, b"4", "réponse 400")
    rapport = {"sites": {"M1_table_methodes": hex(SITE_METHODES),
                         "M2_reponse_400": hex(SITE_400)}}

    # --- témoin sauvage : les quatre contrôles passent sur l'artefact sain
    em, etat = nouvel_emulateur(exe)
    faute_temoin = (verifier_http02_direct(em, exe)
                    + sentinelle_get(em, etat)
                    + sentinelle_dechet(em, etat))
    rapport["temoin_sauvage"] = "PASS" if not faute_temoin else f"ÉCHEC {faute_temoin}"

    # --- M1 : « GET » -> « AET » dans la table (la table EST la validation)
    mutant = bytearray(exe)
    mutant[SITE_METHODES] = ord("A")
    m1 = bytes(mutant)
    em, etat = nouvel_emulateur(m1)
    d1 = verifier_http02_direct(em, m1)
    rapport["M1_feuille_http02"] = "DÉTECTÉ" if d1 else "NON DÉTECTÉ !"
    em, etat = nouvel_emulateur(m1)
    d2 = sentinelle_get(em, etat)
    rapport["M1_sentinelle_get"] = "DÉTECTÉ" if d2 else "NON DÉTECTÉ !"

    # --- M2 : « 400 » -> « 500 » dans la réponse du déchet
    mutant = bytearray(exe)
    mutant[SITE_400] = ord("5")
    m2 = bytes(mutant)
    em, etat = nouvel_emulateur(m2)
    d3 = sentinelle_dechet(em, etat)
    rapport["M2_sentinelle_dechet"] = "DÉTECTÉ" if d3 else "NON DÉTECTÉ !"

    ok = (rapport["temoin_sauvage"] == "PASS" and d1 and d2 and d3)
    rapport["verdict"] = ("PASS — le harnais détecte les défauts injectés"
                          if ok else "ÉCHEC — harnais aveugle !")
    return rapport


def verifier_http02_direct(em, exe):
    """Détection M1 déterministe : « GET / HTTP/1.1 » contre le modèle intact."""
    ligne = b"GET / HTTP/1.1"
    rva = om._rva_depuis_spec("http-02")
    ptr = om.poser_entree(em, ligne)
    zone = om.poser_zone(em, 56)
    fautes = []
    try:
        em.executer_bloc(rva, (ptr, len(ligne), zone))
        rax = em.uc.reg_read(UC_X86_REG_RAX)
        v_att, _ = om.ref_http02(ligne)
        if rax != v_att:
            fautes.append(f"http-02 verdict {rax} != {v_att} (table méthodes mutée)")
    except om.EchecOracle as exc:
        fautes.append(f"http-02 {exc}")
    return fautes


# ---------------------------------------------------------------------------
# Volet feuilles — orchestrateur de tranches (une suite = un émutateur neuf)
# ---------------------------------------------------------------------------

def volet_feuilles(exe, repartition, graine, tranche, verbeux):
    resultats = {}
    for cible in CIBLES_FEUILLES:
        n_total = repartition[cible]
        suite = SUITES[cible]
        fait, k, echecs, non_repro = 0, 0, [], []
        t0 = time.time()
        while fait < n_total:
            n = min(tranche, n_total - fait)
            graine_k = graine * 1_000_003 + k
            try:
                suite(exe, graine_k, n)
            except om.EchecOracle as exc:
                # confirmation : re-exécution de la tranche entière sur un
                # NOUVEL émutateur (créé dans la suite), même graine — un
                # échec reproductible est un défaut réel ; sinon artefact.
                try:
                    suite(exe, graine_k, n)
                    non_repro.append({"cible": cible, "tranche": k,
                                      "graine": graine_k, "erreur": str(exc)})
                except om.EchecOracle as exc2:
                    echecs.append({"cible": cible, "tranche": k, "graine": graine_k,
                                   "erreur": str(exc2)})
                    if verbeux:
                        print(f"  [ÉCHEC confirmé] {cible} tranche {k} : {exc2}")
            fait += n
            k += 1
            if verbeux and k % 10 == 0:
                dt = time.time() - t0
                print(f"  … {cible} : {fait}/{n_total} cas, {dt:.0f}s, "
                      f"{len(echecs)} échec(s) confirmé(s)")
        resultats[cible] = {"cas": fait, "tranches": k, "duree_s": round(time.time() - t0, 1),
                            "echecs_confirmes": len(echecs),
                            "echecs_non_reproductibles": len(non_repro)}
        print(f"[feuilles] {cible} : {fait} cas en {resultats[cible]['duree_s']}s "
              f"({fait / max(resultats[cible]['duree_s'], 0.001):.0f} cas/s) — "
              f"{len(echecs)} confirmé(s), {len(non_repro)} non reproductible(s)")
        resultats.setdefault("_detail_echecs", []).extend(echecs)
        resultats.setdefault("_detail_non_repro", []).extend(non_repro)
    return resultats


# ---------------------------------------------------------------------------
# Volet accumulation — propriétés P1-P5 par cas, rejeu sur état vierge
# ---------------------------------------------------------------------------

def volet_accumulation(exe, n_total, graine, lot, verbeux):
    t0 = time.time()
    echecs, non_repro, sent_ok, sent_total = [], [], 0, 0
    em, etat = None, None
    for i in range(n_total):
        if em is None or i % lot == 0:
            em, etat = nouvel_emulateur(exe)
        if i % 500 == 0:                      # sentinelle différentielle tournante
            f_sent = SENTINELLES[(i // 500) % len(SENTINELLES)](em, etat)
            sent_total += 1
            fautes = [f"[sentinelle {(i // 500) % len(SENTINELLES)}] {f}" for f in f_sent]
            nom = "sentinelle"
            contenu = {"forme": ["get", "dechet", "geante"][(i // 500) % 3]}
        else:
            nom, cas = cas_accumulation(graine, i)
            fautes = jouer_session(em, cas, etat)
            contenu = {"chunks": [f"{len(c)}o:{bytes(c)[:32].hex()}{'…' if len(c) > 32 else ''}"
                                  if not isinstance(c, int) else f"fin({c})"
                                  for c in cas["chunks"][:6]],
                       "recv_amont": list(map(str, cas["recv_amont"]))}
        if not fautes and nom == "sentinelle":
            sent_ok += 1
        if fautes:
            em2, etat2 = nouvel_emulateur(exe)
            if nom == "sentinelle":
                confirme = [f"[sentinelle] {f}" for f in
                            SENTINELLES[(i // 500) % len(SENTINELLES)](em2, etat2)]
            else:
                _, cas = cas_accumulation(graine, i)   # rejeu exact : même cas
                confirme = jouer_session(em2, cas, etat2)
            if confirme:
                echecs.append({"cas": i, "generateur": nom, "fautes": confirme,
                               "contenu": contenu})
                print(f"[ÉCHEC confirmé] accumulation cas {i} ({nom}) : {confirme}")
            else:
                non_repro.append({"cas": i, "generateur": nom, "fautes": fautes,
                                  "contenu": contenu})
        if verbeux and i and i % 500 == 0:
            dt = time.time() - t0
            print(f"  … accumulation : {i}/{n_total} cas, {dt:.0f}s, "
                  f"{len(echecs)} échec(s)")
    duree = round(time.time() - t0, 1)
    print(f"[accumulation] {n_total} cas en {duree}s "
          f"({n_total / max(duree, 0.001):.1f} cas/s) — {len(echecs)} confirmé(s), "
          f"{len(non_repro)} non reproductible(s), sentinelles {sent_ok}/{sent_total}")
    return {"cas": n_total, "duree_s": duree, "echecs_confirmes": len(echecs),
            "echecs_non_reproductibles": len(non_repro),
            "sentinelles": {"executions": sent_total, "ok": sent_ok},
            "_detail_echecs": echecs, "_detail_non_repro": non_repro}


# ---------------------------------------------------------------------------
# Campagne complète
# ---------------------------------------------------------------------------

def repartition_defaut(total, n_accum):
    feuilles = total - n_accum
    par_cible = feuilles // len(CIBLES_FEUILLES)
    rep = {c: par_cible for c in CIBLES_FEUILLES}
    rep["http-01"] += feuilles - par_cible * len(CIBLES_FEUILLES)   # reste
    rep["http-10-accumulation"] = n_accum
    return rep


def campagne(exe, total, n_accum, graine, tranche, lot, verbeux, avec_auto_test=True):
    rapport = {
        "harnais": "m3/fuzz_million.py",
        "etape": "M3-(d) campagne million",
        "date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "graine": graine,
        "artefact": {"fichier": "m3/proxy.exe", "octets": len(exe),
                     "md5": md5_hex(exe), "sha256": sha256_hex(exe)},
        "perimetre": "http-01..09 + accumulation http-10 (D46)",
        "tranche_feuilles": tranche, "lot_accumulation": lot,
        "repartition": repartition_defaut(total, n_accum),
    }
    if avec_auto_test:
        print("=== auto-test : falsification du harnais (mutations M1/M2) ===")
        rapport["auto_test"] = auto_test(exe)
        for k, v in rapport["auto_test"].items():
            if k != "sites":
                print(f"  {k} : {v}")
        if "ÉCHEC" in rapport["auto_test"]["verdict"]:
            return rapport, False
    if n_accum < total:                       # volet feuilles
        print(f"=== volet FEUILLES : {total - n_accum} cas différentiels, "
              f"tranches de {tranche} ===")
        res_f = volet_feuilles(exe, rapport["repartition"], graine, tranche, verbeux)
        rapport["feuilles"] = {k: v for k, v in res_f.items()
                               if not k.startswith("_")}
        rapport.setdefault("echecs_confirmes", []).extend(res_f.get("_detail_echecs", []))
        rapport.setdefault("echecs_non_reproductibles", []).extend(res_f.get("_detail_non_repro", []))
    if n_accum > 0:
        print(f"=== volet ACCUMULATION : {n_accum} cas à propriétés, "
              f"lots de {lot}, sentinelles tournantes ===")
        res_a = volet_accumulation(exe, n_accum, graine, lot, verbeux)
        rapport["accumulation"] = {k: v for k, v in res_a.items()
                                   if not k.startswith("_")}
        rapport.setdefault("echecs_confirmes", []).extend(res_a.get("_detail_echecs", []))
        rapport.setdefault("echecs_non_reproductibles", []).extend(res_a.get("_detail_non_repro", []))
    rapport["total_cas"] = total
    rapport["duree_totale_s"] = round(
        sum(r.get("duree_s", 0) for r in rapport.get("feuilles", {}).values())
        + rapport.get("accumulation", {}).get("duree_s", 0), 1)
    ok = not rapport.get("echecs_confirmes") and not rapport.get("echecs_non_reproductibles")
    rapport["verdict"] = (f"SANS CRASH — P1-P5 tenues sur {total:,} cas "
                          f"(périmètre D46)".replace(",", " ")
                          if ok else
                          f"{len(rapport.get('echecs_confirmes', []))} VIOLATION(S) confirmée(s), "
                          f"{len(rapport.get('echecs_non_reproductibles', []))} non reproductible(s)")
    return rapport, ok


# ---------------------------------------------------------------------------
# Calibration
# ---------------------------------------------------------------------------

def calibration(exe):
    print("=== calibration : cadence par cible (distribution million projetée) ===")
    rep = repartition_defaut(1_000_000, 10_000)
    durees = {}
    for cible in CIBLES_FEUILLES:
        t0 = time.time()
        SUITES[cible](exe, 20261028, 300)
        dt = time.time() - t0
        durees[cible] = dt
        proj = rep[cible] / max(300 / dt, 0.001)
        print(f"  {cible} : 300 cas en {dt:.2f}s → {300 / dt:.0f} cas/s ; "
              f"projeté {rep[cible]} cas ≈ {proj:.0f}s")
    t0 = time.time()
    volet_accumulation(exe, 30, 20261028, 30, False)
    dt = time.time() - t0
    proj = rep["http-10-accumulation"] / max(30 / dt, 0.001)
    print(f"  http-10-accumulation : 30 cas en {dt:.2f}s → {30 / dt:.1f} cas/s ; "
          f"projeté {rep['http-10-accumulation']} cas ≈ {proj:.0f}s "
          f"({proj / 60:.1f} min)")
    total_proj = sum(rep[c] / max(300 / durees[c], 0.001) for c in CIBLES_FEUILLES) + proj
    print(f"  TOTAL projeté ≈ {total_proj:.0f}s ({total_proj / 60:.1f} min) "
          f"pour 1 000 000 cas")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Campagne million M3 — étape (d)")
    ap.add_argument("--cas", type=int, default=1_000_000)
    ap.add_argument("--accum", type=int, default=10_000,
                    help="part du volet accumulation http-10")
    ap.add_argument("--graine", type=int, default=20261028)
    ap.add_argument("--tranche", type=int, default=2_000,
                    help="cas par tranche feuille (un émutateur par tranche)")
    ap.add_argument("--lot", type=int, default=250,
                    help="cas par émutateur d'accumulation")
    ap.add_argument("--calibration", action="store_true")
    ap.add_argument("--auto-test", action="store_true")
    ap.add_argument("--sans-auto-test", action="store_true")
    ap.add_argument("--verbeux", action="store_true")
    ap.add_argument("--rapport", default=RAPPORT_DEFAUT)
    args = ap.parse_args()

    with open(PROXY, "rb") as f:
        exe = f.read()

    if args.auto_test:
        res = auto_test(exe)
        for k, v in res.items():
            print(f"  {k} : {v}")
        return 0 if "ÉCHEC" not in res["verdict"] else 2
    if args.calibration:
        calibration(exe)
        return 0

    rapport, ok = campagne(exe, args.cas, args.accum, args.graine,
                           args.tranche, args.lot, args.verbeux,
                           avec_auto_test=not args.sans_auto_test)
    with open(args.rapport, "w", encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=2)
    print("=" * 70)
    print(f"BILAN : {rapport['total_cas']:,} cas en "
          f"{rapport.get('duree_totale_s', 0)}s".replace(",", " "))
    print(f"  échecs confirmés : {len(rapport.get('echecs_confirmes', []))}")
    print(f"  échecs non reproductibles : "
          f"{len(rapport.get('echecs_non_reproductibles', []))}")
    print(f"  rapport : {args.rapport}")
    print(f"VERDICT : {rapport['verdict']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
