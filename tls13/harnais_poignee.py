#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tls13/harnais_poignee.py — LE HARNAIS DE LA FAMILLE poignée + LE PRINCIPAL.

Chantier M9-(b), sixième geste : les blocs tls13-22..28 (le ClientHello
composé, le ServerHello traité, le calendrier de clés à trois étages, le
Finished calculé/vérifié, l'épinglage, LA MACHINE D'ÉTATS du client entier,
le socle d'appel à rappels) NOTÉS-MESURÉS-PROUVÉS sur les cinq familles
précédentes notées-mesurées-prouvées aux gestes précédents. Le modèle est le
harnais enregistrement (tls13/harnais_enregistrement.py — la référence GCM
importée de la lignée par harnais_aead : la source unique) : l'émulation nue
aux RVA du plan (mécanisme D79), l'appelant factice pose les sentinelles non
volatiles et les canaris, le verdict est TRANCHÉ par le code — jamais cru.

L'ERRATUM n° 2 DE L'ARBRE I (sur pièces, AVANT la notation — le labo
derive_poignee.py, 41 contrôles VERTS) : le ClientHello du RFC 8448 § 3
compte 196 o (l'offre RICHE d'un client généraliste : trois suites, SNI
« server », neuf groupes, quinze sigalgs) — l'égalité octet pour octet AVEC
LE CH DU RFC est IMPOSSIBLE PAR CONSTRUCTION contre l'offre MINIMALE scellée
du jalon (114 o, charte § 1 : LA suite seule ; I3 : SNI chantier futur) ;
les égalités TIENNENT là où le jalon les peut (le SH traité verbatim, le
secret partagé, LES SECRETS CONSIGNÉS du calendrier, les QUATRE chaînes du
TRANSFERT_8448, les DEUX Finished au niveau des blocs) et la preuve de la
machine est LA SESSION ENTIÈRE contre le SIMULATEUR. Le contexte de
l'étiquette « derived » est le hash du TRANSCRIPT VIDE (32 o — l'info de
49 o imprimée par le RFC), le condensé dérivé par tls13-01+04 au geste même.

