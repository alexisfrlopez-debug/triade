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
  multiples de 64, alignés 16, padding >= 16). ARRÊT D81 : tls-05 0x65C0
  (0x180, mesure auteur — cycle de vie des handles, premier bloc à shims).
  Mesures suivies, slots préfigurés CONSERVÉS (padding >= 16, D8 — les
  adresses préfigurées aval restent exactes) : tls-04 0x62C0 (0x300, 544 o,
  D83 — la poignée de main), tls-06 0x6740 (0x300, 491 o, D88 — l'émission),
  tls-07 0x6A40 (0x300, 394 o, D89 — la réception), tls-08 0x6D40 (0x600,
  740 o, D90 — la session : orchestration complète + compensation intégrale).
  Restent préfigurés : http-08:R2 0x7340 (0x180), http-10:R2 0x74C0
  (0x900 — réarrêt éventuel à leurs mesures, fin d'étape b ; l'adresse
  préfigurée D77 0x7480 datait du slot 0x140 avant élargissement du slot
  http-08:R2 à 0x180, corrigée D91).

EXTENSION M4 (D77, génération 6 — blocs g7xxxx) :
  - .text3 démarre à 0x6000 (alignement section) : tls-01 0x6000,
    tls-02 0x6080, tls-03 0x6180 ; arrêts D79/D81 : tls-05 0x65C0 ;
    préfiguration : tls-04 0x62C0, tls-06 0x6740, tls-07 0x6A40,
    tls-08 0x6D40 (mesuré D90), http-08:R2 0x7340 (0x180), http-10:R2
    0x74C0 (0x900, corrigé D91 — cf. ci-dessus) ;
  - l'IAT secur32 gagne SEPT entrées (D77) : AcquireCredentials-
    HandleW, FreeCredentialsHandle, InitializeSecurityContextW, Delete-
    SecurityContext, QueryContextAttributesW, EncryptMessage, DecryptMessage
    — emplacements .rdata ARRÊTÉS D81 dans l'extension de la zone d'imports
    (après les fixtures http scellées, voir R_IAT_SEC32 ci-dessous — le build
    émettra descripteurs/INT/hints à ces adresses exactes, concordance
    IAT ↔ notation vérifiée comme en M3) ;
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
Règles DecryptMessage (D89 — contrat de la « bibliothèque », partagé modèle/
émulation du harnais tls-07, jamais deux sources de vérité) : en succès le
tampon 0 devient (cb = longueur claire, DATA, pv = zone + en-tête — le clair
remplace le brut à l'offset de l'en-tête d'enregistrement) ; le tampon 1
devient (cb = résidu Extra, EXTRA, pv = zone + consommé) ; en message
incomplet le tampon 0 devient (cb = octets manquants, MISSING) SANS toucher
la zone ; tout autre verdict n'écrit rien.

CADRE DE SESSION TLS (arrêt D81, AMENDÉ D89 — convention partagée tls-04..08, citée
par les spécifications « aux offsets documentés » ; propriété mémoire http-10:R2
qui le fournit VIERGE ; zone de travail complete, jamais de donnée statique) :
  +0x00 CredHandle credentials { u64 dwLower, u64 dwUpper }   (16 o, tls-05)
  +0x10 CtxtHandle contexte    { u64 dwLower, u64 dwUpper }   (16 o, tls-04
         écrit à l'établissement / tls-05 op 1 détruit+remet à zéro)
  +0x20 socket serveur TLS (u64 — tcp-13 via tls-08, fermée par tls-08 SEUL)
  +0x28 pointeur nom UTF-16 (u64 — vise CADRE_NOM_ZONE ; tls-01 destination)
  +0x30 verdict poignée (u32 — tls-04:Q2) ; +0x34 HRESULT d'origine (u32,
         tls-02:Q2 — jamais un HRESULT brut sans verdict nommé à côté)
  +0x38 allers-retours (u16 — tls-04:Q1)
  +0x3A longueur utile réception (u16 — D89, tls-07 UNIQUE propriétaire : la
         longueur de la région vivante de la zone — résidu Extra + octets
         reçus depuis le dernier appel ; l'appelant tls-08 réceptionne
         PAR-DESSUS, à zone+offset+longueur, jamais ailleurs)
  +0x3C offset résidu (u16 — D89, tls-07 : où la région vivante COMMENCE ;
         tls-07 normalise à 0 au DéBUT de chaque appel — le clair pompé par
         l'appelant depuis l'appel précédent est de la mémoire morte, le
         résidu descend en tête par libc-01 AVANT le déchiffrement ; c'est
         la lecture géométrique de tls-07:Q1 « il sera écrasé » : l'écrase-
         ment est l'œuvre de l'appel SUIVANT, d'où « pompe AVANT tout nouvel
         appel »). Cadre vierge : (0, 0) — tls-08 initialise depuis l'état
         final de tls-04 à l'entrée du relais.
  +0x40 tailles de flux StreamSizes (5 x u32, 20 o — tls-06 écrit UNE fois
         par session, tls-03 type 1 lit via le pointeur passé en 5e argument)
  +0x60 zone nom UTF-16 (512 o = 2 x (HOTE_MAX + 1))
  +0x260 zone jeton ÉMISSION (MAX_JETON 16384 — poignée puis enregistrements)
  +0x4260 zone RÉCEPTION (2 x MAX_JETON 32768 — D89 : tls-07:R1 P1/E2, le
         résidu Extra suivi des octets bruts récents ; tls-04 y voit une zone
         ≥ MAX_JETON — ses gardes restent au bornage JETON, inchangées)
  TAILLE_CADRE = 0xC260 (49760 o — 0x8260 avant D89)

.rdata M4 — extension de la zone d'imports ARRÊTÉE D81 (après les fixtures
http scellées qui finissent à 0x299C ; tout l'héritage M3 reste octet pour
octet à ses adresses — R7) :
  0x29A0 table des descripteurs M4 (4 x 20 o : kernel32 FT 0x20B0,
         ws2_32 FT 0x2300, secur32 FT 0x2A00, terminateur) — le répertoire
         d'imports du PE M4 pointera ICI (les 60 o M3 à 0x2030-0x206B
         restent en place, R7 : espace mort lu par personne, le chargeur
         suit le répertoire) ;
  0x29F0 "secur32.dll\0" (12 o) ;
  0x2A00 IAT secur32 : 7 slots + terminateur (0x2A38) ;
  0x2A40 INT secur32 : 7 entrées + terminateur (0x2A78) ;
  0x2A80 hints/names secur32 (7 entrées, se termine 0x2B2A, pad 0x2B30) ;
  0x2C00 fixture tls-05 : L"Microsoft Unified Security Protocol Provider"
         + mot NUL (44 + 1 wchar = 90 o) — pszPackage, unique propriétaire.
  0x2C60 fixture tls-08 (D90) : "tunnel chiffre etabli\r\n" (23 o) — ligne
         console tcp-11 de l'état nommé Q1 (émission APRÈS poignée réussie,
         AVANT la requête — AUCUN secret, charte § 3).
  0x2C80 fixture tls-08 (D90) : "certificat rejete\r\n" (19 o) — ligne
         console tcp-11 du verdict 3 de tls-04 (I4 — LE critère M4 : cet
         endroit précis ; la réponse 502 est émise par http-10:R2 au retour).
  0x2CA0 fixture http-10:R2 (D92) : "HTTP/1.1 502 Certificat rejete\r\n\r\n"
         (34 o) — l'entrée ÉTIQUETÉE de la table des réponses (Q3' : le
         certificat invalide est le seul échec du tunnel DISTINGUABLE côté
         client — terrain § 8.4) ; les autres verdicts de tls-08 (2/4/5/6/7)
         mappent sur la ligne 502 R1 scellée (txt_502 @0x2614, R7) ; la table
         R1 de 7 entrées @0x24E0 reste OCTET POUR OCTET (R7) — la concordance
         M4 vérifiera la 8e entrée au build (table unique, propriétaire
         http-10:R2, I5 de sa spec).

