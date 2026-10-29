#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_m4.py — Oracle à scénarios SSPI du jalon M4 (D93).

L'oracle des ORCHESTRATEURS, comme promis par le plan d'adressage (« source
unique de vérité partagée par build_m4.py, outils/auteur.py et oracle_m4.py »)
et par la surface de vérification arrêtée D77 : « orchestrateurs à l'oracle à
scénarios (compensation par comptage) » — les feuilles et boucles relèvent des
harnais P1-P5 (D79-D90), l'anti-régression inter-jalons du différentiel
d'ancêtre relève des harnais de révision (D91/D92). L'oracle GÉNÈRE des
scénarios hostiles par graine (générateurs d'HRESULT — table TOTALE tls-02 :
listes blanches, codes exacts, exotiques hors domaine) et confronte le MODÈLE
(dérivé de la couche I, jamais de la notation) à l'ÉMULATION (les octets réels
des notations, chaîne complète) :

  F1  session tls-08 à volume hostile — le cœur « générateurs d'HRESULT
      hostiles + compensation PAR COMPTAGE » : poignées multi-allers (CONT à
      jetons variables, INCOMPLET qui reçoit, CERT/échec/exotique en
      terminaison, E5 interminable), acquisitions en échec (ACH fatal 6),
      tailles de flux négociées aléatoires (jamais maxmsg = 0 : la découpe
      mourrait), émissions chiffrées fragmentées, relais à lots, drains,
      altérations, densités « max », libérations E4 (ressaisie unique) —
      CHAQUE scénario confronte Modele (D90, spec tls-08:R1) à l'émulation 18
      blocs : verdict rax, cadre 0xD000 OCTET PAR OCTET, contrat d'appels
      complet (comparer_traces), comptes de compensation, paquet INTACT ;

  F2  routage http-10:R2 — le modèle de routage D93 (dérivé de P6/Q2'/Q3' de
      la spec http-10:R2) contre l'émulation 29 blocs : requêtes https
      générées (autorité, port implicite 443 / EXPLICITE qui gagne, chemin /
      query / fixture « / », fragmentation d'accumulation 1-3 réceptions,
      méthodes, POST CL:0) × scripts SSPI hostiles, PLUS les arrêts
      contractuels D92 (corps CL>0 → 501, Transfer-Encoding → 501, POST sans
      longueur → 411, autorité vide → 400, HTTPS:// mal cassé → 501, pair
      parti → silence) — chaque scénario vérifie la réponse EXACTE au client
      (octets de la table Q3' — l'entrée étiquetée comprise), les lignes
      console EXACTES (connexion / tunnel chiffre etabli / certificat rejete
      UNE FOIS / fin), la compensation croisée PAR COMPTAGE (ACH/DSC/FCH/
      CLOSESOCKET + socket cliente R1), le PAQUET au passage de tls-08 (P6 :
      hôte, port, requête réécrite forme origine, socket cliente) et le CADRE
      TLS VIERGE ; la concordance I est croisée à CHAQUE scénario : le
      verdict de routage attendu est confirmé par modele_cible (D91, dérivé
      de la spec http-08:R2) sur la cible générée ;

  F3  différentiel d'ancêtre à volume (R7 — l'anti-régression comportementale
      du domaine scellé) : requêtes mixtes générées (http absolu / origine /
      CONNECT / malformées héritage 400-431-505-501-411 / https) — l'ancêtre
      http-10:R3 scellé (0.4.0, carte génération 5) et la révision émulés sur
      les MÊMES entrées : écart ZÉRO hors domaine https ; dans le domaine
      https byte-exact, l'ancêtre refuse 501 et la révision route — TOUT
      autre écart serait une régression de l'héritage scellé ;

  F4  falsification — l'oracle DOIT pouvoir échouer (une suite qui ne peut
      pas échouer ne prouve rien) : mutations d'un point extraites des harnais
      D90/D92 (tls-08 ET http-10:R2) ATTRAPÉES sur les selections fixes ;
      le MODÈLE falsifié (octets au client maquillés) nommé par la
      confrontation ; le témoin intact reste vert.

Le modèle de routage (ModeleRoutage) prédit le domaine TLS par construction ;
l'héritage http non TLS (accumulation, parsing, relais, CONNECT) n'est PAS
remodélisé ici — il est scellé 0.4.0 et couvert par F3 (l'ancêtre ÉMULÉ est la
référence, R7 — le même arbitrage que l'oracle M3 pour ses scénarios
scriptés, prolongé en volume). Réutilisation stricte : Modele/Emulateur/
Script/comparer_traces/compter_compensation (harnais_session D90),
EmulateurSession/ScriptR2/differentiel/charger (harnais_session_r2 D92),
modele_cible (harnais_cible_r2 D91) — JAMAIS deux sources de vérité.

Usage : python3 oracle_m4.py [--graine G] [--volume complet|reduit]
   (et depuis build_m4.py : executer(blobs, graine, volume))
"""

from __future__ import annotations

import argparse
import hashlib
import os
import random
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, "outils"))
import layout as L  # noqa: E402

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

import harnais_session as HS  # noqa: E402 — le harnais D90 (tls-08), source des shims
import harnais_session_r2 as SR2  # noqa: E402 — le harnais D92 (http-10:R2), sous-classé
import harnais_cible_r2 as CR2  # noqa: E402 — le modèle http-08:R2 (D91, dérivé de I)

from harnais_session import (  # noqa: E402
    Script, Modele, Emulateur, jouer_scenario, compter_compensation,
    octets_notation, motif, clair_dm, permuter16,
    OK, CONT, INCOMPLET, CONTEXTE_EXPIRE, ALTERE, CERT_INVALIDE,
    INVALID_TOKEN, INVALID_HANDLE, EXOTIQUE,
    SOCKET_CLIENT, SOCKET_SERVEUR, HOTE_DEFAUT, REQUETE_DEFAUT,
    CANARI, ZONE_PAQUET, TAILLE_PAQUET,
)


class EchecOracle(Exception):
    """Tout écart entre le modèle (dérivé de I) et l'émulation."""


