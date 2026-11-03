"""layout.py — Plan d'adressage du projet TRIADE, jalon M5 (profil x86-64-win11-pe).

Source unique de vérité partagée par build_m5.py, outils/auteur.py et
oracle_m5.py. Toute adresse du futur proxy.exe 0.6.0 dérive d'ici ; la
notation référence ces constantes et le builder vérifie la concordance.

HÉRITAGE M0/M1/M2/M3/M4 (R7 — jamais déplacé) :
  - blocs scellés io @ 0x1040/0x1080, libc @ 0x1100-0x13FF (libc-07 @0x13C0) ;
  - blocs réseau M2 @ leurs RVA exacts (tcp-01 0x4000 … tcp-11 0x4B00,
    tcp-13 0x4400) ;
  - zone http @ .text2 (http-01 0x4C00 … http-11 0x5D80), http-12:R1 @0x1800 ;
  - .text3 (0x6000-0x7FFF) : tls-01..08, http-08:R2 0x7340, http-10:R2 0x74C0,
    http-12:R2 0x7DC0 (le câblage D95) — la section est COMPLETE (réserve
    int3 0x7FC0-0x7FFF : 64 o, insuffisante) ;
  - l'extension M5 vit donc dans une section NOUVELLE .text4 — les TROIS
    révisions http-08:R3 / http-10:R3 / http-12:R3 y vivent, leurs ancêtres
    restent indexés par la carte génération 7 et embarqués octet pour octet
    (R7, modèle D77/D95 : la révision cite, elle ne recopie pas).

LA COMPOSITION 0.6.0 (D136, m5/I/README.md — arbitrage du développeur) :
le flux NAVIGATEUR intercepté naît du chemin http:// absolu RELEVÉ vers le
tunnel M4 en amont — le navigateur parle clair au mandataire explicite
(127.0.0.1:25000), le proxy relève vers https:// (Schannel, tls-08 TEL QUEL),
l'autorité de test locale répond. Trois révisions du domaine http :
  - http-08:R3 : le verdict « cible à relever » (5) SOUS POLITIQUE ARMÉE
    SEULEMENT — sans politique : R2 octet pour octet (anti-régression R7,
    le chemin M3 scellé T2 reste vert) ;
  - http-10:R3 : le routage du verdict 5 (LE MÊME chemin que Q2' de R2 —
    port 443) + LA LIGNE DE FLUX (une ligne par session cliente ABOUTIE,
    politique armée seulement — modèle tcp-11, zéro secret, charte § 3) ;
  - http-12:R3 : LA CLI naît — --relever-https arme la politique ; TOUT
    argument inconnu est un REFUS NOMMÉ au démarrage (ExitProcess 3).
    RENUMÉROTÉE R3 (verdict v8) : le nom http-12:R2 est PRIS par le câblage
    D95 embarqué — l'intention écrite m5/I/README.md « http-12:R2 » devient
    http-12:R3, ancêtre http-12:R2 (D95).

ARRÊT (D8 — réarrêté sur la MESURE RÉELLE des notations, comme annoncé
par la préfiguration ; multiples de 64, alignés 16, padding >= 16) :
  http-08:R3 0x8000 (0x1C0 — 377 o mesurés), http-10:R3 0x81C0 (0xAC0 —
  2e réarrêt D8 : la mesure réelle a grandi du ROUTAGE du verdict 5 aux
  trois dispatches et du FORÇAGE E2 du port effectif 443 — l'ancien
  0xA80 laissait moins de 16 o de padding), http-12:R3 0x8C80 (0x340 —
  la marche M5, la CLI et la ligne de politique ; l'ancien 0x8C40 est
  décalé de +0x40 par le réarrêt). ENTREE_PE = 0x8C80 (delta PE
  documenté ; les ancêtres 0x7DC0 et 0x1800 restent embarqués, R7).

Constantes à propriétaire unique (charte m5/I § 8) :
  VERDICT_RELEVER = 5 (http-08:R3 ; distinct des verdicts R2 : 0 succès
  générique, 4 cible TLS) ; LIGNE_FLUX_HOTE_MAX = 14 (borne de ligne
  tcp-11 : préfixe + 12 + suffixe <= 64, P4 de tcp-11:R1 — l'hôte est
  porté TRONQUÉ au-delà, la troncature est nommée dans le contrat) ;
  les compteurs de flux (entre/sortie) tiennent en u32 (l'accumulation
  est bornée 0x4000 et le corps par la table R1). LA LIGNE EST COMPOSÉE
  EN DEUX TEMPS : le préfixe (« flux » + méthode PAR LA TABLE + hôte
  tronqué + «:») au ROUTAGE (.pas_releve — AVANT tout relais : le tampon
  de requête [rsp..rsp+0x4000) est prêté aux relais, http-09 y reçoit la
  réponse, le corps pompé l'écrase ; la méthode vient de R_TAB_METHODES,
  .rdata STABLE — jamais le span du tampon), le suffixe (v/e/s) à .fin ;
  la longueur du préfixe vit à FLUX_PREF_LEN (+0x70D8, le trou R2).

ExtENSION .rdata M5 — la zone libre 0x2CC2-0x2FFF des DEUX scellés (vérifiée
vierge octet pour octet sur proxy.exe 0.4.0 ET 0.5.1) porte les fixtures et
les structures M5 : la ligne de refus CLI, la ligne de politique, les pièces
de la ligne de flux, la commande --relever-https en UTF-16, LA TABLE DES
DESCRIPTEURS M5 (le répertoire d'imports du PE M5 y pointera — les 80 o M4
à 0x29A0 restent en place, espace mort lu par personne, miroir D81 des 60 o
M3), l'entrée kernel32 additionnelle GetCommandLineW (IAT M5 propre — les
slots scellés M3 ne bougent pas, R7) et LA PORTE M5 : une entrée (0x8000,
0x2000, somme .text4) marchée aux BORNES par http-12:R3 (miroir D95 — la
porte se garde elle-même, fail-closed sur entrée trouée).
"""

