"""layout.py — Plan d'adressage du projet TRIADE, jalon M8 (profil
x86-64-win11-pe, le domaine sys — l'ère 0.9.0 des additions mesurées, D160),
ÉTENDU au chantier M9-(d) : LE SOCLE SOCKET (sys-04..06, l'ère 1.0.0 du
transport — la fondation I/O du client TLS 1.3 pur, le plan M9 l'attendait).

Source unique de vérité partagée par le futur build_m8.py, outils/auteur.py
et oracle du jalon (les chantiers (b)/(c)). Toute adresse, tout décalage,
toute constante du domaine dérive d'ici ; la notation référencera ces
constes et le builder vérifiera la concordance. La présente version NAÎT à
l'ouverture (couche I écrite-avant-code, modèle D77) : les RVA définitifs
des blocs seront ARRÊTÉS au chantier (b) sur les longueurs réelles des
notations (D47/D79 — la mesure auteur décide, la préfiguration n'est pas
un droit).

HÉRITAGE M0/M1/M2/M3/M4/M5 (R7 — jamais déplacé) :
  - le proxy.exe 0.6.0 SCELLÉ (m5/, sha consigné à la carte génération 7) :
    TOUT son plan d'adressage vit dans m5/layout.py — le présent module le
    CHARGE par chemin absolu (leçon D158 : les layout.py homonymes se
    chargent par importlib, jamais par sys.path) et n'ajoute QUE la
    section .text5 et les constantes du domaine sys ;
  - .text/.rdata/.data/.text2/.text3/.text4 COMPLÈTES (0x1000-0x9FFF) :
    l'extension M8 vit dans une section NOUVELLE .text5 — le corps scellé
    0.6.0 ne bouge pas d'un octet (§ 9).

LA SECTION .text5 (ARRÊT D161 au chantier (b) — la mesure auteur décide) :
  0xA000-0xBFFF (8 Kio, modèle .text3/.text4) ; SizeOfImage 0xA000 → 0xC000
  et la table de sections 6 → 7 entrées AU BUILD du chantier (c) — deltas PE
  documentés alors (modèle D94/D136). Slots ARRÊTÉS sur les longueurs réelles
  des notations (D8 — multiples de 64, alignés 16, padding >= 16), tassés
  depuis 0xA000 (la préfiguration 0xA000/0xA400/0xB000 n'était pas un
  droit, D47/D79) :
    sys-01 @ 0xA000 (0x40)   l'émetteur — six octets utiles (mesurés), NOP au reste ;
    sys-02 @ 0xA040 (0x140)  le résolveur — 293 o notés (mesurés), NOP au reste ;
    sys-03 @ 0xA180 (0xC0)   la twin de hello-02 — 164 o notés (mesurés), NOP au reste ;
    réserve 0xA240-0xBFFF (croissance du domaine : sys-04 et suivants).

LES CONSTANTES DU DOMAINE (charte m8/I/README.md — source unique ici) :
  - MOTIF_STUB : les quatre premiers octets du stub natif Windows 10/11
    x64 (4C 8B D1 B8 = mov r10, rcx ; mov eax, imm32) — vérifié AVANT
    toute extraction (charte § 2) ; le labo prouve sur FIXTURES, le
    terrain mesure le VRAI (la version Windows du run consignée au
    témoin) ; OFF_SSN : le décalage de l'imm32 dans le stub (4) ;
  - les décalages PE/EAT : le format PE32+ est STABLE (documenté) —
    e_lfanew @ +0x3C (fenêtre lisible [0x40, 0x400]), le motif « PE\\0\\0 »,
    le répertoire export (1re entrée du DataDirectory) @ PE+0x88
    (RVA) / +0x8C (taille), et dans le répertoire export :
    NumberOfFunctions @ +0x14, NumberOfNames @ +0x18,
    AddressOfFunctions @ +0x1C, AddressOfNames @ +0x20,
    AddressOfNameOrdinals @ +0x24 (tous RVA 32 bits relatifs à la base) ;
  - la TABLE DES VERDICTS du domaine (charte § 5) — les SEPT noms, jamais
    recopiés dans les spécifications ;
  - les versions de l'ère : 0.9.0-dev.1 (posée par le premier build M8 —
    geste de BUILD, jamais scellage, miroir M6/M7 D149) et 0.9.0 (la
    finale attendra le terrain vert du chantier (d)) ; le plancher R10
    demeure 0x00040000 (hérité — l'anti-rollback ne se relâche pas d'une
    ère à l'autre).
"""