# --- Les réponses héritage M3 (textes consignés m3/layout.py, R7) -----------------

TXT_400 = SR2.TXT_400
TXT_411 = SR2.TXT_411
TXT_501 = SR2.TXT_501
TXT_502 = SR2.TXT_502
CONN, FIN = SR2.MSG_CONNEXION, SR2.MSG_FIN
ETABLI, CERTL = L.TXT_TLS_ETABLI, L.TXT_TLS_CERT

# HRESULT hostiles par famille (tls-02 — liste blanche vérifiée D79 + exotiques)
CERTS = [0x80090325, 0x80090328, 0x80090327, 0x80090349, 0x80090322]   # verdict 3
ECHECS = [0x80090308, 0x80090330, 0x8009030F, 0x80090310]              # verdict 5
EXOTIQUES = [0x81234567, 0x00000001, 0x7FFFFFFF, 0x80000000]           # verdict 6


# ============================================================================
# Le cœur générateur d'HRESULT hostiles — PARTAGÉ F1/F2 (jamais deux sources)
# ============================================================================

def _generer_sspi(alea: random.Random) -> dict:
    """Les listes hostiles du script SSPI. TERMINATION PAR CONSTRUCTION :
    la poignée est bornée par la garde E5 (16 allers) ; chaque cycle .relais
    consomme UNE entrée recv (liste finie à terminateur ≤ 0) ; chaque chaîne
    de drain fait décroître strictement le lot ; les défauts de listes sont
    bornés par les MÊMES règles côté modèle et émulation (jamais deux
    sources). maxmsg >= 1 TOUJOURS : une découpe à message nul mourrait."""
    gai = [0x2AFA] if alea.random() < 0.10 else []
    socket_ = [-1] if alea.random() < 0.04 else []
    connect = [-1] if alea.random() < 0.05 else []
    ach = alea.choice([0] * 12 + [INVALID_HANDLE])
    # la poignée : 0..5 CONT à jetons variables, puis une terminaison nommée —
    # le SUCCÈS est majoritaire (le chemin profond — relais, drains,
    # compensation intégrale — est là que les contrats vivent ; les échecs
    # nommés restent couverts, en minorité)
    isc = [(CONT, alea.randint(0, 512)) for _ in range(alea.randint(0, 5))]
    poids = ([OK] * 13 + CERTS + ECHECS + EXOTIQUES[:1] + [INCOMPLET] * 2)
    isc.append((alea.choice(poids), alea.randint(0, 256)))
    if alea.random() < 0.05:                # la poignée interminable — E5
        isc = [(CONT, 8)] * 16
    # tailles de flux négociées (tls-06 lit le NÉGOCIÉ — jamais une constante)
    tailles = (alea.randint(0, 32), alea.randint(0, 32),
               alea.choice([64, 128, 512, 2048]), 4, 8)
    qca = [(alea.choice([0] * 18 + EXOTIQUES[:2]), tailles)]
    em = ([alea.choice(ECHECS + EXOTIQUES)] if alea.random() < 0.10 else []) + [0] * 8
    # le relais : lots, drains, incomplets, altérations — termine TOUJOURS
    dm = []
    for _ in range(alea.randint(1, 5)):
        r = alea.random()
        if r < 0.55:
            dm.append((OK, alea.randint(0, 16), alea.randint(1, 512),
                       alea.randint(0, 16)))
        elif r < 0.70:
            dm.append((INCOMPLET, 5, 100, 16))
        elif r < 0.78:
            dm.append((alea.choice(ECHECS + EXOTIQUES), 5, 100, 16))
        elif r < 0.86:      # densité : le clair déborde le lot (la pompe suit)
            dm.append((OK, alea.randint(0, 16), alea.randint(512, 2048),
                       alea.randint(0, 16)))
        else:                # le clair pompe petit, le résidu grossit
            dm.append((OK, 0, 0, alea.randint(1, 64)))
    dm.append(alea.choice([(CONTEXTE_EXPIRE, 5, 0, 16),
                           (CONTEXTE_EXPIRE, 5, 0, 16),
                           (alea.choice(ECHECS + EXOTIQUES), 5, 100, 16)]))
    recv = []
    for _ in range(alea.randint(0, 6)):
        r = alea.random()
        if r < 0.10:
            recv.append("max")              # densité hostile — la chambre pleine
        else:
            recv.append(alea.randint(1, 600))
    recv.append(alea.choice([0, 0, 0, -1]))  # fermeture système / erreur
    send = []
    for _ in range(alea.randint(0, 6)):
        r = alea.random()
        if r < 0.60:
            send.append("plein")
        elif r < 0.93:                         # émission partielle — l'achèvement
            send.append(alea.randint(1, 64))
        else:                                  # le pair est parti (rare : la
            send.append(-1)                    # poignée émettant souvent, un
                                              # échec tuerait la session entière)
    dsc = [INVALID_HANDLE] if alea.random() < 0.12 else []   # E4 : UNE ressaisie
    fch = ([INVALID_HANDLE] * alea.randint(1, 2) if alea.random() < 0.10 else [])
    return {"gai": gai, "socket_": socket_, "connect": connect, "ach": ach,
            "isc": isc, "qca": qca, "em": em, "dm": dm, "recv": recv,
            "send": send, "dsc": dsc, "fch": fch}


def _hote(alea: random.Random) -> bytes:
    """88 % ASCII routable, 6 % octet >= 0x80 (tls-01 refus 2 → verdict 7),
    6 % hors borne HOTE_MAX (refus 1 → verdict 7) — les branches nommées
    restent couvertes sans étouffer le chemin profond."""
    r = alea.random()
    if r < 0.06:
        return b"ex" + bytes([alea.randint(0x80, 0xFF)]) + b"mple.fr"
    if r < 0.12:
        return b"h" + b"x" * alea.randint(255, 300) + b".fr"
    n = alea.randint(1, 48)
    return bytes(alea.choice(b"abcdefghijklmnopqrstuvwxyz0123456789-.")
                 for _ in range(n))


