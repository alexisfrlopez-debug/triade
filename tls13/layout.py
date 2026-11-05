#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tls13/layout.py — LE PLAN D'ADRESSAGE DU DOMAINE tls13 (M9, l'ère 1.0.0).

La source unique des constantes du domaine (le modèle m8/layout.py, D161) :
la suite arrêtée, la table des verdicts, les versions de l'ère, les
constantes publiques des SIX familles et la PRÉFIGURATION .text6.

LA PRÉFIGURATION N'EST PAS UN DROIT (D161, la leçon de M8-(b)) : les RVA et
tailles définitifs des blocs seront ARRÊTÉS au chantier de la notation sur
les LONGUEURS RÉELLES mesurées (auteur.py décide, la préfiguration s'incline)
; seuls les constantes immuables (les valeurs de spécification) et les bornes
d'héritage (le scellé 0.9.0, R7) sont ARRÊTÉS ici.
"""

# --- La suite arrêtée (charte § 1 : une constante, jamais une négociation) ------

SUITE = 0x1301                     # TLS_AES_128_GCM_SHA256 (RFC 8446 §9.1)
GROUPE = 0x001D                    # x25519 (RFC 7748)
PREFIXE_ETIQUETTE = b"tls13 "      # RFC 8446 §7.1 (le NUL de terminaison

# --- Les versions de l'ère (le miroir m8 : 0x00090001 = 0.9.0-dev.1) ----------

VERSION_DEV = 0x01000001           # 1.0.0-dev.1 (geste de BUILD, jamais scellage)
VERSION_FINALE = 0x01000000        # 1.0.0 (le scellage est un fait de carte, D165)

# --- La table des SEPT verdicts du domaine (charte § 5 : l'échec nommé) --------

VERDICTS = {
    0: "OK",
    -1: "argument invalide",
    -2: "taille ou longueur invalide",
    -3: "état du domaine invalide (contexte non initialisé / calendrier divergent)",
    -4: "cryptographie divergente (étiquette AEAD, Finished) — fail-closed",
    -5: "négociation refusée (le ServerHello diverge de la suite proposée)",
    -6: "épinglage divergent (l'empreinte du certificat ≠ l'attendue)",
    -7: "transport en échec (le socle sys a rendu un NTSTATUS non nul)",
}

# --- Les constantes publiques de la famille sha (tls13-01..04) -----------------

SHA_H0 = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
          0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)   # FIPS 180-4 §5.3.1
SHA_TAILLE_BLOC = 64
SHA_TAILLE_CONDENSE = 32
SHA_CTX = 112          # H[8]u32 @+0 · tampon[64] @+32 · remplissage @+96 ·
                       # réservé @+100 · total u64 @+104 (la disposition ah)

# --- Les constantes publiques de la famille hkdf (tls13-05..08) -----------------

HMAC_IPAD = 0x36                          # RFC 2104 §2 (le masque intérieur)
HMAC_OPAD = 0x5C                          # RFC 2104 §2 (le masque extérieur)
HMAC_BLOC = SHA_TAILLE_BLOC               # 64 o : la clé expulsée au bloc
HKDF_MAX_L = 8160                         # 255 × 32 : la borne RFC 5869 §2.3

# --- Les constantes publiques de la famille x25519 (tls13-09..14) ---------------

F25519_M51 = 0x7FFFFFFFFFFFF              # le masque de membre (2^51 − 1)
F25519_P_MEMBRES = (0x7FFFFFFFFFFED,) + (0x7FFFFFFFFFFFF,) * 4
                                          # p = 2^255 − 19 en radix 2^51 :
                                          # (2^51 − 19) puis (2^51 − 1)×4 —
                                          # DÉRIVÉ PAR ARITHMÉTIQUE (av-10 I2
                                          # cité ; erratum M9 : jamais copié)
F25519_REPLI = 19                         # 2^255 ≡ 19 (mod p)
X25519_A24 = 121665                       # (486662 − 2) / 4 — RFC 7748 §5
X25519_BASE = 9                           # le point de base u = 9, RFC 7748 §6.1
X25519_EXP_INV = bytes.fromhex(
    "eb" + "ff" * 30 + "7f")              # p − 2, 32 o little-endian (l'exposant
                                          # d'inversion de tls13-13 I4 — PUBLIC)

# --- Les constantes publiques de la famille aead (tls13-15..19) ------------------

AES_CLE = 16                              # la clé AES-128
AES_CLES_TOUR = 176                       # 11 clés × 16 o (FIPS 197 §5.2)
GCM_NONCE = 12                            # le IV du protocole, RFC 8446 §5.3
GCM_ETIQUETTE = 16                        # l'étiquette AEAD
GCM_R = bytes.fromhex("e1" + "00" * 15)   # SP 800-38D §6.3 (la constante de repli)

# --- Les constantes publiques de la famille enregistrement (tls13-20..21) --------

TYPE_POIGNEE = 22                         # les types de contenu, RFC 8446 §5.1
TYPE_ALERTE = 21
TYPE_APPDATA = 23                         # le protégé est TOUJOURS opaque 23
VERSION_HERITAGE = 0x0303                 # l'enregistrement et le ClientHello
CHARGE_MAX = 1 << 14                      # RFC 8446 §5.1 : TLSPlaintext.length
ENREGISTREMENT_CTX = 200                  # clés @+0 (176) · IV @+176 (12) ·
                                          # réserve @+188 (4) · séquence u64 @+192
ALERTE_CLOSE_NOTIFY = b"\x01\x00"         # WARNING · close_notify, RFC 8446 §6.1

# --- Les constantes publiques de la famille poignée (tls13-22..26) ---------------

EXT_SUPPORTED_VERSIONS = 0x002B           # les extensions proposées, RFC 8446 §4.2
EXT_SUPPORTED_GROUPS = 0x000A
EXT_SIG_ALGS = 0x000D
EXT_KEY_SHARE = 0x0033
VERSION_TLS13 = 0x0304                    # supported_versions, RFC 8446 §4.2.1
SIG_ALGOS = (0x0804, 0x0401)              # rsa_pss_rsae_sha256, rsa_pkcs1_sha256
CLIENTHELLO_TAILLE = 114                  # la construction FIXE (tls13-22 Q1)
SERVERHELLO_MIN = 90                      # le message minimal attendu (tls13-23 P1)
HRR_MAGIQUE = bytes.fromhex(
    "cf21ad74e59a6111be1d8c021e65b891"
    "c2a211167abb8c5e079e09e2c8a8339c")   # SHA-256("HelloRetryRequest") —
                                          # RFC 8446 §4.1.3 (la valeur magique)
CALENDRIER_CTX = 48                       # secret 32 @+0 · étape u32 @+32 · réserve
SESSION_TAILLE = 17520                    # la disposition de tls13-27 P1
SESSION_POIGNEE_MAX = 1 << 14             # la borne de réassemblage (nommée)
LIBELLES = {                              # RFC 8446 §7.1 — données PUBLIQUES
    "derived": b"derived",
    "c hs traffic": b"c hs traffic",
    "s hs traffic": b"s hs traffic",
    "c ap traffic": b"c ap traffic",
    "s ap traffic": b"s ap traffic",
    "key": b"key",
    "iv": b"iv",
    "finished": b"finished",
}

# --- La borne d'héritage (le scellé 0.9.0 — R7, ne bouge jamais) ---------------

TEXT5_RAW_M8 = 0xAE00             # la fin du fichier m8/proxy.exe scellé
TAILLE_FICHIER_M8 = 0xAE00        # 44 544 o (l'ancre : le corps hérité)

# --- La PRÉFIGURATION .text6 (ARRÊT à la notation — D161) ----------------------

# La 8e section suit .text5 : raw 0xAE00, RVA 0xC000 (SizeOfImage 0xC000 du
# scellé 0.9.0 → la nouvelle image s'étend, la marge d'en-têtes 0x400 reçoit
# le HUITIÈME en-tête — le constat s'y refera au chantier du build, le
# décalage de packaging D94 n'est pas rejoué).
TEXT6_RAW = TEXT5_RAW_M8          # préfiguration : la mesure décidera
TEXT6_VA = 0xC000                 # préfiguration : aligné SectionAlignment

# --- La famille sha ARRÊTÉE (chantier (b), le 05/11 — D161 rejoué) ---------------
# Les slots ARRÊTÉS sur les longueurs réelles MESURÉES par outils/auteur.py
# (la mesure auteur décide, la préfiguration 0x200/bloc s'incline) : multiples
# de 64 (D8), tassés depuis TEXT6_VA, padding >= 16 — le MINIMUM admissible
# pour chaque longueur mesurée :
#   tls13-01 : 74 o notés  -> slot 0x80  (padding 54)
#   tls13-02 : 387 o notés -> slot 0x1C0 (padding 61)
#   tls13-03 : 139 o notés -> slot 0xC0  (padding 53)
#   tls13-04 : 165 o notés -> slot 0xC0  (padding 27)
# Les familles suivantes (x25519, aead, enregistrement, poignée,
# principal) s'arrêteront au geste de LEUR notation, chacune à la suite.

TLS01_VA = 0xC000        # h100001 — l'initialisation (slot 0x80)
TLS02_VA = 0xC080        # h100002 — la compression (slot 0x1C0)
TLS03_VA = 0xC240        # h100003 — l'absorption (slot 0xC0)
TLS04_VA = 0xC300        # h100004 — la finalisation (slot 0xC0)
# fin de la famille sha : 0xC3C0 — la famille hkdf suit à la contiguïté

# --- La famille hkdf ARRÊTÉE (chantier (b), la suite — D161 rejoué) ---------------
# MÊME ARRÊT sur les longueurs réelles MESURÉES par outils/auteur.py (la mesure
# auteur décide) : multiples de 64 (D8), tassés depuis la fin sha (0xC3C0),
# padding >= 16 — le MINIMUM admissible pour chaque longueur mesurée :
#   tls13-05 : 435 o notés -> slot 0x200 (padding 77)
#   tls13-06 : 151 o notés -> slot 0xC0  (padding 41)
#   tls13-07 : 347 o notés -> slot 0x180 (padding 37)
#   tls13-08 : 310 o notés -> slot 0x180 (padding 74)
TLS05_VA = 0xC3C0        # h100005 — HMAC-SHA-256 (slot 0x200)
TLS06_VA = 0xC5C0        # h100006 — HKDF-Extract (slot 0xC0)
TLS07_VA = 0xC680        # h100007 — HKDF-Expand (slot 0x180)
TLS08_VA = 0xC800        # h100008 — HKDF-Expand-Label (slot 0x180)
# fin de la famille hkdf : 0xC980 — les familles suivantes suivent

SLOTS_TLS13 = {
    "h100001": (TLS01_VA, 0x80),
    "h100002": (TLS02_VA, 0x1C0),
    "h100003": (TLS03_VA, 0xC0),
    "h100004": (TLS04_VA, 0xC0),
    "h100005": (TLS05_VA, 0x200),
    "h100006": (TLS06_VA, 0xC0),
    "h100007": (TLS07_VA, 0x180),
    "h100008": (TLS08_VA, 0x180),
}

# --- Le fixture K[64] : la réserve M8 exactement remplie (vérifiée sur pièces) ---
# La zone RVA 0x2F00-0x2FFF (raw 0x2300) est VIERGE dans le scellé 0.9.0 —
# 256 octets nuls constatés sur pièces au chantier (b) (m8/proxy.exe relu :
# sha256 1492b0bc…, .rdata RVA 0x2000 raw 0x1400, la borne de marche M8
# R_SYS_BORNE = 0x2F00). K[64] u32 = 256 o : la réserve est ÉPUISÉE par la
# table — le prochain fixture du domaine vivra en .text6 (l'arrêt nommé,
# miroir D95 : jamais au-delà d'une borne sans arrêt consigné).

R_K = 0x2F00             # K[64] u32 — FIPS 180-4 § 4.2.2 (la table de tls13-02)

# Les constantes FIPS 180-4 § 4.2.2 : parties fractionnaires des racines
# cubiques des 64 premiers nombres premiers — DÉRIVÉES PAR ARITHMÉTIQUE à
# l'instrument du chantier (b) (racine cubique entière de p × 2^96 ; le juge
# est le code, jamais une copie d'écriture).
K = (
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
    0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
    0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
    0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
    0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
)

# --- Les décalages du contexte SHA (la disposition ah — miroir M6, charte § 6) ---

CTX_H = 0                 # H[8] u32 — l'état du hachage
CTX_TAMPON = 32           # tampon[64] — le couplage partiel
CTX_REMPLISSAGE = 96      # u32 — octets valides du tampon
CTX_RESERVE = 100         # u32 — l'alignement (jamais lu)
CTX_TOTAL = 104           # u64 — octets absorbés cumulés

# --- Les adresses de blocs (les appels directs inter-blocs — I1 des specs) -------

A_INIT = TLS01_VA          # tls13-01 (l'initialisation)
A_COMPRIMER = TLS02_VA     # tls13-02 (la compression — appelée par 03 et 04)
A_ABSORBER = TLS03_VA      # tls13-03 (l'absorption)
A_FINALISER = TLS04_VA     # tls13-04 (la finalisation)
A_HMAC = TLS05_VA          # tls13-05 (l'HMAC — appelée par 06, 07 et 25)
A_EXTRACT = TLS06_VA       # tls13-06 (l'extraction)
A_EXPAND = TLS07_VA        # tls13-07 (l'expansion — appelée par 08)
A_EXPAND_LABEL = TLS08_VA  # tls13-08 (l'étiquette — LE bloc du calendrier)