import importlib.util
import os

# Le plan M4 se charge sous un nom distinct ("layout_m4") : les fichiers
# s'appellent tous layout.py — l'import classique serait circulaire.
_CHEMIN_M4 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "m4", "layout.py")
_spec = importlib.util.spec_from_file_location("layout_m4", _CHEMIN_M4)
L4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L4)   # noqa: E402 — plan M4 (héritage)

# --- Image et sections --------------------------------------------------------

IMAGE_BASE = L4.IMAGE_BASE
TEXT_RVA, RDATA_RVA, DATA_RVA = L4.TEXT_RVA, L4.RDATA_RVA, L4.DATA_RVA
TEXT2_RVA = L4.TEXT2_RVA                      # 0x4000 — complète
TEXT3_RVA = L4.TEXT3_RVA                      # 0x6000 — complète (0x7FC0 int3)
TEXT4_RVA = 0x8000                            # NOUVELLE section M5 (0.6.0)
FILE_ALIGN, SECT_ALIGN = L4.FILE_ALIGN, L4.SECT_ALIGN
TEXT_VSIZE, RDATA_VSIZE, DATA_VSIZE = L4.TEXT_VSIZE, L4.RDATA_VSIZE, L4.DATA_VSIZE
TEXT2_VSIZE = L4.TEXT2_VSIZE                  # 0x2000
TEXT3_VSIZE = L4.TEXT3_VSIZE                  # 0x2000
TEXT4_VSIZE = 0x2000                          # 0x8000-0x9FFF (préfiguration)
SIZE_OF_IMAGE = 0xA000
TEXT_FILE, RDATA_FILE, DATA_FILE = L4.TEXT_FILE, L4.RDATA_FILE, L4.DATA_FILE
TEXT2_FILE, TEXT3_FILE = L4.TEXT2_FILE, L4.TEXT3_FILE
TEXT4_FILE = 0x6E00                           # après .text3 (0x4E00+0x2000)
DATA_RAW = L4.DATA_RAW                        # .data committée (état serveur)
TAILLE_FICHIER = 0x8E00                       # 0x6E00 + 0x2000