def _requete(alea: random.Random) -> bytes:
    """GET forme origine (l'entrée CLAIRE de tls-06, 20..180 o)."""
    chemin = b"/" + bytes(alea.choice(b"abcdefghij0123456789-_./")
                           for _ in range(alea.randint(1, 40)))
    return b"GET " + chemin + b" HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"


# ============================================================================
# F1 — session tls-08 à volume hostile (compensation PAR COMPTAGE)
# ============================================================================

def confronter_session(emu: Emulateur, script: Script, hote: bytes,
                       requete: bytes, port: int) -> tuple[list[str], int]:
    """Modele (spec tls-08:R1, D90) contre l'émulation 18 blocs — écarts
    nommés : rax, cadre octet par octet, contrat d'appels complet, comptes de
    compensation, paquet INTACT (le clair de l'appelant jamais touché)."""
    rax_att, appels_att, _image, problemes = jouer_scenario(
        emu, script, hote, requete, port)
    if compter_compensation(emu.appels) != compter_compensation(appels_att):
        problemes.append("comptes de compensation modèle/émulation divergent "
                         f"{compter_compensation(emu.appels)} != "
                         f"{compter_compensation(appels_att)}")
    paquet_lu = bytes(emu.uc.mem_read(ZONE_PAQUET, TAILLE_PAQUET))
    # limite de layout du paquet de TEST (D90 : hôte @0x100, requête @0x200) :
    # un hôte de plus de 0x100 octets y recouvrirait la zone requête — la garde
    # tls-01 (HOTE_MAX, verdict 7) est atteinte avant, seul le préfixe est
    # vérifié (le recouvrement est l'artefact du harnais, jamais de la notation)
    limite = min(len(hote), 0x100)
    if (paquet_lu[0x100:0x100 + limite] != hote[:limite]
            or paquet_lu[0x200:0x200 + len(requete)] != requete
            or paquet_lu[0x30:0x100] != CANARI * (0x100 - 0x30)):
        problemes.append("paquet altéré (hôte/requête/canaris)")
    return problemes, rax_att


def famille_session(emu: Emulateur, graine: int, n: int) -> tuple[int, list]:
    alea = random.Random(graine * 100003 + 1)
    cas, ecarts = 0, []
    for i in range(n):
        sspi = _generer_sspi(alea)
        script = Script(**sspi)
        hote, requete = _hote(alea), _requete(alea)
        port = alea.choice([443, 443, alea.randint(1, 65535)])
        problemes, _rax = confronter_session(emu, script, hote, requete, port)
        cas += 1
        if problemes:
            ecarts.append((i, f"hôte {hote[:16]!r}", problemes[:3]))
    return cas, ecarts


# ============================================================================
# F2 — le modèle de routage http-10:R2 (dérivé de I : P6/Q2'/Q3', D92)
# ============================================================================

class ModeleClient(Modele):
    """Modele (tls-08, D90) + la capture des octets EFFECTIVEMENT émis au
    client — miroir du SEND-à-contenu du harnais R2 : le _pomper est repris
    TEL QUEL avec la capture en plus (la conformité au parent est constatée
    par comparer_traces en F1 : mêmes appels SEND socket/pointeur/longueur —
    jamais deux sources)."""

    def __init__(self, script: Script, hote: bytes, requete: bytes, port: int):
        super().__init__(script, hote, requete, port)
        self.client_envoye = bytearray()

    def _pomper(self, span_ptr: int, span_len: int) -> None:
        if span_len == 0:
            return                             # span VIDE : jamais tcp-04 à 0 (P3)
        contenu = clair_dm(self.i_dm - 1, span_len)
        envoye = 0
        while envoye < span_len:
            r = self.script.comportement_send(self.i_send, span_len - envoye)
            self.appels.append(("SEND", SOCKET_CLIENT, span_ptr + envoye,
                                span_len - envoye))
            self.i_send += 1
            if r <= 0:
                raise HS._Fin()                # le client est parti — Q1
            prise = min(r, span_len - envoye)
            self.client_envoye += contenu[envoye:envoye + prise]
            envoye += prise


def _reponse_envoyee(script: Script, i_send: int, reponse: bytes) -> bytes:
    """L'achèvement borné de la réponse (E8 hérité — miroir de .emettre) :
    octets EFFECTIVEMENT émis au client, abandon honnête sur échec."""
    envoye = bytearray()
    pos = 0
    while pos < len(reponse):
        r = script.comportement_send(i_send, len(reponse) - pos)
        i_send += 1
        if r <= 0:
            break                              # E8 : fin sans insister
        prise = min(r, len(reponse) - pos)
        envoye += reponse[pos:pos + prise]
        pos += prise
    return bytes(envoye)


class ModeleRoutage:
    """http-10:R2 en Python — dérivé de la couche I (P6/Q2'/Q3') : le paquet
    de session, la session tls-08 (Modele D90), la table des réponses (0 → le
    flux déjà pompé PAR tls-08 ; 3 → l'entrée ÉTIQUETÉE ; 2/4/5/6/7 → la 502
    R1 scellée), les lignes console, la compensation croisée (comptage de la
    session + socket cliente R1 exactement une fois). Les arrêts contractuels
    D92 (TE/CL/411/400/501/pair parti) répondent de la table SANS tls-08."""

    def __init__(self, gen: dict):
        self.gen = gen
        self.session = (ModeleClient(gen["m_script"], gen["hote"],
                                     gen["requete_r"], gen["port"])
                        if gen["routed"] else None)

    def executer(self) -> dict:
        if self.session is not None:
            verdict, appels, _page = self.session.executer()
            wf = [CONN] + [a[2] for a in appels if a[0] == "WF"] + [FIN]
            comptes = tuple(x + d for x, d in zip(compter_compensation(appels),
                                                  (0, 0, 0, 1)))
            ports = [permuter16(struct.unpack_from("<H", a[2], 2)[0])
                     for a in appels if a[0] == "CONNECT"]
            gai = [a[1] for a in appels if a[0] == "GAI"]
            client = bytes(self.session.client_envoye)
            if verdict != 0:
                reponse = L.TXT_502_CERT if verdict == 3 else TXT_502
                client += _reponse_envoyee(self.gen["script"],
                                           self.session.i_send, reponse)
            return {"client": client, "wf": wf, "comptes": comptes,
                    "paquet": self.gen["paquet"], "ports": ports, "gai": gai,
                    "verdict": verdict}
        reponse = self.gen["reponse_ar"]
        client = _reponse_envoyee(self.gen["script"], 0, reponse) if reponse else b""
        return {"client": client, "wf": [CONN, FIN], "comptes": (0, 0, 0, 1),
                "paquet": None, "ports": [], "gai": [], "verdict": None}