import importlib.util
import os

# --- L'héritage m5 chargé par chemin absolu (leçon D158) ------------------------

ICI = os.path.dirname(os.path.abspath(__file__))
_CHEMIN_M5 = os.path.join(os.path.dirname(ICI), "m5", "layout.py")
_spec = importlib.util.spec_from_file_location("layout_m5", _CHEMIN_M5)
L5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L5)

# --- Image et sections (l'héritage réexporté — le build (c) compose depuis 0.6.0)

IMAGE_BASE = L5.IMAGE_BASE
SIZE_OF_IMAGE_M5 = L5.SIZE_OF_IMAGE          # 0xA000 — le corps scellé 0.6.0
SIZE_OF_IMAGE = 0xC000                       # 0xA000 + .text5 (AU BUILD (c))
TEXT5_VA = 0xA000                            # la section NOUVELLE du jalon
TEXT5_FILE = 0x8E00                          # ARRÊT D162 (chantier (c)) : la
                                            # 7e section vit APRÈS .text4 —
                                            # les SIX premières raw INCHANGÉES
                                            # (0x400/0x1400/0x2400/0x2E00/
                                            # 0x4E00/0x6E00), les 7 en-têtes
                                            # (608 o) TIENNENT dans la marge
                                            # 0x400 : le décalage de packaging
                                            # D94 n'est PAS rejoué
TAILLE_FICHIER = 0xAE00                      # 0x8E00 + 0x2000 (ARRÊT D162)
TAILLE_FICHIER_M5 = L5.TAILLE_FICHIER        # le scellé — ne bouge pas

# --- Les slots ARRÊTÉS du domaine sys (D161 — la mesure auteur décide) -----------
# ARRÊT DÉFINITIF au chantier (b) sur les longueurs RÉELLES des notations
# (D47/D79 : la préfiguration 0xA000/0xA400/0xB000 n'était pas un droit) :
#   sys-01 : 6 o notés   -> slot 0x40  (padding 58)
#   sys-02 : 293 o notés -> slot 0x140 (padding 27)
#   sys-03 : 164 o notés -> slot 0xC0  (padding 28)
# Tassés depuis 0xA000 (D8 : slots multiples de 64, alignés 16, padding >= 16)
# — la réserve contiguë 0xA240-0xBFFF (7 488 o) porte la croissance du
# domaine (sys-04 et suivants ; TLS 1.3 pur attend sa décision propre, D160).

SYS01_VA = 0xA000        # g90001 — l'émetteur (slot 0x40)
SYS02_VA = 0xA040        # g90002 — le résolveur (slot 0x140)
SYS03_VA = 0xA180        # g90003 — la twin de hello-02 (slot 0xC0)
ZONE_SYS = (0xA000, 0xBFFF)       # .text5 entière
ZONE_SYS_RESERVE = (0xA240, 0xBFFF)   # la croissance du domaine
SLOTS_SYS = {
    "g90001": (SYS01_VA, 0x40),
    "g90002": (SYS02_VA, 0x140),
    "g90003": (SYS03_VA, 0xC0),
}

# --- Les constantes du domaine (charte m8/I/README.md — source unique) ----------

MOTIF_STUB = bytes.fromhex("4C8BD1B8")   # mov r10, rcx ; mov eax, imm32
OFF_SSN = 4                              # l'imm32 du SSN dans le stub
MOTIF_PE = b"PE\x00\x00"
E_LFANEW = 0x3C                          # DOS → offset du motif PE
E_LFANEW_MIN = 0x40                      # la fenêtre lisible (verdict -2 sinon)
E_LFANEW_MAX = 0x400
OFF_EXPORT_RVA = 0x88                    # DataDirectory[0] (PE32+) : RVA
OFF_EXPORT_TAILLE = 0x8C                 #                       : taille
EXP_NBFONC = 0x14                        # le répertoire export :
EXP_NBNOMS = 0x18                        #   NumberOfNames (la borne, charte § 8)
EXP_ADRFONC = 0x1C                       #   AddressOfFunctions (RVAs)
EXP_ADRNOMS = 0x20                       #   AddressOfNames (RVAs des noms)
EXP_ADRORD = 0x24                        #   AddressOfNameOrdinals (u16)

