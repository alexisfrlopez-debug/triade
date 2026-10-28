"""layout.py — Plan d'adressage du projet TRIADE, jalon M4 (profil x86-64-win11-pe).

Source unique de vérité partagée par build_m4.py, outils/auteur.py et
oracle_m4.py. Toute adresse du futur proxy.exe 0.5.0-dev dérive d'ici ; la
notation référence ces constantes et le builder vérifie la concordance.

HÉRITAGE M0/M1/M2/M3 (R7 — jamais déplacé) :
  - blocs scellés io @ 0x1040/0x1080 et libc @ 0x1100-0x13FF ;
  - blocs réseau M2 @ leurs RVA exacts (tcp-01 0x4000, tcp-02 0x4100,
    tcp-03 0x4140, tcp-04 0x4180, tcp-05 0x41C0, tcp-06 0x4300,
    tcp-11 0x4B00) ;
  - tcp-13 @ 0x4400 (zone tramp M2 réaffectée, D47) ;
  - zone http @ .text2 : http-01 0x4C00, http-02 0x4C80, http-03 0x4E80,
    http-04 0x4F40, http-05 0x5080, http-06 0x5140, http-07 0x5200,
    http-08 0x5380, http-09 0x54C0, http-10 0x5580, http-11 0x5D80 ;
    http-12 @ .text 0x1800 (orchestrateur, entrée du programme) ;
  - .text2 est COMPLÈTE (0x4000-0x5FFF) : l'extension M4 vit dans une
    section NOUVELLE .text3 — la zone http scellée 0.4.0 ne bouge pas d'un
    octet (§ 9) et les DEUX blocs révisés (http-08:R2, http-10:R2) vivent
    AUSSI en .text3 : leurs ancêtres restent indexés par la carte
    génération 5, les révisions citent (m4/I/README, D77).

ARRÊT PARTIEL étape b (D79 — mesure auteur, trois feuilles pures) :
  tls-01 0x6000 (0x80), tls-02 0x6080 (0x100), tls-03 0x6180 (0x140) —
  slots réarrêtés sur les longueurs réelles des notations (règles D8 :
  multiples de 64, alignés 16, padding >= 16). Les CINQ blocs suivants
  (tls-04..08) et les DEUX révisions restent PRÉFIGURÉS : leurs slots
  seront réarrêtés quand leurs notations existeront (fin d'étape b).

EXTENSION M4 (D77, génération 6 — blocs g7xxxx) :
  - .text3 démarre à 0x6000 (alignement section) : tls-01 0x6000,
    tls-02 0x6080, tls-03 0x6180 ; préfiguration : tls-04 0x62C0,
    tls-05 0x65C0, tls-06 0x6740, tls-07 0x6A40, tls-08 0x6D40,
    http-08:R2 0x7340, http-10:R2 0x7480 ;
  - l'IAT secur32 gagne SEPT entrées appendues (D77) : AcquireCredentials-
    HandleW, FreeCredentialsHandle, InitializeSecurityContextW, Delete-
    SecurityContext, QueryContextAttributesW, EncryptMessage, DecryptMessage
    — les emplacements .rdata exacts seront arrêtés au build (extension
    de la zone d'imports après les fixtures http scellées) ;
  - état .data identique à M3 (la session TLS vivra dans le cadre alloué
    par http-10:R2 — propriétaire unique, charte § 6).

Constantes à propriétaire unique (charte m4/I, § 8) :
  MAX_JETON = 16384 (tls-03 ; TLS 1.3 enchaîne certificats + fin
  d'extension sur ~ 16 Kio) ; HOTE_MAX = 255 (hérité tcp-13, borne
  tls-01) ; MAX_MESSAGE est la valeur NÉGOCIÉE (tls-06 la lit dans les
  tailles de flux — jamais une constante ici).

Liste blanche HRESULT tls-02 (winerror.h, vérifiée à la source D79 —
trois valeurs corrigées par la vérification : DECRYPT_FAILURE 0x80090330
[0x80090321 = BUFFER_TOO_SMALL], CONTEXT_EXPIRED 0x00090317,
CERT_WRONG_USAGE 0x80090349) :
  SEC_E_OK                0x00000000  verdict 0 succès
  SEC_I_CONTINUE_NEEDED   0x00090312  verdict 1 continuer
  SEC_E_INCOMPLETE_MESSAGE 0x80090318 verdict 2 message incomplet
  SEC_E_UNTRUSTED_ROOT    0x80090325  verdict 3 certificat invalide
  SEC_E_CERT_EXPIRED      0x80090328  verdict 3
  SEC_E_CERT_UNKNOWN      0x80090327  verdict 3
  SEC_E_CERT_WRONG_USAGE  0x80090349  verdict 3
  SEC_E_WRONG_PRINCIPAL   0x80090322  verdict 3
  SEC_I_CONTEXT_EXPIRED   0x00090317  verdict 4 fin de contexte
  SEC_E_INVALID_TOKEN     0x80090308  verdict 5 échec négocié
  SEC_E_DECRYPT_FAILURE   0x80090330  verdict 5
  SEC_E_MESSAGE_ALTERED   0x8009030F  verdict 5
  SEC_E_OUT_OF_SEQUENCE   0x80090310  verdict 5
  toute autre valeur                  verdict 6 fatal inconnu
Constantes SSPI tls-03 (sspi.h) : SECBUFFER_VERSION 0 ; SECBUFFER_DATA 1 ;
SECBUFFER_TOKEN 2 ; SECBUFFER_STREAM_TRAILER 6 ; SECBUFFER_STREAM_HEADER 7 ;
SecBuffer { ULONG cbBuffer ; ULONG BufferType ; void* pvBuffer } (16 o x64) ;
SecBufferDesc { ULONG ulVersion ; ULONG cBuffers ; void* pBuffers } (16 o) ;
SecPkgContext_StreamSizes { cbHeader, cbTrailer, cbMaximumMessage,
cBuffers, cbBlockSize } (5 ULONG : en-tête +0, queue +4, message max +8 —
tls-06, unique propriétaire de l'acquisition).
"""