def script_session(script: SR2.ScriptR2, k: int) -> Script:
    """Le script VU DE LA SESSION tls-08 : l'accumulation consomme les k
    premières entrées recv (les fragments de la requête cliente) — la session
    voit la MÊME suite d'indices que l'émulation (jamais deux sources)."""
    return Script(gai=script.entries_gai, socket_=script.entries_socket,
                  connect=script.entries_connect, ach=script.hresult_ach,
                  isc=script.entries_isc, qca=script.entries_qca,
                  em=script.entries_em, dm=script.entries_dm,
                  recv=script.entries_recv[k:], send=script.entries_send,
                  dsc=script.entries_dsc, fch=script.entries_fch)


def confronter_routage(emu: SR2.EmulateurSession, gen: dict,
                       attendu: dict) -> list[str]:
    """L'émulation 29 blocs contre le modèle de routage — écarts nommés :
    octets au client, lignes console, comptes, ports, résolutions, paquet P6,
    cadre VIERGE, requête claire intacte, hygiène."""
    emu.preparer()
    try:
        emu.appeler(gen["script"])
    except Exception as e:
        return [f"faute d'exécution : {type(e).__name__} {e}"]
    appels = emu.appels
    problemes: list[str] = []
    envoi = b"".join(a[4] for a in appels if a[0] == "SEND" and a[1] == SOCKET_CLIENT)
    if envoi != attendu["client"]:
        problemes.append(f"octets au client : {len(envoi)} o != "
                         f"{len(attendu['client'])} o attendus")
    wfs = [a[2] for a in appels if a[0] == "WF"]
    if wfs != attendu["wf"]:
        problemes.append(f"lignes console : {[w[:20] for w in wfs]} != "
                         f"{[w[:20] for w in attendu['wf']]}")
    comptes = compter_compensation(appels)
    if comptes != attendu["comptes"]:
        problemes.append(f"comptes de compensation {comptes} != "
                         f"{attendu['comptes']} (ACH, DSC, FCH, CLOSESOCKET)")
    ports = [permuter16(struct.unpack_from("<H", a[2], 2)[0])
             for a in appels if a[0] == "CONNECT"]
    if ports != attendu["ports"]:
        problemes.append(f"ports de connexion {ports} != {attendu['ports']}")
    gai = [a[1] for a in appels if a[0] == "GAI"]
    if gai != attendu["gai"]:
        problemes.append(f"hôtes résolus {gai} != {attendu['gai']}")
    if sum(1 for a in appels if a[0] == "CREATETHREAD") != 0:
        problemes.append("spawn de thread inattendu sur le domaine https")
    if attendu["paquet"] is not None:
        if emu.boundary is None:
            problemes.append("tls-08 jamais appelé (P6/Q2')")
        else:
            b = emu.boundary
            hote, port, requete_r = attendu["paquet"]
            if (b["hote"] != hote or b["port"] != port
                    or b["requete"] != requete_r or b["socket"] != SOCKET_CLIENT):
                problemes.append(f"paquet de session : hôte {b['hote']!r} port "
                                 f"{b['port']} requête {b['requete'][:24]!r}… != "
                                 "attendu (P6)")
            if not b["cadre_vierge"]:
                problemes.append("cadre TLS non vierge au passage (P6/P1)")
            if bytes(emu.uc.mem_read(b["req_ptr"], b["req_len"])) != requete_r:
                problemes.append("requête claire altérée par le tunnel (Q3 tls-06)")
    elif emu.boundary is not None:
        problemes.append("tls-08 appelé à tort sur un arrêt contractuel")
    problemes += emu.hygiene()
    return problemes


# --- Les générateurs de requête (le domaine de F2 : contrôlé par construction) ---

ALPHABET_HOTE = b"abcdefghijklmnopqrstuvwxyz0123456789-."
METHODES_ROUTAGE = [b"GET"] * 6 + [b"HEAD", b"PUT", b"DELETE", b"OPTIONS", b"TRACE"]


def _autorite(alea: random.Random) -> tuple[bytes, bytes]:
    """(hôte, autorité) — 25 % de port EXPLICITE (l'explicite gagne, D92)."""
    n = alea.randint(1, 32)
    hote = bytes(alea.choice(ALPHABET_HOTE) for _ in range(n))
    if alea.random() < 0.25:
        return hote, hote + b":" + str(alea.randint(1, 65535)).encode()
    return hote, hote


def _chemin(alea: random.Random) -> tuple[bytes, bytes]:
    """(partie de cible, chemin attendu de la réécriture) — la query sans
    chemin tombe sur la fixture « / » (Q1 de http-08:R2, miroir R1)."""
    r = alea.random()
    if r < 0.15:
        return b"", b"/"                        # https://h → fixture « / »
    if r < 0.30:
        q = bytes(alea.choice(b"ab0=&") for _ in range(alea.randint(1, 12)))
        return b"?" + q, b"/"                   # query sans chemin → « / »
    if r < 0.45:
        return b"/", b"/"                       # « / » nu
    partie = b"/" + bytes(alea.choice(b"abcdefghij0123456789-_./")
                          for _ in range(alea.randint(1, 24)))
    if alea.random() < 0.30:
        q = bytes(alea.choice(b"ab0=&") for _ in range(alea.randint(1, 12)))
        partie += b"?" + q
    return partie, partie