# la TABLE DES VERDICTS (charte § 5 — les SEPT noms du domaine)
V_RESOLU = 0            # succès : résolu (sys-02) / émis (sys-03)
V_NOM_ABSENT = -1       # le nom est introuvable dans l'EAT (marche complète)
V_PAS_MODULE = -2       # la base n'est pas un module PE (motif / e_lfanew fou)
V_EAT_ABSENTE = -3      # le répertoire export est absent (RVA nul)
V_STUB_DIVERGENT = -4   # le stub diverge du motif (hook ou ère inconnue)
V_SPAN_INVALIDE = -5    # le span du nom est invalide (nul / longueur nulle)
V_STATUS_NONNUL = -6    # le syscall a rendu un STATUS non nul (consigné rdx)

# --- Les versions de l'ère (geste de BUILD au premier build — jamais scellage) ---

VERSION_DEV1 = "0.9.0-dev.1"     # posée par le premier build M8 (chantier (c))
VERSION_U64_DEV1 = 0x00090001
VERSION_U64_MIN = 0x00040000     # le plancher R10 hérité (jamais relâché)
VERSION_FINALE = "0.9.0"         # la finale attend le terrain vert du (d)

# --- Les noms de blocs (la carte génération 8 — chantier (c)) -------------------

NOMS_BLOCS = dict(L5.NOMS_BLOCS) | {
    "g90001": "sys-01-emetteur",
    "g90002": "sys-02-resolveur",
    "g90003": "sys-03-ecriture",
}

# --- Les fixtures .rdata du domaine (chantier (b) — posées au build (c)) ---------
# La zone 0x2EB0-0x2FFF est VIERGE dans le scellé 0.6.0 (vérifiée sur pièces au
# (b) : 336 octets nuls dans proxy.exe, .rdata raw 0x1400 — après la borne de
# marche M5 R_BORNE_M5 = 0x2EB0). Les fixtures du domaine y vivent : le corps
# scellé ne bouge d'AUCUN octet (R7), la zone libre reçoit les nouveaux.

R_SYS_NOM = 0x2EC0      # "NtWriteFile" — le span-nom (P3 de sys-03), la CLEF
TXT_SYS_NOM = b"NtWriteFile"    # 11 octets, AUCUN NUL : P1 de sys-02 est un SPAN
LEN_SYS_NOM = 11        # la mesure sur pièces (erratum M8-(b) : la couche I
                        # naissante disait « 10 octets » — N-t-W-r-i-t-e-F-i-l-e)

R_SYS_LIGNE = 0x2ED0    # la LIGNE de hello-02 — le fixture M0 CITÉ (I4 de
                        # sys-03) : byte-exact le MESSAGE de m0/build_m0.py
                        # (jamais une seconde copie : la twin ÉMET ces octets)
TXT_SYS_LIGNE = b"TRIADE M0 : Hello, Windows 11 !\r\n\x00"   # 33 utiles + NUL
LEN_SYS_LIGNE = 33      # la longueur ÉMISE (hello-02 reçut r8d=33 de M0)

R_SYS_BORNE = 0x2F00    # la borne des fixtures du domaine (fail-closed, miroir
                        # D95 : le prochain fixture pose ICI, jamais au-delà
                        # sans arrêt nommé — 0x2F00-0x2FFF demeure en réserve)

# --- memcmp — le seul appel direct DÉCLARÉ du domaine (I2 de sys-02) -------------
# Cité depuis la table scellée de la lignée (jamais un littéral) : libc-02:R1,
# bloc carte b20002, embarqué à chaque build depuis M1.

def _trouver_memcmp():
    for ent in L5.L4.L3.BLOCS_LIBC_EMBARQUES:
        if ent[0] == "b20002":
            return ent[2], ent[3]
    raise RuntimeError("b20002 (libc-02 memcmp) introuvable à la table scellée")

MEMCMP_VA, MEMCMP_SLOT = _trouver_memcmp()   # 0x1180, 0x80 — la source héritée