import importlib.util
import os

# Le plan M3 se charge sous un nom distinct ("layout_m3") : les fichiers
# s'appellent tous layout.py — l'import classique serait circulaire.
_CHEMIN_M3 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "m3", "layout.py")
_spec = importlib.util.spec_from_file_location("layout_m3", _CHEMIN_M3)
L3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L3)   # noqa: E402 — plan M3 (héritage)

# --- Image et sections --------------------------------------------------------

IMAGE_BASE = L3.IMAGE_BASE
TEXT_RVA, RDATA_RVA, DATA_RVA = L3.TEXT_RVA, L3.RDATA_RVA, L3.DATA_RVA
TEXT2_RVA = L3.TEXT2_RVA                      # 0x4000
TEXT3_RVA = 0x6000                            # NOUVELLE section M4 (D77)
FILE_ALIGN, SECT_ALIGN = L3.FILE_ALIGN, L3.SECT_ALIGN
TEXT_VSIZE, RDATA_VSIZE, DATA_VSIZE = L3.TEXT_VSIZE, L3.RDATA_VSIZE, L3.DATA_VSIZE
TEXT2_VSIZE = L3.TEXT2_VSIZE                  # 0x2000 — complète
TEXT3_VSIZE = 0x2000                          # 0x6000-0x7FFF (préfiguration,
                                              # réarrêt à la fin d'étape b)
SIZE_OF_IMAGE = 0x8000
TEXT_FILE, RDATA_FILE, DATA_FILE, TEXT2_FILE = (
    L3.TEXT_FILE, L3.RDATA_FILE, L3.DATA_FILE, L3.TEXT2_FILE)
TEXT3_FILE = 0x4E00                           # après .text2 (0x2C00+0x2000)
DATA_RAW = L3.DATA_RAW                        # .data committée (état serveur)
TAILLE_FICHIER = 0x6E00                       # 0x4E00 + 0x2000 (préfiguration)

DLL_CHARACTERISTICS = L3.DLL_CHARACTERISTICS  # DYNAMICBASE | HEVA | NX

VERSION_DEV1 = "0.5.0-dev.1"   # tunnel chiffré : 8 blocs tls + 2 révisions http
VERSION_U64_DEV1 = 0x00050001  # R10 : monotonie (plancher 0.4.0 = 0x00040000)
VERSION_U64_MIN = 0x00040000   # accepté par la porte R10 (http-12:Q1 scellé)