CADRE DE SESSION http-10:R2 (convention D92 — extension du cadre R1, citée par
la notation g70010 ; le cadre R1 0x5580 reste scellé et indexé par la carte
génération 5, ses offsets internes sont inchangés — l'innocuité de la revendi-
cation @+0x7010 est prouvée par balayage de la notation scellée : jamais lue,
jamais écrite) :
  +0x0000..+0x7017  cadre R1 TEL QUEL (accumulation 0x4000, réécriture 0x3000,
                    zones d'accueil 0x6F00-0x7018 — verdicts http-04, géométrie
                    de session, longueur réécrite @+0x7008, dernier recv
                    @+0x7018) ;
  +0x7010 verdict http-08:R2 (u64 — D92 : écrit APRÈS l'appel du parseur sur
         TOUT chemin, lu aux DEUX dispatches de routage [.trancher, post-
         réécriture] ; valeur 4 = « cible TLS ». Toujours initialisé avant
         lecture : la précède immédiatement l'appel http-08:R2) ;
  +0x7020 garde rdi (u64 — D92 : le rep stosq du cadre TLS emprunte rdi,
         NON-VOLATIL ABI msx64 : préservé au cadre, restitué avant l'appel
         de tls-08 ; jamais lu ni écrit par R1 — innocuité par balayage) ;
  +0x7100 paquet de session (0x30 — convention D90 ci-dessus, écrit par la
         notation avant l'appel de tls-08) ;
  +0x7130 cadre de session TLS (0xC260 — convention D81/D89 ci-dessus, fourni
         VIERGE : rep stosq intégral par la notation, P6/P1) ;
  TAILLE_CADRE_SESSION_R2 = 0x13390 (0x7100 + 0x30 + 0xC260 — le probing Q0
  hérité D63 descend désormais de -0x1000 à -0x13000 par pas de 0x1000, touche
  finale [rsp-0x13390], sub rsp, 0x13390 — 0x13390 multiple de 16 : l'ABI P5
  est préservé, les offsets R1 restent numériquement exacts).

PAQUET DE SESSION TLS (convention D90 — écrit par http-10:R2, lu par tls-08,
P2 de sa spec : « spans : autorité cible [hôte, port], requête claire
réécrite en forme origine, socket cliente, contexte de réponse ») :
  +0x00 hôte ptr (u64 — span autorité, découpé par http-07:R1)
  +0x08 hôte longueur (u64)
  +0x10 port (u16 — ordre hôte, tcp-13:R1 P3)
  +0x18 requête ptr (u64 — forme origine, réécriture propriété http-10:R2)
  +0x20 requête longueur (u64)
  +0x28 socket cliente (u64 — propriété http-10:R2, JAMAIS fermée par tls-08,
         I1 de sa spec) ; le « contexte de réponse » de la P2 vit dans le
         cadre http-10:R2 (table des réponses, zones d'émission) : NON
         consommé par tls-08 — la réponse 502 suit le RETOUR du verdict.

Verdict de session tls-08 (Q2) : le domaine tls-02 (2-6) est transporté TEL
QUEL (jamais remappé) ; VERDICT_CIBLE = 7 est le verdict PROPRE de tls-08
(« cible injoignable » — hors domaine tls-02 par construction).
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
    ("g70005", "tls-05:R1", 0x65C0, 0x180, "M4-dev.1", 1),   # cycle de vie (ARRÊT D81)
    ("g70006", "tls-06:R1", 0x6740, 0x300, "M4-dev.1", 0),   # émission (préfig.)
    ("g70007", "tls-07:R1", 0x6A40, 0x300, "M4-dev.1", 0),   # réception (préfig.)
    ("g70008", "tls-08:R1", 0x6D40, 0x600, "M4-dev.1", 0),   # session TLS (mesurée D90)
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

# --- IAT secur32 : SEPT entrées (D77 — emplacements ARRÊTÉS D81, cf. IAT_SEC32_SLOTS)

SECUR32_IMPORTS = [
    "AcquireCredentialsHandleW", "FreeCredentialsHandle",
    "InitializeSecurityContextW", "DeleteSecurityContext",
    "QueryContextAttributesW", "EncryptMessage", "DecryptMessage",
]
# Concordance IAT ↔ notation vérifiée au build comme en M3 (le répertoire
# d'imports du PE M4 pointera R_IMPORTS_M4 ; INT/hints/dll à leurs RVA).

# --- Constantes à propriétaire unique (charte m4/I § 8) -------------------------

MAX_JETON = 16384               # tls-03 (type 0) : borne des jetons de poignée
HOTE_MAX = L3.HOTE_MAX          # 255 — tls-01 (héritage tcp-13)
# MAX_MESSAGE : JAMAIS une constante — valeur négociée, lue dans les tailles
# de flux ([tailles + 8], acquises par tls-06 — charte § 6/§ 8)
ISC_REQUETES = 0xC01C           # tls-04 (D83) : fContextReq d'Initialize-
                                # SecurityContextW — REPLAY_DETECT 0x4 |
                                # SEQUENCE_DETECT 0x8 | CONFIDENTIALITY 0x10 |
                                # EXTENDED_ERROR 0x4000 | STREAM 0x8000.
                                # STREAM est exigé par tls-03:1 (en-tête/queue)
                                # et tls-06/07 (enregistrements) ; JAMAIS
                                # MANUAL_CRED_VALIDATION (charte § 2 : la
                                # validation automatique reste l'état le plus
                                # dur) ni ALLOCATE_MEMORY (les jetons vivent
                                # dans le cadre, pas en mémoire de bibliothèque).

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
SECBUFFER_MISSING, SECBUFFER_EXTRA = 4, 5     # D89 — réponses DecryptMessage
SECBUFFER_STREAM_TRAILER, SECBUFFER_STREAM_HEADER = 6, 7
TAILLE_SECBUFFER = 16           # { u32 cb, u32 type, u64 pv } — x64
TAILLE_SECBUFFERDESC = 16       # { u32 version, u32 count, u64 pBuffers }
CAPACITE_CADRE_MIN = 16 + 4 * 16   # descripteur le plus large (type 2) = 80 o

# --- Cadre de session TLS (ARRÊT D81 — voir docstring, convention tls-04..08) ---

CADRE_CRED = 0x00               # CredHandle { u64 dwLower, u64 dwUpper }
CADRE_CTXT = 0x10               # CtxtHandle { u64 dwLower, u64 dwUpper }
CADRE_SOCKET = 0x20             # u64 — socket serveur TLS (propriétaire tls-08)
CADRE_PTR_NOM = 0x28            # u64 — vise CADRE_NOM_ZONE (destination tls-01)
CADRE_VERDICT = 0x30            # u32 — verdict poignée (tls-04:Q2)
CADRE_HRESULT = 0x34            # u32 — HRESULT d'origine (tls-02:Q2)
CADRE_ALLERS = 0x38             # u16 — allers-retours (tls-04:Q1)
CADRE_UTILE = 0x3A              # u16 — longueur utile réception (D89, tls-07)
CADRE_OFFSET = 0x3C             # u16 — offset résidu (D89, tls-07 — normalisé
                                # à 0 au début de CHAQUE appel tls-07)
CADRE_TAILLES = 0x40            # 5 x u32 StreamSizes (tls-06 écrit, tls-03 lit)
CADRE_NOM_ZONE = 0x60           # 512 o = 2 * (HOTE_MAX + 1)
CADRE_EMISSION = 0x260          # MAX_JETON
CADRE_RECEPTION = 0x4260        # 2 x MAX_JETON (D89 — tls-07:R1 P1/E2)
CAPACITE_RECEPTION = 2 * MAX_JETON   # 32768 — borne E2 de tls-07
TAILLE_CADRE = 0xC260           # 49760 o (0x8260 avant D89)
SECPKG_CRED_OUTBOUND = 2        # client (tls-05 op 0 — validation AUTOMATIQUE)

# --- .rdata M4 : extension de la zone d'imports secur32 (ARRÊT D81) -------------

R_IMPORTS_M4 = 0x29A0           # table des descripteurs M4 (4 x 20 o, fin 0x29F0)
R_NOM_SEC32 = 0x29F0            # "secur32.dll\0" (12 o)
R_IAT_SEC32 = 0x2A00            # IAT secur32 : 7 slots + terminateur 0x2A38
R_INT_SEC32 = 0x2A40            # INT secur32 : 7 entrées + terminateur 0x2A78
R_HN_SEC32 = 0x2A80             # hints/names secur32 (7 entrées, fin 0x2B2A)
R_PKG_M4 = 0x2C00               # L"Microsoft Unified Security Protocol Provider"
PKG_M4 = "Microsoft Unified Security Protocol Provider".encode("utf-16-le") + b"\x00\x00"

# Fixtures .rdata M4 de tls-08 (D90 — états nommés console, aucun secret) :
R_TXT_TLS_ETABLI = 0x2C60       # "tunnel chiffre etabli\r\n" (23 o) — Q1
TXT_TLS_ETABLI = b"tunnel chiffre etabli\r\n"
R_TXT_TLS_CERT = 0x2C80         # "certificat rejete\r\n" (19 o) — I4 (critère M4)
TXT_TLS_CERT = b"certificat rejete\r\n"

# Fixtures .rdata M4 de http-10:R2 (D92 — l'entrée étiquetée de la table Q3') :
R_TXT_502_CERT = 0x2CA0         # "HTTP/1.1 502 Certificat rejete\r\n\r\n" (34 o)
TXT_502_CERT = b"HTTP/1.1 502 Certificat rejete\r\n\r\n"
REP_502_CERT = 7                # index de l'entrée dans la table des réponses
                                # (7 lignes R1 scellées + la 8e, propriété R2)

# --- Cadre de session http-10:R2 (convention D92 — voir docstring ci-dessus) ------

SESSION_VERDICT_CIBLE = 0x7010  # u64 — verdict http-08:R2 (4 = cible TLS)
SESSION_RDI_GARDE = 0x7020      # u64 — garde de rdi autour du rep stosq (ABI)
SESSION_PAQUET = 0x7100         # 0x30 — paquet de session (convention D90)
SESSION_CADRE_TLS = 0x7130      # 0xC260 — cadre TLS VIERGE (convention D81/D89)
TAILLE_CADRE_SESSION_R2 = 0x13390   # 0x7100 + 0x30 + 0xC260 (multiple de 16)

# --- Paquet de session TLS (convention D90 — http-10:R2 écrit, tls-08 lit) ---------

PAQUET_HOTE_PTR = 0x00          # u64 — span hôte (autorité, http-07:R1)
PAQUET_HOTE_LEN = 0x08          # u64
PAQUET_PORT = 0x10              # u16 — ordre hôte (tcp-13:R1 P3)
PAQUET_REQUETE_PTR = 0x18       # u64 — requête réécrite forme origine
PAQUET_REQUETE_LEN = 0x20       # u64
PAQUET_SOCKET_CLIENT = 0x28     # u64 — propriété http-10:R2 (I1 de tls-08)
# Le « contexte de réponse » (P2 de tls-08) vit dans le cadre http-10:R2,
# NON consommé par tls-08 : la réponse 502 suit le RETOUR du verdict.

VERDICT_CIBLE = 7               # tls-08 (D90) : « cible injoignable » — hors
                                # domaine tls-02 (0-6) : tcp-13 en échec (E1)
                                # OU tls-01 en refus (la cible ne peut être ni
                                # connectée ni nommée pour la poignée) ;
                                # http-10:R2 mappe à 502.

IAT_SEC32_SLOTS = {
    "AcquireCredentialsHandleW": 0x2A00,
    "FreeCredentialsHandle": 0x2A08,
    "InitializeSecurityContextW": 0x2A10,
    "DeleteSecurityContext": 0x2A18,
    "QueryContextAttributesW": 0x2A20,
    "EncryptMessage": 0x2A28,
    "DecryptMessage": 0x2A30,
}
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