# ============================================================================
# --- LE TRANSPORT AFD (chantier M9-(d), l'ère 1.0.0 — charte § 9 du README ---
# --- révisé : la source unique des constantes du socle socket sys-04..06) ---
#
# PROVENANCE (la couche I la cite, l'instrument verifier_specs_m9d.py la
# RE-DÉRIVE PAR CODE — le juge est le code, jamais une copie d'écriture) :
#   (1) les définitions canoniques du header phnt/ntafd.h — « Ancillary
#       Function Driver Definitions », diversenok, Hunt & Hackett, avril 2025
#       (systeminformer/phnt, commit 2dda0dd) : AfdOpenPacket, la macro
#       _AFD_CONTROL_CODE, AFD_CONNECT_JOIN_INFO_TL, AFD_BIND_INFO_TL,
#       AFD_SEND_INFO/AFD_RECV_INFO (C_ASSERT mêmes tailles), les
#       AFD_*ADDRUSE et les TDI_RECEIVE_* ;
#   (2) les MESURES WinDbg Windows 11 x64 de la série « Under the Hood of
#       AFD.sys » (M. Lewczak, leftarcode.com, parties 1 à 4, juillet-août
#       2025) : les dumps OCTET PAR OCTET du create EA, du bind IMPLICITE
#       mswsock, du connect (SOCKADDR en mode TLI — aucun device de
#       transport déclaré à la création), du send et du receive — recopiés
#       en VECTEURS DORÉS à l'instrument ;
#   le laboratoire ne possède AUCUN Windows : les preuves de notation se
#   joueront au harnais sur FIXTURES AFD SYNTHÉTIQUES (le modèle
#   différentiel M4/M5), et le terrain M9-(f) confrontera le VRAI afd.sys de
#   la machine du développeur — la version Windows du run sera consignée au
#   témoin (charte § 2, la réserve d'ère étendue au transport).
#
# L'ORDRE DES GESTES DE sys-04 (la séquence mesurée mswsock, jamais une
# invention) : NtCreateFile(\Device\Afd\Endpoint, EA AfdOpenPacketXX, le
# handle SYNCHRONE) PUIS IOCTL_AFD_BIND (le bind implicite WILDCARD —
# « infer the address », jamais une adresse choisie par le domaine) PUIS
# IOCTL_AFD_CONNECT (le sockaddr distant du kit, boutisme réseau) — chaque
# SSN résolu AU GESTE MÊME par sys-02 (charte § 1/§ 6 : le bloc ne détient
# rien, chaque appel résout).
# ============================================================================

# --- le périphérique et le EA de création (les mesures p. 1) --------------------

AFD_NOM_DEVICE = "\\Device\\Afd\\Endpoint"    # le nom ouvert par ws2_32 sur
                                             # Windows 11 (mesuré leftarcode
                                             # p.1 — phnt nomme le device
                                             # \Device\Afd, la MESURE ouvre
                                             # \Device\Afd\Endpoint)
TXT_AFD_DEVICE = AFD_NOM_DEVICE.encode("utf-16le")   # 40 o — 20 caractères
LEN_AFD_DEVICE = 40                         # sans le NUL UTF-16 du fixture

AFD_EA_NOM = b"AfdOpenPacketXX"              # 15 o — phnt AfdOpenPacket ;
                                             # ReactOS AFD_PACKET_COMMAND_
                                             # LENGTH 15 : les DEUX recoupent
LEN_AFD_EA_NOM = 15
AFD_EA_VALEUR = 30                           # EaValueLength MESURÉ (dump
                                             # 1E 00) : les SIX DWORD utiles
                                             # + 6 o de marge — les NOTRES
                                             # NULS (déterministes ; la
                                             # mesure ws2_32 y laisse du
                                             # bruit de pile qu'afd.sys ne
                                             # lit pas : TransportDevice-
                                             # NameLength = 0)
AFD_EA_TAILLE = 54                           # 8 (l'en-tête EA) + 16 (le nom
                                             # + NUL) + 30 (la valeur)

# --- les paramètres du NtCreateFile (les mesures p. 1) -------------------------

AFD_DESIRED_ACCESS = 0xC0140000              # mesuré ws2_32 Windows 11 (GENERIC_
                                             # READ|WRITE + SYNCHRONIZE +
                                             # marge d'accès — la mesure fait
                                             # foi, le terrain recoupera)
AFD_CREATE_OPTIONS = 0x20                    # FILE_SYNCHRONOUS_IO_NONALERT :
                                             # le handle est SYNCHRONE — le
                                             # recv BLOQUANT du kit (Q2 du
                                             # socle tls13-28)