# --- Blocs embarqués dans proxy.exe M4 (couche C, génération 6) ---------------
# g7xxxx = M4. Les trois premières feuilles pures sont ARRÊTÉES sur mesure
# (D79) ; la suite est PRÉFIGURÉE (réarrêt à la fin d'étape b).

BLOCS_TLS = [
    ("g70001", "tls-01:R1", 0x6000, 0x80, "M4-dev.1", 1),    # hôte → UTF-16
    ("g70002", "tls-02:R1", 0x6080, 0x100, "M4-dev.1", 1),   # verdicts SSPI
    ("g70003", "tls-03:R1", 0x6180, 0x140, "M4-dev.1", 1),   # jetons (descripteurs)
    ("g70004", "tls-04:R1", 0x62C0, 0x300, "M4-dev.1", 0),   # poignée de main (préfig.)
    ("g70005", "tls-05:R1", 0x65C0, 0x180, "M4-dev.1", 0),   # cycle de vie (préfig.)
    ("g70006", "tls-06:R1", 0x6740, 0x300, "M4-dev.1", 0),   # émission (préfig.)
    ("g70007", "tls-07:R1", 0x6A40, 0x300, "M4-dev.1", 0),   # réception (préfig.)
    ("g70008", "tls-08:R1", 0x6D40, 0x600, "M4-dev.1", 0),   # session TLS (préfig.)
]
BLOCS_REVISIONS = [
    ("g70009", "http-08:R2", 0x7340, 0x180, "M4-dev.1", 0),  # cible https (préfig.)
    ("g70010", "http-10:R2", 0x74C0, 0x900, "M4-dev.1", 0),  # session + routage (préfig.)
]
# L'héritage M3 complet (io, libc, tcp, http-01..07, 09, 11, 12) est repris
# OCTET POUR OCTET (R7) depuis le plan M3 — le build_m4 le lira via L3.

ENTREE = L3.ENTREE                            # 0x1800 — http-12 (R7, inchangé)

NOMS_BLOCS = dict(L3.NOMS_BLOCS) | {
    "g70001": "tls-utf16", "g70002": "tls-verdicts", "g70003": "tls-jetons",
    "g70004": "tls-poignee", "g70005": "tls-cles", "g70006": "tls-emission",
    "g70007": "tls-reception", "g70008": "tls-session",
    "g70009": "http-cible-r2", "g70010": "http-session-r2",
}

# --- .text3 : zones ------------------------------------------------------------

ZONE_TLS_FEUILLES = (0x6000, 0x641F)   # tls-01..03 (arrêtées D79, mesure auteur)
ZONE_TLS_SUITE = (0x6420, 0x733F)      # tls-04..08 (préfiguration — réarrêt b)
ZONE_REVISIONS = (0x7340, 0x7DFF)      # http-08:R2, http-10:R2 (préfiguration)
ZONE_RESERVEE_T3 = (0x7E00, 0x7FFF)    # int3 — extension future (M5 : patch à
                                       # chaud le réutilisera peut-être)

# --- IAT secur32 : SEPT entrées appendues (D77 — emplacements au build) --------

SECUR32_IMPORTS = [
    "AcquireCredentialsHandleW", "FreeCredentialsHandle",
    "InitializeSecurityContextW", "DeleteSecurityContext",
    "QueryContextAttributesW", "EncryptMessage", "DecryptMessage",
]
# Les RVA .rdata des slots (R_IAT_SECUR32…) et les hint/names seront arrêtés
# au build (extension de la zone d'imports après les fixtures http scellées —
# la concordance IAT ↔ notation sera vérifiée comme en M3).

# --- Constantes à propriétaire unique (charte m4/I § 8) -------------------------

MAX_JETON = 16384               # tls-03 (type 0) : borne des jetons de poignée
HOTE_MAX = L3.HOTE_MAX          # 255 — tls-01 (héritage tcp-13)
# MAX_MESSAGE : JAMAIS une constante — valeur négociée, lue dans les tailles
# de flux ([tailles + 8], acquises par tls-06 — charte § 6/§ 8)

# --- Liste blanche HRESULT tls-02 (winerror.h, vérifiée D79) --------------------

