#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oracle_m5.py — Oracle à scénarios ÉTENDU du jalon M5 (D136 — le relèvement).

L'oracle de l'ORCHESTRATION http-10:R3, comme promis par la surface de
vérification D136 (m5/I/README.md) : « L'orchestration relève de l'oracle à
scénarios ÉTENDU : cible relevée saine (ligne de flux exacte, page relayée,
verdict 0), certificat invalide relevé (verdict 3, 502 étiquetée), politique
absente (zéro écart contre R1/R2), ligne de flux vérifiée OCTET PAR OCTET
contre le modèle de composition. » L'oracle GÉNÈRE des scénarios par graine
(méthodes, autorités, ports explicites, chemins, en-têtes, SSPI hostiles)
et confronte le MODÈLE DE COMPOSITION (dérivé de la couche I, jamais de la
notation) à l'ÉMULATION (les octets réels des notations, chaîne complète —
l'intégration LA PLUS LARGE du projet : TREIZE-ET-UN blocs réels + l'ANCIÊTRE
scellé 0.5.1 pour le différentiel) :

  F1  RELEVÉE à volume (politique armée) — le cœur D136 : le domaine http://
      absolu GÉNÉRÉ (72 % routée — le tunnel tls-08 par LE MÊME chemin Q2',
      port 443 FORCÉ E2 : l'explicite du navigateur est PERDU —, 28 % gardes
      et arrêts nommés : corps/TE → 501, POST/PUT sans longueur → 411, la
      ligne porte le verdict NOMMÉ ; autorité vide → 400 et « HTTP:// » mal
      cassé → 501 SANS ligne — le refus précède le routage, la sentinelle
      demeure) ; CHAQUE scénario vérifie la ligne de flux OCTET PAR OCTET
      (méthode PAR TABLE, hôte TRONQUÉ à 14 — E3, port EFFECTIF, v/e/s :
      entrés = accumulation + corps pompé, sortis = émissions .emettre, les
      relais délégués JAMAIS comptés deux fois), la réponse exacte au
      client (page relayée, 502 ÉTIQUETÉE sur verdict 3 — la ligne nomme la
      CAUSE, la réponse nomme l'effet), la compensation croisée PAR
      COMPTAGE, le paquet P6/P7 au passage de tls-08 (autorité découpée,
      requête réécrite en forme origine, cadre TLS vierge), les ports et
      résolutions, l'hygiène — ET la concordance I : le verdict de la
      FEUILLE (harnais_cible_r3.modele_cible, D136 : le 5e argument et la
      politique) croisé avec le routage généré (jamais deux sources) ;

  F2  DOMAINES HÉRITÉS sous les DEUX politiques — le différentiel d'ancêtre
      Q7 à volume : chaque scénario joué à politique 0, l'ancêtre http-10:R2
      scellé (octets 0.5.1) ÉMULÉ contre la révision — traces normalisées
      IDENTIQUES (l'anti-régression R7 : sans politique, R2 octet pour
      octet sur tout chemin, AUCUNE ligne) — PUIS à politique 1 : les
      domaines origine (port 80, la requête réécrite émise en clair, la
      réponse relayée par la pompe), CONNECT (le tunnel aveugle, la pompe
      détachée), https (Q2' D92 — le port explicite GAGNE, contrairement à
      la relevée), malformées et pair parti (SANS ligne : la requête n'est
      pas identifiable, rien à nommer) — les octets au client et la
      compensation sont ceux de l'ancêtre ÉMULÉ (la RÉFÉRENCE R7, le même
      arbitrage que l'oracle M3/M4 : l'héritage n'est jamais remodélisé),
      la ligne seule est composée par le modèle de spécification ;

  F3  falsification — les TREIZE mutations d'un point de la révision
      (harnais_session_r3.MUTATIONS_V4, stables en taille — leçon D82)
      ATTRAPÉES sur les scénarios du harnais, le MODÈLE falsifié (la ligne
      maquillée) NOMMÉ par la confrontation, le témoin intact VERT — une
      suite qui ne peut pas échouer ne prouve rien.

Réutilisation stricte (jamais deux sources de vérité) : ModeleClient/
_reponse_envoyee/script_session/_generer_sspi/_autorite/_chemin/_fragmenter
(oracle_m4 D93 — l'héritage), EmulateurSessionR3/ScR3/jouer_r3/
differentiel_q7/ligne_flux/MUTATIONS_V4 (harnais_session_r3 D136),
modele_cible (harnais_cible_r3), les shims D90/D92 (harnais_session_r2).

Usage : python3 oracle_m5.py [--graine G] [--volume complet|reduit]
   (et depuis build_m5.py : executer(blobs, graine, volume))
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import random
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
M4_DIR = os.path.join(ICI, os.pardir, "m4")
sys.path.insert(0, ICI)
sys.path.insert(0, M4_DIR)
sys.path.insert(0, os.path.join(M4_DIR, "outils"))
sys.path.insert(0, os.path.join(ICI, "outils"))

import layout as L4  # noqa: E402  — m4/layout.py (m4 AVANT m5 sur le chemin)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

import harnais_session as HS  # noqa: E402 — les shims D90 (tls-08)
import harnais_session_r2 as SR2  # noqa: E402 — le harnais D92 (l'ancêtre)
import oracle_m4 as od4  # noqa: E402 — l'oracle D93 (l'héritage des modèles)
from harnais_session import (  # noqa: E402
    compter_compensation, permuter16, SOCKET_CLIENT,
)
import harnais_session_r3 as SR3  # noqa: E402 — le harnais D136 (la révision)
import harnais_cible_r3 as CR3  # noqa: E402 — la feuille http-08:R3 (D136)

from oracle_m4 import EchecOracle  # noqa: E402 — l'échec nommé (build_m5 l'attrape)

# Les réponses héritées (textes consignés, R7 — via le harnais R3)
TXT_400, TXT_411 = SR3.TXT_400, SR3.TXT_411
TXT_431, TXT_501, TXT_505 = SR3.TXT_431, SR3.TXT_501, SR3.TXT_505
TXT_502 = SR3.TXT_502
CONN, FIN = SR3.CONNECTION, SR3.FIN


# ============================================================================
# Le modèle de composition D136 (écrit depuis la SPÉCIFICATION — jamais la notation)
# ============================================================================

class ModeleRoutageR3:
    """http-10:R3 en Python — le modèle de routage D93 (oracle_m4, l'héritage
    REPRIS) ÉTENDU de LA LIGNE DE FLUX et du verdict 5 :

      - mode « routed » (relevée verdict 5 / https verdict 4) : la session
        tls-08 (ModeleClient D90) sur le port EFFECTIF — 443 FORCÉ pour la
        relevée (E2 : l'explicite du navigateur est perdu, un relèvement
        vers :8080 serait une invention), le port explicite GAGNE pour
        https (Q2' D92) —, la table des réponses Q3' INCHANGÉE (0 → le flux
        pompé PAR tls-08 ; 3 → l'entrée ÉTIQUETÉE ; 2/4/5/6/7 → la 502),
        la ligne : v = LE VERDICT tls TRANSPORTÉ (la ligne nomme la CAUSE,
        la réponse nomme l'effet — E1), e = l'accumulation + le corps pompé,
        s = les émissions .emettre de la session (sur un relèvement réussi,
        s=0 est la signature honnête du relais tls-08 — P8) ;
      - mode « arret » (les gardes et arrêts NOMMÉS) : la réponse seule au
        client, la ligne porte le verdict de la réponse NOMMÉE (501/411)
        quand le refus vient APRÈS le routage — PAS de ligne quand le refus
        le précède (autorité vide, casse, http-02 en échec, accumulation
        morte : la sentinelle -1, rien à nommer) ;
      - mode « heritage » (origine, CONNECT — les domaines dont l'héritage
        n'est JAMAIS remodélisé) : les octets au client, la compensation,
        les ports et la pompe appartiennent à l'ancêtre ÉMULÉ (la RÉFÉRENCE
        R7, le même arbitrage que l'oracle M3/M4), la ligne seule est
        composée ici (v=0 aboutie, port effectif 80/tunnel, s = l'émission
        propre : la requête réécrite pour l'origine, le 200 du tunnel)."""

    def __init__(self, gen: dict):
        self.gen = gen
        self.session = (od4.ModeleClient(gen["m_script"], gen["hote"],
                                         gen["requete_r"], gen["port"])
                        if gen["mode"] == "routed" else None)

    def executer(self) -> dict:
        gen = self.gen
        if gen["mode"] == "routed":
            verdict, appels, _page = self.session.executer()
            wf = [CONN] + [a[2] for a in appels if a[0] == "WF"] + [FIN]
            comptes = tuple(x + d for x, d in zip(
                compter_compensation(appels), (0, 0, 0, 1)))
            ports = [permuter16(struct.unpack_from("<H", a[2], 2)[0])
                     for a in appels if a[0] == "CONNECT"]
            gai = [a[1] for a in appels if a[0] == "GAI"]
            client = bytes(self.session.client_envoye)
            if verdict != 0:                       # Q3' : la table des réponses
                reponse = L4.TXT_502_CERT if verdict == 3 else TXT_502
                envoyee = od4._reponse_envoyee(gen["script"],
                                                self.session.i_send, reponse)
                client += envoyee
                s_ligne = len(envoyee)             # P8 : les émissions propres
            else:
                s_ligne = 0                        # le relais tls-08 délégué
            ligne = SR3.ligne_flux(gen["methode_t"], gen["hote"], gen["port"],
                                   verdict, len(gen["entree"]), s_ligne)
            wf.insert(-1, ligne)                   # Q6 : avant la compensation
            return {"client": client, "wf": wf, "comptes": comptes,
                    "paquet": gen["paquet"], "ports": ports, "gai": gai,
                    "ct": 0, "verdict": verdict}
        if gen["mode"] == "arret":
            reponse = gen["reponse_ar"]
            client = od4._reponse_envoyee(gen["script"], 0, reponse) \
                if reponse else b""
            wf = [CONN, FIN]
            if gen["ligne"]:                       # la garde APRÈS le routage
                ligne = SR3.ligne_flux(gen["methode_t"], gen["hote"],
                                       gen["port"], gen["v_ligne"],
                                       len(gen["entree"]), len(client))
                wf.insert(1, ligne)
            return {"client": client, "wf": wf, "comptes": (0, 0, 0, 1),
                    "paquet": None, "ports": [], "gai": [], "ct": 0,
                    "verdict": None}
        # « heritage » : la référence R7 (l'ancêtre ÉMULÉ à politique 0)
        ref = gen["reference"]
        wf = list(ref["wf"])
        if gen["ligne"]:
            if gen["echec_amont"]:
                # l'amont injoignable (tcp-13 en échec — gai/socket/connect,
                # l'ISSUE est propriété du générateur) : la réponse NOMMÉE
                # 502 — la ligne porte l'EFFET (v=502, s = les octets émis
                # de la réponse, exactement le client vu de l'ancêtre)
                s = len(ref["client"])
                v = 502
            else:
                # aboutie : s = l'émission PROPRE de la session (la requête
                # réécrite pour l'origine, le 200 du tunnel) — le relais
                # délégué n'est JAMAIS compté (P8)
                s = len(od4._reponse_envoyee(gen["script"], 0, gen["emission"]))
                v = 0
            ligne = SR3.ligne_flux(gen["methode_t"], gen["hote"], gen["port"],
                                   v, len(gen["entree"]), s)
            wf.insert(-1, ligne)
        return {"client": ref["client"], "wf": wf, "comptes": ref["comptes"],
                "paquet": None, "ports": ref["ports"], "gai": ref["gai"],
                "ct": ref["ct"], "verdict": v}


def _sc_r3(gen: dict, attendu: dict):
    """Le ScR3 complet — les attendus du modèle confrontés aux octets."""
    return SR3.ScR3(gen["entree"][:40].decode("latin-1"), gen["politique"],
                    gen["entree"], gen["script"], gen["mode"] == "routed",
                    False, attendu["client"], attendu["wf"],
                    attendu["comptes"], attendu["paquet"], attendu["ports"],
                    attendu["gai"], attendu["ct"])


def observer(emu) -> dict:
    """Les observables bruts d'un run déjà effectué — les MÊMES champs que
    HR2.jouer compare (jamais deux sources de vérité pour la lecture)."""
    appels = emu.appels
    return {
        "client": b"".join(a[4] for a in appels
                           if a[0] == "SEND" and a[1] == SOCKET_CLIENT),
        "wf": [a[2] for a in appels if a[0] == "WF"],
        "comptes": compter_compensation(appels),
        "ports": [permuter16(struct.unpack_from("<H", a[2], 2)[0])
                  for a in appels if a[0] == "CONNECT"],
        "gai": [a[1] for a in appels if a[0] == "GAI"],
        "ct": sum(1 for a in appels if a[0] == "CREATETHREAD"),
    }


# ============================================================================
# Les générateurs (le domaine contrôlé PAR CONSTRUCTION — jamais deux sources)
# ============================================================================

def _construire(entree: bytes, recv: list, sspi: dict, mode: str,
                **champs) -> dict:
    """Le scénario généré : le script VOIT la requête en fragments PUIS la
    suite d'entrées (le SSPI pour les routés, la réponse amont pour les
    hérités, la fermeture pour les autres) — la session voit la MÊME suite
    d'indices que l'émulation."""
    script = SR2.ScriptR2(recv=list(recv), gai=sspi["gai"],
                          socket_=sspi["socket_"], connect=sspi["connect"],
                          ach=sspi["ach"], isc=sspi["isc"], qca=sspi["qca"],
                          em=sspi["em"], dm=sspi["dm"], send=sspi["send"],
                          dsc=sspi["dsc"], fch=sspi["fch"])
    gen = {"entree": entree, "script": script, "mode": mode, "politique": 1}
    gen.update(champs)
    return gen


def _hote_ligne(alea: random.Random) -> bytes:
    """L'hôte de la ligne : 70 % court (<= 13), 30 % long (> 14 — la borne
    FLUX_HOTE_MAX garde une visibilité réelle, E3)."""
    n = alea.choice((alea.randint(1, 13), alea.randint(1, 13),
                     alea.randint(15, 32)))
    return bytes(alea.choice(b"abcdefghijklmnopqrstuvwxyz0123456789-.")
                 for _ in range(n))


def generer_scenario_relevee(alea: random.Random) -> tuple[dict, bool]:
    """Un scénario du domaine RELEVÉ (le navigateur parle http:// absolu au
    mandataire explicite) : 72 % routée (le cœur D136 — le modèle de session
    tls-08 s'applique, port 443 FORCÉ : l'explicite du navigateur est PERDU,
    E2), 28 % gardes et arrêts nommés. Retour (gen, concordance) — la
    concordance croise le verdict de la FEUILLE (modele_cible, politique
    armée) avec le routage généré (D136, jamais deux sources)."""
    hote, autorite = od4._autorite(alea)       # 25 % de port EXPLICITE (E2)
    r = alea.random()
    if r < 0.28:                               # --- gardes et arrêts nommés
        quel = alea.random()
        if quel < 0.35:                        # corps sur cible relevée → 501
            entree = (b"POST http://" + autorite + b"/p HTTP/1.1\r\nHost: "
                      + hote + b"\r\nContent-Length: 17\r\n\r\nCORPS-DE-17-OCTETS")
            gen = _construire(entree, [entree] + [16, 0], od4._generer_sspi(alea),
                              "arret", ligne=True, v_ligne=501, hote=hote,
                              port=443, methode_t=b"POST", reponse_ar=TXT_501)
            return gen, True
        if quel < 0.60:                        # Transfer-Encoding → 501 (E4 hérité)
            entree = (b"GET http://" + autorite + b"/ HTTP/1.1\r\nHost: "
                      + hote + b"\r\nTransfer-Encoding: chunked\r\n\r\n")
            gen = _construire(entree, od4._fragmenter(entree, alea) + [0],
                              od4._generer_sspi(alea), "arret", ligne=True,
                              v_ligne=501, hote=hote, port=443,
                              methode_t=b"GET", reponse_ar=TXT_501)
            return gen, True
        if quel < 0.80:                        # POST/PUT sans longueur → 411
            m = alea.choice([b"POST", b"PUT"])
            entree = (m + b" http://" + autorite + b"/p HTTP/1.1\r\nHost: "
                      + hote + b"\r\n\r\n")
            gen = _construire(entree, od4._fragmenter(entree, alea) + [0],
                              od4._generer_sspi(alea), "arret", ligne=True,
                              v_ligne=411, hote=hote, port=443, methode_t=m,
                              reponse_ar=TXT_411)
            return gen, True
        if quel < 0.90:                        # autorité vide → 400 SANS ligne
            entree = b"GET http:///chemin HTTP/1.1\r\nHost: " + hote + b"\r\n\r\n"
            gen = _construire(entree, od4._fragmenter(entree, alea) + [0],
                              od4._generer_sspi(alea), "arret", ligne=False,
                              hote=hote, port=443, methode_t=b"GET",
                              reponse_ar=TXT_400)
            v_cible = CR3.modele_cible(b"http:///chemin", 1, 1)[0]
            return gen, v_cible == 2
        # « HTTP:// » mal cassé → 501 SANS ligne (le refus précède le routage)
        entree = (b"GET HTTP://" + autorite + b"/ HTTP/1.1\r\nHost: "
                  + hote + b"\r\n\r\n")
        gen = _construire(entree, od4._fragmenter(entree, alea) + [0],
                          od4._generer_sspi(alea), "arret", ligne=False,
                          hote=hote, port=443, methode_t=b"GET",
                          reponse_ar=TXT_501)
        v_cible = CR3.modele_cible(b"HTTP://" + autorite + b"/", 1, 1)[0]
        return gen, v_cible == 3
    # --- la domaine routée (72 %)
    methode = alea.choice(od4.METHODES_ROUTAGE)
    m_enum = SR2.METHODES.index(methode) + 1
    partie, chemin = od4._chemin(alea)
    cible = b"http://" + autorite + partie
    entetes = b"Host: " + hote + b"\r\n"
    if alea.random() < 0.15:                   # en-tête supplémentaire inerte
        entetes += b"X-Pad: " + bytes(alea.choice(b"abcdefghij")
                                      for _ in range(alea.randint(1, 16))) + b"\r\n"
    if methode in (b"POST", b"PUT"):
        entetes += b"Content-Length: 0\r\n"    # le zéro unique est valide (M3)
    entree = methode + b" " + cible + b" HTTP/1.1\r\n" + entetes + b"\r\n"
    requete_r = methode + b" " + chemin + b" HTTP/1.1\r\n" + entetes + b"\r\n"
    # concordance I : la FEUILLE tranche (le 5e argument, la politique)
    v, _f, aut_off, aut_len, chm_off, chm_len = CR3.modele_cible(cible, m_enum, 1)
    concordance = (v == 5 and cible[aut_off:aut_off + aut_len] == autorite
                   and (cible[chm_off:chm_off + chm_len]
                        if chm_off is not None and chm_off >= 0 else b"/") == chemin)
    sspi = od4._generer_sspi(alea)
    fragments = od4._fragmenter(entree, alea)
    gen = _construire(entree, fragments + sspi["recv"], sspi, "routed",
                      hote=hote, port=443, methode_t=methode,
                      paquet=(hote, 443, requete_r), requete_r=requete_r)
    gen["m_script"] = od4.script_session(gen["script"], len(fragments))
    return gen, concordance


# Les malformées héritées (SANS ligne : http-02 en échec ou refus PRÉ-ROUTAGE)
MALFORMEES_HERITEES = [
    (b"GET  / HTTP/1.1\r\nHost: h\r\n\r\n", TXT_400),        # double espace
    (b"GET / HTTP/1.1\nHost: h\r\n\r\n", TXT_400),           # LF isolé
    (b"GET / HTTP/1.1\r\nX-A: b\r\n\r\n", TXT_400),          # Host absent
    (b"GET foo HTTP/1.1\r\nHost: h\r\n\r\n", TXT_400),       # cible nue (verdict 1)
    (b"GET /x" + b"y" * 2048 + b" HTTP/1.1\r\nHost: h\r\n\r\n", TXT_400),
    (b"GET / HTTP/1.1\r\nHost: h\r\nX-Pad: " + b"a" * 8200 + b"\r\n\r\n", TXT_431),
    (b"GET / HTTP/2.0\r\nHost: h\r\n\r\n", TXT_505),         # version
]


def _connexion_amont(alea: random.Random, sspi: dict) -> bool:
    """L'ISSUE de la connexion amont (tcp-13) est PROPRIÉTÉ DU GÉNÉRATEUR :
    80 % saine (les listes gai/socket/connect VIDÉES — les défauts des
    listes épuisées sont le succès, D90), 20 % l'échec NOMMÉ (gai, socket
    ou connect — la réponse 502, la ligne v=502). Le modèle n'en dérive
    RIEN des observations : l'issue est connue AVANT le run (jamais deux
    sources)."""
    sspi["gai"], sspi["socket_"], sspi["connect"] = [], [], []
    # leçon m4 (F3) : les émissions à ≤ 0 (« le pair est parti ») sont
    # retirées — l'abandon honnête de la phase d'émission propre est couvert
    # par la famille routée (le modèle la rejoue) ; ici l'ISSUE doit être
    # connue du modèle (jamais deux sources)
    sspi["send"] = [e for e in sspi["send"] if e == "plein" or e > 0]
    if alea.random() < 0.20:
        quel = alea.random()
        if quel < 0.34:
            sspi["gai"] = [0x2AFA]           # résolution — hôte inconnu
        elif quel < 0.67:
            sspi["socket_"] = [-1]           # socket refusée
        else:
            sspi["connect"] = [-1]           # connexion refusée
        return False
    return True


def generer_scenario_herite(alea: random.Random) -> tuple[dict, bool]:
    """Les domaines HÉRITÉS sous les DEUX politiques : la révision ne change
    NI le routage NI les octets au client — la politique ne fait qu'apparaître
    LA LIGNE (et JAMAIS un verdict 5 hors domaine http://) : origine (port
    80), CONNECT (le tunnel aveugle), https (Q2' D92), malformées et pair
    parti (SANS ligne). Retour (gen, concordance)."""
    r = alea.random()
    if r < 0.28:                               # --- origine (port 80)
        hote = _hote_ligne(alea)
        methode = alea.choice([b"GET", b"GET", b"HEAD", b"OPTIONS", b"TRACE"])
        partie, _chem = od4._chemin(alea)
        partie = partie if partie.startswith(b"/") else b"/"
        # la forme origine EXIGE un chemin en « / » : le vide ou la query nue
        # (b"?…") y seraient un 400 mal formé — le domaine couvert est le
        # chemin origine VALIDE (les malformées ont leur branche propre)
        entree = (methode + b" " + partie + b" HTTP/1.1\r\nHost: " + hote
                  + b"\r\n\r\n")
        sspi = od4._generer_sspi(alea)
        saine = _connexion_amont(alea, sspi)
        queue = [alea.randint(1, 400), 0] if saine else [0]
        gen = _construire(entree, od4._fragmenter(entree, alea) + queue, sspi,
                          "heritage", ligne=True, hote=hote, port=80,
                          methode_t=methode, emission=entree, echec_amont=not saine)
        return gen, True                       # la réécriture est l'identité
    if r < 0.46:                               # --- CONNECT (le tunnel)
        hote = _hote_ligne(alea)
        port = alea.choice((443, 443, 8080, alea.randint(1, 65535)))
        autorite = hote + b":" + str(port).encode()
        entree = (b"CONNECT " + autorite + b" HTTP/1.1\r\nHost: " + hote
                  + b"\r\n\r\n")
        sspi = od4._generer_sspi(alea)
        saine = _connexion_amont(alea, sspi)
        gen = _construire(entree, od4._fragmenter(entree, alea) + [0], sspi,
                          "heritage", ligne=True, hote=hote, port=port,
                          methode_t=b"CONNECT", emission=SR3.TXT_TUNNEL,
                          echec_amont=not saine)
        return gen, True
    if r < 0.80:                               # --- https (Q2' D92)
        hote, autorite = od4._autorite(alea)
        methode = alea.choice(od4.METHODES_ROUTAGE)
        m_enum = SR2.METHODES.index(methode) + 1
        partie, chemin = od4._chemin(alea)
        cible = b"https://" + autorite + partie
        port = int(autorite.rsplit(b":", 1)[1]) if b":" in autorite else 443
        entetes = b"Host: " + hote + b"\r\n"
        if alea.random() < 0.15:
            entetes += b"X-Pad: " + bytes(alea.choice(b"abcdefghij")
                                          for _ in range(alea.randint(1, 16))) + b"\r\n"
        if methode in (b"POST", b"PUT"):
            entetes += b"Content-Length: 0\r\n"
        entree = methode + b" " + cible + b" HTTP/1.1\r\n" + entetes + b"\r\n"
        requete_r = methode + b" " + chemin + b" HTTP/1.1\r\n" + entetes + b"\r\n"
        v, _f, aut_off, aut_len, chm_off, chm_len = CR3.modele_cible(cible, m_enum, 1)
        concordance = (v == 4 and cible[aut_off:aut_off + aut_len] == autorite
                       and (cible[chm_off:chm_off + chm_len]
                            if chm_off is not None and chm_off >= 0 else b"/") == chemin)
        sspi = od4._generer_sspi(alea)
        fragments = od4._fragmenter(entree, alea)
        gen = _construire(entree, fragments + sspi["recv"], sspi, "routed",
                          hote=hote, port=port, methode_t=methode,
                          paquet=(hote, port, requete_r), requete_r=requete_r)
        gen["m_script"] = od4.script_session(gen["script"], len(fragments))
        return gen, concordance
    if r < 0.93:                               # --- malformées (SANS ligne)
        entree, ar = alea.choice(MALFORMEES_HERITEES)
        gen = _construire(entree, od4._fragmenter(entree, alea) + [0],
                          od4._generer_sspi(alea), "arret", ligne=False,
                          hote=b"h", port=80, methode_t=b"GET", reponse_ar=ar)
        return gen, True
    # --- pair parti (accumulation morte — SANS ligne, silence honnête)
    hote = _hote_ligne(alea)
    entree = b"GET /x HTTP/1.1"
    gen = _construire(entree, [entree, 0], od4._generer_sspi(alea), "arret",
                      ligne=False, hote=hote, port=80, methode_t=b"GET",
                      reponse_ar=b"")
    return gen, True


# ============================================================================
# F1 — la relevée à volume (politique armée, la ligne OCTET PAR OCTET)
# ============================================================================

def famille_relevee(emu, graine: int, n: int) -> tuple[int, list]:
    alea = random.Random(graine * 100003 + 1)
    cas, ecarts = 0, []
    for i in range(n):
        gen, concordance = generer_scenario_relevee(alea)
        problemes = [] if concordance else \
            ["concordance I http-08:R3 : le verdict de la feuille dévie du "
             "routage généré (D136 — le 5e argument, la politique)"]
        attendu = ModeleRoutageR3(gen).executer()
        problemes += SR3.jouer_r3(emu, _sc_r3(gen, attendu))
        cas += 1
        if problemes:
            ecarts.append((i, gen["entree"][:40], problemes[:3]))
    return cas, ecarts


# ============================================================================
# F2 — les domaines hérités sous les DEUX politiques (Q7 + la ligne)
# ============================================================================

def famille_heritage(emu_r3, emu_r2, graine: int, n: int) -> tuple[int, list]:
    alea = random.Random(graine * 100003 + 2)
    cas, ecarts = 0, []
    for i in range(n):
        gen, concordance = generer_scenario_herite(alea)
        problemes = [] if concordance else \
            ["concordance I : le verdict de la feuille dévie du domaine généré"]
        # Q7 — politique 0 : l'anti-régression R7 (traces normalisées,
        # l'ancêtre scellé 0.5.1 émulé contre la révision)
        sc_q7 = SR3.ScR3(f"#{i}", 0, gen["entree"], gen["script"], False,
                         False, b"", [], (0, 0, 0, 0), None, [], [], 0)
        problemes += SR3.differentiel_q7(emu_r2, emu_r3, sc_q7)
        # la RÉFÉRENCE R7 : l'ancêtre ÉMULÉ à politique 0 (jamais remodélisé)
        if gen["mode"] != "routed":
            emu_r2.politique = 0
            emu_r2.preparer()
            try:
                emu_r2.appeler(gen["script"])
                gen["reference"] = observer(emu_r2)
            except Exception as e:
                problemes.append(f"faute de l'ancêtre de référence : "
                                 f"{type(e).__name__} {e}")
                gen["reference"] = None
        if gen["mode"] == "routed" or gen.get("reference") is not None:
            attendu = ModeleRoutageR3(gen).executer()
            problemes += SR3.jouer_r3(emu_r3, _sc_r3(gen, attendu))
        cas += 1
        if problemes:
            ecarts.append((i, gen["entree"][:40], problemes[:3]))
    return cas, ecarts


# ============================================================================
# F3 — falsification : l'oracle DOIT pouvoir échouer (témoin armé)
# ============================================================================

def famille_falsification(ks: Ks, blobs: dict, emu_r2) -> tuple[int, list, int]:
    """(n_contrôles, verdicts, défauts) — les TREIZE mutations d'un point de
    la révision (harnais_session_r3.MUTATIONS_V4) ATTRAPÉES sur les scénarios
    du harnais (politique armée ET la branche Q7 à politique 0) ; le MODÈLE
    falsifié (la ligne maquillée) nommé par la confrontation ; le témoin
    intact VERT sur les MÊMES scénarios."""
    verdicts: list[str] = []
    defauts = 0
    chemin_r3 = os.path.join(ICI, "notation", "http-10-session-r3.asm")
    for nom, mutation in SR3.MUTATIONS_V4:
        blob_m = SR3.octets_mutation(ks, chemin_r3, SR3.RVA_SESSION_R3, mutation)
        blobs_m = dict(blobs)
        blobs_m["http-10-R3"] = blob_m
        emu_m = SR3.EmulateurSessionR3(blobs_m, SR3.RVA_SESSION_R3, SR3.CADRE_R2,
                                       politique=1, pushes=7)
        emu_m0 = SR3.EmulateurSessionR3(blobs_m, SR3.RVA_SESSION_R3, SR3.CADRE_R2,
                                        politique=0, pushes=7)
        attrapes = 0
        for sc in SR3.SCENARIOS:               # politique armée (jouer_r3 règle)
            try:
                if SR3.jouer_r3(emu_m, sc):
                    attrapes += 1
            except Exception:
                attrapes += 1                  # faute d'exécution = écart nommé
        try:                                   # la branche Q7 (politique 0) :
            for sc in SR3.SCENARIOS:           # seuls les scénarios SANS politique
                if sc.politique:               # ont un attendu Q7 valide (leçon D82)
                    continue
                emu_m0.politique = 0
                if SR3.HR2.jouer(emu_m0, sc) or \
                        SR3.differentiel_q7(emu_r2, emu_m0, sc):
                    attrapes += 1
                    break
        except Exception:
            attrapes += 1
        if attrapes == 0:
            defauts += 1
        verdicts.append(f"mutation http-10:R3 « {nom.split(' :')[0]} » : "
                        f"{'ATTRAPÉE' if attrapes else 'MANQUÉE'} ({attrapes} armes)")
    # le modèle falsifié — la confrontation DOIT nommer l'écart (la ligne
    # maquillée : le verdict de flux remappé, l'arme E1)
    emu_v = SR3.EmulateurSessionR3(blobs, SR3.RVA_SESSION_R3, SR3.CADRE_R2,
                                   politique=1, pushes=7)
    sc0 = SR3.SCENARIOS[0]
    wf_corrompu = [w.replace(b"v=0", b"v=1") if w.startswith(b"flux ") else w
                   for w in sc0.wf]
    corrompu = sc0._replace(wf=wf_corrompu)
    if SR3.jouer_r3(emu_v, corrompu):
        verdicts.append("modèle falsifié (la ligne maquillée v=0 -> v=1) : ATTRAPÉ")
    else:
        defauts += 1
        verdicts.append("modèle falsifié : MANQUÉ — la confrontation est creuse")
    # témoin intact — les mêmes scénarios restent verts
    emu_t = SR3.EmulateurSessionR3(blobs, SR3.RVA_SESSION_R3, SR3.CADRE_R2,
                                   politique=1, pushes=7)
    verts = sum(1 for sc in SR3.SCENARIOS if not SR3.jouer_r3(emu_t, sc))
    if verts != len(SR3.SCENARIOS):
        defauts += 1
    verdicts.append(f"témoin intact : {verts}/{len(SR3.SCENARIOS)} scénarios verts")
    return len(verdicts), verdicts, defauts


# ============================================================================
# Chargement (LA table d'intégration D92 + les révisions — source unique) et entrée
# ============================================================================

def charger_blobs(ks: Ks) -> tuple[dict, list[tuple]]:
    """Les vingt-neuf blocs hérités + l'ancêtre par LA table d'intégration
    D92 (harnais_session_r2.charger) sous silence, PUIS les DEUX révisions
    R3 assemblées de leurs notations (les octets réels — jamais deux
    sources) ; les contrôles V1 sont COLLECTÉS, pas imprimés."""
    collecte: list[tuple] = []
    veritable = SR2.controle
    SR2.controle = lambda nom, ok, detail="": collecte.append((nom, ok))
    try:
        blobs = SR2.charger(ks)
    finally:
        SR2.controle = veritable
    for rva, cle, bloc in ((SR3.RVA_CIBLE_R3, "http-08-R3", "http-08-cible-r3"),
                           (SR3.RVA_SESSION_R3, "http-10-R3",
                            "http-10-session-r3")):
        chemin = os.path.join(ICI, "notation", bloc + ".asm")
        b, declare = HS.octets_notation(ks, bloc, rva, chemin=chemin)
        collecte.append((f"V1 {bloc} == taille déclarée", len(b) == declare))
        blobs[cle] = b
    return blobs, collecte


VOLUMES = {"complet": (200, 150), "reduit": (8, 6)}


def executer(blobs: dict, graine: int = 1, volume: str = "complet") -> dict:
    """Le point d'entrée du build_m5.py — lève EchecOracle sur TOUT écart ;
    sinon retourne le verdict (les graines différencient les exécutions ;
    seuls les comptes hachés survivent au rapport de build)."""
    n1, n2 = VOLUMES.get(volume, VOLUMES["complet"])
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    emu_r3 = SR3.EmulateurSessionR3(blobs, SR3.RVA_SESSION_R3, SR3.CADRE_R2,
                                    politique=1, pushes=7)
    emu_r2 = SR3.EmulateurSessionR3(blobs, SR3.RVA_SESSION_R2, SR3.CADRE_R2,
                                    politique=0, pushes=5)
    familles: dict[str, str] = {}
    ecarts: list[str] = []
    cas, e1 = famille_relevee(emu_r3, graine, n1)
    familles["F1-relevee-D136"] = f"{cas} scénarios générés, {len(e1)} écart(s)"
    ecarts += [f"F1#{i} {h!r} — {'; '.join(p)}" for i, h, p in e1[:4]]
    cas, e2 = famille_heritage(emu_r3, emu_r2, graine, n2)
    familles["F2-heritage-Q7"] = f"{cas} scénarios générés, {len(e2)} écart(s)"
    ecarts += [f"F2#{i} {h!r} — {'; '.join(p)}" for i, h, p in e2[:4]]
    n_f3, verdicts, defauts = famille_falsification(ks, blobs, emu_r2)
    familles["F3-falsification"] = f"{n_f3} contrôles, {defauts} défaut(s)"
    ecarts += [v for v in verdicts if "MANQUÉ" in v]
    total = n1 + n2 + n_f3
    if len(e1) + len(e2) + defauts:
        raise EchecOracle(f"{len(e1) + len(e2) + defauts} écart(s) — "
                          + " | ".join(ecarts[:6]))
    empreinte = hashlib.sha256(
        f"{total}|{graine}|{volume}|".encode()
        + b"".join(k.encode() for k in sorted(familles))).hexdigest()[:16]
    return {"total_cas": total, "empreinte": empreinte, "graine": graine,
            "volume": volume, "familles": familles}


def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261103)
    parseur.add_argument("--volume", choices=["complet", "reduit"],
                         default="complet")
    args = parseur.parse_args()
    print("=== oracle_m5.py — l'oracle à scénarios étendu du relèvement (D136) ===")
    print(f"graine {args.graine} · volume {args.volume} · familles F1-F3 "
          "(relevée / domaines hérités + Q7 / falsification)")
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    blobs, collecte = charger_blobs(ks)
    ok_chargement = all(ok for _nom, ok in collecte)
    print(f"\n[chargement] {len(collecte)} contrôles V1 (table d'intégration "
          f"D92 + les révisions R3) : {'VERTS' if ok_chargement else 'ÉCHEC'}")
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
