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

# Les slots des 28 blocs : PRÉFIGURÉS en tassé depuis TEXT6_VA (D8 : multiples
# de 64, alignés 16, padding >= 16) — ARRÊTÉS à la notation sur les longueurs
# réelles (D161 : sys-01 fut préfiguré 0x40 et le resta ; sys-02 0x140 → 0x140
# ; la préfiguration s'incline devant la mesure, TOUJOURS).
TAILLE_SLOT_PREFIGUREE = 0x200    # par bloc, préfiguration généreuse
