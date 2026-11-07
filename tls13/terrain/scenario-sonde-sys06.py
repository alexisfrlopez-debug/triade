#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA SONDE SYS-06 (m9-(g)) : LE NTSTATUS BRUT DE LA RÉCEPTION
========================================================================
(la sonde NOMMÉE D'AVANCE par le recoup du cinquième run ET la passation
107, OUVERTE par le recoup du sixième run : LE JUMEAU CONSTATÉ PAR CODE
— le journal du run 6 == le journal du run 5 LIGNE À LIGNE, l'émission
VERT deux fois, la réception immédiate -7 deux fois, le run en SA
seconde deux fois, le bord DNS changé — LE PASSAGER ÉLIMINÉ SUR
PIÈCES ; restent le contrat de réception sys-06 et LA DEMI-FIN : UN
SEUL MOT D'INFORMATION MANQUE)

LA MISSION : lire CE QUE L'INSTRUMENT NE REMONTE PAS, AU MIROIR EXACT DE
L'ENTRÉE 185. Le bloc sys-06 (spécification m8/I/sys-06-reception.md,
RÉVISION 2) rend n ≥ 1 à la lecture réussie, -6 quand le syscall a rendu
un STATUS non nul — et CONSIGNE LE NTSTATUS BRUT DANS RDX (Q5) ; LE
ZÉRO EST LA DEMI-FIN (Q2 : le pair a fermé proprement → -7, rdx = 0).
Le scénario m9f (CFUNCTYPE) ne lit que RAX : LE CODE EXACT DE LA
PREMIÈRE LECTURE RÉELLE EST L'INFORMATION MANQUANTE NOMMÉE (la limite
NOMMÉE de l'instrument, le recoup-5 l'a dite, le recoup-6 la redit).
La sonde franchit CETTE limite PAR UN TRAMPOLINE DE CAPTURE —
l'artefact INTACT, JAMAIS reconstruit : un bloc de 33 octets posé au run
(VirtualAlloc, le MÊME geste que le trampoline NtClose du kit m9f T6 :
« ctypes ne peut pas charger rax, le trampoline le fait » — la sonde :
ctypes ne peut pas LIRE rdx, le trampoline le rend), qui APPELLE sys-06
à son adresse scellée et rend (le code de rax) EMPAQUETÉ avec (le
NTSTATUS de rdx). Les octets du trampoline sont CONSIGNÉS AU TÉMOIN :
la preuve lisible de ce qui est exécuté.

  LE TRAMPOLINE (msx64, l'ABI respectée — shadow space 0x28, pile
  alignée) :
      sub  rsp, 0x28             ; le cadre : 0x20 shadow + 8 alignement
      mov  rax, <sys-06>         ; l'adresse scellée, posée AU RUN
      call rax                   ; LE MÊME BLOC, LE MÊME GESTE
      shl  rdx, 32               ; le NTSTATUS dans les bits hauts
      mov  ecx, eax              ; le code, ZÉRO-ÉTENDU en 32 bits
      or   rcx, rdx              ; l'EMPQUETAGE (code | NTSTATUS << 32)
      mov  rax, rcx              ; le rendu
      add  rsp, 0x28
      ret