def _fragmenter(requete: bytes, alea: random.Random) -> list[bytes]:
    """La requête découpée en 1..3 réceptions (l'accumulation la reconstitue
    — la complétude de tête est garantie à la frontière des fragments). Les
    coupes sont DISTINCTES : un fragment vide serait une réception à zéro
    octet — une FERMETURE pour le shim, jamais un fragment."""
    n = alea.choice([1, 1, 2, 3])
    if n == 1 or len(requete) < 8:
        return [requete]
    coupes = sorted({alea.randrange(1, len(requete)) for _ in range(n - 1)})
    fragments, prec = [], 0
    for c in coupes:
        fragments.append(requete[prec:c])
        prec = c
    fragments.append(requete[prec:])
    return fragments


def _construire(entree: bytes, fragments: list[bytes], sspi: dict, routed: bool,
                reponse_ar: bytes | None, paquet: tuple | None, hote: bytes,
                requete_r: bytes | None, port: int) -> dict:
    k = len(fragments)
    script = SR2.ScriptR2(recv=list(fragments) + sspi["recv"], gai=sspi["gai"],
                          socket_=sspi["socket_"], connect=sspi["connect"],
                          ach=sspi["ach"], isc=sspi["isc"], qca=sspi["qca"],
                          em=sspi["em"], dm=sspi["dm"], send=sspi["send"],
                          dsc=sspi["dsc"], fch=sspi["fch"])
    return {"entree": entree, "script": script, "k": k, "routed": routed,
            "reponse_ar": reponse_ar, "paquet": paquet, "hote": hote,
            "requete_r": requete_r, "port": port,
            "m_script": script_session(script, k) if routed else None}


def generer_scenario_https(alea: random.Random) -> tuple[dict, bool]:
    """Un scénario de routage : 70 % domaine https ROUTÉ (le modèle de session
    s'applique — paquet P6, tls-08, table Q3'), 30 % arrêts contractuels D92.
    Retour (gen, concordance_I) — la concordance croise le verdict de routage
    attendu avec modele_cible (D91, dérivé de la spec http-08:R2)."""
    hote, autorite = _autorite(alea)
    r = alea.random()
    if r < 0.30:                                # --- les arrêts contractuels
        quel = alea.random()
        if quel < 0.25:                         # corps sur cible TLS → 501 (D92)
            entree = (b"POST https://" + autorite + b"/p HTTP/1.1\r\nHost: "
                      + hote + b"\r\nContent-Length: 17\r\n\r\nCORPS-DE-17-OCTETS")
            ar, v_att = TXT_501, 4
        elif quel < 0.45:                       # Transfer-Encoding → 501 (E4)
            entree = (b"GET https://" + autorite + b"/ HTTP/1.1\r\nHost: "
                      + hote + b"\r\nTransfer-Encoding: chunked\r\n\r\n")
            ar, v_att = TXT_501, 4
        elif quel < 0.60:                       # POST/PUT sans longueur → 411
            m = alea.choice([b"POST", b"PUT"])  # (E5 : la spec R1 cite les DEUX)
            entree = (m + b" https://" + autorite + b"/p HTTP/1.1\r\nHost: "
                      + hote + b"\r\n\r\n")
            ar, v_att = TXT_411, 4
        elif quel < 0.75:                       # autorité vide → 400 (Q3 hérité)
            entree = b"GET https:///chemin HTTP/1.1\r\nHost: " + hote + b"\r\n\r\n"
            ar, v_att = TXT_400, 2
        elif quel < 0.90:                       # HTTPS:// mal cassé → 501 (Q5)
            entree = b"GET HTTPS://" + autorite + b"/ HTTP/1.1\r\nHost: " \
                     + hote + b"\r\n\r\n"
            ar, v_att = TXT_501, 3
        else:                                   # pair parti → silence (E8)
            entree = b"GET https://" + autorite + b"/x HTTP/1.1"
            ar, v_att = b"", 4
        sspi = _generer_sspi(alea)
        if ar == b"":                           # l'entrée est INACHEVÉE : l'accumulation
            sspi["recv"] = [0]                  # consomme l'amont — la terminaison suit
        gen = _construire(entree, _fragmenter(entree, alea), sspi, False, ar,
                          None, hote, None, 443)
        v_cible = CR2.modele_cible(
            entree.split(b" ")[1] if b" " in entree else b"", 1)[0]
        return gen, (v_cible == v_att)
    # --- le domaine routé (70 %)
    methode = alea.choice(METHODES_ROUTAGE)
    m_enum = SR2.METHODES.index(methode) + 1
    partie, chemin = _chemin(alea)
    cible = b"https://" + autorite + partie
    port = int(autorite.rsplit(b":", 1)[1]) if b":" in autorite else 443
    entetes = b"Host: " + hote + b"\r\n"
    if alea.random() < 0.15:                    # en-tête supplémentaire inerte
        entetes += b"X-Pad: " + bytes(alea.choice(b"abcdefghij")
                                      for _ in range(alea.randint(1, 16))) + b"\r\n"
    if methode in (b"POST", b"PUT") or alea.random() < 0.08:
        entetes += b"Content-Length: 0\r\n"     # le zéro unique est valide (M3) —
        if methode not in (b"POST", b"PUT"):   # POST/PUT SANS longueur → 411 (E5)
            methode, m_enum = b"POST", 3
    entree = methode + b" " + cible + b" HTTP/1.1\r\n" + entetes + b"\r\n"
    requete_r = methode + b" " + chemin + b" HTTP/1.1\r\n" + entetes + b"\r\n"
    # concordance I : le verdict de routage ET les découpages, par modele_cible
    v, _f, aut_off, aut_len, chm_off, chm_len = CR2.modele_cible(cible, m_enum)
    concordance = (v == 4 and cible[aut_off:aut_off + aut_len] == autorite
                   and (cible[chm_off:chm_off + chm_len] if chm_off is not None
                        and chm_off >= 0 else b"/") == chemin)
    sspi = _generer_sspi(alea)
    gen = _construire(entree, _fragmenter(entree, alea), sspi, True, None,
                      (hote, port, requete_r), hote, requete_r, port)
    return gen, concordance