AFD_CREATE_DISPOSITION = 1                   # FILE_OPEN
AFD_SHARE_ACCESS = 3                         # FILE_SHARE_READ | FILE_SHARE_WRITE
OBJ_CASE_INSENSITIVE = 0x40                  # les attributs d'objet (mesuré)
OBJECT_ATTRIBUTES_TAILLE = 0x30              # 48 o (mesuré)

# --- l'endpoint du jalon (le EA porté par ces valeurs, jamais ailleurs) --------

AF_INET = 2                                  # la famille IPv4
SOCK_STREAM = 1                              # le flux TCP
IPPROTO_TCP = 6                              # le protocole TCP
SOCKADDR_TAILLE = 16                         # sockaddr_in : family u16 LE,
                                             # port u16 RÉSEAU, adresse u32
                                             # RÉSEAU, zero[8] — LE BOUTISME
                                             # EST CELUI DU FORMAT, le kit
                                             # fournit, le domaine ne
                                             # convertit JAMAIS en silence

# --- les IOCTL du transport — DÉRIVÉS PAR LA MACRO canonique -------------------
# _AFD_CONTROL_CODE(Request, METHOD_NEITHER) = FILE_DEVICE_NETWORK(0x12) << 12
#     | Request << 2 | 3  (phnt ; les quatre recoupés par les mesures) :
#   BIND 0x12003 (mesuré p.2) · CONNECT 0x12007 (p.2) ·
#   RECEIVE 0x12017 (p.4) · SEND 0x1201F (p.3).

AFD_REQ_BIND = 0
AFD_REQ_CONNECT = 1
AFD_REQ_RECEIVE = 5
AFD_REQ_SEND = 7


def _afd_ioctl(req):
    return 0x12 << 12 | req << 2 | 3


IOCTL_AFD_BIND = _afd_ioctl(AFD_REQ_BIND)            # 0x12003
IOCTL_AFD_CONNECT = _afd_ioctl(AFD_REQ_CONNECT)      # 0x12007
IOCTL_AFD_RECEIVE = _afd_ioctl(AFD_REQ_RECEIVE)      # 0x12017
IOCTL_AFD_SEND = _afd_ioctl(AFD_REQ_SEND)            # 0x1201F

# --- les structures d'échange (les mesures p. 2/3/4 — les tailles EXACTES) -----

AFD_BIND_WILDCARD = 2                        # AFD_WILDCARDADDRESS (phnt) : le
                                             # bind IMPLICITE mswsock au
                                             # connect — le noyau DÉDUIT
                                             # l'adresse source (mesuré p.2 :
                                             # « infer from which available
                                             # address » — jamais une
                                             # adresse choisie par le domaine)
AFD_BIND_TAILLE = 0x14                       # 20 o : flags u32 + SOCKADDR 16
AFD_BIND_SORTIE = 0x10                       # 16 o de sortie (mesuré !irp)
AFD_CONNECT_TAILLE = 0x28                    # 40 o : SanActive (1 + 7 NUL) +
                                             # RootEndpoint 8 + Connect-
                                             # Endpoint 8 (la MESURE : les
                                             # zéros SONT acceptés) + SOCKADDR
AFD_SENDRECV_TAILLE = 0x18                   # 24 o : BufferArray ptr +
                                             # BufferCount u32 + AfdFlags u32 +
                                             # TdiFlags u32 (C_ASSERT phnt :
                                             # SEND == RECV)
WSABUF_TAILLE = 12                           # len u32 + buf ptr
TDI_RECEIVE_NORMAL = 0x20                    # le recv NORMAL : le champ
                                             # AfdFlags MESURÉ (leftarcode
                                             # p.4 : « I have experimentally
                                             # checked » — la littérature le
                                             # met en TdiFlags, la MESURE le
                                             # met en AfdFlags ; l'erratum de
                                             # lecture consigné à sys-06)
IOSB_TAILLE = 16                             # IO_STATUS_BLOCK : Status 8 +
                                             # Information 8 (le compteur du
                                             # transport : émis/lu)

# --- la table des verdicts ÉTENDUE (charte § 5 : le huitième nom) ---------------