LE DÉROULÉ (chaque geste résout, jamais un numéro en cache — charte
§ 6) :

  T0 LE TÉMOIN     l'artefact relu (sha + taille), l'environnement, le
                   VRAI ntdll, la cartographie, les fixtures, les têtes
                   des SIX slots, LES DEUX contrôles T0.erratum-9 (la
                   pose du WSABUF canonique relue DANS L'IMAGE aux DEUX
                   blocs — l'artefact est le RÉPARÉ de23e577…) — LE T0
                   du kit m9f (l'artefact est LE MÊME que le kit) ;
  T1 LA RÉSOLUTION les SSN des TROIS noms du transport par les DEUX
                   lecteurs (le miroir Python + le bloc sys-02 : les
                   DEUX d'accord, le stub confronté) ;
  T2 L'ÉTABLISSEMENT sys-04 (create + bind + connect, TROIS appels NT)
                   — l'endpoint AFD TCP IPv4 établi par le VRAI afd.sys ;
  S3 LA MESURE     LE CŒUR, LE GESTE M9F DÉCOMPOSÉ : (a) le trampoline
                   posé, ses octets consignés ; (b) LE COMPAS ÉTALONNÉ —
                   un handle invalide doit rendre -6 +
                   STATUS_INVALID_HANDLE (0xC0000008) : la preuve que
                   le trampoline lit VRAIMENT rdx (un compas muet
                   arrête la sonde : échec nommé, fail-closed) ; (c) LA
                   MESURE — LE CH DE RÉFÉRENCE (la construction re-jouée
                   du m9f, 119 o : 16 03 03 00 72 || 114 o, l'aléa et
                   la clé de la sonde) ÉMIS PAR SYS-05 DIRECT (le
                   chemin RÉPARÉ du kit — vert aux runs 5/6 : la
                   reproduction), PUIS LA PREMIÈRE LECTURE PAR LE
                   TRAMPOLINE : LE CODE EXACT DU GESTE M9F, LU ET NOMMÉ
                   (n ≥ 1 : LE SERVERHELLO ARRIVÉ — la percée ; -7 : LE
                   ZÉRO, la demi-fin ; -6 : le NTSTATUS brut nommé par
                   la table — les valeurs recoupées aux sources
                   canoniques ntstatus.h, Wine ET ReactOS s'accordent
                   au bit près) ; (d) LA VARIATION TAILLE (une capacité
                   d'UN octet sur une session FRAÎCHE sacrifiée) ; (e)
                   LA VARIATION DÉLAI (la lecture re-tentée APRÈS 2 s :
                   le refus est-il transitoire ? un PENDING qui n'a pas
                   mûri ?) ; (f) LE VERDICT DE MESURE ;
  S4 LA CONTRE-ÉPREUVE : LA POIGNÉE par LE RAPPEL STANDARD (tls13-27
                   OUVRIR sur une session NEUVE ET VIERGE — le CH
                   composé PAR LA MACHINE, émis par sys-05 SANS le
                   trampoline) : si la lecture passe, LA POIGNÉE
                   CONTINUE (la ligne, la clôture) — LA PERCÉE, le
                   jalon en vue ; si elle meurt au même geste, la
                   non-régression est CONSTATÉE (le chemin standard et
                   le trampoline meurent ENSEMBLE : la mesure du
                   trampoline parle pour les DEUX) ;
  T6 LA CLÔTURE    les handles fermés (NtClose par le trombone sys-01,
                   le trampoline à deux instructions du kit m9f), le
                   trampoline libéré, l'artefact relu INCHANGÉ, la
                   cartographie libérée.

LA TABLE DES NTSTATUS NOMME CE QUI EST LU — et la CLASSE tranche les
candidats restants du recoup-6 : STATUS_PENDING (0x00000103, classe
SUCCÈS) : le noyau n'a PAS REFUSÉ, il n'a pas FINI — le bloc rend -6
sur tout status non nul : CE SERAIT LE BUG DU CONTRAT (l'erratum de la
notation, la révision de la spec) ; STATUS_INVALID_PARAMETER
(0xC000000D) : le contrat d'appel (l'IOCTL 0x12017 / l'AFD_RECV_INFO
de 24 o) ; STATUS_INVALID_DEVICE_STATE (0xC0000184) : l'état de
l'endpoint ; RESET/REFUSED/DISCONNECT : le pair ou le réseau (la
demi-fin brutale) ; rax == -7 SANS STATUS : LE ZÉRO — LA DEMI-FIN
PROPRE (sys-06 Q2 : le pair a refermé à l'offre sans SNI).

LES PIÈCES naissent toutes seules dans ./preuves-sonde-sys06/ :
  temoin-sonde-sys06.txt, sonde-sys06-journal.log, VERDICT-sonde-
  sys06.txt (+ ligne-recue.txt, journal-emissions.txt si la poignée a
  couru) — à renvoyer EN ENTIER au coffre /test/preuves-sonde-sys06/
  (dossier Drive « Triade » → « test »). Le laboratoire recoupe sur
  pièces (D138/D145/D148).

LA NOTE D'HONNÊTETÉ : la mission de la sonde est LA MESURE, PAS la
finale — un verdict « VERT-MESURE » n'est PAS le vert du critère M9-(f)
(la finale 1.0.0 attend le run m9f complet : la falsification T5 y
vit) ; si la lecture condamne LE CONTRAT DU BLOC (un PENDING ou un
AVERTISSEMENT traité en -6, un paramètre que le noyau refuse) : la
réparation sera UN ERRATUM DE LA NOTATION + LA RÉVISION DE LA SPEC
sys-06, jamais une dérive silencieuse ; si la lecture nomme LE ZÉRO
(la demi-fin propre) : le pair a refermé à l'offre sans SNI — le kit
m9f demeure acquitté, le geste sera la cible ou le SNI ; si LA LECTURE
REND DES OCTETS : LA PERCÉE — la poignée enchaîne dans le même run,
renvoyez les pièces.
"""

import ctypes
import ctypes.wintypes as wt
import hashlib
import os
import platform
import socket
import struct
import sys
import threading
import time

ICI = os.path.dirname(os.path.abspath(__file__))
PREUVES = os.path.join(ICI, "preuves-sonde-sys06")

# --- l'artefact : LE MÊME que le kit m9f RÉPARÉ (la carte génération 11) ----------
SHA_PROXY = ("de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be"
             "66b29226f")
TAILLE_PROXY = 65024

# --- les adresses scellées (le plan, source unique — R7) -------------------------
R_SYS01 = 0xA000          # l'émetteur — le trombone ABI (6 octets)
R_SYS02 = 0xA040          # le résolveur SSN — l'EAT de ntdll LUE
R_SYS04 = 0xA240          # l'établissement AFD (create + bind + connect)
R_SYS05 = 0xA540          # l'émission (IOCTL_AFD_SEND, totale ou refus)
R_SYS06 = 0xA6C0          # la réception (IOCTL_AFD_RECEIVE, bloquante)
R_TLS27 = 0xFF40          # la machine d'états du client TLS 1.3
R_TLS28 = 0x10D00         # le socle d'appel (l'erratum n° 5 l'a déplacé)
R_SYS_DEVICE = 0x10C20    # « \Device\Afd\Endpoint » UTF-16LE + NUL (42 o)
R_SYS_NOM_CREATEFILE = 0x10CB0     # « NtCreateFile » (11 o, SPAN sans NUL)
R_SYS_NOM_DEVICEIOCTL = 0x10CC0    # « NtDeviceIoControlFile » (21 o)
R_SYS_NOM_CLOSE = 0x10CE0          # « NtClose » (7 o)
R_TETE_CH = 0x10082      # l'écriture de l'en-tête du record CH (12 o)

OCTETS_SYS01 = bytes.fromhex("4989ca0f05c3")   # mov r10,rcx; syscall; ret
OCTETS_TETE_CH = bytes.fromhex("41c7021603030041c6420472")
NOM_DEVICE = "\\Device\\Afd\\Endpoint"    # le nom du périphérique AFD
MOTIF_STUB = bytes.fromhex("4c8bd1b8")         # mov r10,rcx ; mov eax —

# --- l'erratum n° 9 : LA POSE DU WSABUF canonique relue DANS L'IMAGE -------------
# (le kit EMPORTE LA PREUVE que ces octets sont LES RÉPARÉS — la sonde
# de l'Entrée 185 a mesuré 0xC0000005 SUR LA POSE « packée » (buf à +4) ;
# sys-06 EST LE BLOC MESURÉ : la même preuve au MÊME endroit)
POSE_WSABUF_OFF = 0x46                 # sys-05/+0x46 ET sys-06+0x46
OCTETS_POSE_WSABUF = bytes.fromhex("8974246048897c2468")

# --- la session : les dimensions DÉCLARÉES (tls13-27 P1) ------------------------
SESSION_TAILLE = 17520     # le contexte session
KIT96 = 96                 # aléa 32 + clé privée 32 + empreinte attendue 32
SOCLE_TAILLE = 32          # émettre ptr/ctx + recevoir ptr/ctx (tls13-28 P1)
TAMPOIN_CAPACITE = 16500   # ≥ 5 + 2^14 + 17 (É3 : l'enregistrement ENTIER)

# --- LA CIBLE ET LA CONFIANCE DU KIT (figées au laboratoire le 06/11) -----------
CIBLE = "www.cloudflare.com"
CIBLE_PORT = 443
EMPREINTE_EPINGLEE = bytes.fromhex(
    "045d0758ed7db6e7a3a1ffaffb2cd8ca2a8185318d40422145af3259b106f72f")
TEMOIN_APPLICATIF = b"HTTP/1.1 200 OK"
LIGNE_EMISE = (f"GET / HTTP/1.1\r\nHost: {CIBLE}\r\n"
               f"User-Agent: TRIADE-M9-sonde6\r\nConnection: close\r\n\r\n"
               ).encode("ascii")

# la construction re-jouée du CH (le recoup : les DEUX lecteurs)
CH_TAILLE = 114
CH_RECORD = bytes.fromhex("1603030072")    # type 22, 0x0303, longueur 114

# --- LE TRAMPOLINE DE CAPTURE : le squelette (l'imm64 de sys-06 posé au run) -----
# sub rsp,0x28 ; mov rax,imm64 ; call rax ; shl rdx,32 ; mov ecx,eax ;
# or rcx,rdx ; mov rax,rcx ; add rsp,0x28 ; ret — 33 octets, l'ABI msx64
# respectée (shadow 0x20 + alignement, la pile alignée au `call`)
SQUELETTE_TRAMPO = (b"\x48\x83\xec\x28"          # sub rsp, 0x28
                    + b"\x48\xb8" + b"\x00" * 8   # mov rax, <imm64 sys-06>
                    + b"\xff\xd0"                 # call rax
                    + b"\x48\xc1\xe2\x20"         # shl rdx, 32
                    + b"\x89\xc1"                 # mov ecx, eax (zéro-étendu)
                    + b"\x48\x09\xd1"             # or rcx, rdx
                    + b"\x48\x89\xc8"             # mov rax, rcx
                    + b"\x48\x83\xc4\x28"         # add rsp, 0x28
                    + b"\xc3")                    # ret
HANDLE_INVALIDE = 0xDEAD0000     # aligné, inexistant : le compas (le
                                # gestionnaire d'objets rend INVALID_HANDLE)

# --- LA TABLE DES NTSTATUS (la sonde NOMME ce qu'elle lit) -----------------------
# les valeurs recoupées aux sources canoniques ntstatus.h — Wine ET
# ReactOS s'accordent au bit près (vérifiés au labo le 07/11 : le
# dépôt ne grave JAMAIS de tête, la provenance est la règle)
NTSTATUS_NOMS = {
    0x00000000: "STATUS_SUCCESS",
    0x00000102: "STATUS_TIMEOUT",
    0x00000103: "STATUS_PENDING",
    0x80000005: "STATUS_BUFFER_OVERFLOW",
    0xC0000008: "STATUS_INVALID_HANDLE",
    0xC000000D: "STATUS_INVALID_PARAMETER",
    0xC0000010: "STATUS_INVALID_DEVICE_REQUEST",
    0xC00000A3: "STATUS_DEVICE_NOT_READY",
    0xC00000BF: "STATUS_NETWORK_BUSY",
    0xC00000D0: "STATUS_REQUEST_NOT_ACCEPTED",
    0xC0000120: "STATUS_CANCELLED",
    0xC000013B: "STATUS_LOCAL_DISCONNECT",
    0xC000013C: "STATUS_REMOTE_DISCONNECT",
    0xC0000184: "STATUS_INVALID_DEVICE_STATE",
    0xC000020C: "STATUS_CONNECTION_DISCONNECTED",
    0xC000020D: "STATUS_CONNECTION_RESET",
    0xC0000236: "STATUS_CONNECTION_REFUSED",
    0xC0000237: "STATUS_GRACEFUL_DISCONNECT",
    0xC000023A: "STATUS_CONNECTION_INVALID",
    0xC000023C: "STATUS_NETWORK_UNREACHABLE",
    0xC000023D: "STATUS_HOST_UNREACHABLE",
    0xC000023E: "STATUS_PROTOCOL_UNREACHABLE",
    0xC0000241: "STATUS_CONNECTION_ABORTED",
}


def classe_ntstatus(nt):
    """La classe de sévérité (les bits 31-30 de l'espace NTSTATUS) — le
    diagnostic tranche les candidats : un status de classe SUCCÈS ou
    AVERTISSEMENT traité en -6 par le bloc serait LE BUG DU CONTRAT,
    pas un refus du noyau."""
    if nt == 0:
        return "SUCCÈS (le geste a passé)"
    if nt < 0x40000000:
        return ("CLASSE SUCCÈS (sévérité 00 : PENDING vit ici) — un "
                "status de CETTE classe traité en -6 par le bloc serait "
                "LE BUG DU CONTRAT, pas un refus du noyau")
    if nt < 0x80000000:
        return ("CLASSE INFORMATION (sévérité 01) — pas une erreur : la "
                "même limite du contrat")
    if nt < 0xC0000000:
        return ("CLASSE AVERTISSEMENT (sévérité 10) — pas une erreur : "
                "la même limite du contrat")
    return "CLASSE ERREUR (sévérité 11) — un vrai refus du noyau"


def nommer_ntstatus(nt):
    nom = NTSTATUS_NOMS.get(nt)
    if nom is None:
        return f"0x{nt:08X} (non nommé par la table — la pièce fait foi)"
    return f"{nom} (0x{nt:08X})"


DONT_RESOLVE_DLL_REFERENCES = 0x00000001
PAGE_EXECUTE_READ = 0x20
PAGE_EXECUTE_READWRITE = 0x40
MEM_COMMIT = 0x1000
MEM_RELEASE = 0x8000

# --- le journal, le témoin, le verdict --------------------------------------------

_journal = []
_temoin = []
_echecs = []


def journal(msg):
    _journal.append(time.strftime("%H:%M:%S") + "  " + msg)
    print("[journal] " + msg)
    _ecrire_journal()


def temoin(msg):
    _temoin.append(msg)
    print("  " + msg)


def verifie(nom, condition, detail=""):
    if condition:
        temoin(f"[ok] {nom}" + (f" — {detail}" if detail else ""))
    else:
        temoin(f"[ÉCHEC] {nom}" + (f" — {detail}" if detail else ""))
        _echecs.append(nom)
    return bool(condition)


def _ecrire_journal():
    try:
        os.makedirs(PREUVES, exist_ok=True)
        with open(os.path.join(PREUVES, "sonde-sys06-journal.log"), "w",
                  encoding="utf-8") as f:
            f.write("\n".join(_journal) + "\n")
    except OSError:
        pass


def _ecrire_temoin():
    """Le témoin écrit AU FUR ET À MESURE (la mesure est le cœur : ses
    pièces survivent à tout arrêt ultérieur — la sonde est honnête
    jusqu'au bout)."""
    try:
        os.makedirs(PREUVES, exist_ok=True)
        with open(os.path.join(PREUVES, "temoin-sonde-sys06.txt"), "w",
                  encoding="utf-8") as f:
            f.write("\n".join(_temoin) + "\n")
    except OSError:
        pass


def sha256_fichier(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def u16(adresse):
    return struct.unpack("<H", ctypes.string_at(adresse, 2))[0]


def u32(adresse):
    return struct.unpack("<I", ctypes.string_at(adresse, 4))[0]


# --- LE MIROIR PYTHON n° 1 : la marche EAT (le lecteur indépendant de sys-02) ----

def lire_ssn_python(base, span, longueur):
    """La marche EAT refaite en Python : (code, rva_stub, detail) — LE
    MÊME contrat que sys-02."""
    try:
        e_lfanew = u32(base + 0x3C)
        if not (0x40 <= e_lfanew <= 0x400):
            return (-2, None, f"e_lfanew {e_lfanew:#x} hors fenêtre")
        if ctypes.string_at(base + e_lfanew, 4) != b"PE\x00\x00":
            return (-2, None, "le motif PE absent")
        opt = base + e_lfanew + 24
        if u16(opt) != 0x20B:
            return (-2, None, f"magic optionnel {u16(opt):#x} != 0x20B")
        exp_rva = u32(opt + 112)
        if exp_rva == 0:
            return (-3, None, "répertoire export absent")
        nb_noms = u32(base + exp_rva + 0x18)
        a_fonctions = u32(base + exp_rva + 0x1C)
        a_noms = u32(base + exp_rva + 0x20)
        a_ordinaux = u32(base + exp_rva + 0x24)
        for i in range(nb_noms):
            nom_rva = u32(base + a_noms + 4 * i)
            if ctypes.string_at(base + nom_rva, longueur) == span[:longueur]:
                ordinal = u16(base + a_ordinaux + 2 * i)
                stub_rva = u32(base + a_fonctions + 4 * ordinal)
                return (0, stub_rva, None)
        return (-1, None, f"« {span.decode('ascii', 'replace')} » introuvable"
                          f" ({nb_noms} noms marchés)")
    except Exception as exc:
        return (-99, None, f"exception Python : {exc}")


def ssn_par_deux_lecteurs(base, nom):
    """LE MÊME SSN par sys-02 ET par le miroir Python ; le motif confronté.
    Rend (ssn, stub_rva) ou lève RuntimeError."""
    span = nom.encode("ascii")
    code, rva_stub, detail = lire_ssn_python(base, span, len(span))
    if code != 0:
        raise RuntimeError(f"le miroir Python refuse « {nom} » : {detail}")
    octets_stub = ctypes.string_at(base + rva_stub, 8)
    if octets_stub[:4] != MOTIF_STUB:
        raise RuntimeError(f"le stub de « {nom} » diverge : "
                            f"{octets_stub[:4].hex()} != {MOTIF_STUB.hex()} — "
                            "un stub crocheté (un hook ?) : le numéro NE "
                            "SERA JAMAIS extrait d'un stub inattendu")
    ssn_attendu = struct.unpack("<I", octets_stub[4:8])[0]
    r = SYS02(span, len(span), base)
    if r != ssn_attendu:
        raise RuntimeError(f"sys-02 rend {r}, le miroir Python "
                            f"{ssn_attendu} — les DEUX lecteurs divergent")
    return ssn_attendu, rva_stub


# --- LE MIROIR PYTHON n° 2 : l'échelle X25519 (RFC 7748 § 5) ---------------------

def x25519_echelle(priv, point_base=9):
    """L'échelle de Montgomery EN PUR PYTHON (l'erratum n° 7 : x_3 NAÎT
    AU POINT DE BASE, a24 = 121665 — le pseudocode officiel RFC 7748
    § 5)."""
    p = 2 ** 255 - 19

    def cswap(swap, a, b):
        return (b, a) if swap else (a, b)

    k = int.from_bytes(priv, "little")
    k &= (1 << 254) - 8             # le clamp RFC 7748 § 5 (248/127/64)
    k |= 1 << 254
    u = point_base % p
    x1 = u
    x2, z2, x3, z3 = 1, 0, u, 1     # x_3 = u — LE POINT DE BASE
    swap = 0
    for t in range(254, -1, -1):
        k_t = (k >> t) & 1
        swap ^= k_t
        x2, x3 = cswap(swap, x2, x3)
        z2, z3 = cswap(swap, z2, z3)
        swap = k_t
        a = (x2 + z2) % p
        aa = a * a % p
        b = (x2 - z2) % p
        bb = b * b % p
        e = (aa - bb) % p
        c = (x3 + z3) % p
        d = (x3 - z3) % p
        da = d * a % p
        cb = c * b % p
        x3 = (da + cb) ** 2 % p
        z3 = x1 * (da - cb) ** 2 % p
        x2 = aa * bb % p
        z2 = e * (aa + 121665 * e) % p   # a24 = (486662-2)/4 = 121665
    x2, x3 = cswap(swap, x2, x3)
    z2, z3 = cswap(swap, z2, z3)
    return (x2 * pow(z2, p - 2, p) % p).to_bytes(32, "little")


def construction_ch_reference(alea, cle_publique):
    """La construction re-jouée du plan (114 o FIXES) — LE MÊME CH que
    le kit m9f (la charge de la mesure est L'OFFRE DU JALON)."""
    def u16be(x):
        return struct.pack(">H", x)
    exts = (u16be(0x002B) + u16be(3) + bytes([2]) + u16be(0x0304)
            + u16be(0x000A) + u16be(4) + u16be(2) + u16be(0x001D)
            + u16be(0x000D) + u16be(6) + u16be(4) + u16be(0x0804)
            + u16be(0x0401)
            + u16be(0x0033) + u16be(38) + u16be(36) + u16be(0x001D)
            + u16be(32) + cle_publique)
    corps = (u16be(0x0303) + alea + bytes([0])
             + u16be(2) + u16be(0x1301) + bytes([1, 0])
             + u16be(len(exts)) + exts)
    ch = bytes([1]) + len(corps).to_bytes(3, "big") + corps
    assert len(ch) == 114
    return ch


# --- LES APPELÉES DE L'ARTEFACT (les CFUNCTYPE aux adresses scellées) ------------

SYS02 = None      # posé au T0 (la base connue)
SYS04 = None
SYS05 = None
SYS06 = None
TLS27 = None


def lier_blocs(base):
    global SYS02, SYS04, SYS05, SYS06, TLS27
    SYS02 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p, ctypes.c_uint64,
                             ctypes.c_void_p)(base + R_SYS02)
    SYS04 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p, ctypes.c_void_p,
                             ctypes.c_void_p)(base + R_SYS04)
    SYS05 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p, ctypes.c_uint64,
                             ctypes.c_void_p, ctypes.c_uint64)(base + R_SYS05)
    SYS06 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p, ctypes.c_uint64,
                             ctypes.c_void_p, ctypes.c_uint64)(base + R_SYS06)
    TLS27 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64,
                             ctypes.c_void_p, ctypes.c_uint64)(base + R_TLS27)


def depaqueter(rendu):
    """Le rendu empaqueté du trampoline : (code 32 signé, NTSTATUS u32).
    rax rendu = (NTSTATUS << 32) | (code & 0xFFFFFFFF)."""
    code_u32 = rendu & 0xFFFFFFFF
    code = code_u32 - (1 << 32) if code_u32 >= (1 << 31) else code_u32
    nt = (rendu >> 32) & 0xFFFFFFFF
    return code, nt


# --- la garde-chien (un transport muet est une information, pas une attente) ----

def _garde_chien():
    journal("LA GARDE-CHIEN : 300 s écoulées — le transport est muet ; "
            "les pièces écrites à l'instant demeurent, fermez la fenêtre "
            "et renvoyez preuves-sonde-sys06/ TEL QUELLE (un échec nommé "
            "vaut plus qu'un vert muet)")
    _ecrire_temoin()
    _verdict()
    os._exit(3)


def armer_garde_chien():
    t = threading.Timer(300.0, _garde_chien)
    t.daemon = True
    t.start()


# --- LE RUN ----------------------------------------------------------------------

class RefusNomme(RuntimeError):
    pass


def main():
    print("=== LA SONDE SYS-06 : LE CODE EXACT DE LA PREMIÈRE LECTURE "
          "RÉELLE (la sonde nommée d'avance, ouverte par le recoup du "
          "sixième run — le passager éliminé sur pièces, la limite "
          "NOMMÉE de l'instrument franchie sans reconstruire "
          "l'artefact) ===\n")
    os.makedirs(PREUVES, exist_ok=True)
    armer_garde_chien()

    # ---------------- T0 — LE TÉMOIN ------------------------------------------
    print("T0 — LE TÉMOIN (les empreintes, l'environnement, la cartographie)")
    chemin_proxy = os.path.join(ICI, "proxy.exe")
    if not os.path.isfile(chemin_proxy):
        print(f"ÉCHEC NOMMÉ : proxy.exe introuvable ({chemin_proxy})")
        return 1
    sha_proxy = sha256_fichier(chemin_proxy)
    verifie("T0.proxy : l'empreinte de l'artefact",
            sha_proxy == SHA_PROXY, f"sha256 {sha_proxy[:16]}…")
    verifie("T0.proxy : la taille",
            os.path.getsize(chemin_proxy) == TAILLE_PROXY,
            f"{os.path.getsize(chemin_proxy)} o")

    if sys.platform != "win32":
        print(f"ÉCHEC NOMMÉ : cette sonde exige Windows (sys.platform="
              f"{sys.platform!r}) — le VRAI ntdll et le VRAI afd.sys")
        return 1
    if struct.calcsize("P") != 8:
        print("ÉCHEC NOMMÉ : cette sonde exige un Python 64 bits "
              f"(pointeur {struct.calcsize('P') * 8} bits)")
        return 1

    wv = sys.getwindowsversion()
    temoin(f"[env] Windows {wv.major}.{wv.minor} build {wv.build}")
    temoin(f"[env] Python {platform.python_version()} · {platform.machine()}")

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.GetModuleHandleW.restype = ctypes.c_void_p
    k32.GetModuleHandleW.argtypes = [wt.LPCWSTR]
    k32.LoadLibraryExW.restype = ctypes.c_void_p
    k32.LoadLibraryExW.argtypes = [wt.LPCWSTR, ctypes.c_void_p, wt.DWORD]
    k32.VirtualProtect.restype = wt.BOOL
    k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t, wt.DWORD,
                                   ctypes.POINTER(wt.DWORD)]
    k32.VirtualAlloc.restype = ctypes.c_void_p
    k32.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, wt.DWORD,
                                 wt.DWORD]
    k32.VirtualFree.restype = wt.BOOL
    k32.VirtualFree.argtypes = [ctypes.c_void_p, ctypes.c_size_t, wt.DWORD]
    k32.FreeLibrary.restype = wt.BOOL
    k32.FreeLibrary.argtypes = [ctypes.c_void_p]

    ntdll_base = k32.GetModuleHandleW("ntdll")
    verifie("T0.ntdll : le VRAI ntdll localisé", bool(ntdll_base),
            f"base {ntdll_base:#x}")
    chemin_ntdll = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"),
                                "System32", "ntdll.dll")
    temoin(f"[env] ntdll : {chemin_ntdll}")
    temoin(f"[env] ntdll sha256 : {sha256_fichier(chemin_ntdll)}")

    # la cartographie : DONT_RESOLVE — aucune entrée résolue
    base = k32.LoadLibraryExW(chemin_proxy, None,
                              DONT_RESOLVE_DLL_REFERENCES)
    verifie("T0.carte : l'artefact cartographié", bool(base),
            f"base {base:#x}")
    if not base:
        print(f"ÉCHEC NOMMÉ : LoadLibraryEx a rendu "
              f"{ctypes.get_last_error()}")
        return 1

    # la section exécutable réaffirmée (le geste du chargeur, miroir m8d)
    vieux = wt.DWORD()
    k32.VirtualProtect(base + 0xA000, 0x2000, PAGE_EXECUTE_READ,
                       ctypes.byref(vieux))
    k32.VirtualProtect(base + 0xC000, 0x4E00, PAGE_EXECUTE_READ,
                       ctypes.byref(vieux))

    # les octets attendus, constatés UN PAR UN
    verifie("T0.sys-01 : le trombone ABI",
            ctypes.string_at(base + R_SYS01, 6) == OCTETS_SYS01,
            f"{ctypes.string_at(base + R_SYS01, 6).hex()}")
    verifie("T0.fixture-device : le périphérique AFD UTF-16LE + NUL",
            ctypes.string_at(base + R_SYS_DEVICE, 42)
            == NOM_DEVICE.encode("utf-16le") + b"\x00\x00",
            f"{NOM_DEVICE!r} — 42 o")
    for rva, nom in ((R_SYS_NOM_CREATEFILE, "NtCreateFile"),
                     (R_SYS_NOM_DEVICEIOCTL, "NtDeviceIoControlFile"),
                     (R_SYS_NOM_CLOSE, "NtClose")):
        verifie(f"T0.fixture-span : « {nom} »",
                ctypes.string_at(base + rva, len(nom)) == nom.encode(),
                f"@{rva:#x}")
    verifie("T0.erratum-5 : l'octet de longueur du record CH relu "
            "(41 C7 02 16 03 03 00 41 C6 42 04 72)",
            ctypes.string_at(base + R_TETE_CH, 12) == OCTETS_TETE_CH,
            f"@{R_TETE_CH:#x}")
    # l'erratum n° 9 : LA POSE DU WSABUF canonique relue DANS L'IMAGE aux
    # DEUX blocs — le kit EMPORTE LA PREUVE que ces octets sont LES RÉPARÉS
    # (la sonde de l'Entrée 185 a mesuré 0xC0000005 sur la pose « packée »)
    for rva, nom in ((R_SYS05, "sys-05"), (R_SYS06, "sys-06")):
        verifie(f"T0.erratum-9 : LA POSE DU WSABUF canonique relu dans "
                f"{nom} (89 74 24 60 48 89 7c 24 68 — buf à +8)",
                ctypes.string_at(base + rva + POSE_WSABUF_OFF, 9)
                == OCTETS_POSE_WSABUF,
                f"@{rva + POSE_WSABUF_OFF:#x}")
    for rva, nom in ((R_SYS02, "sys-02"), (R_SYS04, "sys-04"),
                     (R_SYS05, "sys-05"), (R_SYS06, "sys-06"),
                     (R_TLS27, "tls13-27"), (R_TLS28, "tls13-28")):
        tete = ctypes.string_at(base + rva, 6)
        verifie(f"T0.slot : la tête {nom} @{rva:#x}",
                tete != b"\x00" * 6 and tete != b"\xcc" * 6, tete.hex())

    # la cible résolue
    infos = socket.getaddrinfo(CIBLE, CIBLE_PORT, socket.AF_INET,
                               socket.SOCK_STREAM)
    ip_cible = infos[0][4][0]
    temoin(f"[cible] {CIBLE}:{CIBLE_PORT} → {ip_cible} (DNS résolu au run)")
    temoin(f"[cible] l'empreinte ÉPINGLÉE : {EMPREINTE_EPINGLEE.hex()}")

    lier_blocs(base)
    journal("T0 " + ("VERT" if not _echecs else f"échecs : {_echecs}"))
    if _echecs:
        return _verdict()

    # ---------------- T1 — LA RÉSOLUTION ----------------------------------------
    print("\nT1 — LA RÉSOLUTION (le VRAI ntdll lu par les DEUX lecteurs)")
    try:
        ssn_create, _ = ssn_par_deux_lecteurs(ntdll_base, "NtCreateFile")
        ssn_ioctl, _ = ssn_par_deux_lecteurs(
            ntdll_base, "NtDeviceIoControlFile")
        ssn_close, _ = ssn_par_deux_lecteurs(ntdll_base, "NtClose")
    except RuntimeError as e:
        journal(f"T1 : {e}")
        _echecs.append("T1.la-résolution")
        return _verdict()
    temoin(f"[T1] NtCreateFile          SSN {ssn_create} (motif sain)")
    temoin(f"[T1] NtDeviceIoControlFile SSN {ssn_ioctl} "
           "(jamais un numéro en cache : chaque geste résout)")
    temoin(f"[T1] NtClose               SSN {ssn_close}")
    journal("T1 VERT : les DEUX lecteurs d'accord sur les TROIS noms")

    # ---------------- T2 — L'ÉTABLISSEMENT --------------------------------------
    print("\nT2 — L'ÉTABLISSEMENT (le socket par le VRAI afd.sys)")

    def etablir(tag):
        """sys-04 : create + bind + connect, TROIS appels NT."""
        sockaddr = (struct.pack("<H", 2)
                    + struct.pack(">H", CIBLE_PORT)
                    + socket.inet_aton(ip_cible)
                    + b"\x00" * 8)
        buf_sa = ctypes.create_string_buffer(sockaddr, 16)
        handle_sortie = ctypes.c_uint64(0)
        r = SYS04(ntdll_base, ctypes.cast(buf_sa, ctypes.c_void_p),
                  ctypes.cast(ctypes.byref(handle_sortie),
                              ctypes.c_void_p))
        verifie(f"{tag} : sys-04 (create + bind + connect, TROIS appels "
                "NT)", r == 0 and handle_sortie.value != 0,
                f"rax {r}, handle {handle_sortie.value:#x}")
        if r != 0:
            journal(f"{tag} : rax {r} — l'établissement a échoué "
                    "(le socle a nommé son refus)")
            raise RefusNomme(f"{tag} : l'établissement a échoué "
                             f"(verdict {r})")
        return handle_sortie.value

    try:
        handle_1 = etablir("T2.session-1")
    except RefusNomme as e:
        journal(f"T2 : {e}")
        return _verdict()
    journal("T2 VERT : l'endpoint AFD TCP IPv4 établi (le VRAI afd.sys, "
            "zéro ws2_32)")

    # ---------------- S3 — LA MESURE (LE CŒUR) -----------------------------------
    # les handles de la sonde : handle_1 (la mesure), handle_2 (la
    # session sacrifiée de la variation (d), posée DANS la branche),
    # handle_p (la contre-épreuve S4)
    handle_2 = 0
    print("\nS3 — LA MESURE (le geste m9f DÉCOMPOSÉ : l'offre par sys-05 "
          "direct, LA PREMIÈRE LECTURE par le trampoline de capture — le "
          "code exact que l'instrument ne remonte pas)")

    # (a) le trampoline posé, ses octets consignés
    zone_trampo = k32.VirtualAlloc(None, 64, MEM_COMMIT,
                                   PAGE_EXECUTE_READWRITE)
    verifie("S3.trampo : la zone de capture allouée (VirtualAlloc RWX, "
            "64 o)", bool(zone_trampo), f"zone {zone_trampo:#x}")
    corps_trampo = (SQUELETTE_TRAMPO[:6]
                    + struct.pack("<Q", base + R_SYS06)
                    + SQUELETTE_TRAMPO[14:])
    ctypes.memmove(zone_trampo, corps_trampo, len(corps_trampo))
    trampo = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                              ctypes.c_uint64, ctypes.c_void_p,
                              ctypes.c_uint64)(zone_trampo)
    temoin(f"[S3] le trampoline de capture : {len(corps_trampo)} o — "
          f"{corps_trampo.hex()}")
    temoin("[S3] le trampoline appelé : sub rsp,0x28 ; mov rax,sys-06 ; "
           "call rax ; shl rdx,32 ; mov ecx,eax ; or rcx,rdx ; mov "
           "rax,rcx ; add rsp,0x28 ; ret — LE MÊME BLOC, le NTSTATUS "
           "rendu avec le code")

    # (b) LE COMPAS ÉTALONNÉ : un handle invalide doit rendre -6 +
    # STATUS_INVALID_HANDLE — la preuve que la capture lit VRAIMENT rdx
    buf_1o = ctypes.create_string_buffer(b"\x00", 1)
    rendu = trampo(ntdll_base, HANDLE_INVALIDE,
                   ctypes.cast(buf_1o, ctypes.c_void_p), 1)
    code_c, nt_c = depaqueter(rendu)
    verifie("S3.compas : le handle invalide rend -6 + "
            "STATUS_INVALID_HANDLE (0xC0000008) — la capture lit "
            "VRAIMENT rdx (un compas muet arrête la sonde)",
            code_c == -6 and nt_c == 0xC0000008,
            f"lu : code {code_c}, {nommer_ntstatus(nt_c)}")
    journal("S3.compas : le compas étalonné — le handle invalide rend "
            f"{nommer_ntstatus(nt_c)}")
    if code_c != -6 or nt_c != 0xC0000008:
        # fail-closed : la mesure suivante serait SANS VALEUR
        journal("S3 : le compas est MUET — la mesure est refusée (un "
                "instrument non étalonné ne mesure pas)")
        _verdict()
        return 1

    # (c) LA MESURE — LE GESTE M9F DÉCOMPOSÉ : (1) le ClientHello DE
    # RÉFÉRENCE émis par SYS-05 DIRECT (le chemin RÉPARÉ du kit — vert
    # aux runs 5/6 : la reproduction) ; (2) LA PREMIÈRE LECTURE par LE
    # TRAMPOLINE : LE CODE EXACT ENFIN LU (n / -7 le zéro / -6 + le
    # NTSTATUS brut)
    alea_sonde = os.urandom(32)
    privee_sonde = os.urandom(32)
    pub_sonde = x25519_echelle(privee_sonde)
    ch_sonde = CH_RECORD + construction_ch_reference(alea_sonde, pub_sonde)
    buf_ch = ctypes.create_string_buffer(ch_sonde, len(ch_sonde))
    temoin(f"[S3] l'aléa de la sonde    : {alea_sonde.hex()}")
    temoin(f"[S3] la clé privée de la sonde : {privee_sonde.hex()}")
    temoin(f"[S3] la clé publique (l'échelle Python) : {pub_sonde.hex()}")
    temoin(f"[S3] la charge : LE CH DE RÉFÉRENCE (16 03 03 00 72 || "
          f"114 o) — {len(ch_sonde)} o")
    r_emission = SYS05(ntdll_base, handle_1,
                       ctypes.cast(buf_ch, ctypes.c_void_p), len(ch_sonde))
    temoin(f"[S3] L'OFFRE (sys-05 direct, le chemin réparé du kit) : rax "
          f"{r_emission}" + (" — le CH PARTI (la reproduction des runs "
                             "5/6 : l'émission est VERT)"
                             if r_emission == 0 else
                             " — ANOMALIE NOMMÉE (les runs 5/6 l'ont eue "
                             "VERT : la pièce fait foi)"))
    journal(f"S3.offre : sys-05 direct rend {r_emission} "
            + ("(le CH parti)" if r_emission == 0 else "(ANOMALIE nommée)"))
    buf_lecture = ctypes.create_string_buffer(TAMPOIN_CAPACITE)
    rendu = trampo(ntdll_base, handle_1,
                   ctypes.cast(buf_lecture, ctypes.c_void_p),
                   TAMPOIN_CAPACITE)
    code_m, nt_m = depaqueter(rendu)
    if code_m >= 1:
        tete_flux = bytes(buf_lecture.raw[:min(code_m, 64)])
        temoin(f"[S3] LA MESURE (la première lecture réelle, la capture) : "
              f"code {code_m} — LA LECTURE A RENDU {code_m} OCTETS : LE "
              f"SERVERHELLO ARRIVÉ — LA PERCÉE ; NTSTATUS "
              f"{nommer_ntstatus(nt_m)} — {classe_ntstatus(nt_m)}")
        temoin(f"[S3] la tête du flux reçu : {tete_flux.hex()}…")
    else:
        temoin(f"[S3] LA MESURE (la première lecture réelle, la capture) : "
              f"code {code_m}, NTSTATUS {nommer_ntstatus(nt_m)} — "
              f"{classe_ntstatus(nt_m)}"
              + (" — LE ZÉRO : LA DEMI-FIN (sys-06 Q2 : le pair a refermé "
                 "proprement à l'offre)" if code_m == -7 and nt_m == 0
                 else ""))
    journal(f"S3.mesure : la première lecture par le trampoline : code "
            f"{code_m}, NTSTATUS {nommer_ntstatus(nt_m)}")
    if code_m >= 1:
        journal("S3.mesure : LA LECTURE A VÉCU — le ServerHello EST ARRIVÉ "
                "(la percée de lecture est consignée, la contre-épreuve "
                "S4 dira si la machine d'états passe aussi)")
    else:
        # (d) LA VARIATION TAILLE : une capacité d'UN octet sur une session
        # FRAÎCHE sacrifiée (l'offre y est émise, la lecture y est tentée
        # à la capacité minimale du contrat P4 : 1 ≤ r9)
        try:
            handle_2 = etablir("S3.d.session-sacrifiée")
            r_offre_d = SYS05(ntdll_base, handle_2,
                              ctypes.cast(buf_ch, ctypes.c_void_p),
                              len(ch_sonde))
            rendu = trampo(ntdll_base, handle_2,
                           ctypes.cast(buf_1o, ctypes.c_void_p), 1)
            code_d, nt_d = depaqueter(rendu)
            temoin(f"[S3] LA VARIATION TAILLE (capacité 1, session fraîche "
                  f"— l'offre y a rendu rax {r_offre_d}) : code {code_d}, "
                  f"NTSTATUS {nommer_ntstatus(nt_d)} — "
                  f"{classe_ntstatus(nt_d)}")
            journal(f"S3.variation-taille : capacité 1 : code {code_d}, "
                    f"{nommer_ntstatus(nt_d)}")
        except RefusNomme:
            handle_2 = 0
            journal("S3.variation-taille : la session sacrifiée n'a pas "
                    "pu être établie — la variation n'a pas couru")
        # (e) LA VARIATION DÉLAI : la lecture re-tentée après 2 s sur LA
        # MÊME session (le refus est-il transitoire ? un PENDING qui n'a
        # pas mûri ?)
        time.sleep(2.0)
        rendu = trampo(ntdll_base, handle_1,
                       ctypes.cast(buf_lecture, ctypes.c_void_p),
                       TAMPOIN_CAPACITE)
        code_e, nt_e = depaqueter(rendu)
        temoin(f"[S3] LA VARIATION DÉLAI (la lecture re-tentée après 2 s) : "
              f"code {code_e}, NTSTATUS {nommer_ntstatus(nt_e)} — "
              f"{classe_ntstatus(nt_e)}")
        journal(f"S3.variation-délai : après 2 s : code {code_e}, "
                f"{nommer_ntstatus(nt_e)}")

    # LE VERDICT DE MESURE : la mission est RENDUE si le compas est
    # étalonné ET la lecture consignée (le témoin écrit AU FUR ET À
    # MESURE survit à tout)
    compas_ok = (code_c == -6 and nt_c == 0xC0000008)
    lecture_consignee = any("LA MESURE (la première lecture réelle" in l
                            for l in _temoin)
    verifie("S3.mesure : LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE LU "
            "ET NOMMÉ (la limite nommée de l'instrument, franchie)",
            compas_ok and lecture_consignee,
            f"code {code_m}, {nommer_ntstatus(nt_m)} — "
            f"{classe_ntstatus(nt_m)}")
    journal("S3 " + ("VERT : LA MESURE RENDUE" if not _echecs
                     else f"échecs : {_echecs}"))
    _ecrire_temoin()

    # ---------------- S4 — LA CONTRE-ÉPREUVE (LE RAPPEL STANDARD) ----------------
    # TOUJOURS sur une session NEUVE ET VIERGE (handle_p) : la poignée
    # ENTIÈRE par le chemin du kit m9f (SANS le trampoline) — la
    # machine d'états compose ET émet SON CH, lit SA réponse : la
    # non-régression du chemin standard, ou LA PERCÉE
    print("\nS4 — LA CONTRE-ÉPREUVE (la poignée par LE RAPPEL STANDARD : "
          "le chemin du kit m9f, une session NEUVE, sans le trampoline)")
    session_s4 = None
    handle_p = 0
    poignee_tenue = False
    alea_p = os.urandom(32)
    privee_p = os.urandom(32)

    journal_emissions = []

    def rappel_emission(ctx, ptr, n):
        journal_emissions.append(bytes(ctypes.string_at(ptr, n)))
        r = SYS05(ntdll_base, handle_p, ptr, n)
        if r != 0:
            journal(f"le rappel émission : sys-05 rend {r} (l'émission "
                    "TOTALE ou refusée — jamais un demi-envoi déguisé)")
        return r

    def rappel_reception(ctx, ptr, capacite):
        return SYS06(ntdll_base, handle_p, ptr, capacite)

    cb_e = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                            ctypes.c_void_p, ctypes.c_uint64)(
                                rappel_emission)
    cb_r = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p,
                            ctypes.c_void_p, ctypes.c_uint64)(
                                rappel_reception)
    ctx_neutre = ctypes.c_uint64(0)
    socle = (ctypes.c_uint64 * 4)(
        ctypes.cast(cb_e, ctypes.c_void_p).value,
        ctypes.addressof(ctx_neutre),
        ctypes.cast(cb_r, ctypes.c_void_p).value,
        ctypes.addressof(ctx_neutre))
    session = ctypes.create_string_buffer(SESSION_TAILLE)
    kit96 = ctypes.create_string_buffer(alea_p + privee_p
                                        + EMPREINTE_EPINGLEE, KIT96)
    try:
        handle_p = etablir("S4.session")
    except RefusNomme:
        handle_p = 0
        journal("S4 : la session de la contre-épreuve n'a pu être "
                "établie — la contre-épreuve n'a pas couru")
    if handle_p:
        journal("S4 : OUVRIR — la poignée ENTIÈRE par la machine "
                "d'états (le socle câblé aux SYSCALLS DIRECTS, SANS le "
                "trampoline)")
        r = TLS27(ctypes.cast(session, ctypes.c_void_p), 1,
                  ctypes.cast(socle, ctypes.c_void_p),
                  ctypes.addressof(kit96))
        etat = struct.unpack_from("<I", session.raw, 1120)[0]
        if r == 0 and etat == 3:
            session_s4 = session
            temoin("[S4] LA CONTRE-ÉPREUVE PASSE : la machine d'états A "
                  "ÉTABLI LA SESSION par le chemin standard — LA "
                  "PERCÉE, le jalon en vue (le refus n'a pas tenu)")
            journal("S4 : LA POIGNÉE PASSE — le CH est parti par le "
                    "rappel standard, la session EST CONNECTÉE")
            # la ligne applicative (le critère du jalon) : É2 ÉMETTRE
            # puis É3 RECEVOIR (la boucle du m9f : 64 records au plus)
            ligne = ctypes.create_string_buffer(LIGNE_EMISE,
                                                len(LIGNE_EMISE))
            r4 = TLS27(ctypes.cast(session, ctypes.c_void_p), 2,
                       ctypes.cast(ligne, ctypes.c_void_p),
                       len(LIGNE_EMISE))
            verifie("S4.ligne : la ligne émise (rax == 0)", r4 == 0,
                    f"rax {r4}")
            if r4 == 0:
                tampon = ctypes.create_string_buffer(TAMPOIN_CAPACITE)
                flux_recu = b""
                temoin_trouve = False
                for i in range(64):
                    r5 = TLS27(ctypes.cast(session, ctypes.c_void_p), 3,
                               ctypes.cast(tampon, ctypes.c_void_p),
                               TAMPOIN_CAPACITE)
                    if r5 < 0:
                        if temoin_trouve:
                            journal(f"S4 : le transport a rendu {r5} APRÈS "
                                    "le témoin — la ligne est ÉCHANGÉE, "
                                    "la fin est honnête")
                            break
                        journal(f"S4 : É3 rend {r5} — la session est morte "
                                "avant la ligne")
                        break
                    if r5 == 0:
                        journal("S4 : le close_notify du serveur (la fin "
                                "PROPRE du protocole)")
                        break
                    flux_recu += tampon.raw[:r5]
                    if TEMOIN_APPLICATIF in flux_recu:
                        temoin_trouve = True
                        journal(f"S4 : le témoin « {TEMOIN_APPLICATIF.decode()} "
                                f"» REÇU et DÉCHIFFRÉ PAR LA MACHINE "
                                f"(record {i + 1}, {r5} o restitués)")
                        break
                verifie("S4.témoin-applicatif : la ligne applicative "
                        "chiffrée ÉCHANGÉE — le témoin dans le flux "
                        "DÉCHIFFRÉ PAR LA MACHINE", temoin_trouve,
                        f"{len(flux_recu)} o reconstitués")
                temoin(f"[S4] la tête du flux reçu : "
                      f"{flux_recu[:48].hex()}…")
                with open(os.path.join(PREUVES, "ligne-recue.txt"),
                          "wb") as f:
                    f.write(flux_recu[:65536])
                poignee_tenue = temoin_trouve
        else:
            temoin(f"[S4] la contre-épreuve : la machine d'états meurt AU "
                  f"MÊME GESTE (rax {r}, état {etat}) — la "
                  "non-régression CONSTATÉE : le chemin standard et le "
                  "trampoline meurent ENSEMBLE (la mesure du trampoline "
                  "parle pour les DEUX)")
            journal(f"S4 : la poignée meurt au geste standard (rax {r}, "
                    f"état {etat}) — le refus est AU BLOC, pas au "
                    "trampoline")
    if journal_emissions:
        with open(os.path.join(PREUVES, "journal-emissions.txt"),
                  "wb") as f:
            f.write(b"".join(journal_emissions))
        temoin(f"[S4] les émissions de la contre-épreuve : "
              f"{len(journal_emissions)} enregistrement(s), "
              f"{sum(len(e) for e in journal_emissions)} o")

    # ---------------- T6 — LA CLÔTURE --------------------------------------------
    print("\nT6 — LA CLÔTURE (les handles fermés, le trampoline libéré, "
          "l'artefact relu INCHANGÉ)")
    if session_s4 is not None:
        # le close_notify composé et scellé PAR LA MACHINE (É4)
        r = TLS27(ctypes.cast(session_s4, ctypes.c_void_p), 4,
                  ctypes.c_void_p(0), 0)
        etat = struct.unpack_from("<I", session_s4.raw, 1120)[0]
        verifie("T6.fermer : le close_notify composé, scellé, ÉMIS "
                "(état 4)", r == 0 and etat == 4, f"rax {r}, état {etat}")
        if journal_emissions:
            verifie("T6.close_notify : la dernière émission == 24 o "
                    "(5 + 2 + 17 : le scellé de 01 00)",
                    len(journal_emissions[-1]) == 24,
                    f"{len(journal_emissions[-1])} o")
    trampoline_zone = k32.VirtualAlloc(None, 64, MEM_COMMIT,
                                       PAGE_EXECUTE_READWRITE)
    # l'erratum n° 8 (le recoup du run 1 de la sonde, Entrée 185) : le jmp
    # rel32 NE PEUT PAS coder la distance zone→artefact — VirtualAlloc
    # atterrit à ~126 Tio de la base : struct.error, le run meurt dans T6
    # AVANT le verdict. L'ADRESSAGE ABSOLU (le MÊME patron que le
    # trampoline de capture : lui, a traversé) : mov rax,SSN ; mov
    # rdx,sys-01 ; jmp rdx
    corps = (b"\x48\xb8" + struct.pack("<Q", ssn_close)
             + b"\x48\xba" + struct.pack("<Q", base + R_SYS01)
             + b"\xff\xe2")
    ctypes.memmove(trampoline_zone, corps, len(corps))
    fermer = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)(
        trampoline_zone)

    def fermer_handle(handle, tag):
        status = fermer(ctypes.c_void_p(handle))
        verifie(f"{tag} : NtClose émis par sys-01 (le trombone ABI)",
                status == 0,
                f"NTSTATUS {status & 0xffffffffffffffff:#x}")
        return status == 0

    fermer_handle(handle_1, "T6.session-1")
    # la liste EXPLICITE (les handles posés : la session sacrifiée de la
    # variation (d), la session de la contre-épreuve S4)
    autres = (("handle_2", handle_2), ("handle_p", handle_p))
    for nom, valeur in autres:
        if valeur:
            fermer_handle(valeur, f"T6.{nom}")
    k32.VirtualFree(trampoline_zone, 0, MEM_RELEASE)
    k32.VirtualFree(zone_trampo, 0, MEM_RELEASE)
    verifie("T6.intégrité : proxy.exe relu inchangé",
            sha256_fichier(chemin_proxy) == SHA_PROXY)
    k32.FreeLibrary(base)
    journal("T6 " + ("VERT" if not _echecs else f"échecs : {_echecs}"))

    return _verdict()