def famille_routage(emu: SR2.EmulateurSession, graine: int, n: int) -> tuple[int, list]:
    alea = random.Random(graine * 100003 + 2)
    cas, ecarts = 0, []
    for i in range(n):
        gen, concordance = generer_scenario_https(alea)
        problemes = [] if concordance else \
            ["concordance I http-08:R2 : le verdict de routage généré dévie "
             "du modèle (D91)"]
        attendu = ModeleRoutage(gen).executer()
        problemes += confronter_routage(emu, gen, attendu)
        cas += 1
        if problemes:
            ecarts.append((i, gen["entree"][:48], problemes[:3]))
    return cas, ecarts


# ============================================================================
# F3 — différentiel d'ancêtre à volume (R7 — l'anti-régression du scellé)
# ============================================================================

MALFORMEES = [
    b"GET  / HTTP/1.1\r\nHost: h\r\n\r\n",          # double espace → 400
    b"GET / HTTP/1.1\nHost: h\r\n\r\n",             # LF isolé → 400
    b"GET / HTTP/1.1\r\nX-A: b\r\n\r\n",            # Host absent → 400
    b"GET foo HTTP/1.1\r\nHost: h\r\n\r\n",         # cible nue → 400
    b"GET /x" + b"y" * 2048 + b" HTTP/1.1\r\nHost: h\r\n\r\n",   # → 400
    b"GET / HTTP/1.1\r\nHost: h\r\nX-Pad: " + b"a" * 8200 + b"\r\n\r\n",  # → 431
    b"FOO / HTTP/1.1\r\nHost: h\r\n\r\n",           # méthode inconnue → 501
    b"GET /x HTTP/1.1\r\nHost: h\r\nTransfer-Encoding: chunked\r\n\r\n",  # → 501
    b"POST /p HTTP/1.1\r\nHost: h\r\n\r\n",         # sans longueur → 411
    b"GET / HTTP/2.0\r\nHost: h\r\n\r\n",           # version → 505
]


def generer_scenario_mixte(alea: random.Random) -> tuple[bytes, SR2.ScriptR2, bool]:
    """Requête mixte + script — (entree, script, diverge). diverge = le domaine
    https BYTE-EXACT (l'ancêtre refuse 501, la révision route) : cible
    « https:// » minuscule, méthode ≠ CONNECT, aucun arrêt identique des deux
    côtés (TE/corps : refus IDENTIQUE — aucune tolérance neuve, D92)."""
    hote, autorite = _autorite(alea)
    sspi = _generer_sspi(alea)
    quel = alea.random()
    if quel < 0.28:                             # http absolu sain — le relais M3
        entree = b"GET http://" + autorite + b"/a?q=1 HTTP/1.1\r\nHost: " \
                 + hote + b"\r\n\r\n"
        amont, diverge = [alea.randint(1, 400), 0], False
    elif quel < 0.42:                           # origine — l'autorité vient de Host
        entree = b"GET /a?q=1 HTTP/1.1\r\nHost: " + hote + b"\r\n\r\n"
        amont, diverge = [alea.randint(1, 400), 0], False
    elif quel < 0.52:                           # CONNECT — tunnel aveugle
        entree = b"CONNECT " + autorite + b" HTTP/1.1\r\nHost: " + hote + b"\r\n\r\n"
        amont, diverge = [alea.randint(1, 200), 0], False
    elif quel < 0.68:                           # malformées héritage
        entree = alea.choice(MALFORMEES)
        amont, diverge = [0], False
    elif quel < 0.80:                           # https + arrêt IDENTIQUE (501)
        entree = (b"POST https://" + autorite + b"/s HTTP/1.1\r\nHost: " + hote
                  + b"\r\nContent-Length: 10\r\n\r\n0123456789")
        amont, diverge = [0], False
    else:                                       # le domaine https — l'ancêtre 501
        entree = b"GET https://" + autorite + b"/c?q=1 HTTP/1.1\r\nHost: " \
                 + hote + b"\r\n\r\n"
        amont, diverge = sspi["recv"], True
        # le différentiel vérifie que l'ancêtre DÉLIVRE son 501 octet pour
        # octet : aucun échec d'émission dans la liste (les partiels achèvent,
        # seuls les <= 0 abandonnent — E8). L'abandon honnête est couvert par
        # F1/F2 CÔTÉ MODÈLE ; le différentiel, lui, mesure la divergence de
        # ROUTAGE — jamais la livraison.
        sspi["send"] = [e for e in sspi["send"] if e == "plein" or e > 0]
    fragments = _fragmenter(entree, alea)
    script = SR2.ScriptR2(recv=list(fragments) + amont, gai=sspi["gai"],
                          socket_=sspi["socket_"], connect=sspi["connect"],
                          ach=sspi["ach"], isc=sspi["isc"], qca=sspi["qca"],
                          em=sspi["em"], dm=sspi["dm"], send=sspi["send"],
                          dsc=sspi["dsc"], fch=sspi["fch"])
    return entree, script, diverge


def famille_ancetre(emu_r1: SR2.EmulateurSession, emu_r2: SR2.EmulateurSession,
                    graine: int, n: int) -> tuple[int, list]:
    alea = random.Random(graine * 100003 + 3)
    cas, ecarts = 0, []
    for i in range(n):
        entree, script, diverge = generer_scenario_mixte(alea)
        sc = SR2.Sc(nom=f"mixte#{i}", entree=entree, script=script, tls=diverge,
                    diverge=diverge, client=b"", wf=[], comptes=(0, 0, 0, 0),
                    paquet=None, ports=[], gai=[], ct=0)
        problemes = SR2.differentiel(emu_r1, emu_r2, sc)
        cas += 1
        if problemes:
            ecarts.append((i, entree[:40], problemes[:2]))
    return cas, ecarts