V_TRANSPORT_ECHEC = -7                       # l'émission PARTIELLE, la DEMI-FIN
                                             # de réception (Q2/Q3 du socle
                                             # tls13-28 : « le zéro de
                                             # réception est le refus -7 du
                                             # KIT » ; « un envoi partiel est
                                             # le refus du kit ») — la table
                                             # du domaine passe de SEPT à
                                             # HUIT noms à M9-(d)

# --- les noms NT du transport (les CLEFS de résolution — des SPANS, jamais -----
# --- de NUL supposé, miroir R_SYS_NOM) ------------------------------------------

TXT_NT_CREATEFILE = b"NtCreateFile"              # 11 o — le geste 1 de sys-04
LEN_NT_CREATEFILE = 11
TXT_NT_DEVICEIOCTL = b"NtDeviceIoControlFile"    # 21 o — les gestes 2/3 de
LEN_NT_DEVICEIOCTL = 21                          #        sys-04, 05 et 06
TXT_NT_CLOSE = b"NtClose"                        # 7 o — LA FERMETURE AU KIT
LEN_NT_CLOSE = 7                                 # (le kit résoudra et émettra
                                                 # par sys-02 + sys-01 : la
                                                 # fermeture n'est PAS un bloc)

# --- Les slots .text5 du socle (sys-04..06 — L'ARRÊT DÉFINITIF au geste de ---
# --- la notation, D161 REJOUÉ : la mesure auteur décide, la préfiguration ---
# --- s'est inclinée — 676/289/287 o de code MESURÉS (la leçon du round-trip ---
# --- au passage : le DesiredAccess en edx ZÉRO-étendu, jamais mov rdx ---
# --- dont le C7 SIGNERAIT l'extension — le harnais l'a attrapé AVANT le ---
# --- noyau), les tailles des slots restent les bornes préfigurées ---------
# --- tassées depuis la réserve contiguë 0xA240, la croissance M8) -------------

SYS04_VA = 0xA240        # g90004 — l'établissement : 676 o MESURÉS (arrêté :
SYS05_VA = 0xA540        # g90005 — l'émission : 289 o MESURÉS (arrêté :
SYS06_VA = 0xA6C0        # g90006 — la réception : 287 o MESURÉS (arrêté :
SLOTS_SYS["g90004"] = (SYS04_VA, 0x300)   # 676 o de code · 92 o de NOP (I10)
SLOTS_SYS["g90005"] = (SYS05_VA, 0x180)   # 289 o de code · 95 o de NOP (I8)
SLOTS_SYS["g90006"] = (SYS06_VA, 0x180)   # 287 o de code · 97 o de NOP (I9)

NOMS_BLOCS["g90004"] = "sys-04-transport"
NOMS_BLOCS["g90005"] = "sys-05-emission"
NOMS_BLOCS["g90006"] = "sys-06-reception"

# --- Les fixtures .text6 du transport (PRÉFIGURATION — l'ARRÊT au geste de -----
# ---- la notation, miroir D161 : la mesure décidera ; la réserve .rdata M8 ----
# ---- est ÉPUISÉE par K[64] [Entrée 172], les fixtures vivent AU-DELÀ des ------
# ---- fixtures poignée tls13 [fin 0x10C10 : R_HRR 0x10BF0 + 32], chacun --------
# ---- aligné 16 — l'instrument recoupe les DEUX plans, la concordance des ------
# ---- bornes est un contrôle VERT) ---------------------------------------------

R_SYS_DEVICE = 0x10C20         # le nom UTF-16LE du périphérique + NUL (42 o)
R_SYS_EA = 0x10C50             # le EA complet DÉTERMINISTE (54 o — la valeur
                               # aux SIX DWORD utiles + 6 NULS)
R_SYS_BIND = 0x10C90           # le bind implicite WILDCARD (20 o : flags 2,
                               # AF_INET, port 0, INADDR_ANY, zero NUL)
R_SYS_NOM_CREATEFILE = 0x10CB0  # « NtCreateFile » (11 o, SPAN sans NUL)
R_SYS_NOM_DEVICEIOCTL = 0x10CC0  # « NtDeviceIoControlFile » (21 o, SPAN)
R_SYS_NOM_CLOSE = 0x10CE0      # « NtClose » (7 o, SPAN)
R_SYS_FIXTURES_FIN = 0x10CF0   # la borne préfigurée — le prochain fixture
                               # pose ICI (miroir D95 : jamais au-delà d'une
                               # borne sans arrêt nommé au geste suivant)