DLL_CHARACTERISTICS = L4.DLL_CHARACTERISTICS  # DYNAMICBASE | HEVA | NX

VERSION_DEV1 = "0.6.0-dev.1"   # les trois révisions http R3 + la porte M5
VERSION_U64_DEV1 = 0x00060000  # R10 : monotonie (> 0.5.1 = 0x00050003 ≥
                               # plancher 0.4.0)
VERSION_U64_MIN = 0x00040000   # plancher hérité (http-12:Q1 scellé)
VERSION_060 = "0.6.0"          # la balise est posée à la validation terrain

# --- Blocs embarqués dans proxy.exe M5 (couche C, génération 7 — g8xxxx) -------

BLOCS_REVISIONS_M5 = [
    ("g80001", "http-08:R3", 0x8000, 0x1C0, "M5-dev.1", 0),   # cible + verdict « à relever » (mesure 377 o)
    ("g80002", "http-10:R3", 0x81C0, 0xAC0, "M5-dev.1", 0),   # session + routage 5 + ligne de flux (2e réarrêt D8)
    ("g80003", "http-12:R3", 0x8C80, 0x340, "M5-dev.1", 0),   # orchestration + porte M5 + CLI (décalé +0x40)
]
# L'héritage M4 complet (io, libc, tcp, http R1/R2, tls, http-12:R2) est
# repris OCTET POUR OCTET (R7) — le build_m5 le lira via L4/B4.

ENTREE = L4.ENTREE            # 0x1800 — http-12:R1 (R7, mort au lancement)
ENTREE_R2 = L4.ENTREE_R2      # 0x7DC0 — http-12:R2 (R7, mort au lancement)
ENTREE_M5 = 0x8C80            # 0.6.0 : le point d'entrée PE devient http-12:R3
                              # (2e réarrêt D8 — l'ancien 0x8C40 est décalé)

NOMS_BLOCS = dict(L4.NOMS_BLOCS) | {
    "g80001": "http-cible-r3", "g80002": "http-session-r3",
    "g80003": "http-principal-r3",
}

# --- .text4 : zones ------------------------------------------------------------

ZONE_REVISIONS_M5 = (0x8000, 0x8C7F)   # http-08:R3, http-10:R3 (mesure)
ZONE_PRINCIPAL_M5 = (0x8C80, 0x8FBF)   # http-12:R3 (l'entrée PE)
ZONE_RESERVEE_T4 = (0x8FC0, 0x9FFF)    # int3 — extension future (patch à chaud)

# --- .rdata M5 : fixtures, imports additionnels, porte M5 ------------------------
# La zone démarre APRÈS la dernière fixture M4 (0x2CA0 + 34 = 0x2CC2) ; les
# octets 0x2CC2-0x2FFF sont VIERGES dans les DEUX scellés (vérifié au build).

R_TXT_CMD_KO = 0x2CE0          # "TRIADE M5 : argument inconnu, arret\r\n" (37 o)
TXT_CMD_KO = b"TRIADE M5 : argument inconnu, arret\r\n"

R_TXT_POLITIQUE = 0x2D10       # "relever-https arme\r\n" (20 o) — ligne console
TXT_POLITIQUE = b"relever-https arme\r\n"   # de l'état nommé (politique armée)

# ARRÊT (propriétaire unique, charte § 8) : les littéraux de la LIGNE DE FLUX
# (« flux », «  », « : », « v= », « e= », « s= », CRLF) vivent EN IMMÉDIATS
# dans la notation http-10:R3 (I9 : la ligne est composée DANS LE CADRE,
# zones FLUX — jamais en donnée statique) ; la zone 0x2D30-0x2D7F reste
# VIERGE (aucune fixture morte — le premier jet du plan prévoyait des
# fixtures .rdata, la notation les a remplacées par des immédiats, le plan
# suit).