# ============================================================================
# F4 — falsification : l'oracle DOIT pouvoir échouer (témoin armé)
# ============================================================================

def _selection_f1() -> list[tuple]:
    """Six scénarios tls-08 FIXES (shapes D90 — les attendus viennent du
    MODELE, jamais de la main : la sélection ne fait que viser les branches
    nommées de la spec : succès, certificat, cible injoignable, densité,
    acquisition fatale, exotique)."""
    return [
        (Script(isc=[(CONT, 64), (OK, 32)], recv=[128, 121, 0],
                dm=[(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)]),
         HOTE_DEFAUT, REQUETE_DEFAUT, 443),
        (Script(isc=[(CERT_INVALIDE, 0)]), HOTE_DEFAUT, REQUETE_DEFAUT, 443),
        (Script(gai=[0x2AFA]), HOTE_DEFAUT, REQUETE_DEFAUT, 443),
        (Script(isc=[(CONT, 64), (OK, 32)], recv=[128, "max"],
                dm=[(INCOMPLET, 5, 100, 16)]), HOTE_DEFAUT, REQUETE_DEFAUT, 443),
        (Script(ach=INVALID_HANDLE), HOTE_DEFAUT, REQUETE_DEFAUT, 443),
        (Script(isc=[(EXOTIQUE, 0)]), HOTE_DEFAUT, REQUETE_DEFAUT, 443),
    ]


def _selection_f2() -> list[dict]:
    """Six scénarios de routage FIXES (shapes D92 — les attendus viennent du
    MODELE DE ROUTAGE, jamais de la main)."""
    hote = b"exemple.fr"
    requete_r = b"GET /chemin HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"
    entree = b"GET https://exemple.fr/chemin HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"

    def _gen(script, routed, reponse_ar, paquet, entree=entree,
             hote=hote, requete_r=requete_r, port=443):
        return {"entree": entree, "script": script, "k": 1, "routed": routed,
                "reponse_ar": reponse_ar, "paquet": paquet, "hote": hote,
                "requete_r": requete_r if routed else None, "port": port,
                "m_script": script_session(script, 1) if routed else None}

    return [
        _gen(SR2.ScriptR2(isc=[(CONT, 64), (OK, 32)], recv=[entree, 128, 121, 21],
                         dm=[(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)]),
             True, None, (hote, 443, requete_r)),
        _gen(SR2.ScriptR2(isc=[(CERT_INVALIDE, 0)], recv=[entree]),
             True, None, (hote, 443, requete_r)),
        _gen(SR2.ScriptR2(gai=[0x2AFA], recv=[entree]),
             True, None, (hote, 443, requete_r)),
        _gen(SR2.ScriptR2(recv=[b"POST https://exemple.fr/s HTTP/1.1\r\n"
                                b"Host: exemple.fr\r\n"
                                b"Content-Length: 10\r\n\r\n0123456789"]),
             False, TXT_501, None),
        _gen(SR2.ScriptR2(recv=[b"GET https://exemple.fr/x HTTP/1.1\r\n"
                                b"Host: exemple.fr\r\n"
                                b"Transfer-Encoding: chunked\r\n\r\n"]),
             False, TXT_501, None),
        _gen(SR2.ScriptR2(recv=[b"GET https://exemple.fr/x HTTP/1.1", 0]),
             False, b"", None),
    ]


def famille_falsification(ks: Ks, blobs: dict) -> tuple[int, list[str], int]:
    """(n_contrôles, verdicts, défauts) — mutations d'un point extraites des
    harnais D90/D92 ATTRAPÉES sur les sélections fixes ; le MODÈLE falsifié
    (octets au client maquillés) nommé par la confrontation ; le témoin
    intact reste vert sur les MÊMES sélections."""
    verdicts: list[str] = []
    defauts = 0
    sel_f1 = _selection_f1()
    sel_f2 = _selection_f2()
    attendus_f2 = [ModeleRoutage(gen).executer() for gen in sel_f2]
    # (1) mutations tls-08 — la sélection F1 doit nommer l'écart
    for indice in (0, 4, 7, 10):
        nom, mutation = HS.MUTATIONS_V4[indice]
        blob_m, _ = octets_notation(ks, "tls-08-session", HS.RVA_TLS08, mutation)
        blobs_m = dict(blobs)
        blobs_m["tls-08"] = blob_m
        emu_m = HS.Emulateur(blobs_m)
        attrapes = sum(1 for script, hote, requete, port in sel_f1
                       if confronter_session(emu_m, script, hote, requete, port)[0])
        if attrapes == 0:
            defauts += 1
        verdicts.append(f"mutation tls-08 « {nom} » : "
                        f"{'ATTRAPÉE' if attrapes else 'MANQUÉE'} ({attrapes}/6)")
    # (2) mutations http-10:R2 — la sélection F2 doit nommer l'écart
    for indice in (1, 4, 7, 10):
        nom, mutation = SR2.MUTATIONS_V4[indice]
        blob_m, _ = octets_notation(ks, "http-10-session-r2",
                                    SR2.RVA_SESSION_R2, mutation)
        blobs_m = dict(blobs)
        blobs_m["http-10-R2"] = blob_m
        emu_m = SR2.EmulateurSession(blobs_m, SR2.RVA_SESSION_R2, SR2.CADRE_R2)
        attrapes = sum(1 for gen, attendu in zip(sel_f2, attendus_f2)
                       if confronter_routage(emu_m, gen, attendu))
        if attrapes == 0:
            defauts += 1
        verdicts.append(f"mutation http-10:R2 « {nom} » : "
                        f"{'ATTRAPÉE' if attrapes else 'MANQUÉE'} ({attrapes}/6)")
    # (3) le modèle falsifié — la confrontation DOIT nommer l'écart
    emu_v = SR2.EmulateurSession(blobs, SR2.RVA_SESSION_R2, SR2.CADRE_R2)
    corrompu = dict(attendus_f2[0])
    corrompu["client"] += b"X"
    if confronter_routage(emu_v, sel_f2[0], corrompu):
        verdicts.append("modèle falsifié (octets au client maquillés) : ATTRAPÉ")
    else:
        defauts += 1
        verdicts.append("modèle falsifié : MANQUÉ — la confrontation est creuse")
    # (4) témoin intact — les mêmes sélections restent vertes
    emu_t = HS.Emulateur(blobs)
    verts_f1 = sum(1 for script, hote, requete, port in sel_f1
                   if not confronter_session(emu_t, script, hote, requete, port)[0])
    verts_f2 = sum(1 for gen, attendu in zip(sel_f2, attendus_f2)
                   if not confronter_routage(emu_v, gen, attendu))
    if verts_f1 != len(sel_f1) or verts_f2 != len(sel_f2):
        defauts += 1
    verdicts.append(f"témoin intact : F1 {verts_f1}/{len(sel_f1)}, "
                    f"F2 {verts_f2}/{len(sel_f2)}")
    return len(verdicts), verdicts, defauts