def _verdict():
    lignes = []
    lignes.append("TRIADE — LA SONDE SYS-06 : LE CODE EXACT DE LA "
                  "PREMIÈRE LECTURE RÉELLE")
    lignes.append("=" * 72)
    lignes.append(f"le run : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lignes.append("")
    if _echecs:
        lignes.append(f"VERDICT : ROUGE — {len(_echecs)} échec(s) "
                      "nommé(s) :")
        for nom in _echecs:
            lignes.append(f"  - {nom}")
        lignes.append("")
        lignes.append("Un échec honnête vaut plus qu'un vert muet : la "
                      "ligne NOMME le défaut. Renvoyez preuves-sonde-"
                      "sys06/ TEL QUEL au coffre /test/preuves-sonde-"
                      "sys06/.")
    else:
        lignes.append("VERDICT : VERT — LA MESURE RENDUE :")
        lignes.append("  - le compas étalonné (le handle invalide rend "
                      "-6 + STATUS_INVALID_HANDLE : la capture lit "
                      "VRAIMENT rdx) ;")
        lignes.append("  - LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE "
                      "LU ET NOMMÉ (la limite nommée de l'instrument, "
                      "franchie par le trampoline — l'artefact INTACT) : "
                      "n ≥ 1 le ServerHello arrivé, -7 le zéro de la "
                      "demi-fin, ou -6 + le NTSTATUS brut nommé ;")
        lignes.append("  - les variations (taille, délai) consignées ;")
        lignes.append("  - la contre-épreuve standard : la non-régression "
                      "constatée (ou la percée, si la poignée a tenu).")
        lignes.append("")
        lignes.append("LA MISSION DE LA SONDE EST LA MESURE, PAS LA "
                      "FINALE : un verdict VERT-MESURE n'est PAS le vert "
                      "du critère M9-(f) — la finale 1.0.0 attend le run "
                      "m9f complet (la falsification T5 y vit). Renvoyez "
                      "preuves-sonde-sys06/ EN ENTIER au coffre "
                      "/test/preuves-sonde-sys06/ : le laboratoire "
                      "recoupe sur pièces (D138/D145/D148), nomme le "
                      "coupable (le contrat du bloc sys-06, ou la "
                      "demi-fin du pair) et répare selon la charte "
                      "(l'erratum de la notation, la révision de la "
                      "spec sys-06 — jamais une dérive silencieuse).")
    lignes.append("")
    lignes.extend(_temoin)
    with open(os.path.join(PREUVES, "VERDICT-sonde-sys06.txt"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    _ecrire_temoin()
    _ecrire_journal()
    print("\n" + "\n".join(lignes[:12]))
    print(f"\n[pièces] {PREUVES} — témoin, journal, verdict")
    return 1 if _echecs else 0


if __name__ == "__main__":
    sys.exit(main())
