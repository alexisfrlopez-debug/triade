#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harnais_session_r3.py — Harnais de http-10:R3 (0.6.0, D136 — le relèvement).

LA révision du jalon M5 côté orchestration : la session proxy 0.5.1 (http-10:R2,
embarquée scellée) reprend son comportement hérité TEL QUEL et AJOUTE le
routage du verdict « cible à relever » (http-08:R3 rax = 5, SOUS politique
armée) vers le tunnel tls-08 par LE MÊME chemin Q2' (port 443, la requête
réécrite en forme origine, la table des réponses INCHANGÉE) ET LA LIGNE DE
FLUX — la pièce d'interception du critère (b) : « flux <methode> <hote>:<port>
v=<verdict> e=<entrés> s=<sortis> », une ligne par session aboutie dont la
requête a été parsée, politique armée seulement. La notation R3 (2686 o, slot
0x81C0×0xAC0, padding 66 >= 16 — D8) est émulée à son RVA .text4 exact AVEC
les vrais octets de sa chaîne d'appel — L'INTÉGRATION LA PLUS LARGE DU
PROJET : TRENTE-ET-UN blocs réels (les vingt-neuf de R2 + http-08:R3
@0x8000 + http-10:R3 @0x81C0) + l'ANCIÊTRE scellé (http-10:R2 @0x74C0 avec
http-08:R2 @0x7340, embarqués 0.5.1) pour le différentiel. Vecteurs de la
spécification m5/I/http-10-session-r3.md :

  V1  round-trip de notation 100 % (taille == « Code : N o », padding >= 16)
      pour la révision ET les deux blocs .text4, sur la base des vingt-neuf
      blocs intégrés du harnais R2 (jamais deux sources) ;

  V2a DIFFÉRENTIEL D'ANCÊTRE SANS POLITIQUE (Q7 — l'anti-régression R7) :
      l'ancêtre http-10:R2 (octets scellés 0.5.1, assemblés à 0x74C0) et la
      révision sont émulés sur les MÊMES scénarios à R_POLITIQUE = 0 : les
      traces observables (lignes console, octets au client, résolutions,
      connexions, fermetures, spawns) comparées APRÈS NORMALISATION par la
      base du cadre de CHAQUE run (R3 : SEPT pushes au prologue — les
      compteurs rsi/rdi, P8 — la base descend de 0x10, l'alignement P5 est
      intact) : ÉCART ZÉRO sur TOUT scénario — « sans politique : R2 OCTET
      POUR OCTET sur tout chemin », aucune ligne de flux, aucun verdict 5 ;

  V2b oracle à scénarios étendu (D136) SOUS POLITIQUE ARMÉE : cible relevée
      saine (verdict 0, page relayée, ligne de flux exacte), certificat
      invalide relevé (verdict 3, 502 étiquetée, ligne v=3 — la LIGNE nomme
      la CAUSE, la réponse nomme l'effet, E1), port explicite du navigateur
      PERDU au relèvement (E2 : l'origine est l'HTTPS standard, port 443
      FORCÉ après le tri-entrée — la ligne porte le port effectif), garde
      corps sur cible relevée (501 honnête), amont injoignable (v=502),
      hôte tronqué à 14 (E3, la borne nommée), CONNECT (v=0, pompe
      détachée), 411/431 (la réponse nommée / la SENTINELLE : rien à
      nommer), accumulation morte (sentinelle), domaine https inchangé —
      chaque scénario vérifie la ligne de flux OCTET PAR OCTET contre le
      MODÈLE DE COMPOSITION (écrit depuis la spécification, jamais la
      notation), la réponse exacte au client, la compensation croisée PAR
      COMPTAGE, le paquet P6/P7 au passage de tls-08 et les compteurs P8
      (entrés = accumulation + corps pompé ; sortis = émissions .emettre ;
      les relais délégués ne sont JAMAIS comptés deux fois — sur un
      relèvement réussi, s=0 est la signature honnête du relais tls-08) ;

  V3  NON APPLICABLE (spec http-10:R3:V3 — héritage M3 : la session reste
      hors fuzz direct, ses entrées non fiables traversent les blocs fuzzés) ;

  V4  falsification : TREIZE mutations d'un seul point, STABLES EN TAILLE
      (leçon D82), chacune ATTRAPÉE (le verdict 5 non routé au dispatch ET
      à la garde, la force E2 amnésiée, la politique non passée à la
      feuille, la ligne émise sans politique, l'hôte non tronqué, le
      verdict de flux remappé, la sentinelle amnésiée, le défaut TLS dévié,
      le compteur sorti amnésié, la feuille rappelée à l'ancêtre R2) ; le
      témoin intact reste vert ;

  V6bis contrôle statique du prologue (héritage D63/D92 — cadre 0x13390
      INCHANGÉ : probing -0x1000..-0x13000, touche [rsp-0x13390]) + rejet
      I6'/I7 : appels directs ⊆ liste blanche héritage + http-08:R3 @0x8000
      (JAMAIS l'ancêtre http-08:R2 @0x7340), UN SEUL appel IAT (CloseHandle
      — la ligne de flux vit via tcp-11 et libc-04, appels DIRECTS
      hérités), aucun appel SSPI direct.

Règles shims PARTAGÉES avec harnais_session.py/harnais_session_r2.py (D90/
D92 — jamais deux sources de vérité, l'EmulateurSession R2 est SOUS-CLASSÉ) ;
la politique est un ÉTAT .data (R_POLITIQUE @0x3860, layout M5) écrit par
preparer() — lue UNE fois par la session (P7), passée en 5e argument à la
feuille (la loge vit SOUS le cadre), cachée à +0x70D0 pour la ligne (Q6/Q7).
LA LIGNE EST COMPOSÉE EN DEUX TEMPS (layout FLUX_PREF_LEN @+0x70D8) : le
préfixe « flux <méthode PAR TABLE> <hôte tronqué>: » au ROUTAGE (avant tout
relais — le tampon de requête appartient aux relais : http-09 y reçoit la
réponse, le corps pompé l'écrase ; la méthode vient de R_TAB_METHODES,
.rdata STABLE), le suffixe « v=… e=… s=… » à .fin — le modèle juge les
OCTETS de la ligne complète.

Usage : python3 harnais_session_r3.py [--graine G]
"""

from __future__ import annotations

import argparse
import os
import struct
import sys
from collections import namedtuple

ICI = os.path.dirname(os.path.abspath(__file__))
M4_DIR = os.path.join(ICI, os.pardir, "m4")
sys.path.insert(0, ICI)
sys.path.insert(0, M4_DIR)
sys.path.insert(0, os.path.join(M4_DIR, "outils"))
sys.path.insert(0, os.path.join(ICI, "outils"))

import layout as L  # noqa: E402  — m4/layout.py (via harnais_session_r2)

import harnais_session as HS  # noqa: E402
import harnais_session_r2 as HR2  # noqa: E402
from harnais_session_r2 import (  # noqa: E402
    ScriptR2, EmulateurSession, normaliser,
    TXT_400, TXT_431, TXT_501, TXT_411, TXT_505, TXT_502, TXT_TUNNEL,
    MSG_CONNEXION, MSG_TUNNEL, MSG_FIN,
    ZONE_PILE, RSP_ENTREE, CADRE_R2,
)
from harnais_session import (  # noqa: E402
    motif, clair_dm, OK, CONT, CONTEXTE_EXPIRE, CERT_INVALIDE,
    compter_compensation, lignes_notation, octets_notation,
)

import importlib.util  # noqa: E402
_spec5 = importlib.util.spec_from_file_location(
    "layout_m5", os.path.join(ICI, "layout.py"))
L5 = importlib.util.module_from_spec(_spec5)   # le plan M5 (source unique)
_spec5.loader.exec_module(L5)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

# --- Mémoire du harnais (.text4 NOUVELLE — les trois révisions M5) ----------------

ZONE_TEXT4, TAILLE_TEXT4 = 0x8000, 0x2000
RVA_CIBLE_R3 = 0x8000            # g80001 (http-08:R3 — m5/layout.py)
RVA_SESSION_R3, SLOT_R3 = 0x81C0, 0xAC0   # g80002 (http-10:R3)
RVA_SESSION_R2 = 0x74C0          # g70010 (l'ancêtre scellé 0.5.1)

CONNECTION, TUNJ, FIN = MSG_CONNEXION, MSG_TUNNEL, MSG_FIN
ETABLI, CERTL = L.TXT_TLS_ETABLI, L.TXT_TLS_CERT

REUSSITES, ECHECS = [], []


def controle(nom: str, ok: bool, detail: str = "") -> None:
    if ok:
        REUSSITES.append(nom)
        print(f"  [PASS] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append(nom)
        print(f"  [FAIL] {nom}" + (f" — {detail}" if detail else ""))


# --- Le modèle de composition (écrit depuis la SPÉCIFICATION — jamais la notation) -

def ligne_flux(methode: bytes, hote: bytes, port: int, verdict: int,
               e: int, s: int) -> bytes:
    """Q6 — « flux » + méthode + « » + hôte (TRONQUÉ à FLUX_HOTE_MAX) + «:» +
    port (LE CHAMP NUMÉRIQUE de tcp-11) + « v= » + verdict + « e= » + entrés
    + « s= » + sortis + CRLF. Les trois nombres en décimal minimal (libc-04),
    le port pareil (tcp-11 compose préfixe + itoa(port) + suffixe)."""
    h = hote[:L5.FLUX_HOTE_MAX]
    return (b"flux " + methode + b" " + h + b":" + str(port).encode()
            + b" v=" + str(verdict).encode()
            + b" e=" + str(e).encode() + b" s=" + str(s).encode() + b"\r\n")


# --- Émulateur de session R3 (hérite des shims D90/R2 — jamais deux sources) -------

class EmulateurSessionR3(EmulateurSession):
    """Un chargement = un émulateur NEUF (leçon D79). La RÉVISION vit en
    .text4 avec sa feuille http-08:R3 ; l'ANCÊTRE R2 reste chargé en .text3.
    La politique est un état .data écrit par preparer() (P7 : la session la
    lit UNE fois, la cache à +0x70D0 — le differentiel Q7 l'exige à 0)."""

    def __init__(self, blobs: dict, rva_session: int, cadre_taille: int,
                 politique: int = 0, pushes: int = 5):
        super().__init__(blobs, rva_session, cadre_taille)
        uc = self.uc
        uc.mem_map(ZONE_TEXT4, TAILLE_TEXT4)
        page = b"\xCC" * TAILLE_TEXT4
        for rva, cle in ((RVA_CIBLE_R3, "http-08-R3"),
                         (RVA_SESSION_R3, "http-10-R3")):
            b = blobs[cle]
            page = page[:rva - ZONE_TEXT4] + b + page[rva - ZONE_TEXT4 + len(b):]
        uc.mem_write(ZONE_TEXT4, page)
        self.text4 = bytes(uc.mem_read(ZONE_TEXT4, TAILLE_TEXT4))
        self.politique = politique
        # R3 : SEPT pushes au prologue (rbx, r12..r15, rsi, rdi — P8) : la
        # base du cadre descend de 0x10 (l'alignement P5 ≡ 0 mod 16 tient),
        # la normalisation du differentiel suit CHAQUE base
        self.rsp_session = RSP_ENTREE - pushes * 8 - cadre_taille

    def preparer(self, politique: int | None = None) -> None:
        super().preparer()
        if politique is not None:
            self.politique = politique
        self.uc.mem_write(L5.R_POLITIQUE, struct.pack("<Q", self.politique))

    def hygiene(self) -> list[str]:
        problemes = super().hygiene()
        if struct.unpack("<Q", bytes(self.uc.mem_read(L5.R_POLITIQUE, 8)))[0] \
                != self.politique:
            problemes.append("R_POLITIQUE .data modifiée (P7 : lue, jamais écrite)")
        if bytes(self.uc.mem_read(ZONE_TEXT4, TAILLE_TEXT4)) != self.text4:
            problemes.append(".text4 altérée en run (auto-modification)")
        return problemes


# --- Scénarios ---------------------------------------------------------------------

ScR3 = namedtuple("ScR3", "nom politique entree script tls diverge client wf "
                          "comptes paquet ports gai ct")

HOTE = b"exemple.fr"
HOTE_LONG = b"un-hote-tres-long.fr"           # 20 o > 14 : tronqué « un-hote-tres-l »
GET_ABS = b"GET http://exemple.fr/chemin HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"
GET_ABS_8080 = (b"GET http://exemple.fr:8080/chemin HTTP/1.1\r\n"
                b"Host: exemple.fr:8080\r\n\r\n")
GET_ORI = b"GET /chemin HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"
GET_HTTPS = b"GET https://exemple.fr/chemin HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"
GET_LONG = b"GET /chemin HTTP/1.1\r\nHost: un-hote-tres-long.fr\r\n\r\n"
POST_SANS_CL = b"POST /x HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"
POST_CORPS_ABS = (b"POST http://exemple.fr/s HTTP/1.1\r\nHost: exemple.fr\r\n"
                  b"Content-Length: 10\r\n\r\n0123456789")
CONNECT_REQ = b"CONNECT exemple.fr:443 HTTP/1.1\r\nHost: exemple.fr:443\r\n\r\n"
GET_HTTP_MAJ = b"GET HTTP://exemple.fr/ HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"
REQUETE_R = b"GET /chemin HTTP/1.1\r\nHost: exemple.fr\r\n\r\n"   # la réécriture
REQUETE_8080 = b"GET /chemin HTTP/1.1\r\nHost: exemple.fr:8080\r\n\r\n"

SCENARIOS = [
    ScR3("relevée SAINNE — le navigateur http:// relevé vers le tunnel "
         "(P7/Q2' : MÊME chemin que https, port 443, réécriture origine)",
         1, GET_ABS,
         ScriptR2(isc=[(CONT, 64), (OK, 32)],
                  recv=[GET_ABS, 128, 121, 21, 0],
                  dm=[(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)]),
         True, False, clair_dm(0, 100),
         [CONNECTION, ETABLI, ligne_flux(b"GET", HOTE, 443, 0, 59, 0), FIN],
         (1, 1, 1, 2), (HOTE, 443, REQUETE_R), [443], [HOTE], 0),
    ScR3("relevée CERTIFICAT invalide — v=3 LA CAUSE, 502 étiquetée l'effet "
         "(E1 : jamais de remappage muet), s=34 les octets émis",
         1, GET_ABS, ScriptR2(isc=[(CERT_INVALIDE, 0)], recv=[GET_ABS, 16, 0]),
         True, False, L.TXT_502_CERT,
         [CONNECTION, CERTL, ligne_flux(b"GET", HOTE, 443, 3, 59, 34), FIN],
         (1, 1, 1, 2), (HOTE, 443, REQUETE_R), [443], [HOTE], 0),
    ScR3("relevée + corps (CL > 0) → 501 refus honnête (la garde .trancher "
         "s'applique AUSSI à la relevée — P7)",
         1, POST_CORPS_ABS, ScriptR2(recv=[POST_CORPS_ABS, 16, 0]),
         True, False, TXT_501,
         [CONNECTION, ligne_flux(b"POST", HOTE, 443, 501, 85, 31), FIN],
         (0, 0, 0, 1), None, [], [], 0),
    ScR3("relevée amont injoignable (résolution dans tls-08) → v=7 LE VERDICT "
         "tls TRANSPORTÉ (la ligne nomme la CAUSE — cible injoignable — la "
         "réponse 502 nomme l'effet, E1 ; le domaine Q6 : 2..7 verdicts "
         "tls-08 TELS QUELS)",
         1, GET_ABS, ScriptR2(gai=[0x2AFA], recv=[GET_ABS]),
         True, False, TXT_502,
         [CONNECTION, ligne_flux(b"GET", HOTE, 443, 7, 59, 40), FIN],
         (0, 0, 0, 1), (HOTE, 443, REQUETE_R), [], [HOTE], 0),
    ScR3("port EXPLICITE du navigateur PERDU au relèvement (E2 : l'origine "
         "est l'HTTPS standard — 443 FORCÉ après le tri-entrée, la ligne "
         "porte le port effectif, l'explicite :8080 n'apparaît nulle part "
         "hors l'en-tête Host du navigateur, transporté tel quel)",
         1, GET_ABS_8080,
         ScriptR2(isc=[(CONT, 64), (OK, 32)],
                  recv=[GET_ABS_8080, 128, 121, 21, 0],
                  dm=[(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)]),
         True, False, clair_dm(0, 100),
         [CONNECTION, ETABLI, ligne_flux(b"GET", HOTE, 443, 0, 69, 0), FIN],
         (1, 1, 1, 2), (HOTE, 443, REQUETE_8080), [443], [HOTE], 0),
    ScR3("origine + politique — la forme origine reste le chemin M3 (PAS de "
         "relèvement : la politique n'invente rien), ligne quand même (v=0 ; "
         "s=42 : la requête réécrite EST l'émission claire de la session, "
         "P8 — la RÉPONSE seule est déléguée à http-09, jamais comptée deux "
         "fois)",
         1, GET_ORI, ScriptR2(recv=[GET_ORI, 16, 0]),
         False, False, motif(1, 16),
         [CONNECTION, ligne_flux(b"GET", HOTE, 80, 0, 42, 42), FIN],
         (0, 0, 0, 2), None, [80], [HOTE], 0),
    ScR3("hôte > 14 octets → TRONQUÉ (E3 : la borne FLUX_HOTE_MAX est un "
         "état de la ligne, jamais une perte silencieuse de verdict)",
         1, GET_LONG, ScriptR2(recv=[GET_LONG, 16, 0]),
         False, False, motif(1, 16),
         [CONNECTION, ligne_flux(b"GET", HOTE_LONG, 80, 0, 52, 52), FIN],
         (0, 0, 0, 2), None, [80], [HOTE_LONG], 0),
    ScR3("CONNECT + politique — le tunnel aveugle (v=0 tunnel établi, "
         "s=30 les octets du 200, la pompe détachée spawnée)",
         1, CONNECT_REQ, ScriptR2(recv=[CONNECT_REQ, 16, 0]),
         False, False, TXT_TUNNEL,
         [CONNECTION, TUNJ, ligne_flux(b"CONNECT", HOTE, 443, 0, 57, 30), FIN],
         (0, 0, 0, 2), None, [443], [HOTE], 1),
    ScR3("POST origine sans Content-Length → 411 (v=411 la réponse nommée, "
         "s=33), le routage AVANT le refus : la ligne porte l'hôte effectif",
         1, POST_SANS_CL, ScriptR2(recv=[POST_SANS_CL]),
         False, False, TXT_411,
         [CONNECTION, ligne_flux(b"POST", HOTE, 80, 411, 38, 33), FIN],
         (0, 0, 0, 1), None, [], [], 0),
    ScR3("tête trop grande → 431 : la SENTINELLE tient (Q6 — la requête "
         "n'est pas identifiable, AUCUNE ligne, même politique armée)",
         1, b"GET /" + b"A" * 8197 + b" HTTP/1.1\r\nHost: h\r\n\r\n",
         ScriptR2(recv=[b"GET /" + b"A" * 8197 + b" HTTP/1.1\r\nHost: h\r\n\r\n"]),
         False, False, TXT_431, [CONNECTION, FIN],
         (0, 0, 0, 1), None, [], [], 0),
    ScR3("client parti en accumulation → sentinelle (Q6 : accumulation "
         "morte, rien à nommer — fin SANS réponse ni ligne)",
         1, b"GET /x HTTP/1.1", ScriptR2(recv=[b"GET /x HTTP/1.1", 0]),
         False, False, b"", [CONNECTION, FIN],
         (0, 0, 0, 1), None, [], [], 0),
    ScR3("« HTTP:// » mal cassé → le refus hérité (Q5 http-08:R3 : casse "
         "byte-exact, AUCUNE tolérance nouvelle) — 501 SANS ligne (le "
         "refus précède le routage : la sentinelle demeure)",
         1, GET_HTTP_MAJ, ScriptR2(recv=[GET_HTTP_MAJ]),
         False, False, TXT_501, [CONNECTION, FIN],
         (0, 0, 0, 1), None, [], [], 0),
    ScR3("domaine https + politique — INCHANGÉ (Q4 hérité : la révision ne "
         "touche pas https, la ligne porte le même verdict 0)",
         1, GET_HTTPS,
         ScriptR2(isc=[(CONT, 64), (OK, 32)],
                  recv=[GET_HTTPS, 128, 121, 21, 0],
                  dm=[(OK, 5, 100, 16), (CONTEXTE_EXPIRE, 5, 0, 16)]),
         True, False, clair_dm(0, 100),
         [CONNECTION, ETABLI, ligne_flux(b"GET", HOTE, 443, 0, 60, 0), FIN],
         (1, 1, 1, 2), (HOTE, 443, REQUETE_R), [443], [HOTE], 0),
    ScR3("relevée SAINNE SANS politique — R2 octet pour octet (Q7 : le "
         "chemin M3 clair, port 80, AUCUNE ligne)",
         0, GET_ABS, ScriptR2(recv=[GET_ABS, 16, 0]),
         False, False, motif(1, 16), [CONNECTION, FIN],
         (0, 0, 0, 2), None, [80], [HOTE], 0),
]


# --- Jouer un scénario (la politique est un état .data — P7) ------------------------

def jouer_r3(emu: EmulateurSessionR3, sc: ScR3) -> list[str]:
    emu.politique = sc.politique
    return HR2.jouer(emu, sc)


# --- V2a : le différentiel d'ancêtre SANS politique (Q7) ----------------------------

def differentiel_q7(emu_r2: EmulateurSessionR3, emu_r3: EmulateurSessionR3,
                    sc: ScR3) -> list[str]:
    """Q7 — R_POLITIQUE = 0 : la révision R3 est l'ancêtre R2 OCTET POUR
    OCTET : traces normalisées identiques sur TOUT scénario (lignes console
    comprises — aucune ligne de flux n'existe sans politique)."""
    emu_r2.politique = 0
    emu_r3.politique = 0
    emu_r2.preparer()
    emu_r3.preparer()
    try:
        emu_r2.appeler(sc.script)
        emu_r3.appeler(sc.script)
    except Exception as e:
        return [f"faute d'exécution au différentiel : {type(e).__name__} {e}"]
    t2 = normaliser(emu_r2.appels, emu_r2.rsp_session)
    t3 = normaliser(emu_r3.appels, emu_r3.rsp_session)
    if t2 != t3:
        k = next((i for i in range(max(len(t2), len(t3)))
                  if i >= len(t2) or i >= len(t3) or t2[i] != t3[i]), 0)
        return [f"trace #{k} : ancêtre {t2[k] if k < len(t2) else None} != "
                f"révision {t3[k] if k < len(t3) else None}"]
    return []


# --- V4 : falsification (mutations d'un point, stables en taille) -------------------

def octets_mutation(ks: Ks, chemin: str, rva: int, mutation: tuple) -> bytes:
    """Mutation d'un point de la notation RÉSOLUE. Trois formes : (avant,
    apres) — ligne unique contenant `avant` ; (ligne, suivant, old, new) —
    la ligne `ligne` dont la SUIVANTE commence par `suivant` ; (ligne,
    suivant, apres, old, new) — la ligne `ligne` dont la suivante commence
    par `suivant` ET la SUIVANTE-DE-LA-SUIVANTE par `apres` (désambiguïse
    les TRIPLETS « cmp …, 5 » de la force E2, du dispatch .trancher et du
    second dispatch post-réécriture — trois jumeaux, un seul contexte)."""
    lignes = lignes_notation(chemin)
    if len(mutation) == 2:
        avant, apres = mutation
        cibles = [i for i, l in enumerate(lignes) if avant in l]
        if len(cibles) != 1:
            raise RuntimeError(f"mutation ambiguë ({len(cibles)}) : {avant!r}")
        lignes[cibles[0]] = lignes[cibles[0]].replace(avant, apres)
    elif len(mutation) == 4:
        ligne_cible, suivant, old, new = mutation
        cibles = [i for i, l in enumerate(lignes)
                  if l == ligne_cible and i + 1 < len(lignes)
                  and lignes[i + 1].startswith(suivant)]
        if len(cibles) != 1:
            raise RuntimeError(f"mutation à contexte ambiguë ({len(cibles)}) : "
                               f"{ligne_cible!r} + {suivant!r}")
        lignes[cibles[0]] = lignes[cibles[0]].replace(old, new)
    else:
        ligne_cible, suivant, apres, old, new = mutation
        cibles = [i for i, l in enumerate(lignes)
                  if l == ligne_cible and i + 2 < len(lignes)
                  and lignes[i + 1].startswith(suivant)
                  and lignes[i + 2].startswith(apres)]
        if len(cibles) != 1:
            raise RuntimeError(f"mutation à contexte ambiguë ({len(cibles)}) : "
                               f"{ligne_cible!r} + {suivant!r} + {apres!r}")
        lignes[cibles[0]] = lignes[cibles[0]].replace(old, new)
    sortie, adresse = [], rva
    for ligne in lignes:
        enc, _ = ks.asm(ligne, adresse)
        if not enc:
            raise RuntimeError(f"ligne inassemblable à 0x{adresse:x} : {ligne!r}")
        sortie.append(bytes(enc))
        adresse += len(enc)
    return b"".join(sortie)


MUTATIONS_V4 = [
    ("M1 le verdict 5 non routé au dispatch (cmp 5 → 6 : la relevée tombe "
     "dans le refus 400 — P7 morte)",
     ("cmp rax, 5", "cmp rax, 6")),
    ("M2 la garde .trancher amnésique pour la relevée (un corps relevé "
     "serait pompé en clair vers l'origine)",
     ("cmp qword ptr [rsp + 0x7010], 5", "je ", "5", "6")),
    ("M3 la force E2 amnésiée (cmp 5 → 6 à la force : le port explicite du "
     "navigateur (:8080) gagnerait — un relèvement vers :8080 serait une "
     "invention)",
     ("cmp qword ptr [rsp + 0x7010], 5", "jne ",
      "mov dword ptr [rsp + 0x6FB0], 443", "5", "6")),
    ("M12 le SECOND dispatch amnésique pour la relevée (cmp 5 → 6 post-"
     "réécriture : la relevée tomberait dans l'émission claire .emission_"
     "amont — le tunnel ne serait jamais pris, LE défaut que la révision "
     "corrige)",
     ("cmp qword ptr [rsp + 0x7010], 5", "jne ",
      "mov rax, qword ptr [rsp + 0x6FA0]", "5", "6")),
    ("M4 la politique non passée à la feuille (la loge 5 reçoit la longueur "
     "d'accumulation : la feuille croit la politique armée)",
     ("mov qword ptr [rsp + 0x28], rax", "mov qword ptr [rsp + 0x28], r13")),
    ("M5 la ligne émise sans politique (la cache déviée +0x70D8 — la loge "
     "du préfixe : le canari/la longueur lus comme « armée » — Q7 morte au "
     "niveau du journal)",
     ("mov qword ptr [rsp + 0x70D0], rax", "mov qword ptr [rsp + 0x70D8], rax")),
    ("M6 l'hôte non tronqué (la borne 14 → 24 à la composition : la ligne "
     "dépasserait la borne tcp-11, E3 morte)",
     ("cmp r11, 14", "cmp r11, 24")),
    ("M7 le verdict de flux remappé (la cause tls remplacée par la socket "
     "cliente — la ligne mentirait, E1 morte)",
     ("mov qword ptr [rsp + 0x7028], rax", "mov qword ptr [rsp + 0x7028], rbx")),
    ("M8 la sentinelle amnésiée (init -1 → 0 : les sessions non "
     "identifiables émettraient une ligne qui porte du vide)",
     ("mov qword ptr [rsp + 0x7028], -1", "mov qword ptr [rsp + 0x7028], 0")),
    ("M9 le défaut TLS 443 dévié (80 : la cible https serait jointe en "
     "clair — attrapée par le domaine https)",
     ("mov r8d, 443", "mov r8d, 80")),
    ("M10 le compteur sorti amnésié (add rdi ← rdx : la ligne mentirait sur "
     "les octets émis, P8 morte)",
     ("add rdi, rax", "add rdi, rdx")),
    ("M11 la feuille rappelée à l'ANCIÊTRE http-08:R2 @0x7340 (la politique "
     "n'atteindrait jamais le parseur — I6'/I7)",
     ("call 0x8000", "call 0x7340")),
    ("M13 la méthode hors table (le préfixe relirait le span du tampon "
     "recyclé : shl 4 → shl 0, l'entrée 0 serait lue — la ligne "
     "porterait le mot « flux » comme méthode)",
     ("shl rax, 4", "shl rax, 0")),
]


# --- V6bis : contrôle statique — prologue + rejet I6'/I7 ---------------------------

BLANCHE_I7 = {0x4140, 0x4180, 0x41C0, 0x4300, 0x4400, 0x4B00, 0x4C00, 0x4C80,
              0x4F40, 0x5080, 0x5140, 0x5200, 0x54C0,      # héritage M2/M3
              0x1200, 0x1280,                               # libc-03/libc-04 (I7 :
              # la ligne de flux vit via tcp-11 ET libc-04/libc-03 — appels
              # DIRECTS hérités du suffixe numérique)
              0x6D40,                                        # tls-08 (Q2')
              0x8000}                                        # http-08:R3 (P7)


def controle_statique(lignes: list[str], rva: int, slot: int, brut: str = "") -> list[str]:
    import re
    problemes: list[str] = []
    texte = "\n".join(lignes[:14])
    if "mov r10, -0x1000" not in texte:
        problemes.append("prologue : init du probing absente")
    if "mov rax, qword ptr [rsp + r10]" not in texte:
        problemes.append("prologue : touche de boucle absente")
    if "sub r10, 0x1000" not in texte or "cmp r10, -0x13000" not in texte:
        problemes.append("prologue : bornes de la boucle de probing fautives")
    if "mov rax, qword ptr [rsp - 0x13390]" not in texte:
        problemes.append("prologue : touche finale du bas de cadre absente")
    if "sub rsp, 0x13390" not in texte:
        problemes.append("prologue : cadre de session 0x13390 absent")
    if "push rsi" not in texte or "push rdi" not in texte:
        problemes.append("prologue : les compteurs P8 (rsi/rdi) ne sont pas "
                         "sauvegardés (7 pushes attendus)")
    internes = lambda c: rva <= c < rva + slot
    for ligne in lignes:
        m = re.match(r"^call (0x[0-9a-f]+)$", ligne)
        if m:
            cible = int(m.group(1), 16)
            if cible not in BLANCHE_I7 and not internes(cible):
                problemes.append(f"appel direct hors liste blanche : 0x{cible:x}")
                break
    iat = [ligne for ligne in lignes if ligne.startswith("call qword ptr")]
    if len(iat) != 1:
        problemes.append(f"{len(iat)} appels IAT != 1 (CloseHandle attendu — I7)")
    elif "= 0x20f8" not in brut:
        problemes.append("l'appel IAT ne résout pas vers CloseHandle @0x20F8")
    return problemes


# --- main ---------------------------------------------------------------------------

def main() -> int:
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--graine", type=int, default=20261103)
    args = parseur.parse_args()

    print("=== harnais_session_r3.py — http-10:R3 (0.6.0 : routage du "
          "relèvement + ligne de flux) ===")
    print(f"graine {args.graine} · intégration : 31 blocs réels + l'ancêtre "
          "scellé 0.5.1 (http-10:R2 @0x74C0 + http-08:R2 @0x7340)")

    ks = Ks(KS_ARCH_X86, KS_MODE_64)

    print("\n[V1] round-trip de notation")
    blobs = HR2.charger(ks)      # les 29 blocs hérités + l'ancêtre (R2)
    controle("V1 héritage : les 29 blocs intégrés round-trip (harnais R2)",
             not HR2.ECHECS, f"{len(HR2.REUSSITES)} contrôles")
    HR2.REUSSITES.clear(), HR2.ECHECS.clear()
    for rva, cle, bloc in ((RVA_CIBLE_R3, "http-08-R3", "http-08-cible-r3"),
                           (RVA_SESSION_R3, "http-10-R3", "http-10-session-r3")):
        chemin = os.path.join(ICI, "notation", bloc + ".asm")
        b, d = octets_notation(ks, bloc, rva, chemin=chemin)
        blobs[cle] = b
        controle(f"V1 {bloc} == taille déclarée (@{rva:#x})", len(b) == d,
                 f"{len(b)} o")
    blob_r3 = blobs["http-10-R3"]
    controle("V1 http-10-session-r3 : padding du slot >= 16 (D8)",
             SLOT_R3 - len(blob_r3) >= 16, f"{SLOT_R3 - len(blob_r3)} o")

    emu_r3 = EmulateurSessionR3(blobs, RVA_SESSION_R3, CADRE_R2,
                                politique=0, pushes=7)
    emu_r2 = EmulateurSessionR3(blobs, RVA_SESSION_R2, CADRE_R2,
                                politique=0, pushes=5)

    print("\n[V2] oracle à scénarios (politique armée — ligne de flux OCTET "
          "PAR OCTET contre le modèle) + différentiel d'ancêtre SANS "
          "politique (Q7 : R2 octet pour octet)")
    for sc in SCENARIOS:
        problemes = jouer_r3(emu_r3, sc)
        problemes += differentiel_q7(emu_r2, emu_r3, sc)
        ligne = next((w for w in sc.wf if w.startswith(b"flux ")), None)
        detail = (f"ligne « {ligne[:-2].decode()} »" if ligne
                  else "aucune ligne (sentinelle)")
        controle(f"scénario « {sc.nom} »", not problemes,
                 "; ".join(problemes[:3]) if problemes
                 else f"politique={sc.politique}, {detail}, "
                      f"{len(emu_r3.appels)} appels")

    print("\n[V3] NON APPLICABLE — spec http-10:R3:V3 : la session reste "
          "hors fuzz direct (héritage M3 des orchestrateurs)")
    controle("V3 écarté conformément à la spécification (traçabilité)", True)

    print("\n[V4] falsification — treize mutations d'un point, chacune attrapée")
    chemin_r3 = os.path.join(ICI, "notation", "http-10-session-r3.asm")
    for nom, mutation in MUTATIONS_V4:
        blob_m = octets_mutation(ks, chemin_r3, RVA_SESSION_R3, mutation)
        blobs_m = dict(blobs)
        blobs_m["http-10-R3"] = blob_m
        emu_m = EmulateurSessionR3(blobs_m, RVA_SESSION_R3, CADRE_R2,
                                   politique=1, pushes=7)
        emu_m0 = EmulateurSessionR3(blobs_m, RVA_SESSION_R3, CADRE_R2,
                                    politique=0, pushes=7)
        attrapes = 0
        for sc in SCENARIOS:
            try:
                if jouer_r3(emu_m, sc):
                    attrapes += 1
            except Exception:
                attrapes += 1          # faute d'exécution = écart nommé
        try:                           # la Q7 armée aussi (mutations M4/M5) :
            for sc in SCENARIOS:       # SANS politique, seuls les scénarios à
                if sc.politique:       # politique 0 ont un attendu valide (un
                    continue           # scénario armé y échouerait TOUJOURS —
                emu_m0.politique = 0   # l'arme serait creuse, leçon D82)
                if HR2.jouer(emu_m0, sc) or differentiel_q7(emu_r2, emu_m0, sc):
                    attrapes += 1
                    break
        except Exception:
            attrapes += 1
        controle(f"mutation « {nom} » ATTRAPÉE", attrapes > 0,
                 f"{attrapes} armes en écart")
    emu_t = EmulateurSessionR3(blobs, RVA_SESSION_R3, CADRE_R2,
                               politique=1, pushes=7)
    verts = sum(1 for sc in SCENARIOS if not jouer_r3(emu_t, sc))
    controle("témoin intact : VERT sur les mêmes scénarios",
             verts == len(SCENARIOS), f"{verts}/{len(SCENARIOS)}")

    print("\n[V6bis] contrôle statique — prologue 0x13390 (D63/D92) + "
          "compteurs P8 + rejet I6'/I7")
    lignes = lignes_notation(chemin_r3)
    with open(chemin_r3, encoding="utf-8") as f:
        brut = f.read()
    problemes = controle_statique(lignes, RVA_SESSION_R3, SLOT_R3, brut)
    controle("prologue : probing -0x1000..-0x13000, touche [rsp-0x13390], "
             "sub rsp, 0x13390, 7 pushes (P8) ; I6'/I7 : appels ⊆ liste "
             "blanche + http-08:R3 @0x8000, un seul IAT (CloseHandle)",
             not problemes, "; ".join(problemes))

    print("\n" + "=" * 70)
    print(f"BILAN : {len(REUSSITES)} PASS, {len(ECHECS)} ÉCHEC")
    for nom in ECHECS:
        print(f"  FAIL {nom}")
    print("=" * 70)
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main())