R_CMD_RELEVER = 0x2D80         # L"--relever-https" + NUL (32 o) — comparaison
TXT_CMD_RELEVER = "--relever-https".encode("utf-16-le") + b"\x00\x00"
CMD_RELEVER_LEN = 15           # caractères larges (30 o + NUL)

R_IMPORTS_M5 = 0x2DA0          # table des descripteurs M5 (5 x 20 o, fin 0x2E04) :
                               # kernel32#2 (GetCommandLineW) + les trois
                               # descripteurs M4 REPRIS (pointeurs identiques) + terme
R_NOM_KERNEL32_M5 = 0x2E10     # "kernel32.dll\0" (13 o) — nom propre au descripteur M5
R_IAT_M5 = 0x2E30              # IAT M5 : 1 slot + terminateur (0x2E38)
R_INT_M5 = 0x2E50              # INT M5 : 1 entrée + terminateur (0x2E58)
R_HN_M5 = 0x2E70               # hints/names : hint u16 + "GetCommandLineW\0" (18 o)

R_TAB_SUM_M5 = 0x2EA0          # porte M5 : UNE entrée (0x8000, 0x2000, somme .text4)
R_BORNE_M5 = 0x2EB0            # la BORNE de marche (l'adresse après l'entrée) —
                               # miroir D95 : la table est PLEINE, fail-closed

IAT_M5_SLOTS = {
    "GetCommandLineW": R_IAT_M5,   # 0x2E30
}
SECUR32_IMPORTS = L4.SECUR32_IMPORTS       # héritage (R7)
KERNEL32_M5_IMPORTS = ["GetCommandLineW"]  # l'entrée nouvelle (I1 de http-12:R3)

# --- .data M5 : l'état de la politique ------------------------------------------

R_POLITIQUE = 0x3860           # u64 — 0 : chemin scellé ; 1 : --relever-https armé
                               # (unique propriétaire http-12:R3, écrit UNE fois
                               # au démarrage avant toute initialisation réseau,
                               # lu par http-10:R3 — jamais par les feuilles pures)

# --- Cadre de session http-10:R3 (convention 0.6.0 — extension du cadre R2) ------
# TAILLE_CADRE_SESSION INCHANGÉE (0x13390 — l'ABI P5 et le probing D63 restent
# exacts) : les zones R3 vivent dans le trou documenté +0x7028..+0x70FF du
# cadre R2 (jamais lu ni écrit par R1/R2 — innocuité par balayage, miroir D92).

FLUX_VERDICT = 0x7028          # u64 — verdict de session (ligne de flux) ;
                               # -1 = sentinelle « session non identifiable »
                               # (aucune ligne — rien à nommer)
FLUX_POLITIQUE = 0x70D0        # u64 — la CACHE de la politique (P7 : l'état
                               # .data R_POLITIQUE lu UNE fois par session au
                               # passage de http-08:R3, jamais relu ; la loge
                               # ABI du 5e argument vit SOUS le cadre — le
                               # tampon de requête [rsp..rsp+0x4000) n'est
                               # JAMAIS touché par l'argumentation)
FLUX_PREF_LEN = 0x70D8         # u64 — la longueur du préfixe « flux <m> <h>: »
                               # (composé au ROUTAGE, .pas_releve — AVANT tout
                               # relais : la méthode vient de R_TAB_METHODES
                               # (.rdata STABLE) et l'hôte y est copié pendant
                               # la validité de son span ; le tampon de requête
                               # [rsp..rsp+0x4000) est prêté aux relais —
                               # http-09 y reçoit la réponse, le corps pompé
                               # l'écrase ; les ZONES FLUX au-delà de 0x4000
                               # ne le sont JAMAIS)
ZONE_FLUX_PREF = 0x7030        # 0x40 — le préfixe « flux <methode> <hote>: »
ZONE_FLUX_SUF = 0x7070         # 0x60 — le suffixe «:port v=… e=… s=…\r\n»
ZONE_FLUX_ITOA = 0x70E0        # 0x10 — le tampon libc-04 (12 o utiles)
FLUX_HOTE_MAX = 14             # la borne de ligne tcp-11 (P4 : préfixe + 12 +
                               # suffixe <= 64) — au-delà : troncature NOMMÉE