HRESULTS = {
    0x00000000: 0,   # SEC_E_OK — succès
    0x00090312: 1,   # SEC_I_CONTINUE_NEEDED — continuer
    0x80090318: 2,   # SEC_E_INCOMPLETE_MESSAGE — message incomplet
    0x80090325: 3,   # SEC_E_UNTRUSTED_ROOT — certificat invalide
    0x80090328: 3,   # SEC_E_CERT_EXPIRED
    0x80090327: 3,   # SEC_E_CERT_UNKNOWN
    0x80090349: 3,   # SEC_E_CERT_WRONG_USAGE
    0x80090322: 3,   # SEC_E_WRONG_PRINCIPAL
    0x00090317: 4,   # SEC_I_CONTEXT_EXPIRED — fin de contexte
    0x80090308: 5,   # SEC_E_INVALID_TOKEN — échec négocié
    0x80090330: 5,   # SEC_E_DECRYPT_FAILURE
    0x8009030F: 5,   # SEC_E_MESSAGE_ALTERED
    0x80090310: 5,   # SEC_E_OUT_OF_SEQUENCE
}
VERDICT_FATAL = 6               # toute autre valeur (table TOTALE)

# --- Constantes SSPI tls-03 (sspi.h) --------------------------------------------

SECBUFFER_VERSION = 0
SECBUFFER_EMPTY, SECBUFFER_DATA, SECBUFFER_TOKEN = 0, 1, 2
SECBUFFER_STREAM_TRAILER, SECBUFFER_STREAM_HEADER = 6, 7
TAILLE_SECBUFFER = 16           # { u32 cb, u32 type, u64 pv } — x64
TAILLE_SECBUFFERDESC = 16       # { u32 version, u32 count, u64 pBuffers }
CAPACITE_CADRE_MIN = 16 + 4 * 16   # descripteur le plus large (type 2) = 80 o

# --- Jetons de retour d'émulation (oracle, hors binaire) ------------------------

SENTINELLE_RETOUR = L3.SENTINELLE_RETOUR

# --- Réexports de l'héritage M3 (le plan M4 est la source unique pour ses outils) -

IAT_SLOTS = L3.IAT_SLOTS            # kernel32 + ws2_32 (R7 — scellé 0.4.0)
R_TAB_METHODES = L3.R_TAB_METHODES
R_METHODES = L3.R_METHODES
R_SLASH = L3.R_SLASH
R_TAB_REPONSES = L3.R_TAB_REPONSES
R_TXT_400, R_TXT_431 = L3.R_TXT_400, L3.R_TXT_431
R_TXT_501, R_TXT_411 = L3.R_TXT_501, L3.R_TXT_411
R_TXT_505, R_TXT_502 = L3.R_TXT_505, L3.R_TXT_502
R_TXT_TUNNEL = L3.R_TXT_TUNNEL
R_TAB_SUM, R_VERSION, R_ANCRE = L3.R_TAB_SUM, L3.R_VERSION, L3.R_ANCRE
R_RELOC = L3.R_RELOC
R_MSG_BANNIERE = L3.R_MSG_BANNIERE
R_MSG_CONNEXION = L3.R_MSG_CONNEXION
R_MSG_TUNNEL, R_MSG_FIN = L3.R_MSG_TUNNEL, L3.R_MSG_FIN
R_MSG_ARRET, R_MSG_INCONNU = L3.R_MSG_ARRET, L3.R_MSG_INCONNU
R_MSG_ERREUR, R_MSG_KO = L3.R_MSG_ERREUR, L3.R_MSG_KO
R_CMD_QUIT, R_NOM_HOST = L3.R_CMD_QUIT, L3.R_NOM_HOST
R_NOM_CL, R_NOM_TE = L3.R_NOM_CL, L3.R_NOM_TE
R_STDOUT, R_STDIN = L3.R_STDOUT, L3.R_STDIN
R_LISTEN, R_QUIT, R_CS = L3.R_LISTEN, L3.R_QUIT, L3.R_CS
R_CURSEUR, ARENA_BASE = L3.R_CURSEUR, L3.ARENE_BASE
BANNIERE, PORT_ECOUTE = L3.BANNIERE, L3.PORT_ECOUTE