# ============================================================================
# Chargement (LA table d'intégration D92 — source unique) et point d'entrée
# ============================================================================

def charger_blobs(ks: Ks) -> tuple[dict, list[tuple]]:
    """Les vingt-neuf blocs réels + l'ancêtre scellé par LA table d'intégration
    de D92 (harnais_session_r2.charger) sous silence : les contrôles V1 sont
    COLLECTÉS, pas imprimés — l'oracle les constate en UN contrôle (jamais
    deux sources de vérité pour la table d'intégration)."""
    collecte: list[tuple] = []
    veritable = SR2.controle
    SR2.controle = lambda nom, ok, detail="": collecte.append((nom, ok))
    try:
        blobs = SR2.charger(ks)
    finally:
        SR2.controle = veritable
    return blobs, collecte


VOLUMES = {"complet": (250, 150, 150), "reduit": (8, 6, 6)}


def executer(blobs: dict, graine: int = 1, volume: str = "complet") -> dict:
    """Le point d'entrée du futur build_m4.py — lève EchecOracle sur TOUT
    écart ; sinon retourne le verdict (les graines différencient les
    exécutions ; seuls les comptes hachés survivent au rapport de build)."""
    n1, n2, n3 = VOLUMES.get(volume, VOLUMES["complet"])
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    emu_f1 = HS.Emulateur(blobs)
    emu_r2 = SR2.EmulateurSession(blobs, SR2.RVA_SESSION_R2, SR2.CADRE_R2)
    emu_r1 = SR2.EmulateurSession(blobs, SR2.RVA_SESSION_R1, SR2.CADRE_R1)
    familles: dict[str, str] = {}
    ecarts: list[str] = []
    cas, e1 = famille_session(emu_f1, graine, n1)
    familles["F1-session-tls08"] = f"{cas} scénarios hostiles, {len(e1)} écart(s)"
    ecarts += [f"F1#{i} {h} — {'; '.join(p)}" for i, h, p in e1[:4]]
    cas, e2 = famille_routage(emu_r2, graine, n2)
    familles["F2-routage-http10R2"] = f"{cas} scénarios générés, {len(e2)} écart(s)"
    ecarts += [f"F2#{i} {h!r} — {'; '.join(p)}" for i, h, p in e2[:4]]
    cas, e3 = famille_ancetre(emu_r1, emu_r2, graine, n3)
    familles["F3-ancetre-R7"] = f"{cas} scénarios mixtes, {len(e3)} écart(s)"
    ecarts += [f"F3#{i} {h!r} — {'; '.join(p)}" for i, h, p in e3[:4]]
    n_f4, verdicts, defauts = famille_falsification(ks, blobs)
    familles["F4-falsification"] = f"{n_f4} contrôles, {defauts} défaut(s)"
    ecarts += [v for v in verdicts if "MANQUÉ" in v]
    total = n1 + n2 + n3 + n_f4
    if len(e1) + len(e2) + len(e3) + defauts:
        raise EchecOracle(f"{len(e1) + len(e2) + len(e3) + defauts} écart(s) — "
                          + " | ".join(ecarts[:6]))
    empreinte = hashlib.sha256(
        f"{total}|{graine}|{volume}|".encode()
        + b"".join(k.encode() for k in sorted(familles))).hexdigest()[:16]
    return {"total_cas": total, "empreinte": empreinte, "graine": graine,
            "volume": volume, "familles": familles}


def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261028)
    parseur.add_argument("--volume", choices=["complet", "reduit"],
                         default="complet")
    args = parseur.parse_args()
    print("=== oracle_m4.py — l'oracle à scénarios SSPI (D93) ===")
    print(f"graine {args.graine} · volume {args.volume} · familles F1-F4 "
          "(session / routage / ancêtre / falsification)")
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    blobs, collecte = charger_blobs(ks)
    ok_chargement = all(ok for _nom, ok in collecte)
    print(f"\n[chargement] {len(collecte)} contrôles V1 (table d'intégration "
          f"D92, source unique) : {'VERTS' if ok_chargement else 'ÉCHEC'}")
    if not ok_chargement:
        return 1
    try:
        verdict = executer(blobs, graine=args.graine, volume=args.volume)
    except EchecOracle as e:
        print(f"\nÉCHEC : {e}")
        return 1
    for cle, valeur in verdict["familles"].items():
        print(f"[{cle}] {valeur}")
    print("\n" + "=" * 70)
    print(f"BILAN : {verdict['total_cas']} cas · empreinte "
          f"{verdict['empreinte']} · graine {verdict['graine']}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