# Domaine TOTAL du verdict de session (la ligne ne porte QUE des états nommés) :
#   -1 : session non identifiable (pas de ligne de flux)
#    0 : aboutie — requête servie (relais M3 à fermeture délimitée, relais TLS
#        réussi [tls-08 verdict 0], tunnel CONNECT établi)
#  2..7 : verdicts tls-08 TRANSPORTÉS TELS QUELS (3 = certificat rejeté —
#        LE critère (b) vu du navigateur ; la réponse 502 suit le retour)
#  400/411/431/501/502/505 : la réponse d'erreur HTTP nommée (chemin hérité)
SENTINELLE_FLUX = -1

# --- Jetons de retour d'émulation (oracle, hors binaire) ------------------------

SENTINELLE_RETOUR = L4.SENTINELLE_RETOUR

# --- Réexports de l'héritage M4 (le plan M5 est la source unique pour ses outils) -

IAT_SLOTS = L4.IAT_SLOTS       # kernel32 + ws2_32 (R7 — scellé 0.4.0)
IAT_SEC32_SLOTS = L4.IAT_SEC32_SLOTS
R_TAB_SUM = L4.R_TAB_SUM       # la table M3/M4 (28 entrées) — marche héritée
R_VERSION = L4.R_VERSION       # 0x2820 — la borne héritée (adresse)
R_ANCRE = L4.R_ANCRE
R_SLASH = L4.R_SLASH
R_TAB_METHODES = L4.R_TAB_METHODES
R_METHODES = L4.R_METHODES
R_TAB_REPONSES = L4.R_TAB_REPONSES
R_TXT_400, R_TXT_431 = L4.R_TXT_400, L4.R_TXT_431
R_TXT_501, R_TXT_411 = L4.R_TXT_501, L4.R_TXT_411
R_TXT_505, R_TXT_502 = L4.R_TXT_505, L4.R_TXT_502
R_TXT_TUNNEL = L4.R_TXT_TUNNEL
R_TXT_502_CERT = L4.R_TXT_502_CERT
R_PKG_M4 = L4.R_PKG_M4
R_TXT_TLS_ETABLI = L4.R_TXT_TLS_ETABLI
R_TXT_TLS_CERT = L4.R_TXT_TLS_CERT
R_MSG_BANNIERE = L4.R_MSG_BANNIERE
R_MSG_CONNEXION = L4.R_MSG_CONNEXION
R_MSG_TUNNEL, R_MSG_FIN = L4.R_MSG_TUNNEL, L4.R_MSG_FIN
R_MSG_ARRET, R_MSG_ERREUR = L4.R_MSG_ARRET, L4.R_MSG_ERREUR
R_MSG_KO = L4.R_MSG_KO
R_CMD_QUIT = L4.R_CMD_QUIT
R_NOM_HOST, R_NOM_CL, R_NOM_TE = L4.R_NOM_HOST, L4.R_NOM_CL, L4.R_NOM_TE
R_STDOUT, R_STDIN = L4.R_STDOUT, L4.R_STDIN
R_LISTEN, R_QUIT, R_CS = L4.R_LISTEN, L4.R_QUIT, L4.R_CS
R_CURSEUR, ARENE_BASE = L4.R_CURSEUR, L4.ARENA_BASE
BANNIERE, PORT_ECOUTE = L4.BANNIERE, L4.PORT_ECOUTE
TAILLE_CADRE_SESSION = L4.TAILLE_CADRE_SESSION_R2   # 0x13390 — INCHANGÉ (R3)
CADRE_TLS = L4.SESSION_CADRE_TLS                    # +0x7130 (convention D81/D89)
PAQUET_ = L4.SESSION_PAQUET                         # +0x7100 (convention D90)
VERDICT_CIBLE = L4.VERDICT_CIBLE                    # 7 (tls-08 : cible injoignable)
SESSION_VERDICT_CIBLE = L4.SESSION_VERDICT_CIBLE    # +0x7010 (convention D92)