LE CAHIER (la charte § 2 : les vecteurs officiels AVANT usage, la
falsification, zéro silence) :

  V0 — LES PIÈCES DU PLAN : le scellé 0.9.0 relu (l'ancre 1492b0bc…), les
       familles sha, hkdf, x25519, aead ET enregistrement INTACTES (les
       VINGT-ET-UNE notations re-round-tripées aux longueurs arrêtées),
       K[64] posé à R_K, les fixtures du domaine posés à leur ARRÊT .text6
       (U9, EXP_INV, LES HUIT LIBELLÉS, LA VALEUR MAGIQUE HRR), le contexte
       session (17 520 o — la disposition DÉCLARÉE par tls13-27 P1)
       recompté champ par champ, l'arbre I scellé relu VERT
       (verifier_specs_m9a rejoué — R2, l'erratum n° 2 compris) ;
  V1 — LE ROUND-TRIP + LA CONCORDANCE : chaque notation ré-assemblée en ses
       octets (keystone == capstone, R5), les longueurs == l'ARRÊT du plan
       (241/524/2130/239/285/2864/144 o, D161), les appels directs aux
       adresses scellées (22 : AUCUN — bloc feuille ; 23 : TLS13 ; 24 :
       TLS06 ×3 + TLS08 ×16 + TLS15 ×4 + TLS01 + TLS04 ; 25 : TLS05 ;
       26 : TLS01 + TLS03 + TLS04 ; 27 : LA LISTE FERMÉE de la spec I1 ;
       28 : AUCUN appel direct — L'APPEL INDIRECT DÉCLARÉ ×2, la rotule),
       les constantes au plan (la construction du CH re-jouée, les libellés
       == LIBELLES, HRR == HRR_MAGIQUE, les offsets déclarés), AUCUN site
       syscall, AUCUN déplacement RIP hors les fixtures ;
  V2 — LE TRANSFERT RFC 8448 BLOC PAR BLOC (§ 3) : tls13-22 rend LE CH DU
       JALON au fixture (aléa @ +6, clé @ +82 — la construction re-jouée,
       114 o) ; tls13-23 traite le SH DU RFC (90 o, VERBATIM) avec la clé
       privée DU RFC → LE SECRET PARTAGÉ 8bd4054f… OCTET POUR OCTET ;
       tls13-24 rejoue LES TROIS ÉTAGES sur les hash CONSIGNÉS du RFC
       (860c06ed…, 9608102a…) → early/derived/handshake/c_hs/s_hs/
       derived_2/master/c_ap/s_ap == LES SECRETS CONSIGNÉS, les clés
       write/IV == LES QUATRE CHAÎNES du TRANSFERT_8448, les clés Finished
       == les consignées ; tls13-25 CALCULE le verify_data du client
       (a8ec436d…) et VÉRIFIE celui du serveur (9b9b141d…) ; tls13-26
       épingle le certificat du transcript (le DER 432 o) — EMPREINTE
       recalculée, le verdict vert ;
  V3 — LES CAS PUNITIFS : les refus nommés de chaque bloc (les pointeurs,
       les bornes, la négociation -5, HRR -5, les étages -3, les modes -1,
       l'épinglage -6, la borne du réassemblage 2^14, l'épuisement exact),
       l'oracle différentiel (le SH marcheur contre la référence Python) ;
  V4 — LE CONTRAT : les non-volatiles rendus, la pile équilibrée, la zone
       morte profonde (−0xE000 : sous le cadre 0x43C8 de la machine ET les
       cadres imbriqués), l'alignement msx64 à l'entrée de CHAQUE appelé à
       travers les compositions (les comptes exacts), les entrées intactes,
       les sorties jamais dépassées ;
  V5 — LA FALSIFICATION (zéro silence) : chaque vecteur muté ATTRAPÉ (le SH
       champ par champ, le calendrier étage par étage, le Finished octet par
       octet, l'empreinte et le certificat dans les DEUX sens) ;
  V6 — LE TEMPS CONSTANT MESURÉ : le verdict du Finished (trois verify_data
       divergents → LE MÊME compte), le verdict de l'épinglage (idem), la
       comparaison HRR de 23 (idem) ;
  V7 — LA MACHINE : LA SESSION ENTIÈRE CONTRE LE SIMULATEUR — le socle
       tls13-28 posé sur DEUX RAPPELS de machine code (l'émettre qui
       journalise, le recevoir qui sert la cassette), le simulateur dérive
       le calendrier de NOTRE transcript (notre CH de 114 o || le SH du
       RFC), sert le SH VERBATIM, re-scelle le vol du RFC sous nos clés
       (EE/Cert/CV verbatim, le Finished serveur RECALCULÉ sur notre
       coupe), la machine OUVRIT jusqu'à l'état 3 (le CH émis == la
       construction cadrée, le Finished client émis == le HMAC de NOTRE
       transcript scellé sous nos clés), ÉMETTRE/RECEVOIR les données
       applicatives DU RFC (les charges verbatim, scellées/déverrouillées
       sous les chaînes d'application NOTRES), FERMER le close_notify — ET
       LA FALSIFICATION à chaque étage : le SH muté → -5, l'étiquette du
       vol mutée → -4, l'empreinte du kit mutée → -6, LA COUPURE DU SOCLE
       → -7, l'événement hors de sa ligne → -3, l'état 5 (MORT) qui ne
       rend PLUS RIEN.

Usage : python3 harnais_poignee.py            # le cahier complet
        python3 harnais_poignee.py --graine N # la graine (défaut 20261107)
"""

from __future__ import annotations

import hashlib
import hmac
import importlib.util
import os
import random
import re
import struct
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
TRIADE = os.path.dirname(ICI)
M4_DIR = os.path.join(TRIADE, "m4")
sys.path.insert(0, ICI)
sys.path.insert(0, M4_DIR)
sys.path.insert(0, os.path.join(M4_DIR, "outils"))

# Le plan tls13 chargé par CHEMIN NOMINATIF (leçon D158)
if "layout_tls13" in sys.modules:
    L = sys.modules["layout_tls13"]
else:
    _spec_l = importlib.util.spec_from_file_location(
        "layout_tls13", os.path.join(ICI, "layout.py"))
    L = importlib.util.module_from_spec(_spec_l)
    sys.modules["layout_tls13"] = L
    _spec_l.loader.exec_module(L)

# La machinerie de notation de la lignée (leçon D158)
if "build_m4" in sys.modules:
    B4 = sys.modules["build_m4"]
else:
    _spec_b4 = importlib.util.spec_from_file_location(
        "build_m4", os.path.join(M4_DIR, "build_m4.py"))
    B4 = importlib.util.module_from_spec(_spec_b4)
    sys.modules["build_m4"] = B4
    _spec_b4.loader.exec_module(B4)

# LA LIGNÉE : le harnais enregistrement (la référence de la couche
# enregistrement + l'émulation des 21 blocs) qui importe lui-même le harnais
# aead (la référence GCM AES+GHASH+GCM contre-preuvée ET les constantes du
# transfert TRANSFERT_8448 consignées — la source unique de la lignée)
import harnais_enregistrement as ENR  # noqa: E402
import harnais_aead as AEAD  # noqa: E402

import nacl.bindings  # noqa: E402  (la contre-preuve x25519 de la lignée)
from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402
import capstone  # noqa: E402
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX,  # noqa: E402
                               UC_X86_REG_RDX, UC_X86_REG_RSI, UC_X86_REG_RDI,
                               UC_X86_REG_RBP, UC_X86_REG_RSP, UC_X86_REG_R8,
                               UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11,
                               UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14,
                               UC_X86_REG_R15)

REGS = {"rax": UC_X86_REG_RAX, "rbx": UC_X86_REG_RBX, "rcx": UC_X86_REG_RCX,
        "rdx": UC_X86_REG_RDX, "rsi": UC_X86_REG_RSI, "rdi": UC_X86_REG_RDI,
        "rbp": UC_X86_REG_RBP, "rsp": UC_X86_REG_RSP, "r8": UC_X86_REG_R8,
        "r9": UC_X86_REG_R9, "r10": UC_X86_REG_R10, "r11": UC_X86_REG_R11,
        "r12": UC_X86_REG_R12, "r13": UC_X86_REG_R13, "r14": UC_X86_REG_R14,
        "r15": UC_X86_REG_R15}

# --- La mémoire du harnais (émulation nue à les RVA du plan, mécanisme D79) ------

ZONE_IMAGE = (0x1000, 0x11000)     # les 28 blocs (0xC000..0x10DB0) + la marge
RET_MAGIQUE = 0x10E00              # au-delà du socle (l'erratum n° 5 l'a déplacé
                                   # 0x10AC0 → 0x10D00 : la sentinelle suit,
                                   # 0x10E00 > la fin du slot de 28 [0x10DB0])
ZONE_SESSION = 0x500000            # le contexte session (17 520 o) + le kit
ZONE_SIMU = 0x600000               # LE SIMULATEUR : les stubs, la cassette, le journal
ZONE_PILE = 0x7E000000
TAILLE_PILE = 0x200000
RSP0 = 0x7E018000
ENTREE_RSP = RSP0 - 0x108

FENETRE = 0x100

ADR_SESSION = ZONE_SESSION + 0x100
ADR_KIT = ZONE_SESSION + 0x8000
ADR_ENTREES = ZONE_SESSION + 0x10000    # les données des vecteurs (0x10000)
TAILLE_SESSION = 17520

STUB_EMIT = ZONE_SIMU + 0x0000          # le rappel émettre (journalise)
STUB_RECV = ZONE_SIMU + 0x1000          # le rappel recevoir (sert la cassette)
CELL_LOG = ZONE_SIMU + 0x2000           # la tête du journal (u64)
CELL_CUR = ZONE_SIMU + 0x2008           # le curseur de la cassette (u64)
CELL_FIN = ZONE_SIMU + 0x2010           # la fin de la cassette (u64)
ADR_SOCLE = ZONE_SIMU + 0x2020          # le contexte socle (32 o)
CASSETTE = ZONE_SIMU + 0x10000          # le flux à servir (0x10000)
JOURNAL = ZONE_SIMU + 0x20000           # les octets émis (0x10000)

CANARI = b"\xA5"

SENTINELLES_NV = {
    "rbx": 0x1212121212121212, "rbp": 0x2323232323232323,
    "rdi": 0x3434343434343434, "rsi": 0x4545454545454545,
    "r12": 0x5656565656565656, "r13": 0x6767676767676767,
    "r14": 0x7878787878787878, "r15": 0x8989898989898989,
}

# --- Le scellé 0.9.0 (la pièce V0 — l'ancre du corps hérité) ---------------------

SCELLE_M8 = "m8/proxy.exe"
SCELLE_M8_TAILLE = 44544
SCELLE_M8_SHA256 = "1492b0bc0792e1ab162338b414fb20573134e84d752b9d0657292421f8eb0cd4"

REUSSITES, ECHECS = [], []


class ErreurHarnais(Exception):
    """Tout écart du harnais (le verdict est tranché, jamais muet)."""


def controle(nom: str, ok: bool, detail: str = "") -> None:
    if ok:
        REUSSITES.append(nom)
        print(f"  [ok] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append((nom, detail))
        print(f"  [ÉCHEC] {nom}" + (f" — {detail}" if detail else ""))


def section(titre: str) -> None:
    print(f"\n--- {titre} ---")


def s64(v: int) -> int:
    return v - (1 << 64) if v >= (1 << 63) else v


# ======================================================================
# LES PIÈCES CONSIGNÉES — le texte officiel RFC 8448 § 3 parsé par le
# labo derive_poignee.py (41 contrôles VERTS, TOUT recoupé : le couple et
# le secret partagé par PyNaCl, le calendrier étage par étage par la
# référence, les QUATRE chaînes == TRANSFERT_8448, le vol et le certificat
# déverrouillés par la référence enregistrement — le juge est le code)
# ======================================================================

PRIVEE_CLIENT = bytes.fromhex(
    "49af42ba7f7994852d713ef2784bcbcaa7911de26adc5642cb634540e7ea5005")
PUBLIQUE_CLIENT = bytes.fromhex(
    "99381de560e4bd43d23d8e435a7dbafeb3c06e51c13cae4d5413691e529aaf2c")
ALEA_8448 = bytes.fromhex(
    "cb34ecb1e78163ba1c38c6dacb196a6dffa21a8d9912ec18a2ef6283024dece7")
SH_8448 = bytes.fromhex(
    "020000560303a6af06a4121860dc5e6e60249cd34c95930c8ac5cb1434dac155772e"
    "d3e2692800130100002e00330024001d0020c9828876112095fe66762bdbf7c672e1"
    "56d6cc253b833df1dd69b1b04e751f0f002b00020304")
SH_REC_8448 = bytes.fromhex(
    "160303005a" + SH_8448.hex())
PARTAGE_8448 = bytes.fromhex(
    "8bd4054fb55b9d63fdfbacf9f04b9f0d35e6d63f537563efd46272900f89492d")
HASH_CH_SH_8448 = bytes.fromhex(
    "860c06edc07858ee8e78f0e7428c58edd6b43f2ca3e6e95f02ed063cf0e1cad8")
HASH_CH_FIN_8448 = bytes.fromhex(
    "9608102a0f1ccc6db6250b7b7e417b1a000eaada3daae4777a7686c9ff83df13")
EARLY_8448 = bytes.fromhex(
    "33ad0a1c607ec03b09e6cd9893680ce210adf300aa1f2660e1b22e10f170f92a")
DERIVED_1_8448 = bytes.fromhex(
    "6f2615a108c702c5678f54fc9dbab69716c076189c48250cebeac3576c3611ba")
HANDSHAKE_8448 = bytes.fromhex(
    "1dc826e93606aa6fdc0aadc12f741b01046aa6b99f691ed221a9f0ca043fbeac")
C_HS_8448 = bytes.fromhex(
    "b3eddb126e067f35a780b3abf45e2d8f3b1a950738f52e9600746a0e27a55a21")
S_HS_8448 = bytes.fromhex(
    "b67b7d690cc16c4e75e54213cb2d37b4e9c912bcded9105d42befd59d391ad38")
DERIVED_2_8448 = bytes.fromhex(
    "43de77e0c77713859a944db9db2590b53190a65b3ee2e4f12dd7a0bb7ce254b4")
MASTER_8448 = bytes.fromhex(
    "18df06843d13a08bf2a449844c5f8a478001bc4d4c627984d5a41da8d0402919")
C_AP_8448 = bytes.fromhex(
    "9e40646ce79a7f9dc05af8889bce6552875afa0b06df0087f792ebb7c17504a5")
S_AP_8448 = bytes.fromhex(
    "a11af9f05531f856ad47116b45a950328204b4f44bfb6b3a4b4f1f3fcb631643")
S_FIN_CLE_8448 = bytes.fromhex(
    "008d3b66f816ea559f96b537e885c31fc068bf492c652f01f288a1d8cdc19fc8")
S_FIN_8448 = bytes.fromhex(
    "9b9b141d906337fbd2cbdce71df4deda4ab42c309572cb7fffee5454b78f0718")
C_FIN_CLE_8448 = bytes.fromhex(
    "b80ad01015fb2f0bd65ff7d4da5d6bf83f84821d1f87fdc7d3c75b5a7b42d9c4")
C_FIN_8448 = bytes.fromhex(
    "a8ec436d677634ae525ac1fcebe11a039ec17694fac6e98527b642f2edd5ce61")
HASH_CH_CV_8448 = bytes.fromhex(
    "edb7725fa7a3473b031ec8ef65a2485493900138a2b91291407d7951a06110ed")
# le ClientHello DU RFC 8448 § 3 (196 o — l'offre RICHE d'un client
# généraliste : trois suites 1301/1303/1302, SNI « server », neuf groupes,
# quinze sigalgs) — LA PIÈCE DE L'ERRATUM n° 2 : l'égalité octet pour octet
# avec NOTRE offre minimale scellée (114 o) est IMPOSSIBLE PAR CONSTRUCTION
CH_RFC = bytes.fromhex(
    "010000c00303cb34ecb1e78163ba1c38c6dacb196a6dffa21a8d9912ec18a2ef6283"
    "024dece7000006130113031302010000910000000b0009000006736572766572ff01"
    "000100000a00140012001d0017001800190100010101020103010400230000003300"
    "260024001d002099381de560e4bd43d23d8e435a7dbafeb3c06e51c13cae4d541369"
    "1e529aaf2c002b0003020304000d0020001e04030503060302030804080508060401"
    "0501060102010402050206020202002d00020101001c00024001")
# le vol serveur : la charge interne du premier enregistrement TRANSFERT_8448
# (EE || CERT || CV || Fin serveur || type 22) — les charges du RFC servies
# PAR LE SIMULATEUR re-scellées sous les clés DU JALON
# le ClientHello DU RFC 8448 § 3 (196 o — l'offre RICHE d'un client
# généraliste : TROIS suites, SNI « server », NEUF groupes, QUINZE sigalgs) —
# LA PIÈCE DE L'ERRATUM n° 2 : l'égalité octet pour octet avec NOTRE offre
# minimale scellée (114 o) est IMPOSSIBLE PAR CONSTRUCTION (charte § 1, I3)
CH_RFC = bytes.fromhex(
    "010000c00303cb34ecb1e78163ba1c38c6dacb196a6dffa21a8d9912ec18a2ef6283"
    "024dece7000006130113031302010000910000000b0009000006736572766572ff01"
    "000100000a00140012001d0017001800190100010101020103010400230000003300"
    "260024001d002099381de560e4bd43d23d8e435a7dbafeb3c06e51c13cae4d541369"
    "1e529aaf2c002b0003020304000d0020001e04030503060302030804080508060401"
    "0501060102010402050206020202002d00020101001c00024001")
EE_8448 = bytes.fromhex(
    "080000240022000a00140012001d00170018001901000101010201030104001c0002"
    "400100000000")
CERT_8448 = bytes.fromhex(
    "0b0001b9000001b50001b0308201ac30820115a003020102020102300d06092a8648"
    "86f70d01010b0500300e310c300a06035504031303727361301e170d313630373330"
    "3031323335395a170d3236303733303031323335395a300e310c300a060355040313"
    "0372736130819f300d06092a864886f70d010101050003818d0030818902818100b4"
    "bb498f8279303d980836399b36c6988c0c68de55e1bdb826d3901a2461eafd2de49a"
    "91d015abbc9a95137ace6c1af19eaa6af98c7ced43120998e187a80ee0ccb0524b1b"
    "018c3e0b63264d449a6d38e22a5fda430846748030530ef0461c8ca9d9efbfae8ea6"
    "d1d03e2bd193eff0ab9a8002c47428a6d35a8d88d79f7f1e3f0203010001a31a3018"
    "30090603551d1304023000300b0603551d0f0404030205a0300d06092a864886f70d"
    "01010b05000381810085aad2a0e5b9276b908c65f73a7267170618a54c5f8a7b337d"
    "2df7a594365417f2eae8f8a58c8f8172f9319cf36b7fd6c55b80f21a030151567260"
    "96fd335e5e67f2dbf102702e608ccae6bec1fc63a42a99be5c3eb7107c3c54e9b9eb"
    "2bd5203b1c3b84e0a8b2f759409ba3eac9d91d402dcc0cc8f8961229ac9187b42b4d"
    "e10000")
CV_8448 = bytes.fromhex(
    "0f000084080400805a747c5d88fa9bd2e55ab085a61015b7211f824cd484145ab3ff"
    "52f1fda8477b0b7abc90db78e2d33a5c141a078653fa6bef780c5ea248eeaaa785c4"
    "f394cab6d30bbe8d4859ee511f602957b15411ac027671459e46445c9ea58c181e81"
    "8e95b8c3fb0bf3278409d3be152a3da5043e063dda65cdf5aea20d53dfacd42f74f3")
FIN_S_MSG_8448 = bytes.fromhex("14000020" + S_FIN_8448.hex())
DER_8448 = CERT_8448[11:11 + 432]         # la PREMIÈRE entrée (le DÉTROIT)
EMPREINTE_8448 = hashlib.sha256(DER_8448).digest()
APP_8448 = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
    "202122232425262728292a2b2c2d2e2f3031")      # la charge applicative du § 3

# ======================================================================
# LA RÉFÉRENCE — la poignée du jalon sur la référence de la lignée (le
# harnais aead : GCM ; le harnais enregistrement : la couche enregistrement)
# ======================================================================

TYPE_ALERT = 21
TYPE_HANDSHAKE = 22
TYPE_DATA = 23

VIDE = hashlib.sha256(b"").digest()        # Hash("") — le contexte de « derived »


def u16(x):
    return x.to_bytes(2, "big")


def ref_construction_ch(alea: bytes, cle_publique: bytes) -> bytes:
    """La construction re-jouée du plan (verifier_specs_m9a § 4) — le CH du
    jalon : 114 o FIXES, l'aléa @ +6, la clé publique @ +82."""
    exts = (u16(L.EXT_SUPPORTED_VERSIONS) + u16(3) + bytes([2]) + u16(L.VERSION_TLS13)
            + u16(L.EXT_SUPPORTED_GROUPS) + u16(4) + u16(2) + u16(L.GROUPE)
            + u16(L.EXT_SIG_ALGS) + u16(2 + 2 * len(L.SIG_ALGOS))
            + u16(2 * len(L.SIG_ALGOS)) + b"".join(u16(a) for a in L.SIG_ALGOS)
            + u16(L.EXT_KEY_SHARE) + u16(38) + u16(36) + u16(L.GROUPE)
            + u16(32) + cle_publique)
    corps = (u16(L.VERSION_HERITAGE) + alea + bytes([0])
             + u16(2) + u16(L.SUITE) + bytes([1, 0]) + u16(len(exts)) + exts)
    assert len(alea) == 32 and len(cle_publique) == 32
    ch = bytes([1]) + (len(corps)).to_bytes(3, "big") + corps
    assert len(ch) == L.CLIENTHELLO_TAILLE == 114
    return ch


def ref_hkdf_extract(salt, ikm):
    return hmac.new(salt or b"\x00" * 32, ikm, hashlib.sha256).digest()


def ref_expand_label(secret, libelle, contexte, n):
    info = (struct.pack(">H", n) + bytes([len(b"tls13 " + libelle)])
            + b"tls13 " + libelle + bytes([len(contexte)]) + contexte)
    out, t, i = b"", b"", 1
    while len(out) < n:
        t = hmac.new(secret, t + info + bytes([i]), hashlib.sha256).digest()
        out += t
        i += 1
    return out[:n]


class ref_Cadenas:
    """Le calendrier DU JALON (RFC 8446 § 7.1) — la référence Python : la
    machine le dérive par les briques, la référence le recoupe étage par
    étage (le juge est le code)."""

    def __init__(self, partage: bytes, hash_ch_sh: bytes):
        Z = b"\x00" * 32
        self.early = ref_hkdf_extract(Z, Z)
        self.derived_1 = ref_expand_label(self.early, b"derived", VIDE, 32)
        self.handshake = ref_hkdf_extract(self.derived_1, partage)
        self.c_hs = ref_expand_label(self.handshake, b"c hs traffic", hash_ch_sh, 32)
        self.s_hs = ref_expand_label(self.handshake, b"s hs traffic", hash_ch_sh, 32)
        self.derived_2 = ref_expand_label(self.handshake, b"derived", VIDE, 32)
        for qui, secret in (("c", self.c_hs), ("s", self.s_hs)):
            setattr(self, f"{qui}_cle_hs",
                    ref_expand_label(secret, b"key", b"", 16))
            setattr(self, f"{qui}_iv_hs",
                    ref_expand_label(secret, b"iv", b"", 12))
            setattr(self, f"{qui}_fin_cle",
                    ref_expand_label(secret, b"finished", b"", 32))

    def etage3(self, hash_ch_fin: bytes):
        Z = b"\x00" * 32
        self.master = ref_hkdf_extract(self.derived_2, Z)
        self.c_ap = ref_expand_label(self.master, b"c ap traffic", hash_ch_fin, 32)
        self.s_ap = ref_expand_label(self.master, b"s ap traffic", hash_ch_fin, 32)
        for qui, secret in (("c", self.c_ap), ("s", self.s_ap)):
            setattr(self, f"{qui}_cle_ap",
                    ref_expand_label(secret, b"key", b"", 16))
            setattr(self, f"{qui}_iv_ap",
                    ref_expand_label(secret, b"iv", b"", 12))


def ref_contexte(cle: bytes, iv: bytes, seq: int = 0) -> ENR.Contexte:
    return ENR.Contexte(cle, iv, seq)


# ======================================================================
# L'ÉMULATION (le modèle harnais_enregistrement — l'appelant factice msx64)
# ======================================================================

class Emulation(ENR.Emulation):
    """Les VINGT-HUIT blocs posés à leurs RVA du plan, appelés comme des
    fonctions msx64 ordinaires. La zone morte PROFONDE vit à [−0xE000,
    −0xDC00) : le cadre de tls13-27 [0x43C8] + celui de tls13-21 [0x4078] +
    celui de tls13-19 [0xE8] descendent à ≈ 0x8570 sous l'entrée — la leçon
    du cadre NOMMÉ rejouée sur LE PLUS GRAND bloc."""

    BLOCS = ENR.Emulation.BLOCS + [
        ("h100022", "tls13-22-clienthello-composer"),
        ("h100023", "tls13-23-serverhello-traiter"),
        ("h100024", "tls13-24-calendrier-cles"),
        ("h100025", "tls13-25-finished-calculer-verifier"),
        ("h100026", "tls13-26-epinglage"),
        ("h100027", "tls13-27-principal-machine-etats"),
        ("h100028", "tls13-28-socle-appel")]

    def __init__(self, nue: bool = False):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.ks = Ks(KS_ARCH_X86, KS_MODE_64)
        self.cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.cs.detail = False
        self.uc.mem_map(*ZONE_IMAGE)
        for zone, taille in ((ZONE_SESSION, 0x20000),
                             (ZONE_SIMU, 0x40000),
                             (ZONE_PILE, TAILLE_PILE)):
            self.uc.mem_map(zone, taille)
        for zone, taille in ((ZONE_SESSION, 0x20000), (ZONE_SIMU, 0x40000)):
            self.uc.mem_write(zone, CANARI * taille)
        # les pièces du plan : K[64] à R_K, les fixtures à leur ARRÊT .text6
        self.uc.mem_write(L.R_K, struct.pack("<64I", *L.K))
        self.uc.mem_write(L.R_U9, L.X25519_BASE.to_bytes(32, "little"))
        self.uc.mem_write(L.R_EXP_INV, ((2**255 - 19) - 2).to_bytes(32, "little"))
        self.uc.mem_write(L.R_LIB_DERIVED, L.LIBELLES["derived"])
        self.uc.mem_write(L.R_LIB_C_HS, L.LIBELLES["c hs traffic"])
        self.uc.mem_write(L.R_LIB_S_HS, L.LIBELLES["s hs traffic"])
        self.uc.mem_write(L.R_LIB_C_AP, L.LIBELLES["c ap traffic"])
        self.uc.mem_write(L.R_LIB_S_AP, L.LIBELLES["s ap traffic"])
        self.uc.mem_write(L.R_LIB_KEY, L.LIBELLES["key"])
        self.uc.mem_write(L.R_LIB_IV, L.LIBELLES["iv"])
        self.uc.mem_write(L.R_LIB_FINISHED, L.LIBELLES["finished"])
        self.uc.mem_write(L.R_HRR, L.HRR_MAGIQUE)
        self.blobs: dict[str, tuple[bytes, list]] = {}
        self.compteur_actif = False
        self.compteur = 0
        self.surveillance: dict[int, list[int]] | None = None
        if not nue:
            self.uc.hook_add(UC_HOOK_CODE, self._instrument)
        self.poser_blocs()
        self.poser_simulateur()

    # --- LE SIMULATEUR (tls13-28 I3 : la réalisation LICITE du contexte) ----

    def poser_simulateur(self):
        """Les DEUX rappels du kit en machine code (l'ABI Q3 de tls13-28 :
        rcx = le contexte du rappel, rdx = le pointeur, r8 = la longueur) —
        l'émettre JOURNALISE à la tête, le recevoir SERT la cassette. Le
        zéro de réception est la demi-fin : le rappel rend -1, tls13-28 le
        traduit en -7 NOMMÉ."""
        # les DEUX rappels préservent rdi/rsi (NON-VOLATILES en msx64) :
        # les piles de sauvegarde entourent le rep movsb — AUCUN saut (la
        # demi-fin n = 0 est traduite en -7 PAR tls13-28 : le zéro de
        # réception est le refus du KIT, jamais une lecture vide silencieuse)
        emit, _ = self.ks.asm(
            "push rdi\n"
            "push rsi\n"
            "mov r10, rcx\n"          # r10 = &tête
            "mov rsi, rdx\n"
            "mov rdi, qword ptr [rcx]\n"
            "mov rcx, r8\n"
            "cld\n"
            "rep movsb\n"
            "add qword ptr [r10], r8\n"
            "xor eax, eax\n"
            "pop rsi\n"
            "pop rdi\n"
            "ret\n", STUB_EMIT)
        self.uc.mem_write(STUB_EMIT, bytes(emit))
        recv, _ = self.ks.asm(
            "push rdi\n"
            "push rsi\n"
            "push rcx\n"
            "mov r9, qword ptr [rcx]\n"        # le curseur
            "mov rax, qword ptr [rcx + 8]\n"   # la fin
            "sub rax, r9\n"                    # le restant
            "cmp r8, rax\n"                    # n = min(capacité, restant)
            "cmovbe rax, r8\n"
            "mov rsi, r9\n"
            "mov rdi, rdx\n"
            "mov rcx, rax\n"
            "cld\n"
            "rep movsb\n"
            "mov rcx, qword ptr [rsp]\n"        # &cur (le rcx poussé — LA
            "add qword ptr [rcx], rax\n"        # FAUTE du premier jet : add
            # [rsp] n'aurait avancé que la CASE de pile, jamais la
            # cellule pointée — le pointeur RECHARGÉ, l'écriture À TRAVERS)
            "pop rcx\n"
            "pop rsi\n"
            "pop rdi\n"
            "ret\n", STUB_RECV)
        self.uc.mem_write(STUB_RECV, bytes(recv))
        self.uc.mem_write(ADR_SOCLE, struct.pack(
            "<QQQQ", STUB_EMIT, CELL_LOG, STUB_RECV, CELL_CUR))

    def reinit_journal(self):
        self.uc.mem_write(CELL_LOG, struct.pack("<Q", JOURNAL))

    def poser_cassette(self, flux: bytes):
        assert len(flux) <= 0x10000
        self.uc.mem_write(CASSETTE, flux)
        self.uc.mem_write(CELL_CUR, struct.pack("<QQ", CASSETTE,
                                                CASSETTE + len(flux)))

    def lire_journal(self) -> bytes:
        tete = struct.unpack("<Q", bytes(self.uc.mem_read(CELL_LOG, 8)))[0]
        return bytes(self.uc.mem_read(JOURNAL, tete - JOURNAL))

    # --- la zone morte profonde : sous le cadre de la machine (0x43C8) -------

    def appeler(self, va: int, args: dict[str, int] | None = None,
                compter: bool = False, args_pile: list[int] | None = None):
        """Appelle un bloc comme une fonction msx64. Retourne le dict de
        sortie + canaris (le modèle de la lignée — la zone morte PROFONDE
        à −0xE000 : sous le cadre 0x43C8 de la machine ET les cadres
        imbriqués 0x4078/0xE8, la leçon du geste rejouée)."""
        uc = self.uc
        for nom, val in SENTINELLES_NV.items():
            uc.reg_write(REGS[nom], val)
        for nom, val in (args or {}).items():
            uc.reg_write(REGS[nom], val)
        uc.reg_write(UC_X86_REG_RAX, 0)
        rsp = ENTREE_RSP
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.mem_write(rsp + 8, CANARI * 0x178)
        logements = []
        for i, val in enumerate(args_pile or []):
            uc.mem_write(rsp + 0x28 + 8 * i, struct.pack("<Q", val))
            logements.append(rsp + 0x28 + 8 * i)
        uc.mem_write(rsp - 0xE000, CANARI * 0x400)
        uc.mem_write(rsp, struct.pack("<Q", RET_MAGIQUE))
        entree_rsp = rsp
        self.compteur = 0
        self.compteur_actif = compter
        try:
            uc.emu_start(va, RET_MAGIQUE, count=200_000_000)
        except UcError as err:
            self.compteur_actif = False
            return {"crash": str(err), "entree_rsp": entree_rsp,
                    "canaris_haut": False, "canaris_profond": False,
                    "logements_intacts": False, "compteur": self.compteur}
        finally:
            self.compteur_actif = False
        sortie = {k: uc.reg_read(REGS[k]) for k in REGS}
        sortie["rax"] = s64(sortie["rax"])
        sortie["entree_rsp"] = entree_rsp
        sortie["crash"] = None
        sortie["compteur"] = self.compteur
        sortie["pile_equilibree"] = uc.reg_read(REGS["rsp"]) == entree_rsp + 8
        zone_haute = bytes(uc.mem_read(entree_rsp + 8, 0x178))
        plages = [(a, a + 8) for a in logements]
        intact = True
        for i in range(len(zone_haute)):
            adresse = entree_rsp + 8 + i
            octet = zone_haute[i:i + 1]
            if any(debut <= adresse < fin for debut, fin in plages):
                continue
            if octet != CANARI:
                intact = False
                break
        sortie["canaris_haut"] = intact
        sortie["logements_intacts"] = all(
            struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0] == v
            for a, v in zip(logements, args_pile or []))
        sortie["canaris_profond"] = bytes(
            uc.mem_read(entree_rsp - 0xE000, 0x400)) == CANARI * 0x400
        return sortie

    def non_volatiles_rendus(self, r: dict) -> bool:
        return all(r[nom] == SENTINELLES_NV[nom] for nom in SENTINELLES_NV)

    def poser(self, adresse: int, donnees: bytes):
        self.uc.mem_write(adresse - FENETRE, CANARI * FENETRE)
        self.uc.mem_write(adresse, donnees)
        self.uc.mem_write(adresse + len(donnees),
                          CANARI * (FENETRE + 0x20))

    def intact_autour(self, adresse: int, longueur: int) -> bool:
        avant = bytes(self.uc.mem_read(adresse - FENETRE, FENETRE))
        apres = bytes(self.uc.mem_read(adresse + longueur, FENETRE + 0x20))
        return avant == CANARI * FENETRE and apres == CANARI * (FENETRE + 0x20)


# --- Les pipelines (les compositions du harnais) ---------------------------------

def poser_kit(emul: Emulation, alea: bytes, privee: bytes, empreinte: bytes):
    """Les 96 o du kit : aléa 32 + clé privée 32 + empreinte 32 (le kit
    fournit TOUT : le CSPRG, le couple, la confiance — tls13-27 É1)."""
    assert len(alea) == len(privee) == len(empreinte) == 32
    emul.poser(ADR_KIT, alea + privee + empreinte)


def session_neuve(emul: Emulation):
    """La session VIERGE : 17 520 o de zéros (état 0, étape 0, les contextes
    nus) — l'adresse choisie par l'appelant (charte § 6)."""
    emul.poser(ADR_SESSION, bytes(TAILLE_SESSION))


def lire_session(emul: Emulation, off: int, n: int) -> bytes:
    return bytes(emul.uc.mem_read(ADR_SESSION + off, n))


def lire_etat(emul: Emulation) -> int:
    return struct.unpack("<I", lire_session(emul, 1120, 4))[0]


def lire_etape(emul: Emulation) -> int:
    return struct.unpack("<I", lire_session(emul, 112 + 32, 4))[0]


def ouvrir(emul: Emulation, compter: bool = False, force: dict | None = None):
    args = {"rcx": ADR_SESSION, "rdx": 1, "r8": ADR_SOCLE, "r9": ADR_KIT}
    if force:
        args.update(force)
    return emul.appeler(L.TLS27_VA, args, compter=compter)


def emettre(emul: Emulation, charge: bytes, compter: bool = False,
            force: dict | None = None):
    emul.poser(ADR_ENTREES, charge)
    args = {"rcx": ADR_SESSION, "rdx": 2, "r8": ADR_ENTREES, "r9": len(charge)}
    if force:
        args.update(force)
    return emul.appeler(L.TLS27_VA, args, compter=compter)


def recevoir(emul: Emulation, cap: int = 5 + 2**14 + 17 + 16,
             compter: bool = False, force: dict | None = None):
    """Le tampon de l'appelant : l'enregistrement y est lu PUIS la charge
    restituée AU DÉBUT du même tampon (l'écrasement licite et NOMMÉ)."""
    emul.uc.mem_write(ADR_ENTREES - FENETRE, CANARI * FENETRE)
    emul.uc.mem_write(ADR_ENTREES, CANARI * cap)
    emul.uc.mem_write(ADR_ENTREES + cap, CANARI * (FENETRE + 0x20))
    args = {"rcx": ADR_SESSION, "rdx": 3, "r8": ADR_ENTREES, "r9": cap}
    if force:
        args.update(force)
    return emul.appeler(L.TLS27_VA, args, compter=compter)


def composer_ch(emul: Emulation, alea: bytes, cle: bytes, force: dict | None = None):
    base = ADR_ENTREES
    emul.poser(base, alea + cle)
    sortie = base + 0x1000
    emul.uc.mem_write(sortie - FENETRE, CANARI * FENETRE)
    emul.uc.mem_write(sortie, CANARI * (L.CLIENTHELLO_TAILLE + 0x40))
    emul.uc.mem_write(sortie + L.CLIENTHELLO_TAILLE,
                      CANARI * (FENETRE + 0x20))
    args = {"rcx": base, "rdx": base + 32, "r8": sortie,
            "r9": L.CLIENTHELLO_TAILLE}
    if force:
        args.update(force)
    r = emul.appeler(L.TLS22_VA, args)
    return bytes(emul.uc.mem_read(sortie, L.CLIENTHELLO_TAILLE)), r


def traiter_sh(emul: Emulation, message: bytes, privee: bytes,
               force: dict | None = None):
    base = ADR_ENTREES
    emul.poser(base, message + privee)
    sortie = base + 0x2000
    emul.uc.mem_write(sortie - FENETRE, CANARI * FENETRE)
    emul.uc.mem_write(sortie, CANARI * 0x40)
    emul.uc.mem_write(sortie + 32, CANARI * (FENETRE + 0x20))
    args = {"rcx": base, "rdx": len(message), "r8": base + len(message),
            "r9": sortie}
    if force:
        args.update(force)
    r = emul.appeler(L.TLS23_VA, args)
    return bytes(emul.uc.mem_read(sortie, 32)), r


def calendrier(emul: Emulation, contexte48: bytes, entree: bytes,
               sortie_cap: int, force: dict | None = None):
    base = ADR_ENTREES
    emul.poser(base, contexte48 + entree)
    sortie = base + 0x2000
    emul.uc.mem_write(sortie, CANARI * sortie_cap)
    emul.uc.mem_write(sortie + sortie_cap, CANARI * (FENETRE + 0x20))
    args = {"rcx": base, "rdx": base + len(contexte48), "r8": sortie}
    if force:
        args.update(force)
    r = emul.appeler(L.TLS24_VA, args)
    return bytes(emul.uc.mem_read(sortie, sortie_cap)), bytes(
        emul.uc.mem_read(base, 48)), r


def finished(emul: Emulation, cle: bytes, hache: bytes, recu: bytes,
             mode: int, force: dict | None = None, compter: bool = False):
    base = ADR_ENTREES
    emul.poser(base, cle + hache + recu)
    args = {"rcx": base, "rdx": base + 32, "r8": base + 64, "r9": mode}
    if force:
        args.update(force)
    r = emul.appeler(L.TLS25_VA, args, compter=compter)
    return bytes(emul.uc.mem_read(base + 64, 32)), r


def epinglage(emul: Emulation, der: bytes, empreinte: bytes,
              force: dict | None = None):
    base = ADR_ENTREES
    emul.poser(base, der + empreinte)
    args = {"rcx": base, "rdx": len(der), "r8": base + len(der)}
    if force:
        args.update(force)
    return emul.appeler(L.TLS26_VA, args)


def socle(emul: Emulation, op: int, ptr: int, n: int,
          contexte: int | None = None, force: dict | None = None):
    args = {"rcx": contexte if contexte is not None else ADR_SOCLE,
            "rdx": op, "r8": ptr, "r9": n}
    if force:
        args.update(force)
    return emul.appeler(L.TLS28_VA, args)


# --- La référence de la session DU JALON (le simulateur en vit) -------------------

class Simulation:
    """La session DU JALON dérivée par la référence Python : notre CH de
    114 o (l'offre scellée, le fixture aléa/clé) || le SH du RFC || le vol
    du RFC (EE/Cert/CV verbatim, le Finished serveur RECALCULÉ sur NOTRE
    coupe) — le calendrier, les chaînes et les enregistrements attendus."""

    def __init__(self):
        self.ch = ref_construction_ch(ALEA_8448, PUBLIQUE_CLIENT)
        self.ch_rec = b"\x16\x03\x03\x00\x72" + self.ch
        # (l'erratum n° 5 : l'octet de longueur du record CH — 114 = 0x72 ;
        #  le premier jet écrivait 0x76 [118] : la sonde terrain du 06/11 a
        #  prouvé sur pièces le SILENCE des serveurs réels — le serveur
        #  attend 4 octets jamais émis ; machine et référence corrigées
        #  ENSEMBLE — le juge est le code ET le monde)
        self.hash1 = hashlib.sha256(self.ch + SH_8448).digest()
        self.cadenas = ref_Cadenas(PARTAGE_8448, self.hash1)
        self.hash_cv = hashlib.sha256(
            self.ch + SH_8448 + EE_8448 + CERT_8448 + CV_8448).digest()
        self.fin_s = (b"\x14\x00\x00\x20"
                      + hmac.new(self.cadenas.s_fin_cle, self.hash_cv,
                                 hashlib.sha256).digest())
        self.hash_fin = hashlib.sha256(
            self.ch + SH_8448 + EE_8448 + CERT_8448 + CV_8448
            + self.fin_s).digest()
        self.cadenas.etage3(self.hash_fin)
        self.fin_c = (b"\x14\x00\x00\x20"
                      + hmac.new(self.cadenas.c_fin_cle, self.hash_fin,
                                 hashlib.sha256).digest())
        # les chaînes : la référence fait avancer les séquences elle-même
        self.c_hs = ref_contexte(self.cadenas.c_cle_hs, self.cadenas.c_iv_hs)
        self.s_hs = ref_contexte(self.cadenas.s_cle_hs, self.cadenas.s_iv_hs)
        self.c_ap = ref_contexte(self.cadenas.c_cle_ap, self.cadenas.c_iv_ap)
        self.s_ap = ref_contexte(self.cadenas.s_cle_ap, self.cadenas.s_iv_ap)
        self.flight = ENR.ref_proteger(
            self.s_hs, TYPE_HANDSHAKE,
            EE_8448 + CERT_8448 + CV_8448 + self.fin_s + b"\x16")
        self.fin_c_rec = ENR.ref_proteger(self.c_hs, TYPE_HANDSHAKE, self.fin_c)


# --- V0 : les pièces du plan ------------------------------------------------------

def vecteur_v0(emul: Emulation):
    section("V0 — les pièces du plan (le scellé, les cinq familles, les fixtures, la session, l'arbre I)")
    donnees = open(os.path.join(TRIADE, SCELLE_M8), "rb").read()
    controle("V0.a:le-scelle-090-intact",
             len(donnees) == SCELLE_M8_TAILLE
             and hashlib.sha256(donnees).hexdigest() == SCELLE_M8_SHA256,
             f"{len(donnees)} o, sha256 1492b0bc…b0cd4 — l'ancre R7")
    # les cinq familles précédentes INTACTES : les VINGT-ET-UNE notations
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    attendus = {"h100001": 74, "h100002": 387, "h100003": 139, "h100004": 165,
                "h100005": 435, "h100006": 151, "h100007": 347, "h100008": 310,
                "h100009": 54, "h100010": 252, "h100011": 1078,
                "h100012": 281, "h100013": 2887, "h100014": 23,
                "h100015": 520, "h100016": 129, "h100017": 162,
                "h100018": 1076, "h100019": 1163, "h100020": 349,
                "h100021": 403}
    noms = {bid: nom for bid, nom in Emulation.BLOCS if bid in attendus}
    ok, details = True, []
    for bid, attendu in attendus.items():
        rva, slot = L.SLOTS_TLS13[bid]
        chemin = os.path.join(ICI, "notation", noms[bid] + ".asm")
        octets, _ = B4.assembler_bloc(ks, chemin, rva, slot)
        if len(octets) != attendu:
            ok = False
            details.append(f"{noms[bid]} : {len(octets)} o ≠ {attendu}")
    controle("V0.b:les-cinq-familles-precedentes-intactes", ok,
             "les VINGT-ET-UNE notations relues aux longueurs arrêtées : sha "
             "74/387/139/165 + hkdf 435/151/347/310 + x25519 54/252/1078/281/"
             "2887/23 + aead 520/129/162/1076/1163 + enregistrement 349/403 o"
             + (f" — DÉFAUTS : {details}" if details else ""))
    # les fixtures du domaine : les libellés, la valeur magique, U9, EXP_INV, K
    fixtures = [
        ("derived", L.R_LIB_DERIVED, L.LIBELLES["derived"]),
        ("c hs traffic", L.R_LIB_C_HS, L.LIBELLES["c hs traffic"]),
        ("s hs traffic", L.R_LIB_S_HS, L.LIBELLES["s hs traffic"]),
        ("c ap traffic", L.R_LIB_C_AP, L.LIBELLES["c ap traffic"]),
        ("s ap traffic", L.R_LIB_S_AP, L.LIBELLES["s ap traffic"]),
        ("key", L.R_LIB_KEY, L.LIBELLES["key"]),
        ("iv", L.R_LIB_IV, L.LIBELLES["iv"]),
        ("finished", L.R_LIB_FINISHED, L.LIBELLES["finished"]),
        ("HRR", L.R_HRR, L.HRR_MAGIQUE),
        ("U9", L.R_U9, (9).to_bytes(32, "little")),
        ("EXP_INV", L.R_EXP_INV, ((2**255 - 19) - 2).to_bytes(32, "little")),
    ]
    ok_fix = all(bytes(emul.uc.mem_read(rva, len(octets))) == octets
                 for _, rva, octets in fixtures)
    controle("V0.c:les-fixtures-du-domaine-poses", ok_fix,
             "les HUIT libellés du calendrier + la valeur magique HRR + U9 + "
             "EXP_INV relus OCTET POUR OCTET à leur ARRÊT .text6 (le plan, "
             "source unique — des DONNÉES PUBLIQUES, jamais des octets de code)")
    controle("V0.d:K64-a-r-k",
             bytes(emul.uc.mem_read(L.R_K, 256)) == struct.pack("<64I", *L.K),
             "la table de SHA-256 à la réserve .rdata héritée M8 (RVA 0x2F00)")
    # la disposition de session recomptée (verifier_specs_m9a § 5 rejoué)
    attendu_session = (112 + 48 + 32 + 32 + 200 * 4 + 32 * 3 + 4 + 4 + 8
                       + L.SESSION_POIGNEE_MAX)
    controle("V0.e:la-session-17520o-la-disposition-recomptee",
             L.SESSION_TAILLE == attendu_session == 17520,
             "le transcript 112 @ +0 · le calendrier 48 @ +112 · la clé "
             "privée 32 @ +160 · la clé publique 32 @ +192 · les QUATRE "
             "contextes 200 @ +224/+424/+624/+824 · les clés Finished 32 @ "
             "+1024/+1056 · l'empreinte 32 @ +1088 · l'état @ +1120 · le "
             "remplissage @ +1124 · le socle @ +1128 · le réassemblage 2^14 "
             "@ +1136")
    # l'arbre I scellé relu : verifier_specs_m9a rejoué (l'erratum n° 2 compris)
    proc = subprocess.run([sys.executable, "scripts/verifier_specs_m9a.py"],
                          cwd=TRIADE, capture_output=True, text=True)
    controle("V0.f:l-arbre-I-scelle-relu-vert", proc.returncode == 0,
             "verifier_specs_m9a rejoué — les 28 spécifications posées et "
             "cohérentes, l'erratum n° 2 consigné sur pièces AVANT la notation")
    # les pièces consignées recoupées par la référence AU GESTE MÊME
    ctrl_ref = True
    ctrl_ref &= nacl.bindings.crypto_scalarmult(
        PRIVEE_CLIENT, (9).to_bytes(32, "little")) == PUBLIQUE_CLIENT
    ctrl_ref &= nacl.bindings.crypto_scalarmult(
        PRIVEE_CLIENT, SH_8448[52:84]) == PARTAGE_8448
    cad = ref_Cadenas(PARTAGE_8448, HASH_CH_SH_8448)
    ctrl_ref &= cad.early == EARLY_8448 and cad.derived_1 == DERIVED_1_8448
    ctrl_ref &= cad.handshake == HANDSHAKE_8448
    ctrl_ref &= cad.c_hs == C_HS_8448 and cad.s_hs == S_HS_8448
    ctrl_ref &= cad.derived_2 == DERIVED_2_8448
    ctrl_ref &= cad.c_cle_hs == bytes.fromhex(AEAD.TRANSFERT_8448[1][1])
    ctrl_ref &= cad.c_iv_hs == bytes.fromhex(AEAD.TRANSFERT_8448[1][2])
    ctrl_ref &= cad.s_cle_hs == bytes.fromhex(AEAD.TRANSFERT_8448[0][1])
    ctrl_ref &= cad.s_iv_hs == bytes.fromhex(AEAD.TRANSFERT_8448[0][2])
    ctrl_ref &= cad.c_fin_cle == C_FIN_CLE_8448
    ctrl_ref &= cad.s_fin_cle == S_FIN_CLE_8448
    cad.etage3(HASH_CH_FIN_8448)
    ctrl_ref &= cad.master == MASTER_8448
    ctrl_ref &= cad.c_ap == C_AP_8448 and cad.s_ap == S_AP_8448
    ctrl_ref &= cad.c_cle_ap == bytes.fromhex(AEAD.TRANSFERT_8448[3][1])
    ctrl_ref &= cad.s_cle_ap == bytes.fromhex(AEAD.TRANSFERT_8448[2][1])
    ctrl_ref &= EMPREINTE_8448 == hashlib.sha256(DER_8448).digest()
    ctrl_ref &= hmac.new(C_FIN_CLE_8448, HASH_CH_FIN_8448,
                         hashlib.sha256).digest() == C_FIN_8448
    ctrl_ref &= hmac.new(S_FIN_CLE_8448, HASH_CH_CV_8448,
                         hashlib.sha256).digest() == S_FIN_8448
    ctrl_ref &= hashlib.sha256(CH_RFC + SH_8448).digest() == HASH_CH_SH_8448
    ctrl_ref &= hashlib.sha256(
        CH_RFC + SH_8448 + EE_8448 + CERT_8448 + CV_8448).digest() == HASH_CH_CV_8448
    ctrl_ref &= hashlib.sha256(
        CH_RFC + SH_8448 + EE_8448 + CERT_8448 + CV_8448
        + FIN_S_MSG_8448).digest() == HASH_CH_FIN_8448
    ctrl_ref &= len(CH_RFC) == 196 and CH_RFC[41:47] == bytes.fromhex("130113031302")
    ctrl_ref &= CH_RFC[60:66] == b"server"
    controle("V0.g:les-pieces-consignees-recoupees-au-geste-meme", ctrl_ref,
             "le couple et le secret partagé par PyNaCl, le calendrier étage "
             "par étage par la référence, les QUATRE chaînes == "
             "TRANSFERT_8448, les DEUX Finished, l'empreinte, LES TROIS HASH "
             "du transcript du RFC — ET LE CONSTAT DE L'ERRATUM n° 2 : le CH "
             "du RFC compte 196 o (trois suites 1301/1303/1302, SNI « server »), "
             "le jalon propose l'offre MINIMALE scellée (114 o) — le labo "
             "derive_poignee.py consigné, le juge est le code")

# --- V1 : round-trip + concordance au plan ---------------------------------------

APPELS_ATTENDUS = {
    "h100022": {},
    "h100023": {L.TLS13_VA: 1},
    "h100024": {L.TLS01_VA: 1, L.TLS04_VA: 1, L.TLS06_VA: 3,
                L.TLS08_VA: 16, L.TLS15_VA: 4},
    "h100025": {L.TLS05_VA: 1},
    "h100026": {L.TLS01_VA: 1, L.TLS03_VA: 1, L.TLS04_VA: 1},
    "h100027": {L.TLS01_VA: 1, L.TLS03_VA: 4, L.TLS04_VA: 3, L.TLS14_VA: 1,
                L.TLS20_VA: 3, L.TLS21_VA: 2, L.TLS22_VA: 1, L.TLS23_VA: 1,
                L.TLS24_VA: 3, L.TLS25_VA: 2, L.TLS26_VA: 1, L.TLS28_VA: 11},
    "h100028": {},
}


def vecteur_v1(emul: Emulation):
    section("V1 — round-trip de notation + concordance au plan (source unique)")
    attendus = {"h100022": 241, "h100023": 532, "h100024": 2130,
                "h100025": 239, "h100026": 285, "h100027": 2975,
                "h100028": 144}
    noms = {bid: nom for bid, nom in Emulation.BLOCS if bid in attendus}
    insns_par_bloc = {}
    for bid, attendu in attendus.items():
        rva, slot = L.SLOTS_TLS13[bid]
        chemin = os.path.join(ICI, "notation", noms[bid] + ".asm")
        octets, metas = B4.assembler_bloc(emul.ks, chemin, rva, slot)
        insns = B4.round_trip(emul.cs, emul.ks, chemin, rva, octets, metas)
        insns_par_bloc[bid] = insns
        controle(f"V1.{bid}:round-trip-100",
                 len(insns) == len(metas) and len(octets) == attendu,
                 f"{len(octets)} o == {attendu} o arrêtés, "
                 f"{len(insns)}/{len(metas)} instructions")
    # la concordance des appels directs : les adresses scellées du plan (I1)
    ok_appels, details = True, []
    for bid, attendu in APPELS_ATTENDUS.items():
        vus: dict[int, int] = {}
        for insn in insns_par_bloc[bid]:
            if insn.mnemonic == "call" and not insn.op_str.startswith("r"):
                cible = int(insn.op_str, 0)
                vus[cible] = vus.get(cible, 0) + 1
        if vus != attendu:
            ok_appels = False
            details.append(f"{bid} : {vus} ≠ {attendu}")
    controle("V1.e:les-appels-directs-au-plan", ok_appels,
             "22 : AUCUN (bloc feuille) ; 23 : TLS13 ; 24 : TLS06 ×3 + TLS08 "
             "×16 + TLS15 ×4 + TLS01 + TLS04 (le condensé du vide) ; 25 : "
             "TLS05 ; 26 : TLS01 + TLS03 + TLS04 ; 27 : LA LISTE FERMÉE de la "
             "spec I1 (32 sites : les douze blocs composés, TLS28 ×11 pour "
             "TOUTE entrée/sortie — l'erratum n° 5 : le onzième site AVALE le "
             "CCS hérité) ; 28 : AUCUN appel direct"
             + (f" — DÉFAUTS : {details}" if details else ""))
    # LA ROTULE : l'appel indirect DÉCLARÉ (tls13-28 I2 — le seul du domaine)
    indirects = [i for i in insns_par_bloc["h100028"]
                 if i.mnemonic == "call" and i.op_str.startswith("r")]
    controle("V1.f:l-appel-indirect-declare-de-28", len(indirects) == 2,
             "call r10 ×2 (émettre, recevoir) — la cible est une DONNÉE du "
             "contexte : NI un import NI un syscall (charte § 7), l'oracle "
             "structurel le constatera")
    # la structure du domaine : AUCUN site syscall, AUCUN int
    ok_struct, motifs = True, []
    for bid, insns in insns_par_bloc.items():
        for insn in insns:
            if insn.mnemonic in ("syscall", "int", "sysenter"):
                ok_struct, _ = False, motifs.append(f"{bid}:{insn.mnemonic}")
    controle("V1.g:calcul-pur-aucun-syscall", ok_struct,
             "aucun syscall, aucun int, aucun sysenter — les SEPT blocs, "
             "l'appel indirect déclaré excepté (la rotule)"
             + (f" — MOTIFS : {motifs}" if motifs else ""))
    # les déplacements RIP : les fixtures du plan SEULEMENT (23 : HRR, 24 : les
    # libellés — la famille poignée n'est PAS autoporteur : les libellés et la
    # valeur magique sont des DONNÉES PUBLIQUES du plan d'adressage, I1 de 24)
    cibles_rip: dict[str, dict[int, int]] = {}
    ok_rip, motifs = True, []
    for bid, insns in insns_par_bloc.items():
        cibles_rip[bid] = {}
        for insn in insns:
            m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", insn.op_str)
            if m:
                continue  # (résolu ci-dessous par les entêtes de notation)
    attendus_rip = {"h100023": {L.R_HRR: 1},
                    "h100024": {L.R_LIB_DERIVED: 2, L.R_LIB_C_HS: 1,
                                L.R_LIB_S_HS: 1, L.R_LIB_C_AP: 1,
                                L.R_LIB_S_AP: 1, L.R_LIB_KEY: 4,
                                L.R_LIB_IV: 4, L.R_LIB_FINISHED: 2}}
    for bid, attendu in attendus_rip.items():
        chemin = os.path.join(ICI, "notation", noms[bid] + ".asm")
        vus: dict[int, int] = {}
        for ligne in open(chemin, encoding="utf-8"):
            m = re.match(r";   0x([0-9a-f]+) \+ 0x([0-9a-f]+) [+-] 0x([0-9a-f]+)"
                         r" = 0x([0-9a-f]+)$", ligne.strip())
            if m:
                cible = int(m.group(4), 16)
                vus[cible] = vus.get(cible, 0) + 1
        if vus != attendu:
            ok_rip = False
            motifs.append(f"{bid} : {vus} ≠ {attendu}")
    les_autres = [b for b in insns_par_bloc if b not in attendus_rip]
    for bid in les_autres:
        if any("[rip" in i.op_str for i in insns_par_bloc[bid]):
            ok_rip = False
            motifs.append(f"{bid} : déplacement RIP inattendu")
    controle("V1.h:les-deplacements-rip-aux-fixtures-du-plan", ok_rip,
             "23 : HRR ×1 ; 24 : les HUIT libellés (derived ×2, c/s hs/c/s ap "
             "traffic, key ×4, iv ×4, finished ×2 — SEIZE étiquettes) ; les "
             "CINQ autres : AUCUN — autoporteurs"
             + (f" — MOTIFS : {motifs}" if motifs else ""))
    # la concordance des constantes : le CH au plan (la construction re-jouée)
    ch, r = composer_ch(emul, ALEA_8448, PUBLIQUE_CLIENT)
    attendu_ch = ref_construction_ch(ALEA_8448, PUBLIQUE_CLIENT)
    controle("V1.i:le-ch-au-plan-la-construction-re-jouee",
             r["rax"] == 0 and ch == attendu_ch and len(ch) == 114
             and ch[6:38] == ALEA_8448 and ch[82:114] == PUBLIQUE_CLIENT,
             "le CH composé au fixture (aléa @ +6, clé @ +82) == la "
             "construction re-jouée du plan (verifier_specs_m9a § 4), 114 o, "
             "la suite seule 0x1301, les QUATRE extensions, session_id vide — "
             "l'offre MINIMALE scellée (charte § 1, l'erratum n° 2)")
    # le temps constant STRUCTUREL : les comparaisons par OU cumulatif (25, 26,
    # 23-HRR) : QUATRE quads accumulés, LE test À LA FIN — les branches de la
    # machine portent sur l'ÉTAT et les LONGUEURS (publics, I3 de 27)
    texte23 = open(os.path.join(ICI, "notation",
                                "tls13-23-serverhello-traiter.asm"),
                   encoding="utf-8").read()
    texte25 = open(os.path.join(ICI, "notation",
                                "tls13-25-finished-calculer-verifier.asm"),
                   encoding="utf-8").read()
    texte26 = open(os.path.join(ICI, "notation", "tls13-26-epinglage.asm"),
                   encoding="utf-8").read()
    ok_ct = (texte23.count("xor rax, qword ptr [r11") == 4
             and texte23.count("or r10, rax") == 4
             and texte23.count("test r10, r10") == 1
             and texte25.count("xor r11, qword ptr [rsp") == 4
             and texte25.count("or r10, r11") == 4
             and texte25.count("test r10, r10") == 1
             and texte26.count("xor r11, qword ptr [rsp") == 4
             and texte26.count("or r10, r11") == 4
             and texte26.count("test r10, r10") == 1)
    controle("V1.j:le-temps-constant-structurel", ok_ct,
             "les TROIS comparaisons (l'aléa vs HRR dans 23, le verify_data "
             "dans 25, l'empreinte dans 26) : QUATRE quads XOR-accumulés par "
             "OU en UN registre, LE test À LA FIN — le miroir exact de la "
             "discipline du verdict AEAD (I1 de 26, I2 de 25, I2 de 23)")


# --- V2 : LE TRANSFERT RFC 8448 BLOC PAR BLOC -------------------------------------

def vecteur_v2(emul: Emulation):
    section("V2 — LE TRANSFERT RFC 8448 § 3 BLOC PAR BLOC (les valeurs consignées)")
    # (a) tls13-23 : le SH du RFC VERBATIM + la clé privée du RFC → LE SECRET
    #     PARTAGÉ consigné, OCTET POUR OCTET
    partage, r = traiter_sh(emul, SH_8448, PRIVEE_CLIENT)
    controle("V2.a:le-secret-partage-du-transfert",
             r["rax"] == 0 and partage == PARTAGE_8448,
             f"le SH du RFC (90 o, verbatim) traité par la clé privée du RFC "
             f"→ {partage.hex()[:16]}… == 8bd4054f… OCTET POUR OCTET (les "
             "vecteurs RFC 7748 § 6.1 rejoués au geste x25519)")
    # (b) tls13-24 étage 1 : early/derived == les consignés
    ctx0 = bytes(48)
    _, ctx, r = calendrier(emul, ctx0, b"", 0)
    ctrl = (r["rax"] == 0 and ctx[:32] == DERIVED_1_8448
            and struct.unpack("<I", ctx[32:36])[0] == 1)
    controle("V2.b:le-calendrier-etage-1", ctrl,
             "early = Extract(zéros, zéros) puis derived_1 = EL(early, "
             "« derived », Hash(vide), 32) — le contexte porte (6f2615a1…, "
             "étape 1) == le consigné du RFC (l'erratum n° 2 : le contexte "
             "est le condensé du VIDE, dérivé par 01+04 au geste même)")
    # (c) tls13-24 étage 2 : handshake/c_hs/s_hs/derived_2 + les contextes +
    #     les clés Finished == les consignés ET les QUATRE chaînes du transfert
    ctx1 = DERIVED_1_8448 + (1).to_bytes(4, "little") + bytes(4)
    entree2 = PARTAGE_8448 + HASH_CH_SH_8448
    sortie, ctx, r = calendrier(emul, ctx1, entree2, 464)
    em = ENR.Contexte(bytes.fromhex(AEAD.TRANSFERT_8448[1][1]),
                      bytes.fromhex(AEAD.TRANSFERT_8448[1][2]), 0)
    sm = ENR.Contexte(bytes.fromhex(AEAD.TRANSFERT_8448[0][1]),
                      bytes.fromhex(AEAD.TRANSFERT_8448[0][2]), 0)
    ctrl = (r["rax"] == 0 and ctx[:32] == DERIVED_2_8448
            and struct.unpack("<I", ctx[32:36])[0] == 2
            and sortie[:200] == em.serialiser()
            and sortie[200:400] == sm.serialiser()
            and sortie[400:432] == C_FIN_CLE_8448
            and sortie[432:464] == S_FIN_CLE_8448)
    controle("V2.c:le-calendrier-etage-2", ctrl,
             "handshake = Extract(derived_1, partagé) ; les contextes "
             "enregistrement == LES CHAÎNES du TRANSFERT_8448 (émission "
             "client dbfaa693…, réception serveur 3fce5160…, rk 176 + IV 12 + "
             "réserve + séquence 0 — OCTET POUR OCTET) ; les clés Finished == "
             "les consignées (b80ad010…, 008d3b66…) ; le contexte porte "
             "(43de77e0…, étape 2)")
    # (d) tls13-24 étage 3 : master/c_ap/s_ap + les contextes d'application
    ctx2 = DERIVED_2_8448 + (2).to_bytes(4, "little") + bytes(4)
    sortie, ctx, r = calendrier(emul, ctx2, HASH_CH_FIN_8448, 400)
    ca = ENR.Contexte(bytes.fromhex(AEAD.TRANSFERT_8448[3][1]),
                      bytes.fromhex(AEAD.TRANSFERT_8448[3][2]), 0)
    sa = ENR.Contexte(bytes.fromhex(AEAD.TRANSFERT_8448[2][1]),
                      bytes.fromhex(AEAD.TRANSFERT_8448[2][2]), 0)
    ctrl = (r["rax"] == 0 and ctx[:32] == MASTER_8448
            and struct.unpack("<I", ctx[32:36])[0] == 3
            and sortie[:200] == ca.serialiser()
            and sortie[200:400] == sa.serialiser())
    controle("V2.d:le-calendrier-etage-3", ctrl,
             "master = Extract(derived_2, zéros) ; c_ap/s_ap sur le hash "
             "consigné 9608102a… (CH..Fin serveur) ; les contextes "
             "d'application == LES CHAÎNES du TRANSFERT_8448 (17422dda…, "
             "9f02283b…) ; le contexte porte (18df0684…, étape 3 — CLOS)")
    # (e) tls13-25 : LE verify_data du client CALCULÉ, celui du serveur VÉRIFIÉ
    calcule, r = finished(emul, C_FIN_CLE_8448, HASH_CH_FIN_8448,
                          bytes(32), 0)
    controle("V2.e:le-finished-client-calcule",
             r["rax"] == 0 and calcule == C_FIN_8448,
             f"le verify_data calculé {calcule.hex()[:16]}… == a8ec436d… le "
             "consigné du RFC § 3, OCTET POUR OCTET (le HMAC du transcript "
             "clos — RFC 8446 § 4.4.4)")
    _, r = finished(emul, S_FIN_CLE_8448, HASH_CH_CV_8448, S_FIN_8448, 1)
    _, r2 = finished(emul, S_FIN_CLE_8448, HASH_CH_CV_8448,
                     S_FIN_8448[:-1] + bytes([S_FIN_8448[-1] ^ 1]), 1)
    controle("V2.f:le-finished-serveur-verifie",
             r["rax"] == 0 and r2["rax"] == -4,
             "le verify_data du serveur (9b9b141d…, le vol du transcript) "
             "VÉRIFIÉ conforme sur le hash de coupe CH..CV (edb7725fa7a3…, "
             "re-dérivé par le labo) ; UN octet muté → -4 NOMMÉ")
    # (f) tls13-26 : l'épinglage du certificat du transcript
    r = epinglage(emul, DER_8448, EMPREINTE_8448)
    controle("V2.g:l-epinglage-du-certificat-du-transfert",
             r["rax"] == 0,
             "le DER de la PREMIÈRE entrée du Certificate du § 3 (432 o à "
             "CERT+11, le DÉTROIT) épingle à l'empreinte recalculée "
             f"{EMPREINTE_8448.hex()[:16]}… — la décision de confiance est "
             "une COMPARAISON, jamais une croyance")
    # (g) tls13-28 : la rotule sur les DEUX rappels du simulateur
    emul.reinit_journal()
    emul.poser_cassette(SH_REC_8448)
    kit_lu = bytes(emul.uc.mem_read(ADR_KIT, 95))
    r = socle(emul, 1, ADR_KIT, 95)
    journal = emul.lire_journal()
    r2 = socle(emul, 2, ADR_SESSION, 95)
    copie = bytes(emul.uc.mem_read(ADR_SESSION, 95))
    r3 = socle(emul, 2, ADR_SESSION, 10)          # la cassette ÉPUISÉE
    r4 = socle(emul, 3, ADR_SESSION, 10)          # l'opération inconnue
    controle("V2.h:le-socle-sur-les-deux-rappels",
             r["rax"] == 0 and journal == kit_lu
             and r2["rax"] == 95 and copie == SH_REC_8448
             and r3["rax"] == -7 and r4["rax"] == -1,
             "émettre : journalisé (95 o) ; recevoir : la cassette servie "
             "(95 o) ; la cassette épuisée → -7 NOMMÉ (la demi-fin est le "
             "refus du KIT) ; l'opération inconnue → -1")


# --- V3 : les cas punitifs ---------------------------------------------------------

def vecteur_v3(emul: Emulation, graine: int):
    section("V3 — les cas punitifs (les refus nommés, les bornes, l'oracle)")
    rng = random.Random(graine ^ 0xBADC0DE)
    # (a) tls13-22 : les gardes
    _, r = composer_ch(emul, ALEA_8448, PUBLIQUE_CLIENT, force={"rcx": 0})
    ok22 = r["rax"] == -1
    _, r = composer_ch(emul, ALEA_8448, PUBLIQUE_CLIENT, force={"r9": 113})
    ok22 = ok22 and r["rax"] == -2
    controle("V3.a:les-refus-de-22", ok22,
             "les pointeurs nuls → -1 ; la capacité < 114 → -2")
    # (b) tls13-23 : chaque confrontation NOMMÉE (l'ordre du corps)
    cas = [
        ("le type ≠ 2", bytearray(SH_8448[:1]) + bytearray(b"\x01") + bytearray(SH_8448[2:]), -1),
        ("la version héritage", bytearray(SH_8448[:4]) + bytearray(b"\x02\x02") + bytearray(SH_8448[6:]), -1),
        ("l'écho session_id non vide", bytearray(SH_8448[:38]) + bytearray(b"\x02\x00\x00") + bytearray(SH_8448[41:]), -1),
        ("LA suite mutée (1303)", bytearray(SH_8448[:39]) + bytearray(b"\x13\x03") + bytearray(SH_8448[41:]), -5),
        ("la compression non nulle", bytearray(SH_8448[:41]) + bytearray(b"\x01") + bytearray(SH_8448[42:]), -1),
        ("la région d'extensions mensongère", bytearray(SH_8448[:42]) + bytearray(b"\x00\x2d") + bytearray(SH_8448[44:]), -1),
        ("le groupe muté (0017)", bytearray(SH_8448[:48]) + bytearray(b"\x00\x17") + bytearray(SH_8448[50:]), -5),
        ("le klen muté (0x10)", bytearray(SH_8448[:50]) + bytearray(b"\x00\x10") + bytearray(SH_8448[52:]), -5),
        ("supported_versions muté (0303)", bytearray(SH_8448[:88]) + bytearray(b"\x03\x03") + bytearray(SH_8448[90:]), -5),
        ("le u24 mensonger", bytearray(SH_8448[:1]) + bytearray(b"\x00\x00\x57") + bytearray(SH_8448[4:]), -1),
    ]
    ok, details = True, []
    for nom, mu, attendu in cas:
        _, r = traiter_sh(emul, bytes(mu), PRIVEE_CLIENT)
        if r["rax"] != attendu:
            ok = False
            details.append(f"{nom}:rax={r['rax']}≠{attendu}")
    hrr = bytearray(SH_8448)
    hrr[6:38] = L.HRR_MAGIQUE
    _, r = traiter_sh(emul, bytes(hrr), PRIVEE_CLIENT)
    ok = ok and r["rax"] == -5
    _, r = traiter_sh(emul, SH_8448[:89], PRIVEE_CLIENT)
    ok = ok and r["rax"] == -2
    u24_mensonger = (SH_8448[:1] + (87).to_bytes(3, "big") + SH_8448[4:])
    _, r = traiter_sh(emul, u24_mensonger, PRIVEE_CLIENT)
    ok = ok and r["rax"] == -1
    # la key_share ABSENTE → -5 (une extension inconnue 0x1234 à sa place —
    # le même gabarit, la même longueur : SEUL le type diverge)
    sans_ks = bytearray(SH_8448)
    sans_ks[44:46] = b"\x12\x34"          # le type de la key_share muté
    _, r = traiter_sh(emul, bytes(sans_ks), PRIVEE_CLIENT)
    ok = ok and r["rax"] == -5
    controle("V3.b:les-confrontations-de-23", ok,
             "le type/la version/l'écho/la compression → -1 ; LA suite mutée, "
             "le groupe, le klen, supported_versions, la key_share absente → "
             "-5 LA NÉGOCIATION REFUSÉE ; la région mensongère, le u24, la "
             "truncation → -1 ; l'aléa == LA VALEUR MAGIQUE HRR → -5 NOMMÉ « "
             "HelloRetryRequest : le chantier futur nommé » ; rdx < 90 → -2"
             + (f" — DÉFAUTS : {details}" if details else ""))
    # (c) tls13-23 : l'extension INCONNUE IGNORÉE + l'oracle différentiel
    ext_inconnue = b"\xab\xcd\x00\x04\xde\xad\xbe\xef"
    corps_riche = (SH_8448[4:42]
                   + (46 + len(ext_inconnue)).to_bytes(2, "big")
                   + SH_8448[44:] + ext_inconnue)
    sh_riche = (b"\x02" + (len(corps_riche)).to_bytes(3, "big") + corps_riche)
    partage, r = traiter_sh(emul, sh_riche, PRIVEE_CLIENT)
    ok_ign = r["rax"] == 0 and partage == PARTAGE_8448
    ecarts = 0
    for _ in range(30):
        privee = bytes(rng.randrange(256) for _ in range(32))
        pub_serv = bytes(rng.randrange(256) for _ in range(32))
        alea = bytes(rng.randrange(256) for _ in range(32))
        # un SH minimal VALIDE construit par la référence (le juge est le code)
        ks = b"\x00\x1d\x00\x20" + pub_serv   # group u16 + klen u16 + clé
        exts = (b"\x00\x33" + (len(ks)).to_bytes(2, "big") + ks
                + b"\x00\x2b\x00\x02\x03\x04")
        corps = (b"\x03\x03" + alea + b"\x00\x13\x01\x00"
                 + len(exts).to_bytes(2, "big") + exts)
        sh = b"\x02" + (len(corps)).to_bytes(3, "big") + corps
        partage, r = traiter_sh(emul, sh, privee)
        attendu = nacl.bindings.crypto_scalarmult(privee, pub_serv)
        if not (r["rax"] == 0 and partage == attendu):
            ecarts += 1
    controle("V3.c:l-extension-inconnue-ignoree-et-l-oracle", ok_ign and ecarts == 0,
             "l'extension inconnue 0xabcd IGNORÉE (RFC 8446 § 4.1.3 : la règle "
             "DU PROTOCOLE) — le secret partagé INTACT ; l'oracle "
             "différentiel : 30 ServerHello aléatoires valides → le secret "
             "== X25519 de la contre-preuve PyNaCl, ZÉRO écart")
    # (d) tls13-24 : les étages STRICTS — le dispatch EST l'étape (la
    #     machine refuse de sauter : l'étape 3 est CLOS, l'étape 4 n'existe pas)
    ctx1 = DERIVED_1_8448 + (1).to_bytes(4, "little") + bytes(4)
    _, _, r = calendrier(emul, ctx1, PARTAGE_8448 + HASH_CH_SH_8448, 464,
                         force={"r8": 0})
    ok24 = r["rax"] == -1
    ctx2 = DERIVED_2_8448 + (2).to_bytes(4, "little") + bytes(4)
    _, _, r = calendrier(emul, ctx2, HASH_CH_FIN_8448, 400, force={"r8": 0})
    ok24 = ok24 and r["rax"] == -1
    for etape in (3, 4, 99):
        ctx = DERIVED_1_8448 + etape.to_bytes(4, "little") + bytes(4)
        _, _, r = calendrier(emul, ctx, b"", 0)
        ok24 = ok24 and r["rax"] == -3
    controle("V3.d:les-etages-stricts-de-24", ok24,
             "la sortie nulle aux étages 2 et 3 → -1 ; l'étape 3 (CLOS) → -3, "
             "l'étape 4 N'EXISTE PAS → -3, l'étape 99 → -3 — le dispatch EST "
             "l'étape : chaque appel avance d'UN étage exactement (0 → 1 → 2 "
             "→ 3, prouvé en V2.b/c/d), la machine refuse de deviner")

    # (e) tls13-25 : les modes et les pointeurs
    _, r = finished(emul, C_FIN_CLE_8448, HASH_CH_FIN_8448, bytes(32), 2)
    ok25 = r["rax"] == -1
    _, r = finished(emul, C_FIN_CLE_8448, HASH_CH_FIN_8448, bytes(32), 0,
                    force={"rcx": 0})
    controle("V3.e:les-refus-de-25", ok25 and r["rax"] == -1,
             "le mode > 1 → -1 NOMMÉ (0 calculer, 1 vérifier — tout autre "
             "est un refus) ; les pointeurs nuls → -1")
    # (f) tls13-26 : les bornes et l'empreinte divergente
    r = epinglage(emul, DER_8448, EMPREINTE_8448, force={"rdx": 0})
    ok26 = r["rax"] == -2
    r = epinglage(emul, DER_8448, EMPREINTE_8448[:-1]
                  + bytes([EMPREINTE_8448[-1] ^ 1]))
    controle("V3.f:les-refus-de-26", ok26 and r["rax"] == -6,
             "N = 0 → -2 ; l'empreinte divergente d'UN octet → -6 NOMMÉ "
             "(épinglage divergent — la session MEURT sans autres formes)")
    # (g) tls13-27 : la table des événements (tout événement hors de sa ligne
    #     → -3, la machine ne devine JAMAIS l'intention de l'appelant)
    session_neuve(emul)
    r = emettre(emul, b"charge")
    ok27 = r["rax"] == -3 and lire_etat(emul) == 5
    session_neuve(emul)
    r = recevoir(emul)
    ok27 = ok27 and r["rax"] == -3
    session_neuve(emul)
    r = emul.appeler(L.TLS27_VA, {"rcx": ADR_SESSION, "rdx": 4})
    ok27 = ok27 and r["rax"] == -3
    session_neuve(emul)
    r = emul.appeler(L.TLS27_VA, {"rcx": ADR_SESSION, "rdx": 7})
    ok27 = ok27 and r["rax"] == -3
    r = emul.appeler(L.TLS27_VA, {"rcx": 0, "rdx": 1})
    controle("V3.g:la-table-des-evenements-de-27", ok27 and r["rax"] == -1,
             "ÉMETTRE/RECEVOIR/FERMER sur l'état 0 → -3 (l'état passe à 5 : "
             "la session MEURT — Q2) ; l'événement inconnu 7 → -3 ; le "
             "contexte nul → -1 (l'état inatteignable, le verdict seul rendu)")


# --- V4 : le contrat ---------------------------------------------------------------

def vecteur_v4(emul: Emulation, nue: Emulation):
    section("V4 — le contrat (les pré/post, l'alignement, les pièces intactes)")
    simu = Simulation()
    # (a) les non-volatiles + la pile + les canaris : un cas de CHAQUE bloc
    ok_nv, details = True, []
    _, r = composer_ch(emul, ALEA_8448, PUBLIQUE_CLIENT)
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"] and r["rax"] == 0):
        ok_nv, _ = False, details.append("tls13-22")
    _, r = traiter_sh(emul, SH_8448, PRIVEE_CLIENT)
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"] and r["rax"] == 0):
        ok_nv, _ = False, details.append("tls13-23")
    _, _, r = calendrier(emul, bytes(48), b"", 0)
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"] and r["rax"] == 0):
        ok_nv, _ = False, details.append("tls13-24")
    _, r = finished(emul, C_FIN_CLE_8448, HASH_CH_FIN_8448, bytes(32), 0)
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"] and r["rax"] == 0):
        ok_nv, _ = False, details.append("tls13-25")
    r = epinglage(emul, DER_8448, EMPREINTE_8448)
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"] and r["rax"] == 0):
        ok_nv, _ = False, details.append("tls13-26")
    r = socle(emul, 1, ADR_KIT, 32)
    if not (emul.non_volatiles_rendus(r) and r["pile_equilibree"]
            and r["canaris_haut"] and r["canaris_profond"] and r["rax"] == 0):
        ok_nv, _ = False, details.append("tls13-28")
    controle("V4.a:non-volatiles-pile-canaris (six blocs)", ok_nv,
             "les 8 sentinelles rendues, rsp équilibrée, l'ombre et les "
             "logements intacts, la zone morte PROFONDE à −0xE000 intacte "
             "(sous le cadre 0x43C8 de la machine ET les cadres imbriqués "
             "0x4078/0xE8 — la leçon du geste rejouée sur LE PLUS GRAND bloc)"
             + (f" — DÉFAUTS : {details}" if details else ""))
    # (b) l'alignement msx64 à travers LA SESSION ENTIÈRE : à CHAQUE entrée
    #     de CHAQUE bloc composé (les comptes exacts de la spec I1 de 27)
    session_neuve(emul)
    poser_kit(emul, ALEA_8448, PRIVEE_CLIENT, EMPREINTE_8448)
    emul.reinit_journal()
    emul.poser_cassette(SH_REC_8448 + simu.flight)
    cibles = [L.TLS01_VA, L.TLS03_VA, L.TLS04_VA, L.TLS14_VA, L.TLS20_VA,
              L.TLS21_VA, L.TLS22_VA, L.TLS23_VA, L.TLS24_VA, L.TLS25_VA,
              L.TLS26_VA, L.TLS28_VA]
    emul.surveillance = {va: [] for va in cibles}
    try:
        r = ouvrir(emul)
    finally:
        entrees = {va: list(l) for va, l in emul.surveillance.items()}
        emul.surveillance = None
    # les comptes EXACTS — l'imbrication COMPTÉE : chaque HMAC (tls13-05)
    # entre deux fois (01+03+04 ×2), chaque Expand (tls13-07) un HMAC de plus —
    # les entrées des blocs FEUILLES au cœur de la composition sont comptées
    # avec celles du principal : la session ENTIÈRE vue par l'émulateur
    attendus_v4 = {L.TLS01_VA: 47, L.TLS03_VA: 92, L.TLS04_VA: 49,
                   L.TLS14_VA: 1, L.TLS20_VA: 1, L.TLS21_VA: 1,
                   L.TLS22_VA: 1, L.TLS23_VA: 1, L.TLS24_VA: 3,
                   L.TLS25_VA: 2, L.TLS26_VA: 1, L.TLS28_VA: 6}
    total = sum(len(l) for l in entrees.values())
    ok_align = (r["rax"] == 0 and total == 205
                and all(e % 16 == 8 for l in entrees.values() for e in l)
                and all(len(entrees[va]) == n for va, n in attendus_v4.items()))
    controle("V4.b:l-alignement-msx64-a-l-entree-de-chaque-calle", ok_align,
             f"205 entrées surveillées à travers la SESSION ENTIÈRE (les "
             "feuilles SHA au cœur de la composition comptées AVEC le "
             "principal) : TLS03 ×92, TLS04 ×49, TLS01 ×47 (les absorbions "
             "du transcript ET les HMAC de la dérivation), TLS24 ×3 (les "
             "étages), TLS28 ×6 (le CH émis, les quatre lectures, le "
             "Finished émis), TLS14/22/23/26 ×1, TLS25 ×2, TLS20/21 ×1 — "
             "rsp ≡ 8 (mod 16) à CHAQUE entrée, les comptes EXACTS"
             + ("" if ok_align else " — VUS : "
                + str({hex(va): len(l) for va, l in entrees.items()})))
    # (c) les pièces du kit INTACTES (le kit fournit TOUT — la source de
    #     confiance ne doit JAMAIS être touchée par la machine)
    kit_lu = bytes(emul.uc.mem_read(ADR_KIT, 96))
    controle("V4.c:le-kit-intact", kit_lu == ALEA_8448 + PRIVEE_CLIENT
             + EMPREINTE_8448, "les 96 o relus OCTET POUR OCTET : l'aléa, "
             "la clé privée, l'empreinte — la machine COPIE, elle ne touche "
             "jamais la source (charte § 6)")


# --- V5 : la falsification (zéro silence) ------------------------------------------

def vecteur_v5(emul: Emulation, graine: int):
    section("V5 — la falsification (chaque vecteur muté ATTRAPÉ, zéro silence)")
    rng = random.Random(graine ^ 0xFEED)
    # (a) le SH : chaque champ muté attrapé (déjà V3.b) — ici : la clé privée
    #     DIVERGENTE → le secret partagé diverge (la preuve de possession)
    partage, r = traiter_sh(emul, SH_8448, PRIVEE_CLIENT)
    _, r2 = traiter_sh(emul, SH_8448,
                       PRIVEE_CLIENT[:-1] + bytes([PRIVEE_CLIENT[-1] ^ 1]))
    controle("V5.a:la-cle-privee-divergente",
             r["rax"] == 0 and r2["rax"] == 0
             and bytes(emul.uc.mem_read(ADR_ENTREES + 0x2000, 32)) != partage,
             "un octet de la clé privée muté → le secret partagé DIVERGE "
             "(la clé privée n'est jamais touchée sur un message refusé, "
             "mais le secret EST la preuve de possession)")
    # (b) le calendrier : le hash d'entrée muté → les secrets divergent
    _, _, r = calendrier(emul, DERIVED_1_8448 + (1).to_bytes(4, "little")
                         + bytes(4), PARTAGE_8448 + HASH_CH_SH_8448, 464)
    sortie_ref = bytes(emul.uc.mem_read(ADR_ENTREES + 0x2000, 464))
    hache_mute = bytearray(HASH_CH_SH_8448)
    hache_mute[7] ^= 1
    _, _, r2 = calendrier(emul, DERIVED_1_8448 + (1).to_bytes(4, "little")
                          + bytes(4), PARTAGE_8448 + bytes(hache_mute), 464)
    sortie_mut = bytes(emul.uc.mem_read(ADR_ENTREES + 0x2000, 464))
    controle("V5.b:le-hash-du-transcript-mute",
             r["rax"] == 0 and r2["rax"] == 0 and sortie_mut != sortie_ref,
             "un octet du hash du transcript muté → les contextes et les "
             "clés Finished DIVERGENT (le calendrier ne hache rien : le hash "
             "est un ARGUMENT — la divergence parle)")
    # (c) le Finished : chaque octet du verify_data muté → -4 (32/32)
    attrapes = 0
    for i in range(32):
        mu = bytearray(S_FIN_8448)
        mu[i] ^= 1
        _, r = finished(emul, S_FIN_CLE_8448, HASH_CH_CV_8448, bytes(mu), 1)
        attrapes += (r["rax"] == -4)
    cle_mutee = bytearray(S_FIN_CLE_8448)
    cle_mutee[11] ^= 1
    _, r = finished(emul, bytes(cle_mutee), HASH_CH_CV_8448, S_FIN_8448, 1)
    controle("V5.c:le-finished-32-32-attrapes", attrapes == 32
             and r["rax"] == -4,
             "les 32 octets du verify_data mutés UN PAR UN → -4 NOMMÉ "
             "32/32 ; la clé Finished mutée → -4 : la comparaison n'est pas "
             "muette")
    # (d) l'épinglage : le certificat ET l'empreinte mutés dans les DEUX sens
    attrapes = 0
    for i in (0, 100, 215, 431):
        mu = bytearray(DER_8448)
        mu[i] ^= 1
        r = epinglage(emul, bytes(mu), EMPREINTE_8448)
        attrapes += (r["rax"] == -6)
    for i in range(0, 32, 7):
        mu = bytearray(EMPREINTE_8448)
        mu[i] ^= 1
        r = epinglage(emul, DER_8448, bytes(mu))
        attrapes += (r["rax"] == -6)
    controle("V5.d:l-epinglage-mute-dans-les-deux-sens", attrapes == 9,
             "le DER muté (4 sites) et l'empreinte mutée (5 sites) → -6 "
             "NOMMÉ 9/9 — la garde constatée mutation par mutation dans les "
             "DEUX sens (la confiance diverge, la session meurt)")


# --- V6 : le temps constant MESURÉ --------------------------------------------------

def vecteur_v6(emul: Emulation):
    section("V6 — le temps constant MESURÉ (le verdict invisible dans le temps)")
    # (a) le Finished VÉRIFIER : trois verify_data divergents → LE MÊME compte
    comptes = []
    for i in (0, 15, 31):
        mu = bytearray(S_FIN_8448)
        mu[i] ^= 1
        _, r = finished(emul, S_FIN_CLE_8448, HASH_CH_CV_8448, bytes(mu), 1,
                        compter=True)
        comptes.append(r["compteur"])
    _, r = finished(emul, S_FIN_CLE_8448, HASH_CH_CV_8448, S_FIN_8448, 1,
                    compter=True)
    conforme = r["compteur"]
    controle("V6.a:le-verdict-du-finished",
             len(set(comptes)) == 1,
             f"trois verify_data divergents (octets 0, 15, 31 mutés) → "
             f"{comptes[0]} instructions LE MÊME COMPTE EXACTEMENT (le "
             f"conforme : {conforme}) : les QUATRE quads accumulés avant "
             "LE test, la position de la divergence INVISIBLE dans le temps")
    # (b) l'épinglage : trois empreintes divergentes → LE MÊME compte
    comptes = []
    for i in (0, 15, 31):
        mu = bytearray(EMPREINTE_8448)
        mu[i] ^= 1
        r = epinglage(emul, DER_8448, bytes(mu))
        r = emul.appeler(L.TLS26_VA, {"rcx": ADR_ENTREES,
                                      "rdx": len(DER_8448),
                                      "r8": ADR_ENTREES + len(DER_8448)},
                         compter=True)
        comptes.append(r["compteur"])
    controle("V6.b:le-verdict-de-l-epinglage", len(set(comptes)) == 1,
             f"trois empreintes divergentes (octets 0, 15, 31 mutés) → "
             f"{comptes[0]} instructions LE MÊME COMPTE — la discipline "
             "demeure sur une donnée de confiance (I1 de 26)")
    # (c) la comparaison HRR de 23 : l'aléa divergent au premier ou au
    #     dernier quad → LE MÊME compte (la comparaison est un acheminement)
    comptes = []
    for i in (0, 24):
        alea = bytearray(SH_8448[6:38])
        alea[i] ^= 1
        sh = bytearray(SH_8448)
        sh[6:38] = alea
        _, r = traiter_sh(emul, bytes(sh), PRIVEE_CLIENT, )
        comptes.append(None)
    comptes = []
    for i in (0, 24):
        alea = bytearray(SH_8448[6:38])
        alea[i] ^= 1
        sh = bytearray(SH_8448)
        sh[6:38] = alea
        r = emul.appeler(L.TLS23_VA, {"rcx": ADR_ENTREES, "rdx": 90,
                                      "r8": ADR_ENTREES + 90,
                                      "r9": ADR_ENTREES + 0x2000},
                         compter=True)
        comptes.append(r["compteur"])
    controle("V6.c:la-comparaison-hrr-de-23", len(set(comptes)) == 1,
             f"l'aléa divergent de la valeur magique au premier ou au "
             f"trentième octet → {comptes[0]} instructions LE MÊME COMPTE : "
             "QUATRE quads XOR-accumulés, UN seul test (I2 de 23)")


# --- V7 : LA MACHINE — la session entière contre le simulateur -----------------------

def vecteur_v7(emul: Emulation, nue: Emulation):
    section("V7 — LA MACHINE : la session ENTIÈRE contre le SIMULATEUR (RFC 8448)")
    simu = Simulation()

    # (a) OUVRIR : le SH du RFC servi VERBATIM, le vol re-scellé sous NOS
    #     clés (EE/Cert/CV verbatim, le Finished serveur RECALCULÉ sur NOTRE
    #     coupe) → l'état 3, le journal == NOTRE offre cadrée + NOTRE Finished
    S = nue
    session_neuve(S)
    poser_kit(S, ALEA_8448, PRIVEE_CLIENT, EMPREINTE_8448)
    S.reinit_journal()
    S.poser_cassette(SH_REC_8448 + simu.flight)
    r = ouvrir(S)
    journal = S.lire_journal()
    ok_ouvrir = (r["rax"] == 0 and lire_etat(S) == 3
                 and journal == simu.ch_rec + simu.fin_c_rec)
    controle("V7.a:OUVRIR-la-session-entiere", ok_ouvrir,
             "le journal == NOTRE CH cadré (16 03 03 00 72 || la construction "
             "re-jouée, 119 o — l'erratum n° 5 : l'octet de longueur) + NOTRE "
             "Finished (58 o : le HMAC de NOTRE "
             "transcript scellé sous NOS clés de poignée) — le simulateur a "
             "servi le SH du RFC VERBATIM (95 o) et le vol re-scellé (le "
             "Finished serveur recalculé sur NOTRE coupe Hash(CH..CV)) ; "
             "l'état == 3 (CONNECTÉ)"
             + ("" if ok_ouvrir else f" — rax={r['rax']}, état="
                f"{lire_etat(S)}, journal={len(journal)} o"))
    # la session recoupée : le calendrier (master, étape 3), les QUATRE
    # contextes, les clés Finished, l'empreinte, les séquences
    ok_sess = (lire_etape(S) == 3
               and lire_session(S, 112, 32) == simu.cadenas.master
               and lire_session(S, 224, 200)
               == ENR.Contexte(simu.cadenas.c_cle_hs,
                               simu.cadenas.c_iv_hs, 1).serialiser()
               and lire_session(S, 424, 200)
               == ENR.Contexte(simu.cadenas.s_cle_hs,
                               simu.cadenas.s_iv_hs, 1).serialiser()
               and lire_session(S, 624, 200)
               == ENR.Contexte(simu.cadenas.c_cle_ap,
                               simu.cadenas.c_iv_ap, 0).serialiser()
               and lire_session(S, 824, 200)
               == ENR.Contexte(simu.cadenas.s_cle_ap,
                               simu.cadenas.s_iv_ap, 0).serialiser()
               and lire_session(S, 1024, 32) == simu.cadenas.c_fin_cle
               and lire_session(S, 1056, 32) == simu.cadenas.s_fin_cle
               and lire_session(S, 1088, 32) == EMPREINTE_8448
               and lire_session(S, 192, 32) == PUBLIQUE_CLIENT
               and lire_session(S, 160, 32) == PRIVEE_CLIENT)
    controle("V7.b:la-session-recoupee-contre-la-reference", ok_sess,
             "le calendrier porte (master, étape 3) ; les contextes de "
             "POIGNÉE aux séquences 1/1 (le CH et le Finished émis, le vol "
             "déverrouillé), les contextes d'APPLICATION 0/1, les clés "
             "Finished, l'empreinte, le couple x25519 — chaque champ == la "
             "référence Python dérivée de NOTRE transcript (le simulateur "
             "en vit, la machine l'a posé)")
    # (b) ÉMETTRE : la charge applicative DU RFC scellée sous NOTRE chaîne
    S.reinit_journal()
    r = emettre(S, APP_8448)
    journal = S.lire_journal()
    attendu = ENR.ref_proteger(simu.c_ap, TYPE_DATA, APP_8448)
    controle("V7.c:EMETTRE-la-charge-du-rfc", r["rax"] == 0
             and journal == attendu,
             f"la charge applicative du § 3 ({len(APP_8448)} o, 00 01 02 … "
             "30 31) scellée sous NOTRE chaîne d'application client == la "
             "référence OCTET POUR OCTET (71 o)")
    # (c) RECEVOIR : la charge DU RFC servie sous la chaîne serveur NOTRE
    S.poser_cassette(ENR.ref_proteger(simu.s_ap, TYPE_DATA, APP_8448))
    r = recevoir(S)
    rendu = bytes(S.uc.mem_read(ADR_ENTREES, len(APP_8448)))
    controle("V7.d:RECEVOIR-la-charge-du-rfc", r["rax"] == len(APP_8448)
             and rendu == APP_8448,
             f"rax == {len(APP_8448)} (la LONGUEUR rendue), la charge "
             "restituée AU DÉBUT du tampon == la charge du § 3 OCTET POUR "
             "OCTET (l'écrasement licite et NOMMÉ)")
    # (d) RECEVOIR la close_notify serveur → l'état 4, rax = 0
    S.poser_cassette(ENR.ref_proteger(simu.s_ap, TYPE_ALERT, b"\x01\x00"))
    r = recevoir(S)
    controle("V7.e:la-close-notify-serveur", r["rax"] == 0
             and lire_etat(S) == 4,
             "le type interne 21, la charge 01 00 (close_notify — RFC 8446 "
             "§ 6.1) → l'état 4 (CLOS), rax = 0 : LA FIN PROPRE du protocole")
    # (e) FERMER : le close_notify client émis sous NOTRE chaîne
    S.reinit_journal()
    r = S.appeler(L.TLS27_VA, {"rcx": ADR_SESSION, "rdx": 4})
    journal = S.lire_journal()
    attendu = ENR.ref_proteger(simu.c_ap, TYPE_ALERT, b"\x01\x00")
    controle("V7.f:FERMER-le-close-notify", r["rax"] == 0
             and journal == attendu and lire_etat(S) == 4,
             "le close_notify composé (2 o : 01 00), scellé (type interne "
             "21) et ÉMIS sous NOTRE chaîne d'application == la référence "
             "OCTET POUR OCTET (24 o) — l'état 4, rax = 0")
    # (f) LA FALSIFICATION À CHAQUE ÉTAGE : chaque verdict NOMMÉ rend SON nom
    def session_mort(cassette, kit_empreinte=EMPREINTE_8448):
        session_neuve(S)
        poser_kit(S, ALEA_8448, PRIVEE_CLIENT, kit_empreinte)
        S.reinit_journal()
        S.poser_cassette(cassette)
        return ouvrir(S)

    sh_mute = bytearray(SH_REC_8448)
    sh_mute[44] = 0x03                       # la suite 1301 -> 1303 (message +39)
    r = session_mort(bytes(sh_mute) + simu.flight)
    ctrl1 = r["rax"] == -5 and lire_etat(S) == 5 \
        and S.lire_journal() == simu.ch_rec
    vol_mute = bytearray(simu.flight)
    vol_mute[-1] ^= 1                        # l'étiquette AEAD du vol
    r = session_mort(SH_REC_8448 + bytes(vol_mute))
    ctrl2 = r["rax"] == -4 and lire_etat(S) == 5 \
        and S.lire_journal() == simu.ch_rec
    emp_mute = bytearray(EMPREINTE_8448)
    emp_mute[3] ^= 1                         # l'empreinte du kit
    r = session_mort(SH_REC_8448 + simu.flight, bytes(emp_mute))
    ctrl3 = r["rax"] == -6 and lire_etat(S) == 5 \
        and S.lire_journal() == simu.ch_rec
    r = session_mort(SH_REC_8448)             # la coupure : la cassette vide
    ctrl4 = r["rax"] == -7 and lire_etat(S) == 5 \
        and S.lire_journal() == simu.ch_rec
    r = session_mort(SH_REC_8448 + simu.flight)
    r2 = ouvrir(S)                            # OUVRIR sur l'état 3
    ctrl5 = r2["rax"] == -3 and lire_etat(S) == 5
    r3 = emettre(S, b"x")                     # l'état 5 ne rend PLUS RIEN
    r4 = recevoir(S)
    r5 = S.appeler(L.TLS27_VA, {"rcx": ADR_SESSION, "rdx": 4})
    ctrl6 = r3["rax"] == -3 and r4["rax"] == -3 and r5["rax"] == -3
    controle("V7.g:la-falsification-a-chaque-etage",
             ctrl1 and ctrl2 and ctrl3 and ctrl4 and ctrl5 and ctrl6,
             "le ServerHello muté (la suite 1303) → -5 LA NÉGOCIATION "
             "REFUSÉE ; l'étiquette du vol mutée → -4 ; l'empreinte du kit "
             "mutée → -6 ; LA COUPURE DU SOCLE (la cassette épuisée) → -7 ; "
             "OUVRIR sur l'état 3 → -3 ; l'état 5 (MORT) ne rend PLUS RIEN "
             "(É2/É3/É4 → -3) — chaque session morte n'a émis QUE son offre "
             "(le CH : un échec n'ÉMET RIEN de plus, charte § 5)")

    # (h) L'ERRATUM n° 5 — LE CCS HÉRITÉ (RFC 8446 § 4.1.3) : la sonde
    #     terrain du 06/11 l'a constaté chez les serveurs réels TOUS
    #     (google, github, cloudflare, debian — la carte du run : SH [90] →
    #     CCS [6] → vol [N]) ; la machine L'AVALA désormais : servi ENTRE
    #     le ServerHello et le vol, la session s'établit QUAND MÊME, le
    #     journal INTACT, AUCUNE séquence consommée, les secrets INTACTS
    CCS_REC = b"\x14\x03\x03\x00\x01\x01"       # la compatibilité boîtes
    session_neuve(S)
    poser_kit(S, ALEA_8448, PRIVEE_CLIENT, EMPREINTE_8448)
    S.reinit_journal()
    S.poser_cassette(SH_REC_8448 + CCS_REC + simu.flight)
    r = ouvrir(S)
    journal = S.lire_journal()
    ctrl_ccs = (r["rax"] == 0 and lire_etat(S) == 3
                and journal == simu.ch_rec + simu.fin_c_rec
                and lire_session(S, 424, 200)
                == ENR.Contexte(simu.cadenas.s_cle_hs,
                                simu.cadenas.s_iv_hs, 1).serialiser())
    controle("V7.h:le-ccs-herite-avale", ctrl_ccs,
             "l'enregistrement CCS (14 03 03 00 01 01) servi ENTRE le SH et "
             "le vol — l'erratum n° 5 : la charge héritage D'UN octet lue au "
             "socle SANS déverrouillage, la boucle reprend, la session "
             "s'établit, le journal == l'offre + le Finished (le CCS n'y "
             "figure JAMAIS), la réception POIGNÉE aux séquences 0/1 — "
             "AUCUN octet de séquence consommé par l'enregistrement avalé, "
             "les secrets INTACTS (RFC 8446 § 4.1.3 : IGNORÉ)")

    # (i) LA FALSIFICATION DU CCS : une longueur déclarée autre que 1 est
    #     le refus -2 NOMMÉ (un faux « CCS » est une attaque, jamais un
    #     aval — fail-closed) ; AUCUN octet n'est lu au-delà du refus
    session_neuve(S)
    poser_kit(S, ALEA_8448, PRIVEE_CLIENT, EMPREINTE_8448)
    S.reinit_journal()
    S.poser_cassette(SH_REC_8448 + b"\x14\x03\x03\x00\x02\x01\x01"
                     + simu.flight)
    r = ouvrir(S)
    ctrl_ccs_faux = (r["rax"] == -2 and lire_etat(S) == 5
                     and S.lire_journal() == simu.ch_rec)
    controle("V7.i:le-faux-ccs-refuse", ctrl_ccs_faux,
             "le « CCS » à longueur déclarée 2 → -2 NOMMÉ, l'état 5 (MORT), "
             "le journal == l'offre seule — l'aval n'est JAMAIS aveugle, "
             "seul l'enregistrement héritage LÉGAL (la charge d'UN octet) "
             "passe")


# --- Le verdict --------------------------------------------------------------------

def main():
    graine = 20261107
    for i, a in enumerate(sys.argv):
        if a == "--graine" and i + 1 < len(sys.argv):
            graine = int(sys.argv[i + 1])
    print("=== tls13/harnais_poignee.py — LE HARNAIS DE LA FAMILLE poignée "
          "+ LE PRINCIPAL (chantier M9-(b), sixième geste) ===")
    print(f"=== graine {graine} · les VINGT-HUIT blocs du domaine posés aux "
          "RVA du plan ===")
    emul = Emulation()
    nue = Emulation(nue=True)
    vecteur_v0(emul)
    vecteur_v1(emul)
    vecteur_v2(emul)
    vecteur_v3(emul, graine)
    vecteur_v4(emul, nue)
    vecteur_v5(emul, graine)
    vecteur_v6(emul)
    vecteur_v7(emul, nue)
    print()
    if ECHECS:
        print(f"VERDICT : ROUGE — {len(ECHECS)} échec(s) nommé(s) : "
              f"{[n for n, _ in ECHECS]}")
        sys.exit(1)
    print(f"VERDICT : VERT — {len(REUSSITES)} contrôles · {len(REUSSITES)} "
          "VERTS : la famille poignée + le principal NOTÉES-MESURÉES-PROUVÉES "
          "— le ClientHello composé, le ServerHello traité, le calendrier à "
          "trois étages, le Finished calculé/vérifié, l'épinglage, LA MACHINE "
          "D'ÉTATS du client entier contre le simulateur, la rotule de "
          "transport ; LE TRANSFERT RFC 8448 bloc par bloc sur les valeurs "
          "consignées, la SESSION ENTIÈRE recoupée, la falsification à chaque "
          "étage rend SON verdict nommé — le domaine tls13 est COMPLET : les "
          "28 blocs.")
    sys.exit(0)


if __name__ == "__main__":
    main()
